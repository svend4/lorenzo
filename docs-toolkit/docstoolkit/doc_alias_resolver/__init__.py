"""E377 DocAliasResolver — resolve symbolic doc aliases to canonical IDs.

Public API
----------
:class:`DocAlias`         — a registered alias
:class:`ResolutionStats`  — aggregate statistics
:class:`DocAliasResolver` — main interface for alias resolution
"""

from .resolver import DocAlias, ResolutionStats, DocAliasResolver

__all__ = ["DocAlias", "ResolutionStats", "DocAliasResolver"]
