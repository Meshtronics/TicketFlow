# Copilot Repository Instructions

## Coding conventions
* **Language:** Python ≥ 3.10.  
* **Formatting:** `black` (88‑char line length) + `ruff` for linting.  Run `black -q . && ruff --fix .` before committing.
* **Type hints:** Mandatory for all new functions and public methods (`from __future__ import annotations`).
* **Imports:** Standard library ⟶ third‑party ⟶ local, separated by a blank line.  No wildcard imports.
* **Logging:** Use the shared `import logging; logger = logging.getLogger(__name__)` pattern instead of bare `print`.
* **Change scope:** When tasked with a change, prefer to create a new function or class instead of modifying existing ones.  If you must modify, ensure the change is minimal and well‑documented.

## Testing
* Use **pytest**; name files `test_*.py`.
* Every new module requires at least one happy‑path unit test.
* Keep fixtures in `tests/conftest.py` or `tests/fixtures/`.

## Commit & branch naming
* Branches: `feat/<ticket‑id>‑<slug>` or `fix/<ticket‑id>‑<slug>`.
* Commit titles: `feat: <short description> (closes <ticket‑id>)`.
* Reference the ticket Markdown file path in the body when relevant.

## External libraries
* Prefer **standard library** first, then:  
  - `pandas` for tabular data  
  - `ruamel.yaml` for YAML that must round‑trip  
  - `pydantic` for data validation  
* Avoid heavy dependencies unless the ticket explicitly calls for them.

## Security & privacy
* Never embed tokens, passwords, or personal data in committed code.  Use environment variables or GitHub Secrets.
* Do not make outbound HTTP calls unless the ticket’s context requires it.

## Documentation
* Public functions/classes: one‑line summary + parameter/return docstring in Google style.
* Update `CHANGELOG.md` when a ticket introduces a new feature.

## Ticket‑aware behaviour
* If a ticket is referenced (e.g. `2025‑06‑18‑004_*`), read its **Definition of Done** carefully and honor file list and acceptance criteria.
* Place new files where the ticket specifies; if unclear, favour `src/` for production code and `scripts/` for runnable helpers.

> ✂ You can shorten, reorder, or extend these guidelines at any time; keep them under ~200 lines so Copilot can ingest them efficiently.
