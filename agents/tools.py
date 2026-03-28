"""Engineer execution tools for YOLO Org Learning.

Provides run_backtest() — executes backtests using the yolo backtesting engine
against cached market data. Cache-only mode: no live Polygon API calls.

Data access is delegated to analysis.datastore.DataStore — no hardcoded paths
leak into this module.
"""

from __future__ import annotations

import csv
import logging
import os
import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

logger = logging.getLogger(__name__)

AGENTS_DIR = Path(__file__).parent
MIN_TRADE_GATE = 50
MOMENTUM_THRESHOLD = 0.50
VALID_AGENTS = {"optimist", "challenger", "manager", "statistician", "execution-realist", "scout"}


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


def _create_datastore(yolo_repo: Path) -> object:
    """Create a DataStore instance. Thin wrapper to allow test mocking."""
    from analysis.datastore import DataStore

    return DataStore(yolo_repo)


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
    if config.get("news_trigger"):
        strategy_dict["news_trigger"] = config["news_trigger"]
    if config.get("use_news"):
        strategy_dict["use_news"] = True

    return Strategy.from_dict(strategy_dict)



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


def _load_news_for_backtest(ticker: str, date_str: str, ds: object) -> list:
    """Load news articles for a ticker covering the backtest date + 1-day lookback."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    date_from = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
    # Combine articles from both dates, deduplicate by benzinga_id
    seen: set[int] = set()
    articles: list = []
    for d in (date_from, date_str):
        for a in ds.get_news(ticker, d):
            if a.benzinga_id not in seen:
                seen.add(a.benzinga_id)
                articles.append(a)
    articles.sort(key=lambda a: a.published_ms)
    return articles


def _run_single_backtest(
    ticker: str, date_str: str, strategy: object, ds: object,
) -> tuple:
    """Run backtest for one ticker/date. Returns (BacktestResult, summary_dict)."""
    from analysis.backtester import reports
    from analysis.backtester.engine import BacktestEngine

    bars = ds.get_1min_bars(ticker, date_str)
    if len(bars) < 20:
        raise ValueError(f"Too few bars for {ticker} on {date_str}: {len(bars)}")

    news = None
    if getattr(strategy, "use_news", False):
        news = _load_news_for_backtest(ticker, date_str, ds)

    engine = BacktestEngine(bars, strategy, ticker=ticker, date=date_str, news=news)
    result = engine.run()
    summary = reports.summarise(result)
    return result, summary


def _compute_distribution_metrics(all_trades: list[dict]) -> dict:
    """Compute per-trade distribution metrics from aggregated trade dicts.

    Returns dict with: avg_winner_pct, avg_loser_pct, median_pnl_pct,
    max_single_trade_pnl_pct, top10_pnl_contribution_pct.
    All values are None if no trades.
    """
    pnls = []
    for t in all_trades:
        raw = t.get("pnl_pct", "")
        if raw:
            pnls.append(float(raw))

    if not pnls:
        return {
            "avg_winner_pct": None,
            "avg_loser_pct": None,
            "median_pnl_pct": None,
            "max_single_trade_pnl_pct": None,
            "top10_pnl_contribution_pct": None,
        }

    winners = [p for p in pnls if p > 0]
    losers = [p for p in pnls if p <= 0]
    sorted_pnls = sorted(pnls)
    n = len(sorted_pnls)
    median = (sorted_pnls[n // 2] if n % 2 == 1
              else (sorted_pnls[n // 2 - 1] + sorted_pnls[n // 2]) / 2)

    total_abs_pnl = sum(abs(p) for p in pnls)
    top10 = sorted(pnls, key=abs, reverse=True)[:10]
    top10_contribution = (
        sum(abs(p) for p in top10) / total_abs_pnl * 100
        if total_abs_pnl > 0 else 0.0
    )

    return {
        "avg_winner_pct": round(sum(winners) / len(winners), 4) if winners else 0.0,
        "avg_loser_pct": round(sum(losers) / len(losers), 4) if losers else 0.0,
        "median_pnl_pct": round(median, 4),
        "max_single_trade_pnl_pct": round(max(pnls), 4),
        "top10_pnl_contribution_pct": round(top10_contribution, 2),
    }


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


BACKUP_RETENTION_DAYS = 30


def _create_backup(memory_path: Path) -> Path | None:
    """Create a timestamped backup of memory_path in memory-history/.

    Returns the backup path, or None if no file to back up.
    """
    if not memory_path.exists():
        return None

    history_dir = memory_path.parent / "memory-history"
    history_dir.mkdir(exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    backup_path = history_dir / f"{timestamp}.md"
    backup_path.write_text(memory_path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_path


def _rotate_backups(history_dir: Path) -> None:
    """Delete backups older than BACKUP_RETENTION_DAYS."""
    if not history_dir.exists():
        return

    cutoff = datetime.now(UTC) - timedelta(days=BACKUP_RETENTION_DAYS)
    cutoff_ts = cutoff.timestamp()

    for backup in history_dir.glob("*.md"):
        if backup.stat().st_mtime < cutoff_ts:
            backup.unlink()


def update_memory(
    agent: str,
    content: str,
    agents_dir: Path | None = None,
    calling_agent: str | None = None,
) -> dict:
    """Write content to an agent's memory file with backup and rotation.

    Creates a timestamped backup before overwriting. Rotates backups
    older than 30 days after a successful write.

    Args:
        agent: Target agent name (optimist, challenger, manager).
        content: Full markdown content to write to memory.md.
        agents_dir: Override agents directory (for testing).
        calling_agent: Identity of the agent making the call (for enforcement).

    Returns:
        Dict with ok, path, backup_path, and error.
    """
    if agent not in VALID_AGENTS:
        return {
            "ok": False,
            "path": None,
            "backup_path": None,
            "error": f"Invalid agent: {agent}. Must be one of {sorted(VALID_AGENTS)}",
        }

    if calling_agent is not None and calling_agent != agent:
        return {
            "ok": False,
            "path": None,
            "backup_path": None,
            "error": f"Identity mismatch: {calling_agent} cannot write {agent}'s memory",
        }

    base = agents_dir if agents_dir is not None else AGENTS_DIR
    memory_path = base / agent / "memory.md"

    # Create backup before writing
    try:
        backup_path = _create_backup(memory_path)
    except OSError as e:
        logger.exception("Failed to create backup for %s", agent)
        return {
            "ok": False,
            "path": str(memory_path),
            "backup_path": None,
            "error": f"Backup failed: {e}",
        }

    # Write new content
    try:
        memory_path.write_text(content, encoding="utf-8")
    except OSError as e:
        logger.exception("Failed to write memory for %s", agent)
        return {
            "ok": False,
            "path": str(memory_path),
            "backup_path": None,
            "error": f"Write failed: {e}",
        }

    # Rotate old backups (only after successful write)
    history_dir = memory_path.parent / "memory-history"
    try:
        _rotate_backups(history_dir)
    except OSError:
        logger.warning("Backup rotation failed for %s — non-fatal", agent)

    return {
        "ok": True,
        "path": str(memory_path),
        "backup_path": str(backup_path) if backup_path else None,
        "error": None,
    }


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

    ds = _create_datastore(yolo_repo)

    # Validate required fields (dates is optional — defaults to "all")
    required = ["strategy_id", "tickers", "entry_rules", "exit_rules"]
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
    dates = config.get("dates")
    momentum_universe = config.get("momentum_universe", False)

    # Normalise dates — "all", [], None, ["all"] all mean "use all cached dates"
    all_dates = (
        dates is None
        or dates == "all"
        or dates == ["all"]
        or (isinstance(dates, list) and len(dates) == 0)
    )

    # Build ticker-date pairs via DataStore
    if tickers == "all" or tickers == ["all"]:
        ticker_date_pairs = ds.list_ticker_date_pairs(
            dates=None if all_dates else dates,
        )
    elif all_dates:
        ticker_date_pairs = ds.list_ticker_date_pairs(dates=None)
        ticker_set = set(tickers)
        ticker_date_pairs = [(t, d) for t, d in ticker_date_pairs if t in ticker_set]
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
                bars_raw = ds.get_1min_bars(ticker, date_str)
                bar_dicts = [{"h": float(b.high), "l": float(b.low)} for b in bars_raw]
                if not _passes_momentum_filter(bar_dicts):
                    pairs_skipped_momentum += 1
                    continue

            result, summary = _run_single_backtest(
                ticker, date_str, strategy, ds,
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
    csv_path = _write_trades_csv(all_trades, ds.results_dir, strategy_id)

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

    distribution = _compute_distribution_metrics(all_trades)

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
        **distribution,
    }
