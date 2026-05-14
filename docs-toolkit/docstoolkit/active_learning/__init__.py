"""Active Learning Queue — M6 module.

Automatically collects ambiguous / low-confidence queries for human
labelling, then exports labelled data as a YAML golden dataset.

Public API
----------
LearningQueue      — SQLite-backed queue (add / get / list_pending / label /
                     skip / export_golden / stats)
LearningItem       — dataclass for one queue entry
LowConfidenceTrigger  — fires when max passage score < threshold
DownThumbTrigger      — fires on user thumbs-down feedback
GoldenMismatchTrigger — fires when query matches a golden query but top-1
                        passage is wrong
CompositeTrigger      — fires if ANY child trigger fires
auto_enqueue          — convenience wrapper: trigger → build item → enqueue
"""

from docstoolkit.active_learning.queue import LearningItem, LearningQueue
from docstoolkit.active_learning.triggers import (
    CompositeTrigger,
    DownThumbTrigger,
    GoldenMismatchTrigger,
    LowConfidenceTrigger,
    auto_enqueue,
)

__all__ = [
    "LearningQueue",
    "LearningItem",
    "LowConfidenceTrigger",
    "DownThumbTrigger",
    "GoldenMismatchTrigger",
    "CompositeTrigger",
    "auto_enqueue",
]
