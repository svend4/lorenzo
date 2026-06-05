"""Tests for docstoolkit.doc_ranker."""
from __future__ import annotations

import math

import pytest

from docstoolkit.doc_ranker import (
    DocInfo,
    DocRanker,
    RankConfig,
    RankedDoc,
    RankSignal,
    SignalScore,
)


DAY = 86400.0
NOW = 1_700_000_000.0


# ---------------------------------------------------------------------------
class TestRankSignal:
    def test_members_present(self):
        names = {s.name for s in RankSignal}
        assert names == {
            "RELEVANCE", "RECENCY", "POPULARITY",
            "LENGTH", "AUTHORITY", "FRESHNESS",
        }

    def test_values_are_strings(self):
        assert RankSignal.RELEVANCE.value == "relevance"
        assert RankSignal.FRESHNESS.value == "freshness"

    def test_equality(self):
        assert RankSignal.RELEVANCE == RankSignal.RELEVANCE
        assert RankSignal.RELEVANCE != RankSignal.RECENCY


# ---------------------------------------------------------------------------
class TestSignalScore:
    def test_construct(self):
        s = SignalScore(signal=RankSignal.RELEVANCE, raw_value=0.5, normalized=0.5)
        assert s.signal == RankSignal.RELEVANCE
        assert s.raw_value == 0.5
        assert s.normalized == 0.5

    def test_fields_are_mutable(self):
        s = SignalScore(signal=RankSignal.LENGTH, raw_value=0.1, normalized=0.2)
        s.normalized = 0.9
        assert s.normalized == 0.9


# ---------------------------------------------------------------------------
class TestRankedDoc:
    def test_construct(self):
        s = SignalScore(signal=RankSignal.RELEVANCE, raw_value=1.0, normalized=1.0)
        r = RankedDoc(doc_id="d1", final_score=0.8, signal_scores={RankSignal.RELEVANCE: s}, rank=1)
        assert r.doc_id == "d1"
        assert r.final_score == 0.8
        assert r.rank == 1
        assert r.signal_scores[RankSignal.RELEVANCE].raw_value == 1.0


# ---------------------------------------------------------------------------
class TestRankConfig:
    def test_defaults(self):
        c = RankConfig()
        assert c.weights == {RankSignal.RELEVANCE: 1.0}
        assert c.normalize_scores is True
        assert c.boost_recent_days == 30

    def test_default_weights_independent(self):
        a = RankConfig()
        b = RankConfig()
        a.weights[RankSignal.RECENCY] = 0.5
        assert RankSignal.RECENCY not in b.weights

    def test_override(self):
        c = RankConfig(
            weights={RankSignal.AUTHORITY: 2.0},
            normalize_scores=False,
            boost_recent_days=7,
        )
        assert c.weights == {RankSignal.AUTHORITY: 2.0}
        assert c.normalize_scores is False
        assert c.boost_recent_days == 7


# ---------------------------------------------------------------------------
class TestDocInfo:
    def test_defaults(self):
        d = DocInfo(doc_id="x")
        assert d.doc_id == "x"
        assert d.relevance == 0.0
        assert d.created_at == 0.0
        assert d.popularity == 0
        assert d.length == 0
        assert d.authority == 0.0

    def test_full(self):
        d = DocInfo(
            doc_id="d", relevance=0.9, created_at=NOW,
            popularity=100, length=500, authority=0.7,
        )
        assert d.relevance == 0.9
        assert d.popularity == 100


# ---------------------------------------------------------------------------
class TestScoreRelevance:
    def test_direct_value(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", relevance=0.7)]
        scores = ranker.score_signal(docs, RankSignal.RELEVANCE)
        assert scores[0].raw_value == 0.7

    def test_multiple_docs(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [
            DocInfo(doc_id="a", relevance=0.1),
            DocInfo(doc_id="b", relevance=0.9),
        ]
        scores = ranker.score_signal(docs, RankSignal.RELEVANCE)
        assert scores[0].raw_value == 0.1
        assert scores[1].raw_value == 0.9


# ---------------------------------------------------------------------------
class TestScoreRecency:
    def test_zero_age(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", created_at=NOW)]
        scores = ranker.score_signal(docs, RankSignal.RECENCY, now=NOW)
        assert scores[0].raw_value == 1.0

    def test_one_day_old(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", created_at=NOW - DAY)]
        scores = ranker.score_signal(docs, RankSignal.RECENCY, now=NOW)
        assert scores[0].raw_value == pytest.approx(0.5)

    def test_old_doc_less_recent(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        new = DocInfo(doc_id="new", created_at=NOW)
        old = DocInfo(doc_id="old", created_at=NOW - 100 * DAY)
        scores = ranker.score_signal([new, old], RankSignal.RECENCY, now=NOW)
        assert scores[0].raw_value > scores[1].raw_value

    def test_future_clamped(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", created_at=NOW + 10 * DAY)]
        scores = ranker.score_signal(docs, RankSignal.RECENCY, now=NOW)
        assert scores[0].raw_value == 1.0


# ---------------------------------------------------------------------------
class TestScorePopularity:
    def test_zero_popularity(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", popularity=0)]
        scores = ranker.score_signal(docs, RankSignal.POPULARITY)
        assert scores[0].raw_value == 0.0

    def test_log_value(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", popularity=99)]
        scores = ranker.score_signal(docs, RankSignal.POPULARITY)
        assert scores[0].raw_value == pytest.approx(math.log(100))

    def test_monotonic(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [
            DocInfo(doc_id="a", popularity=1),
            DocInfo(doc_id="b", popularity=100),
        ]
        scores = ranker.score_signal(docs, RankSignal.POPULARITY)
        assert scores[0].raw_value < scores[1].raw_value


# ---------------------------------------------------------------------------
class TestScoreLength:
    def test_exact_1000(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", length=1000)]
        scores = ranker.score_signal(docs, RankSignal.LENGTH)
        assert scores[0].raw_value == 1.0

    def test_zero_length(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", length=0)]
        scores = ranker.score_signal(docs, RankSignal.LENGTH)
        assert scores[0].raw_value == 0.0

    def test_500_chars(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", length=500)]
        scores = ranker.score_signal(docs, RankSignal.LENGTH)
        assert scores[0].raw_value == pytest.approx(0.5)

    def test_large_clamped(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", length=5000)]
        scores = ranker.score_signal(docs, RankSignal.LENGTH)
        assert scores[0].raw_value == 0.0


# ---------------------------------------------------------------------------
class TestScoreAuthority:
    def test_direct(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", authority=0.42)]
        scores = ranker.score_signal(docs, RankSignal.AUTHORITY)
        assert scores[0].raw_value == 0.42

    def test_zero(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a")]
        scores = ranker.score_signal(docs, RankSignal.AUTHORITY)
        assert scores[0].raw_value == 0.0


# ---------------------------------------------------------------------------
class TestScoreFreshness:
    def test_fresh_doc(self):
        ranker = DocRanker(RankConfig(boost_recent_days=30, normalize_scores=False))
        docs = [DocInfo(doc_id="a", created_at=NOW - 5 * DAY)]
        scores = ranker.score_signal(docs, RankSignal.FRESHNESS, now=NOW)
        assert scores[0].raw_value == 1.0

    def test_stale_doc(self):
        ranker = DocRanker(RankConfig(boost_recent_days=30, normalize_scores=False))
        docs = [DocInfo(doc_id="a", created_at=NOW - 100 * DAY)]
        scores = ranker.score_signal(docs, RankSignal.FRESHNESS, now=NOW)
        assert scores[0].raw_value == 0.0

    def test_boundary(self):
        ranker = DocRanker(RankConfig(boost_recent_days=30, normalize_scores=False))
        # Exactly 30 days old -> not strictly less than 30 -> 0.
        docs = [DocInfo(doc_id="a", created_at=NOW - 30 * DAY)]
        scores = ranker.score_signal(docs, RankSignal.FRESHNESS, now=NOW)
        assert scores[0].raw_value == 0.0

    def test_custom_boost_window(self):
        ranker = DocRanker(RankConfig(boost_recent_days=7, normalize_scores=False))
        docs = [
            DocInfo(doc_id="a", created_at=NOW - 5 * DAY),
            DocInfo(doc_id="b", created_at=NOW - 10 * DAY),
        ]
        scores = ranker.score_signal(docs, RankSignal.FRESHNESS, now=NOW)
        assert scores[0].raw_value == 1.0
        assert scores[1].raw_value == 0.0


# ---------------------------------------------------------------------------
class TestNormalizeSignals:
    def test_empty(self):
        assert DocRanker.normalize_signals([]) == []

    def test_single_value(self):
        assert DocRanker.normalize_signals([5.0]) == [1.0]

    def test_all_equal(self):
        assert DocRanker.normalize_signals([2.0, 2.0, 2.0]) == [1.0, 1.0, 1.0]

    def test_mixed(self):
        assert DocRanker.normalize_signals([0.0, 5.0, 10.0]) == [0.0, 0.5, 1.0]

    def test_negative_values(self):
        assert DocRanker.normalize_signals([-5.0, 0.0, 5.0]) == [0.0, 0.5, 1.0]

    def test_range_preserved(self):
        out = DocRanker.normalize_signals([1.0, 2.0, 3.0, 4.0])
        assert min(out) == 0.0
        assert max(out) == 1.0


# ---------------------------------------------------------------------------
class TestCombineScores:
    def test_single_weight(self):
        v = DocRanker.combine_scores(
            {RankSignal.RELEVANCE: 0.8},
            {RankSignal.RELEVANCE: 1.0},
        )
        assert v == 0.8

    def test_weighted_sum(self):
        v = DocRanker.combine_scores(
            {RankSignal.RELEVANCE: 0.5, RankSignal.RECENCY: 1.0},
            {RankSignal.RELEVANCE: 0.6, RankSignal.RECENCY: 0.4},
        )
        assert v == pytest.approx(0.5 * 0.6 + 1.0 * 0.4)

    def test_weights_with_no_match(self):
        v = DocRanker.combine_scores(
            {RankSignal.RELEVANCE: 0.5},
            {RankSignal.AUTHORITY: 1.0},
        )
        assert v == 0.0

    def test_extra_scores_ignored(self):
        v = DocRanker.combine_scores(
            {RankSignal.RELEVANCE: 1.0, RankSignal.LENGTH: 1.0},
            {RankSignal.RELEVANCE: 1.0},
        )
        assert v == 1.0

    def test_empty_inputs(self):
        assert DocRanker.combine_scores({}, {}) == 0.0


# ---------------------------------------------------------------------------
class TestRankIntegration:
    def test_default_config(self):
        ranker = DocRanker()
        docs = [
            DocInfo(doc_id="a", relevance=0.2),
            DocInfo(doc_id="b", relevance=0.9),
            DocInfo(doc_id="c", relevance=0.5),
        ]
        out = ranker.rank(docs)
        assert [r.doc_id for r in out] == ["b", "c", "a"]
        assert [r.rank for r in out] == [1, 2, 3]

    def test_multi_signal(self):
        cfg = RankConfig(weights={
            RankSignal.RELEVANCE: 0.5,
            RankSignal.RECENCY: 0.5,
        })
        ranker = DocRanker(cfg)
        docs = [
            DocInfo(doc_id="old_relevant", relevance=1.0, created_at=NOW - 100 * DAY),
            DocInfo(doc_id="new_irrelevant", relevance=0.0, created_at=NOW),
        ]
        out = ranker.rank(docs, now=NOW)
        ids = [r.doc_id for r in out]
        # Both should score equal-ish; either order valid, but both must rank in 1..2.
        assert set(ids) == {"old_relevant", "new_irrelevant"}
        assert {r.rank for r in out} == {1, 2}

    def test_final_score_in_zero_one(self):
        cfg = RankConfig(weights={RankSignal.RELEVANCE: 1.0})
        ranker = DocRanker(cfg)
        docs = [DocInfo(doc_id=str(i), relevance=i * 0.1) for i in range(5)]
        out = ranker.rank(docs)
        for r in out:
            assert 0.0 <= r.final_score <= 1.0

    def test_signal_scores_stored(self):
        cfg = RankConfig(weights={
            RankSignal.RELEVANCE: 0.5,
            RankSignal.AUTHORITY: 0.5,
        })
        ranker = DocRanker(cfg)
        docs = [
            DocInfo(doc_id="a", relevance=0.5, authority=0.4),
            DocInfo(doc_id="b", relevance=0.9, authority=0.7),
        ]
        out = ranker.rank(docs)
        for r in out:
            assert RankSignal.RELEVANCE in r.signal_scores
            assert RankSignal.AUTHORITY in r.signal_scores

    def test_ranking_stable_for_one_doc(self):
        ranker = DocRanker()
        docs = [DocInfo(doc_id="only", relevance=0.3)]
        out = ranker.rank(docs)
        assert len(out) == 1
        assert out[0].rank == 1

    def test_normalize_disabled(self):
        cfg = RankConfig(
            weights={RankSignal.POPULARITY: 1.0},
            normalize_scores=False,
        )
        ranker = DocRanker(cfg)
        docs = [
            DocInfo(doc_id="a", popularity=0),
            DocInfo(doc_id="b", popularity=999),
        ]
        out = ranker.rank(docs)
        # Top doc should be b with raw log(1000).
        assert out[0].doc_id == "b"
        assert out[0].final_score == pytest.approx(math.log(1000))


# ---------------------------------------------------------------------------
class TestTopK:
    def test_basic(self):
        ranker = DocRanker()
        docs = [DocInfo(doc_id=str(i), relevance=i * 0.1) for i in range(10)]
        out = ranker.top_k(docs, k=3)
        assert len(out) == 3
        assert [r.doc_id for r in out] == ["9", "8", "7"]

    def test_k_larger_than_docs(self):
        ranker = DocRanker()
        docs = [DocInfo(doc_id="a", relevance=0.5)]
        out = ranker.top_k(docs, k=10)
        assert len(out) == 1

    def test_k_zero(self):
        ranker = DocRanker()
        docs = [DocInfo(doc_id="a", relevance=0.5)]
        assert ranker.top_k(docs, k=0) == []

    def test_k_negative(self):
        ranker = DocRanker()
        docs = [DocInfo(doc_id="a", relevance=0.5)]
        assert ranker.top_k(docs, k=-3) == []

    def test_ranks_consecutive(self):
        ranker = DocRanker()
        docs = [DocInfo(doc_id=str(i), relevance=i * 0.1) for i in range(5)]
        out = ranker.top_k(docs, k=3)
        assert [r.rank for r in out] == [1, 2, 3]


# ---------------------------------------------------------------------------
class TestRerank:
    def test_boost_changes_order(self):
        cfg = RankConfig(
            weights={RankSignal.RELEVANCE: 1.0},
            normalize_scores=False,
        )
        ranker = DocRanker(cfg)
        docs = [
            DocInfo(doc_id="a", relevance=0.9),
            DocInfo(doc_id="b", relevance=0.5),
        ]
        ranked = ranker.rank(docs)
        # Boost the lower doc enough to overtake.
        boosted = ranker.rerank(ranked, boost_ids={"b"}, boost_factor=10.0)
        assert boosted[0].doc_id == "b"
        assert boosted[0].rank == 1

    def test_no_boost_ids_preserves_order(self):
        ranker = DocRanker()
        docs = [
            DocInfo(doc_id="a", relevance=0.9),
            DocInfo(doc_id="b", relevance=0.5),
        ]
        ranked = ranker.rank(docs)
        boosted = ranker.rerank(ranked, boost_ids=set(), boost_factor=2.0)
        assert [r.doc_id for r in boosted] == [r.doc_id for r in ranked]

    def test_boost_factor_applied(self):
        ranker = DocRanker()
        docs = [DocInfo(doc_id="a", relevance=0.5)]
        ranked = ranker.rank(docs)
        original = ranked[0].final_score
        boosted = ranker.rerank(ranked, boost_ids={"a"}, boost_factor=2.0)
        assert boosted[0].final_score == pytest.approx(original * 2.0)

    def test_unmatched_boost_ids_ignored(self):
        ranker = DocRanker()
        docs = [
            DocInfo(doc_id="a", relevance=0.9),
            DocInfo(doc_id="b", relevance=0.5),
        ]
        ranked = ranker.rank(docs)
        boosted = ranker.rerank(ranked, boost_ids={"nonexistent"}, boost_factor=100.0)
        assert [r.doc_id for r in boosted] == ["a", "b"]
        assert boosted[0].final_score == ranked[0].final_score

    def test_rerank_assigns_new_ranks(self):
        cfg = RankConfig(
            weights={RankSignal.RELEVANCE: 1.0},
            normalize_scores=False,
        )
        ranker = DocRanker(cfg)
        docs = [
            DocInfo(doc_id="a", relevance=0.9),
            DocInfo(doc_id="b", relevance=0.7),
            DocInfo(doc_id="c", relevance=0.5),
        ]
        ranked = ranker.rank(docs)
        boosted = ranker.rerank(ranked, boost_ids={"c"}, boost_factor=10.0)
        assert [r.rank for r in boosted] == [1, 2, 3]
        assert boosted[0].doc_id == "c"

    def test_rerank_does_not_mutate_input(self):
        ranker = DocRanker()
        docs = [
            DocInfo(doc_id="a", relevance=0.9),
            DocInfo(doc_id="b", relevance=0.5),
        ]
        ranked = ranker.rank(docs)
        before = [(r.doc_id, r.final_score, r.rank) for r in ranked]
        _ = ranker.rerank(ranked, boost_ids={"b"}, boost_factor=10.0)
        after = [(r.doc_id, r.final_score, r.rank) for r in ranked]
        assert before == after


# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_docs(self):
        ranker = DocRanker()
        assert ranker.rank([]) == []

    def test_single_doc(self):
        ranker = DocRanker()
        docs = [DocInfo(doc_id="only", relevance=0.3)]
        out = ranker.rank(docs)
        assert len(out) == 1
        assert out[0].doc_id == "only"

    def test_weights_with_unused_signal(self):
        # All weights are valid signals; ranker should still produce output.
        cfg = RankConfig(weights={
            RankSignal.RELEVANCE: 0.5,
            RankSignal.AUTHORITY: 0.5,
        })
        ranker = DocRanker(cfg)
        docs = [DocInfo(doc_id="a", relevance=0.5, authority=0.5)]
        out = ranker.rank(docs)
        assert len(out) == 1

    def test_empty_weights(self):
        cfg = RankConfig(weights={})
        ranker = DocRanker(cfg)
        docs = [DocInfo(doc_id="a", relevance=0.5)]
        out = ranker.rank(docs)
        assert len(out) == 1
        # With no weights, combine returns 0.0.
        assert out[0].final_score == 0.0

    def test_all_docs_identical(self):
        ranker = DocRanker()
        docs = [
            DocInfo(doc_id="a", relevance=0.5),
            DocInfo(doc_id="b", relevance=0.5),
            DocInfo(doc_id="c", relevance=0.5),
        ]
        out = ranker.rank(docs)
        assert {r.doc_id for r in out} == {"a", "b", "c"}
        assert all(r.final_score == 1.0 for r in out)

    def test_negative_popularity_treated_as_zero(self):
        ranker = DocRanker(RankConfig(normalize_scores=False))
        docs = [DocInfo(doc_id="a", popularity=-5)]
        scores = ranker.score_signal(docs, RankSignal.POPULARITY)
        assert scores[0].raw_value == 0.0

    def test_none_config_uses_default(self):
        ranker = DocRanker(None)
        assert ranker.config.weights == {RankSignal.RELEVANCE: 1.0}

    def test_rank_returns_ranked_doc_type(self):
        ranker = DocRanker()
        docs = [DocInfo(doc_id="a", relevance=0.5)]
        out = ranker.rank(docs)
        assert isinstance(out[0], RankedDoc)
        assert isinstance(out[0].signal_scores[RankSignal.RELEVANCE], SignalScore)
