"""doc_versioning_v2 — in-memory document version history with branching and tagging.

Adds to the original ``doc_versioning`` module:

* SQLite-backed storage (in-memory by default, file-backed optional).
* Branches, tags and rollback as new commits.
* Unified diff between any two versions.
"""
from .store import (
    Branch,
    DocVersion,
    Tag,
    VersionStore,
)

__all__ = [
    "Branch",
    "DocVersion",
    "Tag",
    "VersionStore",
]
