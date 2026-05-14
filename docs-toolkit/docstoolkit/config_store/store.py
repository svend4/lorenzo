"""Hierarchical, namespaced configuration store backed by SQLite.

Supports dot-notation keys, namespaces, JSON-typed values,
change listeners, and import/export.  Pure stdlib only.
"""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable

__all__ = ["ConfigEntry", "ConfigStore"]

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS config (
    namespace TEXT NOT NULL,
    key       TEXT NOT NULL,
    value     TEXT,
    description TEXT DEFAULT '',
    created_at  REAL,
    updated_at  REAL,
    PRIMARY KEY (namespace, key)
)
"""

_PRAGMA_WAL = "PRAGMA journal_mode=WAL"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class ConfigEntry:
    """A single configuration entry."""

    namespace: str
    key: str          # dot-notation, e.g. "server.port"
    value: Any
    description: str = ""
    created_at: float = 0.0
    updated_at: float = 0.0


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

class ConfigStore:
    """SQLite-backed config store with namespaces and change listeners.

    Parameters
    ----------
    db_path:
        File path for the SQLite database, or ``":memory:"`` (default).
    now_fn:
        Callable that returns the current time as a float (seconds since
        epoch).  Defaults to :func:`time.time`.  Inject a fake clock in
        tests to get deterministic timestamps.

    Example::

        store = ConfigStore()
        store.set("app", "server.port", 8080, description="HTTP port")
        port = store.get("app", "server.port")   # 8080
        store.close()
    """

    def __init__(self, db_path: str = ":memory:", now_fn=None) -> None:
        self._db_path = db_path
        self._now = now_fn if now_fn is not None else time.time
        self._lock = threading.Lock()
        # subscribers: {(namespace, key): [callback, ...]}
        self._subscribers: dict[tuple[str, str], list[Callable]] = {}
        self._conn = self._connect()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute(_PRAGMA_WAL)
        conn.execute(_CREATE_TABLE)
        conn.commit()
        return conn

    @staticmethod
    def _encode(value: Any) -> str:
        return json.dumps(value)

    @staticmethod
    def _decode(raw: str) -> Any:
        return json.loads(raw)

    def _row_to_entry(self, row: sqlite3.Row) -> ConfigEntry:
        return ConfigEntry(
            namespace=row["namespace"],
            key=row["key"],
            value=self._decode(row["value"]),
            description=row["description"] or "",
            created_at=row["created_at"] or 0.0,
            updated_at=row["updated_at"] or 0.0,
        )

    def _fire(self, namespace: str, key: str,
              old_value: Any, new_value: Any) -> None:
        """Invoke registered callbacks for *(namespace, key)*."""
        callbacks = self._subscribers.get((namespace, key), [])
        for cb in callbacks:
            try:
                cb(old_value, new_value)
            except Exception:
                pass  # subscribers must not crash the store

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set(self, namespace: str, key: str, value: Any,
            description: str = "") -> ConfigEntry:
        """Set a config value.  Overwrites if the entry already exists.

        Change listeners are fired only when the stored value actually
        changes (by JSON equality).

        Returns the resulting :class:`ConfigEntry`.
        """
        now = self._now()
        encoded = self._encode(value)
        with self._lock:
            cur = self._conn.execute(
                "SELECT value, created_at FROM config "
                "WHERE namespace=? AND key=?",
                (namespace, key),
            )
            row = cur.fetchone()
            old_value: Any
            if row is None:
                old_value = _MISSING
                created_at = now
                self._conn.execute(
                    "INSERT INTO config "
                    "(namespace, key, value, description, created_at, updated_at) "
                    "VALUES (?,?,?,?,?,?)",
                    (namespace, key, encoded, description, now, now),
                )
            else:
                old_value = self._decode(row["value"])
                created_at = row["created_at"]
                self._conn.execute(
                    "UPDATE config "
                    "SET value=?, description=?, updated_at=? "
                    "WHERE namespace=? AND key=?",
                    (encoded, description, now, namespace, key),
                )
            self._conn.commit()

        entry = ConfigEntry(
            namespace=namespace,
            key=key,
            value=value,
            description=description,
            created_at=created_at,
            updated_at=now,
        )

        # Fire listeners if value changed (new entry counts as changed)
        if old_value is _MISSING or old_value != value:
            self._fire(namespace, key, None if old_value is _MISSING else old_value, value)

        return entry

    def get(self, namespace: str, key: str, default: Any = None) -> Any:
        """Return the stored value for *namespace*/*key*, or *default*."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT value FROM config WHERE namespace=? AND key=?",
                (namespace, key),
            )
            row = cur.fetchone()
        if row is None:
            return default
        return self._decode(row["value"])

    def get_entry(self, namespace: str, key: str) -> "ConfigEntry | None":
        """Return the full :class:`ConfigEntry`, or *None* if not found."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT * FROM config WHERE namespace=? AND key=?",
                (namespace, key),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return self._row_to_entry(row)

    def delete(self, namespace: str, key: str) -> bool:
        """Delete the entry.  Returns *True* if it existed, *False* otherwise."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT value FROM config WHERE namespace=? AND key=?",
                (namespace, key),
            )
            row = cur.fetchone()
            if row is None:
                return False
            old_value = self._decode(row["value"])
            self._conn.execute(
                "DELETE FROM config WHERE namespace=? AND key=?",
                (namespace, key),
            )
            self._conn.commit()

        self._fire(namespace, key, old_value, None)
        return True

    def list(self, namespace: str,
             prefix: str | None = None) -> list[ConfigEntry]:
        """Return all entries for *namespace*, optionally filtered by key prefix."""
        with self._lock:
            if prefix is None:
                cur = self._conn.execute(
                    "SELECT * FROM config WHERE namespace=? ORDER BY key",
                    (namespace,),
                )
            else:
                cur = self._conn.execute(
                    "SELECT * FROM config "
                    "WHERE namespace=? AND key LIKE ? ESCAPE '\\' ORDER BY key",
                    (namespace, _like_prefix(prefix)),
                )
            rows = cur.fetchall()
        return [self._row_to_entry(r) for r in rows]

    def namespaces(self) -> list[str]:
        """Return all distinct namespaces in sorted order."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT DISTINCT namespace FROM config ORDER BY namespace"
            )
            rows = cur.fetchall()
        return [r["namespace"] for r in rows]

    def subscribe(self, namespace: str, key: str,
                  callback: Callable[[Any, Any], None]) -> None:
        """Register *callback(old_value, new_value)* for *(namespace, key)*.

        Multiple callbacks per key are supported and called in registration
        order.  Callbacks are **not** persisted to the database.
        """
        k = (namespace, key)
        self._subscribers.setdefault(k, []).append(callback)

    def export_namespace(self, namespace: str) -> dict:
        """Export all entries in *namespace* as ``{key: value}`` dict."""
        return {e.key: e.value for e in self.list(namespace)}

    def import_namespace(self, namespace: str, data: dict,
                         overwrite: bool = True) -> int:
        """Import ``{key: value}`` pairs into *namespace*.

        Parameters
        ----------
        overwrite:
            When *True* (default) existing keys are updated.
            When *False* existing keys are left untouched.

        Returns
        -------
        int
            Number of entries actually written (inserted or updated).
        """
        count = 0
        for key, value in data.items():
            if not overwrite:
                existing = self.get_entry(namespace, key)
                if existing is not None:
                    continue
            self.set(namespace, key, value)
            count += 1
        return count

    def count(self, namespace: str | None = None) -> int:
        """Return total entry count, or count within *namespace* if given."""
        with self._lock:
            if namespace is None:
                cur = self._conn.execute("SELECT COUNT(*) FROM config")
            else:
                cur = self._conn.execute(
                    "SELECT COUNT(*) FROM config WHERE namespace=?",
                    (namespace,),
                )
            return cur.fetchone()[0]

    def clear_namespace(self, namespace: str) -> int:
        """Delete all entries in *namespace*.  Returns count deleted."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(*) FROM config WHERE namespace=?",
                (namespace,),
            )
            n = cur.fetchone()[0]
            self._conn.execute(
                "DELETE FROM config WHERE namespace=?",
                (namespace,),
            )
            self._conn.commit()
        return n

    def close(self) -> None:
        """Close the underlying database connection."""
        with self._lock:
            self._conn.close()


# ---------------------------------------------------------------------------
# Internal sentinel / helpers
# ---------------------------------------------------------------------------

class _MissingType:
    """Sentinel for 'no prior value'."""
    __slots__ = ()


_MISSING = _MissingType()


def _like_prefix(prefix: str) -> str:
    """Return a LIKE pattern that matches *prefix* followed by anything.

    Escapes ``%`` and ``_`` so they are treated as literals.
    """
    escaped = prefix.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return escaped + "%"
