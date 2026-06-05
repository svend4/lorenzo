"""Tests for docstoolkit.got — Graph-of-Thoughts module."""
import pytest
from dataclasses import dataclass

from docstoolkit.got.node import ThoughtNode, NodeType
from docstoolkit.got.graph import ThoughtGraph
from docstoolkit.got.reasoner import GoTReasoner, ReasoningResult
from docstoolkit.got import ThoughtNode, NodeType, ThoughtGraph, GoTReasoner, ReasoningResult


# ---------------------------------------------------------------------------
# Passage helper (mirrors rag.types.Passage but standalone for test isolation)
# ---------------------------------------------------------------------------

@dataclass
class P:
    text: str
    doc_id: str
    title: str = ""
    score: float = 0.5


# ===========================================================================
# NodeType
# ===========================================================================

class TestNodeType:
    def test_five_values(self):
        values = list(NodeType)
        assert len(values) == 5

    def test_hypothesis_value(self):
        assert NodeType.HYPOTHESIS.value == "hypothesis"

    def test_fact_value(self):
        assert NodeType.FACT.value == "fact"

    def test_refuted_value(self):
        assert NodeType.REFUTED.value == "refuted"

    def test_refined_value(self):
        assert NodeType.REFINED.value == "refined"

    def test_synthesis_value(self):
        assert NodeType.SYNTHESIS.value == "synthesis"

    def test_is_str_subclass(self):
        # NodeType(str, Enum) — values are strings
        assert isinstance(NodeType.FACT, str)

    def test_values_are_lowercase(self):
        for nt in NodeType:
            assert nt.value == nt.value.lower()


# ===========================================================================
# ThoughtNode
# ===========================================================================

class TestThoughtNode:
    def _node(self, **kwargs) -> ThoughtNode:
        defaults = dict(node_id="n1", text="Some hypothesis")
        defaults.update(kwargs)
        return ThoughtNode(**defaults)

    def test_required_fields(self):
        n = self._node()
        assert n.node_id == "n1"
        assert n.text == "Some hypothesis"

    def test_default_node_type(self):
        n = self._node()
        assert n.node_type == NodeType.HYPOTHESIS

    def test_default_confidence(self):
        n = self._node()
        assert n.confidence == 0.5

    def test_default_source_passages_empty(self):
        n = self._node()
        assert n.source_passages == []

    def test_default_parent_ids_empty(self):
        n = self._node()
        assert n.parent_ids == []

    def test_default_children_ids_empty(self):
        n = self._node()
        assert n.children_ids == []

    def test_is_confirmed_false_for_hypothesis(self):
        n = self._node(node_type=NodeType.HYPOTHESIS)
        assert n.is_confirmed() is False

    def test_is_confirmed_true_for_fact(self):
        n = self._node(node_type=NodeType.FACT)
        assert n.is_confirmed() is True

    def test_is_confirmed_false_for_refuted(self):
        n = self._node(node_type=NodeType.REFUTED)
        assert n.is_confirmed() is False

    def test_is_refuted_false_for_hypothesis(self):
        n = self._node(node_type=NodeType.HYPOTHESIS)
        assert n.is_refuted() is False

    def test_is_refuted_true_for_refuted(self):
        n = self._node(node_type=NodeType.REFUTED)
        assert n.is_refuted() is True

    def test_is_refuted_false_for_fact(self):
        n = self._node(node_type=NodeType.FACT)
        assert n.is_refuted() is False

    def test_summary_contains_type(self):
        n = self._node(node_type=NodeType.FACT, confidence=0.9)
        s = n.summary()
        assert "[fact]" in s

    def test_summary_contains_confidence(self):
        n = self._node(confidence=0.75)
        s = n.summary()
        assert "0.75" in s

    def test_summary_truncates_text_at_80(self):
        long_text = "x" * 100
        n = self._node(text=long_text)
        s = n.summary()
        # The summary uses text[:80], so "x"*80 in s
        assert "x" * 80 in s
        assert "x" * 81 not in s

    def test_summary_format(self):
        n = self._node(node_type=NodeType.HYPOTHESIS, text="Test claim", confidence=0.50)
        s = n.summary()
        assert s == "[hypothesis] Test claim (conf=0.50)"

    def test_mutable_lists_not_shared(self):
        n1 = ThoughtNode(node_id="a", text="a")
        n2 = ThoughtNode(node_id="b", text="b")
        n1.parent_ids.append("x")
        assert n2.parent_ids == []

    def test_custom_confidence(self):
        n = self._node(confidence=0.99)
        assert n.confidence == 0.99


# ===========================================================================
# ThoughtGraph
# ===========================================================================

class TestThoughtGraph:
    def _graph_with_nodes(self):
        """Build a simple 3-node graph: root → child → grandchild."""
        g = ThoughtGraph()
        root = ThoughtNode(node_id="root", text="Root hypothesis")
        child = ThoughtNode(node_id="child", text="Child fact",
                            node_type=NodeType.FACT, parent_ids=["root"])
        grandchild = ThoughtNode(node_id="gc", text="Grandchild synthesis",
                                 node_type=NodeType.SYNTHESIS, parent_ids=["child"])
        g.add_node(root)
        g.add_node(child)
        g.add_node(grandchild)
        return g

    def test_empty_graph_node_count(self):
        g = ThoughtGraph()
        assert g.node_count() == 0

    def test_empty_graph_roots(self):
        g = ThoughtGraph()
        assert g.roots() == []

    def test_empty_graph_leaves(self):
        g = ThoughtGraph()
        assert g.leaves() == []

    def test_add_node_increments_count(self):
        g = ThoughtGraph()
        n = ThoughtNode(node_id="x", text="x")
        g.add_node(n)
        assert g.node_count() == 1

    def test_get_node_returns_correct_node(self):
        g = ThoughtGraph()
        n = ThoughtNode(node_id="abc", text="hello")
        g.add_node(n)
        result = g.get_node("abc")
        assert result is n

    def test_get_node_unknown_returns_none(self):
        g = ThoughtGraph()
        assert g.get_node("missing") is None

    def test_roots_no_parents(self):
        g = self._graph_with_nodes()
        roots = g.roots()
        assert len(roots) == 1
        assert roots[0].node_id == "root"

    def test_leaves_no_children(self):
        g = self._graph_with_nodes()
        leaves = g.leaves()
        assert len(leaves) == 1
        assert leaves[0].node_id == "gc"

    def test_add_node_updates_parent_children_ids(self):
        g = ThoughtGraph()
        parent = ThoughtNode(node_id="p", text="parent")
        g.add_node(parent)
        child = ThoughtNode(node_id="c", text="child", parent_ids=["p"])
        g.add_node(child)
        assert "c" in g.get_node("p").children_ids

    def test_add_node_no_duplicate_in_children(self):
        g = ThoughtGraph()
        parent = ThoughtNode(node_id="p", text="parent")
        g.add_node(parent)
        child = ThoughtNode(node_id="c", text="child", parent_ids=["p"])
        g.add_node(child)
        g.add_node(child)  # add again
        assert g.get_node("p").children_ids.count("c") == 1

    def test_node_count_multi(self):
        g = self._graph_with_nodes()
        assert g.node_count() == 3

    def test_path_to_root_for_root_node(self):
        g = self._graph_with_nodes()
        path = g.path_to_root("root")
        assert path == ["root"]

    def test_path_to_root_for_child(self):
        g = self._graph_with_nodes()
        path = g.path_to_root("child")
        assert path == ["child", "root"]

    def test_path_to_root_for_grandchild(self):
        g = self._graph_with_nodes()
        path = g.path_to_root("gc")
        # gc → child → root
        assert path == ["gc", "child", "root"]

    def test_path_to_root_unknown_node(self):
        g = self._graph_with_nodes()
        path = g.path_to_root("nonexistent")
        assert path == []

    def test_to_markdown_non_empty(self):
        g = self._graph_with_nodes()
        md = g.to_markdown()
        assert len(md) > 0

    def test_to_markdown_contains_root(self):
        g = self._graph_with_nodes()
        md = g.to_markdown()
        assert "Root hypothesis" in md

    def test_to_markdown_contains_child_indented(self):
        g = self._graph_with_nodes()
        md = g.to_markdown()
        # Child should be indented with 2 spaces
        assert "  - " in md

    def test_to_markdown_empty_graph(self):
        g = ThoughtGraph()
        md = g.to_markdown()
        assert md == ""

    def test_confirmed_facts_returns_only_facts(self):
        g = self._graph_with_nodes()
        facts = g.confirmed_facts()
        assert all(n.node_type == NodeType.FACT for n in facts)
        assert len(facts) == 1
        assert facts[0].node_id == "child"

    def test_refuted_nodes_returns_only_refuted(self):
        g = ThoughtGraph()
        r = ThoughtNode(node_id="r", text="refuted", node_type=NodeType.REFUTED)
        h = ThoughtNode(node_id="h", text="hypothesis")
        g.add_node(r)
        g.add_node(h)
        refuted = g.refuted_nodes()
        assert len(refuted) == 1
        assert refuted[0].node_id == "r"

    def test_confirmed_facts_empty_when_no_facts(self):
        g = ThoughtGraph()
        n = ThoughtNode(node_id="x", text="x")
        g.add_node(n)
        assert g.confirmed_facts() == []

    def test_refuted_nodes_empty_when_none(self):
        g = self._graph_with_nodes()
        assert g.refuted_nodes() == []


# ===========================================================================
# ReasoningResult
# ===========================================================================

class TestReasoningResult:
    def _make_result(self, fact_confidences=None, refuted=0):
        g = ThoughtGraph()
        for i, conf in enumerate(fact_confidences or []):
            n = ThoughtNode(node_id=f"f{i}", text=f"fact {i}",
                            node_type=NodeType.FACT, confidence=conf)
            g.add_node(n)
        for i in range(refuted):
            n = ThoughtNode(node_id=f"r{i}", text=f"refuted {i}",
                            node_type=NodeType.REFUTED)
            g.add_node(n)
        return ReasoningResult(
            query="test query",
            graph=g,
            final_answer="some answer",
            confirmed_count=len(fact_confidences or []),
            refuted_count=refuted,
        )

    def test_confidence_no_facts_returns_0_5(self):
        result = self._make_result(fact_confidences=[])
        assert result.confidence() == 0.5

    def test_confidence_single_fact(self):
        result = self._make_result(fact_confidences=[0.8])
        assert abs(result.confidence() - 0.8) < 1e-9

    def test_confidence_multiple_facts_average(self):
        result = self._make_result(fact_confidences=[0.6, 0.8])
        assert abs(result.confidence() - 0.7) < 1e-9

    def test_confirmed_count_field(self):
        result = self._make_result(fact_confidences=[0.7, 0.9])
        assert result.confirmed_count == 2

    def test_refuted_count_field(self):
        result = self._make_result(fact_confidences=[], refuted=3)
        assert result.refuted_count == 3

    def test_query_field(self):
        result = self._make_result()
        assert result.query == "test query"

    def test_final_answer_field(self):
        result = self._make_result()
        assert result.final_answer == "some answer"

    def test_synthesis_node_id_default_empty(self):
        result = self._make_result()
        assert result.synthesis_node_id == ""


# ===========================================================================
# GoTReasoner
# ===========================================================================

class TestGoTReasoner:
    def _passages(self):
        return [
            P("The memory system stores agent context persistently.", "doc1", score=0.8),
            P("Graph-of-thoughts enables multi-step reasoning over documents.", "doc2", score=0.7),
            P("RAG retrieval augments generation with relevant passages.", "doc3", score=0.6),
        ]

    def test_reason_returns_reasoning_result(self):
        r = GoTReasoner(self._passages())
        result = r.reason("memory system")
        assert isinstance(result, ReasoningResult)

    def test_reason_query_stored(self):
        r = GoTReasoner(self._passages())
        result = r.reason("memory system")
        assert result.query == "memory system"

    def test_reason_final_answer_non_empty(self):
        r = GoTReasoner(self._passages())
        result = r.reason("memory system")
        assert result.final_answer != ""

    def test_reason_synthesis_node_in_graph(self):
        r = GoTReasoner(self._passages())
        result = r.reason("memory system")
        synth = result.graph.get_node(result.synthesis_node_id)
        assert synth is not None
        assert synth.node_type == NodeType.SYNTHESIS

    def test_reason_with_and_produces_multiple_hypotheses(self):
        r = GoTReasoner(self._passages())
        result = r.reason("memory system and graph reasoning")
        # Should have at least 2 hypothesis nodes + synthesis
        assert result.graph.node_count() >= 3

    def test_reason_confirmed_plus_refuted_equals_hypothesis_nodes(self):
        r = GoTReasoner(self._passages())
        result = r.reason("memory system and graph reasoning and RAG retrieval")
        assert result.confirmed_count + result.refuted_count == (
            result.graph.node_count() - 1  # -1 for synthesis
        )

    def test_reason_with_relevant_passages_has_fact(self):
        # Passages closely matching the query
        passages = [P("memory agent stores context memory", "doc1", score=0.9)]
        r = GoTReasoner(passages)
        result = r.reason("memory agent context")
        assert result.confirmed_count >= 1

    def test_reason_synthesis_type(self):
        r = GoTReasoner(self._passages())
        result = r.reason("memory")
        synth_node = result.graph.get_node("synthesis")
        assert synth_node.node_type == NodeType.SYNTHESIS

    def test_reason_empty_passages_all_refuted(self):
        r = GoTReasoner([])
        result = r.reason("memory and graph")
        assert result.confirmed_count == 0
        assert result.refuted_count >= 1

    def test_reason_max_hypotheses_respected(self):
        r = GoTReasoner(self._passages())
        result = r.reason("a, b, c, d, e, f, g", max_hypotheses=3)
        # node_count = max_hypotheses (3) + 1 synthesis = 4
        assert result.graph.node_count() <= 4

    def test_decompose_single_word(self):
        r = GoTReasoner([])
        result = r._decompose("memory", max_hypotheses=5)
        assert result == ["memory"]

    def test_decompose_and_split(self):
        r = GoTReasoner([])
        parts = r._decompose("memory and graph", max_hypotheses=5)
        assert len(parts) == 2

    def test_decompose_comma_split(self):
        r = GoTReasoner([])
        parts = r._decompose("memory, graph, rag", max_hypotheses=5)
        assert len(parts) == 3

    def test_decompose_question_split(self):
        r = GoTReasoner([])
        parts = r._decompose("what is memory? how does it work", max_hypotheses=5)
        assert len(parts) == 2

    def test_decompose_limits_to_max(self):
        r = GoTReasoner([])
        parts = r._decompose("a, b, c, d, e, f", max_hypotheses=3)
        assert len(parts) == 3

    def test_decompose_strips_whitespace(self):
        r = GoTReasoner([])
        parts = r._decompose("  memory  and  graph  ", max_hypotheses=5)
        for p in parts:
            assert p == p.strip()

    def test_decompose_filters_empty(self):
        r = GoTReasoner([])
        parts = r._decompose("memory and graph", max_hypotheses=5)
        for p in parts:
            assert p != ""

    def test_decompose_lowercases(self):
        r = GoTReasoner([])
        parts = r._decompose("Memory and Graph", max_hypotheses=5)
        assert all(p == p.lower() for p in parts)

    def test_find_support_empty_passages(self):
        r = GoTReasoner([])
        passage, score = r._find_support("memory")
        assert passage is None
        assert score == 0.0

    def test_find_support_returns_best_match(self):
        passages = [
            P("memory stores context", "doc1", score=0.9),
            P("graph visualization tool", "doc2", score=0.6),
        ]
        r = GoTReasoner(passages)
        passage, score = r._find_support("memory context")
        assert passage.doc_id == "doc1"

    def test_find_support_score_positive_for_overlap(self):
        passages = [P("memory stores context", "doc1", score=0.9)]
        r = GoTReasoner(passages)
        _, score = r._find_support("memory context")
        assert score > 0.0

    def test_find_support_no_overlap_score_zero(self):
        passages = [P("xyz abc def", "doc1", score=0.9)]
        r = GoTReasoner(passages)
        _, score = r._find_support("memory context")
        assert score == 0.0

    def test_token_set_filters_short_words(self):
        r = GoTReasoner([])
        tokens = r._token_set("a ab abc abcd")
        assert "a" not in tokens
        assert "ab" not in tokens
        assert "abc" in tokens
        assert "abcd" in tokens

    def test_token_set_lowercases(self):
        r = GoTReasoner([])
        tokens = r._token_set("Memory GRAPH Rag")
        assert "memory" in tokens
        assert "graph" in tokens
        assert "rag" in tokens

    def test_token_set_empty_string(self):
        r = GoTReasoner([])
        tokens = r._token_set("")
        assert tokens == set()

    def test_jaccard_empty_both(self):
        r = GoTReasoner([])
        assert r._jaccard(set(), set()) == 0.0

    def test_jaccard_identical(self):
        r = GoTReasoner([])
        s = {"memory", "graph", "rag"}
        assert r._jaccard(s, s) == 1.0

    def test_jaccard_no_overlap(self):
        r = GoTReasoner([])
        a = {"memory", "graph"}
        b = {"rag", "pipeline"}
        assert r._jaccard(a, b) == 0.0

    def test_jaccard_partial_overlap(self):
        r = GoTReasoner([])
        a = {"memory", "graph", "rag"}
        b = {"memory", "graph", "pipeline"}
        # intersection=2, union=4
        assert abs(r._jaccard(a, b) - 0.5) < 1e-9

    def test_jaccard_one_empty(self):
        r = GoTReasoner([])
        a = {"memory"}
        b = set()
        # union = 1, inter = 0
        assert r._jaccard(a, b) == 0.0

    def test_reason_graph_has_synthesis_as_leaf(self):
        r = GoTReasoner(self._passages())
        result = r.reason("memory and graph")
        leaves = result.graph.leaves()
        leaf_ids = [n.node_id for n in leaves]
        assert "synthesis" in leaf_ids

    def test_reason_confidence_with_facts_between_0_and_1(self):
        passages = [P("memory agent stores context memory", "doc1", score=0.8)]
        r = GoTReasoner(passages)
        result = r.reason("memory agent context")
        conf = result.confidence()
        assert 0.0 <= conf <= 1.0
