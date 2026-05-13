"""Sliding window: time- or count-based windows, bucketed aggregation, statistics."""
from docstoolkit.sliding_window.window import WindowType, WindowConfig, SlidingWindow
from docstoolkit.sliding_window.aggregator import WindowAggregator
from docstoolkit.sliding_window.stats import WindowedStatistics

__all__ = [
    "WindowType",
    "WindowConfig",
    "SlidingWindow",
    "WindowAggregator",
    "WindowedStatistics",
]
