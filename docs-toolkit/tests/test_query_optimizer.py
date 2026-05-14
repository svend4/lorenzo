"""Tests for the query_optimizer module (E67).

Coverage targets:
- PlanNode: total_cost, depth
- QueryPlan fields
- PushDownFilters rule
- EliminateRedundantSorts rule
- LimitPushDown rule
- QueryOptimizer: optimize, explain, add_rule
- CostEstimator: all four estimate methods
- Edge cases
"""
from __future__ import annotations

import math
import pytest

from docstoolkit.query_optimizer import (
    PlanNode,
    PlanNodeType,
    QueryPlan,
    OptimizationRule,
    PushDownFilters,
    EliminateRedundantSorts,
    LimitPushDown,
    QueryOptimizer,
    TableStats,
    CostEstimator,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_node(
    node_type: PlanNodeType,
    cost: float = 0.0,
    children: list[PlanNode] | None = None,
    params: dict | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        cost=cost,
        children=children or [],
        params=params or {},
    )


def scan(cost: float = 1.0, children=None, **params) -> PlanNode:
    return make_node(PlanNodeType.SCAN, cost, children=children, params=dict(params))


def filter_node(cost: float = 0.5, children=None, **params) -> PlanNode:
    return make_node(PlanNodeType.FILTER, cost, children=children, params=dict(params))


def sort_node(cost: float = 0.3, children=None, **params) -> PlanNode:
    return make_node(PlanNodeType.SORT, cost, children=children, params=dict(params))


def limit_node(cost: float = 0.1, children=None) -> PlanNode:
    return make_node(PlanNodeType.LIMIT, cost, children=children)


def project_node(cost: float = 0.2, children=None) -> PlanNode:
    return make_node(PlanNodeType.PROJECT, cost, children=children)


def join_node(cost: float = 2.0, children=None) -> PlanNode:
    return make_node(PlanNodeType.JOIN, cost, children=children)


def make_plan(root: PlanNode, query: str = "SELECT *") -> QueryPlan:
    return QueryPlan(query=query, root=root)


# ===========================================================================
# 1. PlanNodeType enum
# ===========================================================================

class TestPlanNodeType:
    def test_scan_member(self):
        assert PlanNodeType.SCAN.value == "SCAN"

    def test_filter_member(self):
        assert PlanNodeType.FILTER.value == "FILTER"

    def test_sort_member(self):
        assert PlanNodeType.SORT.value == "SORT"

    def test_limit_member(self):
        assert PlanNodeType.LIMIT.value == "LIMIT"

    def test_join_member(self):
        assert PlanNodeType.JOIN.value == "JOIN"

    def test_project_member(self):
        assert PlanNodeType.PROJECT.value == "PROJECT"

    def test_enum_count(self):
        assert len(PlanNodeType) == 6


# ===========================================================================
# 2. PlanNode basics
# ===========================================================================

class TestPlanNodeFields:
    def test_default_cost_zero(self):
        node = PlanNode(node_type=PlanNodeType.SCAN)
        assert node.cost == 0.0

    def test_default_children_empty(self):
        node = PlanNode(node_type=PlanNodeType.SCAN)
        assert node.children == []

    def test_default_params_empty(self):
        node = PlanNode(node_type=PlanNodeType.SCAN)
        assert node.params == {}

    def test_children_not_shared(self):
        # Default factory must create separate list per instance
        a = PlanNode(node_type=PlanNodeType.SCAN)
        b = PlanNode(node_type=PlanNodeType.SCAN)
        a.children.append(PlanNode(node_type=PlanNodeType.FILTER))
        assert b.children == []

    def test_params_not_shared(self):
        a = PlanNode(node_type=PlanNodeType.SCAN)
        b = PlanNode(node_type=PlanNodeType.SCAN)
        a.params["key"] = "value"
        assert "key" not in b.params


# ===========================================================================
# 3. PlanNode.total_cost()
# ===========================================================================

class TestPlanNodeTotalCost:
    def test_leaf_total_cost(self):
        node = scan(cost=3.0)
        assert node.total_cost() == 3.0

    def test_single_child_total_cost(self):
        child = scan(cost=2.0)
        parent = make_node(PlanNodeType.FILTER, cost=1.0, children=[child])
        assert parent.total_cost() == 3.0

    def test_two_children_total_cost(self):
        c1 = scan(cost=1.0)
        c2 = filter_node(cost=0.5)
        parent = join_node(cost=2.0, children=[c1, c2])
        assert parent.total_cost() == 3.5

    def test_three_level_tree(self):
        leaf = scan(cost=1.0)
        mid = filter_node(cost=0.5, children=[leaf])
        # mid.total_cost() should be 1.5
        root = sort_node(cost=0.3, children=[mid])
        assert root.total_cost() == pytest.approx(1.8)

    def test_zero_costs(self):
        child = PlanNode(PlanNodeType.SCAN, cost=0.0)
        root = PlanNode(PlanNodeType.FILTER, cost=0.0, children=[child])
        assert root.total_cost() == 0.0

    def test_multiple_branches(self):
        # root has two children each with one child
        ll = scan(cost=1.0)
        rl = scan(cost=2.0)
        left = filter_node(cost=0.5, children=[ll])   # 1.5
        right = filter_node(cost=0.5, children=[rl])  # 2.5
        root = join_node(cost=3.0, children=[left, right])
        assert root.total_cost() == pytest.approx(7.0)


# ===========================================================================
# 4. PlanNode.depth()
# ===========================================================================

class TestPlanNodeDepth:
    def test_leaf_depth_is_one(self):
        node = scan()
        assert node.depth() == 1

    def test_one_child_depth_two(self):
        child = scan()
        parent = make_node(PlanNodeType.FILTER, children=[child])
        assert parent.depth() == 2

    def test_two_level_chain(self):
        leaf = scan()
        mid = filter_node(children=[leaf])
        root = sort_node(children=[mid])
        assert root.depth() == 3

    def test_unbalanced_tree_takes_max(self):
        deep_leaf = scan()
        deep_mid = filter_node(children=[deep_leaf])  # depth=2
        shallow_leaf = scan()                          # depth=1
        root = join_node(children=[deep_mid, shallow_leaf])
        assert root.depth() == 3

    def test_wide_tree_all_leaves(self):
        leaves = [scan() for _ in range(5)]
        root = join_node(children=leaves)
        assert root.depth() == 2

    def test_empty_children_list_is_leaf(self):
        node = PlanNode(PlanNodeType.FILTER, children=[])
        assert node.depth() == 1


# ===========================================================================
# 5. QueryPlan fields
# ===========================================================================

class TestQueryPlan:
    def test_query_stored(self):
        plan = make_plan(scan(), query="SELECT id FROM t")
        assert plan.query == "SELECT id FROM t"

    def test_root_stored(self):
        root = scan(cost=5.0)
        plan = make_plan(root)
        assert plan.root is root

    def test_default_estimated_cost(self):
        plan = make_plan(scan())
        assert plan.estimated_cost == 0.0

    def test_default_optimized_false(self):
        plan = make_plan(scan())
        assert plan.optimized is False

    def test_custom_estimated_cost(self):
        plan = QueryPlan(query="q", root=scan(), estimated_cost=42.0)
        assert plan.estimated_cost == 42.0

    def test_custom_optimized_true(self):
        plan = QueryPlan(query="q", root=scan(), optimized=True)
        assert plan.optimized is True


# ===========================================================================
# 6. PushDownFilters rule
# ===========================================================================

class TestPushDownFilters:
    def setup_method(self):
        self.rule = PushDownFilters()

    def test_name(self):
        assert self.rule.name == "PushDownFilters"

    def test_no_children_unchanged(self):
        root = scan()
        plan = make_plan(root)
        result = self.rule.apply(plan)
        assert result.root.node_type == PlanNodeType.SCAN
        assert result.root.children == []

    def test_filter_moves_before_non_filter(self):
        # root -> [sort, filter]  => root -> [filter, sort]
        s = sort_node(cost=0.3)
        f = filter_node(cost=0.5)
        root = join_node(cost=2.0, children=[s, f])
        plan = make_plan(root)
        result = self.rule.apply(plan)
        children = result.root.children
        assert children[0].node_type == PlanNodeType.FILTER
        assert children[1].node_type == PlanNodeType.SORT

    def test_filter_already_first_unchanged(self):
        f = filter_node(cost=0.5)
        s = sort_node(cost=0.3)
        root = join_node(cost=2.0, children=[f, s])
        plan = make_plan(root)
        result = self.rule.apply(plan)
        children = result.root.children
        assert children[0].node_type == PlanNodeType.FILTER
        assert children[1].node_type == PlanNodeType.SORT

    def test_only_filters_order_preserved(self):
        f1 = filter_node(cost=0.5)
        f2 = filter_node(cost=0.6)
        root = join_node(children=[f1, f2])
        plan = make_plan(root)
        result = self.rule.apply(plan)
        assert all(c.node_type == PlanNodeType.FILTER for c in result.root.children)

    def test_only_non_filters_order_preserved(self):
        s = sort_node()
        pr = project_node()
        root = join_node(children=[s, pr])
        plan = make_plan(root)
        result = self.rule.apply(plan)
        assert result.root.children[0].node_type == PlanNodeType.SORT
        assert result.root.children[1].node_type == PlanNodeType.PROJECT

    def test_original_plan_not_mutated(self):
        s = sort_node()
        f = filter_node()
        root = join_node(children=[s, f])
        plan = make_plan(root)
        _ = self.rule.apply(plan)
        # Original plan children order should be unchanged
        assert plan.root.children[0].node_type == PlanNodeType.SORT
        assert plan.root.children[1].node_type == PlanNodeType.FILTER

    def test_recursive_push_down(self):
        # Root -> [sort_node containing [scan, filter]]
        inner_scan = scan()
        inner_filter = filter_node()
        sort = sort_node(children=[inner_scan, inner_filter])
        root = project_node(children=[sort])
        plan = make_plan(root)
        result = self.rule.apply(plan)
        inner_children = result.root.children[0].children
        assert inner_children[0].node_type == PlanNodeType.FILTER
        assert inner_children[1].node_type == PlanNodeType.SCAN

    def test_multiple_filters_before_multiple_non_filters(self):
        f1 = filter_node(cost=0.1)
        f2 = filter_node(cost=0.2)
        s1 = sort_node(cost=0.3)
        s2 = scan(cost=0.4)
        root = join_node(children=[s1, f1, s2, f2])
        plan = make_plan(root)
        result = self.rule.apply(plan)
        children = result.root.children
        types = [c.node_type for c in children]
        assert types[:2] == [PlanNodeType.FILTER, PlanNodeType.FILTER]
        assert set(types[2:]) == {PlanNodeType.SORT, PlanNodeType.SCAN}


# ===========================================================================
# 7. EliminateRedundantSorts rule
# ===========================================================================

class TestEliminateRedundantSorts:
    def setup_method(self):
        self.rule = EliminateRedundantSorts()

    def test_name(self):
        assert self.rule.name == "EliminateRedundantSorts"

    def test_double_sort_same_params_collapsed(self):
        inner_sort = sort_node(cost=0.3, children=[scan()], col="name")
        outer_sort = sort_node(cost=0.3, children=[inner_sort], col="name")
        plan = make_plan(outer_sort)
        result = self.rule.apply(plan)
        # outer_sort should now have scan() as its child, not inner_sort
        assert result.root.node_type == PlanNodeType.SORT
        assert len(result.root.children) == 1
        assert result.root.children[0].node_type == PlanNodeType.SCAN

    def test_different_params_not_collapsed(self):
        inner_sort = sort_node(cost=0.3, children=[scan()], col="age")
        outer_sort = sort_node(cost=0.3, children=[inner_sort], col="name")
        plan = make_plan(outer_sort)
        result = self.rule.apply(plan)
        # inner_sort should still be there
        assert result.root.children[0].node_type == PlanNodeType.SORT

    def test_non_sort_child_not_affected(self):
        f = filter_node(cost=0.5, children=[scan()])
        s = sort_node(cost=0.3, children=[f])
        plan = make_plan(s)
        result = self.rule.apply(plan)
        assert result.root.children[0].node_type == PlanNodeType.FILTER

    def test_no_sort_tree_unchanged(self):
        root = join_node(children=[scan(), filter_node()])
        plan = make_plan(root)
        result = self.rule.apply(plan)
        assert result.root.node_type == PlanNodeType.JOIN
        assert len(result.root.children) == 2

    def test_original_plan_not_mutated(self):
        inner_sort = sort_node(children=[scan()], col="x")
        outer_sort = sort_node(children=[inner_sort], col="x")
        plan = make_plan(outer_sort)
        _ = self.rule.apply(plan)
        assert plan.root.children[0].node_type == PlanNodeType.SORT

    def test_triple_sort_same_params(self):
        leaf_sort = sort_node(cost=0.1, children=[scan()], col="x")
        mid_sort = sort_node(cost=0.2, children=[leaf_sort], col="x")
        outer_sort = sort_node(cost=0.3, children=[mid_sort], col="x")
        plan = make_plan(outer_sort)
        result = self.rule.apply(plan)
        # All intermediate SORT(col=x) nodes should be eliminated,
        # leaving outer_sort -> scan
        assert result.root.node_type == PlanNodeType.SORT
        assert result.root.children[0].node_type == PlanNodeType.SCAN

    def test_sort_with_empty_params_match(self):
        inner = sort_node(children=[scan()])
        outer = sort_node(children=[inner])
        plan = make_plan(outer)
        result = self.rule.apply(plan)
        assert result.root.children[0].node_type == PlanNodeType.SCAN


# ===========================================================================
# 8. LimitPushDown rule
# ===========================================================================

class TestLimitPushDown:
    def setup_method(self):
        self.rule = LimitPushDown()

    def test_name(self):
        assert self.rule.name == "LimitPushDown"

    def test_limit_over_sort_swapped(self):
        s = sort_node(children=[scan()])
        lim = limit_node(children=[s])
        plan = make_plan(lim)
        result = self.rule.apply(plan)
        # Root should now be SORT
        assert result.root.node_type == PlanNodeType.SORT
        # SORT's child should be LIMIT
        assert result.root.children[0].node_type == PlanNodeType.LIMIT
        # LIMIT's child should be the original SCAN
        assert result.root.children[0].children[0].node_type == PlanNodeType.SCAN

    def test_no_sort_child_unchanged(self):
        f = filter_node(children=[scan()])
        lim = limit_node(children=[f])
        plan = make_plan(lim)
        result = self.rule.apply(plan)
        assert result.root.node_type == PlanNodeType.LIMIT
        assert result.root.children[0].node_type == PlanNodeType.FILTER

    def test_sort_not_direct_child_of_limit_unchanged(self):
        # LIMIT -> FILTER -> SORT  (SORT is not direct child of LIMIT)
        s = sort_node(children=[scan()])
        f = filter_node(children=[s])
        lim = limit_node(children=[f])
        plan = make_plan(lim)
        result = self.rule.apply(plan)
        assert result.root.node_type == PlanNodeType.LIMIT
        assert result.root.children[0].node_type == PlanNodeType.FILTER

    def test_original_plan_not_mutated(self):
        s = sort_node(children=[scan()])
        lim = limit_node(children=[s])
        plan = make_plan(lim)
        _ = self.rule.apply(plan)
        assert plan.root.node_type == PlanNodeType.LIMIT

    def test_scan_unchanged(self):
        plan = make_plan(scan())
        result = self.rule.apply(plan)
        assert result.root.node_type == PlanNodeType.SCAN

    def test_cost_preserved_after_swap(self):
        s = sort_node(cost=2.0, children=[scan(cost=1.0)])
        lim = limit_node(cost=0.5, children=[s])
        plan = make_plan(lim)
        result = self.rule.apply(plan)
        assert result.root.cost == 2.0          # was sort
        assert result.root.children[0].cost == 0.5  # was limit

    def test_recursive_limit_push_down(self):
        # Nested: LIMIT -> SORT -> LIMIT -> SORT -> SCAN
        inner_scan = scan()
        inner_sort = sort_node(children=[inner_scan])
        inner_limit = limit_node(children=[inner_sort])
        outer_sort = sort_node(children=[inner_limit])
        outer_limit = limit_node(children=[outer_sort])
        plan = make_plan(outer_limit)
        result = self.rule.apply(plan)
        # After push-down the outermost node should be SORT
        assert result.root.node_type == PlanNodeType.SORT


# ===========================================================================
# 9. QueryOptimizer
# ===========================================================================

class TestQueryOptimizer:
    def test_default_rules_applied(self):
        # A plan where all three default rules are applicable
        inner_sort = sort_node(children=[scan()], col="x")
        outer_sort = sort_node(children=[inner_sort], col="x")
        plan = make_plan(outer_sort)
        optimizer = QueryOptimizer()
        result = optimizer.optimize(plan)
        assert result.optimized is True

    def test_optimize_sets_optimized_flag(self):
        plan = make_plan(scan())
        optimizer = QueryOptimizer()
        result = optimizer.optimize(plan)
        assert result.optimized is True

    def test_optimize_recalculates_estimated_cost(self):
        root = scan(cost=3.0)
        plan = make_plan(root)
        optimizer = QueryOptimizer()
        result = optimizer.optimize(plan)
        assert result.estimated_cost == pytest.approx(3.0)

    def test_optimize_with_tree_cost(self):
        child = scan(cost=2.0)
        root = filter_node(cost=1.0, children=[child])
        plan = make_plan(root)
        optimizer = QueryOptimizer()
        result = optimizer.optimize(plan)
        assert result.estimated_cost == pytest.approx(3.0)

    def test_optimize_does_not_mutate_original(self):
        plan = make_plan(scan(cost=5.0))
        optimizer = QueryOptimizer()
        _ = optimizer.optimize(plan)
        assert plan.optimized is False

    def test_add_rule_appended(self):
        optimizer = QueryOptimizer(rules=[])
        assert len(optimizer._rules) == 0
        optimizer.add_rule(PushDownFilters())
        assert len(optimizer._rules) == 1

    def test_add_rule_applied_in_optimize(self):
        class CountingRule(OptimizationRule):
            def __init__(self):
                self.called = False

            @property
            def name(self):
                return "CountingRule"

            def apply(self, plan):
                self.called = True
                return plan

        optimizer = QueryOptimizer(rules=[])
        rule = CountingRule()
        optimizer.add_rule(rule)
        optimizer.optimize(make_plan(scan()))
        assert rule.called is True

    def test_empty_rules_list(self):
        optimizer = QueryOptimizer(rules=[])
        plan = make_plan(scan(cost=7.0))
        result = optimizer.optimize(plan)
        assert result.optimized is True
        assert result.estimated_cost == pytest.approx(7.0)

    def test_explain_single_node(self):
        optimizer = QueryOptimizer()
        plan = make_plan(scan(cost=1.0))
        output = optimizer.explain(plan)
        assert "SCAN" in output
        assert "cost=1.0" in output

    def test_explain_two_levels(self):
        child = scan(cost=1.0)
        root = filter_node(cost=0.5, children=[child])
        optimizer = QueryOptimizer()
        plan = make_plan(root)
        output = optimizer.explain(plan)
        lines = output.splitlines()
        assert len(lines) == 2
        assert lines[0].startswith("FILTER")
        assert lines[1].startswith("  SCAN")

    def test_explain_three_levels(self):
        leaf = scan(cost=1.0)
        mid = filter_node(cost=0.5, children=[leaf])
        root = sort_node(cost=0.3, children=[mid])
        optimizer = QueryOptimizer()
        plan = make_plan(root)
        output = optimizer.explain(plan)
        lines = output.splitlines()
        assert len(lines) == 3
        assert lines[0].startswith("SORT")
        assert lines[1].startswith("  FILTER")
        assert lines[2].startswith("    SCAN")

    def test_explain_format_cost(self):
        optimizer = QueryOptimizer()
        plan = make_plan(scan(cost=2.5))
        output = optimizer.explain(plan)
        assert "cost=2.5" in output

    def test_custom_rules_only(self):
        optimizer = QueryOptimizer(rules=[PushDownFilters()])
        assert len(optimizer._rules) == 1
        assert isinstance(optimizer._rules[0], PushDownFilters)

    def test_default_has_three_rules(self):
        optimizer = QueryOptimizer()
        assert len(optimizer._rules) == 3


# ===========================================================================
# 10. TableStats
# ===========================================================================

class TestTableStats:
    def test_table_name(self):
        ts = TableStats(table_name="users", row_count=1000)
        assert ts.table_name == "users"

    def test_row_count(self):
        ts = TableStats(table_name="orders", row_count=5000)
        assert ts.row_count == 5000

    def test_default_avg_row_size(self):
        ts = TableStats(table_name="x", row_count=100)
        assert ts.avg_row_size == 100

    def test_custom_avg_row_size(self):
        ts = TableStats(table_name="x", row_count=100, avg_row_size=200)
        assert ts.avg_row_size == 200


# ===========================================================================
# 11. CostEstimator
# ===========================================================================

class TestCostEstimator:
    def _estimator_with_table(
        self, table: str = "t", row_count: int = 1000, avg_row_size: int = 100
    ) -> CostEstimator:
        ts = TableStats(table_name=table, row_count=row_count, avg_row_size=avg_row_size)
        return CostEstimator(stats={table: ts})

    def test_estimate_scan_known_table(self):
        est = self._estimator_with_table("users", 1000, 100)
        assert est.estimate_scan("users") == pytest.approx(100.0)

    def test_estimate_scan_unknown_table(self):
        est = CostEstimator()
        assert est.estimate_scan("unknown") == pytest.approx(1.0)

    def test_estimate_scan_zero_rows(self):
        est = self._estimator_with_table("t", 0, 100)
        assert est.estimate_scan("t") == pytest.approx(0.0)

    def test_estimate_scan_custom_row_size(self):
        est = self._estimator_with_table("t", 500, 200)
        # 500 * 200 / 1000 = 100.0
        assert est.estimate_scan("t") == pytest.approx(100.0)

    def test_estimate_scan_no_stats_dict(self):
        est = CostEstimator(stats=None)
        assert est.estimate_scan("anything") == pytest.approx(1.0)

    def test_estimate_filter_zero_selectivity(self):
        est = CostEstimator()
        assert est.estimate_filter(0.0) == pytest.approx(0.0)

    def test_estimate_filter_full_selectivity(self):
        est = CostEstimator()
        assert est.estimate_filter(1.0) == pytest.approx(10.0)

    def test_estimate_filter_half_selectivity(self):
        est = CostEstimator()
        assert est.estimate_filter(0.5) == pytest.approx(5.0)

    def test_estimate_filter_small_selectivity(self):
        est = CostEstimator()
        assert est.estimate_filter(0.1) == pytest.approx(1.0)

    def test_estimate_sort_small(self):
        est = CostEstimator()
        # 10 * log2(11) / 1000
        expected = 10 * math.log2(11) / 1000
        assert est.estimate_sort(10) == pytest.approx(expected)

    def test_estimate_sort_zero_rows(self):
        est = CostEstimator()
        # 0 * log2(1) / 1000 = 0
        assert est.estimate_sort(0) == pytest.approx(0.0)

    def test_estimate_sort_one_row(self):
        est = CostEstimator()
        expected = 1 * math.log2(2) / 1000
        assert est.estimate_sort(1) == pytest.approx(expected)

    def test_estimate_sort_large(self):
        est = CostEstimator()
        expected = 1000 * math.log2(1001) / 1000
        assert est.estimate_sort(1000) == pytest.approx(expected)

    def test_estimate_join_basic(self):
        est = CostEstimator()
        # 100 * 200 / 1000 = 20.0
        assert est.estimate_join(100, 200) == pytest.approx(20.0)

    def test_estimate_join_zero_left(self):
        est = CostEstimator()
        assert est.estimate_join(0, 500) == pytest.approx(0.0)

    def test_estimate_join_zero_right(self):
        est = CostEstimator()
        assert est.estimate_join(500, 0) == pytest.approx(0.0)

    def test_estimate_join_equal_sides(self):
        est = CostEstimator()
        # 1000 * 1000 / 1000 = 1000.0
        assert est.estimate_join(1000, 1000) == pytest.approx(1000.0)

    def test_estimate_join_asymmetric(self):
        est = CostEstimator()
        assert est.estimate_join(10, 10000) == est.estimate_join(10000, 10)


# ===========================================================================
# 12. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_single_scan_node_total_cost(self):
        node = scan(cost=0.0)
        assert node.total_cost() == 0.0

    def test_deeply_nested_depth(self):
        node = scan()
        for _ in range(9):
            node = filter_node(children=[node])
        assert node.depth() == 10

    def test_plan_with_no_applicable_rules(self):
        # A plain SCAN — none of the three default rules change anything
        plan = make_plan(scan(cost=5.0))
        optimizer = QueryOptimizer()
        result = optimizer.optimize(plan)
        assert result.optimized is True
        assert result.root.node_type == PlanNodeType.SCAN
        assert result.estimated_cost == pytest.approx(5.0)

    def test_push_down_filters_idempotent(self):
        f = filter_node()
        s = sort_node()
        root = join_node(children=[f, s])
        plan = make_plan(root)
        rule = PushDownFilters()
        result1 = rule.apply(plan)
        result2 = rule.apply(result1)
        assert result1.root.children[0].node_type == result2.root.children[0].node_type

    def test_eliminate_sorts_idempotent(self):
        inner = sort_node(children=[scan()], col="x")
        outer = sort_node(children=[inner], col="x")
        plan = make_plan(outer)
        rule = EliminateRedundantSorts()
        result1 = rule.apply(plan)
        result2 = rule.apply(result1)
        # second pass should not change anything further
        assert result1.root.children[0].node_type == result2.root.children[0].node_type

    def test_limit_push_down_idempotent(self):
        s = sort_node(children=[scan()])
        lim = limit_node(children=[s])
        plan = make_plan(lim)
        rule = LimitPushDown()
        result1 = rule.apply(plan)
        result2 = rule.apply(result1)
        # After first apply, root is SORT; second apply won't swap again
        assert result1.root.node_type == result2.root.node_type

    def test_empty_optimizer_rule_list_returns_plan_optimized(self):
        optimizer = QueryOptimizer(rules=[])
        plan = make_plan(scan())
        result = optimizer.optimize(plan)
        assert result.optimized is True

    def test_optimizer_explain_empty_children(self):
        optimizer = QueryOptimizer()
        plan = make_plan(scan(cost=0.0))
        output = optimizer.explain(plan)
        assert output == "SCAN(cost=0.0)"

    def test_plan_node_type_is_plan_node_type_enum(self):
        node = scan()
        assert isinstance(node.node_type, PlanNodeType)

    def test_large_tree_total_cost(self):
        leaves = [scan(cost=1.0) for _ in range(10)]
        root = join_node(cost=0.0, children=leaves)
        assert root.total_cost() == pytest.approx(10.0)
