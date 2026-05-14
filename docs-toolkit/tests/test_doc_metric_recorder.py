"""Tests for E333 DocMetricRecorder."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_metric_recorder import (
    DocMetricRecorder,
    MetricPoint,
    MetricStats,
    MetricSummary,
)


# --------------------------------------------------------------------- helpers


def _seed(rec: DocMetricRecorder) -> None:
    rec.record("a", "size", 10.0, now=100.0)
    rec.record("a", "size", 20.0, now=200.0)
    rec.record("a", "size", 30.0, now=300.0)
    rec.record("b", "size", 5.0, now=100.0)
    rec.record("b", "size", 15.0, now=200.0)
    rec.record("c", "size", 100.0, now=150.0)
    rec.record("a", "errors", 1.0, now=100.0)
    rec.record("b", "errors", 3.0, now=100.0)


# ============================================================ dataclass tests


class TestMetricPointDataclass:
    def test_basic_construction(self) -> None:
        p = MetricPoint(doc_id="d", metric="m", value=1.5, recorded_at=10.0)
        assert p.doc_id == "d"
        assert p.metric == "m"
        assert p.value == 1.5
        assert p.recorded_at == 10.0

    def test_default_tags(self) -> None:
        p = MetricPoint(doc_id="d", metric="m", value=0.0)
        assert p.tags == {}

    def test_default_recorded_at(self) -> None:
        p = MetricPoint(doc_id="d", metric="m", value=0.0)
        assert p.recorded_at == 0.0

    def test_separate_default_tags(self) -> None:
        p1 = MetricPoint(doc_id="a", metric="x", value=0.0)
        p2 = MetricPoint(doc_id="b", metric="x", value=0.0)
        p1.tags["k"] = 1
        assert p2.tags == {}

    def test_explicit_tags(self) -> None:
        p = MetricPoint(
            doc_id="d", metric="m", value=0.0, tags={"region": "eu"}
        )
        assert p.tags == {"region": "eu"}


class TestMetricSummaryDataclass:
    def test_basic_fields(self) -> None:
        s = MetricSummary(
            doc_id="d",
            metric="m",
            count=2,
            total=4.0,
            avg=2.0,
            min_value=1.0,
            max_value=3.0,
        )
        assert s.doc_id == "d"
        assert s.metric == "m"
        assert s.count == 2
        assert s.total == 4.0
        assert s.avg == 2.0
        assert s.min_value == 1.0
        assert s.max_value == 3.0

    def test_equality(self) -> None:
        a = MetricSummary("d", "m", 1, 1.0, 1.0, 1.0, 1.0)
        b = MetricSummary("d", "m", 1, 1.0, 1.0, 1.0, 1.0)
        assert a == b


class TestMetricStatsDataclass:
    def test_basic_fields(self) -> None:
        s = MetricStats(total_points=10, unique_docs=3, unique_metrics=2)
        assert s.total_points == 10
        assert s.unique_docs == 3
        assert s.unique_metrics == 2

    def test_equality(self) -> None:
        assert MetricStats(0, 0, 0) == MetricStats(0, 0, 0)


# =============================================================== construction


class TestConstruction:
    def test_default_state_empty(self) -> None:
        rec = DocMetricRecorder()
        s = rec.stats()
        assert s.total_points == 0
        assert s.unique_docs == 0
        assert s.unique_metrics == 0

    def test_no_points_no_docs(self) -> None:
        rec = DocMetricRecorder()
        assert rec.all_doc_ids() == []

    def test_summary_empty(self) -> None:
        rec = DocMetricRecorder()
        assert rec.summary("x", "y") is None


# ======================================================================= record


class TestRecord:
    def test_record_returns_point(self) -> None:
        rec = DocMetricRecorder()
        p = rec.record("d", "m", 1.0, now=42.0)
        assert isinstance(p, MetricPoint)
        assert p.doc_id == "d"
        assert p.metric == "m"
        assert p.value == 1.0
        assert p.recorded_at == 42.0

    def test_record_stores_tags(self) -> None:
        rec = DocMetricRecorder()
        p = rec.record("d", "m", 1.0, tags={"k": "v"}, now=0.0)
        assert p.tags == {"k": "v"}

    def test_record_tags_defensive_copy(self) -> None:
        rec = DocMetricRecorder()
        tags = {"k": "v"}
        p = rec.record("d", "m", 1.0, tags=tags, now=0.0)
        tags["k"] = "mutated"
        assert p.tags == {"k": "v"}

    def test_record_none_tags(self) -> None:
        rec = DocMetricRecorder()
        p = rec.record("d", "m", 1.0, tags=None, now=0.0)
        assert p.tags == {}

    def test_record_timestamp_default_now(self) -> None:
        rec = DocMetricRecorder()
        p = rec.record("d", "m", 1.0)
        assert p.recorded_at > 0.0

    def test_record_value_cast_to_float(self) -> None:
        rec = DocMetricRecorder()
        p = rec.record("d", "m", 7, now=0.0)
        assert isinstance(p.value, float)
        assert p.value == 7.0

    def test_record_multiple_indexed(self) -> None:
        rec = DocMetricRecorder()
        rec.record("d", "m", 1.0, now=0.0)
        rec.record("d", "m", 2.0, now=1.0)
        rec.record("d", "n", 5.0, now=2.0)
        s = rec.stats()
        assert s.total_points == 3
        assert s.unique_docs == 1
        assert s.unique_metrics == 2


# ====================================================================== summary


class TestSummary:
    def test_summary_basic(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        s = rec.summary("a", "size")
        assert s is not None
        assert s.count == 3
        assert s.total == 60.0
        assert s.avg == 20.0
        assert s.min_value == 10.0
        assert s.max_value == 30.0

    def test_summary_doc_id_metric_fields(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        s = rec.summary("b", "size")
        assert s.doc_id == "b"
        assert s.metric == "size"

    def test_summary_single_point(self) -> None:
        rec = DocMetricRecorder()
        rec.record("a", "x", 7.0, now=0.0)
        s = rec.summary("a", "x")
        assert s.count == 1
        assert s.total == 7.0
        assert s.avg == 7.0
        assert s.min_value == 7.0
        assert s.max_value == 7.0

    def test_summary_none_when_missing(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        assert rec.summary("zzz", "size") is None
        assert rec.summary("a", "nope") is None


# ====================================================================== points


class TestPoints:
    def test_points_most_recent_first(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        pts = rec.points("a", "size")
        assert [p.recorded_at for p in pts] == [300.0, 200.0, 100.0]

    def test_points_empty(self) -> None:
        rec = DocMetricRecorder()
        assert rec.points("d", "m") == []

    def test_points_limit(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        pts = rec.points("a", "size", limit=2)
        assert len(pts) == 2
        assert pts[0].recorded_at == 300.0
        assert pts[1].recorded_at == 200.0

    def test_points_limit_zero(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        assert rec.points("a", "size", limit=0) == []

    def test_points_negative_limit_raises(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        with pytest.raises(ValueError):
            rec.points("a", "size", limit=-1)


# ============================================================== points_in_range


class TestPointsInRange:
    def test_inclusive_bounds(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        pts = rec.points_in_range("a", "size", 100.0, 200.0)
        assert [p.recorded_at for p in pts] == [100.0, 200.0]

    def test_ascending_sort(self) -> None:
        rec = DocMetricRecorder()
        rec.record("a", "m", 1.0, now=300.0)
        rec.record("a", "m", 2.0, now=100.0)
        rec.record("a", "m", 3.0, now=200.0)
        pts = rec.points_in_range("a", "m", 0.0, 500.0)
        assert [p.recorded_at for p in pts] == [100.0, 200.0, 300.0]

    def test_empty_range(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        assert rec.points_in_range("a", "size", 500.0, 600.0) == []

    def test_no_points_for_key(self) -> None:
        rec = DocMetricRecorder()
        assert rec.points_in_range("x", "y", 0.0, 100.0) == []

    def test_invalid_range_raises(self) -> None:
        rec = DocMetricRecorder()
        with pytest.raises(ValueError):
            rec.points_in_range("a", "m", 10.0, 5.0)


# ============================================================ top_docs_by_total


class TestTopDocsByTotal:
    def test_sorted_desc(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        top = rec.top_docs_by_total("size")
        # a -> 60, b -> 20, c -> 100
        assert top == [("c", 100.0), ("a", 60.0), ("b", 20.0)]

    def test_limit(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        top = rec.top_docs_by_total("size", limit=2)
        assert len(top) == 2
        assert top[0] == ("c", 100.0)

    def test_tie_break_by_doc_id_asc(self) -> None:
        rec = DocMetricRecorder()
        rec.record("zeta", "m", 5.0, now=0.0)
        rec.record("alpha", "m", 5.0, now=0.0)
        rec.record("mu", "m", 5.0, now=0.0)
        top = rec.top_docs_by_total("m")
        assert top == [("alpha", 5.0), ("mu", 5.0), ("zeta", 5.0)]

    def test_unknown_metric(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        assert rec.top_docs_by_total("nope") == []

    def test_negative_limit_raises(self) -> None:
        rec = DocMetricRecorder()
        with pytest.raises(ValueError):
            rec.top_docs_by_total("m", limit=-1)


# ============================================================== top_docs_by_avg


class TestTopDocsByAvg:
    def test_sorted_desc(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        top = rec.top_docs_by_avg("size")
        # a avg=20, b avg=10, c avg=100
        assert top == [("c", 100.0), ("a", 20.0), ("b", 10.0)]

    def test_limit(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        assert rec.top_docs_by_avg("size", limit=1) == [("c", 100.0)]

    def test_tie_break_by_doc_id_asc(self) -> None:
        rec = DocMetricRecorder()
        rec.record("zeta", "m", 4.0, now=0.0)
        rec.record("zeta", "m", 6.0, now=0.0)
        rec.record("alpha", "m", 5.0, now=0.0)
        top = rec.top_docs_by_avg("m")
        assert top == [("alpha", 5.0), ("zeta", 5.0)]

    def test_unknown_metric(self) -> None:
        rec = DocMetricRecorder()
        assert rec.top_docs_by_avg("nope") == []

    def test_negative_limit_raises(self) -> None:
        rec = DocMetricRecorder()
        with pytest.raises(ValueError):
            rec.top_docs_by_avg("m", limit=-2)


# ============================================================= metrics_for_doc


class TestMetricsForDoc:
    def test_sorted_unique(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        assert rec.metrics_for_doc("a") == ["errors", "size"]

    def test_no_metrics(self) -> None:
        rec = DocMetricRecorder()
        assert rec.metrics_for_doc("nobody") == []

    def test_duplicates_collapsed(self) -> None:
        rec = DocMetricRecorder()
        rec.record("a", "m1", 1.0, now=0.0)
        rec.record("a", "m1", 2.0, now=0.0)
        rec.record("a", "m2", 3.0, now=0.0)
        assert rec.metrics_for_doc("a") == ["m1", "m2"]


# ============================================================= docs_for_metric


class TestDocsForMetric:
    def test_sorted_unique(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        assert rec.docs_for_metric("size") == ["a", "b", "c"]

    def test_unknown_metric(self) -> None:
        rec = DocMetricRecorder()
        assert rec.docs_for_metric("nope") == []

    def test_unique_collapsed(self) -> None:
        rec = DocMetricRecorder()
        rec.record("a", "m", 1.0, now=0.0)
        rec.record("a", "m", 2.0, now=0.0)
        assert rec.docs_for_metric("m") == ["a"]


# =================================================================== clear_doc


class TestClearDoc:
    def test_returns_count(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        removed = rec.clear_doc("a")
        # 3 size + 1 errors = 4
        assert removed == 4

    def test_removed_from_index(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        rec.clear_doc("a")
        assert rec.summary("a", "size") is None
        assert rec.summary("a", "errors") is None
        assert "a" not in rec.all_doc_ids()

    def test_missing_doc_returns_zero(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        assert rec.clear_doc("ghost") == 0


# ================================================================ clear_metric


class TestClearMetric:
    def test_returns_count(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        removed = rec.clear_metric("size")
        # a:3 + b:2 + c:1
        assert removed == 6

    def test_removed_from_index(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        rec.clear_metric("size")
        assert rec.docs_for_metric("size") == []
        # errors metric still present
        assert rec.docs_for_metric("errors") == ["a", "b"]

    def test_missing_metric_returns_zero(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        assert rec.clear_metric("ghost") == 0


# ================================================================= all_doc_ids


class TestAllDocIds:
    def test_sorted(self) -> None:
        rec = DocMetricRecorder()
        rec.record("zeta", "m", 0.0, now=0.0)
        rec.record("alpha", "m", 0.0, now=0.0)
        rec.record("mu", "m", 0.0, now=0.0)
        assert rec.all_doc_ids() == ["alpha", "mu", "zeta"]

    def test_unique(self) -> None:
        rec = DocMetricRecorder()
        rec.record("a", "m1", 0.0, now=0.0)
        rec.record("a", "m2", 0.0, now=0.0)
        assert rec.all_doc_ids() == ["a"]

    def test_empty(self) -> None:
        rec = DocMetricRecorder()
        assert rec.all_doc_ids() == []


# ======================================================================= stats


class TestStats:
    def test_totals(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        s = rec.stats()
        assert s.total_points == 8
        assert s.unique_docs == 3
        assert s.unique_metrics == 2

    def test_empty(self) -> None:
        rec = DocMetricRecorder()
        s = rec.stats()
        assert s == MetricStats(total_points=0, unique_docs=0, unique_metrics=0)

    def test_after_clear_doc(self) -> None:
        rec = DocMetricRecorder()
        _seed(rec)
        rec.clear_doc("a")
        s = rec.stats()
        assert s.total_points == 4  # b:size 2 + c:size 1 + b:errors 1
        assert s.unique_docs == 2
        assert s.unique_metrics == 2


# ================================================================ thread safety


class TestThreadSafety:
    def test_concurrent_record(self) -> None:
        rec = DocMetricRecorder()
        n_threads = 8
        per_thread = 200

        def worker(tid: int) -> None:
            for i in range(per_thread):
                rec.record(f"doc{tid}", "m", float(i), now=float(i))

        threads = [
            threading.Thread(target=worker, args=(tid,))
            for tid in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = rec.stats()
        assert s.total_points == n_threads * per_thread
        assert s.unique_docs == n_threads
        assert s.unique_metrics == 1
        # each doc has per_thread points
        for tid in range(n_threads):
            summary = rec.summary(f"doc{tid}", "m")
            assert summary is not None
            assert summary.count == per_thread

    def test_concurrent_record_and_query(self) -> None:
        rec = DocMetricRecorder()
        stop = threading.Event()

        def writer() -> None:
            i = 0
            while not stop.is_set():
                rec.record("d", "m", float(i), now=float(i))
                i += 1

        def reader() -> None:
            while not stop.is_set():
                rec.summary("d", "m")
                rec.stats()
                rec.points("d", "m", limit=10)

        ws = [threading.Thread(target=writer) for _ in range(2)]
        rs = [threading.Thread(target=reader) for _ in range(2)]
        for t in ws + rs:
            t.start()
        # let it run briefly then stop
        import time as _t
        _t.sleep(0.05)
        stop.set()
        for t in ws + rs:
            t.join()

        s = rec.stats()
        assert s.total_points > 0
        assert s.unique_docs == 1
