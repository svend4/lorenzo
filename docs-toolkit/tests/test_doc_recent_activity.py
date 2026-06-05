"""Tests for E416 DocRecentActivity."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_recent_activity import (
    Activity,
    ActivityStats,
    DocRecentActivity,
)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_default_max_size():
    tracker = DocRecentActivity()
    assert tracker._max_size == 1000


def test_custom_max_size():
    tracker = DocRecentActivity(max_size=50)
    assert tracker._max_size == 50


def test_max_size_one_allowed():
    tracker = DocRecentActivity(max_size=1)
    assert tracker._max_size == 1


def test_max_size_zero_raises():
    with pytest.raises(ValueError):
        DocRecentActivity(max_size=0)


def test_max_size_negative_raises():
    with pytest.raises(ValueError):
        DocRecentActivity(max_size=-10)


def test_starts_empty():
    tracker = DocRecentActivity()
    assert tracker.recent() == []
    assert tracker.stats().total_activities == 0


# ---------------------------------------------------------------------------
# record()
# ---------------------------------------------------------------------------


def test_record_returns_activity():
    tracker = DocRecentActivity()
    activity = tracker.record("doc-1", "alice", "view")
    assert isinstance(activity, Activity)
    assert activity.doc_id == "doc-1"
    assert activity.actor == "alice"
    assert activity.kind == "view"
    assert activity.details == ""
    assert activity.activity_id == 1


def test_record_auto_increments_id():
    tracker = DocRecentActivity()
    a = tracker.record("d", "u", "view")
    b = tracker.record("d", "u", "view")
    c = tracker.record("d", "u", "view")
    assert (a.activity_id, b.activity_id, c.activity_id) == (1, 2, 3)


def test_record_uses_now_argument():
    tracker = DocRecentActivity()
    activity = tracker.record("d", "u", "view", now=12345.0)
    assert activity.at == 12345.0


def test_record_defaults_to_time_time(monkeypatch):
    tracker = DocRecentActivity()
    monkeypatch.setattr(time, "time", lambda: 999.0)
    activity = tracker.record("d", "u", "view")
    assert activity.at == 999.0


def test_record_with_details():
    tracker = DocRecentActivity()
    activity = tracker.record("d", "u", "edit", details="renamed title")
    assert activity.details == "renamed title"


def test_record_appends_to_global_list():
    tracker = DocRecentActivity()
    tracker.record("d1", "u1", "view")
    tracker.record("d2", "u2", "edit")
    assert len(tracker._activities) == 2


def test_record_indexes_by_doc():
    tracker = DocRecentActivity()
    tracker.record("d1", "u1", "view")
    tracker.record("d1", "u2", "edit")
    tracker.record("d2", "u3", "view")
    assert len(tracker._by_doc["d1"]) == 2
    assert len(tracker._by_doc["d2"]) == 1


def test_record_indexes_by_actor():
    tracker = DocRecentActivity()
    tracker.record("d1", "alice", "view")
    tracker.record("d2", "alice", "edit")
    tracker.record("d3", "bob", "view")
    assert len(tracker._by_actor["alice"]) == 2
    assert len(tracker._by_actor["bob"]) == 1


# ---------------------------------------------------------------------------
# max_size enforcement
# ---------------------------------------------------------------------------


def test_eviction_when_over_max_size():
    tracker = DocRecentActivity(max_size=3)
    tracker.record("d1", "u", "view")
    tracker.record("d2", "u", "view")
    tracker.record("d3", "u", "view")
    tracker.record("d4", "u", "view")
    assert len(tracker._activities) == 3
    # Oldest (d1) should be evicted
    doc_ids = [a.doc_id for a in tracker._activities]
    assert "d1" not in doc_ids
    assert "d4" in doc_ids


def test_eviction_cleans_doc_index():
    tracker = DocRecentActivity(max_size=2)
    tracker.record("d1", "u", "view")
    tracker.record("d2", "u", "view")
    tracker.record("d3", "u", "view")
    assert "d1" not in tracker._by_doc
    assert "d2" in tracker._by_doc
    assert "d3" in tracker._by_doc


def test_eviction_cleans_actor_index():
    tracker = DocRecentActivity(max_size=2)
    tracker.record("d1", "alice", "view")
    tracker.record("d2", "bob", "view")
    tracker.record("d3", "carol", "view")
    assert "alice" not in tracker._by_actor
    assert "bob" in tracker._by_actor
    assert "carol" in tracker._by_actor


def test_eviction_keeps_doc_index_when_multiple_entries():
    tracker = DocRecentActivity(max_size=2)
    tracker.record("d1", "u1", "view")
    tracker.record("d1", "u2", "edit")
    tracker.record("d2", "u3", "view")  # evicts first d1 record
    assert "d1" in tracker._by_doc
    assert len(tracker._by_doc["d1"]) == 1


# ---------------------------------------------------------------------------
# recent()
# ---------------------------------------------------------------------------


def test_recent_default_limit():
    tracker = DocRecentActivity()
    for i in range(15):
        tracker.record(f"d{i}", "u", "view")
    result = tracker.recent()
    assert len(result) == 10


def test_recent_newest_first():
    tracker = DocRecentActivity()
    a1 = tracker.record("d1", "u", "view")
    a2 = tracker.record("d2", "u", "view")
    a3 = tracker.record("d3", "u", "view")
    result = tracker.recent()
    assert [a.activity_id for a in result] == [a3.activity_id, a2.activity_id, a1.activity_id]


def test_recent_with_custom_limit():
    tracker = DocRecentActivity()
    for i in range(5):
        tracker.record(f"d{i}", "u", "view")
    result = tracker.recent(limit=2)
    assert len(result) == 2


def test_recent_limit_zero():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view")
    assert tracker.recent(limit=0) == []


def test_recent_limit_larger_than_buffer():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view")
    result = tracker.recent(limit=100)
    assert len(result) == 1


def test_recent_empty():
    tracker = DocRecentActivity()
    assert tracker.recent() == []


# ---------------------------------------------------------------------------
# recent_for_doc()
# ---------------------------------------------------------------------------


def test_recent_for_doc_filters():
    tracker = DocRecentActivity()
    tracker.record("d1", "u", "view")
    tracker.record("d2", "u", "view")
    tracker.record("d1", "u", "edit")
    result = tracker.recent_for_doc("d1")
    assert len(result) == 2
    assert all(a.doc_id == "d1" for a in result)


def test_recent_for_doc_newest_first():
    tracker = DocRecentActivity()
    a1 = tracker.record("d1", "u", "view")
    a2 = tracker.record("d1", "u", "edit")
    result = tracker.recent_for_doc("d1")
    assert result[0].activity_id == a2.activity_id
    assert result[1].activity_id == a1.activity_id


def test_recent_for_doc_unknown_doc():
    tracker = DocRecentActivity()
    tracker.record("d1", "u", "view")
    assert tracker.recent_for_doc("missing") == []


def test_recent_for_doc_with_limit():
    tracker = DocRecentActivity()
    for _ in range(5):
        tracker.record("d1", "u", "view")
    result = tracker.recent_for_doc("d1", limit=2)
    assert len(result) == 2


def test_recent_for_doc_limit_zero():
    tracker = DocRecentActivity()
    tracker.record("d1", "u", "view")
    assert tracker.recent_for_doc("d1", limit=0) == []


# ---------------------------------------------------------------------------
# recent_for_actor()
# ---------------------------------------------------------------------------


def test_recent_for_actor_filters():
    tracker = DocRecentActivity()
    tracker.record("d", "alice", "view")
    tracker.record("d", "bob", "view")
    tracker.record("d", "alice", "edit")
    result = tracker.recent_for_actor("alice")
    assert len(result) == 2
    assert all(a.actor == "alice" for a in result)


def test_recent_for_actor_newest_first():
    tracker = DocRecentActivity()
    a1 = tracker.record("d", "alice", "view")
    a2 = tracker.record("d", "alice", "edit")
    result = tracker.recent_for_actor("alice")
    assert result[0].activity_id == a2.activity_id


def test_recent_for_actor_unknown():
    tracker = DocRecentActivity()
    assert tracker.recent_for_actor("nobody") == []


def test_recent_for_actor_with_limit():
    tracker = DocRecentActivity()
    for _ in range(4):
        tracker.record("d", "alice", "view")
    assert len(tracker.recent_for_actor("alice", limit=2)) == 2


def test_recent_for_actor_limit_zero():
    tracker = DocRecentActivity()
    tracker.record("d", "alice", "view")
    assert tracker.recent_for_actor("alice", limit=0) == []


# ---------------------------------------------------------------------------
# recent_of_kind()
# ---------------------------------------------------------------------------


def test_recent_of_kind_filters():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view")
    tracker.record("d", "u", "edit")
    tracker.record("d", "u", "view")
    result = tracker.recent_of_kind("view")
    assert len(result) == 2
    assert all(a.kind == "view" for a in result)


def test_recent_of_kind_newest_first():
    tracker = DocRecentActivity()
    a1 = tracker.record("d", "u", "view")
    tracker.record("d", "u", "edit")
    a3 = tracker.record("d", "u", "view")
    result = tracker.recent_of_kind("view")
    assert result[0].activity_id == a3.activity_id
    assert result[1].activity_id == a1.activity_id


def test_recent_of_kind_unknown():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view")
    assert tracker.recent_of_kind("comment") == []


def test_recent_of_kind_with_limit():
    tracker = DocRecentActivity()
    for _ in range(5):
        tracker.record("d", "u", "view")
    assert len(tracker.recent_of_kind("view", limit=3)) == 3


def test_recent_of_kind_limit_zero():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view")
    assert tracker.recent_of_kind("view", limit=0) == []


# ---------------------------------------------------------------------------
# since()
# ---------------------------------------------------------------------------


def test_since_returns_recent_only():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view", now=10.0)
    tracker.record("d", "u", "view", now=20.0)
    tracker.record("d", "u", "view", now=30.0)
    result = tracker.since(20.0)
    assert len(result) == 2
    assert all(a.at >= 20.0 for a in result)


def test_since_ascending_order():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view", now=30.0)
    tracker.record("d", "u", "view", now=10.0)
    tracker.record("d", "u", "view", now=20.0)
    result = tracker.since(0.0)
    assert [a.at for a in result] == [10.0, 20.0, 30.0]


def test_since_inclusive():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view", now=10.0)
    result = tracker.since(10.0)
    assert len(result) == 1


def test_since_no_match():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view", now=5.0)
    assert tracker.since(100.0) == []


def test_since_empty_tracker():
    tracker = DocRecentActivity()
    assert tracker.since(0.0) == []


# ---------------------------------------------------------------------------
# active_docs / active_actors
# ---------------------------------------------------------------------------


def test_active_docs_within_window():
    tracker = DocRecentActivity()
    tracker.record("d1", "u", "view", now=100.0)
    tracker.record("d2", "u", "view", now=200.0)
    result = tracker.active_docs(within_seconds=50, now=210.0)
    # only d2 within last 50s of 210
    assert result == ["d2"]


def test_active_docs_default_window_one_day():
    tracker = DocRecentActivity()
    now = 1000000.0
    tracker.record("d1", "u", "view", now=now - 100)
    tracker.record("d2", "u", "view", now=now - 200000)  # outside 1 day
    result = tracker.active_docs(now=now)
    assert "d1" in result
    assert "d2" not in result


def test_active_docs_sorted():
    tracker = DocRecentActivity()
    tracker.record("zeta", "u", "view", now=100.0)
    tracker.record("alpha", "u", "view", now=100.0)
    tracker.record("mu", "u", "view", now=100.0)
    result = tracker.active_docs(within_seconds=1000, now=200.0)
    assert result == ["alpha", "mu", "zeta"]


def test_active_docs_empty():
    tracker = DocRecentActivity()
    assert tracker.active_docs(now=100.0) == []


def test_active_actors_within_window():
    tracker = DocRecentActivity()
    tracker.record("d", "alice", "view", now=100.0)
    tracker.record("d", "bob", "view", now=200.0)
    result = tracker.active_actors(within_seconds=50, now=210.0)
    assert result == ["bob"]


def test_active_actors_sorted():
    tracker = DocRecentActivity()
    tracker.record("d", "zoe", "view", now=100.0)
    tracker.record("d", "alice", "view", now=100.0)
    tracker.record("d", "mike", "view", now=100.0)
    result = tracker.active_actors(within_seconds=1000, now=200.0)
    assert result == ["alice", "mike", "zoe"]


def test_active_actors_dedup():
    tracker = DocRecentActivity()
    tracker.record("d1", "alice", "view", now=100.0)
    tracker.record("d2", "alice", "edit", now=110.0)
    result = tracker.active_actors(within_seconds=1000, now=200.0)
    assert result == ["alice"]


# ---------------------------------------------------------------------------
# counts
# ---------------------------------------------------------------------------


def test_count_for_doc():
    tracker = DocRecentActivity()
    tracker.record("d1", "u", "view")
    tracker.record("d1", "u", "edit")
    tracker.record("d2", "u", "view")
    assert tracker.count_for_doc("d1") == 2
    assert tracker.count_for_doc("d2") == 1
    assert tracker.count_for_doc("missing") == 0


def test_count_for_actor():
    tracker = DocRecentActivity()
    tracker.record("d", "alice", "view")
    tracker.record("d", "alice", "edit")
    tracker.record("d", "bob", "view")
    assert tracker.count_for_actor("alice") == 2
    assert tracker.count_for_actor("bob") == 1
    assert tracker.count_for_actor("missing") == 0


def test_count_of_kind():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view")
    tracker.record("d", "u", "view")
    tracker.record("d", "u", "edit")
    assert tracker.count_of_kind("view") == 2
    assert tracker.count_of_kind("edit") == 1
    assert tracker.count_of_kind("comment") == 0


# ---------------------------------------------------------------------------
# clearing
# ---------------------------------------------------------------------------


def test_clear_doc_returns_count():
    tracker = DocRecentActivity()
    tracker.record("d1", "u", "view")
    tracker.record("d1", "u", "edit")
    tracker.record("d2", "u", "view")
    removed = tracker.clear_doc("d1")
    assert removed == 2


def test_clear_doc_removes_activities():
    tracker = DocRecentActivity()
    tracker.record("d1", "u", "view")
    tracker.record("d2", "u", "view")
    tracker.clear_doc("d1")
    assert tracker.count_for_doc("d1") == 0
    assert tracker.count_for_doc("d2") == 1


def test_clear_doc_cleans_actor_index():
    tracker = DocRecentActivity()
    tracker.record("d1", "alice", "view")
    tracker.record("d1", "alice", "edit")
    tracker.clear_doc("d1")
    assert tracker.count_for_actor("alice") == 0


def test_clear_doc_unknown_returns_zero():
    tracker = DocRecentActivity()
    assert tracker.clear_doc("missing") == 0


def test_clear_actor_returns_count():
    tracker = DocRecentActivity()
    tracker.record("d", "alice", "view")
    tracker.record("d", "alice", "edit")
    tracker.record("d", "bob", "view")
    removed = tracker.clear_actor("alice")
    assert removed == 2


def test_clear_actor_removes_activities():
    tracker = DocRecentActivity()
    tracker.record("d", "alice", "view")
    tracker.record("d", "bob", "view")
    tracker.clear_actor("alice")
    assert tracker.count_for_actor("alice") == 0
    assert tracker.count_for_actor("bob") == 1


def test_clear_actor_cleans_doc_index():
    tracker = DocRecentActivity()
    tracker.record("d1", "alice", "view")
    tracker.clear_actor("alice")
    assert tracker.count_for_doc("d1") == 0


def test_clear_actor_unknown_returns_zero():
    tracker = DocRecentActivity()
    assert tracker.clear_actor("nobody") == 0


def test_clear_all_returns_count():
    tracker = DocRecentActivity()
    for i in range(5):
        tracker.record(f"d{i}", "u", "view")
    assert tracker.clear_all() == 5


def test_clear_all_empties():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view")
    tracker.clear_all()
    assert tracker.recent() == []
    assert tracker._by_doc == {}
    assert tracker._by_actor == {}


def test_clear_all_empty_tracker():
    tracker = DocRecentActivity()
    assert tracker.clear_all() == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_empty():
    tracker = DocRecentActivity()
    stats = tracker.stats()
    assert isinstance(stats, ActivityStats)
    assert stats.total_activities == 0
    assert stats.unique_docs == 0
    assert stats.unique_actors == 0
    assert stats.kind_counts == {}


def test_stats_totals():
    tracker = DocRecentActivity()
    tracker.record("d1", "alice", "view")
    tracker.record("d1", "bob", "edit")
    tracker.record("d2", "alice", "view")
    stats = tracker.stats()
    assert stats.total_activities == 3
    assert stats.unique_docs == 2
    assert stats.unique_actors == 2


def test_stats_kind_counts():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "view")
    tracker.record("d", "u", "view")
    tracker.record("d", "u", "edit")
    tracker.record("d", "u", "comment")
    stats = tracker.stats()
    assert stats.kind_counts == {"view": 2, "edit": 1, "comment": 1}


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_thread_safety_concurrent_record():
    tracker = DocRecentActivity(max_size=100000)
    threads = []
    per_thread = 100

    def worker(tid: int):
        for i in range(per_thread):
            tracker.record(f"doc-{tid}", f"actor-{tid}", "view", details=str(i))

    for tid in range(10):
        t = threading.Thread(target=worker, args=(tid,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    assert tracker.stats().total_activities == 10 * per_thread
    # Each doc has per_thread entries
    for tid in range(10):
        assert tracker.count_for_doc(f"doc-{tid}") == per_thread


def test_thread_safety_record_and_query():
    tracker = DocRecentActivity(max_size=10000)
    stop = threading.Event()

    def writer():
        i = 0
        while not stop.is_set():
            tracker.record("d", "u", "view", details=str(i))
            i += 1

    def reader():
        for _ in range(50):
            tracker.recent()
            tracker.recent_for_doc("d")
            tracker.stats()

    w = threading.Thread(target=writer)
    w.start()
    readers = [threading.Thread(target=reader) for _ in range(5)]
    for r in readers:
        r.start()
    for r in readers:
        r.join()
    stop.set()
    w.join()

    # If we got here without deadlock or exception, test passes
    assert tracker.stats().total_activities > 0


def test_thread_safety_unique_ids():
    tracker = DocRecentActivity(max_size=100000)
    ids: list[int] = []
    lock = threading.Lock()

    def worker():
        for _ in range(50):
            a = tracker.record("d", "u", "view")
            with lock:
                ids.append(a.activity_id)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(ids) == 500
    assert len(set(ids)) == 500  # all unique


# ---------------------------------------------------------------------------
# Integration scenarios
# ---------------------------------------------------------------------------


def test_full_lifecycle():
    tracker = DocRecentActivity(max_size=10)
    tracker.record("doc1", "alice", "view", now=1.0)
    tracker.record("doc1", "alice", "edit", details="title", now=2.0)
    tracker.record("doc2", "bob", "view", now=3.0)
    tracker.record("doc1", "carol", "comment", details="nice doc", now=4.0)

    # Recent overall
    recent = tracker.recent()
    assert recent[0].kind == "comment"
    assert recent[-1].kind == "view"

    # Per-doc
    doc1_acts = tracker.recent_for_doc("doc1")
    assert [a.kind for a in doc1_acts] == ["comment", "edit", "view"]

    # Per-actor
    alice_acts = tracker.recent_for_actor("alice")
    assert [a.kind for a in alice_acts] == ["edit", "view"]

    # Active subsets
    assert tracker.active_docs(within_seconds=2, now=5.0) == ["doc1", "doc2"]

    # Stats
    stats = tracker.stats()
    assert stats.total_activities == 4
    assert stats.unique_docs == 2
    assert stats.unique_actors == 3


def test_details_preserved_after_record():
    tracker = DocRecentActivity()
    tracker.record("d", "u", "edit", details="abc")
    activity = tracker.recent()[0]
    assert activity.details == "abc"


def test_activity_dataclass_defaults():
    a = Activity(activity_id=1, doc_id="d", actor="u", kind="view")
    assert a.at == 0.0
    assert a.details == ""


def test_activity_stats_dataclass_defaults():
    s = ActivityStats(total_activities=0, unique_docs=0, unique_actors=0)
    assert s.kind_counts == {}
