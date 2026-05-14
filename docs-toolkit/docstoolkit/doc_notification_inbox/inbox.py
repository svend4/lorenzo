"""E326 DocNotificationInbox — per-user notification inbox implementation.

Pure stdlib, thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Notification:
    """A single notification stored in an inbox."""

    notification_id: str = ""
    user_id: str = ""
    doc_id: Optional[str] = None
    title: str = ""
    body: str = ""
    category: str = "info"
    created_at: float = 0.0
    read: bool = False
    archived: bool = False


@dataclass
class InboxStats:
    """Aggregate statistics across all inboxes."""

    total_notifications: int = 0
    unread_count: int = 0
    unique_users: int = 0
    archived_count: int = 0


class DocNotificationInbox:
    """Per-user notification inbox with read/unread, archive, and category filters."""

    def __init__(self) -> None:
        self._notifications: dict[str, Notification] = {}
        self._by_user: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Sending
    # ------------------------------------------------------------------
    def send(
        self,
        user_id: str,
        title: str = "",
        body: str = "",
        category: str = "info",
        doc_id: Optional[str] = None,
        now: Optional[float] = None,
    ) -> Notification:
        """Create and store a new notification for ``user_id``."""
        ts = now if now is not None else time.time()
        nid = uuid.uuid4().hex
        notif = Notification(
            notification_id=nid,
            user_id=user_id,
            doc_id=doc_id,
            title=title,
            body=body,
            category=category,
            created_at=ts,
            read=False,
            archived=False,
        )
        with self._lock:
            self._notifications[nid] = notif
            self._by_user.setdefault(user_id, []).append(nid)
        return notif

    # ------------------------------------------------------------------
    # Read / unread
    # ------------------------------------------------------------------
    def mark_read(self, notification_id: str) -> bool:
        with self._lock:
            n = self._notifications.get(notification_id)
            if n is None:
                return False
            n.read = True
            return True

    def mark_unread(self, notification_id: str) -> bool:
        with self._lock:
            n = self._notifications.get(notification_id)
            if n is None:
                return False
            n.read = False
            return True

    def mark_all_read(self, user_id: str) -> int:
        count = 0
        with self._lock:
            for nid in self._by_user.get(user_id, []):
                n = self._notifications.get(nid)
                if n is not None and not n.read:
                    n.read = True
                    count += 1
        return count

    # ------------------------------------------------------------------
    # Archive
    # ------------------------------------------------------------------
    def archive(self, notification_id: str) -> bool:
        with self._lock:
            n = self._notifications.get(notification_id)
            if n is None:
                return False
            n.archived = True
            return True

    def unarchive(self, notification_id: str) -> bool:
        with self._lock:
            n = self._notifications.get(notification_id)
            if n is None:
                return False
            n.archived = False
            return True

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------
    def delete(self, notification_id: str) -> bool:
        with self._lock:
            n = self._notifications.pop(notification_id, None)
            if n is None:
                return False
            ids = self._by_user.get(n.user_id)
            if ids is not None:
                try:
                    ids.remove(notification_id)
                except ValueError:
                    pass
                if not ids:
                    self._by_user.pop(n.user_id, None)
            return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def get(self, notification_id: str) -> Optional[Notification]:
        with self._lock:
            return self._notifications.get(notification_id)

    def inbox_for(
        self,
        user_id: str,
        unread_only: bool = False,
        include_archived: bool = False,
    ) -> list[Notification]:
        """Return notifications for ``user_id``, most recent first."""
        with self._lock:
            ids = list(self._by_user.get(user_id, []))
            items = [self._notifications[i] for i in ids if i in self._notifications]
        result = []
        for n in items:
            if not include_archived and n.archived:
                continue
            if unread_only and n.read:
                continue
            result.append(n)
        # Most recent first: reverse insertion order (stable for equal timestamps)
        result.sort(key=lambda x: x.created_at, reverse=True)
        return result

    def unread_count(self, user_id: str) -> int:
        with self._lock:
            ids = list(self._by_user.get(user_id, []))
            return sum(
                1
                for i in ids
                if i in self._notifications
                and not self._notifications[i].read
                and not self._notifications[i].archived
            )

    def notifications_by_category(
        self, user_id: str, category: str
    ) -> list[Notification]:
        with self._lock:
            ids = list(self._by_user.get(user_id, []))
            items = [
                self._notifications[i]
                for i in ids
                if i in self._notifications
                and self._notifications[i].category == category
            ]
        items.sort(key=lambda x: x.created_at, reverse=True)
        return items

    def clear_archived(self, user_id: str) -> int:
        count = 0
        with self._lock:
            ids = list(self._by_user.get(user_id, []))
            to_remove = [
                nid
                for nid in ids
                if nid in self._notifications and self._notifications[nid].archived
            ]
            for nid in to_remove:
                self._notifications.pop(nid, None)
                try:
                    self._by_user[user_id].remove(nid)
                except (ValueError, KeyError):
                    pass
                count += 1
            if user_id in self._by_user and not self._by_user[user_id]:
                self._by_user.pop(user_id, None)
        return count

    def all_users(self) -> list[str]:
        with self._lock:
            return sorted(self._by_user.keys())

    def stats(self) -> InboxStats:
        with self._lock:
            total = len(self._notifications)
            unread = sum(
                1
                for n in self._notifications.values()
                if not n.read and not n.archived
            )
            archived = sum(1 for n in self._notifications.values() if n.archived)
            users = len(self._by_user)
        return InboxStats(
            total_notifications=total,
            unread_count=unread,
            unique_users=users,
            archived_count=archived,
        )
