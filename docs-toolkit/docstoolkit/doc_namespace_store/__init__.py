"""E415 DocNamespaceStore — multi-namespace document organization.

Public API
----------
:class:`Namespace`         — a single namespace definition
:class:`NamespaceStats`    — aggregate statistics
:class:`DocNamespaceStore` — main interface for namespace management
"""

from .store import Namespace, NamespaceStats, DocNamespaceStore

__all__ = ["Namespace", "NamespaceStats", "DocNamespaceStore"]
