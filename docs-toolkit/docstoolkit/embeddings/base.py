"""Базовые типы для embeddings."""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Результат поиска."""
    doc_id: str
    score: float
    title: str = ""
    path: str = ""
    snippet: str = ""

    def __lt__(self, other):
        return self.score < other.score


class EmbeddingProvider(ABC):
    """Общий интерфейс провайдера embeddings."""

    name: str = "base"
    dim: int = 0

    @abstractmethod
    def encode(self, texts: list[str]) -> list[list[float]]:
        """Возвращает векторы для списка текстов. Размерность = self.dim."""
        ...

    @abstractmethod
    def similarity(self, query_vec: list[float], doc_vecs: list[list[float]]) -> list[float]:
        """Возвращает scores [0..1] между query и каждым doc."""
        ...

    def search(self, query: str, docs: list[dict], top_k: int = 10) -> list[SearchResult]:
        """Default-реализация: encode → similarity → топ-k.

        docs: list[{id, title, content, path, ...}]
        """
        if not docs:
            return []
        query_vec = self.encode([query])[0]
        doc_texts = [self._doc_text(d) for d in docs]
        doc_vecs = self.encode(doc_texts)
        scores = self.similarity(query_vec, doc_vecs)

        scored = []
        for d, s in zip(docs, scores):
            if s > 0:
                scored.append(SearchResult(
                    doc_id=d.get("id", d.get("path", "?")),
                    score=float(s),
                    title=d.get("title", ""),
                    path=d.get("path", ""),
                    snippet=d.get("content", d.get("preview", ""))[:200],
                ))
        scored.sort(key=lambda r: -r.score)
        return scored[:top_k]

    @staticmethod
    def _doc_text(d: dict) -> str:
        return " ".join(filter(None, [
            d.get("title", ""),
            d.get("content", ""),
            d.get("preview", ""),
        ]))
