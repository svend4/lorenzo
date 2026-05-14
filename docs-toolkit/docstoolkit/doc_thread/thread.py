"""Discussion thread manager for documents (E218).

Implements:
- ``MessageReaction`` enum (LIKE, DISLIKE, HEART, LAUGH, CONFUSED, INSIGHTFUL)
- ``MessageStatus`` enum (ACTIVE, EDITED, DELETED, RESOLVED, FLAGGED)
- ``ThreadMessage`` and ``Thread`` dataclasses
- ``DocThread`` class with thread/message/reaction operations

Stdlib only — uses ``threading`` and ``uuid``.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class MessageReaction(Enum):
    """Allowed reaction kinds for thread messages."""

    LIKE = "like"
    DISLIKE = "dislike"
    HEART = "heart"
    LAUGH = "laugh"
    CONFUSED = "confused"
    INSIGHTFUL = "insightful"


class MessageStatus(Enum):
    """Status of a thread message."""

    ACTIVE = "active"
    EDITED = "edited"
    DELETED = "deleted"
    RESOLVED = "resolved"
    FLAGGED = "flagged"


@dataclass
class ThreadMessage:
    """A single message inside a discussion thread."""

    message_id: str
    thread_id: str
    author: str
    content: str
    created_at: float = 0.0
    edited_at: Optional[float] = None
    parent_id: Optional[str] = None
    status: MessageStatus = MessageStatus.ACTIVE
    reactions: dict = field(default_factory=dict)  # reaction value -> set[str]


@dataclass
class Thread:
    """A discussion thread attached to a document."""

    thread_id: str
    doc_id: str
    created_by: str
    created_at: float
    messages: list = field(default_factory=list)
    participants: set = field(default_factory=set)
    archived: bool = False


class DocThread:
    """In-memory manager for document discussion threads."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._threads: dict[str, Thread] = {}
        # message_id -> (thread_id, ThreadMessage) for O(1) lookup
        self._msg_index: dict[str, ThreadMessage] = {}

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _new_id(prefix: str) -> str:
        return f"{prefix}-{uuid.uuid4().hex[:12]}"

    # ----------------------------------------------------------------- threads
    def create_thread(
        self,
        doc_id: str,
        created_by: str,
        initial_message: Optional[str] = None,
        now: float = 0.0,
    ) -> Thread:
        """Create a new thread for ``doc_id``."""
        with self._lock:
            thread_id = self._new_id("thr")
            thread = Thread(
                thread_id=thread_id,
                doc_id=doc_id,
                created_by=created_by,
                created_at=now,
            )
            thread.participants.add(created_by)
            self._threads[thread_id] = thread

            if initial_message:
                msg = ThreadMessage(
                    message_id=self._new_id("msg"),
                    thread_id=thread_id,
                    author=created_by,
                    content=initial_message,
                    created_at=now,
                )
                thread.messages.append(msg)
                self._msg_index[msg.message_id] = msg
            return thread

    def archive_thread(self, thread_id: str) -> bool:
        with self._lock:
            t = self._threads.get(thread_id)
            if t is None or t.archived:
                return False
            t.archived = True
            return True

    def unarchive_thread(self, thread_id: str) -> bool:
        with self._lock:
            t = self._threads.get(thread_id)
            if t is None or not t.archived:
                return False
            t.archived = False
            return True

    def delete_thread(self, thread_id: str) -> bool:
        with self._lock:
            t = self._threads.pop(thread_id, None)
            if t is None:
                return False
            for msg in t.messages:
                self._msg_index.pop(msg.message_id, None)
            return True

    # ---------------------------------------------------------------- messages
    def add_message(
        self,
        thread_id: str,
        author: str,
        content: str,
        parent_id: Optional[str] = None,
        now: float = 0.0,
    ) -> Optional[ThreadMessage]:
        with self._lock:
            t = self._threads.get(thread_id)
            if t is None or t.archived:
                return None
            if parent_id is not None:
                parent = self._msg_index.get(parent_id)
                if parent is None or parent.thread_id != thread_id:
                    return None
            msg = ThreadMessage(
                message_id=self._new_id("msg"),
                thread_id=thread_id,
                author=author,
                content=content,
                created_at=now,
                parent_id=parent_id,
            )
            t.messages.append(msg)
            t.participants.add(author)
            self._msg_index[msg.message_id] = msg
            return msg

    def edit_message(
        self, message_id: str, new_content: str, now: float = 0.0
    ) -> bool:
        with self._lock:
            msg = self._msg_index.get(message_id)
            if msg is None or msg.status == MessageStatus.DELETED:
                return False
            msg.content = new_content
            msg.edited_at = now
            # Preserve special statuses other than DELETED; mark active->edited.
            if msg.status == MessageStatus.ACTIVE:
                msg.status = MessageStatus.EDITED
            return True

    def delete_message(self, message_id: str, now: float = 0.0) -> bool:
        with self._lock:
            msg = self._msg_index.get(message_id)
            if msg is None or msg.status == MessageStatus.DELETED:
                return False
            msg.status = MessageStatus.DELETED
            msg.edited_at = now
            return True

    def flag_message(self, message_id: str) -> bool:
        with self._lock:
            msg = self._msg_index.get(message_id)
            if msg is None or msg.status == MessageStatus.DELETED:
                return False
            msg.status = MessageStatus.FLAGGED
            return True

    def resolve_message(self, message_id: str) -> bool:
        with self._lock:
            msg = self._msg_index.get(message_id)
            if msg is None or msg.status == MessageStatus.DELETED:
                return False
            msg.status = MessageStatus.RESOLVED
            return True

    # --------------------------------------------------------------- reactions
    def add_reaction(
        self, message_id: str, user_id: str, reaction: MessageReaction
    ) -> bool:
        if not isinstance(reaction, MessageReaction):
            return False
        with self._lock:
            msg = self._msg_index.get(message_id)
            if msg is None or msg.status == MessageStatus.DELETED:
                return False
            key = reaction.value
            users = msg.reactions.setdefault(key, set())
            if user_id in users:
                return False
            users.add(user_id)
            return True

    def remove_reaction(
        self, message_id: str, user_id: str, reaction: MessageReaction
    ) -> bool:
        if not isinstance(reaction, MessageReaction):
            return False
        with self._lock:
            msg = self._msg_index.get(message_id)
            if msg is None:
                return False
            key = reaction.value
            users = msg.reactions.get(key)
            if not users or user_id not in users:
                return False
            users.remove(user_id)
            if not users:
                del msg.reactions[key]
            return True

    # ----------------------------------------------------------------- queries
    def get_thread(self, thread_id: str) -> Optional[Thread]:
        with self._lock:
            return self._threads.get(thread_id)

    def get_message(self, message_id: str) -> Optional[ThreadMessage]:
        with self._lock:
            return self._msg_index.get(message_id)

    def threads_for_doc(
        self, doc_id: str, include_archived: bool = False
    ) -> list:
        with self._lock:
            out = []
            for t in self._threads.values():
                if t.doc_id != doc_id:
                    continue
                if t.archived and not include_archived:
                    continue
                out.append(t)
            out.sort(key=lambda t: t.created_at)
            return out

    def messages_for_thread(
        self, thread_id: str, include_deleted: bool = False
    ) -> list:
        with self._lock:
            t = self._threads.get(thread_id)
            if t is None:
                return []
            if include_deleted:
                return list(t.messages)
            return [m for m in t.messages if m.status != MessageStatus.DELETED]

    def replies_to(self, message_id: str) -> list:
        with self._lock:
            msg = self._msg_index.get(message_id)
            if msg is None:
                return []
            t = self._threads.get(msg.thread_id)
            if t is None:
                return []
            return [m for m in t.messages if m.parent_id == message_id]

    def participants_of(self, thread_id: str) -> set:
        with self._lock:
            t = self._threads.get(thread_id)
            if t is None:
                return set()
            return set(t.participants)

    def messages_by_author(self, author: str) -> list:
        with self._lock:
            return [m for m in self._msg_index.values() if m.author == author]

    def reaction_count(
        self, message_id: str, reaction: Optional[MessageReaction] = None
    ) -> int:
        with self._lock:
            msg = self._msg_index.get(message_id)
            if msg is None:
                return 0
            if reaction is None:
                return sum(len(u) for u in msg.reactions.values())
            return len(msg.reactions.get(reaction.value, set()))

    def top_reactions(self, message_id: str) -> list:
        with self._lock:
            msg = self._msg_index.get(message_id)
            if msg is None:
                return []
            pairs = []
            for key, users in msg.reactions.items():
                try:
                    pairs.append((MessageReaction(key), len(users)))
                except ValueError:
                    continue
            pairs.sort(key=lambda p: (-p[1], p[0].value))
            return pairs

    # ---------------------------------------------------------------- counters
    @property
    def thread_count(self) -> int:
        with self._lock:
            return len(self._threads)

    @property
    def message_count(self) -> int:
        with self._lock:
            return len(self._msg_index)

    def clear(self) -> None:
        with self._lock:
            self._threads.clear()
            self._msg_index.clear()
