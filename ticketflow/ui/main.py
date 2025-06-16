from __future__ import annotations

import logging
from pathlib import Path

import streamlit as st

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from ticketflow.config import cfg

logger = logging.getLogger(__name__)

def main() -> None:
    """Render the TicketFlow dashboard."""
    st.set_page_config(page_title="TicketFlow", layout="wide")
    st.title("📋 TicketFlow Dashboard")

    ticket_dir_value = cfg("defaults", "ticket_dir", default="tickets")
    tickets_dir = ROOT / str(ticket_dir_value) / "open"

    if not tickets_dir.exists():
        logger.warning(f"Tickets directory not found: {tickets_dir}")
        st.error(f"Tickets directory not found: `{tickets_dir}`")
        return

    files = sorted(tickets_dir.glob("*.md"))
    st.info(f"{len(files)} open tickets detected in `{tickets_dir}`")

    if not files:
        st.warning("No tickets found.")
        return

    for ticket_file in files:
        with st.expander(ticket_file.name, expanded=False):
            st.markdown(ticket_file.read_text(encoding="utf-8"))

if __name__ == "__main__":
    main()
