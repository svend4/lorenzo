"""Tests for E365 DocPinningPolicy."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_pinning_policy import (
    DocPinningPolicy,
    PinPolicyResult,
    PinPolicyRule,
    PinPolicyStats,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestPinPolicyRuleDataclass:
    def test_minimal_construction(self):
        rule = PinPolicyRule(rule_id="r1", pattern="*")
        assert rule.rule_id == "r1"
        assert rule.pattern == "*"

    def test_defaults(self):
        rule = PinPolicyRule(rule_id="r1", pattern="*")
        assert rule.auto_pin is False
        assert rule.max_pinned is None
        assert rule.priority == 0
        assert rule.description == ""

    def test_full_construction(self):
        rule = PinPolicyRule(
            rule_id="r1",
            pattern="prefix:*",
            auto_pin=True,
            max_pinned=10,
            priority=5,
            description="desc",
        )
        assert rule.auto_pin is True
        assert rule.max_pinned == 10
        assert rule.priority == 5
        assert rule.description == "desc"

    def test_equality(self):
        a = PinPolicyRule(rule_id="r1", pattern="*")
        b = PinPolicyRule(rule_id="r1", pattern="*")
        assert a == b

    def test_inequality(self):
        a = PinPolicyRule(rule_id="r1", pattern="*")
        b = PinPolicyRule(rule_id="r2", pattern="*")
        assert a != b


class TestPinPolicyResultDataclass:
    def test_construction(self):
        r = PinPolicyResult(
            doc_id="d1", matched_rule="r1", auto_pin=True, max_pinned=5, reason="ok"
        )
        assert r.doc_id == "d1"
        assert r.matched_rule == "r1"
        assert r.auto_pin is True
        assert r.max_pinned == 5
        assert r.reason == "ok"

    def test_no_match(self):
        r = PinPolicyResult(
            doc_id="d1", matched_rule=None, auto_pin=False, max_pinned=None, reason="x"
        )
        assert r.matched_rule is None
        assert r.max_pinned is None

    def test_equality(self):
        a = PinPolicyResult("d", None, False, None, "x")
        b = PinPolicyResult("d", None, False, None, "x")
        assert a == b


class TestPinPolicyStatsDataclass:
    def test_construction(self):
        s = PinPolicyStats(total_rules=3, auto_pin_rules=1, unique_patterns=2)
        assert s.total_rules == 3
        assert s.auto_pin_rules == 1
        assert s.unique_patterns == 2

    def test_zeros(self):
        s = PinPolicyStats(0, 0, 0)
        assert s.total_rules == 0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_policy(self):
        p = DocPinningPolicy()
        assert p.list_rules() == []

    def test_stats_empty(self):
        p = DocPinningPolicy()
        s = p.stats()
        assert s.total_rules == 0
        assert s.auto_pin_rules == 0
        assert s.unique_patterns == 0

    def test_independent_instances(self):
        p1 = DocPinningPolicy()
        p2 = DocPinningPolicy()
        p1.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        assert p2.list_rules() == []


# ---------------------------------------------------------------------------
# add_rule
# ---------------------------------------------------------------------------


class TestAddRule:
    def test_add_new(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        assert len(p.list_rules()) == 1

    def test_add_multiple(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="a:*"))
        p.add_rule(PinPolicyRule(rule_id="r2", pattern="b:*"))
        assert len(p.list_rules()) == 2

    def test_replace_existing(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="a:*"))
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="b:*"))
        rules = p.list_rules()
        assert len(rules) == 1
        assert rules[0].pattern == "b:*"

    def test_replace_preserves_id(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="a:*", auto_pin=True))
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="a:*", auto_pin=False))
        assert p.get_rule("r1").auto_pin is False


# ---------------------------------------------------------------------------
# remove_rule
# ---------------------------------------------------------------------------


class TestRemoveRule:
    def test_remove_existing_returns_true(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        assert p.remove_rule("r1") is True

    def test_remove_missing_returns_false(self):
        p = DocPinningPolicy()
        assert p.remove_rule("nope") is False

    def test_remove_actually_removes(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        p.remove_rule("r1")
        assert p.get_rule("r1") is None

    def test_remove_one_keeps_others(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="a:*"))
        p.add_rule(PinPolicyRule(rule_id="r2", pattern="b:*"))
        p.remove_rule("r1")
        assert p.get_rule("r2") is not None


# ---------------------------------------------------------------------------
# get_rule
# ---------------------------------------------------------------------------


class TestGetRule:
    def test_get_existing(self):
        p = DocPinningPolicy()
        rule = PinPolicyRule(rule_id="r1", pattern="a:*", priority=3)
        p.add_rule(rule)
        got = p.get_rule("r1")
        assert got == rule

    def test_get_missing(self):
        p = DocPinningPolicy()
        assert p.get_rule("missing") is None

    def test_get_after_remove(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        p.remove_rule("r1")
        assert p.get_rule("r1") is None


# ---------------------------------------------------------------------------
# list_rules
# ---------------------------------------------------------------------------


class TestListRules:
    def test_empty(self):
        p = DocPinningPolicy()
        assert p.list_rules() == []

    def test_sorted_by_priority_desc(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="low", pattern="*", priority=1))
        p.add_rule(PinPolicyRule(rule_id="high", pattern="*", priority=10))
        p.add_rule(PinPolicyRule(rule_id="mid", pattern="*", priority=5))
        ids = [r.rule_id for r in p.list_rules()]
        assert ids == ["high", "mid", "low"]

    def test_ties_broken_by_rule_id_asc(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="b", pattern="*", priority=1))
        p.add_rule(PinPolicyRule(rule_id="a", pattern="*", priority=1))
        p.add_rule(PinPolicyRule(rule_id="c", pattern="*", priority=1))
        ids = [r.rule_id for r in p.list_rules()]
        assert ids == ["a", "b", "c"]

    def test_returns_list(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        assert isinstance(p.list_rules(), list)


# ---------------------------------------------------------------------------
# evaluate
# ---------------------------------------------------------------------------


class TestEvaluate:
    def test_exact_match(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="doc:1", auto_pin=True))
        result = p.evaluate("doc:1")
        assert result.matched_rule == "r1"
        assert result.auto_pin is True

    def test_wildcard_match(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="prefix:*", auto_pin=True))
        result = p.evaluate("prefix:anything")
        assert result.matched_rule == "r1"

    def test_global_wildcard(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        result = p.evaluate("anything-at-all")
        assert result.matched_rule == "r1"

    def test_no_match(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="prefix:*"))
        result = p.evaluate("other:doc")
        assert result.matched_rule is None
        assert result.auto_pin is False
        assert result.max_pinned is None
        assert result.reason == "no matching rule"

    def test_empty_policy_no_match(self):
        p = DocPinningPolicy()
        result = p.evaluate("doc:1")
        assert result.matched_rule is None
        assert result.reason == "no matching rule"

    def test_result_doc_id(self):
        p = DocPinningPolicy()
        result = p.evaluate("xyz")
        assert result.doc_id == "xyz"

    def test_propagates_max_pinned(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*", max_pinned=7))
        result = p.evaluate("any")
        assert result.max_pinned == 7

    def test_reason_includes_rule_id(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="my-rule", pattern="*"))
        result = p.evaluate("any")
        assert "my-rule" in result.reason


class TestEvaluatePriority:
    def test_highest_priority_wins(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="low", pattern="*", priority=1, auto_pin=False))
        p.add_rule(PinPolicyRule(rule_id="high", pattern="*", priority=10, auto_pin=True))
        result = p.evaluate("doc:1")
        assert result.matched_rule == "high"
        assert result.auto_pin is True

    def test_specific_higher_priority_over_wildcard(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="wild", pattern="*", priority=1))
        p.add_rule(
            PinPolicyRule(rule_id="spec", pattern="prefix:*", priority=10, auto_pin=True)
        )
        result = p.evaluate("prefix:doc1")
        assert result.matched_rule == "spec"

    def test_only_matching_rules_considered(self):
        p = DocPinningPolicy()
        # High priority but doesn't match
        p.add_rule(PinPolicyRule(rule_id="hp", pattern="other:*", priority=100))
        # Lower priority but matches
        p.add_rule(PinPolicyRule(rule_id="lp", pattern="my:*", priority=1, auto_pin=True))
        result = p.evaluate("my:doc")
        assert result.matched_rule == "lp"

    def test_ties_resolved_by_rule_id(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="b", pattern="*", priority=5))
        p.add_rule(PinPolicyRule(rule_id="a", pattern="*", priority=5))
        result = p.evaluate("doc")
        assert result.matched_rule == "a"


# ---------------------------------------------------------------------------
# auto_pin_candidates
# ---------------------------------------------------------------------------


class TestAutoPinCandidates:
    def test_empty_input(self):
        p = DocPinningPolicy()
        assert p.auto_pin_candidates([]) == []

    def test_empty_policy(self):
        p = DocPinningPolicy()
        assert p.auto_pin_candidates(["a", "b"]) == []

    def test_returns_sorted(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*", auto_pin=True))
        result = p.auto_pin_candidates(["c", "a", "b"])
        assert result == ["a", "b", "c"]

    def test_filters_non_auto(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="auto:*", auto_pin=True))
        p.add_rule(PinPolicyRule(rule_id="r2", pattern="other:*", auto_pin=False))
        result = p.auto_pin_candidates(["auto:1", "other:1", "auto:2"])
        assert result == ["auto:1", "auto:2"]

    def test_filters_no_match(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="auto:*", auto_pin=True))
        result = p.auto_pin_candidates(["auto:1", "unmatched"])
        assert result == ["auto:1"]

    def test_priority_decides_auto_pin(self):
        p = DocPinningPolicy()
        # Higher priority disables auto-pin
        p.add_rule(PinPolicyRule(rule_id="block", pattern="x:*", priority=10, auto_pin=False))
        p.add_rule(PinPolicyRule(rule_id="allow", pattern="*", priority=1, auto_pin=True))
        result = p.auto_pin_candidates(["x:1", "y:1"])
        assert result == ["y:1"]


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_empty(self):
        p = DocPinningPolicy()
        assert p.clear() == 0

    def test_clear_returns_count(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        p.add_rule(PinPolicyRule(rule_id="r2", pattern="*"))
        p.add_rule(PinPolicyRule(rule_id="r3", pattern="*"))
        assert p.clear() == 3

    def test_clear_removes_all(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        p.clear()
        assert p.list_rules() == []

    def test_clear_then_add(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        p.clear()
        p.add_rule(PinPolicyRule(rule_id="r2", pattern="*"))
        assert len(p.list_rules()) == 1


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        p = DocPinningPolicy()
        s = p.stats()
        assert s == PinPolicyStats(0, 0, 0)

    def test_total_rules(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        p.add_rule(PinPolicyRule(rule_id="r2", pattern="a:*"))
        assert p.stats().total_rules == 2

    def test_auto_pin_count(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*", auto_pin=True))
        p.add_rule(PinPolicyRule(rule_id="r2", pattern="*", auto_pin=False))
        p.add_rule(PinPolicyRule(rule_id="r3", pattern="*", auto_pin=True))
        assert p.stats().auto_pin_rules == 2

    def test_unique_patterns(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="*"))
        p.add_rule(PinPolicyRule(rule_id="r2", pattern="*"))
        p.add_rule(PinPolicyRule(rule_id="r3", pattern="a:*"))
        assert p.stats().unique_patterns == 2

    def test_unique_patterns_all_distinct(self):
        p = DocPinningPolicy()
        p.add_rule(PinPolicyRule(rule_id="r1", pattern="a:*"))
        p.add_rule(PinPolicyRule(rule_id="r2", pattern="b:*"))
        p.add_rule(PinPolicyRule(rule_id="r3", pattern="c:*"))
        assert p.stats().unique_patterns == 3

    def test_returns_stats_dataclass(self):
        p = DocPinningPolicy()
        assert isinstance(p.stats(), PinPolicyStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_add_rule(self):
        p = DocPinningPolicy()
        N = 50
        T = 8

        def worker(start: int):
            for i in range(N):
                rid = f"t{start}-r{i}"
                p.add_rule(PinPolicyRule(rule_id=rid, pattern="*"))

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(T)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(p.list_rules()) == N * T

    def test_concurrent_add_and_remove(self):
        p = DocPinningPolicy()
        N = 30
        T = 4

        def adder(start: int):
            for i in range(N):
                p.add_rule(PinPolicyRule(rule_id=f"a{start}-{i}", pattern="*"))

        def remover(start: int):
            for i in range(N):
                p.remove_rule(f"a{start}-{i}")

        threads = []
        for t in range(T):
            threads.append(threading.Thread(target=adder, args=(t,)))
            threads.append(threading.Thread(target=remover, args=(t,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # No crashes, list_rules is callable
        rules = p.list_rules()
        assert isinstance(rules, list)

    def test_concurrent_clear(self):
        p = DocPinningPolicy()
        for i in range(20):
            p.add_rule(PinPolicyRule(rule_id=f"r{i}", pattern="*"))

        results = []
        lock = threading.Lock()

        def clearer():
            n = p.clear()
            with lock:
                results.append(n)

        threads = [threading.Thread(target=clearer) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Exactly one cleared everything; rest cleared 0
        assert sum(results) == 20
        assert p.list_rules() == []
