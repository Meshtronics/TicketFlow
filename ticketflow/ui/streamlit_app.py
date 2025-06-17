import sys
from pathlib import Path

# Ensure the project root is in sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
import logging
from ticketflow.config import cfg
from ticketflow.core import create_ticket, list_tickets, edit_ticket, move_ticket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    st.set_page_config(page_title="TicketFlow", layout="wide")
    st.title("📋 TicketFlow Dashboard")

    # Use Streamlit session_state for messages
    if "success_message" not in st.session_state:
        st.session_state["success_message"] = ""
    if "fail_message" not in st.session_state:
        st.session_state["fail_message"] = ""

    if len(st.session_state["success_message"]) > 0:
        st.success(st.session_state["success_message"])
        st.session_state["success_message"] = ""
        
    if len(st.session_state["fail_message"]) > 0:
        st.error(st.session_state["fail_message"])
        st.session_state["fail_message"] = ""

    # Set the Streamlit Expander to use a custom HTML template
    st.markdown(
        """
        <style>
            /* Streamlit ≥ 1.28 renders an expander as
            <details>…<summary>…<p>Your label</p></summary>…</details> */
            div[data-testid="stExpander"] details summary p {
                font-size: 1.4rem;      /* 1.4 × root size ≈ 22 px */
                font-weight: 600;        /* optional – make it bolder */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Ensure ticket_dir is resolved relative to the project root
    ticket_dir = project_root / Path(str(cfg("defaults", "ticket_dir", default="tickets")))

    open_tab, archived_tab = st.tabs(["Open", "Archived"])

    with open_tab:
        open_tickets = list_tickets("open")
        st.subheader("Open Tickets")
        for t in open_tickets:
            if int(t['score']) > 80:
                icon = "💪"
            elif int(t['score']) > 60:
                icon = "👍"
            elif int(t['score']) < 20:
                icon = "💩"
            else:
                icon = "😞"          
                
            with st.expander(f"{t['id']} — {t['title']} (Score: {t['score']}) {icon}"):
                col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
                with col1:
                    st.markdown(f"<h3>{t['id']} — {t['title']} (Score: {t['score']})</h3>", unsafe_allow_html=True)
                    path = Path(t["path"])
                    text = path.read_text(encoding="utf-8")
                with col2:
                    disabled = t["id"].startswith("0000-00-00-000")
                    if st.button("Save", icon=":material/save:", key=f"save-{t['id']}"):
                        edit_ticket(t['id'], st.session_state[t['id']])
                        st.session_state["success_message"] = f"Ticket {t['id']} saved successfully."
                        st.rerun()  # refresh the page to show the updated ticket
                with col3:
                    disabled = t["id"].startswith("0000-00-00-000")
                    if st.button("Archive", icon=":material/archive:", key=f"arch-{t['id']}", disabled=disabled):
                        move_ticket(t['id'], archive=True)
                        st.session_state["success_message"] = f"Ticket {t['id']} archived successfully."
                        st.rerun()  # refresh the page to move the ticket to the archived tabab

                if st.text_area("Edit", text, height=400, key=t['id']):
                    pass


    with archived_tab:
        archived = list_tickets("archive")
        st.subheader("Archived Tickets")
        for t in archived:
            with st.expander(f"{t['id']} — {t['title']} (Score: {t['score']})"):
                st.markdown(f"<h3>{t['id']} — {t['title']} (Score: {t['score']})</h3>", unsafe_allow_html=True)
                if st.button("Restore", key=f"restore-{t['id']}"):
                    move_ticket(t['id'], archive=False)
                st.markdown(Path(t['path']).read_text(encoding="utf-8"))

    st.sidebar.header("New Ticket")
    new_title = st.sidebar.text_input("Title")
    if st.sidebar.button("Create") and new_title.strip():
        create_ticket(new_title, open_in_editor=False)
        st.rerun()


if __name__ == "__main__":
    main()
