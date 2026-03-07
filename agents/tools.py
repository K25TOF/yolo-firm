"""Engineer execution tools for YOLO Org Learning.

Provides run_backtest() — executes backtests using the yolo backtesting engine
against cached market data. Cache-only mode: no live Polygon API calls.
"""

from __future__ import annotations

import csv
import logging
import os
import sys
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

logger = logging.getLogger(__name__)

AGENTS_DIR = Path(__file__).parent
MIN_TRADE_GATE = 50
MOMENTUM_THRESHOLD = 0.50
VALID_AGENTS = {"analyst", "engineer", "manager"}


def resolve_yolo_repo() -> Path:
    """Resolve the yolo repo path from env var or relative fallback."""
    env_path = os.environ.get("YOLO_REPO_PATH")
    if env_path:
        return Path(env_path)
    return AGENTS_DIR.parent.parent / "yolo"


def _ensure_yolo_on_path(yolo_repo: Path) -> None:
    """Add yolo repo to sys.path if not already present."""
    repo_str = str(yolo_repo)
    if repo_str not in sys.path:
        sys.path.insert(0, repo_str)


def _build_strategy(config: dict) -> object:
    """Build a Strategy object from config dict."""
    from analysis.backtester.strategy import Strategy

    strategy_dict = {
        "name": config.get("strategy_id", "unnamed"),
        "entry_rules": config["entry_rules"],
        "exit_rules": config["exit_rules"],
        "skip_first_entry": config.get("skip_first", False),
        "force_close_eod": config.get("force_close_eod", True),
    }
    if config.get("atr_exit"):
        strategy_dict["atr_exit"] = config["atr_exit"]
    if config.get("volume_decay_exit"):
        strategy_dict["volume_decay_exit"] = config["volume_decay_exit"]

    return Strategy.from_dict(strategy_dict)


def _load_cached_bars(ticker: str, date_str: str, yolo_repo: Path) -> list:
    """Load 1-min bars from day_sim cache. Raises FileNotFoundError if missing."""
    import json

    from src.models.polygon import Bar

    cache_path = yolo_repo / "analysis" / "cache" / "day_sim" / f"{ticker}_{date_str}_1min.json"
    if not cache_path.exists():
        raise FileNotFoundError(
            f"Cache miss: {ticker}_{date_str} not found. "
            f"Check date is within available cached range."
        )

    data = json.loads(cache_path.read_text(encoding="utf-8"))
    return [Bar.model_validate(r) for r in data]


def _discover_pairs_from_cache(
    yolo_repo: Path, dates: list[str],
) -> list[tuple[str, str]]:
    """Scan day_sim cache for all ticker-date pairs matching requested dates.

    Returns:
        List of (ticker, date) tuples found in cache.
    """
    cache_dir = yolo_repo / "analysis" / "cache" / "day_sim"
    if not cache_dir.is_dir():
        return []

    date_set = set(dates)
    pairs: list[tuple[str, str]] = []
    for f in cache_dir.iterdir():
        if not f.name.endswith("_1min.json"):
            continue
        # Format: {TICKER}_{YYYY-MM-DD}_1min.json
        parts = f.stem.rsplit("_", 2)  # [ticker, date, "1min"]
        if len(parts) != 3:
            continue
        ticker, date_str = parts[0], parts[1]
        if date_str in date_set:
            pairs.append((ticker, date_str))

    return sorted(pairs)


def _passes_momentum_filter(bars: list) -> bool:
    """Check if bars show >= 50% intraday price range.

    Args:
        bars: List of bar dicts with 'h' (high) and 'l' (low) keys.

    Returns:
        True if (day_high - day_low) / day_low >= 0.50.
    """
    if not bars:
        return False
    day_high = max(b["h"] for b in bars)
    day_low = min(b["l"] for b in bars)
    if day_low == 0:
        return False
    return (day_high - day_low) / day_low >= MOMENTUM_THRESHOLD


def _run_single_backtest(
    ticker: str, date_str: str, strategy: object, yolo_repo: Path,
) -> tuple:
    """Run backtest for one ticker/date. Returns (BacktestResult, summary_dict)."""
    from analysis.backtester import reports
    from analysis.backtester.engine import BacktestEngine

    bars = _load_cached_bars(ticker, date_str, yolo_repo)
    if len(bars) < 20:
        raise ValueError(f"Too few bars for {ticker} on {date_str}: {len(bars)}")

    engine = BacktestEngine(bars, strategy, ticker=ticker, date=date_str)
    result = engine.run()
    summary = reports.summarise(result)
    return result, summary


def _write_trades_csv(all_trades: list[dict], results_dir: Path, strategy_id: str) -> Path:
    """Write aggregated trades to a timestamped CSV."""
    results_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    path = results_dir / f"{strategy_id}-{ts}.csv"

    fieldnames = [
        "date", "ticker", "entry_price", "exit_price",
        "pnl_pct", "hold_bars", "exit_type", "signal_num",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for t in all_trades:
            writer.writerow({k: str(t.get(k, "")) for k in fieldnames})

    return path


def update_memory(
    agent: str,
    content: str,
    agents_dir: Path | None = None,
    calling_agent: str | None = None,
) -> dict:
    """Write content to an agent's memory file.

    Args:
        agent: Target agent name (analyst, engineer, manager).
        content: Full markdown content to write to memory.md.
        agents_dir: Override agents directory (for testing).
        calling_agent: Identity of the agent making the call (for enforcement).

    Returns:
        Dict with ok=True/False and path or error message.
    """
    if agent not in VALID_AGENTS:
        return {"ok": False, "error": f"Invalid agent: {agent}. Must be one of {sorted(VALID_AGENTS)}"}

    if calling_agent is not None and calling_agent != agent:
        return {"ok": False, "error": f"Identity mismatch: {calling_agent} cannot write {agent}'s memory"}

    base = agents_dir if agents_dir is not None else AGENTS_DIR
    memory_path = base / agent / "memory.md"

    try:
        memory_path.write_text(content, encoding="utf-8")
    except OSError as e:
        logger.exception("Failed to write memory for %s", agent)
        return {"ok": False, "error": f"Write failed: {e}"}

    return {"ok": True, "path": str(memory_path)}


def run_backtest(config: dict, yolo_repo: Path | None = None) -> dict:
    """Execute a backtest using the yolo backtesting engine.

    Args:
        config: Strategy configuration dict with keys:
            strategy_id, tickers, dates, entry_rules, exit_rules,
            skip_first, atr_exit, force_close_eod
        yolo_repo: Override yolo repo path (for testing).

    Returns:
        Dict with: strategy_id, trade_count, inconclusive, win_rate,
        total_pnl_pct, avg_hold_bars, summary, results_path
    """
    if yolo_repo is None:
        yolo_repo = resolve_yolo_repo()

    _ensure_yolo_on_path(yolo_repo)

    # Validate required fields
    required = ["strategy_id", "tickers", "dates", "entry_rules", "exit_rules"]
    missing = [k for k in required if k not in config]
    if missing:
        return {
            "error": f"Missing required config fields: {missing}",
            "inconclusive": True,
            "trade_count": 0,
            "strategy_id": config.get("strategy_id", "unknown"),
        }

    strategy_id = config["strategy_id"]

    try:
        strategy = _build_strategy(config)
    except Exception as e:
        logger.exception("Failed to build strategy")
        return {
            "error": f"Invalid strategy config: {e}",
            "inconclusive": True,
            "trade_count": 0,
            "strategy_id": strategy_id,
        }

    tickers = config["tickers"]
    dates = config["dates"]
    momentum_universe = config.get("momentum_universe", False)

    # Build ticker-date pairs
    if tickers == "all":
        ticker_date_pairs = _discover_pairs_from_cache(yolo_repo, dates)
    else:
        ticker_date_pairs = [
            (ticker, date_str) for date_str in dates for ticker in tickers
        ]

    all_trades: list[dict] = []
    total_pnl = Decimal("0")
    wins = 0
    total_closed = 0
    total_hold = 0
    errors: list[str] = []
    pairs_evaluated = 0
    pairs_skipped_momentum = 0
    pairs_skipped_other = 0

    for ticker, date_str in ticker_date_pairs:
        try:
            if momentum_universe:
                bars_raw = _load_cached_bars(ticker, date_str, yolo_repo)
                bar_dicts = [{"h": float(b.high), "l": float(b.low)} for b in bars_raw]
                if not _passes_momentum_filter(bar_dicts):
                    pairs_skipped_momentum += 1
                    continue

            result, summary = _run_single_backtest(
                ticker, date_str, strategy, yolo_repo,
            )
            pairs_evaluated += 1
            n = summary["n_closed"]
            total_closed += n
            if n > 0:
                wins += int(summary["win_rate"] * n)
                total_pnl += Decimal(str(summary["total_pnl_pct"]))
                total_hold += summary["avg_hold_bars"] * n

            for t in result.trades:
                all_trades.append({
                    "date": date_str,
                    "ticker": ticker,
                    "entry_price": str(t.entry_price),
                    "exit_price": str(t.exit_price) if t.exit_price else "",
                    "pnl_pct": str(t.pnl_pct) if t.pnl_pct else "",
                    "hold_bars": str(t.hold_bars) if t.hold_bars else "",
                    "exit_type": t.exit_type or "",
                    "signal_num": str(t.signal_num) if t.signal_num else "",
                })
        except (FileNotFoundError, ValueError) as e:
            pairs_skipped_other += 1
            errors.append(f"{ticker}/{date_str}: {e}")
        except Exception as e:
            pairs_skipped_other += 1
            logger.exception("Backtest error for %s/%s", ticker, date_str)
            errors.append(f"{ticker}/{date_str}: {e}")

    if total_closed == 0 and errors:
        return {
            "error": "; ".join(errors[:5]),
            "inconclusive": True,
            "trade_count": 0,
            "strategy_id": strategy_id,
        }

    # Write CSV
    results_dir = yolo_repo / "analysis" / "research" / "results"
    csv_path = _write_trades_csv(all_trades, results_dir, strategy_id)

    trade_count = len(all_trades)
    inconclusive = trade_count < MIN_TRADE_GATE
    win_rate = wins / total_closed if total_closed > 0 else 0.0
    avg_hold = total_hold / total_closed if total_closed > 0 else 0.0

    summary_parts = [f"{trade_count} trades"]
    if inconclusive:
        summary_parts.append(f"(< {MIN_TRADE_GATE} minimum gate, inconclusive)")
    summary_parts.append(f"Win rate: {win_rate:.1%}")
    summary_parts.append(f"Total PnL: {total_pnl:.2f}%")
    summary_parts.append(f"Avg hold: {avg_hold:.1f} bars")
    if errors:
        summary_parts.append(f"Errors: {len(errors)} ticker/dates skipped")
    summary_text = ". ".join(summary_parts)

    return {
        "strategy_id": strategy_id,
        "trade_count": trade_count,
        "inconclusive": inconclusive,
        "win_rate": round(win_rate, 4),
        "total_pnl_pct": float(total_pnl),
        "avg_hold_bars": round(avg_hold, 1),
        "summary": summary_text,
        "results_path": str(csv_path),
        "momentum_universe_enabled": momentum_universe,
        "pairs_evaluated": pairs_evaluated,
        "pairs_skipped_momentum": pairs_skipped_momentum,
        "pairs_skipped_other": pairs_skipped_other,
    }
