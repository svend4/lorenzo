"""Document workflow v2 module for docs-toolkit (E265).

Advanced document workflows with parallel branches, conditional
transitions, and per-step timeout handling.

Quick start::

    from docstoolkit.doc_workflow_v2 import (
        DocWorkflowV2, WorkflowDefinitionV2, StepStatus, WorkflowStatus,
    )

    definition = WorkflowDefinitionV2("article")
    definition.add_step("draft", "Draft")
    definition.add_step("review_a", "Review A")
    definition.add_step("review_b", "Review B", parallel_with=["review_a"])
    definition.add_step("publish", "Publish")
    definition.add_transition("draft", "review_a")
    definition.add_transition("draft", "review_b")
    definition.add_transition("review_a", "publish")
    definition.add_transition("review_b", "publish")

    wf = DocWorkflowV2(definition)
    instance = wf.start("doc-1", now=0.0)
    wf.complete_step(instance.instance_id, "draft", now=1.0)
"""
from docstoolkit.doc_workflow_v2.workflow import (
    DocWorkflowV2,
    StepDef,
    StepInstance,
    StepStatus,
    WorkflowDefinitionV2,
    WorkflowInstance,
    WorkflowStatus,
)

__all__ = [
    "DocWorkflowV2",
    "StepDef",
    "StepInstance",
    "StepStatus",
    "WorkflowDefinitionV2",
    "WorkflowInstance",
    "WorkflowStatus",
]
