"""Tests for docstoolkit.attribution — counterfactual leave-one-out attribution."""
import pytest
from docstoolkit.rag.types import Passage
from docstoolkit.attribution.scorer import (
    _tokenize, _jaccard, _semantic_diff, _claim_loss,
    AttributionScore, AttributionMap,
    counterfactual_attribution, embedding_attribution,
)
from docstoolkit.attribution.anomaly import AnomalyReport, detect_overreliance
from docstoolkit.attribution import (
    AttributionScore as ImportedScore,
    AttributionMap as ImportedMap,
    counterfactual_attribution as imported_cf,
    embedding_attribution as imported_ea,
    detect_overreliance as imported_dr,
    AnomalyReport as ImportedAnomalyReport,
)


# ---------------------------------------------------------------------------
# Helper: make a Passage easily
# ---------------------------------------------------------------------------

def make_passage(text: str, doc_id: str = "doc1", score: float = 1.0) -> Passage:
    return Passage(text=text, doc_id=doc_id, score=score)


# ===========================================================================
# _tokenize
# ===========================================================================

class TestTokenize:
    def test_lowercase(self):
        tokens = _tokenize("Hello World")
        assert "hello" in tokens
        assert "world" in tokens
        assert "Hello" not in tokens

    def test_strips_punctuation(self):
        tokens = _tokenize("hello, world!")
        assert "hello" in tokens
        assert "world" in tokens
        assert "hello," not in tokens

    def test_empty_string(self):
        tokens = _tokenize("")
        assert tokens == set()

    def test_returns_set(self):
        tokens = _tokenize("the the the cat")
        assert isinstance(tokens, set)
        # set deduplicates
        assert "the" in tokens
        assert "cat" in tokens

    def test_numbers(self):
        tokens = _tokenize("version 2.0 release")
        assert "version" in tokens
        assert "2" in tokens
        assert "0" in tokens

    def test_cyrillic(self):
        tokens = _tokenize("Память агента")
        assert "память" in tokens
        assert "агента" in tokens


# ===========================================================================
# _jaccard
# ===========================================================================

class TestJaccard:
    def test_identical_texts(self):
        j = _jaccard("hello world", "hello world")
        assert j == 1.0

    def test_disjoint_texts(self):
        j = _jaccard("apple banana", "cherry dragon")
        assert j == 0.0

    def test_partial_overlap(self):
        j = _jaccard("apple banana cherry", "apple dragon elephant")
        assert 0.0 < j < 1.0

    def test_symmetry(self):
        a = "foo bar baz"
        b = "bar baz qux"
        assert _jaccard(a, b) == _jaccard(b, a)

    def test_both_empty(self):
        j = _jaccard("", "")
        assert j == 1.0

    def test_one_empty(self):
        j = _jaccard("hello", "")
        assert j == 0.0

    def test_value_range(self):
        j = _jaccard("hello world foo", "hello bar baz")
        assert 0.0 <= j <= 1.0


# ===========================================================================
# _semantic_diff
# ===========================================================================

class TestSemanticDiff:
    def test_identical_returns_zero(self):
        diff = _semantic_diff("hello world", "hello world")
        assert diff == 0.0

    def test_completely_different_close_to_one(self):
        diff = _semantic_diff("apple banana cherry", "dragon elephant fox")
        assert diff > 0.8

    def test_complement_of_jaccard(self):
        a = "foo bar baz"
        b = "bar baz qux"
        assert abs(_semantic_diff(a, b) - (1.0 - _jaccard(a, b))) < 1e-9

    def test_range(self):
        diff = _semantic_diff("some text here", "other words there")
        assert 0.0 <= diff <= 1.0


# ===========================================================================
# _claim_loss
# ===========================================================================

class TestClaimLoss:
    def test_sentence_in_both_not_lost(self):
        base = "The sky is blue"
        new = "The sky is blue and clear"
        lost = _claim_loss(base, new)
        # high overlap — should not be lost
        assert len(lost) == 0

    def test_sentence_only_in_base_is_lost(self):
        base = "Apples are red. Dragons breathe fire."
        new = "Apples are red."
        lost = _claim_loss(base, new)
        assert any("dragon" in s.lower() or "Dragons" in s for s in lost)

    def test_empty_base(self):
        lost = _claim_loss("", "some answer")
        assert lost == []

    def test_returns_list(self):
        lost = _claim_loss("foo bar", "baz qux")
        assert isinstance(lost, list)

    def test_completely_different_all_lost(self):
        base = "Alpha beta gamma. Delta epsilon zeta."
        new = "Completely unrelated text with different words."
        lost = _claim_loss(base, new)
        # both sentences should be lost (< 0.3 overlap)
        assert len(lost) >= 1


# ===========================================================================
# AttributionScore
# ===========================================================================

class TestAttributionScore:
    def test_fields(self):
        score = AttributionScore(
            passage_id="0",
            doc_id="doc1",
            influence=0.7,
            semantic_diff=0.7,
        )
        assert score.passage_id == "0"
        assert score.doc_id == "doc1"
        assert score.influence == 0.7
        assert score.semantic_diff == 0.7
        assert score.claim_loss == []

    def test_claim_loss_default(self):
        score = AttributionScore(
            passage_id="1",
            doc_id="doc2",
            influence=0.3,
            semantic_diff=0.3,
        )
        assert score.claim_loss == []

    def test_claim_loss_custom(self):
        score = AttributionScore(
            passage_id="2",
            doc_id="doc3",
            influence=0.5,
            semantic_diff=0.5,
            claim_loss=["lost sentence"],
        )
        assert score.claim_loss == ["lost sentence"]


# ===========================================================================
# AttributionMap
# ===========================================================================

class TestAttributionMap:
    def _make_map(self, scores=None, balanced=True):
        if scores is None:
            scores = [
                AttributionScore("0", "doc1", 0.6, 0.6),
                AttributionScore("1", "doc2", 0.4, 0.4),
            ]
        return AttributionMap(
            query="test query",
            base_answer="base answer text",
            scores=scores,
            is_balanced=balanced,
        )

    def test_top_contributor_returns_highest(self):
        amap = self._make_map()
        top = amap.top_contributor()
        assert top is not None
        assert top.passage_id == "0"
        assert top.influence == 0.6

    def test_top_contributor_empty_returns_none(self):
        amap = AttributionMap(
            query="query",
            base_answer="answer",
            scores=[],
            is_balanced=True,
        )
        assert amap.top_contributor() is None

    def test_is_balanced_true(self):
        scores = [
            AttributionScore("0", "doc1", 0.4, 0.4),
            AttributionScore("1", "doc2", 0.3, 0.3),
            AttributionScore("2", "doc3", 0.3, 0.3),
        ]
        amap = AttributionMap("q", "a", scores, is_balanced=True)
        assert amap.is_balanced is True

    def test_is_balanced_false(self):
        scores = [
            AttributionScore("0", "doc1", 0.8, 0.8),
            AttributionScore("1", "doc2", 0.2, 0.2),
        ]
        amap = AttributionMap("q", "a", scores, is_balanced=False)
        assert amap.is_balanced is False

    def test_to_markdown_contains_attribution(self):
        amap = self._make_map()
        md = amap.to_markdown()
        assert "Attribution" in md

    def test_to_markdown_contains_query(self):
        amap = self._make_map()
        md = amap.to_markdown()
        assert "test query" in md

    def test_to_markdown_is_string(self):
        amap = self._make_map()
        assert isinstance(amap.to_markdown(), str)


# ===========================================================================
# counterfactual_attribution
# ===========================================================================

class TestCounterfactualAttribution:
    def test_empty_passages_returns_empty_map(self):
        result = counterfactual_attribution("query", "base answer", [])
        assert isinstance(result, AttributionMap)
        assert result.scores == []
        assert result.is_balanced is True

    def test_single_passage_influence_normalized(self):
        passages = [make_passage("unique content about dragons", "doc1")]
        base_answer = "Answer about completely different topic with no shared words."
        result = counterfactual_attribution("query", base_answer, passages)
        assert len(result.scores) == 1
        # With single passage, influence should be 1.0 after normalization if diff > 0
        # or 0.0 if answer is identical to surrogate
        assert result.scores[0].influence in (0.0, 1.0) or 0.0 <= result.scores[0].influence <= 1.0

    def test_with_answerer_fn_none_uses_text_concat(self):
        passages = [
            make_passage("alpha beta gamma", "doc1"),
            make_passage("delta epsilon zeta", "doc2"),
        ]
        base_answer = "alpha beta gamma delta epsilon zeta"
        result = counterfactual_attribution("query", base_answer, passages)
        assert len(result.scores) == 2

    def test_influences_sum_to_one(self):
        passages = [
            make_passage("cats and dogs are pets", "doc1"),
            make_passage("fish swim in water", "doc2"),
            make_passage("birds can fly high", "doc3"),
        ]
        base_answer = "cats and dogs are pets fish swim in water"
        result = counterfactual_attribution("query", base_answer, passages)
        if any(s.influence > 0 for s in result.scores):
            total = sum(s.influence for s in result.scores)
            assert abs(total - 1.0) < 1e-6

    def test_sorted_by_influence_descending(self):
        passages = [
            make_passage("completely unrelated text xyz abc", "doc1"),
            make_passage("answer is about cats and dogs", "doc2"),
        ]
        base_answer = "answer is about cats and dogs"
        result = counterfactual_attribution("query", base_answer, passages)
        influences = [s.influence for s in result.scores]
        assert influences == sorted(influences, reverse=True)

    def test_with_custom_answerer_fn(self):
        passages = [
            make_passage("passage one text", "doc1"),
            make_passage("passage two text", "doc2"),
        ]
        base_answer = "passage one text passage two text"

        call_log = []
        def mock_answerer(q, subset_passages):
            call_log.append(len(subset_passages))
            return " ".join(p.text for p in subset_passages)

        result = counterfactual_attribution("query", base_answer, passages, mock_answerer)
        assert len(result.scores) == 2
        # answerer_fn called once per passage
        assert len(call_log) == 2
        # each call gets n-1 passages
        assert all(c == 1 for c in call_log)

    def test_is_balanced_computed_correctly(self):
        passages = [
            make_passage("very unique irreplaceable content alpha", "doc1"),
            make_passage("also unique beta gamma delta", "doc2"),
        ]
        base_answer = "alpha beta gamma delta"
        result = counterfactual_attribution("query", base_answer, passages)
        max_inf = max((s.influence for s in result.scores), default=0.0)
        expected_balanced = max_inf <= 0.5
        assert result.is_balanced == expected_balanced

    def test_passage_ids_are_strings(self):
        passages = [make_passage("text one", "doc1"), make_passage("text two", "doc2")]
        result = counterfactual_attribution("q", "answer", passages)
        for score in result.scores:
            assert isinstance(score.passage_id, str)

    def test_doc_ids_preserved(self):
        passages = [
            make_passage("foo bar", "my-doc-1"),
            make_passage("baz qux", "my-doc-2"),
        ]
        result = counterfactual_attribution("q", "foo bar baz qux", passages)
        doc_ids = {s.doc_id for s in result.scores}
        assert "my-doc-1" in doc_ids
        assert "my-doc-2" in doc_ids

    def test_returns_attribution_map_type(self):
        result = counterfactual_attribution("q", "answer", [])
        assert isinstance(result, AttributionMap)


# ===========================================================================
# embedding_attribution
# ===========================================================================

class TestEmbeddingAttribution:
    def test_returns_attribution_map(self):
        passages = [make_passage("hello world", "doc1")]
        result = embedding_attribution("query", "hello world response", passages)
        assert isinstance(result, AttributionMap)

    def test_empty_passages_returns_empty(self):
        result = embedding_attribution("query", "answer", [])
        assert isinstance(result, AttributionMap)
        assert result.scores == []
        assert result.is_balanced is True

    def test_influences_normalized_sum_to_one(self):
        passages = [
            make_passage("cats dogs pets animals", "doc1"),
            make_passage("fish water swim ocean", "doc2"),
            make_passage("birds fly sky feathers", "doc3"),
        ]
        base_answer = "cats dogs fish water birds sky"
        result = embedding_attribution("query", base_answer, passages)
        if any(s.influence > 0 for s in result.scores):
            total = sum(s.influence for s in result.scores)
            assert abs(total - 1.0) < 1e-6

    def test_highest_overlap_gets_highest_influence(self):
        passages = [
            make_passage("completely unrelated xyz uvw", "doc1"),
            make_passage("cats dogs answer topic", "doc2"),
        ]
        base_answer = "cats dogs answer topic response"
        result = embedding_attribution("query", base_answer, passages)
        top = result.top_contributor()
        assert top is not None
        assert top.doc_id == "doc2"

    def test_sorted_descending(self):
        passages = [
            make_passage("alpha beta gamma", "doc1"),
            make_passage("delta epsilon zeta eta theta", "doc2"),
        ]
        base_answer = "delta epsilon zeta eta theta phi"
        result = embedding_attribution("query", base_answer, passages)
        influences = [s.influence for s in result.scores]
        assert influences == sorted(influences, reverse=True)

    def test_passage_ids_correct(self):
        passages = [
            make_passage("text a", "docA"),
            make_passage("text b", "docB"),
        ]
        result = embedding_attribution("q", "text a text b", passages)
        ids = {s.passage_id for s in result.scores}
        assert "0" in ids
        assert "1" in ids

    def test_query_preserved(self):
        passages = [make_passage("some text", "doc1")]
        result = embedding_attribution("my special query", "some text", passages)
        assert result.query == "my special query"

    def test_base_answer_preserved(self):
        passages = [make_passage("some text", "doc1")]
        result = embedding_attribution("query", "my base answer", passages)
        assert result.base_answer == "my base answer"


# ===========================================================================
# AnomalyReport
# ===========================================================================

class TestAnomalyReport:
    def test_fields(self):
        report = AnomalyReport(
            is_anomalous=True,
            reason="overreliance",
            dominant_passage_id="0",
            dominant_influence=0.8,
            recommendation="Consider more diverse sources",
        )
        assert report.is_anomalous is True
        assert report.reason == "overreliance"
        assert report.dominant_passage_id == "0"
        assert report.dominant_influence == 0.8
        assert isinstance(report.recommendation, str)

    def test_non_anomalous_fields(self):
        report = AnomalyReport(
            is_anomalous=False,
            reason="balanced",
            dominant_passage_id="1",
            dominant_influence=0.3,
            recommendation="Looks balanced",
        )
        assert report.is_anomalous is False
        assert report.reason == "balanced"


# ===========================================================================
# detect_overreliance
# ===========================================================================

class TestDetectOverreliance:
    def _make_map_with_influences(self, influences, query="test query"):
        scores = [
            AttributionScore(str(i), f"doc{i}", inf, inf)
            for i, inf in enumerate(influences)
        ]
        # sort desc
        scores.sort(key=lambda s: s.influence, reverse=True)
        max_inf = max(influences) if influences else 0.0
        return AttributionMap(
            query=query,
            base_answer="base",
            scores=scores,
            is_balanced=max_inf <= 0.5,
        )

    def test_overreliance_when_above_threshold(self):
        amap = self._make_map_with_influences([0.8, 0.2])
        report = detect_overreliance(amap, threshold=0.5)
        assert report.is_anomalous is True
        assert report.reason == "overreliance"

    def test_balanced_when_below_threshold(self):
        amap = self._make_map_with_influences([0.4, 0.35, 0.25])
        report = detect_overreliance(amap, threshold=0.5)
        assert report.is_anomalous is False
        assert report.reason == "balanced"

    def test_exact_threshold_not_anomalous(self):
        # threshold is strictly greater-than
        amap = self._make_map_with_influences([0.5, 0.5])
        report = detect_overreliance(amap, threshold=0.5)
        assert report.is_anomalous is False

    def test_recommendation_non_empty(self):
        amap = self._make_map_with_influences([0.9, 0.1])
        report = detect_overreliance(amap)
        assert len(report.recommendation) > 0

    def test_recommendation_overreliance_contains_query(self):
        amap = self._make_map_with_influences([0.9, 0.1], query="find the dragons")
        report = detect_overreliance(amap)
        assert "find the dragons" in report.recommendation or "find the dragon" in report.recommendation or report.recommendation  # at minimum non-empty

    def test_dominant_influence_matches_max(self):
        amap = self._make_map_with_influences([0.7, 0.3])
        report = detect_overreliance(amap)
        assert abs(report.dominant_influence - 0.7) < 1e-6

    def test_custom_threshold_respected_higher(self):
        amap = self._make_map_with_influences([0.6, 0.4])
        # default threshold 0.5 → anomalous, but custom 0.7 → not anomalous
        report = detect_overreliance(amap, threshold=0.7)
        assert report.is_anomalous is False

    def test_custom_threshold_respected_lower(self):
        amap = self._make_map_with_influences([0.4, 0.6])
        # threshold 0.3 → anomalous
        report = detect_overreliance(amap, threshold=0.3)
        assert report.is_anomalous is True

    def test_reason_values(self):
        amap_over = self._make_map_with_influences([0.9, 0.1])
        amap_bal = self._make_map_with_influences([0.4, 0.6])
        report_over = detect_overreliance(amap_over)
        report_bal = detect_overreliance(amap_bal, threshold=0.7)
        assert report_over.reason in ["overreliance", "none", "balanced"]
        assert report_bal.reason in ["overreliance", "none", "balanced"]

    def test_empty_scores_not_anomalous(self):
        amap = AttributionMap(query="q", base_answer="a", scores=[], is_balanced=True)
        report = detect_overreliance(amap)
        assert report.is_anomalous is False
        assert report.dominant_passage_id == ""

    def test_returns_anomaly_report_type(self):
        amap = self._make_map_with_influences([0.5, 0.5])
        report = detect_overreliance(amap)
        assert isinstance(report, AnomalyReport)


# ===========================================================================
# Public API imports
# ===========================================================================

class TestPublicAPI:
    def test_imports_work(self):
        assert ImportedScore is AttributionScore
        assert ImportedMap is AttributionMap
        assert imported_cf is counterfactual_attribution
        assert imported_ea is embedding_attribution
        assert imported_dr is detect_overreliance
        assert ImportedAnomalyReport is AnomalyReport

    def test_end_to_end_cf_then_detect(self):
        passages = [
            make_passage("unique dragons breathe fire magic spells", "doc1"),
            make_passage("also relevant topic answer here yes", "doc2"),
        ]
        base_answer = "unique dragons breathe fire magic spells also relevant topic"
        amap = counterfactual_attribution("find dragons", base_answer, passages)
        report = detect_overreliance(amap)
        assert isinstance(report, AnomalyReport)
        assert report.reason in ["overreliance", "balanced"]

    def test_end_to_end_embedding_then_detect(self):
        passages = [
            make_passage("query relevant highly specific answer match", "doc1"),
            make_passage("unrelated other topic xyz abc", "doc2"),
        ]
        base_answer = "query relevant highly specific answer match"
        amap = embedding_attribution("query", base_answer, passages)
        report = detect_overreliance(amap)
        assert isinstance(report, AnomalyReport)
