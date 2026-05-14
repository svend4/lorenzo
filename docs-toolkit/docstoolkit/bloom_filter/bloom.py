"""Classic Bloom filter — probabilistic membership test.

Given a target capacity (``n``) and a desired false-positive rate (``p``),
the filter sizes its bit array (``m``) and number of hash functions (``k``)
using the standard formulas:

    m = -(n * ln(p)) / (ln(2)^2)
    k = (m / n) * ln(2)

Hash positions are generated via Kirsch-Mitzenmacher double-hashing,
seeded with SHA-256 — so we get k independent positions from just two
real hashes.  Pure stdlib only.
"""
from __future__ import annotations

import hashlib
import math
import struct
from dataclasses import dataclass
from typing import Iterable


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class BloomFilterConfig:
    """Configuration for a :class:`BloomFilter`.

    :param capacity: expected number of items the filter should hold.
    :param error_rate: target false-positive probability (``0 < p < 1``).
    """
    capacity: int
    error_rate: float = 0.01


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_bytes(item) -> bytes:
    """Coerce an item to bytes for hashing.

    Bytes pass through unchanged; str is encoded as UTF-8; everything else
    goes through ``repr()`` (this gives sensible, stable hashes for ints,
    tuples, etc.).
    """
    if isinstance(item, bytes):
        return item
    if isinstance(item, bytearray):
        return bytes(item)
    if isinstance(item, str):
        return item.encode("utf-8")
    return repr(item).encode("utf-8")


def _compute_m_k(capacity: int, error_rate: float) -> tuple[int, int]:
    """Return ``(m, k)`` for the given capacity/error_rate."""
    if capacity <= 0:
        raise ValueError("capacity must be > 0")
    if not (0.0 < error_rate < 1.0):
        raise ValueError("error_rate must be in (0, 1)")
    ln2 = math.log(2)
    m = -(capacity * math.log(error_rate)) / (ln2 ** 2)
    m = max(1, math.ceil(m))
    k = (m / capacity) * ln2
    k = max(1, int(round(k)))
    return m, k


# ---------------------------------------------------------------------------
# Bloom filter
# ---------------------------------------------------------------------------

class BloomFilter:
    """A classic Bloom filter.

    Backed by ``bytearray((m + 7) // 8)``; uses double-hashing built on
    SHA-256 so the number of *real* hash computations stays constant
    regardless of ``k``.
    """

    # struct format for serialise header: capacity, error_rate, m, k, byte_len
    _HEADER = struct.Struct("!IdIII")

    def __init__(self, capacity: int = 1000, error_rate: float = 0.01) -> None:
        self.capacity = int(capacity)
        self.error_rate = float(error_rate)
        self.m, self.k = _compute_m_k(self.capacity, self.error_rate)
        self._bits = bytearray((self.m + 7) // 8)

    # ------------------------------------------------------------------ hash

    def _hashes(self, item) -> list[int]:
        """Return ``k`` bit positions in ``[0, m)`` using double-hashing."""
        data = _to_bytes(item)
        digest = hashlib.sha256(data).digest()
        # split the 32-byte digest into two 16-byte halves -> two 128-bit hashes
        h1 = int.from_bytes(digest[:16], "big")
        h2 = int.from_bytes(digest[16:], "big")
        m = self.m
        out = []
        for i in range(self.k):
            out.append((h1 + i * h2) % m)
        return out

    # ------------------------------------------------------------------ ops

    def _set_bit(self, pos: int) -> None:
        self._bits[pos >> 3] |= 1 << (pos & 7)

    def _get_bit(self, pos: int) -> bool:
        return bool(self._bits[pos >> 3] & (1 << (pos & 7)))

    def add(self, item) -> None:
        """Insert ``item`` into the filter."""
        for pos in self._hashes(item):
            self._set_bit(pos)

    def contains(self, item) -> bool:
        """Return ``True`` if ``item`` is *probably* present.

        False positives possible; false negatives are not.
        """
        for pos in self._hashes(item):
            if not self._get_bit(pos):
                return False
        return True

    def __contains__(self, item) -> bool:  # pragma: no cover - thin alias
        return self.contains(item)

    def add_all(self, items: Iterable) -> int:
        """Add every item from ``items`` and return how many were added."""
        n = 0
        for it in items:
            self.add(it)
            n += 1
        return n

    # ---------------------------------------------------------------- stats

    def bits_set(self) -> int:
        """Return the number of bits currently set to 1."""
        # Python ints expose .bit_count() on 3.10+
        return sum(b.bit_count() for b in self._bits)

    def count(self) -> int:
        """Approximate count of distinct items added.

        Uses the Swamidass-Baldi estimator::

            n* = -(m / k) * ln(1 - X / m)

        where ``X`` is :meth:`bits_set`.  Returns 0 for an empty filter and
        clamps the log argument to avoid division by zero when the filter
        is saturated.
        """
        x = self.bits_set()
        if x == 0:
            return 0
        if x >= self.m:
            # fully saturated — return a very large estimate
            x = self.m - 1
        ratio = 1.0 - (x / self.m)
        if ratio <= 0.0:
            return self.m  # saturated
        est = -(self.m / self.k) * math.log(ratio)
        return int(round(est))

    def false_positive_rate(self) -> float:
        """Current observed false-positive rate ``(bits_set/m)^k``."""
        if self.m == 0:
            return 0.0
        return (self.bits_set() / self.m) ** self.k

    # --------------------------------------------------------------- mutate

    def clear(self) -> None:
        """Reset the bit array to all zeros."""
        for i in range(len(self._bits)):
            self._bits[i] = 0

    # ------------------------------------------------------------- combine

    def _check_compatible(self, other: "BloomFilter") -> None:
        if not isinstance(other, BloomFilter):
            raise TypeError("other must be a BloomFilter")
        if self.m != other.m or self.k != other.k:
            raise ValueError(
                "BloomFilters must share m and k to combine "
                f"(self: m={self.m}, k={self.k}; other: m={other.m}, k={other.k})"
            )

    def union(self, other: "BloomFilter") -> "BloomFilter":
        """Return a new filter containing the union of ``self`` and ``other``."""
        self._check_compatible(other)
        out = BloomFilter(capacity=self.capacity, error_rate=self.error_rate)
        # combine via bitwise OR
        for i in range(len(self._bits)):
            out._bits[i] = self._bits[i] | other._bits[i]
        return out

    def intersection(self, other: "BloomFilter") -> "BloomFilter":
        """Return an approximate intersection filter (bitwise AND)."""
        self._check_compatible(other)
        out = BloomFilter(capacity=self.capacity, error_rate=self.error_rate)
        for i in range(len(self._bits)):
            out._bits[i] = self._bits[i] & other._bits[i]
        return out

    # ------------------------------------------------------------ serialise

    def serialize(self) -> bytes:
        """Serialise to a self-describing byte string."""
        header = self._HEADER.pack(
            self.capacity,
            self.error_rate,
            self.m,
            self.k,
            len(self._bits),
        )
        return header + bytes(self._bits)

    @classmethod
    def deserialize(cls, data: bytes) -> "BloomFilter":
        """Inverse of :meth:`serialize`."""
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        header_size = cls._HEADER.size
        if len(data) < header_size:
            raise ValueError("data is too short to contain a header")
        capacity, error_rate, m, k, byte_len = cls._HEADER.unpack(data[:header_size])
        body = data[header_size:header_size + byte_len]
        if len(body) != byte_len:
            raise ValueError("data truncated: bit array shorter than declared")
        bf = cls.__new__(cls)
        bf.capacity = capacity
        bf.error_rate = error_rate
        bf.m = m
        bf.k = k
        bf._bits = bytearray(body)
        return bf

    # ------------------------------------------------------------ dunder

    def __len__(self) -> int:
        return self.count()

    def __repr__(self) -> str:  # pragma: no cover - debug
        return (
            f"BloomFilter(capacity={self.capacity}, error_rate={self.error_rate}, "
            f"m={self.m}, k={self.k}, bits_set={self.bits_set()})"
        )
