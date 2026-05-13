"""Time series store for docs-toolkit.

Provides an SQLite-backed append-only store for numeric time series data,
with support for tag-based filtering and window aggregation.

Example::

    from docstoolkit.timeseries import (
        DataPoint, Aggregation, AggregatedPoint,
        TimeSeriesConfig, TimeSeriesStore,
    )

    store = TimeSeriesStore()
    store.write(DataPoint(ts=1_000_000.0, value=42.0, metric="cpu"))
    points = store.read("cpu")
    agg = store.aggregate("cpu", Aggregation.MEAN, window_seconds=60.0)
    store.close()
"""
from docstoolkit.timeseries.point import Aggregation, AggregatedPoint, DataPoint
from docstoolkit.timeseries.store import TimeSeriesConfig, TimeSeriesStore

__all__ = [
    "DataPoint",
    "Aggregation",
    "AggregatedPoint",
    "TimeSeriesConfig",
    "TimeSeriesStore",
]
