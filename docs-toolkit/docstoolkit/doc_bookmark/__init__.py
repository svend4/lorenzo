"""Doc bookmark module — bookmark manager for documents.

Provides per-user lists, folders, tags, ordering and visit tracking.
"""
from docstoolkit.doc_bookmark.bookmark import (
    Bookmark,
    DocBookmark,
    Folder,
    UserBookmarkStats,
)

__all__ = [
    "Bookmark",
    "DocBookmark",
    "Folder",
    "UserBookmarkStats",
]
