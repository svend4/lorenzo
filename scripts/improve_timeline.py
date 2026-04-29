"""
improve_timeline.py — извлекает даты и временные маркеры из всех docs/,
создаёт docs/TIMELINE.md с хронологией событий.
Запуск: python scripts/improve_timeline.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Паттерны для дат и временных маркеров
DATE_PATTERNS = [
    # 2026-04-29, 2025-11-01
    (r'\b(202[4-9][-/]\d{2}[-/]\d{2})\b', 'точная дата'),
    # "в 2025 году", "за 2026"
    (r'\b(202[4-9])\s*год', 'год'),
    # "Q1 2025", "Q3 2026"
    (r'\b(Q[1-4]\s+202[4-9])\b', 'квартал'),
    # "январь 2026", "март 2025"
    (r'\b(январ[ьея]|феврал[ьея]|март[ае]?|апрел[ьея]|ма[йея]|июн[ьея]|'
     r'июл[ьея]|август[ае]?|сентябр[ьея]|октябр[ьея]|ноябр[ьея]|декабр[ьея])'
     r'\s+(202[4-9])\b', 'месяц+год'),
    # "первые месяцы 2026"
    (r'первые\s+месяцы\s+(202[4-9])', 'период'),
    # "через 1-2 недели", "12-18 дней"
    (r'(\d+[-–]\d+)\s+(недел[ьи]|дн[ейя]|месяц[аев]?)', 'длительность'),
    # "phase 1", "фаза 1"
    (r'\b(phase|фаза|итерация|iteration)\s+(\d+)\b', 'фаза'),
    # "v2.x", "версия 0.1.5"
    (r'\b(v\d+\.\d+[\w.]*|версия\s+\d+\.\d+[\w.]*)\b', 'версия'),
]


def extract_dates(text: str, filepath: Path) -> list[dict]:
    entries = []
    rel = str(filepath.relative_to(ROOT))

    for pattern, kind in DATE_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            # Контекст: 60 символов вокруг совпадения
            start = max(0, m.start() - 40)
            end = min(len(text), m.end() + 60)
            context = text[start:end].replace('\n', ' ').strip()
            context = re.sub(r'\s+', ' ', context)
            entries.append({
                'match': m.group(0),
                'kind': kind,
                'context': context[:150],
                'file': rel,
            })
    return entries


def main():
    print("Извлечение дат и временных маркеров...")
    all_entries = []

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in ("README.md", "TIMELINE.md", "DUPLICATES.md"):
            continue
        text = f.read_text(encoding="utf-8")
        entries = extract_dates(text, f)
        all_entries.extend(entries)

    print(f"  найдено записей: {len(all_entries)}")

    # Группируем по типу
    by_kind: dict[str, list[dict]] = defaultdict(list)
    for e in all_entries:
        by_kind[e['kind']].append(e)

    lines = [
        "# Хронология и временные маркеры\n",
        f"Всего временных меток: **{len(all_entries)}**\n",
    ]

    kind_order = ['точная дата', 'год', 'квартал', 'месяц+год',
                  'период', 'фаза', 'длительность', 'версия']

    for kind in kind_order:
        entries = by_kind.get(kind, [])
        if not entries:
            continue

        lines.append(f"\n## {kind.capitalize()} ({len(entries)})\n")
        lines.append("| Маркер | Контекст | Файл |")
        lines.append("|--------|----------|------|")

        # Убираем дубли по совпадению+файлу
        seen = set()
        for e in entries:
            key = (e['match'].lower(), e['file'])
            if key in seen:
                continue
            seen.add(key)
            ctx = e['context'].replace('|', '/')
            lines.append(f"| `{e['match']}` | {ctx} | `{e['file']}` |")
            if len(seen) >= 30:
                remaining = len(entries) - len(seen)
                if remaining > 0:
                    lines.append(f"| ... | _ещё {remaining} записей_ | |")
                break

    out = DOCS / "TIMELINE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
