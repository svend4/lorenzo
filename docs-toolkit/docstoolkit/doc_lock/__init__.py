"""In-memory document locking system.

Public API
----------
- ``LockType``    — SHARED (read) / EXCLUSIVE (write)
- ``LockState``   — AVAILABLE / LOCKED_SHARED / LOCKED_EXCLUSIVE
- ``LockInfo``    — dataclass describing a held lock
- ``LockError``   — raised for invalid lock operations
- ``LockManager`` — manages shared/exclusive locks with optional timeouts
"""

from docstoolkit.doc_lock.manager import (
    LockError,
    LockInfo,
    LockManager,
    LockState,
    LockType,
)

__all__ = [
    "LockType",
    "LockState",
    "LockInfo",
    "LockError",
    "LockManager",
]
