"""Telemetry: OpenTelemetry traces + Prometheus metrics export.

3 уровня:
  1. Stub (default) — no-op, чтобы код не ломался
  2. OTel SDK — если установлено opentelemetry-api/sdk
  3. Prometheus exposition format — для /metrics endpoint

Использование:
    from docstoolkit.telemetry import tracer, meter, init_telemetry

    init_telemetry(otlp_endpoint="http://jaeger:4317")

    with tracer.span("rag.ask"):
        meter.counter("rag.requests").inc(1)
        result = ask(question)

В production — opentelemetry-instrument автоматически экспортит.
"""
from docstoolkit.telemetry.tracer import (
    tracer, init_telemetry, get_tracer, Span,
)
from docstoolkit.telemetry.metrics import (
    meter, Counter, Histogram, Gauge, prometheus_format,
)

__all__ = [
    "tracer", "init_telemetry", "get_tracer", "Span",
    "meter", "Counter", "Histogram", "Gauge", "prometheus_format",
]
