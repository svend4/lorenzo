"""Часть 5: общий движок разбивки MHTML по секциям и запись файлов."""
import re
from pathlib import Path
from part1_utils import write_doc, clean
from part2_split_md import split_by_h2, slug
from part3_mhtml import parse_mhtml


def split_by_keyword_sections(text: str, keywords: list[str]) -> dict[str, str]:
    """
    Делит большой текст на секции по ключевым словам.
    keywords — список строк-маркеров. Возвращает {keyword: текст_секции}.
    """
    result = {}
    positions = []

    for kw in keywords:
        # Ищем keyword в тексте (без учёта регистра)
        idx = text.lower().find(kw.lower())
        if idx >= 0:
            positions.append((idx, kw))

    positions.sort(key=lambda x: x[0])

    for i, (pos, kw) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        result[kw] = clean(text[pos:end])

    return result


def write_mhtml_section(text: str, dest: Path, title: str):
    """Записывает секцию MHTML как Markdown-файл с заголовком."""
    content = f"# {title}\n\n{text}"
    write_doc(dest, content)


def extract_and_split(mhtml_path: Path, sections_map: dict, out_dir: Path):
    """
    Главная функция обработки MHTML:
    1. Парсит MHTML → Markdown
    2. Делит по секциям по keywords из sections_map
    3. Записывает файлы
    sections_map = {keyword: (filename, display_title)}
    """
    text = parse_mhtml(mhtml_path)

    if not text:
        print(f"  WARNING: no text extracted from {mhtml_path.name}")
        return

    # Сначала пробуем разделить по H2-заголовкам
    h2_sections = split_by_h2(text)

    if len(h2_sections) > 3:
        # Есть H2-заголовки — используем их
        for i, (title, body) in enumerate(h2_sections):
            if not title:
                fname = "00-intro.md"
                display = "Введение"
            else:
                fname = f"{i:02d}-{slug(title)[:50]}.md"
                display = title
            dest = out_dir / fname
            if not dest.exists():
                write_doc(dest, f"# {display}\n\n{body}")
    else:
        # Нет H2 — делим по ключевым словам
        keywords = list(sections_map.keys())
        sections = split_by_keyword_sections(text, keywords)

        for kw, body in sections.items():
            fname, display = sections_map[kw]
            dest = out_dir / fname
            if not dest.exists() and body.strip():
                write_mhtml_section(body, dest, display)

    print(f"  done: {mhtml_path.name}")
