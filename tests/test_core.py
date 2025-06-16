from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ticketflow.core import create_ticket, move_ticket, list_tickets, edit_ticket


def test_create_and_move(tmp_path, monkeypatch):
    open_dir = tmp_path / "open"
    arch_dir = tmp_path / "archive"
    monkeypatch.setattr('ticketflow.core.ROOT', tmp_path)
    monkeypatch.setattr('ticketflow.core.OPEN_DIR', open_dir)
    monkeypatch.setattr('ticketflow.core.ARCH_DIR', arch_dir)

    path = create_ticket("Test Ticket", open_in_editor=False)
    assert path.exists()
    assert path.parent == open_dir

    edit_ticket(path.stem.split('_')[0], "Updated")
    assert path.read_text() == "Updated"

    moved = move_ticket(path.stem.split('_')[0], archive=True)
    assert moved.parent == arch_dir
    assert moved.exists()

    tickets = list_tickets("archive")
    assert tickets[0]['id'] == path.stem.split('_')[0]
