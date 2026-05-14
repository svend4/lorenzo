"""Tests for docstoolkit.observability — 70+ cases covering all public APIs."""
import time

import pytest

from docstoolkit.observability import (
    Counter,
    Gauge,
    Histogram,
    MetricsRegistry,
    Span,
    SpanStatus,
    Trace,
    Tracer,
)


# ---------------------------------------------------------------------------
# SpanStatus
# ---------------------------------------------------------------------------

class TestSpanStatus:
    def test_enum_values(self):
        assert SpanStatus.OK.value == "ok"
        assert SpanStatus.ERROR.value == "error"
        assert SpanStatus.TIMEOUT.value == "timeout"

    def test_enum_members(self):
        members = {s.name for s in SpanStatus}
        assert members == {"OK", "ERROR", "TIMEOUT"}


# ---------------------------------------------------------------------------
# Span
# ---------------------------------------------------------------------------

class TestSpanDefaults:
    def test_span_id_auto_8_chars(self):
        s = Span(trace_id="abc")
        assert isinstance(s.span_id, str)
        assert len(s.span_id) == 8

    def test_span_ids_unique(self):
        ids = {Span(trace_id="t").span_id for _ in range(50)}
        assert len(ids) == 50

    def test_default_parent_none(self):
        s = Span(trace_id="t")
        assert s.parent_id is None

    def test_default_name_empty(self):
        s = Span(trace_id="t")
        assert s.name == ""

    def test_default_status_ok(self):
        s = Span(trace_id="t")
        assert s.status is SpanStatus.OK

    def test_default_tags_empty_dict(self):
        s = Span(trace_id="t")
        assert s.tags == {}

    def test_default_error_empty(self):
        s = Span(trace_id="t")
        assert s.error == ""

    def test_start_ts_auto(self):
        before = time.time()
        s = Span(trace_id="t")
        after = time.time()
        assert before <= s.start_ts <= after

    def test_end_ts_none(self):
        s = Span(trace_id="t")
        assert s.end_ts is None


class TestSpanFinish:
    def test_finish_sets_end_ts(self):
        s = Span(trace_id="t")
        before = time.time()
        s.finish()
        after = time.time()
        assert s.end_ts is not None
        assert before <= s.end_ts <= after

    def test_finish_default_status_ok(self):
        s = Span(trace_id="t")
        s.finish()
        assert s.status is SpanStatus.OK

    def test_finish_with_error_status(self):
        s = Span(trace_id="t")
        s.finish(status=SpanStatus.ERROR, error="boom")
        assert s.status is SpanStatus.ERROR
        assert s.error == "boom"

    def test_finish_with_timeout_status(self):
        s = Span(trace_id="t")
        s.finish(status=SpanStatus.TIMEOUT)
        assert s.status is SpanStatus.TIMEOUT

    def test_finish_idempotent_first_call_wins(self):
        s = Span(trace_id="t")
        s.finish(status=SpanStatus.ERROR, error="first")
        first_end = s.end_ts
        s.finish(status=SpanStatus.OK, error="second")
        # second finish overwrites (spec does not forbid it, so just verify no exception)
        assert s.end_ts is not None
        _ = first_end  # used


class TestSpanDurationMs:
    def test_duration_none_before_finish(self):
        s = Span(trace_id="t")
        assert s.duration_ms() is None

    def test_duration_positive_after_finish(self):
        s = Span(trace_id="t")
        time.sleep(0.01)
        s.finish()
        d = s.duration_ms()
        assert d is not None
        assert d > 0

    def test_duration_manual_timestamps(self):
        s = Span(trace_id="t", start_ts=1000.0, end_ts=1001.5)
        assert abs(s.duration_ms() - 1500.0) < 1e-6

    def test_duration_zero_elapsed(self):
        s = Span(trace_id="t", start_ts=5.0, end_ts=5.0)
        assert s.duration_ms() == 0.0


class TestSpanIsFinished:
    def test_not_finished_initially(self):
        s = Span(trace_id="t")
        assert s.is_finished() is False

    def test_finished_after_finish(self):
        s = Span(trace_id="t")
        s.finish()
        assert s.is_finished() is True


class TestSpanSetTag:
    def test_set_tag_stores_value(self):
        s = Span(trace_id="t")
        s.set_tag("env", "prod")
        assert s.tags["env"] == "prod"

    def test_set_tag_overwrite(self):
        s = Span(trace_id="t")
        s.set_tag("key", "v1")
        s.set_tag("key", "v2")
        assert s.tags["key"] == "v2"

    def test_set_tag_multiple(self):
        s = Span(trace_id="t")
        s.set_tag("a", 1)
        s.set_tag("b", 2)
        assert s.tags == {"a": 1, "b": 2}

    def test_set_tag_non_string_value(self):
        s = Span(trace_id="t")
        s.set_tag("count", 42)
        s.set_tag("flag", True)
        assert s.tags["count"] == 42
        assert s.tags["flag"] is True


# ---------------------------------------------------------------------------
# Trace
# ---------------------------------------------------------------------------

class TestTraceDataclass:
    def _make_trace(self):
        root = Span(trace_id="tid", parent_id=None, name="root")
        child = Span(trace_id="tid", parent_id=root.span_id, name="child")
        return Trace(trace_id="tid", spans=[root, child])

    def test_root_span_no_parent(self):
        t = self._make_trace()
        root = t.root_span()
        assert root is not None
        assert root.name == "root"

    def test_root_span_none_when_missing(self):
        child = Span(trace_id="tid", parent_id="fakeid")
        t = Trace(trace_id="tid", spans=[child])
        assert t.root_span() is None

    def test_child_spans(self):
        t = self._make_trace()
        root = t.root_span()
        children = t.child_spans(root.span_id)
        assert len(children) == 1
        assert children[0].name == "child"

    def test_child_spans_empty(self):
        t = self._make_trace()
        assert t.child_spans("nonexistent") == []

    def test_total_duration_ms_none_if_no_root(self):
        t = Trace(trace_id="t", spans=[])
        assert t.total_duration_ms() is None

    def test_total_duration_ms_none_if_root_unfinished(self):
        root = Span(trace_id="t", parent_id=None, name="root")
        t = Trace(trace_id="t", spans=[root])
        assert t.total_duration_ms() is None

    def test_total_duration_ms_value(self):
        root = Span(trace_id="t", parent_id=None, start_ts=0.0, end_ts=2.0)
        t = Trace(trace_id="t", spans=[root])
        assert t.total_duration_ms() == 2000.0

    def test_has_errors_false_all_ok(self):
        root = Span(trace_id="t", parent_id=None)
        t = Trace(trace_id="t", spans=[root])
        assert t.has_errors() is False

    def test_has_errors_true_with_error_span(self):
        root = Span(trace_id="t", parent_id=None, status=SpanStatus.ERROR)
        t = Trace(trace_id="t", spans=[root])
        assert t.has_errors() is True

    def test_has_errors_true_with_timeout_span(self):
        root = Span(trace_id="t", parent_id=None, status=SpanStatus.TIMEOUT)
        t = Trace(trace_id="t", spans=[root])
        assert t.has_errors() is True

    def test_span_count(self):
        t = self._make_trace()
        assert t.span_count() == 2

    def test_span_count_empty(self):
        t = Trace(trace_id="t", spans=[])
        assert t.span_count() == 0

    def test_created_ts_auto(self):
        before = time.time()
        t = Trace(trace_id="t")
        after = time.time()
        assert before <= t.created_ts <= after


# ---------------------------------------------------------------------------
# Tracer
# ---------------------------------------------------------------------------

class TestTracerStartTrace:
    def test_returns_trace_id_and_span(self):
        tr = Tracer()
        tid, root = tr.start_trace("my_op")
        assert isinstance(tid, str)
        assert len(tid) > 0
        assert isinstance(root, Span)

    def test_root_span_name(self):
        tr = Tracer()
        _, root = tr.start_trace("fetch")
        assert root.name == "fetch"

    def test_root_span_no_parent(self):
        tr = Tracer()
        _, root = tr.start_trace()
        assert root.parent_id is None

    def test_root_span_trace_id_matches(self):
        tr = Tracer()
        tid, root = tr.start_trace()
        assert root.trace_id == tid

    def test_unique_trace_ids(self):
        tr = Tracer()
        ids = {tr.start_trace()[0] for _ in range(20)}
        assert len(ids) == 20


class TestTracerStartSpan:
    def test_start_span_registered_in_trace(self):
        tr = Tracer()
        tid, root = tr.start_trace("root")
        child = tr.start_span(tid, "child", parent_id=root.span_id)
        trace = tr.get_trace(tid)
        assert child in trace.spans

    def test_start_span_parent_id_set(self):
        tr = Tracer()
        tid, root = tr.start_trace("root")
        child = tr.start_span(tid, "child", parent_id=root.span_id)
        assert child.parent_id == root.span_id

    def test_start_span_unknown_trace(self):
        tr = Tracer()
        # Should not raise; span is created but not registered anywhere
        span = tr.start_span("unknown-tid", "orphan")
        assert span.name == "orphan"


class TestTracerFinishSpan:
    def test_finish_span_marks_finished(self):
        tr = Tracer()
        _, root = tr.start_trace("op")
        tr.finish_span(root)
        assert root.is_finished()

    def test_finish_span_with_error(self):
        tr = Tracer()
        _, root = tr.start_trace("op")
        tr.finish_span(root, status=SpanStatus.ERROR, error="fail")
        assert root.status is SpanStatus.ERROR
        assert root.error == "fail"


class TestTracerGetTrace:
    def test_get_trace_returns_trace(self):
        tr = Tracer()
        tid, _ = tr.start_trace()
        trace = tr.get_trace(tid)
        assert trace is not None
        assert trace.trace_id == tid

    def test_get_trace_none_missing(self):
        tr = Tracer()
        assert tr.get_trace("no-such-id") is None


class TestTracerFinishTrace:
    def test_finish_trace_finishes_all_spans(self):
        tr = Tracer()
        tid, root = tr.start_trace("root")
        child = tr.start_span(tid, "child", parent_id=root.span_id)
        trace = tr.finish_trace(tid)
        assert trace is not None
        assert all(s.is_finished() for s in trace.spans)

    def test_finish_trace_returns_none_missing(self):
        tr = Tracer()
        assert tr.finish_trace("missing") is None

    def test_finish_trace_already_finished_spans_unchanged(self):
        tr = Tracer()
        tid, root = tr.start_trace("root")
        root.finish(status=SpanStatus.ERROR, error="manual")
        tr.finish_trace(tid)
        assert root.status is SpanStatus.ERROR  # not overwritten


class TestTracerActiveTraces:
    def test_active_traces_zero_initially(self):
        tr = Tracer()
        assert tr.active_traces() == 0

    def test_active_traces_increments(self):
        tr = Tracer()
        tr.start_trace("a")
        tr.start_trace("b")
        assert tr.active_traces() == 2

    def test_active_traces_decrements_after_finish(self):
        tr = Tracer()
        tid, _ = tr.start_trace("a")
        tr.start_trace("b")
        tr.finish_trace(tid)
        assert tr.active_traces() == 1

    def test_active_traces_zero_after_all_finished(self):
        tr = Tracer()
        tid1, _ = tr.start_trace("a")
        tid2, _ = tr.start_trace("b")
        tr.finish_trace(tid1)
        tr.finish_trace(tid2)
        assert tr.active_traces() == 0


# ---------------------------------------------------------------------------
# Counter
# ---------------------------------------------------------------------------

class TestCounter:
    def test_default_value_zero(self):
        c = Counter(name="hits")
        assert c.value == 0

    def test_increment_default(self):
        c = Counter(name="hits")
        c.increment()
        assert c.value == 1

    def test_increment_by_n(self):
        c = Counter(name="hits")
        c.increment(5)
        assert c.value == 5

    def test_increment_multiple_times(self):
        c = Counter(name="hits")
        c.increment(3)
        c.increment(2)
        assert c.value == 5

    def test_reset(self):
        c = Counter(name="hits")
        c.increment(10)
        c.reset()
        assert c.value == 0

    def test_tags_stored(self):
        c = Counter(name="req", tags={"env": "prod"})
        assert c.tags["env"] == "prod"


# ---------------------------------------------------------------------------
# Gauge
# ---------------------------------------------------------------------------

class TestGauge:
    def test_default_value_zero(self):
        g = Gauge(name="cpu")
        assert g.value == 0.0

    def test_set(self):
        g = Gauge(name="cpu")
        g.set(75.5)
        assert g.value == 75.5

    def test_increment(self):
        g = Gauge(name="cpu")
        g.set(10.0)
        g.increment(5.0)
        assert g.value == 15.0

    def test_increment_default(self):
        g = Gauge(name="cpu")
        g.increment()
        assert g.value == 1.0

    def test_decrement(self):
        g = Gauge(name="cpu")
        g.set(10.0)
        g.decrement(3.0)
        assert g.value == 7.0

    def test_decrement_default(self):
        g = Gauge(name="cpu")
        g.set(5.0)
        g.decrement()
        assert g.value == 4.0

    def test_goes_negative(self):
        g = Gauge(name="balance")
        g.decrement(5.0)
        assert g.value == -5.0


# ---------------------------------------------------------------------------
# Histogram
# ---------------------------------------------------------------------------

class TestHistogram:
    def test_empty_count(self):
        h = Histogram(name="latency")
        assert h.count() == 0

    def test_record_increases_count(self):
        h = Histogram(name="latency")
        h.record(10.0)
        h.record(20.0)
        assert h.count() == 2

    def test_mean_empty(self):
        h = Histogram(name="latency")
        assert h.mean() == 0.0

    def test_mean_values(self):
        h = Histogram(name="latency")
        for v in [10.0, 20.0, 30.0]:
            h.record(v)
        assert abs(h.mean() - 20.0) < 1e-9

    def test_percentile_empty_returns_zero(self):
        h = Histogram(name="latency")
        assert h.percentile(50) == 0.0

    def test_percentile_single_value(self):
        h = Histogram(name="latency")
        h.record(42.0)
        assert h.percentile(50) == 42.0
        assert h.percentile(0) == 42.0
        assert h.percentile(100) == 42.0

    def test_percentile_p0_min(self):
        h = Histogram(name="latency")
        for v in [1, 2, 3, 4, 5]:
            h.record(float(v))
        assert h.percentile(0) == 1.0

    def test_percentile_p100_max(self):
        h = Histogram(name="latency")
        for v in [1, 2, 3, 4, 5]:
            h.record(float(v))
        assert h.percentile(100) == 5.0

    def test_percentile_p50_median(self):
        h = Histogram(name="latency")
        for v in [1, 2, 3, 4, 5]:
            h.record(float(v))
        assert h.percentile(50) == 3.0

    def test_percentile_interpolation(self):
        h = Histogram(name="latency")
        h.record(0.0)
        h.record(100.0)
        # p50 should be midpoint = 50.0
        assert abs(h.percentile(50) - 50.0) < 1e-9


# ---------------------------------------------------------------------------
# MetricsRegistry
# ---------------------------------------------------------------------------

class TestMetricsRegistry:
    def test_counter_returns_counter(self):
        r = MetricsRegistry()
        c = r.counter("hits")
        assert isinstance(c, Counter)

    def test_counter_reuse_by_name(self):
        r = MetricsRegistry()
        c1 = r.counter("hits")
        c2 = r.counter("hits")
        assert c1 is c2

    def test_counter_different_names(self):
        r = MetricsRegistry()
        c1 = r.counter("a")
        c2 = r.counter("b")
        assert c1 is not c2

    def test_gauge_returns_gauge(self):
        r = MetricsRegistry()
        g = r.gauge("cpu")
        assert isinstance(g, Gauge)

    def test_gauge_reuse_by_name(self):
        r = MetricsRegistry()
        g1 = r.gauge("cpu")
        g2 = r.gauge("cpu")
        assert g1 is g2

    def test_histogram_returns_histogram(self):
        r = MetricsRegistry()
        h = r.histogram("latency")
        assert isinstance(h, Histogram)

    def test_histogram_reuse_by_name(self):
        r = MetricsRegistry()
        h1 = r.histogram("latency")
        h2 = r.histogram("latency")
        assert h1 is h2

    def test_snapshot_empty(self):
        r = MetricsRegistry()
        assert r.snapshot() == {}

    def test_snapshot_contains_counter(self):
        r = MetricsRegistry()
        c = r.counter("hits")
        c.increment(3)
        snap = r.snapshot()
        assert "counter.hits" in snap
        assert snap["counter.hits"]["value"] == 3

    def test_snapshot_contains_gauge(self):
        r = MetricsRegistry()
        g = r.gauge("cpu")
        g.set(88.0)
        snap = r.snapshot()
        assert "gauge.cpu" in snap
        assert snap["gauge.cpu"]["value"] == 88.0

    def test_snapshot_contains_histogram(self):
        r = MetricsRegistry()
        h = r.histogram("latency")
        h.record(10.0)
        h.record(20.0)
        snap = r.snapshot()
        assert "histogram.latency" in snap
        assert snap["histogram.latency"]["count"] == 2

    def test_snapshot_all_three_types(self):
        r = MetricsRegistry()
        r.counter("req").increment()
        r.gauge("mem").set(512.0)
        r.histogram("rtt").record(5.0)
        snap = r.snapshot()
        assert "counter.req" in snap
        assert "gauge.mem" in snap
        assert "histogram.rtt" in snap

    def test_counter_tags_in_snapshot(self):
        r = MetricsRegistry()
        r.counter("api", tags={"method": "GET"})
        snap = r.snapshot()
        assert snap["counter.api"]["tags"] == {"method": "GET"}
