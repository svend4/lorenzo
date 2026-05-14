"""Explainability layer: attribution, reasoning traces, and reports."""
from docstoolkit.explainability.attribution import (
    AttributionMethod,
    TokenAttribution,
    PassageAttribution,
    AttributionExplainer,
)
from docstoolkit.explainability.trace import (
    TraceStep,
    ReasoningTrace,
    TraceBuilder,
)
from docstoolkit.explainability.report import (
    ExplainabilityReport,
    ExplainabilityEngine,
)

__all__ = [
    # attribution
    "AttributionMethod",
    "TokenAttribution",
    "PassageAttribution",
    "AttributionExplainer",
    # trace
    "TraceStep",
    "ReasoningTrace",
    "TraceBuilder",
    # report
    "ExplainabilityReport",
    "ExplainabilityEngine",
]
