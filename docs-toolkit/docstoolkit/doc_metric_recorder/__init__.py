"""E333 DocMetricRecorder — record and aggregate per-document numeric metrics.

Public API
----------
:class:`MetricPoint`       — a single recorded metric data point
:class:`MetricSummary`     — aggregate summary for a metric on a doc
:class:`MetricStats`       — global aggregate statistics
:class:`DocMetricRecorder` — main interface for metric recording
"""

from .recorder import MetricPoint, MetricSummary, MetricStats, DocMetricRecorder

__all__ = ["MetricPoint", "MetricSummary", "MetricStats", "DocMetricRecorder"]
