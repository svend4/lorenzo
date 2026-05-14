"""E344 DocReplicationLog implementation."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ReplicationEntry:
    """A single replicated document operation."""

    lsn: int
    doc_id: str
    operation: str
    source_replica: str
    created_at: float = 0.0
    payload: dict = field(default_factory=dict)


@dataclass
class ReplicaStatus:
    """Sync status of a single replica."""

    replica_id: str
    last_applied_lsn: int = 0
    last_sync_at: float = 0.0
    lag: int = 0


@dataclass
class ReplicationStats:
    """Aggregate statistics for the replication log."""

    total_entries: int
    total_replicas: int
    max_lag: int
    avg_lag: float


class DocReplicationLog:
    """Thread-safe replication log for cross-region document sync."""

    def __init__(self) -> None:
        self._entries: list[ReplicationEntry] = []
        self._replicas: dict[str, ReplicaStatus] = {}
        self._next_lsn: int = 1
        self._lock = threading.Lock()

    # ----- append / replicas -----

    def append(
        self,
        doc_id: str,
        operation: str,
        source_replica: str,
        payload: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> ReplicationEntry:
        """Append a new replication entry. Returns the created entry."""
        with self._lock:
            ts = now if now is not None else time.time()
            entry = ReplicationEntry(
                lsn=self._next_lsn,
                doc_id=doc_id,
                operation=operation,
                source_replica=source_replica,
                created_at=ts,
                payload=dict(payload) if payload else {},
            )
            self._next_lsn += 1
            self._entries.append(entry)
            return entry

    def register_replica(
        self, replica_id: str, now: Optional[float] = None
    ) -> ReplicaStatus:
        """Register a new replica at lsn 0."""
        with self._lock:
            ts = now if now is not None else time.time()
            status = ReplicaStatus(
                replica_id=replica_id,
                last_applied_lsn=0,
                last_sync_at=ts,
                lag=len(self._entries),
            )
            self._replicas[replica_id] = status
            return status

    def unregister_replica(self, replica_id: str) -> bool:
        """Remove a replica. Returns True if it existed."""
        with self._lock:
            if replica_id in self._replicas:
                del self._replicas[replica_id]
                return True
            return False

    # ----- queries -----

    def pending_for(
        self, replica_id: str, limit: Optional[int] = None
    ) -> list[ReplicationEntry]:
        """Return entries with lsn > replica's last_applied_lsn, sorted asc."""
        with self._lock:
            status = self._replicas.get(replica_id)
            if status is None:
                return []
            last = status.last_applied_lsn
            pending = [e for e in self._entries if e.lsn > last]
            pending.sort(key=lambda e: e.lsn)
            if limit is not None:
                pending = pending[:limit]
            return pending

    def apply(
        self, replica_id: str, lsn: int, now: Optional[float] = None
    ) -> bool:
        """Advance replica's last_applied_lsn to lsn (must be greater)."""
        with self._lock:
            status = self._replicas.get(replica_id)
            if status is None:
                return False
            if lsn <= status.last_applied_lsn:
                return False
            status.last_applied_lsn = lsn
            status.last_sync_at = now if now is not None else time.time()
            status.lag = sum(1 for e in self._entries if e.lsn > lsn)
            return True

    def lag_for(self, replica_id: str) -> Optional[int]:
        """Number of entries with lsn > last_applied_lsn for replica."""
        with self._lock:
            status = self._replicas.get(replica_id)
            if status is None:
                return None
            last = status.last_applied_lsn
            return sum(1 for e in self._entries if e.lsn > last)

    def replica_status(self, replica_id: str) -> Optional[ReplicaStatus]:
        """Return replica status with refreshed lag."""
        with self._lock:
            status = self._replicas.get(replica_id)
            if status is None:
                return None
            last = status.last_applied_lsn
            status.lag = sum(1 for e in self._entries if e.lsn > last)
            return status

    def all_replicas(self) -> list[ReplicaStatus]:
        """All replicas sorted by replica_id, with refreshed lag."""
        with self._lock:
            result = []
            for rid in sorted(self._replicas.keys()):
                status = self._replicas[rid]
                last = status.last_applied_lsn
                status.lag = sum(1 for e in self._entries if e.lsn > last)
                result.append(status)
            return result

    def get_entry(self, lsn: int) -> Optional[ReplicationEntry]:
        """Look up a single entry by lsn."""
        with self._lock:
            for e in self._entries:
                if e.lsn == lsn:
                    return e
            return None

    def entries_for_doc(self, doc_id: str) -> list[ReplicationEntry]:
        """All entries for a given doc_id, sorted by lsn asc."""
        with self._lock:
            res = [e for e in self._entries if e.doc_id == doc_id]
            res.sort(key=lambda e: e.lsn)
            return res

    def entries_by_operation(self, operation: str) -> list[ReplicationEntry]:
        """All entries with the given operation, sorted by lsn asc."""
        with self._lock:
            res = [e for e in self._entries if e.operation == operation]
            res.sort(key=lambda e: e.lsn)
            return res

    # ----- maintenance -----

    def truncate(self, up_to_lsn: int) -> int:
        """Remove entries with lsn <= up_to_lsn if all replicas caught up."""
        with self._lock:
            if not self._replicas:
                return 0
            min_applied = min(s.last_applied_lsn for s in self._replicas.values())
            if min_applied < up_to_lsn:
                return 0
            before = len(self._entries)
            self._entries = [e for e in self._entries if e.lsn > up_to_lsn]
            return before - len(self._entries)

    def stats(self) -> ReplicationStats:
        """Aggregate stats; refreshes lags."""
        with self._lock:
            total_entries = len(self._entries)
            total_replicas = len(self._replicas)
            lags: list[int] = []
            for status in self._replicas.values():
                last = status.last_applied_lsn
                lag = sum(1 for e in self._entries if e.lsn > last)
                status.lag = lag
                lags.append(lag)
            max_lag = max(lags) if lags else 0
            avg_lag = (sum(lags) / len(lags)) if lags else 0.0
            return ReplicationStats(
                total_entries=total_entries,
                total_replicas=total_replicas,
                max_lag=max_lag,
                avg_lag=avg_lag,
            )
