"""Unit tests for agents/notify.py — Pushover notification module."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from notify import send_pushover


class TestSendPushover:
    """Tests for Pushover notification sending."""

    @patch("notify.urllib.request.urlopen")
    @patch("notify.urllib.request.Request")
    @patch.dict(
        "os.environ",
        {
            "PUSHOVER_USER_KEY": "test-user-key",
            "PUSHOVER_APP_TOKEN": "test-app-token",
        },
    )
    def test_sends_correct_payload(
        self,
        mock_request_cls: MagicMock,
        mock_urlopen: MagicMock,
    ) -> None:
        """Pushover API receives correct title, message, and priority."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"status":1}'
        mock_urlopen.return_value.__enter__ = lambda s: mock_response
        mock_urlopen.return_value.__exit__ = MagicMock(return_value=False)

        result = send_pushover("Test Title", "Test message", priority=0)

        assert result is True
        # Verify the Request was constructed with correct URL
        mock_request_cls.assert_called_once()
        call_args = mock_request_cls.call_args
        assert "api.pushover.net" in call_args[0][0]

        # Verify payload contains required fields
        payload = call_args[1].get("data") or call_args[0][1]
        if isinstance(payload, bytes):
            payload = payload.decode()
        assert "test-user-key" in payload
        assert "test-app-token" in payload
        assert (
            "Test+message" in payload
            or "Test%20message" in payload
            or "Test message" in payload
        )

    @patch.dict("os.environ", {}, clear=True)
    def test_fails_silently_if_no_keys(self) -> None:
        """Returns False without crash when Pushover keys are missing."""
        # Remove any existing keys
        result = send_pushover("Title", "Message")
        assert result is False

    @patch("notify.urllib.request.urlopen")
    @patch("notify.urllib.request.Request")
    @patch.dict(
        "os.environ",
        {
            "PUSHOVER_USER_KEY": "test-user-key",
            "PUSHOVER_APP_TOKEN": "test-app-token",
        },
    )
    def test_priority_levels_correct(
        self,
        mock_request_cls: MagicMock,
        mock_urlopen: MagicMock,
    ) -> None:
        """Priority values -1, 0, 1, 2 are passed correctly to API."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"status":1}'
        mock_urlopen.return_value.__enter__ = lambda s: mock_response
        mock_urlopen.return_value.__exit__ = MagicMock(return_value=False)

        for priority in (-1, 0, 1, 2):
            mock_request_cls.reset_mock()
            send_pushover("Title", "Msg", priority=priority)

            call_args = mock_request_cls.call_args
            payload = call_args[1].get("data") or call_args[0][1]
            if isinstance(payload, bytes):
                payload = payload.decode()
            assert (
                f"priority={priority}" in payload or f"priority={priority}" in payload
            )

    @patch("notify.urllib.request.urlopen", side_effect=Exception("Network error"))
    @patch.dict(
        "os.environ",
        {
            "PUSHOVER_USER_KEY": "test-user-key",
            "PUSHOVER_APP_TOKEN": "test-app-token",
        },
    )
    def test_returns_false_on_network_error(self, mock_urlopen: MagicMock) -> None:
        """Returns False on network failure without crashing."""
        result = send_pushover("Title", "Message")
        assert result is False
