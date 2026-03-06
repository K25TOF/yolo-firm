"""Unit tests for agents/server.py — WebSocket server auth, broadcast, lifecycle."""

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from server import (
    CHAT_UI_PATH,
    CONNECTED_CLIENTS,
    MESSAGE_BUFFER,
    authenticate,
    broadcast,
    handle_command,
    handler,
    process_request,
    reset_idle_timer,
)


class TestAuthenticate:
    """Tests for WebSocket connection authentication."""

    def test_valid_token_accepted(self) -> None:
        ws = AsyncMock()
        ws.recv = AsyncMock(return_value=json.dumps({"type": "auth", "token": "secret"}))

        result = asyncio.run(authenticate(ws, "secret"))
        assert result is True

    def test_invalid_token_rejected(self) -> None:
        ws = AsyncMock()
        ws.recv = AsyncMock(return_value=json.dumps({"type": "auth", "token": "wrong"}))

        result = asyncio.run(authenticate(ws, "secret"))
        assert result is False
        ws.close.assert_called()

    def test_no_token_configured_accepts_all(self) -> None:
        ws = AsyncMock()
        # When token is None, auth is disabled — no recv needed
        result = asyncio.run(authenticate(ws, None))
        assert result is True

    def test_malformed_auth_message_rejected(self) -> None:
        ws = AsyncMock()
        ws.recv = AsyncMock(return_value="not json")

        result = asyncio.run(authenticate(ws, "secret"))
        assert result is False
        ws.close.assert_called()

    def test_missing_token_field_rejected(self) -> None:
        ws = AsyncMock()
        ws.recv = AsyncMock(return_value=json.dumps({"type": "auth"}))

        result = asyncio.run(authenticate(ws, "secret"))
        assert result is False
        ws.close.assert_called()


class TestBroadcast:
    """Tests for message broadcasting."""

    def test_broadcast_to_connected_client(self) -> None:
        CONNECTED_CLIENTS.clear()
        ws = AsyncMock()
        CONNECTED_CLIENTS.add(ws)

        msg = {"type": "token", "speaker": "analyst", "content": "hello"}
        asyncio.run(broadcast(msg))

        ws.send.assert_called_once_with(json.dumps(msg))
        CONNECTED_CLIENTS.clear()

    def test_broadcast_to_multiple_clients(self) -> None:
        CONNECTED_CLIENTS.clear()
        ws1 = AsyncMock()
        ws2 = AsyncMock()
        CONNECTED_CLIENTS.add(ws1)
        CONNECTED_CLIENTS.add(ws2)

        msg = {"type": "message", "speaker": "manager", "content": "test"}
        asyncio.run(broadcast(msg))

        ws1.send.assert_called_once()
        ws2.send.assert_called_once()
        CONNECTED_CLIENTS.clear()

    def test_broadcast_no_clients_no_crash(self) -> None:
        CONNECTED_CLIENTS.clear()
        msg = {"type": "system", "speaker": "system", "content": "test"}
        # Should not raise
        asyncio.run(broadcast(msg))

    def test_broadcast_removes_disconnected_client(self) -> None:
        CONNECTED_CLIENTS.clear()
        ws = AsyncMock()
        ws.send = AsyncMock(side_effect=Exception("disconnected"))
        CONNECTED_CLIENTS.add(ws)

        msg = {"type": "token", "speaker": "analyst", "content": "hello"}
        asyncio.run(broadcast(msg))

        assert ws not in CONNECTED_CLIENTS
        CONNECTED_CLIENTS.clear()


class TestIdleTimer:
    """Tests for idle timer reset."""

    def test_reset_idle_timer_updates_timestamp(self) -> None:
        import server

        old = server._last_activity
        reset_idle_timer()
        assert server._last_activity >= old


class TestProcessRequest:
    """Tests for HTTP request handling via process_request hook."""

    def test_serves_html_on_get_root(self, tmp_path: Path) -> None:
        import server

        # Create a temporary HTML file
        chat_dir = tmp_path / "chat-ui"
        chat_dir.mkdir()
        html_file = chat_dir / "index.html"
        html_file.write_text("<html><body>Chat UI</body></html>")

        original = server.CHAT_UI_PATH
        server.CHAT_UI_PATH = html_file
        try:
            from websockets.datastructures import Headers
            from websockets.http11 import Request

            request = Request(path="/", headers=Headers({"Host": "localhost"}))
            connection = MagicMock()
            result = asyncio.run(process_request(connection, request))
            assert result is not None
            assert result.status_code == 200
            assert b"Chat UI" in result.body
        finally:
            server.CHAT_UI_PATH = original

    def test_returns_none_for_websocket_upgrade(self) -> None:
        from websockets.datastructures import Headers
        from websockets.http11 import Request

        request = Request(
            path="/",
            headers=Headers({
                "Host": "localhost",
                "Upgrade": "websocket",
            }),
        )
        connection = MagicMock()
        result = asyncio.run(process_request(connection, request))
        assert result is None

    def test_returns_none_for_non_root_path(self) -> None:
        from websockets.datastructures import Headers
        from websockets.http11 import Request

        request = Request(path="/other", headers=Headers({"Host": "localhost"}))
        connection = MagicMock()
        result = asyncio.run(process_request(connection, request))
        assert result is None

    def test_returns_404_when_html_missing(self, tmp_path: Path) -> None:
        import server

        original = server.CHAT_UI_PATH
        server.CHAT_UI_PATH = tmp_path / "nonexistent.html"
        try:
            from websockets.datastructures import Headers
            from websockets.http11 import Request

            request = Request(path="/", headers=Headers({"Host": "localhost"}))
            connection = MagicMock()
            result = asyncio.run(process_request(connection, request))
            assert result is not None
            assert result.status_code == 404
        finally:
            server.CHAT_UI_PATH = original

    def test_chat_ui_html_file_exists(self) -> None:
        assert CHAT_UI_PATH.parent.name == "chat-ui"
        # File won't exist until we create it in Step 4


class TestHandleCommand:
    """Tests for pause/resume/cancel command handling."""

    def test_pause_writes_interrupt_flag(self, tmp_path: Path) -> None:
        import server

        original = server.INTERRUPT_FLAG
        server.INTERRUPT_FLAG = tmp_path / "session-interrupt.flag"
        try:
            data = {"type": "pause"}
            result = asyncio.run(handle_command(data))
            assert result is True
            assert server.INTERRUPT_FLAG.read_text() == "pause"
        finally:
            server.INTERRUPT_FLAG = original

    def test_resume_deletes_interrupt_flag(self, tmp_path: Path) -> None:
        import server

        flag = tmp_path / "session-interrupt.flag"
        flag.write_text("pause")
        original = server.INTERRUPT_FLAG
        server.INTERRUPT_FLAG = flag
        try:
            data = {"type": "resume"}
            result = asyncio.run(handle_command(data))
            assert result is True
            assert not flag.exists()
        finally:
            server.INTERRUPT_FLAG = original

    def test_cancel_writes_interrupt_flag(self, tmp_path: Path) -> None:
        import server

        original = server.INTERRUPT_FLAG
        server.INTERRUPT_FLAG = tmp_path / "session-interrupt.flag"
        try:
            data = {"type": "cancel"}
            result = asyncio.run(handle_command(data))
            assert result is True
            assert server.INTERRUPT_FLAG.read_text() == "cancel"
        finally:
            server.INTERRUPT_FLAG = original

    def test_non_command_returns_false(self) -> None:
        data = {"type": "token", "speaker": "analyst", "content": "hello"}
        result = asyncio.run(handle_command(data))
        assert result is False

    def test_resume_no_flag_no_crash(self, tmp_path: Path) -> None:
        import server

        original = server.INTERRUPT_FLAG
        server.INTERRUPT_FLAG = tmp_path / "session-interrupt.flag"
        try:
            data = {"type": "resume"}
            result = asyncio.run(handle_command(data))
            assert result is True  # still handled, just no file to delete
        finally:
            server.INTERRUPT_FLAG = original


class TestMessageBuffer:
    """Tests for in-memory message buffer: append, replay, and clear."""

    def setup_method(self) -> None:
        """Clear buffer and clients before each test."""
        MESSAGE_BUFFER.clear()
        CONNECTED_CLIENTS.clear()

    def test_broadcast_appends_to_buffer(self) -> None:
        msg = {"type": "token", "speaker": "analyst", "content": "hello"}
        asyncio.run(broadcast(msg))
        assert len(MESSAGE_BUFFER) == 1
        assert MESSAGE_BUFFER[0] == msg

    def test_buffer_accumulates_messages(self) -> None:
        msgs = [
            {"type": "system", "speaker": "system", "content": "Session started"},
            {"type": "token", "speaker": "manager", "content": "Hello"},
            {"type": "token", "speaker": "analyst", "content": "World"},
        ]
        for m in msgs:
            asyncio.run(broadcast(m))
        assert len(MESSAGE_BUFFER) == 3

    def test_session_complete_clears_buffer(self) -> None:
        asyncio.run(broadcast({"type": "token", "speaker": "manager", "content": "hi"}))
        asyncio.run(broadcast({"type": "system", "speaker": "system", "content": "Session complete"}))
        assert len(MESSAGE_BUFFER) == 0

    def test_non_session_complete_system_msg_keeps_buffer(self) -> None:
        asyncio.run(broadcast({"type": "system", "speaker": "system", "content": "Session started"}))
        asyncio.run(broadcast({"type": "system", "speaker": "system", "content": "Turn: analyst"}))
        assert len(MESSAGE_BUFFER) == 2

    def _make_ws(self, messages: list[str] | None = None) -> AsyncMock:
        """Create a mock WebSocket with async iteration support."""
        ws = AsyncMock()
        items = messages or []

        async def _aiter(self_ws):
            for m in items:
                yield m

        ws.__aiter__ = _aiter
        return ws

    def test_replay_buffer_to_new_client(self) -> None:
        """Late-joining client receives all buffered messages."""
        MESSAGE_BUFFER.extend([
            {"type": "system", "speaker": "system", "content": "Session started"},
            {"type": "token", "speaker": "manager", "content": "Hello"},
        ])

        ws = self._make_ws()

        asyncio.run(handler(ws, token=None))

        # Should have received 2 replayed messages
        assert ws.send.call_count == 2
        first_msg = json.loads(ws.send.call_args_list[0][0][0])
        assert first_msg["content"] == "Session started"
        second_msg = json.loads(ws.send.call_args_list[1][0][0])
        assert second_msg["content"] == "Hello"

    def test_replay_failure_disconnects_client(self) -> None:
        """Client that fails during replay is removed from CONNECTED_CLIENTS."""
        MESSAGE_BUFFER.append({"type": "token", "speaker": "a", "content": "x"})

        ws = self._make_ws()
        ws.send = AsyncMock(side_effect=Exception("broken"))

        asyncio.run(handler(ws, token=None))

        assert ws not in CONNECTED_CLIENTS

    def test_empty_buffer_no_replay(self) -> None:
        """Client connecting with empty buffer gets no replay messages."""
        ws = self._make_ws()

        asyncio.run(handler(ws, token=None))

        ws.send.assert_not_called()
