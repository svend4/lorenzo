"""Per-document throttling with token bucket per doc_id.

Stdlib-only (threading + dataclasses). Deterministic via explicit ``now=`` arg.
Different from ``throttle_meter``: each bucket is tied to a ``doc_id``, supports
per-doc enable/disable, and tracks per-bucket request/denial counters.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class ThrottleConfig:
    """Default configuration for new per-document buckets."""

    burst_capacity: int = 10
    refill_rate: float = 1.0  # tokens per second
    enabled: bool = True


@dataclass
class Bucket:
    """Live state of a single per-document throttle bucket."""

    doc_id: str
    tokens: float
    last_refill: float
    burst_capacity: int
    refill_rate: float
    total_requests: int = 0
    total_denied: int = 0
    enabled: bool = True


@dataclass
class ThrottleResult:
    """Result of a :py:meth:`DocThrottler.acquire` call."""

    allowed: bool
    doc_id: str
    tokens_remaining: float
    retry_after_seconds: float


class DocThrottler:
    """Per-document token-bucket throttler.

    Auto-creates a bucket on first ``acquire`` using the default config.
    All public methods are thread-safe.
    """

    def __init__(self, default_config: Optional[ThrottleConfig] = None) -> None:
        self._lock = threading.Lock()
        self._default: ThrottleConfig = default_config or ThrottleConfig()
        self._buckets: dict[str, Bucket] = {}
        self._total_requests: int = 0
        self._total_denied: int = 0

    # ----------------------------------------------------------------- helpers

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return time.time() if now is None else now

    def _ensure_bucket_locked(self, doc_id: str, now: float) -> Bucket:
        """Return the bucket for ``doc_id``, creating it from default if needed.

        Caller must hold ``self._lock``.
        """
        bucket = self._buckets.get(doc_id)
        if bucket is not None:
            return bucket
        bucket = Bucket(
            doc_id=doc_id,
            tokens=float(self._default.burst_capacity),
            last_refill=now,
            burst_capacity=self._default.burst_capacity,
            refill_rate=self._default.refill_rate,
            enabled=self._default.enabled,
        )
        self._buckets[doc_id] = bucket
        return bucket

    @staticmethod
    def _refill_locked(bucket: Bucket, now: float) -> None:
        """Refill the bucket up to its capacity. Caller must hold the lock."""
        elapsed = now - bucket.last_refill
        if elapsed < 0:
            elapsed = 0.0
        new_tokens = bucket.tokens + bucket.refill_rate * elapsed
        if new_tokens > bucket.burst_capacity:
            new_tokens = float(bucket.burst_capacity)
        bucket.tokens = new_tokens
        bucket.last_refill = now

    # ----------------------------------------------------------------- acquire

    def acquire(
        self,
        doc_id: str,
        tokens: int = 1,
        now: Optional[float] = None,
    ) -> ThrottleResult:
        """Try to consume ``tokens`` from the bucket for ``doc_id``."""
        if tokens < 0:
            raise ValueError("tokens must be >= 0")
        t = self._now(now)
        with self._lock:
            bucket = self._ensure_bucket_locked(doc_id, t)
            bucket.total_requests += 1
            self._total_requests += 1

            # Disabled throttling — always allow, do not deduct tokens.
            if not bucket.enabled:
                # Still refill so peek reflects elapsed time.
                self._refill_locked(bucket, t)
                return ThrottleResult(
                    allowed=True,
                    doc_id=doc_id,
                    tokens_remaining=bucket.tokens,
                    retry_after_seconds=0.0,
                )

            self._refill_locked(bucket, t)

            # Request larger than capacity — never satisfiable in one shot.
            if tokens > bucket.burst_capacity:
                if bucket.refill_rate > 0:
                    retry = (tokens - bucket.tokens) / bucket.refill_rate
                else:
                    retry = float("inf")
                bucket.total_denied += 1
                self._total_denied += 1
                return ThrottleResult(
                    allowed=False,
                    doc_id=doc_id,
                    tokens_remaining=bucket.tokens,
                    retry_after_seconds=max(retry, 0.0),
                )

            if bucket.tokens >= tokens:
                bucket.tokens -= tokens
                return ThrottleResult(
                    allowed=True,
                    doc_id=doc_id,
                    tokens_remaining=bucket.tokens,
                    retry_after_seconds=0.0,
                )

            deficit = tokens - bucket.tokens
            if bucket.refill_rate > 0:
                retry = deficit / bucket.refill_rate
            else:
                retry = float("inf")
            bucket.total_denied += 1
            self._total_denied += 1
            return ThrottleResult(
                allowed=False,
                doc_id=doc_id,
                tokens_remaining=bucket.tokens,
                retry_after_seconds=retry,
            )

    # -------------------------------------------------------------------- peek

    def peek(
        self, doc_id: str, now: Optional[float] = None
    ) -> Optional[Bucket]:
        """Return a snapshot of the bucket state with refill applied.

        Does NOT mutate the live bucket. Returns None if doc_id is unknown.
        """
        t = self._now(now)
        with self._lock:
            bucket = self._buckets.get(doc_id)
            if bucket is None:
                return None
            elapsed = t - bucket.last_refill
            if elapsed < 0:
                elapsed = 0.0
            new_tokens = bucket.tokens + bucket.refill_rate * elapsed
            if new_tokens > bucket.burst_capacity:
                new_tokens = float(bucket.burst_capacity)
            return Bucket(
                doc_id=bucket.doc_id,
                tokens=new_tokens,
                last_refill=t,
                burst_capacity=bucket.burst_capacity,
                refill_rate=bucket.refill_rate,
                total_requests=bucket.total_requests,
                total_denied=bucket.total_denied,
                enabled=bucket.enabled,
            )

    # --------------------------------------------------------------- wait_time

    def wait_time(
        self,
        doc_id: str,
        tokens: int,
        now: Optional[float] = None,
    ) -> float:
        """Return seconds until ``tokens`` tokens are available for ``doc_id``."""
        if tokens < 0:
            raise ValueError("tokens must be >= 0")
        t = self._now(now)
        with self._lock:
            bucket = self._ensure_bucket_locked(doc_id, t)
            elapsed = t - bucket.last_refill
            if elapsed < 0:
                elapsed = 0.0
            current = bucket.tokens + bucket.refill_rate * elapsed
            if current > bucket.burst_capacity:
                current = float(bucket.burst_capacity)

            if current >= tokens:
                return 0.0
            deficit = tokens - current
            if bucket.refill_rate <= 0:
                return float("inf")
            return deficit / bucket.refill_rate

    # --------------------------------------------------------------- configure

    def configure(
        self,
        doc_id: str,
        burst_capacity: Optional[int] = None,
        refill_rate: Optional[float] = None,
    ) -> bool:
        """Reconfigure an existing bucket. Returns True if updated.

        Creates the bucket from defaults first if it doesn't exist.
        Updating ``burst_capacity`` clamps current tokens to the new cap.
        """
        if burst_capacity is not None and burst_capacity < 0:
            raise ValueError("burst_capacity must be >= 0")
        if refill_rate is not None and refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")
        t = self._now(None)
        with self._lock:
            bucket = self._ensure_bucket_locked(doc_id, t)
            changed = False
            if burst_capacity is not None:
                bucket.burst_capacity = burst_capacity
                if bucket.tokens > burst_capacity:
                    bucket.tokens = float(burst_capacity)
                changed = True
            if refill_rate is not None:
                bucket.refill_rate = refill_rate
                changed = True
            return changed

    # ------------------------------------------------------------------- reset

    def reset(self, doc_id: str) -> bool:
        """Reset a bucket back to full capacity. Returns True if found."""
        with self._lock:
            bucket = self._buckets.get(doc_id)
            if bucket is None:
                return False
            bucket.tokens = float(bucket.burst_capacity)
            bucket.last_refill = self._now(None)
            return True

    def reset_all(self) -> int:
        """Reset every bucket. Returns the number of buckets reset."""
        t = self._now(None)
        with self._lock:
            count = 0
            for bucket in self._buckets.values():
                bucket.tokens = float(bucket.burst_capacity)
                bucket.last_refill = t
                count += 1
            return count

    # ------------------------------------------------------- enable / disable

    def disable_throttling(self, doc_id: str) -> bool:
        """Disable throttling for ``doc_id`` (auto-creates bucket if missing)."""
        t = self._now(None)
        with self._lock:
            bucket = self._ensure_bucket_locked(doc_id, t)
            was_enabled = bucket.enabled
            bucket.enabled = False
            return was_enabled

    def enable_throttling(self, doc_id: str) -> bool:
        """Enable throttling for ``doc_id`` (auto-creates bucket if missing)."""
        t = self._now(None)
        with self._lock:
            bucket = self._ensure_bucket_locked(doc_id, t)
            was_disabled = not bucket.enabled
            bucket.enabled = True
            return was_disabled

    def is_throttled(self, doc_id: str) -> bool:
        """True if throttling is enabled AND tokens are exhausted (< 1)."""
        t = self._now(None)
        with self._lock:
            bucket = self._buckets.get(doc_id)
            if bucket is None:
                return False
            if not bucket.enabled:
                return False
            elapsed = t - bucket.last_refill
            if elapsed < 0:
                elapsed = 0.0
            current = bucket.tokens + bucket.refill_rate * elapsed
            if current > bucket.burst_capacity:
                current = float(bucket.burst_capacity)
            return current < 1.0

    # ------------------------------------------------------------- set_default

    def set_default(
        self,
        burst_capacity: Optional[int] = None,
        refill_rate: Optional[float] = None,
    ) -> ThrottleConfig:
        """Update the default config used for newly created buckets."""
        if burst_capacity is not None and burst_capacity < 0:
            raise ValueError("burst_capacity must be >= 0")
        if refill_rate is not None and refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")
        with self._lock:
            if burst_capacity is not None:
                self._default.burst_capacity = burst_capacity
            if refill_rate is not None:
                self._default.refill_rate = refill_rate
            return ThrottleConfig(
                burst_capacity=self._default.burst_capacity,
                refill_rate=self._default.refill_rate,
                enabled=self._default.enabled,
            )

    # ------------------------------------------------------------- introspect

    def all_doc_ids(self) -> list[str]:
        """Sorted list of all known doc_ids."""
        with self._lock:
            return sorted(self._buckets.keys())

    @property
    def total_requests(self) -> int:
        with self._lock:
            return self._total_requests

    @property
    def total_denied(self) -> int:
        with self._lock:
            return self._total_denied

    def most_throttled(self, top_k: int = 10) -> list[tuple[str, int]]:
        """Top doc_ids by denial count: list of ``(doc_id, total_denied)``."""
        if top_k < 0:
            raise ValueError("top_k must be >= 0")
        with self._lock:
            pairs = [
                (b.doc_id, b.total_denied)
                for b in self._buckets.values()
                if b.total_denied > 0
            ]
        pairs.sort(key=lambda p: (-p[1], p[0]))
        return pairs[:top_k]

    def clear(self) -> None:
        """Remove all buckets and reset aggregate counters."""
        with self._lock:
            self._buckets.clear()
            self._total_requests = 0
            self._total_denied = 0
