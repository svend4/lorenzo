"""Адаптеры для разных типов peer'ов."""
import json
import urllib.parse
import urllib.request
import urllib.error
from abc import ABC, abstractmethod


class Adapter(ABC):
    """Интерфейс адаптера к peer."""

    name: str = "base"

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Возвращает [{title, path, snippet, score}, ...]."""
        ...

    @abstractmethod
    def health(self) -> dict:
        """Health check."""
        ...


class HTTPAdapter(Adapter):
    """HTTP адаптер: ходит на peer's serve.py /api endpoints."""

    name = "http"

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get_json(self, path: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "docstoolkit-federation/0.1",
        })
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, json.JSONDecodeError) as e:
            return {"error": str(e)}

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        data = self._get_json("/search", {"q": query, "json": "1"})
        if "error" in data:
            return []
        results = data.get("results", [])
        return [
            {
                "title": r.get("title", ""),
                "path": r.get("path", ""),
                "snippet": r.get("preview", ""),
                "score": r.get("score", 0),
            }
            for r in results[:top_k]
        ]

    def health(self) -> dict:
        return self._get_json("/api/health")


class LocalAdapter(Adapter):
    """Адаптер к локальному корпусу (без HTTP)."""

    name = "local"

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        try:
            from docstoolkit.embeddings import get_provider
            from docstoolkit.config import load_config
            cfg = load_config()
            index_path = cfg.docs_dir / "search_index.json"
            if not index_path.exists():
                return []
            docs = json.loads(index_path.read_text(encoding="utf-8"))
            if isinstance(docs, dict):
                docs = docs.get("docs", [])
            prov = get_provider("tfidf")
            prov.fit([d.get("content", "") + " " + d.get("title", "")
                      for d in docs])
            results = prov.search(query, docs, top_k=top_k)
            return [
                {
                    "title": r.title,
                    "path": r.path,
                    "snippet": r.snippet[:200],
                    "score": r.score,
                }
                for r in results
            ]
        except Exception as e:
            return [{"error": str(e)}]

    def health(self) -> dict:
        try:
            from docstoolkit.config import load_config
            cfg = load_config()
            return {
                "ok": True,
                "root": str(cfg.root),
                "docs_dir": str(cfg.docs_dir),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}


class MockAdapter(Adapter):
    """Mock для тестов."""

    name = "mock"

    def __init__(self, results: list[dict] | None = None,
                 health_data: dict | None = None):
        self._results = results or []
        self._health = health_data or {"ok": True, "kind": "mock"}

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        return self._results[:top_k]

    def health(self) -> dict:
        return self._health


def make_adapter(peer) -> Adapter:
    """Factory: peer → adapter."""
    if peer.kind == "http":
        return HTTPAdapter(peer.url)
    if peer.kind == "local":
        return LocalAdapter()
    if peer.kind == "mock":
        return MockAdapter()
    return HTTPAdapter(peer.url)
