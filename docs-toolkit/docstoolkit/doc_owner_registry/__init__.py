"""E391 DocOwnerRegistry — document ownership tracking.

Public API
----------
:class:`Ownership`        — a single doc ownership record
:class:`OwnershipStats`   — aggregate statistics
:class:`DocOwnerRegistry` — main interface for ownership management
"""

from .registry import Ownership, OwnershipStats, DocOwnerRegistry

__all__ = ["Ownership", "OwnershipStats", "DocOwnerRegistry"]
