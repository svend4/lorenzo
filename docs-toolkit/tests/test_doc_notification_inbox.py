"""Tests for E326 DocNotificationInbox."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_notification_inbox import (
    DocNotificationInbox,
    InboxStats,
    Notification,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------
class TestNotificationDataclass:
    def test_default_construction(self):
        n = Notification()
        assert n.notification_id == ""
        assert n.user_id == ""
        assert n.doc_id is None
        assert n.title == ""
        assert n.body == ""
        assert n.category == "info"
        assert n.created_at == 0.0
        assert n.read is False
        assert n.archived is False

    def test_custom_fields(self):
        n = Notification(
            notification_id="x",
            user_id="u",
            doc_id="d",
            title="t",
            body="b",
            category="alert",
            created_at=1.5,
            read=True,
            archived=True,
        )
        assert n.notification_id == "x"
        assert n.user_id == "u"
        assert n.doc_id == "d"
        assert n.title == "t"
        assert n.body == "b"
        assert n.category == "alert"
        assert n.created_at == 1.5
        assert n.read is True
        assert n.archived is True

    def test_is_dataclass(self):
        import dataclasses

        assert dataclasses.is_dataclass(Notification)

    def test_category_default_info(self):
        n = Notification(notification_id="x", user_id="u")
        assert n.category == "info"


class TestInboxStatsDataclass:
    def test_default_construction(self):
        s = InboxStats()
        assert s.total_notifications == 0
        assert s.unread_count == 0
        assert s.unique_users == 0
        assert s.archived_count == 0

    def test_custom_fields(self):
        s = InboxStats(
            total_notifications=10,
            unread_count=3,
            unique_users=2,
            archived_count=1,
        )
        assert s.total_notifications == 10
        assert s.unread_count == 3
        assert s.unique_users == 2
        assert s.archived_count == 1

    def test_is_dataclass(self):
        import dataclasses

        assert dataclasses.is_dataclass(InboxStats)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_inbox(self):
        inbox = DocNotificationInbox()
        assert inbox.all_users() == []

    def test_initial_stats_empty(self):
        inbox = DocNotificationInbox()
        s = inbox.stats()
        assert s.total_notifications == 0
        assert s.unread_count == 0
        assert s.unique_users == 0
        assert s.archived_count == 0

    def test_get_missing_returns_none(self):
        inbox = DocNotificationInbox()
        assert inbox.get("nope") is None


# ---------------------------------------------------------------------------
# Send
# ---------------------------------------------------------------------------
class TestSend:
    def test_send_returns_notification(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1", title="Hi")
        assert isinstance(n, Notification)

    def test_send_assigns_uuid(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        assert n.notification_id
        assert len(n.notification_id) >= 16

    def test_send_unique_ids(self):
        inbox = DocNotificationInbox()
        ids = {inbox.send("u1").notification_id for _ in range(50)}
        assert len(ids) == 50

    def test_send_sets_user_id(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u42")
        assert n.user_id == "u42"

    def test_send_default_category(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        assert n.category == "info"

    def test_send_custom_category(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1", category="alert")
        assert n.category == "alert"

    def test_send_default_read_false(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        assert n.read is False

    def test_send_default_archived_false(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        assert n.archived is False

    def test_send_timestamp_now(self):
        inbox = DocNotificationInbox()
        before = time.time()
        n = inbox.send("u1")
        after = time.time()
        assert before <= n.created_at <= after

    def test_send_explicit_now(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1", now=42.0)
        assert n.created_at == 42.0

    def test_send_doc_id(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1", doc_id="doc-7")
        assert n.doc_id == "doc-7"

    def test_send_title_body(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1", title="T", body="B")
        assert n.title == "T"
        assert n.body == "B"

    def test_send_stored_retrievable(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        assert inbox.get(n.notification_id) is n


# ---------------------------------------------------------------------------
# mark_read
# ---------------------------------------------------------------------------
class TestMarkRead:
    def test_mark_read_returns_true(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        assert inbox.mark_read(n.notification_id) is True

    def test_mark_read_sets_read_true(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.mark_read(n.notification_id)
        assert inbox.get(n.notification_id).read is True

    def test_mark_read_missing_returns_false(self):
        inbox = DocNotificationInbox()
        assert inbox.mark_read("nope") is False

    def test_mark_read_idempotent(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.mark_read(n.notification_id)
        assert inbox.mark_read(n.notification_id) is True
        assert inbox.get(n.notification_id).read is True


# ---------------------------------------------------------------------------
# mark_unread
# ---------------------------------------------------------------------------
class TestMarkUnread:
    def test_mark_unread_returns_true(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.mark_read(n.notification_id)
        assert inbox.mark_unread(n.notification_id) is True

    def test_mark_unread_sets_read_false(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.mark_read(n.notification_id)
        inbox.mark_unread(n.notification_id)
        assert inbox.get(n.notification_id).read is False

    def test_mark_unread_missing_returns_false(self):
        inbox = DocNotificationInbox()
        assert inbox.mark_unread("nope") is False


# ---------------------------------------------------------------------------
# mark_all_read
# ---------------------------------------------------------------------------
class TestMarkAllRead:
    def test_mark_all_read_count(self):
        inbox = DocNotificationInbox()
        inbox.send("u1")
        inbox.send("u1")
        inbox.send("u1")
        assert inbox.mark_all_read("u1") == 3

    def test_mark_all_read_skips_already_read(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        inbox.send("u1")
        inbox.mark_read(a.notification_id)
        assert inbox.mark_all_read("u1") == 1

    def test_mark_all_read_only_user(self):
        inbox = DocNotificationInbox()
        inbox.send("u1")
        b = inbox.send("u2")
        inbox.mark_all_read("u1")
        assert inbox.get(b.notification_id).read is False

    def test_mark_all_read_unknown_user(self):
        inbox = DocNotificationInbox()
        assert inbox.mark_all_read("ghost") == 0


# ---------------------------------------------------------------------------
# Archive
# ---------------------------------------------------------------------------
class TestArchive:
    def test_archive_returns_true(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        assert inbox.archive(n.notification_id) is True

    def test_archive_sets_archived_true(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.archive(n.notification_id)
        assert inbox.get(n.notification_id).archived is True

    def test_archive_missing_returns_false(self):
        inbox = DocNotificationInbox()
        assert inbox.archive("nope") is False


# ---------------------------------------------------------------------------
# Unarchive
# ---------------------------------------------------------------------------
class TestUnarchive:
    def test_unarchive_returns_true(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.archive(n.notification_id)
        assert inbox.unarchive(n.notification_id) is True

    def test_unarchive_sets_archived_false(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.archive(n.notification_id)
        inbox.unarchive(n.notification_id)
        assert inbox.get(n.notification_id).archived is False

    def test_unarchive_missing_returns_false(self):
        inbox = DocNotificationInbox()
        assert inbox.unarchive("nope") is False


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
class TestDelete:
    def test_delete_returns_true(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        assert inbox.delete(n.notification_id) is True

    def test_delete_removes_notification(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.delete(n.notification_id)
        assert inbox.get(n.notification_id) is None

    def test_delete_removes_from_inbox(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.delete(n.notification_id)
        assert inbox.inbox_for("u1") == []

    def test_delete_missing_returns_false(self):
        inbox = DocNotificationInbox()
        assert inbox.delete("nope") is False

    def test_delete_user_disappears_when_empty(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        inbox.delete(n.notification_id)
        assert "u1" not in inbox.all_users()


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------
class TestGet:
    def test_get_found(self):
        inbox = DocNotificationInbox()
        n = inbox.send("u1")
        assert inbox.get(n.notification_id) is n

    def test_get_not_found(self):
        inbox = DocNotificationInbox()
        assert inbox.get("missing") is None


# ---------------------------------------------------------------------------
# inbox_for
# ---------------------------------------------------------------------------
class TestInboxFor:
    def test_inbox_for_empty_user(self):
        inbox = DocNotificationInbox()
        assert inbox.inbox_for("ghost") == []

    def test_inbox_for_most_recent_first(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1", now=1.0)
        b = inbox.send("u1", now=2.0)
        c = inbox.send("u1", now=3.0)
        order = [n.notification_id for n in inbox.inbox_for("u1")]
        assert order == [c.notification_id, b.notification_id, a.notification_id]

    def test_inbox_for_unread_only(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        b = inbox.send("u1")
        inbox.mark_read(a.notification_id)
        ids = {n.notification_id for n in inbox.inbox_for("u1", unread_only=True)}
        assert ids == {b.notification_id}

    def test_inbox_for_excludes_archived_by_default(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        inbox.send("u1")
        inbox.archive(a.notification_id)
        ids = {n.notification_id for n in inbox.inbox_for("u1")}
        assert a.notification_id not in ids

    def test_inbox_for_include_archived(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        inbox.archive(a.notification_id)
        ids = {
            n.notification_id
            for n in inbox.inbox_for("u1", include_archived=True)
        }
        assert a.notification_id in ids

    def test_inbox_for_only_user(self):
        inbox = DocNotificationInbox()
        inbox.send("u1")
        b = inbox.send("u2")
        ids = {n.notification_id for n in inbox.inbox_for("u2")}
        assert ids == {b.notification_id}


# ---------------------------------------------------------------------------
# unread_count
# ---------------------------------------------------------------------------
class TestUnreadCount:
    def test_unread_count_zero(self):
        inbox = DocNotificationInbox()
        assert inbox.unread_count("u1") == 0

    def test_unread_count_basic(self):
        inbox = DocNotificationInbox()
        inbox.send("u1")
        inbox.send("u1")
        assert inbox.unread_count("u1") == 2

    def test_unread_count_after_mark_read(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        inbox.send("u1")
        inbox.mark_read(a.notification_id)
        assert inbox.unread_count("u1") == 1

    def test_unread_count_per_user(self):
        inbox = DocNotificationInbox()
        inbox.send("u1")
        inbox.send("u2")
        inbox.send("u2")
        assert inbox.unread_count("u2") == 2
        assert inbox.unread_count("u1") == 1

    def test_unread_count_ignores_archived(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        inbox.send("u1")
        inbox.archive(a.notification_id)
        assert inbox.unread_count("u1") == 1


# ---------------------------------------------------------------------------
# notifications_by_category
# ---------------------------------------------------------------------------
class TestNotificationsByCategory:
    def test_filter_by_category(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1", category="alert")
        inbox.send("u1", category="info")
        ids = {n.notification_id for n in inbox.notifications_by_category("u1", "alert")}
        assert ids == {a.notification_id}

    def test_category_empty(self):
        inbox = DocNotificationInbox()
        inbox.send("u1", category="info")
        assert inbox.notifications_by_category("u1", "alert") == []

    def test_category_most_recent_first(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1", category="warning", now=1.0)
        b = inbox.send("u1", category="warning", now=2.0)
        ids = [n.notification_id for n in inbox.notifications_by_category("u1", "warning")]
        assert ids == [b.notification_id, a.notification_id]

    def test_category_only_user(self):
        inbox = DocNotificationInbox()
        inbox.send("u1", category="alert")
        b = inbox.send("u2", category="alert")
        ids = {n.notification_id for n in inbox.notifications_by_category("u2", "alert")}
        assert ids == {b.notification_id}


# ---------------------------------------------------------------------------
# clear_archived
# ---------------------------------------------------------------------------
class TestClearArchived:
    def test_clear_archived_count(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        b = inbox.send("u1")
        inbox.archive(a.notification_id)
        inbox.archive(b.notification_id)
        assert inbox.clear_archived("u1") == 2

    def test_clear_archived_zero_when_none(self):
        inbox = DocNotificationInbox()
        inbox.send("u1")
        assert inbox.clear_archived("u1") == 0

    def test_clear_archived_only_archived_removed(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        b = inbox.send("u1")
        inbox.archive(a.notification_id)
        inbox.clear_archived("u1")
        assert inbox.get(a.notification_id) is None
        assert inbox.get(b.notification_id) is not None

    def test_clear_archived_unknown_user(self):
        inbox = DocNotificationInbox()
        assert inbox.clear_archived("ghost") == 0

    def test_clear_archived_only_target_user(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        b = inbox.send("u2")
        inbox.archive(a.notification_id)
        inbox.archive(b.notification_id)
        inbox.clear_archived("u1")
        assert inbox.get(b.notification_id) is not None


# ---------------------------------------------------------------------------
# all_users
# ---------------------------------------------------------------------------
class TestAllUsers:
    def test_all_users_empty(self):
        inbox = DocNotificationInbox()
        assert inbox.all_users() == []

    def test_all_users_sorted(self):
        inbox = DocNotificationInbox()
        inbox.send("charlie")
        inbox.send("alpha")
        inbox.send("bravo")
        assert inbox.all_users() == ["alpha", "bravo", "charlie"]

    def test_all_users_unique(self):
        inbox = DocNotificationInbox()
        inbox.send("u1")
        inbox.send("u1")
        assert inbox.all_users() == ["u1"]


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_stats_total(self):
        inbox = DocNotificationInbox()
        inbox.send("u1")
        inbox.send("u2")
        inbox.send("u2")
        assert inbox.stats().total_notifications == 3

    def test_stats_unique_users(self):
        inbox = DocNotificationInbox()
        inbox.send("u1")
        inbox.send("u2")
        inbox.send("u2")
        assert inbox.stats().unique_users == 2

    def test_stats_unread(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        inbox.send("u1")
        inbox.mark_read(a.notification_id)
        assert inbox.stats().unread_count == 1

    def test_stats_archived(self):
        inbox = DocNotificationInbox()
        a = inbox.send("u1")
        inbox.send("u1")
        inbox.archive(a.notification_id)
        assert inbox.stats().archived_count == 1

    def test_stats_returns_inboxstats(self):
        inbox = DocNotificationInbox()
        assert isinstance(inbox.stats(), InboxStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_send(self):
        inbox = DocNotificationInbox()
        n_threads = 8
        per_thread = 50

        def worker():
            for _ in range(per_thread):
                inbox.send("u1")

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert inbox.stats().total_notifications == n_threads * per_thread
        assert inbox.unread_count("u1") == n_threads * per_thread

    def test_concurrent_send_unique_ids(self):
        inbox = DocNotificationInbox()
        results: list[str] = []
        lock = threading.Lock()

        def worker():
            local = []
            for _ in range(25):
                local.append(inbox.send("u1").notification_id)
            with lock:
                results.extend(local)

        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == len(set(results))

    def test_concurrent_send_multi_user(self):
        inbox = DocNotificationInbox()

        def worker(uid):
            for _ in range(20):
                inbox.send(uid)

        threads = [
            threading.Thread(target=worker, args=(f"user-{i}",)) for i in range(5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert inbox.stats().total_notifications == 100
        assert inbox.stats().unique_users == 5
