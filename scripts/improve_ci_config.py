"""
improve_ci_config.py — генерирует GitHub Actions workflow для docs.

Создаёт:
  .github/workflows/docs.yml       — основной CI для docs
  .github/workflows/docs_check.yml — быстрая проверка при PR

Запуск:
    python scripts/improve_ci_config.py
    python scripts/improve_ci_config.py --dry-run    # показать без записи
    python scripts/improve_ci_config.py --minimal    # только базовые проверки
"""
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
GH_DIR = ROOT / ".github" / "workflows"
TODAY = date.today().isoformat()

DRY_RUN = "--dry-run" in sys.argv
MINIMAL = "--minimal" in sys.argv

DOCS_YML = """\
# Автоматически создан improve_ci_config.py
# Обновляет метрики и индексы после push в main/master
name: docs-update

on:
  push:
    branches: [main, master]
    paths:
      - 'docs/**'
      - 'scripts/**'
  workflow_dispatch:

jobs:
  update-docs:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # нужен для git log в staleness/rss

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements*.txt') }}

      - name: Install dependencies
        run: |
          pip install --quiet anthropic || true

      - name: Run fast scripts
        run: python scripts/improve_run_all.py --fast --group reports

      - name: Update search index
        run: python scripts/improve_search_index.py

      - name: Generate RSS feed
        run: python scripts/improve_rss.py

      - name: Commit updated docs
        run: |
          git config user.name  "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/
          git diff --staged --quiet || git commit -m "docs: auto-update metrics [skip ci]"
          git push
"""

DOCS_CHECK_YML = """\
# Автоматически создан improve_ci_config.py
# Быстрая проверка docs при PR
name: docs-check

on:
  pull_request:
    paths:
      - 'docs/**'
      - 'scripts/**'

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Check broken links (internal)
        run: python scripts/improve_broken_links.py

      - name: Check spellcheck
        run: python scripts/improve_spellcheck.py

      - name: Check readability
        run: python scripts/improve_readability_v2.py

      - name: Verify search index up to date
        run: python scripts/improve_search_index.py

      - name: Check for regressions
        run: |
          # Убеждаемся, что METRICS.md существует
          test -f docs/METRICS.md || (echo "❌ docs/METRICS.md missing" && exit 1)
          # Убеждаемся, что search_index.json существует
          test -f docs/search_index.json || (echo "❌ search_index.json missing" && exit 1)
          echo "✅ Core docs present"
"""

MINIMAL_YML = """\
# Минимальный workflow — только проверка при PR
name: docs-check-minimal

on:
  pull_request:
    paths: ['docs/**']

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Broken links
        run: python scripts/improve_broken_links.py
      - name: Spellcheck
        run: python scripts/improve_spellcheck.py
"""


def main() -> None:
    print("⚙️  improve_ci_config.py — генерация GitHub Actions")
    if DRY_RUN:
        print("   Режим: dry-run\n")
        if MINIMAL:
            print("=== .github/workflows/docs_check_minimal.yml ===")
            print(MINIMAL_YML)
        else:
            print("=== .github/workflows/docs.yml ===")
            print(DOCS_YML)
            print("=== .github/workflows/docs_check.yml ===")
            print(DOCS_CHECK_YML)
        return

    GH_DIR.mkdir(parents=True, exist_ok=True)

    if MINIMAL:
        out = GH_DIR / "docs_check_minimal.yml"
        out.write_text(MINIMAL_YML, encoding="utf-8")
        print(f"  wrote: {out.relative_to(ROOT)}")
    else:
        out1 = GH_DIR / "docs.yml"
        out2 = GH_DIR / "docs_check.yml"
        out1.write_text(DOCS_YML, encoding="utf-8")
        out2.write_text(DOCS_CHECK_YML, encoding="utf-8")
        print(f"  wrote: {out1.relative_to(ROOT)}")
        print(f"  wrote: {out2.relative_to(ROOT)}")

    print("\n  Добавьте в репозиторий:")
    print("  git add .github/workflows/ && git commit -m 'ci: add docs workflows'")
    print("\n  Требуются секреты в GitHub:")
    print("  - ANTHROPIC_API_KEY (для LLM-скриптов, опционально)")


if __name__ == "__main__":
    main()
