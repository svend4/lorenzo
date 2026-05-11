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

База содержит **1244 документов** объёмом **1,479,550 слов** в **23 секциях**. Здоровье репозитория: **90/100**, средний балл документов: **100.0/100/100**, словарное богатство (STTR): **0.628**.

Цель базы знаний — поддержка разработки **Svyazi 2.0**, community intelligence platform, объединяющей лучшие OSS-проекты с Хабра в единую архитектуру Knowledge OS.

## Корпус документов

### Общая статистика

| Метрика | Значение |
|---------|----------|
| Документов | **1244** |
| Слов | **1,479,550** |
| Секций | **23** |
| Здоровье репо | **90/100** |
| Средний балл | **100.0/100/100** |
| Словарное богатство (STTR) | **0.628** |

### По секциям

| Секция | Файлов | Слов |
|--------|--------|------|
| **obsidian** | 1238 | 1,442,526 |
| **Anthropic Vacancies** | 357 | 341,363 |
| **nautilus** | 255 | 171,970 |
| **anthropic-vacancies** | 111 | 45,126 |
| **AI Collaborations** | 17 | 27,880 |
| **lorenzo-agent** | 62 | 27,563 |
| **svyazi-2-0** | 60 | 19,650 |
| **habr-unique-projects** | 56 | 18,952 |
| **technology-combinations** | 53 | 18,631 |
| **processing-guide** | 13 | 17,267 |
| **Habr Projects** | 16 | 14,703 |
| **Svyazi 2.0** | 16 | 13,298 |
| **ai-collaborations** | 31 | 11,627 |
| **Templates** | 24 | 7,490 |
| **Contacts** | 17 | 5,007 |
| **Tech Combinations** | 7 | 3,779 |
| **letters** | 10 | 3,188 |
| **meta-scripting** | 7 | 3,184 |
| **autofilled** | 13 | 2,670 |
| **glossary** | 4 | 2,620 |
| **badges** | 1 | 122 |

## Ключевые проекты

_Авторы и проекты из CONTACTS.md:_

| Автор | Проект | Слой | Приоритет |
|-------|--------|------|-----------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 129 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 81 | — |
| **Cutcode** | AIF Handoff | orchestration | 79 | — |
| **Dmitriila** | SENTINEL | security | 69 | — |
| **MiXaiLL76** | Auto AI Router | security | 63 | — |
| **Sonia_Black** | knowledge-space | knowledge | 43 | — |
| **VitalyOborin** | Yodoca | memory | 103 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 89 | — |

## Ключевые сущности

- 👤 **anthropic** (people) — упомянут в 654 файлах
- 📦 **lorenzo** (projects) — упомянут в 516 файлах
- 👤 **claude** (people) — упомянут в 453 файлах
- 📦 **nautilus** (projects) — упомянут в 404 файлах
- 📦 **svyazi** (projects) — упомянут в 390 файлах
- ⚙️ **mcp** (tech) — упомянут в 357 файлах
- 🏢 **вк** (orgs) — упомянут в 298 файлах
- 📦 **github** (projects) — упомянут в 262 файлах
- ⚙️ **bm25** (tech) — упомянут в 257 файлах
- 🏢 **meta** (orgs) — упомянут в 218 файлах

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
| 1 | [11 integration contracts](01-svyazi/11-integration-contracts.md) | `01-svyazi` | 3 мин | 737 | 9.6 |
| 2 | [Интеграционный контракт, который стоит зафиксирова](04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | `04-ai-collaborations` | 4 мин | 846 | 9.4 |
| 3 | [09 architectural gaps](01-svyazi/09-architectural-gaps.md) | `01-svyazi` | 3 мин | 758 | 9.3 |
| 4 | [Архитектурные зазоры, которые важнее новых инструм](04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | `04-ai-collaborations` | 4 мин | 805 | 9.2 |
| 5 | [03 component catalog](01-svyazi/03-component-catalog.md) | `01-svyazi` | 6 мин | 1352 | 9.1 |

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

