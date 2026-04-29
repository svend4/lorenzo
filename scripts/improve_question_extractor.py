"""
improve_question_extractor.py — извлечение вопросов, гипотез и TODO.

Ищет в текстах:
  - Вопросы: предложения с «?» или «как», «почему», «зачем», «что если»
  - Гипотезы: «возможно», «предположим», «скорее всего», «вероятно»
  - TODO/Ideas: «нужно», «стоит», «следует», «можно было бы», «планируется»
  - Открытые вопросы: «неясно», «непонятно», «требует изучения»

Создаёт docs/QUESTIONS.md — база открытых вопросов из всей базы знаний.
Запуск:
    python scripts/improve_question_extractor.py
    python scripts/improve_question_extractor.py --section 05-habr-projects
    python scripts/improve_question_extractor.py --type questions
    python scripts/improve_question_extractor.py --min-words 8
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

TYPE_FILTER = None
if "--type" in sys.argv:
    idx = sys.argv.index("--type")
    if idx + 1 < len(sys.argv):
        TYPE_FILTER = sys.argv[idx + 1]

MIN_WORDS = 6
if "--min-words" in sys.argv:
    idx = sys.argv.index("--min-words")
    if idx + 1 < len(sys.argv):
        MIN_WORDS = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "QUESTIONS.md", "SEARCH.md", "HEADING_AUDIT.md", "CONTRADICTIONS.md",
    "PARAGRAPH_QUALITY.md", "VOCABULARY.md", "LANGUAGE_STATS.md",
}

# Паттерны по типам
PATTERNS = {
    "question": re.compile(
        r'\?|'
        r'\bкак\s+(?:это|можно|лучше|правильно|работает)\b|'
        r'\bпочему\b|\bзачем\b|'
        r'\bчто\s+если\b|\bчто\s+будет\b|'
        r'\bhow\s+(?:to|does|can|should)\b|\bwhy\b|\bwhat\s+if\b',
        re.I
    ),
    "hypothesis": re.compile(
        r'\bвозможно\b|\bпредположим\b|\bскорее\s+всего\b|\bвероятно\b|'
        r'\bможет\s+быть\b|\bесли\s+предположить\b|'
        r'\bperhaps\b|\bprobably\b|\bmight\b|\bassume\b|\bhypothes',
        re.I
    ),
    "todo": re.compile(
        r'\bнужно\s+(?:будет|проверить|реализовать|добавить|изучить)\b|'
        r'\bстоит\s+(?:рассмотреть|проверить|добавить|изучить)\b|'
        r'\bследует\b|\bпланируется\b|\bбудет\s+реализовано\b|'
        r'\bTODO\b|\bFIXME\b|\bHACK\b|'
        r'\bneed\s+to\b|\bshould\s+(?:be|consider|check)\b|\bplan\s+to\b',
        re.I
    ),
    "open": re.compile(
        r'\bнеясно\b|\bнепонятно\b|\bтребует\s+(?:изучения|уточнения|проверки)\b|'
        r'\bостаётся\s+открытым\b|\bпод\s+вопросом\b|'
        r'\bunclear\b|\bopen\s+question\b|\bneeds?\s+(?:investigation|clarification)\b',
        re.I
    ),
}

TYPE_LABELS = {
    "question":   "❓ Вопрос",
    "hypothesis": "💭 Гипотеза",
    "todo":       "📌 TODO/Идея",
    "open":       "🔓 Открытый вопрос",
}


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[*_`|>\[\]]', ' ', text)
    return text


def _split_sentences(text: str) -> list[str]:
    clean = _clean(text)
    sents = re.split(r'(?<=[.!?])\s+|\n', clean)
    return [s.strip() for s in sents if len(s.split()) >= MIN_WORDS]


def _current_heading(text: str, char_pos: int) -> str:
    before = text[:char_pos]
    matches = list(re.finditer(r'^#{1,3}\s+(.+)$', before, re.MULTILINE))
    if matches:
        return matches[-1].group(1).strip()[:60]
    return ""


def extract_from_file(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []

    source = str(path.relative_to(ROOT))
    clean_text = _clean(text)
    sentences = _split_sentences(clean_text)
    found = []

    for sent in sentences:
        types_found = []
        for typ, pattern in PATTERNS.items():
            if TYPE_FILTER and typ != TYPE_FILTER:
                continue
            if pattern.search(sent):
                types_found.append(typ)

        if types_found:
            # Позиция в тексте для поиска заголовка
            pos = clean_text.find(sent[:40])
            heading = _current_heading(text, max(0, pos)) if pos >= 0 else ""
            found.append({
                "types": types_found,
                "primary_type": types_found[0],
                "sentence": sent[:200].strip(),
                "source": source,
                "heading": heading,
            })

    return found


def main() -> None:
    print("❓ improve_question_extractor.py — вопросы и гипотезы")
    if TYPE_FILTER:
        print(f"   Тип: {TYPE_FILTER}")
    print(f"   Мин. слов: {MIN_WORDS}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    all_items: list[dict] = []
    for f in files:
        items = extract_from_file(f)
        all_items.extend(items)

    by_type: dict[str, list] = defaultdict(list)
    for item in all_items:
        by_type[item["primary_type"]].append(item)

    print(f"   Найдено: {len(all_items)}")
    for typ, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
        print(f"   {TYPE_LABELS[typ]}: {len(items)}")

    lines = [
        "# Вопросы и открытые темы из базы знаний\n",
        f"_Обновлено: {TODAY}_\n",
        f"Всего: **{len(all_items)}** | Файлов: **{len(files)}**\n",
        "## Сводка\n",
        "| Тип | Кол-во |",
        "|-----|--------|",
    ]
    for typ, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
        lines.append(f"| {TYPE_LABELS[typ]} | {len(items)} |")

    for typ in ["open", "question", "todo", "hypothesis"]:
        items = by_type.get(typ, [])
        if not items:
            continue
        if TYPE_FILTER and typ != TYPE_FILTER:
            continue
        lines += [f"\n## {TYPE_LABELS[typ]} ({len(items)})\n"]
        # Группируем по файлу
        by_file: dict[str, list] = defaultdict(list)
        for it in items:
            by_file[it["source"]].append(it)

        for src, file_items in sorted(by_file.items(), key=lambda x: -len(x[1])):
            fname = src.split("/")[-1]
            lines.append(f"### `{fname}` ({len(file_items)})\n")
            for it in file_items[:5]:
                heading = f" [{it['heading']}]" if it["heading"] else ""
                lines.append(f"- {it['sentence'][:150]}{heading}")
            if len(file_items) > 5:
                lines.append(f"- _...ещё {len(file_items)-5}_")
            lines.append("")

    out = DOCS / "QUESTIONS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
