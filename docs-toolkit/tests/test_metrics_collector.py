"""Tests for docstoolkit.metrics_collector — E113 Metrics Collector.

Coverage targets
----------------
- MetricType enum (counter / gauge / histogram / timer)
- counter: default increment, custom value, accumulation
- gauge: set / update / total tracking
- histogram: records observations, min/max, percentiles
- timer: records durations, percentiles
- measure() context manager
- snapshot(): correct MetricSnapshot fields
- snapshot(): None for unknown metric
- all_snapshots(): returns all metrics in order
- reset(): True when found, False when missing; state cleared
- reset_all(): all metrics zeroed; names preserved
- metric_names(): insertion order
- exists(): True/False
- count / total / min / max accuracy
- p50 / p95 / p99 correctness with known distributions
- thread safety: concurrent counter increments
- labels stored in snapshot
- multiple metrics are independent
- type mismatch raises ValueError
- MetricSnapshot dataclass fields
"""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.metrics_collector import (
    MetricSnapshot,
    MetricType,
    MetricsCollector,
)


# ===========================================================================
# Helpers
# ===========================================================================

def fresh() -> MetricsCollector:
    """Return a new, empty MetricsCollector."""
    return MetricsCollector()


# ===========================================================================
# MetricType enum
# ===========================================================================

class TestMetricType:
    def test_counter_value(self):
        assert MetricType.COUNTER.value == "counter"

    def test_gauge_value(self):
        assert MetricType.GAUGE.value == "gauge"

    def test_histogram_value(self):
        assert MetricType.HISTOGRAM.value == "histogram"

    def test_timer_value(self):
        assert MetricType.TIMER.value == "timer"

    def test_all_four_members(self):
        names = {m.name for m in MetricType}
        assert names == {"COUNTER", "GAUGE", "HISTOGRAM", "TIMER"}

    def test_str_enum_identity(self):
        assert MetricType("counter") is MetricType.COUNTER

    def test_is_str_subclass(self):
        assert isinstance(MetricType.COUNTER, str)


# ===========================================================================
# MetricSnapshot dataclass
# ===========================================================================

class TestMetricSnapshot:
    def test_all_required_fields(self):
        snap = MetricSnapshot(
            name="x",
            metric_type=MetricType.COUNTER,
            value=5.0,
            count=5,
            total=5.0,
        )
        assert snap.name == "x"
        assert snap.metric_type == MetricType.COUNTER
        assert snap.value == 5.0
        assert snap.count == 5
        assert snap.total == 5.0

    def test_optional_fields_default_none(self):
        snap = MetricSnapshot(
            name="x", metric_type=MetricType.GAUGE,
            value=0.0, count=0, total=0.0,
        )
        assert snap.min is None
        assert snap.max is None
        assert snap.p50 is None
        assert snap.p95 is None
        assert snap.p99 is None

    def test_labels_default_empty_dict(self):
        snap = MetricSnapshot(
            name="x", metric_type=MetricType.GAUGE,
            value=0.0, count=0, total=0.0,
        )
        assert snap.labels == {}

    def test_labels_independent_between_instances(self):
        s1 = MetricSnapshot(
            name="a", metric_type=MetricType.GAUGE,
            value=0.0, count=0, total=0.0, labels={"k": "v"},
        )
        s2 = MetricSnapshot(
            name="b", metric_type=MetricType.GAUGE,
            value=0.0, count=0, total=0.0,
        )
        assert "k" not in s2.labels


# ===========================================================================
# Counter
# ===========================================================================

class TestCounter:
    def test_default_increment_is_one(self):
        mc = fresh()
        mc.counter("req")
        snap = mc.snapshot("req")
        assert snap.value == 1.0

    def test_count_after_single_call(self):
        mc = fresh()
        mc.counter("req")
        assert mc.snapshot("req").count == 1

    def test_custom_increment_value(self):
        mc = fresh()
        mc.counter("bytes", value=512.0)
        assert mc.snapshot("bytes").value == 512.0

    def test_accumulates_over_multiple_calls(self):
        mc = fresh()
        for _ in range(5):
            mc.counter("req")
        assert mc.snapshot("req").value == 5.0

    def test_count_tracks_number_of_calls(self):
        mc = fresh()
        mc.counter("req")
        mc.counter("req")
        mc.counter("req")
        assert mc.snapshot("req").count == 3

    def test_total_equals_value_for_counter(self):
        mc = fresh()
        mc.counter("req", value=3.0)
        mc.counter("req", value=7.0)
        snap = mc.snapshot("req")
        assert snap.total == pytest.approx(10.0)
        assert snap.value == pytest.approx(10.0)

    def test_counter_type_in_snapshot(self):
        mc = fresh()
        mc.counter("req")
        assert mc.snapshot("req").metric_type == MetricType.COUNTER

    def test_counter_fractional_value(self):
        mc = fresh()
        mc.counter("score", value=0.5)
        mc.counter("score", value=0.25)
        assert mc.snapshot("score").value == pytest.approx(0.75)

    def test_counter_min_max_none(self):
        mc = fresh()
        mc.counter("c")
        snap = mc.snapshot("c")
        assert snap.min is None
        assert snap.max is None

    def test_counter_percentiles_none(self):
        mc = fresh()
        mc.counter("c")
        snap = mc.snapshot("c")
        assert snap.p50 is None
        assert snap.p95 is None
        assert snap.p99 is None


# ===========================================================================
# Gauge
# ===========================================================================

class TestGauge:
    def test_set_value(self):
        mc = fresh()
        mc.gauge("temp", 22.5)
        assert mc.snapshot("temp").value == pytest.approx(22.5)

    def test_update_overwrites_value(self):
        mc = fresh()
        mc.gauge("temp", 22.5)
        mc.gauge("temp", 30.0)
        assert mc.snapshot("temp").value == pytest.approx(30.0)

    def test_count_tracks_number_of_sets(self):
        mc = fresh()
        mc.gauge("temp", 1.0)
        mc.gauge("temp", 2.0)
        mc.gauge("temp", 3.0)
        assert mc.snapshot("temp").count == 3

    def test_total_is_sum_of_all_set_values(self):
        mc = fresh()
        mc.gauge("temp", 10.0)
        mc.gauge("temp", 20.0)
        mc.gauge("temp", 30.0)
        assert mc.snapshot("temp").total == pytest.approx(60.0)

    def test_gauge_type_in_snapshot(self):
        mc = fresh()
        mc.gauge("g", 0.0)
        assert mc.snapshot("g").metric_type == MetricType.GAUGE

    def test_gauge_can_go_negative(self):
        mc = fresh()
        mc.gauge("delta", -5.0)
        assert mc.snapshot("delta").value == pytest.approx(-5.0)

    def test_gauge_min_max_none(self):
        mc = fresh()
        mc.gauge("g", 1.0)
        snap = mc.snapshot("g")
        assert snap.min is None
        assert snap.max is None

    def test_gauge_percentiles_none(self):
        mc = fresh()
        mc.gauge("g", 1.0)
        snap = mc.snapshot("g")
        assert snap.p50 is None
        assert snap.p95 is None
        assert snap.p99 is None


# ===========================================================================
# Histogram
# ===========================================================================

class TestHistogram:
    def test_single_observation_value(self):
        mc = fresh()
        mc.histogram("size", 1024.0)
        assert mc.snapshot("size").value == pytest.approx(1024.0)

    def test_value_is_last_observation(self):
        mc = fresh()
        mc.histogram("size", 100.0)
        mc.histogram("size", 200.0)
        mc.histogram("size", 300.0)
        assert mc.snapshot("size").value == pytest.approx(300.0)

    def test_count(self):
        mc = fresh()
        for v in [1.0, 2.0, 3.0]:
            mc.histogram("h", v)
        assert mc.snapshot("h").count == 3

    def test_total(self):
        mc = fresh()
        for v in [10.0, 20.0, 30.0]:
            mc.histogram("h", v)
        assert mc.snapshot("h").total == pytest.approx(60.0)

    def test_min_single(self):
        mc = fresh()
        mc.histogram("h", 42.0)
        assert mc.snapshot("h").min == pytest.approx(42.0)

    def test_max_single(self):
        mc = fresh()
        mc.histogram("h", 42.0)
        assert mc.snapshot("h").max == pytest.approx(42.0)

    def test_min_multiple(self):
        mc = fresh()
        for v in [5.0, 2.0, 8.0, 1.0]:
            mc.histogram("h", v)
        assert mc.snapshot("h").min == pytest.approx(1.0)

    def test_max_multiple(self):
        mc = fresh()
        for v in [5.0, 2.0, 8.0, 1.0]:
            mc.histogram("h", v)
        assert mc.snapshot("h").max == pytest.approx(8.0)

    def test_histogram_type_in_snapshot(self):
        mc = fresh()
        mc.histogram("h", 1.0)
        assert mc.snapshot("h").metric_type == MetricType.HISTOGRAM

    def test_p50_single_value(self):
        mc = fresh()
        mc.histogram("h", 7.0)
        assert mc.snapshot("h").p50 == pytest.approx(7.0)

    def test_p50_five_values(self):
        # [1,2,3,4,5] → median = 3.0
        mc = fresh()
        for v in [1.0, 2.0, 3.0, 4.0, 5.0]:
            mc.histogram("h", v)
        assert mc.snapshot("h").p50 == pytest.approx(3.0)

    def test_p95_uniform_distribution(self):
        # 100 values: 1..100.  p95 → rank = 0.95 * 99 = 94.05 → 95 + 0.05 = 95.05
        mc = fresh()
        for v in range(1, 101):
            mc.histogram("h", float(v))
        snap = mc.snapshot("h")
        assert snap.p95 == pytest.approx(95.05, rel=1e-4)

    def test_p99_uniform_distribution(self):
        # rank = 0.99 * 99 = 98.01 → vals[98]=99, vals[99]=100 → 99 + 0.01 = 99.01
        mc = fresh()
        for v in range(1, 101):
            mc.histogram("h", float(v))
        snap = mc.snapshot("h")
        assert snap.p99 == pytest.approx(99.01, rel=1e-4)

    def test_percentiles_not_none_after_observations(self):
        mc = fresh()
        for v in [10.0, 20.0, 30.0]:
            mc.histogram("h", v)
        snap = mc.snapshot("h")
        assert snap.p50 is not None
        assert snap.p95 is not None
        assert snap.p99 is not None


# ===========================================================================
# Timer
# ===========================================================================

class TestTimer:
    def test_single_duration_value(self):
        mc = fresh()
        mc.timer("db", 12.3)
        assert mc.snapshot("db").value == pytest.approx(12.3)

    def test_value_is_last_duration(self):
        mc = fresh()
        mc.timer("db", 10.0)
        mc.timer("db", 20.0)
        assert mc.snapshot("db").value == pytest.approx(20.0)

    def test_count(self):
        mc = fresh()
        mc.timer("db", 1.0)
        mc.timer("db", 2.0)
        assert mc.snapshot("db").count == 2

    def test_total(self):
        mc = fresh()
        mc.timer("db", 5.0)
        mc.timer("db", 15.0)
        assert mc.snapshot("db").total == pytest.approx(20.0)

    def test_min(self):
        mc = fresh()
        for ms in [50.0, 10.0, 30.0]:
            mc.timer("t", ms)
        assert mc.snapshot("t").min == pytest.approx(10.0)

    def test_max(self):
        mc = fresh()
        for ms in [50.0, 10.0, 30.0]:
            mc.timer("t", ms)
        assert mc.snapshot("t").max == pytest.approx(50.0)

    def test_timer_type_in_snapshot(self):
        mc = fresh()
        mc.timer("t", 1.0)
        assert mc.snapshot("t").metric_type == MetricType.TIMER

    def test_p50_three_values(self):
        mc = fresh()
        for ms in [10.0, 20.0, 30.0]:
            mc.timer("t", ms)
        # sorted [10,20,30], p50 → rank=1.0 → 20.0
        assert mc.snapshot("t").p50 == pytest.approx(20.0)

    def test_p95_ten_values(self):
        # [10,20,...,100].  rank = 0.95*9=8.55 → 90 + 0.55*10 = 95.5
        mc = fresh()
        for ms in range(10, 101, 10):
            mc.timer("t", float(ms))
        snap = mc.snapshot("t")
        assert snap.p95 == pytest.approx(95.5, rel=1e-4)

    def test_p99_ten_values(self):
        # rank = 0.99*9=8.91 → 90 + 0.91*10 = 99.1
        mc = fresh()
        for ms in range(10, 101, 10):
            mc.timer("t", float(ms))
        snap = mc.snapshot("t")
        assert snap.p99 == pytest.approx(99.1, rel=1e-4)


# ===========================================================================
# measure() context manager
# ===========================================================================

class TestMeasure:
    def test_measure_creates_timer_metric(self):
        mc = fresh()
        with mc.measure("op"):
            pass
        assert mc.exists("op")
        assert mc.snapshot("op").metric_type == MetricType.TIMER

    def test_measure_records_positive_duration(self):
        mc = fresh()
        with mc.measure("op"):
            pass
        assert mc.snapshot("op").value >= 0.0

    def test_measure_duration_roughly_correct(self):
        mc = fresh()
        with mc.measure("op"):
            time.sleep(0.05)  # 50 ms
        snap = mc.snapshot("op")
        # generous tolerance: 10 ms – 500 ms
        assert 10.0 <= snap.value <= 500.0

    def test_measure_count_increments(self):
        mc = fresh()
        with mc.measure("op"):
            pass
        with mc.measure("op"):
            pass
        assert mc.snapshot("op").count == 2

    def test_measure_with_labels(self):
        mc = fresh()
        with mc.measure("op", labels={"env": "test"}):
            pass
        assert mc.snapshot("op").labels == {"env": "test"}

    def test_measure_records_even_on_exception(self):
        mc = fresh()
        with pytest.raises(RuntimeError):
            with mc.measure("op"):
                raise RuntimeError("boom")
        assert mc.snapshot("op").count == 1

    def test_measure_yields_none(self):
        mc = fresh()
        with mc.measure("op") as ctx:
            assert ctx is None


# ===========================================================================
# snapshot()
# ===========================================================================

class TestSnapshot:
    def test_returns_none_for_unknown(self):
        mc = fresh()
        assert mc.snapshot("nonexistent") is None

    def test_returns_metric_snapshot_instance(self):
        mc = fresh()
        mc.counter("c")
        assert isinstance(mc.snapshot("c"), MetricSnapshot)

    def test_snapshot_name_matches(self):
        mc = fresh()
        mc.counter("my_counter")
        assert mc.snapshot("my_counter").name == "my_counter"

    def test_snapshot_is_copy_not_reference(self):
        """Two consecutive snapshots are independent objects."""
        mc = fresh()
        mc.counter("c")
        s1 = mc.snapshot("c")
        mc.counter("c")
        s2 = mc.snapshot("c")
        assert s1.value != s2.value

    def test_snapshot_labels_is_copy(self):
        """Mutating the returned labels dict does not affect the metric."""
        mc = fresh()
        mc.counter("c", labels={"k": "v"})
        snap = mc.snapshot("c")
        snap.labels["extra"] = "x"
        snap2 = mc.snapshot("c")
        assert "extra" not in snap2.labels


# ===========================================================================
# all_snapshots()
# ===========================================================================

class TestAllSnapshots:
    def test_empty_returns_empty_list(self):
        mc = fresh()
        assert mc.all_snapshots() == []

    def test_returns_list_of_metric_snapshots(self):
        mc = fresh()
        mc.counter("a")
        mc.gauge("b", 1.0)
        snaps = mc.all_snapshots()
        assert all(isinstance(s, MetricSnapshot) for s in snaps)

    def test_count_matches_registered_metrics(self):
        mc = fresh()
        mc.counter("a")
        mc.gauge("b", 1.0)
        mc.histogram("c", 5.0)
        assert len(mc.all_snapshots()) == 3

    def test_insertion_order_preserved(self):
        mc = fresh()
        mc.counter("z")
        mc.gauge("a", 0.0)
        mc.timer("m", 1.0)
        names = [s.name for s in mc.all_snapshots()]
        assert names == ["z", "a", "m"]

    def test_reflects_latest_values(self):
        mc = fresh()
        mc.counter("c")
        mc.counter("c")
        snaps = {s.name: s for s in mc.all_snapshots()}
        assert snaps["c"].count == 2


# ===========================================================================
# reset()
# ===========================================================================

class TestReset:
    def test_returns_true_when_found(self):
        mc = fresh()
        mc.counter("c")
        assert mc.reset("c") is True

    def test_returns_false_when_not_found(self):
        mc = fresh()
        assert mc.reset("ghost") is False

    def test_counter_value_zeroed(self):
        mc = fresh()
        mc.counter("c", value=5.0)
        mc.reset("c")
        assert mc.snapshot("c").value == 0.0

    def test_counter_count_zeroed(self):
        mc = fresh()
        mc.counter("c")
        mc.reset("c")
        assert mc.snapshot("c").count == 0

    def test_counter_total_zeroed(self):
        mc = fresh()
        mc.counter("c", value=99.0)
        mc.reset("c")
        assert mc.snapshot("c").total == 0.0

    def test_histogram_observations_cleared(self):
        mc = fresh()
        for v in [1.0, 2.0, 3.0]:
            mc.histogram("h", v)
        mc.reset("h")
        snap = mc.snapshot("h")
        assert snap.count == 0
        assert snap.p50 is None

    def test_histogram_min_max_cleared(self):
        mc = fresh()
        mc.histogram("h", 5.0)
        mc.reset("h")
        snap = mc.snapshot("h")
        assert snap.min is None
        assert snap.max is None

    def test_metric_still_exists_after_reset(self):
        mc = fresh()
        mc.counter("c")
        mc.reset("c")
        assert mc.exists("c")

    def test_can_record_after_reset(self):
        mc = fresh()
        mc.counter("c", value=10.0)
        mc.reset("c")
        mc.counter("c", value=1.0)
        assert mc.snapshot("c").value == pytest.approx(1.0)


# ===========================================================================
# reset_all()
# ===========================================================================

class TestResetAll:
    def test_zeroes_all_metrics(self):
        mc = fresh()
        mc.counter("a", value=5.0)
        mc.gauge("b", 3.0)
        mc.histogram("c", 7.0)
        mc.reset_all()
        for name in ["a", "b", "c"]:
            snap = mc.snapshot(name)
            assert snap.count == 0
            assert snap.value == 0.0

    def test_names_still_registered_after_reset_all(self):
        mc = fresh()
        mc.counter("a")
        mc.gauge("b", 0.0)
        mc.reset_all()
        assert set(mc.metric_names()) == {"a", "b"}

    def test_empty_collector_reset_all_is_noop(self):
        mc = fresh()
        mc.reset_all()  # should not raise
        assert mc.all_snapshots() == []


# ===========================================================================
# metric_names()
# ===========================================================================

class TestMetricNames:
    def test_empty_returns_empty_list(self):
        mc = fresh()
        assert mc.metric_names() == []

    def test_returns_all_names(self):
        mc = fresh()
        mc.counter("x")
        mc.gauge("y", 0.0)
        assert set(mc.metric_names()) == {"x", "y"}

    def test_insertion_order(self):
        mc = fresh()
        mc.timer("t1", 1.0)
        mc.timer("t2", 2.0)
        mc.counter("c1")
        assert mc.metric_names() == ["t1", "t2", "c1"]

    def test_no_duplicates(self):
        mc = fresh()
        mc.counter("c")
        mc.counter("c")
        mc.counter("c")
        assert mc.metric_names().count("c") == 1

    def test_returns_copy(self):
        mc = fresh()
        mc.counter("c")
        names = mc.metric_names()
        names.append("injected")
        assert "injected" not in mc.metric_names()


# ===========================================================================
# exists()
# ===========================================================================

class TestExists:
    def test_false_for_unknown(self):
        mc = fresh()
        assert mc.exists("nope") is False

    def test_true_after_counter(self):
        mc = fresh()
        mc.counter("c")
        assert mc.exists("c") is True

    def test_true_after_gauge(self):
        mc = fresh()
        mc.gauge("g", 0.0)
        assert mc.exists("g") is True

    def test_true_after_histogram(self):
        mc = fresh()
        mc.histogram("h", 1.0)
        assert mc.exists("h") is True

    def test_true_after_timer(self):
        mc = fresh()
        mc.timer("t", 1.0)
        assert mc.exists("t") is True

    def test_still_true_after_reset(self):
        mc = fresh()
        mc.counter("c")
        mc.reset("c")
        assert mc.exists("c") is True

    def test_false_after_fresh_instance(self):
        mc1 = fresh()
        mc2 = fresh()
        mc1.counter("c")
        assert mc2.exists("c") is False


# ===========================================================================
# Labels
# ===========================================================================

class TestLabels:
    def test_labels_stored_in_counter_snapshot(self):
        mc = fresh()
        mc.counter("req", labels={"method": "GET", "status": "200"})
        snap = mc.snapshot("req")
        assert snap.labels == {"method": "GET", "status": "200"}

    def test_labels_stored_in_gauge_snapshot(self):
        mc = fresh()
        mc.gauge("temp", 22.0, labels={"host": "web01"})
        assert mc.snapshot("temp").labels == {"host": "web01"}

    def test_labels_stored_in_histogram_snapshot(self):
        mc = fresh()
        mc.histogram("size", 512.0, labels={"bucket": "s3"})
        assert mc.snapshot("size").labels == {"bucket": "s3"}

    def test_labels_stored_in_timer_snapshot(self):
        mc = fresh()
        mc.timer("query", 5.0, labels={"db": "postgres"})
        assert mc.snapshot("query").labels == {"db": "postgres"}

    def test_first_call_labels_win(self):
        """Subsequent calls with different labels are ignored."""
        mc = fresh()
        mc.counter("c", labels={"first": "yes"})
        mc.counter("c", labels={"second": "yes"})
        snap = mc.snapshot("c")
        assert snap.labels == {"first": "yes"}
        assert "second" not in snap.labels

    def test_no_labels_stored_as_empty_dict(self):
        mc = fresh()
        mc.counter("c")
        assert mc.snapshot("c").labels == {}

    def test_labels_in_all_snapshots(self):
        mc = fresh()
        mc.counter("c", labels={"env": "prod"})
        snaps = {s.name: s for s in mc.all_snapshots()}
        assert snaps["c"].labels == {"env": "prod"}


# ===========================================================================
# Multiple independent metrics
# ===========================================================================

class TestMultipleMetrics:
    def test_counters_independent(self):
        mc = fresh()
        mc.counter("a", value=3.0)
        mc.counter("b", value=7.0)
        assert mc.snapshot("a").value == pytest.approx(3.0)
        assert mc.snapshot("b").value == pytest.approx(7.0)

    def test_different_types_independent(self):
        mc = fresh()
        mc.counter("requests", value=100.0)
        mc.gauge("temperature", 25.0)
        mc.histogram("payload", 1024.0)
        mc.timer("latency", 30.0)

        assert mc.snapshot("requests").metric_type == MetricType.COUNTER
        assert mc.snapshot("temperature").metric_type == MetricType.GAUGE
        assert mc.snapshot("payload").metric_type == MetricType.HISTOGRAM
        assert mc.snapshot("latency").metric_type == MetricType.TIMER

    def test_reset_one_leaves_others_unchanged(self):
        mc = fresh()
        mc.counter("a", value=5.0)
        mc.counter("b", value=10.0)
        mc.reset("a")
        assert mc.snapshot("b").value == pytest.approx(10.0)

    def test_all_snapshots_contains_all(self):
        mc = fresh()
        mc.counter("c1")
        mc.gauge("g1", 0.0)
        mc.histogram("h1", 1.0)
        mc.timer("t1", 1.0)
        names = {s.name for s in mc.all_snapshots()}
        assert names == {"c1", "g1", "h1", "t1"}


# ===========================================================================
# Type mismatch
# ===========================================================================

class TestTypeMismatch:
    def test_counter_then_gauge_raises(self):
        mc = fresh()
        mc.counter("m")
        with pytest.raises(ValueError):
            mc.gauge("m", 1.0)

    def test_gauge_then_counter_raises(self):
        mc = fresh()
        mc.gauge("m", 1.0)
        with pytest.raises(ValueError):
            mc.counter("m")

    def test_histogram_then_timer_raises(self):
        mc = fresh()
        mc.histogram("m", 1.0)
        with pytest.raises(ValueError):
            mc.timer("m", 1.0)

    def test_timer_then_histogram_raises(self):
        mc = fresh()
        mc.timer("m", 1.0)
        with pytest.raises(ValueError):
            mc.histogram("m", 1.0)


# ===========================================================================
# Percentile correctness (known distributions)
# ===========================================================================

class TestPercentileCorrectness:
    def test_two_values_p50(self):
        # [0, 100]: rank = 0.5 * 1 = 0.5 → 0 + 0.5*100 = 50.0
        mc = fresh()
        mc.histogram("h", 0.0)
        mc.histogram("h", 100.0)
        assert mc.snapshot("h").p50 == pytest.approx(50.0)

    def test_sorted_insertion_order_does_not_matter(self):
        mc1 = fresh()
        mc2 = fresh()
        for v in [5.0, 1.0, 3.0, 2.0, 4.0]:
            mc1.histogram("h", v)
        for v in [1.0, 2.0, 3.0, 4.0, 5.0]:
            mc2.histogram("h", v)
        assert mc1.snapshot("h").p50 == pytest.approx(mc2.snapshot("h").p50)

    def test_p50_equals_median_odd_count(self):
        mc = fresh()
        for v in [10.0, 30.0, 20.0]:   # sorted: [10,20,30]
            mc.histogram("h", v)
        # rank = 0.5 * 2 = 1.0 → vals[1] = 20.0
        assert mc.snapshot("h").p50 == pytest.approx(20.0)

    def test_p99_almost_max(self):
        mc = fresh()
        for v in range(1, 101):
            mc.histogram("h", float(v))
        snap = mc.snapshot("h")
        # p99 must be close to 100 but not equal
        assert snap.p99 < 100.0
        assert snap.p99 > 98.0

    def test_p50_lte_p95_lte_p99(self):
        mc = fresh()
        for v in range(1, 51):
            mc.timer("t", float(v))
        snap = mc.snapshot("t")
        assert snap.p50 <= snap.p95 <= snap.p99

    def test_single_value_all_percentiles_equal(self):
        mc = fresh()
        mc.histogram("h", 42.0)
        snap = mc.snapshot("h")
        assert snap.p50 == pytest.approx(42.0)
        assert snap.p95 == pytest.approx(42.0)
        assert snap.p99 == pytest.approx(42.0)


# ===========================================================================
# Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_counter_increments(self):
        """1000 threads each increment by 1 → total must be 1000."""
        mc = fresh()

        def inc():
            mc.counter("c", value=1.0)

        threads = [threading.Thread(target=inc) for _ in range(1000)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        snap = mc.snapshot("c")
        assert snap.value == pytest.approx(1000.0)
        assert snap.count == 1000

    def test_concurrent_histogram_observations(self):
        """500 threads each record one observation → count must be 500."""
        mc = fresh()
        barrier = threading.Barrier(500)

        def observe(v):
            barrier.wait()
            mc.histogram("h", float(v))

        threads = [threading.Thread(target=observe, args=(i,)) for i in range(500)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert mc.snapshot("h").count == 500

    def test_concurrent_snapshot_reads(self):
        """Reading snapshots from many threads must not raise."""
        mc = fresh()
        mc.counter("c")
        errors = []

        def read():
            try:
                mc.snapshot("c")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=read) for _ in range(200)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []

    def test_concurrent_mixed_operations(self):
        """Mix of writes and reads from many threads must not corrupt state."""
        mc = fresh()
        errors = []

        def work(i):
            try:
                mc.counter("c")
                mc.gauge("g", float(i))
                mc.snapshot("c")
                mc.snapshot("g")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=work, args=(i,)) for i in range(300)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        # counter must have been incremented exactly 300 times
        assert mc.snapshot("c").count == 300


# ===========================================================================
# Public __init__ exports
# ===========================================================================

class TestPublicExports:
    def test_metric_type_exported(self):
        from docstoolkit.metrics_collector import MetricType
        assert MetricType.COUNTER

    def test_metric_snapshot_exported(self):
        from docstoolkit.metrics_collector import MetricSnapshot
        assert MetricSnapshot

    def test_metrics_collector_exported(self):
        from docstoolkit.metrics_collector import MetricsCollector
        assert MetricsCollector

    def test_only_three_public_names(self):
        import docstoolkit.metrics_collector as m
        assert set(m.__all__) == {"MetricType", "MetricSnapshot", "MetricsCollector"}
