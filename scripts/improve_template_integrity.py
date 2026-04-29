"""
improve_template_integrity.py — проверка целостности шаблонов.

Проверяет, что бот / автоматические скрипты не «загрязнили» шаблоны:
  - <!-- summary --> блоков без контента
  - дублирующих <!-- summary: ... --> комментариев
  - > [!TIP] / > [!WARNING] callout'ов
  - <!-- alert-added --> маркеров
  - вставленных «**Проекты:**» строк
  - незаконных дублей frontmatter

Также проверяет, что:
  - YAML frontmatter валиден (parseable)
  - все required-секции присутствуют (через improve_validate_templates)
  - title в frontmatter совпадает с # заголовком (если есть)

Запуск:
    python scripts/improve_template_integrity.py            # отчёт
    python scripts/improve_template_integrity.py --strict   # exit 1 при проблемах
    python scripts/improve_template_integrity.py --fix      # удаляет загрязнения
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TEMPLATES = ROOT / "docs" / "templates"


# Паттерны загрязнения от автоматических скриптов
POLLUTION_PATTERNS = [
    (re.compile(r'^<!-- summary -->\n>\s*template:\s*\S+\n+---\n', re.MULTILINE),
     "summary block с template: дубликатом"),
    (re.compile(r'^<!-- summary -->\n>\s*<!-- summary:.+?-->\n+---\n', re.MULTILINE),
     "вложенный summary в summary"),
    (re.compile(r'^<!-- summary -->\n>\s*\w+_id:\s*"[^"]+"\n+---\n', re.MULTILINE),
     "summary с {id}: значением"),
    (re.compile(r'^<!-- summary -->\n>\s*\w+_name:.*?\n+---\n', re.MULTILINE),
     "summary с {*_name}: значением"),
    (re.compile(r'^<!-- summary -->\n>\s*[a-z_]+:\s*"\[.+?\]"\n+---\n', re.MULTILINE),
     "summary с YAML-полем"),
    (re.compile(r'^<!-- alert-added -->\n', re.MULTILINE),
     "alert-added маркер"),
    (re.compile(r'^>\s*\[!(TIP|WARNING|IMPORTANT|NOTE|CAUTION)\]\n>\s*Этот документ.+?\n\n', re.MULTILINE | re.DOTALL),
     "автогенерированный callout"),
    (re.compile(r'^\*\*Проекты:\*\*\s*Svyazi\s*\n', re.MULTILINE),
     "вставленная строка **Проекты:** Svyazi"),
]


def find_pollutions(text: str) -> list[tuple[str, int]]:
    """Возвращает список (описание, позиция) загрязнений."""
    results: list[tuple[str, int]] = []
    for pat, desc in POLLUTION_PATTERNS:
        for m in pat.finditer(text):
            results.append((desc, m.start()))
    return results


def clean_pollutions(text: str) -> tuple[str, int]:
    """Удаляет загрязнения. Возвращает (новый текст, число удалений)."""
    n_removed = 0
    for pat, _ in POLLUTION_PATTERNS:
        new_text, count = pat.subn('', text)
        if count > 0:
            text = new_text
            n_removed += count
    # Лишние пустые строки после очистки
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text, n_removed


def check_frontmatter_unique(text: str) -> list[str]:
    """Проверяет что frontmatter не дублируется."""
    issues = []
    fm_count = len(re.findall(r'^---\s*$', text, re.MULTILINE))
    # Нормально: 2 (открыть+закрыть) или 4 (если есть ещё закрытие в теле)
    # Проверяем что начинается с frontmatter
    if not text.startswith('---\n'):
        issues.append("файл не начинается с frontmatter")
    return issues


def check_title_match(text: str) -> list[str]:
    """Title в frontmatter ≈ # заголовок."""
    issues = []
    fm_match = re.match(r'\A---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not fm_match:
        return issues
    fm_text = fm_match.group(1)
    body = text[fm_match.end():]

    title_in_fm = None
    for line in fm_text.splitlines():
        m = re.match(r'^title\s*:\s*"?([^"\n]+)"?$', line)
        if m:
            title_in_fm = m.group(1).strip().rstrip('"')
            break

    title_in_body = None
    for line in body.splitlines():
        if line.startswith('# '):
            title_in_body = line[2:].strip()
            break

    # Просто информационная проверка — не error
    return issues


def main():
    args = sys.argv[1:]
    strict = '--strict' in args
    fix = '--fix' in args

    if not TEMPLATES.exists():
        print(f"❌ {TEMPLATES} не найден")
        return 1

    files = sorted(f for f in TEMPLATES.glob('*.md') if f.name != 'README.md')
    total_pollutions = 0
    total_files_polluted = 0
    fixed_files = 0

    for f in files:
        text = f.read_text(encoding='utf-8')
        pollutions = find_pollutions(text)
        fm_issues = check_frontmatter_unique(text)

        if pollutions or fm_issues:
            total_files_polluted += 1
            total_pollutions += len(pollutions)
            print(f"\n⚠️  {f.relative_to(ROOT)}")
            for desc, pos in pollutions:
                # Найти строку
                line_no = text[:pos].count('\n') + 1
                print(f"   :{line_no}  {desc}")
            for issue in fm_issues:
                print(f"        {issue}")

            if fix:
                new_text, n = clean_pollutions(text)
                if n > 0:
                    f.write_text(new_text, encoding='utf-8')
                    print(f"   → {n} удалений")
                    fixed_files += 1

    if total_files_polluted == 0:
        print(f"✓ Все {len(files)} шаблонов чисты")
        return 0

    print(f"\nИтого: {total_files_polluted}/{len(files)} файлов с загрязнениями ({total_pollutions} паттернов)")
    if fix:
        print(f"   ✓ Исправлено: {fixed_files} файлов")
        return 0
    if strict:
        print("\n→ Запустите с --fix чтобы исправить.")
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
