"""E309 DocShareRegistry — manage document share links and access grants.

Public API
----------
:class:`ShareLink`       — a shareable link for a document
:class:`ShareGrant`      — a direct share grant to a specific user
:class:`ShareStats`      — aggregate statistics
:class:`DocShareRegistry` — main interface for share management
"""

from .registry import ShareLink, ShareGrant, ShareStats, DocShareRegistry

__all__ = ["ShareLink", "ShareGrant", "ShareStats", "DocShareRegistry"]
