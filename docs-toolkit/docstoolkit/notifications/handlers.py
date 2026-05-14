import sqlite3
import json
from abc import ABC, abstractmethod
from docstoolkit.notifications.message import Notification, Channel


class NotificationHandler(ABC):
    """Abstract handler for one delivery channel."""
    channel: Channel

    @abstractmethod
    def send(self, notification: Notification) -> bool:
        """Send notification. Returns True on success."""


class LogHandler(NotificationHandler):
    """Logs notifications to an in-memory list (for testing)."""
    channel = Channel.LOG

    def __init__(self):
        self._log: list = []

    def send(self, notification: Notification) -> bool:
        self._log.append(notification)
        return True

    def messages(self) -> list:
        return list(self._log)

    def clear(self) -> None:
        self._log.clear()


class NullHandler(NotificationHandler):
    """Discards all notifications."""
    channel = Channel.NULL

    def send(self, notification: Notification) -> bool:
        return True


class StoreHandler(NotificationHandler):
    """Stores notifications in SQLite."""
    channel = Channel.STORE

    _SCHEMA = """
    CREATE TABLE IF NOT EXISTS notifications (
        notification_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        level TEXT NOT NULL,
        source TEXT NOT NULL DEFAULT '',
        tags_json TEXT NOT NULL DEFAULT '[]',
        ts TEXT NOT NULL
    );
    """

    def __init__(self, db_path=None):
        self._path = str(db_path) if db_path else ":memory:"
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(self._SCHEMA)
        self._conn.commit()

    def send(self, notification: Notification) -> bool:
        try:
            self._conn.execute(
                "INSERT OR IGNORE INTO notifications "
                "(notification_id, title, body, level, source, tags_json, ts) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (notification.notification_id, notification.title, notification.body,
                 notification.level.value, notification.source,
                 json.dumps(notification.tags), notification.ts),
            )
            self._conn.commit()
            return True
        except Exception:
            return False

    def count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM notifications").fetchone()[0]

    def list_by_level(self, level) -> list:
        rows = self._conn.execute(
            "SELECT * FROM notifications WHERE level=? ORDER BY ts DESC",
            (level.value,)
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self):
        self._conn.close()
