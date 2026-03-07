"""Unit tests for agents/tools.py — backtest execution and memory tools."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add agents/ to path so we can import tools
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from tools import (
    _compute_distribution_metrics,
    _discover_pairs_from_cache,
    _passes_momentum_filter,
    resolve_yolo_repo,
    run_backtest,
    update_memory,
)


def _make_mock_result(n_trades: int = 5, pnl: float = 0.12) -> MagicMock:
    """Create a mock BacktestResult with n trades."""
    result = MagicMock()
    trades = []
    for i in range(n_trades):
        t = MagicMock()
        t.entry_index = i * 10
        t.exit_index = i * 10 + 5
        t.entry_price = 1.50
        t.exit_price = 1.55
        t.pnl_pct = pnl / n_trades if n_trades else 0
        t.hold_bars = 5
        t.exit_type = "ema"
        t.signal_num = i + 1
        t.entry_time = 1000000 + i * 60000
        t.entry_indicators = {}
        t.exit_indicators = {}
        trades.append(t)
    result.trades = trades
    return result


def _make_summary(n_trades: int = 5, win_rate: float = 0.45, pnl: float = 0.12) -> dict:
    """Create a mock reports.summarise() return value."""
    return {
        "ticker": "MOBX",
        "date": "2026-03-03",
        "strategy_name": "test",
        "n_trades": n_trades,
        "n_closed": n_trades,
        "n_open": 0,
        "win_rate": win_rate,
        "total_pnl_pct": pnl,
        "max_single_loss_pct": -0.02,
        "avg_hold_bars": 5,
        "n_missed": 0,
    }


VALID_CONFIG = {
    "strategy_id": "HYP-TEST",
    "tickers": ["MOBX"],
    "dates": ["2026-03-03"],
    "entry_rules": [
        {"indicator": "ema_gap", "operator": "crosses_above", "value": "3.0",
         "params": {"fast": 3, "slow": 9}},
    ],
    "exit_rules": [
        {"indicator": "ema_gap", "operator": "crosses_below", "value": "1.5",
         "params": {"fast": 3, "slow": 9}},
    ],
    "skip_first": True,
    "atr_exit": {"multiplier": "2.0", "period": 14},
    "force_close_eod": True,
}


class TestRunBacktestSchema:
    """Tests for run_backtest return schema."""

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_returns_correct_schema(
        self, mock_strat: MagicMock, mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_run.return_value = (
            _make_mock_result(60), _make_summary(60, 0.50, 0.25),
        )
        config = {**VALID_CONFIG, "tickers": ["MOBX"] * 3, "dates": ["2026-03-03"] * 20}

        result = run_backtest(config, yolo_repo=tmp_path)

        assert "trade_count" in result
        assert "inconclusive" in result
        assert "summary" in result
        assert "results_path" in result
        assert "strategy_id" in result
        assert "win_rate" in result

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_inconclusive_when_under_50_trades(
        self, mock_strat: MagicMock, mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_run.return_value = (
            _make_mock_result(10), _make_summary(10, 0.40, 0.05),
        )

        result = run_backtest(VALID_CONFIG, yolo_repo=tmp_path)

        assert result["inconclusive"] is True
        assert result["trade_count"] < 50

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_not_inconclusive_when_over_50_trades(
        self, mock_strat: MagicMock, mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_run.return_value = (
            _make_mock_result(60), _make_summary(60, 0.50, 0.25),
        )
        config = {**VALID_CONFIG, "tickers": ["MOBX"], "dates": ["2026-03-03"]}

        result = run_backtest(config, yolo_repo=tmp_path)

        assert result["inconclusive"] is False
        assert result["trade_count"] >= 50


class TestRunBacktestCSV:
    """Tests for results CSV output."""

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_results_csv_written(
        self, mock_strat: MagicMock, mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_run.return_value = (
            _make_mock_result(5), _make_summary(5),
        )

        result = run_backtest(VALID_CONFIG, yolo_repo=tmp_path)

        assert result["results_path"] is not None
        csv_path = Path(result["results_path"])
        assert csv_path.exists()
        assert csv_path.suffix == ".csv"


class TestRunBacktestErrors:
    """Tests for error handling."""

    def test_bad_config_returns_error(self, tmp_path: Path) -> None:
        bad_config = {"strategy_id": "test"}  # Missing required fields

        result = run_backtest(bad_config, yolo_repo=tmp_path)

        assert "error" in result
        assert result["inconclusive"] is True

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_missing_cache_returns_error_in_summary(
        self, mock_strat: MagicMock, mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_run.side_effect = FileNotFoundError("No cached data")

        result = run_backtest(VALID_CONFIG, yolo_repo=tmp_path)

        assert "error" in result
        assert result["inconclusive"] is True


class TestResolveYoloRepo:
    """Tests for YOLO repo path resolution."""

    def test_env_var_takes_precedence(self, tmp_path: Path) -> None:
        with patch.dict("os.environ", {"YOLO_REPO_PATH": str(tmp_path)}):
            assert resolve_yolo_repo() == tmp_path

    def test_fallback_to_relative_path(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            result = resolve_yolo_repo()
            assert result.name == "yolo"


class TestUpdateMemory:
    """Tests for update_memory tool."""

    def test_writes_file(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        (agents_dir / "analyst").mkdir(parents=True)

        result = update_memory("analyst", "# New memory\n- fact 1", agents_dir=agents_dir)

        assert result["ok"] is True
        written = (agents_dir / "analyst" / "memory.md").read_text()
        assert "# New memory" in written
        assert "fact 1" in written

    def test_agent_identity_enforced(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        (agents_dir / "analyst").mkdir(parents=True)

        result = update_memory(
            "analyst", "content", agents_dir=agents_dir, calling_agent="manager",
        )

        assert result["ok"] is False
        assert "mismatch" in result["error"].lower()

    def test_error_on_invalid_agent(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir(parents=True)

        result = update_memory("hacker", "content", agents_dir=agents_dir)

        assert result["ok"] is False


# --- Helpers for momentum filter tests ---

def _bar(high: float, low: float) -> dict:
    """Create a minimal bar dict with high and low prices (for filter helper)."""
    return {"h": high, "l": low}


def _mock_bar_obj(high: float, low: float) -> MagicMock:
    """Create a mock Bar object with high/low attributes (for _load_cached_bars mock)."""
    b = MagicMock()
    b.high = high
    b.low = low
    return b


class TestMomentumFilter:
    """Tests for _passes_momentum_filter helper."""

    def test_excludes_low_range_pairs(self) -> None:
        """Pair with <50% range is excluded."""
        # 49% range: (1.49 - 1.0) / 1.0 = 0.49
        bars = [_bar(1.2, 1.0), _bar(1.49, 1.1), _bar(1.3, 1.05)]
        assert _passes_momentum_filter(bars) is False

    def test_includes_high_range_pairs(self) -> None:
        """Pair with >=50% range passes."""
        # 100% range: (2.0 - 1.0) / 1.0 = 1.0
        bars = [_bar(2.0, 1.0), _bar(1.5, 1.2)]
        assert _passes_momentum_filter(bars) is True

    def test_threshold_boundary_passes(self) -> None:
        """Exactly 50.0% range passes."""
        # (1.50 - 1.00) / 1.00 = 0.50 exactly
        bars = [_bar(1.50, 1.00)]
        assert _passes_momentum_filter(bars) is True

    def test_threshold_boundary_fails(self) -> None:
        """49.9% range does not pass."""
        # (1.499 - 1.00) / 1.00 = 0.499
        bars = [_bar(1.499, 1.00)]
        assert _passes_momentum_filter(bars) is False

    def test_zero_low_returns_false(self) -> None:
        """Guard: day_low == 0 returns False (no division by zero)."""
        bars = [_bar(5.0, 0.0)]
        assert _passes_momentum_filter(bars) is False

    def test_empty_bars_returns_false(self) -> None:
        """Empty bar list returns False."""
        assert _passes_momentum_filter([]) is False


class TestMomentumUniverse:
    """Integration tests for momentum_universe in run_backtest."""

    @patch("tools._run_single_backtest")
    @patch("tools._load_cached_bars")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_momentum_filter_excludes_low_range(
        self, mock_strat: MagicMock, mock_load: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Pair with <50% range is skipped when momentum_universe=true."""
        # 20% range — should be filtered out
        mock_load.return_value = [_mock_bar_obj(1.2, 1.0)] * 25
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "momentum_universe": True}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_run.assert_not_called()
        assert result["pairs_skipped_momentum"] == 1
        assert result["pairs_evaluated"] == 0

    @patch("tools._run_single_backtest")
    @patch("tools._load_cached_bars")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_momentum_filter_includes_high_range(
        self, mock_strat: MagicMock, mock_load: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Pair with >=50% range passes filter and is evaluated."""
        # 100% range — should pass
        mock_load.return_value = [_mock_bar_obj(2.0, 1.0)] * 25
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "momentum_universe": True}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_run.assert_called_once()
        assert result["pairs_evaluated"] == 1
        assert result["pairs_skipped_momentum"] == 0

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_momentum_filter_disabled_by_default(
        self, mock_strat: MagicMock, mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """momentum_universe=false processes all pairs as before."""
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))

        result = run_backtest(VALID_CONFIG, yolo_repo=tmp_path)

        mock_run.assert_called_once()
        assert result["momentum_universe_enabled"] is False

    @patch("tools._run_single_backtest")
    @patch("tools._load_cached_bars")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_momentum_filter_uses_full_extended_day(
        self, mock_strat: MagicMock, mock_load: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Filter uses all bars (pre-market + RTH + after-hours), not RTH only.

        Pre-market bar has the low, after-hours bar has the high.
        Combined range >= 50%, but no single bar spans that range.
        """
        bars = [
            _mock_bar_obj(1.1, 1.0),   # pre-market: low of day
            _mock_bar_obj(1.3, 1.2),   # RTH: mid range
            _mock_bar_obj(1.55, 1.4),  # after-hours: high of day
        ]
        # range = (1.55 - 1.0) / 1.0 = 0.55 >= 0.50
        mock_load.return_value = bars
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "momentum_universe": True}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_run.assert_called_once()
        assert result["pairs_evaluated"] == 1

    @patch("tools._run_single_backtest")
    @patch("tools._load_cached_bars")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_results_include_momentum_skip_count(
        self, mock_strat: MagicMock, mock_load: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Return dict contains all momentum-related fields."""
        mock_load.return_value = [_mock_bar_obj(1.1, 1.0)] * 25  # <50% range
        config = {
            **VALID_CONFIG,
            "tickers": ["MOBX", "NPT"],
            "dates": ["2026-03-03"],
            "momentum_universe": True,
        }

        result = run_backtest(config, yolo_repo=tmp_path)

        assert "momentum_universe_enabled" in result
        assert result["momentum_universe_enabled"] is True
        assert "pairs_evaluated" in result
        assert "pairs_skipped_momentum" in result
        assert result["pairs_skipped_momentum"] == 2
        assert "pairs_skipped_other" in result


class TestDiscoverPairsFromCache:
    """Tests for _discover_pairs_from_cache — tickers='all' support."""

    def test_discovers_ticker_date_pairs(self, tmp_path: Path) -> None:
        """Finds all ticker-date pairs from cache filenames."""
        cache_dir = tmp_path / "analysis" / "cache" / "day_sim"
        cache_dir.mkdir(parents=True)
        (cache_dir / "MOBX_2026-03-03_1min.json").write_text("[]")
        (cache_dir / "NPT_2026-03-03_1min.json").write_text("[]")
        (cache_dir / "MOBX_2026-03-04_1min.json").write_text("[]")

        pairs = _discover_pairs_from_cache(tmp_path, dates=["2026-03-03", "2026-03-04"])

        assert ("MOBX", "2026-03-03") in pairs
        assert ("NPT", "2026-03-03") in pairs
        assert ("MOBX", "2026-03-04") in pairs
        assert len(pairs) == 3

    def test_filters_by_dates(self, tmp_path: Path) -> None:
        """Only returns pairs for requested dates."""
        cache_dir = tmp_path / "analysis" / "cache" / "day_sim"
        cache_dir.mkdir(parents=True)
        (cache_dir / "MOBX_2026-03-03_1min.json").write_text("[]")
        (cache_dir / "MOBX_2026-03-04_1min.json").write_text("[]")

        pairs = _discover_pairs_from_cache(tmp_path, dates=["2026-03-03"])

        assert len(pairs) == 1
        assert ("MOBX", "2026-03-03") in pairs

    def test_empty_cache_returns_empty(self, tmp_path: Path) -> None:
        """Returns empty list if no matching files."""
        cache_dir = tmp_path / "analysis" / "cache" / "day_sim"
        cache_dir.mkdir(parents=True)

        pairs = _discover_pairs_from_cache(tmp_path, dates=["2026-03-03"])

        assert pairs == []

    def test_ignores_non_1min_files(self, tmp_path: Path) -> None:
        """Only matches _1min.json files."""
        cache_dir = tmp_path / "analysis" / "cache" / "day_sim"
        cache_dir.mkdir(parents=True)
        (cache_dir / "MOBX_2026-03-03_1min.json").write_text("[]")
        (cache_dir / "MOBX_2026-03-03_5min.json").write_text("[]")

        pairs = _discover_pairs_from_cache(tmp_path, dates=["2026-03-03"])

        assert len(pairs) == 1


class TestTickersAll:
    """Integration tests for tickers='all' in run_backtest."""

    @patch("tools._run_single_backtest")
    @patch("tools._discover_pairs_from_cache")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_tickers_all_uses_cache_discovery(
        self, mock_strat: MagicMock, mock_discover: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """tickers='all' discovers pairs from cache instead of explicit list."""
        mock_discover.return_value = [("MOBX", "2026-03-03"), ("NPT", "2026-03-03")]
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {
            **VALID_CONFIG,
            "tickers": "all",
            "dates": ["2026-03-03"],
        }

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_discover.assert_called_once()
        assert mock_run.call_count == 2
        assert result["pairs_evaluated"] == 2

    @patch("tools._run_single_backtest")
    @patch("tools._discover_pairs_from_cache")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_tickers_all_as_list_element(
        self, mock_strat: MagicMock, mock_discover: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """tickers=["all"] (list) also triggers cache discovery."""
        mock_discover.return_value = [("MOBX", "2026-03-03")]
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {
            **VALID_CONFIG,
            "tickers": ["all"],
            "dates": ["2026-03-03"],
        }

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_discover.assert_called_once()
        assert result["pairs_evaluated"] == 1


class TestDistributionMetrics:
    """Tests for _compute_distribution_metrics helper."""

    def test_normal_case(self) -> None:
        """Mixed winners and losers produce correct metrics."""
        trades = [
            {"pnl_pct": "5.0"},
            {"pnl_pct": "10.0"},
            {"pnl_pct": "-3.0"},
            {"pnl_pct": "-7.0"},
            {"pnl_pct": "2.0"},
        ]
        m = _compute_distribution_metrics(trades)

        assert m["avg_winner_pct"] == round((5.0 + 10.0 + 2.0) / 3, 4)
        assert m["avg_loser_pct"] == round((-3.0 + -7.0) / 2, 4)
        assert m["median_pnl_pct"] == 2.0
        assert m["max_single_trade_pnl_pct"] == 10.0
        assert m["top10_pnl_contribution_pct"] == 100.0  # only 5 trades

    def test_zero_trades(self) -> None:
        """Empty trade list returns all None."""
        m = _compute_distribution_metrics([])

        assert m["avg_winner_pct"] is None
        assert m["avg_loser_pct"] is None
        assert m["median_pnl_pct"] is None
        assert m["max_single_trade_pnl_pct"] is None
        assert m["top10_pnl_contribution_pct"] is None

    def test_single_trade(self) -> None:
        """Single trade returns itself as all metrics."""
        m = _compute_distribution_metrics([{"pnl_pct": "3.5"}])

        assert m["avg_winner_pct"] == 3.5
        assert m["avg_loser_pct"] == 0.0
        assert m["median_pnl_pct"] == 3.5
        assert m["max_single_trade_pnl_pct"] == 3.5
        assert m["top10_pnl_contribution_pct"] == 100.0

    def test_all_winners(self) -> None:
        """All positive trades — avg_loser_pct is 0.0."""
        trades = [{"pnl_pct": "2.0"}, {"pnl_pct": "4.0"}, {"pnl_pct": "6.0"}]
        m = _compute_distribution_metrics(trades)

        assert m["avg_winner_pct"] == 4.0
        assert m["avg_loser_pct"] == 0.0
        assert m["max_single_trade_pnl_pct"] == 6.0

    def test_all_losers(self) -> None:
        """All negative trades — avg_winner_pct is 0.0."""
        trades = [{"pnl_pct": "-1.0"}, {"pnl_pct": "-3.0"}, {"pnl_pct": "-5.0"}]
        m = _compute_distribution_metrics(trades)

        assert m["avg_winner_pct"] == 0.0
        assert m["avg_loser_pct"] == -3.0
        assert m["max_single_trade_pnl_pct"] == -1.0

    def test_top10_contribution_with_many_trades(self) -> None:
        """Top 10 contribution < 100% when there are more than 10 trades."""
        # 10 small trades + 1 big trade
        trades = [{"pnl_pct": "1.0"} for _ in range(10)]
        trades.append({"pnl_pct": "90.0"})
        m = _compute_distribution_metrics(trades)

        # total abs = 10 * 1.0 + 90.0 = 100.0
        # top 10 abs = 90.0 + 9 * 1.0 = 99.0
        assert m["top10_pnl_contribution_pct"] == 99.0

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_distribution_in_run_backtest_output(
        self, mock_strat: MagicMock, mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """run_backtest return dict includes all distribution fields."""
        mock_run.return_value = (
            _make_mock_result(5), _make_summary(5, 0.60, 0.12),
        )

        result = run_backtest(VALID_CONFIG, yolo_repo=tmp_path)

        assert "avg_winner_pct" in result
        assert "avg_loser_pct" in result
        assert "median_pnl_pct" in result
        assert "max_single_trade_pnl_pct" in result
        assert "top10_pnl_contribution_pct" in result

    def test_trades_with_empty_pnl_skipped(self) -> None:
        """Trades with empty pnl_pct are ignored."""
        trades = [{"pnl_pct": "5.0"}, {"pnl_pct": ""}, {"pnl_pct": "3.0"}]
        m = _compute_distribution_metrics(trades)

        assert m["avg_winner_pct"] == 4.0
        assert m["median_pnl_pct"] == 4.0


class TestDatesAll:
    """Tests for dates='all' support in run_backtest."""

    @patch("tools._run_single_backtest")
    @patch("tools._discover_pairs_from_cache")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_dates_all_string(
        self, mock_strat: MagicMock, mock_discover: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates='all' discovers all dates from cache."""
        mock_discover.return_value = [("MOBX", "2026-03-03"), ("MOBX", "2026-03-04")]
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "dates": "all"}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_discover.assert_called_once_with(tmp_path, dates=None)
        assert result["pairs_evaluated"] == 2

    @patch("tools._run_single_backtest")
    @patch("tools._discover_pairs_from_cache")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_dates_empty_list(
        self, mock_strat: MagicMock, mock_discover: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates=[] discovers all dates from cache."""
        mock_discover.return_value = [("MOBX", "2026-03-03")]
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "dates": []}

        run_backtest(config, yolo_repo=tmp_path)

        mock_discover.assert_called_once_with(tmp_path, dates=None)

    @patch("tools._run_single_backtest")
    @patch("tools._discover_pairs_from_cache")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_dates_none(
        self, mock_strat: MagicMock, mock_discover: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates=None discovers all dates from cache."""
        mock_discover.return_value = [("MOBX", "2026-03-03")]
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {k: v for k, v in VALID_CONFIG.items() if k != "dates"}

        run_backtest(config, yolo_repo=tmp_path)

        mock_discover.assert_called_once_with(tmp_path, dates=None)

    @patch("tools._run_single_backtest")
    @patch("tools._discover_pairs_from_cache")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_dates_list_with_all(
        self, mock_strat: MagicMock, mock_discover: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates=['all'] discovers all dates from cache."""
        mock_discover.return_value = [("MOBX", "2026-03-03")]
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "dates": ["all"]}

        run_backtest(config, yolo_repo=tmp_path)

        mock_discover.assert_called_once_with(tmp_path, dates=None)

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_explicit_dates_unchanged(
        self, mock_strat: MagicMock, mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Explicit date list still works as before (regression)."""
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))

        result = run_backtest(VALID_CONFIG, yolo_repo=tmp_path)

        mock_run.assert_called_once()
        assert result["pairs_evaluated"] == 1

    @patch("tools._run_single_backtest")
    @patch("tools._discover_pairs_from_cache")
    @patch("tools._build_strategy", return_value=MagicMock())
    def test_dates_all_with_explicit_tickers_filters(
        self, mock_strat: MagicMock, mock_discover: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates='all' + explicit tickers only runs those tickers."""
        mock_discover.return_value = [
            ("AAPL", "2026-03-03"), ("MOBX", "2026-03-03"), ("NPT", "2026-03-03"),
        ]
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "tickers": ["MOBX"], "dates": "all"}

        run_backtest(config, yolo_repo=tmp_path)

        # Should only evaluate MOBX, not AAPL or NPT
        assert mock_run.call_count == 1

    def test_discover_pairs_no_date_filter(self, tmp_path: Path) -> None:
        """_discover_pairs_from_cache with dates=None returns all pairs."""
        cache_dir = tmp_path / "analysis" / "cache" / "day_sim"
        cache_dir.mkdir(parents=True)
        (cache_dir / "MOBX_2026-03-03_1min.json").write_text("[]")
        (cache_dir / "MOBX_2026-03-04_1min.json").write_text("[]")
        (cache_dir / "NPT_2026-03-05_1min.json").write_text("[]")

        pairs = _discover_pairs_from_cache(tmp_path, dates=None)

        assert len(pairs) == 3
        assert ("MOBX", "2026-03-03") in pairs
        assert ("MOBX", "2026-03-04") in pairs
        assert ("NPT", "2026-03-05") in pairs
