"""
improve_auto_linker.py — автоматические внутренние ссылки в документах.

Находит упоминания проектов/технологий/людей из named_entities.json
и превращает их в markdown-ссылки на соответствующие файлы.

Алгоритм:
  1. Загружает named_entities.json → словарь {имя: best_file}
  2. Для каждого файла ищет plain-text упоминания сущностей
  3. Заменяет первое вхождение в абзаце на [Имя](path/to/file.md)
  4. Пропускает уже существующие ссылки и заголовки

Режимы:
  --dry-run   (по умолч.) — показывает план
  --apply     — записывает изменения
  --types projects,tech   — только эти типы сущностей
  --min-mentions N        — только сущности с ≥N упоминаний (по умолч.: 3)

Запуск:
    python scripts/improve_auto_linker.py --dry-run
    python scripts/improve_auto_linker.py --apply --types projects
    python scripts/improve_auto_linker.py --apply --section 05-habr-projects
"""
import json
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

APPLY   = "--apply" in sys.argv
DRY_RUN = not APPLY

TYPES_FILTER: set[str] = set()
if "--types" in sys.argv:
    idx = sys.argv.index("--types")
    if idx + 1 < len(sys.argv):
        TYPES_FILTER = set(sys.argv[idx + 1].split(","))

MIN_MENTIONS = 3
if "--min-mentions" in sys.argv:
    idx = sys.argv.index("--min-mentions")
    if idx + 1 < len(sys.argv):
        MIN_MENTIONS = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

ENTITIES_PATH = DOCS / "named_entities.json"

SKIP_FILES = {
    "NAMED_ENTITIES.md", "SEARCH.md", "SUMMARIES.md", "SIMILAR_PASSAGES.md",
    "KEYWORD_INDEX.md", "CONTRADICTIONS.md", "HEADING_AUDIT.md",
    "CONCEPT_GRAPH.md", "EMPTY_SECTIONS.md", "QUESTIONS.md",
}

# Типы которые мы линкуем
DEFAULT_TYPES = {"projects", "tech", "people"}


def _load_entity_map(min_mentions: int) -> dict[str, dict]:
    """
    Возвращает {entity_name: {type, best_file, display_name}}.
    best_file — файл с наибольшим числом упоминаний.
    """
    if not ENTITIES_PATH.exists():
        return {}
    try:
        data = json.loads(ENTITIES_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}

    entity_map = {}
    types_to_use = TYPES_FILTER or DEFAULT_TYPES

    for name, info in data.items():
        if not isinstance(info, dict):
            continue
        ent_type = info.get("type", "")
        if ent_type not in types_to_use:
            continue
        files = info.get("files", [])
        if len(files) < min_mentions:
            continue

        # Выбираем лучший файл: в той же секции что сущность называется
        best = files[0] if files else None
        # Предпочитаем файл 05-habr-projects для проектов
        for f in files:
            if "05-habr-projects" in f or "01-svyazi" in f:
                best = f
                break

        display = info.get("name", name)
        entity_map[display] = {
            "type": ent_type,
            "best_file": best,
            "files_count": len(files),
        }
        # Также добавляем варианты написания (заглавные)
        entity_map[display.capitalize()] = entity_map[display]
        entity_map[display.upper()] = entity_map[display]

    return entity_map


def _make_link(name: str, target: str, source: str) -> str:
    """Создаёт относительный markdown-link."""
    try:
        target_path = ROOT / target
        source_path = (ROOT / source).parent
        rel = target_path.relative_to(ROOT)
        # Относительный путь от исходного файла
        try:
            rel_from_source = Path("..") / rel
        except Exception:
            rel_from_source = Path("/") / rel
        return f"[{name}]({rel_from_source})"
    except Exception:
        return f"[{name}]({target})"


def _link_paragraph(para: str, entity_map: dict[str, dict], source: str) -> tuple[str, int]:
    """Добавляет ссылки в абзац. Возвращает (новый_текст, число_замен)."""
    replacements = 0
    result = para

    for name, info in sorted(entity_map.items(), key=lambda x: -len(x[0])):
        if not info["best_file"]:
            continue
        if info["best_file"] == source:
            continue  # не линкуем файл сам на себя

        # Ищем слово как отдельный токен (не внутри ссылки)
        # Паттерн: имя не предшествует ](  и не в уже существующей ссылке
        pattern = r'(?<!\[)(?<!\()(?<!/)\b' + re.escape(name) + r'\b(?!\])'
        if not re.search(pattern, result):
            continue

        link = _make_link(name, info["best_file"], source)
        # Заменяем только первое вхождение в абзаце
        result, n = re.subn(pattern, link, result, count=1)
        if n:
            replacements += n
            # После замены убираем эту сущность чтобы не дублировать
            break  # только одну замену за проход (по самой длинной сущности)

    return result, replacements


def process_file(path: Path, entity_map: dict[str, dict]) -> tuple[str, int]:
    """Обрабатывает файл. Возвращает (новый_текст, число_добавленных_ссылок)."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return "", 0

    source = str(path.relative_to(ROOT))
    lines = text.splitlines(keepends=True)
    result_lines = []
    total_links = 0
    in_code_block = False

    for line in lines:
        # Пропускаем заголовки, код, уже существующие ссылки
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
        if in_code_block:
            result_lines.append(line)
            continue
        if re.match(r'^#{1,6}\s', line):
            result_lines.append(line)
            continue
        if stripped.startswith(">"):
            result_lines.append(line)
            continue
        if stripped.startswith("|"):
            result_lines.append(line)
            continue

        new_line, n = _link_paragraph(line, entity_map, source)
        result_lines.append(new_line)
        total_links += n

    new_text = "".join(result_lines)
    return new_text, total_links


def main() -> None:
    print("🔗 improve_auto_linker.py — автоматические внутренние ссылки")
    print(f"   Мин. упоминаний: {MIN_MENTIONS} | Режим: {'APPLY' if APPLY else 'dry-run'}")
    types_str = ', '.join(TYPES_FILTER or DEFAULT_TYPES)
    print(f"   Типы сущностей: {types_str}\n")

    entity_map = _load_entity_map(MIN_MENTIONS)
    if not entity_map:
        print("  ⚠️  named_entities.json не найден. Запустите improve_named_entity_index.py")
        return

    # Убираем дубли (разные регистры одной сущности)
    seen = set()
    unique_map = {}
    for name, info in entity_map.items():
        key = name.lower()
        if key not in seen:
            seen.add(key)
            unique_map[name] = info
    entity_map = unique_map

    print(f"   Сущностей для линковки: {len(entity_map)}")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    total_files_changed = 0
    total_links_added = 0

    for f in files:
        new_text, n_links = process_file(f, entity_map)
        if n_links == 0:
            continue
        total_files_changed += 1
        total_links_added += n_links
        print(f"  {'✅' if APPLY else '📋'} {f.relative_to(ROOT)} (+{n_links} ссылок)")
        if APPLY and new_text:
            f.write_text(new_text, encoding="utf-8")

    print(f"\n  {'Добавлено' if APPLY else 'Будет добавлено'}: {total_links_added} ссылок в {total_files_changed} файлах")
    if DRY_RUN:
        print("  Запустите с --apply для реальной записи.")


if __name__ == "__main__":
    main()
