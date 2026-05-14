"""Ranked scoreboard with add/update/query/top-N operations.

Stdlib only (``threading`` for safety, ``dataclasses`` for records).
Each query recomputes the sorted view from the underlying dict so the
implementation stays simple and predictable.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Entry:
    """A single leaderboard record."""

    entity_id: str
    score: float
    metadata: dict = field(default_factory=dict)
    updated_at: float = 0.0


@dataclass
class RankInfo:
    """Information about an entity's position on the board."""

    entity_id: str
    score: float
    rank: int  # 1-based
    percentile: float  # 0..100


class Leaderboard:
    """A simple in-memory ranked scoreboard.

    Parameters
    ----------
    higher_is_better:
        When True (default), higher scores rank first.  When False,
        lower scores rank first (useful for things like latency).

    Ties are broken alphabetically by ``entity_id``.
    """

    def __init__(self, higher_is_better: bool = True):
        self.higher_is_better = bool(higher_is_better)
        self._entries: Dict[str, Entry] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _sort_key(self, entry: Entry):
        # Primary key: score (inverted when higher_is_better)
        # Secondary key: entity_id alphabetically (stable tiebreaker)
        if self.higher_is_better:
            return (-entry.score, entry.entity_id)
        return (entry.score, entry.entity_id)

    def _sorted_entries(self) -> List[Entry]:
        return sorted(self._entries.values(), key=self._sort_key)

    # ------------------------------------------------------------------ #
    # Mutations
    # ------------------------------------------------------------------ #
    def add(
        self,
        entity_id: str,
        score: float,
        metadata: Optional[dict] = None,
        now: float = 0.0,
    ) -> Entry:
        """Add or replace an entry with the given ``entity_id``."""
        if not isinstance(entity_id, str):
            raise TypeError("entity_id must be a str")
        with self._lock:
            entry = Entry(
                entity_id=entity_id,
                score=float(score),
                metadata=dict(metadata) if metadata else {},
                updated_at=float(now),
            )
            self._entries[entity_id] = entry
            return entry

    def update(
        self, entity_id: str, score: float, now: float = 0.0
    ) -> Optional[Entry]:
        """Update the score of an existing entry.  Returns None if absent."""
        with self._lock:
            existing = self._entries.get(entity_id)
            if existing is None:
                return None
            existing.score = float(score)
            existing.updated_at = float(now)
            return existing

    def increment(
        self, entity_id: str, delta: float, now: float = 0.0
    ) -> Optional[Entry]:
        """Add ``delta`` to the entry's score.  Returns None if absent."""
        with self._lock:
            existing = self._entries.get(entity_id)
            if existing is None:
                return None
            existing.score = float(existing.score) + float(delta)
            existing.updated_at = float(now)
            return existing

    def remove(self, entity_id: str) -> bool:
        """Remove an entry.  Returns True if it existed."""
        with self._lock:
            return self._entries.pop(entity_id, None) is not None

    def clear(self) -> None:
        """Drop every entry."""
        with self._lock:
            self._entries.clear()

    # ------------------------------------------------------------------ #
    # Reads
    # ------------------------------------------------------------------ #
    def get(self, entity_id: str) -> Optional[Entry]:
        """Return the entry, or None if missing."""
        with self._lock:
            return self._entries.get(entity_id)

    def rank_of(self, entity_id: str) -> Optional[int]:
        """Return the 1-based rank, or None if entity is unknown."""
        with self._lock:
            if entity_id not in self._entries:
                return None
            for idx, entry in enumerate(self._sorted_entries(), start=1):
                if entry.entity_id == entity_id:
                    return idx
            return None  # pragma: no cover - defensive

    def rank_info(self, entity_id: str) -> Optional[RankInfo]:
        """Return rank and percentile (0..100) for ``entity_id``."""
        with self._lock:
            if entity_id not in self._entries:
                return None
            sorted_entries = self._sorted_entries()
            total = len(sorted_entries)
            for idx, entry in enumerate(sorted_entries, start=1):
                if entry.entity_id == entity_id:
                    if total <= 1:
                        percentile = 100.0
                    else:
                        # Top entry → 100, bottom → 0
                        percentile = (total - idx) / (total - 1) * 100.0
                    return RankInfo(
                        entity_id=entity_id,
                        score=entry.score,
                        rank=idx,
                        percentile=percentile,
                    )
            return None  # pragma: no cover - defensive

    def top_n(self, n: int) -> List[Entry]:
        """Return the top ``n`` entries.  Empty list when ``n <= 0``."""
        if n <= 0:
            return []
        with self._lock:
            return self._sorted_entries()[:n]

    def bottom_n(self, n: int) -> List[Entry]:
        """Return the bottom ``n`` entries.  Order: worst first."""
        if n <= 0:
            return []
        with self._lock:
            sorted_entries = self._sorted_entries()
            if not sorted_entries:
                return []
            tail = sorted_entries[-n:]
            return list(reversed(tail))

    def range(self, start: int, end: int) -> List[Entry]:
        """1-based inclusive slice of the ranked list."""
        with self._lock:
            sorted_entries = self._sorted_entries()
            if start < 1:
                start = 1
            if end < start:
                return []
            return sorted_entries[start - 1 : end]

    def around(self, entity_id: str, window: int) -> List[Entry]:
        """Return ``2*window + 1`` entries centred on ``entity_id``.

        Bounds are clipped to the list.  Empty list when entity is unknown
        or ``window < 0``.
        """
        if window < 0:
            return []
        with self._lock:
            if entity_id not in self._entries:
                return []
            sorted_entries = self._sorted_entries()
            for idx, entry in enumerate(sorted_entries):
                if entry.entity_id == entity_id:
                    lo = max(0, idx - window)
                    hi = min(len(sorted_entries), idx + window + 1)
                    return sorted_entries[lo:hi]
            return []  # pragma: no cover - defensive

    def score_at_rank(self, rank: int) -> Optional[float]:
        """Return the score at the given 1-based rank, or None."""
        if rank < 1:
            return None
        with self._lock:
            sorted_entries = self._sorted_entries()
            if rank > len(sorted_entries):
                return None
            return sorted_entries[rank - 1].score

    def entries_with_score(self, score: float) -> List[Entry]:
        """All entries whose score equals ``score``."""
        target = float(score)
        with self._lock:
            return [
                entry
                for entry in self._sorted_entries()
                if entry.score == target
            ]

    def all_entries(self) -> List[Entry]:
        """Every entry in ranked order."""
        with self._lock:
            return self._sorted_entries()

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #
    @property
    def count(self) -> int:
        with self._lock:
            return len(self._entries)

    def __len__(self) -> int:  # convenience
        return self.count

    def __contains__(self, entity_id: object) -> bool:
        with self._lock:
            return entity_id in self._entries
