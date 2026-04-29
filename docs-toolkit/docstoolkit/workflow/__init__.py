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
"""
from docstoolkit.workflow.dag import (
    Workflow, Step, StepResult, WorkflowResult, run, run_async,
)

__all__ = [
    "Workflow", "Step", "StepResult", "WorkflowResult",
    "run", "run_async",
]
