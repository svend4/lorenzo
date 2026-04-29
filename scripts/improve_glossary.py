"""
improve_glossary.py — извлекает все проекты, авторов и URL из docs/,
создаёт docs/GLOSSARY.md и docs/AUTHORS.md.
Запуск: python scripts/improve_glossary.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Известные проекты
PROJECTS = [
    "Svyazi", "CardIndex", "AgentFS", "knowledge-space", "mclaude",
    "AI Factory", "AIF Handoff", "Rufler", "LiteParse", "Legal RAG",
    "Hybrid RAG", "Graph RAG", "Yodoca", "NGT Memory", "MemNet",
    "agent-memory-mcp", "Memory OS", "SENTINEL", "LiteLLM",
    "Auto AI Router", "Tool Search", "RLM-Toolkit", "AutoResearch",
    "Sequential", "Wikontic", "Firecrawl", "Yjs", "Automerge",
    "Whisper", "Yttri", "OpenWhispr", "Self-Aware MCP",
]

# Известные авторы
AUTHORS = [
    "Андрей Чуян", "andrey_chuyan",
    "Виталий Оборин", "VitalyOborin",
    "kksudo", "spbmolot",
    "AnastasiyaW", "Sonia_Black",
    "lee-to", "Cutcode",
    "zodigancode", "lib4u",
    "nlaik", "iximy", "tagir_analyzes",
    "VladSpace", "vpakspace",
    "Antipozitive", "VitaliySemenov", "moshael",
    "akazant", "akzhankalimatov",
    "Dmitriila", "BerriAI", "MiXaiLL76",
]


def find_mentions(docs_text: str, terms: list[str]) -> dict[str, list[str]]:
    """Для каждого термина находит файлы, где он упоминается."""
    mentions = defaultdict(list)
    for f in DOCS.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        for term in terms:
            if term.lower() in text.lower():
                mentions[term].append(str(f.relative_to(ROOT)))
    return mentions


def extract_urls(text: str) -> list[str]:
    return re.findall(r'https?://[^\s\)\]"]+', text)


def make_glossary():
    print("Извлечение упоминаний проектов...")
    project_mentions = find_mentions("", PROJECTS)

    lines = ["# Глоссарий проектов\n",
             "Все проекты, упоминаемые в документах, с количеством файлов.\n",
             "| Проект | Упоминается в файлах |",
             "|--------|---------------------|"]

    for proj in sorted(PROJECTS):
        files = project_mentions.get(proj, [])
        count = len(files)
        lines.append(f"| **{proj}** | {count} |")

    out = DOCS / "GLOSSARY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


def make_authors():
    print("Извлечение упоминаний авторов...")
    author_mentions = find_mentions("", AUTHORS)

    lines = ["# Авторы и коллаборации\n",
             "Авторы проектов, упоминаемые в исследованиях.\n",
             "| Автор | Упоминается в файлах |",
             "|-------|---------------------|"]

    for author in sorted(AUTHORS):
        files = author_mentions.get(author, [])
        count = len(files)
        if count > 0:
            lines.append(f"| **{author}** | {count} |")

    out = DOCS / "AUTHORS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


def make_url_index():
    print("Извлечение URL...")
    all_urls = defaultdict(set)

    for f in DOCS.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        for url in extract_urls(text):
            all_urls[url].add(str(f.relative_to(ROOT)))

    lines = ["# Индекс ссылок\n",
             f"Всего уникальных URL: {len(all_urls)}\n",
             "| URL | Найден в файлах |",
             "|-----|-----------------|"]

    for url, files in sorted(all_urls.items())[:200]:  # топ 200
        count = len(files)
        lines.append(f"| {url} | {count} |")

    out = DOCS / "LINKS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    make_glossary()
    make_authors()
    make_url_index()
    print("Готово.")
