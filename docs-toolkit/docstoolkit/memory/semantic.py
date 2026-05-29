"""Semantic memory tier — consolidated long-term facts.

Semantic memory stores *what is known* as extracted, deduplicated facts.
Unlike episodic memory it has no age limit; facts persist until explicitly
demoted or deleted.  A fact's ``importance_score`` drives recall ranking.

Promotion from episodic memory is handled by
:class:`~docstoolkit.memory.promotion.PromotionPolicy`.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Fact
# ---------------------------------------------------------------------------

@dataclass
class SemanticFact:
    """A consolidated long-term fact in semantic memory."""
    fact_id: str
    content: str
    importance_score: float = 0.5   # [0,1] — higher = recalled first
    mention_count: int = 1          # how many times this fact was reinforced
    created_ts: str = field(default_factory=_now_iso)
    updated_ts: str = field(default_factory=_now_iso)
    source_session: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        content: str,
        importance_score: float = 0.5,
        source_session: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> "SemanticFact":
        return cls(
            fact_id=uuid.uuid4().hex[:16],
            content=content,
            importance_score=max(0.0, min(1.0, importance_score)),
            source_session=source_session,
            tags=tags or [],
        )

    def reinforce(self, delta: float = 0.05) -> None:
        """Increase importance and record another mention."""
        self.mention_count += 1
        self.importance_score = min(1.0, self.importance_score + delta)
        self.updated_ts = _now_iso()

    def decay(self, delta: float = 0.02) -> None:
        """Slightly lower importance (ageing / recency penalty)."""
        self.importance_score = max(0.0, self.importance_score - delta)
        self.updated_ts = _now_iso()

    def to_dict(self) -> dict:
        return {
            "fact_id": self.fact_id,
            "content": self.content,
            "importance_score": self.importance_score,
            "mention_count": self.mention_count,
            "created_ts": self.created_ts,
            "updated_ts": self.updated_ts,
            "source_session": self.source_session,
            "tags": self.tags,
        }


# ---------------------------------------------------------------------------
# Semantic memory store
# ---------------------------------------------------------------------------

def _token_jaccard(a: str, b: str) -> float:
    ta = set(a.lower().split())
    tb = set(b.lower().split())
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


class SemanticMemory:
    """Long-term semantic fact store.

    Parameters
    ----------
    max_facts:
        Upper bound on stored facts.  When exceeded the lowest-importance
        facts are evicted.
    dedup_threshold:
        Jaccard similarity above which a new fact is considered a duplicate
        of an existing one (triggering ``reinforce()`` instead of insert).
    """

    def __init__(
        self,
        max_facts: int = 1000,
        dedup_threshold: float = 0.80,
    ) -> None:
        self._max_facts = max_facts
        self._dedup_threshold = dedup_threshold
        self._facts: dict[str, SemanticFact] = {}

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def add(
        self,
        content: str,
        importance_score: float = 0.5,
        source_session: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> SemanticFact:
        """Add a new fact or reinforce an existing near-duplicate."""
        for fact in self._facts.values():
            if _token_jaccard(fact.content, content) >= self._dedup_threshold:
                fact.reinforce()
                return fact

        fact = SemanticFact.create(
            content,
            importance_score=importance_score,
            source_session=source_session,
            tags=tags,
        )
        self._facts[fact.fact_id] = fact

        # Evict least important if over capacity
        if len(self._facts) > self._max_facts:
            lowest = min(self._facts.values(), key=lambda f: f.importance_score)
            del self._facts[lowest.fact_id]

        return fact

    def remove(self, fact_id: str) -> bool:
        """Remove a fact by ID. Returns True if found."""
        if fact_id in self._facts:
            del self._facts[fact_id]
            return True
        return False

    def reinforce(self, fact_id: str, delta: float = 0.05) -> bool:
        """Boost importance of an existing fact."""
        if fact_id in self._facts:
            self._facts[fact_id].reinforce(delta)
            return True
        return False

    def decay_all(self, delta: float = 0.01) -> None:
        """Apply a uniform importance decay to all facts."""
        for fact in self._facts.values():
            fact.decay(delta)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def search(self, query: str, top_k: int = 10) -> List[SemanticFact]:
        """Return up to *top_k* facts most relevant to *query*.

        Ranking = 0.7 × token_jaccard + 0.3 × importance_score
        """
        scored = [
            (0.7 * _token_jaccard(query, f.content) + 0.3 * f.importance_score, f)
            for f in self._facts.values()
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [f for _, f in scored[:top_k]]

    def get(self, fact_id: str) -> Optional[SemanticFact]:
        return self._facts.get(fact_id)

    def all_facts(self) -> List[SemanticFact]:
        """Return all facts sorted by descending importance."""
        return sorted(self._facts.values(), key=lambda f: f.importance_score, reverse=True)

    def clear(self) -> None:
        self._facts.clear()

    def stats(self) -> dict:
        facts = list(self._facts.values())
        avg_importance = sum(f.importance_score for f in facts) / len(facts) if facts else 0.0
        return {
            "n_facts": len(facts),
            "max_facts": self._max_facts,
            "avg_importance": avg_importance,
            "high_importance_facts": sum(1 for f in facts if f.importance_score >= 0.7),
        }

    def to_context(self, top_k: int = 10) -> str:
        """Format top facts as a single string for LLM context."""
        top = self.all_facts()[:top_k]
        return "\n".join(f"• {f.content} (importance={f.importance_score:.2f})" for f in top)
