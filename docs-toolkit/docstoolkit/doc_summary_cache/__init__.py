"""E401 DocSummaryCache — versioned summary cache for documents.

Public API
----------
:class:`SummaryEntry`    — a single cached summary
:class:`CacheStats`      — aggregate statistics
:class:`DocSummaryCache` — main interface for summary caching
"""

from .cache import SummaryEntry, CacheStats, DocSummaryCache

__all__ = ["SummaryEntry", "CacheStats", "DocSummaryCache"]
