"""Bandit-driven ask() — Sprint 76 / I7.

Wraps `rag.ask()` with a `BanditExperiment` so each call picks one of
several pre-configured variants (e.g. method+rerank combos), and the
bandit learns which variant the user prefers over time.

Usage:
    from docstoolkit.bandit import BanditExperiment
    from docstoolkit.rag.bandit_ask import ask_with_bandit

    exp = BanditExperiment("retriever-test", ["bm25", "hybrid", "semantic"])

    variants = {
        "bm25":     {"method": "bm25"},
        "hybrid":   {"method": "hybrid"},
        "semantic": {"method": "semantic"},
    }

    result, picked = ask_with_bandit("query", exp, variants)
    # The caller can later record outcome:
    exp.record(picked, success=True)  # or False, based on user feedback
"""
from __future__ import annotations

from typing import Any

from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import AnswerResult


def ask_with_bandit(
    question: str,
    experiment: Any,
    variants: dict[str, dict],
    **ask_kwargs,
) -> tuple[AnswerResult, str]:
    """Pick one variant via the bandit, call ask() with its kwargs.

    Returns (result, picked_variant_name). The caller is responsible
    for calling `experiment.record(picked, success=...)` after evaluating.
    """
    if not variants:
        raise ValueError("variants must be a non-empty dict")
    picked = experiment.choose()
    if picked not in variants:
        # Fallback: first variant
        picked = next(iter(variants))
    merged = {**ask_kwargs, **variants[picked]}
    result = ask(question, **merged)
    return result, picked


def evaluate_record(
    experiment: Any,
    picked: str,
    result: AnswerResult,
    *,
    success_threshold: float = 0.3,
) -> bool:
    """Convenience: classify an AnswerResult as success and record it.

    Heuristic: passage max-score above threshold AND non-empty answer
    AND no error → success.
    """
    if result.error:
        success = False
    elif not result.answer or not result.retrieved_passages:
        success = False
    else:
        max_score = max(
            (p.score for p in result.retrieved_passages), default=0.0,
        )
        success = max_score >= success_threshold
    experiment.record(picked, success=success)
    return success
