"""Query plan nodes and plan tree structures."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PlanNodeType(Enum):
    SCAN = "SCAN"
    FILTER = "FILTER"
    SORT = "SORT"
    LIMIT = "LIMIT"
    JOIN = "JOIN"
    PROJECT = "PROJECT"


@dataclass
class PlanNode:
    node_type: PlanNodeType
    cost: float = 0.0
    children: list["PlanNode"] = field(default_factory=list)
    params: dict = field(default_factory=dict)

    def total_cost(self) -> float:
        """Return self.cost plus the total_cost of all children recursively."""
        return self.cost + sum(child.total_cost() for child in self.children)

    def depth(self) -> int:
        """Return 1 for a leaf node, or 1 + max child depth for an internal node."""
        if not self.children:
            return 1
        return 1 + max(child.depth() for child in self.children)
