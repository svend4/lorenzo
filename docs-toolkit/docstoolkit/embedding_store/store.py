"""EmbeddingStore: in-memory brute-force vector store."""

from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.embedding_store.vector import EmbeddingVector


@dataclass
class StoreConfig:
    """Configuration for an EmbeddingStore."""

    dimension: int = 128
    metric: str = "cosine"        # "cosine" | "dot"
    normalize_on_add: bool = True


class EmbeddingStore:
    """In-memory store for EmbeddingVectors with brute-force similarity search."""

    def __init__(self, config: StoreConfig | None = None) -> None:
        self._config: StoreConfig = config if config is not None else StoreConfig()
        self._vectors: dict[str, EmbeddingVector] = {}

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def add(self, vec: EmbeddingVector) -> None:
        """Add (or replace) a vector in the store.

        Raises ValueError if *vec* dimension doesn't match the store's
        configured dimension.
        """
        if vec.dimension() != self._config.dimension:
            raise ValueError(
                f"Vector dimension {vec.dimension()} does not match "
                f"store dimension {self._config.dimension}."
            )
        if self._config.normalize_on_add:
            vec = vec.normalize()
        self._vectors[vec.doc_id] = vec

    def get(self, doc_id: str) -> EmbeddingVector | None:
        """Return the vector for *doc_id*, or None if not present."""
        return self._vectors.get(doc_id)

    def remove(self, doc_id: str) -> bool:
        """Remove the vector for *doc_id*.  Return True if it existed."""
        if doc_id in self._vectors:
            del self._vectors[doc_id]
            return True
        return False

    def clear(self) -> None:
        """Remove all vectors from the store."""
        self._vectors.clear()

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def search(
        self,
        query: EmbeddingVector,
        top_k: int = 10,
    ) -> list[tuple[str, float]]:
        """Return the top-*k* most similar vectors as (doc_id, score) pairs.

        Scores are sorted in descending order (highest similarity first).
        """
        if not self._vectors:
            return []

        metric = self._config.metric
        if metric == "cosine":
            # When normalize_on_add=True every stored vector is already unit
            # length, so cosine = dot.  We normalise the query here too so
            # the result is always a proper cosine similarity.
            norm_query = query.normalize()
            scores = [
                (doc_id, norm_query.dot(v))
                for doc_id, v in self._vectors.items()
            ]
        elif metric == "dot":
            scores = [
                (doc_id, query.dot(v))
                for doc_id, v in self._vectors.items()
            ]
        else:
            raise ValueError(f"Unknown metric: {metric!r}")

        scores.sort(key=lambda t: t[1], reverse=True)
        return scores[:top_k]

    def all_ids(self) -> list[str]:
        """Return all stored document IDs (order not guaranteed)."""
        return list(self._vectors.keys())

    def size(self) -> int:
        """Return the number of vectors currently in the store."""
        return len(self._vectors)
