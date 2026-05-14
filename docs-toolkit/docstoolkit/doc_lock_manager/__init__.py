"""E310 DocLockManager — optimistic/pessimistic document locking.

Public API
----------
:class:`DocLock`        — an active lock on a document
:class:`LockStats`      — aggregate lock statistics
:class:`DocLockManager` — main interface for acquiring and releasing locks
"""

from .manager import DocLock, LockStats, DocLockManager

__all__ = ["DocLock", "LockStats", "DocLockManager"]
