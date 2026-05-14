"""E394 DocOutlineBuilder — build hierarchical outline from document headings.

Public API
----------
:class:`OutlineNode`      — a single node in a document outline
:class:`OutlineStats`     — aggregate statistics
:class:`DocOutlineBuilder` — main interface for outline construction
"""

from .builder import OutlineNode, OutlineStats, DocOutlineBuilder

__all__ = ["OutlineNode", "OutlineStats", "DocOutlineBuilder"]
