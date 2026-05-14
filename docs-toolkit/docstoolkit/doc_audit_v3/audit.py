"""E277 DocAuditV3 — high-volume audit log with batch writes and partitions."""
from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class AuditEntry:
    """A single audit entry, assigned to a partition."""

    entry_id: int
    partition: str
    actor: str
    action: str
    resource: str
    timestamp: float
    details: dict = field(default_factory=dict)


@dataclass
class BatchStats:
    """Outcome of a batch_record call."""

    entries_written: int
    partitions_touched: set
    duration_ms: float = 0.0


@dataclass
class AuditStats:
    """Aggregate statistics across the audit log."""

    total_entries: int
    total_partitions: int
    entries_per_partition: dict
    oldest_at: Optional[float] = None
    newest_at: Optional[float] = None


# ---------------------------------------------------------------------------
# Default partition function
# ---------------------------------------------------------------------------


def _default_partition(now: float) -> str:
    """Default partitioning: YYYY-MM derived from timestamp."""
    return datetime.fromtimestamp(now).strftime("%Y-%m")


# ---------------------------------------------------------------------------
# DocAuditV3
# ---------------------------------------------------------------------------


class DocAuditV3:
    """High-performance audit log with batch writes, partitioning, snapshots."""

    def __init__(self, partition_func: Optional[Callable[[float], str]] = None):
        self._partition_func = partition_func or _default_partition
        self._lock = threading.Lock()
        self._next_id: int = 1
        # entry_id -> AuditEntry
        self._by_id: dict = {}
        # partition -> list[entry_id]
        self._by_partition: dict = {}

    # ---------------------------- recording ---------------------------------

    def record(
        self,
        actor: str,
        action: str,
        resource: str,
        details: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> AuditEntry:
        """Record a single audit entry."""
        ts = time.time() if now is None else now
        with self._lock:
            return self._record_locked(actor, action, resource, details, ts)

    def _record_locked(
        self,
        actor: str,
        action: str,
        resource: str,
        details: Optional[dict],
        ts: float,
    ) -> AuditEntry:
        entry_id = self._next_id
        self._next_id += 1
        partition = self._partition_func(ts)
        entry = AuditEntry(
            entry_id=entry_id,
            partition=partition,
            actor=actor,
            action=action,
            resource=resource,
            timestamp=ts,
            details=dict(details) if details else {},
        )
        self._by_id[entry_id] = entry
        self._by_partition.setdefault(partition, []).append(entry_id)
        return entry

    def batch_record(self, entries: list) -> BatchStats:
        """Record many entries atomically under one lock."""
        start = time.time()
        written = 0
        partitions_touched: set = set()
        with self._lock:
            for raw in entries:
                ts = raw.get("now")
                if ts is None:
                    ts = time.time()
                entry = self._record_locked(
                    actor=raw.get("actor", ""),
                    action=raw.get("action", ""),
                    resource=raw.get("resource", ""),
                    details=raw.get("details"),
                    ts=ts,
                )
                partitions_touched.add(entry.partition)
                written += 1
        duration_ms = (time.time() - start) * 1000.0
        return BatchStats(
            entries_written=written,
            partitions_touched=partitions_touched,
            duration_ms=duration_ms,
        )

    # ---------------------------- queries -----------------------------------

    def get_entry(self, entry_id: int) -> Optional[AuditEntry]:
        with self._lock:
            return self._by_id.get(entry_id)

    def entries_in_partition(self, partition: str) -> list:
        with self._lock:
            ids = self._by_partition.get(partition, [])
            return [self._by_id[i] for i in ids]

    def entries_for_actor(
        self,
        actor: str,
        partition: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list:
        with self._lock:
            if partition is not None:
                ids = self._by_partition.get(partition, [])
                candidates = (self._by_id[i] for i in ids)
            else:
                candidates = (self._by_id[i] for i in sorted(self._by_id.keys()))
            result = []
            for entry in candidates:
                if entry.actor == actor:
                    result.append(entry)
                    if limit is not None and len(result) >= limit:
                        break
            return result

    def entries_for_resource(
        self,
        resource: str,
        partition: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list:
        with self._lock:
            if partition is not None:
                ids = self._by_partition.get(partition, [])
                candidates = (self._by_id[i] for i in ids)
            else:
                candidates = (self._by_id[i] for i in sorted(self._by_id.keys()))
            result = []
            for entry in candidates:
                if entry.resource == resource:
                    result.append(entry)
                    if limit is not None and len(result) >= limit:
                        break
            return result

    def partitions(self) -> list:
        with self._lock:
            return sorted(self._by_partition.keys())

    def partition_for(self, now: float) -> str:
        return self._partition_func(now)

    def count_entries(self, partition: Optional[str] = None) -> int:
        with self._lock:
            if partition is None:
                return len(self._by_id)
            return len(self._by_partition.get(partition, []))

    def recent(self, limit: int = 10, partition: Optional[str] = None) -> list:
        with self._lock:
            if partition is not None:
                ids = list(self._by_partition.get(partition, []))
            else:
                ids = sorted(self._by_id.keys())
            ids = ids[-limit:] if limit > 0 else []
            return [self._by_id[i] for i in reversed(ids)]

    # ---------------------------- mutation ----------------------------------

    def drop_partition(self, partition: str) -> int:
        with self._lock:
            ids = self._by_partition.pop(partition, [])
            for i in ids:
                self._by_id.pop(i, None)
            return len(ids)

    def clear(self) -> None:
        with self._lock:
            self._by_id.clear()
            self._by_partition.clear()
            self._next_id = 1

    # ---------------------------- snapshot ----------------------------------

    def snapshot(self) -> bytes:
        with self._lock:
            payload = {
                "next_id": self._next_id,
                "entries": [
                    {
                        "entry_id": e.entry_id,
                        "partition": e.partition,
                        "actor": e.actor,
                        "action": e.action,
                        "resource": e.resource,
                        "timestamp": e.timestamp,
                        "details": e.details,
                    }
                    for e in self._by_id.values()
                ],
            }
        return json.dumps(payload).encode("utf-8")

    def restore(self, data: bytes) -> int:
        payload = json.loads(data.decode("utf-8"))
        with self._lock:
            self._by_id.clear()
            self._by_partition.clear()
            self._next_id = int(payload.get("next_id", 1))
            count = 0
            for raw in payload.get("entries", []):
                entry = AuditEntry(
                    entry_id=int(raw["entry_id"]),
                    partition=str(raw["partition"]),
                    actor=str(raw["actor"]),
                    action=str(raw["action"]),
                    resource=str(raw["resource"]),
                    timestamp=float(raw["timestamp"]),
                    details=dict(raw.get("details") or {}),
                )
                self._by_id[entry.entry_id] = entry
                self._by_partition.setdefault(entry.partition, []).append(
                    entry.entry_id
                )
                count += 1
            # Ensure partition lists are ordered by entry_id
            for k in self._by_partition:
                self._by_partition[k].sort()
            # Ensure next_id is greater than any seen id
            if self._by_id:
                max_id = max(self._by_id.keys())
                if self._next_id <= max_id:
                    self._next_id = max_id + 1
            return count

    # ---------------------------- stats -------------------------------------

    def stats(self) -> AuditStats:
        with self._lock:
            per_part = {k: len(v) for k, v in self._by_partition.items()}
            oldest: Optional[float] = None
            newest: Optional[float] = None
            for e in self._by_id.values():
                if oldest is None or e.timestamp < oldest:
                    oldest = e.timestamp
                if newest is None or e.timestamp > newest:
                    newest = e.timestamp
            return AuditStats(
                total_entries=len(self._by_id),
                total_partitions=len(self._by_partition),
                entries_per_partition=per_part,
                oldest_at=oldest,
                newest_at=newest,
            )

    @property
    def total_entries(self) -> int:
        with self._lock:
            return len(self._by_id)

    @property
    def total_partitions(self) -> int:
        with self._lock:
            return len(self._by_partition)
