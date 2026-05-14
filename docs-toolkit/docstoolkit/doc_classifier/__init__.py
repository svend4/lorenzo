"""E58 Document classifier — keyword-frequency based, stdlib only.

Public API
----------
:class:`Category`                 — classification category definition
:class:`ClassificationResult`     — result of a single document classification
:class:`ClassifierConfig`         — configuration for DocumentClassifier
:class:`DocumentClassifier`       — keyword-count classifier
:class:`CategoryHierarchy`        — hierarchical category support
"""
from .category import Category, ClassificationResult
from .classifier import ClassifierConfig, DocumentClassifier
from .hierarchy import CategoryHierarchy

__all__ = [
    "Category",
    "ClassificationResult",
    "ClassifierConfig",
    "DocumentClassifier",
    "CategoryHierarchy",
]
