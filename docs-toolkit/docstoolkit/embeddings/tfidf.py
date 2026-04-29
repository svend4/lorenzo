"""TF-IDF провайдер — baseline без зависимостей.

Использует:
  - Простой токенизатор (ru/en слова + цифры)
  - IDF из корпуса при первом encode
  - Sparse vectors (через dict[token, weight])
  - Cosine similarity на разреженных векторах
"""
import math
import re
from collections import Counter

from docstoolkit.embeddings.base import EmbeddingProvider


_STOP_WORDS = {
    # ru
    "и", "в", "на", "что", "как", "это", "для", "или", "но", "не", "по", "с", "из",
    "к", "у", "о", "за", "от", "до", "же", "ли", "бы",
    # en
    "the", "a", "an", "of", "in", "to", "is", "are", "for", "and", "or", "but",
    "with", "on", "at", "by", "as", "be", "this", "that",
}


def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zа-яё][a-zа-яё\-]{2,}", text.lower())
    return [w for w in words if w not in _STOP_WORDS]


class TFIDFProvider(EmbeddingProvider):
    name = "tfidf"
    dim = 0  # sparse, dim не определена

    def __init__(self):
        self._idf: dict[str, float] = {}
        self._fitted = False

    def fit(self, corpus: list[str]):
        """Считает IDF на корпусе."""
        df: Counter = Counter()
        n_docs = len(corpus)
        for text in corpus:
            tokens = set(_tokenize(text))
            for t in tokens:
                df[t] += 1
        self._idf = {
            t: math.log((n_docs + 1) / (cnt + 1)) + 1.0
            for t, cnt in df.items()
        }
        self._fitted = True

    def encode(self, texts: list[str]) -> list[dict[str, float]]:
        """Возвращает sparse-векторы (dict)."""
        if not self._fitted:
            self.fit(texts)
        vecs = []
        for text in texts:
            tokens = _tokenize(text)
            tf = Counter(tokens)
            total = max(sum(tf.values()), 1)
            vec = {}
            for t, cnt in tf.items():
                tf_norm = cnt / total
                idf = self._idf.get(t, 1.0)
                vec[t] = tf_norm * idf
            vecs.append(vec)
        return vecs

    def similarity(self, query_vec, doc_vecs):
        """Cosine similarity для sparse-векторов."""
        return [_cosine_sparse(query_vec, dv) for dv in doc_vecs]


def _cosine_sparse(a: dict, b: dict) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[t] * b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
