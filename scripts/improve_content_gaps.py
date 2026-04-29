"""
improve_content_gaps.py — находит темы, упомянутые в docs/, но без собственного документа.

Логика:
  1. Собирает «упоминания» — слова/словосочетания, встречающиеся >= MIN_MENTIONS раз
     в разных файлах, похожие на названия проектов/концепций.
  2. Проверяет, есть ли документ, посвящённый этой теме.
  3. Выдаёт список пробелов с частотой и рекомендуемым местом создания файла.

Создаёт docs/CONTENT_GAPS.md.
Запуск: python scripts/improve_content_gaps.py
        python scripts/improve_content_gaps.py --min-mentions 3
        python scripts/improve_content_gaps.py --section 05-habr-projects
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

MIN_MENTIONS = 3
if "--min-mentions" in sys.argv:
    idx = sys.argv.index("--min-mentions")
    if idx + 1 < len(sys.argv):
        MIN_MENTIONS = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "CONTENT_GAPS.md", "SEARCH.md", "READABILITY.md", "SPELLCHECK.md",
    "BROKEN_LINKS.md", "COVERAGE.md", "STALENESS.md", "METRICS.md",
    "HEALTH.md", "SCORING.md", "ENTITIES.md", "CONTACTS.md",
}

# Технические термины — не считать «темами без документа»
KNOWN_TERMS = {
    "llm", "rag", "mcp", "api", "json", "yaml", "html", "markdown",
    "github", "git", "python", "linux", "docker", "kubernetes",
    "vector", "embedding", "index", "search", "query", "context",
    "model", "token", "prompt", "inference", "fine-tuning",
    "memory", "knowledge", "graph", "database", "cache",
    "workflow", "pipeline", "automation", "script", "plugin",
    "interface", "layer", "module", "service", "component",
    "user", "data", "file", "code", "text", "document",
    "version", "update", "change", "fix", "error", "issue",
    "claude", "anthropic", "openai", "gpt", "gemini",
    "habr", "github", "telegram", "slack",
    "svyazi", "yodoca", "agentfs", "ngt",
}

# Паттерны для поиска упоминаний концепций (CamelCase, аббревиатуры, «проекты»)
CONCEPT_PATTERNS = [
    # CamelCase слова (вероятно названия)
    r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b',
    # Аббревиатуры 2-6 букв в верхнем регистре
    r'\b[A-Z]{2,6}\b',
    # Русские словосочетания в кавычках
    r'«([^»]{5,40})»',
    r'"([^"]{5,40})"',
]


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    return text


def _extract_concepts(text: str) -> list[str]:
    clean = _clean(text)
    concepts = []
    for pat in CONCEPT_PATTERNS:
        concepts.extend(re.findall(pat, clean))
    # Фильтрация
    result = []
    for c in concepts:
        low = c.lower().strip()
        if len(low) < 3 or len(low) > 50:
            continue
        if low in KNOWN_TERMS:
            continue
        if re.match(r'^\d+$', low):
            continue
        result.append(c.strip())
    return result


def _has_dedicated_doc(term: str, all_files: list[Path]) -> Path | None:
    """Ищет файл, посвящённый данной теме (по имени файла)."""
    low = term.lower().replace(' ', '-').replace('_', '-')
    for f in all_files:
        fname = f.stem.lower().replace('_', '-').replace(' ', '-')
        if low in fname or fname in low:
            return f
    return None


def _suggest_location(term: str, sources: list[str]) -> str:
    """Предлагает папку для нового файла на основе источников."""
    source_paths = [Path(s) for s in sources]
    # Находим самую частую папку
    folder_counts: Counter = Counter()
    for sp in source_paths:
        parts = sp.parts
        if len(parts) > 1:
            folder_counts[parts[1]] += 1
    if folder_counts:
        best = folder_counts.most_common(1)[0][0]
        return f"docs/{best}/"
    return "docs/"


def main() -> None:
    print("🔍 improve_content_gaps.py — поиск тематических пробелов")

    target = SECTION_FILTER or DOCS
    all_files = [f for f in sorted(target.rglob("*.md")) if f.name not in SKIP_FILES]
    print(f"   Файлов: {len(all_files)}")
    print(f"   Мин. упоминаний: {MIN_MENTIONS}\n")

    # Подсчёт упоминаний по файлам (не просто сумма)
    # concept -> set of files where it's mentioned
    concept_files: dict[str, set[str]] = defaultdict(set)

    for f in all_files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        concepts = _extract_concepts(text)
        rel = str(f.relative_to(ROOT))
        for c in set(concepts):  # один файл — один голос
            concept_files[c].add(rel)

    # Отбираем концепции с достаточным числом упоминаний
    gaps = []
    for concept, files in concept_files.items():
        if len(files) < MIN_MENTIONS:
            continue
        dedicated = _has_dedicated_doc(concept, all_files)
        if dedicated:
            continue
        location = _suggest_location(concept, list(files))
        gaps.append({
            "concept": concept,
            "mentions": len(files),
            "files": sorted(files),
            "location": location,
        })

    gaps.sort(key=lambda x: -x["mentions"])

    lines = [
        "# Тематические пробелы (Content Gaps)\n",
        f"_Обновлено: {TODAY}_\n",
        f"Найдено пробелов: **{len(gaps)}** (мин. упоминаний: {MIN_MENTIONS})\n",
        "> Концепции, упоминаемые во многих файлах, но не имеющие собственного документа.\n",
    ]

    if gaps:
        lines += [
            "## Рекомендуется создать документы\n",
            "| Концепция | Упоминаний | Рекомендуемая папка |",
            "|-----------|-----------|-------------------|",
        ]
        for g in gaps[:50]:
            lines.append(
                f"| `{g['concept']}` | {g['mentions']} | `{g['location']}` |"
            )

        lines.append("\n## Детали по топ-20 пробелам\n")
        for g in gaps[:20]:
            lines.append(f"### `{g['concept']}` ({g['mentions']} файлов)\n")
            lines.append("Упоминается в:")
            for fpath in g["files"][:5]:
                lines.append(f"- `{fpath}`")
            if len(g["files"]) > 5:
                lines.append(f"- ... и ещё {len(g['files']) - 5} файлах")
            lines.append(f"\nСоздать: `{g['location']}{g['concept'].lower().replace(' ', '-')}.md`\n")
    else:
        lines.append("_Пробелов не найдено при текущем пороге._\n")

    out = DOCS / "CONTENT_GAPS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  пробелов: {len(gaps)}")
    if gaps:
        print(f"  топ-3: {', '.join(g['concept'] for g in gaps[:3])}")


if __name__ == "__main__":
    main()
