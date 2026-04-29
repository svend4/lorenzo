# Установка и конфигурация

## Установка

### Базовая

```bash
pip install docs-toolkit
```

Без зависимостей. Работает: markdown, html, mhtml, jupyter ingest; TF-IDF поиск;
echo RAG; knowledge graph; jobs queue; web dashboard.

### С опциональными зависимостями

```bash
# Все extras
pip install docs-toolkit[all]

# Точечно
pip install docs-toolkit[mcp]      # MCP-серверы
pip install docs-toolkit[llm]      # Anthropic для RAG
pip install pypdf                  # PDF ingest
pip install ebooklib               # EPUB ingest
pip install python-docx            # DOCX ingest
pip install sentence-transformers  # semantic search
pip install openai                 # OpenAI RAG
pip install google-generativeai    # Gemini RAG
```

### Из исходников

```bash
git clone https://github.com/svend4/lorenzo.git
cd lorenzo/docs-toolkit
pip install -e .
```

### Docker

```bash
docker run --rm -v $(pwd):/work -w /work \
  ghcr.io/svend4/docs-toolkit:latest doc validate
```

### GitHub Action

```yaml
- uses: svend4/lorenzo/docs-toolkit@main
  with:
    command: validate
    fail-on-warnings: true
```

## Конфигурация

```bash
docstoolkit init
```

Создаст `docstoolkit.toml` в текущей директории:

```toml
[paths]
docs = "docs"
templates = "docs/templates"
schemas = "docs/templates/_schemas"
tasks = "tasks"
skills = ".claude/skills"

[validation]
strict = false
skip_dirs = ["templates", "_schemas", "node_modules", ".git"]

[language]
primary = "en"             # ru | en
fallback = "en"

[sections]
# Имена ваших разделов для красивых README
# "01-architecture" = "Архитектура"
```

## Проверка

```bash
docstoolkit doctor
```

Запускает 8 типов проверок:
1. Python ≥ 3.10
2. Конфиг найден и валиден
3. docs/ существует и доступен на запись
4. templates/ + _schemas/ согласованы
5. Ingest plugins загружаются
6. Опциональные зависимости (mcp, anthropic, pypdf, ebooklib, python-docx, pytest)

Exit codes: `0` = ok, `1` = есть warnings, `2` = есть errors.

## Структура репозитория для docs-toolkit

```
my-repo/
├── docstoolkit.toml         # конфиг
├── docs/                    # ваши документы
│   ├── templates/           # шаблоны
│   │   └── _schemas/        # JSON-схемы
│   └── ...
├── tasks/                   # манифесты задач (опц.)
└── .claude/skills/          # скилы (опц., для Claude Code)
```
