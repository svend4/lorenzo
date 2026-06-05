"""High-level document repository with CRUD, tagging, query, and stats (E157)."""

from docstoolkit.doc_repository.repository import (
    DocRepository,
    RepoConfig,
    RepoDocument,
    RepoStats,
)

__all__ = ["DocRepository", "RepoConfig", "RepoDocument", "RepoStats"]
