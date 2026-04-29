# docs-toolkit

Универсальный набор инструментов для обработки markdown-монорепозиториев,
извлечённый из Lorenzo.

**Это первая стадия выноса** — на этом этапе пакет содержит:
- ядро с относительными путями (без хардкода `/home/user/lorenzo`);
- конфиг через `docstoolkit.toml`;
- стартовый набор универсальных инструментов;
- шаблоны (типизированные документы) и манифесты задач.

Не вынесено пока (домен-специфика):
- RU-словари орфографии;
- контактные шаблоны Habr-авторов;
- нумерация секций `01-svyazi/`.

## Что есть прямо сейчас

```
docs-toolkit/
├── README.md                           # этот файл
├── pyproject.toml                      # пакет + CLI
├── docstoolkit.toml.example            # пример конфига
├── docstoolkit/
│   ├── __init__.py
│   ├── config.py                       # загрузчик docstoolkit.toml
│   ├── core.py                         # ROOT/DOCS, write_doc, clean
│   ├── frontmatter.py                  # парсер YAML-frontmatter
│   ├── validate.py                     # валидация по JSON Schema
│   ├── init.py                         # создание из шаблона
│   └── cli.py                          # точка входа docstoolkit
└── examples/lorenzo-config/
    └── docstoolkit.toml                # конфиг как в этом репо
```

## Установка (после публикации)

```bash
pip install docs-toolkit
```

Сейчас (vendored, в этом репо):

```bash
cd docs-toolkit
pip install -e .
```

## Использование

```bash
# Создать docstoolkit.toml
docstoolkit init

# Создать документ из шаблона
docstoolkit doc new --type rfc --slug docs/rfcs/RFC-0001.md \
  --vars rfc_id=RFC-0001 title="My RFC"

# Валидация
docstoolkit doc validate --section docs/contacts

# Список доступных шаблонов
docstoolkit doc list-templates
```

## Конфиг (docstoolkit.toml)

```toml
[paths]
docs = "docs"
templates = "docs/templates"
schemas = "docs/templates/_schemas"

[validation]
strict = false
skip_dirs = ["templates", "_schemas", "node_modules"]

[language]
primary = "ru"
fallback = "en"

[sections]
"01-svyazi" = "Svyazi 2.0"
"05-habr-projects" = "Хабр-проекты"
```

## Roadmap

### Phase 1 (текущая) — vendored ядро
- ✅ `docstoolkit/` пакет с пустым `cli.py`
- ✅ Загрузчик конфига
- ✅ Валидатор шаблонов

### Phase 2 — extract & test
- [ ] Перенести `improve_validate_templates.py` → `docstoolkit/validate.py`
- [ ] Перенести `improve_template_init.py` → `docstoolkit/init.py`
- [ ] Перенести `improve_task_codegen.py` → `docstoolkit/codegen.py`
- [ ] Тесты с фикстурой `tests/fixtures/sample-repo/`

### Phase 3 — plugins
- [ ] Ингестия: PDF, EPUB, MHTML, HTML
- [ ] Языковые плагины: ru/en NLP
- [ ] Domain-плагины: legal, contacts, etc.

### Phase 4 — distribute
- [ ] PyPI публикация
- [ ] GitHub Action: `docstoolkit-action@v1`
- [ ] Docker image
- [ ] Документация на ReadTheDocs

## Связь с Lorenzo

В Lorenzo сейчас есть симлинки `docs-toolkit/docstoolkit` → внутреннее ядро.
После публикации в PyPI Lorenzo сможет:

```bash
pip install docs-toolkit
# и убрать собственные scripts/improve_validate_templates.py и т.п.
```

Связанные манифесты, шаблоны и скилы остаются специфичными для Lorenzo.
