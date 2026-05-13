"""E193 Document inbox filter — declarative rules engine with conditions and actions.

Public API
----------
:class:`Operator`        — comparison operators for conditions
:class:`ActionType`      — action types applied when rules match
:class:`Condition`       — single condition (field/operator/value)
:class:`Action`          — action specification (type + args)
:class:`FilterRule`      — rule (conditions + actions + match_mode + priority)
:class:`MatchResult`     — result of evaluating a single document
:class:`DocInboxFilter`  — main rules engine
"""
from .filter import (
    Action,
    ActionType,
    Condition,
    DocInboxFilter,
    FilterRule,
    MatchResult,
    Operator,
)

__all__ = [
    "Action",
    "ActionType",
    "Condition",
    "DocInboxFilter",
    "FilterRule",
    "MatchResult",
    "Operator",
]
