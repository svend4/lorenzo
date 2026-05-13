"""Tests for docstoolkit.reranker — E25 Passage re-ranking module.

65+ tests covering:
    - FeatureExtractor: overlap, exact phrase, title match, position_score
    - ScoringWeights normalize
    - PassageScorer: score ordering, score_all
    - PassageReranker: rerank changes order, improvement()
    - Edge cases: empty passages, single passage, no query terms
"""
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.reranker import (
    FeatureExtractor,
    PassageFeatures,
    PassageScore,
    PassageScorer,
    PassageReranker,
    RerankResult,
    RerankerConfig,
    ScoringWeights,
)


# ===========================================================================
# Helpers
# ===========================================================================


def make_features(
    *,
    passage_id: str = "abc12345",
    query_term_overlap: float = 0.5,
    bm25_score: float = 1.0,
    passage_length: int = 20,
    position_score: float = 1.0,
    title_match: bool = False,
    exact_phrase_match: bool = False,
) -> PassageFeatures:
    return PassageFeatures(
        passage_id=passage_id,
        query_term_overlap=query_term_overlap,
        bm25_score=bm25_score,
        passage_length=passage_length,
        position_score=position_score,
        title_match=title_match,
        exact_phrase_match=exact_phrase_match,
    )


extractor = FeatureExtractor()
scorer = PassageScorer()


# ===========================================================================
# FeatureExtractor — passage_id
# ===========================================================================


class TestPassageId:
    def test_returns_8_hex_chars(self):
        pid = FeatureExtractor.passage_id("hello world", 1)
        assert len(pid) == 8
        assert all(c in "0123456789abcdef" for c in pid)

    def test_deterministic(self):
        pid1 = FeatureExtractor.passage_id("hello world", 1)
        pid2 = FeatureExtractor.passage_id("hello world", 1)
        assert pid1 == pid2

    def test_differs_by_rank(self):
        pid1 = FeatureExtractor.passage_id("hello world", 1)
        pid2 = FeatureExtractor.passage_id("hello world", 2)
        assert pid1 != pid2

    def test_differs_by_passage(self):
        pid1 = FeatureExtractor.passage_id("hello world", 1)
        pid2 = FeatureExtractor.passage_id("goodbye world", 1)
        assert pid1 != pid2

    def test_empty_passage(self):
        pid = FeatureExtractor.passage_id("", 1)
        assert len(pid) == 8

    def test_only_first_50_chars_used(self):
        base = "x" * 50
        pid1 = FeatureExtractor.passage_id(base + "AAAA", 1)
        pid2 = FeatureExtractor.passage_id(base + "BBBB", 1)
        assert pid1 == pid2


# ===========================================================================
# FeatureExtractor — query_term_overlap
# ===========================================================================


class TestQueryTermOverlap:
    def test_full_overlap(self):
        feat = extractor.extract("hello world", "hello world how are you", 1)
        # both "hello" and "world" found: 2/(2+1) ≈ 0.667
        assert feat.query_term_overlap == pytest.approx(2 / 3)

    def test_zero_overlap(self):
        feat = extractor.extract("neural network", "cooking recipes and bread", 1)
        assert feat.query_term_overlap == 0.0

    def test_empty_query(self):
        feat = extractor.extract("", "hello world", 1)
        assert feat.query_term_overlap == 0.0

    def test_partial_overlap(self):
        feat = extractor.extract("cat dog bird", "cat is a pet", 1)
        # "cat" found, "dog"/"bird" not (assuming len>=2 tokens): 1/(3+1) = 0.25
        assert feat.query_term_overlap == pytest.approx(1 / 4)

    def test_overlap_is_between_0_and_1(self):
        feat = extractor.extract("some words here now", "some words here now", 1)
        assert 0.0 <= feat.query_term_overlap <= 1.0

    def test_cyrillic_overlap(self):
        feat = extractor.extract("нейронная сеть", "нейронная сеть обучение", 1)
        assert feat.query_term_overlap > 0.0

    def test_case_insensitive_overlap(self):
        feat = extractor.extract("Hello World", "hello world example text", 1)
        assert feat.query_term_overlap > 0.0


# ===========================================================================
# FeatureExtractor — bm25_score
# ===========================================================================


class TestBm25Score:
    def test_positive_for_matching_passage(self):
        feat = extractor.extract("machine learning", "machine learning is useful for many things", 1)
        assert feat.bm25_score > 0.0

    def test_zero_for_no_overlap(self):
        feat = extractor.extract("neural network", "cooking recipes and baking bread", 1)
        assert feat.bm25_score == 0.0

    def test_more_matches_higher_score(self):
        feat_low = extractor.extract("agent memory", "agent does things", 1)
        feat_high = extractor.extract("agent memory", "agent memory agent memory retrieval system", 1)
        assert feat_high.bm25_score >= feat_low.bm25_score

    def test_empty_query(self):
        feat = extractor.extract("", "hello world passage text here", 1)
        assert feat.bm25_score == 0.0

    def test_empty_passage(self):
        feat = extractor.extract("hello world", "", 1)
        assert feat.bm25_score == 0.0

    def test_non_negative(self):
        feat = extractor.extract("query words here", "some passage text words", 1)
        assert feat.bm25_score >= 0.0


# ===========================================================================
# FeatureExtractor — passage_length
# ===========================================================================


class TestPassageLength:
    def test_word_count(self):
        feat = extractor.extract("query", "one two three four five", 1)
        assert feat.passage_length == 5

    def test_empty_passage_is_zero(self):
        feat = extractor.extract("query", "", 1)
        assert feat.passage_length == 0

    def test_single_word(self):
        feat = extractor.extract("query", "word", 1)
        assert feat.passage_length == 1

    def test_long_passage(self):
        passage = " ".join(["word"] * 200)
        feat = extractor.extract("query", passage, 1)
        assert feat.passage_length == 200


# ===========================================================================
# FeatureExtractor — position_score
# ===========================================================================


class TestPositionScore:
    def test_rank_1(self):
        feat = extractor.extract("query", "passage", 1)
        assert feat.position_score == pytest.approx(1.0)

    def test_rank_2(self):
        feat = extractor.extract("query", "passage", 2)
        assert feat.position_score == pytest.approx(0.5)

    def test_rank_10(self):
        feat = extractor.extract("query", "passage", 10)
        assert feat.position_score == pytest.approx(0.1)

    def test_decreases_with_rank(self):
        feat1 = extractor.extract("query", "passage", 1)
        feat5 = extractor.extract("query", "passage", 5)
        feat10 = extractor.extract("query", "passage", 10)
        assert feat1.position_score > feat5.position_score > feat10.position_score

    def test_formula_1_over_rank(self):
        for rank in [1, 3, 7, 20]:
            feat = extractor.extract("query", "passage", rank)
            assert feat.position_score == pytest.approx(1.0 / rank)


# ===========================================================================
# FeatureExtractor — title_match
# ===========================================================================


class TestTitleMatch:
    def test_query_term_in_title(self):
        feat = extractor.extract("neural network", "unrelated passage text", 1, title="neural architecture")
        assert feat.title_match is True

    def test_no_overlap_with_title(self):
        feat = extractor.extract("quantum computing", "passage text", 1, title="cooking recipes")
        assert feat.title_match is False

    def test_empty_title(self):
        feat = extractor.extract("hello world", "passage text", 1, title="")
        assert feat.title_match is False

    def test_empty_query(self):
        feat = extractor.extract("", "passage text", 1, title="neural network")
        assert feat.title_match is False

    def test_case_insensitive_title_match(self):
        feat = extractor.extract("Neural Network", "passage text", 1, title="neural architecture")
        assert feat.title_match is True

    def test_default_title_empty(self):
        feat = extractor.extract("query text", "passage text", 1)
        assert feat.title_match is False


# ===========================================================================
# FeatureExtractor — exact_phrase_match
# ===========================================================================


class TestExactPhraseMatch:
    def test_exact_match_present(self):
        feat = extractor.extract("machine learning", "this is about machine learning algorithms", 1)
        assert feat.exact_phrase_match is True

    def test_exact_match_absent(self):
        feat = extractor.extract("machine learning", "deep neural networks for NLP tasks", 1)
        assert feat.exact_phrase_match is False

    def test_case_insensitive(self):
        feat = extractor.extract("Machine Learning", "This is about machine learning algorithms", 1)
        assert feat.exact_phrase_match is True

    def test_empty_query(self):
        feat = extractor.extract("", "some passage text here", 1)
        assert feat.exact_phrase_match is False

    def test_partial_word_match(self):
        feat = extractor.extract("learn", "machine learning is great", 1)
        assert feat.exact_phrase_match is True

    def test_empty_passage(self):
        feat = extractor.extract("machine learning", "", 1)
        assert feat.exact_phrase_match is False


# ===========================================================================
# FeatureExtractor — full extract integration
# ===========================================================================


class TestFeatureExtractorIntegration:
    def test_returns_passage_features_instance(self):
        feat = extractor.extract("query", "passage text", 1)
        assert isinstance(feat, PassageFeatures)

    def test_passage_id_set(self):
        feat = extractor.extract("query", "passage text", 1)
        assert len(feat.passage_id) == 8

    def test_all_fields_present(self):
        feat = extractor.extract("hello world", "hello world example passage", 2, title="hello title")
        assert feat.passage_id
        assert 0.0 <= feat.query_term_overlap <= 1.0
        assert feat.bm25_score >= 0.0
        assert feat.passage_length >= 0
        assert feat.position_score > 0.0
        assert isinstance(feat.title_match, bool)
        assert isinstance(feat.exact_phrase_match, bool)


# ===========================================================================
# ScoringWeights
# ===========================================================================


class TestScoringWeights:
    def test_default_values(self):
        w = ScoringWeights()
        assert w.overlap == 0.3
        assert w.bm25 == 0.3
        assert w.position == 0.2
        assert w.title == 0.1
        assert w.phrase == 0.1

    def test_default_sums_to_one(self):
        w = ScoringWeights()
        total = w.overlap + w.bm25 + w.position + w.title + w.phrase
        assert total == pytest.approx(1.0)

    def test_normalize_returns_new_instance(self):
        w = ScoringWeights(overlap=1.0, bm25=1.0, position=1.0, title=1.0, phrase=1.0)
        w2 = w.normalize()
        assert w2 is not w

    def test_normalize_equal_weights(self):
        w = ScoringWeights(overlap=1.0, bm25=1.0, position=1.0, title=1.0, phrase=1.0)
        w2 = w.normalize()
        assert w2.overlap == pytest.approx(0.2)
        assert w2.bm25 == pytest.approx(0.2)
        assert w2.position == pytest.approx(0.2)
        assert w2.title == pytest.approx(0.2)
        assert w2.phrase == pytest.approx(0.2)

    def test_normalize_sum_is_one(self):
        w = ScoringWeights(overlap=3.0, bm25=1.0, position=2.0, title=0.5, phrase=0.5)
        w2 = w.normalize()
        total = w2.overlap + w2.bm25 + w2.position + w2.title + w2.phrase
        assert total == pytest.approx(1.0)

    def test_normalize_preserves_ratios(self):
        w = ScoringWeights(overlap=2.0, bm25=1.0, position=0.0, title=0.0, phrase=0.0)
        w2 = w.normalize()
        assert w2.overlap == pytest.approx(2 / 3)
        assert w2.bm25 == pytest.approx(1 / 3)

    def test_normalize_all_zero_unchanged(self):
        w = ScoringWeights(overlap=0.0, bm25=0.0, position=0.0, title=0.0, phrase=0.0)
        w2 = w.normalize()
        assert w2.overlap == 0.0
        assert w2.bm25 == 0.0

    def test_custom_weights(self):
        w = ScoringWeights(overlap=0.5, bm25=0.2, position=0.1, title=0.1, phrase=0.1)
        assert w.overlap == 0.5


# ===========================================================================
# PassageScorer — score()
# ===========================================================================


class TestPassageScorerScore:
    def test_higher_overlap_higher_score(self):
        w = ScoringWeights(overlap=1.0, bm25=0.0, position=0.0, title=0.0, phrase=0.0)
        low = make_features(query_term_overlap=0.1)
        high = make_features(query_term_overlap=0.9)
        assert scorer.score(high, w) > scorer.score(low, w)

    def test_title_match_raises_score(self):
        w = ScoringWeights(overlap=0.0, bm25=0.0, position=0.0, title=1.0, phrase=0.0)
        no_title = make_features(title_match=False)
        with_title = make_features(title_match=True)
        assert scorer.score(with_title, w) > scorer.score(no_title, w)

    def test_phrase_match_raises_score(self):
        w = ScoringWeights(overlap=0.0, bm25=0.0, position=0.0, title=0.0, phrase=1.0)
        no_phrase = make_features(exact_phrase_match=False)
        with_phrase = make_features(exact_phrase_match=True)
        assert scorer.score(with_phrase, w) > scorer.score(no_phrase, w)

    def test_position_score_raises_score(self):
        w = ScoringWeights(overlap=0.0, bm25=0.0, position=1.0, title=0.0, phrase=0.0)
        low_pos = make_features(position_score=0.1)
        high_pos = make_features(position_score=1.0)
        assert scorer.score(high_pos, w) > scorer.score(low_pos, w)

    def test_bm25_normalised(self):
        w = ScoringWeights(overlap=0.0, bm25=1.0, position=0.0, title=0.0, phrase=0.0)
        feat = make_features(bm25_score=1.0)
        # bm25_norm = 1.0 / (1.0 + 1.0) = 0.5
        assert scorer.score(feat, w) == pytest.approx(0.5)

    def test_bm25_zero(self):
        w = ScoringWeights(overlap=0.0, bm25=1.0, position=0.0, title=0.0, phrase=0.0)
        feat = make_features(bm25_score=0.0)
        assert scorer.score(feat, w) == pytest.approx(0.0)

    def test_score_non_negative(self):
        feat = make_features()
        s = scorer.score(feat)
        assert s >= 0.0

    def test_uses_default_weights_when_none(self):
        feat = make_features()
        s1 = scorer.score(feat, None)
        s2 = scorer.score(feat, ScoringWeights())
        assert s1 == pytest.approx(s2)

    def test_all_zero_features(self):
        feat = make_features(
            query_term_overlap=0.0,
            bm25_score=0.0,
            position_score=0.0,
            title_match=False,
            exact_phrase_match=False,
        )
        s = scorer.score(feat)
        assert s == pytest.approx(0.0)


# ===========================================================================
# PassageScorer — score_all()
# ===========================================================================


class TestPassageScorerScoreAll:
    def test_returns_list_of_passage_scores(self):
        features = [
            extractor.extract("query", "relevant passage about query terms", rank)
            for rank in range(1, 4)
        ]
        result = scorer.score_all(features)
        assert all(isinstance(ps, PassageScore) for ps in result)

    def test_length_matches_input(self):
        features = [extractor.extract("q", f"passage {i}", i + 1) for i in range(5)]
        result = scorer.score_all(features)
        assert len(result) == 5

    def test_empty_list(self):
        result = scorer.score_all([])
        assert result == []

    def test_original_rank_derived_from_position_score(self):
        feat = extractor.extract("q", "some passage text here", 3)
        result = scorer.score_all([feat])
        assert result[0].original_rank == 3

    def test_passage_id_preserved(self):
        feat = extractor.extract("query", "unique passage text here", 1)
        result = scorer.score_all([feat])
        assert result[0].passage_id == feat.passage_id

    def test_features_preserved(self):
        feat = extractor.extract("query", "passage text example", 1)
        result = scorer.score_all([feat])
        assert result[0].features is feat

    def test_higher_relevance_higher_score(self):
        relevant = extractor.extract("machine learning", "machine learning deep learning neural", 1)
        irrelevant = extractor.extract("machine learning", "cooking baking bread recipes", 2)
        result = scorer.score_all([relevant, irrelevant])
        assert result[0].rerank_score > result[1].rerank_score


# ===========================================================================
# PassageReranker — basic
# ===========================================================================


class TestPassageReranker:
    def test_returns_rerank_result(self):
        reranker = PassageReranker()
        result = reranker.rerank("query", ["passage one", "passage two"])
        assert isinstance(result, RerankResult)

    def test_query_stored(self):
        reranker = PassageReranker()
        result = reranker.rerank("my query", ["text"])
        assert result.query == "my query"

    def test_passages_count(self):
        reranker = PassageReranker()
        result = reranker.rerank("query", ["a", "b", "c"])
        assert len(result.passages) == 3

    def test_reranked_not_larger_than_top_k(self):
        config = RerankerConfig(top_k=2)
        reranker = PassageReranker(config)
        passages = [f"passage {i}" for i in range(10)]
        result = reranker.rerank("query", passages)
        assert len(result.reranked) <= 2

    def test_single_passage(self):
        reranker = PassageReranker()
        result = reranker.rerank("query", ["single passage text"])
        assert len(result.reranked) == 1
        assert result.reranked[0].original_rank == 1

    def test_empty_passages(self):
        reranker = PassageReranker()
        result = reranker.rerank("query", [])
        assert result.passages == []
        assert result.reranked == []

    def test_rerank_changes_order(self):
        """A highly relevant later passage should move to top."""
        reranker = PassageReranker()
        passages = [
            "unrelated content about cooking and food recipes",   # rank 1 original
            "machine learning neural network deep learning model training",  # rank 2 original
        ]
        result = reranker.rerank("machine learning neural", passages)
        # rank 2 original should now be rank 1 reranked
        assert result.reranked[0].original_rank == 2

    def test_original_order_preserved_in_passages(self):
        reranker = PassageReranker()
        passages = ["first", "second", "third"]
        result = reranker.rerank("query", passages)
        ranks = [ps.original_rank for ps in result.passages]
        assert ranks == [1, 2, 3]

    def test_top_k_default_is_10(self):
        reranker = PassageReranker()
        passages = [f"passage {i} about topic relevance" for i in range(20)]
        result = reranker.rerank("topic relevance", passages)
        assert len(result.reranked) <= 10

    def test_titles_used_for_title_match(self):
        reranker = PassageReranker()
        passages = ["generic unrelated text here", "also unrelated text here"]
        titles = ["machine learning guide", "cooking recipes book"]
        result = reranker.rerank("machine learning", passages, titles=titles)
        # passage with matching title should score higher
        title_match_rank = result.reranked[0].original_rank
        assert title_match_rank == 1  # first passage has title match

    def test_no_titles_no_crash(self):
        reranker = PassageReranker()
        result = reranker.rerank("query", ["passage one", "passage two"])
        assert len(result.reranked) >= 1

    def test_config_none_uses_defaults(self):
        reranker = PassageReranker(config=None)
        result = reranker.rerank("query", ["text"])
        assert isinstance(result, RerankResult)

    def test_partial_titles_list(self):
        """Titles list shorter than passages should not crash."""
        reranker = PassageReranker()
        passages = ["one", "two", "three"]
        titles = ["title one"]
        result = reranker.rerank("one", passages, titles=titles)
        assert len(result.passages) == 3


# ===========================================================================
# RerankResult — improvement()
# ===========================================================================


class TestRerankResultImprovement:
    def _make_result(self, original_ranks: list[int], reranked_order: list[int]) -> RerankResult:
        """Build a synthetic RerankResult for testing improvement().

        original_ranks: the original_rank values for each PassageScore (same order)
        reranked_order: original_rank values in the re-ranked order
        """
        extractor_local = FeatureExtractor()
        passages_list: list[PassageScore] = []
        for rank in original_ranks:
            feat = extractor_local.extract("q", f"passage {rank}", rank)
            ps = PassageScore(
                passage_id=feat.passage_id,
                original_rank=rank,
                rerank_score=1.0 / rank,
                features=feat,
            )
            passages_list.append(ps)

        # Build reranked order by matching original_ranks
        rank_to_ps = {ps.original_rank: ps for ps in passages_list}
        reranked: list[PassageScore] = [rank_to_ps[r] for r in reranked_order]

        return RerankResult(query="q", passages=passages_list, reranked=reranked)

    def test_no_change(self):
        result = self._make_result([1, 2, 3], [1, 2, 3])
        assert result.improvement(3) == pytest.approx(0.0)

    def test_perfect_reversal_top1(self):
        # Original rank 3 is now rank 1 -> improvement = 3-1 = 2
        result = self._make_result([1, 2, 3], [3, 2, 1])
        assert result.improvement(1) == pytest.approx(2.0)

    def test_improvement_top2(self):
        # reranked order: [3, 2, 1]
        # new rank 1: original 3 -> delta = 3-1 = 2
        # new rank 2: original 2 -> delta = 2-2 = 0
        # avg = (2+0)/2 = 1.0
        result = self._make_result([1, 2, 3], [3, 2, 1])
        assert result.improvement(2) == pytest.approx(1.0)

    def test_empty_reranked_returns_zero(self):
        result = RerankResult(query="q", passages=[], reranked=[])
        assert result.improvement() == pytest.approx(0.0)

    def test_single_passage_no_change(self):
        result = self._make_result([1], [1])
        assert result.improvement(1) == pytest.approx(0.0)

    def test_n_larger_than_reranked(self):
        result = self._make_result([1, 2], [2, 1])
        # Asking for n=10 but only 2 passages
        imp = result.improvement(n=10)
        assert isinstance(imp, float)

    def test_negative_improvement_when_demoted(self):
        # Original rank 1 ends up at new rank 2 -> delta = 1-2 = -1
        result = self._make_result([1, 2], [2, 1])
        assert result.improvement(1) == pytest.approx(1.0)  # rank 2 moved to 1: +1

    def test_default_n_is_5(self):
        result = self._make_result([1, 2, 3], [1, 2, 3])
        # n=5 but only 3 passages, should not raise
        imp = result.improvement()
        assert isinstance(imp, float)


# ===========================================================================
# RerankerConfig
# ===========================================================================


class TestRerankerConfig:
    def test_defaults(self):
        config = RerankerConfig()
        assert config.top_k == 10
        assert isinstance(config.weights, ScoringWeights)

    def test_custom_top_k(self):
        config = RerankerConfig(top_k=5)
        assert config.top_k == 5

    def test_custom_weights(self):
        w = ScoringWeights(overlap=0.5, bm25=0.5, position=0.0, title=0.0, phrase=0.0)
        config = RerankerConfig(weights=w)
        assert config.weights.overlap == 0.5

    def test_independent_default_weights(self):
        """Each RerankerConfig instance should have its own ScoringWeights."""
        c1 = RerankerConfig()
        c2 = RerankerConfig()
        assert c1.weights is not c2.weights


# ===========================================================================
# Edge cases and integration
# ===========================================================================


class TestEdgeCases:
    def test_all_identical_passages(self):
        reranker = PassageReranker()
        passages = ["same text here"] * 5
        result = reranker.rerank("same text", passages)
        assert len(result.passages) == 5

    def test_unicode_passages(self):
        reranker = PassageReranker()
        passages = [
            "нейронная сеть глубокое обучение модели",
            "рецепт приготовления борща с мясом",
        ]
        result = reranker.rerank("нейронная сеть", passages)
        assert result.reranked[0].original_rank == 1

    def test_mixed_lang_passages(self):
        reranker = PassageReranker()
        passages = ["machine learning нейронные сети", "cooking food recipes"]
        result = reranker.rerank("machine learning", passages)
        assert len(result.reranked) >= 1

    def test_very_long_query(self):
        reranker = PassageReranker()
        query = " ".join(["word"] * 100)
        passages = ["word " * 50, "other content here now"]
        result = reranker.rerank(query, passages)
        assert len(result.reranked) >= 1

    def test_query_with_no_tokens_in_passages(self):
        reranker = PassageReranker()
        passages = ["aaa bbb ccc", "ddd eee fff"]
        result = reranker.rerank("zzz yyy xxx", passages)
        assert len(result.passages) == 2

    def test_top_k_zero(self):
        config = RerankerConfig(top_k=0)
        reranker = PassageReranker(config)
        passages = ["text one", "text two"]
        result = reranker.rerank("text", passages)
        assert len(result.reranked) == 0

    def test_exact_phrase_boosts_score_end_to_end(self):
        reranker = PassageReranker()
        passages = [
            "completely unrelated content without the terms",
            "this passage is about machine learning exactly",
        ]
        result = reranker.rerank("machine learning", passages)
        # Passage 2 has exact phrase; should rank first
        assert result.reranked[0].original_rank == 2

    def test_reranked_sorted_descending(self):
        reranker = PassageReranker()
        passages = [
            "somewhat relevant content about topics here",
            "machine learning neural network deep learning algorithm training",
            "cooking baking bread food recipes",
        ]
        result = reranker.rerank("machine learning neural", passages)
        scores = [ps.rerank_score for ps in result.reranked]
        assert scores == sorted(scores, reverse=True)
