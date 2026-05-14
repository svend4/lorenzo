"""E403 DocLinkAnchor — named anchors within documents.

Public API
----------
:class:`Anchor`         — a single named anchor
:class:`AnchorStats`    — aggregate statistics
:class:`DocLinkAnchor`  — main interface for anchor management
"""

from .anchor import Anchor, AnchorStats, DocLinkAnchor

__all__ = ["Anchor", "AnchorStats", "DocLinkAnchor"]
