"""Explainability report: aggregates attributions, trace, and confidence."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.explainability.attribution import (
    AttributionExplainer,
    PassageAttribution,
)
from docstoolkit.explainability.trace import ReasoningTrace


@dataclass
class ExplainabilityReport:
    query: str
    answer: str
    attributions: list[PassageAttribution]
    trace: ReasoningTrace | None = None
    confidence: float = 0.0

    def top_passages(self, n: int = 3) -> list[PassageAttribution]:
        """Return top-n passages sorted by attribution_score descending."""
        return sorted(self.attributions, key=lambda a: a.attribution_score, reverse=True)[:n]

    def to_dict(self) -> dict:
        """Serialize report to a plain dict."""
        result: dict = {
            "query": self.query,
            "answer": self.answer,
            "confidence": self.confidence,
            "attributions": [
                {
                    "passage_id": a.passage_id,
                    "passage_text": a.passage_text,
                    "attribution_score": a.attribution_score,
                    "rank": a.rank,
                    "token_attributions": [
                        {
                            "token": t.token,
                            "score": t.score,
                            "method": t.method.value,
                        }
                        for t in a.token_attributions
                    ],
                }
                for a in self.attributions
            ],
        }
        if self.trace is not None:
            result["trace"] = {
                "query": self.trace.query,
                "final_answer": self.trace.final_answer,
                "total_ms": self.trace.total_ms,
                "steps": [
                    {
                        "step_name": s.step_name,
                        "input_summary": s.input_summary,
                        "output_summary": s.output_summary,
                        "duration_ms": s.duration_ms,
                        "metadata": s.metadata,
                    }
                    for s in self.trace.steps
                ],
            }
        else:
            result["trace"] = None
        return result

    def to_markdown(self) -> str:
        """Render report as markdown: query, answer, top passages, trace."""
        lines = ["# Explainability Report\n"]
        lines.append(f"**Query:** {self.query}\n")
        lines.append(f"**Answer:** {self.answer}\n")
        lines.append(f"**Confidence:** {self.confidence:.3f}\n")

        top = self.top_passages(3)
        if top:
            lines.append("## Top Passages\n")
            for pa in top:
                lines.append(
                    f"### Passage {pa.passage_id} (score: {pa.attribution_score:.3f}, rank: {pa.rank})\n"
                )
                lines.append(pa.passage_text + "\n")
                tokens = pa.top_tokens(5)
                if tokens:
                    token_str = ", ".join(f"{t.token}={t.score:.3f}" for t in tokens)
                    lines.append(f"**Top tokens:** {token_str}\n")

        if self.trace is not None:
            lines.append(self.trace.to_markdown())

        return "\n".join(lines)


class ExplainabilityEngine:
    """Compute and package explainability for a query/answer/passages triplet."""

    def __init__(self) -> None:
        self._explainer = AttributionExplainer()

    def explain(
        self,
        query: str,
        answer: str,
        passages: list[str],
        trace: ReasoningTrace | None = None,
    ) -> ExplainabilityReport:
        """Compute attributions and estimate confidence.

        Confidence = average attribution_score of top-3 passages (0.0 if none).
        """
        attributions = self._explainer.explain_all(query, passages)

        top3 = attributions[:3]
        if top3:
            confidence = sum(a.attribution_score for a in top3) / len(top3)
        else:
            confidence = 0.0

        return ExplainabilityReport(
            query=query,
            answer=answer,
            attributions=attributions,
            trace=trace,
            confidence=confidence,
        )
