"""E400 DocUrlResolver — resolve document URLs to canonical doc IDs.

Public API
----------
:class:`UrlMapping`     — a single URL-to-doc mapping
:class:`ResolverStats`  — aggregate statistics
:class:`DocUrlResolver` — main interface for URL resolution
"""

from .resolver import UrlMapping, ResolverStats, DocUrlResolver

__all__ = ["UrlMapping", "ResolverStats", "DocUrlResolver"]
