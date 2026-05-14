"""Tests for ``docstoolkit.doc_url_resolver``."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_url_resolver import (
    DocUrlResolver,
    ResolverStats,
    UrlMapping,
)


# ---------------------------------------------------------------------------
# TestUrlMappingDataclass
# ---------------------------------------------------------------------------
class TestUrlMappingDataclass:
    def test_construct_with_defaults(self):
        m = UrlMapping(url="https://x", doc_id="d1")
        assert m.url == "https://x"
        assert m.doc_id == "d1"
        assert m.is_primary is True
        assert m.created_at == 0.0

    def test_construct_all_fields(self):
        m = UrlMapping(url="u", doc_id="d", is_primary=False, created_at=42.0)
        assert m.is_primary is False
        assert m.created_at == 42.0

    def test_equality(self):
        a = UrlMapping(url="u", doc_id="d", is_primary=True, created_at=1.0)
        b = UrlMapping(url="u", doc_id="d", is_primary=True, created_at=1.0)
        assert a == b

    def test_inequality_on_doc(self):
        a = UrlMapping(url="u", doc_id="d1")
        b = UrlMapping(url="u", doc_id="d2")
        assert a != b

    def test_inequality_on_primary(self):
        a = UrlMapping(url="u", doc_id="d", is_primary=True)
        b = UrlMapping(url="u", doc_id="d", is_primary=False)
        assert a != b


# ---------------------------------------------------------------------------
# TestResolverStatsDataclass
# ---------------------------------------------------------------------------
class TestResolverStatsDataclass:
    def test_fields(self):
        s = ResolverStats(
            total_mappings=3,
            unique_docs=2,
            unique_urls=3,
            primary_count=2,
        )
        assert s.total_mappings == 3
        assert s.unique_docs == 2
        assert s.unique_urls == 3
        assert s.primary_count == 2

    def test_equality(self):
        a = ResolverStats(1, 1, 1, 1)
        b = ResolverStats(1, 1, 1, 1)
        assert a == b

    def test_inequality(self):
        a = ResolverStats(1, 1, 1, 1)
        b = ResolverStats(1, 1, 1, 0)
        assert a != b


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_initial_state_empty(self):
        r = DocUrlResolver()
        assert r.all_urls() == []
        assert r.all_doc_ids() == []
        assert r.stats() == ResolverStats(0, 0, 0, 0)

    def test_independent_instances(self):
        a = DocUrlResolver()
        b = DocUrlResolver()
        a.map_url("u", "d")
        assert b.all_urls() == []


# ---------------------------------------------------------------------------
# TestMapUrl
# ---------------------------------------------------------------------------
class TestMapUrl:
    def test_new_mapping_default_not_primary(self):
        r = DocUrlResolver()
        m = r.map_url("u1", "d1")
        assert m.url == "u1"
        assert m.doc_id == "d1"
        assert m.is_primary is False

    def test_new_mapping_primary(self):
        r = DocUrlResolver()
        m = r.map_url("u1", "d1", is_primary=True)
        assert m.is_primary is True
        assert r.primary_url_for("d1") == "u1"

    def test_timestamp_uses_now(self):
        r = DocUrlResolver()
        m = r.map_url("u", "d", now=100.0)
        assert m.created_at == 100.0

    def test_timestamp_default(self):
        r = DocUrlResolver()
        m = r.map_url("u", "d")
        assert m.created_at > 0

    def test_replace_same_url_same_doc(self):
        r = DocUrlResolver()
        r.map_url("u", "d", now=1.0)
        m = r.map_url("u", "d", now=2.0)
        assert m.created_at == 2.0
        assert r.urls_for("d") == ["u"]

    def test_replace_url_with_different_doc(self):
        r = DocUrlResolver()
        r.map_url("u", "d1")
        r.map_url("u", "d2")
        assert r.resolve("u") == "d2"
        assert r.urls_for("d1") == []
        assert r.urls_for("d2") == ["u"]

    def test_replace_url_clears_primary_of_old_doc(self):
        r = DocUrlResolver()
        r.map_url("u", "d1", is_primary=True)
        r.map_url("u", "d2", is_primary=False)
        assert r.primary_url_for("d1") is None

    def test_promote_via_map_url_demotes_prev(self):
        r = DocUrlResolver()
        r.map_url("u1", "d", is_primary=True)
        r.map_url("u2", "d", is_primary=True)
        assert r.primary_url_for("d") == "u2"
        m1 = r.get_mapping("u1")
        assert m1 is not None
        assert m1.is_primary is False

    def test_multiple_urls_for_same_doc(self):
        r = DocUrlResolver()
        r.map_url("a", "d")
        r.map_url("b", "d")
        r.map_url("c", "d")
        assert r.urls_for("d") == ["a", "b", "c"]

    def test_remap_same_url_same_primary(self):
        r = DocUrlResolver()
        r.map_url("u", "d", is_primary=True)
        r.map_url("u", "d", is_primary=True, now=2.0)
        assert r.primary_url_for("d") == "u"

    def test_demote_via_non_primary_remap(self):
        # Map first as primary, then remap as non-primary same doc.
        r = DocUrlResolver()
        r.map_url("u", "d", is_primary=True)
        r.map_url("u", "d", is_primary=False)
        # The non-primary remap goes through 'replace prior' branch — primary cleared.
        assert r.primary_url_for("d") is None

    def test_mapping_returned_object_is_stored(self):
        r = DocUrlResolver()
        m = r.map_url("u", "d", is_primary=True)
        assert r.get_mapping("u") is m


# ---------------------------------------------------------------------------
# TestSetPrimary
# ---------------------------------------------------------------------------
class TestSetPrimary:
    def test_set_primary_true(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        assert r.set_primary("u") is True
        assert r.primary_url_for("d") == "u"

    def test_set_primary_unknown_url(self):
        r = DocUrlResolver()
        assert r.set_primary("u") is False

    def test_set_primary_demotes_prev(self):
        r = DocUrlResolver()
        r.map_url("u1", "d", is_primary=True)
        r.map_url("u2", "d")
        assert r.set_primary("u2") is True
        assert r.primary_url_for("d") == "u2"
        m1 = r.get_mapping("u1")
        assert m1 is not None
        assert m1.is_primary is False
        m2 = r.get_mapping("u2")
        assert m2 is not None
        assert m2.is_primary is True

    def test_set_primary_idempotent(self):
        r = DocUrlResolver()
        r.map_url("u", "d", is_primary=True)
        assert r.set_primary("u") is True
        assert r.primary_url_for("d") == "u"

    def test_set_primary_different_docs_independent(self):
        r = DocUrlResolver()
        r.map_url("u1", "d1", is_primary=True)
        r.map_url("u2", "d2")
        r.set_primary("u2")
        assert r.primary_url_for("d1") == "u1"
        assert r.primary_url_for("d2") == "u2"


# ---------------------------------------------------------------------------
# TestUnmapUrl
# ---------------------------------------------------------------------------
class TestUnmapUrl:
    def test_unmap_existing(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        assert r.unmap_url("u") is True
        assert r.resolve("u") is None

    def test_unmap_missing(self):
        r = DocUrlResolver()
        assert r.unmap_url("nope") is False

    def test_unmap_primary_clears_primary(self):
        r = DocUrlResolver()
        r.map_url("u", "d", is_primary=True)
        r.unmap_url("u")
        assert r.primary_url_for("d") is None

    def test_unmap_non_primary_keeps_primary(self):
        r = DocUrlResolver()
        r.map_url("u1", "d", is_primary=True)
        r.map_url("u2", "d")
        r.unmap_url("u2")
        assert r.primary_url_for("d") == "u1"

    def test_unmap_last_url_removes_doc_from_inventory(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        r.unmap_url("u")
        assert "d" not in r.all_doc_ids()

    def test_unmap_one_of_many(self):
        r = DocUrlResolver()
        r.map_url("a", "d")
        r.map_url("b", "d")
        r.unmap_url("a")
        assert r.urls_for("d") == ["b"]


# ---------------------------------------------------------------------------
# TestUnmapDoc
# ---------------------------------------------------------------------------
class TestUnmapDoc:
    def test_unmap_doc_returns_count(self):
        r = DocUrlResolver()
        r.map_url("a", "d")
        r.map_url("b", "d")
        r.map_url("c", "d")
        assert r.unmap_doc("d") == 3

    def test_unmap_doc_missing_returns_zero(self):
        r = DocUrlResolver()
        assert r.unmap_doc("ghost") == 0

    def test_unmap_doc_removes_urls(self):
        r = DocUrlResolver()
        r.map_url("a", "d")
        r.map_url("b", "d")
        r.unmap_doc("d")
        assert r.resolve("a") is None
        assert r.resolve("b") is None

    def test_unmap_doc_clears_primary(self):
        r = DocUrlResolver()
        r.map_url("a", "d", is_primary=True)
        r.unmap_doc("d")
        assert r.primary_url_for("d") is None

    def test_unmap_doc_leaves_other_docs(self):
        r = DocUrlResolver()
        r.map_url("a", "d1")
        r.map_url("b", "d2")
        r.unmap_doc("d1")
        assert r.resolve("b") == "d2"


# ---------------------------------------------------------------------------
# TestResolve
# ---------------------------------------------------------------------------
class TestResolve:
    def test_resolve_existing(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        assert r.resolve("u") == "d"

    def test_resolve_missing(self):
        r = DocUrlResolver()
        assert r.resolve("u") is None

    def test_resolve_after_remap_to_new_doc(self):
        r = DocUrlResolver()
        r.map_url("u", "d1")
        r.map_url("u", "d2")
        assert r.resolve("u") == "d2"

    def test_resolve_after_unmap(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        r.unmap_url("u")
        assert r.resolve("u") is None


# ---------------------------------------------------------------------------
# TestPrimaryUrlFor
# ---------------------------------------------------------------------------
class TestPrimaryUrlFor:
    def test_no_primary_returns_none(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        assert r.primary_url_for("d") is None

    def test_primary_after_map_primary(self):
        r = DocUrlResolver()
        r.map_url("u", "d", is_primary=True)
        assert r.primary_url_for("d") == "u"

    def test_primary_after_set_primary(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        r.set_primary("u")
        assert r.primary_url_for("d") == "u"

    def test_primary_unknown_doc(self):
        r = DocUrlResolver()
        assert r.primary_url_for("nope") is None


# ---------------------------------------------------------------------------
# TestUrlsFor
# ---------------------------------------------------------------------------
class TestUrlsFor:
    def test_sorted(self):
        r = DocUrlResolver()
        for u in ["c", "a", "b"]:
            r.map_url(u, "d")
        assert r.urls_for("d") == ["a", "b", "c"]

    def test_empty_for_unknown_doc(self):
        r = DocUrlResolver()
        assert r.urls_for("d") == []

    def test_unique_urls(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        r.map_url("u", "d")
        assert r.urls_for("d") == ["u"]


# ---------------------------------------------------------------------------
# TestGetMapping
# ---------------------------------------------------------------------------
class TestGetMapping:
    def test_get_existing(self):
        r = DocUrlResolver()
        r.map_url("u", "d", is_primary=True, now=5.0)
        m = r.get_mapping("u")
        assert m is not None
        assert m.url == "u"
        assert m.doc_id == "d"
        assert m.is_primary is True
        assert m.created_at == 5.0

    def test_get_missing(self):
        r = DocUrlResolver()
        assert r.get_mapping("nope") is None

    def test_get_after_unmap(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        r.unmap_url("u")
        assert r.get_mapping("u") is None


# ---------------------------------------------------------------------------
# TestAllUrls
# ---------------------------------------------------------------------------
class TestAllUrls:
    def test_sorted(self):
        r = DocUrlResolver()
        for u in ["x", "a", "m"]:
            r.map_url(u, "d")
        assert r.all_urls() == ["a", "m", "x"]

    def test_empty(self):
        r = DocUrlResolver()
        assert r.all_urls() == []

    def test_across_docs(self):
        r = DocUrlResolver()
        r.map_url("u1", "d1")
        r.map_url("u2", "d2")
        assert r.all_urls() == ["u1", "u2"]


# ---------------------------------------------------------------------------
# TestAllDocIds
# ---------------------------------------------------------------------------
class TestAllDocIds:
    def test_sorted(self):
        r = DocUrlResolver()
        r.map_url("u1", "z")
        r.map_url("u2", "a")
        r.map_url("u3", "m")
        assert r.all_doc_ids() == ["a", "m", "z"]

    def test_unique(self):
        r = DocUrlResolver()
        r.map_url("u1", "d")
        r.map_url("u2", "d")
        assert r.all_doc_ids() == ["d"]

    def test_empty(self):
        r = DocUrlResolver()
        assert r.all_doc_ids() == []


# ---------------------------------------------------------------------------
# TestClear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_returns_count(self):
        r = DocUrlResolver()
        r.map_url("a", "d")
        r.map_url("b", "d")
        r.map_url("c", "d2", is_primary=True)
        assert r.clear() == 3

    def test_clear_empty(self):
        r = DocUrlResolver()
        assert r.clear() == 0

    def test_clear_removes_everything(self):
        r = DocUrlResolver()
        r.map_url("u", "d", is_primary=True)
        r.clear()
        assert r.all_urls() == []
        assert r.all_doc_ids() == []
        assert r.primary_url_for("d") is None

    def test_clear_then_map(self):
        r = DocUrlResolver()
        r.map_url("u", "d")
        r.clear()
        r.map_url("u", "d2")
        assert r.resolve("u") == "d2"


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------
class TestStats:
    def test_initial(self):
        r = DocUrlResolver()
        assert r.stats() == ResolverStats(0, 0, 0, 0)

    def test_counts_after_maps(self):
        r = DocUrlResolver()
        r.map_url("a", "d1", is_primary=True)
        r.map_url("b", "d1")
        r.map_url("c", "d2", is_primary=True)
        s = r.stats()
        assert s.total_mappings == 3
        assert s.unique_urls == 3
        assert s.unique_docs == 2
        assert s.primary_count == 2

    def test_counts_after_unmap(self):
        r = DocUrlResolver()
        r.map_url("a", "d", is_primary=True)
        r.map_url("b", "d")
        r.unmap_url("a")
        s = r.stats()
        assert s.total_mappings == 1
        assert s.primary_count == 0
        assert s.unique_docs == 1

    def test_counts_after_clear(self):
        r = DocUrlResolver()
        r.map_url("a", "d", is_primary=True)
        r.clear()
        assert r.stats() == ResolverStats(0, 0, 0, 0)


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_map_url(self):
        r = DocUrlResolver()
        n_threads = 8
        per_thread = 100

        def worker(tid: int) -> None:
            for i in range(per_thread):
                r.map_url(f"u-{tid}-{i}", f"d-{tid}")

        threads = [
            threading.Thread(target=worker, args=(t,)) for t in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = r.stats()
        assert s.total_mappings == n_threads * per_thread
        assert s.unique_urls == n_threads * per_thread
        assert s.unique_docs == n_threads

    def test_concurrent_set_primary(self):
        r = DocUrlResolver()
        for i in range(50):
            r.map_url(f"u{i}", "d")

        results: list[bool] = []
        lock = threading.Lock()

        def worker(i: int) -> None:
            ok = r.set_primary(f"u{i}")
            with lock:
                results.append(ok)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(results)
        # Exactly one primary remains.
        primaries = [
            u for u in r.all_urls() if r.get_mapping(u) and r.get_mapping(u).is_primary
        ]
        assert len(primaries) == 1
        assert r.primary_url_for("d") == primaries[0]
