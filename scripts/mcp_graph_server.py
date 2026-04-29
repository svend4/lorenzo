"""
mcp_graph_server.py — MCP-сервер lorenzo-graph.

Аналитика и агрегаты: HEALTH, METRICS, KPI, концепт-граф, решения.

Инструменты:
  get_health()                     — общий балл HEALTH/SCORING/METRICS
  get_decisions(topic)             — релевантные ADR
  get_concept_graph(top_n)         — топ концептов и связей
  kpi_history(name)                — история KPI по метрике
  get_project_status(name)         — теги, упоминания, похожие, контакт

Ресурсы:
  lorenzo://docs/HEALTH.md
  lorenzo://docs/METRICS.md
  lorenzo://docs/SCORING.md
  lorenzo://docs/KPI_HISTORY.md
  lorenzo://docs/CONCEPT_GRAPH.md
  lorenzo://docs/DECISIONS.md
  lorenzo://docs/INDEX.md

Запуск:
  python scripts/mcp_graph_server.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_common import ROOT, DOCS, build_server, run_stdio, read_doc, extract_section

try:
    from mcp.types import Tool, Resource, Prompt, PromptArgument
except ImportError:
    class _MCPStub:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    Tool = Resource = Prompt = PromptArgument = _MCPStub  # type: ignore


def tool_health() -> str:
    health = read_doc("HEALTH.md")
    scoring = read_doc("SCORING.md")
    metrics = read_doc("METRICS.md")
    if not (health or scoring or metrics):
        return "Запустите improve_health.py / improve_scoring.py / improve_metrics.py"

    lines = ["## Здоровье репозитория Lorenzo\n"]
    for text, fname in [(health, "HEALTH.md"), (scoring, "SCORING.md"), (metrics, "METRICS.md")]:
        if not text:
            continue
        relevant = [l for l in text.splitlines()
                    if l.strip() and not l.startswith("<!--") and not l.startswith("_")][:12]
        lines.append(f"**{fname}:**\n" + "\n".join(relevant[:10]))
        lines.append("")
    return "\n".join(lines)


def tool_decisions(topic: str) -> str:
    text = read_doc("DECISIONS.md")
    if not text:
        return "DECISIONS.md не найден. Запустите improve_decisions.py"
    section = extract_section(text, topic, lines_after=40)
    if not section:
        lines = [l for l in text.splitlines() if topic.lower() in l.lower()]
        if not lines:
            return f"Решения по «{topic}» не найдены."
        section = "\n".join(lines[:20])
    return f"## Решения по «{topic}»\n\n{section}"


def tool_concept_graph(top_n: int = 30) -> str:
    text = read_doc("CONCEPT_GRAPH.md")
    if not text:
        return "CONCEPT_GRAPH.md не найден. Запустите improve_concept_graph.py"
    lines = text.splitlines()
    out = []
    count = 0
    for line in lines:
        if line.strip().startswith("- "):
            out.append(line)
            count += 1
            if count >= top_n:
                break
        elif line.startswith("##") or line.startswith("```"):
            out.append(line)
    return "\n".join(out[:top_n * 2])


def tool_kpi_history(name: str = "") -> str:
    text = read_doc("KPI_HISTORY.md")
    if not text:
        return "KPI_HISTORY.md не найден. Запустите improve_kpi_snapshot.py"
    if not name:
        return text[:3000]
    lines = text.splitlines()
    out = []
    in_block = False
    for line in lines:
        if name.lower() in line.lower() and ('##' in line or '|' in line):
            in_block = True
        if in_block:
            out.append(line)
            if len(out) > 30:
                break
    return "\n".join(out) if out else f"Метрика «{name}» не найдена в KPI_HISTORY.md."


def tool_project_status(name: str) -> str:
    name_lower = name.lower()
    lines_out = [f"## Статус проекта: {name}\n"]

    ent = read_doc("ENTITIES.md")
    for line in ent.splitlines():
        if name_lower in line.lower() and re.search(r'\d+', line):
            lines_out.append(f"**Упоминания:** {line.strip()}")
            break

    tags_text = read_doc("TAGS.md")
    found_tags = []
    current_tag = None
    for line in tags_text.splitlines():
        tag_m = re.match(r'##\s*#(\w+)', line)
        if tag_m:
            current_tag = tag_m.group(1)
        elif current_tag and name_lower in line.lower() and '`docs/' in line:
            found_tags.append(current_tag)
    if found_tags:
        lines_out.append(f"**Теги:** {', '.join(set(found_tags))}")

    similar_text = read_doc("SIMILAR.md")
    similar_hits = []
    for line in similar_text.splitlines():
        if name_lower in line.lower() and re.search(r'[\d.]+', line):
            similar_hits.append(line.strip())
            if len(similar_hits) >= 3:
                break
    if similar_hits:
        lines_out.append("\n**Похожие документы:**")
        lines_out.extend(similar_hits)

    contacts_text = read_doc("CONTACTS.md")
    for line in contacts_text.splitlines():
        if name_lower in line.lower() and '|' in line:
            lines_out.append(f"\n**Контакт:** {line.strip()}")
            break

    return "\n".join(lines_out) if len(lines_out) > 1 else f"Проект «{name}» не найден."


def dispatch(name: str, args: dict) -> str:
    if name == "get_health":
        return tool_health()
    if name == "get_decisions":
        return tool_decisions(args.get("topic", ""))
    if name == "get_concept_graph":
        return tool_concept_graph(args.get("top_n", 30))
    if name == "kpi_history":
        return tool_kpi_history(args.get("name", ""))
    if name == "get_project_status":
        return tool_project_status(args.get("name", ""))
    return f"Неизвестный инструмент: {name}"


TOOLS = [
    Tool(
        name="get_health",
        description="Общий балл здоровья репозитория из HEALTH.md / SCORING.md / METRICS.md.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="get_decisions",
        description="ADR / архитектурные решения по теме из DECISIONS.md.",
        inputSchema={
            "type": "object",
            "properties": {"topic": {"type": "string"}},
            "required": ["topic"],
        },
    ),
    Tool(
        name="get_concept_graph",
        description="Топ концептов и связей из CONCEPT_GRAPH.md.",
        inputSchema={
            "type": "object",
            "properties": {"top_n": {"type": "integer", "default": 30}},
        },
    ),
    Tool(
        name="kpi_history",
        description="История KPI: общая или по конкретной метрике.",
        inputSchema={
            "type": "object",
            "properties": {"name": {"type": "string"}},
        },
    ),
    Tool(
        name="get_project_status",
        description="Статус проекта: теги, упоминания, похожие документы, контакт.",
        inputSchema={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    ),
]


RESOURCES = [
    Resource(uri="lorenzo://docs/HEALTH.md", name="Health dashboard",
             description="Балл здоровья репо", mimeType="text/markdown"),
    Resource(uri="lorenzo://docs/METRICS.md", name="Metrics",
             description="Метрики качества", mimeType="text/markdown"),
    Resource(uri="lorenzo://docs/SCORING.md", name="Scoring",
             description="Go/No-Go", mimeType="text/markdown"),
    Resource(uri="lorenzo://docs/KPI_HISTORY.md", name="KPI history",
             description="История KPI снапшотов", mimeType="text/markdown"),
    Resource(uri="lorenzo://docs/CONCEPT_GRAPH.md", name="Concept graph",
             description="Граф концептов", mimeType="text/markdown"),
    Resource(uri="lorenzo://docs/DECISIONS.md", name="Decisions",
             description="ADR база", mimeType="text/markdown"),
    Resource(uri="lorenzo://docs/INDEX.md", name="Index",
             description="Главный навигационный хаб", mimeType="text/markdown"),
]


def read_resource(uri: str) -> str:
    if uri.startswith("lorenzo://docs/"):
        rel = uri[len("lorenzo://docs/"):]
        return read_doc(rel)
    return ""


PROMPTS = [
    Prompt(
        name="lorenzo-audit",
        description="Сводный аудит репозитория: HEALTH + противоречия + пробелы",
        arguments=[],
    ),
    Prompt(
        name="lorenzo-decisions-by-topic",
        description="Хронология решений по теме",
        arguments=[PromptArgument(name="topic", description="Тема", required=True)],
    ),
    Prompt(
        name="lorenzo-onboard",
        description="Онбординг для нового участника: HEALTH + INDEX + ключевые ADR",
        arguments=[],
    ),
]


def get_prompt(name: str, args: dict) -> str:
    if name == "lorenzo-audit":
        return (
            "1. Вызови `get_health` для общего балла. "
            "2. Прочитай ресурсы lorenzo://docs/CONTRADICTIONS.md и lorenzo://docs/CONTENT_GAPS.md. "
            "3. Выдели топ-5 проблем 🔴 и топ-5 действий для их решения."
        )
    if name == "lorenzo-decisions-by-topic":
        topic = args.get("topic", "")
        return (
            f"Вызови `get_decisions` с topic='{topic}', "
            f"для каждого упомянутого ADR прочитай файл, "
            f"составь хронологию: дата → решение → обоснование → текущий статус."
        )
    if name == "lorenzo-onboard":
        return (
            "Прочитай в порядке: lorenzo://docs/INDEX.md → lorenzo://docs/HEALTH.md → "
            "lorenzo://docs/DECISIONS.md (топ-10 последних). "
            "Дай новичку: что это за проект (1 абзац), статус (балл), "
            "топ-3 решения из последних, куда смотреть дальше."
        )
    return f"Промпт {name} не определён."


if __name__ == "__main__":
    server = build_server(
        "lorenzo-graph",
        TOOLS,
        dispatch,
        resources_spec=RESOURCES,
        resource_reader=read_resource,
        prompts_spec=PROMPTS,
        prompt_getter=get_prompt,
    )
    run_stdio(server)
