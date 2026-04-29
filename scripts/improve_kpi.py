"""
improve_kpi.py — извлекает числовые KPI и метрики из docs/.
Ищет: числа с единицами, проценты, временные оценки, бюджеты, размеры команд.
Создаёт docs/KPI.md.
Запуск: python scripts/improve_kpi.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"KPI.md", "STATS.md", "HEALTH.md", "WORD_FREQ.md"}

KPI_PATTERNS = [
    # "436 вакансий", "20 проектов"
    (r'(\d[\d\s]*)\s+(вакансий|проектов|файлов|компонентов|разработчиков|команд|участников)',
     "Количество"),
    # Проценты
    (r'(\d+(?:\.\d+)?)\s*%\s+([а-яёa-z][^.\n]{5,60})',
     "Проценты"),
    # Временные оценки "12-18 месяцев", "2 недели"
    (r'(\d+(?:[–\-]\d+)?)\s*(месяц[а-я]*|недел[а-я]*|час[а-я]*|день|дн[ей]+)',
     "Время"),
    # Стоимость "$0", "€500"
    (r'([$€£¥]\s*\d[\d\s,.]*(?:k|K|тыс|млн)?)',
     "Стоимость"),
    # "версия 2.0", "v1.3"
    (r'(?:версия|version|v)\s*(\d+\.\d+(?:\.\d+)?)',
     "Версия"),
    # "топ-N", "топ N"
    (r'топ[- ]?(\d+)',
     "Рейтинг"),
    # Размер файла/данных
    (r'(\d+(?:\.\d+)?)\s*(МБ|KB|MB|GB|ГБ|байт)',
     "Размер"),
    # "1-й этап", "итерация 3"
    (r'(?:этап|итерация|фаза|sprint)\s*(\d+)',
     "Этап"),
]


def extract_kpis(text: str, filepath: Path) -> list[dict]:
    # Убираем code-блоки
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    items = []
    seen: set = set()

    for pattern, category in KPI_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            value = m.group(1).strip()
            context_start = max(0, m.start() - 60)
            context_end   = min(len(text), m.end() + 60)
            context = re.sub(r'\s+', ' ', text[context_start:context_end]).strip()

            key = (category, value.lower()[:20])
            if key in seen:
                continue
            seen.add(key)

            items.append({
                "category": category,
                "value":    value,
                "context":  context[:160],
                "file":     str(filepath.relative_to(ROOT)),
            })
    return items


def main():
    print("Извлечение числовых KPI...")

    by_cat: dict[str, list] = defaultdict(list)
    total = 0

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        if len(text) < 150:
            continue
        for item in extract_kpis(text, f):
            by_cat[item["category"]].append(item)
            total += 1

    cat_order = ["Количество", "Проценты", "Время", "Стоимость",
                 "Размер", "Версия", "Рейтинг", "Этап"]

    lines = [
        "# Числовые KPI и метрики\n",
        f"_Извлечено: **{total}** числовых показателей из документов_\n",
    ]

    for cat in cat_order:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines.append(f"\n## {cat} ({len(items)})\n")
        lines.append("| Значение | Контекст | Источник |")
        lines.append("|----------|----------|---------|")

        seen_val: set = set()
        for item in items:
            key = item["value"].lower()
            if key in seen_val:
                continue
            seen_val.add(key)
            short = item["file"].split("/")[-1].replace(".md", "")[:25]
            ctx = item["context"].replace("|", "\\|")[:80]
            lines.append(f"| **{item['value']}** | {ctx} | `{short}` |")
            if len(seen_val) >= 20:
                rem = len(items) - len(seen_val)
                if rem > 0:
                    lines.append(f"| _...ещё {rem}_ | | |")
                break

    out = DOCS / "KPI.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  KPI: {total}")


if __name__ == "__main__":
    main()
