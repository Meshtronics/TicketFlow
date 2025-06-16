from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ticketflow.package.quality import score_ticket


def test_perfect_ticket() -> None:
    path = Path("tests/fixtures/good_ticket.md")
    result = score_ticket(path)
    assert result["total"] == 100


def test_minimal_ticket() -> None:
    path = Path("tests/fixtures/bad_ticket.md")
    assert score_ticket(path)["total"] <= 20
