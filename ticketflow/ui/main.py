import streamlit as st
from pathlib import Path
from ticketflow.config import cfg          # ← correct import
from ticketflow.core import parse_md_ticket, create_ticket

def launch_ui() -> None:
    st.set_page_config(page_title="TicketFlow", layout="wide")
    st.title("📋 TicketFlow")

    ticket_dir_value = cfg("defaults", "ticket_dir", default="tickets")
    ticket_dir = Path(str(ticket_dir_value)) / "open"
    files = sorted(ticket_dir.glob("*.md"))

    # Sidebar – create ticket
    with st.sidebar:
        st.header("New ticket")
        new_title = st.text_input("Title", "")
        github_issue_default = bool(
            cfg("defaults", "auto_create_github_issue", default=False)
        )
        github_issue = st.checkbox("Create GitHub Issue", value=github_issue_default)

        if st.button("Create"):
            if not new_title.strip():
                st.error("Title cannot be empty")
            else:
                ticket_path = create_ticket(
                    new_title,
                    open_in_editor=False,
                    github_issue=github_issue,
                )
                st.success(f"Created {ticket_path.name}")
                st.rerun()

    # Main table
    st.subheader(f"Open tickets ({len(files)})")
    rows = [
        {"ID": parse_md_ticket(md)[0], "Title": parse_md_ticket(md)[1], "File": md}
        for md in files
    ]
    st.dataframe(rows, hide_index=True)

    # Preview pane (simple MVP)
    if "selected_row" in st.session_state:
        sel = st.session_state["selected_row"]
        st.markdown(sel["File"].read_text())
