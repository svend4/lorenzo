"""
improve_validate.py — валидация структуры репозитория.
Проверяет: наличие README в разделах, правильность именования,
непустые файлы, корректность ссылок, обязательные мета-поля.
Создаёт docs/VALIDATION.md.
Запуск: python scripts/improve_validate.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

REQUIRED_SECTIONS = [
    "01-svyazi",
    "02-anthropic-vacancies",
    "03-technology-combinations",
    "04-ai-collaborations",
    "05-habr-projects",
]

REQUIRED_META_FILES = [
    "README.md", "GLOSSARY.md", "TIMELINE.md", "DECISIONS.md",
    "HEALTH.md", "READING_ORDER.md", "SITEMAP.md",
]

MIN_FILE_WORDS  = 30
MIN_FILE_CHARS  = 150


def check_section_readmes() -> list[str]:
    issues = []
    for sec in REQUIRED_SECTIONS:
        readme = DOCS / sec / "README.md"
        if not readme.exists():
            issues.append(f"❌ Нет README.md в `docs/{sec}/`")
        else:
            text = readme.read_text(encoding="utf-8")
            if len(text.split()) < 20:
                issues.append(f"⚠️ README.md в `{sec}` слишком короткий ({len(text.split())} слов)")
    return issues


def check_meta_files() -> list[str]:
    issues = []
    for name in REQUIRED_META_FILES:
        p = DOCS / name
        if not p.exists():
            issues.append(f"❌ Отсутствует `docs/{name}`")
    return issues


def check_empty_files() -> list[str]:
    issues = []
    for f in sorted(DOCS.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        words = len(text.split())
        if words < MIN_FILE_WORDS:
            rel = f.relative_to(ROOT)
            issues.append(f"⚠️ Слишком короткий файл: `{rel}` ({words} слов)")
    return issues


def check_naming() -> list[str]:
    issues = []
    bad_pattern = re.compile(r'[А-ЯЁа-яё\s]')  # кириллица или пробелы в имени
    for f in sorted(DOCS.rglob("*.md")):
        name = f.name
        # Пропускаем мета-файлы в верхнем регистре
        if name == name.upper().replace(".MD", ".md"):
            continue
        if bad_pattern.search(f.stem) and len(f.stem) > 30:
            rel = f.relative_to(ROOT)
            issues.append(f"ℹ️ Длинное кириллическое имя: `{rel}`")
    return issues[:10]  # не более 10


def check_h1_titles() -> list[str]:
    issues = []
    for f in sorted(DOCS.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        if len(text.split()) < MIN_FILE_WORDS:
            continue
        if not re.search(r'^# ', text, re.MULTILINE):
            rel = f.relative_to(ROOT)
            issues.append(f"⚠️ Нет заголовка H1: `{rel}`")
    return issues[:20]


def check_broken_internal(quick: bool = True) -> list[str]:
    issues = []
    for f in sorted(DOCS.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r'\[([^\]]+)\]\(([^)#]+\.md[^)]*)\)', text):
            href = m.group(2).split("#")[0].strip()
            if href.startswith("http"):
                continue
            target = (f.parent / href).resolve()
            if not target.exists():
                rel = f.relative_to(ROOT)
                issues.append(f"🔗 Сломана ссылка в `{rel}`: `{href}`")
        if quick and len(issues) >= 15:
            break
    return issues[:15]


def main():
    print("Валидация структуры репозитория...")

    all_issues: dict[str, list[str]] = {}

    checks = [
        ("Разделы и README",     check_section_readmes),
        ("Мета-файлы",           check_meta_files),
        ("Пустые/короткие файлы", check_empty_files),
        ("Именование файлов",    check_naming),
        ("Заголовки H1",         check_h1_titles),
        ("Внутренние ссылки",    check_broken_internal),
    ]

    total_ok   = 0
    total_warn = 0
    total_err  = 0

    for name, fn in checks:
        issues = fn()
        all_issues[name] = issues
        for i in issues:
            if i.startswith("❌"): total_err  += 1
            elif i.startswith("⚠️"): total_warn += 1
            else: total_ok += 1
        if not issues:
            total_ok += 1

    lines = [
        "# Валидация структуры репозитория\n",
        f"**Ошибок:** {total_err}  **Предупреждений:** {total_warn}  "
        f"**Пройдено:** {total_ok}\n",

        "## Сводка\n",
        "| Проверка | Статус | Проблем |",
        "|----------|--------|---------|",
    ]

    for name, issues in all_issues.items():
        errs  = sum(1 for i in issues if i.startswith("❌"))
        warns = sum(1 for i in issues if i.startswith("⚠️"))
        if errs > 0:
            status = "❌"
        elif warns > 0:
            status = "⚠️"
        else:
            status = "✅"
        lines.append(f"| {name} | {status} | {len(issues)} |")

    for name, issues in all_issues.items():
        if not issues:
            lines += [f"\n## ✅ {name}\n", "_Всё в порядке_"]
            continue
        lines.append(f"\n## {name}\n")
        for issue in issues:
            lines.append(f"- {issue}")

    # Итог
    if total_err == 0 and total_warn == 0:
        lines += ["\n## Итог\n", "✅ **Репозиторий прошёл все проверки!**"]
    elif total_err == 0:
        lines += ["\n## Итог\n",
                  f"⚠️ **{total_warn} предупреждений** — рекомендуется исправить."]
    else:
        lines += ["\n## Итог\n",
                  f"❌ **{total_err} ошибок, {total_warn} предупреждений** — требуется исправление."]

    out = DOCS / "VALIDATION.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  ошибок: {total_err}, предупреждений: {total_warn}, ок: {total_ok}")


if __name__ == "__main__":
    main()
