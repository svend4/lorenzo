"""E311 DocFlagStore — boolean feature flags and document-level overrides.

Public API
----------
:class:`Flag`          — a feature flag definition
:class:`FlagOverride`  — a per-document flag override
:class:`FlagStats`     — aggregate statistics
:class:`DocFlagStore`  — main interface for flag management
"""

from .store import Flag, FlagOverride, FlagStats, DocFlagStore

__all__ = ["Flag", "FlagOverride", "FlagStats", "DocFlagStore"]
