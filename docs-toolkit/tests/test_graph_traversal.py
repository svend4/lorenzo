"""Tests for docstoolkit.graph_traversal (E72).

Covers:
  - Graph: add/remove nodes & edges, neighbors, degrees, has_node/has_edge,
    undirected symmetry, node attrs, edge listing
  - BFS: order, hop distances, unreachable nodes excluded
  - DFS: reachability, predecessor tracking, discovery order
  - Dijkstra: weighted shortest distances, predecessors, negative-weight skip
  - has_cycle: acyclic/cyclic directed + undirected, self-loop
  - topological_sort: valid ordering, raises on cycle
  - connected_components: single/multiple/isolated components
  - shortest_path: found / not found (empty list)
  - Edge cases: empty graph, single node, disconnected graph
"""

import math
import pytest

from docstoolkit.graph_traversal import (
    Graph,
    Edge,
    NodeId,
    TraversalResult,
    bfs,
    dfs,
    dijkstra,
    has_cycle,
    topological_sort,
    connected_components,
    shortest_path,
)


# ===========================================================================
# Helper factories
# ===========================================================================

def make_line(n: int, directed: bool = True) -> Graph:
    """0 -> 1 -> 2 -> ... -> n-1"""
    g = Graph(directed=directed)
    for i in range(n):
        g.add_node(str(i))
    for i in range(n - 1):
        g.add_edge(str(i), str(i + 1))
    return g


def make_triangle(directed: bool = True) -> Graph:
    """A -> B -> C -> A"""
    g = Graph(directed=directed)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    return g


def make_dag() -> Graph:
    """DAG: A->B, A->C, B->D, C->D (diamond)"""
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    return g


# ===========================================================================
# 1. Graph — nodes
# ===========================================================================

class TestGraphNodes:
    def test_add_node_basic(self):
        g = Graph()
        g.add_node("X")
        assert g.has_node("X")

    def test_add_node_with_attrs(self):
        g = Graph()
        g.add_node("X", color="red", weight=5)
        assert g.node_attrs("X") == {"color": "red", "weight": 5}

    def test_add_node_attrs_merge(self):
        g = Graph()
        g.add_node("X", a=1)
        g.add_node("X", b=2)
        attrs = g.node_attrs("X")
        assert attrs["a"] == 1 and attrs["b"] == 2

    def test_has_node_missing(self):
        g = Graph()
        assert not g.has_node("MISSING")

    def test_remove_node_returns_true(self):
        g = Graph()
        g.add_node("X")
        assert g.remove_node("X") is True

    def test_remove_node_absent_returns_false(self):
        g = Graph()
        assert g.remove_node("NOPE") is False

    def test_remove_node_removes_from_nodes_list(self):
        g = Graph()
        g.add_node("X")
        g.remove_node("X")
        assert not g.has_node("X")

    def test_nodes_empty(self):
        g = Graph()
        assert g.nodes() == []

    def test_nodes_returns_all(self):
        g = Graph()
        g.add_node("A")
        g.add_node("B")
        assert set(g.nodes()) == {"A", "B"}

    def test_len_graph(self):
        g = Graph()
        g.add_node("A")
        g.add_node("B")
        assert len(g) == 2

    def test_node_attrs_copy(self):
        """node_attrs() returns a copy, not a live reference."""
        g = Graph()
        g.add_node("A", x=1)
        attrs = g.node_attrs("A")
        attrs["x"] = 999
        assert g.node_attrs("A")["x"] == 1

    def test_node_attrs_missing_raises(self):
        g = Graph()
        with pytest.raises(KeyError):
            g.node_attrs("MISSING")


# ===========================================================================
# 2. Graph — edges (directed)
# ===========================================================================

class TestGraphEdgesDirected:
    def test_add_edge_creates_nodes(self):
        g = Graph()
        g.add_edge("A", "B")
        assert g.has_node("A") and g.has_node("B")

    def test_has_edge_true(self):
        g = Graph()
        g.add_edge("A", "B")
        assert g.has_edge("A", "B")

    def test_has_edge_false_reverse(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        assert not g.has_edge("B", "A")

    def test_has_edge_missing(self):
        g = Graph()
        assert not g.has_edge("X", "Y")

    def test_remove_edge_returns_true(self):
        g = Graph()
        g.add_edge("A", "B")
        assert g.remove_edge("A", "B") is True

    def test_remove_edge_absent_returns_false(self):
        g = Graph()
        assert g.remove_edge("A", "B") is False

    def test_remove_edge_removes(self):
        g = Graph()
        g.add_edge("A", "B")
        g.remove_edge("A", "B")
        assert not g.has_edge("A", "B")

    def test_edges_list(self):
        g = Graph()
        g.add_edge("A", "B", weight=2.0, label="x")
        edges = g.edges()
        assert len(edges) == 1
        e = edges[0]
        assert e.source == "A" and e.target == "B"
        assert e.weight == 2.0 and e.label == "x"

    def test_edge_weight_default(self):
        g = Graph()
        g.add_edge("A", "B")
        assert g.edges()[0].weight == 1.0

    def test_remove_node_removes_outgoing_edges(self):
        g = Graph()
        g.add_edge("A", "B")
        g.remove_node("A")
        assert not g.has_edge("A", "B")

    def test_remove_node_removes_incoming_edges(self):
        g = Graph()
        g.add_edge("A", "B")
        g.remove_node("B")
        assert not g.has_edge("A", "B")


# ===========================================================================
# 3. Graph — edges (undirected)
# ===========================================================================

class TestGraphEdgesUndirected:
    def test_undirected_adds_both_directions(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        assert g.has_edge("A", "B") and g.has_edge("B", "A")

    def test_undirected_remove_removes_both(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.remove_edge("A", "B")
        assert not g.has_edge("A", "B") and not g.has_edge("B", "A")

    def test_undirected_edges_no_duplicates(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert len(g.edges()) == 2

    def test_undirected_self_loop_single_entry(self):
        g = Graph(directed=False)
        g.add_edge("A", "A")
        assert len(g.edges()) == 1

    def test_undirected_neighbors_symmetric(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        assert "B" in g.neighbors("A")
        assert "A" in g.neighbors("B")


# ===========================================================================
# 4. Graph — neighbors and degrees
# ===========================================================================

class TestGraphDegrees:
    def test_neighbors_directed(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        assert set(g.neighbors("A")) == {"B", "C"}

    def test_neighbors_missing_node(self):
        g = Graph()
        assert g.neighbors("GHOST") == []

    def test_out_degree(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        assert g.out_degree("A") == 2

    def test_in_degree(self):
        g = Graph()
        g.add_edge("A", "C")
        g.add_edge("B", "C")
        assert g.in_degree("C") == 2

    def test_in_degree_zero_for_source(self):
        g = Graph()
        g.add_edge("A", "B")
        assert g.in_degree("A") == 0

    def test_out_degree_zero_for_sink(self):
        g = Graph()
        g.add_edge("A", "B")
        assert g.out_degree("B") == 0

    def test_degree_missing_node(self):
        g = Graph()
        assert g.in_degree("X") == 0
        assert g.out_degree("X") == 0


# ===========================================================================
# 5. BFS
# ===========================================================================

class TestBFS:
    def test_bfs_single_node(self):
        g = Graph()
        g.add_node("A")
        r = bfs(g, "A")
        assert r.visited == ["A"]
        assert r.distances == {"A": 0.0}
        assert r.predecessors == {"A": None}

    def test_bfs_start_missing(self):
        g = Graph()
        r = bfs(g, "X")
        assert r.visited == [] and r.distances == {}

    def test_bfs_line_visited_order(self):
        g = make_line(4)
        r = bfs(g, "0")
        assert r.visited == ["0", "1", "2", "3"]

    def test_bfs_hop_distances(self):
        g = make_line(4)
        r = bfs(g, "0")
        assert r.distances == {"0": 0.0, "1": 1.0, "2": 2.0, "3": 3.0}

    def test_bfs_predecessor_chain(self):
        g = make_line(3)
        r = bfs(g, "0")
        assert r.predecessors["0"] is None
        assert r.predecessors["1"] == "0"
        assert r.predecessors["2"] == "1"

    def test_bfs_unreachable_not_visited(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_node("C")          # isolated
        r = bfs(g, "A")
        assert "C" not in r.visited
        assert "C" not in r.distances

    def test_bfs_tree_breadth_first(self):
        g = Graph()
        g.add_edge("root", "L1a")
        g.add_edge("root", "L1b")
        g.add_edge("L1a", "L2a")
        r = bfs(g, "root")
        # Both level-1 nodes must appear before level-2
        assert r.visited.index("L1a") < r.visited.index("L2a")
        assert r.visited.index("L1b") < r.visited.index("L2a")

    def test_bfs_diamond(self):
        g = make_dag()
        r = bfs(g, "A")
        assert set(r.visited) == {"A", "B", "C", "D"}
        assert r.distances["D"] == 2.0

    def test_bfs_empty_graph(self):
        g = Graph()
        r = bfs(g, "A")
        assert r.visited == []


# ===========================================================================
# 6. DFS
# ===========================================================================

class TestDFS:
    def test_dfs_single_node(self):
        g = Graph()
        g.add_node("A")
        r = dfs(g, "A")
        assert r.visited == ["A"]
        assert r.distances == {"A": 0.0}

    def test_dfs_start_missing(self):
        g = Graph()
        r = dfs(g, "X")
        assert r.visited == []

    def test_dfs_line_all_visited(self):
        g = make_line(5)
        r = dfs(g, "0")
        assert set(r.visited) == {"0", "1", "2", "3", "4"}

    def test_dfs_predecessor_tracking(self):
        g = make_line(3)
        r = dfs(g, "0")
        assert r.predecessors["0"] is None
        assert r.predecessors["1"] == "0"
        assert r.predecessors["2"] == "1"

    def test_dfs_discovery_order_indices(self):
        g = make_line(3)
        r = dfs(g, "0")
        assert r.distances["0"] == 0.0
        assert r.distances["1"] == 1.0
        assert r.distances["2"] == 2.0

    def test_dfs_unreachable_excluded(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_node("Z")
        r = dfs(g, "A")
        assert "Z" not in r.visited

    def test_dfs_all_reachable_in_branching_graph(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "D")
        r = dfs(g, "A")
        assert set(r.visited) == {"A", "B", "C", "D"}

    def test_dfs_empty_graph(self):
        g = Graph()
        r = dfs(g, "A")
        assert r.visited == []


# ===========================================================================
# 7. Dijkstra
# ===========================================================================

class TestDijkstra:
    def test_dijkstra_single_node(self):
        g = Graph()
        g.add_node("A")
        r = dijkstra(g, "A")
        assert r.distances == {"A": 0.0}
        assert r.predecessors == {"A": None}

    def test_dijkstra_start_missing(self):
        g = Graph()
        r = dijkstra(g, "X")
        assert r.distances == {}

    def test_dijkstra_unweighted_equals_bfs_distances(self):
        g = make_line(4)
        r = dijkstra(g, "0")
        assert r.distances == {"0": 0.0, "1": 1.0, "2": 2.0, "3": 3.0}

    def test_dijkstra_weighted(self):
        g = Graph()
        g.add_edge("A", "B", weight=1.0)
        g.add_edge("A", "C", weight=4.0)
        g.add_edge("B", "C", weight=2.0)
        r = dijkstra(g, "A")
        assert r.distances["C"] == 3.0  # A->B->C = 1+2

    def test_dijkstra_predecessor_on_weighted(self):
        g = Graph()
        g.add_edge("A", "B", weight=1.0)
        g.add_edge("A", "C", weight=4.0)
        g.add_edge("B", "C", weight=2.0)
        r = dijkstra(g, "A")
        assert r.predecessors["C"] == "B"

    def test_dijkstra_unreachable_excluded(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_node("Z")
        r = dijkstra(g, "A")
        assert "Z" not in r.distances

    def test_dijkstra_negative_weight_skipped(self):
        """Negative weight edge should be ignored; no crash."""
        g = Graph()
        g.add_edge("A", "B", weight=-1.0)
        g.add_edge("A", "C", weight=2.0)
        r = dijkstra(g, "A")
        # B is only reachable via the negative edge — it stays unreachable
        assert "B" not in r.distances
        assert r.distances.get("C") == 2.0

    def test_dijkstra_diamond(self):
        g = make_dag()
        r = dijkstra(g, "A")
        assert r.distances["D"] == 2.0

    def test_dijkstra_zero_weight(self):
        g = Graph()
        g.add_edge("A", "B", weight=0.0)
        r = dijkstra(g, "A")
        assert r.distances["B"] == 0.0

    def test_dijkstra_empty_graph(self):
        g = Graph()
        r = dijkstra(g, "A")
        assert r.visited == []


# ===========================================================================
# 8. has_cycle
# ===========================================================================

class TestHasCycle:
    def test_empty_graph_no_cycle(self):
        g = Graph()
        assert not has_cycle(g)

    def test_single_node_no_cycle(self):
        g = Graph()
        g.add_node("A")
        assert not has_cycle(g)

    def test_directed_line_no_cycle(self):
        g = make_line(5)
        assert not has_cycle(g)

    def test_directed_dag_no_cycle(self):
        g = make_dag()
        assert not has_cycle(g)

    def test_directed_triangle_cycle(self):
        g = make_triangle(directed=True)
        assert has_cycle(g)

    def test_directed_self_loop(self):
        g = Graph()
        g.add_edge("A", "A")
        assert has_cycle(g)

    def test_directed_two_node_cycle(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "A")
        assert has_cycle(g)

    def test_undirected_no_cycle_tree(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert not has_cycle(g)

    def test_undirected_triangle_cycle(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "A")
        assert has_cycle(g)

    def test_undirected_self_loop(self):
        g = Graph(directed=False)
        g.add_edge("A", "A")
        assert has_cycle(g)

    def test_directed_disconnected_with_cycle_in_one_component(self):
        g = Graph()
        g.add_edge("A", "B")  # acyclic component
        g.add_edge("X", "Y")
        g.add_edge("Y", "X")  # cyclic component
        assert has_cycle(g)


# ===========================================================================
# 9. topological_sort
# ===========================================================================

class TestTopologicalSort:
    def test_single_node(self):
        g = Graph()
        g.add_node("A")
        order = topological_sort(g)
        assert order == ["A"]

    def test_line_order(self):
        g = make_line(4)
        order = topological_sort(g)
        assert order.index("0") < order.index("1")
        assert order.index("1") < order.index("2")
        assert order.index("2") < order.index("3")

    def test_diamond_dag(self):
        g = make_dag()
        order = topological_sort(g)
        assert order.index("A") < order.index("B")
        assert order.index("A") < order.index("C")
        assert order.index("B") < order.index("D")
        assert order.index("C") < order.index("D")

    def test_raises_on_cycle(self):
        g = make_triangle(directed=True)
        with pytest.raises(ValueError, match="cycle"):
            topological_sort(g)

    def test_raises_on_self_loop(self):
        g = Graph()
        g.add_edge("A", "A")
        with pytest.raises(ValueError):
            topological_sort(g)

    def test_empty_graph(self):
        g = Graph()
        assert topological_sort(g) == []

    def test_disconnected_dag(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_node("X")  # isolated
        order = topological_sort(g)
        assert set(order) == {"A", "B", "X"}
        assert order.index("A") < order.index("B")

    def test_returns_all_nodes(self):
        g = make_dag()
        order = topological_sort(g)
        assert set(order) == {"A", "B", "C", "D"}


# ===========================================================================
# 10. connected_components
# ===========================================================================

class TestConnectedComponents:
    def test_empty_graph(self):
        g = Graph()
        comps = connected_components(g)
        assert comps == []

    def test_single_node(self):
        g = Graph()
        g.add_node("A")
        comps = connected_components(g)
        assert len(comps) == 1
        assert comps[0] == ["A"]

    def test_single_connected_component(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        comps = connected_components(g)
        assert len(comps) == 1
        assert set(comps[0]) == {"A", "B", "C"}

    def test_two_components(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("C", "D")
        comps = connected_components(g)
        node_sets = [set(c) for c in comps]
        assert {"A", "B"} in node_sets
        assert {"C", "D"} in node_sets

    def test_isolated_nodes_each_own_component(self):
        g = Graph()
        g.add_node("X")
        g.add_node("Y")
        g.add_node("Z")
        comps = connected_components(g)
        assert len(comps) == 3

    def test_directed_treated_as_undirected(self):
        """A directed graph A->B, C->D has two components even if not strongly connected."""
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("C", "D")
        comps = connected_components(g)
        assert len(comps) == 2

    def test_all_nodes_covered(self):
        g = Graph(directed=False)
        g.add_edge("1", "2")
        g.add_edge("3", "4")
        g.add_node("5")
        comps = connected_components(g)
        all_nodes = {n for c in comps for n in c}
        assert all_nodes == {"1", "2", "3", "4", "5"}


# ===========================================================================
# 11. shortest_path
# ===========================================================================

class TestShortestPath:
    def test_same_node(self):
        g = Graph()
        g.add_node("A")
        path = shortest_path(g, "A", "A")
        assert path == ["A"]

    def test_direct_edge(self):
        g = Graph()
        g.add_edge("A", "B")
        assert shortest_path(g, "A", "B") == ["A", "B"]

    def test_multi_hop(self):
        g = make_line(4)
        assert shortest_path(g, "0", "3") == ["0", "1", "2", "3"]

    def test_weighted_picks_shorter(self):
        g = Graph()
        g.add_edge("A", "B", weight=1.0)
        g.add_edge("A", "C", weight=4.0)
        g.add_edge("B", "C", weight=2.0)
        path = shortest_path(g, "A", "C")
        assert path == ["A", "B", "C"]

    def test_no_path_returns_empty(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_node("Z")
        assert shortest_path(g, "A", "Z") == []

    def test_missing_start_returns_empty(self):
        g = Graph()
        g.add_node("B")
        assert shortest_path(g, "GHOST", "B") == []

    def test_missing_end_returns_empty(self):
        g = Graph()
        g.add_node("A")
        assert shortest_path(g, "A", "GHOST") == []

    def test_undirected_path(self):
        g = Graph(directed=False)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        assert shortest_path(g, "C", "A") == ["C", "B", "A"]

    def test_path_includes_start_and_end(self):
        g = make_line(5)
        path = shortest_path(g, "0", "4")
        assert path[0] == "0" and path[-1] == "4"


# ===========================================================================
# 12. Edge dataclass
# ===========================================================================

class TestEdgeDataclass:
    def test_edge_defaults(self):
        e = Edge(source="A", target="B")
        assert e.weight == 1.0 and e.label == ""

    def test_edge_custom(self):
        e = Edge(source="X", target="Y", weight=3.5, label="knows")
        assert e.source == "X"
        assert e.target == "Y"
        assert e.weight == 3.5
        assert e.label == "knows"


# ===========================================================================
# 13. TraversalResult dataclass
# ===========================================================================

class TestTraversalResult:
    def test_fields_accessible(self):
        tr = TraversalResult(
            visited=["A", "B"],
            distances={"A": 0.0, "B": 1.0},
            predecessors={"A": None, "B": "A"},
        )
        assert tr.visited == ["A", "B"]
        assert tr.distances["B"] == 1.0
        assert tr.predecessors["A"] is None


# ===========================================================================
# 14. Additional edge-case / integration tests
# ===========================================================================

class TestEdgeCases:
    def test_add_edge_idempotent_weight_update(self):
        """Re-adding an edge with a new weight should update it."""
        g = Graph()
        g.add_edge("A", "B", weight=1.0)
        g.add_edge("A", "B", weight=5.0)
        e = g.edges()[0]
        assert e.weight == 5.0

    def test_remove_node_mid_path_disconnects(self):
        g = make_line(5)
        g.remove_node("2")
        r = bfs(g, "0")
        assert "3" not in r.visited and "4" not in r.visited

    def test_large_line_dijkstra(self):
        n = 50
        g = make_line(n)
        r = dijkstra(g, "0")
        assert r.distances[str(n - 1)] == float(n - 1)

    def test_disconnected_bfs_from_isolated(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_node("Z")
        r = bfs(g, "Z")
        assert r.visited == ["Z"]
        assert r.distances == {"Z": 0.0}

    def test_directed_not_symmetric(self):
        g = Graph(directed=True)
        g.add_edge("A", "B")
        assert g.has_edge("A", "B")
        assert not g.has_edge("B", "A")

    def test_topological_sort_multiple_valid_orderings(self):
        """As long as constraints are respected, any valid order is acceptable."""
        g = Graph()
        g.add_edge("A", "C")
        g.add_edge("B", "C")
        order = topological_sort(g)
        assert order.index("A") < order.index("C")
        assert order.index("B") < order.index("C")

    def test_connected_components_directed_weakly_connected(self):
        """Directed graph A->B->C treated as undirected = one component."""
        g = Graph(directed=True)
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        comps = connected_components(g)
        assert len(comps) == 1
        assert set(comps[0]) == {"A", "B", "C"}

    def test_negative_weight_does_not_crash_dijkstra(self):
        g = Graph()
        g.add_edge("A", "B", weight=-100.0)
        g.add_edge("A", "C", weight=1.0)
        r = dijkstra(g, "A")
        assert "B" not in r.distances  # negative edge skipped
        assert r.distances["C"] == 1.0

    def test_export_all_from_init(self):
        """Verify __init__.py re-exports all public symbols."""
        import docstoolkit.graph_traversal as gt
        for name in [
            "Graph", "Edge", "NodeId",
            "TraversalResult",
            "bfs", "dfs", "dijkstra",
            "has_cycle", "topological_sort",
            "connected_components", "shortest_path",
        ]:
            assert hasattr(gt, name), f"Missing export: {name}"
