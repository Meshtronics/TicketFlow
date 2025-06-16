#!/usr/bin/env python3
"""
Regenerate TICKETS_INDEX.md — a markdown table of all open tickets.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from ticketflow.core import parse_md_ticket

ROOT = Path(__file__).resolve().parent.parent
OPEN_DIR = ROOT / "tickets" / "open"
INDEX_FILE = ROOT / "TICKETS_INDEX.md"

HEADER = (
    "| Ticket ID | Title | Status |\n"
    "|-----------|-------|--------|\n"
)

# Regex tolerates normal hyphen or em‑dash and any amount of whitespace
HEADING_RE = re.compile(
    r"""Ticket\s+
        (?P<id>\d{4}-\d{2}-\d{2}-\d{3})   # date‑based ID
        \s+[—-]\s+                        # em‑dash or hyphen
        (?P<title>.+?)$                   # greedy to EOL
    """,
    re.VERBOSE,
)


def parse_title(md_file: Path) -> tuple[str, str]:
    """Return (ticket_id, title).  Fall back to file stem if heading fails."""
    first_line = md_file.read_text(encoding="utf-8", errors="ignore").splitlines()[0]
    m = HEADING_RE.search(first_line)
    if m:
        return m.group("id"), m.group("title")
    # Fallback – derive ID from filename, title = "(unparsed)"
    return md_file.stem.split("_")[0], "(unparsed heading)"


def main() -> None:
    rows: list[str] = []
    for md in sorted(OPEN_DIR.glob("*.md")):
        ticket_id, title = parse_md_ticket(md)
        rows.append(f"| {ticket_id} | {title} | open |")

    body = HEADER + "\n".join(rows) if rows else "_No open tickets_"
    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    INDEX_FILE.write_text(
        f"<!-- auto‑generated {timestamp} -->\n"
        + body
        + "\n",
        encoding="utf-8",
    )
    print(f"Rebuilt {INDEX_FILE.relative_to(ROOT)} ({len(rows)} tickets)")


if __name__ == "__main__":
    main()
