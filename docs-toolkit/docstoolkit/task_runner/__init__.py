"""Task runner module — E159.

Runs named tasks (functions) sequentially or in parallel with timing,
retries, condition-guarded execution, and result collection.

Quick start::

    from docstoolkit.task_runner import (
        TaskRunner, TaskDef, TaskResult, RunResult, TaskStatus,
    )

    runner = TaskRunner()
    runner.add_task(TaskDef(name="hello", func=lambda: "world"))
    result = runner.run_sequential()
    assert result.all_success
"""
from docstoolkit.task_runner.runner import (
    RunResult,
    TaskDef,
    TaskResult,
    TaskRunner,
    TaskStatus,
)

__all__ = [
    "TaskStatus",
    "TaskResult",
    "TaskDef",
    "RunResult",
    "TaskRunner",
]
