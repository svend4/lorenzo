"""SQLite-backed snapshot store."""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Optional

from docstoolkit.snapshot_store.snapshot import Snapshot, SnapshotMetadata

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS snapshots (
    snapshot_id TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    created_at  REAL NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    tags        TEXT NOT NULL DEFAULT '[]',
    size_bytes  INTEGER NOT NULL DEFAULT 0,
    data        BLOB
)
"""

_IDX_NAME = """
CREATE INDEX IF NOT EXISTS idx_snapshots_name       ON snapshots (name)
"""

_IDX_CREATED_AT = """
CREATE INDEX IF NOT EXISTS idx_snapshots_created_at ON snapshots (created_at)
"""


def _metadata_from_row(row: tuple) -> SnapshotMetadata:
    snapshot_id, name, created_at, description, tags_json, size_bytes = row
    return SnapshotMetadata(
        snapshot_id=snapshot_id,
        name=name,
        created_at=created_at,
        description=description,
        tags=json.loads(tags_json) if tags_json else [],
        size_bytes=size_bytes,
    )


class SnapshotStore:
    """SQLite-backed store for named binary snapshots."""

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self._db_path = str(db_path)
        self._conn = sqlite3.connect(self._db_path)
        self._init_schema()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _init_schema(self) -> None:
        cur = self._conn.cursor()
        cur.execute(_CREATE_TABLE)
        cur.execute(_IDX_NAME)
        cur.execute(_IDX_CREATED_AT)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def save(
        self,
        name: str,
        data: bytes,
        description: str = "",
        tags: Optional[list[str]] = None,
    ) -> SnapshotMetadata:
        """Persist a new snapshot and return its metadata."""
        snapshot_id = str(uuid.uuid4())
        created_at = time.time()
        tag_list = list(tags) if tags is not None else []
        size_bytes = len(data)
        self._conn.execute(
            """
            INSERT INTO snapshots (snapshot_id, name, created_at, description, tags, size_bytes, data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot_id,
                name,
                created_at,
                description,
                json.dumps(tag_list),
                size_bytes,
                data,
            ),
        )
        self._conn.commit()
        return SnapshotMetadata(
            snapshot_id=snapshot_id,
            name=name,
            created_at=created_at,
            description=description,
            tags=tag_list,
            size_bytes=size_bytes,
        )

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def load(self, snapshot_id: str) -> Optional[Snapshot]:
        """Return the full snapshot (metadata + data) or None if missing."""
        cur = self._conn.execute(
            "SELECT snapshot_id, name, created_at, description, tags, size_bytes, data "
            "FROM snapshots WHERE snapshot_id = ?",
            (snapshot_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        meta = _metadata_from_row(row[:6])
        data = row[6] if row[6] is not None else b""
        if isinstance(data, memoryview):
            data = bytes(data)
        return Snapshot(metadata=meta, data=data)

    def get_metadata(self, snapshot_id: str) -> Optional[SnapshotMetadata]:
        """Return metadata only (no data) for the given id, or None."""
        cur = self._conn.execute(
            "SELECT snapshot_id, name, created_at, description, tags, size_bytes "
            "FROM snapshots WHERE snapshot_id = ?",
            (snapshot_id,),
        )
        row = cur.fetchone()
        return _metadata_from_row(row) if row else None

    def list(
        self,
        name: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 100,
    ) -> list[SnapshotMetadata]:
        """Return metadata for snapshots, newest first, optionally filtered."""
        if name is not None:
            cur = self._conn.execute(
                "SELECT snapshot_id, name, created_at, description, tags, size_bytes "
                "FROM snapshots WHERE name = ? "
                "ORDER BY created_at DESC, snapshot_id DESC",
                (name,),
            )
        else:
            cur = self._conn.execute(
                "SELECT snapshot_id, name, created_at, description, tags, size_bytes "
                "FROM snapshots "
                "ORDER BY created_at DESC, snapshot_id DESC"
            )
        results: list[SnapshotMetadata] = []
        if limit <= 0:
            return results
        for row in cur.fetchall():
            meta = _metadata_from_row(row)
            if tag is not None and tag not in meta.tags:
                continue
            results.append(meta)
            if len(results) >= limit:
                break
        return results

    def latest(self, name: str) -> Optional[SnapshotMetadata]:
        """Return the most recent snapshot metadata with the given name."""
        cur = self._conn.execute(
            "SELECT snapshot_id, name, created_at, description, tags, size_bytes "
            "FROM snapshots WHERE name = ? "
            "ORDER BY created_at DESC, snapshot_id DESC LIMIT 1",
            (name,),
        )
        row = cur.fetchone()
        return _metadata_from_row(row) if row else None

    # ------------------------------------------------------------------
    # Aggregate
    # ------------------------------------------------------------------

    def count(self) -> int:
        """Return the total number of snapshots stored."""
        cur = self._conn.execute("SELECT COUNT(*) FROM snapshots")
        row = cur.fetchone()
        return int(row[0]) if row else 0

    def total_size(self) -> int:
        """Return the summed size_bytes across all snapshots."""
        cur = self._conn.execute("SELECT COALESCE(SUM(size_bytes), 0) FROM snapshots")
        row = cur.fetchone()
        return int(row[0]) if row else 0

    # ------------------------------------------------------------------
    # Delete / prune
    # ------------------------------------------------------------------

    def delete(self, snapshot_id: str) -> bool:
        """Delete a snapshot by id. Returns True if a row was removed."""
        cur = self._conn.execute(
            "DELETE FROM snapshots WHERE snapshot_id = ?",
            (snapshot_id,),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def prune(self, name: Optional[str] = None, keep_count: int = 10) -> int:
        """Keep the newest ``keep_count`` snapshots and delete older ones.

        When ``name`` is given the prune is scoped to that name; otherwise
        pruning is performed per-name across the entire store.

        Returns the number of deleted rows.
        """
        if keep_count < 0:
            keep_count = 0

        if name is not None:
            names = [name]
        else:
            cur = self._conn.execute("SELECT DISTINCT name FROM snapshots")
            names = [row[0] for row in cur.fetchall()]

        total_deleted = 0
        for n in names:
            cur = self._conn.execute(
                "SELECT snapshot_id FROM snapshots WHERE name = ? "
                "ORDER BY created_at DESC, snapshot_id DESC",
                (n,),
            )
            ids = [row[0] for row in cur.fetchall()]
            to_delete = ids[keep_count:]
            if not to_delete:
                continue
            placeholders = ",".join("?" * len(to_delete))
            cur = self._conn.execute(
                f"DELETE FROM snapshots WHERE snapshot_id IN ({placeholders})",
                to_delete,
            )
            total_deleted += cur.rowcount
        self._conn.commit()
        return total_deleted

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        self._conn.close()
