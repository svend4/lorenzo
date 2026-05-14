"""E323 DocWorkflowState — state machine for document workflow status.

Public API
----------
:class:`StateTransition`   — a defined transition from one state to another
:class:`StateRecord`       — current state record for a document
:class:`WorkflowStats`     — aggregate statistics
:class:`DocWorkflowState`  — main interface for workflow state management
"""

from .state import StateTransition, StateRecord, WorkflowStats, DocWorkflowState

__all__ = ["StateTransition", "StateRecord", "WorkflowStats", "DocWorkflowState"]
