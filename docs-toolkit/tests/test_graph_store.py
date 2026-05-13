"""Tests for the graph_store module."""
from __future__ import annotations

import os
import tempfile

import pytest

from docstoolkit.graph_store import Edge, GraphStats, GraphStore, Node, Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def store() -> GraphStore:
    s = GraphStore()
    yield s
    s.close()


def _build_chain(s: GraphStore, length: int) -> list:
    """Build a chain n0 -> n1 -> ... -> n{length} with 'next' edges."""
    ids = [f"n{i}" for i in range(length + 1)]
    for nid in ids:
        s.add_node(nid, "step")
    for a, b in zip(ids, ids[1:]):
        s.add_edge(a, b, "next")
    return ids


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestNode:
    def test_basic_construction(self):
        n = Node(node_id="a", node_type="doc")
        assert n.node_id == "a"
        assert n.node_type == "doc"
        assert n.properties == {}
        assert n.created_at == 0.0

    def test_with_properties(self):
        n = Node(node_id="a", node_type="doc", properties={"k": 1})
        assert n.properties == {"k": 1}

    def test_with_created_at(self):
        n = Node(node_id="a", node_type="doc", created_at=12.0)
        assert n.created_at == 12.0

    def test_properties_default_is_independent(self):
        n1 = Node(node_id="a", node_type="x")
        n2 = Node(node_id="b", node_type="x")
        n1.properties["k"] = 1
        assert n2.properties == {}


class TestEdge:
    def test_basic_construction(self):
        e = Edge(edge_id=1, source="a", target="b", relation="r")
        assert e.edge_id == 1
        assert e.source == "a"
        assert e.target == "b"
        assert e.relation == "r"
        assert e.properties == {}
        assert e.created_at == 0.0

    def test_with_properties(self):
        e = Edge(
            edge_id=2,
            source="a",
            target="b",
            relation="r",
            properties={"weight": 0.5},
        )
        assert e.properties == {"weight": 0.5}

    def test_properties_default_is_independent(self):
        e1 = Edge(edge_id=1, source="a", target="b", relation="r")
        e2 = Edge(edge_id=2, source="a", target="b", relation="r")
        e1.properties["k"] = 1
        assert e2.properties == {}


class TestPath:
    def test_length_empty(self):
        p = Path(nodes=["a"], edges=[])
        assert p.length == 0

    def test_length_with_edges(self):
        e = Edge(edge_id=1, source="a", target="b", relation="r")
        p = Path(nodes=["a", "b"], edges=[e])
        assert p.length == 1

    def test_length_multi(self):
        e1 = Edge(edge_id=1, source="a", target="b", relation="r")
        e2 = Edge(edge_id=2, source="b", target="c", relation="r")
        p = Path(nodes=["a", "b", "c"], edges=[e1, e2])
        assert p.length == 2

    def test_nodes_attr(self):
        p = Path(nodes=["x", "y"], edges=[])
        assert p.nodes == ["x", "y"]


class TestGraphStats:
    def test_avg_degree_empty(self):
        s = GraphStats(0, 0, {}, {})
        assert s.avg_degree == 0.0

    def test_avg_degree_basic(self):
        s = GraphStats(2, 1, {"x": 2}, {"r": 1})
        assert s.avg_degree == 1.0

    def test_avg_degree_formula(self):
        s = GraphStats(4, 4, {}, {})
        assert s.avg_degree == 2.0

    def test_fields_accessible(self):
        s = GraphStats(3, 5, {"a": 2, "b": 1}, {"r": 5})
        assert s.node_count == 3
        assert s.edge_count == 5
        assert s.node_types == {"a": 2, "b": 1}
        assert s.relations == {"r": 5}


# ---------------------------------------------------------------------------
# Add node
# ---------------------------------------------------------------------------


class TestAddNode:
    def test_returns_node(self, store):
        n = store.add_node("a", "doc")
        assert isinstance(n, Node)
        assert n.node_id == "a"
        assert n.node_type == "doc"

    def test_with_properties(self, store):
        n = store.add_node("a", "doc", properties={"k": "v"})
        assert n.properties == {"k": "v"}

    def test_with_created_at(self, store):
        n = store.add_node("a", "doc", now=42.0)
        assert n.created_at == 42.0

    def test_increases_count(self, store):
        assert store.node_count == 0
        store.add_node("a", "x")
        assert store.node_count == 1
        store.add_node("b", "x")
        assert store.node_count == 2

    def test_upsert(self, store):
        store.add_node("a", "doc")
        store.add_node("a", "person", properties={"name": "Ada"})
        n = store.get_node("a")
        assert n.node_type == "person"
        assert n.properties == {"name": "Ada"}
        assert store.node_count == 1

    def test_default_properties_empty(self, store):
        n = store.add_node("a", "doc")
        assert n.properties == {}


# ---------------------------------------------------------------------------
# Add edge
# ---------------------------------------------------------------------------


class TestAddEdge:
    def test_returns_edge(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e = store.add_edge("a", "b", "r")
        assert isinstance(e, Edge)
        assert e.source == "a"
        assert e.target == "b"
        assert e.relation == "r"

    def test_assigns_edge_id(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e1 = store.add_edge("a", "b", "r")
        e2 = store.add_edge("a", "b", "r")
        assert e1.edge_id != e2.edge_id

    def test_increases_count(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        assert store.edge_count == 0
        store.add_edge("a", "b", "r")
        assert store.edge_count == 1

    def test_with_properties(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e = store.add_edge("a", "b", "r", properties={"w": 2.5})
        assert e.properties == {"w": 2.5}

    def test_default_properties_empty(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e = store.add_edge("a", "b", "r")
        assert e.properties == {}

    def test_with_created_at(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e = store.add_edge("a", "b", "r", now=9.0)
        assert e.created_at == 9.0


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------


class TestGetNode:
    def test_returns_node(self, store):
        store.add_node("a", "doc", properties={"k": 1}, now=1.0)
        n = store.get_node("a")
        assert n.node_id == "a"
        assert n.node_type == "doc"
        assert n.properties == {"k": 1}
        assert n.created_at == 1.0

    def test_missing_returns_none(self, store):
        assert store.get_node("nope") is None

    def test_after_remove_returns_none(self, store):
        store.add_node("a", "x")
        store.remove_node("a")
        assert store.get_node("a") is None


class TestGetEdge:
    def test_returns_edge(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e = store.add_edge("a", "b", "r", properties={"w": 1}, now=2.0)
        fetched = store.get_edge(e.edge_id)
        assert fetched.source == "a"
        assert fetched.target == "b"
        assert fetched.relation == "r"
        assert fetched.properties == {"w": 1}
        assert fetched.created_at == 2.0

    def test_missing_returns_none(self, store):
        assert store.get_edge(9999) is None


# ---------------------------------------------------------------------------
# Remove
# ---------------------------------------------------------------------------


class TestRemoveNode:
    def test_removes_node(self, store):
        store.add_node("a", "x")
        assert store.remove_node("a") is True
        assert store.get_node("a") is None

    def test_missing_returns_false(self, store):
        assert store.remove_node("nope") is False

    def test_cascade_removes_outgoing_edges(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e = store.add_edge("a", "b", "r")
        store.remove_node("a")
        assert store.get_edge(e.edge_id) is None

    def test_cascade_removes_incoming_edges(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e = store.add_edge("a", "b", "r")
        store.remove_node("b")
        assert store.get_edge(e.edge_id) is None

    def test_cascade_removes_all_touching(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("a", "b", "r")
        store.add_edge("c", "a", "r")
        store.add_edge("b", "c", "r")
        store.remove_node("a")
        assert store.edge_count == 1  # only b -> c remains


class TestRemoveEdge:
    def test_removes_edge(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e = store.add_edge("a", "b", "r")
        assert store.remove_edge(e.edge_id) is True
        assert store.get_edge(e.edge_id) is None

    def test_missing_returns_false(self, store):
        assert store.remove_edge(9999) is False

    def test_does_not_remove_nodes(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e = store.add_edge("a", "b", "r")
        store.remove_edge(e.edge_id)
        assert store.get_node("a") is not None
        assert store.get_node("b") is not None


# ---------------------------------------------------------------------------
# Filtered listings
# ---------------------------------------------------------------------------


class TestNodesByType:
    def test_empty(self, store):
        assert store.nodes_by_type("doc") == []

    def test_filters(self, store):
        store.add_node("a", "doc")
        store.add_node("b", "person")
        store.add_node("c", "doc")
        docs = store.nodes_by_type("doc")
        assert {n.node_id for n in docs} == {"a", "c"}

    def test_unknown_type(self, store):
        store.add_node("a", "doc")
        assert store.nodes_by_type("nope") == []


class TestEdgesByRelation:
    def test_empty(self, store):
        assert store.edges_by_relation("r") == []

    def test_filters(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("a", "b", "ref")
        store.add_edge("a", "b", "wrote")
        store.add_edge("a", "b", "ref")
        refs = store.edges_by_relation("ref")
        assert len(refs) == 2
        assert all(e.relation == "ref" for e in refs)


# ---------------------------------------------------------------------------
# Outgoing / incoming
# ---------------------------------------------------------------------------


class TestOutgoing:
    def test_basic(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("a", "b", "r")
        store.add_edge("a", "c", "r")
        edges = store.outgoing("a")
        assert {e.target for e in edges} == {"b", "c"}

    def test_with_relation_filter(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("a", "b", "r1")
        store.add_edge("a", "b", "r2")
        edges = store.outgoing("a", relation="r1")
        assert len(edges) == 1
        assert edges[0].relation == "r1"

    def test_empty(self, store):
        store.add_node("a", "x")
        assert store.outgoing("a") == []

    def test_unknown_node(self, store):
        assert store.outgoing("nope") == []


class TestIncoming:
    def test_basic(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("b", "a", "r")
        store.add_edge("c", "a", "r")
        edges = store.incoming("a")
        assert {e.source for e in edges} == {"b", "c"}

    def test_with_relation_filter(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("b", "a", "r1")
        store.add_edge("b", "a", "r2")
        edges = store.incoming("a", relation="r1")
        assert len(edges) == 1
        assert edges[0].relation == "r1"

    def test_empty(self, store):
        store.add_node("a", "x")
        assert store.incoming("a") == []


# ---------------------------------------------------------------------------
# Neighbors
# ---------------------------------------------------------------------------


class TestNeighbors:
    def test_out(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("a", "b", "r")
        store.add_edge("a", "c", "r")
        assert set(store.neighbors("a", direction="out")) == {"b", "c"}

    def test_in(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("b", "a", "r")
        store.add_edge("c", "a", "r")
        assert set(store.neighbors("a", direction="in")) == {"b", "c"}

    def test_both(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("a", "b", "r")
        store.add_edge("c", "a", "r")
        assert set(store.neighbors("a", direction="both")) == {"b", "c"}

    def test_both_dedups(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("a", "b", "r")
        store.add_edge("b", "a", "r")
        result = store.neighbors("a", direction="both")
        assert sorted(result) == ["b"]

    def test_default_is_out(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("a", "b", "r")
        store.add_edge("c", "a", "r")
        assert store.neighbors("a") == ["b"]

    def test_invalid_direction(self, store):
        store.add_node("a", "x")
        with pytest.raises(ValueError):
            store.neighbors("a", direction="bad")


# ---------------------------------------------------------------------------
# Find path
# ---------------------------------------------------------------------------


class TestFindPath:
    def test_direct(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("a", "b", "r")
        p = store.find_path("a", "b")
        assert p is not None
        assert p.nodes == ["a", "b"]
        assert p.length == 1

    def test_multi_hop(self, store):
        ids = _build_chain(store, 4)
        p = store.find_path(ids[0], ids[-1])
        assert p is not None
        assert p.nodes == ids
        assert p.length == 4

    def test_self_path(self, store):
        store.add_node("a", "x")
        p = store.find_path("a", "a")
        assert p is not None
        assert p.nodes == ["a"]
        assert p.length == 0

    def test_no_path(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        assert store.find_path("a", "b") is None

    def test_respects_max_depth(self, store):
        ids = _build_chain(store, 5)
        assert store.find_path(ids[0], ids[-1], max_depth=2) is None
        assert store.find_path(ids[0], ids[2], max_depth=2) is not None

    def test_shortest(self, store):
        for nid in ["a", "b", "c", "d"]:
            store.add_node(nid, "x")
        store.add_edge("a", "b", "r")
        store.add_edge("b", "c", "r")
        store.add_edge("c", "d", "r")
        store.add_edge("a", "d", "r")  # shortcut
        p = store.find_path("a", "d")
        assert p.length == 1

    def test_unknown_source(self, store):
        store.add_node("b", "x")
        assert store.find_path("nope", "b") is None

    def test_unknown_target(self, store):
        store.add_node("a", "x")
        assert store.find_path("a", "nope") is None

    def test_directed_only(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("a", "b", "r")
        # Reverse direction shouldn't be reachable.
        assert store.find_path("b", "a") is None


# ---------------------------------------------------------------------------
# Connected to
# ---------------------------------------------------------------------------


class TestConnectedTo:
    def test_depth_1(self, store):
        ids = _build_chain(store, 3)
        result = store.connected_to(ids[0], depth=1)
        assert result == {ids[1]}

    def test_depth_2(self, store):
        ids = _build_chain(store, 3)
        result = store.connected_to(ids[0], depth=2)
        assert result == {ids[1], ids[2]}

    def test_full_reach(self, store):
        ids = _build_chain(store, 3)
        result = store.connected_to(ids[0], depth=10)
        assert result == {ids[1], ids[2], ids[3]}

    def test_does_not_include_self(self, store):
        store.add_node("a", "x")
        assert "a" not in store.connected_to("a", depth=3)

    def test_zero_depth(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("a", "b", "r")
        assert store.connected_to("a", depth=0) == set()

    def test_unknown_node(self, store):
        assert store.connected_to("nope", depth=3) == set()

    def test_handles_cycles(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("a", "b", "r")
        store.add_edge("b", "c", "r")
        store.add_edge("c", "a", "r")
        assert store.connected_to("a", depth=10) == {"b", "c"}


# ---------------------------------------------------------------------------
# Degree
# ---------------------------------------------------------------------------


class TestDegree:
    def test_isolated_node(self, store):
        store.add_node("a", "x")
        assert store.degree("a") == 0
        assert store.in_degree("a") == 0
        assert store.out_degree("a") == 0

    def test_out_only(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("a", "b", "r")
        store.add_edge("a", "c", "r")
        assert store.out_degree("a") == 2
        assert store.in_degree("a") == 0
        assert store.degree("a") == 2

    def test_in_only(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("b", "a", "r")
        assert store.in_degree("a") == 1
        assert store.out_degree("a") == 0
        assert store.degree("a") == 1

    def test_mixed(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_node("c", "x")
        store.add_edge("a", "b", "r")
        store.add_edge("c", "a", "r")
        assert store.in_degree("a") == 1
        assert store.out_degree("a") == 1
        assert store.degree("a") == 2

    def test_self_loop_counts_both(self, store):
        store.add_node("a", "x")
        store.add_edge("a", "a", "r")
        assert store.in_degree("a") == 1
        assert store.out_degree("a") == 1
        assert store.degree("a") == 2


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self, store):
        s = store.stats()
        assert s.node_count == 0
        assert s.edge_count == 0
        assert s.node_types == {}
        assert s.relations == {}
        assert s.avg_degree == 0.0

    def test_with_data(self, store):
        store.add_node("a", "doc")
        store.add_node("b", "person")
        store.add_node("c", "doc")
        store.add_edge("a", "b", "wrote")
        store.add_edge("c", "b", "wrote")
        store.add_edge("a", "c", "refs")
        s = store.stats()
        assert s.node_count == 3
        assert s.edge_count == 3
        assert s.node_types == {"doc": 2, "person": 1}
        assert s.relations == {"wrote": 2, "refs": 1}
        assert s.avg_degree == 2.0

    def test_returns_graphstats(self, store):
        assert isinstance(store.stats(), GraphStats)


# ---------------------------------------------------------------------------
# Counts
# ---------------------------------------------------------------------------


class TestCount:
    def test_node_count_property(self, store):
        assert store.node_count == 0
        store.add_node("a", "x")
        assert store.node_count == 1

    def test_edge_count_property(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        assert store.edge_count == 0
        store.add_edge("a", "b", "r")
        assert store.edge_count == 1

    def test_node_count_after_remove(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.remove_node("a")
        assert store.node_count == 1

    def test_edge_count_after_cascade(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("a", "b", "r")
        store.remove_node("a")
        assert store.edge_count == 0


# ---------------------------------------------------------------------------
# Clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clears_nodes_and_edges(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        store.add_edge("a", "b", "r")
        store.clear()
        assert store.node_count == 0
        assert store.edge_count == 0

    def test_after_clear_can_add_again(self, store):
        store.add_node("a", "x")
        store.clear()
        store.add_node("a", "y")
        assert store.get_node("a").node_type == "y"


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


class TestPersistence:
    def test_file_db_persists(self):
        tmpdir = tempfile.mkdtemp()
        db_path = os.path.join(tmpdir, "graph.db")
        try:
            s1 = GraphStore(db_path)
            s1.add_node("a", "doc", properties={"k": 1}, now=5.0)
            s1.add_node("b", "doc")
            e = s1.add_edge("a", "b", "ref", properties={"w": 2}, now=6.0)
            edge_id = e.edge_id
            s1.close()

            s2 = GraphStore(db_path)
            assert s2.node_count == 2
            assert s2.edge_count == 1
            n = s2.get_node("a")
            assert n.properties == {"k": 1}
            assert n.created_at == 5.0
            re = s2.get_edge(edge_id)
            assert re.source == "a"
            assert re.properties == {"w": 2}
            s2.close()
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)
            os.rmdir(tmpdir)

    def test_memory_is_independent(self):
        s1 = GraphStore()
        s2 = GraphStore()
        s1.add_node("a", "x")
        assert s2.node_count == 0
        s1.close()
        s2.close()


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_self_loop_allowed(self, store):
        store.add_node("a", "x")
        e = store.add_edge("a", "a", "r")
        assert e.source == "a"
        assert e.target == "a"
        assert store.edge_count == 1

    def test_self_loop_path(self, store):
        store.add_node("a", "x")
        store.add_edge("a", "a", "r")
        # source==target shortcut returns empty path, not the loop.
        p = store.find_path("a", "a")
        assert p.length == 0

    def test_multi_edges_allowed(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        e1 = store.add_edge("a", "b", "r")
        e2 = store.add_edge("a", "b", "r")
        assert e1.edge_id != e2.edge_id
        assert store.edge_count == 2

    def test_find_path_no_outgoing(self, store):
        store.add_node("a", "x")
        store.add_node("b", "x")
        assert store.find_path("a", "b") is None

    def test_add_edge_to_unknown_nodes(self, store):
        # Edge insertion doesn't require nodes — but path/find should
        # still handle missing nodes gracefully.
        e = store.add_edge("ghost1", "ghost2", "r")
        assert e.edge_id > 0

    def test_close_idempotent_then_reopen(self):
        tmpdir = tempfile.mkdtemp()
        db_path = os.path.join(tmpdir, "g.db")
        try:
            s = GraphStore(db_path)
            s.add_node("a", "x")
            s.close()
            s2 = GraphStore(db_path)
            assert s2.get_node("a") is not None
            s2.close()
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)
            os.rmdir(tmpdir)

    def test_properties_roundtrip_nested(self, store):
        store.add_node(
            "a",
            "doc",
            properties={"meta": {"tags": ["x", "y"], "n": 3}},
        )
        n = store.get_node("a")
        assert n.properties == {"meta": {"tags": ["x", "y"], "n": 3}}

    def test_unicode_properties(self, store):
        store.add_node("a", "doc", properties={"title": "Связи"})
        assert store.get_node("a").properties == {"title": "Связи"}
