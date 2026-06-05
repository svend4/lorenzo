"""Tests for ``docstoolkit.doc_bookmark``."""
from __future__ import annotations

import time

import pytest

from docstoolkit.doc_bookmark import (
    Bookmark,
    DocBookmark,
    Folder,
    UserBookmarkStats,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestBookmark:
    def test_minimal_construction(self):
        bm = Bookmark(bookmark_id="b1", user_id="u1", doc_id="d1")
        assert bm.bookmark_id == "b1"
        assert bm.folder is None
        assert bm.tags == []
        assert bm.visit_count == 0

    def test_full_construction(self):
        bm = Bookmark(
            bookmark_id="b1",
            user_id="u1",
            doc_id="d1",
            folder="f1",
            tags=["a", "b"],
            note="hi",
            order=3,
            created_at=10.0,
            last_visited=20.0,
            visit_count=2,
        )
        assert bm.note == "hi"
        assert bm.tags == ["a", "b"]
        assert bm.last_visited == 20.0

    def test_tags_default_factory_independent(self):
        a = Bookmark(bookmark_id="a", user_id="u", doc_id="d")
        b = Bookmark(bookmark_id="b", user_id="u", doc_id="d")
        a.tags.append("x")
        assert b.tags == []


class TestFolder:
    def test_construction(self):
        f = Folder(folder_id="f1", user_id="u1", name="Reading")
        assert f.parent_folder is None
        assert f.name == "Reading"

    def test_with_parent(self):
        f = Folder(
            folder_id="f1", user_id="u1", name="Sub", parent_folder="root"
        )
        assert f.parent_folder == "root"


class TestUserBookmarkStats:
    def test_construction(self):
        s = UserBookmarkStats(
            user_id="u1",
            total_bookmarks=3,
            total_folders=1,
            unique_docs=2,
            unique_tags=4,
            most_visited=[("d1", 5)],
        )
        assert s.user_id == "u1"
        assert s.most_visited == [("d1", 5)]


# ---------------------------------------------------------------------------
# Add / remove / update
# ---------------------------------------------------------------------------


class TestAddBookmark:
    def test_basic_add(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        assert bm.user_id == "u1"
        assert bm.doc_id == "d1"
        assert bm.folder is None
        assert bm.tags == []
        assert bm.order == 0
        assert bm.created_at > 0

    def test_add_with_folder_and_tags(self):
        db = DocBookmark()
        bm = db.add_bookmark(
            "u1", "d1", folder="f1", tags=["x", "y"], note="hello"
        )
        assert bm.folder == "f1"
        assert bm.tags == ["x", "y"]
        assert bm.note == "hello"

    def test_add_with_explicit_now(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1", now=42.0)
        assert bm.created_at == 42.0

    def test_unique_ids(self):
        db = DocBookmark()
        a = db.add_bookmark("u1", "d1")
        b = db.add_bookmark("u1", "d2")
        assert a.bookmark_id != b.bookmark_id

    def test_order_increments_within_folder(self):
        db = DocBookmark()
        a = db.add_bookmark("u1", "d1")
        b = db.add_bookmark("u1", "d2")
        c = db.add_bookmark("u1", "d3", folder="f1")
        d = db.add_bookmark("u1", "d4", folder="f1")
        assert (a.order, b.order) == (0, 1)
        assert (c.order, d.order) == (0, 1)

    def test_order_separate_per_user(self):
        db = DocBookmark()
        a = db.add_bookmark("u1", "d1")
        b = db.add_bookmark("u2", "d1")
        assert a.order == 0
        assert b.order == 0

    def test_tags_copied_not_referenced(self):
        db = DocBookmark()
        tags = ["x"]
        bm = db.add_bookmark("u1", "d1", tags=tags)
        tags.append("y")
        assert bm.tags == ["x"]


class TestRemoveBookmark:
    def test_remove_existing(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        assert db.remove_bookmark(bm.bookmark_id) is True
        assert db.get_bookmark(bm.bookmark_id) is None

    def test_remove_missing(self):
        db = DocBookmark()
        assert db.remove_bookmark("nope") is False

    def test_remove_decrements_total(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        db.add_bookmark("u1", "d2")
        db.remove_bookmark(bm.bookmark_id)
        assert db.total_bookmarks == 1


class TestUpdateBookmark:
    def test_update_folder(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        assert db.update_bookmark(bm.bookmark_id, folder="f1") is True
        assert db.get_bookmark(bm.bookmark_id).folder == "f1"

    def test_update_tags(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1", tags=["a"])
        db.update_bookmark(bm.bookmark_id, tags=["b", "c"])
        assert db.get_bookmark(bm.bookmark_id).tags == ["b", "c"]

    def test_update_note(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        db.update_bookmark(bm.bookmark_id, note="hello")
        assert db.get_bookmark(bm.bookmark_id).note == "hello"

    def test_update_missing(self):
        db = DocBookmark()
        assert db.update_bookmark("nope", note="x") is False

    def test_update_none_args_keep_existing(self):
        db = DocBookmark()
        bm = db.add_bookmark(
            "u1", "d1", folder="f1", tags=["x"], note="orig"
        )
        db.update_bookmark(bm.bookmark_id)
        out = db.get_bookmark(bm.bookmark_id)
        assert out.folder == "f1"
        assert out.tags == ["x"]
        assert out.note == "orig"


# ---------------------------------------------------------------------------
# Folder operations on bookmarks
# ---------------------------------------------------------------------------


class TestMoveToFolder:
    def test_move_to_folder(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        assert db.move_to_folder(bm.bookmark_id, "f1") is True
        assert db.get_bookmark(bm.bookmark_id).folder == "f1"

    def test_move_to_root(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1", folder="f1")
        assert db.move_to_folder(bm.bookmark_id, None) is True
        assert db.get_bookmark(bm.bookmark_id).folder is None

    def test_move_assigns_next_order(self):
        db = DocBookmark()
        a = db.add_bookmark("u1", "d1", folder="f1")
        b = db.add_bookmark("u1", "d2", folder="f1")
        c = db.add_bookmark("u1", "d3")
        db.move_to_folder(c.bookmark_id, "f1")
        assert db.get_bookmark(c.bookmark_id).order == 2

    def test_move_missing(self):
        db = DocBookmark()
        assert db.move_to_folder("nope", "f1") is False


class TestAddTag:
    def test_add_tag_to_empty(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        assert db.add_tag(bm.bookmark_id, "x") is True
        assert db.get_bookmark(bm.bookmark_id).tags == ["x"]

    def test_add_tag_existing_no_dup(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1", tags=["x"])
        db.add_tag(bm.bookmark_id, "x")
        assert db.get_bookmark(bm.bookmark_id).tags == ["x"]

    def test_add_tag_missing(self):
        db = DocBookmark()
        assert db.add_tag("nope", "x") is False


class TestRemoveTag:
    def test_remove_existing_tag(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1", tags=["x", "y"])
        assert db.remove_tag(bm.bookmark_id, "x") is True
        assert db.get_bookmark(bm.bookmark_id).tags == ["y"]

    def test_remove_absent_tag(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1", tags=["x"])
        assert db.remove_tag(bm.bookmark_id, "z") is True
        assert db.get_bookmark(bm.bookmark_id).tags == ["x"]

    def test_remove_tag_missing_bookmark(self):
        db = DocBookmark()
        assert db.remove_tag("nope", "x") is False


# ---------------------------------------------------------------------------
# Visits / lookup
# ---------------------------------------------------------------------------


class TestRecordVisit:
    def test_first_visit(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        assert db.record_visit(bm.bookmark_id, now=10.0) is True
        out = db.get_bookmark(bm.bookmark_id)
        assert out.visit_count == 1
        assert out.last_visited == 10.0

    def test_multiple_visits(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        db.record_visit(bm.bookmark_id, now=10.0)
        db.record_visit(bm.bookmark_id, now=20.0)
        out = db.get_bookmark(bm.bookmark_id)
        assert out.visit_count == 2
        assert out.last_visited == 20.0

    def test_visit_missing(self):
        db = DocBookmark()
        assert db.record_visit("nope") is False

    def test_visit_default_now(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        before = time.time()
        db.record_visit(bm.bookmark_id)
        after = time.time()
        out = db.get_bookmark(bm.bookmark_id)
        assert before <= out.last_visited <= after


class TestGetBookmark:
    def test_get_existing(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        assert db.get_bookmark(bm.bookmark_id) is bm

    def test_get_missing(self):
        db = DocBookmark()
        assert db.get_bookmark("nope") is None


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------


class TestBookmarksForUser:
    def test_filter_by_user(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        db.add_bookmark("u2", "d2")
        out = db.bookmarks_for_user("u1")
        assert len(out) == 1
        assert out[0].user_id == "u1"

    def test_filter_by_folder(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        db.add_bookmark("u1", "d2", folder="f1")
        out = db.bookmarks_for_user("u1", folder="f1")
        assert len(out) == 1
        assert out[0].doc_id == "d2"

    def test_sort_by_order(self):
        db = DocBookmark()
        a = db.add_bookmark("u1", "d1")
        b = db.add_bookmark("u1", "d2")
        db.reorder(a.bookmark_id, 5)
        db.reorder(b.bookmark_id, 1)
        out = db.bookmarks_for_user("u1", sorted_by="order")
        assert [x.doc_id for x in out] == ["d2", "d1"]

    def test_sort_by_created_at(self):
        db = DocBookmark()
        a = db.add_bookmark("u1", "d1", now=10.0)
        b = db.add_bookmark("u1", "d2", now=5.0)
        out = db.bookmarks_for_user("u1", sorted_by="created_at")
        assert [x.doc_id for x in out] == ["d2", "d1"]

    def test_sort_by_visit_count(self):
        db = DocBookmark()
        a = db.add_bookmark("u1", "d1")
        b = db.add_bookmark("u1", "d2")
        db.record_visit(a.bookmark_id)
        db.record_visit(a.bookmark_id)
        db.record_visit(b.bookmark_id)
        out = db.bookmarks_for_user("u1", sorted_by="visit_count")
        assert out[0].doc_id == "d1"

    def test_sort_by_last_visited(self):
        db = DocBookmark()
        a = db.add_bookmark("u1", "d1")
        b = db.add_bookmark("u1", "d2")
        db.record_visit(a.bookmark_id, now=10.0)
        db.record_visit(b.bookmark_id, now=20.0)
        out = db.bookmarks_for_user("u1", sorted_by="last_visited")
        assert out[0].doc_id == "d2"

    def test_invalid_sort(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        with pytest.raises(ValueError):
            db.bookmarks_for_user("u1", sorted_by="bogus")

    def test_no_bookmarks_for_user(self):
        db = DocBookmark()
        assert db.bookmarks_for_user("ghost") == []


class TestBookmarksWithTag:
    def test_filter_by_tag(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1", tags=["x", "y"])
        db.add_bookmark("u1", "d2", tags=["y"])
        db.add_bookmark("u1", "d3", tags=["z"])
        out = db.bookmarks_with_tag("u1", "y")
        assert {b.doc_id for b in out} == {"d1", "d2"}

    def test_filter_per_user(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1", tags=["x"])
        db.add_bookmark("u2", "d2", tags=["x"])
        out = db.bookmarks_with_tag("u1", "x")
        assert len(out) == 1
        assert out[0].user_id == "u1"

    def test_no_match(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1", tags=["x"])
        assert db.bookmarks_with_tag("u1", "z") == []


class TestBookmarksForDoc:
    def test_all_users(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        db.add_bookmark("u2", "d1")
        db.add_bookmark("u3", "d2")
        out = db.bookmarks_for_doc("d1")
        assert {b.user_id for b in out} == {"u1", "u2"}

    def test_no_match(self):
        db = DocBookmark()
        assert db.bookmarks_for_doc("ghost") == []


class TestReorder:
    def test_reorder_existing(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        assert db.reorder(bm.bookmark_id, 42) is True
        assert db.get_bookmark(bm.bookmark_id).order == 42

    def test_reorder_missing(self):
        db = DocBookmark()
        assert db.reorder("nope", 1) is False


# ---------------------------------------------------------------------------
# Folders
# ---------------------------------------------------------------------------


class TestCreateFolder:
    def test_basic(self):
        db = DocBookmark()
        f = db.create_folder("u1", "Reading")
        assert f.user_id == "u1"
        assert f.name == "Reading"
        assert f.parent_folder is None
        assert f.created_at > 0

    def test_with_parent(self):
        db = DocBookmark()
        parent = db.create_folder("u1", "Root")
        child = db.create_folder("u1", "Sub", parent_folder=parent.folder_id)
        assert child.parent_folder == parent.folder_id

    def test_with_explicit_now(self):
        db = DocBookmark()
        f = db.create_folder("u1", "F", now=42.0)
        assert f.created_at == 42.0

    def test_unique_ids(self):
        db = DocBookmark()
        a = db.create_folder("u1", "A")
        b = db.create_folder("u1", "B")
        assert a.folder_id != b.folder_id


class TestDeleteFolder:
    def test_delete_existing(self):
        db = DocBookmark()
        f = db.create_folder("u1", "F")
        assert db.delete_folder(f.folder_id) is True
        assert db.folders_for_user("u1") == []

    def test_delete_missing(self):
        db = DocBookmark()
        assert db.delete_folder("nope") is False

    def test_delete_moves_bookmarks_to_root(self):
        db = DocBookmark()
        f = db.create_folder("u1", "F")
        bm = db.add_bookmark("u1", "d1", folder=f.folder_id)
        db.delete_folder(f.folder_id)
        assert db.get_bookmark(bm.bookmark_id).folder is None

    def test_delete_moves_bookmarks_to_other(self):
        db = DocBookmark()
        f1 = db.create_folder("u1", "F1")
        f2 = db.create_folder("u1", "F2")
        bm = db.add_bookmark("u1", "d1", folder=f1.folder_id)
        db.delete_folder(f1.folder_id, move_to=f2.folder_id)
        assert db.get_bookmark(bm.bookmark_id).folder == f2.folder_id


class TestFoldersForUser:
    def test_filter_by_user(self):
        db = DocBookmark()
        db.create_folder("u1", "A")
        db.create_folder("u1", "B")
        db.create_folder("u2", "C")
        out = db.folders_for_user("u1")
        assert {f.name for f in out} == {"A", "B"}

    def test_no_folders(self):
        db = DocBookmark()
        assert db.folders_for_user("ghost") == []


# ---------------------------------------------------------------------------
# Aggregates
# ---------------------------------------------------------------------------


class TestIsBookmarked:
    def test_true(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        assert db.is_bookmarked("u1", "d1") is True

    def test_false_diff_user(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        assert db.is_bookmarked("u2", "d1") is False

    def test_false_missing(self):
        db = DocBookmark()
        assert db.is_bookmarked("u1", "d1") is False


class TestTotalBookmarksForUser:
    def test_count(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        db.add_bookmark("u1", "d2")
        db.add_bookmark("u2", "d1")
        assert db.total_bookmarks_for_user("u1") == 2

    def test_zero(self):
        db = DocBookmark()
        assert db.total_bookmarks_for_user("ghost") == 0


class TestUserStats:
    def test_basic_stats(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1", tags=["x", "y"])
        db.add_bookmark("u1", "d2", tags=["y", "z"])
        db.create_folder("u1", "F")
        s = db.user_stats("u1")
        assert s.total_bookmarks == 2
        assert s.total_folders == 1
        assert s.unique_docs == 2
        assert s.unique_tags == 3

    def test_most_visited(self):
        db = DocBookmark()
        a = db.add_bookmark("u1", "d1")
        b = db.add_bookmark("u1", "d2")
        db.record_visit(a.bookmark_id)
        db.record_visit(a.bookmark_id)
        db.record_visit(a.bookmark_id)
        db.record_visit(b.bookmark_id)
        s = db.user_stats("u1", top_k=2)
        assert s.most_visited[0] == ("d1", 3)
        assert s.most_visited[1] == ("d2", 1)

    def test_top_k_limit(self):
        db = DocBookmark()
        for i in range(5):
            bm = db.add_bookmark("u1", f"d{i}")
            db.record_visit(bm.bookmark_id)
        s = db.user_stats("u1", top_k=2)
        assert len(s.most_visited) == 2

    def test_unvisited_excluded(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        s = db.user_stats("u1")
        assert s.most_visited == []

    def test_empty_user(self):
        db = DocBookmark()
        s = db.user_stats("ghost")
        assert s.total_bookmarks == 0
        assert s.most_visited == []


class TestPopularDocs:
    def test_counts_across_users(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        db.add_bookmark("u2", "d1")
        db.add_bookmark("u3", "d2")
        out = db.popular_docs()
        assert out[0] == ("d1", 2)

    def test_top_k_limit(self):
        db = DocBookmark()
        for i in range(5):
            db.add_bookmark(f"u{i}", "d1")
            db.add_bookmark(f"u{i}", "d2")
            db.add_bookmark(f"u{i}", "d3")
        out = db.popular_docs(top_k=2)
        assert len(out) == 2

    def test_empty(self):
        db = DocBookmark()
        assert db.popular_docs() == []


class TestTotalBookmarks:
    def test_zero(self):
        assert DocBookmark().total_bookmarks == 0

    def test_after_adds(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        db.add_bookmark("u2", "d2")
        assert db.total_bookmarks == 2


class TestTotalFolders:
    def test_zero(self):
        assert DocBookmark().total_folders == 0

    def test_after_creates(self):
        db = DocBookmark()
        db.create_folder("u1", "A")
        db.create_folder("u2", "B")
        assert db.total_folders == 2


class TestClear:
    def test_clear_bookmarks(self):
        db = DocBookmark()
        db.add_bookmark("u1", "d1")
        db.clear()
        assert db.total_bookmarks == 0

    def test_clear_folders(self):
        db = DocBookmark()
        db.create_folder("u1", "F")
        db.clear()
        assert db.total_folders == 0


class TestEdgeCases:
    def test_long_lists(self):
        db = DocBookmark()
        for i in range(50):
            db.add_bookmark("u1", f"d{i}")
        assert db.total_bookmarks_for_user("u1") == 50

    def test_concurrent_safety_simple(self):
        import threading

        db = DocBookmark()

        def worker():
            for i in range(20):
                db.add_bookmark("u1", f"d{i}")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert db.total_bookmarks == 80

    def test_unicode_note_and_tags(self):
        db = DocBookmark()
        bm = db.add_bookmark(
            "пользователь", "документ", tags=["тег"], note="заметка"
        )
        assert bm.note == "заметка"
        assert bm.tags == ["тег"]

    def test_empty_string_user_or_doc(self):
        db = DocBookmark()
        bm = db.add_bookmark("", "")
        assert bm.user_id == ""
        assert bm.doc_id == ""

    def test_move_then_reorder_independent(self):
        db = DocBookmark()
        bm = db.add_bookmark("u1", "d1")
        db.move_to_folder(bm.bookmark_id, "f1")
        db.reorder(bm.bookmark_id, 99)
        assert db.get_bookmark(bm.bookmark_id).order == 99
