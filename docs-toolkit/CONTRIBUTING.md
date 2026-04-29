# Contributing to docs-toolkit

Спасибо за интерес! Это руководство покрывает workflow для contributors.

## Quick start

```bash
git clone https://github.com/svend4/lorenzo.git
cd lorenzo/docs-toolkit
pip install -e .[all]    # все опц. зависимости
python -m pytest tests/  # должно: passed
```

## Структура проекта

```
docs-toolkit/
├── docstoolkit/
│   ├── __init__.py          # public API
│   ├── config.py            # docstoolkit.toml
│   ├── core.py              # write_doc, clean_text
│   ├── frontmatter.py       # YAML parser
│   ├── cli.py               # main entry point
│   ├── doctor.py            # diagnostics
│   ├── serve.py             # web dashboard
│   ├── plugins.py           # entry_points discovery
│   ├── ingest/              # md/html/pdf/epub/docx/jupyter/mhtml
│   ├── embeddings/          # tfidf, sentence-transformers, hybrid, cache
│   ├── lang/                # detect, i18n, readability
│   ├── skills/              # testing framework
│   └── web/                 # url, arxiv, hn, habr
├── tests/                   # pytest
├── examples/                # example-plugin-pack
├── pyproject.toml
├── Dockerfile
├── action.yml               # GitHub Action
├── README.md
├── CHANGELOG.md
├── SECURITY.md
└── CONTRIBUTING.md          # этот файл
```

## Правила кода

### Python

- **Python 3.10+** (для `match` statement и `|` types)
- **Без зависимостей в core** (`docstoolkit/core.py`, `frontmatter.py`,
  `config.py`, `cli.py`). Опциональные deps только в специализированных модулях.
- **Type hints обязательны** для public API, опциональны для internal helpers.
- **Docstrings обязательны** для public функций (одна строка минимум).

### Тесты

- Каждый PR должен включать тесты (`tests/test_*.py`).
- Формат: `pytest`, без сложных fixtures.
- Mocking сети через `unittest.mock.patch`.
- Coverage целевой: ≥ 80% для нового кода.

```bash
python -m pytest tests/ -v --cov=docstoolkit
```

### Стиль

- Indent: 4 пробела
- Strings: double quotes
- Imports: stdlib → docstoolkit → third-party (через пустую строку)
- Line length: 100

## PR процесс

1. **Откройте issue** перед большим PR — обсудите подход.
2. **Branch name:** `feature/<short-name>` или `fix/<short-name>`.
3. **Commit messages:** Conventional Commits:
   - `feat:` новая функция
   - `fix:` багфикс
   - `docs:` документация
   - `test:` тесты
   - `refactor:` рефакторинг без изменения поведения
   - `perf:` производительность
   - `chore:` инфраструктура
4. **PR description:** что меняется, зачем, как тестировалось.
5. **Update CHANGELOG.md** в секции `## [Unreleased]`.
6. **Все CI checks должны проходить:** `unit-tests`, `mcp-smoke`,
   `validate-templates`, `python-syntax`.

## Добавление новых компонентов

### Новый ingest плагин

1. Создайте `docstoolkit/ingest/<format>.py` с функцией `ingest(path: Path) → Document`.
2. Зарегистрируйте в `dispatch.py:_autoload()`.
3. Добавьте тест в `tests/test_ingest.py`.
4. Обновите `Dockerfile` если нужны системные зависимости.

### Новый embeddings провайдер

1. Создайте `docstoolkit/embeddings/<name>.py` с классом наследником `EmbeddingProvider`.
2. Реализуйте `encode(texts) → list[vector]` и `similarity(query, docs) → list[float]`.
3. Регистрируйте в `dispatch.py:_REGISTRY` (для core) или через entry_points (для плагина).

### Новая команда CLI

1. Добавьте `cmd_<name>(args)` в `cli.py`.
2. Зарегистрируйте subparser в `main()`.
3. Smoke-test: `docstoolkit <name> --help`.

### Новый шаблон документа

1. Создайте `<example>/docs/templates/<template>.md` с YAML-frontmatter.
2. Создайте `<example>/docs/templates/_schemas/<template>.json` со схемой.
3. Добавьте тест: `python -m docstoolkit.cli doc validate`.

## Code of Conduct

Будьте уважительны. Технические дискуссии всегда о коде, не о людях.

## Лицензия

Контрибуция предполагает согласие с MIT лицензией проекта.
