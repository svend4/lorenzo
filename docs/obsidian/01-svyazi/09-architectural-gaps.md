---
title: "09 Architectural Gaps"
tags:
  - svyazi
date: 2026-04-29
---

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Архитектурный зазор Уже сильные кандидаты Что в них уже хорошо закрыто Что пока остаётся незакрытым Что брать в MVP --------------- Карточка как единица правды Svyazi, AgentFS Card
> 🔧 **Подход:** В‑третьих, нужен memory governance layer, который не даёт ассоциативной памяти записывать предлагаемое как истинное.
> ✅ **Результат:** Наоборот, даже средний model tier даёт много пользы, если extract/normalize/review/evidence и memory status already pinned.
> 🏷️ **Ключевые слова:** `svyazi`, `memory`, `проект`, `search`, `review`, `agentfs`, `knowledge`, `evidence`
>


<!-- summary -->
> После первичного обзора видно, что дефицит уже не в наличии компонентов, а в **стыках между ними**. Svyazi[^svyazi] хорошо закрывает ingest и нормализацию; AgentFS[^agentfs] даёт `.agentos` и compile‑to‑runtime политику
**Проекты:** Svyazi, CardIndex[^cardindex], AgentFS, [[03-component-catalog|knowledge-space]][^knowledge-space], mclaude, AI Factory, Rufler[^rufler], LiteParse

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, self-improvement -->



## Архитектурные зазоры, которые важнее новых инструментов

После первичного обзора видно, что дефицит уже не в наличии компонентов, а в **стыках между ними**. Svyazi хорошо закрывает ingest и нормализацию; AgentFS даёт `.agentos` и compile‑to‑runtime политику; [[03-component-catalog|knowledge-space]] формирует agent‑readable reference cards; NGT[^ngt] Memory и Yodoca[^yodoca] решают разные режимы памяти; research-docs/LiteParse и Legal RAG[^rag] решают доказуемость; LiteLLM, Auto AI Router и Tool Search — execution plane; SENTINEL[^sentinel] и path‑guard практики — безопасность. Но именно на переходах “card ↔ memory”, “memory ↔ evidence”, “evidence ↔ review”, “review ↔ agent execution” сегодня остаётся больше всего архитектурного риска. citeturn41search0turn27view0turn33view2turn22view4turn21view0turn20view5turn20view6turn39view0turn39view1turn20view10

В практическом смысле есть пять зазоров, которые стоит считать приоритетнее поиска ещё десяти новых инструментов. Во‑первых, нужен **единый тип карточки**, который умеет хранить и “человека”, и “проект”, и “эпизод”, и “документ”, и “слабую гипотезу”. Во‑вторых, нужен **Evidence Envelope**: стандарт, по которому любой вывод системы можно обратно привязать к странице, координате, фрагменту текста или истории изменения. В‑третьих, нужен **memory governance layer**, который не даёт ассоциативной памяти записывать предлагаемое как истинное. В‑четвёртых, нужен **agent contract layer**, где навыки, маршрутизация и права оформлены как исполнимые правила, а не как размазанные инструкции по разным файлам. В‑пятых, нужен **review protocol**, который отделяет “обнаружено системой” от “принято в индекс сообщества” или “использовано во внешнем отчёте”. Каждый из этих зазоров уже частично покрыт найденными решениями, но не целиком одной системой. citeturn41search0turn20view5turn20view6turn22view4turn21view0turn20view16turn27view0turn20view3turn20view11

Ниже — концентрированная таблица именно по архитектурным зазорам, а не по самим проектам.

| Архитектурный зазор | Уже сильные кандидаты | Что в них уже хорошо закрыто | Что пока остаётся незакрытым | Что брать в MVP |
|---|---|---|---|---|
| Карточка как единица правды | Svyazi, AgentFS | CardIndex, hash/dedup, versionable vault, persistent state | Универсальная типизация для person/project/doc/episode/hypothesis | Card schema + raw/inferred split + immutable IDs citeturn41search0turn27view0turn33view4 |
| Доказуемое основание вывода | research-docs/LiteParse, Legal RAG, Hybrid RAG | Bounding boxes, page-level grounding, coordinates, transparent retrieval | Единый формат “evidence pack” между retrieval и интерфейсом | Page-level viewer + source_id/page/span/box schema citeturn20view5turn20view6turn34view2 |
| Память с контролируемым статусом | NGT Memory, Yodoca, agent-memory-mcp, Memory OS | Associative retrieval, consolidation, forgetting, typed memory, guard rails | Чёткая граница truth/proposal/conflict/decayed | Pending queue + confidence/state machine на наполнение графа citeturn22view4turn21view0turn20view16turn39view3 |
| Оркестрация и review | mclaude, AI Factory, Rufler, Sequential | Locks, mailbox, patch learning, YAML swarm, sequential review | Стандарт handoff для non-code workflow и knowledge moderation | 2–3 роли: extractor → reviewer → publisher citeturn20view2turn20view3turn20view4turn20view11 |
| Безопасный execution plane | LiteLLM, Auto AI Router, Tool Search, SENTINEL | Unified API, lightweight routing, lazy tool loading, runtime guard | Общая policy matrix на tool classes и external skills | Read-only by default + write approval + path allowlist citeturn11search2turn39view0turn39view1turn20view10turn20view16 |

Из этого следует важный практический принцип: **Svyazi‑2.0 нужно начинать не с “самой умной модели”, а с самой строгой структуры переходов между слоями**. Сильная модель без карточного статуса, Evidence Envelope и review protocol быстро превращает систему в красивый, но плохо аудитируемый генератор гипотез. Наоборот, даже средний model tier даёт много пользы, если extract/normalize/review/evidence и memory status already pinned. Это согласуется и с Svyazi‑подходом к [[01-executive-summary|CardIndex]] и privacy by design, и с Memory OS‑критикой “thoughtful but schema-breaking reasoning”, и с Legal RAG‑подходом к page‑level доказуемости. citeturn41search0turn39view3turn20view6turn20view18

<!-- similar-docs -->

---

**Похожие документы:**
- [[09-архитектурные-зазоры-которые-важнее-новых-инструме]] (сходство 1.00)
- [[QA]] (сходство 0.17)
- [[11-интеграционный-контракт-который-стоит-зафиксироват]] (сходство 0.16)


<!-- see-also -->

---

**Смотрите также:**
- [[00-intro-part2|11-integration-contracts]]/11-integration-contracts.md)
- [[00-intro-part2|06-security-privacy]]/06-security-privacy.md)
- [[00-intro-part2|07-mvp-planning]]/07-mvp-planning.md)



<!-- footnotes-added -->

---

[^rag]: Retrieval-Augmented Generation — генерация с поиском

[^cardindex]: OSS-проект: индекс знаний на карточках (MIT)

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^yodoca]: OSS-проект: система памяти с консолидацией (Apache 2.0)

[^ngt]: OSS-проект: ассоциативный граф памяти (BSL 1.1)

[^sentinel]: OSS-проект: безопасность и allowlist для MCP

[^rufler]: OSS-проект: оркестратор AI-агентов

[^svyazi]: Главный проект: экосистема AI-компонентов

[^knowledge-space]: OSS-проект: база знаний 785+ карточек (MIT)
