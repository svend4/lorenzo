"""Tests for docstoolkit.priority_inbox."""
from __future__ import annotations

import pytest

from docstoolkit.priority_inbox import (
    PriorityInbox,
    Message,
    Priority,
    MessageStatus,
    InboxStats,
)


# ----------------------------------------------------------------- Priority
class TestPriority:
    def test_urgent_is_zero(self):
        assert Priority.URGENT == 0

    def test_priority_ordering(self):
        assert Priority.URGENT < Priority.HIGH < Priority.NORMAL < Priority.LOW

    def test_four_values(self):
        assert len(list(Priority)) == 4

    def test_names(self):
        names = {p.name for p in Priority}
        assert names == {"URGENT", "HIGH", "NORMAL", "LOW"}


# ----------------------------------------------------------------- MessageStatus
class TestMessageStatus:
    def test_values_present(self):
        names = {s.name for s in MessageStatus}
        assert names == {"UNREAD", "READ", "ARCHIVED", "DELETED"}

    def test_unread_value(self):
        assert MessageStatus.UNREAD.value == "unread"


# ----------------------------------------------------------------- Message
class TestMessage:
    def test_create(self):
        m = Message(
            msg_id="x",
            subject="hi",
            body="hello",
            priority=Priority.NORMAL,
        )
        assert m.msg_id == "x"
        assert m.category == "default"
        assert m.status == MessageStatus.UNREAD
        assert m.metadata == {}
        assert m.expires_at is None

    def test_is_expired_true(self):
        m = Message("x", "s", "b", Priority.NORMAL, expires_at=10.0)
        assert m.is_expired(20.0)

    def test_is_expired_false(self):
        m = Message("x", "s", "b", Priority.NORMAL, expires_at=100.0)
        assert not m.is_expired(50.0)

    def test_is_expired_none(self):
        m = Message("x", "s", "b", Priority.NORMAL)
        assert not m.is_expired(1e12)


# ----------------------------------------------------------------- InboxStats
class TestInboxStats:
    def test_construct(self):
        s = InboxStats(
            total=1,
            unread=1,
            read=0,
            archived=0,
            by_priority={Priority.URGENT: 1},
            by_category={"a": 1},
        )
        assert s.total == 1
        assert s.by_priority[Priority.URGENT] == 1


# ----------------------------------------------------------------- Add
class TestAdd:
    def test_returns_message(self):
        ib = PriorityInbox()
        m = ib.add("subj", "body")
        assert isinstance(m, Message)
        assert m.subject == "subj"
        assert m.body == "body"
        assert m.priority == Priority.NORMAL
        assert m.status == MessageStatus.UNREAD

    def test_assigns_id(self):
        ib = PriorityInbox()
        m1 = ib.add("a", "b")
        m2 = ib.add("a", "b")
        assert m1.msg_id != m2.msg_id

    def test_with_priority_and_category(self):
        ib = PriorityInbox()
        m = ib.add("s", "b", priority=Priority.URGENT, category="alerts")
        assert m.priority == Priority.URGENT
        assert m.category == "alerts"

    def test_with_metadata(self):
        ib = PriorityInbox()
        m = ib.add("s", "b", metadata={"k": "v"})
        assert m.metadata == {"k": "v"}

    def test_metadata_copied(self):
        ib = PriorityInbox()
        meta = {"k": "v"}
        m = ib.add("s", "b", metadata=meta)
        meta["k"] = "z"
        assert m.metadata == {"k": "v"}

    def test_now_sets_received_at(self):
        ib = PriorityInbox()
        m = ib.add("s", "b", now=123.0)
        assert m.received_at == 123.0

    def test_expires_at(self):
        ib = PriorityInbox()
        m = ib.add("s", "b", expires_at=999.0)
        assert m.expires_at == 999.0

    def test_stored(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        assert ib.get(m.msg_id) is m


# ----------------------------------------------------------------- AddMessage
class TestAddMessage:
    def test_basic(self):
        ib = PriorityInbox()
        m = Message("xx", "s", "b", Priority.HIGH)
        ib.add_message(m)
        assert ib.get("xx") is m

    def test_overwrites_same_id(self):
        ib = PriorityInbox()
        m1 = Message("xx", "s1", "b", Priority.HIGH)
        m2 = Message("xx", "s2", "b", Priority.LOW)
        ib.add_message(m1)
        ib.add_message(m2)
        assert ib.get("xx").subject == "s2"


# ----------------------------------------------------------------- Peek
class TestPeek:
    def test_empty(self):
        ib = PriorityInbox()
        assert ib.peek() is None

    def test_single(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        assert ib.peek().msg_id == m.msg_id

    def test_highest_priority(self):
        ib = PriorityInbox()
        ib.add("low", "x", priority=Priority.LOW, now=1.0)
        ib.add("urg", "x", priority=Priority.URGENT, now=2.0)
        ib.add("hi", "x", priority=Priority.HIGH, now=3.0)
        assert ib.peek().subject == "urg"

    def test_peek_does_not_modify(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        ib.peek()
        assert ib.get(m.msg_id).status == MessageStatus.UNREAD

    def test_peek_skips_read(self):
        ib = PriorityInbox()
        m1 = ib.add("a", "x", priority=Priority.URGENT, now=1.0)
        ib.add("b", "x", priority=Priority.HIGH, now=2.0)
        ib.mark_read(m1.msg_id)
        assert ib.peek().subject == "b"

    def test_peek_skips_expired(self):
        ib = PriorityInbox()
        ib.add("exp", "x", priority=Priority.URGENT, now=1.0, expires_at=5.0)
        ib.add("ok", "x", priority=Priority.HIGH, now=1.0)
        assert ib.peek(now=10.0).subject == "ok"


# ----------------------------------------------------------------- Pop
class TestPop:
    def test_empty(self):
        ib = PriorityInbox()
        assert ib.pop() is None

    def test_pop_marks_read(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        popped = ib.pop()
        assert popped.msg_id == m.msg_id
        assert ib.get(m.msg_id).status == MessageStatus.READ

    def test_pop_returns_highest(self):
        ib = PriorityInbox()
        ib.add("low", "x", priority=Priority.LOW, now=1.0)
        ib.add("urg", "x", priority=Priority.URGENT, now=2.0)
        assert ib.pop().subject == "urg"

    def test_pop_advances(self):
        ib = PriorityInbox()
        ib.add("a", "x", priority=Priority.URGENT, now=1.0)
        ib.add("b", "x", priority=Priority.HIGH, now=2.0)
        s1 = ib.pop().subject
        s2 = ib.pop().subject
        assert s1 == "a" and s2 == "b"


# ----------------------------------------------------------------- PriorityOrder
class TestPriorityOrder:
    def test_full_ordering(self):
        ib = PriorityInbox()
        ib.add("low", "x", priority=Priority.LOW, now=1.0)
        ib.add("norm", "x", priority=Priority.NORMAL, now=2.0)
        ib.add("hi", "x", priority=Priority.HIGH, now=3.0)
        ib.add("urg", "x", priority=Priority.URGENT, now=4.0)
        order = [ib.pop().subject for _ in range(4)]
        assert order == ["urg", "hi", "norm", "low"]

    def test_same_priority_received_order(self):
        ib = PriorityInbox()
        ib.add("first", "x", priority=Priority.HIGH, now=1.0)
        ib.add("second", "x", priority=Priority.HIGH, now=2.0)
        ib.add("third", "x", priority=Priority.HIGH, now=3.0)
        order = [ib.pop().subject for _ in range(3)]
        assert order == ["first", "second", "third"]


# ----------------------------------------------------------------- MarkRead
class TestMarkRead:
    def test_basic(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        assert ib.mark_read(m.msg_id) is True
        assert ib.get(m.msg_id).status == MessageStatus.READ

    def test_missing_id(self):
        ib = PriorityInbox()
        assert ib.mark_read("nope") is False

    def test_already_read(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        ib.mark_read(m.msg_id)
        assert ib.mark_read(m.msg_id) is True


# ----------------------------------------------------------------- MarkUnread
class TestMarkUnread:
    def test_basic(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        ib.mark_read(m.msg_id)
        assert ib.mark_unread(m.msg_id) is True
        assert ib.get(m.msg_id).status == MessageStatus.UNREAD

    def test_missing(self):
        ib = PriorityInbox()
        assert ib.mark_unread("x") is False


# ----------------------------------------------------------------- Archive
class TestArchive:
    def test_basic(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        assert ib.archive(m.msg_id) is True
        assert ib.get(m.msg_id).status == MessageStatus.ARCHIVED

    def test_missing(self):
        ib = PriorityInbox()
        assert ib.archive("x") is False

    def test_archived_not_in_unread(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        ib.archive(m.msg_id)
        assert ib.list_unread() == []

    def test_archived_not_in_peek(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        ib.archive(m.msg_id)
        assert ib.peek() is None


# ----------------------------------------------------------------- Delete
class TestDelete:
    def test_basic(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        assert ib.delete(m.msg_id) is True
        assert ib.get(m.msg_id) is None

    def test_missing(self):
        ib = PriorityInbox()
        assert ib.delete("x") is False

    def test_delete_removes_from_storage(self):
        ib = PriorityInbox()
        m = ib.add("s", "b")
        ib.delete(m.msg_id)
        assert ib.count_unread() == 0


# ----------------------------------------------------------------- ListUnread
class TestListUnread:
    def test_empty(self):
        ib = PriorityInbox()
        assert ib.list_unread() == []

    def test_sorted_by_priority(self):
        ib = PriorityInbox()
        ib.add("low", "x", priority=Priority.LOW, now=1.0)
        ib.add("urg", "x", priority=Priority.URGENT, now=2.0)
        ib.add("norm", "x", priority=Priority.NORMAL, now=3.0)
        subs = [m.subject for m in ib.list_unread()]
        assert subs == ["urg", "norm", "low"]

    def test_filter_by_category(self):
        ib = PriorityInbox()
        ib.add("a", "x", category="alerts", now=1.0)
        ib.add("b", "x", category="news", now=2.0)
        ib.add("c", "x", category="alerts", now=3.0)
        subs = [m.subject for m in ib.list_unread(category="alerts")]
        assert set(subs) == {"a", "c"}

    def test_excludes_read(self):
        ib = PriorityInbox()
        m1 = ib.add("a", "x", now=1.0)
        ib.add("b", "x", now=2.0)
        ib.mark_read(m1.msg_id)
        subs = [m.subject for m in ib.list_unread()]
        assert subs == ["b"]

    def test_excludes_expired(self):
        ib = PriorityInbox()
        ib.add("a", "x", now=1.0, expires_at=5.0)
        ib.add("b", "x", now=1.0)
        subs = [m.subject for m in ib.list_unread(now=10.0)]
        assert subs == ["b"]


# ----------------------------------------------------------------- ListByPriority
class TestListByPriority:
    def test_empty(self):
        ib = PriorityInbox()
        assert ib.list_by_priority(Priority.HIGH) == []

    def test_basic(self):
        ib = PriorityInbox()
        ib.add("a", "x", priority=Priority.HIGH, now=1.0)
        ib.add("b", "x", priority=Priority.LOW, now=2.0)
        ib.add("c", "x", priority=Priority.HIGH, now=3.0)
        subs = [m.subject for m in ib.list_by_priority(Priority.HIGH)]
        assert subs == ["a", "c"]

    def test_excludes_expired(self):
        ib = PriorityInbox()
        ib.add("a", "x", priority=Priority.HIGH, now=1.0, expires_at=5.0)
        ib.add("b", "x", priority=Priority.HIGH, now=1.0)
        subs = [m.subject for m in ib.list_by_priority(Priority.HIGH, now=10.0)]
        assert subs == ["b"]

    def test_excludes_read(self):
        ib = PriorityInbox()
        m = ib.add("a", "x", priority=Priority.HIGH, now=1.0)
        ib.mark_read(m.msg_id)
        assert ib.list_by_priority(Priority.HIGH) == []


# ----------------------------------------------------------------- ListByCategory
class TestListByCategory:
    def test_empty(self):
        ib = PriorityInbox()
        assert ib.list_by_category("x") == []

    def test_basic(self):
        ib = PriorityInbox()
        ib.add("a", "x", category="alerts", now=1.0)
        ib.add("b", "x", category="news", now=2.0)
        ib.add("c", "x", category="alerts", now=3.0)
        subs = [m.subject for m in ib.list_by_category("alerts")]
        assert set(subs) == {"a", "c"}

    def test_excludes_archived(self):
        ib = PriorityInbox()
        m = ib.add("a", "x", category="z", now=1.0)
        ib.archive(m.msg_id)
        assert ib.list_by_category("z") == []

    def test_includes_read(self):
        ib = PriorityInbox()
        m = ib.add("a", "x", category="z", now=1.0)
        ib.mark_read(m.msg_id)
        assert len(ib.list_by_category("z")) == 1


# ----------------------------------------------------------------- CountUnread
class TestCountUnread:
    def test_empty(self):
        ib = PriorityInbox()
        assert ib.count_unread() == 0

    def test_basic(self):
        ib = PriorityInbox()
        ib.add("a", "x")
        ib.add("b", "x")
        assert ib.count_unread() == 2

    def test_excludes_read(self):
        ib = PriorityInbox()
        m = ib.add("a", "x")
        ib.add("b", "x")
        ib.mark_read(m.msg_id)
        assert ib.count_unread() == 1

    def test_excludes_expired(self):
        ib = PriorityInbox()
        ib.add("a", "x", now=1.0, expires_at=5.0)
        ib.add("b", "x", now=1.0)
        assert ib.count_unread(now=10.0) == 1


# ----------------------------------------------------------------- Stats
class TestStats:
    def test_empty(self):
        ib = PriorityInbox()
        s = ib.stats()
        assert s.total == 0
        assert s.unread == 0
        assert s.read == 0
        assert s.archived == 0

    def test_counts(self):
        ib = PriorityInbox()
        m1 = ib.add("a", "x", priority=Priority.URGENT, category="alerts")
        ib.add("b", "x", priority=Priority.NORMAL, category="news")
        m3 = ib.add("c", "x", priority=Priority.LOW, category="alerts")
        ib.mark_read(m1.msg_id)
        ib.archive(m3.msg_id)
        s = ib.stats()
        assert s.total == 3
        assert s.unread == 1
        assert s.read == 1
        assert s.archived == 1
        assert s.by_priority[Priority.URGENT] == 1
        assert s.by_priority[Priority.NORMAL] == 1
        assert s.by_priority[Priority.LOW] == 1
        assert s.by_category["alerts"] == 2
        assert s.by_category["news"] == 1

    def test_expired_not_counted(self):
        ib = PriorityInbox()
        ib.add("a", "x", now=1.0, expires_at=5.0)
        ib.add("b", "x", now=1.0)
        s = ib.stats(now=10.0)
        assert s.total == 1


# ----------------------------------------------------------------- Expiration
class TestExpiration:
    def test_peek_skips_expired(self):
        ib = PriorityInbox()
        ib.add("a", "x", priority=Priority.URGENT, now=1.0, expires_at=5.0)
        assert ib.peek(now=10.0) is None

    def test_pop_skips_expired(self):
        ib = PriorityInbox()
        ib.add("a", "x", priority=Priority.URGENT, now=1.0, expires_at=5.0)
        assert ib.pop(now=10.0) is None

    def test_at_boundary_expires(self):
        ib = PriorityInbox()
        ib.add("a", "x", now=1.0, expires_at=5.0)
        assert ib.peek(now=5.0) is None

    def test_not_yet_expired(self):
        ib = PriorityInbox()
        ib.add("a", "x", now=1.0, expires_at=5.0)
        assert ib.peek(now=4.0) is not None

    def test_no_expiration(self):
        ib = PriorityInbox()
        ib.add("a", "x", now=1.0)
        assert ib.peek(now=1e12) is not None

    def test_expired_still_in_storage(self):
        ib = PriorityInbox()
        m = ib.add("a", "x", now=1.0, expires_at=5.0)
        # peek says nothing, but get() returns the message
        assert ib.peek(now=10.0) is None
        assert ib.get(m.msg_id) is not None


# ----------------------------------------------------------------- CleanupExpired
class TestCleanupExpired:
    def test_no_expired(self):
        ib = PriorityInbox()
        ib.add("a", "x")
        assert ib.cleanup_expired(now=10.0) == 0

    def test_removes_expired(self):
        ib = PriorityInbox()
        m1 = ib.add("a", "x", now=1.0, expires_at=5.0)
        m2 = ib.add("b", "x", now=1.0)
        removed = ib.cleanup_expired(now=10.0)
        assert removed == 1
        assert ib.get(m1.msg_id) is None
        assert ib.get(m2.msg_id) is not None

    def test_multiple(self):
        ib = PriorityInbox()
        for i in range(5):
            ib.add(f"s{i}", "x", now=1.0, expires_at=5.0)
        ib.add("alive", "x", now=1.0)
        assert ib.cleanup_expired(now=10.0) == 5
        assert ib.count_unread(now=10.0) == 1


# ----------------------------------------------------------------- Clear
class TestClear:
    def test_empty(self):
        ib = PriorityInbox()
        ib.clear()
        assert ib.stats().total == 0

    def test_clear_removes_all(self):
        ib = PriorityInbox()
        ib.add("a", "x")
        ib.add("b", "x")
        ib.clear()
        assert ib.stats().total == 0
        assert ib.peek() is None


# ----------------------------------------------------------------- EdgeCases
class TestEdgeCases:
    def test_empty_inbox(self):
        ib = PriorityInbox()
        assert ib.peek() is None
        assert ib.pop() is None
        assert ib.count_unread() == 0
        assert ib.list_unread() == []
        assert ib.stats().total == 0

    def test_all_expired(self):
        ib = PriorityInbox()
        for i in range(3):
            ib.add(f"s{i}", "x", now=1.0, expires_at=5.0)
        assert ib.peek(now=100.0) is None
        assert ib.pop(now=100.0) is None
        assert ib.count_unread(now=100.0) == 0

    def test_duplicate_id_via_add_message(self):
        ib = PriorityInbox()
        ib.add_message(Message("xx", "s1", "b", Priority.HIGH))
        ib.add_message(Message("xx", "s2", "b", Priority.LOW))
        # Second overwrites first
        assert ib.get("xx").subject == "s2"
        assert ib.stats().total == 1

    def test_pop_already_read_message(self):
        ib = PriorityInbox()
        m = ib.add("a", "x")
        ib.mark_read(m.msg_id)
        assert ib.pop() is None

    def test_delete_then_get(self):
        ib = PriorityInbox()
        m = ib.add("a", "x")
        ib.delete(m.msg_id)
        assert ib.get(m.msg_id) is None

    def test_archive_then_unread_listing(self):
        ib = PriorityInbox()
        m = ib.add("a", "x")
        ib.archive(m.msg_id)
        assert ib.list_unread() == []

    def test_mark_unread_after_archive(self):
        ib = PriorityInbox()
        m = ib.add("a", "x")
        ib.archive(m.msg_id)
        # archive is not deleted, mark_unread should still work
        assert ib.mark_unread(m.msg_id) is True
        assert ib.get(m.msg_id).status == MessageStatus.UNREAD


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
