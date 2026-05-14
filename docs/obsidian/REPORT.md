---
title: "Svyazi 2.0 — Knowledge Base Report"
tags:
  - general
date: 2026-05-14
---

# Svyazi 2.0 — Knowledge Base Report

_Сгенерировано автоматически: 2026-05-14_

---

## Содержание

1. [Executive Summary](#executive-summary)
2. [Корпус документов](#корпус-документов)
3. [Ключевые проекты](#ключевые-проекты)
4. [Ключевые сущности](#ключевые-сущности)
5. [Архитектурные решения](#архитектурные-решения)
6. [Открытые вопросы](#открытые-вопросы)
7. [Рекомендуемое чтение](#рекомендуемое-чтение)

## Executive Summary

**Svyazi 2.0 — Knowledge Base Report** — аналитический обзор базы знаний, сгенерированный автоматически 2026-05-14.

База содержит **1306 документов** объёмом **1,515,189 слов** в **26 секциях**. Здоровье репозитория: **90/100**, средний балл документов: **97.9/100/100**, словарное богатство (STTR): **0.624**.

Цель базы знаний — поддержка разработки **Svyazi 2.0**, community intelligence platform, объединяющей лучшие OSS-проекты с Хабра в единую архитектуру Knowledge OS.

## Корпус документов

### Общая статистика

| Метрика | Значение |
|---------|----------|
| Документов | **1306** |
| Слов | **1,515,189** |
| Секций | **26** |
| Здоровье репо | **90/100** |
| Средний балл | **97.9/100/100** |
| Словарное богатство (STTR) | **0.624** |

### По секциям

| Секция | Файлов | Слов |
|--------|--------|------|
| **obsidian** | 1300 | 1,463,622 |
| **Anthropic Vacancies** | 357 | 355,535 |
| **nautilus** | 255 | 179,896 |
| **anthropic-vacancies** | 111 | 48,013 |
| **AI Collaborations** | 40 | 34,824 |
| **lorenzo-agent** | 62 | 29,064 |
| **svyazi-2-0** | 60 | 22,257 |
| **habr-unique-projects** | 56 | 20,596 |
| **technology-combinations** | 53 | 20,386 |
| **ROADMAP** | 7 | 18,232 |
| **processing-guide** | 13 | 18,013 |
| **Habr Projects** | 16 | 15,409 |
| **Svyazi 2.0** | 16 | 13,727 |
| **ai-collaborations** | 31 | 13,346 |
| **Templates** | 24 | 8,838 |
| **Contacts** | 32 | 8,431 |
| **Tech Combinations** | 7 | 4,050 |
| **letters** | 10 | 3,727 |
| **meta-scripting** | 7 | 3,604 |
| **autofilled** | 13 | 3,550 |
| **glossary** | 4 | 2,798 |
| **rfcs** | 5 | 1,899 |
| **badges** | 1 | 44 |

## Ключевые проекты

_Авторы и проекты из CONTACTS.md:_

| Автор | Проект | Слой | Приоритет |
|-------|--------|------|-----------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 126 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 78 | — |
| **Cutcode** | AIF Handoff | orchestration | 68 | — |
| **Dmitriila** | SENTINEL | security | 60 | — |
| **MiXaiLL76** | Auto AI Router | security | 56 | — |
| **Sonia_Black** | knowledge-space | knowledge | 38 | — |
| **VitalyOborin** | Yodoca | memory | 102 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 80 | — |

## Ключевые сущности

- 📦 **obsidian** (projects) — упомянут в 775 файлах
- 👤 **anthropic** (people) — упомянут в 736 файлах
- 📦 **nautilus** (projects) — упомянут в 542 файлах
- 📦 **lorenzo** (projects) — упомянут в 511 файлах
- 👤 **claude** (people) — упомянут в 458 файлах
- 📦 **svyazi** (projects) — упомянут в 391 файлах
- ⚙️ **mcp** (tech) — упомянут в 360 файлах
- 🏢 **вк** (orgs) — упомянут в 297 файлах
- ⚙️ **bm25** (tech) — упомянут в 259 файлах
- 📦 **github** (projects) — упомянут в 259 файлах

## Архитектурные решения

_Из DECISIONS.md:_

- **На Хабре пока не видно одного готового проекта, который уже собрал все слои в единое целое, но видно много авторов, ка
- путь — начать с минимального прототипа из пяти компонентов: 1. Svyazi‑подобный import/normalize/CardIndex 2. AgentFS‑под
- Svyazi + AgentFS + NGT/Yodoca + LiteParse: даёт уже полезный MVP 2. > 🏷️ **Ключевые слова:** `svyazi`, `проект`, `cardin
- кандидат для слоя `.agentos/` и compile‑to‑runtime политики. citeturn33view4turn27view0 | Комментарии к статье и Git
- слой — не память, не RAG[^rag] и не оркестр **Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[^agentfs], mcla
- слой — не память, не RAG и не оркестрация по отдельности: все они уже представлены на Хабре и в репозиториях. Дефицитный
- Svyazi + AgentFS + NGT^ngt/Yodoca + LiteParse: это даёт уже полезный MVP. > 🏷️ **Ключевые слова:** `summary`, `svyazi`, 
- **Svyazi‑2.0 нужно начинать не с “самой умной модели”, а с самой строгой структуры переходов между слоями**. Сильная мод

## Открытые вопросы

_Из QUESTIONS.md — вопросы, требующие решения:_

- **Интерфейс** — есть ли понятный публичный API/контракт для интеграции?
- **Доказуемость** — можно ли проверить, что слой работает правильно?
- ше задавать вопрос о memory write policy и conservative consolidation: *что в вашей архитектуре оказ
- о memory write policy и conservative consolidation: *что в вашей архитектуре оказалось критичнее для
- Вопрос: как вы оцениваете эту многоуровневую агентную архитектуру, где каждый член команды получает 
- как вы оцениваете эту многоуровневую агентную архитектуру, где каждый член команды получает персонал
- Как двойственная архитектура избегает этого?
- Как бы выглядел Слой B идеально?

## Рекомендуемое чтение

_Топ документов по насыщенности (из READING_LIST.md):_

| # | Документ | Секция | Время | Слов |
|---|----------|--------|-------|------|
| 1 | [[TABLES|Все таблицы репозитория]] | `TABLES.md` | 1426 мин | 334302 | — |
| 2 | [[OUTLINE|Outline базы знаний]] | `OUTLINE.md` | 183 мин | 40378 | — |
| 3 | [[READABILITY|Читаемость документов (Flesch-Kincaid)]] | `READABILITY.md` | 159 мин | 37544 | — |
| 4 | [[READING_TIME|Время чтения документов]] | `READING_TIME.md` | 117 мин | 27575 | — |
| 5 | [[341-приложение-c-образец-спецификаций-инструментов-ing|Приложение C: Образец Спецификаций Инструментов In]] | `02-anthropic-vacancies` | 89 мин | 20580 | — |
| 6 | [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]] | `02-anthropic-vacancies` | 91 мин | 19240 | — |
| 7 | [[133-обратная-связь|Обратная связь]] | `02-anthropic-vacancies` | 75 мин | 17102 | — |
| 8 | [[CONCEPTS|Глоссарий понятий]] | `CONCEPTS.md` | 65 мин | 15040 | — |

---

## Быстрый старт

```bash
# Поиск по базе знаний
python scripts/improve_passage_retrieval.py --query "ваш запрос"
python scripts/improve_faceted_search.py --query "RAG" --section 05-habr-projects

# Список чтения по теме
python scripts/improve_reading_list.py --query "архитектура агента"

# LLM Q&A (требует ANTHROPIC_API_KEY)
python scripts/improve_llm_qa.py --question "Что такое NGT Memory?"
```

_Отчёт сгенерирован автоматически скриптом `improve_export_report.py` (2026-05-14)_


<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [CONCEPTS](../CONCEPTS.md)
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)

