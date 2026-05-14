"""Document observability collector: traces, metrics, custom events."""
from __future__ import annotations

import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class MetricType(Enum):
    """Type of a recorded metric."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMING = "timing"


@dataclass
class Trace:
    """A trace span with start/end timing."""

    trace_id: str
    span_name: str
    start_at: float
    end_at: Optional[float] = None
    parent_span_id: Optional[str] = None
    tags: dict = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        """Duration in milliseconds (0.0 if not ended)."""
        if self.end_at is None:
            return 0.0
        return (self.end_at - self.start_at) * 1000.0


@dataclass
class MetricPoint:
    """A single metric measurement."""

    name: str
    value: float
    metric_type: MetricType
    timestamp: float
    tags: dict = field(default_factory=dict)


@dataclass
class CustomEvent:
    """A custom event with arbitrary payload."""

    event_id: int
    event_type: str
    data: dict
    timestamp: float
    severity: str = "info"


@dataclass
class Aggregate:
    """Aggregate statistics for a metric."""

    metric_name: str
    count: int
    sum: float
    min: float
    max: float
    avg: float


class DocObservability:
    """Collector for traces, metrics, and custom events."""

    def __init__(
        self,
        max_traces: int = 10000,
        max_metrics: int = 100000,
        max_events: int = 10000,
    ) -> None:
        self._max_traces = max_traces
        self._max_metrics = max_metrics
        self._max_events = max_events
        self._traces: deque = deque(maxlen=max_traces)
        self._traces_by_id: dict = {}
        self._metrics: deque = deque(maxlen=max_metrics)
        self._events: deque = deque(maxlen=max_events)
        self._next_event_id = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ traces

    def start_span(
        self,
        span_name: str,
        parent_span_id: Optional[str] = None,
        tags: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> Trace:
        """Start a new span, returning the Trace object."""
        ts = float(now) if now is not None else time.time()
        trace_id = uuid.uuid4().hex
        trace = Trace(
            trace_id=trace_id,
            span_name=span_name,
            start_at=ts,
            end_at=None,
            parent_span_id=parent_span_id,
            tags=dict(tags) if tags else {},
        )
        with self._lock:
            # If we're about to evict, drop from the lookup map first.
            if (
                self._max_traces
                and len(self._traces) == self._max_traces
                and self._traces
            ):
                evicted = self._traces[0]
                self._traces_by_id.pop(evicted.trace_id, None)
            self._traces.append(trace)
            self._traces_by_id[trace_id] = trace
        return trace

    def end_span(self, trace_id: str, now: Optional[float] = None) -> bool:
        """Close a span by id, returning True if found."""
        ts = float(now) if now is not None else time.time()
        with self._lock:
            trace = self._traces_by_id.get(trace_id)
            if trace is None:
                return False
            trace.end_at = ts
            return True

    # ----------------------------------------------------------------- metrics

    def record_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        tags: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> MetricPoint:
        """Record a metric point of any type."""
        ts = float(now) if now is not None else time.time()
        point = MetricPoint(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=ts,
            tags=dict(tags) if tags else {},
        )
        with self._lock:
            self._metrics.append(point)
        return point

    def increment(
        self,
        name: str,
        value: float = 1.0,
        tags: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> MetricPoint:
        """Record a COUNTER metric."""
        return self.record_metric(name, value, MetricType.COUNTER, tags, now)

    def gauge(
        self,
        name: str,
        value: float,
        tags: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> MetricPoint:
        """Record a GAUGE metric."""
        return self.record_metric(name, value, MetricType.GAUGE, tags, now)

    def histogram(
        self,
        name: str,
        value: float,
        tags: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> MetricPoint:
        """Record a HISTOGRAM metric."""
        return self.record_metric(name, value, MetricType.HISTOGRAM, tags, now)

    def timing(
        self,
        name: str,
        value: float,
        tags: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> MetricPoint:
        """Record a TIMING metric."""
        return self.record_metric(name, value, MetricType.TIMING, tags, now)

    # ------------------------------------------------------------------ events

    def record_event(
        self,
        event_type: str,
        data: Optional[dict] = None,
        severity: str = "info",
        now: Optional[float] = None,
    ) -> CustomEvent:
        """Record a custom event."""
        ts = float(now) if now is not None else time.time()
        with self._lock:
            event_id = self._next_event_id
            self._next_event_id += 1
            event = CustomEvent(
                event_id=event_id,
                event_type=event_type,
                data=dict(data) if data else {},
                timestamp=ts,
                severity=severity,
            )
            self._events.append(event)
        return event

    # ------------------------------------------------------------------ query

    def traces(self, limit: Optional[int] = None) -> list:
        """Return recorded traces, most recent last; optional limit (latest N)."""
        with self._lock:
            result = list(self._traces)
        if limit is not None and limit >= 0:
            result = result[-limit:] if limit > 0 else []
        return result

    def metrics(
        self, name: Optional[str] = None, limit: Optional[int] = None
    ) -> list:
        """Return metrics, optionally filtered by name."""
        with self._lock:
            result = list(self._metrics)
        if name is not None:
            result = [m for m in result if m.name == name]
        if limit is not None and limit >= 0:
            result = result[-limit:] if limit > 0 else []
        return result

    def events(
        self,
        event_type: Optional[str] = None,
        severity: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list:
        """Return events filtered by type and/or severity."""
        with self._lock:
            result = list(self._events)
        if event_type is not None:
            result = [e for e in result if e.event_type == event_type]
        if severity is not None:
            result = [e for e in result if e.severity == severity]
        if limit is not None and limit >= 0:
            result = result[-limit:] if limit > 0 else []
        return result

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Lookup a trace by id."""
        with self._lock:
            return self._traces_by_id.get(trace_id)

    # ------------------------------------------------------------ aggregations

    def aggregate(
        self,
        metric_name: str,
        start: Optional[float] = None,
        end: Optional[float] = None,
    ) -> Optional[Aggregate]:
        """Aggregate stats for a metric, optionally bounded by [start, end]."""
        with self._lock:
            values = [
                m.value
                for m in self._metrics
                if m.name == metric_name
                and (start is None or m.timestamp >= start)
                and (end is None or m.timestamp <= end)
            ]
        if not values:
            return None
        total = sum(values)
        count = len(values)
        return Aggregate(
            metric_name=metric_name,
            count=count,
            sum=total,
            min=min(values),
            max=max(values),
            avg=total / count,
        )

    def time_series(
        self,
        metric_name: str,
        bucket_size: float = 60.0,
        now: Optional[float] = None,
    ) -> list:
        """Bucketed time series (bucket_start, sum_value)."""
        if bucket_size <= 0:
            return []
        with self._lock:
            points = [m for m in self._metrics if m.name == metric_name]
        if not points:
            return []
        buckets: dict = {}
        for p in points:
            bucket_start = (p.timestamp // bucket_size) * bucket_size
            buckets[bucket_start] = buckets.get(bucket_start, 0.0) + p.value
        return sorted(buckets.items())

    def unique_metric_names(self) -> set:
        """Set of unique metric names recorded."""
        with self._lock:
            return {m.name for m in self._metrics}

    # ---------------------------------------------------------------- lifecycle

    def clear(self) -> None:
        """Remove all traces, metrics, and events."""
        with self._lock:
            self._traces.clear()
            self._traces_by_id.clear()
            self._metrics.clear()
            self._events.clear()
            self._next_event_id = 1

    @property
    def total_traces(self) -> int:
        with self._lock:
            return len(self._traces)

    @property
    def total_metrics(self) -> int:
        with self._lock:
            return len(self._metrics)

    @property
    def total_events(self) -> int:
        with self._lock:
            return len(self._events)
