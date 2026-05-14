"""metrics_collector — thread-safe, in-memory named metric collection.

Public surface
--------------
MetricType      — COUNTER / GAUGE / HISTOGRAM / TIMER enum
MetricSnapshot  — immutable snapshot of a single metric
MetricsCollector — store and query engine for all metrics
"""
from __future__ import annotations

from docstoolkit.metrics_collector.collector import (
    MetricSnapshot,
    MetricType,
    MetricsCollector,
)

__all__ = [
    "MetricType",
    "MetricSnapshot",
    "MetricsCollector",
]
