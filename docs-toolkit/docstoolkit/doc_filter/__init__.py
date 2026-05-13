"""E150 Document filter — filters collections of documents by metadata, content, or computed predicates.

Public API
----------
:class:`FilterOp`         — enum of filter operators
:class:`FilterCondition`  — single filter condition (field/op/value)
:class:`Document`         — document dataclass with id/content/metadata
:class:`FilterResult`     — result of a filter operation
:class:`DocFilter`        — main filter engine
"""
from .filter import (
    DocFilter,
    Document,
    FilterCondition,
    FilterOp,
    FilterResult,
)

__all__ = [
    "DocFilter",
    "Document",
    "FilterCondition",
    "FilterOp",
    "FilterResult",
]
