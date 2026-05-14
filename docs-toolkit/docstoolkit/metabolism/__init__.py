"""Document metabolism: living documents that absorb, age, and converge."""
from docstoolkit.metabolism.signals import StalenessSignal, ConflictSignal, FreshnessScore
from docstoolkit.metabolism.absorber import absorb_fragment, AbsorptionResult
from docstoolkit.metabolism.aging import age_document, AgeReport, DocAge
from docstoolkit.metabolism.lifecycle import DocLifecycle, LifecycleState

__all__ = [
    "StalenessSignal", "ConflictSignal", "FreshnessScore",
    "absorb_fragment", "AbsorptionResult",
    "age_document", "AgeReport", "DocAge",
    "DocLifecycle", "LifecycleState",
]
