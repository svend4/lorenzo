"""E301 DocConflictResolver — detect and resolve conflicting document versions.

Public API
----------
:class:`Conflict`          — a detected conflict between two doc versions
:class:`Resolution`        — the result of resolving a conflict
:class:`ResolverStats`     — aggregate statistics
:class:`DocConflictResolver` — main interface for conflict management
"""

from .resolver import Conflict, Resolution, ResolverStats, DocConflictResolver

__all__ = ["Conflict", "Resolution", "ResolverStats", "DocConflictResolver"]
