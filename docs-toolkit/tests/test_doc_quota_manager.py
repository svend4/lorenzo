"""Tests for E305 DocQuotaManager."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_quota_manager import (
    DocQuotaManager,
    QuotaCheckResult,
    QuotaRule,
    QuotaUsage,
)


# ---------------------------------------------------------------------------
# TestQuotaRuleDataclass
# ---------------------------------------------------------------------------


class TestQuotaRuleDataclass:
    def test_required_fields(self):
        rule = QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=100)
        assert rule.rule_id == "r1"
        assert rule.subject == "user:alice"
        assert rule.resource == "docs"
        assert rule.limit == 100

    def test_default_period(self):
        rule = QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=100)
        assert rule.period == "total"

    def test_custom_period_daily(self):
        rule = QuotaRule(
            rule_id="r1", subject="user:alice", resource="docs", limit=10, period="daily"
        )
        assert rule.period == "daily"

    def test_custom_period_monthly(self):
        rule = QuotaRule(
            rule_id="r1", subject="user:alice", resource="docs", limit=50, period="monthly"
        )
        assert rule.period == "monthly"

    def test_wildcard_subject(self):
        rule = QuotaRule(rule_id="global", subject="*", resource="api_calls", limit=1000)
        assert rule.subject == "*"

    def test_zero_limit(self):
        rule = QuotaRule(rule_id="r0", subject="user:bob", resource="storage_mb", limit=0)
        assert rule.limit == 0


# ---------------------------------------------------------------------------
# TestQuotaUsageDataclass
# ---------------------------------------------------------------------------


class TestQuotaUsageDataclass:
    def test_fields_accessible(self):
        usage = QuotaUsage(
            subject="user:alice",
            resource="docs",
            used=50,
            limit=100,
            remaining=50,
            exceeded=False,
        )
        assert usage.subject == "user:alice"
        assert usage.resource == "docs"
        assert usage.used == 50
        assert usage.limit == 100
        assert usage.remaining == 50
        assert usage.exceeded is False

    def test_exceeded_true(self):
        usage = QuotaUsage(
            subject="user:bob",
            resource="docs",
            used=110,
            limit=100,
            remaining=0,
            exceeded=True,
        )
        assert usage.exceeded is True
        assert usage.remaining == 0

    def test_exceeded_at_exact_limit_is_false(self):
        usage = QuotaUsage(
            subject="user:carol",
            resource="docs",
            used=100,
            limit=100,
            remaining=0,
            exceeded=False,
        )
        assert usage.exceeded is False

    def test_remaining_nonzero(self):
        usage = QuotaUsage(
            subject="u", resource="r", used=10, limit=100, remaining=90, exceeded=False
        )
        assert usage.remaining == 90


# ---------------------------------------------------------------------------
# TestQuotaCheckResultDataclass
# ---------------------------------------------------------------------------


class TestQuotaCheckResultDataclass:
    def test_allowed_fields(self):
        result = QuotaCheckResult(
            allowed=True,
            subject="user:alice",
            resource="docs",
            used=5,
            limit=100,
            reason="within quota",
        )
        assert result.allowed is True
        assert result.subject == "user:alice"
        assert result.resource == "docs"
        assert result.used == 5
        assert result.limit == 100
        assert result.reason == "within quota"

    def test_denied_fields(self):
        result = QuotaCheckResult(
            allowed=False,
            subject="user:bob",
            resource="storage_mb",
            used=200,
            limit=100,
            reason="quota exceeded",
        )
        assert result.allowed is False
        assert result.reason == "quota exceeded"


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_rules(self):
        mgr = DocQuotaManager()
        assert mgr.rules_for_subject("anyone") == []

    def test_empty_usage(self):
        mgr = DocQuotaManager()
        assert mgr.get_usage("user:x", "docs") == 0

    def test_all_subjects_empty(self):
        mgr = DocQuotaManager()
        assert mgr.all_subjects() == []

    def test_exceeded_subjects_empty(self):
        mgr = DocQuotaManager()
        assert mgr.exceeded_subjects() == []


# ---------------------------------------------------------------------------
# TestSetRule
# ---------------------------------------------------------------------------


class TestSetRule:
    def test_set_new_rule(self):
        mgr = DocQuotaManager()
        rule = QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=100)
        mgr.set_rule(rule)
        assert mgr.get_rule("r1") == rule

    def test_replace_existing_rule(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=100))
        new_rule = QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=200)
        mgr.set_rule(new_rule)
        assert mgr.get_rule("r1").limit == 200

    def test_multiple_resources_for_same_subject(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=50))
        mgr.set_rule(QuotaRule(rule_id="r2", subject="user:alice", resource="storage_mb", limit=500))
        rules = mgr.rules_for_subject("user:alice")
        resources = {r.resource for r in rules}
        assert resources == {"docs", "storage_mb"}

    def test_set_global_wildcard_rule(self):
        mgr = DocQuotaManager()
        rule = QuotaRule(rule_id="global", subject="*", resource="api_calls", limit=1000)
        mgr.set_rule(rule)
        assert mgr.get_rule("global") is rule


# ---------------------------------------------------------------------------
# TestRemoveRule
# ---------------------------------------------------------------------------


class TestRemoveRule:
    def test_remove_existing_returns_true(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="u", resource="docs", limit=10))
        assert mgr.remove_rule("r1") is True

    def test_remove_nonexistent_returns_false(self):
        mgr = DocQuotaManager()
        assert mgr.remove_rule("no-such-rule") is False

    def test_removed_rule_is_gone(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="u", resource="docs", limit=10))
        mgr.remove_rule("r1")
        assert mgr.get_rule("r1") is None

    def test_remove_idempotent_second_call_false(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="u", resource="docs", limit=10))
        mgr.remove_rule("r1")
        assert mgr.remove_rule("r1") is False


# ---------------------------------------------------------------------------
# TestGetRule
# ---------------------------------------------------------------------------


class TestGetRule:
    def test_found(self):
        mgr = DocQuotaManager()
        rule = QuotaRule(rule_id="r1", subject="u", resource="docs", limit=10)
        mgr.set_rule(rule)
        assert mgr.get_rule("r1") is rule

    def test_not_found_returns_none(self):
        mgr = DocQuotaManager()
        assert mgr.get_rule("missing") is None


# ---------------------------------------------------------------------------
# TestRulesForSubject
# ---------------------------------------------------------------------------


class TestRulesForSubject:
    def test_returns_matching_rules(self):
        mgr = DocQuotaManager()
        r1 = QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=10)
        r2 = QuotaRule(rule_id="r2", subject="user:alice", resource="api_calls", limit=100)
        r3 = QuotaRule(rule_id="r3", subject="user:bob", resource="docs", limit=5)
        mgr.set_rule(r1)
        mgr.set_rule(r2)
        mgr.set_rule(r3)
        rules = mgr.rules_for_subject("user:alice")
        assert len(rules) == 2
        assert r3 not in rules

    def test_sorted_by_rule_id(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="zz", subject="u", resource="r1", limit=1))
        mgr.set_rule(QuotaRule(rule_id="aa", subject="u", resource="r2", limit=2))
        rules = mgr.rules_for_subject("u")
        assert [r.rule_id for r in rules] == ["aa", "zz"]

    def test_empty_for_unknown_subject(self):
        mgr = DocQuotaManager()
        assert mgr.rules_for_subject("ghost") == []


# ---------------------------------------------------------------------------
# TestIncrement
# ---------------------------------------------------------------------------


class TestIncrement:
    def test_increment_from_zero(self):
        mgr = DocQuotaManager()
        total = mgr.increment("user:alice", "docs")
        assert total == 1

    def test_increment_returns_new_total(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 5)
        total = mgr.increment("user:alice", "docs", 3)
        assert total == 8

    def test_increment_multiple_calls(self):
        mgr = DocQuotaManager()
        for _ in range(10):
            mgr.increment("user:alice", "docs")
        assert mgr.get_usage("user:alice", "docs") == 10

    def test_increment_different_resources_independent(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 3)
        mgr.increment("user:alice", "storage_mb", 100)
        assert mgr.get_usage("user:alice", "docs") == 3
        assert mgr.get_usage("user:alice", "storage_mb") == 100


# ---------------------------------------------------------------------------
# TestDecrement
# ---------------------------------------------------------------------------


class TestDecrement:
    def test_decrement_basic(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 10)
        total = mgr.decrement("user:alice", "docs", 3)
        assert total == 7

    def test_decrement_floors_at_zero(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 2)
        total = mgr.decrement("user:alice", "docs", 10)
        assert total == 0

    def test_decrement_on_zero_stays_zero(self):
        mgr = DocQuotaManager()
        total = mgr.decrement("user:alice", "docs", 5)
        assert total == 0

    def test_decrement_returns_value(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 5)
        result = mgr.decrement("user:alice", "docs", 2)
        assert result == 3


# ---------------------------------------------------------------------------
# TestResetUsage
# ---------------------------------------------------------------------------


class TestResetUsage:
    def test_reset_brings_to_zero(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 50)
        mgr.reset_usage("user:alice", "docs")
        assert mgr.get_usage("user:alice", "docs") == 0

    def test_reset_unknown_subject_stays_zero(self):
        mgr = DocQuotaManager()
        mgr.reset_usage("ghost", "docs")
        assert mgr.get_usage("ghost", "docs") == 0

    def test_reset_does_not_affect_other_resources(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 10)
        mgr.increment("user:alice", "storage_mb", 200)
        mgr.reset_usage("user:alice", "docs")
        assert mgr.get_usage("user:alice", "storage_mb") == 200


# ---------------------------------------------------------------------------
# TestGetUsage
# ---------------------------------------------------------------------------


class TestGetUsage:
    def test_zero_for_unknown(self):
        mgr = DocQuotaManager()
        assert mgr.get_usage("nobody", "docs") == 0

    def test_returns_incremented_value(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 7)
        assert mgr.get_usage("user:alice", "docs") == 7


# ---------------------------------------------------------------------------
# TestCheck
# ---------------------------------------------------------------------------


class TestCheck:
    def _mgr_with_rule(self, limit: int, subject: str = "user:alice") -> DocQuotaManager:
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject=subject, resource="docs", limit=limit))
        return mgr

    def test_under_limit_allowed(self):
        mgr = self._mgr_with_rule(10)
        mgr.increment("user:alice", "docs", 5)
        result = mgr.check("user:alice", "docs", 1)
        assert result.allowed is True
        assert result.used == 5
        assert result.limit == 10

    def test_at_limit_allowed(self):
        mgr = self._mgr_with_rule(10)
        mgr.increment("user:alice", "docs", 10)
        result = mgr.check("user:alice", "docs", 0)
        assert result.allowed is True

    def test_exactly_fills_limit_allowed(self):
        mgr = self._mgr_with_rule(10)
        mgr.increment("user:alice", "docs", 9)
        result = mgr.check("user:alice", "docs", 1)
        assert result.allowed is True

    def test_over_limit_denied(self):
        mgr = self._mgr_with_rule(10)
        mgr.increment("user:alice", "docs", 10)
        result = mgr.check("user:alice", "docs", 1)
        assert result.allowed is False
        assert "exceeded" in result.reason

    def test_no_rule_allowed(self):
        mgr = DocQuotaManager()
        result = mgr.check("user:alice", "docs", 99)
        assert result.allowed is True
        assert result.limit == 0

    def test_wildcard_fallback_allowed(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="global", subject="*", resource="docs", limit=100))
        mgr.increment("user:newbie", "docs", 5)
        result = mgr.check("user:newbie", "docs", 1)
        assert result.allowed is True
        assert result.limit == 100

    def test_wildcard_fallback_denied(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="global", subject="*", resource="docs", limit=5))
        mgr.increment("user:newbie", "docs", 5)
        result = mgr.check("user:newbie", "docs", 1)
        assert result.allowed is False

    def test_exact_subject_overrides_wildcard(self):
        mgr = DocQuotaManager()
        # Wildcard is restrictive; exact rule is generous
        mgr.set_rule(QuotaRule(rule_id="global", subject="*", resource="docs", limit=5))
        mgr.set_rule(QuotaRule(rule_id="vip", subject="user:alice", resource="docs", limit=1000))
        mgr.increment("user:alice", "docs", 500)
        result = mgr.check("user:alice", "docs", 1)
        assert result.allowed is True
        assert result.limit == 1000

    def test_result_subject_and_resource_echoed(self):
        mgr = DocQuotaManager()
        result = mgr.check("user:alice", "api_calls", 5)
        assert result.subject == "user:alice"
        assert result.resource == "api_calls"

    def test_reason_non_empty(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=10))
        result = mgr.check("user:alice", "docs", 1)
        assert result.reason != ""


# ---------------------------------------------------------------------------
# TestUsageSnapshot
# ---------------------------------------------------------------------------


class TestUsageSnapshot:
    def test_remaining_calculation(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=100))
        mgr.increment("user:alice", "docs", 40)
        snap = mgr.usage_snapshot("user:alice", "docs")
        assert snap.used == 40
        assert snap.limit == 100
        assert snap.remaining == 60
        assert snap.exceeded is False

    def test_exceeded_flag_set(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=10))
        mgr.increment("user:alice", "docs", 15)
        snap = mgr.usage_snapshot("user:alice", "docs")
        assert snap.exceeded is True
        assert snap.remaining == 0

    def test_no_rule_gives_zero_limit(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 5)
        snap = mgr.usage_snapshot("user:alice", "docs")
        assert snap.limit == 0
        assert snap.exceeded is False

    def test_wildcard_rule_used_in_snapshot(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="global", subject="*", resource="docs", limit=50))
        mgr.increment("user:newbie", "docs", 20)
        snap = mgr.usage_snapshot("user:newbie", "docs")
        assert snap.limit == 50
        assert snap.remaining == 30


# ---------------------------------------------------------------------------
# TestAllSubjects
# ---------------------------------------------------------------------------


class TestAllSubjects:
    def test_sorted_order(self):
        mgr = DocQuotaManager()
        mgr.increment("user:charlie", "docs")
        mgr.increment("user:alice", "docs")
        mgr.increment("user:bob", "docs")
        assert mgr.all_subjects() == ["user:alice", "user:bob", "user:charlie"]

    def test_unique_subjects(self):
        mgr = DocQuotaManager()
        mgr.increment("user:alice", "docs", 3)
        mgr.increment("user:alice", "storage_mb", 10)
        assert mgr.all_subjects() == ["user:alice"]

    def test_empty_when_no_usage(self):
        mgr = DocQuotaManager()
        assert mgr.all_subjects() == []


# ---------------------------------------------------------------------------
# TestExceededSubjects
# ---------------------------------------------------------------------------


class TestExceededSubjects:
    def test_returns_only_exceeded(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=10))
        mgr.set_rule(QuotaRule(rule_id="r2", subject="user:bob", resource="docs", limit=10))
        mgr.increment("user:alice", "docs", 15)  # exceeded
        mgr.increment("user:bob", "docs", 5)     # within limit
        assert mgr.exceeded_subjects() == ["user:alice"]

    def test_no_exceeded_returns_empty(self):
        mgr = DocQuotaManager()
        mgr.set_rule(QuotaRule(rule_id="r1", subject="user:alice", resource="docs", limit=100))
        mgr.increment("user:alice", "docs", 10)
        assert mgr.exceeded_subjects() == []

    def test_sorted_order(self):
        mgr = DocQuotaManager()
        for uid in ["user:charlie", "user:alice", "user:bob"]:
            mgr.set_rule(QuotaRule(rule_id=f"r-{uid}", subject=uid, resource="docs", limit=1))
            mgr.increment(uid, "docs", 5)
        exceeded = mgr.exceeded_subjects()
        assert exceeded == ["user:alice", "user:bob", "user:charlie"]

    def test_no_rule_subject_not_in_exceeded(self):
        mgr = DocQuotaManager()
        mgr.increment("user:nolimit", "docs", 9999)
        assert "user:nolimit" not in mgr.exceeded_subjects()


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_increment(self):
        mgr = DocQuotaManager()
        threads = []
        iterations = 100

        def worker():
            for _ in range(iterations):
                mgr.increment("user:shared", "docs")

        num_threads = 20
        for _ in range(num_threads):
            t = threading.Thread(target=worker)
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        expected = num_threads * iterations
        assert mgr.get_usage("user:shared", "docs") == expected

    def test_concurrent_set_rule_and_check(self):
        """set_rule and check can run concurrently without error."""
        mgr = DocQuotaManager()
        errors: list[Exception] = []

        def setter():
            for i in range(50):
                mgr.set_rule(
                    QuotaRule(rule_id=f"r{i % 5}", subject="u", resource="docs", limit=100 + i)
                )

        def checker():
            for _ in range(50):
                try:
                    mgr.check("u", "docs", 1)
                except Exception as exc:  # noqa: BLE001
                    errors.append(exc)

        threads = [threading.Thread(target=setter) for _ in range(5)]
        threads += [threading.Thread(target=checker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
