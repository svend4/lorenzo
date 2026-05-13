"""Feedback loop: thumbs-up/down + quality tracking + auto-tuning.

Использование:
    from docstoolkit.feedback import FeedbackStore, Feedback, AutoTuner

    store = FeedbackStore()
    store.record(Feedback(
        request_id="req_123", request="что такое X",
        response_text="ответ", thumbs="up",
        skill="rag", retriever="hybrid",
    ))

    # Aggregations
    stats = store.aggregate_per_skill()
    quality = store.quality_score(skill="rag")

    # Auto-tuning
    tuner = AutoTuner(store, min_samples=20, improve_threshold=0.15)
    for suggestion in tuner.suggest_improvements():
        print(suggestion)
"""
from docstoolkit.feedback.store import FeedbackStore, Feedback
from docstoolkit.feedback.autotuner import AutoTuner, WinRateStats, wilson_lower, compute_winrates

__all__ = ["FeedbackStore", "Feedback", "AutoTuner", "WinRateStats", "wilson_lower", "compute_winrates"]
