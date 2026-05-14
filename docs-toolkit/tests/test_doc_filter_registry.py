"""Tests for ``docstoolkit.doc_filter_registry``."""

from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_filter_registry import (
    DocFilterRegistry,
    FilterStats,
    SavedFilter,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
T0 = 1_000_000.0  # deterministic "now"


def make_registry() -> DocFilterRegistry:
    return DocFilterRegistry()


# ---------------------------------------------------------------------------
# TestSavedFilterDataclass
# ---------------------------------------------------------------------------
class TestSavedFilterDataclass:
    def test_required_fields(self):
        flt = SavedFilter(filter_id="f1", name="N", owner="u1")
        assert flt.filter_id == "f1"
        assert flt.name == "N"
        assert flt.owner == "u1"

    def test_query_defaults_to_empty_dict(self):
        flt = SavedFilter(filter_id="f1", name="N", owner="u1")
        assert flt.query == {}

    def test_query_default_is_per_instance(self):
        a = SavedFilter(filter_id="a", name="A", owner="u")
        b = SavedFilter(filter_id="b", name="B", owner="u")
        a.query["k"] = 1
        assert b.query == {}

    def test_created_at_default(self):
        flt = SavedFilter(filter_id="f1", name="N", owner="u")
        assert flt.created_at == 0.0

    def test_updated_at_default(self):
        flt = SavedFilter(filter_id="f1", name="N", owner="u")
        assert flt.updated_at == 0.0

    def test_shared_default_is_false(self):
        flt = SavedFilter(filter_id="f1", name="N", owner="u")
        assert flt.shared is False

    def test_use_count_default_is_zero(self):
        flt = SavedFilter(filter_id="f1", name="N", owner="u")
        assert flt.use_count == 0

    def test_explicit_field_values(self):
        flt = SavedFilter(
            filter_id="f1",
            name="N",
            owner="u",
            query={"tag": "x"},
            created_at=1.0,
            updated_at=2.0,
            shared=True,
            use_count=5,
        )
        assert flt.query == {"tag": "x"}
        assert flt.created_at == 1.0
        assert flt.updated_at == 2.0
        assert flt.shared is True
        assert flt.use_count == 5


# ---------------------------------------------------------------------------
# TestFilterStatsDataclass
# ---------------------------------------------------------------------------
class TestFilterStatsDataclass:
    def test_constructs_with_all_fields(self):
        s = FilterStats(
            total_filters=3,
            shared_filters=1,
            unique_owners=2,
            total_uses=10,
        )
        assert s.total_filters == 3
        assert s.shared_filters == 1
        assert s.unique_owners == 2
        assert s.total_uses == 10

    def test_equality(self):
        a = FilterStats(1, 1, 1, 1)
        b = FilterStats(1, 1, 1, 1)
        assert a == b

    def test_inequality(self):
        a = FilterStats(1, 1, 1, 1)
        b = FilterStats(2, 1, 1, 1)
        assert a != b


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_construct_empty(self):
        reg = DocFilterRegistry()
        assert reg.stats() == FilterStats(0, 0, 0, 0)

    def test_independent_instances(self):
        a = DocFilterRegistry()
        b = DocFilterRegistry()
        a.save_filter("f", "u", {})
        assert b.stats().total_filters == 0


# ---------------------------------------------------------------------------
# TestSaveFilter
# ---------------------------------------------------------------------------
class TestSaveFilter:
    def test_returns_saved_filter(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u1", {"x": 1}, now=T0)
        assert isinstance(flt, SavedFilter)

    def test_assigns_uuid(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u1", {}, now=T0)
        # parses as a UUID
        uuid.UUID(flt.filter_id)

    def test_unique_ids(self):
        reg = make_registry()
        ids = {reg.save_filter("F", "u", {}, now=T0).filter_id for _ in range(20)}
        assert len(ids) == 20

    def test_sets_created_and_updated_at(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u1", {}, now=T0)
        assert flt.created_at == T0
        assert flt.updated_at == T0

    def test_defaults_shared_false(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u1", {}, now=T0)
        assert flt.shared is False

    def test_respects_shared_true(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u1", {}, shared=True, now=T0)
        assert flt.shared is True

    def test_query_stored(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u1", {"tag": "v"}, now=T0)
        assert flt.query == {"tag": "v"}

    def test_query_is_copied(self):
        reg = make_registry()
        q = {"tag": "v"}
        flt = reg.save_filter("F", "u1", q, now=T0)
        q["tag"] = "MUTATED"
        assert flt.query == {"tag": "v"}

    def test_persists_in_registry(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u1", {}, now=T0)
        assert reg.get_filter(flt.filter_id) is flt

    def test_use_count_starts_zero(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u1", {}, now=T0)
        assert flt.use_count == 0

    def test_now_defaults_to_time(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u1", {})
        assert flt.created_at > 0.0


# ---------------------------------------------------------------------------
# TestUpdateFilter
# ---------------------------------------------------------------------------
class TestUpdateFilter:
    def test_returns_none_when_missing(self):
        reg = make_registry()
        assert reg.update_filter("nope") is None

    def test_updates_name(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        out = reg.update_filter(flt.filter_id, name="G", now=T0 + 1)
        assert out is not None
        assert out.name == "G"

    def test_updates_query(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {"a": 1}, now=T0)
        out = reg.update_filter(flt.filter_id, query={"b": 2}, now=T0 + 1)
        assert out.query == {"b": 2}

    def test_query_is_copied_on_update(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        q = {"x": 1}
        reg.update_filter(flt.filter_id, query=q, now=T0 + 1)
        q["x"] = 999
        assert reg.get_filter(flt.filter_id).query == {"x": 1}

    def test_updates_shared(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        out = reg.update_filter(flt.filter_id, shared=True, now=T0 + 1)
        assert out.shared is True

    def test_partial_update_leaves_others(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {"a": 1}, shared=True, now=T0)
        out = reg.update_filter(flt.filter_id, name="G", now=T0 + 1)
        assert out.query == {"a": 1}
        assert out.shared is True

    def test_updates_updated_at(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        out = reg.update_filter(flt.filter_id, name="G", now=T0 + 10)
        assert out.updated_at == T0 + 10
        assert out.created_at == T0

    def test_update_with_no_changes_still_bumps_updated_at(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        out = reg.update_filter(flt.filter_id, now=T0 + 5)
        assert out.updated_at == T0 + 5


# ---------------------------------------------------------------------------
# TestDeleteFilter
# ---------------------------------------------------------------------------
class TestDeleteFilter:
    def test_returns_true_when_existed(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        assert reg.delete_filter(flt.filter_id) is True

    def test_returns_false_when_missing(self):
        reg = make_registry()
        assert reg.delete_filter("nope") is False

    def test_actually_removes(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        reg.delete_filter(flt.filter_id)
        assert reg.get_filter(flt.filter_id) is None

    def test_removes_from_owner_index(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        reg.delete_filter(flt.filter_id)
        assert reg.filters_for_owner("u") == []

    def test_owner_dropped_when_empty(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        reg.delete_filter(flt.filter_id)
        assert "u" not in reg.all_owners()

    def test_other_filters_unaffected(self):
        reg = make_registry()
        a = reg.save_filter("A", "u", {}, now=T0)
        b = reg.save_filter("B", "u", {}, now=T0)
        reg.delete_filter(a.filter_id)
        assert reg.get_filter(b.filter_id) is not None


# ---------------------------------------------------------------------------
# TestGetFilter
# ---------------------------------------------------------------------------
class TestGetFilter:
    def test_found(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        assert reg.get_filter(flt.filter_id) is flt

    def test_not_found(self):
        reg = make_registry()
        assert reg.get_filter("nope") is None

    def test_after_delete(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        reg.delete_filter(flt.filter_id)
        assert reg.get_filter(flt.filter_id) is None


# ---------------------------------------------------------------------------
# TestRecordUse
# ---------------------------------------------------------------------------
class TestRecordUse:
    def test_returns_false_when_missing(self):
        reg = make_registry()
        assert reg.record_use("nope") is False

    def test_returns_true_when_found(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        assert reg.record_use(flt.filter_id) is True

    def test_increments_use_count(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        reg.record_use(flt.filter_id)
        assert reg.get_filter(flt.filter_id).use_count == 1

    def test_increments_multiple_times(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        for _ in range(5):
            reg.record_use(flt.filter_id)
        assert reg.get_filter(flt.filter_id).use_count == 5

    def test_no_effect_when_missing(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        reg.record_use("nope")
        assert reg.get_filter(flt.filter_id).use_count == 0


# ---------------------------------------------------------------------------
# TestFiltersForOwner
# ---------------------------------------------------------------------------
class TestFiltersForOwner:
    def test_empty_for_unknown_owner(self):
        reg = make_registry()
        assert reg.filters_for_owner("nope") == []

    def test_returns_only_owners_filters(self):
        reg = make_registry()
        a = reg.save_filter("A", "u1", {}, now=T0)
        reg.save_filter("B", "u2", {}, now=T0)
        out = reg.filters_for_owner("u1")
        assert [f.filter_id for f in out] == [a.filter_id]

    def test_sorted_by_name(self):
        reg = make_registry()
        reg.save_filter("Charlie", "u", {}, now=T0)
        reg.save_filter("Alpha", "u", {}, now=T0)
        reg.save_filter("Bravo", "u", {}, now=T0)
        names = [f.name for f in reg.filters_for_owner("u")]
        assert names == ["Alpha", "Bravo", "Charlie"]

    def test_excludes_after_delete(self):
        reg = make_registry()
        a = reg.save_filter("A", "u", {}, now=T0)
        reg.save_filter("B", "u", {}, now=T0)
        reg.delete_filter(a.filter_id)
        names = [f.name for f in reg.filters_for_owner("u")]
        assert names == ["B"]


# ---------------------------------------------------------------------------
# TestSharedFilters
# ---------------------------------------------------------------------------
class TestSharedFilters:
    def test_empty_when_none_shared(self):
        reg = make_registry()
        reg.save_filter("F", "u", {}, now=T0)
        assert reg.shared_filters() == []

    def test_returns_only_shared(self):
        reg = make_registry()
        reg.save_filter("Private", "u", {}, now=T0)
        s = reg.save_filter("Public", "u", {}, shared=True, now=T0)
        out = reg.shared_filters()
        assert [f.filter_id for f in out] == [s.filter_id]

    def test_sorted_by_name(self):
        reg = make_registry()
        reg.save_filter("Charlie", "u", {}, shared=True, now=T0)
        reg.save_filter("Alpha", "u", {}, shared=True, now=T0)
        reg.save_filter("Bravo", "u", {}, shared=True, now=T0)
        assert [f.name for f in reg.shared_filters()] == ["Alpha", "Bravo", "Charlie"]

    def test_across_owners(self):
        reg = make_registry()
        reg.save_filter("X", "u1", {}, shared=True, now=T0)
        reg.save_filter("Y", "u2", {}, shared=True, now=T0)
        assert len(reg.shared_filters()) == 2


# ---------------------------------------------------------------------------
# TestVisibleTo
# ---------------------------------------------------------------------------
class TestVisibleTo:
    def test_includes_own_private(self):
        reg = make_registry()
        flt = reg.save_filter("A", "u1", {}, now=T0)
        out = reg.visible_to("u1")
        assert flt.filter_id in {f.filter_id for f in out}

    def test_includes_shared_from_others(self):
        reg = make_registry()
        s = reg.save_filter("S", "u2", {}, shared=True, now=T0)
        out = reg.visible_to("u1")
        assert s.filter_id in {f.filter_id for f in out}

    def test_excludes_others_private(self):
        reg = make_registry()
        priv = reg.save_filter("P", "u2", {}, now=T0)
        out = reg.visible_to("u1")
        assert priv.filter_id not in {f.filter_id for f in out}

    def test_deduplicates_own_shared(self):
        reg = make_registry()
        own_shared = reg.save_filter("S", "u1", {}, shared=True, now=T0)
        out = reg.visible_to("u1")
        ids = [f.filter_id for f in out]
        assert ids.count(own_shared.filter_id) == 1

    def test_sorted_by_name(self):
        reg = make_registry()
        reg.save_filter("Zeta", "u1", {}, now=T0)
        reg.save_filter("Alpha", "u2", {}, shared=True, now=T0)
        reg.save_filter("Mike", "u1", {}, now=T0)
        names = [f.name for f in reg.visible_to("u1")]
        assert names == ["Alpha", "Mike", "Zeta"]

    def test_unknown_user_gets_only_shared(self):
        reg = make_registry()
        reg.save_filter("P", "u1", {}, now=T0)
        s = reg.save_filter("S", "u2", {}, shared=True, now=T0)
        out = reg.visible_to("unknown")
        assert [f.filter_id for f in out] == [s.filter_id]


# ---------------------------------------------------------------------------
# TestMostUsed
# ---------------------------------------------------------------------------
class TestMostUsed:
    def test_empty(self):
        reg = make_registry()
        assert reg.most_used() == []

    def test_sorted_by_use_count_desc(self):
        reg = make_registry()
        a = reg.save_filter("A", "u", {}, now=T0)
        b = reg.save_filter("B", "u", {}, now=T0)
        c = reg.save_filter("C", "u", {}, now=T0)
        for _ in range(3):
            reg.record_use(b.filter_id)
        for _ in range(5):
            reg.record_use(a.filter_id)
        reg.record_use(c.filter_id)
        names = [f.name for f in reg.most_used()]
        assert names == ["A", "B", "C"]

    def test_tie_broken_by_name_asc(self):
        reg = make_registry()
        reg.save_filter("Bravo", "u", {}, now=T0)
        reg.save_filter("Alpha", "u", {}, now=T0)
        names = [f.name for f in reg.most_used()]
        assert names == ["Alpha", "Bravo"]

    def test_limit_truncates(self):
        reg = make_registry()
        for n in ("A", "B", "C", "D"):
            reg.save_filter(n, "u", {}, now=T0)
        out = reg.most_used(limit=2)
        assert len(out) == 2

    def test_limit_zero(self):
        reg = make_registry()
        reg.save_filter("A", "u", {}, now=T0)
        assert reg.most_used(limit=0) == []

    def test_limit_negative_treated_as_zero(self):
        reg = make_registry()
        reg.save_filter("A", "u", {}, now=T0)
        assert reg.most_used(limit=-3) == []

    def test_default_limit_ten(self):
        reg = make_registry()
        for i in range(15):
            reg.save_filter(f"F{i:02d}", "u", {}, now=T0)
        assert len(reg.most_used()) == 10


# ---------------------------------------------------------------------------
# TestRenameFilter
# ---------------------------------------------------------------------------
class TestRenameFilter:
    def test_returns_true_when_found(self):
        reg = make_registry()
        flt = reg.save_filter("Old", "u", {}, now=T0)
        assert reg.rename_filter(flt.filter_id, "New") is True

    def test_actually_renames(self):
        reg = make_registry()
        flt = reg.save_filter("Old", "u", {}, now=T0)
        reg.rename_filter(flt.filter_id, "New")
        assert reg.get_filter(flt.filter_id).name == "New"

    def test_returns_false_when_missing(self):
        reg = make_registry()
        assert reg.rename_filter("nope", "X") is False


# ---------------------------------------------------------------------------
# TestAllOwners
# ---------------------------------------------------------------------------
class TestAllOwners:
    def test_empty(self):
        reg = make_registry()
        assert reg.all_owners() == []

    def test_unique(self):
        reg = make_registry()
        reg.save_filter("A", "u1", {}, now=T0)
        reg.save_filter("B", "u1", {}, now=T0)
        reg.save_filter("C", "u2", {}, now=T0)
        assert reg.all_owners() == ["u1", "u2"]

    def test_sorted(self):
        reg = make_registry()
        reg.save_filter("a", "zed", {}, now=T0)
        reg.save_filter("b", "alf", {}, now=T0)
        reg.save_filter("c", "mike", {}, now=T0)
        assert reg.all_owners() == ["alf", "mike", "zed"]

    def test_drops_owner_after_last_delete(self):
        reg = make_registry()
        flt = reg.save_filter("A", "solo", {}, now=T0)
        reg.delete_filter(flt.filter_id)
        assert reg.all_owners() == []


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty_registry(self):
        reg = make_registry()
        assert reg.stats() == FilterStats(0, 0, 0, 0)

    def test_total_filters(self):
        reg = make_registry()
        reg.save_filter("A", "u1", {}, now=T0)
        reg.save_filter("B", "u1", {}, now=T0)
        reg.save_filter("C", "u2", {}, now=T0)
        assert reg.stats().total_filters == 3

    def test_shared_filters(self):
        reg = make_registry()
        reg.save_filter("A", "u1", {}, shared=True, now=T0)
        reg.save_filter("B", "u1", {}, now=T0)
        reg.save_filter("C", "u2", {}, shared=True, now=T0)
        assert reg.stats().shared_filters == 2

    def test_unique_owners(self):
        reg = make_registry()
        reg.save_filter("A", "u1", {}, now=T0)
        reg.save_filter("B", "u1", {}, now=T0)
        reg.save_filter("C", "u2", {}, now=T0)
        assert reg.stats().unique_owners == 2

    def test_total_uses(self):
        reg = make_registry()
        a = reg.save_filter("A", "u", {}, now=T0)
        b = reg.save_filter("B", "u", {}, now=T0)
        for _ in range(3):
            reg.record_use(a.filter_id)
        reg.record_use(b.filter_id)
        assert reg.stats().total_uses == 4

    def test_after_delete(self):
        reg = make_registry()
        a = reg.save_filter("A", "u1", {}, shared=True, now=T0)
        reg.save_filter("B", "u2", {}, now=T0)
        reg.delete_filter(a.filter_id)
        s = reg.stats()
        assert s.total_filters == 1
        assert s.shared_filters == 0
        assert s.unique_owners == 1


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_save_filter(self):
        reg = make_registry()
        n_threads = 8
        per_thread = 50
        barrier = threading.Barrier(n_threads)
        errors: list[Exception] = []

        def worker(tid: int) -> None:
            try:
                barrier.wait()
                for i in range(per_thread):
                    reg.save_filter(f"f{tid}-{i}", f"u{tid}", {"i": i}, now=T0)
            except Exception as e:  # pragma: no cover - defensive
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert errors == []
        stats = reg.stats()
        assert stats.total_filters == n_threads * per_thread
        assert stats.unique_owners == n_threads

    def test_concurrent_record_use(self):
        reg = make_registry()
        flt = reg.save_filter("F", "u", {}, now=T0)
        n_threads = 8
        per_thread = 25
        barrier = threading.Barrier(n_threads)

        def worker() -> None:
            barrier.wait()
            for _ in range(per_thread):
                reg.record_use(flt.filter_id)

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert reg.get_filter(flt.filter_id).use_count == n_threads * per_thread
