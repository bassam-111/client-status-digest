from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import date

from digest import load_tasks, render_digest, summarise


def test_summarise_uses_sample_data_counts():
    summary = summarise(load_tasks("tasks.csv"), date(2026, 10, 28))

    assert summary["Acme Media"] == {
        "total": 3,
        "open": 2,
        "overdue": 1,
        "next_due": "2026-10-27",
        "overdue_titles": ["Deliver edited property photos"],
        "open_titles": ["Deliver edited property photos", "Send final invoice"],
    }
    assert summary["Harbor Realty"]["total"] == 3
    assert summary["Harbor Realty"]["open"] == 2
    assert summary["Harbor Realty"]["overdue"] == 0
    assert summary["Harbor Realty"]["next_due"] == "2026-10-28"
    assert summary["Northwind Studio"]["overdue_titles"] == [
        "Follow up on revision request"
    ]


def test_render_digest_matches_expected_lines():
    summary = summarise(load_tasks("tasks.csv"), date(2026, 10, 28))

    digest = render_digest(summary, date(2026, 10, 28))

    assert "Client status digest as of 2026-10-28" in digest
    assert "Acme Media: 2 open of 3 total, 1 overdue, next due 2026-10-27" in digest
    assert "  OVERDUE: Deliver edited property photos" in digest
    assert "Harbor Realty: 2 open of 3 total, 0 overdue, next due 2026-10-28" in digest
    assert "Northwind Studio: 2 open of 2 total, 1 overdue, next due 2026-10-25" in digest
