"""SQLite-backed attribute (key-value) store per entity.

Provides bulk operations, automatic type coercion, and optional
change history.  Uses only the Python standard library (``sqlite3``,
``json``, ``threading``).
"""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from dataclasses import dataclass
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class AttributeValue:
    """A single typed attribute belonging to an entity."""

    entity_id: str
    key: str
    value: Any
    value_type: str
    updated_at: float


@dataclass
class AttributeChange:
    """A single change to an attribute (kept in the history table)."""

    entity_id: str
    key: str
    old_value: Any
    new_value: Any
    timestamp: float


# ---------------------------------------------------------------------------
# Type coercion helpers
# ---------------------------------------------------------------------------


def _detect_type(value: Any) -> str:
    """Return the ``value_type`` string for a Python value."""
    # ``bool`` is a subclass of ``int`` in Python — check it first.
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "string"
    if isinstance(value, (list, dict)):
        return "json"
    raise TypeError(
        f"Unsupported attribute value type: {type(value).__name__}"
    )


def _encode(value: Any, value_type: str) -> str:
    """Encode a Python value into its TEXT representation."""
    if value_type == "bool":
        return "1" if value else "0"
    if value_type == "int":
        return str(int(value))
    if value_type == "float":
        return repr(float(value))
    if value_type == "string":
        return str(value)
    if value_type == "json":
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    raise ValueError(f"Unknown value_type: {value_type}")


def _decode(raw: str, value_type: str) -> Any:
    """Decode a TEXT value back into its Python representation."""
    if value_type == "bool":
        return raw == "1"
    if value_type == "int":
        return int(raw)
    if value_type == "float":
        return float(raw)
    if value_type == "string":
        return raw
    if value_type == "json":
        return json.loads(raw)
    raise ValueError(f"Unknown value_type: {value_type}")


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class AttributeStore:
    """SQLite-backed attribute store with optional change history.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` for an
        in-memory database (default).
    track_history:
        If ``True``, every ``set``/``delete`` writes an entry into the
        ``history`` table.  Disabled by default.
    """

    _CREATE_ATTRIBUTES = """
    CREATE TABLE IF NOT EXISTS attributes (
        entity_id  TEXT NOT NULL,
        key        TEXT NOT NULL,
        value      TEXT,
        value_type TEXT NOT NULL,
        updated_at REAL NOT NULL,
        PRIMARY KEY (entity_id, key)
    )
    """

    _CREATE_HISTORY = """
    CREATE TABLE IF NOT EXISTS history (
        entity_id  TEXT NOT NULL,
        key        TEXT NOT NULL,
        old_value  TEXT,
        new_value  TEXT,
        old_type   TEXT,
        new_type   TEXT,
        timestamp  REAL NOT NULL
    )
    """

    _CREATE_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_attr_entity ON attributes (entity_id)",
        "CREATE INDEX IF NOT EXISTS idx_attr_key    ON attributes (key)",
        "CREATE INDEX IF NOT EXISTS idx_hist_entity ON history (entity_id)",
        "CREATE INDEX IF NOT EXISTS idx_hist_key    ON history (key)",
    ]

    def __init__(
        self,
        db_path: str = ":memory:",
        track_history: bool = False,
    ) -> None:
        self._db_path = db_path
        self._track_history = bool(track_history)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(self._CREATE_ATTRIBUTES)
        self._conn.execute(self._CREATE_HISTORY)
        for stmt in self._CREATE_INDEXES:
            self._conn.execute(stmt)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _now(self, now: float) -> float:
        return now if now else time.time()

    def _row_to_attribute(self, row: tuple) -> AttributeValue:
        entity_id, key, raw, value_type, updated_at = row
        return AttributeValue(
            entity_id=entity_id,
            key=key,
            value=_decode(raw, value_type),
            value_type=value_type,
            updated_at=updated_at,
        )

    def _record_history(
        self,
        entity_id: str,
        key: str,
        old_raw: Optional[str],
        old_type: Optional[str],
        new_raw: Optional[str],
        new_type: Optional[str],
        ts: float,
    ) -> None:
        if not self._track_history:
            return
        self._conn.execute(
            "INSERT INTO history "
            "(entity_id, key, old_value, new_value, old_type, new_type, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (entity_id, key, old_raw, new_raw, old_type, new_type, ts),
        )

    def _fetch_raw(
        self, entity_id: str, key: str
    ) -> Optional[tuple]:
        cur = self._conn.execute(
            "SELECT value, value_type FROM attributes "
            "WHERE entity_id = ? AND key = ?",
            (entity_id, key),
        )
        return cur.fetchone()

    # ------------------------------------------------------------------
    # Single-attribute operations
    # ------------------------------------------------------------------

    def set(
        self,
        entity_id: str,
        key: str,
        value: Any,
        now: float = 0.0,
    ) -> AttributeValue:
        """Upsert an attribute and return its new value."""
        value_type = _detect_type(value)
        encoded = _encode(value, value_type)
        ts = self._now(now)
        with self._lock:
            existing = self._fetch_raw(entity_id, key)
            old_raw = existing[0] if existing else None
            old_type = existing[1] if existing else None
            self._conn.execute(
                "INSERT INTO attributes "
                "(entity_id, key, value, value_type, updated_at) "
                "VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(entity_id, key) DO UPDATE SET "
                "value = excluded.value, "
                "value_type = excluded.value_type, "
                "updated_at = excluded.updated_at",
                (entity_id, key, encoded, value_type, ts),
            )
            self._record_history(
                entity_id, key, old_raw, old_type, encoded, value_type, ts
            )
            self._conn.commit()
        return AttributeValue(
            entity_id=entity_id,
            key=key,
            value=value,
            value_type=value_type,
            updated_at=ts,
        )

    def get(self, entity_id: str, key: str, default: Any = None) -> Any:
        """Return the decoded value for an attribute, or ``default``."""
        with self._lock:
            row = self._fetch_raw(entity_id, key)
        if row is None:
            return default
        return _decode(row[0], row[1])

    def get_typed(
        self, entity_id: str, key: str
    ) -> Optional[AttributeValue]:
        """Return the full :class:`AttributeValue` for an attribute."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT entity_id, key, value, value_type, updated_at "
                "FROM attributes WHERE entity_id = ? AND key = ?",
                (entity_id, key),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return self._row_to_attribute(row)

    def has(self, entity_id: str, key: str) -> bool:
        """Return ``True`` if the attribute exists."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT 1 FROM attributes WHERE entity_id = ? AND key = ? LIMIT 1",
                (entity_id, key),
            )
            return cur.fetchone() is not None

    def delete(self, entity_id: str, key: str) -> bool:
        """Delete a single attribute.  Returns ``True`` if it existed."""
        ts = self._now(0.0)
        with self._lock:
            existing = self._fetch_raw(entity_id, key)
            if existing is None:
                return False
            self._conn.execute(
                "DELETE FROM attributes WHERE entity_id = ? AND key = ?",
                (entity_id, key),
            )
            self._record_history(
                entity_id, key, existing[0], existing[1], None, None, ts
            )
            self._conn.commit()
        return True

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------

    def set_many(
        self,
        entity_id: str,
        attributes: dict,
        now: float = 0.0,
    ) -> list:
        """Upsert multiple attributes for one entity."""
        ts = self._now(now)
        results: list = []
        with self._lock:
            for key, value in attributes.items():
                value_type = _detect_type(value)
                encoded = _encode(value, value_type)
                existing = self._fetch_raw(entity_id, key)
                old_raw = existing[0] if existing else None
                old_type = existing[1] if existing else None
                self._conn.execute(
                    "INSERT INTO attributes "
                    "(entity_id, key, value, value_type, updated_at) "
                    "VALUES (?, ?, ?, ?, ?) "
                    "ON CONFLICT(entity_id, key) DO UPDATE SET "
                    "value = excluded.value, "
                    "value_type = excluded.value_type, "
                    "updated_at = excluded.updated_at",
                    (entity_id, key, encoded, value_type, ts),
                )
                self._record_history(
                    entity_id, key, old_raw, old_type, encoded, value_type, ts
                )
                results.append(
                    AttributeValue(
                        entity_id=entity_id,
                        key=key,
                        value=value,
                        value_type=value_type,
                        updated_at=ts,
                    )
                )
            self._conn.commit()
        return results

    def get_all(self, entity_id: str) -> dict:
        """Return all attributes of an entity as a ``{key: value}`` dict."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT key, value, value_type FROM attributes "
                "WHERE entity_id = ?",
                (entity_id,),
            )
            rows = cur.fetchall()
        return {key: _decode(raw, vtype) for key, raw, vtype in rows}

    def delete_entity(self, entity_id: str) -> int:
        """Delete every attribute belonging to an entity.

        Returns the number of attributes deleted.
        """
        ts = self._now(0.0)
        with self._lock:
            cur = self._conn.execute(
                "SELECT key, value, value_type FROM attributes "
                "WHERE entity_id = ?",
                (entity_id,),
            )
            rows = cur.fetchall()
            count = len(rows)
            if count == 0:
                return 0
            self._conn.execute(
                "DELETE FROM attributes WHERE entity_id = ?",
                (entity_id,),
            )
            for key, old_raw, old_type in rows:
                self._record_history(
                    entity_id, key, old_raw, old_type, None, None, ts
                )
            self._conn.commit()
        return count

    # ------------------------------------------------------------------
    # Search / aggregation
    # ------------------------------------------------------------------

    def entities_with_key(self, key: str) -> list:
        """Return a list of entity ids that have the given attribute key."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT DISTINCT entity_id FROM attributes WHERE key = ? "
                "ORDER BY entity_id",
                (key,),
            )
            return [row[0] for row in cur.fetchall()]

    def entities_with_value(self, key: str, value: Any) -> list:
        """Return entity ids where ``key`` has the exact value ``value``."""
        value_type = _detect_type(value)
        encoded = _encode(value, value_type)
        with self._lock:
            cur = self._conn.execute(
                "SELECT entity_id FROM attributes "
                "WHERE key = ? AND value = ? AND value_type = ? "
                "ORDER BY entity_id",
                (key, encoded, value_type),
            )
            return [row[0] for row in cur.fetchall()]

    def count_entities(self) -> int:
        """Return the number of distinct entities currently stored."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(DISTINCT entity_id) FROM attributes"
            )
            return int(cur.fetchone()[0])

    def count_attributes(self, entity_id: Optional[str] = None) -> int:
        """Return the number of attributes (optionally for one entity)."""
        with self._lock:
            if entity_id is None:
                cur = self._conn.execute(
                    "SELECT COUNT(*) FROM attributes"
                )
            else:
                cur = self._conn.execute(
                    "SELECT COUNT(*) FROM attributes WHERE entity_id = ?",
                    (entity_id,),
                )
            return int(cur.fetchone()[0])

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    def history(
        self, entity_id: str, key: Optional[str] = None
    ) -> list:
        """Return the history of changes for an entity (and optional key).

        Only returns rows when ``track_history`` was enabled at
        construction time; otherwise returns an empty list.
        """
        if not self._track_history:
            return []
        with self._lock:
            if key is None:
                cur = self._conn.execute(
                    "SELECT entity_id, key, old_value, new_value, "
                    "old_type, new_type, timestamp FROM history "
                    "WHERE entity_id = ? ORDER BY timestamp ASC, ROWID ASC",
                    (entity_id,),
                )
            else:
                cur = self._conn.execute(
                    "SELECT entity_id, key, old_value, new_value, "
                    "old_type, new_type, timestamp FROM history "
                    "WHERE entity_id = ? AND key = ? "
                    "ORDER BY timestamp ASC, ROWID ASC",
                    (entity_id, key),
                )
            rows = cur.fetchall()
        out: list = []
        for eid, k, old_raw, new_raw, old_type, new_type, ts in rows:
            old_val = _decode(old_raw, old_type) if old_type else None
            new_val = _decode(new_raw, new_type) if new_type else None
            out.append(
                AttributeChange(
                    entity_id=eid,
                    key=k,
                    old_value=old_val,
                    new_value=new_val,
                    timestamp=ts,
                )
            )
        return out

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove every attribute and history entry."""
        with self._lock:
            self._conn.execute("DELETE FROM attributes")
            self._conn.execute("DELETE FROM history")
            self._conn.commit()

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            self._conn.close()
