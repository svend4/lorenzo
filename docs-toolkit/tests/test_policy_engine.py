"""Tests for the E44 policy engine module (65+ test cases)."""
from __future__ import annotations

import pytest

from docstoolkit.policy_engine import (
    Condition,
    Policy,
    PolicyDecision,
    PolicyEngine,
    PolicyRule,
    RuleEffect,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_rule(
    name: str = "r",
    conditions: list[Condition] | None = None,
    effect: RuleEffect = RuleEffect.ALLOW,
    priority: int = 0,
    description: str = "",
) -> PolicyRule:
    return PolicyRule(
        name=name,
        conditions=conditions or [],
        effect=effect,
        priority=priority,
        description=description,
    )


# ===========================================================================
# RuleEffect
# ===========================================================================


class TestRuleEffect:
    def test_values(self):
        assert RuleEffect.ALLOW.value == "allow"
        assert RuleEffect.DENY.value == "deny"
        assert RuleEffect.AUDIT.value == "audit"

    def test_enum_members(self):
        members = {e.name for e in RuleEffect}
        assert members == {"ALLOW", "DENY", "AUDIT"}


# ===========================================================================
# Condition — operator coverage
# ===========================================================================


class TestConditionEq:
    def test_eq_true(self):
        assert Condition("role", "eq", "admin").evaluate({"role": "admin"})

    def test_eq_false(self):
        assert not Condition("role", "eq", "admin").evaluate({"role": "user"})

    def test_eq_integer(self):
        assert Condition("level", "eq", 5).evaluate({"level": 5})


class TestConditionNe:
    def test_ne_true(self):
        assert Condition("role", "ne", "guest").evaluate({"role": "admin"})

    def test_ne_false(self):
        assert not Condition("role", "ne", "admin").evaluate({"role": "admin"})


class TestConditionGt:
    def test_gt_true(self):
        assert Condition("age", "gt", 18).evaluate({"age": 25})

    def test_gt_false_equal(self):
        assert not Condition("age", "gt", 25).evaluate({"age": 25})

    def test_gt_false_less(self):
        assert not Condition("age", "gt", 30).evaluate({"age": 25})


class TestConditionLt:
    def test_lt_true(self):
        assert Condition("age", "lt", 30).evaluate({"age": 25})

    def test_lt_false_equal(self):
        assert not Condition("age", "lt", 25).evaluate({"age": 25})

    def test_lt_false_greater(self):
        assert not Condition("age", "lt", 20).evaluate({"age": 25})


class TestConditionGte:
    def test_gte_equal(self):
        assert Condition("score", "gte", 100).evaluate({"score": 100})

    def test_gte_greater(self):
        assert Condition("score", "gte", 99).evaluate({"score": 100})

    def test_gte_false(self):
        assert not Condition("score", "gte", 101).evaluate({"score": 100})


class TestConditionLte:
    def test_lte_equal(self):
        assert Condition("score", "lte", 100).evaluate({"score": 100})

    def test_lte_less(self):
        assert Condition("score", "lte", 101).evaluate({"score": 100})

    def test_lte_false(self):
        assert not Condition("score", "lte", 99).evaluate({"score": 100})


class TestConditionIn:
    def test_in_true(self):
        assert Condition("role", "in", ["admin", "editor"]).evaluate({"role": "admin"})

    def test_in_false(self):
        assert not Condition("role", "in", ["admin", "editor"]).evaluate({"role": "viewer"})

    def test_in_empty_list(self):
        assert not Condition("role", "in", []).evaluate({"role": "admin"})


class TestConditionContains:
    def test_contains_string_true(self):
        assert Condition("email", "contains", "@example.com").evaluate({"email": "alice@example.com"})

    def test_contains_string_false(self):
        assert not Condition("email", "contains", "@other.com").evaluate({"email": "alice@example.com"})

    def test_contains_list_true(self):
        assert Condition("tags", "contains", "urgent").evaluate({"tags": ["urgent", "review"]})

    def test_contains_list_false(self):
        assert not Condition("tags", "contains", "resolved").evaluate({"tags": ["urgent", "review"]})


class TestConditionStartswith:
    def test_startswith_true(self):
        assert Condition("path", "startswith", "/api/").evaluate({"path": "/api/v1/users"})

    def test_startswith_false(self):
        assert not Condition("path", "startswith", "/admin/").evaluate({"path": "/api/v1/users"})

    def test_startswith_empty_prefix(self):
        assert Condition("path", "startswith", "").evaluate({"path": "/api/v1"})


# ===========================================================================
# Condition — dot-notation field access
# ===========================================================================


class TestConditionDotNotation:
    CTX = {"user": {"role": "admin", "profile": {"age": 30}}, "action": "delete"}

    def test_one_level_deep(self):
        assert Condition("action", "eq", "delete").evaluate(self.CTX)

    def test_two_levels_deep(self):
        assert Condition("user.role", "eq", "admin").evaluate(self.CTX)

    def test_three_levels_deep(self):
        assert Condition("user.profile.age", "eq", 30).evaluate(self.CTX)

    def test_missing_top_level_key_returns_false(self):
        assert not Condition("missing", "eq", "x").evaluate(self.CTX)

    def test_missing_nested_key_returns_false(self):
        assert not Condition("user.nonexistent", "eq", "x").evaluate(self.CTX)

    def test_missing_deep_nested_returns_false(self):
        assert not Condition("user.profile.weight", "eq", 70).evaluate(self.CTX)

    def test_intermediate_not_dict_returns_false(self):
        ctx = {"user": "string_value"}
        assert not Condition("user.role", "eq", "admin").evaluate(ctx)


# ===========================================================================
# Condition — invalid operator
# ===========================================================================


class TestConditionInvalidOperator:
    def test_raises_on_bad_operator(self):
        with pytest.raises(ValueError, match="Unknown operator"):
            Condition("x", "regex", ".*")

    def test_raises_on_empty_operator(self):
        with pytest.raises(ValueError):
            Condition("x", "", "v")


# ===========================================================================
# PolicyRule
# ===========================================================================


class TestPolicyRuleId:
    def test_auto_rule_id_length(self):
        rule = make_rule()
        assert len(rule.rule_id) == 8

    def test_auto_rule_id_hex(self):
        rule = make_rule()
        int(rule.rule_id, 16)  # must not raise

    def test_unique_ids(self):
        ids = {make_rule().rule_id for _ in range(50)}
        assert len(ids) == 50

    def test_custom_rule_id(self):
        rule = PolicyRule(
            name="x",
            conditions=[],
            effect=RuleEffect.ALLOW,
            rule_id="custom01",
        )
        assert rule.rule_id == "custom01"


class TestPolicyRuleMatches:
    def test_no_conditions_always_matches(self):
        rule = make_rule(conditions=[])
        assert rule.matches({"anything": True})

    def test_single_condition_match(self):
        rule = make_rule(conditions=[Condition("role", "eq", "admin")])
        assert rule.matches({"role": "admin"})

    def test_single_condition_no_match(self):
        rule = make_rule(conditions=[Condition("role", "eq", "admin")])
        assert not rule.matches({"role": "user"})

    def test_all_conditions_must_match(self):
        rule = make_rule(conditions=[
            Condition("role", "eq", "admin"),
            Condition("action", "eq", "delete"),
        ])
        assert rule.matches({"role": "admin", "action": "delete"})

    def test_partial_conditions_no_match(self):
        rule = make_rule(conditions=[
            Condition("role", "eq", "admin"),
            Condition("action", "eq", "delete"),
        ])
        assert not rule.matches({"role": "admin", "action": "read"})

    def test_empty_context_no_match(self):
        rule = make_rule(conditions=[Condition("role", "eq", "admin")])
        assert not rule.matches({})


class TestPolicyRuleToDict:
    def test_to_dict_keys(self):
        rule = make_rule(
            name="test-rule",
            conditions=[Condition("role", "eq", "admin")],
            effect=RuleEffect.DENY,
            priority=5,
            description="desc",
        )
        d = rule.to_dict()
        assert d["name"] == "test-rule"
        assert d["effect"] == "deny"
        assert d["priority"] == 5
        assert d["description"] == "desc"
        assert len(d["conditions"]) == 1
        assert d["conditions"][0] == {"field": "role", "operator": "eq", "value": "admin"}
        assert "rule_id" in d

    def test_to_dict_empty_conditions(self):
        rule = make_rule()
        assert rule.to_dict()["conditions"] == []


# ===========================================================================
# PolicyDecision
# ===========================================================================


class TestPolicyDecision:
    def test_is_allowed_true(self):
        d = PolicyDecision(
            effect=RuleEffect.ALLOW, rule_id="r1", rule_name="n", context={}
        )
        assert d.is_allowed()
        assert not d.is_denied()

    def test_is_denied_true(self):
        d = PolicyDecision(
            effect=RuleEffect.DENY, rule_id="r1", rule_name="n", context={}
        )
        assert d.is_denied()
        assert not d.is_allowed()

    def test_audit_is_neither_allowed_nor_denied(self):
        d = PolicyDecision(
            effect=RuleEffect.AUDIT, rule_id=None, rule_name=None, context={}
        )
        assert not d.is_allowed()
        assert not d.is_denied()

    def test_default_reason(self):
        d = PolicyDecision(effect=RuleEffect.ALLOW, rule_id=None, rule_name=None, context={})
        assert d.reason == ""


# ===========================================================================
# Policy.evaluate
# ===========================================================================


class TestPolicyEvaluate:
    def _allow_admins_policy(self) -> Policy:
        p = Policy(name="AdminPolicy", default_effect=RuleEffect.DENY)
        p.add_rule(make_rule(
            name="allow-admin",
            conditions=[Condition("role", "eq", "admin")],
            effect=RuleEffect.ALLOW,
            priority=10,
        ))
        return p

    def test_first_matching_rule_wins(self):
        p = self._allow_admins_policy()
        d = p.evaluate({"role": "admin"})
        assert d.is_allowed()
        assert d.rule_name == "allow-admin"

    def test_default_effect_when_no_match(self):
        p = self._allow_admins_policy()
        d = p.evaluate({"role": "viewer"})
        assert d.is_denied()
        assert d.rule_id is None
        assert d.rule_name is None

    def test_default_allow_policy(self):
        p = Policy(name="OpenPolicy", default_effect=RuleEffect.ALLOW)
        d = p.evaluate({"anything": True})
        assert d.is_allowed()

    def test_priority_ordering_highest_first(self):
        p = Policy(name="PrioTest", default_effect=RuleEffect.DENY)
        # Lower priority rule would DENY; higher priority rule ALLOWs first
        p.add_rule(make_rule(
            name="low-deny",
            conditions=[Condition("x", "eq", 1)],
            effect=RuleEffect.DENY,
            priority=1,
        ))
        p.add_rule(make_rule(
            name="high-allow",
            conditions=[Condition("x", "eq", 1)],
            effect=RuleEffect.ALLOW,
            priority=100,
        ))
        d = p.evaluate({"x": 1})
        assert d.is_allowed()
        assert d.rule_name == "high-allow"

    def test_second_rule_fires_when_first_no_match(self):
        p = Policy(name="Fallthrough", default_effect=RuleEffect.DENY)
        p.add_rule(make_rule(
            name="admin-allow",
            conditions=[Condition("role", "eq", "admin")],
            effect=RuleEffect.ALLOW,
            priority=10,
        ))
        p.add_rule(make_rule(
            name="editor-allow",
            conditions=[Condition("role", "eq", "editor")],
            effect=RuleEffect.ALLOW,
            priority=5,
        ))
        d = p.evaluate({"role": "editor"})
        assert d.is_allowed()
        assert d.rule_name == "editor-allow"

    def test_audit_rule_returned(self):
        p = Policy(name="AuditPolicy", default_effect=RuleEffect.AUDIT)
        p.add_rule(make_rule(
            name="audit-all",
            conditions=[],
            effect=RuleEffect.AUDIT,
            priority=0,
        ))
        d = p.evaluate({"role": "anyone"})
        assert d.effect is RuleEffect.AUDIT

    def test_add_rule_then_evaluate(self):
        p = Policy(name="Dynamic", default_effect=RuleEffect.DENY)
        rule = make_rule(
            name="late-add",
            conditions=[Condition("flag", "eq", True)],
            effect=RuleEffect.ALLOW,
        )
        p.add_rule(rule)
        assert p.evaluate({"flag": True}).is_allowed()
        assert p.evaluate({"flag": False}).is_denied()

    def test_policy_id_auto_generated(self):
        p = Policy(name="P")
        assert len(p.policy_id) == 8

    def test_policy_id_unique(self):
        ids = {Policy(name="P").policy_id for _ in range(50)}
        assert len(ids) == 50

    def test_reason_contains_rule_name_on_match(self):
        p = self._allow_admins_policy()
        d = p.evaluate({"role": "admin"})
        assert "allow-admin" in d.reason

    def test_reason_mentions_default_effect_when_no_match(self):
        p = self._allow_admins_policy()
        d = p.evaluate({"role": "nobody"})
        assert "default" in d.reason.lower() or "deny" in d.reason.lower()


# ===========================================================================
# PolicyEngine
# ===========================================================================


class TestPolicyEngineBasics:
    def test_empty_engine_allows(self):
        engine = PolicyEngine()
        d = engine.evaluate({"anything": True})
        assert d.is_allowed()
        assert "no policies" in d.reason.lower()

    def test_policy_count_zero(self):
        assert PolicyEngine().policy_count() == 0

    def test_add_policy_increments_count(self):
        engine = PolicyEngine()
        engine.add_policy(Policy(name="P1"))
        assert engine.policy_count() == 1
        engine.add_policy(Policy(name="P2"))
        assert engine.policy_count() == 2

    def test_remove_policy_existing(self):
        engine = PolicyEngine()
        p = Policy(name="P")
        engine.add_policy(p)
        assert engine.remove_policy(p.policy_id) is True
        assert engine.policy_count() == 0

    def test_remove_policy_missing(self):
        engine = PolicyEngine()
        assert engine.remove_policy("does-not-exist") is False

    def test_remove_policy_makes_engine_open(self):
        engine = PolicyEngine()
        p = Policy(name="DenyAll", default_effect=RuleEffect.DENY)
        engine.add_policy(p)
        assert engine.evaluate({}).is_denied()
        engine.remove_policy(p.policy_id)
        assert engine.evaluate({}).is_allowed()


class TestPolicyEngineDenyPrecedence:
    def test_deny_overrides_allow(self):
        engine = PolicyEngine()

        allow_p = Policy(name="AllowAll", default_effect=RuleEffect.ALLOW)
        deny_p = Policy(name="DenyAll", default_effect=RuleEffect.DENY)

        engine.add_policy(allow_p)
        engine.add_policy(deny_p)

        d = engine.evaluate({"role": "admin"})
        assert d.is_denied()

    def test_single_deny_rule_beats_allow_policy(self):
        engine = PolicyEngine()

        allow_p = Policy(name="AllowAll", default_effect=RuleEffect.ALLOW)
        deny_p = Policy(name="SelectiveDeny", default_effect=RuleEffect.ALLOW)
        deny_p.add_rule(make_rule(
            name="deny-guests",
            conditions=[Condition("role", "eq", "guest")],
            effect=RuleEffect.DENY,
        ))

        engine.add_policy(allow_p)
        engine.add_policy(deny_p)

        assert engine.evaluate({"role": "guest"}).is_denied()
        assert engine.evaluate({"role": "admin"}).is_allowed()


class TestPolicyEngineAllowWins:
    def test_allow_with_no_deny(self):
        engine = PolicyEngine()
        p = Policy(name="AllowAdmins", default_effect=RuleEffect.DENY)
        p.add_rule(make_rule(
            name="admin-ok",
            conditions=[Condition("role", "eq", "admin")],
            effect=RuleEffect.ALLOW,
        ))
        engine.add_policy(p)
        assert engine.evaluate({"role": "admin"}).is_allowed()
        assert engine.evaluate({"role": "user"}).is_denied()


class TestPolicyEngineAudit:
    def test_all_audit_returns_audit(self):
        engine = PolicyEngine()
        p1 = Policy(name="Audit1", default_effect=RuleEffect.AUDIT)
        p2 = Policy(name="Audit2", default_effect=RuleEffect.AUDIT)
        engine.add_policy(p1)
        engine.add_policy(p2)
        d = engine.evaluate({"x": 1})
        assert d.effect is RuleEffect.AUDIT

    def test_audit_plus_allow_returns_allow(self):
        engine = PolicyEngine()
        audit_p = Policy(name="Audit", default_effect=RuleEffect.AUDIT)
        allow_p = Policy(name="Allow", default_effect=RuleEffect.ALLOW)
        engine.add_policy(audit_p)
        engine.add_policy(allow_p)
        d = engine.evaluate({})
        assert d.is_allowed()

    def test_audit_plus_deny_returns_deny(self):
        engine = PolicyEngine()
        audit_p = Policy(name="Audit", default_effect=RuleEffect.AUDIT)
        deny_p = Policy(name="Deny", default_effect=RuleEffect.DENY)
        engine.add_policy(audit_p)
        engine.add_policy(deny_p)
        d = engine.evaluate({})
        assert d.is_denied()


class TestPolicyEngineAuditLog:
    def _setup(self):
        engine = PolicyEngine()
        p = Policy(name="TestPolicy", default_effect=RuleEffect.ALLOW)
        engine.add_policy(p)
        ctx = {"user": {"role": "admin"}, "action": "read"}
        decision = engine.evaluate(ctx)
        return engine, ctx, decision

    def test_audit_log_returns_dict(self):
        engine, ctx, decision = self._setup()
        log = engine.audit_log(ctx, decision)
        assert isinstance(log, dict)

    def test_audit_log_effect(self):
        engine, ctx, decision = self._setup()
        log = engine.audit_log(ctx, decision)
        assert log["effect"] == decision.effect.value

    def test_audit_log_context(self):
        engine, ctx, decision = self._setup()
        log = engine.audit_log(ctx, decision)
        assert log["context"] == ctx

    def test_audit_log_reason(self):
        engine, ctx, decision = self._setup()
        log = engine.audit_log(ctx, decision)
        assert "reason" in log

    def test_audit_log_timestamp_present(self):
        engine, ctx, decision = self._setup()
        log = engine.audit_log(ctx, decision)
        assert "timestamp" in log
        # basic ISO format check
        ts = log["timestamp"]
        assert "T" in ts and ts.endswith("Z")

    def test_audit_log_policy_count(self):
        engine, ctx, decision = self._setup()
        log = engine.audit_log(ctx, decision)
        assert log["policy_count"] == 1

    def test_audit_log_rule_id_and_name(self):
        engine, ctx, decision = self._setup()
        log = engine.audit_log(ctx, decision)
        assert "rule_id" in log
        assert "rule_name" in log


# ===========================================================================
# Integration: multi-condition, multi-policy scenario
# ===========================================================================


class TestIntegration:
    def test_rbac_scenario(self):
        """Admins can delete; editors can write; others get default deny."""
        engine = PolicyEngine()

        acl = Policy(name="ACL", default_effect=RuleEffect.DENY)
        acl.add_rule(make_rule(
            name="admin-full-access",
            conditions=[Condition("user.role", "eq", "admin")],
            effect=RuleEffect.ALLOW,
            priority=20,
        ))
        acl.add_rule(make_rule(
            name="editor-write",
            conditions=[
                Condition("user.role", "eq", "editor"),
                Condition("action", "in", ["create", "update"]),
            ],
            effect=RuleEffect.ALLOW,
            priority=10,
        ))
        engine.add_policy(acl)

        admin_ctx = {"user": {"role": "admin"}, "action": "delete"}
        editor_write_ctx = {"user": {"role": "editor"}, "action": "create"}
        editor_delete_ctx = {"user": {"role": "editor"}, "action": "delete"}
        viewer_ctx = {"user": {"role": "viewer"}, "action": "read"}

        assert engine.evaluate(admin_ctx).is_allowed()
        assert engine.evaluate(editor_write_ctx).is_allowed()
        assert engine.evaluate(editor_delete_ctx).is_denied()
        assert engine.evaluate(viewer_ctx).is_denied()

    def test_ip_blocklist_overrides_allow(self):
        engine = PolicyEngine()

        allow_p = Policy(name="AllowAll", default_effect=RuleEffect.ALLOW)
        blocklist = Policy(name="IPBlocklist", default_effect=RuleEffect.ALLOW)
        blocklist.add_rule(make_rule(
            name="block-bad-ip",
            conditions=[Condition("request.ip", "in", ["1.2.3.4", "5.6.7.8"])],
            effect=RuleEffect.DENY,
        ))

        engine.add_policy(allow_p)
        engine.add_policy(blocklist)

        safe_ctx = {"request": {"ip": "9.9.9.9"}}
        bad_ctx = {"request": {"ip": "1.2.3.4"}}

        assert engine.evaluate(safe_ctx).is_allowed()
        assert engine.evaluate(bad_ctx).is_denied()
