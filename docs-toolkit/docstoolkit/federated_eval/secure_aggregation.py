"""Phase VI.2 — Additive-share secure aggregation.

Implements a semi-honest secure-sum protocol so a central aggregator can
compute Σx_i across N nodes without ever seeing any individual x_i.
Each node:
  1. Generates N pairwise PRNG-derived masks; the mask sum across all
     nodes is zero by construction.
  2. Sends value + own_masks to the aggregator.
  3. Aggregator sums; pairwise masks cancel out; result = Σx_i.

This is the protocol described in Bonawitz et al. (2017) "Practical
Secure Aggregation for Privacy-Preserving Machine Learning", simplified:
- No dropout-handling (assumes all nodes complete)
- No public-key crypto (relies on a pre-shared seed-exchange step)
- Stdlib-only

For production deployments use libsodium / PySyft / TFF; this module
is sufficient to demonstrate the federation flow and ground the integration
tests.
"""
from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, field


@dataclass(frozen=True)
class MaskedShare:
    """One node's masked contribution.

    `masked_value = value + sum(mask(node_id, other_id) for other_id in peers
                                where node_id < other_id)
                          - sum(mask(other_id, node_id) for other_id in peers
                                where other_id < node_id)`

    The aggregator sums all `masked_value` across nodes; for every
    pair (i, j) the +mask(i,j) from node i cancels the -mask(i,j) from
    node j.
    """
    node_id: str
    masked_value: float


def _pair_mask(seed: bytes, peer_a: str, peer_b: str,
               salt: str = "") -> float:
    """Deterministic shared mask for the canonical pair (sorted)."""
    lo, hi = (peer_a, peer_b) if peer_a < peer_b else (peer_b, peer_a)
    h = hashlib.blake2b(digest_size=8)
    h.update(seed)
    h.update(salt.encode("utf-8"))
    h.update(lo.encode("utf-8"))
    h.update(b"\x00")
    h.update(hi.encode("utf-8"))
    # Map 8-byte hash to a float in [-1, +1]; large enough to mask
    # any [0, 1] metric value securely against direct inversion.
    (n,) = struct.unpack("<Q", h.digest())
    return ((n / (1 << 64)) - 0.5) * 2.0


def mask_share(node_id: str,
               value: float,
               peers: list[str],
               seed: bytes,
               salt: str = "") -> MaskedShare:
    """Compute one node's masked share of `value`.

    `seed` is the pre-shared secret common to all nodes. Different `salt`
    values (e.g. metric name) re-randomise the masks per metric so the
    same seed can be reused across rounds.
    """
    masked = float(value)
    for peer in peers:
        if peer == node_id:
            continue
        m = _pair_mask(seed, node_id, peer, salt=salt)
        # Convention: node with smaller id ADDS, larger id SUBTRACTS.
        if node_id < peer:
            masked += m
        else:
            masked -= m
    return MaskedShare(node_id=node_id, masked_value=masked)


def aggregate_shares(shares: list[MaskedShare]) -> float:
    """Sum masked shares; pairwise masks cancel.

    The aggregator never sees the raw `value`; only the sum is recoverable.
    """
    return sum(s.masked_value for s in shares)


def secure_average(node_values: dict[str, float],
                   seed: bytes,
                   salt: str = "") -> float:
    """End-to-end helper for the typical case: aggregate over `node_values`.

    Simulates the full N-node protocol in one process so tests can verify
    correctness without spinning real services.
    """
    peers = list(node_values)
    if not peers:
        return 0.0
    shares = [
        mask_share(node_id, value, peers, seed=seed, salt=salt)
        for node_id, value in node_values.items()
    ]
    total = aggregate_shares(shares)
    return total / len(peers)


__all__ = [
    "MaskedShare",
    "mask_share",
    "aggregate_shares",
    "secure_average",
]
