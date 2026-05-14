"""E228 doc_redirect: redirect store with chain resolution and loop detection."""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enum: RedirectType
# ---------------------------------------------------------------------------


class RedirectType(Enum):
    """Type of redirect — mirrors common HTTP status semantics."""

    PERMANENT_301 = "permanent_301"
    TEMPORARY_302 = "temporary_302"
    INTERNAL_307 = "internal_307"
    GONE_410 = "gone_410"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Redirect:
    """A single redirect entry."""

    source: str
    target: str
    redirect_type: RedirectType = RedirectType.PERMANENT_301
    created_at: float = 0.0
    last_used: Optional[float] = None
    hit_count: int = 0


@dataclass
class RedirectStats:
    """Aggregate statistics about a redirect store."""

    total_redirects: int
    by_type: dict
    total_hits: int
    top_hit: Optional[Redirect]
    unused_count: int


@dataclass
class ResolutionPath:
    """Result of walking a redirect chain."""

    source: str
    final: str
    chain: list = field(default_factory=list)
    had_loop: bool = False
    loop_at: Optional[str] = None


# ---------------------------------------------------------------------------
# DocRedirect
# ---------------------------------------------------------------------------


_MAX_DEPTH = 32


class DocRedirect:
    """Thread-safe redirect store with chain resolution."""

    def __init__(self) -> None:
        self._redirects: dict = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_redirect(
        self,
        source: str,
        target: str,
        redirect_type: RedirectType = RedirectType.PERMANENT_301,
        now: float = 0.0,
    ) -> Redirect:
        """Register a new redirect. Raises ValueError if source == target."""
        if source == target:
            raise ValueError("Redirect source must differ from target")
        with self._lock:
            redirect = Redirect(
                source=source,
                target=target,
                redirect_type=redirect_type,
                created_at=now,
            )
            self._redirects[source] = redirect
            return redirect

    def remove_redirect(self, source: str) -> bool:
        """Remove a redirect. Returns True if removed, False if absent."""
        with self._lock:
            if source in self._redirects:
                del self._redirects[source]
                return True
            return False

    def update_redirect(
        self,
        source: str,
        target: str = None,
        redirect_type: RedirectType = None,
    ) -> bool:
        """Update target and/or type of an existing redirect."""
        with self._lock:
            redirect = self._redirects.get(source)
            if redirect is None:
                return False
            if target is not None:
                if target == source:
                    raise ValueError("Redirect source must differ from target")
                redirect.target = target
            if redirect_type is not None:
                redirect.redirect_type = redirect_type
            return True

    def lookup(self, source: str) -> Optional[Redirect]:
        """Return the redirect for ``source`` if any."""
        with self._lock:
            return self._redirects.get(source)

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def resolve(
        self,
        source: str,
        follow_chain: bool = True,
        now: float = 0.0,
    ) -> ResolutionPath:
        """Resolve ``source`` to its final target, following the chain if asked."""
        with self._lock:
            chain: list = []
            visited: set = set()
            current = source
            final = source
            had_loop = False
            loop_at: Optional[str] = None

            depth = 0
            while depth < _MAX_DEPTH:
                redirect = self._redirects.get(current)
                if redirect is None:
                    break
                if current in visited:
                    had_loop = True
                    loop_at = current
                    break
                visited.add(current)
                # Track hit on the redirect being traversed.
                redirect.hit_count += 1
                redirect.last_used = now
                chain.append(redirect)
                final = redirect.target

                # GONE_410 is terminal — do not follow further.
                if redirect.redirect_type == RedirectType.GONE_410:
                    break
                if not follow_chain:
                    break
                current = redirect.target
                depth += 1

            return ResolutionPath(
                source=source,
                final=final,
                chain=chain,
                had_loop=had_loop,
                loop_at=loop_at,
            )

    # ------------------------------------------------------------------
    # Inverse lookups & patterns
    # ------------------------------------------------------------------

    def targets_to(self, target: str) -> list:
        """Return all redirects that point directly to ``target``."""
        with self._lock:
            return [r for r in self._redirects.values() if r.target == target]

    def redirects_from_pattern(self, pattern: str) -> list:
        """Return all redirects whose source matches the given regex pattern."""
        regex = re.compile(pattern)
        with self._lock:
            return [r for r in self._redirects.values() if regex.search(r.source)]

    # ------------------------------------------------------------------
    # Loop detection
    # ------------------------------------------------------------------

    def detect_loops(self) -> list:
        """Return a list of loops, each represented as the source list forming the cycle."""
        loops: list = []
        seen_cycles: set = set()
        with self._lock:
            for start in list(self._redirects.keys()):
                visited: list = []
                visited_set: set = set()
                current = start
                depth = 0
                while depth < _MAX_DEPTH:
                    if current in visited_set:
                        # Found a cycle. Extract sub-cycle starting at current.
                        idx = visited.index(current)
                        cycle = visited[idx:]
                        # Normalise representation (rotate so smallest element is first).
                        if cycle:
                            min_idx = cycle.index(min(cycle))
                            rotated = tuple(cycle[min_idx:] + cycle[:min_idx])
                            if rotated not in seen_cycles:
                                seen_cycles.add(rotated)
                                loops.append(list(rotated))
                        break
                    visited.append(current)
                    visited_set.add(current)
                    redirect = self._redirects.get(current)
                    if redirect is None:
                        break
                    current = redirect.target
                    depth += 1
        return loops

    def has_loop(self, source: str) -> bool:
        """Return True if walking from ``source`` lands in a loop."""
        with self._lock:
            visited: set = set()
            current = source
            depth = 0
            while depth < _MAX_DEPTH:
                if current in visited:
                    return True
                visited.add(current)
                redirect = self._redirects.get(current)
                if redirect is None:
                    return False
                current = redirect.target
                depth += 1
            return False

    def chain_length(self, source: str) -> int:
        """Return number of hops in the chain. ``0`` if no redirect, ``-1`` if loop."""
        with self._lock:
            if source not in self._redirects:
                return 0
            visited: set = set()
            current = source
            length = 0
            depth = 0
            while depth < _MAX_DEPTH:
                if current in visited:
                    return -1
                visited.add(current)
                redirect = self._redirects.get(current)
                if redirect is None:
                    return length
                length += 1
                current = redirect.target
                depth += 1
            return length

    # ------------------------------------------------------------------
    # Hits & maintenance
    # ------------------------------------------------------------------

    def track_hit(self, source: str, now: float = 0.0) -> bool:
        """Manually record a hit against an existing redirect."""
        with self._lock:
            redirect = self._redirects.get(source)
            if redirect is None:
                return False
            redirect.hit_count += 1
            redirect.last_used = now
            return True

    def cleanup_unused(self, min_hits: int = 1) -> int:
        """Remove redirects with fewer than ``min_hits`` hits. Returns count removed."""
        with self._lock:
            to_remove = [
                src for src, r in self._redirects.items() if r.hit_count < min_hits
            ]
            for src in to_remove:
                del self._redirects[src]
            return len(to_remove)

    # ------------------------------------------------------------------
    # Stats & utility
    # ------------------------------------------------------------------

    def stats(self) -> RedirectStats:
        """Return aggregate statistics."""
        with self._lock:
            by_type: dict = {}
            total_hits = 0
            top_hit: Optional[Redirect] = None
            unused_count = 0
            for r in self._redirects.values():
                key = r.redirect_type.value
                by_type[key] = by_type.get(key, 0) + 1
                total_hits += r.hit_count
                if r.hit_count == 0:
                    unused_count += 1
                if top_hit is None or r.hit_count > top_hit.hit_count:
                    top_hit = r
            if top_hit is not None and top_hit.hit_count == 0:
                top_hit = None
            return RedirectStats(
                total_redirects=len(self._redirects),
                by_type=by_type,
                total_hits=total_hits,
                top_hit=top_hit,
                unused_count=unused_count,
            )

    @property
    def total_redirects(self) -> int:
        """Number of redirects currently registered."""
        with self._lock:
            return len(self._redirects)

    def clear(self) -> None:
        """Drop all redirects."""
        with self._lock:
            self._redirects.clear()

    def find_terminals(self, source: str) -> str:
        """Walk the chain from ``source`` and return the last non-redirect (or last before loop)."""
        with self._lock:
            visited: set = set()
            current = source
            last = source
            depth = 0
            while depth < _MAX_DEPTH:
                if current in visited:
                    return last
                visited.add(current)
                redirect = self._redirects.get(current)
                if redirect is None:
                    return current
                last = redirect.target
                if redirect.redirect_type == RedirectType.GONE_410:
                    return last
                current = redirect.target
                depth += 1
            return last
