"""
improve_concepts.py — извлекает определения понятий прямо из текстов.
Ищет паттерны: "X — это ...", "X представляет собой ...", "X: ...", "X (англ. ...)"
Создаёт docs/CONCEPTS.md.
Запуск: python scripts/improve_concepts.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Паттерны определений на русском и английском
DEF_PATTERNS = [
    # "Термин — это определение"
    r'([A-ZА-ЯЁ][^\n.]{2,40})\s+—\s+это\s+([^.\n]{20,300})',
    # "Термин представляет собой"
    r'([A-ZА-ЯЁ][^\n.]{2,40})\s+представляет\s+собой\s+([^.\n]{20,300})',
    # "Термин — система/инструмент/платформа ..."
    r'([A-ZА-ЯЁ][^\n.]{2,40})\s+—\s+(?:система|инструмент|платформа|фреймворк|протокол|модуль|сервис|библиотека)\s+([^.\n]{15,250})',
    # "X is a ..."
    r'([A-Z][a-zA-Z\s\-]{2,35})\s+is\s+(?:a|an|the)\s+([^.\n]{20,250})',
    # Markdown bold определение: **Термин** — описание
    r'\*\*([A-ZА-ЯЁa-zA-Z][^*]{2,40})\*\*\s*[—:]\s*([^.\n]{20,250})',
]

SKIP = {"CONCEPTS.md", "GLOSSARY.md", "COMPLEXITY.md", "COMPARE.md"}

# Стоп-слова для фильтрации мусорных "определений"
BAD_STARTS = ("что ", "как ", "где ", "это ", "все ", "при ", "для ",
              "из ", "на ", "по ", "то ", "не ", "он ", "же ")


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def extract_definitions(text: str, filepath: Path) -> list[dict]:
    # Убираем code-блоки и таблицы
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)

    results = []
    seen_terms: set[str] = set()

    for pattern in DEF_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            term = clean(m.group(1))
            defn = clean(m.group(2))

            # Фильтрация
            if len(term) < 3 or len(term) > 60:
                continue
            if len(defn) < 20:
                continue
            if defn.lower().startswith(BAD_STARTS):
                continue
            if term.lower() in ("и", "в", "на", "с", "к", "а", "но"):
                continue

            key = term.lower()[:20]
            if key in seen_terms:
                continue
            seen_terms.add(key)

            results.append({
                "term": term,
                "definition": defn[:300],
                "file": str(filepath.relative_to(ROOT)),
            })

    return results


def main():
    print("Извлечение определений понятий...")

    by_letter: dict[str, list[dict]] = defaultdict(list)
    total = 0

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        if len(text) < 300:
            continue

        for item in extract_definitions(text, f):
            letter = item["term"][0].upper()
            if not letter.isalpha():
                letter = "#"
            by_letter[letter].append(item)
            total += 1

    # Дедупликация по term
    all_items: list[dict] = []
    seen_global: set[str] = set()
    for letter in sorted(by_letter.keys()):
        for item in by_letter[letter]:
            key = item["term"].lower()[:25]
            if key not in seen_global:
                seen_global.add(key)
                all_items.append(item)

    all_items.sort(key=lambda x: x["term"].lower())

    lines = [
        "# Глоссарий понятий\n",
        "_Определения извлечены автоматически из документов._\n",
        f"**Извлечено понятий:** {len(all_items)}  (из {total} совпадений)\n",
    ]

    current_letter = ""
    for item in all_items:
        letter = item["term"][0].upper()
        if not letter.isalpha():
            letter = "#"
        if letter != current_letter:
            current_letter = letter
            lines.append(f"\n## {letter}\n")

        short = item["file"].split("/")[-1].replace(".md", "")
        lines.append(f"**{item['term']}**")
        lines.append(f": {item['definition']}  ")
        lines.append(f"  _→ [{short}]({item['file']})_\n")

    out = DOCS / "CONCEPTS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  понятий: {len(all_items)}")


if __name__ == "__main__":
    main()
