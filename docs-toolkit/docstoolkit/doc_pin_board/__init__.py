"""E306 DocPinBoard — per-user document pinning with ordered pin lists.

Public API
----------
:class:`PinnedDoc`    — a single pinned document entry
:class:`PinBoardStats` — aggregate statistics
:class:`DocPinBoard`  — main interface for pin management
"""

from .board import PinnedDoc, PinBoardStats, DocPinBoard

__all__ = ["PinnedDoc", "PinBoardStats", "DocPinBoard"]
