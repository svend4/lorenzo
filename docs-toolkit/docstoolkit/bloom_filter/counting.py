"""Counting Bloom filter — supports element removal.

Each slot is an 8-bit unsigned counter (saturating at 255).  Adding
increments all ``k`` slots; removing decrements them.  Membership tests
return ``True`` iff every slot is non-zero.

Pure stdlib only.
"""
from __future__ import annotations

from typing import Iterable

from docstoolkit.bloom_filter.bloom import _compute_m_k, _to_bytes
import hashlib


_COUNTER_MAX = 255


class CountingBloomFilter:
    """A Bloom filter with per-slot counters; supports ``remove``."""

    def __init__(self, capacity: int = 1000, error_rate: float = 0.01) -> None:
        self.capacity = int(capacity)
        self.error_rate = float(error_rate)
        self.m, self.k = _compute_m_k(self.capacity, self.error_rate)
        # one byte per slot
        self._counts = bytearray(self.m)

    # ------------------------------------------------------------------ hash

    def _hashes(self, item) -> list[int]:
        data = _to_bytes(item)
        digest = hashlib.sha256(data).digest()
        h1 = int.from_bytes(digest[:16], "big")
        h2 = int.from_bytes(digest[16:], "big")
        m = self.m
        return [(h1 + i * h2) % m for i in range(self.k)]

    # ------------------------------------------------------------------ ops

    def add(self, item) -> None:
        """Increment all k slots for ``item`` (saturate at 255)."""
        for pos in self._hashes(item):
            if self._counts[pos] < _COUNTER_MAX:
                self._counts[pos] += 1

    def remove(self, item) -> bool:
        """Decrement all k slots for ``item``.

        Returns ``True`` if every slot was ``> 0`` before the call
        (i.e. the item *might* have been present); ``False`` otherwise
        and no decrements happen.
        """
        positions = self._hashes(item)
        for pos in positions:
            if self._counts[pos] == 0:
                return False
        for pos in positions:
            # saturated slots are conservatively left alone — once a counter
            # has been pinned at 255 we no longer know the true count and
            # decrementing it could cause false negatives later.
            if self._counts[pos] < _COUNTER_MAX:
                self._counts[pos] -= 1
        return True

    def contains(self, item) -> bool:
        for pos in self._hashes(item):
            if self._counts[pos] == 0:
                return False
        return True

    def __contains__(self, item) -> bool:  # pragma: no cover - thin alias
        return self.contains(item)

    def add_all(self, items: Iterable) -> int:
        n = 0
        for it in items:
            self.add(it)
            n += 1
        return n

    # ---------------------------------------------------------------- stats

    def bits_set(self) -> int:
        """Return the number of slots with a non-zero counter."""
        return sum(1 for c in self._counts if c)

    def clear(self) -> None:
        for i in range(len(self._counts)):
            self._counts[i] = 0

    def __repr__(self) -> str:  # pragma: no cover - debug
        return (
            f"CountingBloomFilter(capacity={self.capacity}, "
            f"error_rate={self.error_rate}, m={self.m}, k={self.k}, "
            f"slots_used={self.bits_set()})"
        )
