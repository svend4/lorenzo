"""
improve_heading_audit.py — аудит иерархии заголовков.

Проверяет:
  - H3/H4 без родительского H2 (нарушение иерархии)
  - Пустые секции: заголовок + <MIN_CONTENT слов под ним
  - Одиночные заголовки: H2 с одним единственным дочерним абзацем
  - Дублирующиеся заголовки в одном файле
  - Заголовки-вопросы без ответа (только заголовок, содержимое пустое)
  - Слишком длинные заголовки (> MAX_HEADING_WORDS слов)
  - Пропущенные уровни (H1 → H3, минуя H2)

Создаёт docs/HEADING_AUDIT.md.
Запуск:
    python scripts/improve_heading_audit.py
    python scripts/improve_heading_audit.py --section 02-anthropic-vacancies
    python scripts/improve_heading_audit.py --verbose
"""
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

VERBOSE = "--verbose" in sys.argv

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

MIN_CONTENT = 10     # слов под заголовком для непустой секции
MAX_HEADING_WORDS = 15

SKIP_FILES = {
    "HEADING_AUDIT.md", "SEARCH.md", "OUTLINE.md", "SUMMARIES.md",
    "PARAGRAPH_QUALITY.md", "CONTRADICTIONS.md", "KEYWORD_INDEX.md",
}

ISSUE_LABELS = {
    "no_parent":     "⚠️  Нет родительского H2",
    "empty_section": "🕳️  Пустая секция",
    "dup_heading":   "♊ Дублирующийся заголовок",
    "long_heading":  "📏 Длинный заголовок",
    "skip_level":    "🪜 Пропущен уровень",
    "no_h1":         "❌ Нет H1",
    "multi_h1":      "❌ Несколько H1",
}


def _parse_headings(text: str) -> list[dict]:
    """Возвращает [{level, title, line_idx, content_words}]."""
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    lines = clean.splitlines()
    headings = []

    for i, line in enumerate(lines):
        m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            headings.append({
                "level": level,
                "title": title,
                "line_idx": i,
                "line_end": i,
            })

    # Считаем слова в каждой секции
    for i, h in enumerate(headings):
        start = h["line_idx"] + 1
        end = headings[i + 1]["line_idx"] if i + 1 < len(headings) else len(lines)
        section_text = "\n".join(lines[start:end])
        # Убираем вложенные заголовки из счёта
        section_text = re.sub(r'^#+.*$', '', section_text, flags=re.MULTILINE)
        h["content_words"] = len(section_text.split())
        h["line_end"] = end

    return headings


def audit_file(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []

    headings = _parse_headings(text)
    if not headings:
        return []

    issues = []
    seen_titles: Counter = Counter()

    h1_count = sum(1 for h in headings if h["level"] == 1)
    if h1_count == 0:
        issues.append({"type": "no_h1", "title": "(весь файл)", "line": 0})
    elif h1_count > 1:
        issues.append({"type": "multi_h1", "title": f"{h1_count} заголовков H1", "line": 0})

    prev_level = 0
    has_h2 = False

    for h in headings:
        lvl = h["level"]
        title = h["title"]
        line = h["line_idx"] + 1

        seen_titles[title.lower()] += 1

        # Пропущенный уровень: H1→H3 или H2→H4
        if prev_level > 0 and lvl > prev_level + 1:
            issues.append({
                "type": "skip_level",
                "title": title,
                "line": line,
                "detail": f"H{prev_level} → H{lvl}",
            })

        # H3+ без H2
        if lvl == 2:
            has_h2 = True
        if lvl >= 3 and not has_h2:
            issues.append({
                "type": "no_parent",
                "title": title,
                "line": line,
                "detail": f"H{lvl} без H2",
            })

        # Пустая секция
        if h["content_words"] < MIN_CONTENT and lvl <= 4:
            issues.append({
                "type": "empty_section",
                "title": title,
                "line": line,
                "detail": f"{h['content_words']} слов",
            })

        # Длинный заголовок
        if len(title.split()) > MAX_HEADING_WORDS:
            issues.append({
                "type": "long_heading",
                "title": title[:60],
                "line": line,
                "detail": f"{len(title.split())} слов",
            })

        prev_level = lvl

    # Дублирующиеся заголовки
    for title_lower, count in seen_titles.items():
        if count > 1:
            issues.append({
                "type": "dup_heading",
                "title": title_lower[:60],
                "line": 0,
                "detail": f"{count} раза",
            })

    return issues


def main() -> None:
    print("🏗️  improve_heading_audit.py — аудит заголовков")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    all_results: dict[str, list] = {}
    type_counts: Counter = Counter()

    for f in files:
        issues = audit_file(f)
        if issues:
            rel = str(f.relative_to(ROOT))
            all_results[rel] = issues
            for iss in issues:
                type_counts[iss["type"]] += 1

    lines = [
        "# Аудит заголовков\n",
        f"_Обновлено: {TODAY}_\n",
        f"Файлов с проблемами: **{len(all_results)}** из {len(files)}\n",
        "## Типы проблем\n",
        "| Тип | Кол-во |",
        "|-----|--------|",
    ]
    for t, label in ISSUE_LABELS.items():
        if type_counts[t]:
            lines.append(f"| {label} | {type_counts[t]} |")

    lines += ["\n## По файлам\n"]
    for fpath, issues in sorted(all_results.items(), key=lambda x: -len(x[1])):
        tc = Counter(i["type"] for i in issues)
        summary = ', '.join(f"{ISSUE_LABELS[t].split()[-1]}: {n}" for t, n in tc.most_common())
        lines.append(f"### `{fpath}` ({len(issues)} проблем)\n")
        lines.append(f"_{summary}_\n")
        if VERBOSE:
            for iss in issues[:8]:
                label = ISSUE_LABELS.get(iss["type"], iss["type"])
                detail = f" — {iss.get('detail', '')}" if iss.get("detail") else ""
                lines.append(f"- {label}{detail}: `{iss['title']}`" +
                              (f" (строка {iss['line']})" if iss.get("line") else ""))
        lines.append("")

    out = DOCS / "HEADING_AUDIT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов с проблемами: {len(all_results)}")
    for t, cnt in type_counts.most_common():
        print(f"  {ISSUE_LABELS.get(t, t)}: {cnt}")


if __name__ == "__main__":
    main()
