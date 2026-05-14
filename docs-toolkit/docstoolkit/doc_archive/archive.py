"""E181 Document archive — gzip-compressed storage with retention policies.

Documents are stored in a SQLite database (in-memory by default) as gzip-compressed
UTF-8 blobs. The :class:`DocArchive` class is thread-safe via an internal lock and
opens its connection with ``check_same_thread=False``.

Only Python's standard library is used (``gzip``, ``sqlite3``, ``threading``).
"""
from __future__ import annotations

import gzip
import sqlite3
import threading
from dataclasses import dataclass
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class ArchivedDoc:
    """Metadata about a single archived document."""

    doc_id: str
    original_size: int
    compressed_size: int
    archived_at: float

    @property
    def compression_ratio(self) -> float:
        """Return compressed/original size ratio. 0.0 if original was empty."""
        if self.original_size == 0:
            return 0.0
        return self.compressed_size / self.original_size


@dataclass
class RetentionPolicy:
    """Retention policy for automatic eviction.

    - ``max_age_seconds``: drop entries older than this (vs ``now``). ``None`` = no age limit.
    - ``max_count``: keep at most this many entries (oldest first). ``None`` = no cap.
    - ``min_count``: never drop below this many entries, even if other rules say so.
    """

    max_age_seconds: Optional[float] = None
    max_count: Optional[int] = None
    min_count: int = 0


@dataclass
class ArchiveStats:
    """Aggregate statistics across the entire archive."""

    total_archived: int
    total_original_size: int
    total_compressed_size: int

    @property
    def space_saved(self) -> int:
        """Bytes saved (original - compressed). May be negative if compression grew data."""
        return self.total_original_size - self.total_compressed_size

    @property
    def avg_ratio(self) -> float:
        """Average compression ratio across the archive."""
        if self.total_original_size == 0:
            return 0.0
        return self.total_compressed_size / self.total_original_size


# ---------------------------------------------------------------------------
# DocArchive
# ---------------------------------------------------------------------------


class DocArchive:
    """Compressed document archive backed by SQLite.

    The schema is a single table ``archive`` with columns:
    ``doc_id`` (PK), ``compressed_blob`` BLOB, ``original_size`` INTEGER,
    ``archived_at`` REAL.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS archive (
                doc_id TEXT PRIMARY KEY,
                compressed_blob BLOB NOT NULL,
                original_size INTEGER NOT NULL,
                archived_at REAL NOT NULL
            )
            """
        )
        self._conn.commit()
        self._closed = False

    # -- internal helpers -------------------------------------------------

    @staticmethod
    def _row_to_doc(row: tuple) -> ArchivedDoc:
        doc_id, blob, original_size, archived_at = row
        return ArchivedDoc(
            doc_id=doc_id,
            original_size=int(original_size),
            compressed_size=len(blob),
            archived_at=float(archived_at),
        )

    # -- core operations --------------------------------------------------

    def archive(self, doc_id: str, content: str, now: float = 0.0) -> ArchivedDoc:
        """Compress ``content`` and store it under ``doc_id``.

        If ``doc_id`` already exists, it is overwritten.
        """
        encoded = content.encode("utf-8")
        original_size = len(encoded)
        blob = gzip.compress(encoded)
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO archive "
                "(doc_id, compressed_blob, original_size, archived_at) "
                "VALUES (?, ?, ?, ?)",
                (doc_id, blob, original_size, float(now)),
            )
            self._conn.commit()
        return ArchivedDoc(
            doc_id=doc_id,
            original_size=original_size,
            compressed_size=len(blob),
            archived_at=float(now),
        )

    def restore(self, doc_id: str) -> Optional[str]:
        """Return decompressed content for ``doc_id``, or ``None`` if not found."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT compressed_blob FROM archive WHERE doc_id = ?", (doc_id,)
            )
            row = cur.fetchone()
        if row is None:
            return None
        return gzip.decompress(row[0]).decode("utf-8")

    def exists(self, doc_id: str) -> bool:
        """Return True if ``doc_id`` is in the archive."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT 1 FROM archive WHERE doc_id = ?", (doc_id,)
            )
            return cur.fetchone() is not None

    def delete(self, doc_id: str) -> bool:
        """Delete ``doc_id``. Return True if a row was removed."""
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM archive WHERE doc_id = ?", (doc_id,)
            )
            self._conn.commit()
            return cur.rowcount > 0

    def list_all(self) -> List[ArchivedDoc]:
        """Return every archived document, ordered by archive time ascending."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT doc_id, compressed_blob, original_size, archived_at "
                "FROM archive ORDER BY archived_at ASC, doc_id ASC"
            )
            rows = cur.fetchall()
        return [self._row_to_doc(r) for r in rows]

    # -- retention --------------------------------------------------------

    def apply_retention(self, policy: RetentionPolicy, now: float = 0.0) -> int:
        """Apply ``policy`` and return the number of entries removed."""
        docs = self.list_all()
        total = len(docs)
        min_count = max(0, int(policy.min_count or 0))

        to_remove: List[str] = []

        # 1) Age-based eviction (oldest first).
        if policy.max_age_seconds is not None:
            cutoff = float(now) - float(policy.max_age_seconds)
            for d in docs:
                if d.archived_at < cutoff:
                    to_remove.append(d.doc_id)

        # 2) Count-based eviction (drop oldest until <= max_count).
        if policy.max_count is not None:
            cap = max(0, int(policy.max_count))
            already = set(to_remove)
            remaining = [d for d in docs if d.doc_id not in already]
            # remaining is already in ascending time order
            overflow = len(remaining) - cap
            if overflow > 0:
                for d in remaining[:overflow]:
                    to_remove.append(d.doc_id)

        # 3) Enforce min_count by un-removing the *newest* candidates first.
        if min_count > 0 and to_remove:
            kept_after = total - len(set(to_remove))
            if kept_after < min_count:
                need_back = min_count - kept_after
                # Map doc_id -> archived_at for ordering
                age_map = {d.doc_id: d.archived_at for d in docs}
                # Sort removal candidates by archived_at DESC (newest first), restore those.
                unique_removals = list(dict.fromkeys(to_remove))  # preserve order, dedupe
                unique_removals.sort(key=lambda did: age_map.get(did, 0.0), reverse=True)
                restored = set(unique_removals[:need_back])
                to_remove = [did for did in to_remove if did not in restored]

        if not to_remove:
            return 0

        unique = list(dict.fromkeys(to_remove))
        with self._lock:
            self._conn.executemany(
                "DELETE FROM archive WHERE doc_id = ?",
                [(did,) for did in unique],
            )
            self._conn.commit()
        return len(unique)

    # -- stats / accessors ------------------------------------------------

    def stats(self) -> ArchiveStats:
        """Return aggregate statistics across the archive."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(*), COALESCE(SUM(original_size), 0), "
                "COALESCE(SUM(LENGTH(compressed_blob)), 0) FROM archive"
            )
            total, orig, comp = cur.fetchone()
        return ArchiveStats(
            total_archived=int(total),
            total_original_size=int(orig),
            total_compressed_size=int(comp),
        )

    @property
    def count(self) -> int:
        """Number of archived documents."""
        with self._lock:
            cur = self._conn.execute("SELECT COUNT(*) FROM archive")
            return int(cur.fetchone()[0])

    def total_size_bytes(self) -> int:
        """Sum of compressed blob sizes."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT COALESCE(SUM(LENGTH(compressed_blob)), 0) FROM archive"
            )
            return int(cur.fetchone()[0])

    def oldest(self, now: float = 0.0) -> Optional[ArchivedDoc]:
        """Return the oldest archived document, or ``None`` if archive is empty.

        ``now`` is accepted for signature symmetry with :meth:`newest`; it is
        not used in the lookup itself.
        """
        with self._lock:
            cur = self._conn.execute(
                "SELECT doc_id, compressed_blob, original_size, archived_at "
                "FROM archive ORDER BY archived_at ASC, doc_id ASC LIMIT 1"
            )
            row = cur.fetchone()
        if row is None:
            return None
        return self._row_to_doc(row)

    def newest(self, now: float = 0.0) -> Optional[ArchivedDoc]:
        """Return the newest archived document, or ``None`` if archive is empty."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT doc_id, compressed_blob, original_size, archived_at "
                "FROM archive ORDER BY archived_at DESC, doc_id DESC LIMIT 1"
            )
            row = cur.fetchone()
        if row is None:
            return None
        return self._row_to_doc(row)

    # -- batch / lifecycle ------------------------------------------------

    def archive_batch(
        self, docs: Dict[str, str], now: float = 0.0
    ) -> List[ArchivedDoc]:
        """Archive multiple documents in one transaction."""
        results: List[ArchivedDoc] = []
        rows = []
        for doc_id, content in docs.items():
            encoded = content.encode("utf-8")
            blob = gzip.compress(encoded)
            rows.append((doc_id, blob, len(encoded), float(now)))
            results.append(
                ArchivedDoc(
                    doc_id=doc_id,
                    original_size=len(encoded),
                    compressed_size=len(blob),
                    archived_at=float(now),
                )
            )
        if rows:
            with self._lock:
                self._conn.executemany(
                    "INSERT OR REPLACE INTO archive "
                    "(doc_id, compressed_blob, original_size, archived_at) "
                    "VALUES (?, ?, ?, ?)",
                    rows,
                )
                self._conn.commit()
        return results

    def clear(self) -> None:
        """Remove all entries from the archive."""
        with self._lock:
            self._conn.execute("DELETE FROM archive")
            self._conn.commit()

    def close(self) -> None:
        """Close the underlying SQLite connection. Safe to call multiple times."""
        with self._lock:
            if not self._closed:
                self._conn.close()
                self._closed = True
