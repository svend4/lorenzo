"""Tests for docstoolkit.recommender (E51)."""
from __future__ import annotations

import pytest

from docstoolkit.recommender import (
    UserProfile,
    ContentScorer,
    RecommendationScore,
    RecommendationConfig,
    Recommendation,
    RecommendationEngine,
)


# ============================================================
# UserProfile
# ============================================================

class TestUserProfileInit:
    def test_user_id_stored(self):
        p = UserProfile(user_id="u1")
        assert p.user_id == "u1"

    def test_defaults_empty(self):
        p = UserProfile(user_id="u1")
        assert p.viewed_docs == []
        assert p.liked_docs == set()
        assert p.disliked_docs == set()
        assert p.query_history == []
        assert p.tags == {}

    def test_independent_defaults(self):
        """Mutable defaults must not be shared between instances."""
        p1 = UserProfile(user_id="a")
        p2 = UserProfile(user_id="b")
        p1.viewed_docs.append("x")
        assert p2.viewed_docs == []


class TestUserProfileAddView:
    def test_add_view_appends(self):
        p = UserProfile(user_id="u")
        p.add_view("doc1")
        assert p.viewed_docs == ["doc1"]

    def test_add_view_multiple(self):
        p = UserProfile(user_id="u")
        p.add_view("d1")
        p.add_view("d2")
        assert p.viewed_docs == ["d1", "d2"]

    def test_add_view_duplicate_allowed(self):
        p = UserProfile(user_id="u")
        p.add_view("d1")
        p.add_view("d1")
        assert len(p.viewed_docs) == 2

    def test_add_view_does_not_affect_liked(self):
        p = UserProfile(user_id="u")
        p.add_view("d1")
        assert "d1" not in p.liked_docs


class TestUserProfileAddLike:
    def test_add_like_adds_to_liked(self):
        p = UserProfile(user_id="u")
        p.add_like("doc1")
        assert "doc1" in p.liked_docs

    def test_add_like_removes_from_disliked(self):
        p = UserProfile(user_id="u")
        p.disliked_docs.add("doc1")
        p.add_like("doc1")
        assert "doc1" not in p.disliked_docs

    def test_add_like_idempotent(self):
        p = UserProfile(user_id="u")
        p.add_like("doc1")
        p.add_like("doc1")
        assert len(p.liked_docs) == 1

    def test_add_like_multiple(self):
        p = UserProfile(user_id="u")
        p.add_like("d1")
        p.add_like("d2")
        assert p.liked_docs == {"d1", "d2"}


class TestUserProfileAddDislike:
    def test_add_dislike_adds_to_disliked(self):
        p = UserProfile(user_id="u")
        p.add_dislike("doc1")
        assert "doc1" in p.disliked_docs

    def test_add_dislike_removes_from_liked(self):
        p = UserProfile(user_id="u")
        p.liked_docs.add("doc1")
        p.add_dislike("doc1")
        assert "doc1" not in p.liked_docs

    def test_add_dislike_idempotent(self):
        p = UserProfile(user_id="u")
        p.add_dislike("doc1")
        p.add_dislike("doc1")
        assert len(p.disliked_docs) == 1

    def test_add_dislike_multiple(self):
        p = UserProfile(user_id="u")
        p.add_dislike("d1")
        p.add_dislike("d2")
        assert p.disliked_docs == {"d1", "d2"}


class TestUserProfileInterestTags:
    def test_empty_tags_returns_empty(self):
        p = UserProfile(user_id="u")
        assert p.interest_tags() == []

    def test_top_n_ordering(self):
        p = UserProfile(user_id="u", tags={"a": 0.3, "b": 0.9, "c": 0.6})
        result = p.interest_tags(n=3)
        assert result == ["b", "c", "a"]

    def test_top_n_limits(self):
        p = UserProfile(user_id="u", tags={str(i): float(i) for i in range(20)})
        result = p.interest_tags(n=10)
        assert len(result) == 10

    def test_default_n_is_10(self):
        p = UserProfile(user_id="u", tags={str(i): float(i) for i in range(20)})
        result = p.interest_tags()
        assert len(result) == 10

    def test_n_larger_than_tags(self):
        p = UserProfile(user_id="u", tags={"x": 1.0, "y": 2.0})
        result = p.interest_tags(n=100)
        assert len(result) == 2

    def test_negative_scores_included(self):
        p = UserProfile(user_id="u", tags={"neg": -1.0, "pos": 1.0})
        result = p.interest_tags(n=2)
        assert result[0] == "pos"
        assert result[1] == "neg"


class TestUserProfileSeenDocs:
    def test_empty_profile_no_seen(self):
        p = UserProfile(user_id="u")
        assert p.seen_docs() == set()

    def test_viewed_counted_as_seen(self):
        p = UserProfile(user_id="u")
        p.add_view("d1")
        assert "d1" in p.seen_docs()

    def test_liked_counted_as_seen(self):
        p = UserProfile(user_id="u")
        p.add_like("d2")
        assert "d2" in p.seen_docs()

    def test_disliked_counted_as_seen(self):
        p = UserProfile(user_id="u")
        p.add_dislike("d3")
        assert "d3" in p.seen_docs()

    def test_union_of_all_sources(self):
        p = UserProfile(user_id="u")
        p.add_view("v1")
        p.add_like("l1")
        p.add_dislike("dl1")
        assert p.seen_docs() == {"v1", "l1", "dl1"}

    def test_duplicates_collapsed(self):
        p = UserProfile(user_id="u")
        p.add_view("d1")
        p.add_view("d1")
        p.add_like("d1")
        assert p.seen_docs() == {"d1"}


# ============================================================
# ContentScorer
# ============================================================

class TestContentScorerTagMatch:
    def setup_method(self):
        self.scorer = ContentScorer()

    def _profile(self, tags: dict[str, float]) -> UserProfile:
        return UserProfile(user_id="u", tags=tags)

    def test_no_tags_zero_contribution(self):
        p = self._profile({"python": 1.0})
        result = self.scorer.score_for_profile(p, "d1", "some text", doc_tags=[])
        # tag_match = 0 / (0+1) = 0
        assert result.score == pytest.approx(0.0)

    def test_tag_match_present(self):
        p = self._profile({"python": 0.8})
        result = self.scorer.score_for_profile(p, "d1", "", doc_tags=["python"])
        # tag_match = 0.8 / (1+1) = 0.4
        assert result.score == pytest.approx(0.4)

    def test_tag_match_reason_included(self):
        p = self._profile({"python": 0.8})
        result = self.scorer.score_for_profile(p, "d1", "", doc_tags=["python"])
        assert any("tag_match" in r for r in result.reasons)

    def test_tag_match_unknown_tag_zero(self):
        p = self._profile({"python": 1.0})
        result = self.scorer.score_for_profile(p, "d1", "", doc_tags=["java"])
        # tag_match = 0 / (1+1) = 0
        assert result.score == pytest.approx(0.0)

    def test_tag_match_partial_overlap(self):
        p = self._profile({"python": 1.0, "java": 0.0})
        result = self.scorer.score_for_profile(
            p, "d1", "", doc_tags=["python", "java"]
        )
        # tag_sum = 1.0 + 0.0 = 1.0; tag_match = 1.0/3 ≈ 0.333
        assert result.score == pytest.approx(1.0 / 3, rel=1e-4)

    def test_tag_match_multiple_matching_tags(self):
        p = self._profile({"a": 1.0, "b": 1.0})
        result = self.scorer.score_for_profile(p, "d1", "", doc_tags=["a", "b"])
        # tag_sum = 2.0; tag_match = 2.0 / (2+1) ≈ 0.667
        assert result.score == pytest.approx(2.0 / 3, rel=1e-4)


class TestContentScorerQueryOverlap:
    def setup_method(self):
        self.scorer = ContentScorer()

    def _profile(self, queries: list[str]) -> UserProfile:
        p = UserProfile(user_id="u")
        p.query_history = queries
        return p

    def test_no_queries_zero_overlap(self):
        p = self._profile([])
        result = self.scorer.score_for_profile(p, "d1", "hello world", doc_tags=[])
        assert result.score == pytest.approx(0.0)

    def test_exact_match_high_overlap(self):
        p = self._profile(["hello world"])
        result = self.scorer.score_for_profile(p, "d1", "hello world", doc_tags=[])
        assert result.score == pytest.approx(1.0)

    def test_partial_overlap(self):
        p = self._profile(["hello"])
        result = self.scorer.score_for_profile(p, "d1", "hello world", doc_tags=[])
        # jaccard({"hello"}, {"hello","world"}) = 1/2 = 0.5
        assert result.score == pytest.approx(0.5)

    def test_no_overlap_zero(self):
        p = self._profile(["xyz"])
        result = self.scorer.score_for_profile(p, "d1", "hello world", doc_tags=[])
        assert result.score == pytest.approx(0.0)

    def test_uses_last_3_queries(self):
        # Only the last 3 should matter
        p = self._profile(["irrelevant", "irrelevant2", "hello", "world", "test"])
        # last 3: "hello", "world", "test"
        result = self.scorer.score_for_profile(p, "d1", "hello world", doc_tags=[])
        assert result.score > 0

    def test_query_overlap_reason_included(self):
        p = self._profile(["hello"])
        result = self.scorer.score_for_profile(p, "d1", "hello world", doc_tags=[])
        assert any("query_overlap" in r for r in result.reasons)

    def test_empty_doc_text_zero_overlap(self):
        p = self._profile(["hello"])
        result = self.scorer.score_for_profile(p, "d1", "", doc_tags=[])
        assert result.score == pytest.approx(0.0)


class TestContentScorerDislikePenalty:
    def setup_method(self):
        self.scorer = ContentScorer()

    def test_dislike_penalty_applied(self):
        p = UserProfile(user_id="u")
        p.add_dislike("d1")
        result = self.scorer.score_for_profile(p, "d1", "some text", doc_tags=[])
        assert result.score == pytest.approx(-0.5)

    def test_dislike_penalty_reason_included(self):
        p = UserProfile(user_id="u")
        p.add_dislike("d1")
        result = self.scorer.score_for_profile(p, "d1", "", doc_tags=[])
        assert any("dislike_penalty" in r for r in result.reasons)

    def test_no_dislike_no_penalty(self):
        p = UserProfile(user_id="u")
        result = self.scorer.score_for_profile(p, "d1", "", doc_tags=[])
        assert result.score == pytest.approx(0.0)
        assert not any("dislike_penalty" in r for r in result.reasons)

    def test_dislike_reduces_positive_score(self):
        p = UserProfile(user_id="u", tags={"a": 2.0})
        p.add_dislike("d1")
        result = self.scorer.score_for_profile(p, "d1", "", doc_tags=["a"])
        # tag_match = 2/(1+1) = 1.0; penalty = -0.5 → 0.5
        assert result.score == pytest.approx(0.5)

    def test_liked_doc_no_penalty(self):
        p = UserProfile(user_id="u")
        p.add_like("d1")
        result = self.scorer.score_for_profile(p, "d1", "", doc_tags=[])
        assert result.score == pytest.approx(0.0)


class TestContentScorerScoreAll:
    def setup_method(self):
        self.scorer = ContentScorer()

    def test_returns_all_docs(self):
        p = UserProfile(user_id="u")
        docs = {"a": "text", "b": "text", "c": "text"}
        results = self.scorer.score_all(p, docs)
        assert len(results) == 3

    def test_sorted_descending(self):
        p = UserProfile(user_id="u", tags={"x": 1.0})
        docs = {
            "high": "text",
            "low": "text",
        }
        tags = {"high": ["x"], "low": []}
        results = self.scorer.score_all(p, docs, doc_tags=tags)
        assert results[0].doc_id == "high"
        assert results[1].doc_id == "low"

    def test_empty_docs_returns_empty(self):
        p = UserProfile(user_id="u")
        results = self.scorer.score_all(p, {})
        assert results == []

    def test_doc_tags_optional(self):
        p = UserProfile(user_id="u")
        docs = {"d1": "text"}
        results = self.scorer.score_all(p, docs)
        assert len(results) == 1

    def test_result_is_recommendation_score(self):
        p = UserProfile(user_id="u")
        docs = {"d1": "text"}
        results = self.scorer.score_all(p, docs)
        assert isinstance(results[0], RecommendationScore)


# ============================================================
# RecommendationEngine
# ============================================================

class TestRecommendationEngineBasic:
    def setup_method(self):
        self.engine = RecommendationEngine()

    def test_returns_list(self):
        p = UserProfile(user_id="u")
        result = self.engine.recommend(p, {})
        assert isinstance(result, list)

    def test_empty_docs_returns_empty(self):
        p = UserProfile(user_id="u")
        result = self.engine.recommend(p, {})
        assert result == []

    def test_result_is_recommendation(self):
        p = UserProfile(user_id="u")
        docs = {"d1": "text"}
        result = self.engine.recommend(p, docs)
        assert len(result) == 1
        assert isinstance(result[0], Recommendation)

    def test_rank_starts_at_one(self):
        p = UserProfile(user_id="u")
        docs = {"d1": "a", "d2": "b", "d3": "c"}
        result = self.engine.recommend(p, docs)
        ranks = [r.rank for r in result]
        assert 1 in ranks

    def test_ranks_are_sequential(self):
        p = UserProfile(user_id="u")
        docs = {f"d{i}": f"text{i}" for i in range(5)}
        result = self.engine.recommend(p, docs)
        ranks = sorted(r.rank for r in result)
        assert ranks == list(range(1, len(result) + 1))

    def test_doc_id_in_recommendation(self):
        p = UserProfile(user_id="u")
        docs = {"myDoc": "content"}
        result = self.engine.recommend(p, docs)
        assert result[0].doc_id == "myDoc"


class TestRecommendationEngineExcludeSeen:
    def test_exclude_seen_default_true(self):
        config = RecommendationConfig()
        assert config.exclude_seen is True

    def test_viewed_doc_excluded(self):
        p = UserProfile(user_id="u")
        p.add_view("d1")
        engine = RecommendationEngine(RecommendationConfig(exclude_seen=True))
        result = engine.recommend(p, {"d1": "text", "d2": "text"})
        ids = [r.doc_id for r in result]
        assert "d1" not in ids
        assert "d2" in ids

    def test_liked_doc_excluded(self):
        p = UserProfile(user_id="u")
        p.add_like("d1")
        engine = RecommendationEngine(RecommendationConfig(exclude_seen=True))
        result = engine.recommend(p, {"d1": "text", "d2": "text"})
        ids = [r.doc_id for r in result]
        assert "d1" not in ids

    def test_disliked_doc_excluded(self):
        p = UserProfile(user_id="u")
        p.add_dislike("d1")
        engine = RecommendationEngine(RecommendationConfig(exclude_seen=True))
        result = engine.recommend(p, {"d1": "text", "d2": "text"})
        ids = [r.doc_id for r in result]
        assert "d1" not in ids

    def test_exclude_seen_false_includes_viewed(self):
        p = UserProfile(user_id="u")
        p.add_view("d1")
        engine = RecommendationEngine(RecommendationConfig(exclude_seen=False))
        result = engine.recommend(p, {"d1": "text"})
        assert len(result) == 1
        assert result[0].doc_id == "d1"

    def test_all_docs_seen_returns_empty(self):
        p = UserProfile(user_id="u")
        p.add_view("d1")
        p.add_view("d2")
        engine = RecommendationEngine(RecommendationConfig(exclude_seen=True))
        result = engine.recommend(p, {"d1": "text", "d2": "text"})
        assert result == []


class TestRecommendationEngineTopK:
    def test_top_k_limits_results(self):
        p = UserProfile(user_id="u")
        docs = {f"d{i}": f"text{i}" for i in range(20)}
        engine = RecommendationEngine(RecommendationConfig(top_k=5))
        result = engine.recommend(p, docs)
        assert len(result) <= 5

    def test_top_k_zero_returns_empty(self):
        p = UserProfile(user_id="u")
        docs = {"d1": "text"}
        engine = RecommendationEngine(RecommendationConfig(top_k=0))
        result = engine.recommend(p, docs)
        assert result == []

    def test_top_k_larger_than_docs(self):
        p = UserProfile(user_id="u")
        docs = {"d1": "text", "d2": "text"}
        engine = RecommendationEngine(RecommendationConfig(top_k=100))
        result = engine.recommend(p, docs)
        assert len(result) == 2

    def test_default_top_k_is_10(self):
        config = RecommendationConfig()
        assert config.top_k == 10


class TestRecommendationEngineDiversity:
    def test_diversity_factor_default(self):
        config = RecommendationConfig()
        assert config.diversity_factor == pytest.approx(0.1)

    def test_diversity_penalizes_high_overlap(self):
        """Second doc with same tags should be penalized relative to distinct doc."""
        p = UserProfile(user_id="u", tags={"a": 1.0, "b": 1.0})
        docs = {
            "same_tags": "text",
            "also_same": "text",
            "different": "text",
        }
        tag_map = {
            "same_tags": ["a", "b"],
            "also_same": ["a", "b"],
            "different": ["c", "d"],
        }
        engine = RecommendationEngine(
            RecommendationConfig(top_k=3, diversity_factor=1.0)
        )
        result = engine.recommend(p, docs, doc_tags=tag_map)
        # "same_tags" will be selected first; "also_same" overlaps 100% → penalized
        # "different" has 0% overlap → not penalized
        ids = [r.doc_id for r in result]
        # "different" should be ranked above "also_same" due to diversity penalty
        assert ids.index("different") < ids.index("also_same")

    def test_no_overlap_no_penalty(self):
        """Documents with entirely different tags should not be penalized."""
        p = UserProfile(user_id="u", tags={"a": 1.0})
        docs = {"d1": "text", "d2": "text"}
        tag_map = {"d1": ["a"], "d2": ["b"]}
        engine = RecommendationEngine(
            RecommendationConfig(top_k=2, diversity_factor=1.0)
        )
        result = engine.recommend(p, docs, doc_tags=tag_map)
        # d1 scores higher (tag match), d2 has no overlap with d1 → no penalty
        assert len(result) == 2

    def test_diversity_zero_factor_no_penalty(self):
        """diversity_factor=0 should not penalize any document."""
        p = UserProfile(user_id="u", tags={"a": 1.0})
        docs = {"d1": "text", "d2": "text"}
        tag_map = {"d1": ["a"], "d2": ["a"]}
        engine = RecommendationEngine(
            RecommendationConfig(top_k=2, diversity_factor=0.0)
        )
        result = engine.recommend(p, docs, doc_tags=tag_map)
        # Both docs have same score (same tags), no penalty → both included
        assert len(result) == 2


class TestRecommendationEngineIntegration:
    def test_reasons_propagated(self):
        p = UserProfile(user_id="u", tags={"python": 0.9})
        docs = {"d1": "python tutorial"}
        engine = RecommendationEngine()
        result = engine.recommend(p, docs, doc_tags={"d1": ["python"]})
        assert len(result[0].reasons) > 0

    def test_score_in_recommendation(self):
        p = UserProfile(user_id="u")
        docs = {"d1": "text"}
        engine = RecommendationEngine()
        result = engine.recommend(p, docs)
        assert isinstance(result[0].score, float)

    def test_custom_scorer_used(self):
        """Engine should accept an injected scorer."""

        class FixedScorer(ContentScorer):
            def score_for_profile(self, profile, doc_id, doc_text, doc_tags=None):
                return RecommendationScore(doc_id=doc_id, score=42.0, reasons=["fixed"])

        p = UserProfile(user_id="u")
        docs = {"d1": "text"}
        engine = RecommendationEngine(scorer=FixedScorer())
        result = engine.recommend(p, docs)
        assert result[0].score == pytest.approx(42.0)

    def test_recommend_without_tags_arg(self):
        """doc_tags should be optional (defaults to no tags)."""
        p = UserProfile(user_id="u")
        docs = {"d1": "hello world", "d2": "foo bar"}
        engine = RecommendationEngine()
        result = engine.recommend(p, docs)
        assert len(result) == 2

    def test_ordering_by_score(self):
        p = UserProfile(user_id="u", tags={"ml": 1.0})
        docs = {
            "ml_doc": "machine learning tutorial",
            "other_doc": "cooking recipe",
        }
        tag_map = {"ml_doc": ["ml"], "other_doc": []}
        engine = RecommendationEngine()
        result = engine.recommend(p, docs, doc_tags=tag_map)
        assert result[0].doc_id == "ml_doc"

    def test_config_defaults(self):
        engine = RecommendationEngine()
        assert engine.config.top_k == 10
        assert engine.config.exclude_seen is True
        assert engine.config.diversity_factor == pytest.approx(0.1)
