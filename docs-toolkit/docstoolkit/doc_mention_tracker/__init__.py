"""E292 DocMentionTracker — track @mentions and cross-references between documents.

Parses and stores @user mentions, [[doc]] cross-references, and #tag mentions
across a document corpus.  Pure stdlib, thread-safe.

Public API
----------
:class:`Mention`         — a single recorded mention
:class:`MentionStats`    — aggregate statistics (counts by type, unique targets/sources)
:class:`DocMentionTracker` — main interface for recording and querying mentions
"""

from docstoolkit.doc_mention_tracker.tracker import (
    DocMentionTracker,
    Mention,
    MentionStats,
)

__all__ = [
    "DocMentionTracker",
    "Mention",
    "MentionStats",
]
