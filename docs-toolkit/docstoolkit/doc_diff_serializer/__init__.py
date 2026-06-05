"""E413 DocDiffSerializer — serialize and parse document diff payloads.

Public API
----------
:class:`DiffOp`             — a single diff operation
:class:`SerializedDiff`     — a complete serialized diff
:class:`SerializerStats`    — aggregate statistics
:class:`DocDiffSerializer`  — main interface for diff serialization
"""

from .serializer import DiffOp, SerializedDiff, SerializerStats, DocDiffSerializer

__all__ = ["DiffOp", "SerializedDiff", "SerializerStats", "DocDiffSerializer"]
