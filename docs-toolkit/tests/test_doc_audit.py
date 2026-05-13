"""Tests for E206 doc_audit module."""
from __future__ import annotations

import os
import tempfile
import time

import pytest

from docstoolkit.doc_audit import (
    AuditEvent,
    ComplianceReport,
    ComplianceTag,
    DocAudit,
    EventCategory,
    Severity,
)


# ---------------------------------------------------------------------------
# Enum tests
# ---------------------------------------------------------------------------


class TestEventCategory:
    def test_has_authentication(self):
        assert EventCategory.AUTHENTICATION.value == "authentication"

    def test_has_authorization(self):
        assert EventCategory.AUTHORIZATION.value == "authorization"

    def test_has_data_access(self):
        assert EventCategory.DATA_ACCESS.value == "data_access"

    def test_has_data_modification(self):
        assert EventCategory.DATA_MODIFICATION.value == "data_modification"

    def test_has_administrative(self):
        assert EventCategory.ADMINISTRATIVE.value == "administrative"

    def test_has_security(self):
        assert EventCategory.SECURITY.value == "security"

    def test_has_compliance(self):
        assert EventCategory.COMPLIANCE.value == "compliance"

    def test_total_count(self):
        assert len(EventCategory) == 7


class TestComplianceTag:
    def test_has_gdpr(self):
        assert ComplianceTag.GDPR.value == "gdpr"

    def test_has_hipaa(self):
        assert ComplianceTag.HIPAA.value == "hipaa"

    def test_has_sox(self):
        assert ComplianceTag.SOX.value == "sox"

    def test_has_pci_dss(self):
        assert ComplianceTag.PCI_DSS.value == "pci_dss"

    def test_has_ccpa(self):
        assert ComplianceTag.CCPA.value == "ccpa"

    def test_has_general(self):
        assert ComplianceTag.GENERAL.value == "general"

    def test_total_count(self):
        assert len(ComplianceTag) == 6


class TestSeverity:
    def test_has_low(self):
        assert Severity.LOW.value == "low"

    def test_has_medium(self):
        assert Severity.MEDIUM.value == "medium"

    def test_has_high(self):
        assert Severity.HIGH.value == "high"

    def test_has_critical(self):
        assert Severity.CRITICAL.value == "critical"

    def test_total_count(self):
        assert len(Severity) == 4


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestAuditEvent:
    def test_defaults(self):
        ev = AuditEvent(
            event_id=1,
            timestamp=100.0,
            actor="alice",
            action="read",
            resource="/doc",
            category=EventCategory.DATA_ACCESS,
        )
        assert ev.severity == Severity.LOW
        assert ev.compliance_tags == set()
        assert ev.outcome == "success"
        assert ev.details == {}

    def test_custom_fields(self):
        ev = AuditEvent(
            event_id=2,
            timestamp=200.0,
            actor="bob",
            action="write",
            resource="/x",
            category=EventCategory.DATA_MODIFICATION,
            severity=Severity.HIGH,
            compliance_tags={ComplianceTag.GDPR},
            outcome="failure",
            details={"k": "v"},
        )
        assert ev.severity == Severity.HIGH
        assert ev.outcome == "failure"
        assert ev.details == {"k": "v"}
        assert ComplianceTag.GDPR in ev.compliance_tags

    def test_distinct_default_dicts(self):
        a = AuditEvent(1, 1.0, "a", "b", "c", EventCategory.SECURITY)
        b = AuditEvent(2, 2.0, "a", "b", "c", EventCategory.SECURITY)
        a.details["x"] = 1
        assert "x" not in b.details


class TestComplianceReport:
    def test_construct(self):
        r = ComplianceReport(
            tag=ComplianceTag.GDPR,
            period_start=0.0,
            period_end=100.0,
            total_events=5,
            by_category={"data_access": 5},
            by_severity={"low": 5},
            by_outcome={"success": 5},
            unique_actors=2,
        )
        assert r.tag is ComplianceTag.GDPR
        assert r.total_events == 5
        assert r.unique_actors == 2


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def audit():
    a = DocAudit()
    yield a
    a.close()


def _seed_events(a: DocAudit, base: float = 1000.0):
    a.log(
        "alice", "login", "/auth", EventCategory.AUTHENTICATION,
        severity=Severity.LOW, now=base + 0,
    )
    a.log(
        "alice", "read", "/doc/1", EventCategory.DATA_ACCESS,
        severity=Severity.LOW,
        compliance_tags={ComplianceTag.GDPR}, now=base + 1,
    )
    a.log(
        "bob", "write", "/doc/2", EventCategory.DATA_MODIFICATION,
        severity=Severity.MEDIUM,
        compliance_tags={ComplianceTag.HIPAA}, now=base + 2,
    )
    a.log(
        "bob", "delete", "/doc/2", EventCategory.DATA_MODIFICATION,
        severity=Severity.HIGH, outcome="failure",
        compliance_tags={ComplianceTag.GDPR, ComplianceTag.HIPAA},
        now=base + 3,
    )
    a.log(
        "admin", "config", "/sys", EventCategory.ADMINISTRATIVE,
        severity=Severity.CRITICAL, outcome="failure", now=base + 4,
    )


# ---------------------------------------------------------------------------
# log()
# ---------------------------------------------------------------------------


class TestLog:
    def test_returns_event(self, audit):
        ev = audit.log(
            "alice", "read", "/x", EventCategory.DATA_ACCESS, now=10.0
        )
        assert isinstance(ev, AuditEvent)
        assert ev.actor == "alice"
        assert ev.action == "read"
        assert ev.resource == "/x"
        assert ev.category == EventCategory.DATA_ACCESS

    def test_assigns_event_id(self, audit):
        e1 = audit.log("a", "x", "y", EventCategory.SECURITY, now=1.0)
        e2 = audit.log("a", "x", "y", EventCategory.SECURITY, now=2.0)
        assert e1.event_id == 1
        assert e2.event_id == 2

    def test_default_outcome(self, audit):
        ev = audit.log("a", "x", "y", EventCategory.SECURITY, now=1.0)
        assert ev.outcome == "success"

    def test_default_severity(self, audit):
        ev = audit.log("a", "x", "y", EventCategory.SECURITY, now=1.0)
        assert ev.severity == Severity.LOW

    def test_custom_severity(self, audit):
        ev = audit.log(
            "a", "x", "y", EventCategory.SECURITY,
            severity=Severity.CRITICAL, now=1.0,
        )
        assert ev.severity == Severity.CRITICAL

    def test_compliance_tags_set(self, audit):
        ev = audit.log(
            "a", "x", "y", EventCategory.COMPLIANCE,
            compliance_tags={ComplianceTag.GDPR, ComplianceTag.HIPAA}, now=1.0,
        )
        assert ComplianceTag.GDPR in ev.compliance_tags
        assert ComplianceTag.HIPAA in ev.compliance_tags

    def test_details_stored(self, audit):
        ev = audit.log(
            "a", "x", "y", EventCategory.SECURITY,
            details={"ip": "1.2.3.4"}, now=1.0,
        )
        assert ev.details["ip"] == "1.2.3.4"

    def test_default_timestamp_uses_now(self, audit):
        before = time.time()
        ev = audit.log("a", "x", "y", EventCategory.SECURITY)
        after = time.time()
        assert before <= ev.timestamp <= after

    def test_total_events_increments(self, audit):
        assert audit.total_events == 0
        audit.log("a", "x", "y", EventCategory.SECURITY, now=1.0)
        assert audit.total_events == 1


# ---------------------------------------------------------------------------
# get()
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_known(self, audit):
        ev = audit.log("a", "x", "y", EventCategory.SECURITY, now=1.0)
        got = audit.get(ev.event_id)
        assert got is not None
        assert got.event_id == ev.event_id
        assert got.actor == "a"

    def test_get_missing(self, audit):
        assert audit.get(999) is None

    def test_get_preserves_tags(self, audit):
        ev = audit.log(
            "a", "x", "y", EventCategory.DATA_ACCESS,
            compliance_tags={ComplianceTag.GDPR}, now=1.0,
        )
        got = audit.get(ev.event_id)
        assert ComplianceTag.GDPR in got.compliance_tags

    def test_get_preserves_details(self, audit):
        ev = audit.log(
            "a", "x", "y", EventCategory.SECURITY,
            details={"k": "v"}, now=1.0,
        )
        got = audit.get(ev.event_id)
        assert got.details == {"k": "v"}


# ---------------------------------------------------------------------------
# events_by_actor
# ---------------------------------------------------------------------------


class TestEventsByActor:
    def test_filters_by_actor(self, audit):
        _seed_events(audit)
        assert len(audit.events_by_actor("alice")) == 2

    def test_unknown_returns_empty(self, audit):
        _seed_events(audit)
        assert audit.events_by_actor("zoe") == []

    def test_limit(self, audit):
        for i in range(5):
            audit.log("alice", "x", "y", EventCategory.SECURITY, now=float(i))
        assert len(audit.events_by_actor("alice", limit=3)) == 3


# ---------------------------------------------------------------------------
# events_by_resource
# ---------------------------------------------------------------------------


class TestEventsByResource:
    def test_filters(self, audit):
        _seed_events(audit)
        assert len(audit.events_by_resource("/doc/2")) == 2

    def test_unknown(self, audit):
        _seed_events(audit)
        assert audit.events_by_resource("/missing") == []

    def test_limit(self, audit):
        for i in range(5):
            audit.log("a", "x", "/r", EventCategory.SECURITY, now=float(i))
        assert len(audit.events_by_resource("/r", limit=2)) == 2


# ---------------------------------------------------------------------------
# events_by_category
# ---------------------------------------------------------------------------


class TestEventsByCategory:
    def test_filter_data_mod(self, audit):
        _seed_events(audit)
        assert len(audit.events_by_category(EventCategory.DATA_MODIFICATION)) == 2

    def test_filter_authentication(self, audit):
        _seed_events(audit)
        assert len(audit.events_by_category(EventCategory.AUTHENTICATION)) == 1

    def test_filter_security_empty(self, audit):
        _seed_events(audit)
        assert audit.events_by_category(EventCategory.SECURITY) == []

    def test_limit(self, audit):
        for i in range(4):
            audit.log("a", "x", "y", EventCategory.SECURITY, now=float(i))
        assert len(audit.events_by_category(EventCategory.SECURITY, limit=2)) == 2


# ---------------------------------------------------------------------------
# events_by_severity
# ---------------------------------------------------------------------------


class TestEventsBySeverity:
    def test_filter_high(self, audit):
        _seed_events(audit)
        assert len(audit.events_by_severity(Severity.HIGH)) == 1

    def test_filter_low(self, audit):
        _seed_events(audit)
        assert len(audit.events_by_severity(Severity.LOW)) == 2

    def test_filter_critical(self, audit):
        _seed_events(audit)
        assert len(audit.events_by_severity(Severity.CRITICAL)) == 1

    def test_limit(self, audit):
        for i in range(5):
            audit.log(
                "a", "x", "y", EventCategory.SECURITY,
                severity=Severity.MEDIUM, now=float(i),
            )
        assert len(audit.events_by_severity(Severity.MEDIUM, limit=3)) == 3


# ---------------------------------------------------------------------------
# events_by_compliance_tag
# ---------------------------------------------------------------------------


class TestEventsByComplianceTag:
    def test_filter_gdpr(self, audit):
        _seed_events(audit)
        assert len(audit.events_by_compliance_tag(ComplianceTag.GDPR)) == 2

    def test_filter_hipaa(self, audit):
        _seed_events(audit)
        assert len(audit.events_by_compliance_tag(ComplianceTag.HIPAA)) == 2

    def test_filter_unused(self, audit):
        _seed_events(audit)
        assert audit.events_by_compliance_tag(ComplianceTag.SOX) == []

    def test_limit(self, audit):
        for i in range(4):
            audit.log(
                "a", "x", "y", EventCategory.SECURITY,
                compliance_tags={ComplianceTag.GDPR}, now=float(i),
            )
        assert len(
            audit.events_by_compliance_tag(ComplianceTag.GDPR, limit=2)
        ) == 2


# ---------------------------------------------------------------------------
# events_in_range
# ---------------------------------------------------------------------------


class TestEventsInRange:
    def test_includes_boundaries(self, audit):
        _seed_events(audit, base=1000.0)
        # Events at 1000..1004
        got = audit.events_in_range(1000.0, 1004.0)
        assert len(got) == 5

    def test_narrow_window(self, audit):
        _seed_events(audit, base=1000.0)
        got = audit.events_in_range(1001.0, 1003.0)
        assert len(got) == 3

    def test_empty_window(self, audit):
        _seed_events(audit, base=1000.0)
        got = audit.events_in_range(5000.0, 6000.0)
        assert got == []


# ---------------------------------------------------------------------------
# failures()
# ---------------------------------------------------------------------------


class TestFailures:
    def test_finds_failures(self, audit):
        _seed_events(audit)
        fails = audit.failures()
        assert len(fails) == 2
        assert all(e.outcome != "success" for e in fails)

    def test_no_failures(self, audit):
        audit.log("a", "x", "y", EventCategory.SECURITY, now=1.0)
        assert audit.failures() == []

    def test_limit(self, audit):
        for i in range(4):
            audit.log(
                "a", "x", "y", EventCategory.SECURITY,
                outcome="failure", now=float(i),
            )
        assert len(audit.failures(limit=2)) == 2


# ---------------------------------------------------------------------------
# compliance_report()
# ---------------------------------------------------------------------------


class TestComplianceReportMethod:
    def test_gdpr_report(self, audit):
        _seed_events(audit, base=1000.0)
        rep = audit.compliance_report(ComplianceTag.GDPR, 0.0, 9999.0)
        assert isinstance(rep, ComplianceReport)
        assert rep.tag is ComplianceTag.GDPR
        assert rep.total_events == 2

    def test_categories_and_severities(self, audit):
        _seed_events(audit, base=1000.0)
        rep = audit.compliance_report(ComplianceTag.HIPAA, 0.0, 9999.0)
        # Two events tagged HIPAA: both DATA_MODIFICATION
        assert rep.by_category.get("data_modification") == 2
        assert "medium" in rep.by_severity
        assert "high" in rep.by_severity

    def test_outcomes(self, audit):
        _seed_events(audit, base=1000.0)
        rep = audit.compliance_report(ComplianceTag.GDPR, 0.0, 9999.0)
        # GDPR: one success (alice read), one failure (bob delete)
        assert rep.by_outcome.get("success") == 1
        assert rep.by_outcome.get("failure") == 1

    def test_unique_actors(self, audit):
        _seed_events(audit, base=1000.0)
        rep = audit.compliance_report(ComplianceTag.GDPR, 0.0, 9999.0)
        assert rep.unique_actors == 2  # alice, bob

    def test_empty_report(self, audit):
        _seed_events(audit, base=1000.0)
        rep = audit.compliance_report(ComplianceTag.SOX, 0.0, 9999.0)
        assert rep.total_events == 0
        assert rep.unique_actors == 0
        assert rep.by_category == {}

    def test_period_bounds_respected(self, audit):
        _seed_events(audit, base=1000.0)
        rep = audit.compliance_report(ComplianceTag.GDPR, 1003.0, 1004.0)
        assert rep.total_events == 1  # only bob delete


# ---------------------------------------------------------------------------
# count()
# ---------------------------------------------------------------------------


class TestCount:
    def test_total(self, audit):
        _seed_events(audit)
        assert audit.count() == 5

    def test_by_actor(self, audit):
        _seed_events(audit)
        assert audit.count(actor="bob") == 2

    def test_by_category(self, audit):
        _seed_events(audit)
        assert audit.count(category=EventCategory.DATA_MODIFICATION) == 2

    def test_by_severity(self, audit):
        _seed_events(audit)
        assert audit.count(severity=Severity.CRITICAL) == 1

    def test_by_outcome(self, audit):
        _seed_events(audit)
        assert audit.count(outcome="failure") == 2

    def test_combined(self, audit):
        _seed_events(audit)
        n = audit.count(
            actor="bob",
            category=EventCategory.DATA_MODIFICATION,
            outcome="failure",
        )
        assert n == 1


# ---------------------------------------------------------------------------
# recent()
# ---------------------------------------------------------------------------


class TestRecent:
    def test_returns_descending(self, audit):
        for i in range(5):
            audit.log("a", "x", "y", EventCategory.SECURITY, now=float(i))
        r = audit.recent(limit=3)
        assert len(r) == 3
        assert r[0].event_id == 5
        assert r[1].event_id == 4
        assert r[2].event_id == 3

    def test_default_limit(self, audit):
        for i in range(15):
            audit.log("a", "x", "y", EventCategory.SECURITY, now=float(i))
        r = audit.recent()
        assert len(r) == 10

    def test_empty(self, audit):
        assert audit.recent() == []


# ---------------------------------------------------------------------------
# actors_count()
# ---------------------------------------------------------------------------


class TestActorsCount:
    def test_zero(self, audit):
        assert audit.actors_count() == 0

    def test_distinct(self, audit):
        _seed_events(audit)
        assert audit.actors_count() == 3  # alice, bob, admin

    def test_duplicates_not_double_counted(self, audit):
        audit.log("a", "x", "y", EventCategory.SECURITY, now=1.0)
        audit.log("a", "x", "y", EventCategory.SECURITY, now=2.0)
        assert audit.actors_count() == 1


# ---------------------------------------------------------------------------
# purge_older_than()
# ---------------------------------------------------------------------------


class TestPurgeOlderThan:
    def test_removes_old(self, audit):
        audit.log("a", "x", "y", EventCategory.SECURITY, now=100.0)
        audit.log("a", "x", "y", EventCategory.SECURITY, now=200.0)
        audit.log("a", "x", "y", EventCategory.SECURITY, now=300.0)
        # cutoff = now(=400) - older_than(=150) = 250 → delete <250
        removed = audit.purge_older_than(older_than=150.0, now=400.0)
        assert removed == 2
        assert audit.total_events == 1

    def test_no_removal_when_all_fresh(self, audit):
        audit.log("a", "x", "y", EventCategory.SECURITY, now=100.0)
        removed = audit.purge_older_than(older_than=1000.0, now=200.0)
        assert removed == 0

    def test_purge_all(self, audit):
        audit.log("a", "x", "y", EventCategory.SECURITY, now=10.0)
        audit.log("a", "x", "y", EventCategory.SECURITY, now=20.0)
        removed = audit.purge_older_than(older_than=0.0, now=1000.0)
        assert removed == 2
        assert audit.total_events == 0


# ---------------------------------------------------------------------------
# Persistence (file db)
# ---------------------------------------------------------------------------


class TestPersistence:
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "audit.db")
            a = DocAudit(db_path=path)
            ev = a.log(
                "alice", "read", "/x", EventCategory.DATA_ACCESS,
                severity=Severity.MEDIUM,
                compliance_tags={ComplianceTag.GDPR},
                details={"foo": 1},
                now=42.0,
            )
            a.close()

            b = DocAudit(db_path=path)
            got = b.get(ev.event_id)
            assert got is not None
            assert got.actor == "alice"
            assert got.severity == Severity.MEDIUM
            assert ComplianceTag.GDPR in got.compliance_tags
            assert got.details == {"foo": 1}
            b.close()

    def test_total_events_persist(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "audit.db")
            a = DocAudit(db_path=path)
            for i in range(3):
                a.log(
                    "x", "y", "z", EventCategory.SECURITY, now=float(i)
                )
            a.close()

            b = DocAudit(db_path=path)
            assert b.total_events == 3
            b.close()


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_audit_counts(self, audit):
        assert audit.total_events == 0
        assert audit.count() == 0
        assert audit.actors_count() == 0
        assert audit.recent() == []
        assert audit.failures() == []

    def test_clear_resets(self, audit):
        _seed_events(audit)
        assert audit.total_events == 5
        audit.clear()
        assert audit.total_events == 0
        assert audit.actors_count() == 0

    def test_clear_resets_event_ids(self, audit):
        audit.log("a", "x", "y", EventCategory.SECURITY, now=1.0)
        audit.log("a", "x", "y", EventCategory.SECURITY, now=2.0)
        audit.clear()
        ev = audit.log("a", "x", "y", EventCategory.SECURITY, now=3.0)
        assert ev.event_id == 1

    def test_close_safe_to_call(self, audit):
        audit.close()
        # Should not raise on second call.
        audit.close()

    def test_empty_compliance_tags(self, audit):
        ev = audit.log("a", "x", "y", EventCategory.SECURITY, now=1.0)
        assert ev.compliance_tags == set()
        got = audit.get(ev.event_id)
        assert got.compliance_tags == set()

    def test_multiple_compliance_tags_roundtrip(self, audit):
        tags = {ComplianceTag.GDPR, ComplianceTag.HIPAA, ComplianceTag.SOX}
        ev = audit.log(
            "a", "x", "y", EventCategory.COMPLIANCE,
            compliance_tags=tags, now=1.0,
        )
        got = audit.get(ev.event_id)
        assert got.compliance_tags == tags

    def test_details_with_nested(self, audit):
        det = {"meta": {"a": [1, 2, 3]}, "n": 42}
        ev = audit.log(
            "a", "x", "y", EventCategory.SECURITY,
            details=det, now=1.0,
        )
        got = audit.get(ev.event_id)
        assert got.details == det

    def test_in_memory_isolated(self):
        a = DocAudit()
        b = DocAudit()
        a.log("x", "y", "z", EventCategory.SECURITY, now=1.0)
        assert a.total_events == 1
        assert b.total_events == 0
        a.close()
        b.close()
