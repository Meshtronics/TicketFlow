import streamlit as st
from pathlib import Path
import logging

from ticketflow.config import cfg

ticket_dir_value = cfg("defaults", "ticket_dir", default="tickets")
TICKETS_DIR = Path(str(ticket_dir_value)) / "open"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="TicketFlow", layout="wide")
st.title("📋 TicketFlow Dashboard (MVP stub)")

files = sorted(TICKETS_DIR.glob("*.md"))
st.info(f"{len(files)} open tickets detected in {TICKETS_DIR.relative_to(Path.cwd())}")

logger.info(f"Ticket directory resolved to: {TICKETS_DIR}")
logger.info(f"Markdown files found: {len(files)}")

for f in files:
    logger.info(f"Processing file: {f}")
    with st.expander(f.name, expanded=False):
        st.markdown(f.read_text())
