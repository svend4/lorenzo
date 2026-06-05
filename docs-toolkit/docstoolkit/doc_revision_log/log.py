"""E340 DocRevisionLog — chronological revision log with revision content.

Public API
----------
- ``Revision``         — a single revision of a document
- ``RevisionLogStats`` — aggregate statistics
- ``DocRevisionLog``   — main interface for revision log management
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Revision:
    """A single revision of a document."""

    revision_id: int
    doc_id: str
    revision_number: int
    content: str
    author: str = ""
    created_at: float = 0.0
    message: str = ""
    parent_revision: Optional[int] = None


@dataclass
class RevisionLogStats:
    """Aggregate statistics over the revision log."""

    total_revisions: int
    unique_docs: int
    unique_authors: int


# ---------------------------------------------------------------------------
# DocRevisionLog
# ---------------------------------------------------------------------------


class DocRevisionLog:
    """Thread-safe chronological revision log for documents.

    Each :meth:`commit` call appends a :class:`Revision` capturing the full
    content of the document at that point in time.  Revisions are indexed by
    global ``revision_id`` and by document.  Within a single document,
    ``revision_number`` increases monotonically starting at 1.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._revisions: dict[int, Revision] = {}
        self._by_doc: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._next_doc_revision: dict[str, int] = {}

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def commit(
        self,
        doc_id: str,
        content: str,
        author: str = "",
        message: str = "",
        now: Optional[float] = None,
    ) -> Revision:
        """Commit a new revision and return the resulting :class:`Revision`."""
        ts = time.time() if now is None else now
        with self._lock:
            revision_id = self._next_id
            self._next_id += 1
            revision_number = self._next_doc_revision.get(doc_id, 1)
            self._next_doc_revision[doc_id] = revision_number + 1
            doc_ids = self._by_doc.setdefault(doc_id, [])
            parent_revision = doc_ids[-1] if doc_ids else None
            rev = Revision(
                revision_id=revision_id,
                doc_id=doc_id,
                revision_number=revision_number,
                content=content,
                author=author,
                created_at=ts,
                message=message,
                parent_revision=parent_revision,
            )
            self._revisions[revision_id] = rev
            doc_ids.append(revision_id)
        return rev

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get_revision(self, revision_id: int) -> Optional[Revision]:
        """Return the revision with *revision_id*, or ``None`` if not found."""
        with self._lock:
            return self._revisions.get(revision_id)

    def get_by_number(
        self, doc_id: str, revision_number: int
    ) -> Optional[Revision]:
        """Return revision *revision_number* for *doc_id*, or ``None``."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            for rid in ids:
                rev = self._revisions.get(rid)
                if rev is not None and rev.revision_number == revision_number:
                    return rev
        return None

    def latest(self, doc_id: str) -> Optional[Revision]:
        """Return the most recent revision for *doc_id*, or ``None``."""
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            if not ids:
                return None
            return self._revisions.get(ids[-1])

    def revisions_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> list[Revision]:
        """Return all revisions for *doc_id* sorted by ``revision_number``
        descending (most recent first)."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            revs = [self._revisions[i] for i in ids if i in self._revisions]
        revs.sort(key=lambda r: r.revision_number, reverse=True)
        if limit is not None:
            revs = revs[:limit]
        return revs

    def revisions_by_author(
        self, author: str, limit: Optional[int] = None
    ) -> list[Revision]:
        """Return all revisions by *author* sorted by ``created_at`` desc."""
        with self._lock:
            revs = [r for r in self._revisions.values() if r.author == author]
        revs.sort(key=lambda r: r.created_at, reverse=True)
        if limit is not None:
            revs = revs[:limit]
        return revs

    def revision_count(self, doc_id: str) -> int:
        """Return the number of revisions recorded for *doc_id*."""
        with self._lock:
            return len(self._by_doc.get(doc_id, []))

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def revert_to(
        self,
        doc_id: str,
        revision_number: int,
        author: str = "",
        message: str = "",
        now: Optional[float] = None,
    ) -> Optional[Revision]:
        """Create a new revision with content from *revision_number*.

        Returns the new :class:`Revision`.  If the target revision does not
        exist, returns ``None`` without creating any new revision.
        """
        target = self.get_by_number(doc_id, revision_number)
        if target is None:
            return None
        return self.commit(
            doc_id=doc_id,
            content=target.content,
            author=author,
            message=message,
            now=now,
        )

    def delete_doc_revisions(self, doc_id: str) -> int:
        """Remove all revisions for *doc_id* and return the number removed."""
        with self._lock:
            ids = self._by_doc.pop(doc_id, [])
            if not ids:
                # Ensure counter slot is also gone, if it existed.
                self._next_doc_revision.pop(doc_id, None)
                return 0
            for rid in ids:
                self._revisions.pop(rid, None)
            self._next_doc_revision.pop(doc_id, None)
            return len(ids)

    # ------------------------------------------------------------------
    # Enumeration / stats
    # ------------------------------------------------------------------

    def all_doc_ids(self) -> list[str]:
        """Return a sorted list of doc IDs with at least one revision."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> RevisionLogStats:
        """Return aggregate statistics over the revision log."""
        with self._lock:
            total = len(self._revisions)
            unique_docs = len(self._by_doc)
            unique_authors = len(
                {r.author for r in self._revisions.values() if r.author}
            )
        return RevisionLogStats(
            total_revisions=total,
            unique_docs=unique_docs,
            unique_authors=unique_authors,
        )
