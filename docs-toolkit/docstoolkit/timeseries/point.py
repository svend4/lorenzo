"""Time series data point types for docs-toolkit."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Aggregation(Enum):
    """Aggregation functions for time windows."""

    MEAN = "mean"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    LAST = "last"


@dataclass
class DataPoint:
    """A single time series measurement.

    Attributes:
        ts:     Unix timestamp (seconds since epoch, fractional ok).
        value:  Numeric measurement value.
        tags:   Arbitrary key/value labels for the point.
        metric: Name of the metric this point belongs to.
    """

    ts: float
    value: float
    tags: dict[str, str] = field(default_factory=dict)
    metric: str = ""


@dataclass
class AggregatedPoint:
    """Result of aggregating DataPoints within a time window.

    Attributes:
        ts:     Start of the aggregation window (Unix timestamp).
        value:  Aggregated value for the window.
        count:  Number of raw points that contributed to the window.
        metric: Name of the metric.
    """

    ts: float
    value: float
    count: int
    metric: str = ""
