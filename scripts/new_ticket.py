#!/usr/bin/env python3
"""
Create a new ticket Markdown file in tickets/open/ with a date‑based ID.

Usage examples
--------------
python scripts/new_ticket.py "Implement profile engine"
python scripts/new_ticket.py # will prompt for title
python scripts/new_ticket.py "Title" --no-edit
"""
from __future__ import annotations

import argparse
import platform
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from textwrap import dedent
from ticketflow.config import cfg  # type: ignore[import]

ROOT = Path(__file__).resolve().parent.parent
TICKETS_DIR = ROOT / "tickets" / "open"
INDEX_SCRIPT = Path(__file__).with_name("build_index.py")


def create_issue(ticket_id: str, title: str) -> None:
    cli_binary = str(cfg("github", "cli_binary", default="gh"))
    if shutil.which(cli_binary) is None:
        print("GitHub CLI not found; skipping Issue creation.")
        return
    labels = cfg("github", "issue_labels", default=[])
    if not isinstance(labels, list):
        labels = []
    cmd = [
        cli_binary,
        "issue", "create",
        "--title", f"{ticket_id} {title}",
        "--label", ",".join(labels),
        "--body", f"See `{ticket_id}` in repo /tickets.",
    ]
    subprocess.run(cmd, check=False)


def slugify(text: str) -> str:
    return (
        "".join(c.lower() if c.isalnum() else "-" for c in text)
        .strip("-")
        .replace("--", "-")
    )


def next_ticket_id(today: date) -> str:
    prefix = today.strftime("%Y-%m-%d")
    existing = {
        p.stem.split("_")[0] for p in TICKETS_DIR.glob(f"{prefix}-*.md")
    }
    n = 1
    while f"{prefix}-{n:03d}" in existing:
        n += 1
    return f"{prefix}-{n:03d}"


def pick_editor() -> list[str] | None:
    """
    Return a command list for subprocess.run or None.
    Order of preference:
      • $EDITOR     (if set and on PATH)
      • VS Code     ('code -r')
      • Notepad++   ('notepad++.exe')  if installed
      • Windows     ('notepad.exe')
      • *nix        ('nano')
    """
    env = os.getenv("EDITOR") or cfg("defaults", "editor_cmd")
    if isinstance(env, str) and env and shutil.which(env.split()[0]):
        return env.split()

    if shutil.which("code"):
        return ["code", "-r"]

    if shutil.which("notepad++.exe"):
        return ["notepad++.exe"]

    if os.name == "nt" and shutil.which("notepad.exe"):
        return ["notepad.exe"]

    if shutil.which("nano"):
        return ["nano"]

    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new ticket.")
    parser.add_argument("title", nargs="?", help="Short ticket title")
    parser.add_argument(
        "--no-edit",
        action="store_true",
        help="Skip opening the ticket in an editor",
    )
    args = parser.parse_args()

    title = args.title or input("Short ticket title: ").strip()
    if not title:
        sys.exit("Aborted – empty title.")
        
    TICKETS_DIR.mkdir(parents=True, exist_ok=True)
    ticket_id = next_ticket_id(date.today())
    filename = f"{ticket_id}_{slugify(title)}.md"
    path = TICKETS_DIR / filename

    if args.github or cfg("defaults", "auto_create_github_issue", default=False):
        create_issue(ticket_id, title)

    template = dedent(
        f"""\
        # 🚧  Ticket {ticket_id} — {title}

        **Goal / Definition of Done**  
        _Fill me in._

        **Context / Motivation**  
        _Why are we doing this?_

        **Deliverables**  
        - [ ] …

        **Relevant files / locations**  
        …

        **Notes for AI agents**  
        …

        ---

        _Status: open_  
        _Assignee: unassigned_
        """
    )
    path.write_text(template, encoding="utf-8")
    print(f"✅  Created {path.relative_to(ROOT)}")

    if not args.no_edit:
        cmd = pick_editor()
        if cmd:
            try:
                subprocess.run([*cmd, str(path)], check=False)
            except FileNotFoundError:
                print("⚠️  Editor command failed; fallback to default opener.")
                cmd = None

        if cmd is None:
            if os.name == "nt":
                os.startfile(str(path))  # type: ignore[attr-defined]
            else:
                webbrowser.open(f"file://{path}")

    # rebuild index
    subprocess.run([sys.executable, str(INDEX_SCRIPT)], check=True)


if __name__ == "__main__":
    main()
