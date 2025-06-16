#!/usr/bin/env python3
"""
Move a ticket from tickets/open/ to tickets/archive/.
Optional: close the matching GitHub Issue if `gh` CLI is available.
"""
from __future__ import annotations

import argparse
import logging
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Final

from ticketflow.config import cfg

logger = logging.getLogger(__name__)

ROOT: Final = Path(__file__).resolve().parent.parent
ticket_dir = str(cfg("defaults", "ticket_dir", default="tickets"))
OPEN_DIR: Final = ROOT / ticket_dir / "open"
ARCH_DIR: Final = ROOT / ticket_dir / "archive"
INDEX_SCRIPT: Final = Path(__file__).with_name("build_index.py")
TICKET_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{3}$")


def try_close_issue(ticket_id: str) -> None:
    """Close GitHub Issue that contains the ticket ID in title (best‑effort)."""
    if shutil.which("gh") is None:
        logger.info("ℹ️  GitHub CLI not found; skipping Issue close.")
        return

    try:
        subprocess.run(
            ["gh", "issue", "close", "--search", ticket_id],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.info("✅  Closed GitHub Issue containing “%s”", ticket_id)
    except subprocess.CalledProcessError:
        logger.warning("⚠️  Could not find or close matching GitHub Issue.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ticket_id", help="e.g. 2025-06-18-003")
    parser.add_argument(
        "--close-issue",
        "--github",
        action="store_true",
        dest="close_issue",
        help="Also close matching GitHub Issue (requires gh CLI)",
    )
    args = parser.parse_args()

    if not TICKET_RE.match(args.ticket_id):
        sys.exit("Invalid ticket ID format")

    matches = list(OPEN_DIR.glob(f"{args.ticket_id}_*.md"))
    if not matches:
        sys.exit("Ticket not found in tickets/open/")
    src = matches[0]

    ARCH_DIR.mkdir(parents=True, exist_ok=True)
    dest = ARCH_DIR / src.name
    src.rename(dest)
    logger.info("📦  Moved %s → tickets/archive/", src.name)

    if args.close_issue:
        try_close_issue(args.ticket_id)

    subprocess.run([sys.executable, str(INDEX_SCRIPT)], check=True)


if __name__ == "__main__":
    main()
