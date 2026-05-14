"""DAG-based task planner with critical path analysis.

Pure stdlib implementation. Provides:

* :class:`TaskStatus` — task lifecycle states.
* :class:`Task` — a unit of work with dependencies and timing data.
* :class:`Plan` — full planning result (topo order + critical path).
* :class:`TaskPlanner` — main façade for building, validating and analysing
  a directed acyclic graph (DAG) of tasks.

Algorithms used:

* Topological sort — Kahn's algorithm (BFS with in-degree).
* Cycle detection — DFS with white/gray/black coloring.
* Critical path — longest path through DAG via topo order + dynamic
  programming over predecessors.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    """Lifecycle status of a single task."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    DONE = "done"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass
class Task:
    """A unit of work that may depend on other tasks."""

    task_id: str
    name: str
    duration: float
    dependencies: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    started_at: float = 0.0
    completed_at: float = 0.0


@dataclass
class Plan:
    """Snapshot of the planner's DAG analysis."""

    tasks: list[Task]
    task_order: list[str]
    critical_path: list[str]
    total_duration: float


class TaskPlanner:
    """Build and analyse a DAG of tasks.

    Tasks are identified by string IDs and may declare ``dependencies`` —
    other task IDs that must reach :attr:`TaskStatus.DONE` first.
    """

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_task(
        self,
        task_id: str,
        name: str,
        duration: float,
        dependencies: Optional[list[str]] = None,
    ) -> Task:
        """Register a new task; duplicate IDs raise :class:`ValueError`."""
        if task_id in self._tasks:
            raise ValueError(f"Task already exists: {task_id}")
        if duration < 0:
            raise ValueError("duration must be non-negative")
        task = Task(
            task_id=task_id,
            name=name,
            duration=float(duration),
            dependencies=list(dependencies or []),
        )
        self._tasks[task_id] = task
        return task

    def remove_task(self, task_id: str) -> bool:
        """Remove a task; fails if any other task depends on it."""
        if task_id not in self._tasks:
            return False
        for other in self._tasks.values():
            if other.task_id == task_id:
                continue
            if task_id in other.dependencies:
                return False
        del self._tasks[task_id]
        return True

    def update_status(
        self,
        task_id: str,
        status: TaskStatus,
        now: float = 0.0,
    ) -> bool:
        """Set the status of a task and record timing transitions."""
        task = self._tasks.get(task_id)
        if task is None:
            return False
        task.status = status
        if status == TaskStatus.RUNNING and task.started_at == 0.0:
            task.started_at = float(now)
        if status in (TaskStatus.DONE, TaskStatus.FAILED):
            task.completed_at = float(now)
        return True

    def mark_done(self, task_id: str, now: float = 0.0) -> bool:
        """Convenience wrapper that marks a task as :attr:`TaskStatus.DONE`."""
        return self.update_status(task_id, TaskStatus.DONE, now=now)

    def clear(self) -> None:
        """Drop all tasks."""
        self._tasks.clear()

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_task(self, task_id: str) -> Optional[Task]:
        """Return a single task or ``None`` if absent."""
        return self._tasks.get(task_id)

    @property
    def task_count(self) -> int:
        """Total number of registered tasks."""
        return len(self._tasks)

    @property
    def complete_count(self) -> int:
        """Number of tasks in :attr:`TaskStatus.DONE`."""
        return sum(1 for t in self._tasks.values() if t.status == TaskStatus.DONE)

    @property
    def progress(self) -> float:
        """Fraction of tasks that are DONE (``0.0`` for an empty plan)."""
        if not self._tasks:
            return 0.0
        return self.complete_count / len(self._tasks)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def ready_tasks(self) -> list[Task]:
        """Tasks whose dependencies are all DONE and are not yet finished."""
        out: list[Task] = []
        for task in self._tasks.values():
            if task.status in (TaskStatus.DONE, TaskStatus.FAILED):
                continue
            deps_ok = True
            for dep_id in task.dependencies:
                dep = self._tasks.get(dep_id)
                if dep is None or dep.status != TaskStatus.DONE:
                    deps_ok = False
                    break
            if deps_ok:
                out.append(task)
        return out

    def blocked_tasks(self) -> list[Task]:
        """Tasks with at least one FAILED dependency (transitively or direct)."""
        out: list[Task] = []
        for task in self._tasks.values():
            for dep_id in task.dependencies:
                dep = self._tasks.get(dep_id)
                if dep is not None and dep.status == TaskStatus.FAILED:
                    out.append(task)
                    break
        return out

    # ------------------------------------------------------------------
    # Graph analysis
    # ------------------------------------------------------------------

    def topological_order(self) -> list[str]:
        """Return task IDs in topological order using Kahn's algorithm.

        Raises :class:`ValueError` if the graph contains a cycle or a
        reference to a missing dependency.
        """
        in_degree: dict[str, int] = {tid: 0 for tid in self._tasks}
        successors: dict[str, list[str]] = {tid: [] for tid in self._tasks}
        for task in self._tasks.values():
            for dep_id in task.dependencies:
                if dep_id not in self._tasks:
                    raise ValueError(
                        f"Task {task.task_id} depends on missing task {dep_id}"
                    )
                successors[dep_id].append(task.task_id)
                in_degree[task.task_id] += 1

        queue: deque[str] = deque(
            sorted(tid for tid, deg in in_degree.items() if deg == 0)
        )
        order: list[str] = []
        while queue:
            tid = queue.popleft()
            order.append(tid)
            for succ in successors[tid]:
                in_degree[succ] -= 1
                if in_degree[succ] == 0:
                    queue.append(succ)

        if len(order) != len(self._tasks):
            raise ValueError("Cycle detected in task graph")
        return order

    def has_cycle(self) -> bool:
        """Detect cycles via DFS with white/gray/black coloring."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = {tid: WHITE for tid in self._tasks}
        # Use successors so DFS proceeds in dependency direction.
        successors: dict[str, list[str]] = {tid: [] for tid in self._tasks}
        for task in self._tasks.values():
            for dep_id in task.dependencies:
                if dep_id in self._tasks:
                    successors[dep_id].append(task.task_id)

        def dfs(node: str) -> bool:
            color[node] = GRAY
            for nxt in successors[node]:
                if color[nxt] == GRAY:
                    return True
                if color[nxt] == WHITE and dfs(nxt):
                    return True
            color[node] = BLACK
            return False

        for tid in self._tasks:
            if color[tid] == WHITE:
                if dfs(tid):
                    return True
        return False

    def critical_path(self) -> list[str]:
        """Longest path through the DAG (by total task duration)."""
        if not self._tasks:
            return []
        order = self.topological_order()
        # dp[tid] = (length, predecessor)
        dp: dict[str, float] = {tid: 0.0 for tid in self._tasks}
        prev: dict[str, Optional[str]] = {tid: None for tid in self._tasks}
        for tid in order:
            task = self._tasks[tid]
            best_len = 0.0
            best_prev: Optional[str] = None
            for dep_id in task.dependencies:
                candidate = dp[dep_id]
                if candidate > best_len or (
                    candidate == best_len and best_prev is None
                ):
                    best_len = candidate
                    best_prev = dep_id
            dp[tid] = best_len + task.duration
            prev[tid] = best_prev

        # Find sink with maximum dp value.  Tie-break: prefer nodes that
        # appear later in topo order (i.e. deeper in the DAG) so that
        # zero-duration chains still yield the full path.
        end_id = order[0]
        best_val = dp[end_id]
        for tid in order:
            if dp[tid] >= best_val:
                best_val = dp[tid]
                end_id = tid

        # Reconstruct path.
        path: list[str] = []
        cur: Optional[str] = end_id
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path

    def total_duration(self) -> float:
        """Length of the critical path."""
        path = self.critical_path()
        return sum(self._tasks[tid].duration for tid in path)

    # ------------------------------------------------------------------
    # Plan & validation
    # ------------------------------------------------------------------

    def plan(self) -> Plan:
        """Build a :class:`Plan` snapshot."""
        order = self.topological_order()
        cp = self.critical_path()
        total = sum(self._tasks[tid].duration for tid in cp)
        return Plan(
            tasks=[self._tasks[tid] for tid in order],
            task_order=order,
            critical_path=cp,
            total_duration=total,
        )

    def validate(self) -> tuple[bool, list[str]]:
        """Check for cycles and missing dependencies.

        Returns ``(ok, errors)`` — ``ok`` is ``True`` iff ``errors`` is empty.
        """
        errors: list[str] = []
        for task in self._tasks.values():
            for dep_id in task.dependencies:
                if dep_id not in self._tasks:
                    errors.append(
                        f"Task {task.task_id} has missing dependency {dep_id}"
                    )
        if self.has_cycle():
            errors.append("Cycle detected in task graph")
        return (len(errors) == 0, errors)
