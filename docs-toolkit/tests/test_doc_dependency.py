"""Tests for docstoolkit.doc_dependency."""
import threading

import pytest

from docstoolkit.doc_dependency import (
    Dependency,
    DependencyGraph,
    DependencyType,
    DocDependency,
    ResolveResult,
)


class TestDependencyType:
    def test_members(self):
        assert DependencyType.REQUIRES.value == "requires"
        assert DependencyType.RECOMMENDS.value == "recommends"
        assert DependencyType.RELATES_TO.value == "relates_to"
        assert DependencyType.CONFLICTS_WITH.value == "conflicts_with"
        assert DependencyType.REPLACES.value == "replaces"

    def test_count(self):
        assert len(list(DependencyType)) == 5


class TestDependency:
    def test_defaults(self):
        d = Dependency(source="a", target="b")
        assert d.source == "a"
        assert d.target == "b"
        assert d.dep_type == DependencyType.REQUIRES
        assert d.priority == 0
        assert d.notes is None

    def test_custom(self):
        d = Dependency(
            source="x",
            target="y",
            dep_type=DependencyType.RECOMMENDS,
            priority=5,
            notes="reason",
        )
        assert d.dep_type == DependencyType.RECOMMENDS
        assert d.priority == 5
        assert d.notes == "reason"


class TestDependencyGraph:
    def test_defaults(self):
        g = DependencyGraph(docs=["a"], dependencies=[])
        assert g.docs == ["a"]
        assert g.dependencies == []
        assert g.has_cycle is False
        assert g.build_order == []

    def test_with_data(self):
        dep = Dependency(source="a", target="b")
        g = DependencyGraph(
            docs=["a", "b"],
            dependencies=[dep],
            has_cycle=False,
            build_order=["b", "a"],
        )
        assert g.build_order == ["b", "a"]


class TestResolveResult:
    def test_basic(self):
        r = ResolveResult(
            target_doc_id="a", chain=["b"], missing=[], conflicts=[]
        )
        assert r.target_doc_id == "a"
        assert r.chain == ["b"]
        assert r.missing == []
        assert r.conflicts == []


class TestRegisterDoc:
    def test_register_new(self):
        d = DocDependency()
        assert d.register_doc("a") is True
        assert d.doc_count == 1

    def test_register_duplicate(self):
        d = DocDependency()
        d.register_doc("a")
        assert d.register_doc("a") is False
        assert d.doc_count == 1

    def test_register_empty_string(self):
        d = DocDependency()
        assert d.register_doc("") is False
        assert d.doc_count == 0

    def test_register_many(self):
        d = DocDependency()
        for i in range(10):
            d.register_doc(f"doc-{i}")
        assert d.doc_count == 10


class TestUnregisterDoc:
    def test_unregister_existing(self):
        d = DocDependency()
        d.register_doc("a")
        assert d.unregister_doc("a") is True
        assert d.doc_count == 0

    def test_unregister_missing(self):
        d = DocDependency()
        assert d.unregister_doc("ghost") is False

    def test_cascade_outgoing(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("a", "c", DependencyType.RECOMMENDS)
        assert d.dependency_count == 2
        d.unregister_doc("a")
        assert d.dependency_count == 0

    def test_cascade_incoming(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("c", "b")
        assert d.dependency_count == 2
        d.unregister_doc("b")
        assert d.dependency_count == 0

    def test_cascade_does_not_remove_others(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("c", "e")
        d.unregister_doc("a")
        assert d.dependency_count == 1


class TestAddDependency:
    def test_add_basic(self):
        d = DocDependency()
        dep = d.add_dependency("a", "b")
        assert isinstance(dep, Dependency)
        assert dep.source == "a"
        assert dep.target == "b"
        assert dep.dep_type == DependencyType.REQUIRES

    def test_add_auto_registers_docs(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        assert d.doc_count == 2

    def test_add_self_loop_rejected(self):
        d = DocDependency()
        assert d.add_dependency("a", "a") is None

    def test_add_empty_source(self):
        d = DocDependency()
        assert d.add_dependency("", "b") is None

    def test_add_empty_target(self):
        d = DocDependency()
        assert d.add_dependency("a", "") is None

    def test_add_duplicate_returns_none(self):
        d = DocDependency()
        first = d.add_dependency("a", "b")
        second = d.add_dependency("a", "b")
        assert first is not None
        assert second is None

    def test_add_different_dep_types_allowed(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.REQUIRES)
        d.add_dependency("a", "b", DependencyType.RECOMMENDS)
        assert d.dependency_count == 2

    def test_add_with_priority_and_notes(self):
        d = DocDependency()
        dep = d.add_dependency(
            "a", "b", priority=10, notes="critical"
        )
        assert dep.priority == 10
        assert dep.notes == "critical"


class TestRemoveDependency:
    def test_remove_specific_type(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.REQUIRES)
        d.add_dependency("a", "b", DependencyType.RECOMMENDS)
        assert d.remove_dependency("a", "b", DependencyType.REQUIRES) is True
        assert d.dependency_count == 1

    def test_remove_all_types(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.REQUIRES)
        d.add_dependency("a", "b", DependencyType.RECOMMENDS)
        assert d.remove_dependency("a", "b") is True
        assert d.dependency_count == 0

    def test_remove_nonexistent(self):
        d = DocDependency()
        assert d.remove_dependency("a", "b") is False

    def test_remove_specific_type_missing(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.REQUIRES)
        assert (
            d.remove_dependency("a", "b", DependencyType.RECOMMENDS) is False
        )


class TestDependenciesOf:
    def test_outgoing(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("a", "c")
        deps = d.dependencies_of("a")
        assert len(deps) == 2

    def test_filter_by_type(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.REQUIRES)
        d.add_dependency("a", "c", DependencyType.RECOMMENDS)
        reqs = d.dependencies_of("a", DependencyType.REQUIRES)
        assert len(reqs) == 1
        assert reqs[0].target == "b"

    def test_empty_for_unknown(self):
        d = DocDependency()
        assert d.dependencies_of("ghost") == []


class TestDependentsOf:
    def test_incoming(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("c", "b")
        deps = d.dependents_of("b")
        assert len(deps) == 2

    def test_filter_by_type(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.REQUIRES)
        d.add_dependency("c", "b", DependencyType.RECOMMENDS)
        recs = d.dependents_of("b", DependencyType.RECOMMENDS)
        assert len(recs) == 1
        assert recs[0].source == "c"

    def test_empty(self):
        d = DocDependency()
        assert d.dependents_of("ghost") == []


class TestRequires:
    def test_direct(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        assert "b" in d.requires("a")

    def test_transitive(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "c")
        d.add_dependency("c", "d")
        result = d.requires("a")
        assert set(result) == {"b", "c", "d"}

    def test_only_requires_type(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.REQUIRES)
        d.add_dependency("a", "c", DependencyType.RECOMMENDS)
        result = d.requires("a")
        assert result == ["b"]

    def test_no_deps(self):
        d = DocDependency()
        d.register_doc("a")
        assert d.requires("a") == []


class TestRequiredBy:
    def test_direct(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        assert "a" in d.required_by("b")

    def test_transitive(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "c")
        result = d.required_by("c")
        assert set(result) == {"a", "b"}

    def test_excludes_other_types(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.RECOMMENDS)
        assert d.required_by("b") == []


class TestRecommends:
    def test_direct(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.RECOMMENDS)
        assert d.recommends("a") == ["b"]

    def test_empty(self):
        d = DocDependency()
        d.register_doc("a")
        assert d.recommends("a") == []


class TestRelated:
    def test_undirected(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.RELATES_TO)
        assert "b" in d.related("a")
        assert "a" in d.related("b")

    def test_multiple(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.RELATES_TO)
        d.add_dependency("c", "a", DependencyType.RELATES_TO)
        assert set(d.related("a")) == {"b", "c"}


class TestConflictsWith:
    def test_undirected(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.CONFLICTS_WITH)
        assert "b" in d.conflicts_with("a")
        assert "a" in d.conflicts_with("b")

    def test_empty(self):
        d = DocDependency()
        d.register_doc("a")
        assert d.conflicts_with("a") == []


class TestResolve:
    def test_simple_chain(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "c")
        result = d.resolve("a")
        assert result.target_doc_id == "a"
        # deepest first: c then b
        assert result.chain.index("c") < result.chain.index("b")

    def test_no_deps(self):
        d = DocDependency()
        d.register_doc("a")
        result = d.resolve("a")
        assert result.chain == []
        assert result.missing == []

    def test_diamond(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("a", "c")
        d.add_dependency("b", "d")
        d.add_dependency("c", "d")
        result = d.resolve("a")
        assert set(result.chain) == {"b", "c", "d"}

    def test_with_conflicts(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("a", "c")
        d.add_dependency("b", "c", DependencyType.CONFLICTS_WITH)
        result = d.resolve("a")
        assert ("b", "c") in result.conflicts


class TestResolveMissing:
    def test_missing_target(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        # b auto-registered by add_dependency; force unregister
        d._docs.discard("b")
        result = d.resolve("a")
        assert "b" in result.missing

    def test_no_missing_when_registered(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        result = d.resolve("a")
        assert result.missing == []


class TestBuildOrder:
    def test_simple(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        order = d.build_order()
        # b must come before a (b is dependency of a)
        assert order.index("b") < order.index("a")

    def test_chain(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "c")
        order = d.build_order()
        assert order.index("c") < order.index("b") < order.index("a")

    def test_isolated_docs_included(self):
        d = DocDependency()
        d.register_doc("solo")
        d.add_dependency("a", "b")
        order = d.build_order()
        assert "solo" in order
        assert "a" in order and "b" in order

    def test_subset(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "c")
        d.register_doc("x")
        order = d.build_order(["a", "b", "c"])
        assert "x" not in order
        assert len(order) == 3

    def test_ignores_non_requires(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.RECOMMENDS)
        # No REQUIRES => any order is acceptable; both should be present
        order = d.build_order()
        assert set(order) == {"a", "b"}


class TestBuildOrderCycle:
    def test_two_node_cycle(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "a")
        with pytest.raises(ValueError):
            d.build_order()

    def test_self_loop_not_possible(self):
        # self-loop is rejected, so no cycle
        d = DocDependency()
        d.add_dependency("a", "a")
        # No edge added; build_order should succeed (a is unregistered though)
        order = d.build_order()
        assert order == []

    def test_three_node_cycle(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "c")
        d.add_dependency("c", "a")
        with pytest.raises(ValueError):
            d.build_order()


class TestHasCycle:
    def test_no_cycle(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        assert d.has_cycle() is False

    def test_with_cycle(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "a")
        assert d.has_cycle() is True

    def test_cycle_on_other_type(self):
        d = DocDependency()
        d.add_dependency("a", "b", DependencyType.RECOMMENDS)
        d.add_dependency("b", "a", DependencyType.RECOMMENDS)
        assert d.has_cycle(DependencyType.RECOMMENDS) is True
        assert d.has_cycle(DependencyType.REQUIRES) is False


class TestFindCycles:
    def test_no_cycles(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        assert d.find_cycles() == []

    def test_one_cycle(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "a")
        cycles = d.find_cycles()
        assert len(cycles) == 1
        assert set(cycles[0]) == {"a", "b"}

    def test_longer_cycle(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "c")
        d.add_dependency("c", "a")
        cycles = d.find_cycles()
        assert len(cycles) == 1
        assert set(cycles[0]) == {"a", "b", "c"}


class TestRoots:
    def test_basic(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "c")
        # roots: docs with no incoming REQUIRES = a
        roots = d.roots()
        assert "a" in roots
        assert "c" not in roots

    def test_isolated_is_root(self):
        d = DocDependency()
        d.register_doc("alone")
        assert "alone" in d.roots()


class TestLeaves:
    def test_basic(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "c")
        leaves = d.leaves()
        assert "c" in leaves
        assert "a" not in leaves

    def test_isolated_is_leaf(self):
        d = DocDependency()
        d.register_doc("alone")
        assert "alone" in d.leaves()


class TestGraph:
    def test_full_graph(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        g = d.graph()
        assert isinstance(g, DependencyGraph)
        assert set(g.docs) == {"a", "b"}
        assert len(g.dependencies) == 1

    def test_subset_graph(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("c", "e")
        g = d.graph(["a", "b"])
        assert set(g.docs) == {"a", "b"}
        assert len(g.dependencies) == 1

    def test_graph_has_cycle_flag(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("b", "a")
        g = d.graph()
        assert g.has_cycle is True
        assert g.build_order == []


class TestDocCount:
    def test_zero(self):
        d = DocDependency()
        assert d.doc_count == 0

    def test_after_register(self):
        d = DocDependency()
        d.register_doc("a")
        d.register_doc("b")
        assert d.doc_count == 2

    def test_after_add_dependency(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        assert d.doc_count == 2


class TestDependencyCount:
    def test_zero(self):
        d = DocDependency()
        assert d.dependency_count == 0

    def test_after_add(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.add_dependency("c", "e")
        assert d.dependency_count == 2

    def test_after_remove(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.remove_dependency("a", "b")
        assert d.dependency_count == 0


class TestClear:
    def test_clear_all(self):
        d = DocDependency()
        d.add_dependency("a", "b")
        d.register_doc("c")
        d.clear()
        assert d.doc_count == 0
        assert d.dependency_count == 0

    def test_clear_idempotent(self):
        d = DocDependency()
        d.clear()
        d.clear()
        assert d.doc_count == 0


class TestEdgeCases:
    def test_thread_safety_add(self):
        d = DocDependency()

        def worker(start: int):
            for i in range(start, start + 50):
                d.add_dependency(f"src-{i}", f"tgt-{i}")

        threads = [threading.Thread(target=worker, args=(i * 100,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert d.dependency_count == 200

    def test_unregister_then_re_register(self):
        d = DocDependency()
        d.register_doc("a")
        d.unregister_doc("a")
        assert d.register_doc("a") is True

    def test_resolve_unknown_doc(self):
        d = DocDependency()
        result = d.resolve("ghost")
        assert result.target_doc_id == "ghost"
        assert result.chain == []

    def test_long_chain_resolve(self):
        d = DocDependency()
        for i in range(20):
            d.add_dependency(f"d{i}", f"d{i+1}")
        result = d.resolve("d0")
        assert len(result.chain) == 20
        # deepest first
        assert result.chain[0] == "d20"

    def test_priority_preserved(self):
        d = DocDependency()
        d.add_dependency("a", "b", priority=99)
        deps = d.dependencies_of("a")
        assert deps[0].priority == 99

    def test_notes_preserved(self):
        d = DocDependency()
        d.add_dependency("a", "b", notes="hello")
        deps = d.dependencies_of("a")
        assert deps[0].notes == "hello"

    def test_replaces_type(self):
        d = DocDependency()
        d.add_dependency("new", "old", DependencyType.REPLACES)
        deps = d.dependencies_of("new", DependencyType.REPLACES)
        assert len(deps) == 1
        assert deps[0].target == "old"
