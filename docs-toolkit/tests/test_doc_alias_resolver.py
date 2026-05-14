"""Tests for ``docstoolkit.doc_alias_resolver``."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_alias_resolver import (
    DocAlias,
    DocAliasResolver,
    ResolutionStats,
)


# ---------------------------------------------------------------------------
# TestDocAliasDataclass
# ---------------------------------------------------------------------------
class TestDocAliasDataclass:
    def test_construct_with_defaults(self):
        a = DocAlias(alias="a1", target="doc-1")
        assert a.alias == "a1"
        assert a.target == "doc-1"
        assert a.created_at == 0.0

    def test_construct_with_timestamp(self):
        a = DocAlias(alias="a1", target="doc-1", created_at=123.5)
        assert a.created_at == 123.5

    def test_equality(self):
        a = DocAlias(alias="x", target="y", created_at=1.0)
        b = DocAlias(alias="x", target="y", created_at=1.0)
        assert a == b

    def test_inequality_on_target(self):
        a = DocAlias(alias="x", target="y")
        b = DocAlias(alias="x", target="z")
        assert a != b


# ---------------------------------------------------------------------------
# TestResolutionStatsDataclass
# ---------------------------------------------------------------------------
class TestResolutionStatsDataclass:
    def test_fields(self):
        s = ResolutionStats(
            total_aliases=2,
            unique_targets=1,
            total_resolutions=10,
            cache_hits=5,
        )
        assert s.total_aliases == 2
        assert s.unique_targets == 1
        assert s.total_resolutions == 10
        assert s.cache_hits == 5

    def test_equality(self):
        a = ResolutionStats(1, 1, 1, 1)
        b = ResolutionStats(1, 1, 1, 1)
        assert a == b


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_resolver(self):
        r = DocAliasResolver()
        assert r.list_aliases() == []

    def test_initial_stats(self):
        r = DocAliasResolver()
        s = r.stats()
        assert s.total_aliases == 0
        assert s.unique_targets == 0
        assert s.total_resolutions == 0
        assert s.cache_hits == 0

    def test_resolve_unregistered_does_not_raise(self):
        r = DocAliasResolver()
        assert r.resolve("nope") == "nope"


# ---------------------------------------------------------------------------
# TestRegisterAlias
# ---------------------------------------------------------------------------
class TestRegisterAlias:
    def test_register_returns_dataclass(self):
        r = DocAliasResolver()
        entry = r.register_alias("a", "doc-1", now=100.0)
        assert isinstance(entry, DocAlias)
        assert entry.alias == "a"
        assert entry.target == "doc-1"
        assert entry.created_at == 100.0

    def test_register_uses_time_when_now_omitted(self):
        r = DocAliasResolver()
        entry = r.register_alias("a", "doc-1")
        assert entry.created_at > 0.0

    def test_register_stores_alias(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        assert r.get_alias("a").target == "doc-1"

    def test_register_replaces_existing(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1", now=1.0)
        r.register_alias("a", "doc-2", now=2.0)
        got = r.get_alias("a")
        assert got.target == "doc-2"
        assert got.created_at == 2.0

    def test_register_invalidates_cache(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        # populate cache
        r.resolve("a")
        assert r.stats().cache_hits == 0
        r.resolve("a")
        assert r.stats().cache_hits == 1
        # replace -> cache wiped
        r.register_alias("a", "doc-2")
        r.resolve("a")
        assert r.stats().cache_hits == 1  # still 1, not 2

    def test_register_many_distinct(self):
        r = DocAliasResolver()
        for i in range(5):
            r.register_alias(f"a{i}", f"doc-{i}")
        assert r.stats().total_aliases == 5


# ---------------------------------------------------------------------------
# TestUnregisterAlias
# ---------------------------------------------------------------------------
class TestUnregisterAlias:
    def test_unregister_existing_returns_true(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        assert r.unregister_alias("a") is True

    def test_unregister_missing_returns_false(self):
        r = DocAliasResolver()
        assert r.unregister_alias("ghost") is False

    def test_unregister_removes(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.unregister_alias("a")
        assert r.get_alias("a") is None

    def test_unregister_invalidates_cache(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.resolve("a")
        r.unregister_alias("a")
        # cache cleared -> hits unchanged on a fresh path
        assert r.stats().cache_hits == 0


# ---------------------------------------------------------------------------
# TestGetAlias
# ---------------------------------------------------------------------------
class TestGetAlias:
    def test_returns_none_for_unknown(self):
        r = DocAliasResolver()
        assert r.get_alias("x") is None

    def test_returns_entry(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        entry = r.get_alias("a")
        assert entry is not None
        assert entry.target == "doc-1"


# ---------------------------------------------------------------------------
# TestResolve
# ---------------------------------------------------------------------------
class TestResolve:
    def test_resolve_direct(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        assert r.resolve("a") == "doc-1"

    def test_resolve_chain(self):
        r = DocAliasResolver()
        r.register_alias("a", "b")
        r.register_alias("b", "c")
        r.register_alias("c", "doc-final")
        assert r.resolve("a") == "doc-final"

    def test_resolve_chain_two_hops(self):
        r = DocAliasResolver()
        r.register_alias("a", "b")
        r.register_alias("b", "doc-x")
        assert r.resolve("a") == "doc-x"

    def test_resolve_unregistered_returns_itself(self):
        r = DocAliasResolver()
        assert r.resolve("not-registered") == "not-registered"

    def test_resolve_terminal_target_not_an_alias(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        # "doc-1" is not registered as alias, so it is canonical.
        assert r.resolve("a") == "doc-1"

    def test_resolve_increments_counter(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.resolve("a")
        r.resolve("a")
        assert r.stats().total_resolutions == 2


# ---------------------------------------------------------------------------
# TestResolveCycle
# ---------------------------------------------------------------------------
class TestResolveCycle:
    def test_self_loop_returns_none(self):
        r = DocAliasResolver()
        r.register_alias("a", "a")
        assert r.resolve("a") is None

    def test_two_node_cycle_returns_none(self):
        r = DocAliasResolver()
        r.register_alias("a", "b")
        r.register_alias("b", "a")
        assert r.resolve("a") is None

    def test_three_node_cycle_returns_none(self):
        r = DocAliasResolver()
        r.register_alias("a", "b")
        r.register_alias("b", "c")
        r.register_alias("c", "a")
        assert r.resolve("a") is None

    def test_cycle_not_cached(self):
        r = DocAliasResolver()
        r.register_alias("a", "a")
        r.resolve("a")
        # cycle returned None, so no cache hit on second pass either
        r.resolve("a")
        assert r.stats().cache_hits == 0


# ---------------------------------------------------------------------------
# TestResolveMaxHops
# ---------------------------------------------------------------------------
class TestResolveMaxHops:
    def test_max_hops_exceeded_returns_none(self):
        r = DocAliasResolver()
        # 5-step chain: a -> b -> c -> d -> e -> doc
        r.register_alias("a", "b")
        r.register_alias("b", "c")
        r.register_alias("c", "d")
        r.register_alias("d", "e")
        r.register_alias("e", "doc")
        assert r.resolve("a", max_hops=2) is None

    def test_max_hops_exactly_sufficient(self):
        r = DocAliasResolver()
        r.register_alias("a", "b")
        r.register_alias("b", "doc-x")
        assert r.resolve("a", max_hops=2) == "doc-x"

    def test_max_hops_zero_for_single_alias(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        # hops budget too small to even traverse the first alias step
        assert r.resolve("a", max_hops=0) is None


# ---------------------------------------------------------------------------
# TestResolveCaches
# ---------------------------------------------------------------------------
class TestResolveCaches:
    def test_second_resolve_hits_cache(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.resolve("a")
        r.resolve("a")
        assert r.stats().cache_hits == 1

    def test_many_hits(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        for _ in range(10):
            r.resolve("a")
        # 10 calls: first miss, 9 hits
        assert r.stats().cache_hits == 9

    def test_cache_per_alias(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.register_alias("b", "doc-2")
        r.resolve("a")
        r.resolve("b")
        r.resolve("a")
        r.resolve("b")
        assert r.stats().cache_hits == 2

    def test_chain_cached(self):
        r = DocAliasResolver()
        r.register_alias("a", "b")
        r.register_alias("b", "doc-x")
        r.resolve("a")
        r.resolve("a")
        assert r.stats().cache_hits == 1


# ---------------------------------------------------------------------------
# TestResolveStrict
# ---------------------------------------------------------------------------
class TestResolveStrict:
    def test_strict_returns_none_for_unregistered(self):
        r = DocAliasResolver()
        assert r.resolve_strict("nope") is None

    def test_strict_resolves_registered(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        assert r.resolve_strict("a") == "doc-1"

    def test_strict_resolves_chain(self):
        r = DocAliasResolver()
        r.register_alias("a", "b")
        r.register_alias("b", "doc-x")
        assert r.resolve_strict("a") == "doc-x"

    def test_strict_cycle_returns_none(self):
        r = DocAliasResolver()
        r.register_alias("a", "b")
        r.register_alias("b", "a")
        assert r.resolve_strict("a") is None


# ---------------------------------------------------------------------------
# TestAliasesFor
# ---------------------------------------------------------------------------
class TestAliasesFor:
    def test_no_aliases(self):
        r = DocAliasResolver()
        assert r.aliases_for("doc-1") == []

    def test_returns_sorted(self):
        r = DocAliasResolver()
        r.register_alias("zeta", "doc-1")
        r.register_alias("alpha", "doc-1")
        r.register_alias("mu", "doc-1")
        assert r.aliases_for("doc-1") == ["alpha", "mu", "zeta"]

    def test_only_direct_target(self):
        r = DocAliasResolver()
        r.register_alias("a", "b")  # immediate target is "b", not "doc-1"
        r.register_alias("b", "doc-1")
        # "a" does NOT directly point at "doc-1"
        assert r.aliases_for("doc-1") == ["b"]

    def test_unrelated_target(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        assert r.aliases_for("doc-other") == []


# ---------------------------------------------------------------------------
# TestListAliases
# ---------------------------------------------------------------------------
class TestListAliases:
    def test_empty(self):
        r = DocAliasResolver()
        assert r.list_aliases() == []

    def test_sorted_by_alias(self):
        r = DocAliasResolver()
        r.register_alias("zeta", "z")
        r.register_alias("alpha", "a")
        r.register_alias("mu", "m")
        names = [e.alias for e in r.list_aliases()]
        assert names == ["alpha", "mu", "zeta"]

    def test_returns_dataclass_entries(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        out = r.list_aliases()
        assert len(out) == 1
        assert isinstance(out[0], DocAlias)
        assert out[0].target == "doc-1"


# ---------------------------------------------------------------------------
# TestClearCache
# ---------------------------------------------------------------------------
class TestClearCache:
    def test_returns_zero_when_empty(self):
        r = DocAliasResolver()
        assert r.clear_cache() == 0

    def test_returns_count_after_resolves(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.register_alias("b", "doc-2")
        r.resolve("a")
        r.resolve("b")
        assert r.clear_cache() == 2

    def test_does_not_remove_aliases(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.resolve("a")
        r.clear_cache()
        assert r.get_alias("a") is not None

    def test_after_clear_cache_misses_again(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.resolve("a")
        r.clear_cache()
        r.resolve("a")
        # only one hit possible after a fresh miss
        assert r.stats().cache_hits == 0


# ---------------------------------------------------------------------------
# TestClearAll
# ---------------------------------------------------------------------------
class TestClearAll:
    def test_returns_zero_when_empty(self):
        r = DocAliasResolver()
        assert r.clear_all() == 0

    def test_returns_count(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.register_alias("b", "doc-2")
        r.register_alias("c", "doc-3")
        assert r.clear_all() == 3

    def test_removes_all_aliases(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.register_alias("b", "doc-2")
        r.clear_all()
        assert r.list_aliases() == []

    def test_also_clears_cache(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.resolve("a")
        r.clear_all()
        # no aliases left, no cache entries either
        assert r.clear_cache() == 0


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty_stats(self):
        r = DocAliasResolver()
        s = r.stats()
        assert s == ResolutionStats(0, 0, 0, 0)

    def test_counts_aliases_and_targets(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.register_alias("b", "doc-1")
        r.register_alias("c", "doc-2")
        s = r.stats()
        assert s.total_aliases == 3
        assert s.unique_targets == 2

    def test_counts_resolutions(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.resolve("a")
        r.resolve("a")
        r.resolve("a")
        s = r.stats()
        assert s.total_resolutions == 3
        assert s.cache_hits == 2

    def test_counts_unregistered_resolution_attempt(self):
        r = DocAliasResolver()
        r.resolve("nope")
        assert r.stats().total_resolutions == 1

    def test_unique_targets_after_replace(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        r.register_alias("a", "doc-2")
        s = r.stats()
        assert s.total_aliases == 1
        assert s.unique_targets == 1


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_register(self):
        r = DocAliasResolver()
        n_threads = 8
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                r.register_alias(f"t{tid}-a{i}", f"doc-{tid}-{i}")

        threads = [
            threading.Thread(target=worker, args=(tid,)) for tid in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = r.stats()
        assert s.total_aliases == n_threads * per_thread

    def test_concurrent_register_and_resolve(self):
        r = DocAliasResolver()
        r.register_alias("a", "doc-1")
        errors: list[BaseException] = []

        def reg_worker() -> None:
            try:
                for i in range(100):
                    r.register_alias(f"k{i}", f"doc-{i}")
            except BaseException as e:  # pragma: no cover - safety net
                errors.append(e)

        def res_worker() -> None:
            try:
                for _ in range(100):
                    r.resolve("a")
            except BaseException as e:  # pragma: no cover - safety net
                errors.append(e)

        threads = [
            threading.Thread(target=reg_worker),
            threading.Thread(target=res_worker),
            threading.Thread(target=reg_worker),
            threading.Thread(target=res_worker),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        # The two res_workers performed 100 resolves each.
        assert r.stats().total_resolutions >= 200
