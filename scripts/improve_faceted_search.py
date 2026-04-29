"""
improve_faceted_search.py — фасетный поиск по базе знаний.

Поиск с фильтрами (фасетами) поверх keyword_index.json + named_entities.json:
  --query "текст"       — полнотекстовый запрос
  --section X           — только в секции
  --entity "AgentFS"    — только файлы с этой сущностью
  --type projects|people|tech  — тип сущности
  --min-words N         — минимум слов в файле
  --after YYYY-MM-DD    — файлы изменённые после даты
  --format table|list   — формат вывода

Сохраняет последний результат в docs/SEARCH_RESULTS.md.
Запуск:
    python scripts/improve_faceted_search.py --query "агент память"
    python scripts/improve_faceted_search.py --query "RAG" --section 05-habr-projects
    python scripts/improve_faceted_search.py --entity "NGT Memory" --top 10
    python scripts/improve_faceted_search.py --type projects --section 05-habr-projects
"""
import json
import re
import sys
from pathlib import Path
from datetime import date, datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

KEYWORD_INDEX = DOCS / "keyword_index.json"
ENTITIES_INDEX = DOCS / "named_entities.json"

QUERY = None
ENTITY_FILTER = None
TYPE_FILTER = None
TOP = 15
MIN_WORDS = 0
AFTER_DATE = None
OUTPUT_FORMAT = "table"
SECTION_FILTER = None

for flag, attr in [("--query", "QUERY"), ("--entity", "ENTITY_FILTER"),
                    ("--type", "TYPE_FILTER"), ("--format", "OUTPUT_FORMAT")]:
    if flag in sys.argv:
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            globals()[attr] = sys.argv[idx + 1]

if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP = int(sys.argv[idx + 1])

if "--min-words" in sys.argv:
    idx = sys.argv.index("--min-words")
    if idx + 1 < len(sys.argv):
        MIN_WORDS = int(sys.argv[idx + 1])

if "--after" in sys.argv:
    idx = sys.argv.index("--after")
    if idx + 1 < len(sys.argv):
        AFTER_DATE = sys.argv[idx + 1]

if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = sys.argv[idx + 1]

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для",
    "the", "a", "an", "is", "of", "in", "on", "to", "for", "with",
}


def _load_keyword_index() -> dict:
    if not KEYWORD_INDEX.exists():
        return {}
    try:
        data = json.loads(KEYWORD_INDEX.read_text(encoding="utf-8"))
        return data.get("index", {})
    except Exception:
        return {}


def _load_entities() -> dict:
    if not ENTITIES_INDEX.exists():
        return {}
    try:
        return json.loads(ENTITIES_INDEX.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _word_count(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8").split())
    except Exception:
        return 0


def _file_mtime(path: Path) -> str:
    try:
        ts = path.stat().st_mtime
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    except Exception:
        return "unknown"


def _search_by_query(query: str, index: dict) -> dict[str, float]:
    """Возвращает {file: score}."""
    terms = [t.lower() for t in re.findall(r'[а-яёa-z]{3,}', query)
             if t.lower() not in STOPWORDS]
    scores: dict[str, float] = {}

    for term in terms:
        for entry in index.get(term, []):
            f = entry["f"]
            scores[f] = scores.get(f, 0) + entry["n"] * 1.0

        # Биграмм поиск для пар слов
        if len(terms) > 1:
            for i in range(len(terms) - 1):
                bg = terms[i] + " " + terms[i + 1]
                for entry in index.get(bg, []):
                    f = entry["f"]
                    scores[f] = scores.get(f, 0) + entry["n"] * 3.0

    return scores


def _filter_by_entity(entity: str, entities_data: dict,
                       type_filter: str | None) -> set[str]:
    """Возвращает множество файлов содержащих данную сущность.
    entities_data: {name: {name, type, files}} (плоская структура)
    """
    entity_lower = entity.lower()
    files: set[str] = set()

    for ent_name, ent in entities_data.items():
        if not isinstance(ent, dict):
            continue
        if type_filter and ent.get("type") != type_filter:
            continue
        name = ent.get("name", ent_name).lower()
        if entity_lower in name or name in entity_lower:
            files.update(ent.get("files", []))

    return files


def _filter_by_type(type_filter: str, entities_data: dict) -> set[str]:
    """Все файлы с сущностями данного типа."""
    files: set[str] = set()
    for ent_name, ent in entities_data.items():
        if isinstance(ent, dict) and ent.get("type") == type_filter:
            files.update(ent.get("files", []))
    return files


def main() -> None:
    print("🔍 improve_faceted_search.py — фасетный поиск")

    if not QUERY and not ENTITY_FILTER and not TYPE_FILTER:
        print("  Укажите хотя бы один фильтр:")
        print("    --query \"текст\"")
        print("    --entity \"AgentFS\"")
        print("    --type projects|people|tech|orgs")
        return

    index = _load_keyword_index()
    entities_data = _load_entities()

    if not index and QUERY:
        print("  ⚠️  keyword_index.json не найден. Запустите improve_keyword_index.py")
        return

    # Базовый набор файлов из запроса
    scores: dict[str, float] = {}

    if QUERY:
        scores = _search_by_query(QUERY, index)
        print(f"   Запрос: «{QUERY}» → {len(scores)} файлов")

    # Фильтр по сущности
    if ENTITY_FILTER:
        entity_files = _filter_by_entity(ENTITY_FILTER, entities_data, TYPE_FILTER)
        print(f"   Сущность: «{ENTITY_FILTER}» → {len(entity_files)} файлов")
        if scores:
            # Пересечение с бустом
            for f in entity_files:
                scores[f] = scores.get(f, 0) + 5.0
        else:
            scores = {f: 5.0 for f in entity_files}

    # Фильтр по типу сущности (без конкретного имени)
    elif TYPE_FILTER and not ENTITY_FILTER:
        type_files = _filter_by_type(TYPE_FILTER, entities_data)
        print(f"   Тип: «{TYPE_FILTER}» → {len(type_files)} файлов")
        scores = {f: scores.get(f, 0) + 3.0 for f in type_files}

    if not scores:
        print("  Ничего не найдено.")
        return

    # Применяем фасеты
    results = []
    for file_path, score in sorted(scores.items(), key=lambda x: -x[1]):
        # Фильтр по секции
        if SECTION_FILTER and SECTION_FILTER not in file_path:
            continue

        path = ROOT / file_path
        if not path.exists():
            continue

        # Фильтр по размеру
        if MIN_WORDS > 0:
            wc = _word_count(path)
            if wc < MIN_WORDS:
                continue
        else:
            wc = None

        # Фильтр по дате
        mtime = _file_mtime(path)
        if AFTER_DATE and mtime < AFTER_DATE:
            continue

        results.append({
            "file": file_path,
            "score": round(score, 2),
            "mtime": mtime,
            "wc": wc,
        })

        if len(results) >= TOP:
            break

    print(f"\n   Результатов: {len(results)}\n")

    # Вывод в терминал
    for i, r in enumerate(results, 1):
        wc_str = f" ({r['wc']} сл.)" if r['wc'] else ""
        print(f"  {i:2d}. [{r['score']:6.1f}] {r['file']}{wc_str}")

    # Записать в файл
    lines = [
        "# Результаты поиска\n",
        f"_Обновлено: {TODAY}_\n",
    ]
    if QUERY:
        lines.append(f"**Запрос:** `{QUERY}`\n")
    if ENTITY_FILTER:
        lines.append(f"**Сущность:** `{ENTITY_FILTER}`\n")
    if TYPE_FILTER:
        lines.append(f"**Тип:** `{TYPE_FILTER}`\n")
    if SECTION_FILTER:
        lines.append(f"**Секция:** `{SECTION_FILTER}`\n")
    lines.append(f"**Результатов:** {len(results)}\n")

    if OUTPUT_FORMAT == "table":
        lines += ["| # | Файл | Оценка | Дата |", "|---|------|--------|------|"]
        for i, r in enumerate(results, 1):
            fname = r["file"].split("/")[-1]
            lines.append(f"| {i} | `{fname}` | {r['score']} | {r['mtime']} |")
    else:
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. [{r['file']}]({r['file']}) — score: {r['score']}")

    out = DOCS / "SEARCH_RESULTS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
