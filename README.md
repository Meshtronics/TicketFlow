<!--
README.md  —  TicketFlow
-------------------------------------------------------------------------------
Starter, AI‑friendly ticketing & backlog system you can drop into any project
via “Use this template” on GitHub.
-->

# 🗂️ TicketFlow

**TicketFlow** gives every repository a lightweight, self‑contained workflow for
writing, tracking, and closing development tickets that both **humans _and_
AI assistants** (GitHub Copilot, OpenAI Codex, etc.) can consume _offline_.

* No external SaaS boards  
* No proprietary formats  
* One **`/tickets`** folder in your repo = the single source of truth

---

## ✨  What you get

| Capability | How it works |
|------------|--------------|
| **Open / archive ticket folders** | Markdown files in `tickets/open/` and `tickets/archive/` |
| **Ticket helper scripts** | `scripts/new_ticket.py`, `move_ticket.py`, `build_index.py` |
| **Streamlit dashboard (stub)** | `ticketflow gui` → browse tickets in a browser |
| **Issue ↔ ticket mirroring** (opt‑in) | Re‑usable GitHub Action (`meshtronics/ticketflow@v1`) |
| **Repo instructions for AI** | `.github/copilot-instructions.md` (editable) |
| **Template repo flag** | Click **Use this template** to bootstrap future projects |

Everything under **`template/`** is copied into each new project that adopts
TicketFlow.  The rest (Streamlit UI, Action source) lives here so you can update
and tag new releases centrally.

---

## 🚀  Quick start

### 1  Create a project from the template

```bash
# On GitHub UI
New > Repository > From template > meshtronics/ticketflow
