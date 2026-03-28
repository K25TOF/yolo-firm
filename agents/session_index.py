"""Session index management — append-only JSON index for research sessions.

Provides atomic read/write operations for research/session-log/index.json.
Used by session.py and invoke.py to record completed sessions, and by
scripts/query_sessions.py to search session history.
"""

from __future__ import annotations

import json
import logging
import os
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

INDEX_FILENAME = "index.json"

# Flag patterns to count in transcripts
_FLAG_PATTERNS = [
    r"\[STAT FLAG\]",
    r"\[EXEC FLAG\]",
    r"\[SCOUT FIND\]",
    r"\[SCOUT CONFLICT\]",
    r"\*\*FLAG FOR CONTEXT:\*\*",
]
_BLOCKER_PATTERN = r"\[BLOCKER:"

# Stale thresholds in days
STALE_THRESHOLD_DEFAULT = 14
STALE_THRESHOLD_CURRENT_STATE = 7
STALE_EXEMPT_FILES = {"CLAUDE.md"}


def _read_index(index_path: Path) -> list[dict]:
    """Read the session index, returning empty list if missing or corrupt."""
    if not index_path.exists():
        return []
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        logger.warning("Index is not a list, resetting: %s", index_path)
        return []
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Failed to read index, returning empty: %s", e)
        return []


def _write_index_atomic(index_path: Path, entries: list[dict]) -> None:
    """Write entries to index using temp-file-then-rename for atomicity."""
    index_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=str(index_path.parent), suffix=".tmp", prefix=".index-",
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp_path, str(index_path))
    except Exception:
        # Clean up temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def count_flags(transcript: str) -> int:
    """Count flag tags in a session transcript."""
    total = 0
    for pattern in _FLAG_PATTERNS:
        total += len(re.findall(pattern, transcript))
    return total


def count_blockers(transcript: str) -> int:
    """Count blocker tags in a session transcript."""
    return len(re.findall(_BLOCKER_PATTERN, transcript))


def append_entry(
    index_path: Path,
    session_id: str,
    date: str,
    agents: list[str],
    question_summary: str,
    verdict_summary: str,
    flag_count: int,
    blocker_count: int,
    status: str,
    log_path: str,
) -> dict:
    """Append a new session entry to the index. Returns the entry."""
    entry = {
        "id": session_id,
        "date": date,
        "agents": agents,
        "question_summary": question_summary[:200],
        "verdict_summary": verdict_summary[:500],
        "flag_count": flag_count,
        "blocker_count": blocker_count,
        "status": status,
        "superseded_by": None,
        "log_path": log_path,
    }
    entries = _read_index(index_path)
    entries.append(entry)
    _write_index_atomic(index_path, entries)
    return entry


def update_status(
    index_path: Path,
    session_id: str,
    status: str,
    superseded_by: str | None = None,
) -> bool:
    """Update status (and optionally superseded_by) on an existing entry.

    Returns True if entry was found and updated, False otherwise.
    """
    entries = _read_index(index_path)
    for entry in entries:
        if entry["id"] == session_id:
            entry["status"] = status
            if superseded_by is not None:
                entry["superseded_by"] = superseded_by
            _write_index_atomic(index_path, entries)
            return True
    return False


def query(
    index_path: Path,
    topic: str | None = None,
    agent: str | None = None,
    has_blockers: bool = False,
    status: str | None = None,
) -> list[dict]:
    """Query index entries by filter criteria."""
    entries = _read_index(index_path)
    results = []
    for entry in entries:
        if topic:
            topic_lower = topic.lower()
            if (topic_lower not in entry.get("question_summary", "").lower()
                    and topic_lower not in entry.get("verdict_summary", "").lower()):
                continue
        if agent:
            if agent.lower() not in [a.lower() for a in entry.get("agents", [])]:
                continue
        if has_blockers:
            if entry.get("blocker_count", 0) <= 0:
                continue
        if status:
            if entry.get("status", "").lower() != status.lower():
                continue
        results.append(entry)
    return results


def check_stale_documents(
    doc_paths: list[Path],
) -> list[dict]:
    """Check documents for staleness based on modification time.

    Returns list of {path, last_modified, threshold_days, stale: True} for stale docs.
    """
    now = datetime.now(UTC).timestamp()
    stale_docs = []
    for path in doc_paths:
        if not path.exists():
            continue  # Missing files handled separately
        filename = path.name
        if filename in STALE_EXEMPT_FILES:
            continue
        if filename == "CURRENT-STATE.md":
            threshold_days = STALE_THRESHOLD_CURRENT_STATE
        else:
            threshold_days = STALE_THRESHOLD_DEFAULT

        mtime = path.stat().st_mtime
        age_days = (now - mtime) / 86400
        if age_days > threshold_days:
            last_mod = datetime.fromtimestamp(mtime, tz=UTC).strftime("%Y-%m-%d")
            stale_docs.append({
                "path": str(path),
                "last_modified": last_mod,
                "threshold_days": threshold_days,
            })
    return stale_docs
