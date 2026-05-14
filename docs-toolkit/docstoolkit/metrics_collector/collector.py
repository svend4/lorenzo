"""MetricsCollector — thread-safe, in-memory named metric collection.

Supports four metric types:
    COUNTER   — monotonically increasing sum; value = cumulative total.
    GAUGE     — arbitrary value that can go up or down; value = last set value.
    HISTOGRAM — records arbitrary observations; computes percentiles.
    TIMER     — records durations in milliseconds; computes percentiles.

All operations are protected by a single ``threading.Lock`` so the collector
is safe to use from multiple threads.

Public API
----------
counter(name, value, labels)
gauge(name, value, labels)
histogram(name, value, labels)
timer(name, duration_ms, labels)
measure(name, labels)           — context manager; records elapsed ms
snapshot(name)                  — MetricSnapshot | None
all_snapshots()                 — list[MetricSnapshot]
reset(name)                     — bool
reset_all()
metric_names()                  — list[str]
exists(name)                    — bool
"""
from __future__ import annotations

import math
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Generator


class MetricType(str, Enum):
    """Category of a metric."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class MetricSnapshot:
    """Immutable snapshot of a single metric at a point in time.

    Attributes:
        name:        Metric name.
        metric_type: One of COUNTER / GAUGE / HISTOGRAM / TIMER.
        value:       Current value: cumulative sum (counter/gauge) or last
                     recorded observation (histogram/timer).
        count:       Number of times the metric has been updated.
        total:       Sum of all recorded values.
        min:         Minimum recorded value (None for counter/gauge).
        max:         Maximum recorded value (None for counter/gauge).
        p50:         50th-percentile (median); None when N < 1 or not applicable.
        p95:         95th-percentile; None when not applicable.
        p99:         99th-percentile; None when not applicable.
        labels:      Label dict attached at first registration.
    """

    name: str
    metric_type: MetricType
    value: float
    count: int
    total: float
    min: float | None = None
    max: float | None = None
    p50: float | None = None
    p95: float | None = None
    p99: float | None = None
    labels: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal state per metric
# ---------------------------------------------------------------------------

class _MetricState:
    """Mutable accumulator for a single named metric."""

    __slots__ = (
        "metric_type",
        "labels",
        "value",
        "count",
        "total",
        "min",
        "max",
        "_observations",
    )

    def __init__(self, metric_type: MetricType, labels: dict) -> None:
        self.metric_type = metric_type
        self.labels: dict = dict(labels)
        self.value: float = 0.0
        self.count: int = 0
        self.total: float = 0.0
        self.min: float | None = None
        self.max: float | None = None
        # Only populated for HISTOGRAM / TIMER so we can compute percentiles.
        self._observations: list[float] = []

    # ------------------------------------------------------------------
    # Update helpers (called from MetricsCollector while lock is held)
    # ------------------------------------------------------------------

    def update_counter(self, amount: float) -> None:
        self.value += amount
        self.total += amount
        self.count += 1

    def update_gauge(self, new_value: float) -> None:
        self.value = new_value
        self.total += new_value
        self.count += 1

    def update_distribution(self, observation: float) -> None:
        """Used for both HISTOGRAM and TIMER."""
        self.value = observation
        self.total += observation
        self.count += 1
        if self.min is None or observation < self.min:
            self.min = observation
        if self.max is None or observation > self.max:
            self.max = observation
        self._observations.append(observation)

    def reset(self) -> None:
        self.value = 0.0
        self.count = 0
        self.total = 0.0
        self.min = None
        self.max = None
        self._observations.clear()

    # ------------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------------

    def to_snapshot(self, name: str) -> MetricSnapshot:
        p50 = p95 = p99 = None
        if self._observations:
            p50 = _percentile(self._observations, 50.0)
            p95 = _percentile(self._observations, 95.0)
            p99 = _percentile(self._observations, 99.0)
        return MetricSnapshot(
            name=name,
            metric_type=self.metric_type,
            value=self.value,
            count=self.count,
            total=self.total,
            min=self.min,
            max=self.max,
            p50=p50,
            p95=p95,
            p99=p99,
            labels=dict(self.labels),
        )


# ---------------------------------------------------------------------------
# Percentile helper (linear interpolation, same as WindowedStatistics)
# ---------------------------------------------------------------------------

def _percentile(values: list[float], p: float) -> float:
    """Linear-interpolated percentile over *values* (need not be sorted).

    Args:
        values: Non-empty list of numeric observations.
        p:      Percentile in [0, 100].

    Returns:
        Interpolated value.
    """
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n == 1:
        return sorted_vals[0]
    if p <= 0:
        return sorted_vals[0]
    if p >= 100:
        return sorted_vals[-1]
    rank = (p / 100.0) * (n - 1)
    lo = int(math.floor(rank))
    hi = lo + 1
    if hi >= n:
        return sorted_vals[-1]
    frac = rank - lo
    return sorted_vals[lo] + frac * (sorted_vals[hi] - sorted_vals[lo])


# ---------------------------------------------------------------------------
# MetricsCollector
# ---------------------------------------------------------------------------

class MetricsCollector:
    """Thread-safe, in-memory metrics collector.

    All four metric types share a single flat namespace keyed by *name*.
    A name must always be used with the same metric type; mixing types for
    the same name raises ``ValueError``.

    Labels are stored on first registration.  Subsequent calls with the
    same name but different labels are silently ignored (first-call wins).

    Example::

        mc = MetricsCollector()
        mc.counter("requests", labels={"method": "GET"})
        mc.counter("requests")          # increments the same metric
        mc.gauge("temperature", 22.5)
        mc.histogram("response_size", 1024)
        mc.timer("query_time", 12.3)

        with mc.measure("db_query"):
            do_db_work()

        snap = mc.snapshot("requests")
        print(snap.value, snap.count)
    """

    def __init__(self) -> None:
        self._metrics: dict[str, _MetricState] = {}
        self._order: list[str] = []  # insertion-order registry
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_or_create(
        self,
        name: str,
        metric_type: MetricType,
        labels: dict | None,
    ) -> _MetricState:
        """Return the state for *name*, creating it if absent.

        Raises:
            ValueError: if *name* already exists with a different MetricType.
        """
        if name in self._metrics:
            state = self._metrics[name]
            if state.metric_type != metric_type:
                raise ValueError(
                    f"Metric '{name}' already registered as "
                    f"{state.metric_type.value!r}; "
                    f"cannot use it as {metric_type.value!r}"
                )
            return state
        # New metric
        state = _MetricState(metric_type, labels or {})
        self._metrics[name] = state
        self._order.append(name)
        return state

    # ------------------------------------------------------------------
    # Public recording methods
    # ------------------------------------------------------------------

    def counter(
        self,
        name: str,
        value: float = 1.0,
        labels: dict | None = None,
    ) -> None:
        """Increment a counter by *value* (default 1.0).

        Args:
            name:   Metric name.
            value:  Amount to add; should be >= 0 for a proper counter.
            labels: Label dict; only used on first call for this name.
        """
        with self._lock:
            state = self._get_or_create(name, MetricType.COUNTER, labels)
            state.update_counter(value)

    def gauge(
        self,
        name: str,
        value: float,
        labels: dict | None = None,
    ) -> None:
        """Set gauge to *value*.

        Args:
            name:   Metric name.
            value:  New gauge reading.
            labels: Label dict; only used on first call for this name.
        """
        with self._lock:
            state = self._get_or_create(name, MetricType.GAUGE, labels)
            state.update_gauge(value)

    def histogram(
        self,
        name: str,
        value: float,
        labels: dict | None = None,
    ) -> None:
        """Record *value* as an observation in a histogram.

        Args:
            name:   Metric name.
            value:  Observed value.
            labels: Label dict; only used on first call for this name.
        """
        with self._lock:
            state = self._get_or_create(name, MetricType.HISTOGRAM, labels)
            state.update_distribution(value)

    def timer(
        self,
        name: str,
        duration_ms: float,
        labels: dict | None = None,
    ) -> None:
        """Record *duration_ms* (milliseconds) in a timer metric.

        Args:
            name:        Metric name.
            duration_ms: Duration to record.
            labels:      Label dict; only used on first call for this name.
        """
        with self._lock:
            state = self._get_or_create(name, MetricType.TIMER, labels)
            state.update_distribution(duration_ms)

    @contextmanager
    def measure(
        self,
        name: str,
        labels: dict | None = None,
    ) -> Generator[None, None, None]:
        """Context manager that measures elapsed wall-clock time and records it.

        The elapsed duration is recorded in milliseconds via :meth:`timer`.

        Args:
            name:   Timer metric name.
            labels: Optional labels for first registration.

        Example::

            with collector.measure("my_op"):
                do_work()
        """
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            self.timer(name, elapsed_ms, labels=labels)

    # ------------------------------------------------------------------
    # Query methods
    # ------------------------------------------------------------------

    def snapshot(self, name: str) -> MetricSnapshot | None:
        """Return a :class:`MetricSnapshot` for *name*, or ``None`` if unknown.

        Args:
            name: Metric name.

        Returns:
            Current snapshot, or ``None``.
        """
        with self._lock:
            state = self._metrics.get(name)
            if state is None:
                return None
            return state.to_snapshot(name)

    def all_snapshots(self) -> list[MetricSnapshot]:
        """Return snapshots for all registered metrics in insertion order.

        Returns:
            List of :class:`MetricSnapshot` objects.
        """
        with self._lock:
            return [self._metrics[n].to_snapshot(n) for n in self._order]

    def reset(self, name: str) -> bool:
        """Reset a metric to its zero state.

        Args:
            name: Metric name.

        Returns:
            ``True`` if the metric existed and was reset; ``False`` otherwise.
        """
        with self._lock:
            state = self._metrics.get(name)
            if state is None:
                return False
            state.reset()
            return True

    def reset_all(self) -> None:
        """Reset every registered metric to its zero state."""
        with self._lock:
            for state in self._metrics.values():
                state.reset()

    def metric_names(self) -> list[str]:
        """Return all registered metric names in insertion order.

        Returns:
            Ordered list of metric names.
        """
        with self._lock:
            return list(self._order)

    def exists(self, name: str) -> bool:
        """Return ``True`` if *name* is a registered metric.

        Args:
            name: Metric name to check.
        """
        with self._lock:
            return name in self._metrics
