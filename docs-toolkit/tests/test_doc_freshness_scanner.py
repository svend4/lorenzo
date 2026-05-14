"""Tests for E370 DocFreshnessScanner."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_freshness_scanner import (
    DocFreshnessScanner,
    FreshnessRecord,
    FreshnessStats,
    StaleDoc,
)


# ---------------------------------------------------------------------------
class TestFreshnessRecordDataclass:
    def test_basic(self):
        r = FreshnessRecord(doc_id="d", last_modified=1.0)
        assert r.doc_id == "d"
        assert r.last_modified == 1.0
        assert r.last_reviewed is None
        assert r.expected_review_interval == 0.0

    def test_full(self):
        r = FreshnessRecord(
            doc_id="d", last_modified=1.0, last_reviewed=2.0, expected_review_interval=10.0
        )
        assert r.last_reviewed == 2.0
        assert r.expected_review_interval == 10.0

    def test_equality(self):
        a = FreshnessRecord("d", 1.0)
        b = FreshnessRecord("d", 1.0)
        assert a == b

    def test_inequality(self):
        a = FreshnessRecord("d", 1.0)
        b = FreshnessRecord("d", 2.0)
        assert a != b


class TestStaleDocDataclass:
    def test_basic(self):
        s = StaleDoc(doc_id="d", staleness_seconds=10.0, overdue_review=False, reason="x")
        assert s.doc_id == "d"
        assert s.staleness_seconds == 10.0
        assert s.overdue_review is False
        assert s.reason == "x"

    def test_equality(self):
        a = StaleDoc("d", 1.0, True, "r")
        b = StaleDoc("d", 1.0, True, "r")
        assert a == b

    def test_reason_field(self):
        s = StaleDoc("d", 1.0, False, "because")
        assert "because" in s.reason


class TestFreshnessStatsDataclass:
    def test_basic(self):
        st = FreshnessStats(total_records=5, stale_count=2, overdue_review_count=1, avg_age_seconds=100.0)
        assert st.total_records == 5
        assert st.stale_count == 2
        assert st.overdue_review_count == 1
        assert st.avg_age_seconds == 100.0

    def test_zero(self):
        st = FreshnessStats(0, 0, 0, 0.0)
        assert st.total_records == 0


class TestConstruction:
    def test_default_empty(self):
        s = DocFreshnessScanner()
        assert s.stats().total_records == 0

    def test_independent_instances(self):
        a = DocFreshnessScanner()
        b = DocFreshnessScanner()
        a.record("d", 1.0)
        assert b.get("d") is None


class TestRecord:
    def test_new(self):
        s = DocFreshnessScanner()
        rec = s.record("d", 1.0)
        assert rec.doc_id == "d"
        assert rec.last_modified == 1.0

    def test_returns_record(self):
        s = DocFreshnessScanner()
        rec = s.record("d", 1.0, expected_review_interval=5.0)
        assert isinstance(rec, FreshnessRecord)
        assert rec.expected_review_interval == 5.0

    def test_replace(self):
        s = DocFreshnessScanner()
        s.record("d", 1.0)
        s.record("d", 2.0)
        assert s.get("d").last_modified == 2.0

    def test_with_last_reviewed(self):
        s = DocFreshnessScanner()
        rec = s.record("d", 1.0, last_reviewed=0.5)
        assert rec.last_reviewed == 0.5

    def test_multiple(self):
        s = DocFreshnessScanner()
        s.record("a", 1.0)
        s.record("b", 2.0)
        assert s.stats().total_records == 2


class TestUpdateModified:
    def test_true_when_found(self):
        s = DocFreshnessScanner()
        s.record("d", 1.0)
        assert s.update_modified("d", 5.0) is True
        assert s.get("d").last_modified == 5.0

    def test_false_when_missing(self):
        s = DocFreshnessScanner()
        assert s.update_modified("nope", 5.0) is False

    def test_preserves_other_fields(self):
        s = DocFreshnessScanner()
        s.record("d", 1.0, expected_review_interval=10.0, last_reviewed=0.5)
        s.update_modified("d", 5.0)
        rec = s.get("d")
        assert rec.expected_review_interval == 10.0
        assert rec.last_reviewed == 0.5


class TestUpdateReviewed:
    def test_true_when_found(self):
        s = DocFreshnessScanner()
        s.record("d", 1.0)
        assert s.update_reviewed("d", 9.0) is True
        assert s.get("d").last_reviewed == 9.0

    def test_false_when_missing(self):
        s = DocFreshnessScanner()
        assert s.update_reviewed("nope", 9.0) is False

    def test_overwrites(self):
        s = DocFreshnessScanner()
        s.record("d", 1.0, last_reviewed=0.5)
        s.update_reviewed("d", 9.0)
        assert s.get("d").last_reviewed == 9.0


class TestRemove:
    def test_true_when_found(self):
        s = DocFreshnessScanner()
        s.record("d", 1.0)
        assert s.remove("d") is True
        assert s.get("d") is None

    def test_false_when_missing(self):
        s = DocFreshnessScanner()
        assert s.remove("d") is False

    def test_idempotent(self):
        s = DocFreshnessScanner()
        s.record("d", 1.0)
        s.remove("d")
        assert s.remove("d") is False


class TestGet:
    def test_found(self):
        s = DocFreshnessScanner()
        s.record("d", 1.0)
        rec = s.get("d")
        assert rec is not None and rec.doc_id == "d"

    def test_not_found(self):
        s = DocFreshnessScanner()
        assert s.get("missing") is None


class TestFindStale:
    def test_threshold_filters(self):
        s = DocFreshnessScanner()
        s.record("fresh", 95.0)
        s.record("stale", 10.0)
        out = s.find_stale(older_than_seconds=50.0, now=100.0)
        ids = [d.doc_id for d in out]
        assert ids == ["stale"]

    def test_sorted_desc(self):
        s = DocFreshnessScanner()
        s.record("a", 90.0)  # age 10
        s.record("b", 0.0)   # age 100
        s.record("c", 50.0)  # age 50
        out = s.find_stale(older_than_seconds=0.0, now=100.0)
        assert [d.doc_id for d in out] == ["b", "c", "a"]

    def test_inclusive_boundary(self):
        s = DocFreshnessScanner()
        s.record("d", 50.0)  # age exactly 50
        out = s.find_stale(older_than_seconds=50.0, now=100.0)
        assert len(out) == 1

    def test_empty(self):
        s = DocFreshnessScanner()
        assert s.find_stale(older_than_seconds=10.0, now=100.0) == []

    def test_overdue_flag(self):
        s = DocFreshnessScanner()
        s.record("d", 0.0, expected_review_interval=10.0, last_reviewed=None)
        out = s.find_stale(older_than_seconds=10.0, now=100.0)
        assert out[0].overdue_review is True

    def test_reason_populated(self):
        s = DocFreshnessScanner()
        s.record("d", 10.0)
        out = s.find_stale(older_than_seconds=10.0, now=100.0)
        assert out[0].reason


class TestFindOverdueReviews:
    def test_never_reviewed_counts(self):
        s = DocFreshnessScanner()
        s.record("d", 0.0, expected_review_interval=10.0)
        out = s.find_overdue_reviews(now=100.0)
        assert len(out) == 1 and out[0].overdue_review is True

    def test_no_interval_skipped(self):
        s = DocFreshnessScanner()
        s.record("d", 0.0)  # interval 0 → not scheduled
        out = s.find_overdue_reviews(now=100.0)
        assert out == []

    def test_reviewed_within_interval(self):
        s = DocFreshnessScanner()
        s.record("d", 0.0, expected_review_interval=50.0, last_reviewed=90.0)
        # 90 + 50 = 140 > 100 → not overdue
        out = s.find_overdue_reviews(now=100.0)
        assert out == []

    def test_reviewed_but_overdue(self):
        s = DocFreshnessScanner()
        s.record("d", 0.0, expected_review_interval=10.0, last_reviewed=20.0)
        # 20 + 10 = 30 < 100 → overdue
        out = s.find_overdue_reviews(now=100.0)
        assert len(out) == 1

    def test_sorted_by_doc_id(self):
        s = DocFreshnessScanner()
        s.record("c", 0.0, expected_review_interval=10.0)
        s.record("a", 0.0, expected_review_interval=10.0)
        s.record("b", 0.0, expected_review_interval=10.0)
        out = s.find_overdue_reviews(now=100.0)
        assert [d.doc_id for d in out] == ["a", "b", "c"]

    def test_reason_for_never_reviewed(self):
        s = DocFreshnessScanner()
        s.record("d", 0.0, expected_review_interval=10.0)
        out = s.find_overdue_reviews(now=100.0)
        assert "never" in out[0].reason


class TestFreshestDocs:
    def test_sorted_asc(self):
        s = DocFreshnessScanner()
        s.record("a", 0.0)   # age 100
        s.record("b", 90.0)  # age 10
        s.record("c", 50.0)  # age 50
        out = s.freshest_docs(now=100.0)
        assert [doc_id for doc_id, _ in out] == ["b", "c", "a"]

    def test_limit(self):
        s = DocFreshnessScanner()
        for i in range(5):
            s.record(f"d{i}", float(i))
        out = s.freshest_docs(limit=2, now=100.0)
        assert len(out) == 2

    def test_empty(self):
        s = DocFreshnessScanner()
        assert s.freshest_docs(now=100.0) == []

    def test_age_value(self):
        s = DocFreshnessScanner()
        s.record("d", 80.0)
        out = s.freshest_docs(now=100.0)
        assert out[0][1] == 20.0


class TestStalestDocs:
    def test_sorted_desc(self):
        s = DocFreshnessScanner()
        s.record("a", 90.0)
        s.record("b", 0.0)
        s.record("c", 50.0)
        out = s.stalest_docs(now=100.0)
        assert [doc_id for doc_id, _ in out] == ["b", "c", "a"]

    def test_limit(self):
        s = DocFreshnessScanner()
        for i in range(5):
            s.record(f"d{i}", float(i))
        out = s.stalest_docs(limit=3, now=100.0)
        assert len(out) == 3

    def test_empty(self):
        s = DocFreshnessScanner()
        assert s.stalest_docs(now=100.0) == []

    def test_age_value(self):
        s = DocFreshnessScanner()
        s.record("d", 20.0)
        out = s.stalest_docs(now=100.0)
        assert out[0][1] == 80.0


class TestClear:
    def test_count(self):
        s = DocFreshnessScanner()
        s.record("a", 1.0)
        s.record("b", 2.0)
        s.record("c", 3.0)
        assert s.clear() == 3
        assert s.stats().total_records == 0

    def test_empty(self):
        s = DocFreshnessScanner()
        assert s.clear() == 0


class TestStats:
    def test_totals(self):
        s = DocFreshnessScanner()
        s.record("a", 0.0)
        s.record("b", 50.0)
        s.record("c", 95.0)
        st = s.stats(stale_threshold=40.0, now=100.0)
        assert st.total_records == 3
        # ages: 100, 50, 5 → 100>=40 and 50>=40 → 2 stale
        assert st.stale_count == 2

    def test_avg_age(self):
        s = DocFreshnessScanner()
        s.record("a", 90.0)  # age 10
        s.record("b", 80.0)  # age 20
        st = s.stats(now=100.0)
        assert st.avg_age_seconds == 15.0

    def test_overdue_count(self):
        s = DocFreshnessScanner()
        s.record("a", 0.0, expected_review_interval=10.0)  # overdue
        s.record("b", 0.0, expected_review_interval=10.0, last_reviewed=99.0)  # not overdue
        st = s.stats(now=100.0)
        assert st.overdue_review_count == 1

    def test_empty(self):
        s = DocFreshnessScanner()
        st = s.stats(now=100.0)
        assert st.total_records == 0
        assert st.avg_age_seconds == 0.0
        assert st.stale_count == 0
        assert st.overdue_review_count == 0

    def test_default_threshold(self):
        s = DocFreshnessScanner()
        s.record("d", 0.0)
        # default threshold is 30 days; age is 100 → not stale
        st = s.stats(now=100.0)
        assert st.stale_count == 0


class TestThreadSafety:
    def test_concurrent_record(self):
        s = DocFreshnessScanner()

        def worker(start):
            for i in range(50):
                s.record(f"d{start}_{i}", float(i))

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert s.stats().total_records == 8 * 50

    def test_concurrent_mixed_ops(self):
        s = DocFreshnessScanner()
        for i in range(100):
            s.record(f"d{i}", float(i))

        def updater():
            for i in range(100):
                s.update_modified(f"d{i}", float(i + 1000))

        def reader():
            for i in range(100):
                s.get(f"d{i}")

        threads = [
            threading.Thread(target=updater),
            threading.Thread(target=updater),
            threading.Thread(target=reader),
            threading.Thread(target=reader),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert s.stats().total_records == 100

    def test_concurrent_remove(self):
        s = DocFreshnessScanner()
        for i in range(200):
            s.record(f"d{i}", 0.0)

        def remover(start, stop):
            for i in range(start, stop):
                s.remove(f"d{i}")

        threads = [
            threading.Thread(target=remover, args=(0, 100)),
            threading.Thread(target=remover, args=(100, 200)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert s.stats().total_records == 0
