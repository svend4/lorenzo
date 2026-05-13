#!/usr/bin/env python3
"""
Lorenzo Gateway — OpenAI-compatible HTTP gateway for Svyazi 2.0.

Любой AI-агент подключается к базе знаний Lorenzo по стандартному OpenAI-протоколу:
  - читает корпус (2461 карточек, hybrid BM25+TF-IDF поиск)
  - обогащает его (добавляет новые карточки через POST /api/cards)
  - вызывает инструменты через function calling

Ключевое отличие от DAF-gateway:
  - поиск — наш hybrid_search() (pure Python, offline, без чёрных ящиков)
  - write-back — создание .md карточек прямо в docs/
  - без Redis, без Docker — одна команда: python scripts/gateway.py

Эндпоинты:
    POST /v1/chat/completions  — OpenAI API (с function calling + SSE streaming)
    POST /api/ask              — прямой RAG-запрос
    POST /api/cards            — добавить карточку (обогащение)
    GET  /api/status           — статистика корпуса
    GET  /api/health           — health check
    GET  /v1/models            — список моделей

Использование:
    pip install fastapi uvicorn
    python scripts/gateway.py
    # → http://localhost:8083

Подключение:
    curl -X POST http://localhost:8083/api/ask -H "Content-Type: application/json" \\
         -d '{"query": "агент с памятью консолидация"}'

    # OpenAI-compatible (Claude Desktop, Cursor, любой клиент):
    # base_url = "http://localhost:8083/v1"
    # model    = "lorenzo-gateway"

Опционально с LLM-синтезом:
    export ANTHROPIC_API_KEY=sk-ant-...
    python scripts/gateway.py
"""

import json
import math
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("Установите зависимости: pip install fastapi uvicorn pydantic")
    sys.exit(1)

# ANN-поиск через hnswlib (опционально — если индекс построен)
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from improve_ann_index import ann_search as _ann_search
    _ANN_AVAILABLE = True
except Exception:
    _ANN_AVAILABLE = False

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

# ── Приложение ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="Lorenzo Gateway",
    description="OpenAI-compatible gateway для Svyazi 2.0 knowledge corpus",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Индексы (lazy load, кэш в памяти) ──────────────────────────────────────

_INDEX: list[dict] | None = None
_PASSAGES: list[dict] | None = None


def _load_index() -> list[dict]:
    global _INDEX
    if _INDEX is None:
        p = DOCS / "search_index.json"
        _INDEX = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    return _INDEX


def _load_passages() -> list[dict]:
    global _PASSAGES
    if _PASSAGES is None:
        p = DOCS / "passages.json"
        if p.exists():
            raw = json.loads(p.read_text(encoding="utf-8"))
            _PASSAGES = raw.get("passages", raw) if isinstance(raw, dict) else raw
        else:
            _PASSAGES = []
    return _PASSAGES


def _invalidate_index() -> None:
    global _INDEX
    _INDEX = None

# ── Поиск (полностью наш, без внешних зависимостей) ────────────────────────

def _tokenize(text: str) -> list[str]:
    return re.findall(r"[а-яёa-z0-9]+", text.lower())


def _tfidf_search(query: str, top_k: int = 10) -> list[dict]:
    docs = _load_index()
    tokens = set(_tokenize(query))
    scored: list[tuple[float, dict]] = []
    for d in docs:
        parts = [
            (d.get("title") or "") + " " + (d.get("title") or ""),  # двойной вес заголовка
            d.get("summary") or "",
            d.get("content") or "",
            " ".join(d.get("tags") or []),
        ]
        words = _tokenize(" ".join(parts))
        if not words:
            continue
        score = sum(words.count(t) for t in tokens) / len(words)
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


def _bm25_search(query: str, top_k: int = 10) -> list[dict]:
    passages = _load_passages()
    tokens = _tokenize(query)
    if not passages or not tokens:
        return []

    k1, b = 1.5, 0.75
    N = len(passages)
    avgdl = sum(len(_tokenize(p.get("text", ""))) for p in passages) / max(N, 1)

    idf: dict[str, float] = {}
    for t in set(tokens):
        df = sum(1 for p in passages if t in _tokenize(p.get("text", "")))
        idf[t] = math.log((N - df + 0.5) / (df + 0.5) + 1)

    scored: dict[str, float] = {}
    for p in passages:
        src = p.get("source", "")
        words = _tokenize(p.get("text", ""))
        dl = len(words)
        score = sum(
            idf.get(t, 0) * (words.count(t) * (k1 + 1))
            / (words.count(t) + k1 * (1 - b + b * dl / max(avgdl, 1)))
            for t in tokens
        )
        if score > 0:
            scored[src] = scored.get(src, 0) + score

    docs = _load_index()
    path_to_doc = {d.get("path", ""): d for d in docs}
    results: list[dict] = []
    for src, _ in sorted(scored.items(), key=lambda x: x[1], reverse=True):
        if src in path_to_doc:
            results.append(path_to_doc[src])
        if len(results) >= top_k:
            break
    return results


def hybrid_search(query: str, top_k: int = 10) -> list[dict]:
    """0.6×TF-IDF + 0.4×BM25 fusion — наш основной поиск."""
    tfidf = _tfidf_search(query, top_k * 2)
    bm25  = _bm25_search(query, top_k * 2)

    scores: dict[str, float] = {}
    for rank, d in enumerate(tfidf):
        p = d.get("path", "")
        scores[p] = scores.get(p, 0) + 0.6 * (1 / (rank + 1))
    for rank, d in enumerate(bm25):
        p = d.get("path", "")
        scores[p] = scores.get(p, 0) + 0.4 * (1 / (rank + 1))

    path_to_doc = {d.get("path", ""): d for d in _load_index()}
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [path_to_doc[p] for p, _ in ranked[:top_k] if p in path_to_doc]


def find_collabs(query: str, top_k: int = 5) -> list[dict]:
    """Jaccard similarity по файлам 05-habr-projects/."""
    project_dir = DOCS / "05-habr-projects"
    tokens = set(_tokenize(query))
    results: list[dict] = []
    for f in project_dir.rglob("*.md"):
        if f.name == "README.md":
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        words = set(_tokenize(text))
        sim = len(tokens & words) / len(tokens | words) if (tokens | words) else 0
        if sim > 0:
            results.append({
                "path":    str(f.relative_to(ROOT)),
                "title":   f.stem,
                "score":   round(sim, 4),
                "preview": text[:300],
            })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

# ── Инструменты (function calling) ─────────────────────────────────────────

TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": (
                "Поиск по базе знаний Lorenzo (2461 карточка, hybrid BM25+TF-IDF). "
                "Используй для любых вопросов о проектах, технологиях, архитектурах, авторах."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос (RU или EN)"},
                    "top_k": {"type": "integer", "description": "Число результатов (по умолч. 5)", "default": 5},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_card",
            "description": "Прочитать конкретный документ из базы знаний по пути.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь относительно корня репо, напр. docs/05-habr-projects/memory/yodoca.md",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_card",
            "description": (
                "Добавить новую карточку знаний в корпус (обогащение). "
                "Используй чтобы сохранить найденную информацию, вывод анализа, новый проект."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title":   {"type": "string", "description": "Заголовок карточки"},
                    "content": {"type": "string", "description": "Содержимое в Markdown"},
                    "section": {
                        "type": "string",
                        "description": "Раздел: 01-svyazi | 04-ai-collaborations | 05-habr-projects",
                        "default": "04-ai-collaborations",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Теги карточки",
                    },
                },
                "required": ["title", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_collabs",
            "description": "Найти кандидатов на коллаборацию среди Хабр-проектов.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Описание того, что ищешь"},
                    "top_k": {"type": "integer", "description": "Число кандидатов (по умолч. 5)", "default": 5},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_contacts",
            "description": "Получить контактную информацию и открытое письмо для автора проекта.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Название проекта или хендл автора (yodoca, kksudo, agentfs…)",
                    },
                },
                "required": ["project"],
            },
        },
    },
]

# ── Выполнение инструментов ─────────────────────────────────────────────────

def _exec_search(args: dict) -> str:
    results = hybrid_search(args["query"], int(args.get("top_k", 5)))
    if not results:
        return "Ничего не найдено."
    lines = [f"Найдено {len(results)} результатов для: «{args['query']}»\n"]
    for i, r in enumerate(results, 1):
        title   = r.get("title") or Path(r.get("path", "?")).stem
        summary = r.get("summary") or (r.get("content") or "")[:200]
        lines += [f"{i}. **{title}**", f"   Путь: {r.get('path', '')}", f"   {summary}", ""]
    return "\n".join(lines)


def _exec_get_card(args: dict) -> str:
    path = ROOT / args["path"]
    if not path.exists():
        results = hybrid_search(Path(args["path"]).stem, 1)
        if results:
            path = ROOT / results[0]["path"]
        else:
            return f"Карточка не найдена: {args['path']}"
    return path.read_text(encoding="utf-8", errors="ignore")[:5000]


def _cosine_sim(a: str, b: str) -> float:
    """Простое косинусное сходство двух строк по TF-весам."""
    def tf(text: str) -> dict:
        words = _tokenize(text)
        freq: dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return freq
    fa, fb = tf(a), tf(b)
    keys = set(fa) | set(fb)
    dot = sum(fa.get(k, 0) * fb.get(k, 0) for k in keys)
    na  = sum(v * v for v in fa.values()) ** 0.5
    nb  = sum(v * v for v in fb.values()) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def _find_duplicate(title: str, content: str, threshold: float = 0.85) -> dict | None:
    """Проверить, есть ли уже карточка с похожим содержимым."""
    query_text = f"{title} {content[:500]}"
    for doc in _load_index()[:200]:  # проверяем топ по заголовку
        existing = f"{doc.get('title', '')} {(doc.get('content') or doc.get('preview', ''))[:500]}"
        if _cosine_sim(query_text, existing) >= threshold:
            return doc
    return None


def _sync_passages(filepath: "Path") -> None:
    """Добавить абзацы нового файла в passages.json без полной пересборки."""
    import math
    passages_path = DOCS / "passages.json"
    try:
        text = filepath.read_text(encoding="utf-8")
        rel  = str(filepath.relative_to(ROOT))
        # Разбить на абзацы (≥ 5 слов)
        new_passages = []
        for para in re.split(r"\n{2,}", text):
            para = para.strip()
            words = _tokenize(para)
            if len(words) >= 5:
                new_passages.append({
                    "file": rel,
                    "text": para[:800],
                    "wc":   len(words),
                    "tokens": words,
                })
        if not new_passages:
            return
        # Загрузить существующие passages
        if passages_path.exists():
            raw = json.loads(passages_path.read_text(encoding="utf-8"))
            existing = raw.get("passages", raw) if isinstance(raw, dict) else raw
        else:
            existing = []
        combined = existing + new_passages
        # Пересчитать BM25-индекс
        N    = len(combined)
        avgdl = sum(p["wc"] for p in combined) / max(N, 1)
        df: dict[str, int] = {}
        for p in combined:
            for t in set(p["tokens"]):
                df[t] = df.get(t, 0) + 1
        idf = {t: math.log((N - n + 0.5) / (n + 0.5) + 1) for t, n in df.items()}
        passages_path.write_text(
            json.dumps({"passages": combined, "idf": idf, "avgdl": avgdl, "N": N},
                       ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass


def _exec_add_card(args: dict) -> str:
    title   = args["title"]
    content = args["content"]
    section = args.get("section", "04-ai-collaborations")
    tags    = args.get("tags") or []

    # Дедупликация: проверить наличие похожей карточки
    dup = _find_duplicate(title, content)
    if dup:
        return (
            f"Дубль найден (сходство ≥ 0.85): **{dup.get('title', '?')}**\n"
            f"Путь: {dup.get('path', '?')}\n"
            f"Карточка не создана. Используйте существующую или передайте уникальный контент."
        )

    slug       = re.sub(r"[^a-zа-яё0-9]+", "-", title.lower()).strip("-")[:50]
    target_dir = DOCS / section
    target_dir.mkdir(parents=True, exist_ok=True)

    now      = datetime.now()
    date     = now.strftime("%Y-%m-%d")
    written_at = now.strftime("%Y-%m-%dT%H:%M:%S")
    tags_str = ", ".join(tags)
    preview  = content[:200].replace("\n", " ")

    md = f"""---
title: {title}
date: {date}
tags: [{tags_str}]
source: gateway
state: raw
write_type: episode
written_by: gateway
written_at: {written_at}
---

# {title}

<!-- summary -->
> {preview}

<!-- tags: {tags_str} -->

{content}

---
_Добавлено через Lorenzo Gateway: {date}_
"""
    filepath = target_dir / f"{slug}.md"
    filepath.write_text(md, encoding="utf-8")

    # 1. Обновить search_index.json
    try:
        import subprocess
        subprocess.run(
            ["python3", str(SCRIPTS / "improve_index_update.py")],
            cwd=ROOT, capture_output=True, timeout=30,
        )
    except Exception:
        pass
    _invalidate_index()

    # 2. Синхронизировать passages.json (BM25)
    _sync_passages(filepath)

    return (
        f"✅ Карточка создана: {filepath.relative_to(ROOT)}\n"
        f"Заголовок: {title}\nТеги: {tags_str}\n"
        f"Статус: raw (используйте Review Queue для одобрения)"
    )


def _exec_find_collabs(args: dict) -> str:
    results = find_collabs(args["query"], int(args.get("top_k", 5)))
    if not results:
        return "Кандидаты на коллаборацию не найдены."
    lines = [f"Кандидаты для: «{args['query']}»\n"]
    for i, r in enumerate(results, 1):
        lines += [
            f"{i}. **{r['title']}** (score: {r['score']})",
            f"   {r['path']}",
            f"   {r['preview'][:150]}",
            "",
        ]
    return "\n".join(lines)


def _exec_get_contacts(args: dict) -> str:
    project = args["project"].lower()
    for folder in [DOCS / "letters", DOCS / "contacts"]:
        if folder.exists():
            for f in folder.glob("*.md"):
                if project in f.name.lower() or project in f.read_text(encoding="utf-8", errors="ignore").lower()[:500]:
                    return f.read_text(encoding="utf-8", errors="ignore")[:3000]
    results = hybrid_search(f"контакт {project} автор", 3)
    if results:
        lines = [f"Связанные карточки для «{project}»:"]
        for r in results:
            lines.append(f"- {r.get('path')}: {r.get('title')}")
        return "\n".join(lines)
    return f"Контакты не найдены для: {project}"


def dispatch_tool(name: str, args: dict) -> str:
    dispatch = {
        "search":       _exec_search,
        "get_card":     _exec_get_card,
        "add_card":     _exec_add_card,
        "find_collabs": _exec_find_collabs,
        "get_contacts": _exec_get_contacts,
    }
    fn = dispatch.get(name)
    return fn(args) if fn else f"Неизвестный инструмент: {name}"

# ── Pydantic-модели ─────────────────────────────────────────────────────────

class Message(BaseModel):
    role:         str
    content:      Any    = None
    tool_calls:   list   | None = None
    tool_call_id: str    | None = None
    name:         str    | None = None


class ChatRequest(BaseModel):
    model:       str   = "lorenzo-gateway"
    messages:    list[Message]
    tools:       list  | None = None
    tool_choice: Any          = "auto"
    max_tokens:  int          = 4096
    temperature: float        = 0.7
    stream:      bool         = False


class AskRequest(BaseModel):
    query:  str
    top_k:  int = 10
    mode:   str = "hybrid"    # hybrid | ann | tfidf | bm25


class CardRequest(BaseModel):
    title:   str
    content: str
    section: str       = "04-ai-collaborations"
    tags:    list[str] = []


class CollabRequest(BaseModel):
    query: str
    top_k: int = 5

# ── Вспомогательные функции ─────────────────────────────────────────────────

def _extract_user_text(messages: list[Message]) -> str:
    for m in reversed(messages):
        if m.role == "user":
            c = m.content
            if isinstance(c, list):
                return " ".join(
                    item.get("text", "") if isinstance(item, dict) else str(item)
                    for item in c
                )
            return str(c or "")
    return ""


def _intent(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["коллаб", "партнёр", "collab", "partner", "совместн"]):
        return "find_collabs"
    if any(w in t for w in ["контакт", "автор", "написать", "contact", "letter", "письм"]):
        return "get_contacts"
    if any(w in t for w in ["добавь", "запиши", "сохрани", "add card", "enrich", "обогати"]):
        return "add_card"
    return "search"


def _rag_answer(query: str, top_k: int = 8) -> str:
    """RAG без LLM — возвращает контекст из корпуса."""
    results = hybrid_search(query, top_k)
    if not results:
        return "По запросу ничего не найдено в базе знаний Lorenzo."
    lines = [f"**Результаты поиска по базе знаний** для: «{query}»\n"]
    for i, r in enumerate(results, 1):
        title   = r.get("title") or Path(r.get("path", "?")).stem
        summary = r.get("summary") or (r.get("content") or "")[:300]
        lines += [f"**{i}. {title}**", f"`{r.get('path', '')}`", summary, ""]
    return "\n".join(lines)


def _llm_answer(query: str, context: str) -> str | None:
    """Опциональный синтез через Claude (если есть ANTHROPIC_API_KEY)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=(
                "Ты — Lorenzo, ассистент по базе знаний Svyazi 2.0. "
                "Отвечай кратко и по делу, опираясь на предоставленный контекст. "
                "Если ответа нет в контексте — честно скажи об этом."
            ),
            messages=[{
                "role": "user",
                "content": f"Контекст из базы знаний:\n\n{context}\n\nВопрос: {query}",
            }],
        )
        return resp.content[0].text
    except Exception:
        return None


def _openai_response(t0: float, model: str, content: str, finish: str = "stop") -> dict:
    return {
        "id":      f"chatcmpl-{int(t0 * 1000)}",
        "object":  "chat.completion",
        "created": int(t0),
        "model":   model,
        "choices": [{
            "index":   0,
            "message": {"role": "assistant", "content": content},
            "finish_reason": finish,
        }],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "_meta":  {"latency_s": round(time.time() - t0, 3)},
    }


def _stream_response(t0: float, model: str, content: str):
    """Generator yielding OpenAI-compatible SSE chunks."""
    import asyncio
    chunk_id = f"chatcmpl-{int(t0 * 1000)}"
    created  = int(t0)
    words    = content.split(" ")
    # Role chunk first
    yield "data: " + json.dumps({
        "id": chunk_id, "object": "chat.completion.chunk", "created": created,
        "model": model,
        "choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}, "finish_reason": None}],
    }, ensure_ascii=False) + "\n\n"
    # Content chunks — word by word
    for i, word in enumerate(words):
        piece = word if i == 0 else " " + word
        yield "data: " + json.dumps({
            "id": chunk_id, "object": "chat.completion.chunk", "created": created,
            "model": model,
            "choices": [{"index": 0, "delta": {"content": piece}, "finish_reason": None}],
        }, ensure_ascii=False) + "\n\n"
    # Stop chunk
    yield "data: " + json.dumps({
        "id": chunk_id, "object": "chat.completion.chunk", "created": created,
        "model": model,
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        "_meta": {"latency_s": round(time.time() - t0, 3)},
    }, ensure_ascii=False) + "\n\n"
    yield "data: [DONE]\n\n"


def _openai_tool_call(t0: float, model: str, tool_name: str, tool_args: dict) -> dict:
    return {
        "id":      f"chatcmpl-{int(t0 * 1000)}",
        "object":  "chat.completion",
        "created": int(t0),
        "model":   model,
        "choices": [{
            "index": 0,
            "message": {
                "role":    "assistant",
                "content": None,
                "tool_calls": [{
                    "id":       f"call_{int(t0 * 1000)}",
                    "type":     "function",
                    "function": {
                        "name":      tool_name,
                        "arguments": json.dumps(tool_args, ensure_ascii=False),
                    },
                }],
            },
            "finish_reason": "tool_calls",
        }],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }

# ── Эндпоинты ───────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {
        "status":   "ok",
        "cards":    len(_load_index()),
        "passages": len(_load_passages()),
        "version":  "1.0.0",
        "corpus":   "Lorenzo / Svyazi 2.0",
        "llm":      bool(os.environ.get("ANTHROPIC_API_KEY")),
    }


_NOISE_SECTIONS = frozenset({
    "obsidian", "confluence", "autofilled", "badges",
    "nautilus", "habr-unique-projects", "svyazi-2-0",
    "ai-collaborations", "anthropic-vacancies",
    "technology-combinations", "lorenzo-agent", "meta-scripting",
    "processing-guide",
})


@app.get("/api/status")
async def status():
    idx = _load_index()
    sections: dict[str, int] = {}
    noise_cards = 0
    for d in idx:
        sec = d.get("section", "other")
        if sec in _NOISE_SECTIONS:
            noise_cards += 1
        else:
            sections[sec] = sections.get(sec, 0) + 1
    return {
        "total_cards":    len(idx),
        "core_cards":     len(idx) - noise_cards,
        "total_passages": len(_load_passages()),
        "sections":       sections,
        "tools":          [t["function"]["name"] for t in TOOLS],
        "llm_enabled":    bool(os.environ.get("ANTHROPIC_API_KEY")),
        "ann_enabled":    _ANN_AVAILABLE,
        "search_modes":   ["hybrid", "ann"] if _ANN_AVAILABLE else ["hybrid"],
    }


@app.get("/api/benchmark")
async def benchmark():
    """Метрики PROTOTYPE_SPEC §8 — все 5 критериев успеха."""
    import re as _re

    idx     = _load_index()
    cards   = len(idx)

    # Orphan rate из ORPHANS.md
    orphan_rate = 0.0
    orphans_file = DOCS / "ORPHANS.md"
    if orphans_file.exists():
        m = _re.search(r'изолированных:\s*(\d+)', orphans_file.read_text(encoding="utf-8"))
        if m:
            isolated = int(m.group(1))
            orphan_rate = isolated / cards if cards else 0.0

    # Hit Rate@10 из PRECISION_EVAL.md (pre-computed)
    hit_rate = None
    prec_file = DOCS / "PRECISION_EVAL.md"
    if prec_file.exists():
        m = _re.search(r'Hit Rate@\d+\s*\|\s*\*\*([\d.]+)\*\*', prec_file.read_text(encoding="utf-8"))
        if m:
            hit_rate = float(m.group(1))

    # Latency — одиночный запрос
    t0      = __import__("time").time()
    hybrid_search("агент память консолидация", 5)
    latency = round(__import__("time").time() - t0, 3)

    criteria = {
        "latency_s":    {"value": latency,    "threshold": "≤5.0s",  "pass": latency <= 5.0},
        "cards":        {"value": cards,      "threshold": "≥500",   "pass": cards >= 500},
        "orphan_rate":  {"value": orphan_rate,"threshold": "≤0.15",  "pass": orphan_rate <= 0.15},
        "hit_rate_10":  {"value": hit_rate,   "threshold": "≥0.70",  "pass": hit_rate is not None and hit_rate >= 0.70},
    }
    all_pass = all(v["pass"] for v in criteria.values())
    return {"criteria": criteria, "all_pass": all_pass, "spec": "PROTOTYPE_SPEC §8"}


@app.post("/api/ask")
async def ask(req: AskRequest):
    """Прямой RAG-запрос. Возвращает результаты + контекст + опционально LLM-ответ.

    mode=hybrid (по умолч.) — BM25 + TF-IDF, ~210мс, Recall 1.0
    mode=ann               — HNSW + точный re-rank, ~5мс, Recall 0.42 (нужен --build)
    """
    t0 = time.time()
    if req.mode == "ann" and _ANN_AVAILABLE:
        results = _ann_search(req.query, req.top_k)
        search_mode = "ann"
    else:
        results = hybrid_search(req.query, req.top_k)
        search_mode = "hybrid"
    context = "\n\n".join(
        f"### {r.get('title', r.get('path'))}\n{r.get('summary') or (r.get('content') or '')[:500]}"
        for r in results
    )
    answer = _llm_answer(req.query, context) or context
    return {
        "query":       req.query,
        "answer":      answer,
        "results":     results,
        "search_mode": search_mode,
        "ann_available": _ANN_AVAILABLE,
        "latency_s":   round(time.time() - t0, 3),
    }


@app.post("/api/search")
async def search_endpoint(req: AskRequest):
    """Лёгкий поиск — только список результатов без LLM-синтеза.

    Быстрее /api/ask: нет LLM-вызова, нет контекстной сборки.
    Подходит для автодополнения и инкрементального UI.
    """
    t0      = time.time()
    results = hybrid_search(req.query, req.top_k)
    return {
        "query":     req.query,
        "results":   results,
        "count":     len(results),
        "latency_s": round(time.time() - t0, 3),
    }


@app.post("/api/collabs")
async def collabs_endpoint(req: CollabRequest):
    """Поиск кандидатов коллаборации по запросу.

    Возвращает отсортированный список проектов из docs/05-habr-projects/
    с Jaccard-similarity score, автором и наличием письма.
    """
    t0      = time.time()
    results = find_collabs(req.query, req.top_k)
    return {
        "query":     req.query,
        "results":   results,
        "count":     len(results),
        "latency_s": round(time.time() - t0, 3),
    }


@app.post("/api/cards")
async def add_card_endpoint(req: CardRequest):
    """Добавить карточку в корпус (обогащение базы знаний)."""
    result = _exec_add_card(req.model_dump())
    return {"status": "created", "message": result}


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest):
    """
    OpenAI-совместимый эндпоинт.

    Поддерживает два режима:
    1. Без tools от клиента → gateway сам решает инструмент, выполняет, возвращает ответ.
    2. С tools от клиента → стандартный function-calling flow (возвращает tool_calls).
    """
    t0       = time.time()
    user_msg = _extract_user_text(req.messages)

    # ── Завершение multi-turn: клиент вернул результаты инструментов ──
    tool_results = [m for m in req.messages if m.role == "tool"]
    if tool_results:
        combined = "\n\n".join(str(m.content) for m in tool_results)
        answer   = _llm_answer(user_msg, combined) or f"Результат из базы знаний:\n\n{combined}"
        return _openai_response(t0, req.model, answer)

    intent    = _intent(user_msg)
    has_tools = req.tools is not None  # клиент передал свои определения инструментов

    # ── Режим 2: клиент управляет function calling ─────────────────────────
    if has_tools:
        tool_args: dict[str, Any] = {"query": user_msg}
        if intent == "find_collabs":
            return _openai_tool_call(t0, req.model, "find_collabs", tool_args)
        if intent == "get_contacts":
            tool_args = {"project": user_msg}
            return _openai_tool_call(t0, req.model, "get_contacts", tool_args)
        return _openai_tool_call(t0, req.model, "search", tool_args)

    # ── Режим 1: gateway сам обрабатывает запрос ───────────────────────────
    if intent == "find_collabs":
        raw = _exec_find_collabs({"query": user_msg})
    elif intent == "get_contacts":
        raw = _exec_get_contacts({"project": user_msg})
    elif intent == "add_card":
        raw = _rag_answer(user_msg)
    else:
        raw = _rag_answer(user_msg)

    answer = _llm_answer(user_msg, raw) or raw

    if req.stream:
        return StreamingResponse(
            _stream_response(t0, req.model, answer),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
    return _openai_response(t0, req.model, answer)


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [{
            "id":          "lorenzo-gateway",
            "object":      "model",
            "created":     1748600000,
            "owned_by":    "svyazi",
            "description": "Lorenzo Knowledge OS — Svyazi 2.0 corpus gateway",
        }],
    }

# ── Точка входа ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Lorenzo Gateway — OpenAI-compatible knowledge server")
    parser.add_argument("--host",   default="0.0.0.0")
    parser.add_argument("--port",   type=int, default=8083)
    parser.add_argument("--reload", action="store_true", help="Авто-перезагрузка при изменении файлов")
    args = parser.parse_args()

    idx      = _load_index()
    passages = _load_passages()
    llm_mode = "с LLM-синтезом (Claude)" if os.environ.get("ANTHROPIC_API_KEY") else "RAG-only (без API-ключа)"

    print(f"""
╔═══════════════════════════════════════════════════════╗
║          Lorenzo Gateway v1.0  —  Svyazi 2.0          ║
╚═══════════════════════════════════════════════════════╝

  Корпус:   {len(idx)} карточек, {len(passages)} абзацев
  Режим:    {llm_mode}
  Адрес:    http://{args.host}:{args.port}

  Эндпоинты:
    POST /v1/chat/completions   OpenAI-compatible (function calling)
    POST /api/ask               Прямой RAG-запрос
    POST /api/cards             Добавить карточку (обогащение)
    GET  /api/status            Статистика корпуса
    GET  /api/health            Health check
    GET  /v1/models             Список моделей
    GET  /docs                  Swagger UI

  Инструменты: search, get_card, add_card, find_collabs, get_contacts

  Пример:
    curl -X POST http://localhost:{args.port}/api/ask \\
         -H "Content-Type: application/json" \\
         -d '{{"query": "агент с памятью консолидация"}}'
""")

    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)
