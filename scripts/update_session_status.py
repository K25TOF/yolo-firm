#!/usr/bin/env python3
"""Update status on an existing session index entry.

Usage:
    python scripts/update_session_status.py --id LC-2025-016 --status superseded --superseded-by LC-2025-017
    python scripts/update_session_status.py --id LC-2025-016 --status invalid
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from session_index import update_status


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Update session status.")
    parser.add_argument("--id", required=True, help="Session ID to update")
    parser.add_argument(
        "--status", required=True,
        choices=["active", "complete", "superseded", "invalid"],
        help="New status",
    )
    parser.add_argument("--superseded-by", default=None, help="ID of superseding session")
    args = parser.parse_args()

    index_path = Path(__file__).parent.parent / "research" / "session-log" / "index.json"

    success = update_status(
        index_path=index_path,
        session_id=args.id,
        status=args.status,
        superseded_by=args.superseded_by,
    )

    if success:
        print(f"Updated {args.id} → status={args.status}")
        if args.superseded_by:
            print(f"  superseded_by={args.superseded_by}")
    else:
        print(f"Session {args.id} not found in index.")
        sys.exit(1)


if __name__ == "__main__":
    main()
