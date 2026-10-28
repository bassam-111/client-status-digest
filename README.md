# Client Status Digest

A small operations tool that turns a task list into a per-client status digest.

It reads `tasks.csv`, groups tasks by client, and reports per client:
open vs total tasks, overdue count, next due date, and the overdue titles.
The same logic powers a one-page Flask dashboard and a plain-text digest
you can paste into a client update email.

Built with **Python, Flask, HTML/CSS** — skills on the resume, nothing extra claimed.

## How to run

```bash
pip install -r requirements.txt

# CLI digest (uses a fixed date for the demo so output is reproducible)
python digest.py tasks.csv 2026-10-28

# Web dashboard
python app.py
# then open http://127.0.0.1:5000
```

## Sample output

```
Client status digest as of 2026-10-28

Acme Media: 2 open of 3 total, 1 overdue, next due 2026-10-27
  OVERDUE: Deliver edited property photos
Harbor Realty: 2 open of 3 total, 0 overdue, next due 2026-10-28
Northwind Studio: 2 open of 2 total, 1 overdue, next due 2026-10-25
  OVERDUE: Follow up on revision request

Acme Media: open=2 overdue=1 next_due=2026-10-27
Harbor Realty: open=2 overdue=0 next_due=2026-10-28
Northwind Studio: open=2 overdue=1 next_due=2026-10-25
```

## Files

- `digest.py` — grouping, overdue logic, and plain-text digest (no framework dependency)
- `app.py` — Flask dashboard using the same logic
- `tasks.csv` — sample dataset of 8 tasks across 3 clients (sample data only)
- `requirements.txt` — Flask

## Try your own data

Replace `tasks.csv` with your own export keeping the same columns
(`id,client,title,status,due_date,owner`). Status `done` counts as closed;
anything else counts as open.
