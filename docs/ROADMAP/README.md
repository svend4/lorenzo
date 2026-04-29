# ROADMAP — варианты развития Lorenzo / Knowledge OS

**Дата:** 2026-04-29
**Статус:** Lorenzo на 53-м спринте, production-ready foundation для индивидуального knowledge worker'а или маленькой команды.

Эта серия документов отвечает на вопрос: **«Что дальше?»**

Структурирована от **состояния системы** через **простые улучшения**, **средние**, **инновационные** до **никем не сделанных** концепций — с конкретными приоритетами для решения.

---

## Структура серии

| # | Документ | Тема | Объём |
|--:|----------|------|------:|
| 00 | [00-CURRENT-STATE.md](./00-CURRENT-STATE.md) | Текущая стадия: что есть, что умеет, чего нет | ~340 строк |
| 01 | [01-SIMPLE.md](./01-SIMPLE.md) | 7 простых улучшений (1-3 спринта каждое) | ~310 строк |
| 02 | [02-MEDIUM.md](./02-MEDIUM.md) | 8 средних улучшений (mainstream RAG) | ~440 строк |
| 03 | [03-INNOVATIVE.md](./03-INNOVATIVE.md) | 10 frontier research направлений | ~620 строк |
| 04 | [04-NOVEL.md](./04-NOVEL.md) | 10 никем не сделанных концепций | ~700 строк |
| 05 | [05-PRIORITIES.md](./05-PRIORITIES.md) | 3 стратегических пути + первые спринты | ~280 строк |

**Общий объём:** ~2700 строк структурированных планов.

---

## TL;DR per документ

### 00 — Current state
- 53 спринта, ~30 модулей, 96 batch-скриптов, 546 тестов
- Сильные слои: Retrieval (85%), Reasoning (70%), Orchestration (75%), Observability (80%)
- 10 ключевых capabilities (RAG, agent, A/B, eval, conversation, plan-execute, ...)
- 10 главных дыр (KG reasoning, cross-doc synthesis, cross-modal, active clarification, ...)

### 01 — Simple
Проверенные паттерны, 1-3 спринта, низкий риск:
- **S1** Saved searches + alerts
- **S2** Faceted search UI
- **S3** Document classification (auto-routing)
- **S4** Citation graph + PageRank
- **S5** Bulk diff queries
- **S6** Per-user preferences profile
- **S7** Read-receipt + reads tracking

### 02 — Medium
Mainstream современного RAG, 2-5 спринтов:
- **M1** Knowledge Graph extraction + reasoning
- **M2** Cross-encoder re-ranking
- **M3** Hierarchical retrieval
- **M4** Query intent classification
- **M5** Continuous online evaluation
- **M6** Active learning queue
- **M7** Incremental indexing
- **M8** Cross-modal CLIP-style embeddings

### 03 — Innovative (frontier research)
Опубликованные paper'ы, мало production реализаций, 4-8 спринтов:
- **I1** Self-RAG с reflection
- **I2** Multi-agent debate
- **I3** Provenance с confidence intervals
- **I4** Counterfactual probing (attribution map)
- **I5** Memory-augmented LLM (MemGPT-style)
- **I6** Hybrid sparse+dense+graph с learned fusion
- **I7** Bandit-allocated A/B testing
- **I8** Differential queries по времени
- **I9** Self-improving prompts (genetic algorithm)
- **I10** Hierarchical map-reduce summarization

### 04 — Novel (никем не сделано)
Концепции которые никем не упакованы в production, 6-12+ спринтов:
- **N1** Document «metabolism» — живые документы
- **N2** Negotiating retrieval (multi-agent bargaining)
- **N3** Graph-of-thoughts над корпусом
- **N4** Continual «voice» / эпистемический профиль
- **N5** Federated golden datasets с privacy
- **N6** Knowledge diffusion между корпусами
- **N7** Self-organizing taxonomy
- **N8** Counterfactual corpus («что если»)
- **N9** Personality-shaped retrieval
- **N10** Adversarial co-evolution

### 05 — Priorities
3 пути с конкретными sprint-планами:
- **Путь A — Quick value:** 12 спринтов, 3 месяца, production usability
- **Путь B — Differentiation:** 15-18 спринтов, 4-5 месяцев, конкурентное преимущество
- **Путь C — Long-game:** 8-12 спринтов в одну novel идею, 8-12 месяцев, research focus
- **Hybrid:** A → B → C по этапам, 12 месяцев общий roadmap

---

## Как читать эту серию

### Первое чтение
1. Начни с **05-PRIORITIES.md** — ответ на вопрос «что делать»
2. Если выбрал путь — читай соответствующий блок (A → 01, B → 02 + 03, C → 04)
3. **00-CURRENT-STATE.md** — для контекста («где мы стоим»)

### Второе чтение / для разработки
- Конкретный пункт (например M2 cross-encoder reranking) — иди в 02-MEDIUM.md, читай раздел
- Каждый пункт содержит: концепцию, primitives для переиспользования, sprint breakdown, API sketch, метрики, риски

### Для презентации / pitch
- Сильнее всего демо: **04-NOVEL.md** + N3 (graph-of-thoughts) — visual wow
- Investor talking points: **04-NOVEL.md** N1, N5 — patentable concepts
- Customer / user value: **02-MEDIUM.md** M2 + M5 + M6 — measurable improvements

---

## Decision flowchart

```
Есть production users?
├── Да → 05-PRIORITIES.md → Путь A → начать с S6 (per-user preferences)
└── Нет → Хочешь конкурентное отличие?
         ├── Да → 03-INNOVATIVE.md → I3 (provenance) или I1 (self-RAG)
         └── Нет → Готов к research-bet?
                  ├── Да → 04-NOVEL.md → N3 (graph-of-thoughts) для start
                  └── Нет → 02-MEDIUM.md → M2 (cross-encoder) для quality lift
```

---

## Метрики серии

| Метрика | Значение |
|---------|---------:|
| Идей описано | 35 (7+8+10+10) |
| Спринтов суммарно | ~150-220 (всё реализовать невозможно) |
| Минимальный path к value | 12-15 спринтов (Путь A) |
| Максимальный novelty | 1 идея × 8-12 спринтов (Путь C) |
| Hybrid recommended | 36-48 спринтов / 12 месяцев |

---

## Дальнейшие действия

### Если выбрал путь
→ Открой **05-PRIORITIES.md**, найди свой путь, начни первый спринт.

### Если ещё в раздумьях
→ Прочитай **00-CURRENT-STATE.md**, потом decision flowchart выше.

### Если хочешь discussions / brainstorm
→ Добавь свои идеи как N11+ в **04-NOVEL.md**, или альтернативные стратегические пути в **05-PRIORITIES.md**.

---

## Maintenance

Эта серия — snapshot на 2026-04-29 (Sprint 53). По мере реализации items нужно:
- Помечать ✅ для completed (например `S6 ✅` после реализации в Sprint 54)
- Update метрики в **00-CURRENT-STATE.md**
- Добавлять lessons learned в реализованные пункты
- Ревизию серии раз в квартал — что-то стало ясно проще, что-то сложнее

---

**Контакт:** все документы living — improvements / corrections welcome.
**Связанные доки:** `docs/INDEX.md`, `docs/HEALTH.md`, `docs/SCORING.md`, `docs/TECH_RADAR.md`.
