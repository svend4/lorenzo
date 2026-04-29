"""
improve_broken_links.py — проверяет внутренние ссылки в docs/.
Находит ссылки на несуществующие файлы и якоря.
Создаёт docs/BROKEN_LINKS.md.
Запуск: python scripts/improve_broken_links.py
"""
import re
from pathlib import Path

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
    anchor_map = build_anchor_map()

    all_broken = []
    for f in sorted(DOCS.rglob("*.md")):
        if f.name == "BROKEN_LINKS.md":
            continue
        broken = check_links(f, anchor_map)
        all_broken.extend(broken)

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
