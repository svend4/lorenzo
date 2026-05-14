"""Token-bucket sampler (E93).

A sampler decides which items to *keep* and which to *drop* based on a
configured rate (tokens / second) with bursting controlled by a capacity
parameter.
"""
from __future__ import annotations

import enum
import threading
from typing import Iterable, List, Optional

from docstoolkit.token_sampler.bucket import TokenBucket


class SamplingDecision(enum.Enum):
    """Outcome of a single sampling decision."""

    KEEP = "keep"
    DROP = "drop"


class TokenBucketSampler:
    """Decide which items to keep using a token bucket.

    Parameters
    ----------
    rate_per_sec:
        Steady-state sampling rate (events / second).
    burst:
        Maximum burst size (defaults to ``int(rate_per_sec)`` capped to at
        least ``1``).
    """

    def __init__(self, rate_per_sec: float, burst: Optional[int] = None) -> None:
        if rate_per_sec < 0:
            raise ValueError("rate_per_sec must be >= 0")
        self._rate_per_sec: float = float(rate_per_sec)
        if burst is None:
            burst = max(1, int(rate_per_sec))
        if burst <= 0:
            raise ValueError("burst must be > 0")
        self._burst: int = int(burst)
        self._bucket = TokenBucket(capacity=self._burst, refill_rate=self._rate_per_sec)
        self._kept: int = 0
        self._dropped: int = 0
        self._stats_lock = threading.Lock()

    # ------------------------------------------------------------------ #
    #  Sampling API                                                      #
    # ------------------------------------------------------------------ #

    def should_sample(self, now: Optional[float] = None) -> SamplingDecision:
        """Make a single sampling decision.

        Consumes one token and returns :data:`SamplingDecision.KEEP` if it
        was available, otherwise :data:`SamplingDecision.DROP`.
        """
        allowed = self._bucket.consume(1, now=now)
        with self._stats_lock:
            if allowed:
                self._kept += 1
            else:
                self._dropped += 1
        return SamplingDecision.KEEP if allowed else SamplingDecision.DROP

    def sample(self, items: Iterable) -> List:
        """Return only those items for which :meth:`should_sample` is ``KEEP``."""
        kept = []
        for item in items:
            if self.should_sample() is SamplingDecision.KEEP:
                kept.append(item)
        return kept

    # ------------------------------------------------------------------ #
    #  Stats / introspection                                             #
    # ------------------------------------------------------------------ #

    def stats(self) -> dict:
        """Return the running keep/drop counts and configured rate."""
        with self._stats_lock:
            return {
                "kept": self._kept,
                "dropped": self._dropped,
                "rate": self._rate_per_sec,
            }

    def reset_stats(self) -> None:
        """Reset the keep / drop counters back to zero."""
        with self._stats_lock:
            self._kept = 0
            self._dropped = 0

    @property
    def rate_per_sec(self) -> float:
        """The configured steady-state rate (events / second)."""
        return self._rate_per_sec

    @property
    def burst(self) -> int:
        """The configured burst (bucket capacity)."""
        return self._burst

    @property
    def bucket(self) -> TokenBucket:
        """The underlying token bucket (mostly for introspection)."""
        return self._bucket

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"TokenBucketSampler(rate_per_sec={self._rate_per_sec}, "
            f"burst={self._burst})"
        )
