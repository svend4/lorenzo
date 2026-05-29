---
date: 2026-05-29
tags: [memory, rag, knowledge, ingestion, local-first]
state: normalized
---

# MemNet: исследовательская память


<!-- summary -->
> Раздел memnet-enriched формируется автоматически из данных репозитория. MemNet реализует концепцию «Memory Is All You Need» на уровне обучаемой архитектуры, решая проблему высокой стоимости консолидирующих LLM-вызовов.

> [!NOTE]
> Раздел `memnet-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: MemNet — «Memory Is All You Need» https://habr.com/ru/articles/983684/ Здесь автор делает то же само -->
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\05-habr-projects\memory\memnet.md -->

# MemNet: исследовательская память

## Что это

MemNet реализует концепцию «Memory Is All You Need» на уровне обучаемой архитектуры, решая проблему высокой стоимости консолидирующих LLM-вызовов. Проект использует гибридный RAG-пайплайн с собственными методами обработки для структурированных данных, где физическая обработка документов дешевле LLM-операций в четыре порядка величины.

## Ключевые особенности

- **Структурирование документов:** Docling отделяет заголовки от основного контента, pdfplumber предоставляет координаты для визуального выделения элементов
- **Гибридный поиск:** Комбинация FAISS и BM25 для эффективного поиска по векторному и текстовому индексам
- **Специализированная обработка:** Переписанные методы для работы с JSON-метаинформацией и HTML-таблицами

## Статус проекта

| Параметр | Значение |
|----------|----------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | https://habr.com/ru/articles/983684/ |
| Слой | memory |
| Контакт | [@Antipozitive](../../contacts/antipozitive.md) |

## Интеграция с Svyazi

MemNet работает на слое memory экосистемы, обеспечивая архитектурный подход к организации и поиску знаний. Проект связан с Yodoca (решает её проблему стоимости), CardIndex и гибридным RAG, формируя единую систему управления исследовательской памятью в рамках Svyazi 2.0.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [memnet](docs\05-habr-projects\memory\memnet.md)_


## Использование
```bash
# Запуск
python scripts/improve_memnet_enriched.py
```
