"""Unit tests for streaming invocation in session.py."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock


sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from session import (
    TurnResult,
    invoke_agent,
    invoke_agent_streaming,
    send_to_ws,
)


class TestInvokeAgentStreaming:
    """Tests for streaming agent invocation."""

    def _mock_stream_context(self, text: str, input_tokens: int = 100, output_tokens: int = 50):
        """Create a mock streaming context manager."""
        # Mock the stream context manager
        stream = MagicMock()

        # Mock text_stream iterator
        stream.text_stream = iter(list(text))  # yield char by char
        stream.get_final_message.return_value = MagicMock(
            content=[MagicMock(text=text)],
            usage=MagicMock(input_tokens=input_tokens, output_tokens=output_tokens),
        )

        # Make it work as context manager
        ctx = MagicMock()
        ctx.__enter__ = MagicMock(return_value=stream)
        ctx.__exit__ = MagicMock(return_value=False)
        return ctx

    def test_uses_stream_api(self) -> None:
        mock_client = MagicMock()
        mock_client.messages.stream.return_value = self._mock_stream_context("Response.")

        result = invoke_agent_streaming(
            client=mock_client,
            agent="analyst",
            message="test",
            system_prompt="You are Analyst.",
            docs=[],
            memory=None,
            model="claude-haiku-4-5-20251001",
        )

        mock_client.messages.stream.assert_called_once()
        mock_client.messages.create.assert_not_called()
        assert isinstance(result, TurnResult)

    def test_captures_full_response(self) -> None:
        mock_client = MagicMock()
        mock_client.messages.stream.return_value = self._mock_stream_context("Full response text.")

        result = invoke_agent_streaming(
            client=mock_client,
            agent="analyst",
            message="test",
            system_prompt="You are Analyst.",
            docs=[],
            memory=None,
            model="claude-haiku-4-5-20251001",
        )

        assert result.response == "Full response text."

    def test_tracks_token_counts(self) -> None:
        mock_client = MagicMock()
        mock_client.messages.stream.return_value = self._mock_stream_context(
            "Response.", input_tokens=500, output_tokens=200,
        )

        result = invoke_agent_streaming(
            client=mock_client,
            agent="analyst",
            message="test",
            system_prompt="You are Analyst.",
            docs=[],
            memory=None,
            model="claude-haiku-4-5-20251001",
        )

        assert result.input_tokens == 500
        assert result.output_tokens == 200

    def test_sends_tokens_to_ws(self) -> None:
        mock_client = MagicMock()
        mock_client.messages.stream.return_value = self._mock_stream_context("Hi")

        mock_ws = MagicMock()

        invoke_agent_streaming(
            client=mock_client,
            agent="analyst",
            message="test",
            system_prompt="You are Analyst.",
            docs=[],
            memory=None,
            model="claude-haiku-4-5-20251001",
            ws_conn=mock_ws,
        )

        # Should have sent: system "Turn: analyst" + tokens + cost
        calls = mock_ws.send.call_args_list
        assert len(calls) >= 4  # system + "H" + "i" + cost
        # First is system turn notification
        first_msg = json.loads(calls[0][0][0])
        assert first_msg["type"] == "system"
        # Second is first token
        token_msg = json.loads(calls[1][0][0])
        assert token_msg["type"] == "token"
        assert token_msg["speaker"] == "analyst"

    def test_no_ws_conn_still_works(self) -> None:
        mock_client = MagicMock()
        mock_client.messages.stream.return_value = self._mock_stream_context("Response.")

        # ws_conn=None should not crash
        result = invoke_agent_streaming(
            client=mock_client,
            agent="analyst",
            message="test",
            system_prompt="You are Analyst.",
            docs=[],
            memory=None,
            model="claude-haiku-4-5-20251001",
            ws_conn=None,
        )

        assert result.response == "Response."

    def test_ws_send_failure_does_not_crash(self) -> None:
        mock_client = MagicMock()
        mock_client.messages.stream.return_value = self._mock_stream_context("Hi")

        mock_ws = MagicMock()
        mock_ws.send.side_effect = Exception("connection lost")

        # Should not raise despite WS failure
        result = invoke_agent_streaming(
            client=mock_client,
            agent="analyst",
            message="test",
            system_prompt="You are Analyst.",
            docs=[],
            memory=None,
            model="claude-haiku-4-5-20251001",
            ws_conn=mock_ws,
        )

        assert result.response == "Hi"

    def test_includes_transcript_in_message(self) -> None:
        mock_client = MagicMock()
        mock_client.messages.stream.return_value = self._mock_stream_context("Response.")

        invoke_agent_streaming(
            client=mock_client,
            agent="analyst",
            message="Your turn",
            system_prompt="You are Analyst.",
            docs=[],
            memory=None,
            model="claude-haiku-4-5-20251001",
            transcript="**Manager:** Session opened.",
        )

        call_kwargs = mock_client.messages.stream.call_args.kwargs
        user_msg = call_kwargs["messages"][0]["content"]
        assert "Session opened" in user_msg
        assert "Your turn" in user_msg


class TestInvokeAgentBlocking:
    """Verify existing blocking path is unchanged."""

    def test_blocking_uses_create(self) -> None:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Blocking response.")]
        mock_response.usage = MagicMock(input_tokens=100, output_tokens=50)
        mock_client.messages.create.return_value = mock_response

        result = invoke_agent(
            client=mock_client,
            agent="analyst",
            message="test",
            system_prompt="You are Analyst.",
            docs=[],
            memory=None,
            model="claude-haiku-4-5-20251001",
        )

        mock_client.messages.create.assert_called_once()
        assert result.response == "Blocking response."


class TestSendToWs:
    """Tests for WebSocket send helper."""

    def test_sends_json(self) -> None:
        mock_ws = MagicMock()
        msg = {"type": "token", "speaker": "analyst", "content": "hi"}
        send_to_ws(mock_ws, msg)
        mock_ws.send.assert_called_once_with(json.dumps(msg))

    def test_none_ws_no_crash(self) -> None:
        send_to_ws(None, {"type": "test"})  # Should not raise

    def test_send_failure_no_crash(self) -> None:
        mock_ws = MagicMock()
        mock_ws.send.side_effect = Exception("broken")
        send_to_ws(mock_ws, {"type": "test"})  # Should not raise
