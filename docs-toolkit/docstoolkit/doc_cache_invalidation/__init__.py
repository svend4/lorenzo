"""Document cache invalidation module (E262).

Provides pattern-based cache invalidation for documents.  Supports
invalidation by document id, tag, tag set (any/all), regex pattern,
dependency, TTL, and manual deletion.  Uses only :mod:`threading` and
:mod:`re` from the standard library.

Typical usage::

    from docstoolkit.doc_cache_invalidation import DocCacheInvalidation

    cache = DocCacheInvalidation()
    cache.set("k1", doc_id="doc1", value={"title": "T"}, tags={"a"})
    cache.get("k1")                       # {"title": "T"}
    cache.invalidate_by_tag("a")          # removes k1
"""
from docstoolkit.doc_cache_invalidation.cache import (
    CacheKey,
    CacheStats,
    DocCacheInvalidation,
    InvalidationEvent,
    InvalidationStrategy,
)

__all__ = [
    "CacheKey",
    "CacheStats",
    "DocCacheInvalidation",
    "InvalidationEvent",
    "InvalidationStrategy",
]
