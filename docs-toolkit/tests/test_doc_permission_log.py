"""Tests for docstoolkit.doc_permission_log (E296).

Coverage (≥45 tests):
  - PermissionEvent: fields, auto-id increments, reason default
  - PermissionSummary: fields, current_state mapping
  - PermLogStats: fields and type
  - DocPermissionLog.log: returns event, stores event, auto-id, timestamps
  - DocPermissionLog.get_event: found / not found
  - DocPermissionLog.events_for_doc: all, filtered by principal, ordering, empty
  - DocPermissionLog.events_for_principal: all, filtered by doc_id, ordering, empty
  - DocPermissionLog.current_state: grant/deny/revoke/None, latest-wins
  - DocPermissionLog.summary: None when empty, fields, event_count, current_state
  - DocPermissionLog.has_permission: True/False cases
  - DocPermissionLog.docs_where_granted: empty, single, multiple, sorted, revoke removes
  - DocPermissionLog.stats: counts, totals, event_type_counts
  - DocPermissionLog.total_events: property
  - Thread safety: concurrent writes produce correct count
"""
import threading

import pytest

from docstoolkit.doc_permission_log import (
    DocPermissionLog,
    PermissionEvent,
    PermissionSummary,
    PermLogStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _plog() -> DocPermissionLog:
    return DocPermissionLog()


def _grant(log: DocPermissionLog, doc="doc1", principal="alice",
           action="read", granted_by="admin", reason="", now=1.0) -> PermissionEvent:
    return log.log(doc, principal, action, "grant",
                   granted_by=granted_by, reason=reason, now=now)


def _deny(log: DocPermissionLog, doc="doc1", principal="alice",
          action="read", granted_by="admin", now=2.0) -> PermissionEvent:
    return log.log(doc, principal, action, "deny",
                   granted_by=granted_by, now=now)


def _revoke(log: DocPermissionLog, doc="doc1", principal="alice",
            action="read", granted_by="admin", now=3.0) -> PermissionEvent:
    return log.log(doc, principal, action, "revoke",
                   granted_by=granted_by, now=now)


# ===========================================================================
# PermissionEvent dataclass
# ===========================================================================

class TestPermissionEvent:
    def test_fields_stored(self):
        ev = PermissionEvent(
            event_id=1,
            doc_id="docA",
            principal="alice",
            action="write",
            event_type="grant",
            granted_by="admin",
            timestamp=100.0,
            reason="initial grant",
        )
        assert ev.event_id == 1
        assert ev.doc_id == "docA"
        assert ev.principal == "alice"
        assert ev.action == "write"
        assert ev.event_type == "grant"
        assert ev.granted_by == "admin"
        assert ev.timestamp == 100.0
        assert ev.reason == "initial grant"

    def test_reason_defaults_to_empty(self):
        ev = PermissionEvent(
            event_id=1, doc_id="d", principal="u",
            action="read", event_type="grant", granted_by="g", timestamp=0.0,
        )
        assert ev.reason == ""

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(PermissionEvent)


# ===========================================================================
# PermissionSummary dataclass
# ===========================================================================

class TestPermissionSummary:
    def test_fields(self):
        s = PermissionSummary(
            doc_id="d1",
            principal="bob",
            current_state="grant",
            last_event_at=50.0,
            event_count=3,
        )
        assert s.doc_id == "d1"
        assert s.principal == "bob"
        assert s.current_state == "grant"
        assert s.last_event_at == 50.0
        assert s.event_count == 3

    def test_current_state_none(self):
        s = PermissionSummary(
            doc_id="d", principal="u",
            current_state=None, last_event_at=0.0, event_count=1,
        )
        assert s.current_state is None


# ===========================================================================
# PermLogStats dataclass
# ===========================================================================

class TestPermLogStats:
    def test_fields(self):
        st = PermLogStats(
            total_events=10,
            total_docs=3,
            total_principals=2,
            event_type_counts={"grant": 5, "deny": 3, "revoke": 2},
        )
        assert st.total_events == 10
        assert st.total_docs == 3
        assert st.total_principals == 2
        assert st.event_type_counts == {"grant": 5, "deny": 3, "revoke": 2}


# ===========================================================================
# DocPermissionLog.log  (append)
# ===========================================================================

class TestDocPermissionLogLog:
    def test_log_returns_permission_event(self):
        log = _plog()
        ev = _grant(log)
        assert isinstance(ev, PermissionEvent)

    def test_event_id_starts_at_one(self):
        log = _plog()
        ev = _grant(log)
        assert ev.event_id == 1

    def test_event_id_auto_increments(self):
        log = _plog()
        ev1 = _grant(log)
        ev2 = _deny(log)
        assert ev2.event_id == ev1.event_id + 1

    def test_event_id_increments_by_one_each_time(self):
        log = _plog()
        ids = [log.log("d", "u", "read", "grant", now=float(i)).event_id
               for i in range(5)]
        assert ids == list(range(1, 6))

    def test_log_stores_doc_id(self):
        log = _plog()
        ev = log.log("myDoc", "alice", "write", "grant", now=1.0)
        assert ev.doc_id == "myDoc"

    def test_log_stores_principal(self):
        log = _plog()
        ev = log.log("d", "charlie", "read", "deny", now=1.0)
        assert ev.principal == "charlie"

    def test_log_stores_action(self):
        log = _plog()
        ev = log.log("d", "u", "delete", "grant", now=1.0)
        assert ev.action == "delete"

    def test_log_stores_event_type(self):
        log = _plog()
        ev = log.log("d", "u", "read", "revoke", now=1.0)
        assert ev.event_type == "revoke"

    def test_log_stores_granted_by(self):
        log = _plog()
        ev = log.log("d", "u", "read", "grant", granted_by="superadmin", now=1.0)
        assert ev.granted_by == "superadmin"

    def test_log_stores_reason(self):
        log = _plog()
        ev = log.log("d", "u", "read", "grant", reason="GDPR compliance", now=1.0)
        assert ev.reason == "GDPR compliance"

    def test_log_stores_timestamp(self):
        log = _plog()
        ev = log.log("d", "u", "read", "grant", now=999.5)
        assert ev.timestamp == 999.5

    def test_log_now_none_defaults_to_zero(self):
        log = _plog()
        ev = log.log("d", "u", "read", "grant")
        assert ev.timestamp == 0.0

    def test_total_events_increases(self):
        log = _plog()
        _grant(log)
        assert log.total_events == 1
        _deny(log)
        assert log.total_events == 2

    def test_log_multiple_events_different_docs(self):
        log = _plog()
        log.log("docA", "alice", "read", "grant", now=1.0)
        log.log("docB", "bob", "write", "deny", now=2.0)
        assert log.total_events == 2


# ===========================================================================
# DocPermissionLog.get_event
# ===========================================================================

class TestGetEvent:
    def test_get_existing_event(self):
        log = _plog()
        ev = _grant(log)
        fetched = log.get_event(ev.event_id)
        assert fetched is not None
        assert fetched.event_id == ev.event_id

    def test_get_returns_correct_event(self):
        log = _plog()
        ev1 = _grant(log, doc="d1", now=1.0)
        ev2 = _deny(log, doc="d2", now=2.0)
        assert log.get_event(ev1.event_id).doc_id == "d1"
        assert log.get_event(ev2.event_id).doc_id == "d2"

    def test_get_missing_returns_none(self):
        log = _plog()
        assert log.get_event(9999) is None

    def test_get_zero_returns_none(self):
        log = _plog()
        assert log.get_event(0) is None

    def test_get_all_stored_events(self):
        log = _plog()
        events = [log.log("d", "u", "read", "grant", now=float(i)) for i in range(5)]
        for ev in events:
            assert log.get_event(ev.event_id) is not None


# ===========================================================================
# DocPermissionLog.events_for_doc
# ===========================================================================

class TestEventsForDoc:
    def setup_method(self):
        self.log = _plog()
        self.ev1 = self.log.log("docA", "alice", "read",  "grant",  now=1.0)
        self.ev2 = self.log.log("docA", "alice", "write", "deny",   now=2.0)
        self.ev3 = self.log.log("docA", "bob",   "read",  "grant",  now=3.0)
        self.ev4 = self.log.log("docB", "alice", "read",  "grant",  now=4.0)

    def test_returns_all_events_for_doc(self):
        results = self.log.events_for_doc("docA")
        assert len(results) == 3

    def test_excludes_other_docs(self):
        results = self.log.events_for_doc("docA")
        assert all(e.doc_id == "docA" for e in results)

    def test_empty_doc_returns_empty(self):
        assert self.log.events_for_doc("unknown") == []

    def test_ordered_newest_first(self):
        results = self.log.events_for_doc("docA")
        timestamps = [e.timestamp for e in results]
        assert timestamps == sorted(timestamps, reverse=True)

    def test_filter_by_principal(self):
        results = self.log.events_for_doc("docA", principal="alice")
        assert len(results) == 2
        assert all(e.principal == "alice" for e in results)

    def test_filter_by_principal_no_match(self):
        results = self.log.events_for_doc("docA", principal="ghost")
        assert results == []

    def test_filter_by_principal_single_result(self):
        results = self.log.events_for_doc("docA", principal="bob")
        assert len(results) == 1
        assert results[0].event_id == self.ev3.event_id

    def test_single_event_doc(self):
        results = self.log.events_for_doc("docB")
        assert len(results) == 1
        assert results[0].event_id == self.ev4.event_id


# ===========================================================================
# DocPermissionLog.events_for_principal
# ===========================================================================

class TestEventsForPrincipal:
    def setup_method(self):
        self.log = _plog()
        self.ev1 = self.log.log("docA", "alice", "read",  "grant",  now=1.0)
        self.ev2 = self.log.log("docB", "alice", "write", "deny",   now=2.0)
        self.ev3 = self.log.log("docA", "bob",   "read",  "grant",  now=3.0)
        self.ev4 = self.log.log("docC", "alice", "read",  "revoke", now=4.0)

    def test_returns_all_events_for_principal(self):
        results = self.log.events_for_principal("alice")
        assert len(results) == 3

    def test_excludes_other_principals(self):
        results = self.log.events_for_principal("alice")
        assert all(e.principal == "alice" for e in results)

    def test_empty_principal_returns_empty(self):
        assert self.log.events_for_principal("ghost") == []

    def test_ordered_newest_first(self):
        results = self.log.events_for_principal("alice")
        timestamps = [e.timestamp for e in results]
        assert timestamps == sorted(timestamps, reverse=True)

    def test_filter_by_doc_id(self):
        results = self.log.events_for_principal("alice", doc_id="docA")
        assert len(results) == 1
        assert results[0].event_id == self.ev1.event_id

    def test_filter_by_doc_id_no_match(self):
        results = self.log.events_for_principal("alice", doc_id="docZ")
        assert results == []

    def test_single_event_principal(self):
        results = self.log.events_for_principal("bob")
        assert len(results) == 1
        assert results[0].event_id == self.ev3.event_id


# ===========================================================================
# DocPermissionLog.current_state
# ===========================================================================

class TestCurrentState:
    def test_grant_returns_grant(self):
        log = _plog()
        _grant(log, now=1.0)
        assert log.current_state("doc1", "alice", "read") == "grant"

    def test_deny_returns_deny(self):
        log = _plog()
        _deny(log, now=2.0)
        assert log.current_state("doc1", "alice", "read") == "deny"

    def test_revoke_returns_revoke(self):
        log = _plog()
        _revoke(log, now=3.0)
        assert log.current_state("doc1", "alice", "read") == "revoke"

    def test_no_events_returns_none(self):
        log = _plog()
        assert log.current_state("doc1", "alice", "read") is None

    def test_latest_event_wins_grant_then_revoke(self):
        log = _plog()
        _grant(log, now=1.0)
        _revoke(log, now=2.0)
        assert log.current_state("doc1", "alice", "read") == "revoke"

    def test_latest_event_wins_revoke_then_grant(self):
        log = _plog()
        _revoke(log, now=1.0)
        _grant(log, now=2.0)
        assert log.current_state("doc1", "alice", "read") == "grant"

    def test_different_actions_are_independent(self):
        log = _plog()
        log.log("doc1", "alice", "read",  "grant",  now=1.0)
        log.log("doc1", "alice", "write", "deny",   now=2.0)
        assert log.current_state("doc1", "alice", "read")  == "grant"
        assert log.current_state("doc1", "alice", "write") == "deny"

    def test_different_principals_are_independent(self):
        log = _plog()
        log.log("doc1", "alice", "read", "grant", now=1.0)
        log.log("doc1", "bob",   "read", "deny",  now=2.0)
        assert log.current_state("doc1", "alice", "read") == "grant"
        assert log.current_state("doc1", "bob",   "read") == "deny"

    def test_different_docs_are_independent(self):
        log = _plog()
        log.log("docA", "alice", "read", "grant",  now=1.0)
        log.log("docB", "alice", "read", "deny",   now=2.0)
        assert log.current_state("docA", "alice", "read") == "grant"
        assert log.current_state("docB", "alice", "read") == "deny"


# ===========================================================================
# DocPermissionLog.summary
# ===========================================================================

class TestSummary:
    def test_none_when_no_events(self):
        log = _plog()
        assert log.summary("doc1", "alice") is None

    def test_returns_permission_summary_instance(self):
        log = _plog()
        _grant(log, now=5.0)
        s = log.summary("doc1", "alice")
        assert isinstance(s, PermissionSummary)

    def test_doc_id_and_principal_set(self):
        log = _plog()
        _grant(log, doc="docX", principal="carol", now=1.0)
        s = log.summary("docX", "carol")
        assert s.doc_id == "docX"
        assert s.principal == "carol"

    def test_event_count(self):
        log = _plog()
        _grant(log, now=1.0)
        _deny(log, now=2.0)
        _revoke(log, now=3.0)
        s = log.summary("doc1", "alice")
        assert s.event_count == 3

    def test_last_event_at(self):
        log = _plog()
        _grant(log, now=10.0)
        _deny(log, now=20.0)
        s = log.summary("doc1", "alice")
        assert s.last_event_at == 20.0

    def test_current_state_grant(self):
        log = _plog()
        _grant(log, now=1.0)
        s = log.summary("doc1", "alice")
        assert s.current_state == "grant"

    def test_current_state_deny(self):
        log = _plog()
        _deny(log, now=1.0)
        s = log.summary("doc1", "alice")
        assert s.current_state == "deny"

    def test_current_state_none_after_revoke(self):
        log = _plog()
        _grant(log, now=1.0)
        _revoke(log, now=2.0)
        s = log.summary("doc1", "alice")
        assert s.current_state is None

    def test_summary_ignores_other_principals(self):
        log = _plog()
        _grant(log, principal="alice", now=1.0)
        log.log("doc1", "bob", "read", "deny", now=2.0)
        s = log.summary("doc1", "alice")
        assert s.event_count == 1


# ===========================================================================
# DocPermissionLog.has_permission
# ===========================================================================

class TestHasPermission:
    def test_true_when_granted(self):
        log = _plog()
        _grant(log, now=1.0)
        assert log.has_permission("doc1", "alice", "read") is True

    def test_false_when_denied(self):
        log = _plog()
        _deny(log, now=1.0)
        assert log.has_permission("doc1", "alice", "read") is False

    def test_false_when_revoked(self):
        log = _plog()
        _grant(log, now=1.0)
        _revoke(log, now=2.0)
        assert log.has_permission("doc1", "alice", "read") is False

    def test_false_when_no_events(self):
        log = _plog()
        assert log.has_permission("doc1", "alice", "read") is False

    def test_true_after_re_grant(self):
        log = _plog()
        _grant(log, now=1.0)
        _revoke(log, now=2.0)
        _grant(log, now=3.0)
        assert log.has_permission("doc1", "alice", "read") is True

    def test_action_specific(self):
        log = _plog()
        log.log("doc1", "alice", "read",  "grant", now=1.0)
        log.log("doc1", "alice", "write", "deny",  now=2.0)
        assert log.has_permission("doc1", "alice", "read")  is True
        assert log.has_permission("doc1", "alice", "write") is False


# ===========================================================================
# DocPermissionLog.docs_where_granted
# ===========================================================================

class TestDocsWhereGranted:
    def test_empty_when_no_events(self):
        log = _plog()
        assert log.docs_where_granted("alice", "read") == []

    def test_single_granted_doc(self):
        log = _plog()
        log.log("docA", "alice", "read", "grant", now=1.0)
        assert log.docs_where_granted("alice", "read") == ["docA"]

    def test_multiple_granted_docs_sorted(self):
        log = _plog()
        log.log("docC", "alice", "read", "grant", now=1.0)
        log.log("docA", "alice", "read", "grant", now=2.0)
        log.log("docB", "alice", "read", "grant", now=3.0)
        assert log.docs_where_granted("alice", "read") == ["docA", "docB", "docC"]

    def test_revoke_removes_doc(self):
        log = _plog()
        log.log("docA", "alice", "read", "grant",  now=1.0)
        log.log("docB", "alice", "read", "grant",  now=2.0)
        log.log("docA", "alice", "read", "revoke", now=3.0)
        assert log.docs_where_granted("alice", "read") == ["docB"]

    def test_deny_not_included(self):
        log = _plog()
        log.log("docA", "alice", "read", "deny", now=1.0)
        assert log.docs_where_granted("alice", "read") == []

    def test_action_specific(self):
        log = _plog()
        log.log("docA", "alice", "read",  "grant", now=1.0)
        log.log("docA", "alice", "write", "deny",  now=2.0)
        assert log.docs_where_granted("alice", "read")  == ["docA"]
        assert log.docs_where_granted("alice", "write") == []

    def test_principal_specific(self):
        log = _plog()
        log.log("docA", "alice", "read", "grant", now=1.0)
        log.log("docA", "bob",   "read", "deny",  now=2.0)
        assert log.docs_where_granted("alice", "read") == ["docA"]
        assert log.docs_where_granted("bob",   "read") == []

    def test_unknown_principal_returns_empty(self):
        log = _plog()
        log.log("docA", "alice", "read", "grant", now=1.0)
        assert log.docs_where_granted("ghost", "read") == []


# ===========================================================================
# DocPermissionLog.stats
# ===========================================================================

class TestStats:
    def test_empty_log_stats(self):
        s = _plog().stats()
        assert s.total_events == 0
        assert s.total_docs == 0
        assert s.total_principals == 0
        assert s.event_type_counts == {}

    def test_returns_perm_log_stats_instance(self):
        assert isinstance(_plog().stats(), PermLogStats)

    def test_total_events(self):
        log = _plog()
        for _ in range(4):
            _grant(log)
        assert log.stats().total_events == 4

    def test_total_docs(self):
        log = _plog()
        log.log("docA", "alice", "read", "grant", now=1.0)
        log.log("docB", "alice", "read", "grant", now=2.0)
        assert log.stats().total_docs == 2

    def test_total_docs_same_doc_multiple_events(self):
        log = _plog()
        log.log("docA", "alice", "read", "grant",  now=1.0)
        log.log("docA", "alice", "read", "revoke", now=2.0)
        assert log.stats().total_docs == 1

    def test_total_principals(self):
        log = _plog()
        log.log("docA", "alice", "read", "grant", now=1.0)
        log.log("docA", "bob",   "read", "grant", now=2.0)
        assert log.stats().total_principals == 2

    def test_event_type_counts_grant(self):
        log = _plog()
        _grant(log, now=1.0)
        _grant(log, now=2.0)
        assert log.stats().event_type_counts.get("grant") == 2

    def test_event_type_counts_deny(self):
        log = _plog()
        _deny(log, now=1.0)
        assert log.stats().event_type_counts.get("deny") == 1

    def test_event_type_counts_revoke(self):
        log = _plog()
        _revoke(log, now=1.0)
        assert log.stats().event_type_counts.get("revoke") == 1

    def test_event_type_counts_mixed(self):
        log = _plog()
        _grant(log, now=1.0)
        _deny(log, now=2.0)
        _revoke(log, now=3.0)
        _grant(log, now=4.0)
        counts = log.stats().event_type_counts
        assert counts["grant"]  == 2
        assert counts["deny"]   == 1
        assert counts["revoke"] == 1


# ===========================================================================
# DocPermissionLog.total_events property
# ===========================================================================

class TestTotalEventsProperty:
    def test_starts_at_zero(self):
        assert _plog().total_events == 0

    def test_increments_on_log(self):
        log = _plog()
        _grant(log)
        assert log.total_events == 1

    def test_counts_all_event_types(self):
        log = _plog()
        _grant(log, now=1.0)
        _deny(log, now=2.0)
        _revoke(log, now=3.0)
        assert log.total_events == 3


# ===========================================================================
# Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_writes_correct_count(self):
        log = _plog()
        errors = []

        def writer(n, doc):
            try:
                for i in range(n):
                    log.log(doc, "alice", "read", "grant", now=float(i))
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=writer, args=(20, f"doc{t}"))
            for t in range(5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert log.total_events == 100

    def test_concurrent_writes_unique_ids(self):
        log = _plog()

        results = []
        lock = threading.Lock()

        def writer():
            ev = log.log("doc", "user", "read", "grant", now=0.0)
            with lock:
                results.append(ev.event_id)

        threads = [threading.Thread(target=writer) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(set(results)) == 50
