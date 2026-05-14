"""Sliding window metric aggregation for documents.

Stores numeric metric points keyed by ``(doc_id, metric)`` along with their
timestamps. Supports rolling window aggregations (count, sum, average, min,
max) over arbitrary time windows.

Storage layout
--------------
* ``_points`` — flat list of :class:`WindowPoint` instances, kept in
  insertion order. Because :meth:`DocMetricWindow.record` defaults
  ``timestamp`` to :func:`time.time`, the list is also (typically) ordered
  by timestamp. Pruning rebuilds the index to keep things consistent.
* ``_by_key`` — mapping from ``(doc_id, metric)`` to the list of integer
  indices in ``_points`` belonging to that key.
* ``_lock`` — :class:`threading.Lock` used by every public method to
  guarantee safe concurrent access.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class WindowPoint:
    """A single data point inside a sliding window."""

    doc_id: str
    metric: str
    value: float
    timestamp: float


@dataclass
class WindowStats:
    """Aggregate stats for points inside a single window."""

    count: int
    sum: float
    avg: float
    min_value: float
    max_value: float


@dataclass
class MetricStats:
    """Global statistics across all recorded points."""

    total_points: int
    unique_metrics: int
    unique_docs: int


class DocMetricWindow:
    """Thread-safe sliding-window aggregator for per-document metrics."""

    def __init__(self) -> None:
        self._points: list[WindowPoint] = []
        self._by_key: dict[tuple, list[int]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ record

    def record(
        self,
        doc_id: str,
        metric: str,
        value: float,
        timestamp: Optional[float] = None,
    ) -> WindowPoint:
        """Record a numeric data point.

        Parameters
        ----------
        doc_id:
            Document identifier.
        metric:
            Metric name.
        value:
            Numeric value to record.
        timestamp:
            Optional explicit timestamp; defaults to :func:`time.time`.

        Returns
        -------
        WindowPoint
            The newly recorded point.
        """
        ts = float(timestamp) if timestamp is not None else time.time()
        point = WindowPoint(doc_id=doc_id, metric=metric, value=float(value), timestamp=ts)
        with self._lock:
            idx = len(self._points)
            self._points.append(point)
            self._by_key.setdefault((doc_id, metric), []).append(idx)
        return point

    # -------------------------------------------------------------- helpers

    def _points_in_window(
        self,
        doc_id: str,
        metric: str,
        window_seconds: float,
        now: Optional[float],
    ) -> list[WindowPoint]:
        cutoff_now = float(now) if now is not None else time.time()
        cutoff_old = cutoff_now - float(window_seconds)
        indices = self._by_key.get((doc_id, metric), [])
        selected = [
            self._points[i]
            for i in indices
            if cutoff_old <= self._points[i].timestamp <= cutoff_now
        ]
        selected.sort(key=lambda p: p.timestamp)
        return selected

    # --------------------------------------------------------------- queries

    def window_stats(
        self,
        doc_id: str,
        metric: str,
        window_seconds: float,
        now: Optional[float] = None,
    ) -> Optional[WindowStats]:
        """Aggregate stats for points inside ``[now - window_seconds, now]``.

        Returns ``None`` if no points fall inside the window.
        """
        with self._lock:
            points = self._points_in_window(doc_id, metric, window_seconds, now)
        if not points:
            return None
        values = [p.value for p in points]
        total = sum(values)
        count = len(values)
        return WindowStats(
            count=count,
            sum=total,
            avg=total / count,
            min_value=min(values),
            max_value=max(values),
        )

    def recent_points(
        self,
        doc_id: str,
        metric: str,
        window_seconds: float,
        now: Optional[float] = None,
    ) -> list[WindowPoint]:
        """Return points inside the window, sorted by timestamp ascending."""
        with self._lock:
            return self._points_in_window(doc_id, metric, window_seconds, now)

    def rolling_average(
        self,
        doc_id: str,
        metric: str,
        window_seconds: float,
        now: Optional[float] = None,
    ) -> Optional[float]:
        """Average of values inside the window; ``None`` if no points."""
        stats = self.window_stats(doc_id, metric, window_seconds, now)
        return None if stats is None else stats.avg

    def rolling_sum(
        self,
        doc_id: str,
        metric: str,
        window_seconds: float,
        now: Optional[float] = None,
    ) -> Optional[float]:
        """Sum of values inside the window; ``None`` if no points."""
        stats = self.window_stats(doc_id, metric, window_seconds, now)
        return None if stats is None else stats.sum

    # -------------------------------------------------------------- mutating

    def prune_before(self, timestamp: float) -> int:
        """Remove points strictly older than ``timestamp``.

        Returns
        -------
        int
            Number of points removed.
        """
        cutoff = float(timestamp)
        with self._lock:
            kept: list[WindowPoint] = []
            removed = 0
            for p in self._points:
                if p.timestamp < cutoff:
                    removed += 1
                else:
                    kept.append(p)
            self._points = kept
            # Rebuild secondary index.
            new_index: dict[tuple, list[int]] = {}
            for i, p in enumerate(self._points):
                new_index.setdefault((p.doc_id, p.metric), []).append(i)
            self._by_key = new_index
            return removed

    def clear_doc(self, doc_id: str) -> int:
        """Remove all points for ``doc_id``. Returns number of removed points."""
        with self._lock:
            kept: list[WindowPoint] = []
            removed = 0
            for p in self._points:
                if p.doc_id == doc_id:
                    removed += 1
                else:
                    kept.append(p)
            self._points = kept
            new_index: dict[tuple, list[int]] = {}
            for i, p in enumerate(self._points):
                new_index.setdefault((p.doc_id, p.metric), []).append(i)
            self._by_key = new_index
            return removed

    def clear_metric(self, metric: str) -> int:
        """Remove all points whose metric matches. Returns count removed."""
        with self._lock:
            kept: list[WindowPoint] = []
            removed = 0
            for p in self._points:
                if p.metric == metric:
                    removed += 1
                else:
                    kept.append(p)
            self._points = kept
            new_index: dict[tuple, list[int]] = {}
            for i, p in enumerate(self._points):
                new_index.setdefault((p.doc_id, p.metric), []).append(i)
            self._by_key = new_index
            return removed

    def clear_all(self) -> int:
        """Remove every recorded point. Returns count removed."""
        with self._lock:
            removed = len(self._points)
            self._points = []
            self._by_key = {}
            return removed

    # ------------------------------------------------------------- listings

    def metrics_for_doc(self, doc_id: str) -> list[str]:
        """Sorted unique list of metric names recorded for ``doc_id``."""
        with self._lock:
            seen = {
                key[1]
                for key in self._by_key
                if key[0] == doc_id and self._by_key[key]
            }
        return sorted(seen)

    def docs_for_metric(self, metric: str) -> list[str]:
        """Sorted unique list of doc ids that recorded ``metric``."""
        with self._lock:
            seen = {
                key[0]
                for key in self._by_key
                if key[1] == metric and self._by_key[key]
            }
        return sorted(seen)

    def all_doc_ids(self) -> list[str]:
        """Sorted unique list of all known doc ids."""
        with self._lock:
            seen = {key[0] for key, idxs in self._by_key.items() if idxs}
        return sorted(seen)

    # ----------------------------------------------------------------- stats

    def stats(self) -> MetricStats:
        """Return global :class:`MetricStats`."""
        with self._lock:
            total = len(self._points)
            metrics = {p.metric for p in self._points}
            docs = {p.doc_id for p in self._points}
            return MetricStats(
                total_points=total,
                unique_metrics=len(metrics),
                unique_docs=len(docs),
            )
