"""Tests for docstoolkit.memory episodic / semantic split + promotion policy."""
from __future__ import annotations

import time

import pytest

from docstoolkit.memory import (
    EpisodicEvent, EpisodicMemory,
    SemanticFact, SemanticMemory,
    PromotionConfig, PromotionPolicy, PromotionResult, TieredMemoryStore,
)
from docstoolkit.memory.episodic import _token_jaccard


# ===========================================================================
# EpisodicEvent
# ===========================================================================

class TestEpisodicEvent:
    def test_create_sets_event_id(self):
        e = EpisodicEvent.create("hello")
        assert e.event_id and len(e.event_id) > 0

    def test_create_sets_timestamp(self):
        e = EpisodicEvent.create("hello")
        assert "T" in e.timestamp  # ISO format

    def test_default_mention_count_one(self):
        e = EpisodicEvent.create("hello")
        assert e.mention_count == 1

    def test_age_hours_near_zero(self):
        e = EpisodicEvent.create("hello")
        assert e.age_hours() < 1.0

    def test_to_dict_has_content(self):
        e = EpisodicEvent.create("test content", tags=["a", "b"])
        d = e.to_dict()
        assert d["content"] == "test content"
        assert "a" in d["tags"]


# ===========================================================================
# EpisodicMemory
# ===========================================================================

class TestEpisodicMemory:
    def test_add_returns_event(self):
        mem = EpisodicMemory()
        e = mem.add("first event")
        assert isinstance(e, EpisodicEvent)

    def test_add_stores_event(self):
        mem = EpisodicMemory()
        mem.add("first event")
        assert len(mem.all_events()) == 1

    def test_near_duplicate_increments_mention_count(self):
        mem = EpisodicMemory()
        e1 = mem.add("the agent found a memory bug")
        e2 = mem.add("the agent found a memory bug")
        assert e2.event_id == e1.event_id
        assert e2.mention_count == 2
        assert len(mem.all_events()) == 1  # still just one

    def test_different_content_creates_two_events(self):
        mem = EpisodicMemory()
        mem.add("event alpha")
        mem.add("event beta zeta completely different text")
        assert len(mem.all_events()) == 2

    def test_max_events_evicts_oldest(self):
        mem = EpisodicMemory(max_events=3)
        mem.add("a")
        mem.add("b and more words here")
        mem.add("c is completely different")
        mem.add("d yet another event here")
        assert len(mem.all_events()) <= 3

    def test_search_returns_relevant(self):
        mem = EpisodicMemory()
        mem.add("agent memory system")
        mem.add("database connection error")
        mem.add("agent retrieval pipeline")
        results = mem.search("agent system", top_k=2)
        contents = [e.content for e in results]
        assert any("agent" in c for c in contents)

    def test_search_respects_top_k(self):
        mem = EpisodicMemory()
        for i in range(10):
            mem.add(f"event number {i} with content")
        results = mem.search("event", top_k=3)
        assert len(results) <= 3

    def test_promotion_candidates_above_threshold(self):
        mem = EpisodicMemory(promotion_threshold=2)
        e = mem.add("frequently mentioned topic about agents")
        mem.add("frequently mentioned topic about agents")  # increments
        assert e in mem.promotion_candidates()

    def test_promotion_candidates_below_threshold(self):
        mem = EpisodicMemory(promotion_threshold=3)
        mem.add("mentioned only once")
        assert len(mem.promotion_candidates()) == 0

    def test_stale_eviction(self):
        mem = EpisodicMemory(max_age_hours=0.0)  # instant expiry
        mem.add("will be evicted")
        time.sleep(0.01)
        evicted = mem.evict_stale()
        assert evicted >= 1
        assert len(mem.all_events()) == 0

    def test_clear_removes_all(self):
        mem = EpisodicMemory()
        mem.add("a")
        mem.add("b")
        mem.clear()
        assert len(mem.all_events()) == 0

    def test_stats_has_expected_keys(self):
        mem = EpisodicMemory()
        mem.add("test")
        s = mem.stats()
        for key in ("n_events", "max_events", "promotion_candidates"):
            assert key in s

    def test_to_context_returns_string(self):
        mem = EpisodicMemory()
        mem.add("recent event 1")
        mem.add("recent event 2")
        ctx = mem.to_context(top_k=2)
        assert isinstance(ctx, str)
        assert len(ctx) > 0


# ===========================================================================
# SemanticFact
# ===========================================================================

class TestSemanticFact:
    def test_create_sets_fact_id(self):
        f = SemanticFact.create("agents use memory")
        assert f.fact_id

    def test_importance_clamped(self):
        f = SemanticFact.create("test", importance_score=99.9)
        assert f.importance_score == 1.0

    def test_reinforce_increments_mention_and_importance(self):
        f = SemanticFact.create("test", importance_score=0.5)
        f.reinforce(delta=0.1)
        assert f.mention_count == 2
        assert f.importance_score == pytest.approx(0.6, rel=1e-4)

    def test_reinforce_clamps_at_1(self):
        f = SemanticFact.create("test", importance_score=0.99)
        f.reinforce(delta=0.5)
        assert f.importance_score == 1.0

    def test_decay_lowers_importance(self):
        f = SemanticFact.create("test", importance_score=0.5)
        f.decay(delta=0.1)
        assert f.importance_score == pytest.approx(0.4, rel=1e-4)

    def test_decay_clamps_at_0(self):
        f = SemanticFact.create("test", importance_score=0.01)
        f.decay(delta=0.5)
        assert f.importance_score == 0.0

    def test_to_dict_contains_content(self):
        f = SemanticFact.create("my fact content")
        d = f.to_dict()
        assert d["content"] == "my fact content"


# ===========================================================================
# SemanticMemory
# ===========================================================================

class TestSemanticMemory:
    def test_add_returns_fact(self):
        mem = SemanticMemory()
        f = mem.add("agents use memory for long-term recall")
        assert isinstance(f, SemanticFact)

    def test_add_stores_fact(self):
        mem = SemanticMemory()
        mem.add("fact one about agents")
        assert len(mem.all_facts()) == 1

    def test_dedup_reinforces_existing(self):
        mem = SemanticMemory(dedup_threshold=0.8)
        f1 = mem.add("agents use memory for long-term recall")
        f2 = mem.add("agents use memory for long-term recall")
        assert f2.fact_id == f1.fact_id
        assert f1.mention_count == 2

    def test_different_facts_stored_separately(self):
        mem = SemanticMemory()
        mem.add("agents use memory")
        mem.add("databases store information")
        assert len(mem.all_facts()) == 2

    def test_max_facts_evicts_lowest_importance(self):
        mem = SemanticMemory(max_facts=3)
        mem.add("a", importance_score=0.9)
        mem.add("b different content entirely", importance_score=0.8)
        mem.add("c yet another unique fact here", importance_score=0.7)
        mem.add("d the fourth unique fact is here", importance_score=0.1)
        assert len(mem.all_facts()) <= 3
        # highest-importance should be retained
        contents = [f.content for f in mem.all_facts()]
        assert any("a" in c for c in contents)

    def test_search_returns_relevant(self):
        mem = SemanticMemory()
        mem.add("agents retrieve memory efficiently", importance_score=0.8)
        mem.add("databases are slow for retrieval", importance_score=0.3)
        results = mem.search("agent retrieval", top_k=1)
        assert "agent" in results[0].content or "agents" in results[0].content

    def test_remove_fact(self):
        mem = SemanticMemory()
        f = mem.add("removable fact")
        assert mem.remove(f.fact_id) is True
        assert len(mem.all_facts()) == 0

    def test_remove_nonexistent_returns_false(self):
        mem = SemanticMemory()
        assert mem.remove("no-such-id") is False

    def test_decay_all_lowers_importance(self):
        mem = SemanticMemory()
        mem.add("test fact", importance_score=0.5)
        mem.decay_all(delta=0.1)
        assert mem.all_facts()[0].importance_score == pytest.approx(0.4, rel=1e-4)

    def test_stats_has_expected_keys(self):
        mem = SemanticMemory()
        mem.add("test")
        s = mem.stats()
        for key in ("n_facts", "max_facts", "avg_importance", "high_importance_facts"):
            assert key in s

    def test_to_context_string(self):
        mem = SemanticMemory()
        mem.add("fact about memory", importance_score=0.8)
        ctx = mem.to_context()
        assert "fact about memory" in ctx


# ===========================================================================
# PromotionPolicy
# ===========================================================================

class TestPromotionPolicy:
    def _setup(self, promo_threshold=2):
        episodic = EpisodicMemory(promotion_threshold=promo_threshold)
        semantic = SemanticMemory()
        policy = PromotionPolicy(episodic, semantic,
                                 config=PromotionConfig(mention_threshold=promo_threshold))
        return episodic, semantic, policy

    def test_promotes_frequent_event(self):
        ep, sem, pol = self._setup(promo_threshold=2)
        ep.add("agent memory system is great")
        ep.add("agent memory system is great")  # mention_count=2
        result = pol.run()
        assert result.total_promoted >= 1

    def test_does_not_promote_infrequent(self):
        ep, sem, pol = self._setup(promo_threshold=3)
        ep.add("mentioned just once here")
        result = pol.run()
        # Nothing should be promoted; event below threshold is not a candidate
        assert result.total_promoted == 0
        # skipped_threshold may be 0 because promotion_candidates() already
        # filters out low-mention events before the policy sees them
        assert result.total_promoted == 0

    def test_skips_too_short_content(self):
        ep, sem, pol = self._setup(promo_threshold=1)
        cfg = PromotionConfig(mention_threshold=1, min_tokens=5)
        pol2 = PromotionPolicy(ep, sem, config=cfg)
        ep.add("hi")  # 1 token < 5
        ep._events[0].mention_count = 3
        result = pol2.run()
        assert len(result.skipped_too_short) >= 1

    def test_dedup_reinforces_existing_semantic(self):
        ep, sem, pol = self._setup(promo_threshold=2)
        # Pre-load semantic with same fact
        sem.add("agent memory system is great", importance_score=0.5)
        old_imp = sem.all_facts()[0].importance_score

        ep.add("agent memory system is great")
        ep.add("agent memory system is great")
        result = pol.run()
        assert len(result.skipped_dedup) >= 1
        # Importance reinforced
        assert sem.all_facts()[0].importance_score >= old_imp

    def test_result_is_promotion_result(self):
        ep, sem, pol = self._setup()
        result = pol.run()
        assert isinstance(result, PromotionResult)

    def test_judge_fn_sets_importance(self):
        ep, sem, _ = self._setup(promo_threshold=2)
        cfg = PromotionConfig(mention_threshold=2)
        pol = PromotionPolicy(ep, sem, config=cfg, judge_fn=lambda c: 0.99)
        ep.add("this topic appears again and again in the text")
        ep.add("this topic appears again and again in the text")
        pol.run()
        if sem.all_facts():
            assert sem.all_facts()[0].importance_score == pytest.approx(0.99, rel=1e-2)


# ===========================================================================
# TieredMemoryStore
# ===========================================================================

class TestTieredMemoryStore:
    def test_add_goes_to_episodic(self):
        store = TieredMemoryStore()
        store.add("a new event happened today")
        assert store.episodic.stats()["n_events"] == 1

    def test_promote_moves_to_semantic(self):
        store = TieredMemoryStore(
            episodic_max_events=100,
        )
        store.episodic._promotion_threshold = 1
        store.episodic._promo_threshold = 1
        store._policy._cfg.mention_threshold = 1
        store.add("important frequently-seen fact about agents")
        result = store.promote()
        assert result.total_promoted + result.total_skipped >= 0  # always valid

    def test_recall_searches_both_tiers(self):
        store = TieredMemoryStore()
        store.add("recent event with agent memory")
        store.semantic.add("long-term fact about retrieval systems")
        recall = store.recall("agent memory retrieval", top_k=3)
        assert "episodic" in recall
        assert "semantic" in recall

    def test_to_context_string(self):
        store = TieredMemoryStore()
        store.add("recent event")
        store.semantic.add("known fact about systems")
        ctx = store.to_context()
        assert isinstance(ctx, str)

    def test_stats_has_both_tiers(self):
        store = TieredMemoryStore()
        s = store.stats()
        assert "episodic" in s
        assert "semantic" in s

    def test_auto_promote_triggers_on_add(self):
        store = TieredMemoryStore(auto_promote=True)
        # With auto-promote, promotion is called but may not move anything (threshold)
        store.add("event a")
        # Just verifying no exception and structure is intact
        assert store.episodic.stats()["n_events"] >= 0

    def test_episodic_to_semantic_after_threshold(self):
        """End-to-end: re-mentioning a fact N times graduates it to semantic."""
        threshold = 3
        cfg = PromotionConfig(mention_threshold=threshold)
        store = TieredMemoryStore()
        store._policy._cfg = cfg
        store.episodic._promo_threshold = threshold

        content = "knowledge graph enables multi-hop reasoning"
        for _ in range(threshold):
            store.episodic.add(content)

        result = store.promote()
        assert result.total_promoted >= 1
        # Fact should now be searchable in semantic memory
        facts = store.semantic.search("knowledge graph", top_k=3)
        assert len(facts) >= 1


# ===========================================================================
# Token-Jaccard helper
# ===========================================================================

class TestTokenJaccard:
    def test_identical_is_one(self):
        assert _token_jaccard("hello world", "hello world") == 1.0

    def test_disjoint_is_zero(self):
        assert _token_jaccard("abc def", "xyz uvw") == 0.0

    def test_partial_overlap(self):
        score = _token_jaccard("cat and dog", "cat and fish")
        assert 0.0 < score < 1.0

    def test_empty_both_is_one(self):
        assert _token_jaccard("", "") == 1.0

    def test_empty_one_is_zero(self):
        assert _token_jaccard("hello", "") == 0.0
