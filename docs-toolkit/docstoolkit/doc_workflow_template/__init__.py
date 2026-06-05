"""E350 DocWorkflowTemplate — reusable workflow templates for documents.

Public API
----------
:class:`WorkflowStep`        — a single step in a workflow template
:class:`WorkflowTemplate`    — a named workflow template
:class:`TemplateStats`       — aggregate statistics
:class:`DocWorkflowTemplate` — main interface for template management
"""

from .template import WorkflowStep, WorkflowTemplate, TemplateStats, DocWorkflowTemplate

__all__ = ["WorkflowStep", "WorkflowTemplate", "TemplateStats", "DocWorkflowTemplate"]
