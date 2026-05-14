"""E355 DocRelationGraph — typed relationships between documents.

Public API
----------
:class:`Relation`        — a single typed relation between two docs
:class:`RelationStats`   — aggregate statistics
:class:`DocRelationGraph` — main interface for relation management
"""

from .graph import Relation, RelationStats, DocRelationGraph

__all__ = ["Relation", "RelationStats", "DocRelationGraph"]
