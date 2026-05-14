"""Tests for E376 DocPriorityScore."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_priority_score import (
    DocPriorityScore,
    PriorityScore,
    PriorityStats,
    ScoreFactor,
)


# ---------------------------------------------------------------- dataclasses
class TestScoreFactorDataclass:
    def test_minimal(self):
        f = ScoreFactor(name="recency")
        assert f.name == "recency"
        assert f.weight == 1.0
        assert f.description == ""

    def test_full(self):
        f = ScoreFactor(name="freshness", weight=2.5, description="how new")
        assert f.weight == 2.5
        assert f.description == "how new"

    def test_equality(self):
        a = ScoreFactor(name="x", weight=1.0)
        b = ScoreFactor(name="x", weight=1.0)
        assert a == b

    def test_inequality(self):
        a = ScoreFactor(name="x", weight=1.0)
        b = ScoreFactor(name="x", weight=2.0)
        assert a != b


class TestPriorityScoreDataclass:
    def test_defaults(self):
        s = PriorityScore(doc_id="d1", total_score=3.0)
        assert s.doc_id == "d1"
        assert s.total_score == 3.0
        assert s.factor_scores == {}
        assert s.computed_at == 0.0

    def test_full(self):
        s = PriorityScore(
            doc_id="d2", total_score=5.0, factor_scores={"a": 2.0}, computed_at=100.0
        )
        assert s.factor_scores == {"a": 2.0}
        assert s.computed_at == 100.0

    def test_independent_dicts(self):
        a = PriorityScore(doc_id="a", total_score=0.0)
        b = PriorityScore(doc_id="b", total_score=0.0)
        a.factor_scores["x"] = 1.0
        assert "x" not in b.factor_scores


class TestPriorityStatsDataclass:
    def test_basic(self):
        s = PriorityStats(total_factors=2, total_scores=3, unique_docs=4, avg_score=5.5)
        assert s.total_factors == 2
        assert s.total_scores == 3
        assert s.unique_docs == 4
        assert s.avg_score == 5.5


# ----------------------------------------------------------------- construction
class TestConstruction:
    def test_empty(self):
        store = DocPriorityScore()
        assert store.list_factors() == []
        assert store.all_doc_ids() == []

    def test_isolated_instances(self):
        a = DocPriorityScore()
        b = DocPriorityScore()
        a.define_factor(ScoreFactor(name="x"))
        assert b.list_factors() == []


# ---------------------------------------------------------------- define_factor
class TestDefineFactor:
    def test_define_one(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=1.5))
        assert s.get_factor("a") is not None

    def test_define_replaces(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=1.0))
        s.define_factor(ScoreFactor(name="a", weight=3.0))
        assert s.get_factor("a").weight == 3.0

    def test_define_invalidates_cache(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=1.0))
        s.set_value("d", "a", 2.0)
        s.compute("d")
        assert "d" in s._cached_scores
        s.define_factor(ScoreFactor(name="b", weight=2.0))
        assert "d" not in s._cached_scores


# ---------------------------------------------------------------- remove_factor
class TestRemoveFactor:
    def test_remove_unknown(self):
        s = DocPriorityScore()
        assert s.remove_factor("nope") is False

    def test_remove_existing(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        assert s.remove_factor("a") is True
        assert s.get_factor("a") is None

    def test_remove_cascades_values(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.define_factor(ScoreFactor(name="b"))
        s.set_value("d1", "a", 1.0)
        s.set_value("d1", "b", 2.0)
        s.set_value("d2", "a", 3.0)
        s.remove_factor("a")
        assert s.get_value("d1", "a") is None
        assert s.get_value("d2", "a") is None
        assert s.get_value("d1", "b") == 2.0

    def test_remove_clears_affected_cache(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d1", "a", 1.0)
        s.compute("d1")
        assert "d1" in s._cached_scores
        s.remove_factor("a")
        assert "d1" not in s._cached_scores


# ------------------------------------------------------------------- get_factor
class TestGetFactor:
    def test_found(self):
        s = DocPriorityScore()
        f = ScoreFactor(name="x", weight=2.0)
        s.define_factor(f)
        assert s.get_factor("x") == f

    def test_not_found(self):
        s = DocPriorityScore()
        assert s.get_factor("missing") is None


# ------------------------------------------------------------------ list_factors
class TestListFactors:
    def test_empty(self):
        s = DocPriorityScore()
        assert s.list_factors() == []

    def test_sorted(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="z"))
        s.define_factor(ScoreFactor(name="a"))
        s.define_factor(ScoreFactor(name="m"))
        names = [f.name for f in s.list_factors()]
        assert names == ["a", "m", "z"]


# --------------------------------------------------------------------- set_value
class TestSetValue:
    def test_undefined_factor_returns_false(self):
        s = DocPriorityScore()
        assert s.set_value("d", "missing", 1.0) is False

    def test_defined_factor_returns_true(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        assert s.set_value("d", "a", 1.0) is True

    def test_value_stored(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d", "a", 4.0)
        assert s.get_value("d", "a") == 4.0

    def test_set_invalidates_cache(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=1.0))
        s.set_value("d", "a", 1.0)
        s.compute("d")
        assert "d" in s._cached_scores
        s.set_value("d", "a", 5.0)
        assert "d" not in s._cached_scores

    def test_overwrite(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d", "a", 1.0)
        s.set_value("d", "a", 2.5)
        assert s.get_value("d", "a") == 2.5


# --------------------------------------------------------------------- get_value
class TestGetValue:
    def test_found(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d", "a", 3.0)
        assert s.get_value("d", "a") == 3.0

    def test_not_found(self):
        s = DocPriorityScore()
        assert s.get_value("d", "a") is None

    def test_not_found_other_doc(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d1", "a", 1.0)
        assert s.get_value("d2", "a") is None


# ----------------------------------------------------------------------- compute
class TestCompute:
    def test_weighted_sum(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=2.0))
        s.define_factor(ScoreFactor(name="b", weight=3.0))
        s.set_value("d", "a", 1.0)
        s.set_value("d", "b", 4.0)
        score = s.compute("d")
        assert score.total_score == 1.0 * 2.0 + 4.0 * 3.0

    def test_factor_scores_dict(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=2.0))
        s.set_value("d", "a", 3.0)
        score = s.compute("d")
        assert score.factor_scores == {"a": 6.0}

    def test_empty_doc(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        score = s.compute("never_set")
        assert score.total_score == 0.0
        assert score.factor_scores == {}

    def test_computed_at_now(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d", "a", 1.0)
        score = s.compute("d", now=42.0)
        assert score.computed_at == 42.0

    def test_computed_at_auto(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d", "a", 1.0)
        score = s.compute("d")
        assert score.computed_at > 0.0

    def test_caches_result(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d", "a", 1.0)
        s.compute("d")
        assert "d" in s._cached_scores


# --------------------------------------------------------------------- score_for
class TestScoreFor:
    def test_returns_cached(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d", "a", 1.0)
        first = s.compute("d", now=10.0)
        second = s.score_for("d", now=99.0)
        assert second is first
        assert second.computed_at == 10.0

    def test_computes_if_not_cached(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=2.0))
        s.set_value("d", "a", 3.0)
        score = s.score_for("d", now=5.0)
        assert score is not None
        assert score.total_score == 6.0

    def test_none_for_unknown_doc(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        assert s.score_for("nothing") is None


# --------------------------------------------------------------------- clear_doc
class TestClearDoc:
    def test_clears_count(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.define_factor(ScoreFactor(name="b"))
        s.set_value("d", "a", 1.0)
        s.set_value("d", "b", 2.0)
        assert s.clear_doc("d") == 2

    def test_clears_zero(self):
        s = DocPriorityScore()
        assert s.clear_doc("ghost") == 0

    def test_clears_cache(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d", "a", 1.0)
        s.compute("d")
        s.clear_doc("d")
        assert "d" not in s._cached_scores

    def test_does_not_affect_others(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d1", "a", 1.0)
        s.set_value("d2", "a", 2.0)
        s.clear_doc("d1")
        assert s.get_value("d2", "a") == 2.0


# ---------------------------------------------------------------------- top_docs
class TestTopDocs:
    def test_sorted_desc(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=1.0))
        s.set_value("d1", "a", 1.0)
        s.set_value("d2", "a", 5.0)
        s.set_value("d3", "a", 3.0)
        top = s.top_docs()
        assert [d for d, _ in top] == ["d2", "d3", "d1"]

    def test_limit(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        for i in range(5):
            s.set_value(f"d{i}", "a", float(i))
        top = s.top_docs(limit=2)
        assert len(top) == 2

    def test_tie_break_by_doc_id_asc(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("b", "a", 1.0)
        s.set_value("a", "a", 1.0)
        s.set_value("c", "a", 1.0)
        top = s.top_docs()
        assert [d for d, _ in top] == ["a", "b", "c"]

    def test_empty(self):
        s = DocPriorityScore()
        assert s.top_docs() == []


# ------------------------------------------------------------------- bottom_docs
class TestBottomDocs:
    def test_sorted_asc(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d1", "a", 1.0)
        s.set_value("d2", "a", 5.0)
        s.set_value("d3", "a", 3.0)
        bot = s.bottom_docs()
        assert [d for d, _ in bot] == ["d1", "d3", "d2"]

    def test_limit(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        for i in range(5):
            s.set_value(f"d{i}", "a", float(i))
        bot = s.bottom_docs(limit=3)
        assert len(bot) == 3

    def test_empty(self):
        s = DocPriorityScore()
        assert s.bottom_docs() == []


# ------------------------------------------------------------------- all_doc_ids
class TestAllDocIds:
    def test_sorted(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("z", "a", 1.0)
        s.set_value("a", "a", 1.0)
        s.set_value("m", "a", 1.0)
        assert s.all_doc_ids() == ["a", "m", "z"]

    def test_empty(self):
        s = DocPriorityScore()
        assert s.all_doc_ids() == []

    def test_unique(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.define_factor(ScoreFactor(name="b"))
        s.set_value("d", "a", 1.0)
        s.set_value("d", "b", 2.0)
        assert s.all_doc_ids() == ["d"]


# ------------------------------------------------------------------------- stats
class TestStats:
    def test_empty(self):
        s = DocPriorityScore()
        st = s.stats()
        assert st.total_factors == 0
        assert st.unique_docs == 0
        assert st.avg_score == 0.0

    def test_factors_count(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.define_factor(ScoreFactor(name="b"))
        assert s.stats().total_factors == 2

    def test_unique_docs(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d1", "a", 1.0)
        s.set_value("d2", "a", 2.0)
        assert s.stats().unique_docs == 2

    def test_avg_score(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=1.0))
        s.set_value("d1", "a", 2.0)
        s.set_value("d2", "a", 4.0)
        assert s.stats().avg_score == 3.0

    def test_total_scores_after_compute(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a"))
        s.set_value("d1", "a", 1.0)
        s.stats()  # triggers compute internally
        assert s.stats().total_scores >= 1


# ----------------------------------------------------------------- thread safety
class TestThreadSafety:
    def test_concurrent_set_value(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=1.0))

        def worker(i: int):
            for j in range(50):
                s.set_value(f"d{i}", "a", float(j))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All 8 docs should have a final value of 49.0
        for i in range(8):
            assert s.get_value(f"d{i}", "a") == 49.0
        assert len(s.all_doc_ids()) == 8

    def test_concurrent_define_and_set(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=1.0))

        def writer():
            for i in range(100):
                s.set_value(f"d{i}", "a", 1.0)

        def definer():
            for i in range(50):
                s.define_factor(ScoreFactor(name=f"f{i}", weight=1.0))

        t1 = threading.Thread(target=writer)
        t2 = threading.Thread(target=definer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert len(s.all_doc_ids()) == 100
        assert s.get_factor("a") is not None

    def test_concurrent_compute(self):
        s = DocPriorityScore()
        s.define_factor(ScoreFactor(name="a", weight=2.0))
        for i in range(20):
            s.set_value(f"d{i}", "a", float(i))

        results = []
        lock = threading.Lock()

        def worker():
            for i in range(20):
                sc = s.compute(f"d{i}")
                with lock:
                    results.append(sc.total_score)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 80
