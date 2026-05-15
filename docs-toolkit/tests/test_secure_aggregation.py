"""Phase VI.2 — additive-share secure aggregation tests.

Verifies the protocol invariant: aggregator-side sum recovers Σx_i
without ever observing individual x_i.
"""
from __future__ import annotations

import math
import pytest

from docstoolkit.federated_eval.secure_aggregation import (
    MaskedShare, mask_share, aggregate_shares, secure_average,
)


SEED = b"shared-secret-bytes-for-tests"


def test_pairwise_masks_cancel_in_sum():
    """Two nodes: their masks differ by sign so the sum equals raw total."""
    a = mask_share("A", 0.7, peers=["A", "B"], seed=SEED)
    b = mask_share("B", 0.3, peers=["A", "B"], seed=SEED)
    total = aggregate_shares([a, b])
    assert total == pytest.approx(1.0, abs=1e-10)


def test_single_node_no_peers_returns_value():
    a = mask_share("A", 0.42, peers=["A"], seed=SEED)
    assert a.masked_value == pytest.approx(0.42)


def test_three_node_aggregation():
    values = {"A": 0.1, "B": 0.2, "C": 0.3}
    peers = list(values)
    shares = [
        mask_share(nid, v, peers, seed=SEED)
        for nid, v in values.items()
    ]
    total = aggregate_shares(shares)
    assert total == pytest.approx(0.6, abs=1e-10)


def test_masked_value_hides_raw_value():
    """No individual share should match its raw value (with overwhelming probability)."""
    values = {"A": 0.1, "B": 0.2, "C": 0.3}
    peers = list(values)
    for nid, v in values.items():
        share = mask_share(nid, v, peers, seed=SEED)
        # The mask shifts the value by at least 1e-6 in absolute terms,
        # so equality would be vanishingly unlikely if masks were
        # implemented correctly.
        assert share.masked_value != v


def test_different_salt_yields_different_masks():
    a1 = mask_share("A", 0.5, peers=["A", "B"], seed=SEED, salt="precision")
    a2 = mask_share("A", 0.5, peers=["A", "B"], seed=SEED, salt="recall")
    assert a1.masked_value != a2.masked_value


def test_secure_average_three_nodes():
    avg = secure_average({"A": 0.6, "B": 0.8, "C": 1.0}, seed=SEED)
    assert avg == pytest.approx(0.8, abs=1e-10)


def test_secure_average_empty_returns_zero():
    assert secure_average({}, seed=SEED) == 0.0


def test_masked_share_dataclass_is_immutable():
    s = MaskedShare(node_id="X", masked_value=1.0)
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        s.node_id = "Y"


def test_order_independence():
    """Aggregation must be commutative — different submission orders give the same total."""
    values = {"A": 0.1, "B": 0.5, "C": 0.4}
    peers = list(values)
    shares = [mask_share(n, v, peers, seed=SEED) for n, v in values.items()]
    total1 = aggregate_shares(shares)
    total2 = aggregate_shares(list(reversed(shares)))
    assert total1 == pytest.approx(total2, abs=1e-10)
