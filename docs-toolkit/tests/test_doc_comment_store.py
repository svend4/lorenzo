"""Tests for docstoolkit.doc_comment_store (E308)."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_comment_store import (
    Comment,
    CommentStats,
    CommentThread,
    DocCommentStore,
)


# ---------------------------------------------------------------------------
# TestCommentDataclass
# ---------------------------------------------------------------------------
class TestCommentDataclass:
    def test_required_fields(self):
        c = Comment(
            comment_id="abc",
            doc_id="d1",
            author="alice",
            body="Hello",
        )
        assert c.comment_id == "abc"
        assert c.doc_id == "d1"
        assert c.author == "alice"
        assert c.body == "Hello"

    def test_default_created_at(self):
        c = Comment(comment_id="x", doc_id="d", author="a", body="b")
        assert c.created_at == 0.0

    def test_default_parent_id_is_none(self):
        c = Comment(comment_id="x", doc_id="d", author="a", body="b")
        assert c.parent_id is None

    def test_default_edited_at_is_none(self):
        c = Comment(comment_id="x", doc_id="d", author="a", body="b")
        assert c.edited_at is None

    def test_default_deleted_is_false(self):
        c = Comment(comment_id="x", doc_id="d", author="a", body="b")
        assert c.deleted is False

    def test_explicit_parent_id(self):
        c = Comment(comment_id="r", doc_id="d", author="a", body="b", parent_id="p1")
        assert c.parent_id == "p1"

    def test_mutable_body(self):
        c = Comment(comment_id="x", doc_id="d", author="a", body="old")
        c.body = "new"
        assert c.body == "new"


# ---------------------------------------------------------------------------
# TestCommentThreadDataclass
# ---------------------------------------------------------------------------
class TestCommentThreadDataclass:
    def test_root_field(self):
        root = Comment(comment_id="r", doc_id="d", author="a", body="root body")
        thread = CommentThread(root=root)
        assert thread.root is root

    def test_replies_defaults_to_empty_list(self):
        root = Comment(comment_id="r", doc_id="d", author="a", body="root")
        thread = CommentThread(root=root)
        assert thread.replies == []

    def test_replies_can_be_set(self):
        root = Comment(comment_id="r", doc_id="d", author="a", body="root")
        reply = Comment(comment_id="rp", doc_id="d", author="b", body="reply", parent_id="r")
        thread = CommentThread(root=root, replies=[reply])
        assert len(thread.replies) == 1
        assert thread.replies[0] is reply

    def test_independent_default_lists(self):
        root1 = Comment(comment_id="r1", doc_id="d", author="a", body="root1")
        root2 = Comment(comment_id="r2", doc_id="d", author="b", body="root2")
        t1 = CommentThread(root=root1)
        t2 = CommentThread(root=root2)
        t1.replies.append(Comment(comment_id="x", doc_id="d", author="c", body="x"))
        assert t2.replies == []


# ---------------------------------------------------------------------------
# TestCommentStatsDataclass
# ---------------------------------------------------------------------------
class TestCommentStatsDataclass:
    def test_all_fields(self):
        s = CommentStats(
            total_comments=10,
            total_threads=5,
            unique_authors=3,
            docs_with_comments=2,
        )
        assert s.total_comments == 10
        assert s.total_threads == 5
        assert s.unique_authors == 3
        assert s.docs_with_comments == 2

    def test_zero_stats(self):
        s = CommentStats(
            total_comments=0,
            total_threads=0,
            unique_authors=0,
            docs_with_comments=0,
        )
        assert s.total_comments == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_store_no_errors(self):
        store = DocCommentStore()
        assert store is not None

    def test_initial_all_doc_ids_empty(self):
        store = DocCommentStore()
        assert store.all_doc_ids() == []

    def test_initial_stats_zeroed(self):
        store = DocCommentStore()
        s = store.stats()
        assert s.total_comments == 0
        assert s.total_threads == 0
        assert s.unique_authors == 0
        assert s.docs_with_comments == 0


# ---------------------------------------------------------------------------
# TestAddComment
# ---------------------------------------------------------------------------
class TestAddComment:
    def test_returns_comment_instance(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "Hello")
        assert isinstance(c, Comment)

    def test_uuid_generated(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "Hello")
        assert c.comment_id != ""
        assert len(c.comment_id) == 36  # standard UUID4 string length

    def test_unique_uuids(self):
        store = DocCommentStore()
        ids = {store.add_comment("d1", "alice", "msg").comment_id for _ in range(20)}
        assert len(ids) == 20

    def test_top_level_has_no_parent(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "Hello")
        assert c.parent_id is None

    def test_reply_sets_parent_id(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root")
        reply = store.add_comment("d1", "bob", "Reply", parent_id=root.comment_id)
        assert reply.parent_id == root.comment_id

    def test_timestamp_defaults_to_zero(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "Hi")
        assert c.created_at == 0.0

    def test_explicit_timestamp(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "Hi", now=42.5)
        assert c.created_at == 42.5

    def test_fields_stored_correctly(self):
        store = DocCommentStore()
        c = store.add_comment("doc_x", "carol", "body text", now=99.0)
        assert c.doc_id == "doc_x"
        assert c.author == "carol"
        assert c.body == "body text"

    def test_multiple_comments_stored(self):
        store = DocCommentStore()
        store.add_comment("d1", "alice", "First")
        store.add_comment("d1", "bob", "Second")
        assert store.comment_count("d1") == 2

    def test_not_deleted_by_default(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "Hello")
        assert c.deleted is False

    def test_edited_at_none_by_default(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "Hello")
        assert c.edited_at is None


# ---------------------------------------------------------------------------
# TestEditComment
# ---------------------------------------------------------------------------
class TestEditComment:
    def test_body_updated(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "original")
        store.edit_comment(c.comment_id, "updated")
        fetched = store.get_comment(c.comment_id)
        assert fetched.body == "updated"

    def test_edited_at_set(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "original")
        store.edit_comment(c.comment_id, "updated", now=77.7)
        fetched = store.get_comment(c.comment_id)
        assert fetched.edited_at == 77.7

    def test_returns_true_on_success(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "body")
        result = store.edit_comment(c.comment_id, "new body")
        assert result is True

    def test_returns_false_for_missing_id(self):
        store = DocCommentStore()
        result = store.edit_comment("nonexistent-id", "new body")
        assert result is False

    def test_returns_false_for_deleted_comment(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "body")
        store.delete_comment(c.comment_id)
        result = store.edit_comment(c.comment_id, "new body")
        assert result is False

    def test_edit_does_not_affect_other_fields(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "body", now=5.0)
        store.edit_comment(c.comment_id, "new body", now=10.0)
        fetched = store.get_comment(c.comment_id)
        assert fetched.author == "alice"
        assert fetched.doc_id == "d1"
        assert fetched.created_at == 5.0

    def test_edit_at_defaults_to_zero_when_no_now(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "body")
        store.edit_comment(c.comment_id, "new body")
        fetched = store.get_comment(c.comment_id)
        assert fetched.edited_at == 0.0


# ---------------------------------------------------------------------------
# TestDeleteComment
# ---------------------------------------------------------------------------
class TestDeleteComment:
    def test_marks_deleted(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "body")
        store.delete_comment(c.comment_id)
        fetched = store.get_comment(c.comment_id)
        assert fetched.deleted is True

    def test_returns_true_for_existing(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "body")
        result = store.delete_comment(c.comment_id)
        assert result is True

    def test_returns_false_for_missing(self):
        store = DocCommentStore()
        result = store.delete_comment("nonexistent-uuid")
        assert result is False

    def test_double_delete_returns_true_both_times(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "body")
        store.delete_comment(c.comment_id)
        # Second delete still finds the comment (soft-delete), returns True
        result = store.delete_comment(c.comment_id)
        assert result is True

    def test_deleted_excluded_from_count(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "body")
        store.delete_comment(c.comment_id)
        assert store.comment_count("d1") == 0


# ---------------------------------------------------------------------------
# TestGetComment
# ---------------------------------------------------------------------------
class TestGetComment:
    def test_returns_comment_by_id(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "Hello")
        fetched = store.get_comment(c.comment_id)
        assert fetched is c

    def test_returns_none_for_missing_id(self):
        store = DocCommentStore()
        assert store.get_comment("no-such-id") is None

    def test_returns_deleted_comment_still(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "body")
        store.delete_comment(c.comment_id)
        fetched = store.get_comment(c.comment_id)
        # get_comment returns the object regardless of deleted flag
        assert fetched is not None
        assert fetched.deleted is True


# ---------------------------------------------------------------------------
# TestCommentsForDoc
# ---------------------------------------------------------------------------
class TestCommentsForDoc:
    def test_empty_for_unknown_doc(self):
        store = DocCommentStore()
        assert store.comments_for_doc("nope") == []

    def test_insertion_order_preserved(self):
        store = DocCommentStore()
        c1 = store.add_comment("d1", "alice", "first")
        c2 = store.add_comment("d1", "bob", "second")
        c3 = store.add_comment("d1", "carol", "third")
        result = store.comments_for_doc("d1")
        assert [c.comment_id for c in result] == [c1.comment_id, c2.comment_id, c3.comment_id]

    def test_excludes_deleted_by_default(self):
        store = DocCommentStore()
        c1 = store.add_comment("d1", "alice", "keep")
        c2 = store.add_comment("d1", "bob", "delete me")
        store.delete_comment(c2.comment_id)
        result = store.comments_for_doc("d1")
        assert len(result) == 1
        assert result[0].comment_id == c1.comment_id

    def test_include_deleted_flag(self):
        store = DocCommentStore()
        c1 = store.add_comment("d1", "alice", "keep")
        c2 = store.add_comment("d1", "bob", "delete me")
        store.delete_comment(c2.comment_id)
        result = store.comments_for_doc("d1", include_deleted=True)
        assert len(result) == 2

    def test_only_returns_comments_for_given_doc(self):
        store = DocCommentStore()
        store.add_comment("d1", "alice", "for d1")
        store.add_comment("d2", "bob", "for d2")
        result = store.comments_for_doc("d1")
        assert all(c.doc_id == "d1" for c in result)
        assert len(result) == 1


# ---------------------------------------------------------------------------
# TestThreadsForDoc
# ---------------------------------------------------------------------------
class TestThreadsForDoc:
    def test_empty_for_unknown_doc(self):
        store = DocCommentStore()
        assert store.threads_for_doc("nope") == []

    def test_single_top_level_no_replies(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root comment", now=1.0)
        threads = store.threads_for_doc("d1")
        assert len(threads) == 1
        assert threads[0].root.comment_id == root.comment_id
        assert threads[0].replies == []

    def test_replies_attached_to_correct_thread(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root", now=1.0)
        reply = store.add_comment("d1", "bob", "Reply", parent_id=root.comment_id, now=2.0)
        threads = store.threads_for_doc("d1")
        assert len(threads[0].replies) == 1
        assert threads[0].replies[0].comment_id == reply.comment_id

    def test_replies_sorted_by_created_at(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root", now=1.0)
        r3 = store.add_comment("d1", "carol", "late reply", parent_id=root.comment_id, now=5.0)
        r1 = store.add_comment("d1", "alice", "early reply", parent_id=root.comment_id, now=2.0)
        r2 = store.add_comment("d1", "bob", "mid reply", parent_id=root.comment_id, now=3.0)
        threads = store.threads_for_doc("d1")
        reply_times = [r.created_at for r in threads[0].replies]
        assert reply_times == [2.0, 3.0, 5.0]

    def test_threads_ordered_by_root_created_at(self):
        store = DocCommentStore()
        r2 = store.add_comment("d1", "bob", "Second root", now=2.0)
        r1 = store.add_comment("d1", "alice", "First root", now=1.0)
        r3 = store.add_comment("d1", "carol", "Third root", now=3.0)
        threads = store.threads_for_doc("d1")
        assert len(threads) == 3
        root_times = [t.root.created_at for t in threads]
        assert root_times == [1.0, 2.0, 3.0]

    def test_deleted_root_excluded(self):
        store = DocCommentStore()
        r1 = store.add_comment("d1", "alice", "Keep", now=1.0)
        r2 = store.add_comment("d1", "bob", "Delete", now=2.0)
        store.delete_comment(r2.comment_id)
        threads = store.threads_for_doc("d1")
        assert len(threads) == 1
        assert threads[0].root.comment_id == r1.comment_id

    def test_deleted_reply_excluded(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root", now=1.0)
        r1 = store.add_comment("d1", "bob", "Keep reply", parent_id=root.comment_id, now=2.0)
        r2 = store.add_comment("d1", "carol", "Delete reply", parent_id=root.comment_id, now=3.0)
        store.delete_comment(r2.comment_id)
        threads = store.threads_for_doc("d1")
        assert len(threads[0].replies) == 1
        assert threads[0].replies[0].comment_id == r1.comment_id

    def test_replies_not_included_in_other_threads(self):
        store = DocCommentStore()
        r1 = store.add_comment("d1", "alice", "Root 1", now=1.0)
        r2 = store.add_comment("d1", "bob", "Root 2", now=2.0)
        store.add_comment("d1", "carol", "Reply to r1", parent_id=r1.comment_id, now=3.0)
        threads = store.threads_for_doc("d1")
        assert len(threads[0].replies) == 1
        assert len(threads[1].replies) == 0


# ---------------------------------------------------------------------------
# TestRepliesTo
# ---------------------------------------------------------------------------
class TestRepliesTo:
    def test_no_replies_returns_empty(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "Root")
        assert store.replies_to(c.comment_id) == []

    def test_returns_direct_replies(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root", now=1.0)
        r1 = store.add_comment("d1", "bob", "Reply 1", parent_id=root.comment_id, now=2.0)
        r2 = store.add_comment("d1", "carol", "Reply 2", parent_id=root.comment_id, now=3.0)
        replies = store.replies_to(root.comment_id)
        assert {r.comment_id for r in replies} == {r1.comment_id, r2.comment_id}

    def test_replies_sorted_by_created_at(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root", now=1.0)
        store.add_comment("d1", "carol", "Third", parent_id=root.comment_id, now=5.0)
        store.add_comment("d1", "alice", "First", parent_id=root.comment_id, now=2.0)
        store.add_comment("d1", "bob", "Second", parent_id=root.comment_id, now=3.0)
        replies = store.replies_to(root.comment_id)
        times = [r.created_at for r in replies]
        assert times == sorted(times)

    def test_deleted_replies_excluded(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root", now=1.0)
        r1 = store.add_comment("d1", "bob", "Keep", parent_id=root.comment_id, now=2.0)
        r2 = store.add_comment("d1", "carol", "Delete", parent_id=root.comment_id, now=3.0)
        store.delete_comment(r2.comment_id)
        replies = store.replies_to(root.comment_id)
        assert len(replies) == 1
        assert replies[0].comment_id == r1.comment_id

    def test_only_direct_replies(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root", now=1.0)
        r1 = store.add_comment("d1", "bob", "Direct", parent_id=root.comment_id, now=2.0)
        # Reply to the reply (grandchild) — should NOT appear in replies_to(root)
        store.add_comment("d1", "carol", "Grandchild", parent_id=r1.comment_id, now=3.0)
        replies = store.replies_to(root.comment_id)
        assert len(replies) == 1
        assert replies[0].comment_id == r1.comment_id

    def test_returns_empty_for_unknown_id(self):
        store = DocCommentStore()
        assert store.replies_to("no-such-id") == []


# ---------------------------------------------------------------------------
# TestCommentCount
# ---------------------------------------------------------------------------
class TestCommentCount:
    def test_zero_for_unknown_doc(self):
        store = DocCommentStore()
        assert store.comment_count("nope") == 0

    def test_counts_all_live_comments(self):
        store = DocCommentStore()
        store.add_comment("d1", "alice", "one")
        store.add_comment("d1", "bob", "two")
        store.add_comment("d1", "carol", "three")
        assert store.comment_count("d1") == 3

    def test_excludes_deleted(self):
        store = DocCommentStore()
        c1 = store.add_comment("d1", "alice", "keep")
        c2 = store.add_comment("d1", "bob", "delete")
        store.delete_comment(c2.comment_id)
        assert store.comment_count("d1") == 1

    def test_includes_replies_in_count(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "Root")
        store.add_comment("d1", "bob", "Reply", parent_id=root.comment_id)
        assert store.comment_count("d1") == 2

    def test_isolated_per_doc(self):
        store = DocCommentStore()
        store.add_comment("d1", "alice", "for d1")
        store.add_comment("d2", "bob", "for d2")
        store.add_comment("d2", "carol", "also d2")
        assert store.comment_count("d1") == 1
        assert store.comment_count("d2") == 2


# ---------------------------------------------------------------------------
# TestAllDocIds
# ---------------------------------------------------------------------------
class TestAllDocIds:
    def test_empty_initially(self):
        store = DocCommentStore()
        assert store.all_doc_ids() == []

    def test_returns_docs_with_live_comments(self):
        store = DocCommentStore()
        store.add_comment("z_doc", "alice", "msg")
        store.add_comment("a_doc", "bob", "msg")
        result = store.all_doc_ids()
        assert "a_doc" in result
        assert "z_doc" in result

    def test_sorted_alphabetically(self):
        store = DocCommentStore()
        store.add_comment("z", "a", "msg")
        store.add_comment("a", "b", "msg")
        store.add_comment("m", "c", "msg")
        result = store.all_doc_ids()
        assert result == sorted(result)

    def test_excludes_docs_with_only_deleted(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "only comment")
        store.delete_comment(c.comment_id)
        store.add_comment("d2", "bob", "live comment")
        result = store.all_doc_ids()
        assert "d1" not in result
        assert "d2" in result

    def test_deduplicates_doc_ids(self):
        store = DocCommentStore()
        store.add_comment("d1", "alice", "first")
        store.add_comment("d1", "bob", "second")
        result = store.all_doc_ids()
        assert result.count("d1") == 1

    def test_doc_appears_after_adding_comment(self):
        store = DocCommentStore()
        assert "d1" not in store.all_doc_ids()
        store.add_comment("d1", "alice", "hello")
        assert "d1" in store.all_doc_ids()


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty_store(self):
        store = DocCommentStore()
        s = store.stats()
        assert s.total_comments == 0
        assert s.total_threads == 0
        assert s.unique_authors == 0
        assert s.docs_with_comments == 0

    def test_total_comments_counts_all_live(self):
        store = DocCommentStore()
        root = store.add_comment("d1", "alice", "root")
        store.add_comment("d1", "bob", "reply", parent_id=root.comment_id)
        store.add_comment("d2", "carol", "other doc")
        s = store.stats()
        assert s.total_comments == 3

    def test_total_threads_counts_only_top_level(self):
        store = DocCommentStore()
        r1 = store.add_comment("d1", "alice", "root1")
        r2 = store.add_comment("d1", "bob", "root2")
        store.add_comment("d1", "carol", "reply", parent_id=r1.comment_id)
        s = store.stats()
        assert s.total_threads == 2

    def test_unique_authors_counted(self):
        store = DocCommentStore()
        store.add_comment("d1", "alice", "msg")
        store.add_comment("d1", "alice", "again")
        store.add_comment("d1", "bob", "msg")
        s = store.stats()
        assert s.unique_authors == 2

    def test_docs_with_comments_counted(self):
        store = DocCommentStore()
        store.add_comment("d1", "alice", "msg")
        store.add_comment("d2", "bob", "msg")
        store.add_comment("d1", "carol", "also d1")
        s = store.stats()
        assert s.docs_with_comments == 2

    def test_deleted_excluded_from_stats(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "will be deleted")
        store.add_comment("d1", "bob", "stays")
        store.delete_comment(c.comment_id)
        s = store.stats()
        assert s.total_comments == 1
        assert s.total_threads == 1

    def test_deleted_thread_excluded(self):
        store = DocCommentStore()
        r = store.add_comment("d1", "alice", "thread root")
        store.delete_comment(r.comment_id)
        s = store.stats()
        assert s.total_threads == 0

    def test_docs_with_only_deleted_not_counted(self):
        store = DocCommentStore()
        c = store.add_comment("d1", "alice", "only comment")
        store.delete_comment(c.comment_id)
        store.add_comment("d2", "bob", "live")
        s = store.stats()
        assert s.docs_with_comments == 1


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_add_comment(self):
        store = DocCommentStore()
        errors: list[Exception] = []

        def worker(author: str) -> None:
            try:
                for i in range(50):
                    store.add_comment(f"d{i % 5}", author, f"msg {i}")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(f"author_{t}",)) for t in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        # 6 authors × 50 comments each = 300 total live comments
        s = store.stats()
        assert s.total_comments == 300

    def test_concurrent_add_and_delete(self):
        store = DocCommentStore()
        added_ids: list[str] = []
        ids_lock = threading.Lock()

        def adder() -> None:
            for i in range(40):
                c = store.add_comment("d1", f"user_{i}", f"msg {i}")
                with ids_lock:
                    added_ids.append(c.comment_id)

        def deleter() -> None:
            for _ in range(40):
                with ids_lock:
                    cid = added_ids.pop(0) if added_ids else None
                if cid is not None:
                    store.delete_comment(cid)

        t1 = threading.Thread(target=adder)
        t2 = threading.Thread(target=deleter)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # No exception; total non-negative
        assert store.comment_count("d1") >= 0

    def test_concurrent_reads_consistent(self):
        store = DocCommentStore()
        for i in range(20):
            store.add_comment("d1", f"author_{i}", f"msg {i}", now=float(i))

        read_counts: list[int] = []

        def reader() -> None:
            count = store.comment_count("d1")
            read_counts.append(count)

        threads = [threading.Thread(target=reader) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(c == 20 for c in read_counts)

    def test_concurrent_stats(self):
        store = DocCommentStore()
        errors: list[Exception] = []

        def adder_and_reader() -> None:
            try:
                store.add_comment("d1", "user", "msg")
                _ = store.stats()
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=adder_and_reader) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
