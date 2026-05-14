"""EvalHarness: runs a search function over an EvalDataset and produces an EvalReport."""
from dataclasses import dataclass, field
from typing import Callable

from docstoolkit.eval_harness.dataset import EvalDataset
from docstoolkit.eval_harness.metrics import (
    F1Score,
    MRR,
    NDCG,
    PrecisionAtK,
    RecallAtK,
)

_K = 5  # default @K for per-result metrics


@dataclass
class EvalResult:
    """Evaluation result for a single query."""

    query_id: str
    query: str
    retrieved: list[str]
    relevant: set[str]
    precision_at_5: float
    recall_at_5: float
    mrr: float
    ndcg_at_5: float

    def f1(self) -> float:
        """Harmonic mean of precision_at_5 and recall_at_5."""
        return F1Score.compute(self.precision_at_5, self.recall_at_5)


@dataclass
class EvalReport:
    """Aggregated evaluation results over the entire dataset."""

    results: list[EvalResult]
    dataset_size: int

    # ------------------------------------------------------------------
    # Aggregates
    # ------------------------------------------------------------------

    def avg_precision(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.precision_at_5 for r in self.results) / len(self.results)

    def avg_recall(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.recall_at_5 for r in self.results) / len(self.results)

    def avg_mrr(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.mrr for r in self.results) / len(self.results)

    def avg_ndcg(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.ndcg_at_5 for r in self.results) / len(self.results)

    def avg_f1(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.f1() for r in self.results) / len(self.results)

    def to_dict(self) -> dict:
        """Serialise the report to a plain dict."""
        return {
            "dataset_size": self.dataset_size,
            "num_results": len(self.results),
            "avg_precision_at_5": self.avg_precision(),
            "avg_recall_at_5": self.avg_recall(),
            "avg_mrr": self.avg_mrr(),
            "avg_ndcg_at_5": self.avg_ndcg(),
            "avg_f1": self.avg_f1(),
            "results": [
                {
                    "query_id": r.query_id,
                    "query": r.query,
                    "retrieved": r.retrieved,
                    "relevant": sorted(r.relevant),
                    "precision_at_5": r.precision_at_5,
                    "recall_at_5": r.recall_at_5,
                    "mrr": r.mrr,
                    "ndcg_at_5": r.ndcg_at_5,
                    "f1": r.f1(),
                }
                for r in self.results
            ],
        }


class EvalHarness:
    """Orchestrates evaluation of a search function over an EvalDataset."""

    def __init__(self, dataset: EvalDataset) -> None:
        self._dataset = dataset

    def run(
        self,
        search_fn: Callable[[str], list[str]],
        top_k: int = 10,
    ) -> EvalReport:
        """Evaluate *search_fn* over every query in the dataset.

        Args:
            search_fn: Callable that accepts a query string and returns an
                       ordered list of doc_id strings.
            top_k:     Number of results to request from search_fn.  The
                       per-result metrics are always computed at K=5.

        Returns:
            An EvalReport with per-query EvalResult objects and aggregate stats.
        """
        results: list[EvalResult] = []

        for eval_query in self._dataset:
            retrieved = search_fn(eval_query.query)
            if not isinstance(retrieved, list):
                retrieved = list(retrieved)
            # Trim to top_k if the search function returns more
            retrieved = retrieved[:top_k]

            relevant = eval_query.relevant_docs

            precision = PrecisionAtK.compute(retrieved, relevant, k=_K)
            recall = RecallAtK.compute(retrieved, relevant, k=_K)
            mrr = MRR.compute(retrieved, relevant)
            ndcg = NDCG.compute(retrieved, relevant, k=_K)

            results.append(
                EvalResult(
                    query_id=eval_query.query_id,
                    query=eval_query.query,
                    retrieved=retrieved,
                    relevant=relevant,
                    precision_at_5=precision,
                    recall_at_5=recall,
                    mrr=mrr,
                    ndcg_at_5=ndcg,
                )
            )

        return EvalReport(results=results, dataset_size=len(self._dataset))
