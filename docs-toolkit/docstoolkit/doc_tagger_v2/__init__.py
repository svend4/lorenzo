"""E208 doc_tagger_v2 — advanced tagger with hierarchies, aliases, and feedback.

Public API
----------
:class:`TagDefinition`   — tag definition with parent, aliases, keywords
:class:`TagSuggestion`   — suggested tag with confidence and source
:class:`TaggingFeedback` — feedback record for a tag suggestion
:class:`DocTaggerV2`     — advanced tagger
"""
from .tagger import (
    DocTaggerV2,
    TagDefinition,
    TaggingFeedback,
    TagSuggestion,
)

__all__ = [
    "DocTaggerV2",
    "TagDefinition",
    "TagSuggestion",
    "TaggingFeedback",
]
