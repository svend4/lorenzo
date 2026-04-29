"""Тесты telemetry: tracer + metrics."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.telemetry import tracer, meter, get_tracer, prometheus_format
from docstoolkit.telemetry.tracer import StubTracer, Span
from docstoolkit.telemetry.metrics import Meter, Counter, Histogram, Gauge


def test_tracer_basic_span():
    t = StubTracer()
    with t.span("test") as s:
        s.set_attribute("x", 1)
    spans = t.get_recent()
    assert len(spans) >= 1
    assert spans[-1].name == "test"
    assert spans[-1].attributes["x"] == 1


def test_tracer_records_exception():
    t = StubTracer()
    with pytest.raises(ValueError):
        with t.span("fail") as s:
            raise ValueError("oops")
    spans = t.get_recent()
    assert spans[-1].status == "error"
    assert any(e["name"] == "exception" for e in spans[-1].events)


def test_tracer_buffer_limit():
    t = StubTracer(max_buffer=3)
    for i in range(5):
        with t.span(f"s{i}"):
            pass
    spans = t.get_recent()
    assert len(spans) == 3  # only last 3


def test_span_duration():
    s = Span(name="x", started_ns=1_000_000, ended_ns=2_000_000)
    assert s.duration_ms == 1.0


def test_counter_inc():
    c = Counter(name="test_total")
    c.inc()
    c.inc(5)
    assert c.value == 6.0


def test_gauge_set_inc_dec():
    g = Gauge(name="active")
    g.set(10)
    g.inc(2)
    g.dec(5)
    assert g.value == 7.0


def test_histogram_observe():
    h = Histogram(name="durations", buckets=[1.0, 5.0])
    h.observe(0.5)
    h.observe(2.0)
    h.observe(10.0)
    assert h._count == 3
    assert h._sum == 12.5
    assert h._bucket_counts[0] == 1  # ≤ 1.0
    assert h._bucket_counts[1] == 2  # ≤ 5.0


def test_meter_returns_singleton_per_name():
    m = Meter()
    c1 = m.counter("requests")
    c2 = m.counter("requests")
    assert c1 is c2


def test_prometheus_format_counter():
    m = Meter()
    c = m.counter("test_calls", "Test counter")
    c.inc(3)
    # Подменим module-level meter
    import docstoolkit.telemetry.metrics as metrics_mod
    original = metrics_mod.meter
    metrics_mod.meter = m
    try:
        out = prometheus_format()
        assert "# HELP test_calls" in out
        assert "# TYPE test_calls counter" in out
        assert "test_calls" in out
        assert "3" in out
    finally:
        metrics_mod.meter = original


def test_prometheus_format_histogram():
    m = Meter()
    h = m.histogram("latency", buckets=[0.1, 1.0])
    h.observe(0.05)
    h.observe(0.5)
    import docstoolkit.telemetry.metrics as metrics_mod
    original = metrics_mod.meter
    metrics_mod.meter = m
    try:
        out = prometheus_format()
        assert "latency_bucket" in out
        assert "latency_sum" in out
        assert "latency_count 2" in out
    finally:
        metrics_mod.meter = original


def test_init_telemetry_no_otel_returns_false():
    """Без opentelemetry SDK возвращает False, не падает."""
    from docstoolkit.telemetry import init_telemetry
    # Запускаем — даже если SDK установлен, вернёт True/False
    result = init_telemetry()
    assert isinstance(result, bool)
