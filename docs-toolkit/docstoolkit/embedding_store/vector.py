"""EmbeddingVector: a lightweight wrapper around a float list vector."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field


@dataclass
class EmbeddingVector:
    """A single embedding vector associated with a document ID."""

    doc_id: str
    vector: list[float]
    metadata: dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def dimension(self) -> int:
        """Return the number of dimensions in the vector."""
        return len(self.vector)

    def norm(self) -> float:
        """Return the L2 (Euclidean) norm of the vector."""
        return math.sqrt(sum(x * x for x in self.vector))

    def normalize(self) -> "EmbeddingVector":
        """Return a new EmbeddingVector scaled to unit length.

        If the vector is the zero vector (norm == 0) the original vector is
        returned unchanged to avoid division by zero.
        """
        n = self.norm()
        if n == 0.0:
            return EmbeddingVector(
                doc_id=self.doc_id,
                vector=list(self.vector),
                metadata=dict(self.metadata),
                created_at=self.created_at,
            )
        inv = 1.0 / n
        return EmbeddingVector(
            doc_id=self.doc_id,
            vector=[x * inv for x in self.vector],
            metadata=dict(self.metadata),
            created_at=self.created_at,
        )

    def dot(self, other: "EmbeddingVector") -> float:
        """Return the dot product of this vector with *other*."""
        return sum(a * b for a, b in zip(self.vector, other.vector))

    def cosine_similarity(self, other: "EmbeddingVector") -> float:
        """Return the cosine similarity between this vector and *other*.

        Computed as the dot product of the two normalised vectors.
        Returns 0.0 if either vector has zero norm.
        """
        n_self = self.norm()
        n_other = other.norm()
        if n_self == 0.0 or n_other == 0.0:
            return 0.0
        return self.dot(other) / (n_self * n_other)
