"""MemGPT-grade promotion policy: episodic → semantic memory.

A fact from :class:`~docstoolkit.memory.episodic.EpisodicMemory` graduates
to :class:`~docstoolkit.memory.semantic.SemanticMemory` when the promotion
policy decides it is worth keeping permanently.

Default rules (all configurable):
1. Mention count ≥ ``promotion_threshold`` (default 3).
2. Token length ≥ ``min_tokens`` (filter noise).
3. The fact must not already exist in semantic memory above
   ``dedup_threshold`` similarity.

Optional LLM-judge integration: if ``judge_fn`` is provided it is called
with ``(content) → float`` and the score is used as the initial
``importance_score`` in semantic memory.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

from docstoolkit.memory.episodic import EpisodicEvent, EpisodicMemory, _token_jaccard
from docstoolkit.memory.semantic import SemanticFact, SemanticMemory


# ---------------------------------------------------------------------------
# PromotionConfig
# ---------------------------------------------------------------------------

@dataclass
class PromotionConfig:
    """Tuning knobs for the promotion policy."""
    mention_threshold: int = 3
    min_tokens: int = 3                  # filter very short fragments
    dedup_threshold: float = 0.80        # similarity above which we skip promotion
    default_importance: float = 0.60     # base importance for promoted facts
    importance_boost_per_mention: float = 0.05   # each extra mention adds this


# ---------------------------------------------------------------------------
# PromotionResult
# ---------------------------------------------------------------------------

@dataclass
class PromotionResult:
    """Summary of a promotion pass."""
    promoted: List[str]           # fact_ids of newly promoted facts
    skipped_dedup: List[str]      # event_ids skipped because already in semantic
    skipped_threshold: List[str]  # event_ids below mention threshold
    skipped_too_short: List[str]  # event_ids with too few tokens

    @property
    def total_promoted(self) -> int:
        return len(self.promoted)

    @property
    def total_skipped(self) -> int:
        return len(self.skipped_dedup) + len(self.skipped_threshold) + len(self.skipped_too_short)


# ---------------------------------------------------------------------------
# PromotionPolicy
# ---------------------------------------------------------------------------

JudgeFn = Callable[[str], float]   # content → importance score [0,1]


class PromotionPolicy:
    """Drives the episodic → semantic promotion cycle.

    Usage::

        policy = PromotionPolicy(episodic, semantic)
        result = policy.run()
        print(f"Promoted {result.total_promoted} facts")

    The policy is designed to be run on a schedule (e.g. daily CI job) or
    after a conversation session ends.
    """

    def __init__(
        self,
        episodic: EpisodicMemory,
        semantic: SemanticMemory,
        config: Optional[PromotionConfig] = None,
        judge_fn: Optional[JudgeFn] = None,
    ) -> None:
        self._episodic = episodic
        self._semantic = semantic
        self._cfg = config or PromotionConfig()
        self._judge_fn = judge_fn

    def run(self) -> PromotionResult:
        """Promote all eligible episodic events to semantic memory.

        Episodic events that are promoted are NOT removed from episodic
        memory (they continue to age out naturally via TTL).
        """
        result = PromotionResult(
            promoted=[], skipped_dedup=[], skipped_threshold=[], skipped_too_short=[]
        )

        candidates = self._episodic.promotion_candidates()

        for event in candidates:
            if event.mention_count < self._cfg.mention_threshold:
                result.skipped_threshold.append(event.event_id)
                continue

            tokens = event.content.split()
            if len(tokens) < self._cfg.min_tokens:
                result.skipped_too_short.append(event.event_id)
                continue

            # Check near-duplicate in semantic
            if self._is_duplicate_in_semantic(event.content):
                # Reinforce the existing fact instead
                self._reinforce_existing(event.content)
                result.skipped_dedup.append(event.event_id)
                continue

            importance = self._compute_importance(event)
            fact = self._semantic.add(
                content=event.content,
                importance_score=importance,
                source_session=event.session_id,
                tags=event.tags,
            )
            result.promoted.append(fact.fact_id)

        return result

    def _is_duplicate_in_semantic(self, content: str) -> bool:
        for fact in self._semantic.all_facts():
            if _token_jaccard(fact.content, content) >= self._cfg.dedup_threshold:
                return True
        return False

    def _reinforce_existing(self, content: str) -> None:
        for fact in self._semantic.all_facts():
            if _token_jaccard(fact.content, content) >= self._cfg.dedup_threshold:
                fact.reinforce(self._cfg.importance_boost_per_mention)
                return

    def _compute_importance(self, event: EpisodicEvent) -> float:
        if self._judge_fn is not None:
            try:
                score = float(self._judge_fn(event.content))
                return max(0.0, min(1.0, score))
            except Exception:
                pass

        # Heuristic: base + boost per extra mention beyond threshold
        extra_mentions = max(0, event.mention_count - self._cfg.mention_threshold)
        importance = self._cfg.default_importance + extra_mentions * self._cfg.importance_boost_per_mention
        return min(1.0, importance)


# ---------------------------------------------------------------------------
# Convenience: TieredMemoryStore
# ---------------------------------------------------------------------------

class TieredMemoryStore:
    """Unified API combining episodic + semantic memory with auto-promotion.

    This is the high-level entry point for MemGPT-grade memory management.

    Parameters
    ----------
    episodic_max_events:
        Max events in episodic tier.
    episodic_max_age_hours:
        Age limit for episodic events.
    semantic_max_facts:
        Max facts in semantic tier.
    promotion_config:
        Optional :class:`PromotionConfig` override.
    auto_promote:
        If True, promotion runs automatically on every ``add()`` call.
    """

    def __init__(
        self,
        episodic_max_events: int = 200,
        episodic_max_age_hours: float = 24 * 7,
        semantic_max_facts: int = 1000,
        promotion_config: Optional[PromotionConfig] = None,
        auto_promote: bool = False,
    ) -> None:
        self.episodic = EpisodicMemory(
            max_events=episodic_max_events,
            max_age_hours=episodic_max_age_hours,
            promotion_threshold=(promotion_config or PromotionConfig()).mention_threshold,
        )
        self.semantic = SemanticMemory(max_facts=semantic_max_facts)
        self._policy = PromotionPolicy(
            self.episodic, self.semantic, config=promotion_config
        )
        self._auto_promote = auto_promote

    def add(self, content: str, session_id: Optional[str] = None, tags: Optional[List[str]] = None) -> EpisodicEvent:
        """Add an event to episodic memory (and optionally run promotion)."""
        event = self.episodic.add(content, session_id=session_id, tags=tags)
        if self._auto_promote:
            self._policy.run()
        return event

    def promote(self) -> PromotionResult:
        """Manually trigger a promotion pass."""
        return self._policy.run()

    def recall(self, query: str, top_k: int = 10) -> dict:
        """Search both memory tiers and return combined results."""
        episodic = self.episodic.search(query, top_k=top_k)
        semantic = self.semantic.search(query, top_k=top_k)
        return {
            "episodic": [e.to_dict() for e in episodic],
            "semantic": [f.to_dict() for f in semantic],
        }

    def to_context(self, episodic_k: int = 3, semantic_k: int = 5) -> str:
        """Format both tiers as a single LLM-ready context string."""
        parts = []
        sem_ctx = self.semantic.to_context(top_k=semantic_k)
        if sem_ctx:
            parts.append("## Known facts\n" + sem_ctx)
        ep_ctx = self.episodic.to_context(top_k=episodic_k)
        if ep_ctx:
            parts.append("## Recent events\n" + ep_ctx)
        return "\n\n".join(parts)

    def stats(self) -> dict:
        return {
            "episodic": self.episodic.stats(),
            "semantic": self.semantic.stats(),
        }
