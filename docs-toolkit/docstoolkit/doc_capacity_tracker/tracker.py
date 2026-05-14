"""E424 DocCapacityTracker — thread-safe capacity tracking per bucket."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CapacityBucket:
    """A capacity bucket tracking used vs total capacity."""

    name: str
    capacity: int
    used: int = 0
    created_at: float = 0.0


@dataclass
class CapacityCheck:
    """Outcome of an acquire attempt."""

    bucket: str
    allowed: bool
    requested: int
    available: int
    reason: str = ""


@dataclass
class CapacityStats:
    """Aggregate statistics across all buckets."""

    total_buckets: int
    total_capacity: int
    total_used: int
    buckets_at_capacity: int


class DocCapacityTracker:
    """Thread-safe tracker for capacity limits per resource bucket."""

    def __init__(self) -> None:
        self._buckets: dict[str, CapacityBucket] = {}
        self._lock = threading.Lock()

    def create_bucket(
        self, name: str, capacity: int, now: Optional[float] = None
    ) -> CapacityBucket:
        """Create or replace a bucket with the given capacity.

        Raises ValueError if ``capacity`` is negative.
        """
        if capacity < 0:
            raise ValueError(f"capacity must be >= 0, got {capacity}")
        ts = time.time() if now is None else now
        with self._lock:
            bucket = CapacityBucket(
                name=name, capacity=capacity, used=0, created_at=ts
            )
            self._buckets[name] = bucket
            return bucket

    def delete_bucket(self, name: str) -> bool:
        """Delete a bucket. Returns True if it existed."""
        with self._lock:
            return self._buckets.pop(name, None) is not None

    def get_bucket(self, name: str) -> Optional[CapacityBucket]:
        """Return the bucket or None."""
        with self._lock:
            return self._buckets.get(name)

    def set_capacity(self, name: str, new_capacity: int) -> bool:
        """Adjust the capacity of an existing bucket.

        Raises ValueError if ``new_capacity`` is negative.
        Returns True if bucket existed.
        """
        if new_capacity < 0:
            raise ValueError(f"capacity must be >= 0, got {new_capacity}")
        with self._lock:
            bucket = self._buckets.get(name)
            if bucket is None:
                return False
            bucket.capacity = new_capacity
            return True

    def acquire(self, name: str, units: int = 1) -> CapacityCheck:
        """Attempt to acquire ``units`` from the bucket atomically."""
        with self._lock:
            bucket = self._buckets.get(name)
            if bucket is None:
                return CapacityCheck(
                    bucket=name,
                    allowed=False,
                    requested=units,
                    available=0,
                    reason="bucket not found",
                )
            if units < 0:
                return CapacityCheck(
                    bucket=name,
                    allowed=False,
                    requested=units,
                    available=bucket.capacity - bucket.used,
                    reason="negative units",
                )
            available = bucket.capacity - bucket.used
            if bucket.used + units <= bucket.capacity:
                bucket.used += units
                return CapacityCheck(
                    bucket=name,
                    allowed=True,
                    requested=units,
                    available=bucket.capacity - bucket.used,
                    reason="",
                )
            return CapacityCheck(
                bucket=name,
                allowed=False,
                requested=units,
                available=available,
                reason="capacity exceeded",
            )

    def release(self, name: str, units: int = 1) -> bool:
        """Release ``units`` back to the bucket. Floors at 0."""
        with self._lock:
            bucket = self._buckets.get(name)
            if bucket is None:
                return False
            bucket.used = max(0, bucket.used - units)
            return True

    def try_acquire(self, name: str, units: int = 1) -> bool:
        """Convenience wrapper returning just allowed bool."""
        return self.acquire(name, units).allowed

    def available(self, name: str) -> Optional[int]:
        """Return remaining capacity or None if bucket missing."""
        with self._lock:
            bucket = self._buckets.get(name)
            if bucket is None:
                return None
            return bucket.capacity - bucket.used

    def usage_pct(self, name: str) -> Optional[float]:
        """Return used/capacity ratio (1.0 if capacity == 0)."""
        with self._lock:
            bucket = self._buckets.get(name)
            if bucket is None:
                return None
            if bucket.capacity == 0:
                return 1.0
            return bucket.used / bucket.capacity

    def list_buckets(self) -> list[CapacityBucket]:
        """Return all buckets sorted by name."""
        with self._lock:
            return sorted(self._buckets.values(), key=lambda b: b.name)

    def buckets_near_capacity(
        self, threshold_pct: float = 0.9
    ) -> list[CapacityBucket]:
        """Return buckets at or above the threshold usage, sorted by name."""
        with self._lock:
            result = []
            for bucket in self._buckets.values():
                if bucket.capacity == 0:
                    pct = 1.0
                else:
                    pct = bucket.used / bucket.capacity
                if pct >= threshold_pct:
                    result.append(bucket)
            return sorted(result, key=lambda b: b.name)

    def reset(self, name: str) -> bool:
        """Reset used count to 0. Returns True if bucket existed."""
        with self._lock:
            bucket = self._buckets.get(name)
            if bucket is None:
                return False
            bucket.used = 0
            return True

    def clear(self) -> int:
        """Remove all buckets. Returns count cleared."""
        with self._lock:
            count = len(self._buckets)
            self._buckets.clear()
            return count

    def stats(self) -> CapacityStats:
        """Return aggregate statistics."""
        with self._lock:
            total_capacity = sum(b.capacity for b in self._buckets.values())
            total_used = sum(b.used for b in self._buckets.values())
            at_cap = sum(
                1 for b in self._buckets.values() if b.used >= b.capacity
            )
            return CapacityStats(
                total_buckets=len(self._buckets),
                total_capacity=total_capacity,
                total_used=total_used,
                buckets_at_capacity=at_cap,
            )
