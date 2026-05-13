"""Token bucket primitive for the E93 token-bucket sampler module.

A small thread-safe token bucket that supports deterministic testing
through an explicit ``now`` parameter (so tests do not have to sleep).
"""
from __future__ import annotations

import threading
import time
from typing import Optional, Tuple


class TokenBucket:
    """Thread-safe token bucket.

    Parameters
    ----------
    capacity:
        Maximum number of tokens the bucket can hold (also the burst size).
        Must be a positive integer.
    refill_rate:
        Tokens added per second.  May be 0 (no refill) but never negative.
    """

    def __init__(self, capacity: int, refill_rate: float) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        if refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")
        self._capacity: int = int(capacity)
        self._refill_rate: float = float(refill_rate)
        self._tokens: float = float(capacity)
        self._last_refill: float = time.time()
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                  #
    # ------------------------------------------------------------------ #

    def _refill(self, now: Optional[float] = None) -> None:
        """Add tokens proportional to elapsed time.

        Must be called while holding ``self._lock``.
        """
        if now is None:
            now = time.time()
        elapsed = now - self._last_refill
        if elapsed > 0 and self._refill_rate > 0:
            added = elapsed * self._refill_rate
            self._tokens = min(float(self._capacity), self._tokens + added)
        # Always advance last_refill so future deltas are correct, even
        # for zero refill_rate.
        if elapsed > 0:
            self._last_refill = now

    # ------------------------------------------------------------------ #
    #  Public API                                                        #
    # ------------------------------------------------------------------ #

    def consume(self, amount: int = 1, now: Optional[float] = None) -> bool:
        """Refill then consume ``amount`` tokens.

        Returns ``True`` if the tokens were consumed, ``False`` otherwise
        (the bucket is left unchanged when ``False`` is returned).
        """
        if amount < 0:
            raise ValueError("amount must be >= 0")
        with self._lock:
            self._refill(now)
            if self._tokens >= amount:
                self._tokens -= amount
                return True
            return False

    def try_consume(
        self, amount: int = 1, now: Optional[float] = None
    ) -> Tuple[bool, float]:
        """Like :meth:`consume` but also returns the remaining token count.

        Returns
        -------
        tuple
            ``(success, current_tokens_remaining)`` where ``success`` is
            ``True`` iff the requested amount was consumed.  The
            remaining-token value reflects the bucket *after* the
            potential consumption.
        """
        if amount < 0:
            raise ValueError("amount must be >= 0")
        with self._lock:
            self._refill(now)
            if self._tokens >= amount:
                self._tokens -= amount
                return True, self._tokens
            return False, self._tokens

    def available(self, now: Optional[float] = None) -> float:
        """Return the number of tokens currently available (after refill)."""
        with self._lock:
            self._refill(now)
            return self._tokens

    def reset(self) -> None:
        """Refill the bucket back to full capacity and reset the refill clock."""
        with self._lock:
            self._tokens = float(self._capacity)
            self._last_refill = time.time()

    def time_until_available(
        self, amount: int = 1, now: Optional[float] = None
    ) -> float:
        """Estimate the time (in seconds) until ``amount`` tokens are available.

        Returns ``0.0`` if the bucket already has enough tokens.  If the
        bucket is configured with ``refill_rate == 0`` and does not
        already have the tokens, returns ``float('inf')``.
        """
        if amount < 0:
            raise ValueError("amount must be >= 0")
        with self._lock:
            self._refill(now)
            if self._tokens >= amount:
                return 0.0
            if amount > self._capacity:
                # Cannot ever be satisfied – the bucket caps out at capacity.
                if self._refill_rate <= 0:
                    return float("inf")
                # Time to fill from current level to capacity.
                needed = float(self._capacity) - self._tokens
                return needed / self._refill_rate
            if self._refill_rate <= 0:
                return float("inf")
            needed = amount - self._tokens
            return needed / self._refill_rate

    # ------------------------------------------------------------------ #
    #  Introspection                                                     #
    # ------------------------------------------------------------------ #

    @property
    def capacity(self) -> int:
        """The bucket capacity (max tokens)."""
        return self._capacity

    @property
    def refill_rate(self) -> float:
        """The refill rate in tokens per second."""
        return self._refill_rate

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"TokenBucket(capacity={self._capacity}, "
            f"refill_rate={self._refill_rate}, tokens={self._tokens:.3f})"
        )
