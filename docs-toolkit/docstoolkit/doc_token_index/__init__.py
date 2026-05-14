"""E348 DocTokenIndex — token frequency index for fast term lookup.

Public API
----------
:class:`TokenInfo`     — info about a single token
:class:`IndexStats`    — aggregate statistics
:class:`DocTokenIndex` — main interface for token indexing
"""

from .index import TokenInfo, IndexStats, DocTokenIndex

__all__ = ["TokenInfo", "IndexStats", "DocTokenIndex"]
