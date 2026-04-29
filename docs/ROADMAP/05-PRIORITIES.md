# 05 — Приоритеты: что делать прямо сейчас

Финальный документ серии. Конкретный sprint-план для 3 разных стратегий.

**Документ:** часть серии ROADMAP. См. также: [00-CURRENT-STATE](./00-CURRENT-STATE.md), [01-SIMPLE](./01-SIMPLE.md), [02-MEDIUM](./02-MEDIUM.md), [03-INNOVATIVE](./03-INNOVATIVE.md), [04-NOVEL](./04-NOVEL.md).

---

## 3 стратегических пути

### Путь A: Quick value (быстрый rollout, проверенные паттерны)
**Цель:** усилить production usability за 12 недель / 12-15 спринтов
**Аудитория:** existing users, маленькая команда, демо для друзей

### Путь B: Differentiation (отличиться от других RAG)
**Цель:** сделать что-то что не делают LangChain/LlamaIndex, но реализуемо
**Аудитория:** technical buyers, конкурентное позиционирование

### Путь C: Long-game (исследовательский плацдарм)
**Цель:** создать что-то truly novel, что задаёт направление для индустрии
**Аудитория:** научное сообщество, патенты, future product

---

## Decision matrix — какой путь выбрать

| Вопрос | Путь A | Путь B | Путь C |
|--------|:------:|:------:|:------:|
| У тебя есть пользователи прямо сейчас? | ⭐ | ✓ | — |
| Нужен оборотный капитал в 6 месяцев? | ⭐ | ✓ | — |
| Хочешь публикации / patent? | — | ✓ | ⭐ |
| Терпение к research uncertainty? | — | ✓ | ⭐ |
| Готов вложить 6-12 месяцев в одну идею? | — | ✓ | ⭐ |
| Команда состоит из 1-2 человек? | ⭐ | ⭐ | ✓ |
| У тебя >$50K research budget? | — | ✓ | ⭐ |

**Если 4+ ⭐ в одной колонке → твой путь.**

---

## Путь A — Quick value (12 спринтов, ~3 месяца)

### Состав
- **S6** Per-user preferences profile (1 спринт) — foundation
- **S2** Faceted search UI (3 спринта) — visibility
- **S4** Citation graph + PageRank (1 спринт) — quick win
- **M2** Cross-encoder reranking (3 спринта) — biggest quality lift
- **M5** Continuous online eval (3 спринта) — production confidence
- **S7** Read-receipt tracking (1 спринт) — personal use loop

### Quarterly milestones

**Месяц 1 (sprints 54-58):** Foundation
- W1-W2: S6 per-user preferences
- W3-W6: S2 faceted UI (backend → frontend → polish)
- W7: S4 PageRank
- Demo: working web UI с фасетами и personalized defaults

**Месяц 2 (sprints 59-62):** Quality
- W8-W11: M2 cross-encoder reranking (abstraction → integration → production)
- W12: A/B test reranking against baseline
- Eval: +15% precision@5 expected

**Месяц 3 (sprints 63-66):** Production
- W13-W15: M5 continuous online eval (sampling → drift → dashboard)
- W16: S7 read tracking
- Polish, docs, blog post

### Метрики успеха пути A
- Week-1 active users (если есть): +50%
- Eval score (golden datasets): 60 → 75 (out of 100)
- Time-to-first-result: <500ms
- Documentation completeness: 100% public modules covered

### Risks
- UI work непредсказуем по time. Mitigation: cap S2 at 4 спринтов
- Reranker model download нужен internet первый раз. Mitigation: bundled docker image option
- Online eval может найти проблемы которые не было плана решать. Mitigation: backlog с приоритетами

---

## Путь B — Differentiation (15-18 спринтов, ~4-5 месяцев)

### Состав
- **M5** Continuous online eval (3) — нужно перед изменениями
- **I3** Provenance + confidence intervals (5) — flagship feature
- **M1** Knowledge graph (4) — multi-hop рассуждение
- **I1** Self-RAG с reflection (5) — hallucination reduction
- (опционально) **N3** Graph-of-thoughts (8) — visual differentiator

### Quarterly milestones

**Месяц 1 (sprints 54-56):** Eval foundation
- M5 — continuous online eval готов
- Baseline metrics established
- Drift detection работает

**Месяцы 2-3 (sprints 57-66):** Trust & reasoning
- I3 — provenance с CI (5 спринтов)
  - Claim extraction → source linking → bootstrap CI → UI
  - Demo: «every claim has source span + 95% CI on confidence»
- M1 — knowledge graph (4 спринта)
  - Triplet extraction → storage → query → integration с retrieval
  - Demo: multi-hop query с visualization

**Месяц 4 (sprints 67-71):** Hallucination control
- I1 — Self-RAG (5 спринтов)
  - Decision tokens → reflect step → loop control → calibration → A/B
  - Eval: -30% hallucination rate
  - Production rollout с canary

**Месяц 5 (sprints 72-79, optional):** Visual demo
- N3 — Graph-of-thoughts (8 спринтов)
  - Strong demo, но big investment
  - Skip if budget/time tight

### Метрики успеха пути B
- Provenance: 100% answers have CI + source spans
- Multi-hop accuracy: +25% против flat RAG
- Hallucination rate: -30%
- Differentiation: 3 features что не делает LangChain (provenance CI, KG-aware retrieval, self-RAG)

### Risks
- Big project, scope creep. Mitigation: ruthless cuts при overrun
- I1 + I3 + M1 — complex interactions, integration debt. Mitigation: shared abstractions design upfront
- KG quality зависит от extraction. Mitigation: opt LLM-assisted extraction при rule-based слабом

---

## Путь C — Long-game (8-12 месяцев, single big bet)

### Опция C1: Document metabolism (N1)
- 8-12 спринтов
- Highest novelty
- Research-grade outcome
- Risk: может не сработать (auto-rewrite quality)

### Опция C2: Graph-of-thoughts production (N3)
- 8-10 спринтов
- Visual wow-factor
- Builds on existing primitives (workflow, agent)
- Risk: hard для small UI / UX team

### Опция C3: Federated privacy eval (N5)
- 10+ спринтов
- Patentable
- Niche but high-impact for compliance buyers
- Risk: requires HE/DP expertise

### Структура пути C (универсальная)

**Month 1:** Foundation
- Background research (papers, prior art)
- Threat model / requirements
- Prototype simplest possible version

**Month 2-3:** Core loop
- MVP что worked end-to-end
- Internal demo

**Month 4-6:** Quality + integration
- Connect к existing Lorenzo modules
- Production hardening
- Documentation

**Month 7-9:** External validation
- Demo на conference / user
- Article / patent application
- Open source release (if appropriate)

**Month 10-12:** Iteration
- Based на feedback
- Polish
- Long-term maintenance plan

### Метрики успеха пути C
- 1 publishable result (paper, blog, talk)
- 1 patentable concept (legal review)
- 1 working prototype demonstrable
- Acquisition / collaboration interest from external party

### Risks
- 9-12 month bet может не закрыться. Mitigation: monthly checkpoints, kill criteria
- Solo engineering risk. Mitigation: внешние reviewers / collaborators
- Tech may not work as expected. Mitigation: alternative path planned

---

## Hybrid: Pragmatic recommendation

### Месяцы 1-3: Путь A (всё равно нужен)
Без production confidence (eval, dashboard, UI) трудно осмысленно идти дальше.

### Месяцы 4-6: Путь B core (I1 + M1)
Self-RAG и Knowledge Graph дают reasoning differentiation без enormous risk.

### Месяцы 7+: 1 элемент пути C
Например N3 (graph-of-thoughts) если есть UI ресурсы, или N1 (metabolism) если research focus.

**Total:** 12-month roadmap, ~36-48 спринтов, full coverage от production basics до research differentiation.

---

## Критерии stop / kill

### Когда отступить от плана?

| Сигнал | Действие |
|--------|----------|
| 3 спринта подряд без прогресса по фиче | Pause, retrospective, переформулировать |
| Eval score regression >10% | Hard rollback, hotfix спринт |
| Production incident (data loss, security) | Прервать roadmap, безопасность first |
| Новая user research выявила другую priority | Re-plan, do not blindly continue |
| Найден existing OSS что делает то же самое | Adopt that, don't duplicate |
| Budget overrun >50% | Cut scope ruthlessly |

---

## Ближайший спринт (если стартуем Путь A)

### Sprint 54: Per-user preferences profile (S6)

**Цель:** Foundation для всей дальнейшей personalization
**Бюджет:** 1 спринт (3-5 рабочих дней при 1-человеке)

**Задачи:**
1. `docstoolkit/profile/` модуль
2. `UserProfile` dataclass + load/save
3. `apply_profile(profile, kwargs) → kwargs` middleware
4. Интеграция в `rag.ask`, `agent.run`, CLI
5. Тесты (~15 кейсов)
6. Docs: `docs-toolkit/PROFILES.md`
7. Live demo: 2 user'а с разными defaults на same query

**Definition of Done:**
- `pytest docs-toolkit/tests/test_profile.py` все green
- Full suite не сломан (>540 tests pass)
- `lorenzo --user alice rag ask "X"` использует Alice's defaults
- `improve_mcp_test.py` 30/30
- Commit + push to working branch

---

## Ближайший спринт (если стартуем Путь B)

### Sprint 54: Continuous online eval (M5) — старт

**Цель:** Без production метрик невозможно осмысленно delivering improvements
**Бюджет:** 3 спринта (M5 это композитная фича)

**Задачи Sprint 54:**
1. `docstoolkit/online_eval/` модуль
2. `OnlineEvalSampler` (random sampling 1/N)
3. SQLite таблица `online_eval_runs`
4. Hook в `rag.ask` для возможности sampling
5. Tests + docs

**Sprint 55:** Drift detection + alert via webhooks
**Sprint 56:** HTML dashboard

---

## Ближайший спринт (если стартуем Путь C — N3 graph-of-thoughts)

### Sprint 54: Thought primitives

**Цель:** Foundation для graph-of-thoughts
**Бюджет:** 1 спринт

**Задачи:**
1. `docstoolkit/got/` модуль
2. `Thought`, `ThoughtEdge`, `ThoughtGraph` dataclasses
3. Basic traversal API (children, parents, leaves)
4. Markdown / DOT export для visualization
5. Tests

**Sprint 55-56:** Graph construction (LLM-driven thought spawning)
**Sprint 57-59:** Aggregation methods + UI POC
**Sprint 60-61:** Integration with existing RAG / adaptive

---

## Recap

| Путь | Сила | Риск | Срок | Бюджет |
|------|------|------|------|--------|
| **A — Quick value** | Production-ready impact | Low | 3 мес | 12-15 спринтов |
| **B — Differentiation** | Конкурентное преимущество | Medium | 4-5 мес | 15-18 спринтов |
| **C — Long-game** | Truly novel result | High | 8-12 мес | 8-12 спринтов в одну тему |
| **Hybrid (рекомендуется)** | Балансированный | Medium | 12 мес | 36-48 спринтов |

**Default рекомендация:** Hybrid (A → B → C) если ресурсы позволяют. Если только 3 месяца — Путь A. Если хочется research focus — Путь C с минимальной A в начале для baseline.

Готов начать любой из них в следующем спринте.
