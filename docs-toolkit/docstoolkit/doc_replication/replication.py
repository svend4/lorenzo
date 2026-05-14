"""Document replication coordinator with primary-replica topology and event log."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ReplicaRole(Enum):
    """Role of a replica in the topology."""

    PRIMARY = "primary"
    REPLICA = "replica"
    OFFLINE = "offline"


class ReplicationStatus(Enum):
    """Status of replication for a particular event/replica pair."""

    PENDING = "pending"
    SYNCED = "synced"
    FAILED = "failed"
    CONFLICTING = "conflicting"


@dataclass
class Replica:
    """A node in the replication topology."""

    replica_id: str
    role: ReplicaRole
    endpoint: str
    last_sync_at: float = 0.0
    last_seq: int = 0


@dataclass
class ReplicationEvent:
    """A recorded replication event in the log."""

    event_seq: int
    doc_id: str
    action: str  # "upsert", "delete"
    payload: dict = field(default_factory=dict)
    timestamp: float = 0.0
    version: int = 1
    applied_to: set = field(default_factory=set)  # replica_ids


@dataclass
class ReplicationStats:
    """Replication coordinator statistics."""

    total_replicas: int
    active_replicas: int
    total_events: int
    total_pending: int
    lag_by_replica: dict = field(default_factory=dict)


class DocReplication:
    """Coordinates document replication across primary/replica nodes."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._replicas: dict[str, Replica] = {}
        self._events: list[ReplicationEvent] = []
        self._failed: dict[str, set] = {}  # replica_id -> set of failed seqs
        self._seq: int = 0

    def register_replica(
        self,
        replica_id: str,
        role: ReplicaRole,
        endpoint: str,
        now: float = 0.0,
    ) -> Replica:
        """Register a new replica or overwrite existing one."""
        with self._lock:
            replica = Replica(
                replica_id=replica_id,
                role=role,
                endpoint=endpoint,
                last_sync_at=now,
                last_seq=0,
            )
            self._replicas[replica_id] = replica
            self._failed.setdefault(replica_id, set())
            return replica

    def set_role(self, replica_id: str, role: ReplicaRole) -> bool:
        """Change the role of a registered replica."""
        with self._lock:
            replica = self._replicas.get(replica_id)
            if replica is None:
                return False
            replica.role = role
            return True

    def unregister_replica(self, replica_id: str) -> bool:
        """Remove a replica from the topology."""
        with self._lock:
            if replica_id not in self._replicas:
                return False
            del self._replicas[replica_id]
            self._failed.pop(replica_id, None)
            # Remove replica from applied_to sets so purge can still work
            for event in self._events:
                event.applied_to.discard(replica_id)
            return True

    def record_event(
        self,
        doc_id: str,
        action: str,
        payload: dict = None,
        version: int = 1,
        now: float = 0.0,
    ) -> ReplicationEvent:
        """Append a new event to the replication log."""
        with self._lock:
            self._seq += 1
            event = ReplicationEvent(
                event_seq=self._seq,
                doc_id=doc_id,
                action=action,
                payload=dict(payload) if payload else {},
                timestamp=now,
                version=version,
                applied_to=set(),
            )
            self._events.append(event)
            return event

    def pending_events_for(self, replica_id: str) -> list[ReplicationEvent]:
        """Return events not yet applied to the given replica."""
        with self._lock:
            replica = self._replicas.get(replica_id)
            if replica is None:
                return []
            result = []
            for event in self._events:
                if replica_id in event.applied_to:
                    continue
                if event.event_seq <= replica.last_seq:
                    continue
                result.append(event)
            return result

    def mark_applied(
        self, replica_id: str, event_seq: int, now: float = 0.0
    ) -> bool:
        """Mark a particular event as applied to a replica."""
        with self._lock:
            replica = self._replicas.get(replica_id)
            if replica is None:
                return False
            event = self._find_event(event_seq)
            if event is None:
                return False
            event.applied_to.add(replica_id)
            if event_seq > replica.last_seq:
                replica.last_seq = event_seq
            replica.last_sync_at = now
            self._failed.get(replica_id, set()).discard(event_seq)
            return True

    def mark_failed(self, replica_id: str, event_seq: int) -> bool:
        """Mark a particular event as failed for a replica."""
        with self._lock:
            replica = self._replicas.get(replica_id)
            if replica is None:
                return False
            event = self._find_event(event_seq)
            if event is None:
                return False
            self._failed.setdefault(replica_id, set()).add(event_seq)
            return True

    def replicas(self) -> list[Replica]:
        """Return all registered replicas."""
        with self._lock:
            return list(self._replicas.values())

    def active_replicas(self) -> list[Replica]:
        """Return replicas not in OFFLINE role."""
        with self._lock:
            return [
                r for r in self._replicas.values() if r.role != ReplicaRole.OFFLINE
            ]

    def events_since(self, seq: int) -> list[ReplicationEvent]:
        """Return events with event_seq > seq."""
        with self._lock:
            return [e for e in self._events if e.event_seq > seq]

    def latest_event(self) -> Optional[ReplicationEvent]:
        """Return the most recent event or None."""
        with self._lock:
            if not self._events:
                return None
            return self._events[-1]

    def replica_lag(self, replica_id: str) -> int:
        """Return how many events the replica is behind."""
        with self._lock:
            replica = self._replicas.get(replica_id)
            if replica is None:
                return 0
            return max(0, self._seq - replica.last_seq)

    def stats(self) -> ReplicationStats:
        """Compute aggregate replication statistics."""
        with self._lock:
            active = [
                r for r in self._replicas.values() if r.role != ReplicaRole.OFFLINE
            ]
            lag_by_replica = {
                r.replica_id: max(0, self._seq - r.last_seq)
                for r in self._replicas.values()
            }
            # Count pending = sum of pending per active replica
            total_pending = 0
            for replica in active:
                for event in self._events:
                    if replica.replica_id in event.applied_to:
                        continue
                    if event.event_seq <= replica.last_seq:
                        continue
                    total_pending += 1
            return ReplicationStats(
                total_replicas=len(self._replicas),
                active_replicas=len(active),
                total_events=len(self._events),
                total_pending=total_pending,
                lag_by_replica=lag_by_replica,
            )

    def purge_applied(self) -> int:
        """Remove events applied to all active replicas. Returns count removed."""
        with self._lock:
            active_ids = {
                r.replica_id
                for r in self._replicas.values()
                if r.role != ReplicaRole.OFFLINE
            }
            if not active_ids:
                # Nothing to compare against: purge nothing
                return 0
            keep = []
            removed = 0
            for event in self._events:
                if active_ids.issubset(event.applied_to):
                    removed += 1
                else:
                    keep.append(event)
            self._events = keep
            return removed

    def set_primary(self, replica_id: str) -> bool:
        """Promote replica_id to PRIMARY and demote others to REPLICA."""
        with self._lock:
            if replica_id not in self._replicas:
                return False
            for rid, replica in self._replicas.items():
                if rid == replica_id:
                    replica.role = ReplicaRole.PRIMARY
                elif replica.role == ReplicaRole.PRIMARY:
                    replica.role = ReplicaRole.REPLICA
            return True

    def primary(self) -> Optional[Replica]:
        """Return the current PRIMARY replica, or None."""
        with self._lock:
            for replica in self._replicas.values():
                if replica.role == ReplicaRole.PRIMARY:
                    return replica
            return None

    @property
    def total_replicas(self) -> int:
        with self._lock:
            return len(self._replicas)

    @property
    def total_events(self) -> int:
        with self._lock:
            return len(self._events)

    def clear(self) -> None:
        """Reset all state."""
        with self._lock:
            self._replicas.clear()
            self._events.clear()
            self._failed.clear()
            self._seq = 0

    # internal
    def _find_event(self, event_seq: int) -> Optional[ReplicationEvent]:
        for event in self._events:
            if event.event_seq == event_seq:
                return event
        return None
