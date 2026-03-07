"""Research agenda orchestrator — runs sessions back-to-back.

Reads research-agenda.md, finds the next incomplete task, runs a session
for it, marks it complete, and loops until all tasks are done, max-sessions
is reached, or a pause/blocker flag is set.

Usage:
    python3 run_agenda.py [--max-sessions N] [--dry-run] [--status-every N]
"""

from __future__ import annotations

import argparse
import re
import time
from datetime import UTC, datetime
from pathlib import Path

from notify import send_pushover
from session import DEFAULT_MODEL, SessionResult, generate_session_id, run_session

AGENTS_DIR = Path(__file__).parent

_TASK_RE = re.compile(r"^- \[ \] (.+)$", re.MULTILINE)


def _find_next_task(content: str) -> str | None:
    """Find the first incomplete task line in agenda content.

    Returns the full task line (without the '- [ ] ' prefix), or None.
    """
    match = _TASK_RE.search(content)
    return match.group(1) if match else None


def _mark_task_complete(content: str, task_line: str) -> str:
    """Replace '- [ ] {task}' with '- [x] {task}' in agenda content."""
    return content.replace(f"- [ ] {task_line}", f"- [x] {task_line}", 1)


def _write_run_log(
    agents_dir: Path,
    session_logs: list[dict],
    total_cost: float,
    total_elapsed: float,
) -> Path:
    """Write agenda-run-log.md with per-session breakdown."""
    log_path = agents_dir / "agenda-run-log.md"
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# Agenda Run Log — {now}\n",
        f"\nTotal sessions: {len(session_logs)}",
        f"Total cost: ${total_cost:.4f}",
        f"Total elapsed: {total_elapsed / 60:.1f} min\n",
        "\n| # | Session ID | Task | Cost | Duration | Outcome |",
        "|---|---|---|---|---|---|",
    ]
    for i, entry in enumerate(session_logs, 1):
        lines.append(
            f"| {i} | {entry['session_id']} | {entry['task'][:50]} "
            f"| ${entry['cost']:.4f} | {entry['duration']:.0f}s "
            f"| {entry['outcome']} |",
        )
    lines.append("")

    log_path.write_text("\n".join(lines))
    return log_path


def run_agenda(
    max_sessions: int = 50,
    dry_run: bool = False,
    status_every: int = 3,
    model: str = DEFAULT_MODEL,
) -> None:
    """Run research sessions back-to-back from research-agenda.md.

    Args:
        max_sessions: Maximum number of sessions to run.
        dry_run: Print plan without executing sessions.
        status_every: Send status update every N sessions.
        model: Anthropic model ID.
    """
    agents_dir = AGENTS_DIR
    agenda_path = agents_dir / "research-agenda.md"

    if not agenda_path.is_file():
        print("ERROR: research-agenda.md not found")
        return

    agenda_content = agenda_path.read_text()
    print("=== RESEARCH AGENDA ===")
    print(f"File: {agenda_path}")

    if dry_run:
        print("\n--- DRY RUN: Tasks that would be executed ---")
        content = agenda_content
        task_num = 0
        while True:
            task = _find_next_task(content)
            if not task:
                break
            task_num += 1
            print(f"  {task_num}. {task}")
            content = _mark_task_complete(content, task)
            if task_num >= max_sessions:
                print(f"  (capped at --max-sessions {max_sessions})")
                break
        if task_num == 0:
            print("  No incomplete tasks found.")
        print("--- END DRY RUN ---")
        return

    start_time = time.monotonic()
    session_logs: list[dict] = []
    total_cost = 0.0

    for session_num in range(1, max_sessions + 1):
        # Check pause flag between sessions
        pause_flag = agents_dir / "pause.flag"
        if pause_flag.exists():
            print(
                f"\n[agenda] Paused (pause.flag found). {session_num - 1} sessions completed."
            )
            send_pushover(
                "Research Paused",
                f"⏸ Research paused (pause.flag set). "
                f"{session_num - 1} sessions completed.",
                priority=0,
            )
            break

        # Check blocker flag
        blocker_flag = agents_dir / "blocker.flag"
        if blocker_flag.exists():
            print("\n[agenda] Blocker flag found. Stopping.")
            break

        # Read current agenda state
        agenda_content = agenda_path.read_text()
        task = _find_next_task(agenda_content)
        if not task:
            print("\n[agenda] All tasks complete!")
            elapsed = time.monotonic() - start_time
            send_pushover(
                "Agenda Complete",
                f"✅ Agenda complete. {session_num - 1} sessions, "
                f"${total_cost:.4f} total cost, "
                f"{elapsed / 60:.1f} min elapsed.",
                priority=0,
            )
            break

        # Generate session ID and run
        session_id = generate_session_id()
        question = f"Research agenda task: {task}"
        print(f"\n=== AGENDA SESSION {session_num} — {session_id} ===")
        print(f"Task: {task[:80]}")

        result: SessionResult = run_session(
            question=question,
            open_mode=False,
            model=model,
            session_id=session_id,
            dry_run=False,
        )

        # Log session result
        session_logs.append(
            {
                "session_id": result.session_id,
                "task": task,
                "cost": result.cost_usd,
                "duration": result.duration_seconds,
                "outcome": result.outcome,
            }
        )
        total_cost += result.cost_usd

        # Mark task complete in agenda file
        agenda_content = agenda_path.read_text()
        updated = _mark_task_complete(agenda_content, task)
        agenda_path.write_text(updated)
        print(f"[agenda] Task marked complete: {task[:60]}")

        # Check if session hit a blocker
        if result.outcome == "blocker":
            print("[agenda] Session ended with blocker. Stopping.")
            break

        # Status update every N sessions
        if session_num % status_every == 0:
            elapsed = time.monotonic() - start_time
            send_pushover(
                "Research Status",
                f"📊 Research update: session {session_num}, "
                f"cost ${total_cost:.4f}, "
                f"elapsed {elapsed / 60:.1f} min.",
                priority=-1,
            )

    # Write run log
    elapsed = time.monotonic() - start_time
    log_path = _write_run_log(agents_dir, session_logs, total_cost, elapsed)
    print("\n=== AGENDA RUN COMPLETE ===")
    print(f"Sessions: {len(session_logs)}")
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Elapsed: {elapsed / 60:.1f} min")
    print(f"Run log: {log_path}")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run research sessions from research-agenda.md.",
    )
    parser.add_argument(
        "--max-sessions",
        type=int,
        default=50,
        help="Maximum sessions to run (default: 50)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print agenda tasks without executing sessions",
    )
    parser.add_argument(
        "--status-every",
        type=int,
        default=3,
        help="Send status update every N sessions (default: 3)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Anthropic model ID (default: {DEFAULT_MODEL})",
    )

    args = parser.parse_args()
    run_agenda(
        max_sessions=args.max_sessions,
        dry_run=args.dry_run,
        status_every=args.status_every,
        model=args.model,
    )


if __name__ == "__main__":
    main()
