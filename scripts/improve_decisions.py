"""
improve_decisions.py — извлекает ключевые выводы и решения из всех файлов.
Ищет паттерны: "главный вывод", "лучший выбор", "рекомендуется" и т.д.
Создаёт docs/DECISIONS.md.
Запуск: python scripts/improve_decisions.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

DECISION_PATTERNS = [
    r'(?:главный|основной|ключевой)\s+вывод[:\s]+(.{20,300})',
    r'(?:итоговый|итого)[:\s]+(.{20,200})',
    r'лучший\s+(?:выбор|вариант|подход|кандидат)[:\s]+(.{20,200})',
    r'рекомендуется\s+(.{20,200})',
    r'оптимальн(?:о|ый|ая)\s+(.{20,200})',
    r'наиболее\s+(?:прагматичный|реалистичный|важный)[:\s]+(.{20,200})',
    r'самый\s+(?:важный|дефицитный|сильный)[:\s]+(.{20,200})',
    r'(?:первое|второе|третье)\s+—\s+(.{20,200})',
    r'приоритет(?:ом|е)?\s+(?:является|считается)[:\s]+(.{20,200})',
    r'(?:не\s+стоит|лучше\s+не|нельзя)\s+(.{20,150})',
    r'главн(?:ое|ый)\s+(?:правило|принцип|ограничение)[:\s]+(.{20,200})',
    r'важн(?:о|ый|ая)\s+практическ(?:ий|ое)\s+принцип[:\s]+(.{20,200})',
]

CATEGORIES = {
    "архитектура":   ["CardIndex", "AgentFS", "слой", "контракт", "envelope", "схема"],
    "память":        ["Yodoca", "NGT", "memory", "консолидац", "forgetting", "episod"],
    "безопасность":  ["SENTINEL", "allowlist", "PII", "quarantine", "path guard"],
    "оркестрация":   ["mclaude", "AI Factory", "Rufler", "handoff", "locks"],
    "MVP":           ["MVP", "прототип", "12-18", "первая итерация", "начать"],
    "лицензия":      ["MIT", "Apache", "BSL", "лицензия", "license"],
    "риски":         ["риск", "хаос", "опасность", "ломает", "не стоит"],
    "контакты":      ["Андрей", "Виталий", "kksudo", "spbmolot", "написать"],
}


def categorize(text: str) -> str:
    low = text.lower()
    for cat, keywords in CATEGORIES.items():
        if any(k.lower() in low for k in keywords):
            return cat
    return "общее"


def extract_decisions(text: str, filepath: Path) -> list[dict]:
    items = []
    for pattern in DECISION_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
            val = m.group(1).strip()
            val = re.sub(r'\s+', ' ', val)[:250]
            if len(val) < 20:
                continue
            # Убираем служебные строки
            if val.startswith(('|', '#', '>')):
                continue
            items.append({
                "text": val,
                "file": str(filepath.relative_to(ROOT)),
                "category": categorize(val),
            })
    return items


def main():
    print("Извлечение решений и выводов...")
    by_cat: dict[str, list[dict]] = defaultdict(list)
    total = 0

    for f in sorted(DOCS.rglob("*.md")):
        skip = {"DECISIONS.md", "ACTION_ITEMS.md", "CONSISTENCY.md",
                "README.md", "QA.md"}
        if f.name in skip:
            continue
        text = f.read_text(encoding="utf-8")
        if len(text) < 200:
            continue
        for item in extract_decisions(text, f):
            by_cat[item["category"]].append(item)
            total += 1

    lines = [
        "# Ключевые решения и выводы\n",
        f"Автоматически извлечено из всех документов: **{total} записей**\n",
    ]

    cat_order = ["архитектура", "MVP", "память", "оркестрация",
                 "безопасность", "лицензия", "риски", "контакты", "общее"]

    for cat in cat_order:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines.append(f"\n## {cat.capitalize()} ({len(items)})\n")

        seen = set()
        for item in items:
            key = item["text"][:50].lower()
            if key in seen:
                continue
            seen.add(key)
            short = item["file"].split("/")[-1].replace(".md", "")
            lines.append(f"- {item['text']}  \n  _→ {short}_\n")
            if len(seen) >= 20:
                remaining = len(items) - len(seen)
                if remaining > 0:
                    lines.append(f"_...ещё {remaining} записей в этой категории_\n")
                break

    out = DOCS / "DECISIONS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  решений: {total}")


if __name__ == "__main__":
    main()
