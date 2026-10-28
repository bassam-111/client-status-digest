"""One-page Flask view of the client status digest (same logic as digest.py)."""
from datetime import date

from flask import Flask, render_template_string

from digest import load_tasks, summarise

app = Flask(__name__)

TEMPLATE = """
<!doctype html><html><head><meta charset="utf-8">
<title>Client Status Digest</title>
<style>body{font-family:system-ui,sans-serif;max-width:720px;margin:2em auto;padding:0 1em}
table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:6px 10px;text-align:left}
.overdue{color:#b00020;font-weight:bold}</style></head>
<body><h1>Client Status Digest — {{ today }}</h1>
<table><tr><th>Client</th><th>Open / Total</th><th>Overdue</th><th>Next due</th></tr>
{% for client, s in summary.items() %}
<tr><td>{{ client }}</td><td>{{ s.open }} / {{ s.total }}</td>
<td class="{{ 'overdue' if s.overdue else '' }}">{{ s.overdue }}</td>
<td>{{ s.next_due or '—' }}</td></tr>
{% endfor %}</table>
{% for client, s in summary.items() %}
<h2>{{ client }}</h2><ul>
{% for t in s.open_titles %}<li>{{ t }}</li>{% endfor %}</ul>
{% endfor %}</body></html>
"""


@app.route("/")
def index():
    return render_template_string(
        TEMPLATE, summary=summarise(load_tasks("tasks.csv"), date.today()),
        today=date.today().isoformat(),
    )


if __name__ == "__main__":
    app.run(debug=True)
