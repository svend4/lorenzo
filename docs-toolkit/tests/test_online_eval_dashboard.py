"""Tests for online_eval HTML dashboard (Sprint 56 / M5 dashboard step)."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from docstoolkit.online_eval import (
    OnlineEvalRun,
    OnlineEvalStore,
    render_dashboard,
)


@pytest.fixture
def store(tmp_path):
    s = OnlineEvalStore(db_path=tmp_path / "eval.sqlite")
    yield s
    s.close()


def _mk_run(seed: int = 0, ts: str | None = None) -> OnlineEvalRun:
    return OnlineEvalRun(
        id=f"id{seed:04d}",
        query=f"q{seed}",
        ts=ts or datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
        precision=0.5 + seed * 0.01,
        recall=0.4 + seed * 0.01,
        f1=0.45 + seed * 0.01,
        citation_precision=0.6,
        answer_score=0.7,
        retriever="hybrid",
        answerer="echo",
        duration_ms=100 + seed,
    )


def test_dashboard_returns_html_string(store):
    store.save_run(_mk_run(0))
    html = render_dashboard(store)
    assert isinstance(html, str)
    assert html.startswith("<!doctype html>")
    assert "Continuous Online Eval" in html


def test_dashboard_contains_metric_rows(store):
    store.save_run(_mk_run(0))
    html = render_dashboard(store)
    for metric in ("precision", "recall", "f1",
                   "citation_precision", "answer_score"):
        assert metric in html


def test_dashboard_lists_recent_runs(store):
    for i in range(3):
        store.save_run(_mk_run(i))
    html = render_dashboard(store)
    assert "q0" in html
    assert "q1" in html
    assert "q2" in html


def test_dashboard_empty_store_renders(store):
    html = render_dashboard(store)
    assert "<!doctype html>" in html
    # Should still render headers
    assert "Метрики" in html


def test_dashboard_escapes_query_text(store):
    run = _mk_run(0)
    run.query = "<script>alert(1)</script>"
    store.save_run(run)
    html = render_dashboard(store)
    assert "<script>alert" not in html  # must be escaped
    assert "&lt;script&gt;" in html


def test_dashboard_custom_title(store):
    html = render_dashboard(store, title="My Eval Report")
    assert "My Eval Report" in html


def test_dashboard_drift_significance(store):
    # baseline week: low f1
    base_ts = (datetime.now(tz=timezone.utc) - timedelta(days=10)).isoformat(timespec="seconds")
    for i in range(5):
        r = _mk_run(i, ts=base_ts)
        r.f1 = 0.2
        store.save_run(r)
    # current week: high f1
    for i in range(5, 10):
        r = _mk_run(i)
        r.f1 = 0.9
        store.save_run(r)
    html = render_dashboard(store, window_days=7)
    # A significant delta in f1 should show as 'sig' row
    assert "class='sig'" in html or 'class="sig"' in html
