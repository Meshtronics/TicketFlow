# Using the TicketFlow Template

This short guide mirrors the main README but focuses only on the steps needed to start a project from the template.

## 1. Create a repository from the template

1. On GitHub choose **Use this template**.
2. Clone your new repository.
3. You will see the following structure:
   ```
   tickets/
     ├─ open/
     │   └─ 0000-00-00-000_example.md
     └─ archive/
   scripts/
   .github/
   TICKETS_INDEX.md
   ```

## 2. Create and manage tickets

* Run `python scripts/new_ticket.py "Title"` to generate a ticket. The script writes the Markdown file and updates `TICKETS_INDEX.md`.
* Commit the changes and push.
* When a ticket is finished, move it to the archive:
  ```
  python scripts/move_ticket.py TICKET_ID [--close-issue]
  ```
  This moves the file to `tickets/archive/` and optionally closes a linked GitHub Issue.
* Regenerate the index at any time with `python scripts/build_index.py`.

## 3. Optional extras

* `ticketflow gui` launches a browser UI for browsing and editing tickets (requires `streamlit`).
* `.github/workflows/sync_issues.yml` mirrors tickets with GitHub Issues if you keep it enabled.
* Edit `.ticketflow.yml` to tweak default paths or enable automatic Issue creation.

That's all you need to bootstrap a new project with TicketFlow.
