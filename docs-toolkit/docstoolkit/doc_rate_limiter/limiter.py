"""Per-key token-bucket rate limiter for document operations (E280)."""
import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class RateLimit:
    key: str
    capacity: float
    refill_rate: float
    current_tokens: float
    last_refill_at: float


@dataclass
class AllowResult:
    key: str
    allowed: bool
    tokens_remaining: float
    wait_seconds: float


@dataclass
class RateLimiterStats:
    total_keys: int
    total_allowed: int
    total_denied: int
    allow_rate: float


_DEFAULT_CAPACITY = 10.0
_DEFAULT_REFILL_RATE = 1.0


class DocRateLimiter:
    def __init__(self):
        self._lock = threading.Lock()
        self._buckets: dict[str, RateLimit] = {}
        self._allowed = 0
        self._denied = 0

    # ------------------------------------------------------------------
    # Internal helpers (must be called with lock held)
    # ------------------------------------------------------------------

    def _refill(self, bucket: RateLimit, now: float) -> None:
        elapsed = max(0.0, now - bucket.last_refill_at)
        bucket.current_tokens = min(
            bucket.capacity,
            bucket.current_tokens + elapsed * bucket.refill_rate,
        )
        bucket.last_refill_at = now

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def configure(
        self,
        key: str,
        capacity: float,
        refill_rate: float,
        now: Optional[float] = None,
    ) -> RateLimit:
        if now is None:
            now = time.time()
        with self._lock:
            bucket = RateLimit(
                key=key,
                capacity=capacity,
                refill_rate=refill_rate,
                current_tokens=capacity,
                last_refill_at=now,
            )
            self._buckets[key] = bucket
            return RateLimit(
                key=bucket.key,
                capacity=bucket.capacity,
                refill_rate=bucket.refill_rate,
                current_tokens=bucket.current_tokens,
                last_refill_at=bucket.last_refill_at,
            )

    def allow(
        self,
        key: str,
        tokens: float = 1.0,
        now: Optional[float] = None,
    ) -> AllowResult:
        if now is None:
            now = time.time()
        with self._lock:
            if key not in self._buckets:
                self._buckets[key] = RateLimit(
                    key=key,
                    capacity=_DEFAULT_CAPACITY,
                    refill_rate=_DEFAULT_REFILL_RATE,
                    current_tokens=_DEFAULT_CAPACITY,
                    last_refill_at=now,
                )
            bucket = self._buckets[key]
            self._refill(bucket, now)
            if bucket.current_tokens >= tokens:
                bucket.current_tokens -= tokens
                self._allowed += 1
                return AllowResult(
                    key=key,
                    allowed=True,
                    tokens_remaining=bucket.current_tokens,
                    wait_seconds=0.0,
                )
            else:
                wait = (tokens - bucket.current_tokens) / bucket.refill_rate
                self._denied += 1
                return AllowResult(
                    key=key,
                    allowed=False,
                    tokens_remaining=bucket.current_tokens,
                    wait_seconds=wait,
                )

    def reset(self, key: str, now: Optional[float] = None) -> bool:
        if now is None:
            now = time.time()
        with self._lock:
            if key not in self._buckets:
                return False
            bucket = self._buckets[key]
            bucket.current_tokens = bucket.capacity
            bucket.last_refill_at = now
            return True

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._buckets:
                del self._buckets[key]
                return True
            return False

    def get_limit(self, key: str) -> Optional[RateLimit]:
        with self._lock:
            b = self._buckets.get(key)
            if b is None:
                return None
            return RateLimit(
                key=b.key,
                capacity=b.capacity,
                refill_rate=b.refill_rate,
                current_tokens=b.current_tokens,
                last_refill_at=b.last_refill_at,
            )

    def keys(self) -> list:
        with self._lock:
            return sorted(self._buckets.keys())

    def stats(self) -> RateLimiterStats:
        with self._lock:
            total = self._allowed + self._denied
            rate = self._allowed / total if total > 0 else 1.0
            return RateLimiterStats(
                total_keys=len(self._buckets),
                total_allowed=self._allowed,
                total_denied=self._denied,
                allow_rate=rate,
            )

    @property
    def total_keys(self) -> int:
        with self._lock:
            return len(self._buckets)
