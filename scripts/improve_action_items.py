"""
improve_action_items.py — извлекает задачи, риски, решения и TODO из docs/.
Создаёт docs/ACTION_ITEMS.md.
Запуск: python scripts/improve_action_items.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Паттерны для разных типов элементов
PATTERNS = {
    "todo": [
        r'(?:TODO|FIXME|HACK|XXX)[:\s]+(.{10,120})',
        r'нужно\s+(?:сделать|добавить|проверить|реализовать)[:\s]+(.{10,120})',
        r'следует\s+(?:добавить|проверить|реализовать)[:\s]+(.{10,120})',
    ],
    "risk": [
        r'(?:риск|risk)[:\s]+(.{10,150})',
        r'опасн(?:ость|о)[:\s]+(.{10,150})',
        r'внимание[!:\s]+(.{10,150})',
        r'не\s+стоит\s+(.{10,120})',
        r'лучше\s+не\s+(.{10,120})',
    ],
    "decision": [
        r'(?:решение|decision)[:\s]+(.{10,150})',
        r'лучший\s+(?:выбор|вариант|подход)[:\s]+(.{10,150})',
        r'рекомендуется\s+(.{10,150})',
        r'оптимально\s+(.{10,120})',
    ],
    "next_step": [
        r'следующий\s+шаг[:\s]+(.{10,150})',
        r'next\s+step[s]?[:\s]+(.{10,150})',
        r'после\s+(?:того|этого)[,\s]+(.{10,150})',
        r'в\s+первую\s+очередь\s+(.{10,120})',
        r'начать\s+с\s+(.{10,120})',
    ],
    "limitation": [
        r'ограничени(?:е|я)[:\s]+(.{10,150})',
        r'limitation[s]?[:\s]+(.{10,150})',
        r'не\s+подходит\s+(.{10,120})',
        r'лицензи(?:я|онн)[а-я]+\s+(?:проблем|ограничен)[а-я]+[:\s]+(.{10,120})',
    ],
    "contact": [
        r'написать\s+(.{5,80})',
        r'связаться\s+с\s+(.{5,80})',
        r'первый\s+контакт[:\s]+(.{10,120})',
    ],
}

EMOJI = {
    "todo":       "📋",
    "risk":       "⚠️",
    "decision":   "✅",
    "next_step":  "➡️",
    "limitation": "🚫",
    "contact":    "📬",
}


def extract_items(text: str, filepath: Path) -> list[dict]:
    items = []
    rel = str(filepath.relative_to(ROOT))
    low = text.lower()

    for kind, patterns in PATTERNS.items():
        for pattern in patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
                val = m.group(1).strip()
                val = re.sub(r'\s+', ' ', val)
                if len(val) < 10:
                    continue
                items.append({"kind": kind, "text": val[:200], "file": rel})

    return items


def main():
    print("Извлечение action items...")
    by_kind: dict[str, list[dict]] = defaultdict(list)

    for f in sorted(DOCS.rglob("*.md")):
        skip = {"ACTION_ITEMS.md", "README.md", "QA.md", "PRIORITIES.md"}
        if f.name in skip:
            continue
        text = f.read_text(encoding="utf-8")
        if len(text) < 100:
            continue
        for item in extract_items(text, f):
            by_kind[item["kind"]].append(item)

    lines = [
        "# Action Items, риски и решения\n",
        "Автоматически извлечено из всех документов.\n",
    ]

    total = sum(len(v) for v in by_kind.values())
    lines.append(f"**Всего элементов:** {total}\n")

    kind_labels = {
        "todo":       "Задачи (TODO)",
        "risk":       "Риски",
        "decision":   "Решения и рекомендации",
        "next_step":  "Следующие шаги",
        "limitation": "Ограничения",
        "contact":    "Контактные действия",
    }

    for kind in ["next_step", "decision", "risk", "limitation", "todo", "contact"]:
        items = by_kind.get(kind, [])
        if not items:
            continue
        emoji = EMOJI[kind]
        label = kind_labels[kind]
        lines.append(f"\n## {emoji} {label} ({len(items)})\n")

        # Дедупликация по первым 60 символам
        seen = set()
        for item in items:
            key = item["text"][:60].lower()
            if key in seen:
                continue
            seen.add(key)
            short_file = item["file"].split("/")[-1].replace(".md", "")
            lines.append(f"- {item['text']}  \n  _→ {short_file}_")

        if len(seen) < len(items):
            lines.append(f"\n_({len(items) - len(seen)} дублей скрыто)_")

    out = DOCS / "ACTION_ITEMS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  элементов: {total}")


if __name__ == "__main__":
    main()
