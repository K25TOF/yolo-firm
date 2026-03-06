"""WebSocket server for YOLO Org Learning session streaming.

Accepts connections from chat UI, receives streamed tokens from session.py,
broadcasts to all connected clients.

Usage:
    python server.py
    python server.py --port 8003 --token mysecret
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import signal
import time
from pathlib import Path

import websockets
from websockets.datastructures import Headers
from websockets.http11 import Response

# Connected clients set — shared across handlers
CONNECTED_CLIENTS: set = set()

# Idle timer state
_last_activity: float = time.monotonic()
IDLE_TIMEOUT_SECONDS = 30 * 60  # 30 minutes

DEFAULT_PORT = 8003
PID_FILE = Path(__file__).parent / ".server.pid"
CHAT_UI_PATH = Path(__file__).parent / "chat-ui" / "index.html"
INTERRUPT_FLAG = Path(__file__).parent / "session-interrupt.flag"


def reset_idle_timer() -> None:
    """Reset the idle timer — called on every message received."""
    global _last_activity  # noqa: PLW0603
    _last_activity = time.monotonic()


async def process_request(connection: object, request: object) -> Response | None:
    """Serve chat UI on GET /, pass through WebSocket upgrades."""
    if request.path == "/" and "Upgrade" not in request.headers:
        try:
            html = CHAT_UI_PATH.read_bytes()
            return Response(
                200, "OK",
                Headers({"Content-Type": "text/html; charset=utf-8"}),
                html,
            )
        except FileNotFoundError:
            return Response(
                404, "Not Found",
                Headers({"Content-Type": "text/plain"}),
                b"Chat UI not found",
            )
    return None


async def handle_command(data: dict) -> bool:
    """Handle pause/resume/cancel commands. Returns True if handled."""
    cmd = data.get("type")
    if cmd == "pause":
        INTERRUPT_FLAG.write_text("pause")
        await broadcast({
            "type": "system", "speaker": "system",
            "content": "Session paused",
        })
        return True
    if cmd == "resume":
        INTERRUPT_FLAG.unlink(missing_ok=True)
        await broadcast({
            "type": "system", "speaker": "system",
            "content": "Session resumed",
        })
        return True
    if cmd == "cancel":
        INTERRUPT_FLAG.write_text("cancel")
        await broadcast({
            "type": "system", "speaker": "system",
            "content": "Session cancelled",
        })
        return True
    return False


async def authenticate(websocket: object, token: str | None) -> bool:
    """Authenticate a WebSocket connection.

    If token is None, auth is disabled and all connections are accepted.
    Otherwise, client must send {"type": "auth", "token": "..."} as first message.
    """
    if token is None:
        return True

    try:
        raw = await websocket.recv()
        data = json.loads(raw)
        if data.get("type") == "auth" and data.get("token") == token:
            return True
    except (json.JSONDecodeError, TypeError, KeyError):
        pass

    await websocket.close(1008, "Authentication failed")
    return False


async def broadcast(message: dict) -> None:
    """Send a message to all connected clients.

    Removes clients that fail to receive (disconnected).
    """
    if not CONNECTED_CLIENTS:
        return

    payload = json.dumps(message)
    disconnected = set()

    for ws in CONNECTED_CLIENTS.copy():
        try:
            await ws.send(payload)
        except Exception:
            disconnected.add(ws)

    CONNECTED_CLIENTS.difference_update(disconnected)


async def handler(websocket: object, token: str | None) -> None:
    """Handle a single WebSocket connection."""
    if not await authenticate(websocket, token):
        return

    CONNECTED_CLIENTS.add(websocket)
    remote = getattr(websocket, "remote_address", ("unknown",))
    print(f"[server] Client connected: {remote}")

    try:
        async for raw in websocket:
            reset_idle_timer()
            try:
                data = json.loads(raw)
                if not await handle_command(data):
                    await broadcast(data)
            except json.JSONDecodeError:
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        CONNECTED_CLIENTS.discard(websocket)
        print(f"[server] Client disconnected: {remote}")


async def idle_watchdog(shutdown_event: asyncio.Event) -> None:
    """Monitor idle time and shut down server after IDLE_TIMEOUT_SECONDS."""
    while not shutdown_event.is_set():
        await asyncio.sleep(60)  # Check every minute
        elapsed = time.monotonic() - _last_activity
        if elapsed >= IDLE_TIMEOUT_SECONDS:
            print(f"[server] Idle for {IDLE_TIMEOUT_SECONDS // 60} min — shutting down")
            shutdown_event.set()
            return


def _cleanup_pid() -> None:
    """Remove PID file on exit."""
    try:
        PID_FILE.unlink(missing_ok=True)
    except OSError:
        pass


async def serve(port: int, token: str | None) -> None:
    """Start the WebSocket server."""
    reset_idle_timer()
    shutdown_event = asyncio.Event()

    # Write PID file
    PID_FILE.write_text(str(os.getpid()))

    # Set up signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown_event.set)

    # Start idle watchdog
    watchdog = asyncio.create_task(idle_watchdog(shutdown_event))

    async with websockets.serve(
        lambda ws: handler(ws, token),
        "127.0.0.1",
        port,
        process_request=process_request,
    ):
        print(f"[server] Listening on ws://127.0.0.1:{port}")
        if token:
            print("[server] Auth enabled")
        else:
            print("[server] Auth disabled (no token configured)")
        print(f"[server] PID {os.getpid()} written to {PID_FILE}")

        await shutdown_event.wait()

    watchdog.cancel()
    _cleanup_pid()
    print("[server] Stopped")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="YOLO session WebSocket server.")
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT,
        help=f"Port to bind (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--token", default=None,
        help="Auth token (default: from SESSION_TOKEN env var, or disabled)",
    )
    args = parser.parse_args()

    token = args.token or os.environ.get("SESSION_TOKEN")

    try:
        asyncio.run(serve(args.port, token))
    except KeyboardInterrupt:
        _cleanup_pid()
        print("\n[server] Interrupted")


if __name__ == "__main__":
    main()
