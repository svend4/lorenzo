"""E320 DocApprovalChain — multi-step document approval workflow.

Public API
----------
:class:`ApprovalStep`    — a single step in an approval chain
:class:`ApprovalChain`   — a complete approval workflow for a document
:class:`ChainStats`      — aggregate statistics
:class:`DocApprovalChain` — main interface for approval chain management
"""

from .chain import ApprovalStep, ApprovalChain, ChainStats, DocApprovalChain

__all__ = ["ApprovalStep", "ApprovalChain", "ChainStats", "DocApprovalChain"]
