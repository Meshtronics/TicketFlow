#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ticketflow.quality import score_ticket

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main() -> None:
    p = argparse.ArgumentParser(description="Score a TicketFlow ticket")
    p.add_argument("path", help="Path to ticket markdown")
    p.add_argument("--threshold", type=int, default=60, help="Fail below this score")
    args = p.parse_args()

    result = score_ticket(Path(args.path))
    print(json.dumps(result, indent=2))
    if result["total"] < args.threshold:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
