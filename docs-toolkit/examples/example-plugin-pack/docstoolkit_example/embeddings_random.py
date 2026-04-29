"""Random embeddings provider (демо).

Не для production — генерирует случайные векторы для тестов.
Показывает, как реализовать собственный EmbeddingProvider.
"""
import hashlib
import math

from docstoolkit.embeddings.base import EmbeddingProvider


class RandomProvider(EmbeddingProvider):
    name = "random"
    dim = 64

    def __init__(self, dim: int = 64):
        self.dim = dim

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Детерминистично-случайный вектор (хэш текста как seed)."""
        vecs = []
        for text in texts:
            h = hashlib.sha256(text.encode("utf-8")).digest()
            vec = []
            for i in range(self.dim):
                byte = h[i % len(h)]
                vec.append((byte / 255.0) * 2 - 1)  # [-1, 1]
            # L2 normalize
            norm = math.sqrt(sum(v * v for v in vec))
            if norm > 0:
                vec = [v / norm for v in vec]
            vecs.append(vec)
        return vecs

    def similarity(self, query_vec, doc_vecs):
        return [sum(q * d for q, d in zip(query_vec, dv)) for dv in doc_vecs]
