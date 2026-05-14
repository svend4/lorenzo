"""Tests for docstoolkit.governance (E1: governance policy engine)."""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.governance import (
    DataClass,
    ClassificationRule,
    DataClassifier,
    classify_document,
    RetentionPolicy,
    RetentionRule,
    RetentionEngine,
    PolicyViolation,
    PolicyEngine,
    PolicyReport,
)


# ---------------------------------------------------------------------------
# DataClass enum
# ---------------------------------------------------------------------------

class TestDataClass:
    def test_four_values(self):
        values = {dc.value for dc in DataClass}
        assert values == {"public", "internal", "confidential", "secret"}

    def test_public_value(self):
        assert DataClass.PUBLIC.value == "public"

    def test_internal_value(self):
        assert DataClass.INTERNAL.value == "internal"

    def test_confidential_value(self):
        assert DataClass.CONFIDENTIAL.value == "confidential"

    def test_secret_value(self):
        assert DataClass.SECRET.value == "secret"

    def test_is_string_enum(self):
        assert isinstance(DataClass.PUBLIC, str)
        assert DataClass.SECRET == "secret"


# ---------------------------------------------------------------------------
# ClassificationRule
# ---------------------------------------------------------------------------

class TestClassificationRule:
    def test_fields(self):
        rule = ClassificationRule("r", r"\btest\b", DataClass.PUBLIC, priority=5)
        assert rule.name == "r"
        assert rule.pattern == r"\btest\b"
        assert rule.data_class == DataClass.PUBLIC
        assert rule.priority == 5

    def test_default_priority_zero(self):
        rule = ClassificationRule("r", r"\btest\b", DataClass.PUBLIC)
        assert rule.priority == 0


# ---------------------------------------------------------------------------
# DataClassifier
# ---------------------------------------------------------------------------

class TestDataClassifier:
    def test_default_class_is_internal(self):
        dc = DataClassifier()
        assert dc.default_class == DataClass.INTERNAL

    def test_empty_rules_returns_default(self):
        dc = DataClassifier()
        assert dc.classify("hello world") == DataClass.INTERNAL

    def test_classify_returns_first_match(self):
        dc = DataClassifier()
        dc.add_rule(ClassificationRule("r1", r"\bfoo\b", DataClass.SECRET, priority=10))
        dc.add_rule(ClassificationRule("r2", r"\bfoo\b", DataClass.PUBLIC, priority=5))
        assert dc.classify("foo") == DataClass.SECRET

    def test_add_rule_sorted_by_priority_desc(self):
        dc = DataClassifier()
        dc.add_rule(ClassificationRule("low", r"\bx\b", DataClass.PUBLIC, priority=1))
        dc.add_rule(ClassificationRule("high", r"\bx\b", DataClass.SECRET, priority=100))
        dc.add_rule(ClassificationRule("mid", r"\bx\b", DataClass.CONFIDENTIAL, priority=50))
        assert dc.rules[0].priority == 100
        assert dc.rules[1].priority == 50
        assert dc.rules[2].priority == 1

    def test_classify_returns_default_on_no_match(self):
        dc = DataClassifier()
        dc.add_rule(ClassificationRule("r", r"\bsecret\b", DataClass.SECRET, priority=1))
        assert dc.classify("nothing special here") == DataClass.INTERNAL

    def test_classify_case_insensitive(self):
        dc = DataClassifier()
        dc.add_rule(ClassificationRule("r", r"\bSECRET\b", DataClass.SECRET, priority=1))
        assert dc.classify("this is secret data") == DataClass.SECRET

    def test_classify_custom_default(self):
        dc = DataClassifier(default_class=DataClass.PUBLIC)
        assert dc.classify("no match") == DataClass.PUBLIC

    def test_explain_returns_rule_name_on_match(self):
        dc = DataClassifier()
        dc.add_rule(ClassificationRule("my_rule", r"\bpassword\b", DataClass.SECRET, priority=10))
        result = dc.explain("reset password now")
        assert result == (DataClass.SECRET, "my_rule")

    def test_explain_returns_default_on_no_match(self):
        dc = DataClassifier()
        dc.add_rule(ClassificationRule("r", r"\bsecret\b", DataClass.SECRET, priority=1))
        result = dc.explain("normal text")
        assert result == (DataClass.INTERNAL, "default")

    def test_explain_empty_rules(self):
        dc = DataClassifier()
        cls, name = dc.explain("anything")
        assert cls == DataClass.INTERNAL
        assert name == "default"

    def test_explain_custom_default(self):
        dc = DataClassifier(default_class=DataClass.PUBLIC)
        cls, name = dc.explain("no match")
        assert cls == DataClass.PUBLIC
        assert name == "default"

    def test_multiple_rules_correct_priority(self):
        dc = DataClassifier()
        dc.add_rule(ClassificationRule("confidential_rule", r"\bconfidential\b",
                                       DataClass.CONFIDENTIAL, priority=50))
        dc.add_rule(ClassificationRule("secret_rule", r"\bpassword\b",
                                       DataClass.SECRET, priority=100))
        # Both patterns match — higher priority wins
        result = dc.classify("password confidential")
        assert result == DataClass.SECRET


# ---------------------------------------------------------------------------
# classify_document convenience function
# ---------------------------------------------------------------------------

class TestClassifyDocument:
    def test_password_is_secret(self):
        assert classify_document("The password is abc123") == DataClass.SECRET

    def test_secret_keyword_is_secret(self):
        assert classify_document("This is a secret document") == DataClass.SECRET

    def test_api_key_is_secret(self):
        assert classify_document("Your api key expires soon") == DataClass.SECRET

    def test_token_is_secret(self):
        assert classify_document("Bearer token required") == DataClass.SECRET

    def test_confidential_keyword(self):
        assert classify_document("This document is confidential") == DataClass.CONFIDENTIAL

    def test_internal_only_keyword(self):
        assert classify_document("For internal only distribution") == DataClass.CONFIDENTIAL

    def test_do_not_share_keyword(self):
        assert classify_document("do not share this") == DataClass.CONFIDENTIAL

    def test_open_source_is_public(self):
        assert classify_document("This is an open source project") == DataClass.PUBLIC

    def test_mit_license_is_public(self):
        assert classify_document("Released under MIT license") == DataClass.PUBLIC

    def test_plain_content_is_internal(self):
        assert classify_document("Meeting notes from today") == DataClass.INTERNAL

    def test_custom_rules_override_defaults(self):
        custom = [
            ClassificationRule("custom_secret", r"\btopsecret\b", DataClass.SECRET, priority=200),
        ]
        assert classify_document("topsecret mission", rules=custom) == DataClass.SECRET

    def test_custom_rules_no_match_returns_internal(self):
        custom = [
            ClassificationRule("custom", r"\btopsecret\b", DataClass.SECRET, priority=10),
        ]
        assert classify_document("normal content", rules=custom) == DataClass.INTERNAL

    def test_secret_beats_confidential_in_defaults(self):
        # Both patterns match — SECRET has higher priority
        result = classify_document("password confidential")
        assert result == DataClass.SECRET


# ---------------------------------------------------------------------------
# RetentionRule
# ---------------------------------------------------------------------------

class TestRetentionRule:
    def test_fields(self):
        rule = RetentionRule(DataClass.SECRET, max_age_days=30)
        assert rule.data_class == DataClass.SECRET
        assert rule.max_age_days == 30
        assert rule.auto_archive is False
        assert rule.auto_delete is False

    def test_auto_flags(self):
        rule = RetentionRule(DataClass.CONFIDENTIAL, 60, auto_archive=True, auto_delete=True)
        assert rule.auto_archive is True
        assert rule.auto_delete is True


# ---------------------------------------------------------------------------
# RetentionPolicy
# ---------------------------------------------------------------------------

class TestRetentionPolicy:
    def _make_policy(self):
        policy = RetentionPolicy(name="test_policy", default_max_age_days=365)
        policy.rules.append(RetentionRule(DataClass.SECRET, 30))
        policy.rules.append(RetentionRule(DataClass.CONFIDENTIAL, 90))
        return policy

    def test_rule_for_returns_matching_rule(self):
        policy = self._make_policy()
        rule = policy.rule_for(DataClass.SECRET)
        assert rule is not None
        assert rule.data_class == DataClass.SECRET
        assert rule.max_age_days == 30

    def test_rule_for_no_match_returns_none(self):
        policy = self._make_policy()
        assert policy.rule_for(DataClass.PUBLIC) is None

    def test_max_age_for_returns_rule_value(self):
        policy = self._make_policy()
        assert policy.max_age_for(DataClass.SECRET) == 30
        assert policy.max_age_for(DataClass.CONFIDENTIAL) == 90

    def test_max_age_for_no_rule_returns_default(self):
        policy = self._make_policy()
        assert policy.max_age_for(DataClass.PUBLIC) == 365

    def test_default_max_age_days(self):
        policy = RetentionPolicy(name="p")
        assert policy.default_max_age_days == 365


# ---------------------------------------------------------------------------
# RetentionEngine
# ---------------------------------------------------------------------------

def _iso_ago(days: float) -> str:
    """Return an ISO-formatted datetime `days` ago."""
    dt = datetime.now(timezone.utc) - timedelta(days=days)
    return dt.isoformat()


class TestRetentionEngine:
    def _engine(self, **rules_kwargs):
        policy = RetentionPolicy(name="p", default_max_age_days=365)
        for dc, kwargs in rules_kwargs.items():
            policy.rules.append(RetentionRule(dc, **kwargs))
        return RetentionEngine(policy)

    def test_recent_doc_no_violation(self):
        engine = RetentionEngine(RetentionPolicy("p", default_max_age_days=365))
        result = engine.check("doc1", DataClass.INTERNAL, _iso_ago(10))
        assert result is None

    def test_old_doc_returns_violation(self):
        engine = RetentionEngine(RetentionPolicy("p", default_max_age_days=30))
        result = engine.check("doc1", DataClass.INTERNAL, _iso_ago(60))
        assert result is not None
        assert result.doc_id == "doc1"
        assert result.data_class == DataClass.INTERNAL
        assert result.age_days > 59
        assert result.max_age_days == 30

    def test_auto_delete_action(self):
        policy = RetentionPolicy("p", default_max_age_days=365)
        policy.rules.append(RetentionRule(DataClass.SECRET, 10, auto_delete=True))
        engine = RetentionEngine(policy)
        result = engine.check("doc1", DataClass.SECRET, _iso_ago(20))
        assert result is not None
        assert result.action == "delete"

    def test_auto_archive_action(self):
        policy = RetentionPolicy("p", default_max_age_days=365)
        policy.rules.append(RetentionRule(DataClass.CONFIDENTIAL, 10, auto_archive=True))
        engine = RetentionEngine(policy)
        result = engine.check("doc1", DataClass.CONFIDENTIAL, _iso_ago(20))
        assert result is not None
        assert result.action == "archive"

    def test_neither_flag_action_review(self):
        policy = RetentionPolicy("p", default_max_age_days=10)
        engine = RetentionEngine(policy)
        result = engine.check("doc1", DataClass.INTERNAL, _iso_ago(20))
        assert result is not None
        assert result.action == "review"

    def test_auto_delete_beats_auto_archive(self):
        policy = RetentionPolicy("p", default_max_age_days=365)
        policy.rules.append(
            RetentionRule(DataClass.SECRET, 10, auto_archive=True, auto_delete=True)
        )
        engine = RetentionEngine(policy)
        result = engine.check("doc1", DataClass.SECRET, _iso_ago(20))
        assert result is not None
        assert result.action == "delete"

    def test_unparseable_date_no_violation(self):
        engine = RetentionEngine(RetentionPolicy("p", default_max_age_days=1))
        result = engine.check("doc1", DataClass.INTERNAL, "not-a-date")
        assert result is None

    def test_none_date_no_violation(self):
        engine = RetentionEngine(RetentionPolicy("p", default_max_age_days=1))
        result = engine.check("doc1", DataClass.INTERNAL, None)
        assert result is None

    def test_check_batch_returns_only_violations(self):
        policy = RetentionPolicy("p", default_max_age_days=30)
        engine = RetentionEngine(policy)
        docs = [
            ("old", DataClass.INTERNAL, _iso_ago(60)),
            ("new", DataClass.INTERNAL, _iso_ago(5)),
            ("also_old", DataClass.INTERNAL, _iso_ago(90)),
        ]
        violations = engine.check_batch(docs)
        assert len(violations) == 2
        ids = {v.doc_id for v in violations}
        assert ids == {"old", "also_old"}

    def test_check_batch_empty_input(self):
        engine = RetentionEngine(RetentionPolicy("p"))
        assert engine.check_batch([]) == []

    def test_violation_fields(self):
        policy = RetentionPolicy("p", default_max_age_days=10)
        engine = RetentionEngine(policy)
        result = engine.check("my_doc", DataClass.PUBLIC, _iso_ago(20))
        assert result is not None
        assert result.doc_id == "my_doc"
        assert result.data_class == DataClass.PUBLIC
        assert result.max_age_days == 10


# ---------------------------------------------------------------------------
# PolicyViolation
# ---------------------------------------------------------------------------

class TestPolicyViolation:
    def test_fields(self):
        v = PolicyViolation(
            doc_id="d1",
            violation_type="retention",
            detail="old doc",
            severity="high",
            data_class=DataClass.CONFIDENTIAL,
        )
        assert v.doc_id == "d1"
        assert v.violation_type == "retention"
        assert v.detail == "old doc"
        assert v.severity == "high"
        assert v.data_class == DataClass.CONFIDENTIAL

    def test_default_data_class(self):
        v = PolicyViolation("d", "access", "detail", "low")
        assert v.data_class == DataClass.INTERNAL

    def test_is_critical_true(self):
        v = PolicyViolation("d", "classification", "secret", "critical")
        assert v.is_critical() is True

    def test_is_critical_false_for_high(self):
        v = PolicyViolation("d", "retention", "old", "high")
        assert v.is_critical() is False

    def test_is_critical_false_for_medium(self):
        v = PolicyViolation("d", "retention", "old", "medium")
        assert v.is_critical() is False

    def test_is_critical_false_for_low(self):
        v = PolicyViolation("d", "retention", "old", "low")
        assert v.is_critical() is False


# ---------------------------------------------------------------------------
# PolicyReport
# ---------------------------------------------------------------------------

class TestPolicyReport:
    def _make_report(self):
        report = PolicyReport(docs_checked=5, clean_docs=2)
        report.violations = [
            PolicyViolation("d1", "classification", "secret", "critical"),
            PolicyViolation("d2", "retention", "old", "high"),
            PolicyViolation("d3", "retention", "old", "medium"),
            PolicyViolation("d4", "classification", "secret", "critical"),
        ]
        return report

    def test_violation_count(self):
        report = self._make_report()
        assert report.violation_count() == 4

    def test_critical_count(self):
        report = self._make_report()
        assert report.critical_count() == 2

    def test_by_type_classification(self):
        report = self._make_report()
        result = report.by_type("classification")
        assert len(result) == 2
        assert all(v.violation_type == "classification" for v in result)

    def test_by_type_retention(self):
        report = self._make_report()
        result = report.by_type("retention")
        assert len(result) == 2

    def test_by_type_no_match(self):
        report = self._make_report()
        assert report.by_type("access") == []

    def test_summary_format(self):
        report = self._make_report()
        s = report.summary()
        assert "docs=5" in s
        assert "clean=2" in s
        assert "violations=4" in s
        assert "critical=2" in s

    def test_empty_report(self):
        report = PolicyReport(docs_checked=3, clean_docs=3)
        assert report.violation_count() == 0
        assert report.critical_count() == 0
        assert "violations=0" in report.summary()


# ---------------------------------------------------------------------------
# PolicyEngine.audit
# ---------------------------------------------------------------------------

class TestPolicyEngine:
    def _make_classifier(self):
        dc = DataClassifier()
        dc.add_rule(ClassificationRule("secret", r"\bpassword\b", DataClass.SECRET, priority=100))
        dc.add_rule(ClassificationRule("public", r"\bopen.?source\b", DataClass.PUBLIC, priority=10))
        return dc

    def test_audit_returns_policy_report(self):
        engine = PolicyEngine(self._make_classifier())
        report = engine.audit([])
        assert isinstance(report, PolicyReport)

    def test_empty_docs_zero_violations(self):
        engine = PolicyEngine(self._make_classifier())
        report = engine.audit([])
        assert report.violation_count() == 0
        assert report.docs_checked == 0

    def test_docs_checked_matches_input(self):
        engine = PolicyEngine(self._make_classifier())
        docs = [
            ("d1", "normal text", _iso_ago(1)),
            ("d2", "more normal", _iso_ago(2)),
            ("d3", "even more normal", _iso_ago(3)),
        ]
        report = engine.audit(docs)
        assert report.docs_checked == 3

    def test_secret_doc_adds_violation(self):
        engine = PolicyEngine(self._make_classifier())
        docs = [("d1", "the password is 1234", _iso_ago(1))]
        report = engine.audit(docs)
        class_violations = report.by_type("classification")
        assert len(class_violations) == 1
        assert class_violations[0].doc_id == "d1"
        assert class_violations[0].severity == "critical"

    def test_non_secret_doc_no_classification_violation(self):
        engine = PolicyEngine(self._make_classifier())
        docs = [("d1", "normal meeting notes", _iso_ago(1))]
        report = engine.audit(docs)
        assert len(report.by_type("classification")) == 0

    def test_retention_violation_included(self):
        policy = RetentionPolicy("p", default_max_age_days=30)
        retention = RetentionEngine(policy)
        engine = PolicyEngine(self._make_classifier(), retention_engine=retention)
        docs = [("d1", "normal text", _iso_ago(60))]
        report = engine.audit(docs)
        ret_violations = report.by_type("retention")
        assert len(ret_violations) == 1
        assert ret_violations[0].doc_id == "d1"

    def test_no_retention_engine_no_retention_violations(self):
        engine = PolicyEngine(self._make_classifier(), retention_engine=None)
        docs = [("d1", "normal text", _iso_ago(1000))]
        report = engine.audit(docs)
        assert len(report.by_type("retention")) == 0

    def test_clean_docs_count(self):
        engine = PolicyEngine(self._make_classifier())
        docs = [
            ("clean1", "open source project", _iso_ago(1)),
            ("secret1", "password exposed", _iso_ago(1)),
            ("clean2", "meeting notes", _iso_ago(1)),
        ]
        report = engine.audit(docs)
        assert report.clean_docs == 2

    def test_retention_severity_secret_critical(self):
        policy = RetentionPolicy("p", default_max_age_days=1)
        retention = RetentionEngine(policy)
        engine = PolicyEngine(self._make_classifier(), retention_engine=retention)
        docs = [("d1", "the password is here", _iso_ago(10))]
        report = engine.audit(docs)
        ret_violations = report.by_type("retention")
        assert len(ret_violations) == 1
        assert ret_violations[0].severity == "critical"

    def test_retention_severity_internal_medium(self):
        policy = RetentionPolicy("p", default_max_age_days=1)
        retention = RetentionEngine(policy)
        engine = PolicyEngine(self._make_classifier(), retention_engine=retention)
        docs = [("d1", "normal meeting notes", _iso_ago(10))]
        report = engine.audit(docs)
        ret_violations = report.by_type("retention")
        assert len(ret_violations) == 1
        assert ret_violations[0].severity == "medium"

    def test_retention_severity_public_low(self):
        policy = RetentionPolicy("p", default_max_age_days=1)
        retention = RetentionEngine(policy)
        engine = PolicyEngine(self._make_classifier(), retention_engine=retention)
        docs = [("d1", "open source project", _iso_ago(10))]
        report = engine.audit(docs)
        ret_violations = report.by_type("retention")
        assert len(ret_violations) == 1
        assert ret_violations[0].severity == "low"

    def test_multiple_docs_multiple_violations(self):
        policy = RetentionPolicy("p", default_max_age_days=30)
        retention = RetentionEngine(policy)
        engine = PolicyEngine(self._make_classifier(), retention_engine=retention)
        docs = [
            ("d1", "the password is secret", _iso_ago(60)),  # classification + retention
            ("d2", "normal text", _iso_ago(1)),              # clean
            ("d3", "normal text", _iso_ago(60)),             # retention only
        ]
        report = engine.audit(docs)
        assert report.docs_checked == 3
        assert len(report.by_type("classification")) == 1
        assert len(report.by_type("retention")) == 2
        assert report.clean_docs == 1
