# Svyazi 2.0 — Knowledge Base Report

_Сгенерировано автоматически: 2026-04-29_

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

**Svyazi 2.0 — Knowledge Base Report** — аналитический обзор базы знаний, сгенерированный автоматически 2026-04-29.

База содержит **1195 документов** объёмом **992,315 слов** в **20 секциях**. Здоровье репозитория: **77/100/100**, средний балл документов: **71.2/100/100**, словарное богатство (STTR): **0.675**.

Цель базы знаний — поддержка разработки **Svyazi 2.0**, community intelligence platform, объединяющей лучшие OSS-проекты с Хабра в единую архитектуру Knowledge OS.

## Корпус документов

### Общая статистика

| Метрика | Значение |
|---------|----------|
| Документов | **1195** |
| Слов | **992,315** |
| Секций | **20** |
| Здоровье репо | **77/100/100** |
| Средний балл | **71.2/100/100** |
| Словарное богатство (STTR) | **0.675** |

### По секциям

| Секция | Файлов | Слов |
|--------|--------|------|
| **obsidian** | 1190 | 975,036 |
| **Anthropic Vacancies** | 357 | 311,655 |
| **nautilus** | 255 | 148,523 |
| **anthropic-vacancies** | 111 | 30,960 |
| **AI Collaborations** | 17 | 26,057 |
| **lorenzo-agent** | 62 | 19,979 |
| **habr-unique-projects** | 56 | 13,161 |
| **technology-combinations** | 53 | 12,903 |
| **svyazi-2-0** | 59 | 12,455 |
| **Svyazi 2.0** | 16 | 11,256 |
| **Habr Projects** | 10 | 9,333 |
| **ai-collaborations** | 30 | 8,207 |
| **Templates** | 24 | 4,973 |
| **Contacts** | 15 | 3,492 |
| **Tech Combinations** | 7 | 3,084 |
| **glossary** | 4 | 2,282 |
| **autofilled** | 13 | 1,710 |
| **badges** | 1 | 59 |

## Ключевые проекты

_Авторы и проекты из CONTACTS.md:_

| Автор | Проект | Слой | Приоритет |
|-------|--------|------|-----------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 50 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 33 | — |
| **Cutcode** | AIF Handoff | orchestration | 36 | — |
| **Dmitriila** | SENTINEL | security | 34 | — |
| **MiXaiLL76** | Auto AI Router | security | 30 | — |
| **Sonia_Black** | knowledge-space | knowledge | 19 | — |
| **VitalyOborin** | Yodoca | memory | 39 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 43 | — |

## Ключевые сущности

- 👤 **anthropic** (people) — упомянут в 743 файлах
- 📦 **nautilus** (projects) — упомянут в 467 файлах
- 👤 **claude** (people) — упомянут в 400 файлах
- ⚙️ **mcp** (tech) — упомянут в 300 файлах
- 📦 **svyazi** (projects) — упомянут в 296 файлах
- 🏢 **вк** (orgs) — упомянут в 265 файлах
- 📦 **github** (projects) — упомянут в 238 файлах
- 🏢 **meta** (orgs) — упомянут в 199 файлах
- 👤 **svend4** (people) — упомянут в 195 файлах
- ⚙️ **llm** (tech) — упомянут в 192 файлах

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

- - - - - - - - - - -  Как реализован forensic RAG с доказуемостью? [[Карта базы знаний Lorenzo](docs/
- - Как реализован forensic RAG с доказуемостью? [[Глобальный Q&A](docs/QA.md)]
- - Что такое Evidence Envelope и зачем он нужен? [[Глобальный Q&A](docs/QA.md)]
- - Какие RAG-подходы сравниваются в документах? [[Глобальный Q&A](docs/QA.md)]
- - Какие инструменты обеспечивают безопасность агентов? [[Глобальный Q&A](docs/QA.md)]
- ## Как реализован forensic RAG с доказуемостью? [Раздел: 01-svyazi]
- ## Что такое Evidence Envelope и зачем он нужен? [Как реализован forensic RAG с доказуемостью?]
- ## Какие RAG-подходы сравниваются в документах? [Что такое Evidence Envelope и зачем он нужен?]

## Рекомендуемое чтение

_Топ документов по насыщенности (из READING_LIST.md):_

| # | Документ | Секция | Время | Слов |
|---|----------|--------|-------|------|
| 1 | [11 integration contracts](docs/01-svyazi/11-integration-contracts.md) | `01-svyazi` | 3 мин | 737 | 9.6 |
| 2 | [Интеграционный контракт, который стоит зафиксирова](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | `04-ai-collaborations` | 4 мин | 846 | 9.4 |
| 3 | [09 architectural gaps](docs/01-svyazi/09-architectural-gaps.md) | `01-svyazi` | 3 мин | 758 | 9.3 |
| 4 | [Архитектурные зазоры, которые важнее новых инструм](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | `04-ai-collaborations` | 4 мин | 805 | 9.2 |
| 5 | [03 component catalog](docs/01-svyazi/03-component-catalog.md) | `01-svyazi` | 6 мин | 1352 | 9.1 |

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

_Отчёт сгенерирован автоматически скриптом `improve_export_report.py` (2026-04-29)_

