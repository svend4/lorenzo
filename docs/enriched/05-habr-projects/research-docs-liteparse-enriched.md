---
date: 2026-06-05
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# research-docs + LiteParse


<!-- summary -->
> Раздел research-docs-liteparse-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `research-docs-liteparse-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Документ создан на основе исследования. Ссылки ведут на связанные материалы. Параметр | Значение | У -->
<!-- tags: liteparse, pdf, forensic, bounding-boxes, visual-citations, spatial-text, html-report, evidence, document-qa -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\05-habr-projects\knowledge\research-docs-liteparse.md -->

# research-docs + LiteParse

## Что это

Проект исследует интеграцию LiteParse для обработки PDF-документов с фокусом на форензическую аналитику и пространственный анализ текста. Решает задачу извлечения и визуализации структурированной информации из документов с сохранением пространственных координат и создания доказательственной базы.

## Ключевые особенности

- **Bounding-box анализ:** Определение и отслеживание точных координат элементов в документе для визуального цитирования
- **Форензическая QA:** Поддержка forensic-qa для надежного анализа документов с целью формирования доказательственной базы
- **HTML-отчеты:** Генерация структурированных HTML-отчетов с сохранением пространственной информации
- **Пространственное парсинг:** Анализ расположения и взаимосвязи текстовых элементов в контексте документа

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Язык/стек | — |
| Лицензия | Apache-2.0 |
| Зрелость | beta |
| Приоритет | 2 |
| Упоминаний в репо | 594 |

## Интеграция с Svyazi

Компонент работает на слое `ingestion/evidence`, обеспечивая форензическую обработку документов. Интегрируется с экосистемой Svyazi через AgentFS, knowledge-space и agent-memory-mcp для централизованного управления доказательственными материалами и метаданными.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [research-docs-liteparse](docs\05-habr-projects\knowledge\research-docs-liteparse.md)_


## Использование
```bash
# Запуск
python scripts/improve_research_docs_liteparse_enriched.py
```
