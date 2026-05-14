"""E308 DocCommentStore — threaded comment storage for documents.

Public API
----------
:class:`Comment`         — a single comment (top-level or reply)
:class:`CommentThread`   — a top-level comment with its replies
:class:`CommentStats`    — aggregate statistics
:class:`DocCommentStore` — main interface for comment CRUD
"""

from .store import Comment, CommentThread, CommentStats, DocCommentStore

__all__ = ["Comment", "CommentThread", "CommentStats", "DocCommentStore"]
