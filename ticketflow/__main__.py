# ticketflow/__main__.py
import typer
from ticketflow.ui.main import launch_ui
app = typer.Typer()
app.command()(launch_ui)
if __name__ == "__main__":
    app()