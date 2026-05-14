"""Workflow DAG runner: оркестрация многошаговых pipeline'ов.

Использование:
    from docstoolkit.workflow import Workflow, Step, run

    wf = Workflow(name="rag-with-rerank", steps=[
        Step("retrieve", fn=lambda q: search(q, top_k=20),
             inputs={"q": "$.question"}),
        Step("rerank",   fn=lambda passages: rerank(passages, k=5),
             inputs={"passages": "$.retrieve.output"}),
        Step("answer",   fn=lambda q, ps: answer(q, ps),
             inputs={"q": "$.question", "ps": "$.rerank.output"}),
    ])

    result = run(wf, {"question": "что такое RAG?"})
    # result.outputs["answer"] — финальный ответ
    # result.steps — детали каждого шага (input/output/duration/error)

E48 Workflow Engine:
    from docstoolkit.workflow import (
        StepStatus, WorkflowStep, WorkflowConfig, WorkflowEngine,
    )
    # StepResult re-exported from step module (E48 variant)
"""
from docstoolkit.workflow.dag import (
    Workflow, Step, run, run_async,
)
from docstoolkit.workflow.dag import StepResult as DagStepResult
from docstoolkit.workflow.dag import WorkflowResult as DagWorkflowResult
from docstoolkit.workflow.step import StepStatus, StepResult, WorkflowStep
from docstoolkit.workflow.engine import WorkflowConfig, WorkflowResult, WorkflowEngine

__all__ = [
    # Legacy DAG runner
    "Workflow", "Step", "DagStepResult", "DagWorkflowResult",
    "run", "run_async",
    # E48 engine
    "StepStatus", "StepResult", "WorkflowStep",
    "WorkflowConfig", "WorkflowResult", "WorkflowEngine",
]
