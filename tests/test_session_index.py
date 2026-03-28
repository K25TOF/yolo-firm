"""Unit tests for agents/session_index.py — session index and stale detection."""

import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from session_index import (
    _write_index_atomic,
    append_entry,
    check_stale_documents,
    count_blockers,
    count_flags,
    query,
    update_status,
)


class TestAppendEntry:
    """Tests for appending entries to the session index."""

    def test_entry_written_on_session_complete(self, tmp_path: Path) -> None:
        index_path = tmp_path / "index.json"

        entry = append_entry(
            index_path=index_path,
            session_id="LC-2025-016",
            date="2026-03-28T10:00:00Z",
            agents=["manager", "optimist", "challenger"],
            question_summary="Test ORB entry filter effectiveness",
            verdict_summary="Filters show marginal improvement",
            flag_count=3,
            blocker_count=1,
            status="complete",
            log_path="session-log/2026-03-28-orb-filter.md",
        )

        assert index_path.exists()
        data = json.loads(index_path.read_text())
        assert len(data) == 1
        assert data[0]["id"] == "LC-2025-016"
        assert data[0]["status"] == "complete"
        assert data[0]["superseded_by"] is None
        assert entry["id"] == "LC-2025-016"

    def test_append_preserves_existing_entries(self, tmp_path: Path) -> None:
        index_path = tmp_path / "index.json"
        index_path.write_text(json.dumps([{"id": "LC-2025-001", "status": "complete"}]))

        append_entry(
            index_path=index_path,
            session_id="LC-2025-002",
            date="2026-03-28T12:00:00Z",
            agents=["manager"],
            question_summary="Follow-up",
            verdict_summary="Done",
            flag_count=0,
            blocker_count=0,
            status="complete",
            log_path="log.md",
        )

        data = json.loads(index_path.read_text())
        assert len(data) == 2
        assert data[0]["id"] == "LC-2025-001"
        assert data[1]["id"] == "LC-2025-002"

    def test_question_summary_truncated_to_200(self, tmp_path: Path) -> None:
        index_path = tmp_path / "index.json"
        long_summary = "x" * 300

        append_entry(
            index_path=index_path,
            session_id="test",
            date="2026-03-28",
            agents=[],
            question_summary=long_summary,
            verdict_summary="",
            flag_count=0,
            blocker_count=0,
            status="complete",
            log_path="log.md",
        )

        data = json.loads(index_path.read_text())
        assert len(data[0]["question_summary"]) == 200

    def test_creates_parent_directory(self, tmp_path: Path) -> None:
        index_path = tmp_path / "session-log" / "index.json"

        append_entry(
            index_path=index_path,
            session_id="test",
            date="2026-03-28",
            agents=[],
            question_summary="q",
            verdict_summary="v",
            flag_count=0,
            blocker_count=0,
            status="complete",
            log_path="log.md",
        )

        assert index_path.exists()


class TestAtomicWrite:
    """Tests for atomic write safety."""

    def test_partial_write_leaves_index_intact(self, tmp_path: Path) -> None:
        """Simulated crash mid-write should not corrupt existing index."""
        index_path = tmp_path / "index.json"
        original = [{"id": "safe", "status": "complete"}]
        index_path.write_text(json.dumps(original))

        with patch("session_index.os.replace", side_effect=OSError("disk error")):
            with pytest.raises(OSError):
                _write_index_atomic(index_path, [{"id": "new"}])

        # Original file must be intact
        data = json.loads(index_path.read_text())
        assert data == original

    def test_no_temp_files_left_on_failure(self, tmp_path: Path) -> None:
        index_path = tmp_path / "index.json"

        with patch("session_index.os.replace", side_effect=OSError("fail")):
            with pytest.raises(OSError):
                _write_index_atomic(index_path, [{"id": "x"}])

        # No .tmp files should remain
        tmp_files = list(tmp_path.glob("*.tmp"))
        assert len(tmp_files) == 0


class TestUpdateStatus:
    """Tests for updating status on existing entries."""

    def test_updates_status_field(self, tmp_path: Path) -> None:
        index_path = tmp_path / "index.json"
        index_path.write_text(json.dumps([
            {"id": "LC-001", "status": "active"},
            {"id": "LC-002", "status": "complete"},
        ]))

        result = update_status(index_path, "LC-001", "superseded", superseded_by="LC-003")

        assert result is True
        data = json.loads(index_path.read_text())
        assert data[0]["status"] == "superseded"
        assert data[0]["superseded_by"] == "LC-003"
        # Other entry untouched
        assert data[1]["status"] == "complete"

    def test_returns_false_for_missing_id(self, tmp_path: Path) -> None:
        index_path = tmp_path / "index.json"
        index_path.write_text(json.dumps([{"id": "LC-001", "status": "active"}]))

        result = update_status(index_path, "nonexistent", "invalid")

        assert result is False


class TestQuery:
    """Tests for querying session index."""

    @pytest.fixture
    def index_with_entries(self, tmp_path: Path) -> Path:
        index_path = tmp_path / "index.json"
        entries = [
            {
                "id": "LC-001", "agents": ["manager", "optimist"],
                "question_summary": "ORB entry filter analysis",
                "verdict_summary": "Filters marginal", "flag_count": 2,
                "blocker_count": 0, "status": "complete",
            },
            {
                "id": "LC-002", "agents": ["manager", "challenger"],
                "question_summary": "ATR exit optimization",
                "verdict_summary": "ATR trailing stop confirmed",
                "flag_count": 1, "blocker_count": 1, "status": "complete",
            },
            {
                "id": "LC-003", "agents": ["manager", "optimist", "challenger"],
                "question_summary": "Volume profile clustering",
                "verdict_summary": "Clusters are backward-looking",
                "flag_count": 5, "blocker_count": 3, "status": "active",
            },
        ]
        index_path.write_text(json.dumps(entries))
        return index_path

    def test_topic_match(self, index_with_entries: Path) -> None:
        results = query(index_with_entries, topic="ORB")
        assert len(results) == 1
        assert results[0]["id"] == "LC-001"

    def test_topic_matches_verdict(self, index_with_entries: Path) -> None:
        results = query(index_with_entries, topic="trailing stop")
        assert len(results) == 1
        assert results[0]["id"] == "LC-002"

    def test_topic_case_insensitive(self, index_with_entries: Path) -> None:
        results = query(index_with_entries, topic="orb")
        assert len(results) == 1

    def test_agent_match(self, index_with_entries: Path) -> None:
        results = query(index_with_entries, agent="challenger")
        assert len(results) == 2
        assert {r["id"] for r in results} == {"LC-002", "LC-003"}

    def test_has_blockers_filter(self, index_with_entries: Path) -> None:
        results = query(index_with_entries, has_blockers=True)
        assert len(results) == 2
        assert {r["id"] for r in results} == {"LC-002", "LC-003"}

    def test_status_filter(self, index_with_entries: Path) -> None:
        results = query(index_with_entries, status="active")
        assert len(results) == 1
        assert results[0]["id"] == "LC-003"

    def test_combined_filters(self, index_with_entries: Path) -> None:
        results = query(index_with_entries, agent="challenger", has_blockers=True)
        assert len(results) == 2

    def test_empty_index(self, tmp_path: Path) -> None:
        index_path = tmp_path / "index.json"
        results = query(index_path, topic="anything")
        assert results == []


class TestCountFlags:
    """Tests for flag and blocker counting."""

    def test_counts_various_flag_types(self) -> None:
        transcript = (
            "[STAT FLAG] sample too small\n"
            "[EXEC FLAG] latency issue\n"
            "[SCOUT FIND] paper found\n"
            "[SCOUT CONFLICT] contradicts internal\n"
            "> **FLAG FOR CONTEXT:** important finding\n"
        )
        assert count_flags(transcript) == 5

    def test_counts_blockers(self) -> None:
        transcript = (
            "[BLOCKER: engine gap]\n"
            "Some text\n"
            "[BLOCKER: data missing]\n"
        )
        assert count_blockers(transcript) == 2

    def test_zero_on_clean_transcript(self) -> None:
        assert count_flags("Normal discussion. No flags.") == 0
        assert count_blockers("Normal discussion. No blockers.") == 0


class TestStaleDetection:
    """Tests for stale context document detection."""

    def test_fresh_file_not_flagged(self, tmp_path: Path) -> None:
        doc = tmp_path / "fresh.md"
        doc.write_text("content")
        # File just created — should be fresh

        results = check_stale_documents([doc])
        assert len(results) == 0

    def test_stale_current_state_flagged_at_8_days(self, tmp_path: Path) -> None:
        doc = tmp_path / "CURRENT-STATE.md"
        doc.write_text("content")
        old_time = time.time() - (8 * 86400)
        os.utime(doc, (old_time, old_time))

        results = check_stale_documents([doc])
        assert len(results) == 1
        assert results[0]["threshold_days"] == 7

    def test_current_state_fresh_at_6_days(self, tmp_path: Path) -> None:
        doc = tmp_path / "CURRENT-STATE.md"
        doc.write_text("content")
        recent_time = time.time() - (6 * 86400)
        os.utime(doc, (recent_time, recent_time))

        results = check_stale_documents([doc])
        assert len(results) == 0

    def test_other_doc_flagged_at_15_days(self, tmp_path: Path) -> None:
        doc = tmp_path / "way-of-working.md"
        doc.write_text("content")
        old_time = time.time() - (15 * 86400)
        os.utime(doc, (old_time, old_time))

        results = check_stale_documents([doc])
        assert len(results) == 1
        assert results[0]["threshold_days"] == 14

    def test_claude_md_never_flagged(self, tmp_path: Path) -> None:
        doc = tmp_path / "CLAUDE.md"
        doc.write_text("content")
        ancient_time = time.time() - (365 * 86400)
        os.utime(doc, (ancient_time, ancient_time))

        results = check_stale_documents([doc])
        assert len(results) == 0

    def test_missing_file_ignored(self, tmp_path: Path) -> None:
        doc = tmp_path / "nonexistent.md"
        results = check_stale_documents([doc])
        assert len(results) == 0
