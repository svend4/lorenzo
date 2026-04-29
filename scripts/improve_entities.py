"""
improve_entities.py — извлечение именованных сущностей из docs/.
Категории: люди, проекты, организации, технологии, URL/репозитории.
Создаёт docs/ENTITIES.md.
Запуск: python scripts/improve_entities.py
"""
import re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Списки известных сущностей
PEOPLE = [
    "Андрей", "Виталий", "kksudo", "spbmolot", "Lorenzo",
    "svend4", "Свенд", "Антропик",
]

PROJECTS = [
    "Svyazi", "CardIndex", "AgentFS", "Yodoca", "NGT", "SENTINEL",
    "Rufler", "AI Factory", "mclaude", "LiteParse", "Firecrawl",
    "knowledge-space", "Wikontic", "MemNet", "agent-memory-mcp",
    "Nautilus", "Lorenzo", "Cowork", "ingit", "AgentPool",
    "MCP Tool Search", "Shield", "SGB",
]

ORGS = [
    "Anthropic", "OpenAI", "Google", "Хабр", "GitHub", "Obsidian",
    "Habr", "Claude", "ChatGPT",
]

TECH = [
    "MCP", "RAG", "LLM", "CRDT", "TF-IDF", "Mermaid", "FAISS",
    "JSON", "YAML", "OAuth", "JWT", "REST", "GraphQL", "WebSocket",
    "Python", "TypeScript", "Rust", "SQLite", "PostgreSQL",
    "MIT", "Apache", "BSL", "FastAPI", "LangChain",
]

SKIP = {"ENTITIES.md", "GLOSSARY.md", "AUTHORS.md"}


def find_github_urls(text: str) -> list[str]:
    urls = re.findall(r'https?://github\.com/[\w\-]+/[\w\-]+', text)
    return list(set(urls))


def count_entity(text: str, entity: str) -> int:
    pattern = re.compile(re.escape(entity), re.IGNORECASE)
    return len(pattern.findall(text))


def build_counts(entity_list: list[str], all_texts: dict[str, str]) -> list[tuple]:
    results = []
    for ent in entity_list:
        total = sum(count_entity(t, ent) for t in all_texts.values())
        if total == 0:
            continue
        files = [f for f, t in all_texts.items() if count_entity(t, ent) > 0]
        results.append((ent, total, len(files)))
    return sorted(results, key=lambda x: -x[1])


def main():
    print("Извлечение именованных сущностей...")

    all_texts: dict[str, str] = {}
    all_github: list[str] = []

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        rel = str(f.relative_to(ROOT))
        all_texts[rel] = text
        all_github.extend(find_github_urls(text))

    github_counter = Counter(all_github)

    people_data  = build_counts(PEOPLE,   all_texts)
    project_data = build_counts(PROJECTS, all_texts)
    org_data     = build_counts(ORGS,     all_texts)
    tech_data    = build_counts(TECH,     all_texts)

    def table(rows: list[tuple], header="Сущность") -> list[str]:
        out = [f"| {header} | Упоминаний | Файлов |",
               "|---------|------------|--------|"]
        for ent, total, files in rows:
            out.append(f"| **{ent}** | {total} | {files} |")
        return out

    lines = [
        "# Именованные сущности\n",
        f"**Файлов просмотрено:** {len(all_texts)}\n",

        f"\n## Люди и авторы ({len(people_data)})\n",
    ] + table(people_data, "Имя") + [

        f"\n## Проекты ({len(project_data)})\n",
    ] + table(project_data, "Проект") + [

        f"\n## Организации ({len(org_data)})\n",
    ] + table(org_data, "Организация") + [

        f"\n## Технологии и стандарты ({len(tech_data)})\n",
    ] + table(tech_data, "Технология") + [

        f"\n## GitHub репозитории ({len(github_counter)})\n",
        "| Репозиторий | Упоминаний |",
        "|-------------|------------|",
    ]

    for url, cnt in github_counter.most_common(30):
        lines.append(f"| [{url}]({url}) | {cnt} |")

    # Ко-встречаемость проектов
    lines += ["\n## Ко-встречаемость проектов (топ пары)\n",
              "| Пара | Общих файлов |",
              "|------|-------------|"]
    proj_files: dict[str, set] = {}
    for ent, _, _ in project_data:
        proj_files[ent] = {f for f, t in all_texts.items() if count_entity(t, ent) > 0}

    pairs = []
    proj_names = [e for e, _, _ in project_data]
    for i in range(len(proj_names)):
        for j in range(i+1, len(proj_names)):
            a, b = proj_names[i], proj_names[j]
            common = len(proj_files.get(a, set()) & proj_files.get(b, set()))
            if common >= 3:
                pairs.append((a, b, common))
    for a, b, c in sorted(pairs, key=lambda x: -x[2])[:20]:
        lines.append(f"| {a} ↔ {b} | {c} |")

    out = DOCS / "ENTITIES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  людей: {len(people_data)}, проектов: {len(project_data)}, "
          f"орг: {len(org_data)}, технологий: {len(tech_data)}, "
          f"GitHub URL: {len(github_counter)}")


if __name__ == "__main__":
    main()
