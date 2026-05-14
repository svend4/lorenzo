"""Adaptive token-bucket sampler (E93).

An adaptive sampler reacts to load-feedback signals to grow or shrink the
sampling rate, clamped to a configured ``[min_rate, max_rate]`` range.
"""
from __future__ import annotations

import threading
from typing import Optional

from docstoolkit.token_sampler.sampler import SamplingDecision, TokenBucketSampler


class AdaptiveSampler:
    """Adapt sampling rate based on a binary load signal.

    Parameters
    ----------
    initial_rate:
        Initial sampling rate (events / second).
    min_rate:
        Lower bound for the rate after adjustments.
    max_rate:
        Upper bound for the rate after adjustments.
    adjustment_factor:
        Multiplicative factor applied on each :meth:`feedback` call.
        Must be > 1; otherwise the rate could never grow or shrink.
    """

    def __init__(
        self,
        initial_rate: float,
        min_rate: float = 0.1,
        max_rate: float = 1000.0,
        adjustment_factor: float = 1.2,
    ) -> None:
        if initial_rate <= 0:
            raise ValueError("initial_rate must be > 0")
        if min_rate <= 0:
            raise ValueError("min_rate must be > 0")
        if max_rate <= 0:
            raise ValueError("max_rate must be > 0")
        if min_rate > max_rate:
            raise ValueError("min_rate must be <= max_rate")
        if adjustment_factor <= 1.0:
            raise ValueError("adjustment_factor must be > 1.0")

        self._min_rate: float = float(min_rate)
        self._max_rate: float = float(max_rate)
        self._adjustment_factor: float = float(adjustment_factor)

        clamped_initial = max(self._min_rate, min(self._max_rate, float(initial_rate)))
        self._current_rate: float = clamped_initial
        self._sampler = TokenBucketSampler(rate_per_sec=clamped_initial)
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    #  Public API                                                        #
    # ------------------------------------------------------------------ #

    def feedback(self, load_high: bool) -> None:
        """React to a load signal.

        * ``load_high=True``  shrinks the rate (divide by adjustment_factor).
        * ``load_high=False`` grows  the rate (multiply by adjustment_factor).

        The new rate is clamped to ``[min_rate, max_rate]``.
        """
        with self._lock:
            if load_high:
                new_rate = self._current_rate / self._adjustment_factor
            else:
                new_rate = self._current_rate * self._adjustment_factor
            new_rate = max(self._min_rate, min(self._max_rate, new_rate))
            if new_rate != self._current_rate:
                self._current_rate = new_rate
                # Rebuild the underlying sampler so future decisions reflect
                # the new rate.  Stats are preserved by carrying them over.
                prior_stats = self._sampler.stats()
                self._sampler = TokenBucketSampler(rate_per_sec=new_rate)
                # Carry over keep/drop counters for continuity.
                self._sampler._kept = prior_stats["kept"]
                self._sampler._dropped = prior_stats["dropped"]

    def current_rate(self) -> float:
        """Return the currently configured sampling rate."""
        with self._lock:
            return self._current_rate

    def should_sample(self, now: Optional[float] = None) -> SamplingDecision:
        """Delegate sampling decision to the internal :class:`TokenBucketSampler`."""
        # Snapshot the sampler under the lock to be safe against concurrent
        # feedback() calls swapping it out.
        with self._lock:
            sampler = self._sampler
        return sampler.should_sample(now=now)

    # ------------------------------------------------------------------ #
    #  Introspection                                                     #
    # ------------------------------------------------------------------ #

    @property
    def min_rate(self) -> float:
        """The lower bound on the sampling rate."""
        return self._min_rate

    @property
    def max_rate(self) -> float:
        """The upper bound on the sampling rate."""
        return self._max_rate

    @property
    def adjustment_factor(self) -> float:
        """The multiplicative adjustment factor."""
        return self._adjustment_factor

    @property
    def sampler(self) -> TokenBucketSampler:
        """The currently-active internal sampler."""
        with self._lock:
            return self._sampler

    def stats(self) -> dict:
        """Forward stats from the underlying sampler, augmented with the rate."""
        with self._lock:
            sampler = self._sampler
        s = sampler.stats()
        s["rate"] = self._current_rate
        return s

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"AdaptiveSampler(current_rate={self._current_rate}, "
            f"min_rate={self._min_rate}, max_rate={self._max_rate}, "
            f"adjustment_factor={self._adjustment_factor})"
        )
