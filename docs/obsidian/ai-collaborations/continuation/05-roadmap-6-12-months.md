---
title: "Roadmap на 6–12 месяцев"
tags:
  - ai-collaborations
date: 2026-04-29
---

# Roadmap на 6–12 месяцев

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** CardIndex, mclaude, AI Factory

---
<!-- tags: memory, rag, orchestration, security, knowledge, architecture, roadmap, self-improvement, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

5. Roadmap на 6–12 месяцев

Ниже дорожная карта уже не “по инструментам”, а по системным способностям. Она предполагает, что базовый MVP из CardIndex + evidence + memory уже начат.

| Фаза | Срок | Главная цель | Definition of Done | Метрика успеха
| 0. Contract Freeze | 2–3 недели | Зафиксировать Card Envelope, Evidence Envelope, Memory Write Policy, Trace Envelope | Есть JSON/YAML‑схемы, тестовые карточки person/project/episode/evidence, все pipeline‑шаги пишут в один формат | 100% карточек имеют card_id, state, sources, payload_hash
| 1. Evidence‑first MVP | 1 месяц | Любой match объясняется источниками | UI показывает match + evidence pack + page/span/source links | ≥80% recommendations имеют проверяемый evidence
| 2. Memory Governance | 1–2 месяца | Ассоциации не смешиваются с фактами | Есть episode/proposal/fact/decayed/conflict states и review queue | False positive по approved facts <10% на тестовом наборе
| 3. AgentOps Layer | 2–3 месяца | Все agent runs трассируются | Langfuse/Trace‑подобный слой пишет model/tool/cost/latency/anomaly | 100% внешних выводов имеют trace_id
| 4. Multi‑agent Moderation | 3–4 месяца | Extractor/reviewer/publisher работают как роли | mclaude/AI Factory/A2A‑style handoff; risky actions через HITL | Среднее время review падает на 30–50%
| 5. Local‑first/Federation | 4–6 месяцев | Узлы сообщества синхронизируют только разрешённые слои | Локальный vault + selective sync + shared metadata graph | Нет PII в shared layer по audit checks
| 6. Self‑Improvement Loop | 6–12 месяцев | Ошибки превращаются в benchmark/prompt/skill patches | Есть regression set, nightly eval, rollback policy | Улучшение precision/recall без роста false positives

Ключевой порядок такой: контракты → evidence → memory governance → AgentOps → multi‑agent → federation → self‑improvement. Не наоборот. Если сначала строить “рой”, он ускорит хаос. Если сначала закрепить card/evidence/memory/trace contracts, рой будет ускорять проверяемый процесс.

<!-- see-also -->

---

**Смотрите также:**
- [[roadmap]]
- [[10-architecture-rfc]]
- [[12-дорожная-карта-прототипа-следующей-итерации]]
- [[12-roadmap]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[roadmap]] (сходство 0.20)
- [[10-architecture-rfc]] (сходство 0.19)
- [[12-дорожная-карта-прототипа-следующей-итерации]] (сходство 0.18)

