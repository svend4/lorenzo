"""Per-document numeric metric recorder.

Records metric data points keyed by (doc_id, metric) and computes summary
aggregates (count/total/avg/min/max), top-N rankings by total or average,
and supports time-range queries.

Storage:
    - A global ordered list of :class:`MetricPoint` instances.
    - A secondary index mapping ``(doc_id, metric)`` to lists of integer
      positions inside that global list.
    - :class:`threading.Lock` for safe concurrent recording and queries.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MetricPoint:
    """A single recorded metric data point for a document."""

    doc_id: str
    metric: str
    value: float
    recorded_at: float = 0.0
    tags: dict = field(default_factory=dict)


@dataclass
class MetricSummary:
    """Aggregate summary for a metric on a single document."""

    doc_id: str
    metric: str
    count: int
    total: float
    avg: float
    min_value: float
    max_value: float


@dataclass
class MetricStats:
    """Global aggregate statistics across all recorded metrics."""

    total_points: int
    unique_docs: int
    unique_metrics: int


class DocMetricRecorder:
    """Thread-safe in-memory recorder of per-document numeric metrics."""

    def __init__(self) -> None:
        self._points: list = []
        self._by_key: dict = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ record

    def record(
        self,
        doc_id: str,
        metric: str,
        value: float,
        tags: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> MetricPoint:
        """Record a numeric metric data point.

        Parameters
        ----------
        doc_id:
            Document identifier.
        metric:
            Name of the metric being recorded.
        value:
            Numeric value.
        tags:
            Optional dictionary of additional dimensions; copied defensively.
        now:
            Optional timestamp override; defaults to :func:`time.time`.
        """
        ts = time.time() if now is None else float(now)
        tag_copy = dict(tags) if tags else {}
        point = MetricPoint(
            doc_id=doc_id,
            metric=metric,
            value=float(value),
            recorded_at=ts,
            tags=tag_copy,
        )
        with self._lock:
            idx = len(self._points)
            self._points.append(point)
            key = (doc_id, metric)
            bucket = self._by_key.get(key)
            if bucket is None:
                bucket = []
                self._by_key[key] = bucket
            bucket.append(idx)
        return point

    # ----------------------------------------------------------------- summary

    def summary(self, doc_id: str, metric: str) -> Optional[MetricSummary]:
        """Return aggregate summary for a (doc_id, metric) pair.

        Returns ``None`` if no points are recorded for the key.
        """
        with self._lock:
            indices = self._by_key.get((doc_id, metric))
            if not indices:
                return None
            values = [self._points[i].value for i in indices]
        count = len(values)
        total = float(sum(values))
        avg = total / count
        return MetricSummary(
            doc_id=doc_id,
            metric=metric,
            count=count,
            total=total,
            avg=avg,
            min_value=min(values),
            max_value=max(values),
        )

    # ------------------------------------------------------------------ points

    def points(
        self,
        doc_id: str,
        metric: str,
        limit: Optional[int] = None,
    ) -> list:
        """Return points for a (doc_id, metric), most recent first."""
        with self._lock:
            indices = self._by_key.get((doc_id, metric), [])
            pts = [self._points[i] for i in indices]
        pts.sort(key=lambda p: p.recorded_at, reverse=True)
        if limit is not None:
            if limit < 0:
                raise ValueError("limit must be non-negative")
            pts = pts[:limit]
        return pts

    def points_in_range(
        self,
        doc_id: str,
        metric: str,
        start: float,
        end: float,
    ) -> list:
        """Return points with ``start <= recorded_at <= end``, sorted ascending."""
        if start > end:
            raise ValueError("start must be <= end")
        with self._lock:
            indices = self._by_key.get((doc_id, metric), [])
            pts = [
                self._points[i]
                for i in indices
                if start <= self._points[i].recorded_at <= end
            ]
        pts.sort(key=lambda p: p.recorded_at)
        return pts

    # ----------------------------------------------------------- top-N queries

    def _aggregate_by_doc(self, metric: str) -> dict:
        agg: dict = {}
        with self._lock:
            for (doc_id, m), indices in self._by_key.items():
                if m != metric:
                    continue
                total = 0.0
                count = 0
                for i in indices:
                    total += self._points[i].value
                    count += 1
                if count:
                    agg[doc_id] = (total, count)
        return agg

    def top_docs_by_total(self, metric: str, limit: int = 10) -> list:
        """Return ``[(doc_id, total), ...]`` ranked by total value desc."""
        if limit < 0:
            raise ValueError("limit must be non-negative")
        agg = self._aggregate_by_doc(metric)
        items = [(doc_id, total) for doc_id, (total, _c) in agg.items()]
        items.sort(key=lambda t: (-t[1], t[0]))
        return items[:limit]

    def top_docs_by_avg(self, metric: str, limit: int = 10) -> list:
        """Return ``[(doc_id, avg), ...]`` ranked by mean value desc."""
        if limit < 0:
            raise ValueError("limit must be non-negative")
        agg = self._aggregate_by_doc(metric)
        items = [
            (doc_id, total / count) for doc_id, (total, count) in agg.items()
        ]
        items.sort(key=lambda t: (-t[1], t[0]))
        return items[:limit]

    # ------------------------------------------------------------- enumeration

    def metrics_for_doc(self, doc_id: str) -> list:
        """Return sorted unique metric names recorded for ``doc_id``."""
        with self._lock:
            names = {m for (d, m) in self._by_key if d == doc_id}
        return sorted(names)

    def docs_for_metric(self, metric: str) -> list:
        """Return sorted unique doc ids that recorded ``metric``."""
        with self._lock:
            docs = {d for (d, m) in self._by_key if m == metric}
        return sorted(docs)

    def all_doc_ids(self) -> list:
        """Return sorted list of all unique doc ids."""
        with self._lock:
            docs = {d for (d, _m) in self._by_key}
        return sorted(docs)

    # ----------------------------------------------------------------- clear

    def clear_doc(self, doc_id: str) -> int:
        """Remove all points for ``doc_id``; return count removed."""
        with self._lock:
            removed = 0
            keys_to_drop = [k for k in self._by_key if k[0] == doc_id]
            for key in keys_to_drop:
                removed += len(self._by_key[key])
                del self._by_key[key]
            return removed

    def clear_metric(self, metric: str) -> int:
        """Remove all points for ``metric``; return count removed."""
        with self._lock:
            removed = 0
            keys_to_drop = [k for k in self._by_key if k[1] == metric]
            for key in keys_to_drop:
                removed += len(self._by_key[key])
                del self._by_key[key]
            return removed

    # ------------------------------------------------------------------ stats

    def stats(self) -> MetricStats:
        """Return :class:`MetricStats` describing global recorder state."""
        with self._lock:
            total = sum(len(v) for v in self._by_key.values())
            docs = {d for (d, _m) in self._by_key}
            metrics = {m for (_d, m) in self._by_key}
        return MetricStats(
            total_points=total,
            unique_docs=len(docs),
            unique_metrics=len(metrics),
        )
