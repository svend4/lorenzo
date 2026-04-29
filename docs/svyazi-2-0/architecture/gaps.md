# Архитектурные зазоры

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (3).md`, раздел «Архитектурные зазоры, которые важнее новых инструментов».
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse

---

<!-- toc -->
## Содержание

- [Пять зазоров, важнее поиска ещё десяти инструментов](#пять-зазоров-важнее-поиска-ещё-десяти-инструментов)
- [Сводная таблица зазоров](#сводная-таблица-зазоров)
- [Главный практический принцип](#главный-практический-принцип)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, self-improvement -->




> Источник: `deep-research-report (3).md`, раздел «Архитектурные зазоры, которые важнее новых инструментов».

После первичного обзора видно, что дефицит уже не в наличии компонентов, а в **стыках между ними**. Svyazi хорошо закрывает ingest и нормализацию; AgentFS даёт `.agentos` и compile‑to‑runtime политику; knowledge-space формирует agent‑readable reference cards; NGT Memory и Yodoca решают разные режимы памяти; research-docs/LiteParse и Legal RAG решают доказуемость; LiteLLM, Auto AI Router и Tool Search — execution plane; SENTINEL и path‑guard практики — безопасность. Но именно на переходах «card ↔ memory», «memory ↔ evidence», «evidence ↔ review», «review ↔ agent execution» сегодня остаётся больше всего архитектурного риска. citeturn41search0turn27view0turn33view2turn22view4turn21view0turn20view5turn20view6turn39view0turn39view1turn20view10

## Пять зазоров, важнее поиска ещё десяти инструментов

1. **Единый тип карточки** — должен хранить и «человека», и «проект», и «эпизод», и «документ», и «слабую гипотезу».
2. **Evidence envelope** — стандарт, по которому любой вывод системы можно обратно привязать к странице, координате, фрагменту текста или истории изменения.
3. **Memory governance layer** — не даёт ассоциативной памяти записывать предлагаемое как истинное.
4. **Agent contract layer** — навыки, маршрутизация и права оформлены как исполнимые правила, а не как размазанные инструкции по разным файлам.
5. **Review protocol** — отделяет «обнаружено системой» от «принято в индекс сообщества» или «использовано во внешнем отчёте».

Каждый из этих зазоров уже частично покрыт найденными решениями, но не целиком одной системой. citeturn41search0turn20view5turn20view6turn22view4turn21view0turn20view16turn27view0turn20view3turn20view11

## Сводная таблица зазоров

| Архитектурный зазор | Уже сильные кандидаты | Что в них уже хорошо закрыто | Что пока остаётся незакрытым | Что брать в MVP |
|---|---|---|---|---|
| Карточка как единица правды | Svyazi, AgentFS | CardIndex, hash/dedup, versionable vault, persistent state | Универсальная типизация для person/project/doc/episode/hypothesis | Card schema + raw/inferred split + immutable IDs citeturn41search0turn27view0turn33view4 |
| Доказуемое основание вывода | research-docs/LiteParse, Legal RAG, Hybrid RAG | Bounding boxes, page-level grounding, coordinates, transparent retrieval | Единый формат «evidence pack» между retrieval и интерфейсом | Page-level viewer + source_id/page/span/box schema citeturn20view5turn20view6turn34view2 |
| Память с контролируемым статусом | NGT Memory, Yodoca, agent-memory-mcp, Memory OS | Associative retrieval, consolidation, forgetting, typed memory, guard rails | Чёткая граница truth/proposal/conflict/decayed | Pending queue + confidence/state machine на наполнение графа citeturn22view4turn21view0turn20view16turn39view3 |
| Оркестрация и review | mclaude, AI Factory, Rufler, Sequential | Locks, mailbox, patch learning, YAML swarm, sequential review | Стандарт handoff для non-code workflow и knowledge moderation | 2–3 роли: extractor → reviewer → publisher citeturn20view2turn20view3turn20view4turn20view11 |
| Безопасный execution plane | LiteLLM, Auto AI Router, Tool Search, SENTINEL | Unified API, lightweight routing, lazy tool loading, runtime guard | Общая policy matrix на tool classes и external skills | Read-only by default + write approval + path allowlist citeturn11search2turn39view0turn39view1turn20view10turn20view16 |

## Главный практический принцип

**Svyazi‑2.0 нужно начинать не с «самой умной модели», а с самой строгой структуры переходов между слоями.** Сильная модель без карточного статуса, Evidence Envelope и review protocol быстро превращает систему в красивый, но плохо аудитируемый генератор гипотез. Наоборот, даже средний model tier даёт много пользы, если extract/normalize/review/evidence и memory status already pinned. Это согласуется и с Svyazi‑подходом к CardIndex и privacy by design, и с Memory OS‑критикой «thoughtful but schema-breaking reasoning», и с Legal RAG‑подходом к page‑level доказуемости. citeturn41search0turn39view3turn20view6turn20view18

<!-- see-also -->

---

**Смотрите также:**
- [09-architectural-gaps](docs/01-svyazi/09-architectural-gaps.md)
- [09-архитектурные-зазоры-которые-важнее-новых-инструме](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md)
- [QA](docs/QA.md)
- [11-integration-contracts](docs/01-svyazi/11-integration-contracts.md)

