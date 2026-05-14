"""Doc reaction module for docs-toolkit.

Public API
----------
- ``ReactionType``    — enum of reaction kinds
- ``Reaction``        — individual reaction record
- ``ReactionSummary`` — aggregated reaction counts for a document
- ``UserActivity``    — aggregated reaction stats for a user
- ``DocReaction``     — central reaction manager
"""

from docstoolkit.doc_reaction.reaction import (
    ReactionType,
    Reaction,
    ReactionSummary,
    UserActivity,
    DocReaction,
)

__all__ = [
    "ReactionType",
    "Reaction",
    "ReactionSummary",
    "UserActivity",
    "DocReaction",
]
