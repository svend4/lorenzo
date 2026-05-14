"""Tests for E228 doc_redirect module."""
from __future__ import annotations

import pytest

from docstoolkit.doc_redirect import (
    DocRedirect,
    Redirect,
    RedirectStats,
    RedirectType,
    ResolutionPath,
)


# ---------------------------------------------------------------------------
# TestRedirectType
# ---------------------------------------------------------------------------


class TestRedirectType:
    def test_permanent_value(self):
        assert RedirectType.PERMANENT_301.value == "permanent_301"

    def test_temporary_value(self):
        assert RedirectType.TEMPORARY_302.value == "temporary_302"

    def test_internal_value(self):
        assert RedirectType.INTERNAL_307.value == "internal_307"

    def test_gone_value(self):
        assert RedirectType.GONE_410.value == "gone_410"

    def test_distinct_members(self):
        assert len(set(RedirectType)) == 4


# ---------------------------------------------------------------------------
# TestRedirect
# ---------------------------------------------------------------------------


class TestRedirect:
    def test_basic_construction(self):
        r = Redirect(source="a", target="b")
        assert r.source == "a"
        assert r.target == "b"

    def test_default_redirect_type(self):
        r = Redirect(source="a", target="b")
        assert r.redirect_type == RedirectType.PERMANENT_301

    def test_default_created_at(self):
        r = Redirect(source="a", target="b")
        assert r.created_at == 0.0

    def test_default_last_used(self):
        r = Redirect(source="a", target="b")
        assert r.last_used is None

    def test_default_hit_count(self):
        r = Redirect(source="a", target="b")
        assert r.hit_count == 0

    def test_custom_fields(self):
        r = Redirect(
            source="x", target="y", redirect_type=RedirectType.GONE_410, created_at=10.0
        )
        assert r.redirect_type == RedirectType.GONE_410
        assert r.created_at == 10.0


# ---------------------------------------------------------------------------
# TestRedirectStats
# ---------------------------------------------------------------------------


class TestRedirectStats:
    def test_construction(self):
        s = RedirectStats(
            total_redirects=2,
            by_type={"permanent_301": 2},
            total_hits=5,
            top_hit=None,
            unused_count=0,
        )
        assert s.total_redirects == 2
        assert s.total_hits == 5


# ---------------------------------------------------------------------------
# TestResolutionPath
# ---------------------------------------------------------------------------


class TestResolutionPath:
    def test_construction(self):
        p = ResolutionPath(source="a", final="b")
        assert p.source == "a"
        assert p.final == "b"

    def test_default_chain(self):
        p = ResolutionPath(source="a", final="b")
        assert p.chain == []

    def test_default_had_loop(self):
        p = ResolutionPath(source="a", final="b")
        assert p.had_loop is False
        assert p.loop_at is None


# ---------------------------------------------------------------------------
# TestAddRedirect
# ---------------------------------------------------------------------------


class TestAddRedirect:
    def test_add_basic(self):
        dr = DocRedirect()
        r = dr.add_redirect("a", "b")
        assert r.source == "a"
        assert r.target == "b"

    def test_add_returns_redirect(self):
        dr = DocRedirect()
        r = dr.add_redirect("a", "b")
        assert isinstance(r, Redirect)

    def test_add_increments_total(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("c", "d")
        assert dr.total_redirects == 2

    def test_add_with_type(self):
        dr = DocRedirect()
        r = dr.add_redirect("a", "b", redirect_type=RedirectType.TEMPORARY_302)
        assert r.redirect_type == RedirectType.TEMPORARY_302

    def test_add_with_now(self):
        dr = DocRedirect()
        r = dr.add_redirect("a", "b", now=123.0)
        assert r.created_at == 123.0

    def test_add_self_redirect_raises(self):
        dr = DocRedirect()
        with pytest.raises(ValueError):
            dr.add_redirect("a", "a")

    def test_add_overwrites(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("a", "c")
        assert dr.lookup("a").target == "c"
        assert dr.total_redirects == 1


# ---------------------------------------------------------------------------
# TestRemoveRedirect
# ---------------------------------------------------------------------------


class TestRemoveRedirect:
    def test_remove_existing(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        assert dr.remove_redirect("a") is True

    def test_remove_missing(self):
        dr = DocRedirect()
        assert dr.remove_redirect("nope") is False

    def test_remove_decrements_total(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.remove_redirect("a")
        assert dr.total_redirects == 0


# ---------------------------------------------------------------------------
# TestUpdateRedirect
# ---------------------------------------------------------------------------


class TestUpdateRedirect:
    def test_update_target(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        assert dr.update_redirect("a", target="c") is True
        assert dr.lookup("a").target == "c"

    def test_update_type(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.update_redirect("a", redirect_type=RedirectType.GONE_410)
        assert dr.lookup("a").redirect_type == RedirectType.GONE_410

    def test_update_missing(self):
        dr = DocRedirect()
        assert dr.update_redirect("nope", target="x") is False

    def test_update_self_raises(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        with pytest.raises(ValueError):
            dr.update_redirect("a", target="a")


# ---------------------------------------------------------------------------
# TestResolveDirect
# ---------------------------------------------------------------------------


class TestResolveDirect:
    def test_resolve_simple(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        path = dr.resolve("a")
        assert path.final == "b"

    def test_resolve_chain_length_one(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        path = dr.resolve("a")
        assert len(path.chain) == 1

    def test_resolve_source_preserved(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        path = dr.resolve("a")
        assert path.source == "a"

    def test_resolve_increments_hit_count(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.resolve("a")
        assert dr.lookup("a").hit_count == 1

    def test_resolve_records_last_used(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.resolve("a", now=99.0)
        assert dr.lookup("a").last_used == 99.0

    def test_resolve_no_follow(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "c")
        path = dr.resolve("a", follow_chain=False)
        assert path.final == "b"
        assert len(path.chain) == 1


# ---------------------------------------------------------------------------
# TestResolveChain
# ---------------------------------------------------------------------------


class TestResolveChain:
    def test_resolve_two_hops(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "c")
        path = dr.resolve("a")
        assert path.final == "c"
        assert len(path.chain) == 2

    def test_resolve_three_hops(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "c")
        dr.add_redirect("c", "d")
        path = dr.resolve("a")
        assert path.final == "d"
        assert len(path.chain) == 3

    def test_resolve_chain_no_loop(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "c")
        path = dr.resolve("a")
        assert path.had_loop is False

    def test_resolve_gone_410_terminates(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b", redirect_type=RedirectType.GONE_410)
        dr.add_redirect("b", "c")
        path = dr.resolve("a")
        # 410 is terminal — chain stops at the gone redirect.
        assert path.final == "b"
        assert len(path.chain) == 1


# ---------------------------------------------------------------------------
# TestResolveLoop
# ---------------------------------------------------------------------------


class TestResolveLoop:
    def test_simple_loop_flagged(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "a")
        path = dr.resolve("a")
        assert path.had_loop is True

    def test_loop_at_set(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "a")
        path = dr.resolve("a")
        assert path.loop_at is not None

    def test_self_loop_blocked_on_add(self):
        dr = DocRedirect()
        with pytest.raises(ValueError):
            dr.add_redirect("a", "a")

    def test_three_node_loop(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "c")
        dr.add_redirect("c", "a")
        path = dr.resolve("a")
        assert path.had_loop is True


# ---------------------------------------------------------------------------
# TestResolveNotFound
# ---------------------------------------------------------------------------


class TestResolveNotFound:
    def test_resolve_missing(self):
        dr = DocRedirect()
        path = dr.resolve("nope")
        assert path.final == "nope"

    def test_resolve_missing_empty_chain(self):
        dr = DocRedirect()
        path = dr.resolve("nope")
        assert path.chain == []

    def test_resolve_missing_no_loop(self):
        dr = DocRedirect()
        path = dr.resolve("nope")
        assert path.had_loop is False


# ---------------------------------------------------------------------------
# TestLookup
# ---------------------------------------------------------------------------


class TestLookup:
    def test_lookup_found(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        assert dr.lookup("a") is not None

    def test_lookup_missing(self):
        dr = DocRedirect()
        assert dr.lookup("nope") is None

    def test_lookup_does_not_increment_hits(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.lookup("a")
        assert dr.lookup("a").hit_count == 0


# ---------------------------------------------------------------------------
# TestTargetsTo
# ---------------------------------------------------------------------------


class TestTargetsTo:
    def test_targets_to_one(self):
        dr = DocRedirect()
        dr.add_redirect("a", "z")
        assert len(dr.targets_to("z")) == 1

    def test_targets_to_multiple(self):
        dr = DocRedirect()
        dr.add_redirect("a", "z")
        dr.add_redirect("b", "z")
        dr.add_redirect("c", "z")
        assert len(dr.targets_to("z")) == 3

    def test_targets_to_none(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        assert dr.targets_to("nope") == []


# ---------------------------------------------------------------------------
# TestRedirectsFromPattern
# ---------------------------------------------------------------------------


class TestRedirectsFromPattern:
    def test_pattern_match(self):
        dr = DocRedirect()
        dr.add_redirect("docs/old/a", "docs/new/a")
        dr.add_redirect("docs/old/b", "docs/new/b")
        dr.add_redirect("api/v1/x", "api/v2/x")
        matches = dr.redirects_from_pattern(r"docs/old")
        assert len(matches) == 2

    def test_pattern_match_none(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        assert dr.redirects_from_pattern(r"^xyz") == []

    def test_pattern_regex(self):
        dr = DocRedirect()
        dr.add_redirect("v1-foo", "v2-foo")
        dr.add_redirect("v1-bar", "v2-bar")
        matches = dr.redirects_from_pattern(r"^v1-")
        assert len(matches) == 2


# ---------------------------------------------------------------------------
# TestDetectLoops
# ---------------------------------------------------------------------------


class TestDetectLoops:
    def test_no_loop(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "c")
        assert dr.detect_loops() == []

    def test_simple_loop(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "a")
        loops = dr.detect_loops()
        assert len(loops) == 1
        assert set(loops[0]) == {"a", "b"}

    def test_three_cycle(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "c")
        dr.add_redirect("c", "a")
        loops = dr.detect_loops()
        assert len(loops) == 1
        assert set(loops[0]) == {"a", "b", "c"}

    def test_no_duplicate_loops(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "a")
        # Both "a" and "b" lead to the same cycle — should report once.
        loops = dr.detect_loops()
        assert len(loops) == 1


# ---------------------------------------------------------------------------
# TestHasLoop
# ---------------------------------------------------------------------------


class TestHasLoop:
    def test_has_loop_true(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "a")
        assert dr.has_loop("a") is True

    def test_has_loop_false(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        assert dr.has_loop("a") is False

    def test_has_loop_unknown(self):
        dr = DocRedirect()
        assert dr.has_loop("nope") is False


# ---------------------------------------------------------------------------
# TestChainLength
# ---------------------------------------------------------------------------


class TestChainLength:
    def test_chain_length_zero(self):
        dr = DocRedirect()
        assert dr.chain_length("nope") == 0

    def test_chain_length_one(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        assert dr.chain_length("a") == 1

    def test_chain_length_three(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "c")
        dr.add_redirect("c", "d")
        assert dr.chain_length("a") == 3

    def test_chain_length_loop(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "a")
        assert dr.chain_length("a") == -1


# ---------------------------------------------------------------------------
# TestTrackHit
# ---------------------------------------------------------------------------


class TestTrackHit:
    def test_track_hit_success(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        assert dr.track_hit("a") is True

    def test_track_hit_increments(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.track_hit("a")
        dr.track_hit("a")
        assert dr.lookup("a").hit_count == 2

    def test_track_hit_records_time(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.track_hit("a", now=42.0)
        assert dr.lookup("a").last_used == 42.0

    def test_track_hit_missing(self):
        dr = DocRedirect()
        assert dr.track_hit("nope") is False


# ---------------------------------------------------------------------------
# TestCleanupUnused
# ---------------------------------------------------------------------------


class TestCleanupUnused:
    def test_cleanup_unused_all(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("c", "d")
        removed = dr.cleanup_unused()
        assert removed == 2
        assert dr.total_redirects == 0

    def test_cleanup_keeps_used(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("c", "d")
        dr.track_hit("a")
        dr.cleanup_unused()
        assert dr.lookup("a") is not None
        assert dr.lookup("c") is None

    def test_cleanup_min_hits(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.track_hit("a")
        removed = dr.cleanup_unused(min_hits=2)
        assert removed == 1


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------


class TestStats:
    def test_stats_empty(self):
        dr = DocRedirect()
        s = dr.stats()
        assert s.total_redirects == 0
        assert s.total_hits == 0
        assert s.top_hit is None

    def test_stats_by_type(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("c", "d", redirect_type=RedirectType.GONE_410)
        s = dr.stats()
        assert s.by_type["permanent_301"] == 1
        assert s.by_type["gone_410"] == 1

    def test_stats_total_hits(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.track_hit("a")
        dr.track_hit("a")
        s = dr.stats()
        assert s.total_hits == 2

    def test_stats_top_hit(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("c", "d")
        dr.track_hit("a")
        dr.track_hit("a")
        dr.track_hit("c")
        s = dr.stats()
        assert s.top_hit is not None
        assert s.top_hit.source == "a"

    def test_stats_unused_count(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("c", "d")
        dr.track_hit("a")
        s = dr.stats()
        assert s.unused_count == 1


# ---------------------------------------------------------------------------
# TestFindTerminals
# ---------------------------------------------------------------------------


class TestFindTerminals:
    def test_find_terminals_no_redirect(self):
        dr = DocRedirect()
        assert dr.find_terminals("x") == "x"

    def test_find_terminals_single(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        assert dr.find_terminals("a") == "b"

    def test_find_terminals_chain(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "c")
        dr.add_redirect("c", "d")
        assert dr.find_terminals("a") == "d"

    def test_find_terminals_gone(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b", redirect_type=RedirectType.GONE_410)
        dr.add_redirect("b", "c")
        assert dr.find_terminals("a") == "b"

    def test_find_terminals_loop(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("b", "a")
        # Last target before re-encountering "a" was "a" (b -> a), so final stored.
        result = dr.find_terminals("a")
        assert result in {"a", "b"}


# ---------------------------------------------------------------------------
# TestClear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_empties_store(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.add_redirect("c", "d")
        dr.clear()
        assert dr.total_redirects == 0

    def test_clear_empty(self):
        dr = DocRedirect()
        dr.clear()
        assert dr.total_redirects == 0


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_total_redirects_property(self):
        dr = DocRedirect()
        assert dr.total_redirects == 0
        dr.add_redirect("a", "b")
        assert dr.total_redirects == 1

    def test_resolve_deep_chain_within_depth(self):
        dr = DocRedirect()
        # Build chain of length 20
        for i in range(20):
            dr.add_redirect(f"n{i}", f"n{i + 1}")
        path = dr.resolve("n0")
        assert path.final == "n20"
        assert len(path.chain) == 20

    def test_resolve_chain_exceeds_max_depth(self):
        dr = DocRedirect()
        # Build chain longer than _MAX_DEPTH = 32
        for i in range(40):
            dr.add_redirect(f"n{i}", f"n{i + 1}")
        path = dr.resolve("n0")
        # Should stop at MAX_DEPTH (32 hops)
        assert len(path.chain) <= 32

    def test_overwrite_resets_hit_count(self):
        dr = DocRedirect()
        dr.add_redirect("a", "b")
        dr.track_hit("a")
        dr.add_redirect("a", "c")
        # New redirect — fresh state.
        assert dr.lookup("a").hit_count == 0

    def test_multiple_redirects_to_same_target(self):
        dr = DocRedirect()
        dr.add_redirect("a", "z")
        dr.add_redirect("b", "z")
        targets = dr.targets_to("z")
        sources = {r.source for r in targets}
        assert sources == {"a", "b"}
