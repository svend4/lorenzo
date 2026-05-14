"""Priority-based task scheduler — E99.

Executes tasks in priority order (lower integer = higher priority) using
:class:`queue.PriorityQueue` and :class:`threading.Thread` (stdlib only).

Quick start::

    from docstoolkit.priority_scheduler import PriorityScheduler, TaskStatus

    sched = PriorityScheduler(workers=2)
    sched.start()

    task = sched.submit(lambda x: x ** 2, 7, priority=1)
    print(sched.result(task.task_id))  # 49

    sched.stop()
"""
from docstoolkit.priority_scheduler.scheduler import (
    TaskStatus,
    ScheduledTask,
    PriorityScheduler,
)

__all__ = [
    "TaskStatus",
    "ScheduledTask",
    "PriorityScheduler",
]
