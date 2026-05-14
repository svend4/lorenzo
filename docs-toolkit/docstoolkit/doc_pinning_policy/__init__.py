"""E365 DocPinningPolicy — policy rules for document pinning.

Public API
----------
:class:`PinPolicyRule`     — a pinning policy rule
:class:`PinPolicyResult`   — result of evaluating policy for a doc
:class:`PinPolicyStats`    — aggregate statistics
:class:`DocPinningPolicy`  — main interface for pinning policy
"""

from .policy import PinPolicyRule, PinPolicyResult, PinPolicyStats, DocPinningPolicy

__all__ = ["PinPolicyRule", "PinPolicyResult", "PinPolicyStats", "DocPinningPolicy"]
