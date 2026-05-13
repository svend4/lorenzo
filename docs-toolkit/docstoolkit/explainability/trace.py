"""Reasoning trace capture and formatting for explainability."""
from dataclasses import dataclass, field


@dataclass
class TraceStep:
    step_name: str
    input_summary: str
    output_summary: str
    duration_ms: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class ReasoningTrace:
    query: str
    steps: list[TraceStep]
    final_answer: str = ""
    total_ms: float = 0.0

    def add_step(self, step: TraceStep) -> None:
        """Append a step to the trace."""
        self.steps.append(step)

    def to_markdown(self) -> str:
        """Render trace as numbered markdown list of steps."""
        lines = [f"## Reasoning Trace\n", f"**Query:** {self.query}\n"]
        if self.final_answer:
            lines.append(f"**Answer:** {self.final_answer}\n")
        lines.append("### Steps\n")
        for i, step in enumerate(self.steps, start=1):
            lines.append(f"{i}. **{step.step_name}**")
            lines.append(f"   - Input: {step.input_summary}")
            lines.append(f"   - Output: {step.output_summary}")
            if step.duration_ms:
                lines.append(f"   - Duration: {step.duration_ms:.1f}ms")
        if self.total_ms:
            lines.append(f"\n**Total duration:** {self.total_ms:.1f}ms")
        return "\n".join(lines)

    def step_count(self) -> int:
        """Return the number of steps in the trace."""
        return len(self.steps)


class TraceBuilder:
    """Incrementally build a ReasoningTrace."""

    def __init__(self, query: str) -> None:
        self._query = query
        self._steps: list[TraceStep] = []

    def record(
        self,
        step_name: str,
        input_summary: str,
        output_summary: str,
        duration_ms: float = 0.0,
        **metadata,
    ) -> None:
        """Record a single step in the trace."""
        self._steps.append(
            TraceStep(
                step_name=step_name,
                input_summary=input_summary,
                output_summary=output_summary,
                duration_ms=duration_ms,
                metadata=dict(metadata),
            )
        )

    def build(self, final_answer: str = "") -> ReasoningTrace:
        """Finalize and return the ReasoningTrace."""
        total_ms = sum(s.duration_ms for s in self._steps)
        return ReasoningTrace(
            query=self._query,
            steps=list(self._steps),
            final_answer=final_answer,
            total_ms=total_ms,
        )
