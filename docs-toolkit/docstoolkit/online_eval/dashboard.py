"""HTML dashboard для continuous online eval.

Sprint 56 / M5 — dashboard step.

Использование:
    from docstoolkit.online_eval import OnlineEvalStore, render_dashboard

    store = OnlineEvalStore()
    html = render_dashboard(store, window_days=7)
    Path("eval-dashboard.html").write_text(html, encoding="utf-8")
"""
from __future__ import annotations

from datetime import datetime, timezone
from html import escape

from docstoolkit.online_eval.runner import (
    DriftReport,
    OnlineEvalRun,
    OnlineEvalStore,
)


_METRICS = ("precision", "recall", "f1", "citation_precision", "answer_score")


def _row(label: str, baseline: float, current: float, delta: float, sig: bool) -> str:
    arrow = "▲" if delta > 0 else ("▼" if delta < 0 else "→")
    cls = "sig" if sig else "ok"
    return (
        f"<tr class='{cls}'>"
        f"<td>{escape(label)}</td>"
        f"<td class='num'>{baseline:.3f}</td>"
        f"<td class='num'>{current:.3f}</td>"
        f"<td class='num'>{arrow} {delta:+.3f}</td>"
        f"</tr>"
    )


def _summary_table(reports: list[DriftReport]) -> str:
    rows = "".join(
        _row(r.metric, r.baseline_value, r.current_value, r.delta, r.significant)
        for r in reports
    )
    return (
        "<table class='summary'>"
        "<thead><tr><th>Метрика</th><th>Baseline</th>"
        "<th>Current</th><th>Delta</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def _recent_runs_table(runs: list[OnlineEvalRun], limit: int = 25) -> str:
    head = (
        "<tr><th>ts</th><th>query</th><th>precision</th>"
        "<th>recall</th><th>f1</th><th>answer</th><th>ms</th></tr>"
    )
    body = []
    for r in runs[:limit]:
        body.append(
            "<tr>"
            f"<td>{escape(r.ts)}</td>"
            f"<td class='q'>{escape(r.query[:80])}</td>"
            f"<td class='num'>{r.precision:.2f}</td>"
            f"<td class='num'>{r.recall:.2f}</td>"
            f"<td class='num'>{r.f1:.2f}</td>"
            f"<td class='num'>{r.answer_score:.2f}</td>"
            f"<td class='num'>{r.duration_ms}</td>"
            "</tr>"
        )
    return f"<table class='runs'><thead>{head}</thead><tbody>{''.join(body)}</tbody></table>"


_CSS = """
body{font-family:system-ui,sans-serif;margin:2rem;color:#222}
h1{margin-top:0}
table{border-collapse:collapse;margin:1rem 0;width:100%}
th,td{border:1px solid #ddd;padding:.3rem .6rem;text-align:left;font-size:14px}
th{background:#f3f3f3}
td.num{text-align:right;font-variant-numeric:tabular-nums}
td.q{font-family:ui-monospace,monospace}
tr.sig td{background:#fff5e6}
tr.ok td{background:#fafafa}
.meta{color:#666;font-size:12px}
"""


def render_dashboard(
    store: OnlineEvalStore,
    *,
    window_days: int = 7,
    title: str = "Continuous Online Eval — Dashboard",
) -> str:
    """Render full HTML dashboard for the last `window_days` of eval runs."""
    runs = store.recent_runs(days=window_days)
    current = store.current_stats(days=window_days)
    baseline = store.baseline_stats(
        days_ago_start=window_days * 2,
        days_ago_end=window_days,
    )
    reports: list[DriftReport] = []
    for m in _METRICS:
        b = baseline.get(m, 0.0)
        c = current.get(m, 0.0)
        delta = c - b
        reports.append(DriftReport(
            metric=m, baseline_value=b, current_value=c,
            delta=delta, significant=abs(delta) > 0.1,
            window_days=window_days,
        ))
    now = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    return (
        "<!doctype html><meta charset=utf-8>"
        f"<title>{escape(title)}</title>"
        f"<style>{_CSS}</style>"
        f"<h1>{escape(title)}</h1>"
        f"<p class=meta>generated {escape(now)} · window={window_days}d · "
        f"runs={len(runs)}</p>"
        "<h2>Метрики (baseline vs current)</h2>"
        + _summary_table(reports)
        + "<h2>Последние запросы</h2>"
        + _recent_runs_table(runs)
    )
