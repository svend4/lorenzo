"""Feedback loop: signal capture, storage, and aggregation (E19).

E19 Public API
--------------
Signal layer:
    FeedbackType, FeedbackSignal

New signal store:
    SignalStore  (E19 SQLite-backed store for FeedbackSignal objects)

Legacy store (backward-compat — keeps existing tests working):
    FeedbackStore  (pre-E19 store with .record() / .list_recent() / ._calc_quality())

Aggregation layer:
    DocScore, FeedbackAggregator
"""

# E19 — signal layer
from docstoolkit.feedback.signal import FeedbackType, FeedbackSignal

# E19 — new signal store (use SignalStore for new code)
from docstoolkit.feedback.store import SignalStore

# Legacy store — FeedbackStore keeps pointing at the pre-E19 implementation
# so that existing tests using .record() / .list_recent() / ._calc_quality() work
from docstoolkit.feedback.legacy_store import FeedbackStore, Feedback

# E19 — aggregation layer
from docstoolkit.feedback.aggregator import DocScore, FeedbackAggregator

# Legacy autotuner (still importable)
from docstoolkit.feedback.autotuner import AutoTuner, WinRateStats, wilson_lower, compute_winrates

__all__ = [
    # E19
    "FeedbackType",
    "FeedbackSignal",
    "SignalStore",
    "DocScore",
    "FeedbackAggregator",
    # Legacy backward-compat
    "FeedbackStore",
    "Feedback",
    # Legacy autotuner
    "AutoTuner",
    "WinRateStats",
    "wilson_lower",
    "compute_winrates",
]
