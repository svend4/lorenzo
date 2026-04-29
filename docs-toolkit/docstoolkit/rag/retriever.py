"""Retriever — поиск пассажей через embeddings."""
import json
from pathlib import Path

from docstoolkit.config import load_config
from docstoolkit.embeddings import get_provider, HybridSearcher
from docstoolkit.rag.types import Passage


class Retriever:
    """Wrapper над embeddings.search() с возвратом Passage."""

    def __init__(self, method: str = "hybrid", model: str = ""):
        self.method = method
        self.model = model
        self._docs = None
        self._keyword = None
        self._semantic = None
        self._hybrid = None

    def _load_docs(self) -> list[dict]:
        if self._docs is not None:
            return self._docs
        cfg = load_config()
        path = cfg.docs_dir / "search_index.json"
        if not path.exists():
            self._docs = []
            return self._docs
        data = json.loads(path.read_text(encoding="utf-8"))
        self._docs = data if isinstance(data, list) else data.get("docs", [])
        return self._docs

    def _get_keyword(self):
        if self._keyword is None:
            from docstoolkit.embeddings.tfidf import TFIDFProvider
            from docstoolkit.embeddings.cache import EmbeddingCache
            cfg = load_config()
            cache = EmbeddingCache(cfg.root / ".docstoolkit" / "cache" / "embeddings.sqlite")
            self._keyword = TFIDFProvider(cache=cache)
            if not self._keyword._fitted:
                docs = self._load_docs()
                self._keyword.fit([d.get("content", "") + " " + d.get("title", "")
                                   for d in docs])
        return self._keyword

    def _get_semantic(self):
        if self._semantic is None:
            try:
                self._semantic = get_provider("sentence-transformers", model=self.model)
            except (ImportError, TypeError):
                self._semantic = None
        return self._semantic

    def search(self, query: str, top_k: int = 5) -> list[Passage]:
        docs = self._load_docs()
        if not docs:
            return []

        if self.method == "keyword":
            results = self._get_keyword().search(query, docs, top_k=top_k)
        elif self.method == "semantic":
            sem = self._get_semantic()
            if sem is None:
                results = self._get_keyword().search(query, docs, top_k=top_k)
            else:
                results = sem.search(query, docs, top_k=top_k)
        else:  # hybrid (default)
            kw = self._get_keyword()
            sem = self._get_semantic()
            searcher = HybridSearcher(keyword=kw, semantic=sem)
            results = searcher.search(query, docs, top_k=top_k)

        return [
            Passage(
                text=r.snippet or "",
                doc_id=r.path or r.doc_id,
                title=r.title,
                score=r.score,
            )
            for r in results
        ]


def retrieve_passages(query: str, top_k: int = 5,
                      method: str = "hybrid") -> list[Passage]:
    """Удобная обёртка."""
    return Retriever(method=method).search(query, top_k=top_k)
