"""Token-bucket throttling with burst capacity and refill rate per key.

Stdlib-only (threading + dataclasses). Deterministic via explicit ``now=`` param.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ThrottleConfig:
    """Configuration for a single throttle bucket."""

    capacity: int  # max burst
    refill_rate: float  # tokens per second


@dataclass
class Bucket:
    """Live state of a single throttle bucket."""

    key: str
    capacity: int
    refill_rate: float
    tokens: float
    last_refill: float


@dataclass
class ThrottleResult:
    """Result of an :py:meth:`ThrottleMeter.acquire` call."""

    allowed: bool
    tokens_remaining: float
    retry_after_seconds: float  # 0 if allowed


class ThrottleMeter:
    """Token-bucket throttle meter with per-key buckets and a default config.

    All public methods are thread-safe.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._configs: dict[str, ThrottleConfig] = {}
        self._buckets: dict[str, Bucket] = {}
        self._default: Optional[ThrottleConfig] = None
        self._allowed_count: int = 0
        self._denied_count: int = 0

    # ------------------------------------------------------------------ config

    def configure(
        self, key: str, capacity: int, refill_rate: float
    ) -> ThrottleConfig:
        """Configure (or reconfigure) a bucket for ``key``.

        Capacity/refill_rate must be non-negative.
        Existing bucket state is reset to a full bucket.
        """
        if capacity < 0:
            raise ValueError("capacity must be >= 0")
        if refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")
        with self._lock:
            cfg = ThrottleConfig(capacity=capacity, refill_rate=refill_rate)
            self._configs[key] = cfg
            # reset bucket to full
            self._buckets[key] = Bucket(
                key=key,
                capacity=capacity,
                refill_rate=refill_rate,
                tokens=float(capacity),
                last_refill=0.0,
            )
            return cfg

    def configure_default(
        self, capacity: int, refill_rate: float
    ) -> ThrottleConfig:
        """Set a default config used for unconfigured keys on demand."""
        if capacity < 0:
            raise ValueError("capacity must be >= 0")
        if refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")
        with self._lock:
            self._default = ThrottleConfig(
                capacity=capacity, refill_rate=refill_rate
            )
            return self._default

    def get_config(self, key: str) -> Optional[ThrottleConfig]:
        """Return config for ``key``, or None if not configured."""
        with self._lock:
            return self._configs.get(key)

    # ----------------------------------------------------------------- helpers

    def _ensure_bucket_locked(self, key: str, now: float) -> Bucket:
        """Return the bucket for ``key``, creating it from default if needed.

        Caller must hold ``self._lock``.
        Raises KeyError if no config and no default.
        """
        bucket = self._buckets.get(key)
        if bucket is not None:
            return bucket
        cfg = self._configs.get(key)
        if cfg is None:
            if self._default is None:
                raise KeyError(
                    f"no config for key={key!r} and no default configured"
                )
            cfg = self._default
            self._configs[key] = cfg
        bucket = Bucket(
            key=key,
            capacity=cfg.capacity,
            refill_rate=cfg.refill_rate,
            tokens=float(cfg.capacity),
            last_refill=now,
        )
        self._buckets[key] = bucket
        return bucket

    @staticmethod
    def _refill_locked(bucket: Bucket, now: float) -> None:
        """Refill the bucket up to its capacity. Caller must hold the lock."""
        elapsed = now - bucket.last_refill
        if elapsed < 0:
            # Clock went backwards — clamp to zero and reset last_refill.
            elapsed = 0.0
        added = bucket.refill_rate * elapsed
        new_tokens = bucket.tokens + added
        if new_tokens > bucket.capacity:
            new_tokens = float(bucket.capacity)
        bucket.tokens = new_tokens
        bucket.last_refill = now

    # ----------------------------------------------------------------- acquire

    def acquire(
        self, key: str, tokens: int = 1, now: float = 0.0
    ) -> ThrottleResult:
        """Try to consume ``tokens`` from the bucket for ``key``.

        Returns ``ThrottleResult`` with ``allowed`` flag, ``tokens_remaining``
        and ``retry_after_seconds`` (0 if allowed).
        """
        if tokens < 0:
            raise ValueError("tokens must be >= 0")
        with self._lock:
            bucket = self._ensure_bucket_locked(key, now)
            self._refill_locked(bucket, now)

            if tokens > bucket.capacity:
                # Can never satisfy request — always denied; never refills enough.
                if bucket.refill_rate > 0:
                    retry = (tokens - bucket.tokens) / bucket.refill_rate
                else:
                    retry = float("inf")
                self._denied_count += 1
                return ThrottleResult(
                    allowed=False,
                    tokens_remaining=bucket.tokens,
                    retry_after_seconds=max(retry, 0.0),
                )

            if bucket.tokens >= tokens:
                bucket.tokens -= tokens
                self._allowed_count += 1
                return ThrottleResult(
                    allowed=True,
                    tokens_remaining=bucket.tokens,
                    retry_after_seconds=0.0,
                )

            # Not enough — compute retry_after.
            deficit = tokens - bucket.tokens
            if bucket.refill_rate > 0:
                retry = deficit / bucket.refill_rate
            else:
                retry = float("inf")
            self._denied_count += 1
            return ThrottleResult(
                allowed=False,
                tokens_remaining=bucket.tokens,
                retry_after_seconds=retry,
            )

    # -------------------------------------------------------------------- peek

    def peek(self, key: str, now: float = 0.0) -> Optional[Bucket]:
        """Return a copy of the bucket state without mutating it.

        Returns None if the key is not configured and no default is set.
        Does not consume tokens, but does logically advance the bucket clock
        in the returned snapshot.
        """
        with self._lock:
            bucket = self._buckets.get(key)
            if bucket is None:
                cfg = self._configs.get(key) or self._default
                if cfg is None:
                    return None
                # Synthesize snapshot without registering a bucket.
                return Bucket(
                    key=key,
                    capacity=cfg.capacity,
                    refill_rate=cfg.refill_rate,
                    tokens=float(cfg.capacity),
                    last_refill=now,
                )
            # Snapshot with refill applied — do NOT mutate the live bucket.
            elapsed = now - bucket.last_refill
            if elapsed < 0:
                elapsed = 0.0
            new_tokens = bucket.tokens + bucket.refill_rate * elapsed
            if new_tokens > bucket.capacity:
                new_tokens = float(bucket.capacity)
            return Bucket(
                key=bucket.key,
                capacity=bucket.capacity,
                refill_rate=bucket.refill_rate,
                tokens=new_tokens,
                last_refill=now,
            )

    # --------------------------------------------------------------- wait_time

    def wait_time(self, key: str, tokens: int, now: float = 0.0) -> float:
        """Return seconds until at least ``tokens`` tokens are available.

        Returns 0.0 if enough tokens are already available.
        Returns float('inf') when refill_rate is 0 and we can't satisfy now.
        Raises KeyError if key is unconfigured and no default is set.
        """
        if tokens < 0:
            raise ValueError("tokens must be >= 0")
        with self._lock:
            bucket = self._ensure_bucket_locked(key, now)
            # Compute snapshot tokens after refill without mutating timestamp.
            elapsed = now - bucket.last_refill
            if elapsed < 0:
                elapsed = 0.0
            current = bucket.tokens + bucket.refill_rate * elapsed
            if current > bucket.capacity:
                current = float(bucket.capacity)

            if current >= tokens:
                return 0.0
            if tokens > bucket.capacity:
                # Impossible to satisfy
                if bucket.refill_rate <= 0:
                    return float("inf")
                return (tokens - current) / bucket.refill_rate
            if bucket.refill_rate <= 0:
                return float("inf")
            return (tokens - current) / bucket.refill_rate

    # ------------------------------------------------------------------- reset

    def reset(self, key: str) -> bool:
        """Reset the bucket for ``key`` back to full capacity.

        Returns True if a bucket was reset, False if the key was not known.
        """
        with self._lock:
            cfg = self._configs.get(key)
            if cfg is None and key not in self._buckets:
                return False
            if cfg is None:
                # No config but a bucket exists (shouldn't happen normally).
                bucket = self._buckets[key]
                bucket.tokens = float(bucket.capacity)
                bucket.last_refill = 0.0
                return True
            self._buckets[key] = Bucket(
                key=key,
                capacity=cfg.capacity,
                refill_rate=cfg.refill_rate,
                tokens=float(cfg.capacity),
                last_refill=0.0,
            )
            return True

    def reset_all(self) -> int:
        """Reset every known bucket back to full capacity.

        Returns the number of buckets that were reset.
        """
        with self._lock:
            count = 0
            for key, cfg in self._configs.items():
                self._buckets[key] = Bucket(
                    key=key,
                    capacity=cfg.capacity,
                    refill_rate=cfg.refill_rate,
                    tokens=float(cfg.capacity),
                    last_refill=0.0,
                )
                count += 1
            # Buckets without configs (edge): also restore those.
            for key, bucket in list(self._buckets.items()):
                if key in self._configs:
                    continue
                bucket.tokens = float(bucket.capacity)
                bucket.last_refill = 0.0
                count += 1
            return count

    # ------------------------------------------------------------------ remove

    def remove(self, key: str) -> bool:
        """Remove config and bucket for ``key``.

        Returns True if anything was removed.
        """
        with self._lock:
            had = key in self._configs or key in self._buckets
            self._configs.pop(key, None)
            self._buckets.pop(key, None)
            return had

    # ---------------------------------------------------------------- all_keys

    def all_keys(self) -> list[str]:
        """Return a sorted list of all known keys (configured or with bucket)."""
        with self._lock:
            keys = set(self._configs) | set(self._buckets)
            return sorted(keys)

    # ------------------------------------------------------------------- stats

    def stats(self) -> dict:
        """Return aggregate stats:

        - ``allowed_count``: total successful acquires
        - ``denied_count``: total denied acquires
        - ``total_keys``: number of known keys
        """
        with self._lock:
            return {
                "allowed_count": self._allowed_count,
                "denied_count": self._denied_count,
                "total_keys": len(set(self._configs) | set(self._buckets)),
            }
