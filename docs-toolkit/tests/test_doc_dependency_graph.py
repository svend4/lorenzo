"""Tests for E298 DocDependencyGraph module.

Run with:
    cd /home/user/lorenzo/docs-toolkit
    python -m pytest tests/test_doc_dependency_graph.py -q
"""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_dependency_graph import (
    DependencyEdge,
    DocDependencyGraph,
    GraphStats,
)


# ---------------------------------------------------------------------------
# TestDependencyEdgeDataclass
# ---------------------------------------------------------------------------

class TestDependencyEdgeDataclass:
    def test_required_fields(self):
        e = DependencyEdge(from_doc="a", to_doc="b")
        assert e.from_doc == "a"
        assert e.to_doc == "b"

    def test_default_kind(self):
        e = DependencyEdge(from_doc="a", to_doc="b")
        assert e.kind == "depends_on"

    def test_custom_kind(self):
        e = DependencyEdge(from_doc="a", to_doc="b", kind="imports")
        assert e.kind == "imports"

    def test_equality(self):
        e1 = DependencyEdge(from_doc="a", to_doc="b", kind="extends")
        e2 = DependencyEdge(from_doc="a", to_doc="b", kind="extends")
        assert e1 == e2

    def test_inequality_different_kind(self):
        e1 = DependencyEdge(from_doc="a", to_doc="b", kind="imports")
        e2 = DependencyEdge(from_doc="a", to_doc="b", kind="extends")
        assert e1 != e2


# ---------------------------------------------------------------------------
# TestGraphStatsDataclass
# ---------------------------------------------------------------------------

class TestGraphStatsDataclass:
    def test_fields_exist(self):
        s = GraphStats(total_nodes=5, total_edges=4, root_count=2, leaf_count=1)
        assert s.total_nodes == 5
        assert s.total_edges == 4
        assert s.root_count == 2
        assert s.leaf_count == 1

    def test_zero_values(self):
        s = GraphStats(total_nodes=0, total_edges=0, root_count=0, leaf_count=0)
        assert s.total_nodes == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_graph_no_docs(self):
        g = DocDependencyGraph()
        assert g.all_docs() == []

    def test_empty_graph_no_edges(self):
        g = DocDependencyGraph()
        assert g.edges() == []

    def test_empty_graph_stats(self):
        g = DocDependencyGraph()
        s = g.stats()
        assert s.total_nodes == 0
        assert s.total_edges == 0
        assert s.root_count == 0
        assert s.leaf_count == 0

    def test_empty_has_no_cycle(self):
        g = DocDependencyGraph()
        assert g.has_cycle() is False


# ---------------------------------------------------------------------------
# TestAddDependency
# ---------------------------------------------------------------------------

class TestAddDependency:
    def test_new_edge_returns_true(self):
        g = DocDependencyGraph()
        assert g.add_dependency("a", "b") is True

    def test_duplicate_edge_returns_false(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert g.add_dependency("a", "b") is False

    def test_both_docs_registered(self):
        g = DocDependencyGraph()
        g.add_dependency("x", "y")
        assert "x" in g.all_docs()
        assert "y" in g.all_docs()

    def test_custom_kind_stored(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b", kind="imports")
        edge = g.edges()[0]
        assert edge.kind == "imports"

    def test_duplicate_does_not_create_second_edge(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("a", "b")
        assert len(g.edges()) == 1

    def test_multiple_different_edges(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("a", "c")
        g.add_dependency("b", "c")
        assert len(g.edges()) == 3


# ---------------------------------------------------------------------------
# TestRemoveDependency
# ---------------------------------------------------------------------------

class TestRemoveDependency:
    def test_existing_edge_returns_true(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert g.remove_dependency("a", "b") is True

    def test_nonexistent_edge_returns_false(self):
        g = DocDependencyGraph()
        assert g.remove_dependency("a", "b") is False

    def test_edge_gone_after_remove(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.remove_dependency("a", "b")
        assert g.has_dependency("a", "b") is False

    def test_nodes_remain_after_remove(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.remove_dependency("a", "b")
        assert "a" in g.all_docs()
        assert "b" in g.all_docs()

    def test_remove_one_of_multiple_edges(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("a", "c")
        g.remove_dependency("a", "b")
        assert g.has_dependency("a", "c") is True
        assert len(g.edges()) == 1


# ---------------------------------------------------------------------------
# TestRemoveDoc
# ---------------------------------------------------------------------------

class TestRemoveDoc:
    def test_returns_count_of_removed_edges(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("c", "a")
        count = g.remove_doc("a")
        assert count == 2

    def test_doc_removed_from_nodes(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.remove_doc("a")
        assert "a" not in g.all_docs()

    def test_incident_edges_removed(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "c")
        g.remove_doc("b")
        assert g.edges() == []

    def test_nonexistent_doc_returns_zero(self):
        g = DocDependencyGraph()
        assert g.remove_doc("ghost") == 0

    def test_isolated_node_removal(self):
        """A registered node with no edges returns 0."""
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.remove_dependency("a", "b")
        count = g.remove_doc("a")
        assert count == 0
        assert "a" not in g.all_docs()


# ---------------------------------------------------------------------------
# TestDependenciesOf
# ---------------------------------------------------------------------------

class TestDependenciesOf:
    def test_empty_when_no_outgoing(self):
        g = DocDependencyGraph()
        g.add_dependency("x", "y")
        assert g.dependencies_of("y") == []

    def test_single_dependency(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert g.dependencies_of("a") == ["b"]

    def test_multiple_dependencies_sorted(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "c")
        g.add_dependency("a", "b")
        assert g.dependencies_of("a") == ["b", "c"]

    def test_unknown_doc_returns_empty(self):
        g = DocDependencyGraph()
        assert g.dependencies_of("unknown") == []


# ---------------------------------------------------------------------------
# TestDependentsOf
# ---------------------------------------------------------------------------

class TestDependentsOf:
    def test_empty_when_no_incoming(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert g.dependents_of("a") == []

    def test_single_dependent(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert g.dependents_of("b") == ["a"]

    def test_multiple_dependents_sorted(self):
        g = DocDependencyGraph()
        g.add_dependency("c", "z")
        g.add_dependency("a", "z")
        assert g.dependents_of("z") == ["a", "c"]

    def test_unknown_doc_returns_empty(self):
        g = DocDependencyGraph()
        assert g.dependents_of("unknown") == []


# ---------------------------------------------------------------------------
# TestHasDependency
# ---------------------------------------------------------------------------

class TestHasDependency:
    def test_returns_true_for_existing_edge(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert g.has_dependency("a", "b") is True

    def test_returns_false_for_missing_edge(self):
        g = DocDependencyGraph()
        assert g.has_dependency("a", "b") is False

    def test_direction_matters(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert g.has_dependency("b", "a") is False


# ---------------------------------------------------------------------------
# TestAllDocs
# ---------------------------------------------------------------------------

class TestAllDocs:
    def test_empty_graph(self):
        g = DocDependencyGraph()
        assert g.all_docs() == []

    def test_sorted_output(self):
        g = DocDependencyGraph()
        g.add_dependency("c", "a")
        g.add_dependency("b", "a")
        assert g.all_docs() == ["a", "b", "c"]

    def test_no_duplicates(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("a", "b")  # duplicate
        docs = g.all_docs()
        assert len(docs) == len(set(docs))


# ---------------------------------------------------------------------------
# TestEdges
# ---------------------------------------------------------------------------

class TestEdges:
    def test_empty_graph(self):
        g = DocDependencyGraph()
        assert g.edges() == []

    def test_single_edge(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        result = g.edges()
        assert len(result) == 1
        assert result[0] == DependencyEdge("a", "b", "depends_on")

    def test_sorted_by_from_to_kind(self):
        g = DocDependencyGraph()
        g.add_dependency("b", "c")
        g.add_dependency("a", "c")
        g.add_dependency("a", "b")
        froms = [e.from_doc for e in g.edges()]
        assert froms == sorted(froms)


# ---------------------------------------------------------------------------
# TestEdgesFromTo
# ---------------------------------------------------------------------------

class TestEdgesFromTo:
    def test_edges_from_returns_correct_edges(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("a", "c")
        g.add_dependency("x", "y")
        result = g.edges_from("a")
        assert all(e.from_doc == "a" for e in result)
        assert len(result) == 2

    def test_edges_from_sorted(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "z")
        g.add_dependency("a", "m")
        to_docs = [e.to_doc for e in g.edges_from("a")]
        assert to_docs == sorted(to_docs)

    def test_edges_from_unknown_doc(self):
        g = DocDependencyGraph()
        assert g.edges_from("ghost") == []

    def test_edges_to_returns_correct_edges(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "z")
        g.add_dependency("b", "z")
        g.add_dependency("c", "x")
        result = g.edges_to("z")
        assert all(e.to_doc == "z" for e in result)
        assert len(result) == 2

    def test_edges_to_sorted(self):
        g = DocDependencyGraph()
        g.add_dependency("z", "target")
        g.add_dependency("a", "target")
        from_docs = [e.from_doc for e in g.edges_to("target")]
        assert from_docs == sorted(from_docs)

    def test_edges_to_unknown_doc(self):
        g = DocDependencyGraph()
        assert g.edges_to("ghost") == []


# ---------------------------------------------------------------------------
# TestHasCycle
# ---------------------------------------------------------------------------

class TestHasCycle:
    def test_no_cycle_in_dag(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "c")
        assert g.has_cycle() is False

    def test_simple_cycle(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "a")
        assert g.has_cycle() is True

    def test_longer_cycle(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "c")
        g.add_dependency("c", "a")
        assert g.has_cycle() is True

    def test_self_loop(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "a")
        assert g.has_cycle() is True

    def test_no_cycle_after_removing_back_edge(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "a")
        g.remove_dependency("b", "a")
        assert g.has_cycle() is False

    def test_diamond_no_cycle(self):
        g = DocDependencyGraph()
        # a -> b, a -> c, b -> d, c -> d  (diamond DAG)
        g.add_dependency("a", "b")
        g.add_dependency("a", "c")
        g.add_dependency("b", "d")
        g.add_dependency("c", "d")
        assert g.has_cycle() is False


# ---------------------------------------------------------------------------
# TestTopologicalSort
# ---------------------------------------------------------------------------

class TestTopologicalSort:
    def test_simple_chain(self):
        # "b depends on a": edge b -> a means _in[a]={b}, in-degree(b)=0
        # Kahn's puts nodes with in-degree 0 first, so b comes before a
        g = DocDependencyGraph()
        g.add_dependency("b", "a")
        result = g.topological_sort()
        # b has no incoming edges (in-degree 0) => b precedes a
        assert result.index("b") < result.index("a")

    def test_diamond_shape(self):
        # Edges: a->b, a->c, b->d, c->d
        # In-degrees: a=0, b=1, c=1, d=2
        # Kahn's: a first, then b/c, then d
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("a", "c")
        g.add_dependency("b", "d")
        g.add_dependency("c", "d")
        result = g.topological_sort()
        # a has in-degree 0, so it comes before b, c, d
        assert result.index("a") < result.index("b")
        assert result.index("a") < result.index("c")
        # b and c come before d
        assert result.index("b") < result.index("d")
        assert result.index("c") < result.index("d")

    def test_raises_on_cycle(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "a")
        with pytest.raises(ValueError, match="cycles"):
            g.topological_sort()

    def test_all_nodes_present(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "c")
        result = g.topological_sort()
        assert sorted(result) == ["a", "b", "c"]

    def test_empty_graph(self):
        g = DocDependencyGraph()
        assert g.topological_sort() == []


# ---------------------------------------------------------------------------
# TestReachableFrom
# ---------------------------------------------------------------------------

class TestReachableFrom:
    def test_direct_dependency(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert g.reachable_from("a") == ["b"]

    def test_transitive(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "c")
        result = g.reachable_from("a")
        assert sorted(result) == ["b", "c"]

    def test_empty_for_leaf(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert g.reachable_from("b") == []

    def test_self_excluded(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        assert "a" not in g.reachable_from("a")

    def test_unknown_doc_returns_empty(self):
        g = DocDependencyGraph()
        assert g.reachable_from("ghost") == []

    def test_sorted_output(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "c")
        g.add_dependency("a", "b")
        result = g.reachable_from("a")
        assert result == sorted(result)

    def test_cycle_safe(self):
        """reachable_from must not loop infinitely on cycles."""
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "c")
        g.add_dependency("c", "a")
        result = g.reachable_from("a")
        assert set(result) == {"b", "c"}


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty_graph(self):
        g = DocDependencyGraph()
        s = g.stats()
        assert s.total_nodes == 0
        assert s.total_edges == 0
        assert s.root_count == 0
        assert s.leaf_count == 0

    def test_single_edge(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        s = g.stats()
        assert s.total_nodes == 2
        assert s.total_edges == 1

    def test_root_count(self):
        """Roots = nodes with no incoming edges."""
        g = DocDependencyGraph()
        # a -> b -> c
        g.add_dependency("a", "b")
        g.add_dependency("b", "c")
        s = g.stats()
        # only 'a' has in-degree 0 in this graph
        assert s.root_count == 1

    def test_leaf_count(self):
        """Leaves = nodes with no outgoing edges."""
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("a", "c")
        s = g.stats()
        # b and c have no outgoing edges
        assert s.leaf_count == 2

    def test_isolated_node_is_both_root_and_leaf(self):
        """A standalone node (no edges at all) is both a root and a leaf."""
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.remove_dependency("a", "b")
        # both a and b are isolated
        s = g.stats()
        assert s.root_count == 2
        assert s.leaf_count == 2

    def test_totals_after_remove(self):
        g = DocDependencyGraph()
        g.add_dependency("a", "b")
        g.add_dependency("b", "c")
        g.remove_dependency("a", "b")
        s = g.stats()
        assert s.total_edges == 1
        assert s.total_nodes == 3


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_add_dependency(self):
        """Multiple threads adding edges must not corrupt internal state."""
        g = DocDependencyGraph()
        errors: list[Exception] = []

        def worker(n: int) -> None:
            try:
                for i in range(20):
                    g.add_dependency(f"doc_{n}", f"dep_{i}")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        # All added nodes should appear in all_docs without duplicates
        docs = g.all_docs()
        assert len(docs) == len(set(docs))

    def test_concurrent_add_and_remove(self):
        """Concurrent adds and removes must not raise exceptions."""
        g = DocDependencyGraph()
        errors: list[Exception] = []

        def adder(n: int) -> None:
            try:
                for i in range(10):
                    g.add_dependency(f"a{n}", f"b{i}")
            except Exception as exc:
                errors.append(exc)

        def remover(n: int) -> None:
            try:
                for i in range(10):
                    g.remove_dependency(f"a{n}", f"b{i}")
            except Exception as exc:
                errors.append(exc)

        threads = (
            [threading.Thread(target=adder, args=(t,)) for t in range(4)]
            + [threading.Thread(target=remover, args=(t,)) for t in range(4)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
