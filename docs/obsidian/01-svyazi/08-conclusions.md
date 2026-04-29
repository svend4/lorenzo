---
title: "08 Conclusions"
tags:
  - svyazi
date: 2026-04-29
---

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей, не придумывая половину архитектуры заново.
> 🔧 **Подход:** По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей, не придумывая половину архитектуры заново.
> ✅ **Результат:** Первое — Svyazi + AgentFS + NGT^ngt/Yodoca + LiteParse: это даёт уже полезный MVP.
> 🏷️ **Ключевые слова:** `summary`, `svyazi`, `executive`, `проект`, `выводы`, `collaborations`, `first`, `cardindex`
>


<!-- summary -->
> По итогам поиска видно, что **Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей**, не придумывая половину архитектуры заново. Самый дефицитный слой — не память, не RAG[^rag] и не оркестр
**Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[^agentfs], mclaude, AI Factory, Rufler[^rufler], [[01-executive-summary|LiteParse]], Yodoca[^yodoca]

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement, collaboration -->



## Выводы

По итогам поиска видно, что **Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей**, не придумывая половину архитектуры заново. Самый дефицитный слой — не память, не RAG и не оркестрация по отдельности: все они уже представлены на Хабре и в репозиториях. Дефицитный слой — **правильная сборка**: где [[01-executive-summary|CardIndex]] остаётся source of truth, где память умеет и усиливать, и забывать, где retrieval остаётся доказуемым, где агентность не ломает безопасность, и где стоимость не взрывается ещё до первой полезной операции. citeturn41search0turn27view0turn22view4turn21view0turn20view5turn20view6turn20view11turn20view10turn39view1turn39view0

Если ранжировать найденные направления по практической силе именно для старта, то порядок такой. **Первое** — Svyazi + AgentFS + NGT[^ngt]/Yodoca + LiteParse: это даёт уже полезный MVP. **Второе** — добавить AI Factory/mclaude/Rufler/Sequential как build‑ и moderation‑контур. **Третье** — подключить voice/local-first sync и только потом [[01-executive-summary|AutoResearch]]. Другими словами, наиболее реалистичная стратегия — сначала собрать **машину обнаружения и объяснения коллабораций**, а уже затем превращать её в полностью самоулучшающуюся агентную фабрику. Именно такой порядок лучше всего соответствует зрелости найденных проектов и снижает интеграционный риск. citeturn41search0turn27view0turn21view0turn22view4turn20view5turn20view3turn20view2turn20view4turn20view11turn21view10turn11search11turn20view19

<!-- similar-docs -->

---

**Похожие документы:**
- [[07-выводы]] (сходство 0.95)
- [[00-intro-part2|01-executive-summary]]/01-executive-summary.md) (сходство 0.21)
- [[01-executive-summary]] (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [[07-выводы]]
- [[08-что-это-продолжение-добавляет]]
- [[01-executive-summary]]
- [[MISSING]]



<!-- footnotes-added -->

---

[^rag]: Retrieval-Augmented Generation — генерация с поиском

[^cardindex]: OSS-проект: индекс знаний на карточках (MIT)

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^yodoca]: OSS-проект: система памяти с консолидацией (Apache 2.0)

[^ngt]: OSS-проект: ассоциативный граф памяти (BSL 1.1)

[^rufler]: OSS-проект: оркестратор AI-агентов

[^svyazi]: Главный проект: экосистема AI-компонентов
