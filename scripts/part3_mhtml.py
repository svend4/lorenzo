"""Часть 3: извлечение текста из MHTML через существующий парсер."""
import sys
from pathlib import Path

# Добавляем папку scripts в путь, чтобы импортировать extract_mhtml
sys.path.insert(0, str(Path(__file__).parent))
from extract_mhtml import extract_text_from_mhtml
from part2_split_md import split_by_h2, slug
from part1_utils import clean


def parse_mhtml(filepath: Path) -> str:
    """Возвращает чистый Markdown из MHTML-файла."""
    print(f"  parsing: {filepath.name}")
    text = extract_text_from_mhtml(str(filepath))
    return clean(text)


def split_mhtml_by_requests(text: str) -> list[tuple[str, str]]:
    """
    Разбивает текст чата на пары (запрос, ответ).
    Каждый блок '[Запрос]' становится новым разделом.
    Возвращает список (заголовок-из-запроса, полный блок).
    """
    parts = re.split(r'(\*\*\[Запрос\]\*\*)', text)
    # parts = ['до первого', '**[Запрос]**', 'текст1', '**[Запрос]**', 'текст2', ...]

    sections = []
    i = 1
    while i < len(parts) - 1:
        header_marker = parts[i]   # '**[Запрос]**'
        block = parts[i + 1]       # запрос + ответ

        # Первые 80 символов запроса → заголовок
        first_line = block.strip().split('\n')[0][:80]
        title = first_line.strip('*: ')

        sections.append((title, clean(header_marker + block)))
        i += 2

    return sections


import re
