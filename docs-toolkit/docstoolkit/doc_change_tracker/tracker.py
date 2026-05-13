"""SQLite-backed document change tracker with batching and timeline support."""
from __future__ import annotations

import sqlite3
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4


class ChangeType(str, Enum):
    """Enumeration of supported document change types."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    RENAME = "RENAME"
    TAG = "TAG"
    COMMENT = "COMMENT"


@dataclass
class ChangeEvent:
    """Represents a single document change event."""

    event_id: int
    doc_id: str
    change_type: ChangeType
    actor: str
    timestamp: float
    description: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None
    batch_id: Optional[str] = None


@dataclass
class ChangeBatch:
    """A logical group of change events produced by a single actor."""

    batch_id: str
    actor: str
    started_at: float
    ended_at: float
    events: list = field(default_factory=list)


@dataclass
class TimelineEntry:
    """One bucket in the timeline aggregation."""

    timestamp: float
    event_count: int
    event_types: dict = field(default_factory=dict)
    actors: set = field(default_factory=set)


class DocChangeTracker:
    """SQLite-backed tracker for document change events and batches.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` (default).
    """

    _CREATE_EVENTS = """
    CREATE TABLE IF NOT EXISTS events (
        event_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id      TEXT NOT NULL,
        change_type TEXT NOT NULL,
        actor       TEXT NOT NULL,
        timestamp   REAL NOT NULL,
        description TEXT,
        before      TEXT,
        after       TEXT,
        batch_id    TEXT
    )
    """

    _CREATE_BATCHES = """
    CREATE TABLE IF NOT EXISTS batches (
        batch_id   TEXT PRIMARY KEY,
        actor      TEXT NOT NULL,
        started_at REAL NOT NULL,
        ended_at   REAL NOT NULL
    )
    """

    _CREATE_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_evt_doc       ON events (doc_id)",
        "CREATE INDEX IF NOT EXISTS idx_evt_actor     ON events (actor)",
        "CREATE INDEX IF NOT EXISTS idx_evt_type      ON events (change_type)",
        "CREATE INDEX IF NOT EXISTS idx_evt_ts        ON events (timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_evt_batch     ON events (batch_id)",
    ]

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._setup()

    # ------------------------------------------------------------------
    # Setup / helpers
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(self._CREATE_EVENTS)
            cur.execute(self._CREATE_BATCHES)
            for stmt in self._CREATE_INDEXES:
                cur.execute(stmt)
            self._conn.commit()

    @staticmethod
    def _row_to_event(row: sqlite3.Row) -> ChangeEvent:
        return ChangeEvent(
            event_id=row["event_id"],
            doc_id=row["doc_id"],
            change_type=ChangeType(row["change_type"]),
            actor=row["actor"],
            timestamp=row["timestamp"],
            description=row["description"],
            before=row["before"],
            after=row["after"],
            batch_id=row["batch_id"],
        )

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record(
        self,
        doc_id: str,
        change_type: ChangeType,
        actor: str,
        description: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        now: float = 0.0,
        batch_id: Optional[str] = None,
    ) -> ChangeEvent:
        """Record a change event and return it."""
        ts = now if now else time.time()
        if not isinstance(change_type, ChangeType):
            change_type = ChangeType(change_type)
        with self._lock:
            cur = self._conn.execute(
                """
                INSERT INTO events
                    (doc_id, change_type, actor, timestamp,
                     description, before, after, batch_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    doc_id,
                    change_type.value,
                    actor,
                    ts,
                    description,
                    before,
                    after,
                    batch_id,
                ),
            )
            event_id = cur.lastrowid
            self._conn.commit()
        return ChangeEvent(
            event_id=event_id,
            doc_id=doc_id,
            change_type=change_type,
            actor=actor,
            timestamp=ts,
            description=description,
            before=before,
            after=after,
            batch_id=batch_id,
        )

    # ------------------------------------------------------------------
    # Batches
    # ------------------------------------------------------------------

    def start_batch(self, actor: str, now: float = 0.0) -> str:
        """Open a new batch and return its id."""
        ts = now if now else time.time()
        batch_id = uuid4().hex[:16]
        with self._lock:
            self._conn.execute(
                "INSERT INTO batches (batch_id, actor, started_at, ended_at) "
                "VALUES (?, ?, ?, ?)",
                (batch_id, actor, ts, ts),
            )
            self._conn.commit()
        return batch_id

    def end_batch(self, batch_id: str, now: float = 0.0) -> Optional[ChangeBatch]:
        """Close a batch and return the populated :class:`ChangeBatch`."""
        ts = now if now else time.time()
        with self._lock:
            row = self._conn.execute(
                "SELECT batch_id FROM batches WHERE batch_id = ?", (batch_id,)
            ).fetchone()
            if row is None:
                return None
            self._conn.execute(
                "UPDATE batches SET ended_at = ? WHERE batch_id = ?",
                (ts, batch_id),
            )
            self._conn.commit()
        return self.get_batch(batch_id)

    def get_batch(self, batch_id: str) -> Optional[ChangeBatch]:
        """Return the batch and all its events (chronological)."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM batches WHERE batch_id = ?", (batch_id,)
            ).fetchone()
            if row is None:
                return None
            event_rows = self._conn.execute(
                "SELECT * FROM events WHERE batch_id = ? ORDER BY timestamp ASC, event_id ASC",
                (batch_id,),
            ).fetchall()
        return ChangeBatch(
            batch_id=row["batch_id"],
            actor=row["actor"],
            started_at=row["started_at"],
            ended_at=row["ended_at"],
            events=[self._row_to_event(r) for r in event_rows],
        )

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def events_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> list:
        """Return events for *doc_id*, newest first."""
        sql = "SELECT * FROM events WHERE doc_id = ? ORDER BY timestamp DESC, event_id DESC"
        params: list = [doc_id]
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_event(r) for r in rows]

    def events_by_actor(
        self, actor: str, limit: Optional[int] = None
    ) -> list:
        """Return events made by *actor*, newest first."""
        sql = "SELECT * FROM events WHERE actor = ? ORDER BY timestamp DESC, event_id DESC"
        params: list = [actor]
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_event(r) for r in rows]

    def events_in_range(self, start: float, end: float) -> list:
        """Return events whose timestamp lies inside ``[start, end]`` (newest first)."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM events WHERE timestamp >= ? AND timestamp <= ? "
                "ORDER BY timestamp DESC, event_id DESC",
                (start, end),
            ).fetchall()
        return [self._row_to_event(r) for r in rows]

    def events_by_type(
        self, change_type: ChangeType, limit: Optional[int] = None
    ) -> list:
        """Return events filtered by *change_type*, newest first."""
        if not isinstance(change_type, ChangeType):
            change_type = ChangeType(change_type)
        sql = (
            "SELECT * FROM events WHERE change_type = ? "
            "ORDER BY timestamp DESC, event_id DESC"
        )
        params: list = [change_type.value]
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_event(r) for r in rows]

    # ------------------------------------------------------------------
    # Timeline
    # ------------------------------------------------------------------

    def timeline(
        self, start: float, end: float, bucket_size: float = 3600.0
    ) -> list:
        """Return :class:`TimelineEntry` rows bucketed by *bucket_size* seconds.

        Buckets are emitted in ascending order. Only non-empty buckets are
        included.
        """
        if bucket_size <= 0:
            raise ValueError("bucket_size must be > 0")
        with self._lock:
            rows = self._conn.execute(
                "SELECT timestamp, change_type, actor FROM events "
                "WHERE timestamp >= ? AND timestamp <= ? "
                "ORDER BY timestamp ASC",
                (start, end),
            ).fetchall()

        buckets: dict = {}
        for r in rows:
            bucket_idx = int((r["timestamp"] - start) // bucket_size)
            bucket_ts = start + bucket_idx * bucket_size
            entry = buckets.get(bucket_idx)
            if entry is None:
                entry = TimelineEntry(
                    timestamp=bucket_ts,
                    event_count=0,
                    event_types={},
                    actors=set(),
                )
                buckets[bucket_idx] = entry
            entry.event_count += 1
            entry.event_types[r["change_type"]] = (
                entry.event_types.get(r["change_type"], 0) + 1
            )
            entry.actors.add(r["actor"])
        return [buckets[k] for k in sorted(buckets)]

    # ------------------------------------------------------------------
    # Aggregate helpers
    # ------------------------------------------------------------------

    def actors_for_doc(self, doc_id: str) -> set:
        """Return the set of actors that have ever touched *doc_id*."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT DISTINCT actor FROM events WHERE doc_id = ?", (doc_id,)
            ).fetchall()
        return {r["actor"] for r in rows}

    def last_change(self, doc_id: str) -> Optional[ChangeEvent]:
        """Return the most recent event for *doc_id*, or ``None``."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM events WHERE doc_id = ? "
                "ORDER BY timestamp DESC, event_id DESC LIMIT 1",
                (doc_id,),
            ).fetchone()
        return self._row_to_event(row) if row else None

    def count_for_doc(self, doc_id: str) -> int:
        """Return the number of events recorded for *doc_id*."""
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) FROM events WHERE doc_id = ?", (doc_id,)
            ).fetchone()
        return row[0]

    @property
    def total_events(self) -> int:
        """Return total number of events across all documents."""
        with self._lock:
            row = self._conn.execute("SELECT COUNT(*) FROM events").fetchone()
        return row[0]

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove every event and batch from the tracker."""
        with self._lock:
            self._conn.execute("DELETE FROM events")
            self._conn.execute("DELETE FROM batches")
            self._conn.commit()

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            self._conn.close()
