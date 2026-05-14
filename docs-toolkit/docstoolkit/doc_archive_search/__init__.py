"""E254 Document archive search — full-text search over compressed archives.

Public API
----------
:class:`ArchiveEntry`     — single compressed archive entry
:class:`SearchMatch`      — a match in a document with score and excerpts
:class:`SearchOptions`    — knobs for search behaviour
:class:`DocArchiveSearch` — main archive + search class
"""
from docstoolkit.doc_archive_search.archive_search import (
    ArchiveEntry,
    DocArchiveSearch,
    SearchMatch,
    SearchOptions,
)

__all__ = [
    "ArchiveEntry",
    "DocArchiveSearch",
    "SearchMatch",
    "SearchOptions",
]
