"""Tag-based cache invalidation module (E100).

Provides an in-memory :class:`TaggedCache` whose entries are associated
with one or more string tags.  Invalidating a tag atomically removes every
entry that carries it.  The implementation is thread-safe and uses only the
Python standard library.

Typical usage::

    from docstoolkit.cache_invalidation import TaggedCache, CacheEntry

    cache = TaggedCache()
    cache.set("user:42", {"name": "Alice"}, tags={"users", "profile"})
    cache.get("user:42")           # {"name": "Alice"}
    cache.invalidate_tag("users")  # removes user:42
    cache.get("user:42")           # None
"""
from docstoolkit.cache_invalidation.cache import CacheEntry, TaggedCache

__all__ = [
    "CacheEntry",
    "TaggedCache",
]
