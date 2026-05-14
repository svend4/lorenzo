"""Tests for E277 DocAuditV3."""
import json
import threading
import time
from docstoolkit.doc_audit_v3 import AuditEntry, AuditStats, BatchStats, DocAuditV3


T0 = 1_700_000_000.0


def _audit() -> DocAuditV3:
    return DocAuditV3()


# ---------------------------------------------------------------------------
# Basic record
# ---------------------------------------------------------------------------


def test_record_returns_audit_entry():
    a = _audit()
    e = a.record("alice", "read", "doc:1", now=T0)
    assert isinstance(e, AuditEntry)


def test_record_assigns_entry_id_starting_at_1():
    a = _audit()
    e = a.record("alice", "read", "doc:1", now=T0)
    assert e.entry_id == 1


def test_record_second_entry_id_is_2():
    a = _audit()
    a.record("alice", "read", "doc:1", now=T0)
    e2 = a.record("bob", "write", "doc:2", now=T0 + 1)
    assert e2.entry_id == 2


def test_record_actor_action_resource():
    a = _audit()
    e = a.record("alice", "delete", "doc:99", now=T0)
    assert e.actor == "alice"
    assert e.action == "delete"
    assert e.resource == "doc:99"


def test_record_timestamp_stored():
    a = _audit()
    e = a.record("alice", "read", "doc:1", now=T0)
    assert e.timestamp == T0


def test_record_details_stored():
    a = _audit()
    e = a.record("alice", "read", "doc:1", details={"ip": "1.2.3.4"}, now=T0)
    assert e.details == {"ip": "1.2.3.4"}


def test_record_details_defaults_empty():
    a = _audit()
    e = a.record("alice", "read", "doc:1", now=T0)
    assert e.details == {}


def test_record_partition_assigned():
    a = _audit()
    e = a.record("alice", "read", "doc:1", now=T0)
    assert isinstance(e.partition, str)
    assert len(e.partition) > 0


# ---------------------------------------------------------------------------
# Default partition: YYYY-MM
# ---------------------------------------------------------------------------


def test_default_partition_format():
    a = _audit()
    part = a.partition_for(T0)
    assert len(part) == 7
    assert part[4] == "-"


def test_default_partition_year_month():
    a = _audit()
    part = a.partition_for(T0)
    from datetime import datetime
    expected = datetime.fromtimestamp(T0).strftime("%Y-%m")
    assert part == expected


# ---------------------------------------------------------------------------
# Custom partition function
# ---------------------------------------------------------------------------


def test_custom_partition_function():
    a = DocAuditV3(partition_func=lambda _ts: "fixed-part")
    e = a.record("u", "a", "r", now=T0)
    assert e.partition == "fixed-part"


def test_custom_partition_used_in_batch():
    called = []
    def pf(ts):
        called.append(ts)
        return "p"
    a = DocAuditV3(partition_func=pf)
    a.batch_record([{"actor": "u", "action": "a", "resource": "r", "now": T0}])
    assert "p" in [e.partition for e in a.entries_in_partition("p")]


# ---------------------------------------------------------------------------
# get_entry
# ---------------------------------------------------------------------------


def test_get_entry_returns_entry():
    a = _audit()
    e = a.record("alice", "read", "doc:1", now=T0)
    got = a.get_entry(e.entry_id)
    assert got is e


def test_get_entry_missing_returns_none():
    a = _audit()
    assert a.get_entry(999) is None


# ---------------------------------------------------------------------------
# entries_in_partition
# ---------------------------------------------------------------------------


def test_entries_in_partition_returns_list():
    a = _audit()
    e = a.record("alice", "read", "doc:1", now=T0)
    part = e.partition
    entries = a.entries_in_partition(part)
    assert e in entries


def test_entries_in_partition_unknown_returns_empty():
    a = _audit()
    assert a.entries_in_partition("no-such") == []


def test_entries_in_partition_all_belong():
    a = DocAuditV3(partition_func=lambda _: "p1")
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 1)
    entries = a.entries_in_partition("p1")
    assert len(entries) == 2


# ---------------------------------------------------------------------------
# entries_for_actor
# ---------------------------------------------------------------------------


def test_entries_for_actor_filters():
    a = DocAuditV3(partition_func=lambda _: "p")
    a.record("alice", "read", "r", now=T0)
    a.record("bob", "write", "r", now=T0 + 1)
    a.record("alice", "delete", "r", now=T0 + 2)
    result = a.entries_for_actor("alice")
    assert len(result) == 2
    assert all(e.actor == "alice" for e in result)


def test_entries_for_actor_with_partition():
    a = DocAuditV3(partition_func=lambda _: "p1")
    a.record("alice", "r", "x", now=T0)
    result = a.entries_for_actor("alice", partition="p1")
    assert len(result) == 1


def test_entries_for_actor_limit():
    a = _audit()
    for _ in range(5):
        a.record("alice", "r", "x", now=T0)
    result = a.entries_for_actor("alice", limit=2)
    assert len(result) == 2


def test_entries_for_actor_no_match():
    a = _audit()
    a.record("bob", "r", "x", now=T0)
    assert a.entries_for_actor("alice") == []


# ---------------------------------------------------------------------------
# entries_for_resource
# ---------------------------------------------------------------------------


def test_entries_for_resource_filters():
    a = DocAuditV3(partition_func=lambda _: "p")
    a.record("alice", "read", "doc:1", now=T0)
    a.record("bob", "write", "doc:2", now=T0 + 1)
    a.record("alice", "delete", "doc:1", now=T0 + 2)
    result = a.entries_for_resource("doc:1")
    assert len(result) == 2
    assert all(e.resource == "doc:1" for e in result)


def test_entries_for_resource_limit():
    a = _audit()
    for _ in range(5):
        a.record("u", "r", "doc:1", now=T0)
    result = a.entries_for_resource("doc:1", limit=3)
    assert len(result) == 3


# ---------------------------------------------------------------------------
# partitions
# ---------------------------------------------------------------------------


def test_partitions_returns_sorted_list():
    def pf(ts):
        return "b" if ts >= T0 + 60 else "a"
    a = DocAuditV3(partition_func=pf)
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 60)
    parts = a.partitions()
    assert parts == ["a", "b"]


def test_partitions_empty_initially():
    assert _audit().partitions() == []


# ---------------------------------------------------------------------------
# count_entries
# ---------------------------------------------------------------------------


def test_count_entries_total():
    a = _audit()
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 1)
    assert a.count_entries() == 2


def test_count_entries_by_partition():
    a = DocAuditV3(partition_func=lambda _: "p1")
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 1)
    assert a.count_entries("p1") == 2


def test_count_entries_missing_partition():
    a = _audit()
    assert a.count_entries("no-such") == 0


# ---------------------------------------------------------------------------
# recent
# ---------------------------------------------------------------------------


def test_recent_returns_latest_entries():
    a = _audit()
    for i in range(5):
        a.record("u", "a", f"r:{i}", now=T0 + i)
    result = a.recent(3)
    assert len(result) == 3


def test_recent_order_is_newest_first():
    a = DocAuditV3(partition_func=lambda _: "p")
    e1 = a.record("u", "a", "r", now=T0)
    e2 = a.record("u", "b", "r", now=T0 + 1)
    result = a.recent(2)
    assert result[0].entry_id == e2.entry_id
    assert result[1].entry_id == e1.entry_id


def test_recent_partition_filter():
    def pf(ts):
        return "p1" if ts < T0 + 50 else "p2"
    a = DocAuditV3(partition_func=pf)
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 100)
    result = a.recent(10, partition="p1")
    assert all(e.partition == "p1" for e in result)


# ---------------------------------------------------------------------------
# drop_partition
# ---------------------------------------------------------------------------


def test_drop_partition_removes_entries():
    a = DocAuditV3(partition_func=lambda _: "p1")
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 1)
    dropped = a.drop_partition("p1")
    assert dropped == 2
    assert a.count_entries() == 0


def test_drop_partition_missing_returns_zero():
    a = _audit()
    assert a.drop_partition("no-such") == 0


def test_drop_partition_does_not_affect_others():
    def pf(ts):
        return "p1" if ts < T0 + 50 else "p2"
    a = DocAuditV3(partition_func=pf)
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 100)
    a.drop_partition("p1")
    assert a.count_entries() == 1


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


def test_clear_removes_all():
    a = _audit()
    a.record("u", "a", "r", now=T0)
    a.clear()
    assert a.count_entries() == 0


def test_clear_resets_id_counter():
    a = _audit()
    a.record("u", "a", "r", now=T0)
    a.clear()
    e = a.record("u", "b", "r", now=T0 + 1)
    assert e.entry_id == 1


# ---------------------------------------------------------------------------
# batch_record
# ---------------------------------------------------------------------------


def test_batch_record_returns_batch_stats():
    a = _audit()
    stats = a.batch_record([
        {"actor": "u", "action": "a", "resource": "r", "now": T0},
    ])
    assert isinstance(stats, BatchStats)


def test_batch_record_entries_written_count():
    a = _audit()
    stats = a.batch_record([
        {"actor": "u1", "action": "a", "resource": "r", "now": T0},
        {"actor": "u2", "action": "b", "resource": "r", "now": T0 + 1},
    ])
    assert stats.entries_written == 2


def test_batch_record_partitions_touched():
    def pf(ts):
        return "pa" if ts < T0 + 50 else "pb"
    a = DocAuditV3(partition_func=pf)
    stats = a.batch_record([
        {"actor": "u", "action": "a", "resource": "r", "now": T0},
        {"actor": "u", "action": "b", "resource": "r", "now": T0 + 100},
    ])
    assert "pa" in stats.partitions_touched
    assert "pb" in stats.partitions_touched


def test_batch_record_empty():
    a = _audit()
    stats = a.batch_record([])
    assert stats.entries_written == 0


def test_batch_record_duration_ms_positive():
    a = _audit()
    stats = a.batch_record([{"actor": "u", "action": "a", "resource": "r", "now": T0}])
    assert stats.duration_ms >= 0.0


# ---------------------------------------------------------------------------
# snapshot / restore
# ---------------------------------------------------------------------------


def test_snapshot_returns_bytes():
    a = _audit()
    a.record("u", "a", "r", now=T0)
    snap = a.snapshot()
    assert isinstance(snap, bytes)


def test_restore_reloads_entries():
    a = _audit()
    a.record("alice", "read", "doc:1", now=T0)
    snap = a.snapshot()
    b = _audit()
    count = b.restore(snap)
    assert count == 1
    assert b.count_entries() == 1


def test_restore_preserves_entry_fields():
    a = _audit()
    e = a.record("alice", "read", "doc:1", details={"k": "v"}, now=T0)
    snap = a.snapshot()
    b = _audit()
    b.restore(snap)
    restored = b.get_entry(e.entry_id)
    assert restored is not None
    assert restored.actor == "alice"
    assert restored.details == {"k": "v"}


def test_restore_continues_id_sequence():
    a = _audit()
    a.record("u", "a", "r", now=T0)
    snap = a.snapshot()
    b = _audit()
    b.restore(snap)
    e2 = b.record("u", "b", "r", now=T0 + 1)
    assert e2.entry_id == 2


def test_roundtrip_multiple_partitions():
    def pf(ts):
        return "pa" if ts < T0 + 50 else "pb"
    a = DocAuditV3(partition_func=pf)
    a.record("u1", "a", "r", now=T0)
    a.record("u2", "b", "r", now=T0 + 100)
    snap = a.snapshot()
    b = DocAuditV3(partition_func=pf)
    b.restore(snap)
    assert set(b.partitions()) == {"pa", "pb"}


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_returns_audit_stats():
    a = _audit()
    s = a.stats()
    assert isinstance(s, AuditStats)


def test_stats_total_entries():
    a = _audit()
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 1)
    assert a.stats().total_entries == 2


def test_stats_total_partitions():
    def pf(ts):
        return "pa" if ts < T0 + 50 else "pb"
    a = DocAuditV3(partition_func=pf)
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 100)
    assert a.stats().total_partitions == 2


def test_stats_entries_per_partition():
    a = DocAuditV3(partition_func=lambda _: "only")
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 1)
    assert a.stats().entries_per_partition == {"only": 2}


def test_stats_oldest_newest():
    a = _audit()
    a.record("u", "a", "r", now=T0)
    a.record("u", "b", "r", now=T0 + 60)
    s = a.stats()
    assert s.oldest_at == T0
    assert s.newest_at == T0 + 60


def test_stats_empty_log():
    a = _audit()
    s = a.stats()
    assert s.total_entries == 0
    assert s.oldest_at is None
    assert s.newest_at is None


# ---------------------------------------------------------------------------
# total_entries / total_partitions properties
# ---------------------------------------------------------------------------


def test_total_entries_property():
    a = _audit()
    a.record("u", "a", "r", now=T0)
    assert a.total_entries == 1


def test_total_partitions_property():
    a = DocAuditV3(partition_func=lambda _: "p")
    a.record("u", "a", "r", now=T0)
    assert a.total_partitions == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_concurrent_record():
    a = _audit()
    errors = []
    def worker():
        try:
            for i in range(20):
                a.record("u", "a", f"r:{i}", now=T0 + i)
        except Exception as exc:
            errors.append(exc)
    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    assert a.total_entries == 100
