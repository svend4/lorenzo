"""Token bucket rate limiter per document/key.

Pure stdlib implementation, thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class BucketState:
    """Current state of a token bucket."""

    key: str
    tokens: float
    capacity: float
    refill_rate: float
    last_refill_at: float = 0.0


@dataclass
class BucketStats:
    """Aggregate statistics across all buckets."""

    total_buckets: int
    total_allowed: int
    total_denied: int
    current_total_tokens: float


class DocTokenBucket:
    """Token bucket rate limiter keyed by string identifier."""

    def __init__(self) -> None:
        self._buckets: dict[str, BucketState] = {}
        self._allowed: int = 0
        self._denied: int = 0
        self._lock = threading.Lock()

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return time.monotonic() if now is None else now

    def _refill(self, state: BucketState, now: float) -> None:
        """Internal helper. Refill tokens based on elapsed time."""
        elapsed = max(0.0, now - state.last_refill_at)
        if elapsed > 0 and state.refill_rate > 0:
            state.tokens = min(state.capacity, state.tokens + elapsed * state.refill_rate)
        state.last_refill_at = now

    def register(
        self,
        key: str,
        capacity: float,
        refill_rate: float,
        initial_tokens: Optional[float] = None,
        now: Optional[float] = None,
    ) -> BucketState:
        """Create or replace a bucket."""
        ts = self._now(now)
        tokens = capacity if initial_tokens is None else initial_tokens
        if tokens > capacity:
            tokens = capacity
        if tokens < 0:
            tokens = 0.0
        state = BucketState(
            key=key,
            tokens=float(tokens),
            capacity=float(capacity),
            refill_rate=float(refill_rate),
            last_refill_at=ts,
        )
        with self._lock:
            self._buckets[key] = state
        return state

    def consume(
        self,
        key: str,
        count: float = 1.0,
        now: Optional[float] = None,
    ) -> bool:
        """Attempt to consume ``count`` tokens from bucket ``key``."""
        ts = self._now(now)
        with self._lock:
            state = self._buckets.get(key)
            if state is None:
                self._denied += 1
                return False
            self._refill(state, ts)
            if state.tokens >= count:
                state.tokens -= count
                self._allowed += 1
                return True
            self._denied += 1
            return False

    def peek(self, key: str, now: Optional[float] = None) -> Optional[float]:
        """Return current refilled token count, or None if missing."""
        ts = self._now(now)
        with self._lock:
            state = self._buckets.get(key)
            if state is None:
                return None
            self._refill(state, ts)
            return state.tokens

    def restore(
        self,
        key: str,
        count: float,
        now: Optional[float] = None,
    ) -> bool:
        """Refill then add ``count`` tokens up to capacity."""
        ts = self._now(now)
        with self._lock:
            state = self._buckets.get(key)
            if state is None:
                return False
            self._refill(state, ts)
            state.tokens = min(state.capacity, state.tokens + count)
            return True

    def reset(self, key: str, now: Optional[float] = None) -> bool:
        """Reset bucket to full capacity."""
        ts = self._now(now)
        with self._lock:
            state = self._buckets.get(key)
            if state is None:
                return False
            state.tokens = state.capacity
            state.last_refill_at = ts
            return True

    def remove(self, key: str) -> bool:
        """Remove a bucket entirely."""
        with self._lock:
            if key in self._buckets:
                del self._buckets[key]
                return True
            return False

    def get_state(self, key: str) -> Optional[BucketState]:
        """Return the BucketState for ``key`` or None."""
        with self._lock:
            return self._buckets.get(key)

    def list_keys(self) -> list[str]:
        """Return sorted list of registered keys."""
        with self._lock:
            return sorted(self._buckets.keys())

    def stats(self, now: Optional[float] = None) -> BucketStats:
        """Return aggregate stats; refills all buckets at ``now``."""
        ts = self._now(now)
        with self._lock:
            total_tokens = 0.0
            for state in self._buckets.values():
                self._refill(state, ts)
                total_tokens += state.tokens
            return BucketStats(
                total_buckets=len(self._buckets),
                total_allowed=self._allowed,
                total_denied=self._denied,
                current_total_tokens=total_tokens,
            )
