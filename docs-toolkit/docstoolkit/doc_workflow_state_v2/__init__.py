"""E409 DocWorkflowStateV2 — enhanced state machine with guards and history.

Public API
----------
:class:`StateGuard`         — a condition that must pass for transition
:class:`Transition`         — a state transition with guards
:class:`StateRecord`        — current state record
:class:`WorkflowStatsV2`    — aggregate statistics
:class:`DocWorkflowStateV2` — main interface for workflow state v2
"""

from .state import StateGuard, Transition, StateRecord, WorkflowStatsV2, DocWorkflowStateV2

__all__ = ["StateGuard", "Transition", "StateRecord", "WorkflowStatsV2", "DocWorkflowStateV2"]
