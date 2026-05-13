"""Tests for the E13 Request Deduplication module.

Run with:
    cd /home/user/lorenzo/docs-toolkit && python -m pytest tests/test_dedup.py -q
"""
import hashlib
import time
import uuid

import pytest

from docstoolkit.dedup import (
    DeduplicationConfig,
    DeduplicationKey,
    DeduplicationResult,
    DeduplicationStrategy,
    DedupEntry,
    DedupStore,
    RequestDeduplicator,
    compute_key,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fresh_store() -> DedupStore:
    return DedupStore()  # in-memory


def _fresh_dedup(strategy=DeduplicationStrategy.NORMALIZED, ttl=300.0) -> RequestDeduplicator:
    cfg = DeduplicationConfig(strategy=strategy, ttl_seconds=ttl)
    return RequestDeduplicator(config=cfg)


def _make_entry(key_hash="abc123", request_id=None, ttl=300.0, created_ts=None, result=None):
    return DedupEntry(
        request_id=request_id or str(uuid.uuid4()),
        key_hash=key_hash,
        strategy=DeduplicationStrategy.NORMALIZED,
        result=result,
        created_ts=created_ts if created_ts is not None else time.time(),
        ttl_seconds=ttl,
    )


# ===========================================================================
# Section 1 — compute_key / DeduplicationKey
# ===========================================================================

class TestComputeKeyBasics:
    def test_returns_deduplication_key(self):
        dk = compute_key("hello", DeduplicationStrategy.EXACT)
        assert isinstance(dk, DeduplicationKey)

    def test_key_hash_is_16_hex_chars(self):
        dk = compute_key("hello", DeduplicationStrategy.EXACT)
        assert len(dk.key_hash) == 16
        int(dk.key_hash, 16)  # must be valid hex

    def test_request_id_defaults_to_uuid4(self):
        dk = compute_key("hello", DeduplicationStrategy.EXACT)
        uuid.UUID(dk.request_id, version=4)

    def test_request_id_respected_when_provided(self):
        rid = "my-custom-id"
        dk = compute_key("hello", DeduplicationStrategy.EXACT, request_id=rid)
        assert dk.request_id == rid

    def test_strategy_stored(self):
        dk = compute_key("x", DeduplicationStrategy.SEMANTIC)
        assert dk.strategy == DeduplicationStrategy.SEMANTIC

    def test_created_ts_is_recent(self):
        before = time.time()
        dk = compute_key("x", DeduplicationStrategy.EXACT)
        after = time.time()
        assert before <= dk.created_ts <= after


class TestExactStrategy:
    def test_same_payload_same_hash(self):
        h1 = compute_key("Hello World", DeduplicationStrategy.EXACT).key_hash
        h2 = compute_key("Hello World", DeduplicationStrategy.EXACT).key_hash
        assert h1 == h2

    def test_different_case_different_hash(self):
        h1 = compute_key("Hello", DeduplicationStrategy.EXACT).key_hash
        h2 = compute_key("hello", DeduplicationStrategy.EXACT).key_hash
        assert h1 != h2

    def test_extra_whitespace_different_hash(self):
        h1 = compute_key("hello world", DeduplicationStrategy.EXACT).key_hash
        h2 = compute_key("hello  world", DeduplicationStrategy.EXACT).key_hash
        assert h1 != h2

    def test_hash_is_sha256_prefix(self):
        payload = "test-payload"
        expected = hashlib.sha256(payload.encode()).hexdigest()[:16]
        dk = compute_key(payload, DeduplicationStrategy.EXACT)
        assert dk.key_hash == expected


class TestNormalizedStrategy:
    def test_same_payload_same_hash(self):
        h1 = compute_key("Hello World", DeduplicationStrategy.NORMALIZED).key_hash
        h2 = compute_key("Hello World", DeduplicationStrategy.NORMALIZED).key_hash
        assert h1 == h2

    def test_case_insensitive(self):
        h1 = compute_key("Hello World", DeduplicationStrategy.NORMALIZED).key_hash
        h2 = compute_key("HELLO WORLD", DeduplicationStrategy.NORMALIZED).key_hash
        assert h1 == h2

    def test_whitespace_collapsed(self):
        h1 = compute_key("hello world", DeduplicationStrategy.NORMALIZED).key_hash
        h2 = compute_key("hello   world", DeduplicationStrategy.NORMALIZED).key_hash
        assert h1 == h2

    def test_leading_trailing_stripped(self):
        h1 = compute_key("  hello world  ", DeduplicationStrategy.NORMALIZED).key_hash
        h2 = compute_key("hello world", DeduplicationStrategy.NORMALIZED).key_hash
        assert h1 == h2

    def test_different_content_different_hash(self):
        h1 = compute_key("foo", DeduplicationStrategy.NORMALIZED).key_hash
        h2 = compute_key("bar", DeduplicationStrategy.NORMALIZED).key_hash
        assert h1 != h2


class TestSemanticStrategy:
    def test_same_prefix_same_hash(self):
        base = "a" * 100
        h1 = compute_key(base + "extra1", DeduplicationStrategy.SEMANTIC).key_hash
        h2 = compute_key(base + "extra2", DeduplicationStrategy.SEMANTIC).key_hash
        assert h1 == h2

    def test_short_payload_same_as_exact_100(self):
        payload = "short"
        h_sem = compute_key(payload, DeduplicationStrategy.SEMANTIC).key_hash
        h_norm = compute_key(payload, DeduplicationStrategy.NORMALIZED).key_hash
        # For short payloads (< 100 chars), SEMANTIC == NORMALIZED
        assert h_sem == h_norm

    def test_truncation_at_100_chars(self):
        # Two payloads that differ only after position 100 should share hash
        prefix = "x" * 100
        h1 = compute_key(prefix + "aaa", DeduplicationStrategy.SEMANTIC).key_hash
        h2 = compute_key(prefix + "bbb", DeduplicationStrategy.SEMANTIC).key_hash
        assert h1 == h2

    def test_different_prefix_different_hash(self):
        h1 = compute_key("alpha" + "z" * 95, DeduplicationStrategy.SEMANTIC).key_hash
        h2 = compute_key("beta" + "z" * 96, DeduplicationStrategy.SEMANTIC).key_hash
        assert h1 != h2

    def test_semantic_is_case_insensitive(self):
        h1 = compute_key("HELLO", DeduplicationStrategy.SEMANTIC).key_hash
        h2 = compute_key("hello", DeduplicationStrategy.SEMANTIC).key_hash
        assert h1 == h2


# ===========================================================================
# Section 2 — DedupStore
# ===========================================================================

class TestDedupStorePut:
    def test_put_and_get(self):
        store = _fresh_store()
        entry = _make_entry(key_hash="aabbcc")
        store.put(entry)
        got = store.get("aabbcc")
        assert got is not None
        assert got.request_id == entry.request_id

    def test_put_replaces_existing(self):
        store = _fresh_store()
        e1 = _make_entry(key_hash="k1", request_id="req-1")
        e2 = _make_entry(key_hash="k1", request_id="req-2")
        store.put(e1)
        store.put(e2)
        got = store.get("k1")
        assert got.request_id == "req-2"

    def test_get_missing_returns_none(self):
        store = _fresh_store()
        assert store.get("nonexistent") is None


class TestDedupStoreExpiry:
    def test_get_returns_none_when_expired(self):
        store = _fresh_store()
        past_ts = time.time() - 400  # created 400 s ago
        entry = _make_entry(key_hash="old", created_ts=past_ts, ttl=300.0)
        store.put(entry)
        # Even without explicit eviction, get() should return None
        assert store.get("old") is None

    def test_get_returns_entry_within_ttl(self):
        store = _fresh_store()
        entry = _make_entry(key_hash="live", ttl=300.0)
        store.put(entry)
        assert store.get("live") is not None

    def test_ttl_zero_means_immortal(self):
        store = _fresh_store()
        past_ts = time.time() - 999_999
        entry = _make_entry(key_hash="immortal", created_ts=past_ts, ttl=0.0)
        store.put(entry)
        assert store.get("immortal") is not None

    def test_is_duplicate_true_for_live_entry(self):
        store = _fresh_store()
        store.put(_make_entry(key_hash="dup1"))
        assert store.is_duplicate("dup1") is True

    def test_is_duplicate_false_for_expired(self):
        store = _fresh_store()
        past_ts = time.time() - 1000
        store.put(_make_entry(key_hash="exp1", created_ts=past_ts, ttl=300.0))
        assert store.is_duplicate("exp1") is False

    def test_is_duplicate_false_for_missing(self):
        store = _fresh_store()
        assert store.is_duplicate("no-such-key") is False


class TestDedupStoreEviction:
    def test_evict_removes_expired(self):
        store = _fresh_store()
        past_ts = time.time() - 400
        store.put(_make_entry(key_hash="old1", created_ts=past_ts, ttl=300.0))
        store.put(_make_entry(key_hash="old2", created_ts=past_ts, ttl=300.0))
        removed = store.evict_expired()
        assert removed == 2

    def test_evict_leaves_live_entries(self):
        store = _fresh_store()
        store.put(_make_entry(key_hash="live1", ttl=300.0))
        removed = store.evict_expired()
        assert removed == 0
        assert store.get("live1") is not None

    def test_evict_uses_now_param(self):
        store = _fresh_store()
        created_ts = 1_000_000.0
        store.put(_make_entry(key_hash="t1", created_ts=created_ts, ttl=300.0))
        # now just before expiry — should NOT evict
        removed = store.evict_expired(now=created_ts + 299)
        assert removed == 0
        # now just after expiry — should evict
        removed = store.evict_expired(now=created_ts + 301)
        assert removed == 1

    def test_evict_immortal_entries_not_removed(self):
        store = _fresh_store()
        past_ts = time.time() - 999_999
        store.put(_make_entry(key_hash="immortal", created_ts=past_ts, ttl=0.0))
        removed = store.evict_expired()
        assert removed == 0

    def test_evict_mixed_entries(self):
        store = _fresh_store()
        past_ts = time.time() - 400
        store.put(_make_entry(key_hash="exp", created_ts=past_ts, ttl=300.0))
        store.put(_make_entry(key_hash="live", ttl=300.0))
        removed = store.evict_expired()
        assert removed == 1
        assert store.get("live") is not None


class TestDedupStoreStats:
    def test_stats_keys_present(self):
        store = _fresh_store()
        s = store.stats()
        assert "total" in s
        assert "expired_evicted" in s
        assert "duplicate_hits" in s

    def test_total_increments_on_put(self):
        store = _fresh_store()
        store.put(_make_entry(key_hash="s1"))
        store.put(_make_entry(key_hash="s2"))
        assert store.stats()["total"] == 2

    def test_expired_evicted_increments(self):
        store = _fresh_store()
        past_ts = time.time() - 400
        store.put(_make_entry(key_hash="e1", created_ts=past_ts, ttl=300.0))
        store.evict_expired()
        assert store.stats()["expired_evicted"] == 1

    def test_duplicate_hits_increments_on_is_duplicate_true(self):
        store = _fresh_store()
        store.put(_make_entry(key_hash="d1"))
        store.is_duplicate("d1")
        store.is_duplicate("d1")
        assert store.stats()["duplicate_hits"] == 2

    def test_duplicate_hits_does_not_increment_on_miss(self):
        store = _fresh_store()
        store.is_duplicate("no-such")
        assert store.stats()["duplicate_hits"] == 0


# ===========================================================================
# Section 3 — RequestDeduplicator
# ===========================================================================

class TestDeduplicatorCheck:
    def test_first_call_not_duplicate(self):
        dedup = _fresh_dedup()
        res = dedup.check("SELECT 1")
        assert res.is_duplicate is False

    def test_second_call_is_duplicate(self):
        dedup = _fresh_dedup()
        dedup.check("SELECT 1")
        res = dedup.check("SELECT 1")
        assert res.is_duplicate is True

    def test_duplicate_returns_original_request_id(self):
        dedup = _fresh_dedup()
        first = dedup.check("payload-abc")
        second = dedup.check("payload-abc")
        assert second.original_request_id == first.request_id

    def test_non_duplicate_original_request_id_is_none(self):
        dedup = _fresh_dedup()
        res = dedup.check("unique-payload")
        assert res.original_request_id is None

    def test_result_contains_key_hash(self):
        dedup = _fresh_dedup()
        res = dedup.check("payload-xyz")
        assert len(res.key_hash) == 16

    def test_request_id_returned_in_result(self):
        dedup = _fresh_dedup()
        rid = "my-req-id"
        res = dedup.check("some payload", request_id=rid)
        assert res.request_id == rid

    def test_different_payloads_not_duplicate(self):
        dedup = _fresh_dedup()
        dedup.check("payload-A")
        res = dedup.check("payload-B")
        assert res.is_duplicate is False

    def test_normalized_case_insensitive(self):
        dedup = _fresh_dedup(strategy=DeduplicationStrategy.NORMALIZED)
        dedup.check("Hello World")
        res = dedup.check("HELLO WORLD")
        assert res.is_duplicate is True

    def test_exact_case_sensitive(self):
        dedup = _fresh_dedup(strategy=DeduplicationStrategy.EXACT)
        dedup.check("Hello World")
        res = dedup.check("HELLO WORLD")
        assert res.is_duplicate is False

    def test_semantic_ignores_suffix_beyond_100(self):
        dedup = _fresh_dedup(strategy=DeduplicationStrategy.SEMANTIC)
        prefix = "x" * 100
        dedup.check(prefix + "version-1")
        res = dedup.check(prefix + "version-2")
        assert res.is_duplicate is True


class TestDeduplicatorTTL:
    def test_entry_expired_via_evict(self):
        dedup = _fresh_dedup(ttl=300.0)
        first = dedup.check("some request")
        # Evict using a future timestamp that puts the entry past its TTL
        future = first.key_hash  # just to confirm it's stored
        entry = dedup.store.get(first.key_hash)
        assert entry is not None
        future_now = entry.created_ts + 301
        evicted = dedup.evict_expired(now=future_now)
        assert evicted == 1

    def test_after_eviction_new_check_not_duplicate(self):
        dedup = _fresh_dedup(ttl=300.0)
        first = dedup.check("the payload")
        entry = dedup.store.get(first.key_hash)
        future_now = entry.created_ts + 301
        dedup.evict_expired(now=future_now)
        # Store now empty — next call should NOT be duplicate
        res = dedup.check("the payload")
        assert res.is_duplicate is False

    def test_before_expiry_still_duplicate(self):
        dedup = _fresh_dedup(ttl=300.0)
        first = dedup.check("the payload")
        entry = dedup.store.get(first.key_hash)
        # Evict just before expiry — nothing should be removed
        before_now = entry.created_ts + 299
        evicted = dedup.evict_expired(now=before_now)
        assert evicted == 0
        res = dedup.check("the payload")
        assert res.is_duplicate is True

    def test_get_returns_none_for_expired_without_evict(self):
        """DedupStore.get() must honour TTL even without explicit eviction."""
        dedup = _fresh_dedup(ttl=300.0)
        first = dedup.check("aging request")
        entry = dedup.store.get(first.key_hash)
        # Manually create an already-expired entry in the store
        past_ts = time.time() - 400
        expired_entry = DedupEntry(
            request_id="old-req",
            key_hash="expired-hash",
            strategy=DeduplicationStrategy.NORMALIZED,
            result=None,
            created_ts=past_ts,
            ttl_seconds=300.0,
        )
        dedup.store.put(expired_entry)
        assert dedup.store.get("expired-hash") is None

    def test_zero_ttl_never_expires(self):
        dedup = _fresh_dedup(ttl=0.0)
        dedup.check("immortal payload")
        # Even evicting very far in the future leaves the entry
        removed = dedup.evict_expired(now=time.time() + 1_000_000)
        assert removed == 0
        res = dedup.check("immortal payload")
        assert res.is_duplicate is True


class TestDeduplicatorCompleteAndGetResult:
    def test_complete_stores_result(self):
        dedup = _fresh_dedup()
        res = dedup.check("query")
        dedup.complete(res.request_id, "the answer")
        assert dedup.get_result(res.request_id) == "the answer"

    def test_get_result_before_complete_returns_none(self):
        dedup = _fresh_dedup()
        res = dedup.check("query")
        assert dedup.get_result(res.request_id) is None

    def test_get_result_unknown_id_returns_none(self):
        dedup = _fresh_dedup()
        assert dedup.get_result("no-such-id") is None

    def test_result_retrievable_by_duplicate_caller(self):
        dedup = _fresh_dedup()
        first = dedup.check("my payload")
        dedup.complete(first.request_id, "computed result")
        dup = dedup.check("my payload")
        assert dup.is_duplicate is True
        assert dedup.get_result(dup.original_request_id) == "computed result"

    def test_complete_overwrites_result(self):
        dedup = _fresh_dedup()
        res = dedup.check("query")
        dedup.complete(res.request_id, "first answer")
        dedup.complete(res.request_id, "second answer")
        assert dedup.get_result(res.request_id) == "second answer"

    def test_result_can_be_empty_string(self):
        dedup = _fresh_dedup()
        res = dedup.check("empty result request")
        dedup.complete(res.request_id, "")
        assert dedup.get_result(res.request_id) == ""


class TestDeduplicatorEvictExpired:
    def test_evict_returns_zero_when_nothing_expired(self):
        dedup = _fresh_dedup(ttl=300.0)
        dedup.check("req1")
        assert dedup.evict_expired() == 0

    def test_evict_count_matches_expired_entries(self):
        dedup = _fresh_dedup(ttl=300.0)
        r1 = dedup.check("req-alpha")
        r2 = dedup.check("req-beta")
        e1 = dedup.store.get(r1.key_hash)
        # Both were created at nearly the same time; use e1's timestamp
        future = e1.created_ts + 301
        removed = dedup.evict_expired(now=future)
        assert removed == 2

    def test_evict_only_removes_expired_not_live(self):
        store = _fresh_store()
        past_ts = time.time() - 400
        store.put(_make_entry(key_hash="expired-one", created_ts=past_ts, ttl=300.0))
        store.put(_make_entry(key_hash="live-one", ttl=300.0))
        removed = store.evict_expired()
        assert removed == 1
        assert store.get("live-one") is not None
        assert store.get("expired-one") is None

    def test_stats_expired_evicted_tracks_multiple_calls(self):
        store = _fresh_store()
        past_ts = time.time() - 400
        store.put(_make_entry(key_hash="e1", created_ts=past_ts, ttl=300.0))
        store.evict_expired()
        store.put(_make_entry(key_hash="e2", created_ts=past_ts, ttl=300.0))
        store.evict_expired()
        assert store.stats()["expired_evicted"] == 2


class TestDeduplicatorConfig:
    def test_default_strategy_is_normalized(self):
        dedup = RequestDeduplicator()
        assert dedup.config.strategy == DeduplicationStrategy.NORMALIZED

    def test_default_ttl_is_300(self):
        dedup = RequestDeduplicator()
        assert dedup.config.ttl_seconds == 300.0

    def test_default_max_size_is_10000(self):
        dedup = RequestDeduplicator()
        assert dedup.config.max_size == 10_000

    def test_custom_config_respected(self):
        cfg = DeduplicationConfig(
            strategy=DeduplicationStrategy.EXACT,
            ttl_seconds=60.0,
            max_size=500,
        )
        dedup = RequestDeduplicator(config=cfg)
        assert dedup.config.strategy == DeduplicationStrategy.EXACT
        assert dedup.config.ttl_seconds == 60.0
        assert dedup.config.max_size == 500

    def test_custom_store_injected(self):
        store = _fresh_store()
        dedup = RequestDeduplicator(store=store)
        assert dedup.store is store


# ===========================================================================
# Section 4 — Integration / edge cases
# ===========================================================================

class TestIntegration:
    def test_full_round_trip(self):
        dedup = RequestDeduplicator()
        # First request
        r1 = dedup.check("SELECT * FROM users WHERE id = 42")
        assert r1.is_duplicate is False
        dedup.complete(r1.request_id, '[{"id":42}]')
        # Duplicate request (extra whitespace, different case)
        r2 = dedup.check("SELECT * FROM USERS WHERE ID = 42")
        assert r2.is_duplicate is True
        assert r2.original_request_id == r1.request_id
        assert dedup.get_result(r2.original_request_id) == '[{"id":42}]'

    def test_multiple_unique_payloads(self):
        dedup = _fresh_dedup()
        results = [dedup.check(f"payload-{i}") for i in range(20)]
        assert all(not r.is_duplicate for r in results)

    def test_all_duplicates_after_first(self):
        dedup = _fresh_dedup()
        dedup.check("repeated")
        dups = [dedup.check("repeated") for _ in range(10)]
        assert all(d.is_duplicate for d in dups)

    def test_semantic_long_payload_dedup(self):
        dedup = _fresh_dedup(strategy=DeduplicationStrategy.SEMANTIC)
        base = "semantic query " * 10  # > 100 chars
        first = dedup.check(base + " variant-A")
        second = dedup.check(base + " variant-B")
        assert second.is_duplicate is True

    def test_separate_stores_independent(self):
        d1 = _fresh_dedup()
        d2 = _fresh_dedup()
        d1.check("shared payload")
        res = d2.check("shared payload")
        # d2 has its own store — should NOT be a duplicate
        assert res.is_duplicate is False

    def test_evict_then_recheck_creates_new_entry(self):
        dedup = _fresh_dedup(ttl=100.0)
        r1 = dedup.check("transient request")
        entry = dedup.store.get(r1.key_hash)
        dedup.evict_expired(now=entry.created_ts + 101)
        r2 = dedup.check("transient request")
        assert r2.is_duplicate is False
        assert r2.request_id != r1.request_id

    def test_dedup_result_is_dataclass(self):
        dedup = _fresh_dedup()
        res = dedup.check("anything")
        assert isinstance(res, DeduplicationResult)

    def test_dedup_entry_strategy_preserved(self):
        store = _fresh_store()
        entry = _make_entry(key_hash="strat-test")
        entry.strategy = DeduplicationStrategy.EXACT
        store.put(entry)
        got = store.get("strat-test")
        assert got.strategy == DeduplicationStrategy.EXACT
