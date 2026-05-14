"""Tests for E371 DocProgressLog."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_progress_log import (
    DocProgressLog,
    ProgressEntry,
    ProgressStats,
    ProgressSummary,
)


class TestProgressEntryDataclass:
    def test_construct_full(self):
        e = ProgressEntry(
            entry_id=1,
            operation_id="op1",
            doc_id="d1",
            percent=10.0,
            message="hi",
            recorded_at=123.0,
        )
        assert e.entry_id == 1
        assert e.operation_id == "op1"
        assert e.doc_id == "d1"
        assert e.percent == 10.0
        assert e.message == "hi"
        assert e.recorded_at == 123.0

    def test_defaults(self):
        e = ProgressEntry(entry_id=1, operation_id="op", doc_id="d", percent=5.0)
        assert e.message == ""
        assert e.recorded_at == 0.0

    def test_equality(self):
        a = ProgressEntry(1, "o", "d", 5.0, "m", 1.0)
        b = ProgressEntry(1, "o", "d", 5.0, "m", 1.0)
        assert a == b

    def test_inequality(self):
        a = ProgressEntry(1, "o", "d", 5.0, "m", 1.0)
        b = ProgressEntry(2, "o", "d", 5.0, "m", 1.0)
        assert a != b


class TestProgressSummaryDataclass:
    def test_construct(self):
        s = ProgressSummary(
            operation_id="op",
            doc_id="d",
            current_percent=50.0,
            entry_count=3,
            started_at=1.0,
            last_updated_at=5.0,
        )
        assert s.operation_id == "op"
        assert s.doc_id == "d"
        assert s.current_percent == 50.0
        assert s.entry_count == 3
        assert s.started_at == 1.0
        assert s.last_updated_at == 5.0

    def test_equality(self):
        a = ProgressSummary("o", "d", 1.0, 1, 0.0, 0.0)
        b = ProgressSummary("o", "d", 1.0, 1, 0.0, 0.0)
        assert a == b


class TestProgressStatsDataclass:
    def test_construct(self):
        st = ProgressStats(total_entries=10, unique_operations=3, unique_docs=2)
        assert st.total_entries == 10
        assert st.unique_operations == 3
        assert st.unique_docs == 2

    def test_equality(self):
        a = ProgressStats(1, 1, 1)
        b = ProgressStats(1, 1, 1)
        assert a == b


class TestConstruction:
    def test_default(self):
        log = DocProgressLog()
        assert log.stats().total_entries == 0

    def test_independent_instances(self):
        a = DocProgressLog()
        b = DocProgressLog()
        a.log_progress("op", "d", 10.0, now=1.0)
        assert b.stats().total_entries == 0

    def test_empty_all_operations(self):
        log = DocProgressLog()
        assert log.all_operations() == []


class TestLogProgress:
    def test_basic(self):
        log = DocProgressLog()
        e = log.log_progress("op", "d", 10.0, "start", now=100.0)
        assert e.entry_id == 1
        assert e.operation_id == "op"
        assert e.doc_id == "d"
        assert e.percent == 10.0
        assert e.message == "start"
        assert e.recorded_at == 100.0

    def test_id_increments(self):
        log = DocProgressLog()
        a = log.log_progress("op", "d", 10.0, now=1.0)
        b = log.log_progress("op", "d", 20.0, now=2.0)
        c = log.log_progress("op2", "d2", 5.0, now=3.0)
        assert a.entry_id == 1
        assert b.entry_id == 2
        assert c.entry_id == 3

    def test_clamp_low(self):
        log = DocProgressLog()
        e = log.log_progress("op", "d", -50.0, now=1.0)
        assert e.percent == 0.0

    def test_clamp_high(self):
        log = DocProgressLog()
        e = log.log_progress("op", "d", 150.0, now=1.0)
        assert e.percent == 100.0

    def test_clamp_boundary_zero(self):
        log = DocProgressLog()
        e = log.log_progress("op", "d", 0.0, now=1.0)
        assert e.percent == 0.0

    def test_clamp_boundary_hundred(self):
        log = DocProgressLog()
        e = log.log_progress("op", "d", 100.0, now=1.0)
        assert e.percent == 100.0

    def test_uses_time_when_now_none(self):
        log = DocProgressLog()
        e = log.log_progress("op", "d", 10.0)
        assert e.recorded_at > 0.0

    def test_default_message_empty(self):
        log = DocProgressLog()
        e = log.log_progress("op", "d", 10.0, now=1.0)
        assert e.message == ""


class TestEntriesFor:
    def test_empty(self):
        log = DocProgressLog()
        assert log.entries_for("nope") == []

    def test_most_recent_first(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 10.0, "a", now=1.0)
        log.log_progress("op", "d", 20.0, "b", now=2.0)
        log.log_progress("op", "d", 30.0, "c", now=3.0)
        entries = log.entries_for("op")
        assert [e.message for e in entries] == ["c", "b", "a"]

    def test_limit(self):
        log = DocProgressLog()
        for i in range(5):
            log.log_progress("op", "d", float(i * 10), str(i), now=float(i))
        entries = log.entries_for("op", limit=2)
        assert len(entries) == 2
        assert entries[0].message == "4"
        assert entries[1].message == "3"

    def test_limit_larger_than_count(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 10.0, now=1.0)
        assert len(log.entries_for("op", limit=100)) == 1

    def test_only_returns_matching_operation(self):
        log = DocProgressLog()
        log.log_progress("op1", "d", 10.0, now=1.0)
        log.log_progress("op2", "d", 20.0, now=2.0)
        entries = log.entries_for("op1")
        assert len(entries) == 1
        assert entries[0].operation_id == "op1"


class TestSummary:
    def test_none_when_empty(self):
        log = DocProgressLog()
        assert log.summary("op") is None

    def test_fields(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 10.0, now=1.0)
        log.log_progress("op", "d", 50.0, now=2.0)
        log.log_progress("op", "d", 75.0, now=3.0)
        s = log.summary("op")
        assert s is not None
        assert s.operation_id == "op"
        assert s.doc_id == "d"
        assert s.current_percent == 75.0
        assert s.entry_count == 3
        assert s.started_at == 1.0
        assert s.last_updated_at == 3.0

    def test_single_entry(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 42.0, now=10.0)
        s = log.summary("op")
        assert s is not None
        assert s.current_percent == 42.0
        assert s.entry_count == 1
        assert s.started_at == 10.0
        assert s.last_updated_at == 10.0


class TestLatestFor:
    def test_none_when_empty(self):
        log = DocProgressLog()
        assert log.latest_for("op") is None

    def test_returns_latest(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 10.0, "a", now=1.0)
        log.log_progress("op", "d", 20.0, "b", now=2.0)
        latest = log.latest_for("op")
        assert latest is not None
        assert latest.message == "b"
        assert latest.percent == 20.0

    def test_ignores_other_operations(self):
        log = DocProgressLog()
        log.log_progress("op1", "d", 10.0, "a", now=1.0)
        log.log_progress("op2", "d", 20.0, "b", now=2.0)
        latest = log.latest_for("op1")
        assert latest is not None
        assert latest.message == "a"


class TestOperationsForDoc:
    def test_empty(self):
        log = DocProgressLog()
        assert log.operations_for_doc("d") == []

    def test_sorted_unique(self):
        log = DocProgressLog()
        log.log_progress("opB", "d1", 10.0, now=1.0)
        log.log_progress("opA", "d1", 20.0, now=2.0)
        log.log_progress("opC", "d1", 30.0, now=3.0)
        log.log_progress("opA", "d1", 40.0, now=4.0)
        assert log.operations_for_doc("d1") == ["opA", "opB", "opC"]

    def test_filters_by_doc(self):
        log = DocProgressLog()
        log.log_progress("op1", "d1", 10.0, now=1.0)
        log.log_progress("op2", "d2", 20.0, now=2.0)
        assert log.operations_for_doc("d1") == ["op1"]
        assert log.operations_for_doc("d2") == ["op2"]


class TestEntriesForDoc:
    def test_empty(self):
        log = DocProgressLog()
        assert log.entries_for_doc("d") == []

    def test_most_recent_first(self):
        log = DocProgressLog()
        log.log_progress("op1", "d", 10.0, "a", now=1.0)
        log.log_progress("op2", "d", 20.0, "b", now=2.0)
        log.log_progress("op1", "d", 30.0, "c", now=3.0)
        entries = log.entries_for_doc("d")
        assert [e.message for e in entries] == ["c", "b", "a"]

    def test_filters_by_doc(self):
        log = DocProgressLog()
        log.log_progress("op", "d1", 10.0, now=1.0)
        log.log_progress("op", "d2", 20.0, now=2.0)
        log.log_progress("op", "d1", 30.0, now=3.0)
        entries = log.entries_for_doc("d1")
        assert len(entries) == 2
        assert all(e.doc_id == "d1" for e in entries)


class TestClearOperation:
    def test_returns_count(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 10.0, now=1.0)
        log.log_progress("op", "d", 20.0, now=2.0)
        assert log.clear_operation("op") == 2

    def test_returns_zero_for_unknown(self):
        log = DocProgressLog()
        assert log.clear_operation("nope") == 0

    def test_removes_entries(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 10.0, now=1.0)
        log.clear_operation("op")
        assert log.entries_for("op") == []
        assert log.summary("op") is None

    def test_preserves_other_operations(self):
        log = DocProgressLog()
        log.log_progress("op1", "d", 10.0, now=1.0)
        log.log_progress("op2", "d", 20.0, now=2.0)
        log.log_progress("op1", "d", 30.0, now=3.0)
        removed = log.clear_operation("op1")
        assert removed == 2
        # op2 still works
        assert len(log.entries_for("op2")) == 1
        s = log.summary("op2")
        assert s is not None
        assert s.current_percent == 20.0

    def test_clear_then_relog(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 10.0, now=1.0)
        log.clear_operation("op")
        e = log.log_progress("op", "d", 50.0, now=2.0)
        assert e.percent == 50.0
        assert log.entries_for("op")[0].percent == 50.0


class TestClearAll:
    def test_returns_count(self):
        log = DocProgressLog()
        log.log_progress("op1", "d", 10.0, now=1.0)
        log.log_progress("op2", "d", 20.0, now=2.0)
        log.log_progress("op2", "d", 30.0, now=3.0)
        assert log.clear_all() == 3

    def test_empty_returns_zero(self):
        log = DocProgressLog()
        assert log.clear_all() == 0

    def test_resets_state(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 10.0, now=1.0)
        log.clear_all()
        assert log.stats().total_entries == 0
        assert log.all_operations() == []
        assert log.entries_for("op") == []


class TestAllOperations:
    def test_empty(self):
        log = DocProgressLog()
        assert log.all_operations() == []

    def test_sorted_unique(self):
        log = DocProgressLog()
        log.log_progress("opB", "d", 10.0, now=1.0)
        log.log_progress("opA", "d", 20.0, now=2.0)
        log.log_progress("opC", "d", 30.0, now=3.0)
        log.log_progress("opA", "d", 40.0, now=4.0)
        assert log.all_operations() == ["opA", "opB", "opC"]

    def test_after_clear_operation(self):
        log = DocProgressLog()
        log.log_progress("op1", "d", 10.0, now=1.0)
        log.log_progress("op2", "d", 20.0, now=2.0)
        log.clear_operation("op1")
        assert log.all_operations() == ["op2"]


class TestStats:
    def test_empty(self):
        log = DocProgressLog()
        s = log.stats()
        assert s.total_entries == 0
        assert s.unique_operations == 0
        assert s.unique_docs == 0

    def test_totals(self):
        log = DocProgressLog()
        log.log_progress("op1", "d1", 10.0, now=1.0)
        log.log_progress("op1", "d2", 20.0, now=2.0)
        log.log_progress("op2", "d1", 30.0, now=3.0)
        log.log_progress("op2", "d3", 40.0, now=4.0)
        s = log.stats()
        assert s.total_entries == 4
        assert s.unique_operations == 2
        assert s.unique_docs == 3

    def test_after_clear_all(self):
        log = DocProgressLog()
        log.log_progress("op", "d", 10.0, now=1.0)
        log.clear_all()
        s = log.stats()
        assert s.total_entries == 0
        assert s.unique_operations == 0
        assert s.unique_docs == 0

    def test_single_doc_multiple_ops(self):
        log = DocProgressLog()
        log.log_progress("op1", "d", 10.0, now=1.0)
        log.log_progress("op2", "d", 20.0, now=2.0)
        s = log.stats()
        assert s.unique_docs == 1
        assert s.unique_operations == 2


class TestThreadSafety:
    def test_concurrent_log_progress(self):
        log = DocProgressLog()
        n_threads = 8
        n_per_thread = 50

        def worker(tid: int) -> None:
            for i in range(n_per_thread):
                log.log_progress(
                    f"op{tid}", f"doc{tid}", float(i % 101), f"msg{i}", now=float(i)
                )

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        total = n_threads * n_per_thread
        s = log.stats()
        assert s.total_entries == total
        assert s.unique_operations == n_threads
        assert s.unique_docs == n_threads
        # All entry_ids must be unique and contiguous
        all_entries: list[ProgressEntry] = []
        for op in log.all_operations():
            all_entries.extend(log.entries_for(op))
        ids = sorted(e.entry_id for e in all_entries)
        assert ids == list(range(1, total + 1))

    def test_concurrent_mixed_ops(self):
        log = DocProgressLog()

        def worker() -> None:
            for i in range(20):
                log.log_progress("shared", "d", float(i), now=float(i))

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = log.stats()
        assert s.total_entries == 100
        assert s.unique_operations == 1

    def test_concurrent_clear_and_log(self):
        log = DocProgressLog()
        for _ in range(20):
            log.log_progress("op", "d", 50.0, now=1.0)

        results: list[int] = []

        def clearer() -> None:
            results.append(log.clear_all())

        def logger() -> None:
            for i in range(10):
                log.log_progress("op2", "d2", float(i), now=float(i))

        threads = [
            threading.Thread(target=clearer),
            threading.Thread(target=logger),
            threading.Thread(target=logger),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # No crash and stats remain consistent
        s = log.stats()
        assert s.total_entries >= 0

    def test_concurrent_reads_during_writes(self):
        log = DocProgressLog()
        stop = threading.Event()

        def writer() -> None:
            i = 0
            while not stop.is_set() and i < 100:
                log.log_progress("op", "d", float(i % 101), now=float(i))
                i += 1

        def reader() -> None:
            while not stop.is_set():
                log.stats()
                log.all_operations()
                log.entries_for("op", limit=5)

        w = threading.Thread(target=writer)
        r = threading.Thread(target=reader)
        w.start()
        r.start()
        w.join()
        stop.set()
        r.join()
        # No exceptions => pass
        assert log.stats().total_entries > 0
