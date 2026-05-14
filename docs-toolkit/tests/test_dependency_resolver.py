"""Tests for docstoolkit.dependency_resolver (~90 tests)."""
from __future__ import annotations

import pytest

from docstoolkit.dependency_resolver import (
    CyclicDependencyError,
    DependencyNode,
    DependencyResolver,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def node(name: str, *deps: str) -> DependencyNode:
    """Shorthand for building a DependencyNode."""
    return DependencyNode(name=name, deps=list(deps))


# ===========================================================================
# DependencyNode dataclass
# ===========================================================================

class TestDependencyNode:
    def test_name_stored(self):
        n = DependencyNode(name="A")
        assert n.name == "A"

    def test_deps_default_empty(self):
        n = DependencyNode(name="A")
        assert n.deps == []

    def test_deps_stored(self):
        n = DependencyNode(name="A", deps=["B", "C"])
        assert n.deps == ["B", "C"]

    def test_deps_mutable_default_not_shared(self):
        n1 = DependencyNode(name="X")
        n2 = DependencyNode(name="Y")
        n1.deps.append("Z")
        assert n2.deps == []


# ===========================================================================
# CyclicDependencyError
# ===========================================================================

class TestCyclicDependencyError:
    def test_cycle_attribute_stored(self):
        err = CyclicDependencyError(["A", "B", "A"])
        assert err.cycle == ["A", "B", "A"]

    def test_cycle_message_contains_nodes(self):
        err = CyclicDependencyError(["A", "B", "A"])
        msg = str(err)
        assert "A" in msg
        assert "B" in msg

    def test_is_exception_subclass(self):
        err = CyclicDependencyError(["X"])
        assert isinstance(err, Exception)

    def test_empty_cycle_list(self):
        err = CyclicDependencyError([])
        assert err.cycle == []


# ===========================================================================
# DependencyResolver – registration
# ===========================================================================

class TestRegistration:
    def test_node_count_empty(self):
        r = DependencyResolver()
        assert r.node_count() == 0

    def test_add_increases_count(self):
        r = DependencyResolver()
        r.add(node("A"))
        assert r.node_count() == 1

    def test_add_many_increases_count(self):
        r = DependencyResolver()
        r.add_many([node("A"), node("B"), node("C")])
        assert r.node_count() == 3

    def test_add_overwrites_duplicate(self):
        r = DependencyResolver()
        r.add(node("A", "B"))
        r.add(node("A"))          # no deps — overwrites
        r.add(node("B"))
        order = r.resolve()
        # A now has no deps, so both orderings are valid, but both nodes present
        assert set(order) == {"A", "B"}

    def test_add_many_overwrites_duplicate(self):
        r = DependencyResolver()
        r.add(node("A", "B"))
        r.add_many([node("A"), node("B")])  # A now has no deps
        assert r.node_count() == 2

    def test_remove_returns_true_when_found(self):
        r = DependencyResolver()
        r.add(node("A"))
        assert r.remove("A") is True

    def test_remove_returns_false_when_not_found(self):
        r = DependencyResolver()
        assert r.remove("Z") is False

    def test_remove_decreases_count(self):
        r = DependencyResolver()
        r.add(node("A"))
        r.remove("A")
        assert r.node_count() == 0

    def test_clear_resets_state(self):
        r = DependencyResolver()
        r.add_many([node("A"), node("B")])
        r.clear()
        assert r.node_count() == 0

    def test_clear_allows_fresh_add(self):
        r = DependencyResolver()
        r.add(node("A"))
        r.clear()
        r.add(node("B"))
        assert r.node_count() == 1


# ===========================================================================
# DependencyResolver – resolve (basic)
# ===========================================================================

class TestResolveBasic:
    def test_empty_graph_returns_empty_list(self):
        r = DependencyResolver()
        assert r.resolve() == []

    def test_single_node_no_deps(self):
        r = DependencyResolver()
        r.add(node("A"))
        assert r.resolve() == ["A"]

    def test_two_independent_nodes_both_present(self):
        r = DependencyResolver()
        r.add_many([node("A"), node("B")])
        result = r.resolve()
        assert set(result) == {"A", "B"}
        assert len(result) == 2

    def test_dep_appears_before_dependent(self):
        r = DependencyResolver()
        r.add(node("B"))
        r.add(node("A", "B"))   # A depends on B → B must come first
        result = r.resolve()
        assert result.index("B") < result.index("A")

    def test_linear_chain_order(self):
        # A → B → C  (A depends on B, B depends on C)
        # expected: C, B, A
        r = DependencyResolver()
        r.add(node("C"))
        r.add(node("B", "C"))
        r.add(node("A", "B"))
        result = r.resolve()
        assert result.index("C") < result.index("B") < result.index("A")

    def test_linear_chain_length(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        assert len(r.resolve()) == 3

    def test_all_nodes_present_in_resolve(self):
        r = DependencyResolver()
        r.add_many([node("X"), node("Y", "X"), node("Z", "Y")])
        assert set(r.resolve()) == {"X", "Y", "Z"}


# ===========================================================================
# DependencyResolver – resolve (diamond / complex)
# ===========================================================================

class TestResolveDiamond:
    def test_diamond_d_before_b_and_c(self):
        # A → B, A → C, B → D, C → D
        r = DependencyResolver()
        r.add_many([
            node("D"),
            node("B", "D"),
            node("C", "D"),
            node("A", "B", "C"),
        ])
        result = r.resolve()
        assert result.index("D") < result.index("B")
        assert result.index("D") < result.index("C")

    def test_diamond_a_last(self):
        r = DependencyResolver()
        r.add_many([
            node("D"),
            node("B", "D"),
            node("C", "D"),
            node("A", "B", "C"),
        ])
        result = r.resolve()
        assert result[-1] == "A"

    def test_diamond_d_first(self):
        r = DependencyResolver()
        r.add_many([
            node("D"),
            node("B", "D"),
            node("C", "D"),
            node("A", "B", "C"),
        ])
        result = r.resolve()
        assert result[0] == "D"

    def test_diamond_all_nodes_present(self):
        r = DependencyResolver()
        r.add_many([
            node("D"),
            node("B", "D"),
            node("C", "D"),
            node("A", "B", "C"),
        ])
        assert set(r.resolve()) == {"A", "B", "C", "D"}


# ===========================================================================
# DependencyResolver – cycle detection
# ===========================================================================

class TestCycleDetection:
    def test_direct_cycle_raises(self):
        r = DependencyResolver()
        r.add(node("A", "B"))
        r.add(node("B", "A"))
        with pytest.raises(CyclicDependencyError):
            r.resolve()

    def test_direct_cycle_error_contains_nodes(self):
        r = DependencyResolver()
        r.add(node("A", "B"))
        r.add(node("B", "A"))
        with pytest.raises(CyclicDependencyError) as exc_info:
            r.resolve()
        cycle = exc_info.value.cycle
        assert "A" in cycle
        assert "B" in cycle

    def test_three_node_cycle_raises(self):
        r = DependencyResolver()
        r.add(node("A", "B"))
        r.add(node("B", "C"))
        r.add(node("C", "A"))
        with pytest.raises(CyclicDependencyError):
            r.resolve()

    def test_three_node_cycle_contains_all_cycle_nodes(self):
        r = DependencyResolver()
        r.add(node("A", "B"))
        r.add(node("B", "C"))
        r.add(node("C", "A"))
        with pytest.raises(CyclicDependencyError) as exc_info:
            r.resolve()
        cycle = exc_info.value.cycle
        # All three should appear somewhere in the cycle path
        assert len(cycle) >= 3

    def test_self_loop_raises(self):
        r = DependencyResolver()
        r.add(node("A", "A"))
        with pytest.raises(CyclicDependencyError):
            r.resolve()

    def test_cycle_not_raised_for_valid_graph(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        # Should not raise
        r.resolve()

    def test_has_cycle_true_for_direct_cycle(self):
        r = DependencyResolver()
        r.add(node("A", "B"))
        r.add(node("B", "A"))
        assert r.has_cycle() is True

    def test_has_cycle_false_for_acyclic(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        assert r.has_cycle() is False

    def test_has_cycle_false_for_empty(self):
        r = DependencyResolver()
        assert r.has_cycle() is False

    def test_has_cycle_false_for_single_node(self):
        r = DependencyResolver()
        r.add(node("A"))
        assert r.has_cycle() is False

    def test_has_cycle_true_for_three_node_cycle(self):
        r = DependencyResolver()
        r.add(node("A", "B"))
        r.add(node("B", "C"))
        r.add(node("C", "A"))
        assert r.has_cycle() is True


# ===========================================================================
# DependencyResolver – unknown dependency
# ===========================================================================

class TestUnknownDependency:
    def test_unknown_dep_raises_value_error(self):
        r = DependencyResolver()
        r.add(node("A", "MISSING"))
        with pytest.raises(ValueError, match="MISSING"):
            r.resolve()

    def test_unknown_dep_message_contains_dep_name(self):
        r = DependencyResolver()
        r.add(node("X", "GHOST"))
        with pytest.raises(ValueError) as exc_info:
            r.resolve()
        assert "GHOST" in str(exc_info.value)

    def test_no_error_when_all_deps_registered(self):
        r = DependencyResolver()
        r.add_many([node("B"), node("A", "B")])
        r.resolve()  # should not raise


# ===========================================================================
# DependencyResolver – resolve_for
# ===========================================================================

class TestResolveFor:
    def test_resolve_for_single_node_no_deps(self):
        r = DependencyResolver()
        r.add_many([node("A"), node("B")])
        result = r.resolve_for("A")
        assert result == ["A"]

    def test_resolve_for_includes_transitive_deps(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        result = r.resolve_for("A")
        assert set(result) == {"A", "B", "C"}

    def test_resolve_for_name_last(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        result = r.resolve_for("A")
        assert result[-1] == "A"

    def test_resolve_for_order_correct(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        result = r.resolve_for("A")
        assert result.index("C") < result.index("B") < result.index("A")

    def test_resolve_for_excludes_unrelated_nodes(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B"), node("X"), node("Y", "X")])
        result = r.resolve_for("A")
        assert "X" not in result
        assert "Y" not in result

    def test_resolve_for_unknown_name_raises_key_error(self):
        r = DependencyResolver()
        with pytest.raises(KeyError):
            r.resolve_for("NOPE")

    def test_resolve_for_cycle_raises(self):
        r = DependencyResolver()
        r.add(node("A", "B"))
        r.add(node("B", "A"))
        with pytest.raises(CyclicDependencyError):
            r.resolve_for("A")

    def test_resolve_for_diamond_subgraph(self):
        r = DependencyResolver()
        r.add_many([
            node("D"),
            node("B", "D"),
            node("C", "D"),
            node("A", "B", "C"),
            node("Z"),  # unrelated
        ])
        result = r.resolve_for("A")
        assert set(result) == {"A", "B", "C", "D"}
        assert result[-1] == "A"
        assert result[0] == "D"


# ===========================================================================
# DependencyResolver – dependencies_of
# ===========================================================================

class TestDependenciesOf:
    def test_dependencies_of_no_deps(self):
        r = DependencyResolver()
        r.add(node("A"))
        assert r.dependencies_of("A") == set()

    def test_dependencies_of_direct_dep(self):
        r = DependencyResolver()
        r.add_many([node("B"), node("A", "B")])
        assert r.dependencies_of("A") == {"B"}

    def test_dependencies_of_transitive(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        assert r.dependencies_of("A") == {"B", "C"}

    def test_dependencies_of_diamond(self):
        r = DependencyResolver()
        r.add_many([
            node("D"),
            node("B", "D"),
            node("C", "D"),
            node("A", "B", "C"),
        ])
        assert r.dependencies_of("A") == {"B", "C", "D"}

    def test_dependencies_of_does_not_include_self(self):
        r = DependencyResolver()
        r.add_many([node("B"), node("A", "B")])
        assert "A" not in r.dependencies_of("A")

    def test_dependencies_of_unknown_raises_key_error(self):
        r = DependencyResolver()
        with pytest.raises(KeyError):
            r.dependencies_of("MISSING")

    def test_dependencies_of_leaf_node(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        assert r.dependencies_of("C") == set()


# ===========================================================================
# DependencyResolver – dependents_of
# ===========================================================================

class TestDependentsOf:
    def test_dependents_of_no_dependents(self):
        r = DependencyResolver()
        r.add_many([node("B"), node("A", "B")])
        assert r.dependents_of("A") == set()

    def test_dependents_of_direct(self):
        r = DependencyResolver()
        r.add_many([node("B"), node("A", "B")])
        assert r.dependents_of("B") == {"A"}

    def test_dependents_of_transitive(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        # Both B and A depend on C (transitively)
        assert r.dependents_of("C") == {"B", "A"}

    def test_dependents_of_diamond_leaf(self):
        r = DependencyResolver()
        r.add_many([
            node("D"),
            node("B", "D"),
            node("C", "D"),
            node("A", "B", "C"),
        ])
        assert r.dependents_of("D") == {"B", "C", "A"}

    def test_dependents_of_does_not_include_self(self):
        r = DependencyResolver()
        r.add_many([node("B"), node("A", "B")])
        assert "B" not in r.dependents_of("B")

    def test_dependents_of_unknown_raises_key_error(self):
        r = DependencyResolver()
        with pytest.raises(KeyError):
            r.dependents_of("MISSING")

    def test_dependents_of_root_node(self):
        r = DependencyResolver()
        r.add_many([node("C"), node("B", "C"), node("A", "B")])
        # A has no dependents (nothing depends on A)
        assert r.dependents_of("A") == set()


# ===========================================================================
# DependencyResolver – multiple independent chains
# ===========================================================================

class TestMultipleChains:
    def test_two_independent_chains_all_nodes(self):
        # Chain 1: C1 → B1 → A1
        # Chain 2: C2 → B2 → A2
        r = DependencyResolver()
        r.add_many([
            node("C1"), node("B1", "C1"), node("A1", "B1"),
            node("C2"), node("B2", "C2"), node("A2", "B2"),
        ])
        result = r.resolve()
        assert set(result) == {"A1", "B1", "C1", "A2", "B2", "C2"}

    def test_two_independent_chains_internal_order(self):
        r = DependencyResolver()
        r.add_many([
            node("C1"), node("B1", "C1"), node("A1", "B1"),
            node("C2"), node("B2", "C2"), node("A2", "B2"),
        ])
        result = r.resolve()
        assert result.index("C1") < result.index("B1") < result.index("A1")
        assert result.index("C2") < result.index("B2") < result.index("A2")

    def test_no_deps_nodes_can_appear_anywhere_relative_to_each_other(self):
        r = DependencyResolver()
        r.add_many([node("X"), node("Y"), node("Z")])
        result = r.resolve()
        assert set(result) == {"X", "Y", "Z"}

    def test_nodes_with_no_dependents_appear_last(self):
        # Roots (no one depends on them) should appear last in topo order
        r = DependencyResolver()
        r.add_many([node("B"), node("A", "B")])
        result = r.resolve()
        assert result[-1] == "A"

    def test_add_then_remove_then_resolve(self):
        r = DependencyResolver()
        r.add_many([node("A"), node("B", "A"), node("C", "B")])
        r.remove("C")
        result = r.resolve()
        assert set(result) == {"A", "B"}
        assert result.index("A") < result.index("B")
