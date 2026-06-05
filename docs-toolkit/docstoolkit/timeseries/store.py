"""SQLite-backed time series store for docs-toolkit.

Pure stdlib implementation — no external dependencies.
"""
from __future__ import annotations

import json
import math
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from docstoolkit.timeseries.point import Aggregation, AggregatedPoint, DataPoint

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class TimeSeriesConfig:
    """Configuration for a TimeSeriesStore.

    Attributes:
        retention_seconds: How long to keep points (seconds).  0 = keep forever.
        max_points:        Maximum total rows per metric.  0 = unlimited.
                           When exceeded on write the oldest point(s) are pruned.
    """

    retention_seconds: float = 0.0
    max_points: int = 0


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS ts_data (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    metric    TEXT    NOT NULL,
    ts        REAL    NOT NULL,
    value     REAL    NOT NULL,
    tags_json TEXT    NOT NULL DEFAULT '{}'
);
"""

_CREATE_IDX_METRIC_TS = """
CREATE INDEX IF NOT EXISTS idx_ts_data_metric_ts ON ts_data (metric, ts);
"""

_CREATE_IDX_METRIC = """
CREATE INDEX IF NOT EXISTS idx_ts_data_metric ON ts_data (metric);
"""


class TimeSeriesStore:
    """Append-only time series store backed by SQLite.

    Example::

        store = TimeSeriesStore()
        store.write(DataPoint(ts=time.time(), value=42.0, metric="cpu"))
        points = store.read("cpu")
        store.close()
    """

    def __init__(
        self,
        db_path: "str | Path" = ":memory:",
        config: Optional[TimeSeriesConfig] = None,
    ) -> None:
        self._config = config or TimeSeriesConfig()
        db_str = str(db_path)
        self._conn = sqlite3.connect(db_str, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA synchronous=NORMAL;")
        self._setup_schema()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _setup_schema(self) -> None:
        with self._conn:
            self._conn.execute(_CREATE_TABLE)
            self._conn.execute(_CREATE_IDX_METRIC_TS)
            self._conn.execute(_CREATE_IDX_METRIC)

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def write(self, point: DataPoint) -> None:
        """Insert a single DataPoint."""
        with self._conn:
            self._conn.execute(
                "INSERT INTO ts_data (metric, ts, value, tags_json) VALUES (?, ?, ?, ?)",
                (point.metric, point.ts, point.value, json.dumps(point.tags or {})),
            )
            if self._config.max_points > 0:
                self._enforce_max_points(point.metric)

    def write_batch(self, points: "list[DataPoint]") -> None:
        """Insert multiple DataPoints in a single transaction."""
        with self._conn:
            self._conn.executemany(
                "INSERT INTO ts_data (metric, ts, value, tags_json) VALUES (?, ?, ?, ?)",
                [
                    (p.metric, p.ts, p.value, json.dumps(p.tags or {}))
                    for p in points
                ],
            )
            if self._config.max_points > 0:
                metrics_seen = {p.metric for p in points}
                for m in metrics_seen:
                    self._enforce_max_points(m)

    def _enforce_max_points(self, metric: str) -> None:
        """Delete oldest points for *metric* if count exceeds max_points."""
        row = self._conn.execute(
            "SELECT COUNT(*) AS n FROM ts_data WHERE metric = ?", (metric,)
        ).fetchone()
        excess = row["n"] - self._config.max_points
        if excess > 0:
            self._conn.execute(
                """
                DELETE FROM ts_data
                WHERE id IN (
                    SELECT id FROM ts_data
                    WHERE metric = ?
                    ORDER BY ts ASC
                    LIMIT ?
                )
                """,
                (metric, excess),
            )

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def read(
        self,
        metric: str,
        since: Optional[float] = None,
        until: Optional[float] = None,
        tags: Optional[dict] = None,
    ) -> "list[DataPoint]":
        """Return DataPoints for *metric*, optionally filtered by time and tags.

        Args:
            metric: Metric name to query.
            since:  Include points with ts >= since.
            until:  Include points with ts <= until.
            tags:   All specified tags must match exactly (subset match).

        Returns:
            List of DataPoint sorted by ts ascending.
        """
        sql = "SELECT metric, ts, value, tags_json FROM ts_data WHERE metric = ?"
        params: list = [metric]

        if since is not None:
            sql += " AND ts >= ?"
            params.append(since)
        if until is not None:
            sql += " AND ts <= ?"
            params.append(until)

        sql += " ORDER BY ts ASC"

        rows = self._conn.execute(sql, params).fetchall()
        result = []
        for row in rows:
            stored_tags: dict = json.loads(row["tags_json"])
            if tags:
                if not all(stored_tags.get(k) == v for k, v in tags.items()):
                    continue
            result.append(
                DataPoint(
                    ts=row["ts"],
                    value=row["value"],
                    tags=stored_tags,
                    metric=row["metric"],
                )
            )
        return result

    # ------------------------------------------------------------------
    # Aggregate
    # ------------------------------------------------------------------

    def aggregate(
        self,
        metric: str,
        aggregation: Aggregation,
        window_seconds: float,
        since: Optional[float] = None,
        until: Optional[float] = None,
    ) -> "list[AggregatedPoint]":
        """Aggregate DataPoints into fixed time windows.

        Each window starts at ``floor(ts / window_seconds) * window_seconds``.

        Args:
            metric:         Metric to aggregate.
            aggregation:    Which aggregation function to apply.
            window_seconds: Width of each time window in seconds.
            since:          Lower bound (inclusive) on ts.
            until:          Upper bound (inclusive) on ts.

        Returns:
            List of AggregatedPoint sorted by window start (ts) ascending.
        """
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")

        points = self.read(metric, since=since, until=until)
        if not points:
            return []

        # Group points by window bucket
        buckets: dict[float, list[float]] = {}
        for p in points:
            bucket = math.floor(p.ts / window_seconds) * window_seconds
            buckets.setdefault(bucket, []).append(p.value)

        result = []
        for bucket_ts in sorted(buckets):
            values = buckets[bucket_ts]
            count = len(values)

            if aggregation is Aggregation.MEAN:
                agg_value = sum(values) / count
            elif aggregation is Aggregation.SUM:
                agg_value = sum(values)
            elif aggregation is Aggregation.MIN:
                agg_value = min(values)
            elif aggregation is Aggregation.MAX:
                agg_value = max(values)
            elif aggregation is Aggregation.COUNT:
                agg_value = float(count)
            elif aggregation is Aggregation.LAST:
                # points are already sorted by ts; last in bucket = last appended
                agg_value = values[-1]
            else:
                raise ValueError(f"Unknown aggregation: {aggregation}")

            result.append(
                AggregatedPoint(ts=bucket_ts, value=agg_value, count=count, metric=metric)
            )

        return result

    # ------------------------------------------------------------------
    # Metadata helpers
    # ------------------------------------------------------------------

    def metrics(self) -> "list[str]":
        """Return sorted list of distinct metric names."""
        rows = self._conn.execute(
            "SELECT DISTINCT metric FROM ts_data ORDER BY metric"
        ).fetchall()
        return [r["metric"] for r in rows]

    def count(self, metric: str) -> int:
        """Return number of stored points for *metric*."""
        row = self._conn.execute(
            "SELECT COUNT(*) AS n FROM ts_data WHERE metric = ?", (metric,)
        ).fetchone()
        return row["n"]

    def latest(self, metric: str) -> Optional[DataPoint]:
        """Return the most recent DataPoint for *metric*, or None if empty."""
        row = self._conn.execute(
            "SELECT metric, ts, value, tags_json FROM ts_data WHERE metric = ? ORDER BY ts DESC LIMIT 1",
            (metric,),
        ).fetchone()
        if row is None:
            return None
        return DataPoint(
            ts=row["ts"],
            value=row["value"],
            tags=json.loads(row["tags_json"]),
            metric=row["metric"],
        )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def cleanup(self, now: Optional[float] = None) -> int:
        """Delete points older than retention_seconds.

        Does nothing if ``retention_seconds`` is 0 (keep forever).

        Args:
            now: Reference timestamp; defaults to ``time.time()``.

        Returns:
            Number of rows deleted.
        """
        if self._config.retention_seconds <= 0:
            return 0

        if now is None:
            now = time.time()

        cutoff = now - self._config.retention_seconds
        with self._conn:
            cursor = self._conn.execute(
                "DELETE FROM ts_data WHERE ts < ?", (cutoff,)
            )
        return cursor.rowcount

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        self._conn.close()
