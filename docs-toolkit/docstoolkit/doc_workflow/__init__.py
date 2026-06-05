"""Document workflow module for docs-toolkit (E192).

Provides a state-machine-style document workflow with statuses, transitions,
role-based access control, and approval chains. Tailored for documents that
move through stages like draft -> review -> approved -> published.

Quick start::

    from docstoolkit.doc_workflow import (
        DocWorkflow, WorkflowDefinition, WorkflowStatus,
    )

    definition = WorkflowDefinition("article")
    definition.add_transition(
        WorkflowStatus.DRAFT, WorkflowStatus.REVIEW
    )
    definition.add_transition(
        WorkflowStatus.REVIEW, WorkflowStatus.APPROVED,
        required_role="editor",
    )
    definition.add_transition(
        WorkflowStatus.APPROVED, WorkflowStatus.PUBLISHED,
        required_role="publisher",
    )

    wf = DocWorkflow(definition)
    wf.register("doc-1")
    wf.transition("doc-1", WorkflowStatus.REVIEW, actor="alice")
    wf.transition(
        "doc-1", WorkflowStatus.APPROVED,
        actor="bob", user_role="editor",
    )
"""
from docstoolkit.doc_workflow.workflow import (
    WorkflowStatus,
    Transition,
    DocState,
    TransitionResult,
    WorkflowDefinition,
    DocWorkflow,
)

__all__ = [
    "WorkflowStatus",
    "Transition",
    "DocState",
    "TransitionResult",
    "WorkflowDefinition",
    "DocWorkflow",
]
