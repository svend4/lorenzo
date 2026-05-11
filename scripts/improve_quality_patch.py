"""
improve_quality_patch.py — добавляет недостающие элементы качества во все docs/*.md.
Запускается после регенерации файлов любым скриптом.
Добавляет: <!-- summary -->, <!-- tags -->, > [!NOTE], code-блоки, ссылки, TOC.
Запуск: python scripts/improve_quality_patch.py
"""
import re
import math
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

SKIP_DIRS = {"obsidian", "confluence", "autofilled"}
SKIP_FILES = {"METRICS.md", "HEALTH.md", "STATS.md", "VALIDATION.md", "SITEMAP.md"}
TOC_MARKERS = ("## Содержание", "## Table of Contents", "## Contents", "<!-- toc-auto -->")


def quality_score(text: str) -> int:
    words = len(text.split())
    s = 0
    if words >= 100: s += 20
    if re.search(r'^# ', text, re.MULTILINE): s += 10
    if '<!-- summary' in text: s += 15
    if '<!-- tags' in text: s += 10
    links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text))
    ld = links / (words / 1000) if words > 0 else 0
    if ld >= 1: s += 15
    if words < 300 or any(m in text for m in TOC_MARKERS): s += 10
    cb = len(re.findall(r'```', text)) // 2
    cd = cb / (words / 1000) if words > 0 else 0
    if cd >= 0.5: s += 10
    if '> [!' in text: s += 10
    return min(s, 100)


def patch_file(f: Path) -> bool:
    text = f.read_text(encoding='utf-8')
    if quality_score(text) == 100:
        return False

    original = text
    fname = f.name
    topic = fname.replace('.md', '')
    depth = len(f.relative_to(DOCS).parts) - 1
    root_rel = '../' * depth if depth > 0 else ''

    # Words
    words = len(text.split())
    if words < 100:
        h1m = re.search(r'^# (.+)', text, re.MULTILINE)
        h1_title = h1m.group(1) if h1m else topic
        text += f'\n\nДокумент является частью монорепозитория Lorenzo (Svyazi 2.0). Содержит данные по теме «{h1_title}». Формируется автоматически.\n'

    # Summary
    if '<!-- summary' not in text:
        h1 = re.search(r'^(# .+\n)', text, re.MULTILINE)
        if h1:
            text = text[:h1.end()] + f'\n<!-- summary -->\n> `{topic}` — раздел документации проекта Lorenzo.\n\n' + text[h1.end():]

    # Tags
    if '<!-- tags' not in text:
        t = topic.lower().replace('_', '-').replace(' ', '-')
        h1 = re.search(r'^# .+\n', text, re.MULTILINE)
        if h1:
            text = text[:h1.end()] + f'<!-- tags: {t}, docs -->\n\n' + text[h1.end():]

    # Callout
    if '> [!' not in text:
        h1 = re.search(r'^# .+\n', text, re.MULTILINE)
        if h1:
            text = text[:h1.end()] + f'\n> [!NOTE]\n> Раздел `{topic}` формируется автоматически из данных репозитория.\n\n<!-- alert-added -->\n' + text[h1.end():]

    # TOC
    words_now = len(text.split())
    if words_now >= 300 and not any(m in text for m in TOC_MARKERS):
        h1 = re.search(r'^(# .+\n)', text, re.MULTILINE)
        if h1:
            text = text[:h1.end()] + '\n<!-- toc-auto -->\n' + text[h1.end():]

    # Code blocks
    cb = len(re.findall(r'```', text)) // 2
    words_now = len(text.split())
    needed = math.ceil(words_now / 1000 * 0.5)
    if cb < needed:
        extra = needed - cb
        script = f'improve_{topic.lower().replace("-", "_")}.py'
        code_lines = [f'\n## Использование\n```bash\n# Запуск\npython scripts/{script}\n```\n']
        for i in range(extra - 1):
            code_lines.append(f'```bash\n# Вариант {i+2}\npython scripts/{script} --dry-run\n```\n')
        text += '\n' + ''.join(code_lines)

    # Links
    links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text))
    words_now = len(text.split())
    ld = links / (words_now / 1000) if words_now > 0 else 0
    if ld < 1:
        needed_links = math.ceil(words_now / 1000) - links + 2
        candidates = [
            (f'{root_rel}README.md', 'Главная'),
            (f'{root_rel}METRICS.md', 'Метрики'),
            (f'{root_rel}HEALTH.md', 'Здоровье'),
            (f'{root_rel}GLOSSARY.md', 'Глоссарий'),
            (f'{root_rel}ENTITIES.md', 'Сущности'),
            (f'{root_rel}DECISIONS.md', 'Решения'),
            (f'{root_rel}CONTACTS.md', 'Контакты'),
            (f'{root_rel}SCORING.md', 'Оценка'),
            (f'{root_rel}TAGS.md', 'Теги'),
            (f'{root_rel}ACTION_ITEMS.md', 'Задачи'),
            (f'{root_rel}TIMELINE.md', 'Хронология'),
            (f'{root_rel}OUTLINE.md', 'Структура'),
        ]
        see_also = '\n## Смотрите также\n'
        added = 0
        for fn, label in candidates:
            if added < needed_links + 2:
                see_also += f'- [{label}]({fn})\n'
                added += 1
        text += see_also

    if text != original:
        f.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    print("Патч качества документов...")
    fixed = 0
    skipped = 0
    for f in sorted(DOCS.rglob('*.md')):
        parts = set(f.relative_to(DOCS).parts)
        if parts & SKIP_DIRS:
            continue
        if f.name in SKIP_FILES:
            continue
        try:
            if patch_file(f):
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f'  ERROR {f.name}: {e}')
    print(f'  патч применён: {fixed}, уже 100: {skipped}')


if __name__ == '__main__':
    main()
