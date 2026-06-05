"""E444 DocTopicFilter — filter documents by topic membership.

Public API
----------
:class:`TopicMembership`  — doc-to-topic assignment
:class:`FilterStats`      — aggregate statistics
:class:`DocTopicFilter`   — main interface for topic-based filtering
"""

from .filter import TopicMembership, FilterStats, DocTopicFilter

__all__ = ["TopicMembership", "FilterStats", "DocTopicFilter"]
