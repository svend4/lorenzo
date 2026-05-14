"""DocRenderPipeline — staged document rendering pipeline (pure stdlib)."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional


class RenderStage(Enum):
    """Lifecycle stages of a document render.

    Steps are executed in stage order:
    PARSE -> TRANSFORM -> RENDER -> POST_PROCESS.
    """

    PARSE = "parse"
    TRANSFORM = "transform"
    RENDER = "render"
    POST_PROCESS = "post_process"


# Order in which stages execute.  Each stage maps to its index.
_STAGE_ORDER: dict[RenderStage, int] = {
    RenderStage.PARSE: 0,
    RenderStage.TRANSFORM: 1,
    RenderStage.RENDER: 2,
    RenderStage.POST_PROCESS: 3,
}


@dataclass
class RenderStep:
    """A single render step.

    Attributes
    ----------
    name:
        Unique step identifier within a pipeline.
    func:
        Callable ``(text, ctx) -> (new_text, new_ctx)``.
    stage:
        Lifecycle stage in which this step runs.
    priority:
        Within a stage, lower values run first.
    enabled:
        Disabled steps are skipped at render time.
    """

    name: str
    func: Callable[[str, "RenderContext"], tuple[str, "RenderContext"]]
    stage: RenderStage = RenderStage.TRANSFORM
    priority: int = 0
    enabled: bool = True


@dataclass
class RenderContext:
    """Mutable context carried alongside text through the pipeline."""

    doc_id: str
    variables: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    applied_steps: list[str] = field(default_factory=list)


@dataclass
class RenderResult:
    """Aggregate result of a single render."""

    output: str
    context: RenderContext
    success: bool
    duration_ms: float = 0.0


class DocRenderPipeline:
    """Staged document rendering pipeline.

    Steps are grouped into :class:`RenderStage` buckets.  At render time
    stages execute in fixed order; within a stage steps run from lowest
    priority to highest.  Step exceptions are captured into
    ``context.errors`` and do not abort the pipeline.
    """

    def __init__(self) -> None:
        self._steps: dict[str, RenderStep] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_step(
        self,
        name: str,
        func: Callable[[str, RenderContext], tuple[str, RenderContext]],
        stage: RenderStage = RenderStage.TRANSFORM,
        priority: int = 0,
    ) -> RenderStep:
        """Register a new step.  Raises :class:`ValueError` on duplicate names."""
        with self._lock:
            if name in self._steps:
                raise ValueError(f"step {name!r} already exists")
            step = RenderStep(
                name=name,
                func=func,
                stage=stage,
                priority=priority,
                enabled=True,
            )
            self._steps[name] = step
            return step

    def remove_step(self, name: str) -> bool:
        with self._lock:
            if name in self._steps:
                del self._steps[name]
                return True
            return False

    def enable_step(self, name: str) -> bool:
        with self._lock:
            step = self._steps.get(name)
            if step is None:
                return False
            step.enabled = True
            return True

    def disable_step(self, name: str) -> bool:
        with self._lock:
            step = self._steps.get(name)
            if step is None:
                return False
            step.enabled = False
            return True

    def move_step(self, name: str, stage: RenderStage) -> bool:
        with self._lock:
            step = self._steps.get(name)
            if step is None:
                return False
            step.stage = stage
            return True

    def set_priority(self, name: str, priority: int) -> bool:
        with self._lock:
            step = self._steps.get(name)
            if step is None:
                return False
            step.priority = priority
            return True

    def clear(self) -> None:
        with self._lock:
            self._steps.clear()

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def step_count(self) -> int:
        with self._lock:
            return len(self._steps)

    def list_steps(
        self,
        stage: Optional[RenderStage] = None,
        enabled_only: bool = False,
    ) -> list[RenderStep]:
        """Return registered steps, optionally filtered.

        Ordering matches execution order: stage first, priority within stage.
        """
        with self._lock:
            steps = list(self._steps.values())
        if stage is not None:
            steps = [s for s in steps if s.stage == stage]
        if enabled_only:
            steps = [s for s in steps if s.enabled]
        steps.sort(key=lambda s: (_STAGE_ORDER[s.stage], s.priority))
        return steps

    def steps_in_stage(self, stage: RenderStage) -> list[RenderStep]:
        return self.list_steps(stage=stage)

    def validate(self) -> tuple[bool, list[str]]:
        """Basic structural validation.

        Currently checks that every step has a callable ``func`` and a
        recognised stage.  Returns ``(ok, errors)``.
        """
        errors: list[str] = []
        with self._lock:
            steps = list(self._steps.values())
        for step in steps:
            if not callable(step.func):
                errors.append(f"step {step.name!r} has non-callable func")
            if not isinstance(step.stage, RenderStage):
                errors.append(f"step {step.name!r} has invalid stage {step.stage!r}")
        return (not errors, errors)

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def render(
        self,
        input_text: str,
        doc_id: str = "doc",
        variables: dict | None = None,
    ) -> RenderResult:
        """Run all enabled steps in stage / priority order."""
        ctx = RenderContext(
            doc_id=doc_id,
            variables=dict(variables) if variables else {},
        )
        # Snapshot the steps under the lock so that concurrent mutations
        # don't change ordering mid-render.
        with self._lock:
            steps = sorted(
                [s for s in self._steps.values() if s.enabled],
                key=lambda s: (_STAGE_ORDER[s.stage], s.priority),
            )

        text = input_text
        start = time.perf_counter()
        for step in steps:
            try:
                new_text, new_ctx = step.func(text, ctx)
                text = new_text
                if isinstance(new_ctx, RenderContext):
                    ctx = new_ctx
                ctx.applied_steps.append(step.name)
            except Exception as exc:  # noqa: BLE001 — intentional broad capture
                ctx.errors.append(f"{step.name}: {exc}")
        duration_ms = (time.perf_counter() - start) * 1000.0

        return RenderResult(
            output=text,
            context=ctx,
            success=not ctx.errors,
            duration_ms=duration_ms,
        )

    def render_batch(self, inputs: list[tuple[str, str]]) -> list[RenderResult]:
        """Render multiple ``(text, doc_id)`` pairs sequentially."""
        results: list[RenderResult] = []
        for text, doc_id in inputs:
            results.append(self.render(text, doc_id=doc_id))
        return results
