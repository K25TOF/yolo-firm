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

import re

from invoke import (
    build_prompt,
    extract_memory_update,
    get_agent_tools,
    load_context,
    parse_context_manifest,
    write_session_log,
)
from notify import send_pushover
from tools import run_backtest, update_memory

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

VALID_AGENTS = {"analyst", "engineer", "manager"}
_NEXT_RE = re.compile(r"\[NEXT:\s*(\w+)\s*\]", re.IGNORECASE)
_BLOCKER_RE = re.compile(r"\[BLOCKER:\s*(.+?)\s*\]", re.IGNORECASE)
_SCOPE_BLOCKING_RE = re.compile(r"\[SCOPE REQUEST BLOCKING:\s*(.+?)\s*\]", re.IGNORECASE)
_SCOPE_RE = re.compile(r"\[SCOPE REQUEST:\s*(.+?)\s*\]", re.IGNORECASE)


def _parse_next_agent(text: str) -> str | None:
    """Extract routing tag [NEXT: agent] from Manager response.

    Returns lowercase agent name if valid, None otherwise.
    """
    match = _NEXT_RE.search(text)
    if not match:
        return None
    agent = match.group(1).lower()
    return agent if agent in VALID_AGENTS else None


@dataclass
class SessionResult:
    """Result of a complete session, returned by run_session."""

    session_id: str
    outcome: str  # "complete" | "blocker" | "cancelled" | "turn_limit" | "dry_run"
    input_tokens: int
    output_tokens: int
    cost_usd: float
    duration_seconds: float
    task_summary: str


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


TOOL_DISPATCH = {
    "run_backtest": run_backtest,
    "update_memory": update_memory,
}

MAX_TOOL_ROUNDS = 5


def _dispatch_tool(name: str, tool_input: dict, calling_agent: str) -> dict:
    """Dispatch a tool call to the appropriate handler."""
    fn = TOOL_DISPATCH.get(name)
    if not fn:
        return {"error": f"Unknown tool: {name}"}
    if name == "update_memory":
        return fn(
            agent=tool_input["agent"],
            content=tool_input["content"],
            calling_agent=calling_agent,
        )
    return fn(tool_input)


def invoke_agent(
    client: object,
    agent: str,
    message: str,
    system_prompt: str,
    docs: list[dict],
    memory: str | None,
    model: str,
    transcript: str = "",
    tools: list[dict] | None = None,
) -> TurnResult:
    """Invoke a single agent via the Anthropic API.

    If transcript is provided, it is prepended to the message.
    If tools is provided, enables tool use with automatic dispatch loop.
    """
    full_message = message
    if transcript:
        full_message = (
            f"## Session transcript so far\n\n{transcript}\n\n---\n\n{message}"
        )

    prompt = build_prompt(system_prompt, docs, memory, full_message)

    create_kwargs: dict = {
        "model": model,
        "max_tokens": MAX_TOKENS_PER_TURN,
        "system": prompt["system"],
        "messages": list(prompt["messages"]),
    }
    if tools:
        create_kwargs["tools"] = tools

    api_response = client.messages.create(**create_kwargs)

    total_in = api_response.usage.input_tokens
    total_out = api_response.usage.output_tokens

    # Tool use loop — handle tool_use blocks in response
    messages = list(create_kwargs["messages"])
    rounds = 0
    while api_response.stop_reason == "tool_use" and rounds < MAX_TOOL_ROUNDS:
        rounds += 1
        # Collect all content blocks (text + tool_use)
        messages.append({"role": "assistant", "content": api_response.content})

        # Process each tool_use block
        tool_results = []
        for block in api_response.content:
            if block.type == "tool_use":
                tool_label = block.input.get("strategy_id", block.name)
                print(f"  [tool] {block.name}({tool_label})")
                result = _dispatch_tool(block.name, block.input, agent)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, default=str),
                })

        messages.append({"role": "user", "content": tool_results})

        api_response = client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS_PER_TURN,
            system=prompt["system"],
            messages=messages,
            tools=tools or [],
        )
        total_in += api_response.usage.input_tokens
        total_out += api_response.usage.output_tokens

    # Extract final text from response
    response_text = ""
    for block in api_response.content:
        if hasattr(block, "text"):
            response_text += block.text
    memory_upd = extract_memory_update(response_text)

    return TurnResult(
        agent=agent,
        message=message,
        response=response_text,
        input_tokens=total_in,
        output_tokens=total_out,
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

    cmd = [sys.executable, str(server_script), "--port", str(port)]

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

        return connect(
            f"ws://127.0.0.1:{port}",
            ping_interval=None,  # Disable client-side keepalive pings
            close_timeout=5,
        )
    except Exception:
        return None


def write_review_doc(
    reviews_dir: Path,
    session_id: str,
    model: str,
    manager_close_response: str,
    log_path: Path,
) -> Path:
    """Write a PO review document from the Manager CLOSE synthesis.

    Creates the reviews directory if needed. Appends a link to the session log.
    Returns the path to the review file.
    """
    reviews_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now(UTC).strftime("%Y-%m-%d")
    filename = f"{today}-{session_id}-review.md"
    review_path = reviews_dir / filename

    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    log_name = log_path.name if log_path else "unknown"

    content = (
        f"# Session Review: {session_id}\n"
        f"_Date: {now} | Model: {model}_\n\n"
        f"## Manager Synthesis\n\n"
        f"{manager_close_response}\n\n"
        f"---\n"
        f"_Session log: session-log/{log_name}_\n"
    )
    review_path.write_text(content)

    # Append link to session log
    if log_path and log_path.exists():
        with open(log_path, "a") as f:
            f.write(f"\nReview: reviews/{filename}\n")

    return review_path


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
    max_turns: int = 50,
) -> SessionResult:
    """Run a dynamic multi-agent research session.

    Manager controls routing via [NEXT: agent] and [SESSION_COMPLETE] tags.
    Non-manager turns always return to Manager.
    Returns SessionResult with outcome, token usage, cost, and duration.
    """
    global _tracker, _log_path  # noqa: PLW0603

    start_time = time.monotonic()
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
        for agent_name in ("manager", "analyst", "engineer"):
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
        print(f"  Max turns: {max_turns}")
        print("=== END DRY RUN ===")
        return SessionResult(
            session_id=session_id, outcome="dry_run",
            input_tokens=0, output_tokens=0, cost_usd=0.0,
            duration_seconds=time.monotonic() - start_time,
            task_summary="Dry run — no API calls made.",
        )

    # --- LIVE MODE ---
    client = create_client()

    # Start WebSocket server and connect
    ws_conn = None
    server_up = ensure_server_running()
    if server_up:
        ws_conn = connect_ws()
        if ws_conn:
            print("[session] Connected to WebSocket server")
        print("Chat UI → http://localhost:8003")

    # Agent context cache — avoids reloading on every turn
    _ctx_cache: dict[str, tuple] = {}

    def _get_context(agent_name: str) -> tuple:
        if agent_name not in _ctx_cache:
            _ctx_cache[agent_name] = load_agent_context(
                agent_name, agents_dir, firm_repo, yolo_repo,
            )
        return _ctx_cache[agent_name]

    def _invoke(agent_name: str, message: str, transcript: str = "") -> TurnResult:
        """Invoke agent — streaming if WS connected, blocking if tools present."""
        prompt, docs, mem_text, memory = _get_context(agent_name)
        tools = get_agent_tools(agent_name)

        if tools:
            return invoke_agent(
                client, agent_name, message, prompt, docs, memory, model,
                transcript=transcript, tools=tools,
            )
        if ws_conn:
            return invoke_agent_streaming(
                client, agent_name, message, prompt, docs, memory, model,
                transcript=transcript, ws_conn=ws_conn,
            )
        return invoke_agent(
            client, agent_name, message, prompt, docs, memory, model,
            transcript=transcript,
        )

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

    print(f"=== SESSION {session_id} ===")
    print(f"Model: {model}")
    if question:
        print(f"Question: {question}")
    else:
        print("Mode: open (Manager decides topic)")
    print(f"Max turns: {max_turns}")
    print("=" * 40)

    send_to_ws(ws_conn, {
        "type": "system", "speaker": "system",
        "content": f"Session {session_id} started",
    })

    # Build opening message
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
            f"Open the session per protocol. Define scope, "
            f"and which agents are needed."
        )

    # --- DYNAMIC SESSION LOOP ---
    current_agent = "manager"
    current_message = open_message
    cancelled = False
    outcome = "complete"

    for turn_num in range(max_turns):
        # Check interrupt before each turn
        if _handle_interrupt():
            cancelled = True
            outcome = "cancelled"
            break

        # Warn when approaching turn limit
        remaining = max_turns - turn_num
        if remaining == 5:
            print(f"[session] WARNING: {remaining} turns remaining before force close")

        # Build transcript for context
        transcript = build_transcript(tracker.turns) if turn_num > 0 else ""

        # Invoke agent
        label = "OPEN" if turn_num == 0 else ""
        turn = _invoke(current_agent, current_message, transcript)
        tracker.turns.append(turn)

        # Write session log
        ctx = _get_context(current_agent)
        ctx_files = [d["path"] for d in ctx[1]]
        ctx_missing = ctx[2]
        _log_path = write_session_log(
            log_dir, session_id, current_agent, model,
            ctx_files, ctx_missing, current_message, turn.response,
        )

        # Send to WS if agent used blocking path (tools present)
        if ws_conn and get_agent_tools(current_agent):
            send_to_ws(ws_conn, {
                "type": "message", "speaker": current_agent,
                "content": turn.response,
            })

        print_turn(turn, tracker, label)

        if turn.memory_update:
            memory_updates.append((current_agent, turn.memory_update))

        # --- ROUTING LOGIC ---
        if current_agent == "manager":
            # Check for blocker tag
            blocker_match = _BLOCKER_RE.search(turn.response)
            if blocker_match:
                desc = blocker_match.group(1)
                flag_path = agents_dir / "blocker.flag"
                flag_path.write_text(desc)
                send_pushover(
                    "Blocker", f"🚨 Blocker: {desc}. Research paused.",
                    priority=1,
                )
                outcome = "blocker"
                break

            # Check for blocking scope request (before non-blocking)
            scope_blocking_match = _SCOPE_BLOCKING_RE.search(turn.response)
            if scope_blocking_match:
                desc = scope_blocking_match.group(1)
                flag_path = agents_dir / "scope-request.flag"
                flag_path.write_text(desc)
                send_pushover(
                    "Scope Request (Blocking)",
                    f"📋 Scope request: {desc}. Approve or reject.",
                    priority=0,
                )
                outcome = "blocker"
                break

            # Check for non-blocking scope request
            scope_match = _SCOPE_RE.search(turn.response)
            if scope_match and not scope_blocking_match:
                desc = scope_match.group(1)
                flag_path = agents_dir / "scope-request.flag"
                flag_path.write_text(desc)
                send_pushover(
                    "Scope Request",
                    f"📋 Scope request: {desc}. Approve or reject.",
                    priority=0,
                )
                # Non-blocking — session continues

            # Check for session complete
            if "[SESSION_COMPLETE]" in turn.response:
                # Write review doc on final manager turn
                reviews_dir = agents_dir / "reviews"
                write_review_doc(
                    reviews_dir=reviews_dir,
                    session_id=session_id,
                    model=model,
                    manager_close_response=turn.response,
                    log_path=_log_path,
                )
                break

            # Check for routing tag
            next_tag = _NEXT_RE.search(turn.response)
            if next_tag is None:
                # No routing tag and no SESSION_COMPLETE → session complete
                break

            next_agent = _parse_next_agent(turn.response)
            # Invalid agent name defaults to manager
            current_agent = next_agent if next_agent else "manager"
            current_message = (
                f"Session transcript so far.\n\n"
                f"{current_agent.title()}, your turn. Respond per protocol."
            )
        else:
            # Non-manager turns always return to Manager
            current_agent = "manager"
            current_message = (
                "Here is the updated session transcript.\n\n"
                "Continue the session per protocol."
            )
    else:
        # Loop exhausted without break → turn limit reached
        if outcome == "complete":
            outcome = "turn_limit"

    # --- SUMMARY ---
    print(f"\n{tracker.summary()}")
    print(f"\nSession ID: {session_id}")
    print(f"Log: {_log_path}")
    print(f"Turns: {len(tracker.turns)}")

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

    elapsed = time.monotonic() - start_time
    cost = tracker.total_input * COST_PER_INPUT + tracker.total_output * COST_PER_OUTPUT
    summary = ""
    if tracker.turns:
        summary = tracker.turns[-1].response[:200]

    return SessionResult(
        session_id=session_id,
        outcome=outcome,
        input_tokens=tracker.total_input,
        output_tokens=tracker.total_output,
        cost_usd=round(cost, 6),
        duration_seconds=round(elapsed, 2),
        task_summary=summary,
    )


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
    parser.add_argument(
        "--max-turns", type=int, default=50,
        help="Maximum turns before force close (default: 50)",
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
        max_turns=args.max_turns,
    )


if __name__ == "__main__":
    main()
