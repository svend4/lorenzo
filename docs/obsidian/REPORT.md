---
title: "Svyazi 2.0 — Knowledge Base Report"
tags:
  - general
date: 2026-05-11
---

# Svyazi 2.0 — Knowledge Base Report

_Сгенерировано автоматически: 2026-05-11_

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

**Svyazi 2.0 — Knowledge Base Report** — аналитический обзор базы знаний, сгенерированный автоматически 2026-05-11.

База содержит **1244 документов** объёмом **1,537,236 слов** в **23 секциях**. Здоровье репозитория: **90/100**, средний балл документов: **95.9/100/100**, словарное богатство (STTR): **0.621**.

Цель базы знаний — поддержка разработки **Svyazi 2.0**, community intelligence platform, объединяющей лучшие OSS-проекты с Хабра в единую архитектуру Knowledge OS.

## Корпус документов

### Общая статистика

| Метрика | Значение |
|---------|----------|
| Документов | **1244** |
| Слов | **1,537,236** |
| Секций | **23** |
| Здоровье репо | **90/100** |
| Средний балл | **95.9/100/100** |
| Словарное богатство (STTR) | **0.621** |

### По секциям

| Секция | Файлов | Слов |
|--------|--------|------|
| **obsidian** | 1238 | 1,491,904 |
| **Anthropic Vacancies** | 357 | 341,828 |
| **nautilus** | 255 | 176,913 |
| **anthropic-vacancies** | 111 | 47,082 |
| **lorenzo-agent** | 62 | 28,664 |
| **AI Collaborations** | 17 | 27,940 |
| **svyazi-2-0** | 60 | 20,715 |
| **habr-unique-projects** | 56 | 19,966 |
| **technology-combinations** | 53 | 19,585 |
| **processing-guide** | 13 | 17,500 |
| **Habr Projects** | 16 | 14,869 |
| **Svyazi 2.0** | 16 | 13,360 |
| **ai-collaborations** | 31 | 12,182 |
| **Templates** | 24 | 7,707 |
| **Contacts** | 17 | 5,044 |
| **Tech Combinations** | 7 | 3,815 |
| **letters** | 10 | 3,618 |
| **meta-scripting** | 7 | 3,344 |
| **autofilled** | 13 | 2,904 |
| **glossary** | 4 | 2,692 |
| **badges** | 1 | 113 |

## Ключевые проекты

_Авторы и проекты из CONTACTS.md:_

| Автор | Проект | Слой | Приоритет |
|-------|--------|------|-----------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 132 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 82 | — |
| **Cutcode** | AIF Handoff | orchestration | 74 | — |
| **Dmitriila** | SENTINEL | security | 65 | — |
| **MiXaiLL76** | Auto AI Router | security | 61 | — |
| **Sonia_Black** | knowledge-space | knowledge | 42 | — |
| **VitalyOborin** | Yodoca | memory | 110 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 85 | — |

## Ключевые сущности

- 📦 **obsidian** (projects) — упомянут в 807 файлах
- 👤 **anthropic** (people) — упомянут в 739 файлах
- 📦 **nautilus** (projects) — упомянут в 542 файлах
- 📦 **lorenzo** (projects) — упомянут в 499 файлах
- 👤 **claude** (people) — упомянут в 455 файлах
- 📦 **svyazi** (projects) — упомянут в 392 файлах
- ⚙️ **mcp** (tech) — упомянут в 361 файлах
- 🏢 **вк** (orgs) — упомянут в 298 файлах
- 📦 **github** (projects) — упомянут в 263 файлах
- ⚙️ **bm25** (tech) — упомянут в 261 файлах

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

- -  Какие 5 архитектурных зазоров выделены в исследовании? [Содержан]
- -  Что входит в интеграционный контракт между слоями? [Содержание]
- -  Как реализован forensic RAG с доказуемостью? [Содержание]
- -  Что такое Evidence Envelope и зачем он нужен? [Содержание]
- -  Какие RAG-подходы сравниваются в документах? [Содержание]
- - Какие 5 архитектурных зазоров выделены в исследовании? [[QA|[Глобальный Q&A]]]
- - Что входит в интеграционный контракт между слоями? [[QA|[Глобальный Q&A]]]
- - Как реализован forensic RAG с доказуемостью? [[QA|[Глобальный Q&A]]]

## Рекомендуемое чтение

_Топ документов по насыщенности (из READING_LIST.md):_

| # | Документ | Секция | Время | Слов |
|---|----------|--------|-------|------|
| 1 | [[TABLES|Все таблицы репозитория]] | `TABLES.md` | 1519 мин | 352795 | — |
| 2 | [[OUTLINE|Outline базы знаний]] | `OUTLINE.md` | 183 мин | 40376 | — |
| 3 | [[READABILITY|Читаемость документов (Flesch-Kincaid)]] | `READABILITY.md` | 159 мин | 37538 | — |
| 4 | [[READING_TIME|Время чтения документов]] | `READING_TIME.md` | 117 мин | 27566 | — |
| 5 | [[341-приложение-c-образец-спецификаций-инструментов-ing|Приложение C: Образец Спецификаций Инструментов In]] | `02-anthropic-vacancies` | 89 мин | 20580 | — |
| 6 | [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]] | `02-anthropic-vacancies` | 91 мин | 19240 | — |
| 7 | [[133-обратная-связь|Обратная связь]] | `02-anthropic-vacancies` | 75 мин | 17102 | — |
| 8 | [[CONCEPTS|Глоссарий понятий]] | `CONCEPTS.md` | 65 мин | 15054 | — |

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

_Отчёт сгенерирован автоматически скриптом `improve_export_report.py` (2026-05-11)_


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [[07-mvp-planning]]
- [[CONCEPTS]]
- [[HEALTH]]
- [[OUTLINE]]
- [[READABILITY]]
- [[READING_TIME]]
- [[README]]
- [[SEARCH]]
- _...ещё 1_


<!-- similar-docs -->

---

**Похожие документы:**
- [[REPORT]] (сходство 0.68)
- [[KNOWLEDGE_MAP]] (сходство 0.31)
- [[KNOWLEDGE_MAP]] (сходство 0.30)

