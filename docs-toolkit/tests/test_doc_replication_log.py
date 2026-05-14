"""Tests for E344 DocReplicationLog."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_replication_log import (
    DocReplicationLog,
    ReplicaStatus,
    ReplicationEntry,
    ReplicationStats,
)


class TestReplicationEntryDataclass:
    def test_create_minimal(self):
        e = ReplicationEntry(lsn=1, doc_id="d", operation="insert", source_replica="r1")
        assert e.lsn == 1
        assert e.doc_id == "d"
        assert e.operation == "insert"
        assert e.source_replica == "r1"

    def test_default_created_at(self):
        e = ReplicationEntry(lsn=1, doc_id="d", operation="x", source_replica="r")
        assert e.created_at == 0.0

    def test_default_payload(self):
        e = ReplicationEntry(lsn=1, doc_id="d", operation="x", source_replica="r")
        assert e.payload == {}

    def test_payload_independent_per_instance(self):
        a = ReplicationEntry(lsn=1, doc_id="a", operation="x", source_replica="r")
        b = ReplicationEntry(lsn=2, doc_id="b", operation="x", source_replica="r")
        a.payload["k"] = "v"
        assert b.payload == {}

    def test_custom_values(self):
        e = ReplicationEntry(
            lsn=7,
            doc_id="d",
            operation="update",
            source_replica="r1",
            created_at=123.4,
            payload={"k": 1},
        )
        assert e.created_at == 123.4
        assert e.payload == {"k": 1}


class TestReplicaStatusDataclass:
    def test_defaults(self):
        s = ReplicaStatus(replica_id="r")
        assert s.last_applied_lsn == 0
        assert s.last_sync_at == 0.0
        assert s.lag == 0

    def test_custom_values(self):
        s = ReplicaStatus(
            replica_id="r", last_applied_lsn=5, last_sync_at=12.0, lag=3
        )
        assert s.last_applied_lsn == 5
        assert s.last_sync_at == 12.0
        assert s.lag == 3


class TestReplicationStatsDataclass:
    def test_create(self):
        s = ReplicationStats(
            total_entries=10, total_replicas=3, max_lag=5, avg_lag=2.5
        )
        assert s.total_entries == 10
        assert s.total_replicas == 3
        assert s.max_lag == 5
        assert s.avg_lag == 2.5


class TestConstruction:
    def test_empty_log(self):
        log = DocReplicationLog()
        assert log.stats().total_entries == 0
        assert log.stats().total_replicas == 0

    def test_two_logs_independent(self):
        a = DocReplicationLog()
        b = DocReplicationLog()
        a.append("d", "insert", "r1")
        assert b.stats().total_entries == 0


class TestAppend:
    def test_first_lsn_is_one(self):
        log = DocReplicationLog()
        e = log.append("d", "insert", "r1")
        assert e.lsn == 1

    def test_lsn_increments(self):
        log = DocReplicationLog()
        e1 = log.append("d", "insert", "r1")
        e2 = log.append("d", "update", "r1")
        e3 = log.append("d", "delete", "r1")
        assert (e1.lsn, e2.lsn, e3.lsn) == (1, 2, 3)

    def test_timestamp_assigned(self):
        log = DocReplicationLog()
        e = log.append("d", "insert", "r1", now=100.0)
        assert e.created_at == 100.0

    def test_default_timestamp_uses_time(self):
        log = DocReplicationLog()
        e = log.append("d", "insert", "r1")
        assert e.created_at > 0

    def test_payload_stored(self):
        log = DocReplicationLog()
        e = log.append("d", "insert", "r1", payload={"k": "v"})
        assert e.payload == {"k": "v"}

    def test_payload_default_empty(self):
        log = DocReplicationLog()
        e = log.append("d", "insert", "r1")
        assert e.payload == {}

    def test_payload_is_copy(self):
        log = DocReplicationLog()
        src = {"k": "v"}
        e = log.append("d", "insert", "r1", payload=src)
        src["k"] = "changed"
        assert e.payload == {"k": "v"}

    def test_entry_appears_in_get(self):
        log = DocReplicationLog()
        e = log.append("d1", "insert", "r1")
        assert log.get_entry(e.lsn) is e


class TestRegisterReplica:
    def test_initial_lsn_zero(self):
        log = DocReplicationLog()
        s = log.register_replica("r1")
        assert s.last_applied_lsn == 0

    def test_replica_appears(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        assert log.replica_status("r1") is not None

    def test_register_uses_now(self):
        log = DocReplicationLog()
        s = log.register_replica("r1", now=42.0)
        assert s.last_sync_at == 42.0

    def test_register_default_now(self):
        log = DocReplicationLog()
        s = log.register_replica("r1")
        assert s.last_sync_at > 0


class TestUnregisterReplica:
    def test_unregister_existing(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        assert log.unregister_replica("r1") is True

    def test_unregister_missing(self):
        log = DocReplicationLog()
        assert log.unregister_replica("ghost") is False

    def test_status_gone_after_unregister(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.unregister_replica("r1")
        assert log.replica_status("r1") is None


class TestPendingFor:
    def test_empty_for_unknown_replica(self):
        log = DocReplicationLog()
        log.append("d", "insert", "r1")
        assert log.pending_for("ghost") == []

    def test_returns_all_when_lsn_zero(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        log.append("d", "update", "r2")
        pending = log.pending_for("r1")
        assert [e.lsn for e in pending] == [1, 2]

    def test_returns_only_after_applied(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        log.append("d", "update", "r2")
        log.apply("r1", 1)
        pending = log.pending_for("r1")
        assert [e.lsn for e in pending] == [2]

    def test_sorted_by_lsn_asc(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        for i in range(5):
            log.append(f"d{i}", "insert", "r2")
        pending = log.pending_for("r1")
        lsns = [e.lsn for e in pending]
        assert lsns == sorted(lsns)

    def test_limit_applied(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        for _ in range(5):
            log.append("d", "insert", "r2")
        pending = log.pending_for("r1", limit=2)
        assert len(pending) == 2

    def test_limit_larger_than_pending(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        pending = log.pending_for("r1", limit=10)
        assert len(pending) == 1


class TestApply:
    def test_advance_lsn(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        log.append("d", "update", "r2")
        assert log.apply("r1", 2) is True
        assert log.replica_status("r1").last_applied_lsn == 2

    def test_must_be_greater(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        log.append("d", "update", "r2")
        log.apply("r1", 2)
        assert log.apply("r1", 2) is False
        assert log.apply("r1", 1) is False

    def test_apply_unknown_replica(self):
        log = DocReplicationLog()
        log.append("d", "insert", "r2")
        assert log.apply("ghost", 1) is False

    def test_apply_updates_timestamp(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        log.apply("r1", 1, now=999.0)
        assert log.replica_status("r1").last_sync_at == 999.0

    def test_apply_updates_lag(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        for _ in range(5):
            log.append("d", "insert", "r2")
        log.apply("r1", 3)
        assert log.replica_status("r1").lag == 2


class TestLagFor:
    def test_lag_zero_when_no_entries(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        assert log.lag_for("r1") == 0

    def test_lag_counts_all_unapplied(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        log.append("d", "update", "r2")
        assert log.lag_for("r1") == 2

    def test_lag_after_apply(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        log.append("d", "update", "r2")
        log.apply("r1", 1)
        assert log.lag_for("r1") == 1

    def test_lag_none_for_unknown(self):
        log = DocReplicationLog()
        assert log.lag_for("ghost") is None


class TestReplicaStatus:
    def test_refreshes_lag(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        log.append("d", "update", "r2")
        s = log.replica_status("r1")
        assert s.lag == 2

    def test_none_for_unknown(self):
        log = DocReplicationLog()
        assert log.replica_status("ghost") is None

    def test_lag_after_apply(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "r2")
        log.append("d", "update", "r2")
        log.apply("r1", 2)
        s = log.replica_status("r1")
        assert s.lag == 0


class TestAllReplicas:
    def test_sorted_by_id(self):
        log = DocReplicationLog()
        log.register_replica("r3")
        log.register_replica("r1")
        log.register_replica("r2")
        ids = [s.replica_id for s in log.all_replicas()]
        assert ids == ["r1", "r2", "r3"]

    def test_lags_refreshed(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.register_replica("r2")
        log.append("d", "insert", "x")
        log.append("d", "update", "x")
        log.apply("r1", 1)
        replicas = {s.replica_id: s for s in log.all_replicas()}
        assert replicas["r1"].lag == 1
        assert replicas["r2"].lag == 2

    def test_empty(self):
        log = DocReplicationLog()
        assert log.all_replicas() == []


class TestGetEntry:
    def test_found(self):
        log = DocReplicationLog()
        e = log.append("d", "insert", "r1")
        assert log.get_entry(e.lsn) is e

    def test_not_found(self):
        log = DocReplicationLog()
        log.append("d", "insert", "r1")
        assert log.get_entry(999) is None

    def test_not_found_empty(self):
        log = DocReplicationLog()
        assert log.get_entry(1) is None


class TestEntriesForDoc:
    def test_returns_only_matching(self):
        log = DocReplicationLog()
        log.append("a", "insert", "r1")
        log.append("b", "insert", "r1")
        log.append("a", "update", "r1")
        res = log.entries_for_doc("a")
        assert len(res) == 2
        assert all(e.doc_id == "a" for e in res)

    def test_sorted_asc(self):
        log = DocReplicationLog()
        log.append("a", "insert", "r1")
        log.append("a", "update", "r1")
        log.append("a", "delete", "r1")
        lsns = [e.lsn for e in log.entries_for_doc("a")]
        assert lsns == sorted(lsns)

    def test_empty_for_unknown_doc(self):
        log = DocReplicationLog()
        log.append("a", "insert", "r1")
        assert log.entries_for_doc("nope") == []


class TestEntriesByOperation:
    def test_filtered(self):
        log = DocReplicationLog()
        log.append("a", "insert", "r1")
        log.append("b", "update", "r1")
        log.append("c", "insert", "r1")
        res = log.entries_by_operation("insert")
        assert len(res) == 2
        assert all(e.operation == "insert" for e in res)

    def test_sorted_asc(self):
        log = DocReplicationLog()
        log.append("a", "insert", "r1")
        log.append("a", "insert", "r1")
        log.append("a", "insert", "r1")
        lsns = [e.lsn for e in log.entries_by_operation("insert")]
        assert lsns == sorted(lsns)

    def test_empty_for_unknown_op(self):
        log = DocReplicationLog()
        log.append("a", "insert", "r1")
        assert log.entries_by_operation("frobnicate") == []


class TestTruncate:
    def test_removes_when_all_caught_up(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.register_replica("r2")
        log.append("d", "insert", "x")
        log.append("d", "update", "x")
        log.append("d", "delete", "x")
        log.apply("r1", 2)
        log.apply("r2", 2)
        removed = log.truncate(2)
        assert removed == 2

    def test_zero_when_lagging(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.register_replica("r2")
        log.append("d", "insert", "x")
        log.append("d", "update", "x")
        log.apply("r1", 2)
        # r2 still at 0
        removed = log.truncate(2)
        assert removed == 0

    def test_zero_when_no_replicas(self):
        log = DocReplicationLog()
        log.append("d", "insert", "x")
        assert log.truncate(1) == 0

    def test_truncate_partial(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "x")
        log.append("d", "update", "x")
        log.append("d", "delete", "x")
        log.apply("r1", 3)
        removed = log.truncate(2)
        assert removed == 2
        # entry 3 still present
        assert log.get_entry(3) is not None
        assert log.get_entry(1) is None
        assert log.get_entry(2) is None

    def test_truncate_does_not_reset_lsn(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.append("d", "insert", "x")
        log.apply("r1", 1)
        log.truncate(1)
        e = log.append("d", "update", "x")
        assert e.lsn == 2


class TestStats:
    def test_empty(self):
        log = DocReplicationLog()
        s = log.stats()
        assert s.total_entries == 0
        assert s.total_replicas == 0
        assert s.max_lag == 0
        assert s.avg_lag == 0.0

    def test_total_entries(self):
        log = DocReplicationLog()
        log.append("a", "insert", "r1")
        log.append("b", "insert", "r1")
        assert log.stats().total_entries == 2

    def test_total_replicas(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.register_replica("r2")
        assert log.stats().total_replicas == 2

    def test_max_lag(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.register_replica("r2")
        log.append("a", "insert", "x")
        log.append("b", "insert", "x")
        log.apply("r1", 1)
        # r1 lag = 1, r2 lag = 2
        assert log.stats().max_lag == 2

    def test_avg_lag(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        log.register_replica("r2")
        log.append("a", "insert", "x")
        log.append("b", "insert", "x")
        log.apply("r1", 1)
        # lags: 1 and 2, avg = 1.5
        assert log.stats().avg_lag == 1.5


class TestThreadSafety:
    def test_concurrent_appends(self):
        log = DocReplicationLog()
        N = 50
        T = 8

        def worker():
            for _ in range(N):
                log.append("d", "insert", "r1")

        threads = [threading.Thread(target=worker) for _ in range(T)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        s = log.stats()
        assert s.total_entries == N * T
        lsns = sorted(e.lsn for e in log.entries_by_operation("insert"))
        assert lsns == list(range(1, N * T + 1))

    def test_concurrent_appends_and_applies(self):
        log = DocReplicationLog()
        log.register_replica("r1")
        N = 30
        T = 4

        def appender():
            for _ in range(N):
                log.append("d", "update", "src")

        threads = [threading.Thread(target=appender) for _ in range(T)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        total = N * T
        assert log.lag_for("r1") == total
        assert log.apply("r1", total) is True
        assert log.lag_for("r1") == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
