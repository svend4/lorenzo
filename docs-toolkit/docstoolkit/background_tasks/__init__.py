"""Background tasks module — E78.

Provides a thread-pool backed executor for fire-and-forget background
work, with per-task state tracking, timeouts, cancellation, and priority.

Quick start::

    from docstoolkit.background_tasks import (
        TaskState, TaskPriority, Task,
        ExecutorConfig, BackgroundExecutor,
    )

    executor = BackgroundExecutor()

    task_id = executor.submit_fn(my_func, arg1, arg2, timeout=10.0)
    task = executor.wait(task_id)

    print(task.state)   # TaskState.SUCCESS
    print(task.result)  # return value of my_func
    executor.shutdown()
"""
from docstoolkit.background_tasks.task import Task, TaskPriority, TaskState
from docstoolkit.background_tasks.executor import BackgroundExecutor, ExecutorConfig

__all__ = [
    # task
    "TaskState",
    "TaskPriority",
    "Task",
    # executor
    "ExecutorConfig",
    "BackgroundExecutor",
]
