"""NormPipeline — chain multiple TextNormalizer steps."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.text_normalizer.normalizer import TextNormalizer


@dataclass
class NormStep:
    """A named normalization step wrapping a :class:`TextNormalizer`."""

    name: str
    normalizer: TextNormalizer


class NormPipeline:
    """Execute a sequence of :class:`NormStep` objects on text.

    Parameters
    ----------
    steps:
        Optional initial list of :class:`NormStep` objects.  Defaults to an
        empty pipeline.
    """

    def __init__(self, steps: list[NormStep] | None = None) -> None:
        self._steps: list[NormStep] = list(steps) if steps is not None else []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_step(self, step: NormStep) -> None:
        """Append *step* to the pipeline."""
        self._steps.append(step)

    def run(self, text: str) -> str:
        """Apply each step's normalizer to *text* in order and return the result."""
        for step in self._steps:
            text = step.normalizer.normalize(text)
        return text

    def run_batch(self, texts: list[str]) -> list[str]:
        """Return a new list with :meth:`run` applied to every element."""
        return [self.run(t) for t in texts]

    def step_names(self) -> list[str]:
        """Return the names of all steps in pipeline order."""
        return [step.name for step in self._steps]
