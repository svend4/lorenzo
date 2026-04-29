# Карта найденных проектов и паттернов

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (1).md`, раздел «Карта найденных проектов и паттернов».
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement, collaboration -->




> Источник: `deep-research-report (1).md`, раздел «Карта найденных проектов и паттернов».

Сводная таблица. Каждой строке посвящён отдельный документ в [`../components/`](../components/) — эта таблица даёт обзор, а детали — в подпапке.

| Проект или связка | Автор | Ссылка на статью и репо | Краткое описание | Ключевые компоненты и паттерны | Лицензия | Maturity / статус | Релевантность к Svyazi‑2.0 |
|---|---|---|---|---|---|---|---|
| **Svyazi** | Андрей Чуян | Хабр citeturn41search0 | Гибридная система извлечения структурированных профилей участников сообщества из свободного текста; уже показала кейс «карточек коллабораций». | 6 слоёв, YAML, SHA256‑дедупликация, Ollama+Qwen, LLM+детерминированный код, CardIndex, privacy by design. | **Код закрыт**. citeturn41search0 | Активный закрытый авторский прототип. citeturn41search0 | **Очень высокая**: это базовый ingest/normalize/discovery‑слой. |
| **knowledge-space** | Sonia_Black / AnastasiyaW | Хабр + GitHub citeturn33view0turn33view2turn37search1 | Agent‑first референсная база: 785+ карточек по 26 доменам, растущая из реальных research‑сессий. | Dense reference cards, gotchas, wiki‑links, `research/inbox/`, «для агентов, не людей». | **MIT**. citeturn33view0turn37search1 | Активный OSS, база растёт почти ежедневно. citeturn33view1turn37search1 | **Высокая**: это внешний knowledge layer для агентов и нормализатора. |
| **AgentFS** | kksudo | Хабр + GitHub citeturn33view4turn33view7turn27view0 | Превращает Obsidian‑vault в операционную систему для AI‑агентов с единым `.agentos/`‑ядром. | Compile‑to‑native configs, persistent state, security policies, memory consolidation, doctor/triage/compile CLI. | **MIT**. citeturn33view4turn27view0 | Рабочий прототип, версия 0.1.5; «рабочая, но не финальная». citeturn33view7 | **Очень высокая**: это лучший кандидат на файловое ядро Svyazi‑2.0. |
| **mclaude** | AnastasiyaW | Хабр + GitHub citeturn20view2turn37search0 | Координация нескольких сессий Claude Code и других coding‑агентов над одним проектом. | Locks, handoffs, mailbox, multi‑session turn‑taking, shared project memory. | **MIT**. citeturn37search0 | Активный OSS. citeturn37search0 | **Высокая**: решает параллельную работу модераторов/агентов над общим графом. |
| **AI Factory + AIF Handoff** | lee-to / Cutcode | Хабр + GitHub citeturn20view3turn29search0turn29search9 | Spec‑driven многоагентный development‑framework и автономный Kanban‑слой поверх него. | Skills, patches, self‑learning, worktrees, MCP handoff, plan/implement/review, WebSocket Kanban. | **MIT**. citeturn29search0turn29search9 | Активный OSS, релизы v2.x; handoff добавлен в свежих релизах. citeturn29search4 | **Высокая**: готовый оркестратор для build‑ и moderation‑контуров Svyazi‑2.0. |
| **Rufler** | zodigancode / lib4u | Хабр + repo/DEV citeturn20view4turn21view8turn32search0 | Декларативный YAML‑слой для запуска автономного роя Claude Code‑агентов. | `depends_on`, auto‑objective prompts, pause/resume, token accounting, MCP server management. | **MIT**. citeturn32search0 | Активный OSS. citeturn32search0 | **Средне‑высокая**: быстрый orchestration‑слой без тяжёлого UI. |
| **research-docs + LiteParse** | nlaik / Jerry Liu / LlamaIndex | Хабр + GitHub citeturn20view5turn15search1turn15search5turn40search0 | Forensic document QA с HTML‑отчётом и bounding boxes на страницах PDF. | Локальный парсер, spatial text parsing, visual citations, multi‑format docs, HTML evidence report. | **Apache 2.0** для LiteParse; для samples — неуточнено в просмотренных источниках. citeturn40search0turn40search1 | Активный OSS. citeturn15search1turn15search5 | **Очень высокая**: даёт visual grounding, которого Svyazi‑подобным системам обычно не хватает. |
| **Hybrid RAG knowledge base** | iximy | Хабр citeturn34view2 | Минималистский Hybrid RAG без тяжёлых фреймворков. | `pdfplumber`, координаты слов, TF‑IDF, FAISS, metadata filtering, прозрачный retrieval‑layer. | Неуточнено. citeturn34view2 | Практический implementation guide; публичный код в статье не акцентирован. citeturn34view2 | **Высокая**: полезен как быстрый базовый retrieval‑контур. |
| **Legal RAG** | tagir_analyzes | Хабр citeturn20view6 | Подробный кейс page‑level Legal RAG с 17 итерациями и измерением пределов масштабирования. | Page‑level grounding, context distillation, систематический eval loop, error analysis. | Неуточнено. citeturn20view6 | Зрелый инженерный кейс, а не только концепт. citeturn20view6 | **Очень высокая**: лучший источник для evidence‑first и audit‑friendly retrieval. |
| **Graph RAG** | VladSpace / vpakspace | Хабр + GitHub citeturn34view3turn40search2 | Графовый RAG с provenance‑trace и typed API, собранный из 5 исследовательских техник. | Skeleton Indexing, Phrase/Passage dual nodes, VectorCypher, Datalog reasoning, agentic routing. | Неуточнено. citeturn34view3turn40search2 | Активный публичный repo / production‑ready ambition. citeturn34view3turn40search2 | **Высокая**: добавляет multi‑hop retrieval и relation‑reasoning. |
| **Yodoca** | VitalyOborin | Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1 | Локальный self‑evolving AI assistant с долговременной памятью и ночной консолидацией. | Hot/slow path, private write‑path consolidator, `is_session_consolidated`, Ebbinghaus decay, causal edges, proactive memory. | **Apache 2.0**. citeturn18search1 | Активный OSS. citeturn18search1 | **Очень высокая**: лучший слой для nightly consolidation и controlled forgetting. |
| **NGT Memory** | spbmolot / ngt-memory | Хабр + GitHub/site citeturn22view4turn22view3turn32search2 | Персистентная память для LLM‑приложений с ассоциативным графом и миллисекундным retrieval overhead. | Cosine similarity + Hebbian graph + hierarchical consolidation, REST API, Docker, 2–3 ms собственных затрат. | **BSL 1.1**; в статье прямо сказано «бесплатно для личных проектов». citeturn22view5 | Активная разработка. citeturn22view3turn32search2 | **Очень высокая**: быстрый ассоциативный memory‑слой для discovery и matching. |
| **MemNet / memory-is-all-you-need** | Antipozitive | Хабр + GitHub citeturn21view4turn17search0turn18search2 | Исследовательская активная память для трансформеров. | Hebbian graph memory, STDP, spreading activation, «dreaming», anti‑forgetting. | **MIT**. citeturn17search0turn18search2 | Экспериментальный research codebase. citeturn17search0 | **Средне‑высокая**: не MVP‑слой, но сильная идея для future memory engine. |
| **agent-memory-mcp + Memory OS** | VitaliySemenov / moshael | Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 | Typed memory MCP плюс более тяжёлая концепция Memory OS с онтологией, gardener‑loop и bi‑temporal facts. | SQLite+WAL, typed memories, repo/doc search, path guard; ontology, concept loop, maintenance contour, planner/scout/synthesizer. | Для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. citeturn15search3turn39view3 | `agent-memory-mcp` — рабочий OSS; Memory OS — концептуально амбициозный кейс без явного публичного репо в статье. citeturn15search3turn39view3 | **Высокая**: слой typed memory и governance для более поздних итераций. |
| **Self‑Aware MCP + Skills + CodeWiki** | akazant / akzhankalimatov / AnastasiyaW | Хабр + repo/marketplace + Хабр/репо citeturn20view12turn30search1turn20view15turn12search2turn37search7 | Контекст реального мира для агента плюс reusable skills и авто‑документация кодовой базы. | location/time/OS tools, skill files in repo, hooks, subagents, code wiki generation. | Self‑Aware MCP — **MIT** по карточке MCP Marketplace; config‑kit — **MIT**; CodeWiki — неуточнено. citeturn30search1turn37search7turn12search2 | Активный стек инструментов. citeturn20view12turn37search7turn12search2 | **Высокая**: делает агентный слой контекстным, переносимым и предсказуемым. |
| **Voice/local-first stack** | atatchin / askid / обзоры Handy/OpenWhispr | Хабр citeturn21view10turn21view11turn21view12turn35search0 | Локальный speech→text→LLM transform и более широкий local‑first knowledge workspace с recording/transcription. | Whisper локально, Ollama post‑processing, Handy/OpenWhispr/GigaAM, live transcription, diarization, semantic links, SQLite. | Смешанная картина; для Yttri лицензия в просмотренных источниках не уточнена. citeturn35search0turn21view11 | От usable scripts до beta‑продукта. citeturn21view10turn35search0 | **Средне‑высокая**: лучший входной канал для «raw episodes» в память. |
| **Yjs + Automerge** | Kevin Jahns / Automerge team | Документация и репо citeturn11search0turn11search7turn11search13turn11search1turn11search11turn11search23 | Базовый local‑first/CRDT sync‑слой для оффлайн‑совместимости и мультидевайсной синхронизации. | Shared types, automatic merge without conflicts, offline sync, local‑first data engine. | **MIT**. citeturn11search13turn11search23 | Активный OSS. citeturn11search13turn11search11 | **Средняя**, но стратегически важная: синхронизация между устройствами и узлами. |
| **Security + routing plane** | Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig | Хабр + GitHub/docs citeturn20view10turn11search2turn19search5turn39view0turn39view1turn20view18 | Рантайм‑безопасность и бюджетный execution plane для агентных систем. | SENTINEL micro‑model swarm; LiteLLM unified API; Auto AI Router on Go; Tool Search lazy MCP loading; budget/privacy presets in RLM‑Toolkit. | Смешанная: SENTINEL — неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2.0. citeturn20view10turn19search5turn28search3 | Активный operational stack. citeturn20view10turn11search2turn39view0turn39view1 | **Очень высокая**: без этого Svyazi‑2.0 будет либо дорогой, либо небезопасной. |
| **AutoResearch + Sequential** | Андрей Карпаты / Виктория Дочкина | Хабр + GitHub/обзор citeturn20view19turn20view11 | Ночной цикл самоулучшения и протокол reviewer‑цепочки без централизованного координатора. | Edit‑run‑measure‑rollback loop, bounded experiments, sequential protocol, strong-model self‑organization. | Для AutoResearch — по статье на GitHub; лицензия в Habr‑обзоре не уточнялась. Для Sequential — исследовательская статья без OSS‑лицензии. citeturn20view19turn20view11 | Active research / practical harness. citeturn20view19turn20view11 | **Высокая**: это кандидат на self‑improvement и multi‑review для Svyazi‑2.0. |

<!-- see-also -->

---

**Смотрите также:**
- [03-component-catalog](docs/01-svyazi/03-component-catalog.md)
- [03-карта-найденных-проектов-и-паттернов](docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md)
- [04-приоритетные-ансамбли](docs/04-ai-collaborations/04-приоритетные-ансамбли.md)
- [04-ensembles-overview](docs/01-svyazi/04-ensembles-overview.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [03-component-catalog](docs/01-svyazi/03-component-catalog.md) (сходство 0.91)
- [03-карта-найденных-проектов-и-паттернов](docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) (сходство 0.90)
- [03-component-catalog](docs/obsidian/01-svyazi/03-component-catalog.md) (сходство 0.89)

