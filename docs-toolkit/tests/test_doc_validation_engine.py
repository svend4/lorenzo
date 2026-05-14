"""Tests for the doc_validation_engine module (E354) — ≥55 tests."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_validation_engine import (
    DocValidationEngine,
    ValidationIssue,
    ValidationResult,
    ValidationRule,
    ValidationStats,
)


# ---------------------------------------------------------------------------
# Helpers — common check callables
# ---------------------------------------------------------------------------

def check_nonempty(content: str):
    if not content.strip():
        return "content is empty"
    return None


def check_has_title(content: str):
    if "# " not in content:
        return "missing H1 title"
    return None


def check_no_tabs(content: str):
    if "\t" in content:
        return "tabs are not allowed"
    return None


def always_fails(content: str):
    return "always fails"


def always_passes(content: str):
    return None


def raises(content: str):
    raise RuntimeError("boom")


# ---------------------------------------------------------------------------
# ValidationRule dataclass
# ---------------------------------------------------------------------------

class TestValidationRuleDataclass:
    def test_basic_construction(self):
        r = ValidationRule(rule_id="r1", name="Rule One")
        assert r.rule_id == "r1"
        assert r.name == "Rule One"

    def test_default_description(self):
        r = ValidationRule(rule_id="r1", name="x")
        assert r.description == ""

    def test_default_severity_warning(self):
        r = ValidationRule(rule_id="r1", name="x")
        assert r.severity == "warning"

    def test_default_enabled(self):
        r = ValidationRule(rule_id="r1", name="x")
        assert r.enabled is True

    def test_default_check_none(self):
        r = ValidationRule(rule_id="r1", name="x")
        assert r.check is None

    def test_custom_severity(self):
        r = ValidationRule(rule_id="r1", name="x", severity="error")
        assert r.severity == "error"

    def test_assign_check_callable(self):
        r = ValidationRule(rule_id="r1", name="x", check=check_nonempty)
        assert callable(r.check)


# ---------------------------------------------------------------------------
# ValidationIssue dataclass
# ---------------------------------------------------------------------------

class TestValidationIssueDataclass:
    def test_construction(self):
        i = ValidationIssue(rule_id="r1", severity="error", message="bad")
        assert i.rule_id == "r1"
        assert i.severity == "error"
        assert i.message == "bad"

    def test_equality(self):
        a = ValidationIssue(rule_id="r1", severity="warning", message="m")
        b = ValidationIssue(rule_id="r1", severity="warning", message="m")
        assert a == b

    def test_inequality(self):
        a = ValidationIssue(rule_id="r1", severity="warning", message="m")
        b = ValidationIssue(rule_id="r2", severity="warning", message="m")
        assert a != b


# ---------------------------------------------------------------------------
# ValidationResult dataclass
# ---------------------------------------------------------------------------

class TestValidationResultDataclass:
    def test_construction(self):
        r = ValidationResult(doc_id="d1", valid=True)
        assert r.doc_id == "d1"
        assert r.valid is True

    def test_default_issues_empty_list(self):
        r = ValidationResult(doc_id="d1", valid=True)
        assert r.issues == []

    def test_default_validated_at(self):
        r = ValidationResult(doc_id="d1", valid=True)
        assert r.validated_at == 0.0

    def test_independent_issues_lists(self):
        a = ValidationResult(doc_id="a", valid=True)
        b = ValidationResult(doc_id="b", valid=True)
        a.issues.append(ValidationIssue(rule_id="x", severity="info", message="m"))
        assert b.issues == []


# ---------------------------------------------------------------------------
# ValidationStats dataclass
# ---------------------------------------------------------------------------

class TestValidationStatsDataclass:
    def test_construction(self):
        s = ValidationStats(
            total_rules=3,
            enabled_rules=2,
            total_validations=10,
            total_issues_found=4,
        )
        assert s.total_rules == 3
        assert s.enabled_rules == 2
        assert s.total_validations == 10
        assert s.total_issues_found == 4


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_engine_no_rules(self):
        e = DocValidationEngine()
        assert e.list_rules() == []

    def test_empty_engine_stats(self):
        e = DocValidationEngine()
        s = e.stats()
        assert s.total_rules == 0
        assert s.enabled_rules == 0
        assert s.total_validations == 0
        assert s.total_issues_found == 0


# ---------------------------------------------------------------------------
# register_rule
# ---------------------------------------------------------------------------

class TestRegisterRule:
    def test_register_new(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="One"))
        assert e.get_rule("r1") is not None

    def test_register_increments_count(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="One"))
        e.register_rule(ValidationRule(rule_id="r2", name="Two"))
        assert e.stats().total_rules == 2

    def test_register_replace_same_id(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="One"))
        e.register_rule(ValidationRule(rule_id="r1", name="OneRenamed"))
        assert e.stats().total_rules == 1
        assert e.get_rule("r1").name == "OneRenamed"

    def test_register_with_check(self):
        e = DocValidationEngine()
        rule = ValidationRule(rule_id="r1", name="x", check=check_nonempty)
        e.register_rule(rule)
        assert e.get_rule("r1").check is check_nonempty


# ---------------------------------------------------------------------------
# unregister_rule
# ---------------------------------------------------------------------------

class TestUnregisterRule:
    def test_unregister_existing(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="x"))
        assert e.unregister_rule("r1") is True

    def test_unregister_removes_from_engine(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="x"))
        e.unregister_rule("r1")
        assert e.get_rule("r1") is None

    def test_unregister_missing(self):
        e = DocValidationEngine()
        assert e.unregister_rule("nope") is False

    def test_unregister_decreases_count(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="x"))
        e.register_rule(ValidationRule(rule_id="r2", name="y"))
        e.unregister_rule("r1")
        assert e.stats().total_rules == 1


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------

class TestEnableDisable:
    def test_disable_existing(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="x"))
        assert e.disable_rule("r1") is True
        assert e.get_rule("r1").enabled is False

    def test_enable_existing(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="x", enabled=False))
        assert e.enable_rule("r1") is True
        assert e.get_rule("r1").enabled is True

    def test_disable_missing(self):
        e = DocValidationEngine()
        assert e.disable_rule("nope") is False

    def test_enable_missing(self):
        e = DocValidationEngine()
        assert e.enable_rule("nope") is False

    def test_toggle_cycle(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="x"))
        e.disable_rule("r1")
        e.enable_rule("r1")
        e.disable_rule("r1")
        assert e.get_rule("r1").enabled is False

    def test_enable_changes_stats_enabled_count(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="x", enabled=False))
        assert e.stats().enabled_rules == 0
        e.enable_rule("r1")
        assert e.stats().enabled_rules == 1


# ---------------------------------------------------------------------------
# get_rule
# ---------------------------------------------------------------------------

class TestGetRule:
    def test_get_found(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="r1", name="x"))
        assert e.get_rule("r1").rule_id == "r1"

    def test_get_not_found(self):
        e = DocValidationEngine()
        assert e.get_rule("nope") is None


# ---------------------------------------------------------------------------
# list_rules
# ---------------------------------------------------------------------------

class TestListRules:
    def test_empty(self):
        e = DocValidationEngine()
        assert e.list_rules() == []

    def test_sorted_by_id(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="zeta", name="z"))
        e.register_rule(ValidationRule(rule_id="alpha", name="a"))
        e.register_rule(ValidationRule(rule_id="mu", name="m"))
        ids = [r.rule_id for r in e.list_rules()]
        assert ids == ["alpha", "mu", "zeta"]

    def test_returns_all(self):
        e = DocValidationEngine()
        for i in range(5):
            e.register_rule(ValidationRule(rule_id=f"r{i}", name=str(i)))
        assert len(e.list_rules()) == 5


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------

class TestValidate:
    def test_no_rules_returns_valid(self):
        e = DocValidationEngine()
        r = e.validate("d1", "hello")
        assert r.valid is True
        assert r.issues == []

    def test_all_enabled_rules_run(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_fails, severity="warning"))
        e.register_rule(ValidationRule(rule_id="b", name="b", check=always_fails, severity="warning"))
        r = e.validate("d1", "any")
        assert len(r.issues) == 2

    def test_disabled_rule_skipped(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_fails))
        e.register_rule(ValidationRule(rule_id="b", name="b", check=always_fails, enabled=False))
        r = e.validate("d1", "any")
        assert len(r.issues) == 1
        assert r.issues[0].rule_id == "a"

    def test_rule_ids_filter(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_fails))
        e.register_rule(ValidationRule(rule_id="b", name="b", check=always_fails))
        e.register_rule(ValidationRule(rule_id="c", name="c", check=always_fails))
        r = e.validate("d1", "any", rule_ids=["a", "c"])
        ids = sorted(i.rule_id for i in r.issues)
        assert ids == ["a", "c"]

    def test_rule_ids_unknown_skipped(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_fails))
        r = e.validate("d1", "any", rule_ids=["a", "missing"])
        assert len(r.issues) == 1

    def test_rule_ids_disabled_skipped(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_fails, enabled=False))
        r = e.validate("d1", "any", rule_ids=["a"])
        assert r.issues == []

    def test_valid_true_when_no_issues(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_passes))
        r = e.validate("d1", "any")
        assert r.valid is True

    def test_issue_carries_severity(self):
        e = DocValidationEngine()
        e.register_rule(
            ValidationRule(rule_id="a", name="a", check=always_fails, severity="info")
        )
        r = e.validate("d1", "any")
        assert r.issues[0].severity == "info"

    def test_issue_carries_message(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_fails))
        r = e.validate("d1", "any")
        assert r.issues[0].message == "always fails"

    def test_now_used_for_validated_at(self):
        e = DocValidationEngine()
        r = e.validate("d1", "x", now=123.456)
        assert r.validated_at == 123.456

    def test_default_now_uses_time(self):
        e = DocValidationEngine()
        r = e.validate("d1", "x")
        assert r.validated_at > 0

    def test_doc_id_propagated(self):
        e = DocValidationEngine()
        r = e.validate("my-doc", "x")
        assert r.doc_id == "my-doc"

    def test_check_returning_none_no_issue(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_passes))
        e.register_rule(ValidationRule(rule_id="b", name="b", check=always_fails))
        r = e.validate("d1", "any")
        assert len(r.issues) == 1
        assert r.issues[0].rule_id == "b"

    def test_rule_without_check_skipped(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a"))  # no check
        r = e.validate("d1", "any")
        assert r.issues == []
        assert r.valid is True

    def test_check_exception_captured_as_issue(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=raises, severity="error"))
        r = e.validate("d1", "any")
        assert len(r.issues) == 1
        assert "rule error" in r.issues[0].message
        assert r.valid is False


# ---------------------------------------------------------------------------
# Severity behaviour
# ---------------------------------------------------------------------------

class TestValidateSeverity:
    def test_warning_keeps_valid(self):
        e = DocValidationEngine()
        e.register_rule(
            ValidationRule(rule_id="w", name="w", check=always_fails, severity="warning")
        )
        r = e.validate("d1", "x")
        assert r.valid is True
        assert r.issues[0].severity == "warning"

    def test_info_keeps_valid(self):
        e = DocValidationEngine()
        e.register_rule(
            ValidationRule(rule_id="i", name="i", check=always_fails, severity="info")
        )
        r = e.validate("d1", "x")
        assert r.valid is True

    def test_error_makes_invalid(self):
        e = DocValidationEngine()
        e.register_rule(
            ValidationRule(rule_id="e", name="e", check=always_fails, severity="error")
        )
        r = e.validate("d1", "x")
        assert r.valid is False

    def test_mixed_severities(self):
        e = DocValidationEngine()
        e.register_rule(
            ValidationRule(rule_id="w", name="w", check=always_fails, severity="warning")
        )
        e.register_rule(
            ValidationRule(rule_id="e", name="e", check=always_fails, severity="error")
        )
        e.register_rule(
            ValidationRule(rule_id="i", name="i", check=always_fails, severity="info")
        )
        r = e.validate("d1", "x")
        assert r.valid is False
        assert len(r.issues) == 3

    def test_real_check_nonempty(self):
        e = DocValidationEngine()
        e.register_rule(
            ValidationRule(rule_id="ne", name="nonempty", check=check_nonempty, severity="error")
        )
        r = e.validate("d1", "")
        assert r.valid is False
        assert r.issues[0].message == "content is empty"


# ---------------------------------------------------------------------------
# validate_rule
# ---------------------------------------------------------------------------

class TestValidateRule:
    def test_single_rule_issue(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_fails))
        issue = e.validate_rule("a", "any")
        assert issue is not None
        assert issue.rule_id == "a"

    def test_single_rule_no_issue(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_passes))
        assert e.validate_rule("a", "any") is None

    def test_unknown_rule_returns_none(self):
        e = DocValidationEngine()
        assert e.validate_rule("nope", "any") is None

    def test_rule_without_check_returns_none(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a"))
        assert e.validate_rule("a", "any") is None

    def test_validate_rule_uses_severity(self):
        e = DocValidationEngine()
        e.register_rule(
            ValidationRule(rule_id="a", name="a", check=always_fails, severity="error")
        )
        issue = e.validate_rule("a", "any")
        assert issue.severity == "error"

    def test_validate_rule_exception(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=raises))
        issue = e.validate_rule("a", "any")
        assert issue is not None
        assert "rule error" in issue.message


# ---------------------------------------------------------------------------
# clear_rules
# ---------------------------------------------------------------------------

class TestClearRules:
    def test_clear_empty_returns_zero(self):
        e = DocValidationEngine()
        assert e.clear_rules() == 0

    def test_clear_returns_count(self):
        e = DocValidationEngine()
        for i in range(7):
            e.register_rule(ValidationRule(rule_id=f"r{i}", name=str(i)))
        assert e.clear_rules() == 7

    def test_clear_empties_engine(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a"))
        e.register_rule(ValidationRule(rule_id="b", name="b"))
        e.clear_rules()
        assert e.list_rules() == []
        assert e.stats().total_rules == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_total_validations_increments(self):
        e = DocValidationEngine()
        e.validate("d1", "x")
        e.validate("d2", "y")
        e.validate("d3", "z")
        assert e.stats().total_validations == 3

    def test_total_issues_found_increments(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_fails))
        e.register_rule(ValidationRule(rule_id="b", name="b", check=always_fails))
        e.validate("d1", "x")  # 2 issues
        e.validate("d2", "y")  # 2 issues
        assert e.stats().total_issues_found == 4

    def test_enabled_rules_count(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a"))
        e.register_rule(ValidationRule(rule_id="b", name="b", enabled=False))
        e.register_rule(ValidationRule(rule_id="c", name="c"))
        s = e.stats()
        assert s.total_rules == 3
        assert s.enabled_rules == 2

    def test_no_issues_no_increment(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_passes))
        e.validate("d1", "x")
        assert e.stats().total_issues_found == 0

    def test_stats_returns_stats_instance(self):
        e = DocValidationEngine()
        assert isinstance(e.stats(), ValidationStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_validate(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a", check=always_fails))
        e.register_rule(ValidationRule(rule_id="b", name="b", check=always_passes))

        errors: list = []

        def worker(n: int) -> None:
            try:
                for i in range(50):
                    e.validate(f"d{n}-{i}", "content")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(n,)) for n in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        s = e.stats()
        assert s.total_validations == 8 * 50
        assert s.total_issues_found == 8 * 50  # one failing rule per call

    def test_concurrent_register_and_validate(self):
        e = DocValidationEngine()

        errors: list = []

        def registrar() -> None:
            try:
                for i in range(100):
                    e.register_rule(
                        ValidationRule(rule_id=f"r{i}", name=str(i), check=always_passes)
                    )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def validator() -> None:
            try:
                for _ in range(100):
                    e.validate("d", "x")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=registrar),
            threading.Thread(target=validator),
            threading.Thread(target=validator),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert e.stats().total_validations == 200

    def test_concurrent_enable_disable(self):
        e = DocValidationEngine()
        e.register_rule(ValidationRule(rule_id="a", name="a"))

        errors: list = []

        def flipper() -> None:
            try:
                for i in range(200):
                    if i % 2:
                        e.enable_rule("a")
                    else:
                        e.disable_rule("a")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=flipper) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        # Rule still exists
        assert e.get_rule("a") is not None
