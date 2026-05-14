"""E425 DocLinkAlias — alias mapping for document hyperlinks.

A purely in-memory implementation backed by simple ``dict`` indexes and
protected by a ``threading.Lock``.  No third-party dependencies.

Each alias is a short symbolic name (for example ``"docs"`` or
``"home"``) bound to a target URL.  The manager supports registration,
resolution (with hit counting), text expansion via a marker prefix and
basic introspection over the alias table.
"""
from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class LinkAliasEntry:
    """A single link alias entry."""

    alias: str
    target_url: str
    description: str = ""
    created_at: float = 0.0
    hit_count: int = 0


@dataclass
class AliasStats:
    """Aggregate statistics for the alias store."""

    total_aliases: int
    unique_targets: int
    total_hits: int


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


# Pattern fragment for valid alias characters (alphanumeric + underscore).
_ALIAS_CHARS = re.compile(r"[A-Za-z0-9_]+")


class DocLinkAlias:
    """Thread-safe in-memory store mapping symbolic aliases to URLs."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # alias -> LinkAliasEntry
        self._aliases: dict[str, LinkAliasEntry] = {}

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def register(
        self,
        alias: str,
        target_url: str,
        description: str = "",
        now: Optional[float] = None,
    ) -> LinkAliasEntry:
        """Register *alias* → *target_url*.

        If *alias* already exists, the existing entry is updated
        (``target_url`` and ``description`` are replaced) while preserving
        ``created_at`` and ``hit_count``.
        """
        if not isinstance(alias, str) or not alias:
            raise ValueError("alias must be a non-empty string")
        if not isinstance(target_url, str) or not target_url:
            raise ValueError("target_url must be a non-empty string")
        ts = time.time() if now is None else float(now)
        with self._lock:
            existing = self._aliases.get(alias)
            if existing is None:
                entry = LinkAliasEntry(
                    alias=alias,
                    target_url=target_url,
                    description=description,
                    created_at=ts,
                    hit_count=0,
                )
                self._aliases[alias] = entry
                return entry
            existing.target_url = target_url
            existing.description = description
            return existing

    def unregister(self, alias: str) -> bool:
        """Remove *alias* if it exists.  Returns ``True`` on success."""
        with self._lock:
            return self._aliases.pop(alias, None) is not None

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def resolve(self, alias: str) -> Optional[str]:
        """Return the target URL for *alias* and increment ``hit_count``."""
        with self._lock:
            entry = self._aliases.get(alias)
            if entry is None:
                return None
            entry.hit_count += 1
            return entry.target_url

    def peek(self, alias: str) -> Optional[LinkAliasEntry]:
        """Return the entry for *alias* without changing ``hit_count``."""
        with self._lock:
            return self._aliases.get(alias)

    # ------------------------------------------------------------------
    # Text expansion
    # ------------------------------------------------------------------

    def expand_text(self, text: str, marker: str = "@") -> str:
        """Replace ``marker`` + alias_name patterns in *text* with target URLs.

        Pattern: ``marker`` followed by one or more alphanumeric / ``_``
        characters.  Aliases that are not registered are left unchanged
        in the output.  Each successful resolution increments the
        corresponding ``hit_count``.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not isinstance(marker, str) or not marker:
            raise ValueError("marker must be a non-empty string")

        pattern = re.compile(re.escape(marker) + r"([A-Za-z0-9_]+)")

        def _sub(match: re.Match[str]) -> str:
            name = match.group(1)
            entry = self._aliases.get(name)
            if entry is None:
                return match.group(0)
            entry.hit_count += 1
            return entry.target_url

        with self._lock:
            return pattern.sub(_sub, text)

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def update_target(self, alias: str, new_target: str) -> bool:
        """Change the target URL of an existing alias."""
        if not isinstance(new_target, str) or not new_target:
            raise ValueError("new_target must be a non-empty string")
        with self._lock:
            entry = self._aliases.get(alias)
            if entry is None:
                return False
            entry.target_url = new_target
            return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def aliases_for_target(self, target_url: str) -> list[str]:
        """Return all aliases that resolve to *target_url* (sorted)."""
        with self._lock:
            return sorted(
                a for a, e in self._aliases.items() if e.target_url == target_url
            )

    def list_aliases(self) -> list[LinkAliasEntry]:
        """Return all entries sorted by alias name."""
        with self._lock:
            return sorted(self._aliases.values(), key=lambda e: e.alias)

    def top_used(self, limit: int = 10) -> list[LinkAliasEntry]:
        """Return the *limit* most-used aliases.

        Sorted by ``hit_count`` descending then by ``alias`` ascending.
        """
        if limit < 0:
            raise ValueError("limit must be non-negative")
        with self._lock:
            entries = list(self._aliases.values())
        entries.sort(key=lambda e: (-e.hit_count, e.alias))
        return entries[:limit]

    def unused_aliases(self) -> list[str]:
        """Return aliases that have never been resolved (sorted)."""
        with self._lock:
            return sorted(a for a, e in self._aliases.items() if e.hit_count == 0)

    # ------------------------------------------------------------------
    # Maintenance / stats
    # ------------------------------------------------------------------

    def clear(self) -> int:
        """Drop every alias.  Returns the number of removed entries."""
        with self._lock:
            n = len(self._aliases)
            self._aliases.clear()
            return n

    def stats(self) -> AliasStats:
        """Return aggregate statistics about the alias store."""
        with self._lock:
            total = len(self._aliases)
            unique_targets = len({e.target_url for e in self._aliases.values()})
            total_hits = sum(e.hit_count for e in self._aliases.values())
        return AliasStats(
            total_aliases=total,
            unique_targets=unique_targets,
            total_hits=total_hits,
        )

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        with self._lock:
            return len(self._aliases)

    def __contains__(self, alias: object) -> bool:
        if not isinstance(alias, str):
            return False
        with self._lock:
            return alias in self._aliases
