# REGISTRY — реестр артефактов Lorenzo

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> python scripts/improve_template_init.py --type rfc --slug docs/rfcs/RFC-NNNN.md
**Проекты:** Svyazi

---

<!-- toc -->
## Содержание

- [Сводка](#сводка)
- [Скрипты по группам](#скрипты-по-группам)
- [Шаблоны](#шаблоны)
- [Скилы](#скилы)
- [MCP-серверы](#mcp-серверы)
- [Манифесты задач](#манифесты-задач)
- [Контакты](#контакты)
- [Полезные команды](#полезные-команды)

---

<!-- tags: knowledge, ingestion, architecture, roadmap, self-improvement, collaboration -->




_Обновлено: 2026-04-29_

## Сводка

| Слой | Кол-во |
|------|--------|
| Скрипты `improve_*.py` | 152 |
| Шаблоны `docs/templates/*.md` | 22 |
| Скилы `.claude/skills/*.md` | 28 |
| MCP-серверы | 10 |
| Манифесты задач | 13 |
| Контакты | 14 |

## Скрипты по группам

| Группа | Скриптов |
|--------|----------|
| `analysis` | 9 |
| `analytics` | 6 |
| `cicd` | 4 |
| `content` | 4 |
| `deeptext` | 10 |
| `export` | 7 |
| `extract` | 9 |
| `generate` | 7 |
| `graph` | 4 |
| `index` | 6 |
| `nlpplus` | 10 |
| `quality` | 10 |
| `reports` | 19 |
| `structure` | 6 |
| `textwork` | 8 |
| `без группы` | 33 |

## Шаблоны

| Шаблон | Описание | Обязательных секций |
|--------|----------|---------------------|
| [`agent-spec`](templates/agent-spec.md) | Спецификация AI-агента: тип, принципал, скилы, tools, память, decision boundary | 7 |
| [`contact-outreach`](templates/contact-outreach.md) | Контактный файл автора OSS-проекта: профиль, статус связи, первое сообщение | 3 |
| [`contradiction-record`](templates/contradiction-record.md) | Запись о противоречии между двумя источниками | 5 |
| [`decision-record`](templates/decision-record.md) | Architecture Decision Record (ADR): контекст → варианты → решение → последствия | 5 |
| [`ensemble`](templates/ensemble.md) | Описание ансамбля компонентов: задача, состав, контракт, риски, MVP | 5 |
| [`experiment-log`](templates/experiment-log.md) | Журнал эксперимента: гипотеза, метод, журнал, результат, выводы | 6 |
| [`faq-entry`](templates/faq-entry.md) | FAQ-запись: вопрос, краткий и подробный ответ | 3 |
| [`glossary-entry`](templates/glossary-entry.md) | Глоссарная статья: определение, происхождение, синонимы, примеры | 3 |
| [`kpi-snapshot`](templates/kpi-snapshot.md) | Снапшот KPI с деталями метрик и трендом | 4 |
| [`legal-case`](templates/legal-case.md) | Юридический кейс: Aktenzeichen, стороны, хронология, нормы, прецеденты | 5 |
| [`meeting-notes`](templates/meeting-notes.md) | Протокол встречи: повестка, обсуждение, решения, action items | 6 |
| [`mega-stack`](templates/mega-stack.md) | Полный технологический стек для класса задач со всеми слоями | 5 |
| [`project-component`](templates/project-component.md) | Карточка компонента: что это, особенности, статус, интеграция с экосистемой | 3 |
| [`protocol-spec`](templates/protocol-spec.md) | Спецификация протокола в стиле IETF / Nautilus NPP | 5 |
| [`prototype-mvp`](templates/prototype-mvp.md) | План MVP с фазами, метриками успеха, рисками | 6 |
| [`research-note`](templates/research-note.md) | Свободная заметка-исследование: контекст, находки, источники, открытые вопросы | 5 |
| [`retrospective`](templates/retrospective.md) | Ретроспектива: что хорошо, что плохо, action items | 2 |
| [`rfc`](templates/rfc.md) | Request for Comments — формальная спецификация в стиле IETF/Nautilus NPP | 5 |
| [`risk-entry`](templates/risk-entry.md) | Запись риска: вероятность, влияние, митигация | 4 |
| [`tech-pair`](templates/tech-pair.md) | Пара технологий с описанием синергии | 5 |
| [`tech-radar-entry`](templates/tech-radar-entry.md) | Запись Tech Radar: квадрант, кольцо, обоснование | 5 |
| [`weekly-digest`](templates/weekly-digest.md) | Еженедельный дайджест: TL;DR, что сделано, метрики, решения, план | 4 |

## Скилы

| Скилл | Назначение |
|-------|------------|
| [`analyze-project`](../.claude/skills/analyze-project.md) | Анализирует конкретный проект из базы знаний Lorenzo. |
| [`audit-corpus`](../.claude/skills/audit-corpus.md) | Сводный аудит состояния всего монорепо: метрики, противоречия, пробелы. |
| [`compare`](../.claude/skills/compare.md) | Сравнение двух или нескольких документов / разделов / подходов. |
| [`daily-routine`](../.claude/skills/daily-routine.md) | Ежедневная процедура: аудит → противоречия → пробелы → отчёт. |
| [`design-ensemble`](../.claude/skills/design-ensemble.md) | Дизайн ансамбля компонентов под конкретную задачу Svyazi 2.0. |
| [`dispatch`](../.claude/skills/dispatch.md) | Запуск нескольких скилов параллельно или последовательно с агрегацией результата. |
| [`evaluate-skill`](../.claude/skills/evaluate-skill.md) | Мета-скилл: оценить, насколько применённый скилл решил задачу пользователя. |
| [`evaluate-tech`](../.claude/skills/evaluate-tech.md) | Оценка одной технологии для использования в Svyazi 2.0 / Lorenzo. |
| [`find-cinderella`](../.claude/skills/find-cinderella.md) | Поиск «Cinderella Syndrome» — ценные проекты/идеи без видимости. |
| [`find-contradictions`](../.claude/skills/find-contradictions.md) | Поиск противоречий между документами по теме или в целом. |
| [`find-gaps`](../.claude/skills/find-gaps.md) | Поиск пробелов в базе знаний: упомянутых, но не описанных тем. |
| [`generate-rfc`](../.claude/skills/generate-rfc.md) | Создание RFC-документа по теме с подтягиванием контекста из корпуса. |
| [`improve`](../.claude/skills/improve.md) | Универсальный навык улучшения любого элемента Lorenzo: документа, контакта, |
| [`new-research`](../.claude/skills/new-research.md) | Старт нового исследования по теме. |
| [`outreach-day`](../.claude/skills/outreach-day.md) | «День аутрича» — связаться с N приоритетными контактами. |
| [`plan-mvp`](../.claude/skills/plan-mvp.md) | Планирование MVP/прототипа из имеющихся компонентов и решений. |
| [`propose-collaboration`](../.claude/skills/propose-collaboration.md) | Предложение, к кому обратиться по теме / для конкретной задачи. |
| [`propose-mega-stack`](../.claude/skills/propose-mega-stack.md) | Предложение «мега-стека» — полного технологического стека для класса задач. |
| [`review-architecture`](../.claude/skills/review-architecture.md) | Архитектурное ревью документа / раздела / системы. |
| [`review-docs`](../.claude/skills/review-docs.md) | Рецензирует документ или раздел базы знаний Lorenzo. |
| [`search`](../.claude/skills/search.md) | Полнотекстовый поиск по базе знаний Lorenzo. |
| [`skill-router`](../.claude/skills/skill-router.md) | Мета-скилл: выбирает подходящий специализированный скилл по запросу пользователя. |
| [`status`](../.claude/skills/status.md) | Быстрая сводка текущего состояния проекта Lorenzo без чтения множества файлов. |
| [`summarize`](../.claude/skills/summarize.md) | Резюмирование документа, раздела или подборки документов по теме. |
| [`synthesize`](../.claude/skills/synthesize.md) | Синтез единой картины по теме из многих документов. |
| [`track-decisions`](../.claude/skills/track-decisions.md) | Отслеживание архитектурных решений (ADR) по теме / в хронологии. |
| [`weekly-review`](../.claude/skills/weekly-review.md) | Еженедельное ревью: дайджест + аудит + ретро + план. |
| [`write-contact`](../.claude/skills/write-contact.md) | Помогает написать первое сообщение автору проекта. |

## MCP-серверы

| Сервер | Описание |
|--------|----------|
| `lorenzo-contacts` | Контакты: get_contact, list_contacts, update_contact_status, propose_outreach |
| `lorenzo-docs` | [Legacy] Монолитный сервер для обратной совместимости |
| `lorenzo-export` | Экспорт: Obsidian, Confluence, EPUB, RSS, CSV, HTML, Report |
| `lorenzo-graph` | Аналитика: get_health, get_decisions, get_concept_graph, kpi_history, get_project_status |
| `lorenzo-llm` | LLM с кэшем: llm_summary, llm_qa, llm_enrich, llm_contact |
| `lorenzo-runner` | Запуск improve_*.py: list_scripts, describe_script, run_improve, run_group |
| `lorenzo-search` | Read-only поиск: search_docs, bm25_passages, find_similar, faceted_search |
| `lorenzo-skills` | Скилы: list_skills, get_skill, match_skill (router), compose_skills, evaluate_skill |
| `lorenzo-templates` | Шаблоны и манифесты: list_templates, init_doc, validate_doc, list_tasks, show_task |
| `lorenzo-watch` | Мониторинг: recent_changes, pending_actions, watch_status, trigger_recompute |

## Манифесты задач

| ID | Описание | MCP сервер | MCP tool | Шаблон |
|----|----------|------------|----------|--------|
| `audit-corpus` | Сводный аудит состояния всего монорепо | `lorenzo-graph` | `audit_corpus` | `—` |
| `compare` | Сравнение двух документов / разделов / подходов | `lorenzo-runner` | `compare` | `—` |
| `daily-routine` | Ежедневная процедура аудита и проверки изменений | `lorenzo-runner` | `daily_routine` | `—` |
| `find-contradictions` | Поиск противоречий между документами | `lorenzo-graph` | `find_contradictions` | `—` |
| `find-gaps` | Поиск пробелов в базе знаний | `lorenzo-graph` | `find_gaps` | `—` |
| `generate-rfc` | Создание RFC-документа по теме с подтягиванием контекста из  | `lorenzo-runner` | `generate_rfc` | `rfc` |
| `plan-mvp` | Планирование MVP/прототипа из имеющихся компонентов | `lorenzo-runner` | `plan_mvp` | `prototype-mvp` |
| `search` | Полнотекстовый поиск по корпусу | `lorenzo-search` | `search_docs` | `—` |
| `summarize` | Резюмирование документа, раздела или подборки по теме | `lorenzo-search` | `summarize` | `—` |
| `synthesize` | Синтез единой картины по теме из многих документов | `lorenzo-search` | `synthesize` | `research-note` |
| `track-decisions` | Отслеживание ADR по теме / в хронологии | `lorenzo-graph` | `get_decisions` | `—` |
| `weekly-review` | Еженедельное ревью с дайджестом, аудитом, ретро и KPI snapsh | `lorenzo-runner` | `weekly_review` | `—` |
| `write-contact` | Помогает написать первое сообщение автору OSS-проекта | `lorenzo-contacts` | `write_contact` | `contact-outreach` |

## Контакты

| Slug | Автор | Статус |
|------|-------|--------|
| `anastasiyaw` | AnastasiyaW | not_started |
| `andrey-chuyan` | andrey_chuyan | not_started |
| `antipozitive` | Antipozitive | not_started |
| `cutcode` | Cutcode | not_started |
| `dmitriila` | Dmitriila | not_started |
| `kksudo` | kksudo | studied |
| `mixaill76` | MiXaiLL76 | not_started |
| `nlaik` | nlaik | not_started |
| `sonia-black` | Sonia_Black | not_started |
| `spbmolot` | spbmolot | studied |
| `tagir-analyzes` | tagir_analyzes | not_started |
| `vitalyoborin` | VitalyOborin | not_started |
| `vladspace` | VladSpace | not_started |
| `zodigancode` | zodigancode | not_started |

## Полезные команды

```bash
# Создать документ из шаблона
python scripts/improve_template_init.py --type rfc --slug docs/rfcs/RFC-NNNN.md

# Валидация
python scripts/improve_validate_templates.py --report

# Запуск пайплайна задачи
python scripts/improve_workflow_run.py --task audit-corpus

# Каталог скриптов
python scripts/improve_scripts_catalog.py

# Генерация скилов из манифестов
python scripts/improve_task_codegen.py

# Реестр артефактов (этот файл)
python scripts/improve_registry.py
```

<!-- see-also -->

---

**Смотрите также:**
- [TASKS_INDEX](docs/TASKS_INDEX.md)
- [PROGRESS](docs/PROGRESS.md)
- [GITHUB_ISSUES](docs/GITHUB_ISSUES.md)
- [EMPTY_SECTIONS](docs/EMPTY_SECTIONS.md)

