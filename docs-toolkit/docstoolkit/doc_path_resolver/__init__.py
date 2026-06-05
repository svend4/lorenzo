"""E384 DocPathResolver — resolve hierarchical document paths.

Public API
----------
:class:`PathMapping`      — a single path-to-doc mapping
:class:`PathResolverStats` — aggregate statistics
:class:`DocPathResolver`   — main interface for path resolution
"""

from .resolver import PathMapping, PathResolverStats, DocPathResolver

__all__ = ["PathMapping", "PathResolverStats", "DocPathResolver"]
