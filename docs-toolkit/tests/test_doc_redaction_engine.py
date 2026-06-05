"""Tests for E327 DocRedactionEngine."""

from __future__ import annotations

import re
import threading

import pytest

from docstoolkit.doc_redaction_engine import (
    DocRedactionEngine,
    RedactionResult,
    RedactionRule,
    RedactionStats,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestRedactionRuleDataclass:
    def test_required_fields(self):
        r = RedactionRule(rule_id="r1", pattern=r"\d+")
        assert r.rule_id == "r1"
        assert r.pattern == r"\d+"

    def test_defaults(self):
        r = RedactionRule(rule_id="r1", pattern=r"\d+")
        assert r.replacement == "[REDACTED]"
        assert r.description == ""
        assert r.enabled is True

    def test_custom_values(self):
        r = RedactionRule(
            rule_id="r1",
            pattern=r"\d+",
            replacement="***",
            description="digits",
            enabled=False,
        )
        assert r.replacement == "***"
        assert r.description == "digits"
        assert r.enabled is False

    def test_equality(self):
        a = RedactionRule(rule_id="x", pattern="x")
        b = RedactionRule(rule_id="x", pattern="x")
        assert a == b

    def test_inequality(self):
        a = RedactionRule(rule_id="x", pattern="x")
        b = RedactionRule(rule_id="y", pattern="x")
        assert a != b


class TestRedactionResultDataclass:
    def test_required_fields(self):
        res = RedactionResult(original_length=10, redacted_length=8, redacted_text="ab")
        assert res.original_length == 10
        assert res.redacted_length == 8
        assert res.redacted_text == "ab"

    def test_defaults(self):
        res = RedactionResult(original_length=0, redacted_length=0, redacted_text="")
        assert res.applied_rules == []
        assert res.match_counts == {}

    def test_default_factory_independence(self):
        a = RedactionResult(original_length=0, redacted_length=0, redacted_text="")
        b = RedactionResult(original_length=0, redacted_length=0, redacted_text="")
        a.applied_rules.append("r1")
        a.match_counts["r1"] = 1
        assert b.applied_rules == []
        assert b.match_counts == {}

    def test_custom_values(self):
        res = RedactionResult(
            original_length=10,
            redacted_length=5,
            redacted_text="abcde",
            applied_rules=["r1"],
            match_counts={"r1": 2},
        )
        assert res.applied_rules == ["r1"]
        assert res.match_counts == {"r1": 2}


class TestRedactionStatsDataclass:
    def test_fields(self):
        s = RedactionStats(total_rules=3, enabled_rules=2, total_redactions_performed=5)
        assert s.total_rules == 3
        assert s.enabled_rules == 2
        assert s.total_redactions_performed == 5

    def test_equality(self):
        a = RedactionStats(total_rules=1, enabled_rules=1, total_redactions_performed=0)
        b = RedactionStats(total_rules=1, enabled_rules=1, total_redactions_performed=0)
        assert a == b


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_default_empty(self):
        e = DocRedactionEngine()
        assert e.list_rules() == []

    def test_stats_on_empty(self):
        e = DocRedactionEngine()
        s = e.stats()
        assert s.total_rules == 0
        assert s.enabled_rules == 0
        assert s.total_redactions_performed == 0

    def test_two_engines_independent(self):
        a = DocRedactionEngine()
        b = DocRedactionEngine()
        a.add_rule(RedactionRule(rule_id="r1", pattern="x"))
        assert b.list_rules() == []


# ---------------------------------------------------------------------------
# add_rule
# ---------------------------------------------------------------------------


class TestAddRule:
    def test_add_new(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        assert e.get_rule("r1") is not None

    def test_replace_existing(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+", replacement="A"))
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+", replacement="B"))
        assert e.get_rule("r1").replacement == "B"
        assert len(e.list_rules()) == 1

    def test_compiles_regex(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        # If regex is cached, test_pattern should work right away
        assert e.test_pattern("r1", "abc 123") == 1

    def test_invalid_pattern_raises(self):
        e = DocRedactionEngine()
        with pytest.raises(re.error):
            e.add_rule(RedactionRule(rule_id="bad", pattern="["))

    def test_multiple_rules(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        e.add_rule(RedactionRule(rule_id="r2", pattern=r"[a-z]+"))
        assert len(e.list_rules()) == 2


# ---------------------------------------------------------------------------
# remove_rule
# ---------------------------------------------------------------------------


class TestRemoveRule:
    def test_remove_existing(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern="x"))
        assert e.remove_rule("r1") is True
        assert e.get_rule("r1") is None

    def test_remove_unknown(self):
        e = DocRedactionEngine()
        assert e.remove_rule("nope") is False

    def test_remove_clears_compiled(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        e.remove_rule("r1")
        assert e.test_pattern("r1", "123") == 0

    def test_remove_one_keeps_others(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern="x"))
        e.add_rule(RedactionRule(rule_id="r2", pattern="y"))
        e.remove_rule("r1")
        assert [r.rule_id for r in e.list_rules()] == ["r2"]


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------


class TestEnableDisable:
    def test_disable_then_enable(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern="x"))
        assert e.disable_rule("r1") is True
        assert e.get_rule("r1").enabled is False
        assert e.enable_rule("r1") is True
        assert e.get_rule("r1").enabled is True

    def test_enable_unknown(self):
        e = DocRedactionEngine()
        assert e.enable_rule("nope") is False

    def test_disable_unknown(self):
        e = DocRedactionEngine()
        assert e.disable_rule("nope") is False

    def test_disabled_rule_skipped_in_redact(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        e.disable_rule("r1")
        res = e.redact("123")
        assert res.redacted_text == "123"
        assert res.applied_rules == []


# ---------------------------------------------------------------------------
# get_rule
# ---------------------------------------------------------------------------


class TestGetRule:
    def test_found(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern="x"))
        assert e.get_rule("r1").rule_id == "r1"

    def test_not_found(self):
        e = DocRedactionEngine()
        assert e.get_rule("nope") is None


# ---------------------------------------------------------------------------
# list_rules
# ---------------------------------------------------------------------------


class TestListRules:
    def test_empty(self):
        e = DocRedactionEngine()
        assert e.list_rules() == []

    def test_sorted_by_id(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="zeta", pattern="z"))
        e.add_rule(RedactionRule(rule_id="alpha", pattern="a"))
        e.add_rule(RedactionRule(rule_id="mu", pattern="m"))
        ids = [r.rule_id for r in e.list_rules()]
        assert ids == ["alpha", "mu", "zeta"]


# ---------------------------------------------------------------------------
# redact
# ---------------------------------------------------------------------------


class TestRedact:
    def test_single_rule(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="digits", pattern=r"\d+", replacement="#"))
        res = e.redact("abc 123 def")
        assert res.redacted_text == "abc # def"

    def test_multiple_rules(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="digits", pattern=r"\d+", replacement="#"))
        e.add_rule(RedactionRule(rule_id="vowels", pattern=r"[aeiou]", replacement="*"))
        res = e.redact("abc 12")
        assert "#" in res.redacted_text
        assert "*" in res.redacted_text

    def test_no_matches(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="digits", pattern=r"\d+"))
        res = e.redact("hello")
        assert res.redacted_text == "hello"
        assert res.applied_rules == []

    def test_disabled_rules_skipped(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+", replacement="#"))
        e.disable_rule("r1")
        res = e.redact("123")
        assert res.redacted_text == "123"

    def test_rule_ids_filter(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="digits", pattern=r"\d+", replacement="#"))
        e.add_rule(RedactionRule(rule_id="vowels", pattern=r"[aeiou]", replacement="*"))
        res = e.redact("abc 123", rule_ids=["digits"])
        assert res.redacted_text == "abc #"
        assert "vowels" not in res.applied_rules

    def test_rule_ids_filter_with_unknown(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="digits", pattern=r"\d+", replacement="#"))
        res = e.redact("abc 123", rule_ids=["digits", "nope"])
        assert res.redacted_text == "abc #"

    def test_lengths_recorded(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+", replacement="#"))
        res = e.redact("123456")
        assert res.original_length == 6
        assert res.redacted_length == 1

    def test_empty_text(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        res = e.redact("")
        assert res.original_length == 0
        assert res.redacted_length == 0
        assert res.redacted_text == ""
        assert res.applied_rules == []

    def test_no_rules(self):
        e = DocRedactionEngine()
        res = e.redact("hello world")
        assert res.redacted_text == "hello world"
        assert res.applied_rules == []
        assert res.match_counts == {}


# ---------------------------------------------------------------------------
# redact match counts
# ---------------------------------------------------------------------------


class TestRedactMatchCounts:
    def test_single_match_count(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        res = e.redact("abc 1 2 3")
        assert res.match_counts["r1"] == 3

    def test_zero_match_count_recorded(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        res = e.redact("hello")
        assert res.match_counts.get("r1", 0) == 0

    def test_multiple_rules_counts(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="digits", pattern=r"\d+"))
        e.add_rule(RedactionRule(rule_id="words", pattern=r"[a-z]+"))
        res = e.redact("a 1 b 2")
        assert res.match_counts["digits"] == 2
        assert res.match_counts["words"] == 2


# ---------------------------------------------------------------------------
# redact applied_rules
# ---------------------------------------------------------------------------


class TestRedactAppliedRules:
    def test_only_matched_rules(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="digits", pattern=r"\d+"))
        e.add_rule(RedactionRule(rule_id="xs", pattern=r"x+"))
        res = e.redact("abc 123")
        assert "digits" in res.applied_rules
        assert "xs" not in res.applied_rules

    def test_sorted(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="zeta", pattern=r"z"))
        e.add_rule(RedactionRule(rule_id="alpha", pattern=r"a"))
        e.add_rule(RedactionRule(rule_id="mu", pattern=r"m"))
        res = e.redact("a m z")
        assert res.applied_rules == ["alpha", "mu", "zeta"]

    def test_empty_when_no_matches(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"x"))
        res = e.redact("hello")
        assert res.applied_rules == []


# ---------------------------------------------------------------------------
# test_pattern
# ---------------------------------------------------------------------------


class TestTestPattern:
    def test_count_only(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        assert e.test_pattern("r1", "1 2 3") == 3

    def test_unknown_returns_zero(self):
        e = DocRedactionEngine()
        assert e.test_pattern("nope", "1 2 3") == 0

    def test_does_not_modify_text(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+", replacement="#"))
        original = "abc 123"
        e.test_pattern("r1", original)
        assert original == "abc 123"

    def test_does_not_count_in_total_redactions(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        e.test_pattern("r1", "123")
        assert e.stats().total_redactions_performed == 0

    def test_zero_when_no_match(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        assert e.test_pattern("r1", "hello") == 0


# ---------------------------------------------------------------------------
# clear_rules
# ---------------------------------------------------------------------------


class TestClearRules:
    def test_returns_count(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern="x"))
        e.add_rule(RedactionRule(rule_id="r2", pattern="y"))
        assert e.clear_rules() == 2

    def test_empty_after(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern="x"))
        e.clear_rules()
        assert e.list_rules() == []

    def test_empty_engine(self):
        e = DocRedactionEngine()
        assert e.clear_rules() == 0

    def test_compiled_cleared(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        e.clear_rules()
        assert e.test_pattern("r1", "123") == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_total_rules(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern="x"))
        e.add_rule(RedactionRule(rule_id="r2", pattern="y"))
        assert e.stats().total_rules == 2

    def test_enabled_rules(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern="x"))
        e.add_rule(RedactionRule(rule_id="r2", pattern="y"))
        e.disable_rule("r2")
        s = e.stats()
        assert s.total_rules == 2
        assert s.enabled_rules == 1

    def test_redactions_increment(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        e.redact("123")
        e.redact("456")
        e.redact("hello")
        assert e.stats().total_redactions_performed == 3

    def test_redactions_increment_even_without_matches(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+"))
        e.redact("hello")
        assert e.stats().total_redactions_performed == 1

    def test_redactions_increment_no_rules(self):
        e = DocRedactionEngine()
        e.redact("hello")
        assert e.stats().total_redactions_performed == 1

    def test_returns_redaction_stats_instance(self):
        e = DocRedactionEngine()
        assert isinstance(e.stats(), RedactionStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_add_rule(self):
        e = DocRedactionEngine()

        def worker(start: int) -> None:
            for i in range(start, start + 50):
                e.add_rule(RedactionRule(rule_id=f"r{i}", pattern=r"\d+"))

        threads = [threading.Thread(target=worker, args=(s,)) for s in (0, 50, 100, 150)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(e.list_rules()) == 200

    def test_concurrent_redact(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="r1", pattern=r"\d+", replacement="#"))
        results = []

        def worker() -> None:
            for _ in range(50):
                res = e.redact("abc 123 def")
                results.append(res.redacted_text)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 200
        assert all(r == "abc # def" for r in results)
        assert e.stats().total_redactions_performed == 200

    def test_concurrent_add_and_redact(self):
        e = DocRedactionEngine()
        e.add_rule(RedactionRule(rule_id="base", pattern=r"\d+", replacement="#"))

        errors: list = []

        def adder() -> None:
            try:
                for i in range(50):
                    e.add_rule(RedactionRule(rule_id=f"r{i}", pattern=r"[a-z]"))
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        def reader() -> None:
            try:
                for _ in range(50):
                    e.redact("abc 123 def")
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [
            threading.Thread(target=adder),
            threading.Thread(target=adder),
            threading.Thread(target=reader),
            threading.Thread(target=reader),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        # base rule still present
        assert e.get_rule("base") is not None

    def test_concurrent_clear_and_add(self):
        e = DocRedactionEngine()
        errors: list = []

        def adder() -> None:
            try:
                for i in range(100):
                    e.add_rule(RedactionRule(rule_id=f"r{i}", pattern="x"))
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        def clearer() -> None:
            try:
                for _ in range(10):
                    e.clear_rules()
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [
            threading.Thread(target=adder),
            threading.Thread(target=clearer),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
