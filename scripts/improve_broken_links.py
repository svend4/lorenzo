"""
improve_broken_links.py — проверяет внутренние ссылки в docs/.
Находит ссылки на несуществующие файлы и якоря.
Создаёт docs/BROKEN_LINKS.md и docs/bad_links.json (пути с ошибками ОС).

Новое: --fix автоматически исправляет ссылки с неправильным регистром или лишними ../.
       --section РАЗДЕЛ — проверить только один раздел.
Запуск: python scripts/improve_broken_links.py
        python scripts/improve_broken_links.py --fix       # автоматическое исправление
        python scripts/improve_broken_links.py --fix --dry-run  # показать исправления
        python scripts/improve_broken_links.py --section 05-habr-projects
"""
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

FIX     = "--fix"     in sys.argv
DRY_RUN = "--dry-run" in sys.argv

# --section поддержка
_SECTION_IDX = sys.argv.index("--section") if "--section" in sys.argv else -1
SECTION = sys.argv[_SECTION_IDX + 1] if _SECTION_IDX >= 0 and _SECTION_IDX + 1 < len(sys.argv) else ""

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Паттерны для ссылок
LINK_RE = re.compile(r'\[([^\]\n]+)\]\(([^)\n]+)\)')
ANCHOR_RE = re.compile(r'^#+\s+(.+)$', re.MULTILINE)

# Максимальная длина пути (безопасный предел ОС)
MAX_PATH_LEN = 240


def anchor_from_heading(heading: str) -> str:
    """GitHub-style якорь из заголовка."""
    h = heading.lower().strip()
    h = re.sub(r'[^\w\s\-]', '', h)
    h = re.sub(r'\s+', '-', h)
    return '#' + h.strip('-')


def _safe_exists(path: Path) -> bool:
    """Проверяет существование пути, обрабатывая OSError (слишком длинное имя)."""
    try:
        return path.exists()
    except OSError:
        return False


def build_anchor_map() -> dict[str, set[str]]:
    """Строит словарь file_path → set of valid anchors.
    Дублирующиеся заголовки получают суффиксы -1, -2, ... как в GitHub.
    """
    anchor_map: dict[str, set[str]] = {}
    scan_root = (DOCS / SECTION) if SECTION else DOCS
    for f in scan_root.rglob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        anchors = set()
        seen: dict[str, int] = {}
        for m in ANCHOR_RE.finditer(text):
            base = anchor_from_heading(m.group(1))
            anchors.add(base)
            count = seen.get(base, 0)
            seen[base] = count + 1
            if count > 0:
                anchors.add(f"{base}-{count}")
        anchor_map[str(f)] = anchors
    return anchor_map


def _find_closest_file(target_name: str) -> Path | None:
    """Ищет файл по имени (без учёта регистра и пути) во всём docs/."""
    target_lower = target_name.lower()
    for f in DOCS.rglob("*.md"):
        if f.name.lower() == target_lower:
            return f
    return None


def _try_fix_link(filepath: Path, broken_target: str) -> str | None:
    """Возвращает исправленный путь или None если исправить не удалось."""
    # Убираем якорь для поиска файла
    anchor = ""
    path_part = broken_target
    if "#" in broken_target:
        path_part, anch = broken_target.rsplit("#", 1)
        anchor = "#" + anch

    target_path = (filepath.parent / path_part).resolve()
    target_name = Path(path_part).name

    # 1. Попробовать найти файл с таким именем в docs/
    found = _find_closest_file(target_name)
    if found and found != target_path:
        rel = os.path.relpath(found, filepath.parent)
        return rel.replace("\\", "/") + anchor

    return None


def fix_broken_links(filepath: Path, broken: list[dict]) -> int:
    """Исправляет битые ссылки с типом 'файл не существует'. Возвращает число исправлений."""
    if not broken:
        return 0
    text = filepath.read_text(encoding="utf-8")
    fixes = 0
    for item in broken:
        if item["issue"] != "файл не существует":
            continue
        fixed = _try_fix_link(filepath, item["target"])
        if fixed and fixed != item["target"]:
            old_link = f"]({item['target']})"
            new_link = f"]({fixed})"
            if old_link in text:
                if DRY_RUN:
                    print(f"  [dry] {filepath.relative_to(ROOT)}: {item['target']} → {fixed}")
                else:
                    text = text.replace(old_link, new_link, 1)
                fixes += 1
    if fixes > 0 and not DRY_RUN:
        try:
            filepath.write_text(text, encoding="utf-8")
        except OSError as e:
            print(f"  [fix] ошибка записи {filepath.name}: {e}")
    return fixes


def check_links(filepath: Path, anchor_map: dict) -> tuple[list[dict], list[dict]]:
    """Проверяет все ссылки в файле.

    Возвращает (broken, os_errors) где os_errors — ссылки с path > MAX_PATH_LEN.
    """
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return [], []

    # Strip code blocks so links inside ``` ... ``` are not checked
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', '', text)

    broken: list[dict] = []
    os_errors: list[dict] = []

    for m in LINK_RE.finditer(text):
        link_text = m.group(1)
        target = m.group(2).strip()

        # Пропускаем внешние ссылки
        if target.startswith(('http://', 'https://', 'mailto:', '#')):
            if target.startswith('#'):
                anchors = anchor_map.get(str(filepath), set())
                if target not in anchors:
                    broken.append({
                        "file": str(filepath.relative_to(ROOT)),
                        "text": link_text[:60],
                        "target": target,
                        "issue": "якорь не найден",
                    })
            continue

        # Относительный путь (URL-decode для файлов с пробелами/скобками)
        decoded_target = unquote(target.split('#')[0] if '#' in target else target)
        if target.startswith('/'):
            resolved = ROOT / decoded_target.lstrip('/')
        else:
            resolved = filepath.parent / decoded_target
        target = unquote(target)  # decode for anchor checking too

        # Убираем якорь из пути
        anchor = None
        if '#' in str(resolved):
            path_part, anchor = str(resolved).rsplit('#', 1)
            resolved = Path(path_part)
            anchor = '#' + anchor

        # Проверяем длину пути до вызова exists()
        resolved_str = str(resolved)
        if len(resolved_str) > MAX_PATH_LEN:
            os_errors.append({
                "file":   str(filepath.relative_to(ROOT)),
                "target": target[:100],
                "issue":  f"путь слишком длинный ({len(resolved_str)} симв.)",
            })
            continue

        if not _safe_exists(resolved):
            broken.append({
                "file": str(filepath.relative_to(ROOT)),
                "text": link_text[:60],
                "target": target[:80],
                "issue": "файл не существует",
            })
        elif anchor:
            anchors = anchor_map.get(resolved_str, set())
            if anchor not in anchors:
                broken.append({
                    "file": str(filepath.relative_to(ROOT)),
                    "text": link_text[:60],
                    "target": target[:80],
                    "issue": "якорь не найден в файле",
                })

    return broken, os_errors


def main():
    print("Проверка внутренних ссылок...")
    if SECTION:
        print(f"  Раздел: {SECTION}")
    if FIX:
        print(f"  Режим: {'dry-run (исправления не записываются)' if DRY_RUN else 'auto-fix'}")

    anchor_map = build_anchor_map()
    scan_root  = (DOCS / SECTION) if SECTION else DOCS

    all_broken:   list[dict] = []
    all_os_errors: list[dict] = []
    total_fixed = 0

    # Пути-зеркала (obsidian, confluence) пропускаем — они auto-generated
    # templates/ и autofilled/ содержат intentional placeholder-ссылки
    SKIP_DIRS = {"obsidian", "confluence", "templates", "autofilled"}

    for f in sorted(scan_root.rglob("*.md")):
        if f.name in {"BROKEN_LINKS.md", "SUMMARIES.md"}:
            continue
        if any(part in SKIP_DIRS for part in f.relative_to(DOCS).parts):
            continue
        broken, os_errs = check_links(f, anchor_map)
        if FIX and broken:
            fixed = fix_broken_links(f, broken)
            total_fixed += fixed
            broken, _ = check_links(f, anchor_map)
        all_broken.extend(broken)
        all_os_errors.extend(os_errs)

    if FIX:
        print(f"  Исправлено автоматически: {total_fixed}")

    # ── Markdown-отчёт ──────────────────────────────────────────────
    lines = [
        "# Сломанные внутренние ссылки\n",
        f"**Найдено:** {len(all_broken)} проблем, {len(all_os_errors)} пропущено (длинный путь)\n",
    ]

    if not all_broken:
        lines.append("✅ Все внутренние ссылки рабочие!\n")
    else:
        lines += [
            "| Файл | Текст ссылки | Цель | Проблема |",
            "|------|--------------|------|----------|",
        ]
        for item in all_broken[:50]:
            lines.append(
                f"| `{item['file']}` | {item['text'][:30]} "
                f"| `{item['target'][:40]}` | {item['issue']} |"
            )
        if len(all_broken) > 50:
            lines.append(f"\n_...и ещё {len(all_broken) - 50} проблем_")

    if all_os_errors:
        lines += [
            f"\n## Пропущено из-за длинного пути ({len(all_os_errors)})\n",
            "_Markdown-ссылки с путём > 240 символов — OS не может проверить._\n",
            "| Файл | Цель (сокр.) | Проблема |",
            "|------|--------------|----------|",
        ]
        for item in all_os_errors[:20]:
            lines.append(
                f"| `{item['file'][:60]}` | `{item['target'][:50]}` | {item['issue']} |"
            )

    # Внешние URL (список, без ping)
    ext_urls: set[str] = set()
    for f in scan_root.rglob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in re.finditer(r'https?://[^\s\)"\'>\]]+', text):
            url = m.group(0).rstrip('.,;)')
            if len(url) > 10:
                ext_urls.add(url)

    lines += [
        f"\n## Внешние URL ({len(ext_urls)} уникальных)\n",
        "_Внешние ссылки не проверяются автоматически — требуют ручной проверки._\n",
    ]
    for url in sorted(ext_urls)[:30]:
        lines.append(f"- {url}")

    out = DOCS / "BROKEN_LINKS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ── JSON-лог OS-ошибок ────────────────────────────────────────
    if all_os_errors:
        bad_out = DOCS / "bad_links.json"
        bad_out.write_text(
            json.dumps(all_os_errors, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  wrote: {bad_out.relative_to(ROOT)}  ({len(all_os_errors)} длинных путей)")

    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  сломанных ссылок: {len(all_broken)}, пропущено: {len(all_os_errors)}, внешних URL: {len(ext_urls)}")


if __name__ == "__main__":
    main()
