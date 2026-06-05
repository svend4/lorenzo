"""Query plan optimizer: rules and orchestrator."""
from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from docstoolkit.query_optimizer.plan import PlanNode, PlanNodeType


@dataclass
class QueryPlan:
    query: str
    root: PlanNode
    estimated_cost: float = 0.0
    optimized: bool = False


class OptimizationRule(ABC):
    """Abstract base class for a single optimization rule."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable rule name."""

    @abstractmethod
    def apply(self, plan: QueryPlan) -> QueryPlan:
        """Apply the rule to *plan* and return a (possibly new) QueryPlan."""


# ---------------------------------------------------------------------------
# Concrete rules
# ---------------------------------------------------------------------------

class PushDownFilters(OptimizationRule):
    """Move FILTER nodes closer to SCAN nodes.

    For each node whose children list contains a FILTER among non-FILTER
    siblings, re-order so that FILTER nodes appear *before* non-FILTER nodes.
    This is applied recursively bottom-up so that filters propagate all the
    way down the tree.
    """

    @property
    def name(self) -> str:
        return "PushDownFilters"

    def _reorder_children(self, node: PlanNode) -> None:
        """Recursively reorder children of *node* so FILTERs come first."""
        # Recurse into children first (bottom-up)
        for child in node.children:
            self._reorder_children(child)

        if not node.children:
            return

        filters = [c for c in node.children if c.node_type == PlanNodeType.FILTER]
        others = [c for c in node.children if c.node_type != PlanNodeType.FILTER]
        # Only reorder if there is at least one FILTER and at least one non-FILTER sibling
        if filters and others:
            node.children = filters + others

    def apply(self, plan: QueryPlan) -> QueryPlan:
        new_plan = copy.deepcopy(plan)
        self._reorder_children(new_plan.root)
        return new_plan


class EliminateRedundantSorts(OptimizationRule):
    """Remove SORT nodes that are direct children of another SORT with the same params."""

    @property
    def name(self) -> str:
        return "EliminateRedundantSorts"

    def _eliminate(self, node: PlanNode) -> None:
        """Recursively remove redundant SORT children."""
        i = 0
        while i < len(node.children):
            child = node.children[i]
            # If the current node is SORT and the child is also SORT with same params,
            # replace child with child's children (inline grandchildren).
            if (
                node.node_type == PlanNodeType.SORT
                and child.node_type == PlanNodeType.SORT
                and child.params == node.params
            ):
                # Replace child with its own children (may be empty list)
                node.children[i : i + 1] = child.children
                # Do NOT increment i: re-check position i (which is now the first
                # grandchild, if any) on the next iteration.
            else:
                self._eliminate(child)
                i += 1

    def apply(self, plan: QueryPlan) -> QueryPlan:
        new_plan = copy.deepcopy(plan)
        self._eliminate(new_plan.root)
        return new_plan


class LimitPushDown(OptimizationRule):
    """Push LIMIT nodes below SORT nodes.

    When a LIMIT node has a SORT node as its direct child, swap them so that
    the SORT sits above the LIMIT (i.e. LIMIT becomes child of SORT, and
    SORT becomes the node in the original LIMIT's position).
    """

    @property
    def name(self) -> str:
        return "LimitPushDown"

    def _push_down(self, node: PlanNode) -> PlanNode:
        """Return the (possibly replaced) node after pushing LIMITs down."""
        # Recurse into children first
        node.children = [self._push_down(c) for c in node.children]

        # If this node is LIMIT and its sole child is SORT, swap them.
        if (
            node.node_type == PlanNodeType.LIMIT
            and len(node.children) == 1
            and node.children[0].node_type == PlanNodeType.SORT
        ):
            sort_node = node.children[0]
            # LIMIT takes SORT's children
            node.children = sort_node.children
            # SORT's child becomes LIMIT
            sort_node.children = [node]
            # Return SORT (it now sits above LIMIT)
            return sort_node

        return node

    def apply(self, plan: QueryPlan) -> QueryPlan:
        new_plan = copy.deepcopy(plan)
        new_plan.root = self._push_down(new_plan.root)
        return new_plan


# ---------------------------------------------------------------------------
# Optimizer
# ---------------------------------------------------------------------------

class QueryOptimizer:
    """Applies a sequence of optimization rules to a QueryPlan."""

    def __init__(self, rules: list[OptimizationRule] | None = None) -> None:
        if rules is None:
            self._rules: list[OptimizationRule] = [
                PushDownFilters(),
                EliminateRedundantSorts(),
                LimitPushDown(),
            ]
        else:
            self._rules = list(rules)

    def add_rule(self, rule: OptimizationRule) -> None:
        """Append *rule* to the end of the rule list."""
        self._rules.append(rule)

    def optimize(self, plan: QueryPlan) -> QueryPlan:
        """Apply all rules in sequence, mark optimized=True, recalculate cost."""
        result = plan
        for rule in self._rules:
            result = rule.apply(result)
        result.optimized = True
        result.estimated_cost = result.root.total_cost()
        return result

    def explain(self, plan: QueryPlan) -> str:
        """Return an indented tree string representation of the plan."""
        lines: list[str] = []
        self._explain_node(plan.root, 0, lines)
        return "\n".join(lines)

    def _explain_node(self, node: PlanNode, indent: int, lines: list[str]) -> None:
        prefix = "  " * indent
        lines.append(f"{prefix}{node.node_type.value}(cost={node.cost})")
        for child in node.children:
            self._explain_node(child, indent + 1, lines)
