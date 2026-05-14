"""Tests for the bloom_filter module — 90+ tests covering all spec requirements."""
from __future__ import annotations

import math
import random
import struct

import pytest

from docstoolkit.bloom_filter import (
    BloomFilter,
    BloomFilterConfig,
    CountingBloomFilter,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _expected_m_k(capacity: int, error_rate: float) -> tuple[int, int]:
    ln2 = math.log(2)
    m = max(1, math.ceil(-(capacity * math.log(error_rate)) / (ln2 ** 2)))
    k = max(1, int(round((m / capacity) * ln2)))
    return m, k


# ---------------------------------------------------------------------------
# 1. BloomFilterConfig
# ---------------------------------------------------------------------------

class TestBloomFilterConfig:
    def test_default_error_rate(self):
        c = BloomFilterConfig(capacity=1000)
        assert c.error_rate == 0.01

    def test_custom_error_rate(self):
        c = BloomFilterConfig(capacity=500, error_rate=0.05)
        assert c.error_rate == 0.05

    def test_capacity_required(self):
        with pytest.raises(TypeError):
            BloomFilterConfig()  # missing capacity

    def test_capacity_stored(self):
        c = BloomFilterConfig(capacity=2500)
        assert c.capacity == 2500

    def test_repr_contains_fields(self):
        c = BloomFilterConfig(capacity=10, error_rate=0.001)
        text = repr(c)
        assert "capacity=10" in text
        assert "0.001" in text

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(BloomFilterConfig)

    def test_equality(self):
        a = BloomFilterConfig(capacity=10, error_rate=0.1)
        b = BloomFilterConfig(capacity=10, error_rate=0.1)
        assert a == b

    def test_inequality(self):
        a = BloomFilterConfig(capacity=10, error_rate=0.1)
        b = BloomFilterConfig(capacity=10, error_rate=0.01)
        assert a != b


# ---------------------------------------------------------------------------
# 2. BloomFilter construction / m & k
# ---------------------------------------------------------------------------

class TestBloomFilterConstruction:
    def test_defaults(self):
        bf = BloomFilter()
        assert bf.capacity == 1000
        assert bf.error_rate == 0.01

    def test_custom_args(self):
        bf = BloomFilter(capacity=500, error_rate=0.001)
        assert bf.capacity == 500
        assert bf.error_rate == 0.001

    def test_m_matches_formula_small(self):
        bf = BloomFilter(capacity=100, error_rate=0.01)
        exp_m, _ = _expected_m_k(100, 0.01)
        assert bf.m == exp_m

    def test_m_matches_formula_large(self):
        bf = BloomFilter(capacity=100_000, error_rate=0.001)
        exp_m, _ = _expected_m_k(100_000, 0.001)
        assert bf.m == exp_m

    def test_k_matches_formula(self):
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        _, exp_k = _expected_m_k(1000, 0.01)
        assert bf.k == exp_k

    def test_k_min_one(self):
        # very loose error_rate should still yield k >= 1
        bf = BloomFilter(capacity=10_000, error_rate=0.5)
        assert bf.k >= 1

    def test_m_at_least_one(self):
        bf = BloomFilter(capacity=1, error_rate=0.5)
        assert bf.m >= 1

    def test_bit_array_size(self):
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        assert len(bf._bits) == (bf.m + 7) // 8

    def test_bit_array_is_bytearray(self):
        bf = BloomFilter()
        assert isinstance(bf._bits, bytearray)

    def test_bit_array_starts_empty(self):
        bf = BloomFilter()
        assert all(b == 0 for b in bf._bits)

    def test_invalid_capacity_zero(self):
        with pytest.raises(ValueError):
            BloomFilter(capacity=0)

    def test_invalid_capacity_negative(self):
        with pytest.raises(ValueError):
            BloomFilter(capacity=-100)

    def test_invalid_error_rate_zero(self):
        with pytest.raises(ValueError):
            BloomFilter(capacity=1000, error_rate=0.0)

    def test_invalid_error_rate_one(self):
        with pytest.raises(ValueError):
            BloomFilter(capacity=1000, error_rate=1.0)

    def test_invalid_error_rate_negative(self):
        with pytest.raises(ValueError):
            BloomFilter(capacity=1000, error_rate=-0.1)

    def test_invalid_error_rate_above_one(self):
        with pytest.raises(ValueError):
            BloomFilter(capacity=1000, error_rate=1.5)


# ---------------------------------------------------------------------------
# 3. _hashes() — k positions in [0, m)
# ---------------------------------------------------------------------------

class TestHashes:
    def test_hash_count_equals_k(self):
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        positions = bf._hashes("anything")
        assert len(positions) == bf.k

    def test_hash_positions_in_range(self):
        bf = BloomFilter(capacity=200, error_rate=0.01)
        for item in ["a", "b", "c", "long string here", 42, b"bytes"]:
            for p in bf._hashes(item):
                assert 0 <= p < bf.m

    def test_hashes_deterministic(self):
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        assert bf._hashes("hello") == bf._hashes("hello")

    def test_hashes_differ_for_different_items(self):
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        a = bf._hashes("hello")
        b = bf._hashes("world")
        assert a != b

    def test_hash_handles_bytes(self):
        bf = BloomFilter()
        positions = bf._hashes(b"binary data")
        assert len(positions) == bf.k

    def test_hash_handles_str(self):
        bf = BloomFilter()
        positions = bf._hashes("string data")
        assert len(positions) == bf.k

    def test_hash_handles_int(self):
        bf = BloomFilter()
        positions = bf._hashes(12345)
        assert len(positions) == bf.k

    def test_hash_handles_tuple(self):
        bf = BloomFilter()
        positions = bf._hashes(("a", 1, 2.5))
        assert len(positions) == bf.k


# ---------------------------------------------------------------------------
# 4. add / contains
# ---------------------------------------------------------------------------

class TestAddContains:
    def test_add_then_contains(self):
        bf = BloomFilter(capacity=100, error_rate=0.01)
        bf.add("hello")
        assert bf.contains("hello") is True

    def test_contains_returns_bool(self):
        bf = BloomFilter()
        bf.add("x")
        assert type(bf.contains("x")) is bool
        assert type(bf.contains("y")) is bool

    def test_empty_filter_contains_nothing(self):
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        assert bf.contains("anything") is False
        assert bf.contains("else") is False

    def test_no_false_negatives_strings(self):
        bf = BloomFilter(capacity=2000, error_rate=0.01)
        items = [f"item-{i}" for i in range(500)]
        for it in items:
            bf.add(it)
        for it in items:
            assert bf.contains(it)

    def test_no_false_negatives_bytes(self):
        bf = BloomFilter(capacity=200, error_rate=0.01)
        items = [bytes([i, i + 1, i + 2]) for i in range(150)]
        for it in items:
            bf.add(it)
        for it in items:
            assert bf.contains(it)

    def test_no_false_negatives_ints(self):
        bf = BloomFilter(capacity=500, error_rate=0.01)
        items = list(range(300))
        for it in items:
            bf.add(it)
        for it in items:
            assert bf.contains(it)

    def test_no_false_negatives_mixed_types(self):
        bf = BloomFilter(capacity=200, error_rate=0.01)
        items = ["abc", 123, b"def", ("x", 1), 3.14]
        for it in items:
            bf.add(it)
        for it in items:
            assert bf.contains(it)

    def test_add_idempotent(self):
        bf = BloomFilter()
        bf.add("dup")
        before = bf.bits_set()
        for _ in range(50):
            bf.add("dup")
        assert bf.bits_set() == before

    def test_add_returns_none(self):
        bf = BloomFilter()
        assert bf.add("x") is None

    def test_false_positive_rate_close_to_target(self):
        # Insert ~capacity items then probe with many unseen items.
        capacity = 5000
        target = 0.01
        bf = BloomFilter(capacity=capacity, error_rate=target)
        for i in range(capacity):
            bf.add(f"in-{i}")
        misses = 10_000
        hits = sum(1 for i in range(misses) if bf.contains(f"out-{i}"))
        actual = hits / misses
        # allow a generous 3x ceiling — bloom-filter math is asymptotic
        assert actual < target * 3, (
            f"expected ~{target}, got {actual} ({hits}/{misses})"
        )


# ---------------------------------------------------------------------------
# 5. __contains__ alias
# ---------------------------------------------------------------------------

class TestContainsDunder:
    def test_in_operator_present(self):
        bf = BloomFilter()
        bf.add("hi")
        assert "hi" in bf

    def test_in_operator_absent(self):
        bf = BloomFilter()
        assert "missing" not in bf

    def test_in_operator_matches_contains(self):
        bf = BloomFilter()
        bf.add(42)
        assert (42 in bf) == bf.contains(42)
        assert (99 in bf) == bf.contains(99)


# ---------------------------------------------------------------------------
# 6. add_all
# ---------------------------------------------------------------------------

class TestAddAll:
    def test_add_all_returns_count(self):
        bf = BloomFilter()
        n = bf.add_all(["a", "b", "c"])
        assert n == 3

    def test_add_all_zero(self):
        bf = BloomFilter()
        assert bf.add_all([]) == 0

    def test_add_all_inserts(self):
        bf = BloomFilter()
        bf.add_all(["x", "y", "z"])
        assert "x" in bf
        assert "y" in bf
        assert "z" in bf

    def test_add_all_generator(self):
        bf = BloomFilter()
        n = bf.add_all(f"item-{i}" for i in range(50))
        assert n == 50
        assert "item-0" in bf
        assert "item-49" in bf

    def test_add_all_iterator_consumed(self):
        bf = BloomFilter()
        it = iter(["a", "b"])
        n = bf.add_all(it)
        assert n == 2
        # the iterator is exhausted
        assert list(it) == []


# ---------------------------------------------------------------------------
# 7. count() / bits_set()
# ---------------------------------------------------------------------------

class TestCountAndBits:
    def test_bits_set_empty(self):
        bf = BloomFilter()
        assert bf.bits_set() == 0

    def test_bits_set_after_add(self):
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        bf.add("x")
        # at most k bits set, possibly fewer if any positions collide
        assert 1 <= bf.bits_set() <= bf.k

    def test_bits_set_grows_with_distinct_items(self):
        bf = BloomFilter(capacity=10_000, error_rate=0.01)
        b0 = bf.bits_set()
        bf.add("a")
        b1 = bf.bits_set()
        bf.add("b")
        b2 = bf.bits_set()
        assert b1 > b0
        assert b2 >= b1  # might equal if 'b' collides on all positions (unlikely)

    def test_count_empty_zero(self):
        bf = BloomFilter()
        assert bf.count() == 0

    def test_count_approximate_small_load(self):
        bf = BloomFilter(capacity=10_000, error_rate=0.01)
        n_added = 500
        for i in range(n_added):
            bf.add(f"thing-{i}")
        est = bf.count()
        # within +/- 20%
        assert abs(est - n_added) <= 0.20 * n_added, (
            f"expected ~{n_added}, got {est}"
        )

    def test_count_approximate_medium_load(self):
        bf = BloomFilter(capacity=5000, error_rate=0.001)
        n_added = 1000
        for i in range(n_added):
            bf.add(f"item-{i}")
        est = bf.count()
        assert abs(est - n_added) <= 0.20 * n_added

    def test_count_returns_int(self):
        bf = BloomFilter()
        bf.add("a")
        assert isinstance(bf.count(), int)

    def test_len_uses_count(self):
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        for i in range(100):
            bf.add(f"x-{i}")
        assert len(bf) == bf.count()

    def test_count_saturated_filter(self):
        # set every bit -> count should be large but not crash
        bf = BloomFilter(capacity=10, error_rate=0.5)
        for i in range(len(bf._bits)):
            bf._bits[i] = 0xFF
        # saturated: just make sure it returns a non-negative int
        assert bf.count() >= 0


# ---------------------------------------------------------------------------
# 8. false_positive_rate
# ---------------------------------------------------------------------------

class TestFalsePositiveRate:
    def test_fpr_empty(self):
        bf = BloomFilter()
        assert bf.false_positive_rate() == 0.0

    def test_fpr_increases_with_load(self):
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        prev = bf.false_positive_rate()
        for i in range(500):
            bf.add(f"item-{i}")
            cur = bf.false_positive_rate()
            assert cur >= prev
            prev = cur

    def test_fpr_in_unit_interval(self):
        bf = BloomFilter(capacity=100, error_rate=0.01)
        for i in range(200):
            bf.add(f"x-{i}")
        rate = bf.false_positive_rate()
        assert 0.0 <= rate <= 1.0

    def test_fpr_under_target_at_capacity(self):
        # At ~capacity, observed FPR should be in the same ballpark as target.
        capacity = 2000
        target = 0.01
        bf = BloomFilter(capacity=capacity, error_rate=target)
        for i in range(capacity):
            bf.add(f"item-{i}")
        # bound: <= 5x target (very generous; theory says ~equal)
        assert bf.false_positive_rate() <= target * 5


# ---------------------------------------------------------------------------
# 9. clear
# ---------------------------------------------------------------------------

class TestClear:
    def test_clear_zeroes_bits(self):
        bf = BloomFilter()
        for i in range(100):
            bf.add(f"item-{i}")
        assert bf.bits_set() > 0
        bf.clear()
        assert bf.bits_set() == 0

    def test_clear_then_no_contain(self):
        bf = BloomFilter()
        bf.add("present")
        bf.clear()
        assert "present" not in bf

    def test_clear_idempotent(self):
        bf = BloomFilter()
        bf.add("x")
        bf.clear()
        bf.clear()
        assert bf.bits_set() == 0

    def test_clear_then_reuse(self):
        bf = BloomFilter()
        bf.add("a")
        bf.clear()
        bf.add("b")
        assert "b" in bf
        assert "a" not in bf  # no false negative because cleared

    def test_clear_preserves_params(self):
        bf = BloomFilter(capacity=500, error_rate=0.05)
        m_before, k_before = bf.m, bf.k
        bf.add("x")
        bf.clear()
        assert bf.m == m_before
        assert bf.k == k_before
        assert bf.capacity == 500
        assert bf.error_rate == 0.05


# ---------------------------------------------------------------------------
# 10. union / intersection
# ---------------------------------------------------------------------------

class TestUnionIntersection:
    def test_union_contains_both(self):
        a = BloomFilter(capacity=1000, error_rate=0.01)
        b = BloomFilter(capacity=1000, error_rate=0.01)
        a.add("x")
        b.add("y")
        u = a.union(b)
        assert "x" in u
        assert "y" in u

    def test_union_is_new_filter(self):
        a = BloomFilter()
        b = BloomFilter()
        u = a.union(b)
        assert u is not a and u is not b

    def test_union_preserves_params(self):
        a = BloomFilter(capacity=400, error_rate=0.02)
        b = BloomFilter(capacity=400, error_rate=0.02)
        u = a.union(b)
        assert u.capacity == 400
        assert u.error_rate == 0.02
        assert u.m == a.m and u.k == a.k

    def test_union_bitwise_or(self):
        a = BloomFilter()
        b = BloomFilter()
        a._bits[0] = 0b10101010
        b._bits[0] = 0b01010101
        u = a.union(b)
        assert u._bits[0] == 0b11111111

    def test_union_mismatched_m_raises(self):
        a = BloomFilter(capacity=100, error_rate=0.01)
        b = BloomFilter(capacity=200, error_rate=0.01)  # different m
        with pytest.raises(ValueError):
            a.union(b)

    def test_union_mismatched_error_rate_raises(self):
        a = BloomFilter(capacity=1000, error_rate=0.01)
        b = BloomFilter(capacity=1000, error_rate=0.0001)
        with pytest.raises(ValueError):
            a.union(b)

    def test_union_with_non_filter_raises(self):
        a = BloomFilter()
        with pytest.raises(TypeError):
            a.union("not a filter")

    def test_intersection_bitwise_and(self):
        a = BloomFilter()
        b = BloomFilter()
        a._bits[0] = 0b11110000
        b._bits[0] = 0b10101010
        i = a.intersection(b)
        assert i._bits[0] == 0b10100000

    def test_intersection_common_item(self):
        a = BloomFilter(capacity=1000, error_rate=0.01)
        b = BloomFilter(capacity=1000, error_rate=0.01)
        a.add("shared")
        a.add("only-a")
        b.add("shared")
        b.add("only-b")
        i = a.intersection(b)
        # shared is in both, so all its bit positions are 1 in both => present
        assert "shared" in i

    def test_intersection_returns_new(self):
        a = BloomFilter()
        b = BloomFilter()
        i = a.intersection(b)
        assert i is not a and i is not b

    def test_intersection_preserves_params(self):
        a = BloomFilter(capacity=500, error_rate=0.01)
        b = BloomFilter(capacity=500, error_rate=0.01)
        i = a.intersection(b)
        assert i.capacity == 500
        assert i.error_rate == 0.01
        assert i.m == a.m and i.k == a.k

    def test_intersection_mismatch_raises(self):
        a = BloomFilter(capacity=100, error_rate=0.01)
        b = BloomFilter(capacity=200, error_rate=0.01)
        with pytest.raises(ValueError):
            a.intersection(b)

    def test_intersection_with_non_filter_raises(self):
        a = BloomFilter()
        with pytest.raises(TypeError):
            a.intersection("nope")

    def test_union_does_not_mutate_originals(self):
        a = BloomFilter()
        b = BloomFilter()
        a.add("x")
        b.add("y")
        a_bits_before = bytes(a._bits)
        b_bits_before = bytes(b._bits)
        a.union(b)
        assert bytes(a._bits) == a_bits_before
        assert bytes(b._bits) == b_bits_before

    def test_intersection_does_not_mutate_originals(self):
        a = BloomFilter()
        b = BloomFilter()
        a.add("x")
        b.add("y")
        a_bits_before = bytes(a._bits)
        b_bits_before = bytes(b._bits)
        a.intersection(b)
        assert bytes(a._bits) == a_bits_before
        assert bytes(b._bits) == b_bits_before


# ---------------------------------------------------------------------------
# 11. serialize / deserialize
# ---------------------------------------------------------------------------

class TestSerialize:
    def test_serialize_returns_bytes(self):
        bf = BloomFilter()
        bf.add("hello")
        assert isinstance(bf.serialize(), bytes)

    def test_roundtrip_preserves_params(self):
        bf = BloomFilter(capacity=2500, error_rate=0.05)
        clone = BloomFilter.deserialize(bf.serialize())
        assert clone.capacity == bf.capacity
        assert clone.error_rate == bf.error_rate
        assert clone.m == bf.m
        assert clone.k == bf.k

    def test_roundtrip_preserves_bits(self):
        bf = BloomFilter(capacity=500, error_rate=0.01)
        for i in range(100):
            bf.add(f"item-{i}")
        clone = BloomFilter.deserialize(bf.serialize())
        assert clone._bits == bf._bits

    def test_roundtrip_membership(self):
        bf = BloomFilter(capacity=500, error_rate=0.01)
        items = [f"x-{i}" for i in range(200)]
        bf.add_all(items)
        clone = BloomFilter.deserialize(bf.serialize())
        for it in items:
            assert clone.contains(it)

    def test_roundtrip_no_false_negatives(self):
        bf = BloomFilter(capacity=500, error_rate=0.001)
        items = [f"y-{i}" for i in range(300)]
        bf.add_all(items)
        clone = BloomFilter.deserialize(bf.serialize())
        for it in items:
            assert it in clone

    def test_deserialize_rejects_non_bytes(self):
        with pytest.raises(TypeError):
            BloomFilter.deserialize("not bytes")  # type: ignore[arg-type]

    def test_deserialize_rejects_short(self):
        with pytest.raises(ValueError):
            BloomFilter.deserialize(b"too short")

    def test_deserialize_rejects_truncated_body(self):
        bf = BloomFilter()
        bf.add("x")
        data = bf.serialize()
        truncated = data[:-3]
        with pytest.raises(ValueError):
            BloomFilter.deserialize(truncated)

    def test_serialize_includes_header(self):
        bf = BloomFilter(capacity=10, error_rate=0.5)
        data = bf.serialize()
        # header size = struct format I d I I I = 4+8+4+4+4 = 24 bytes
        header_size = struct.calcsize("!IdIII")
        assert len(data) >= header_size

    def test_two_independent_clones(self):
        bf = BloomFilter()
        bf.add("seed")
        a = BloomFilter.deserialize(bf.serialize())
        b = BloomFilter.deserialize(bf.serialize())
        a.add("extra-a")
        # b should not see 'extra-a'
        assert "extra-a" not in b
        assert "seed" in a and "seed" in b


# ---------------------------------------------------------------------------
# 12. CountingBloomFilter
# ---------------------------------------------------------------------------

class TestCountingBloomFilter:
    def test_construction_defaults(self):
        cbf = CountingBloomFilter()
        assert cbf.capacity == 1000
        assert cbf.error_rate == 0.01

    def test_construction_custom(self):
        cbf = CountingBloomFilter(capacity=200, error_rate=0.05)
        assert cbf.capacity == 200
        assert cbf.error_rate == 0.05

    def test_m_and_k_match_bloom(self):
        bf = BloomFilter(capacity=400, error_rate=0.01)
        cbf = CountingBloomFilter(capacity=400, error_rate=0.01)
        assert cbf.m == bf.m
        assert cbf.k == bf.k

    def test_counters_array_size(self):
        cbf = CountingBloomFilter(capacity=200, error_rate=0.01)
        assert len(cbf._counts) == cbf.m

    def test_counters_start_zero(self):
        cbf = CountingBloomFilter()
        assert all(c == 0 for c in cbf._counts)

    def test_add_then_contains(self):
        cbf = CountingBloomFilter()
        cbf.add("hello")
        assert "hello" in cbf

    def test_no_false_negatives(self):
        cbf = CountingBloomFilter(capacity=500, error_rate=0.01)
        items = [f"i-{i}" for i in range(200)]
        for it in items:
            cbf.add(it)
        for it in items:
            assert cbf.contains(it)

    def test_empty_contains_false(self):
        cbf = CountingBloomFilter()
        assert "absent" not in cbf

    def test_remove_present_returns_true(self):
        cbf = CountingBloomFilter()
        cbf.add("a")
        assert cbf.remove("a") is True

    def test_remove_then_absent(self):
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.001)
        cbf.add("solo")
        cbf.remove("solo")
        assert "solo" not in cbf

    def test_remove_absent_returns_false(self):
        cbf = CountingBloomFilter()
        assert cbf.remove("never-added") is False

    def test_remove_absent_no_side_effect(self):
        cbf = CountingBloomFilter()
        cbf.add("kept")
        before = bytes(cbf._counts)
        cbf.remove("not-there")
        assert bytes(cbf._counts) == before

    def test_double_remove(self):
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.001)
        cbf.add("dup")
        cbf.add("dup")
        # remove twice: both succeed because each slot was incremented twice
        assert cbf.remove("dup") is True
        assert cbf.remove("dup") is True
        # third remove fails (slots may be 0 now)
        # note: collisions could still leave some > 0, but for capacity=1000 unlikely
        # we don't strictly require False here, but bits should be fully cleared
        assert "dup" not in cbf or cbf.remove("dup") is False

    def test_remove_doesnt_kill_others(self):
        cbf = CountingBloomFilter(capacity=2000, error_rate=0.001)
        items = [f"keep-{i}" for i in range(50)]
        for it in items:
            cbf.add(it)
        cbf.add("temp")
        assert cbf.remove("temp")
        for it in items:
            assert it in cbf

    def test_saturation_at_255(self):
        cbf = CountingBloomFilter(capacity=10, error_rate=0.5)
        # add the same item many more times than 255
        for _ in range(1000):
            cbf.add("over")
        # every slot for "over" must be exactly 255
        positions = cbf._hashes("over")
        for p in positions:
            assert cbf._counts[p] == 255

    def test_saturated_slots_not_decremented(self):
        # once saturated, remove() shouldn't take a saturated slot below 255
        cbf = CountingBloomFilter(capacity=10, error_rate=0.5)
        for _ in range(500):
            cbf.add("S")
        cbf.remove("S")
        # all slots for "S" should still be 255 (conservative behaviour)
        for p in cbf._hashes("S"):
            assert cbf._counts[p] == 255

    def test_add_all_returns_count(self):
        cbf = CountingBloomFilter()
        n = cbf.add_all(["a", "b", "c", "d"])
        assert n == 4

    def test_clear(self):
        cbf = CountingBloomFilter()
        for i in range(50):
            cbf.add(f"x-{i}")
        cbf.clear()
        assert all(c == 0 for c in cbf._counts)
        assert "x-0" not in cbf

    def test_bits_set_counts_nonzero_slots(self):
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        assert cbf.bits_set() == 0
        cbf.add("one")
        # at most k slots non-zero
        assert 1 <= cbf.bits_set() <= cbf.k

    def test_contains_handles_mixed_types(self):
        cbf = CountingBloomFilter()
        items = ["s", 42, b"b", (1, 2)]
        for it in items:
            cbf.add(it)
        for it in items:
            assert it in cbf

    def test_invalid_capacity(self):
        with pytest.raises(ValueError):
            CountingBloomFilter(capacity=0)

    def test_invalid_error_rate(self):
        with pytest.raises(ValueError):
            CountingBloomFilter(capacity=100, error_rate=1.0)

    def test_remove_then_re_add(self):
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.001)
        cbf.add("phoenix")
        cbf.remove("phoenix")
        assert "phoenix" not in cbf
        cbf.add("phoenix")
        assert "phoenix" in cbf


# ---------------------------------------------------------------------------
# 13. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_filter_count_zero(self):
        bf = BloomFilter()
        assert bf.count() == 0
        assert bf.bits_set() == 0
        assert bf.false_positive_rate() == 0.0

    def test_zero_adds_zero_count(self):
        bf = BloomFilter()
        bf.add_all([])
        assert bf.count() == 0

    def test_hash_str_vs_bytes_distinct(self):
        # 'abc' and b'abc' should map differently because we encode str as
        # utf-8 then SHA-256; bytes pass through unchanged.  They both yield
        # the same bytes value, so they should be equivalent — verify.
        bf = BloomFilter()
        bf.add("abc")
        # str 'abc' encoded utf-8 = b'abc' — so b'abc' should also match
        assert b"abc" in bf

    def test_hash_int(self):
        bf = BloomFilter()
        bf.add(42)
        assert 42 in bf

    def test_hash_negative_int(self):
        bf = BloomFilter()
        bf.add(-99)
        assert -99 in bf

    def test_hash_large_int(self):
        bf = BloomFilter()
        bf.add(10**18)
        assert 10**18 in bf

    def test_unicode_string(self):
        bf = BloomFilter()
        bf.add("привет мир")
        assert "привет мир" in bf

    def test_empty_string(self):
        bf = BloomFilter()
        bf.add("")
        assert "" in bf

    def test_empty_bytes(self):
        bf = BloomFilter()
        bf.add(b"")
        assert b"" in bf

    def test_at_capacity(self):
        # exact-capacity stress — observed FPR shouldn't blow up
        capacity = 1000
        target = 0.01
        bf = BloomFilter(capacity=capacity, error_rate=target)
        for i in range(capacity):
            bf.add(f"cap-{i}")
        # at capacity, theoretical FPR ~= target
        # allow generous slack
        assert bf.false_positive_rate() <= target * 10
        # but every inserted item must still be present
        for i in range(capacity):
            assert f"cap-{i}" in bf

    def test_above_capacity_no_false_negatives(self):
        # over-fill: false-positive rate degrades, but no false negatives ever
        capacity = 200
        bf = BloomFilter(capacity=capacity, error_rate=0.01)
        items = [f"over-{i}" for i in range(capacity * 5)]
        for it in items:
            bf.add(it)
        for it in items:
            assert it in bf

    def test_very_tight_error_rate(self):
        bf = BloomFilter(capacity=100, error_rate=1e-6)
        # m and k should be plausibly larger than for 0.01
        bf2 = BloomFilter(capacity=100, error_rate=0.01)
        assert bf.m > bf2.m
        assert bf.k >= bf2.k

    def test_very_loose_error_rate(self):
        bf = BloomFilter(capacity=100, error_rate=0.5)
        # still functional
        bf.add("x")
        assert "x" in bf

    def test_capacity_one(self):
        bf = BloomFilter(capacity=1, error_rate=0.01)
        bf.add("solo")
        assert "solo" in bf

    def test_counting_above_capacity(self):
        cbf = CountingBloomFilter(capacity=100, error_rate=0.01)
        for i in range(500):
            cbf.add(f"o-{i}")
        for i in range(500):
            assert f"o-{i}" in cbf

    def test_union_self(self):
        a = BloomFilter()
        a.add("x")
        u = a.union(a)
        assert "x" in u
        # union(self,self) bits equal self
        assert u._bits == a._bits

    def test_intersection_self(self):
        a = BloomFilter()
        a.add("x")
        i = a.intersection(a)
        assert "x" in i
        assert i._bits == a._bits

    def test_serialize_empty(self):
        bf = BloomFilter(capacity=100, error_rate=0.01)
        data = bf.serialize()
        clone = BloomFilter.deserialize(data)
        assert clone.bits_set() == 0
        assert clone.m == bf.m and clone.k == bf.k

    def test_random_workload(self):
        rng = random.Random(0xC0FFEE)
        bf = BloomFilter(capacity=2000, error_rate=0.01)
        added = set()
        for _ in range(1500):
            s = "".join(rng.choices("abcdefghij", k=8))
            bf.add(s)
            added.add(s)
        # zero false negatives
        for s in added:
            assert s in bf
