"""Tests for E429 :mod:`docstoolkit.doc_dependency_resolver`."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_dependency_resolver import (
    Dependency,
    DocDependencyResolver,
    ResolutionResult,
    ResolverStats,
)


# ---------------------------------------------------------------------------
# Dataclass smoke tests
# ---------------------------------------------------------------------------


def test_dependency_defaults():
    dep = Dependency(from_doc="a", to_doc="b")
    assert dep.from_doc == "a"
    assert dep.to_doc == "b"
    assert dep.kind == "depends_on"


def test_dependency_custom_kind():
    dep = Dependency(from_doc="x", to_doc="y", kind="references")
    assert dep.kind == "references"


def test_resolution_result_defaults():
    r = ResolutionResult()
    assert r.order == []
    assert r.has_cycle is False
    assert r.cycle_nodes == []
    assert r.unresolved == []


def test_resolver_stats_construction():
    s = ResolverStats(
        total_nodes=3,
        total_dependencies=2,
        resolutions_performed=1,
        cycles_detected=0,
    )
    assert s.total_nodes == 3
    assert s.total_dependencies == 2
    assert s.resolutions_performed == 1
    assert s.cycles_detected == 0


# ---------------------------------------------------------------------------
# add_node
# ---------------------------------------------------------------------------


def test_add_node_new_returns_true():
    r = DocDependencyResolver()
    assert r.add_node("a") is True


def test_add_node_duplicate_returns_false():
    r = DocDependencyResolver()
    r.add_node("a")
    assert r.add_node("a") is False


def test_add_node_registers_in_all_nodes():
    r = DocDependencyResolver()
    r.add_node("foo")
    r.add_node("bar")
    assert r.all_nodes() == ["bar", "foo"]


# ---------------------------------------------------------------------------
# add_dependency
# ---------------------------------------------------------------------------


def test_add_dependency_new_returns_true():
    r = DocDependencyResolver()
    assert r.add_dependency(Dependency("a", "b")) is True


def test_add_dependency_duplicate_returns_false():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    assert r.add_dependency(Dependency("a", "b")) is False


def test_add_dependency_auto_registers_nodes():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    assert r.all_nodes() == ["a", "b"]


def test_add_dependency_populates_forward():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    assert r.dependencies_of("a") == ["b"]


def test_add_dependency_populates_reverse():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    assert r.dependents_of("b") == ["a"]


def test_add_dependency_multiple_targets():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("a", "c"))
    assert r.dependencies_of("a") == ["b", "c"]


def test_add_dependency_kind_field_ignored_for_dedup():
    # Same (from, to) pair with different kind still counts as duplicate.
    r = DocDependencyResolver()
    assert r.add_dependency(Dependency("a", "b", kind="depends_on")) is True
    assert r.add_dependency(Dependency("a", "b", kind="references")) is False


# ---------------------------------------------------------------------------
# remove_dependency
# ---------------------------------------------------------------------------


def test_remove_dependency_existing_returns_true():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    assert r.remove_dependency("a", "b") is True


def test_remove_dependency_missing_returns_false():
    r = DocDependencyResolver()
    assert r.remove_dependency("a", "b") is False


def test_remove_dependency_unknown_from_returns_false():
    r = DocDependencyResolver()
    r.add_node("b")
    assert r.remove_dependency("a", "b") is False


def test_remove_dependency_clears_forward():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.remove_dependency("a", "b")
    assert r.dependencies_of("a") == []


def test_remove_dependency_clears_reverse():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.remove_dependency("a", "b")
    assert r.dependents_of("b") == []


def test_remove_dependency_keeps_nodes():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.remove_dependency("a", "b")
    assert r.all_nodes() == ["a", "b"]


# ---------------------------------------------------------------------------
# remove_node
# ---------------------------------------------------------------------------


def test_remove_node_existing_returns_true():
    r = DocDependencyResolver()
    r.add_node("a")
    assert r.remove_node("a") is True


def test_remove_node_missing_returns_false():
    r = DocDependencyResolver()
    assert r.remove_node("ghost") is False


def test_remove_node_clears_outgoing_edges():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.remove_node("a")
    assert r.dependents_of("b") == []


def test_remove_node_clears_incoming_edges():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.remove_node("b")
    assert r.dependencies_of("a") == []


def test_remove_node_drops_from_all_nodes():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.remove_node("a")
    assert "a" not in r.all_nodes()


def test_remove_node_idempotent():
    r = DocDependencyResolver()
    r.add_node("a")
    r.remove_node("a")
    assert r.remove_node("a") is False


# ---------------------------------------------------------------------------
# dependencies_of / dependents_of
# ---------------------------------------------------------------------------


def test_dependencies_of_unknown_node_empty():
    r = DocDependencyResolver()
    assert r.dependencies_of("nope") == []


def test_dependents_of_unknown_node_empty():
    r = DocDependencyResolver()
    assert r.dependents_of("nope") == []


def test_dependencies_of_sorted():
    r = DocDependencyResolver()
    for tgt in ["z", "m", "a", "c"]:
        r.add_dependency(Dependency("x", tgt))
    assert r.dependencies_of("x") == ["a", "c", "m", "z"]


def test_dependents_of_sorted():
    r = DocDependencyResolver()
    for src in ["z", "m", "a", "c"]:
        r.add_dependency(Dependency(src, "x"))
    assert r.dependents_of("x") == ["a", "c", "m", "z"]


def test_dependencies_of_isolated_node():
    r = DocDependencyResolver()
    r.add_node("solo")
    assert r.dependencies_of("solo") == []
    assert r.dependents_of("solo") == []


# ---------------------------------------------------------------------------
# all_nodes
# ---------------------------------------------------------------------------


def test_all_nodes_empty():
    r = DocDependencyResolver()
    assert r.all_nodes() == []


def test_all_nodes_sorted():
    r = DocDependencyResolver()
    r.add_node("c")
    r.add_node("a")
    r.add_node("b")
    assert r.all_nodes() == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# resolve — topological order
# ---------------------------------------------------------------------------


def test_resolve_empty():
    r = DocDependencyResolver()
    res = r.resolve()
    assert res.order == []
    assert res.has_cycle is False


def test_resolve_single_node():
    r = DocDependencyResolver()
    r.add_node("a")
    res = r.resolve()
    assert res.order == ["a"]
    assert res.has_cycle is False


def test_resolve_linear_chain():
    # c -> b -> a, so order is [a, b, c] (deps first).
    r = DocDependencyResolver()
    r.add_dependency(Dependency("c", "b"))
    r.add_dependency(Dependency("b", "a"))
    res = r.resolve()
    assert res.order == ["a", "b", "c"]
    assert res.has_cycle is False


def test_resolve_dependencies_emitted_before_dependents():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("app", "lib"))
    r.add_dependency(Dependency("lib", "core"))
    res = r.resolve()
    assert res.order.index("core") < res.order.index("lib") < res.order.index("app")


def test_resolve_diamond():
    # d depends on b and c; b and c depend on a.
    r = DocDependencyResolver()
    r.add_dependency(Dependency("d", "b"))
    r.add_dependency(Dependency("d", "c"))
    r.add_dependency(Dependency("b", "a"))
    r.add_dependency(Dependency("c", "a"))
    res = r.resolve()
    assert res.order[0] == "a"
    assert res.order[-1] == "d"
    assert set(res.order[1:3]) == {"b", "c"}
    assert res.has_cycle is False


def test_resolve_disjoint_components():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("b", "a"))
    r.add_dependency(Dependency("y", "x"))
    res = r.resolve()
    assert res.order.index("a") < res.order.index("b")
    assert res.order.index("x") < res.order.index("y")
    assert not res.has_cycle


def test_resolve_self_loop_is_cycle():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "a"))
    res = r.resolve()
    assert res.has_cycle is True
    assert "a" in res.cycle_nodes
    assert "a" in res.unresolved


def test_resolve_two_node_cycle():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "a"))
    res = r.resolve()
    assert res.has_cycle is True
    assert set(res.cycle_nodes) == {"a", "b"}
    assert set(res.unresolved) == {"a", "b"}


def test_resolve_partial_progress_before_cycle():
    # x depends on (a) and on (b->c->b cycle).  ``a`` should still be in order.
    r = DocDependencyResolver()
    r.add_dependency(Dependency("x", "a"))
    r.add_dependency(Dependency("x", "b"))
    r.add_dependency(Dependency("b", "c"))
    r.add_dependency(Dependency("c", "b"))
    res = r.resolve()
    assert res.has_cycle is True
    assert "a" in res.order
    assert {"b", "c"}.issubset(set(res.cycle_nodes))


def test_resolve_increments_resolutions():
    r = DocDependencyResolver()
    r.add_node("a")
    before = r.stats().resolutions_performed
    r.resolve()
    r.resolve()
    after = r.stats().resolutions_performed
    assert after - before == 2


def test_resolve_increments_cycles_only_on_cycle():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.resolve()
    assert r.stats().cycles_detected == 0
    r.add_dependency(Dependency("b", "a"))
    r.resolve()
    assert r.stats().cycles_detected == 1


def test_resolve_deterministic_within_layer():
    r = DocDependencyResolver()
    for name in ["d", "a", "c", "b"]:
        r.add_node(name)
    res = r.resolve()
    assert res.order == ["a", "b", "c", "d"]


# ---------------------------------------------------------------------------
# resolve_subset
# ---------------------------------------------------------------------------


def test_resolve_subset_empty_roots():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    res = r.resolve_subset([])
    assert res.order == []


def test_resolve_subset_unknown_root_ignored():
    r = DocDependencyResolver()
    r.add_node("a")
    res = r.resolve_subset(["ghost"])
    assert res.order == []


def test_resolve_subset_includes_root_only_when_no_deps():
    r = DocDependencyResolver()
    r.add_node("a")
    r.add_node("b")
    res = r.resolve_subset(["a"])
    assert res.order == ["a"]


def test_resolve_subset_includes_transitive_deps():
    # c -> b -> a; asking for c should return [a, b, c].
    r = DocDependencyResolver()
    r.add_dependency(Dependency("c", "b"))
    r.add_dependency(Dependency("b", "a"))
    res = r.resolve_subset(["c"])
    assert res.order == ["a", "b", "c"]


def test_resolve_subset_excludes_unrelated_branch():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("c", "b"))
    r.add_dependency(Dependency("b", "a"))
    r.add_dependency(Dependency("z", "y"))
    res = r.resolve_subset(["c"])
    assert "z" not in res.order
    assert "y" not in res.order


def test_resolve_subset_detects_cycle_in_subgraph():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "a"))
    r.add_dependency(Dependency("z", "y"))  # outside, healthy
    res = r.resolve_subset(["a"])
    assert res.has_cycle is True
    assert set(res.cycle_nodes) == {"a", "b"}


def test_resolve_subset_increments_resolutions():
    r = DocDependencyResolver()
    r.add_node("a")
    before = r.stats().resolutions_performed
    r.resolve_subset(["a"])
    assert r.stats().resolutions_performed == before + 1


# ---------------------------------------------------------------------------
# has_cycle (quick check)
# ---------------------------------------------------------------------------


def test_has_cycle_false_for_empty():
    assert DocDependencyResolver().has_cycle() is False


def test_has_cycle_false_for_dag():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "c"))
    assert r.has_cycle() is False


def test_has_cycle_true_for_self_loop():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("x", "x"))
    assert r.has_cycle() is True


def test_has_cycle_true_for_two_cycle():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "a"))
    assert r.has_cycle() is True


def test_has_cycle_does_not_increment_stats():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    before = r.stats()
    r.has_cycle()
    after = r.stats()
    assert before.resolutions_performed == after.resolutions_performed
    assert before.cycles_detected == after.cycles_detected


# ---------------------------------------------------------------------------
# find_cycles
# ---------------------------------------------------------------------------


def test_find_cycles_empty():
    assert DocDependencyResolver().find_cycles() == []


def test_find_cycles_dag():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "c"))
    assert r.find_cycles() == []


def test_find_cycles_self_loop():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "a"))
    cycles = r.find_cycles()
    assert cycles == [["a"]]


def test_find_cycles_two_cycle():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "a"))
    cycles = r.find_cycles()
    assert len(cycles) == 1
    # Cycle should start with smallest element 'a'.
    assert cycles[0][0] == "a"
    assert set(cycles[0]) == {"a", "b"}


def test_find_cycles_three_cycle():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "c"))
    r.add_dependency(Dependency("c", "a"))
    cycles = r.find_cycles()
    assert len(cycles) == 1
    assert cycles[0][0] == "a"
    assert set(cycles[0]) == {"a", "b", "c"}


def test_find_cycles_two_independent_cycles():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "a"))
    r.add_dependency(Dependency("x", "y"))
    r.add_dependency(Dependency("y", "x"))
    cycles = r.find_cycles()
    assert len(cycles) == 2
    sets = [set(c) for c in cycles]
    assert {"a", "b"} in sets
    assert {"x", "y"} in sets


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_empty():
    s = DocDependencyResolver().stats()
    assert s.total_nodes == 0
    assert s.total_dependencies == 0
    assert s.resolutions_performed == 0
    assert s.cycles_detected == 0


def test_stats_counts_nodes_and_edges():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("a", "c"))
    r.add_node("d")
    s = r.stats()
    assert s.total_nodes == 4
    assert s.total_dependencies == 2


def test_stats_reflects_removals():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("a", "c"))
    r.remove_dependency("a", "b")
    s = r.stats()
    assert s.total_dependencies == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_concurrent_add_dependency_no_loss():
    r = DocDependencyResolver()
    errors: list[BaseException] = []

    def worker(start: int) -> None:
        try:
            for i in range(50):
                r.add_dependency(Dependency(f"n{start}_{i}", "shared"))
        except BaseException as exc:  # pragma: no cover - safety net
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    # 8 threads * 50 edges = 400 unique sources all pointing to 'shared'.
    assert len(r.dependents_of("shared")) == 400


def test_concurrent_add_and_resolve_no_crash():
    r = DocDependencyResolver()
    errors: list[BaseException] = []
    stop = threading.Event()

    def writer() -> None:
        try:
            i = 0
            while not stop.is_set():
                r.add_dependency(Dependency(f"a{i}", f"b{i}"))
                i += 1
        except BaseException as exc:  # pragma: no cover
            errors.append(exc)

    def reader() -> None:
        try:
            for _ in range(20):
                r.resolve()
        except BaseException as exc:  # pragma: no cover
            errors.append(exc)

    w = threading.Thread(target=writer)
    rt = threading.Thread(target=reader)
    w.start()
    rt.start()
    rt.join()
    stop.set()
    w.join()
    assert not errors


def test_concurrent_remove_and_query():
    r = DocDependencyResolver()
    for i in range(50):
        r.add_dependency(Dependency(f"src{i}", "target"))

    errors: list[BaseException] = []

    def remover() -> None:
        try:
            for i in range(50):
                r.remove_dependency(f"src{i}", "target")
        except BaseException as exc:  # pragma: no cover
            errors.append(exc)

    def querier() -> None:
        try:
            for _ in range(50):
                r.dependents_of("target")
                r.all_nodes()
                r.stats()
        except BaseException as exc:  # pragma: no cover
            errors.append(exc)

    rm = threading.Thread(target=remover)
    qr = threading.Thread(target=querier)
    rm.start()
    qr.start()
    rm.join()
    qr.join()
    assert not errors
    assert r.dependents_of("target") == []


def test_concurrent_resolutions_counted():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))

    def worker() -> None:
        for _ in range(25):
            r.resolve()

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert r.stats().resolutions_performed == 100


# ---------------------------------------------------------------------------
# Integration / end-to-end
# ---------------------------------------------------------------------------


def test_full_workflow_dag():
    r = DocDependencyResolver()
    edges = [
        ("paper", "intro"),
        ("paper", "results"),
        ("results", "data"),
        ("intro", "abstract"),
    ]
    for src, tgt in edges:
        r.add_dependency(Dependency(src, tgt))

    res = r.resolve()
    assert not res.has_cycle
    # Leaves before parents.
    for src, tgt in edges:
        assert res.order.index(tgt) < res.order.index(src)


def test_full_workflow_break_cycle():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "c"))
    r.add_dependency(Dependency("c", "a"))

    assert r.has_cycle() is True
    r.remove_dependency("c", "a")
    assert r.has_cycle() is False
    res = r.resolve()
    assert res.order == ["c", "b", "a"]


def test_stats_after_mixed_operations():
    r = DocDependencyResolver()
    r.add_dependency(Dependency("a", "b"))
    r.add_dependency(Dependency("b", "c"))
    r.resolve()
    r.add_dependency(Dependency("c", "a"))  # introduces cycle
    r.resolve()
    s = r.stats()
    assert s.total_nodes == 3
    assert s.total_dependencies == 3
    assert s.resolutions_performed == 2
    assert s.cycles_detected == 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
