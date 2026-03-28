"""Unit tests for agents/invoke.py — context loading and session logging."""

import sys
from pathlib import Path

import pytest

# Add agents/ to path so we can import invoke
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from invoke import (
    load_context,
    parse_context_manifest,
    write_session_log,
)


@pytest.fixture
def sample_manifest(tmp_path: Path) -> Path:
    """Create a sample context-manifest.md file."""
    manifest = tmp_path / "context-manifest.md"
    manifest.write_text(
        "# Test — Context Manifest\n\n"
        "## Firm Documents (yolo-firm/)\n\n"
        "| Document | Path | Purpose |\n"
        "|---|---|---|\n"
        "| RACI | `raci.md` | Roles |\n"
        "| Strategy | `strategy-roadmap.md` | Vision |\n\n"
        "## Research Documents (yolo/analysis/research/)\n\n"
        "| Document | Path | Purpose |\n"
        "|---|---|---|\n"
        "| Ideas | `analysis/research/ideas.md` | Ideas log |\n"
    )
    return manifest


@pytest.fixture
def firm_repo(tmp_path: Path) -> Path:
    """Create a mock yolo-firm repo with some docs."""
    firm = tmp_path / "yolo-firm"
    firm.mkdir()
    (firm / "raci.md").write_text("# RACI\nRoles here.")
    (firm / "strategy-roadmap.md").write_text("# Strategy\nRoadmap here.")
    return firm


@pytest.fixture
def yolo_repo(tmp_path: Path) -> Path:
    """Create a mock yolo repo with research docs."""
    yolo = tmp_path / "yolo"
    yolo.mkdir()
    research = yolo / "analysis" / "research"
    research.mkdir(parents=True)
    (research / "ideas.md").write_text("# Ideas\nIDEA-001: Test idea")
    return yolo


class TestParseContextManifest:
    """Tests for parsing context-manifest.md files."""

    def test_parses_firm_docs(self, sample_manifest: Path) -> None:
        result = parse_context_manifest(sample_manifest)
        firm_paths = [e["path"] for e in result if e["source"] == "firm"]
        assert "raci.md" in firm_paths
        assert "strategy-roadmap.md" in firm_paths

    def test_parses_yolo_docs(self, sample_manifest: Path) -> None:
        result = parse_context_manifest(sample_manifest)
        yolo_paths = [e["path"] for e in result if e["source"] == "yolo"]
        assert "analysis/research/ideas.md" in yolo_paths

    def test_returns_document_names(self, sample_manifest: Path) -> None:
        result = parse_context_manifest(sample_manifest)
        names = [e["name"] for e in result]
        assert "RACI" in names
        assert "Ideas" in names

    def test_empty_manifest(self, tmp_path: Path) -> None:
        manifest = tmp_path / "empty.md"
        manifest.write_text("# Empty manifest\n\nNo tables here.\n")
        result = parse_context_manifest(manifest)
        assert result == []


class TestLoadContext:
    """Tests for loading document content from repos."""

    def test_loads_firm_docs(
        self, sample_manifest: Path, firm_repo: Path, yolo_repo: Path,
    ) -> None:
        entries = parse_context_manifest(sample_manifest)
        docs, missing = load_context(entries, firm_repo, yolo_repo)
        assert len(docs) >= 2
        assert any("RACI" in d["content"] for d in docs)
        assert missing == []

    def test_handles_missing_file_gracefully(
        self, tmp_path: Path, firm_repo: Path, yolo_repo: Path,
    ) -> None:
        entries = [
            {"name": "Missing", "path": "nonexistent.md", "source": "firm"},
        ]
        docs, missing = load_context(entries, firm_repo, yolo_repo)
        assert len(docs) == 0
        assert "nonexistent.md" in missing[0]

    def test_loads_yolo_docs(
        self, sample_manifest: Path, firm_repo: Path, yolo_repo: Path,
    ) -> None:
        entries = parse_context_manifest(sample_manifest)
        docs, missing = load_context(entries, firm_repo, yolo_repo)
        yolo_docs = [d for d in docs if "Ideas" in d["content"]]
        assert len(yolo_docs) == 1


class TestWriteSessionLog:
    """Tests for session log file writing."""

    def test_creates_log_file(self, tmp_path: Path) -> None:
        write_session_log(
            log_dir=tmp_path,
            session_id="test-session",
            agent="optimist",
            model="claude-haiku-4-5-20251001",
            context_files=["raci.md", "strategy-roadmap.md"],
            missing_files=[],
            message="What should we test?",
            response="We should test volume filters.",
        )
        log_files = list(tmp_path.glob("*.md"))
        assert len(log_files) == 1
        assert "test-session" in log_files[0].name

    def test_log_contains_exchange(self, tmp_path: Path) -> None:
        write_session_log(
            log_dir=tmp_path,
            session_id="test-session",
            agent="optimist",
            model="claude-haiku-4-5-20251001",
            context_files=["raci.md"],
            missing_files=[],
            message="What should we test?",
            response="Volume filters.",
        )
        log_file = list(tmp_path.glob("*.md"))[0]
        content = log_file.read_text()
        assert "What should we test?" in content
        assert "Volume filters." in content
        assert "optimist" in content.lower()

    def test_log_notes_missing_files(self, tmp_path: Path) -> None:
        write_session_log(
            log_dir=tmp_path,
            session_id="test-session",
            agent="optimist",
            model="claude-haiku-4-5-20251001",
            context_files=["raci.md"],
            missing_files=["missing.md"],
            message="test",
            response="response",
        )
        log_file = list(tmp_path.glob("*.md"))[0]
        content = log_file.read_text()
        assert "MISSING" in content
        assert "missing.md" in content

    def test_appends_to_existing_session(self, tmp_path: Path) -> None:
        for i in range(2):
            write_session_log(
                log_dir=tmp_path,
                session_id="multi-turn",
                agent="optimist",
                model="claude-haiku-4-5-20251001",
                context_files=["raci.md"],
                missing_files=[],
                message=f"Question {i}",
                response=f"Answer {i}",
            )
        log_files = list(tmp_path.glob("*.md"))
        assert len(log_files) == 1
        content = log_files[0].read_text()
        assert "Question 0" in content
        assert "Question 1" in content


