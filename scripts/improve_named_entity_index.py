"""
improve_named_entity_index.py — индекс именованных сущностей из всей базы.

Извлекает без ML (по паттернам и словарям):
  - Люди: CamelCase имена, известные авторы из CONTACTS.md
  - Проекты/Продукты: слова из ENTITIES.md + CamelCase + GitHub-ссылки
  - Технологии: из словаря tech-терминов
  - Организации: Inc, Ltd, GmbH, LLC + известные
  - Даты: 2020–2026, Q1/Q2, «в январе», «через N месяцев»

Создаёт docs/NAMED_ENTITIES.md + docs/named_entities.json.
Запуск:
    python scripts/improve_named_entity_index.py
    python scripts/improve_named_entity_index.py --section 05-habr-projects
    python scripts/improve_named_entity_index.py --type people
    python scripts/improve_named_entity_index.py --min-mentions 2
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

MIN_MENTIONS = 2
if "--min-mentions" in sys.argv:
    idx = sys.argv.index("--min-mentions")
    if idx + 1 < len(sys.argv):
        MIN_MENTIONS = int(sys.argv[idx + 1])

TYPE_FILTER = None
if "--type" in sys.argv:
    idx = sys.argv.index("--type")
    if idx + 1 < len(sys.argv):
        TYPE_FILTER = sys.argv[idx + 1]

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "NAMED_ENTITIES.md", "ENTITIES.md", "SEARCH.md", "CONTACTS.md",
    "READABILITY.md", "SPELLCHECK.md", "SOURCE_MAP.md",
}

# ─── Словари ───────────────────────────────────────────────────────────────

KNOWN_PEOPLE = {
    "kksudo", "spbmolot", "vitalyoborin", "anastasiyaw", "andrey_chuyan",
    "svend4", "claude", "anthropic",
}

KNOWN_PROJECTS = {
    "agentfs", "ngt", "yodoca", "svyazi", "wikontic", "memnet",
    "knowledge-space", "nautilus", "lorenzo",
    "claude", "gpt", "gemini", "llama", "mistral",
    "langchain", "llamaindex", "chromadb", "weaviate", "qdrant",
    "faiss", "elasticsearch", "opensearch",
    "obsidian", "notion", "confluence", "github",
}

KNOWN_TECH = {
    "llm", "rag", "mcp", "api", "json", "yaml", "sql", "nosql",
    "python", "rust", "go", "typescript", "javascript",
    "docker", "kubernetes", "terraform",
    "postgresql", "sqlite", "redis", "mongodb",
    "bert", "gpt", "transformer", "embedding", "vector",
    "tfidf", "bm25", "cosine", "jaccard",
    "fastapi", "flask", "django", "react", "vue",
    "markdown", "html", "css",
    "git", "github", "gitlab", "ci", "cd",
    "grpc", "graphql", "rest", "webhook",
}

KNOWN_ORGS = {
    "anthropic", "openai", "google", "microsoft", "meta", "yandex",
    "сбер", "тинькофф", "озон", "вк", "mail",
}

# ─── Паттерны ──────────────────────────────────────────────────────────────

DATE_PATTERNS = [
    re.compile(r'\b(20[12]\d[-/](0[1-9]|1[0-2])(?:[-/]\d{1,2})?)\b'),
    re.compile(r'\b(Q[1-4]\s*20[12]\d|20[12]\d\s*Q[1-4])\b', re.IGNORECASE),
    re.compile(r'\b(январ[еьяи]|феврал[еьяи]|март[еа]?|апрел[еьяи]|ма[йе]|июн[еьяи]'
               r'|июл[еьяи]|август[еа]?|сентябр[еьяи]|октябр[еьяи]|ноябр[еьяи]|декабр[еьяи])'
               r'\s+20[12]\d\b', re.IGNORECASE),
    re.compile(r'\bв\s+20[12]\d\s+год[ау]?\b', re.IGNORECASE),
]

CAMEL_CASE_RE = re.compile(r'\b[A-Z][a-z]{2,}(?:[A-Z][a-z]{2,})+\b')
GITHUB_RE = re.compile(r'github\.com/([A-Za-z0-9_-]+)/([A-Za-z0-9_-]+)')
ORG_SUFFIX_RE = re.compile(r'\b([A-Z][A-Za-z]+)\s+(?:Inc|Ltd|LLC|GmbH|Corp|АО|ООО)\b')


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    return text


def _extract_entities(text: str, path: Path) -> dict[str, list[str]]:
    """Возвращает {тип: [сущность, ...]}."""
    clean = _clean(text)
    entities: dict[str, list[str]] = {
        "people": [], "projects": [], "tech": [], "orgs": [], "dates": [],
    }

    lower = clean.lower()

    # Люди
    for name in KNOWN_PEOPLE:
        if name in lower:
            entities["people"].append(name)

    # GitHub авторы/репозитории
    for m in GITHUB_RE.finditer(clean):
        user, repo = m.group(1).lower(), m.group(2).lower()
        if user not in ("svend4",):
            entities["people"].append(user)
        entities["projects"].append(repo)

    # Проекты по словарю
    for proj in KNOWN_PROJECTS:
        if re.search(rf'\b{re.escape(proj)}\b', lower):
            entities["projects"].append(proj)

    # CamelCase — вероятно названия
    for m in CAMEL_CASE_RE.finditer(clean):
        word = m.group(0)
        if len(word) > 4 and word.lower() not in ("False", "True", "None"):
            entities["projects"].append(word)

    # Технологии
    for tech in KNOWN_TECH:
        if re.search(rf'\b{re.escape(tech)}\b', lower):
            entities["tech"].append(tech)

    # Организации
    for org in KNOWN_ORGS:
        if org in lower:
            entities["orgs"].append(org)
    for m in ORG_SUFFIX_RE.finditer(clean):
        entities["orgs"].append(m.group(1))

    # Даты
    for pat in DATE_PATTERNS:
        for m in pat.finditer(clean):
            entities["dates"].append(m.group(0).strip())

    # Дедупликация
    return {k: list(set(v)) for k, v in entities.items()}


def main() -> None:
    print("🏷️  improve_named_entity_index.py — индекс именованных сущностей")
    print(f"   Мин. упоминаний: {MIN_MENTIONS}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "obsidian" not in str(f)
             and "confluence" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    # entity -> {type, files: set, total_count}
    entity_data: dict[str, dict] = {}

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = str(f.relative_to(ROOT))
        found = _extract_entities(text, f)

        for etype, names in found.items():
            if TYPE_FILTER and etype != TYPE_FILTER:
                continue
            for name in names:
                key = name.lower().strip()
                if not key or len(key) < 2:
                    continue
                if key not in entity_data:
                    entity_data[key] = {
                        "name": name, "type": etype,
                        "files": set(), "count": 0,
                    }
                entity_data[key]["files"].add(rel)
                entity_data[key]["count"] += 1

    # Фильтрация по MIN_MENTIONS
    filtered = {
        k: v for k, v in entity_data.items()
        if len(v["files"]) >= MIN_MENTIONS
    }

    # По типу
    by_type: dict[str, list] = defaultdict(list)
    for key, data in filtered.items():
        by_type[data["type"]].append((key, data))

    # Сортировка по частоте
    for etype in by_type:
        by_type[etype].sort(key=lambda x: -len(x[1]["files"]))

    # Формируем отчёт
    type_icons = {
        "people": "👤", "projects": "📦", "tech": "⚙️",
        "orgs": "🏢", "dates": "📅",
    }

    lines = [
        "# Индекс именованных сущностей\n",
        f"_Обновлено: {TODAY}_\n",
        f"Всего сущностей: **{len(filtered)}** (мин. {MIN_MENTIONS} упоминаний)\n",
    ]

    for etype in ["people", "projects", "tech", "orgs", "dates"]:
        if TYPE_FILTER and etype != TYPE_FILTER:
            continue
        items = by_type.get(etype, [])
        if not items:
            continue
        icon = type_icons[etype]
        lines += [
            f"\n## {icon} {etype.title()} ({len(items)})\n",
            "| Сущность | Файлов | Тип |",
            "|----------|--------|-----|",
        ]
        for key, data in items[:40]:
            files_count = len(data["files"])
            lines.append(f"| `{data['name']}` | {files_count} | {etype} |")

        # Детали топ-5
        lines.append(f"\n**Топ-5 по упоминаниям:**\n")
        for key, data in items[:5]:
            lines.append(f"### `{data['name']}` ({len(data['files'])} файлов)\n")
            for fp in sorted(data["files"])[:5]:
                lines.append(f"- `{fp}`")
            if len(data["files"]) > 5:
                lines.append(f"- _...ещё {len(data['files'])-5}_")
            lines.append("")

    out_md = DOCS / "NAMED_ENTITIES.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # JSON для machine-readable использования
    json_data = {
        key: {
            "name": v["name"], "type": v["type"],
            "files": sorted(v["files"]), "mention_count": v["count"],
        }
        for key, v in filtered.items()
    }
    out_json = DOCS / "named_entities.json"
    out_json.write_text(
        json.dumps(json_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"  wrote: {out_md.relative_to(ROOT)}")
    print(f"  wrote: {out_json.relative_to(ROOT)}")
    for etype, items in by_type.items():
        print(f"  {type_icons.get(etype, '·')} {etype}: {len(items)}")


if __name__ == "__main__":
    main()
