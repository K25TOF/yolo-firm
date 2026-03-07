"""Single-agent invocation script with context loading, session logging, and memory extraction.

Usage:
    python invoke.py --agent analyst --message "What hypotheses should we test next?"
    python invoke.py --agent engineer --message "Run EXP-020" --dry-run
"""

from __future__ import annotations

import argparse
import os
import re
from datetime import UTC, datetime
from pathlib import Path


def parse_context_manifest(manifest_path: Path) -> list[dict]:
    """Parse a context-manifest.md file and return list of document entries.

    Each entry has: {name, path, source} where source is 'firm' or 'yolo'.
    """
    text = manifest_path.read_text()
    entries: list[dict] = []
    current_source: str | None = None

    for line in text.splitlines():
        # Detect section headers to determine source
        lower = line.lower()
        if "## " in line and "firm" in lower:
            current_source = "firm"
            continue
        if "## " in line and ("research" in lower or "yolo" in lower):
            current_source = "yolo"
            continue

        # Parse table rows (skip header and separator)
        if current_source and line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.split("|")]
            # Filter empty strings from leading/trailing pipes
            cells = [c for c in cells if c]
            if len(cells) >= 2 and cells[0] not in ("Document",):
                name = cells[0]
                # Extract path from backticks
                raw_path = cells[1]
                path_match = re.search(r"`([^`]+)`", raw_path)
                path = path_match.group(1) if path_match else raw_path
                entries.append({
                    "name": name,
                    "path": path,
                    "source": current_source,
                })

    return entries


def load_context(
    entries: list[dict],
    firm_repo: Path,
    yolo_repo: Path,
) -> tuple[list[dict], list[str]]:
    """Load document content from repos based on manifest entries.

    Returns (docs, missing) where docs is list of {name, path, content}
    and missing is list of human-readable missing file descriptions.
    """
    docs: list[dict] = []
    missing: list[str] = []

    for entry in entries:
        if entry["source"] == "firm":
            file_path = firm_repo / entry["path"]
        else:
            file_path = yolo_repo / entry["path"]

        if file_path.is_file():
            docs.append({
                "name": entry["name"],
                "path": entry["path"],
                "content": file_path.read_text(),
            })
        else:
            missing.append(f"{entry['path']} ({entry['name']})")

    return docs, missing


def write_session_log(
    log_dir: Path,
    session_id: str,
    agent: str,
    model: str,
    context_files: list[str],
    missing_files: list[str],
    message: str,
    response: str,
) -> Path:
    """Write or append a session exchange to the session log.

    Returns the path to the log file.
    """
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    log_file = log_dir / f"{today}-{session_id}.md"

    if log_file.exists():
        # Append another exchange to existing session
        with open(log_file, "a") as f:
            f.write(f"\n**Manager:** {message}\n\n")
            f.write(f"**{agent.title()}:** {response}\n\n")
            f.write("---\n")
    else:
        # Create new session log
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
        with open(log_file, "w") as f:
            f.write(f"# Session: {session_id}\n")
            f.write(f"_Date: {now} | Agent: {agent} | Model: {model}_\n\n")
            f.write("## Context loaded\n")
            for cf in context_files:
                f.write(f"- {cf}\n")
            if missing_files:
                for mf in missing_files:
                    f.write(f"- MISSING: {mf}\n")
            f.write("\n## Exchange\n\n")
            f.write(f"**Manager:** {message}\n\n")
            f.write(f"**{agent.title()}:** {response}\n\n")
            f.write("---\n")

    return log_file


def extract_memory_update(response: str) -> str | None:
    """Extract [MEMORY UPDATE] section from agent response.

    Returns the memory update content, or None if no update found.
    """
    marker = "[MEMORY UPDATE]"
    idx = response.find(marker)
    if idx == -1:
        return None

    # Extract everything after the marker
    after = response[idx + len(marker):]

    # Find the end — next section header (##) or end of string
    lines = after.splitlines()
    result_lines: list[str] = []
    for line in lines:
        if line.startswith("## ") or line.startswith("# "):
            break
        result_lines.append(line)

    content = "\n".join(result_lines).strip()
    return content if content else None


def build_prompt(
    system_prompt: str,
    docs: list[dict],
    memory: str | None,
    message: str,
) -> dict:
    """Build the full prompt payload for the Anthropic API.

    Returns dict with 'system' and 'messages' keys.
    """
    # Build system content: system prompt + context docs + memory
    system_parts = [system_prompt]

    if docs:
        system_parts.append("\n---\n\n## Context Documents\n")
        for doc in docs:
            system_parts.append(f"### {doc['name']} ({doc['path']})\n\n{doc['content']}\n")

    if memory:
        system_parts.append(f"\n---\n\n## Your Persistent Memory\n\n{memory}\n")

    return {
        "system": "\n".join(system_parts),
        "messages": [{"role": "user", "content": message}],
    }


def get_engineer_tools() -> list[dict]:
    """Return Anthropic tool definitions for the Engineer agent.

    Returns a list of tool definitions in Anthropic API format
    for use with messages.create(tools=...).
    """
    return [
        {
            "name": "run_backtest",
            "description": (
                "Execute a backtest using cached market data. Returns trade count, "
                "win rate, PnL, and whether results are statistically conclusive "
                "(>= 50 trades). Results are written to a CSV file."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "strategy_id": {
                        "type": "string",
                        "description": "Unique identifier for this strategy/hypothesis (e.g. 'HYP-001').",
                    },
                    "tickers": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of ticker symbols to backtest (e.g. ['MOBX', 'ASTS']).",
                    },
                    "dates": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of dates in YYYY-MM-DD format to backtest.",
                    },
                    "entry_rules": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "indicator": {"type": "string"},
                                "operator": {"type": "string"},
                                "value": {"type": "string"},
                                "params": {"type": "object"},
                            },
                            "required": ["indicator", "operator", "value"],
                        },
                        "description": "Entry signal rules.",
                    },
                    "exit_rules": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "indicator": {"type": "string"},
                                "operator": {"type": "string"},
                                "value": {"type": "string"},
                                "params": {"type": "object"},
                            },
                            "required": ["indicator", "operator", "value"],
                        },
                        "description": "Exit signal rules.",
                    },
                    "skip_first": {
                        "type": "boolean",
                        "description": "Skip the first entry signal (default: false).",
                    },
                    "atr_exit": {
                        "type": "object",
                        "properties": {
                            "multiplier": {"type": "string"},
                            "period": {"type": "integer"},
                        },
                        "description": "ATR-based stop loss. Optional.",
                    },
                    "volume_decay_exit": {
                        "type": "object",
                        "properties": {
                            "lookback": {"type": "integer"},
                            "threshold": {"type": "string"},
                        },
                        "description": "Volume decay exit. Optional.",
                    },
                    "force_close_eod": {
                        "type": "boolean",
                        "description": "Force close all positions at end of day (default: true).",
                    },
                },
                "required": ["strategy_id", "tickers", "dates", "entry_rules", "exit_rules"],
            },
        },
    ]


def main() -> None:
    """CLI entry point for single-agent invocation."""
    parser = argparse.ArgumentParser(description="Invoke a single YOLO Org Learning agent.")
    parser.add_argument("--agent", required=True, choices=["manager", "analyst", "engineer"],
                        help="Agent to invoke")
    parser.add_argument("--message", required=True, help="Message to send to the agent")
    parser.add_argument("--model", default="claude-haiku-4-5-20251001",
                        help="Anthropic model ID (default: claude-haiku-4-5-20251001)")
    parser.add_argument("--session-id", default=None,
                        help="Session ID for log grouping (default: auto-generated)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Build prompt and print without calling API")

    args = parser.parse_args()

    # Resolve paths
    agents_dir = Path(__file__).parent
    firm_repo = agents_dir.parent
    yolo_repo = firm_repo.parent / "yolo"

    agent_dir = agents_dir / args.agent
    system_prompt_path = agent_dir / "system-prompt.md"
    manifest_path = agent_dir / "context-manifest.md"
    memory_path = agent_dir / "memory.md"

    # Load system prompt
    if not system_prompt_path.is_file():
        print(f"ERROR: System prompt not found: {system_prompt_path}")
        raise SystemExit(1)
    system_prompt = system_prompt_path.read_text()

    # Parse manifest and load context
    if manifest_path.is_file():
        entries = parse_context_manifest(manifest_path)
        docs, missing = load_context(entries, firm_repo, yolo_repo)
    else:
        docs, missing = [], []

    # Load memory if it exists
    memory = memory_path.read_text() if memory_path.is_file() else None

    # Build prompt
    prompt = build_prompt(system_prompt, docs, memory, args.message)

    # Generate session ID
    session_id = args.session_id or f"{args.agent}-{datetime.now(UTC).strftime('%H%M%S')}"

    if args.dry_run:
        print(f"=== DRY RUN: {args.agent} ===")
        print(f"Model: {args.model}")
        print(f"Session: {session_id}")
        print(f"Context docs: {len(docs)} loaded, {len(missing)} missing")
        if missing:
            print(f"Missing: {missing}")
        print(f"System prompt length: {len(prompt['system'])} chars")
        print(f"Message: {args.message}")
        print("=== END DRY RUN ===")
        return

    # Call Anthropic API
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        raise SystemExit(1)

    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic package not installed. Run: pip install anthropic")
        raise SystemExit(1)

    client = anthropic.Anthropic(api_key=api_key)
    api_response = client.messages.create(
        model=args.model,
        max_tokens=4096,
        system=prompt["system"],
        messages=prompt["messages"],
    )

    response_text = api_response.content[0].text

    # Write session log
    log_dir = agents_dir / "session-log"
    log_dir.mkdir(exist_ok=True)
    context_files = [d["path"] for d in docs]
    write_session_log(
        log_dir=log_dir,
        session_id=session_id,
        agent=args.agent,
        model=args.model,
        context_files=context_files,
        missing_files=missing,
        message=args.message,
        response=response_text,
    )

    # Check for memory updates
    memory_update = extract_memory_update(response_text)
    if memory_update:
        pending_path = agents_dir / "memory-pending.md"
        with open(pending_path, "a") as f:
            f.write(f"\n## {args.agent.title()} — {session_id}\n\n{memory_update}\n")
        print(f"[MEMORY] Update pending PO approval → {pending_path}")

    # Print response
    print(response_text)

    # Print token usage
    usage = api_response.usage
    print(f"\n---\nTokens: {usage.input_tokens} in / {usage.output_tokens} out")


if __name__ == "__main__":
    main()
