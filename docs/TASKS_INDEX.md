# Каталог задач (TASKS_INDEX)

_Обновлено: 2026-04-29_

**Всего задач:** 5


Этот файл автогенерируется из `tasks/*.task.yaml`. Не редактируйте вручную.


## По MCP-серверу


### lorenzo-contacts (1)

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `write-contact` | Помогает написать первое сообщение автору OSS-проекта | "напиши письмо автору", "составь запрос на коллаборацию" | contact-outreach | write_contact |

### lorenzo-graph (2)

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сейчас с базой знаний" | — | audit_corpus |
| `find-contradictions` | Поиск противоречий между документами | "где противоречия про", "что в моих документах конфликтует" | — | find_contradictions |

### lorenzo-runner (2)

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `generate-rfc` | Создание RFC-документа по теме с подтягиванием контекста из корпуса | "напиши RFC по", "оформи спецификацию для" | rfc | generate_rfc |
| `weekly-review` | Еженедельное ревью с дайджестом, аудитом, ретро и KPI snapshot | "weekly review", "пятничный обход" | — | weekly_review |

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

