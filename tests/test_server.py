"""Unit tests for agents/server.py — WebSocket server auth, broadcast, lifecycle."""

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock


sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from server import (
    CONNECTED_CLIENTS,
    authenticate,
    broadcast,
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
