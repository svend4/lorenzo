"""
improve_broken_links.py — проверяет внутренние ссылки в docs/.
Находит ссылки на несуществующие файлы и якоря.
Создаёт docs/BROKEN_LINKS.md.

Новое: --fix автоматически исправляет ссылки с неправильным регистром или лишними ../.
Запуск: python scripts/improve_broken_links.py
        python scripts/improve_broken_links.py --fix       # автоматическое исправление
        python scripts/improve_broken_links.py --fix --dry-run  # показать исправления
"""
import os
import re
import sys
from pathlib import Path

FIX     = "--fix"     in sys.argv
DRY_RUN = "--dry-run" in sys.argv

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Паттерны для ссылок
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
ANCHOR_RE = re.compile(r'^#+\s+(.+)$', re.MULTILINE)


def anchor_from_heading(heading: str) -> str:
    """GitHub-style якорь из заголовка."""
    h = heading.lower().strip()
    h = re.sub(r'[^\w\s\-]', '', h)
    h = re.sub(r'\s+', '-', h)
    return '#' + h.strip('-')


def build_anchor_map() -> dict[str, set[str]]:
    """Строит словарь file_path → set of valid anchors."""
    anchor_map: dict[str, set[str]] = {}
    for f in DOCS.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        anchors = set()
        for m in ANCHOR_RE.finditer(text):
            anchors.add(anchor_from_heading(m.group(1)))
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
        filepath.write_text(text, encoding="utf-8")
    return fixes


def check_links(filepath: Path, anchor_map: dict) -> list[dict]:
    """Проверяет все ссылки в файле."""
    text = filepath.read_text(encoding="utf-8")
    broken = []

    for m in LINK_RE.finditer(text):
        link_text = m.group(1)
        target = m.group(2).strip()

        # Пропускаем внешние ссылки
        if target.startswith(('http://', 'https://', 'mailto:', '#')):
            # Якорь в том же файле
            if target.startswith('#'):
                anchors = anchor_map.get(str(filepath), set())
                if target not in anchors:
                    broken.append({
                        "file": str(filepath.relative_to(ROOT)),
                        "text": link_text,
                        "target": target,
                        "issue": "якорь не найден",
                    })
            continue

        # Относительный путь
        if target.startswith('/'):
            resolved = ROOT / target.lstrip('/')
        else:
            resolved = filepath.parent / target

        # Убираем якорь из пути
        anchor = None
        if '#' in str(resolved):
            path_part, anchor = str(resolved).rsplit('#', 1)
            resolved = Path(path_part)
            anchor = '#' + anchor

        if not resolved.exists():
            broken.append({
                "file": str(filepath.relative_to(ROOT)),
                "text": link_text,
                "target": target,
                "issue": "файл не существует",
            })
        elif anchor:
            anchors = anchor_map.get(str(resolved), set())
            if anchor not in anchors:
                broken.append({
                    "file": str(filepath.relative_to(ROOT)),
                    "text": link_text,
                    "target": target,
                    "issue": "якорь не найден в файле",
                })

    return broken


def main():
    print("Проверка внутренних ссылок...")
    if FIX:
        print(f"  Режим: {'dry-run (исправления не записываются)' if DRY_RUN else 'auto-fix'}")
    anchor_map = build_anchor_map()

    all_broken = []
    total_fixed = 0
    for f in sorted(DOCS.rglob("*.md")):
        if f.name == "BROKEN_LINKS.md":
            continue
        broken = check_links(f, anchor_map)
        if FIX and broken:
            fixed = fix_broken_links(f, broken)
            total_fixed += fixed
            # После фикса перепроверяем
            broken = check_links(f, anchor_map)
        all_broken.extend(broken)

    if FIX:
        print(f"  Исправлено автоматически: {total_fixed}")

    lines = [
        "# Сломанные внутренние ссылки\n",
        f"**Найдено:** {len(all_broken)} проблем\n",
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
            lines.append(f"\n_...и ещё {len(all_broken)-50} проблем_")

    # Также проверяем внешние URL (просто список, не ping)
    ext_urls = set()
    for f in DOCS.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
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
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  сломанных ссылок: {len(all_broken)}, внешних URL: {len(ext_urls)}")


if __name__ == "__main__":
    main()
