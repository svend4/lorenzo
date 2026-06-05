"""SQLite-backed feature store."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Optional

from docstoolkit.feature_store.feature import FeatureDefinition, FeatureType, FeatureValue

_CREATE_DEFS = """
CREATE TABLE IF NOT EXISTS feature_defs (
    name               TEXT PRIMARY KEY,
    feature_type       TEXT NOT NULL,
    description        TEXT NOT NULL DEFAULT '',
    default_value_json TEXT,
    tags_json          TEXT NOT NULL DEFAULT '[]'
)
"""

_CREATE_VALS = """
CREATE TABLE IF NOT EXISTS feature_values (
    entity_id    TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    value_json   TEXT,
    ts           REAL NOT NULL,
    version      INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (entity_id, feature_name)
)
"""

_IDX_ENTITY = """
CREATE INDEX IF NOT EXISTS idx_fv_entity_id    ON feature_values (entity_id)
"""

_IDX_FEATURE = """
CREATE INDEX IF NOT EXISTS idx_fv_feature_name ON feature_values (feature_name)
"""


def _def_from_row(row: tuple) -> FeatureDefinition:
    name, feature_type, description, default_value_json, tags_json = row
    return FeatureDefinition(
        name=name,
        feature_type=FeatureType(feature_type),
        description=description,
        default_value=json.loads(default_value_json) if default_value_json is not None else None,
        tags=json.loads(tags_json),
    )


def _val_from_row(row: tuple) -> FeatureValue:
    entity_id, feature_name, value_json, ts, version = row
    return FeatureValue(
        entity_id=entity_id,
        feature_name=feature_name,
        value=json.loads(value_json) if value_json is not None else None,
        ts=ts,
        version=version,
    )


class FeatureStore:
    """SQLite-backed store for feature definitions and values."""

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self._db_path = str(db_path)
        self._conn = sqlite3.connect(self._db_path)
        self._conn.isolation_level = None  # autocommit by default; we use explicit transactions
        self._init_schema()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _init_schema(self) -> None:
        cur = self._conn.cursor()
        cur.execute(_CREATE_DEFS)
        cur.execute(_CREATE_VALS)
        cur.execute(_IDX_ENTITY)
        cur.execute(_IDX_FEATURE)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Feature definitions
    # ------------------------------------------------------------------

    def register(self, defn: FeatureDefinition) -> None:
        """Upsert a feature definition."""
        self._conn.execute(
            """
            INSERT INTO feature_defs (name, feature_type, description, default_value_json, tags_json)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                feature_type       = excluded.feature_type,
                description        = excluded.description,
                default_value_json = excluded.default_value_json,
                tags_json          = excluded.tags_json
            """,
            (
                defn.name,
                defn.feature_type.value,
                defn.description,
                json.dumps(defn.default_value) if defn.default_value is not None else None,
                json.dumps(defn.tags),
            ),
        )

    def get_definition(self, name: str) -> Optional[FeatureDefinition]:
        """Return the definition for *name*, or None if not registered."""
        cur = self._conn.execute(
            "SELECT name, feature_type, description, default_value_json, tags_json "
            "FROM feature_defs WHERE name = ?",
            (name,),
        )
        row = cur.fetchone()
        return _def_from_row(row) if row else None

    def list_definitions(self, tag: Optional[str] = None) -> list[FeatureDefinition]:
        """Return all definitions, optionally filtered by tag."""
        cur = self._conn.execute(
            "SELECT name, feature_type, description, default_value_json, tags_json "
            "FROM feature_defs ORDER BY name"
        )
        rows = cur.fetchall()
        defs = [_def_from_row(r) for r in rows]
        if tag is not None:
            defs = [d for d in defs if tag in d.tags]
        return defs

    # ------------------------------------------------------------------
    # Feature values
    # ------------------------------------------------------------------

    def write(self, fv: FeatureValue) -> None:
        """Upsert a feature value by (entity_id, feature_name)."""
        self._conn.execute(
            """
            INSERT INTO feature_values (entity_id, feature_name, value_json, ts, version)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(entity_id, feature_name) DO UPDATE SET
                value_json = excluded.value_json,
                ts         = excluded.ts,
                version    = excluded.version
            """,
            (
                fv.entity_id,
                fv.feature_name,
                json.dumps(fv.value),
                fv.ts,
                fv.version,
            ),
        )

    def write_batch(self, fvs: list[FeatureValue]) -> None:
        """Upsert multiple feature values in a single transaction."""
        with self._conn:
            for fv in fvs:
                self._conn.execute(
                    """
                    INSERT INTO feature_values (entity_id, feature_name, value_json, ts, version)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(entity_id, feature_name) DO UPDATE SET
                        value_json = excluded.value_json,
                        ts         = excluded.ts,
                        version    = excluded.version
                    """,
                    (
                        fv.entity_id,
                        fv.feature_name,
                        json.dumps(fv.value),
                        fv.ts,
                        fv.version,
                    ),
                )

    def read(self, entity_id: str, feature_name: str) -> Optional[FeatureValue]:
        """Return a single feature value, or None if not found."""
        cur = self._conn.execute(
            "SELECT entity_id, feature_name, value_json, ts, version "
            "FROM feature_values WHERE entity_id = ? AND feature_name = ?",
            (entity_id, feature_name),
        )
        row = cur.fetchone()
        return _val_from_row(row) if row else None

    def read_entity(self, entity_id: str) -> dict[str, FeatureValue]:
        """Return all features for an entity as {feature_name: FeatureValue}."""
        cur = self._conn.execute(
            "SELECT entity_id, feature_name, value_json, ts, version "
            "FROM feature_values WHERE entity_id = ? ORDER BY feature_name",
            (entity_id,),
        )
        return {row[1]: _val_from_row(row) for row in cur.fetchall()}

    def read_feature(
        self,
        feature_name: str,
        entity_ids: Optional[list[str]] = None,
    ) -> list[FeatureValue]:
        """Return all values for a feature, optionally filtered to *entity_ids*."""
        if entity_ids is not None:
            if not entity_ids:
                return []
            placeholders = ",".join("?" * len(entity_ids))
            cur = self._conn.execute(
                f"SELECT entity_id, feature_name, value_json, ts, version "
                f"FROM feature_values "
                f"WHERE feature_name = ? AND entity_id IN ({placeholders}) "
                f"ORDER BY entity_id",
                (feature_name, *entity_ids),
            )
        else:
            cur = self._conn.execute(
                "SELECT entity_id, feature_name, value_json, ts, version "
                "FROM feature_values WHERE feature_name = ? ORDER BY entity_id",
                (feature_name,),
            )
        return [_val_from_row(row) for row in cur.fetchall()]

    def delete(self, entity_id: str, feature_name: str) -> bool:
        """Delete a feature value. Returns True if a row was deleted."""
        cur = self._conn.execute(
            "DELETE FROM feature_values WHERE entity_id = ? AND feature_name = ?",
            (entity_id, feature_name),
        )
        return cur.rowcount > 0

    def entities(self) -> list[str]:
        """Return sorted list of distinct entity_ids."""
        cur = self._conn.execute(
            "SELECT DISTINCT entity_id FROM feature_values ORDER BY entity_id"
        )
        return [row[0] for row in cur.fetchall()]

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
