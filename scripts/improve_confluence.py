"""
improve_confluence.py — конвертирует docs/*.md в формат Confluence Wiki Markup.

Создаёт docs/confluence/ с файлами .wiki.
Основные преобразования:
  # H1 → h1.
  **bold** → *bold*
  `code` → {{code}}
  ```lang ... ``` → {code:language=lang} ... {code}
  [text](url) → [text|url]
  | table | → стандартные таблицы Confluence

Запуск:
    python scripts/improve_confluence.py
    python scripts/improve_confluence.py --section 01-svyazi
    python scripts/improve_confluence.py --dry-run
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
OUT_DIR = DOCS / "confluence"
TODAY = date.today().isoformat()

DRY_RUN = "--dry-run" in sys.argv

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {"SEARCH.md", "READABILITY.md", "SPELLCHECK.md", "CONTENT_GAPS.md",
              "LINK_PREVIEW.md", "BROKEN_LINKS.md"}


def md_to_confluence(text: str, source_path: Path) -> str:
    lines = text.split('\n')
    result = []
    in_code = False
    code_lang = ""

    for line in lines:
        # Код-блок начало/конец
        code_start = re.match(r'^```(\w*)', line)
        if code_start:
            if not in_code:
                in_code = True
                code_lang = code_start.group(1) or "none"
                lang_str = f":language={code_lang}" if code_lang != "none" else ""
                result.append(f"{{code{lang_str}}}")
            else:
                in_code = False
                result.append("{code}")
            continue

        if in_code:
            result.append(line)
            continue

        # Заголовки
        for level in range(6, 0, -1):
            prefix = '#' * level + ' '
            if line.startswith(prefix):
                content = line[len(prefix):]
                line = f"h{level}. {content}"
                break

        # HTML-комментарии — убираем
        line = re.sub(r'<!--.*?-->', '', line)

        # Горизонтальная линия
        if re.match(r'^---+$', line.strip()):
            result.append("----")
            continue

        # Таблица — конвертируем заголовок
        if line.startswith('|') and '|' in line[1:]:
            cells = [c.strip() for c in line.split('|')[1:-1]]
            # Строка-разделитель --- пропускаем
            if all(re.match(r'^-+$', c.replace(':', '')) for c in cells if c):
                continue
            result.append('|| ' + ' || '.join(cells) + ' ||')
            continue

        # Inline: bold **text** / __text__
        line = re.sub(r'\*\*(.+?)\*\*', r'*\1*', line)
        line = re.sub(r'__(.+?)__', r'*\1*', line)

        # Italic *text* / _text_ (не путать с bold)
        line = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'_\1_', line)
        line = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'_\1_', line)

        # Strikethrough ~~text~~
        line = re.sub(r'~~(.+?)~~', r'-\1-', line)

        # Inline code `code` → {{code}}
        line = re.sub(r'`([^`]+)`', r'{{\1}}', line)

        # Links [text](url) → [text|url]
        line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'[\1|\2]', line)

        # Images ![alt](url)
        line = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'![\2]!', line)

        # Blockquote > text → {quote}text{quote} (упрощённо)
        if line.startswith('> '):
            line = '{quote}' + line[2:] + '{quote}'

        # Списки — Confluence использует * и # как в markdown, почти идентично
        # Неупорядоченный: - item → * item
        line = re.sub(r'^(\s*)-\s+', r'\1* ', line)

        result.append(line)

    # Добавляем метаданные в начало
    rel = source_path.relative_to(DOCS)
    header = (
        f"{{info:title=Источник}}\n"
        f"Сгенерировано из: {{{{docs/{rel}}}}}\n"
        f"Дата: {TODAY}\n"
        f"{{info}}\n\n"
    )
    return header + '\n'.join(result)


def main() -> None:
    print("🏗️  improve_confluence.py — конвертация в Confluence Wiki")
    if DRY_RUN:
        print("   Режим: dry-run")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES and "confluence" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    if not DRY_RUN:
        OUT_DIR.mkdir(exist_ok=True)

    ok = 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
            wiki = md_to_confluence(text, f)

            if not DRY_RUN:
                rel = f.relative_to(DOCS)
                out = OUT_DIR / rel.with_suffix('.wiki')
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(wiki, encoding="utf-8")
            ok += 1
        except Exception as e:
            print(f"  ❌ {f.name}: {e}")

    print(f"  Конвертировано: {ok}/{len(files)} файлов")
    if not DRY_RUN:
        print(f"  Вывод: {OUT_DIR.relative_to(ROOT)}/")
        print("  Формат: .wiki — Confluence Wiki Markup")


if __name__ == "__main__":
    main()
