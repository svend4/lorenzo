"""Tests for docstoolkit.doc_audit_search (E343)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_audit_search import (
    AuditEntry,
    AuditSearchQuery,
    AuditStats,
    DocAuditSearch,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def populate(idx: DocAuditSearch) -> None:
    """Insert a small fixed corpus."""
    idx.record("doc1", "alice", "read", now=100.0)
    idx.record("doc1", "bob", "write", now=110.0)
    idx.record("doc2", "alice", "read", now=120.0)
    idx.record("doc2", "alice", "delete", now=130.0)
    idx.record("doc3", "carol", "read", now=140.0)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestAuditEntryDataclass:
    def test_fields(self):
        e = AuditEntry(entry_id=1, doc_id="d", actor="a", action="read")
        assert e.entry_id == 1
        assert e.doc_id == "d"
        assert e.actor == "a"
        assert e.action == "read"

    def test_defaults(self):
        e = AuditEntry(entry_id=1, doc_id="d", actor="a", action="read")
        assert e.timestamp == 0.0
        assert e.details == {}

    def test_details_independent(self):
        e1 = AuditEntry(entry_id=1, doc_id="d", actor="a", action="r")
        e2 = AuditEntry(entry_id=2, doc_id="d", actor="a", action="r")
        e1.details["k"] = "v"
        assert e2.details == {}

    def test_timestamp_set(self):
        e = AuditEntry(entry_id=1, doc_id="d", actor="a", action="r", timestamp=42.0)
        assert e.timestamp == 42.0

    def test_details_set(self):
        e = AuditEntry(
            entry_id=1,
            doc_id="d",
            actor="a",
            action="r",
            details={"reason": "test"},
        )
        assert e.details == {"reason": "test"}


class TestAuditSearchQueryDataclass:
    def test_all_defaults_none(self):
        q = AuditSearchQuery()
        assert q.doc_id is None
        assert q.actor is None
        assert q.action is None
        assert q.start_time is None
        assert q.end_time is None
        assert q.limit is None

    def test_fields_set(self):
        q = AuditSearchQuery(
            doc_id="d",
            actor="a",
            action="r",
            start_time=1.0,
            end_time=10.0,
            limit=5,
        )
        assert q.doc_id == "d"
        assert q.actor == "a"
        assert q.action == "r"
        assert q.start_time == 1.0
        assert q.end_time == 10.0
        assert q.limit == 5


class TestAuditStatsDataclass:
    def test_fields(self):
        s = AuditStats(
            total_entries=10, unique_docs=3, unique_actors=2, unique_actions=4
        )
        assert s.total_entries == 10
        assert s.unique_docs == 3
        assert s.unique_actors == 2
        assert s.unique_actions == 4


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty(self):
        idx = DocAuditSearch()
        assert idx.stats().total_entries == 0

    def test_initial_next_id(self):
        idx = DocAuditSearch()
        e = idx.record("d", "a", "r")
        assert e.entry_id == 1


# ---------------------------------------------------------------------------
# Record
# ---------------------------------------------------------------------------


class TestRecord:
    def test_returns_entry(self):
        idx = DocAuditSearch()
        e = idx.record("d", "a", "r")
        assert isinstance(e, AuditEntry)
        assert e.doc_id == "d"
        assert e.actor == "a"
        assert e.action == "r"

    def test_id_increments(self):
        idx = DocAuditSearch()
        e1 = idx.record("d", "a", "r")
        e2 = idx.record("d", "a", "r")
        e3 = idx.record("d", "a", "r")
        assert (e1.entry_id, e2.entry_id, e3.entry_id) == (1, 2, 3)

    def test_uses_now_argument(self):
        idx = DocAuditSearch()
        e = idx.record("d", "a", "r", now=999.0)
        assert e.timestamp == 999.0

    def test_default_timestamp_is_real(self):
        idx = DocAuditSearch()
        e = idx.record("d", "a", "r")
        assert e.timestamp > 0.0

    def test_details_stored(self):
        idx = DocAuditSearch()
        e = idx.record("d", "a", "r", details={"x": 1})
        assert e.details == {"x": 1}

    def test_details_default_empty(self):
        idx = DocAuditSearch()
        e = idx.record("d", "a", "r")
        assert e.details == {}

    def test_details_copied(self):
        idx = DocAuditSearch()
        d = {"x": 1}
        e = idx.record("d", "a", "r", details=d)
        d["y"] = 2
        assert e.details == {"x": 1}


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


class TestSearch:
    def test_filter_by_doc_id(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(doc_id="doc1"))
        assert len(results) == 2
        assert all(r.doc_id == "doc1" for r in results)

    def test_filter_by_actor(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(actor="alice"))
        assert len(results) == 3
        assert all(r.actor == "alice" for r in results)

    def test_filter_by_action(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(action="read"))
        assert len(results) == 3
        assert all(r.action == "read" for r in results)

    def test_multi_filter_and(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(actor="alice", action="read"))
        assert len(results) == 2

    def test_no_filters_returns_all(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery())
        assert len(results) == 5

    def test_no_match(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(doc_id="nope"))
        assert results == []

    def test_time_range_start(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(start_time=120.0))
        assert len(results) == 3

    def test_time_range_end(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(end_time=120.0))
        assert len(results) == 3

    def test_time_range_both(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(
            AuditSearchQuery(start_time=110.0, end_time=130.0)
        )
        assert len(results) == 3

    def test_limit(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(limit=2))
        assert len(results) == 2

    def test_limit_zero(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(limit=0))
        assert results == []


class TestSearchSorting:
    def test_sorted_desc(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery())
        timestamps = [r.timestamp for r in results]
        assert timestamps == sorted(timestamps, reverse=True)

    def test_sorted_desc_with_filter(self):
        idx = DocAuditSearch()
        populate(idx)
        results = idx.search(AuditSearchQuery(actor="alice"))
        timestamps = [r.timestamp for r in results]
        assert timestamps == sorted(timestamps, reverse=True)


# ---------------------------------------------------------------------------
# get_entry
# ---------------------------------------------------------------------------


class TestGetEntry:
    def test_found(self):
        idx = DocAuditSearch()
        e = idx.record("d", "a", "r")
        assert idx.get_entry(e.entry_id) == e

    def test_not_found(self):
        idx = DocAuditSearch()
        idx.record("d", "a", "r")
        assert idx.get_entry(999) is None

    def test_empty(self):
        idx = DocAuditSearch()
        assert idx.get_entry(1) is None


# ---------------------------------------------------------------------------
# entries_for_doc
# ---------------------------------------------------------------------------


class TestEntriesForDoc:
    def test_returns_matching(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_for_doc("doc1")
        assert len(entries) == 2

    def test_sorted_desc(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_for_doc("doc2")
        ts = [e.timestamp for e in entries]
        assert ts == sorted(ts, reverse=True)

    def test_limit(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_for_doc("doc1", limit=1)
        assert len(entries) == 1

    def test_unknown(self):
        idx = DocAuditSearch()
        populate(idx)
        assert idx.entries_for_doc("nope") == []


# ---------------------------------------------------------------------------
# entries_for_actor
# ---------------------------------------------------------------------------


class TestEntriesForActor:
    def test_returns_matching(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_for_actor("alice")
        assert len(entries) == 3

    def test_sorted_desc(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_for_actor("alice")
        ts = [e.timestamp for e in entries]
        assert ts == sorted(ts, reverse=True)

    def test_limit(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_for_actor("alice", limit=2)
        assert len(entries) == 2

    def test_unknown(self):
        idx = DocAuditSearch()
        populate(idx)
        assert idx.entries_for_actor("nope") == []


# ---------------------------------------------------------------------------
# entries_by_action
# ---------------------------------------------------------------------------


class TestEntriesByAction:
    def test_returns_matching(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_by_action("read")
        assert len(entries) == 3

    def test_sorted_desc(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_by_action("read")
        ts = [e.timestamp for e in entries]
        assert ts == sorted(ts, reverse=True)

    def test_limit(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_by_action("read", limit=1)
        assert len(entries) == 1

    def test_unknown(self):
        idx = DocAuditSearch()
        populate(idx)
        assert idx.entries_by_action("nope") == []


# ---------------------------------------------------------------------------
# entries_in_range
# ---------------------------------------------------------------------------


class TestEntriesInRange:
    def test_inclusive_bounds(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_in_range(100.0, 140.0)
        assert len(entries) == 5

    def test_partial_range(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_in_range(110.0, 130.0)
        assert len(entries) == 3

    def test_asc_order(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_in_range(0.0, 1e9)
        ts = [e.timestamp for e in entries]
        assert ts == sorted(ts)

    def test_doc_filter(self):
        idx = DocAuditSearch()
        populate(idx)
        entries = idx.entries_in_range(0.0, 1e9, doc_id="doc1")
        assert len(entries) == 2
        assert all(e.doc_id == "doc1" for e in entries)

    def test_doc_filter_unknown(self):
        idx = DocAuditSearch()
        populate(idx)
        assert idx.entries_in_range(0.0, 1e9, doc_id="nope") == []

    def test_empty_range(self):
        idx = DocAuditSearch()
        populate(idx)
        assert idx.entries_in_range(1000.0, 2000.0) == []


# ---------------------------------------------------------------------------
# top_actors / top_actions
# ---------------------------------------------------------------------------


class TestTopActors:
    def test_sorted_count_desc(self):
        idx = DocAuditSearch()
        populate(idx)
        top = idx.top_actors()
        assert top[0] == ("alice", 3)
        counts = [c for _, c in top]
        assert counts == sorted(counts, reverse=True)

    def test_tiebreak_actor_asc(self):
        idx = DocAuditSearch()
        idx.record("d", "zoe", "r", now=1.0)
        idx.record("d", "alice", "r", now=2.0)
        idx.record("d", "bob", "r", now=3.0)
        top = idx.top_actors()
        # all count=1, alpha order
        assert [a for a, _ in top] == ["alice", "bob", "zoe"]

    def test_limit(self):
        idx = DocAuditSearch()
        populate(idx)
        top = idx.top_actors(limit=2)
        assert len(top) == 2

    def test_empty(self):
        idx = DocAuditSearch()
        assert idx.top_actors() == []


class TestTopActions:
    def test_sorted_count_desc(self):
        idx = DocAuditSearch()
        populate(idx)
        top = idx.top_actions()
        assert top[0] == ("read", 3)

    def test_tiebreak_action_asc(self):
        idx = DocAuditSearch()
        idx.record("d", "a", "zoom", now=1.0)
        idx.record("d", "a", "alpha", now=2.0)
        idx.record("d", "a", "beta", now=3.0)
        top = idx.top_actions()
        assert [a for a, _ in top] == ["alpha", "beta", "zoom"]

    def test_limit(self):
        idx = DocAuditSearch()
        populate(idx)
        top = idx.top_actions(limit=1)
        assert len(top) == 1

    def test_empty(self):
        idx = DocAuditSearch()
        assert idx.top_actions() == []


# ---------------------------------------------------------------------------
# delete_entries_for_doc
# ---------------------------------------------------------------------------


class TestDeleteEntriesForDoc:
    def test_returns_count(self):
        idx = DocAuditSearch()
        populate(idx)
        n = idx.delete_entries_for_doc("doc1")
        assert n == 2

    def test_unknown_returns_zero(self):
        idx = DocAuditSearch()
        populate(idx)
        assert idx.delete_entries_for_doc("nope") == 0

    def test_gone_from_doc_index(self):
        idx = DocAuditSearch()
        populate(idx)
        idx.delete_entries_for_doc("doc1")
        assert idx.entries_for_doc("doc1") == []

    def test_gone_from_actor_index(self):
        idx = DocAuditSearch()
        idx.record("doc1", "bob", "write", now=1.0)
        idx.delete_entries_for_doc("doc1")
        assert idx.entries_for_actor("bob") == []

    def test_gone_from_action_index(self):
        idx = DocAuditSearch()
        idx.record("doc1", "bob", "write", now=1.0)
        idx.delete_entries_for_doc("doc1")
        assert idx.entries_by_action("write") == []

    def test_other_docs_remain(self):
        idx = DocAuditSearch()
        populate(idx)
        idx.delete_entries_for_doc("doc1")
        assert len(idx.entries_for_doc("doc2")) == 2


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_returns_count(self):
        idx = DocAuditSearch()
        populate(idx)
        assert idx.clear() == 5

    def test_empty_returns_zero(self):
        idx = DocAuditSearch()
        assert idx.clear() == 0

    def test_all_gone(self):
        idx = DocAuditSearch()
        populate(idx)
        idx.clear()
        s = idx.stats()
        assert s.total_entries == 0
        assert s.unique_docs == 0
        assert s.unique_actors == 0
        assert s.unique_actions == 0

    def test_resets_next_id(self):
        idx = DocAuditSearch()
        populate(idx)
        idx.clear()
        e = idx.record("d", "a", "r")
        assert e.entry_id == 1


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        s = DocAuditSearch().stats()
        assert s == AuditStats(0, 0, 0, 0)

    def test_populated(self):
        idx = DocAuditSearch()
        populate(idx)
        s = idx.stats()
        assert s.total_entries == 5
        assert s.unique_docs == 3
        assert s.unique_actors == 3
        assert s.unique_actions == 3

    def test_returns_dataclass(self):
        s = DocAuditSearch().stats()
        assert isinstance(s, AuditStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_record(self):
        idx = DocAuditSearch()
        n_threads = 8
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                idx.record(f"doc{tid}", f"actor{tid}", "write", now=float(i))

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = idx.stats()
        assert s.total_entries == n_threads * per_thread
        # Unique ids
        ids = {e.entry_id for e in idx.search(AuditSearchQuery())}
        assert len(ids) == n_threads * per_thread

    def test_concurrent_record_and_search(self):
        idx = DocAuditSearch()
        stop = threading.Event()

        def writer():
            i = 0
            while not stop.is_set():
                idx.record("doc", "a", "r", now=float(i))
                i += 1

        def reader():
            for _ in range(100):
                idx.search(AuditSearchQuery(doc_id="doc"))

        w = threading.Thread(target=writer)
        r = threading.Thread(target=reader)
        w.start()
        r.start()
        r.join()
        stop.set()
        w.join()
        assert idx.stats().total_entries > 0
