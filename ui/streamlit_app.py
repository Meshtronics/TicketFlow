import streamlit as st
from pathlib import Path

TICKETS_DIR = Path.cwd() / "tickets" / "open"

st.set_page_config(page_title="TicketFlow", layout="wide")
st.title("📋 TicketFlow Dashboard (MVP stub)")

files = sorted(TICKETS_DIR.glob("*.md"))
st.info(f"{len(files)} open tickets detected in {TICKETS_DIR.relative_to(Path.cwd())}")

for f in files:
    with st.expander(f.name, expanded=False):
        st.markdown(f.read_text())
