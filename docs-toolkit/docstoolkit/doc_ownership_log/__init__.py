"""E440 DocOwnershipLog — append-only log of ownership transfers.

Public API
----------
:class:`OwnershipEvent`  — a single ownership event
:class:`OwnershipStats`  — aggregate statistics
:class:`DocOwnershipLog` — main interface for ownership log
"""

from .log import OwnershipEvent, OwnershipStats, DocOwnershipLog

__all__ = ["OwnershipEvent", "OwnershipStats", "DocOwnershipLog"]
