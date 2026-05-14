"""Tests for docstoolkit.snapshot module."""
import hashlib
import re
import time
from pathlib import Path

import pytest

from docstoolkit.snapshot import (
    CapturedState,
    SnapshotCapture,
    SnapshotDiff,
    SnapshotMeta,
    SnapshotStore,
    diff_snapshots,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _capture(docs: dict, snapshot_id: str = "", metadata: dict | None = None) -> CapturedState:
    return SnapshotCapture().capture(docs, snapshot_id=snapshot_id, metadata=metadata)


def _make_state(
    snapshot_id: str = "s1",
    ts: str = "2026-01-01T00:00:00",
    doc_count: int = 2,
    total_bytes: int = 100,
    doc_hashes: dict | None = None,
    metadata: dict | None = None,
) -> CapturedState:
    return CapturedState(
        snapshot_id=snapshot_id,
        ts=ts,
        doc_count=doc_count,
        total_bytes=total_bytes,
        doc_hashes=doc_hashes or {},
        metadata=metadata or {},
    )


# ===========================================================================
# CapturedState — fields and defaults
# ===========================================================================

class TestCapturedStateFields:
    def test_fields_assigned(self):
        s = CapturedState(
            snapshot_id="x1", ts="2026-01-01T00:00:00",
            doc_count=3, total_bytes=256,
        )
        assert s.snapshot_id == "x1"
        assert s.ts == "2026-01-01T00:00:00"
        assert s.doc_count == 3
        assert s.total_bytes == 256

    def test_doc_hashes_default_empty(self):
        s = CapturedState(
            snapshot_id="x", ts="", doc_count=0, total_bytes=0
        )
        assert s.doc_hashes == {}

    def test_metadata_default_empty(self):
        s = CapturedState(
            snapshot_id="x", ts="", doc_count=0, total_bytes=0
        )
        assert s.metadata == {}

    def test_doc_hashes_independent(self):
        """Mutable defaults don't share state between instances."""
        a = CapturedState(snapshot_id="a", ts="", doc_count=0, total_bytes=0)
        b = CapturedState(snapshot_id="b", ts="", doc_count=0, total_bytes=0)
        a.doc_hashes["k"] = "v"
        assert "k" not in b.doc_hashes

    def test_metadata_independent(self):
        a = CapturedState(snapshot_id="a", ts="", doc_count=0, total_bytes=0)
        b = CapturedState(snapshot_id="b", ts="", doc_count=0, total_bytes=0)
        a.metadata["key"] = "val"
        assert "key" not in b.metadata


# ===========================================================================
# CapturedState — to_dict / from_dict round-trip
# ===========================================================================

class TestCapturedStateSerialisation:
    def test_to_dict_keys(self):
        s = _make_state()
        d = s.to_dict()
        assert set(d.keys()) == {
            "snapshot_id", "ts", "doc_count", "total_bytes", "doc_hashes", "metadata"
        }

    def test_to_dict_values(self):
        s = _make_state(
            snapshot_id="abc",
            ts="2026-05-01T10:00:00",
            doc_count=7,
            total_bytes=500,
            doc_hashes={"doc1": "abcdef0123456789"},
            metadata={"env": "prod"},
        )
        d = s.to_dict()
        assert d["snapshot_id"] == "abc"
        assert d["ts"] == "2026-05-01T10:00:00"
        assert d["doc_count"] == 7
        assert d["total_bytes"] == 500
        assert d["doc_hashes"] == {"doc1": "abcdef0123456789"}
        assert d["metadata"] == {"env": "prod"}

    def test_round_trip(self):
        s = _make_state(
            snapshot_id="rt-1",
            ts="2026-02-14T08:00:00",
            doc_count=4,
            total_bytes=128,
            doc_hashes={"a": "1234567890abcdef"},
            metadata={"tag": "test"},
        )
        s2 = CapturedState.from_dict(s.to_dict())
        assert s2.snapshot_id == s.snapshot_id
        assert s2.ts == s.ts
        assert s2.doc_count == s.doc_count
        assert s2.total_bytes == s.total_bytes
        assert s2.doc_hashes == s.doc_hashes
        assert s2.metadata == s.metadata

    def test_from_dict_doc_count_total_bytes_preserved(self):
        d = {
            "snapshot_id": "p1",
            "ts": "2026-01-01",
            "doc_count": 99,
            "total_bytes": 12345,
            "doc_hashes": {},
            "metadata": {},
        }
        s = CapturedState.from_dict(d)
        assert s.doc_count == 99
        assert s.total_bytes == 12345

    def test_from_dict_numeric_strings_coerced(self):
        d = {
            "snapshot_id": "p2",
            "ts": "t",
            "doc_count": "5",
            "total_bytes": "200",
            "doc_hashes": {},
            "metadata": {},
        }
        s = CapturedState.from_dict(d)
        assert s.doc_count == 5
        assert s.total_bytes == 200

    def test_from_dict_missing_optional_keys(self):
        d = {"snapshot_id": "min"}
        s = CapturedState.from_dict(d)
        assert s.ts == ""
        assert s.doc_count == 0
        assert s.total_bytes == 0
        assert s.doc_hashes == {}
        assert s.metadata == {}


# ===========================================================================
# SnapshotCapture.capture
# ===========================================================================

class TestSnapshotCapture:
    def setup_method(self):
        self.cap = SnapshotCapture()

    def test_returns_captured_state(self):
        result = self.cap.capture({"doc1": "hello"})
        assert isinstance(result, CapturedState)

    def test_doc_count_equals_len_docs(self):
        docs = {"a": "aaa", "b": "bbb", "c": "ccc"}
        result = self.cap.capture(docs)
        assert result.doc_count == 3

    def test_total_bytes_sum_of_utf8_lengths(self):
        docs = {"a": "hello", "b": "world!"}
        result = self.cap.capture(docs)
        expected = len("hello".encode()) + len("world!".encode())
        assert result.total_bytes == expected

    def test_total_bytes_multibyte_content(self):
        content = "привет"  # Cyrillic — 2 bytes per char in UTF-8
        docs = {"doc": content}
        result = self.cap.capture(docs)
        assert result.total_bytes == len(content.encode())

    def test_doc_hashes_keys_match_doc_ids(self):
        docs = {"alpha": "aaa", "beta": "bbb"}
        result = self.cap.capture(docs)
        assert set(result.doc_hashes.keys()) == {"alpha", "beta"}

    def test_hash_values_are_16_char_hex(self):
        docs = {"doc1": "some content", "doc2": "other"}
        result = self.cap.capture(docs)
        for doc_id, h in result.doc_hashes.items():
            assert len(h) == 16, f"hash for {doc_id!r} is {len(h)} chars"
            assert re.fullmatch(r"[0-9a-f]{16}", h), f"not hex: {h!r}"

    def test_hash_matches_sha256_prefix(self):
        content = "test content"
        docs = {"doc": content}
        result = self.cap.capture(docs)
        expected = hashlib.sha256(content.encode()).hexdigest()[:16]
        assert result.doc_hashes["doc"] == expected

    def test_auto_generates_snapshot_id_when_empty(self):
        result = self.cap.capture({"x": "y"})
        assert result.snapshot_id.startswith("snap-")

    def test_auto_id_format_timestamp(self):
        result = self.cap.capture({"x": "y"})
        # snap-YYYYMMDDHHMMSS  → 5 + 14 = 19 chars
        assert re.fullmatch(r"snap-\d{14}", result.snapshot_id), result.snapshot_id

    def test_custom_snapshot_id_preserved(self):
        result = self.cap.capture({"x": "y"}, snapshot_id="my-custom-id")
        assert result.snapshot_id == "my-custom-id"

    def test_empty_docs(self):
        result = self.cap.capture({})
        assert result.doc_count == 0
        assert result.total_bytes == 0
        assert result.doc_hashes == {}

    def test_metadata_stored(self):
        result = self.cap.capture({"x": "y"}, metadata={"env": "test", "version": 2})
        assert result.metadata == {"env": "test", "version": 2}

    def test_metadata_none_becomes_empty_dict(self):
        result = self.cap.capture({"x": "y"}, metadata=None)
        assert result.metadata == {}

    def test_ts_is_non_empty_string(self):
        result = self.cap.capture({"x": "y"})
        assert isinstance(result.ts, str)
        assert len(result.ts) > 0

    def test_different_docs_different_hashes(self):
        r1 = self.cap.capture({"doc": "version one"})
        r2 = self.cap.capture({"doc": "version two"})
        assert r1.doc_hashes["doc"] != r2.doc_hashes["doc"]

    def test_same_docs_same_hashes(self):
        docs = {"doc": "stable content"}
        r1 = self.cap.capture(docs)
        r2 = self.cap.capture(docs)
        assert r1.doc_hashes == r2.doc_hashes


# ===========================================================================
# SnapshotCapture.capture_directory
# ===========================================================================

class TestSnapshotCaptureDirectory:
    def setup_method(self):
        self.cap = SnapshotCapture()

    def test_returns_captured_state(self, tmp_path):
        (tmp_path / "a.md").write_text("hello")
        result = self.cap.capture_directory(tmp_path)
        assert isinstance(result, CapturedState)

    def test_doc_ids_are_relative_paths(self, tmp_path):
        (tmp_path / "readme.md").write_text("content")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "notes.md").write_text("notes")
        result = self.cap.capture_directory(tmp_path)
        assert "readme.md" in result.doc_hashes
        assert str(Path("sub") / "notes.md") in result.doc_hashes

    def test_doc_count_matches_files(self, tmp_path):
        for i in range(4):
            (tmp_path / f"doc{i}.md").write_text(f"content {i}")
        result = self.cap.capture_directory(tmp_path)
        assert result.doc_count == 4

    def test_pattern_filter_md(self, tmp_path):
        (tmp_path / "keep.md").write_text("md file")
        (tmp_path / "skip.txt").write_text("txt file")
        result = self.cap.capture_directory(tmp_path, pattern="*.md")
        assert result.doc_count == 1
        assert "keep.md" in result.doc_hashes

    def test_pattern_filter_txt(self, tmp_path):
        (tmp_path / "a.md").write_text("md")
        (tmp_path / "b.txt").write_text("txt")
        result = self.cap.capture_directory(tmp_path, pattern="*.txt")
        assert "b.txt" in result.doc_hashes
        assert "a.md" not in result.doc_hashes

    def test_empty_directory(self, tmp_path):
        result = self.cap.capture_directory(tmp_path)
        assert result.doc_count == 0
        assert result.doc_hashes == {}

    def test_custom_snapshot_id(self, tmp_path):
        (tmp_path / "a.md").write_text("x")
        result = self.cap.capture_directory(tmp_path, snapshot_id="dir-snap-1")
        assert result.snapshot_id == "dir-snap-1"

    def test_auto_snapshot_id_when_not_provided(self, tmp_path):
        (tmp_path / "a.md").write_text("x")
        result = self.cap.capture_directory(tmp_path)
        assert result.snapshot_id.startswith("snap-")


# ===========================================================================
# SnapshotMeta
# ===========================================================================

class TestSnapshotMeta:
    def test_size_kb_exact(self):
        m = SnapshotMeta(
            snapshot_id="x", ts="t", doc_count=1, total_bytes=2048
        )
        assert m.size_kb() == 2.0

    def test_size_kb_fractional(self):
        m = SnapshotMeta(
            snapshot_id="x", ts="t", doc_count=1, total_bytes=1536
        )
        assert m.size_kb() == 1.5

    def test_size_kb_zero(self):
        m = SnapshotMeta(
            snapshot_id="x", ts="t", doc_count=0, total_bytes=0
        )
        assert m.size_kb() == 0.0

    def test_label_default_empty(self):
        m = SnapshotMeta(snapshot_id="x", ts="t", doc_count=0, total_bytes=0)
        assert m.label == ""

    def test_label_set(self):
        m = SnapshotMeta(
            snapshot_id="x", ts="t", doc_count=0, total_bytes=0, label="baseline"
        )
        assert m.label == "baseline"


# ===========================================================================
# SnapshotStore
# ===========================================================================

class TestSnapshotStore:
    def setup_method(self):
        self.store = SnapshotStore()  # in-memory

    def teardown_method(self):
        self.store.close()

    def _make_and_save(self, sid: str, ts: str = "2026-01-01T00:00:00", label: str = "") -> CapturedState:
        cap = SnapshotCapture()
        state = cap.capture({"doc": "content"}, snapshot_id=sid)
        object.__setattr__(state, "ts", ts)  # override ts for ordering tests
        self.store.save(state, label=label)
        return state

    # --- save / load ---

    def test_save_and_load_round_trip(self):
        state = SnapshotCapture().capture({"a": "hello"}, snapshot_id="sl-1")
        self.store.save(state)
        loaded = self.store.load("sl-1")
        assert loaded is not None
        assert loaded.snapshot_id == "sl-1"
        assert loaded.doc_hashes == state.doc_hashes
        assert loaded.doc_count == state.doc_count
        assert loaded.total_bytes == state.total_bytes

    def test_load_missing_returns_none(self):
        result = self.store.load("does-not-exist")
        assert result is None

    def test_save_preserves_label(self):
        state = SnapshotCapture().capture({"x": "y"}, snapshot_id="lbl-1")
        self.store.save(state, label="my-label")
        metas = self.store.list_snapshots()
        assert metas[0].label == "my-label"

    def test_save_replaces_on_duplicate_id(self):
        cap = SnapshotCapture()
        s1 = cap.capture({"doc": "v1"}, snapshot_id="dup-1")
        s2 = cap.capture({"doc": "v2"}, snapshot_id="dup-1")
        self.store.save(s1)
        self.store.save(s2)
        loaded = self.store.load("dup-1")
        assert loaded.doc_hashes == s2.doc_hashes

    # --- list_snapshots ---

    def test_list_snapshots_returns_list(self):
        self._make_and_save("ls-1")
        result = self.store.list_snapshots()
        assert isinstance(result, list)

    def test_list_snapshots_returns_meta_objects(self):
        self._make_and_save("ls-2")
        result = self.store.list_snapshots()
        assert all(isinstance(m, SnapshotMeta) for m in result)

    def test_list_snapshots_ordered_desc(self):
        self._make_and_save("ls-a", ts="2026-01-01T00:00:00")
        self._make_and_save("ls-b", ts="2026-06-01T00:00:00")
        self._make_and_save("ls-c", ts="2026-03-01T00:00:00")
        result = self.store.list_snapshots()
        ids = [m.snapshot_id for m in result]
        # ls-b (June) > ls-c (March) > ls-a (Jan)
        assert ids == ["ls-b", "ls-c", "ls-a"]

    def test_list_snapshots_empty_store(self):
        assert self.store.list_snapshots() == []

    def test_list_snapshots_meta_fields(self):
        state = SnapshotCapture().capture({"doc": "abc"}, snapshot_id="mf-1")
        self.store.save(state, label="tag1")
        metas = self.store.list_snapshots()
        m = metas[0]
        assert m.snapshot_id == "mf-1"
        assert m.doc_count == state.doc_count
        assert m.total_bytes == state.total_bytes
        assert m.label == "tag1"

    # --- delete ---

    def test_delete_returns_true_when_found(self):
        self._make_and_save("del-1")
        assert self.store.delete("del-1") is True

    def test_delete_returns_false_when_missing(self):
        assert self.store.delete("not-there") is False

    def test_delete_removes_from_store(self):
        self._make_and_save("del-2")
        self.store.delete("del-2")
        assert self.store.load("del-2") is None

    def test_delete_reduces_count(self):
        self._make_and_save("cnt-1")
        self._make_and_save("cnt-2")
        assert self.store.count() == 2
        self.store.delete("cnt-1")
        assert self.store.count() == 1

    # --- count ---

    def test_count_empty(self):
        assert self.store.count() == 0

    def test_count_after_saves(self):
        self._make_and_save("c1")
        self._make_and_save("c2")
        self._make_and_save("c3")
        assert self.store.count() == 3

    # --- latest ---

    def test_latest_on_empty_store_returns_none(self):
        assert self.store.latest() is None

    def test_latest_returns_captured_state(self):
        self._make_and_save("lt-1")
        result = self.store.latest()
        assert isinstance(result, CapturedState)

    def test_latest_returns_most_recent(self):
        self._make_and_save("lt-a", ts="2026-01-01T00:00:00")
        self._make_and_save("lt-b", ts="2026-12-31T23:59:59")
        self._make_and_save("lt-c", ts="2026-06-15T12:00:00")
        latest = self.store.latest()
        assert latest.snapshot_id == "lt-b"


# ===========================================================================
# SnapshotDiff
# ===========================================================================

class TestSnapshotDiff:
    def _make_diff(
        self,
        added=0, removed=0, modified=0, unchanged=0,
        before_id="b", after_id="a",
    ) -> SnapshotDiff:
        return SnapshotDiff(
            snapshot_id_before=before_id,
            snapshot_id_after=after_id,
            added_docs=[f"add{i}" for i in range(added)],
            removed_docs=[f"rem{i}" for i in range(removed)],
            modified_docs=[f"mod{i}" for i in range(modified)],
            unchanged_docs=[f"unc{i}" for i in range(unchanged)],
        )

    def test_total_changes_all_zero(self):
        d = self._make_diff(unchanged=5)
        assert d.total_changes() == 0

    def test_total_changes_added_only(self):
        d = self._make_diff(added=3)
        assert d.total_changes() == 3

    def test_total_changes_removed_only(self):
        d = self._make_diff(removed=2)
        assert d.total_changes() == 2

    def test_total_changes_modified_only(self):
        d = self._make_diff(modified=4)
        assert d.total_changes() == 4

    def test_total_changes_mixed(self):
        d = self._make_diff(added=1, removed=2, modified=3, unchanged=10)
        assert d.total_changes() == 6

    def test_change_rate_no_docs(self):
        d = self._make_diff()
        assert d.change_rate() == 0.0

    def test_change_rate_all_unchanged(self):
        d = self._make_diff(unchanged=10)
        assert d.change_rate() == 0.0

    def test_change_rate_all_added(self):
        d = self._make_diff(added=5)
        assert d.change_rate() == 1.0

    def test_change_rate_half(self):
        d = self._make_diff(modified=2, unchanged=2)
        assert d.change_rate() == pytest.approx(0.5)

    def test_change_rate_mixed(self):
        d = self._make_diff(added=1, removed=1, modified=1, unchanged=7)
        # 3 changes out of 10 total
        assert d.change_rate() == pytest.approx(0.3)

    def test_summary_format(self):
        d = self._make_diff(added=3, removed=1, modified=2, unchanged=5)
        assert d.summary() == "+3 -1 ~2 =5"

    def test_summary_all_zeros(self):
        d = self._make_diff()
        assert d.summary() == "+0 -0 ~0 =0"

    def test_ids_preserved(self):
        d = SnapshotDiff(
            snapshot_id_before="before-snap",
            snapshot_id_after="after-snap",
        )
        assert d.snapshot_id_before == "before-snap"
        assert d.snapshot_id_after == "after-snap"


# ===========================================================================
# diff_snapshots
# ===========================================================================

class TestDiffSnapshots:
    def _state(self, sid: str, hashes: dict) -> CapturedState:
        return CapturedState(
            snapshot_id=sid,
            ts="2026-01-01T00:00:00",
            doc_count=len(hashes),
            total_bytes=0,
            doc_hashes=hashes,
        )

    def test_identical_snapshots_all_unchanged(self):
        hashes = {"a": "h1", "b": "h2", "c": "h3"}
        before = self._state("b1", hashes)
        after = self._state("a1", dict(hashes))
        diff = diff_snapshots(before, after)
        assert diff.added_docs == []
        assert diff.removed_docs == []
        assert diff.modified_docs == []
        assert sorted(diff.unchanged_docs) == ["a", "b", "c"]

    def test_added_doc(self):
        before = self._state("b", {"a": "h1"})
        after = self._state("a", {"a": "h1", "new": "h99"})
        diff = diff_snapshots(before, after)
        assert "new" in diff.added_docs
        assert "a" in diff.unchanged_docs
        assert diff.removed_docs == []

    def test_removed_doc(self):
        before = self._state("b", {"a": "h1", "gone": "h2"})
        after = self._state("a", {"a": "h1"})
        diff = diff_snapshots(before, after)
        assert "gone" in diff.removed_docs
        assert "a" in diff.unchanged_docs

    def test_modified_doc(self):
        before = self._state("b", {"doc": "old_hash_1234"})
        after = self._state("a", {"doc": "new_hash_5678"})
        diff = diff_snapshots(before, after)
        assert "doc" in diff.modified_docs
        assert diff.added_docs == []
        assert diff.removed_docs == []
        assert diff.unchanged_docs == []

    def test_unchanged_doc(self):
        before = self._state("b", {"stable": "same_hash_xxx"})
        after = self._state("a", {"stable": "same_hash_xxx"})
        diff = diff_snapshots(before, after)
        assert "stable" in diff.unchanged_docs
        assert diff.modified_docs == []

    def test_empty_before_and_after(self):
        before = self._state("b", {})
        after = self._state("a", {})
        diff = diff_snapshots(before, after)
        assert diff.added_docs == []
        assert diff.removed_docs == []
        assert diff.modified_docs == []
        assert diff.unchanged_docs == []
        assert diff.total_changes() == 0

    def test_empty_before_all_added(self):
        before = self._state("b", {})
        after = self._state("a", {"x": "h1", "y": "h2"})
        diff = diff_snapshots(before, after)
        assert sorted(diff.added_docs) == ["x", "y"]
        assert diff.removed_docs == []
        assert diff.unchanged_docs == []

    def test_empty_after_all_removed(self):
        before = self._state("b", {"x": "h1", "y": "h2"})
        after = self._state("a", {})
        diff = diff_snapshots(before, after)
        assert sorted(diff.removed_docs) == ["x", "y"]
        assert diff.added_docs == []
        assert diff.unchanged_docs == []

    def test_mixed_case(self):
        before = self._state("b", {
            "keep": "hk",
            "change": "hc_old",
            "remove": "hr",
        })
        after = self._state("a", {
            "keep": "hk",
            "change": "hc_new",
            "add": "ha",
        })
        diff = diff_snapshots(before, after)
        assert diff.added_docs == ["add"]
        assert diff.removed_docs == ["remove"]
        assert diff.modified_docs == ["change"]
        assert diff.unchanged_docs == ["keep"]

    def test_snapshot_ids_assigned(self):
        before = self._state("snap-before", {})
        after = self._state("snap-after", {})
        diff = diff_snapshots(before, after)
        assert diff.snapshot_id_before == "snap-before"
        assert diff.snapshot_id_after == "snap-after"

    def test_returns_snapshot_diff_instance(self):
        before = self._state("b", {})
        after = self._state("a", {})
        result = diff_snapshots(before, after)
        assert isinstance(result, SnapshotDiff)

    def test_lists_are_sorted(self):
        before = self._state("b", {"z": "h1", "m": "h2", "a": "h3"})
        after = self._state("a", {"z": "h1", "m": "h2_new", "b": "h99"})
        diff = diff_snapshots(before, after)
        assert diff.added_docs == sorted(diff.added_docs)
        assert diff.removed_docs == sorted(diff.removed_docs)
        assert diff.modified_docs == sorted(diff.modified_docs)
        assert diff.unchanged_docs == sorted(diff.unchanged_docs)
