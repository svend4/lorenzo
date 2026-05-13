"""Tests for E223 doc_index_master."""

from __future__ import annotations

import pytest

from docstoolkit.doc_index_master import (
    DocIndexMaster,
    IndexEntry,
    IndexHealth,
    IndexType,
    RegistryStats,
)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
class RecordingUpdater:
    """A callable updater that records the calls it receives."""

    def __init__(self, fail: bool = False) -> None:
        self.calls: list[tuple] = []
        self.fail = fail

    def __call__(self, doc_id, content=None, action="upsert"):
        self.calls.append((doc_id, content, action))
        if self.fail:
            raise RuntimeError("boom")
        return True


# --------------------------------------------------------------------------- #
class TestIndexType:
    def test_members_exist(self):
        names = {m.name for m in IndexType}
        assert {"SEARCH", "TAGS", "METADATA", "FULL_TEXT", "GRAPH", "CUSTOM"} <= names

    def test_values_are_strings(self):
        assert IndexType.SEARCH.value == "search"
        assert IndexType.FULL_TEXT.value == "full_text"


class TestIndexHealth:
    def test_members_exist(self):
        names = {m.name for m in IndexHealth}
        assert names == {"HEALTHY", "STALE", "REBUILDING", "ERROR"}


class TestIndexEntry:
    def test_defaults(self):
        e = IndexEntry(name="i", index_type=IndexType.SEARCH)
        assert e.version == 0
        assert e.last_updated == 0.0
        assert e.health is IndexHealth.HEALTHY
        assert e.entry_count == 0
        assert e.metadata == {}

    def test_independent_metadata(self):
        a = IndexEntry(name="a", index_type=IndexType.TAGS)
        b = IndexEntry(name="b", index_type=IndexType.TAGS)
        a.metadata["x"] = 1
        assert "x" not in b.metadata


class TestRegistryStats:
    def test_fields(self):
        s = RegistryStats(
            total_indexes=1,
            healthy_count=1,
            stale_count=0,
            error_count=0,
            total_entries=5,
            by_type={"search": 1},
        )
        assert s.total_indexes == 1
        assert s.by_type == {"search": 1}


# --------------------------------------------------------------------------- #
class TestRegisterIndex:
    def test_register_returns_entry(self):
        m = DocIndexMaster()
        e = m.register_index("primary", IndexType.SEARCH, now=10.0)
        assert isinstance(e, IndexEntry)
        assert e.name == "primary"
        assert e.index_type is IndexType.SEARCH
        assert e.last_updated == 10.0
        assert e.health is IndexHealth.HEALTHY

    def test_register_duplicate_raises(self):
        m = DocIndexMaster()
        m.register_index("primary", IndexType.SEARCH)
        with pytest.raises(ValueError):
            m.register_index("primary", IndexType.TAGS)

    def test_register_with_metadata_copies(self):
        m = DocIndexMaster()
        meta = {"k": "v"}
        e = m.register_index("a", IndexType.METADATA, metadata=meta)
        meta["k"] = "changed"
        assert e.metadata == {"k": "v"}

    def test_register_without_updater_ok(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.GRAPH)
        assert m.get_index("a") is not None


class TestUnregisterIndex:
    def test_unregister_known(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        assert m.unregister_index("a") is True
        assert m.get_index("a") is None

    def test_unregister_unknown(self):
        m = DocIndexMaster()
        assert m.unregister_index("ghost") is False


class TestMarkStale:
    def test_mark_stale_ok(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        assert m.mark_stale("a") is True
        assert m.get_index("a").health is IndexHealth.STALE

    def test_mark_stale_missing(self):
        m = DocIndexMaster()
        assert m.mark_stale("missing") is False


class TestMarkHealthy:
    def test_mark_healthy_bumps_version(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.mark_stale("a")
        assert m.mark_healthy("a", now=5.0) is True
        e = m.get_index("a")
        assert e.health is IndexHealth.HEALTHY
        assert e.version == 1
        assert e.last_updated == 5.0

    def test_mark_healthy_sets_entry_count(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.mark_healthy("a", entry_count=42)
        assert m.get_index("a").entry_count == 42

    def test_mark_healthy_missing(self):
        m = DocIndexMaster()
        assert m.mark_healthy("nope") is False


class TestMarkRebuilding:
    def test_mark_rebuilding_clears_count(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.mark_healthy("a", entry_count=10)
        assert m.mark_rebuilding("a") is True
        e = m.get_index("a")
        assert e.health is IndexHealth.REBUILDING
        assert e.entry_count == 0

    def test_mark_rebuilding_missing(self):
        m = DocIndexMaster()
        assert m.mark_rebuilding("nope") is False


class TestMarkError:
    def test_mark_error_stores_reason(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        assert m.mark_error("a", reason="disk full") is True
        e = m.get_index("a")
        assert e.health is IndexHealth.ERROR
        assert e.metadata["error_reason"] == "disk full"

    def test_mark_error_without_reason(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        assert m.mark_error("a") is True
        assert "error_reason" not in m.get_index("a").metadata

    def test_mark_error_missing(self):
        m = DocIndexMaster()
        assert m.mark_error("ghost") is False


# --------------------------------------------------------------------------- #
class TestDispatchUpsert:
    def test_dispatch_calls_all_updaters(self):
        m = DocIndexMaster()
        u1 = RecordingUpdater()
        u2 = RecordingUpdater()
        m.register_index("a", IndexType.SEARCH, updater=u1)
        m.register_index("b", IndexType.TAGS, updater=u2)
        res = m.dispatch_upsert("doc1", content="hello", now=3.0)
        assert res == {"a": True, "b": True}
        assert u1.calls == [("doc1", "hello", "upsert")]
        assert u2.calls == [("doc1", "hello", "upsert")]

    def test_dispatch_bumps_version_and_updates_time(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH, updater=RecordingUpdater())
        m.dispatch_upsert("d1", content="x", now=7.0)
        e = m.get_index("a")
        assert e.version == 1
        assert e.last_updated == 7.0

    def test_dispatch_skips_indexes_without_updater(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)  # no updater
        res = m.dispatch_upsert("doc1")
        assert res == {}


class TestDispatchDelete:
    def test_dispatch_delete_calls(self):
        m = DocIndexMaster()
        u = RecordingUpdater()
        m.register_index("a", IndexType.SEARCH, updater=u)
        res = m.dispatch_delete("doc-x", now=2.0)
        assert res == {"a": True}
        assert u.calls == [("doc-x", None, "delete")]

    def test_dispatch_delete_with_no_indexes(self):
        m = DocIndexMaster()
        assert m.dispatch_delete("doc-x") == {}


class TestDispatchTargetTypes:
    def test_filter_by_type(self):
        m = DocIndexMaster()
        u_search = RecordingUpdater()
        u_tags = RecordingUpdater()
        m.register_index("a", IndexType.SEARCH, updater=u_search)
        m.register_index("b", IndexType.TAGS, updater=u_tags)
        res = m.dispatch_upsert("d", target_types=[IndexType.SEARCH])
        assert res == {"a": True}
        assert u_tags.calls == []

    def test_filter_multiple_types(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH, updater=RecordingUpdater())
        m.register_index("b", IndexType.TAGS, updater=RecordingUpdater())
        m.register_index("c", IndexType.GRAPH, updater=RecordingUpdater())
        res = m.dispatch_upsert(
            "d", target_types=[IndexType.SEARCH, IndexType.GRAPH]
        )
        assert set(res.keys()) == {"a", "c"}

    def test_empty_target_filters_all_out(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH, updater=RecordingUpdater())
        res = m.dispatch_upsert("d", target_types=[])
        assert res == {}


class TestDispatchFailingUpdater:
    def test_failure_returns_false_and_sets_error(self):
        m = DocIndexMaster()
        ok = RecordingUpdater()
        bad = RecordingUpdater(fail=True)
        m.register_index("a", IndexType.SEARCH, updater=ok)
        m.register_index("b", IndexType.TAGS, updater=bad)
        res = m.dispatch_upsert("doc", content="x")
        assert res["a"] is True
        assert res["b"] is False
        assert m.get_index("b").health is IndexHealth.ERROR
        assert m.get_index("a").health is IndexHealth.HEALTHY

    def test_failure_on_delete(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH, updater=RecordingUpdater(fail=True))
        res = m.dispatch_delete("doc")
        assert res == {"a": False}
        assert m.get_index("a").health is IndexHealth.ERROR


# --------------------------------------------------------------------------- #
class TestGetIndex:
    def test_get_known(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        assert m.get_index("a").name == "a"

    def test_get_unknown(self):
        m = DocIndexMaster()
        assert m.get_index("ghost") is None


class TestIndexesByType:
    def test_returns_only_matching(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.register_index("b", IndexType.SEARCH)
        m.register_index("c", IndexType.TAGS)
        results = m.indexes_by_type(IndexType.SEARCH)
        names = {e.name for e in results}
        assert names == {"a", "b"}

    def test_empty_when_none(self):
        m = DocIndexMaster()
        assert m.indexes_by_type(IndexType.GRAPH) == []


class TestUnhealthyIndexes:
    def test_returns_non_healthy(self):
        m = DocIndexMaster()
        m.register_index("h", IndexType.SEARCH)
        m.register_index("s", IndexType.SEARCH)
        m.register_index("e", IndexType.SEARCH)
        m.mark_stale("s")
        m.mark_error("e")
        names = {e.name for e in m.unhealthy_indexes()}
        assert names == {"s", "e"}


class TestStaleIndexes:
    def test_returns_only_stale(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.register_index("b", IndexType.SEARCH)
        m.mark_stale("a")
        names = {e.name for e in m.stale_indexes()}
        assert names == {"a"}


class TestRebuildingIndexes:
    def test_returns_only_rebuilding(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.register_index("b", IndexType.SEARCH)
        m.mark_rebuilding("b")
        names = {e.name for e in m.rebuilding_indexes()}
        assert names == {"b"}


# --------------------------------------------------------------------------- #
class TestBumpVersion:
    def test_bump_version(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        assert m.bump_version("a", now=9.0) is True
        e = m.get_index("a")
        assert e.version == 1
        assert e.last_updated == 9.0

    def test_bump_version_missing(self):
        m = DocIndexMaster()
        assert m.bump_version("ghost") is False


class TestSetMetadata:
    def test_set_metadata_known(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        assert m.set_metadata("a", "owner", "lorenzo") is True
        assert m.get_index("a").metadata["owner"] == "lorenzo"

    def test_set_metadata_missing(self):
        m = DocIndexMaster()
        assert m.set_metadata("nope", "k", "v") is False


# --------------------------------------------------------------------------- #
class TestStats:
    def test_empty_stats(self):
        s = DocIndexMaster().stats()
        assert s.total_indexes == 0
        assert s.total_entries == 0
        assert s.by_type == {}
        assert s.healthy_count == s.stale_count == s.error_count == 0

    def test_mixed_stats(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.register_index("b", IndexType.TAGS)
        m.register_index("c", IndexType.SEARCH)
        m.mark_healthy("a", entry_count=3)
        m.mark_healthy("b", entry_count=2)
        m.mark_stale("c")
        s = m.stats()
        assert s.total_indexes == 3
        assert s.healthy_count == 2
        assert s.stale_count == 1
        assert s.error_count == 0
        assert s.total_entries == 5
        assert s.by_type == {"search": 2, "tags": 1}

    def test_error_counted(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.mark_error("a")
        s = m.stats()
        assert s.error_count == 1
        assert s.healthy_count == 0


class TestIndexCount:
    def test_initial_zero(self):
        assert DocIndexMaster().index_count == 0

    def test_grows_with_registration(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.register_index("b", IndexType.TAGS)
        assert m.index_count == 2


class TestClear:
    def test_clear_removes_all(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH, updater=RecordingUpdater())
        m.register_index("b", IndexType.TAGS)
        m.clear()
        assert m.index_count == 0
        assert m.all_names() == []
        # dispatch after clear yields no calls
        assert m.dispatch_upsert("doc") == {}


class TestAllNames:
    def test_empty(self):
        assert DocIndexMaster().all_names() == []

    def test_lists_all(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.register_index("b", IndexType.TAGS)
        assert set(m.all_names()) == {"a", "b"}


# --------------------------------------------------------------------------- #
class TestEdgeCases:
    def test_dispatch_with_no_indexes(self):
        m = DocIndexMaster()
        assert m.dispatch_upsert("doc") == {}
        assert m.dispatch_delete("doc") == {}

    def test_mark_after_unregister(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.unregister_index("a")
        assert m.mark_stale("a") is False
        assert m.mark_healthy("a") is False
        assert m.mark_rebuilding("a") is False
        assert m.mark_error("a") is False
        assert m.bump_version("a") is False
        assert m.set_metadata("a", "k", "v") is False

    def test_reregister_after_unregister(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH)
        m.unregister_index("a")
        e = m.register_index("a", IndexType.TAGS)
        assert e.index_type is IndexType.TAGS

    def test_dispatch_does_not_increment_version_on_failure(self):
        m = DocIndexMaster()
        m.register_index("a", IndexType.SEARCH, updater=RecordingUpdater(fail=True))
        m.dispatch_upsert("doc", now=4.0)
        e = m.get_index("a")
        # version stays 0; health becomes ERROR
        assert e.version == 0
        assert e.health is IndexHealth.ERROR

    def test_register_default_now_zero(self):
        m = DocIndexMaster()
        e = m.register_index("a", IndexType.SEARCH)
        assert e.last_updated == 0.0
