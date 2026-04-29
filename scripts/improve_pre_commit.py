"""
improve_pre_commit.py — генерирует .pre-commit-config.yaml для проекта.

Хуки включают:
  - trailing whitespace, end-of-file fixes
  - проверка YAML/JSON синтаксиса
  - проверка орфографии (improve_spellcheck.py)
  - проверка сломанных ссылок (improve_broken_links.py)
  - проверка читаемости (improve_readability_v2.py)
  - обновление поискового индекса

Запуск:
    python scripts/improve_pre_commit.py
    python scripts/improve_pre_commit.py --dry-run
    python scripts/improve_pre_commit.py --install  # pip install pre-commit && pre-commit install
"""
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
TODAY = date.today().isoformat()

DRY_RUN = "--dry-run" in sys.argv
INSTALL  = "--install"  in sys.argv

PRE_COMMIT_CONFIG = """\
# Автоматически создан improve_pre_commit.py
# Запуск: pre-commit run --all-files
# Установка: pip install pre-commit && pre-commit install
repos:
  # Стандартные хуки
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
        types: [markdown]
      - id: end-of-file-fixer
        types: [markdown]
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: mixed-line-ending
        args: [--fix=lf]

  # Локальные проверки
  - repo: local
    hooks:
      - id: spellcheck
        name: Проверка орфографии
        entry: python scripts/improve_spellcheck.py
        language: system
        pass_filenames: false
        files: \\.md$
        stages: [pre-commit]

      - id: broken-links
        name: Проверка ссылок
        entry: python scripts/improve_broken_links.py
        language: system
        pass_filenames: false
        files: \\.md$
        stages: [pre-commit]

      - id: readability
        name: Индекс читаемости
        entry: python scripts/improve_readability_v2.py
        language: system
        pass_filenames: false
        files: \\.md$
        stages: [pre-commit]
        verbose: true

      - id: search-index
        name: Обновление поискового индекса
        entry: python scripts/improve_search_index.py
        language: system
        pass_filenames: false
        files: docs/.*\\.md$
        stages: [pre-commit]
"""

GITIGNORE_ADDITIONS = """
# pre-commit cache
.pre-commit-cache/
"""


def main() -> None:
    print("🪝 improve_pre_commit.py — настройка pre-commit хуков")
    if DRY_RUN:
        print("   Режим: dry-run\n")
        print(PRE_COMMIT_CONFIG)
        return

    out = ROOT / ".pre-commit-config.yaml"
    if out.exists():
        print(f"  ⚠️  {out.name} уже существует — перезаписываем")

    out.write_text(PRE_COMMIT_CONFIG, encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")

    # Добавляем в .gitignore если нужно
    gitignore = ROOT / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8")
        if ".pre-commit-cache" not in content:
            gitignore.write_text(content + GITIGNORE_ADDITIONS, encoding="utf-8")
            print(f"  updated: .gitignore (добавлен .pre-commit-cache/)")

    if INSTALL:
        if not shutil.which("pre-commit"):
            print("\n  Устанавливаем pre-commit...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], check=False)

        if shutil.which("pre-commit"):
            print("\n  Устанавливаем хуки...")
            result = subprocess.run(["pre-commit", "install"], cwd=ROOT,
                                    capture_output=True, text=True)
            if result.returncode == 0:
                print("  ✅ pre-commit хуки установлены")
            else:
                print(f"  ❌ ошибка: {result.stderr[:100]}")
        else:
            print("  ❌ pre-commit не найден. pip install pre-commit")
    else:
        print("\n  Для установки хуков:")
        print("  pip install pre-commit && pre-commit install")
        print("  или: python scripts/improve_pre_commit.py --install")


if __name__ == "__main__":
    main()
