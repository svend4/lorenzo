"""TextPipeline — composable text processing pipeline (pure stdlib)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class PipelineStep:
    """A single named transformation step.

    Parameters
    ----------
    name:
        Human-readable identifier.  Multiple steps may share a name.
    fn:
        Callable that accepts a :class:`str` and returns a :class:`str`.
    enabled:
        When ``False`` the step is skipped and the input passes through
        unchanged.
    condition:
        Optional predicate ``str -> bool``.  The step is skipped when the
        predicate returns ``False`` for the current input.
    """

    name: str
    fn: Callable[[str], str]
    enabled: bool = True
    condition: Callable[[str], bool] | None = None


@dataclass
class StepOutput:
    """Result record for a single executed (or skipped) step.

    Parameters
    ----------
    step_name:
        Name taken from :attr:`PipelineStep.name`.
    input:
        Text fed into this step (before ``fn`` was applied).
    output:
        Text produced by this step.  Equal to *input* when *skipped* is
        ``True``.
    skipped:
        ``True`` when the step was disabled or its condition returned
        ``False``.
    """

    step_name: str
    input: str
    output: str
    skipped: bool = False


@dataclass
class PipelineResult:
    """Aggregate result returned by :meth:`TextPipeline.run`.

    Parameters
    ----------
    final:
        The text produced after all steps have been applied (or the
        original text if every step was skipped).
    steps:
        Ordered list of :class:`StepOutput` records, one per step.
    """

    final: str
    steps: list[StepOutput] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Properties / helpers
    # ------------------------------------------------------------------

    @property
    def was_modified(self) -> bool:
        """``True`` if *final* differs from the text passed to the first step."""
        if not self.steps:
            return False
        return self.final != self.steps[0].input

    def get_step(self, name: str) -> StepOutput | None:
        """Return the first :class:`StepOutput` whose *step_name* matches *name*.

        Returns ``None`` when no matching step is found.
        """
        for s in self.steps:
            if s.step_name == name:
                return s
        return None

    def step_names(self) -> list[str]:
        """Return the names of all steps in execution order."""
        return [s.step_name for s in self.steps]


class TextPipeline:
    """Composable text-transformation pipeline.

    Steps are executed in the order they were added.  Each step receives
    the output of the previous step as its input.  Skipped steps pass
    their input through unchanged.

    Parameters
    ----------
    steps:
        Optional initial list of :class:`PipelineStep` objects.
    """

    def __init__(self, steps: list[PipelineStep] | None = None) -> None:
        self._steps: list[PipelineStep] = list(steps) if steps is not None else []

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_step(self, step: PipelineStep) -> "TextPipeline":
        """Append *step* to the pipeline.

        Returns ``self`` so calls can be chained::

            pipeline.add_step(a).add_step(b).add_step(c)
        """
        self._steps.append(step)
        return self

    def remove_step(self, name: str) -> bool:
        """Remove the first step whose name equals *name*.

        Returns ``True`` if a step was found and removed, ``False``
        otherwise.
        """
        for i, step in enumerate(self._steps):
            if step.name == name:
                del self._steps[i]
                return True
        return False

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def run(self, text: str) -> PipelineResult:
        """Execute all steps in order.

        Parameters
        ----------
        text:
            The initial input text.

        Returns
        -------
        PipelineResult
            Contains the final transformed text and per-step records.
        """
        return self._execute(text, self._steps)

    def run_steps(self, text: str, step_names: list[str]) -> PipelineResult:
        """Execute only the steps whose names appear in *step_names*.

        Steps are executed in their *definition* order, not the order of
        *step_names*.  Steps not in *step_names* are omitted entirely from
        the result (they do not appear in :attr:`PipelineResult.steps`).

        Parameters
        ----------
        text:
            The initial input text.
        step_names:
            Names of the steps to include.

        Returns
        -------
        PipelineResult
        """
        name_set = set(step_names)
        subset = [s for s in self._steps if s.name in name_set]
        return self._execute(text, subset)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def step_count(self) -> int:
        """Return the total number of registered steps."""
        return len(self._steps)

    def step_names(self) -> list[str]:
        """Return the names of all registered steps in definition order."""
        return [s.name for s in self._steps]

    def clone(self) -> "TextPipeline":
        """Return a new :class:`TextPipeline` with a shallow copy of the step list.

        Modifying the clone (adding or removing steps) does not affect the
        original, and vice-versa.  The :class:`PipelineStep` objects
        themselves are shared.
        """
        return TextPipeline(list(self._steps))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _execute(text: str, steps: list[PipelineStep]) -> PipelineResult:
        """Run *steps* against *text* and collect per-step records."""
        outputs: list[StepOutput] = []
        current = text

        for step in steps:
            step_input = current

            # Determine whether to skip this step.
            if not step.enabled:
                skipped = True
            elif step.condition is not None and not step.condition(step_input):
                skipped = True
            else:
                skipped = False

            if skipped:
                step_output = step_input  # pass through unchanged
            else:
                # Let exceptions propagate — no silent swallowing.
                step_output = step.fn(step_input)

            outputs.append(
                StepOutput(
                    step_name=step.name,
                    input=step_input,
                    output=step_output,
                    skipped=skipped,
                )
            )
            current = step_output

        return PipelineResult(final=current, steps=outputs)
