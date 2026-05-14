"""E204 Document statistics — aggregated stats over collections with grouping, comparison, percentiles.

Public API
----------
:class:`MetricType`       — enum of supported metric types
:class:`DocStat`          — single computed statistic
:class:`GroupedStats`     — grouped statistics result
:class:`Distribution`     — histogram-based distribution
:class:`ComparisonResult` — comparison between two collections
:class:`DocStats`         — main statistics engine
"""
from .stats import (
    ComparisonResult,
    Distribution,
    DocStat,
    DocStats,
    GroupedStats,
    MetricType,
)

__all__ = [
    "ComparisonResult",
    "Distribution",
    "DocStat",
    "DocStats",
    "GroupedStats",
    "MetricType",
]
