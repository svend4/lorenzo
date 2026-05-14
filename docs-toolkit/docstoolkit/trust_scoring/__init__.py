"""Trust scoring module — E33.

Provides signal extraction, aggregation, and persistence for document trust.
"""

from docstoolkit.trust_scoring.signals import (
    TrustSignal,
    SignalScore,
    TrustSignalExtractor,
)
from docstoolkit.trust_scoring.scorer import (
    TrustWeights,
    TrustScore,
    TrustScorer,
)
from docstoolkit.trust_scoring.registry import TrustRegistry

__all__ = [
    # signals
    "TrustSignal",
    "SignalScore",
    "TrustSignalExtractor",
    # scorer
    "TrustWeights",
    "TrustScore",
    "TrustScorer",
    # registry
    "TrustRegistry",
]
