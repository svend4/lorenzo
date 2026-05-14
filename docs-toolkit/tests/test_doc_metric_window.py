"""Tests for E437 DocMetricWindow."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_metric_window import (
    DocMetricWindow,
    MetricStats,
    WindowPoint,
    WindowStats,
)


# ---------------------------------------------------------------- construction


def test_empty_construction():
    w = DocMetricWindow()
    assert w.stats() == MetricStats(total_points=0, unique_metrics=0, unique_docs=0)


def test_empty_all_doc_ids():
    assert DocMetricWindow().all_doc_ids() == []


def test_empty_metrics_for_doc():
    assert DocMetricWindow().metrics_for_doc("any") == []


def test_empty_docs_for_metric():
    assert DocMetricWindow().docs_for_metric("any") == []


def test_empty_window_stats():
    assert DocMetricWindow().window_stats("d", "m", 60.0, now=100.0) is None


def test_empty_recent_points():
    assert DocMetricWindow().recent_points("d", "m", 60.0, now=100.0) == []


def test_empty_rolling_average():
    assert DocMetricWindow().rolling_average("d", "m", 60.0, now=100.0) is None


def test_empty_rolling_sum():
    assert DocMetricWindow().rolling_sum("d", "m", 60.0, now=100.0) is None


# --------------------------------------------------------------------- record


def test_record_returns_window_point():
    w = DocMetricWindow()
    p = w.record("doc1", "latency", 1.5, timestamp=100.0)
    assert isinstance(p, WindowPoint)
    assert p.doc_id == "doc1"
    assert p.metric == "latency"
    assert p.value == 1.5
    assert p.timestamp == 100.0


def test_record_default_timestamp_uses_time():
    w = DocMetricWindow()
    before = time.time()
    p = w.record("doc1", "m", 1.0)
    after = time.time()
    assert before <= p.timestamp <= after


def test_record_coerces_value_to_float():
    w = DocMetricWindow()
    p = w.record("doc1", "m", 3, timestamp=1.0)
    assert isinstance(p.value, float)
    assert p.value == 3.0


def test_record_coerces_timestamp_to_float():
    w = DocMetricWindow()
    p = w.record("doc1", "m", 1.0, timestamp=5)
    assert isinstance(p.timestamp, float)
    assert p.timestamp == 5.0


def test_record_updates_stats():
    w = DocMetricWindow()
    w.record("d1", "m1", 1.0, timestamp=1.0)
    w.record("d1", "m2", 2.0, timestamp=2.0)
    w.record("d2", "m1", 3.0, timestamp=3.0)
    s = w.stats()
    assert s.total_points == 3
    assert s.unique_metrics == 2
    assert s.unique_docs == 2


def test_record_appends_to_internal_list():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=1.0)
    w.record("d", "m", 2.0, timestamp=2.0)
    assert len(w._points) == 2


def test_record_updates_secondary_index():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=1.0)
    w.record("d", "m", 2.0, timestamp=2.0)
    assert w._by_key[("d", "m")] == [0, 1]


# ---------------------------------------------------------------- window_stats


def test_window_stats_includes_all_points():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=100.0)
    w.record("d", "m", 2.0, timestamp=110.0)
    w.record("d", "m", 3.0, timestamp=120.0)
    s = w.window_stats("d", "m", 30.0, now=120.0)
    assert s == WindowStats(count=3, sum=6.0, avg=2.0, min_value=1.0, max_value=3.0)


def test_window_stats_excludes_old_points():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=50.0)
    w.record("d", "m", 2.0, timestamp=110.0)
    w.record("d", "m", 3.0, timestamp=120.0)
    s = w.window_stats("d", "m", 30.0, now=120.0)
    assert s is not None
    assert s.count == 2
    assert s.sum == 5.0


def test_window_stats_excludes_future_points():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=100.0)
    w.record("d", "m", 99.0, timestamp=200.0)
    s = w.window_stats("d", "m", 50.0, now=100.0)
    assert s is not None
    assert s.count == 1
    assert s.sum == 1.0


def test_window_stats_none_outside_window():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=10.0)
    assert w.window_stats("d", "m", 5.0, now=100.0) is None


def test_window_stats_isolates_by_doc():
    w = DocMetricWindow()
    w.record("d1", "m", 1.0, timestamp=10.0)
    w.record("d2", "m", 99.0, timestamp=10.0)
    s = w.window_stats("d1", "m", 60.0, now=20.0)
    assert s.count == 1
    assert s.sum == 1.0


def test_window_stats_isolates_by_metric():
    w = DocMetricWindow()
    w.record("d", "m1", 1.0, timestamp=10.0)
    w.record("d", "m2", 99.0, timestamp=10.0)
    s = w.window_stats("d", "m1", 60.0, now=20.0)
    assert s.count == 1
    assert s.sum == 1.0


def test_window_stats_inclusive_boundary_old():
    w = DocMetricWindow()
    # exactly now - window_seconds should be included
    w.record("d", "m", 1.0, timestamp=70.0)
    s = w.window_stats("d", "m", 30.0, now=100.0)
    assert s is not None
    assert s.count == 1


def test_window_stats_inclusive_boundary_now():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=100.0)
    s = w.window_stats("d", "m", 30.0, now=100.0)
    assert s is not None
    assert s.count == 1


def test_window_stats_min_max():
    w = DocMetricWindow()
    for v, ts in [(10.0, 1.0), (5.0, 2.0), (7.0, 3.0), (12.0, 4.0)]:
        w.record("d", "m", v, timestamp=ts)
    s = w.window_stats("d", "m", 10.0, now=5.0)
    assert s.min_value == 5.0
    assert s.max_value == 12.0


def test_window_stats_single_point():
    w = DocMetricWindow()
    w.record("d", "m", 4.0, timestamp=100.0)
    s = w.window_stats("d", "m", 10.0, now=100.0)
    assert s == WindowStats(count=1, sum=4.0, avg=4.0, min_value=4.0, max_value=4.0)


def test_window_stats_default_now_uses_time(monkeypatch):
    w = DocMetricWindow()
    fixed = 5000.0
    monkeypatch.setattr(time, "time", lambda: fixed)
    w.record("d", "m", 1.0, timestamp=fixed - 1.0)
    s = w.window_stats("d", "m", 10.0)
    assert s is not None
    assert s.count == 1


# --------------------------------------------------------------- recent_points


def test_recent_points_sorted_ascending():
    w = DocMetricWindow()
    w.record("d", "m", 3.0, timestamp=30.0)
    w.record("d", "m", 1.0, timestamp=10.0)
    w.record("d", "m", 2.0, timestamp=20.0)
    pts = w.recent_points("d", "m", 100.0, now=100.0)
    assert [p.timestamp for p in pts] == [10.0, 20.0, 30.0]


def test_recent_points_filters_window():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=10.0)
    w.record("d", "m", 2.0, timestamp=90.0)
    pts = w.recent_points("d", "m", 20.0, now=100.0)
    assert len(pts) == 1
    assert pts[0].value == 2.0


def test_recent_points_empty_returns_list():
    w = DocMetricWindow()
    assert w.recent_points("d", "m", 1.0, now=10.0) == []


def test_recent_points_only_returns_matching_key():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=10.0)
    w.record("d2", "m", 2.0, timestamp=10.0)
    w.record("d", "m2", 3.0, timestamp=10.0)
    pts = w.recent_points("d", "m", 60.0, now=20.0)
    assert len(pts) == 1
    assert pts[0].value == 1.0


# ------------------------------------------------------- rolling aggregations


def test_rolling_average_basic():
    w = DocMetricWindow()
    for v, ts in [(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]:
        w.record("d", "m", v, timestamp=ts)
    assert w.rolling_average("d", "m", 10.0, now=5.0) == 2.0


def test_rolling_average_none_when_empty():
    w = DocMetricWindow()
    assert w.rolling_average("d", "m", 10.0, now=100.0) is None


def test_rolling_sum_basic():
    w = DocMetricWindow()
    for v, ts in [(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]:
        w.record("d", "m", v, timestamp=ts)
    assert w.rolling_sum("d", "m", 10.0, now=5.0) == 6.0


def test_rolling_sum_none_when_empty():
    w = DocMetricWindow()
    assert w.rolling_sum("d", "m", 10.0, now=100.0) is None


def test_rolling_sum_excludes_old_points():
    w = DocMetricWindow()
    w.record("d", "m", 100.0, timestamp=1.0)
    w.record("d", "m", 5.0, timestamp=99.0)
    assert w.rolling_sum("d", "m", 5.0, now=100.0) == 5.0


# ------------------------------------------------------------------- pruning


def test_prune_before_removes_old():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=5.0)
    w.record("d", "m", 2.0, timestamp=15.0)
    w.record("d", "m", 3.0, timestamp=25.0)
    removed = w.prune_before(20.0)
    assert removed == 2
    assert len(w._points) == 1
    assert w._points[0].value == 3.0


def test_prune_before_zero_when_nothing_removed():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=100.0)
    assert w.prune_before(50.0) == 0


def test_prune_before_keeps_equal_timestamp():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=50.0)
    assert w.prune_before(50.0) == 0
    assert len(w._points) == 1


def test_prune_before_rebuilds_index():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=5.0)
    w.record("d", "m", 2.0, timestamp=15.0)
    w.prune_before(10.0)
    # index for ('d','m') should reference only position 0 of new list
    assert w._by_key[("d", "m")] == [0]
    assert w._points[0].value == 2.0


def test_prune_before_empties_index_for_key():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=5.0)
    w.prune_before(10.0)
    assert ("d", "m") not in w._by_key


def test_prune_before_then_window_stats():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=5.0)
    w.record("d", "m", 2.0, timestamp=15.0)
    w.prune_before(10.0)
    s = w.window_stats("d", "m", 100.0, now=100.0)
    assert s.count == 1
    assert s.sum == 2.0


# ---------------------------------------------------------------- clear_doc


def test_clear_doc_returns_count():
    w = DocMetricWindow()
    w.record("d1", "m", 1.0, timestamp=1.0)
    w.record("d1", "m2", 2.0, timestamp=2.0)
    w.record("d2", "m", 3.0, timestamp=3.0)
    assert w.clear_doc("d1") == 2


def test_clear_doc_keeps_other_docs():
    w = DocMetricWindow()
    w.record("d1", "m", 1.0, timestamp=1.0)
    w.record("d2", "m", 2.0, timestamp=2.0)
    w.clear_doc("d1")
    assert w.all_doc_ids() == ["d2"]


def test_clear_doc_nonexistent():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=1.0)
    assert w.clear_doc("missing") == 0
    assert w.stats().total_points == 1


def test_clear_doc_rebuilds_index():
    w = DocMetricWindow()
    w.record("d1", "m", 1.0, timestamp=1.0)
    w.record("d2", "m", 2.0, timestamp=2.0)
    w.clear_doc("d1")
    assert ("d1", "m") not in w._by_key
    assert w._by_key[("d2", "m")] == [0]


# --------------------------------------------------------------- clear_metric


def test_clear_metric_returns_count():
    w = DocMetricWindow()
    w.record("d", "m1", 1.0, timestamp=1.0)
    w.record("d", "m1", 2.0, timestamp=2.0)
    w.record("d", "m2", 3.0, timestamp=3.0)
    assert w.clear_metric("m1") == 2


def test_clear_metric_keeps_other_metrics():
    w = DocMetricWindow()
    w.record("d", "m1", 1.0, timestamp=1.0)
    w.record("d", "m2", 2.0, timestamp=2.0)
    w.clear_metric("m1")
    assert w.metrics_for_doc("d") == ["m2"]


def test_clear_metric_nonexistent():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=1.0)
    assert w.clear_metric("nope") == 0


# ----------------------------------------------------------------- clear_all


def test_clear_all_returns_count():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=1.0)
    w.record("d", "m2", 2.0, timestamp=2.0)
    assert w.clear_all() == 2


def test_clear_all_empties_state():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=1.0)
    w.clear_all()
    assert w.stats() == MetricStats(total_points=0, unique_metrics=0, unique_docs=0)
    assert w._points == []
    assert w._by_key == {}


def test_clear_all_on_empty():
    w = DocMetricWindow()
    assert w.clear_all() == 0


# ------------------------------------------------------------------ listings


def test_metrics_for_doc_sorted_unique():
    w = DocMetricWindow()
    w.record("d", "z", 1.0, timestamp=1.0)
    w.record("d", "a", 2.0, timestamp=2.0)
    w.record("d", "m", 3.0, timestamp=3.0)
    w.record("d", "a", 4.0, timestamp=4.0)
    assert w.metrics_for_doc("d") == ["a", "m", "z"]


def test_metrics_for_doc_other_doc_excluded():
    w = DocMetricWindow()
    w.record("d1", "m1", 1.0, timestamp=1.0)
    w.record("d2", "m2", 2.0, timestamp=2.0)
    assert w.metrics_for_doc("d1") == ["m1"]


def test_docs_for_metric_sorted_unique():
    w = DocMetricWindow()
    w.record("zz", "m", 1.0, timestamp=1.0)
    w.record("aa", "m", 2.0, timestamp=2.0)
    w.record("mm", "m", 3.0, timestamp=3.0)
    w.record("aa", "m", 4.0, timestamp=4.0)
    assert w.docs_for_metric("m") == ["aa", "mm", "zz"]


def test_docs_for_metric_other_metric_excluded():
    w = DocMetricWindow()
    w.record("d1", "m1", 1.0, timestamp=1.0)
    w.record("d2", "m2", 2.0, timestamp=2.0)
    assert w.docs_for_metric("m1") == ["d1"]


def test_all_doc_ids_sorted_unique():
    w = DocMetricWindow()
    w.record("zz", "m1", 1.0, timestamp=1.0)
    w.record("aa", "m2", 2.0, timestamp=2.0)
    w.record("zz", "m3", 3.0, timestamp=3.0)
    assert w.all_doc_ids() == ["aa", "zz"]


# ---------------------------------------------------------------------- stats


def test_stats_counts_points():
    w = DocMetricWindow()
    for i in range(5):
        w.record("d", "m", float(i), timestamp=float(i))
    assert w.stats().total_points == 5


def test_stats_counts_unique_docs():
    w = DocMetricWindow()
    w.record("d1", "m", 1.0, timestamp=1.0)
    w.record("d2", "m", 2.0, timestamp=2.0)
    w.record("d1", "m", 3.0, timestamp=3.0)
    assert w.stats().unique_docs == 2


def test_stats_counts_unique_metrics():
    w = DocMetricWindow()
    w.record("d", "m1", 1.0, timestamp=1.0)
    w.record("d", "m2", 2.0, timestamp=2.0)
    w.record("d", "m1", 3.0, timestamp=3.0)
    assert w.stats().unique_metrics == 2


def test_stats_after_clear_all():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=1.0)
    w.clear_all()
    assert w.stats() == MetricStats(total_points=0, unique_metrics=0, unique_docs=0)


# ------------------------------------------------------------------- dataclass


def test_window_point_dataclass_fields():
    p = WindowPoint(doc_id="x", metric="y", value=1.5, timestamp=2.0)
    assert (p.doc_id, p.metric, p.value, p.timestamp) == ("x", "y", 1.5, 2.0)


def test_window_stats_dataclass_fields():
    s = WindowStats(count=1, sum=2.0, avg=2.0, min_value=2.0, max_value=2.0)
    assert s.count == 1 and s.sum == 2.0


def test_metric_stats_dataclass_fields():
    s = MetricStats(total_points=3, unique_metrics=2, unique_docs=1)
    assert s.total_points == 3
    assert s.unique_metrics == 2
    assert s.unique_docs == 1


# -------------------------------------------------------------- thread safety


def test_thread_safe_concurrent_record():
    w = DocMetricWindow()
    n_threads = 8
    n_per_thread = 200

    def worker(tid: int):
        for i in range(n_per_thread):
            w.record(f"d{tid}", "m", float(i), timestamp=float(i))

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert w.stats().total_points == n_threads * n_per_thread
    assert w.stats().unique_docs == n_threads


def test_thread_safe_record_and_query():
    w = DocMetricWindow()
    stop = threading.Event()
    errors: list[Exception] = []

    def writer():
        i = 0
        while not stop.is_set():
            try:
                w.record("d", "m", float(i % 100), timestamp=float(i))
            except Exception as e:  # noqa: BLE001
                errors.append(e)
            i += 1

    def reader():
        while not stop.is_set():
            try:
                w.window_stats("d", "m", 1000.0, now=1e9)
                w.recent_points("d", "m", 1000.0, now=1e9)
                w.stats()
            except Exception as e:  # noqa: BLE001
                errors.append(e)

    threads = [threading.Thread(target=writer) for _ in range(3)]
    threads += [threading.Thread(target=reader) for _ in range(3)]
    for t in threads:
        t.start()
    time.sleep(0.2)
    stop.set()
    for t in threads:
        t.join()

    assert errors == []
    assert w.stats().total_points > 0


def test_thread_safe_prune_during_record():
    w = DocMetricWindow()
    for i in range(500):
        w.record("d", "m", float(i), timestamp=float(i))

    stop = threading.Event()
    errors: list[Exception] = []

    def pruner():
        while not stop.is_set():
            try:
                w.prune_before(100.0)
            except Exception as e:  # noqa: BLE001
                errors.append(e)

    def reader():
        while not stop.is_set():
            try:
                w.window_stats("d", "m", 1000.0, now=1e9)
            except Exception as e:  # noqa: BLE001
                errors.append(e)

    threads = [threading.Thread(target=pruner), threading.Thread(target=reader)]
    for t in threads:
        t.start()
    time.sleep(0.1)
    stop.set()
    for t in threads:
        t.join()

    assert errors == []


# ----------------------------------------------------------- integration-ish


def test_full_lifecycle():
    w = DocMetricWindow()
    w.record("d1", "latency", 1.0, timestamp=10.0)
    w.record("d1", "latency", 2.0, timestamp=20.0)
    w.record("d1", "latency", 3.0, timestamp=30.0)
    w.record("d1", "errors", 5.0, timestamp=20.0)
    w.record("d2", "latency", 7.0, timestamp=25.0)

    assert w.stats().total_points == 5
    assert w.metrics_for_doc("d1") == ["errors", "latency"]
    assert w.docs_for_metric("latency") == ["d1", "d2"]

    s = w.window_stats("d1", "latency", 15.0, now=30.0)
    assert s.count == 2
    assert s.sum == 5.0
    assert s.avg == 2.5

    assert w.rolling_sum("d1", "latency", 15.0, now=30.0) == 5.0
    assert w.rolling_average("d1", "latency", 15.0, now=30.0) == 2.5

    removed = w.prune_before(25.0)
    assert removed == 3  # latency@10,20 and errors@20

    assert w.stats().total_points == 2
    assert w.clear_metric("latency") == 2
    assert w.stats().total_points == 0


def test_negative_values_supported():
    w = DocMetricWindow()
    w.record("d", "m", -1.0, timestamp=1.0)
    w.record("d", "m", -2.0, timestamp=2.0)
    s = w.window_stats("d", "m", 10.0, now=5.0)
    assert s.sum == -3.0
    assert s.min_value == -2.0
    assert s.max_value == -1.0


def test_zero_window_includes_only_now():
    w = DocMetricWindow()
    w.record("d", "m", 1.0, timestamp=100.0)
    w.record("d", "m", 2.0, timestamp=99.0)
    s = w.window_stats("d", "m", 0.0, now=100.0)
    assert s is not None
    assert s.count == 1
    assert s.sum == 1.0


def test_large_window_includes_all():
    w = DocMetricWindow()
    for i in range(10):
        w.record("d", "m", float(i), timestamp=float(i))
    s = w.window_stats("d", "m", 1e9, now=1e9)
    assert s.count == 10
    assert s.sum == 45.0


def test_record_does_not_affect_other_keys_index():
    w = DocMetricWindow()
    w.record("d1", "m", 1.0, timestamp=1.0)
    w.record("d2", "m", 2.0, timestamp=2.0)
    assert w._by_key[("d1", "m")] == [0]
    assert w._by_key[("d2", "m")] == [1]
