"""Query optimizer module: plan nodes, optimization rules, and cost estimation."""
from docstoolkit.query_optimizer.plan import PlanNode, PlanNodeType
from docstoolkit.query_optimizer.optimizer import (
    QueryPlan,
    OptimizationRule,
    PushDownFilters,
    EliminateRedundantSorts,
    LimitPushDown,
    QueryOptimizer,
)
from docstoolkit.query_optimizer.stats import TableStats, CostEstimator

__all__ = [
    # plan
    "PlanNode",
    "PlanNodeType",
    # optimizer
    "QueryPlan",
    "OptimizationRule",
    "PushDownFilters",
    "EliminateRedundantSorts",
    "LimitPushDown",
    "QueryOptimizer",
    # stats
    "TableStats",
    "CostEstimator",
]
