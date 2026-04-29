"""Реестр handler'ов для job queue.

Handler — функция (args: dict, progress_cb: callable) → result dict.
"""
from typing import Callable


HANDLERS: dict[str, Callable] = {}


def register_handler(name: str, fn: Callable):
    """Регистрация handler'а."""
    HANDLERS[name] = fn


# ----- Built-in handlers -----

def _index_build_handler(args: dict, progress_cb=None) -> dict:
    """Полный rebuild embeddings cache."""
    from docstoolkit.embeddings import get_provider
    from docstoolkit.embeddings.cache import EmbeddingCache
    from docstoolkit.config import load_config
    import json

    cfg = load_config()
    cache = EmbeddingCache(cfg.root / ".docstoolkit" / "cache" / "embeddings.sqlite")
    provider_name = args.get("provider", "tfidf")

    cache.invalidate(provider_name)

    if provider_name == "sentence-transformers":
        prov = get_provider("sentence-transformers", model=args.get("model", ""))
    else:
        from docstoolkit.embeddings.tfidf import TFIDFProvider
        prov = TFIDFProvider(cache=cache)

    index_path = cfg.docs_dir / "search_index.json"
    if not index_path.exists():
        return {"error": "search_index.json not found", "vectors": 0}

    docs = json.loads(index_path.read_text(encoding="utf-8"))
    if isinstance(docs, dict):
        docs = docs.get("docs", [])

    if provider_name == "tfidf":
        prov.fit([d.get("content", "") + " " + d.get("title", "") for d in docs],
                 force=True)
        if progress_cb:
            progress_cb(20, f"IDF computed ({len(prov._idf)} tokens)")

    n = len(docs)
    saved = 0
    for i, d in enumerate(docs):
        text = d.get("content", "") + " " + d.get("title", "")
        if not text.strip():
            continue
        doc_id = d.get("path", "")
        if not doc_id:
            continue
        vec = prov.encode([text])[0]
        cache.save_vector(provider_name, doc_id, text, vec,
                          dim=len(vec) if isinstance(vec, list) else 0)
        saved += 1
        if progress_cb and i % 50 == 0:
            pct = 20 + int(80 * i / n)
            progress_cb(pct, f"{saved}/{n} vectorized")

    cache.close()
    return {"provider": provider_name, "vectors": saved, "docs_total": n}


def _ingest_dir_handler(args: dict, progress_cb=None) -> dict:
    """Ингестия целой директории."""
    from docstoolkit.ingest import ingest_dir
    from pathlib import Path
    path = Path(args["path"])
    output_dir = Path(args.get("output", path / "_ingested"))
    output_dir.mkdir(parents=True, exist_ok=True)

    docs = ingest_dir(path, recursive=args.get("recursive", True))
    saved = 0
    for i, doc in enumerate(docs):
        slug = doc.source.path.stem
        target = output_dir / f"{slug}.md"
        target.write_text(doc.to_markdown(), encoding="utf-8")
        saved += 1
        if progress_cb and i % 5 == 0:
            pct = int(100 * i / max(len(docs), 1))
            progress_cb(pct, f"{saved}/{len(docs)} ingested")

    return {"path": str(path), "saved": saved, "total": len(docs)}


def _rag_batch_handler(args: dict, progress_cb=None) -> dict:
    """Batch RAG: список вопросов → список ответов."""
    from docstoolkit.rag import ask
    questions = args.get("questions", [])
    method = args.get("method", "hybrid")
    answerer = args.get("answerer", "echo")
    top_k = args.get("top_k", 5)

    answers = []
    for i, q in enumerate(questions):
        result = ask(q, top_k=top_k, method=method, answerer=answerer)
        answers.append({
            "question": q,
            "answer": result.answer,
            "citations": result.citations,
            "duration_ms": result.duration_ms,
        })
        if progress_cb:
            pct = int(100 * (i + 1) / len(questions))
            progress_cb(pct, f"{i+1}/{len(questions)}")

    return {"answered": len(answers), "answers": answers}


# Регистрация
register_handler("index_build", _index_build_handler)
register_handler("ingest_dir", _ingest_dir_handler)
register_handler("rag_batch", _rag_batch_handler)
