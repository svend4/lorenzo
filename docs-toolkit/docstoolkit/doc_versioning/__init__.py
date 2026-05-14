"""Semantic versioning for documentation files.

Public API
----------
version
    ChangeType, DocVersion

detector
    ChangeDetector

history
    VersionRecord, VersionHistory
"""
from docstoolkit.doc_versioning.version import ChangeType, DocVersion
from docstoolkit.doc_versioning.detector import ChangeDetector
from docstoolkit.doc_versioning.history import VersionRecord, VersionHistory

__all__ = [
    "ChangeType",
    "DocVersion",
    "ChangeDetector",
    "VersionRecord",
    "VersionHistory",
]
