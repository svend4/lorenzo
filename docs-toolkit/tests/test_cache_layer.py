"""Tests for docstoolkit.cache_layer — backends, serializers, and CacheLayer."""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Optional
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.cache_layer import (
    CacheBackend,
    CacheConfig,
    CacheLayer,
    CacheStats,
    JsonSerializer,
    MemoryBackend,
    PickleSerializer,
    Serializer,
    SqliteBackend,
    StringSerializer,
)


# ===========================================================================
# Module-level helpers for pickling
# ===========================================================================

class _Point:
    """Simple picklable class used by TestPickleSerializer."""

    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y


# ===========================================================================
# Helpers
# ===========================================================================

def make_memory() -> MemoryBackend:
    return MemoryBackend()


def make_sqlite() -> SqliteBackend:
    return SqliteBackend(":memory:")


# ===========================================================================
# MemoryBackend — basic operations
# ===========================================================================

class TestMemoryBackendBasic:
    def test_get_missing_returns_none(self):
        b = make_memory()
        assert b.get("missing") is None

    def test_set_and_get(self):
        b = make_memory()
        b.set("k", b"hello")
        assert b.get("k") == b"hello"

    def test_set_overwrite(self):
        b = make_memory()
        b.set("k", b"first")
        b.set("k", b"second")
        assert b.get("k") == b"second"

    def test_delete_existing_returns_true(self):
        b = make_memory()
        b.set("k", b"v")
        assert b.delete("k") is True

    def test_delete_removes_entry(self):
        b = make_memory()
        b.set("k", b"v")
        b.delete("k")
        assert b.get("k") is None

    def test_delete_missing_returns_false(self):
        b = make_memory()
        assert b.delete("nope") is False

    def test_clear_returns_count(self):
        b = make_memory()
        b.set("a", b"1")
        b.set("b", b"2")
        b.set("c", b"3")
        assert b.clear() == 3

    def test_clear_removes_all(self):
        b = make_memory()
        b.set("a", b"1")
        b.set("b", b"2")
        b.clear()
        assert b.size() == 0
        assert b.get("a") is None

    def test_size_empty(self):
        b = make_memory()
        assert b.size() == 0

    def test_size_after_set(self):
        b = make_memory()
        b.set("x", b"x")
        b.set("y", b"y")
        assert b.size() == 2

    def test_size_after_delete(self):
        b = make_memory()
        b.set("x", b"x")
        b.delete("x")
        assert b.size() == 0

    def test_multiple_keys(self):
        b = make_memory()
        for i in range(10):
            b.set(f"key{i}", str(i).encode())
        for i in range(10):
            assert b.get(f"key{i}") == str(i).encode()
        assert b.size() == 10

    def test_binary_values(self):
        b = make_memory()
        data = bytes(range(256))
        b.set("bin", data)
        assert b.get("bin") == data


# ===========================================================================
# MemoryBackend — TTL
# ===========================================================================

class TestMemoryBackendTTL:
    def test_no_ttl_does_not_expire(self):
        b = make_memory()
        b.set("k", b"v")
        # Simulate significant time passing without touching time.monotonic
        assert b.get("k") == b"v"

    def test_ttl_future_not_expired(self):
        b = make_memory()
        b.set("k", b"v", ttl=9999.0)
        assert b.get("k") == b"v"

    def test_ttl_expired_returns_none(self):
        b = make_memory()
        # Set a very large "now" so the entry appears expired immediately
        future = time.monotonic() + 1000
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=future):
            b.set("k", b"v", ttl=1.0)  # expiry = future + 1
        # Now access with real time (far past the expiry)
        even_later = future + 2
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=even_later):
            assert b.get("k") is None

    def test_ttl_expired_evicted_from_store(self):
        b = make_memory()
        base = time.monotonic()
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base):
            b.set("k", b"v", ttl=1.0)
        # Access after expiry
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base + 2):
            b.get("k")
        # Size should now reflect eviction
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base + 2):
            assert b.size() == 0

    def test_size_excludes_expired(self):
        b = make_memory()
        base = time.monotonic()
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base):
            b.set("alive", b"1", ttl=9999.0)
            b.set("dead", b"2", ttl=1.0)
        # Check size after the short TTL has expired
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base + 2):
            assert b.size() == 1

    def test_overwrite_resets_ttl(self):
        b = make_memory()
        base = time.monotonic()
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base):
            b.set("k", b"old", ttl=1.0)
        # Overwrite with fresh TTL
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base + 0.5):
            b.set("k", b"new", ttl=9999.0)
        # Should still be alive well after the original TTL
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base + 5):
            assert b.get("k") == b"new"


# ===========================================================================
# SqliteBackend — basic operations
# ===========================================================================

class TestSqliteBackendBasic:
    def test_get_missing_returns_none(self):
        b = make_sqlite()
        assert b.get("missing") is None

    def test_set_and_get(self):
        b = make_sqlite()
        b.set("k", b"world")
        assert b.get("k") == b"world"

    def test_set_overwrite(self):
        b = make_sqlite()
        b.set("k", b"first")
        b.set("k", b"second")
        assert b.get("k") == b"second"

    def test_delete_existing_returns_true(self):
        b = make_sqlite()
        b.set("k", b"v")
        assert b.delete("k") is True

    def test_delete_removes_entry(self):
        b = make_sqlite()
        b.set("k", b"v")
        b.delete("k")
        assert b.get("k") is None

    def test_delete_missing_returns_false(self):
        b = make_sqlite()
        assert b.delete("gone") is False

    def test_clear_returns_count(self):
        b = make_sqlite()
        b.set("a", b"1")
        b.set("b", b"2")
        assert b.clear() == 2

    def test_clear_removes_all(self):
        b = make_sqlite()
        b.set("a", b"1")
        b.clear()
        assert b.size() == 0

    def test_size_empty(self):
        b = make_sqlite()
        assert b.size() == 0

    def test_size_after_set(self):
        b = make_sqlite()
        b.set("x", b"x")
        b.set("y", b"y")
        assert b.size() == 2

    def test_binary_values(self):
        b = make_sqlite()
        data = bytes(range(256))
        b.set("bin", data)
        assert b.get("bin") == data

    def test_file_backed(self, tmp_path):
        path = str(tmp_path / "cache.db")
        b = SqliteBackend(path)
        b.set("persistent", b"value")
        assert b.get("persistent") == b"value"
        b.close()


# ===========================================================================
# SqliteBackend — TTL
# ===========================================================================

class TestSqliteBackendTTL:
    def test_no_ttl_does_not_expire(self):
        b = make_sqlite()
        b.set("k", b"v")
        assert b.get("k") == b"v"

    def test_ttl_future_not_expired(self):
        b = make_sqlite()
        b.set("k", b"v", ttl=9999.0)
        assert b.get("k") == b"v"

    def test_ttl_expired_returns_none(self):
        b = make_sqlite()
        # Store with an already-past expiry by patching time.time at set-time
        past = time.time() - 10
        with patch("docstoolkit.cache_layer.backend.time.time", return_value=past):
            b.set("k", b"v", ttl=1.0)  # expiry = past + 1 = 9s ago
        assert b.get("k") is None

    def test_ttl_expired_evicted_on_access(self):
        b = make_sqlite()
        past = time.time() - 10
        with patch("docstoolkit.cache_layer.backend.time.time", return_value=past):
            b.set("k", b"v", ttl=1.0)
        b.get("k")  # triggers eviction
        assert b.size() == 0

    def test_size_excludes_expired(self):
        b = make_sqlite()
        past = time.time() - 10
        b.set("alive", b"1", ttl=9999.0)
        with patch("docstoolkit.cache_layer.backend.time.time", return_value=past):
            b.set("dead", b"2", ttl=1.0)
        assert b.size() == 1


# ===========================================================================
# JsonSerializer
# ===========================================================================

class TestJsonSerializer:
    def test_roundtrip_str(self):
        s = JsonSerializer()
        assert s.deserialize(s.serialize("hello")) == "hello"

    def test_roundtrip_int(self):
        s = JsonSerializer()
        assert s.deserialize(s.serialize(42)) == 42

    def test_roundtrip_float(self):
        s = JsonSerializer()
        assert s.deserialize(s.serialize(3.14)) == pytest.approx(3.14)

    def test_roundtrip_list(self):
        s = JsonSerializer()
        val = [1, 2, 3, "four"]
        assert s.deserialize(s.serialize(val)) == val

    def test_roundtrip_dict(self):
        s = JsonSerializer()
        val = {"a": 1, "b": [2, 3]}
        assert s.deserialize(s.serialize(val)) == val

    def test_roundtrip_none(self):
        s = JsonSerializer()
        assert s.deserialize(s.serialize(None)) is None

    def test_serialize_returns_bytes(self):
        s = JsonSerializer()
        assert isinstance(s.serialize("x"), bytes)

    def test_unicode(self):
        s = JsonSerializer()
        val = "привет мир"
        assert s.deserialize(s.serialize(val)) == val


# ===========================================================================
# PickleSerializer
# ===========================================================================

class TestPickleSerializer:
    def test_roundtrip_str(self):
        s = PickleSerializer()
        assert s.deserialize(s.serialize("hello")) == "hello"

    def test_roundtrip_int(self):
        s = PickleSerializer()
        assert s.deserialize(s.serialize(99)) == 99

    def test_roundtrip_list(self):
        s = PickleSerializer()
        val = [1, "two", 3.0]
        assert s.deserialize(s.serialize(val)) == val

    def test_roundtrip_dict(self):
        s = PickleSerializer()
        val = {"x": {1, 2, 3}}
        assert s.deserialize(s.serialize(val)) == val

    def test_roundtrip_custom_object(self):
        s = PickleSerializer()
        p = _Point(3, 4)
        assert s.deserialize(s.serialize(p)) == p

    def test_serialize_returns_bytes(self):
        s = PickleSerializer()
        assert isinstance(s.serialize(42), bytes)


# ===========================================================================
# StringSerializer
# ===========================================================================

class TestStringSerializer:
    def test_roundtrip(self):
        s = StringSerializer()
        assert s.deserialize(s.serialize("hello")) == "hello"

    def test_unicode_roundtrip(self):
        s = StringSerializer()
        val = "Привет мир 🌍"
        assert s.deserialize(s.serialize(val)) == val

    def test_serialize_returns_bytes(self):
        s = StringSerializer()
        assert isinstance(s.serialize("hi"), bytes)

    def test_reject_non_string(self):
        s = StringSerializer()
        with pytest.raises(TypeError):
            s.serialize(42)

    def test_reject_list(self):
        s = StringSerializer()
        with pytest.raises(TypeError):
            s.serialize([1, 2])


# ===========================================================================
# CacheStats
# ===========================================================================

class TestCacheStats:
    def test_initial_zero(self):
        st = CacheStats()
        assert st.hits == 0
        assert st.misses == 0
        assert st.evictions == 0

    def test_hit_rate_no_lookups(self):
        assert CacheStats().hit_rate() == 0.0

    def test_hit_rate_all_hits(self):
        st = CacheStats(hits=10, misses=0)
        assert st.hit_rate() == 1.0

    def test_hit_rate_all_misses(self):
        st = CacheStats(hits=0, misses=5)
        assert st.hit_rate() == 0.0

    def test_hit_rate_mixed(self):
        st = CacheStats(hits=3, misses=1)
        assert st.hit_rate() == pytest.approx(0.75)

    def test_hit_rate_half(self):
        st = CacheStats(hits=5, misses=5)
        assert st.hit_rate() == pytest.approx(0.5)


# ===========================================================================
# CacheLayer — get / set / delete
# ===========================================================================

class TestCacheLayerBasic:
    def test_get_missing_returns_none(self):
        c = CacheLayer(MemoryBackend(), JsonSerializer())
        assert c.get("x") is None

    def test_set_and_get(self):
        c = CacheLayer(MemoryBackend(), JsonSerializer())
        c.set("k", {"a": 1})
        assert c.get("k") == {"a": 1}

    def test_set_with_pickle(self):
        c = CacheLayer(MemoryBackend(), PickleSerializer())
        c.set("k", {1, 2, 3})
        assert c.get("k") == {1, 2, 3}

    def test_set_with_string_serializer(self):
        c = CacheLayer(MemoryBackend(), StringSerializer())
        c.set("k", "hello")
        assert c.get("k") == "hello"

    def test_delete_existing(self):
        c = CacheLayer(MemoryBackend(), JsonSerializer())
        c.set("k", 1)
        assert c.delete("k") is True
        assert c.get("k") is None

    def test_delete_missing_returns_false(self):
        c = CacheLayer(MemoryBackend(), JsonSerializer())
        assert c.delete("nope") is False

    def test_clear_returns_count(self):
        c = CacheLayer(MemoryBackend(), JsonSerializer())
        c.set("a", 1)
        c.set("b", 2)
        c.set("c", 3)
        assert c.clear() == 3

    def test_clear_empties_cache(self):
        c = CacheLayer(MemoryBackend(), JsonSerializer())
        c.set("a", 1)
        c.clear()
        assert c.get("a") is None

    def test_default_backend_is_memory(self):
        c = CacheLayer()
        c.set("k", "v")
        assert c.get("k") == "v"

    def test_default_serializer_is_json(self):
        c = CacheLayer(MemoryBackend())
        c.set("k", [1, 2, 3])
        assert c.get("k") == [1, 2, 3]

    def test_sqlite_backend(self):
        c = CacheLayer(SqliteBackend(":memory:"), JsonSerializer())
        c.set("key", {"msg": "sqlite"})
        assert c.get("key") == {"msg": "sqlite"}


# ===========================================================================
# CacheLayer — stats tracking
# ===========================================================================

class TestCacheLayerStats:
    def test_initial_stats_zero(self):
        c = CacheLayer()
        st = c.stats()
        assert st.hits == 0
        assert st.misses == 0
        assert st.evictions == 0

    def test_miss_increments_misses(self):
        c = CacheLayer()
        c.get("absent")
        assert c.stats().misses == 1

    def test_hit_increments_hits(self):
        c = CacheLayer()
        c.set("k", 1)
        c.get("k")
        assert c.stats().hits == 1

    def test_hit_does_not_increment_misses(self):
        c = CacheLayer()
        c.set("k", 1)
        c.get("k")
        assert c.stats().misses == 0

    def test_multiple_hits_and_misses(self):
        c = CacheLayer()
        c.set("a", 1)
        c.set("b", 2)
        c.get("a")   # hit
        c.get("b")   # hit
        c.get("c")   # miss
        st = c.stats()
        assert st.hits == 2
        assert st.misses == 1

    def test_hit_rate_via_stats(self):
        c = CacheLayer()
        c.set("a", 1)
        c.get("a")   # hit
        c.get("b")   # miss
        assert c.stats().hit_rate() == pytest.approx(0.5)

    def test_stats_returns_snapshot(self):
        c = CacheLayer()
        snap1 = c.stats()
        c.get("x")  # miss
        snap2 = c.stats()
        assert snap1.misses == 0
        assert snap2.misses == 1


# ===========================================================================
# CacheLayer — get_or_set
# ===========================================================================

class TestCacheLayerGetOrSet:
    def test_computes_value_on_miss(self):
        c = CacheLayer()
        result = c.get_or_set("k", lambda: 42)
        assert result == 42

    def test_stores_computed_value(self):
        c = CacheLayer()
        c.get_or_set("k", lambda: 42)
        assert c.get("k") == 42

    def test_does_not_call_factory_on_hit(self):
        c = CacheLayer()
        c.set("k", 99)
        calls = []
        result = c.get_or_set("k", lambda: calls.append(1) or 0)
        assert result == 99
        assert calls == []

    def test_factory_called_once_on_miss(self):
        c = CacheLayer()
        calls = []

        def factory():
            calls.append(1)
            return "value"

        c.get_or_set("k", factory)
        assert len(calls) == 1

    def test_custom_ttl_passed_through(self):
        c = CacheLayer(MemoryBackend(), JsonSerializer(), CacheConfig(default_ttl=9999.0))
        c.get_or_set("k", lambda: "hello", ttl=1.0)
        # Verify it stored something
        assert c.get("k") == "hello"


# ===========================================================================
# CacheLayer — eviction
# ===========================================================================

class TestCacheLayerEviction:
    def test_lru_evicts_oldest_on_overflow(self):
        config = CacheConfig(max_size=3, eviction_policy="lru")
        c = CacheLayer(MemoryBackend(), JsonSerializer(), config)
        c.set("a", 1)
        c.set("b", 2)
        c.set("c", 3)
        # Adding a fourth triggers eviction of "a" (oldest)
        c.set("d", 4)
        assert c.stats().evictions >= 1

    def test_random_eviction_policy(self):
        config = CacheConfig(max_size=2, eviction_policy="random")
        c = CacheLayer(MemoryBackend(), JsonSerializer(), config)
        c.set("a", 1)
        c.set("b", 2)
        c.set("c", 3)  # triggers eviction of one random entry
        assert c.stats().evictions >= 1

    def test_ttl_eviction_policy(self):
        config = CacheConfig(max_size=2, eviction_policy="ttl")
        c = CacheLayer(MemoryBackend(), JsonSerializer(), config)
        c.set("a", 1, ttl=1.0)
        c.set("b", 2, ttl=9999.0)
        c.set("c", 3, ttl=9999.0)  # triggers eviction; "a" has shortest TTL
        assert c.stats().evictions >= 1

    def test_eviction_count_tracked(self):
        config = CacheConfig(max_size=2, eviction_policy="lru")
        c = CacheLayer(MemoryBackend(), JsonSerializer(), config)
        for i in range(5):
            c.set(f"k{i}", i)
        assert c.stats().evictions == 3

    def test_no_eviction_under_max_size(self):
        config = CacheConfig(max_size=10, eviction_policy="lru")
        c = CacheLayer(MemoryBackend(), JsonSerializer(), config)
        for i in range(5):
            c.set(f"k{i}", i)
        assert c.stats().evictions == 0


# ===========================================================================
# CacheLayer — TTL propagation
# ===========================================================================

class TestCacheLayerTTL:
    def test_default_ttl_applied(self):
        config = CacheConfig(default_ttl=9999.0)
        c = CacheLayer(MemoryBackend(), JsonSerializer(), config)
        c.set("k", "value")
        assert c.get("k") == "value"

    def test_explicit_ttl_overrides_default(self):
        config = CacheConfig(default_ttl=9999.0)
        b = MemoryBackend()
        c = CacheLayer(b, JsonSerializer(), config)
        base = time.monotonic()
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base):
            c.set("k", "value", ttl=1.0)
        # Access after explicit TTL expired
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base + 2):
            assert c.get("k") is None

    def test_zero_ttl_expires_immediately(self):
        b = MemoryBackend()
        c = CacheLayer(b, JsonSerializer())
        base = time.monotonic()
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base):
            c.set("k", "value", ttl=0.0)
        with patch("docstoolkit.cache_layer.backend.time.monotonic", return_value=base + 0.01):
            assert c.get("k") is None


# ===========================================================================
# ABC contracts
# ===========================================================================

class TestABCContracts:
    def test_cache_backend_is_abstract(self):
        with pytest.raises(TypeError):
            CacheBackend()  # type: ignore[abstract]

    def test_serializer_is_abstract(self):
        with pytest.raises(TypeError):
            Serializer()  # type: ignore[abstract]

    def test_memory_backend_is_instance_of_abc(self):
        assert isinstance(MemoryBackend(), CacheBackend)

    def test_sqlite_backend_is_instance_of_abc(self):
        assert isinstance(SqliteBackend(":memory:"), CacheBackend)

    def test_json_serializer_is_instance_of_abc(self):
        assert isinstance(JsonSerializer(), Serializer)

    def test_pickle_serializer_is_instance_of_abc(self):
        assert isinstance(PickleSerializer(), Serializer)

    def test_string_serializer_is_instance_of_abc(self):
        assert isinstance(StringSerializer(), Serializer)
