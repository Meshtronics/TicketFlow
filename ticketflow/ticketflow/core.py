"""ticketflow.core – utilities shared by CLI, scripts and UI."""

from __future__ import annotations
import re
import os
import sys
import shutil
import subprocess
import webbrowser
from datetime import date
from pathlib import Path
from textwrap import dedent
from typing import Tuple
from ticketflow.config import cfg

# ---------- 1. Markdown heading parser -------------------------------------
_HEADING_RE = re.compile(
    r"""Ticket\s+
        (?P<id>\d{4}-\d{2}-\d{2}-\d{3})\s+[—-]\s+
        (?P<title>.+?)$""",
    re.VERBOSE,
)


def parse_md_ticket(md_file: Path) -> Tuple[str, str]:
    """Return (ticket‑ID, title). Fallback to filename if heading can’t be parsed."""
    first = md_file.read_text(encoding="utf-8", errors="ignore").splitlines()[0]
    m = _HEADING_RE.search(first)
    if m:
        return m.group("id"), m.group("title")
    return md_file.stem.split("_")[0], "(unparsed heading)"


# ---------- 2. Ticket‑creation engine --------------------------------------
ROOT = Path(__file__).resolve().parent.parent
ticket_dir = cfg("defaults", "ticket_dir", default="tickets")
if not isinstance(ticket_dir, str):
    ticket_dir = "tickets"
OPEN_DIR = ROOT / ticket_dir / "open"
INDEX_SCRIPT = ROOT / "scripts" / "build_index.py"


def _slug(txt: str) -> str:
    return (
        "".join(c.lower() if c.isalnum() else "-" for c in txt)
        .strip("-")
        .replace("--", "-")
    )


def _next_id() -> str:
    prefix = date.today().strftime("%Y-%m-%d")
    existing = {p.stem.split("_")[0] for p in OPEN_DIR.glob(f"{prefix}-*.md")}
    n = 1
    while f"{prefix}-{n:03d}" in existing:
        n += 1
    return f"{prefix}-{n:03d}"


def create_ticket(
    title: str, *, open_in_editor: bool = True, github_issue: bool | None = None
) -> Path:
    """Create a ticket .md (and optionally a GitHub Issue); return the Path."""
    if not title.strip():
        raise ValueError("Title cannot be empty")

    github_issue = (
        github_issue
        if github_issue is not None
        else bool(cfg("defaults", "auto_create_github_issue", default=False))
    )

    OPEN_DIR.mkdir(parents=True, exist_ok=True)
    ticket_id = _next_id()
    path = OPEN_DIR / f"{ticket_id}_{_slug(title)}.md"

    # --- optional Issue creation ------------------------------------------------
    if github_issue:
        cli = str(cfg("github", "cli_binary", default="gh"))
        if shutil.which(cli):
            labels_raw = cfg("github", "issue_labels", default=[])
            labels = ",".join(labels_raw) if isinstance(labels_raw, list) else ""
            subprocess.run(
                [
                    cli,
                    "issue",
                    "create",
                    "--title",
                    f"{ticket_id} {title}",
                    "--label",
                    labels,
                    "--body",
                    f"See `{ticket_id}` in repo /tickets.",
                ],
                check=False,
            )

    # --- write stub file --------------------------------------------------------
    path.write_text(
        dedent(
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
        ),
        encoding="utf-8",
    )

    print(f"✅  Created {path.relative_to(ROOT)}")

    if open_in_editor:
        if os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            webbrowser.open(f"file://{path}")

    subprocess.run([sys.executable, str(INDEX_SCRIPT)], check=False)
    return path
