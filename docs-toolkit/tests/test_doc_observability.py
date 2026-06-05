"""Tests for docstoolkit.doc_observability."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_observability import (
    Aggregate,
    CustomEvent,
    DocObservability,
    MetricPoint,
    MetricType,
    Trace,
)


# ---------------------------------------------------------------------------
class TestMetricType:
    def test_counter(self):
        assert MetricType.COUNTER.value == "counter"

    def test_gauge(self):
        assert MetricType.GAUGE.value == "gauge"

    def test_histogram(self):
        assert MetricType.HISTOGRAM.value == "histogram"

    def test_timing(self):
        assert MetricType.TIMING.value == "timing"

    def test_distinct(self):
        assert len({m for m in MetricType}) == 4


# ---------------------------------------------------------------------------
class TestTrace:
    def test_basic(self):
        t = Trace(trace_id="t1", span_name="s", start_at=100.0)
        assert t.trace_id == "t1"
        assert t.span_name == "s"
        assert t.start_at == 100.0
        assert t.end_at is None
        assert t.parent_span_id is None
        assert t.tags == {}

    def test_duration_zero_when_not_ended(self):
        t = Trace(trace_id="t1", span_name="s", start_at=100.0)
        assert t.duration_ms == 0.0

    def test_duration_ms_calculated(self):
        t = Trace(trace_id="t1", span_name="s", start_at=100.0, end_at=101.5)
        assert t.duration_ms == pytest.approx(1500.0)

    def test_tags_default_independent(self):
        t1 = Trace(trace_id="a", span_name="s", start_at=1.0)
        t2 = Trace(trace_id="b", span_name="s", start_at=1.0)
        t1.tags["x"] = 1
        assert t2.tags == {}


# ---------------------------------------------------------------------------
class TestMetricPoint:
    def test_basic(self):
        m = MetricPoint(
            name="cpu", value=42.0, metric_type=MetricType.GAUGE, timestamp=10.0
        )
        assert m.name == "cpu"
        assert m.value == 42.0
        assert m.metric_type is MetricType.GAUGE
        assert m.timestamp == 10.0
        assert m.tags == {}

    def test_tags(self):
        m = MetricPoint(
            name="cpu",
            value=1.0,
            metric_type=MetricType.COUNTER,
            timestamp=1.0,
            tags={"host": "a"},
        )
        assert m.tags == {"host": "a"}


# ---------------------------------------------------------------------------
class TestCustomEvent:
    def test_basic(self):
        e = CustomEvent(event_id=1, event_type="boot", data={}, timestamp=0.0)
        assert e.event_id == 1
        assert e.event_type == "boot"
        assert e.severity == "info"

    def test_severity_override(self):
        e = CustomEvent(
            event_id=2,
            event_type="err",
            data={"k": 1},
            timestamp=0.0,
            severity="error",
        )
        assert e.severity == "error"


# ---------------------------------------------------------------------------
class TestAggregateDC:
    def test_basic(self):
        a = Aggregate(
            metric_name="cpu", count=3, sum=6.0, min=1.0, max=3.0, avg=2.0
        )
        assert a.metric_name == "cpu"
        assert a.count == 3
        assert a.avg == 2.0


# ---------------------------------------------------------------------------
class TestStartSpan:
    def test_returns_trace(self):
        o = DocObservability()
        t = o.start_span("op", now=1.0)
        assert isinstance(t, Trace)
        assert t.span_name == "op"
        assert t.start_at == 1.0
        assert t.end_at is None

    def test_unique_ids(self):
        o = DocObservability()
        t1 = o.start_span("a", now=1.0)
        t2 = o.start_span("b", now=1.0)
        assert t1.trace_id != t2.trace_id

    def test_parent_and_tags(self):
        o = DocObservability()
        t = o.start_span("op", parent_span_id="P", tags={"k": "v"}, now=1.0)
        assert t.parent_span_id == "P"
        assert t.tags == {"k": "v"}

    def test_recorded(self):
        o = DocObservability()
        o.start_span("op", now=1.0)
        assert o.total_traces == 1


# ---------------------------------------------------------------------------
class TestEndSpan:
    def test_ok(self):
        o = DocObservability()
        t = o.start_span("op", now=1.0)
        assert o.end_span(t.trace_id, now=2.0) is True
        assert t.end_at == 2.0
        assert t.duration_ms == pytest.approx(1000.0)

    def test_missing(self):
        o = DocObservability()
        assert o.end_span("nope", now=1.0) is False

    def test_idempotent_overwrite(self):
        o = DocObservability()
        t = o.start_span("op", now=1.0)
        o.end_span(t.trace_id, now=2.0)
        o.end_span(t.trace_id, now=3.0)
        assert t.end_at == 3.0


# ---------------------------------------------------------------------------
class TestRecordMetric:
    def test_default_gauge(self):
        o = DocObservability()
        m = o.record_metric("x", 1.0, now=1.0)
        assert m.metric_type is MetricType.GAUGE

    def test_explicit_type(self):
        o = DocObservability()
        m = o.record_metric("x", 1.0, MetricType.HISTOGRAM, now=1.0)
        assert m.metric_type is MetricType.HISTOGRAM

    def test_recorded(self):
        o = DocObservability()
        o.record_metric("x", 1.0, now=1.0)
        assert o.total_metrics == 1

    def test_tags_stored(self):
        o = DocObservability()
        m = o.record_metric("x", 1.0, tags={"a": 1}, now=1.0)
        assert m.tags == {"a": 1}


# ---------------------------------------------------------------------------
class TestIncrement:
    def test_default_value(self):
        o = DocObservability()
        m = o.increment("hits", now=1.0)
        assert m.value == 1.0
        assert m.metric_type is MetricType.COUNTER

    def test_custom_value(self):
        o = DocObservability()
        m = o.increment("hits", value=5.0, now=1.0)
        assert m.value == 5.0


# ---------------------------------------------------------------------------
class TestGauge:
    def test_type(self):
        o = DocObservability()
        m = o.gauge("g", 1.5, now=1.0)
        assert m.metric_type is MetricType.GAUGE
        assert m.value == 1.5


# ---------------------------------------------------------------------------
class TestHistogram:
    def test_type(self):
        o = DocObservability()
        m = o.histogram("h", 2.0, now=1.0)
        assert m.metric_type is MetricType.HISTOGRAM


# ---------------------------------------------------------------------------
class TestTiming:
    def test_type(self):
        o = DocObservability()
        m = o.timing("t", 12.0, now=1.0)
        assert m.metric_type is MetricType.TIMING


# ---------------------------------------------------------------------------
class TestRecordEvent:
    def test_basic(self):
        o = DocObservability()
        e = o.record_event("boot", data={"v": 1}, now=1.0)
        assert e.event_type == "boot"
        assert e.data == {"v": 1}
        assert e.severity == "info"

    def test_ids_increment(self):
        o = DocObservability()
        e1 = o.record_event("a", now=1.0)
        e2 = o.record_event("b", now=1.0)
        assert e2.event_id == e1.event_id + 1

    def test_severity(self):
        o = DocObservability()
        e = o.record_event("err", severity="error", now=1.0)
        assert e.severity == "error"


# ---------------------------------------------------------------------------
class TestTraces:
    def test_returns_all(self):
        o = DocObservability()
        for i in range(3):
            o.start_span(f"s{i}", now=float(i))
        assert len(o.traces()) == 3

    def test_limit(self):
        o = DocObservability()
        for i in range(5):
            o.start_span(f"s{i}", now=float(i))
        latest = o.traces(limit=2)
        assert len(latest) == 2
        assert latest[-1].span_name == "s4"


# ---------------------------------------------------------------------------
class TestMetrics:
    def test_filter_by_name(self):
        o = DocObservability()
        o.gauge("a", 1.0, now=1.0)
        o.gauge("b", 2.0, now=1.0)
        o.gauge("a", 3.0, now=1.0)
        assert len(o.metrics(name="a")) == 2

    def test_limit(self):
        o = DocObservability()
        for i in range(5):
            o.gauge("x", float(i), now=float(i))
        out = o.metrics(name="x", limit=2)
        assert len(out) == 2
        assert out[-1].value == 4.0


# ---------------------------------------------------------------------------
class TestEvents:
    def test_filter_by_type(self):
        o = DocObservability()
        o.record_event("a", now=1.0)
        o.record_event("b", now=1.0)
        assert len(o.events(event_type="a")) == 1

    def test_filter_by_severity(self):
        o = DocObservability()
        o.record_event("a", severity="info", now=1.0)
        o.record_event("a", severity="error", now=1.0)
        assert len(o.events(severity="error")) == 1

    def test_combined(self):
        o = DocObservability()
        o.record_event("x", severity="error", now=1.0)
        o.record_event("x", severity="info", now=1.0)
        o.record_event("y", severity="error", now=1.0)
        out = o.events(event_type="x", severity="error")
        assert len(out) == 1


# ---------------------------------------------------------------------------
class TestGetTrace:
    def test_found(self):
        o = DocObservability()
        t = o.start_span("op", now=1.0)
        assert o.get_trace(t.trace_id) is t

    def test_not_found(self):
        o = DocObservability()
        assert o.get_trace("nope") is None


# ---------------------------------------------------------------------------
class TestAggregateQuery:
    def test_empty(self):
        o = DocObservability()
        assert o.aggregate("nope") is None

    def test_basic_stats(self):
        o = DocObservability()
        for v in [1.0, 2.0, 3.0]:
            o.gauge("x", v, now=1.0)
        agg = o.aggregate("x")
        assert agg is not None
        assert agg.count == 3
        assert agg.sum == 6.0
        assert agg.min == 1.0
        assert agg.max == 3.0
        assert agg.avg == 2.0

    def test_time_range(self):
        o = DocObservability()
        o.gauge("x", 1.0, now=10.0)
        o.gauge("x", 2.0, now=20.0)
        o.gauge("x", 3.0, now=30.0)
        agg = o.aggregate("x", start=15.0, end=25.0)
        assert agg.count == 1
        assert agg.sum == 2.0

    def test_unbounded_start(self):
        o = DocObservability()
        o.gauge("x", 1.0, now=10.0)
        o.gauge("x", 2.0, now=20.0)
        agg = o.aggregate("x", end=15.0)
        assert agg.count == 1


# ---------------------------------------------------------------------------
class TestTimeSeries:
    def test_buckets(self):
        o = DocObservability()
        o.gauge("x", 1.0, now=1.0)
        o.gauge("x", 2.0, now=10.0)
        o.gauge("x", 3.0, now=70.0)
        ts = o.time_series("x", bucket_size=60.0)
        assert len(ts) == 2
        assert ts[0] == (0.0, 3.0)
        assert ts[1] == (60.0, 3.0)

    def test_empty(self):
        o = DocObservability()
        assert o.time_series("nope") == []

    def test_invalid_bucket_size(self):
        o = DocObservability()
        o.gauge("x", 1.0, now=1.0)
        assert o.time_series("x", bucket_size=0) == []


# ---------------------------------------------------------------------------
class TestUniqueMetricNames:
    def test_unique(self):
        o = DocObservability()
        o.gauge("a", 1.0, now=1.0)
        o.gauge("b", 1.0, now=1.0)
        o.gauge("a", 1.0, now=1.0)
        assert o.unique_metric_names() == {"a", "b"}

    def test_empty(self):
        o = DocObservability()
        assert o.unique_metric_names() == set()


# ---------------------------------------------------------------------------
class TestClear:
    def test_clears_all(self):
        o = DocObservability()
        o.start_span("op", now=1.0)
        o.gauge("x", 1.0, now=1.0)
        o.record_event("e", now=1.0)
        o.clear()
        assert o.total_traces == 0
        assert o.total_metrics == 0
        assert o.total_events == 0
        assert o.get_trace("any") is None

    def test_resets_event_ids(self):
        o = DocObservability()
        o.record_event("a", now=1.0)
        o.clear()
        e = o.record_event("a", now=1.0)
        assert e.event_id == 1


# ---------------------------------------------------------------------------
class TestTotalProperties:
    def test_traces(self):
        o = DocObservability()
        for i in range(3):
            o.start_span("s", now=float(i))
        assert o.total_traces == 3

    def test_metrics(self):
        o = DocObservability()
        for i in range(4):
            o.gauge("x", float(i), now=float(i))
        assert o.total_metrics == 4

    def test_events(self):
        o = DocObservability()
        for i in range(2):
            o.record_event("e", now=float(i))
        assert o.total_events == 2


# ---------------------------------------------------------------------------
class TestMaxLimits:
    def test_traces_eviction(self):
        o = DocObservability(max_traces=3)
        ids = [o.start_span(f"s{i}", now=float(i)).trace_id for i in range(5)]
        assert o.total_traces == 3
        # The first two should be evicted from both deque and lookup.
        assert o.get_trace(ids[0]) is None
        assert o.get_trace(ids[1]) is None
        assert o.get_trace(ids[4]) is not None

    def test_metrics_eviction(self):
        o = DocObservability(max_metrics=2)
        for i in range(5):
            o.gauge("x", float(i), now=float(i))
        assert o.total_metrics == 2

    def test_events_eviction(self):
        o = DocObservability(max_events=2)
        for i in range(5):
            o.record_event("e", now=float(i))
        assert o.total_events == 2


# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_thread_safety(self):
        o = DocObservability()

        def worker():
            for i in range(50):
                o.gauge("x", float(i), now=1.0)
                o.increment("hits", now=1.0)
                o.record_event("e", now=1.0)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert o.total_metrics == 4 * 50 * 2
        assert o.total_events == 4 * 50

    def test_tags_independent_per_call(self):
        o = DocObservability()
        shared = {"a": 1}
        m = o.gauge("x", 1.0, tags=shared, now=1.0)
        shared["a"] = 2
        assert m.tags == {"a": 1}

    def test_no_now_uses_time(self):
        o = DocObservability()
        m = o.gauge("x", 1.0)
        assert m.timestamp > 0.0

    def test_event_data_independent(self):
        o = DocObservability()
        data = {"v": 1}
        e = o.record_event("a", data=data, now=1.0)
        data["v"] = 99
        assert e.data == {"v": 1}

    def test_aggregate_single_point(self):
        o = DocObservability()
        o.gauge("x", 7.0, now=1.0)
        agg = o.aggregate("x")
        assert agg.min == agg.max == agg.avg == 7.0
        assert agg.count == 1

    def test_traces_limit_zero(self):
        o = DocObservability()
        o.start_span("s", now=1.0)
        assert o.traces(limit=0) == []
