"""Unit tests for agents/session.py — multi-agent session orchestration."""

import re
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add agents/ to path so we can import session
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from session import (
    SessionResult,
    TokenTracker,
    TurnResult,
    build_transcript,
    check_interrupt,
    generate_session_id,
    invoke_agent,
    is_server_running,
    load_agent_context,
    run_session,
    write_review_doc,
)


class TestGenerateSessionId:
    """Tests for session ID generation."""

    def test_returns_timestamp_format(self) -> None:
        sid = generate_session_id()
        assert re.match(r"\d{8}-\d{6}", sid), f"Expected YYYYMMDD-HHMMSS, got {sid}"

    def test_length_is_correct(self) -> None:
        sid = generate_session_id()
        assert len(sid) == 15


class TestTokenTracker:
    """Tests for cumulative token tracking."""

    def test_empty_tracker_has_zero_totals(self) -> None:
        tracker = TokenTracker()
        assert tracker.total_input == 0
        assert tracker.total_output == 0

    def test_tracks_single_turn(self) -> None:
        tracker = TokenTracker()
        tracker.turns.append(
            TurnResult("manager", "q", "r", 100, 50, None),
        )
        assert tracker.total_input == 100
        assert tracker.total_output == 50

    def test_accumulates_multiple_turns(self) -> None:
        tracker = TokenTracker()
        tracker.turns.append(TurnResult("manager", "q1", "r1", 100, 50, None))
        tracker.turns.append(TurnResult("analyst", "q2", "r2", 200, 80, None))
        assert tracker.total_input == 300
        assert tracker.total_output == 130

    def test_summary_includes_per_turn_breakdown(self) -> None:
        tracker = TokenTracker()
        tracker.turns.append(TurnResult("manager", "q", "r", 100, 50, None))
        tracker.turns.append(TurnResult("analyst", "q", "r", 200, 80, None))
        summary = tracker.summary()
        assert "manager" in summary.lower()
        assert "analyst" in summary.lower()
        assert "300" in summary  # total input
        assert "130" in summary  # total output

    def test_summary_includes_cost_estimate(self) -> None:
        tracker = TokenTracker()
        tracker.turns.append(TurnResult("manager", "q", "r", 1_000_000, 200_000, None))
        summary = tracker.summary()
        assert "$" in summary


class TestBuildTranscript:
    """Tests for session transcript generation."""

    def test_empty_turns_returns_empty_string(self) -> None:
        assert build_transcript([]) == ""

    def test_single_turn_formats_correctly(self) -> None:
        turns = [TurnResult("manager", "Open session", "Session opened.", 100, 50, None)]
        transcript = build_transcript(turns)
        assert "Manager" in transcript
        assert "Session opened." in transcript

    def test_multiple_turns_in_order(self) -> None:
        turns = [
            TurnResult("manager", "Open", "Opened.", 100, 50, None),
            TurnResult("analyst", "Question", "Analysis.", 200, 80, None),
        ]
        transcript = build_transcript(turns)
        manager_pos = transcript.index("Manager")
        analyst_pos = transcript.index("Analyst")
        assert manager_pos < analyst_pos

    def test_excludes_token_counts_from_transcript(self) -> None:
        turns = [TurnResult("manager", "q", "r", 12345, 67890, None)]
        transcript = build_transcript(turns)
        assert "12345" not in transcript
        assert "67890" not in transcript


class TestLoadAgentContext:
    """Tests for agent context loading."""

    @pytest.fixture
    def agent_tree(self, tmp_path: Path) -> Path:
        """Create a minimal agent directory structure."""
        agents = tmp_path / "agents"
        agents.mkdir()
        mgr = agents / "manager"
        mgr.mkdir()
        (mgr / "system-prompt.md").write_text("You are Manager.")
        manifest = mgr / "context-manifest.md"
        manifest.write_text(
            "# Manager — Context Manifest\n\n"
            "## Firm Documents (yolo-firm/)\n\n"
            "| Document | Path | Purpose |\n"
            "|---|---|---|\n"
            "| RACI | `raci.md` | Roles |\n",
        )
        # Create firm doc
        (tmp_path / "raci.md").write_text("# RACI\nRoles here.")
        return agents

    def test_loads_system_prompt(self, agent_tree: Path) -> None:
        firm_repo = agent_tree.parent
        yolo_repo = agent_tree.parent / "yolo"
        yolo_repo.mkdir(exist_ok=True)
        prompt, docs, missing, memory = load_agent_context(
            "manager", agent_tree, firm_repo, yolo_repo,
        )
        assert "You are Manager" in prompt

    def test_loads_context_docs(self, agent_tree: Path) -> None:
        firm_repo = agent_tree.parent
        yolo_repo = agent_tree.parent / "yolo"
        yolo_repo.mkdir(exist_ok=True)
        _, docs, missing, _ = load_agent_context(
            "manager", agent_tree, firm_repo, yolo_repo,
        )
        assert len(docs) >= 1
        assert missing == []

    def test_returns_none_memory_when_no_file(self, agent_tree: Path) -> None:
        firm_repo = agent_tree.parent
        yolo_repo = agent_tree.parent / "yolo"
        yolo_repo.mkdir(exist_ok=True)
        _, _, _, memory = load_agent_context(
            "manager", agent_tree, firm_repo, yolo_repo,
        )
        assert memory is None

    def test_loads_memory_when_present(self, agent_tree: Path) -> None:
        (agent_tree / "manager" / "memory.md").write_text("# Memory\n- fact 1")
        firm_repo = agent_tree.parent
        yolo_repo = agent_tree.parent / "yolo"
        yolo_repo.mkdir(exist_ok=True)
        _, _, _, memory = load_agent_context(
            "manager", agent_tree, firm_repo, yolo_repo,
        )
        assert memory is not None
        assert "fact 1" in memory

    def test_missing_system_prompt_raises(self, tmp_path: Path) -> None:
        agents = tmp_path / "agents"
        agents.mkdir()
        (agents / "manager").mkdir()
        # No system-prompt.md
        with pytest.raises(FileNotFoundError):
            load_agent_context(
                "manager", agents, tmp_path, tmp_path / "yolo",
            )


class TestRunSession:
    """Integration tests for the full session flow (mocks API)."""

    @pytest.fixture
    def session_env(self, tmp_path: Path) -> dict:
        """Create a full agent tree for session tests."""
        agents = tmp_path / "agents"
        agents.mkdir()
        log_dir = agents / "session-log"
        log_dir.mkdir()

        for agent in ("manager", "analyst", "engineer"):
            d = agents / agent
            d.mkdir()
            (d / "system-prompt.md").write_text(f"You are {agent.title()}.")
            (d / "context-manifest.md").write_text(
                f"# {agent.title()} — Context Manifest\n\n"
                "## Firm Documents (yolo-firm/)\n\n"
                "| Document | Path | Purpose |\n"
                "|---|---|---|\n"
                "| RACI | `raci.md` | Roles |\n",
            )

        # Firm docs
        (tmp_path / "raci.md").write_text("# RACI\nRoles.")
        # Yolo repo
        (tmp_path / "yolo").mkdir()

        return {
            "agents_dir": agents,
            "firm_repo": tmp_path,
            "yolo_repo": tmp_path / "yolo",
            "log_dir": log_dir,
        }

    def _mock_api_response(self, text: str, input_tokens: int = 100, output_tokens: int = 50):
        """Create a mock Anthropic API response."""
        mock = MagicMock()
        mock.content = [MagicMock(text=text)]
        mock.usage = MagicMock(input_tokens=input_tokens, output_tokens=output_tokens)
        return mock

    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_question_mode_routes_dynamically(
        self, mock_create: MagicMock, mock_ensure: MagicMock, session_env: dict,
    ) -> None:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.side_effect = [
            self._mock_api_response("Opening. [NEXT: analyst]"),
            self._mock_api_response("Analysis done."),
            self._mock_api_response("Closing. [SESSION_COMPLETE]"),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            result = run_session(
                question="Test question",
                open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="test-session",
                dry_run=False,
            )

        assert mock_client.messages.create.call_count == 3
        assert isinstance(result, SessionResult)
        assert result.session_id == "test-session"
        assert result.outcome == "complete"
        assert result.input_tokens > 0
        assert result.cost_usd > 0

    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_open_mode_sends_meta_question(
        self, mock_create: MagicMock, mock_ensure: MagicMock, session_env: dict,
    ) -> None:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.return_value = self._mock_api_response(
            "Response. [SESSION_COMPLETE]",
        )

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            run_session(
                question=None,
                open_mode=True,
                model="claude-haiku-4-5-20251001",
                session_id="test-open",
                dry_run=False,
            )

        first_call = mock_client.messages.create.call_args_list[0]
        first_message = first_call.kwargs.get("messages") or first_call[1].get("messages")
        user_msg = first_message[0]["content"]
        assert "what question" in user_msg.lower() or "investigate" in user_msg.lower()

    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_session_log_created_with_all_turns(
        self, mock_create: MagicMock, mock_ensure: MagicMock, session_env: dict,
    ) -> None:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.side_effect = [
            self._mock_api_response("Manager opens. [NEXT: analyst]"),
            self._mock_api_response("Analyst responds."),
            self._mock_api_response("Manager closes. [SESSION_COMPLETE]"),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            run_session(
                question="Test",
                open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="log-test",
                dry_run=False,
            )

        log_files = list(session_env["log_dir"].glob("*.md"))
        assert len(log_files) == 1
        content = log_files[0].read_text()
        assert "Manager opens." in content
        assert "Analyst responds." in content
        assert "Manager closes." in content

    def test_dry_run_skips_api_calls(self, session_env: dict) -> None:
        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            result = run_session(
                question="Test",
                open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="dry-test",
                dry_run=True,
            )
        assert isinstance(result, SessionResult)
        assert result.outcome == "dry_run"
        assert result.input_tokens == 0

    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_memory_updates_collected(
        self, mock_create: MagicMock, mock_ensure: MagicMock, session_env: dict,
    ) -> None:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.side_effect = [
            self._mock_api_response("Manager opens. [NEXT: analyst]"),
            self._mock_api_response(
                "Analysis.\n\n[MEMORY UPDATE]\n- New finding: X\n",
            ),
            self._mock_api_response("Manager closes. [SESSION_COMPLETE]"),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            run_session(
                question="Test",
                open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="memory-test",
                dry_run=False,
            )

        # Verify memory-pending.md was written
        pending = session_env["agents_dir"] / "memory-pending.md"
        assert pending.exists()
        content = pending.read_text()
        assert "New finding: X" in content


class TestServerLifecycle:
    """Tests for WebSocket server lifecycle management."""

    def test_is_server_running_returns_false_when_port_closed(self) -> None:
        # Port 18999 should not be in use
        assert is_server_running(port=18999) is False

    @patch("session.socket")
    def test_is_server_running_returns_true_when_connected(
        self, mock_socket_mod: MagicMock,
    ) -> None:
        mock_sock = MagicMock()
        mock_socket_mod.socket.return_value = mock_sock
        mock_sock.connect_ex.return_value = 0

        assert is_server_running(port=8003) is True
        mock_sock.close.assert_called()

    @patch("session.socket")
    def test_is_server_running_returns_false_when_refused(
        self, mock_socket_mod: MagicMock,
    ) -> None:
        mock_sock = MagicMock()
        mock_socket_mod.socket.return_value = mock_sock
        mock_sock.connect_ex.return_value = 111  # Connection refused

        assert is_server_running(port=8003) is False
        mock_sock.close.assert_called()


class TestCheckInterrupt:
    """Tests for session interrupt flag checking."""

    def test_returns_none_when_no_flag(self, tmp_path: Path) -> None:
        with patch("session.INTERRUPT_FLAG", tmp_path / "nonexistent.flag"):
            assert check_interrupt() is None

    def test_returns_pause_when_flag_contains_pause(self, tmp_path: Path) -> None:
        flag = tmp_path / "session-interrupt.flag"
        flag.write_text("pause")
        with patch("session.INTERRUPT_FLAG", flag):
            assert check_interrupt() == "pause"

    def test_returns_cancel_when_flag_contains_cancel(self, tmp_path: Path) -> None:
        flag = tmp_path / "session-interrupt.flag"
        flag.write_text("cancel")
        with patch("session.INTERRUPT_FLAG", flag):
            assert check_interrupt() == "cancel"

    def test_strips_whitespace(self, tmp_path: Path) -> None:
        flag = tmp_path / "session-interrupt.flag"
        flag.write_text("  pause  \n")
        with patch("session.INTERRUPT_FLAG", flag):
            assert check_interrupt() == "pause"


class TestWriteReviewDoc:
    """Tests for PO review document generation."""

    def test_review_doc_created_after_session(self, tmp_path: Path) -> None:
        """Review file is created in the reviews directory."""
        reviews_dir = tmp_path / "reviews"
        log_path = tmp_path / "session-log" / "2026-03-06-test-session.md"
        log_path.parent.mkdir(parents=True)
        log_path.write_text("# Session: test-session\n")

        result = write_review_doc(
            reviews_dir=reviews_dir,
            session_id="test-session",
            model="claude-haiku-4-5-20251001",
            manager_close_response="## Synthesis\nKey findings here.",
            log_path=log_path,
        )

        assert result.exists()
        assert result.parent == reviews_dir

    def test_review_doc_filename_format(self, tmp_path: Path) -> None:
        """Review filename follows YYYY-MM-DD-{session-id}-review.md pattern."""
        reviews_dir = tmp_path / "reviews"
        log_path = tmp_path / "log.md"
        log_path.write_text("# Log\n")

        result = write_review_doc(
            reviews_dir=reviews_dir,
            session_id="vwap-audit",
            model="claude-haiku-4-5-20251001",
            manager_close_response="Synthesis.",
            log_path=log_path,
        )

        assert re.match(r"\d{4}-\d{2}-\d{2}-vwap-audit-review\.md", result.name)

    def test_review_doc_contains_manager_close_response(self, tmp_path: Path) -> None:
        """Review doc includes the Manager synthesis text."""
        reviews_dir = tmp_path / "reviews"
        log_path = tmp_path / "log.md"
        log_path.write_text("# Log\n")

        synthesis = "## Key Findings\n\n1. RSI works well\n2. VWAP needs tuning"
        result = write_review_doc(
            reviews_dir=reviews_dir,
            session_id="test-123",
            model="claude-haiku-4-5-20251001",
            manager_close_response=synthesis,
            log_path=log_path,
        )

        content = result.read_text()
        assert "RSI works well" in content
        assert "VWAP needs tuning" in content
        assert "test-123" in content

    def test_review_doc_creates_directory_if_missing(self, tmp_path: Path) -> None:
        """Reviews directory is auto-created if it doesn't exist."""
        reviews_dir = tmp_path / "nonexistent" / "reviews"
        log_path = tmp_path / "log.md"
        log_path.write_text("# Log\n")

        assert not reviews_dir.exists()

        result = write_review_doc(
            reviews_dir=reviews_dir,
            session_id="dir-test",
            model="claude-haiku-4-5-20251001",
            manager_close_response="Synthesis.",
            log_path=log_path,
        )

        assert reviews_dir.exists()
        assert result.exists()

    def test_review_link_appended_to_session_log(self, tmp_path: Path) -> None:
        """Review file path is appended to the session log."""
        reviews_dir = tmp_path / "reviews"
        log_path = tmp_path / "session-log" / "2026-03-06-link-test.md"
        log_path.parent.mkdir(parents=True)
        log_path.write_text("# Session: link-test\n\nSome content.\n")

        result = write_review_doc(
            reviews_dir=reviews_dir,
            session_id="link-test",
            model="claude-haiku-4-5-20251001",
            manager_close_response="Synthesis.",
            log_path=log_path,
        )

        log_content = log_path.read_text()
        assert result.name in log_content
        assert "Review:" in log_content


class TestInvokeAgentToolUse:
    """Tests for tool use support in invoke_agent."""

    def _make_tool_use_response(
        self, tool_name: str, tool_input: dict, tool_id: str = "toolu_01",
        input_tokens: int = 100, output_tokens: int = 50,
    ) -> MagicMock:
        """Create a mock API response with a tool_use block."""
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = "Let me run a backtest."

        tool_block = MagicMock()
        tool_block.type = "tool_use"
        tool_block.name = tool_name
        tool_block.input = tool_input
        tool_block.id = tool_id

        resp = MagicMock()
        resp.content = [text_block, tool_block]
        resp.stop_reason = "tool_use"
        resp.usage = MagicMock(input_tokens=input_tokens, output_tokens=output_tokens)
        return resp

    def _make_text_response(
        self, text: str, input_tokens: int = 80, output_tokens: int = 40,
    ) -> MagicMock:
        """Create a mock API response with only text."""
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = text

        resp = MagicMock()
        resp.content = [text_block]
        resp.stop_reason = "end_turn"
        resp.usage = MagicMock(input_tokens=input_tokens, output_tokens=output_tokens)
        return resp

    def test_tool_use_dispatches_and_returns_final_text(self) -> None:
        """When API returns tool_use, the tool is called and final text is returned."""
        mock_backtest = MagicMock(return_value={
            "strategy_id": "HYP-TEST", "trade_count": 60,
            "inconclusive": False, "win_rate": 0.55,
            "summary": "60 trades. Win rate: 55.0%",
        })

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [
            self._make_tool_use_response(
                "run_backtest",
                {"strategy_id": "HYP-TEST", "tickers": ["MOBX"], "dates": ["2026-03-03"],
                 "entry_rules": [], "exit_rules": []},
            ),
            self._make_text_response("Backtest complete: 60 trades, 55% win rate."),
        ]

        tools = [{"name": "run_backtest", "description": "Run backtest",
                  "input_schema": {"type": "object", "properties": {}}}]

        with patch.dict("session.TOOL_DISPATCH", {"run_backtest": mock_backtest}):
            result = invoke_agent(
                client=mock_client, agent="engineer", message="Run test",
                system_prompt="You are Engineer.", docs=[], memory=None,
                model="claude-haiku-4-5-20251001", tools=tools,
            )

        mock_backtest.assert_called_once()
        assert "60 trades" in result.response
        assert mock_client.messages.create.call_count == 2

    def test_tool_use_accumulates_tokens(self) -> None:
        """Token counts include both the initial call and the tool result call."""
        mock_backtest = MagicMock(return_value={"strategy_id": "T", "trade_count": 10})

        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [
            self._make_tool_use_response(
                "run_backtest", {"strategy_id": "T", "tickers": [], "dates": [],
                                 "entry_rules": [], "exit_rules": []},
                input_tokens=200, output_tokens=100,
            ),
            self._make_text_response("Done.", input_tokens=300, output_tokens=150),
        ]

        tools = [{"name": "run_backtest", "description": "x",
                  "input_schema": {"type": "object", "properties": {}}}]

        with patch.dict("session.TOOL_DISPATCH", {"run_backtest": mock_backtest}):
            result = invoke_agent(
                client=mock_client, agent="engineer", message="Test",
                system_prompt="S", docs=[], memory=None,
                model="claude-haiku-4-5-20251001", tools=tools,
            )

        assert result.input_tokens == 500   # 200 + 300
        assert result.output_tokens == 250  # 100 + 150

    def test_no_tools_works_as_before(self) -> None:
        """invoke_agent without tools parameter behaves unchanged."""
        mock_client = MagicMock()
        mock_client.messages.create.return_value = self._make_text_response(
            "Simple response.",
        )

        result = invoke_agent(
            client=mock_client, agent="analyst", message="Analyse this",
            system_prompt="You are Analyst.", docs=[], memory=None,
            model="claude-haiku-4-5-20251001",
        )

        assert result.response == "Simple response."
        assert mock_client.messages.create.call_count == 1
        # Verify no 'tools' key in the API call
        call_kwargs = mock_client.messages.create.call_args
        assert "tools" not in (call_kwargs.kwargs or {})


class TestParseNextAgent:
    """Tests for _parse_next_agent tag extraction."""

    def test_extracts_analyst(self) -> None:
        from session import _parse_next_agent
        assert _parse_next_agent("Some text [NEXT: analyst] more text") == "analyst"

    def test_extracts_engineer(self) -> None:
        from session import _parse_next_agent
        assert _parse_next_agent("Result [NEXT: engineer]") == "engineer"

    def test_extracts_manager(self) -> None:
        from session import _parse_next_agent
        assert _parse_next_agent("[NEXT: manager]") == "manager"

    def test_case_insensitive(self) -> None:
        from session import _parse_next_agent
        assert _parse_next_agent("[NEXT: Analyst]") == "analyst"
        assert _parse_next_agent("[NEXT: ENGINEER]") == "engineer"

    def test_strips_whitespace(self) -> None:
        from session import _parse_next_agent
        assert _parse_next_agent("[NEXT:  analyst  ]") == "analyst"

    def test_returns_none_when_no_tag(self) -> None:
        from session import _parse_next_agent
        assert _parse_next_agent("No routing tag here.") is None

    def test_invalid_agent_returns_none(self) -> None:
        from session import _parse_next_agent
        assert _parse_next_agent("[NEXT: hacker]") is None


class TestDynamicSession:
    """Tests for dynamic routing session loop."""

    @pytest.fixture
    def session_env(self, tmp_path: Path) -> dict:
        """Create a full agent tree for session tests."""
        agents = tmp_path / "agents"
        agents.mkdir()
        log_dir = agents / "session-log"
        log_dir.mkdir()

        for agent in ("manager", "analyst", "engineer"):
            d = agents / agent
            d.mkdir()
            (d / "system-prompt.md").write_text(f"You are {agent.title()}.")
            (d / "context-manifest.md").write_text(
                f"# {agent.title()} — Context Manifest\n\n"
                "## Firm Documents (yolo-firm/)\n\n"
                "| Document | Path | Purpose |\n"
                "|---|---|---|\n"
                "| RACI | `raci.md` | Roles |\n",
            )

        (tmp_path / "raci.md").write_text("# RACI\nRoles.")
        (tmp_path / "yolo").mkdir()

        return {
            "agents_dir": agents,
            "firm_repo": tmp_path,
            "yolo_repo": tmp_path / "yolo",
            "log_dir": log_dir,
        }

    def _mock_api_response(self, text: str, input_tokens: int = 100, output_tokens: int = 50):
        """Create a mock Anthropic API response."""
        mock = MagicMock()
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = text
        mock.content = [text_block]
        mock.stop_reason = "end_turn"
        mock.usage = MagicMock(input_tokens=input_tokens, output_tokens=output_tokens)
        return mock

    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_session_closes_on_tag(
        self, mock_create: MagicMock, mock_ensure: MagicMock, session_env: dict,
    ) -> None:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        # Manager opens then immediately closes
        mock_client.messages.create.side_effect = [
            self._mock_api_response("Session opened. [SESSION_COMPLETE]"),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            run_session(
                question="Test", open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="close-test", dry_run=False,
            )

        assert mock_client.messages.create.call_count == 1

    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_session_routes_on_next_tag(
        self, mock_create: MagicMock, mock_ensure: MagicMock, session_env: dict,
    ) -> None:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.side_effect = [
            self._mock_api_response("Opening. [NEXT: analyst]"),
            self._mock_api_response("Analysis done."),  # analyst turn routes back to manager
            self._mock_api_response("Closing. [SESSION_COMPLETE]"),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            run_session(
                question="Test", open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="route-test", dry_run=False,
            )

        assert mock_client.messages.create.call_count == 3

    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_session_force_closes_at_turn_limit(
        self, mock_create: MagicMock, mock_ensure: MagicMock, session_env: dict,
    ) -> None:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        # Manager keeps routing to analyst forever
        mock_client.messages.create.return_value = self._mock_api_response(
            "Continuing. [NEXT: analyst]",
        )

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            run_session(
                question="Test", open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="limit-test", dry_run=False,
                max_turns=5,
            )

        assert mock_client.messages.create.call_count == 5

    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_invalid_next_agent_defaults_to_manager(
        self, mock_create: MagicMock, mock_ensure: MagicMock, session_env: dict,
    ) -> None:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.side_effect = [
            self._mock_api_response("Opening. [NEXT: hacker]"),  # invalid → manager
            self._mock_api_response("Closing. [SESSION_COMPLETE]"),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            run_session(
                question="Test", open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="default-test", dry_run=False,
            )

        # Second call should be manager (default fallback)
        assert mock_client.messages.create.call_count == 2

    def test_dry_run_still_works(self, session_env: dict) -> None:
        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            result = run_session(
                question="Test", open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="dry-test-2", dry_run=True,
            )
        assert result.outcome == "dry_run"


class TestBlockerAndScopeRequest:
    """Tests for [BLOCKER:] and [SCOPE REQUEST:] tag detection."""

    @pytest.fixture
    def session_env(self, tmp_path: Path) -> dict:
        """Create a full agent tree for session tests."""
        agents = tmp_path / "agents"
        agents.mkdir()
        log_dir = agents / "session-log"
        log_dir.mkdir()

        for agent in ("manager", "analyst", "engineer"):
            d = agents / agent
            d.mkdir()
            (d / "system-prompt.md").write_text(f"You are {agent.title()}.")
            (d / "context-manifest.md").write_text(
                f"# {agent.title()} — Context Manifest\n\n"
                "## Firm Documents (yolo-firm/)\n\n"
                "| Document | Path | Purpose |\n"
                "|---|---|---|\n"
                "| RACI | `raci.md` | Roles |\n",
            )

        (tmp_path / "raci.md").write_text("# RACI\nRoles.")
        (tmp_path / "yolo").mkdir()

        return {
            "agents_dir": agents,
            "firm_repo": tmp_path,
            "yolo_repo": tmp_path / "yolo",
            "log_dir": log_dir,
        }

    def _mock_api_response(self, text: str, input_tokens: int = 100, output_tokens: int = 50):
        """Create a mock Anthropic API response."""
        mock = MagicMock()
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = text
        mock.content = [text_block]
        mock.stop_reason = "end_turn"
        mock.usage = MagicMock(input_tokens=input_tokens, output_tokens=output_tokens)
        return mock

    @patch("session.send_pushover", return_value=True)
    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_blocker_tag_writes_flag(
        self, mock_create: MagicMock, mock_ensure: MagicMock,
        mock_pushover: MagicMock, session_env: dict,
    ) -> None:
        """[BLOCKER:] tag writes blocker.flag and ends session."""
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.side_effect = [
            self._mock_api_response(
                "Cannot proceed. [BLOCKER: ema_gap_acceleration indicator missing]",
            ),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            result = run_session(
                question="Test", open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="blocker-test", dry_run=False,
            )

        assert result.outcome == "blocker"
        flag_path = session_env["agents_dir"] / "blocker.flag"
        assert flag_path.exists()
        assert "ema_gap_acceleration" in flag_path.read_text()

    @patch("session.send_pushover", return_value=True)
    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_blocker_tag_triggers_notification(
        self, mock_create: MagicMock, mock_ensure: MagicMock,
        mock_pushover: MagicMock, session_env: dict,
    ) -> None:
        """[BLOCKER:] tag sends high-priority Pushover notification."""
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.side_effect = [
            self._mock_api_response("[BLOCKER: Missing data for HYP-026]"),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            run_session(
                question="Test", open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="blocker-notify", dry_run=False,
            )

        mock_pushover.assert_called_once()
        call_kwargs = mock_pushover.call_args
        assert call_kwargs[1].get("priority") == 1 or call_kwargs[0][2] == 1

    @patch("session.send_pushover", return_value=True)
    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_scope_request_tag_writes_flag(
        self, mock_create: MagicMock, mock_ensure: MagicMock,
        mock_pushover: MagicMock, session_env: dict,
    ) -> None:
        """[SCOPE REQUEST:] writes scope-request.flag but continues session."""
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.side_effect = [
            self._mock_api_response(
                "Interesting finding. [SCOPE REQUEST: Test squeeze indicators] "
                "[NEXT: analyst]",
            ),
            self._mock_api_response("Analysis."),
            self._mock_api_response("Closing. [SESSION_COMPLETE]"),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            result = run_session(
                question="Test", open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="scope-test", dry_run=False,
            )

        # Session continues (3 API calls, not 1)
        assert mock_client.messages.create.call_count == 3
        assert result.outcome == "complete"
        flag_path = session_env["agents_dir"] / "scope-request.flag"
        assert flag_path.exists()
        assert "squeeze indicators" in flag_path.read_text()

    @patch("session.send_pushover", return_value=True)
    @patch("session.ensure_server_running", return_value=False)
    @patch("session.create_client")
    def test_scope_request_blocking_stops_session(
        self, mock_create: MagicMock, mock_ensure: MagicMock,
        mock_pushover: MagicMock, session_env: dict,
    ) -> None:
        """[SCOPE REQUEST BLOCKING:] writes flag and ends session."""
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.messages.create.side_effect = [
            self._mock_api_response(
                "[SCOPE REQUEST BLOCKING: Need live data feed for validation]",
            ),
        ]

        with patch("session.AGENTS_DIR", session_env["agents_dir"]), \
             patch("session.FIRM_REPO", session_env["firm_repo"]), \
             patch("session.YOLO_REPO", session_env["yolo_repo"]):
            result = run_session(
                question="Test", open_mode=False,
                model="claude-haiku-4-5-20251001",
                session_id="scope-block", dry_run=False,
            )

        assert result.outcome == "blocker"
        assert mock_client.messages.create.call_count == 1
        flag_path = session_env["agents_dir"] / "scope-request.flag"
        assert flag_path.exists()
