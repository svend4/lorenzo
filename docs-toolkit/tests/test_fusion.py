"""Tests for docstoolkit.fusion — learned retrieval fusion module."""
import json
import math
import tempfile
from pathlib import Path

import pytest

from docstoolkit.fusion import (
    FusionFeatures,
    extract_features,
    LearnedFusion,
    FusionWeights,
    FusedRetriever,
    rrf_fusion,
)
from docstoolkit.fusion.model import _sigmoid, _dot


# ---------------------------------------------------------------------------
# FusionFeatures — fields and defaults
# ---------------------------------------------------------------------------

class TestFusionFeaturesDefaults:
    def test_default_bm25_score(self):
        f = FusionFeatures()
        assert f.bm25_score == 0.0

    def test_default_dense_score(self):
        f = FusionFeatures()
        assert f.dense_score == 0.0

    def test_default_graph_score(self):
        f = FusionFeatures()
        assert f.graph_score == 0.0

    def test_default_query_length(self):
        f = FusionFeatures()
        assert f.query_length == 0

    def test_default_passage_length(self):
        f = FusionFeatures()
        assert f.passage_length == 0

    def test_default_intent(self):
        f = FusionFeatures()
        assert f.intent == ""

    def test_custom_values(self):
        f = FusionFeatures(bm25_score=0.8, dense_score=0.5, graph_score=0.3,
                           query_length=10, passage_length=200, intent="factoid")
        assert f.bm25_score == 0.8
        assert f.dense_score == 0.5
        assert f.graph_score == 0.3
        assert f.query_length == 10
        assert f.passage_length == 200
        assert f.intent == "factoid"


class TestFusionFeaturesToVector:
    def test_returns_list(self):
        f = FusionFeatures()
        v = f.to_vector()
        assert isinstance(v, list)

    def test_returns_5_floats(self):
        f = FusionFeatures(bm25_score=0.5, dense_score=0.3, graph_score=0.2,
                           query_length=25, passage_length=250)
        v = f.to_vector()
        assert len(v) == 5
        for x in v:
            assert isinstance(x, float)

    def test_query_length_normalized_exactly_50(self):
        f = FusionFeatures(query_length=50)
        v = f.to_vector()
        assert v[3] == pytest.approx(1.0)

    def test_query_length_clipped_above_50(self):
        f = FusionFeatures(query_length=100)
        v = f.to_vector()
        assert v[3] == pytest.approx(1.0)

    def test_query_length_half(self):
        f = FusionFeatures(query_length=25)
        v = f.to_vector()
        assert v[3] == pytest.approx(0.5)

    def test_query_length_zero(self):
        f = FusionFeatures(query_length=0)
        v = f.to_vector()
        assert v[3] == pytest.approx(0.0)

    def test_passage_length_normalized_exactly_500(self):
        f = FusionFeatures(passage_length=500)
        v = f.to_vector()
        assert v[4] == pytest.approx(1.0)

    def test_passage_length_clipped_above_500(self):
        f = FusionFeatures(passage_length=1000)
        v = f.to_vector()
        assert v[4] == pytest.approx(1.0)

    def test_passage_length_half(self):
        f = FusionFeatures(passage_length=250)
        v = f.to_vector()
        assert v[4] == pytest.approx(0.5)

    def test_passage_length_zero(self):
        f = FusionFeatures(passage_length=0)
        v = f.to_vector()
        assert v[4] == pytest.approx(0.0)

    def test_scores_in_vector(self):
        f = FusionFeatures(bm25_score=0.7, dense_score=0.4, graph_score=0.1)
        v = f.to_vector()
        assert v[0] == pytest.approx(0.7)
        assert v[1] == pytest.approx(0.4)
        assert v[2] == pytest.approx(0.1)

    def test_intent_not_in_vector(self):
        # intent is categorical, must NOT appear in the numeric vector
        f = FusionFeatures(intent="factoid")
        v = f.to_vector()
        assert len(v) == 5  # no extra element for intent


class TestExtractFeatures:
    def test_returns_fusion_features(self):
        f = extract_features("hello world", "some passage text")
        assert isinstance(f, FusionFeatures)

    def test_query_length_from_string(self):
        query = "hello"
        f = extract_features(query, "passage")
        assert f.query_length == len(query)

    def test_passage_length_from_string(self):
        passage = "a" * 300
        f = extract_features("query", passage)
        assert f.passage_length == 300

    def test_scores_forwarded(self):
        f = extract_features("q", "p", bm25_score=0.9, dense_score=0.6, graph_score=0.3)
        assert f.bm25_score == pytest.approx(0.9)
        assert f.dense_score == pytest.approx(0.6)
        assert f.graph_score == pytest.approx(0.3)

    def test_intent_forwarded(self):
        f = extract_features("q", "p", intent="comparison")
        assert f.intent == "comparison"

    def test_empty_strings(self):
        f = extract_features("", "")
        assert f.query_length == 0
        assert f.passage_length == 0


# ---------------------------------------------------------------------------
# _sigmoid helper
# ---------------------------------------------------------------------------

class TestSigmoid:
    def test_zero(self):
        assert _sigmoid(0) == pytest.approx(0.5)

    def test_large_positive(self):
        assert _sigmoid(100) == pytest.approx(1.0, abs=1e-10)

    def test_large_negative(self):
        assert _sigmoid(-100) == pytest.approx(0.0, abs=1e-10)

    def test_output_in_range(self):
        for x in [-10, -1, 0, 1, 10]:
            s = _sigmoid(x)
            assert 0.0 <= s <= 1.0

    def test_monotone_increasing(self):
        values = [_sigmoid(x) for x in [-5, -2, 0, 2, 5]]
        for i in range(len(values) - 1):
            assert values[i] < values[i + 1]


# ---------------------------------------------------------------------------
# LearnedFusion
# ---------------------------------------------------------------------------

class TestLearnedFusionInit:
    def test_weights_length_default(self):
        model = LearnedFusion()
        assert len(model._weights) == 5

    def test_weights_length_custom(self):
        model = LearnedFusion(n_features=3)
        assert len(model._weights) == 3

    def test_bias_zero_at_init(self):
        model = LearnedFusion()
        assert model._bias == 0.0

    def test_score_returns_float_in_range(self):
        model = LearnedFusion()
        f = FusionFeatures(bm25_score=0.5, dense_score=0.3, graph_score=0.2,
                           query_length=20, passage_length=100)
        s = model.score(f)
        assert isinstance(s, float)
        assert 0.0 <= s <= 1.0


class TestLearnedFusionFit:
    def _make_separable_data(self):
        """Create clearly separable training examples."""
        pos = FusionFeatures(bm25_score=0.9, dense_score=0.9, graph_score=0.9,
                             query_length=10, passage_length=100)
        neg = FusionFeatures(bm25_score=0.1, dense_score=0.1, graph_score=0.1,
                             query_length=10, passage_length=100)
        data = [(pos, True)] * 30 + [(neg, False)] * 30
        return data, pos, neg

    def test_fit_returns_fusion_weights(self):
        model = LearnedFusion()
        data, _, _ = self._make_separable_data()
        result = model.fit(data)
        assert isinstance(result, FusionWeights)

    def test_n_training_examples_in_weights(self):
        model = LearnedFusion()
        data, _, _ = self._make_separable_data()
        result = model.fit(data)
        assert result.n_training_examples == len(data)

    def test_fit_separable_data(self):
        model = LearnedFusion(lr=0.5)
        data, pos, neg = self._make_separable_data()
        model.fit(data, epochs=50)
        assert model.score(pos) > model.score(neg)

    def test_accuracy_in_weights(self):
        model = LearnedFusion(lr=0.5)
        data, _, _ = self._make_separable_data()
        result = model.fit(data, epochs=50)
        assert 0.0 <= result.accuracy <= 1.0

    def test_accuracy_high_on_separable(self):
        model = LearnedFusion(lr=0.5)
        data, _, _ = self._make_separable_data()
        result = model.fit(data, epochs=50)
        assert result.accuracy > 0.8


class TestLearnedFusionExplain:
    def test_explain_returns_dict(self):
        model = LearnedFusion()
        f = FusionFeatures(bm25_score=0.5)
        result = model.explain(f)
        assert isinstance(result, dict)

    def test_explain_has_5_keys(self):
        model = LearnedFusion()
        f = FusionFeatures(bm25_score=0.5, dense_score=0.3, graph_score=0.1,
                           query_length=10, passage_length=100)
        result = model.explain(f)
        assert len(result) == 5

    def test_explain_expected_keys(self):
        model = LearnedFusion()
        f = FusionFeatures()
        result = model.explain(f)
        assert set(result.keys()) == {"bm25", "dense", "graph", "query_len", "passage_len"}


class TestLearnedFusionSaveLoad:
    def test_save_load_roundtrip(self, tmp_path):
        model = LearnedFusion(lr=0.5)
        data = [
            (FusionFeatures(bm25_score=0.9, dense_score=0.9, graph_score=0.9,
                            query_length=10, passage_length=100), True),
            (FusionFeatures(bm25_score=0.1, dense_score=0.1, graph_score=0.1,
                            query_length=10, passage_length=100), False),
        ] * 20
        model.fit(data, epochs=30)

        path = tmp_path / "fusion_weights.json"
        model.save(path)

        loaded = LearnedFusion.load(path)
        test_f = FusionFeatures(bm25_score=0.5, dense_score=0.5, graph_score=0.5,
                                query_length=20, passage_length=200)
        assert model.score(test_f) == pytest.approx(loaded.score(test_f))

    def test_save_creates_json_file(self, tmp_path):
        model = LearnedFusion()
        path = tmp_path / "weights.json"
        model.save(path)
        assert path.exists()
        data = json.loads(path.read_text())
        assert "weights" in data
        assert "bias" in data


class TestWeightsSnapshot:
    def test_weights_snapshot_returns_fusion_weights(self):
        model = LearnedFusion()
        snap = model.weights_snapshot()
        assert isinstance(snap, FusionWeights)

    def test_weights_snapshot_has_correct_length(self):
        model = LearnedFusion(n_features=5)
        snap = model.weights_snapshot()
        assert len(snap.weights) == 5


# ---------------------------------------------------------------------------
# FusionWeights dataclass
# ---------------------------------------------------------------------------

class TestFusionWeights:
    def test_has_weights_field(self):
        fw = FusionWeights(weights=[0.1, 0.2, 0.3, 0.4, 0.5])
        assert len(fw.weights) == 5

    def test_has_bias_field(self):
        fw = FusionWeights(weights=[0.0] * 5, bias=0.5)
        assert fw.bias == pytest.approx(0.5)

    def test_has_n_training_examples_field(self):
        fw = FusionWeights(weights=[0.0] * 5, n_training_examples=100)
        assert fw.n_training_examples == 100

    def test_has_accuracy_field(self):
        fw = FusionWeights(weights=[0.0] * 5, accuracy=0.95)
        assert fw.accuracy == pytest.approx(0.95)

    def test_default_bias_zero(self):
        fw = FusionWeights(weights=[0.0] * 5)
        assert fw.bias == 0.0

    def test_default_n_training_examples_zero(self):
        fw = FusionWeights(weights=[0.0] * 5)
        assert fw.n_training_examples == 0

    def test_default_accuracy_zero(self):
        fw = FusionWeights(weights=[0.0] * 5)
        assert fw.accuracy == 0.0


# ---------------------------------------------------------------------------
# rrf_fusion
# ---------------------------------------------------------------------------

class TestRRFFusion:
    def test_empty_input(self):
        result = rrf_fusion([])
        assert result == []

    def test_single_list_score_formula(self):
        result = rrf_fusion([["a", "b", "c"]], k=60)
        result_dict = dict(result)
        assert result_dict["a"] == pytest.approx(1.0 / (60 + 1))
        assert result_dict["b"] == pytest.approx(1.0 / (60 + 2))
        assert result_dict["c"] == pytest.approx(1.0 / (60 + 3))

    def test_two_lists_scores_summed(self):
        # "a" appears rank 1 in both lists
        result = rrf_fusion([["a", "b"], ["a", "c"]], k=60)
        result_dict = dict(result)
        expected_a = 1.0 / (60 + 1) + 1.0 / (60 + 1)
        assert result_dict["a"] == pytest.approx(expected_a)

    def test_sorted_descending(self):
        result = rrf_fusion([["a", "b", "c"]])
        scores = [s for _, s in result]
        assert scores == sorted(scores, reverse=True)

    def test_returns_doc_id_strings(self):
        result = rrf_fusion([["doc1", "doc2"]])
        for doc_id, score in result:
            assert isinstance(doc_id, str)
            assert isinstance(score, float)

    def test_all_items_in_result(self):
        result = rrf_fusion([["a", "b"], ["c", "d"]])
        doc_ids = {doc_id for doc_id, _ in result}
        assert doc_ids == {"a", "b", "c", "d"}

    def test_custom_k(self):
        result = rrf_fusion([["x"]], k=10)
        result_dict = dict(result)
        assert result_dict["x"] == pytest.approx(1.0 / (10 + 1))


# ---------------------------------------------------------------------------
# FusedRetriever
# ---------------------------------------------------------------------------

class TestFusedRetrieverIsTraned:
    def test_is_trained_false_without_model(self):
        r = FusedRetriever()
        assert r.is_trained() is False

    def test_is_trained_true_with_model(self):
        model = LearnedFusion()
        r = FusedRetriever(fusion_model=model)
        assert r.is_trained() is True


class TestFusedRetrieverScorePassages:
    def _candidates(self):
        return [
            {"text": "first passage", "doc_id": "doc1", "bm25": 0.9, "dense": 0.5, "graph": 0.3},
            {"text": "second passage", "doc_id": "doc2", "bm25": 0.6, "dense": 0.8, "graph": 0.4},
            {"text": "third passage", "doc_id": "doc3", "bm25": 0.3, "dense": 0.2, "graph": 0.9},
        ]

    def test_no_model_fallback_rrf(self):
        r = FusedRetriever(fallback_to_rrf=True)
        result = r.score_passages("test query", self._candidates())
        assert len(result) > 0
        for doc_id, score in result:
            assert isinstance(doc_id, str)
            assert isinstance(score, float)

    def test_no_model_no_fallback_sorts_by_bm25(self):
        r = FusedRetriever(fallback_to_rrf=False)
        result = r.score_passages("test query", self._candidates())
        scores = [s for _, s in result]
        assert scores == sorted(scores, reverse=True)
        # top should be doc1 (highest bm25)
        assert result[0][0] == "doc1"

    def test_with_trained_model_uses_fusion_scores(self):
        # Train a model
        model = LearnedFusion(lr=0.5)
        pos = FusionFeatures(bm25_score=0.9, dense_score=0.5, graph_score=0.3,
                             query_length=10, passage_length=13)
        neg = FusionFeatures(bm25_score=0.3, dense_score=0.2, graph_score=0.9,
                             query_length=10, passage_length=12)
        data = [(pos, True)] * 30 + [(neg, False)] * 30
        model.fit(data, epochs=30)

        r = FusedRetriever(fusion_model=model)
        result = r.score_passages("test query", self._candidates(), top_k=3)
        assert len(result) <= 3
        for doc_id, score in result:
            assert isinstance(doc_id, str)
            assert 0.0 <= score <= 1.0

    def test_returns_top_k(self):
        r = FusedRetriever(fallback_to_rrf=True)
        result = r.score_passages("query", self._candidates(), top_k=2)
        assert len(result) == 2

    def test_empty_candidates(self):
        r = FusedRetriever()
        result = r.score_passages("query", [])
        assert result == []

    def test_result_is_list_of_tuples(self):
        r = FusedRetriever(fallback_to_rrf=True)
        result = r.score_passages("query", self._candidates())
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_sorted_descending_with_rrf(self):
        r = FusedRetriever(fallback_to_rrf=True)
        result = r.score_passages("query", self._candidates())
        scores = [s for _, s in result]
        assert scores == sorted(scores, reverse=True)
