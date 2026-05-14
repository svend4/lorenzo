"""Tests for the snapshot_store module (E83)."""

from __future__ import annotations

import os
import time
import uuid

import pytest

from docstoolkit.snapshot_store import (
    Snapshot,
    SnapshotMetadata,
    SnapshotStore,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_store() -> SnapshotStore:
    """Return a fresh in-memory SnapshotStore."""
    return SnapshotStore()


def sample_metadata(
    snapshot_id: str = "snap-1",
    name: str = "config",
    created_at: float = 1000.0,
    description: str = "",
    tags: list[str] | None = None,
    size_bytes: int = 0,
) -> SnapshotMetadata:
    return SnapshotMetadata(
        snapshot_id=snapshot_id,
        name=name,
        created_at=created_at,
        description=description,
        tags=tags or [],
        size_bytes=size_bytes,
    )


# ===========================================================================
# SnapshotMetadata dataclass tests
# ===========================================================================

class TestSnapshotMetadata:
    def test_required_fields(self):
        m = SnapshotMetadata(snapshot_id="id1", name="x", created_at=1.0)
        assert m.snapshot_id == "id1"
        assert m.name == "x"
        assert m.created_at == 1.0

    def test_description_default(self):
        m = SnapshotMetadata(snapshot_id="i", name="n", created_at=0.0)
        assert m.description == ""

    def test_tags_default_empty_list(self):
        m = SnapshotMetadata(snapshot_id="i", name="n", created_at=0.0)
        assert m.tags == []

    def test_tags_default_is_list_type(self):
        m = SnapshotMetadata(snapshot_id="i", name="n", created_at=0.0)
        assert isinstance(m.tags, list)

    def test_size_bytes_default(self):
        m = SnapshotMetadata(snapshot_id="i", name="n", created_at=0.0)
        assert m.size_bytes == 0

    def test_size_bytes_explicit(self):
        m = SnapshotMetadata(snapshot_id="i", name="n", created_at=0.0, size_bytes=42)
        assert m.size_bytes == 42

    def test_tags_explicit(self):
        m = SnapshotMetadata(
            snapshot_id="i", name="n", created_at=0.0, tags=["a", "b"]
        )
        assert m.tags == ["a", "b"]

    def test_description_explicit(self):
        m = SnapshotMetadata(
            snapshot_id="i", name="n", created_at=0.0, description="desc"
        )
        assert m.description == "desc"

    def test_tags_default_factory_independence(self):
        m1 = SnapshotMetadata(snapshot_id="a", name="n", created_at=0.0)
        m2 = SnapshotMetadata(snapshot_id="b", name="n", created_at=0.0)
        m1.tags.append("t1")
        assert m2.tags == []

    def test_equality(self):
        m1 = SnapshotMetadata(snapshot_id="i", name="n", created_at=1.0)
        m2 = SnapshotMetadata(snapshot_id="i", name="n", created_at=1.0)
        assert m1 == m2

    def test_inequality_different_id(self):
        m1 = SnapshotMetadata(snapshot_id="a", name="n", created_at=1.0)
        m2 = SnapshotMetadata(snapshot_id="b", name="n", created_at=1.0)
        assert m1 != m2

    def test_float_created_at(self):
        m = SnapshotMetadata(snapshot_id="i", name="n", created_at=1234.5678)
        assert m.created_at == 1234.5678


# ===========================================================================
# Snapshot dataclass tests
# ===========================================================================

class TestSnapshot:
    def test_basic_construction(self):
        meta = sample_metadata()
        s = Snapshot(metadata=meta, data=b"payload")
        assert s.metadata is meta
        assert s.data == b"payload"

    def test_data_is_bytes(self):
        s = Snapshot(metadata=sample_metadata(), data=b"")
        assert isinstance(s.data, bytes)

    def test_empty_data(self):
        s = Snapshot(metadata=sample_metadata(), data=b"")
        assert s.data == b""

    def test_binary_data(self):
        payload = bytes(range(256))
        s = Snapshot(metadata=sample_metadata(), data=payload)
        assert s.data == payload

    def test_metadata_attribute(self):
        meta = sample_metadata(snapshot_id="abc")
        s = Snapshot(metadata=meta, data=b"x")
        assert s.metadata.snapshot_id == "abc"

    def test_equality(self):
        meta = sample_metadata()
        s1 = Snapshot(metadata=meta, data=b"x")
        s2 = Snapshot(metadata=meta, data=b"x")
        assert s1 == s2


# ===========================================================================
# SnapshotStore.__init__ tests
# ===========================================================================

class TestSnapshotStoreInit:
    def test_default_in_memory(self):
        store = SnapshotStore()
        assert store.count() == 0
        store.close()

    def test_explicit_memory(self):
        store = SnapshotStore(":memory:")
        assert store.count() == 0
        store.close()

    def test_file_db(self, tmp_path):
        db_path = tmp_path / "snapshots.db"
        store = SnapshotStore(str(db_path))
        store.save("a", b"x")
        store.close()
        assert db_path.exists()

    def test_file_db_persists_across_instances(self, tmp_path):
        db_path = tmp_path / "snapshots.db"
        s1 = SnapshotStore(str(db_path))
        meta = s1.save("a", b"hello")
        s1.close()
        s2 = SnapshotStore(str(db_path))
        loaded = s2.load(meta.snapshot_id)
        assert loaded is not None
        assert loaded.data == b"hello"
        s2.close()


# ===========================================================================
# SnapshotStore.save tests
# ===========================================================================

class TestSnapshotStoreSave:
    def test_returns_metadata(self):
        store = make_store()
        meta = store.save("config", b"data")
        assert isinstance(meta, SnapshotMetadata)
        store.close()

    def test_metadata_has_id(self):
        store = make_store()
        meta = store.save("config", b"data")
        assert meta.snapshot_id
        assert isinstance(meta.snapshot_id, str)
        store.close()

    def test_id_is_uuid(self):
        store = make_store()
        meta = store.save("config", b"data")
        # Should parse as a UUID
        parsed = uuid.UUID(meta.snapshot_id)
        assert str(parsed) == meta.snapshot_id
        store.close()

    def test_ids_are_unique(self):
        store = make_store()
        ids = set()
        for _ in range(20):
            meta = store.save("x", b"")
            ids.add(meta.snapshot_id)
        assert len(ids) == 20
        store.close()

    def test_name_persisted(self):
        store = make_store()
        meta = store.save("my-snap", b"data")
        assert meta.name == "my-snap"
        loaded = store.get_metadata(meta.snapshot_id)
        assert loaded.name == "my-snap"
        store.close()

    def test_created_at_is_recent(self):
        store = make_store()
        before = time.time()
        meta = store.save("x", b"")
        after = time.time()
        assert before <= meta.created_at <= after
        store.close()

    def test_created_at_is_float(self):
        store = make_store()
        meta = store.save("x", b"")
        assert isinstance(meta.created_at, float)
        store.close()

    def test_size_bytes_equals_len_data(self):
        store = make_store()
        meta = store.save("x", b"hello world")
        assert meta.size_bytes == len(b"hello world")
        store.close()

    def test_size_bytes_empty(self):
        store = make_store()
        meta = store.save("x", b"")
        assert meta.size_bytes == 0
        store.close()

    def test_size_bytes_large(self):
        store = make_store()
        data = b"x" * 10_000
        meta = store.save("x", data)
        assert meta.size_bytes == 10_000
        store.close()

    def test_description_default_empty(self):
        store = make_store()
        meta = store.save("x", b"")
        assert meta.description == ""
        store.close()

    def test_description_persisted(self):
        store = make_store()
        meta = store.save("x", b"", description="my note")
        assert meta.description == "my note"
        loaded = store.get_metadata(meta.snapshot_id)
        assert loaded.description == "my note"
        store.close()

    def test_tags_default_empty(self):
        store = make_store()
        meta = store.save("x", b"")
        assert meta.tags == []
        store.close()

    def test_tags_persisted(self):
        store = make_store()
        meta = store.save("x", b"", tags=["a", "b", "c"])
        assert meta.tags == ["a", "b", "c"]
        loaded = store.get_metadata(meta.snapshot_id)
        assert loaded.tags == ["a", "b", "c"]
        store.close()

    def test_tags_none_becomes_empty_list(self):
        store = make_store()
        meta = store.save("x", b"", tags=None)
        assert meta.tags == []
        store.close()

    def test_data_persisted_round_trip(self):
        store = make_store()
        meta = store.save("x", b"binary\x00\x01\x02data")
        loaded = store.load(meta.snapshot_id)
        assert loaded.data == b"binary\x00\x01\x02data"
        store.close()

    def test_save_multiple_with_same_name(self):
        store = make_store()
        m1 = store.save("config", b"v1")
        m2 = store.save("config", b"v2")
        assert m1.snapshot_id != m2.snapshot_id
        assert store.count() == 2
        store.close()

    def test_save_count_increments(self):
        store = make_store()
        assert store.count() == 0
        store.save("a", b"")
        assert store.count() == 1
        store.save("b", b"")
        assert store.count() == 2
        store.close()

    def test_save_with_binary_data(self):
        store = make_store()
        data = bytes(range(256))
        meta = store.save("bin", data)
        loaded = store.load(meta.snapshot_id)
        assert loaded.data == data
        assert meta.size_bytes == 256
        store.close()


# ===========================================================================
# SnapshotStore.load tests
# ===========================================================================

class TestSnapshotStoreLoad:
    def test_load_returns_snapshot(self):
        store = make_store()
        meta = store.save("x", b"data")
        loaded = store.load(meta.snapshot_id)
        assert isinstance(loaded, Snapshot)
        store.close()

    def test_load_returns_full_data(self):
        store = make_store()
        meta = store.save("x", b"hello, world!")
        loaded = store.load(meta.snapshot_id)
        assert loaded.data == b"hello, world!"
        store.close()

    def test_load_metadata_matches_save(self):
        store = make_store()
        meta = store.save("x", b"data", description="d", tags=["t1", "t2"])
        loaded = store.load(meta.snapshot_id)
        assert loaded.metadata.snapshot_id == meta.snapshot_id
        assert loaded.metadata.name == "x"
        assert loaded.metadata.description == "d"
        assert loaded.metadata.tags == ["t1", "t2"]
        assert loaded.metadata.size_bytes == 4
        store.close()

    def test_load_missing_returns_none(self):
        store = make_store()
        assert store.load("does-not-exist") is None
        store.close()

    def test_load_missing_uuid_returns_none(self):
        store = make_store()
        assert store.load(str(uuid.uuid4())) is None
        store.close()

    def test_load_empty_data(self):
        store = make_store()
        meta = store.save("x", b"")
        loaded = store.load(meta.snapshot_id)
        assert loaded.data == b""
        store.close()

    def test_load_data_is_bytes(self):
        store = make_store()
        meta = store.save("x", b"abc")
        loaded = store.load(meta.snapshot_id)
        assert isinstance(loaded.data, bytes)
        store.close()

    def test_load_preserves_binary_bytes(self):
        store = make_store()
        payload = b"\x00\x01\x02\xff\xfe\xfd"
        meta = store.save("x", payload)
        loaded = store.load(meta.snapshot_id)
        assert loaded.data == payload
        store.close()

    def test_load_large_payload(self):
        store = make_store()
        payload = os.urandom(50_000)
        meta = store.save("x", payload)
        loaded = store.load(meta.snapshot_id)
        assert loaded.data == payload
        store.close()


# ===========================================================================
# SnapshotStore.get_metadata tests
# ===========================================================================

class TestSnapshotStoreGetMetadata:
    def test_returns_metadata(self):
        store = make_store()
        meta = store.save("x", b"data")
        got = store.get_metadata(meta.snapshot_id)
        assert isinstance(got, SnapshotMetadata)
        store.close()

    def test_metadata_fields(self):
        store = make_store()
        meta = store.save("conf", b"abcd", description="d", tags=["t"])
        got = store.get_metadata(meta.snapshot_id)
        assert got.snapshot_id == meta.snapshot_id
        assert got.name == "conf"
        assert got.description == "d"
        assert got.tags == ["t"]
        assert got.size_bytes == 4
        assert got.created_at == meta.created_at
        store.close()

    def test_missing_returns_none(self):
        store = make_store()
        assert store.get_metadata("nope") is None
        store.close()

    def test_missing_uuid_returns_none(self):
        store = make_store()
        assert store.get_metadata(str(uuid.uuid4())) is None
        store.close()

    def test_metadata_after_save_then_get(self):
        store = make_store()
        original = store.save("x", b"abc")
        retrieved = store.get_metadata(original.snapshot_id)
        assert retrieved == original
        store.close()


# ===========================================================================
# SnapshotStore.list tests
# ===========================================================================

class TestSnapshotStoreList:
    def test_empty_initially(self):
        store = make_store()
        assert store.list() == []
        store.close()

    def test_empty_returns_list_type(self):
        store = make_store()
        result = store.list()
        assert isinstance(result, list)
        store.close()

    def test_single_snapshot(self):
        store = make_store()
        meta = store.save("a", b"x")
        result = store.list()
        assert len(result) == 1
        assert result[0].snapshot_id == meta.snapshot_id
        store.close()

    def test_returns_metadata_type(self):
        store = make_store()
        store.save("a", b"x")
        result = store.list()
        assert isinstance(result[0], SnapshotMetadata)
        store.close()

    def test_results_are_metadata_not_snapshots(self):
        store = make_store()
        store.save("a", b"x")
        result = store.list()
        for item in result:
            assert not hasattr(item, "data")
        store.close()

    def test_sorted_newest_first(self):
        store = make_store()
        m1 = store.save("a", b"")
        time.sleep(0.005)
        m2 = store.save("b", b"")
        time.sleep(0.005)
        m3 = store.save("c", b"")
        ids = [m.snapshot_id for m in store.list()]
        assert ids == [m3.snapshot_id, m2.snapshot_id, m1.snapshot_id]
        store.close()

    def test_filter_by_name(self):
        store = make_store()
        store.save("a", b"")
        store.save("b", b"")
        store.save("a", b"")
        result = store.list(name="a")
        assert len(result) == 2
        assert all(m.name == "a" for m in result)
        store.close()

    def test_filter_by_name_missing(self):
        store = make_store()
        store.save("a", b"")
        result = store.list(name="zzz")
        assert result == []
        store.close()

    def test_filter_by_tag(self):
        store = make_store()
        store.save("a", b"", tags=["red", "small"])
        store.save("b", b"", tags=["blue"])
        store.save("c", b"", tags=["red", "large"])
        result = store.list(tag="red")
        assert len(result) == 2
        assert all("red" in m.tags for m in result)
        store.close()

    def test_filter_by_tag_missing(self):
        store = make_store()
        store.save("a", b"", tags=["red"])
        result = store.list(tag="nonexistent")
        assert result == []
        store.close()

    def test_filter_by_name_and_tag(self):
        store = make_store()
        store.save("a", b"", tags=["red"])
        store.save("a", b"", tags=["blue"])
        store.save("b", b"", tags=["red"])
        result = store.list(name="a", tag="red")
        assert len(result) == 1
        assert result[0].name == "a"
        assert "red" in result[0].tags
        store.close()

    def test_limit_parameter(self):
        store = make_store()
        for _ in range(5):
            store.save("x", b"")
            time.sleep(0.001)
        result = store.list(limit=3)
        assert len(result) == 3
        store.close()

    def test_limit_default_is_100(self):
        store = make_store()
        for _ in range(10):
            store.save("x", b"")
        assert len(store.list()) == 10
        store.close()

    def test_limit_larger_than_count(self):
        store = make_store()
        store.save("a", b"")
        store.save("b", b"")
        result = store.list(limit=999)
        assert len(result) == 2
        store.close()

    def test_limit_with_filter(self):
        store = make_store()
        for _ in range(5):
            store.save("x", b"", tags=["t"])
            time.sleep(0.001)
        result = store.list(tag="t", limit=2)
        assert len(result) == 2
        store.close()

    def test_limit_zero(self):
        store = make_store()
        store.save("x", b"")
        result = store.list(limit=0)
        assert result == []
        store.close()

    def test_list_no_data_attribute(self):
        store = make_store()
        store.save("x", b"sensitive payload")
        result = store.list()
        # metadata only — no data field
        for item in result:
            assert not hasattr(item, "data")
        store.close()


# ===========================================================================
# SnapshotStore.delete tests
# ===========================================================================

class TestSnapshotStoreDelete:
    def test_delete_existing_returns_true(self):
        store = make_store()
        meta = store.save("x", b"")
        assert store.delete(meta.snapshot_id) is True
        store.close()

    def test_delete_missing_returns_false(self):
        store = make_store()
        assert store.delete("doesnt-exist") is False
        store.close()

    def test_delete_removes_from_count(self):
        store = make_store()
        meta = store.save("x", b"")
        assert store.count() == 1
        store.delete(meta.snapshot_id)
        assert store.count() == 0
        store.close()

    def test_delete_removes_from_list(self):
        store = make_store()
        m1 = store.save("x", b"")
        m2 = store.save("y", b"")
        store.delete(m1.snapshot_id)
        result = store.list()
        assert len(result) == 1
        assert result[0].snapshot_id == m2.snapshot_id
        store.close()

    def test_delete_makes_load_return_none(self):
        store = make_store()
        meta = store.save("x", b"data")
        store.delete(meta.snapshot_id)
        assert store.load(meta.snapshot_id) is None
        store.close()

    def test_delete_makes_get_metadata_none(self):
        store = make_store()
        meta = store.save("x", b"data")
        store.delete(meta.snapshot_id)
        assert store.get_metadata(meta.snapshot_id) is None
        store.close()

    def test_delete_twice_returns_false(self):
        store = make_store()
        meta = store.save("x", b"")
        store.delete(meta.snapshot_id)
        assert store.delete(meta.snapshot_id) is False
        store.close()

    def test_delete_only_target(self):
        store = make_store()
        m1 = store.save("x", b"")
        m2 = store.save("y", b"")
        m3 = store.save("z", b"")
        store.delete(m2.snapshot_id)
        ids = {m.snapshot_id for m in store.list()}
        assert ids == {m1.snapshot_id, m3.snapshot_id}
        store.close()


# ===========================================================================
# SnapshotStore.latest tests
# ===========================================================================

class TestSnapshotStoreLatest:
    def test_latest_none_when_empty(self):
        store = make_store()
        assert store.latest("nope") is None
        store.close()

    def test_latest_none_for_missing_name(self):
        store = make_store()
        store.save("a", b"")
        assert store.latest("b") is None
        store.close()

    def test_latest_single_snapshot(self):
        store = make_store()
        meta = store.save("a", b"")
        got = store.latest("a")
        assert got.snapshot_id == meta.snapshot_id
        store.close()

    def test_latest_returns_most_recent(self):
        store = make_store()
        m1 = store.save("a", b"v1")
        time.sleep(0.005)
        m2 = store.save("a", b"v2")
        time.sleep(0.005)
        m3 = store.save("a", b"v3")
        got = store.latest("a")
        assert got.snapshot_id == m3.snapshot_id
        store.close()

    def test_latest_returns_metadata_type(self):
        store = make_store()
        store.save("a", b"")
        got = store.latest("a")
        assert isinstance(got, SnapshotMetadata)
        store.close()

    def test_latest_only_matches_name(self):
        store = make_store()
        store.save("a", b"")
        time.sleep(0.005)
        b_meta = store.save("b", b"")
        time.sleep(0.005)
        store.save("a", b"")
        got = store.latest("b")
        assert got.snapshot_id == b_meta.snapshot_id
        store.close()

    def test_latest_no_data_field(self):
        store = make_store()
        store.save("a", b"payload")
        got = store.latest("a")
        assert not hasattr(got, "data")
        store.close()


# ===========================================================================
# SnapshotStore.count tests
# ===========================================================================

class TestSnapshotStoreCount:
    def test_initial_zero(self):
        store = make_store()
        assert store.count() == 0
        store.close()

    def test_count_after_save(self):
        store = make_store()
        store.save("a", b"")
        assert store.count() == 1
        store.close()

    def test_count_returns_int(self):
        store = make_store()
        assert isinstance(store.count(), int)
        store.close()

    def test_count_after_multiple_saves(self):
        store = make_store()
        for _ in range(7):
            store.save("x", b"")
        assert store.count() == 7
        store.close()

    def test_count_after_delete(self):
        store = make_store()
        m = store.save("a", b"")
        store.save("b", b"")
        store.delete(m.snapshot_id)
        assert store.count() == 1
        store.close()


# ===========================================================================
# SnapshotStore.total_size tests
# ===========================================================================

class TestSnapshotStoreTotalSize:
    def test_initial_zero(self):
        store = make_store()
        assert store.total_size() == 0
        store.close()

    def test_returns_int(self):
        store = make_store()
        assert isinstance(store.total_size(), int)
        store.close()

    def test_single_snapshot(self):
        store = make_store()
        store.save("a", b"hello")
        assert store.total_size() == 5
        store.close()

    def test_sums_across_snapshots(self):
        store = make_store()
        store.save("a", b"x" * 10)
        store.save("b", b"x" * 20)
        store.save("c", b"x" * 30)
        assert store.total_size() == 60
        store.close()

    def test_after_delete(self):
        store = make_store()
        m1 = store.save("a", b"x" * 100)
        store.save("b", b"x" * 50)
        store.delete(m1.snapshot_id)
        assert store.total_size() == 50
        store.close()

    def test_empty_data_contributes_zero(self):
        store = make_store()
        store.save("a", b"")
        store.save("b", b"")
        assert store.total_size() == 0
        store.close()


# ===========================================================================
# SnapshotStore.prune tests
# ===========================================================================

class TestSnapshotStorePrune:
    def test_prune_no_snapshots(self):
        store = make_store()
        deleted = store.prune(name="missing", keep_count=10)
        assert deleted == 0
        store.close()

    def test_prune_returns_count(self):
        store = make_store()
        for _ in range(5):
            store.save("x", b"")
            time.sleep(0.001)
        deleted = store.prune(name="x", keep_count=2)
        assert deleted == 3
        store.close()

    def test_prune_keeps_newest(self):
        store = make_store()
        metas = []
        for _ in range(5):
            metas.append(store.save("x", b""))
            time.sleep(0.005)
        store.prune(name="x", keep_count=2)
        remaining = {m.snapshot_id for m in store.list(name="x")}
        # Last two saves should remain
        assert remaining == {metas[-1].snapshot_id, metas[-2].snapshot_id}
        store.close()

    def test_prune_keep_count_zero_deletes_all(self):
        store = make_store()
        for _ in range(3):
            store.save("x", b"")
            time.sleep(0.001)
        deleted = store.prune(name="x", keep_count=0)
        assert deleted == 3
        assert store.count() == 0
        store.close()

    def test_prune_keep_count_larger_than_total(self):
        store = make_store()
        for _ in range(3):
            store.save("x", b"")
        deleted = store.prune(name="x", keep_count=10)
        assert deleted == 0
        assert store.count() == 3
        store.close()

    def test_prune_does_not_affect_other_names(self):
        store = make_store()
        for _ in range(5):
            store.save("x", b"")
            time.sleep(0.001)
        for _ in range(3):
            store.save("y", b"")
            time.sleep(0.001)
        store.prune(name="x", keep_count=1)
        assert len(store.list(name="x")) == 1
        assert len(store.list(name="y")) == 3
        store.close()

    def test_prune_default_keep_count(self):
        store = make_store()
        # Default keep_count = 10
        for _ in range(12):
            store.save("x", b"")
            time.sleep(0.001)
        deleted = store.prune(name="x")
        assert deleted == 2
        assert len(store.list(name="x", limit=999)) == 10
        store.close()

    def test_prune_all_names_when_none(self):
        store = make_store()
        for _ in range(3):
            store.save("a", b"")
            time.sleep(0.001)
        for _ in range(4):
            store.save("b", b"")
            time.sleep(0.001)
        deleted = store.prune(keep_count=1)
        # 2 from a + 3 from b = 5
        assert deleted == 5
        assert len(store.list(name="a")) == 1
        assert len(store.list(name="b")) == 1
        store.close()

    def test_prune_negative_keep_count_treated_as_zero(self):
        store = make_store()
        store.save("x", b"")
        store.save("x", b"")
        deleted = store.prune(name="x", keep_count=-1)
        assert deleted == 2
        store.close()

    def test_prune_empty_store_with_no_name(self):
        store = make_store()
        deleted = store.prune(keep_count=5)
        assert deleted == 0
        store.close()


# ===========================================================================
# SnapshotStore.close tests
# ===========================================================================

class TestSnapshotStoreClose:
    def test_close_does_not_raise(self):
        store = make_store()
        store.close()  # should not raise

    def test_close_then_use_raises(self):
        store = make_store()
        store.close()
        # Using a closed sqlite connection should raise ProgrammingError
        import sqlite3
        with pytest.raises(sqlite3.ProgrammingError):
            store.save("x", b"")


# ===========================================================================
# Integration / scenario tests
# ===========================================================================

class TestSnapshotStoreScenarios:
    def test_save_load_delete_cycle(self):
        store = make_store()
        meta = store.save("config", b"v1", description="initial", tags=["dev"])
        loaded = store.load(meta.snapshot_id)
        assert loaded is not None
        assert loaded.data == b"v1"
        assert store.delete(meta.snapshot_id) is True
        assert store.load(meta.snapshot_id) is None

    def test_versioning_workflow(self):
        store = make_store()
        v1 = store.save("config", b"a=1")
        time.sleep(0.005)
        v2 = store.save("config", b"a=2")
        time.sleep(0.005)
        v3 = store.save("config", b"a=3")
        latest = store.latest("config")
        assert latest.snapshot_id == v3.snapshot_id
        history = store.list(name="config")
        assert [h.snapshot_id for h in history] == [
            v3.snapshot_id, v2.snapshot_id, v1.snapshot_id
        ]
        store.close()

    def test_prune_retains_newest_then_load_works(self):
        store = make_store()
        keep_ids = []
        all_metas = []
        for i in range(10):
            m = store.save("config", f"v{i}".encode())
            all_metas.append(m)
            time.sleep(0.002)
        store.prune(name="config", keep_count=3)
        # Last 3 should remain
        keep_ids = [m.snapshot_id for m in all_metas[-3:]]
        for kid in keep_ids:
            assert store.load(kid) is not None
        # Older ones gone
        for m in all_metas[:-3]:
            assert store.load(m.snapshot_id) is None
        store.close()

    def test_tags_filtering_with_many(self):
        store = make_store()
        store.save("a", b"", tags=["prod", "stable"])
        store.save("a", b"", tags=["dev"])
        store.save("a", b"", tags=["prod", "experimental"])
        result = store.list(tag="prod")
        assert len(result) == 2
        store.close()

    def test_total_size_after_prune(self):
        store = make_store()
        store.save("x", b"x" * 10)
        time.sleep(0.001)
        store.save("x", b"y" * 20)
        time.sleep(0.001)
        store.save("x", b"z" * 30)
        store.prune(name="x", keep_count=1)
        assert store.total_size() == 30
        store.close()

    def test_count_after_prune(self):
        store = make_store()
        for _ in range(6):
            store.save("x", b"")
            time.sleep(0.001)
        store.prune(name="x", keep_count=2)
        assert store.count() == 2
        store.close()

    def test_persistence_round_trip(self, tmp_path):
        db = tmp_path / "snap.db"
        s1 = SnapshotStore(str(db))
        m = s1.save("x", b"hello", description="d", tags=["a"])
        s1.close()
        s2 = SnapshotStore(str(db))
        got = s2.load(m.snapshot_id)
        assert got.data == b"hello"
        assert got.metadata.description == "d"
        assert got.metadata.tags == ["a"]
        s2.close()

    def test_metadata_consistency_save_get_list_latest(self):
        store = make_store()
        meta = store.save("x", b"data", description="d", tags=["t"])
        got_metadata = store.get_metadata(meta.snapshot_id)
        list_metadata = store.list(name="x")[0]
        latest_metadata = store.latest("x")
        # All three should be equal
        assert got_metadata == meta
        assert list_metadata == meta
        assert latest_metadata == meta
        store.close()
