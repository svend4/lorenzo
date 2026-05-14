"""Tests for E307 DocReadTracker."""
from __future__ import annotations

import threading
import time
from dataclasses import fields

import pytest

from docstoolkit.doc_read_tracker import DocReadTracker, ReadEvent, ReadStats


# ─────────────────────────────────────────────────────────────── dataclasses ──

class TestReadEventDataclass:
    def test_fields_exist(self):
        names = {f.name for f in fields(ReadEvent)}
        assert names == {"event_id", "doc_id", "user_id", "read_at", "duration_seconds"}

    def test_defaults(self):
        e = ReadEvent(event_id=1, doc_id="d", user_id="u")
        assert e.read_at == 0.0
        assert e.duration_seconds == 0.0

    def test_construct_with_all_fields(self):
        e = ReadEvent(event_id=7, doc_id="doc1", user_id="alice", read_at=1.0, duration_seconds=30.0)
        assert e.event_id == 7
        assert e.doc_id == "doc1"
        assert e.user_id == "alice"
        assert e.read_at == 1.0
        assert e.duration_seconds == 30.0

    def test_equality(self):
        a = ReadEvent(event_id=1, doc_id="d", user_id="u", read_at=1.0, duration_seconds=5.0)
        b = ReadEvent(event_id=1, doc_id="d", user_id="u", read_at=1.0, duration_seconds=5.0)
        assert a == b

    def test_inequality(self):
        a = ReadEvent(event_id=1, doc_id="d", user_id="u")
        b = ReadEvent(event_id=2, doc_id="d", user_id="u")
        assert a != b


class TestReadStatsDataclass:
    def test_fields_exist(self):
        names = {f.name for f in fields(ReadStats)}
        assert names == {"doc_id", "total_reads", "unique_readers", "avg_duration", "last_read_at"}

    def test_construct(self):
        s = ReadStats(doc_id="doc1", total_reads=5, unique_readers=3, avg_duration=12.5, last_read_at=999.0)
        assert s.doc_id == "doc1"
        assert s.total_reads == 5
        assert s.unique_readers == 3
        assert s.avg_duration == 12.5
        assert s.last_read_at == 999.0

    def test_equality(self):
        a = ReadStats(doc_id="d", total_reads=1, unique_readers=1, avg_duration=0.0, last_read_at=0.0)
        b = ReadStats(doc_id="d", total_reads=1, unique_readers=1, avg_duration=0.0, last_read_at=0.0)
        assert a == b


# ──────────────────────────────────────────────────────────────────────────────

class TestConstruction:
    def test_instantiation(self):
        t = DocReadTracker()
        assert t is not None

    def test_empty_initial_state(self):
        t = DocReadTracker()
        assert t.all_doc_ids() == []
        assert t.recent_events() == []

    def test_multiple_instances_are_independent(self):
        t1 = DocReadTracker()
        t2 = DocReadTracker()
        t1.record("doc1", "user1", now=1.0)
        assert t2.all_doc_ids() == []


# ──────────────────────────────────────────────────────────────────────────────

class TestRecord:
    def test_returns_read_event(self):
        t = DocReadTracker()
        e = t.record("doc1", "alice", now=100.0)
        assert isinstance(e, ReadEvent)

    def test_event_id_starts_at_1(self):
        t = DocReadTracker()
        e = t.record("doc1", "alice", now=1.0)
        assert e.event_id == 1

    def test_event_id_increments(self):
        t = DocReadTracker()
        ids = [t.record("doc1", "alice", now=float(i)).event_id for i in range(1, 6)]
        assert ids == [1, 2, 3, 4, 5]

    def test_timestamp_stored(self):
        t = DocReadTracker()
        e = t.record("doc1", "alice", now=12345.0)
        assert e.read_at == 12345.0

    def test_duration_stored(self):
        t = DocReadTracker()
        e = t.record("doc1", "alice", duration_seconds=42.5, now=1.0)
        assert e.duration_seconds == 42.5

    def test_default_duration_is_zero(self):
        t = DocReadTracker()
        e = t.record("doc1", "alice", now=1.0)
        assert e.duration_seconds == 0.0

    def test_doc_id_and_user_id_stored(self):
        t = DocReadTracker()
        e = t.record("my_doc", "bob", now=1.0)
        assert e.doc_id == "my_doc"
        assert e.user_id == "bob"

    def test_now_uses_time_time_when_omitted(self):
        t = DocReadTracker()
        before = time.time()
        e = t.record("doc1", "alice")
        after = time.time()
        assert before <= e.read_at <= after

    def test_multiple_records_different_docs(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        t.record("doc2", "bob", now=2.0)
        assert set(t.all_doc_ids()) == {"doc1", "doc2"}


# ──────────────────────────────────────────────────────────────────────────────

class TestEventsForDoc:
    def test_empty_for_unknown_doc(self):
        t = DocReadTracker()
        assert t.events_for_doc("nonexistent") == []

    def test_single_event(self):
        t = DocReadTracker()
        e = t.record("doc1", "alice", now=1.0)
        assert t.events_for_doc("doc1") == [e]

    def test_multiple_events_insertion_order(self):
        t = DocReadTracker()
        e1 = t.record("doc1", "alice", now=1.0)
        e2 = t.record("doc1", "bob", now=2.0)
        e3 = t.record("doc1", "alice", now=3.0)
        assert t.events_for_doc("doc1") == [e1, e2, e3]

    def test_limit_zero_returns_empty(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        assert t.events_for_doc("doc1", limit=0) == []

    def test_limit_one(self):
        t = DocReadTracker()
        e1 = t.record("doc1", "alice", now=1.0)
        t.record("doc1", "bob", now=2.0)
        assert t.events_for_doc("doc1", limit=1) == [e1]

    def test_limit_larger_than_list(self):
        t = DocReadTracker()
        e1 = t.record("doc1", "alice", now=1.0)
        e2 = t.record("doc1", "bob", now=2.0)
        assert t.events_for_doc("doc1", limit=100) == [e1, e2]

    def test_other_doc_not_included(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        e2 = t.record("doc2", "bob", now=2.0)
        assert t.events_for_doc("doc2") == [e2]


# ──────────────────────────────────────────────────────────────────────────────

class TestEventsForUser:
    def test_empty_for_unknown_user(self):
        t = DocReadTracker()
        assert t.events_for_user("ghost") == []

    def test_single_event(self):
        t = DocReadTracker()
        e = t.record("doc1", "alice", now=1.0)
        assert t.events_for_user("alice") == [e]

    def test_multiple_events_insertion_order(self):
        t = DocReadTracker()
        e1 = t.record("doc1", "alice", now=1.0)
        e2 = t.record("doc2", "alice", now=2.0)
        e3 = t.record("doc3", "alice", now=3.0)
        assert t.events_for_user("alice") == [e1, e2, e3]

    def test_limit_applied(self):
        t = DocReadTracker()
        e1 = t.record("doc1", "alice", now=1.0)
        t.record("doc2", "alice", now=2.0)
        assert t.events_for_user("alice", limit=1) == [e1]

    def test_other_user_not_included(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        e2 = t.record("doc1", "bob", now=2.0)
        assert t.events_for_user("bob") == [e2]


# ──────────────────────────────────────────────────────────────────────────────

class TestHasRead:
    def test_false_before_any_record(self):
        t = DocReadTracker()
        assert t.has_read("alice", "doc1") is False

    def test_true_after_record(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        assert t.has_read("alice", "doc1") is True

    def test_false_for_different_doc(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        assert t.has_read("alice", "doc2") is False

    def test_false_for_different_user(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        assert t.has_read("bob", "doc1") is False

    def test_true_after_multiple_reads(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        t.record("doc1", "alice", now=2.0)
        assert t.has_read("alice", "doc1") is True


# ──────────────────────────────────────────────────────────────────────────────

class TestReadCount:
    def test_zero_for_unknown_doc(self):
        t = DocReadTracker()
        assert t.read_count("nope") == 0

    def test_increments_with_each_record(self):
        t = DocReadTracker()
        for i in range(1, 6):
            t.record("doc1", f"user{i}", now=float(i))
            assert t.read_count("doc1") == i

    def test_different_docs_counted_separately(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        t.record("doc1", "bob", now=2.0)
        t.record("doc2", "carol", now=3.0)
        assert t.read_count("doc1") == 2
        assert t.read_count("doc2") == 1

    def test_same_user_multiple_reads(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        t.record("doc1", "alice", now=2.0)
        assert t.read_count("doc1") == 2


# ──────────────────────────────────────────────────────────────────────────────

class TestUniqueReaders:
    def test_empty_for_unknown_doc(self):
        t = DocReadTracker()
        assert t.unique_readers("doc1") == []

    def test_single_reader(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        assert t.unique_readers("doc1") == ["alice"]

    def test_deduplicated(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        t.record("doc1", "alice", now=2.0)
        assert t.unique_readers("doc1") == ["alice"]

    def test_sorted(self):
        t = DocReadTracker()
        for name in ["zara", "alice", "bob", "carol"]:
            t.record("doc1", name, now=1.0)
        assert t.unique_readers("doc1") == ["alice", "bob", "carol", "zara"]

    def test_multiple_docs_independent(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        t.record("doc2", "bob", now=2.0)
        assert t.unique_readers("doc1") == ["alice"]
        assert t.unique_readers("doc2") == ["bob"]


# ──────────────────────────────────────────────────────────────────────────────

class TestMostReadDocs:
    def test_empty_tracker(self):
        t = DocReadTracker()
        assert t.most_read_docs() == []

    def test_single_doc(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        assert t.most_read_docs() == [("doc1", 1)]

    def test_sorted_by_count_desc(self):
        t = DocReadTracker()
        for _ in range(3):
            t.record("doc1", "alice", now=1.0)
        for _ in range(5):
            t.record("doc2", "bob", now=1.0)
        t.record("doc3", "carol", now=1.0)
        result = t.most_read_docs()
        assert result[0] == ("doc2", 5)
        assert result[1] == ("doc1", 3)
        assert result[2] == ("doc3", 1)

    def test_tie_broken_by_doc_id_asc(self):
        t = DocReadTracker()
        t.record("zebra", "u", now=1.0)
        t.record("apple", "u", now=2.0)
        t.record("mango", "u", now=3.0)
        result = t.most_read_docs()
        ids = [r[0] for r in result]
        assert ids == ["apple", "mango", "zebra"]

    def test_limit_applied(self):
        t = DocReadTracker()
        for i in range(5):
            t.record(f"doc{i}", "alice", now=float(i))
        result = t.most_read_docs(limit=3)
        assert len(result) == 3

    def test_limit_larger_than_docs(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        result = t.most_read_docs(limit=100)
        assert len(result) == 1


# ──────────────────────────────────────────────────────────────────────────────

class TestRecentEvents:
    def test_empty_tracker(self):
        t = DocReadTracker()
        assert t.recent_events() == []

    def test_single_event(self):
        t = DocReadTracker()
        e = t.record("doc1", "alice", now=1.0)
        assert t.recent_events() == [e]

    def test_tail_semantics(self):
        t = DocReadTracker()
        events = [t.record("doc1", "alice", now=float(i)) for i in range(1, 16)]
        recent = t.recent_events(limit=10)
        assert recent == events[-10:]

    def test_limit_larger_than_total(self):
        t = DocReadTracker()
        events = [t.record("doc1", "alice", now=float(i)) for i in range(5)]
        assert t.recent_events(limit=20) == events

    def test_limit_one_returns_last(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        last = t.record("doc2", "bob", now=2.0)
        assert t.recent_events(limit=1) == [last]

    def test_default_limit_is_ten(self):
        t = DocReadTracker()
        for i in range(15):
            t.record("doc1", "alice", now=float(i))
        assert len(t.recent_events()) == 10


# ──────────────────────────────────────────────────────────────────────────────

class TestStatsForDoc:
    def test_zero_reads(self):
        t = DocReadTracker()
        s = t.stats_for_doc("unknown")
        assert s.doc_id == "unknown"
        assert s.total_reads == 0
        assert s.unique_readers == 0
        assert s.avg_duration == 0.0
        assert s.last_read_at == 0.0

    def test_total_reads(self):
        t = DocReadTracker()
        for i in range(4):
            t.record("doc1", f"u{i}", now=float(i + 1))
        assert t.stats_for_doc("doc1").total_reads == 4

    def test_unique_readers_count(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        t.record("doc1", "alice", now=2.0)
        t.record("doc1", "bob", now=3.0)
        assert t.stats_for_doc("doc1").unique_readers == 2

    def test_avg_duration_only_counts_nonzero(self):
        t = DocReadTracker()
        t.record("doc1", "alice", duration_seconds=0.0, now=1.0)   # excluded
        t.record("doc1", "bob", duration_seconds=10.0, now=2.0)
        t.record("doc1", "carol", duration_seconds=30.0, now=3.0)
        s = t.stats_for_doc("doc1")
        assert s.avg_duration == pytest.approx(20.0)

    def test_avg_duration_all_zero(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        t.record("doc1", "bob", now=2.0)
        assert t.stats_for_doc("doc1").avg_duration == 0.0

    def test_last_read_at(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=5.0)
        t.record("doc1", "bob", now=10.0)
        t.record("doc1", "carol", now=3.0)
        assert t.stats_for_doc("doc1").last_read_at == 10.0

    def test_returns_read_stats_instance(self):
        t = DocReadTracker()
        t.record("doc1", "alice", now=1.0)
        assert isinstance(t.stats_for_doc("doc1"), ReadStats)


# ──────────────────────────────────────────────────────────────────────────────

class TestAllDocIds:
    def test_empty(self):
        t = DocReadTracker()
        assert t.all_doc_ids() == []

    def test_sorted(self):
        t = DocReadTracker()
        for name in ["zebra", "alpha", "mango"]:
            t.record(name, "alice", now=1.0)
        assert t.all_doc_ids() == ["alpha", "mango", "zebra"]

    def test_no_duplicates(self):
        t = DocReadTracker()
        for _ in range(3):
            t.record("doc1", "alice", now=1.0)
        assert t.all_doc_ids() == ["doc1"]

    def test_multiple_docs(self):
        t = DocReadTracker()
        t.record("c_doc", "u", now=1.0)
        t.record("a_doc", "u", now=2.0)
        t.record("b_doc", "u", now=3.0)
        assert t.all_doc_ids() == ["a_doc", "b_doc", "c_doc"]


# ──────────────────────────────────────────────────────────────────────────────

class TestThreadSafety:
    def test_concurrent_record_calls(self):
        t = DocReadTracker()
        num_threads = 20
        records_per_thread = 50
        errors: list[Exception] = []

        def worker(tid: int) -> None:
            try:
                for i in range(records_per_thread):
                    t.record(f"doc{tid % 5}", f"user{tid}", duration_seconds=float(i))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_threads)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert errors == [], f"Thread errors: {errors}"
        total_expected = num_threads * records_per_thread
        assert len(t._events) == total_expected

    def test_event_ids_are_unique_under_concurrency(self):
        t = DocReadTracker()
        ids: list[int] = []
        lock = threading.Lock()

        def worker() -> None:
            for _ in range(25):
                e = t.record("doc1", "user", now=1.0)
                with lock:
                    ids.append(e.event_id)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert len(ids) == len(set(ids)), "Duplicate event_ids detected"

    def test_read_count_consistent_under_concurrency(self):
        t = DocReadTracker()
        num_threads = 10
        per_thread = 30

        def worker() -> None:
            for _ in range(per_thread):
                t.record("shared_doc", "user", now=1.0)

        threads = [threading.Thread(target=worker) for _ in range(num_threads)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert t.read_count("shared_doc") == num_threads * per_thread
