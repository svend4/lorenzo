"""E288 DocTagManager — tag management for documents.

Add, remove, and query tags per document with support for tag aliases and
tag hierarchies.  Pure stdlib, thread-safe.

Public API
----------
:class:`TagInfo`          — metadata about a single tag (doc_count, aliases, parent)
:class:`DocTags`          — tags associated with a document (sorted list + count)
:class:`TagManagerStats`  — aggregate statistics (unique tags, docs, assignments)
:class:`DocTagManager`    — main interface for tag CRUD and querying
"""

from docstoolkit.doc_tag_manager.manager import (
    DocTagManager,
    DocTags,
    TagInfo,
    TagManagerStats,
)

__all__ = [
    "DocTagManager",
    "DocTags",
    "TagInfo",
    "TagManagerStats",
]
