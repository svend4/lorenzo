"""Tests for docstoolkit.access_log (E114).

Coverage (~85 tests):
  - AccessEvent: fields, defaults, unique ids
  - LogStats: fields, defaults
  - AccessLog.record: creates event, returns AccessEvent, stores it
  - AccessLog.query: no filters, filter by user_id/resource/action/status_code,
      since/until time range, limit/offset pagination, ordering DESC
  - AccessLog.stats: total_events, unique_users, unique_resources, error_count,
      avg_duration_ms, by_action, by_status, with user_id/time filters
  - AccessLog.get: found and not found
  - AccessLog.count: no filter, by user_id, by resource, combined
  - AccessLog.delete_before: removes old events, returns correct count
  - Persistence: file-backed DB survives re-open
  - Virtual time via now_fn
  - metadata stored and retrieved correctly
  - Thread safety: multiple threads writing concurrently
"""
import os
import threading
import time

import pytest

from docstoolkit.access_log import AccessEvent, AccessLog, LogStats


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _log(*args, **kwargs) -> AccessLog:
    """Return a fresh in-memory AccessLog, optionally pre-seeded."""
    return AccessLog(*args, **kwargs)


def _record(log: AccessLog, **kwargs) -> AccessEvent:
    defaults = dict(
        user_id="alice",
        resource="/api/docs",
        action="read",
        status_code=200,
        duration_ms=10.0,
    )
    defaults.update(kwargs)
    return log.record(**defaults)


# ===========================================================================
# AccessEvent dataclass
# ===========================================================================

class TestAccessEventDefaults:
    def test_event_id_generated(self):
        ev = AccessEvent()
        assert ev.event_id
        assert isinstance(ev.event_id, str)

    def test_event_id_length(self):
        ev = AccessEvent()
        assert len(ev.event_id) == 12  # uuid4().hex[:12]

    def test_event_id_unique(self):
        ids = {AccessEvent().event_id for _ in range(20)}
        assert len(ids) == 20

    def test_timestamp_default_zero(self):
        ev = AccessEvent()
        assert ev.timestamp == 0.0

    def test_user_id_default_empty(self):
        assert AccessEvent().user_id == ""

    def test_resource_default_empty(self):
        assert AccessEvent().resource == ""

    def test_action_default_empty(self):
        assert AccessEvent().action == ""

    def test_status_code_default_200(self):
        assert AccessEvent().status_code == 200

    def test_duration_ms_default_zero(self):
        assert AccessEvent().duration_ms == 0.0

    def test_metadata_default_empty_dict(self):
        assert AccessEvent().metadata == {}

    def test_metadata_not_shared(self):
        ev1 = AccessEvent()
        ev2 = AccessEvent()
        ev1.metadata["x"] = 1
        assert "x" not in ev2.metadata


class TestAccessEventFields:
    def test_custom_event_id(self):
        ev = AccessEvent(event_id="myid")
        assert ev.event_id == "myid"

    def test_fields_stored(self):
        ev = AccessEvent(
            event_id="abc",
            timestamp=1_000.0,
            user_id="bob",
            resource="/docs/page",
            action="write",
            status_code=201,
            duration_ms=42.5,
            metadata={"ip": "1.2.3.4"},
        )
        assert ev.event_id == "abc"
        assert ev.timestamp == 1_000.0
        assert ev.user_id == "bob"
        assert ev.resource == "/docs/page"
        assert ev.action == "write"
        assert ev.status_code == 201
        assert ev.duration_ms == 42.5
        assert ev.metadata == {"ip": "1.2.3.4"}


# ===========================================================================
# LogStats dataclass
# ===========================================================================

class TestLogStatsDefaults:
    def test_total_events_zero(self):
        assert LogStats().total_events == 0

    def test_unique_users_zero(self):
        assert LogStats().unique_users == 0

    def test_unique_resources_zero(self):
        assert LogStats().unique_resources == 0

    def test_error_count_zero(self):
        assert LogStats().error_count == 0

    def test_avg_duration_ms_zero(self):
        assert LogStats().avg_duration_ms == 0.0

    def test_by_action_empty_dict(self):
        assert LogStats().by_action == {}

    def test_by_status_empty_dict(self):
        assert LogStats().by_status == {}


# ===========================================================================
# AccessLog.record
# ===========================================================================

class TestAccessLogRecord:
    def test_record_returns_access_event(self):
        log = _log()
        ev = _record(log)
        assert isinstance(ev, AccessEvent)

    def test_record_event_id_is_set(self):
        log = _log()
        ev = _record(log)
        assert ev.event_id

    def test_record_stores_user_id(self):
        log = _log()
        ev = _record(log, user_id="carol")
        assert ev.user_id == "carol"

    def test_record_stores_resource(self):
        log = _log()
        ev = _record(log, resource="/items/42")
        assert ev.resource == "/items/42"

    def test_record_stores_action(self):
        log = _log()
        ev = _record(log, action="delete")
        assert ev.action == "delete"

    def test_record_stores_status_code(self):
        log = _log()
        ev = _record(log, status_code=404)
        assert ev.status_code == 404

    def test_record_stores_duration_ms(self):
        log = _log()
        ev = _record(log, duration_ms=99.9)
        assert ev.duration_ms == 99.9

    def test_record_stores_metadata(self):
        log = _log()
        ev = _record(log, metadata={"region": "eu"})
        assert ev.metadata == {"region": "eu"}

    def test_record_timestamp_set_by_now_fn(self):
        log = _log(now_fn=lambda: 5000.0)
        ev = _record(log)
        assert ev.timestamp == 5000.0

    def test_record_increases_count(self):
        log = _log()
        _record(log)
        assert log.count() == 1

    def test_record_multiple_increases_count(self):
        log = _log()
        for _ in range(5):
            _record(log)
        assert log.count() == 5

    def test_record_metadata_none_defaults_to_empty(self):
        log = _log()
        ev = log.record("u", "/r", "read", metadata=None)
        assert ev.metadata == {}

    def test_record_persisted_retrievable_by_get(self):
        log = _log()
        ev = _record(log)
        fetched = log.get(ev.event_id)
        assert fetched is not None
        assert fetched.event_id == ev.event_id


# ===========================================================================
# AccessLog.query
# ===========================================================================

class TestAccessLogQueryNoFilters:
    def test_query_empty_log_returns_empty(self):
        log = _log()
        assert log.query() == []

    def test_query_returns_all_events(self):
        log = _log()
        for _ in range(4):
            _record(log)
        assert len(log.query()) == 4

    def test_query_returns_list(self):
        log = _log()
        _record(log)
        result = log.query()
        assert isinstance(result, list)
        assert isinstance(result[0], AccessEvent)


class TestAccessLogQueryFilters:
    def setup_method(self):
        t = 1_000_000.0
        tick = iter(range(100))
        self.log = AccessLog(now_fn=lambda: t + next(tick) * 10)
        # e1: alice, /api/docs, read, 200, 10ms
        self.e1 = self.log.record("alice", "/api/docs", "read", 200, 10.0)
        # e2: alice, /api/docs, write, 201, 20ms
        self.e2 = self.log.record("alice", "/api/docs", "write", 201, 20.0)
        # e3: bob, /api/items, read, 200, 30ms
        self.e3 = self.log.record("bob", "/api/items", "read", 200, 30.0)
        # e4: bob, /api/admin, delete, 403, 5ms
        self.e4 = self.log.record("bob", "/api/admin", "delete", 403, 5.0)
        # e5: carol, /api/docs, read, 500, 50ms
        self.e5 = self.log.record("carol", "/api/docs", "read", 500, 50.0)

    def test_query_by_user_id(self):
        results = self.log.query(user_id="alice")
        assert len(results) == 2
        assert all(r.user_id == "alice" for r in results)

    def test_query_by_user_id_no_match(self):
        assert self.log.query(user_id="nobody") == []

    def test_query_by_resource(self):
        results = self.log.query(resource="/api/docs")
        assert len(results) == 3
        assert all(r.resource == "/api/docs" for r in results)

    def test_query_by_resource_no_match(self):
        assert self.log.query(resource="/nonexistent") == []

    def test_query_by_action(self):
        results = self.log.query(action="read")
        assert len(results) == 3
        assert all(r.action == "read" for r in results)

    def test_query_by_action_delete(self):
        results = self.log.query(action="delete")
        assert len(results) == 1
        assert results[0].event_id == self.e4.event_id

    def test_query_by_action_no_match(self):
        assert self.log.query(action="patch") == []

    def test_query_by_status_code(self):
        results = self.log.query(status_code=200)
        assert len(results) == 2

    def test_query_by_status_code_403(self):
        results = self.log.query(status_code=403)
        assert len(results) == 1
        assert results[0].event_id == self.e4.event_id

    def test_query_by_status_code_no_match(self):
        assert self.log.query(status_code=418) == []

    def test_query_since(self):
        # e1 at t+0, e2 at t+10, ... e5 at t+40
        # since t+35 → only e5
        t = 1_000_000.0
        results = self.log.query(since=t + 35)
        assert len(results) == 1
        assert results[0].event_id == self.e5.event_id

    def test_query_until(self):
        # until t+5 → only e1
        t = 1_000_000.0
        results = self.log.query(until=t + 5)
        assert len(results) == 1
        assert results[0].event_id == self.e1.event_id

    def test_query_since_until_range(self):
        t = 1_000_000.0
        results = self.log.query(since=t + 5, until=t + 25)
        assert len(results) == 2

    def test_query_combined_user_and_action(self):
        results = self.log.query(user_id="alice", action="write")
        assert len(results) == 1
        assert results[0].event_id == self.e2.event_id

    def test_query_combined_user_and_resource(self):
        results = self.log.query(user_id="bob", resource="/api/items")
        assert len(results) == 1
        assert results[0].event_id == self.e3.event_id

    def test_query_combined_action_and_status(self):
        results = self.log.query(action="read", status_code=500)
        assert len(results) == 1
        assert results[0].event_id == self.e5.event_id


class TestAccessLogQueryPagination:
    def setup_method(self):
        tick = iter(range(100))
        self.log = AccessLog(now_fn=lambda: float(next(tick)))
        for i in range(10):
            self.log.record(f"user{i}", "/r", "read")

    def test_query_limit(self):
        assert len(self.log.query(limit=3)) == 3

    def test_query_limit_one(self):
        assert len(self.log.query(limit=1)) == 1

    def test_query_limit_larger_than_total(self):
        assert len(self.log.query(limit=100)) == 10

    def test_query_offset(self):
        all_events = self.log.query(limit=100)
        paged = self.log.query(limit=100, offset=5)
        assert len(paged) == 5
        assert paged[0].event_id == all_events[5].event_id

    def test_query_offset_zero_same_as_no_offset(self):
        assert self.log.query(offset=0) == self.log.query()

    def test_query_offset_beyond_total_returns_empty(self):
        assert self.log.query(offset=100) == []

    def test_query_pagination_covers_all(self):
        page1 = self.log.query(limit=5, offset=0)
        page2 = self.log.query(limit=5, offset=5)
        all_ids = {e.event_id for e in page1 + page2}
        assert len(all_ids) == 10


class TestAccessLogQueryOrdering:
    def test_query_ordered_timestamp_desc(self):
        tick = iter(range(100))
        log = AccessLog(now_fn=lambda: float(next(tick)))
        for _ in range(5):
            _record(log)
        results = log.query()
        timestamps = [r.timestamp for r in results]
        assert timestamps == sorted(timestamps, reverse=True)


# ===========================================================================
# AccessLog.stats
# ===========================================================================

class TestAccessLogStats:
    def setup_method(self):
        tick = iter(range(100))
        self.log = AccessLog(now_fn=lambda: float(next(tick)))
        self.log.record("alice", "/a", "read",   200, 10.0)
        self.log.record("alice", "/b", "write",  201, 20.0)
        self.log.record("bob",   "/a", "read",   200, 30.0)
        self.log.record("bob",   "/c", "delete", 404, 5.0)
        self.log.record("carol", "/a", "read",   500, 50.0)

    def test_stats_total_events(self):
        s = self.log.stats()
        assert s.total_events == 5

    def test_stats_unique_users(self):
        s = self.log.stats()
        assert s.unique_users == 3

    def test_stats_unique_resources(self):
        s = self.log.stats()
        assert s.unique_resources == 3  # /a, /b, /c

    def test_stats_error_count(self):
        # 404 and 500 are errors (>= 400)
        s = self.log.stats()
        assert s.error_count == 2

    def test_stats_avg_duration_ms(self):
        s = self.log.stats()
        expected = (10.0 + 20.0 + 30.0 + 5.0 + 50.0) / 5
        assert abs(s.avg_duration_ms - expected) < 1e-6

    def test_stats_by_action(self):
        s = self.log.stats()
        assert s.by_action.get("read") == 3
        assert s.by_action.get("write") == 1
        assert s.by_action.get("delete") == 1

    def test_stats_by_status(self):
        s = self.log.stats()
        assert s.by_status.get(200) == 2
        assert s.by_status.get(201) == 1
        assert s.by_status.get(404) == 1
        assert s.by_status.get(500) == 1

    def test_stats_filtered_by_user_id(self):
        s = self.log.stats(user_id="alice")
        assert s.total_events == 2
        assert s.unique_users == 1
        assert s.error_count == 0

    def test_stats_user_id_no_errors(self):
        s = self.log.stats(user_id="alice")
        assert s.error_count == 0

    def test_stats_user_id_error_user(self):
        s = self.log.stats(user_id="bob")
        assert s.error_count == 1

    def test_stats_with_since(self):
        # timestamps are 0,1,2,3,4; since=3 → 2 events
        s = self.log.stats(since=3.0)
        assert s.total_events == 2

    def test_stats_with_until(self):
        # until=1 → 2 events (ts=0, ts=1)
        s = self.log.stats(until=1.0)
        assert s.total_events == 2

    def test_stats_with_since_and_until(self):
        s = self.log.stats(since=1.0, until=2.0)
        assert s.total_events == 2

    def test_stats_empty_log(self):
        s = AccessLog().stats()
        assert s.total_events == 0
        assert s.unique_users == 0
        assert s.unique_resources == 0
        assert s.error_count == 0
        assert s.avg_duration_ms == 0.0
        assert s.by_action == {}
        assert s.by_status == {}

    def test_stats_returns_log_stats_instance(self):
        assert isinstance(self.log.stats(), LogStats)


# ===========================================================================
# AccessLog.get
# ===========================================================================

class TestAccessLogGet:
    def test_get_existing_event(self):
        log = _log()
        ev = _record(log)
        fetched = log.get(ev.event_id)
        assert fetched is not None
        assert fetched.event_id == ev.event_id

    def test_get_preserves_all_fields(self):
        log = AccessLog(now_fn=lambda: 9999.0)
        ev = log.record("u1", "/res", "write", 201, 77.7, {"k": "v"})
        f = log.get(ev.event_id)
        assert f.user_id == "u1"
        assert f.resource == "/res"
        assert f.action == "write"
        assert f.status_code == 201
        assert f.duration_ms == 77.7
        assert f.metadata == {"k": "v"}
        assert f.timestamp == 9999.0

    def test_get_missing_returns_none(self):
        log = _log()
        assert log.get("nonexistent-id") is None

    def test_get_after_multiple_records(self):
        log = _log()
        evs = [_record(log, user_id=f"u{i}") for i in range(5)]
        for ev in evs:
            assert log.get(ev.event_id).user_id == ev.user_id

    def test_get_returns_access_event_instance(self):
        log = _log()
        ev = _record(log)
        assert isinstance(log.get(ev.event_id), AccessEvent)


# ===========================================================================
# AccessLog.count
# ===========================================================================

class TestAccessLogCount:
    def setup_method(self):
        self.log = _log()
        self.log.record("alice", "/a", "read")
        self.log.record("alice", "/b", "read")
        self.log.record("bob",   "/a", "write")
        self.log.record("bob",   "/c", "read")

    def test_count_all(self):
        assert self.log.count() == 4

    def test_count_by_user_id(self):
        assert self.log.count(user_id="alice") == 2

    def test_count_by_user_id_single(self):
        assert self.log.count(user_id="bob") == 2

    def test_count_by_resource(self):
        assert self.log.count(resource="/a") == 2

    def test_count_by_resource_single(self):
        assert self.log.count(resource="/b") == 1

    def test_count_combined_user_and_resource(self):
        assert self.log.count(user_id="alice", resource="/a") == 1

    def test_count_combined_no_match(self):
        assert self.log.count(user_id="alice", resource="/c") == 0

    def test_count_no_match(self):
        assert self.log.count(user_id="ghost") == 0

    def test_count_empty_log(self):
        assert _log().count() == 0


# ===========================================================================
# AccessLog.delete_before
# ===========================================================================

class TestAccessLogDeleteBefore:
    def test_delete_before_removes_old_events(self):
        tick = iter(range(100))
        log = AccessLog(now_fn=lambda: float(next(tick)))
        for _ in range(5):
            _record(log)
        # timestamps 0..4; delete < 3 → removes 0,1,2
        deleted = log.delete_before(3.0)
        assert deleted == 3
        assert log.count() == 2

    def test_delete_before_returns_count_deleted(self):
        tick = iter(range(100))
        log = AccessLog(now_fn=lambda: float(next(tick)))
        for _ in range(4):
            _record(log)
        assert log.delete_before(2.0) == 2

    def test_delete_before_removes_nothing_when_all_newer(self):
        tick = iter(range(100))
        log = AccessLog(now_fn=lambda: float(next(tick)) + 100)
        for _ in range(3):
            _record(log)
        assert log.delete_before(50.0) == 0
        assert log.count() == 3

    def test_delete_before_removes_all(self):
        tick = iter(range(100))
        log = AccessLog(now_fn=lambda: float(next(tick)))
        for _ in range(3):
            _record(log)
        deleted = log.delete_before(1000.0)
        assert deleted == 3
        assert log.count() == 0

    def test_delete_before_remaining_events_are_accessible(self):
        tick = iter(range(100))
        log = AccessLog(now_fn=lambda: float(next(tick)))
        for i in range(6):
            log.record(f"u{i}", "/r", "read")
        log.delete_before(3.0)  # removes ts 0,1,2
        remaining = log.query(limit=100)
        assert all(r.timestamp >= 3.0 for r in remaining)


# ===========================================================================
# Persistence (file DB)
# ===========================================================================

class TestAccessLogPersistence:
    def test_persists_across_reopen(self, tmp_path):
        db = str(tmp_path / "log.db")
        log1 = AccessLog(db_path=db)
        ev = log1.record("alice", "/page", "read", 200, 5.0, {"tag": "test"})
        log1.close()

        log2 = AccessLog(db_path=db)
        fetched = log2.get(ev.event_id)
        assert fetched is not None
        assert fetched.user_id == "alice"
        assert fetched.resource == "/page"
        assert fetched.metadata == {"tag": "test"}
        log2.close()

    def test_count_persists_across_reopen(self, tmp_path):
        db = str(tmp_path / "log.db")
        log1 = AccessLog(db_path=db)
        for _ in range(7):
            _record(log1)
        log1.close()

        log2 = AccessLog(db_path=db)
        assert log2.count() == 7
        log2.close()

    def test_query_persists_across_reopen(self, tmp_path):
        db = str(tmp_path / "log.db")
        log1 = AccessLog(db_path=db)
        log1.record("bob", "/x", "write", 201)
        log1.close()

        log2 = AccessLog(db_path=db)
        results = log2.query(user_id="bob")
        assert len(results) == 1
        assert results[0].resource == "/x"
        log2.close()


# ===========================================================================
# Virtual time via now_fn
# ===========================================================================

class TestAccessLogVirtualTime:
    def test_now_fn_used_for_timestamp(self):
        log = AccessLog(now_fn=lambda: 42.0)
        ev = _record(log)
        assert ev.timestamp == 42.0

    def test_now_fn_called_at_record_time(self):
        calls = []
        def now():
            t = float(len(calls))
            calls.append(t)
            return t

        log = AccessLog(now_fn=now)
        ev1 = _record(log)
        ev2 = _record(log)
        assert ev1.timestamp == 0.0
        assert ev2.timestamp == 1.0

    def test_now_fn_enables_time_range_filtering(self):
        tick = iter(range(100))
        log = AccessLog(now_fn=lambda: float(next(tick)) * 100)
        for _ in range(5):
            _record(log)
        # timestamps: 0, 100, 200, 300, 400
        results = log.query(since=150.0, until=350.0)
        assert len(results) == 2
        assert all(150.0 <= r.timestamp <= 350.0 for r in results)


# ===========================================================================
# Metadata stored/retrieved
# ===========================================================================

class TestAccessLogMetadata:
    def test_metadata_round_trip(self):
        log = _log()
        meta = {"user_agent": "Mozilla/5.0", "ip": "10.0.0.1", "count": 3}
        ev = log.record("alice", "/r", "read", metadata=meta)
        fetched = log.get(ev.event_id)
        assert fetched.metadata == meta

    def test_metadata_nested(self):
        log = _log()
        meta = {"headers": {"x-request-id": "abc123"}, "tags": ["a", "b"]}
        ev = log.record("alice", "/r", "read", metadata=meta)
        assert log.get(ev.event_id).metadata == meta

    def test_metadata_empty_dict(self):
        log = _log()
        ev = log.record("alice", "/r", "read", metadata={})
        assert log.get(ev.event_id).metadata == {}

    def test_metadata_none_becomes_empty_dict(self):
        log = _log()
        ev = log.record("alice", "/r", "read", metadata=None)
        assert log.get(ev.event_id).metadata == {}

    def test_metadata_in_query_results(self):
        log = _log()
        log.record("alice", "/r", "read", metadata={"k": "v"})
        results = log.query(user_id="alice")
        assert results[0].metadata == {"k": "v"}


# ===========================================================================
# close
# ===========================================================================

class TestAccessLogClose:
    def test_close_no_error(self):
        log = _log()
        _record(log)
        log.close()  # should not raise

    def test_close_in_memory(self):
        log = AccessLog()
        log.close()  # should not raise


# ===========================================================================
# Thread safety
# ===========================================================================

class TestAccessLogThreadSafety:
    def test_concurrent_writes(self):
        log = _log()
        errors = []

        def writer(n):
            try:
                for _ in range(n):
                    log.record("user", "/r", "read")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=writer, args=(10,)) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert log.count() == 50
