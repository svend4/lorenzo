"""
improve_crossrefs.py — строит карту перекрёстных ссылок между файлами.
Создаёт docs/CROSSREFS.md: какой файл упоминает какие проекты,
и для каждого проекта — список файлов где он встречается.
Запуск: python scripts/improve_crossrefs.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

PROJECTS = [
    "Svyazi", "CardIndex", "AgentFS", "knowledge-space", "mclaude",
    "AI Factory", "AIF Handoff", "Rufler", "LiteParse", "Legal RAG",
    "Hybrid RAG", "Graph RAG", "Yodoca", "NGT Memory", "MemNet",
    "agent-memory-mcp", "Memory OS", "SENTINEL", "LiteLLM",
    "Auto AI Router", "Tool Search", "RLM-Toolkit", "AutoResearch",
    "Sequential", "Wikontic", "Firecrawl", "Yjs", "Automerge",
    "Whisper", "Yttri",
]


def build_index() -> dict[str, list[str]]:
    """Проект → список файлов где упоминается."""
    index: dict[str, list[str]] = defaultdict(list)
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in ("README.md", "CROSSREFS.md", "GLOSSARY.md"):
            continue
        text = f.read_text(encoding="utf-8")
        rel = str(f.relative_to(ROOT))
        for proj in PROJECTS:
            if proj.lower() in text.lower():
                index[proj].append(rel)
    return index


def build_file_map() -> dict[str, list[str]]:
    """Файл → список проектов которые в нём упоминаются."""
    fmap: dict[str, list[str]] = defaultdict(list)
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in ("README.md", "CROSSREFS.md", "GLOSSARY.md"):
            continue
        text = f.read_text(encoding="utf-8")
        rel = str(f.relative_to(ROOT))
        for proj in PROJECTS:
            if proj.lower() in text.lower():
                fmap[rel].append(proj)
    return fmap


def main():
    print("Строю индекс перекрёстных ссылок...")
    proj_index = build_index()
    file_map = build_file_map()

    lines = [
        "# Перекрёстные ссылки\n",
        "## Проекты → файлы\n",
        "Для каждого проекта — в каких файлах он упоминается.\n",
        "| Проект | Файлов | Где упоминается |",
        "|--------|--------|-----------------|",
    ]

    for proj in sorted(PROJECTS):
        files = proj_index.get(proj, [])
        if not files:
            continue
        # Первые 3 файла для краткости
        sample = ", ".join(f"`{f}`" for f in files[:3])
        if len(files) > 3:
            sample += f" +{len(files)-3}"
        lines.append(f"| **{proj}** | {len(files)} | {sample} |")

    lines.append("\n## Файлы → проекты\n")
    lines.append("Топ-20 файлов с наибольшим числом упоминаемых проектов.\n")
    lines.append("| Файл | Проектов | Список |")
    lines.append("|------|----------|--------|")

    top_files = sorted(file_map.items(), key=lambda x: -len(x[1]))[:20]
    for fpath, projs in top_files:
        proj_list = ", ".join(projs[:6])
        if len(projs) > 6:
            proj_list += f" +{len(projs)-6}"
        lines.append(f"| `{fpath}` | {len(projs)} | {proj_list} |")

    out = DOCS / "CROSSREFS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  проектов в индексе: {len(proj_index)}")
    print(f"  файлов проиндексировано: {len(file_map)}")


if __name__ == "__main__":
    main()
