"""E337 DocTagHierarchy — hierarchical tag taxonomy for documents.

Public API
----------
:class:`TagNode`         — a node in the tag hierarchy
:class:`TagHierarchyStats` — aggregate statistics
:class:`DocTagHierarchy` — main interface for hierarchical tag management
"""

from .hierarchy import TagNode, TagHierarchyStats, DocTagHierarchy

__all__ = ["TagNode", "TagHierarchyStats", "DocTagHierarchy"]
