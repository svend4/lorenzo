"""Continuous online evaluation — мониторинг качества RAG в production.

Использование:
    from docstoolkit.online_eval import (
        OnlineEvalSampler, OnlineEvalStore, OnlineEvalRunner,
        OnlineEvalRun, DriftReport,
    )

    sampler = OnlineEvalSampler(sample_rate=0.05)
    store   = OnlineEvalStore(db_path=Path("/tmp/eval.sqlite"))
    runner  = OnlineEvalRunner(store=store, sampler=sampler)

    run = runner.maybe_run(query, rag_result)  # None if not sampled
    if run:
        print(f"Sampled: f1={run.f1:.3f}")

    drift = runner.compute_drift()
    for d in drift:
        if d.significant:
            print(f"DRIFT {d.metric}: {d.delta:+.3f}")
"""
from docstoolkit.online_eval.sampler import OnlineEvalSampler
from docstoolkit.online_eval.runner import (
    OnlineEvalRun,
    DriftReport,
    OnlineEvalStore,
    OnlineEvalRunner,
)
from docstoolkit.online_eval.dashboard import render_dashboard
from docstoolkit.online_eval.drift import psi, psi_label, chi_square_drift, DriftWindow

__all__ = [
    "OnlineEvalSampler",
    "OnlineEvalStore",
    "OnlineEvalRunner",
    "OnlineEvalRun",
    "DriftReport",
    "render_dashboard",
    "psi",
    "psi_label",
    "chi_square_drift",
    "DriftWindow",
]
