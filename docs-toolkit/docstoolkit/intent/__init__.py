"""Query intent classification and pipeline routing."""
from docstoolkit.intent.classifier import (
    Intent, IntentClassifier,
    FACTOID, EXPLANATION, COMPARISON, SYNTHESIS, OPINION, INSTRUCTION, UNKNOWN,
)
from docstoolkit.intent.router import PipelineConfig, IntentRouter

__all__ = [
    "Intent",
    "IntentClassifier",
    "PipelineConfig",
    "IntentRouter",
    # Labels
    "FACTOID",
    "EXPLANATION",
    "COMPARISON",
    "SYNTHESIS",
    "OPINION",
    "INSTRUCTION",
    "UNKNOWN",
]
