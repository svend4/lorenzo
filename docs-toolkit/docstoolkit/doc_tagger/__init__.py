"""E175 Doc tagger — auto-tag documents using keyword/regex rules.

Public API
----------
:class:`TagRule`        — rule defining a tag with keywords/patterns
:class:`TaggingResult`  — result of tagging a single document
:class:`TaggerConfig`   — configuration for DocTagger
:class:`DocTagger`      — rule-based document tagger
"""
from .tagger import DocTagger, TaggerConfig, TagRule, TaggingResult

__all__ = [
    "DocTagger",
    "TaggerConfig",
    "TagRule",
    "TaggingResult",
]
