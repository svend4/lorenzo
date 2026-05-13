# Svyazi 2.0 — Knowledge Base Report

_Сгенерировано автоматически: 2026-05-13_

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

**Svyazi 2.0 — Knowledge Base Report** — аналитический обзор базы знаний, сгенерированный автоматически 2026-05-13.

База содержит **1214 документов** объёмом **1,141,443 слов** в **22 секциях**. Здоровье репозитория: **84/100/100**, средний балл документов: **73.0/100/100**, словарное богатство (STTR): **0.636**.

Цель базы знаний — поддержка разработки **Svyazi 2.0**, community intelligence platform, объединяющей лучшие OSS-проекты с Хабра в единую архитектуру Knowledge OS.

## Корпус документов

### Общая статистика

| Метрика | Значение |
|---------|----------|
| Документов | **1214** |
| Слов | **1,141,443** |
| Секций | **22** |
| Здоровье репо | **84/100/100** |
| Средний балл | **73.0/100/100** |
| Словарное богатство (STTR) | **0.636** |

### По секциям

| Секция | Файлов | Слов |
|--------|--------|------|
| **obsidian** | 1209 | 1,116,627 |
| **Anthropic Vacancies** | 357 | 312,364 |
| **nautilus** | 255 | 153,298 |
| **anthropic-vacancies** | 111 | 32,927 |
| **AI Collaborations** | 17 | 26,115 |
| **lorenzo-agent** | 62 | 21,077 |
| **ROADMAP** | 6 | 17,368 |
| **processing-guide** | 12 | 14,614 |
| **habr-unique-projects** | 56 | 14,157 |
| **technology-combinations** | 53 | 13,849 |
| **svyazi-2-0** | 59 | 13,565 |
| **Svyazi 2.0** | 16 | 11,288 |
| **Habr Projects** | 10 | 9,088 |
| **ai-collaborations** | 30 | 8,743 |
| **Templates** | 24 | 5,041 |
| **Contacts** | 15 | 3,623 |
| **Tech Combinations** | 7 | 3,084 |
| **glossary** | 4 | 2,354 |
| **autofilled** | 13 | 1,944 |
| **badges** | 1 | 44 |

## Ключевые проекты

_Авторы и проекты из CONTACTS.md:_

| Автор | Проект | Слой | Приоритет |
|-------|--------|------|-----------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 85 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 53 | — |
| **Cutcode** | AIF Handoff | orchestration | 74 | — |
| **Dmitriila** | SENTINEL | security | 68 | — |
| **MiXaiLL76** | Auto AI Router | security | 64 | — |
| **Sonia_Black** | knowledge-space | knowledge | 33 | — |
| **VitalyOborin** | Yodoca | memory | 70 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 77 | — |

## Ключевые сущности

- 👤 **anthropic** (people) — упомянут в 806 файлах
- 📦 **nautilus** (projects) — упомянут в 532 файлах
- 👤 **claude** (people) — упомянут в 419 файлах
- 📦 **svyazi** (projects) — упомянут в 317 файлах
- ⚙️ **mcp** (tech) — упомянут в 315 файлах
- 🏢 **вк** (orgs) — упомянут в 277 файлах
- 📦 **github** (projects) — упомянут в 241 файлах
- 👤 **svend4** (people) — упомянут в 207 файлах
- 🏢 **meta** (orgs) — упомянут в 198 файлах
- ⚙️ **llm** (tech) — упомянут в 191 файлах

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

- - Как реализован forensic RAG с доказуемостью? [[Глобальный Q&A](docs/QA.md)]
- - Что такое Evidence Envelope и зачем он нужен? [[Глобальный Q&A](docs/QA.md)]
- - Какие RAG-подходы сравниваются в документах? [[Глобальный Q&A](docs/QA.md)]
- - Какие инструменты обеспечивают безопасность агентов? [[Глобальный Q&A](docs/QA.md)]
- - Какова политика доступа по умолчанию (tool classes)? [[Глобальный Q&A](docs/QA.md)]
- ## Как реализован forensic RAG с доказуемостью? [Раздел: 01-svyazi]
- ## Что такое Evidence Envelope и зачем он нужен? [Как реализован forensic RAG с доказуемостью?]
- ## Какие RAG-подходы сравниваются в документах? [Что такое Evidence Envelope и зачем он нужен?]

## Рекомендуемое чтение

_Топ документов по насыщенности (из READING_LIST.md):_

| # | Документ | Секция | Время | Слов |
|---|----------|--------|-------|------|
| 1 | [Все таблицы репозитория](docs/TABLES.md) | `TABLES.md` | 726 мин | 169164 | — |
| 2 | [Outline базы знаний](docs/OUTLINE.md) | `OUTLINE.md` | 133 мин | 30208 | — |
| 3 | [Читаемость документов (Flesch-Kincaid)](docs/READABILITY.md) | `READABILITY.md` | 109 мин | 25522 | — |
| 4 | [Время чтения документов](docs/READING_TIME.md) | `READING_TIME.md` | 106 мин | 25007 | — |
| 5 | [Приложение C: Образец Спецификаций Инструментов In](docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md) | `02-anthropic-vacancies` | 89 мин | 20553 | — |
| 6 | [Интегральный анализ профиля svend4](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | `02-anthropic-vacancies` | 90 мин | 19217 | — |
| 7 | [Обратная связь](docs/02-anthropic-vacancies/133-обратная-связь.md) | `02-anthropic-vacancies` | 75 мин | 17075 | — |
| 8 | [Глоссарий понятий](docs/CONCEPTS.md) | `CONCEPTS.md` | 57 мин | 13247 | — |

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

_Отчёт сгенерирован автоматически скриптом `improve_export_report.py` (2026-05-13)_

