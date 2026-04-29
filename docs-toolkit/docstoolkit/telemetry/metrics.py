"""Prometheus-compatible metrics: Counter / Histogram / Gauge.

Без зависимостей: in-memory accumulator + prometheus exposition format.
"""
import threading
from dataclasses import dataclass, field


@dataclass
class Counter:
    """Monotonic counter."""
    name: str
    description: str = ""
    labels: dict = field(default_factory=dict)
    _value: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def inc(self, amount: float = 1.0):
        with self._lock:
            self._value += amount

    @property
    def value(self) -> float:
        return self._value


@dataclass
class Gauge:
    """Set/get value."""
    name: str
    description: str = ""
    labels: dict = field(default_factory=dict)
    _value: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def set(self, value: float):
        with self._lock:
            self._value = value

    def inc(self, amount: float = 1.0):
        with self._lock:
            self._value += amount

    def dec(self, amount: float = 1.0):
        with self._lock:
            self._value -= amount

    @property
    def value(self) -> float:
        return self._value


@dataclass
class Histogram:
    """Histogram с фиксированными buckets + sum/count."""
    name: str
    description: str = ""
    buckets: list[float] = field(
        default_factory=lambda: [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]
    )
    _bucket_counts: list[int] = field(default_factory=list)
    _sum: float = 0.0
    _count: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def __post_init__(self):
        self._bucket_counts = [0] * len(self.buckets)

    def observe(self, value: float):
        with self._lock:
            self._sum += value
            self._count += 1
            for i, threshold in enumerate(self.buckets):
                if value <= threshold:
                    self._bucket_counts[i] += 1


class Meter:
    """Реестр всех metrics."""

    def __init__(self):
        self._counters: dict[str, Counter] = {}
        self._gauges: dict[str, Gauge] = {}
        self._histograms: dict[str, Histogram] = {}
        self._lock = threading.Lock()

    def counter(self, name: str, description: str = "",
                labels: dict | None = None) -> Counter:
        with self._lock:
            if name not in self._counters:
                self._counters[name] = Counter(
                    name=name, description=description,
                    labels=labels or {})
            return self._counters[name]

    def gauge(self, name: str, description: str = "",
              labels: dict | None = None) -> Gauge:
        with self._lock:
            if name not in self._gauges:
                self._gauges[name] = Gauge(
                    name=name, description=description,
                    labels=labels or {})
            return self._gauges[name]

    def histogram(self, name: str, description: str = "",
                  buckets: list[float] | None = None) -> Histogram:
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = Histogram(
                    name=name, description=description,
                    buckets=buckets or [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0])
            return self._histograms[name]

    def all_counters(self):
        return list(self._counters.values())

    def all_gauges(self):
        return list(self._gauges.values())

    def all_histograms(self):
        return list(self._histograms.values())


# Module-level
meter = Meter()


def _format_labels(labels: dict) -> str:
    if not labels:
        return ""
    parts = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
    return "{" + parts + "}"


def prometheus_format() -> str:
    """Возвращает все metrics в Prometheus exposition format."""
    lines = []
    for c in meter.all_counters():
        if c.description:
            lines.append(f"# HELP {c.name} {c.description}")
        lines.append(f"# TYPE {c.name} counter")
        lines.append(f"{c.name}{_format_labels(c.labels)} {c.value}")

    for g in meter.all_gauges():
        if g.description:
            lines.append(f"# HELP {g.name} {g.description}")
        lines.append(f"# TYPE {g.name} gauge")
        lines.append(f"{g.name}{_format_labels(g.labels)} {g.value}")

    for h in meter.all_histograms():
        if h.description:
            lines.append(f"# HELP {h.name} {h.description}")
        lines.append(f"# TYPE {h.name} histogram")
        cumulative = 0
        for threshold, count in zip(h.buckets, h._bucket_counts):
            cumulative = max(cumulative, count)
            lines.append(f'{h.name}_bucket{{le="{threshold}"}} {cumulative}')
        lines.append(f'{h.name}_bucket{{le="+Inf"}} {h._count}')
        lines.append(f"{h.name}_sum {h._sum}")
        lines.append(f"{h.name}_count {h._count}")

    return "\n".join(lines) + "\n"
