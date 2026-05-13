"""Tests for docstoolkit.alerts — SavedQuery, FiredAlert, AlertStore, AlertRunner."""
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.alerts import AlertStore, AlertRunner, SavedQuery, FiredAlert
from docstoolkit.rag.types import Passage


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_store(tmp_path: Path) -> AlertStore:
    return AlertStore(db_path=tmp_path / "alerts.sqlite")


def ts_hours_ago(hours: float) -> str:
    dt = datetime.now(timezone.utc) - timedelta(hours=hours)
    return dt.isoformat(timespec="seconds")


def ts_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# SavedQuery dataclass
# ---------------------------------------------------------------------------

def test_saved_query_auto_id():
    q = SavedQuery(query="RAG retrieval")
    assert q.id
    assert len(q.id) == 16


def test_saved_query_auto_created_ts():
    q = SavedQuery(query="RAG retrieval")
    assert q.created_ts
    # Should parse as ISO date
    datetime.fromisoformat(q.created_ts)


def test_saved_query_defaults():
    q = SavedQuery(query="test")
    assert q.retriever_method == "hybrid"
    assert q.top_k == 10
    assert q.schedule == "daily"
    assert q.cooldown_hours == 24
    assert q.enabled is True
    assert q.owner == ""


def test_saved_query_custom_fields():
    q = SavedQuery(
        query="agents", owner="alice", retriever_method="keyword",
        top_k=5, cooldown_hours=1,
    )
    assert q.query == "agents"
    assert q.owner == "alice"
    assert q.top_k == 5
    assert q.cooldown_hours == 1


# ---------------------------------------------------------------------------
# FiredAlert dataclass
# ---------------------------------------------------------------------------

def test_fired_alert_auto_id_and_ts():
    a = FiredAlert(query_id="qid", query="q", owner="bob",
                   added_docs=["doc1"], removed_docs=[])
    assert a.id
    assert a.ts
    datetime.fromisoformat(a.ts)


# ---------------------------------------------------------------------------
# AlertStore — save / get / list_all
# ---------------------------------------------------------------------------

def test_save_and_get(tmp_path):
    store = make_store(tmp_path)
    q = SavedQuery(query="knowledge graph")
    qid = store.save(q)
    assert qid == q.id

    fetched = store.get(qid)
    assert fetched is not None
    assert fetched.query == "knowledge graph"
    assert fetched.id == qid
    store.close()


def test_get_nonexistent_returns_none(tmp_path):
    store = make_store(tmp_path)
    assert store.get("no-such-id") is None
    store.close()


def test_list_all_empty(tmp_path):
    store = make_store(tmp_path)
    assert store.list_all() == []
    store.close()


def test_list_all_returns_all(tmp_path):
    store = make_store(tmp_path)
    store.save(SavedQuery(query="alpha", owner="alice"))
    store.save(SavedQuery(query="beta", owner="alice"))
    store.save(SavedQuery(query="gamma", owner="bob"))
    all_q = store.list_all()
    assert len(all_q) == 3
    store.close()


def test_list_all_filter_by_owner(tmp_path):
    store = make_store(tmp_path)
    store.save(SavedQuery(query="alpha", owner="alice"))
    store.save(SavedQuery(query="beta", owner="bob"))
    alice_q = store.list_all(owner="alice")
    assert len(alice_q) == 1
    assert alice_q[0].query == "alpha"
    store.close()


def test_save_overwrite(tmp_path):
    store = make_store(tmp_path)
    q = SavedQuery(query="original")
    store.save(q)
    q.query = "updated"
    store.save(q)
    fetched = store.get(q.id)
    assert fetched.query == "updated"
    store.close()


# ---------------------------------------------------------------------------
# AlertStore — list_due
# ---------------------------------------------------------------------------

def test_list_due_new_query_no_last_run(tmp_path):
    store = make_store(tmp_path)
    q = SavedQuery(query="new query", last_run_ts="")
    store.save(q)
    due = store.list_due()
    assert any(d.id == q.id for d in due)
    store.close()


def test_list_due_cooldown_not_elapsed(tmp_path):
    store = make_store(tmp_path)
    # last_run just 1 hour ago but cooldown is 24h
    q = SavedQuery(query="recent", cooldown_hours=24,
                   last_run_ts=ts_hours_ago(1))
    store.save(q)
    due = store.list_due()
    assert all(d.id != q.id for d in due)
    store.close()


def test_list_due_cooldown_elapsed(tmp_path):
    store = make_store(tmp_path)
    # last_run 25h ago, cooldown 24h
    q = SavedQuery(query="stale", cooldown_hours=24,
                   last_run_ts=ts_hours_ago(25))
    store.save(q)
    due = store.list_due()
    assert any(d.id == q.id for d in due)
    store.close()


def test_list_due_disabled_not_returned(tmp_path):
    store = make_store(tmp_path)
    q = SavedQuery(query="disabled", enabled=False, last_run_ts="")
    store.save(q)
    due = store.list_due()
    assert all(d.id != q.id for d in due)
    store.close()


def test_list_due_exact_cooldown_boundary(tmp_path):
    store = make_store(tmp_path)
    # last_run exactly cooldown_hours ago → should be due
    q = SavedQuery(query="boundary", cooldown_hours=6,
                   last_run_ts=ts_hours_ago(6.01))
    store.save(q)
    due = store.list_due()
    assert any(d.id == q.id for d in due)
    store.close()


# ---------------------------------------------------------------------------
# AlertStore — update_after_run + record_alert + list_alerts
# ---------------------------------------------------------------------------

def test_update_after_run(tmp_path):
    store = make_store(tmp_path)
    q = SavedQuery(query="test")
    store.save(q)
    store.update_after_run(q.id, "abc123hash")
    fetched = store.get(q.id)
    assert fetched.last_results_hash == "abc123hash"
    assert fetched.last_run_ts  # Not empty
    store.close()


def test_record_and_list_alerts(tmp_path):
    store = make_store(tmp_path)
    q = SavedQuery(query="agent memory")
    store.save(q)

    alert = FiredAlert(
        query_id=q.id, query=q.query, owner="alice",
        added_docs=["docs/a.md", "docs/b.md"],
        removed_docs=["docs/c.md"],
    )
    store.record_alert(alert)

    alerts = store.list_alerts()
    assert len(alerts) == 1
    a = alerts[0]
    assert a.query_id == q.id
    assert a.added_docs == ["docs/a.md", "docs/b.md"]
    assert a.removed_docs == ["docs/c.md"]
    store.close()


def test_list_alerts_filter_by_query_id(tmp_path):
    store = make_store(tmp_path)
    q1 = SavedQuery(query="q1")
    q2 = SavedQuery(query="q2")
    store.save(q1)
    store.save(q2)

    store.record_alert(FiredAlert(query_id=q1.id, query="q1", owner="",
                                   added_docs=["a"], removed_docs=[]))
    store.record_alert(FiredAlert(query_id=q2.id, query="q2", owner="",
                                   added_docs=["b"], removed_docs=[]))

    assert len(store.list_alerts(query_id=q1.id)) == 1
    assert store.list_alerts(query_id=q1.id)[0].query_id == q1.id
    store.close()


def test_list_alerts_limit(tmp_path):
    store = make_store(tmp_path)
    q = SavedQuery(query="flood")
    store.save(q)
    for _ in range(10):
        store.record_alert(FiredAlert(query_id=q.id, query="flood", owner="",
                                       added_docs=[], removed_docs=[]))
    assert len(store.list_alerts(limit=5)) == 5
    store.close()


# ---------------------------------------------------------------------------
# AlertRunner — tick()
# ---------------------------------------------------------------------------

def _make_passages(*doc_ids: str) -> list[Passage]:
    return [Passage(text="", doc_id=d, title=d, score=1.0) for d in doc_ids]


def test_tick_fires_alert_when_results_change(tmp_path):
    store = make_store(tmp_path)

    call_count = [0]
    results_by_call = [
        _make_passages("doc-A", "doc-B"),
        _make_passages("doc-A", "doc-C"),  # doc-B gone, doc-C added
    ]

    def retriever(query, top_k):
        idx = call_count[0] % len(results_by_call)
        call_count[0] += 1
        return results_by_call[idx]

    runner = AlertRunner(store=store, retriever_fn=retriever)

    q = SavedQuery(query="test", cooldown_hours=0, last_run_ts="")
    store.save(q)

    # First tick: no old hash → no alert fired (first run just records)
    fired = runner.tick()
    assert len(fired) == 0
    assert call_count[0] == 1

    # Second tick: hash changed → alert fired
    # Reset cooldown so it's due again
    store.update_after_run(q.id, store.get(q.id).last_results_hash)
    # Manually set last_run to past so it's due
    store.conn.execute("UPDATE saved_queries SET last_run_ts = ? WHERE id = ?",
                       (ts_hours_ago(1), q.id))
    store.conn.commit()

    fired = runner.tick()
    assert len(fired) == 1
    assert fired[0].query_id == q.id
    store.close()


def test_tick_no_alert_when_results_same(tmp_path):
    store = make_store(tmp_path)
    same_passages = _make_passages("doc-A", "doc-B")

    runner = AlertRunner(store=store, retriever_fn=lambda q, k: same_passages)

    q = SavedQuery(query="stable", cooldown_hours=0, last_run_ts="")
    store.save(q)

    # First tick: records initial hash
    runner.tick()

    # Set as due again
    store.conn.execute("UPDATE saved_queries SET last_run_ts = ? WHERE id = ?",
                       (ts_hours_ago(1), q.id))
    store.conn.commit()

    # Second tick: same results → no alert
    fired = runner.tick()
    assert len(fired) == 0
    store.close()


def test_tick_no_due_queries_returns_empty(tmp_path):
    store = make_store(tmp_path)
    runner = AlertRunner(store=store, retriever_fn=lambda q, k: [])
    assert runner.tick() == []
    store.close()


def test_tick_handles_retriever_exception(tmp_path):
    store = make_store(tmp_path)

    def failing_retriever(query, top_k):
        raise RuntimeError("network error")

    runner = AlertRunner(store=store, retriever_fn=failing_retriever)
    q = SavedQuery(query="boom", cooldown_hours=0, last_run_ts="")
    store.save(q)

    # Should not raise; exception is swallowed
    fired = runner.tick()
    assert isinstance(fired, list)
    store.close()


def test_hash_results_deterministic(tmp_path):
    store = make_store(tmp_path)
    runner = AlertRunner(store=store, retriever_fn=lambda q, k: [])

    p1 = _make_passages("a", "b", "c")
    p2 = _make_passages("c", "a", "b")  # same docs, different order
    assert runner._hash_results(p1) == runner._hash_results(p2)
    store.close()


def test_hash_results_different_for_different_docs(tmp_path):
    store = make_store(tmp_path)
    runner = AlertRunner(store=store, retriever_fn=lambda q, k: [])

    p1 = _make_passages("a", "b")
    p2 = _make_passages("a", "c")
    assert runner._hash_results(p1) != runner._hash_results(p2)
    store.close()


def test_hash_empty_passages(tmp_path):
    store = make_store(tmp_path)
    runner = AlertRunner(store=store, retriever_fn=lambda q, k: [])
    h = runner._hash_results([])
    assert isinstance(h, str)
    assert len(h) == 32  # MD5 hex
    store.close()
