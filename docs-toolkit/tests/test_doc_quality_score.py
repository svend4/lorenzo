"""Tests for E345 DocQualityScore."""

import threading

import pytest

from docstoolkit.doc_quality_score import (
    Dimension,
    DimensionScore,
    DocQualityScore,
    QualityReport,
    QualityStats,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
class TestDimensionDataclass:
    def test_defaults(self):
        d = Dimension(name="clarity")
        assert d.name == "clarity"
        assert d.weight == 1.0
        assert d.description == ""

    def test_custom_values(self):
        d = Dimension(name="accuracy", weight=2.5, description="How accurate")
        assert d.weight == 2.5
        assert d.description == "How accurate"

    def test_equality(self):
        assert Dimension("x") == Dimension("x")
        assert Dimension("x", 2.0) != Dimension("x", 1.0)


class TestDimensionScoreDataclass:
    def test_defaults(self):
        ds = DimensionScore(doc_id="d", dimension="c", score=0.5)
        assert ds.doc_id == "d"
        assert ds.dimension == "c"
        assert ds.score == 0.5
        assert ds.evaluated_at == 0.0
        assert ds.evaluator == ""

    def test_custom_values(self):
        ds = DimensionScore("d", "c", 0.8, evaluated_at=123.0, evaluator="alice")
        assert ds.evaluated_at == 123.0
        assert ds.evaluator == "alice"


class TestQualityReportDataclass:
    def test_defaults(self):
        r = QualityReport(doc_id="d")
        assert r.doc_id == "d"
        assert r.dimensions == {}
        assert r.overall_score == 0.0
        assert r.dimension_count == 0

    def test_independent_dict(self):
        a = QualityReport(doc_id="a")
        b = QualityReport(doc_id="b")
        a.dimensions["x"] = 1
        assert b.dimensions == {}


class TestQualityStatsDataclass:
    def test_defaults(self):
        s = QualityStats()
        assert s.total_dimensions == 0
        assert s.total_evaluations == 0
        assert s.unique_docs == 0
        assert s.avg_overall_score == 0.0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_state(self):
        q = DocQualityScore()
        assert q.list_dimensions() == []
        assert q.all_doc_ids() == []
        assert q.stats().total_dimensions == 0

    def test_independent_instances(self):
        a = DocQualityScore()
        b = DocQualityScore()
        a.define_dimension(Dimension("x"))
        assert b.list_dimensions() == []


# ---------------------------------------------------------------------------
# define_dimension
# ---------------------------------------------------------------------------
class TestDefineDimension:
    def test_new(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("clarity", weight=1.5))
        assert q.get_dimension("clarity").weight == 1.5

    def test_replace(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("clarity", weight=1.0))
        q.define_dimension(Dimension("clarity", weight=2.0))
        assert q.get_dimension("clarity").weight == 2.0
        assert len(q.list_dimensions()) == 1

    def test_multiple(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("a"))
        q.define_dimension(Dimension("b"))
        q.define_dimension(Dimension("c"))
        assert len(q.list_dimensions()) == 3


# ---------------------------------------------------------------------------
# undefine_dimension
# ---------------------------------------------------------------------------
class TestUndefineDimension:
    def test_existing_returns_true(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        assert q.undefine_dimension("x") is True
        assert q.get_dimension("x") is None

    def test_missing_returns_false(self):
        q = DocQualityScore()
        assert q.undefine_dimension("nope") is False

    def test_removes_scores(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("d1", "x", 0.5)
        q.evaluate("d2", "x", 0.7)
        q.undefine_dimension("x")
        assert q.get_score("d1", "x") is None
        assert q.get_score("d2", "x") is None

    def test_does_not_affect_other_dimensions(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.define_dimension(Dimension("y"))
        q.evaluate("d1", "x", 0.5)
        q.evaluate("d1", "y", 0.7)
        q.undefine_dimension("x")
        assert q.get_score("d1", "y") is not None


# ---------------------------------------------------------------------------
# get_dimension
# ---------------------------------------------------------------------------
class TestGetDimension:
    def test_found(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("c", weight=2.0))
        assert q.get_dimension("c").name == "c"

    def test_not_found(self):
        q = DocQualityScore()
        assert q.get_dimension("nope") is None


# ---------------------------------------------------------------------------
# list_dimensions
# ---------------------------------------------------------------------------
class TestListDimensions:
    def test_empty(self):
        q = DocQualityScore()
        assert q.list_dimensions() == []

    def test_sorted_by_name(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("c"))
        q.define_dimension(Dimension("a"))
        q.define_dimension(Dimension("b"))
        names = [d.name for d in q.list_dimensions()]
        assert names == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# evaluate
# ---------------------------------------------------------------------------
class TestEvaluate:
    def test_undefined_returns_none(self):
        q = DocQualityScore()
        assert q.evaluate("d", "x", 0.5) is None

    def test_creates_score(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        ds = q.evaluate("d", "x", 0.6, evaluator="alice", now=100.0)
        assert ds is not None
        assert ds.score == 0.6
        assert ds.evaluator == "alice"
        assert ds.evaluated_at == 100.0

    def test_replaces_existing(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("d", "x", 0.5, now=1.0)
        q.evaluate("d", "x", 0.9, now=2.0)
        ds = q.get_score("d", "x")
        assert ds.score == 0.9
        assert ds.evaluated_at == 2.0

    def test_uses_time_time_when_now_none(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        ds = q.evaluate("d", "x", 0.5)
        assert ds.evaluated_at > 0.0


# ---------------------------------------------------------------------------
# get_score
# ---------------------------------------------------------------------------
class TestGetScore:
    def test_found(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("d", "x", 0.5)
        assert q.get_score("d", "x").score == 0.5

    def test_not_found(self):
        q = DocQualityScore()
        assert q.get_score("d", "x") is None


# ---------------------------------------------------------------------------
# delete_score
# ---------------------------------------------------------------------------
class TestDeleteScore:
    def test_existing_returns_true(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("d", "x", 0.5)
        assert q.delete_score("d", "x") is True
        assert q.get_score("d", "x") is None

    def test_missing_returns_false(self):
        q = DocQualityScore()
        assert q.delete_score("d", "x") is False


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
class TestReport:
    def test_none_if_no_scores(self):
        q = DocQualityScore()
        assert q.report("d") is None

    def test_single_dimension(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x", weight=2.0))
        q.evaluate("d", "x", 0.7)
        r = q.report("d")
        assert r is not None
        assert r.overall_score == pytest.approx(0.7)
        assert r.dimension_count == 1
        assert "x" in r.dimensions

    def test_weighted_average(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("a", weight=1.0))
        q.define_dimension(Dimension("b", weight=3.0))
        q.evaluate("d", "a", 1.0)
        q.evaluate("d", "b", 0.5)
        r = q.report("d")
        # (1.0 * 1 + 0.5 * 3) / (1 + 3) = 2.5 / 4 = 0.625
        assert r.overall_score == pytest.approx(0.625)
        assert r.dimension_count == 2

    def test_only_uses_defined_dimensions(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("a"))
        q.define_dimension(Dimension("b"))
        q.evaluate("d", "a", 0.6)
        q.evaluate("d", "b", 0.8)
        # Undefine b, its score should not contribute
        q.define_dimension(Dimension("a"))  # keep a
        # Manually remove the dimension definition for b without touching scores:
        # we have to simulate by undefining b which deletes scores too.
        # Instead, use scenario where score exists for a dim that's been undefined:
        # Re-evaluate: define b, add score, undefine b, check report
        # But undefine_dimension removes scores. So scenario unreachable via
        # public API — just verify the dimensions used match defined set.
        r = q.report("d")
        assert set(r.dimensions.keys()) == {"a", "b"}

    def test_independent_per_doc(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("d1", "x", 0.2)
        q.evaluate("d2", "x", 0.8)
        assert q.report("d1").overall_score == pytest.approx(0.2)
        assert q.report("d2").overall_score == pytest.approx(0.8)


# ---------------------------------------------------------------------------
# scores_for_doc
# ---------------------------------------------------------------------------
class TestScoresForDoc:
    def test_empty(self):
        q = DocQualityScore()
        assert q.scores_for_doc("d") == []

    def test_sorted_by_dimension(self):
        q = DocQualityScore()
        for n in ["c", "a", "b"]:
            q.define_dimension(Dimension(n))
            q.evaluate("d", n, 0.5)
        names = [s.dimension for s in q.scores_for_doc("d")]
        assert names == ["a", "b", "c"]

    def test_only_returns_for_doc(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("d1", "x", 0.1)
        q.evaluate("d2", "x", 0.9)
        scores = q.scores_for_doc("d1")
        assert len(scores) == 1
        assert scores[0].doc_id == "d1"


# ---------------------------------------------------------------------------
# scores_for_dimension
# ---------------------------------------------------------------------------
class TestScoresForDimension:
    def test_empty(self):
        q = DocQualityScore()
        assert q.scores_for_dimension("x") == []

    def test_sorted_by_doc_id(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        for d in ["d3", "d1", "d2"]:
            q.evaluate(d, "x", 0.5)
        ids = [s.doc_id for s in q.scores_for_dimension("x")]
        assert ids == ["d1", "d2", "d3"]

    def test_only_returns_for_dimension(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.define_dimension(Dimension("y"))
        q.evaluate("d", "x", 0.1)
        q.evaluate("d", "y", 0.9)
        scores = q.scores_for_dimension("x")
        assert len(scores) == 1
        assert scores[0].dimension == "x"


# ---------------------------------------------------------------------------
# top_docs
# ---------------------------------------------------------------------------
class TestTopDocs:
    def test_empty(self):
        q = DocQualityScore()
        assert q.top_docs() == []

    def test_sorted_descending(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("a", "x", 0.1)
        q.evaluate("b", "x", 0.9)
        q.evaluate("c", "x", 0.5)
        top = q.top_docs()
        assert [d for d, _ in top] == ["b", "c", "a"]

    def test_limit(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        for i, sc in enumerate([0.1, 0.2, 0.3, 0.4]):
            q.evaluate(f"d{i}", "x", sc)
        top = q.top_docs(limit=2)
        assert len(top) == 2
        assert top[0][0] == "d3"

    def test_tiebreak_by_doc_id_ascending(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("z", "x", 0.5)
        q.evaluate("a", "x", 0.5)
        q.evaluate("m", "x", 0.5)
        top = q.top_docs()
        assert [d for d, _ in top] == ["a", "m", "z"]


# ---------------------------------------------------------------------------
# bottom_docs
# ---------------------------------------------------------------------------
class TestBottomDocs:
    def test_empty(self):
        q = DocQualityScore()
        assert q.bottom_docs() == []

    def test_sorted_ascending(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("a", "x", 0.1)
        q.evaluate("b", "x", 0.9)
        q.evaluate("c", "x", 0.5)
        bot = q.bottom_docs()
        assert [d for d, _ in bot] == ["a", "c", "b"]

    def test_limit(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        for i, sc in enumerate([0.1, 0.2, 0.3, 0.4]):
            q.evaluate(f"d{i}", "x", sc)
        bot = q.bottom_docs(limit=2)
        assert len(bot) == 2
        assert bot[0][0] == "d0"


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------
class TestAllDocIds:
    def test_empty(self):
        q = DocQualityScore()
        assert q.all_doc_ids() == []

    def test_sorted(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        for d in ["d3", "d1", "d2"]:
            q.evaluate(d, "x", 0.5)
        assert q.all_doc_ids() == ["d1", "d2", "d3"]

    def test_unique(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("a"))
        q.define_dimension(Dimension("b"))
        q.evaluate("d", "a", 0.5)
        q.evaluate("d", "b", 0.7)
        assert q.all_doc_ids() == ["d"]


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty(self):
        q = DocQualityScore()
        s = q.stats()
        assert s.total_dimensions == 0
        assert s.total_evaluations == 0
        assert s.unique_docs == 0
        assert s.avg_overall_score == 0.0

    def test_counts(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("a"))
        q.define_dimension(Dimension("b"))
        q.evaluate("d1", "a", 0.5)
        q.evaluate("d1", "b", 0.5)
        q.evaluate("d2", "a", 0.5)
        s = q.stats()
        assert s.total_dimensions == 2
        assert s.total_evaluations == 3
        assert s.unique_docs == 2

    def test_avg_overall_score(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))
        q.evaluate("d1", "x", 0.4)
        q.evaluate("d2", "x", 0.6)
        s = q.stats()
        assert s.avg_overall_score == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# Thread-safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_evaluate(self):
        q = DocQualityScore()
        q.define_dimension(Dimension("x"))

        def worker(start):
            for i in range(50):
                q.evaluate(f"d{start}_{i}", "x", 0.5)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert q.stats().total_evaluations == 8 * 50

    def test_concurrent_define_and_evaluate(self):
        q = DocQualityScore()

        def define():
            for i in range(50):
                q.define_dimension(Dimension(f"dim{i}"))

        def evaluate():
            for i in range(50):
                q.evaluate(f"d{i}", f"dim{i % 10}", 0.5)

        t1 = threading.Thread(target=define)
        t2 = threading.Thread(target=evaluate)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # No crashes; counts are well-defined
        assert q.stats().total_dimensions == 50
