"""E359 DocChangesetStore — group document changes into reviewable changesets.

Public API
----------
:class:`Changeset`         — a named bundle of document edits
:class:`ChangesetEdit`     — a single edit within a changeset
:class:`ChangesetStats`    — aggregate statistics
:class:`DocChangesetStore` — main interface for changeset management
"""

from .store import Changeset, ChangesetEdit, ChangesetStats, DocChangesetStore

__all__ = ["Changeset", "ChangesetEdit", "ChangesetStats", "DocChangesetStore"]
