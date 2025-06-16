"""
ticketflow – lightweight CLI wrapper.

Commands
--------
ticketflow ui            # launch Streamlit dashboard
ticketflow new "Title"   # create ticket from CLI
"""

from __future__ import annotations
import argparse
import json
import os
import sys

from pathlib import Path

from core import create_ticket
from ticketflow.quality import score_ticket


def _launch_streamlit() -> None:
    # Replace current process with `streamlit run -m ticketflow.ui.main`
    cmd = ["streamlit", "run", "-m", "ticketflow.ui.main"]
    try:
        os.execvp(cmd[0], cmd)  # never returns
    except FileNotFoundError:
        raise FileNotFoundError(
            "Error: The 'streamlit' command was not found. "
            "Please ensure Streamlit is installed and that its installation directory is in your system's PATH. "
            "You can typically install it using: pip install streamlit"
        )


def main() -> None:
    p = argparse.ArgumentParser(prog="ticketflow")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("ui", help="Launch Streamlit dashboard")

    new = sub.add_parser("new", help="Create a new ticket")
    new.add_argument("title", help="Ticket title")
    new.add_argument("--no-edit", action="store_true")
    new.add_argument("--github", action="store_true", help="Force create GitHub Issue")

    score = sub.add_parser("score", help="Score a ticket")
    score.add_argument("path", help="Path to ticket markdown")
    score.add_argument(
        "--threshold", type=int, default=60, help="Fail below this score"
    )

    args = p.parse_args()

    if args.cmd == "ui" or args.cmd is None:  # default = ui
        _launch_streamlit()
    elif args.cmd == "new":
        create_ticket(
            args.title,
            open_in_editor=not args.no_edit,
            github_issue=args.github or None,
        )
    elif args.cmd == "score":
        result = score_ticket(Path(args.path))
        print(json.dumps(result, indent=2))
        if result["total"] < args.threshold:
            sys.exit(1)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
