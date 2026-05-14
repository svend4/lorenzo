"""Schema registry backed by SQLite."""
from __future__ import annotations

import json
import sqlite3
from typing import Optional

from docstoolkit.schema_registry.schema import Schema, SchemaVersion, FieldDef

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS schemas (
    schema_id   TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    version     TEXT NOT NULL,
    fields      TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created_ts  REAL NOT NULL
)
"""


def _schema_to_row(schema: Schema) -> tuple:
    fields_json = json.dumps(
        [
            {
                "name": f.name,
                "field_type": f.field_type,
                "required": f.required,
                "nullable": f.nullable,
                "description": f.description,
            }
            for f in schema.fields
        ]
    )
    return (
        schema.schema_id,
        schema.name,
        str(schema.version),
        fields_json,
        schema.description,
        schema.created_ts,
    )


def _row_to_schema(row: tuple) -> Schema:
    schema_id, name, version_str, fields_json, description, created_ts = row
    version = SchemaVersion.parse(version_str)
    raw_fields = json.loads(fields_json)
    fields = [
        FieldDef(
            name=f["name"],
            field_type=f["field_type"],
            required=f.get("required", True),
            nullable=f.get("nullable", False),
            description=f.get("description", ""),
        )
        for f in raw_fields
    ]
    return Schema(
        schema_id=schema_id,
        name=name,
        version=version,
        fields=fields,
        description=description,
        created_ts=created_ts,
    )


class SchemaRegistry:
    """In-memory (or file-backed) SQLite schema registry."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def register(self, schema: Schema) -> None:
        """Store or replace a schema."""
        row = _schema_to_row(schema)
        self._conn.execute(
            """
            INSERT OR REPLACE INTO schemas
                (schema_id, name, version, fields, description, created_ts)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            row,
        )
        self._conn.commit()

    def delete(self, schema_id: str) -> bool:
        """Delete a schema by ID. Returns True if a row was deleted."""
        cursor = self._conn.execute(
            "DELETE FROM schemas WHERE schema_id = ?", (schema_id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get(self, schema_id: str) -> Optional[Schema]:
        """Retrieve a schema by its ID."""
        cursor = self._conn.execute(
            "SELECT schema_id, name, version, fields, description, created_ts "
            "FROM schemas WHERE schema_id = ?",
            (schema_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_schema(row)

    def find(self, name: str, version: Optional[str] = None) -> Optional[Schema]:
        """Find a schema by name and optional version string."""
        if version is not None:
            cursor = self._conn.execute(
                "SELECT schema_id, name, version, fields, description, created_ts "
                "FROM schemas WHERE name = ? AND version = ?",
                (name, version),
            )
        else:
            cursor = self._conn.execute(
                "SELECT schema_id, name, version, fields, description, created_ts "
                "FROM schemas WHERE name = ? LIMIT 1",
                (name,),
            )
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_schema(row)

    def list_schemas(self) -> list:
        """Return all registered schemas."""
        cursor = self._conn.execute(
            "SELECT schema_id, name, version, fields, description, created_ts "
            "FROM schemas ORDER BY name, version"
        )
        return [_row_to_schema(row) for row in cursor.fetchall()]

    def list_versions(self, name: str) -> list:
        """Return all SchemaVersion objects registered under a given name."""
        cursor = self._conn.execute(
            "SELECT version FROM schemas WHERE name = ? ORDER BY version",
            (name,),
        )
        versions = [SchemaVersion.parse(row[0]) for row in cursor.fetchall()]
        return sorted(versions)

    def latest(self, name: str) -> Optional[Schema]:
        """Return the schema with the highest version for a given name."""
        versions = self.list_versions(name)
        if not versions:
            return None
        best = max(versions)
        return self.find(name, str(best))

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        self._conn.close()
