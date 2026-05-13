"""SQLite-backed EventStore for the E84 event sourcing module."""
import json
import sqlite3

from docstoolkit.event_sourcing.event import Event, EventEnvelope

_SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    sequence     INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id     TEXT    UNIQUE,
    aggregate_id TEXT,
    event_type   TEXT,
    payload      TEXT,
    version      INTEGER,
    timestamp    REAL
);
CREATE INDEX IF NOT EXISTS idx_events_aggregate_id ON events (aggregate_id);
CREATE INDEX IF NOT EXISTS idx_events_event_type   ON events (event_type);
"""


class EventStore:
    """SQLite-backed append-only event store with global sequence ordering.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file. Use ``":memory:"`` (the default) for
        an in-memory database.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def append(self, event: Event) -> int:
        """Insert *event* and return its assigned global sequence number."""
        cur = self._conn.execute(
            "INSERT INTO events "
            "(event_id, aggregate_id, event_type, payload, version, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                event.event_id,
                event.aggregate_id,
                event.event_type,
                json.dumps(event.payload),
                event.version,
                event.timestamp,
            ),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def append_many(self, events: list) -> list:
        """Insert all *events* in a single transaction.

        Returns a list of the assigned sequence numbers in the same order.
        """
        sequences: list = []
        try:
            cur = self._conn.cursor()
            for event in events:
                cur.execute(
                    "INSERT INTO events "
                    "(event_id, aggregate_id, event_type, payload, version, timestamp) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        event.event_id,
                        event.aggregate_id,
                        event.event_type,
                        json.dumps(event.payload),
                        event.version,
                        event.timestamp,
                    ),
                )
                sequences.append(int(cur.lastrowid))
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        return sequences

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_events(
        self,
        aggregate_id: str,
        from_version: int = 0,
        to_version: int = None,
    ) -> list:
        """Return events for *aggregate_id*, ordered by sequence ascending.

        Filters: ``version >= from_version`` and (if provided)
        ``version <= to_version``.
        """
        if to_version is not None:
            rows = self._conn.execute(
                "SELECT * FROM events "
                "WHERE aggregate_id = ? AND version >= ? AND version <= ? "
                "ORDER BY sequence ASC",
                (aggregate_id, from_version, to_version),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM events "
                "WHERE aggregate_id = ? AND version >= ? "
                "ORDER BY sequence ASC",
                (aggregate_id, from_version),
            ).fetchall()
        return [self._row_to_envelope(r) for r in rows]

    def get_by_type(self, event_type: str, limit: int = 100) -> list:
        """Return up to *limit* envelopes with given *event_type*, by sequence."""
        rows = self._conn.execute(
            "SELECT * FROM events WHERE event_type = ? "
            "ORDER BY sequence ASC LIMIT ?",
            (event_type, limit),
        ).fetchall()
        return [self._row_to_envelope(r) for r in rows]

    def get_all(self, from_sequence: int = 0, limit: int = 100) -> list:
        """Return up to *limit* envelopes with ``sequence >= from_sequence``."""
        rows = self._conn.execute(
            "SELECT * FROM events WHERE sequence >= ? "
            "ORDER BY sequence ASC LIMIT ?",
            (from_sequence, limit),
        ).fetchall()
        return [self._row_to_envelope(r) for r in rows]

    def latest_version(self, aggregate_id: str) -> int:
        """Return the highest ``version`` for *aggregate_id*, or ``0`` if none."""
        row = self._conn.execute(
            "SELECT MAX(version) FROM events WHERE aggregate_id = ?",
            (aggregate_id,),
        ).fetchone()
        result = row[0]
        return int(result) if result is not None else 0

    def count(self) -> int:
        """Return total number of events in the store."""
        return int(
            self._conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        self._conn.close()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_envelope(row: sqlite3.Row) -> EventEnvelope:
        event = Event(
            event_id=row["event_id"],
            aggregate_id=row["aggregate_id"],
            event_type=row["event_type"],
            payload=json.loads(row["payload"]),
            version=int(row["version"]),
            timestamp=float(row["timestamp"]),
        )
        return EventEnvelope(event=event, sequence=int(row["sequence"]))
