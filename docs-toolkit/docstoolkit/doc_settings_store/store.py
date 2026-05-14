"""SQLite-backed per-document settings store.

Differs from a generic key-value config store: settings are scoped to a
``doc_id``, every key has an optional registered ``SettingSchema`` (type,
default value, required flag) and child documents can inherit settings
from a parent.  Uses only the Python standard library.
"""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class SettingValue:
    """A single typed setting belonging to a document."""

    doc_id: str
    key: str
    value: Any
    value_type: str  # "int", "float", "bool", "str", "json"
    set_at: float = 0.0


@dataclass
class SettingSchema:
    """Schema definition for a setting key."""

    key: str
    value_type: str
    default: Any = None
    required: bool = False
    description: str = ""


@dataclass
class SettingsStoreStats:
    """Aggregate statistics about a :class:`DocSettingsStore`."""

    total_docs: int
    total_settings: int
    total_schemas: int
    avg_settings_per_doc: float


# ---------------------------------------------------------------------------
# Type coercion helpers
# ---------------------------------------------------------------------------


_VALID_TYPES = {"int", "float", "bool", "str", "json"}


def _coerce(value: Any, value_type: str) -> Any:
    """Coerce a Python value to the requested ``value_type``."""
    if value_type == "bool":
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            low = value.strip().lower()
            if low in ("true", "1", "yes"):
                return True
            if low in ("false", "0", "no", ""):
                return False
            return bool(value)
        return bool(value)
    if value_type == "int":
        if isinstance(value, bool):
            return int(value)
        return int(value)
    if value_type == "float":
        return float(value)
    if value_type == "str":
        return str(value)
    if value_type == "json":
        # store accepts arbitrary JSON-serialisable objects
        json.dumps(value)
        return value
    raise ValueError(f"Unknown value_type: {value_type}")


def _encode(value: Any, value_type: str) -> str:
    """Encode a coerced value into the TEXT representation in SQLite."""
    coerced = _coerce(value, value_type)
    if value_type == "bool":
        return "1" if coerced else "0"
    if value_type == "int":
        return str(int(coerced))
    if value_type == "float":
        return repr(float(coerced))
    if value_type == "str":
        return str(coerced)
    if value_type == "json":
        return json.dumps(coerced, ensure_ascii=False, sort_keys=True)
    raise ValueError(f"Unknown value_type: {value_type}")


def _decode(raw: Optional[str], value_type: str) -> Any:
    """Decode TEXT back into a Python value."""
    if raw is None:
        return None
    if value_type == "bool":
        return raw == "1"
    if value_type == "int":
        return int(raw)
    if value_type == "float":
        return float(raw)
    if value_type == "str":
        return raw
    if value_type == "json":
        return json.loads(raw)
    raise ValueError(f"Unknown value_type: {value_type}")


def _detect_type(value: Any) -> str:
    """Best-effort type detection for unschema'd ``set`` calls."""
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    return "json"


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class DocSettingsStore:
    """SQLite-backed per-document settings store with schema + inheritance."""

    _CREATE_SETTINGS = """
    CREATE TABLE IF NOT EXISTS settings (
        doc_id     TEXT NOT NULL,
        key        TEXT NOT NULL,
        value      TEXT,
        value_type TEXT NOT NULL,
        set_at     REAL NOT NULL,
        PRIMARY KEY (doc_id, key)
    )
    """

    _CREATE_SCHEMAS = """
    CREATE TABLE IF NOT EXISTS schemas (
        key          TEXT PRIMARY KEY,
        value_type   TEXT NOT NULL,
        default_json TEXT,
        required     INTEGER NOT NULL DEFAULT 0,
        description  TEXT NOT NULL DEFAULT ''
    )
    """

    _CREATE_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_settings_doc ON settings (doc_id)",
        "CREATE INDEX IF NOT EXISTS idx_settings_key ON settings (key)",
    ]

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(self._CREATE_SETTINGS)
        self._conn.execute(self._CREATE_SCHEMAS)
        for stmt in self._CREATE_INDEXES:
            self._conn.execute(stmt)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return now if now is not None else time.time()

    def _fetch_raw(
        self, doc_id: str, key: str
    ) -> Optional[tuple]:
        cur = self._conn.execute(
            "SELECT value, value_type, set_at FROM settings "
            "WHERE doc_id = ? AND key = ?",
            (doc_id, key),
        )
        return cur.fetchone()

    def _schema_for_key(self, key: str) -> Optional[SettingSchema]:
        cur = self._conn.execute(
            "SELECT key, value_type, default_json, required, description "
            "FROM schemas WHERE key = ?",
            (key,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        k, vtype, default_json, required, desc = row
        default = json.loads(default_json) if default_json is not None else None
        return SettingSchema(
            key=k,
            value_type=vtype,
            default=default,
            required=bool(required),
            description=desc or "",
        )

    def _resolve_type(self, key: str, value: Any) -> str:
        schema = self._schema_for_key(key)
        if schema is not None:
            return schema.value_type
        return _detect_type(value)

    # ------------------------------------------------------------------
    # Schema management
    # ------------------------------------------------------------------

    def register_schema(
        self,
        key: str,
        value_type: str,
        default: Any = None,
        required: bool = False,
        description: str = "",
    ) -> SettingSchema:
        """Register (or replace) a schema for ``key``."""
        if value_type not in _VALID_TYPES:
            raise ValueError(
                f"Invalid value_type {value_type!r}; "
                f"expected one of {sorted(_VALID_TYPES)}"
            )
        if default is not None:
            # validate that default coerces cleanly
            _coerce(default, value_type)
        default_json = (
            json.dumps(default, ensure_ascii=False, sort_keys=True)
            if default is not None
            else None
        )
        with self._lock:
            self._conn.execute(
                "INSERT INTO schemas (key, value_type, default_json, required, description) "
                "VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(key) DO UPDATE SET "
                "value_type = excluded.value_type, "
                "default_json = excluded.default_json, "
                "required = excluded.required, "
                "description = excluded.description",
                (key, value_type, default_json, 1 if required else 0, description or ""),
            )
            self._conn.commit()
        return SettingSchema(
            key=key,
            value_type=value_type,
            default=default,
            required=bool(required),
            description=description or "",
        )

    def schemas(self) -> list:
        """Return all registered schemas, ordered by key."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT key, value_type, default_json, required, description "
                "FROM schemas ORDER BY key"
            )
            rows = cur.fetchall()
        out: list = []
        for k, vtype, default_json, required, desc in rows:
            default = (
                json.loads(default_json) if default_json is not None else None
            )
            out.append(
                SettingSchema(
                    key=k,
                    value_type=vtype,
                    default=default,
                    required=bool(required),
                    description=desc or "",
                )
            )
        return out

    def get_schema(self, key: str) -> Optional[SettingSchema]:
        """Return the schema for ``key`` (or ``None``)."""
        with self._lock:
            return self._schema_for_key(key)

    # ------------------------------------------------------------------
    # Single-setting operations
    # ------------------------------------------------------------------

    def set(
        self,
        doc_id: str,
        key: str,
        value: Any,
        now: Optional[float] = None,
    ) -> SettingValue:
        """Upsert a setting and return the resulting :class:`SettingValue`."""
        ts = self._now(now)
        with self._lock:
            value_type = self._resolve_type(key, value)
            coerced = _coerce(value, value_type)
            encoded = _encode(coerced, value_type)
            self._conn.execute(
                "INSERT INTO settings (doc_id, key, value, value_type, set_at) "
                "VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(doc_id, key) DO UPDATE SET "
                "value = excluded.value, "
                "value_type = excluded.value_type, "
                "set_at = excluded.set_at",
                (doc_id, key, encoded, value_type, ts),
            )
            self._conn.commit()
        return SettingValue(
            doc_id=doc_id,
            key=key,
            value=coerced,
            value_type=value_type,
            set_at=ts,
        )

    def get(self, doc_id: str, key: str, default: Any = None) -> Any:
        """Return the decoded value.

        Falls back to the registered schema default and finally to
        ``default``.
        """
        with self._lock:
            row = self._fetch_raw(doc_id, key)
            if row is not None:
                return _decode(row[0], row[1])
            schema = self._schema_for_key(key)
        if schema is not None and schema.default is not None:
            return schema.default
        return default

    def get_value(self, doc_id: str, key: str) -> Optional[SettingValue]:
        """Return the full :class:`SettingValue` for a setting (or None)."""
        with self._lock:
            row = self._fetch_raw(doc_id, key)
        if row is None:
            return None
        raw, vtype, ts = row
        return SettingValue(
            doc_id=doc_id,
            key=key,
            value=_decode(raw, vtype),
            value_type=vtype,
            set_at=ts,
        )

    def delete(self, doc_id: str, key: str) -> bool:
        """Delete a single setting.  Returns ``True`` if it existed."""
        with self._lock:
            existing = self._fetch_raw(doc_id, key)
            if existing is None:
                return False
            self._conn.execute(
                "DELETE FROM settings WHERE doc_id = ? AND key = ?",
                (doc_id, key),
            )
            self._conn.commit()
        return True

    def delete_doc(self, doc_id: str) -> int:
        """Delete every setting for ``doc_id``; return the number removed."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(*) FROM settings WHERE doc_id = ?",
                (doc_id,),
            )
            count = int(cur.fetchone()[0])
            if count:
                self._conn.execute(
                    "DELETE FROM settings WHERE doc_id = ?", (doc_id,)
                )
                self._conn.commit()
        return count

    def has(self, doc_id: str, key: str) -> bool:
        """Return ``True`` if the setting exists for the document."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT 1 FROM settings WHERE doc_id = ? AND key = ? LIMIT 1",
                (doc_id, key),
            )
            return cur.fetchone() is not None

    # ------------------------------------------------------------------
    # Document / key indexing
    # ------------------------------------------------------------------

    def keys_for_doc(self, doc_id: str) -> list:
        """Return the keys set for ``doc_id`` (sorted)."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT key FROM settings WHERE doc_id = ? ORDER BY key",
                (doc_id,),
            )
            return [row[0] for row in cur.fetchall()]

    def docs_with_setting(self, key: str) -> list:
        """Return doc ids that have a setting for ``key`` (sorted)."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT DISTINCT doc_id FROM settings WHERE key = ? ORDER BY doc_id",
                (key,),
            )
            return [row[0] for row in cur.fetchall()]

    def docs_with_value(self, key: str, value: Any) -> list:
        """Return doc ids where ``key`` has the exact ``value``."""
        with self._lock:
            schema = self._schema_for_key(key)
        value_type = schema.value_type if schema else _detect_type(value)
        encoded = _encode(value, value_type)
        with self._lock:
            cur = self._conn.execute(
                "SELECT doc_id FROM settings "
                "WHERE key = ? AND value = ? AND value_type = ? "
                "ORDER BY doc_id",
                (key, encoded, value_type),
            )
            return [row[0] for row in cur.fetchall()]

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------

    def bulk_set(
        self,
        doc_id: str,
        settings: dict,
        now: Optional[float] = None,
    ) -> int:
        """Upsert many settings at once.  Returns the number of writes."""
        if not settings:
            return 0
        ts = self._now(now)
        count = 0
        with self._lock:
            for key, value in settings.items():
                value_type = self._resolve_type(key, value)
                coerced = _coerce(value, value_type)
                encoded = _encode(coerced, value_type)
                self._conn.execute(
                    "INSERT INTO settings (doc_id, key, value, value_type, set_at) "
                    "VALUES (?, ?, ?, ?, ?) "
                    "ON CONFLICT(doc_id, key) DO UPDATE SET "
                    "value = excluded.value, "
                    "value_type = excluded.value_type, "
                    "set_at = excluded.set_at",
                    (doc_id, key, encoded, value_type, ts),
                )
                count += 1
            self._conn.commit()
        return count

    def inherit(
        self,
        child_doc_id: str,
        parent_doc_id: str,
        override: bool = False,
        now: Optional[float] = None,
    ) -> int:
        """Copy settings from ``parent_doc_id`` to ``child_doc_id``.

        With ``override=False`` (default) keys already present on the child
        are kept untouched.  Returns the number of settings copied.
        """
        ts = self._now(now)
        copied = 0
        with self._lock:
            cur = self._conn.execute(
                "SELECT key, value, value_type FROM settings WHERE doc_id = ?",
                (parent_doc_id,),
            )
            parent_rows = cur.fetchall()
            if not parent_rows:
                return 0
            existing_keys: set = set()
            if not override:
                cur = self._conn.execute(
                    "SELECT key FROM settings WHERE doc_id = ?",
                    (child_doc_id,),
                )
                existing_keys = {row[0] for row in cur.fetchall()}
            for key, raw, vtype in parent_rows:
                if not override and key in existing_keys:
                    continue
                self._conn.execute(
                    "INSERT INTO settings (doc_id, key, value, value_type, set_at) "
                    "VALUES (?, ?, ?, ?, ?) "
                    "ON CONFLICT(doc_id, key) DO UPDATE SET "
                    "value = excluded.value, "
                    "value_type = excluded.value_type, "
                    "set_at = excluded.set_at",
                    (child_doc_id, key, raw, vtype, ts),
                )
                copied += 1
            self._conn.commit()
        return copied

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self, doc_id: str) -> list:
        """Return a list of error strings for ``doc_id``.

        Detects:
        * missing required schema keys, and
        * value-type mismatches against the registered schema.
        """
        errors: list = []
        with self._lock:
            cur = self._conn.execute(
                "SELECT key, value_type FROM settings WHERE doc_id = ?",
                (doc_id,),
            )
            present = {row[0]: row[1] for row in cur.fetchall()}
            cur = self._conn.execute(
                "SELECT key, value_type, required FROM schemas"
            )
            schema_rows = cur.fetchall()
        for key, expected_type, required in schema_rows:
            actual_type = present.get(key)
            if actual_type is None:
                if required:
                    errors.append(f"missing required setting: {key}")
                continue
            if actual_type != expected_type:
                errors.append(
                    f"type mismatch for {key}: expected {expected_type}, "
                    f"got {actual_type}"
                )
        return errors

    # ------------------------------------------------------------------
    # Stats and introspection
    # ------------------------------------------------------------------

    @property
    def total_docs(self) -> int:
        """Number of distinct ``doc_id`` values currently stored."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(DISTINCT doc_id) FROM settings"
            )
            return int(cur.fetchone()[0])

    @property
    def total_settings(self) -> int:
        """Total number of settings rows."""
        with self._lock:
            cur = self._conn.execute("SELECT COUNT(*) FROM settings")
            return int(cur.fetchone()[0])

    def stats(self) -> SettingsStoreStats:
        """Return aggregate statistics."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(DISTINCT doc_id), COUNT(*) FROM settings"
            )
            docs, settings_count = cur.fetchone()
            cur = self._conn.execute("SELECT COUNT(*) FROM schemas")
            schemas_count = int(cur.fetchone()[0])
        docs = int(docs or 0)
        settings_count = int(settings_count or 0)
        avg = float(settings_count) / docs if docs else 0.0
        return SettingsStoreStats(
            total_docs=docs,
            total_settings=settings_count,
            total_schemas=schemas_count,
            avg_settings_per_doc=avg,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            self._conn.close()
