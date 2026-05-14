"""E437 DocMetricWindow — sliding window metric aggregation.

Public API
----------
:class:`WindowPoint`     — a single data point in a window
:class:`WindowStats`     — aggregate stats for a window
:class:`MetricStats`     — global statistics
:class:`DocMetricWindow` — main interface for window metric aggregation
"""

from .window import WindowPoint, WindowStats, MetricStats, DocMetricWindow

__all__ = ["WindowPoint", "WindowStats", "MetricStats", "DocMetricWindow"]
