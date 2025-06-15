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

-   One **`/tickets`** folder in your repo = the single source of truth

* * * * *

✨ What you get
--------------

| Capability | How it works |
| --- | --- |
| **Open / archive ticket folders** | Markdown files in `tickets/open/` and `tickets/archive/` |
| **Ticket helper scripts** | `scripts/new_ticket.py`, `move_ticket.py`, `build_index.py` |
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

```tickets/
  ├─ open/
  │   └─ 0000-00-00-000_example.md
  └─ archive/
scripts/
.github/workflows/sync_issues.yml   # (optional)
.github/copilot-instructions.md
TICKETS_INDEX.md
```

### 2  Create your first real ticket

```python scripts/new_ticket.py "Implement profile engine"
# Answer prompts; an .md file appears in tickets/open/
git add tickets TICKETS_INDEX.md
git commit -m "docs: add ticket 2025‑06‑18‑001"
git push
```

### 3  (Optional) open the browser UI

```pip install streamlit pydantic            # once per machine
ticketflow gui                            # or: python -m ui.streamlit_app
```

### 4  (Optional) mirror with GitHub Issues

Edit `.github/workflows/sync_issues.yml` in your project; keep or delete as you prefer. When enabled:

-   Opening / editing / closing an Issue automatically writes, updates, or moves the matching Markdown ticket.

-   Closing a ticket with `move_ticket.py` (or through the UI) can ping the Issue API to close the Issue too (PAT token required---see workflow file).

* * * * *

🗂️ Folder map
--------------

```template/
 ├─ tickets/               # Copied verbatim to every project
 │   ├─ open/
 │   └─ archive/
 ├─ scripts/
 │   ├─ new_ticket.py      # create
 │   ├─ move_ticket.py     # close/archive
 │   └─ build_index.py     # (re)generate backlog index
 └─ .github/
     └─ workflows/
         └─ sync_issues.yml    # plug‑and‑play action reference
ui/
 └─ streamlit_app.py        # evolving dashboard (read‑only MVP)
action/
 ├─ Dockerfile              # builds meshtronics/ticketflow Action
 └─ entrypoint.sh
.github/
 ├─ workflows/release.yml   # publishes the Action on tag
 └─ copilot-instructions.md # house coding rules (edit freely)
docs/
 └─ TEMPLATE_GUIDE.md       # deeper integration notes
 ```

* * * * *

⚙️ Helper script cheatsheet
---------------------------

| Command | What it does |
| --- | --- |
| `python scripts/new_ticket.py "Title"` | Generates a new ticket with date/ID slug, opens in `$EDITOR`, updates index |
| `python scripts/move_ticket.py TICKET_ID [--close-issue]` | Moves ticket to `archive/` and (optionally) closes linked Issue |
| `python scripts/build_index.py` | Rewrites **`TICKETS_INDEX.md`** (run in CI or pre‑commit) |

*All scripts are pure Python 3.10+, no external deps except `jinja2`.*

* * * * *

🛠️ Extending TicketFlow
------------------------

-   **Streamlit CRUD** -- flesh out `ui/streamlit_app.py` into a full editor with Pydantic validation and Issue API calls.

-   **Custom ticket schema** -- adjust the Markdown scaffold or enforce additional metadata with YAML front‑matter if you like.

-   **CI gates** -- lint tickets for missing sections; require at least one open ticket reference in every feature PR.

* * * * *

📄 License
----------

Released under the GNU Affero v3.0 License - please review before using for commercial work.

* * * * *

### Happy shipping 🚢

TicketFlow keeps your backlog **in‑repo, AI‑friendly, and click‑simple** so you can spend time building features, not copying issues around.
