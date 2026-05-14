"""Observability middleware: spans, traces, and metrics — pure stdlib."""

from docstoolkit.observability.span import Span, SpanStatus
from docstoolkit.observability.tracer import Trace, Tracer
from docstoolkit.observability.metrics import (
    Counter,
    Gauge,
    Histogram,
    MetricsRegistry,
)

__all__ = [
    "Span",
    "SpanStatus",
    "Trace",
    "Tracer",
    "Counter",
    "Gauge",
    "Histogram",
    "MetricsRegistry",
]
