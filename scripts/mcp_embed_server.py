"""
mcp_embed_server.py — MCP-сервер lorenzo-embed.

Семантический и гибридный поиск через docs-toolkit/embeddings/.

Инструменты:
  semantic_search(query, top_k, model)  — sentence-transformers если установлен
  hybrid_search(query, top_k)           — RRF: keyword (TF-IDF) + semantic
  keyword_search(query, top_k)          — чистый TF-IDF baseline
  list_providers()                      — какие провайдеры доступны
  encode(text)                          — векторизация (для дебага)

Запуск:
  python scripts/mcp_embed_server.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(ROOT / "docs-toolkit"))

from mcp_common import build_server, run_stdio, ROOT, DOCS

try:
    from mcp.types import Tool, Resource, Prompt, PromptArgument
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore

# Импорт docs-toolkit embeddings (через vendoring)
try:
    from docstoolkit.embeddings import (
        get_provider, list_providers as _list_providers, HybridSearcher
    )
    _EMBEDDINGS_OK = True
except ImportError:
    _EMBEDDINGS_OK = False


_index_cache: list[dict] | None = None
_keyword_provider = None


def _load_index() -> list[dict]:
    global _index_cache
    if _index_cache is not None:
        return _index_cache
    path = DOCS / "search_index.json"
    if not path.exists():
        _index_cache = []
        return _index_cache
    data = json.loads(path.read_text(encoding="utf-8"))
    _index_cache = data if isinstance(data, list) else data.get("docs", [])
    return _index_cache


def _get_keyword():
    global _keyword_provider
    if _keyword_provider is not None:
        return _keyword_provider
    if not _EMBEDDINGS_OK:
        return None
    docs = _load_index()
    prov = get_provider("tfidf")
    prov.fit([(d.get("content", "") + " " + d.get("title", "")) for d in docs])
    _keyword_provider = prov
    return prov


def _format_results(results, query: str) -> str:
    if not results:
        return f"Ничего не найдено по «{query}»"
    lines = [f"Найдено {len(results)} результатов для «{query}»:\n"]
    for r in results:
        lines.append(f"**{r.title}** (score={r.score:.3f})")
        lines.append(f"`{r.path}`")
        if r.snippet:
            lines.append(f"> {r.snippet[:200]}…")
        lines.append("")
    return "\n".join(lines)


def tool_keyword_search(query: str, top_k: int = 10) -> str:
    if not query:
        return "❌ Укажите query."
    if not _EMBEDDINGS_OK:
        return "❌ docs-toolkit недоступен. PYTHONPATH должен включать docs-toolkit/"
    prov = _get_keyword()
    if not prov:
        return "❌ Не удалось инициализировать keyword провайдер"
    docs = _load_index()
    results = prov.search(query, docs, top_k=top_k)
    return _format_results(results, query)


def tool_semantic_search(query: str, top_k: int = 10,
                         model: str = "paraphrase-multilingual-MiniLM-L12-v2") -> str:
    if not query:
        return "❌ Укажите query."
    if not _EMBEDDINGS_OK:
        return "❌ docs-toolkit недоступен"
    try:
        prov = get_provider("sentence-transformers", model=model)
    except ImportError:
        return ("⚠️ sentence-transformers не установлен. "
                "pip install sentence-transformers")
    docs = _load_index()
    results = prov.search(query, docs, top_k=top_k)
    return _format_results(results, query)


def tool_hybrid_search(query: str, top_k: int = 10) -> str:
    if not query:
        return "❌ Укажите query."
    if not _EMBEDDINGS_OK:
        return "❌ docs-toolkit недоступен"
    keyword = _get_keyword()
    semantic = None
    try:
        semantic = get_provider("sentence-transformers")
    except ImportError:
        pass
    searcher = HybridSearcher(keyword=keyword, semantic=semantic)
    docs = _load_index()
    results = searcher.search(query, docs, top_k=top_k)
    method = "hybrid" if semantic else "keyword (semantic недоступен)"
    return f"_Метод: {method}_\n\n" + _format_results(results, query)


def tool_list_providers() -> str:
    if not _EMBEDDINGS_OK:
        return "❌ docs-toolkit недоступен"
    base = _list_providers()
    extra = []
    try:
        get_provider("sentence-transformers")
        extra.append("sentence-transformers (доступен)")
    except ImportError:
        extra.append("sentence-transformers (требует pip install)")
    return "## Embedding providers\n\n" + \
           "\n".join(f"- **{p}**" for p in base) + \
           "\n\n## Опциональные\n\n" + \
           "\n".join(f"- {e}" for e in extra)


def tool_encode(text: str) -> str:
    """Дебаг: показать вектор для текста."""
    if not _EMBEDDINGS_OK:
        return "❌ docs-toolkit недоступен"
    if not text:
        return "❌ Укажите text"
    prov = _get_keyword()
    if not prov:
        return "❌ Провайдер недоступен"
    vec = prov.encode([text])[0]
    if isinstance(vec, dict):
        # Sparse — топ-10 токенов
        items = sorted(vec.items(), key=lambda x: -x[1])[:10]
        lines = [f"Sparse vector ({len(vec)} non-zero):"]
        for token, weight in items:
            lines.append(f"  {token:20s} {weight:.4f}")
        return "\n".join(lines)
    else:
        return f"Dense vector dim={len(vec)}, norm={sum(v*v for v in vec)**0.5:.3f}\nFirst 8: {vec[:8]}"


def dispatch(name: str, args: dict) -> str:
    if name == "keyword_search":
        return tool_keyword_search(args.get("query", ""), args.get("top_k", 10))
    if name == "semantic_search":
        return tool_semantic_search(
            args.get("query", ""), args.get("top_k", 10),
            args.get("model", "paraphrase-multilingual-MiniLM-L12-v2"))
    if name == "hybrid_search":
        return tool_hybrid_search(args.get("query", ""), args.get("top_k", 10))
    if name == "list_providers":
        return tool_list_providers()
    if name == "encode":
        return tool_encode(args.get("text", ""))
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(
        name="keyword_search",
        description="TF-IDF поиск по корпусу (быстрый baseline).",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="semantic_search",
        description="Семантический поиск через sentence-transformers (нужен pip install).",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer", "default": 10},
                "model": {"type": "string",
                          "default": "paraphrase-multilingual-MiniLM-L12-v2"},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="hybrid_search",
        description="Гибридный RRF поиск (keyword + semantic, fallback на keyword если semantic недоступен).",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "top_k": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="list_providers",
        description="Список доступных embedding-провайдеров.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="encode",
        description="Вектор для текста (debug).",
        inputSchema={
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    ),
]


PROMPTS = [
    Prompt(
        name="lorenzo-deep-search",
        description="Полный гибридный поиск с пояснением scores",
        arguments=[PromptArgument(name="query", required=True)],
    ),
]


def get_prompt(name: str, args: dict) -> str:
    if name == "lorenzo-deep-search":
        q = args.get("query", "")
        return (
            f"1. Вызови `keyword_search` с query='{q}' top_k=10. "
            f"2. Вызови `semantic_search` с query='{q}' top_k=10 (если доступно). "
            f"3. Вызови `hybrid_search` с query='{q}' top_k=10. "
            f"4. Сравни топ-3 от каждого метода — где совпадения, где расхождения. "
            f"5. Объясни, какой метод сработал лучше для этого запроса."
        )
    return f"Промпт {name} не определён."


if __name__ == "__main__":
    server = build_server(
        "lorenzo-embed", TOOLS, dispatch,
        prompts_spec=PROMPTS, prompt_getter=get_prompt,
    )
    run_stdio(server)
