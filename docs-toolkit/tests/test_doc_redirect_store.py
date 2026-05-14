"""Tests for E351 DocRedirectStore."""

from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_redirect_store import (
    DocRedirectStore,
    Redirect,
    RedirectStats,
)


# ---------------------------------------------------------------- dataclasses
class TestRedirectDataclass:
    def test_construct_required(self):
        r = Redirect(
            redirect_id="abc",
            from_path="/a",
            to_path="/b",
        )
        assert r.redirect_id == "abc"
        assert r.from_path == "/a"
        assert r.to_path == "/b"

    def test_defaults(self):
        r = Redirect(redirect_id="x", from_path="/a", to_path="/b")
        assert r.code == 301
        assert r.created_at == 0.0
        assert r.hit_count == 0
        assert r.enabled is True

    def test_override_fields(self):
        r = Redirect(
            redirect_id="x",
            from_path="/a",
            to_path="/b",
            code=302,
            created_at=12.5,
            hit_count=7,
            enabled=False,
        )
        assert r.code == 302
        assert r.created_at == 12.5
        assert r.hit_count == 7
        assert r.enabled is False

    def test_is_dataclass(self):
        import dataclasses

        assert dataclasses.is_dataclass(Redirect)


class TestRedirectStatsDataclass:
    def test_construct(self):
        s = RedirectStats(
            total_redirects=3, enabled_redirects=2, total_hits=10
        )
        assert s.total_redirects == 3
        assert s.enabled_redirects == 2
        assert s.total_hits == 10

    def test_is_dataclass(self):
        import dataclasses

        assert dataclasses.is_dataclass(RedirectStats)


# ----------------------------------------------------------------- Construction
class TestConstruction:
    def test_empty_store(self):
        store = DocRedirectStore()
        assert store.list_redirects() == []

    def test_initial_stats(self):
        store = DocRedirectStore()
        s = store.stats()
        assert s.total_redirects == 0
        assert s.enabled_redirects == 0
        assert s.total_hits == 0

    def test_independent_instances(self):
        a = DocRedirectStore()
        b = DocRedirectStore()
        a.add("/x", "/y")
        assert b.list_redirects() == []


# ------------------------------------------------------------------------ Add
class TestAdd:
    def test_add_returns_redirect(self):
        store = DocRedirectStore()
        r = store.add("/old", "/new")
        assert isinstance(r, Redirect)
        assert r.from_path == "/old"
        assert r.to_path == "/new"

    def test_add_generates_uuid(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        # Must parse as UUID
        uuid.UUID(r.redirect_id)

    def test_add_unique_ids(self):
        store = DocRedirectStore()
        r1 = store.add("/a", "/b")
        r2 = store.add("/c", "/d")
        assert r1.redirect_id != r2.redirect_id

    def test_add_default_code(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        assert r.code == 301

    def test_add_custom_code(self):
        store = DocRedirectStore()
        for code in (301, 302, 307, 308):
            r = store.add(f"/from{code}", "/to", code=code)
            assert r.code == code

    def test_add_default_enabled(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        assert r.enabled is True

    def test_add_hit_count_starts_zero(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        assert r.hit_count == 0

    def test_add_uses_now_override(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b", now=1234.5)
        assert r.created_at == 1234.5

    def test_add_uses_time_when_now_none(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        assert r.created_at > 0

    def test_add_replaces_by_from_path(self):
        store = DocRedirectStore()
        r1 = store.add("/old", "/new1")
        r2 = store.add("/old", "/new2")
        # Old redirect must be gone
        assert store.get(r1.redirect_id) is None
        assert store.get(r2.redirect_id) is not None
        # Only one in list
        assert len(store.list_redirects()) == 1
        assert store.list_redirects()[0].to_path == "/new2"

    def test_add_replace_gives_new_id(self):
        store = DocRedirectStore()
        r1 = store.add("/old", "/a")
        r2 = store.add("/old", "/b")
        assert r1.redirect_id != r2.redirect_id


# --------------------------------------------------------------------- Remove
class TestRemove:
    def test_remove_existing(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        assert store.remove(r.redirect_id) is True
        assert store.get(r.redirect_id) is None

    def test_remove_nonexistent(self):
        store = DocRedirectStore()
        assert store.remove("nope") is False

    def test_remove_clears_by_from(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        store.remove(r.redirect_id)
        assert store.resolve("/a") is None

    def test_remove_twice_returns_false(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        store.remove(r.redirect_id)
        assert store.remove(r.redirect_id) is False


# ---------------------------------------------------------- RemoveByFrom
class TestRemoveByFrom:
    def test_remove_by_from_existing(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        assert store.remove_by_from("/a") is True

    def test_remove_by_from_missing(self):
        store = DocRedirectStore()
        assert store.remove_by_from("/missing") is False

    def test_remove_by_from_clears_get(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        store.remove_by_from("/a")
        assert store.get(r.redirect_id) is None

    def test_remove_by_from_clears_resolve(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        store.remove_by_from("/a")
        assert store.resolve("/a") is None


# ---------------------------------------------------------- Enable/Disable
class TestEnableDisable:
    def test_disable_existing(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        assert store.disable(r.redirect_id) is True
        assert store.get(r.redirect_id).enabled is False

    def test_enable_existing(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        store.disable(r.redirect_id)
        assert store.enable(r.redirect_id) is True
        assert store.get(r.redirect_id).enabled is True

    def test_disable_missing(self):
        store = DocRedirectStore()
        assert store.disable("nope") is False

    def test_enable_missing(self):
        store = DocRedirectStore()
        assert store.enable("nope") is False

    def test_disable_then_resolve_returns_none(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        store.disable(r.redirect_id)
        assert store.resolve("/a") is None

    def test_toggle_multiple_times(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        store.disable(r.redirect_id)
        store.enable(r.redirect_id)
        store.disable(r.redirect_id)
        assert store.get(r.redirect_id).enabled is False


# ------------------------------------------------------------------------ Get
class TestGet:
    def test_get_found(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        got = store.get(r.redirect_id)
        assert got is not None
        assert got.from_path == "/a"

    def test_get_missing(self):
        store = DocRedirectStore()
        assert store.get("nope") is None

    def test_get_returns_same_instance(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        got = store.get(r.redirect_id)
        assert got is r


# -------------------------------------------------------------------- Resolve
class TestResolve:
    def test_resolve_returns_target(self):
        store = DocRedirectStore()
        store.add("/old", "/new")
        assert store.resolve("/old") == "/new"

    def test_resolve_missing_returns_none(self):
        store = DocRedirectStore()
        assert store.resolve("/x") is None

    def test_resolve_increments_hit_count(self):
        store = DocRedirectStore()
        r = store.add("/old", "/new")
        store.resolve("/old")
        store.resolve("/old")
        store.resolve("/old")
        assert store.get(r.redirect_id).hit_count == 3

    def test_resolve_disabled_returns_none(self):
        store = DocRedirectStore()
        r = store.add("/old", "/new")
        store.disable(r.redirect_id)
        assert store.resolve("/old") is None

    def test_resolve_disabled_does_not_increment(self):
        store = DocRedirectStore()
        r = store.add("/old", "/new")
        store.disable(r.redirect_id)
        store.resolve("/old")
        assert store.get(r.redirect_id).hit_count == 0


# ----------------------------------------------------------------------- Peek
class TestPeek:
    def test_peek_returns_redirect(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        peeked = store.peek("/a")
        assert peeked is not None
        assert peeked.to_path == "/b"

    def test_peek_missing(self):
        store = DocRedirectStore()
        assert store.peek("/x") is None

    def test_peek_no_hit_increment(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        store.peek("/a")
        store.peek("/a")
        assert store.get(r.redirect_id).hit_count == 0

    def test_peek_works_when_disabled(self):
        store = DocRedirectStore()
        r = store.add("/a", "/b")
        store.disable(r.redirect_id)
        assert store.peek("/a") is not None


# ----------------------------------------------------------- ListRedirects
class TestListRedirects:
    def test_empty(self):
        store = DocRedirectStore()
        assert store.list_redirects() == []

    def test_sorted_by_from_path(self):
        store = DocRedirectStore()
        store.add("/c", "/x")
        store.add("/a", "/x")
        store.add("/b", "/x")
        paths = [r.from_path for r in store.list_redirects()]
        assert paths == ["/a", "/b", "/c"]

    def test_enabled_only_false_includes_disabled(self):
        store = DocRedirectStore()
        r = store.add("/a", "/x")
        store.add("/b", "/y")
        store.disable(r.redirect_id)
        items = store.list_redirects(enabled_only=False)
        assert len(items) == 2

    def test_enabled_only_true_filters(self):
        store = DocRedirectStore()
        r = store.add("/a", "/x")
        store.add("/b", "/y")
        store.disable(r.redirect_id)
        items = store.list_redirects(enabled_only=True)
        assert len(items) == 1
        assert items[0].from_path == "/b"

    def test_enabled_only_still_sorted(self):
        store = DocRedirectStore()
        store.add("/c", "/x")
        store.add("/a", "/x")
        store.add("/b", "/x")
        items = store.list_redirects(enabled_only=True)
        assert [r.from_path for r in items] == ["/a", "/b", "/c"]


# --------------------------------------------------------- TopHitRedirects
class TestTopHitRedirects:
    def test_empty(self):
        store = DocRedirectStore()
        assert store.top_hit_redirects() == []

    def test_sorted_by_hit_count_desc(self):
        store = DocRedirectStore()
        store.add("/a", "/x")
        store.add("/b", "/x")
        store.add("/c", "/x")
        store.resolve("/b")
        store.resolve("/b")
        store.resolve("/c")
        top = store.top_hit_redirects()
        assert top[0].from_path == "/b"
        assert top[1].from_path == "/c"
        assert top[2].from_path == "/a"

    def test_tie_breaker_from_path_asc(self):
        store = DocRedirectStore()
        store.add("/c", "/x")
        store.add("/a", "/x")
        store.add("/b", "/x")
        top = store.top_hit_redirects()
        assert [r.from_path for r in top] == ["/a", "/b", "/c"]

    def test_limit(self):
        store = DocRedirectStore()
        for i in range(5):
            store.add(f"/p{i}", "/x")
        top = store.top_hit_redirects(limit=2)
        assert len(top) == 2

    def test_limit_default(self):
        store = DocRedirectStore()
        for i in range(15):
            store.add(f"/p{i:02d}", "/x")
        top = store.top_hit_redirects()
        assert len(top) == 10

    def test_limit_zero(self):
        store = DocRedirectStore()
        store.add("/a", "/x")
        assert store.top_hit_redirects(limit=0) == []


# ------------------------------------------------------------- ChainResolve
class TestChainResolve:
    def test_single_link(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        assert store.chain_resolve("/a") == "/b"

    def test_two_link_chain(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        store.add("/b", "/c")
        assert store.chain_resolve("/a") == "/c"

    def test_three_link_chain(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        store.add("/b", "/c")
        store.add("/c", "/d")
        assert store.chain_resolve("/a") == "/d"

    def test_no_starting_redirect_returns_none(self):
        store = DocRedirectStore()
        assert store.chain_resolve("/missing") is None

    def test_max_hops_limit(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        store.add("/b", "/c")
        store.add("/c", "/d")
        result = store.chain_resolve("/a", max_hops=2)
        # Two hops applied; final reached is /c
        assert result == "/c"

    def test_max_hops_zero(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        assert store.chain_resolve("/a", max_hops=0) is None

    def test_cycle_detection(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        store.add("/b", "/a")
        assert store.chain_resolve("/a") is None

    def test_cycle_three_nodes(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        store.add("/b", "/c")
        store.add("/c", "/a")
        assert store.chain_resolve("/a") is None

    def test_chain_increments_hits(self):
        store = DocRedirectStore()
        r1 = store.add("/a", "/b")
        r2 = store.add("/b", "/c")
        store.chain_resolve("/a")
        assert store.get(r1.redirect_id).hit_count == 1
        assert store.get(r2.redirect_id).hit_count == 1

    def test_chain_stops_at_disabled(self):
        store = DocRedirectStore()
        store.add("/a", "/b")
        r2 = store.add("/b", "/c")
        store.disable(r2.redirect_id)
        # First hop succeeds -> /b; second is disabled, stop.
        assert store.chain_resolve("/a") == "/b"


# ---------------------------------------------------------------------- Clear
class TestClear:
    def test_clear_empty_returns_zero(self):
        store = DocRedirectStore()
        assert store.clear() == 0

    def test_clear_returns_count(self):
        store = DocRedirectStore()
        store.add("/a", "/x")
        store.add("/b", "/x")
        store.add("/c", "/x")
        assert store.clear() == 3

    def test_clear_empties_store(self):
        store = DocRedirectStore()
        store.add("/a", "/x")
        store.add("/b", "/x")
        store.clear()
        assert store.list_redirects() == []
        assert store.resolve("/a") is None


# ---------------------------------------------------------------------- Stats
class TestStats:
    def test_stats_empty(self):
        store = DocRedirectStore()
        s = store.stats()
        assert s == RedirectStats(0, 0, 0)

    def test_stats_counts(self):
        store = DocRedirectStore()
        store.add("/a", "/x")
        store.add("/b", "/x")
        s = store.stats()
        assert s.total_redirects == 2
        assert s.enabled_redirects == 2

    def test_stats_enabled_filtered(self):
        store = DocRedirectStore()
        r = store.add("/a", "/x")
        store.add("/b", "/x")
        store.disable(r.redirect_id)
        s = store.stats()
        assert s.total_redirects == 2
        assert s.enabled_redirects == 1

    def test_stats_total_hits(self):
        store = DocRedirectStore()
        store.add("/a", "/x")
        store.add("/b", "/y")
        store.resolve("/a")
        store.resolve("/a")
        store.resolve("/b")
        s = store.stats()
        assert s.total_hits == 3


# -------------------------------------------------------------- ThreadSafety
class TestThreadSafety:
    def test_concurrent_add(self):
        store = DocRedirectStore()

        def worker(start: int):
            for i in range(50):
                store.add(f"/p{start}_{i}", "/x")

        threads = [
            threading.Thread(target=worker, args=(t,)) for t in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(store.list_redirects()) == 8 * 50

    def test_concurrent_add_and_resolve(self):
        store = DocRedirectStore()
        for i in range(20):
            store.add(f"/p{i}", "/x")

        def adder():
            for i in range(50):
                store.add(f"/add_{i}", "/x")

        def resolver():
            for _ in range(100):
                for i in range(20):
                    store.resolve(f"/p{i}")

        threads = [
            threading.Thread(target=adder),
            threading.Thread(target=resolver),
            threading.Thread(target=resolver),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Each /p{i} resolved 200 times total
        for i in range(20):
            r = store.peek(f"/p{i}")
            assert r.hit_count == 200

    def test_concurrent_add_same_from_path(self):
        store = DocRedirectStore()

        def worker():
            for _ in range(100):
                store.add("/contended", "/x")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Only one redirect should exist for the contended path
        items = store.list_redirects()
        assert len(items) == 1
        assert items[0].from_path == "/contended"


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
