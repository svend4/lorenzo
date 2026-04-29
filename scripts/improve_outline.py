"""
improve_outline.py — строит иерархический outline всей базы знаний.

Генерирует два вида оглавления:
  1. По структуре папок + заголовкам H1/H2 каждого файла
  2. По темам (TF-IDF кластеры) — тематическая карта

Создаёт docs/OUTLINE.md.
Запуск:
    python scripts/improve_outline.py
    python scripts/improve_outline.py --depth 3      # H1+H2+H3
    python scripts/improve_outline.py --section 01-svyazi
    python scripts/improve_outline.py --format tree  # ASCII-дерево
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date
import math

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

MAX_DEPTH = 2
if "--depth" in sys.argv:
    idx = sys.argv.index("--depth")
    if idx + 1 < len(sys.argv):
        MAX_DEPTH = int(sys.argv[idx + 1])

FORMAT = "markdown"
if "--format" in sys.argv:
    idx = sys.argv.index("--format")
    if idx + 1 < len(sys.argv):
        FORMAT = sys.argv[idx + 1]

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "OUTLINE.md", "SEARCH.md", "READABILITY.md", "SPELLCHECK.md",
    "CONTENT_GAPS.md", "LINK_PREVIEW.md", "BROKEN_LINKS.md",
    "COVERAGE.md", "STALENESS.md", "TOPIC_MODEL.md", "CITATION_INDEX.md",
    "READING_TIME.md", "VERSION_DIFF.md", "GITHUB_ISSUES.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "the", "a", "an", "is", "are",
    "of", "in", "on", "to", "for", "with", "by", "and", "not",
}


def _word_count(text: str) -> int:
    return len(re.findall(r'\S+', text))


def _extract_headings(text: str, max_level: int = 3) -> list[tuple[int, str]]:
    """Возвращает [(уровень, заголовок)]."""
    result = []
    for m in re.finditer(r'^(#{1,%d})\s+(.+)$' % max_level, text, re.MULTILINE):
        level = len(m.group(1))
        title = m.group(2).strip()
        # Убираем разметку
        title = re.sub(r'[`*_]', '', title)
        result.append((level, title))
    return result


def _extract_summary(text: str) -> str:
    """Первые 120 символов текста после H1."""
    lines = text.split('\n')
    found_h1 = False
    for line in lines:
        line = line.strip()
        if re.match(r'^#\s', line):
            found_h1 = True
            continue
        if found_h1 and line and not line.startswith('#') and not line.startswith('<!--'):
            clean = re.sub(r'[*_`\[\]|]', '', line)
            return clean[:120] + ('…' if len(clean) > 120 else '')
    return ""


def _section_label(path: Path) -> str:
    """Человекочитаемое название секции."""
    name = path.name
    # Убираем ведущие цифры
    name = re.sub(r'^\d+-', '', name)
    return name.replace('-', ' ').replace('_', ' ').title()


def _build_tree_section(section_dir: Path, files: list[Path]) -> list[str]:
    """Строит outline одной секции."""
    lines = []
    section_name = _section_label(section_dir)
    rel = section_dir.relative_to(ROOT)
    lines.append(f"\n## 📁 {section_name} (`{rel}/`)\n")

    total_words = 0
    for f in sorted(files):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        words = _word_count(text)
        total_words += words
        rel_f = f.relative_to(ROOT)

        headings = _extract_headings(text, MAX_DEPTH)
        summary = _extract_summary(text)

        # Первый заголовок = название документа
        h1 = headings[0][1] if headings else f.stem.replace('-', ' ').title()
        lines.append(f"### [{h1}]({rel_f})")
        if summary:
            lines.append(f"> {summary}\n")

        # Подзаголовки H2+
        sub = [(lv, t) for lv, t in headings[1:] if lv <= MAX_DEPTH]
        for lv, title in sub[:8]:
            indent = "  " * (lv - 1)
            lines.append(f"{indent}- {title}")
        if len(sub) > 8:
            lines.append(f"  _... ещё {len(sub)-8} разделов_")
        lines.append(f"\n_Слов: {words}_\n")

    lines.append(f"**Итого в секции: {total_words:,} слов, {len(files)} файлов**\n")
    return lines


def _build_thematic_map(all_files: list[Path]) -> list[str]:
    """Строит тематическую карту на основе TF-IDF."""
    # Простая TF без IDF для скорости
    topic_files: dict[str, list[tuple[Path, float]]] = defaultdict(list)

    # Определяем доминирующую тему по топ-словам
    TOPICS = {
        "архитектура": {"архитектура", "слой", "уровень", "компонент", "система", "architecture", "layer"},
        "агенты": {"агент", "agent", "мультиагент", "workflow", "оркестрация", "llm"},
        "память": {"память", "memory", "хранение", "кэш", "retrieval", "vector", "embedding"},
        "проекты": {"проект", "project", "github", "репозиторий", "oss", "habr"},
        "контакты": {"автор", "контакт", "сообщение", "collaboration", "partner"},
        "анализ": {"анализ", "analysis", "исследование", "сравнение", "метрика"},
        "код": {"код", "code", "python", "скрипт", "api", "функция"},
        "документация": {"документ", "document", "markdown", "описание", "шаблон"},
    }

    for f in all_files:
        try:
            text = f.read_text(encoding="utf-8").lower()
        except Exception:
            continue
        tokens = set(re.findall(r'[а-яёa-z]{4,}', text))

        scores: dict[str, int] = {}
        for topic, keywords in TOPICS.items():
            scores[topic] = len(tokens & keywords)

        if scores:
            best = max(scores, key=lambda k: scores[k])
            score = scores[best]
            if score > 0:
                topic_files[best].append((f, score))

    lines = ["\n## 🗺️ Тематическая карта\n"]
    for topic, file_scores in sorted(topic_files.items(), key=lambda x: -len(x[1])):
        top_files = sorted(file_scores, key=lambda x: -x[1])[:5]
        lines.append(f"### {topic.title()} ({len(file_scores)} документов)")
        for f, score in top_files:
            rel = f.relative_to(ROOT)
            lines.append(f"- [`{f.stem}`]({rel})")
        if len(file_scores) > 5:
            lines.append(f"- _... ещё {len(file_scores)-5}_")
        lines.append("")

    return lines


def main() -> None:
    print("📋 improve_outline.py — иерархический outline базы знаний")
    print(f"   Глубина заголовков: H1–H{MAX_DEPTH}\n")

    target = SECTION_FILTER or DOCS

    # Собираем файлы по секциям
    by_section: dict[Path, list[Path]] = defaultdict(list)
    all_files = []
    for f in sorted(target.rglob("*.md")):
        if f.name in SKIP_FILES:
            continue
        if "obsidian" in str(f) or "confluence" in str(f) or "merged" in str(f):
            continue
        # Определяем секцию (папку)
        rel = f.relative_to(target)
        if len(rel.parts) == 1:
            section = target
        else:
            section = target / rel.parts[0]
        by_section[section].append(f)
        all_files.append(f)

    total_files = sum(len(v) for v in by_section.values())
    total_words = 0
    print(f"   Секций: {len(by_section)}  |  Файлов: {total_files}\n")

    lines = [
        "# Outline базы знаний\n",
        f"_Обновлено: {TODAY}_\n",
        f"Секций: **{len(by_section)}** | Файлов: **{total_files}**\n",
        "## Содержание\n",
    ]

    # Оглавление секций
    for section in sorted(by_section.keys()):
        label = _section_label(section)
        count = len(by_section[section])
        anchor = label.lower().replace(' ', '-')
        lines.append(f"- [{label}](#{anchor}) — {count} файлов")
    lines.append("")

    # Детальный outline по секциям
    for section in sorted(by_section.keys()):
        files = by_section[section]
        section_lines = _build_tree_section(section, files)
        lines.extend(section_lines)

    # Тематическая карта
    lines.extend(_build_thematic_map(all_files))

    out = DOCS / "OUTLINE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  секций: {len(by_section)}, файлов: {total_files}")


if __name__ == "__main__":
    main()
