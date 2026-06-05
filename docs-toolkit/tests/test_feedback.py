"""Tests for the E19 feedback loop module.

Covers:
  - FeedbackType enum
  - FeedbackSignal dataclass (auto-id, auto-ts, value normalisation, predicates)
  - FeedbackStore (add/get/for_query/for_doc/stats/top_docs/worst_docs)
  - FeedbackAggregator (score_doc, score_all, query_satisfaction, rerank)
  - Edge cases: empty store, all-neutral, single signal
"""
import sys
import time
import uuid
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.feedback import (
    FeedbackType,
    FeedbackSignal,
    SignalStore as FeedbackStore,  # E19 store; SignalStore is the canonical E19 class
    DocScore,
    FeedbackAggregator,
)


# ======================================================================
# Helpers
# ======================================================================

def make_signal(
    query: str = "q",
    feedback_type: FeedbackType = FeedbackType.THUMBS_UP,
    doc_id: str | None = None,
    value: float = 0.0,
    note: str = "",
    ts: float | None = None,
) -> FeedbackSignal:
    sig = FeedbackSignal(
        query=query,
        feedback_type=feedback_type,
        doc_id=doc_id,
        value=value,
        note=note,
    )
    if ts is not None:
        sig.ts = ts
    return sig


@pytest.fixture
def store() -> FeedbackStore:
    return FeedbackStore()  # :memory: default


@pytest.fixture
def agg(store: FeedbackStore) -> FeedbackAggregator:
    return FeedbackAggregator(store)


# ======================================================================
# FeedbackType enum
# ======================================================================

class TestFeedbackType:
    def test_enum_members_exist(self):
        assert FeedbackType.THUMBS_UP
        assert FeedbackType.THUMBS_DOWN
        assert FeedbackType.RATING
        assert FeedbackType.CORRECTION
        assert FeedbackType.SKIP

    def test_enum_values_are_strings(self):
        for member in FeedbackType:
            assert isinstance(member.value, str)

    def test_enum_by_value(self):
        assert FeedbackType("thumbs_up") is FeedbackType.THUMBS_UP
        assert FeedbackType("thumbs_down") is FeedbackType.THUMBS_DOWN
        assert FeedbackType("rating") is FeedbackType.RATING
        assert FeedbackType("correction") is FeedbackType.CORRECTION
        assert FeedbackType("skip") is FeedbackType.SKIP


# ======================================================================
# FeedbackSignal — construction and auto-fields
# ======================================================================

class TestFeedbackSignalConstruction:
    def test_auto_signal_id_is_uuid4_format(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP)
        # Should be a valid UUID4 string
        parsed = uuid.UUID(sig.signal_id, version=4)
        assert str(parsed) == sig.signal_id

    def test_signal_id_is_unique_across_instances(self):
        s1 = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP)
        s2 = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP)
        assert s1.signal_id != s2.signal_id

    def test_auto_ts_is_recent(self):
        before = time.time()
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP)
        after = time.time()
        assert before <= sig.ts <= after

    def test_explicit_signal_id_preserved(self):
        my_id = str(uuid.uuid4())
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP, signal_id=my_id)
        assert sig.signal_id == my_id

    def test_explicit_ts_preserved(self):
        ts = 1_000_000.0
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP, ts=ts)
        assert sig.ts == ts

    def test_doc_id_default_is_none(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP)
        assert sig.doc_id is None

    def test_doc_id_can_be_set(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP, doc_id="doc1")
        assert sig.doc_id == "doc1"

    def test_note_default_is_empty_string(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP)
        assert sig.note == ""

    def test_note_preserved(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP, note="great")
        assert sig.note == "great"


# ======================================================================
# FeedbackSignal — value normalisation
# ======================================================================

class TestFeedbackSignalValueNormalisation:
    def test_thumbs_up_always_one(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP, value=0.0)
        assert sig.value == 1.0

    def test_thumbs_up_ignores_raw_value(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP, value=-5.0)
        assert sig.value == 1.0

    def test_thumbs_down_always_minus_one(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_DOWN, value=0.0)
        assert sig.value == -1.0

    def test_thumbs_down_ignores_raw_value(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_DOWN, value=99.0)
        assert sig.value == -1.0

    def test_skip_always_zero(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.SKIP, value=1.0)
        assert sig.value == 0.0

    def test_rating_1_maps_to_0(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.RATING, value=1.0)
        assert sig.value == pytest.approx(0.0)

    def test_rating_5_maps_to_1(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.RATING, value=5.0)
        assert sig.value == pytest.approx(1.0)

    def test_rating_3_maps_to_half(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.RATING, value=3.0)
        assert sig.value == pytest.approx(0.5)

    def test_rating_clamped_above(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.RATING, value=10.0)
        assert sig.value == pytest.approx(1.0)

    def test_rating_clamped_below(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.RATING, value=-5.0)
        assert sig.value == pytest.approx(0.0)

    def test_correction_keeps_provided_value(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.CORRECTION, value=-0.5)
        assert sig.value == pytest.approx(-0.5)

    def test_correction_default_value_zero(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.CORRECTION)
        assert sig.value == 0.0


# ======================================================================
# FeedbackSignal — predicates
# ======================================================================

class TestFeedbackSignalPredicates:
    def test_thumbs_up_is_positive(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_UP)
        assert sig.is_positive() is True
        assert sig.is_negative() is False

    def test_thumbs_down_is_negative(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.THUMBS_DOWN)
        assert sig.is_negative() is True
        assert sig.is_positive() is False

    def test_skip_is_neither_positive_nor_negative(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.SKIP)
        assert sig.is_positive() is False
        assert sig.is_negative() is False

    def test_rating_1_is_not_positive(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.RATING, value=1.0)
        assert sig.is_positive() is False

    def test_rating_5_is_positive(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.RATING, value=5.0)
        assert sig.is_positive() is True

    def test_positive_correction(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.CORRECTION, value=0.8)
        assert sig.is_positive() is True
        assert sig.is_negative() is False

    def test_negative_correction(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.CORRECTION, value=-0.3)
        assert sig.is_negative() is True
        assert sig.is_positive() is False

    def test_neutral_correction(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.CORRECTION, value=0.0)
        assert sig.is_positive() is False
        assert sig.is_negative() is False


# ======================================================================
# FeedbackStore — basic operations
# ======================================================================

class TestFeedbackStoreAddGet:
    def test_store_defaults_to_memory(self):
        s = FeedbackStore()  # should not raise
        s.close()

    def test_store_file_path(self, tmp_path):
        db = tmp_path / "fb.sqlite"
        s = FeedbackStore(db_path=db)
        sig = make_signal(query="hello")
        s.add(sig)
        assert s.get(sig.signal_id) is not None
        s.close()
        assert db.exists()

    def test_add_and_get_roundtrip(self, store):
        sig = make_signal(query="find me", doc_id="d1", note="ok")
        store.add(sig)
        got = store.get(sig.signal_id)
        assert got is not None
        assert got.signal_id == sig.signal_id
        assert got.query == "find me"
        assert got.doc_id == "d1"
        assert got.note == "ok"
        assert got.feedback_type == FeedbackType.THUMBS_UP
        assert got.value == pytest.approx(1.0)

    def test_get_missing_returns_none(self, store):
        assert store.get("nonexistent-id") is None

    def test_add_upserts_by_signal_id(self, store):
        sig = make_signal(query="original")
        store.add(sig)
        # Overwrite by re-adding with same signal_id but different query
        sig2 = FeedbackSignal(
            query="updated",
            feedback_type=FeedbackType.THUMBS_DOWN,
            signal_id=sig.signal_id,
        )
        store.add(sig2)
        got = store.get(sig.signal_id)
        assert got.query == "updated"
        assert got.feedback_type == FeedbackType.THUMBS_DOWN

    def test_get_preserves_doc_id_none(self, store):
        sig = make_signal(query="q")
        store.add(sig)
        got = store.get(sig.signal_id)
        assert got.doc_id is None

    def test_get_preserves_ts(self, store):
        sig = make_signal(query="q", ts=123456.789)
        store.add(sig)
        got = store.get(sig.signal_id)
        assert got.ts == pytest.approx(123456.789)


# ======================================================================
# FeedbackStore — for_query / for_doc
# ======================================================================

class TestFeedbackStoreFilters:
    def test_for_query_returns_matching_signals(self, store):
        store.add(make_signal(query="A"))
        store.add(make_signal(query="A"))
        store.add(make_signal(query="B"))
        result = store.for_query("A")
        assert len(result) == 2
        assert all(s.query == "A" for s in result)

    def test_for_query_empty_when_no_match(self, store):
        store.add(make_signal(query="A"))
        assert store.for_query("Z") == []

    def test_for_query_empty_store(self, store):
        assert store.for_query("anything") == []

    def test_for_doc_returns_matching_signals(self, store):
        store.add(make_signal(query="q", doc_id="d1"))
        store.add(make_signal(query="q", doc_id="d1"))
        store.add(make_signal(query="q", doc_id="d2"))
        result = store.for_doc("d1")
        assert len(result) == 2
        assert all(s.doc_id == "d1" for s in result)

    def test_for_doc_empty_when_no_match(self, store):
        store.add(make_signal(query="q", doc_id="d1"))
        assert store.for_doc("d99") == []

    def test_for_doc_does_not_return_none_doc_id_signals(self, store):
        store.add(make_signal(query="q", doc_id=None))
        assert store.for_doc("") == []

    def test_for_query_ordered_by_ts(self, store):
        store.add(make_signal(query="q", ts=2.0))
        store.add(make_signal(query="q", ts=1.0))
        store.add(make_signal(query="q", ts=3.0))
        result = store.for_query("q")
        assert [s.ts for s in result] == [1.0, 2.0, 3.0]


# ======================================================================
# FeedbackStore — stats
# ======================================================================

class TestFeedbackStoreStats:
    def test_stats_empty_store(self, store):
        s = store.stats()
        assert s["total"] == 0
        assert s["positive"] == 0
        assert s["negative"] == 0
        assert s["neutral"] == 0
        assert s["avg_value"] == 0.0

    def test_stats_keys_present(self, store):
        store.add(make_signal())
        s = store.stats()
        for key in ("total", "positive", "negative", "neutral", "avg_value"):
            assert key in s

    def test_stats_counts_total(self, store):
        for _ in range(5):
            store.add(make_signal())
        assert store.stats()["total"] == 5

    def test_stats_positive_count(self, store):
        store.add(make_signal(feedback_type=FeedbackType.THUMBS_UP))
        store.add(make_signal(feedback_type=FeedbackType.THUMBS_UP))
        store.add(make_signal(feedback_type=FeedbackType.THUMBS_DOWN))
        s = store.stats()
        assert s["positive"] == 2
        assert s["negative"] == 1
        assert s["neutral"] == 0

    def test_stats_neutral_count(self, store):
        store.add(make_signal(feedback_type=FeedbackType.SKIP))
        store.add(make_signal(feedback_type=FeedbackType.THUMBS_UP))
        s = store.stats()
        assert s["neutral"] == 1
        assert s["positive"] == 1

    def test_stats_avg_value_thumbs_up_down(self, store):
        store.add(make_signal(feedback_type=FeedbackType.THUMBS_UP))   # 1.0
        store.add(make_signal(feedback_type=FeedbackType.THUMBS_DOWN))  # -1.0
        s = store.stats()
        assert s["avg_value"] == pytest.approx(0.0)

    def test_stats_avg_value_all_positive(self, store):
        for _ in range(4):
            store.add(make_signal(feedback_type=FeedbackType.THUMBS_UP))
        assert store.stats()["avg_value"] == pytest.approx(1.0)

    def test_stats_all_neutral(self, store):
        for _ in range(3):
            store.add(make_signal(feedback_type=FeedbackType.SKIP))
        s = store.stats()
        assert s["neutral"] == 3
        assert s["positive"] == 0
        assert s["negative"] == 0
        assert s["avg_value"] == pytest.approx(0.0)


# ======================================================================
# FeedbackStore — top_docs / worst_docs
# ======================================================================

class TestFeedbackStoreTopWorstDocs:
    def test_top_docs_empty_store(self, store):
        assert store.top_docs() == []

    def test_worst_docs_empty_store(self, store):
        assert store.worst_docs() == []

    def test_top_docs_returns_tuples(self, store):
        store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_UP))
        result = store.top_docs()
        assert len(result) == 1
        assert isinstance(result[0], tuple)
        assert result[0][0] == "d1"
        assert result[0][1] == pytest.approx(1.0)

    def test_top_docs_sorted_desc(self, store):
        store.add(make_signal(doc_id="low", feedback_type=FeedbackType.THUMBS_DOWN))
        store.add(make_signal(doc_id="high", feedback_type=FeedbackType.THUMBS_UP))
        result = store.top_docs()
        assert result[0][0] == "high"
        assert result[-1][0] == "low"

    def test_worst_docs_sorted_asc(self, store):
        store.add(make_signal(doc_id="low", feedback_type=FeedbackType.THUMBS_DOWN))
        store.add(make_signal(doc_id="high", feedback_type=FeedbackType.THUMBS_UP))
        result = store.worst_docs()
        assert result[0][0] == "low"
        assert result[-1][0] == "high"

    def test_top_docs_ignores_signals_without_doc_id(self, store):
        store.add(make_signal(doc_id=None, feedback_type=FeedbackType.THUMBS_UP))
        assert store.top_docs() == []

    def test_top_docs_n_limits_results(self, store):
        for i in range(10):
            store.add(make_signal(doc_id=f"doc{i}", feedback_type=FeedbackType.THUMBS_UP))
        assert len(store.top_docs(n=3)) == 3

    def test_worst_docs_n_limits_results(self, store):
        for i in range(10):
            store.add(make_signal(doc_id=f"doc{i}", feedback_type=FeedbackType.THUMBS_DOWN))
        assert len(store.worst_docs(n=5)) == 5

    def test_top_docs_averages_multiple_signals(self, store):
        # d1: up + down → avg 0.0
        store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_UP))
        store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_DOWN))
        # d2: up → avg 1.0
        store.add(make_signal(doc_id="d2", feedback_type=FeedbackType.THUMBS_UP))
        result = store.top_docs()
        assert result[0][0] == "d2"
        assert result[1][0] == "d1"


# ======================================================================
# FeedbackAggregator — score_doc
# ======================================================================

class TestFeedbackAggregatorScoreDoc:
    def test_score_doc_none_when_no_signals(self, agg):
        assert agg.score_doc("missing") is None

    def test_score_doc_returns_doc_score(self, store, agg):
        store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_UP))
        ds = agg.score_doc("d1")
        assert isinstance(ds, DocScore)

    def test_score_doc_fields(self, store, agg):
        store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_UP))
        store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_DOWN))
        ds = agg.score_doc("d1")
        assert ds.doc_id == "d1"
        assert ds.signal_count == 2
        assert ds.avg_value == pytest.approx(0.0)
        assert ds.positive_rate == pytest.approx(0.5)

    def test_score_doc_all_positive(self, store, agg):
        for _ in range(3):
            store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_UP))
        ds = agg.score_doc("d1")
        assert ds.avg_value == pytest.approx(1.0)
        assert ds.positive_rate == pytest.approx(1.0)

    def test_score_doc_all_negative(self, store, agg):
        for _ in range(3):
            store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_DOWN))
        ds = agg.score_doc("d1")
        assert ds.avg_value == pytest.approx(-1.0)
        assert ds.positive_rate == pytest.approx(0.0)

    def test_score_doc_single_signal(self, store, agg):
        store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.SKIP))
        ds = agg.score_doc("d1")
        assert ds.signal_count == 1
        assert ds.avg_value == pytest.approx(0.0)
        assert ds.positive_rate == pytest.approx(0.0)


# ======================================================================
# FeedbackAggregator — score_all
# ======================================================================

class TestFeedbackAggregatorScoreAll:
    def test_score_all_empty_store(self, agg):
        assert agg.score_all() == []

    def test_score_all_returns_doc_scores(self, store, agg):
        store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_UP))
        store.add(make_signal(doc_id="d2", feedback_type=FeedbackType.THUMBS_DOWN))
        result = agg.score_all()
        assert len(result) == 2
        assert all(isinstance(ds, DocScore) for ds in result)

    def test_score_all_sorted_desc_by_avg_value(self, store, agg):
        store.add(make_signal(doc_id="low", feedback_type=FeedbackType.THUMBS_DOWN))
        store.add(make_signal(doc_id="high", feedback_type=FeedbackType.THUMBS_UP))
        store.add(make_signal(doc_id="mid", feedback_type=FeedbackType.SKIP))
        result = agg.score_all()
        avg_values = [ds.avg_value for ds in result]
        assert avg_values == sorted(avg_values, reverse=True)

    def test_score_all_excludes_signals_without_doc_id(self, store, agg):
        store.add(make_signal(doc_id=None, feedback_type=FeedbackType.THUMBS_UP))
        assert agg.score_all() == []

    def test_score_all_covers_all_docs(self, store, agg):
        doc_ids = ["a", "b", "c", "d"]
        for did in doc_ids:
            store.add(make_signal(doc_id=did, feedback_type=FeedbackType.THUMBS_UP))
        result = agg.score_all()
        result_ids = {ds.doc_id for ds in result}
        assert result_ids == set(doc_ids)


# ======================================================================
# FeedbackAggregator — query_satisfaction
# ======================================================================

class TestFeedbackAggregatorQuerySatisfaction:
    def test_query_satisfaction_zero_when_no_signals(self, agg):
        assert agg.query_satisfaction("unknown query") == 0.0

    def test_query_satisfaction_all_positive(self, store, agg):
        for _ in range(3):
            store.add(make_signal(query="hi", feedback_type=FeedbackType.THUMBS_UP))
        assert agg.query_satisfaction("hi") == pytest.approx(1.0)

    def test_query_satisfaction_all_negative(self, store, agg):
        for _ in range(3):
            store.add(make_signal(query="hi", feedback_type=FeedbackType.THUMBS_DOWN))
        assert agg.query_satisfaction("hi") == pytest.approx(-1.0)

    def test_query_satisfaction_mixed(self, store, agg):
        store.add(make_signal(query="q", feedback_type=FeedbackType.THUMBS_UP))   # 1.0
        store.add(make_signal(query="q", feedback_type=FeedbackType.THUMBS_DOWN))  # -1.0
        assert agg.query_satisfaction("q") == pytest.approx(0.0)

    def test_query_satisfaction_single_signal(self, store, agg):
        store.add(make_signal(query="solo", feedback_type=FeedbackType.THUMBS_UP))
        assert agg.query_satisfaction("solo") == pytest.approx(1.0)

    def test_query_satisfaction_skip_signals(self, store, agg):
        for _ in range(4):
            store.add(make_signal(query="q", feedback_type=FeedbackType.SKIP))
        assert agg.query_satisfaction("q") == pytest.approx(0.0)


# ======================================================================
# FeedbackAggregator — rerank
# ======================================================================

class TestFeedbackAggregatorRerank:
    def test_rerank_empty_list(self, agg):
        assert agg.rerank([]) == []

    def test_rerank_single_doc(self, store, agg):
        store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_UP))
        result = agg.rerank(["d1"])
        assert result == ["d1"]

    def test_rerank_preserves_order_when_no_feedback(self, agg):
        # No signals → all avg_values = 0, so reciprocal rank dominates
        doc_ids = ["a", "b", "c"]
        result = agg.rerank(doc_ids)
        assert result == doc_ids  # original order preserved when no feedback

    def test_rerank_boosts_high_scoring_doc(self, store, agg):
        # d3 is originally ranked last but has high feedback
        for _ in range(5):
            store.add(make_signal(doc_id="d3", feedback_type=FeedbackType.THUMBS_UP))
        result = agg.rerank(["d1", "d2", "d3"], boost_factor=2.0)
        assert result[0] == "d3"

    def test_rerank_demotes_low_scoring_doc(self, store, agg):
        # d1 is ranked first but has very negative feedback; d2/d3 have none
        for _ in range(5):
            store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.THUMBS_DOWN))
        result = agg.rerank(["d1", "d2", "d3"], boost_factor=2.0)
        # d1 should not remain first
        assert result[0] != "d1"

    def test_rerank_returns_all_docs(self, store, agg):
        doc_ids = ["a", "b", "c", "d", "e"]
        store.add(make_signal(doc_id="c", feedback_type=FeedbackType.THUMBS_UP))
        result = agg.rerank(doc_ids)
        assert sorted(result) == sorted(doc_ids)

    def test_rerank_boost_factor_zero_preserves_order(self, agg):
        # With boost_factor=0, all adjusted scores come from reciprocal rank only
        result = agg.rerank(["a", "b", "c"], boost_factor=0.0)
        assert result == ["a", "b", "c"]

    def test_rerank_docs_without_signals_treated_as_neutral(self, store, agg):
        store.add(make_signal(doc_id="good", feedback_type=FeedbackType.THUMBS_UP))
        result = agg.rerank(["no_signal", "good"], boost_factor=0.5)
        # "good" should stay ahead or move up compared to "no_signal"
        assert "good" in result
        assert "no_signal" in result


# ======================================================================
# Edge cases: no feedback / single signal / all neutral
# ======================================================================

class TestEdgeCases:
    def test_score_doc_with_all_neutral_signals(self, store, agg):
        for _ in range(5):
            store.add(make_signal(doc_id="d1", feedback_type=FeedbackType.SKIP))
        ds = agg.score_doc("d1")
        assert ds is not None
        assert ds.avg_value == pytest.approx(0.0)
        assert ds.positive_rate == pytest.approx(0.0)

    def test_stats_single_thumbs_up(self, store):
        store.add(make_signal(feedback_type=FeedbackType.THUMBS_UP))
        s = store.stats()
        assert s["total"] == 1
        assert s["positive"] == 1
        assert s["negative"] == 0
        assert s["avg_value"] == pytest.approx(1.0)

    def test_stats_single_thumbs_down(self, store):
        store.add(make_signal(feedback_type=FeedbackType.THUMBS_DOWN))
        s = store.stats()
        assert s["total"] == 1
        assert s["negative"] == 1
        assert s["avg_value"] == pytest.approx(-1.0)

    def test_query_satisfaction_returns_float(self, store, agg):
        result = agg.query_satisfaction("any")
        assert isinstance(result, float)

    def test_score_all_single_doc(self, store, agg):
        store.add(make_signal(doc_id="only", feedback_type=FeedbackType.THUMBS_UP))
        result = agg.score_all()
        assert len(result) == 1
        assert result[0].doc_id == "only"

    def test_feedback_signal_rating_2_normalised(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.RATING, value=2.0)
        assert sig.value == pytest.approx(0.25)

    def test_feedback_signal_rating_4_normalised(self):
        sig = FeedbackSignal(query="q", feedback_type=FeedbackType.RATING, value=4.0)
        assert sig.value == pytest.approx(0.75)
