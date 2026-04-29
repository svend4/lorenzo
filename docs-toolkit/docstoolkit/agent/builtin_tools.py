"""Встроенные tools для AgentLoop — обёртки над docs-toolkit функциями."""
from docstoolkit.agent.types import Tool


def _search_tool(query: str = "", top_k: int = 5) -> str:
    """Поиск по корпусу через embeddings."""
    try:
        from docstoolkit.embeddings import get_provider
        from docstoolkit.config import load_config
        import json as _json

        cfg = load_config()
        index_path = cfg.docs_dir / "search_index.json"
        if not index_path.exists():
            return "❌ search_index.json не найден"
        docs = _json.loads(index_path.read_text(encoding="utf-8"))
        if isinstance(docs, dict):
            docs = docs.get("docs", [])

        prov = get_provider("tfidf")
        prov.fit([d.get("content", "") + " " + d.get("title", "") for d in docs])
        results = prov.search(query, docs, top_k=top_k)

        if not results:
            return f"Ничего не найдено по «{query}»"
        lines = [f"Найдено: {len(results)}"]
        for r in results:
            lines.append(f"- [{r.score:.3f}] {r.title} ({r.path})")
            if r.snippet:
                lines.append(f"  {r.snippet[:200]}")
        return "\n".join(lines)
    except Exception as e:
        return f"Search error: {e}"


def _read_doc_tool(path: str = "") -> str:
    """Читает файл из docs/."""
    try:
        from docstoolkit.config import load_config
        from pathlib import Path
        cfg = load_config()
        full = (cfg.docs_dir / path).resolve()
        full.relative_to(cfg.docs_dir.resolve())
        if not full.exists():
            return f"❌ Не найден: {path}"
        return full.read_text(encoding="utf-8")[:4000]
    except (ValueError, Exception) as e:
        return f"Read error: {e}"


def _list_skills_tool(category: str = "") -> str:
    """Список скилов из .claude/skills/."""
    try:
        from docstoolkit.skills import list_skills
        skills = list_skills()
        return "\n".join(f"- {n}" for n in sorted(skills)[:30])
    except Exception as e:
        return f"List skills error: {e}"


def _validate_doc_tool(file_path: str = "") -> str:
    """Валидация документа по схеме шаблона."""
    try:
        from docstoolkit.config import load_config
        from docstoolkit.frontmatter import extract_frontmatter
        from pathlib import Path
        import json as _json

        cfg = load_config()
        full = Path(file_path)
        if not full.is_absolute():
            full = cfg.root / file_path
        if not full.exists():
            return f"❌ Не найден: {file_path}"
        text = full.read_text(encoding="utf-8")
        fm, _ = extract_frontmatter(text)
        if not fm or "template" not in fm:
            return f"⚠️  Нет frontmatter / template поля"

        schema_path = cfg.schemas_dir / f"{fm['template']}.json"
        if not schema_path.exists():
            return f"⚠️  Схема для {fm['template']} не найдена"
        schema = _json.loads(schema_path.read_text(encoding="utf-8"))

        errors = []
        for req in schema.get("required", []):
            if req not in fm:
                errors.append(f"missing required: {req}")
        if errors:
            return "❌ Errors:\n" + "\n".join(f"  - {e}" for e in errors)
        return f"✓ {file_path}: валиден по схеме {fm['template']}"
    except Exception as e:
        return f"Validate error: {e}"


def default_tools() -> list[Tool]:
    """Стандартный набор tools для AgentLoop."""
    return [
        Tool(
            name="search",
            fn=_search_tool,
            description="Полнотекстовый поиск по корпусу документов",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос"},
                    "top_k": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="read_doc",
            fn=_read_doc_tool,
            description="Читает один файл из docs/ по относительному пути",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Путь относительно docs/"},
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="list_skills",
            fn=_list_skills_tool,
            description="Список доступных скилов (instructions для агента)",
            input_schema={
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                },
            },
        ),
        Tool(
            name="validate_doc",
            fn=_validate_doc_tool,
            description="Валидация документа по JSON-схеме его шаблона",
            input_schema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Путь к .md файлу"},
                },
                "required": ["file_path"],
            },
        ),
    ]
