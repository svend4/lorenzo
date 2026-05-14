"""Aggregation windows and MetricsAggregator for the metrics aggregator."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.metrics_agg.metric import MetricSample, MetricType


@dataclass
class AggregationWindow:
    """A time-bounded slice of metric samples.

    Attributes:
        start_ts: Start of the window (inclusive), Unix timestamp.
        end_ts:   End of the window (inclusive), Unix timestamp.
        samples:  All samples that fall within [start_ts, end_ts].
    """

    start_ts: float
    end_ts: float
    samples: list[MetricSample] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Aggregation helpers
    # ------------------------------------------------------------------

    def _values(self) -> list[float]:
        return [s.value for s in self.samples]

    def mean(self) -> float:
        """Arithmetic mean of all sample values; 0.0 for empty window."""
        vals = self._values()
        if not vals:
            return 0.0
        return sum(vals) / len(vals)

    def sum_(self) -> float:
        """Sum of all sample values; 0.0 for empty window."""
        return sum(self._values())

    def min_(self) -> float:
        """Minimum sample value; 0.0 for empty window."""
        vals = self._values()
        if not vals:
            return 0.0
        return min(vals)

    def max_(self) -> float:
        """Maximum sample value; 0.0 for empty window."""
        vals = self._values()
        if not vals:
            return 0.0
        return max(vals)

    def count(self) -> int:
        """Number of samples in the window."""
        return len(self.samples)

    def percentile(self, p: float) -> float:
        """Linear-interpolation percentile of sample values.

        Args:
            p: Percentile in [0, 100].  p=0 → min; p=100 → max.

        Returns:
            Interpolated percentile value.

        Raises:
            ValueError: If the window contains no samples.
        """
        vals = sorted(self._values())
        n = len(vals)
        if n == 0:
            raise ValueError("Cannot compute percentile of an empty window")
        if p <= 0:
            return vals[0]
        if p >= 100:
            return vals[-1]
        # Linear interpolation (same as numpy's default)
        rank = (p / 100.0) * (n - 1)
        lower = int(rank)
        upper = lower + 1
        if upper >= n:
            return vals[-1]
        frac = rank - lower
        return vals[lower] + frac * (vals[upper] - vals[lower])


class MetricsAggregator:
    """In-memory store and aggregation engine for metric samples.

    All samples are retained in insertion order; no automatic eviction
    is performed.  Use :meth:`window` to obtain a time-bounded slice.
    """

    def __init__(self) -> None:
        # list of all recorded samples in insertion order
        self._samples: list[MetricSample] = []

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def record(self, sample: MetricSample) -> None:
        """Append *sample* to the internal store.

        Args:
            sample: The :class:`MetricSample` to record.
        """
        self._samples.append(sample)

    # ------------------------------------------------------------------
    # Reading / querying
    # ------------------------------------------------------------------

    def names(self) -> list[str]:
        """Return distinct metric names in the order first seen.

        Returns:
            Ordered list of unique metric names.
        """
        seen: dict[str, None] = {}
        for s in self._samples:
            seen[s.name] = None
        return list(seen.keys())

    def label_values(self, name: str, label_key: str) -> list[str]:
        """Distinct values for *label_key* across all samples of *name*.

        Args:
            name:      Metric name to filter by.
            label_key: Label key whose values are enumerated.

        Returns:
            Ordered (first-seen) list of distinct label values.
        """
        seen: dict[str, None] = {}
        for s in self._samples:
            if s.name == name and label_key in s.labels:
                seen[s.labels[label_key]] = None
        return list(seen.keys())

    def window(
        self,
        name: str,
        start_ts: float,
        end_ts: float,
        labels: Optional[dict] = None,
    ) -> AggregationWindow:
        """Return an :class:`AggregationWindow` for samples matching the criteria.

        Only samples whose timestamp is in ``[start_ts, end_ts]`` are
        included.  If *labels* is provided every key/value pair must
        match the sample's label set (subset match).

        Args:
            name:     Metric name to filter by.
            start_ts: Window start timestamp (inclusive).
            end_ts:   Window end timestamp (inclusive).
            labels:   Optional label filter (all pairs must match).

        Returns:
            :class:`AggregationWindow` containing matching samples.
        """
        matching: list[MetricSample] = []
        for s in self._samples:
            if s.name != name:
                continue
            if not (start_ts <= s.ts <= end_ts):
                continue
            if labels is not None:
                if not all(s.labels.get(k) == v for k, v in labels.items()):
                    continue
            matching.append(s)
        return AggregationWindow(start_ts=start_ts, end_ts=end_ts, samples=matching)

    def rate(
        self,
        name: str,
        window_seconds: float,
        now: Optional[float] = None,
    ) -> float:
        """Compute the per-second rate of COUNTER samples.

        Sums all COUNTER samples recorded in the last *window_seconds*
        seconds and divides by *window_seconds*.

        Args:
            name:           Metric name.
            window_seconds: Length of the look-back window in seconds.
            now:            Reference time; defaults to ``time.time()``.

        Returns:
            Rate in units/second (sum / window_seconds).
        """
        if now is None:
            now = time.time()
        start_ts = now - window_seconds
        total = 0.0
        for s in self._samples:
            if (
                s.name == name
                and s.metric_type == MetricType.COUNTER
                and start_ts <= s.ts <= now
            ):
                total += s.value
        return total / window_seconds if window_seconds > 0 else 0.0

    def histogram_buckets(
        self, name: str, buckets: list[float]
    ) -> dict[float, int]:
        """Count how many samples fall at or below each bucket threshold.

        Args:
            name:    Metric name to filter by.
            buckets: List of upper-bound thresholds (need not be sorted).

        Returns:
            Mapping ``{threshold: count}`` for each value in *buckets*.
        """
        relevant = [s.value for s in self._samples if s.name == name]
        result: dict[float, int] = {}
        for threshold in buckets:
            result[threshold] = sum(1 for v in relevant if v <= threshold)
        return result
