"""Client status digest: group operations tasks by client.

Reads tasks.csv, groups open tasks per client, and reports:
- total / open / overdue tasks per client
- oldest open task and next follow-up due
- a short plain-text digest per client, ready to paste into an update email

No external services, no invented client data: the bundled tasks.csv is
sample data only. Replace it with your own export keeping the same columns.
"""
import csv
import sys
from collections import defaultdict
from datetime import date


def parse_date(value):
    value = (value or "").strip()
    if not value:
        return None
    year, month, day = (int(part) for part in value.split("-"))
    return date(year, month, day)


def load_tasks(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def summarise(tasks, today):
    clients = defaultdict(list)
    for task in tasks:
        clients[task["client"]].append(task)

    summary = {}
    for client, rows in clients.items():
        open_rows = [r for r in rows if r["status"].strip().lower() != "done"]
        overdue = [
            r for r in open_rows
            if (due := parse_date(r["due_date"])) and due < today
        ]
        due_dates = [parse_date(r["due_date"]) for r in open_rows]
        due_dates = [d for d in due_dates if d]
        summary[client] = {
            "total": len(rows),
            "open": len(open_rows),
            "overdue": len(overdue),
            "next_due": min(due_dates).isoformat() if due_dates else None,
            "overdue_titles": [r["title"] for r in overdue],
            "open_titles": [r["title"] for r in open_rows],
        }
    return summary


def render_digest(summary, today):
    lines = [f"Client status digest as of {today.isoformat()}", ""]
    for client in sorted(summary):
        s = summary[client]
        lines.append(
            f"{client}: {s['open']} open of {s['total']} total, "
            f"{s['overdue']} overdue, next due {s['next_due'] or '—'}"
        )
        for title in s["overdue_titles"]:
            lines.append(f"  OVERDUE: {title}")
    return "\n".join(lines)


def main(argv):
    path = argv[1] if len(argv) > 1 else "tasks.csv"
    today = parse_date(argv[2]) if len(argv) > 2 else date.today()
    summary = summarise(load_tasks(path), today)
    print(render_digest(summary, today))
    print()
    for client in sorted(summary):
        s = summary[client]
        print(f"{client}: open={s['open']} overdue={s['overdue']} next_due={s['next_due']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
