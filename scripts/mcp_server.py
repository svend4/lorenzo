"""
mcp_server.py — MCP-сервер для документации Lorenzo / Svyazi 2.0.
Экспортирует инструменты: search_docs, get_doc, run_script, get_stats.
Запуск: python scripts/mcp_server.py
Протокол: stdio (стандартный MCP транспорт)
"""
import json
import sys
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# ─── MCP protocol helpers ────────────────────────────────────────────────────

def send(obj: dict) -> None:
    print(json.dumps(obj), flush=True)


def send_result(req_id, content: list[dict]) -> None:
    send({"jsonrpc": "2.0", "id": req_id, "result": {"content": content}})


def send_error(req_id, code: int, message: str) -> None:
    send({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}})


def text_content(text: str) -> dict:
    return {"type": "text", "text": text}


# ─── Tool implementations ─────────────────────────────────────────────────────

def tool_search_docs(query: str, max_results: int = 10) -> str:
    """Полнотекстовый поиск по docs/."""
    q = query.lower()
    results = []
    for f in sorted(DOCS.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        if q in text.lower():
            # Найти контекст вокруг совпадения
            idx = text.lower().find(q)
            snippet = text[max(0, idx-60):idx+120].replace("\n", " ").strip()
            results.append(f"**{f.relative_to(ROOT)}**\n> {snippet[:180]}")
    if not results:
        return f"Ничего не найдено по запросу: {query}"
    return f"Найдено {len(results)} файлов по '{query}':\n\n" + "\n\n".join(results[:max_results])


def tool_get_doc(path: str) -> str:
    """Читает документ из docs/."""
    p = ROOT / path
    if not p.exists():
        # Попробовать поиск по имени файла
        matches = list(DOCS.rglob(f"*{Path(path).name}*"))
        if matches:
            p = matches[0]
        else:
            return f"Файл не найден: {path}"
    text = p.read_text(encoding="utf-8")
    # Возвращаем первые 2000 слов
    words = text.split()
    if len(words) > 2000:
        text = " ".join(words[:2000]) + "\n\n_[...обрезано]_"
    return f"# {p.relative_to(ROOT)}\n\n{text}"


def tool_run_script(script_name: str, dry_run: bool = True) -> str:
    """Запускает один из improve_*.py скриптов."""
    scripts_dir = ROOT / "scripts"
    # Санитизация: только буквы, цифры, _-
    safe = re.sub(r'[^a-zA-Z0-9_\-]', '', script_name.replace(".py", ""))
    script_path = scripts_dir / f"{safe}.py"

    if not script_path.exists():
        available = [f.name for f in scripts_dir.glob("improve_*.py")][:10]
        return f"Скрипт не найден: {safe}.py\nДоступные: {', '.join(available)}"

    if dry_run:
        return f"[dry-run] Запустил бы: python {script_path.relative_to(ROOT)}"

    try:
        result = subprocess.run(
            ["python", str(script_path)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        out = result.stdout[-1000:] if result.stdout else ""
        err = result.stderr[-500:]  if result.stderr else ""
        return f"stdout:\n{out}\nstderr:\n{err}\ncode: {result.returncode}"
    except subprocess.TimeoutExpired:
        return "Timeout: скрипт работал > 60 секунд"
    except Exception as e:
        return f"Ошибка запуска: {e}"


def tool_get_stats() -> str:
    """Возвращает статистику репозитория."""
    total_md = len(list(DOCS.rglob("*.md")))
    total_words = sum(len(f.read_text(encoding="utf-8").split()) for f in DOCS.rglob("*.md"))
    scripts_n = len(list((ROOT / "scripts").glob("improve_*.py")))

    stats_file = DOCS / "STATS.md"
    extra = ""
    if stats_file.exists():
        m = re.search(r'Итого.*?(\d[\d,]+)\s*слов', stats_file.read_text(encoding="utf-8"))
        if m:
            extra = f"\n(по STATS.md: {m.group(1)} слов)"

    return (
        f"## Статистика Lorenzo / Svyazi 2.0\n\n"
        f"- Markdown файлов: **{total_md}**\n"
        f"- Слов: **{total_words:,}**{extra}\n"
        f"- Скриптов improve_*: **{scripts_n}**\n"
        f"- Корень: `{ROOT}`\n"
    )


# ─── MCP dispatch ─────────────────────────────────────────────────────────────

TOOLS_MANIFEST = [
    {
        "name": "search_docs",
        "description": "Полнотекстовый поиск по документации Svyazi 2.0",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query":       {"type": "string", "description": "Поисковый запрос"},
                "max_results": {"type": "integer", "description": "Максимум результатов (по умолч. 10)"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_doc",
        "description": "Читает документ из репозитория Lorenzo по пути или имени",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Относительный путь к файлу (напр. docs/FAQ.md)"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "run_script",
        "description": "Запускает один из improve_*.py скриптов (по умолч. dry-run)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "script_name": {"type": "string", "description": "Имя скрипта (напр. improve_stats)"},
                "dry_run":     {"type": "boolean", "description": "Только показать команду, не запускать"},
            },
            "required": ["script_name"],
        },
    },
    {
        "name": "get_stats",
        "description": "Возвращает статистику репозитория: файлы, слова, скрипты",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def handle_request(req: dict) -> None:
    method = req.get("method", "")
    req_id = req.get("id")
    params = req.get("params", {})

    if method == "initialize":
        send({
            "jsonrpc": "2.0", "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "lorenzo-docs", "version": "1.0.0"},
            }
        })

    elif method == "tools/list":
        send({"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS_MANIFEST}})

    elif method == "tools/call":
        name = params.get("name", "")
        args = params.get("arguments", {})

        if name == "search_docs":
            out = tool_search_docs(args.get("query", ""), args.get("max_results", 10))
        elif name == "get_doc":
            out = tool_get_doc(args.get("path", ""))
        elif name == "run_script":
            out = tool_run_script(args.get("script_name", ""), args.get("dry_run", True))
        elif name == "get_stats":
            out = tool_get_stats()
        else:
            send_error(req_id, -32601, f"Unknown tool: {name}")
            return

        send_result(req_id, [text_content(out)])

    elif method == "notifications/initialized":
        pass  # no response needed

    else:
        if req_id is not None:
            send_error(req_id, -32601, f"Method not found: {method}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            handle_request(req)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")


if __name__ == "__main__":
    main()
