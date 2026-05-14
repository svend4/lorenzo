"""doc_topic_model (E231) — lightweight topic modeling using TF-IDF and greedy clustering.

Pure stdlib (math, collections, re, threading) — no sklearn, no numpy.

Public API
----------
:class:`Topic`         — a discovered topic with keywords and doc assignments
:class:`TopicDoc`      — assignment of a document to a topic with a score
:class:`TopicModel`    — the fitted model output (topics, assignments, counts)
:class:`DocTopicModel` — main facade for fitting and querying topic models
"""

from .model import (
    DocTopicModel,
    Topic,
    TopicDoc,
    TopicModel,
)

__all__ = [
    "DocTopicModel",
    "Topic",
    "TopicDoc",
    "TopicModel",
]
