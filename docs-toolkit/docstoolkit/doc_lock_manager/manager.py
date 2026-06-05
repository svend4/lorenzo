"""E310 DocLockManager — optimistic/pessimistic document locking.

Implements read (shared) and write (exclusive) locks with optional TTL
expiration. Thread-safe via ``threading.Lock``. Pure stdlib, no
third-party dependencies.
"""

from __future__ import annotations

import threading
import uuid
import time as _time
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class DocLock:
    """An active lock on a document."""

    lock_id: str
    doc_id: str
    holder: str
    acquired_at: float = 0.0
    expires_at: Optional[float] = None
    lock_type: str = "write"

    def _is_active(self, now: float) -> bool:
        """Return True if the lock has not yet expired at *now*."""
        if self.expires_at is None:
            return True
        return now < self.expires_at


@dataclass
class LockStats:
    """Aggregate lock statistics for a :class:`DocLockManager` instance."""

    total_locks: int
    write_locks: int
    read_locks: int
    unique_docs: int


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------

class DocLockManager:
    """Main interface for acquiring and releasing document locks.

    A *write* lock is exclusive: it can only be acquired when the document
    has no other active locks.

    A *read* lock is shared: multiple readers may coexist, but a read lock
    cannot be acquired while a write lock is active.

    All methods are thread-safe via an internal :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._locks: dict[str, DocLock] = {}           # lock_id → DocLock
        self._doc_locks: dict[str, list[str]] = {}     # doc_id  → [lock_id, ...]
        self._mutex = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _now(self) -> float:
        return _time.monotonic()

    def _active_for_doc(self, doc_id: str, now: float) -> list[DocLock]:
        """Return all active (non-expired) DocLock objects for *doc_id*."""
        ids = self._doc_locks.get(doc_id, [])
        result = []
        for lid in ids:
            lock = self._locks.get(lid)
            if lock is not None and lock._is_active(now):
                result.append(lock)
        return result

    def _remove_lock(self, lock_id: str) -> Optional[DocLock]:
        """Remove a lock from internal storage. Returns removed DocLock or None."""
        lock = self._locks.pop(lock_id, None)
        if lock is not None:
            ids = self._doc_locks.get(lock.doc_id, [])
            try:
                ids.remove(lock_id)
            except ValueError:
                pass
            if not ids:
                self._doc_locks.pop(lock.doc_id, None)
            else:
                self._doc_locks[lock.doc_id] = ids
        return lock

    # ------------------------------------------------------------------
    # Acquire
    # ------------------------------------------------------------------

    def acquire(
        self,
        doc_id: str,
        holder: str,
        lock_type: str = "write",
        ttl_seconds: Optional[float] = None,
        now: Optional[float] = None,
    ) -> Optional[DocLock]:
        """Try to acquire a lock on *doc_id* for *holder*.

        Parameters
        ----------
        doc_id:
            Identifier of the document to lock.
        holder:
            User or process requesting the lock.
        lock_type:
            ``"write"`` (exclusive) or ``"read"`` (shared).
        ttl_seconds:
            Optional time-to-live in seconds.  ``None`` means the lock
            never expires.
        now:
            Current timestamp (seconds).  Defaults to
            :func:`time.monotonic`.

        Returns
        -------
        DocLock
            The newly created lock if acquisition succeeded.
        None
            If the lock could not be acquired due to a conflicting lock.
        """
        if now is None:
            now = self._now()

        with self._mutex:
            active = self._active_for_doc(doc_id, now)

            if lock_type == "write":
                # Write lock requires no active locks at all.
                if active:
                    return None
            else:
                # Read lock requires no active write locks.
                if any(lk.lock_type == "write" for lk in active):
                    return None

            expires_at = (now + ttl_seconds) if ttl_seconds is not None else None
            lock = DocLock(
                lock_id=str(uuid.uuid4()),
                doc_id=doc_id,
                holder=holder,
                acquired_at=now,
                expires_at=expires_at,
                lock_type=lock_type,
            )
            self._locks[lock.lock_id] = lock
            self._doc_locks.setdefault(doc_id, []).append(lock.lock_id)
            return lock

    # ------------------------------------------------------------------
    # Release
    # ------------------------------------------------------------------

    def release(self, lock_id: str) -> bool:
        """Remove the lock identified by *lock_id*.

        Returns ``True`` if the lock existed and was removed, ``False``
        otherwise.
        """
        with self._mutex:
            removed = self._remove_lock(lock_id)
            return removed is not None

    def release_all(self, doc_id: str) -> int:
        """Release all locks on *doc_id* (active or expired).

        Returns the number of locks removed.
        """
        with self._mutex:
            ids = list(self._doc_locks.get(doc_id, []))
            count = 0
            for lid in ids:
                if self._remove_lock(lid) is not None:
                    count += 1
            return count

    def release_by_holder(self, holder: str) -> int:
        """Release all locks held by *holder* across all documents.

        Returns the number of locks removed.
        """
        with self._mutex:
            to_remove = [
                lid for lid, lk in self._locks.items() if lk.holder == holder
            ]
            count = 0
            for lid in to_remove:
                if self._remove_lock(lid) is not None:
                    count += 1
            return count

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def get_lock(self, lock_id: str) -> Optional[DocLock]:
        """Return the :class:`DocLock` for *lock_id*, or ``None``."""
        with self._mutex:
            return self._locks.get(lock_id)

    def locks_for_doc(
        self, doc_id: str, now: Optional[float] = None
    ) -> list[DocLock]:
        """Return all active locks for *doc_id*, sorted by *acquired_at*.

        Expired locks are excluded.
        """
        if now is None:
            now = self._now()
        with self._mutex:
            active = self._active_for_doc(doc_id, now)
            return sorted(active, key=lambda lk: lk.acquired_at)

    def is_locked(self, doc_id: str, now: Optional[float] = None) -> bool:
        """Return ``True`` if *doc_id* has at least one active lock."""
        if now is None:
            now = self._now()
        with self._mutex:
            return bool(self._active_for_doc(doc_id, now))

    def is_write_locked(self, doc_id: str, now: Optional[float] = None) -> bool:
        """Return ``True`` if *doc_id* has an active write lock."""
        if now is None:
            now = self._now()
        with self._mutex:
            return any(
                lk.lock_type == "write"
                for lk in self._active_for_doc(doc_id, now)
            )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def expire_stale(self, now: Optional[float] = None) -> int:
        """Remove all expired locks.

        Returns the number of locks removed.
        """
        if now is None:
            now = self._now()
        with self._mutex:
            expired = [
                lid
                for lid, lk in self._locks.items()
                if lk.expires_at is not None and now >= lk.expires_at
            ]
            count = 0
            for lid in expired:
                if self._remove_lock(lid) is not None:
                    count += 1
            return count

    def stats(self, now: Optional[float] = None) -> LockStats:
        """Return aggregate :class:`LockStats` for currently active locks."""
        if now is None:
            now = self._now()
        with self._mutex:
            write_count = 0
            read_count = 0
            docs: set[str] = set()
            for lk in self._locks.values():
                if not lk._is_active(now):
                    continue
                docs.add(lk.doc_id)
                if lk.lock_type == "write":
                    write_count += 1
                else:
                    read_count += 1
            total = write_count + read_count
            return LockStats(
                total_locks=total,
                write_locks=write_count,
                read_locks=read_count,
                unique_docs=len(docs),
            )
