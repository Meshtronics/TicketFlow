<!--
README.md  —  TicketFlow
-------------------------------------------------------------------------------
Starter, AI‑friendly ticketing & backlog system you can drop into any project
via “Use this template” on GitHub.
-->

🗂️ TicketFlow
==============

**TicketFlow** gives every repository a lightweight, self‑contained workflow for writing, tracking, and closing development tickets that both **humans *and* AI assistants** (GitHub Copilot, OpenAI Codex, etc.) can consume *offline*.

-   No external SaaS boards

-   No proprietary formats

-   One **`/ticketflow`** folder in your repo = the single source of truth

* * * * *

✨ What you get
--------------

| Capability | How it works |
| --- | --- |
| **Open / archive ticket folders** | Markdown files in `ticketflow/tickets/open/` and `ticketflow/tickets/archive/` |
| **Ticket helper scripts** | `ticketflow/scripts/new_ticket.py`, `move_ticket.py`, `build_index.py` |
| **Streamlit dashboard (stub)** | `ticketflow gui` → browse tickets in a browser |
| **Issue ↔ ticket mirroring** (opt‑in) | Re‑usable GitHub Action (`meshtronics/ticketflow@v1`) |
| **Repo instructions for AI** | `.github/copilot-instructions.md` (editable) |
| **Template‑repo flag** | Click **Use this template** to bootstrap future projects |

Everything under **`template/`** is copied into each new project that adopts TicketFlow. The rest (Streamlit UI, Action source) lives here so you can update and tag new releases centrally.

* * * * *

🚀 Quick start
--------------

### 1  Create a project from the template

bash

Copy

```# GitHub UI
New > Repository > From template > meshtronics/ticketflow
```

Clone your new project and you will see:

```ticketflow/
  ├─ tickets/
  │   ├─ open/
  │   │   └─ 0000-00-00-000_example.md
  │   └─ archive/
  ├─ scripts/
  └─ .ticketflow.yml
TICKETS_INDEX.md
.github/workflows/sync_issues.yml   # (optional)
.github/copilot-instructions.md
```

### 2  Create your first real ticket

```python ticketflow/scripts/new_ticket.py "Implement profile engine"
# Answer prompts; an .md file appears in ticketflow/tickets/open/
git add ticketflow/tickets TICKETS_INDEX.md
git commit -m "docs: add ticket 2025‑06‑18‑001"
git push
```

### 3  (Optional) open the browser UI

```pip install streamlit pydantic            # once per machine
ticketflow gui                            # or: python -m ticketflow.ui.streamlit_app
```

### 4  (Optional) mirror with GitHub Issues

Edit `.github/workflows/sync_issues.yml` in your project; keep or delete as you prefer. When enabled:

-   Opening / editing / closing an Issue automatically writes, updates, or moves the matching Markdown ticket.

-   Closing a ticket with `move_ticket.py` (or through the UI) can ping the Issue API to close the Issue too (PAT token required---see workflow file).

* * * * *

🗂️ Folder map
--------------

```
ticketflow/
(ticketflow template repo root)
├─ .ticketflow.yml              ← default config copied downstream
├─ tickets/                     ← example open/archive folders
│   └─ open/0000-00-00-000_example.md
├─ scripts/                     ← helper scripts users will run
│   ├─ new_ticket.py
│   ├─ move_ticket.py
│   └─ build_index.py
├─ ticketflow/                  ← Python package for shared code & UI
│   ├─ __init__.py
│   ├─ __main__.py              ← so `python -m ticketflow ui` works
│   ├─ config.py                ← YAML loader (used by scripts & UI)
│   └─ ui/
│       └─ main.py              ← Streamlit app
├─ .github/
│   └─ workflows/
│       └─ sync_issues.yml      ← copied downstream; calls reusable Action
├─ action/                      ← Dockerfile + entrypoint for Action
│   ├─ Dockerfile
│   └─ entrypoint.sh
├─ README.md
└─ LICENSE

 ```

* * * * *

⚙️ Helper script cheatsheet
---------------------------

| Command | What it does |
| --- | --- |
| `python ticketflow/scripts/new_ticket.py "Title"` | Generates a new ticket with date/ID slug, opens in `$EDITOR`, updates index |
| `python ticketflow/scripts/move_ticket.py TICKET_ID [--close-issue]` | Moves ticket to `archive/` and (optionally) closes linked Issue |
| `python ticketflow/scripts/build_index.py` | Rewrites **`TICKETS_INDEX.md`** (run in CI or pre‑commit) |

*All scripts are pure Python 3.10+, no external deps except `jinja2`.*

* * * * *

🛠️ Extending TicketFlow
------------------------

-   **Streamlit CRUD** -- flesh out `ticketflow/ui/streamlit_app.py` into a full editor with Pydantic validation and Issue API calls.

-   **Custom ticket schema** -- adjust the Markdown scaffold or enforce additional metadata with YAML front‑matter if you like.

-   **CI gates** -- lint tickets for missing sections; require at least one open ticket reference in every feature PR.

* * * * *

📄 License
----------

Released under the GNU Affero v3.0 License - please review before using for commercial work.

* * * * *

### Happy shipping 🚢

TicketFlow keeps your backlog **in‑repo, AI‑friendly, and click‑simple** so you can spend time building features, not copying issues around.
