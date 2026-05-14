"""Tests for doc_replication module."""
import pytest

from docstoolkit.doc_replication import (
    DocReplication,
    Replica,
    ReplicaRole,
    ReplicationEvent,
    ReplicationStats,
    ReplicationStatus,
)


class TestReplicaRole:
    def test_values(self):
        assert ReplicaRole.PRIMARY.value == "primary"
        assert ReplicaRole.REPLICA.value == "replica"
        assert ReplicaRole.OFFLINE.value == "offline"

    def test_distinct(self):
        roles = {ReplicaRole.PRIMARY, ReplicaRole.REPLICA, ReplicaRole.OFFLINE}
        assert len(roles) == 3


class TestReplicationStatus:
    def test_values(self):
        assert ReplicationStatus.PENDING.value == "pending"
        assert ReplicationStatus.SYNCED.value == "synced"
        assert ReplicationStatus.FAILED.value == "failed"
        assert ReplicationStatus.CONFLICTING.value == "conflicting"

    def test_distinct(self):
        statuses = {
            ReplicationStatus.PENDING,
            ReplicationStatus.SYNCED,
            ReplicationStatus.FAILED,
            ReplicationStatus.CONFLICTING,
        }
        assert len(statuses) == 4


class TestReplica:
    def test_create(self):
        r = Replica(replica_id="r1", role=ReplicaRole.PRIMARY, endpoint="path://r1")
        assert r.replica_id == "r1"
        assert r.role == ReplicaRole.PRIMARY
        assert r.endpoint == "path://r1"
        assert r.last_sync_at == 0.0
        assert r.last_seq == 0

    def test_with_sync(self):
        r = Replica(
            replica_id="r2",
            role=ReplicaRole.REPLICA,
            endpoint="x",
            last_sync_at=10.5,
            last_seq=7,
        )
        assert r.last_sync_at == 10.5
        assert r.last_seq == 7


class TestReplicationEvent:
    def test_create(self):
        e = ReplicationEvent(event_seq=1, doc_id="d1", action="upsert")
        assert e.event_seq == 1
        assert e.doc_id == "d1"
        assert e.action == "upsert"
        assert e.payload == {}
        assert e.version == 1
        assert e.applied_to == set()

    def test_with_payload(self):
        e = ReplicationEvent(
            event_seq=2,
            doc_id="d2",
            action="delete",
            payload={"x": 1},
            timestamp=5.0,
            version=3,
        )
        assert e.payload == {"x": 1}
        assert e.timestamp == 5.0
        assert e.version == 3


class TestReplicationStats:
    def test_create(self):
        s = ReplicationStats(
            total_replicas=2,
            active_replicas=1,
            total_events=5,
            total_pending=3,
        )
        assert s.total_replicas == 2
        assert s.active_replicas == 1
        assert s.total_events == 5
        assert s.total_pending == 3
        assert s.lag_by_replica == {}

    def test_with_lag(self):
        s = ReplicationStats(
            total_replicas=2,
            active_replicas=2,
            total_events=10,
            total_pending=4,
            lag_by_replica={"r1": 0, "r2": 4},
        )
        assert s.lag_by_replica["r2"] == 4


class TestRegisterReplica:
    def test_register(self):
        d = DocReplication()
        r = d.register_replica("r1", ReplicaRole.PRIMARY, "ep1", now=1.0)
        assert r.replica_id == "r1"
        assert r.role == ReplicaRole.PRIMARY
        assert r.endpoint == "ep1"
        assert r.last_sync_at == 1.0

    def test_register_multiple(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        assert d.total_replicas == 2

    def test_overwrite(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1b")
        assert d.total_replicas == 1
        rs = d.replicas()
        assert rs[0].role == ReplicaRole.PRIMARY
        assert rs[0].endpoint == "ep1b"


class TestSetRole:
    def test_change_role(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        assert d.set_role("r1", ReplicaRole.PRIMARY) is True
        assert d.replicas()[0].role == ReplicaRole.PRIMARY

    def test_unknown(self):
        d = DocReplication()
        assert d.set_role("missing", ReplicaRole.PRIMARY) is False

    def test_to_offline(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        d.set_role("r1", ReplicaRole.OFFLINE)
        assert d.active_replicas() == []


class TestUnregisterReplica:
    def test_unregister(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        assert d.unregister_replica("r1") is True
        assert d.total_replicas == 0

    def test_unknown(self):
        d = DocReplication()
        assert d.unregister_replica("nope") is False

    def test_removes_applied_state(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        e = d.record_event("doc1", "upsert")
        d.mark_applied("r1", e.event_seq)
        assert d.unregister_replica("r1") is True
        # event should no longer have r1 in applied_to
        evs = d.events_since(0)
        assert "r1" not in evs[0].applied_to


class TestRecordEvent:
    def test_record(self):
        d = DocReplication()
        e = d.record_event("d1", "upsert", {"x": 1}, version=2, now=3.0)
        assert e.event_seq == 1
        assert e.doc_id == "d1"
        assert e.action == "upsert"
        assert e.payload == {"x": 1}
        assert e.version == 2
        assert e.timestamp == 3.0

    def test_seq_increments(self):
        d = DocReplication()
        a = d.record_event("d1", "upsert")
        b = d.record_event("d2", "upsert")
        c = d.record_event("d3", "delete")
        assert (a.event_seq, b.event_seq, c.event_seq) == (1, 2, 3)

    def test_default_payload(self):
        d = DocReplication()
        e = d.record_event("d1", "upsert")
        assert e.payload == {}

    def test_payload_copied(self):
        d = DocReplication()
        p = {"a": 1}
        e = d.record_event("d1", "upsert", p)
        p["a"] = 99
        assert e.payload == {"a": 1}


class TestPendingEventsFor:
    def test_all_pending_initially(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        d.record_event("d1", "upsert")
        d.record_event("d2", "upsert")
        pending = d.pending_events_for("r1")
        assert len(pending) == 2

    def test_after_apply(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        e1 = d.record_event("d1", "upsert")
        d.record_event("d2", "upsert")
        d.mark_applied("r1", e1.event_seq)
        pending = d.pending_events_for("r1")
        assert len(pending) == 1
        assert pending[0].doc_id == "d2"

    def test_unknown_replica(self):
        d = DocReplication()
        d.record_event("d1", "upsert")
        assert d.pending_events_for("nope") == []

    def test_empty_log(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        assert d.pending_events_for("r1") == []


class TestMarkApplied:
    def test_basic(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        e = d.record_event("d1", "upsert")
        assert d.mark_applied("r1", e.event_seq, now=5.0) is True
        rs = d.replicas()[0]
        assert rs.last_seq == 1
        assert rs.last_sync_at == 5.0

    def test_unknown_replica(self):
        d = DocReplication()
        e = d.record_event("d1", "upsert")
        assert d.mark_applied("nope", e.event_seq) is False

    def test_unknown_event(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        assert d.mark_applied("r1", 999) is False

    def test_updates_applied_to(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        e = d.record_event("d1", "upsert")
        d.mark_applied("r1", e.event_seq)
        ev = d.events_since(0)[0]
        assert "r1" in ev.applied_to

    def test_does_not_lower_last_seq(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        e1 = d.record_event("d1", "upsert")
        e2 = d.record_event("d2", "upsert")
        d.mark_applied("r1", e2.event_seq)
        d.mark_applied("r1", e1.event_seq)
        assert d.replicas()[0].last_seq == 2


class TestMarkFailed:
    def test_basic(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        e = d.record_event("d1", "upsert")
        assert d.mark_failed("r1", e.event_seq) is True

    def test_unknown_replica(self):
        d = DocReplication()
        e = d.record_event("d1", "upsert")
        assert d.mark_failed("nope", e.event_seq) is False

    def test_unknown_event(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        assert d.mark_failed("r1", 999) is False

    def test_apply_clears_failed(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        e = d.record_event("d1", "upsert")
        d.mark_failed("r1", e.event_seq)
        d.mark_applied("r1", e.event_seq)
        # internally cleared; no public API to inspect but should not crash on subsequent ops
        assert d.mark_failed("r1", e.event_seq) is True


class TestReplicas:
    def test_empty(self):
        d = DocReplication()
        assert d.replicas() == []

    def test_returns_all(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        d.register_replica("r3", ReplicaRole.OFFLINE, "ep3")
        assert len(d.replicas()) == 3


class TestActiveReplicas:
    def test_excludes_offline(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.register_replica("r2", ReplicaRole.OFFLINE, "ep2")
        d.register_replica("r3", ReplicaRole.REPLICA, "ep3")
        active = d.active_replicas()
        ids = {r.replica_id for r in active}
        assert ids == {"r1", "r3"}

    def test_all_active(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        assert len(d.active_replicas()) == 2

    def test_empty(self):
        d = DocReplication()
        assert d.active_replicas() == []


class TestEventsSince:
    def test_all(self):
        d = DocReplication()
        d.record_event("d1", "upsert")
        d.record_event("d2", "upsert")
        d.record_event("d3", "delete")
        assert len(d.events_since(0)) == 3

    def test_partial(self):
        d = DocReplication()
        d.record_event("d1", "upsert")
        d.record_event("d2", "upsert")
        d.record_event("d3", "delete")
        evs = d.events_since(1)
        assert len(evs) == 2
        assert evs[0].doc_id == "d2"

    def test_beyond(self):
        d = DocReplication()
        d.record_event("d1", "upsert")
        assert d.events_since(99) == []


class TestLatestEvent:
    def test_empty(self):
        d = DocReplication()
        assert d.latest_event() is None

    def test_one(self):
        d = DocReplication()
        e = d.record_event("d1", "upsert")
        assert d.latest_event().event_seq == e.event_seq

    def test_multiple(self):
        d = DocReplication()
        d.record_event("d1", "upsert")
        d.record_event("d2", "delete")
        latest = d.latest_event()
        assert latest.doc_id == "d2"


class TestReplicaLag:
    def test_zero_lag(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        assert d.replica_lag("r1") == 0

    def test_with_lag(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        d.record_event("d1", "upsert")
        d.record_event("d2", "upsert")
        d.record_event("d3", "upsert")
        assert d.replica_lag("r1") == 3

    def test_after_apply(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        e1 = d.record_event("d1", "upsert")
        d.record_event("d2", "upsert")
        d.mark_applied("r1", e1.event_seq)
        assert d.replica_lag("r1") == 1

    def test_unknown(self):
        d = DocReplication()
        assert d.replica_lag("nope") == 0


class TestStats:
    def test_empty(self):
        d = DocReplication()
        s = d.stats()
        assert s.total_replicas == 0
        assert s.active_replicas == 0
        assert s.total_events == 0
        assert s.total_pending == 0
        assert s.lag_by_replica == {}

    def test_with_data(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        d.register_replica("r3", ReplicaRole.OFFLINE, "ep3")
        d.record_event("d1", "upsert")
        d.record_event("d2", "upsert")
        s = d.stats()
        assert s.total_replicas == 3
        assert s.active_replicas == 2
        assert s.total_events == 2
        # pending: 2 events x 2 active replicas (offline excluded)
        assert s.total_pending == 4
        assert s.lag_by_replica["r1"] == 2

    def test_after_apply(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        e = d.record_event("d1", "upsert")
        d.mark_applied("r1", e.event_seq)
        s = d.stats()
        assert s.total_pending == 0
        assert s.lag_by_replica["r1"] == 0


class TestPurgeApplied:
    def test_nothing_to_purge(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        d.record_event("d1", "upsert")
        assert d.purge_applied() == 0

    def test_purge_all_applied(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        e1 = d.record_event("d1", "upsert")
        e2 = d.record_event("d2", "upsert")
        d.mark_applied("r1", e1.event_seq)
        d.mark_applied("r2", e1.event_seq)
        d.mark_applied("r1", e2.event_seq)
        d.mark_applied("r2", e2.event_seq)
        assert d.purge_applied() == 2
        assert d.total_events == 0

    def test_partial_purge(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        e1 = d.record_event("d1", "upsert")
        d.record_event("d2", "upsert")
        d.mark_applied("r1", e1.event_seq)
        d.mark_applied("r2", e1.event_seq)
        assert d.purge_applied() == 1
        assert d.total_events == 1

    def test_no_active_replicas(self):
        d = DocReplication()
        d.record_event("d1", "upsert")
        # No replicas to compare against — purge nothing
        assert d.purge_applied() == 0

    def test_ignores_offline_replicas(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        d.register_replica("r2", ReplicaRole.OFFLINE, "ep2")
        e = d.record_event("d1", "upsert")
        d.mark_applied("r1", e.event_seq)
        # r2 is offline so should not block purge
        assert d.purge_applied() == 1


class TestSetPrimary:
    def test_promote(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        assert d.set_primary("r1") is True
        assert d.primary().replica_id == "r1"

    def test_demotes_old_primary(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        d.set_primary("r2")
        rs = {r.replica_id: r.role for r in d.replicas()}
        assert rs["r1"] == ReplicaRole.REPLICA
        assert rs["r2"] == ReplicaRole.PRIMARY

    def test_unknown(self):
        d = DocReplication()
        assert d.set_primary("nope") is False

    def test_idempotent(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.set_primary("r1")
        assert d.primary().replica_id == "r1"


class TestPrimary:
    def test_none(self):
        d = DocReplication()
        assert d.primary() is None

    def test_no_primary(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.REPLICA, "ep1")
        assert d.primary() is None

    def test_returns_primary(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        assert d.primary().replica_id == "r1"


class TestTotalReplicas:
    def test_zero(self):
        d = DocReplication()
        assert d.total_replicas == 0

    def test_count(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        assert d.total_replicas == 2


class TestTotalEvents:
    def test_zero(self):
        d = DocReplication()
        assert d.total_events == 0

    def test_count(self):
        d = DocReplication()
        d.record_event("d1", "upsert")
        d.record_event("d2", "delete")
        assert d.total_events == 2


class TestClear:
    def test_clears_replicas(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.clear()
        assert d.total_replicas == 0

    def test_clears_events(self):
        d = DocReplication()
        d.record_event("d1", "upsert")
        d.clear()
        assert d.total_events == 0

    def test_resets_seq(self):
        d = DocReplication()
        d.record_event("d1", "upsert")
        d.record_event("d2", "upsert")
        d.clear()
        e = d.record_event("d3", "upsert")
        assert e.event_seq == 1


class TestEdgeCases:
    def test_offline_replica_no_pending(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.OFFLINE, "ep1")
        d.record_event("d1", "upsert")
        # Offline still has pending events technically but stats excludes them
        s = d.stats()
        assert s.total_pending == 0

    def test_multiple_events_same_doc(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.record_event("d1", "upsert", {"v": 1})
        d.record_event("d1", "upsert", {"v": 2})
        d.record_event("d1", "delete")
        assert d.total_events == 3

    def test_complete_replication_flow(self):
        d = DocReplication()
        d.register_replica("p", ReplicaRole.PRIMARY, "ep-p")
        d.register_replica("r", ReplicaRole.REPLICA, "ep-r")
        e1 = d.record_event("doc1", "upsert", {"x": 1})
        e2 = d.record_event("doc2", "upsert", {"y": 2})
        # Apply to both
        for rid in ("p", "r"):
            for seq in (e1.event_seq, e2.event_seq):
                d.mark_applied(rid, seq)
        # Purge fully replicated
        purged = d.purge_applied()
        assert purged == 2
        assert d.total_events == 0
        # Stats
        s = d.stats()
        assert s.total_pending == 0

    def test_failover_scenario(self):
        d = DocReplication()
        d.register_replica("r1", ReplicaRole.PRIMARY, "ep1")
        d.register_replica("r2", ReplicaRole.REPLICA, "ep2")
        d.register_replica("r3", ReplicaRole.REPLICA, "ep3")
        # primary fails
        d.set_role("r1", ReplicaRole.OFFLINE)
        # promote r2
        d.set_primary("r2")
        assert d.primary().replica_id == "r2"
        # r3 still replica
        roles = {r.replica_id: r.role for r in d.replicas()}
        assert roles["r1"] == ReplicaRole.OFFLINE
        assert roles["r3"] == ReplicaRole.REPLICA

    def test_lag_after_mass_events(self):
        d = DocReplication()
        d.register_replica("slow", ReplicaRole.REPLICA, "ep1")
        for i in range(10):
            d.record_event(f"d{i}", "upsert")
        assert d.replica_lag("slow") == 10
