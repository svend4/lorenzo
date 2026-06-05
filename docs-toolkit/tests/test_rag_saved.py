"""Tests for saved searches / alerts (Sprint 91 / S1)."""
from __future__ import annotations

import pytest

from docstoolkit.alerts import AlertStore
from docstoolkit.rag.saved import list_queries, run_due_alerts, save_query
from docstoolkit.rag.types import Passage


@pytest.fixture
def store(tmp_path):
    s = AlertStore(db_path=tmp_path / "alerts.sqlite")
    yield s
    s.close()


def test_save_query_returns_id(store):
    qid = save_query("Yodoca", owner="alice", store=store)
    assert qid
    assert len(qid) == 16


def test_list_queries_returns_saved(store):
    save_query("a", owner="alice", store=store)
    save_query("b", owner="alice", store=store)
    qs = list_queries(owner="alice", store=store)
    assert len(qs) == 2


def test_list_queries_filters_by_owner(store):
    save_query("a", owner="alice", store=store)
    save_query("b", owner="bob", store=store)
    qs = list_queries(owner="alice", store=store)
    assert len(qs) == 1
    assert qs[0].owner == "alice"


def test_list_queries_empty(store):
    assert list_queries(owner="ghost", store=store) == []


def test_run_due_alerts_with_custom_retriever(store):
    save_query("test", owner="alice", store=store)

    def fake_retriever(query, top_k):
        return [Passage(text="x", doc_id="d", title="D", score=0.5)]

    # First tick — establishes baseline, may or may not fire
    fired = run_due_alerts(retriever=fake_retriever, store=store)
    assert isinstance(fired, list)


def test_save_query_custom_schedule(store):
    qid = save_query("q", schedule="hourly", store=store)
    qs = list_queries(store=store)
    saved = next(q for q in qs if q.id == qid)
    assert saved.schedule == "hourly"


def test_save_query_default_owner(store):
    qid = save_query("q", store=store)
    qs = list_queries(store=store)
    assert any(q.id == qid for q in qs)
