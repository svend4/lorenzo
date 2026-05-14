"""SQLite-backed version history for documentation files."""
from __future__ import annotations

import hashlib
import sqlite3
import time
from dataclasses import dataclass
from typing import Optional

from docstoolkit.doc_versioning.version import ChangeType, DocVersion


# ---------------------------------------------------------------------------
# Data transfer object
# ---------------------------------------------------------------------------

@dataclass
class VersionRecord:
    """A single entry in a document's version history."""

    doc_id: str
    version: DocVersion
    change_type: ChangeType
    summary: str
    ts: float
    content_hash: str  # first 16 hex chars of SHA-256


# ---------------------------------------------------------------------------
# History store
# ---------------------------------------------------------------------------

_DDL = """
CREATE TABLE IF NOT EXISTS doc_versions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id       TEXT    NOT NULL,
    major        INTEGER NOT NULL,
    minor        INTEGER NOT NULL,
    patch        INTEGER NOT NULL,
    change_type  TEXT    NOT NULL,
    summary      TEXT    NOT NULL DEFAULT '',
    ts           REAL    NOT NULL,
    content_hash TEXT    NOT NULL
);
"""


class VersionHistory:
    """Persistent (or in-memory) version history backed by SQLite.

    Parameters
    ----------
    db_path:
        Path passed to ``sqlite3.connect``.  Defaults to ``":memory:"``
        for an ephemeral in-process store.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(_DDL)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def record(
        self,
        doc_id: str,
        content: str,
        change_type: ChangeType,
        summary: str = "",
        ts: Optional[float] = None,
    ) -> VersionRecord:
        """Record a new version of *doc_id*.

        The method is **idempotent with respect to content**: if the
        content hash is identical to the most recent record for *doc_id*
        the existing record is returned unchanged.

        Version assignment
        ------------------
        * If no previous record exists the version starts at ``0.1.0``.
        * Otherwise the latest version is bumped by *change_type*.
        """
        content_hash = _sha256_prefix(content)
        timestamp = ts if ts is not None else time.time()

        latest = self.latest(doc_id)

        if latest is not None and latest.content_hash == content_hash:
            # Content unchanged — skip
            return latest

        if latest is None:
            new_version = DocVersion.initial()
        else:
            new_version = latest.version.bump(change_type)

        self._conn.execute(
            """
            INSERT INTO doc_versions
                (doc_id, major, minor, patch, change_type, summary, ts, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                doc_id,
                new_version.major,
                new_version.minor,
                new_version.patch,
                change_type.value,
                summary,
                timestamp,
                content_hash,
            ),
        )
        self._conn.commit()

        return VersionRecord(
            doc_id=doc_id,
            version=new_version,
            change_type=change_type,
            summary=summary,
            ts=timestamp,
            content_hash=content_hash,
        )

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def latest(self, doc_id: str) -> Optional[VersionRecord]:
        """Return the most recently recorded version for *doc_id*, or None."""
        row = self._conn.execute(
            """
            SELECT * FROM doc_versions
            WHERE doc_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (doc_id,),
        ).fetchone()
        return _row_to_record(row) if row else None

    def list_versions(self, doc_id: str) -> list[VersionRecord]:
        """Return all version records for *doc_id* ordered oldest-first."""
        rows = self._conn.execute(
            """
            SELECT * FROM doc_versions
            WHERE doc_id = ?
            ORDER BY id ASC
            """,
            (doc_id,),
        ).fetchall()
        return [_row_to_record(r) for r in rows]

    def diff_summary(
        self, doc_id: str, from_version: str, to_version: str
    ) -> str:
        """Return a human-readable one-liner describing the change between two versions.

        Format: ``"v{from} → v{to}: {change_type}"``

        Raises ``KeyError`` if either version is not found for *doc_id*.
        """
        records = {str(r.version): r for r in self.list_versions(doc_id)}

        if from_version not in records:
            raise KeyError(
                f"Version {from_version!r} not found for doc {doc_id!r}"
            )
        if to_version not in records:
            raise KeyError(
                f"Version {to_version!r} not found for doc {doc_id!r}"
            )

        to_record = records[to_version]
        return f"v{from_version} → v{to_version}: {to_record.change_type.value}"

    def all_docs(self) -> list[str]:
        """Return a sorted list of distinct doc_id values in the store."""
        rows = self._conn.execute(
            "SELECT DISTINCT doc_id FROM doc_versions ORDER BY doc_id"
        ).fetchall()
        return [r["doc_id"] for r in rows]

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _sha256_prefix(text: str, length: int = 16) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:length]


def _row_to_record(row: sqlite3.Row) -> VersionRecord:
    return VersionRecord(
        doc_id=row["doc_id"],
        version=DocVersion(row["major"], row["minor"], row["patch"]),
        change_type=ChangeType(row["change_type"]),
        summary=row["summary"],
        ts=row["ts"],
        content_hash=row["content_hash"],
    )
