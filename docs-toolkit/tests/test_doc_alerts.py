"""Tests for docstoolkit.doc_alerts (E210)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_alerts import (
    Alert,
    AlertRule,
    AlertSeverity,
    AlertState,
    AlertStats,
    DocAlerts,
)


# ------------------- helpers -------------------

def _cond_size_gt(threshold: int):
    def _c(payload: dict) -> bool:
        return payload.get("size", 0) > threshold
    return _c


def _cond_always_true(payload: dict) -> bool:
    return True


def _cond_always_false(payload: dict) -> bool:
    return False


# ------------------- AlertSeverity -------------------

class TestAlertSeverity:
    def test_has_info(self):
        assert AlertSeverity.INFO.value == "info"

    def test_has_low(self):
        assert AlertSeverity.LOW.value == "low"

    def test_has_medium(self):
        assert AlertSeverity.MEDIUM.value == "medium"

    def test_has_high(self):
        assert AlertSeverity.HIGH.value == "high"

    def test_has_critical(self):
        assert AlertSeverity.CRITICAL.value == "critical"

    def test_five_levels(self):
        assert len(list(AlertSeverity)) == 5


# ------------------- AlertState -------------------

class TestAlertState:
    def test_has_active(self):
        assert AlertState.ACTIVE.value == "active"

    def test_has_acknowledged(self):
        assert AlertState.ACKNOWLEDGED.value == "acknowledged"

    def test_has_resolved(self):
        assert AlertState.RESOLVED.value == "resolved"

    def test_has_expired(self):
        assert AlertState.EXPIRED.value == "expired"

    def test_four_states(self):
        assert len(list(AlertState)) == 4


# ------------------- AlertRule -------------------

class TestAlertRule:
    def test_construction(self):
        rule = AlertRule(
            rule_id="r1", name="n", condition=_cond_always_true
        )
        assert rule.rule_id == "r1"
        assert rule.name == "n"
        assert rule.condition is _cond_always_true

    def test_default_severity_medium(self):
        rule = AlertRule(
            rule_id="r1", name="n", condition=_cond_always_true
        )
        assert rule.severity == AlertSeverity.MEDIUM

    def test_default_enabled_true(self):
        rule = AlertRule(
            rule_id="r1", name="n", condition=_cond_always_true
        )
        assert rule.enabled is True

    def test_default_cooldown_60(self):
        rule = AlertRule(
            rule_id="r1", name="n", condition=_cond_always_true
        )
        assert rule.cooldown_seconds == 60.0

    def test_default_expires_none(self):
        rule = AlertRule(
            rule_id="r1", name="n", condition=_cond_always_true
        )
        assert rule.expires_after is None

    def test_default_last_triggered_zero(self):
        rule = AlertRule(
            rule_id="r1", name="n", condition=_cond_always_true
        )
        assert rule.last_triggered == 0.0


# ------------------- Alert -------------------

class TestAlert:
    def test_construction(self):
        a = Alert(
            alert_id="a1",
            rule_id="r1",
            triggered_at=10.0,
            state=AlertState.ACTIVE,
            payload={"x": 1},
            severity=AlertSeverity.HIGH,
        )
        assert a.alert_id == "a1"
        assert a.rule_id == "r1"
        assert a.triggered_at == 10.0
        assert a.state == AlertState.ACTIVE
        assert a.payload == {"x": 1}
        assert a.severity == AlertSeverity.HIGH

    def test_defaults(self):
        a = Alert(
            alert_id="a1",
            rule_id="r1",
            triggered_at=0.0,
            state=AlertState.ACTIVE,
            payload={},
            severity=AlertSeverity.LOW,
        )
        assert a.acknowledged_by is None
        assert a.acknowledged_at is None
        assert a.resolved_at is None
        assert a.expires_at is None


# ------------------- AlertStats -------------------

class TestAlertStats:
    def test_defaults(self):
        s = AlertStats()
        assert s.total == 0
        assert s.active == 0
        assert s.acknowledged == 0
        assert s.resolved == 0
        assert s.by_severity == {}

    def test_construction(self):
        s = AlertStats(total=5, active=3, acknowledged=1, resolved=1,
                       by_severity={"high": 2})
        assert s.total == 5
        assert s.active == 3
        assert s.acknowledged == 1
        assert s.resolved == 1
        assert s.by_severity == {"high": 2}


# ------------------- add_rule -------------------

class TestAddRule:
    def test_returns_rule(self):
        da = DocAlerts()
        rule = da.add_rule("size_check", _cond_size_gt(100))
        assert isinstance(rule, AlertRule)

    def test_rule_id_unique(self):
        da = DocAlerts()
        r1 = da.add_rule("a", _cond_always_true)
        r2 = da.add_rule("b", _cond_always_true)
        assert r1.rule_id != r2.rule_id

    def test_sets_name(self):
        da = DocAlerts()
        rule = da.add_rule("named", _cond_always_true)
        assert rule.name == "named"

    def test_sets_severity(self):
        da = DocAlerts()
        rule = da.add_rule(
            "x", _cond_always_true, severity=AlertSeverity.CRITICAL
        )
        assert rule.severity == AlertSeverity.CRITICAL

    def test_sets_cooldown(self):
        da = DocAlerts()
        rule = da.add_rule("x", _cond_always_true, cooldown_seconds=5.0)
        assert rule.cooldown_seconds == 5.0

    def test_sets_expires_after(self):
        da = DocAlerts()
        rule = da.add_rule("x", _cond_always_true, expires_after=30.0)
        assert rule.expires_after == 30.0

    def test_enabled_by_default(self):
        da = DocAlerts()
        rule = da.add_rule("x", _cond_always_true)
        assert rule.enabled is True

    def test_increments_rule_count(self):
        da = DocAlerts()
        assert da.rule_count == 0
        da.add_rule("a", _cond_always_true)
        assert da.rule_count == 1


# ------------------- remove_rule -------------------

class TestRemoveRule:
    def test_removes_existing(self):
        da = DocAlerts()
        rule = da.add_rule("a", _cond_always_true)
        assert da.remove_rule(rule.rule_id) is True
        assert da.rule_count == 0

    def test_returns_false_unknown(self):
        da = DocAlerts()
        assert da.remove_rule("nope") is False

    def test_no_effect_on_other_rules(self):
        da = DocAlerts()
        r1 = da.add_rule("a", _cond_always_true)
        r2 = da.add_rule("b", _cond_always_true)
        da.remove_rule(r1.rule_id)
        assert da.rule_count == 1
        assert any(r.rule_id == r2.rule_id for r in da.list_rules())


# ------------------- enable / disable -------------------

class TestEnableDisable:
    def test_disable_existing(self):
        da = DocAlerts()
        rule = da.add_rule("a", _cond_always_true)
        assert da.disable_rule(rule.rule_id) is True
        assert rule.enabled is False

    def test_enable_existing(self):
        da = DocAlerts()
        rule = da.add_rule("a", _cond_always_true)
        da.disable_rule(rule.rule_id)
        assert da.enable_rule(rule.rule_id) is True
        assert rule.enabled is True

    def test_disable_unknown(self):
        da = DocAlerts()
        assert da.disable_rule("nope") is False

    def test_enable_unknown(self):
        da = DocAlerts()
        assert da.enable_rule("nope") is False


# ------------------- evaluate basic -------------------

class TestEvaluateBasic:
    def test_fires_when_true(self):
        da = DocAlerts()
        da.add_rule("always", _cond_always_true)
        fired = da.evaluate({}, now=1.0)
        assert len(fired) == 1

    def test_no_fire_when_false(self):
        da = DocAlerts()
        da.add_rule("never", _cond_always_false)
        fired = da.evaluate({}, now=1.0)
        assert fired == []

    def test_alert_state_active(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        fired = da.evaluate({}, now=1.0)
        assert fired[0].state == AlertState.ACTIVE

    def test_alert_records_payload(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        fired = da.evaluate({"k": "v"}, now=1.0)
        assert fired[0].payload == {"k": "v"}

    def test_alert_records_triggered_at(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        fired = da.evaluate({}, now=42.0)
        assert fired[0].triggered_at == 42.0

    def test_alert_records_severity(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, severity=AlertSeverity.HIGH)
        fired = da.evaluate({}, now=1.0)
        assert fired[0].severity == AlertSeverity.HIGH

    def test_expires_at_set_when_rule_has_expires(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, expires_after=30.0)
        fired = da.evaluate({}, now=10.0)
        assert fired[0].expires_at == 40.0

    def test_expires_at_none_when_rule_has_none(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        fired = da.evaluate({}, now=10.0)
        assert fired[0].expires_at is None


# ------------------- evaluate multiple rules -------------------

class TestEvaluateMultipleRules:
    def test_two_rules_fire(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.add_rule("b", _cond_always_true)
        fired = da.evaluate({}, now=1.0)
        assert len(fired) == 2

    def test_only_matching_fire(self):
        da = DocAlerts()
        da.add_rule("yes", _cond_always_true)
        da.add_rule("no", _cond_always_false)
        fired = da.evaluate({}, now=1.0)
        assert len(fired) == 1

    def test_condition_payload_based(self):
        da = DocAlerts()
        da.add_rule("big", _cond_size_gt(100))
        da.add_rule("huge", _cond_size_gt(1_000_000))
        fired = da.evaluate({"size": 500}, now=1.0)
        assert len(fired) == 1


# ------------------- cooldown -------------------

class TestEvaluateCooldown:
    def test_blocks_within_cooldown(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, cooldown_seconds=10.0)
        first = da.evaluate({}, now=0.0)
        assert len(first) == 1
        second = da.evaluate({}, now=5.0)
        assert second == []

    def test_allows_after_cooldown(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, cooldown_seconds=10.0)
        da.evaluate({}, now=0.0)
        again = da.evaluate({}, now=11.0)
        assert len(again) == 1

    def test_cooldown_exact_boundary(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, cooldown_seconds=10.0)
        da.evaluate({}, now=0.0)
        # equal => not less than => allow
        again = da.evaluate({}, now=10.0)
        assert len(again) == 1

    def test_zero_cooldown_always_fires(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, cooldown_seconds=0.0)
        da.evaluate({}, now=0.0)
        again = da.evaluate({}, now=0.0)
        assert len(again) == 1


# ------------------- disabled rules -------------------

class TestEvaluateDisabled:
    def test_disabled_rule_does_not_fire(self):
        da = DocAlerts()
        rule = da.add_rule("a", _cond_always_true)
        da.disable_rule(rule.rule_id)
        fired = da.evaluate({}, now=1.0)
        assert fired == []

    def test_reenabled_rule_fires(self):
        da = DocAlerts()
        rule = da.add_rule("a", _cond_always_true)
        da.disable_rule(rule.rule_id)
        da.enable_rule(rule.rule_id)
        fired = da.evaluate({}, now=1.0)
        assert len(fired) == 1


# ------------------- condition fails -------------------

class TestEvaluateConditionFails:
    def test_exception_in_condition_does_not_fire(self):
        def boom(payload: dict) -> bool:
            raise RuntimeError("nope")

        da = DocAlerts()
        da.add_rule("bad", boom)
        fired = da.evaluate({}, now=1.0)
        assert fired == []

    def test_exception_does_not_block_other_rules(self):
        def boom(payload: dict) -> bool:
            raise RuntimeError("nope")

        da = DocAlerts()
        da.add_rule("bad", boom)
        da.add_rule("good", _cond_always_true)
        fired = da.evaluate({}, now=1.0)
        assert len(fired) == 1


# ------------------- acknowledge -------------------

class TestAcknowledge:
    def test_ack_active_alert(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        assert da.acknowledge(alert.alert_id, by="alice", now=2.0) is True

    def test_ack_sets_state(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.acknowledge(alert.alert_id, by="alice", now=2.0)
        assert alert.state == AlertState.ACKNOWLEDGED

    def test_ack_records_by(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.acknowledge(alert.alert_id, by="alice", now=2.0)
        assert alert.acknowledged_by == "alice"

    def test_ack_records_time(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.acknowledge(alert.alert_id, by="bob", now=2.5)
        assert alert.acknowledged_at == 2.5

    def test_ack_unknown(self):
        da = DocAlerts()
        assert da.acknowledge("nope", by="x", now=1.0) is False

    def test_ack_already_acked_fails(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.acknowledge(alert.alert_id, by="alice", now=2.0)
        assert da.acknowledge(alert.alert_id, by="bob", now=3.0) is False


# ------------------- resolve -------------------

class TestResolve:
    def test_resolve_active(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        assert da.resolve(alert.alert_id, now=2.0) is True
        assert alert.state == AlertState.RESOLVED

    def test_resolve_acked(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.acknowledge(alert.alert_id, by="x", now=2.0)
        assert da.resolve(alert.alert_id, now=3.0) is True
        assert alert.state == AlertState.RESOLVED

    def test_resolve_records_time(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.resolve(alert.alert_id, now=9.0)
        assert alert.resolved_at == 9.0

    def test_resolve_unknown(self):
        da = DocAlerts()
        assert da.resolve("nope", now=1.0) is False

    def test_resolve_twice_fails(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.resolve(alert.alert_id, now=2.0)
        assert da.resolve(alert.alert_id, now=3.0) is False


# ------------------- expire_overdue -------------------

class TestExpireOverdue:
    def test_expires_overdue_alert(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, expires_after=10.0)
        alert = da.evaluate({}, now=0.0)[0]
        n = da.expire_overdue(now=11.0)
        assert n == 1
        assert alert.state == AlertState.EXPIRED

    def test_does_not_expire_in_window(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, expires_after=10.0)
        alert = da.evaluate({}, now=0.0)[0]
        n = da.expire_overdue(now=5.0)
        assert n == 0
        assert alert.state == AlertState.ACTIVE

    def test_ignores_alerts_without_expires(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.evaluate({}, now=0.0)
        assert da.expire_overdue(now=1_000_000.0) == 0

    def test_ignores_resolved(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, expires_after=10.0)
        alert = da.evaluate({}, now=0.0)[0]
        da.resolve(alert.alert_id, now=1.0)
        n = da.expire_overdue(now=100.0)
        assert n == 0
        assert alert.state == AlertState.RESOLVED

    def test_expires_acked_alerts(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, expires_after=10.0)
        alert = da.evaluate({}, now=0.0)[0]
        da.acknowledge(alert.alert_id, by="x", now=1.0)
        n = da.expire_overdue(now=20.0)
        assert n == 1
        assert alert.state == AlertState.EXPIRED


# ------------------- get_alert -------------------

class TestGetAlert:
    def test_returns_known(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        assert da.get_alert(alert.alert_id) is alert

    def test_returns_none_unknown(self):
        da = DocAlerts()
        assert da.get_alert("nope") is None


# ------------------- active_alerts -------------------

class TestActiveAlerts:
    def test_lists_active(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.evaluate({}, now=1.0)
        assert len(da.active_alerts()) == 1

    def test_excludes_acked(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.acknowledge(alert.alert_id, by="x", now=2.0)
        assert da.active_alerts() == []

    def test_empty_when_no_alerts(self):
        da = DocAlerts()
        assert da.active_alerts() == []


# ------------------- acknowledged_alerts -------------------

class TestAcknowledgedAlerts:
    def test_lists_acked(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.acknowledge(alert.alert_id, by="x", now=2.0)
        assert len(da.acknowledged_alerts()) == 1

    def test_empty_when_none(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.evaluate({}, now=1.0)
        assert da.acknowledged_alerts() == []


# ------------------- resolved_alerts -------------------

class TestResolvedAlerts:
    def test_lists_resolved(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.resolve(alert.alert_id, now=2.0)
        assert len(da.resolved_alerts()) == 1

    def test_empty_when_none(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.evaluate({}, now=1.0)
        assert da.resolved_alerts() == []


# ------------------- alerts_by_severity -------------------

class TestAlertsBySeverity:
    def test_filter_by_high(self):
        da = DocAlerts()
        da.add_rule("h", _cond_always_true, severity=AlertSeverity.HIGH)
        da.add_rule("l", _cond_always_true, severity=AlertSeverity.LOW)
        da.evaluate({}, now=1.0)
        high = da.alerts_by_severity(AlertSeverity.HIGH)
        assert len(high) == 1
        assert high[0].severity == AlertSeverity.HIGH

    def test_empty_no_matches(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, severity=AlertSeverity.LOW)
        da.evaluate({}, now=1.0)
        assert da.alerts_by_severity(AlertSeverity.CRITICAL) == []


# ------------------- alerts_for_rule -------------------

class TestAlertsForRule:
    def test_filters_by_rule(self):
        da = DocAlerts()
        r1 = da.add_rule("a", _cond_always_true, cooldown_seconds=0.0)
        r2 = da.add_rule("b", _cond_always_true, cooldown_seconds=0.0)
        da.evaluate({}, now=1.0)
        da.evaluate({}, now=2.0)
        a1 = da.alerts_for_rule(r1.rule_id)
        a2 = da.alerts_for_rule(r2.rule_id)
        assert len(a1) == 2
        assert len(a2) == 2
        assert all(a.rule_id == r1.rule_id for a in a1)

    def test_empty_unknown_rule(self):
        da = DocAlerts()
        assert da.alerts_for_rule("nope") == []


# ------------------- stats -------------------

class TestStats:
    def test_returns_stats(self):
        da = DocAlerts()
        s = da.stats()
        assert isinstance(s, AlertStats)
        assert s.total == 0

    def test_counts_total(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, cooldown_seconds=0.0)
        da.evaluate({}, now=1.0)
        da.evaluate({}, now=2.0)
        assert da.stats().total == 2

    def test_counts_active(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.evaluate({}, now=1.0)
        assert da.stats().active == 1

    def test_counts_acked(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.acknowledge(alert.alert_id, by="x", now=2.0)
        assert da.stats().acknowledged == 1

    def test_counts_resolved(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.resolve(alert.alert_id, now=2.0)
        assert da.stats().resolved == 1

    def test_by_severity(self):
        da = DocAlerts()
        da.add_rule("h", _cond_always_true, severity=AlertSeverity.HIGH)
        da.add_rule("c", _cond_always_true, severity=AlertSeverity.CRITICAL)
        da.evaluate({}, now=1.0)
        bs = da.stats().by_severity
        assert bs["high"] == 1
        assert bs["critical"] == 1


# ------------------- rule_count -------------------

class TestRuleCount:
    def test_zero_initial(self):
        assert DocAlerts().rule_count == 0

    def test_increments(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.add_rule("b", _cond_always_true)
        assert da.rule_count == 2

    def test_decrements_on_remove(self):
        da = DocAlerts()
        rule = da.add_rule("a", _cond_always_true)
        da.remove_rule(rule.rule_id)
        assert da.rule_count == 0


# ------------------- alert_count -------------------

class TestAlertCount:
    def test_zero_initial(self):
        assert DocAlerts().alert_count == 0

    def test_increments_on_fire(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, cooldown_seconds=0.0)
        da.evaluate({}, now=1.0)
        da.evaluate({}, now=2.0)
        assert da.alert_count == 2


# ------------------- list_rules -------------------

class TestListRules:
    def test_empty(self):
        assert DocAlerts().list_rules() == []

    def test_all_rules(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.add_rule("b", _cond_always_true)
        assert len(da.list_rules()) == 2

    def test_enabled_only(self):
        da = DocAlerts()
        r1 = da.add_rule("a", _cond_always_true)
        da.add_rule("b", _cond_always_true)
        da.disable_rule(r1.rule_id)
        rules = da.list_rules(enabled_only=True)
        assert len(rules) == 1
        assert rules[0].enabled is True


# ------------------- clear -------------------

class TestClear:
    def test_clears_rules(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.clear()
        assert da.rule_count == 0

    def test_clears_alerts(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        da.evaluate({}, now=1.0)
        da.clear()
        assert da.alert_count == 0


# ------------------- edge cases -------------------

class TestEdgeCases:
    def test_payload_is_copied(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        payload = {"k": "v"}
        alert = da.evaluate(payload, now=1.0)[0]
        payload["k"] = "changed"
        assert alert.payload["k"] == "v"

    def test_default_now_zero(self):
        da = DocAlerts()
        da.add_rule("a", _cond_always_true)
        fired = da.evaluate({})
        assert fired[0].triggered_at == 0.0

    def test_evaluate_no_rules(self):
        da = DocAlerts()
        assert da.evaluate({"x": 1}, now=1.0) == []

    def test_remove_rule_keeps_alerts(self):
        da = DocAlerts()
        rule = da.add_rule("a", _cond_always_true)
        alert = da.evaluate({}, now=1.0)[0]
        da.remove_rule(rule.rule_id)
        # alerts persist even after rule removal
        assert da.get_alert(alert.alert_id) is alert

    def test_last_triggered_updated(self):
        da = DocAlerts()
        rule = da.add_rule("a", _cond_always_true, cooldown_seconds=5.0)
        da.evaluate({}, now=3.0)
        assert rule.last_triggered == 3.0

    def test_severity_value_strings(self):
        # ensure stats keys are severity .value strings
        da = DocAlerts()
        da.add_rule("a", _cond_always_true, severity=AlertSeverity.INFO)
        da.evaluate({}, now=1.0)
        assert "info" in da.stats().by_severity
