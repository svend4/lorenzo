"""sentence-transformers провайдер — опциональный, нужен `pip install sentence-transformers`.

Модели по умолчанию:
  - all-MiniLM-L6-v2 (384 dim, быстрая, английский)
  - paraphrase-multilingual-MiniLM-L12-v2 (384 dim, RU+EN)
"""
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
except ImportError:
    raise ImportError(
        "Для sentence-transformers провайдера: "
        "pip install sentence-transformers numpy"
    )

from docstoolkit.embeddings.base import EmbeddingProvider


DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


class SentenceTransformersProvider(EmbeddingProvider):
    name = "sentence-transformers"

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model_name = model
        self._model = SentenceTransformer(model)
        self.dim = self._model.get_sentence_embedding_dimension()

    def encode(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vecs = self._model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return vecs.tolist()

    def similarity(self, query_vec, doc_vecs):
        if not doc_vecs:
            return []
        q = np.array(query_vec)
        D = np.array(doc_vecs)
        # Cosine similarity (vectors уже нормализованы у MiniLM)
        q_norm = q / (np.linalg.norm(q) + 1e-12)
        D_norm = D / (np.linalg.norm(D, axis=1, keepdims=True) + 1e-12)
        scores = D_norm @ q_norm
        # Преобразуем [-1..1] → [0..1]
        return ((scores + 1.0) / 2.0).tolist()
