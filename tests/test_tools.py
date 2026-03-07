"""Unit tests for agents/tools.py — backtest execution tool."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add agents/ to path so we can import tools
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from tools import resolve_yolo_repo, run_backtest


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
