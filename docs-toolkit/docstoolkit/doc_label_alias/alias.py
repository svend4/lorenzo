"""E428 DocLabelAlias — alias mapping for document labels.

A purely in-memory implementation backed by a single ``dict`` index
and protected by a ``threading.Lock``.  No third-party dependencies.

Each alias maps a short variant label (for example ``"py"``) to its
canonical form (``"python"``).  The manager supports registration,
resolution (returning the canonical name or the input unchanged) and
batch helpers that resolve and deduplicate lists of labels.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class LabelAliasEntry:
    """A single label alias entry."""

    alias: str
    canonical: str
    created_at: float = 0.0
    description: str = ""


@dataclass
class AliasStats:
    """Aggregate statistics for the alias store."""

    total_aliases: int
    unique_canonicals: int


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


class DocLabelAlias:
    """Thread-safe in-memory store mapping label aliases to canonical labels."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # alias -> LabelAliasEntry
        self._aliases: dict[str, LabelAliasEntry] = {}

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def register(
        self,
        alias: str,
        canonical: str,
        description: str = "",
        now: Optional[float] = None,
    ) -> LabelAliasEntry:
        """Register *alias* → *canonical*.

        If *alias* already exists, the existing entry is updated
        (``canonical`` and ``description`` replaced) while preserving
        ``created_at``.
        """
        if not isinstance(alias, str) or not alias:
            raise ValueError("alias must be a non-empty string")
        if not isinstance(canonical, str) or not canonical:
            raise ValueError("canonical must be a non-empty string")
        ts = time.time() if now is None else float(now)
        with self._lock:
            existing = self._aliases.get(alias)
            if existing is None:
                entry = LabelAliasEntry(
                    alias=alias,
                    canonical=canonical,
                    created_at=ts,
                    description=description,
                )
                self._aliases[alias] = entry
                return entry
            existing.canonical = canonical
            existing.description = description
            return existing

    def unregister(self, alias: str) -> bool:
        """Remove *alias* if it exists.  Returns ``True`` on success."""
        with self._lock:
            return self._aliases.pop(alias, None) is not None

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def resolve(self, label: str) -> str:
        """Return the canonical label for *label*.

        If *label* is a registered alias, its ``canonical`` value is
        returned; otherwise *label* itself is returned unchanged.
        """
        with self._lock:
            entry = self._aliases.get(label)
            if entry is None:
                return label
            return entry.canonical

    def resolve_list(self, labels: list[str]) -> list[str]:
        """Resolve every label in *labels*, dedupe and sort the result."""
        with self._lock:
            seen: set[str] = set()
            for label in labels:
                entry = self._aliases.get(label)
                seen.add(entry.canonical if entry is not None else label)
        return sorted(seen)

    def get_alias(self, alias: str) -> Optional[LabelAliasEntry]:
        """Return the entry for *alias* or ``None`` if missing."""
        with self._lock:
            return self._aliases.get(alias)

    def aliases_for_canonical(self, canonical: str) -> list[str]:
        """Return all aliases pointing to *canonical* (sorted)."""
        with self._lock:
            return sorted(
                a for a, e in self._aliases.items() if e.canonical == canonical
            )

    def list_aliases(self) -> list[LabelAliasEntry]:
        """Return all entries sorted by alias name."""
        with self._lock:
            return sorted(self._aliases.values(), key=lambda e: e.alias)

    def canonicals(self) -> list[str]:
        """Return sorted unique canonical labels."""
        with self._lock:
            return sorted({e.canonical for e in self._aliases.values()})

    # ------------------------------------------------------------------
    # Batch helpers
    # ------------------------------------------------------------------

    def merge_labels(self, input_labels: list[str]) -> list[str]:
        """Resolve every label, deduplicate via set, return sorted list."""
        with self._lock:
            merged: set[str] = set()
            for label in input_labels:
                entry = self._aliases.get(label)
                merged.add(entry.canonical if entry is not None else label)
        return sorted(merged)

    def bulk_register(self, mappings: dict) -> int:
        """Register many ``alias -> canonical`` pairs from *mappings*.

        Returns the number of (re-)registered entries.
        """
        if not isinstance(mappings, dict):
            raise TypeError("mappings must be a dict")
        count = 0
        ts = time.time()
        with self._lock:
            for alias, canonical in mappings.items():
                if not isinstance(alias, str) or not alias:
                    raise ValueError("alias must be a non-empty string")
                if not isinstance(canonical, str) or not canonical:
                    raise ValueError("canonical must be a non-empty string")
                existing = self._aliases.get(alias)
                if existing is None:
                    self._aliases[alias] = LabelAliasEntry(
                        alias=alias,
                        canonical=canonical,
                        created_at=ts,
                        description="",
                    )
                else:
                    existing.canonical = canonical
                count += 1
        return count

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
            unique = len({e.canonical for e in self._aliases.values()})
        return AliasStats(total_aliases=total, unique_canonicals=unique)

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
