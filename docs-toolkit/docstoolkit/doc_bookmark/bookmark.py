"""Bookmark manager for documents.

A purely in-memory implementation backed by simple ``dict`` indexes
and protected by a ``threading.Lock``.  No third-party dependencies.

Each user has a private list of :class:`Bookmark` objects which may
be grouped into :class:`Folder` instances, tagged, annotated and
reordered.  The store also tracks visit counts so that the most
popular documents (per-user and globally) can be reported.
"""
from __future__ import annotations

import threading
import time
import uuid
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Bookmark:
    """A single bookmark for a document owned by one user."""

    bookmark_id: str
    user_id: str
    doc_id: str
    folder: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    note: Optional[str] = None
    order: int = 0
    created_at: float = 0.0
    last_visited: Optional[float] = None
    visit_count: int = 0


@dataclass
class Folder:
    """A user-defined folder used to organise bookmarks."""

    folder_id: str
    user_id: str
    name: str
    parent_folder: Optional[str] = None
    created_at: float = 0.0


@dataclass
class UserBookmarkStats:
    """Aggregate statistics for a single user."""

    user_id: str
    total_bookmarks: int
    total_folders: int
    unique_docs: int
    unique_tags: int
    most_visited: list[tuple[str, int]]


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


class DocBookmark:
    """Thread-safe in-memory bookmark manager."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._bookmarks: dict[str, Bookmark] = {}
        self._folders: dict[str, Folder] = {}

    # ---- helpers --------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return now if now is not None else time.time()

    def _next_order(self, user_id: str, folder: Optional[str]) -> int:
        """Return the next ``order`` value for a user/folder slot."""
        max_order = -1
        for b in self._bookmarks.values():
            if b.user_id == user_id and b.folder == folder:
                if b.order > max_order:
                    max_order = b.order
        return max_order + 1

    # ---- bookmarks ------------------------------------------------------

    def add_bookmark(
        self,
        user_id: str,
        doc_id: str,
        folder: Optional[str] = None,
        tags: Optional[list[str]] = None,
        note: Optional[str] = None,
        now: Optional[float] = None,
    ) -> Bookmark:
        """Create a new bookmark and return it."""
        ts = self._now(now)
        bookmark_id = uuid.uuid4().hex
        with self._lock:
            order = self._next_order(user_id, folder)
            bm = Bookmark(
                bookmark_id=bookmark_id,
                user_id=user_id,
                doc_id=doc_id,
                folder=folder,
                tags=list(tags) if tags else [],
                note=note,
                order=order,
                created_at=ts,
                last_visited=None,
                visit_count=0,
            )
            self._bookmarks[bookmark_id] = bm
            return bm

    def remove_bookmark(self, bookmark_id: str) -> bool:
        with self._lock:
            return self._bookmarks.pop(bookmark_id, None) is not None

    def update_bookmark(
        self,
        bookmark_id: str,
        folder: Optional[str] = None,
        tags: Optional[list[str]] = None,
        note: Optional[str] = None,
    ) -> bool:
        """Update one or more attributes of an existing bookmark.

        Only the arguments that are not ``None`` are considered; to
        move a bookmark out of its folder use :meth:`move_to_folder`.
        """
        with self._lock:
            bm = self._bookmarks.get(bookmark_id)
            if bm is None:
                return False
            if folder is not None:
                bm.folder = folder
            if tags is not None:
                bm.tags = list(tags)
            if note is not None:
                bm.note = note
            return True

    def move_to_folder(
        self, bookmark_id: str, folder: Optional[str] = None
    ) -> bool:
        """Move a bookmark to ``folder`` (``None`` => root)."""
        with self._lock:
            bm = self._bookmarks.get(bookmark_id)
            if bm is None:
                return False
            bm.folder = folder
            bm.order = self._next_order(bm.user_id, folder)
            return True

    def add_tag(self, bookmark_id: str, tag: str) -> bool:
        with self._lock:
            bm = self._bookmarks.get(bookmark_id)
            if bm is None:
                return False
            if tag not in bm.tags:
                bm.tags.append(tag)
            return True

    def remove_tag(self, bookmark_id: str, tag: str) -> bool:
        with self._lock:
            bm = self._bookmarks.get(bookmark_id)
            if bm is None:
                return False
            if tag in bm.tags:
                bm.tags.remove(tag)
            return True

    def record_visit(
        self, bookmark_id: str, now: Optional[float] = None
    ) -> bool:
        ts = self._now(now)
        with self._lock:
            bm = self._bookmarks.get(bookmark_id)
            if bm is None:
                return False
            bm.last_visited = ts
            bm.visit_count += 1
            return True

    def get_bookmark(self, bookmark_id: str) -> Optional[Bookmark]:
        with self._lock:
            return self._bookmarks.get(bookmark_id)

    # ---- queries --------------------------------------------------------

    def bookmarks_for_user(
        self,
        user_id: str,
        folder: Optional[str] = None,
        sorted_by: str = "order",
    ) -> list[Bookmark]:
        """Return all bookmarks of ``user_id`` (optionally filtered by folder).

        ``sorted_by`` may be ``"order"`` (default), ``"created_at"``,
        ``"last_visited"`` or ``"visit_count"``.
        """
        with self._lock:
            items = [
                b
                for b in self._bookmarks.values()
                if b.user_id == user_id
                and (folder is None or b.folder == folder)
            ]
            if sorted_by == "order":
                items.sort(key=lambda b: b.order)
            elif sorted_by == "created_at":
                items.sort(key=lambda b: b.created_at)
            elif sorted_by == "last_visited":
                items.sort(
                    key=lambda b: (b.last_visited if b.last_visited is not None else 0.0),
                    reverse=True,
                )
            elif sorted_by == "visit_count":
                items.sort(key=lambda b: b.visit_count, reverse=True)
            else:
                raise ValueError(f"Unknown sorted_by: {sorted_by}")
            return items

    def bookmarks_with_tag(self, user_id: str, tag: str) -> list[Bookmark]:
        with self._lock:
            return [
                b
                for b in self._bookmarks.values()
                if b.user_id == user_id and tag in b.tags
            ]

    def bookmarks_for_doc(self, doc_id: str) -> list[Bookmark]:
        with self._lock:
            return [
                b for b in self._bookmarks.values() if b.doc_id == doc_id
            ]

    def reorder(self, bookmark_id: str, new_order: int) -> bool:
        with self._lock:
            bm = self._bookmarks.get(bookmark_id)
            if bm is None:
                return False
            bm.order = new_order
            return True

    # ---- folders --------------------------------------------------------

    def create_folder(
        self,
        user_id: str,
        name: str,
        parent_folder: Optional[str] = None,
        now: Optional[float] = None,
    ) -> Folder:
        ts = self._now(now)
        folder_id = uuid.uuid4().hex
        with self._lock:
            folder = Folder(
                folder_id=folder_id,
                user_id=user_id,
                name=name,
                parent_folder=parent_folder,
                created_at=ts,
            )
            self._folders[folder_id] = folder
            return folder

    def delete_folder(
        self, folder_id: str, move_to: Optional[str] = None
    ) -> bool:
        """Delete ``folder_id``.

        Any bookmarks currently stored in the deleted folder are moved
        to ``move_to`` (or to the root when ``move_to`` is ``None``).
        """
        with self._lock:
            folder = self._folders.pop(folder_id, None)
            if folder is None:
                return False
            for bm in self._bookmarks.values():
                if bm.folder == folder_id:
                    bm.folder = move_to
                    bm.order = self._next_order(bm.user_id, move_to)
            return True

    def folders_for_user(self, user_id: str) -> list[Folder]:
        with self._lock:
            return [
                f for f in self._folders.values() if f.user_id == user_id
            ]

    # ---- aggregates -----------------------------------------------------

    def is_bookmarked(self, user_id: str, doc_id: str) -> bool:
        with self._lock:
            for b in self._bookmarks.values():
                if b.user_id == user_id and b.doc_id == doc_id:
                    return True
            return False

    def total_bookmarks_for_user(self, user_id: str) -> int:
        with self._lock:
            return sum(
                1 for b in self._bookmarks.values() if b.user_id == user_id
            )

    def user_stats(
        self, user_id: str, top_k: int = 5
    ) -> UserBookmarkStats:
        with self._lock:
            user_bookmarks = [
                b for b in self._bookmarks.values() if b.user_id == user_id
            ]
            user_folders = [
                f for f in self._folders.values() if f.user_id == user_id
            ]
            unique_docs = {b.doc_id for b in user_bookmarks}
            unique_tags: set[str] = set()
            for b in user_bookmarks:
                unique_tags.update(b.tags)
            visit_counter: Counter[str] = Counter()
            for b in user_bookmarks:
                if b.visit_count > 0:
                    visit_counter[b.doc_id] += b.visit_count
            most_visited = visit_counter.most_common(top_k)
            return UserBookmarkStats(
                user_id=user_id,
                total_bookmarks=len(user_bookmarks),
                total_folders=len(user_folders),
                unique_docs=len(unique_docs),
                unique_tags=len(unique_tags),
                most_visited=most_visited,
            )

    def popular_docs(self, top_k: int = 10) -> list[tuple[str, int]]:
        """Return the most-bookmarked documents across all users."""
        with self._lock:
            counter: Counter[str] = Counter()
            for b in self._bookmarks.values():
                counter[b.doc_id] += 1
            return counter.most_common(top_k)

    # ---- totals & maintenance -------------------------------------------

    @property
    def total_bookmarks(self) -> int:
        with self._lock:
            return len(self._bookmarks)

    @property
    def total_folders(self) -> int:
        with self._lock:
            return len(self._folders)

    def clear(self) -> None:
        with self._lock:
            self._bookmarks.clear()
            self._folders.clear()
