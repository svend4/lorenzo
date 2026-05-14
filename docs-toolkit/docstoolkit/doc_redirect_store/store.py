"""E351 DocRedirectStore — implementation."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Redirect:
    """A single redirect rule."""

    redirect_id: str
    from_path: str
    to_path: str
    code: int = 301
    created_at: float = 0.0
    hit_count: int = 0
    enabled: bool = True


@dataclass
class RedirectStats:
    """Aggregate statistics over the redirect store."""

    total_redirects: int
    enabled_redirects: int
    total_hits: int


class DocRedirectStore:
    """Thread-safe manager of document URL redirect rules."""

    def __init__(self) -> None:
        self._redirects: dict[str, Redirect] = {}
        self._by_from: dict[str, str] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ add
    def add(
        self,
        from_path: str,
        to_path: str,
        code: int = 301,
        now: Optional[float] = None,
    ) -> Redirect:
        """Create a redirect; replace any existing rule for ``from_path``."""
        ts = now if now is not None else time.time()
        with self._lock:
            existing_id = self._by_from.get(from_path)
            if existing_id is not None:
                # Replace: drop the existing redirect
                self._redirects.pop(existing_id, None)
            rid = str(uuid.uuid4())
            redirect = Redirect(
                redirect_id=rid,
                from_path=from_path,
                to_path=to_path,
                code=code,
                created_at=ts,
                hit_count=0,
                enabled=True,
            )
            self._redirects[rid] = redirect
            self._by_from[from_path] = rid
            return redirect

    # --------------------------------------------------------------- remove
    def remove(self, redirect_id: str) -> bool:
        """Remove by id. Returns True if it existed."""
        with self._lock:
            redirect = self._redirects.pop(redirect_id, None)
            if redirect is None:
                return False
            # Only clear by_from if it still points to this id
            if self._by_from.get(redirect.from_path) == redirect_id:
                self._by_from.pop(redirect.from_path, None)
            return True

    def remove_by_from(self, from_path: str) -> bool:
        """Remove by from_path. Returns True if it existed."""
        with self._lock:
            rid = self._by_from.pop(from_path, None)
            if rid is None:
                return False
            self._redirects.pop(rid, None)
            return True

    # --------------------------------------------------------- enable/disable
    def enable(self, redirect_id: str) -> bool:
        with self._lock:
            redirect = self._redirects.get(redirect_id)
            if redirect is None:
                return False
            redirect.enabled = True
            return True

    def disable(self, redirect_id: str) -> bool:
        with self._lock:
            redirect = self._redirects.get(redirect_id)
            if redirect is None:
                return False
            redirect.enabled = False
            return True

    # ------------------------------------------------------------------ get
    def get(self, redirect_id: str) -> Optional[Redirect]:
        with self._lock:
            return self._redirects.get(redirect_id)

    # ------------------------------------------------------------- resolve
    def resolve(self, from_path: str) -> Optional[str]:
        """Resolve a redirect, incrementing hit_count if enabled."""
        with self._lock:
            rid = self._by_from.get(from_path)
            if rid is None:
                return None
            redirect = self._redirects.get(rid)
            if redirect is None or not redirect.enabled:
                return None
            redirect.hit_count += 1
            return redirect.to_path

    def peek(self, from_path: str) -> Optional[Redirect]:
        """Look up redirect without modifying hit_count."""
        with self._lock:
            rid = self._by_from.get(from_path)
            if rid is None:
                return None
            return self._redirects.get(rid)

    # --------------------------------------------------------------- lists
    def list_redirects(self, enabled_only: bool = False) -> list[Redirect]:
        with self._lock:
            items = list(self._redirects.values())
        if enabled_only:
            items = [r for r in items if r.enabled]
        items.sort(key=lambda r: r.from_path)
        return items

    def top_hit_redirects(self, limit: int = 10) -> list[Redirect]:
        with self._lock:
            items = list(self._redirects.values())
        items.sort(key=lambda r: (-r.hit_count, r.from_path))
        if limit < 0:
            limit = 0
        return items[:limit]

    # ------------------------------------------------------- chain resolve
    def chain_resolve(
        self, from_path: str, max_hops: int = 10
    ) -> Optional[str]:
        """Follow chain of redirects up to ``max_hops``.

        Returns the final target path. Increments ``hit_count`` along the
        chain. Returns ``None`` if the first link does not resolve, or if
        a cycle is detected.
        """
        with self._lock:
            visited: set[str] = set()
            current = from_path
            hops = 0
            final_target: Optional[str] = None

            while hops < max_hops:
                rid = self._by_from.get(current)
                if rid is None:
                    break
                redirect = self._redirects.get(rid)
                if redirect is None or not redirect.enabled:
                    break
                if current in visited:
                    # Cycle detected
                    return None
                visited.add(current)
                redirect.hit_count += 1
                final_target = redirect.to_path
                # Check if we'd loop back on next hop
                if redirect.to_path in visited:
                    return None
                current = redirect.to_path
                hops += 1

            return final_target

    # ---------------------------------------------------------------- clear
    def clear(self) -> int:
        with self._lock:
            count = len(self._redirects)
            self._redirects.clear()
            self._by_from.clear()
            return count

    # ---------------------------------------------------------------- stats
    def stats(self) -> RedirectStats:
        with self._lock:
            items = list(self._redirects.values())
        total = len(items)
        enabled = sum(1 for r in items if r.enabled)
        hits = sum(r.hit_count for r in items)
        return RedirectStats(
            total_redirects=total,
            enabled_redirects=enabled,
            total_hits=hits,
        )
