"""E42 Evaluation Harness — IR metrics, dataset management, and batch runner.

Example usage::

    from docstoolkit.eval_harness import (
        EvalDataset, EvalHarness, EvalQuery,
        PrecisionAtK, RecallAtK, MRR, NDCG, F1Score,
    )

    dataset = EvalDataset.from_list([
        {"query": "What is RAG?", "relevant_docs": ["rag.md", "retrieval.md"]},
    ])

    def my_search(query: str) -> list[str]:
        return ["rag.md", "other.md"]

    harness = EvalHarness(dataset)
    report = harness.run(my_search)
    print(report.avg_mrr())
"""
from docstoolkit.eval_harness.dataset import EvalDataset, EvalQuery
from docstoolkit.eval_harness.metrics import F1Score, MRR, NDCG, PrecisionAtK, RecallAtK
from docstoolkit.eval_harness.runner import EvalHarness, EvalReport, EvalResult

__all__ = [
    # metrics
    "PrecisionAtK",
    "RecallAtK",
    "MRR",
    "NDCG",
    "F1Score",
    # dataset
    "EvalQuery",
    "EvalDataset",
    # runner
    "EvalResult",
    "EvalReport",
    "EvalHarness",
]
