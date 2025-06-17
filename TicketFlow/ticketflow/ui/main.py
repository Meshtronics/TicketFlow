"""Entry point to launch the Streamlit dashboard."""
from ticketflow.ui import streamlit_app


def main() -> None:
    streamlit_app.main()


if __name__ == "__main__":
    main()
