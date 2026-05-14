"""E407 DocVersionDiff — compute and store diffs between document versions.

Public API
----------
:class:`VersionContent`   — content of a single version
:class:`DiffSummary`      — summary of differences between two versions
:class:`DocVersionDiff`   — main interface for version diffing
"""

from .diff import VersionContent, DiffSummary, DocVersionDiff

__all__ = ["VersionContent", "DiffSummary", "DocVersionDiff"]
