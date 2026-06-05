"""E397 DocMetadataIndex — indexed key-value metadata for documents.

Public API
----------
:class:`MetaEntry`         — a single metadata entry
:class:`MetaStats`         — aggregate statistics
:class:`DocMetadataIndex`  — main interface for metadata indexing
"""

from .index import MetaEntry, MetaStats, DocMetadataIndex

__all__ = ["MetaEntry", "MetaStats", "DocMetadataIndex"]
