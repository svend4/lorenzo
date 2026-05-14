"""High-level monitor that tracks multiple named metric series — pure stdlib."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from docstoolkit.anomaly.detector import Anomaly, AnomalyConfig, AnomalyDetector


@dataclass(frozen=True)
class MetricSeries:
    """Immutable snapshot of a named metric series."""

    name: str
    values: List[float] = field(default_factory=list)
    timestamps: List[float] = field(default_factory=list)

    def latest(self) -> Optional[float]:
        """Return the most recently added value, or None if the series is empty."""
        if self.values:
            return self.values[-1]
        return None

    def add(self, value: float, ts: Optional[float] = None) -> "MetricSeries":
        """Return a *new* MetricSeries with *value* (and optional *ts*) appended."""
        if ts is None:
            ts = time.time()
        return MetricSeries(
            name=self.name,
            values=list(self.values) + [value],
            timestamps=list(self.timestamps) + [ts],
        )


class AnomalyMonitor:
    """Stateful monitor that tracks multiple named series and accumulates anomalies."""

    def __init__(self, config: Optional[AnomalyConfig] = None) -> None:
        self._config = config or AnomalyConfig()
        self._detector = AnomalyDetector(self._config)
        self._series: Dict[str, MetricSeries] = {}
        self._anomalies: List[Anomaly] = []

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_point(
        self,
        series_name: str,
        value: float,
        ts: Optional[float] = None,
    ) -> List[Anomaly]:
        """Append *value* to the named series and return any new anomalies found.

        Anomaly detection is re-run on the full series after each new point.
        Only anomalies whose timestamp matches the newly added point are
        considered "new" and returned from this call, but all anomalies for
        the series are tracked internally.
        """
        if ts is None:
            ts = time.time()

        # Update (or create) the series
        series = self._series.get(series_name) or MetricSeries(name=series_name)
        series = series.add(value, ts)
        self._series[series_name] = series

        # Re-detect on full series history
        detected = self._detector.detect(series.values, series.timestamps)

        # Identify which anomalies are "new" (matching this timestamp)
        new_anomalies = [a for a in detected if a.ts == ts]

        # Merge new anomalies into global store (avoid duplicates by ts+type+value)
        existing_keys = {(a.ts, a.anomaly_type, a.value) for a in self._anomalies}
        for anomaly in new_anomalies:
            key = (anomaly.ts, anomaly.anomaly_type, anomaly.value)
            if key not in existing_keys:
                self._anomalies.append(anomaly)
                existing_keys.add(key)

        return new_anomalies

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_series(self, series_name: str) -> Optional[MetricSeries]:
        """Return the MetricSeries for *series_name*, or None if not found."""
        return self._series.get(series_name)

    def all_anomalies(self) -> List[Anomaly]:
        """Return all anomalies detected across all series, sorted by timestamp."""
        return sorted(self._anomalies, key=lambda a: a.ts)

    def series_names(self) -> List[str]:
        """Return the names of all tracked series in insertion order."""
        return list(self._series.keys())
