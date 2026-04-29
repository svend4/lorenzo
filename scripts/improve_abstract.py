"""
improve_abstract.py — генерирует структурированный абстракт для каждого документа.

Без LLM, по паттернам в тексте определяет:
  - Проблема/контекст (предложения с «проблем», «задач», «нужно», «требует»)
  - Подход/метод    (предложения с «решени», «метод», «алгоритм», «подход»)
  - Результат       (предложения с «результат», «достигн», «получен», «вывод»)
  - Ключевые слова  (TF-IDF топ-8)

Вставляет блок <!-- abstract --> в начало файла после H1.
Идемпотентно.

Режимы:
  --dry-run  (по умолчанию)
  --apply    — записать
  --min-words N — не обрабатывать файлы короче N слов (по умолч.: 200)
  --section

Запуск:
    python scripts/improve_abstract.py --dry-run
    python scripts/improve_abstract.py --apply --section 05-habr-projects
"""
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

APPLY    = "--apply"   in sys.argv
DRY_RUN  = not APPLY

MIN_WORDS = 200
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
    "README.md", "SEARCH.md", "OUTLINE.md", "TIMELINE.md",
    "NAMED_ENTITIES.md", "SOURCE_MAP.md", "COMPARE.md",
    "READABILITY.md", "SPELLCHECK.md",
}

ABSTRACT_MARKER = "<!-- abstract-auto -->"

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "этот", "эта", "его", "её", "их",
    "the", "a", "an", "is", "are", "of", "in", "on", "to", "for",
    "with", "by", "and", "not", "it", "be", "was", "we", "as",
}

# Паттерны для определения типа предложения
PROBLEM_KW = re.compile(
    r'проблем|задач[аи]|требует|нужн[оа]|необходим|сложн|вызов|challenge|problem|issue|need', re.I
)
APPROACH_KW = re.compile(
    r'предлага[ею]|решени[ею]|метод|подход|алгоритм|архитектур|используется|propose|approach|method|solution|design', re.I
)
RESULT_KW = re.compile(
    r'результат|достигн|получен|вывод|показыва[ею]т|позволяет|даёт|обеспечивает|result|achieve|enable|provide|show', re.I
)


def _sentences(text: str) -> list[str]:
    """Разбивает на предложения, чистит markdown."""
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'<!--.*?-->', ' ', clean, flags=re.DOTALL)
    clean = re.sub(r'https?://\S+', '[URL]', clean)
    clean = re.sub(r'[*_`#|>\[\]]', '', clean)
    clean = re.sub(r'\s+', ' ', clean)
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', clean) if len(s.strip()) > 40]


def _keywords(text: str, n: int = 8) -> list[str]:
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    tokens = [
        t for t in re.findall(r'[а-яёa-z]{4,}', clean.lower())
        if t not in STOPWORDS
    ]
    return [w for w, _ in Counter(tokens).most_common(n * 3) if len(w) > 4][:n]


def _best_sentence(sentences: list[str], pattern: re.Pattern, max_len: int = 180) -> str:
    """Находит лучшее предложение по паттерну."""
    candidates = [s for s in sentences if pattern.search(s)]
    if not candidates:
        return ""
    # Предпочитаем средние по длине предложения (не слишком короткие и не слишком длинные)
    best = min(candidates, key=lambda s: abs(len(s) - 120))
    return re.sub(r'\s+', ' ', best).strip()[:max_len]


def build_abstract(text: str) -> dict:
    """Строит абстракт из текста."""
    sents = _sentences(text)
    kws   = _keywords(text)

    problem  = _best_sentence(sents, PROBLEM_KW)
    approach = _best_sentence(sents, APPROACH_KW)
    result   = _best_sentence(sents, RESULT_KW)

    # Если ничего не нашли — берём первое осмысленное предложение
    if not problem and sents:
        problem = sents[0][:180]

    return {
        "problem":  problem,
        "approach": approach,
        "result":   result,
        "keywords": kws,
    }


def _format_abstract(ab: dict) -> str:
    lines = [
        ABSTRACT_MARKER,
        "> **Абстракт** (авто)",
        ">",
    ]
    if ab["problem"]:
        lines.append(f"> 🎯 **Проблема:** {ab['problem']}")
    if ab["approach"]:
        lines.append(f"> 🔧 **Подход:** {ab['approach']}")
    if ab["result"]:
        lines.append(f"> ✅ **Результат:** {ab['result']}")
    if ab["keywords"]:
        kw_str = ', '.join(f'`{k}`' for k in ab["keywords"])
        lines.append(f"> 🏷️ **Ключевые слова:** {kw_str}")
    lines.append(">")
    return "\n".join(lines)


def process_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False

    if len(text.split()) < MIN_WORDS:
        return False

    ab = build_abstract(text)
    if not ab["problem"]:
        return False

    block = _format_abstract(ab)

    if ABSTRACT_MARKER in text:
        new_text = re.sub(
            rf'{re.escape(ABSTRACT_MARKER)}.*?(?=\n[^>]|\Z)',
            block,
            text, flags=re.DOTALL,
        )
        if new_text == text:
            return False
    else:
        # Вставляем после H1
        m = re.search(r'^#\s+.+$', text, re.MULTILINE)
        if m:
            pos = m.end()
            new_text = text[:pos] + "\n\n" + block + "\n" + text[pos:]
        else:
            new_text = block + "\n\n" + text

    if APPLY:
        path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    print("📄 improve_abstract.py — структурированные абстракты")
    print(f"   Мин. слов: {MIN_WORDS} | Режим: {'APPLY' if APPLY else 'dry-run'}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    done = skipped = 0
    for f in files:
        changed = process_file(f)
        if changed:
            print(f"  ✅ {f.relative_to(ROOT)}")
            done += 1
        else:
            skipped += 1

    print(f"\n  {'Добавлено' if APPLY else 'Будет добавлено'}: {done}")
    print(f"  Пропущено: {skipped}")
    if DRY_RUN:
        print("  Запустите с --apply для реальной записи.")


if __name__ == "__main__":
    main()
