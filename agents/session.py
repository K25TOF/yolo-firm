"""Multi-agent session orchestrator for YOLO Org Learning.

Runs a full research session: Manager open → Analyst turn → Engineer turn → Manager synthesis.
Streams tokens to WebSocket server (if running) alongside terminal output.

Usage:
    python session.py --question "Should we add a VWAP entry filter?"
    python session.py --open
    python session.py --question "Audit EXP-023" --session-id vwap-audit
    python session.py --question "test" --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from invoke import (
    build_prompt,
    extract_memory_update,
    load_context,
    parse_context_manifest,
    write_session_log,
)

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS_PER_TURN = 4096

# Haiku pricing: $1.00 / $5.00 per 1M tokens (in/out)
COST_PER_INPUT = 1.00 / 1_000_000
COST_PER_OUTPUT = 5.00 / 1_000_000

# Path constants — resolved relative to this file
AGENTS_DIR = Path(__file__).parent
FIRM_REPO = AGENTS_DIR.parent
YOLO_REPO = FIRM_REPO.parent / "yolo"
INTERRUPT_FLAG = AGENTS_DIR / "session-interrupt.flag"


@dataclass
class TurnResult:
    """Result of a single agent turn."""

    agent: str
    message: str
    response: str
    input_tokens: int
    output_tokens: int
    memory_update: str | None


@dataclass
class TokenTracker:
    """Tracks cumulative token usage across a session."""

    turns: list[TurnResult] = field(default_factory=list)

    @property
    def total_input(self) -> int:
        """Total input tokens across all turns."""
        return sum(t.input_tokens for t in self.turns)

    @property
    def total_output(self) -> int:
        """Total output tokens across all turns."""
        return sum(t.output_tokens for t in self.turns)

    def summary(self) -> str:
        """Human-readable summary with per-turn breakdown and cost estimate."""
        lines = ["=== TOKEN SUMMARY ==="]
        for t in self.turns:
            lines.append(f"  {t.agent:>10}: {t.input_tokens:,} in / {t.output_tokens:,} out")
        lines.append(f"  {'TOTAL':>10}: {self.total_input:,} in / {self.total_output:,} out")
        cost = self.total_input * COST_PER_INPUT + self.total_output * COST_PER_OUTPUT
        lines.append(f"  Estimated cost: ${cost:.4f}")
        return "\n".join(lines)


def create_client() -> object:
    """Create an Anthropic API client from environment."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        raise SystemExit(1)

    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic package not installed. Run: pip install anthropic")
        raise SystemExit(1)

    return anthropic.Anthropic(api_key=api_key)


def generate_session_id() -> str:
    """Generate a timestamp-based session ID: YYYYMMDD-HHMMSS."""
    return datetime.now(UTC).strftime("%Y%m%d-%H%M%S")


def load_agent_context(
    agent: str,
    agents_dir: Path,
    firm_repo: Path,
    yolo_repo: Path,
) -> tuple[str, list[dict], list[str], str | None]:
    """Load system prompt, context docs, and memory for a given agent.

    Returns (system_prompt, docs, missing, memory).
    Raises FileNotFoundError if system prompt is missing.
    """
    agent_dir = agents_dir / agent
    prompt_path = agent_dir / "system-prompt.md"
    manifest_path = agent_dir / "context-manifest.md"
    memory_path = agent_dir / "memory.md"

    if not prompt_path.is_file():
        raise FileNotFoundError(f"System prompt not found: {prompt_path}")

    system_prompt = prompt_path.read_text()

    if manifest_path.is_file():
        entries = parse_context_manifest(manifest_path)
        docs, missing = load_context(entries, firm_repo, yolo_repo)
    else:
        docs, missing = [], []

    memory = memory_path.read_text() if memory_path.is_file() else None

    return system_prompt, docs, missing, memory


def build_transcript(turns: list[TurnResult]) -> str:
    """Build a markdown transcript of all turns for injection into next turn."""
    if not turns:
        return ""

    lines = []
    for t in turns:
        label = t.agent.title()
        lines.append(f"**{label}:** {t.response}")
        lines.append("")

    return "\n".join(lines).strip()


def invoke_agent(
    client: object,
    agent: str,
    message: str,
    system_prompt: str,
    docs: list[dict],
    memory: str | None,
    model: str,
    transcript: str = "",
) -> TurnResult:
    """Invoke a single agent via the Anthropic API.

    If transcript is provided, it is prepended to the message.
    """
    full_message = message
    if transcript:
        full_message = (
            f"## Session transcript so far\n\n{transcript}\n\n---\n\n{message}"
        )

    prompt = build_prompt(system_prompt, docs, memory, full_message)

    api_response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS_PER_TURN,
        system=prompt["system"],
        messages=prompt["messages"],
    )

    response_text = api_response.content[0].text
    memory_upd = extract_memory_update(response_text)

    return TurnResult(
        agent=agent,
        message=message,
        response=response_text,
        input_tokens=api_response.usage.input_tokens,
        output_tokens=api_response.usage.output_tokens,
        memory_update=memory_upd,
    )


def send_to_ws(ws_conn: object | None, message: dict) -> None:
    """Send a JSON message to the WebSocket server. No crash on failure."""
    if ws_conn is None:
        return
    try:
        ws_conn.send(json.dumps(message))
    except Exception as e:
        print(f"[session] WebSocket send failed: {e}")


def invoke_agent_streaming(
    client: object,
    agent: str,
    message: str,
    system_prompt: str,
    docs: list[dict],
    memory: str | None,
    model: str,
    transcript: str = "",
    ws_conn: object | None = None,
) -> TurnResult:
    """Invoke a single agent via streaming API.

    Tokens are printed to stdout and pushed to WebSocket server as they arrive.
    Falls back gracefully if WS connection is unavailable.
    """
    full_message = message
    if transcript:
        full_message = (
            f"## Session transcript so far\n\n{transcript}\n\n---\n\n{message}"
        )

    prompt = build_prompt(system_prompt, docs, memory, full_message)

    # Send turn start notification
    send_to_ws(ws_conn, {
        "type": "system", "speaker": "system",
        "content": f"Turn: {agent}",
    })

    # Stream response
    with client.messages.stream(
        model=model,
        max_tokens=MAX_TOKENS_PER_TURN,
        system=prompt["system"],
        messages=prompt["messages"],
    ) as stream:
        for delta in stream.text_stream:
            sys.stdout.write(delta)
            sys.stdout.flush()
            send_to_ws(ws_conn, {
                "type": "token", "speaker": agent, "content": delta,
            })

    final = stream.get_final_message()
    response_text = final.content[0].text
    memory_upd = extract_memory_update(response_text)

    # Send turn cost
    in_tok = final.usage.input_tokens
    out_tok = final.usage.output_tokens
    cost = in_tok * COST_PER_INPUT + out_tok * COST_PER_OUTPUT
    send_to_ws(ws_conn, {
        "type": "cost", "speaker": "system",
        "content": f"Turn cost: ${cost:.4f} ({in_tok} in / {out_tok} out)",
    })

    return TurnResult(
        agent=agent,
        message=message,
        response=response_text,
        input_tokens=in_tok,
        output_tokens=out_tok,
        memory_update=memory_upd,
    )


def is_server_running(port: int = 8003) -> bool:
    """Check if the WebSocket server is listening on the given port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex(("127.0.0.1", port))
        return result == 0
    finally:
        sock.close()


def ensure_server_running(port: int = 8003) -> bool:
    """Start the WebSocket server if not already running.

    Returns True if server is running (or was started), False if failed.
    """
    if is_server_running(port):
        return True

    # Try to start server
    agents_dir = AGENTS_DIR
    server_script = agents_dir / "server.py"
    if not server_script.is_file():
        print("[session] WARNING: server.py not found, continuing without streaming")
        return False

    session_token = os.environ.get("SESSION_TOKEN")
    cmd = [sys.executable, str(server_script), "--port", str(port)]
    if session_token:
        cmd.extend(["--token", session_token])

    try:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError as e:
        print(f"[session] WARNING: Failed to start server: {e}")
        return False

    # Wait up to 3 seconds for server to start
    for _ in range(30):
        time.sleep(0.1)
        if is_server_running(port):
            print(f"[session] WebSocket server started on ws://127.0.0.1:{port}")
            return True

    print("[session] WARNING: Server did not start in time, continuing without streaming")
    return False


def connect_ws(port: int = 8003) -> object | None:
    """Open a sync WebSocket connection to the server. Returns None on failure."""
    try:
        from websockets.sync.client import connect

        session_token = os.environ.get("SESSION_TOKEN")
        ws = connect(f"ws://127.0.0.1:{port}")

        if session_token:
            ws.send(json.dumps({"type": "auth", "token": session_token}))

        return ws
    except Exception:
        return None


def check_interrupt() -> str | None:
    """Check for pause/cancel interrupt flag.

    Returns 'pause', 'cancel', or None.
    """
    if not INTERRUPT_FLAG.is_file():
        return None
    return INTERRUPT_FLAG.read_text().strip()


def print_turn(turn: TurnResult, tracker: TokenTracker, label: str = "") -> None:
    """Print a turn's output to terminal with formatting."""
    header = turn.agent.upper()
    if label:
        header = f"{header} — {label}"
    print(f"\n=== {header} ===\n")
    print(turn.response)
    print(
        f"\nTokens: {turn.input_tokens:,} in / {turn.output_tokens:,} out"
        f" | Cumulative: {tracker.total_input:,} / {tracker.total_output:,}",
    )
    print("---")


# Module-level state for interrupt handler
_tracker: TokenTracker | None = None
_log_path: Path | None = None


def _handle_interrupt(signum: int, frame: object) -> None:
    """Handle Ctrl+C — print partial summary and exit."""
    print("\n\n--- SESSION INTERRUPTED (Ctrl+C) ---")
    if _tracker and _tracker.turns:
        print(_tracker.summary())
    if _log_path:
        print(f"Partial session log: {_log_path}")
    sys.exit(130)


def run_session(
    question: str | None,
    open_mode: bool,
    model: str,
    session_id: str,
    dry_run: bool,
) -> None:
    """Run a full multi-agent research session.

    Flow: Manager OPEN → Analyst → Engineer → Manager CLOSE.
    """
    global _tracker, _log_path  # noqa: PLW0603

    agents_dir = AGENTS_DIR
    firm_repo = FIRM_REPO
    yolo_repo = YOLO_REPO
    log_dir = agents_dir / "session-log"
    log_dir.mkdir(exist_ok=True)

    tracker = TokenTracker()
    _tracker = tracker
    memory_updates: list[tuple[str, str]] = []

    # --- DRY RUN MODE ---
    if dry_run:
        print(f"=== DRY RUN: session {session_id} ===")
        for agent_name in ("manager", "analyst", "engineer", "manager"):
            prompt, docs, missing, memory = load_agent_context(
                agent_name, agents_dir, firm_repo, yolo_repo,
            )
            print(
                f"\n  {agent_name.title()}: "
                f"{len(docs)} docs loaded, {len(missing)} missing, "
                f"prompt {len(prompt)} chars"
                f"{', memory loaded' if memory else ''}",
            )
        if question:
            print(f"\n  Question: {question}")
        else:
            print("\n  Mode: open (Manager decides topic)")
        print(f"  Model: {model}")
        print("=== END DRY RUN ===")
        return

    # --- LIVE MODE ---
    client = create_client()

    # Start WebSocket server and connect
    ws_conn = None
    server_up = ensure_server_running()
    if server_up:
        ws_conn = connect_ws()
        if ws_conn:
            print("[session] Connected to WebSocket server")
        session_token = os.environ.get("SESSION_TOKEN")
        if session_token:
            print(f"Chat UI → http://localhost:8003?token={session_token}")
        else:
            print("Chat UI → http://localhost:8003")

    def _invoke(agent, message, prompt, docs, mem, transcript=""):
        """Invoke agent — streaming if WS connected, blocking otherwise."""
        if ws_conn:
            return invoke_agent_streaming(
                client, agent, message, prompt, docs, mem, model,
                transcript=transcript, ws_conn=ws_conn,
            )
        return invoke_agent(
            client, agent, message, prompt, docs, mem, model,
            transcript=transcript,
        )

    print(f"=== SESSION {session_id} ===")
    print(f"Model: {model}")
    if question:
        print(f"Question: {question}")
    else:
        print("Mode: open (Manager decides topic)")
    print("=" * 40)

    send_to_ws(ws_conn, {
        "type": "system", "speaker": "system",
        "content": f"Session {session_id} started",
    })

    # --- TURN 1: MANAGER OPEN ---
    mgr_prompt, mgr_docs, mgr_missing, mgr_memory = load_agent_context(
        "manager", agents_dir, firm_repo, yolo_repo,
    )
    context_files = [d["path"] for d in mgr_docs]

    if open_mode:
        open_message = (
            "Based on your context, memory, and the current ideas log, "
            "what question should this session investigate? "
            "State the question clearly, then open the session per protocol."
        )
    else:
        open_message = (
            f"PO has triggered a research session.\n\n"
            f"Question: {question}\n\n"
            f"Open the session per protocol. Define scope, time-box, "
            f"and which agents are needed."
        )

    turn = _invoke("manager", open_message, mgr_prompt, mgr_docs, mgr_memory)
    tracker.turns.append(turn)
    _log_path = write_session_log(
        log_dir, session_id, "manager", model,
        context_files, mgr_missing, open_message, turn.response,
    )
    print_turn(turn, tracker, "OPEN")
    if turn.memory_update:
        memory_updates.append(("manager", turn.memory_update))

    cancelled = False

    def _handle_interrupt() -> bool:
        """Check interrupt flag. Handle pause (block) or cancel (return True)."""
        status = check_interrupt()
        if status == "cancel":
            print("[session] Cancelled by PO")
            send_to_ws(ws_conn, {
                "type": "system", "speaker": "system",
                "content": "Session cancelled by PO",
            })
            return True
        if status == "pause":
            print("[session] Paused by PO — waiting for resume...")
            send_to_ws(ws_conn, {
                "type": "system", "speaker": "system",
                "content": "Session paused — waiting for resume...",
            })
            while check_interrupt() == "pause":
                time.sleep(1)
            if check_interrupt() == "cancel":
                print("[session] Cancelled by PO")
                send_to_ws(ws_conn, {
                    "type": "system", "speaker": "system",
                    "content": "Session cancelled by PO",
                })
                return True
            print("[session] Resumed")
        return False

    if _handle_interrupt():
        cancelled = True

    # --- TURN 2: ANALYST ---
    if not cancelled:
        ana_prompt, ana_docs, ana_missing, ana_memory = load_agent_context(
            "analyst", agents_dir, firm_repo, yolo_repo,
        )
        transcript = build_transcript(tracker.turns)
        analyst_message = (
            "Manager has opened a research session and addressed you.\n\n"
            "Analyst, your turn. Respond to the Manager's question per protocol."
        )

        turn = _invoke(
            "analyst", analyst_message,
            ana_prompt, ana_docs, ana_memory, transcript,
        )
        tracker.turns.append(turn)
        write_session_log(
            log_dir, session_id, "analyst", model,
            [d["path"] for d in ana_docs], ana_missing,
            analyst_message, turn.response,
        )
        print_turn(turn, tracker)
        if turn.memory_update:
            memory_updates.append(("analyst", turn.memory_update))

        if _handle_interrupt():
            cancelled = True

    # --- TURN 3: ENGINEER ---
    if not cancelled:
        eng_prompt, eng_docs, eng_missing, eng_memory = load_agent_context(
            "engineer", agents_dir, firm_repo, yolo_repo,
        )
        transcript = build_transcript(tracker.turns)
        engineer_message = (
            "Manager has opened a research session. "
            "Here is the transcript so far.\n\n"
            "Engineer, your turn. Respond per protocol."
        )

        turn = _invoke(
            "engineer", engineer_message,
            eng_prompt, eng_docs, eng_memory, transcript,
        )
        tracker.turns.append(turn)
        write_session_log(
            log_dir, session_id, "engineer", model,
            [d["path"] for d in eng_docs], eng_missing,
            engineer_message, turn.response,
        )
        print_turn(turn, tracker)
        if turn.memory_update:
            memory_updates.append(("engineer", turn.memory_update))

        if _handle_interrupt():
            cancelled = True

    # --- TURN 4: MANAGER CLOSE ---
    if not cancelled:
        transcript = build_transcript(tracker.turns)
        close_message = (
            "All agents have responded. Here is the full session transcript.\n\n"
            "Run the session close routine per protocol: "
            "summarise findings, note memory updates, write session minutes."
        )

        turn = _invoke(
            "manager", close_message,
            mgr_prompt, mgr_docs, mgr_memory, transcript,
        )
        tracker.turns.append(turn)
        write_session_log(
            log_dir, session_id, "manager", model,
            context_files, mgr_missing, close_message, turn.response,
        )
        print_turn(turn, tracker, "CLOSE")
        if turn.memory_update:
            memory_updates.append(("manager", turn.memory_update))

    # --- SUMMARY ---
    print(f"\n{tracker.summary()}")
    print(f"\nSession ID: {session_id}")
    print(f"Log: {_log_path}")

    if memory_updates:
        pending_path = agents_dir / "memory-pending.md"
        with open(pending_path, "a") as f:
            for agent_name, update in memory_updates:
                f.write(f"\n## {agent_name.title()} — {session_id}\n\n{update}\n")
        print(f"\nMemory updates flagged: {len(memory_updates)}")
        for agent_name, update in memory_updates:
            preview = update.split("\n")[0][:60]
            print(f"  - {agent_name.title()}: {preview}")
        print(f"  → {pending_path}")
    else:
        print("\nNo memory updates flagged.")

    # Clean up interrupt flag
    INTERRUPT_FLAG.unlink(missing_ok=True)

    # Close WebSocket connection
    if not cancelled:
        send_to_ws(ws_conn, {
            "type": "system", "speaker": "system",
            "content": "Session complete",
        })
    if ws_conn:
        try:
            ws_conn.close()
        except Exception:
            pass

    print("\n=== SESSION COMPLETE ===")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run a YOLO Org Learning research session.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--question", help="Research question for the session",
    )
    group.add_argument(
        "--open", action="store_true",
        help="Let Manager decide what to investigate",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Anthropic model ID (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--session-id", default=None,
        help="Session ID for log grouping (default: auto-generated)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Build prompts without calling API",
    )

    args = parser.parse_args()

    signal.signal(signal.SIGINT, _handle_interrupt)

    session_id = args.session_id or generate_session_id()

    run_session(
        question=args.question,
        open_mode=args.open,
        model=args.model,
        session_id=session_id,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
