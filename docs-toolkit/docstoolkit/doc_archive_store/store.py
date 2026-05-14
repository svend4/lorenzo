"""E316 DocArchiveStore — in-memory archive and restore of document versions.

All operations are thread-safe via a single ``threading.Lock``.
No third-party dependencies; only the Python standard library is used.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class ArchivedDoc:
    """A single archived document snapshot."""

    archive_id: str
    doc_id: str
    content: str
    archived_at: float = 0.0
    archived_by: str = ""
    reason: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class ArchiveStats:
    """Aggregate statistics over all archives held in the store."""

    total_archives: int
    unique_docs: int
    total_size_chars: int


# ---------------------------------------------------------------------------
# DocArchiveStore
# ---------------------------------------------------------------------------


class DocArchiveStore:
    """Thread-safe in-memory store for archiving and restoring document versions.

    Archives are keyed by a UUID ``archive_id``; the insertion order for each
    document is preserved so that ``restore_latest`` always returns the most
    recently archived snapshot.
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        # archive_id → ArchivedDoc
        self._archives: Dict[str, ArchivedDoc] = {}
        # doc_id → list of archive_ids in insertion order
        self._by_doc: Dict[str, List[str]] = {}

    # ------------------------------------------------------------------
    # Mutating operations
    # ------------------------------------------------------------------

    def archive(
        self,
        doc_id: str,
        content: str,
        archived_by: str = "",
        reason: str = "",
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> ArchivedDoc:
        """Create a new archive snapshot for *doc_id*.

        Parameters
        ----------
        doc_id:
            Identifier of the document being archived.
        content:
            Full text content to store.
        archived_by:
            Optional actor/user who triggered the archive.
        reason:
            Optional reason string (e.g. ``"manual"``, ``"auto"``,
            ``"pre-delete"``).
        metadata:
            Optional arbitrary key/value pairs stored alongside the snapshot.
        now:
            Timestamp to use for ``archived_at``; defaults to
            ``time.time()``.

        Returns
        -------
        ArchivedDoc
            The newly created archive record.
        """
        archive_id = str(uuid.uuid4())
        archived_at = now if now is not None else time.time()
        doc = ArchivedDoc(
            archive_id=archive_id,
            doc_id=doc_id,
            content=content,
            archived_at=archived_at,
            archived_by=archived_by,
            reason=reason,
            metadata=dict(metadata) if metadata is not None else {},
        )
        with self._lock:
            self._archives[archive_id] = doc
            self._by_doc.setdefault(doc_id, []).append(archive_id)
        return doc

    def delete_archive(self, archive_id: str) -> bool:
        """Remove a single archive by its *archive_id*.

        Returns
        -------
        bool
            ``True`` if the archive existed and was removed; ``False``
            otherwise.
        """
        with self._lock:
            doc = self._archives.pop(archive_id, None)
            if doc is None:
                return False
            ids = self._by_doc.get(doc.doc_id, [])
            try:
                ids.remove(archive_id)
            except ValueError:
                pass
            if not ids:
                self._by_doc.pop(doc.doc_id, None)
            return True

    def purge_doc(self, doc_id: str) -> int:
        """Delete **all** archives for *doc_id*.

        Returns
        -------
        int
            Number of archives that were removed.
        """
        with self._lock:
            ids = self._by_doc.pop(doc_id, [])
            for aid in ids:
                self._archives.pop(aid, None)
            return len(ids)

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def restore_latest(self, doc_id: str) -> Optional[ArchivedDoc]:
        """Return the most recently archived snapshot for *doc_id*.

        "Most recently" means the **last** one appended via :meth:`archive`
        (insertion order).

        Returns ``None`` if no archives exist for *doc_id*.
        """
        with self._lock:
            ids = self._by_doc.get(doc_id)
            if not ids:
                return None
            return self._archives.get(ids[-1])

    def restore_by_id(self, archive_id: str) -> Optional[ArchivedDoc]:
        """Return the archive with the given *archive_id*, or ``None``."""
        with self._lock:
            return self._archives.get(archive_id)

    def get_archive(self, archive_id: str) -> Optional[ArchivedDoc]:
        """Alias for :meth:`restore_by_id`."""
        with self._lock:
            return self._archives.get(archive_id)

    def archives_for_doc(
        self,
        doc_id: str,
        limit: Optional[int] = None,
    ) -> List[ArchivedDoc]:
        """Return archives for *doc_id* in most-recent-first order.

        Parameters
        ----------
        doc_id:
            The document whose archives to retrieve.
        limit:
            If given, return at most *limit* archives (still most-recent
            first).
        """
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
        # Reverse so most-recent (last inserted) comes first
        ids.reverse()
        if limit is not None:
            ids = ids[:limit]
        with self._lock:
            return [self._archives[aid] for aid in ids if aid in self._archives]

    def all_doc_ids(self) -> List[str]:
        """Return a sorted list of doc IDs that have at least one archive."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> ArchiveStats:
        """Return aggregate statistics over all archives currently held."""
        with self._lock:
            total_archives = len(self._archives)
            unique_docs = len(self._by_doc)
            total_size_chars = sum(
                len(doc.content) for doc in self._archives.values()
            )
        return ArchiveStats(
            total_archives=total_archives,
            unique_docs=unique_docs,
            total_size_chars=total_size_chars,
        )
