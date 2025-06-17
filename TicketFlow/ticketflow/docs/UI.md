# TicketFlow Streamlit UI

The Streamlit dashboard allows you to manage tickets without using the CLI. Run:

```bash
python -m ticketflow ui
```

The app shows open tickets and archived tickets in separate tabs. You can create
new tickets from the sidebar, edit existing ones and archive or restore them.
All operations invoke the functions from `ticketflow.core` so the behaviour is
the same as the CLI tools.
