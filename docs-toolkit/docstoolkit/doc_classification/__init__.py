"""E347 DocClassification — document classification taxonomy and assignment.

Public API
----------
:class:`Category`           — a classification category
:class:`Classification`     — a single doc's classification
:class:`ClassificationStats` — aggregate statistics
:class:`DocClassification`  — main interface for classification management
"""

from .classification import Category, Classification, ClassificationStats, DocClassification

__all__ = ["Category", "Classification", "ClassificationStats", "DocClassification"]
