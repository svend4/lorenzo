"""E21 Anomaly detection module — pure stdlib, no external dependencies."""
from docstoolkit.anomaly.stats import RunningStats, moving_average, ewma
from docstoolkit.anomaly.detector import (
    AnomalyType,
    Anomaly,
    AnomalyConfig,
    AnomalyDetector,
)
from docstoolkit.anomaly.monitor import MetricSeries, AnomalyMonitor

__all__ = [
    # stats
    "RunningStats",
    "moving_average",
    "ewma",
    # detector
    "AnomalyType",
    "Anomaly",
    "AnomalyConfig",
    "AnomalyDetector",
    # monitor
    "MetricSeries",
    "AnomalyMonitor",
]
