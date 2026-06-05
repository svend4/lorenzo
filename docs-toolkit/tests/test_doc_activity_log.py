"""Tests for docstoolkit.doc_activity_log (E304).

Coverage:
- ActivityEntry dataclass
- ActivityStats dataclass
- DocActivityLog construction (empty state)
- DocActivityLog.log (entry_id increments, timestamp, metadata, return value)
- entries_for_doc (empty doc, multiple entries, limit)
- entries_by_actor (empty actor, multiple, limit)
- entries_by_action (empty action, multiple, limit)
- recent (empty, fewer than limit, exactly limit, more than limit)
- get_entry (found, not found)
- doc_ids (sorted, empty)
- actors (sorted, deduplicated)
- actions (sorted, deduplicated)
- stats (totals, action_counts)
- thread safety
"""

from __future__ import annotations

import threading
from dataclasses import fields

import pytest

from docstoolkit.doc_activity_log import ActivityEntry, ActivityStats, DocActivityLog


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_log() -> DocActivityLog:
    return DocActivityLog()


# ---------------------------------------------------------------------------
# TestActivityEntryDataclass
# ---------------------------------------------------------------------------

class TestActivityEntryDataclass:
    def test_entry_id_stored(self):
        e = ActivityEntry(entry_id=1, doc_id="d1", action="created", actor="alice")
        assert e.entry_id == 1

    def test_doc_id_stored(self):
        e = ActivityEntry(entry_id=2, doc_id="doc42", action="viewed", actor="bob")
        assert e.doc_id == "doc42"

    def test_action_stored(self):
        e = ActivityEntry(entry_id=3, doc_id="d", action="edited", actor="u")
        assert e.action == "edited"

    def test_actor_stored(self):
        e = ActivityEntry(entry_id=4, doc_id="d", action="shared", actor="charlie")
        assert e.actor == "charlie"

    def test_timestamp_default(self):
        e = ActivityEntry(entry_id=5, doc_id="d", action="deleted", actor="u")
        assert e.timestamp == 0.0

    def test_timestamp_custom(self):
        e = ActivityEntry(entry_id=6, doc_id="d", action="viewed", actor="u", timestamp=1000.5)
        assert e.timestamp == 1000.5

    def test_metadata_default_empty(self):
        e = ActivityEntry(entry_id=7, doc_id="d", action="created", actor="u")
        assert e.metadata == {}

    def test_metadata_stored(self):
        e = ActivityEntry(entry_id=8, doc_id="d", action="edited", actor="u", metadata={"key": "val"})
        assert e.metadata["key"] == "val"

    def test_metadata_independent_per_instance(self):
        e1 = ActivityEntry(entry_id=9, doc_id="d", action="viewed", actor="u")
        e2 = ActivityEntry(entry_id=10, doc_id="d", action="viewed", actor="u")
        e1.metadata["x"] = 1
        assert "x" not in e2.metadata

    def test_is_dataclass(self):
        fnames = {f.name for f in fields(ActivityEntry)}
        assert fnames == {"entry_id", "doc_id", "action", "actor", "timestamp", "metadata"}

    def test_field_count(self):
        assert len(fields(ActivityEntry)) == 6


# ---------------------------------------------------------------------------
# TestActivityStatsDataclass
# ---------------------------------------------------------------------------

class TestActivityStatsDataclass:
    def test_total_entries_stored(self):
        s = ActivityStats(total_entries=5, unique_docs=2, unique_actors=3)
        assert s.total_entries == 5

    def test_unique_docs_stored(self):
        s = ActivityStats(total_entries=0, unique_docs=7, unique_actors=1)
        assert s.unique_docs == 7

    def test_unique_actors_stored(self):
        s = ActivityStats(total_entries=10, unique_docs=3, unique_actors=4)
        assert s.unique_actors == 4

    def test_action_counts_default_empty(self):
        s = ActivityStats(total_entries=0, unique_docs=0, unique_actors=0)
        assert s.action_counts == {}

    def test_action_counts_stored(self):
        s = ActivityStats(
            total_entries=3, unique_docs=1, unique_actors=1,
            action_counts={"created": 2, "viewed": 1},
        )
        assert s.action_counts["created"] == 2

    def test_is_dataclass(self):
        fnames = {f.name for f in fields(ActivityStats)}
        assert fnames == {"total_entries", "unique_docs", "unique_actors", "action_counts"}

    def test_field_count(self):
        assert len(fields(ActivityStats)) == 4


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_doc_ids_empty(self):
        log = make_log()
        assert log.doc_ids() == []

    def test_actors_empty(self):
        log = make_log()
        assert log.actors() == []

    def test_actions_empty(self):
        log = make_log()
        assert log.actions() == []

    def test_recent_empty(self):
        log = make_log()
        assert log.recent() == []

    def test_stats_zeros(self):
        log = make_log()
        s = log.stats()
        assert s.total_entries == 0
        assert s.unique_docs == 0
        assert s.unique_actors == 0
        assert s.action_counts == {}


# ---------------------------------------------------------------------------
# TestLog
# ---------------------------------------------------------------------------

class TestLog:
    def test_returns_activity_entry(self):
        log = make_log()
        e = log.log("doc1", "created", "alice")
        assert isinstance(e, ActivityEntry)

    def test_entry_id_starts_at_one(self):
        log = make_log()
        e = log.log("doc1", "created", "alice")
        assert e.entry_id == 1

    def test_entry_id_increments(self):
        log = make_log()
        e1 = log.log("doc1", "created", "alice")
        e2 = log.log("doc2", "viewed", "bob")
        assert e2.entry_id == e1.entry_id + 1

    def test_entry_id_increments_across_docs(self):
        log = make_log()
        ids = [log.log(f"doc{i}", "viewed", "u").entry_id for i in range(5)]
        assert ids == list(range(1, 6))

    def test_timestamp_set_from_now_param(self):
        log = make_log()
        e = log.log("d", "created", "u", now=9999.0)
        assert e.timestamp == 9999.0

    def test_timestamp_auto_set_when_now_is_none(self):
        import time as _time
        log = make_log()
        before = _time.time()
        e = log.log("d", "created", "u")
        after = _time.time()
        assert before <= e.timestamp <= after

    def test_metadata_stored(self):
        log = make_log()
        e = log.log("d", "edited", "u", metadata={"field": "title"})
        assert e.metadata["field"] == "title"

    def test_metadata_none_becomes_empty_dict(self):
        log = make_log()
        e = log.log("d", "viewed", "u", metadata=None)
        assert e.metadata == {}

    def test_metadata_copy_is_independent(self):
        log = make_log()
        meta = {"k": "v"}
        e = log.log("d", "viewed", "u", metadata=meta)
        meta["extra"] = "x"
        assert "extra" not in e.metadata

    def test_doc_id_stored_in_entry(self):
        log = make_log()
        e = log.log("my-doc", "created", "alice")
        assert e.doc_id == "my-doc"

    def test_action_stored_in_entry(self):
        log = make_log()
        e = log.log("d", "shared", "u")
        assert e.action == "shared"

    def test_actor_stored_in_entry(self):
        log = make_log()
        e = log.log("d", "deleted", "sysbot")
        assert e.actor == "sysbot"


# ---------------------------------------------------------------------------
# TestEntriesForDoc
# ---------------------------------------------------------------------------

class TestEntriesForDoc:
    def test_empty_for_unknown_doc(self):
        log = make_log()
        assert log.entries_for_doc("nope") == []

    def test_single_entry(self):
        log = make_log()
        log.log("doc1", "created", "alice")
        result = log.entries_for_doc("doc1")
        assert len(result) == 1
        assert result[0].doc_id == "doc1"

    def test_multiple_entries_insertion_order(self):
        log = make_log()
        log.log("doc1", "created", "alice", now=1.0)
        log.log("doc1", "edited", "bob", now=2.0)
        log.log("doc1", "viewed", "charlie", now=3.0)
        result = log.entries_for_doc("doc1")
        assert [e.action for e in result] == ["created", "edited", "viewed"]

    def test_isolates_to_requested_doc(self):
        log = make_log()
        log.log("doc1", "created", "alice")
        log.log("doc2", "created", "bob")
        assert len(log.entries_for_doc("doc1")) == 1

    def test_limit_parameter(self):
        log = make_log()
        for i in range(5):
            log.log("doc1", "viewed", "u", now=float(i))
        result = log.entries_for_doc("doc1", limit=3)
        assert len(result) == 3

    def test_limit_returns_first_n(self):
        log = make_log()
        for i in range(4):
            log.log("doc1", f"action{i}", "u", now=float(i))
        result = log.entries_for_doc("doc1", limit=2)
        assert result[0].action == "action0"
        assert result[1].action == "action1"

    def test_limit_none_returns_all(self):
        log = make_log()
        for _ in range(10):
            log.log("doc1", "viewed", "u")
        assert len(log.entries_for_doc("doc1", limit=None)) == 10


# ---------------------------------------------------------------------------
# TestEntriesByActor
# ---------------------------------------------------------------------------

class TestEntriesByActor:
    def test_empty_for_unknown_actor(self):
        log = make_log()
        assert log.entries_by_actor("nobody") == []

    def test_single_entry(self):
        log = make_log()
        log.log("d", "viewed", "alice")
        result = log.entries_by_actor("alice")
        assert len(result) == 1

    def test_multiple_entries_insertion_order(self):
        log = make_log()
        log.log("d1", "created", "alice", now=1.0)
        log.log("d2", "edited", "alice", now=2.0)
        log.log("d3", "viewed", "alice", now=3.0)
        result = log.entries_by_actor("alice")
        assert [e.doc_id for e in result] == ["d1", "d2", "d3"]

    def test_isolates_to_requested_actor(self):
        log = make_log()
        log.log("d", "viewed", "alice")
        log.log("d", "viewed", "bob")
        assert len(log.entries_by_actor("alice")) == 1

    def test_limit_parameter(self):
        log = make_log()
        for i in range(6):
            log.log(f"doc{i}", "viewed", "alice")
        result = log.entries_by_actor("alice", limit=3)
        assert len(result) == 3

    def test_limit_returns_first_n(self):
        log = make_log()
        for i in range(4):
            log.log(f"doc{i}", "viewed", "alice", now=float(i))
        result = log.entries_by_actor("alice", limit=2)
        assert result[0].doc_id == "doc0"
        assert result[1].doc_id == "doc1"


# ---------------------------------------------------------------------------
# TestEntriesByAction
# ---------------------------------------------------------------------------

class TestEntriesByAction:
    def test_empty_for_unknown_action(self):
        log = make_log()
        assert log.entries_by_action("nonexistent") == []

    def test_single_entry(self):
        log = make_log()
        log.log("d", "created", "u")
        result = log.entries_by_action("created")
        assert len(result) == 1

    def test_multiple_entries(self):
        log = make_log()
        log.log("d1", "created", "u")
        log.log("d2", "viewed", "u")
        log.log("d3", "created", "u")
        result = log.entries_by_action("created")
        assert len(result) == 2

    def test_insertion_order_preserved(self):
        log = make_log()
        log.log("d1", "edited", "alice", now=1.0)
        log.log("d2", "edited", "bob", now=2.0)
        result = log.entries_by_action("edited")
        assert result[0].actor == "alice"
        assert result[1].actor == "bob"

    def test_limit_parameter(self):
        log = make_log()
        for i in range(5):
            log.log(f"doc{i}", "viewed", "u")
        result = log.entries_by_action("viewed", limit=2)
        assert len(result) == 2

    def test_limit_returns_first_n(self):
        log = make_log()
        for i in range(4):
            log.log(f"doc{i}", "viewed", "u", now=float(i))
        result = log.entries_by_action("viewed", limit=3)
        assert result[0].doc_id == "doc0"
        assert result[2].doc_id == "doc2"


# ---------------------------------------------------------------------------
# TestRecent
# ---------------------------------------------------------------------------

class TestRecent:
    def test_empty_log(self):
        log = make_log()
        assert log.recent(5) == []

    def test_fewer_than_limit(self):
        log = make_log()
        log.log("d", "created", "u")
        log.log("d", "viewed", "u")
        result = log.recent(10)
        assert len(result) == 2

    def test_exactly_limit(self):
        log = make_log()
        for i in range(5):
            log.log(f"doc{i}", "viewed", "u")
        result = log.recent(5)
        assert len(result) == 5

    def test_more_than_limit_returns_tail(self):
        log = make_log()
        for i in range(10):
            log.log(f"doc{i}", "viewed", "u", now=float(i))
        result = log.recent(3)
        assert len(result) == 3
        # tail means the last 3 logged
        assert result[0].doc_id == "doc7"
        assert result[2].doc_id == "doc9"

    def test_default_limit_is_ten(self):
        log = make_log()
        for i in range(15):
            log.log(f"doc{i}", "viewed", "u")
        result = log.recent()
        assert len(result) == 10

    def test_recent_preserves_insertion_order(self):
        log = make_log()
        for i in range(5):
            log.log(f"doc{i}", "viewed", "u", now=float(i))
        result = log.recent(5)
        assert [e.doc_id for e in result] == [f"doc{i}" for i in range(5)]


# ---------------------------------------------------------------------------
# TestGetEntry
# ---------------------------------------------------------------------------

class TestGetEntry:
    def test_found_by_id(self):
        log = make_log()
        e = log.log("d", "created", "alice")
        found = log.get_entry(e.entry_id)
        assert found is not None
        assert found.entry_id == e.entry_id

    def test_not_found_returns_none(self):
        log = make_log()
        assert log.get_entry(9999) is None

    def test_found_entry_has_correct_fields(self):
        log = make_log()
        log.log("doc1", "created", "alice", now=42.0)
        log.log("doc2", "viewed", "bob", now=43.0)
        found = log.get_entry(2)
        assert found.doc_id == "doc2"
        assert found.actor == "bob"
        assert found.timestamp == 43.0

    def test_get_entry_first(self):
        log = make_log()
        log.log("d", "created", "u")
        log.log("d", "viewed", "u")
        assert log.get_entry(1).action == "created"

    def test_get_entry_zero_not_found(self):
        log = make_log()
        log.log("d", "created", "u")
        assert log.get_entry(0) is None


# ---------------------------------------------------------------------------
# TestDocIds
# ---------------------------------------------------------------------------

class TestDocIds:
    def test_empty_initially(self):
        log = make_log()
        assert log.doc_ids() == []

    def test_single_doc(self):
        log = make_log()
        log.log("doc1", "created", "u")
        assert log.doc_ids() == ["doc1"]

    def test_multiple_docs_sorted(self):
        log = make_log()
        log.log("doc-c", "created", "u")
        log.log("doc-a", "viewed", "u")
        log.log("doc-b", "edited", "u")
        assert log.doc_ids() == ["doc-a", "doc-b", "doc-c"]

    def test_duplicate_entries_same_doc_deduplicated(self):
        log = make_log()
        log.log("doc1", "created", "u")
        log.log("doc1", "edited", "u")
        log.log("doc1", "viewed", "u")
        assert log.doc_ids() == ["doc1"]

    def test_mixed_docs_sorted(self):
        log = make_log()
        for name in ["z-doc", "a-doc", "m-doc"]:
            log.log(name, "viewed", "u")
        assert log.doc_ids() == ["a-doc", "m-doc", "z-doc"]


# ---------------------------------------------------------------------------
# TestActors
# ---------------------------------------------------------------------------

class TestActors:
    def test_empty_initially(self):
        log = make_log()
        assert log.actors() == []

    def test_single_actor(self):
        log = make_log()
        log.log("d", "viewed", "alice")
        assert log.actors() == ["alice"]

    def test_multiple_actors_sorted(self):
        log = make_log()
        log.log("d", "created", "charlie")
        log.log("d", "viewed", "alice")
        log.log("d", "edited", "bob")
        assert log.actors() == ["alice", "bob", "charlie"]

    def test_actors_deduplicated(self):
        log = make_log()
        log.log("d1", "created", "alice")
        log.log("d2", "edited", "alice")
        log.log("d3", "viewed", "alice")
        assert log.actors() == ["alice"]

    def test_actors_two_unique(self):
        log = make_log()
        log.log("d", "created", "zara")
        log.log("d", "viewed", "amit")
        assert log.actors() == ["amit", "zara"]


# ---------------------------------------------------------------------------
# TestActions
# ---------------------------------------------------------------------------

class TestActions:
    def test_empty_initially(self):
        log = make_log()
        assert log.actions() == []

    def test_single_action(self):
        log = make_log()
        log.log("d", "created", "u")
        assert log.actions() == ["created"]

    def test_multiple_actions_sorted(self):
        log = make_log()
        log.log("d", "viewed", "u")
        log.log("d", "created", "u")
        log.log("d", "edited", "u")
        assert log.actions() == ["created", "edited", "viewed"]

    def test_actions_deduplicated(self):
        log = make_log()
        log.log("d1", "viewed", "u")
        log.log("d2", "viewed", "u")
        log.log("d3", "viewed", "u")
        assert log.actions() == ["viewed"]

    def test_all_standard_actions(self):
        log = make_log()
        for action in ["deleted", "shared", "created", "edited", "viewed"]:
            log.log("d", action, "u")
        assert log.actions() == ["created", "deleted", "edited", "shared", "viewed"]


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_returns_activity_stats_instance(self):
        log = make_log()
        assert isinstance(log.stats(), ActivityStats)

    def test_empty_log_zeros(self):
        log = make_log()
        s = log.stats()
        assert s.total_entries == 0
        assert s.unique_docs == 0
        assert s.unique_actors == 0
        assert s.action_counts == {}

    def test_total_entries(self):
        log = make_log()
        log.log("d1", "created", "alice")
        log.log("d2", "viewed", "bob")
        log.log("d1", "edited", "alice")
        s = log.stats()
        assert s.total_entries == 3

    def test_unique_docs(self):
        log = make_log()
        log.log("doc1", "created", "u")
        log.log("doc2", "viewed", "u")
        log.log("doc1", "edited", "u")
        s = log.stats()
        assert s.unique_docs == 2

    def test_unique_actors(self):
        log = make_log()
        log.log("d", "created", "alice")
        log.log("d", "viewed", "bob")
        log.log("d", "edited", "alice")
        s = log.stats()
        assert s.unique_actors == 2

    def test_action_counts_single(self):
        log = make_log()
        log.log("d", "created", "u")
        log.log("d", "created", "u")
        log.log("d", "viewed", "u")
        s = log.stats()
        assert s.action_counts["created"] == 2
        assert s.action_counts["viewed"] == 1

    def test_action_counts_dict_is_complete(self):
        log = make_log()
        for action in ["created", "edited", "deleted"]:
            log.log("d", action, "u")
        s = log.stats()
        assert set(s.action_counts.keys()) == {"created", "edited", "deleted"}


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_log_calls_no_errors(self):
        log = make_log()
        errors = []

        def worker(i: int) -> None:
            try:
                log.log(f"doc{i % 5}", "viewed", f"user{i % 10}")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []

    def test_concurrent_log_unique_entry_ids(self):
        log = make_log()
        collected: list[int] = []
        lock = threading.Lock()

        def worker() -> None:
            e = log.log("doc", "viewed", "u")
            with lock:
                collected.append(e.entry_id)

        threads = [threading.Thread(target=worker) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(set(collected)) == 50

    def test_concurrent_log_total_entries(self):
        log = make_log()

        def worker(i: int) -> None:
            log.log(f"doc{i}", "created", "u")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(80)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert log.stats().total_entries == 80

    def test_concurrent_log_and_query(self):
        log = make_log()
        errors = []

        def logger(i: int) -> None:
            try:
                for j in range(5):
                    log.log(f"doc{i}", "viewed", f"actor{i}", now=float(j))
            except Exception as exc:
                errors.append(exc)

        def reader() -> None:
            try:
                for _ in range(10):
                    log.recent(5)
                    log.doc_ids()
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=logger, args=(i,)) for i in range(10)]
        threads += [threading.Thread(target=reader) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []

    def test_concurrent_entries_for_doc(self):
        log = make_log()
        for i in range(20):
            log.log("shared-doc", "viewed", f"actor{i}")

        errors = []

        def reader() -> None:
            try:
                result = log.entries_for_doc("shared-doc")
                assert len(result) >= 20
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=reader) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
