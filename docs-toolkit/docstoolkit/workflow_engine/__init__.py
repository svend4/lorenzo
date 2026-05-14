"""workflow_engine — simple sequential workflow engine (E101).

A workflow is a named sequence of steps. Each step is a Python callable.
The engine executes steps in order, threads outputs through a shared context
dict, supports per-step skip/retry, and records full execution history.

Pure stdlib — no external dependencies.

Usage::

    from docstoolkit.workflow_engine import (
        WorkflowEngine, WorkflowConfig, StepConfig,
        StepStatus, StepResult, WorkflowResult,
    )

    def load(ctx):
        return {"data": [1, 2, 3]}

    def process(ctx):
        data = ctx["_results"]["load"].output["data"]
        return {"total": sum(data)}

    config = WorkflowConfig(
        name="demo",
        steps=[
            StepConfig("load", fn=load),
            StepConfig("process", fn=process),
        ],
    )

    engine = WorkflowEngine()
    result = engine.run(config)
    print(result.success)            # True
    print(result.get("process"))     # StepResult(name="process", ...)
"""

from docstoolkit.workflow_engine.engine import (
    StepStatus,
    StepConfig,
    StepResult,
    WorkflowConfig,
    WorkflowResult,
    WorkflowEngine,
)

__all__ = [
    "StepStatus",
    "StepConfig",
    "StepResult",
    "WorkflowConfig",
    "WorkflowResult",
    "WorkflowEngine",
]
