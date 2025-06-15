#!/usr/bin/env python3
"""
Move a ticket from tickets/open/ to tickets/archive/ and optionally close
the matching GitHub Issue via CLI flag (--close-issue).
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path
from typing import Final

OPEN_DIR: Final = Path(__file__).resolve().parent.parent / "tickets" / "open"
ARCH_DIR: Final = Path(__file__).resolve().parent.parent / "tickets" / "archive"
INDEX_SCRIPT: Final = Path(__file__).with_name("build_index.py")
TICKET_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{3}$")


def close_issue(ticket_id: str) -> None:
    """
    Try to close a GitHub issue with the same title as the ticket ID.
    Requires gh CLI installed and authenticated (`gh auth login`).
    """
    try:
        subprocess.run(
            ["gh", "issue", "close", "--search", ticket_id], check=True
        )
    except subprocess.CalledProcessError:
        print("⚠️  Could not close GitHub Issue – ignoring.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ticket_id", help="e.g. 2025-06-18-003")
    parser.add_argument("--close-issue", action="store_true")
    args = parser.parse_args()

    if not TICKET_RE.match(args.ticket_id):
        raise SystemExit("Invalid ticket ID format")

    matches = list(OPEN_DIR.glob(f"{args.ticket_id}_*.md"))
    if not matches:
        raise SystemExit("Ticket not found in tickets/open/")
    src = matches[0]
    ARCH_DIR.mkdir(parents=True, exist_ok=True)
    dest = ARCH_DIR / src.name
    src.rename(dest)
    print(f"Moved {src.name} → tickets/archive/")

    if args.close_issue:
        close_issue(args.ticket_id)

    subprocess.run(["python", str(INDEX_SCRIPT)], check=True)


if __name__ == "__main__":
    main()
