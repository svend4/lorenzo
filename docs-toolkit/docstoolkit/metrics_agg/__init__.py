"""metrics_agg — in-memory metrics aggregation for docs-toolkit.

Public surface
--------------
MetricType       — COUNTER / GAUGE / HISTOGRAM / SUMMARY enum
MetricSample     — single recorded measurement
MetricFamily     — named collection of samples with helpers
AggregationWindow — time-bounded slice with statistical methods
MetricsAggregator — store + query engine
MetricsReport    — snapshot dataclass with text/JSON export
MetricsReporter  — builds reports from an aggregator
"""
from __future__ import annotations

from docstoolkit.metrics_agg.metric import (
    MetricFamily,
    MetricSample,
    MetricType,
)
from docstoolkit.metrics_agg.aggregator import (
    AggregationWindow,
    MetricsAggregator,
)
from docstoolkit.metrics_agg.reporter import (
    MetricsReport,
    MetricsReporter,
)

__all__ = [
    "MetricType",
    "MetricSample",
    "MetricFamily",
    "AggregationWindow",
    "MetricsAggregator",
    "MetricsReport",
    "MetricsReporter",
]
