"""E319 DocHierarchyStore — tree-structured document hierarchy management.

Public API
----------
:class:`HierarchyNode`   — a node in the document hierarchy
:class:`HierarchyStats`  — aggregate statistics
:class:`DocHierarchyStore` — main interface for hierarchy management
"""

from .store import HierarchyNode, HierarchyStats, DocHierarchyStore

__all__ = ["HierarchyNode", "HierarchyStats", "DocHierarchyStore"]
