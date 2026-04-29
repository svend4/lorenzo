"""
improve_text_segmenter.py — разбивает большие файлы на логические части.

Для файлов > MAX_WORDS слов:
  1. Определяет смысловые границы (заголовки H2/H3, пустые строки, тематические сдвиги)
  2. Разбивает на части с сохранением контекста (breadcrumb)
  3. Создаёт индекс-файл и отдельные части в подпапке

Режимы:
  --dry-run  (по умолчанию)
  --apply    — записать части на диск
  --max-words N     — порог для разбиения (по умолч.: 1500)
  --part-size N     — целевой размер части в словах (по умолч.: 600)
  --section         — обрабатывать секцию

Запуск:
    python scripts/improve_text_segmenter.py --dry-run
    python scripts/improve_text_segmenter.py --apply --section 02-anthropic-vacancies
    python scripts/improve_text_segmenter.py --apply --max-words 1000 --part-size 400
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

APPLY    = "--apply"   in sys.argv
DRY_RUN  = not APPLY

MAX_WORDS  = 1500
PART_SIZE  = 600

if "--max-words" in sys.argv:
    idx = sys.argv.index("--max-words")
    if idx + 1 < len(sys.argv):
        MAX_WORDS = int(sys.argv[idx + 1])

if "--part-size" in sys.argv:
    idx = sys.argv.index("--part-size")
    if idx + 1 < len(sys.argv):
        PART_SIZE = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "README.md", "SEARCH.md", "OUTLINE.md", "COMPARE.md",
    "SOURCE_MAP.md", "TIMELINE.md", "NAMED_ENTITIES.md",
}


def _word_count(text: str) -> int:
    return len(text.split())


def _extract_title(text: str, path: Path) -> str:
    m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    return m.group(1).strip() if m else path.stem.replace('-', ' ').title()


def _split_into_segments(text: str, target_size: int) -> list[dict]:
    """
    Делит текст на сегменты по смысловым границам.
    Возвращает [{heading, level, content, word_count}].
    """
    # Находим все заголовки как потенциальные границы
    heading_re = re.compile(r'^(#{1,3})\s+(.+)$', re.MULTILINE)
    matches = list(heading_re.finditer(text))

    if len(matches) < 2:
        # Нет заголовков — делим по абзацам
        paragraphs = [p.strip() for p in re.split(r'\n{3,}', text) if p.strip()]
        segments = []
        current_content = []
        current_words = 0
        for i, para in enumerate(paragraphs):
            pw = _word_count(para)
            if current_words + pw > target_size and current_content:
                segments.append({
                    "heading": f"Часть {len(segments)+1}",
                    "level": 2,
                    "content": '\n\n'.join(current_content),
                    "word_count": current_words,
                })
                current_content = [para]
                current_words = pw
            else:
                current_content.append(para)
                current_words += pw
        if current_content:
            segments.append({
                "heading": f"Часть {len(segments)+1}",
                "level": 2,
                "content": '\n\n'.join(current_content),
                "word_count": current_words,
            })
        return segments

    # Разбиваем по заголовкам
    raw_sections = []
    for i, m in enumerate(matches):
        level = len(m.group(1))
        heading = m.group(2).strip()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        content = text[start:end].strip()
        raw_sections.append({
            "heading": heading,
            "level": level,
            "content": content,
            "word_count": _word_count(content),
        })

    # Объединяем маленькие секции, разбиваем большие
    segments = []
    buffer_heading = ""
    buffer_content = []
    buffer_words = 0
    buffer_level = 2

    for sec in raw_sections:
        if sec["word_count"] > target_size * 1.5:
            # Сброс буфера
            if buffer_content:
                segments.append({
                    "heading": buffer_heading,
                    "level": buffer_level,
                    "content": '\n\n'.join(buffer_content),
                    "word_count": buffer_words,
                })
                buffer_content, buffer_words = [], 0

            # Делим большую секцию по абзацам
            paras = [p.strip() for p in re.split(r'\n{2,}', sec["content"]) if p.strip()]
            cur_paras, cur_words = [], 0
            for para in paras:
                pw = _word_count(para)
                if cur_words + pw > target_size and cur_paras:
                    segments.append({
                        "heading": sec["heading"],
                        "level": sec["level"],
                        "content": '\n\n'.join(cur_paras),
                        "word_count": cur_words,
                    })
                    cur_paras, cur_words = [para], pw
                else:
                    cur_paras.append(para)
                    cur_words += pw
            if cur_paras:
                segments.append({
                    "heading": sec["heading"],
                    "level": sec["level"],
                    "content": '\n\n'.join(cur_paras),
                    "word_count": cur_words,
                })
        elif buffer_words + sec["word_count"] > target_size and buffer_content:
            segments.append({
                "heading": buffer_heading,
                "level": buffer_level,
                "content": '\n\n'.join(buffer_content),
                "word_count": buffer_words,
            })
            buffer_heading = sec["heading"]
            buffer_content = [sec["content"]]
            buffer_words = sec["word_count"]
            buffer_level = sec["level"]
        else:
            if not buffer_heading:
                buffer_heading = sec["heading"]
                buffer_level = sec["level"]
            buffer_content.append(sec["content"])
            buffer_words += sec["word_count"]

    if buffer_content:
        segments.append({
            "heading": buffer_heading,
            "level": buffer_level,
            "content": '\n\n'.join(buffer_content),
            "word_count": buffer_words,
        })

    return segments


def _write_parts(path: Path, title: str, segments: list[dict]) -> Path:
    """Записывает части в подпапку рядом с оригиналом."""
    parts_dir = path.parent / (path.stem + "-parts")
    parts_dir.mkdir(exist_ok=True)

    # Индексный файл
    index_lines = [
        f"# {title} — Оглавление\n",
        f"_Разбито автоматически: {TODAY}_\n",
        f"Частей: **{len(segments)}**\n",
        f"Оригинал: [{path.name}](../{path.name})\n",
        "## Части\n",
    ]

    for i, seg in enumerate(segments, 1):
        part_name = f"part-{i:02d}.md"
        part_path = parts_dir / part_name
        rel_to_parts = part_name

        # Пишем часть
        part_content = [
            f"# {title}\n",
            f"> Часть {i}/{len(segments)}: **{seg['heading']}**\n",
            f"> [← Оглавление](index.md) | [← Оригинал](../{path.name})\n\n",
            f"## {seg['heading']}\n\n",
            seg["content"],
        ]
        if i < len(segments):
            part_content.append(f"\n\n---\n[Следующая часть →](part-{i+1:02d}.md)")
        if i > 1:
            part_content.insert(-1, f"\n[← Предыдущая часть](part-{i-1:02d}.md)")

        part_path.write_text('\n'.join(part_content), encoding="utf-8")
        index_lines.append(
            f"{i}. [{seg['heading']}]({rel_to_parts}) — {seg['word_count']} слов"
        )

    (parts_dir / "index.md").write_text('\n'.join(index_lines) + '\n', encoding="utf-8")
    return parts_dir


def main() -> None:
    print("✂️  improve_text_segmenter.py — разбивка больших файлов")
    print(f"   Порог: {MAX_WORDS} слов | Размер части: {PART_SIZE} слов")
    print(f"   Режим: {'APPLY' if APPLY else 'dry-run'}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]

    # Только большие файлы
    large = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        wc = _word_count(text)
        if wc >= MAX_WORDS:
            large.append((f, text, wc))

    large.sort(key=lambda x: -x[2])
    print(f"   Всего файлов: {len(files)}")
    print(f"   Больших (≥{MAX_WORDS} слов): {len(large)}\n")

    if not large:
        print("  Нет файлов для разбивки.")
        return

    processed = 0
    for path, text, wc in large:
        title = _extract_title(text, path)
        segments = _split_into_segments(text, PART_SIZE)
        rel = path.relative_to(ROOT)

        print(f"  📄 {rel}")
        print(f"     {wc} слов → {len(segments)} частей")
        for i, seg in enumerate(segments, 1):
            print(f"     {i:2d}. {seg['heading'][:60]} ({seg['word_count']} сл.)")

        if APPLY:
            parts_dir = _write_parts(path, title, segments)
            print(f"     → {parts_dir.relative_to(ROOT)}/")
            processed += 1
        print()

    if APPLY:
        print(f"  ✅ Разбито файлов: {processed}")
    else:
        print(f"  Запустите с --apply для реальной записи.")


if __name__ == "__main__":
    main()
