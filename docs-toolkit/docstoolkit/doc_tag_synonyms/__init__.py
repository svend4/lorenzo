"""E438 DocTagSynonyms — tag synonym groups for normalized search.

Public API
----------
:class:`SynonymGroup`    — a group of synonymous tags
:class:`SynonymStats`    — aggregate statistics
:class:`DocTagSynonyms`  — main interface for tag synonyms
"""

from .synonyms import SynonymGroup, SynonymStats, DocTagSynonyms

__all__ = ["SynonymGroup", "SynonymStats", "DocTagSynonyms"]
