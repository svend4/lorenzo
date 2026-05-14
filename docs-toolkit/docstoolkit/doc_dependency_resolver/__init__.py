"""E429 DocDependencyResolver — resolve dependency order and detect cycles.

Public API
----------
:class:`Dependency`           — a single dependency edge
:class:`ResolutionResult`     — result of resolving dependencies
:class:`ResolverStats`        — aggregate statistics
:class:`DocDependencyResolver` — main interface for dependency resolution
"""

from .resolver import Dependency, ResolutionResult, ResolverStats, DocDependencyResolver

__all__ = ["Dependency", "ResolutionResult", "ResolverStats", "DocDependencyResolver"]
