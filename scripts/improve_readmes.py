"""
improve_readmes.py — создаёт README.md для каждой подпапки docs/.
README содержит: список файлов, первые строки каждого файла как описание.
Запуск: python scripts/improve_readmes.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

FOLDER_TITLES = {
    "01-svyazi": "Svyazi 2.0 — Архитектура и исследование",
    "02-anthropic-vacancies": "Вакансии Anthropic — Анализ по кластерам",
    "03-technology-combinations": "Комбинирование технологий для новых свойств",
    "04-ai-collaborations": "Поиск AI-коллабораций",
    "05-habr-projects": "Уникальные проекты с Хабра",
    "ensembles": "Ансамбли проектов",
    "clusters": "Кластеры вакансий",
    "memory": "Системы памяти",
    "knowledge": "Системы знаний",
}


def first_description(path: Path) -> str:
    """Берёт первый непустой абзац после заголовка."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            # Обрезаем до 120 символов
            return line[:120] + ("…" if len(line) > 120 else "")
    return ""


RICH_MARKERS = (
    "<!-- abstract-auto -->",
    "<!-- backlinks-auto -->",
    "<!-- similar-docs -->",
    "<!-- textrank-summary -->",
)


def make_readme(folder: Path):
    files = sorted(f for f in folder.glob("*.md") if f.name != "README.md")
    if not files:
        return

    # Не перезаписывать README с более богатым авто-сгенерированным контентом
    readme_path = folder / "README.md"
    if readme_path.exists():
        existing = readme_path.read_text(encoding="utf-8")
        if any(marker in existing for marker in RICH_MARKERS):
            return

    title = FOLDER_TITLES.get(folder.name, folder.name)
    lines = [f"# {title}\n"]

    lines.append(f"**Файлов:** {len(files)}\n")
    lines.append("## Содержание\n")

    for f in files:
        desc = first_description(f)
        rel = f.name
        lines.append(f"- [{rel}]({rel}) — {desc}")

    # Подпапки
    subdirs = sorted(d for d in folder.iterdir() if d.is_dir())
    if subdirs:
        lines.append("\n## Подразделы\n")
        for d in subdirs:
            sub_title = FOLDER_TITLES.get(d.name, d.name)
            lines.append(f"- [{d.name}/]({d.name}/) — {sub_title}")

    readme = folder / "README.md"
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  README: {readme.relative_to(ROOT)}")


def main():
    print("Генерация README для всех папок...")
    for folder in sorted(DOCS.rglob("*")):
        if folder.is_dir():
            make_readme(folder)
    make_readme(DOCS)  # корневой docs/README.md


if __name__ == "__main__":
    main()
