"""Episodic memory tier — raw time-stamped events with FIFO eviction.

Episodic memory stores *what happened* in temporal order.  Events older than
``max_age_hours`` or beyond the ``max_events`` capacity are evicted.

Facts that are re-mentioned ``promotion_threshold`` times graduate to
:mod:`semantic memory <docstoolkit.memory.semantic>` via the promotion policy.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import json
import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Iterator, List, Optional


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _now_iso() -> str:
    return _now().isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Event
# ---------------------------------------------------------------------------

@dataclass
class EpisodicEvent:
    """A single time-stamped memory event."""
    event_id: str
    content: str                    # free-text description of what happened
    timestamp: str                  # ISO 8601 UTC
    session_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    mention_count: int = 1          # incremented when same content re-appears

    @classmethod
    def create(
        cls,
        content: str,
        session_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> "EpisodicEvent":
        return cls(
            event_id=uuid.uuid4().hex[:16],
            content=content,
            timestamp=_now_iso(),
            session_id=session_id,
            tags=tags or [],
        )

    def age_hours(self) -> float:
        """Return how many hours ago this event occurred."""
        try:
            ts = datetime.fromisoformat(self.timestamp)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            return (_now() - ts).total_seconds() / 3600
        except Exception:
            return 0.0

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "session_id": self.session_id,
            "tags": self.tags,
            "mention_count": self.mention_count,
        }


# ---------------------------------------------------------------------------
# Episodic store
# ---------------------------------------------------------------------------

class EpisodicMemory:
    """Time-bounded FIFO episodic store with promotion tracking.

    Parameters
    ----------
    max_events:
        Hard upper bound on stored events.  Oldest are evicted first.
    max_age_hours:
        Events older than this are automatically evicted on each ``add()``
        or ``evict_stale()`` call.
    promotion_threshold:
        Number of times a fact must be re-mentioned before it becomes a
        promotion candidate (retrieved via ``promotion_candidates()``).
    similarity_fn:
        Optional callable ``(a, b) -> float`` returning a [0,1] similarity
        score for deduplication.  Defaults to token-Jaccard similarity.
    """

    def __init__(
        self,
        max_events: int = 200,
        max_age_hours: float = 24 * 7,   # 7 days default
        promotion_threshold: int = 3,
        similarity_fn=None,
    ) -> None:
        self._max_events = max_events
        self._max_age_hours = max_age_hours
        self._promo_threshold = promotion_threshold
        self._sim_fn = similarity_fn or _token_jaccard
        self._events: List[EpisodicEvent] = []

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def add(self, content: str, session_id: Optional[str] = None, tags: Optional[List[str]] = None) -> EpisodicEvent:
        """Add an event (or increment an existing near-duplicate)."""
        self._evict_stale()

        # Check for near-duplicate
        for ev in self._events:
            if self._sim_fn(ev.content, content) >= 0.85:
                ev.mention_count += 1
                ev.timestamp = _now_iso()   # refresh timestamp
                return ev

        event = EpisodicEvent.create(content, session_id=session_id, tags=tags)
        self._events.append(event)

        # Evict oldest if over capacity
        while len(self._events) > self._max_events:
            self._events.pop(0)

        return event

    def search(self, query: str, top_k: int = 10) -> List[EpisodicEvent]:
        """Return up to *top_k* events most relevant to *query*."""
        scored = [(self._sim_fn(query, e.content), e) for e in self._events]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored[:top_k]]

    def promotion_candidates(self) -> List[EpisodicEvent]:
        """Return events that have been mentioned enough times to promote."""
        return [e for e in self._events if e.mention_count >= self._promo_threshold]

    def evict_stale(self) -> int:
        """Remove events older than *max_age_hours*. Returns count evicted."""
        return self._evict_stale()

    def _evict_stale(self) -> int:
        before = len(self._events)
        self._events = [e for e in self._events if e.age_hours() < self._max_age_hours]
        return before - len(self._events)

    def all_events(self) -> List[EpisodicEvent]:
        """Return all stored events, oldest first."""
        return list(self._events)

    def clear(self) -> None:
        self._events.clear()

    def stats(self) -> dict:
        return {
            "n_events": len(self._events),
            "max_events": self._max_events,
            "max_age_hours": self._max_age_hours,
            "promotion_threshold": self._promo_threshold,
            "promotion_candidates": len(self.promotion_candidates()),
        }

    def to_context(self, top_k: int = 5) -> str:
        """Format recent events as a single string for LLM context."""
        recent = sorted(self._events, key=lambda e: e.timestamp, reverse=True)[:top_k]
        lines = []
        for e in reversed(recent):
            lines.append(f"[{e.timestamp}] {e.content}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Similarity helper
# ---------------------------------------------------------------------------

def _token_jaccard(a: str, b: str) -> float:
    """Simple token-level Jaccard similarity."""
    ta = set(a.lower().split())
    tb = set(b.lower().split())
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / union
