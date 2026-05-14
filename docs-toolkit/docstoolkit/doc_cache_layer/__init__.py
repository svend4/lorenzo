"""E339 DocCacheLayer — LRU+TTL cache for document data.

Public API
----------
:class:`CacheEntry`    — a single cache entry
:class:`CacheStats`    — aggregate cache statistics
:class:`DocCacheLayer` — main interface for cache management
"""

from .layer import CacheEntry, CacheStats, DocCacheLayer

__all__ = ["CacheEntry", "CacheStats", "DocCacheLayer"]
