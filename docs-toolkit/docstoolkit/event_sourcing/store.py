"""SQLite-backed EventStore for persisting DomainEvents."""
import json
import sqlite3
from pathlib import Path

from docstoolkit.event_sourcing.event import DomainEvent

_SCHEMA = """
CREATE TABLE IF NOT EXISTS domain_events (
    event_id        TEXT    PRIMARY KEY,
    event_type      TEXT    NOT NULL,
    aggregate_id    TEXT    NOT NULL,
    aggregate_type  TEXT    NOT NULL,
    payload_json    TEXT    NOT NULL,
    ts              REAL    NOT NULL,
    version         INTEGER NOT NULL,
    metadata_json   TEXT    NOT NULL DEFAULT '{}',
    UNIQUE (aggregate_id, version)
);

CREATE INDEX IF NOT EXISTS idx_de_aggregate ON domain_events (aggregate_id, version);
CREATE INDEX IF NOT EXISTS idx_de_type      ON domain_events (event_type);
CREATE INDEX IF NOT EXISTS idx_de_ts        ON domain_events (ts);
"""


class VersionConflictError(Exception):
    """Raised when an event with the same (aggregate_id, version) already exists."""


class EventStore:
    """Append-only SQLite event store.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``None`` / ``":memory:"`` for an
        in-memory database (default).
    """

    def __init__(self, db_path: "Path | str | None" = None) -> None:
        path = str(db_path) if db_path is not None else ":memory:"
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def append(self, event: DomainEvent) -> None:
        """Persist *event*.

        Raises :class:`VersionConflictError` if an event with the same
        ``(aggregate_id, version)`` pair is already stored.
        """
        try:
            self._conn.execute(
                "INSERT INTO domain_events "
                "(event_id, event_type, aggregate_id, aggregate_type, "
                " payload_json, ts, version, metadata_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event.event_id,
                    event.event_type,
                    event.aggregate_id,
                    event.aggregate_type,
                    json.dumps(event.payload),
                    event.ts,
                    event.version,
                    json.dumps(event.metadata),
                ),
            )
            self._conn.commit()
        except sqlite3.IntegrityError as exc:
            raise VersionConflictError(
                f"Version conflict: aggregate_id={event.aggregate_id!r} "
                f"version={event.version} already exists."
            ) from exc

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_events(
        self, aggregate_id: str, from_version: int = 1
    ) -> "list[DomainEvent]":
        """Return events for *aggregate_id* ordered by version ascending.

        Parameters
        ----------
        aggregate_id:
            The aggregate whose event stream to load.
        from_version:
            Only events with ``version >= from_version`` are returned.
        """
        rows = self._conn.execute(
            "SELECT * FROM domain_events "
            "WHERE aggregate_id = ? AND version >= ? "
            "ORDER BY version ASC",
            (aggregate_id, from_version),
        ).fetchall()
        return [self._row_to_event(r) for r in rows]

    def get_all_events(self, event_type: str = None) -> "list[DomainEvent]":
        """Return all events, optionally filtered by *event_type*, ordered by ts."""
        if event_type is not None:
            rows = self._conn.execute(
                "SELECT * FROM domain_events WHERE event_type = ? ORDER BY ts ASC",
                (event_type,),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM domain_events ORDER BY ts ASC"
            ).fetchall()
        return [self._row_to_event(r) for r in rows]

    def latest_version(self, aggregate_id: str) -> int:
        """Return the highest version stored for *aggregate_id*, or ``0``."""
        row = self._conn.execute(
            "SELECT MAX(version) FROM domain_events WHERE aggregate_id = ?",
            (aggregate_id,),
        ).fetchone()
        result = row[0]
        return result if result is not None else 0

    def snapshot_count(self) -> int:
        """Total number of events in the store."""
        return self._conn.execute(
            "SELECT COUNT(*) FROM domain_events"
        ).fetchone()[0]

    def aggregate_ids(self) -> "list[str]":
        """Return a list of all distinct aggregate IDs."""
        rows = self._conn.execute(
            "SELECT DISTINCT aggregate_id FROM domain_events"
        ).fetchall()
        return [r[0] for r in rows]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_event(row: sqlite3.Row) -> DomainEvent:
        return DomainEvent(
            event_id=row["event_id"],
            event_type=row["event_type"],
            aggregate_id=row["aggregate_id"],
            aggregate_type=row["aggregate_type"],
            payload=json.loads(row["payload_json"]),
            ts=row["ts"],
            version=row["version"],
            metadata=json.loads(row["metadata_json"]),
        )

    def close(self) -> None:
        self._conn.close()
