"""
improve_questions.py — извлекает открытые вопросы из docs/.
Ищет вопросительные предложения и паттерны "открытый вопрос".
Создаёт docs/QUESTIONS.md.
Запуск: python scripts/improve_questions.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"QUESTIONS.md", "QA.md", "MISSING.md"}

QUESTION_PATTERNS = [
    # Прямые вопросы
    r'([^.\n]{20,200}\?)',
    # "Открытый вопрос: ..." или "Вопрос: ..."
    r'(?:открытый\s+вопрос|вопрос|question)[:\s]+([^.\n]{20,200})',
    # "Как X?" / "Что делать с X?" / "Зачем Y?"
    r'(?:^|\n)(?:как|что|зачем|почему|когда|кто|где|сколько)\s+([^?\n]{10,150}\?)',
    # "TODO: выяснить X"
    r'todo[:\s]+(?:выяснить|уточнить|разобраться|определить|проверить)\s+([^.\n]{10,200})',
]

CATEGORIES = {
    "архитектура":  ["контракт", "схема", "архитектур", "слой", "envelope"],
    "интеграция":   ["интеграц", "совмест", "api", "mcp", "протокол"],
    "лицензия":     ["лицензи", "mit", "bsl", "apache", "права"],
    "MVP/сроки":    ["mvp", "сроки", "когда", "итерац", "timeline"],
    "команда":      ["кто", "автор", "контакт", "написать", "команда"],
    "технология":   ["как", "метод", "алгоритм", "подход", "реализ"],
}


def categorize(text: str) -> str:
    low = text.lower()
    for cat, kws in CATEGORIES.items():
        if any(k in low for k in kws):
            return cat
    return "общее"


def extract_questions(text: str, filepath: Path) -> list[dict]:
    # Убираем code-блоки и таблицы
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)

    items = []
    seen: set[str] = set()

    for pattern in QUESTION_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
            q = re.sub(r'\s+', ' ', m.group(1)).strip()
            if len(q) < 15 or len(q) > 300:
                continue
            # Убираем чисто технические строки
            if q.startswith(('|', '#', '>', '```', '-')):
                continue
            key = q.lower()[:40]
            if key in seen:
                continue
            seen.add(key)
            items.append({
                "text":     q,
                "file":     str(filepath.relative_to(ROOT)),
                "category": categorize(q),
            })
    return items


def main():
    print("Извлечение открытых вопросов...")

    by_cat: dict[str, list] = defaultdict(list)
    total = 0

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        if len(text) < 200:
            continue
        for item in extract_questions(text, f):
            by_cat[item["category"]].append(item)
            total += 1

    cat_order = ["архитектура", "интеграция", "MVP/сроки", "технология",
                 "лицензия", "команда", "общее"]

    lines = [
        "# Открытые вопросы\n",
        f"_Извлечено автоматически из всех документов: **{total}** вопросов_\n",
        "Используйте как список открытых проблем и точек неопределённости.\n",
    ]

    for cat in cat_order:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines.append(f"\n## {cat.capitalize()} ({len(items)})\n")
        seen = set()
        for item in items:
            key = item["text"][:40].lower()
            if key in seen:
                continue
            seen.add(key)
            short = item["file"].split("/")[-1].replace(".md", "")
            lines.append(f"- {item['text']}  ")
            lines.append(f"  _→ {short}_\n")
            if len(seen) >= 15:
                rem = len(items) - len(seen)
                if rem > 0:
                    lines.append(f"_...ещё {rem} вопросов в этой категории_\n")
                break

    out = DOCS / "QUESTIONS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  вопросов: {total}")


if __name__ == "__main__":
    main()
