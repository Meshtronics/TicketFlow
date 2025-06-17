# 🚧  Ticket 2025-06-16-001 — Implement Ticket Quality Scoring (0-100)

<!--
Ticket ID naming convention: YYYY-MM-DD-###_<slug>.md
Place this file in: tickets/open/
-->

# Implement Ticket Quality Scoring (0 – 100)

| Field | Value |
|-------|-------|
| **Ticket ID** | 2025‑06‑16‑001 |
| **Created By** | Reasoning Model (GPT‑4‑o) |
| **Created On** | 2025‑06‑16 |
| **Priority** | Medium |
| **Status** | Open |

---

## 1. Background / Problem Statement
TicketFlow relies on well‑formed Markdown tickets as the contractual hand‑off from the “reasoning” agent to the “coding” agent.  
At present there is **no automated way** to judge how complete or useful a ticket is before the coding phase begins. This gap risks:

* Incomplete context → code that does not satisfy requirements  
* Extra human review cycles  
* Inconsistent ticket quality across contributors and projects  

A lightweight, automated *quality score* (0 – 100) will provide immediate feedback to authors (human or AI) and can be wired into CLI linting and the Streamlit UI to surface problems early.

---

## 2. Objective / Goals
1. **Design and implement** a scoring algorithm that inspects a Markdown ticket and returns an integer 0 – 100 that reflects its completeness and clarity.  
2. **Expose the score via CLI** (`ticketflow score <ticket_path>`).  
3. **Display the score in the UI** (ticket list and detail views).  
4. **Provide a JSON summary** for downstream tooling (e.g., CI gating).  
5. Keep implementation **dependency‑light** (Python stdlib + existing deps; avoid heavy ML for MVP).

---

## 3. Quality Scoring Rubric
| Section Weight | Criteria (examples) |
|----------------|---------------------|
| **Metadata (10 pts)** | Title, ID, status, priority present |
| **Background / Context (15 pts)** | Explains “why” and relevant domain info |
| **Requirements / Acceptance Criteria (25 pts)** | Clear, testable bullets or check‑list |
| **Implementation Plan (25 pts)** | Concrete steps, affected modules, pseudo‑code hints |
| **Related Files (15 pts)** | Accurate list of code/docs to modify or review |
| **Clarity & Formatting (10 pts)** | Uses markdown headings, bullet lists, no TODO placeholders |

Score calculation = Σ section scores (cap at 100).  
A ticket with missing sections automatically gets 0 for that section.

Thresholds (for later CI use):  
* **≥ 80** – Ready  
* **60‑79** – Needs Review  
* **< 60** – Insufficient

---

## 4. Implementation Plan
1. **Module & Script**
   * Create `ticketflow/quality.py` containing:
     * `class TicketScorer` – parses Markdown (use `markdown` or regex) and applies rubric.
     * `def score_ticket(path) -> dict` – returns dict with section scores and total.
   * New CLI entry‑point `ticketflow/scripts/score_ticket.py`:
     ```bash
     ticketflow score tickets/open/2025-06-16-001_ticket-quality-score.md
     # → {"total": 95, "sections": {...}}
     ```
2. **CLI Integration**
   * Update `ticketflow/__main__.py` (`argparse`) to add `score` sub‑command.
3. **UI Integration**
   * Extend Streamlit GUI:
     * Show numeric badge next to each ticket in list view.
     * Detail view: progress‑bar + section‑by‑section breakdown.
4. **Documentation**
   * Update `README.md` and `docs/USAGE.md` with examples.
5. **Tests**
   * Unit tests in `tests/test_quality.py` covering:
     * Perfect ticket → 100  
     * Minimal ticket (only title) → ≤ 20  
   * Add sample bad/good tickets in `tests/fixtures/`.
6. **Optional CI Gate (follow‑up)**
   * GitHub Action step to fail commit if any new/edited ticket scores `< 70`.

---

## 5. Acceptance Criteria
- [ ] Running `ticketflow score <ticket>` outputs JSON with `total` key (0‑100).  
- [ ] Scoring algorithm uses rubric weights stated above.  
- [ ] CLI returns exit‑code 1 if score < 60 (configurable flag `--threshold`).  
- [ ] Streamlit UI shows score badge in ticket list and a breakdown chart in detail view.  
- [ ] Unit tests achieve ≥ 90 % coverage of scoring logic.  
- [ ] Documentation updated with usage examples and rubric table.  

---

## 6. Related Files / Modules
| Path | Why |
|------|-----|
| `ticketflow/__main__.py` | Extend CLI dispatcher |
| `ticketflow/scripts/` | New `score_ticket.py` |
| `ticketflow/quality.py` | **(new)** scoring logic |
| `ticketflow/gui/app.py` | Inject score in UI |
| `tests/` | Add unit tests & fixtures |
| `.github/workflows/ci.yml` | (future) optional gate |

---

## 7. Out of Scope
* Advanced NLP/LLM‑based semantic scoring – use rule‑based rubric for MVP.  
* Auto‑fixing tickets; only scoring/feedback.

---

## 8. Notes
* Consider caching parsed markdown to speed up repeated scoring in UI.  
* Rubric weights are provisional; store in `quality.py` as constants for easy tuning.  
* UI colours: green ≥ 80, amber 60‑79, red < 60.

---

## 9. References
* TicketFlow README “Extending TicketFlow” section (CI gate idea).  
* PairCoder & multi‑agent coding research showing benefit of clear plans.  
* Example ticket templates in `tickets/open/`.

---

> **Blocking ??** – None identified. Ready for coding once approved.

---
