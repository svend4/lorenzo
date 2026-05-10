# Каталог задач (TASKS_INDEX)

<!-- toc -->
## Содержание

- [По MCP-серверу](#по-mcp-серверу)
  - [lorenzo-contacts (1)](#lorenzo-contacts-1)
  - [lorenzo-graph (4)](#lorenzo-graph-4)
  - [lorenzo-runner (5)](#lorenzo-runner-5)
  - [lorenzo-search (3)](#lorenzo-search-3)
- [Подробно](#подробно)
  - [`audit-corpus`](#audit-corpus)
  - [`compare`](#compare)
  - [`daily-routine`](#daily-routine)
  - [`find-contradictions`](#find-contradictions)
  - [`find-gaps`](#find-gaps)
  - [`generate-rfc`](#generate-rfc)
  - [`plan-mvp`](#plan-mvp)
  - [`search`](#search)
  - [`summarize`](#summarize)
  - [`synthesize`](#synthesize)
  - [`track-decisions`](#track-decisions)
  - [`weekly-review`](#weekly-review)
  - [`write-contact`](#write-contact)

---

<!-- tags: architecture, roadmap, self-improvement, collaboration -->


_Обновлено: 2026-04-29_

**Всего задач:** 13


Этот файл автогенерируется из `tasks/*.task.yaml`. Не редактируйте вручную.


## По MCP-серверу


### lorenzo-contacts (1)

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `write-contact` | Помогает написать первое сообщение автору OSS-проекта | "напиши письмо автору", "составь запрос на коллаборацию" | contact-outreach | write_contact |

### lorenzo-graph (4)

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сейчас с базой знаний" | — | audit_corpus |
| `find-contradictions` | Поиск противоречий между документами | "где противоречия про", "что в моих документах конфликтует" | — | find_contradictions |
| `find-gaps` | Поиск пробелов в базе знаний | "чего не хватает", "какие темы упомянуты но без документа" | — | find_gaps |
| `track-decisions` | Отслеживание ADR по теме / в хронологии | "какие решения по", "история решений" | — | get_decisions |

### lorenzo-runner (5)

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `compare` | Сравнение двух документов / разделов / подходов | "сравни", "в чём разница" | — | compare |
| `daily-routine` | Ежедневная процедура аудита и проверки изменений | "ежедневный обход", "что важного за день" | — | daily_routine |
| `generate-rfc` | Создание RFC-документа по теме с подтягиванием контекста из корпуса | "напиши RFC по", "оформи спецификацию для" | rfc | generate_rfc |
| `plan-mvp` | Планирование MVP/прототипа из имеющихся компонентов | "составь план MVP", "что нужно для прототипа" | prototype-mvp | plan_mvp |
| `weekly-review` | Еженедельное ревью с дайджестом, аудитом, ретро и KPI snapshot | "weekly review", "пятничный обход" | — | weekly_review |

### lorenzo-search (3)

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `search` | Полнотекстовый поиск по корпусу | "найди про", "что есть о" | — | search_docs |
| `summarize` | Резюмирование документа, раздела или подборки по теме | "кратко расскажи", "сделай резюме" | — | summarize |
| `synthesize` | Синтез единой картины по теме из многих документов | "сделай синтез", "собери всё про" | research-note | synthesize |

## Подробно


### `audit-corpus`

**Описание:** Сводный аудит состояния всего монорепо

**Триггеры:**
- "оцени состояние репо"
- "что сейчас с базой знаний"
- "покажи health check"
- "регулярный аудит"

**MCP:** lorenzo-graph → `audit_corpus`

**Связанные скилы:** audit-corpus, find-contradictions, find-gaps, weekly-review
**Связанные шаблоны:** kpi-snapshot


### `compare`

**Описание:** Сравнение двух документов / разделов / подходов

**Триггеры:**
- "сравни"
- "в чём разница"
- "что общего"
- "какой подход лучше"

**Inputs:**
- `a`: string (required) — 
- `b`: string (required) — 

**MCP:** lorenzo-runner → `compare`

**Связанные скилы:** compare, search, summarize


### `daily-routine`

**Описание:** Ежедневная процедура аудита и проверки изменений

**Триггеры:**
- "ежедневный обход"
- "что важного за день"
- "daily routine"

**MCP:** lorenzo-runner → `daily_routine`

**Связанные скилы:** daily-routine, audit-corpus, find-contradictions, find-gaps, status


### `find-contradictions`

**Описание:** Поиск противоречий между документами

**Триггеры:**
- "где противоречия про"
- "что в моих документах конфликтует"
- "проверь нет ли несостыковок"

**Inputs:**
- `topic`: string — Опционально — тема для фильтрации

**MCP:** lorenzo-graph → `find_contradictions`

**Связанные скилы:** find-contradictions, audit-corpus
**Связанные шаблоны:** contradiction-record


### `find-gaps`

**Описание:** Поиск пробелов в базе знаний

**Триггеры:**
- "чего не хватает"
- "какие темы упомянуты но без документа"
- "где пробелы"

**Inputs:**
- `topic`: string — 

**MCP:** lorenzo-graph → `find_gaps`

**Связанные скилы:** find-gaps, audit-corpus, synthesize
**Связанные шаблоны:** glossary-entry, project-component, rfc, decision-record


### `generate-rfc`

**Описание:** Создание RFC-документа по теме с подтягиванием контекста из корпуса

**Триггеры:**
- "напиши RFC по"
- "оформи спецификацию для"
- "формализуй идею в RFC"

**Inputs:**
- `topic`: string (required) — Тема RFC одной строкой
- `rfc_id`: string — ID вида RFC-NNNN (если не указан — присваивается автоматически)

**MCP:** lorenzo-runner → `generate_rfc`

**Шаблон:** [`rfc`](templates/rfc.md)

**Связанные скилы:** generate-rfc, search, synthesize
**Связанные шаблоны:** rfc, decision-record, protocol-spec


### `plan-mvp`

**Описание:** Планирование MVP/прототипа из имеющихся компонентов

**Триггеры:**
- "составь план MVP"
- "что нужно для прототипа"
- "минимальный пайплайн"

**Inputs:**
- `goal`: string (required) — 
- `layers`: array — 

**MCP:** lorenzo-runner → `plan_mvp`

**Шаблон:** [`prototype-mvp`](templates/prototype-mvp.md)

**Связанные скилы:** plan-mvp, design-ensemble, evaluate-tech
**Связанные шаблоны:** prototype-mvp, ensemble, mega-stack


### `search`

**Описание:** Полнотекстовый поиск по корпусу

**Триггеры:**
- "найди про"
- "что есть о"
- "где упоминается"
- "поиск по теме"

**Inputs:**
- `query`: string (required) — 

**MCP:** lorenzo-search → `search_docs`

**Связанные скилы:** search, summarize, compare


### `summarize`

**Описание:** Резюмирование документа, раздела или подборки по теме

**Триггеры:**
- "кратко расскажи"
- "сделай резюме"
- "что в двух словах"
- "TL;DR"

**Inputs:**
- `target`: string (required) — Файл, раздел или тема
- `level`: string — tldr | brief | detailed

**MCP:** lorenzo-search → `summarize`

**Связанные скилы:** summarize, search, synthesize


### `synthesize`

**Описание:** Синтез единой картины по теме из многих документов

**Триггеры:**
- "сделай синтез"
- "собери всё про"
- "что мы знаем о"

**Inputs:**
- `topic`: string (required) — 

**MCP:** lorenzo-search → `synthesize`

**Шаблон:** [`research-note`](templates/research-note.md)

**Связанные скилы:** synthesize, search, summarize, compare, find-gaps, find-contradictions
**Связанные шаблоны:** research-note


### `track-decisions`

**Описание:** Отслеживание ADR по теме / в хронологии

**Триггеры:**
- "какие решения по"
- "история решений"
- "почему мы выбрали"

**Inputs:**
- `topic`: string (required) — 

**MCP:** lorenzo-graph → `get_decisions`

**Связанные скилы:** track-decisions, audit-corpus, find-contradictions
**Связанные шаблоны:** decision-record


### `weekly-review`

**Описание:** Еженедельное ревью с дайджестом, аудитом, ретро и KPI snapshot

**Триггеры:**
- "weekly review"
- "пятничный обход"
- "еженедельный отчёт"

**MCP:** lorenzo-runner → `weekly_review`

**Связанные скилы:** weekly-review, audit-corpus, daily-routine, track-decisions
**Связанные шаблоны:** weekly-digest, kpi-snapshot, retrospective


### `write-contact`

**Описание:** Помогает написать первое сообщение автору OSS-проекта

**Триггеры:**
- "напиши письмо автору"
- "составь запрос на коллаборацию"
- "подготовь сообщение для"
- "мне нужно написать"

**Inputs:**
- `author`: string (required) — Имя или slug автора (kksudo, spbmolot)
- `project`: string — Конкретный проект автора если несколько

**MCP:** lorenzo-contacts → `write_contact`

**Шаблон:** [`contact-outreach`](templates/contact-outreach.md)

**Связанные скилы:** write-contact, propose-collaboration, status
**Связанные шаблоны:** contact-outreach

