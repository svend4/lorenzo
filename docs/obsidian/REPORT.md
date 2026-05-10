---
title: "Executive Report: Репозиторий Lorenzo"
tags:
  - ingestion
  - architecture
  - roadmap
  - anthropic
  - collaboration
  - general
date: 2026-05-10
---

# Executive Report: Репозиторий Lorenzo

<!-- toc-auto -->

<!-- summary -->
> Executive Report: сводный отчёт о состоянии репозитория Lorenzo — метрики, прогресс, ключевые выводы.

_Дата генерации: 2026-05-10_

---
<!-- tags: ingestion, architecture, roadmap, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.



## Общая картина

Монорепозиторий **Lorenzo** содержит исследовательскую базу знаний по экосистеме AI-проектов вокруг **Svyazi 2.0**.

| Показатель | Значение |
|------------|---------|
| Всего документов | **1742** |
| Всего слов | **1,823,076** |
| Скриптов обработки | **159** |
| Индекс здоровья | **80/100** |
| Проектов в сети | **22** |
| Связей проектов | **190** |
| Кластеров документов | **120** |
| Ошибок валидации | **0** |
| Предупреждений | **49** |

## Структура репозитория

| Раздел | Файлов | Описание |
|--------|--------|---------|
| `01-svyazi` | 16 | Архитектура Svyazi 2.0 |
| `02-anthropic-vacancies` | 357 | 436 вакансий Anthropic |
| `03-technology-combinations` | 7 | 40+ комбинаций технологий |
| `04-ai-collaborations` | 17 | AI-ансамбли OSS-проектов |
| `05-habr-projects` | 10 | Хабр-проекты: память, граф |

## Извлечённые знания

- **624** ключевых решений → [[DECISIONS|DECISIONS.md]]
- **2845** числовых KPI → [[KPI|KPI.md]]
- **484** открытых вопросов → [[QUESTIONS|QUESTIONS.md]]
- **937** похожих пар документов → [[SIMILAR|SIMILAR.md]]

## Топ навигационных документов

| Документ | Назначение |
|----------|------------|
| [[READING_ORDER|READING_ORDER.md]] | С чего начать читать |
| [[SITEMAP|SITEMAP.md]] | Карта всех разделов |
| [[NARRATIVE|NARRATIVE.md]] | История проекта |
| [[DECISIONS|DECISIONS.md]] | Ключевые решения |
| [[CONTACTS|CONTACTS.md]] | С кем связаться |
| [[HEALTH|HEALTH.md]] | Состояние репо |
| [[VALIDATION|VALIDATION.md]] | Проверка структуры |

## Рекомендуемые следующие шаги

2. ⚠️ Устранить **49 предупреждений** → [[VALIDATION|VALIDATION.md]]
3. 🤝 Связаться с авторами компонентов → [[CONTACTS|CONTACTS.md]]
4. 📋 Проработать открытые вопросы → [[QUESTIONS|QUESTIONS.md]]
5. 🚀 Запустить MVP-прототип → 01-[[07-mvp-planning|svyazi/07-mvp-planning.md]]
6. 🔗 Устранить сломанные ссылки → [[BROKEN_LINKS|BROKEN_LINKS.md]]

## Аналитические инструменты

В репозитории **159 скриптов** для работы с документами:

```bash
python scripts/improve_health.py      # обновить дашборд здоровья
python scripts/improve_validate.py    # проверить структуру
python scripts/improve_compare.py     # сравнить с предыдущим коммитом
python scripts/improve_report.py      # этот отчёт
```

---

_Отчёт сгенерирован автоматически · 2026-05-10_

<!-- backlinks -->

---

**Кто ссылается на этот документ (3):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)

