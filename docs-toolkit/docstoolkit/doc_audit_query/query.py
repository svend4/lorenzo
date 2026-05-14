"""E240 doc_audit_query: query DSL for audit logs."""
from __future__ import annotations

import threading
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class AggregateType(Enum):
    """Aggregate function types."""

    COUNT = "count"
    COUNT_DISTINCT = "count_distinct"
    MIN_TIME = "min_time"
    MAX_TIME = "max_time"
    FIRST = "first"
    LAST = "last"


class TimeBucket(Enum):
    """Time bucket sizes (in seconds)."""

    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2592000  # 30 days


@dataclass
class AuditEvent:
    """A single audit event."""

    event_id: int
    timestamp: float
    actor: str
    action: str
    resource: str
    outcome: str = "success"
    metadata: dict = field(default_factory=dict)


@dataclass
class Query:
    """Composable query filter."""

    actors: Optional[list[str]] = None
    actions: Optional[list[str]] = None
    resources: Optional[list[str]] = None
    outcomes: Optional[list[str]] = None
    start: Optional[float] = None
    end: Optional[float] = None
    text_contains: Optional[str] = None


@dataclass
class Bucket:
    """A time bucket containing events."""

    start: float
    end: float
    events: list[AuditEvent] = field(default_factory=list)


@dataclass
class AggregationResult:
    """Result of an aggregation operation."""

    aggregate_type: AggregateType
    value: Any


_EVENT_FIELDS = {"actor", "action", "resource", "outcome", "timestamp", "event_id"}


def _matches(event: AuditEvent, q: Optional[Query]) -> bool:
    """Check whether an event matches the given query."""
    if q is None:
        return True
    if q.actors is not None and event.actor not in q.actors:
        return False
    if q.actions is not None and event.action not in q.actions:
        return False
    if q.resources is not None and event.resource not in q.resources:
        return False
    if q.outcomes is not None and event.outcome not in q.outcomes:
        return False
    if q.start is not None and event.timestamp < q.start:
        return False
    if q.end is not None and event.timestamp > q.end:
        return False
    if q.text_contains is not None:
        needle = q.text_contains
        if (
            needle not in event.actor
            and needle not in event.action
            and needle not in event.resource
            and needle not in event.outcome
        ):
            return False
    return True


class DocAuditQuery:
    """Audit log query engine with composable filters and aggregations."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: list[AuditEvent] = []
        self._next_id: int = 1

    @property
    def total_events(self) -> int:
        with self._lock:
            return len(self._events)

    def add_event(
        self,
        actor: str,
        action: str,
        resource: str,
        outcome: str = "success",
        metadata: dict = None,
        now: float = 0.0,
    ) -> AuditEvent:
        """Add an event and return it."""
        with self._lock:
            event = AuditEvent(
                event_id=self._next_id,
                timestamp=now,
                actor=actor,
                action=action,
                resource=resource,
                outcome=outcome,
                metadata=dict(metadata) if metadata else {},
            )
            self._next_id += 1
            self._events.append(event)
            return event

    def add_events(self, events: list[AuditEvent]) -> int:
        """Append a list of pre-built audit events. Returns count added."""
        with self._lock:
            count = 0
            for ev in events:
                self._events.append(ev)
                if ev.event_id >= self._next_id:
                    self._next_id = ev.event_id + 1
                count += 1
            return count

    def query(self, q: Query) -> list[AuditEvent]:
        """Return events matching the query."""
        with self._lock:
            return [e for e in self._events if _matches(e, q)]

    def count(self, q: Query = None) -> int:
        """Count matching events."""
        with self._lock:
            if q is None:
                return len(self._events)
            return sum(1 for e in self._events if _matches(e, q))

    def distinct(self, q: Query, field: str) -> set:
        """Return distinct values of a field among matching events."""
        if field not in _EVENT_FIELDS:
            raise ValueError(f"Unknown field: {field}")
        with self._lock:
            return {getattr(e, field) for e in self._events if _matches(e, q)}

    def aggregate(
        self,
        q: Query,
        aggregate_type: AggregateType,
        field: str = None,
    ) -> AggregationResult:
        """Apply an aggregate function over matching events."""
        with self._lock:
            matched = [e for e in self._events if _matches(e, q)]

        if aggregate_type == AggregateType.COUNT:
            return AggregationResult(aggregate_type, len(matched))

        if aggregate_type == AggregateType.COUNT_DISTINCT:
            if field is None or field not in _EVENT_FIELDS:
                raise ValueError("COUNT_DISTINCT requires a valid field")
            return AggregationResult(
                aggregate_type, len({getattr(e, field) for e in matched})
            )

        if aggregate_type == AggregateType.MIN_TIME:
            if not matched:
                return AggregationResult(aggregate_type, None)
            return AggregationResult(aggregate_type, min(e.timestamp for e in matched))

        if aggregate_type == AggregateType.MAX_TIME:
            if not matched:
                return AggregationResult(aggregate_type, None)
            return AggregationResult(aggregate_type, max(e.timestamp for e in matched))

        if aggregate_type == AggregateType.FIRST:
            if not matched:
                return AggregationResult(aggregate_type, None)
            first_ev = min(matched, key=lambda e: e.timestamp)
            return AggregationResult(aggregate_type, first_ev)

        if aggregate_type == AggregateType.LAST:
            if not matched:
                return AggregationResult(aggregate_type, None)
            last_ev = max(matched, key=lambda e: e.timestamp)
            return AggregationResult(aggregate_type, last_ev)

        raise ValueError(f"Unknown aggregate type: {aggregate_type}")

    def group_by_time(
        self,
        q: Query,
        bucket: TimeBucket,
        now: float = 0.0,
    ) -> list[Bucket]:
        """Group matching events into time buckets.

        Buckets are aligned to multiples of bucket_size from epoch.
        Empty buckets are included between the first and last (or up to `now`).
        """
        size = bucket.value
        with self._lock:
            matched = [e for e in self._events if _matches(e, q)]

        if not matched and now == 0.0:
            return []

        if matched:
            ts_min = min(e.timestamp for e in matched)
            ts_max = max(e.timestamp for e in matched)
        else:
            ts_min = now
            ts_max = now

        # Use `now` as upper boundary if it is greater than ts_max.
        if now > ts_max:
            ts_max = now

        # Determine start/end of bucket range as aligned multiples.
        start_bucket = (int(ts_min) // size) * size
        end_bucket = (int(ts_max) // size) * size

        # If query has explicit start/end, prefer them as bounds.
        if q is not None and q.start is not None:
            start_bucket = (int(q.start) // size) * size
        if q is not None and q.end is not None:
            end_bucket = (int(q.end) // size) * size

        buckets: list[Bucket] = []
        cur = start_bucket
        while cur <= end_bucket:
            b_start = float(cur)
            b_end = float(cur + size)
            events_in = [e for e in matched if b_start <= e.timestamp < b_end]
            buckets.append(Bucket(start=b_start, end=b_end, events=events_in))
            cur += size

        return buckets

    def group_by_field(self, q: Query, field: str) -> dict[Any, list[AuditEvent]]:
        """Group matching events by the given field's value."""
        if field not in _EVENT_FIELDS:
            raise ValueError(f"Unknown field: {field}")
        with self._lock:
            matched = [e for e in self._events if _matches(e, q)]
        result: dict[Any, list[AuditEvent]] = {}
        for ev in matched:
            key = getattr(ev, field)
            result.setdefault(key, []).append(ev)
        return result

    def _top(self, q: Optional[Query], field: str, n: int) -> list[tuple[str, int]]:
        with self._lock:
            matched = [e for e in self._events if _matches(e, q)]
        counter: Counter = Counter(getattr(e, field) for e in matched)
        return counter.most_common(n)

    def top_actors(self, q: Query = None, n: int = 10) -> list[tuple[str, int]]:
        return self._top(q, "actor", n)

    def top_actions(self, q: Query = None, n: int = 10) -> list[tuple[str, int]]:
        return self._top(q, "action", n)

    def top_resources(self, q: Query = None, n: int = 10) -> list[tuple[str, int]]:
        return self._top(q, "resource", n)

    def failure_rate(self, q: Query = None) -> float:
        """Fraction of matched events whose outcome is not 'success'."""
        with self._lock:
            matched = [e for e in self._events if _matches(e, q)]
        if not matched:
            return 0.0
        failures = sum(1 for e in matched if e.outcome != "success")
        return failures / len(matched)

    def unique_actors_count(self, q: Query = None) -> int:
        """Number of unique actors among matched events."""
        with self._lock:
            matched = [e for e in self._events if _matches(e, q)]
        return len({e.actor for e in matched})

    def recent(self, n: int = 10) -> list[AuditEvent]:
        """Return the n most recent events (newest first by timestamp)."""
        with self._lock:
            sorted_events = sorted(
                self._events, key=lambda e: (e.timestamp, e.event_id), reverse=True
            )
            return sorted_events[:n]

    def clear(self) -> None:
        """Remove all events and reset id counter."""
        with self._lock:
            self._events.clear()
            self._next_id = 1
