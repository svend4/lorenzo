"""E396 DocViewLayout — per-user view layout preferences.

Pure stdlib, thread-safe via :class:`threading.Lock`, dataclasses throughout.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ViewLayout:
    """A single saved view layout for a (user, doc) pair."""

    user_id: str
    doc_id: str
    panels: list = field(default_factory=list)
    column_widths: dict = field(default_factory=dict)
    theme: str = "default"
    updated_at: float = 0.0


@dataclass
class ViewLayoutStats:
    """Aggregate statistics over stored layouts."""

    total_layouts: int
    unique_users: int
    unique_docs: int


class DocViewLayout:
    """Main interface for managing per-user view layouts.

    Stores user-specific layouts keyed by ``(user_id, doc_id)`` plus optional
    per-doc default layouts that act as a fallback in :meth:`resolve`.
    """

    def __init__(self) -> None:
        self._layouts: dict = {}            # (user_id, doc_id) -> ViewLayout
        self._by_user: dict = {}            # user_id -> set[doc_id]
        self._by_doc: dict = {}             # doc_id  -> set[user_id]
        self._defaults: dict = {}           # doc_id  -> ViewLayout
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ save
    def save_layout(
        self,
        user_id: str,
        doc_id: str,
        panels: list,
        column_widths: Optional[dict] = None,
        theme: str = "default",
        now: Optional[float] = None,
    ) -> ViewLayout:
        """Create or replace a layout for ``(user_id, doc_id)``."""
        ts = time.time() if now is None else now
        layout = ViewLayout(
            user_id=user_id,
            doc_id=doc_id,
            panels=list(panels),
            column_widths=dict(column_widths) if column_widths else {},
            theme=theme,
            updated_at=ts,
        )
        key = (user_id, doc_id)
        with self._lock:
            self._layouts[key] = layout
            self._by_user.setdefault(user_id, set()).add(doc_id)
            self._by_doc.setdefault(doc_id, set()).add(user_id)
        return layout

    # ------------------------------------------------------------------- get
    def get_layout(self, user_id: str, doc_id: str) -> Optional[ViewLayout]:
        with self._lock:
            return self._layouts.get((user_id, doc_id))

    # ---------------------------------------------------------------- delete
    def delete_layout(self, user_id: str, doc_id: str) -> bool:
        key = (user_id, doc_id)
        with self._lock:
            if key not in self._layouts:
                return False
            del self._layouts[key]
            docs = self._by_user.get(user_id)
            if docs is not None:
                docs.discard(doc_id)
                if not docs:
                    del self._by_user[user_id]
            users = self._by_doc.get(doc_id)
            if users is not None:
                users.discard(user_id)
                if not users:
                    del self._by_doc[doc_id]
            return True

    # ----------------------------------------------------------- set_default
    def set_default(self, doc_id: str, layout: ViewLayout) -> None:
        """Store a default layout for ``doc_id`` (used by :meth:`resolve`)."""
        with self._lock:
            self._defaults[doc_id] = layout

    def get_default(self, doc_id: str) -> Optional[ViewLayout]:
        with self._lock:
            return self._defaults.get(doc_id)

    # ---------------------------------------------------------------- resolve
    def resolve(self, user_id: str, doc_id: str) -> Optional[ViewLayout]:
        """User-specific layout if present, else default, else ``None``."""
        with self._lock:
            layout = self._layouts.get((user_id, doc_id))
            if layout is not None:
                return layout
            return self._defaults.get(doc_id)

    # ------------------------------------------------------------- listings
    def layouts_for_user(self, user_id: str) -> list:
        with self._lock:
            doc_ids = sorted(self._by_user.get(user_id, set()))
            return [self._layouts[(user_id, d)] for d in doc_ids]

    def layouts_for_doc(self, doc_id: str) -> list:
        with self._lock:
            user_ids = sorted(self._by_doc.get(doc_id, set()))
            return [self._layouts[(u, doc_id)] for u in user_ids]

    # ------------------------------------------------------------- mutations
    def update_theme(
        self,
        user_id: str,
        doc_id: str,
        theme: str,
        now: Optional[float] = None,
    ) -> bool:
        ts = time.time() if now is None else now
        with self._lock:
            layout = self._layouts.get((user_id, doc_id))
            if layout is None:
                return False
            layout.theme = theme
            layout.updated_at = ts
            return True

    def add_panel(
        self,
        user_id: str,
        doc_id: str,
        panel: str,
        now: Optional[float] = None,
    ) -> bool:
        """Append ``panel`` if not already present.

        Returns ``True`` if newly added; ``False`` if duplicate or layout missing.
        """
        ts = time.time() if now is None else now
        with self._lock:
            layout = self._layouts.get((user_id, doc_id))
            if layout is None:
                return False
            if panel in layout.panels:
                return False
            layout.panels.append(panel)
            layout.updated_at = ts
            return True

    def remove_panel(
        self,
        user_id: str,
        doc_id: str,
        panel: str,
        now: Optional[float] = None,
    ) -> bool:
        ts = time.time() if now is None else now
        with self._lock:
            layout = self._layouts.get((user_id, doc_id))
            if layout is None:
                return False
            if panel not in layout.panels:
                return False
            layout.panels.remove(panel)
            layout.updated_at = ts
            return True

    def set_column_width(
        self,
        user_id: str,
        doc_id: str,
        column: str,
        width: float,
        now: Optional[float] = None,
    ) -> bool:
        ts = time.time() if now is None else now
        with self._lock:
            layout = self._layouts.get((user_id, doc_id))
            if layout is None:
                return False
            layout.column_widths[column] = width
            layout.updated_at = ts
            return True

    # ----------------------------------------------------------------- clear
    def clear_user(self, user_id: str) -> int:
        with self._lock:
            doc_ids = list(self._by_user.get(user_id, set()))
            count = 0
            for d in doc_ids:
                key = (user_id, d)
                if key in self._layouts:
                    del self._layouts[key]
                    count += 1
                users = self._by_doc.get(d)
                if users is not None:
                    users.discard(user_id)
                    if not users:
                        del self._by_doc[d]
            if user_id in self._by_user:
                del self._by_user[user_id]
            return count

    def clear_doc(self, doc_id: str) -> int:
        with self._lock:
            user_ids = list(self._by_doc.get(doc_id, set()))
            count = 0
            for u in user_ids:
                key = (u, doc_id)
                if key in self._layouts:
                    del self._layouts[key]
                    count += 1
                docs = self._by_user.get(u)
                if docs is not None:
                    docs.discard(doc_id)
                    if not docs:
                        del self._by_user[u]
            if doc_id in self._by_doc:
                del self._by_doc[doc_id]
            if doc_id in self._defaults:
                del self._defaults[doc_id]
            return count

    # ----------------------------------------------------------------- stats
    def stats(self) -> ViewLayoutStats:
        with self._lock:
            users = {uid for (uid, _did) in self._layouts.keys()}
            docs = {did for (_uid, did) in self._layouts.keys()}
            return ViewLayoutStats(
                total_layouts=len(self._layouts),
                unique_users=len(users),
                unique_docs=len(docs),
            )
