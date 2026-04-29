
<!-- summary -->
> По итогам поиска видно, что **Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей**, не придумывая половину архитектуры заново. Самый дефицитный слой — не память, не RAG[^rag] и не оркестр
**Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[^agentfs], mclaude, AI Factory, Rufler[^rufler], LiteParse, Yodoca[^yodoca]

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement, collaboration -->



## Выводы

По итогам поиска видно, что **Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей**, не придумывая половину архитектуры заново. Самый дефицитный слой — не память, не RAG и не оркестрация по отдельности: все они уже представлены на Хабре и в репозиториях. Дефицитный слой — **правильная сборка**: где CardIndex остаётся source of truth, где память умеет и усиливать, и забывать, где retrieval остаётся доказуемым, где агентность не ломает безопасность, и где стоимость не взрывается ещё до первой полезной операции. citeturn41search0turn27view0turn22view4turn21view0turn20view5turn20view6turn20view11turn20view10turn39view1turn39view0

Если ранжировать найденные направления по практической силе именно для старта, то порядок такой. **Первое** — Svyazi + AgentFS + NGT[^ngt]/Yodoca + LiteParse: это даёт уже полезный MVP. **Второе** — добавить AI Factory/mclaude/Rufler/Sequential как build‑ и moderation‑контур. **Третье** — подключить voice/local-first sync и только потом AutoResearch. Другими словами, наиболее реалистичная стратегия — сначала собрать **машину обнаружения и объяснения коллабораций**, а уже затем превращать её в полностью самоулучшающуюся агентную фабрику. Именно такой порядок лучше всего соответствует зрелости найденных проектов и снижает интеграционный риск. citeturn41search0turn27view0turn21view0turn22view4turn20view5turn20view3turn20view2turn20view4turn20view11turn21view10turn11search11turn20view19

<!-- similar-docs -->

---

**Похожие документы:**
- [07-выводы](../04-ai-collaborations/07-выводы.md) (сходство 0.95)
- [01-executive-summary](../04-ai-collaborations/01-executive-summary.md) (сходство 0.21)
- [01-executive-summary](../04-ai-collaborations/01-executive-summary.md) (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [07-выводы](../04-ai-collaborations/07-выводы.md)
- [08-что-это-продолжение-добавляет](../04-ai-collaborations/08-что-это-продолжение-добавляет.md)
- [01-executive-summary](../04-ai-collaborations/01-executive-summary.md)
- [MISSING](../MISSING.md)



<!-- footnotes-added -->

---

[^rag]: Retrieval-Augmented Generation — генерация с поиском

[^cardindex]: OSS-проект: индекс знаний на карточках (MIT)

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^yodoca]: OSS-проект: система памяти с консолидацией (Apache 2.0)

[^ngt]: OSS-проект: ассоциативный граф памяти (BSL 1.1)

[^rufler]: OSS-проект: оркестратор AI-агентов

[^svyazi]: Главный проект: экосистема AI-компонентов

<!-- backlinks-auto -->
## Упоминается в

- [04 Ensembles Overview](04-ensembles-overview.md)
- [12 Roadmap](12-roadmap.md)
- [Executive summary](../04-ai-collaborations/01-executive-summary.md)
- [Svyazi[^svyazi] 2.0 — Архитектура и исследование](README.md)
- [Svyazi[^svyazi] 2.0 — Исполнительное резюме](01-executive-summary.md)
- [Выводы](../04-ai-collaborations/07-выводы.md)
- [Методика и рамка отбора](../04-ai-collaborations/02-методика-и-рамка-отбора.md)
- [Что это продолжение добавляет](../04-ai-collaborations/08-что-это-продолжение-добавляет.md)
## Упоминается в

- [Svyazi[^svyazi] 2.0 — Архитектура и исследование](docs/01-svyazi/README.md)

<!-- related-auto -->
## Связанные документы

- [Выводы](../04-ai-collaborations/07-выводы.md) _53%_
- [Executive summary](../04-ai-collaborations/01-executive-summary.md) _42%_
- [04 Ensembles Overview](04-ensembles-overview.md) _33%_
- [Что это продолжение добавляет](../04-ai-collaborations/08-что-это-продолжение-добавляет.md) _33%_
- [Svyazi[^svyazi] 2.0 — Исполнительное резюме](01-executive-summary.md) _29%_
- [07 Mvp Planning](07-mvp-planning.md) _29%_
- [Приоритетные ансамбли](../04-ai-collaborations/04-приоритетные-ансамбли.md) _29%_
- [09 Architectural Gaps](09-architectural-gaps.md) _25%_
## Связанные документы

- [Выводы](../04-ai-collaborations/07-выводы.md) _81%_
- [Executive summary](../04-ai-collaborations/01-executive-summary.md) _53%_
- [Что это продолжение добавляет](../04-ai-collaborations/08-что-это-продолжение-добавляет.md) _37%_
- [04 Ensembles Overview](04-ensembles-overview.md) _33%_
- [Приоритетные ансамбли](../04-ai-collaborations/04-приоритетные-ансамбли.md) _33%_
- [Новые ансамбли следующего шага](../04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) _33%_
- [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) _29%_
- [07 Mvp Planning](07-mvp-planning.md) _29%_
