"""Tests for the doc_clip module."""

from __future__ import annotations

import pytest

from docstoolkit.doc_clip import Clip, ClipCollection, DocClip


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------
class TestClip:
    def test_create_minimal(self):
        c = Clip(clip_id="c1", doc_id="d1", text="hello")
        assert c.clip_id == "c1"
        assert c.doc_id == "d1"
        assert c.text == "hello"
        assert c.start == 0
        assert c.end == 0
        assert c.created_at == 0.0
        assert c.note is None
        assert c.tags == []

    def test_create_full(self):
        c = Clip(
            clip_id="c2",
            doc_id="d2",
            text="world",
            start=3,
            end=8,
            created_at=100.0,
            note="great",
            tags=["a", "b"],
        )
        assert c.start == 3
        assert c.end == 8
        assert c.created_at == 100.0
        assert c.note == "great"
        assert c.tags == ["a", "b"]

    def test_tags_default_independent(self):
        c1 = Clip(clip_id="a", doc_id="d", text="x")
        c2 = Clip(clip_id="b", doc_id="d", text="y")
        c1.tags.append("t")
        assert c2.tags == []


class TestClipCollection:
    def test_create_minimal(self):
        c = ClipCollection(name="lib")
        assert c.name == "lib"
        assert c.clip_ids == []
        assert c.created_at == 0.0

    def test_create_full(self):
        c = ClipCollection(name="x", clip_ids=["a", "b"], created_at=42.0)
        assert c.clip_ids == ["a", "b"]
        assert c.created_at == 42.0

    def test_clip_ids_default_independent(self):
        a = ClipCollection(name="a")
        b = ClipCollection(name="b")
        a.clip_ids.append("x")
        assert b.clip_ids == []


# ---------------------------------------------------------------------------
# Basic clip
# ---------------------------------------------------------------------------
class TestClipBasic:
    def test_clip_creates_entry(self):
        dc = DocClip()
        c = dc.clip("d1", "hello world")
        assert c.doc_id == "d1"
        assert c.text == "hello world"
        assert c.clip_id

    def test_clip_unique_ids(self):
        dc = DocClip()
        a = dc.clip("d", "x")
        b = dc.clip("d", "x")
        assert a.clip_id != b.clip_id

    def test_clip_with_metadata(self):
        dc = DocClip()
        c = dc.clip(
            "d1",
            "hello",
            start=1,
            end=6,
            note="memo",
            tags=["t1"],
            now=123.0,
        )
        assert c.start == 1
        assert c.end == 6
        assert c.note == "memo"
        assert c.tags == ["t1"]
        assert c.created_at == 123.0

    def test_clip_default_tags_isolated(self):
        dc = DocClip()
        a = dc.clip("d", "a")
        b = dc.clip("d", "b")
        a.tags.append("x")
        assert b.tags == []

    def test_clip_persists_in_store(self):
        dc = DocClip()
        c = dc.clip("d1", "hi")
        assert dc.get(c.clip_id) is c


# ---------------------------------------------------------------------------
# clip_from_doc
# ---------------------------------------------------------------------------
class TestClipFromDoc:
    def test_extracts_substring(self):
        dc = DocClip()
        c = dc.clip_from_doc("d1", "hello world", 6, 11)
        assert c is not None
        assert c.text == "world"
        assert c.start == 6
        assert c.end == 11

    def test_extract_full(self):
        dc = DocClip()
        c = dc.clip_from_doc("d1", "abc", 0, 3)
        assert c is not None
        assert c.text == "abc"

    def test_negative_start_invalid(self):
        dc = DocClip()
        assert dc.clip_from_doc("d", "hello", -1, 3) is None

    def test_negative_end_invalid(self):
        dc = DocClip()
        assert dc.clip_from_doc("d", "hello", 0, -1) is None

    def test_end_less_than_start_invalid(self):
        dc = DocClip()
        assert dc.clip_from_doc("d", "hello", 4, 2) is None

    def test_start_beyond_length_invalid(self):
        dc = DocClip()
        assert dc.clip_from_doc("d", "hello", 10, 12) is None

    def test_end_beyond_length_invalid(self):
        dc = DocClip()
        assert dc.clip_from_doc("d", "hello", 0, 10) is None

    def test_empty_slice_at_end(self):
        dc = DocClip()
        c = dc.clip_from_doc("d", "hello", 5, 5)
        assert c is not None
        assert c.text == ""

    def test_with_note_and_tags(self):
        dc = DocClip()
        c = dc.clip_from_doc(
            "d", "hello world", 0, 5, note="m", tags=["t"], now=1.0
        )
        assert c.note == "m"
        assert c.tags == ["t"]
        assert c.created_at == 1.0


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------
class TestGet:
    def test_get_existing(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        assert dc.get(c.clip_id) is c

    def test_get_missing(self):
        dc = DocClip()
        assert dc.get("nope") is None


# ---------------------------------------------------------------------------
# update_note
# ---------------------------------------------------------------------------
class TestUpdateNote:
    def test_update_existing(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        assert dc.update_note(c.clip_id, "new") is True
        assert dc.get(c.clip_id).note == "new"

    def test_update_missing(self):
        dc = DocClip()
        assert dc.update_note("nope", "n") is False

    def test_overwrite_note(self):
        dc = DocClip()
        c = dc.clip("d", "x", note="old")
        dc.update_note(c.clip_id, "new")
        assert dc.get(c.clip_id).note == "new"


# ---------------------------------------------------------------------------
# add_tag
# ---------------------------------------------------------------------------
class TestAddTag:
    def test_add_tag(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        assert dc.add_tag(c.clip_id, "t1") is True
        assert "t1" in dc.get(c.clip_id).tags

    def test_add_duplicate(self):
        dc = DocClip()
        c = dc.clip("d", "x", tags=["t1"])
        assert dc.add_tag(c.clip_id, "t1") is False

    def test_add_to_missing(self):
        dc = DocClip()
        assert dc.add_tag("none", "t") is False


# ---------------------------------------------------------------------------
# remove_tag
# ---------------------------------------------------------------------------
class TestRemoveTag:
    def test_remove_existing(self):
        dc = DocClip()
        c = dc.clip("d", "x", tags=["a", "b"])
        assert dc.remove_tag(c.clip_id, "a") is True
        assert dc.get(c.clip_id).tags == ["b"]

    def test_remove_missing_tag(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        assert dc.remove_tag(c.clip_id, "no") is False

    def test_remove_from_missing_clip(self):
        dc = DocClip()
        assert dc.remove_tag("nope", "t") is False


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------
class TestDelete:
    def test_delete_existing(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        assert dc.delete(c.clip_id) is True
        assert dc.get(c.clip_id) is None

    def test_delete_missing(self):
        dc = DocClip()
        assert dc.delete("none") is False

    def test_delete_removes_from_collections(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        dc.create_collection("L", [c.clip_id])
        dc.delete(c.clip_id)
        assert dc.get_collection("L").clip_ids == []


# ---------------------------------------------------------------------------
# clips_for_doc
# ---------------------------------------------------------------------------
class TestClipsForDoc:
    def test_returns_matching(self):
        dc = DocClip()
        a = dc.clip("d1", "a")
        b = dc.clip("d1", "b")
        dc.clip("d2", "c")
        ids = {x.clip_id for x in dc.clips_for_doc("d1")}
        assert ids == {a.clip_id, b.clip_id}

    def test_empty_when_no_clips(self):
        dc = DocClip()
        assert dc.clips_for_doc("d") == []

    def test_unknown_doc(self):
        dc = DocClip()
        dc.clip("d1", "x")
        assert dc.clips_for_doc("zzz") == []


# ---------------------------------------------------------------------------
# clips_with_tag
# ---------------------------------------------------------------------------
class TestClipsWithTag:
    def test_returns_matching(self):
        dc = DocClip()
        a = dc.clip("d", "a", tags=["x"])
        dc.clip("d", "b", tags=["y"])
        result = dc.clips_with_tag("x")
        assert len(result) == 1
        assert result[0].clip_id == a.clip_id

    def test_no_matches(self):
        dc = DocClip()
        dc.clip("d", "a", tags=["x"])
        assert dc.clips_with_tag("zz") == []


# ---------------------------------------------------------------------------
# search_clips
# ---------------------------------------------------------------------------
class TestSearchClips:
    def test_search_in_text(self):
        dc = DocClip()
        a = dc.clip("d", "hello world")
        dc.clip("d", "foo bar")
        result = dc.search_clips("hello")
        assert len(result) == 1
        assert result[0].clip_id == a.clip_id

    def test_search_in_note(self):
        dc = DocClip()
        a = dc.clip("d", "xxx", note="important memo")
        dc.clip("d", "yyy", note=None)
        result = dc.search_clips("memo")
        assert len(result) == 1
        assert result[0].clip_id == a.clip_id

    def test_search_case_insensitive(self):
        dc = DocClip()
        dc.clip("d", "Hello World")
        result = dc.search_clips("hello")
        assert len(result) == 1

    def test_search_case_sensitive(self):
        dc = DocClip()
        dc.clip("d", "Hello World")
        result = dc.search_clips("hello", case_sensitive=True)
        assert result == []

    def test_search_empty_query(self):
        dc = DocClip()
        dc.clip("d", "x")
        assert dc.search_clips("") == []

    def test_search_no_double_count(self):
        dc = DocClip()
        c = dc.clip("d", "memo here", note="memo too")
        result = dc.search_clips("memo")
        assert len(result) == 1
        assert result[0].clip_id == c.clip_id


# ---------------------------------------------------------------------------
# create_collection
# ---------------------------------------------------------------------------
class TestCreateCollection:
    def test_create_empty(self):
        dc = DocClip()
        c = dc.create_collection("L")
        assert c.name == "L"
        assert c.clip_ids == []

    def test_create_with_clip_ids(self):
        dc = DocClip()
        a = dc.clip("d", "a")
        b = dc.clip("d", "b")
        coll = dc.create_collection("L", [a.clip_id, b.clip_id])
        assert coll.clip_ids == [a.clip_id, b.clip_id]

    def test_create_filters_unknown_ids(self):
        dc = DocClip()
        a = dc.clip("d", "a")
        coll = dc.create_collection("L", [a.clip_id, "ghost"])
        assert coll.clip_ids == [a.clip_id]

    def test_create_duplicate_name_returns_existing(self):
        dc = DocClip()
        first = dc.create_collection("L")
        second = dc.create_collection("L")
        assert first is second

    def test_create_with_now(self):
        dc = DocClip()
        coll = dc.create_collection("L", now=99.0)
        assert coll.created_at == 99.0


# ---------------------------------------------------------------------------
# add_to_collection
# ---------------------------------------------------------------------------
class TestAddToCollection:
    def test_add(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        dc.create_collection("L")
        assert dc.add_to_collection("L", c.clip_id) is True
        assert dc.get_collection("L").clip_ids == [c.clip_id]

    def test_add_to_missing_collection(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        assert dc.add_to_collection("missing", c.clip_id) is False

    def test_add_missing_clip(self):
        dc = DocClip()
        dc.create_collection("L")
        assert dc.add_to_collection("L", "nope") is False

    def test_add_duplicate(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        dc.create_collection("L", [c.clip_id])
        assert dc.add_to_collection("L", c.clip_id) is False


# ---------------------------------------------------------------------------
# remove_from_collection
# ---------------------------------------------------------------------------
class TestRemoveFromCollection:
    def test_remove(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        dc.create_collection("L", [c.clip_id])
        assert dc.remove_from_collection("L", c.clip_id) is True
        assert dc.get_collection("L").clip_ids == []

    def test_remove_missing_collection(self):
        dc = DocClip()
        assert dc.remove_from_collection("zz", "any") is False

    def test_remove_missing_clip(self):
        dc = DocClip()
        dc.create_collection("L")
        assert dc.remove_from_collection("L", "nope") is False


# ---------------------------------------------------------------------------
# collections_for_clip
# ---------------------------------------------------------------------------
class TestCollectionsForClip:
    def test_returns_matching(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        dc.create_collection("A", [c.clip_id])
        dc.create_collection("B", [c.clip_id])
        dc.create_collection("C")
        names = {coll.name for coll in dc.collections_for_clip(c.clip_id)}
        assert names == {"A", "B"}

    def test_no_collections(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        assert dc.collections_for_clip(c.clip_id) == []

    def test_unknown_clip(self):
        dc = DocClip()
        dc.create_collection("A")
        assert dc.collections_for_clip("nope") == []


# ---------------------------------------------------------------------------
# get_collection
# ---------------------------------------------------------------------------
class TestGetCollection:
    def test_get(self):
        dc = DocClip()
        dc.create_collection("L")
        assert dc.get_collection("L").name == "L"

    def test_get_missing(self):
        dc = DocClip()
        assert dc.get_collection("zz") is None


# ---------------------------------------------------------------------------
# delete_collection
# ---------------------------------------------------------------------------
class TestDeleteCollection:
    def test_delete(self):
        dc = DocClip()
        dc.create_collection("L")
        assert dc.delete_collection("L") is True
        assert dc.get_collection("L") is None

    def test_delete_missing(self):
        dc = DocClip()
        assert dc.delete_collection("zz") is False

    def test_delete_does_not_delete_clips(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        dc.create_collection("L", [c.clip_id])
        dc.delete_collection("L")
        assert dc.get(c.clip_id) is not None


# ---------------------------------------------------------------------------
# export_collection
# ---------------------------------------------------------------------------
class TestExportCollection:
    def test_export_concatenates(self):
        dc = DocClip()
        a = dc.clip("d", "alpha")
        b = dc.clip("d", "beta")
        dc.create_collection("L", [a.clip_id, b.clip_id])
        out = dc.export_collection("L")
        assert "alpha" in out
        assert "beta" in out
        assert "---" in out

    def test_export_preserves_order(self):
        dc = DocClip()
        a = dc.clip("d", "alpha")
        b = dc.clip("d", "beta")
        dc.create_collection("L", [b.clip_id, a.clip_id])
        out = dc.export_collection("L")
        assert out.index("beta") < out.index("alpha")

    def test_export_missing_collection(self):
        dc = DocClip()
        assert dc.export_collection("zz") == ""

    def test_export_empty_collection(self):
        dc = DocClip()
        dc.create_collection("L")
        assert dc.export_collection("L") == ""

    def test_export_skips_deleted_clips(self):
        dc = DocClip()
        a = dc.clip("d", "alpha")
        b = dc.clip("d", "beta")
        dc.create_collection("L", [a.clip_id, b.clip_id])
        # corrupt: pretend a was deleted but its id remains
        # (use real delete after collection creation)
        # Note: delete() also removes from collection. Use raw store manipulation.
        # We bypass the public API to ensure export tolerates stale ids.
        del dc._clips[a.clip_id]
        out = dc.export_collection("L")
        assert "alpha" not in out
        assert "beta" in out


# ---------------------------------------------------------------------------
# Counters
# ---------------------------------------------------------------------------
class TestTotalClips:
    def test_starts_zero(self):
        assert DocClip().total_clips == 0

    def test_increments(self):
        dc = DocClip()
        dc.clip("d", "x")
        dc.clip("d", "y")
        assert dc.total_clips == 2

    def test_decrements_on_delete(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        dc.delete(c.clip_id)
        assert dc.total_clips == 0


class TestTotalCollections:
    def test_starts_zero(self):
        assert DocClip().total_collections == 0

    def test_increments(self):
        dc = DocClip()
        dc.create_collection("a")
        dc.create_collection("b")
        assert dc.total_collections == 2

    def test_decrements_on_delete(self):
        dc = DocClip()
        dc.create_collection("a")
        dc.delete_collection("a")
        assert dc.total_collections == 0


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clears_clips(self):
        dc = DocClip()
        dc.clip("d", "x")
        dc.clear()
        assert dc.total_clips == 0

    def test_clears_collections(self):
        dc = DocClip()
        dc.create_collection("L")
        dc.clear()
        assert dc.total_collections == 0

    def test_clear_idempotent(self):
        dc = DocClip()
        dc.clear()
        dc.clear()
        assert dc.total_clips == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_clip_empty_text(self):
        dc = DocClip()
        c = dc.clip("d", "")
        assert c.text == ""
        assert dc.total_clips == 1

    def test_clip_from_doc_empty_source(self):
        dc = DocClip()
        c = dc.clip_from_doc("d", "", 0, 0)
        assert c is not None
        assert c.text == ""

    def test_clip_from_doc_none_source(self):
        dc = DocClip()
        assert dc.clip_from_doc("d", None, 0, 0) is None

    def test_search_returns_independent_list(self):
        dc = DocClip()
        dc.clip("d", "hello")
        a = dc.search_clips("hello")
        a.clear()
        assert len(dc.search_clips("hello")) == 1

    def test_clips_for_doc_returns_independent_list(self):
        dc = DocClip()
        dc.clip("d", "x")
        out = dc.clips_for_doc("d")
        out.clear()
        assert len(dc.clips_for_doc("d")) == 1

    def test_clip_ids_are_strings(self):
        dc = DocClip()
        c = dc.clip("d", "x")
        assert isinstance(c.clip_id, str)
        assert len(c.clip_id) > 0
