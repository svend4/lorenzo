"""Tests for docstoolkit.doc_topic_model (E231 — lightweight topic model).

Coverage target: >= 40 tests.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.doc_topic_model import (
    DocTopicModel,
    Topic,
    TopicDoc,
    TopicModel,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

CAR_DOCS = {
    "c1": "cars and engines and wheels and tires",
    "c2": "cars are fast with engines and wheels",
    "c3": "engines and wheels and tires and cars",
}

FOOD_DOCS = {
    "f1": "food and pizza and pasta and bread",
    "f2": "pizza pasta food and bread",
    "f3": "pasta and food and bread and pizza",
}

MIXED_DOCS = {**CAR_DOCS, **FOOD_DOCS}


def make_model(**kwargs) -> DocTopicModel:
    """Return a model with permissive defaults so small corpora can fit."""
    params = dict(num_topics=2, min_term_freq=1, max_terms_per_topic=5)
    params.update(kwargs)
    return DocTopicModel(**params)


def fit_mixed() -> tuple[DocTopicModel, TopicModel]:
    m = make_model()
    return m, m.fit(MIXED_DOCS)


# ---------------------------------------------------------------------------
# Topic dataclass
# ---------------------------------------------------------------------------

class TestTopic:
    def test_construct_with_defaults(self):
        t = Topic(topic_id=0, keywords=["a", "b"])
        assert t.topic_id == 0
        assert t.keywords == ["a", "b"]
        assert t.weight == 1.0
        assert t.doc_ids == []

    def test_construct_with_all_fields(self):
        t = Topic(topic_id=3, keywords=["x"], weight=0.5, doc_ids=["d1"])
        assert t.weight == 0.5
        assert t.doc_ids == ["d1"]

    def test_doc_ids_independent_across_instances(self):
        a = Topic(topic_id=0, keywords=[])
        b = Topic(topic_id=1, keywords=[])
        a.doc_ids.append("d1")
        assert b.doc_ids == []


# ---------------------------------------------------------------------------
# TopicDoc dataclass
# ---------------------------------------------------------------------------

class TestTopicDoc:
    def test_construct(self):
        td = TopicDoc(doc_id="d1", topic_id=2, score=0.75)
        assert td.doc_id == "d1"
        assert td.topic_id == 2
        assert td.score == 0.75

    def test_score_type_is_float(self):
        td = TopicDoc(doc_id="x", topic_id=0, score=1.0)
        assert isinstance(td.score, float)


# ---------------------------------------------------------------------------
# TopicModel dataclass
# ---------------------------------------------------------------------------

class TestTopicModel:
    def test_construct(self):
        t = Topic(topic_id=0, keywords=["k"])
        tm = TopicModel(topics=[t], doc_assignments={"d1": 0}, total_terms=4, total_docs=1)
        assert tm.topics[0].topic_id == 0
        assert tm.doc_assignments == {"d1": 0}
        assert tm.total_terms == 4
        assert tm.total_docs == 1

    def test_empty(self):
        tm = TopicModel(topics=[], doc_assignments={}, total_terms=0, total_docs=0)
        assert tm.topics == []


# ---------------------------------------------------------------------------
# fit
# ---------------------------------------------------------------------------

class TestFit:
    def test_returns_topic_model(self):
        _, result = fit_mixed()
        assert isinstance(result, TopicModel)

    def test_sets_is_fitted(self):
        m, _ = fit_mixed()
        assert m.is_fitted is True

    def test_total_docs_matches_input(self):
        _, result = fit_mixed()
        assert result.total_docs == len(MIXED_DOCS)

    def test_total_terms_is_positive(self):
        _, result = fit_mixed()
        assert result.total_terms > 0

    def test_all_docs_assigned(self):
        _, result = fit_mixed()
        assert set(result.doc_assignments.keys()) == set(MIXED_DOCS.keys())

    def test_topic_ids_are_sequential(self):
        _, result = fit_mixed()
        ids = [t.topic_id for t in result.topics]
        assert ids == list(range(len(ids)))

    def test_topic_keywords_nonempty(self):
        _, result = fit_mixed()
        for t in result.topics:
            assert t.keywords, f"topic {t.topic_id} has no keywords"

    def test_topic_weight_in_range(self):
        _, result = fit_mixed()
        for t in result.topics:
            assert 0.0 <= t.weight <= 1.0

    def test_weights_sum_to_one(self):
        _, result = fit_mixed()
        total = sum(t.weight for t in result.topics)
        assert abs(total - 1.0) < 1e-6

    def test_empty_documents(self):
        m = make_model()
        result = m.fit({})
        assert result.total_docs == 0
        assert result.topics == []
        assert m.is_fitted is True


# ---------------------------------------------------------------------------
# Multiple clusters
# ---------------------------------------------------------------------------

class TestFitMultipleClusters:
    def test_separates_cars_and_food(self):
        m, result = fit_mixed()
        car_topic = m.topic_for("c1")
        food_topic = m.topic_for("f1")
        assert car_topic is not None and food_topic is not None
        assert car_topic.topic_id != food_topic.topic_id

    def test_all_car_docs_share_topic(self):
        m, _ = fit_mixed()
        topics = {m.topic_for(d).topic_id for d in CAR_DOCS}
        assert len(topics) == 1

    def test_all_food_docs_share_topic(self):
        m, _ = fit_mixed()
        topics = {m.topic_for(d).topic_id for d in FOOD_DOCS}
        assert len(topics) == 1

    def test_at_most_num_topics(self):
        m = make_model(num_topics=2)
        result = m.fit(MIXED_DOCS)
        assert len(result.topics) <= 2

    def test_single_topic_when_target_is_one(self):
        m = make_model(num_topics=1)
        result = m.fit(MIXED_DOCS)
        assert len(result.topics) == 1
        assert set(result.topics[0].doc_ids) == set(MIXED_DOCS)


# ---------------------------------------------------------------------------
# assign
# ---------------------------------------------------------------------------

class TestAssign:
    def test_returns_topicdoc(self):
        m, _ = fit_mixed()
        td = m.assign("I love pizza and pasta")
        assert isinstance(td, TopicDoc)

    def test_food_text_goes_to_food_topic(self):
        m, _ = fit_mixed()
        food_topic_id = m.topic_for("f1").topic_id
        td = m.assign("pizza and pasta and bread")
        assert td.topic_id == food_topic_id

    def test_car_text_goes_to_car_topic(self):
        m, _ = fit_mixed()
        car_topic_id = m.topic_for("c1").topic_id
        td = m.assign("cars engines wheels tires")
        assert td.topic_id == car_topic_id

    def test_empty_text_returns_none(self):
        m, _ = fit_mixed()
        assert m.assign("") is None

    def test_unfitted_returns_none(self):
        m = make_model()
        assert m.assign("anything") is None

    def test_unrelated_text_returns_none(self):
        m, _ = fit_mixed()
        # tokens not in vocab and not overlapping any keyword
        td = m.assign("xylophone quizzical Zambia")
        assert td is None

    def test_score_is_float(self):
        m, _ = fit_mixed()
        td = m.assign("pizza pasta")
        assert isinstance(td.score, float)


# ---------------------------------------------------------------------------
# topic_for
# ---------------------------------------------------------------------------

class TestTopicFor:
    def test_returns_topic_for_known_doc(self):
        m, _ = fit_mixed()
        t = m.topic_for("c1")
        assert isinstance(t, Topic)

    def test_returns_none_for_unknown_doc(self):
        m, _ = fit_mixed()
        assert m.topic_for("unknown") is None

    def test_returns_none_when_unfitted(self):
        m = make_model()
        assert m.topic_for("any") is None


# ---------------------------------------------------------------------------
# docs_for_topic
# ---------------------------------------------------------------------------

class TestDocsForTopic:
    def test_returns_doc_ids_for_topic(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        docs = m.docs_for_topic(tid)
        assert set(CAR_DOCS).issubset(set(docs))

    def test_returns_empty_for_unknown_topic(self):
        m, _ = fit_mixed()
        assert m.docs_for_topic(999) == []

    def test_returns_list_copy(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        docs = m.docs_for_topic(tid)
        docs.append("mutated")
        # original topic doc_ids should be unchanged
        assert "mutated" not in m.topic_for("c1").doc_ids


# ---------------------------------------------------------------------------
# top_keywords
# ---------------------------------------------------------------------------

class TestTopKeywords:
    def test_returns_list_of_tuples(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        kws = m.top_keywords(tid, top_k=3)
        assert isinstance(kws, list)
        assert all(isinstance(k, tuple) and len(k) == 2 for k in kws)

    def test_respects_top_k(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        kws = m.top_keywords(tid, top_k=2)
        assert len(kws) == 2

    def test_weights_descending(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        kws = m.top_keywords(tid, top_k=5)
        weights = [w for _, w in kws]
        assert weights == sorted(weights, reverse=True)

    def test_unknown_topic_returns_empty(self):
        m, _ = fit_mixed()
        assert m.top_keywords(999) == []

    def test_top_k_zero(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        assert m.top_keywords(tid, top_k=0) == []

    def test_top_k_negative_safe(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        assert m.top_keywords(tid, top_k=-3) == []


# ---------------------------------------------------------------------------
# similarity
# ---------------------------------------------------------------------------

class TestSimilarity:
    def test_self_similarity_is_one(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        assert m.similarity(tid, tid) == 1.0

    def test_different_topics_have_lower_similarity(self):
        m, _ = fit_mixed()
        a = m.topic_for("c1").topic_id
        b = m.topic_for("f1").topic_id
        sim = m.similarity(a, b)
        assert 0.0 <= sim < 1.0

    def test_unknown_topic_returns_zero(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        assert m.similarity(tid, 999) == 0.0
        assert m.similarity(999, tid) == 0.0


# ---------------------------------------------------------------------------
# most_similar
# ---------------------------------------------------------------------------

class TestMostSimilar:
    def test_returns_list(self):
        m, _ = fit_mixed()
        out = m.most_similar("pizza pasta", top_k=3)
        assert isinstance(out, list)

    def test_food_text_picks_food_topic(self):
        m, _ = fit_mixed()
        food_id = m.topic_for("f1").topic_id
        out = m.most_similar("pizza pasta bread food", top_k=2)
        assert out and out[0].topic_id == food_id

    def test_respects_top_k(self):
        m, _ = fit_mixed()
        out = m.most_similar("pizza pasta", top_k=1)
        assert len(out) <= 1

    def test_empty_text_returns_empty(self):
        m, _ = fit_mixed()
        assert m.most_similar("", top_k=3) == []

    def test_unfitted_returns_empty(self):
        m = make_model()
        assert m.most_similar("anything", top_k=3) == []

    def test_results_sorted_desc(self):
        m, _ = fit_mixed()
        out = m.most_similar("pizza pasta cars engines", top_k=5)
        scores = [td.score for td in out]
        assert scores == sorted(scores, reverse=True)


# ---------------------------------------------------------------------------
# coherence
# ---------------------------------------------------------------------------

class TestCoherence:
    def test_in_range(self):
        m, _ = fit_mixed()
        tid = m.topic_for("c1").topic_id
        c = m.coherence(tid)
        assert 0.0 <= c <= 1.0

    def test_unknown_topic_zero(self):
        m, _ = fit_mixed()
        assert m.coherence(999) == 0.0

    def test_unfitted_zero(self):
        m = make_model()
        assert m.coherence(0) == 0.0


# ---------------------------------------------------------------------------
# is_fitted
# ---------------------------------------------------------------------------

class TestIsFitted:
    def test_false_before_fit(self):
        m = make_model()
        assert m.is_fitted is False

    def test_true_after_fit(self):
        m, _ = fit_mixed()
        assert m.is_fitted is True

    def test_true_after_fit_empty(self):
        m = make_model()
        m.fit({})
        assert m.is_fitted is True


# ---------------------------------------------------------------------------
# num_topics
# ---------------------------------------------------------------------------

class TestNumTopics:
    def test_zero_before_fit(self):
        m = make_model()
        assert m.num_topics == 0

    def test_positive_after_fit(self):
        m, _ = fit_mixed()
        assert m.num_topics >= 1

    def test_respects_target_upper_bound(self):
        m = make_model(num_topics=2)
        m.fit(MIXED_DOCS)
        assert m.num_topics <= 2


# ---------------------------------------------------------------------------
# vocabulary
# ---------------------------------------------------------------------------

class TestVocabulary:
    def test_returns_set(self):
        m, _ = fit_mixed()
        v = m.vocabulary()
        assert isinstance(v, set)

    def test_contains_known_terms(self):
        m, _ = fit_mixed()
        v = m.vocabulary()
        assert "pizza" in v
        assert "cars" in v

    def test_empty_before_fit(self):
        m = make_model()
        assert m.vocabulary() == set()

    def test_returns_copy(self):
        m, _ = fit_mixed()
        v = m.vocabulary()
        v.add("__mutated__")
        # mutation should not affect the model's vocab
        assert "__mutated__" not in m.vocabulary()

    def test_min_term_freq_filters(self):
        m = DocTopicModel(num_topics=2, min_term_freq=3, max_terms_per_topic=5)
        m.fit({
            "a": "alpha beta gamma",
            "b": "alpha beta delta",
            "c": "alpha epsilon",
        })
        v = m.vocabulary()
        # 'alpha' appears in 3 docs, kept; 'gamma' only in 1
        assert "alpha" in v
        assert "gamma" not in v


# ---------------------------------------------------------------------------
# total_docs
# ---------------------------------------------------------------------------

class TestTotalDocs:
    def test_zero_before_fit(self):
        m = make_model()
        assert m.total_docs == 0

    def test_matches_after_fit(self):
        m, _ = fit_mixed()
        assert m.total_docs == len(MIXED_DOCS)

    def test_zero_for_empty_corpus(self):
        m = make_model()
        m.fit({})
        assert m.total_docs == 0


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------

class TestClear:
    def test_resets_fitted_state(self):
        m, _ = fit_mixed()
        m.clear()
        assert m.is_fitted is False

    def test_resets_num_topics(self):
        m, _ = fit_mixed()
        m.clear()
        assert m.num_topics == 0

    def test_resets_total_docs(self):
        m, _ = fit_mixed()
        m.clear()
        assert m.total_docs == 0

    def test_resets_vocabulary(self):
        m, _ = fit_mixed()
        m.clear()
        assert m.vocabulary() == set()

    def test_can_refit_after_clear(self):
        m, _ = fit_mixed()
        m.clear()
        result = m.fit(CAR_DOCS)
        assert result.total_docs == len(CAR_DOCS)
        assert m.is_fitted is True


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_invalid_num_topics(self):
        with pytest.raises(ValueError):
            DocTopicModel(num_topics=0)

    def test_invalid_min_term_freq(self):
        with pytest.raises(ValueError):
            DocTopicModel(num_topics=2, min_term_freq=0)

    def test_invalid_max_terms_per_topic(self):
        with pytest.raises(ValueError):
            DocTopicModel(num_topics=2, max_terms_per_topic=0)

    def test_single_doc(self):
        m = make_model(num_topics=1)
        result = m.fit({"only": "lonely document text words"})
        assert result.total_docs == 1
        assert len(result.topics) == 1
        assert result.topics[0].doc_ids == ["only"]

    def test_documents_with_only_whitespace(self):
        m = make_model()
        result = m.fit({"a": "   ", "b": "real content here words"})
        assert result.total_docs == 2

    def test_refit_overrides_previous(self):
        m = make_model()
        m.fit(CAR_DOCS)
        m.fit(FOOD_DOCS)
        # After refit, car doc ids must not be present
        assert m.topic_for("c1") is None
        assert m.topic_for("f1") is not None

    def test_unicode_text(self):
        m = make_model()
        docs = {
            "u1": "агент память консолидация",
            "u2": "память агент структура",
            "u3": "пицца паста еда",
            "u4": "еда пицца хлеб",
        }
        result = m.fit(docs)
        assert result.total_docs == 4
        # Russian tokens should appear in vocab
        assert "память" in m.vocabulary() or "пицца" in m.vocabulary()

    def test_tokenization_lowercases(self):
        m = make_model()
        m.fit({"a": "Apple APPLE apple", "b": "banana BANANA banana"})
        v = m.vocabulary()
        assert "apple" in v
        assert "banana" in v
        assert "Apple" not in v

    def test_max_terms_per_topic_respected(self):
        m = DocTopicModel(num_topics=1, min_term_freq=1, max_terms_per_topic=3)
        m.fit(MIXED_DOCS)
        assert all(len(t.keywords) <= 3 for t in m._model.topics)

    def test_doc_assignments_consistent_with_topic_doc_ids(self):
        m, result = fit_mixed()
        for doc_id, tid in result.doc_assignments.items():
            assert doc_id in m.docs_for_topic(tid)
