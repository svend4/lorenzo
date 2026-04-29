"""
improve_backlinks.py — индекс обратных ссылок.
Для каждого файла показывает, какие другие файлы на него ссылаются.
Добавляет блок "Кто ссылается" в конец файла и создаёт docs/BACKLINKS.md.
Запуск: python scripts/improve_backlinks.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP = {"BACKLINKS.md", "SITEMAP.md", "CROSSREFS.md", "SIMILAR.md"}
MARKER = "<!-- backlinks -->"


def extract_links(text: str, base: Path) -> set[str]:
    """Извлекает все внутренние md-ссылки из текста."""
    links = set()
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
        href = m.group(2).strip()
        if href.startswith("http") or href.startswith("#"):
            continue
        # Нормализуем путь
        target = (base.parent / href).resolve()
        if target.exists():
            links.add(str(target.relative_to(ROOT)))
    return links


def main():
    print("Строю индекс обратных ссылок...")

    # Шаг 1: для каждого файла — список файлов, на которые он ссылается
    forward: dict[str, set[str]] = {}
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        rel  = str(f.relative_to(ROOT))
        forward[rel] = extract_links(text, f)

    # Шаг 2: инвертируем — кто ссылается на каждый файл
    backward: dict[str, list[str]] = defaultdict(list)
    for src, targets in forward.items():
        for tgt in targets:
            backward[tgt].append(src)

    # BACKLINKS.md
    lines = [
        "# Индекс обратных ссылок\n",
        f"**Файлов с входящими ссылками:** {len(backward)}\n",
        "## Топ-30 самых цитируемых документов\n",
        "| Документ | Входящих ссылок | Ссылающиеся файлы |",
        "|----------|----------------|-------------------|",
    ]

    top = sorted(backward.items(), key=lambda x: -len(x[1]))
    for tgt, srcs in top[:30]:
        short = tgt.split("/")[-1].replace(".md", "")[:35]
        src_list = ", ".join(f"`{s.split('/')[-1]}`" for s in srcs[:4])
        if len(srcs) > 4:
            src_list += f" +{len(srcs)-4}"
        lines.append(f"| `{short}` | {len(srcs)} | {src_list} |")

    # По разделам
    lines.append("\n## Ссылки по разделам\n")
    by_section: dict[str, dict] = defaultdict(lambda: {"in": 0, "out": 0})
    for f, targets in forward.items():
        rel = Path(f).relative_to("docs") if f.startswith("docs/") else Path(f)
        sec = rel.parts[0] if len(rel.parts) > 1 else "root"
        by_section[sec]["out"] += len(targets)
    for tgt, srcs in backward.items():
        rel = Path(tgt).relative_to("docs") if tgt.startswith("docs/") else Path(tgt)
        sec = rel.parts[0] if len(rel.parts) > 1 else "root"
        by_section[sec]["in"] += len(srcs)

    lines += ["| Раздел | Входящих | Исходящих |",
              "|--------|----------|-----------|"]
    for sec, d in sorted(by_section.items()):
        lines.append(f"| **{sec}** | {d['in']} | {d['out']} |")

    out = DOCS / "BACKLINKS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")

    # Шаг 3: добавляем блок в файлы с 3+ входящих ссылок
    updated = 0
    for tgt, srcs in backward.items():
        if len(srcs) < 3:
            continue
        tgt_path = ROOT / tgt
        if not tgt_path.exists() or tgt_path.name in SKIP:
            continue
        text = tgt_path.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        block = [f"\n{MARKER}\n", "---\n",
                 f"**Кто ссылается на этот документ ({len(srcs)}):**"]
        for src in sorted(srcs)[:8]:
            block.append(f"- [{Path(src).stem}]({Path(src).relative_to(ROOT)})")
        if len(srcs) > 8:
            block.append(f"- _...ещё {len(srcs)-8}_")
        block.append("")
        tgt_path.write_text(text + "\n".join(block) + "\n", encoding="utf-8")
        updated += 1

    print(f"  файлов с обратными ссылками: {len(backward)}, обновлено: {updated}")


if __name__ == "__main__":
    main()
