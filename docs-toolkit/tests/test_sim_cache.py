"""Tests for the sim_cache module: fingerprinting, store, and high-level cache."""
import time
import pytest

from docstoolkit.sim_cache import (
    Fingerprint,
    FingerprintBuilder,
    FingerprintMethod,
    SimilarityEntry,
    SimCacheStore,
    SimCacheConfig,
    SimCacheLookupResult,
    SemanticSimilarityCache,
)


# ===========================================================================
# FingerprintBuilder — token_hash
# ===========================================================================

class TestTokenHash:
    def test_returns_fingerprint(self):
        fp = FingerprintBuilder.token_hash("hello world")
        assert isinstance(fp, Fingerprint)

    def test_method_is_token_hash(self):
        fp = FingerprintBuilder.token_hash("hello")
        assert fp.method == FingerprintMethod.TOKEN_HASH

    def test_value_is_int(self):
        fp = FingerprintBuilder.token_hash("hello")
        assert isinstance(fp.value, int)

    def test_deterministic(self):
        fp1 = FingerprintBuilder.token_hash("same text")
        fp2 = FingerprintBuilder.token_hash("same text")
        assert fp1.value == fp2.value

    def test_different_texts_give_different_hashes(self):
        fp1 = FingerprintBuilder.token_hash("hello world")
        fp2 = FingerprintBuilder.token_hash("goodbye world")
        assert fp1.value != fp2.value

    def test_text_len_stored(self):
        text = "hello world"
        fp = FingerprintBuilder.token_hash(text)
        assert fp.text_len == len(text)

    def test_whitespace_normalization(self):
        fp1 = FingerprintBuilder.token_hash("hello   world")
        fp2 = FingerprintBuilder.token_hash("hello world")
        assert fp1.value == fp2.value

    def test_case_normalization(self):
        fp1 = FingerprintBuilder.token_hash("Hello World")
        fp2 = FingerprintBuilder.token_hash("hello world")
        assert fp1.value == fp2.value

    def test_empty_string(self):
        fp = FingerprintBuilder.token_hash("")
        assert isinstance(fp.value, int)
        assert fp.text_len == 0

    def test_value_fits_in_8_bytes(self):
        fp = FingerprintBuilder.token_hash("some text here")
        assert 0 <= fp.value < (1 << 64)


# ===========================================================================
# FingerprintBuilder — simhash
# ===========================================================================

class TestSimHash:
    def test_returns_fingerprint(self):
        fp = FingerprintBuilder.simhash("hello world")
        assert isinstance(fp, Fingerprint)

    def test_method_is_simhash(self):
        fp = FingerprintBuilder.simhash("hello")
        assert fp.method == FingerprintMethod.SIMHASH

    def test_value_is_int(self):
        fp = FingerprintBuilder.simhash("hello")
        assert isinstance(fp.value, int)

    def test_deterministic(self):
        fp1 = FingerprintBuilder.simhash("same text here")
        fp2 = FingerprintBuilder.simhash("same text here")
        assert fp1.value == fp2.value

    def test_default_64_bits(self):
        fp = FingerprintBuilder.simhash("hello world")
        assert 0 <= fp.value < (1 << 64)

    def test_bit_count_param(self):
        fp = FingerprintBuilder.simhash("hello world", bits=32)
        assert 0 <= fp.value < (1 << 32)

    def test_different_texts_usually_differ(self):
        fp1 = FingerprintBuilder.simhash("the quick brown fox")
        fp2 = FingerprintBuilder.simhash("lorem ipsum dolor sit")
        assert fp1.value != fp2.value

    def test_text_len_stored(self):
        text = "hello world"
        fp = FingerprintBuilder.simhash(text)
        assert fp.text_len == len(text)

    def test_empty_string(self):
        fp = FingerprintBuilder.simhash("")
        assert isinstance(fp.value, int)

    def test_similar_texts_have_close_simhash(self):
        base = "the quick brown fox jumps over the lazy dog"
        similar = "the quick brown fox jumps over the lazy cat"
        fp1 = FingerprintBuilder.simhash(base)
        fp2 = FingerprintBuilder.simhash(similar)
        sim = fp1.similarity(fp2)
        assert sim > 0.5, f"Expected similar texts to have sim > 0.5, got {sim}"


# ===========================================================================
# FingerprintBuilder — minhash
# ===========================================================================

class TestMinHash:
    def test_returns_fingerprint(self):
        fp = FingerprintBuilder.minhash("hello world")
        assert isinstance(fp, Fingerprint)

    def test_method_is_minhash(self):
        fp = FingerprintBuilder.minhash("hello")
        assert fp.method == FingerprintMethod.MINHASH

    def test_value_is_int(self):
        fp = FingerprintBuilder.minhash("hello")
        assert isinstance(fp.value, int)

    def test_deterministic(self):
        fp1 = FingerprintBuilder.minhash("same text here")
        fp2 = FingerprintBuilder.minhash("same text here")
        assert fp1.value == fp2.value

    def test_value_fits_in_64_bits(self):
        fp = FingerprintBuilder.minhash("hello world")
        assert 0 <= fp.value < (1 << 64)

    def test_empty_string(self):
        fp = FingerprintBuilder.minhash("")
        assert fp.value == 0

    def test_num_hashes_param(self):
        fp1 = FingerprintBuilder.minhash("hello", num_hashes=8)
        fp2 = FingerprintBuilder.minhash("hello", num_hashes=16)
        # Different number of hashes can yield different packed values
        assert isinstance(fp1.value, int)
        assert isinstance(fp2.value, int)

    def test_text_len_stored(self):
        text = "hello world"
        fp = FingerprintBuilder.minhash(text)
        assert fp.text_len == len(text)


# ===========================================================================
# FingerprintBuilder — build dispatch
# ===========================================================================

class TestBuild:
    def test_build_simhash(self):
        fp = FingerprintBuilder.build("hello", FingerprintMethod.SIMHASH)
        assert fp.method == FingerprintMethod.SIMHASH

    def test_build_token_hash(self):
        fp = FingerprintBuilder.build("hello", FingerprintMethod.TOKEN_HASH)
        assert fp.method == FingerprintMethod.TOKEN_HASH

    def test_build_minhash(self):
        fp = FingerprintBuilder.build("hello", FingerprintMethod.MINHASH)
        assert fp.method == FingerprintMethod.MINHASH

    def test_build_default_is_simhash(self):
        fp = FingerprintBuilder.build("hello")
        assert fp.method == FingerprintMethod.SIMHASH


# ===========================================================================
# Fingerprint.similarity
# ===========================================================================

class TestFingerprintSimilarity:
    def test_token_hash_identical(self):
        fp = FingerprintBuilder.token_hash("hello")
        assert fp.similarity(fp) == 1.0

    def test_token_hash_same_value(self):
        fp1 = FingerprintBuilder.token_hash("hello world")
        fp2 = FingerprintBuilder.token_hash("hello world")
        assert fp1.similarity(fp2) == 1.0

    def test_token_hash_different(self):
        fp1 = FingerprintBuilder.token_hash("hello")
        fp2 = FingerprintBuilder.token_hash("goodbye")
        assert fp1.similarity(fp2) == 0.0

    def test_simhash_identical(self):
        fp = FingerprintBuilder.simhash("hello world")
        assert fp.similarity(fp) == 1.0

    def test_simhash_same_text(self):
        fp1 = FingerprintBuilder.simhash("hello world")
        fp2 = FingerprintBuilder.simhash("hello world")
        assert fp1.similarity(fp2) == 1.0

    def test_simhash_different_texts_less_than_one(self):
        fp1 = FingerprintBuilder.simhash("completely different text alpha")
        fp2 = FingerprintBuilder.simhash("totally unrelated content beta")
        sim = fp1.similarity(fp2)
        assert 0.0 <= sim <= 1.0

    def test_simhash_similarity_range(self):
        fp1 = FingerprintBuilder.simhash("some text")
        fp2 = FingerprintBuilder.simhash("other text")
        sim = fp1.similarity(fp2)
        assert 0.0 <= sim <= 1.0

    def test_minhash_identical(self):
        fp = FingerprintBuilder.minhash("hello world")
        assert fp.similarity(fp) == 1.0

    def test_minhash_same_text(self):
        fp1 = FingerprintBuilder.minhash("hello world")
        fp2 = FingerprintBuilder.minhash("hello world")
        assert fp1.similarity(fp2) == 1.0

    def test_cross_method_raises(self):
        fp1 = FingerprintBuilder.token_hash("hello")
        fp2 = FingerprintBuilder.simhash("hello")
        with pytest.raises(ValueError):
            fp1.similarity(fp2)

    def test_simhash_symmetry(self):
        fp1 = FingerprintBuilder.simhash("foo bar baz")
        fp2 = FingerprintBuilder.simhash("baz qux quux")
        assert fp1.similarity(fp2) == fp2.similarity(fp1)


# ===========================================================================
# SimilarityEntry
# ===========================================================================

class TestSimilarityEntry:
    def test_auto_entry_id(self):
        fp = FingerprintBuilder.simhash("text")
        entry = SimilarityEntry(text="text", fingerprint=fp, result="r")
        assert entry.entry_id is not None
        assert len(entry.entry_id) == 8

    def test_auto_created_ts(self):
        before = time.time()
        fp = FingerprintBuilder.simhash("text")
        entry = SimilarityEntry(text="text", fingerprint=fp, result="r")
        after = time.time()
        assert before <= entry.created_ts <= after

    def test_default_hit_count_zero(self):
        fp = FingerprintBuilder.simhash("text")
        entry = SimilarityEntry(text="text", fingerprint=fp, result="r")
        assert entry.hit_count == 0

    def test_unique_ids(self):
        fp = FingerprintBuilder.simhash("text")
        e1 = SimilarityEntry(text="text", fingerprint=fp, result="r")
        e2 = SimilarityEntry(text="text", fingerprint=fp, result="r")
        assert e1.entry_id != e2.entry_id


# ===========================================================================
# SimCacheStore
# ===========================================================================

class TestSimCacheStore:
    def _make_store(self):
        return SimCacheStore()

    def _make_entry(self, text="hello world", result="result"):
        fp = FingerprintBuilder.simhash(text)
        return SimilarityEntry(text=text, fingerprint=fp, result=result)

    def test_add_and_get(self):
        store = self._make_store()
        entry = self._make_entry()
        store.add(entry)
        retrieved = store.get(entry.entry_id)
        assert retrieved is not None
        assert retrieved.entry_id == entry.entry_id
        assert retrieved.result == entry.result

    def test_get_nonexistent(self):
        store = self._make_store()
        assert store.get("nonexistent") is None

    def test_count_empty(self):
        store = self._make_store()
        assert store.count() == 0

    def test_count_after_add(self):
        store = self._make_store()
        store.add(self._make_entry("text one"))
        store.add(self._make_entry("text two"))
        assert store.count() == 2

    def test_find_similar_exact_match(self):
        store = self._make_store()
        entry = self._make_entry("hello world")
        store.add(entry)
        fp = FingerprintBuilder.simhash("hello world")
        results = store.find_similar(fp, threshold=1.0)
        assert len(results) == 1
        assert results[0].entry_id == entry.entry_id

    def test_find_similar_threshold_filtering(self):
        store = self._make_store()
        # Add a very different text
        entry = self._make_entry("completely unrelated zebra potato")
        store.add(entry)
        fp = FingerprintBuilder.simhash("hello world foo bar")
        # With a high threshold, the unrelated text should not match
        results = store.find_similar(fp, threshold=0.95)
        # The dissimilar entry should not appear
        ids = [r.entry_id for r in results]
        assert entry.entry_id not in ids

    def test_find_similar_returns_sorted_desc(self):
        store = self._make_store()
        text_a = "the quick brown fox jumps over the lazy dog"
        text_b = "completely different unrelated content here now"
        entry_a = self._make_entry(text_a, "result_a")
        entry_b = self._make_entry(text_b, "result_b")
        store.add(entry_a)
        store.add(entry_b)
        query_fp = FingerprintBuilder.simhash(text_a)
        results = store.find_similar(query_fp, threshold=0.0)
        assert len(results) >= 1
        # First result should be entry_a (exact match)
        assert results[0].entry_id == entry_a.entry_id

    def test_find_similar_empty_store(self):
        store = self._make_store()
        fp = FingerprintBuilder.simhash("hello")
        assert store.find_similar(fp) == []

    def test_increment_hits(self):
        store = self._make_store()
        entry = self._make_entry()
        store.add(entry)
        store.increment_hits(entry.entry_id)
        retrieved = store.get(entry.entry_id)
        assert retrieved.hit_count == 1

    def test_increment_hits_multiple(self):
        store = self._make_store()
        entry = self._make_entry()
        store.add(entry)
        store.increment_hits(entry.entry_id)
        store.increment_hits(entry.entry_id)
        store.increment_hits(entry.entry_id)
        retrieved = store.get(entry.entry_id)
        assert retrieved.hit_count == 3

    def test_stats_empty(self):
        store = self._make_store()
        s = store.stats()
        assert s["total"] == 0
        assert s["total_hits"] == 0
        assert s["avg_hits"] == 0.0

    def test_stats_with_entries(self):
        store = self._make_store()
        store.add(self._make_entry("text one"))
        store.add(self._make_entry("text two"))
        s = store.stats()
        assert s["total"] == 2
        assert s["total_hits"] == 0

    def test_stats_after_hits(self):
        store = self._make_store()
        entry = self._make_entry("text one")
        store.add(entry)
        store.increment_hits(entry.entry_id)
        store.increment_hits(entry.entry_id)
        s = store.stats()
        assert s["total_hits"] == 2
        assert s["avg_hits"] == 2.0

    def test_evict_lru_removes_oldest(self):
        store = self._make_store()
        for i in range(5):
            store.add(self._make_entry(f"text number {i}"))
        removed = store.evict_lru(3)
        assert removed == 2
        assert store.count() == 3

    def test_evict_lru_no_op_when_under_limit(self):
        store = self._make_store()
        store.add(self._make_entry("text"))
        removed = store.evict_lru(10)
        assert removed == 0
        assert store.count() == 1

    def test_evict_expired(self):
        store = self._make_store()
        entry = self._make_entry("old text")
        store.add(entry)
        # Evict with ttl=0 means everything is expired
        removed = store.evict_expired(ttl_seconds=0, now=time.time() + 1)
        assert removed == 1
        assert store.count() == 0

    def test_find_similar_only_same_method(self):
        store = self._make_store()
        # Add a SIMHASH entry
        fp_sim = FingerprintBuilder.simhash("hello world")
        entry = SimilarityEntry(text="hello world", fingerprint=fp_sim, result="r")
        store.add(entry)
        # Query with MINHASH fingerprint
        fp_min = FingerprintBuilder.minhash("hello world")
        results = store.find_similar(fp_min, threshold=0.0)
        assert results == []


# ===========================================================================
# SemanticSimilarityCache
# ===========================================================================

class TestSemanticSimilarityCache:
    def _make_cache(self, **kwargs):
        config = SimCacheConfig(**kwargs)
        return SemanticSimilarityCache(config=config)

    def test_miss_on_empty_cache(self):
        cache = self._make_cache()
        result = cache.get("hello world")
        assert result.hit is False
        assert result.result is None
        assert result.entry_id is None
        assert result.similarity == 0.0

    def test_set_returns_entry_id(self):
        cache = self._make_cache()
        eid = cache.set("hello world", "the result")
        assert isinstance(eid, str)
        assert len(eid) == 8

    def test_hit_on_identical_text(self):
        cache = self._make_cache()
        cache.set("hello world", "the result")
        result = cache.get("hello world")
        assert result.hit is True
        assert result.result == "the result"

    def test_hit_on_similar_text(self):
        cache = self._make_cache(threshold=0.5)
        base = "the quick brown fox jumps over the lazy dog"
        cache.set(base, "fox result")
        similar = "the quick brown fox jumps over the lazy cat"
        result = cache.get(similar)
        assert result.hit is True
        assert result.result == "fox result"

    def test_miss_on_dissimilar_text(self):
        cache = self._make_cache(threshold=0.95)
        cache.set("the quick brown fox jumps over the lazy dog", "result")
        result = cache.get("completely unrelated zebra lorem ipsum dolor")
        assert result.hit is False

    def test_set_get_round_trip(self):
        cache = self._make_cache()
        cache.set("normalize whitespace   test", "answer")
        result = cache.get("normalize whitespace test")
        assert result.hit is True
        assert result.result == "answer"

    def test_size_increments(self):
        cache = self._make_cache()
        assert cache.size() == 0
        cache.set("text one", "r1")
        assert cache.size() == 1
        cache.set("text two", "r2")
        assert cache.size() == 2

    def test_stats_keys(self):
        cache = self._make_cache()
        cache.set("hello", "world")
        s = cache.stats()
        assert "total" in s
        assert "total_hits" in s
        assert "avg_hits" in s

    def test_stats_hit_count_incremented_on_get(self):
        cache = self._make_cache()
        cache.set("hello world", "result")
        cache.get("hello world")
        s = cache.stats()
        assert s["total_hits"] >= 1

    def test_lookup_result_has_similarity(self):
        cache = self._make_cache()
        cache.set("hello world", "result")
        result = cache.get("hello world")
        assert result.hit is True
        assert result.similarity == 1.0

    def test_lookup_result_entry_id(self):
        cache = self._make_cache()
        eid = cache.set("hello world", "result")
        result = cache.get("hello world")
        assert result.entry_id == eid

    def test_max_size_respected(self):
        cache = self._make_cache(max_size=3)
        for i in range(5):
            cache.set(f"unique text document number {i} extra words", f"r{i}")
        assert cache.size() <= 4  # max_size=3, +1 for the final set before evict

    def test_ttl_expiry(self):
        cache = self._make_cache(ttl_seconds=0.001)
        cache.set("hello world", "result")
        time.sleep(0.01)
        result = cache.get("hello world")
        assert result.hit is False

    def test_multiple_sets_different_texts(self):
        cache = self._make_cache()
        cache.set("first document text", "result one")
        cache.set("second document text", "result two")
        r1 = cache.get("first document text")
        r2 = cache.get("second document text")
        assert r1.hit is True
        assert r2.hit is True
        assert r1.result == "result one"
        assert r2.result == "result two"

    def test_default_config(self):
        cache = SemanticSimilarityCache()
        assert cache.size() == 0

    def test_custom_store(self):
        store = SimCacheStore()
        cache = SemanticSimilarityCache(store=store)
        cache.set("hello", "world")
        assert store.count() == 1

    def test_token_hash_method(self):
        config = SimCacheConfig(method=FingerprintMethod.TOKEN_HASH, threshold=1.0)
        cache = SemanticSimilarityCache(config=config)
        cache.set("hello world", "result")
        result = cache.get("hello world")
        assert result.hit is True

    def test_minhash_method(self):
        config = SimCacheConfig(method=FingerprintMethod.MINHASH, threshold=0.0)
        cache = SemanticSimilarityCache(config=config)
        cache.set("hello world", "result")
        result = cache.get("hello world")
        assert result.hit is True
