"""E345 DocQualityScore — per-document quality dimension scoring.

Public API
----------
:class:`Dimension`        — a quality dimension definition
:class:`DimensionScore`   — a single dimension's score for a document
:class:`QualityReport`    — aggregate scores for a document
:class:`QualityStats`     — global statistics
:class:`DocQualityScore`  — main interface for quality scoring
"""

from .score import Dimension, DimensionScore, QualityReport, QualityStats, DocQualityScore

__all__ = ["Dimension", "DimensionScore", "QualityReport", "QualityStats", "DocQualityScore"]
