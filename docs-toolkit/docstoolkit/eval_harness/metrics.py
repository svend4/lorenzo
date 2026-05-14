"""IR evaluation metrics: Precision@K, Recall@K, MRR, NDCG, F1Score."""
import math


class PrecisionAtK:
    """Precision at K: fraction of top-K retrieved docs that are relevant."""

    @staticmethod
    def compute(retrieved: list[str], relevant: set[str], k: int) -> float:
        """Return |retrieved[:k] ∩ relevant| / k.  Returns 0 if k <= 0."""
        if k <= 0:
            return 0.0
        top_k = retrieved[:k]
        hits = sum(1 for doc in top_k if doc in relevant)
        return hits / k


class RecallAtK:
    """Recall at K: fraction of relevant docs found in the top K results."""

    @staticmethod
    def compute(retrieved: list[str], relevant: set[str], k: int) -> float:
        """Return |retrieved[:k] ∩ relevant| / (|relevant| + 1e-10)."""
        top_k = retrieved[:k]
        hits = sum(1 for doc in top_k if doc in relevant)
        return hits / (len(relevant) + 1e-10)


class MRR:
    """Mean Reciprocal Rank: 1/rank of first relevant doc (0 if none found)."""

    @staticmethod
    def compute(retrieved: list[str], relevant: set[str]) -> float:
        """Return 1/rank of first relevant item, or 0.0 if none present."""
        for rank, doc in enumerate(retrieved, start=1):
            if doc in relevant:
                return 1.0 / rank
        return 0.0


class NDCG:
    """Normalized Discounted Cumulative Gain at K (binary relevance)."""

    @staticmethod
    def compute(retrieved: list[str], relevant: set[str], k: int) -> float:
        """Return NDCG@K.  DCG uses rel_i / log2(i+2) for i in range(k).

        Returns 0.0 when IDCG is 0 (i.e. no relevant documents exist).
        """
        if k <= 0:
            return 0.0

        def _dcg(ranking: list[str]) -> float:
            total = 0.0
            for i, doc in enumerate(ranking[:k]):
                rel = 1.0 if doc in relevant else 0.0
                total += rel / math.log2(i + 2)
            return total

        dcg = _dcg(retrieved)

        # Ideal: place all relevant docs first
        n_relevant_in_k = min(len(relevant), k)
        ideal_ranking = list(relevant)[:n_relevant_in_k]
        # Pad with placeholders that are not relevant to fill to k
        idcg = _dcg(ideal_ranking)

        if idcg == 0.0:
            return 0.0
        return dcg / idcg


class F1Score:
    """Harmonic mean of precision and recall."""

    @staticmethod
    def compute(precision: float, recall: float) -> float:
        """Return 2*P*R / (P+R), or 0.0 if both are 0."""
        denom = precision + recall
        if denom == 0.0:
            return 0.0
        return 2.0 * precision * recall / denom
