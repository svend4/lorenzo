"""E421 DocAnchorIndex — inverted index over doc anchors for fast lookup.

Public API
----------
:class:`AnchorRef`       — a single anchor reference
:class:`AnchorStats`     — aggregate statistics
:class:`DocAnchorIndex`  — main interface for anchor indexing
"""

from .index import AnchorRef, AnchorStats, DocAnchorIndex

__all__ = ["AnchorRef", "AnchorStats", "DocAnchorIndex"]
