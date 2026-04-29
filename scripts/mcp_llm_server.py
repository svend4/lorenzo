"""
mcp_llm_server.py — MCP-сервер lorenzo-llm.

LLM-обогащение через Anthropic API с локальным кэшем.

Инструменты:
  llm_summary(file_path)        — резюме одного файла
  llm_qa(question)              — Q&A по корпусу с поиском
  llm_enrich(section, dry_run)  — обогащение пустых разделов
  llm_contact(author)           — персональное сообщение автору

Кэш: .claude/llm_cache.jsonl — избегаем повторных вызовов API.

Требует ANTHROPIC_API_KEY в env.

Запуск:
  python scripts/mcp_llm_server.py
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_common import ROOT, build_server, run_stdio

try:
    from mcp.types import Tool
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


CACHE_PATH = ROOT / ".claude" / "llm_cache.jsonl"


def _cache_key(*parts: str) -> str:
    return hashlib.sha256("\x00".join(parts).encode()).hexdigest()[:16]


def _cache_get(key: str) -> str | None:
    if not CACHE_PATH.exists():
        return None
    for line in CACHE_PATH.read_text(encoding='utf-8').splitlines():
        try:
            entry = json.loads(line)
            if entry.get('key') == key:
                return entry.get('value')
        except json.JSONDecodeError:
            continue
    return None


def _cache_put(key: str, value: str):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_PATH.open('a', encoding='utf-8') as f:
        f.write(json.dumps({'key': key, 'value': value[:5000]}, ensure_ascii=False) + '\n')


def _check_api_key() -> str | None:
    if not os.environ.get('ANTHROPIC_API_KEY'):
        return ("❌ ANTHROPIC_API_KEY не задан. "
                "Установите: export ANTHROPIC_API_KEY='sk-ant-...'")
    return None


def _run(script_name: str, args: list[str], timeout: int = 180) -> str:
    err = _check_api_key()
    if err:
        return err
    script = ROOT / "scripts" / script_name
    if not script.exists():
        return f"❌ {script_name} не найден"
    result = subprocess.run([sys.executable, str(script)] + args,
                            capture_output=True, text=True, cwd=ROOT, timeout=timeout)
    out = (result.stdout or result.stderr)[-3000:]
    return out.strip()


def dispatch(name: str, args: dict) -> str:
    if name == "llm_summary":
        f = args.get("file_path", "")
        if not f:
            return "❌ Укажите file_path."
        # Проверка кэша
        text = (ROOT / f).read_text(encoding='utf-8') if (ROOT / f).exists() else ""
        key = _cache_key("summary", text[:1000])
        cached = _cache_get(key)
        if cached:
            return f"[cached]\n\n{cached}"
        result = _run("improve_llm_summary.py", ["--file", f])
        if "❌" not in result:
            _cache_put(key, result)
        return result

    if name == "llm_qa":
        q = args.get("question", "")
        if not q:
            return "❌ Укажите question."
        key = _cache_key("qa", q)
        cached = _cache_get(key)
        if cached:
            return f"[cached]\n\n{cached}"
        result = _run("improve_llm_qa.py", ["--question", q])
        if "❌" not in result:
            _cache_put(key, result)
        return result

    if name == "llm_enrich":
        section = args.get("section", "")
        dry = args.get("dry_run", True)
        a = []
        if section:
            a.extend(["--section", section])
        if dry:
            a.append("--dry-run")
        return _run("improve_llm_enrich.py", a)

    if name == "llm_contact":
        author = args.get("author", "")
        if not author:
            return "❌ Укажите author."
        return _run("improve_llm_contact.py", ["--author", author])

    if name == "cache_stats":
        if not CACHE_PATH.exists():
            return "Кэш пуст."
        lines = CACHE_PATH.read_text(encoding='utf-8').splitlines()
        return f"Кэш: {len(lines)} записей в {CACHE_PATH.relative_to(ROOT)}"

    if name == "cache_clear":
        if CACHE_PATH.exists():
            CACHE_PATH.unlink()
        return "✓ Кэш очищен"

    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(name="llm_summary", description="LLM-резюме одного файла (с кэшем).",
         inputSchema={"type": "object", "properties": {"file_path": {"type": "string"}},
                      "required": ["file_path"]}),
    Tool(name="llm_qa", description="Q&A по корпусу через LLM (с поиском).",
         inputSchema={"type": "object", "properties": {"question": {"type": "string"}},
                      "required": ["question"]}),
    Tool(name="llm_enrich", description="LLM-обогащение раздела (dry_run по умолчанию).",
         inputSchema={"type": "object",
                      "properties": {"section": {"type": "string"},
                                     "dry_run": {"type": "boolean", "default": True}}}),
    Tool(name="llm_contact", description="Персональное сообщение автору проекта.",
         inputSchema={"type": "object", "properties": {"author": {"type": "string"}},
                      "required": ["author"]}),
    Tool(name="cache_stats", description="Статистика LLM-кэша.",
         inputSchema={"type": "object", "properties": {}}),
    Tool(name="cache_clear", description="Очистить LLM-кэш.",
         inputSchema={"type": "object", "properties": {}}),
]


if __name__ == "__main__":
    server = build_server("lorenzo-llm", TOOLS, dispatch)
    run_stdio(server)
