#!/usr/bin/env python3
"""
Create a new ticket Markdown file in tickets/open/ with a date‑based ID,
open it in $EDITOR, and rebuild TICKETS_INDEX.md.
"""
from __future__ import annotations

import os
import subprocess
from datetime import date
from pathlib import Path
from textwrap import dedent

TICKETS_DIR = Path(__file__).resolve().parent.parent / "tickets" / "open"
INDEX_SCRIPT = Path(__file__).with_name("build_index.py")


def slugify(text: str) -> str:
    return (
        "".join(c.lower() if c.isalnum() else "-" for c in text)
        .strip("-")
        .replace("--", "-")
    )


def next_ticket_id(today: date) -> str:
    prefix = today.strftime("%Y-%m-%d")
    existing = {
        p.stem.split("_")[0]  # 2025-06-18-003
        for p in TICKETS_DIR.glob(f"{prefix}-*.md")
    }
    next_num = 1
    while f"{prefix}-{next_num:03d}" in existing:
        next_num += 1
    return f"{prefix}-{next_num:03d}"


def main() -> None:
    TICKETS_DIR.mkdir(parents=True, exist_ok=True)
    title = input("Short ticket title: ").strip()
    if not title:
        print("Aborted – empty title.")
        return

    ticket_id = next_ticket_id(date.today())
    filename = f"{ticket_id}_{slugify(title)}.md"
    path = TICKETS_DIR / filename

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
    path.write_text(template, encoding="utf‑8")
    print(f"Created {path.relative_to(Path.cwd())}")

    # open in editor
    editor = os.getenv("EDITOR", "nano")
    subprocess.run([editor, str(path)])

    # rebuild index
    subprocess.run(["python", str(INDEX_SCRIPT)], check=True)


if __name__ == "__main__":
    main()
