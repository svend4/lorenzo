"""E315 DocLinkGraph — track hyperlinks between documents.

Public API
----------
:class:`DocLink`       — a directed link from one doc to another
:class:`LinkGraphStats` — aggregate statistics
:class:`DocLinkGraph`  — main interface for link graph management
"""

from .graph import DocLink, LinkGraphStats, DocLinkGraph

__all__ = ["DocLink", "LinkGraphStats", "DocLinkGraph"]
