"""FusedRetriever: combines BM25/dense/graph scores via LearnedFusion or RRF."""
from docstoolkit.fusion.features import FusionFeatures, extract_features
from docstoolkit.fusion.model import LearnedFusion


def rrf_fusion(
    ranked_lists: list[list[str]],  # multiple ranked lists of doc_ids
    k: int = 60,
) -> list[tuple[str, float]]:
    """Reciprocal Rank Fusion.

    score(d) = sum over lists: 1 / (k + rank(d, list))
    rank is 1-based.
    Returns [(doc_id, score)] sorted descending.
    """
    if not ranked_lists:
        return []

    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, doc_id in enumerate(ranked, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


class FusedRetriever:
    """Retriever that combines BM25/dense/graph scores via LearnedFusion."""

    def __init__(
        self,
        fusion_model: LearnedFusion | None = None,
        *,
        fallback_to_rrf: bool = True,
    ):
        self._model = fusion_model
        self._fallback = fallback_to_rrf

    def score_passages(
        self,
        query: str,
        candidates: list[dict],  # [{text, doc_id, bm25, dense, graph}]
        top_k: int = 10,
    ) -> list[tuple[str, float]]:
        """Score and rank passages.

        If model trained: use LearnedFusion.score(features)
        Else if fallback_to_rrf: use rrf_fusion on BM25+dense+graph ranked lists
        Else: return candidates sorted by bm25_score

        Returns [(doc_id, score)] sorted descending, top_k.
        """
        if not candidates:
            return []

        if self._model is not None:
            # Use learned fusion scores
            scored = []
            for c in candidates:
                features = extract_features(
                    query,
                    c.get("text", ""),
                    bm25_score=c.get("bm25", 0.0),
                    dense_score=c.get("dense", 0.0),
                    graph_score=c.get("graph", 0.0),
                )
                score = self._model.score(features)
                scored.append((c["doc_id"], score))
            scored.sort(key=lambda x: x[1], reverse=True)
            return scored[:top_k]

        if self._fallback:
            # Build per-signal ranked lists and apply RRF
            bm25_ranked = [
                c["doc_id"] for c in sorted(candidates, key=lambda x: x.get("bm25", 0.0), reverse=True)
            ]
            dense_ranked = [
                c["doc_id"] for c in sorted(candidates, key=lambda x: x.get("dense", 0.0), reverse=True)
            ]
            graph_ranked = [
                c["doc_id"] for c in sorted(candidates, key=lambda x: x.get("graph", 0.0), reverse=True)
            ]
            result = rrf_fusion([bm25_ranked, dense_ranked, graph_ranked])
            return result[:top_k]

        # Fallback: sort by bm25_score
        scored = [(c["doc_id"], c.get("bm25", 0.0)) for c in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def is_trained(self) -> bool:
        return self._model is not None
