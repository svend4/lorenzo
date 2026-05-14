"""E392 DocTopicIndex — topic-based document index.

Public API
----------
:class:`Topic`          — a topic definition
:class:`TopicAssignment` — a doc's assignment to a topic
:class:`TopicIndexStats` — aggregate statistics
:class:`DocTopicIndex`  — main interface for topic management
"""

from .index import Topic, TopicAssignment, TopicIndexStats, DocTopicIndex

__all__ = ["Topic", "TopicAssignment", "TopicIndexStats", "DocTopicIndex"]
