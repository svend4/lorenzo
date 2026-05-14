"""SQLite-backed recorded event log supporting filtered replay and point-in-time recovery."""
import json
import sqlite3
import threading
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Protocol


@dataclass
class RecordedEvent:
    """A single recorded event from the document event log."""

    event_id: int = 0
    event_type: str = ""
    doc_id: str = ""
    payload: dict = field(default_factory=dict)
    timestamp: float = 0.0
    actor: Optional[str] = None


@dataclass
class ReplayResult:
    """Outcome of a replay invocation."""

    events_replayed: int = 0
    events_skipped: int = 0
    errors: List[str] = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0
    success: bool = True


@dataclass
class ReplayFilter:
    """Filter specification applied during replay.

    ``None`` for any field disables that constraint.
    """

    event_types: Optional[List[str]] = None
    doc_ids: Optional[List[str]] = None
    actors: Optional[List[str]] = None
    start: Optional[float] = None
    end: Optional[float] = None

    def matches(self, event: RecordedEvent) -> bool:
        """Return True iff *event* matches all configured constraints."""
        if self.event_types is not None and event.event_type not in self.event_types:
            return False
        if self.doc_ids is not None and event.doc_id not in self.doc_ids:
            return False
        if self.actors is not None and event.actor not in self.actors:
            return False
        if self.start is not None and event.timestamp < self.start:
            return False
        if self.end is not None and event.timestamp > self.end:
            return False
        return True


class EventHandler(Protocol):
    """Protocol for event-replay handler callables.

    A handler receives a :class:`RecordedEvent` and returns ``True`` to mark
    the event as replayed, or ``False`` to mark it as skipped.  Any raised
    exception is captured into :attr:`ReplayResult.errors`.
    """

    def __call__(self, event: RecordedEvent) -> bool:  # pragma: no cover - protocol
        ...


class DocEventReplay:
    """SQLite-backed recorded event log with replay and point-in-time recovery.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` (default).
    """

    _CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS events (
        event_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT    NOT NULL,
        doc_id     TEXT    NOT NULL,
        payload    TEXT    NOT NULL DEFAULT '{}',
        timestamp  REAL    NOT NULL DEFAULT 0,
        actor      TEXT
    )
    """

    _CREATE_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_evt_type      ON events (event_type)",
        "CREATE INDEX IF NOT EXISTS idx_evt_doc_id    ON events (doc_id)",
        "CREATE INDEX IF NOT EXISTS idx_evt_actor     ON events (actor)",
        "CREATE INDEX IF NOT EXISTS idx_evt_timestamp ON events (timestamp)",
    ]

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._setup()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(self._CREATE_TABLE)
            for stmt in self._CREATE_INDEXES:
                cur.execute(stmt)
            self._conn.commit()

    @staticmethod
    def _row_to_event(row: sqlite3.Row) -> RecordedEvent:
        return RecordedEvent(
            event_id=row["event_id"],
            event_type=row["event_type"],
            doc_id=row["doc_id"],
            payload=json.loads(row["payload"]),
            timestamp=row["timestamp"],
            actor=row["actor"],
        )

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record(
        self,
        event_type: str,
        doc_id: str,
        payload: dict,
        actor: Optional[str] = None,
        now: float = 0.0,
    ) -> RecordedEvent:
        """Append an event to the log and return the :class:`RecordedEvent`."""
        payload_dict = dict(payload) if payload is not None else {}
        with self._lock:
            cur = self._conn.execute(
                """
                INSERT INTO events (event_type, doc_id, payload, timestamp, actor)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    event_type,
                    doc_id,
                    json.dumps(payload_dict),
                    float(now),
                    actor,
                ),
            )
            self._conn.commit()
            event_id = cur.lastrowid
        return RecordedEvent(
            event_id=event_id,
            event_type=event_type,
            doc_id=doc_id,
            payload=payload_dict,
            timestamp=float(now),
            actor=actor,
        )

    # ------------------------------------------------------------------
    # Replay
    # ------------------------------------------------------------------

    def _fetch_for_replay(self, filter: Optional[ReplayFilter]) -> List[RecordedEvent]:
        clauses: List[str] = []
        params: List = []
        if filter is not None:
            if filter.event_types is not None:
                if not filter.event_types:
                    return []
                placeholders = ",".join("?" * len(filter.event_types))
                clauses.append(f"event_type IN ({placeholders})")
                params.extend(filter.event_types)
            if filter.doc_ids is not None:
                if not filter.doc_ids:
                    return []
                placeholders = ",".join("?" * len(filter.doc_ids))
                clauses.append(f"doc_id IN ({placeholders})")
                params.extend(filter.doc_ids)
            if filter.actors is not None:
                if not filter.actors:
                    return []
                # Handle None within actor list (matches NULL in SQL).
                non_null = [a for a in filter.actors if a is not None]
                has_null = any(a is None for a in filter.actors)
                sub_clauses: List[str] = []
                if non_null:
                    placeholders = ",".join("?" * len(non_null))
                    sub_clauses.append(f"actor IN ({placeholders})")
                    params.extend(non_null)
                if has_null:
                    sub_clauses.append("actor IS NULL")
                clauses.append("(" + " OR ".join(sub_clauses) + ")")
            if filter.start is not None:
                clauses.append("timestamp >= ?")
                params.append(filter.start)
            if filter.end is not None:
                clauses.append("timestamp <= ?")
                params.append(filter.end)
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        with self._lock:
            rows = self._conn.execute(
                f"SELECT * FROM events {where} ORDER BY event_id ASC",
                params,
            ).fetchall()
        return [self._row_to_event(r) for r in rows]

    def replay(
        self,
        handler: Callable[[RecordedEvent], bool],
        filter: Optional[ReplayFilter] = None,
    ) -> ReplayResult:
        """Apply *handler* to every event matching *filter* (chronological order).

        ``handler`` returning ``True`` increments ``events_replayed``;
        ``False`` increments ``events_skipped``; an exception is captured
        in ``errors`` (the event is also counted as skipped).  The result's
        ``start_time``/``end_time`` are the timestamps of the first and
        last *matching* events (0.0 if empty).
        """
        events = self._fetch_for_replay(filter)
        result = ReplayResult(success=True)
        if events:
            result.start_time = events[0].timestamp
            result.end_time = events[-1].timestamp
        for event in events:
            try:
                handled = handler(event)
            except Exception as exc:  # noqa: BLE001 - capture-and-continue is intentional
                result.errors.append(
                    f"event_id={event.event_id}: {type(exc).__name__}: {exc}"
                )
                result.events_skipped += 1
                result.success = False
                continue
            if handled:
                result.events_replayed += 1
            else:
                result.events_skipped += 1
        return result

    def replay_range(
        self,
        handler: Callable[[RecordedEvent], bool],
        start: float,
        end: float,
    ) -> ReplayResult:
        """Replay all events with ``start <= timestamp <= end``."""
        return self.replay(handler, ReplayFilter(start=start, end=end))

    def replay_to_point(
        self,
        handler: Callable[[RecordedEvent], bool],
        point_in_time: float,
    ) -> ReplayResult:
        """Replay all events with ``timestamp <= point_in_time``."""
        return self.replay(handler, ReplayFilter(end=point_in_time))

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def count(self, filter: Optional[ReplayFilter] = None) -> int:
        """Return the number of events matching *filter* (or all events)."""
        if filter is None:
            with self._lock:
                row = self._conn.execute(
                    "SELECT COUNT(*) FROM events"
                ).fetchone()
            return row[0]
        # Reuse the fetch logic to avoid duplicating WHERE-building code paths
        # that special-case empty IN-lists / NULL actors.
        return len(self._fetch_for_replay(filter))

    def _events_by(
        self,
        column: str,
        value: str,
        limit: Optional[int] = None,
    ) -> List[RecordedEvent]:
        sql = f"SELECT * FROM events WHERE {column} = ? ORDER BY event_id ASC"
        params: List = [value]
        if limit is not None:
            sql += " LIMIT ?"
            params.append(int(limit))
        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_event(r) for r in rows]

    def events_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> List[RecordedEvent]:
        """Return all events with the given ``doc_id`` (chronological)."""
        return self._events_by("doc_id", doc_id, limit)

    def events_by_actor(
        self, actor: str, limit: Optional[int] = None
    ) -> List[RecordedEvent]:
        """Return all events with the given ``actor`` (chronological)."""
        return self._events_by("actor", actor, limit)

    def events_by_type(
        self, event_type: str, limit: Optional[int] = None
    ) -> List[RecordedEvent]:
        """Return all events with the given ``event_type`` (chronological)."""
        return self._events_by("event_type", event_type, limit)

    def latest_event(self, doc_id: str) -> Optional[RecordedEvent]:
        """Return the most-recently-recorded event for ``doc_id`` (or ``None``)."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM events WHERE doc_id = ? "
                "ORDER BY event_id DESC LIMIT 1",
                (doc_id,),
            ).fetchone()
        return self._row_to_event(row) if row else None

    def get(self, event_id: int) -> Optional[RecordedEvent]:
        """Return the event with id ``event_id`` (or ``None``)."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM events WHERE event_id = ?", (int(event_id),)
            ).fetchone()
        return self._row_to_event(row) if row else None

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def purge_older_than(self, older_than: float, now: float = 0.0) -> int:
        """Drop events whose ``timestamp < now - older_than``.

        Returns the number of events that were removed.
        """
        cutoff = float(now) - float(older_than)
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM events WHERE timestamp < ?", (cutoff,)
            )
            self._conn.commit()
            return cur.rowcount

    def clear(self) -> None:
        """Remove every event from the log."""
        with self._lock:
            self._conn.execute("DELETE FROM events")
            self._conn.commit()

    @property
    def total_events(self) -> int:
        """Total number of events currently in the log."""
        with self._lock:
            row = self._conn.execute("SELECT COUNT(*) FROM events").fetchone()
        return row[0]

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            self._conn.close()
