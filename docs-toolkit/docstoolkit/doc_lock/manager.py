"""In-memory document locking manager.

Implements shared (read) and exclusive (write) locks with optional
expiration timeouts. Thread-safe via ``threading.Lock``.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LockType(Enum):
    """Type of lock that can be acquired on a document."""

    SHARED = "shared"
    EXCLUSIVE = "exclusive"


class LockState(Enum):
    """Observable state of a document's locks."""

    AVAILABLE = "available"
    LOCKED_SHARED = "locked_shared"
    LOCKED_EXCLUSIVE = "locked_exclusive"


class LockError(Exception):
    """Raised on lock-related errors."""


@dataclass
class LockInfo:
    """Information about a single held lock."""

    doc_id: str
    lock_type: LockType
    holder_id: str
    acquired_at: float
    expires_at: Optional[float] = None

    def is_expired(self, now: float) -> bool:
        """Return ``True`` if the lock has expired at ``now``."""
        if self.expires_at is None:
            return False
        return now >= self.expires_at


class LockManager:
    """In-memory manager for shared/exclusive document locks."""

    def __init__(self) -> None:
        self._locks: dict[str, list[LockInfo]] = {}
        self._mutex = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _purge_expired(self, doc_id: str, now: float) -> None:
        """Remove expired locks for ``doc_id`` in-place."""
        locks = self._locks.get(doc_id)
        if not locks:
            return
        live = [lk for lk in locks if not lk.is_expired(now)]
        if live:
            self._locks[doc_id] = live
        else:
            self._locks.pop(doc_id, None)

    def _active_locks(self, doc_id: str, now: float) -> list[LockInfo]:
        self._purge_expired(doc_id, now)
        return list(self._locks.get(doc_id, []))

    # ------------------------------------------------------------------
    # Acquire / release
    # ------------------------------------------------------------------
    def acquire_shared(
        self,
        doc_id: str,
        holder_id: str,
        timeout: Optional[float] = None,
        now: float = 0.0,
    ) -> bool:
        """Acquire a shared (read) lock on ``doc_id`` for ``holder_id``.

        Multiple shared locks may coexist. Returns ``True`` on success.
        """
        if not doc_id or not holder_id:
            raise LockError("doc_id and holder_id must be non-empty")
        with self._mutex:
            self._purge_expired(doc_id, now)
            locks = self._locks.setdefault(doc_id, [])
            expires_at = (now + timeout) if timeout is not None else None

            # Idempotent: same holder re-acquires → refresh / upgrade-equivalent
            for lk in locks:
                if lk.holder_id == holder_id:
                    if lk.lock_type == LockType.SHARED:
                        lk.expires_at = expires_at
                        lk.acquired_at = now
                        return True
                    # holder currently has exclusive — allow downgrade refresh
                    if lk.lock_type == LockType.EXCLUSIVE:
                        # Treat as refresh of existing exclusive (caller still
                        # owns the doc); keep exclusive but extend timeout.
                        lk.expires_at = expires_at
                        lk.acquired_at = now
                        return True

            # Block if exclusive lock held by anyone else
            for lk in locks:
                if lk.lock_type == LockType.EXCLUSIVE:
                    return False

            locks.append(
                LockInfo(
                    doc_id=doc_id,
                    lock_type=LockType.SHARED,
                    holder_id=holder_id,
                    acquired_at=now,
                    expires_at=expires_at,
                )
            )
            return True

    def acquire_exclusive(
        self,
        doc_id: str,
        holder_id: str,
        timeout: Optional[float] = None,
        now: float = 0.0,
    ) -> bool:
        """Acquire an exclusive (write) lock on ``doc_id`` for ``holder_id``.

        Succeeds only if no other locks exist. Returns ``True`` on success.
        """
        if not doc_id or not holder_id:
            raise LockError("doc_id and holder_id must be non-empty")
        with self._mutex:
            self._purge_expired(doc_id, now)
            locks = self._locks.setdefault(doc_id, [])
            expires_at = (now + timeout) if timeout is not None else None

            # If only this holder has lock(s) — upgrade/refresh to exclusive
            others = [lk for lk in locks if lk.holder_id != holder_id]
            if others:
                return False

            # Replace any existing locks of same holder with a single exclusive
            self._locks[doc_id] = [
                LockInfo(
                    doc_id=doc_id,
                    lock_type=LockType.EXCLUSIVE,
                    holder_id=holder_id,
                    acquired_at=now,
                    expires_at=expires_at,
                )
            ]
            return True

    def release(self, doc_id: str, holder_id: str) -> bool:
        """Release ``holder_id``'s lock on ``doc_id``.

        Returns ``True`` if a lock was released, ``False`` otherwise.
        """
        with self._mutex:
            locks = self._locks.get(doc_id)
            if not locks:
                return False
            remaining = [lk for lk in locks if lk.holder_id != holder_id]
            if len(remaining) == len(locks):
                return False
            if remaining:
                self._locks[doc_id] = remaining
            else:
                self._locks.pop(doc_id, None)
            return True

    def release_all(self, holder_id: str) -> int:
        """Release all locks held by ``holder_id``. Returns count removed."""
        with self._mutex:
            count = 0
            for doc_id in list(self._locks.keys()):
                locks = self._locks[doc_id]
                remaining = [lk for lk in locks if lk.holder_id != holder_id]
                count += len(locks) - len(remaining)
                if remaining:
                    self._locks[doc_id] = remaining
                else:
                    self._locks.pop(doc_id, None)
            return count

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------
    def state(self, doc_id: str, now: float = 0.0) -> LockState:
        """Return current lock state for ``doc_id``."""
        with self._mutex:
            active = self._active_locks(doc_id, now)
            if not active:
                return LockState.AVAILABLE
            if any(lk.lock_type == LockType.EXCLUSIVE for lk in active):
                return LockState.LOCKED_EXCLUSIVE
            return LockState.LOCKED_SHARED

    def holders(self, doc_id: str, now: float = 0.0) -> list[str]:
        """Return list of holder ids currently holding any lock on doc."""
        with self._mutex:
            active = self._active_locks(doc_id, now)
            return [lk.holder_id for lk in active]

    def is_locked(self, doc_id: str, now: float = 0.0) -> bool:
        """Return ``True`` if any active lock exists on ``doc_id``."""
        with self._mutex:
            return bool(self._active_locks(doc_id, now))

    def is_held_by(self, doc_id: str, holder_id: str, now: float = 0.0) -> bool:
        """Return ``True`` if ``holder_id`` currently holds a lock on doc."""
        with self._mutex:
            active = self._active_locks(doc_id, now)
            return any(lk.holder_id == holder_id for lk in active)

    def cleanup_expired(self, now: float = 0.0) -> int:
        """Remove expired locks across all documents. Returns count removed."""
        with self._mutex:
            count = 0
            for doc_id in list(self._locks.keys()):
                locks = self._locks[doc_id]
                live = [lk for lk in locks if not lk.is_expired(now)]
                count += len(locks) - len(live)
                if live:
                    self._locks[doc_id] = live
                else:
                    self._locks.pop(doc_id, None)
            return count

    def lock_count(self, doc_id: Optional[str] = None) -> int:
        """Return number of locks on ``doc_id`` (or total across all docs)."""
        with self._mutex:
            if doc_id is None:
                return sum(len(v) for v in self._locks.values())
            return len(self._locks.get(doc_id, []))

    def all_locked_docs(self, now: float = 0.0) -> list[str]:
        """Return all doc ids that currently have at least one active lock."""
        with self._mutex:
            result = []
            for doc_id in list(self._locks.keys()):
                if self._active_locks(doc_id, now):
                    result.append(doc_id)
            return result

    def info(self, doc_id: str) -> list[LockInfo]:
        """Return a copy of all ``LockInfo`` entries for ``doc_id``."""
        with self._mutex:
            return list(self._locks.get(doc_id, []))
