"""Persistent document store with JSON metadata and versioning (E272).

This module provides :class:`DocPersistence`, a thread-safe SQLite-backed
store for documents with a strict version history. Every call to
:meth:`DocPersistence.save` inserts a *new* row (a new version) — previous
versions remain accessible until they are explicitly pruned with
:meth:`DocPersistence.purge_old_versions`.

Only the Python standard library is used (``sqlite3``, ``json``,
``threading``).
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


# ── Data model ───────────────────────────────────────────────────────────────

@dataclass
class PersistedDoc:
    """A single versioned document persisted in the store."""

    doc_id: str = ""
    content: str = ""
    metadata: dict = field(default_factory=dict)
    created_at: float = 0.0
    updated_at: float = 0.0
    version: int = 1


@dataclass
class PersistenceStats:
    """Aggregate statistics about the persistence layer."""

    total_docs: int = 0
    total_size: int = 0
    versions: int = 0
    avg_doc_size: float = 0.0


# ── Schema ───────────────────────────────────────────────────────────────────

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS docs (
    doc_id        TEXT NOT NULL,
    version       INTEGER NOT NULL,
    content       TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at    REAL NOT NULL DEFAULT 0,
    updated_at    REAL NOT NULL DEFAULT 0,
    PRIMARY KEY (doc_id, version)
)
"""

_CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_docs_doc_id ON docs(doc_id)
"""


# ── Helpers ──────────────────────────────────────────────────────────────────

def _row_to_doc(row: sqlite3.Row) -> PersistedDoc:
    try:
        metadata = json.loads(row["metadata_json"]) if row["metadata_json"] else {}
    except (TypeError, json.JSONDecodeError):
        metadata = {}
    return PersistedDoc(
        doc_id=row["doc_id"],
        content=row["content"] or "",
        metadata=metadata,
        created_at=row["created_at"] or 0.0,
        updated_at=row["updated_at"] or 0.0,
        version=row["version"],
    )


# ── Persistence ──────────────────────────────────────────────────────────────

class DocPersistence:
    """Thread-safe SQLite-backed persistent document store with versioning.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` for an
        in-memory database.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._conn: Optional[sqlite3.Connection] = sqlite3.connect(
            db_path, check_same_thread=False
        )
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(_CREATE_TABLE)
        self._conn.execute(_CREATE_INDEX)
        self._conn.commit()
        self._closed = False

    # ── Internal ─────────────────────────────────────────────────────────

    def _require_open(self) -> sqlite3.Connection:
        if self._closed or self._conn is None:
            raise RuntimeError("DocPersistence is closed")
        return self._conn

    def _latest_version_locked(self, doc_id: str) -> Optional[int]:
        conn = self._require_open()
        row = conn.execute(
            "SELECT MAX(version) AS v FROM docs WHERE doc_id=?",
            (doc_id,),
        ).fetchone()
        return row["v"] if row and row["v"] is not None else None

    # ── Save ─────────────────────────────────────────────────────────────

    def save(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> PersistedDoc:
        """Persist a new version of *doc_id* and return the stored doc.

        The version number is the previous max version + 1 (starting at 1).
        ``created_at`` is preserved from the first version; ``updated_at``
        is set to *now* (or ``time.time()`` if not provided).
        """
        if not isinstance(doc_id, str):
            raise TypeError("doc_id must be a string")
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            raise TypeError("metadata must be a dict")
        ts = float(now) if now is not None else float(time.time())

        metadata_json = json.dumps(metadata, ensure_ascii=False, sort_keys=True)

        with self._lock:
            conn = self._require_open()
            prev = self._latest_version_locked(doc_id)
            if prev is None:
                version = 1
                created_at = ts
            else:
                version = prev + 1
                row = conn.execute(
                    "SELECT created_at FROM docs WHERE doc_id=? AND version=?",
                    (doc_id, 1),
                ).fetchone()
                created_at = (
                    row["created_at"] if row and row["created_at"] is not None else ts
                )
            conn.execute(
                """
                INSERT INTO docs
                (doc_id, version, content, metadata_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (doc_id, version, content, metadata_json, created_at, ts),
            )
            conn.commit()

        return PersistedDoc(
            doc_id=doc_id,
            content=content,
            metadata=dict(metadata),
            created_at=created_at,
            updated_at=ts,
            version=version,
        )

    # ── Load ─────────────────────────────────────────────────────────────

    def load(self, doc_id: str) -> Optional[PersistedDoc]:
        """Return the latest version of *doc_id*, or ``None`` if missing."""
        with self._lock:
            conn = self._require_open()
            row = conn.execute(
                """
                SELECT * FROM docs WHERE doc_id=?
                ORDER BY version DESC LIMIT 1
                """,
                (doc_id,),
            ).fetchone()
        return _row_to_doc(row) if row else None

    def load_version(
        self, doc_id: str, version: int
    ) -> Optional[PersistedDoc]:
        """Return the specific *version* of *doc_id*, or ``None``."""
        with self._lock:
            conn = self._require_open()
            row = conn.execute(
                "SELECT * FROM docs WHERE doc_id=? AND version=?",
                (doc_id, int(version)),
            ).fetchone()
        return _row_to_doc(row) if row else None

    # ── Delete / Exists ──────────────────────────────────────────────────

    def delete(self, doc_id: str) -> bool:
        """Delete *all* versions of *doc_id*. Returns ``True`` if removed."""
        with self._lock:
            conn = self._require_open()
            cur = conn.execute("DELETE FROM docs WHERE doc_id=?", (doc_id,))
            conn.commit()
            return cur.rowcount > 0

    def exists(self, doc_id: str) -> bool:
        """Return ``True`` if *doc_id* has at least one stored version."""
        with self._lock:
            conn = self._require_open()
            row = conn.execute(
                "SELECT 1 FROM docs WHERE doc_id=? LIMIT 1", (doc_id,)
            ).fetchone()
        return row is not None

    # ── Listing ──────────────────────────────────────────────────────────

    def list_all(self, limit: Optional[int] = None) -> list[PersistedDoc]:
        """Return the latest version of every doc, ordered by ``updated_at`` desc."""
        with self._lock:
            conn = self._require_open()
            sql = (
                "SELECT d.* FROM docs d "
                "INNER JOIN (SELECT doc_id, MAX(version) AS mv FROM docs "
                "GROUP BY doc_id) m ON d.doc_id=m.doc_id AND d.version=m.mv "
                "ORDER BY d.updated_at DESC, d.doc_id ASC"
            )
            params: tuple = ()
            if limit is not None:
                sql += " LIMIT ?"
                params = (int(limit),)
            rows = conn.execute(sql, params).fetchall()
        return [_row_to_doc(r) for r in rows]

    def list_doc_ids(self) -> list[str]:
        """Return all distinct doc_ids, sorted alphabetically."""
        with self._lock:
            conn = self._require_open()
            rows = conn.execute(
                "SELECT DISTINCT doc_id FROM docs ORDER BY doc_id ASC"
            ).fetchall()
        return [r["doc_id"] for r in rows]

    # ── Versions ─────────────────────────────────────────────────────────

    def versions_of(self, doc_id: str) -> list[int]:
        """Return all version numbers for *doc_id*, ascending."""
        with self._lock:
            conn = self._require_open()
            rows = conn.execute(
                "SELECT version FROM docs WHERE doc_id=? ORDER BY version ASC",
                (doc_id,),
            ).fetchall()
        return [int(r["version"]) for r in rows]

    def version_count(self, doc_id: str) -> int:
        """Return how many versions of *doc_id* exist."""
        with self._lock:
            conn = self._require_open()
            row = conn.execute(
                "SELECT COUNT(*) AS c FROM docs WHERE doc_id=?", (doc_id,)
            ).fetchone()
        return int(row["c"]) if row else 0

    def latest_version(self, doc_id: str) -> Optional[int]:
        """Return the highest version number for *doc_id*, or ``None``."""
        with self._lock:
            return self._latest_version_locked(doc_id)

    # ── Purge ────────────────────────────────────────────────────────────

    def purge_old_versions(
        self, doc_id: str, keep_last_n: int = 10
    ) -> int:
        """Keep only the *keep_last_n* most recent versions of *doc_id*.

        Returns the number of versions removed.
        """
        if keep_last_n < 0:
            raise ValueError("keep_last_n must be >= 0")
        with self._lock:
            conn = self._require_open()
            rows = conn.execute(
                "SELECT version FROM docs WHERE doc_id=? ORDER BY version DESC",
                (doc_id,),
            ).fetchall()
            if len(rows) <= keep_last_n:
                return 0
            to_remove = [int(r["version"]) for r in rows[keep_last_n:]]
            placeholders = ",".join(["?"] * len(to_remove))
            params = [doc_id] + to_remove
            cur = conn.execute(
                f"DELETE FROM docs WHERE doc_id=? AND version IN ({placeholders})",
                params,
            )
            conn.commit()
            return cur.rowcount

    def purge_all_old_versions(self, keep_last_n: int = 10) -> int:
        """Apply :meth:`purge_old_versions` to every doc_id; returns total removed."""
        if keep_last_n < 0:
            raise ValueError("keep_last_n must be >= 0")
        # Collect ids first to avoid holding the lock during recursive locking
        ids = self.list_doc_ids()
        removed = 0
        for doc_id in ids:
            removed += self.purge_old_versions(doc_id, keep_last_n=keep_last_n)
        return removed

    # ── Stats / counts ───────────────────────────────────────────────────

    @property
    def total_docs(self) -> int:
        """Number of distinct doc_ids in the store."""
        with self._lock:
            conn = self._require_open()
            row = conn.execute(
                "SELECT COUNT(DISTINCT doc_id) AS c FROM docs"
            ).fetchone()
        return int(row["c"]) if row else 0

    @property
    def total_versions(self) -> int:
        """Total number of rows (versions) in the store."""
        with self._lock:
            conn = self._require_open()
            row = conn.execute("SELECT COUNT(*) AS c FROM docs").fetchone()
        return int(row["c"]) if row else 0

    def stats(self) -> PersistenceStats:
        """Return aggregate statistics."""
        with self._lock:
            conn = self._require_open()
            total_docs_row = conn.execute(
                "SELECT COUNT(DISTINCT doc_id) AS c FROM docs"
            ).fetchone()
            total_versions_row = conn.execute(
                "SELECT COUNT(*) AS c FROM docs"
            ).fetchone()
            size_row = conn.execute(
                "SELECT COALESCE(SUM(LENGTH(content)), 0) AS s FROM docs"
            ).fetchone()
        total_docs = int(total_docs_row["c"]) if total_docs_row else 0
        versions = int(total_versions_row["c"]) if total_versions_row else 0
        total_size = int(size_row["s"]) if size_row else 0
        avg = (total_size / versions) if versions > 0 else 0.0
        return PersistenceStats(
            total_docs=total_docs,
            total_size=total_size,
            versions=versions,
            avg_doc_size=avg,
        )

    # ── Vacuum / close ───────────────────────────────────────────────────

    def vacuum(self) -> int:
        """Remove orphaned rows (corrupt metadata) and compact the database.

        Returns the count of rows that were removed during cleanup.
        """
        with self._lock:
            conn = self._require_open()
            # Find rows whose metadata_json is not valid JSON and drop them
            rows = conn.execute(
                "SELECT rowid, metadata_json FROM docs"
            ).fetchall()
            bad: list[int] = []
            for r in rows:
                try:
                    json.loads(r["metadata_json"])
                except (TypeError, json.JSONDecodeError):
                    bad.append(int(r["rowid"]))
            if bad:
                placeholders = ",".join(["?"] * len(bad))
                conn.execute(
                    f"DELETE FROM docs WHERE rowid IN ({placeholders})", bad
                )
            conn.commit()
            # Run sqlite VACUUM to compact the file
            try:
                conn.execute("VACUUM")
            except sqlite3.OperationalError:
                # VACUUM may fail in some transactional states; ignore
                pass
            return len(bad)

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            if self._conn is not None:
                try:
                    self._conn.close()
                finally:
                    self._conn = None
            self._closed = True

    @property
    def is_open(self) -> bool:
        """``True`` if the store is open and usable."""
        return not self._closed and self._conn is not None
