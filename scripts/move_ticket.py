#!/usr/bin/env python3
"""
Move a ticket from tickets/open/ to tickets/archive/.
Optional: close the matching GitHub Issue if `gh` CLI is available.
"""
from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import Final

from src.config import cfg
from src.core import move_ticket

logger = logging.getLogger(__name__)

ROOT: Final = Path(__file__).resolve().parent.parent
ticket_dir = str(cfg("defaults", "ticket_dir", default="tickets"))
OPEN_DIR: Final = ROOT / ticket_dir / "open"
ARCH_DIR: Final = ROOT / ticket_dir / "archive"
TICKET_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{3}$")



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

    try:
        move_ticket(args.ticket_id, archive=True, close_issue=args.close_issue)
        logger.info("📦  Moved %s to archive", args.ticket_id)
    except FileNotFoundError:
        sys.exit("Ticket not found")


if __name__ == "__main__":
    main()
