"""Tests for E390 DocDiffRecorder."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_diff_recorder import (
    DiffRecord,
    DiffRecorderStats,
    DocDiffRecorder,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------

class TestDiffRecordDataclass:
    def test_defaults(self):
        r = DiffRecord()
        assert r.record_id == 0
        assert r.doc_id == ""
        assert r.author == ""
        assert r.recorded_at == 0.0
        assert r.added_lines == 0
        assert r.removed_lines == 0
        assert r.summary == ""

    def test_fields(self):
        r = DiffRecord(
            record_id=1,
            doc_id="d",
            author="a",
            recorded_at=10.5,
            added_lines=3,
            removed_lines=2,
            summary="s",
        )
        assert r.record_id == 1
        assert r.doc_id == "d"
        assert r.author == "a"
        assert r.recorded_at == 10.5
        assert r.added_lines == 3
        assert r.removed_lines == 2
        assert r.summary == "s"

    def test_equality(self):
        a = DiffRecord(record_id=1, doc_id="d")
        b = DiffRecord(record_id=1, doc_id="d")
        assert a == b

    def test_inequality(self):
        a = DiffRecord(record_id=1, doc_id="d")
        b = DiffRecord(record_id=2, doc_id="d")
        assert a != b


class TestDiffRecorderStatsDataclass:
    def test_defaults(self):
        s = DiffRecorderStats()
        assert s.total_records == 0
        assert s.unique_docs == 0
        assert s.unique_authors == 0
        assert s.total_added == 0
        assert s.total_removed == 0

    def test_fields(self):
        s = DiffRecorderStats(
            total_records=5,
            unique_docs=2,
            unique_authors=3,
            total_added=10,
            total_removed=4,
        )
        assert s.total_records == 5
        assert s.unique_docs == 2
        assert s.unique_authors == 3
        assert s.total_added == 10
        assert s.total_removed == 4

    def test_equality(self):
        a = DiffRecorderStats(total_records=1)
        b = DiffRecorderStats(total_records=1)
        assert a == b


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_default_construct(self):
        rec = DocDiffRecorder()
        assert rec.stats().total_records == 0

    def test_no_records_initially(self):
        rec = DocDiffRecorder()
        assert rec.records_for_doc("any") == []

    def test_no_authors_initially(self):
        rec = DocDiffRecorder()
        assert rec.records_by_author("a") == []

    def test_independent_instances(self):
        a = DocDiffRecorder()
        b = DocDiffRecorder()
        a.record_diff("d", 1, 1)
        assert a.stats().total_records == 1
        assert b.stats().total_records == 0


# ---------------------------------------------------------------------------
# record_diff
# ---------------------------------------------------------------------------

class TestRecordDiff:
    def test_returns_diff_record(self):
        rec = DocDiffRecorder()
        r = rec.record_diff("d", 2, 1)
        assert isinstance(r, DiffRecord)

    def test_id_starts_at_1(self):
        rec = DocDiffRecorder()
        r = rec.record_diff("d", 0, 0)
        assert r.record_id == 1

    def test_id_increments(self):
        rec = DocDiffRecorder()
        r1 = rec.record_diff("d", 1, 0)
        r2 = rec.record_diff("d", 0, 1)
        r3 = rec.record_diff("d", 0, 0)
        assert r1.record_id == 1
        assert r2.record_id == 2
        assert r3.record_id == 3

    def test_stores_fields(self):
        rec = DocDiffRecorder()
        r = rec.record_diff("doc1", 4, 2, author="alice", summary="msg")
        assert r.doc_id == "doc1"
        assert r.added_lines == 4
        assert r.removed_lines == 2
        assert r.author == "alice"
        assert r.summary == "msg"

    def test_negative_added_clamped(self):
        rec = DocDiffRecorder()
        r = rec.record_diff("d", -5, 3)
        assert r.added_lines == 0
        assert r.removed_lines == 3

    def test_negative_removed_clamped(self):
        rec = DocDiffRecorder()
        r = rec.record_diff("d", 5, -1)
        assert r.added_lines == 5
        assert r.removed_lines == 0

    def test_both_negative_clamped(self):
        rec = DocDiffRecorder()
        r = rec.record_diff("d", -2, -3)
        assert r.added_lines == 0
        assert r.removed_lines == 0

    def test_now_used(self):
        rec = DocDiffRecorder()
        r = rec.record_diff("d", 1, 1, now=1234.5)
        assert r.recorded_at == 1234.5

    def test_default_now_is_time(self):
        rec = DocDiffRecorder()
        before = time.time()
        r = rec.record_diff("d", 1, 1)
        after = time.time()
        assert before <= r.recorded_at <= after

    def test_records_added_to_index_by_doc(self):
        rec = DocDiffRecorder()
        rec.record_diff("d1", 1, 1)
        rec.record_diff("d2", 1, 1)
        rec.record_diff("d1", 0, 1)
        assert len(rec.records_for_doc("d1")) == 2
        assert len(rec.records_for_doc("d2")) == 1


# ---------------------------------------------------------------------------
# get_record
# ---------------------------------------------------------------------------

class TestGetRecord:
    def test_returns_record(self):
        rec = DocDiffRecorder()
        r = rec.record_diff("d", 1, 1)
        assert rec.get_record(r.record_id) == r

    def test_missing_returns_none(self):
        rec = DocDiffRecorder()
        assert rec.get_record(99) is None

    def test_zero_id_none(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1)
        assert rec.get_record(0) is None

    def test_negative_id_none(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1)
        assert rec.get_record(-1) is None


# ---------------------------------------------------------------------------
# records_for_doc
# ---------------------------------------------------------------------------

class TestRecordsForDoc:
    def test_empty(self):
        rec = DocDiffRecorder()
        assert rec.records_for_doc("d") == []

    def test_unknown_doc(self):
        rec = DocDiffRecorder()
        rec.record_diff("d1", 1, 1)
        assert rec.records_for_doc("d2") == []

    def test_most_recent_first(self):
        rec = DocDiffRecorder()
        r1 = rec.record_diff("d", 1, 0)
        r2 = rec.record_diff("d", 2, 0)
        r3 = rec.record_diff("d", 3, 0)
        result = rec.records_for_doc("d")
        assert [r.record_id for r in result] == [r3.record_id, r2.record_id, r1.record_id]

    def test_limit(self):
        rec = DocDiffRecorder()
        for i in range(5):
            rec.record_diff("d", i, 0)
        result = rec.records_for_doc("d", limit=2)
        assert len(result) == 2

    def test_limit_none_returns_all(self):
        rec = DocDiffRecorder()
        for i in range(3):
            rec.record_diff("d", i, 0)
        result = rec.records_for_doc("d", limit=None)
        assert len(result) == 3

    def test_filters_to_doc(self):
        rec = DocDiffRecorder()
        rec.record_diff("d1", 1, 0)
        rec.record_diff("d2", 1, 0)
        rec.record_diff("d1", 1, 0)
        result = rec.records_for_doc("d1")
        assert all(r.doc_id == "d1" for r in result)


# ---------------------------------------------------------------------------
# records_by_author
# ---------------------------------------------------------------------------

class TestRecordsByAuthor:
    def test_empty(self):
        rec = DocDiffRecorder()
        assert rec.records_by_author("a") == []

    def test_unknown_author(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1, author="alice")
        assert rec.records_by_author("bob") == []

    def test_most_recent_first(self):
        rec = DocDiffRecorder()
        r1 = rec.record_diff("d", 1, 0, author="a")
        r2 = rec.record_diff("d", 2, 0, author="a")
        r3 = rec.record_diff("d", 3, 0, author="a")
        result = rec.records_by_author("a")
        assert [r.record_id for r in result] == [r3.record_id, r2.record_id, r1.record_id]

    def test_limit(self):
        rec = DocDiffRecorder()
        for i in range(5):
            rec.record_diff("d", i, 0, author="a")
        assert len(rec.records_by_author("a", limit=3)) == 3

    def test_filters_to_author(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 0, author="alice")
        rec.record_diff("d", 1, 0, author="bob")
        rec.record_diff("d", 1, 0, author="alice")
        result = rec.records_by_author("alice")
        assert all(r.author == "alice" for r in result)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# records_in_range
# ---------------------------------------------------------------------------

class TestRecordsInRange:
    def test_empty(self):
        rec = DocDiffRecorder()
        assert rec.records_in_range(0, 100) == []

    def test_inclusive_bounds(self):
        rec = DocDiffRecorder()
        r1 = rec.record_diff("d", 1, 0, now=10.0)
        r2 = rec.record_diff("d", 1, 0, now=20.0)
        result = rec.records_in_range(10.0, 20.0)
        ids = {r.record_id for r in result}
        assert r1.record_id in ids
        assert r2.record_id in ids

    def test_excludes_outside(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 0, now=5.0)
        rec.record_diff("d", 1, 0, now=25.0)
        kept = rec.record_diff("d", 1, 0, now=15.0)
        result = rec.records_in_range(10.0, 20.0)
        assert len(result) == 1
        assert result[0].record_id == kept.record_id

    def test_sorted_asc(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 0, now=30.0)
        rec.record_diff("d", 1, 0, now=10.0)
        rec.record_diff("d", 1, 0, now=20.0)
        result = rec.records_in_range(0, 100)
        times = [r.recorded_at for r in result]
        assert times == sorted(times)

    def test_empty_range(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 0, now=5.0)
        assert rec.records_in_range(10, 20) == []


# ---------------------------------------------------------------------------
# total_lines_changed
# ---------------------------------------------------------------------------

class TestTotalLinesChanged:
    def test_no_records(self):
        rec = DocDiffRecorder()
        assert rec.total_lines_changed("d") == 0

    def test_single_record(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 3, 2)
        assert rec.total_lines_changed("d") == 5

    def test_multiple_records(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 3, 2)
        rec.record_diff("d", 1, 1)
        rec.record_diff("d", 4, 0)
        assert rec.total_lines_changed("d") == 11

    def test_other_doc_isolated(self):
        rec = DocDiffRecorder()
        rec.record_diff("d1", 3, 2)
        rec.record_diff("d2", 100, 100)
        assert rec.total_lines_changed("d1") == 5


# ---------------------------------------------------------------------------
# top_authors
# ---------------------------------------------------------------------------

class TestTopAuthors:
    def test_empty(self):
        rec = DocDiffRecorder()
        assert rec.top_authors() == []

    def test_sorted_desc(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 0, author="alice")
        rec.record_diff("d", 10, 5, author="bob")
        rec.record_diff("d", 2, 1, author="carol")
        result = rec.top_authors()
        authors = [a for a, _ in result]
        assert authors[0] == "bob"

    def test_excludes_empty_author(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 100, 100)  # empty author
        rec.record_diff("d", 1, 1, author="alice")
        result = rec.top_authors()
        authors = [a for a, _ in result]
        assert "" not in authors
        assert "alice" in authors

    def test_tie_breaker_author_asc(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1, author="bob")
        rec.record_diff("d", 1, 1, author="alice")
        result = rec.top_authors()
        assert result[0][0] == "alice"
        assert result[1][0] == "bob"

    def test_limit(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 0, author="a")
        rec.record_diff("d", 2, 0, author="b")
        rec.record_diff("d", 3, 0, author="c")
        result = rec.top_authors(limit=2)
        assert len(result) == 2

    def test_total_lines_correct(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 3, 2, author="alice")
        rec.record_diff("d", 1, 1, author="alice")
        result = rec.top_authors()
        assert result[0] == ("alice", 7)


# ---------------------------------------------------------------------------
# top_docs
# ---------------------------------------------------------------------------

class TestTopDocs:
    def test_empty(self):
        rec = DocDiffRecorder()
        assert rec.top_docs() == []

    def test_sorted_desc(self):
        rec = DocDiffRecorder()
        rec.record_diff("d1", 1, 0)
        rec.record_diff("d2", 10, 5)
        rec.record_diff("d3", 2, 1)
        result = rec.top_docs()
        assert result[0][0] == "d2"

    def test_totals(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 3, 2)
        rec.record_diff("d", 1, 1)
        result = rec.top_docs()
        assert result[0] == ("d", 7)

    def test_limit(self):
        rec = DocDiffRecorder()
        rec.record_diff("d1", 1, 0)
        rec.record_diff("d2", 2, 0)
        rec.record_diff("d3", 3, 0)
        result = rec.top_docs(limit=2)
        assert len(result) == 2

    def test_tie_breaker_doc_asc(self):
        rec = DocDiffRecorder()
        rec.record_diff("zeta", 1, 1)
        rec.record_diff("alpha", 1, 1)
        result = rec.top_docs()
        assert result[0][0] == "alpha"


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------

class TestClearDoc:
    def test_clear_unknown_returns_zero(self):
        rec = DocDiffRecorder()
        assert rec.clear_doc("nope") == 0

    def test_clear_returns_count(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1)
        rec.record_diff("d", 2, 2)
        rec.record_diff("d", 3, 3)
        assert rec.clear_doc("d") == 3

    def test_clear_removes_from_doc_index(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1)
        rec.clear_doc("d")
        assert rec.records_for_doc("d") == []

    def test_clear_removes_from_author_index(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1, author="alice")
        rec.clear_doc("d")
        assert rec.records_by_author("alice") == []

    def test_clear_preserves_other_docs(self):
        rec = DocDiffRecorder()
        rec.record_diff("d1", 1, 1)
        rec.record_diff("d2", 2, 2)
        rec.clear_doc("d1")
        assert len(rec.records_for_doc("d2")) == 1

    def test_clear_preserves_other_author_records(self):
        rec = DocDiffRecorder()
        rec.record_diff("d1", 1, 1, author="alice")
        rec.record_diff("d2", 1, 1, author="alice")
        rec.clear_doc("d1")
        assert len(rec.records_by_author("alice")) == 1


# ---------------------------------------------------------------------------
# clear_all
# ---------------------------------------------------------------------------

class TestClearAll:
    def test_empty_returns_zero(self):
        rec = DocDiffRecorder()
        assert rec.clear_all() == 0

    def test_returns_count(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1)
        rec.record_diff("d", 2, 2)
        assert rec.clear_all() == 2

    def test_empties_records(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1)
        rec.clear_all()
        assert rec.stats().total_records == 0

    def test_empties_indexes(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1, author="alice")
        rec.clear_all()
        assert rec.records_for_doc("d") == []
        assert rec.records_by_author("alice") == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty(self):
        rec = DocDiffRecorder()
        s = rec.stats()
        assert s.total_records == 0
        assert s.unique_docs == 0
        assert s.unique_authors == 0
        assert s.total_added == 0
        assert s.total_removed == 0

    def test_totals(self):
        rec = DocDiffRecorder()
        rec.record_diff("d1", 3, 2, author="alice")
        rec.record_diff("d2", 1, 1, author="bob")
        rec.record_diff("d1", 2, 1, author="alice")
        s = rec.stats()
        assert s.total_records == 3
        assert s.unique_docs == 2
        assert s.unique_authors == 2
        assert s.total_added == 6
        assert s.total_removed == 4

    def test_unique_docs_dedup(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1)
        rec.record_diff("d", 1, 1)
        rec.record_diff("d", 1, 1)
        assert rec.stats().unique_docs == 1

    def test_unique_authors_excludes_empty(self):
        rec = DocDiffRecorder()
        rec.record_diff("d", 1, 1)  # no author
        rec.record_diff("d", 1, 1, author="alice")
        rec.record_diff("d", 1, 1, author="bob")
        assert rec.stats().unique_authors == 2


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_record_diff(self):
        rec = DocDiffRecorder()
        N = 50
        T = 8

        def worker():
            for _ in range(N):
                rec.record_diff("d", 1, 1, author="a")

        threads = [threading.Thread(target=worker) for _ in range(T)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = rec.stats()
        assert s.total_records == N * T
        assert s.total_added == N * T
        assert s.total_removed == N * T

    def test_concurrent_ids_unique(self):
        rec = DocDiffRecorder()
        N = 100
        T = 4

        def worker():
            for _ in range(N):
                rec.record_diff("d", 0, 0)

        threads = [threading.Thread(target=worker) for _ in range(T)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        ids = [r.record_id for r in rec.records_for_doc("d")]
        assert len(ids) == len(set(ids))
        assert sorted(ids) == list(range(1, N * T + 1))
