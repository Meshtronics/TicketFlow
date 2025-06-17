#!/usr/bin/env python3
from __future__ import annotations
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ticketflow.core import create_ticket


def main() -> None:
    p = argparse.ArgumentParser(description="Create a new TicketFlow ticket.")
    p.add_argument("title", nargs="?", help="Short ticket title")
    p.add_argument("--no-edit", action="store_true", help="Do not open editor")
    p.add_argument("--github", action="store_true", help="Force create GitHub Issue")
    args = p.parse_args()

    title = args.title or input("Short ticket title: ").strip()
    create_ticket(
        title, open_in_editor=not args.no_edit, github_issue=args.github or None
    )


if __name__ == "__main__":
    main()
