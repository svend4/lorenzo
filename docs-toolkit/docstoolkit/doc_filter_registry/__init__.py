"""E341 DocFilterRegistry — saved filter/query registry for documents.

Public API
----------
:class:`SavedFilter`     — a single saved filter
:class:`FilterStats`     — aggregate statistics
:class:`DocFilterRegistry` — main interface for filter management
"""

from .registry import SavedFilter, FilterStats, DocFilterRegistry

__all__ = ["SavedFilter", "FilterStats", "DocFilterRegistry"]
