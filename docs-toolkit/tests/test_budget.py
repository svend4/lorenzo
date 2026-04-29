"""Тесты budget tracker."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.budget import (
    BudgetTracker, BudgetRule, BudgetStatus, UsageRecord, BudgetExceeded,
)


@pytest.fixture
def bt(tmp_path):
    t = BudgetTracker(db_path=tmp_path / "b.sqlite")
    yield t
    t.close()


def test_usage_record_auto_id_ts():
    r = UsageRecord(scope="user:x", cost=0.01)
    assert r.id and len(r.id) == 12
    assert r.ts


def test_set_and_get_rule(bt):
    bt.set_rule(BudgetRule(scope="user:a", period="day", limit_usd=0.5))
    rules = bt.get_rules("user:a")
    assert len(rules) == 1
    assert rules[0].limit_usd == 0.5
    assert rules[0].period == "day"


def test_get_rule_includes_global_wildcard(bt):
    bt.set_rule(BudgetRule(scope="*", period="day", limit_usd=10.0))
    rules = bt.get_rules("user:b")
    assert any(r.scope == "*" for r in rules)


def test_remove_rule(bt):
    bt.set_rule(BudgetRule(scope="x", period="day", limit_usd=1.0))
    bt.remove_rule("x", "day")
    assert bt.get_rules("x") == []


def test_record_increments_usage(bt):
    bt.record(scope="user:a", model="m", tokens_in=10, tokens_out=20, cost=0.01)
    bt.record(scope="user:a", model="m", tokens_in=5, tokens_out=15, cost=0.02)
    assert bt.used_in_period("user:a", "day") == pytest.approx(0.03)


def test_check_no_rules_returns_ok(bt):
    s = bt.check("user:nobody")
    assert s.state == "ok"
    assert s.ok


def test_check_warning_threshold(bt):
    bt.set_rule(BudgetRule(scope="u", period="day", limit_usd=1.0, warn_at=0.5))
    bt.record(scope="u", cost=0.6)
    s = bt.check("u")
    assert s.state == "warning"
    assert s.ok  # warning is still ok
    assert "60" in s.reason or "0.6" in s.reason


def test_check_blocked_when_over(bt):
    bt.set_rule(BudgetRule(scope="u", period="day", limit_usd=0.10))
    bt.record(scope="u", cost=0.15)
    s = bt.check("u")
    assert s.state == "blocked"
    assert not s.ok


def test_enforce_raises_on_block(bt):
    bt.set_rule(BudgetRule(scope="u", period="day", limit_usd=0.01))
    bt.record(scope="u", cost=0.05)
    with pytest.raises(BudgetExceeded):
        bt.enforce("u")


def test_enforce_returns_status_when_ok(bt):
    bt.set_rule(BudgetRule(scope="u", period="day", limit_usd=10.0))
    bt.record(scope="u", cost=0.01)
    s = bt.enforce("u")
    assert s.state == "ok"


def test_top_spenders(bt):
    bt.record(scope="user:a", cost=0.05)
    bt.record(scope="user:b", cost=0.10)
    bt.record(scope="user:c", cost=0.02)
    top = bt.top_spenders(period="day", limit=2)
    assert len(top) == 2
    assert top[0][0] == "user:b"
    assert top[0][1] == pytest.approx(0.10)


def test_per_model_breakdown(bt):
    bt.record(scope="x", model="haiku", tokens_in=10, tokens_out=5, cost=0.001)
    bt.record(scope="x", model="haiku", tokens_in=20, tokens_out=10, cost=0.002)
    bt.record(scope="x", model="opus", tokens_in=100, tokens_out=50, cost=0.05)
    bd = bt.per_model_breakdown(period="day")
    assert "haiku" in bd
    assert "opus" in bd
    assert bd["haiku"]["calls"] == 2
    assert bd["haiku"]["cost"] == pytest.approx(0.003)
    assert bd["opus"]["tokens_in"] == 100


def test_report_markdown_contains_sections(bt):
    bt.set_rule(BudgetRule(scope="u", period="day", limit_usd=1.0))
    bt.record(scope="u", model="haiku", cost=0.05)
    md = bt.report_markdown(period="day")
    assert "Budget report" in md
    assert "Top scopes" in md
    assert "haiku" in md
    assert "Active rules" in md


def test_report_markdown_empty(bt):
    md = bt.report_markdown(period="day")
    assert "пусто" in md or "_(empty)_" in md


def test_period_total_returns_all(bt):
    """Period 'total' игнорирует ts."""
    bt.set_rule(BudgetRule(scope="u", period="total", limit_usd=1.0))
    bt.record(scope="u", cost=0.5, model="m")
    s = bt.check("u")
    assert s.used_usd == pytest.approx(0.5)


def test_worst_state_picked_among_rules(bt):
    """Если несколько правил — берётся худшее."""
    bt.set_rule(BudgetRule(scope="u", period="day", limit_usd=10.0))   # ok
    bt.set_rule(BudgetRule(scope="u", period="month", limit_usd=0.01))  # blocked
    bt.record(scope="u", cost=0.05)
    s = bt.check("u")
    assert s.state == "blocked"
