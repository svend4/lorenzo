"""Tests for docstoolkit.audit_logger (E60).

Coverage:
  - AuditAction enum values
  - AuditEvent: fields, defaults, to_dict
  - AuditStore: record, get, query (all filters), count, recent
  - AuditLogger: log, query, recent, actor_summary, export_jsonl
  - Edge cases: empty store, no-match queries, export empty store
"""
import json
import time
from pathlib import Path

import pytest

from docstoolkit.audit_logger import AuditAction, AuditEvent, AuditLogger, AuditStore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_event(**kwargs) -> AuditEvent:
    defaults = dict(
        action=AuditAction.CREATE,
        actor="alice",
        resource="doc/readme.md",
    )
    defaults.update(kwargs)
    return AuditEvent(**defaults)


def store_with_events(events: list[AuditEvent]) -> AuditStore:
    store = AuditStore()
    for ev in events:
        store.record(ev)
    return store


# ===========================================================================
# AuditAction enum
# ===========================================================================

class TestAuditAction:
    def test_create_value(self):
        assert AuditAction.CREATE.value == "CREATE"

    def test_read_value(self):
        assert AuditAction.READ.value == "READ"

    def test_update_value(self):
        assert AuditAction.UPDATE.value == "UPDATE"

    def test_delete_value(self):
        assert AuditAction.DELETE.value == "DELETE"

    def test_search_value(self):
        assert AuditAction.SEARCH.value == "SEARCH"

    def test_export_value(self):
        assert AuditAction.EXPORT.value == "EXPORT"

    def test_login_value(self):
        assert AuditAction.LOGIN.value == "LOGIN"

    def test_logout_value(self):
        assert AuditAction.LOGOUT.value == "LOGOUT"

    def test_permission_change_value(self):
        assert AuditAction.PERMISSION_CHANGE.value == "PERMISSION_CHANGE"

    def test_config_change_value(self):
        assert AuditAction.CONFIG_CHANGE.value == "CONFIG_CHANGE"

    def test_total_member_count(self):
        assert len(AuditAction) == 10

    def test_is_str_enum(self):
        assert isinstance(AuditAction.LOGIN, str)

    def test_lookup_by_value(self):
        assert AuditAction("DELETE") is AuditAction.DELETE


# ===========================================================================
# AuditEvent
# ===========================================================================

class TestAuditEventDefaults:
    def test_event_id_generated(self):
        ev = make_event()
        assert ev.event_id
        assert isinstance(ev.event_id, str)
        assert len(ev.event_id) == 32  # uuid4().hex

    def test_event_id_unique(self):
        ev1 = make_event()
        ev2 = make_event()
        assert ev1.event_id != ev2.event_id

    def test_ts_set_to_now(self):
        before = time.time()
        ev = make_event()
        after = time.time()
        assert before <= ev.ts <= after

    def test_resource_id_default_empty(self):
        ev = make_event()
        assert ev.resource_id == ""

    def test_details_default_empty_dict(self):
        ev = make_event()
        assert ev.details == {}

    def test_details_not_shared(self):
        ev1 = make_event()
        ev2 = make_event()
        ev1.details["x"] = 1
        assert "x" not in ev2.details

    def test_outcome_default_success(self):
        ev = make_event()
        assert ev.outcome == "success"

    def test_ip_address_default_empty(self):
        ev = make_event()
        assert ev.ip_address == ""

    def test_session_id_default_empty(self):
        ev = make_event()
        assert ev.session_id == ""


class TestAuditEventFields:
    def test_action_stored(self):
        ev = make_event(action=AuditAction.DELETE)
        assert ev.action is AuditAction.DELETE

    def test_actor_stored(self):
        ev = make_event(actor="bob")
        assert ev.actor == "bob"

    def test_resource_stored(self):
        ev = make_event(resource="config.yaml")
        assert ev.resource == "config.yaml"

    def test_resource_id_stored(self):
        ev = make_event(resource_id="abc-123")
        assert ev.resource_id == "abc-123"

    def test_details_stored(self):
        ev = make_event(details={"key": "value"})
        assert ev.details == {"key": "value"}

    def test_outcome_failure(self):
        ev = make_event(outcome="failure")
        assert ev.outcome == "failure"

    def test_ip_address_stored(self):
        ev = make_event(ip_address="192.168.1.1")
        assert ev.ip_address == "192.168.1.1"

    def test_session_id_stored(self):
        ev = make_event(session_id="sess-xyz")
        assert ev.session_id == "sess-xyz"

    def test_custom_event_id(self):
        ev = AuditEvent(
            event_id="myid",
            action=AuditAction.READ,
            actor="alice",
            resource="file.md",
        )
        assert ev.event_id == "myid"


class TestAuditEventToDict:
    def setup_method(self):
        self.ev = AuditEvent(
            event_id="fixed-id",
            action=AuditAction.UPDATE,
            actor="carol",
            resource="page.md",
            resource_id="r-99",
            details={"field": "title"},
            outcome="success",
            ts=1_000_000.0,
            ip_address="10.0.0.1",
            session_id="s-42",
        )
        self.d = self.ev.to_dict()

    def test_returns_dict(self):
        assert isinstance(self.d, dict)

    def test_event_id(self):
        assert self.d["event_id"] == "fixed-id"

    def test_action_is_string(self):
        assert self.d["action"] == "UPDATE"
        assert isinstance(self.d["action"], str)

    def test_actor(self):
        assert self.d["actor"] == "carol"

    def test_resource(self):
        assert self.d["resource"] == "page.md"

    def test_resource_id(self):
        assert self.d["resource_id"] == "r-99"

    def test_details(self):
        assert self.d["details"] == {"field": "title"}

    def test_outcome(self):
        assert self.d["outcome"] == "success"

    def test_ts(self):
        assert self.d["ts"] == 1_000_000.0

    def test_ip_address(self):
        assert self.d["ip_address"] == "10.0.0.1"

    def test_session_id(self):
        assert self.d["session_id"] == "s-42"

    def test_all_keys_present(self):
        expected = {
            "event_id", "action", "actor", "resource", "resource_id",
            "details", "outcome", "ts", "ip_address", "session_id",
        }
        assert set(self.d.keys()) == expected


# ===========================================================================
# AuditStore
# ===========================================================================

class TestAuditStoreEmpty:
    def test_count_zero(self):
        s = AuditStore()
        assert s.count() == 0

    def test_recent_empty(self):
        s = AuditStore()
        assert s.recent() == []

    def test_get_missing(self):
        s = AuditStore()
        assert s.get("nonexistent") is None

    def test_query_empty(self):
        s = AuditStore()
        assert s.query() == []


class TestAuditStoreRecord:
    def test_record_increases_count(self):
        s = AuditStore()
        s.record(make_event())
        assert s.count() == 1

    def test_record_multiple(self):
        s = AuditStore()
        for _ in range(5):
            s.record(make_event())
        assert s.count() == 5

    def test_get_returns_event(self):
        s = AuditStore()
        ev = make_event()
        s.record(ev)
        fetched = s.get(ev.event_id)
        assert fetched is not None
        assert fetched.event_id == ev.event_id

    def test_get_preserves_action(self):
        s = AuditStore()
        ev = make_event(action=AuditAction.EXPORT)
        s.record(ev)
        assert s.get(ev.event_id).action is AuditAction.EXPORT

    def test_get_preserves_actor(self):
        s = AuditStore()
        ev = make_event(actor="dave")
        s.record(ev)
        assert s.get(ev.event_id).actor == "dave"

    def test_get_preserves_resource(self):
        s = AuditStore()
        ev = make_event(resource="notes.md")
        s.record(ev)
        assert s.get(ev.event_id).resource == "notes.md"

    def test_get_preserves_details(self):
        s = AuditStore()
        ev = make_event(details={"x": 42})
        s.record(ev)
        assert s.get(ev.event_id).details == {"x": 42}

    def test_get_preserves_outcome(self):
        s = AuditStore()
        ev = make_event(outcome="failure")
        s.record(ev)
        assert s.get(ev.event_id).outcome == "failure"

    def test_get_preserves_ip(self):
        s = AuditStore()
        ev = make_event(ip_address="1.2.3.4")
        s.record(ev)
        assert s.get(ev.event_id).ip_address == "1.2.3.4"

    def test_get_preserves_session(self):
        s = AuditStore()
        ev = make_event(session_id="S1")
        s.record(ev)
        assert s.get(ev.event_id).session_id == "S1"

    def test_get_not_found(self):
        s = AuditStore()
        s.record(make_event())
        assert s.get("no-such-id") is None


class TestAuditStoreQueryFilters:
    def setup_method(self):
        self.store = AuditStore()
        t = 1_000_000.0
        self.ev_alice_create = AuditEvent(
            event_id="e1", action=AuditAction.CREATE, actor="alice",
            resource="doc/a.md", ts=t,
        )
        self.ev_alice_read = AuditEvent(
            event_id="e2", action=AuditAction.READ, actor="alice",
            resource="doc/b.md", ts=t + 10,
        )
        self.ev_bob_delete = AuditEvent(
            event_id="e3", action=AuditAction.DELETE, actor="bob",
            resource="doc/a.md", ts=t + 20,
        )
        self.ev_bob_login = AuditEvent(
            event_id="e4", action=AuditAction.LOGIN, actor="bob",
            resource="system", ts=t + 30,
        )
        for ev in [self.ev_alice_create, self.ev_alice_read,
                   self.ev_bob_delete, self.ev_bob_login]:
            self.store.record(ev)

    def test_query_all(self):
        assert len(self.store.query()) == 4

    def test_query_by_actor_alice(self):
        results = self.store.query(actor="alice")
        assert len(results) == 2
        assert all(r.actor == "alice" for r in results)

    def test_query_by_actor_bob(self):
        results = self.store.query(actor="bob")
        assert len(results) == 2
        assert all(r.actor == "bob" for r in results)

    def test_query_by_actor_no_match(self):
        assert self.store.query(actor="nobody") == []

    def test_query_by_action_create(self):
        results = self.store.query(action=AuditAction.CREATE)
        assert len(results) == 1
        assert results[0].event_id == "e1"

    def test_query_by_action_delete(self):
        results = self.store.query(action=AuditAction.DELETE)
        assert len(results) == 1
        assert results[0].event_id == "e3"

    def test_query_by_action_no_match(self):
        assert self.store.query(action=AuditAction.EXPORT) == []

    def test_query_by_resource(self):
        results = self.store.query(resource="doc/a.md")
        assert len(results) == 2

    def test_query_by_resource_no_match(self):
        assert self.store.query(resource="missing.md") == []

    def test_query_since(self):
        results = self.store.query(since=1_000_025.0)
        assert len(results) == 1
        assert results[0].event_id == "e4"

    def test_query_until(self):
        results = self.store.query(until=1_000_005.0)
        assert len(results) == 1
        assert results[0].event_id == "e1"

    def test_query_since_until_range(self):
        results = self.store.query(since=1_000_005.0, until=1_000_025.0)
        assert len(results) == 2

    def test_query_limit(self):
        results = self.store.query(limit=2)
        assert len(results) == 2

    def test_query_limit_one(self):
        results = self.store.query(limit=1)
        assert len(results) == 1

    def test_query_combined_actor_and_action(self):
        results = self.store.query(actor="alice", action=AuditAction.READ)
        assert len(results) == 1
        assert results[0].event_id == "e2"

    def test_query_combined_actor_resource(self):
        results = self.store.query(actor="bob", resource="doc/a.md")
        assert len(results) == 1
        assert results[0].event_id == "e3"

    def test_query_ordered_newest_first(self):
        results = self.store.query()
        tss = [r.ts for r in results]
        assert tss == sorted(tss, reverse=True)


class TestAuditStoreCount:
    def setup_method(self):
        self.store = AuditStore()
        self.store.record(make_event(actor="alice", action=AuditAction.CREATE))
        self.store.record(make_event(actor="alice", action=AuditAction.READ))
        self.store.record(make_event(actor="bob", action=AuditAction.CREATE))

    def test_count_all(self):
        assert self.store.count() == 3

    def test_count_by_actor(self):
        assert self.store.count(actor="alice") == 2

    def test_count_by_actor_single(self):
        assert self.store.count(actor="bob") == 1

    def test_count_by_action(self):
        assert self.store.count(action=AuditAction.CREATE) == 2

    def test_count_by_actor_and_action(self):
        assert self.store.count(actor="alice", action=AuditAction.CREATE) == 1

    def test_count_no_match(self):
        assert self.store.count(actor="ghost") == 0


class TestAuditStoreRecent:
    def test_recent_returns_n(self):
        s = AuditStore()
        for _ in range(10):
            s.record(make_event())
        assert len(s.recent(5)) == 5

    def test_recent_default_20(self):
        s = AuditStore()
        for _ in range(25):
            s.record(make_event())
        assert len(s.recent()) == 20

    def test_recent_less_than_n(self):
        s = AuditStore()
        for _ in range(3):
            s.record(make_event())
        assert len(s.recent(10)) == 3

    def test_recent_ordered_newest_first(self):
        s = AuditStore()
        t = 1_000_000.0
        for i in range(5):
            s.record(AuditEvent(
                event_id=f"ev{i}", action=AuditAction.READ,
                actor="user", resource="r", ts=t + i,
            ))
        tss = [r.ts for r in s.recent()]
        assert tss == sorted(tss, reverse=True)


class TestAuditStoreClose:
    def test_close_no_error(self):
        s = AuditStore()
        s.record(make_event())
        s.close()  # Should not raise


# ===========================================================================
# AuditLogger
# ===========================================================================

class TestAuditLoggerLog:
    def test_log_returns_audit_event(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.CREATE, "alice", "doc.md")
        assert isinstance(ev, AuditEvent)

    def test_log_stores_event(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.READ, "bob", "notes.md")
        assert logger._store.get(ev.event_id) is not None

    def test_log_action(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.DELETE, "alice", "old.md")
        assert ev.action is AuditAction.DELETE

    def test_log_actor(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.LOGIN, "carol", "system")
        assert ev.actor == "carol"

    def test_log_resource(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.UPDATE, "alice", "readme.md")
        assert ev.resource == "readme.md"

    def test_log_kwargs_resource_id(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.CREATE, "alice", "doc", resource_id="r-1")
        assert ev.resource_id == "r-1"

    def test_log_kwargs_details(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.UPDATE, "alice", "doc", details={"field": "body"})
        assert ev.details == {"field": "body"}

    def test_log_kwargs_outcome_failure(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.LOGIN, "user", "auth", outcome="failure")
        assert ev.outcome == "failure"

    def test_log_kwargs_ip_address(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.LOGIN, "user", "auth", ip_address="1.2.3.4")
        assert ev.ip_address == "1.2.3.4"

    def test_log_kwargs_session_id(self):
        logger = AuditLogger()
        ev = logger.log(AuditAction.READ, "user", "doc", session_id="s-99")
        assert ev.session_id == "s-99"

    def test_log_uses_provided_store(self):
        store = AuditStore()
        logger = AuditLogger(store=store)
        ev = logger.log(AuditAction.SEARCH, "alice", "index")
        assert store.get(ev.event_id) is not None

    def test_default_store_created(self):
        logger = AuditLogger()
        assert logger._store is not None


class TestAuditLoggerQuery:
    def test_query_delegates_to_store(self):
        logger = AuditLogger()
        logger.log(AuditAction.CREATE, "alice", "doc.md")
        logger.log(AuditAction.READ, "alice", "doc.md")
        results = logger.query(actor="alice")
        assert len(results) == 2

    def test_query_empty(self):
        logger = AuditLogger()
        assert logger.query() == []

    def test_query_filter_action(self):
        logger = AuditLogger()
        logger.log(AuditAction.CREATE, "alice", "d")
        logger.log(AuditAction.DELETE, "alice", "d")
        results = logger.query(action=AuditAction.DELETE)
        assert len(results) == 1


class TestAuditLoggerRecent:
    def test_recent_returns_list(self):
        logger = AuditLogger()
        for _ in range(5):
            logger.log(AuditAction.READ, "user", "doc")
        assert len(logger.recent(3)) == 3

    def test_recent_empty(self):
        logger = AuditLogger()
        assert logger.recent() == []


class TestAuditLoggerActorSummary:
    def test_actor_summary_counts(self):
        logger = AuditLogger()
        logger.log(AuditAction.CREATE, "alice", "d")
        logger.log(AuditAction.CREATE, "alice", "d")
        logger.log(AuditAction.READ, "alice", "d")
        summary = logger.actor_summary("alice")
        assert summary.get("CREATE") == 2
        assert summary.get("READ") == 1

    def test_actor_summary_empty_for_unknown_actor(self):
        logger = AuditLogger()
        logger.log(AuditAction.LOGIN, "alice", "system")
        summary = logger.actor_summary("ghost")
        assert summary == {}

    def test_actor_summary_only_for_actor(self):
        logger = AuditLogger()
        logger.log(AuditAction.DELETE, "alice", "d")
        logger.log(AuditAction.DELETE, "bob", "d")
        summary = logger.actor_summary("alice")
        assert "DELETE" in summary
        assert summary["DELETE"] == 1

    def test_actor_summary_multiple_actions(self):
        logger = AuditLogger()
        for action in [AuditAction.LOGIN, AuditAction.READ, AuditAction.LOGOUT]:
            logger.log(action, "carol", "r")
        summary = logger.actor_summary("carol")
        assert set(summary.keys()) == {"LOGIN", "READ", "LOGOUT"}


class TestAuditLoggerExportJsonl:
    def test_export_returns_count(self, tmp_path):
        logger = AuditLogger()
        for _ in range(3):
            logger.log(AuditAction.READ, "user", "doc")
        count = logger.export_jsonl(tmp_path / "out.jsonl")
        assert count == 3

    def test_export_creates_file(self, tmp_path):
        logger = AuditLogger()
        logger.log(AuditAction.CREATE, "alice", "doc")
        out = tmp_path / "audit.jsonl"
        logger.export_jsonl(out)
        assert out.exists()

    def test_export_valid_json_lines(self, tmp_path):
        logger = AuditLogger()
        logger.log(AuditAction.UPDATE, "alice", "readme.md", details={"v": 2})
        out = tmp_path / "audit.jsonl"
        logger.export_jsonl(out)
        lines = out.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 1
        parsed = json.loads(lines[0])
        assert parsed["action"] == "UPDATE"
        assert parsed["actor"] == "alice"
        assert parsed["details"] == {"v": 2}

    def test_export_empty_store(self, tmp_path):
        logger = AuditLogger()
        out = tmp_path / "empty.jsonl"
        count = logger.export_jsonl(out)
        assert count == 0
        assert out.read_text(encoding="utf-8") == ""

    def test_export_multiple_lines(self, tmp_path):
        logger = AuditLogger()
        logger.log(AuditAction.LOGIN, "a", "system")
        logger.log(AuditAction.READ, "b", "doc")
        logger.log(AuditAction.LOGOUT, "a", "system")
        out = tmp_path / "multi.jsonl"
        count = logger.export_jsonl(out)
        assert count == 3
        lines = out.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 3
        for line in lines:
            parsed = json.loads(line)
            assert "event_id" in parsed
            assert "action" in parsed

    def test_export_action_as_string(self, tmp_path):
        logger = AuditLogger()
        logger.log(AuditAction.PERMISSION_CHANGE, "admin", "user/bob")
        out = tmp_path / "perm.jsonl"
        logger.export_jsonl(out)
        line = out.read_text(encoding="utf-8").strip()
        parsed = json.loads(line)
        assert parsed["action"] == "PERMISSION_CHANGE"
        assert isinstance(parsed["action"], str)

    def test_export_accepts_path_object(self, tmp_path):
        logger = AuditLogger()
        logger.log(AuditAction.CONFIG_CHANGE, "sys", "settings")
        out = Path(tmp_path) / "cfg.jsonl"
        count = logger.export_jsonl(out)
        assert count == 1

    def test_export_accepts_string_path(self, tmp_path):
        logger = AuditLogger()
        logger.log(AuditAction.EXPORT, "user", "report")
        out = str(tmp_path / "str.jsonl")
        count = logger.export_jsonl(out)
        assert count == 1
