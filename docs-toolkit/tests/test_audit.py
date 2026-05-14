"""Tests for docstoolkit.audit — immutable audit log with hash-chain tamper detection."""
import json
import sqlite3
import uuid
from datetime import datetime

import pytest

from docstoolkit.audit import AuditEvent, AuditLog, AuditVerifier, EventCategory, VerificationReport


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_event(
    action="doc.create",
    actor="alice",
    category=EventCategory.MUTATION,
    resource="doc-1",
    detail=None,
    event_id=None,
    ts=None,
) -> AuditEvent:
    kwargs = dict(
        event_id=event_id or str(uuid.uuid4()),
        category=category,
        action=action,
        actor=actor,
        resource=resource,
        detail=detail or {},
    )
    if ts:
        kwargs["ts"] = ts
    return AuditEvent(**kwargs)


def make_log(*events) -> AuditLog:
    log = AuditLog()
    for e in events:
        log.append(e)
    return log


# ===========================================================================
# EventCategory
# ===========================================================================

class TestEventCategory:
    def test_auth_value(self):
        assert EventCategory.AUTH.value == "auth"

    def test_access_value(self):
        assert EventCategory.ACCESS.value == "access"

    def test_mutation_value(self):
        assert EventCategory.MUTATION.value == "mutation"

    def test_admin_value(self):
        assert EventCategory.ADMIN.value == "admin"

    def test_system_value(self):
        assert EventCategory.SYSTEM.value == "system"

    def test_is_str_enum(self):
        assert isinstance(EventCategory.AUTH, str)

    def test_five_members(self):
        assert len(EventCategory) == 5

    def test_from_string(self):
        assert EventCategory("auth") is EventCategory.AUTH


# ===========================================================================
# AuditEvent
# ===========================================================================

class TestAuditEventTimestamp:
    def test_ts_auto_set_when_empty(self):
        e = make_event()
        assert e.ts != ""

    def test_ts_is_iso_format(self):
        e = make_event()
        datetime.fromisoformat(e.ts)  # must not raise

    def test_ts_respected_when_provided(self):
        ts = "2024-01-15T10:30:00"
        e = make_event(ts=ts)
        assert e.ts == ts

    def test_ts_seconds_precision(self):
        e = make_event()
        # isoformat with timespec='seconds' → no fractional seconds
        assert "." not in e.ts


class TestAuditEventComputeHash:
    def test_deterministic_same_inputs(self):
        e1 = make_event(event_id="x", action="a", actor="b", ts="2024-01-01T00:00:00")
        e2 = make_event(event_id="x", action="a", actor="b", ts="2024-01-01T00:00:00")
        assert e1.compute_hash() == e2.compute_hash()

    def test_returns_32_char_hex(self):
        e = make_event()
        h = e.compute_hash()
        assert len(h) == 32
        int(h, 16)  # must be valid hex

    def test_different_event_id_different_hash(self):
        e1 = make_event(event_id="id-1", ts="2024-01-01T00:00:00")
        e2 = make_event(event_id="id-2", ts="2024-01-01T00:00:00")
        assert e1.compute_hash() != e2.compute_hash()

    def test_different_action_different_hash(self):
        e1 = make_event(event_id="x", action="doc.create", ts="2024-01-01T00:00:00")
        e2 = make_event(event_id="x", action="doc.delete", ts="2024-01-01T00:00:00")
        assert e1.compute_hash() != e2.compute_hash()

    def test_different_actor_different_hash(self):
        e1 = make_event(event_id="x", actor="alice", ts="2024-01-01T00:00:00")
        e2 = make_event(event_id="x", actor="bob", ts="2024-01-01T00:00:00")
        assert e1.compute_hash() != e2.compute_hash()

    def test_different_category_different_hash(self):
        e1 = make_event(event_id="x", category=EventCategory.AUTH, ts="2024-01-01T00:00:00")
        e2 = make_event(event_id="x", category=EventCategory.ADMIN, ts="2024-01-01T00:00:00")
        assert e1.compute_hash() != e2.compute_hash()

    def test_different_resource_different_hash(self):
        e1 = make_event(event_id="x", resource="doc-1", ts="2024-01-01T00:00:00")
        e2 = make_event(event_id="x", resource="doc-2", ts="2024-01-01T00:00:00")
        assert e1.compute_hash() != e2.compute_hash()

    def test_different_ts_different_hash(self):
        e1 = make_event(event_id="x", ts="2024-01-01T00:00:00")
        e2 = make_event(event_id="x", ts="2024-01-02T00:00:00")
        assert e1.compute_hash() != e2.compute_hash()

    def test_different_prev_hash_different_hash(self):
        e1 = make_event(event_id="x", ts="2024-01-01T00:00:00")
        e2 = make_event(event_id="x", ts="2024-01-01T00:00:00")
        e1.prev_hash = ""
        e2.prev_hash = "abc123"
        assert e1.compute_hash() != e2.compute_hash()

    def test_hash_not_affected_by_detail(self):
        """detail is intentionally excluded from the hash."""
        e1 = make_event(event_id="x", ts="2024-01-01T00:00:00", detail={"k": "v"})
        e2 = make_event(event_id="x", ts="2024-01-01T00:00:00", detail={})
        assert e1.compute_hash() == e2.compute_hash()


class TestAuditEventSealAndVerify:
    def test_seal_sets_event_hash(self):
        e = make_event()
        assert e.event_hash == ""
        e.seal()
        assert e.event_hash != ""

    def test_seal_sets_correct_hash(self):
        e = make_event()
        e.seal()
        assert e.event_hash == e.compute_hash()

    def test_verify_true_after_seal(self):
        e = make_event()
        e.seal()
        assert e.verify() is True

    def test_verify_false_before_seal(self):
        e = make_event()
        # event_hash is "" but compute_hash() returns non-empty
        assert e.verify() is False

    def test_verify_false_after_modifying_action(self):
        e = make_event()
        e.seal()
        e.action = "doc.delete"
        assert e.verify() is False

    def test_verify_false_after_modifying_actor(self):
        e = make_event()
        e.seal()
        e.actor = "mallory"
        assert e.verify() is False

    def test_verify_false_after_modifying_ts(self):
        e = make_event()
        e.seal()
        e.ts = "1970-01-01T00:00:00"
        assert e.verify() is False

    def test_verify_false_after_modifying_resource(self):
        e = make_event()
        e.seal()
        e.resource = "evil-doc"
        assert e.verify() is False

    def test_verify_false_after_modifying_category(self):
        e = make_event()
        e.seal()
        e.category = EventCategory.ADMIN
        assert e.verify() is False

    def test_verify_false_after_modifying_prev_hash(self):
        e = make_event()
        e.seal()
        e.prev_hash = "tampered"
        assert e.verify() is False

    def test_default_prev_hash_is_empty(self):
        e = make_event()
        assert e.prev_hash == ""

    def test_default_event_hash_is_empty(self):
        e = make_event()
        assert e.event_hash == ""

    def test_seal_idempotent(self):
        """Calling seal() twice gives the same hash."""
        e = make_event()
        e.seal()
        h1 = e.event_hash
        e.seal()
        assert e.event_hash == h1


# ===========================================================================
# AuditLog
# ===========================================================================

class TestAuditLogAppendAndGet:
    def test_append_stores_event(self):
        log = AuditLog()
        e = make_event()
        log.append(e)
        assert log.count() == 1

    def test_get_round_trip(self):
        log = AuditLog()
        e = make_event(action="doc.create", actor="alice", resource="doc-99")
        log.append(e)
        fetched = log.get(e.event_id)
        assert fetched is not None
        assert fetched.event_id == e.event_id
        assert fetched.action == e.action
        assert fetched.actor == e.actor
        assert fetched.resource == e.resource

    def test_get_missing_returns_none(self):
        log = AuditLog()
        assert log.get("nonexistent-id") is None

    def test_get_preserves_category(self):
        log = AuditLog()
        e = make_event(category=EventCategory.AUTH)
        log.append(e)
        fetched = log.get(e.event_id)
        assert fetched.category == EventCategory.AUTH

    def test_get_preserves_detail(self):
        log = AuditLog()
        e = make_event(detail={"key": "value", "num": 42})
        log.append(e)
        fetched = log.get(e.event_id)
        assert fetched.detail == {"key": "value", "num": 42}

    def test_get_preserves_ts(self):
        log = AuditLog()
        ts = "2024-06-01T12:00:00"
        e = make_event(ts=ts)
        log.append(e)
        fetched = log.get(e.event_id)
        assert fetched.ts == ts

    def test_append_seals_event(self):
        log = AuditLog()
        e = make_event()
        log.append(e)
        assert e.event_hash != ""

    def test_get_event_verifies(self):
        log = AuditLog()
        e = make_event()
        log.append(e)
        fetched = log.get(e.event_id)
        assert fetched.verify() is True


class TestAuditLogListEvents:
    def test_list_returns_events_in_seq_order(self):
        log = AuditLog()
        ids = []
        for i in range(5):
            e = make_event(action=f"action.{i}", ts=f"2024-01-0{i+1}T00:00:00")
            log.append(e)
            ids.append(e.event_id)
        events = log.list_events(limit=10)
        assert [ev.event_id for ev in events] == ids

    def test_list_filter_by_category(self):
        log = AuditLog()
        e1 = make_event(category=EventCategory.AUTH)
        e2 = make_event(category=EventCategory.MUTATION)
        e3 = make_event(category=EventCategory.AUTH)
        log.append(e1)
        log.append(e2)
        log.append(e3)
        auth_events = log.list_events(category=EventCategory.AUTH)
        assert len(auth_events) == 2
        assert all(ev.category == EventCategory.AUTH for ev in auth_events)

    def test_list_filter_by_actor(self):
        log = AuditLog()
        e1 = make_event(actor="alice")
        e2 = make_event(actor="bob")
        e3 = make_event(actor="alice")
        log.append(e1)
        log.append(e2)
        log.append(e3)
        alice_events = log.list_events(actor="alice")
        assert len(alice_events) == 2
        assert all(ev.actor == "alice" for ev in alice_events)

    def test_list_filter_category_and_actor(self):
        log = AuditLog()
        e1 = make_event(actor="alice", category=EventCategory.AUTH)
        e2 = make_event(actor="bob", category=EventCategory.AUTH)
        e3 = make_event(actor="alice", category=EventCategory.MUTATION)
        log.append(e1)
        log.append(e2)
        log.append(e3)
        result = log.list_events(category=EventCategory.AUTH, actor="alice")
        assert len(result) == 1
        assert result[0].event_id == e1.event_id

    def test_list_respects_limit(self):
        log = AuditLog()
        for i in range(10):
            log.append(make_event())
        assert len(log.list_events(limit=3)) == 3

    def test_list_empty_log(self):
        log = AuditLog()
        assert log.list_events() == []


class TestAuditLogCount:
    def test_count_zero_initially(self):
        log = AuditLog()
        assert log.count() == 0

    def test_count_increments_with_appends(self):
        log = AuditLog()
        for i in range(7):
            log.append(make_event())
        assert log.count() == 7


class TestAuditLogHashChaining:
    def test_first_event_prev_hash_empty(self):
        log = AuditLog()
        e = make_event()
        log.append(e)
        assert e.prev_hash == ""

    def test_second_event_prev_hash_equals_first_event_hash(self):
        log = AuditLog()
        e1 = make_event()
        e2 = make_event()
        log.append(e1)
        log.append(e2)
        assert e2.prev_hash == e1.event_hash

    def test_chain_of_three(self):
        log = AuditLog()
        events = [make_event() for _ in range(3)]
        for e in events:
            log.append(e)
        assert events[1].prev_hash == events[0].event_hash
        assert events[2].prev_hash == events[1].event_hash

    def test_last_hash_after_single_append(self):
        log = AuditLog()
        e = make_event()
        log.append(e)
        assert log.last_hash() == e.event_hash

    def test_last_hash_after_multiple_appends(self):
        log = AuditLog()
        events = [make_event() for _ in range(5)]
        for e in events:
            log.append(e)
        assert log.last_hash() == events[-1].event_hash

    def test_last_hash_empty_initially(self):
        log = AuditLog()
        assert log.last_hash() == ""

    def test_stored_prev_hash_matches(self):
        """Round-trip: fetched event has correct prev_hash."""
        log = AuditLog()
        e1 = make_event()
        e2 = make_event()
        log.append(e1)
        log.append(e2)
        fetched2 = log.get(e2.event_id)
        assert fetched2.prev_hash == e1.event_hash

    def test_in_memory_db(self):
        log = AuditLog(db_path=None)
        e = make_event()
        log.append(e)
        assert log.count() == 1

    def test_file_db_persists(self, tmp_path):
        db_file = tmp_path / "audit.db"
        log = AuditLog(db_path=db_file)
        e = make_event()
        log.append(e)
        h = log.last_hash()
        log.close()

        log2 = AuditLog(db_path=db_file)
        assert log2.count() == 1
        assert log2.last_hash() == h
        log2.close()


# ===========================================================================
# VerificationReport
# ===========================================================================

class TestVerificationReport:
    def test_is_intact_true_when_empty_lists(self):
        r = VerificationReport(total_events=5, valid_count=5)
        assert r.is_intact() is True

    def test_is_intact_false_when_tampered(self):
        r = VerificationReport(total_events=5, valid_count=4, tampered_ids=["x"])
        assert r.is_intact() is False

    def test_is_intact_false_when_chain_broken(self):
        r = VerificationReport(total_events=5, valid_count=4, broken_chain_ids=["y"])
        assert r.is_intact() is False

    def test_is_intact_false_when_both(self):
        r = VerificationReport(
            total_events=5, valid_count=3,
            tampered_ids=["x"], broken_chain_ids=["y"]
        )
        assert r.is_intact() is False

    def test_summary_intact(self):
        r = VerificationReport(total_events=3, valid_count=3)
        s = r.summary()
        assert "INTACT" in s
        assert "3/3" in s
        assert "0 tampered" in s
        assert "0 chain breaks" in s

    def test_summary_compromised(self):
        r = VerificationReport(
            total_events=3, valid_count=1,
            tampered_ids=["a", "b"], broken_chain_ids=["c"]
        )
        s = r.summary()
        assert "COMPROMISED" in s

    def test_summary_tampered_count(self):
        r = VerificationReport(
            total_events=5, valid_count=3,
            tampered_ids=["a", "b"]
        )
        assert "2 tampered" in r.summary()

    def test_summary_chain_breaks_count(self):
        r = VerificationReport(
            total_events=5, valid_count=3,
            broken_chain_ids=["x", "y", "z"]
        )
        assert "3 chain breaks" in r.summary()


# ===========================================================================
# AuditVerifier
# ===========================================================================

class TestAuditVerifierIntact:
    def test_empty_log_intact(self):
        log = AuditLog()
        v = AuditVerifier()
        report = v.verify(log)
        assert report.is_intact() is True
        assert report.total_events == 0
        assert report.valid_count == 0

    def test_single_event_intact(self):
        log = make_log(make_event())
        report = AuditVerifier().verify(log)
        assert report.is_intact() is True
        assert report.total_events == 1
        assert report.valid_count == 1

    def test_multiple_events_intact(self):
        log = make_log(*[make_event() for _ in range(10)])
        report = AuditVerifier().verify(log)
        assert report.is_intact() is True
        assert report.total_events == 10
        assert report.valid_count == 10

    def test_valid_count_matches_total_for_clean_log(self):
        log = make_log(*[make_event() for _ in range(5)])
        report = AuditVerifier().verify(log)
        assert report.valid_count == report.total_events

    def test_tampered_ids_empty_for_clean_log(self):
        log = make_log(make_event(), make_event())
        report = AuditVerifier().verify(log)
        assert report.tampered_ids == []

    def test_broken_chain_ids_empty_for_clean_log(self):
        log = make_log(make_event(), make_event())
        report = AuditVerifier().verify(log)
        assert report.broken_chain_ids == []


class TestAuditVerifierTampering:
    def _get_conn(self, log: AuditLog) -> sqlite3.Connection:
        return log._conn

    def test_tampered_event_hash_detected(self):
        log = AuditLog()
        e = make_event()
        log.append(e)
        # Directly corrupt event_hash in DB
        conn = self._get_conn(log)
        conn.execute(
            "UPDATE audit_log SET event_hash='deadbeefdeadbeefdeadbeefdeadbeef' "
            "WHERE event_id=?", (e.event_id,)
        )
        conn.commit()
        report = AuditVerifier().verify(log)
        assert e.event_id in report.tampered_ids
        assert report.is_intact() is False

    def test_tampered_action_detected(self):
        log = AuditLog()
        e = make_event(action="doc.create")
        log.append(e)
        conn = self._get_conn(log)
        conn.execute(
            "UPDATE audit_log SET action='doc.delete' WHERE event_id=?",
            (e.event_id,)
        )
        conn.commit()
        report = AuditVerifier().verify(log)
        assert e.event_id in report.tampered_ids

    def test_tampered_actor_detected(self):
        log = AuditLog()
        e = make_event(actor="alice")
        log.append(e)
        conn = self._get_conn(log)
        conn.execute(
            "UPDATE audit_log SET actor='mallory' WHERE event_id=?",
            (e.event_id,)
        )
        conn.commit()
        report = AuditVerifier().verify(log)
        assert e.event_id in report.tampered_ids

    def test_chain_break_on_modified_prev_hash(self):
        log = AuditLog()
        e1 = make_event()
        e2 = make_event()
        log.append(e1)
        log.append(e2)
        conn = self._get_conn(log)
        conn.execute(
            "UPDATE audit_log SET prev_hash='00000000000000000000000000000000' "
            "WHERE event_id=?", (e2.event_id,)
        )
        conn.commit()
        report = AuditVerifier().verify(log)
        # e2 has wrong prev_hash → broken chain AND tampered (hash mismatch)
        assert e2.event_id in report.broken_chain_ids

    def test_verify_multiple_tampered(self):
        log = AuditLog()
        events = [make_event() for _ in range(4)]
        for e in events:
            log.append(e)
        conn = self._get_conn(log)
        # Tamper first and third
        for idx in [0, 2]:
            conn.execute(
                "UPDATE audit_log SET event_hash='aaaabbbbccccddddaaaabbbbccccdddd' "
                "WHERE event_id=?", (events[idx].event_id,)
            )
        conn.commit()
        report = AuditVerifier().verify(log)
        assert events[0].event_id in report.tampered_ids
        assert events[2].event_id in report.tampered_ids

    def test_intact_after_no_tampering(self):
        log = AuditLog()
        for _ in range(5):
            log.append(make_event())
        report = AuditVerifier().verify(log)
        assert report.is_intact() is True

    def test_valid_count_reduced_by_tampered(self):
        log = AuditLog()
        events = [make_event() for _ in range(3)]
        for e in events:
            log.append(e)
        conn = self._get_conn(log)
        conn.execute(
            "UPDATE audit_log SET event_hash='badhashbadhashbadhashbadhashbadh' "
            "WHERE event_id=?", (events[1].event_id,)
        )
        conn.commit()
        report = AuditVerifier().verify(log)
        assert report.valid_count < report.total_events

    def test_report_is_instance_of_verification_report(self):
        log = AuditLog()
        report = AuditVerifier().verify(log)
        assert isinstance(report, VerificationReport)


# ===========================================================================
# Integration
# ===========================================================================

class TestAuditIntegration:
    def test_full_workflow_intact(self):
        log = AuditLog()
        events = [
            make_event(action="user.login", actor="alice", category=EventCategory.AUTH),
            make_event(action="doc.create", actor="alice", category=EventCategory.MUTATION, resource="doc-1"),
            make_event(action="doc.read", actor="bob", category=EventCategory.ACCESS, resource="doc-1"),
            make_event(action="user.logout", actor="alice", category=EventCategory.AUTH),
        ]
        for e in events:
            log.append(e)
        report = AuditVerifier().verify(log)
        assert report.is_intact() is True
        assert report.total_events == 4

    def test_all_events_verify_individually(self):
        log = AuditLog()
        originals = [make_event() for _ in range(5)]
        for e in originals:
            log.append(e)
        for e in log.list_events(limit=10):
            assert e.verify(), f"Event {e.event_id} failed verify()"

    def test_chain_integrity_via_list(self):
        log = AuditLog()
        for _ in range(6):
            log.append(make_event())
        events = log.list_events(limit=10)
        prev_hash = ""
        for ev in events:
            assert ev.prev_hash == prev_hash
            prev_hash = ev.event_hash

    def test_filter_and_chain(self):
        log = AuditLog()
        log.append(make_event(category=EventCategory.AUTH, actor="alice"))
        log.append(make_event(category=EventCategory.MUTATION, actor="alice"))
        log.append(make_event(category=EventCategory.AUTH, actor="bob"))
        assert log.count() == 3
        assert len(log.list_events(category=EventCategory.AUTH)) == 2
        assert AuditVerifier().verify(log).is_intact() is True
