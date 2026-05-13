"""Tests for docstoolkit.counterfactual_corpus module."""
import pytest

from docstoolkit.counterfactual_corpus.engine import (
    _token_overlap,
    _rank_passages,
    _classify_severity,
    QueryDelta,
    DecisionDelta,
    CounterfactualReport,
    counterfactual_remove,
    counterfactual_add,
)
from docstoolkit.counterfactual_corpus.cascade import (
    CascadeGraph,
    build_cascade_graph,
    find_cascade,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class FakePassage:
    """Minimal Passage-like object for testing _rank_passages."""
    def __init__(self, text: str, doc_id: str):
        self.text = text
        self.doc_id = doc_id


# ---------------------------------------------------------------------------
# _token_overlap
# ---------------------------------------------------------------------------

class TestTokenOverlap:
    def test_identical_strings(self):
        assert _token_overlap("hello world", "hello world") == 1.0

    def test_disjoint_strings(self):
        assert _token_overlap("apple banana", "cat dog") == 0.0

    def test_partial_overlap(self):
        score = _token_overlap("hello world", "hello python")
        assert 0.0 < score < 1.0

    def test_empty_both(self):
        assert _token_overlap("", "") == 1.0

    def test_empty_one_side(self):
        assert _token_overlap("hello", "") == 0.0
        assert _token_overlap("", "hello") == 0.0

    def test_case_insensitive(self):
        assert _token_overlap("Hello World", "hello world") == 1.0

    def test_punctuation_stripped(self):
        assert _token_overlap("hello, world!", "hello world") == 1.0

    def test_returns_float(self):
        result = _token_overlap("foo bar", "foo baz")
        assert isinstance(result, float)

    def test_symmetric(self):
        a, b = "cats and dogs", "dogs and fish"
        assert _token_overlap(a, b) == _token_overlap(b, a)


# ---------------------------------------------------------------------------
# _rank_passages
# ---------------------------------------------------------------------------

class TestRankPassages:
    def test_returns_list_of_tuples(self):
        passages = [FakePassage("python programming", "doc1")]
        result = _rank_passages("python", passages)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], tuple)
        assert isinstance(result[0][0], str)
        assert isinstance(result[0][1], float)

    def test_doc_with_query_terms_ranked_higher(self):
        passages = [
            FakePassage("javascript web frameworks", "doc1"),
            FakePassage("python machine learning algorithms", "doc2"),
        ]
        result = _rank_passages("python", passages)
        assert result[0][0] == "doc2"

    def test_sorted_descending(self):
        passages = [
            FakePassage("unrelated content foo", "doc1"),
            FakePassage("python python python programming", "doc2"),
            FakePassage("python code", "doc3"),
        ]
        result = _rank_passages("python", passages)
        scores = [score for _, score in result]
        assert scores == sorted(scores, reverse=True)

    def test_empty_passages(self):
        result = _rank_passages("anything", [])
        assert result == []

    def test_doc_id_in_result(self):
        passages = [FakePassage("test content", "my-doc")]
        result = _rank_passages("test", passages)
        assert result[0][0] == "my-doc"

    def test_irrelevant_query_gives_low_scores(self):
        passages = [FakePassage("python data science", "doc1")]
        result = _rank_passages("zzzzz nonexistent", passages)
        assert result[0][1] == 0.0


# ---------------------------------------------------------------------------
# QueryDelta / DecisionDelta / CounterfactualReport dataclasses
# ---------------------------------------------------------------------------

class TestDataclasses:
    def test_query_delta_fields(self):
        qd = QueryDelta(
            query="what is rag",
            baseline_top_doc="doc1",
            new_top_doc="doc2",
            rank_shift=1,
            affected=True,
        )
        assert qd.query == "what is rag"
        assert qd.baseline_top_doc == "doc1"
        assert qd.new_top_doc == "doc2"
        assert qd.rank_shift == 1
        assert qd.affected is True

    def test_decision_delta_fields(self):
        dd = DecisionDelta(
            decision_text="See doc1 for details",
            source_doc="doc1",
            severity="critical",
        )
        assert dd.decision_text == "See doc1 for details"
        assert dd.source_doc == "doc1"
        assert dd.severity == "critical"

    def test_counterfactual_report_fields(self):
        report = CounterfactualReport(
            action="remove",
            target_doc="doc1",
            affected_queries=[],
            affected_decisions=[],
            cascade_docs=[],
            severity="low",
            summary="test summary",
        )
        assert report.action == "remove"
        assert report.target_doc == "doc1"
        assert report.affected_queries == []
        assert report.cascade_docs == []
        assert report.severity == "low"
        assert report.summary == "test summary"

    def test_counterfactual_report_to_markdown_returns_string(self):
        report = CounterfactualReport(
            action="remove",
            target_doc="important-doc",
            affected_queries=[],
            affected_decisions=[],
            cascade_docs=[],
            severity="low",
            summary="Removing important-doc affects 0 queries.",
        )
        md = report.to_markdown()
        assert isinstance(md, str)

    def test_to_markdown_contains_target_doc(self):
        report = CounterfactualReport(
            action="remove",
            target_doc="crucial-paper",
            affected_queries=[],
            affected_decisions=[],
            cascade_docs=[],
            severity="medium",
            summary="Removing crucial-paper affects 1 query.",
        )
        md = report.to_markdown()
        assert "crucial-paper" in md

    def test_to_markdown_contains_action(self):
        report = CounterfactualReport(
            action="add",
            target_doc="new-doc",
            affected_queries=[],
            affected_decisions=[],
            cascade_docs=[],
            severity="low",
            summary="Adding new-doc.",
        )
        md = report.to_markdown()
        assert "add" in md.lower()

    def test_to_markdown_shows_cascade_docs(self):
        report = CounterfactualReport(
            action="remove",
            target_doc="pivot-doc",
            affected_queries=[],
            affected_decisions=[],
            cascade_docs=["child-doc-1", "child-doc-2"],
            severity="high",
            summary="test",
        )
        md = report.to_markdown()
        assert "child-doc-1" in md
        assert "child-doc-2" in md


# ---------------------------------------------------------------------------
# _classify_severity
# ---------------------------------------------------------------------------

class TestClassifySeverity:
    def test_low_zero_queries_zero_cascade(self):
        assert _classify_severity(0, 0) == "low"

    def test_medium_one_query(self):
        assert _classify_severity(1, 0) == "medium"

    def test_medium_two_queries(self):
        assert _classify_severity(2, 0) == "medium"

    def test_high_three_queries(self):
        assert _classify_severity(3, 0) == "high"

    def test_high_five_queries(self):
        assert _classify_severity(5, 0) == "high"

    def test_critical_six_queries(self):
        assert _classify_severity(6, 0) == "critical"

    def test_critical_many_queries(self):
        assert _classify_severity(10, 0) == "critical"

    def test_high_two_cascade_docs(self):
        assert _classify_severity(0, 2) == "high"

    def test_critical_four_cascade_docs(self):
        assert _classify_severity(0, 4) == "critical"

    def test_critical_cascade_overrides_low_queries(self):
        assert _classify_severity(1, 4) == "critical"


# ---------------------------------------------------------------------------
# counterfactual_remove
# ---------------------------------------------------------------------------

class TestCounterfactualRemove:
    def setup_method(self):
        self.docs = {
            "doc-python": "Python is a popular programming language for data science and ML.",
            "doc-java": "Java is widely used in enterprise software and backend systems.",
            "doc-rust": "Rust provides memory safety without a garbage collector.",
            "doc-central": "See doc-python for scripting. Also doc-java is referenced here.",
        }
        self.queries = [
            "python programming language",
            "enterprise backend java",
            "memory safety systems",
        ]

    def test_returns_counterfactual_report(self):
        report = counterfactual_remove("doc-rust", self.docs, self.queries)
        assert isinstance(report, CounterfactualReport)

    def test_action_is_remove(self):
        report = counterfactual_remove("doc-rust", self.docs, self.queries)
        assert report.action == "remove"

    def test_target_doc_set_correctly(self):
        report = counterfactual_remove("doc-python", self.docs, self.queries)
        assert report.target_doc == "doc-python"

    def test_cascade_docs_includes_referencing_docs(self):
        report = counterfactual_remove("doc-python", self.docs, self.queries)
        # doc-central mentions "doc-python"
        assert "doc-central" in report.cascade_docs

    def test_cascade_docs_excludes_target(self):
        report = counterfactual_remove("doc-python", self.docs, self.queries)
        assert "doc-python" not in report.cascade_docs

    def test_irrelevant_doc_low_severity(self):
        # Adding an unrelated doc to remove
        docs = dict(self.docs)
        docs["doc-unrelated"] = "xyzzy frobozz nonsense words"
        report = counterfactual_remove("doc-unrelated", docs, self.queries)
        # Should not affect relevant queries
        assert report.severity in ("low", "medium")

    def test_central_doc_has_more_affected_queries(self):
        report_python = counterfactual_remove("doc-python", self.docs, self.queries)
        report_rust = counterfactual_remove("doc-rust", self.docs, self.queries)
        # doc-python is more relevant to more queries
        n_affected_python = sum(1 for qd in report_python.affected_queries if qd.affected)
        n_affected_rust = sum(1 for qd in report_rust.affected_queries if qd.affected)
        assert n_affected_python >= n_affected_rust

    def test_affected_queries_length_matches_queries(self):
        report = counterfactual_remove("doc-rust", self.docs, self.queries)
        assert len(report.affected_queries) == len(self.queries)

    def test_summary_is_non_empty_string(self):
        report = counterfactual_remove("doc-rust", self.docs, self.queries)
        assert isinstance(report.summary, str)
        assert len(report.summary) > 0

    def test_summary_mentions_target_doc(self):
        report = counterfactual_remove("doc-java", self.docs, self.queries)
        assert "doc-java" in report.summary

    def test_decisions_with_target_reference(self):
        decisions = ["Refer to doc-python for scripting tasks"]
        report = counterfactual_remove(
            "doc-python", self.docs, self.queries, decisions=decisions
        )
        assert len(report.affected_decisions) == 1
        assert report.affected_decisions[0].source_doc == "doc-python"

    def test_decisions_without_target_reference(self):
        decisions = ["Refer to doc-java for enterprise tasks"]
        report = counterfactual_remove(
            "doc-python", self.docs, self.queries, decisions=decisions
        )
        assert len(report.affected_decisions) == 0

    def test_no_decisions_returns_empty_list(self):
        report = counterfactual_remove("doc-rust", self.docs, self.queries)
        assert report.affected_decisions == []

    def test_query_delta_affected_bool(self):
        report = counterfactual_remove("doc-python", self.docs, self.queries)
        for qd in report.affected_queries:
            assert isinstance(qd.affected, bool)

    def test_to_markdown_contains_target(self):
        report = counterfactual_remove("doc-rust", self.docs, self.queries)
        md = report.to_markdown()
        assert "doc-rust" in md


# ---------------------------------------------------------------------------
# counterfactual_add
# ---------------------------------------------------------------------------

class TestCounterfactualAdd:
    def setup_method(self):
        self.docs = {
            "doc-python": "Python is great for scripting.",
            "doc-java": "Java is used in enterprise systems.",
        }
        self.queries = ["machine learning python", "data science algorithms"]

    def test_returns_counterfactual_report(self):
        report = counterfactual_add("new-ml-doc", "machine learning algorithms python", self.docs, self.queries)
        assert isinstance(report, CounterfactualReport)

    def test_action_is_add(self):
        report = counterfactual_add("new-doc", "content here", self.docs, self.queries)
        assert report.action == "add"

    def test_target_doc_set(self):
        report = counterfactual_add("brand-new", "stuff", self.docs, self.queries)
        assert report.target_doc == "brand-new"

    def test_cascade_docs_empty_for_new_doc(self):
        report = counterfactual_add("new-doc", "machine learning", self.docs, self.queries)
        assert report.cascade_docs == []

    def test_relevant_new_doc_appears_in_affected_queries(self):
        # New doc is highly relevant to both queries
        report = counterfactual_add(
            "super-ml-doc",
            "machine learning python data science algorithms",
            self.docs,
            self.queries,
        )
        n_affected = sum(1 for qd in report.affected_queries if qd.affected)
        assert n_affected >= 1

    def test_affected_queries_are_query_delta_objects(self):
        report = counterfactual_add("new-doc", "content", self.docs, self.queries)
        for qd in report.affected_queries:
            assert isinstance(qd, QueryDelta)

    def test_affected_queries_length_matches_queries(self):
        report = counterfactual_add("new-doc", "content", self.docs, self.queries)
        assert len(report.affected_queries) == len(self.queries)

    def test_irrelevant_new_doc_no_affected_queries(self):
        report = counterfactual_add(
            "boring-doc", "xyzzy frobozz zork nonsense", self.docs, self.queries
        )
        n_affected = sum(1 for qd in report.affected_queries if qd.affected)
        assert n_affected == 0

    def test_summary_non_empty(self):
        report = counterfactual_add("new-doc", "content", self.docs, self.queries)
        assert isinstance(report.summary, str)
        assert len(report.summary) > 0

    def test_affected_decisions_empty(self):
        report = counterfactual_add("new-doc", "content", self.docs, self.queries)
        assert report.affected_decisions == []


# ---------------------------------------------------------------------------
# CascadeGraph
# ---------------------------------------------------------------------------

class TestCascadeGraph:
    def test_empty_graph_node_count(self):
        g = CascadeGraph()
        assert g.node_count() == 0

    def test_empty_graph_edge_count(self):
        g = CascadeGraph()
        assert g.edge_count() == 0

    def test_add_citation_forward(self):
        g = CascadeGraph()
        g.add_citation("doc-a", "doc-b")
        assert "doc-b" in g.citations_of("doc-a")

    def test_add_citation_reverse(self):
        g = CascadeGraph()
        g.add_citation("doc-a", "doc-b")
        assert "doc-a" in g.cited_by("doc-b")

    def test_cited_by_multiple_sources(self):
        g = CascadeGraph()
        g.add_citation("doc-a", "doc-c")
        g.add_citation("doc-b", "doc-c")
        sources = g.cited_by("doc-c")
        assert "doc-a" in sources
        assert "doc-b" in sources

    def test_citations_of_empty(self):
        g = CascadeGraph()
        assert g.citations_of("nonexistent") == []

    def test_cited_by_empty(self):
        g = CascadeGraph()
        assert g.cited_by("nonexistent") == []

    def test_node_count_after_add(self):
        g = CascadeGraph()
        g.add_citation("doc-a", "doc-b")
        assert g.node_count() == 2

    def test_edge_count_after_add(self):
        g = CascadeGraph()
        g.add_citation("doc-a", "doc-b")
        g.add_citation("doc-a", "doc-c")
        assert g.edge_count() == 2

    def test_no_duplicate_edges(self):
        g = CascadeGraph()
        g.add_citation("doc-a", "doc-b")
        g.add_citation("doc-a", "doc-b")  # duplicate
        assert g.edge_count() == 1

    def test_node_count_shared_node(self):
        g = CascadeGraph()
        g.add_citation("doc-a", "doc-b")
        g.add_citation("doc-b", "doc-c")
        # nodes: doc-a, doc-b, doc-c = 3
        assert g.node_count() == 3


# ---------------------------------------------------------------------------
# build_cascade_graph
# ---------------------------------------------------------------------------

class TestBuildCascadeGraph:
    def test_empty_docs(self):
        g = build_cascade_graph({})
        assert g.node_count() == 0
        assert g.edge_count() == 0

    def test_finds_mention(self):
        docs = {
            "doc-a": "This references doc-b for background.",
            "doc-b": "Independent document.",
        }
        g = build_cascade_graph(docs)
        assert "doc-b" in g.citations_of("doc-a")

    def test_reverse_lookup_correct(self):
        docs = {
            "doc-a": "See doc-b for more.",
            "doc-b": "See doc-c for more.",
            "doc-c": "Original source.",
        }
        g = build_cascade_graph(docs)
        assert "doc-a" in g.cited_by("doc-b")
        assert "doc-b" in g.cited_by("doc-c")

    def test_no_self_citation(self):
        docs = {"doc-a": "doc-a references itself somehow."}
        g = build_cascade_graph(docs)
        assert "doc-a" not in g.citations_of("doc-a")

    def test_no_cross_reference_gives_empty(self):
        docs = {
            "doc-a": "Apple banana cherry",
            "doc-b": "Dog elephant fish",
        }
        g = build_cascade_graph(docs)
        assert g.edge_count() == 0


# ---------------------------------------------------------------------------
# find_cascade
# ---------------------------------------------------------------------------

class TestFindCascade:
    def test_returns_list(self):
        g = CascadeGraph()
        result = find_cascade("doc-a", g)
        assert isinstance(result, list)

    def test_empty_graph_returns_empty(self):
        g = CascadeGraph()
        result = find_cascade("doc-x", g)
        assert result == []

    def test_target_not_in_result(self):
        g = CascadeGraph()
        g.add_citation("doc-b", "doc-a")
        result = find_cascade("doc-a", g)
        assert "doc-a" not in result

    def test_direct_dependents_found(self):
        g = CascadeGraph()
        g.add_citation("doc-b", "doc-a")
        result = find_cascade("doc-a", g)
        assert "doc-b" in result

    def test_transitive_dependents_found(self):
        g = CascadeGraph()
        g.add_citation("doc-b", "doc-a")
        g.add_citation("doc-c", "doc-b")
        result = find_cascade("doc-a", g)
        assert "doc-b" in result
        assert "doc-c" in result

    def test_max_depth_respected(self):
        # Chain: doc-a → cited by doc-b → cited by doc-c → cited by doc-d
        g = CascadeGraph()
        g.add_citation("doc-b", "doc-a")
        g.add_citation("doc-c", "doc-b")
        g.add_citation("doc-d", "doc-c")
        # With max_depth=1, only direct dependents (doc-b)
        result = find_cascade("doc-a", g, max_depth=1)
        assert "doc-b" in result
        assert "doc-c" not in result
        assert "doc-d" not in result

    def test_max_depth_two(self):
        g = CascadeGraph()
        g.add_citation("doc-b", "doc-a")
        g.add_citation("doc-c", "doc-b")
        g.add_citation("doc-d", "doc-c")
        result = find_cascade("doc-a", g, max_depth=2)
        assert "doc-b" in result
        assert "doc-c" in result
        assert "doc-d" not in result

    def test_no_dependents_returns_empty(self):
        g = CascadeGraph()
        g.add_citation("doc-a", "doc-b")  # doc-a cites doc-b, but nobody cites doc-a
        result = find_cascade("doc-a", g)
        assert result == []
