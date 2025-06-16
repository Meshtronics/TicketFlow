from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# Section weights
WEIGHTS: dict[str, int] = {
    "metadata": 10,
    "background": 15,
    "requirements": 25,
    "implementation": 25,
    "files": 15,
    "clarity": 10,
}


class TicketScorer:
    """Score a Markdown ticket according to the rubric."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.lines = text.splitlines()

    def score(self) -> dict[str, int]:
        sections: dict[str, int] = {
            "metadata": self._score_metadata(),
            "background": self._score_has_heading("background"),
            "requirements": self._score_has_heading("requirement"),
            "implementation": self._score_has_heading("implementation"),
            "files": self._score_has_heading("file"),
            "clarity": self._score_clarity(),
        }
        return sections

    # ---- private helpers -------------------------------------------------
    def _score_metadata(self) -> int:
        first = self.lines[0].lower() if self.lines else ""
        id_match = re.search(r"\d{4}-\d{2}-\d{2}-\d{3}", first)
        has_title = first.startswith("#")
        return WEIGHTS["metadata"] if id_match and has_title else 0

    def _score_has_heading(self, keyword: str) -> int:
        pattern = re.compile(r"^#+\s.*" + keyword, re.IGNORECASE)
        for line in self.lines:
            if pattern.search(line):
                weight_key = {
                    "background": "background",
                    "requirement": "requirements",
                    "implementation": "implementation",
                    "file": "files",
                }[keyword]
                return WEIGHTS[weight_key]
        return 0

    def _score_clarity(self) -> int:
        has_bullets = any(line.lstrip().startswith(("-", "*")) for line in self.lines)
        has_todo = any("todo" in line.lower() for line in self.lines)
        return WEIGHTS["clarity"] if has_bullets and not has_todo else 0


def score_ticket(path: Path) -> dict:
    """Return rubric section scores and total."""
    text = Path(path).read_text(encoding="utf-8")
    scorer = TicketScorer(text)
    sections = scorer.score()
    total = sum(sections.values())
    return {"total": min(total, 100), "sections": sections}
