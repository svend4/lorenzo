"""
improve_mindmap.py — строит майндмап всего репозитория в формате Mermaid mindmap.
Создаёт docs/MINDMAP.md.
Запуск: python scripts/improve_mindmap.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SECTION_ICONS = {
    "01-svyazi":                  "🧠",
    "02-anthropic-vacancies":     "💼",
    "03-technology-combinations": "⚙️",
    "04-ai-collaborations":       "🤝",
    "05-habr-projects":           "📦",
}

SECTION_LABELS = {
    "01-svyazi":                  "Svyazi 2.0",
    "02-anthropic-vacancies":     "Anthropic Vacancies",
    "03-technology-combinations": "Tech Combinations",
    "04-ai-collaborations":       "AI Collaborations",
    "05-habr-projects":           "Habr Projects",
}

# Ключевые понятия для второго уровня майндмапа
SECTION_CONCEPTS = {
    "01-svyazi": [
        "CardIndex", "Evidence Envelope", "Memory Write Policy",
        "Ансамбли", "MVP 12-18 дней", "Безопасность",
    ],
    "02-anthropic-vacancies": [
        "Research & ML", "GTM Sales", "Trust & Safety",
        "Inference Infra", "Product Eng", "Карьерный маппинг",
    ],
    "03-technology-combinations": [
        "Агентный роутинг", "Граф знаний", "Local-first",
        "Sozialrecht", "Бенчмарки",
    ],
    "04-ai-collaborations": [
        "Knowledge OS", "Forensic RAG", "Agent Teams",
        "Security Runtime", "Web Intelligence",
    ],
    "05-habr-projects": [
        "Yodoca", "NGT Memory", "MemNet",
        "knowledge-space", "AgentFS", "Wikontic",
    ],
}

# Связи между ключевыми проектами для второй диаграммы
PROJECT_LINKS = [
    ("Svyazi", "CardIndex", "ingest→index"),
    ("CardIndex", "AgentFS", "storage"),
    ("AgentFS", "knowledge-space", "reference"),
    ("Yodoca", "NGT Memory", "consolidation"),
    ("NGT Memory", "Svyazi", "recall→discovery"),
    ("LiteParse", "Legal RAG", "evidence"),
    ("Legal RAG", "CardIndex", "proof→card"),
    ("mclaude", "AI Factory", "coordination"),
    ("AI Factory", "Rufler", "orchestration"),
    ("Rufler", "AutoResearch", "self-improve"),
    ("LiteLLM", "SENTINEL", "gateway→guard"),
    ("Tool Search", "LiteLLM", "lazy-load"),
]


def make_mindmap() -> str:
    lines = ["mindmap", "  root((Lorenzo Repository))"]

    for section, label in SECTION_LABELS.items():
        icon = SECTION_ICONS.get(section, "📄")
        lines.append(f"    {icon} **{label}**")
        concepts = SECTION_CONCEPTS.get(section, [])
        for concept in concepts:
            lines.append(f"      {concept}")

    return "\n".join(lines)


def make_flow_diagram() -> str:
    """Граф потока данных между ключевыми компонентами."""
    lines = ["flowchart LR"]

    # Группы по слоям
    groups = {
        "INGEST": ["Svyazi", "CardIndex", "Firecrawl"],
        "KNOWLEDGE": ["AgentFS", "knowledge_space"],
        "MEMORY": ["Yodoca", "NGT_Memory", "MemNet"],
        "RAG": ["LiteParse", "Legal_RAG", "Hybrid_RAG"],
        "ORCHESTRATION": ["mclaude", "AI_Factory", "Rufler"],
        "SECURITY": ["LiteLLM", "SENTINEL", "Tool_Search"],
    }

    for group, members in groups.items():
        lines.append(f"  subgraph {group}")
        for m in members:
            label = m.replace("_", " ")
            lines.append(f"    {m}[{label}]")
        lines.append("  end")

    # Ключевые связи
    for src, dst, label in PROJECT_LINKS:
        s = src.replace("-", "_").replace(" ", "_")
        d = dst.replace("-", "_").replace(" ", "_")
        lines.append(f"  {s} -->|{label}| {d}")

    return "\n".join(lines)


def main():
    mindmap = make_mindmap()
    flowchart = make_flow_diagram()

    lines = [
        "# Майндмап репозитория Lorenzo\n",
        "## Структура разделов\n",
        "```mermaid",
        mindmap,
        "```\n",
        "## Поток данных между проектами\n",
        "```mermaid",
        flowchart,
        "```\n",
        "## Легенда\n",
        "| Слой | Проекты |",
        "|------|---------|",
        "| Ingestion | Svyazi, CardIndex, Firecrawl |",
        "| Knowledge | AgentFS, knowledge-space |",
        "| Memory | Yodoca, NGT Memory, MemNet |",
        "| RAG | LiteParse, Legal RAG, Hybrid RAG, Graph RAG |",
        "| Orchestration | mclaude, AI Factory, Rufler, AutoResearch |",
        "| Security | LiteLLM, SENTINEL, Tool Search, Auto AI Router |",
        "| Sync | Yjs, Automerge |",
    ]

    out = DOCS / "MINDMAP.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
