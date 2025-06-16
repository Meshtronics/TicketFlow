import streamlit as st
from pathlib import Path
import logging
from ticketflow.config import cfg
from ticketflow.core import create_ticket, list_tickets, edit_ticket, move_ticket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    st.set_page_config(page_title="TicketFlow", layout="wide")
    st.title("📋 TicketFlow Dashboard")

    ticket_dir = Path(str(cfg("defaults", "ticket_dir", default="tickets")))

    open_tab, archived_tab = st.tabs(["Open", "Archived"])

    with open_tab:
        open_tickets = list_tickets("open")
        st.subheader("Open Tickets")
        for t in open_tickets:
            with st.expander(f"{t['id']} — {t['title']}"):
                path = Path(t["path"])
                text = path.read_text(encoding="utf-8")
                if st.text_area("Edit", text, key=t['id']):
                    pass
                if st.button("Save", key=f"save-{t['id']}"):
                    edit_ticket(t['id'], st.session_state[t['id']])
                if st.button("Archive", key=f"arch-{t['id']}"):
                    move_ticket(t['id'], archive=True)

    with archived_tab:
        archived = list_tickets("archive")
        st.subheader("Archived Tickets")
        for t in archived:
            with st.expander(f"{t['id']} — {t['title']}"):
                if st.button("Restore", key=f"restore-{t['id']}"):
                    move_ticket(t['id'], archive=False)
                st.markdown(Path(t['path']).read_text(encoding="utf-8"))

    st.sidebar.header("New Ticket")
    new_title = st.sidebar.text_input("Title")
    if st.sidebar.button("Create") and new_title.strip():
        create_ticket(new_title, open_in_editor=False)
        st.experimental_rerun()


if __name__ == "__main__":
    main()
