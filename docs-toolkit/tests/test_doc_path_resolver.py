"""Tests for E384 DocPathResolver."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_path_resolver import (
    DocPathResolver,
    PathMapping,
    PathResolverStats,
)


class TestPathMappingDataclass:
    def test_create_with_all_fields(self):
        m = PathMapping(path="/a/b", doc_id="doc1", created_at=123.0)
        assert m.path == "/a/b"
        assert m.doc_id == "doc1"
        assert m.created_at == 123.0

    def test_default_created_at(self):
        m = PathMapping(path="/x", doc_id="d")
        assert m.created_at == 0.0

    def test_equality(self):
        a = PathMapping(path="/a", doc_id="d", created_at=1.0)
        b = PathMapping(path="/a", doc_id="d", created_at=1.0)
        assert a == b

    def test_inequality(self):
        a = PathMapping(path="/a", doc_id="d", created_at=1.0)
        b = PathMapping(path="/b", doc_id="d", created_at=1.0)
        assert a != b


class TestPathResolverStatsDataclass:
    def test_create(self):
        s = PathResolverStats(
            total_mappings=5, unique_paths=5, unique_docs=3, total_segments=10
        )
        assert s.total_mappings == 5
        assert s.unique_paths == 5
        assert s.unique_docs == 3
        assert s.total_segments == 10

    def test_equality(self):
        a = PathResolverStats(1, 1, 1, 1)
        b = PathResolverStats(1, 1, 1, 1)
        assert a == b


class TestConstruction:
    def test_empty_on_init(self):
        r = DocPathResolver()
        assert r.all_paths() == []

    def test_stats_empty(self):
        r = DocPathResolver()
        s = r.stats()
        assert s.total_mappings == 0
        assert s.unique_paths == 0
        assert s.unique_docs == 0
        assert s.total_segments == 0

    def test_resolve_empty(self):
        r = DocPathResolver()
        assert r.resolve("/anything") is None


class TestMapPath:
    def test_basic_map(self):
        r = DocPathResolver()
        m = r.map_path("/a/b", "doc1")
        assert m.path == "/a/b"
        assert m.doc_id == "doc1"
        assert m.created_at > 0

    def test_normalize_trailing_slash(self):
        r = DocPathResolver()
        m = r.map_path("/a/b/", "doc1")
        assert m.path == "/a/b"

    def test_normalize_no_leading_slash(self):
        r = DocPathResolver()
        m = r.map_path("a/b", "doc1")
        assert m.path == "/a/b"

    def test_normalize_double_slashes(self):
        r = DocPathResolver()
        m = r.map_path("/a//b///c", "doc1")
        assert m.path == "/a/b/c"

    def test_normalize_root(self):
        r = DocPathResolver()
        m = r.map_path("/", "root_doc")
        assert m.path == "/"

    def test_normalize_empty(self):
        r = DocPathResolver()
        m = r.map_path("", "root_doc")
        assert m.path == "/"

    def test_replace_existing_path(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        r.map_path("/a", "doc2")
        assert r.resolve("/a") == "doc2"
        # doc1 should no longer have any paths
        assert r.paths_for("doc1") == []
        assert r.paths_for("doc2") == ["/a"]

    def test_custom_now(self):
        r = DocPathResolver()
        m = r.map_path("/a", "doc1", now=999.0)
        assert m.created_at == 999.0

    def test_multiple_paths_same_doc(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        r.map_path("/b", "doc1")
        assert r.paths_for("doc1") == ["/a", "/b"]


class TestUnmapPath:
    def test_unmap_existing_true(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        assert r.unmap_path("/a") is True
        assert r.resolve("/a") is None

    def test_unmap_missing_false(self):
        r = DocPathResolver()
        assert r.unmap_path("/missing") is False

    def test_unmap_normalizes(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        assert r.unmap_path("a/") is True

    def test_unmap_cleans_reverse_index(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        r.unmap_path("/a")
        assert r.paths_for("doc1") == []

    def test_unmap_preserves_other_paths(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        r.map_path("/b", "doc1")
        r.unmap_path("/a")
        assert r.paths_for("doc1") == ["/b"]


class TestUnmapDoc:
    def test_unmap_doc_count(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        r.map_path("/b", "doc1")
        r.map_path("/c", "doc1")
        assert r.unmap_doc("doc1") == 3
        assert r.paths_for("doc1") == []

    def test_unmap_doc_missing_zero(self):
        r = DocPathResolver()
        assert r.unmap_doc("missing") == 0

    def test_unmap_doc_removes_paths(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        r.map_path("/b", "doc2")
        r.unmap_doc("doc1")
        assert r.resolve("/a") is None
        assert r.resolve("/b") == "doc2"


class TestResolve:
    def test_resolve_found(self):
        r = DocPathResolver()
        r.map_path("/a/b", "doc1")
        assert r.resolve("/a/b") == "doc1"

    def test_resolve_not_found(self):
        r = DocPathResolver()
        assert r.resolve("/missing") is None

    def test_resolve_normalizes_lookup(self):
        r = DocPathResolver()
        r.map_path("/a/b", "doc1")
        assert r.resolve("/a/b/") == "doc1"
        assert r.resolve("a/b") == "doc1"
        assert r.resolve("//a//b") == "doc1"

    def test_resolve_root(self):
        r = DocPathResolver()
        r.map_path("/", "root")
        assert r.resolve("/") == "root"
        assert r.resolve("") == "root"


class TestPathsFor:
    def test_paths_for_sorted(self):
        r = DocPathResolver()
        r.map_path("/c", "doc1")
        r.map_path("/a", "doc1")
        r.map_path("/b", "doc1")
        assert r.paths_for("doc1") == ["/a", "/b", "/c"]

    def test_paths_for_missing(self):
        r = DocPathResolver()
        assert r.paths_for("missing") == []

    def test_paths_for_returns_list(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        result = r.paths_for("doc1")
        assert isinstance(result, list)


class TestChildrenOf:
    def test_only_direct_children(self):
        r = DocPathResolver()
        r.map_path("/a", "doc_a")
        r.map_path("/a/b", "doc_b")
        r.map_path("/a/c", "doc_c")
        r.map_path("/a/b/d", "doc_d")
        children = r.children_of("/a")
        assert children == ["/a/b", "/a/c"]

    def test_children_sorted(self):
        r = DocPathResolver()
        r.map_path("/p/z", "d1")
        r.map_path("/p/a", "d2")
        r.map_path("/p/m", "d3")
        assert r.children_of("/p") == ["/p/a", "/p/m", "/p/z"]

    def test_children_of_root(self):
        r = DocPathResolver()
        r.map_path("/a", "d1")
        r.map_path("/b", "d2")
        r.map_path("/a/c", "d3")
        assert r.children_of("/") == ["/a", "/b"]

    def test_children_empty(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        assert r.children_of("/a") == []

    def test_children_normalize_parent(self):
        r = DocPathResolver()
        r.map_path("/a/b", "d1")
        assert r.children_of("/a/") == ["/a/b"]
        assert r.children_of("a") == ["/a/b"]


class TestDescendantsOf:
    def test_all_under(self):
        r = DocPathResolver()
        r.map_path("/a", "d_a")
        r.map_path("/a/b", "d_b")
        r.map_path("/a/b/c", "d_c")
        r.map_path("/a/d", "d_d")
        r.map_path("/x", "d_x")
        desc = r.descendants_of("/a")
        assert desc == ["/a/b", "/a/b/c", "/a/d"]

    def test_descendants_sorted(self):
        r = DocPathResolver()
        r.map_path("/p/z", "d1")
        r.map_path("/p/a/x", "d2")
        r.map_path("/p/m", "d3")
        result = r.descendants_of("/p")
        assert result == sorted(result)

    def test_descendants_of_root(self):
        r = DocPathResolver()
        r.map_path("/", "root")
        r.map_path("/a", "d1")
        r.map_path("/a/b", "d2")
        desc = r.descendants_of("/")
        assert desc == ["/a", "/a/b"]

    def test_descendants_empty(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        assert r.descendants_of("/a") == []

    def test_descendants_excludes_self(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        r.map_path("/a/b", "doc2")
        assert "/a" not in r.descendants_of("/a")


class TestParentOf:
    def test_parent_basic(self):
        r = DocPathResolver()
        assert r.parent_of("/a/b/c") == "/a/b"

    def test_parent_of_single_segment(self):
        r = DocPathResolver()
        assert r.parent_of("/a") == "/"

    def test_parent_of_root_none(self):
        r = DocPathResolver()
        assert r.parent_of("/") is None

    def test_parent_of_empty_none(self):
        r = DocPathResolver()
        assert r.parent_of("") is None

    def test_parent_normalizes(self):
        r = DocPathResolver()
        assert r.parent_of("/a/b/") == "/a"
        assert r.parent_of("a/b") == "/a"


class TestSegmentsOf:
    def test_basic(self):
        r = DocPathResolver()
        assert r.segments_of("/a/b/c") == ["a", "b", "c"]

    def test_root_empty(self):
        r = DocPathResolver()
        assert r.segments_of("/") == []

    def test_excludes_empty_double_slashes(self):
        r = DocPathResolver()
        assert r.segments_of("/a//b") == ["a", "b"]

    def test_trailing_slash(self):
        r = DocPathResolver()
        assert r.segments_of("/a/b/") == ["a", "b"]

    def test_no_leading_slash(self):
        r = DocPathResolver()
        assert r.segments_of("a/b") == ["a", "b"]


class TestAllPaths:
    def test_all_paths_sorted(self):
        r = DocPathResolver()
        r.map_path("/c", "d1")
        r.map_path("/a", "d2")
        r.map_path("/b", "d3")
        mappings = r.all_paths()
        assert [m.path for m in mappings] == ["/a", "/b", "/c"]

    def test_all_paths_empty(self):
        r = DocPathResolver()
        assert r.all_paths() == []

    def test_all_paths_returns_mappings(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        mappings = r.all_paths()
        assert all(isinstance(m, PathMapping) for m in mappings)


class TestClear:
    def test_clear_count(self):
        r = DocPathResolver()
        r.map_path("/a", "d1")
        r.map_path("/b", "d2")
        r.map_path("/c", "d3")
        assert r.clear() == 3

    def test_clear_empties(self):
        r = DocPathResolver()
        r.map_path("/a", "d1")
        r.clear()
        assert r.all_paths() == []
        assert r.resolve("/a") is None

    def test_clear_empty_zero(self):
        r = DocPathResolver()
        assert r.clear() == 0

    def test_clear_clears_reverse_index(self):
        r = DocPathResolver()
        r.map_path("/a", "doc1")
        r.clear()
        assert r.paths_for("doc1") == []


class TestStats:
    def test_stats_totals(self):
        r = DocPathResolver()
        r.map_path("/a", "d1")
        r.map_path("/a/b", "d1")
        r.map_path("/x/y/z", "d2")
        s = r.stats()
        assert s.total_mappings == 3
        assert s.unique_paths == 3
        assert s.unique_docs == 2
        # 1 + 2 + 3
        assert s.total_segments == 6

    def test_stats_root(self):
        r = DocPathResolver()
        r.map_path("/", "root")
        s = r.stats()
        assert s.total_mappings == 1
        assert s.total_segments == 0

    def test_stats_empty(self):
        r = DocPathResolver()
        s = r.stats()
        assert s == PathResolverStats(0, 0, 0, 0)


class TestThreadSafety:
    def test_concurrent_map_path(self):
        r = DocPathResolver()
        N = 100
        T = 8

        def worker(start: int):
            for i in range(N):
                r.map_path(f"/p/{start}/{i}", f"doc_{start}_{i}")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(T)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = r.stats()
        assert s.total_mappings == N * T
        assert s.unique_docs == N * T

    def test_concurrent_unmap(self):
        r = DocPathResolver()
        for i in range(50):
            r.map_path(f"/p/{i}", f"doc_{i}")

        def worker(ids):
            for i in ids:
                r.unmap_path(f"/p/{i}")

        t1 = threading.Thread(target=worker, args=(range(0, 25),))
        t2 = threading.Thread(target=worker, args=(range(25, 50),))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        assert r.stats().total_mappings == 0
