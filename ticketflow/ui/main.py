import streamlit as st
from pathlib import Path
from ticketflow.config import cfg
from ticketflow.core import parse_md_ticket, create_ticket

def launch_ui() -> None:
    st.set_page_config(page_title="TicketFlow", layout="wide")
    st.title("📋 TicketFlow")

    ticket_dir_value = cfg("defaults", "ticket_dir", default="tickets")
    ticket_dir = Path(str(ticket_dir_value)) / "open"
    files = sorted(ticket_dir.glob("*.md"))

    # --- sidebar: create ticket --------------------------------------------
    with st.sidebar:
        st.header("New ticket")
        title = st.text_input("Title")
        gh_default = bool(cfg("defaults", "auto_create_github_issue", default=False))
        gh_flag = st.checkbox("Create GitHub Issue", value=gh_default)

        if st.button("Create"):
            if not title.strip():
                st.error("Title cannot be empty")
            else:
                path = create_ticket(title, open_in_editor=False, github_issue=gh_flag)
                st.success(f"Created {path.name}")
                st.rerun()

    # --- main table ---------------------------------------------------------
    st.subheader(f"Open tickets ({len(files)})")
    rows = [
        {"ID": parse_md_ticket(md)[0], "Title": parse_md_ticket(md)[1]}
        for md in files
    ]
    st.dataframe(rows, hide_index=True)
