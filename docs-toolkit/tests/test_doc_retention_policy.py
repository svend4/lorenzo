"""Tests for docstoolkit.doc_retention_policy (E299)."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_retention_policy import (
    DocRetentionPolicy,
    PolicyStats,
    RetentionResult,
    RetentionRule,
)


# ======================================================================== #
# TestRetentionRuleDataclass
# ======================================================================== #


class TestRetentionRuleDataclass:
    def test_required_fields(self):
        rule = RetentionRule(rule_id="r1", pattern="*")
        assert rule.rule_id == "r1"
        assert rule.pattern == "*"

    def test_defaults(self):
        rule = RetentionRule(rule_id="r1", pattern="*")
        assert rule.ttl_seconds is None
        assert rule.keep_versions is None
        assert rule.priority == 0

    def test_all_fields(self):
        rule = RetentionRule(
            rule_id="r2",
            pattern="doc:*",
            ttl_seconds=3600.0,
            keep_versions=5,
            priority=10,
        )
        assert rule.rule_id == "r2"
        assert rule.pattern == "doc:*"
        assert rule.ttl_seconds == 3600.0
        assert rule.keep_versions == 5
        assert rule.priority == 10

    def test_ttl_none_means_no_expiry(self):
        rule = RetentionRule(rule_id="r3", pattern="*", ttl_seconds=None)
        assert rule.ttl_seconds is None

    def test_priority_negative(self):
        rule = RetentionRule(rule_id="r4", pattern="*", priority=-1)
        assert rule.priority == -1


# ======================================================================== #
# TestRetentionResultDataclass
# ======================================================================== #


class TestRetentionResultDataclass:
    def test_all_fields(self):
        result = RetentionResult(
            doc_id="doc1",
            rule_id="r1",
            expired=True,
            versions_to_delete=3,
            reason="expired",
        )
        assert result.doc_id == "doc1"
        assert result.rule_id == "r1"
        assert result.expired is True
        assert result.versions_to_delete == 3
        assert result.reason == "expired"

    def test_no_rule_applied(self):
        result = RetentionResult(
            doc_id="doc2",
            rule_id=None,
            expired=False,
            versions_to_delete=0,
            reason="no matching rule",
        )
        assert result.rule_id is None
        assert result.expired is False

    def test_zero_versions_to_delete(self):
        result = RetentionResult(
            doc_id="doc3",
            rule_id="r1",
            expired=False,
            versions_to_delete=0,
            reason="ok",
        )
        assert result.versions_to_delete == 0


# ======================================================================== #
# TestPolicyStatsDataclass
# ======================================================================== #


class TestPolicyStatsDataclass:
    def test_all_fields(self):
        ps = PolicyStats(total_rules=3, docs_tracked=10, expired_count=2)
        assert ps.total_rules == 3
        assert ps.docs_tracked == 10
        assert ps.expired_count == 2

    def test_zero_values(self):
        ps = PolicyStats(total_rules=0, docs_tracked=0, expired_count=0)
        assert ps.total_rules == 0
        assert ps.docs_tracked == 0
        assert ps.expired_count == 0


# ======================================================================== #
# TestConstruction
# ======================================================================== #


class TestConstruction:
    def test_empty_policy(self):
        p = DocRetentionPolicy()
        assert p.list_rules() == []

    def test_initial_stats(self):
        p = DocRetentionPolicy()
        s = p.stats()
        assert s.total_rules == 0
        assert s.docs_tracked == 0
        assert s.expired_count == 0

    def test_evaluate_all_empty(self):
        p = DocRetentionPolicy()
        assert p.evaluate_all() == []


# ======================================================================== #
# TestAddRule
# ======================================================================== #


class TestAddRule:
    def test_add_new_rule(self):
        p = DocRetentionPolicy()
        rule = RetentionRule(rule_id="r1", pattern="*")
        p.add_rule(rule)
        assert p.get_rule("r1") is rule

    def test_replace_same_id(self):
        p = DocRetentionPolicy()
        r1 = RetentionRule(rule_id="r1", pattern="*", ttl_seconds=60.0)
        r2 = RetentionRule(rule_id="r1", pattern="docs:*", ttl_seconds=120.0)
        p.add_rule(r1)
        p.add_rule(r2)
        assert p.get_rule("r1") is r2
        assert len(p.list_rules()) == 1

    def test_add_multiple_rules(self):
        p = DocRetentionPolicy()
        for i in range(5):
            p.add_rule(RetentionRule(rule_id=f"r{i}", pattern="*"))
        assert len(p.list_rules()) == 5

    def test_priority_preserved(self):
        p = DocRetentionPolicy()
        rule = RetentionRule(rule_id="r1", pattern="*", priority=99)
        p.add_rule(rule)
        assert p.get_rule("r1").priority == 99


# ======================================================================== #
# TestRemoveRule
# ======================================================================== #


class TestRemoveRule:
    def test_returns_true_when_existed(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*"))
        assert p.remove_rule("r1") is True

    def test_returns_false_when_not_existed(self):
        p = DocRetentionPolicy()
        assert p.remove_rule("missing") is False

    def test_rule_gone_after_remove(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*"))
        p.remove_rule("r1")
        assert p.get_rule("r1") is None

    def test_remove_reduces_count(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*"))
        p.add_rule(RetentionRule(rule_id="r2", pattern="*"))
        p.remove_rule("r1")
        assert len(p.list_rules()) == 1


# ======================================================================== #
# TestGetRule
# ======================================================================== #


class TestGetRule:
    def test_found(self):
        p = DocRetentionPolicy()
        rule = RetentionRule(rule_id="r1", pattern="*")
        p.add_rule(rule)
        assert p.get_rule("r1") is rule

    def test_not_found(self):
        p = DocRetentionPolicy()
        assert p.get_rule("nonexistent") is None

    def test_not_found_after_remove(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*"))
        p.remove_rule("r1")
        assert p.get_rule("r1") is None


# ======================================================================== #
# TestListRules
# ======================================================================== #


class TestListRules:
    def test_empty(self):
        p = DocRetentionPolicy()
        assert p.list_rules() == []

    def test_sorted_by_priority_desc(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="low", pattern="*", priority=1))
        p.add_rule(RetentionRule(rule_id="high", pattern="*", priority=10))
        p.add_rule(RetentionRule(rule_id="mid", pattern="*", priority=5))
        rules = p.list_rules()
        assert [r.rule_id for r in rules] == ["high", "mid", "low"]

    def test_tie_broken_by_rule_id(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="b_rule", pattern="*", priority=5))
        p.add_rule(RetentionRule(rule_id="a_rule", pattern="*", priority=5))
        rules = p.list_rules()
        assert rules[0].rule_id == "a_rule"
        assert rules[1].rule_id == "b_rule"

    def test_returns_copy_list(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*"))
        lst = p.list_rules()
        assert isinstance(lst, list)


# ======================================================================== #
# TestRegisterDoc
# ======================================================================== #


class TestRegisterDoc:
    def test_new_doc(self):
        p = DocRetentionPolicy()
        p.register_doc("doc1", created_at=1000.0)
        assert p.stats().docs_tracked == 1

    def test_update_doc(self):
        p = DocRetentionPolicy()
        p.register_doc("doc1", created_at=1000.0, version_count=1)
        p.register_doc("doc1", created_at=1000.0, version_count=5)
        # Only one entry for same doc_id
        assert p.stats().docs_tracked == 1

    def test_version_count_default(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", keep_versions=3))
        p.register_doc("doc1", created_at=0.0)  # version_count defaults to 1
        result = p.evaluate("doc1", now=0.0)
        assert result.versions_to_delete == 0

    def test_multiple_docs(self):
        p = DocRetentionPolicy()
        p.register_doc("doc1", created_at=1000.0)
        p.register_doc("doc2", created_at=2000.0)
        assert p.stats().docs_tracked == 2

    def test_now_parameter_accepted(self):
        # Should not raise
        p = DocRetentionPolicy()
        p.register_doc("doc1", created_at=0.0, version_count=1, now=500.0)
        assert p.stats().docs_tracked == 1


# ======================================================================== #
# TestEvaluateNoRule
# ======================================================================== #


class TestEvaluateNoRule:
    def test_no_rules_returns_no_match(self):
        p = DocRetentionPolicy()
        p.register_doc("doc1", created_at=0.0)
        result = p.evaluate("doc1", now=9999.0)
        assert result.rule_id is None
        assert result.expired is False
        assert result.versions_to_delete == 0
        assert result.reason == "no matching rule"

    def test_unregistered_doc_no_match(self):
        p = DocRetentionPolicy()
        result = p.evaluate("ghost", now=0.0)
        assert result.rule_id is None
        assert result.expired is False

    def test_reason_text(self):
        p = DocRetentionPolicy()
        result = p.evaluate("doc1", now=0.0)
        assert "no matching rule" in result.reason


# ======================================================================== #
# TestEvaluateTTL
# ======================================================================== #


class TestEvaluateTTL:
    def _policy_with_ttl(self, ttl: float) -> DocRetentionPolicy:
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", ttl_seconds=ttl))
        return p

    def test_not_expired(self):
        p = self._policy_with_ttl(100.0)
        p.register_doc("doc1", created_at=0.0)
        result = p.evaluate("doc1", now=50.0)
        assert result.expired is False

    def test_just_expired(self):
        p = self._policy_with_ttl(100.0)
        p.register_doc("doc1", created_at=0.0)
        result = p.evaluate("doc1", now=101.0)
        assert result.expired is True

    def test_exact_boundary_not_expired(self):
        # age == ttl_seconds is NOT expired (strict >)
        p = self._policy_with_ttl(100.0)
        p.register_doc("doc1", created_at=0.0)
        result = p.evaluate("doc1", now=100.0)
        assert result.expired is False

    def test_no_ttl_rule_never_expires(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", ttl_seconds=None))
        p.register_doc("doc1", created_at=0.0)
        result = p.evaluate("doc1", now=1_000_000.0)
        assert result.expired is False

    def test_expired_reason_contains_info(self):
        p = self._policy_with_ttl(10.0)
        p.register_doc("doc1", created_at=0.0)
        result = p.evaluate("doc1", now=20.0)
        assert result.expired is True
        assert "expired" in result.reason


# ======================================================================== #
# TestEvaluateKeepVersions
# ======================================================================== #


class TestEvaluateKeepVersions:
    def test_under_limit(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", keep_versions=5))
        p.register_doc("doc1", created_at=0.0, version_count=3)
        result = p.evaluate("doc1", now=0.0)
        assert result.versions_to_delete == 0

    def test_at_limit(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", keep_versions=5))
        p.register_doc("doc1", created_at=0.0, version_count=5)
        result = p.evaluate("doc1", now=0.0)
        assert result.versions_to_delete == 0

    def test_over_limit(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", keep_versions=3))
        p.register_doc("doc1", created_at=0.0, version_count=7)
        result = p.evaluate("doc1", now=0.0)
        assert result.versions_to_delete == 4

    def test_keep_versions_none_never_deletes(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", keep_versions=None))
        p.register_doc("doc1", created_at=0.0, version_count=1000)
        result = p.evaluate("doc1", now=0.0)
        assert result.versions_to_delete == 0

    def test_excess_versions_in_reason(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", keep_versions=2))
        p.register_doc("doc1", created_at=0.0, version_count=5)
        result = p.evaluate("doc1", now=0.0)
        assert result.versions_to_delete == 3
        assert "3" in result.reason


# ======================================================================== #
# TestEvaluatePatternMatching
# ======================================================================== #


class TestEvaluatePatternMatching:
    def test_exact_match(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="exact", pattern="doc-123", ttl_seconds=10.0))
        p.register_doc("doc-123", created_at=0.0)
        result = p.evaluate("doc-123", now=0.0)
        assert result.rule_id == "exact"

    def test_exact_match_no_false_positive(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="exact", pattern="doc-123", ttl_seconds=10.0))
        p.register_doc("doc-456", created_at=0.0)
        result = p.evaluate("doc-456", now=0.0)
        assert result.rule_id is None

    def test_wildcard_star_matches_all(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="all", pattern="*", ttl_seconds=10.0))
        for doc_id in ["alpha", "beta", "gamma"]:
            p.register_doc(doc_id, created_at=0.0)
            result = p.evaluate(doc_id, now=0.0)
            assert result.rule_id == "all"

    def test_prefix_wildcard(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="pfx", pattern="archive:*", ttl_seconds=5.0))
        p.register_doc("archive:2024-01", created_at=0.0)
        p.register_doc("live:doc", created_at=0.0)
        assert p.evaluate("archive:2024-01", now=0.0).rule_id == "pfx"
        assert p.evaluate("live:doc", now=0.0).rule_id is None

    def test_higher_priority_wins(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="low", pattern="*", priority=1, ttl_seconds=100.0))
        p.add_rule(RetentionRule(rule_id="high", pattern="doc-*", priority=10, ttl_seconds=5.0))
        p.register_doc("doc-abc", created_at=0.0)
        result = p.evaluate("doc-abc", now=0.0)
        assert result.rule_id == "high"

    def test_lower_priority_fallback(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="fallback", pattern="*", priority=1, ttl_seconds=999.0))
        p.add_rule(RetentionRule(rule_id="specific", pattern="archive:*", priority=5, ttl_seconds=1.0))
        p.register_doc("other:doc", created_at=0.0)
        result = p.evaluate("other:doc", now=0.0)
        assert result.rule_id == "fallback"

    def test_priority_tie_broken_by_rule_id(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="b_rule", pattern="*", priority=5))
        p.add_rule(RetentionRule(rule_id="a_rule", pattern="*", priority=5))
        p.register_doc("doc1", created_at=0.0)
        result = p.evaluate("doc1", now=0.0)
        # "a_rule" < "b_rule" lexicographically, so it wins the tie-break
        assert result.rule_id == "a_rule"


# ======================================================================== #
# TestEvaluateAll
# ======================================================================== #


class TestEvaluateAll:
    def test_evaluates_all_docs(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", ttl_seconds=50.0))
        for i in range(4):
            p.register_doc(f"doc{i}", created_at=0.0)
        results = p.evaluate_all(now=100.0)
        assert len(results) == 4

    def test_sorted_by_doc_id(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*"))
        for doc_id in ["z_doc", "a_doc", "m_doc"]:
            p.register_doc(doc_id, created_at=0.0)
        results = p.evaluate_all(now=0.0)
        assert [r.doc_id for r in results] == ["a_doc", "m_doc", "z_doc"]

    def test_empty_when_no_docs(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*"))
        assert p.evaluate_all() == []

    def test_mixed_expired(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", ttl_seconds=10.0))
        p.register_doc("doc_old", created_at=0.0)
        p.register_doc("doc_new", created_at=999.0)
        results = p.evaluate_all(now=1000.0)
        expired_ids = {r.doc_id for r in results if r.expired}
        fresh_ids = {r.doc_id for r in results if not r.expired}
        assert "doc_old" in expired_ids
        assert "doc_new" in fresh_ids


# ======================================================================== #
# TestApplyTTL
# ======================================================================== #


class TestApplyTTL:
    def test_not_expired(self):
        p = DocRetentionPolicy()
        assert p.apply_ttl("doc1", created_at=0.0, ttl_seconds=100.0, now=50.0) is False

    def test_expired(self):
        p = DocRetentionPolicy()
        assert p.apply_ttl("doc1", created_at=0.0, ttl_seconds=100.0, now=200.0) is True

    def test_exact_boundary(self):
        # age == ttl is NOT expired (strict >)
        p = DocRetentionPolicy()
        assert p.apply_ttl("doc1", created_at=0.0, ttl_seconds=100.0, now=100.0) is False

    def test_one_second_over(self):
        p = DocRetentionPolicy()
        assert p.apply_ttl("doc1", created_at=0.0, ttl_seconds=100.0, now=100.001) is True

    def test_injectable_now(self):
        p = DocRetentionPolicy()
        result = p.apply_ttl("doc1", created_at=1000.0, ttl_seconds=60.0, now=1070.0)
        assert result is True

    def test_no_state_change(self):
        p = DocRetentionPolicy()
        p.apply_ttl("doc1", created_at=0.0, ttl_seconds=10.0, now=999.0)
        assert p.stats().docs_tracked == 0


# ======================================================================== #
# TestStats
# ======================================================================== #


class TestStats:
    def test_empty_stats(self):
        p = DocRetentionPolicy()
        s = p.stats()
        assert s.total_rules == 0
        assert s.docs_tracked == 0
        assert s.expired_count == 0

    def test_total_rules(self):
        p = DocRetentionPolicy()
        for i in range(3):
            p.add_rule(RetentionRule(rule_id=f"r{i}", pattern="*"))
        assert p.stats().total_rules == 3

    def test_docs_tracked(self):
        p = DocRetentionPolicy()
        for i in range(4):
            p.register_doc(f"doc{i}", created_at=0.0)
        assert p.stats().docs_tracked == 4

    def test_expired_count_zero_no_ttl(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*"))
        p.register_doc("doc1", created_at=0.0)
        assert p.stats().expired_count == 0

    def test_expired_count_with_ttl(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*", ttl_seconds=1.0))
        # Register old doc (created far in the past)
        past = time.time() - 1000.0
        p.register_doc("old_doc", created_at=past)
        p.register_doc("new_doc", created_at=time.time())
        s = p.stats()
        assert s.expired_count >= 1

    def test_stats_after_rule_removal(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="r1", pattern="*"))
        p.add_rule(RetentionRule(rule_id="r2", pattern="*"))
        p.remove_rule("r1")
        assert p.stats().total_rules == 1


# ======================================================================== #
# TestThreadSafety
# ======================================================================== #


class TestThreadSafety:
    def test_concurrent_add_rule(self):
        p = DocRetentionPolicy()
        errors: list[Exception] = []

        def add_rules(start: int) -> None:
            try:
                for i in range(start, start + 50):
                    p.add_rule(RetentionRule(rule_id=f"r{i}", pattern="*"))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=add_rules, args=(i * 50,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(p.list_rules()) == 200

    def test_concurrent_register_doc(self):
        p = DocRetentionPolicy()
        errors: list[Exception] = []

        def register(start: int) -> None:
            try:
                for i in range(start, start + 100):
                    p.register_doc(f"doc{i}", created_at=float(i))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=register, args=(i * 100,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert p.stats().docs_tracked == 400

    def test_concurrent_add_and_evaluate(self):
        p = DocRetentionPolicy()
        p.add_rule(RetentionRule(rule_id="base", pattern="*", ttl_seconds=9999.0))
        errors: list[Exception] = []

        def adder() -> None:
            try:
                for i in range(50):
                    p.add_rule(RetentionRule(rule_id=f"dyn{i}", pattern=f"dyn{i}:*"))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def evaluator() -> None:
            try:
                for i in range(50):
                    p.register_doc(f"doc{i}", created_at=0.0)
                    p.evaluate(f"doc{i}", now=0.0)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = (
            [threading.Thread(target=adder) for _ in range(2)]
            + [threading.Thread(target=evaluator) for _ in range(2)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
