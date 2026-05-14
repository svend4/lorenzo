"""Tests for E360 DocDLQStore."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_dlq_store import DLQEntry, DLQStats, DocDLQStore


# --------------------------------------------------------------------- dataclasses


class TestDLQEntryDataclass:
    def test_defaults(self):
        e = DLQEntry()
        assert e.entry_id == 0
        assert e.doc_id == ""
        assert e.operation == ""
        assert e.payload == {}
        assert e.error == ""
        assert e.failed_at == 0.0
        assert e.attempts == 1
        assert e.retried_at is None
        assert e.resolved is False

    def test_payload_is_independent_per_instance(self):
        a = DLQEntry()
        b = DLQEntry()
        a.payload["k"] = "v"
        assert b.payload == {}

    def test_custom_fields(self):
        e = DLQEntry(
            entry_id=7,
            doc_id="d1",
            operation="op",
            payload={"x": 1},
            error="boom",
            failed_at=10.0,
            attempts=3,
            retried_at=15.0,
            resolved=True,
        )
        assert e.entry_id == 7
        assert e.doc_id == "d1"
        assert e.operation == "op"
        assert e.payload == {"x": 1}
        assert e.error == "boom"
        assert e.failed_at == 10.0
        assert e.attempts == 3
        assert e.retried_at == 15.0
        assert e.resolved is True


class TestDLQStatsDataclass:
    def test_defaults(self):
        s = DLQStats()
        assert s.total_entries == 0
        assert s.unresolved_count == 0
        assert s.unique_docs == 0
        assert s.total_attempts == 0

    def test_custom(self):
        s = DLQStats(total_entries=4, unresolved_count=2, unique_docs=3, total_attempts=9)
        assert s.total_entries == 4
        assert s.unresolved_count == 2
        assert s.unique_docs == 3
        assert s.total_attempts == 9


# --------------------------------------------------------------------- construction


class TestConstruction:
    def test_empty_store(self):
        s = DocDLQStore()
        assert s.stats().total_entries == 0

    def test_independent_state(self):
        a = DocDLQStore()
        b = DocDLQStore()
        a.record_failure("d", "op")
        assert b.stats().total_entries == 0

    def test_get_on_empty(self):
        s = DocDLQStore()
        assert s.get(1) is None

    def test_unresolved_on_empty(self):
        s = DocDLQStore()
        assert s.unresolved_entries() == []


# --------------------------------------------------------------------- record_failure


class TestRecordFailure:
    def test_returns_entry(self):
        s = DocDLQStore()
        e = s.record_failure("d1", "op1", error="boom", payload={"a": 1}, now=100.0)
        assert isinstance(e, DLQEntry)
        assert e.doc_id == "d1"
        assert e.operation == "op1"
        assert e.error == "boom"
        assert e.payload == {"a": 1}
        assert e.failed_at == 100.0
        assert e.attempts == 1
        assert e.retried_at is None
        assert e.resolved is False

    def test_id_increments(self):
        s = DocDLQStore()
        a = s.record_failure("d1", "op")
        b = s.record_failure("d1", "op")
        c = s.record_failure("d2", "op")
        assert a.entry_id == 1
        assert b.entry_id == 2
        assert c.entry_id == 3

    def test_attempts_starts_at_one(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        assert e.attempts == 1

    def test_payload_is_copied(self):
        s = DocDLQStore()
        original = {"k": 1}
        e = s.record_failure("d", "op", payload=original)
        original["k"] = 999
        assert e.payload == {"k": 1}

    def test_payload_none_yields_empty(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op", payload=None)
        assert e.payload == {}

    def test_default_now_uses_time(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        assert e.failed_at > 0


# --------------------------------------------------------------------- increment_attempt


class TestIncrementAttempt:
    def test_increments_and_records_retry(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op", now=10.0)
        ok = s.increment_attempt(e.entry_id, error="again", now=20.0)
        assert ok is True
        e2 = s.get(e.entry_id)
        assert e2.attempts == 2
        assert e2.error == "again"
        assert e2.retried_at == 20.0

    def test_multiple_increments(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        s.increment_attempt(e.entry_id)
        s.increment_attempt(e.entry_id)
        s.increment_attempt(e.entry_id)
        assert s.get(e.entry_id).attempts == 4

    def test_returns_false_for_missing(self):
        s = DocDLQStore()
        assert s.increment_attempt(999) is False

    def test_returns_false_for_resolved(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        s.resolve(e.entry_id)
        assert s.increment_attempt(e.entry_id) is False

    def test_default_now_uses_time(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        s.increment_attempt(e.entry_id)
        assert s.get(e.entry_id).retried_at is not None
        assert s.get(e.entry_id).retried_at > 0


# --------------------------------------------------------------------- resolve


class TestResolve:
    def test_true_when_found(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        assert s.resolve(e.entry_id) is True
        assert s.get(e.entry_id).resolved is True

    def test_false_when_missing(self):
        s = DocDLQStore()
        assert s.resolve(123) is False

    def test_idempotent(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        s.resolve(e.entry_id)
        assert s.resolve(e.entry_id) is True
        assert s.get(e.entry_id).resolved is True


# --------------------------------------------------------------------- unresolve


class TestUnresolve:
    def test_true_when_found(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        s.resolve(e.entry_id)
        assert s.unresolve(e.entry_id) is True
        assert s.get(e.entry_id).resolved is False

    def test_false_when_missing(self):
        s = DocDLQStore()
        assert s.unresolve(7) is False

    def test_idempotent_on_unresolved(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        assert s.unresolve(e.entry_id) is True
        assert s.get(e.entry_id).resolved is False


# --------------------------------------------------------------------- delete


class TestDelete:
    def test_removes_entry(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        assert s.delete(e.entry_id) is True
        assert s.get(e.entry_id) is None

    def test_returns_false_when_missing(self):
        s = DocDLQStore()
        assert s.delete(99) is False

    def test_removes_from_doc_index(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        s.delete(e.entry_id)
        assert s.entries_for_doc("d") == []

    def test_keeps_others(self):
        s = DocDLQStore()
        a = s.record_failure("d1", "op")
        b = s.record_failure("d1", "op")
        s.delete(a.entry_id)
        remaining = s.entries_for_doc("d1")
        assert len(remaining) == 1
        assert remaining[0].entry_id == b.entry_id


# --------------------------------------------------------------------- get


class TestGet:
    def test_returns_existing(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        assert s.get(e.entry_id) is e

    def test_missing_returns_none(self):
        s = DocDLQStore()
        assert s.get(42) is None


# --------------------------------------------------------------------- entries_for_doc


class TestEntriesForDoc:
    def test_sorted_desc_by_failed_at(self):
        s = DocDLQStore()
        s.record_failure("d", "op", now=10.0)
        s.record_failure("d", "op", now=30.0)
        s.record_failure("d", "op", now=20.0)
        ts = [e.failed_at for e in s.entries_for_doc("d")]
        assert ts == [30.0, 20.0, 10.0]

    def test_unresolved_only(self):
        s = DocDLQStore()
        a = s.record_failure("d", "op", now=10.0)
        s.record_failure("d", "op", now=20.0)
        s.resolve(a.entry_id)
        result = s.entries_for_doc("d", unresolved_only=True)
        assert len(result) == 1
        assert result[0].failed_at == 20.0

    def test_unknown_doc_empty(self):
        s = DocDLQStore()
        assert s.entries_for_doc("missing") == []

    def test_isolated_per_doc(self):
        s = DocDLQStore()
        s.record_failure("d1", "op")
        s.record_failure("d2", "op")
        assert len(s.entries_for_doc("d1")) == 1
        assert len(s.entries_for_doc("d2")) == 1


# --------------------------------------------------------------------- unresolved_entries


class TestUnresolvedEntries:
    def test_sorted_desc(self):
        s = DocDLQStore()
        s.record_failure("d", "op", now=10.0)
        s.record_failure("d", "op", now=30.0)
        s.record_failure("d", "op", now=20.0)
        ts = [e.failed_at for e in s.unresolved_entries()]
        assert ts == [30.0, 20.0, 10.0]

    def test_excludes_resolved(self):
        s = DocDLQStore()
        a = s.record_failure("d", "op", now=10.0)
        s.record_failure("d", "op", now=20.0)
        s.resolve(a.entry_id)
        result = s.unresolved_entries()
        assert len(result) == 1
        assert result[0].failed_at == 20.0

    def test_empty(self):
        s = DocDLQStore()
        assert s.unresolved_entries() == []


# --------------------------------------------------------------------- oldest_unresolved


class TestOldestUnresolved:
    def test_sorted_asc(self):
        s = DocDLQStore()
        s.record_failure("d", "op", now=30.0)
        s.record_failure("d", "op", now=10.0)
        s.record_failure("d", "op", now=20.0)
        ts = [e.failed_at for e in s.oldest_unresolved()]
        assert ts == [10.0, 20.0, 30.0]

    def test_respects_limit(self):
        s = DocDLQStore()
        for t in range(5):
            s.record_failure("d", "op", now=float(t))
        out = s.oldest_unresolved(limit=2)
        assert len(out) == 2
        assert [e.failed_at for e in out] == [0.0, 1.0]

    def test_excludes_resolved(self):
        s = DocDLQStore()
        a = s.record_failure("d", "op", now=1.0)
        s.record_failure("d", "op", now=2.0)
        s.resolve(a.entry_id)
        out = s.oldest_unresolved()
        assert [e.failed_at for e in out] == [2.0]

    def test_zero_limit(self):
        s = DocDLQStore()
        s.record_failure("d", "op")
        assert s.oldest_unresolved(limit=0) == []


# --------------------------------------------------------------------- most_failing_docs


class TestMostFailingDocs:
    def test_sorted_by_count_desc(self):
        s = DocDLQStore()
        s.record_failure("a", "op")
        s.record_failure("a", "op")
        s.record_failure("a", "op")
        s.record_failure("b", "op")
        s.record_failure("b", "op")
        s.record_failure("c", "op")
        assert s.most_failing_docs() == [("a", 3), ("b", 2), ("c", 1)]

    def test_ties_sorted_by_doc_id(self):
        s = DocDLQStore()
        s.record_failure("z", "op")
        s.record_failure("y", "op")
        s.record_failure("a", "op")
        assert s.most_failing_docs() == [("a", 1), ("y", 1), ("z", 1)]

    def test_limit(self):
        s = DocDLQStore()
        s.record_failure("a", "op")
        s.record_failure("b", "op")
        s.record_failure("c", "op")
        assert s.most_failing_docs(limit=2) == [("a", 1), ("b", 1)]

    def test_excludes_deleted(self):
        s = DocDLQStore()
        e = s.record_failure("a", "op")
        s.delete(e.entry_id)
        assert s.most_failing_docs() == []


# --------------------------------------------------------------------- resolve_all_for_doc


class TestResolveAllForDoc:
    def test_returns_count(self):
        s = DocDLQStore()
        s.record_failure("d", "op")
        s.record_failure("d", "op")
        s.record_failure("d", "op")
        assert s.resolve_all_for_doc("d") == 3

    def test_skips_already_resolved(self):
        s = DocDLQStore()
        a = s.record_failure("d", "op")
        s.record_failure("d", "op")
        s.resolve(a.entry_id)
        assert s.resolve_all_for_doc("d") == 1

    def test_unknown_doc_returns_zero(self):
        s = DocDLQStore()
        assert s.resolve_all_for_doc("missing") == 0

    def test_marks_resolved(self):
        s = DocDLQStore()
        s.record_failure("d", "op")
        s.record_failure("d", "op")
        s.resolve_all_for_doc("d")
        for e in s.entries_for_doc("d"):
            assert e.resolved is True


# --------------------------------------------------------------------- purge_resolved


class TestPurgeResolved:
    def test_returns_count(self):
        s = DocDLQStore()
        a = s.record_failure("d", "op")
        s.record_failure("d", "op")
        b = s.record_failure("d", "op")
        s.resolve(a.entry_id)
        s.resolve(b.entry_id)
        assert s.purge_resolved() == 2

    def test_keeps_unresolved(self):
        s = DocDLQStore()
        a = s.record_failure("d", "op")
        s.record_failure("d", "op")
        s.resolve(a.entry_id)
        s.purge_resolved()
        assert s.stats().total_entries == 1
        assert s.stats().unresolved_count == 1

    def test_cleans_doc_index(self):
        s = DocDLQStore()
        e = s.record_failure("d", "op")
        s.resolve(e.entry_id)
        s.purge_resolved()
        assert s.entries_for_doc("d") == []
        assert s.most_failing_docs() == []

    def test_empty_returns_zero(self):
        s = DocDLQStore()
        assert s.purge_resolved() == 0


# --------------------------------------------------------------------- stats


class TestStats:
    def test_empty(self):
        s = DocDLQStore()
        st = s.stats()
        assert st.total_entries == 0
        assert st.unresolved_count == 0
        assert st.unique_docs == 0
        assert st.total_attempts == 0

    def test_basic_totals(self):
        s = DocDLQStore()
        s.record_failure("d1", "op")
        s.record_failure("d1", "op")
        s.record_failure("d2", "op")
        st = s.stats()
        assert st.total_entries == 3
        assert st.unresolved_count == 3
        assert st.unique_docs == 2

    def test_attempts_accumulated(self):
        s = DocDLQStore()
        a = s.record_failure("d", "op")
        s.increment_attempt(a.entry_id)
        s.increment_attempt(a.entry_id)
        s.record_failure("d", "op")
        st = s.stats()
        assert st.total_attempts == 4  # 3 + 1

    def test_resolved_excluded_from_unresolved(self):
        s = DocDLQStore()
        a = s.record_failure("d", "op")
        s.record_failure("d", "op")
        s.resolve(a.entry_id)
        st = s.stats()
        assert st.total_entries == 2
        assert st.unresolved_count == 1


# --------------------------------------------------------------------- thread safety


class TestThreadSafety:
    def test_concurrent_record_failure(self):
        s = DocDLQStore()
        n_threads = 8
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                s.record_failure(f"doc-{tid}", "op", payload={"i": i})

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        st = s.stats()
        assert st.total_entries == n_threads * per_thread
        assert st.unique_docs == n_threads
        ids = {s.get(i).entry_id for i in range(1, st.total_entries + 1)}
        assert len(ids) == n_threads * per_thread

    def test_concurrent_mixed_ops(self):
        s = DocDLQStore()
        created: list = []
        lock = threading.Lock()

        def writer():
            for _ in range(50):
                e = s.record_failure("d", "op")
                with lock:
                    created.append(e.entry_id)

        def resolver():
            for _ in range(50):
                with lock:
                    snap = list(created)
                for eid in snap:
                    s.resolve(eid)

        t1 = threading.Thread(target=writer)
        t2 = threading.Thread(target=writer)
        t3 = threading.Thread(target=resolver)
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()

        assert s.stats().total_entries == 100


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
