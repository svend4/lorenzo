"""E298 DocDependencyGraph — directed dependency graph for documents.

Public API
----------
:class:`DependencyEdge`   — a single directed dependency between two docs
:class:`GraphStats`       — aggregate statistics for the graph
:class:`DocDependencyGraph` — main interface for dependency management
"""

from .graph import DependencyEdge, GraphStats, DocDependencyGraph

__all__ = ["DependencyEdge", "GraphStats", "DocDependencyGraph"]
