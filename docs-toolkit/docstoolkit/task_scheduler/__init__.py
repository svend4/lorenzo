"""Task scheduler module — E54.

Provides a tick-driven, thread-pool-backed task scheduler with three
scheduling modes: ONCE, INTERVAL, and CRON_LIKE.

Quick start::

    from docstoolkit.task_scheduler import (
        ScheduleType, TaskSchedule,
        TaskStatus, TaskResult, ScheduledTask,
        SchedulerConfig, TaskScheduler,
    )

    scheduler = TaskScheduler()
    task = ScheduledTask(
        name="hello",
        func=lambda: print("hello"),
        schedule=TaskSchedule(schedule_type=ScheduleType.INTERVAL, interval_seconds=5),
    )
    scheduler.add_task(task)

    import time
    while True:
        scheduler.tick()
        time.sleep(0.1)
"""
from docstoolkit.task_scheduler.schedule import ScheduleType, TaskSchedule
from docstoolkit.task_scheduler.task import TaskStatus, TaskResult, ScheduledTask
from docstoolkit.task_scheduler.scheduler import SchedulerConfig, TaskScheduler

__all__ = [
    # schedule
    "ScheduleType",
    "TaskSchedule",
    # task
    "TaskStatus",
    "TaskResult",
    "ScheduledTask",
    # scheduler
    "SchedulerConfig",
    "TaskScheduler",
]
