"""Часть 2: разбивка Markdown-файла по H2-заголовкам."""
from part1_utils import clean
import re

def split_by_h2(text: str) -> list[tuple[str, str]]:
    """
    Возвращает список (заголовок, тело) для каждой H2-секции.
    Первый элемент — всё до первого H2 (заголовок = '').
    """
    pattern = re.compile(r'^## (.+)$', re.MULTILINE)
    positions = [(m.start(), m.group(1)) for m in pattern.finditer(text)]

    sections = []
    if not positions:
        return [('', clean(text))]

    # Контент до первого H2
    preamble = text[:positions[0][0]].strip()
    if preamble:
        sections.append(('', clean(preamble)))

    for i, (pos, title) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        body = text[pos:end].strip()
        sections.append((title, clean(body)))

    return sections


def slug(title: str) -> str:
    """Превращает заголовок в имя файла."""
    s = title.lower()
    s = re.sub(r'[^а-яёa-z0-9]+', '-', s)
    s = s.strip('-')
    return s[:60] or 'section'
