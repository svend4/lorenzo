"""Budget tracker и cost guardrails для LLM-вызовов.

Использование:
    from docstoolkit.budget import BudgetTracker, BudgetRule

    bt = BudgetTracker()
    bt.set_rule(BudgetRule(scope="user:alice", period="day", limit_usd=1.0))

    # Перед вызовом:
    status = bt.check("user:alice")
    if not status.ok:
        raise BudgetExceeded(status.reason)

    # После вызова:
    bt.record(scope="user:alice", model="claude-haiku-4-5",
              tokens_in=100, tokens_out=50, cost=0.002)
"""
from docstoolkit.budget.tracker import (
    BudgetTracker, BudgetRule, BudgetStatus, UsageRecord, BudgetExceeded,
)

__all__ = [
    "BudgetTracker", "BudgetRule", "BudgetStatus",
    "UsageRecord", "BudgetExceeded",
]
