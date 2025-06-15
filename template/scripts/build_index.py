#!/usr/bin/env python3
"""
Regenerate TICKETS_INDEX.md — a markdown table of all open tickets.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

try:
    from jinja2 import Template
except ImportError:  # fallback if jinja2 is missing
    Template = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parent.parent
OPEN_DIR = ROOT / "tickets" / "open"
INDEX_FILE = ROOT / "TICKETS_INDEX.md"

ROW_TEMPLATE = "| {id} | {title} | {status} |"
HEADER = (
    "| Ticket ID | Title | Status |\n"
    "|-----------|-------|--------|\n"
)


def parse_title(path: Path) -> tuple[str, str]:
    """Extract ticket ID and first heading text."""
    first = path.read_text(encoding="utf‑8").splitlines()[0]
    # '# 🚧  Ticket 2025-06-18-003 — Title'
    parts = first.split("Ticket", 1)[1].split("—", 1)
    ticket_id = parts[0].strip()
    title = parts[1].strip()
    return ticket_id, title


def main() -> None:
    rows = []
    for md in sorted(OPEN_DIR.glob("*.md")):
        ticket_id, title = parse_title(md)
        rows.append(ROW_TEMPLATE.format(id=ticket_id, title=title, status="open"))

    body = HEADER + "\n".join(rows) if rows else "_No open tickets_"

    INDEX_FILE.write_text(
        f"<!-- auto‑generated on {datetime.utcnow().isoformat(timespec='seconds')}Z -->\n"
        + body
        + "\n",
        encoding="utf‑8",
    )
    print(f"Rebuilt {INDEX_FILE.relative_to(ROOT)} ({len(rows)} tickets)")


if __name__ == "__main__":
    main()
