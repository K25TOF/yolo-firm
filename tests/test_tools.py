"""Unit tests for agents/tools.py — backtest execution and memory tools."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add agents/ to path so we can import tools
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from tools import _passes_momentum_filter, resolve_yolo_repo, run_backtest, update_memory


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
