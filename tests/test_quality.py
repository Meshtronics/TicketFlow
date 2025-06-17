from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
FIXTURES = Path(__file__).resolve().parent / "fixtures"

from src.quality import score_ticket


def test_perfect_ticket() -> None:
    path = FIXTURES / "good_ticket.md"
    result = score_ticket(path)
    assert result["total"] == 100


def test_minimal_ticket() -> None:
    path = FIXTURES / "bad_ticket.md"
    assert score_ticket(path)["total"] <= 20
