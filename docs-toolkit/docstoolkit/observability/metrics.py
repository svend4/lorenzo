"""Metrics: Counter, Gauge, Histogram, and MetricsRegistry."""
import math
from dataclasses import dataclass, field


@dataclass
class Counter:
    """An integer counter that can only be incremented or reset."""

    name: str
    value: int = 0
    tags: dict = field(default_factory=dict)

    def increment(self, n: int = 1) -> None:
        """Increment the counter by n (default 1)."""
        self.value += n

    def reset(self) -> None:
        """Reset the counter to zero."""
        self.value = 0


@dataclass
class Gauge:
    """A floating-point value that can be set, incremented, or decremented."""

    name: str
    value: float = 0.0

    def set(self, v: float) -> None:
        """Set the gauge to the given value."""
        self.value = v

    def increment(self, n: float = 1.0) -> None:
        """Increment the gauge by n (default 1.0)."""
        self.value += n

    def decrement(self, n: float = 1.0) -> None:
        """Decrement the gauge by n (default 1.0)."""
        self.value -= n


@dataclass
class Histogram:
    """Records a distribution of float values with percentile support."""

    name: str
    values: list[float] = field(default_factory=list)

    def record(self, v: float) -> None:
        """Record a new observation."""
        self.values.append(v)

    def percentile(self, p: float) -> float:
        """Return the p-th percentile using linear interpolation. 0.0 if empty."""
        if not self.values:
            return 0.0
        sorted_vals = sorted(self.values)
        n = len(sorted_vals)
        if n == 1:
            return sorted_vals[0]
        # Map p (0–100) to an index in [0, n-1]
        index = (p / 100.0) * (n - 1)
        lower = math.floor(index)
        upper = math.ceil(index)
        if lower == upper:
            return sorted_vals[lower]
        frac = index - lower
        return sorted_vals[lower] + frac * (sorted_vals[upper] - sorted_vals[lower])

    def mean(self) -> float:
        """Return the arithmetic mean of recorded values, or 0.0 if empty."""
        if not self.values:
            return 0.0
        return sum(self.values) / len(self.values)

    def count(self) -> int:
        """Return the number of recorded observations."""
        return len(self.values)


class MetricsRegistry:
    """Central registry for named metrics; reuses existing instances by name."""

    def __init__(self):
        self._counters: dict[str, Counter] = {}
        self._gauges: dict[str, Gauge] = {}
        self._histograms: dict[str, Histogram] = {}

    def counter(self, name: str, tags: dict = None) -> Counter:
        """Return the existing Counter for name, or create a new one."""
        if name not in self._counters:
            self._counters[name] = Counter(name=name, tags=tags or {})
        return self._counters[name]

    def gauge(self, name: str) -> Gauge:
        """Return the existing Gauge for name, or create a new one."""
        if name not in self._gauges:
            self._gauges[name] = Gauge(name=name)
        return self._gauges[name]

    def histogram(self, name: str) -> Histogram:
        """Return the existing Histogram for name, or create a new one."""
        if name not in self._histograms:
            self._histograms[name] = Histogram(name=name)
        return self._histograms[name]

    def snapshot(self) -> dict:
        """Return a dict with current values for all registered metrics."""
        result: dict = {}

        for name, c in self._counters.items():
            result[f"counter.{name}"] = {"value": c.value, "tags": c.tags}

        for name, g in self._gauges.items():
            result[f"gauge.{name}"] = {"value": g.value}

        for name, h in self._histograms.items():
            result[f"histogram.{name}"] = {
                "count": h.count(),
                "mean": h.mean(),
                "p50": h.percentile(50),
                "p95": h.percentile(95),
                "p99": h.percentile(99),
            }

        return result
