"""Eval / golden dataset framework.

Использование:
    from docstoolkit.eval import GoldenItem, GoldenSet, run_eval

    gset = GoldenSet(name="rag-baseline", items=[
        GoldenItem(question="что такое Yodoca?",
                   expected_answer_contains=["memory", "hot path"],
                   expected_doc_ids=["yodoca.md", "memory-architecture.md"]),
    ])
    result = run_eval(gset, retriever_config={"method": "hybrid", "top_k": 5})
    print(result.report())  # markdown с per-item + aggregate scores
"""
from docstoolkit.eval.golden import (
    GoldenItem, GoldenSet, EvalItemResult, EvalResult,
    score_answer, score_citations, run_eval, load_golden_from_yaml,
)

__all__ = [
    "GoldenItem", "GoldenSet", "EvalItemResult", "EvalResult",
    "score_answer", "score_citations", "run_eval", "load_golden_from_yaml",
]
