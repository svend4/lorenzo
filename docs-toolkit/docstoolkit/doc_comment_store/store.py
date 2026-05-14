"""DocCommentStore — thread-safe comment storage for documents.

Stdlib only — uses ``threading.Lock`` for thread safety.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Comment:
    """A single comment — either a top-level comment or a reply."""

    comment_id: str
    doc_id: str
    author: str
    body: str
    created_at: float = 0.0
    parent_id: Optional[str] = None  # None = top-level; set = reply to that comment_id
    edited_at: Optional[float] = None
    deleted: bool = False


@dataclass
class CommentThread:
    """A top-level comment with its direct replies."""

    root: Comment
    replies: list[Comment] = field(default_factory=list)  # sorted by created_at


@dataclass
class CommentStats:
    """Aggregate statistics for the comment store."""

    total_comments: int   # including replies, excluding deleted
    total_threads: int    # top-level non-deleted comments
    unique_authors: int
    docs_with_comments: int


class DocCommentStore:
    """Main interface for comment CRUD.

    All mutations and reads are guarded by a single ``threading.Lock``, making
    this safe to use from multiple threads simultaneously.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._comments: dict[str, Comment] = {}          # comment_id → Comment
        self._by_doc: dict[str, list[str]] = {}          # doc_id → list of comment_ids (insertion order)

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def add_comment(
        self,
        doc_id: str,
        author: str,
        body: str,
        parent_id: Optional[str] = None,
        now: Optional[float] = None,
    ) -> Comment:
        """Add a new comment (top-level or reply).

        Generates a UUID for ``comment_id``.  ``now`` defaults to ``0.0`` when
        not provided, allowing deterministic testing without importing time.
        """
        created_at = now if now is not None else 0.0
        comment = Comment(
            comment_id=str(uuid.uuid4()),
            doc_id=doc_id,
            author=author,
            body=body,
            created_at=created_at,
            parent_id=parent_id,
        )
        with self._lock:
            self._comments[comment.comment_id] = comment
            self._by_doc.setdefault(doc_id, []).append(comment.comment_id)
        return comment

    def edit_comment(
        self,
        comment_id: str,
        new_body: str,
        now: Optional[float] = None,
    ) -> bool:
        """Update the body of a comment and record the edit timestamp.

        Returns ``False`` if the comment is not found or is deleted.
        """
        edited_at = now if now is not None else 0.0
        with self._lock:
            comment = self._comments.get(comment_id)
            if comment is None or comment.deleted:
                return False
            comment.body = new_body
            comment.edited_at = edited_at
            return True

    def delete_comment(self, comment_id: str) -> bool:
        """Soft-delete a comment by marking ``deleted=True``.

        Returns ``False`` if the comment is not found.
        """
        with self._lock:
            comment = self._comments.get(comment_id)
            if comment is None:
                return False
            comment.deleted = True
            return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_comment(self, comment_id: str) -> Optional[Comment]:
        """Return the comment with the given id, or ``None`` if not found."""
        with self._lock:
            return self._comments.get(comment_id)

    def comments_for_doc(
        self,
        doc_id: str,
        include_deleted: bool = False,
    ) -> list[Comment]:
        """Return comments for a document in insertion order.

        By default excludes deleted comments; pass ``include_deleted=True`` to
        include them.
        """
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            result = []
            for cid in ids:
                c = self._comments.get(cid)
                if c is None:
                    continue
                if not include_deleted and c.deleted:
                    continue
                result.append(c)
        return result

    def threads_for_doc(self, doc_id: str) -> list[CommentThread]:
        """Return top-level non-deleted comments as threads with their replies.

        Threads are ordered by ``root.created_at``.  Each thread's replies are
        non-deleted direct replies sorted by ``created_at``.
        """
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            all_comments = [
                self._comments[cid]
                for cid in ids
                if cid in self._comments
            ]

        # Separate top-level and replies
        top_level = [c for c in all_comments if c.parent_id is None and not c.deleted]
        top_level.sort(key=lambda c: c.created_at)

        # Build a lookup: parent_id → list of reply comments
        replies_map: dict[str, list[Comment]] = {}
        for c in all_comments:
            if c.parent_id is not None and not c.deleted:
                replies_map.setdefault(c.parent_id, []).append(c)

        threads = []
        for root in top_level:
            replies = sorted(
                replies_map.get(root.comment_id, []),
                key=lambda c: c.created_at,
            )
            threads.append(CommentThread(root=root, replies=replies))

        return threads

    def replies_to(self, comment_id: str) -> list[Comment]:
        """Return non-deleted direct replies to the given comment, sorted by created_at."""
        with self._lock:
            result = [
                c for c in self._comments.values()
                if c.parent_id == comment_id and not c.deleted
            ]
        result.sort(key=lambda c: c.created_at)
        return result

    def comment_count(self, doc_id: str) -> int:
        """Return the number of non-deleted comments for a document."""
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            return sum(
                1
                for cid in ids
                if cid in self._comments and not self._comments[cid].deleted
            )

    def all_doc_ids(self) -> list[str]:
        """Return sorted list of doc_ids that have at least one non-deleted comment."""
        with self._lock:
            result = []
            for doc_id, ids in self._by_doc.items():
                has_live = any(
                    cid in self._comments and not self._comments[cid].deleted
                    for cid in ids
                )
                if has_live:
                    result.append(doc_id)
        return sorted(result)

    def stats(self) -> CommentStats:
        """Return aggregate statistics for the store."""
        with self._lock:
            total_comments = 0
            total_threads = 0
            authors: set[str] = set()
            docs_with_comments: set[str] = set()

            for comment in self._comments.values():
                if comment.deleted:
                    continue
                total_comments += 1
                authors.add(comment.author)
                docs_with_comments.add(comment.doc_id)
                if comment.parent_id is None:
                    total_threads += 1

        return CommentStats(
            total_comments=total_comments,
            total_threads=total_threads,
            unique_authors=len(authors),
            docs_with_comments=len(docs_with_comments),
        )
