"""Anomaly detector — pure stdlib, no external deps."""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from docstoolkit.anomaly.stats import RunningStats


class AnomalyType(Enum):
    SPIKE = "spike"
    DROP = "drop"
    DRIFT = "drift"
    OUTLIER = "outlier"


@dataclass
class Anomaly:
    anomaly_type: AnomalyType
    value: float
    expected: float
    deviation: float  # z-score or normalised distance
    ts: float
    description: str

    def severity(self) -> str:
        """Severity bucket based on absolute deviation magnitude."""
        abs_dev = abs(self.deviation)
        if abs_dev < 2:
            return "low"
        if abs_dev < 3:
            return "medium"
        return "high"


@dataclass
class AnomalyConfig:
    z_threshold: float = 2.5
    drift_window: int = 10
    min_samples: int = 5


class AnomalyDetector:
    """Detect anomalies in a univariate time series using simple statistics."""

    def __init__(self, config: Optional[AnomalyConfig] = None) -> None:
        self.config = config or AnomalyConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def detect(
        self,
        values: List[float],
        timestamps: Optional[List[float]] = None,
    ) -> List[Anomaly]:
        """Return anomalies found in *values*.

        Parameters
        ----------
        values:
            Ordered sequence of metric readings.
        timestamps:
            Optional parallel list of Unix timestamps.  When omitted, integer
            indices 0, 1, 2 … are used.
        """
        cfg = self.config
        if len(values) < cfg.min_samples:
            return []

        if timestamps is None:
            timestamps = list(range(len(values)))
        if len(timestamps) != len(values):
            raise ValueError("values and timestamps must have the same length")

        anomalies: List[Anomaly] = []
        flagged: set = set()  # indices already flagged to avoid double-reporting

        # ---- 1. Z-score based SPIKE / DROP ---------------------------------
        stats = RunningStats()
        for v in values:
            stats = stats.update(v)

        for i, (v, ts) in enumerate(zip(values, timestamps)):
            z = stats.z_score(v)
            if z > cfg.z_threshold:
                anomalies.append(
                    Anomaly(
                        anomaly_type=AnomalyType.SPIKE,
                        value=v,
                        expected=stats.mean,
                        deviation=z,
                        ts=ts,
                        description=(
                            f"Spike detected: value {v:.4g} is {z:.2f} std "
                            f"above mean {stats.mean:.4g}"
                        ),
                    )
                )
                flagged.add(i)
            elif z < -cfg.z_threshold:
                anomalies.append(
                    Anomaly(
                        anomaly_type=AnomalyType.DROP,
                        value=v,
                        expected=stats.mean,
                        deviation=z,
                        ts=ts,
                        description=(
                            f"Drop detected: value {v:.4g} is {abs(z):.2f} std "
                            f"below mean {stats.mean:.4g}"
                        ),
                    )
                )
                flagged.add(i)

        # ---- 2. DRIFT: sliding window comparison ---------------------------
        w = cfg.drift_window
        if len(values) >= w:
            for end in range(w, len(values) + 1):
                window = values[end - w : end]
                half = w // 2
                first_half = window[:half]
                second_half = window[half:]
                mean1 = sum(first_half) / len(first_half)
                mean2 = sum(second_half) / len(second_half)
                diff = abs(mean2 - mean1)
                if stats.std() > 0 and diff > stats.std():
                    idx = end - 1  # flag the last index in the window
                    if idx not in flagged:
                        deviation = (mean2 - mean1) / stats.std()
                        anomalies.append(
                            Anomaly(
                                anomaly_type=AnomalyType.DRIFT,
                                value=values[idx],
                                expected=mean1,
                                deviation=deviation,
                                ts=timestamps[idx],
                                description=(
                                    f"Drift detected over window of {w}: "
                                    f"mean shifted from {mean1:.4g} to {mean2:.4g} "
                                    f"(diff {diff:.4g} > 1 std)"
                                ),
                            )
                        )
                        flagged.add(idx)

        # ---- 3. OUTLIER: IQR method for unflagged points -------------------
        sorted_vals = sorted(values)
        q1 = self._percentile(sorted_vals, 25.0)
        q3 = self._percentile(sorted_vals, 75.0)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        for i, (v, ts) in enumerate(zip(values, timestamps)):
            if i in flagged:
                continue
            if v < lower or v > upper:
                median = self._percentile(sorted_vals, 50.0)
                deviation = (v - median) / (iqr if iqr > 0 else 1.0)
                anomalies.append(
                    Anomaly(
                        anomaly_type=AnomalyType.OUTLIER,
                        value=v,
                        expected=median,
                        deviation=deviation,
                        ts=ts,
                        description=(
                            f"Outlier detected: value {v:.4g} outside IQR bounds "
                            f"[{lower:.4g}, {upper:.4g}]"
                        ),
                    )
                )
                flagged.add(i)

        # Sort by timestamp for deterministic output
        anomalies.sort(key=lambda a: a.ts)
        return anomalies

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _percentile(values: List[float], p: float) -> float:
        """Compute percentile *p* (0–100) with linear interpolation.

        *values* must be sorted in ascending order.
        """
        if not values:
            return 0.0
        n = len(values)
        if n == 1:
            return values[0]
        # Convert percentile to a 0-based fractional index
        index = (p / 100.0) * (n - 1)
        lower_idx = int(math.floor(index))
        upper_idx = int(math.ceil(index))
        if lower_idx == upper_idx:
            return values[lower_idx]
        frac = index - lower_idx
        return values[lower_idx] * (1 - frac) + values[upper_idx] * frac
