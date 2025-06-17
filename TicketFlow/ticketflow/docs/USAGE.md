# TicketFlow CLI Usage

## Scoring a Ticket

Run the `score` subcommand to evaluate ticket quality:

```bash
python -m ticketflow score path/to/ticket.md
```

The command prints a JSON object with a `total` score and per-section values. Use `--threshold` to fail below a score:

```bash
python -m ticketflow score ticket.md --threshold 80
```
