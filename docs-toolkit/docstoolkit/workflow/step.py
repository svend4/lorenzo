"""WorkflowStep and StepResult for the E48 Workflow engine."""
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StepResult:
    """Result of a single workflow step execution."""
    step_id: str
    status: StepStatus
    output: dict
    error: str = ""
    duration_ms: float = 0.0

    def is_success(self) -> bool:
        return self.status == StepStatus.SUCCESS


@dataclass
class WorkflowStep:
    """A single step in a workflow pipeline."""
    name: str
    handler: Callable
    step_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    retry_count: int = 0
    skip_on_failure: bool = False
    dependencies: list = field(default_factory=list)

    def execute(self, context: dict) -> StepResult:
        """Call handler(context), catch exceptions, track duration."""
        t0 = time.monotonic()
        try:
            output = self.handler(context)
            duration_ms = (time.monotonic() - t0) * 1000.0
            if not isinstance(output, dict):
                output = {"result": output}
            return StepResult(
                step_id=self.step_id,
                status=StepStatus.SUCCESS,
                output=output,
                duration_ms=duration_ms,
            )
        except Exception as exc:
            duration_ms = (time.monotonic() - t0) * 1000.0
            return StepResult(
                step_id=self.step_id,
                status=StepStatus.FAILED,
                output={},
                error=f"{type(exc).__name__}: {exc}",
                duration_ms=duration_ms,
            )
