"""
mcp_server.py — MCP-сервер Lorenzo: инструменты для работы с базой знаний.
Stage 5: постоянный сервис, доступный любому MCP-совместимому LLM-агенту.

Инструменты:
  search_docs(query)              — полнотекстовый поиск по search_index.json
  bm25_search(query)              — BM25-поиск по абзацам (passages.json)
  get_decisions(topic)            — решения по теме из DECISIONS.md
  get_contacts(project)           — контакты авторов из CONTACTS.md
  get_project_status(name)        — теги, упоминания, связи проекта
  run_improve(script, dry_run)    — запустить скрипт обработки
  run_recipe(name, dry_run)       — запустить именованный рецепт (improve_recipe.py)
  list_recipes()                  — список рецептов с описаниями
  get_health()                    — общий балл здоровья репозитория
  list_scripts()                  — список доступных скриптов
  update_contact_status(author, status, note) — обновить статус контакта

Установка:
  pip install mcp

Запуск (stdio режим для Claude Desktop):
  python scripts/mcp_server.py

Конфигурация для Claude Desktop (~/.claude/claude_desktop_config.json):
  {
    "mcpServers": {
      "lorenzo": {
        "command": "python",
        "args": ["/path/to/lorenzo/scripts/mcp_server.py"],
        "env": {}
      }
    }
  }
"""
import re
import sys
import json
import subprocess
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

# ---------------------------------------------------------------------------
# Утилиты: чтение данных из docs/
# ---------------------------------------------------------------------------

def _load_index() -> list[dict]:
    path = DOCS / "search_index.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("docs", [])


def _tokenize(text: str) -> list[str]:
    words = re.findall(r'[а-яёa-z][а-яёa-z\-]{1,}', text.lower())
    stop = {"и", "в", "на", "что", "как", "это", "для", "или", "но",
            "the", "a", "an", "of", "in", "to", "is", "are", "for"}
    return [w for w in words if w not in stop]


def _doc_text(doc: dict) -> str:
    """search_index.json uses 'content' (new) or 'preview' (old) — 356/460 files
    have empty 'content' but populated 'preview'. Use the best available field."""
    return " ".join(filter(None, [
        doc.get("content", ""),
        doc.get("preview", ""),
        doc.get("summary", ""),
    ]))


def _search(query: str, top_k: int = 8) -> list[dict]:
    index = _load_index()
    tokens = _tokenize(query)
    scored = []
    for doc in index:
        body  = _doc_text(doc).lower()
        title = doc.get("title", "").lower()
        path  = doc.get("path", "").lower()
        tags  = " ".join(doc.get("tags", [])).lower()

        score = 0.0
        for t in tokens:
            if t in title: score += 5.0 + title.count(t) * 0.5
            if t in path:  score += 3.0
            if t in tags:  score += 2.0
            if t in body:  score += 1.0 + body.count(t) * 0.05

        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


def _extract_section(text: str, keyword: str, lines_after: int = 30) -> str:
    keyword_lower = keyword.lower()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if keyword_lower in line.lower():
            return "\n".join(lines[i:i + lines_after])
    return ""


def _read_doc(filename: str) -> str:
    path = DOCS / filename
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _list_improve_scripts() -> list[str]:
    return sorted(p.name for p in SCRIPTS.glob("improve_*.py"))


# ---------------------------------------------------------------------------
# BM25 поиск по абзацам (passages.json)
# ---------------------------------------------------------------------------

import math
from collections import Counter, defaultdict

_PASSAGES_CACHE: list[dict] | None = None
_BM25_CACHE: dict | None = None


def _load_passages() -> list[dict]:
    global _PASSAGES_CACHE
    if _PASSAGES_CACHE is not None:
        return _PASSAGES_CACHE
    path = DOCS / "passages.json"
    if not path.exists():
        _PASSAGES_CACHE = []
        return _PASSAGES_CACHE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        # passages.json может быть списком или {"passages": [...], "generated": ...}
        items: list[dict] = raw if isinstance(raw, list) else raw.get("passages", [])
        stop = {"и","в","не","на","с","по","к","из","за","для","это","как","но","или",
                "что","был","его","её","их","мы","вы","при","от","до","об",
                "the","a","an","is","of","in","on","to","for","with","by","and","not"}
        for p in items:
            # Нормализуем поле file/source
            if "file" not in p:
                p["file"] = p.get("source", p.get("id", "").split("::")[0])
            if "tokens" not in p:
                text = re.sub(r'```.*?```', ' ', p.get("text",""), flags=re.DOTALL)
                text = re.sub(r'[*_`#|>\[\]()]', ' ', text)
                p["tokens"] = [t for t in re.findall(r'[а-яёa-z]{3,}', text.lower())
                               if t not in stop]
        _PASSAGES_CACHE = items
    except Exception:
        _PASSAGES_CACHE = []
    return _PASSAGES_CACHE


def _build_bm25_index(passages: list[dict]) -> dict:
    global _BM25_CACHE
    if _BM25_CACHE is not None:
        return _BM25_CACHE
    N = len(passages)
    df: Counter = Counter()
    total_len = 0
    for p in passages:
        total_len += len(p["tokens"])
        for t in set(p["tokens"]):
            df[t] += 1
    avgdl = total_len / max(N, 1)
    idf = {t: math.log((N - n + 0.5) / (n + 0.5) + 1) for t, n in df.items()}
    inv: dict = defaultdict(list)
    for i, p in enumerate(passages):
        freq = Counter(p["tokens"])
        for t, tf in freq.items():
            inv[t].append((i, tf))
    _BM25_CACHE = {"idf": idf, "inv": dict(inv), "avgdl": avgdl,
                   "lens": [len(p["tokens"]) for p in passages]}
    return _BM25_CACHE


def _bm25_search(query: str, top: int = 8) -> list[dict]:
    passages = _load_passages()
    if not passages:
        return []
    bm25 = _build_bm25_index(passages)
    stop = {"и","в","не","на","с","по","к","из","за","для","это","как","но","или",
            "the","a","an","is","of","in","on","to","for","with","by","and","not"}
    tokens = [t for t in re.findall(r'[а-яёa-z]{3,}', query.lower()) if t not in stop]
    if not tokens:
        return []
    k1, b = 1.5, 0.75
    avgdl = bm25["avgdl"]
    scores: dict[int, float] = defaultdict(float)
    for t in tokens:
        idf = bm25["idf"].get(t, 0)
        for did, tf in bm25["inv"].get(t, []):
            dl = bm25["lens"][did]
            norm_tf = tf * (k1 + 1) / (tf + k1 * (1 - b + b * dl / avgdl))
            scores[did] += idf * norm_tf

    best_by_file: dict[str, tuple[float, dict]] = {}
    for did, score in sorted(scores.items(), key=lambda x: -x[1]):
        p = passages[did]
        fname = p["file"]
        if fname not in best_by_file or score > best_by_file[fname][0]:
            best_by_file[fname] = (score, p)

    results = sorted(best_by_file.values(), key=lambda x: -x[0])[:top]
    return [{"score": round(s, 2), **p} for s, p in results]


# ---------------------------------------------------------------------------
# Рецепты (improve_recipe.py)
# ---------------------------------------------------------------------------

def _load_recipes() -> dict:
    recipe_script = SCRIPTS / "improve_recipe.py"
    if not recipe_script.exists():
        return {}
    try:
        result = subprocess.run(
            [sys.executable, str(recipe_script), "--list"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=10
        )
        return {"_raw_list": result.stdout}
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# MCP сервер
# ---------------------------------------------------------------------------

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
    import asyncio
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

if not MCP_AVAILABLE:
    print("MCP не установлен. Запустите: pip install mcp", file=sys.stderr)
    print("\nДоступные инструменты (демо-режим):", file=sys.stderr)
    print("  search_docs, get_decisions, get_contacts,", file=sys.stderr)
    print("  get_project_status, run_improve, get_health, list_scripts", file=sys.stderr)
    sys.exit(1)

server = Server("lorenzo-knowledge")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_docs",
            description="Полнотекстовый поиск по всем документам Lorenzo. "
                        "Возвращает топ-8 релевантных файлов с выдержками.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос"},
                    "top_k": {"type": "integer", "default": 5, "description": "Число результатов"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_decisions",
            description="Возвращает ключевые решения по теме из DECISIONS.md.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Тема: архитектура, память, RAG, и т.п."},
                },
                "required": ["topic"],
            },
        ),
        Tool(
            name="get_contacts",
            description="Контакты авторов проектов из CONTACTS.md. "
                        "project — название проекта или слой (memory, rag, orchestration).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Проект или слой"},
                },
                "required": ["project"],
            },
        ),
        Tool(
            name="get_project_status",
            description="Статус проекта: теги, число упоминаний, похожие документы, контакт.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Название проекта (Yodoca, NGT, AgentFS...)"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="run_improve",
            description="Запустить скрипт обработки документов. "
                        "По умолчанию dry_run=true — не меняет файлы, только показывает план.",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {"type": "string", "description": "Имя скрипта (improve_metrics.py)"},
                    "dry_run": {"type": "boolean", "default": True},
                },
                "required": ["script"],
            },
        ),
        Tool(
            name="get_health",
            description="Общий балл здоровья репозитория из HEALTH.md и SCORING.md.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_scripts",
            description="Список всех доступных скриптов обработки (improve_*.py).",
            inputSchema={
                "type": "object",
                "properties": {
                    "group": {
                        "type": "string",
                        "description": "Фильтр по группе: structure, index, analysis, extract, quality, graph, reports, export, llm",
                        "enum": ["structure", "index", "analysis", "extract",
                                 "quality", "graph", "reports", "export", "llm", "all"],
                    },
                },
            },
        ),
        Tool(
            name="bm25_search",
            description=(
                "BM25-поиск по абзацам документов Lorenzo (passages.json). "
                "Точнее чем search_docs для конкретных понятий и проектов. "
                "Требует предварительного запуска improve_passage_retrieval.py --index."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос"},
                    "top_k": {"type": "integer", "default": 6,
                              "description": "Число результатов (1-20)"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="run_recipe",
            description=(
                "Запустить именованный рецепт (цепочку скриптов) из improve_recipe.py. "
                "По умолчанию dry_run=true — показывает план без изменений."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string",
                             "description": "Имя рецепта (quality-check, morning-run, ...)"},
                    "dry_run": {"type": "boolean", "default": True},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="list_recipes",
            description="Список всех доступных рецептов Lorenzo с описаниями.",
            inputSchema={
                "type": "object",
                "properties": {
                    "find": {"type": "string",
                             "description": "Поиск рецепта по цели (опционально)"},
                },
            },
        ),
        Tool(
            name="update_contact_status",
            description=(
                "Обновляет статус контакта автора в docs/contacts/<author>.md. "
                "Устанавливает чекбокс studied/messaged/replied/agreed и/или добавляет заметку. "
                "Автоматически синхронизирует PROGRESS.md."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "author": {
                        "type": "string",
                        "description": "Имя автора (или часть имени): kksudo, spbmolot, kk…",
                    },
                    "status": {
                        "type": "string",
                        "description": "Новый статус: studied | messaged | replied | agreed",
                        "enum": ["studied", "messaged", "replied", "agreed"],
                    },
                    "note": {
                        "type": "string",
                        "description": "Текстовая заметка (опционально), добавляется в раздел ## Заметки",
                    },
                },
                "required": ["author"],
            },
        ),
        # ── Write-инструменты (Фаза 3) ──────────────────────────────────────
        Tool(
            name="add_card",
            description=(
                "Добавить новую карточку знаний в корпус Lorenzo. "
                "Создаёт .md-файл, обновляет search_index.json и passages.json. "
                "Перед созданием проверяет на дубли (cosine ≥ 0.85). "
                "Карточка получает статус raw — используйте Review Queue для одобрения."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "title":   {"type": "string", "description": "Заголовок карточки"},
                    "content": {"type": "string", "description": "Содержимое в Markdown"},
                    "section": {
                        "type": "string",
                        "description": "Раздел: 04-ai-collaborations | 05-habr-projects | 01-svyazi",
                        "default": "04-ai-collaborations",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Теги карточки",
                    },
                    "source_url": {
                        "type": "string",
                        "description": "URL источника (опционально)",
                    },
                },
                "required": ["title", "content"],
            },
        ),
        Tool(
            name="update_card_state",
            description=(
                "Обновить статус карточки в жизненном цикле: raw → normalized → approved. "
                "Также поддерживает rejected и decayed. "
                "Используется после ревью карточки агентом или человеком."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь к файлу карточки (относительно корня репо)",
                    },
                    "new_state": {
                        "type": "string",
                        "description": "Новый статус карточки",
                        "enum": ["raw", "normalized", "approved", "rejected", "decayed"],
                    },
                    "reason": {
                        "type": "string",
                        "description": "Причина смены статуса (опционально)",
                    },
                },
                "required": ["path", "new_state"],
            },
        ),
        Tool(
            name="propose_integration",
            description=(
                "Создать proposal-карточку об интеграции двух проектов. "
                "Генерирует карточку с гипотезой, аргументами и ссылками на оба проекта. "
                "Карточка попадает в Review Queue для последующего одобрения."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "project_a":  {"type": "string", "description": "Первый проект (напр. AgentFS)"},
                    "project_b":  {"type": "string", "description": "Второй проект (напр. Yodoca)"},
                    "hypothesis": {
                        "type": "string",
                        "description": "Гипотеза об интеграции (1-3 предложения)",
                    },
                    "rationale": {
                        "type": "string",
                        "description": "Обоснование: зачем это нужно, какой эффект (опционально)",
                    },
                },
                "required": ["project_a", "project_b", "hypothesis"],
            },
        ),
        Tool(
            name="list_cards",
            description=(
                "Список карточек корпуса с фильтрацией по статусу, типу и разделу. "
                "Используй для аудита жизненного цикла карточек."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "Фильтр по статусу: raw | normalized | approved | rejected | decayed | all",
                        "default": "all",
                    },
                    "section": {
                        "type": "string",
                        "description": "Фильтр по разделу (напр. 05-habr-projects)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Максимальное число карточек в ответе",
                        "default": 20,
                    },
                },
            },
        ),
        Tool(
            name="decay_card",
            description=(
                "Пометить карточку как устаревшую (state: decayed). "
                "Операция RFC-0002 decay_event: карточка остаётся в корпусе, "
                "но исключается из поиска и lifecycle promote. "
                "Необратима без явного вызова restore_card."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь к файлу карточки (относительно корня репо)",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Причина устаревания (обязательна для decay_event)",
                    },
                },
                "required": ["path", "reason"],
            },
        ),
        Tool(
            name="restore_card",
            description=(
                "Восстановить карточку из decayed обратно в raw. "
                "Операция restore_event по RFC-0002: отменяет decay_event. "
                "Используется при ошибочном decay или повторной актуализации."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Путь к файлу карточки (относительно корня репо)",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Причина восстановления (опционально)",
                    },
                },
                "required": ["path"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = _dispatch(name, arguments)
    except Exception as e:
        result = f"❌ Ошибка: {e}"
    return [TextContent(type="text", text=result)]


def _dispatch(name: str, args: dict) -> str:
    if name == "search_docs":
        return _tool_search(args.get("query", ""), args.get("top_k", 5))
    if name == "get_decisions":
        return _tool_decisions(args.get("topic", ""))
    if name == "get_contacts":
        return _tool_contacts(args.get("project", ""))
    if name == "get_project_status":
        return _tool_project_status(args.get("name", ""))
    if name == "bm25_search":
        return _tool_bm25_search(args.get("query", ""), args.get("top_k", 6))
    if name == "run_improve":
        return _tool_run_improve(args.get("script", ""), args.get("dry_run", True))
    if name == "run_recipe":
        return _tool_run_recipe(args.get("name", ""), args.get("dry_run", True))
    if name == "list_recipes":
        return _tool_list_recipes(args.get("find", ""))
    if name == "get_health":
        return _tool_health()
    if name == "list_scripts":
        return _tool_list_scripts(args.get("group", "all"))
    if name == "update_contact_status":
        return _tool_update_contact(
            args.get("author", ""),
            args.get("status", ""),
            args.get("note", ""),
        )
    if name == "add_card":
        return _tool_add_card(
            args.get("title", ""),
            args.get("content", ""),
            args.get("section", "04-ai-collaborations"),
            args.get("tags", []),
            args.get("source_url", ""),
        )
    if name == "update_card_state":
        return _tool_update_card_state(
            args.get("path", ""),
            args.get("new_state", ""),
            args.get("reason", ""),
        )
    if name == "propose_integration":
        return _tool_propose_integration(
            args.get("project_a", ""),
            args.get("project_b", ""),
            args.get("hypothesis", ""),
            args.get("rationale", ""),
        )
    if name == "list_cards":
        return _tool_list_cards(
            args.get("state", "all"),
            args.get("section", ""),
            args.get("limit", 20),
        )
    if name == "decay_card":
        return _tool_decay_card(
            args.get("path", ""),
            args.get("reason", ""),
        )
    if name == "restore_card":
        return _tool_restore_card(
            args.get("path", ""),
            args.get("reason", ""),
        )
    return f"Неизвестный инструмент: {name}"


# ---------------------------------------------------------------------------
# Реализации инструментов
# ---------------------------------------------------------------------------

def _tool_search(query: str, top_k: int) -> str:
    if not query:
        return "Укажите поисковый запрос."
    hits = _search(query, top_k)
    if not hits:
        return f"Ничего не найдено по запросу: «{query}»"
    lines = [f"Найдено {len(hits)} результатов для «{query}»:\n"]
    for h in hits:
        title = h.get("title", h.get("path", "?"))
        path  = h.get("path", "")
        snippet = h.get("content", "")[:200].replace("\n", " ")
        lines.append(f"**{title}**\n`{path}`\n> {snippet}...\n")
    return "\n".join(lines)


def _tool_decisions(topic: str) -> str:
    text = _read_doc("DECISIONS.md")
    if not text:
        return "DECISIONS.md не найден. Запустите improve_decisions.py"
    section = _extract_section(text, topic, lines_after=40)
    if not section:
        # Общий поиск по всему файлу
        lines = [l for l in text.splitlines() if topic.lower() in l.lower()]
        if not lines:
            return f"Решения по теме «{topic}» не найдены."
        section = "\n".join(lines[:20])
    return f"## Решения по теме «{topic}»\n\n{section}"


def _tool_contacts(project: str) -> str:
    text = _read_doc("CONTACTS.md")
    if not text:
        return "CONTACTS.md не найден. Запустите improve_contacts.py"
    proj_lower = project.lower()
    lines = text.splitlines()
    relevant = []
    in_section = False
    for line in lines:
        if proj_lower in line.lower():
            in_section = True
        if in_section:
            relevant.append(line)
            if len(relevant) > 15:
                break
    if not relevant:
        return f"Контакты для «{project}» не найдены."

    # Также ищем файл в docs/contacts/
    contact_dir = DOCS / "contacts"
    contact_files = []
    if contact_dir.exists():
        for f in sorted(contact_dir.glob("*.md")):
            if proj_lower in f.read_text(encoding="utf-8").lower():
                contact_files.append(str(f.relative_to(ROOT)))

    result = f"## Контакты: «{project}»\n\n" + "\n".join(relevant[:15])
    if contact_files:
        result += f"\n\n**Контактные файлы:**\n" + "\n".join(f"- `{p}`" for p in contact_files)
    return result


def _tool_project_status(name: str) -> str:
    name_lower = name.lower()
    lines_out = [f"## Статус проекта: {name}\n"]

    # Упоминания из ENTITIES.md
    ent = _read_doc("ENTITIES.md")
    for line in ent.splitlines():
        if name_lower in line.lower() and re.search(r'\d+', line):
            lines_out.append(f"**Упоминания:** {line.strip()}")
            break

    # Теги из TAGS.md
    tags_text = _read_doc("TAGS.md")
    found_tags = []
    for line in tags_text.splitlines():
        tag_m = re.match(r'##\s*#(\w+)', line)
        if tag_m:
            current_tag = tag_m.group(1)
        elif name_lower in line.lower() and '`docs/' in line:
            found_tags.append(current_tag)
    if found_tags:
        lines_out.append(f"**Теги:** {', '.join(set(found_tags))}")

    # Похожие документы из SIMILAR.md
    similar_text = _read_doc("SIMILAR.md")
    similar_hits = []
    for line in similar_text.splitlines():
        if name_lower in line.lower() and re.search(r'[\d.]+', line):
            similar_hits.append(line.strip())
            if len(similar_hits) >= 3:
                break
    if similar_hits:
        lines_out.append("\n**Похожие документы:**")
        lines_out.extend(similar_hits)

    # Контакт
    contacts_text = _read_doc("CONTACTS.md")
    for line in contacts_text.splitlines():
        if name_lower in line.lower() and '|' in line:
            lines_out.append(f"\n**Контакт:** {line.strip()}")
            break

    return "\n".join(lines_out) if len(lines_out) > 1 else f"Проект «{name}» не найден в базе."


def _tool_bm25_search(query: str, top_k: int) -> str:
    if not query:
        return "Укажите поисковый запрос."
    passages = _load_passages()
    if not passages:
        return ("passages.json не найден. Запустите:\n"
                "  python scripts/improve_passage_retrieval.py --index")
    results = _bm25_search(query, top_k)
    if not results:
        return f"Ничего не найдено по BM25 для: «{query}»"
    lines = [f"BM25-поиск «{query}» — топ {len(results)} абзацев:\n"]
    for i, r in enumerate(results, 1):
        fname = r["file"]
        short = "/".join(fname.split("/")[-2:]) if "/" in fname else fname
        text  = r.get("text", "").replace("\n", " ").strip()
        snippet = (text[:150] + "…") if len(text) > 150 else text
        lines.append(f"**{i}. [{r['score']:.2f}]** `{short}`\n> {snippet}\n")
    return "\n".join(lines)


def _tool_run_recipe(name: str, dry_run: bool) -> str:
    if not name:
        return "Укажите имя рецепта. Список: list_recipes()"
    recipe_script = SCRIPTS / "improve_recipe.py"
    if not recipe_script.exists():
        return "improve_recipe.py не найден."
    cmd = [sys.executable, str(recipe_script), "--run", name]
    if dry_run:
        cmd.append("--dry-run")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                cwd=str(ROOT), timeout=300)
        output = result.stdout[-4000:] if result.stdout else ""
        errors = result.stderr[-500:] if result.stderr else ""
        status = "✅" if result.returncode == 0 else "⚠"
        mode   = "[dry-run]" if dry_run else "[запущен]"
        return f"{status} Рецепт «{name}» {mode}\n\n{output}\n{errors}".strip()
    except subprocess.TimeoutExpired:
        return f"⏱ Рецепт «{name}» превысил таймаут 300с"
    except Exception as e:
        return f"❌ Ошибка: {e}"


def _tool_list_recipes(find: str = "") -> str:
    recipe_script = SCRIPTS / "improve_recipe.py"
    if not recipe_script.exists():
        return "improve_recipe.py не найден."
    cmd = [sys.executable, str(recipe_script)]
    if find:
        cmd += ["--find", find]
    else:
        cmd += ["--list"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                cwd=str(ROOT), timeout=10)
        return result.stdout or result.stderr or "Нет рецептов."
    except Exception as e:
        return f"❌ Ошибка: {e}"


def _tool_run_improve(script: str, dry_run: bool) -> str:
    if not script:
        return "Укажите имя скрипта."
    script_path = ROOT / "scripts" / script
    if not script_path.exists():
        available = [s for s in _list_improve_scripts() if script.lower() in s.lower()]
        hint = f"\nПохожие: {', '.join(available)}" if available else ""
        return f"Скрипт {script} не найден.{hint}"

    # Проверка безопасности: разрешаем только improve_*.py
    if not script.startswith("improve_"):
        return f"Разрешены только скрипты improve_*.py. Получено: {script}"

    cmd = [sys.executable, str(script_path)]
    if dry_run:
        cmd.append("--dry-run")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=60)
    output = result.stdout[-3000:] if result.stdout else ""
    errors = result.stderr[-1000:] if result.stderr else ""

    status = "✅ Успешно" if result.returncode == 0 else "❌ Ошибка"
    mode   = "[dry-run]" if dry_run else "[реальный запуск]"
    return f"{status} {mode} {script}\n\n{output}\n{errors}".strip()


def _tool_health() -> str:
    health_text  = _read_doc("HEALTH.md")
    scoring_text = _read_doc("SCORING.md")
    metrics_text = _read_doc("METRICS.md")

    lines = ["## Здоровье репозитория Lorenzo\n"]

    for text, fname in [(health_text, "HEALTH.md"), (scoring_text, "SCORING.md"),
                        (metrics_text, "METRICS.md")]:
        if not text:
            continue
        # Берём первые 10 значимых строк
        relevant = [l for l in text.splitlines()
                    if l.strip() and not l.startswith("<!--") and not l.startswith("_")][:12]
        lines.append(f"**{fname}:**\n" + "\n".join(relevant[:10]))
        lines.append("")

    return "\n".join(lines)


def _tool_list_scripts(group: str) -> str:
    group_map = {
        "structure": ["merge_short", "readmes", "summaries", "tags", "toc", "autocorrect"],
        "index":     ["glossary", "crossrefs", "search_index", "index_update", "timeline", "backlinks"],
        "analysis":  ["dedup", "clusters", "word_freq", "priorities", "similar", "complexity",
                      "sentiment", "density", "heatmap"],
        "extract":   ["action_items", "decisions", "questions", "kpi", "entities", "concepts",
                      "abbreviations", "extract_tables", "extract_code"],
        "quality":   ["consistency", "broken_links", "missing", "orphans", "validate",
                      "metrics", "alerts"],
        "graph":     ["graph", "mindmap", "network", "narrative"],
        "reports":   ["qa", "contacts", "changelog", "reading_order", "stats", "health",
                      "compare", "sitemap", "report"],
        "export":    ["export_csv", "export_json", "export_html"],
        "llm":       ["llm_enrich", "llm_summary", "llm_qa", "autofill"],
    }

    all_scripts = _list_improve_scripts()

    if group == "all" or group not in group_map:
        result = f"Всего скриптов: {len(all_scripts)}\n\n"
        for g, keywords in group_map.items():
            matched = [s for s in all_scripts if any(k in s for k in keywords)]
            result += f"**{g}** ({len(matched)}): {', '.join(matched)}\n"
        return result

    keywords = group_map[group]
    matched = [s for s in all_scripts if any(k in s for k in keywords)]
    return f"**Группа {group}** ({len(matched)} скриптов):\n" + "\n".join(f"- `{s}`" for s in matched)


CONTACT_CHECKBOXES = {
    "studied":  "Изучили профиль",
    "messaged": "Написали первое сообщение",
    "replied":  "Получили ответ",
    "agreed":   "Договорились о сотрудничестве",
}


def _tool_update_contact(author: str, status: str, note: str) -> str:
    """Обновляет чекбокс и/или добавляет заметку в файл контакта."""
    import re as _re
    from datetime import date as _date

    if not author:
        return "❌ Укажите имя автора (author)."

    contact_dir = DOCS / "contacts"
    if not contact_dir.exists():
        return "❌ docs/contacts/ не найден. Запустите improve_autofill.py"

    query = author.lower()
    candidates = [f for f in contact_dir.glob("*.md") if query in f.stem.lower()]

    if len(candidates) == 0:
        slug = _re.sub(r'[^a-z0-9]', '-', query)
        direct = contact_dir / f"{slug}.md"
        if direct.exists():
            candidates = [direct]
        else:
            available = sorted(f.stem for f in contact_dir.glob("*.md"))
            return f"❌ Контакт '{author}' не найден.\nДоступные: {', '.join(available)}"
    elif len(candidates) > 1:
        return f"❓ Несколько совпадений: {', '.join(f.stem for f in candidates)}. Уточните имя."

    path = candidates[0]
    text = path.read_text(encoding="utf-8")
    changes = []

    # Обновляем статус
    if status and status in CONTACT_CHECKBOXES:
        label = CONTACT_CHECKBOXES[status]
        pattern = rf'(\[[ x]\])(\s*{_re.escape(label)})'
        new_text, count = _re.subn(pattern, rf'[x]\2', text, flags=_re.IGNORECASE)
        if count > 0:
            text = new_text
            changes.append(f"✅ Отмечено: {label}")
        else:
            changes.append(f"⚠️ Строка '{label}' не найдена в файле")

    # Добавляем заметку
    if note:
        today = _date.today().isoformat()
        note_line = f"- {today}: {note}"
        if "## Заметки" in text:
            text = text.replace("## Заметки\n", f"## Заметки\n{note_line}\n")
        else:
            footer = _re.search(r'\n---\n', text)
            if footer:
                pos = footer.start()
                text = text[:pos] + f"\n## Заметки\n\n{note_line}\n" + text[pos:]
            else:
                text += f"\n## Заметки\n\n{note_line}\n"
        changes.append(f"📝 Заметка: {note}")

    if not changes:
        # Просто показываем текущий статус
        lines = [f"## Статус контакта: {path.stem}\n"]
        for key, label in CONTACT_CHECKBOXES.items():
            checked = bool(_re.search(rf'\[x\].*{_re.escape(label)}', text, _re.IGNORECASE))
            lines.append(f"{'✅' if checked else '⬜'} {label}")
        return "\n".join(lines)

    path.write_text(text, encoding="utf-8")

    # Синхронизируем прогресс
    sync = ROOT / "scripts" / "improve_progress_sync.py"
    if sync.exists():
        result = subprocess.run([sys.executable, str(sync)],
                                capture_output=True, text=True, cwd=ROOT)
        if result.returncode == 0:
            changes.append("📊 PROGRESS.md синхронизирован")

    return f"**{path.stem}** обновлён:\n" + "\n".join(changes)


# ---------------------------------------------------------------------------
# Write-инструменты (Фаза 3): add_card, update_card_state, propose_integration
# ---------------------------------------------------------------------------

import math as _math
import hashlib as _hashlib
import time as _time
from datetime import datetime as _dt

# Rate limiting: max 1 write call per 100ms (RFC-0003)
_last_write_ts: float = 0.0

def _write_rate_limit() -> None:
    global _last_write_ts
    elapsed = _time.time() - _last_write_ts
    if elapsed < 0.1:
        _time.sleep(0.1 - elapsed)
    _last_write_ts = _time.time()


# Audit trail: append-only JSONL log for all write operations
_AUDIT_LOG = ROOT / ".claude" / "mcp_write_log.jsonl"

def _audit_write(tool: str, args_summary: dict, result_summary: str) -> None:
    try:
        _AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = json.dumps({
            "ts":     _dt.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "tool":   tool,
            "args":   args_summary,
            "result": result_summary[:120],
        }, ensure_ascii=False)
        with open(_AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception:
        pass


def _mcp_tokenize(text: str) -> list[str]:
    stop = {"и", "в", "на", "что", "как", "это", "для", "или", "но",
            "the", "a", "an", "of", "in", "to", "is", "are", "for"}
    words = re.findall(r"[а-яёa-z0-9]+", text.lower())
    return [w for w in words if w not in stop]


def _cosine_sim(a: str, b: str) -> float:
    def tf(t: str) -> dict:
        freq: dict[str, int] = {}
        for w in _mcp_tokenize(t):
            freq[w] = freq.get(w, 0) + 1
        return freq
    fa, fb = tf(a), tf(b)
    keys = set(fa) | set(fb)
    dot  = sum(fa.get(k, 0) * fb.get(k, 0) for k in keys)
    na   = sum(v * v for v in fa.values()) ** 0.5
    nb   = sum(v * v for v in fb.values()) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def _find_dup(title: str, content: str, threshold: float = 0.85) -> dict | None:
    query = f"{title} {content[:400]}"
    for doc in _load_index()[:200]:
        existing = f"{doc.get('title', '')} {(doc.get('content') or doc.get('preview', ''))[:400]}"
        if _cosine_sim(query, existing) >= threshold:
            return doc
    return None


def _sync_passages_mcp(filepath: Path) -> None:
    """Добавить абзацы нового файла в passages.json."""
    passages_path = DOCS / "passages.json"
    try:
        text = filepath.read_text(encoding="utf-8")
        rel  = str(filepath.relative_to(ROOT))
        new_p = []
        for para in re.split(r"\n{2,}", text):
            para = para.strip()
            words = _mcp_tokenize(para)
            if len(words) >= 5:
                new_p.append({"file": rel, "text": para[:800], "wc": len(words), "tokens": words})
        if not new_p:
            return
        existing = []
        if passages_path.exists():
            raw = json.loads(passages_path.read_text(encoding="utf-8"))
            existing = raw.get("passages", raw) if isinstance(raw, dict) else raw
        combined = existing + new_p
        N = len(combined)
        avgdl = sum(p["wc"] for p in combined) / max(N, 1)
        df: dict[str, int] = {}
        for p in combined:
            for t in set(p["tokens"]):
                df[t] = df.get(t, 0) + 1
        idf = {t: _math.log((N - n + 0.5) / (n + 0.5) + 1) for t, n in df.items()}
        passages_path.write_text(
            json.dumps({"passages": combined, "idf": idf, "avgdl": avgdl, "N": N},
                       ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass


def _set_frontmatter_state(text: str, state: str) -> str:
    state_re = re.compile(r"^state:\s*\S+", re.MULTILINE)
    if state_re.search(text):
        return state_re.sub(f"state: {state}", text, count=1)
    fm_re = re.compile(r"^(---\n)")
    if fm_re.search(text):
        return fm_re.sub(f"---\nstate: {state}\n", text, count=1)
    return f"---\nstate: {state}\n---\n\n" + text


def _tool_add_card(title: str, content: str, section: str,
                   tags: list, source_url: str) -> str:
    _write_rate_limit()
    if not title or not content:
        return "❌ title и content обязательны."

    dup = _find_dup(title, content)
    if dup:
        return (
            f"⚠️ Дубль найден (similarity ≥ 0.85):\n"
            f"  **{dup.get('title', '?')}**\n"
            f"  `{dup.get('path', '?')}`\n"
            f"Карточка не создана. Передайте более уникальный контент."
        )

    slug      = re.sub(r"[^a-zа-яё0-9]+", "-", title.lower()).strip("-")[:50]
    target    = DOCS / section
    target.mkdir(parents=True, exist_ok=True)
    date      = _dt.now().strftime("%Y-%m-%d")
    tags_str  = ", ".join(tags)
    preview   = content[:200].replace("\n", " ")
    card_id   = _hashlib.sha256(f"{title}{content[:200]}".encode()).hexdigest()[:12]

    source_line = f"source_url: {source_url}" if source_url else ""
    written_at = _dt.now().strftime("%Y-%m-%dT%H:%M:%S")
    md = f"""---
title: {title}
date: {date}
card_id: {card_id}
tags: [{tags_str}]
source: mcp
state: raw
write_type: episode
written_by: mcp
written_at: {written_at}
{source_line}
---

# {title}

<!-- summary -->
> {preview}

<!-- tags: {tags_str} -->

{content}

---
_Добавлено через Lorenzo MCP: {date}_
"""
    filepath = target / f"{slug}.md"
    filepath.write_text(md, encoding="utf-8")

    try:
        subprocess.run(
            [sys.executable, str(SCRIPTS / "improve_index_update.py")],
            cwd=ROOT, capture_output=True, timeout=30,
        )
    except Exception:
        pass

    _sync_passages_mcp(filepath)
    _audit_write("add_card", {"title": title, "section": section}, f"created {filepath.name}")

    return (
        f"✅ Карточка создана:\n"
        f"  Путь: `{filepath.relative_to(ROOT)}`\n"
        f"  card_id: `{card_id}`\n"
        f"  Статус: raw\n"
        f"  Теги: {tags_str or '(нет)'}\n"
        f"Используйте update_card_state для перевода в normalized/approved."
    )


def _tool_update_card_state(path_str: str, new_state: str, reason: str) -> str:
    _write_rate_limit()
    if not path_str or not new_state:
        return "❌ Укажите path и new_state."

    valid_states = {"raw", "normalized", "approved", "rejected", "decayed"}
    if new_state not in valid_states:
        return f"❌ Недопустимый статус: {new_state}. Допустимые: {', '.join(sorted(valid_states))}"

    filepath = ROOT / path_str
    if not filepath.exists():
        # Поиск по имени файла
        candidates = list(DOCS.rglob(Path(path_str).name))
        if candidates:
            filepath = candidates[0]
        else:
            return f"❌ Файл не найден: {path_str}"

    text = filepath.read_text(encoding="utf-8")
    old_state_m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
    old_state = old_state_m.group(1) if old_state_m else "raw"

    if old_state == new_state:
        return f"ℹ️ Карточка уже в статусе `{new_state}`. Изменений нет."

    new_text = _set_frontmatter_state(text, new_state)

    if reason:
        reason_block = f"\n<!-- state-change: {old_state} → {new_state} | {_dt.now().strftime('%Y-%m-%d')} | {reason} -->\n"
        new_text = new_text + reason_block

    filepath.write_text(new_text, encoding="utf-8")
    _audit_write("update_card_state", {"path": path_str, "new_state": new_state},
                 f"{old_state} → {new_state}")

    return (
        f"✅ Статус обновлён:\n"
        f"  Файл: `{filepath.relative_to(ROOT)}`\n"
        f"  {old_state} → **{new_state}**\n"
        + (f"  Причина: {reason}" if reason else "")
    )


def _tool_propose_integration(project_a: str, project_b: str,
                               hypothesis: str, rationale: str) -> str:
    _write_rate_limit()
    if not project_a or not project_b or not hypothesis:
        return "❌ Укажите project_a, project_b и hypothesis."

    date   = _dt.now().strftime("%Y-%m-%d")
    slug   = f"proposal-{re.sub(r'[^a-zа-яё0-9]+', '-', project_a.lower())}-x-{re.sub(r'[^a-zа-яё0-9]+', '-', project_b.lower())}"[:60]
    card_id = _hashlib.sha256(f"{project_a}{project_b}{hypothesis}".encode()).hexdigest()[:12]

    content = f"""## Гипотеза интеграции

{hypothesis}

## Проекты

- **{project_a}** → [поиск в базе знаний]
- **{project_b}** → [поиск в базе знаний]

## Обоснование

{rationale or '_Не указано_'}

## Статус

- [ ] Предложено
- [ ] Проверено
- [ ] Одобрено
- [ ] Реализовано

## Следующие шаги

1. Изучить API обоих проектов
2. Определить точку интеграции (контракт)
3. Создать proof-of-concept
"""

    tags_str = f"proposal, {project_a.lower()}, {project_b.lower()}, integration"
    md = f"""---
title: "Proposal: {project_a} × {project_b}"
date: {date}
card_id: {card_id}
card_type: proposal
state: raw
tags: [{tags_str}]
projects: [{project_a}, {project_b}]
source: mcp
---

# Proposal: {project_a} × {project_b}

<!-- summary -->
> Гипотеза интеграции {project_a} и {project_b}: {hypothesis[:150]}

<!-- tags: {tags_str} -->

{content}

---
_Proposal создан через Lorenzo MCP: {date}_
"""

    target   = DOCS / "04-ai-collaborations"
    target.mkdir(parents=True, exist_ok=True)
    filepath = target / f"{slug}.md"
    filepath.write_text(md, encoding="utf-8")

    try:
        subprocess.run(
            [sys.executable, str(SCRIPTS / "improve_index_update.py")],
            cwd=ROOT, capture_output=True, timeout=30,
        )
    except Exception:
        pass

    _sync_passages_mcp(filepath)
    _audit_write("propose_integration",
                 {"project_a": project_a, "project_b": project_b},
                 f"proposal {filepath.name}")

    return (
        f"✅ Proposal создан:\n"
        f"  Файл: `{filepath.relative_to(ROOT)}`\n"
        f"  card_id: `{card_id}`\n"
        f"  Проекты: {project_a} × {project_b}\n"
        f"  Статус: raw (требует ревью)\n"
        f"\nГипотеза: {hypothesis[:200]}"
    )


def _tool_list_cards(state: str, section: str, limit: int) -> str:
    base = DOCS / section if section else DOCS
    state_re = re.compile(r"^state:\s*(\S+)", re.MULTILINE)

    results: list[dict] = []
    for path in base.rglob("*.md"):
        if "obsidian" in path.parts:
            continue
        if path.parent == DOCS and path.stem.isupper():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        m = state_re.search(text)
        card_state = m.group(1) if m else "raw"
        if state != "all" and card_state != state:
            continue
        title_m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else path.stem
        results.append({
            "path":  str(path.relative_to(ROOT)),
            "state": card_state,
            "title": title[:60],
        })
        if len(results) >= limit:
            break

    if not results:
        return f"Карточки с фильтрами state={state!r} section={section!r} не найдены."

    counts: dict[str, int] = {}
    for r in results:
        counts[r["state"]] = counts.get(r["state"], 0) + 1

    lines = [
        f"## Карточки (state={state}, section={section or 'all'}, limit={limit})\n",
        f"Найдено: {len(results)}\n",
    ]
    for s, n in sorted(counts.items()):
        lines.append(f"- **{s}**: {n}")
    lines.append("")
    for r in results[:limit]:
        lines.append(f"[{r['state']}] `{r['path']}` — {r['title']}")

    return "\n".join(lines)


# decay_card и restore_card (RFC-0002 decay_event / restore_event)

def _tool_decay_card(path_str: str, reason: str) -> str:
    _write_rate_limit()
    if not path_str:
        return "❌ Укажите path карточки."
    if not reason:
        return "❌ Укажите reason — причина decay_event обязательна (RFC-0002)."

    filepath = ROOT / path_str
    if not filepath.exists():
        candidates = list(DOCS.rglob(Path(path_str).name))
        if len(candidates) == 1:
            filepath = candidates[0]
        elif len(candidates) > 1:
            names = [str(c.relative_to(ROOT)) for c in candidates[:3]]
            return f"❓ Несколько совпадений: {names}"
        else:
            return f"❌ Файл не найден: {path_str}"

    text = filepath.read_text(encoding="utf-8")
    state_m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
    current = state_m.group(1) if state_m else "raw"

    if current == "decayed":
        return f"ℹ️ Карточка уже decayed: `{filepath.relative_to(ROOT)}`"

    now = _dt.now().strftime("%Y-%m-%dT%H:%M:%S")
    if state_m:
        text = re.sub(r"^state:\s*\S+", "state: decayed", text, count=1, flags=re.MULTILINE)
    else:
        text = text.replace("---\n", f"---\nstate: decayed\n", 1)

    # Добавить decay_event в конец файла
    text += f"\n<!-- decay_event: {current} → decayed | {now} | {reason} -->\n"
    filepath.write_text(text, encoding="utf-8")
    _audit_write("decay_card", {"path": path_str, "reason": reason[:60]},
                 f"{current} → decayed")

    return (
        f"✅ Карточка помечена как decayed:\n"
        f"  `{filepath.relative_to(ROOT)}`\n"
        f"  Было: {current} → Стало: decayed\n"
        f"  Причина: {reason}\n"
        f"  Карточка исключена из promote и поиска.\n"
        f"  Восстановление: restore_card"
    )


def _tool_restore_card(path_str: str, reason: str) -> str:
    _write_rate_limit()
    if not path_str:
        return "❌ Укажите path карточки."

    filepath = ROOT / path_str
    if not filepath.exists():
        candidates = list(DOCS.rglob(Path(path_str).name))
        if len(candidates) == 1:
            filepath = candidates[0]
        elif len(candidates) > 1:
            names = [str(c.relative_to(ROOT)) for c in candidates[:3]]
            return f"❓ Несколько совпадений: {names}"
        else:
            return f"❌ Файл не найден: {path_str}"

    text = filepath.read_text(encoding="utf-8")
    state_m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
    current = state_m.group(1) if state_m else "raw"

    if current != "decayed":
        return f"ℹ️ Карточка не в decayed (текущий state: {current}): `{filepath.relative_to(ROOT)}`"

    now = _dt.now().strftime("%Y-%m-%dT%H:%M:%S")
    text = re.sub(r"^state:\s*decayed", "state: raw", text, count=1, flags=re.MULTILINE)
    reason_note = f" | {reason}" if reason else ""
    text += f"\n<!-- restore_event: decayed → raw | {now}{reason_note} -->\n"
    filepath.write_text(text, encoding="utf-8")
    _audit_write("restore_card", {"path": path_str}, "decayed → raw")

    return (
        f"✅ Карточка восстановлена:\n"
        f"  `{filepath.relative_to(ROOT)}`\n"
        f"  decayed → raw\n"
        f"  Карточка снова участвует в promote и поиске."
    )


# ---------------------------------------------------------------------------
# Запуск
# ---------------------------------------------------------------------------

async def main_async():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main_async())
