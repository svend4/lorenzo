"""WorkflowEngine for sequential, dependency-aware step execution."""
import uuid
from dataclasses import dataclass, field

from docstoolkit.workflow.step import (
    StepResult, StepStatus, WorkflowStep,
)


@dataclass
class WorkflowConfig:
    """Configuration for WorkflowEngine behaviour."""
    stop_on_failure: bool = True
    max_retries: int = 0
    timeout_ms: float = 0  # 0 = no timeout


@dataclass
class WorkflowResult:
    """Result of a full workflow run."""
    workflow_id: str
    steps: list = field(default_factory=list)
    context: dict = field(default_factory=dict)
    success: bool = True

    def failed_steps(self) -> list:
        return [s for s in self.steps if s.status == StepStatus.FAILED]

    def succeeded_steps(self) -> list:
        return [s for s in self.steps if s.status == StepStatus.SUCCESS]

    def total_duration_ms(self) -> float:
        return sum(s.duration_ms for s in self.steps)


class WorkflowEngine:
    """Executes WorkflowSteps sequentially, respecting dependencies."""

    def __init__(self, config: WorkflowConfig = None):
        self._config = config or WorkflowConfig()
        self._steps: list[WorkflowStep] = []

    def add_step(self, step: WorkflowStep) -> None:
        self._steps.append(step)

    def step_count(self) -> int:
        return len(self._steps)

    def run(self, initial_context: dict = None) -> WorkflowResult:
        """Execute all steps in order, honouring dependencies.

        Context is accumulated across steps: each step's output dict is
        merged into the shared context dict after a successful execution.
        """
        context = dict(initial_context or {})
        workflow_id = uuid.uuid4().hex[:8]
        result = WorkflowResult(workflow_id=workflow_id, context=context)

        # Build a quick lookup: name → step
        step_by_name: dict[str, WorkflowStep] = {s.name: s for s in self._steps}
        # Track which step names have succeeded so far
        succeeded_names: set[str] = set()

        # Determine execution order: topological sort respecting dependencies.
        ordered = self._topo_order()

        failed = False  # a non-skipped failure occurred
        skipped_names: set[str] = set()

        for step in ordered:
            # Check dependencies: if any required dep failed or was skipped,
            # skip this step too.
            if self._deps_unmet(step, succeeded_names, skipped_names):
                result.steps.append(StepResult(
                    step_id=step.step_id,
                    status=StepStatus.SKIPPED,
                    output={},
                    error="dependency not satisfied",
                ))
                skipped_names.add(step.name)
                continue

            # If a hard failure already occurred and stop_on_failure is set,
            # skip remaining steps.
            if failed and self._config.stop_on_failure:
                result.steps.append(StepResult(
                    step_id=step.step_id,
                    status=StepStatus.SKIPPED,
                    output={},
                    error="upstream failure",
                ))
                skipped_names.add(step.name)
                continue

            # Execute with retries.
            max_attempts = 1 + max(self._config.max_retries, step.retry_count)
            step_result = None
            for attempt in range(max_attempts):
                step_result = step.execute(context)
                if step_result.is_success():
                    break
                # on final attempt, stop retrying
            # step_result is the last attempt's result

            result.steps.append(step_result)

            if step_result.is_success():
                succeeded_names.add(step.name)
                # Merge step output into shared context
                context.update(step_result.output)
            else:
                if step.skip_on_failure:
                    # Treat as skipped — don't propagate hard failure
                    step_result.status = StepStatus.SKIPPED
                    skipped_names.add(step.name)
                else:
                    failed = True
                    result.success = False

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _topo_order(self) -> list[WorkflowStep]:
        """Return steps in an order that respects declared dependencies.

        Steps with no dependencies come first; among peers the insertion
        order is preserved.  Circular dependencies fall back to insertion
        order (no cycle detection needed for the simple sequential case).
        """
        placed: set[str] = set()
        ordered: list[WorkflowStep] = []
        remaining = list(self._steps)

        # Simple iterative placement: keep looping until all placed or stuck.
        max_passes = len(remaining) + 1
        for _ in range(max_passes):
            if not remaining:
                break
            progress = False
            still_remaining = []
            for step in remaining:
                if all(dep in placed for dep in step.dependencies):
                    ordered.append(step)
                    placed.add(step.name)
                    progress = True
                else:
                    still_remaining.append(step)
            remaining = still_remaining
            if not progress:
                # Circular or missing deps — append whatever is left as-is
                ordered.extend(remaining)
                break

        return ordered

    def _deps_unmet(
        self,
        step: WorkflowStep,
        succeeded: set[str],
        skipped: set[str],
    ) -> bool:
        """True if any declared dependency hasn't succeeded."""
        for dep in step.dependencies:
            if dep not in succeeded:
                return True
        return False
