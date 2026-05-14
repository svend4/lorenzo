"""Sequential workflow engine — E101.

Design principles:
- Pure stdlib: no third-party dependencies.
- Stateless engine: WorkflowEngine holds no per-run state; safe to reuse
  concurrently across threads as long as each call gets its own context.
- Context is a plain mutable dict shared by all steps.  Each step's return
  value is stored under context["_results"][step_name] as a StepResult so
  later steps can inspect it.
- Failure handling:
    - max_retries > 0  → retry up to that many *additional* times before
      deciding the step has failed.
    - skip_on_failure  → a final failure is recorded as SKIPPED and the
      workflow continues (success is not affected by SKIPPED steps).
    - Otherwise        → the step is marked FAILED, the workflow stops, and
      all remaining un-run steps are recorded as SKIPPED.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

class StepStatus(str, Enum):
    """Lifecycle states for a single workflow step."""
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


@dataclass
class StepConfig:
    """Declarative configuration for one workflow step.

    Args:
        name:            Unique step identifier within the workflow.
        fn:              Callable invoked as ``fn(context)`` where *context*
                         is the shared mutable dict.  Its return value is
                         stored in ``context["_results"][name].output``.
        max_retries:     Number of *additional* attempts after the first
                         failure (0 = no retries).
        skip_on_failure: When *True* a final failure is recorded as SKIPPED
                         and execution continues.  When *False* a failure
                         halts the workflow.
    """
    name: str
    fn: Callable
    max_retries: int = 0
    skip_on_failure: bool = False


@dataclass
class StepResult:
    """Outcome of a single step execution.

    Args:
        name:     Step name (matches ``StepConfig.name``).
        status:   Final lifecycle state.
        output:   Return value of ``fn(context)``, or *None* on failure.
        error:    The exception instance if the step raised, else *None*.
        attempts: Total number of calls made (1 = ran once with no retries).
    """
    name: str
    status: StepStatus
    output: Any = None
    error: Exception | None = None
    attempts: int = 0


@dataclass
class WorkflowConfig:
    """Full specification of a workflow: a name and an ordered list of steps.

    Args:
        name:  Human-readable workflow identifier.
        steps: Ordered list of :class:`StepConfig` objects.
    """
    name: str
    steps: list[StepConfig] = field(default_factory=list)


class WorkflowResult:
    """Immutable record of a completed workflow run.

    Args:
        name:   Workflow name from :class:`WorkflowConfig`.
        steps:  Ordered list of :class:`StepResult`, one per step.
    """

    def __init__(self, name: str, steps: list[StepResult]) -> None:
        self._name = name
        self._steps = list(steps)
        self._index: dict[str, StepResult] = {s.name: s for s in self._steps}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Workflow name."""
        return self._name

    @property
    def success(self) -> bool:
        """True when every step finished as DONE or SKIPPED (none FAILED)."""
        return all(s.status != StepStatus.FAILED for s in self._steps)

    @property
    def step_results(self) -> list[StepResult]:
        """Ordered list of all step results (a fresh copy)."""
        return list(self._steps)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, step_name: str) -> StepResult | None:
        """Return the :class:`StepResult` for *step_name*, or *None*."""
        return self._index.get(step_name)

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        status = "SUCCESS" if self.success else "FAILED"
        return f"<WorkflowResult name={self._name!r} {status} steps={len(self._steps)}>"


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class WorkflowEngine:
    """Stateless sequential workflow executor.

    The engine itself carries no per-run state — it is safe to reuse the
    same :class:`WorkflowEngine` instance from multiple threads as long as
    each call provides its own *context* dict (or passes *None*).

    Example::

        engine = WorkflowEngine()
        result = engine.run(config)
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        config: WorkflowConfig,
        context: dict | None = None,
    ) -> WorkflowResult:
        """Execute *config* steps sequentially and return a :class:`WorkflowResult`.

        Steps are run in declaration order.  The shared *context* dict is
        passed to every ``fn``; its ``"_results"`` key is reserved for the
        engine and populated with :class:`StepResult` objects keyed by step
        name as each step completes.

        Execution stops on the first hard failure (a step that exhausted all
        retries and has ``skip_on_failure=False``).  Any remaining steps are
        appended to the result with ``StepStatus.SKIPPED``.

        Args:
            config:  Workflow definition.
            context: Optional initial context.  Mutated in place.  A fresh
                     ``{}`` is used when *None*.

        Returns:
            :class:`WorkflowResult` with outcomes for every step.
        """
        if context is None:
            context = {}

        # Reserve the _results namespace.
        if "_results" not in context:
            context["_results"] = {}

        results: list[StepResult] = []
        halt = False  # True after a hard failure

        for cfg in config.steps:
            if halt:
                # Workflow already failed — record remaining steps as SKIPPED.
                sr = StepResult(
                    name=cfg.name,
                    status=StepStatus.SKIPPED,
                    output=None,
                    error=None,
                    attempts=0,
                )
                results.append(sr)
                context["_results"][cfg.name] = sr
                continue

            sr = self._run_step(cfg, context)
            results.append(sr)
            context["_results"][cfg.name] = sr

            if sr.status == StepStatus.FAILED:
                halt = True

        return WorkflowResult(name=config.name, steps=results)

    def validate(self, config: WorkflowConfig) -> list[str]:
        """Return a list of validation error messages for *config*.

        An empty list means the configuration is valid.

        Checks performed:

        * Workflow name must not be empty.
        * Every ``StepConfig.fn`` must be callable.
        * Every ``StepConfig.max_retries`` must be >= 0.
        * Step names must be unique within the workflow.
        """
        errors: list[str] = []

        if not config.name or not config.name.strip():
            errors.append("workflow name must not be empty")

        seen_names: set[str] = set()
        for step in config.steps:
            if step.name in seen_names:
                errors.append(f"duplicate step name: {step.name!r}")
            else:
                seen_names.add(step.name)

            if not callable(step.fn):
                errors.append(
                    f"step {step.name!r}: fn must be callable, got {type(step.fn).__name__!r}"
                )

            if step.max_retries < 0:
                errors.append(
                    f"step {step.name!r}: max_retries must be >= 0, got {step.max_retries}"
                )

        return errors

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run_step(self, cfg: StepConfig, context: dict) -> StepResult:
        """Execute one step with retry logic.

        Total attempts = 1 (initial) + max_retries.

        On success the result has ``status=DONE`` and ``output`` set to the
        return value of ``cfg.fn(context)``.

        On final failure:
        - ``skip_on_failure=True``  → ``status=SKIPPED``
        - ``skip_on_failure=False`` → ``status=FAILED``

        The ``attempts`` field always reflects how many times ``cfg.fn`` was
        actually called.
        """
        max_attempts = 1 + cfg.max_retries
        last_exc: Exception | None = None

        for attempt in range(1, max_attempts + 1):
            try:
                output = cfg.fn(context)
                return StepResult(
                    name=cfg.name,
                    status=StepStatus.DONE,
                    output=output,
                    error=None,
                    attempts=attempt,
                )
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                # If there are retries left, continue the loop.

        # All attempts exhausted.
        final_status = StepStatus.SKIPPED if cfg.skip_on_failure else StepStatus.FAILED
        return StepResult(
            name=cfg.name,
            status=final_status,
            output=None,
            error=last_exc,
            attempts=max_attempts,
        )
