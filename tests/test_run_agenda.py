"""Unit tests for agents/run_agenda.py — research agenda orchestration."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from run_agenda import (
    _find_next_task,
    _mark_task_complete,
    run_agenda,
)
from session import SessionResult


SAMPLE_AGENDA = """\
# Research Agenda — Grinder Strategy Validation

Approved: 2026-03-07
Status: active

## Objective
Validate grinder entry/exit rules on expanded dataset.

## Tasks
- [ ] Task 1: Re-test HYP-025 with corrected exit rule — Deliverable: backtest results
- [ ] Task 2: Analyse sub-$1 vs $5+ performance split — Deliverable: price bucket report
- [x] Task 3: Review acceleration filter thresholds (completed — see LC-2025-002)

## Scope Boundaries
In scope: grinder strategy backtesting, indicator validation
Out of scope: vol_filter changes, live trading decisions

## Success Criteria
Clear pass/fail on grinder entry signal with corrected exit.

## Constraints
- Max sessions: 10
- Escalate to PO if: win rate ambiguous between 35-45%
"""


class TestFindNextTask:
    """Tests for _find_next_task — locating the next incomplete agenda task."""

    def test_finds_first_unchecked_task(self) -> None:
        task = _find_next_task(SAMPLE_AGENDA)
        assert task is not None
        assert "Task 1" in task
        assert "Re-test HYP-025" in task

    def test_skips_completed_tasks(self) -> None:
        # Mark task 1 complete
        agenda = SAMPLE_AGENDA.replace(
            "- [ ] Task 1:",
            "- [x] Task 1:",
        )
        task = _find_next_task(agenda)
        assert task is not None
        assert "Task 2" in task

    def test_returns_none_when_all_complete(self) -> None:
        agenda = SAMPLE_AGENDA.replace("- [ ] Task 1:", "- [x] Task 1:")
        agenda = agenda.replace("- [ ] Task 2:", "- [x] Task 2:")
        task = _find_next_task(agenda)
        assert task is None

    def test_handles_empty_content(self) -> None:
        assert _find_next_task("") is None


class TestMarkTaskComplete:
    """Tests for _mark_task_complete — marking a task [x] in agenda text."""

    def test_marks_matching_task(self) -> None:
        task_text = "Task 1: Re-test HYP-025 with corrected exit rule — Deliverable: backtest results"
        result = _mark_task_complete(SAMPLE_AGENDA, task_text)
        assert "- [x] Task 1: Re-test HYP-025" in result
        # Original [ ] should be gone for task 1
        assert "- [ ] Task 1:" not in result

    def test_preserves_other_tasks(self) -> None:
        task_text = "Task 1: Re-test HYP-025 with corrected exit rule — Deliverable: backtest results"
        result = _mark_task_complete(SAMPLE_AGENDA, task_text)
        # Task 2 should still be unchecked
        assert "- [ ] Task 2:" in result


class TestRunAgenda:
    """Integration tests for the agenda loop."""

    @pytest.fixture
    def agenda_env(self, tmp_path: Path) -> Path:
        """Create an agents dir with a research agenda."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        agenda_path = agents_dir / "research-agenda.md"
        agenda_path.write_text(SAMPLE_AGENDA)
        return agents_dir

    def _mock_session_result(
        self,
        session_id: str = "test",
        outcome: str = "complete",
    ) -> SessionResult:
        return SessionResult(
            session_id=session_id,
            outcome=outcome,
            input_tokens=1000,
            output_tokens=500,
            cost_usd=0.0035,
            duration_seconds=45.0,
            task_summary="Session completed successfully.",
        )

    @patch("run_agenda.run_session")
    @patch("run_agenda.send_pushover", return_value=True)
    def test_next_task_selected_correctly(
        self,
        mock_pushover: MagicMock,
        mock_session: MagicMock,
        agenda_env: Path,
    ) -> None:
        """First incomplete task is selected as session question."""
        mock_session.return_value = self._mock_session_result()

        with patch("run_agenda.AGENTS_DIR", agenda_env):
            run_agenda(max_sessions=1)

        mock_session.assert_called_once()
        call_kwargs = mock_session.call_args[1]
        assert "Re-test HYP-025" in call_kwargs["question"]

    @patch("run_agenda.run_session")
    @patch("run_agenda.send_pushover", return_value=True)
    def test_task_marked_complete_after_session(
        self,
        mock_pushover: MagicMock,
        mock_session: MagicMock,
        agenda_env: Path,
    ) -> None:
        """Task is marked [x] in agenda file after session completes."""
        mock_session.return_value = self._mock_session_result()

        with patch("run_agenda.AGENTS_DIR", agenda_env):
            run_agenda(max_sessions=1)

        agenda_content = (agenda_env / "research-agenda.md").read_text()
        assert "- [x] Task 1:" in agenda_content

    @patch("run_agenda.run_session")
    @patch("run_agenda.send_pushover", return_value=True)
    def test_pause_flag_stops_between_sessions(
        self,
        mock_pushover: MagicMock,
        mock_session: MagicMock,
        agenda_env: Path,
    ) -> None:
        """pause.flag stops the agenda loop between sessions."""
        mock_session.return_value = self._mock_session_result()
        # Create pause flag before second session would start
        call_count = 0

        def session_side_effect(**kwargs):
            nonlocal call_count
            call_count += 1
            # After first session, create pause flag
            (agenda_env / "pause.flag").write_text("pause")
            return self._mock_session_result()

        mock_session.side_effect = session_side_effect

        with patch("run_agenda.AGENTS_DIR", agenda_env):
            run_agenda(max_sessions=10)

        # Only one session should run (pause stops before second)
        assert call_count == 1

    @patch("run_agenda.run_session")
    @patch("run_agenda.send_pushover", return_value=True)
    def test_blocker_flag_stops_agenda(
        self,
        mock_pushover: MagicMock,
        mock_session: MagicMock,
        agenda_env: Path,
    ) -> None:
        """blocker.flag from session stops agenda before next session."""

        def session_side_effect(**kwargs):
            # Session creates blocker flag (as session.py would)
            (agenda_env / "blocker.flag").write_text("Missing indicator")
            return self._mock_session_result(outcome="blocker")

        mock_session.side_effect = session_side_effect

        with patch("run_agenda.AGENTS_DIR", agenda_env):
            run_agenda(max_sessions=10)

        # Only one session runs (blocker outcome stops loop)
        mock_session.assert_called_once()

    @patch("run_agenda.run_session")
    @patch("run_agenda.send_pushover", return_value=True)
    def test_scope_request_blocking_pauses(
        self,
        mock_pushover: MagicMock,
        mock_session: MagicMock,
        agenda_env: Path,
    ) -> None:
        """scope-request.flag from a blocker outcome stops the agenda."""

        def session_side_effect(**kwargs):
            (agenda_env / "scope-request.flag").write_text("Need new data")
            return self._mock_session_result(outcome="blocker")

        mock_session.side_effect = session_side_effect

        with patch("run_agenda.AGENTS_DIR", agenda_env):
            run_agenda(max_sessions=10)

        mock_session.assert_called_once()

    @patch("run_agenda.run_session")
    @patch("run_agenda.send_pushover", return_value=True)
    def test_max_sessions_respected(
        self,
        mock_pushover: MagicMock,
        mock_session: MagicMock,
        agenda_env: Path,
    ) -> None:
        """Loop stops at --max-sessions N even if tasks remain."""
        mock_session.return_value = self._mock_session_result()

        with patch("run_agenda.AGENTS_DIR", agenda_env):
            run_agenda(max_sessions=1)

        mock_session.assert_called_once()
        # Task 2 should still be incomplete
        agenda_content = (agenda_env / "research-agenda.md").read_text()
        assert "- [ ] Task 2:" in agenda_content

    @patch("run_agenda.run_session")
    @patch("run_agenda.send_pushover", return_value=True)
    def test_all_tasks_complete_sends_notification(
        self,
        mock_pushover: MagicMock,
        mock_session: MagicMock,
        agenda_env: Path,
    ) -> None:
        """Pushover 'agenda complete' notification sent when all tasks done."""
        mock_session.return_value = self._mock_session_result()

        with patch("run_agenda.AGENTS_DIR", agenda_env):
            run_agenda(max_sessions=10)

        # Should have sent completion notification
        pushover_calls = mock_pushover.call_args_list
        completion_call = [
            c
            for c in pushover_calls
            if "complete" in str(c).lower() or "Agenda" in str(c)
        ]
        assert len(completion_call) >= 1

    @patch("run_agenda.run_session")
    @patch("run_agenda.send_pushover", return_value=True)
    def test_dry_run_does_not_call_session(
        self,
        mock_pushover: MagicMock,
        mock_session: MagicMock,
        agenda_env: Path,
    ) -> None:
        """Dry-run prints plan but doesn't execute sessions."""
        with patch("run_agenda.AGENTS_DIR", agenda_env):
            run_agenda(max_sessions=10, dry_run=True)

        mock_session.assert_not_called()
