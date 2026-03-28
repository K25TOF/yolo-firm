"""Unit tests for agents/tools.py — backtest execution and memory tools."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add agents/ to path so we can import tools
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from tools import (
    _compute_distribution_metrics,
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


def _make_mock_ds(tmp_path: Path, pairs: list | None = None) -> MagicMock:
    """Create a mock DataStore with sensible defaults."""
    ds = MagicMock()
    ds.list_ticker_date_pairs.return_value = pairs or []
    ds.get_1min_bars.return_value = []
    ds.get_news.return_value = []
    ds.results_dir = tmp_path / "analysis" / "research" / "results"
    return ds


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
    @patch("tools._create_datastore")
    def test_returns_correct_schema(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_ds_factory.return_value = _make_mock_ds(tmp_path)
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
    @patch("tools._create_datastore")
    def test_inconclusive_when_under_50_trades(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_ds_factory.return_value = _make_mock_ds(tmp_path)
        mock_run.return_value = (
            _make_mock_result(10), _make_summary(10, 0.40, 0.05),
        )

        result = run_backtest(VALID_CONFIG, yolo_repo=tmp_path)

        assert result["inconclusive"] is True
        assert result["trade_count"] < 50

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_not_inconclusive_when_over_50_trades(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_ds_factory.return_value = _make_mock_ds(tmp_path)
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
    @patch("tools._create_datastore")
    def test_results_csv_written(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_ds_factory.return_value = _make_mock_ds(tmp_path)
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

    @patch("tools._create_datastore")
    def test_bad_config_returns_error(self, mock_ds_factory: MagicMock, tmp_path: Path) -> None:
        mock_ds_factory.return_value = _make_mock_ds(tmp_path)
        bad_config = {"strategy_id": "test"}  # Missing required fields

        result = run_backtest(bad_config, yolo_repo=tmp_path)

        assert "error" in result
        assert result["inconclusive"] is True

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_missing_cache_returns_error_in_summary(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        mock_ds_factory.return_value = _make_mock_ds(tmp_path)
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
        (agents_dir / "optimist").mkdir(parents=True)

        result = update_memory("optimist", "# New memory\n- fact 1", agents_dir=agents_dir)

        assert result["ok"] is True
        written = (agents_dir / "optimist" / "memory.md").read_text()
        assert "# New memory" in written
        assert "fact 1" in written

    def test_agent_identity_enforced(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        (agents_dir / "optimist").mkdir(parents=True)

        result = update_memory(
            "optimist", "content", agents_dir=agents_dir, calling_agent="manager",
        )

        assert result["ok"] is False
        assert "mismatch" in result["error"].lower()

    def test_error_on_invalid_agent(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir(parents=True)

        result = update_memory("hacker", "content", agents_dir=agents_dir)

        assert result["ok"] is False

    # --- P1.1: Memory versioning tests ---

    def test_backup_created_on_write(self, tmp_path: Path) -> None:
        """Successful write creates timestamped backup of prior content."""
        agents_dir = tmp_path / "agents"
        agent_dir = agents_dir / "optimist"
        agent_dir.mkdir(parents=True)
        (agent_dir / "memory.md").write_text("original content")

        result = update_memory("optimist", "new content", agents_dir=agents_dir)

        assert result["ok"] is True
        assert result["backup_path"] is not None
        # Backup contains the ORIGINAL content (before write)
        backup = Path(result["backup_path"])
        assert backup.exists()
        assert backup.read_text() == "original content"
        # Memory file contains the NEW content
        assert (agent_dir / "memory.md").read_text() == "new content"
        # Backup is in the memory-history subdirectory
        assert backup.parent.name == "memory-history"
        assert backup.parent.parent == agent_dir

    def test_backup_filename_format(self, tmp_path: Path) -> None:
        """Backup filename is YYYYMMDD-HHMMSS.md (UTC)."""
        import re

        agents_dir = tmp_path / "agents"
        agent_dir = agents_dir / "optimist"
        agent_dir.mkdir(parents=True)
        (agent_dir / "memory.md").write_text("old")

        result = update_memory("optimist", "new", agents_dir=agents_dir)

        backup = Path(result["backup_path"])
        assert re.match(r"\d{8}-\d{6}\.md$", backup.name)

    def test_backup_dir_created_if_missing(self, tmp_path: Path) -> None:
        """memory-history/ directory created automatically on first write."""
        agents_dir = tmp_path / "agents"
        agent_dir = agents_dir / "optimist"
        agent_dir.mkdir(parents=True)
        (agent_dir / "memory.md").write_text("old")

        assert not (agent_dir / "memory-history").exists()

        result = update_memory("optimist", "new", agents_dir=agents_dir)

        assert result["ok"] is True
        assert (agent_dir / "memory-history").exists()

    def test_no_backup_when_no_prior_file(self, tmp_path: Path) -> None:
        """First-ever write (no existing memory.md) has no backup to create."""
        agents_dir = tmp_path / "agents"
        agent_dir = agents_dir / "optimist"
        agent_dir.mkdir(parents=True)
        # No memory.md exists yet

        result = update_memory("optimist", "first content", agents_dir=agents_dir)

        assert result["ok"] is True
        assert result["backup_path"] is None
        assert (agent_dir / "memory.md").read_text() == "first content"

    def test_failed_write_preserves_original(self, tmp_path: Path) -> None:
        """If write fails, original memory.md and backup both preserved."""
        agents_dir = tmp_path / "agents"
        agent_dir = agents_dir / "optimist"
        agent_dir.mkdir(parents=True)
        (agent_dir / "memory.md").write_text("precious content")

        with patch.object(Path, "write_text", side_effect=OSError("disk full")):
            result = update_memory("optimist", "bad write", agents_dir=agents_dir)

        assert result["ok"] is False
        assert result["backup_path"] is None
        assert "disk full" in result["error"]
        # Original file must be untouched
        assert (agent_dir / "memory.md").read_text() == "precious content"

    def test_backup_rotation_deletes_old(self, tmp_path: Path) -> None:
        """Backups older than 30 days are deleted after successful write."""
        agents_dir = tmp_path / "agents"
        agent_dir = agents_dir / "optimist"
        history_dir = agent_dir / "memory-history"
        history_dir.mkdir(parents=True)
        (agent_dir / "memory.md").write_text("current")

        # Create an old backup (35 days ago)
        import os
        import time

        old_backup = history_dir / "20260220-120000.md"
        old_backup.write_text("ancient")
        old_time = time.time() - (35 * 86400)
        os.utime(old_backup, (old_time, old_time))

        # Create a recent backup (5 days ago)
        recent_backup = history_dir / "20260322-120000.md"
        recent_backup.write_text("recent")
        recent_time = time.time() - (5 * 86400)
        os.utime(recent_backup, (recent_time, recent_time))

        result = update_memory("optimist", "newest", agents_dir=agents_dir)

        assert result["ok"] is True
        # Old backup deleted
        assert not old_backup.exists()
        # Recent backup preserved
        assert recent_backup.exists()
        # New backup created (3 total files: recent + new backup)
        backups = list(history_dir.glob("*.md"))
        assert len(backups) == 2  # recent + just-created

    def test_rotation_only_on_success(self, tmp_path: Path) -> None:
        """Rotation does NOT run when write fails."""
        agents_dir = tmp_path / "agents"
        agent_dir = agents_dir / "optimist"
        history_dir = agent_dir / "memory-history"
        history_dir.mkdir(parents=True)
        (agent_dir / "memory.md").write_text("current")

        import os
        import time

        old_backup = history_dir / "20260220-120000.md"
        old_backup.write_text("ancient")
        old_time = time.time() - (35 * 86400)
        os.utime(old_backup, (old_time, old_time))

        with patch.object(Path, "write_text", side_effect=OSError("disk full")):
            result = update_memory("optimist", "fail", agents_dir=agents_dir)

        assert result["ok"] is False
        # Old backup must still exist — rotation did not run
        assert old_backup.exists()

    def test_rotation_noop_when_no_old_backups(self, tmp_path: Path) -> None:
        """Rotation is a no-op when all backups are recent."""
        agents_dir = tmp_path / "agents"
        agent_dir = agents_dir / "optimist"
        history_dir = agent_dir / "memory-history"
        history_dir.mkdir(parents=True)
        (agent_dir / "memory.md").write_text("current")

        recent = history_dir / "20260325-120000.md"
        recent.write_text("recent")

        result = update_memory("optimist", "new", agents_dir=agents_dir)

        assert result["ok"] is True
        assert recent.exists()

    def test_identity_violation_returns_no_backup(self, tmp_path: Path) -> None:
        """Identity violation returns error with backup_path=None, no files modified."""
        agents_dir = tmp_path / "agents"
        agent_dir = agents_dir / "optimist"
        agent_dir.mkdir(parents=True)
        (agent_dir / "memory.md").write_text("original")

        result = update_memory(
            "optimist", "hijack", agents_dir=agents_dir, calling_agent="challenger",
        )

        assert result["ok"] is False
        assert result.get("backup_path") is None
        assert (agent_dir / "memory.md").read_text() == "original"
        assert not (agent_dir / "memory-history").exists()

    def test_return_value_schema(self, tmp_path: Path) -> None:
        """Return dict has all required keys: ok, path, backup_path, error."""
        agents_dir = tmp_path / "agents"
        (agents_dir / "optimist").mkdir(parents=True)
        (agents_dir / "optimist" / "memory.md").write_text("old")

        result = update_memory("optimist", "new", agents_dir=agents_dir)

        assert "ok" in result
        assert "path" in result
        assert "backup_path" in result
        assert "error" in result
        assert result["ok"] is True
        assert result["error"] is None
        assert result["path"].endswith("memory.md")
        assert result["backup_path"] is not None


# --- Helpers for momentum filter tests ---

def _bar(high: float, low: float) -> dict:
    """Create a minimal bar dict with high and low prices (for filter helper)."""
    return {"h": high, "l": low}


def _mock_bar_obj(high: float, low: float) -> MagicMock:
    """Create a mock Bar object with high/low attributes."""
    b = MagicMock()
    b.high = high
    b.low = low
    return b


class TestMomentumFilter:
    """Tests for _passes_momentum_filter helper."""

    def test_excludes_low_range_pairs(self) -> None:
        bars = [_bar(1.2, 1.0), _bar(1.49, 1.1), _bar(1.3, 1.05)]
        assert _passes_momentum_filter(bars) is False

    def test_includes_high_range_pairs(self) -> None:
        bars = [_bar(2.0, 1.0), _bar(1.5, 1.2)]
        assert _passes_momentum_filter(bars) is True

    def test_threshold_boundary_passes(self) -> None:
        bars = [_bar(1.50, 1.00)]
        assert _passes_momentum_filter(bars) is True

    def test_threshold_boundary_fails(self) -> None:
        bars = [_bar(1.499, 1.00)]
        assert _passes_momentum_filter(bars) is False

    def test_zero_low_returns_false(self) -> None:
        bars = [_bar(5.0, 0.0)]
        assert _passes_momentum_filter(bars) is False

    def test_empty_bars_returns_false(self) -> None:
        assert _passes_momentum_filter([]) is False


class TestMomentumUniverse:
    """Integration tests for momentum_universe in run_backtest."""

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_momentum_filter_excludes_low_range(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Pair with <50% range is skipped when momentum_universe=true."""
        mock_ds = _make_mock_ds(tmp_path)
        mock_ds.get_1min_bars.return_value = [_mock_bar_obj(1.2, 1.0)] * 25
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "momentum_universe": True}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_run.assert_not_called()
        assert result["pairs_skipped_momentum"] == 1
        assert result["pairs_evaluated"] == 0

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_momentum_filter_includes_high_range(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Pair with >=50% range passes filter and is evaluated."""
        mock_ds = _make_mock_ds(tmp_path)
        mock_ds.get_1min_bars.return_value = [_mock_bar_obj(2.0, 1.0)] * 25
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "momentum_universe": True}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_run.assert_called_once()
        assert result["pairs_evaluated"] == 1
        assert result["pairs_skipped_momentum"] == 0

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_momentum_filter_disabled_by_default(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """momentum_universe=false processes all pairs as before."""
        mock_ds_factory.return_value = _make_mock_ds(tmp_path)
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))

        result = run_backtest(VALID_CONFIG, yolo_repo=tmp_path)

        mock_run.assert_called_once()
        assert result["momentum_universe_enabled"] is False

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_momentum_filter_uses_full_extended_day(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Filter uses all bars (pre-market + RTH + after-hours)."""
        bars = [
            _mock_bar_obj(1.1, 1.0),   # pre-market: low of day
            _mock_bar_obj(1.3, 1.2),   # RTH: mid range
            _mock_bar_obj(1.55, 1.4),  # after-hours: high of day
        ]
        mock_ds = _make_mock_ds(tmp_path)
        mock_ds.get_1min_bars.return_value = bars
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "momentum_universe": True}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_run.assert_called_once()
        assert result["pairs_evaluated"] == 1

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_results_include_momentum_skip_count(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Return dict contains all momentum-related fields."""
        mock_ds = _make_mock_ds(tmp_path)
        mock_ds.get_1min_bars.return_value = [_mock_bar_obj(1.1, 1.0)] * 25
        mock_ds_factory.return_value = mock_ds
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


class TestTickersAll:
    """Integration tests for tickers='all' in run_backtest."""

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_tickers_all_uses_datastore_discovery(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """tickers='all' discovers pairs from DataStore."""
        mock_ds = _make_mock_ds(
            tmp_path, pairs=[("MOBX", "2026-03-03"), ("NPT", "2026-03-03")],
        )
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "tickers": "all", "dates": ["2026-03-03"]}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_ds.list_ticker_date_pairs.assert_called_once()
        assert mock_run.call_count == 2
        assert result["pairs_evaluated"] == 2

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_tickers_all_as_list_element(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """tickers=["all"] also triggers DataStore discovery."""
        mock_ds = _make_mock_ds(tmp_path, pairs=[("MOBX", "2026-03-03")])
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "tickers": ["all"], "dates": ["2026-03-03"]}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_ds.list_ticker_date_pairs.assert_called_once()
        assert result["pairs_evaluated"] == 1


class TestDistributionMetrics:
    """Tests for _compute_distribution_metrics helper."""

    def test_normal_case(self) -> None:
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
        assert m["top10_pnl_contribution_pct"] == 100.0

    def test_zero_trades(self) -> None:
        m = _compute_distribution_metrics([])

        assert m["avg_winner_pct"] is None
        assert m["avg_loser_pct"] is None
        assert m["median_pnl_pct"] is None
        assert m["max_single_trade_pnl_pct"] is None
        assert m["top10_pnl_contribution_pct"] is None

    def test_single_trade(self) -> None:
        m = _compute_distribution_metrics([{"pnl_pct": "3.5"}])

        assert m["avg_winner_pct"] == 3.5
        assert m["avg_loser_pct"] == 0.0
        assert m["median_pnl_pct"] == 3.5
        assert m["max_single_trade_pnl_pct"] == 3.5
        assert m["top10_pnl_contribution_pct"] == 100.0

    def test_all_winners(self) -> None:
        trades = [{"pnl_pct": "2.0"}, {"pnl_pct": "4.0"}, {"pnl_pct": "6.0"}]
        m = _compute_distribution_metrics(trades)

        assert m["avg_winner_pct"] == 4.0
        assert m["avg_loser_pct"] == 0.0
        assert m["max_single_trade_pnl_pct"] == 6.0

    def test_all_losers(self) -> None:
        trades = [{"pnl_pct": "-1.0"}, {"pnl_pct": "-3.0"}, {"pnl_pct": "-5.0"}]
        m = _compute_distribution_metrics(trades)

        assert m["avg_winner_pct"] == 0.0
        assert m["avg_loser_pct"] == -3.0
        assert m["max_single_trade_pnl_pct"] == -1.0

    def test_top10_contribution_with_many_trades(self) -> None:
        trades = [{"pnl_pct": "1.0"} for _ in range(10)]
        trades.append({"pnl_pct": "90.0"})
        m = _compute_distribution_metrics(trades)

        assert m["top10_pnl_contribution_pct"] == 99.0

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_distribution_in_run_backtest_output(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """run_backtest return dict includes all distribution fields."""
        mock_ds_factory.return_value = _make_mock_ds(tmp_path)
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
        trades = [{"pnl_pct": "5.0"}, {"pnl_pct": ""}, {"pnl_pct": "3.0"}]
        m = _compute_distribution_metrics(trades)

        assert m["avg_winner_pct"] == 4.0
        assert m["median_pnl_pct"] == 4.0


class TestDatesAll:
    """Tests for dates='all' support in run_backtest."""

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_dates_all_string(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates='all' discovers all dates via DataStore."""
        mock_ds = _make_mock_ds(
            tmp_path, pairs=[("MOBX", "2026-03-03"), ("MOBX", "2026-03-04")],
        )
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "dates": "all"}

        result = run_backtest(config, yolo_repo=tmp_path)

        mock_ds.list_ticker_date_pairs.assert_called_once_with(dates=None)
        assert result["pairs_evaluated"] == 2

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_dates_empty_list(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates=[] discovers all dates via DataStore."""
        mock_ds = _make_mock_ds(tmp_path, pairs=[("MOBX", "2026-03-03")])
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "dates": []}

        run_backtest(config, yolo_repo=tmp_path)

        mock_ds.list_ticker_date_pairs.assert_called_once_with(dates=None)

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_dates_none(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates=None discovers all dates via DataStore."""
        mock_ds = _make_mock_ds(tmp_path, pairs=[("MOBX", "2026-03-03")])
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {k: v for k, v in VALID_CONFIG.items() if k != "dates"}

        run_backtest(config, yolo_repo=tmp_path)

        mock_ds.list_ticker_date_pairs.assert_called_once_with(dates=None)

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_dates_list_with_all(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates=['all'] discovers all dates via DataStore."""
        mock_ds = _make_mock_ds(tmp_path, pairs=[("MOBX", "2026-03-03")])
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "dates": ["all"]}

        run_backtest(config, yolo_repo=tmp_path)

        mock_ds.list_ticker_date_pairs.assert_called_once_with(dates=None)

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_explicit_dates_unchanged(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """Explicit date list still works as before (regression)."""
        mock_ds_factory.return_value = _make_mock_ds(tmp_path)
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))

        result = run_backtest(VALID_CONFIG, yolo_repo=tmp_path)

        mock_run.assert_called_once()
        assert result["pairs_evaluated"] == 1

    @patch("tools._run_single_backtest")
    @patch("tools._build_strategy", return_value=MagicMock())
    @patch("tools._create_datastore")
    def test_dates_all_with_explicit_tickers_filters(
        self, mock_ds_factory: MagicMock, mock_strat: MagicMock,
        mock_run: MagicMock, tmp_path: Path,
    ) -> None:
        """dates='all' + explicit tickers only runs those tickers."""
        mock_ds = _make_mock_ds(tmp_path, pairs=[
            ("AAPL", "2026-03-03"), ("MOBX", "2026-03-03"), ("NPT", "2026-03-03"),
        ])
        mock_ds_factory.return_value = mock_ds
        mock_run.return_value = (_make_mock_result(5), _make_summary(5))
        config = {**VALID_CONFIG, "tickers": ["MOBX"], "dates": "all"}

        run_backtest(config, yolo_repo=tmp_path)

        assert mock_run.call_count == 1


class TestStatisticianAgent:
    """Tests for statistician agent integration."""

    def test_statistician_in_valid_agents(self) -> None:
        from tools import VALID_AGENTS

        assert "statistician" in VALID_AGENTS

    def test_update_memory_works_for_statistician(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        (agents_dir / "statistician").mkdir(parents=True)

        result = update_memory("statistician", "# Stats memory\n- fact 1", agents_dir=agents_dir)

        assert result["ok"] is True
        written = (agents_dir / "statistician" / "memory.md").read_text()
        assert "Stats memory" in written

    def test_statistician_gets_update_memory_only(self) -> None:
        from invoke import get_agent_tools

        tools = get_agent_tools("statistician")
        tool_names = [t["name"] for t in tools]
        assert "update_memory" in tool_names
        assert "run_backtest" not in tool_names

    def test_statistician_context_files_exist(self) -> None:
        agents_dir = Path(__file__).parent.parent / "agents"
        stat_dir = agents_dir / "statistician"
        assert (stat_dir / "system-prompt.md").is_file()
        assert (stat_dir / "context-manifest.md").is_file()
        assert (stat_dir / "memory.md").is_file()


class TestExecutionRealistAgent:
    """Tests for execution-realist agent integration."""

    def test_execution_realist_in_valid_agents(self) -> None:
        from tools import VALID_AGENTS

        assert "execution-realist" in VALID_AGENTS

    def test_update_memory_works_for_execution_realist(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        (agents_dir / "execution-realist").mkdir(parents=True)

        result = update_memory(
            "execution-realist", "# Exec memory\n- constraint 1", agents_dir=agents_dir,
        )

        assert result["ok"] is True
        written = (agents_dir / "execution-realist" / "memory.md").read_text()
        assert "constraint 1" in written

    def test_execution_realist_identity_enforced(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        (agents_dir / "optimist").mkdir(parents=True)

        result = update_memory(
            "optimist", "content", agents_dir=agents_dir, calling_agent="execution-realist",
        )

        assert result["ok"] is False

    def test_execution_realist_gets_update_memory_only(self) -> None:
        from invoke import get_agent_tools

        tools = get_agent_tools("execution-realist")
        tool_names = [t["name"] for t in tools]
        assert "update_memory" in tool_names
        assert "run_backtest" not in tool_names

    def test_execution_realist_context_files_exist(self) -> None:
        agents_dir = Path(__file__).parent.parent / "agents"
        agent_dir = agents_dir / "execution-realist"
        assert (agent_dir / "system-prompt.md").is_file()
        assert (agent_dir / "context-manifest.md").is_file()
        assert (agent_dir / "memory.md").is_file()
        assert (agent_dir / "constraints.md").is_file()


class TestScoutAgent:
    """Tests for scout agent integration."""

    def test_scout_in_valid_agents(self) -> None:
        from tools import VALID_AGENTS

        assert "scout" in VALID_AGENTS

    def test_update_memory_works_for_scout(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / "agents"
        (agents_dir / "scout").mkdir(parents=True)

        result = update_memory("scout", "# Scout memory\n- searched ORB", agents_dir=agents_dir)

        assert result["ok"] is True

    def test_scout_gets_web_search_and_update_memory(self) -> None:
        from invoke import get_agent_tools

        tools = get_agent_tools("scout")
        tool_names = [t["name"] for t in tools]
        assert "web_search" in tool_names
        assert "update_memory" in tool_names
        assert "run_backtest" not in tool_names

    def test_scout_web_search_is_server_side_tool(self) -> None:
        from invoke import get_agent_tools

        tools = get_agent_tools("scout")
        web_search = [t for t in tools if t.get("name") == "web_search"][0]
        assert web_search["type"] == "web_search_20250305"

    def test_other_agents_do_not_get_web_search(self) -> None:
        from invoke import get_agent_tools

        for agent in ("manager", "optimist", "challenger", "statistician", "execution-realist"):
            tools = get_agent_tools(agent)
            tool_names = [t.get("name") for t in tools]
            assert "web_search" not in tool_names, f"{agent} should not have web_search"

    def test_scout_context_files_exist(self) -> None:
        agents_dir = Path(__file__).parent.parent / "agents"
        scout_dir = agents_dir / "scout"
        assert (scout_dir / "system-prompt.md").is_file()
        assert (scout_dir / "context-manifest.md").is_file()
        assert (scout_dir / "memory.md").is_file()
