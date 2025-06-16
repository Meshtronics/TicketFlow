# ticketflow/ui/main.py
import streamlit as st
from pathlib import Path
from ticketflow.config import cfg

def launch_ui() -> None:
    st.set_page_config(page_title="TicketFlow", layout="wide")
    st.title("📋 TicketFlow")

    ticket_dir = Path(cfg("defaults", "ticket_dir", default="tickets")) / "open"
    files = sorted(ticket_dir.glob("*.md"))

    # Sidebar – create ticket
    with st.sidebar:
        st.header("New ticket")
        new_title = st.text_input("Title", "")
        github_issue = st.checkbox(
            "Create GitHub Issue",
            value=cfg("defaults", "auto_create_github_issue", default=False),
        )
        if st.button("Create"):
            if not new_title:
                st.error("Title cannot be empty")
            else:
                from ticketflow.scripts import new_ticket  # re‑use script logic
                ticket_path = new_ticket.create_ticket_cli(
                    title=new_title,
                    open_in_editor=False,
                    github_issue=github_issue,
                )
                st.success(f"Created {ticket_path.name}")
                st.rerun()  # refresh list

    # Main table
    st.subheader(f"Open tickets ({len(files)})")
    rows = []
    for md in files:
        ticket_id, title = parse_md_ticket(md)
        rows.append({"ID": ticket_id, "Title": title, "File": md})

    df = st.dataframe(rows, hide_index=True)

    # Preview pane
    selected = st.session_state.get("selected_row")
    if selected:
        st.markdown(selected["File"].read_text())
