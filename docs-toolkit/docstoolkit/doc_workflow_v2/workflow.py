"""Document workflow v2 implementation (E265).

Advanced workflow with parallel branches, conditional transitions, and
timeout handling for individual steps.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class StepStatus(Enum):
    """All possible step statuses."""

    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


class WorkflowStatus(Enum):
    """All possible workflow statuses."""

    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class StepDef:
    """Declarative definition of a workflow step."""

    step_id: str
    name: str
    condition: Optional[Callable[[dict], bool]] = None
    timeout_seconds: Optional[float] = None
    parallel_with: List[str] = field(default_factory=list)


@dataclass
class StepInstance:
    """Runtime state for a single step within a workflow instance."""

    step_id: str
    status: StepStatus
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Any = None
    error: Optional[str] = None


@dataclass
class WorkflowInstance:
    """Runtime state for a workflow tracking one document."""

    instance_id: str
    doc_id: str
    status: WorkflowStatus
    context: dict = field(default_factory=dict)
    steps: Dict[str, StepInstance] = field(default_factory=dict)
    started_at: float = 0.0
    completed_at: Optional[float] = None


class WorkflowDefinitionV2:
    """Declarative workflow with steps, transitions, and parallel groups."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._steps: Dict[str, StepDef] = {}
        self._order: List[str] = []
        self._transitions: List[tuple] = []  # (from_step, to_step)

    def add_step(
        self,
        step_id: str,
        name: str,
        condition: Optional[Callable[[dict], bool]] = None,
        timeout_seconds: Optional[float] = None,
        parallel_with: Optional[List[str]] = None,
    ) -> StepDef:
        """Register a step and return its descriptor."""
        step = StepDef(
            step_id=step_id,
            name=name,
            condition=condition,
            timeout_seconds=timeout_seconds,
            parallel_with=list(parallel_with) if parallel_with else [],
        )
        if step_id not in self._steps:
            self._order.append(step_id)
        self._steps[step_id] = step
        return step

    def add_transition(self, from_step: str, to_step: str) -> bool:
        """Register a transition between two steps. Returns ``True`` on success."""
        if from_step not in self._steps or to_step not in self._steps:
            return False
        if (from_step, to_step) in self._transitions:
            return False
        self._transitions.append((from_step, to_step))
        return True

    def steps(self) -> List[StepDef]:
        """Return all registered steps in insertion order."""
        return [self._steps[sid] for sid in self._order]

    def get_step(self, step_id: str) -> Optional[StepDef]:
        """Return a step by id or ``None``."""
        return self._steps.get(step_id)

    def next_steps(self, step_id: str) -> List[str]:
        """Return successor step_ids reachable via a single transition."""
        return [
            to_s for (from_s, to_s) in self._transitions if from_s == step_id
        ]

    def previous_steps(self, step_id: str) -> List[str]:
        """Return predecessor step_ids."""
        return [
            from_s
            for (from_s, to_s) in self._transitions
            if to_s == step_id
        ]

    def initial_steps(self) -> List[str]:
        """Step ids with no incoming transitions."""
        targets = {to_s for (_, to_s) in self._transitions}
        return [sid for sid in self._order if sid not in targets]

    def parallel_groups(self) -> List[Set[str]]:
        """Connected components by ``parallel_with`` (union-find)."""
        parent: Dict[str, str] = {sid: sid for sid in self._steps}

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: str, b: str) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for sid, step in self._steps.items():
            for other in step.parallel_with:
                if other in self._steps:
                    union(sid, other)

        groups: Dict[str, Set[str]] = {}
        for sid in self._steps:
            root = find(sid)
            groups.setdefault(root, set()).add(sid)

        # Only return groups with >1 member (real parallel groups)
        return [g for g in groups.values() if len(g) > 1]


class DocWorkflowV2:
    """Runtime engine tracking workflow instances per document."""

    def __init__(self, definition: WorkflowDefinitionV2) -> None:
        self.definition = definition
        self._instances: Dict[str, WorkflowInstance] = {}
        self._lock = threading.Lock()

    # ---- internal helpers (must be called with lock held) ----

    def _now(self, now: Optional[float]) -> float:
        return time.time() if now is None else now

    def _parallel_group_for(self, step_id: str) -> Set[str]:
        """Return all step_ids in the same parallel group as ``step_id``."""
        for group in self.definition.parallel_groups():
            if step_id in group:
                return group
        return {step_id}

    def _activate_step(
        self,
        instance: WorkflowInstance,
        step_id: str,
        now: float,
    ) -> None:
        """Activate a step (or skip if its condition is False)."""
        if step_id not in instance.steps:
            return
        step_inst = instance.steps[step_id]
        if step_inst.status != StepStatus.PENDING:
            return

        step_def = self.definition.get_step(step_id)
        if step_def is None:
            return

        # Conditional skip
        if step_def.condition is not None:
            try:
                ok = bool(step_def.condition(instance.context))
            except Exception:
                ok = False
            if not ok:
                step_inst.status = StepStatus.SKIPPED
                step_inst.started_at = now
                step_inst.completed_at = now
                # Cascade to successors
                self._advance_from(instance, step_id, now)
                return

        step_inst.status = StepStatus.ACTIVE
        step_inst.started_at = now

    def _activate_with_parallels(
        self,
        instance: WorkflowInstance,
        step_id: str,
        now: float,
    ) -> None:
        """Activate a step alongside its parallel group members."""
        group = self._parallel_group_for(step_id)
        for sid in group:
            self._activate_step(instance, sid, now)

    def _advance_from(
        self,
        instance: WorkflowInstance,
        step_id: str,
        now: float,
    ) -> None:
        """Activate successors of ``step_id`` (after it completed/skipped)."""
        for next_id in self.definition.next_steps(step_id):
            self._activate_with_parallels(instance, next_id, now)
        self._maybe_finalize(instance, now)

    def _maybe_finalize(
        self,
        instance: WorkflowInstance,
        now: float,
    ) -> None:
        """Move workflow to COMPLETED/FAILED if appropriate."""
        if instance.status != WorkflowStatus.ACTIVE:
            return

        statuses = [s.status for s in instance.steps.values()]
        if any(
            s in (StepStatus.FAILED, StepStatus.TIMED_OUT) for s in statuses
        ):
            instance.status = WorkflowStatus.FAILED
            instance.completed_at = now
            return

        if all(
            s in (StepStatus.COMPLETED, StepStatus.SKIPPED) for s in statuses
        ):
            instance.status = WorkflowStatus.COMPLETED
            instance.completed_at = now

    # ---- public API ----

    def start(
        self,
        doc_id: str,
        context: Optional[dict] = None,
        now: float = 0.0,
    ) -> WorkflowInstance:
        """Create a new workflow instance and activate initial step(s)."""
        with self._lock:
            instance_id = uuid.uuid4().hex
            instance = WorkflowInstance(
                instance_id=instance_id,
                doc_id=doc_id,
                status=WorkflowStatus.ACTIVE,
                context=dict(context) if context else {},
                started_at=now,
            )
            for step_def in self.definition.steps():
                instance.steps[step_def.step_id] = StepInstance(
                    step_id=step_def.step_id,
                    status=StepStatus.PENDING,
                )

            self._instances[instance_id] = instance

            initial = self.definition.initial_steps()
            for sid in initial:
                self._activate_with_parallels(instance, sid, now)
            self._maybe_finalize(instance, now)
            return instance

    def complete_step(
        self,
        instance_id: str,
        step_id: str,
        result: Any = None,
        now: Optional[float] = None,
    ) -> bool:
        """Mark a step as COMPLETED and advance to successors."""
        with self._lock:
            instance = self._instances.get(instance_id)
            if instance is None:
                return False
            if instance.status != WorkflowStatus.ACTIVE:
                return False
            step_inst = instance.steps.get(step_id)
            if step_inst is None:
                return False
            if step_inst.status != StepStatus.ACTIVE:
                return False
            t = self._now(now)
            step_inst.status = StepStatus.COMPLETED
            step_inst.completed_at = t
            step_inst.result = result
            self._advance_from(instance, step_id, t)
            return True

    def fail_step(
        self,
        instance_id: str,
        step_id: str,
        error: Optional[str] = None,
        now: Optional[float] = None,
    ) -> bool:
        """Mark a step as FAILED. Workflow becomes FAILED."""
        with self._lock:
            instance = self._instances.get(instance_id)
            if instance is None:
                return False
            if instance.status != WorkflowStatus.ACTIVE:
                return False
            step_inst = instance.steps.get(step_id)
            if step_inst is None:
                return False
            if step_inst.status != StepStatus.ACTIVE:
                return False
            t = self._now(now)
            step_inst.status = StepStatus.FAILED
            step_inst.completed_at = t
            step_inst.error = error
            self._maybe_finalize(instance, t)
            return True

    def skip_step(
        self,
        instance_id: str,
        step_id: str,
        now: Optional[float] = None,
    ) -> bool:
        """Mark a step as SKIPPED and advance to successors."""
        with self._lock:
            instance = self._instances.get(instance_id)
            if instance is None:
                return False
            if instance.status != WorkflowStatus.ACTIVE:
                return False
            step_inst = instance.steps.get(step_id)
            if step_inst is None:
                return False
            if step_inst.status not in (StepStatus.ACTIVE, StepStatus.PENDING):
                return False
            t = self._now(now)
            if step_inst.started_at is None:
                step_inst.started_at = t
            step_inst.status = StepStatus.SKIPPED
            step_inst.completed_at = t
            self._advance_from(instance, step_id, t)
            return True

    def cancel(
        self,
        instance_id: str,
        now: Optional[float] = None,
    ) -> bool:
        """Cancel an active workflow instance."""
        with self._lock:
            instance = self._instances.get(instance_id)
            if instance is None:
                return False
            if instance.status != WorkflowStatus.ACTIVE:
                return False
            instance.status = WorkflowStatus.CANCELLED
            instance.completed_at = self._now(now)
            return True

    def active_steps(self, instance_id: str) -> List[StepInstance]:
        """List ACTIVE step instances for a workflow."""
        with self._lock:
            instance = self._instances.get(instance_id)
            if instance is None:
                return []
            return [
                s for s in instance.steps.values()
                if s.status == StepStatus.ACTIVE
            ]

    def pending_steps(self, instance_id: str) -> List[StepInstance]:
        """List PENDING step instances for a workflow."""
        with self._lock:
            instance = self._instances.get(instance_id)
            if instance is None:
                return []
            return [
                s for s in instance.steps.values()
                if s.status == StepStatus.PENDING
            ]

    def check_timeouts(self, now: Optional[float] = None) -> int:
        """Mark active steps past their deadline as TIMED_OUT.

        Returns the number of steps newly timed out.
        """
        with self._lock:
            t = self._now(now)
            n = 0
            for instance in self._instances.values():
                if instance.status != WorkflowStatus.ACTIVE:
                    continue
                for step_inst in instance.steps.values():
                    if step_inst.status != StepStatus.ACTIVE:
                        continue
                    step_def = self.definition.get_step(step_inst.step_id)
                    if step_def is None or step_def.timeout_seconds is None:
                        continue
                    if step_inst.started_at is None:
                        continue
                    deadline = step_inst.started_at + step_def.timeout_seconds
                    if deadline < t:
                        step_inst.status = StepStatus.TIMED_OUT
                        step_inst.completed_at = t
                        n += 1
                self._maybe_finalize(instance, t)
            return n

    def get_instance(self, instance_id: str) -> Optional[WorkflowInstance]:
        """Fetch a workflow instance by id, or ``None`` if unknown."""
        with self._lock:
            return self._instances.get(instance_id)

    def instances_for_doc(self, doc_id: str) -> List[WorkflowInstance]:
        """List workflow instances tracking the given document."""
        with self._lock:
            return [
                inst for inst in self._instances.values()
                if inst.doc_id == doc_id
            ]

    def active_instances(self) -> List[WorkflowInstance]:
        """List workflow instances still in ACTIVE status."""
        with self._lock:
            return [
                inst for inst in self._instances.values()
                if inst.status == WorkflowStatus.ACTIVE
            ]

    def progress(self, instance_id: str) -> float:
        """Return fraction of steps that are COMPLETED or SKIPPED, 0.0-1.0."""
        with self._lock:
            instance = self._instances.get(instance_id)
            if instance is None:
                return 0.0
            total = len(instance.steps)
            if total == 0:
                return 0.0
            done = sum(
                1 for s in instance.steps.values()
                if s.status in (StepStatus.COMPLETED, StepStatus.SKIPPED)
            )
            return done / total

    @property
    def total_instances(self) -> int:
        """Total number of workflow instances tracked."""
        with self._lock:
            return len(self._instances)

    def clear(self) -> None:
        """Forget every tracked workflow instance."""
        with self._lock:
            self._instances.clear()
