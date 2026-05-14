"""E362 DocLayoutStore — document layout/template position storage.

Public API
----------
:class:`LayoutBlock`     — a positioned block within a layout
:class:`DocLayout`       — a complete layout for a document
:class:`LayoutStats`     — aggregate statistics
:class:`DocLayoutStore`  — main interface for layout management
"""

from .store import LayoutBlock, DocLayout, LayoutStats, DocLayoutStore

__all__ = ["LayoutBlock", "DocLayout", "LayoutStats", "DocLayoutStore"]
