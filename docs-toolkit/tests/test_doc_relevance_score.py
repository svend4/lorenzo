"""Tests for E395 DocRelevanceScore."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_relevance_score import (
    DocRelevanceScore,
    RelevanceScore,
    ScoringStats,
)


# ---------------------------------------------------------------- dataclasses
class TestRelevanceScoreDataclass:
    def test_minimal(self):
        s = RelevanceScore(query="q", doc_id="d", score=0.5)
        assert s.query == "q"
        assert s.doc_id == "d"
        assert s.score == 0.5
        assert s.recorded_at == 0.0

    def test_full(self):
        s = RelevanceScore(query="q", doc_id="d", score=0.8, recorded_at=123.0)
        assert s.recorded_at == 123.0

    def test_equality(self):
        a = RelevanceScore(query="q", doc_id="d", score=0.5, recorded_at=1.0)
        b = RelevanceScore(query="q", doc_id="d", score=0.5, recorded_at=1.0)
        assert a == b

    def test_inequality(self):
        a = RelevanceScore(query="q", doc_id="d", score=0.5)
        b = RelevanceScore(query="q", doc_id="d", score=0.6)
        assert a != b


class TestScoringStatsDataclass:
    def test_minimal(self):
        st = ScoringStats(total_scores=0, unique_queries=0, unique_docs=0, avg_score=0.0)
        assert st.total_scores == 0
        assert st.avg_score == 0.0

    def test_full(self):
        st = ScoringStats(
            total_scores=10, unique_queries=3, unique_docs=5, avg_score=0.7
        )
        assert st.total_scores == 10
        assert st.unique_queries == 3
        assert st.unique_docs == 5
        assert st.avg_score == 0.7

    def test_equality(self):
        a = ScoringStats(total_scores=1, unique_queries=1, unique_docs=1, avg_score=0.5)
        b = ScoringStats(total_scores=1, unique_queries=1, unique_docs=1, avg_score=0.5)
        assert a == b


# --------------------------------------------------------------- construction
class TestConstruction:
    def test_empty_store(self):
        d = DocRelevanceScore()
        assert d.all_queries() == []
        assert d.all_doc_ids() == []

    def test_stats_empty(self):
        d = DocRelevanceScore()
        st = d.stats()
        assert st.total_scores == 0
        assert st.unique_queries == 0
        assert st.unique_docs == 0
        assert st.avg_score == 0.0

    def test_independent_instances(self):
        a = DocRelevanceScore()
        b = DocRelevanceScore()
        a.record_score("q", "d", 0.5)
        assert b.get_score("q", "d") is None


# ----------------------------------------------------------------- record
class TestRecordScore:
    def test_returns_relevance_score(self):
        d = DocRelevanceScore()
        s = d.record_score("q", "d", 0.5, now=10.0)
        assert isinstance(s, RelevanceScore)
        assert s.query == "q"
        assert s.doc_id == "d"
        assert s.score == 0.5
        assert s.recorded_at == 10.0

    def test_default_now_is_current_time(self):
        d = DocRelevanceScore()
        s = d.record_score("q", "d", 0.5)
        assert s.recorded_at > 0.0

    def test_clamp_above_one(self):
        d = DocRelevanceScore()
        s = d.record_score("q", "d", 1.5)
        assert s.score == 1.0

    def test_clamp_below_zero(self):
        d = DocRelevanceScore()
        s = d.record_score("q", "d", -0.3)
        assert s.score == 0.0

    def test_clamp_exact_zero(self):
        d = DocRelevanceScore()
        s = d.record_score("q", "d", 0.0)
        assert s.score == 0.0

    def test_clamp_exact_one(self):
        d = DocRelevanceScore()
        s = d.record_score("q", "d", 1.0)
        assert s.score == 1.0

    def test_replaces_existing(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.3, now=1.0)
        s2 = d.record_score("q", "d", 0.7, now=2.0)
        assert s2.score == 0.7
        assert d.get_score("q", "d") == 0.7

    def test_replace_does_not_duplicate(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.3)
        d.record_score("q", "d", 0.7)
        assert d.stats().total_scores == 1

    def test_indices_updated(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d1", 0.5)
        d.record_score("q2", "d1", 0.6)
        d.record_score("q1", "d2", 0.7)
        assert d.all_queries() == ["q1", "q2"]
        assert d.all_doc_ids() == ["d1", "d2"]


# --------------------------------------------------------------------- get
class TestGetScore:
    def test_get_existing(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.5)
        assert d.get_score("q", "d") == 0.5

    def test_get_missing(self):
        d = DocRelevanceScore()
        assert d.get_score("q", "d") is None

    def test_get_different_query(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d", 0.5)
        assert d.get_score("q2", "d") is None

    def test_get_different_doc(self):
        d = DocRelevanceScore()
        d.record_score("q", "d1", 0.5)
        assert d.get_score("q", "d2") is None


# --------------------------------------------------------------------- delete
class TestDeleteScore:
    def test_delete_existing_returns_true(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.5)
        assert d.delete_score("q", "d") is True

    def test_delete_missing_returns_false(self):
        d = DocRelevanceScore()
        assert d.delete_score("q", "d") is False

    def test_delete_removes(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.5)
        d.delete_score("q", "d")
        assert d.get_score("q", "d") is None

    def test_delete_cleans_indices_query(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.5)
        d.delete_score("q", "d")
        assert d.all_queries() == []
        assert d.all_doc_ids() == []

    def test_delete_keeps_other_entries(self):
        d = DocRelevanceScore()
        d.record_score("q", "d1", 0.5)
        d.record_score("q", "d2", 0.6)
        d.delete_score("q", "d1")
        assert d.get_score("q", "d2") == 0.6
        assert d.all_doc_ids() == ["d2"]


# --------------------------------------------------------------------- top_docs
class TestTopDocsFor:
    def test_empty_returns_empty(self):
        d = DocRelevanceScore()
        assert d.top_docs_for("q") == []

    def test_sorted_by_score_desc(self):
        d = DocRelevanceScore()
        d.record_score("q", "a", 0.3)
        d.record_score("q", "b", 0.9)
        d.record_score("q", "c", 0.5)
        assert d.top_docs_for("q") == [("b", 0.9), ("c", 0.5), ("a", 0.3)]

    def test_tiebreak_by_doc_id_asc(self):
        d = DocRelevanceScore()
        d.record_score("q", "z", 0.5)
        d.record_score("q", "a", 0.5)
        d.record_score("q", "m", 0.5)
        assert d.top_docs_for("q") == [("a", 0.5), ("m", 0.5), ("z", 0.5)]

    def test_limit_applied(self):
        d = DocRelevanceScore()
        d.record_score("q", "a", 0.1)
        d.record_score("q", "b", 0.2)
        d.record_score("q", "c", 0.3)
        result = d.top_docs_for("q", limit=2)
        assert result == [("c", 0.3), ("b", 0.2)]

    def test_min_score_filter(self):
        d = DocRelevanceScore()
        d.record_score("q", "a", 0.1)
        d.record_score("q", "b", 0.5)
        d.record_score("q", "c", 0.9)
        result = d.top_docs_for("q", min_score=0.4)
        assert result == [("c", 0.9), ("b", 0.5)]

    def test_min_score_inclusive(self):
        d = DocRelevanceScore()
        d.record_score("q", "a", 0.5)
        result = d.top_docs_for("q", min_score=0.5)
        assert result == [("a", 0.5)]

    def test_only_for_given_query(self):
        d = DocRelevanceScore()
        d.record_score("q1", "a", 0.9)
        d.record_score("q2", "b", 0.8)
        assert d.top_docs_for("q1") == [("a", 0.9)]


# ------------------------------------------------------------------ top_queries
class TestTopQueriesFor:
    def test_empty_returns_empty(self):
        d = DocRelevanceScore()
        assert d.top_queries_for("d") == []

    def test_sorted_by_score_desc(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d", 0.3)
        d.record_score("q2", "d", 0.9)
        d.record_score("q3", "d", 0.5)
        assert d.top_queries_for("d") == [("q2", 0.9), ("q3", 0.5), ("q1", 0.3)]

    def test_tiebreak_by_query_asc(self):
        d = DocRelevanceScore()
        d.record_score("zebra", "d", 0.5)
        d.record_score("alpha", "d", 0.5)
        d.record_score("mango", "d", 0.5)
        assert d.top_queries_for("d") == [
            ("alpha", 0.5),
            ("mango", 0.5),
            ("zebra", 0.5),
        ]

    def test_limit_applied(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d", 0.1)
        d.record_score("q2", "d", 0.2)
        d.record_score("q3", "d", 0.3)
        result = d.top_queries_for("d", limit=2)
        assert result == [("q3", 0.3), ("q2", 0.2)]

    def test_only_for_given_doc(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d1", 0.9)
        d.record_score("q2", "d2", 0.8)
        assert d.top_queries_for("d1") == [("q1", 0.9)]


# ------------------------------------------------------------- scores_for_query
class TestScoresForQuery:
    def test_empty_returns_empty(self):
        d = DocRelevanceScore()
        assert d.scores_for_query("q") == []

    def test_returns_relevance_scores(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.5)
        results = d.scores_for_query("q")
        assert len(results) == 1
        assert isinstance(results[0], RelevanceScore)

    def test_sorted_desc(self):
        d = DocRelevanceScore()
        d.record_score("q", "a", 0.3)
        d.record_score("q", "b", 0.9)
        d.record_score("q", "c", 0.5)
        results = d.scores_for_query("q")
        assert [e.score for e in results] == [0.9, 0.5, 0.3]

    def test_only_matching_query(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d", 0.5)
        d.record_score("q2", "d", 0.7)
        results = d.scores_for_query("q1")
        assert len(results) == 1
        assert results[0].query == "q1"


# --------------------------------------------------------------- scores_for_doc
class TestScoresForDoc:
    def test_empty_returns_empty(self):
        d = DocRelevanceScore()
        assert d.scores_for_doc("d") == []

    def test_returns_relevance_scores(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.5)
        results = d.scores_for_doc("d")
        assert len(results) == 1
        assert isinstance(results[0], RelevanceScore)

    def test_sorted_desc(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d", 0.3)
        d.record_score("q2", "d", 0.9)
        d.record_score("q3", "d", 0.5)
        results = d.scores_for_doc("d")
        assert [e.score for e in results] == [0.9, 0.5, 0.3]

    def test_only_matching_doc(self):
        d = DocRelevanceScore()
        d.record_score("q", "d1", 0.5)
        d.record_score("q", "d2", 0.7)
        results = d.scores_for_doc("d1")
        assert len(results) == 1
        assert results[0].doc_id == "d1"


# ------------------------------------------------------------------ clear_query
class TestClearQuery:
    def test_clear_returns_count(self):
        d = DocRelevanceScore()
        d.record_score("q", "d1", 0.5)
        d.record_score("q", "d2", 0.6)
        d.record_score("q", "d3", 0.7)
        assert d.clear_query("q") == 3

    def test_clear_missing_returns_zero(self):
        d = DocRelevanceScore()
        assert d.clear_query("q") == 0

    def test_clear_removes_entries(self):
        d = DocRelevanceScore()
        d.record_score("q", "d1", 0.5)
        d.record_score("q", "d2", 0.6)
        d.clear_query("q")
        assert d.get_score("q", "d1") is None
        assert d.get_score("q", "d2") is None

    def test_clear_keeps_other_queries(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d", 0.5)
        d.record_score("q2", "d", 0.6)
        d.clear_query("q1")
        assert d.get_score("q2", "d") == 0.6

    def test_clear_updates_indices(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.5)
        d.clear_query("q")
        assert d.all_queries() == []
        assert d.all_doc_ids() == []


# -------------------------------------------------------------------- clear_doc
class TestClearDoc:
    def test_clear_returns_count(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d", 0.5)
        d.record_score("q2", "d", 0.6)
        assert d.clear_doc("d") == 2

    def test_clear_missing_returns_zero(self):
        d = DocRelevanceScore()
        assert d.clear_doc("d") == 0

    def test_clear_removes_entries(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d", 0.5)
        d.record_score("q2", "d", 0.6)
        d.clear_doc("d")
        assert d.get_score("q1", "d") is None
        assert d.get_score("q2", "d") is None

    def test_clear_keeps_other_docs(self):
        d = DocRelevanceScore()
        d.record_score("q", "d1", 0.5)
        d.record_score("q", "d2", 0.6)
        d.clear_doc("d1")
        assert d.get_score("q", "d2") == 0.6

    def test_clear_updates_indices(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.5)
        d.clear_doc("d")
        assert d.all_doc_ids() == []
        assert d.all_queries() == []


# -------------------------------------------------------------------- clear_all
class TestClearAll:
    def test_clear_returns_count(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d1", 0.5)
        d.record_score("q2", "d2", 0.6)
        d.record_score("q3", "d3", 0.7)
        assert d.clear_all() == 3

    def test_clear_empty_returns_zero(self):
        d = DocRelevanceScore()
        assert d.clear_all() == 0

    def test_clear_removes_everything(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d1", 0.5)
        d.record_score("q2", "d2", 0.6)
        d.clear_all()
        assert d.all_queries() == []
        assert d.all_doc_ids() == []
        assert d.stats().total_scores == 0


# ------------------------------------------------------------------- all_queries
class TestAllQueries:
    def test_empty(self):
        d = DocRelevanceScore()
        assert d.all_queries() == []

    def test_sorted(self):
        d = DocRelevanceScore()
        d.record_score("zebra", "d", 0.5)
        d.record_score("alpha", "d", 0.5)
        d.record_score("mango", "d", 0.5)
        assert d.all_queries() == ["alpha", "mango", "zebra"]

    def test_unique(self):
        d = DocRelevanceScore()
        d.record_score("q", "d1", 0.5)
        d.record_score("q", "d2", 0.6)
        assert d.all_queries() == ["q"]


# ------------------------------------------------------------------- all_doc_ids
class TestAllDocIds:
    def test_empty(self):
        d = DocRelevanceScore()
        assert d.all_doc_ids() == []

    def test_sorted(self):
        d = DocRelevanceScore()
        d.record_score("q", "zebra", 0.5)
        d.record_score("q", "alpha", 0.5)
        d.record_score("q", "mango", 0.5)
        assert d.all_doc_ids() == ["alpha", "mango", "zebra"]

    def test_unique(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d", 0.5)
        d.record_score("q2", "d", 0.6)
        assert d.all_doc_ids() == ["d"]


# ------------------------------------------------------------------------ stats
class TestStats:
    def test_empty(self):
        d = DocRelevanceScore()
        st = d.stats()
        assert st.total_scores == 0
        assert st.unique_queries == 0
        assert st.unique_docs == 0
        assert st.avg_score == 0.0

    def test_counts(self):
        d = DocRelevanceScore()
        d.record_score("q1", "d1", 0.5)
        d.record_score("q1", "d2", 0.7)
        d.record_score("q2", "d1", 0.9)
        st = d.stats()
        assert st.total_scores == 3
        assert st.unique_queries == 2
        assert st.unique_docs == 2

    def test_avg(self):
        d = DocRelevanceScore()
        d.record_score("q", "d1", 0.2)
        d.record_score("q", "d2", 0.4)
        d.record_score("q", "d3", 0.6)
        st = d.stats()
        assert st.avg_score == pytest.approx(0.4)

    def test_avg_after_replace(self):
        d = DocRelevanceScore()
        d.record_score("q", "d", 0.2)
        d.record_score("q", "d", 0.8)
        st = d.stats()
        assert st.total_scores == 1
        assert st.avg_score == pytest.approx(0.8)


# ----------------------------------------------------------------- thread safety
class TestThreadSafety:
    def test_concurrent_record(self):
        d = DocRelevanceScore()

        def worker(qidx: int):
            for i in range(50):
                d.record_score(f"q{qidx}", f"d{i}", (i % 10) / 10.0)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        st = d.stats()
        assert st.total_scores == 8 * 50
        assert st.unique_queries == 8
        assert st.unique_docs == 50

    def test_concurrent_record_same_key(self):
        d = DocRelevanceScore()

        def worker():
            for i in range(100):
                d.record_score("q", "d", (i % 10) / 10.0)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # No duplicates despite contention
        assert d.stats().total_scores == 1

    def test_concurrent_record_and_delete(self):
        d = DocRelevanceScore()
        for i in range(100):
            d.record_score("q", f"d{i}", 0.5)

        def deleter(start: int):
            for i in range(start, start + 25):
                d.delete_score("q", f"d{i}")

        threads = [threading.Thread(target=deleter, args=(s,)) for s in (0, 25, 50, 75)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert d.stats().total_scores == 0
