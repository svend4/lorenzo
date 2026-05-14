"""Tests for docstoolkit.doc_thread (E218)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_thread import (
    DocThread,
    MessageReaction,
    MessageStatus,
    Thread,
    ThreadMessage,
)


# ---------------------------------------------------------------- fixtures
@pytest.fixture
def dt() -> DocThread:
    return DocThread()


@pytest.fixture
def thread(dt: DocThread) -> Thread:
    return dt.create_thread(doc_id="doc-1", created_by="alice", now=1.0)


@pytest.fixture
def thread_with_msg(dt: DocThread):
    t = dt.create_thread(
        doc_id="doc-1", created_by="alice", initial_message="hi", now=1.0
    )
    return t, t.messages[0]


# =========================================================== enums & dataclasses
class TestMessageReaction:
    def test_values(self):
        assert MessageReaction.LIKE.value == "like"
        assert MessageReaction.DISLIKE.value == "dislike"
        assert MessageReaction.HEART.value == "heart"
        assert MessageReaction.LAUGH.value == "laugh"
        assert MessageReaction.CONFUSED.value == "confused"
        assert MessageReaction.INSIGHTFUL.value == "insightful"

    def test_count(self):
        assert len(MessageReaction) == 6


class TestMessageStatus:
    def test_values(self):
        assert MessageStatus.ACTIVE.value == "active"
        assert MessageStatus.EDITED.value == "edited"
        assert MessageStatus.DELETED.value == "deleted"
        assert MessageStatus.RESOLVED.value == "resolved"
        assert MessageStatus.FLAGGED.value == "flagged"

    def test_count(self):
        assert len(MessageStatus) == 5


class TestThreadMessage:
    def test_defaults(self):
        m = ThreadMessage(message_id="m1", thread_id="t1", author="a", content="c")
        assert m.created_at == 0.0
        assert m.edited_at is None
        assert m.parent_id is None
        assert m.status == MessageStatus.ACTIVE
        assert m.reactions == {}

    def test_custom_fields(self):
        m = ThreadMessage(
            message_id="m1",
            thread_id="t1",
            author="a",
            content="c",
            created_at=5.0,
            parent_id="m0",
        )
        assert m.created_at == 5.0
        assert m.parent_id == "m0"


class TestThread:
    def test_defaults(self):
        t = Thread(thread_id="t1", doc_id="d1", created_by="a", created_at=1.0)
        assert t.messages == []
        assert t.participants == set()
        assert t.archived is False


# =================================================================== create
class TestCreateThread:
    def test_returns_thread(self, dt: DocThread):
        t = dt.create_thread(doc_id="d1", created_by="alice", now=1.0)
        assert isinstance(t, Thread)
        assert t.doc_id == "d1"
        assert t.created_by == "alice"
        assert t.created_at == 1.0

    def test_unique_ids(self, dt: DocThread):
        a = dt.create_thread("d1", "alice")
        b = dt.create_thread("d1", "alice")
        assert a.thread_id != b.thread_id

    def test_initial_message(self, dt: DocThread):
        t = dt.create_thread("d1", "alice", initial_message="hello", now=2.0)
        assert len(t.messages) == 1
        m = t.messages[0]
        assert m.content == "hello"
        assert m.author == "alice"
        assert m.created_at == 2.0

    def test_no_initial_message(self, dt: DocThread):
        t = dt.create_thread("d1", "alice")
        assert t.messages == []

    def test_creator_in_participants(self, dt: DocThread):
        t = dt.create_thread("d1", "alice")
        assert "alice" in t.participants

    def test_initial_message_indexed(self, dt: DocThread):
        t = dt.create_thread("d1", "alice", initial_message="hi")
        m = t.messages[0]
        assert dt.get_message(m.message_id) is m

    def test_count_increments(self, dt: DocThread):
        assert dt.thread_count == 0
        dt.create_thread("d1", "alice")
        assert dt.thread_count == 1


# ========================================================== archive / unarchive
class TestArchiveUnarchive:
    def test_archive(self, dt: DocThread, thread: Thread):
        assert dt.archive_thread(thread.thread_id) is True
        assert thread.archived is True

    def test_archive_unknown(self, dt: DocThread):
        assert dt.archive_thread("bogus") is False

    def test_archive_already_archived(self, dt: DocThread, thread: Thread):
        dt.archive_thread(thread.thread_id)
        assert dt.archive_thread(thread.thread_id) is False

    def test_unarchive(self, dt: DocThread, thread: Thread):
        dt.archive_thread(thread.thread_id)
        assert dt.unarchive_thread(thread.thread_id) is True
        assert thread.archived is False

    def test_unarchive_not_archived(self, dt: DocThread, thread: Thread):
        assert dt.unarchive_thread(thread.thread_id) is False

    def test_unarchive_unknown(self, dt: DocThread):
        assert dt.unarchive_thread("bogus") is False

    def test_archived_thread_rejects_messages(self, dt: DocThread, thread: Thread):
        dt.archive_thread(thread.thread_id)
        assert dt.add_message(thread.thread_id, "bob", "hi") is None


# ================================================================ delete thread
class TestDeleteThread:
    def test_delete(self, dt: DocThread, thread: Thread):
        assert dt.delete_thread(thread.thread_id) is True
        assert dt.get_thread(thread.thread_id) is None

    def test_delete_unknown(self, dt: DocThread):
        assert dt.delete_thread("bogus") is False

    def test_delete_purges_messages(self, dt: DocThread):
        t = dt.create_thread("d1", "alice", initial_message="x")
        mid = t.messages[0].message_id
        dt.delete_thread(t.thread_id)
        assert dt.get_message(mid) is None

    def test_count_decrements(self, dt: DocThread, thread: Thread):
        assert dt.thread_count == 1
        dt.delete_thread(thread.thread_id)
        assert dt.thread_count == 0


# =================================================================== add msg
class TestAddMessage:
    def test_add(self, dt: DocThread, thread: Thread):
        m = dt.add_message(thread.thread_id, "bob", "hello", now=2.0)
        assert m is not None
        assert m.author == "bob"
        assert m.content == "hello"
        assert m.created_at == 2.0
        assert m.thread_id == thread.thread_id

    def test_unknown_thread(self, dt: DocThread):
        assert dt.add_message("bogus", "bob", "hi") is None

    def test_updates_participants(self, dt: DocThread, thread: Thread):
        dt.add_message(thread.thread_id, "bob", "hi")
        assert "bob" in thread.participants
        assert "alice" in thread.participants

    def test_appended_to_messages(self, dt: DocThread, thread: Thread):
        m = dt.add_message(thread.thread_id, "bob", "hi")
        assert thread.messages[-1] is m

    def test_reply(self, dt: DocThread, thread: Thread):
        a = dt.add_message(thread.thread_id, "bob", "hi")
        b = dt.add_message(thread.thread_id, "carol", "re", parent_id=a.message_id)
        assert b.parent_id == a.message_id

    def test_reply_to_unknown_parent(self, dt: DocThread, thread: Thread):
        m = dt.add_message(thread.thread_id, "bob", "hi", parent_id="bogus")
        assert m is None

    def test_reply_to_parent_in_other_thread(self, dt: DocThread):
        t1 = dt.create_thread("d1", "a", initial_message="x")
        t2 = dt.create_thread("d1", "b")
        other = t1.messages[0]
        m = dt.add_message(t2.thread_id, "bob", "hi", parent_id=other.message_id)
        assert m is None

    def test_message_indexed(self, dt: DocThread, thread: Thread):
        m = dt.add_message(thread.thread_id, "bob", "hi")
        assert dt.get_message(m.message_id) is m


# ================================================================== edit msg
class TestEditMessage:
    def test_edit(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.edit_message(m.message_id, "new", now=5.0) is True
        assert m.content == "new"
        assert m.edited_at == 5.0
        assert m.status == MessageStatus.EDITED

    def test_edit_unknown(self, dt: DocThread):
        assert dt.edit_message("bogus", "new") is False

    def test_edit_deleted_fails(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.delete_message(m.message_id)
        assert dt.edit_message(m.message_id, "new") is False

    def test_edit_preserves_flagged_status(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.flag_message(m.message_id)
        dt.edit_message(m.message_id, "new")
        # Edit on non-ACTIVE leaves the status as-is (flagged).
        assert m.status == MessageStatus.FLAGGED


# ================================================================ delete msg
class TestDeleteMessage:
    def test_delete(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.delete_message(m.message_id, now=7.0) is True
        assert m.status == MessageStatus.DELETED
        assert m.edited_at == 7.0

    def test_delete_unknown(self, dt: DocThread):
        assert dt.delete_message("bogus") is False

    def test_delete_twice(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.delete_message(m.message_id)
        assert dt.delete_message(m.message_id) is False

    def test_soft_delete_remains_in_thread(self, dt: DocThread, thread_with_msg):
        t, m = thread_with_msg
        dt.delete_message(m.message_id)
        assert m in t.messages


# ================================================================== flag/resolve
class TestFlagMessage:
    def test_flag(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.flag_message(m.message_id) is True
        assert m.status == MessageStatus.FLAGGED

    def test_flag_unknown(self, dt: DocThread):
        assert dt.flag_message("bogus") is False

    def test_flag_deleted_fails(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.delete_message(m.message_id)
        assert dt.flag_message(m.message_id) is False


class TestResolveMessage:
    def test_resolve(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.resolve_message(m.message_id) is True
        assert m.status == MessageStatus.RESOLVED

    def test_resolve_unknown(self, dt: DocThread):
        assert dt.resolve_message("bogus") is False

    def test_resolve_deleted_fails(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.delete_message(m.message_id)
        assert dt.resolve_message(m.message_id) is False


# ================================================================== reactions
class TestAddReaction:
    def test_add(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE) is True
        assert "bob" in m.reactions["like"]

    def test_add_unknown_message(self, dt: DocThread):
        assert dt.add_reaction("bogus", "bob", MessageReaction.LIKE) is False

    def test_duplicate(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE)
        assert dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE) is False

    def test_multiple_users(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "carol", MessageReaction.LIKE)
        assert m.reactions["like"] == {"bob", "carol"}

    def test_multiple_reactions_same_user(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "bob", MessageReaction.HEART)
        assert "bob" in m.reactions["like"]
        assert "bob" in m.reactions["heart"]

    def test_invalid_reaction(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.add_reaction(m.message_id, "bob", "not-an-enum") is False

    def test_on_deleted_message_fails(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.delete_message(m.message_id)
        assert dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE) is False


class TestRemoveReaction:
    def test_remove(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE)
        assert dt.remove_reaction(m.message_id, "bob", MessageReaction.LIKE) is True
        assert "like" not in m.reactions

    def test_remove_unknown_message(self, dt: DocThread):
        assert dt.remove_reaction("bogus", "bob", MessageReaction.LIKE) is False

    def test_remove_not_present(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.remove_reaction(m.message_id, "bob", MessageReaction.LIKE) is False

    def test_remove_only_user(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "carol", MessageReaction.LIKE)
        dt.remove_reaction(m.message_id, "bob", MessageReaction.LIKE)
        assert m.reactions["like"] == {"carol"}

    def test_invalid_reaction(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.remove_reaction(m.message_id, "bob", "x") is False


# ==================================================================== getters
class TestGetThread:
    def test_get(self, dt: DocThread, thread: Thread):
        assert dt.get_thread(thread.thread_id) is thread

    def test_get_unknown(self, dt: DocThread):
        assert dt.get_thread("bogus") is None


class TestGetMessage:
    def test_get(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.get_message(m.message_id) is m

    def test_get_unknown(self, dt: DocThread):
        assert dt.get_message("bogus") is None


# ============================================================== threads_for_doc
class TestThreadsForDoc:
    def test_empty(self, dt: DocThread):
        assert dt.threads_for_doc("d1") == []

    def test_only_for_doc(self, dt: DocThread):
        a = dt.create_thread("d1", "alice", now=1.0)
        dt.create_thread("d2", "bob", now=2.0)
        out = dt.threads_for_doc("d1")
        assert out == [a]

    def test_excludes_archived_by_default(self, dt: DocThread):
        a = dt.create_thread("d1", "alice", now=1.0)
        b = dt.create_thread("d1", "alice", now=2.0)
        dt.archive_thread(a.thread_id)
        out = dt.threads_for_doc("d1")
        assert out == [b]

    def test_include_archived(self, dt: DocThread):
        a = dt.create_thread("d1", "alice", now=1.0)
        b = dt.create_thread("d1", "alice", now=2.0)
        dt.archive_thread(a.thread_id)
        out = dt.threads_for_doc("d1", include_archived=True)
        assert {t.thread_id for t in out} == {a.thread_id, b.thread_id}

    def test_sorted_by_created_at(self, dt: DocThread):
        b = dt.create_thread("d1", "alice", now=5.0)
        a = dt.create_thread("d1", "alice", now=1.0)
        out = dt.threads_for_doc("d1")
        assert out == [a, b]


# ============================================================ messages_for_thread
class TestMessagesForThread:
    def test_empty_thread(self, dt: DocThread, thread: Thread):
        assert dt.messages_for_thread(thread.thread_id) == []

    def test_unknown_thread(self, dt: DocThread):
        assert dt.messages_for_thread("bogus") == []

    def test_excludes_deleted(self, dt: DocThread, thread: Thread):
        a = dt.add_message(thread.thread_id, "bob", "hi")
        b = dt.add_message(thread.thread_id, "bob", "bye")
        dt.delete_message(a.message_id)
        assert dt.messages_for_thread(thread.thread_id) == [b]

    def test_include_deleted(self, dt: DocThread, thread: Thread):
        a = dt.add_message(thread.thread_id, "bob", "hi")
        b = dt.add_message(thread.thread_id, "bob", "bye")
        dt.delete_message(a.message_id)
        out = dt.messages_for_thread(thread.thread_id, include_deleted=True)
        assert out == [a, b]


# =================================================================== replies_to
class TestRepliesTo:
    def test_no_replies(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.replies_to(m.message_id) == []

    def test_with_replies(self, dt: DocThread, thread_with_msg):
        t, m = thread_with_msg
        r1 = dt.add_message(t.thread_id, "bob", "r1", parent_id=m.message_id)
        r2 = dt.add_message(t.thread_id, "carol", "r2", parent_id=m.message_id)
        # unrelated message
        dt.add_message(t.thread_id, "dan", "top-level")
        assert dt.replies_to(m.message_id) == [r1, r2]

    def test_unknown_message(self, dt: DocThread):
        assert dt.replies_to("bogus") == []


# ============================================================== participants_of
class TestParticipantsOf:
    def test_empty_for_unknown(self, dt: DocThread):
        assert dt.participants_of("bogus") == set()

    def test_creator_only(self, dt: DocThread, thread: Thread):
        assert dt.participants_of(thread.thread_id) == {"alice"}

    def test_after_adds(self, dt: DocThread, thread: Thread):
        dt.add_message(thread.thread_id, "bob", "hi")
        dt.add_message(thread.thread_id, "carol", "hi")
        assert dt.participants_of(thread.thread_id) == {"alice", "bob", "carol"}

    def test_returns_copy(self, dt: DocThread, thread: Thread):
        p = dt.participants_of(thread.thread_id)
        p.add("dan")
        assert "dan" not in thread.participants


# ============================================================== messages_by_author
class TestMessagesByAuthor:
    def test_empty(self, dt: DocThread):
        assert dt.messages_by_author("nobody") == []

    def test_finds_messages(self, dt: DocThread):
        t = dt.create_thread("d1", "alice", initial_message="hi", now=1.0)
        m2 = dt.add_message(t.thread_id, "alice", "again", now=2.0)
        dt.add_message(t.thread_id, "bob", "hey", now=3.0)
        out = dt.messages_by_author("alice")
        assert len(out) == 2
        assert t.messages[0] in out
        assert m2 in out

    def test_across_threads(self, dt: DocThread):
        t1 = dt.create_thread("d1", "alice", initial_message="a")
        t2 = dt.create_thread("d2", "alice", initial_message="b")
        out = dt.messages_by_author("alice")
        ids = {m.message_id for m in out}
        assert t1.messages[0].message_id in ids
        assert t2.messages[0].message_id in ids


# ================================================================ reaction_count
class TestReactionCount:
    def test_unknown_message(self, dt: DocThread):
        assert dt.reaction_count("bogus") == 0

    def test_no_reactions(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.reaction_count(m.message_id) == 0

    def test_total(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "carol", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "bob", MessageReaction.HEART)
        assert dt.reaction_count(m.message_id) == 3

    def test_specific(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "carol", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "bob", MessageReaction.HEART)
        assert dt.reaction_count(m.message_id, MessageReaction.LIKE) == 2
        assert dt.reaction_count(m.message_id, MessageReaction.HEART) == 1
        assert dt.reaction_count(m.message_id, MessageReaction.DISLIKE) == 0


# ================================================================== top_reactions
class TestTopReactions:
    def test_unknown_message(self, dt: DocThread):
        assert dt.top_reactions("bogus") == []

    def test_empty(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        assert dt.top_reactions(m.message_id) == []

    def test_sorted_desc(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "carol", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "dan", MessageReaction.LIKE)
        dt.add_reaction(m.message_id, "bob", MessageReaction.HEART)
        out = dt.top_reactions(m.message_id)
        assert out[0] == (MessageReaction.LIKE, 3)
        assert out[1] == (MessageReaction.HEART, 1)


# ====================================================================== counts
class TestThreadCount:
    def test_zero(self, dt: DocThread):
        assert dt.thread_count == 0

    def test_increments(self, dt: DocThread):
        dt.create_thread("d1", "alice")
        dt.create_thread("d2", "bob")
        assert dt.thread_count == 2

    def test_after_delete(self, dt: DocThread):
        t = dt.create_thread("d1", "alice")
        dt.delete_thread(t.thread_id)
        assert dt.thread_count == 0


class TestMessageCount:
    def test_zero(self, dt: DocThread):
        assert dt.message_count == 0

    def test_with_initial_message(self, dt: DocThread):
        dt.create_thread("d1", "alice", initial_message="hi")
        assert dt.message_count == 1

    def test_after_adds(self, dt: DocThread, thread: Thread):
        dt.add_message(thread.thread_id, "bob", "hi")
        dt.add_message(thread.thread_id, "carol", "hey")
        assert dt.message_count == 2

    def test_after_thread_delete(self, dt: DocThread):
        t = dt.create_thread("d1", "alice", initial_message="hi")
        dt.delete_thread(t.thread_id)
        assert dt.message_count == 0


# ====================================================================== clear
class TestClear:
    def test_clear_empty(self, dt: DocThread):
        dt.clear()
        assert dt.thread_count == 0
        assert dt.message_count == 0

    def test_clear_with_data(self, dt: DocThread):
        t = dt.create_thread("d1", "alice", initial_message="hi")
        dt.add_message(t.thread_id, "bob", "hey")
        dt.clear()
        assert dt.thread_count == 0
        assert dt.message_count == 0
        assert dt.get_thread(t.thread_id) is None


# =================================================================== edge cases
class TestEdgeCases:
    def test_empty_initial_message_not_added(self, dt: DocThread):
        # falsy initial messages (empty string) are treated as "no message"
        t = dt.create_thread("d1", "alice", initial_message="")
        assert t.messages == []

    def test_reaction_after_remove_and_readd(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE)
        dt.remove_reaction(m.message_id, "bob", MessageReaction.LIKE)
        assert dt.add_reaction(m.message_id, "bob", MessageReaction.LIKE) is True

    def test_edit_then_delete(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.edit_message(m.message_id, "new", now=2.0)
        assert dt.delete_message(m.message_id, now=3.0) is True
        assert m.status == MessageStatus.DELETED

    def test_reactions_independent_per_message(self, dt: DocThread, thread: Thread):
        a = dt.add_message(thread.thread_id, "bob", "hi")
        b = dt.add_message(thread.thread_id, "carol", "hey")
        dt.add_reaction(a.message_id, "x", MessageReaction.LIKE)
        assert dt.reaction_count(b.message_id) == 0

    def test_unarchive_then_post(self, dt: DocThread, thread: Thread):
        dt.archive_thread(thread.thread_id)
        dt.unarchive_thread(thread.thread_id)
        assert dt.add_message(thread.thread_id, "bob", "hi") is not None

    def test_threads_for_doc_only_returns_matching(self, dt: DocThread):
        dt.create_thread("d1", "a")
        dt.create_thread("d2", "b")
        dt.create_thread("d3", "c")
        assert len(dt.threads_for_doc("d2")) == 1

    def test_resolve_then_edit_keeps_resolved(self, dt: DocThread, thread_with_msg):
        _, m = thread_with_msg
        dt.resolve_message(m.message_id)
        dt.edit_message(m.message_id, "new")
        assert m.status == MessageStatus.RESOLVED
