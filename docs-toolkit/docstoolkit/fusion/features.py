"""Feature extraction for learned retrieval fusion."""
from dataclasses import dataclass


@dataclass
class FusionFeatures:
    """Feature vector for one (query, passage) pair."""
    bm25_score: float = 0.0
    dense_score: float = 0.0
    graph_score: float = 0.0
    query_length: int = 0
    passage_length: int = 0
    intent: str = ""        # factoid | explanation | comparison | etc.

    def to_vector(self) -> list[float]:
        """Return [bm25_score, dense_score, graph_score, query_length_norm,
                   passage_length_norm] as floats.
        Normalize lengths: query_length/50, passage_length/500 (clipped to [0,1]).
        Does NOT include intent string (categorical, handled separately).
        """
        query_len_norm = min(1.0, self.query_length / 50.0)
        passage_len_norm = min(1.0, self.passage_length / 500.0)
        return [
            self.bm25_score,
            self.dense_score,
            self.graph_score,
            query_len_norm,
            passage_len_norm,
        ]


def extract_features(
    query: str,
    passage_text: str,
    *,
    bm25_score: float = 0.0,
    dense_score: float = 0.0,
    graph_score: float = 0.0,
    intent: str = "",
) -> FusionFeatures:
    """Build FusionFeatures from query/passage strings and pre-computed scores."""
    return FusionFeatures(
        bm25_score=bm25_score,
        dense_score=dense_score,
        graph_score=graph_score,
        query_length=len(query),
        passage_length=len(passage_text),
        intent=intent,
    )
