"""DocAliasResolver — resolve symbolic doc aliases to canonical IDs.

Aliases form a directed mapping ``alias -> target``.  ``target`` may itself
be a registered alias, so :meth:`DocAliasResolver.resolve` follows the chain
up to ``max_hops`` steps, caching successful resolutions.  Cycles are
detected and yield ``None``.

The module is pure stdlib and thread-safe via a single ``threading.Lock``.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class DocAlias:
    """A registered alias and its immediate target."""

    alias: str
    target: str
    created_at: float = 0.0


@dataclass
class ResolutionStats:
    """Aggregate counters reported by :meth:`DocAliasResolver.stats`."""

    total_aliases: int
    unique_targets: int
    total_resolutions: int
    cache_hits: int


class DocAliasResolver:
    """Maintain a registry of doc aliases and resolve them to canonical IDs.

    The resolver is intentionally minimal: it stores ``alias -> target``
    mappings, follows alias chains, and caches the terminal target for each
    successful resolution.  Mutating the registry invalidates the cache.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._aliases: dict[str, DocAlias] = {}
        self._cache: dict[str, str] = {}
        self._total_resolutions: int = 0
        self._cache_hits: int = 0

    # ------------------------------------------------------------ registration

    def register_alias(
        self,
        alias: str,
        target: str,
        now: Optional[float] = None,
    ) -> DocAlias:
        """Register (or replace) an alias mapping.

        The internal resolution cache is invalidated on every change so that
        previously cached chains cannot return stale data.
        """
        ts = now if now is not None else time.time()
        entry = DocAlias(alias=alias, target=target, created_at=ts)
        with self._lock:
            self._aliases[alias] = entry
            self._cache.clear()
        return entry

    def unregister_alias(self, alias: str) -> bool:
        """Remove an alias.  Returns ``True`` if the alias existed."""
        with self._lock:
            if alias in self._aliases:
                del self._aliases[alias]
                self._cache.clear()
                return True
            return False

    # ------------------------------------------------------------------ lookup

    def get_alias(self, alias: str) -> Optional[DocAlias]:
        """Return the :class:`DocAlias` registered under ``alias`` if any."""
        with self._lock:
            return self._aliases.get(alias)

    # -------------------------------------------------------------- resolution

    def resolve(self, alias: str, max_hops: int = 10) -> Optional[str]:
        """Resolve ``alias`` by walking the alias chain.

        - If ``alias`` is not registered, returns ``alias`` unchanged.
        - Successful resolutions are cached.
        - Cycles return ``None``.
        - Exceeding ``max_hops`` returns ``None``.
        Counters for total resolutions / cache hits are incremented.
        """
        with self._lock:
            self._total_resolutions += 1

            if alias not in self._aliases:
                # Unregistered: identity passthrough (not cached).
                return alias

            cached = self._cache.get(alias)
            if cached is not None:
                self._cache_hits += 1
                return cached

            seen: set[str] = set()
            current = alias
            hops = 0
            while True:
                if current in seen:
                    return None
                seen.add(current)
                entry = self._aliases.get(current)
                if entry is None:
                    # Reached a non-alias — that is the canonical target.
                    self._cache[alias] = current
                    return current
                if hops >= max_hops:
                    return None
                current = entry.target
                hops += 1

    def resolve_strict(
        self, alias: str, max_hops: int = 10
    ) -> Optional[str]:
        """Like :meth:`resolve` but returns ``None`` for unregistered aliases."""
        with self._lock:
            if alias not in self._aliases:
                # Still count as an attempted resolution.
                self._total_resolutions += 1
                return None
        return self.resolve(alias, max_hops=max_hops)

    # --------------------------------------------------------------- inventory

    def aliases_for(self, target: str) -> list[str]:
        """Return sorted aliases whose *immediate* target equals ``target``."""
        with self._lock:
            return sorted(
                a for a, entry in self._aliases.items() if entry.target == target
            )

    def list_aliases(self) -> list[DocAlias]:
        """Return all registered :class:`DocAlias` entries sorted by alias."""
        with self._lock:
            return [self._aliases[k] for k in sorted(self._aliases)]

    # ---------------------------------------------------------------- cleanup

    def clear_cache(self) -> int:
        """Drop the resolution cache, returning the number of evicted entries."""
        with self._lock:
            n = len(self._cache)
            self._cache.clear()
            return n

    def clear_all(self) -> int:
        """Remove all aliases and clear the cache.

        Returns the number of aliases that were removed.
        """
        with self._lock:
            n = len(self._aliases)
            self._aliases.clear()
            self._cache.clear()
            return n

    # ------------------------------------------------------------------ stats

    def stats(self) -> ResolutionStats:
        """Snapshot of registry size and resolution counters."""
        with self._lock:
            targets = {entry.target for entry in self._aliases.values()}
            return ResolutionStats(
                total_aliases=len(self._aliases),
                unique_targets=len(targets),
                total_resolutions=self._total_resolutions,
                cache_hits=self._cache_hits,
            )
