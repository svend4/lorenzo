"""E388 DocTokenAliasMap — token alias mapping for doc text normalization.

Public API
----------
:class:`TokenAlias`        — a single token alias
:class:`AliasMapStats`     — aggregate statistics
:class:`DocTokenAliasMap`  — main interface for alias mapping
"""

from .map import TokenAlias, AliasMapStats, DocTokenAliasMap

__all__ = ["TokenAlias", "AliasMapStats", "DocTokenAliasMap"]
