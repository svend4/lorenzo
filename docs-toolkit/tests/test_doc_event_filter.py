"""Tests for E380 DocEventFilter."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_event_filter import (
    DocEventFilter,
    FilterResult,
    FilterRule,
    FilterStats,
)


# --------------------------------------------------------------------- dataclasses
class TestFilterRuleDataclass:
    def test_minimal(self):
        rule = FilterRule(rule_id="r1")
        assert rule.rule_id == "r1"
        assert rule.event_type_pattern == "*"
        assert rule.doc_id_pattern == "*"
        assert rule.action == "allow"
        assert rule.priority == 0
        assert rule.enabled is True

    def test_full(self):
        rule = FilterRule(
            rule_id="r2",
            event_type_pattern="doc.*",
            doc_id_pattern="proj-*",
            action="block",
            priority=10,
            enabled=False,
        )
        assert rule.rule_id == "r2"
        assert rule.event_type_pattern == "doc.*"
        assert rule.doc_id_pattern == "proj-*"
        assert rule.action == "block"
        assert rule.priority == 10
        assert rule.enabled is False

    def test_equality(self):
        a = FilterRule(rule_id="x")
        b = FilterRule(rule_id="x")
        assert a == b

    def test_inequality(self):
        a = FilterRule(rule_id="x", priority=1)
        b = FilterRule(rule_id="x", priority=2)
        assert a != b


class TestFilterResultDataclass:
    def test_minimal(self):
        r = FilterResult(allowed=True)
        assert r.allowed is True
        assert r.matched_rule is None
        assert r.reason == ""

    def test_full(self):
        r = FilterResult(allowed=False, matched_rule="r1", reason="blocked")
        assert r.allowed is False
        assert r.matched_rule == "r1"
        assert r.reason == "blocked"

    def test_equality(self):
        assert FilterResult(True, "r", "x") == FilterResult(True, "r", "x")


class TestFilterStatsDataclass:
    def test_basic(self):
        s = FilterStats(
            total_rules=3,
            enabled_rules=2,
            total_evaluations=10,
            allowed_count=7,
            blocked_count=3,
        )
        assert s.total_rules == 3
        assert s.enabled_rules == 2
        assert s.total_evaluations == 10
        assert s.allowed_count == 7
        assert s.blocked_count == 3

    def test_equality(self):
        s1 = FilterStats(1, 1, 1, 1, 0)
        s2 = FilterStats(1, 1, 1, 1, 0)
        assert s1 == s2


# ------------------------------------------------------------------- construction
class TestConstruction:
    def test_default(self):
        f = DocEventFilter()
        assert f.list_rules() == []
        assert f.stats().total_rules == 0

    def test_allow_default(self):
        f = DocEventFilter(default_action="allow")
        res = f.evaluate("any", "doc")
        assert res.allowed is True

    def test_block_default(self):
        f = DocEventFilter(default_action="block")
        res = f.evaluate("any", "doc")
        assert res.allowed is False

    def test_invalid_default_raises(self):
        with pytest.raises(ValueError):
            DocEventFilter(default_action="maybe")

    def test_invalid_default_empty(self):
        with pytest.raises(ValueError):
            DocEventFilter(default_action="")


# ------------------------------------------------------------------------ add_rule
class TestAddRule:
    def test_add_one(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="r1"))
        assert f.get_rule("r1") is not None

    def test_add_multiple(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="a"))
        f.add_rule(FilterRule(rule_id="b"))
        f.add_rule(FilterRule(rule_id="c"))
        assert f.stats().total_rules == 3

    def test_replace_existing(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="r1", priority=1))
        f.add_rule(FilterRule(rule_id="r1", priority=5))
        assert f.get_rule("r1").priority == 5
        assert f.stats().total_rules == 1

    def test_add_invalid_action(self):
        f = DocEventFilter()
        with pytest.raises(ValueError):
            f.add_rule(FilterRule(rule_id="bad", action="meh"))

    def test_add_non_rule(self):
        f = DocEventFilter()
        with pytest.raises(TypeError):
            f.add_rule("not a rule")  # type: ignore[arg-type]


# --------------------------------------------------------------------- remove_rule
class TestRemoveRule:
    def test_remove_existing(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="r1"))
        assert f.remove_rule("r1") is True
        assert f.get_rule("r1") is None

    def test_remove_missing(self):
        f = DocEventFilter()
        assert f.remove_rule("missing") is False

    def test_remove_twice(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="r1"))
        assert f.remove_rule("r1") is True
        assert f.remove_rule("r1") is False


# ----------------------------------------------------------------- enable/disable
class TestEnableDisable:
    def test_disable(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="r1"))
        assert f.disable_rule("r1") is True
        assert f.get_rule("r1").enabled is False

    def test_enable(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="r1", enabled=False))
        assert f.enable_rule("r1") is True
        assert f.get_rule("r1").enabled is True

    def test_disable_missing(self):
        f = DocEventFilter()
        assert f.disable_rule("missing") is False

    def test_enable_missing(self):
        f = DocEventFilter()
        assert f.enable_rule("missing") is False

    def test_disabled_does_not_match(self):
        f = DocEventFilter(default_action="allow")
        f.add_rule(FilterRule(rule_id="block_all", action="block"))
        f.disable_rule("block_all")
        res = f.evaluate("any", "any")
        assert res.allowed is True
        assert res.matched_rule is None


# -------------------------------------------------------------------- get_rule
class TestGetRule:
    def test_get_existing(self):
        f = DocEventFilter()
        rule = FilterRule(rule_id="r1", priority=3)
        f.add_rule(rule)
        got = f.get_rule("r1")
        assert got is not None
        assert got.rule_id == "r1"
        assert got.priority == 3

    def test_get_missing(self):
        f = DocEventFilter()
        assert f.get_rule("missing") is None


# -------------------------------------------------------------------- list_rules
class TestListRules:
    def test_empty(self):
        f = DocEventFilter()
        assert f.list_rules() == []

    def test_sorted_by_priority_desc(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="low", priority=1))
        f.add_rule(FilterRule(rule_id="hi", priority=10))
        f.add_rule(FilterRule(rule_id="mid", priority=5))
        ids = [r.rule_id for r in f.list_rules()]
        assert ids == ["hi", "mid", "low"]

    def test_tiebreak_by_rule_id(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="zeta", priority=5))
        f.add_rule(FilterRule(rule_id="alpha", priority=5))
        f.add_rule(FilterRule(rule_id="mike", priority=5))
        ids = [r.rule_id for r in f.list_rules()]
        assert ids == ["alpha", "mike", "zeta"]


# --------------------------------------------------------------------- evaluate
class TestEvaluate:
    def test_match_allow(self):
        f = DocEventFilter(default_action="block")
        f.add_rule(FilterRule(rule_id="allow_all", action="allow"))
        res = f.evaluate("evt", "doc")
        assert res.allowed is True
        assert res.matched_rule == "allow_all"

    def test_match_block(self):
        f = DocEventFilter(default_action="allow")
        f.add_rule(FilterRule(rule_id="block_all", action="block"))
        res = f.evaluate("evt", "doc")
        assert res.allowed is False
        assert res.matched_rule == "block_all"

    def test_no_match_default_allow(self):
        f = DocEventFilter(default_action="allow")
        f.add_rule(
            FilterRule(
                rule_id="specific",
                event_type_pattern="never.*",
                doc_id_pattern="never.*",
                action="block",
            )
        )
        res = f.evaluate("evt", "doc")
        assert res.allowed is True
        assert res.matched_rule is None

    def test_no_match_default_block(self):
        f = DocEventFilter(default_action="block")
        res = f.evaluate("evt", "doc")
        assert res.allowed is False
        assert res.matched_rule is None

    def test_priority_order(self):
        f = DocEventFilter()
        f.add_rule(
            FilterRule(rule_id="low_block", action="block", priority=1)
        )
        f.add_rule(
            FilterRule(rule_id="high_allow", action="allow", priority=10)
        )
        res = f.evaluate("evt", "doc")
        assert res.matched_rule == "high_allow"
        assert res.allowed is True

    def test_disabled_skipped(self):
        f = DocEventFilter(default_action="allow")
        f.add_rule(
            FilterRule(
                rule_id="block_all",
                action="block",
                priority=100,
                enabled=False,
            )
        )
        res = f.evaluate("evt", "doc")
        assert res.allowed is True
        assert res.matched_rule is None

    def test_reason_populated(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="r1", action="block"))
        res = f.evaluate("evt", "doc")
        assert res.reason
        assert "r1" in res.reason

    def test_reason_when_default(self):
        f = DocEventFilter(default_action="block")
        res = f.evaluate("evt", "doc")
        assert res.reason
        assert "default" in res.reason.lower()

    def test_first_match_wins(self):
        f = DocEventFilter()
        f.add_rule(
            FilterRule(
                rule_id="a", action="allow", priority=5,
                event_type_pattern="x", doc_id_pattern="y",
            )
        )
        f.add_rule(
            FilterRule(
                rule_id="b", action="block", priority=5,
                event_type_pattern="x", doc_id_pattern="y",
            )
        )
        # Tie on priority — sorted by rule_id; "a" wins.
        res = f.evaluate("x", "y")
        assert res.matched_rule == "a"
        assert res.allowed is True


# ---------------------------------------------------------- pattern matching
class TestEvaluatePatterns:
    def test_event_type_wildcard(self):
        f = DocEventFilter(default_action="block")
        f.add_rule(
            FilterRule(
                rule_id="r1", event_type_pattern="doc.*", action="allow"
            )
        )
        assert f.evaluate("doc.created", "x").allowed is True
        assert f.evaluate("user.created", "x").allowed is False

    def test_doc_id_wildcard(self):
        f = DocEventFilter(default_action="block")
        f.add_rule(
            FilterRule(
                rule_id="r1", doc_id_pattern="proj-*", action="allow"
            )
        )
        assert f.evaluate("any", "proj-42").allowed is True
        assert f.evaluate("any", "other-42").allowed is False

    def test_both_patterns(self):
        f = DocEventFilter(default_action="block")
        f.add_rule(
            FilterRule(
                rule_id="r1",
                event_type_pattern="doc.*",
                doc_id_pattern="proj-*",
                action="allow",
            )
        )
        assert f.evaluate("doc.create", "proj-1").allowed is True
        assert f.evaluate("doc.create", "other-1").allowed is False
        assert f.evaluate("other", "proj-1").allowed is False

    def test_question_mark(self):
        f = DocEventFilter(default_action="block")
        f.add_rule(
            FilterRule(
                rule_id="r1", doc_id_pattern="doc?", action="allow"
            )
        )
        assert f.evaluate("e", "doc1").allowed is True
        assert f.evaluate("e", "doc12").allowed is False

    def test_charset_pattern(self):
        f = DocEventFilter(default_action="block")
        f.add_rule(
            FilterRule(
                rule_id="r1", doc_id_pattern="doc[0-9]", action="allow"
            )
        )
        assert f.evaluate("e", "doc5").allowed is True
        assert f.evaluate("e", "docX").allowed is False


# ---------------------------------------------------------------- filter_events
class TestFilterEvents:
    def test_empty_events(self):
        f = DocEventFilter()
        assert f.filter_events([]) == []

    def test_all_allowed_by_default(self):
        f = DocEventFilter(default_action="allow")
        events = [("e1", "d1", None), ("e2", "d2", {"a": 1})]
        assert f.filter_events(events) == events

    def test_blocking_rule(self):
        f = DocEventFilter(default_action="allow")
        f.add_rule(
            FilterRule(
                rule_id="b",
                event_type_pattern="del.*",
                action="block",
            )
        )
        events = [
            ("doc.created", "d1", None),
            ("del.doc", "d2", None),
            ("doc.updated", "d3", None),
        ]
        result = f.filter_events(events)
        assert result == [
            ("doc.created", "d1", None),
            ("doc.updated", "d3", None),
        ]

    def test_block_default_filters_all(self):
        f = DocEventFilter(default_action="block")
        assert f.filter_events([("e", "d", None)]) == []

    def test_payload_preserved(self):
        f = DocEventFilter()
        ev = ("e", "d", {"complex": [1, 2, 3]})
        assert f.filter_events([ev]) == [ev]

    def test_invalid_event_raises(self):
        f = DocEventFilter()
        with pytest.raises(ValueError):
            f.filter_events([("only_one",)])  # type: ignore[list-item]


# ------------------------------------------------------------------- clear_rules
class TestClearRules:
    def test_clear_empty(self):
        f = DocEventFilter()
        assert f.clear_rules() == 0

    def test_clear_returns_count(self):
        f = DocEventFilter()
        for i in range(5):
            f.add_rule(FilterRule(rule_id=f"r{i}"))
        assert f.clear_rules() == 5
        assert f.stats().total_rules == 0

    def test_clear_then_add(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="a"))
        f.clear_rules()
        f.add_rule(FilterRule(rule_id="b"))
        assert f.stats().total_rules == 1


# ------------------------------------------------------------- set_default_action
class TestSetDefaultAction:
    def test_to_block(self):
        f = DocEventFilter(default_action="allow")
        f.set_default_action("block")
        assert f.evaluate("e", "d").allowed is False

    def test_to_allow(self):
        f = DocEventFilter(default_action="block")
        f.set_default_action("allow")
        assert f.evaluate("e", "d").allowed is True

    def test_invalid_raises(self):
        f = DocEventFilter()
        with pytest.raises(ValueError):
            f.set_default_action("none")

    def test_invalid_empty_raises(self):
        f = DocEventFilter()
        with pytest.raises(ValueError):
            f.set_default_action("")


# ------------------------------------------------------------------------- stats
class TestStats:
    def test_initial(self):
        f = DocEventFilter()
        s = f.stats()
        assert s.total_rules == 0
        assert s.enabled_rules == 0
        assert s.total_evaluations == 0
        assert s.allowed_count == 0
        assert s.blocked_count == 0

    def test_after_adding(self):
        f = DocEventFilter()
        f.add_rule(FilterRule(rule_id="a"))
        f.add_rule(FilterRule(rule_id="b", enabled=False))
        s = f.stats()
        assert s.total_rules == 2
        assert s.enabled_rules == 1

    def test_counters_allow(self):
        f = DocEventFilter(default_action="allow")
        f.evaluate("e", "d")
        f.evaluate("e2", "d2")
        s = f.stats()
        assert s.total_evaluations == 2
        assert s.allowed_count == 2
        assert s.blocked_count == 0

    def test_counters_block(self):
        f = DocEventFilter(default_action="block")
        f.evaluate("e", "d")
        s = f.stats()
        assert s.total_evaluations == 1
        assert s.allowed_count == 0
        assert s.blocked_count == 1

    def test_counters_mixed(self):
        f = DocEventFilter(default_action="allow")
        f.add_rule(
            FilterRule(
                rule_id="b", event_type_pattern="bad.*", action="block"
            )
        )
        f.evaluate("good", "d")
        f.evaluate("bad.x", "d")
        f.evaluate("good", "d")
        s = f.stats()
        assert s.total_evaluations == 3
        assert s.allowed_count == 2
        assert s.blocked_count == 1


# ------------------------------------------------------------------- thread safety
class TestThreadSafety:
    def test_concurrent_evaluate(self):
        f = DocEventFilter(default_action="allow")
        f.add_rule(
            FilterRule(
                rule_id="block_x",
                event_type_pattern="x.*",
                action="block",
            )
        )

        errors: list[Exception] = []

        def worker(n: int) -> None:
            try:
                for i in range(200):
                    if (n + i) % 2 == 0:
                        f.evaluate("x.delete", f"doc-{i}")
                    else:
                        f.evaluate("y.create", f"doc-{i}")
            except Exception as exc:  # pragma: no cover - safety net
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        s = f.stats()
        assert s.total_evaluations == 8 * 200
        assert s.allowed_count + s.blocked_count == s.total_evaluations

    def test_concurrent_add_and_evaluate(self):
        f = DocEventFilter(default_action="allow")
        errors: list[Exception] = []

        def adder() -> None:
            try:
                for i in range(100):
                    f.add_rule(FilterRule(rule_id=f"r{i}", priority=i))
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        def evaluator() -> None:
            try:
                for i in range(200):
                    f.evaluate("evt", f"doc-{i}")
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [
            threading.Thread(target=adder),
            threading.Thread(target=evaluator),
            threading.Thread(target=adder),
            threading.Thread(target=evaluator),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        # All adds should have succeeded (idempotent on identical ids).
        assert f.stats().total_rules == 100
