<!-- handcrafted -->
# Шаблоны документов

_Обновлено: 2026-04-29_

Типизированные заготовки для создания документов с YAML-frontmatter и
JSON-схемами для валидации. Каждый шаблон имеет соответствующую схему в
[`_schemas/`](_schemas/).

## Универсальные (T1) — 8

| Шаблон | Назначение |
|--------|------------|
| [research-note.md](research-note.md) | Свободная заметка-исследование |
| [decision-record.md](decision-record.md) | ADR (Architecture Decision Record) |
| [contact-outreach.md](contact-outreach.md) | Контакт с автором OSS-проекта |
| [project-component.md](project-component.md) | Карточка компонента |
| [ensemble.md](ensemble.md) | Ансамбль компонентов |
| [meeting-notes.md](meeting-notes.md) | Протокол встречи |
| [weekly-digest.md](weekly-digest.md) | Еженедельный дайджест |
| [experiment-log.md](experiment-log.md) | Журнал эксперимента |

## Частотные (T2) — 8

| Шаблон | Назначение |
|--------|------------|
| [rfc.md](rfc.md) | RFC в стиле IETF / Nautilus NPP |
| [kpi-snapshot.md](kpi-snapshot.md) | Снапшот KPI с трендом |
| [glossary-entry.md](glossary-entry.md) | Глоссарная статья |
| [retrospective.md](retrospective.md) | Ретроспектива спринта |
| [contradiction-record.md](contradiction-record.md) | Запись о противоречии |
| [risk-entry.md](risk-entry.md) | Запись риска |
| [tech-radar-entry.md](tech-radar-entry.md) | Tech Radar запись |
| [faq-entry.md](faq-entry.md) | FAQ-запись |

## Доменные (T3) — 6

| Шаблон | Назначение |
|--------|------------|
| [agent-spec.md](agent-spec.md) | Спецификация AI-агента |
| [protocol-spec.md](protocol-spec.md) | Спецификация протокола |
| [legal-case.md](legal-case.md) | Юридический кейс (Sozialgericht) |
| [mega-stack.md](mega-stack.md) | Полный технологический стек |
| [tech-pair.md](tech-pair.md) | Пара технологий с синергией |
| [prototype-mvp.md](prototype-mvp.md) | План MVP |

## Мета (T4)

| Шаблон | Назначение |
|--------|------------|
| [template-of-templates.md](template-of-templates.md) | Создание нового шаблона |

## Использование

### Создать документ из шаблона

```bash
python scripts/improve_template_init.py --type research-note \
  --slug docs/research/мой-файл.md \
  --vars title="Моё исследование" status=draft
```

### Список шаблонов с описаниями

```bash
python scripts/improve_template_init.py --list
```

### Валидация документов

```bash
# Все документы
python scripts/improve_validate_templates.py --report

# Один файл
python scripts/improve_validate_templates.py --file docs/contacts/kksudo.md

# Со строгим режимом (exit 1 при ошибках)
python scripts/improve_validate_templates.py --strict
```

### Миграция существующих документов

При изменении схемы:

```bash
python scripts/improve_template_migrate.py --template contact-outreach --dry-run
python scripts/improve_template_migrate.py --template contact-outreach --apply
python scripts/improve_template_migrate.py --all --dry-run
```

### Проверка целостности (бот не «загрязнил» шаблоны)

```bash
python scripts/improve_template_integrity.py            # отчёт
python scripts/improve_template_integrity.py --strict   # exit 1 при загрязнениях
python scripts/improve_template_integrity.py --fix      # автоисправление
```

## Структура шаблона

Каждый шаблон содержит:

1. **YAML-frontmatter** с обязательными полями (`template`, `version`, ...)
2. **Заголовок 1-го уровня** `# ...`
3. **HTML-комментарии** `<!-- summary: ... -->` `<!-- tags: ... -->`
4. **Required-секции** (`##`), указанные в JSON-схеме
5. **Подвал** с `<!-- see-also -->` и связанными документами

## Структура схемы

`_schemas/<template>.json` содержит:
- `properties` — типы полей frontmatter (с enum, pattern, format)
- `required` — обязательные поля frontmatter
- `required_sections` — обязательные секции в теле документа

## Защита от автоматических скриптов

Этот README помечен `<!-- handcrafted -->` в первой строке — `improve_readmes.py`
не будет его перегенерировать. Папки `docs/templates/` и `docs/templates/_schemas/`
включены в `.docignore` — `improve_summaries.py`, `improve_alerts.py` и другие
скрипты их не трогают.

## Связанные документы

- [VALIDATION.md](../VALIDATION.md) — отчёт валидации всего корпуса
- [TASKS_INDEX.md](../TASKS_INDEX.md) — каталог задач (для манифестов)
- [`scripts/improve_validate_templates.py`](../../scripts/improve_validate_templates.py)
- [`scripts/improve_template_init.py`](../../scripts/improve_template_init.py)
- [`scripts/improve_template_migrate.py`](../../scripts/improve_template_migrate.py)
- [`scripts/improve_template_integrity.py`](../../scripts/improve_template_integrity.py)
