#!/usr/bin/env python3
"""Query the session index for matching entries.

Usage:
    python scripts/query_sessions.py --topic "ORB"
    python scripts/query_sessions.py --agent challenger --has-blockers
    python scripts/query_sessions.py --status active
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from session_index import query


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Query session index.")
    parser.add_argument("--topic", help="Match against question/verdict (case-insensitive)")
    parser.add_argument("--agent", help="Match sessions with this agent")
    parser.add_argument("--has-blockers", action="store_true", help="Only sessions with blockers")
    parser.add_argument("--status", help="Filter by status (active|complete|superseded|invalid)")
    args = parser.parse_args()

    index_path = Path(__file__).parent.parent / "agents" / "session-log" / "index.json"

    results = query(
        index_path=index_path,
        topic=args.topic,
        agent=args.agent,
        has_blockers=args.has_blockers,
        status=args.status,
    )

    if not results:
        print("No matching sessions found.")
        return

    # Print as formatted table
    print(f"{'ID':<18} {'Date':<12} {'Status':<12} {'Flags':>5} {'Block':>5}  Question")
    print("-" * 80)
    for r in results:
        date_short = r.get("date", "")[:10]
        print(
            f"{r['id']:<18} {date_short:<12} {r.get('status', ''):<12} "
            f"{r.get('flag_count', 0):>5} {r.get('blocker_count', 0):>5}  "
            f"{r.get('question_summary', '')[:40]}"
        )


if __name__ == "__main__":
    main()
