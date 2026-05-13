"""Tests for docstoolkit.intent_graph (E22)."""
from __future__ import annotations

import pytest

from docstoolkit.intent_graph import (
    IntentEdge,
    IntentGraph,
    IntentGraphBuilder,
    IntentNode,
    IntentNodeType,
)


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def simple_node() -> IntentNode:
    return IntentNode(node_type=IntentNodeType.CONCEPT, label="memory")


@pytest.fixture
def another_node() -> IntentNode:
    return IntentNode(node_type=IntentNodeType.ENTITY, label="AgentFS")


@pytest.fixture
def query_node() -> IntentNode:
    return IntentNode(node_type=IntentNodeType.QUERY, label="find memory agents")


@pytest.fixture
def empty_graph() -> IntentGraph:
    return IntentGraph()


@pytest.fixture
def graph_with_nodes(simple_node, another_node, query_node) -> IntentGraph:
    g = IntentGraph()
    g.add_node(query_node)
    g.add_node(simple_node)
    g.add_node(another_node)
    return g


@pytest.fixture
def builder() -> IntentGraphBuilder:
    return IntentGraphBuilder()


# ===========================================================================
# IntentNodeType enum
# ===========================================================================


class TestIntentNodeType:
    def test_all_values_present(self):
        values = {t.value for t in IntentNodeType}
        assert values == {"QUERY", "CONCEPT", "ENTITY", "ACTION", "FILTER"}

    def test_string_comparison(self):
        assert IntentNodeType.QUERY == "QUERY"

    def test_from_string(self):
        assert IntentNodeType("CONCEPT") is IntentNodeType.CONCEPT

    def test_uniqueness(self):
        types = list(IntentNodeType)
        assert len(types) == len(set(types))


# ===========================================================================
# IntentNode
# ===========================================================================


class TestIntentNode:
    def test_auto_node_id_generated(self, simple_node):
        assert simple_node.node_id is not None
        assert len(simple_node.node_id) == 8

    def test_node_id_is_hex(self, simple_node):
        int(simple_node.node_id, 16)  # raises ValueError if not hex

    def test_two_nodes_have_different_ids(self):
        a = IntentNode(node_type=IntentNodeType.CONCEPT, label="alpha")
        b = IntentNode(node_type=IntentNodeType.CONCEPT, label="alpha")
        assert a.node_id != b.node_id

    def test_default_weight(self, simple_node):
        assert simple_node.weight == 1.0

    def test_default_metadata_is_empty_dict(self, simple_node):
        assert simple_node.metadata == {}

    def test_metadata_not_shared_between_instances(self):
        a = IntentNode(node_type=IntentNodeType.CONCEPT, label="a")
        b = IntentNode(node_type=IntentNodeType.CONCEPT, label="b")
        a.metadata["key"] = "val"
        assert "key" not in b.metadata

    def test_custom_weight(self):
        n = IntentNode(node_type=IntentNodeType.ACTION, label="find", weight=2.5)
        assert n.weight == 2.5

    def test_custom_metadata(self):
        n = IntentNode(
            node_type=IntentNodeType.FILTER, label="date", metadata={"range": "2024"}
        )
        assert n.metadata["range"] == "2024"

    def test_hash_based_on_node_id(self, simple_node):
        assert hash(simple_node) == hash(simple_node.node_id)

    def test_equality_same_node(self, simple_node):
        assert simple_node == simple_node

    def test_equality_same_id(self):
        a = IntentNode(node_type=IntentNodeType.CONCEPT, label="alpha")
        b = IntentNode(node_type=IntentNodeType.CONCEPT, label="beta")
        b.node_id = a.node_id  # force same id
        assert a == b

    def test_inequality_different_ids(self):
        a = IntentNode(node_type=IntentNodeType.CONCEPT, label="alpha")
        b = IntentNode(node_type=IntentNodeType.CONCEPT, label="alpha")
        assert a != b

    def test_usable_in_set(self):
        a = IntentNode(node_type=IntentNodeType.CONCEPT, label="x")
        b = IntentNode(node_type=IntentNodeType.CONCEPT, label="x")
        s = {a, b}
        assert len(s) == 2

    def test_usable_as_dict_key(self, simple_node):
        d = {simple_node: "value"}
        assert d[simple_node] == "value"

    def test_node_type_assigned(self):
        n = IntentNode(node_type=IntentNodeType.ENTITY, label="GPT")
        assert n.node_type is IntentNodeType.ENTITY

    def test_label_assigned(self):
        n = IntentNode(node_type=IntentNodeType.QUERY, label="what is RAG")
        assert n.label == "what is RAG"


# ===========================================================================
# IntentEdge
# ===========================================================================


class TestIntentEdge:
    def test_fields(self):
        e = IntentEdge(source_id="aaa", target_id="bbb", relation="contains")
        assert e.source_id == "aaa"
        assert e.target_id == "bbb"
        assert e.relation == "contains"

    def test_default_weight(self):
        e = IntentEdge(source_id="a", target_id="b", relation="r")
        assert e.weight == 1.0

    def test_custom_weight(self):
        e = IntentEdge(source_id="a", target_id="b", relation="r", weight=0.5)
        assert e.weight == 0.5


# ===========================================================================
# IntentGraph — basic operations
# ===========================================================================


class TestIntentGraphBasic:
    def test_empty_graph_node_count(self, empty_graph):
        assert empty_graph.node_count() == 0

    def test_empty_graph_edge_count(self, empty_graph):
        assert empty_graph.edge_count() == 0

    def test_add_node_increments_count(self, empty_graph, simple_node):
        empty_graph.add_node(simple_node)
        assert empty_graph.node_count() == 1

    def test_add_node_idempotent(self, empty_graph, simple_node):
        empty_graph.add_node(simple_node)
        empty_graph.add_node(simple_node)
        assert empty_graph.node_count() == 1

    def test_get_node_returns_node(self, graph_with_nodes, simple_node):
        assert graph_with_nodes.get_node(simple_node.node_id) is simple_node

    def test_get_node_missing_returns_none(self, empty_graph):
        assert empty_graph.get_node("nonexistent") is None

    def test_add_edge_increments_count(self, graph_with_nodes, simple_node, another_node):
        g = graph_with_nodes
        edge = IntentEdge(
            source_id=simple_node.node_id,
            target_id=another_node.node_id,
            relation="links",
        )
        g.add_edge(edge)
        assert g.edge_count() == 1

    def test_multiple_edges(self, graph_with_nodes, simple_node, another_node, query_node):
        g = graph_with_nodes
        g.add_edge(IntentEdge(simple_node.node_id, another_node.node_id, "a"))
        g.add_edge(IntentEdge(query_node.node_id, simple_node.node_id, "b"))
        assert g.edge_count() == 2


# ===========================================================================
# IntentGraph — neighbors & edges_from
# ===========================================================================


class TestIntentGraphNeighbors:
    def _build_trio(self) -> tuple[IntentGraph, IntentNode, IntentNode, IntentNode]:
        g = IntentGraph()
        a = IntentNode(node_type=IntentNodeType.QUERY, label="q")
        b = IntentNode(node_type=IntentNodeType.CONCEPT, label="c")
        c = IntentNode(node_type=IntentNodeType.ENTITY, label="e")
        for n in (a, b, c):
            g.add_node(n)
        return g, a, b, c

    def test_neighbors_outgoing(self):
        g, a, b, c = self._build_trio()
        g.add_edge(IntentEdge(a.node_id, b.node_id, "contains"))
        neighbors = g.neighbors(a.node_id)
        assert b in neighbors

    def test_neighbors_incoming(self):
        g, a, b, c = self._build_trio()
        g.add_edge(IntentEdge(a.node_id, b.node_id, "contains"))
        # b's neighbor should include a (incoming edge)
        neighbors = g.neighbors(b.node_id)
        assert a in neighbors

    def test_neighbors_both_directions(self):
        g, a, b, c = self._build_trio()
        g.add_edge(IntentEdge(a.node_id, b.node_id, "contains"))
        g.add_edge(IntentEdge(c.node_id, a.node_id, "links"))
        neighbors = g.neighbors(a.node_id)
        assert b in neighbors
        assert c in neighbors

    def test_neighbors_no_duplicates(self):
        g, a, b, c = self._build_trio()
        g.add_edge(IntentEdge(a.node_id, b.node_id, "r1"))
        g.add_edge(IntentEdge(a.node_id, b.node_id, "r2"))
        # b should appear only once in neighbors of a
        neighbors = g.neighbors(a.node_id)
        assert neighbors.count(b) == 1

    def test_neighbors_isolated_node(self):
        g, a, b, c = self._build_trio()
        assert g.neighbors(a.node_id) == []

    def test_edges_from_correct(self):
        g, a, b, c = self._build_trio()
        e1 = IntentEdge(a.node_id, b.node_id, "contains")
        e2 = IntentEdge(a.node_id, c.node_id, "mentions")
        g.add_edge(e1)
        g.add_edge(e2)
        edges = g.edges_from(a.node_id)
        assert len(edges) == 2
        relations = {e.relation for e in edges}
        assert relations == {"contains", "mentions"}

    def test_edges_from_empty_for_no_out_edges(self):
        g, a, b, c = self._build_trio()
        g.add_edge(IntentEdge(a.node_id, b.node_id, "r"))
        # b has no outgoing edges
        assert g.edges_from(b.node_id) == []

    def test_edges_from_unknown_id_returns_empty(self):
        g, *_ = self._build_trio()
        assert g.edges_from("ghost") == []


# ===========================================================================
# IntentGraph — nodes_by_type
# ===========================================================================


class TestIntentGraphNodesByType:
    def test_nodes_by_type_concept(self, graph_with_nodes, simple_node):
        concepts = graph_with_nodes.nodes_by_type(IntentNodeType.CONCEPT)
        assert simple_node in concepts

    def test_nodes_by_type_entity(self, graph_with_nodes, another_node):
        entities = graph_with_nodes.nodes_by_type(IntentNodeType.ENTITY)
        assert another_node in entities

    def test_nodes_by_type_empty_type(self, graph_with_nodes):
        actions = graph_with_nodes.nodes_by_type(IntentNodeType.ACTION)
        assert actions == []

    def test_nodes_by_type_query(self, graph_with_nodes, query_node):
        queries = graph_with_nodes.nodes_by_type(IntentNodeType.QUERY)
        assert query_node in queries


# ===========================================================================
# IntentGraph — to_dict
# ===========================================================================


class TestIntentGraphToDict:
    def test_to_dict_structure(self, graph_with_nodes):
        d = graph_with_nodes.to_dict()
        assert "nodes" in d
        assert "edges" in d

    def test_to_dict_node_fields(self, empty_graph, simple_node):
        empty_graph.add_node(simple_node)
        d = empty_graph.to_dict()
        node_d = d["nodes"][0]
        assert "node_id" in node_d
        assert "node_type" in node_d
        assert "label" in node_d
        assert "weight" in node_d
        assert "metadata" in node_d

    def test_to_dict_edge_fields(self, graph_with_nodes, simple_node, another_node):
        g = graph_with_nodes
        g.add_edge(IntentEdge(simple_node.node_id, another_node.node_id, "links"))
        edge_d = g.to_dict()["edges"][0]
        assert "source_id" in edge_d
        assert "target_id" in edge_d
        assert "relation" in edge_d
        assert "weight" in edge_d

    def test_to_dict_node_count_matches(self, graph_with_nodes):
        d = graph_with_nodes.to_dict()
        assert len(d["nodes"]) == graph_with_nodes.node_count()

    def test_to_dict_is_serializable(self, graph_with_nodes):
        import json
        d = graph_with_nodes.to_dict()
        json.dumps(d)  # must not raise


# ===========================================================================
# IntentGraphBuilder — basic build
# ===========================================================================


class TestIntentGraphBuilderBuild:
    def test_build_returns_graph(self, builder):
        g = builder.build("find documents")
        assert isinstance(g, IntentGraph)

    def test_build_has_query_node(self, builder):
        g = builder.build("search for knowledge")
        queries = g.nodes_by_type(IntentNodeType.QUERY)
        assert len(queries) == 1

    def test_query_node_label_is_original_query(self, builder):
        q = "Find the AgentFS memory layer"
        g = builder.build(q)
        assert g.nodes_by_type(IntentNodeType.QUERY)[0].label == q

    def test_build_empty_string(self, builder):
        g = builder.build("")
        assert g.node_count() == 1  # only the QUERY node
        assert g.edge_count() == 0


# ===========================================================================
# IntentGraphBuilder — concept extraction
# ===========================================================================


class TestIntentGraphBuilderConcepts:
    def test_concept_min_length_4(self, builder):
        g = builder.build("search knowledge")
        labels = {n.label for n in g.nodes_by_type(IntentNodeType.CONCEPT)}
        assert "search" in labels
        assert "knowledge" in labels

    def test_short_tokens_not_concepts(self, builder):
        # "a", "an", "the" are stopwords; "cat" is 3 chars
        g = builder.build("a cat is in")
        concepts = g.nodes_by_type(IntentNodeType.CONCEPT)
        concept_labels = {n.label for n in concepts}
        assert "a" not in concept_labels
        assert "cat" not in concept_labels  # len 3 < 4

    def test_stopwords_excluded(self, builder):
        g = builder.build("the memory of with")
        concept_labels = {n.label for n in g.nodes_by_type(IntentNodeType.CONCEPT)}
        for sw in ("the", "of", "with"):
            assert sw not in concept_labels

    def test_concept_labels_lowercase(self, builder):
        g = builder.build("memory MEMORY Memory")
        # lower-case tokens only become concepts if not capitalized
        concept_labels = {n.label for n in g.nodes_by_type(IntentNodeType.CONCEPT)}
        # "memory" (lowercase) should appear as concept
        assert "memory" in concept_labels

    def test_concept_has_contains_edge_from_query(self, builder):
        g = builder.build("search documents")
        query_node = g.nodes_by_type(IntentNodeType.QUERY)[0]
        edges = g.edges_from(query_node.node_id)
        relations = {e.relation for e in edges}
        assert "contains" in relations


# ===========================================================================
# IntentGraphBuilder — entity detection
# ===========================================================================


class TestIntentGraphBuilderEntities:
    def test_capitalized_word_becomes_entity(self, builder):
        g = builder.build("find AgentFS documents")
        entity_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ENTITY)}
        assert "AgentFS" in entity_labels

    def test_entity_preserves_original_case(self, builder):
        g = builder.build("using NGT Memory system")
        entity_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ENTITY)}
        assert "NGT" in entity_labels
        assert "Memory" in entity_labels

    def test_all_caps_is_entity(self, builder):
        g = builder.build("query RAG system")
        entity_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ENTITY)}
        assert "RAG" in entity_labels

    def test_entity_has_mentions_edge_from_query(self, builder):
        g = builder.build("find Yodoca data")
        query_node = g.nodes_by_type(IntentNodeType.QUERY)[0]
        edges = g.edges_from(query_node.node_id)
        relations = {e.relation for e in edges}
        assert "mentions" in relations

    def test_sentence_start_capital_is_entity(self, builder):
        g = builder.build("Find the documents")
        entity_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ENTITY)}
        assert "Find" in entity_labels


# ===========================================================================
# IntentGraphBuilder — action detection
# ===========================================================================


class TestIntentGraphBuilderActions:
    def test_ing_suffix_is_action(self, builder):
        g = builder.build("searching documents")
        action_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ACTION)}
        assert "searching" in action_labels

    def test_ed_suffix_is_action(self, builder):
        g = builder.build("filtered results")
        action_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ACTION)}
        assert "filtered" in action_labels

    def test_ize_suffix_is_action(self, builder):
        g = builder.build("to summarize documents")
        action_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ACTION)}
        assert "summarize" in action_labels

    def test_ate_suffix_is_action(self, builder):
        g = builder.build("generate results")
        action_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ACTION)}
        assert "generate" in action_labels

    def test_prefix_how_is_action(self, builder):
        g = builder.build("how does it work")
        action_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ACTION)}
        assert "how" in action_labels

    def test_prefix_find_is_action(self, builder):
        g = builder.build("find the data")
        action_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ACTION)}
        # "find" is lowercase because we check lower token; it's also not capitalized here
        assert "find" in action_labels

    def test_prefix_list_is_action(self, builder):
        g = builder.build("list all items")
        action_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ACTION)}
        assert "list" in action_labels

    def test_prefix_compare_is_action(self, builder):
        g = builder.build("compare two systems")
        action_labels = {n.label for n in g.nodes_by_type(IntentNodeType.ACTION)}
        assert "compare" in action_labels

    def test_action_has_performs_edge_from_query(self, builder):
        g = builder.build("find memory clusters")
        query_node = g.nodes_by_type(IntentNodeType.QUERY)[0]
        edges = g.edges_from(query_node.node_id)
        relations = {e.relation for e in edges}
        assert "performs" in relations


# ===========================================================================
# IntentGraphBuilder — co-occurrence edges
# ===========================================================================


class TestIntentGraphBuilderCoOccurrence:
    def test_consecutive_concepts_get_co_occurs_edge(self, builder):
        # "memory" and "layer" are both concepts (len>=4, lowercase, not stopwords)
        g = builder.build("memory layer architecture")
        concept_labels = {n.label: n for n in g.nodes_by_type(IntentNodeType.CONCEPT)}
        assert "memory" in concept_labels
        assert "layer" in concept_labels
        memory_node = concept_labels["memory"]
        layer_node = concept_labels["layer"]
        edges = g.edges_from(memory_node.node_id)
        co_occurs_edges = [e for e in edges if e.relation == "co-occurs"]
        target_ids = {e.target_id for e in co_occurs_edges}
        assert layer_node.node_id in target_ids

    def test_non_consecutive_concepts_no_co_occurs(self, builder):
        # "knowledge" and "layer" separated by a non-concept word
        g = builder.build("knowledge a layer")
        concept_labels = {n.label: n for n in g.nodes_by_type(IntentNodeType.CONCEPT)}
        if "knowledge" in concept_labels and "layer" in concept_labels:
            knowledge_node = concept_labels["knowledge"]
            edges = g.edges_from(knowledge_node.node_id)
            co_occurs_edges = [e for e in edges if e.relation == "co-occurs"]
            layer_id = concept_labels["layer"].node_id
            assert not any(e.target_id == layer_id for e in co_occurs_edges)


# ===========================================================================
# IntentGraphBuilder — merge
# ===========================================================================


class TestIntentGraphBuilderMerge:
    def test_merge_combines_nodes(self, builder):
        g1 = builder.build("memory layer")
        g2 = builder.build("knowledge graph")
        merged = IntentGraphBuilder.merge([g1, g2])
        assert merged.node_count() >= g1.node_count() + g2.node_count() - 1  # QUERY dedup?

    def test_merge_deduplicates_by_label_and_type(self, builder):
        g1 = builder.build("memory knowledge system")
        g2 = builder.build("memory storage layer")
        merged = IntentGraphBuilder.merge([g1, g2])
        # "memory" concept should appear only once
        memory_nodes = [
            n for n in merged.nodes_by_type(IntentNodeType.CONCEPT) if n.label == "memory"
        ]
        assert len(memory_nodes) == 1

    def test_merge_empty_list(self):
        merged = IntentGraphBuilder.merge([])
        assert merged.node_count() == 0
        assert merged.edge_count() == 0

    def test_merge_single_graph(self, builder):
        g = builder.build("find documents")
        merged = IntentGraphBuilder.merge([g])
        assert merged.node_count() == g.node_count()

    def test_merge_combined_edges(self, builder):
        g1 = builder.build("memory layer")
        g2 = builder.build("knowledge graph")
        merged = IntentGraphBuilder.merge([g1, g2])
        assert merged.edge_count() > 0

    def test_merge_no_duplicate_edges(self, builder):
        q = "memory knowledge layer"
        g1 = builder.build(q)
        g2 = builder.build(q)
        merged = IntentGraphBuilder.merge([g1, g2])
        # All nodes have same labels; edges should not be doubled
        g_single = builder.build(q)
        assert merged.edge_count() == g_single.edge_count()

    def test_merge_returns_intent_graph(self, builder):
        g1 = builder.build("search")
        merged = IntentGraphBuilder.merge([g1])
        assert isinstance(merged, IntentGraph)
