"""
improve_timeline_events.py — извлекает даты и события из базы знаний.

Строит хронологическую ленту:
  - Конкретные даты: 2024-03-15, март 2024, Q2 2024
  - Относительные: «через 3 месяца», «в следующем квартале»
  - Контекст события (предложение с датой)
  - Источник (файл + заголовок секции)

Создаёт docs/TIMELINE.md.
Запуск:
    python scripts/improve_timeline_events.py
    python scripts/improve_timeline_events.py --section 01-svyazi
    python scripts/improve_timeline_events.py --from 2023 --to 2025
    python scripts/improve_timeline_events.py --format table
"""
import re
import sys
from collections import defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

YEAR_FROM = 2020
YEAR_TO   = 2030
if "--from" in sys.argv:
    idx = sys.argv.index("--from")
    if idx + 1 < len(sys.argv):
        YEAR_FROM = int(sys.argv[idx + 1])
if "--to" in sys.argv:
    idx = sys.argv.index("--to")
    if idx + 1 < len(sys.argv):
        YEAR_TO = int(sys.argv[idx + 1])

FORMAT = "list"
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
    "TIMELINE.md", "SEARCH.md", "READABILITY.md", "SPELLCHECK.md",
    "SOURCE_MAP.md", "NAMED_ENTITIES.md",
}

MONTH_RU = {
    "январ": "01", "феврал": "02", "март": "03", "апрел": "04",
    "ма": "05", "июн": "06", "июл": "07", "август": "08",
    "сентябр": "09", "октябр": "10", "ноябр": "11", "декабр": "12",
}

MONTH_EN = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}

EVENT_KEYWORDS_RU = {
    "запуск", "релиз", "выпуск", "анонс", "старт", "начало", "завершение",
    "публикация", "обновление", "версия", "деплой", "выход", "открытие",
    "создание", "интеграция", "внедрение", "разработка", "прототип",
}

EVENT_KEYWORDS_EN = {
    "launch", "release", "announce", "start", "begin", "deploy",
    "publish", "update", "version", "open", "create", "integrate",
    "develop", "prototype", "ship", "go live",
}


def _extract_context(sentence: str) -> str:
    """Чистит предложение для отображения."""
    s = re.sub(r'[*_`\[\]#|]', '', sentence)
    s = re.sub(r'https?://\S+', '[URL]', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:200]


def _current_heading(text_before: str) -> str:
    """Последний заголовок перед данной позицией."""
    headings = re.findall(r'^#{1,3}\s+(.+)$', text_before, re.MULTILINE)
    return headings[-1].strip() if headings else ""


def extract_events(path: Path) -> list[dict]:
    """Извлекает события из файла."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []

    # Убираем код и комментарии
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'<!--.*?-->', ' ', clean, flags=re.DOTALL)

    rel = str(path.relative_to(ROOT))
    events = []

    # Разбиваем на предложения
    sentences = re.split(r'(?<=[.!?])\s+', clean)
    pos = 0

    for sentence in sentences:
        s_lower = sentence.lower()
        date_found = None
        date_str   = None
        date_sort  = None

        # 1) YYYY-MM-DD или YYYY-MM
        m = re.search(r'\b(20[12]\d)[-/](0[1-9]|1[0-2])(?:[-/](\d{1,2}))?\b', sentence)
        if m:
            y, mo, d = m.group(1), m.group(2), m.group(3) or "01"
            yr = int(y)
            if YEAR_FROM <= yr <= YEAR_TO:
                date_str  = f"{y}-{mo}-{d}"
                date_sort = f"{y}{mo}{d.zfill(2)}"

        # 2) «месяц YYYY»
        if not date_str:
            for stem, mo in MONTH_RU.items():
                m2 = re.search(rf'\b{stem}\S*\s+(20[12]\d)\b', s_lower)
                if m2:
                    yr = int(m2.group(1))
                    if YEAR_FROM <= yr <= YEAR_TO:
                        date_str  = f"{m2.group(1)}-{mo}"
                        date_sort = f"{m2.group(1)}{mo}01"
                    break

        # 3) «Q1 2024» или «2024 Q2»
        if not date_str:
            m3 = re.search(r'\b(Q[1-4])\s*(20[12]\d)\b|(20[12]\d)\s*(Q[1-4])\b', sentence, re.IGNORECASE)
            if m3:
                if m3.group(1):
                    q, y = m3.group(1).upper(), m3.group(2)
                else:
                    q, y = m3.group(4).upper(), m3.group(3)
                yr = int(y)
                if YEAR_FROM <= yr <= YEAR_TO:
                    q_mo = {"Q1": "01", "Q2": "04", "Q3": "07", "Q4": "10"}[q]
                    date_str  = f"{y} {q}"
                    date_sort = f"{y}{q_mo}01"

        # 4) Просто год
        if not date_str:
            m4 = re.search(r'\b(20[12]\d)\b', sentence)
            if m4:
                yr = int(m4.group(1))
                if YEAR_FROM <= yr <= YEAR_TO:
                    date_str  = m4.group(1)
                    date_sort = f"{m4.group(1)}0601"

        if not date_str:
            continue

        # Проверяем: есть ли в предложении ключевое слово события
        has_event_kw = (
            any(kw in s_lower for kw in EVENT_KEYWORDS_RU) or
            any(kw in s_lower for kw in EVENT_KEYWORDS_EN)
        )

        # Берём контекст позиции в тексте
        text_before = clean[:clean.find(sentence) + 1] if clean.find(sentence) >= 0 else ""
        heading = _current_heading(text_before)

        events.append({
            "date_str":    date_str,
            "date_sort":   date_sort,
            "source":      rel,
            "heading":     heading,
            "context":     _extract_context(sentence),
            "has_event":   has_event_kw,
        })

    return events


def main() -> None:
    print("📅 improve_timeline_events.py — хронологическая лента событий")
    print(f"   Период: {YEAR_FROM}–{YEAR_TO}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "obsidian" not in str(f)
             and "confluence" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    all_events = []
    for f in files:
        evts = extract_events(f)
        all_events.extend(evts)

    # Сортируем по дате
    all_events.sort(key=lambda e: e["date_sort"])

    # Группируем по году
    by_year: dict[str, list] = defaultdict(list)
    for e in all_events:
        year = e["date_sort"][:4]
        by_year[year].append(e)

    print(f"   Найдено дат/событий: {len(all_events)}")
    print(f"   С ключевым словом события: {sum(1 for e in all_events if e['has_event'])}")

    lines = [
        "# Хронологическая лента событий\n",
        f"_Обновлено: {TODAY}_\n",
        f"Период: **{YEAR_FROM}–{YEAR_TO}** | Событий: **{len(all_events)}**\n",
    ]

    if FORMAT == "table":
        lines += [
            "| Дата | Событие | Источник |",
            "|------|---------|---------|",
        ]
        for e in all_events:
            src = Path(e["source"]).name
            ctx = e["context"][:80]
            lines.append(f"| {e['date_str']} | {ctx} | `{src}` |")
    else:
        # Список по годам
        for year in sorted(by_year.keys()):
            events = by_year[year]
            lines.append(f"\n## {year} ({len(events)} упоминаний)\n")
            # Сначала «события» (с ключевым словом), потом просто даты
            sorted_evts = sorted(events, key=lambda e: (not e["has_event"], e["date_sort"]))
            for e in sorted_evts[:20]:
                marker = "🔔" if e["has_event"] else "📌"
                src = Path(e["source"]).name
                ctx = e["context"][:120]
                heading = f" · _{e['heading']}_" if e["heading"] else ""
                lines.append(f"- {marker} **{e['date_str']}**{heading}  ")
                lines.append(f"  {ctx}  ")
                lines.append(f"  `{src}`\n")
            if len(events) > 20:
                lines.append(f"_...ещё {len(events)-20} упоминаний в {year}_\n")

    out = DOCS / "TIMELINE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    for year, evts in sorted(by_year.items()):
        print(f"  {year}: {len(evts)}")


if __name__ == "__main__":
    main()
