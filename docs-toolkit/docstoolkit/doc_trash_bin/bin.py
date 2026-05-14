"""E417 DocTrashBin — soft-delete trash bin with restore capability.

A :class:`DocTrashBin` keeps soft-deleted documents in memory keyed by
``doc_id``. Each entry has an optional expiration time so callers can implement
retention policies on top of it. The bin is thread-safe via an internal
:class:`threading.Lock` and only uses the Python standard library.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class TrashedDoc:
    """A single trashed (soft-deleted) document."""

    doc_id: str
    content: str
    trashed_at: float = 0.0
    trashed_by: str = ""
    reason: str = ""
    expires_at: Optional[float] = None
    metadata: dict = field(default_factory=dict)

    def is_expired(self, now: float) -> bool:
        """Return True if this doc's ``expires_at`` is set and in the past."""
        return self.expires_at is not None and self.expires_at < now


@dataclass
class TrashStats:
    """Aggregate statistics across the trash bin."""

    total_trashed: int
    expired_count: int
    total_size_chars: int


# ---------------------------------------------------------------------------
# DocTrashBin
# ---------------------------------------------------------------------------


class DocTrashBin:
    """Thread-safe in-memory trash bin for soft-deleted documents."""

    def __init__(self) -> None:
        self._trash: Dict[str, TrashedDoc] = {}
        self._lock = threading.Lock()

    # -- internal ---------------------------------------------------------

    @staticmethod
    def _resolve_now(now: Optional[float]) -> float:
        return float(now) if now is not None else float(time.time())

    # -- core operations --------------------------------------------------

    def trash(
        self,
        doc_id: str,
        content: str,
        trashed_by: str = "",
        reason: str = "",
        retention_seconds: Optional[float] = None,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> TrashedDoc:
        """Trash ``content`` under ``doc_id``. Overwrites any existing entry.

        If ``retention_seconds`` is provided, ``expires_at`` is computed as
        ``now + retention_seconds``. ``metadata`` defaults to an empty dict.
        """
        ts = self._resolve_now(now)
        expires_at: Optional[float]
        if retention_seconds is not None:
            expires_at = ts + float(retention_seconds)
        else:
            expires_at = None
        doc = TrashedDoc(
            doc_id=doc_id,
            content=content,
            trashed_at=ts,
            trashed_by=trashed_by,
            reason=reason,
            expires_at=expires_at,
            metadata=dict(metadata) if metadata is not None else {},
        )
        with self._lock:
            self._trash[doc_id] = doc
        return doc

    def restore(self, doc_id: str) -> Optional[TrashedDoc]:
        """Pop and return the trashed doc, or ``None`` if not present."""
        with self._lock:
            return self._trash.pop(doc_id, None)

    def peek(self, doc_id: str) -> Optional[TrashedDoc]:
        """Return the trashed doc without removing it, or ``None``."""
        with self._lock:
            return self._trash.get(doc_id)

    def purge(self, doc_id: str) -> bool:
        """Permanently delete ``doc_id`` from the trash. Return True if removed."""
        with self._lock:
            if doc_id in self._trash:
                del self._trash[doc_id]
                return True
            return False

    def purge_expired(self, now: Optional[float] = None) -> int:
        """Remove every doc whose ``expires_at`` is set and < ``now``.

        Returns the number of entries removed.
        """
        ts = self._resolve_now(now)
        with self._lock:
            to_remove = [
                did
                for did, doc in self._trash.items()
                if doc.expires_at is not None and doc.expires_at < ts
            ]
            for did in to_remove:
                del self._trash[did]
            return len(to_remove)

    def purge_all(self) -> int:
        """Remove every entry. Return the number purged."""
        with self._lock:
            count = len(self._trash)
            self._trash.clear()
            return count

    def is_trashed(self, doc_id: str) -> bool:
        """Return True if ``doc_id`` is currently in the trash."""
        with self._lock:
            return doc_id in self._trash

    def list_trashed(self) -> List[TrashedDoc]:
        """Return every trashed doc, sorted by ``trashed_at`` descending."""
        with self._lock:
            docs = list(self._trash.values())
        docs.sort(key=lambda d: d.trashed_at, reverse=True)
        return docs

    def expiring_soon(
        self, within_seconds: float = 86400, now: Optional[float] = None
    ) -> List[TrashedDoc]:
        """Return docs that will expire within ``within_seconds`` of ``now``.

        Already-expired docs are excluded. Sorted by ``expires_at`` ascending.
        """
        ts = self._resolve_now(now)
        horizon = ts + float(within_seconds)
        with self._lock:
            docs = [
                doc
                for doc in self._trash.values()
                if doc.expires_at is not None
                and doc.expires_at >= ts
                and doc.expires_at <= horizon
            ]
        docs.sort(key=lambda d: (d.expires_at if d.expires_at is not None else 0.0))
        return docs

    def expired(self, now: Optional[float] = None) -> List[TrashedDoc]:
        """Return every already-expired doc, sorted by ``expires_at`` ascending."""
        ts = self._resolve_now(now)
        with self._lock:
            docs = [
                doc
                for doc in self._trash.values()
                if doc.expires_at is not None and doc.expires_at < ts
            ]
        docs.sort(key=lambda d: (d.expires_at if d.expires_at is not None else 0.0))
        return docs

    def total_size(self) -> int:
        """Return the summed character length of all content in the trash."""
        with self._lock:
            return sum(len(doc.content) for doc in self._trash.values())

    def stats(self, now: Optional[float] = None) -> TrashStats:
        """Return aggregate statistics across the trash bin."""
        ts = self._resolve_now(now)
        with self._lock:
            total = len(self._trash)
            expired = sum(
                1
                for doc in self._trash.values()
                if doc.expires_at is not None and doc.expires_at < ts
            )
            size = sum(len(doc.content) for doc in self._trash.values())
        return TrashStats(
            total_trashed=total,
            expired_count=expired,
            total_size_chars=size,
        )
