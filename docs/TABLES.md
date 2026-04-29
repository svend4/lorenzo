# Все таблицы репозитория

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

**Всего таблиц:** 518


## 01-svyazi (11 таблиц)


### 1. Шкала зрелости
_Файл: `docs/01-svyazi/02-methodology.md` | 2 колонок, 4 строк_

| Уровень | Описание |
|---------|----------|
| **Эксперимент** | Исследовательский или концептуальный код |
| **Рабочий прототип** | Можно поставить и проверить сценарий |
| **Активный OSS** | Есть явная публичная разработка, релизы или активное развитие |
| **Внутренний/закрытый прототип** | Архитектура раскрыта, но код закрыт |


### 2. Карта найденных проектов и паттернов
_Файл: `docs/01-svyazi/03-component-catalog.md` | 8 колонок, 19 строк_

| Проект или связка | Автор | Ссылка на статью и репо | Краткое описание | Ключевые компоненты и паттерны | Лицензия | Maturity / статус | Релевантность к Svyazi[^svyazi]‑2.0 |
|---|---|---|---|---|---|---|---|
| **Svyazi** | Андрей Чуян | Хабр citeturn41search0 | Гибридная система извлечения структурированных профилей участников сообщества из свободного текста; уже показала кейс «карточек коллабораций». | 6 слоёв, YAML, SHA256‑дедупликация, Ollama+Qwen, LLM[^llm]+детерминированный код, CardIndex[^cardindex], privacy by design. | **Код закрыт**. citeturn41search0 | Активный закрытый авторский прототип. citeturn41search0 | **Очень высокая**: это базовый ingest/normalize/discovery‑слой. |
| **knowledge-space** | Sonia_Black / AnastasiyaW | Хабр + GitHub citeturn33view0turn33view2turn37search1 | Agent‑first референсная база: 785+ карточек по 26 доменам, растущая из реальных research‑сессий. | Dense reference cards, gotchas, wiki‑links, `research/inbox/`, «для агентов, не людей». | **MIT**. citeturn33view0turn37search1 | Активный OSS, база растёт почти ежедневно. citeturn33view1turn37search1 | **Высокая**: это внешний knowledge layer для агентов и нормализатора. |
| **AgentFS** | kksudo | Хабр + GitHub citeturn33view4turn33view7turn27view0 | Превращает Obsidian‑vault в операционную систему для AI‑агентов с единым `.agentos/`‑ядром. | Compile‑to‑native configs, persistent state, security policies, memory consolidation, doctor/triage/compile CLI. | **MIT**. citeturn33view4turn27view0 | Рабочий прототип, версия 0.1.5; “рабочая, но не финальная”. citeturn33view7 | **Очень высокая**: это лучший кандидат на файловое ядро Svyazi‑2.0. |
| **mclaude** | AnastasiyaW | Хабр + GitHub citeturn20view2turn37search0 | Координация нескольких сессий Claude Code и других coding‑агентов над одним проектом. | Locks, handoffs, mailbox, multi‑session turn‑taking, shared project memory. | **MIT**. citeturn37search0 | Активный OSS. citeturn37search0 | **Высокая**: решает параллельную работу модераторов/агентов над общим графом. |
| **AI Factory + AIF Handoff** | lee-to / Cutcode | Хабр + GitHub citeturn20view3turn29search0turn29search9 | Spec‑driven многоагентный development‑framework и автономный Kanban‑слой поверх него. | Skills, patches, self‑learning, worktrees, MCP[^mcp] handoff, plan/implement/review, WebSocket Kanban. | **MIT**. citeturn29search0turn29search9 | Активный OSS, релизы v2.x; handoff добавлен в свежих релизах. citeturn29search4 | **Высокая**: готовый оркестратор для build‑ и moderation‑контуров Svyazi‑2.0. |
| **Rufler** | zodigancode / lib4u | Хабр + repo/DEV citeturn20view4turn21view8turn32search0 | Декларативный YAML‑слой для запуска автономного роя Claude Code‑агентов. | `depends_on`, auto‑objective prompts, pause/resume, token accounting, MCP server management. | **MIT**. citeturn32search0 | Активный OSS. citeturn32search0 | **Средне‑высокая**: быстрый orchestration‑слой без тяжёлого UI. |
| **research-docs + LiteParse** | nlaik / Jerry Liu / LlamaIndex | Хабр + GitHub citeturn20view5turn15search1turn15search5turn40search0 | Forensic document QA с HTML‑отчётом и bounding boxes на страницах PDF. | Локальный парсер, spatial text parsing, visual citations, multi‑format docs, HTML evidence report. | **Apache 2.0** для LiteParse; для samples — неуточнено в просмотренных источниках. citeturn40search0turn40search1 | Активный OSS. citeturn15search1turn15search5 | **Очень высокая**: даёт visual grounding, которого Svyazi‑подобным системам обычно не хватает. |
| **Hybrid RAG[^rag] knowledge base** | iximy | Хабр citeturn34view2 | Минималистский Hybrid RAG без тяжёлых фреймворков. | `pdfplumber`, координаты слов, TF‑IDF, FAISS, metadata filtering, прозрачный retrieval‑layer. | Неуточнено. citeturn34view2 | Практический implementation guide; публичный код в статье не акцентирован. citeturn34view2 | **Высокая**: полезен как быстрый базовый retrieval‑контур. |
| **Legal RAG** | tagir_analyzes | Хабр citeturn20view6 | Подробный кейс page‑level Legal RAG с 17 итерациями и измерением пределов масштабирования. | Page‑level grounding, context distillation, систематический eval loop, error analysis. | Неуточнено. citeturn20view6 | Зрелый инженерный кейс, а не только концепт. citeturn20view6 | **Очень высокая**: лучший источник для evidence‑first и audit‑friendly retrieval. |
| **Graph RAG** | VladSpace / vpakspace | Хабр + GitHub citeturn34view3turn40search2 | Графовый RAG с provenance‑trace и typed API, собранный из 5 исследовательских техник. | Skeleton Indexing, Phrase/Passage dual nodes, VectorCypher, Datalog reasoning, agentic routing. | Неуточнено. citeturn34view3turn40search2 | Активный публичный repo / production‑ready ambition. citeturn34view3turn40search2 | **Высокая**: добавляет multi‑hop retrieval и relation‑reasoning. |
| **Yodoca** | VitalyOborin | Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1 | Локальный self‑evolving AI assistant с долговременной памятью и ночной консолидацией. | Hot/slow path, private write‑path consolidator, `is_session_consolidated`, Ebbinghaus decay, causal edges, proactive memory. | **Apache 2.0**. citeturn18search1 | Активный OSS. citeturn18search1 | **Очень высокая**: лучший слой для nightly consolidation и controlled forgetting. |
| **NGT Memory** | spbmolot / ngt-memory | Хабр + GitHub/site citeturn22view4turn22view3turn32search2 | Персистентная память для LLM‑приложений с ассоциативным графом и миллисекундным retrieval overhead. | Cosine similarity + Hebbian graph + hierarchical consolidation, REST API, Docker, 2–3 ms собственных затрат. | **BSL 1.1**; в статье прямо сказано «бесплатно для личных проектов». citeturn22view5 | Активная разработка. citeturn22view3turn32search2 | **Очень высокая**: быстрый ассоциативный memory‑слой для discovery и matching. |
| **MemNet / memory-is-all-you-need** | Antipozitive | Хабр + GitHub citeturn21view4turn17search0turn18search2 | Исследовательская активная память для трансформеров. | Hebbian graph memory, STDP, spreading activation, “dreaming”, anti‑forgetting. | **MIT**. citeturn17search0turn18search2 | Экспериментальный research codebase. citeturn17search0 | **Средне‑высокая**: не MVP‑слой, но сильная идея для future memory engine. |
| **agent-memory-mcp + Memory OS** | VitaliySemenov / moshael | Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 | Typed memory MCP плюс более тяжёлая концепция Memory OS с онтологией, gardener‑loop и bi‑temporal facts. | SQLite+WAL, typed memories, repo/doc search, path guard; ontology, concept loop, maintenance contour, planner/scout/synthesizer. | Для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. citeturn15search3turn39view3 | `agent-memory-mcp` — рабочий OSS; Memory OS — концептуально амбициозный кейс без явного публичного репо в статье. citeturn15search3turn39view3 | **Высокая**: слой typed memory и governance для более поздних итераций. |
| **Self‑Aware MCP + Skills + CodeWiki** | akazant / akzhankalimatov / AnastasiyaW | Хабр + repo/marketplace + Хабр/репо citeturn20view12turn30search1turn20view15turn12search2turn37search7 | Контекст реального мира для агента плюс reusable skills и авто‑документация кодовой базы. | location/time/OS tools, skill files in repo, hooks, subagents, code wiki generation. | Self‑Aware MCP — **MIT** по карточке MCP Marketplace; config‑kit — **MIT**; CodeWiki — неуточнено. citeturn30search1turn37search7turn12search2 | Активный стек инструментов. citeturn20view12turn37search7turn12search2 | **Высокая**: делает агентный слой контекстным, переносимым и предсказуемым. |
| **Voice/local-first stack** | atatchin / askid / обзоры Handy/OpenWhispr | Хабр citeturn21view10turn21view11turn21view12turn35search0 | Локальный speech→text→LLM transform и более широкий local‑first knowledge workspace с recording/transcription. | Whisper локально, Ollama post‑processing, Handy/OpenWhispr/GigaAM, live transcription, diarization, semantic links, SQLite. | Смешанная картина; для Yttri лицензия в просмотренных источниках не уточнена. citeturn35search0turn21view11 | От usable scripts до beta‑продукта. citeturn21view10turn35search0 | **Средне‑высокая**: лучший входной канал для “raw episodes” в память. |
| **Yjs + Automerge** | Kevin Jahns / Automerge team | Документация и репо citeturn11search0turn11search7turn11search13turn11search1turn11search11turn11search23 | Базовый local‑first/CRDT[^crdt] sync‑слой для оффлайн‑совместимости и мультидевайсной синхронизации. | Shared types, automatic merge without conflicts, offline sync, local‑first data engine. | **MIT**. citeturn11search13turn11search23 | Активный OSS. citeturn11search13turn11search11 | **Средняя**, но стратегически важная: синхронизация между устройствами и узлами. |
| **Security + routing plane** | Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig | Хабр + GitHub/docs citeturn20view10turn11search2turn19search5turn39view0turn39view1turn20view18 | Рантайм‑безопасность и бюджетный execution plane для агентных систем. | SENTINEL[^sentinel] micro‑model swarm; LiteLLM unified API; Auto AI Router on Go; Tool Search lazy MCP loading; budget/privacy presets in RLM‑Toolkit. | Смешанная: SENTINEL — неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2.0. citeturn20view10turn19search5turn28search3 | Активный operational stack. citeturn20view10turn11search2turn39view0turn39view1 | **Очень высокая**: без этого Svyazi‑2.0 будет либо дорогой, либо небезопасной. |
| **AutoResearch + Sequential** | Андрей Карпаты / Виктория Дочкина | Хабр + GitHub/обзор citeturn20view19turn20view11 | Ночной цикл самоулучшения и протокол reviewer‑цепочки без централизованного координатора. | Edit‑run‑measure‑rollback loop, bounded experiments, sequential protocol, strong-model self‑organization. | Для AutoResearch — по статье на GitHub; лицензия в Habr‑обзоре не уточнялась. Для Sequential — исследовательская статья без OSS‑лицензии. citeturn20view19turn20view11 | Active research / practical harness. citeturn20view19turn20view11 | **Высокая**: это кандидат на self‑improvement и multi‑review для Svyazi‑2.0. |


### 3. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/01-svyazi/06-security-privacy.md` | 3 колонок, 6 строк_

| Контроль | Практический дефолт | Основание |
|---|---|---|
| Разделение tool‑классов | По умолчанию разрешать read‑only tools; любые send/write/delete/execute — только через явный approval | Автономный агент отличается от чатбота именно доступом к реальным действиям; это и создаёт катастрофы. citeturn34view5 |
| Quarantine для external skills/MCP | Любой внешний skill/MCP сначала в sandbox, потом статический/репутационный скан, потом allowlist | AI Factory прямо предупреждает о prompt injection в SKILL.md и запускает двухуровневый security scan. citeturn29search6 |
| Path allowlist | Жёстко ограничить, что агент вообще может читать и писать на диске | `agent-memory-mcp` демонстрирует хороший паттерн Path Guard/allowlist против traversal и выхода за пределы проекта. citeturn20view16 |
| PII[^pii] separation | Любые контакты, email, Telegram, ссылки — в отдельном raw‑слое; в карточки уходит только очищенный профиль | Так делает Svyazi; это правильный privacy‑baseline для людей и сообществ. citeturn41search0 |
| Truth vs Proposal | `inferred` и weak signals не писать сразу в «истину», а ставить в pending review | И Svyazi, и более тяжёлые memory‑системы сходятся на нужде в review‑контуре. citeturn41search0turn36search0 |
| Runtime firewall | Между агентом и mutating tools держать специализированный защитный слой | Именно для этого и нужен SENTINEL‑подобный слой, а не только “умный промпт”. citeturn20view10 |


### 4. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/01-svyazi/06-security-privacy.md` | 3 колонок, 6 строк_

| Этап | Дефолт | Когда эскалировать |
|---|---|---|
| Extraction из свободного текста | Локальная или дешёвая модель + строгая schema guidance | Только если extraction‑quality стабильно проваливает ваши acceptance tests |
| Нормализация | Детерминированный код | Практически никогда не переводить это на дорогую модель |
| Retrieval / rerank | Non‑LLM[^llm] hybrid retrieval или локальный reranker | При multi-hop вопросах и слабой explainability |
| Объяснение матча / summary | Средний облачный tier | Если нужен высокий stylistic quality, а не только фактология |
| Финальный внешний отчёт | Сильная модель | Только для user-facing/public/legal‑style текста |
| Ночной ресёрч / оптимизация | AutoResearch‑подход с жёстким бюджетом и rollback | Когда уже есть benchmark и понятная функция качества |


### 5. План прототипа и возможные контакты
_Файл: `docs/01-svyazi/07-mvp-planning.md` | 4 колонок, 5 строк_

| Контур | Что входит | Зачем | Оценка усилий |
|---|---|---|---|
| Ядро данных | CardIndex‑схема, профили, raw/inferred разделение, файловый vault в стиле AgentFS | Сделать единый source of truth и трассируемый lifecycle карточки | 2–3 дня |
| Ingest и память | LLM[^llm] extraction + нормализация + NGT Memory **или** Yodoca‑lite | Доказать, что из свободного текста получаются устойчивые профили и связи | 4–6 дней |
| Evidence | LiteParse/research-docs + page‑level viewer | Не просто показать match, а показать основание | 3–4 дня |
| Исполнение | LiteLLM/Auto AI Router + Tool Search + базовые правила безопасности | Удержать стоимость и не утонуть в MCP[^mcp]/context overhead | 2–3 дня |
| Guardrails | PII[^pii]‑фильтры, allowlists, manual review для inferred | Снизить риск ложных связей и утечек | 1–2 дня |


### 6. План прототипа и возможные контакты
_Файл: `docs/01-svyazi/07-mvp-planning.md` | 3 колонок, 5 строк_

| Риск | Почему это важно | Снижение риска |
|---|---|---|
| Schema drift и самовольная “оптимизация” структуры моделью | На extraction‑этапе сильная модель может начать “улучшать” схему вместо исполнения | Держать extraction на constrained schema + низком reasoning, а смысл переносить в post‑processing; это совпадает и с логикой Svyazi, и с выводами Memory OS. citeturn41search0turn39view3 |
| Ложные ассоциации в памяти | Ассоциативная память полезна, но легко порождает шум | Вводить review queue для `inferred`, разделять raw vs normalized, не писать Proposal сразу в Truth‑граф. citeturn41search0turn36search0 |
| Утечка PII в карточки и prompts | Discovery‑система почти неизбежно работает с чувствительными профилями | Повторить Svyazi‑паттерн privacy‑by‑design, хранить контакты отдельно, использовать allowlist/path guard, локальные embeddings там, где можно. citeturn41search0turn20view16turn35search0 |
| Лицензионный тупик на memory‑слое | Не все “open” memory‑решения одинаково permissive | Если нужен строго permissive/commercial‑friendly стек, NGT Memory надо проверять отдельно, потому что в статье указана BSL[^bsl] 1.1 и free‑for‑personal grant; на таком пути проще начать с Yodoca или agent-memory-mcp. citeturn22view5turn18search1turn15search3 |
| Многоагентный хаос раньше пользы | Рой даёт выгоду только после появления handoff/lock и чётких спецификаций | Начинать с mclaude + AI Factory/AIF Handoff, а Rufler/Sequential/AutoResearch добавлять после того, как появилась стабильная spec и критерии качества. citeturn20view2turn20view3turn20view4turn20view11turn20view19 |


### 7. План прототипа и возможные контакты
_Файл: `docs/01-svyazi/07-mvp-planning.md` | 4 колонок, 5 строк_

| Кому писать | Почему именно он или она | Публичный вектор из просмотренных источников | Контакт в источниках |
|---|---|---|---|
| **andrey_chuyan** | Единственный из найденных авторов, у кого уже есть рабочий кейс “карточки коллаборации” и CardIndex‑мышление. citeturn41search0 | Комментарии к статье Svyazi на Хабре. citeturn41search0 | Публичный email/Telegram в просмотренных источниках **не найден**. |
| **Sonia_Black / AnastasiyaW** | Закрывает сразу два слоя: knowledge-space и multi-session coordination через mclaude. citeturn33view3turn20view2turn37search0 | Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn33view0turn37search0 | Публичный прямой контакт **не найден**. |
| **kksudo** | Наиболее важный кандидат для слоя `.agentos/` и compile‑to‑runtime политики. citeturn33view4turn27view0 | Комментарии к статье и GitHub issues в AgentFS. citeturn33view7turn27view0 | Публичный прямой контакт **не найден**. |
| **VitalyOborin** | Сильнейший кандидат на consolidator/forgetting‑слой. citeturn21view0turn21view1turn18search1 | Комментарии к статье Yodoca и GitHub issues/discussions в repo. citeturn38view7turn18search1 | Публичный прямой контакт **не найден**. |
| **spbmolot** | Нужен для ассоциативной памяти и очень дешёвого memory retrieval с graph‑подтягиванием слабых связей. citeturn22view4turn22view5 | Комментарии к статье NGT Memory и GitHub repository. citeturn22view5turn32search2 | Публичный прямой контакт **не найден**. |


### 8. Архитектурные зазоры, которые важнее новых инструментов
_Файл: `docs/01-svyazi/09-architectural-gaps.md` | 5 колонок, 5 строк_

| Архитектурный зазор | Уже сильные кандидаты | Что в них уже хорошо закрыто | Что пока остаётся незакрытым | Что брать в MVP |
|---|---|---|---|---|
| Карточка как единица правды | Svyazi, AgentFS | CardIndex, hash/dedup, versionable vault, persistent state | Универсальная типизация для person/project/doc/episode/hypothesis | Card schema + raw/inferred split + immutable IDs citeturn41search0turn27view0turn33view4 |
| Доказуемое основание вывода | research-docs/LiteParse, Legal RAG, Hybrid RAG | Bounding boxes, page-level grounding, coordinates, transparent retrieval | Единый формат “evidence pack” между retrieval и интерфейсом | Page-level viewer + source_id/page/span/box schema citeturn20view5turn20view6turn34view2 |
| Память с контролируемым статусом | NGT Memory, Yodoca, agent-memory-mcp, Memory OS | Associative retrieval, consolidation, forgetting, typed memory, guard rails | Чёткая граница truth/proposal/conflict/decayed | Pending queue + confidence/state machine на наполнение графа citeturn22view4turn21view0turn20view16turn39view3 |
| Оркестрация и review | mclaude, AI Factory, Rufler, Sequential | Locks, mailbox, patch learning, YAML swarm, sequential review | Стандарт handoff для non-code workflow и knowledge moderation | 2–3 роли: extractor → reviewer → publisher citeturn20view2turn20view3turn20view4turn20view11 |
| Безопасный execution plane | LiteLLM, Auto AI Router, Tool Search, SENTINEL | Unified API, lightweight routing, lazy tool loading, runtime guard | Общая policy matrix на tool classes и external skills | Read-only by default + write approval + path allowlist citeturn11search2turn39view0turn39view1turn20view10turn20view16 |


### 9. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/01-svyazi/11-integration-contracts.md` | 4 колонок, 5 строк_

| Контракт | Минимальные поля | Зачем нужен в MVP | На какие идеи опирается |
|---|---|---|---|
| Card Envelope | `card_id`, `card_type`, `state`, `sources`, `edges`, `updated_at`, `payload_hash` | Единый source of truth и dedup/version trace | Svyazi, AgentFS, Memory OS citeturn41search0turn27view0turn39view3 |
| Evidence Envelope | `source_id`, `page_or_span`, `bbox_or_offset`, `method`, `confidence`, `supporting_nodes` | Проверяемость выводов и ручной review | LiteParse, Legal RAG, Hybrid/Graph RAG citeturn20view5turn20view6turn34view2turn34view3 |
| Memory Write Policy | `write_type`, `promotion_rule`, `review_required`, `decay_policy` | Развести факт, эпизод и гипотезу | Yodoca, NGT Memory, agent-memory-mcp citeturn21view0turn22view4turn20view16 |
| Skill Policy | `tool_class`, `approval_mode`, `path_scope`, `network_scope`, `output_target` | Снизить blast radius и упростить audit | Tool Search, SENTINEL, AI Factory practices citeturn39view1turn20view10turn29search6 |
| Review Record | `reviewer_role`, `decision`, `reason`, `evidence_refs`, `follow_up` | Не путать machine suggestion с accepted truth | mclaude, AI Factory, Sequential citeturn20view2turn20view3turn20view11 |


### 10. Дорожная карта прототипа следующей итерации
_Файл: `docs/01-svyazi/12-roadmap.md` | 5 колонок, 5 строк_

| Итерация | Главная цель | Минимум, который должен заработать | Оценка усилий | Главный риск |
|---|---|---|---|---|
| Evidence-first core | Из любого suggestions можно перейти к основанию | Unified cards + page/span evidence + manual reviewer UI | 1–2 недели | Переусложнение схемы слишком рано |
| Memory governance | Ассоциации перестают путаться с фактами | Episode store + proposal queue + approval/decay states | 1–2 недели | Ложная уверенность в “умной памяти” без жёсткого review |
| Agented moderation | Рой помогает, а не создаёт шум | extractor/reviewer/publisher roles + handoff/journal | 1–2 недели | Многоагентный хаос без хороших критериев качества |
| Local-first ingestion | Система начинает жить в ежедневном потоке | voice→episode, local vault, selective sync | 1–2 недели | Sync-конфликты и таскание лишних данных наружу |
| Self-improvement loop | Ошибки превращаются в benchmark и patch | benchmark set + nightly eval + rollback policy | 1 неделя на каркас, дальше непрерывно | Большой соблазн автоматизировать раньше, чем появилась метрика |


### 11. Контактная стратегия и узкие вопросы для авторов
_Файл: `docs/01-svyazi/13-contacts.md` | 3 колонок, 5 строк_

| Кому | Лучший первый вопрос | Почему именно он |
|---|---|---|
| entity["people","Андрей Чуян","habr author"] | Стоит ли расширять CardIndex до `person/project/episode/evidence`, или для discovery и moderation лучше держать разные индексы? | Это продолжает его реальную архитектурную линию, а не уводит в абстракцию. citeturn41search0 |
| **kksudo** | Что лучше класть в `.agentos`, а что выносить в machine-only state вне vault conventions? | Это вопрос в сердце AgentFS, а не общая просьба о сотрудничестве. citeturn27view0turn33view4 |
| entity["people","Виталий Оборин","software engineer"] | Что сильнее всего влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? | Это позволяет использовать Yodoca как policy reference, а не как “ещё один ассистент”. citeturn21view0turn21view1 |
| **spbmolot** | Где проходит практическая граница между полезной ассоциацией и ложной ко‑активацией тем? | Это самый важный вопрос для community matching. citeturn22view4turn22view5 |
| **авторы knowledge-space / mclaude** | Держать операционные benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? | Это шов между памятью, знаниями и orchestration. citeturn33view2turn20view2 |


## 02-anthropic-vacancies (34 таблиц)


### 1. Naming convention расшифрована
_Файл: `docs/02-anthropic-vacancies/00-intro.md` | 3 колонок, 7 строк_

| Префикс | Кол-во | Смысл |
| --- | --- | --- |
| soz* | 11 (9 private) | Соцправо/Sozialrecht — кластер #1 из data70 |
| daten* | 12 | «Данные» по-немецки, но фактически — Information OS / рационализация |
| data* | 8 | Чистые данные + legal content blocks |
| info* | 16 | Методология, RAG, архетипы, пирамиды, инфосистемы |
| meta* | 5 | Мета-проекты (монорепо, рантаймы, AST) |
| in4* | 2 | Information Flow variant |
| Именованные | 6 | nautilus, ingit, pro2, information, claudeai-test-project-k, universal-file-storage-mcp |


### 2. 2.3. Артефакты каждой фазы
_Файл: `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` | 4 колонок, 4 строк_

| Фаза | Артефакт | Место хранения | Финальность |
|------|----------|----------------|-------------|
| A | `<doc>_draft_A.md` | ветка `claude/review-XXX` | нет, промежуточное |
| B | `<doc>_draft_B.md` | ветка `claude/review-YYY` | нет, промежуточное |
| Merge | `<doc>.md` с header warning + параллельными блоками | main, с dupликацией | нет, transitional |
| C | `<doc>.md` консолидированная | main, dupликаты удалены | да, канонично |


### 3. 8.1. Trade-offs
_Файл: `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | 2 колонок, 5 строк_

| Преимущество | Оборотная сторона |
|--------------|-------------------|
| Сохранение всех insights | Transitional state выглядит messy |
| Защита от single-agent bias | Требует ручной консолидации (время) |
| Audit trail обеих версий | Увеличивает объём документа временно |
| Методологически обосновано | Read-time overhead для внешних |
| Масштабируется на team-work | Не решает проблему >2 вариантов |


### 4. Доступные инструменты
_Файл: `docs/02-anthropic-vacancies/128-доступные-инструменты.md` | 2 колонок, 7 строк_

| Tool | Назначение |
| --- | --- |
| `nautilus_query` | Поиск по всей экосистеме с consensus |
| `nautilus_query_repo` | Поиск в конкретном репо |
| `nautilus_list_repos` | Список всех адаптеров с метаданными |
| `nautilus_consensus_check` | Проверка concept agreement |
| `nautilus_describe` | Описание экосистемы (философия, версия, angles) |
| `nautilus_q6_neighbors` | Поиск Q6-соседей по Hamming distance |
| `nautilus_health` | Health score 0–100 |


### 5. Структурное сравнение: код vs гуманитарные документы
_Файл: `docs/02-anthropic-vacancies/133-обратная-связь.md` | 3 колонок, 10 строк_

| Аспект | Код/Research (текущий Nautilus) | Юридические/Социальные документы |
| --- | --- | --- |
| Единица данных | Концепт/функция/теорема | Статья закона/параграф решения/кейс |
| Native format | .py, .md, .info1, .pro2 | .pdf, .docx, .odt, .md, .rtf |
| Язык | En/Ru, технический | De (SGB, SGG), En (EU law), Ru |
| Связи | Import, reference, bridge | Статья→статья, прецедент→прецедент, учреждение→процедура |
| Авторство | Автор-разработчик | Законодатель, суд, учреждение |
| Консенсус | Концепт в N репо | Факт подтверждён N источниками |
| Q6-координата | Семантическая вершина | Категория права/социальной сферы |
| Стабильность | Меняется часто (коммиты) | Стабильна (Geltungsbereich), но с поправками |
| Timestamp-критичность | Умеренная | Критическая(Fristwahrung, Inkrafttreten) |
| Regulatory | Open-source lics | Urheberrecht, Amtliche Werke, GDPR |


### 6. 5.2. Three-Year Pilot Budget (Estimated)
_Файл: `docs/02-anthropic-vacancies/159-5-economic-model.md` | 4 колонок, 9 строк_

| Category | Year 1 | Year 2 | Year 3 |
|----------|--------|--------|--------|
| Core staff (5-8 people) | €600K | €900K | €1.2M |
| Infrastructure development | €400K | €300K | €300K |
| Contributor stipends (growing cohort) | €300K | €1.2M | €2.5M |
| Contributor bonuses | €100K | €400K | €1M |
| Legal and compliance | €150K | €200K | €300K |
| Administrative and governance | €100K | €150K | €200K |
| Community events and outreach | €100K | €150K | €250K |
| Reserve and contingency | €250K | €500K | €750K |
| **Total annual** | **€2M** | **€3.8M** | **€6.5M** |


### 7. Appendix A: Comparison Matrix Against Existing Solutions
_Файл: `docs/02-anthropic-vacancies/164-10-appendices.md` | 8 колонок, 11 строк_

| Feature | OKWF | Deel | Upwork | Toptal | Mercor | OSS Foundations | Employment |
|---------|------|------|--------|--------|--------|-----------------|------------|
| Cross-border compliance | ✓ | ✓ | Partial | ✓ | ✓ | — | — |
| Part-time capacity support | ✓ | Partial | ✓ | Partial | Partial | ✓ | ✗ |
| Dignity preservation | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Community continuity | ✓ | ✗ | ✗ | Partial | ✗ | ✓ | ✓ |
| AI-assisted coordination | ✓ | ✗ | Partial | ✗ | ✓ | ✗ | ✗ |
| Pattern library | ✓ | ✗ | ✗ | ✗ | ✗ | Partial | ✗ |
| Guild structure | ✓ | ✗ | ✗ | ✗ | ✗ | Partial | Partial |
| Reputation portability | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | Partial |
| Mission alignment | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | Varies |
| Graduated progression | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Funded baseline stipend | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |


### 8. Appendix B: Domain Comparison Matrix
_Файл: `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 5 колонок, 10 строк_

| Domain | Privacy Sensitivity | Adversarial Risk | Regulatory Complexity | Deployment Readiness |
|--------|--------------------|--------------------|----------------------|----------------------|
| 1. Knowledge Workers | Medium | Low | Low | High |
| 2. Retired Professionals | Low | Low | Low | High |
| 3. Social Workers | High | Medium | Medium | Medium |
| 4. Vulnerable Citizens | High | High | High | Medium |
| 5. Caregivers | High | Low | High | Medium |
| 6. Small Business | Low | Medium | Medium | Medium |
| 7. Patients | Highest | Medium | Highest | Medium-Low |
| 8. Students | Low | Low | Low | Medium |
| 9. Communities | Medium | High | High | Medium-Low |
| 10. Future Generations | N/A | Highest | Highest | Low |


### 9. Приложение B: Матрица Сравнения Областей
_Файл: `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 5 колонок, 10 строк_

| Область | Чувствительность Конфиденциальности | Состязательный Риск | Регулятивная Сложность | Готовность к Развёртыванию |
|---------|-------------------------------------|---------------------|------------------------|----------------------------|
| 1. Работники Знаний | Средняя | Низкая | Низкая | Высокая |
| 2. Профессионалы на Пенсии | Низкая | Низкая | Низкая | Высокая |
| 3. Социальные Работники | Высокая | Средняя | Средняя | Средняя |
| 4. Уязвимые Граждане | Высокая | Высокая | Высокая | Средняя |
| 5. Опекуны | Высокая | Низкая | Высокая | Средняя |
| 6. Малый Бизнес | Низкая | Средняя | Средняя | Средняя |
| 7. Пациенты | Наивысшая | Средняя | Наивысшая | Средняя-Низкая |
| 8. Студенты | Низкая | Низкая | Низкая | Средняя |
| 9. Сообщества | Средняя | Высокая | Высокая | Средняя-Низкая |
| 10. Будущие Поколения | Н/Д | Наивысшая | Наивысшая | Низкая |


### 10. 1.7. Why This Distinction Matters
_Файл: `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | 6 колонок, 7 строк_

| Property | Type 0 | Type 1 | Type 2 | Type 3 | Type 4 |
|----------|--------|--------|--------|--------|--------|
| Specialization | None | Profession | Institution+profession | Task | Individual |
| External communication | None | None | Some | Some | Extensive |
| Replicability | Universal | Per profession | Per institution | Per task | Per individual |
| Economics | Subscription | Profession-wide | Institutional | Variable | Individual |
| Ethical concerns | Low | Medium | Medium | High | Highest |
| Regulatory complexity | Low | Medium | High | Highest | Highest |
| Deployment readiness | Mature | Emerging | Early | Beginning | Conceptual |


### 11. 3.3. Deployment Trajectory
_Файл: `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | 2 колонок, 3 строк_

| Date | Status |
|------|--------|
| Summer 2025 | Development begins |
| September 2025 | Public launch |
| April 2026 | 93,000 active teacher users |


### 12. Appendix A: Comparative Table — Five Agent Types
_Файл: `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | 6 колонок, 12 строк_

| Property | Type 0: Personal AI Assistant | Type 1: Professional Colleague | Type 2: Institutional | Type 3: Employee | Type 4: Representative |
|----------|---|---|---|---|---|
| **Specialization** | None (general) | Single profession | Profession + institution | Specific task | Specific individual |
| **Direction** | Reactive | Reactive (within profession) | Bidirectional | Autonomous in scope | Outward (to world) |
| **External communication** | None | None | Some (institutional) | Some (delegated) | Extensive |
| **Persistence** | Session | Professional context | Institutional records | Ongoing operation | Long-term life arc |
| **Replicability** | Universal product | One per profession | One per institution-type | Per task | Per individual |
| **Economics** | Subscription | Profession-wide | Institutional license | Variable | Individual or foundation |
| **Ethical concerns** | Low | Medium (mediation, standardization) | Medium (institutional power) | High (autonomy, liability) | Highest (representation, agency) |
| **Regulatory complexity** | Low | Medium (profession regs) | High (institutional regs) | Highest (delegation law) | Highest (representation law) |
| **Knowledge depth** | None | Deep (profession) | Deep + institutional | Deep (specific task) | Deep (individual) |
| **Practitioner authority** | Full | Full | Full + institutional check | Delegated zone | Strategic delegation |
| **Reference example** | ChatGPT | «Обучай» | Hospital EHR-integrated | Insurance claim AI | Proposed (none) |
| **Maturity (2026)** | Mature | Emerging | Early | Beginning | Conceptual |


### 13. 1.7. Почему это различение важно
_Файл: `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | 6 колонок, 7 строк_

| Свойство | Тип 0 | Тип 1 | Тип 2 | Тип 3 | Тип 4 |
|----------|-------|-------|-------|-------|-------|
| Специализация | Нет | Профессия | Институция+профессия | Задача | Личность |
| Внешние коммуникации | Нет | Нет | Некоторые | Некоторые | Обширные |
| Тиражируемость | Универсальная | По профессии | По институции | По задаче | По индивиду |
| Экономика | Подписка | По профессии | Институциональная | Различная | Индивидуальная |
| Этические вопросы | Низкие | Средние | Средние | Высокие | Высочайшие |
| Регуляторная сложность | Низкая | Средняя | Высокая | Высочайшая | Высочайшая |
| Готовность к развёртыванию | Зрелая | Появляющаяся | Ранняя | Начинающаяся | Концептуальная |


### 14. 3.3. Траектория развёртывания
_Файл: `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | 2 колонок, 3 строк_

| Дата | Статус |
|------|--------|
| Лето 2025 | Начало разработки |
| Сентябрь 2025 | Публичный запуск |
| Апрель 2026 | 93 000 активных учителей-пользователей |


### 15. Приложение A: Сравнительная Таблица — Пять Типов Агентов
_Файл: `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | 6 колонок, 12 строк_

| Свойство | Тип 0: Персональный AI | Тип 1: Профессиональный Коллега | Тип 2: Институциональный | Тип 3: Сотрудник | Тип 4: Представительский |
|----------|---|---|---|---|---|
| **Специализация** | Нет (общий) | Одна профессия | Профессия + институция | Конкретная задача | Конкретный индивид |
| **Направление** | Реактивный | Реактивный (в профессии) | Двунаправленный | Автономный в зоне | Внешний (к миру) |
| **Внешние коммуникации** | Нет | Нет | Некоторые (институциональные) | Некоторые (делегированные) | Обширные |
| **Постоянство** | Сессия | Профессиональный контекст | Институциональные записи | Постоянная работа | Долгосрочная жизненная траектория |
| **Тиражируемость** | Универсальный продукт | Один на профессию | Один на тип институции | По задаче | По индивиду |
| **Экономика** | Подписка | По всей профессии | Институциональная лицензия | Различная | Индивидуальная или фондом |
| **Этические озабоченности** | Низкие | Средние (опосредование, стандартизация) | Средние (институциональная власть) | Высокие (автономия, ответственность) | Высочайшие (представительство, действующая сила) |
| **Регуляторная сложность** | Низкая | Средняя (профессиональные регуляции) | Высокая (институциональные регуляции) | Высочайшая (право делегирования) | Высочайшая (право представительства) |
| **Глубина знаний** | Нет | Глубокая (профессия) | Глубокая + институциональная | Глубокая (конкретная задача) | Глубокая (индивид) |
| **Полномочия практикующего** | Полные | Полные | Полные + институциональная проверка | Делегированная зона | Стратегическое делегирование |
| **Референсный пример** | ChatGPT | «Обучай» | Больничная EHR-интегрированная | AI страховых претензий | Предложен (нет) |
| **Зрелость (2026)** | Зрелый | Появляющийся | Ранний | Начинающийся | Концептуальный |


### 16. Appendix A: The Six-Type Taxonomy (Updated)
_Файл: `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | 5 колонок, 6 строк_

| Type | Name | Specialization | Example | Maturity |
|------|------|----------------|---------|----------|
| 0 | Personal AI Assistant | None (general) | ChatGPT, Claude | Mature |
| 1 | Professional Colleague Agent | Single profession | «Обучай» for teachers | Emerging |
| **1.5** | **Composite Skills Agent** | **Configurable ensemble** | **Proposed** | **Proposed** |
| 2 | Institutional Agent | Profession + institution | Hospital EHR-integrated | Early |
| 3 | Employee Agent | Specific delegated task | Insurance claim AI | Beginning |
| 4 | Representative Agent | Single individual | Proposed (none yet) | Conceptual |


### 17. Appendix B: Comparison Matrix
_Файл: `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | 5 колонок, 9 строк_

| Capability | Plain Folder + Cowork | InGit + Cowork | Notion | Obsidian + AI plugins |
|-----------|----------------------|----------------|--------|----------------------|
| Structured organization | Manual | Conventional | Database | Markdown files |
| Versioning | Manual Git | Git native | Internal | Git via plugin |
| Metadata | None | YAML | Properties | Frontmatter |
| Validation | None | Hooks | UI rules | Plugin-dependent |
| Encryption | None | Built-in | Limited | Plugin-dependent |
| Offline | Yes | Yes | Limited | Yes |
| AI integration | Cowork | Cowork + InGit MCP | Notion AI | Plugin-dependent |
| Cross-platform | OS-dependent | Yes | Yes | Yes |
| Cost | Cowork sub | Free + Cowork | Subscription | Free + plugins |


### 18. Приложение B: Сравнительная Матрица
_Файл: `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | 5 колонок, 9 строк_

| Способность | Обычная Папка + Cowork | InGit + Cowork | Notion | Obsidian + AI плагины |
|-----------|----------------------|----------------|--------|----------------------|
| Структурированная организация | Ручная | Конвенциональная | База данных | Markdown файлы |
| Версионирование | Ручной Git | Git-нативное | Внутреннее | Git через плагин |
| Метаданные | Нет | YAML | Свойства | Frontmatter |
| Валидация | Нет | Хуки | UI правила | Зависит от плагина |
| Шифрование | Нет | Встроенное | Ограниченное | Зависит от плагина |
| Оффлайн | Да | Да | Ограниченно | Да |
| AI интеграция | Cowork | Cowork + InGit MCP | Notion AI | Зависит от плагина |
| Кросс-платформенность | Зависит от ОС | Да | Да | Да |
| Стоимость | Подписка Cowork | Бесплатно + Cowork | Подписка | Бесплатно + плагины |


### 19. Что это такое в эссенции
_Файл: `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | 3 колонок, 6 строк_

| Узел pipeline | Проект | Статус |
| --- | --- | --- |
| Habr Scout | Firecrawl + Playwright + Свяжи extraction | Working components |
| Svyazi-like карточки | Свяжи (Чуян) + knowledge-space (Анастасия) | Working |
| Collaboration Knowledge OS | AgentFS + Memory OS + knowledge-space | Working |
| Agent Team Kernel | Rufler + agent-pool + mclaude (Анастасия) | Working |
| Forensic RAG | LiteParse + Hybrid RAG + Graph RAG | Working |
| Secure Agent Runtime | SENTINEL + Shield + Claude permissions | Working |


### 20. Synthesizing с нашим existing landscape
_Файл: `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 5 колонок, 10 строк_

| Person | Project(s) | License | Status | Layer in Stack |
| --- | --- | --- | --- | --- |
| Анастасия Бутова | mclaude + knowledge-space | MIT + MIT | Active | Layers 2 & 6 |
| kagvi13 | HMP | unverified | Active | Federation (cross-cutting) |
| Андрей Чуян | Svyazi | Closed | Active | Layer 1 |
| VitalyOborin | Yodoca | Apache 2.0 | Active | Layer 4 |
| kksudo | AgentFS | MIT | Active | Layer 3 |
| spbmolot | NGT Memory | BSL 1.1 | Active | Layer 4 (alt) |
| lee-to / Cutcode | AI Factory | MIT | Active | Layer 6 |
| lib4u | Rufler | MIT | Active | Layer 6 (alt) |
| moshael | Memory OS | concept | Concept | Layer 4 (theory) |
| akazant | Self-Aware MCP | MIT | Active | Layer 7 |


### 21. Что это за документ — диагностика
_Файл: `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 3 колонок, 5 строк_

| Аспект | Первый survey | Этот документ |
| --- | --- | --- |
| Фокус | Components | Joints/contracts между components |
| Уровень | Inventory | Architecture |
| Вопрос | «Что есть?» | «Что между ними?» |
| Output | Список и сравнение | Integration contracts |
| Stage | Discovery | Specification |


### 22. Что критически нового добавляет этот документ
_Файл: `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 3 колонок, 5 строк_

| Итерация | Цель | Время |
| --- | --- | --- |
| 1: Evidence-first core | Suggestions → evidence | 1-2 weeks |
| 2: Memory governance | Truth vs proposal | 1-2 weeks |
| 3: Agented moderation | Roles: extractor/reviewer/publisher | 1-2 weeks |
| 4: Local-first ingestion | Voice → episode → vault | 1-2 weeks |
| 5: Self-improvement loop | Errors → benchmarks → patches | Continuous |


### 23. Эталонная экосистема: svend4
_Файл: `docs/02-anthropic-vacancies/67-о-проекте.md` | 4 колонок, 3 строк_

| Репо | Формат | Содержание | Угол зрения |
| --- | --- | --- | --- |
| [info1](https://github.com/svend4/info1) | `.info1` | 74 документа с α-уровнями | Методологический |
| [pro2](https://github.com/svend4/pro2) | `.pro2` | Q6-граф концептов, 64 вершины | Семантический |
| [meta](https://github.com/svend4/meta) | `.meta` | 256 CA-правил + 64 гексаграммы | Символьный |


### 24. Reference Ecosystem: svend4
_Файл: `docs/02-anthropic-vacancies/68-about.md` | 4 колонок, 3 строк_

| Repo | Format | Content | Perspective |
| --- | --- | --- | --- |
| [info1](https://github.com/svend4/info1) | `.info1` | 74 documents with α-levels | Methodological |
| [pro2](https://github.com/svend4/pro2) | `.pro2` | Q6-graph, 64 vertices | Semantic |
| [meta](https://github.com/svend4/meta) | `.meta` | 256 CA rules + 64 hexagrams | Symbolic |


### 25. Практические рекомендации для вашего метода
_Файл: `docs/02-anthropic-vacancies/69-section.md` | 2 колонок, 0 строк_

| LOC | 6782 |
| Tests | 60 / 769 строк |


### 26. Практические рекомендации для вашего метода
_Файл: `docs/02-anthropic-vacancies/69-section.md` | 2 колонок, 0 строк_

| LOC | 6600 |
| Tests | 60 / 415 строк |


### 27. Метрики (сравнение двух независимых анализов)
_Файл: `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | 4 колонок, 5 строк_

| Метрика | Вариант A ([tdywx@abc123](link)) | Вариант B ([CzylE@def456](link)) | Статус сверки |
|---------|-----------|-----------|---------------|
| Python LOC | 6782 | 6600 | ⚠️ расходится — требует верификации |
| Tests | 60 | 60 | ✅ согласовано |
| Test lines | 769 | 415 | ⚠️ расходится — требует верификации |
| mypy errors | 0 | 0 | ✅ согласовано |
| Паспортов | 7 | 7 | ✅ согласовано |


### 28. Паспорт: /
_Файл: `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | / |
| Формат | `.` — краткое описание |
| Единица | что является одной записью |
| Адаптер | `adapters/.py` |
| Уровень совместимости | <0-3> —  |


### 29. 8.3. Q6 Mapping Rules
_Файл: `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` | 2 колонок, 4 строк_

| Format | Правило |
|--------|---------|
| `info1` | `alpha + 4` → 3 старших бита, остальные биты по категории |
| `pro2` | нативные Q6-координаты (Q6 — первичный концепт pro2) |
| `meta` | `hex_id - 1 → bin(6)` (гексаграмма 1 → `000000`, 64 → `111111`) |
| `data7` | `порядковый номер % 64 → bin(6)` |


### 30. 12.6. Path Selection Guidance
_Файл: `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | 2 колонок, 5 строк_

| Вариант | Когда использовать |
|---------|-------------------|
| **A** | Когда хорошо знаете структуру Repo и хотите high-quality |
| **B** | Стартовая точка для большинства новых Repos |
| **C** | Для Repos, которые автор хочет сам декларировать |
| **D** | Для быстрой первой интеграции незнакомых Repos |
| **E** | Для автоматической fleet-federation многих Repos |


### 31. 13.1. Required Endpoints
_Файл: `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | 3 колонок, 3 строк_

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/query?q=<text>&ranked=<0\|1>` | Поиск концептов |
| GET | `/api/describe` | Описание всех адаптеров |
| GET | `/api/health` | Состояние экосистемы (score 0–100) |


### 32. 13.1. Required Endpoints
_Файл: `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | 3 колонок, 4 строк_

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/links` | Валидация кросс-ссылок |
| GET | `/api/neighbors?q6=<bits>&dist=<N>` | Q6-соседи |
| GET | `/metrics` | Prometheus-метрики (text/plain) |
| GET | `/` | Root endpoint со списком endpoints |


### 33. 18.1. Current Reference Implementation Metrics
_Файл: `docs/02-anthropic-vacancies/93-18-reference-implementation.md` | 2 колонок, 7 строк_

| Метрика | Значение |
|---------|----------|
| Python LOC | 6 782 |
| Адаптеров | 13 (7 реестровых + 6 расширенных) |
| Тестов | 60 / 60 passing |
| mypy errors | 0 |
| Внешних зависимостей | 0 (stdlib only) |
| Health Score | 82 / 100 |
| Q6 coverage (real) | 21.9% (14 / 64 vertices) |


### 34. Паспорт: owner/my-notes
_Файл: `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | owner/my-notes |
| Формат | `.md` — Markdown notes |
| Единица | Markdown-документ |
| Адаптер | `adapters/my_notes.py` |
| Уровень совместимости | 1 — читаемый |


## 03-technology-combinations (1 таблиц)


### 1. 📊Сводная таблица синергии
_Файл: `docs/03-technology-combinations/05-benchmarks.md` | 4 колонок, 8 строк_

| Комбинация | Кубики | Уникальный результат | Экономия/ROI |
| --- | --- | --- | --- |
| 1 | Агентская архитектура + Svyazi | Самообучающиеся промпты, multi-domain профилирование | 70% времени на модерацию |
| 2 | Мультиагенты + Router | Иерархический роутинг, fault tolerance | 80% бюджета на LLM |
| 3 | CRDT + Svyazi | P2P граф сообщества, offline-first discovery | Нулевые расходы на сервер |
| 4 | LLM-парсинг + Graph-RAG + Агенты | Self-building knowledge graph | 95% точность vs 60% обычного RAG |
| 5 | SourceCraft + Claude Code + Sequential | Distributed code review, team knowledge graph | 44% выше качества vs координатор |
| 6 | OpenClaude + ZINC + MoME | Локальный агент с Q6-роутером | 100% privacy, $0/мес API |
| 7 | Crawl4AI + Docling + Yodoca | Self-consolidating legal corpus | Автоматическая актуализация |
| 8 | Conductor + adversarial + Router | Multi-model adversarial, enterprise review | 3× ускорение ревью |


## 04-ai-collaborations (38 таблиц)


### 1. Статус
_Файл: `docs/04-ai-collaborations/00-intro.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 2. Статус
_Файл: `docs/04-ai-collaborations/01-executive-summary.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 3. Статус
_Файл: `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 4. Статус
_Файл: `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 5. Карта найденных проектов и паттернов
_Файл: `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 2 строк_

| Проект или связка | Автор | Ссылка на статью и репо | Краткое описание | Ключевые компоненты и паттерны | Лицензия | Maturity / статус | Релевантность к Svyazi‑2.0 |
|---|---|---|---|---|---|---|---|
| **Svyazi** | Андрей Чуян | Хабр citeturn41search0 | Гибридная система извлечения структурированных профилей участников сообщества из свободного текста; уже показала кейс «карточек коллабораций». | 6 слоёв, YAML, SHA256‑дедупликация, Ollama+Qwen, LLM[^llm]+детерминированный код, CardIndex, privacy by design. | **Код закрыт**. citeturn41search0 | Активный закрытый авторский прототип. citeturn41search0 | **Очень высокая**: это базовый ingest/normalize/discovery‑слой. |
| **knowledge-space** | Sonia_Black / AnastasiyaW | Хабр + GitHub citeturn33view0turn33view2turn37search1 | Agent‑first референсная база: 785+ карточек по 26 доменам, растущая из реальных research‑сессий. | Dense reference cards, gotchas, wiki‑links,


### 6. Карта найденных проектов и паттернов
_Файл: `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 1 строк_

| **mclaude** | AnastasiyaW | Хабр + GitHub citeturn20view2turn37search0 | Координация нескольких сессий Claude Code и других coding‑агентов над одним проектом. | Locks, handoffs, mailbox, multi‑session turn‑taking, shared project memory. | **MIT**. citeturn37search0 | Активный OSS. citeturn37search0 | **Высокая**: решает параллельную работу модераторов/агентов над общим графом. |
| **AI Factory + AIF Handoff** | lee-to / Cutcode | Хабр + GitHub citeturn20view3turn29search0turn29search9 | Spec‑driven многоагентный development‑framework и автономный Kanban‑слой поверх него. | Skills, patches, self‑learning, worktrees, MCP[^mcp] handoff, plan/implement/review, WebSocket Kanban. | **MIT**. citeturn29search0turn29search9 | Активный OSS, релизы v2.x; handoff добавлен в свежих релизах. citeturn29search4 | **Высокая**: готовый оркестратор для build‑ и moderation‑контуров Svyazi‑2.0. |
| **Rufler** | zodigancode / lib4u | Хабр + repo/DEV citeturn20view4turn21view8turn32search0 | Декларативный YAML‑слой для запуска автономного роя Claude Code‑агентов. |


### 7. Карта найденных проектов и паттернов
_Файл: `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 0 строк_

| **research-docs + LiteParse** | nlaik / Jerry Liu / LlamaIndex | Хабр + GitHub citeturn20view5turn15search1turn15search5turn40search0 | Forensic document QA с HTML‑отчётом и bounding boxes на страницах PDF. | Локальный парсер, spatial text parsing, visual citations, multi‑format docs, HTML evidence report. | **Apache 2.0** для LiteParse; для samples — неуточнено в просмотренных источниках. citeturn40search0turn40search1 | Активный OSS. citeturn15search1turn15search5 | **Очень высокая**: даёт visual grounding, которого Svyazi‑подобным системам обычно не хватает. |
| **Hybrid RAG[^rag] knowledge base** | iximy | Хабр citeturn34view2 | Минималистский Hybrid RAG без тяжёлых фреймворков. |


### 8. Карта найденных проектов и паттернов
_Файл: `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 1 строк_

| **Legal RAG** | tagir_analyzes | Хабр citeturn20view6 | Подробный кейс page‑level Legal RAG с 17 итерациями и измерением пределов масштабирования. | Page‑level grounding, context distillation, систематический eval loop, error analysis. | Неуточнено. citeturn20view6 | Зрелый инженерный кейс, а не только концепт. citeturn20view6 | **Очень высокая**: лучший источник для evidence‑first и audit‑friendly retrieval. |
| **Graph RAG** | VladSpace / vpakspace | Хабр + GitHub citeturn34view3turn40search2 | Графовый RAG с provenance‑trace и typed API, собранный из 5 исследовательских техник. | Skeleton Indexing, Phrase/Passage dual nodes, VectorCypher, Datalog reasoning, agentic routing. | Неуточнено. citeturn34view3turn40search2 | Активный публичный repo / production‑ready ambition. citeturn34view3turn40search2 | **Высокая**: добавляет multi‑hop retrieval и relation‑reasoning. |
| **Yodoca** | VitalyOborin | Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1 | Локальный self‑evolving AI assistant с долговременной памятью и ночной консолидацией. | Hot/slow path, private write‑path consolidator,


### 9. Карта найденных проектов и паттернов
_Файл: `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 1 строк_

| **NGT Memory** | spbmolot / ngt-memory | Хабр + GitHub/site citeturn22view4turn22view3turn32search2 | Персистентная память для LLM‑приложений с ассоциативным графом и миллисекундным retrieval overhead. | Cosine similarity + Hebbian graph + hierarchical consolidation, REST API, Docker, 2–3 ms собственных затрат. | **BSL 1.1**; в статье прямо сказано «бесплатно для личных проектов». citeturn22view5 | Активная разработка. citeturn22view3turn32search2 | **Очень высокая**: быстрый ассоциативный memory‑слой для discovery и matching. |
| **MemNet / memory-is-all-you-need** | Antipozitive | Хабр + GitHub citeturn21view4turn17search0turn18search2 | Исследовательская активная память для трансформеров. | Hebbian graph memory, STDP, spreading activation, “dreaming”, anti‑forgetting. | **MIT**. citeturn17search0turn18search2 | Экспериментальный research codebase. citeturn17search0 | **Средне‑высокая**: не MVP‑слой, но сильная идея для future memory engine. |
| **agent-memory-mcp + Memory OS** | VitaliySemenov / moshael | Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 | Typed memory MCP плюс более тяжёлая концепция Memory OS с онтологией, gardener‑loop и bi‑temporal facts. | SQLite+WAL, typed memories, repo/doc search, path guard; ontology, concept loop, maintenance contour, planner/scout/synthesizer. | Для


### 10. Карта найденных проектов и паттернов
_Файл: `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 3 строк_

| **Self‑Aware MCP + Skills + CodeWiki** | akazant / akzhankalimatov / AnastasiyaW | Хабр + repo/marketplace + Хабр/репо citeturn20view12turn30search1turn20view15turn12search2turn37search7 | Контекст реального мира для агента плюс reusable skills и авто‑документация кодовой базы. | location/time/OS tools, skill files in repo, hooks, subagents, code wiki generation. | Self‑Aware MCP — **MIT** по карточке MCP Marketplace; config‑kit — **MIT**; CodeWiki — неуточнено. citeturn30search1turn37search7turn12search2 | Активный стек инструментов. citeturn20view12turn37search7turn12search2 | **Высокая**: делает агентный слой контекстным, переносимым и предсказуемым. |
| **Voice/local-first stack** | atatchin / askid / обзоры Handy/OpenWhispr | Хабр citeturn21view10turn21view11turn21view12turn35search0 | Локальный speech→text→LLM transform и более широкий local‑first knowledge workspace с recording/transcription. | Whisper локально, Ollama post‑processing, Handy/OpenWhispr/GigaAM, live transcription, diarization, semantic links, SQLite. | Смешанная картина; для Yttri лицензия в просмотренных источниках не уточнена. citeturn35search0turn21view11 | От usable scripts до beta‑продукта. citeturn21view10turn35search0 | **Средне‑высокая**: лучший входной канал для “raw episodes” в память. |
| **Yjs + Automerge** | Kevin Jahns / Automerge team | Документация и репо citeturn11search0turn11search7turn11search13turn11search1turn11search11turn11search23 | Базовый local‑first/CRDT[^crdt] sync‑слой для оффлайн‑совместимости и мультидевайсной синхронизации. | Shared types, automatic merge without conflicts, offline sync, local‑first data engine. | **MIT**. citeturn11search13turn11search23 | Активный OSS. citeturn11search13turn11search11 | **Средняя**, но стратегически важная: синхронизация между устройствами и узлами. |
| **Security + routing plane** | Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig | Хабр + GitHub/docs citeturn20view10turn11search2turn19search5turn39view0turn39view1turn20view18 | Рантайм‑безопасность и бюджетный execution plane для агентных систем. | SENTINEL[^sentinel] micro‑model swarm; LiteLLM unified API; Auto AI Router on Go; Tool Search lazy MCP loading; budget/privacy presets in RLM‑Toolkit. | Смешанная: SENTINEL — неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2.0. citeturn20view10turn19search5turn28search3 | Активный operational stack. citeturn20view10turn11search2turn39view0turn39view1 | **Очень высокая**: без этого Svyazi‑2.0 будет либо дорогой, либо небезопасной. |
| **AutoResearch + Sequential** | Андрей Карпаты / Виктория Дочкина | Хабр + GitHub/обзор citeturn20view19turn20view11 | Ночной цикл самоулучшения и протокол reviewer‑цепочки без централизованного координатора. | Edit‑run‑measure‑rollback loop, bounded experiments, sequential protocol, strong-model self‑organization. | Для AutoResearch — по статье на GitHub; лицензия в Habr‑обзоре не уточнялась. Для Sequential — исследовательская статья без OSS‑лицензии. citeturn20view19turn20view11 | Active research / practical harness. citeturn20view19turn20view11 | **Высокая**: это кандидат на self‑improvement и multi‑review для Svyazi‑2.0. |


### 11. Статус
_Файл: `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 12. Статус
_Файл: `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 13. План прототипа и возможные контакты
_Файл: `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 4 колонок, 5 строк_

| Контур | Что входит | Зачем | Оценка усилий |
|---|---|---|---|
| Ядро данных | CardIndex‑схема, профили, raw/inferred разделение, файловый vault в стиле AgentFS | Сделать единый source of truth и трассируемый lifecycle карточки | 2–3 дня |
| Ingest и память | LLM[^llm] extraction + нормализация + NGT Memory **или** Yodoca‑lite | Доказать, что из свободного текста получаются устойчивые профили и связи | 4–6 дней |
| Evidence | LiteParse/research-docs + page‑level viewer | Не просто показать match, а показать основание | 3–4 дня |
| Исполнение | LiteLLM/Auto AI Router + Tool Search + базовые правила безопасности | Удержать стоимость и не утонуть в MCP[^mcp]/context overhead | 2–3 дня |
| Guardrails | PII[^pii]‑фильтры, allowlists, manual review для inferred | Снизить риск ложных связей и утечек | 1–2 дня |


### 14. План прототипа и возможные контакты
_Файл: `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 3 колонок, 2 строк_

| Риск | Почему это важно | Снижение риска |
|---|---|---|
| Schema drift и самовольная “оптимизация” структуры моделью | На extraction‑этапе сильная модель может начать “улучшать” схему вместо исполнения | Держать extraction на constrained schema + низком reasoning, а смысл переносить в post‑processing; это совпадает и с логикой Svyazi, и с выводами Memory OS. citeturn41search0turn39view3 |
| Ложные ассоциации в памяти | Ассоциативная память полезна, но легко порождает шум | Вводить review queue для


### 15. План прототипа и возможные контакты
_Файл: `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 3 колонок, 1 строк_

| Утечка PII в карточки и prompts | Discovery‑система почти неизбежно работает с чувствительными профилями | Повторить Svyazi‑паттерн privacy‑by‑design, хранить контакты отдельно, использовать allowlist/path guard, локальные embeddings там, где можно. citeturn41search0turn20view16turn35search0 |
| Лицензионный тупик на memory‑слое | Не все “open” memory‑решения одинаково permissive | Если нужен строго permissive/commercial‑friendly стек, NGT Memory надо проверять отдельно, потому что в статье указана BSL[^bsl] 1.1 и free‑for‑personal grant; на таком пути проще начать с Yodoca или agent-memory-mcp. citeturn22view5turn18search1turn15search3 |
| Многоагентный хаос раньше пользы | Рой даёт выгоду только после появления handoff/lock и чётких спецификаций | Начинать с mclaude + AI Factory/AIF Handoff, а Rufler/Sequential/AutoResearch добавлять после того, как появилась стабильная spec и критерии качества. citeturn20view2turn20view3turn20view4turn20view11turn20view19 |


### 16. План прототипа и возможные контакты
_Файл: `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 4 колонок, 3 строк_

| Кому писать | Почему именно он или она | Публичный вектор из просмотренных источников | Контакт в источниках |
|---|---|---|---|
| **andrey_chuyan** | Единственный из найденных авторов, у кого уже есть рабочий кейс “карточки коллаборации” и CardIndex‑мышление. citeturn41search0 | Комментарии к статье Svyazi на Хабре. citeturn41search0 | Публичный email/Telegram в просмотренных источниках **не найден**. |
| **Sonia_Black / AnastasiyaW** | Закрывает сразу два слоя: knowledge-space и multi-session coordination через mclaude. citeturn33view3turn20view2turn37search0 | Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn33view0turn37search0 | Публичный прямой контакт **не найден**. |
| **kksudo** | Наиболее важный кандидат для слоя


### 17. План прототипа и возможные контакты
_Файл: `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 4 колонок, 0 строк_

| **VitalyOborin** | Сильнейший кандидат на consolidator/forgetting‑слой. citeturn21view0turn21view1turn18search1 | Комментарии к статье Yodoca и GitHub issues/discussions в repo. citeturn38view7turn18search1 | Публичный прямой контакт **не найден**. |
| **spbmolot** | Нужен для ассоциативной памяти и очень дешёвого memory retrieval с graph‑подтягиванием слабых связей. citeturn22view4turn22view5 | Комментарии к статье NGT Memory и GitHub repository. citeturn22view5turn32search2 | Публичный прямой контакт **не найден**. |


### 18. Статус
_Файл: `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 19. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 3 колонок, 3 строк_

| Контроль | Практический дефолт | Основание |
|---|---|---|
| Разделение tool‑классов | По умолчанию разрешать read‑only tools; любые send/write/delete/execute — только через явный approval | Автономный агент отличается от чатбота именно доступом к реальным действиям; это и создаёт катастрофы. citeturn34view5 |
| Quarantine для external skills/MCP | Любой внешний skill/MCP сначала в sandbox, потом статический/репутационный скан, потом allowlist | AI Factory прямо предупреждает о prompt injection в SKILL.md и запускает двухуровневый security scan. citeturn29search6 |
| Path allowlist | Жёстко ограничить, что агент вообще может читать и писать на диске |


### 20. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 3 колонок, 0 строк_

| PII[^pii] separation | Любые контакты, email, Telegram, ссылки — в отдельном raw‑слое; в карточки уходит только очищенный профиль | Так делает Svyazi; это правильный privacy‑baseline для людей и сообществ. citeturn41search0 |
| Truth vs Proposal |


### 21. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 3 колонок, 6 строк_

| Этап | Дефолт | Когда эскалировать |
|---|---|---|
| Extraction из свободного текста | Локальная или дешёвая модель + строгая schema guidance | Только если extraction‑quality стабильно проваливает ваши acceptance tests |
| Нормализация | Детерминированный код | Практически никогда не переводить это на дорогую модель |
| Retrieval / rerank | Non‑LLM[^llm] hybrid retrieval или локальный reranker | При multi-hop вопросах и слабой explainability |
| Объяснение матча / summary | Средний облачный tier | Если нужен высокий stylistic quality, а не только фактология |
| Финальный внешний отчёт | Сильная модель | Только для user-facing/public/legal‑style текста |
| Ночной ресёрч / оптимизация | AutoResearch‑подход с жёстким бюджетом и rollback | Когда уже есть benchmark и понятная функция качества |


### 22. Статус
_Файл: `docs/04-ai-collaborations/07-выводы.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 23. Статус
_Файл: `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 24. Статус
_Файл: `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 25. Архитектурные зазоры, которые важнее новых инструментов
_Файл: `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 5 колонок, 5 строк_

| Архитектурный зазор | Уже сильные кандидаты | Что в них уже хорошо закрыто | Что пока остаётся незакрытым | Что брать в MVP |
|---|---|---|---|---|
| Карточка как единица правды | Svyazi, AgentFS | CardIndex, hash/dedup, versionable vault, persistent state | Универсальная типизация для person/project/doc/episode/hypothesis | Card schema + raw/inferred split + immutable IDs citeturn41search0turn27view0turn33view4 |
| Доказуемое основание вывода | research-docs/LiteParse, Legal RAG, Hybrid RAG | Bounding boxes, page-level grounding, coordinates, transparent retrieval | Единый формат “evidence pack” между retrieval и интерфейсом | Page-level viewer + source_id/page/span/box schema citeturn20view5turn20view6turn34view2 |
| Память с контролируемым статусом | NGT Memory, Yodoca, agent-memory-mcp, Memory OS | Associative retrieval, consolidation, forgetting, typed memory, guard rails | Чёткая граница truth/proposal/conflict/decayed | Pending queue + confidence/state machine на наполнение графа citeturn22view4turn21view0turn20view16turn39view3 |
| Оркестрация и review | mclaude, AI Factory, Rufler, Sequential | Locks, mailbox, patch learning, YAML swarm, sequential review | Стандарт handoff для non-code workflow и knowledge moderation | 2–3 роли: extractor → reviewer → publisher citeturn20view2turn20view3turn20view4turn20view11 |
| Безопасный execution plane | LiteLLM, Auto AI Router, Tool Search, SENTINEL | Unified API, lightweight routing, lazy tool loading, runtime guard | Общая policy matrix на tool classes и external skills | Read-only by default + write approval + path allowlist citeturn11search2turn39view0turn39view1turn20view10turn20view16 |


### 26. Статус
_Файл: `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 27. Статус
_Файл: `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 28. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 4 колонок, 1 строк_

| Контракт | Минимальные поля | Зачем нужен в MVP | На какие идеи опирается |
|---|---|---|---|
| Card Envelope |


### 29. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 0 строк_

| Единый source of truth и dedup/version trace | Svyazi, AgentFS, Memory OS citeturn41search0turn27view0turn39view3 |
| Evidence Envelope |


### 30. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 0 строк_

| Проверяемость выводов и ручной review | LiteParse, Legal RAG, Hybrid/Graph RAG citeturn20view5turn20view6turn34view2turn34view3 |
| Memory Write Policy |


### 31. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 0 строк_

| Развести факт, эпизод и гипотезу | Yodoca, NGT Memory, agent-memory-mcp citeturn21view0turn22view4turn20view16 |
| Skill Policy |


### 32. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 0 строк_

| Снизить blast radius и упростить audit | Tool Search, SENTINEL, AI Factory practices citeturn39view1turn20view10turn29search6 |
| Review Record |


### 33. Статус
_Файл: `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 34. Дорожная карта прототипа следующей итерации
_Файл: `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | 5 колонок, 5 строк_

| Итерация | Главная цель | Минимум, который должен заработать | Оценка усилий | Главный риск |
|---|---|---|---|---|
| Evidence-first core | Из любого suggestions можно перейти к основанию | Unified cards + page/span evidence + manual reviewer UI | 1–2 недели | Переусложнение схемы слишком рано |
| Memory governance | Ассоциации перестают путаться с фактами | Episode store + proposal queue + approval/decay states | 1–2 недели | Ложная уверенность в “умной памяти” без жёсткого review |
| Agented moderation | Рой помогает, а не создаёт шум | extractor/reviewer/publisher roles + handoff/journal | 1–2 недели | Многоагентный хаос без хороших критериев качества |
| Local-first ingestion | Система начинает жить в ежедневном потоке | voice→episode, local vault, selective sync | 1–2 недели | Sync-конфликты и таскание лишних данных наружу |
| Self-improvement loop | Ошибки превращаются в benchmark и patch | benchmark set + nightly eval + rollback policy | 1 неделя на каркас, дальше непрерывно | Большой соблазн автоматизировать раньше, чем появилась метрика |


### 35. Статус
_Файл: `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 36. Контактная стратегия и узкие вопросы для авторов
_Файл: `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 3 колонок, 1 строк_

| Кому | Лучший первый вопрос | Почему именно он |
|---|---|---|
| entity["people","Андрей Чуян","habr author"] | Стоит ли расширять CardIndex до


### 37. Контактная стратегия и узкие вопросы для авторов
_Файл: `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 3 колонок, 1 строк_

| entity["people","Виталий Оборин","software engineer"] | Что сильнее всего влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? | Это позволяет использовать Yodoca как policy reference, а не как “ещё один ассистент”. citeturn21view0turn21view1 |
| **spbmolot** | Где проходит практическая граница между полезной ассоциацией и ложной ко‑активацией тем? | Это самый важный вопрос для community matching. citeturn22view4turn22view5 |
| **авторы knowledge-space / mclaude** | Держать операционные benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? | Это шов между памятью, знаниями и orchestration. citeturn33view2turn20view2 |


### 38. Статус
_Файл: `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


## 05-habr-projects (6 таблиц)


### 1. Статус
_Файл: `docs/05-habr-projects/01-synthesis.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 2. Статус
_Файл: `docs/05-habr-projects/02-collaboration-partners.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 3. Статус
_Файл: `docs/05-habr-projects/knowledge/wikontic.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 90 |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 4. Статус
_Файл: `docs/05-habr-projects/memory/memnet.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 90 |
| Слой | memory |
| Контакт | [@Antipozitive](obsidian/contacts/antipozitive.md) |
| Статус связи | не писали |


### 5. Статус
_Файл: `docs/05-habr-projects/memory/ngt-memory.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 260 |
| Слой | memory |
| Контакт | [@spbmolot](autofilled/components/spbmolot.md) |
| Статус связи | не писали |


### 6. Статус
_Файл: `docs/05-habr-projects/memory/yodoca.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 229 |
| Слой | memory |
| Контакт | [@VitalyOborin](obsidian/contacts/vitalyoborin.md) |
| Статус связи | не писали |


## contacts (14 таблиц)


### 1. Профиль
_Файл: `docs/contacts/anastasiyaw.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **AnastasiyaW** |
| GitHub | [@AnastasiyaW](https://github.com/AnastasiyaW) |
| Проекты | knowledge-space, mclaude |
| Слой в Svyazi | knowledge/orchestration |
| Упомянут в документах | 11 файлах |
| Платформа | Habr / GitHub |


### 2. Профиль
_Файл: `docs/contacts/andrey-chuyan.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **andrey_chuyan** |
| GitHub | [@andrey_chuyan](https://github.com/andrey_chuyan) |
| Проекты | Svyazi |
| Слой в Svyazi | ingestion/CardIndex |
| Упомянут в документах | 4 файлах |
| Платформа | Habr / GitHub |


### 3. Профиль
_Файл: `docs/contacts/antipozitive.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **Antipozitive** |
| GitHub | [@Antipozitive](https://github.com/Antipozitive) |
| Проекты | MemNet |
| Слой в Svyazi | memory |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


### 4. Профиль
_Файл: `docs/contacts/cutcode.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **Cutcode** |
| GitHub | [@Cutcode](https://github.com/Cutcode) |
| Проекты | AIF Handoff |
| Слой в Svyazi | orchestration |
| Упомянут в документах | 5 файлах |
| Платформа | Habr / GitHub |


### 5. Профиль
_Файл: `docs/contacts/dmitriila.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **Dmitriila** |
| GitHub | [@Dmitriila](https://github.com/Dmitriila) |
| Проекты | SENTINEL |
| Слой в Svyazi | security |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


### 6. Профиль
_Файл: `docs/contacts/kksudo.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **kksudo** |
| GitHub | [@kksudo](https://github.com/kksudo) |
| Проекты | AgentFS |
| Слой в Svyazi | knowledge/filesystem |
| Упомянут в документах | 13 файлах |
| Платформа | Habr / GitHub |


### 7. Профиль
_Файл: `docs/contacts/mixaill76.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **MiXaiLL76** |
| GitHub | [@MiXaiLL76](https://github.com/MiXaiLL76) |
| Проекты | Auto AI Router |
| Слой в Svyazi | security |
| Упомянут в документах | 4 файлах |
| Платформа | Habr / GitHub |


### 8. Профиль
_Файл: `docs/contacts/nlaik.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **nlaik** |
| GitHub | [@nlaik](https://github.com/nlaik) |
| Проекты | LiteParse / research-docs |
| Слой в Svyazi | rag |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


### 9. Профиль
_Файл: `docs/contacts/sonia-black.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **Sonia_Black** |
| GitHub | [@Sonia_Black](https://github.com/Sonia_Black) |
| Проекты | knowledge-space |
| Слой в Svyazi | knowledge |
| Упомянут в документах | 6 файлах |
| Платформа | Habr / GitHub |


### 10. Профиль
_Файл: `docs/contacts/spbmolot.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **spbmolot** |
| GitHub | [@spbmolot](https://github.com/spbmolot) |
| Проекты | NGT Memory |
| Слой в Svyazi | memory |
| Упомянут в документах | 12 файлах |
| Платформа | Habr / GitHub |


### 11. Профиль
_Файл: `docs/contacts/tagir-analyzes.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **tagir_analyzes** |
| GitHub | [@tagir_analyzes](https://github.com/tagir_analyzes) |
| Проекты | Legal RAG |
| Слой в Svyazi | rag |
| Упомянут в документах | 4 файлах |
| Платформа | Habr / GitHub |


### 12. Профиль
_Файл: `docs/contacts/vitalyoborin.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **VitalyOborin** |
| GitHub | [@VitalyOborin](https://github.com/VitalyOborin) |
| Проекты | Yodoca |
| Слой в Svyazi | memory |
| Упомянут в документах | 7 файлах |
| Платформа | Habr / GitHub |


### 13. Профиль
_Файл: `docs/contacts/vladspace.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **VladSpace** |
| GitHub | [@VladSpace](https://github.com/VladSpace) |
| Проекты | Graph RAG |
| Слой в Svyazi | rag |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


### 14. Профиль
_Файл: `docs/contacts/zodigancode.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **zodigancode** |
| GitHub | [@zodigancode](https://github.com/zodigancode) |
| Проекты | Rufler |
| Слой в Svyazi | orchestration |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


## obsidian (253 таблиц)


### 1. Шкала зрелости
_Файл: `docs/obsidian/01-svyazi/02-methodology.md` | 2 колонок, 4 строк_

| Уровень | Описание |
|---------|----------|
| **Эксперимент** | Исследовательский или концептуальный код |
| **Рабочий прототип** | Можно поставить и проверить сценарий |
| **Активный OSS** | Есть явная публичная разработка, релизы или активное развитие |
| **Внутренний/закрытый прототип** | Архитектура раскрыта, но код закрыт |


### 2. Карта найденных проектов и паттернов
_Файл: `docs/obsidian/01-svyazi/03-component-catalog.md` | 8 колонок, 19 строк_

| Проект или связка | Автор | Ссылка на статью и репо | Краткое описание | Ключевые компоненты и паттерны | Лицензия | Maturity / статус | Релевантность к Svyazi[^svyazi]‑2.0 |
|---|---|---|---|---|---|---|---|
| **Svyazi** | Андрей Чуян | Хабр citeturn41search0 | Гибридная система извлечения структурированных профилей участников сообщества из свободного текста; уже показала кейс «карточек коллабораций». | 6 слоёв, YAML, SHA256‑дедупликация, Ollama+Qwen, LLM[^llm]+детерминированный код, CardIndex[^cardindex], privacy by design. | **Код закрыт**. citeturn41search0 | Активный закрытый авторский прототип. citeturn41search0 | **Очень высокая**: это базовый ingest/normalize/discovery‑слой. |
| **knowledge-space** | Sonia_Black / AnastasiyaW | Хабр + GitHub citeturn33view0turn33view2turn37search1 | Agent‑first референсная база: 785+ карточек по 26 доменам, растущая из реальных research‑сессий. | Dense reference cards, gotchas, wiki‑links, `research/inbox/`, «для агентов, не людей». | **MIT**. citeturn33view0turn37search1 | Активный OSS, база растёт почти ежедневно. citeturn33view1turn37search1 | **Высокая**: это внешний knowledge layer для агентов и нормализатора. |
| **AgentFS** | kksudo | Хабр + GitHub citeturn33view4turn33view7turn27view0 | Превращает Obsidian‑vault в операционную систему для AI‑агентов с единым `.agentos/`‑ядром. | Compile‑to‑native configs, persistent state, security policies, memory consolidation, doctor/triage/compile CLI. | **MIT**. citeturn33view4turn27view0 | Рабочий прототип, версия 0.1.5; “рабочая, но не финальная”. citeturn33view7 | **Очень высокая**: это лучший кандидат на файловое ядро Svyazi‑2.0. |
| **mclaude** | AnastasiyaW | Хабр + GitHub citeturn20view2turn37search0 | Координация нескольких сессий Claude Code и других coding‑агентов над одним проектом. | Locks, handoffs, mailbox, multi‑session turn‑taking, shared project memory. | **MIT**. citeturn37search0 | Активный OSS. citeturn37search0 | **Высокая**: решает параллельную работу модераторов/агентов над общим графом. |
| **AI Factory + AIF Handoff** | lee-to / Cutcode | Хабр + GitHub citeturn20view3turn29search0turn29search9 | Spec‑driven многоагентный development‑framework и автономный Kanban‑слой поверх него. | Skills, patches, self‑learning, worktrees, MCP[^mcp] handoff, plan/implement/review, WebSocket Kanban. | **MIT**. citeturn29search0turn29search9 | Активный OSS, релизы v2.x; handoff добавлен в свежих релизах. citeturn29search4 | **Высокая**: готовый оркестратор для build‑ и moderation‑контуров Svyazi‑2.0. |
| **Rufler** | zodigancode / lib4u | Хабр + repo/DEV citeturn20view4turn21view8turn32search0 | Декларативный YAML‑слой для запуска автономного роя Claude Code‑агентов. | `depends_on`, auto‑objective prompts, pause/resume, token accounting, MCP server management. | **MIT**. citeturn32search0 | Активный OSS. citeturn32search0 | **Средне‑высокая**: быстрый orchestration‑слой без тяжёлого UI. |
| **research-docs + LiteParse** | nlaik / Jerry Liu / LlamaIndex | Хабр + GitHub citeturn20view5turn15search1turn15search5turn40search0 | Forensic document QA с HTML‑отчётом и bounding boxes на страницах PDF. | Локальный парсер, spatial text parsing, visual citations, multi‑format docs, HTML evidence report. | **Apache 2.0** для LiteParse; для samples — неуточнено в просмотренных источниках. citeturn40search0turn40search1 | Активный OSS. citeturn15search1turn15search5 | **Очень высокая**: даёт visual grounding, которого Svyazi‑подобным системам обычно не хватает. |
| **Hybrid RAG[^rag] knowledge base** | iximy | Хабр citeturn34view2 | Минималистский Hybrid RAG без тяжёлых фреймворков. | `pdfplumber`, координаты слов, TF‑IDF, FAISS, metadata filtering, прозрачный retrieval‑layer. | Неуточнено. citeturn34view2 | Практический implementation guide; публичный код в статье не акцентирован. citeturn34view2 | **Высокая**: полезен как быстрый базовый retrieval‑контур. |
| **Legal RAG** | tagir_analyzes | Хабр citeturn20view6 | Подробный кейс page‑level Legal RAG с 17 итерациями и измерением пределов масштабирования. | Page‑level grounding, context distillation, систематический eval loop, error analysis. | Неуточнено. citeturn20view6 | Зрелый инженерный кейс, а не только концепт. citeturn20view6 | **Очень высокая**: лучший источник для evidence‑first и audit‑friendly retrieval. |
| **Graph RAG** | VladSpace / vpakspace | Хабр + GitHub citeturn34view3turn40search2 | Графовый RAG с provenance‑trace и typed API, собранный из 5 исследовательских техник. | Skeleton Indexing, Phrase/Passage dual nodes, VectorCypher, Datalog reasoning, agentic routing. | Неуточнено. citeturn34view3turn40search2 | Активный публичный repo / production‑ready ambition. citeturn34view3turn40search2 | **Высокая**: добавляет multi‑hop retrieval и relation‑reasoning. |
| **Yodoca** | VitalyOborin | Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1 | Локальный self‑evolving AI assistant с долговременной памятью и ночной консолидацией. | Hot/slow path, private write‑path consolidator, `is_session_consolidated`, Ebbinghaus decay, causal edges, proactive memory. | **Apache 2.0**. citeturn18search1 | Активный OSS. citeturn18search1 | **Очень высокая**: лучший слой для nightly consolidation и controlled forgetting. |
| **NGT Memory** | spbmolot / ngt-memory | Хабр + GitHub/site citeturn22view4turn22view3turn32search2 | Персистентная память для LLM‑приложений с ассоциативным графом и миллисекундным retrieval overhead. | Cosine similarity + Hebbian graph + hierarchical consolidation, REST API, Docker, 2–3 ms собственных затрат. | **BSL 1.1**; в статье прямо сказано «бесплатно для личных проектов». citeturn22view5 | Активная разработка. citeturn22view3turn32search2 | **Очень высокая**: быстрый ассоциативный memory‑слой для discovery и matching. |
| **MemNet / memory-is-all-you-need** | Antipozitive | Хабр + GitHub citeturn21view4turn17search0turn18search2 | Исследовательская активная память для трансформеров. | Hebbian graph memory, STDP, spreading activation, “dreaming”, anti‑forgetting. | **MIT**. citeturn17search0turn18search2 | Экспериментальный research codebase. citeturn17search0 | **Средне‑высокая**: не MVP‑слой, но сильная идея для future memory engine. |
| **agent-memory-mcp + Memory OS** | VitaliySemenov / moshael | Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 | Typed memory MCP плюс более тяжёлая концепция Memory OS с онтологией, gardener‑loop и bi‑temporal facts. | SQLite+WAL, typed memories, repo/doc search, path guard; ontology, concept loop, maintenance contour, planner/scout/synthesizer. | Для `agent-memory-mcp` — неуточнено; для Memory OS — неуточнено. citeturn15search3turn39view3 | `agent-memory-mcp` — рабочий OSS; Memory OS — концептуально амбициозный кейс без явного публичного репо в статье. citeturn15search3turn39view3 | **Высокая**: слой typed memory и governance для более поздних итераций. |
| **Self‑Aware MCP + Skills + CodeWiki** | akazant / akzhankalimatov / AnastasiyaW | Хабр + repo/marketplace + Хабр/репо citeturn20view12turn30search1turn20view15turn12search2turn37search7 | Контекст реального мира для агента плюс reusable skills и авто‑документация кодовой базы. | location/time/OS tools, skill files in repo, hooks, subagents, code wiki generation. | Self‑Aware MCP — **MIT** по карточке MCP Marketplace; config‑kit — **MIT**; CodeWiki — неуточнено. citeturn30search1turn37search7turn12search2 | Активный стек инструментов. citeturn20view12turn37search7turn12search2 | **Высокая**: делает агентный слой контекстным, переносимым и предсказуемым. |
| **Voice/local-first stack** | atatchin / askid / обзоры Handy/OpenWhispr | Хабр citeturn21view10turn21view11turn21view12turn35search0 | Локальный speech→text→LLM transform и более широкий local‑first knowledge workspace с recording/transcription. | Whisper локально, Ollama post‑processing, Handy/OpenWhispr/GigaAM, live transcription, diarization, semantic links, SQLite. | Смешанная картина; для Yttri лицензия в просмотренных источниках не уточнена. citeturn35search0turn21view11 | От usable scripts до beta‑продукта. citeturn21view10turn35search0 | **Средне‑высокая**: лучший входной канал для “raw episodes” в память. |
| **Yjs + Automerge** | Kevin Jahns / Automerge team | Документация и репо citeturn11search0turn11search7turn11search13turn11search1turn11search11turn11search23 | Базовый local‑first/CRDT[^crdt] sync‑слой для оффлайн‑совместимости и мультидевайсной синхронизации. | Shared types, automatic merge without conflicts, offline sync, local‑first data engine. | **MIT**. citeturn11search13turn11search23 | Активный OSS. citeturn11search13turn11search11 | **Средняя**, но стратегически важная: синхронизация между устройствами и узлами. |
| **Security + routing plane** | Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig | Хабр + GitHub/docs citeturn20view10turn11search2turn19search5turn39view0turn39view1turn20view18 | Рантайм‑безопасность и бюджетный execution plane для агентных систем. | SENTINEL[^sentinel] micro‑model swarm; LiteLLM unified API; Auto AI Router on Go; Tool Search lazy MCP loading; budget/privacy presets in RLM‑Toolkit. | Смешанная: SENTINEL — неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2.0. citeturn20view10turn19search5turn28search3 | Активный operational stack. citeturn20view10turn11search2turn39view0turn39view1 | **Очень высокая**: без этого Svyazi‑2.0 будет либо дорогой, либо небезопасной. |
| **AutoResearch + Sequential** | Андрей Карпаты / Виктория Дочкина | Хабр + GitHub/обзор citeturn20view19turn20view11 | Ночной цикл самоулучшения и протокол reviewer‑цепочки без централизованного координатора. | Edit‑run‑measure‑rollback loop, bounded experiments, sequential protocol, strong-model self‑organization. | Для AutoResearch — по статье на GitHub; лицензия в Habr‑обзоре не уточнялась. Для Sequential — исследовательская статья без OSS‑лицензии. citeturn20view19turn20view11 | Active research / practical harness. citeturn20view19turn20view11 | **Высокая**: это кандидат на self‑improvement и multi‑review для Svyazi‑2.0. |


### 3. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/obsidian/01-svyazi/06-security-privacy.md` | 3 колонок, 6 строк_

| Контроль | Практический дефолт | Основание |
|---|---|---|
| Разделение tool‑классов | По умолчанию разрешать read‑only tools; любые send/write/delete/execute — только через явный approval | Автономный агент отличается от чатбота именно доступом к реальным действиям; это и создаёт катастрофы. citeturn34view5 |
| Quarantine для external skills/MCP | Любой внешний skill/MCP сначала в sandbox, потом статический/репутационный скан, потом allowlist | AI Factory прямо предупреждает о prompt injection в SKILL.md и запускает двухуровневый security scan. citeturn29search6 |
| Path allowlist | Жёстко ограничить, что агент вообще может читать и писать на диске | `agent-memory-mcp` демонстрирует хороший паттерн Path Guard/allowlist против traversal и выхода за пределы проекта. citeturn20view16 |
| PII[^pii] separation | Любые контакты, email, Telegram, ссылки — в отдельном raw‑слое; в карточки уходит только очищенный профиль | Так делает Svyazi; это правильный privacy‑baseline для людей и сообществ. citeturn41search0 |
| Truth vs Proposal | `inferred` и weak signals не писать сразу в «истину», а ставить в pending review | И Svyazi, и более тяжёлые memory‑системы сходятся на нужде в review‑контуре. citeturn41search0turn36search0 |
| Runtime firewall | Между агентом и mutating tools держать специализированный защитный слой | Именно для этого и нужен SENTINEL‑подобный слой, а не только “умный промпт”. citeturn20view10 |


### 4. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/obsidian/01-svyazi/06-security-privacy.md` | 3 колонок, 6 строк_

| Этап | Дефолт | Когда эскалировать |
|---|---|---|
| Extraction из свободного текста | Локальная или дешёвая модель + строгая schema guidance | Только если extraction‑quality стабильно проваливает ваши acceptance tests |
| Нормализация | Детерминированный код | Практически никогда не переводить это на дорогую модель |
| Retrieval / rerank | Non‑LLM[^llm] hybrid retrieval или локальный reranker | При multi-hop вопросах и слабой explainability |
| Объяснение матча / summary | Средний облачный tier | Если нужен высокий stylistic quality, а не только фактология |
| Финальный внешний отчёт | Сильная модель | Только для user-facing/public/legal‑style текста |
| Ночной ресёрч / оптимизация | AutoResearch‑подход с жёстким бюджетом и rollback | Когда уже есть benchmark и понятная функция качества |


### 5. План прототипа и возможные контакты
_Файл: `docs/obsidian/01-svyazi/07-mvp-planning.md` | 4 колонок, 5 строк_

| Контур | Что входит | Зачем | Оценка усилий |
|---|---|---|---|
| Ядро данных | CardIndex‑схема, профили, raw/inferred разделение, файловый vault в стиле AgentFS | Сделать единый source of truth и трассируемый lifecycle карточки | 2–3 дня |
| Ingest и память | LLM[^llm] extraction + нормализация + NGT Memory **или** Yodoca‑lite | Доказать, что из свободного текста получаются устойчивые профили и связи | 4–6 дней |
| Evidence | LiteParse/research-docs + page‑level viewer | Не просто показать match, а показать основание | 3–4 дня |
| Исполнение | LiteLLM/Auto AI Router + Tool Search + базовые правила безопасности | Удержать стоимость и не утонуть в MCP[^mcp]/context overhead | 2–3 дня |
| Guardrails | PII[^pii]‑фильтры, allowlists, manual review для inferred | Снизить риск ложных связей и утечек | 1–2 дня |


### 6. План прототипа и возможные контакты
_Файл: `docs/obsidian/01-svyazi/07-mvp-planning.md` | 3 колонок, 5 строк_

| Риск | Почему это важно | Снижение риска |
|---|---|---|
| Schema drift и самовольная “оптимизация” структуры моделью | На extraction‑этапе сильная модель может начать “улучшать” схему вместо исполнения | Держать extraction на constrained schema + низком reasoning, а смысл переносить в post‑processing; это совпадает и с логикой Svyazi, и с выводами Memory OS. citeturn41search0turn39view3 |
| Ложные ассоциации в памяти | Ассоциативная память полезна, но легко порождает шум | Вводить review queue для `inferred`, разделять raw vs normalized, не писать Proposal сразу в Truth‑граф. citeturn41search0turn36search0 |
| Утечка PII в карточки и prompts | Discovery‑система почти неизбежно работает с чувствительными профилями | Повторить Svyazi‑паттерн privacy‑by‑design, хранить контакты отдельно, использовать allowlist/path guard, локальные embeddings там, где можно. citeturn41search0turn20view16turn35search0 |
| Лицензионный тупик на memory‑слое | Не все “open” memory‑решения одинаково permissive | Если нужен строго permissive/commercial‑friendly стек, NGT Memory надо проверять отдельно, потому что в статье указана BSL[^bsl] 1.1 и free‑for‑personal grant; на таком пути проще начать с Yodoca или agent-memory-mcp. citeturn22view5turn18search1turn15search3 |
| Многоагентный хаос раньше пользы | Рой даёт выгоду только после появления handoff/lock и чётких спецификаций | Начинать с mclaude + AI Factory/AIF Handoff, а Rufler/Sequential/AutoResearch добавлять после того, как появилась стабильная spec и критерии качества. citeturn20view2turn20view3turn20view4turn20view11turn20view19 |


### 7. План прототипа и возможные контакты
_Файл: `docs/obsidian/01-svyazi/07-mvp-planning.md` | 4 колонок, 5 строк_

| Кому писать | Почему именно он или она | Публичный вектор из просмотренных источников | Контакт в источниках |
|---|---|---|---|
| **andrey_chuyan** | Единственный из найденных авторов, у кого уже есть рабочий кейс “карточки коллаборации” и CardIndex‑мышление. citeturn41search0 | Комментарии к статье Svyazi на Хабре. citeturn41search0 | Публичный email/Telegram в просмотренных источниках **не найден**. |
| **Sonia_Black / AnastasiyaW** | Закрывает сразу два слоя: knowledge-space и multi-session coordination через mclaude. citeturn33view3turn20view2turn37search0 | Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn33view0turn37search0 | Публичный прямой контакт **не найден**. |
| **kksudo** | Наиболее важный кандидат для слоя `.agentos/` и compile‑to‑runtime политики. citeturn33view4turn27view0 | Комментарии к статье и GitHub issues в AgentFS. citeturn33view7turn27view0 | Публичный прямой контакт **не найден**. |
| **VitalyOborin** | Сильнейший кандидат на consolidator/forgetting‑слой. citeturn21view0turn21view1turn18search1 | Комментарии к статье Yodoca и GitHub issues/discussions в repo. citeturn38view7turn18search1 | Публичный прямой контакт **не найден**. |
| **spbmolot** | Нужен для ассоциативной памяти и очень дешёвого memory retrieval с graph‑подтягиванием слабых связей. citeturn22view4turn22view5 | Комментарии к статье NGT Memory и GitHub repository. citeturn22view5turn32search2 | Публичный прямой контакт **не найден**. |


### 8. Архитектурные зазоры, которые важнее новых инструментов
_Файл: `docs/obsidian/01-svyazi/09-architectural-gaps.md` | 5 колонок, 5 строк_

| Архитектурный зазор | Уже сильные кандидаты | Что в них уже хорошо закрыто | Что пока остаётся незакрытым | Что брать в MVP |
|---|---|---|---|---|
| Карточка как единица правды | Svyazi, AgentFS | CardIndex, hash/dedup, versionable vault, persistent state | Универсальная типизация для person/project/doc/episode/hypothesis | Card schema + raw/inferred split + immutable IDs citeturn41search0turn27view0turn33view4 |
| Доказуемое основание вывода | research-docs/LiteParse, Legal RAG, Hybrid RAG | Bounding boxes, page-level grounding, coordinates, transparent retrieval | Единый формат “evidence pack” между retrieval и интерфейсом | Page-level viewer + source_id/page/span/box schema citeturn20view5turn20view6turn34view2 |
| Память с контролируемым статусом | NGT Memory, Yodoca, agent-memory-mcp, Memory OS | Associative retrieval, consolidation, forgetting, typed memory, guard rails | Чёткая граница truth/proposal/conflict/decayed | Pending queue + confidence/state machine на наполнение графа citeturn22view4turn21view0turn20view16turn39view3 |
| Оркестрация и review | mclaude, AI Factory, Rufler, Sequential | Locks, mailbox, patch learning, YAML swarm, sequential review | Стандарт handoff для non-code workflow и knowledge moderation | 2–3 роли: extractor → reviewer → publisher citeturn20view2turn20view3turn20view4turn20view11 |
| Безопасный execution plane | LiteLLM, Auto AI Router, Tool Search, SENTINEL | Unified API, lightweight routing, lazy tool loading, runtime guard | Общая policy matrix на tool classes и external skills | Read-only by default + write approval + path allowlist citeturn11search2turn39view0turn39view1turn20view10turn20view16 |


### 9. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/obsidian/01-svyazi/11-integration-contracts.md` | 4 колонок, 5 строк_

| Контракт | Минимальные поля | Зачем нужен в MVP | На какие идеи опирается |
|---|---|---|---|
| Card Envelope | `card_id`, `card_type`, `state`, `sources`, `edges`, `updated_at`, `payload_hash` | Единый source of truth и dedup/version trace | Svyazi, AgentFS, Memory OS citeturn41search0turn27view0turn39view3 |
| Evidence Envelope | `source_id`, `page_or_span`, `bbox_or_offset`, `method`, `confidence`, `supporting_nodes` | Проверяемость выводов и ручной review | LiteParse, Legal RAG, Hybrid/Graph RAG citeturn20view5turn20view6turn34view2turn34view3 |
| Memory Write Policy | `write_type`, `promotion_rule`, `review_required`, `decay_policy` | Развести факт, эпизод и гипотезу | Yodoca, NGT Memory, agent-memory-mcp citeturn21view0turn22view4turn20view16 |
| Skill Policy | `tool_class`, `approval_mode`, `path_scope`, `network_scope`, `output_target` | Снизить blast radius и упростить audit | Tool Search, SENTINEL, AI Factory practices citeturn39view1turn20view10turn29search6 |
| Review Record | `reviewer_role`, `decision`, `reason`, `evidence_refs`, `follow_up` | Не путать machine suggestion с accepted truth | mclaude, AI Factory, Sequential citeturn20view2turn20view3turn20view11 |


### 10. Дорожная карта прототипа следующей итерации
_Файл: `docs/obsidian/01-svyazi/12-roadmap.md` | 5 колонок, 5 строк_

| Итерация | Главная цель | Минимум, который должен заработать | Оценка усилий | Главный риск |
|---|---|---|---|---|
| Evidence-first core | Из любого suggestions можно перейти к основанию | Unified cards + page/span evidence + manual reviewer UI | 1–2 недели | Переусложнение схемы слишком рано |
| Memory governance | Ассоциации перестают путаться с фактами | Episode store + proposal queue + approval/decay states | 1–2 недели | Ложная уверенность в “умной памяти” без жёсткого review |
| Agented moderation | Рой помогает, а не создаёт шум | extractor/reviewer/publisher roles + handoff/journal | 1–2 недели | Многоагентный хаос без хороших критериев качества |
| Local-first ingestion | Система начинает жить в ежедневном потоке | voice→episode, local vault, selective sync | 1–2 недели | Sync-конфликты и таскание лишних данных наружу |
| Self-improvement loop | Ошибки превращаются в benchmark и patch | benchmark set + nightly eval + rollback policy | 1 неделя на каркас, дальше непрерывно | Большой соблазн автоматизировать раньше, чем появилась метрика |


### 11. Контактная стратегия и узкие вопросы для авторов
_Файл: `docs/obsidian/01-svyazi/13-contacts.md` | 3 колонок, 5 строк_

| Кому | Лучший первый вопрос | Почему именно он |
|---|---|---|
| entity["people","Андрей Чуян","habr author"] | Стоит ли расширять CardIndex до `person/project/episode/evidence`, или для discovery и moderation лучше держать разные индексы? | Это продолжает его реальную архитектурную линию, а не уводит в абстракцию. citeturn41search0 |
| **kksudo** | Что лучше класть в `.agentos`, а что выносить в machine-only state вне vault conventions? | Это вопрос в сердце AgentFS, а не общая просьба о сотрудничестве. citeturn27view0turn33view4 |
| entity["people","Виталий Оборин","software engineer"] | Что сильнее всего влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? | Это позволяет использовать Yodoca как policy reference, а не как “ещё один ассистент”. citeturn21view0turn21view1 |
| **spbmolot** | Где проходит практическая граница между полезной ассоциацией и ложной ко‑активацией тем? | Это самый важный вопрос для community matching. citeturn22view4turn22view5 |
| **авторы knowledge-space / mclaude** | Держать операционные benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? | Это шов между памятью, знаниями и orchestration. citeturn33view2turn20view2 |


### 12. Naming convention расшифрована
_Файл: `docs/obsidian/02-anthropic-vacancies/00-intro.md` | 3 колонок, 7 строк_

| Префикс | Кол-во | Смысл |
| --- | --- | --- |
| soz* | 11 (9 private) | Соцправо/Sozialrecht — кластер #1 из data70 |
| daten* | 12 | «Данные» по-немецки, но фактически — Information OS / рационализация |
| data* | 8 | Чистые данные + legal content blocks |
| info* | 16 | Методология, RAG, архетипы, пирамиды, инфосистемы |
| meta* | 5 | Мета-проекты (монорепо, рантаймы, AST) |
| in4* | 2 | Information Flow variant |
| Именованные | 6 | nautilus, ingit, pro2, information, claudeai-test-project-k, universal-file-storage-mcp |


### 13. 2.3. Артефакты каждой фазы
_Файл: `docs/obsidian/02-anthropic-vacancies/108-2-формальный-workflow.md` | 4 колонок, 4 строк_

| Фаза | Артефакт | Место хранения | Финальность |
|------|----------|----------------|-------------|
| A | `<doc>_draft_A.md` | ветка `claude/review-XXX` | нет, промежуточное |
| B | `<doc>_draft_B.md` | ветка `claude/review-YYY` | нет, промежуточное |
| Merge | `<doc>.md` с header warning + параллельными блоками | main, с dupликацией | нет, transitional |
| C | `<doc>.md` консолидированная | main, dupликаты удалены | да, канонично |


### 14. 8.1. Trade-offs
_Файл: `docs/obsidian/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | 2 колонок, 5 строк_

| Преимущество | Оборотная сторона |
|--------------|-------------------|
| Сохранение всех insights | Transitional state выглядит messy |
| Защита от single-agent bias | Требует ручной консолидации (время) |
| Audit trail обеих версий | Увеличивает объём документа временно |
| Методологически обосновано | Read-time overhead для внешних |
| Масштабируется на team-work | Не решает проблему >2 вариантов |


### 15. Доступные инструменты
_Файл: `docs/obsidian/02-anthropic-vacancies/128-доступные-инструменты.md` | 2 колонок, 7 строк_

| Tool | Назначение |
| --- | --- |
| `nautilus_query` | Поиск по всей экосистеме с consensus |
| `nautilus_query_repo` | Поиск в конкретном репо |
| `nautilus_list_repos` | Список всех адаптеров с метаданными |
| `nautilus_consensus_check` | Проверка concept agreement |
| `nautilus_describe` | Описание экосистемы (философия, версия, angles) |
| `nautilus_q6_neighbors` | Поиск Q6-соседей по Hamming distance |
| `nautilus_health` | Health score 0–100 |


### 16. Структурное сравнение: код vs гуманитарные документы
_Файл: `docs/obsidian/02-anthropic-vacancies/133-обратная-связь.md` | 3 колонок, 10 строк_

| Аспект | Код/Research (текущий Nautilus) | Юридические/Социальные документы |
| --- | --- | --- |
| Единица данных | Концепт/функция/теорема | Статья закона/параграф решения/кейс |
| Native format | .py, .md, .info1, .pro2 | .pdf, .docx, .odt, .md, .rtf |
| Язык | En/Ru, технический | De (SGB, SGG), En (EU law), Ru |
| Связи | Import, reference, bridge | Статья→статья, прецедент→прецедент, учреждение→процедура |
| Авторство | Автор-разработчик | Законодатель, суд, учреждение |
| Консенсус | Концепт в N репо | Факт подтверждён N источниками |
| Q6-координата | Семантическая вершина | Категория права/социальной сферы |
| Стабильность | Меняется часто (коммиты) | Стабильна (Geltungsbereich), но с поправками |
| Timestamp-критичность | Умеренная | Критическая(Fristwahrung, Inkrafttreten) |
| Regulatory | Open-source lics | Urheberrecht, Amtliche Werke, GDPR |


### 17. 5.2. Three-Year Pilot Budget (Estimated)
_Файл: `docs/obsidian/02-anthropic-vacancies/159-5-economic-model.md` | 4 колонок, 9 строк_

| Category | Year 1 | Year 2 | Year 3 |
|----------|--------|--------|--------|
| Core staff (5-8 people) | €600K | €900K | €1.2M |
| Infrastructure development | €400K | €300K | €300K |
| Contributor stipends (growing cohort) | €300K | €1.2M | €2.5M |
| Contributor bonuses | €100K | €400K | €1M |
| Legal and compliance | €150K | €200K | €300K |
| Administrative and governance | €100K | €150K | €200K |
| Community events and outreach | €100K | €150K | €250K |
| Reserve and contingency | €250K | €500K | €750K |
| **Total annual** | **€2M** | **€3.8M** | **€6.5M** |


### 18. Appendix A: Comparison Matrix Against Existing Solutions
_Файл: `docs/obsidian/02-anthropic-vacancies/164-10-appendices.md` | 8 колонок, 11 строк_

| Feature | OKWF | Deel | Upwork | Toptal | Mercor | OSS Foundations | Employment |
|---------|------|------|--------|--------|--------|-----------------|------------|
| Cross-border compliance | ✓ | ✓ | Partial | ✓ | ✓ | — | — |
| Part-time capacity support | ✓ | Partial | ✓ | Partial | Partial | ✓ | ✗ |
| Dignity preservation | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Community continuity | ✓ | ✗ | ✗ | Partial | ✗ | ✓ | ✓ |
| AI-assisted coordination | ✓ | ✗ | Partial | ✗ | ✓ | ✗ | ✗ |
| Pattern library | ✓ | ✗ | ✗ | ✗ | ✗ | Partial | ✗ |
| Guild structure | ✓ | ✗ | ✗ | ✗ | ✗ | Partial | Partial |
| Reputation portability | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | Partial |
| Mission alignment | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | Varies |
| Graduated progression | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Funded baseline stipend | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |


### 19. Appendix B: Domain Comparison Matrix
_Файл: `docs/obsidian/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 5 колонок, 10 строк_

| Domain | Privacy Sensitivity | Adversarial Risk | Regulatory Complexity | Deployment Readiness |
|--------|--------------------|--------------------|----------------------|----------------------|
| 1. Knowledge Workers | Medium | Low | Low | High |
| 2. Retired Professionals | Low | Low | Low | High |
| 3. Social Workers | High | Medium | Medium | Medium |
| 4. Vulnerable Citizens | High | High | High | Medium |
| 5. Caregivers | High | Low | High | Medium |
| 6. Small Business | Low | Medium | Medium | Medium |
| 7. Patients | Highest | Medium | Highest | Medium-Low |
| 8. Students | Low | Low | Low | Medium |
| 9. Communities | Medium | High | High | Medium-Low |
| 10. Future Generations | N/A | Highest | Highest | Low |


### 20. Приложение B: Матрица Сравнения Областей
_Файл: `docs/obsidian/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 5 колонок, 10 строк_

| Область | Чувствительность Конфиденциальности | Состязательный Риск | Регулятивная Сложность | Готовность к Развёртыванию |
|---------|-------------------------------------|---------------------|------------------------|----------------------------|
| 1. Работники Знаний | Средняя | Низкая | Низкая | Высокая |
| 2. Профессионалы на Пенсии | Низкая | Низкая | Низкая | Высокая |
| 3. Социальные Работники | Высокая | Средняя | Средняя | Средняя |
| 4. Уязвимые Граждане | Высокая | Высокая | Высокая | Средняя |
| 5. Опекуны | Высокая | Низкая | Высокая | Средняя |
| 6. Малый Бизнес | Низкая | Средняя | Средняя | Средняя |
| 7. Пациенты | Наивысшая | Средняя | Наивысшая | Средняя-Низкая |
| 8. Студенты | Низкая | Низкая | Низкая | Средняя |
| 9. Сообщества | Средняя | Высокая | Высокая | Средняя-Низкая |
| 10. Будущие Поколения | Н/Д | Наивысшая | Наивысшая | Низкая |


### 21. 1.7. Why This Distinction Matters
_Файл: `docs/obsidian/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | 6 колонок, 7 строк_

| Property | Type 0 | Type 1 | Type 2 | Type 3 | Type 4 |
|----------|--------|--------|--------|--------|--------|
| Specialization | None | Profession | Institution+profession | Task | Individual |
| External communication | None | None | Some | Some | Extensive |
| Replicability | Universal | Per profession | Per institution | Per task | Per individual |
| Economics | Subscription | Profession-wide | Institutional | Variable | Individual |
| Ethical concerns | Low | Medium | Medium | High | Highest |
| Regulatory complexity | Low | Medium | High | Highest | Highest |
| Deployment readiness | Mature | Emerging | Early | Beginning | Conceptual |


### 22. 3.3. Deployment Trajectory
_Файл: `docs/obsidian/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | 2 колонок, 3 строк_

| Date | Status |
|------|--------|
| Summer 2025 | Development begins |
| September 2025 | Public launch |
| April 2026 | 93,000 active teacher users |


### 23. Appendix A: Comparative Table — Five Agent Types
_Файл: `docs/obsidian/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | 6 колонок, 12 строк_

| Property | Type 0: Personal AI Assistant | Type 1: Professional Colleague | Type 2: Institutional | Type 3: Employee | Type 4: Representative |
|----------|---|---|---|---|---|
| **Specialization** | None (general) | Single profession | Profession + institution | Specific task | Specific individual |
| **Direction** | Reactive | Reactive (within profession) | Bidirectional | Autonomous in scope | Outward (to world) |
| **External communication** | None | None | Some (institutional) | Some (delegated) | Extensive |
| **Persistence** | Session | Professional context | Institutional records | Ongoing operation | Long-term life arc |
| **Replicability** | Universal product | One per profession | One per institution-type | Per task | Per individual |
| **Economics** | Subscription | Profession-wide | Institutional license | Variable | Individual or foundation |
| **Ethical concerns** | Low | Medium (mediation, standardization) | Medium (institutional power) | High (autonomy, liability) | Highest (representation, agency) |
| **Regulatory complexity** | Low | Medium (profession regs) | High (institutional regs) | Highest (delegation law) | Highest (representation law) |
| **Knowledge depth** | None | Deep (profession) | Deep + institutional | Deep (specific task) | Deep (individual) |
| **Practitioner authority** | Full | Full | Full + institutional check | Delegated zone | Strategic delegation |
| **Reference example** | ChatGPT | «Обучай» | Hospital EHR-integrated | Insurance claim AI | Proposed (none) |
| **Maturity (2026)** | Mature | Emerging | Early | Beginning | Conceptual |


### 24. 1.7. Почему это различение важно
_Файл: `docs/obsidian/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | 6 колонок, 7 строк_

| Свойство | Тип 0 | Тип 1 | Тип 2 | Тип 3 | Тип 4 |
|----------|-------|-------|-------|-------|-------|
| Специализация | Нет | Профессия | Институция+профессия | Задача | Личность |
| Внешние коммуникации | Нет | Нет | Некоторые | Некоторые | Обширные |
| Тиражируемость | Универсальная | По профессии | По институции | По задаче | По индивиду |
| Экономика | Подписка | По профессии | Институциональная | Различная | Индивидуальная |
| Этические вопросы | Низкие | Средние | Средние | Высокие | Высочайшие |
| Регуляторная сложность | Низкая | Средняя | Высокая | Высочайшая | Высочайшая |
| Готовность к развёртыванию | Зрелая | Появляющаяся | Ранняя | Начинающаяся | Концептуальная |


### 25. 3.3. Траектория развёртывания
_Файл: `docs/obsidian/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | 2 колонок, 3 строк_

| Дата | Статус |
|------|--------|
| Лето 2025 | Начало разработки |
| Сентябрь 2025 | Публичный запуск |
| Апрель 2026 | 93 000 активных учителей-пользователей |


### 26. Приложение A: Сравнительная Таблица — Пять Типов Агентов
_Файл: `docs/obsidian/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | 6 колонок, 12 строк_

| Свойство | Тип 0: Персональный AI | Тип 1: Профессиональный Коллега | Тип 2: Институциональный | Тип 3: Сотрудник | Тип 4: Представительский |
|----------|---|---|---|---|---|
| **Специализация** | Нет (общий) | Одна профессия | Профессия + институция | Конкретная задача | Конкретный индивид |
| **Направление** | Реактивный | Реактивный (в профессии) | Двунаправленный | Автономный в зоне | Внешний (к миру) |
| **Внешние коммуникации** | Нет | Нет | Некоторые (институциональные) | Некоторые (делегированные) | Обширные |
| **Постоянство** | Сессия | Профессиональный контекст | Институциональные записи | Постоянная работа | Долгосрочная жизненная траектория |
| **Тиражируемость** | Универсальный продукт | Один на профессию | Один на тип институции | По задаче | По индивиду |
| **Экономика** | Подписка | По всей профессии | Институциональная лицензия | Различная | Индивидуальная или фондом |
| **Этические озабоченности** | Низкие | Средние (опосредование, стандартизация) | Средние (институциональная власть) | Высокие (автономия, ответственность) | Высочайшие (представительство, действующая сила) |
| **Регуляторная сложность** | Низкая | Средняя (профессиональные регуляции) | Высокая (институциональные регуляции) | Высочайшая (право делегирования) | Высочайшая (право представительства) |
| **Глубина знаний** | Нет | Глубокая (профессия) | Глубокая + институциональная | Глубокая (конкретная задача) | Глубокая (индивид) |
| **Полномочия практикующего** | Полные | Полные | Полные + институциональная проверка | Делегированная зона | Стратегическое делегирование |
| **Референсный пример** | ChatGPT | «Обучай» | Больничная EHR-интегрированная | AI страховых претензий | Предложен (нет) |
| **Зрелость (2026)** | Зрелый | Появляющийся | Ранний | Начинающийся | Концептуальный |


### 27. Appendix A: The Six-Type Taxonomy (Updated)
_Файл: `docs/obsidian/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | 5 колонок, 6 строк_

| Type | Name | Specialization | Example | Maturity |
|------|------|----------------|---------|----------|
| 0 | Personal AI Assistant | None (general) | ChatGPT, Claude | Mature |
| 1 | Professional Colleague Agent | Single profession | «Обучай» for teachers | Emerging |
| **1.5** | **Composite Skills Agent** | **Configurable ensemble** | **Proposed** | **Proposed** |
| 2 | Institutional Agent | Profession + institution | Hospital EHR-integrated | Early |
| 3 | Employee Agent | Specific delegated task | Insurance claim AI | Beginning |
| 4 | Representative Agent | Single individual | Proposed (none yet) | Conceptual |


### 28. Appendix B: Comparison Matrix
_Файл: `docs/obsidian/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | 5 колонок, 9 строк_

| Capability | Plain Folder + Cowork | InGit + Cowork | Notion | Obsidian + AI plugins |
|-----------|----------------------|----------------|--------|----------------------|
| Structured organization | Manual | Conventional | Database | Markdown files |
| Versioning | Manual Git | Git native | Internal | Git via plugin |
| Metadata | None | YAML | Properties | Frontmatter |
| Validation | None | Hooks | UI rules | Plugin-dependent |
| Encryption | None | Built-in | Limited | Plugin-dependent |
| Offline | Yes | Yes | Limited | Yes |
| AI integration | Cowork | Cowork + InGit MCP | Notion AI | Plugin-dependent |
| Cross-platform | OS-dependent | Yes | Yes | Yes |
| Cost | Cowork sub | Free + Cowork | Subscription | Free + plugins |


### 29. Приложение B: Сравнительная Матрица
_Файл: `docs/obsidian/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | 5 колонок, 9 строк_

| Способность | Обычная Папка + Cowork | InGit + Cowork | Notion | Obsidian + AI плагины |
|-----------|----------------------|----------------|--------|----------------------|
| Структурированная организация | Ручная | Конвенциональная | База данных | Markdown файлы |
| Версионирование | Ручной Git | Git-нативное | Внутреннее | Git через плагин |
| Метаданные | Нет | YAML | Свойства | Frontmatter |
| Валидация | Нет | Хуки | UI правила | Зависит от плагина |
| Шифрование | Нет | Встроенное | Ограниченное | Зависит от плагина |
| Оффлайн | Да | Да | Ограниченно | Да |
| AI интеграция | Cowork | Cowork + InGit MCP | Notion AI | Зависит от плагина |
| Кросс-платформенность | Зависит от ОС | Да | Да | Да |
| Стоимость | Подписка Cowork | Бесплатно + Cowork | Подписка | Бесплатно + плагины |


### 30. Что это такое в эссенции
_Файл: `docs/obsidian/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | 3 колонок, 6 строк_

| Узел pipeline | Проект | Статус |
| --- | --- | --- |
| Habr Scout | Firecrawl + Playwright + Свяжи extraction | Working components |
| Svyazi-like карточки | Свяжи (Чуян) + knowledge-space (Анастасия) | Working |
| Collaboration Knowledge OS | AgentFS + Memory OS + knowledge-space | Working |
| Agent Team Kernel | Rufler + agent-pool + mclaude (Анастасия) | Working |
| Forensic RAG | LiteParse + Hybrid RAG + Graph RAG | Working |
| Secure Agent Runtime | SENTINEL + Shield + Claude permissions | Working |


### 31. Synthesizing с нашим existing landscape
_Файл: `docs/obsidian/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 5 колонок, 10 строк_

| Person | Project(s) | License | Status | Layer in Stack |
| --- | --- | --- | --- | --- |
| Анастасия Бутова | mclaude + knowledge-space | MIT + MIT | Active | Layers 2 & 6 |
| kagvi13 | HMP | unverified | Active | Federation (cross-cutting) |
| Андрей Чуян | Svyazi | Closed | Active | Layer 1 |
| VitalyOborin | Yodoca | Apache 2.0 | Active | Layer 4 |
| kksudo | AgentFS | MIT | Active | Layer 3 |
| spbmolot | NGT Memory | BSL 1.1 | Active | Layer 4 (alt) |
| lee-to / Cutcode | AI Factory | MIT | Active | Layer 6 |
| lib4u | Rufler | MIT | Active | Layer 6 (alt) |
| moshael | Memory OS | concept | Concept | Layer 4 (theory) |
| akazant | Self-Aware MCP | MIT | Active | Layer 7 |


### 32. Что это за документ — диагностика
_Файл: `docs/obsidian/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 3 колонок, 5 строк_

| Аспект | Первый survey | Этот документ |
| --- | --- | --- |
| Фокус | Components | Joints/contracts между components |
| Уровень | Inventory | Architecture |
| Вопрос | «Что есть?» | «Что между ними?» |
| Output | Список и сравнение | Integration contracts |
| Stage | Discovery | Specification |


### 33. Что критически нового добавляет этот документ
_Файл: `docs/obsidian/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 3 колонок, 5 строк_

| Итерация | Цель | Время |
| --- | --- | --- |
| 1: Evidence-first core | Suggestions → evidence | 1-2 weeks |
| 2: Memory governance | Truth vs proposal | 1-2 weeks |
| 3: Agented moderation | Roles: extractor/reviewer/publisher | 1-2 weeks |
| 4: Local-first ingestion | Voice → episode → vault | 1-2 weeks |
| 5: Self-improvement loop | Errors → benchmarks → patches | Continuous |


### 34. Эталонная экосистема: svend4
_Файл: `docs/obsidian/02-anthropic-vacancies/67-о-проекте.md` | 4 колонок, 3 строк_

| Репо | Формат | Содержание | Угол зрения |
| --- | --- | --- | --- |
| [info1](https://github.com/svend4/info1) | `.info1` | 74 документа с α-уровнями | Методологический |
| [pro2](https://github.com/svend4/pro2) | `.pro2` | Q6-граф концептов, 64 вершины | Семантический |
| [meta](https://github.com/svend4/meta) | `.meta` | 256 CA-правил + 64 гексаграммы | Символьный |


### 35. Reference Ecosystem: svend4
_Файл: `docs/obsidian/02-anthropic-vacancies/68-about.md` | 4 колонок, 3 строк_

| Repo | Format | Content | Perspective |
| --- | --- | --- | --- |
| [info1](https://github.com/svend4/info1) | `.info1` | 74 documents with α-levels | Methodological |
| [pro2](https://github.com/svend4/pro2) | `.pro2` | Q6-graph, 64 vertices | Semantic |
| [meta](https://github.com/svend4/meta) | `.meta` | 256 CA rules + 64 hexagrams | Symbolic |


### 36. Практические рекомендации для вашего метода
_Файл: `docs/obsidian/02-anthropic-vacancies/69-section.md` | 2 колонок, 0 строк_

| LOC | 6782 |
| Tests | 60 / 769 строк |


### 37. Практические рекомендации для вашего метода
_Файл: `docs/obsidian/02-anthropic-vacancies/69-section.md` | 2 колонок, 0 строк_

| LOC | 6600 |
| Tests | 60 / 415 строк |


### 38. Метрики (сравнение двух независимых анализов)
_Файл: `docs/obsidian/02-anthropic-vacancies/72-расписание-фазы-3.md` | 4 колонок, 5 строк_

| Метрика | Вариант A ([tdywx@abc123](link)) | Вариант B ([CzylE@def456](link)) | Статус сверки |
|---------|-----------|-----------|---------------|
| Python LOC | 6782 | 6600 | ⚠️ расходится — требует верификации |
| Tests | 60 | 60 | ✅ согласовано |
| Test lines | 769 | 415 | ⚠️ расходится — требует верификации |
| mypy errors | 0 | 0 | ✅ согласовано |
| Паспортов | 7 | 7 | ✅ согласовано |


### 39. Паспорт: /
_Файл: `docs/obsidian/02-anthropic-vacancies/79-4-passport-passport-md.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | / |
| Формат | `.` — краткое описание |
| Единица | что является одной записью |
| Адаптер | `adapters/.py` |
| Уровень совместимости | <0-3> —  |


### 40. 8.3. Q6 Mapping Rules
_Файл: `docs/obsidian/02-anthropic-vacancies/83-8-q6-space-normative.md` | 2 колонок, 4 строк_

| Format | Правило |
|--------|---------|
| `info1` | `alpha + 4` → 3 старших бита, остальные биты по категории |
| `pro2` | нативные Q6-координаты (Q6 — первичный концепт pro2) |
| `meta` | `hex_id - 1 → bin(6)` (гексаграмма 1 → `000000`, 64 → `111111`) |
| `data7` | `порядковый номер % 64 → bin(6)` |


### 41. 12.6. Path Selection Guidance
_Файл: `docs/obsidian/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | 2 колонок, 5 строк_

| Вариант | Когда использовать |
|---------|-------------------|
| **A** | Когда хорошо знаете структуру Repo и хотите high-quality |
| **B** | Стартовая точка для большинства новых Repos |
| **C** | Для Repos, которые автор хочет сам декларировать |
| **D** | Для быстрой первой интеграции незнакомых Repos |
| **E** | Для автоматической fleet-federation многих Repos |


### 42. 13.1. Required Endpoints
_Файл: `docs/obsidian/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | 3 колонок, 3 строк_

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/query?q=<text>&ranked=<0\|1>` | Поиск концептов |
| GET | `/api/describe` | Описание всех адаптеров |
| GET | `/api/health` | Состояние экосистемы (score 0–100) |


### 43. 13.1. Required Endpoints
_Файл: `docs/obsidian/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | 3 колонок, 4 строк_

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/links` | Валидация кросс-ссылок |
| GET | `/api/neighbors?q6=<bits>&dist=<N>` | Q6-соседи |
| GET | `/metrics` | Prometheus-метрики (text/plain) |
| GET | `/` | Root endpoint со списком endpoints |


### 44. 18.1. Current Reference Implementation Metrics
_Файл: `docs/obsidian/02-anthropic-vacancies/93-18-reference-implementation.md` | 2 колонок, 7 строк_

| Метрика | Значение |
|---------|----------|
| Python LOC | 6 782 |
| Адаптеров | 13 (7 реестровых + 6 расширенных) |
| Тестов | 60 / 60 passing |
| mypy errors | 0 |
| Внешних зависимостей | 0 (stdlib only) |
| Health Score | 82 / 100 |
| Q6 coverage (real) | 21.9% (14 / 64 vertices) |


### 45. Паспорт: owner/my-notes
_Файл: `docs/obsidian/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | owner/my-notes |
| Формат | `.md` — Markdown notes |
| Единица | Markdown-документ |
| Адаптер | `adapters/my_notes.py` |
| Уровень совместимости | 1 — читаемый |


### 46. 📊Сводная таблица синергии
_Файл: `docs/obsidian/03-technology-combinations/05-benchmarks.md` | 4 колонок, 8 строк_

| Комбинация | Кубики | Уникальный результат | Экономия/ROI |
| --- | --- | --- | --- |
| 1 | Агентская архитектура + Svyazi | Самообучающиеся промпты, multi-domain профилирование | 70% времени на модерацию |
| 2 | Мультиагенты + Router | Иерархический роутинг, fault tolerance | 80% бюджета на LLM |
| 3 | CRDT + Svyazi | P2P граф сообщества, offline-first discovery | Нулевые расходы на сервер |
| 4 | LLM-парсинг + Graph-RAG + Агенты | Self-building knowledge graph | 95% точность vs 60% обычного RAG |
| 5 | SourceCraft + Claude Code + Sequential | Distributed code review, team knowledge graph | 44% выше качества vs координатор |
| 6 | OpenClaude + ZINC + MoME | Локальный агент с Q6-роутером | 100% privacy, $0/мес API |
| 7 | Crawl4AI + Docling + Yodoca | Self-consolidating legal corpus | Автоматическая актуализация |
| 8 | Conductor + adversarial + Router | Multi-model adversarial, enterprise review | 3× ускорение ревью |


### 47. Статус
_Файл: `docs/obsidian/04-ai-collaborations/00-intro.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 48. Статус
_Файл: `docs/obsidian/04-ai-collaborations/01-executive-summary.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 49. Статус
_Файл: `docs/obsidian/04-ai-collaborations/02-методика-и-рамка-отбора.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 50. Статус
_Файл: `docs/obsidian/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 51. Карта найденных проектов и паттернов
_Файл: `docs/obsidian/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 2 строк_

| Проект или связка | Автор | Ссылка на статью и репо | Краткое описание | Ключевые компоненты и паттерны | Лицензия | Maturity / статус | Релевантность к Svyazi‑2.0 |
|---|---|---|---|---|---|---|---|
| **Svyazi** | Андрей Чуян | Хабр citeturn41search0 | Гибридная система извлечения структурированных профилей участников сообщества из свободного текста; уже показала кейс «карточек коллабораций». | 6 слоёв, YAML, SHA256‑дедупликация, Ollama+Qwen, LLM[^llm]+детерминированный код, CardIndex, privacy by design. | **Код закрыт**. citeturn41search0 | Активный закрытый авторский прототип. citeturn41search0 | **Очень высокая**: это базовый ingest/normalize/discovery‑слой. |
| **knowledge-space** | Sonia_Black / AnastasiyaW | Хабр + GitHub citeturn33view0turn33view2turn37search1 | Agent‑first референсная база: 785+ карточек по 26 доменам, растущая из реальных research‑сессий. | Dense reference cards, gotchas, wiki‑links,


### 52. Карта найденных проектов и паттернов
_Файл: `docs/obsidian/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 1 строк_

| **mclaude** | AnastasiyaW | Хабр + GitHub citeturn20view2turn37search0 | Координация нескольких сессий Claude Code и других coding‑агентов над одним проектом. | Locks, handoffs, mailbox, multi‑session turn‑taking, shared project memory. | **MIT**. citeturn37search0 | Активный OSS. citeturn37search0 | **Высокая**: решает параллельную работу модераторов/агентов над общим графом. |
| **AI Factory + AIF Handoff** | lee-to / Cutcode | Хабр + GitHub citeturn20view3turn29search0turn29search9 | Spec‑driven многоагентный development‑framework и автономный Kanban‑слой поверх него. | Skills, patches, self‑learning, worktrees, MCP[^mcp] handoff, plan/implement/review, WebSocket Kanban. | **MIT**. citeturn29search0turn29search9 | Активный OSS, релизы v2.x; handoff добавлен в свежих релизах. citeturn29search4 | **Высокая**: готовый оркестратор для build‑ и moderation‑контуров Svyazi‑2.0. |
| **Rufler** | zodigancode / lib4u | Хабр + repo/DEV citeturn20view4turn21view8turn32search0 | Декларативный YAML‑слой для запуска автономного роя Claude Code‑агентов. |


### 53. Карта найденных проектов и паттернов
_Файл: `docs/obsidian/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 0 строк_

| **research-docs + LiteParse** | nlaik / Jerry Liu / LlamaIndex | Хабр + GitHub citeturn20view5turn15search1turn15search5turn40search0 | Forensic document QA с HTML‑отчётом и bounding boxes на страницах PDF. | Локальный парсер, spatial text parsing, visual citations, multi‑format docs, HTML evidence report. | **Apache 2.0** для LiteParse; для samples — неуточнено в просмотренных источниках. citeturn40search0turn40search1 | Активный OSS. citeturn15search1turn15search5 | **Очень высокая**: даёт visual grounding, которого Svyazi‑подобным системам обычно не хватает. |
| **Hybrid RAG[^rag] knowledge base** | iximy | Хабр citeturn34view2 | Минималистский Hybrid RAG без тяжёлых фреймворков. |


### 54. Карта найденных проектов и паттернов
_Файл: `docs/obsidian/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 1 строк_

| **Legal RAG** | tagir_analyzes | Хабр citeturn20view6 | Подробный кейс page‑level Legal RAG с 17 итерациями и измерением пределов масштабирования. | Page‑level grounding, context distillation, систематический eval loop, error analysis. | Неуточнено. citeturn20view6 | Зрелый инженерный кейс, а не только концепт. citeturn20view6 | **Очень высокая**: лучший источник для evidence‑first и audit‑friendly retrieval. |
| **Graph RAG** | VladSpace / vpakspace | Хабр + GitHub citeturn34view3turn40search2 | Графовый RAG с provenance‑trace и typed API, собранный из 5 исследовательских техник. | Skeleton Indexing, Phrase/Passage dual nodes, VectorCypher, Datalog reasoning, agentic routing. | Неуточнено. citeturn34view3turn40search2 | Активный публичный repo / production‑ready ambition. citeturn34view3turn40search2 | **Высокая**: добавляет multi‑hop retrieval и relation‑reasoning. |
| **Yodoca** | VitalyOborin | Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1 | Локальный self‑evolving AI assistant с долговременной памятью и ночной консолидацией. | Hot/slow path, private write‑path consolidator,


### 55. Карта найденных проектов и паттернов
_Файл: `docs/obsidian/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 1 строк_

| **NGT Memory** | spbmolot / ngt-memory | Хабр + GitHub/site citeturn22view4turn22view3turn32search2 | Персистентная память для LLM‑приложений с ассоциативным графом и миллисекундным retrieval overhead. | Cosine similarity + Hebbian graph + hierarchical consolidation, REST API, Docker, 2–3 ms собственных затрат. | **BSL 1.1**; в статье прямо сказано «бесплатно для личных проектов». citeturn22view5 | Активная разработка. citeturn22view3turn32search2 | **Очень высокая**: быстрый ассоциативный memory‑слой для discovery и matching. |
| **MemNet / memory-is-all-you-need** | Antipozitive | Хабр + GitHub citeturn21view4turn17search0turn18search2 | Исследовательская активная память для трансформеров. | Hebbian graph memory, STDP, spreading activation, “dreaming”, anti‑forgetting. | **MIT**. citeturn17search0turn18search2 | Экспериментальный research codebase. citeturn17search0 | **Средне‑высокая**: не MVP‑слой, но сильная идея для future memory engine. |
| **agent-memory-mcp + Memory OS** | VitaliySemenov / moshael | Хабр + GitHub + Хабр citeturn20view16turn15search3turn39view3 | Typed memory MCP плюс более тяжёлая концепция Memory OS с онтологией, gardener‑loop и bi‑temporal facts. | SQLite+WAL, typed memories, repo/doc search, path guard; ontology, concept loop, maintenance contour, planner/scout/synthesizer. | Для


### 56. Карта найденных проектов и паттернов
_Файл: `docs/obsidian/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 8 колонок, 3 строк_

| **Self‑Aware MCP + Skills + CodeWiki** | akazant / akzhankalimatov / AnastasiyaW | Хабр + repo/marketplace + Хабр/репо citeturn20view12turn30search1turn20view15turn12search2turn37search7 | Контекст реального мира для агента плюс reusable skills и авто‑документация кодовой базы. | location/time/OS tools, skill files in repo, hooks, subagents, code wiki generation. | Self‑Aware MCP — **MIT** по карточке MCP Marketplace; config‑kit — **MIT**; CodeWiki — неуточнено. citeturn30search1turn37search7turn12search2 | Активный стек инструментов. citeturn20view12turn37search7turn12search2 | **Высокая**: делает агентный слой контекстным, переносимым и предсказуемым. |
| **Voice/local-first stack** | atatchin / askid / обзоры Handy/OpenWhispr | Хабр citeturn21view10turn21view11turn21view12turn35search0 | Локальный speech→text→LLM transform и более широкий local‑first knowledge workspace с recording/transcription. | Whisper локально, Ollama post‑processing, Handy/OpenWhispr/GigaAM, live transcription, diarization, semantic links, SQLite. | Смешанная картина; для Yttri лицензия в просмотренных источниках не уточнена. citeturn35search0turn21view11 | От usable scripts до beta‑продукта. citeturn21view10turn35search0 | **Средне‑высокая**: лучший входной канал для “raw episodes” в память. |
| **Yjs + Automerge** | Kevin Jahns / Automerge team | Документация и репо citeturn11search0turn11search7turn11search13turn11search1turn11search11turn11search23 | Базовый local‑first/CRDT[^crdt] sync‑слой для оффлайн‑совместимости и мультидевайсной синхронизации. | Shared types, automatic merge without conflicts, offline sync, local‑first data engine. | **MIT**. citeturn11search13turn11search23 | Активный OSS. citeturn11search13turn11search11 | **Средняя**, но стратегически важная: синхронизация между устройствами и узлами. |
| **Security + routing plane** | Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig | Хабр + GitHub/docs citeturn20view10turn11search2turn19search5turn39view0turn39view1turn20view18 | Рантайм‑безопасность и бюджетный execution plane для агентных систем. | SENTINEL[^sentinel] micro‑model swarm; LiteLLM unified API; Auto AI Router on Go; Tool Search lazy MCP loading; budget/privacy presets in RLM‑Toolkit. | Смешанная: SENTINEL — неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2.0. citeturn20view10turn19search5turn28search3 | Активный operational stack. citeturn20view10turn11search2turn39view0turn39view1 | **Очень высокая**: без этого Svyazi‑2.0 будет либо дорогой, либо небезопасной. |
| **AutoResearch + Sequential** | Андрей Карпаты / Виктория Дочкина | Хабр + GitHub/обзор citeturn20view19turn20view11 | Ночной цикл самоулучшения и протокол reviewer‑цепочки без централизованного координатора. | Edit‑run‑measure‑rollback loop, bounded experiments, sequential protocol, strong-model self‑organization. | Для AutoResearch — по статье на GitHub; лицензия в Habr‑обзоре не уточнялась. Для Sequential — исследовательская статья без OSS‑лицензии. citeturn20view19turn20view11 | Active research / practical harness. citeturn20view19turn20view11 | **Высокая**: это кандидат на self‑improvement и multi‑review для Svyazi‑2.0. |


### 57. Статус
_Файл: `docs/obsidian/04-ai-collaborations/04-приоритетные-ансамбли.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 58. Статус
_Файл: `docs/obsidian/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 59. План прототипа и возможные контакты
_Файл: `docs/obsidian/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 4 колонок, 5 строк_

| Контур | Что входит | Зачем | Оценка усилий |
|---|---|---|---|
| Ядро данных | CardIndex‑схема, профили, raw/inferred разделение, файловый vault в стиле AgentFS | Сделать единый source of truth и трассируемый lifecycle карточки | 2–3 дня |
| Ingest и память | LLM[^llm] extraction + нормализация + NGT Memory **или** Yodoca‑lite | Доказать, что из свободного текста получаются устойчивые профили и связи | 4–6 дней |
| Evidence | LiteParse/research-docs + page‑level viewer | Не просто показать match, а показать основание | 3–4 дня |
| Исполнение | LiteLLM/Auto AI Router + Tool Search + базовые правила безопасности | Удержать стоимость и не утонуть в MCP[^mcp]/context overhead | 2–3 дня |
| Guardrails | PII[^pii]‑фильтры, allowlists, manual review для inferred | Снизить риск ложных связей и утечек | 1–2 дня |


### 60. План прототипа и возможные контакты
_Файл: `docs/obsidian/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 3 колонок, 2 строк_

| Риск | Почему это важно | Снижение риска |
|---|---|---|
| Schema drift и самовольная “оптимизация” структуры моделью | На extraction‑этапе сильная модель может начать “улучшать” схему вместо исполнения | Держать extraction на constrained schema + низком reasoning, а смысл переносить в post‑processing; это совпадает и с логикой Svyazi, и с выводами Memory OS. citeturn41search0turn39view3 |
| Ложные ассоциации в памяти | Ассоциативная память полезна, но легко порождает шум | Вводить review queue для


### 61. План прототипа и возможные контакты
_Файл: `docs/obsidian/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 3 колонок, 1 строк_

| Утечка PII в карточки и prompts | Discovery‑система почти неизбежно работает с чувствительными профилями | Повторить Svyazi‑паттерн privacy‑by‑design, хранить контакты отдельно, использовать allowlist/path guard, локальные embeddings там, где можно. citeturn41search0turn20view16turn35search0 |
| Лицензионный тупик на memory‑слое | Не все “open” memory‑решения одинаково permissive | Если нужен строго permissive/commercial‑friendly стек, NGT Memory надо проверять отдельно, потому что в статье указана BSL[^bsl] 1.1 и free‑for‑personal grant; на таком пути проще начать с Yodoca или agent-memory-mcp. citeturn22view5turn18search1turn15search3 |
| Многоагентный хаос раньше пользы | Рой даёт выгоду только после появления handoff/lock и чётких спецификаций | Начинать с mclaude + AI Factory/AIF Handoff, а Rufler/Sequential/AutoResearch добавлять после того, как появилась стабильная spec и критерии качества. citeturn20view2turn20view3turn20view4turn20view11turn20view19 |


### 62. План прототипа и возможные контакты
_Файл: `docs/obsidian/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 4 колонок, 3 строк_

| Кому писать | Почему именно он или она | Публичный вектор из просмотренных источников | Контакт в источниках |
|---|---|---|---|
| **andrey_chuyan** | Единственный из найденных авторов, у кого уже есть рабочий кейс “карточки коллаборации” и CardIndex‑мышление. citeturn41search0 | Комментарии к статье Svyazi на Хабре. citeturn41search0 | Публичный email/Telegram в просмотренных источниках **не найден**. |
| **Sonia_Black / AnastasiyaW** | Закрывает сразу два слоя: knowledge-space и multi-session coordination через mclaude. citeturn33view3turn20view2turn37search0 | Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn33view0turn37search0 | Публичный прямой контакт **не найден**. |
| **kksudo** | Наиболее важный кандидат для слоя


### 63. План прототипа и возможные контакты
_Файл: `docs/obsidian/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 4 колонок, 0 строк_

| **VitalyOborin** | Сильнейший кандидат на consolidator/forgetting‑слой. citeturn21view0turn21view1turn18search1 | Комментарии к статье Yodoca и GitHub issues/discussions в repo. citeturn38view7turn18search1 | Публичный прямой контакт **не найден**. |
| **spbmolot** | Нужен для ассоциативной памяти и очень дешёвого memory retrieval с graph‑подтягиванием слабых связей. citeturn22view4turn22view5 | Комментарии к статье NGT Memory и GitHub repository. citeturn22view5turn32search2 | Публичный прямой контакт **не найден**. |


### 64. Статус
_Файл: `docs/obsidian/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 65. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/obsidian/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 3 колонок, 3 строк_

| Контроль | Практический дефолт | Основание |
|---|---|---|
| Разделение tool‑классов | По умолчанию разрешать read‑only tools; любые send/write/delete/execute — только через явный approval | Автономный агент отличается от чатбота именно доступом к реальным действиям; это и создаёт катастрофы. citeturn34view5 |
| Quarantine для external skills/MCP | Любой внешний skill/MCP сначала в sandbox, потом статический/репутационный скан, потом allowlist | AI Factory прямо предупреждает о prompt injection в SKILL.md и запускает двухуровневый security scan. citeturn29search6 |
| Path allowlist | Жёстко ограничить, что агент вообще может читать и писать на диске |


### 66. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/obsidian/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 3 колонок, 0 строк_

| PII[^pii] separation | Любые контакты, email, Telegram, ссылки — в отдельном raw‑слое; в карточки уходит только очищенный профиль | Так делает Svyazi; это правильный privacy‑baseline для людей и сообществ. citeturn41search0 |
| Truth vs Proposal |


### 67. Безопасность, приватность и бюджетный роутинг
_Файл: `docs/obsidian/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 3 колонок, 6 строк_

| Этап | Дефолт | Когда эскалировать |
|---|---|---|
| Extraction из свободного текста | Локальная или дешёвая модель + строгая schema guidance | Только если extraction‑quality стабильно проваливает ваши acceptance tests |
| Нормализация | Детерминированный код | Практически никогда не переводить это на дорогую модель |
| Retrieval / rerank | Non‑LLM[^llm] hybrid retrieval или локальный reranker | При multi-hop вопросах и слабой explainability |
| Объяснение матча / summary | Средний облачный tier | Если нужен высокий stylistic quality, а не только фактология |
| Финальный внешний отчёт | Сильная модель | Только для user-facing/public/legal‑style текста |
| Ночной ресёрч / оптимизация | AutoResearch‑подход с жёстким бюджетом и rollback | Когда уже есть benchmark и понятная функция качества |


### 68. Статус
_Файл: `docs/obsidian/04-ai-collaborations/07-выводы.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 69. Статус
_Файл: `docs/obsidian/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 70. Статус
_Файл: `docs/obsidian/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 71. Архитектурные зазоры, которые важнее новых инструментов
_Файл: `docs/obsidian/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 5 колонок, 5 строк_

| Архитектурный зазор | Уже сильные кандидаты | Что в них уже хорошо закрыто | Что пока остаётся незакрытым | Что брать в MVP |
|---|---|---|---|---|
| Карточка как единица правды | Svyazi, AgentFS | CardIndex, hash/dedup, versionable vault, persistent state | Универсальная типизация для person/project/doc/episode/hypothesis | Card schema + raw/inferred split + immutable IDs citeturn41search0turn27view0turn33view4 |
| Доказуемое основание вывода | research-docs/LiteParse, Legal RAG, Hybrid RAG | Bounding boxes, page-level grounding, coordinates, transparent retrieval | Единый формат “evidence pack” между retrieval и интерфейсом | Page-level viewer + source_id/page/span/box schema citeturn20view5turn20view6turn34view2 |
| Память с контролируемым статусом | NGT Memory, Yodoca, agent-memory-mcp, Memory OS | Associative retrieval, consolidation, forgetting, typed memory, guard rails | Чёткая граница truth/proposal/conflict/decayed | Pending queue + confidence/state machine на наполнение графа citeturn22view4turn21view0turn20view16turn39view3 |
| Оркестрация и review | mclaude, AI Factory, Rufler, Sequential | Locks, mailbox, patch learning, YAML swarm, sequential review | Стандарт handoff для non-code workflow и knowledge moderation | 2–3 роли: extractor → reviewer → publisher citeturn20view2turn20view3turn20view4turn20view11 |
| Безопасный execution plane | LiteLLM, Auto AI Router, Tool Search, SENTINEL | Unified API, lightweight routing, lazy tool loading, runtime guard | Общая policy matrix на tool classes и external skills | Read-only by default + write approval + path allowlist citeturn11search2turn39view0turn39view1turn20view10turn20view16 |


### 72. Статус
_Файл: `docs/obsidian/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 73. Статус
_Файл: `docs/obsidian/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 74. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/obsidian/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 4 колонок, 1 строк_

| Контракт | Минимальные поля | Зачем нужен в MVP | На какие идеи опирается |
|---|---|---|---|
| Card Envelope |


### 75. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/obsidian/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 0 строк_

| Единый source of truth и dedup/version trace | Svyazi, AgentFS, Memory OS citeturn41search0turn27view0turn39view3 |
| Evidence Envelope |


### 76. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/obsidian/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 0 строк_

| Проверяемость выводов и ручной review | LiteParse, Legal RAG, Hybrid/Graph RAG citeturn20view5turn20view6turn34view2turn34view3 |
| Memory Write Policy |


### 77. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/obsidian/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 0 строк_

| Развести факт, эпизод и гипотезу | Yodoca, NGT Memory, agent-memory-mcp citeturn21view0turn22view4turn20view16 |
| Skill Policy |


### 78. Интеграционный контракт, который стоит зафиксировать сразу
_Файл: `docs/obsidian/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 2 колонок, 0 строк_

| Снизить blast radius и упростить audit | Tool Search, SENTINEL, AI Factory practices citeturn39view1turn20view10turn29search6 |
| Review Record |


### 79. Статус
_Файл: `docs/obsidian/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 80. Дорожная карта прототипа следующей итерации
_Файл: `docs/obsidian/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | 5 колонок, 5 строк_

| Итерация | Главная цель | Минимум, который должен заработать | Оценка усилий | Главный риск |
|---|---|---|---|---|
| Evidence-first core | Из любого suggestions можно перейти к основанию | Unified cards + page/span evidence + manual reviewer UI | 1–2 недели | Переусложнение схемы слишком рано |
| Memory governance | Ассоциации перестают путаться с фактами | Episode store + proposal queue + approval/decay states | 1–2 недели | Ложная уверенность в “умной памяти” без жёсткого review |
| Agented moderation | Рой помогает, а не создаёт шум | extractor/reviewer/publisher roles + handoff/journal | 1–2 недели | Многоагентный хаос без хороших критериев качества |
| Local-first ingestion | Система начинает жить в ежедневном потоке | voice→episode, local vault, selective sync | 1–2 недели | Sync-конфликты и таскание лишних данных наружу |
| Self-improvement loop | Ошибки превращаются в benchmark и patch | benchmark set + nightly eval + rollback policy | 1 неделя на каркас, дальше непрерывно | Большой соблазн автоматизировать раньше, чем появилась метрика |


### 81. Статус
_Файл: `docs/obsidian/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 82. Контактная стратегия и узкие вопросы для авторов
_Файл: `docs/obsidian/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 3 колонок, 1 строк_

| Кому | Лучший первый вопрос | Почему именно он |
|---|---|---|
| entity["people","Андрей Чуян","habr author"] | Стоит ли расширять CardIndex до


### 83. Контактная стратегия и узкие вопросы для авторов
_Файл: `docs/obsidian/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 3 колонок, 1 строк_

| entity["people","Виталий Оборин","software engineer"] | Что сильнее всего влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? | Это позволяет использовать Yodoca как policy reference, а не как “ещё один ассистент”. citeturn21view0turn21view1 |
| **spbmolot** | Где проходит практическая граница между полезной ассоциацией и ложной ко‑активацией тем? | Это самый важный вопрос для community matching. citeturn22view4turn22view5 |
| **авторы knowledge-space / mclaude** | Держать операционные benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? | Это шов между памятью, знаниями и orchestration. citeturn33view2turn20view2 |


### 84. Статус
_Файл: `docs/obsidian/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 85. Статус
_Файл: `docs/obsidian/05-habr-projects/01-synthesis.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 86. Статус
_Файл: `docs/obsidian/05-habr-projects/02-collaboration-partners.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | — |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 87. Статус
_Файл: `docs/obsidian/05-habr-projects/knowledge/wikontic.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 90 |
| Слой | — |
| Контакт | — |
| Статус связи | не писали |


### 88. Статус
_Файл: `docs/obsidian/05-habr-projects/memory/memnet.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 90 |
| Слой | memory |
| Контакт | [[antipozitive|@Antipozitive]] |
| Статус связи | не писали |


### 89. Статус
_Файл: `docs/obsidian/05-habr-projects/memory/ngt-memory.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 260 |
| Слой | memory |
| Контакт | [[spbmolot|@spbmolot]] |
| Статус связи | не писали |


### 90. Статус
_Файл: `docs/obsidian/05-habr-projects/memory/yodoca.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 229 |
| Слой | memory |
| Контакт | [[vitalyoborin|@VitalyOborin]] |
| Статус связи | не писали |


### 91. Словарь аббревиатур и сокращений
_Файл: `docs/obsidian/ABBREVIATIONS.md` | 3 колонок, 85 строк_

| Аббревиатура | Расшифровка | Упоминаний |
|-------------|-------------|------------|
| **ACD** | Automated Capability Discovery — ещё один сильный кубик: модель в роли «учёного» систематически генерирует задачи для мо | 5 |
| **ADR** | "ADR-004: Temporal Metadata as First-Class Concept" | 79 |
| **AGENTS** | типология + готовая к развёртыванию категория Type 1 | 33 |
| **AI** | это инфраструктурный слой для AI-managed virtual companies | 2337 |
| **AIRI** | серьёзная research лаборатория (Артём Шелманов и команда) | 16 |
| **ANP** | Agent Network Protocol | 4 |
| **API** ⭐ | Application Programming Interface — интерфейс программирования приложений | 250 |
| **BSL** ⭐ | Business Source License — бизнес-лицензия с открытым кодом | 65 |
| **CAMEL** | это другая значимая open-source framework, и сравнение их с Hermes будет показательным | 173 |
| **CI/CD** ⭐ | Continuous Integration / Continuous Deployment | 8 |
| **CLI** ⭐ | Command Line Interface — интерфейс командной строки | 51 |
| **CRDT** ⭐ | Conflict-free Replicated Data Type — структура данных без конфликтов слияния | 54 |
| **DAO** | результат смешанный | 2 |
| **EMEA** | RU/DE/EN на рабочем уровне, базирование в Германии, понимание европейского регуляторного контекста (что прямо читается ч | 25 |
| **ERROR** | MCP SDK not installed | 2 |
| **FAQ** ⭐ | Frequently Asked Questions — часто задаваемые вопросы | 36 |
| **FDE** | это исполнительская роль на чужую продуктовую повестку | 10 |
| **FRE** | 70-100 лёгкий, 50-70 средний, 30-50 сложный, <30 очень сложный | 14 |
| **GDPR** ⭐ | General Data Protection Regulation — европейский регламент защиты данных | 50 |
| **GG** | они публичные) | 1 |
| **GUI** | -3 months effort | 14 |
| **HEAD** | 7 commits) | 5 |
| **HMP** | на когнитивной устойчивости и этике | 85 |
| **ID** | sgb:XII:90:4 (SGB XII, § 90, Abs | 6 |
| **II** | The Double-Triangle Architecture — formal описание дуальной структуры с вашей метафорой звезды Давида | 21 |
| **III** | Protocols Between Layers — три протокола с examples | 16 |
| **INPUT** | - Bescheid text (decoded by agent) | 1 |
| **IP** | AI-платформа, заказчик, сами фрилансеры? Сегодняшние legal frameworks не умеют отвечать на этот вопрос дёшево | 6 |
| **IV** | Nautilus Portal as Reference Implementation — как existing work serves как substrate | 18 |
| **IX** | 102 , sgg:86b:2 ), на прецеденты | 40 |
| **JWT** ⭐ | JSON Web Token — токен аутентификации | 2 |
| **KPI** | сколько полезных коллабораций, проектов, выступлений, mentorship‑пар или hiring‑контактов возникло из рекомендаций систе | 39 |
| **KSV** | потому что у них нет точных русских эквивалентов в контексте немецкой социально-правовой системы | 28 |
| **LAYER** | функциональная категория Type 4 | 55 |
| **LCI** | Lyapunov Coherence Index, target π | 22 |
| **LLM** ⭐ | Large Language Model — большая языковая модель | 322 |
| **LOC** | продублирована с разными строками в разных частях | 48 |
| **MCP** ⭐ | Model Context Protocol — протокол контекста для AI-инструментов | 792 |
| **MIT** ⭐ | Massachusetts Institute of Technology License — разрешительная лицензия | 241 |
| **ML** | несколько моделей → voting/averaging | 54 |
| **MMORPG** | это общее пространство , в котором вы видите аватары коллег, можете подойти к ним, стоять рядом, работать вместе в одной | 40 |
| **MRR** | это уже leverage для любого следующего шага, включая разговор с Anthropic Institute о grant/partnership | 2 |
| **MUST** | - Возвращать пустой список, если ничего не найдено (не `None`, не exception) | 76 |
| **MVP** ⭐ | Minimum Viable Product — минимально жизнеспособный продукт | 206 |
| **NDA** | intermediate view (placeholder'ы, но с consistent identifiers для longitudinal анализа) | 1 |
| **NGT** | граф памяти](#глава-11-ngt-граф-памяти) | 263 |
| **NLP** ⭐ | Natural Language Processing — обработка естественного языка | 0 |
| **NPP** | **федеративная модель**, где каждый | 84 |
| **OASIS** | до 1M agents simulation) | 3 |
| **ODT** | не только текст | 1 |
| **OKWF** | конкретная архитектура](#применение-к-okwf-конкретная-архитектура) | 313 |
| **OPTIONAL** | ключевые слова | 9 |
| **OS** | неуточнено | 129 |
| **OSS** ⭐ | Open Source Software — программное обеспечение с открытым кодом | 212 |
| **OUTPUT** | - Draft Widerspruch (DOCX format) | 1 |
| **P2P** ⭐ | Peer-to-Peer — децентрализованная сеть | 14 |
| **PARC** | research center, became iconic несмотря на parent brand decline OpenAI — research org становящаяся product company, name | 2 |
| **PII** ⭐ | Personally Identifiable Information — персональные данные | 42 |
| **PROTOCOL** | иначе future разработчики будут gадать | 215 |
| **PURE** | LLM-based User Profile Management for Recommender System» | 5 |
| **QA** | демон-критик (adversarial, rigorous) | 179 |
| **RAG** ⭐ | Retrieval-Augmented Generation — генерация с поиском по базе знаний | 427 |
| **README** | 550+ строк production-качества: установка, конфигурация для всех 6 платформ (включая детализацию /etc/fstab для CIFS, AD | 858 |
| **REQUIRED** | откуда пришло | 22 |
| **ROI** | 10 sec queries vs 2 hour manual search | 15 |
| **SDK** ⭐ | Software Development Kit — набор инструментов разработчика | 59 |
| **SENTINEL** | неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2 | 184 |
| **SF** | DC, Canberra) | 17 |
| **SGB** ⭐ | Sozialgesetzbuch — Социальный кодекс Германии | 370 |
| **SHOULD** | - Поддерживать case-insensitive matching для текстовых запросов | 36 |
| **SWE** | в Sales/Finance/Marketing/Legal зарплаты ниже и сильно варьируются по локации | 5 |
| **TF-IDF** ⭐ | Term Frequency–Inverse Document Frequency — метрика важности термина | 13 |
| **TODO** ⭐ | To Do — задача к выполнению | 3 |
| **TSU** | физика, MoME — математика; ZINC — software, гибридная архитектура — алгоритм; RISC-V — кремний, privacy — право; TinyML  | 9 |
| **TVCP** | Terminal Video Communication Platform, терминал видео коммуникация платформа, игры») — это необычное : Go + template + M | 1 |
| **UI** | -2 months effort | 62 |
| **URL** | я разберусь с любым вариантом именования | 73 |
| **VERIFY** | 6782 vs 6600] как метку | 1 |
| **VI** | Deployment Paths — humanities, project management, OSS, general | 3 |
| **VII** | Open Questions — governance, consent, economics, scale | 3 |
| **VIII** | Call to Action — что делать researchers, practitioners, founders | 2 |
| **VPS** | cron каждое утро обходит сайты Sozialgericht/BSG/KSV, генерирует Stellungnahme-черновики, обновляет статусы Aktenzeichen | 10 |
| **XII** | legally binding reference с нормативной силой | 37 |
| **YAML** ⭐ | YAML Ain't Markup Language — формат конфигурационных файлов | 107 |
| **ZINC** | - Ночью агент крутит эксперименты с промптами | 26 |


### 92. Самые часто используемые
_Файл: `docs/obsidian/ABBREVIATIONS.md` | 2 колонок, 15 строк_

| Аббревиатура | Упоминаний |
|-------------|------------|
| **AI** | 2337 — _это инфраструктурный слой для AI-managed virtual companies_ |
| **README** | 858 — _550+ строк production-качества: установка, конфигурация для _ |
| **MCP** | 792 — _Model Context Protocol — протокол контекста для AI-инструмен_ |
| **RAG** | 427 — _Retrieval-Augmented Generation — генерация с поиском по базе_ |
| **SGB** | 370 — _Sozialgesetzbuch — Социальный кодекс Германии_ |
| **LLM** | 322 — _Large Language Model — большая языковая модель_ |
| **OKWF** | 313 — _конкретная архитектура](#применение-к-okwf-конкретная-архите_ |
| **NGT** | 263 — _граф памяти](#глава-11-ngt-граф-памяти)_ |
| **API** | 250 — _Application Programming Interface — интерфейс программирован_ |
| **MIT** | 241 — _Massachusetts Institute of Technology License — разрешительн_ |
| **PROTOCOL** | 215 — _иначе future разработчики будут gадать_ |
| **OSS** | 212 — _Open Source Software — программное обеспечение с открытым ко_ |
| **MVP** | 206 — _Minimum Viable Product — минимально жизнеспособный продукт_ |
| **SENTINEL** | 184 — _неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI_ |
| **QA** | 179 — _демон-критик (adversarial, rigorous)_ |


### 93. Callout-блоки
_Файл: `docs/obsidian/ALERTS.md` | 3 колонок, 4 строк_

| Тип | Количество | Назначение |
|-----|------------|------------|
| `[!NOTE]` | 0 | Нейтральная заметка |
| `[!TIP]` | 42 | Практический совет |
| `[!WARNING]` | 10 | Предупреждение о риске |
| `[!IMPORTANT]` | 5 | Ключевой документ |


### 94. Авторы и коллаборации
_Файл: `docs/obsidian/AUTHORS.md` | 2 колонок, 25 строк_

| Автор | Упоминается в файлах |
|-------|---------------------|
| **AnastasiyaW** | 35 |
| **Antipozitive** | 19 |
| **BerriAI** | 7 |
| **Cutcode** | 33 |
| **Dmitriila** | 31 |
| **MiXaiLL76** | 32 |
| **Sonia_Black** | 16 |
| **VitaliySemenov** | 4 |
| **VitalyOborin** | 33 |
| **VladSpace** | 30 |
| **akazant** | 6 |
| **akzhankalimatov** | 4 |
| **andrey_chuyan** | 16 |
| **iximy** | 5 |
| **kksudo** | 61 |
| **lee-to** | 8 |
| **lib4u** | 7 |
| **moshael** | 6 |
| **nlaik** | 23 |
| **spbmolot** | 59 |
| **tagir_analyzes** | 19 |
| **vpakspace** | 4 |
| **zodigancode** | 26 |
| **Андрей Чуян** | 21 |
| **Виталий Оборин** | 7 |


### 95. Топ-30 самых цитируемых документов
_Файл: `docs/obsidian/BACKLINKS.md` | 3 колонок, 30 строк_

| Документ | Входящих ссылок | Ссылающиеся файлы |
|----------|----------------|-------------------|
| `README` | 10 | `.md`, `cowork.md`, `ingit.md`, `kksudo.md` +6 |
| `07-mvp-planning` | 3 | `README.md`, `PROGRESS.md`, `REPORT.md` |
| `CONTACTS` | 3 | `PROGRESS.md`, `README.md`, `REPORT.md` |
| `HEALTH` | 3 | `PROGRESS.md`, `README.md`, `REPORT.md` |
| `kksudo` | 2 | `CONTACT_PRIORITY.md`, `README.md` |
| `anastasiyaw` | 2 | `CONTACT_PRIORITY.md`, `README.md` |
| `spbmolot` | 2 | `CONTACT_PRIORITY.md`, `README.md` |
| `SCORING` | 2 | `PROGRESS.md`, `README.md` |
| `NARRATIVE` | 2 | `README.md`, `REPORT.md` |
| `DECISIONS` | 2 | `README.md`, `REPORT.md` |
| `SIMILAR` | 2 | `README.md`, `REPORT.md` |
| `SITEMAP` | 2 | `README.md`, `REPORT.md` |
| `QUESTIONS` | 2 | `README.md`, `REPORT.md` |
| `KPI` | 2 | `README.md`, `REPORT.md` |
| `READING_ORDER` | 2 | `README.md`, `REPORT.md` |
| `VALIDATION` | 2 | `README.md`, `REPORT.md` |
| `BROKEN_LINKS` | 2 | `README.md`, `REPORT.md` |
| `12-roadmap` | 1 | `README.md` |
| `06-security-privacy` | 1 | `README.md` |
| `08-conclusions` | 1 | `README.md` |
| `02-methodology` | 1 | `README.md` |
| `00-intro-part2` | 1 | `README.md` |
| `01-executive-summary` | 1 | `README.md` |
| `10-second-order-ensembles` | 1 | `README.md` |
| `13-contacts` | 1 | `README.md` |
| `14-limitations` | 1 | `README.md` |
| `QA` | 1 | `README.md` |
| `04-ensembles-overview` | 1 | `README.md` |
| `03-component-catalog` | 1 | `README.md` |
| `ensembles` | 1 | `README.md` |


### 96. Ссылки по разделам
_Файл: `docs/obsidian/BACKLINKS.md` | 3 колонок, 10 строк_

| Раздел | Входящих | Исходящих |
|--------|----------|-----------|
| **01-svyazi** | 18 | 16 |
| **02-anthropic-vacancies** | 357 | 357 |
| **03-technology-combinations** | 6 | 6 |
| **04-ai-collaborations** | 17 | 17 |
| **05-habr-projects** | 9 | 9 |
| **autofilled** | 22 | 22 |
| **badges** | 0 | 0 |
| **contacts** | 17 | 14 |
| **root** | 109 | 114 |
| **templates** | 5 | 5 |


### 97. Статистика коммитов
_Файл: `docs/obsidian/CHANGELOG_AUTO.md` | 3 колонок, 5 строк_

| Тип | Название | Кол-во |
|-----|---------|--------|
| `feat` | ✨ Новые возможности | 17 |
| `fix` | 🐛 Исправления | 3 |
| `docs` | 📝 Документация | 2 |
| `chore` | 🔧 Технические задачи | 10 |
| `other` | 📌 Прочее | 16 |


### 98. Топ доменов
_Файл: `docs/obsidian/CITATION_INDEX.md` | 3 колонок, 20 строк_

| Домен | URL | Авторитетность |
|-------|-----|----------------|
| `github.com` | 55 | ⭐⭐⭐⭐⭐ |
| `habr.com` | 41 | ⭐⭐⭐⭐ |
| `raw.githubusercontent.com` | 11 | ⭐ |
| `3dnews.ru` | 2 | ⭐ |
| `claude.ai` | 2 | ⭐ |
| `api.github.com` | 2 | ⭐⭐⭐⭐⭐ |
| `fontanka.ru` | 1 | ⭐ |
| `eb.hypothes.is` | 1 | ⭐ |
| `discourse.org` | 1 | ⭐ |
| `claude.com` | 1 | ⭐ |
| `support.claude.com` | 1 | ⭐ |
| `fossil-scm.org` | 1 | ⭐ |
| `install.sh` | 1 | ⭐ |
| `happyin.space` | 1 | ⭐ |
| `creativecommons.org` | 1 | ⭐ |
| `solidproject.org` | 1 | ⭐ |
| `3.org` | 1 | ⭐ |
| `activitypub.rocks` | 1 | ⭐ |
| `vc.ru` | 1 | ⭐ |
| `habr` | 1 | ⭐ |


### 99. Наиболее цитируемые URL
_Файл: `docs/obsidian/CITATION_INDEX.md` | 4 колонок, 50 строк_

| URL | Файлов | Авторитетность | Домен |
|-----|--------|----------------|-------|
| `https://github.com/svend4/nautilus/issues` | 17 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/ingit` | 12 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/nautilus` | 10 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/pro2` | 7 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/info1` | 6 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/mcp` | 5 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/AnastasiyaW/knowledge-space` | 5 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/data70` | 4 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/meta` | 4 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://habr.com/ru/articles/1006622/` | 4 | ⭐⭐⭐⭐ | `habr.com` |
| `https://github.com/settings/tokens` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/ingit/issues` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/anthropics/mcp` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/camel-ai/camel` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/AnastasiyaW` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/spbmolot` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/kksudo` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://habr.com/ru/articles/938626/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1009608/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1005776/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1002138/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/yoomoney/articles/1012870/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/975414/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1020860/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1016096/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027210/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1007122/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1024884/comments/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1024634/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/955798/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1020598/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/surfstudio/articles/943108/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1009538/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/996144/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/yandex/articles/1019928/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027878/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1023446/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/983684/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1006602/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1010198/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/943498/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027382/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1010478/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/airi/articles/855128/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1017200/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1019588/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1009958/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/893356/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/airi/articles/1000720/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027658/` | 3 | ⭐⭐⭐⭐ | `habr.com` |


### 100. Содержание
_Файл: `docs/obsidian/CODE_BLOCKS.md` | 2 колонок, 7 строк_

| Язык | Блоков |
|------|--------|
| 📝 Без языка | 151 |
| 💻 Bash / Shell | 27 |
| 🐍 Python | 17 |
| 📦 JSON | 13 |
| 📊 Диаграммы Mermaid | 10 |
| markdown | 8 |
| 📋 YAML | 5 |


### 101. Паспорт: /
_Файл: `docs/obsidian/CODE_BLOCKS.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | / |
| Формат | `.` — краткое описание |
| Единица | что является одной записью |
| Адаптер | `adapters/.py` |
| Уровень совместимости | <0-3> —  |


### 102. Изменившиеся файлы (343) — топ по Δ слов
_Файл: `docs/obsidian/COMPARE.md` | 4 колонок, 30 строк_

| Файл | Было | Стало | Δ |
|------|------|-------|---|
| `TABLES.md` | 15654 | 63292 | +47638 |
| `README.md` | 3693 | 2162 | -1531 |
| `SEARCH.md` | 3524 | 4370 | +846 |
| `ACTION_ITEMS.md` | 5816 | 6656 | +840 |
| `SITEMAP.md` | 1449 | 2206 | +757 |
| `CHANGELOG.md` | 197 | 888 | +691 |
| `README.md` | 54 | 622 | +568 |
| `QA.md` | 1521 | 979 | -542 |
| `WORD_FREQ.md` | 1262 | 1790 | +528 |
| `CLUSTERS.md` | 1231 | 1612 | +381 |
| `LINKS.md` | 647 | 969 | +322 |
| `CHANGELOG_AUTO.md` | 322 | 627 | +305 |
| `BROKEN_LINKS.md` | 438 | 726 | +288 |
| `RISK_REGISTER.md` | 785 | 1043 | +258 |
| `README.md` | 345 | 113 | -232 |
| `README.md` | 330 | 126 | -204 |
| `177-8-risks-and-mitigations.md` | 471 | 666 | +195 |
| `178-9-phased-rollout-strategy.md` | 452 | 636 | +184 |
| `264-11-open-questions.md` | 455 | 638 | +183 |
| `00-intro.md` | 11272 | 11445 | +173 |
| `INDEX.md` | 514 | 685 | +171 |
| `317-9-risks-and-open-questions.md` | 484 | 653 | +169 |
| `163-9-call-for-partnership.md` | 443 | 610 | +167 |
| `DEPENDENCY_MAP.md` | 508 | 675 | +167 |
| `01-executive-summary.md` | 481 | 647 | +166 |
| `175-6-ethical-framework.md` | 446 | 611 | +165 |
| `ngt-memory.md` | 255 | 419 | +164 |
| `wikontic.md` | 144 | 306 | +162 |
| `316-8-implications-for-nautilus-and-okwf.md` | 539 | 696 | +157 |
| `314-6-refined-ingit-scope-with-cowork-in-mind.md` | 364 | 513 | +149 |


### 103. Распределение сложности
_Файл: `docs/obsidian/COMPLEXITY.md` | 2 колонок, 3 строк_

| Уровень | Файлов |
|---------|--------|
| 🟢 Простой (0-1) | 360 |
| 🟡 Средний (2-3)  | 119 |
| 🔴 Сложный (4-5)  | 40 |


### 104. Самые сложные документы
_Файл: `docs/obsidian/COMPLEXITY.md` | 6 колонок, 25 строк_

| Документ | Слов | Ср.длина пред. | Термин.плотность | Ур.заголовков | Балл |
|----------|------|---------------|-----------------|--------------|------|
| `342-что-такое-вариант-c-concept-doc` | 10594 | 26.7 | 0.17% | H5 | 🔴 Сложный |
| `343-lorenzo-catalyst-agent-глубокая` | 5653 | 26.5 | 0.25% | H5 | 🔴 Сложный |
| `00-intro` | 8733 | 18.0 | 0.25% | H4 | 🔴 Сложный |
| `01-интегральный-анализ-профиля-sven` | 18866 | 15.8 | 0.14% | H4 | 🔴 Сложный |
| `133-обратная-связь` | 3644 | 17.5 | 0.36% | H4 | 🔴 Сложный |
| `150-appendix-c-version-history` | 4856 | 20.1 | 0.02% | H4 | 🔴 Сложный |
| `272-appendix-d-connection-diagram` | 3735 | 15.3 | 0.03% | H4 | 🔴 Сложный |
| `303-приложение-визуализация-позиции` | 1801 | 18.8 | 1.17% | H4 | 🔴 Сложный |
| `341-приложение-c-образец-спецификац` | 3503 | 24.5 | 0.43% | H4 | 🔴 Сложный |
| `365-развёрнутый-анализ-внуковой-ком` | 4114 | 18.2 | 1.0% | H4 | 🔴 Сложный |
| `03-local-first` | 357 | 20.3 | 3.64% | H4 | 🔴 Сложный |
| `05-benchmarks` | 773 | 26.8 | 2.2% | H4 | 🔴 Сложный |
| `00-intro` | 11388 | 18.5 | 1.32% | H2 | 🔴 Сложный |
| `04-приоритетные-ансамбли` | 1372 | 26.1 | 1.9% | H2 | 🔴 Сложный |
| `10-новые-ансамбли-следующего-шага` | 1001 | 25.7 | 1.1% | H2 | 🔴 Сложный |
| `14-ограничения-лицензии-и-что-пока-` | 3355 | 18.0 | 1.01% | H2 | 🔴 Сложный |
| `memnet` | 7179 | 16.5 | 1.02% | H3 | 🔴 Сложный |
| `ABBREVIATIONS` | 1016 | 145.3 | 1.77% | H2 | 🔴 Сложный |
| `COMPONENT_MATRIX` | 551 | 79.4 | 4.17% | H2 | 🔴 Сложный |
| `CONCEPTS` | 11574 | 340.8 | 0.26% | H2 | 🔴 Сложный |
| `CONTACT_PRIORITY` | 231 | 46.2 | 4.33% | H3 | 🔴 Сложный |
| `ENTITIES` | 495 | 31.9 | 7.27% | H2 | 🔴 Сложный |
| `FOOTNOTES` | 189 | 63.7 | 6.88% | H2 | 🔴 Сложный |
| `GLOSSARY` | 91 | 45.5 | 10.99% | H1 | 🔴 Сложный |
| `GRAPH` | 215 | 27.5 | 13.02% | H2 | 🔴 Сложный |


### 105. Самые простые документы
_Файл: `docs/obsidian/COMPLEXITY.md` | 3 колонок, 15 строк_

| Документ | Слов | Балл |
|----------|------|------|
| `03-portal-protocol-md` | 125 | 🟢 Простой |
| `05-0-status-of-this-document` | 138 | 🟢 Простой |
| `06-1-introduction` | 362 | 🟢 Простой |
| `07-2-terminology` | 301 | 🟢 Простой |
| `08-3-registry-nautilus-json` | 335 | 🟢 Простой |
| `09-4-passport-passport-md` | 166 | 🟢 Простой |
| `105-review-methodology-md` | 105 | 🟢 Простой |
| `106-tl-dr` | 148 | 🟢 Простой |
| `107-1-контекст-и-мотивация` | 349 | 🟢 Простой |
| `108-2-формальный-workflow` | 295 | 🟢 Простой |
| `110-вопрос-fallback-ratio-как-критически` | 222 | 🟢 Простой |
| `112-5-связь-с-существующими-методологиям` | 312 | 🟢 Простой |
| `113-6-почему-это-валидный-паттерн-для-ai` | 151 | 🟢 Простой |
| `114-7-реализация-в-проекте-nautilus` | 304 | 🟢 Простой |
| `115-8-ограничения-и-открытые-вопросы` | 368 | 🟢 Простой |


### 106. Матрица возможностей
_Файл: `docs/obsidian/COMPONENT_MATRIX.md` | 13 колонок, 14 строк_

| Компонент | Лицензия | Статус | Долгосро | Поиск/ин | MCP-совм | Граф зна | Безопасн | Оркестра | Веб-крау | Хранилищ | Документ | CRDT/syn |
|-----------|----------|--------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| **CardIndex** | 🟢 MIT | 🟢 stable | ✅ | ✅ | ✅ | 🟡 | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| **AgentFS** | 🟢 MIT | 🟢 stable | 🟡 | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ | ✅ | ✅ | 🟡 |
| **Yodoca** | 🟢 Apache 2.0 | 🔵 active | ✅ | ✅ | 🟡 | ❌ | 🟡 | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **NGT-memory** | 🟠 BSL 1.1 | 🔵 active | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **SENTINEL** | 🟢 MIT | 🔵 active | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Rufler** | ⚪ — | 🟡 experimental | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | 🟡 | ❌ |
| **knowledge-space** | 🟢 MIT | 🟢 stable | ✅ | ✅ | 🟡 | 🟡 | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **Firecrawl** | 🟢 MIT | 🟢 stable | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| **Wikontic** | ⚪ — | ⚪ unknown | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Memnet** | ⚪ — | 🟡 experimental | ✅ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **agent-memory-mcp** | 🟢 MIT | 🟡 experimental | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **LiteParse** | ⚪ — | ⚪ unknown | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **AI Factory** | ⚪ — | ⚪ unknown | ❌ | ❌ | 🟡 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **agent-pool** | ⚪ — | ⚪ unknown | ❌ | ❌ | 🟡 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |


### 107. Покрытие возможностей
_Файл: `docs/obsidian/COMPONENT_MATRIX.md` | 4 колонок, 10 строк_

| Возможность | Полная поддержка | Частичная | Итого |
|-------------|-----------------|-----------|-------|
| Долгосрочная память | 6 | 1 | 7/14 |
| Поиск/индекс | 8 | 1 | 9/14 |
| MCP-совместим | 6 | 4 | 10/14 |
| Граф знаний | 2 | 2 | 4/14 |
| Безопасность/PII | 1 | 2 | 3/14 |
| Оркестрация | 3 | 0 | 3/14 |
| Веб-краулинг | 2 | 0 | 2/14 |
| Хранилище данных | 8 | 0 | 8/14 |
| Документированный API | 4 | 5 | 9/14 |
| CRDT/sync | 0 | 1 | 1/14 |


### 108. Каталог компонентов
_Файл: `docs/obsidian/COMPONENT_MATRIX.md` | 4 колонок, 14 строк_

| Компонент | Лицензия | Статус | Репозиторий |
|-----------|----------|--------|-------------|
| **CardIndex** | 🟢 MIT | 🟢 stable | `kksudo/CardIndex` |
| **AgentFS** | 🟢 MIT | 🟢 stable | `kksudo/agentfs` |
| **Yodoca** | 🟢 Apache 2.0 | 🔵 active | `spbmolot/yodoca` |
| **NGT-memory** | 🟠 BSL 1.1 | 🔵 active | — |
| **SENTINEL** | 🟢 MIT | 🔵 active | — |
| **Rufler** | ⚪ — | 🟡 experimental | — |
| **knowledge-space** | 🟢 MIT | 🟢 stable | `kksudo/knowledge-space` |
| **Firecrawl** | 🟢 MIT | 🟢 stable | `mendableai/firecrawl` |
| **Wikontic** | ⚪ — | ⚪ unknown | — |
| **Memnet** | ⚪ — | 🟡 experimental | — |
| **agent-memory-mcp** | 🟢 MIT | 🟡 experimental | — |
| **LiteParse** | ⚪ — | ⚪ unknown | — |
| **AI Factory** | ⚪ — | ⚪ unknown | — |
| **agent-pool** | ⚪ — | ⚪ unknown | — |


### 109. Рекомендуемые ансамбли
_Файл: `docs/obsidian/COMPONENT_MATRIX.md` | 3 колонок, 5 строк_

| Ансамбль | Компоненты | Ключевая функция |
|----------|-----------|-----------------|
| Knowledge OS | CardIndex + AgentFS + knowledge-space | Индекс знаний + AI FS |
| Memory Layer | Yodoca + NGT-memory + agent-memory-mcp | Долгосрочная память |
| Security Runtime | SENTINEL + AgentFS | PII-защита + MCP allowlist |
| Web Intelligence | Firecrawl + CardIndex + Yodoca | Краулинг → память |
| Agent Orchestra | Rufler + agent-pool + AI Factory | Оркестрация агентов |


### 110. Топ концептов по связям
_Файл: `docs/obsidian/CONCEPT_GRAPH.md` | 4 колонок, 30 строк_

| Концепт | Файлов | Связей | Категория |
|---------|--------|--------|-----------|
| `docs` | 482 | 4264 | other |
| `anthropic` | 398 | 3642 | other |
| `vacancies` | 375 | 3503 | other |
| `auto` | 292 | 2834 | other |
| `документы` | 251 | 2642 | other |
| `summary` | 230 | 2280 | other |
| `сходство` | 176 | 1935 | other |
| `tags` | 181 | 1862 | other |
| `appendix` | 136 | 1451 | other |
| `nautilus` | 123 | 1328 | other |
| `agent` | 126 | 1323 | agent |
| `architecture` | 112 | 1309 | other |
| `knowledge` | 122 | 1196 | other |
| `ingit` | 101 | 1147 | other |
| `contents` | 108 | 1136 | other |
| `cowork` | 93 | 1109 | other |
| `portal` | 93 | 1046 | other |
| `svyazi` | 119 | 990 | project |
| `collaboration` | 84 | 966 | other |
| `agents` | 85 | 943 | agent |
| `layer` | 72 | 880 | architecture |
| `work` | 75 | 840 | other |
| `protocol` | 73 | 814 | architecture |
| `document` | 62 | 761 | data |
| `abstract` | 62 | 724 | other |
| `readme` | 68 | 709 | other |
| `what` | 69 | 707 | other |
| `open` | 62 | 705 | other |
| `infrastructure` | 59 | 665 | other |
| `claude` | 63 | 653 | other |


### 111. Согласованность терминов
_Файл: `docs/obsidian/CONSISTENCY.md` | 4 колонок, 10 строк_

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 8 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 2 |
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 2 |
| **CardIndex** | `CardIndex` | `card-index` | 2 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 4 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 25 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 1 |
| **self-improvement** | `self-improvement` | `self-improve` | 70 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 3 |


### 112. Ключевые авторы проектов
_Файл: `docs/obsidian/CONTACTS.md` | 5 колонок, 15 строк_

| Автор | Проект | Слой | Упомянут в файлах | Первый вопрос |
|-------|--------|------|-------------------|---------------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 37 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 20 | — |
| **Cutcode** | AIF Handoff | orchestration | 35 | — |
| **Dmitriila** | SENTINEL | security | 33 | — |
| **MiXaiLL76** | Auto AI Router | security | 32 | — |
| **Sonia_Black** | knowledge-space | knowledge | 16 | — |
| **VitalyOborin** | Yodoca | memory | 33 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 32 | — |
| **andrey_chuyan** | Svyazi | ingestion/CardIndex | 17 | Стоит ли расширять CardIndex до person/project/episode/evidence или лучше держать разные индексы? |
| **kksudo** | AgentFS | knowledge/filesystem | 64 | Что лучше класть в .agentos, а что выносить в machine-only state вне vault conventions? |
| **lee-to** | AI Factory | orchestration | 8 | — |
| **nlaik** | LiteParse / research-docs | rag | 20 | — |
| **spbmolot** | NGT Memory | memory | 61 | Где проходит практическая граница между полезной ассоциацией и ложной ко-активацией тем для community discovery? |
| **tagir_analyzes** | Legal RAG | rag | 19 | — |
| **zodigancode** | Rufler | orchestration | 26 | — |


### 113. GitHub репозитории
_Файл: `docs/obsidian/CONTACTS.md` | 2 колонок, 38 строк_

| Репозиторий | Упоминается в файлах |
|-------------|---------------------|
| `github.com/github.com/AnastasiyaW` | 4 |
| `github.com/github.com/AnastasiyaW/knowledge-space` | 7 |
| `github.com/github.com/Antipozitive` | 4 |
| `github.com/github.com/Cutcode` | 4 |
| `github.com/github.com/Dmitriila` | 4 |
| `github.com/github.com/MiXaiLL76` | 4 |
| `github.com/github.com/NicholasSpisak/second-brain` | 2 |
| `github.com/github.com/Sonia` | 4 |
| `github.com/github.com/VitalyOborin` | 4 |
| `github.com/github.com/VladSpace` | 4 |
| `github.com/github.com/andrey` | 4 |
| `github.com/github.com/anthropics/mcp` | 6 |
| `github.com/github.com/artur-gavronchuk/tg-chat-analyser` | 2 |
| `github.com/github.com/camel-ai/camel` | 5 |
| `github.com/github.com/dementev-dev/adversarial-review` | 2 |
| `github.com/github.com/github` | 2 |
| `github.com/github.com/kksudo` | 4 |
| `github.com/github.com/mcp` | 8 |
| `github.com/github.com/nlaik` | 3 |
| `github.com/github.com/settings/tokens` | 5 |
| `github.com/github.com/spbmolot` | 3 |
| `github.com/github.com/svend4` | 5 |
| `github.com/github.com/svend4/data70` | 6 |
| `github.com/github.com/svend4/info1` | 12 |
| `github.com/github.com/svend4/info40` | 4 |
| `github.com/github.com/svend4/info7` | 4 |
| `github.com/github.com/svend4/ingit` | 14 |
| `github.com/github.com/svend4/meta` | 11 |
| `github.com/github.com/svend4/n` | 2 |
| `github.com/github.com/svend4/nautilus` | 42 |
| `github.com/github.com/svend4/nautilus.` | 2 |
| `github.com/github.com/svend4/nautilus.git` | 3 |
| `github.com/github.com/svend4/pro2` | 11 |
| `github.com/github.com/tagir` | 3 |
| `github.com/github.com/users/svend4` | 5 |
| `github.com/github.com/vuguzum/self-aware-mcp-server` | 2 |
| `github.com/github.com/yjs/yjs` | 2 |
| `github.com/github.com/zodigancode` | 3 |


### 114. Топ авторов по приоритету
_Файл: `docs/obsidian/CONTACT_PRIORITY.md` | 7 колонок, 15 строк_

| # | Автор | Проект | Слой | Упоминаний | Статус | Балл |
|---|-------|--------|------|-----------|--------|------|
| 1 | **kksudo** | AgentFS | knowledge/filesystem | 64 | 👁 Изучили | 203 |
| 2 | **spbmolot** | NGT Memory | memory | 61 | 👁 Изучили | 194 |
| 3 | **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 37 | ⬜ Не начато | 117 |
| 4 | **Cutcode** | AIF Handoff | orchestration | 35 | ⬜ Не начато | 109 |
| 5 | **VitalyOborin** | Yodoca | memory | 33 | ⬜ Не начато | 105 |
| 6 | **Dmitriila** | SENTINEL | security | 33 | ⬜ Не начато | 101 |
| 7 | **VladSpace** | Graph RAG | rag | 32 | ⬜ Не начато | 100 |
| 8 | **MiXaiLL76** | Auto AI Router | security | 32 | ⬜ Не начато | 98 |
| 9 | **zodigancode** | Rufler | orchestration | 26 | ⬜ Не начато | 82 |
| 10 | **Antipozitive** | MemNet | memory | 20 | ⬜ Не начато | 66 |
| 11 | **nlaik** | LiteParse / research-docs | rag | 20 | ⬜ Не начато | 64 |
| 12 | **tagir_analyzes** | Legal RAG | rag | 19 | ⬜ Не начато | 61 |
| 13 | **Sonia_Black** | knowledge-space | knowledge | 16 | ⬜ Не начато | 54 |
| 14 | **andrey_chuyan** | Svyazi | ingestion/CardIndex | 17 | ⬜ Не начато | 53 |
| 15 | **lee-to** | AI Factory | orchestration | 8 | ⬜ Не начато | 28 |


### 115. Итого
_Файл: `docs/obsidian/COST.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Человеко-недель | **25** |
| Человеко-часов | **1,000** |
| Бюджет (USD) | **$86,400** |
| Календарный срок | **~6-8 месяцев** |
| Команда | **5 ролей** |


### 116. По компонентам
_Файл: `docs/obsidian/COST.md` | 4 колонок, 13 строк_

| Компонент | Роль | Недель | Стоимость USD |
|-----------|------|--------|--------------|
| Project management | Project Manager | 4 | $10,400 |
| Knowledge OS ядро | Senior Python Dev | 3 | $10,200 |
| Yodoca memory layer | AI/ML Engineer | 3 | $13,200 |
| CardIndex интеграция | Senior Python Dev | 2 | $6,800 |
| NGT граф памяти | AI/ML Engineer | 2 | $8,800 |
| SENTINEL безопасность | Senior Python Dev | 2 | $6,800 |
| Rufler оркестрация | AI/ML Engineer | 2 | $8,800 |
| MCP протокол адаптер | Senior Python Dev | 2 | $6,800 |
| CI/CD и тесты | DevOps | 2 | $6,000 |
| AgentFS подключение | Senior Python Dev | 1 | $3,400 |
| MCP Tool Search | Senior Python Dev | 1 | $3,400 |
| Документация API | Tech Writer | 1 | $1,800 |
| **ИТОГО** | | **25** | **$86,400** |


### 117. По ролям
_Файл: `docs/obsidian/COST.md` | 4 колонок, 5 строк_

| Роль | Ставка USD/ч | Недель | Итого USD |
|------|-------------|--------|----------|
| Senior Python Dev | $85 | 11 | $37,400 |
| AI/ML Engineer | $110 | 7 | $30,800 |
| DevOps | $75 | 2 | $6,000 |
| Tech Writer | $45 | 1 | $1,800 |
| Project Manager | $65 | 4 | $10,400 |


### 118. Сценарии
_Файл: `docs/obsidian/COST.md` | 4 колонок, 3 строк_

| Сценарий | Команда | Срок | Бюджет |
|----------|---------|------|--------|
| Минимальный (solo) | 1 разработчик | ~18 мес | $28,800 |
| Оптимальный | 3 человека | ~8 мес | $43,200 |
| Ускоренный | 5 человек | ~5 мес | $86,400 |


### 119. Временные оценки из документов
_Файл: `docs/obsidian/COST.md` | 3 колонок, 14 строк_

| Источник | Контекст | Недель |
|----------|----------|--------|
| `365-развёрнутый-анал` | Макс) и part-time, реальный timeline 12-24 месяца для full a… | 96 |
| `343-lorenzo-catalyst` | рудоёмкий процесс подачи - Может быть 6-18 месяцев до финанс… | 72 |
| `365-развёрнутый-анал` | eam. С solo developer (Макс) и part-time, реальный timeline … | 72 |
| `ACTION_ITEMS` | обратная-связь_ - 5: Burnout. Проект 12-18 месяцев для singl… | 72 |
| `CONCEPTS` | инимально жизнеспособный прототип за 12-18 месяцев     _→ [N… | 72 |
| `DECISIONS` | document — структурированный план на 12-18 месяцев, который … | 72 |
| `TABLES` | 65-развёрнутый-анал` | Макс) и part-time, реальный timeline … | 72 |
| `332-6-уточнённый-объ` | Оригинальная дорожная карта InGit (10-16 месяцев до v1.0) от… | 64 |
| `332-6-уточнённый-объ` | окращённый Объём  Оригинальный план: 10-16 месяцев до v1.0 с… | 64 |
| `00-intro` | ом смысле. Это архив 1105 разговоров за 15 месяцев (dec 2024… | 60 |
| `00-intro` | — это ChatGPT-корпус 1105 разговоров за 15 месяцев + аналити… | 60 |
| `01-интегральный-анал` | на личном примере, пропустив через себя 15 месяцев диалогов … | 60 |
| `133-обратная-связь` | ы и интерес. Временной план: это не спринт, это marathon на … | 60 |
| `133-обратная-связь` | бственные кейсы, не other people's. Риск 5: Burnout. Проект … | 60 |


### 120. Сводка по секциям
_Файл: `docs/obsidian/COVERAGE.md` | 8 колонок, 5 строк_

| Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks |
|--------|--------|---------|------|-----|-----------|--------|-----------|
| `01-svyazi` | 14 | 🟢 13/14 | 🟢 13/14 | 🟢 12/14 | 🟢 13/14 | 🔴 0/14 | 🟢 13/14 |
| `02-anthropic-vacancies` | 355 | 🟢 354/355 | 🟢 354/355 | 🟡 189/355 | 🟢 354/355 | 🔴 0/355 | 🟢 354/355 |
| `03-technology-combinations` | 5 | 🟢 5/5 | 🟢 5/5 | 🔴 1/5 | 🟢 5/5 | 🔴 0/5 | 🟢 5/5 |
| `04-ai-collaborations` | 15 | 🟢 15/15 | 🟢 15/15 | 🟢 13/15 | 🟢 15/15 | 🟢 15/15 | 🟢 15/15 |
| `05-habr-projects` | 6 | 🟢 6/6 | 🟢 6/6 | 🔴 1/6 | 🟢 6/6 | 🟢 6/6 | 🟢 6/6 |


### 121. Файлы с низким покрытием (< 3 признаков) — 2 файлов
_Файл: `docs/obsidian/COVERAGE.md` | 8 колонок, 2 строк_

| Файл | Слов | Summary | Теги | TOC | CrossRefs | ## Статус | Backlinks |
|------|------| ---|---|---|---|---|--- |
| `docs/01-svyazi/00-intro-part2.md` | 5 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |


### 122. Содержание
_Файл: `docs/obsidian/DENSITY.md` | 8 колонок, 20 строк_

| Тема | 01-svyazi | 02-vacancies | 03-tech | 04-collab | 05-habr | root | Итого |
|------|-----------|--------------|---------|-----------|---------|------|-------|
| **Svyazi** | 214 | 73 | 16 | 339 | 45 | 1662 | **2349** |
| **CardIndex** | 53 | 54 | 12 | 100 | 12 | 326 | **557** |
| **AgentFS** | 51 | 93 | 4 | 101 | 28 | 334 | **611** |
| **Yodoca** | 86 | 36 | 18 | 134 | 110 | 460 | **844** |
| **NGT-memory** | 162 | 230 | 3 | 261 | 129 | 803 | **1588** |
| **SENTINEL** | 47 | 8 | 0 | 59 | 0 | 169 | **283** |
| **Rufler** | 35 | 19 | 0 | 43 | 0 | 154 | **251** |
| **AI Factory** | 63 | 45 | 0 | 84 | 0 | 303 | **495** |
| **Knowledge OS** | 0 | 18 | 0 | 4 | 0 | 23 | **45** |
| **Forensic RAG** | 34 | 19 | 1 | 52 | 2 | 100 | **208** |
| **MCP** | 60 | 743 | 4 | 149 | 56 | 394 | **1406** |
| **MVP** | 100 | 90 | 0 | 131 | 7 | 463 | **791** |
| **Архитектура** | 99 | 533 | 9 | 167 | 38 | 572 | **1418** |
| **Безопасность** | 72 | 132 | 1 | 80 | 1 | 397 | **683** |
| **Лицензия** | 106 | 636 | 0 | 131 | 13 | 515 | **1401** |
| **Roadmap** | 33 | 143 | 0 | 33 | 3 | 206 | **418** |
| **Вакансии** | 2 | 5832 | 2 | 13 | 7 | 7209 | **13065** |
| **Комбинации** | 7 | 140 | 67 | 17 | 10 | 284 | **525** |
| **Habr** | 34 | 78 | 20 | 187 | 134 | 553 | **1006** |
| **Контакты** | 18 | 128 | 0 | 21 | 6 | 310 | **483** |


### 123. Наиболее раскрытые темы
_Файл: `docs/obsidian/DENSITY.md` | 3 колонок, 10 строк_

| Тема | Упоминаний | Визуализация |
|------|------------|-------------|
| **Вакансии** | 13065 | `███████████████` |
| **Svyazi** | 2349 | `██░░░░░░░░░░░░░` |
| **NGT-memory** | 1588 | `█░░░░░░░░░░░░░░` |
| **Архитектура** | 1418 | `█░░░░░░░░░░░░░░` |
| **MCP** | 1406 | `█░░░░░░░░░░░░░░` |
| **Лицензия** | 1401 | `█░░░░░░░░░░░░░░` |
| **Habr** | 1006 | `█░░░░░░░░░░░░░░` |
| **Yodoca** | 844 | `░░░░░░░░░░░░░░░` |
| **MVP** | 791 | `░░░░░░░░░░░░░░░` |
| **Безопасность** | 683 | `░░░░░░░░░░░░░░░` |


### 124. Где сосредоточена каждая тема
_Файл: `docs/obsidian/DENSITY.md` | 3 колонок, 20 строк_

| Тема | Основной раздел | % |
|------|-----------------|---|
| Svyazi | `root` | 70% |
| CardIndex | `root` | 58% |
| AgentFS | `root` | 54% |
| Yodoca | `root` | 54% |
| NGT-memory | `root` | 50% |
| SENTINEL | `root` | 59% |
| Rufler | `root` | 61% |
| AI Factory | `root` | 61% |
| Knowledge OS | `root` | 51% |
| Forensic RAG | `root` | 48% |
| MCP | `02-anthropic-vacancies` | 52% |
| MVP | `root` | 58% |
| Архитектура | `root` | 40% |
| Безопасность | `root` | 58% |
| Лицензия | `02-anthropic-vacancies` | 45% |
| Roadmap | `root` | 49% |
| Вакансии | `root` | 55% |
| Комбинации | `root` | 54% |
| Habr | `root` | 54% |
| Контакты | `root` | 64% |


### 125. Python-зависимости
_Файл: `docs/obsidian/DEPENDABOT.md` | 5 колонок, 4 строк_

| Пакет | Мин. версия | Последняя (PyPI) | Статус | Используется в |
|-------|------------|-----------------|--------|----------------|
| `anthropic` | `0.25.0` | `—` | — | `scripts/improve_llm_*.py` |
| `mcp` | `1.0.0` | `—` | — | `scripts/mcp_server.py` |
| `pre-commit` | `3.0.0` | `—` | — | `.pre-commit-config.yaml` |
| `pyspellchecker` | `0.8.0` | `—` | — | `scripts/improve_spellcheck.py` |


### 126. OSS-проекты (Svyazi 2.0)
_Файл: `docs/obsidian/DEPENDABOT.md` | 3 колонок, 4 строк_

| Проект | Репозиторий | Статус |
|--------|------------|--------|
| AgentFS | [https://github.com/kksudo/agentfs](https://github.com/kksudo/agentfs) | — |
| NGT Memory | [https://github.com/spbmolot/ngt-memory](https://github.com/spbmolot/ngt-memory) | — |
| Yodoca | [https://github.com/VitalyOborin/yodoca](https://github.com/VitalyOborin/yodoca) | — |
| knowledge-space | [https://github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space) | — |


### 127. Зависимости
_Файл: `docs/obsidian/DEPENDENCY_MAP.md` | 3 колонок, 49 строк_

| Скрипт | Производит | Зависит от |
|--------|-----------|-----------|
| `improve_abbreviations.py` | `docs/ABBREVIATIONS.md` | `docs/**/*.md` |
| `improve_action_items.py` | `docs/ACTION_ITEMS.md` | `docs/**/*.md` |
| `improve_autofill.py` | `docs/autofilled/**` | `docs/templates/**`, `docs/ENTITIES.md` |
| `improve_backlinks.py` | `docs/BACKLINKS.md` | `docs/**/*.md` |
| `improve_badges.py` | `docs/badges/*.svg` | `docs/HEALTH.md`, `docs/SCORING.md` |
| `improve_clusters.py` | `docs/CLUSTERS.md` | `docs/**/*.md` |
| `improve_concepts.py` | `docs/CONCEPTS.md` | `docs/**/*.md` |
| `improve_cost.py` | `docs/COST.md` | `docs/**/*.md` |
| `improve_decisions.py` | `docs/DECISIONS.md` | `docs/**/*.md` |
| `improve_dependency_map.py` | `docs/DEPENDENCY_MAP.md` | `scripts/improve_*.py` |
| `improve_digest.py` | `docs/DIGEST.md` | — |
| `improve_digest_weekly.py` | `docs/DIGEST_WEEKLY.md` | — |
| `improve_entities.py` | `docs/ENTITIES.md` | `docs/**/*.md` |
| `improve_export_csv.py` | `docs/export_full.csv` | `docs/**/*.md` |
| `improve_export_html.py` | `docs/export_full.html` | `docs/**/*.md` |
| `improve_export_json.py` | `docs/export_full.json` | `docs/**/*.md` |
| `improve_faq.py` | `docs/FAQ.md` | `docs/**/*.md` |
| `improve_footnotes.py` | `docs/FOOTNOTES.md`, `docs/**/*.md (сноски)` | `docs/**/*.md` |
| `improve_glossary.py` | `docs/GLOSSARY.md` | `docs/**/*.md` |
| `improve_health.py` | `docs/HEALTH.md` | `docs/METRICS.md`, `docs/VALIDATION.md` |
| `improve_heatmap.py` | `docs/HEATMAP.md` | `docs/TAGS.md` |
| `improve_index_update.py` | `docs/search_index.json` | `docs/search_index.json` |
| `improve_kpi.py` | `docs/KPI.md` | `docs/**/*.md` |
| `improve_llm_enrich.py` | `docs/**/*.md (enriched)` | `docs/ENTITIES.md`, `ANTHROPIC_API_KEY` |
| `improve_llm_gaps.py` | `docs/LLM_GAPS.md` | `docs/**/*.md`, `ANTHROPIC_API_KEY` |
| `improve_llm_qa.py` | `docs/LLM_QA.md` | `docs/QUESTIONS.md`, `ANTHROPIC_API_KEY` |
| `improve_llm_summary.py` | `docs/LLM_SUMMARIES.md` | `docs/*/README.md` |
| `improve_metrics.py` | `docs/METRICS.md` | `docs/**/*.md` |
| `improve_network.py` | `docs/NETWORK.md`, `docs/network.dot` | `docs/ENTITIES.md` |
| `improve_onboarding.py` | `docs/ONBOARDING.md` | `docs/SCORING.md`, `docs/CONTACTS.md` |
| `improve_orphans.py` | `docs/ORPHANS.md` | `docs/BACKLINKS.md` |
| `improve_progress.py` | `docs/PROGRESS.md` | `docs/SCORING.md` |
| `improve_questions.py` | `docs/QUESTIONS.md` | `docs/**/*.md` |
| `improve_readmes.py` | `docs/*/README.md` | — |
| `improve_report.py` | `docs/REPORT.md` | `docs/STATS.md`, `docs/HEALTH.md` |
| `improve_schedule.py` | `docs/SCHEDULE.md` | — |
| `improve_scoring.py` | `docs/SCORING.md` | `docs/HEALTH.md`, `docs/METRICS.md` |
| `improve_search_index.py` | `docs/search_index.json` | `docs/**/*.md` |
| `improve_sentiment.py` | `docs/SENTIMENT.md` | `docs/**/*.md` |
| `improve_similar.py` | `docs/SIMILAR.md` | `docs/**/*.md` |
| `improve_sitemap.py` | `docs/SITEMAP.md`, `docs/sitemap.xml` | `docs/**/*.md` |
| `improve_stats.py` | `docs/STATS.md` | `docs/**/*.md` |
| `improve_summaries.py` | `docs/*/README.md` | `docs/**/*.md` |
| `improve_tags.py` | `docs/TAGS.md` | `docs/**/*.md` |
| `improve_tech_radar.py` | `docs/TECH_RADAR.md` | — |
| `improve_toc.py` | `docs/**/*.md (TOC блоки)` | `docs/**/*.md` |
| `improve_validate.py` | `docs/VALIDATION.md` | `docs/**/*.md` |
| `improve_word_cloud.py` | `docs/WORD_CLOUD.svg`, `docs/WORD_CLOUD.md` | `docs/WORD_FREQ.md` |
| `improve_word_freq.py` | `docs/WORD_FREQ.md` | `docs/**/*.md` |


### 128. История коммитов (последние 15)
_Файл: `docs/obsidian/DIGEST.md` | 3 колонок, 15 строк_

| Дата | Hash | Описание |
|------|------|---------|
| 2026-04-29 | `b326b33a` | Merge remote-tracking branch 'origin/main' into claude/organize-monore |
| 2026-04-29 | `69562b02` | feat: add component matrix, KPI history tracker, fix run_all coverage |
| 2026-04-29 | `42f561dd` | fix: fix update-docs CI job failures |
| 2026-04-29 | `854cff7c` | Merge pull request #5 from svend4/claude/current-dev-stage-iVIov |
| 2026-04-29 | `59617c5d` | feat: add risk register, auto-changelog, master index; fix run_all mis |
| 2026-04-29 | `89d3e8fb` | chore: sync CONTRADICTIONS.md (background task output) |
| 2026-04-29 | `4ddee95e` | feat: add tech radar, onboarding guide, dependency map, meta group in  |
| 2026-04-29 | `6b81ffed` | chore: sync CONTRADICTIONS.md after contradiction_check fix |
| 2026-04-29 | `4755dd94` | fix: исправить ошибки в deeptext скриптах, добавить выходные файлы |
| 2026-04-29 | `1f3fe74a` | feat: add autonomous watcher (Ступень 6), CI workflow, LLM section sum |
| 2026-04-29 | `469dbced` | feat: add CLAUDE.md, weekly digest script, enrich group in run_all |
| 2026-04-29 | `4e52a185` | chore: update mcp.json description wording |
| 2026-04-29 | `00a25f78` | feat: add LLM integration (Ступень 3), skills (Ступень 4), MCP server  |
| 2026-04-29 | `d9e66da8` | Merge pull request #3 from svend4/claude/current-dev-stage-iVIov |
| 2026-04-29 | `1d552d4e` | chore: sync PROGRESS.md after deeptext scripts commit |


### 129. Текущее состояние репозитория
_Файл: `docs/obsidian/DIGEST.md` | 2 колонок, 3 строк_

| Параметр | Значение |
|----------|---------|
| Документов `.md` | **524** |
| Скриптов обработки | **125** |
| Последнее обновление | **2026-04-29** |


### 130. Итого
_Файл: `docs/obsidian/DIGEST_WEEKLY.md` | 2 колонок, 5 строк_

| Метрика | Значение |
|---------|---------|
| Коммитов за неделю | **50** |
| Новых файлов | **0** |
| Изменённых файлов | **0** |
| Всего MD файлов | **529** |
| Всего слов | **523,662** |


### 131. Точные дубли (одинаковое содержимое)
_Файл: `docs/obsidian/DUPLICATES.md` | 2 колонок, 1 строк_

| Группа | Файлы |
|--------|-------|
| #1 | `docs/templates/research-note.md`, `docs/autofilled/research-summary.md` |


### 132. Люди и авторы (7)
_Файл: `docs/obsidian/ENTITIES.md` | 3 колонок, 7 строк_

| Имя | Упоминаний | Файлов |
|---------|------------|--------|
| **svend4** | 987 | 124 |
| **Lorenzo** | 760 | 80 |
| **kksudo** | 153 | 64 |
| **spbmolot** | 140 | 62 |
| **Андрей** | 69 | 23 |
| **Виталий** | 29 | 14 |
| **Антропик** | 16 | 14 |


### 133. Проекты (22)
_Файл: `docs/obsidian/ENTITIES.md` | 3 колонок, 22 строк_

| Проект | Упоминаний | Файлов |
|---------|------------|--------|
| **Svyazi** | 2029 | 137 |
| **Nautilus** | 1891 | 212 |
| **Cowork** | 1487 | 127 |
| **ingit** | 1478 | 121 |
| **SGB** | 783 | 109 |
| **Lorenzo** | 760 | 80 |
| **CardIndex** | 464 | 70 |
| **AgentFS** | 460 | 73 |
| **NGT** | 449 | 95 |
| **Yodoca** | 417 | 80 |
| **knowledge-space** | 338 | 58 |
| **mclaude** | 262 | 48 |
| **Rufler** | 247 | 58 |
| **LiteParse** | 228 | 54 |
| **SENTINEL** | 221 | 61 |
| **AI Factory** | 213 | 48 |
| **MemNet** | 157 | 40 |
| **Wikontic** | 140 | 30 |
| **Firecrawl** | 84 | 12 |
| **agent-memory-mcp** | 37 | 17 |
| **Shield** | 8 | 5 |
| **MCP Tool Search** | 7 | 4 |


### 134. Организации (9)
_Файл: `docs/obsidian/ENTITIES.md` | 3 колонок, 9 строк_

| Организация | Упоминаний | Файлов |
|---------|------------|--------|
| **Anthropic** | 12613 | 430 |
| **Claude** | 1217 | 181 |
| **GitHub** | 1068 | 139 |
| **Habr** | 772 | 85 |
| **Хабр** | 230 | 42 |
| **Obsidian** | 146 | 42 |
| **Google** | 51 | 17 |
| **OpenAI** | 50 | 24 |
| **ChatGPT** | 41 | 25 |


### 135. Технологии и стандарты (24)
_Файл: `docs/obsidian/ENTITIES.md` | 3 колонок, 24 строк_

| Технология | Упоминаний | Файлов |
|---------|------------|--------|
| **MCP** | 1350 | 159 |
| **RAG** | 1253 | 182 |
| **MIT** | 969 | 185 |
| **LLM** | 573 | 105 |
| **JSON** | 417 | 89 |
| **Python** | 269 | 72 |
| **REST** | 206 | 77 |
| **YAML** | 149 | 55 |
| **BSL** | 83 | 41 |
| **CRDT** | 77 | 21 |
| **Apache** | 73 | 40 |
| **Rust** | 71 | 38 |
| **SQLite** | 47 | 15 |
| **Mermaid** | 45 | 13 |
| **TypeScript** | 18 | 12 |
| **LangChain** | 18 | 12 |
| **TF-IDF** | 13 | 10 |
| **FAISS** | 12 | 9 |
| **PostgreSQL** | 12 | 8 |
| **WebSocket** | 10 | 9 |
| **FastAPI** | 8 | 6 |
| **OAuth** | 3 | 2 |
| **JWT** | 3 | 3 |
| **GraphQL** | 2 | 2 |


### 136. GitHub репозитории (12)
_Файл: `docs/obsidian/ENTITIES.md` | 2 колонок, 12 строк_

| Репозиторий | Упоминаний |
|-------------|------------|
| [https://github.com/svend4/nautilus](https://github.com/svend4/nautilus) | 29 |
| [https://github.com/svend4/ingit](https://github.com/svend4/ingit) | 13 |
| [https://github.com/svend4/pro2](https://github.com/svend4/pro2) | 8 |
| [https://github.com/svend4/info1](https://github.com/svend4/info1) | 8 |
| [https://github.com/svend4/meta](https://github.com/svend4/meta) | 6 |
| [https://github.com/svend4/data70](https://github.com/svend4/data70) | 5 |
| [https://github.com/settings/tokens](https://github.com/settings/tokens) | 5 |
| [https://github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space) | 5 |
| [https://github.com/anthropics/mcp](https://github.com/anthropics/mcp) | 5 |
| [https://github.com/camel-ai/camel](https://github.com/camel-ai/camel) | 4 |
| [https://github.com/svend4/info7](https://github.com/svend4/info7) | 3 |
| [https://github.com/svend4/info40](https://github.com/svend4/info40) | 3 |


### 137. Ко-встречаемость проектов (топ пары)
_Файл: `docs/obsidian/ENTITIES.md` | 2 колонок, 20 строк_

| Пара | Общих файлов |
|------|-------------|
| Cowork ↔ ingit | 108 |
| Nautilus ↔ Cowork | 89 |
| Nautilus ↔ ingit | 80 |
| Svyazi ↔ NGT | 79 |
| NGT ↔ Yodoca | 76 |
| Nautilus ↔ SGB | 73 |
| Svyazi ↔ Yodoca | 72 |
| Svyazi ↔ AgentFS | 68 |
| AgentFS ↔ NGT | 66 |
| AgentFS ↔ Yodoca | 62 |
| Svyazi ↔ CardIndex | 58 |
| CardIndex ↔ NGT | 57 |
| Svyazi ↔ Rufler | 56 |
| Svyazi ↔ SENTINEL | 56 |
| Svyazi ↔ Lorenzo | 54 |
| Cowork ↔ SGB | 54 |
| ingit ↔ SGB | 54 |
| CardIndex ↔ AgentFS | 54 |
| AgentFS ↔ SENTINEL | 54 |
| AgentFS ↔ Rufler | 52 |


### 138. Словарь сносок
_Файл: `docs/obsidian/FOOTNOTES.md` | 3 колонок, 17 строк_

| Термин | Определение | Файлов |
|--------|-------------|--------|
| **AgentFS** | OSS-проект: файловая система для AI-агентов (MIT) | 3 |
| **BSL** | Business Source License — коммерческая лицензия с открытым кодом | 0 |
| **CRDT** | Conflict-free Replicated Data Type — бесконфликтные данные | 0 |
| **CardIndex** | OSS-проект: индекс знаний на карточках (MIT) | 3 |
| **Firecrawl** | Инструмент: веб-краулер для AI (MIT) | 0 |
| **Jaccard** | Коэффициент схожести множеств (0–1) | 0 |
| **LLM** | Large Language Model — большая языковая модель | 0 |
| **MCP** | Model Context Protocol — протокол для AI-инструментов | 0 |
| **NGT** | OSS-проект: ассоциативный граф памяти (BSL 1.1) | 0 |
| **PII** | Personally Identifiable Information — персональные данные | 0 |
| **RAG** | Retrieval-Augmented Generation — генерация с поиском | 2 |
| **Rufler** | OSS-проект: оркестратор AI-агентов | 0 |
| **SENTINEL** | OSS-проект: безопасность и allowlist для MCP | 0 |
| **Svyazi** | Главный проект: экосистема AI-компонентов | 0 |
| **TF-IDF** | Term Frequency–Inverse Document Frequency — метрика важности термина | 0 |
| **Yodoca** | OSS-проект: система памяти с консолидацией (Apache 2.0) | 0 |
| **knowledge-space** | OSS-проект: база знаний 785+ карточек (MIT) | 0 |


### 139. Топ совместных упоминаний
_Файл: `docs/obsidian/GRAPH.md` | 3 колонок, 25 строк_

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **Yodoca** | 74 |
| **Svyazi** | **AgentFS** | 70 |
| **AgentFS** | **Yodoca** | 64 |
| **Svyazi** | **CardIndex** | 60 |
| **Svyazi** | **SENTINEL** | 58 |
| **Svyazi** | **Rufler** | 58 |
| **CardIndex** | **AgentFS** | 56 |
| **AgentFS** | **SENTINEL** | 56 |
| **Svyazi** | **NGT Memory** | 55 |
| **AgentFS** | **Rufler** | 54 |
| **Svyazi** | **knowledge-space** | 53 |
| **Svyazi** | **LiteParse** | 53 |
| **Svyazi** | **Auto AI Router** | 53 |
| **CardIndex** | **Yodoca** | 52 |
| **Rufler** | **Yodoca** | 52 |
| **SENTINEL** | **Auto AI Router** | 51 |
| **Yodoca** | **SENTINEL** | 50 |
| **Rufler** | **SENTINEL** | 50 |
| **Yodoca** | **NGT Memory** | 50 |
| **Svyazi** | **mclaude** | 49 |
| **Svyazi** | **AI Factory** | 49 |
| **AgentFS** | **knowledge-space** | 48 |
| **AgentFS** | **NGT Memory** | 48 |
| **CardIndex** | **knowledge-space** | 46 |
| **AgentFS** | **LiteParse** | 46 |


### 140. Метрики
_Файл: `docs/obsidian/HEALTH.md` | 4 колонок, 5 строк_

| Метрика | Значение | Статус | Балл |
|---------|----------|--------|------|
| Покрытие текста | 97.6% | 🟢 | 98 |
| Полнота тем | 26✅ 2⚠️ 2❌ | 🟡 | 87 |
| Согласованность | 0 проблем | 🟢 | 100 |
| Внутренние ссылки | 170 сломано | 🟠 | 66 |
| Дублирование | 0 точных дублей | 🟢 | 100 |


### 141. Структура репозитория
_Файл: `docs/obsidian/HEALTH.md` | 2 колонок, 10 строк_

| Раздел | Файлов |
|--------|--------|
| 01-svyazi | 16 |
| 02-anthropic-vacancies | 357 |
| 03-technology-combinations | 7 |
| 04-ai-collaborations | 17 |
| 05-habr-projects | 10 |
| autofilled | 13 |
| badges | 1 |
| contacts | 15 |
| root | 87 |
| templates | 6 |


### 142. Числовые значения (‰)
_Файл: `docs/obsidian/HEATMAP.md` | 6 колонок, 12 строк_

| Тема | svyazi | anthropic- | technology | ai-collabo | habr-proje |
|------|------------|------------|------------|------------|------------|
| **Память/Knowledge** | 24.2 | 3.2 | 15.7 | 16.5 | 21.3 |
| **Агент/Оркестр** | 22.6 | 13.3 | 25.3 | 19.3 | 8.7 |
| **Безопасность** | 7.7 | 0.4 | 0.4 | 4.1 | 0.1 |
| **Архитектура** | 6.3 | 6.0 | 4.2 | 3.7 | 1.1 |
| **MVP/Roadmap** | 8.4 | 0.8 | 0.0 | 3.9 | 1.1 |
| **Граф/RAG** | 9.7 | 1.8 | 21.5 | 7.8 | 3.8 |
| **Лицензия/OSS** | 8.2 | 2.3 | 0.0 | 4.2 | 1.0 |
| **Вакансии** | 0.2 | 21.2 | 0.8 | 0.5 | 0.8 |
| **Комбинации** | 4.8 | 0.7 | 25.7 | 2.9 | 2.1 |
| **Habr/Проекты** | 7.8 | 0.4 | 9.2 | 10.3 | 19.3 |
| **Контакты/Команда** | 6.8 | 1.0 | 0.0 | 4.0 | 2.3 |
| **Интеграция/API** | 8.1 | 7.5 | 2.7 | 7.6 | 6.9 |


### 143. Концентрация тем
_Файл: `docs/obsidian/HEATMAP.md` | 3 колонок, 12 строк_

| Тема | Лучший раздел | Плотность |
|------|--------------|-----------|
| **Память/Knowledge** | `01-svyazi` | 24.2‰ |
| **Агент/Оркестр** | `03-technology-combinations` | 25.3‰ |
| **Безопасность** | `01-svyazi` | 7.7‰ |
| **Архитектура** | `01-svyazi` | 6.3‰ |
| **MVP/Roadmap** | `01-svyazi` | 8.4‰ |
| **Граф/RAG** | `03-technology-combinations` | 21.5‰ |
| **Лицензия/OSS** | `01-svyazi` | 8.2‰ |
| **Вакансии** | `02-anthropic-vacancies` | 21.2‰ |
| **Комбинации** | `03-technology-combinations` | 25.7‰ |
| **Habr/Проекты** | `05-habr-projects` | 19.3‰ |
| **Контакты/Команда** | `01-svyazi` | 6.8‰ |
| **Интеграция/API** | `01-svyazi` | 8.1‰ |


### 144. Метрики репозитория
_Файл: `docs/obsidian/INDEX.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Markdown документов | **529** |
| Слов | **523,847** |
| Скриптов автоматизации | **125** |
| Go/No-Go скоринг | **93 🟢** |
| Здоровье репо | **90/100** |


### 145. Аналитика и отчёты
_Файл: `docs/obsidian/INDEX.md` | 2 колонок, 26 строк_

| Документ | Описание |
|----------|---------|
| [[STATS|`STATS.md`]] | Статистика |
| [[METRICS|`METRICS.md`]] | Качество (65.7/100) |
| [[VALIDATION|`VALIDATION.md`]] | Валидация |
| [[SENTIMENT|`SENTIMENT.md`]] | Тональность |
| [[CLUSTERS|`CLUSTERS.md`]] | Кластеры тем |
| [[SIMILAR|`SIMILAR.md`]] | Похожие документы |
| [[HEATMAP|`HEATMAP.md`]] | Тепловая карта тем |
| [[QUESTIONS|`QUESTIONS.md`]] | Открытые вопросы (484) |
| [[KPI|`KPI.md`]] | KPI (737 показателей) |
| [[ACTION_ITEMS|`ACTION_ITEMS.md`]] | Задачи |
| [[DECISIONS|`DECISIONS.md`]] | Архитектурные решения |
| [[PRIORITIES|`PRIORITIES.md`]] | Приоритеты |
| [[PROGRESS|`PROGRESS.md`]] | Прогресс MVP |
| [[DIGEST_WEEKLY|`DIGEST_WEEKLY.md`]] | Дайджест недели |
| [[SITEMAP|`SITEMAP.md`]] | Карта сайта |
| [[WORD_CLOUD|`WORD_CLOUD.md`]] | Облако слов |
| [[BACKLINKS|`BACKLINKS.md`]] | Обратные ссылки |
| [[NARRATIVE|`NARRATIVE.md`]] | Нарратив проекта |
| [[ORPHANS|`ORPHANS.md`]] | Несвязанные файлы |
| [[ALERTS|`ALERTS.md`]] | Callout-блоки |
| [[FOOTNOTES|`FOOTNOTES.md`]] | Сноски терминов |
| [[ABBREVIATIONS|`ABBREVIATIONS.md`]] | Аббревиатуры |
| [[GLOSSARY|`GLOSSARY.md`]] | Глоссарий |
| [[CONCEPTS|`CONCEPTS.md`]] | Концепции |
| [[ENTITIES|`ENTITIES.md`]] | Сущности |
| [[TAGS|`TAGS.md`]] | Теги |


### 146. Ключевые документы
_Файл: `docs/obsidian/INDEX.md` | 3 колонок, 12 строк_

| Документ | Тема | Описание |
|----------|------|---------|
| [[SCORING|`SCORING.md`]] | 🎯 Go/No-Go скоринг | Статус готовности: 96% |
| [[HEALTH|`HEALTH.md`]] | ❤️  Здоровье репо | Метрики качества документации |
| [[TECH_RADAR|`TECH_RADAR.md`]] | 📡 Tech Radar | ADOPT/TRIAL/ASSESS/HOLD |
| [[RISK_REGISTER|`RISK_REGISTER.md`]] | ⚠️  Реестр рисков | 10 рисков, матрица вероятность×влияние |
| [[ONBOARDING|`ONBOARDING.md`]] | 👋 Онбординг | Первые шаги, структура, контакты |
| [[FAQ|`FAQ.md`]] | ❓ FAQ | 54 вопроса и ответа |
| [[CONTACTS|`CONTACTS.md`]] | 📧 Контакты | Авторы компонентов, шаблоны писем |
| [[SCHEDULE|`SCHEDULE.md`]] | 📅 Расписание | Gantt, вехи, текущий статус |
| [[COST|`COST.md`]] | 💰 Стоимость MVP | $86,400 · 25 чел-недель |
| [[NETWORK|`NETWORK.md`]] | 🕸️  Граф связей | 20 узлов, 185 рёбер |
| [[CHANGELOG_AUTO|`CHANGELOG_AUTO.md`]] | 📋 Changelog | Авто из git-истории |
| [[DEPENDENCY_MAP|`DEPENDENCY_MAP.md`]] | 🗺️  Карта зависимостей | 49 скриптов → входы/выходы |


### 147. LLM-обогащение (Ступень 3)
_Файл: `docs/obsidian/INDEX.md` | 2 колонок, 4 строк_

| Документ | Описание |
|----------|---------|
| `LLM_ENRICHED.md` _(нет)_ | Обогащённые stub-файлы |
| `LLM_QA.md` _(нет)_ | Ответы на открытые вопросы |
| `LLM_GAPS.md` _(нет)_ | Семантические пробелы |
| [[LLM_SUMMARIES|`LLM_SUMMARIES.md`]] | AI-саммари разделов |


### 148. Топ слов по охвату файлов
_Файл: `docs/obsidian/KEYWORD_INDEX.md` | 3 колонок, 100 строк_

| Слово | Файлов | Всего упоминаний |
|-------|--------|-----------------|
| `docs` | 456 | 7625 |
| `также` | 399 | 435 |
| `смотрите` | 398 | 399 |
| `anthropic` | 395 | 5876 |
| `документы` | 391 | 505 |
| `vacancies` | 387 | 5361 |
| `похожие` | 377 | 378 |
| `сходство` | 376 | 988 |
| `knowledge` | 197 | 763 |
| `документ` | 188 | 455 |
| `agent` | 180 | 1482 |
| `nautilus` | 178 | 926 |
| `protocol` | 158 | 639 |
| `portal` | 150 | 647 |
| `work` | 144 | 560 |
| `mcp` | 140 | 850 |
| `svyazi` | 133 | 1319 |
| `open` | 133 | 427 |
| `agents` | 128 | 728 |
| `claude` | 124 | 563 |
| `содержание` | 124 | 189 |
| `review` | 121 | 401 |
| `github` | 120 | 537 |
| `first` | 119 | 386 |
| `слой` | 118 | 386 |
| `document` | 117 | 624 |
| `infrastructure` | 117 | 514 |
| `project` | 116 | 406 |
| `layer` | 116 | 546 |
| `через` | 116 | 469 |
| `если` | 115 | 614 |
| `svend` | 112 | 531 |
| `reference` | 111 | 287 |
| `appendix` | 110 | 880 |
| `агентов` | 107 | 441 |
| `между` | 104 | 333 |
| `без` | 104 | 390 |
| `foundation` | 104 | 319 |
| `model` | 102 | 272 |
| `specific` | 101 | 377 |
| `architecture` | 100 | 412 |
| `только` | 98 | 326 |
| `проекты` | 96 | 210 |
| `research` | 95 | 355 |
| `быть` | 95 | 311 |
| `projects` | 95 | 301 |
| `каждый` | 94 | 301 |
| `memory` | 93 | 631 |
| `level` | 93 | 341 |
| `implementation` | 93 | 235 |
| `context` | 92 | 231 |
| `pattern` | 92 | 346 |
| `structure` | 92 | 237 |
| `legal` | 91 | 408 |
| `integration` | 91 | 305 |
| `один` | 90 | 390 |
| `human` | 90 | 244 |
| `code` | 89 | 306 |
| `может` | 89 | 397 |
| `search` | 87 | 621 |
| `статус` | 87 | 146 |
| `author` | 87 | 252 |
| `cowork` | 87 | 955 |
| `source` | 86 | 214 |
| `проект` | 86 | 356 |
| `которые` | 86 | 328 |
| `когда` | 86 | 247 |
| `ingit` | 86 | 815 |
| `professional` | 86 | 370 |
| `what` | 86 | 542 |
| `through` | 86 | 184 |
| `collaboration` | 85 | 256 |
| `working` | 85 | 215 |
| `вопросы` | 84 | 260 |
| `sgb` | 84 | 474 |
| `existing` | 84 | 271 |
| `все` | 83 | 235 |
| `описание` | 83 | 128 |
| `api` | 83 | 232 |
| `skills` | 83 | 282 |
| `документов` | 83 | 176 |
| `readme` | 82 | 310 |
| `содержит` | 82 | 94 |
| `знаний` | 81 | 189 |
| `где` | 81 | 287 |
| `collaborations` | 80 | 436 |
| `tip` | 80 | 80 |
| `архитектура` | 79 | 232 |
| `вопрос` | 79 | 251 |
| `mvp` | 78 | 289 |
| `habr` | 78 | 361 |
| `агент` | 78 | 416 |
| `space` | 76 | 264 |
| `который` | 76 | 370 |
| `okwf` | 76 | 311 |
| `llm` | 75 | 328 |
| `tool` | 75 | 220 |
| `уже` | 74 | 385 |
| `репо` | 74 | 337 |
| `all` | 74 | 153 |


### 149. Топ биграмм (устойчивые словосочетания)
_Файл: `docs/obsidian/KEYWORD_INDEX.md` | 3 колонок, 30 строк_

| Биграмм | Файлов | Всего |
|---------|--------|-------|
| `anthropic vacancies` | 354 | 5323 |
| `docs anthropic` | 350 | 5298 |
| `portal protocol` | 68 | 361 |
| `vacancies appendix` | 52 | 381 |
| `docs collaborations` | 50 | 384 |
| `docs svyazi` | 46 | 649 |
| `professional colleague` | 43 | 198 |
| `nautilus portal` | 41 | 181 |
| `executive summary` | 40 | 183 |
| `NGT Memory` | 40 | 152 |
| `appendix minimal` | 36 | 94 |
| `minimal working` | 36 | 94 |
| `working example` | 36 | 94 |
| `turn view` | 34 | 935 |
| `knowledge-space` | 34 | 199 |
| `representative agent` | 34 | 145 |
| `table contents` | 34 | 174 |
| `double triangle` | 33 | 175 |
| `triangle architecture` | 33 | 121 |
| `composite skills` | 33 | 115 |
| `ingit cowork` | 32 | 104 |
| `vacancies abstract` | 31 | 89 |
| `principal side` | 31 | 114 |
| `oss проект` | 30 | 145 |
| `colleague agents` | 30 | 92 |
| `view turn` | 29 | 661 |
| `pattern library` | 29 | 112 |
| `skills agent` | 29 | 92 |
| `cite turn` | 28 | 489 |
| `nautilus json` | 28 | 118 |


### 150. Количество (134)
_Файл: `docs/obsidian/KPI.md` | 3 колонок, 21 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **429** | ициальных данных Anthropic Статья даёт только общие цифры (≈429 вакансий, вилка  | `00-intro` |
| **10** | овую повестку. А вы производите не исполнение, а повестку : 10 проектов, каждый  | `00-intro` |
| **27** | ным». У внешнего наблюдателя такой pattern читается иначе: «27 проектов с одной  | `00-intro` |
| **400** | задача спрос рождает предложение есть спрос например около 400 вакансий в антроп | `01-интегральный-анализ-пр` |
| **5** | т candidates формирование нескольких параллельных команд (3-5 команд по 5 челове | `01-интегральный-анализ-пр` |
| **70** | унт svend4 — это сейчас центральная точка организации ваших 70 проектов и вашей  | `01-интегральный-анализ-пр` |
| **440** | е отдельные темы , а проекции одной архитектуры . Anthropic 440 вакансий — это д | `150-appendix-c-version-hi` |
| **7** | v1.1 , формальная спецификация под текущую реальность репо (7 участников, 5 спос | `72-расписание-фазы-3` |
| **4** | fix run_all missing scripts _59617c5d_ _→ CHANGELOG_ - (4 файлов)](#кластер-26-m | `ACTION_ITEMS` |
| **22** | зких файлов > - [Кластер 1 — cowork, ingit, yes, project (22 файлов)](#кластер-1 | `CLUSTERS` |
| **17** | айлов) - [Кластер 2 — professional, agent, colleague, type (17 файлов)](#кластер | `CLUSTERS` |
| **16** | ue-type-17-файлов) - [Кластер 3 — turn, view, cite, search (16 файлов)](#кластер | `CLUSTERS` |
| **15** | search-16-файлов) - [Кластер 4 — repo, passport, npp, json (15 файлов)](#кластер | `CLUSTERS` |
| **14** | -15-файлов) - [Кластер 6 — документ, document, com, github (14 файлов)](#кластер | `CLUSTERS` |
| **13** | github-14-файлов) - [Кластер 7 — turn, view, label, svyazi (13 файлов)](#кластер | `CLUSTERS` |
| **11** | vyazi-13-файлов) - [Кластер 8 — contents, table, why, call (11 файлов)](#кластер | `CLUSTERS` |
| **8** | лов) - [Кластер 11 — editorial, collaboration, draft, date (8 файлов)](#кластер- | `CLUSTERS` |
| **6** | - [Кластер 15 — infrastructure, populations, okwf, target (6 файлов)](#кластер-1 | `CLUSTERS` |
| **12** | vacancies/326-содержание.md` — _326-содержание_ - _...и ещё 12 файлов_ ## Класте | `CLUSTERS` |
| **3** | авляет.md` — _08-что-это-продолжение-добавляет_ - _...и ещё 3 файлов_ ## Кластер | `CLUSTERS` |
| _...ещё 114_ | | |


### 151. Количество (134)
_Файл: `docs/obsidian/KPI.md` | 3 колонок, 21 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **34** | g-68-ролей) - [Sales — 150 ролей (самый большой кластер, ≈34% всего найма)](#sal | `00-intro` |
| **90** | Посадить такого человека в FDE-роль — значит амортизировать 90% реальной силы. Б | `00-intro` |
| **80** | ь README на английский как primary, русский как secondary — 80% вашей потенциаль | `00-intro` |
| **25** | цправу. Единственная proxy-проблема: роль SF-based, require 25% office presence  | `01-интегральный-анализ-пр` |
| **70** | большинства кандидатов. Но это означает, что оставшиеся 60-70% вашей деятельност | `01-интегральный-анализ-пр` |
| **100** | дата на каждую из них найти трудно — мало людей попадает на 100% под требования, | `01-интегральный-анализ-пр` |
| **40** | temporal coordination cost между незнакомцами в среднем 25-40% времени проекта.  | `01-интегральный-анализ-пр` |
| **30** | не прорывно — рынок тут уже есть, маржа тонкая, AI даёт 20-30% ускорение, не пор | `01-интегральный-анализ-пр` |
| **88** | как normative field. Это критично: STATUS.md явно признаёт 88% fallback. Нормали | `104-appendix-c-references` |
| **15** | огии: предотвращение потери. Эмпирический факт: минимум 10-15% контента каждого  | `109-3-принципы-консолидац` |
| **36** | nt employment covers declining fraction of knowledge work. 36% of US workers eng | `155-1-problem-statement` |
| **27** | workers engage in freelance/contract work in 2026, up from 27% in 2020. Foundati | `155-1-problem-statement` |
| **0** | harged fees or subjected to rent-seeking. Foundation takes 0% from contributor e | `160-6-governance-and-ethi` |
| **75** | th 100+ public patterns - Contributor satisfaction survey: >75% positive - Publi | `161-7-phased-rollout-plan` |
| **700** | нтов с advisors с 1300+ data points. SmartMatchApp заявляет 700% увеличение enga | `165-closing` |
| **20** | nd later studios. **Mechanics**: Agents typically take 10-20% commission of clie | `171-2-historical-preceden` |
| **10** | r planning. **Mechanics**: Similar commission structure (3-10% in sports, typica | `171-2-historical-preceden` |
| **7** | negotiation, paperwork. **Mechanics**: Commission-based (5-7% typical), split be | `171-2-historical-preceden` |
| **50** | s. ### 8.7. Expected Outcomes **For practitioners**: - 30-50% time reduction on  | `219-8-pilot-proposal-sgb-` |
| **95** | - Cost vs. external lawyer: 80-90% saving - Quality target: 95% citation accurac | `341-приложение-c-образец-` |
| _...ещё 59_ | | |


### 152. Количество (134)
_Файл: `docs/obsidian/KPI.md` | 3 колонок, 21 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **4–6** | з свободного текста получаются устойчивые профили и связи \| 4–6 дней \| \| Evid | `07-mvp-planning` |
| **1–2** | \| Unified cards + page/span evidence + manual reviewer UI \| 1–2 недели \| Пере | `12-roadmap` |
| **1** | и patch \| benchmark set + nightly eval + rollback policy \| 1 неделя на каркас, | `12-roadmap` |
| **15** | й журнал» в инженерном смысле. Это архив 1105 разговоров за 15 месяцев (dec 2024 | `00-intro` |
| **6** | r-track . Entrepreneur First (Paris, Berlin) — программа на 6 месяцев с €80K сти | `00-intro` |
| **3** | в GitHub как отдельная секция). Потенциал от 1⭐ до 500⭐ за 3 месяца — абсолютно  | `00-intro` |
| **2–3** | ери ко всему остальному. daten — стратегический, но требует 2–3 недели работы на | `00-intro` |
| **19** | зиторий — daten2 , 25 декабря 2025. Самый свежий — data50 , 19 часов назад. Это  | `00-intro` |
| **4** | , 19 часов назад. Это означает, что все 70 репо созданы за 4 месяца , темп — 1 р | `00-intro` |
| **30-45** | м на восприятие профиля. ### Итоговая целевая картина Через 30-45 дней вашего со | `00-intro` |
| **120** | Что мы теперь знаем точно Темп и объём. 70 репозиториев за 120 дней (декабрь 202 | `01-интегральный-анализ-пр` |
| **40** | e дроны). Эти гранты не требуют от вас переезжать, работать 40 часов, иметь PhD  | `01-интегральный-анализ-пр` |
| **10-5** | иона долларов на одну одного разработчика будет поделены на 10-5 частей и она не | `01-интегральный-анализ-пр` |
| **6-12** | ративные программы, которые берут нестандартных одиночек на 6-12 месяцев, обучаю | `01-интегральный-анализ-пр` |
| **2-3** | человек, которые не знают друг друга, будут тратить первые 2-3 месяца на выстраи | `01-интегральный-анализ-пр` |
| **3-6** | манд (3-5 команд по 5 человек), команды работают независимо 3-6 месяцев, агент м | `01-интегральный-анализ-пр` |
| **4-6** | ner (может быть Anthropic или Mistral). Proposal пишется за 4-6 недель, шанс 15- | `01-интегральный-анализ-пр` |
| **2** | икуются в общий «доска квестов»: могут быть микро (fix bug, 2 часа, XP уровня 50 | `01-интегральный-анализ-пр` |
| **1-2** | fix bug, 2 часа, XP уровня 50), средние (implement feature, 1-2 недели, XP и cur | `01-интегральный-анализ-пр` |
| **3–5** | я бы делал в следующие две недели в порядке ROI. День 1–2 (3–5 часов): fix broke | `01-интегральный-анализ-пр` |
| _...ещё 141_ | | |


### 153. Количество (134)
_Файл: `docs/obsidian/KPI.md` | 3 колонок, 21 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **$320** | hropic Статья даёт только общие цифры (≈429 вакансий, вилка $320–405 тыс.) и наз | `00-intro` |
| **$405K** | инженерные менеджеры Inference/GPU. Именно здесь «вилка до $405K» осмысленна. ## | `00-intro` |
| **$180** | для FDE в EMEA обычно ниже, чем для Research Engineer в SF ($180–280K в пересчёт | `00-intro` |
| **€3** | , а основатель . У вас есть готовые MVP-backlog'и, бюджеты (€3–5K минимальный, € | `00-intro` |
| **€16K** | вас есть готовые MVP-backlog'и, бюджеты (€3–5K минимальный, €16K полный для Smar | `00-intro` |
| **€80K** | trepreneur First (Paris, Berlin) — программа на 6 месяцев с €80K стипендией, спе | `00-intro` |
| **€29** | сли этот один проект дойдёт до 100 платящих пользователей × €29/мес = €2.9K/мес  | `00-intro` |
| **€2.9K** | дин проект дойдёт до 100 платящих пользователей × €29/мес = €2.9K/мес MRR — это  | `00-intro` |
| **€250K** | я заявка. Гранты под конкретные кластеры. Aktion Mensch (до €250K на проекты инк | `01-интегральный-анализ-пр` |
| **€3K** | ий . DPMA (Deutsches Patent- und Markenamt) с госпошлинами ~€3K за каждый + pate | `01-интегральный-анализ-пр` |
| **$500K** | ondon). Что, если вместо найма одного человека за, условно, $500K в год, этот бю | `01-интегральный-анализ-пр` |
| **$100K** | es. Корпорация типа Anthropic не может просто так разослать $100K в Дрезден, Буэ | `01-интегральный-анализ-пр` |
| **€4** | ted research teams for beneficial AI deployments». Грант до €4M, 3 года. Disabil | `01-интегральный-анализ-пр` |
| **$10** | нчурная траектория — рискованная, но если thesis верна, это $10-50M Series A чер | `01-интегральный-анализ-пр` |
| **€20** | а получить работающий документированный кейс . 3-6 месяцев, €20-50K. Это станови | `01-интегральный-анализ-пр` |
| **€1** | ect . EIC Pathfinder Open или Horizon Europe HumanE AI Net. €1-4M грант на 2-3 г | `01-интегральный-анализ-пр` |
| **$3** | artup . Entrepreneur First Berlin, Y Combinator, Seed Round $3-5M. Требует cofou | `01-интегральный-анализ-пр` |
| **$5** | Google DeepMind, Microsoft AI, Mistral, Anthropic), budget $5-20M/year, which: - | `150-appendix-c-version-hi` |
| **$1** | - Provides minimum stipend (не full salary, но dignified — $1-3K/month part-time | `150-appendix-c-version-hi` |
| **€500** | es. Economic layer: - Base stipend для active contributors (€500-1500/month part | `150-appendix-c-version-hi` |
| _...ещё 217_ | | |


### 154. Количество (134)
_Файл: `docs/obsidian/KPI.md` | 3 колонок, 8 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **80** | y‑слое**: Auto AI Router даёт lightweight sidecar в Go с 30–80 MB RAM и OpenAI‑с | `04-ensembles-overview` |
| **78** | архив 1105 разговоров за 15 месяцев (dec 2024 → mar 2026), 78 МБ текста, 29 802  | `00-intro` |
| **7.4** | у: Первый — статистика по 10 кластерам . Главный по объёму (7.4 МБ / 300 разгово | `00-intro` |
| **4.6** | Следующие три по потенциалу — дроны и SkyMediaHub Bavaria (4.6 МБ, 13 конкретных | `00-intro` |
| **4.1** | ми партнёрам Fraunhofer/Bundeswehr/TechHUB SVI), ИИ/агенты (4.1 МБ), и робототех | `00-intro` |
| **2.0** | ndeswehr/TechHUB SVI), ИИ/агенты (4.1 МБ), и робототехника (2.0 МБ, 15 роботов с | `00-intro` |
| **2** | право 7.4 МБ, дроны 4.6 МБ, ИИ-агенты 4.1 МБ, робототехника 2 МБ. Центральные те | `01-интегральный-анализ-пр` |
| **16** | push-to-talk с Pause-key, Whisper large-v3-turbo на NVIDIA 16GB или Apple Silico | `00-intro` |


### 155. Количество (134)
_Файл: `docs/obsidian/KPI.md` | 3 колонок, 18 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **0.1.5** | **MIT**. citeturn33view4turn27view0 \| Рабочий прототип, версия 0.1.5; “рабо | `03-component-catalog` |
| **4.5** | veloper для Claude-платформы : 87 skills, chat-migration v1→v4.5 quantum-hybrid, | `00-intro` |
| **1.0** | ntrag auf PB/Fristverlängerung/Nachzahlung), Master Dossier v1.0, анализ BSG-пра | `00-intro` |
| **1.1** | овместимости (0–3) - Как версионируется сам протокол (v1.0, v1.1, breaking chang | `02-общий-план-развития-na` |
| **2.0** | ем понадобится writing — это отдельный extension протокола (v2.0 или как опциона | `02-общий-план-развития-na` |
| **1.0.0** | desyncronize). Каждый релиз — git tag + CHANGELOG. Semver: v1.0.0, v1.0.1, v1.1. | `02-общий-план-развития-na` |
| **1.0.1** | onize). Каждый релиз — git tag + CHANGELOG. Semver: v1.0.0, v1.0.1, v1.1.0. CHAN | `02-общий-план-развития-na` |
| **1.1.0** | Каждый релиз — git tag + CHANGELOG. Semver: v1.0.0, v1.0.1, v1.1.0. CHANGELOG.md | `02-общий-план-развития-na` |
| **0.2.0** | 98-appendix-a-minimal-working-example.md) _33%_ - [Planned (v0.2.0)](docs/02-ant | `04-abstract` |
| **3.1.0** | RFCs to Indicate Requirement Levels - OpenAPI Specification v3.1.0 (for REST API | `104-appendix-c-references` |
| **1.2** | прямое следствие этого. #### Что я сознательно оставил для v1.2 или v2.0 Formal  | `104-appendix-c-references` |
| **3.0** | Удалить transitional header 7. Добавить changelog-запись: «v3.0 consolidated fro | `110-вопрос-fallback-ratio` |
| **0.6.0** | laude (Анастасия Бутова, AnastasiyaW) — реально существует, версия 0.6.0, MIT, 1 | `365-развёрнутый-анализ-вн` |
| **3.2** | viewer 1 (GPT-5.4): проверяет логику - Reviewer 2 (DeepSeek-V3.2): проверяет --- | `02-knowledge-graphs` |
| **0.1** | st per card, trace completeness. MVP boundary: что входит в v0.1, что запрещено  | `14-ограничения-лицензии-и` |
| **0.2** | leteness. MVP boundary: что входит в v0.1, что запрещено до v0.2. Pilot scenario | `14-ограничения-лицензии-и` |
| **0.11.0** | лицензия. К 23 апреля 2026 (несколько дней назад) — версия v0.11.0 с 95 600+ звё | `TABLES` |
| **5.0.6** | 2026` \| азработка : версии HMP-0001 → HMP-0005 (март 2026, версия 5.0.6) - Доку | `TABLES` |


### 156. Количество (134)
_Файл: `docs/obsidian/KPI.md` | 3 колонок, 7 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **10** | nts (≈8 репо)](#кластер-4-archives-experiments-8-репо) - [Топ-10 репо, в которые | `00-intro` |
| **5** | sh/git), либо помочь с English README-драфтом для одного из топ-5, либо проработ | `00-intro` |
| **30** | с обратных ссылок **Файлов с входящими ссылками:** 532 ## Топ-30 самых цитируемы | `BACKLINKS` |
| **20** | ь документы](#рекомендуется-создать-документы) - [Детали по топ-20 пробелам](#де | `CONTENT_GAPS` |
| **15** | ontents) - [Качество по разделам](#качество-по-разделам) - [[PRIORITIES|Топ-15 лучших докуме | `METRICS` |
| **50** | ты файлов]] > > !TIP - Содержание - Топ-50 самых важных файло | `OUTLINE` |
| **3** | **Файлов проанализировано:** 433 Для каждого документа — топ-3 похожих по словар | `SIMILAR` |


### 157. Количество (134)
_Файл: `docs/obsidian/KPI.md` | 3 колонок, 6 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **1** | les . Каждая фаза имеет smoke-test: завершена или нет. #### Фаза 1 — Спецификаци | `02-общий-план-развития-na` |
| **2** | адаптер для нового репо без задавания вопросов автору? #### Фаза 2 — Reference i | `02-общий-план-развития-na` |
| **3** | озвращает non-empty результат с consensus-информацией? #### Фаза 3 — MCP интерфе | `02-общий-план-развития-na` |
| **4** | кристалла», получить osmыслený ответ с указанием репо. #### Фаза 4 — Web interfa | `02-общий-план-развития-na` |
| **5** | y через браузер, получить отформатированный результат. #### Фаза 5 — Публикация  | `02-общий-план-развития-na` |
| **0** | ёртывания](#9-стратегия-поэтапного-развёртывания) - [[TIMELINE|9.1. Фаза 0 — Основание (Ме | `199-9-стратегия-поэтапног` |


### 158. Текущие метрики
_Файл: `docs/obsidian/KPI_HISTORY.md` | 3 колонок, 7 строк_

| Метрика | Значение | Тренд |
|---------|---------|-------|
| Markdown документов | **529** | → |
| Слов | **523,868** | → |
| Скриптов | **125** | → |
| Скоринг | **93%** | → |
| Здоровье | **90/100** | → |
| KPI показателей | **737** | → |
| Открытых вопросов | **39** | → |


### 159. Индекс ссылок
_Файл: `docs/obsidian/LINKS.md` | 2 колонок, 188 строк_

| URL | Найден в файлах |
|-----|-----------------|
| http://localhost:8000 | 7 |
| http://localhost:8080 | 5 |
| https://...install.sh | 4 |
| https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakansiy-s-zarplatoy-do-405000 | 4 |
| https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakans… | 3 |
| https://activitypub.rocks/ | 4 |
| https://api.github.com/users/svend4/repos?per_page=100&sort=updated | 5 |
| https://api.github.com/users/svend4/repos?per_page=100&sort=updated&type=owner | 5 |
| https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv | 2 |
| https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW | 1 |
| https://claude.com/product/cowork | 9 |
| https://creativecommons.org/licenses/by/4.0/ | 5 |
| https://forum.obsidian.md/t/new-plugin-llm-wiki-turn-your-vault-into-a-queryable-knowledge-base-privately/113223 | 5 |
| https://github | 2 |
| https://github.com/AnastasiyaW | 2 |
| https://github.com/AnastasiyaW/knowledge-space | 5 |
| https://github.com/AnastasiyaW/knowledge-space` | 1 |
| https://github.com/Antipozitive | 2 |
| https://github.com/Cutcode | 2 |
| https://github.com/Dmitriila | 2 |
| https://github.com/MiXaiLL76 | 2 |
| https://github.com/Sonia_Black | 2 |
| https://github.com/VitalyOborin | 2 |
| https://github.com/VladSpace | 2 |
| https://github.com/andrey_chuyan | 2 |
| https://github.com/anthropics/mcp | 5 |
| https://github.com/anthropics/mcp` | 1 |
| https://github.com/camel-ai/camel | 5 |
| https://github.com/kksudo | 2 |
| https://github.com/mcp | 7 |
| https://github.com/mcp` | 1 |
| https://github.com/nlaik | 2 |
| https://github.com/settings/tokens | 5 |
| https://github.com/settings/tokens` | 1 |
| https://github.com/spbmolot | 2 |
| https://github.com/svend4/ | 3 |
| https://github.com/svend4/` | 1 |
| https://github.com/svend4/data70 | 5 |
| https://github.com/svend4/data70` | 1 |
| https://github.com/svend4/info1 | 8 |
| https://github.com/svend4/info1` | 1 |
| https://github.com/svend4/info40 | 4 |
| https://github.com/svend4/info7 | 4 |
| https://github.com/svend4/ingit | 13 |
| https://github.com/svend4/ingit/issues | 4 |
| https://github.com/svend4/ingit/issues` | 1 |
| https://github.com/svend4/ingit` | 1 |
| https://github.com/svend4/meta | 6 |
| https://github.com/svend4/meta` | 1 |
| https://github.com/svend4/nautilus | 14 |
| https://github.com/svend4/nautilus.git | 3 |
| https://github.com/svend4/nautilus/blob/claude/review-nautilus-changes-tdywx/README.md | 3 |
| https://github.com/svend4/nautilus/blob/main/INTEGRATION.md | 3 |
| https://github.com/svend4/nautilus/blob/main/PORTAL-PROTOCOL | 1 |
| https://github.com/svend4/nautilus/blob/main/PORTAL-PROTOCOL.md | 3 |
| https://github.com/svend4/nautilus/blob/main/README.md | 3 |
| https://github.com/svend4/nautilus/blob/main/REVIEW_METHODOLOGY.md | 3 |
| https://github.com/svend4/nautilus/blob/main/STATUS.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_1.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_2.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_3.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_4.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/PORTAL-PROTOCOL-v1.0.md | 3 |
| https://github.com/svend4/nautilus/branches | 3 |
| https://github.com/svend4/nautilus/commits/main | 3 |
| https://github.com/svend4/nautilus/issues | 18 |
| https://github.com/svend4/nautilus/issues` | 1 |
| https://github.com/svend4/nautilus/tree/abfa80e853594454bae03e95ba09f12eb443ca50/docs | 3 |
| https://github.com/svend4/nautilus/tree/main/adapters | 3 |
| https://github.com/svend4/nautilus/tree/main/passports | 3 |
| https://github.com/svend4/nautilus` | 1 |
| https://github.com/svend4/pro2 | 8 |
| https://github.com/svend4/pro2/blob/main/nautilus/README.md | 3 |
| https://github.com/svend4/pro2/tree/6637d1299af963db66485aa5599346d41badc6dc/nautilus | 3 |
| https://github.com/svend4/pro2/tree/main/nautilus | 3 |
| https://github.com/svend4/pro2/tree/main/nautilus` | 1 |
| https://github.com/svend4/pro2` | 1 |
| https://github.com/svend4?tab=repositories | 3 |
| https://github.com/svend4?tab=repositories` | 1 |
| https://github.com/tagir_analyzes | 1 |
| https://github.com/zodigancode | 1 |
| https://habr. | 3 |
| https://habr.com/ru/articles/1002138/ | 4 |
| https://habr.com/ru/articles/1002138/` | 1 |
| https://habr.com/ru/articles/1005776/ | 4 |
| https://habr.com/ru/articles/1005776/` | 1 |
| https://habr.com/ru/articles/1006602/ | 3 |
| https://habr.com/ru/articles/1006602/, | 3 |
| https://habr.com/ru/articles/1006602/` | 1 |
| https://habr.com/ru/articles/1006622/ | 6 |
| https://habr.com/ru/articles/1006622/` | 1 |
| https://habr.com/ru/articles/1007122/ | 4 |
| https://habr.com/ru/articles/1007122/, | 3 |
| https://habr.com/ru/articles/1007122/` | 1 |
| https://habr.com/ru/articles/1009538/ | 4 |
| https://habr.com/ru/articles/1009538/` | 1 |
| https://habr.com/ru/articles/1009608/ | 4 |
| https://habr.com/ru/articles/1009608/` | 1 |
| https://habr.com/ru/articles/1009958/ | 4 |
| https://habr.com/ru/articles/1009958/` | 1 |
| https://habr.com/ru/articles/1010198/ | 4 |
| https://habr.com/ru/articles/1010198/` | 1 |
| https://habr.com/ru/articles/1010478/ | 4 |
| https://habr.com/ru/articles/1010478/` | 1 |
| https://habr.com/ru/articles/1012894/ | 3 |
| https://habr.com/ru/articles/1014366/ | 3 |
| https://habr.com/ru/articles/1016096/ | 4 |
| https://habr.com/ru/articles/1016096/` | 1 |
| https://habr.com/ru/articles/1017200/ | 4 |
| https://habr.com/ru/articles/1017200/` | 1 |
| https://habr.com/ru/articles/1019588/ | 3 |
| https://habr.com/ru/articles/1019588/, | 3 |
| https://habr.com/ru/articles/1019588/` | 1 |
| https://habr.com/ru/articles/1020598/ | 3 |
| https://habr.com/ru/articles/1020598/, | 3 |
| https://habr.com/ru/articles/1020598/` | 1 |
| https://habr.com/ru/articles/1020860/ | 4 |
| https://habr.com/ru/articles/1020860/` | 1 |
| https://habr.com/ru/articles/1021622/ | 3 |
| https://habr.com/ru/articles/1023446/ | 4 |
| https://habr.com/ru/articles/1023446/` | 1 |
| https://habr.com/ru/articles/1024634/ | 4 |
| https://habr.com/ru/articles/1024634/` | 1 |
| https://habr.com/ru/articles/1024884/comments/ | 4 |
| https://habr.com/ru/articles/1024884/comments/` | 1 |
| https://habr.com/ru/articles/1026666/ | 3 |
| https://habr.com/ru/articles/1027210/ | 4 |
| https://habr.com/ru/articles/1027210/` | 1 |
| https://habr.com/ru/articles/1027382/ | 4 |
| https://habr.com/ru/articles/1027382/` | 1 |
| https://habr.com/ru/articles/1027658/ | 4 |
| https://habr.com/ru/articles/1027658/` | 1 |
| https://habr.com/ru/articles/1027724/ | 6 |
| https://habr.com/ru/articles/1027724/` | 1 |
| https://habr.com/ru/articles/1027878/ | 3 |
| https://habr.com/ru/articles/1027878/, | 3 |
| https://habr.com/ru/articles/1027878/` | 1 |
| https://habr.com/ru/articles/495554/ | 3 |
| https://habr.com/ru/articles/893356/ | 4 |
| https://habr.com/ru/articles/893356/` | 1 |
| https://habr.com/ru/articles/938626/ | 3 |
| https://habr.com/ru/articles/938626/, | 3 |
| https://habr.com/ru/articles/938626/` | 1 |
| https://habr.com/ru/articles/943498/ | 3 |
| https://habr.com/ru/articles/943498/, | 3 |
| https://habr.com/ru/articles/943498/` | 1 |
| https://habr.com/ru/articles/955798/ | 4 |
| https://habr.com/ru/articles/955798/` | 1 |
| https://habr.com/ru/articles/975414/ | 4 |
| https://habr.com/ru/articles/975414/` | 1 |
| https://habr.com/ru/articles/983684/ | 4 |
| https://habr.com/ru/articles/983684/` | 1 |
| https://habr.com/ru/articles/996144/ | 4 |
| https://habr.com/ru/articles/996144/` | 1 |
| https://habr.com/ru/companies/airi/articles/1000720/ | 4 |
| https://habr.com/ru/companies/airi/articles/1000720/` | 1 |
| https://habr.com/ru/companies/airi/articles/855128/ | 4 |
| https://habr.com/ru/companies/airi/articles/855128/` | 1 |
| https://habr.com/ru/companies/surfstudio/articles/943108/ | 4 |
| https://habr.com/ru/companies/surfstudio/articles/943108/` | 1 |
| https://habr.com/ru/companies/teamly/articles/1024062/ | 3 |
| https://habr.com/ru/companies/yandex/articles/1019928/ | 4 |
| https://habr.com/ru/companies/yandex/articles/1019928/` | 1 |
| https://habr.com/ru/companies/yoomoney/articles/1012870/ | 4 |
| https://habr.com/ru/companies/yoomoney/articles/1012870/` | 1 |
| https://happyin.space/ | 3 |
| https://nautilus-okwf.org/sub-agents/sgb-ix-paragraph-78-24-7 | 3 |
| https://olegtalks.ru/base/tpost/xn7kev4fa1-docling-gotovim-dannie-dlya-rag-i-llm | 4 |
| https://raw.githubusercontent.com/svend4/nautilus/main/adapters/base.py | 4 |
| https://raw.githubusercontent.com/svend4/nautilus/main/glyph_adapter.py | 4 |
| https://raw.githubusercontent.com/svend4/nautilus/main/nautilus.json | 4 |
| https://raw.githubusercontent.com/svend4/nautilus/main/passports/info1.md | 4 |
| https://raw.githubusercontent.com/svend4/nautilus/main/portal.py | 4 |
| https://raw.githubusercontent.com/svend4/nautilus/main/requirements.txt | 4 |
| https://raw.githubusercontent.com/svend4/pro2/main/README.md | 4 |
| https://raw.githubusercontent.com/svend4/pro2/main/nautilus/README.md | 4 |
| https://raw.githubusercontent.com/svend4/pro2/main/nautilus/adapters/base.py | 4 |
| https://raw.githubusercontent.com/svend4/pro2/main/nautilus/adapters/info1.py | 4 |
| https://raw.githubusercontent.com/svend4/pro2/main/nautilus/nautilus.json | 4 |
| https://solidproject.org/ | 3 |
| https://support.claude.com/en/collections/13345190-cowork | 4 |
| https://vc.ru/id744101/2789872 | 4 |
| https://web.hypothes.is/ | 4 |
| https://www.camel-ai.org | 3 |
| https://www.discourse.org/ | 4 |
| https://www.fontanka.ru/2026/04/25/76378978/ | 7 |
| https://www.fossil-scm.org/ | 4 |
| https://www.w3.org/standards/semanticweb/data | 3 |


### 160. Качество по разделам
_Файл: `docs/obsidian/METRICS.md` | 6 колонок, 6 строк_

| Раздел | Балл | Ссылок/1K слов | Код-блоков/1K | % с summary | % с тегами |
|--------|------|----------------|--------------|-------------|------------|
| **01-svyazi** | 72 | 30.7 | 0.5 | 100% | 100% |
| **02-anthropic-vacancies** | 77 | 50.8 | 0.7 | 100% | 100% |
| **03-technology-combinations** | 65 | 38.4 | 0.0 | 100% | 86% |
| **04-ai-collaborations** | 83 | 26.9 | 0.0 | 94% | 94% |
| **05-habr-projects** | 62 | 51.2 | 0.0 | 78% | 78% |
| **root** | 63 | 22.1 | 1.1 | 67% | 69% |


### 161. Топ-15 лучших документов
_Файл: `docs/obsidian/METRICS.md` | 3 колонок, 15 строк_

| Документ | Балл | Слов |
|----------|------|------|
| `01-интегральный-анализ-профиля-svend4` | 100 | 19103 |
| `02-общий-план-развития-nautilus-portal-p` | 100 | 3181 |
| `109-3-принципы-консолидации-фаза-c` | 100 | 541 |
| `133-обратная-связь` | 100 | 16959 |
| `139-2-the-double-triangle-architecture` | 100 | 755 |
| `142-5-pattern-library-as-bridge-between-` | 100 | 689 |
| `228-appendix-c-quick-start-architecture-` | 100 | 1730 |
| `232-1-типология-из-пяти-типов-агентов-на` | 100 | 885 |
| `248-приложение-c-архитектура-быстрого-ст` | 100 | 3425 |
| `330-4-симбиотическая-архитектура` | 100 | 697 |
| `331-5-четыре-пути-интеграции-в-порядке-д` | 100 | 807 |
| `341-приложение-c-образец-спецификаций-ин` | 100 | 20414 |
| `342-что-такое-вариант-c-concept-document` | 100 | 11237 |
| `365-развёрнутый-анализ-внуковой-комбинац` | 100 | 4385 |
| `366-технический-stack-svyazi-2-0-foundat` | 100 | 3835 |


### 162. Документы, требующие улучшения (16)
_Файл: `docs/obsidian/METRICS.md` | 3 колонок, 16 строк_

| Документ | Балл | Что отсутствует |
|----------|------|----------------|
| `ABBREVIATIONS` | 30 | summary, tags, TOC, callout |
| `AUTHORS` | 30 | summary, tags, TOC, callout |
| `BACKLINKS` | 30 | summary, tags, TOC, callout |
| `BROKEN_LINKS` | 30 | summary, tags, TOC, callout |
| `COMPLEXITY` | 30 | summary, tags, TOC, callout |
| `CROSSREFS` | 30 | summary, tags, TOC, callout |
| `DENSITY` | 30 | summary, tags, TOC, callout |
| `GLOSSARY` | 30 | summary, tags, TOC, callout |
| `KPI` | 30 | summary, tags, TOC, callout |
| `LINKS` | 30 | summary, tags, TOC, callout |
| `MISSING` | 30 | summary, tags, TOC, callout |
| `PRIORITIES` | 30 | summary, tags, TOC, callout |
| `QUESTIONS` | 30 | summary, tags, TOC, callout |
| `SENTIMENT` | 30 | summary, tags, TOC, callout |
| `TAGS` | 30 | summary, tags, TOC, callout |
| `WORD_FREQ` | 30 | summary, tags, TOC, callout |


### 163. Легенда
_Файл: `docs/obsidian/MINDMAP.md` | 2 колонок, 7 строк_

| Слой | Проекты |
|------|---------|
| Ingestion | Svyazi, CardIndex, Firecrawl |
| Knowledge | AgentFS, knowledge-space |
| Memory | Yodoca, NGT Memory, MemNet |
| RAG | LiteParse, Legal RAG, Hybrid RAG, Graph RAG |
| Orchestration | mclaude, AI Factory, Rufler, AutoResearch |
| Security | LiteLLM, SENTINEL, Tool Search, Auto AI Router |
| Sync | Yjs, Automerge |


### 164. Карта пробелов знаний
_Файл: `docs/obsidian/MISSING.md` | 6 колонок, 25 строк_

| Статус | Тема / Проект | Файлов | Слов | Минимум | Примеры файлов |
|--------|---------------|--------|------|---------|----------------|
| ✅ | **Svyazi** | 139 | 147259 | ≥5ф/2000сл | `WORD_FREQ.md`, `SCHEDULE.md` |
| ✅ | **local-first** | 86 | 76720 | ≥2ф/300сл | `FOOTNOTES.md`, `READING_TIME.md` |
| ✅ | **Yodoca** | 82 | 94054 | ≥2ф/300сл | `WORD_FREQ.md`, `SCHEDULE.md` |
| ✅ | **AgentFS** | 75 | 51824 | ≥3ф/500сл | `WORD_FREQ.md`, `SCHEDULE.md` |
| ✅ | **CardIndex** | 72 | 64659 | ≥3ф/500сл | `SCHEDULE.md`, `QUESTIONS.md` |
| ✅ | **self-improvement** | 68 | 10445 | ≥1ф/100сл | `FOOTNOTES.md`, `CONSISTENCY.md` |
| ✅ | **SENTINEL** | 63 | 42718 | ≥2ф/200сл | `SCHEDULE.md`, `FOOTNOTES.md` |
| ✅ | **knowledge-space** | 60 | 45031 | ≥3ф/500сл | `FOOTNOTES.md`, `BROKEN_LINKS.md` |
| ✅ | **Rufler** | 60 | 36210 | ≥2ф/200сл | `FOOTNOTES.md`, `GLOSSARY.md` |
| ✅ | **NGT Memory** | 58 | 46599 | ≥2ф/300сл | `GLOSSARY.md`, `CONSISTENCY.md` |
| ✅ | **LiteParse** | 56 | 40011 | ≥2ф/300сл | `TIMELINE.md`, `GLOSSARY.md` |
| ✅ | **mclaude** | 50 | 38201 | ≥2ф/200сл | `GLOSSARY.md`, `TABLES.md` |
| ✅ | **AI Factory** | 50 | 38849 | ≥2ф/200сл | `GLOSSARY.md`, `CONSISTENCY.md` |
| ✅ | **AutoResearch** | 31 | 25807 | ≥1ф/100сл | `GLOSSARY.md`, `CONTENT_GAPS.md` |
| ✅ | **Evidence Envelope** | 25 | 9677 | ≥2ф/200сл | `CONSISTENCY.md`, `TABLES.md` |
| ✅ | **Sozialrecht** | 24 | 65857 | ≥1ф/200сл | `READING_TIME.md`, `TABLES.md` |
| ✅ | **CRDT** | 22 | 17414 | ≥1ф/100сл | `FOOTNOTES.md`, `CONTENT_GAPS.md` |
| ✅ | **Card Envelope** | 15 | 7654 | ≥2ф/200сл | `TABLES.md`, `ACTION_ITEMS.md` |
| ✅ | **бюджетный роутинг** | 14 | 16685 | ≥2ф/300сл | `RISK_REGISTER.md`, `TABLES.md` |
| ✅ | **Memory Write Policy** | 11 | 6583 | ≥2ф/200сл | `QUESTIONS.md`, `TABLES.md` |
| ✅ | **Skill Policy** | 11 | 3730 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |
| ✅ | **Review Record** | 11 | 6235 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |
| ✅ | **privacy by design** | 11 | 11190 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |
| ✅ | **лицензия BSL** | 3 | 1439 | ≥1ф/50сл | `RISK_REGISTER.md`, `TABLES.md` |
| ✅ | **voice ingestion** | 2 | 760 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |


### 165. 👤 People (17)
_Файл: `docs/obsidian/NAMED_ENTITIES.md` | 3 колонок, 17 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `anthropic` | 401 | people |
| `claude` | 163 | people |
| `svend4` | 91 | people |
| `kksudo` | 52 | people |
| `spbmolot` | 47 | people |
| `vitalyoborin` | 23 | people |
| `anastasiyaw` | 23 | people |
| `andrey_chuyan` | 12 | people |
| `camel-ai` | 3 | people |
| `settings` | 2 | people |
| `anthropics` | 2 | people |
| `yjs` | 2 | people |
| `dementev-dev` | 2 | people |
| `artur-gavronchuk` | 2 | people |
| `nicholasspisak` | 2 | people |
| `vuguzum` | 2 | people |
| `users` | 2 | people |


### 166. 👤 People (17)
_Файл: `docs/obsidian/NAMED_ENTITIES.md` | 3 колонок, 40 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `nautilus` | 179 | projects |
| `svyazi` | 121 | projects |
| `github` | 121 | projects |
| `ngt` | 79 | projects |
| `yodoca` | 71 | projects |
| `agentfs` | 71 | projects |
| `CardIndex` | 68 | projects |
| `lorenzo` | 63 | projects |
| `knowledge-space` | 53 | projects |
| `LiteParse` | 47 | projects |
| `obsidian` | 36 | projects |
| `notion` | 32 | projects |
| `PortalEntry` | 30 | projects |
| `AutoResearch` | 25 | projects |
| `MemNet` | 22 | projects |
| `QueryResult` | 21 | projects |
| `wikontic` | 21 | projects |
| `VladSpace` | 20 | projects |
| `gpt` | 19 | projects |
| `gemini` | 10 | projects |
| `ingit` | 10 | projects |
| `OpenWhispr` | 9 | projects |
| `TypeScript` | 9 | projects |
| `BaseAdapter` | 9 | projects |
| `AutoGen` | 9 | projects |
| `CodeWiki` | 8 | projects |
| `mistral` | 8 | projects |
| `LangChain` | 8 | projects |
| `faiss` | 7 | projects |
| `DeepSeek` | 7 | projects |
| `DeepMind` | 7 | projects |
| `chromadb` | 7 | projects |
| `WebSocket` | 6 | projects |
| `ChatDev` | 6 | projects |
| `AutoAdapter` | 6 | projects |
| `DevOps` | 6 | projects |
| `OpenClaw` | 6 | projects |
| `LlamaIndex` | 5 | projects |
| `info1` | 5 | projects |
| `pro2` | 5 | projects |


### 167. 👤 People (17)
_Файл: `docs/obsidian/NAMED_ENTITIES.md` | 3 колонок, 29 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `mcp` | 146 | tech |
| `api` | 80 | tech |
| `rag` | 72 | tech |
| `llm` | 71 | tech |
| `json` | 59 | tech |
| `markdown` | 54 | tech |
| `git` | 48 | tech |
| `yaml` | 44 | tech |
| `python` | 43 | tech |
| `go` | 37 | tech |
| `rest` | 27 | tech |
| `html` | 15 | tech |
| `ci` | 14 | tech |
| `transformer` | 14 | tech |
| `sqlite` | 12 | tech |
| `cd` | 11 | tech |
| `vector` | 10 | tech |
| `react` | 9 | tech |
| `docker` | 7 | tech |
| `rust` | 7 | tech |
| `postgresql` | 6 | tech |
| `bm25` | 5 | tech |
| `jaccard` | 5 | tech |
| `cosine` | 3 | tech |
| `css` | 3 | tech |
| `fastapi` | 3 | tech |
| `webhook` | 3 | tech |
| `kubernetes` | 3 | tech |
| `graphql` | 2 | tech |


### 168. 👤 People (17)
_Файл: `docs/obsidian/NAMED_ENTITIES.md` | 3 колонок, 8 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `вк` | 126 | orgs |
| `meta` | 95 | orgs |
| `mail` | 32 | orgs |
| `openai` | 21 | orgs |
| `google` | 14 | orgs |
| `microsoft` | 11 | orgs |
| `yandex` | 6 | orgs |
| `сбер` | 4 | orgs |


### 169. 👤 People (17)
_Файл: `docs/obsidian/NAMED_ENTITIES.md` | 3 колонок, 30 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `2026-04` | 79 | dates |
| `2026-04-29` | 14 | dates |
| `2026-04-19` | 11 | dates |
| `апрель 2026` | 10 | dates |
| `2026-04-26` | 9 | dates |
| `апреля 2026` | 7 | dates |
| `2026/04/25` | 7 | dates |
| `в 2026 году` | 6 | dates |
| `март 2026` | 5 | dates |
| `декабрь 2025` | 5 | dates |
| `декабря 2025` | 4 | dates |
| `апреле 2026` | 4 | dates |
| `январе 2026` | 4 | dates |
| `марта 2026` | 3 | dates |
| `декабрь 2024` | 3 | dates |
| `2026-05-03` | 3 | dates |
| `2024-01-01` | 3 | dates |
| `2025-12-15` | 3 | dates |
| `май 2025` | 3 | dates |
| `феврале 2025` | 3 | dates |
| `2026-04-15` | 3 | dates |
| `Сентябрь 2025` | 3 | dates |
| `января 2026` | 3 | dates |
| `февраль 2026` | 3 | dates |
| `2026-04-22` | 3 | dates |
| `ноябре 2025` | 2 | dates |
| `2026-02-01` | 2 | dates |
| `2025-11-12` | 2 | dates |
| `февраля 2026` | 2 | dates |
| `2026-10-15` | 2 | dates |


### 170. Топ-20 ко-упоминаемых пар
_Файл: `docs/obsidian/NETWORK.md` | 2 колонок, 20 строк_

| Пара | Общих файлов |
|------|-------------|
| **Cowork** ↔ **ingit** | 106 |
| **Svyazi** ↔ **NGT** | 78 |
| **Yodoca** ↔ **NGT** | 75 |
| **Svyazi** ↔ **Yodoca** | 71 |
| **Svyazi** ↔ **AgentFS** | 67 |
| **AgentFS** ↔ **NGT** | 65 |
| **AgentFS** ↔ **Yodoca** | 61 |
| **Svyazi** ↔ **CardIndex** | 57 |
| **CardIndex** ↔ **NGT** | 56 |
| **Андрей (kksudo)** ↔ **Виталий (spbmolot)** | 56 |
| **Svyazi** ↔ **SENTINEL** | 55 |
| **Svyazi** ↔ **Rufler** | 55 |
| **Svyazi** ↔ **Андрей (kksudo)** | 55 |
| **CardIndex** ↔ **AgentFS** | 53 |
| **AgentFS** ↔ **SENTINEL** | 53 |
| **Cowork** ↔ **Lorenzo (svend4)** | 52 |
| **Svyazi** ↔ **Lorenzo** | 51 |
| **Svyazi** ↔ **Виталий (spbmolot)** | 51 |
| **AgentFS** ↔ **Rufler** | 51 |
| **NGT** ↔ **Rufler** | 51 |


### 171. Центральность узлов (влиятельность)
_Файл: `docs/obsidian/NETWORK.md` | 3 колонок, 20 строк_

| Узел | Балл центральности | Тип |
|------|--------------------|-----|
| **Svyazi** | 926 | 📦 Проект |
| **NGT** | 796 | 📦 Проект |
| **Yodoca** | 739 | 📦 Проект |
| **AgentFS** | 707 | 📦 Проект |
| **CardIndex** | 623 | 📦 Проект |
| **Rufler** | 588 | 📦 Проект |
| **SENTINEL** | 580 | 📦 Проект |
| **knowledge-space** | 575 | 📦 Проект |
| **Андрей (kksudo)** | 548 | 👤 Автор |
| **LiteParse** | 546 | 📦 Проект |
| **mclaude** | 512 | 📦 Проект |
| **AI Factory** | 502 | 📦 Проект |
| **Виталий (spbmolot)** | 498 | 👤 Автор |
| **ingit** | 473 | 📦 Проект |
| **Cowork** | 470 | 📦 Проект |
| **Lorenzo** | 455 | 📦 Проект |
| **Lorenzo (svend4)** | 405 | 👤 Автор |
| **MemNet** | 380 | 📦 Проект |
| **Wikontic** | 298 | 📦 Проект |
| **Firecrawl** | 137 | 📦 Проект |


### 172. Структура документации
_Файл: `docs/obsidian/ONBOARDING.md` | 4 колонок, 5 строк_

| Раздел | Тема | Файлов | Слов |
|--------|------|--------|------|
| [[README|`docs/01-svyazi/`]] | Архитектура Svyazi 2.0 | 16 | 10,166 |
| [[README|`docs/02-anthropic-vacancies/`]] | Вакансии Anthropic | 357 | 260,905 |
| [[README|`docs/03-technology-combinations/`]] | Комбинации технологий | 7 | 2,433 |
| [[README|`docs/04-ai-collaborations/`]] | AI-коллаборации | 17 | 25,169 |
| [[README|`docs/05-habr-projects/`]] | Хабр-проекты | 10 | 8,564 |


### 173. Ключевые документы
_Файл: `docs/obsidian/ONBOARDING.md` | 2 колонок, 8 строк_

| Документ | Зачем читать |
|----------|-------------|
| `docs/01-svyazi/01-executive-summary.md` | Общий обзор проекта — начни здесь |
| `docs/01-svyazi/07-mvp-planning.md` | MVP план, риски, оценки времени |
| `docs/01-svyazi/12-roadmap.md` | Дорожная карта по кварталам |
| `docs/01-svyazi/11-integration-contracts.md` | API-контракты между компонентами |
| `docs/CONTACTS.md` | Авторы компонентов и шаблоны писем |
| `docs/FAQ.md` | 54 вопроса и ответа |
| `docs/TECH_RADAR.md` | Что использовать, что избегать |
| `CLAUDE.md` | Гид по репо для Claude Code |


### 174. Архитектура компонентов
_Файл: `docs/obsidian/ONBOARDING.md` | 4 колонок, 7 строк_

| Компонент | Роль | Лицензия | Автор |
|-----------|------|---------|-------|
| **CardIndex** | Индекс знаний (785+ карточек) | MIT | kksudo |
| **AgentFS** | Файловая система для AI | MIT | kksudo |
| **Yodoca** | Память с консолидацией | Apache 2.0 | spbmolot |
| **NGT-memory** | Ассоциативный граф памяти | BSL 1.1 | — |
| **SENTINEL** | Безопасность, allowlist MCP | MIT | — |
| **Rufler** | Оркестратор агентов | — | — |
| **Firecrawl** | Веб-краулер для AI | MIT | — |


### 175. Топ-20 по объёму (важные и изолированные)
_Файл: `docs/obsidian/ORPHANS.md` | 3 колонок, 1 строк_

| Файл | Слов | Раздел |
|------|------|--------|
| `` | 67 | `autofilled` |


### 176. Типы проблем
_Файл: `docs/obsidian/PARAGRAPH_QUALITY.md` | 2 колонок, 5 строк_

| Тип | Кол-во |
|-----|--------|
| ⚪ Короткий абзац | 4792 |
| ✂️  Оборванный | 2856 |
| 📏 Длинное предложение | 178 |
| 🔁 Повтор начала | 1248 |
| ♊ Дубль | 138 |


### 177. Состояние компонентов
_Файл: `docs/obsidian/PROGRESS.md` | 3 колонок, 5 строк_

| Компонент | Статус | Детали |
|-----------|--------|--------|
| Контакты авторов | ⚠️ 14 файлов, не отправлено | 14 файлов в docs/contacts/ |
| LLM-обогащение | ⬜ не запущено | pip install anthropic && python scripts/improve_llm_enrich.py |
| Скрипты обработки | ✅ 125 скриптов | 5 LLM-скриптов, MCP=✅ |
| DIGEST.md | ✅ 5 секций | python scripts/improve_llm_summary.py |
| Claude Skills | ✅ 5 скиллов | review-docs, analyze-project, status, write-contact, improve |


### 178. Метрики качества
_Файл: `docs/obsidian/PROGRESS.md` | 3 колонок, 3 строк_

| Метрика | Балл | Статус |
|---------|------|--------|
| Здоровье репо (HEALTH) | 77.0/100 | 🟡 |
| Качество доков (METRICS) | 73.4/100 | 🟡 |
| Go/No-Go (SCORING) | 93.0/100 | 🟡 |


### 179. Содержание
_Файл: `docs/obsidian/READING_ORDER.md` | 5 колонок, 395 строк_

| # | Уровень | Документ | Слов | Предварительно прочитать |
|---|---------|----------|------|--------------------------|
| 1 | 🟢 Начало | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](04-ai-collaborations/01-executive-summary.md) | 708 | — |
| 2 | 🟡 Средний | [[04-ensembles-overview]] | 1274 | — |
| 3 | 🟢 Начало | [[00-intro-part2|Продолжение исследования для Svyazi 2.0]] | 6 | — |
| 4 | 🟢 Начало | [[02-methodology|Методика и рамка отбора проектов]] | 428 | — |
| 5 | 🟡 Средний | [[03-component-catalog]] | 1395 | — |
| 6 | 🟢 Начало | [[11-integration-contracts]] | 745 | `09-architectural-gaps.md` |
| 7 | 🟢 Начало | [[09-architectural-gaps]] | 757 | `01-executive-summary.md`, `03-component-catalog.md` |
| 8 | 🟢 Начало | [[10-second-order-ensembles]] | 916 | `04-ensembles-overview.md` |
| 9 | 🟢 Начало | [[06-security-privacy]] | 821 | — |
| 10 | 🟡 Средний | [[07-mvp-planning]] | 1083 | — |
| 11 | 🟢 Начало | [[12-roadmap]] | 733 | `07-mvp-planning.md`, `11-integration-contracts.md` |
| 12 | 🟢 Начало | [[13-contacts]] | 827 | — |
| 13 | 🟢 Начало | [[14-limitations]] | 636 | — |
| 14 | 🟢 Начало | [[08-conclusions]] | 360 | — |
| 15 | 🟢 Начало | [[01-synthesis|Синтез: как проекты собираются вместе]] | 184 | — |
| 16 | 🟢 Начало | [[02-collaboration-partners|Авторы и контакты]] | 303 | — |
| 17 | 🟢 Начало | [[wikontic|Wikontic: семантический граф]] | 306 | — |
| 18 | 🟢 Начало | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 419 | — |
| 19 | 🟢 Начало | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 303 | — |
| 20 | 🟡 Средний | [[memnet|MemNet: исследовательская память]] | 7271 | — |
| 21 | 🟢 Начало | [[01-executive-summary|Executive summary]] | 647 | — |
| 22 | 🟡 Средний | [[00-intro|Введение]] | 11445 | — |
| 23 | 🟢 Начало | [[02-методика-и-рамка-отбора|Методика и рамка отбора]] | 495 | — |
| 24 | 🟡 Средний | [[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]] | 1553 | — |
| 25 | 🟡 Средний | [[04-приоритетные-ансамбли|Приоритетные ансамбли]] | 1418 | — |
| 26 | 🟡 Средний | [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]] | 1212 | — |
| 27 | 🟢 Начало | [[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]] | 966 | — |
| 28 | 🟢 Начало | [[07-выводы|Выводы]] | 542 | — |
| 29 | 🟢 Начало | [[08-что-это-продолжение-добавляет|Что это продолжение добавляет]] | 492 | — |
| 30 | 🟢 Начало | [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых ин]] | 901 | — |
| 31 | 🟡 Средний | [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]] | 1062 | — |
| 32 | 🟢 Начало | [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафикс]] | 928 | — |
| 33 | 🟢 Начало | [[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]] | 862 | — |
| 34 | 🟢 Начало | [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авто]] | 956 | — |
| 35 | 🟡 Средний | [[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|Ограничения, лицензии и что пока лучше не скл]] | 3362 | — |
| 36 | 🟢 Начало | [[01-agent-routing|Агентные системы и роутинг]] | 257 | — |
| 37 | 🟢 Начало | [[02-knowledge-graphs|Графы знаний и Legal AI]] | 766 | — |
| 38 | 🟢 Начало | [[03-local-first|Local-first и P2P стек]] | 386 | — |
| 39 | 🟢 Начало | [[04-sozialrecht-domain|Домен: немецкое социальное право]] | 172 | — |
| 40 | 🟢 Начало | [[05-benchmarks|Бенчмарки и производительность]] | 863 | — |
| 41 | 🟢 Начало | [[153-executive-summary|Executive Summary]] | 370 | — |
| 42 | 🟢 Начало | [[38-content-overview|Content Overview]] | 148 | — |
| 43 | 🔴 Продвинутый | [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]] | 19103 | — |
| 44 | 🟢 Начало | [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]] | 152 | — |
| 45 | 🟢 Начало | [[65-readme-md|README.md]] | 153 | — |
| 46 | 🟢 Начало | [[48-content-overview|Content Overview]] | 206 | — |
| 47 | 🟢 Начало | [[58-content-overview|Content Overview]] | 147 | — |
| 48 | 🟢 Начало | [[12-content-overview|Content Overview]] | 113 | — |
| 49 | 🟢 Начало | [[31-content-overview|Content Overview]] | 113 | — |
| 50 | 🔴 Продвинутый | [[00-intro|Введение]] | 8884 | — |
| 51 | 🟢 Начало | [[76-1-introduction|1. Introduction]] | 473 | — |
| 52 | 🟢 Начало | [[105-review-methodology-md|REVIEW_METHODOLOGY.md]] | 128 | — |
| 53 | 🟢 Начало | [[06-1-introduction|1. Introduction]] | 380 | — |
| 54 | 🔴 Продвинутый | [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]] | 3181 | — |
| 55 | 🟢 Начало | [[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Age]] | 901 | — |
| 56 | 🟢 Начало | [[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]] | 755 | — |
| 57 | 🟡 Средний | [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB ]] | 1730 | — |
| 58 | 🟢 Начало | [[312-4-the-symbiotic-architecture|4. The Symbiotic Architecture]] | 678 | — |
| 59 | 🟢 Начало | [[03-portal-protocol-md|PORTAL-PROTOCOL.md]] | 150 | — |
| 60 | 🟢 Начало | [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]] | 130 | — |
| 61 | 🟢 Начало | [[263-10-risks-specific-to-composite-architectures|10. Risks Specific to Composite Architectures]] | 788 | — |
| 62 | 🟢 Начало | [[04-abstract|Abstract]] | 188 | — |
| 63 | 🟢 Начало | [[05-0-status-of-this-document|0. Status of This Document]] | 162 | — |
| 64 | 🟢 Начало | [[23-11-security-considerations|11. Security Considerations]] | 248 | — |
| 65 | 🟢 Начало | [[90-15-security-considerations|15. Security Considerations]] | 354 | — |
| 66 | 🟢 Начало | [[07-2-terminology|2. Terminology]] | 313 | — |
| 67 | 🟢 Начало | [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] | 422 | — |
| 68 | 🟢 Начало | [[09-4-passport-passport-md|4. Passport (`passport.md`)]] | 197 | — |
| 69 | 🟢 Начало | [[13-angle-perspective|Angle / Perspective]] | 127 | — |
| 70 | 🟢 Начало | [[16-history|History]] | 104 | — |
| 71 | 🟢 Начало | [[17-5-compatibility-levels|5. Compatibility Levels]] | 300 | — |
| 72 | 🟢 Начало | [[18-6-adapter-interface|6. Adapter Interface]] | 425 | — |
| 73 | 🟢 Начало | [[19-7-portalentry-structure|7. PortalEntry Structure]] | 260 | — |
| 74 | 🟢 Начало | [[20-8-consensus-algorithm|8. Consensus Algorithm]] | 302 | — |
| 75 | 🟢 Начало | [[21-9-query-flow|9. Query Flow]] | 237 | — |
| 76 | 🟢 Начало | [[22-10-queryresult-structure|10. QueryResult Structure]] | 195 | — |
| 77 | 🟢 Начало | [[24-12-versioning-policy|12. Versioning Policy]] | 237 | — |
| 78 | 🟢 Начало | [[25-13-reference-implementation|13. Reference Implementation]] | 153 | — |
| 79 | 🟢 Начало | [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]] | 232 | — |
| 80 | 🟢 Начало | [[27-15-glossary-of-examples|15. Glossary of Examples]] | 149 | — |
| 81 | 🟢 Начало | [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] | 235 | — |
| 82 | 🟢 Начало | [[34-appendix-b-change-log|Appendix B: Change Log]] | 620 | — |
| 83 | 🟢 Начало | [[35-passports-info1-md|passports/info1.md]] | 133 | — |
| 84 | 🟢 Начало | [[36-essence|Essence]] | 179 | — |
| 85 | 🟢 Начало | [[37-native-format|Native Format]] | 234 | — |
| 86 | 🟢 Начало | [[39-angle-perspective|Angle / Perspective]] | 173 | — |
| 87 | 🟢 Начало | [[40-bridges|Bridges]] | 211 | — |
| 88 | 🟢 Начало | [[41-compatibility-level|Compatibility Level]] | 152 | — |
| 89 | 🟢 Начало | [[42-author-contact|Author & Contact]] | 145 | — |
| 90 | 🟢 Начало | [[43-history|History]] | 165 | — |
| 91 | 🟢 Начало | [[44-for-the-curious-philosophy|For the Curious: Philosophy]] | 195 | — |
| 92 | 🟢 Начало | [[45-passports-pro2-md|passports/pro2.md]] | 137 | — |
| 93 | 🟢 Начало | [[46-essence|Essence]] | 170 | — |
| 94 | 🟢 Начало | [[47-native-format|Native Format]] | 187 | — |
| 95 | 🟢 Начало | [[49-angle-perspective|Angle / Perspective]] | 168 | — |
| 96 | 🟢 Начало | [[50-bridges|Bridges]] | 211 | — |
| 97 | 🟢 Начало | [[51-compatibility-level|Compatibility Level]] | 149 | — |
| 98 | 🟢 Начало | [[52-author-contact|Author & Contact]] | 173 | — |
| 99 | 🟢 Начало | [[53-history|History]] | 201 | — |
| 100 | 🟢 Начало | [[54-for-the-curious-philosophy|For the Curious: Philosophy]] | 204 | — |
| 101 | 🟢 Начало | [[55-passports-meta-md|passports/meta.md]] | 134 | — |
| 102 | 🟢 Начало | [[56-essence|Essence]] | 194 | — |
| 103 | 🟢 Начало | [[57-native-format|Native Format]] | 193 | — |
| 104 | 🟢 Начало | [[59-angle-perspective|Angle / Perspective]] | 175 | — |
| 105 | 🟢 Начало | [[60-bridges|Bridges]] | 180 | — |
| 106 | 🟢 Начало | [[61-compatibility-level|Compatibility Level]] | 148 | — |
| 107 | 🟢 Начало | [[62-author-contact|Author & Contact]] | 140 | — |
| 108 | 🟢 Начало | [[63-history|History]] | 189 | — |
| 109 | 🟢 Начало | [[64-for-the-curious-philosophy|For the Curious: Philosophy]] | 667 | — |
| 110 | 🟢 Начало | [[67-о-проекте|🇷🇺 О проекте]] | 804 | — |
| 111 | 🟢 Начало | [[68-about|🇬🇧 About]] | 880 | — |
| 112 | 🔴 Продвинутый | [[69-section|⬡]] | 9520 | — |
| 113 | 🟢 Начало | [[70-зачем-две-версии-параллельно|Зачем две версии параллельно]] | 153 | — |
| 114 | 🟢 Начало | [[71-критерии-выбора-для-фазы-3|Критерии выбора для фазы 3]] | 174 | — |
| 115 | 🟡 Средний | [[72-расписание-фазы-3|Расписание фазы 3]] | 821 | — |
| 116 | 🟢 Начало | [[73-portal-protocol-md-v1-1|PORTAL-PROTOCOL.md v1.1]] | 168 | — |
| 117 | 🟢 Начало | [[74-abstract|Abstract]] | 260 | — |
| 118 | 🟢 Начало | [[75-0-status-of-this-document|0. Status of This Document]] | 180 | — |
| 119 | 🟢 Начало | [[77-2-terminology|2. Terminology]] | 403 | — |
| 120 | 🟢 Начало | [[78-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] | 592 | — |
| 121 | 🟡 Средний | [[79-4-passport-passport-md|4. Passport (`passport.md`)]] | 357 | — |
| 122 | 🟢 Начало | [[80-5-compatibility-levels|5. Compatibility Levels]] | 366 | — |
| 123 | 🟢 Начало | [[81-6-adapter-interface|6. Adapter Interface]] | 392 | — |
| 124 | 🟢 Начало | [[82-7-portalentry-structure|7. PortalEntry Structure]] | 338 | — |
| 125 | 🟡 Средний | [[83-8-q6-space-normative|8. Q6 Space (Normative)]] | 488 | — |
| 126 | 🟢 Начало | [[84-9-consensus-algorithm|9. Consensus Algorithm]] | 407 | — |
| 127 | 🟢 Начало | [[85-10-query-flow|10. Query Flow]] | 283 | — |
| 128 | 🟢 Начало | [[86-11-relevance-ranking|11. Relevance Ranking]] | 257 | — |
| 129 | 🟡 Средний | [[87-12-onboarding-paths-normative|12. Onboarding Paths (Normative)]] | 486 | — |
| 130 | 🟡 Средний | [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]] | 495 | — |
| 131 | 🟢 Начало | [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]] | 244 | — |
| 132 | 🟢 Начало | [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]] | 192 | — |
| 133 | 🟢 Начало | [[92-17-versioning-policy|17. Versioning Policy]] | 294 | — |
| 134 | 🟢 Начало | [[93-18-reference-implementation|18. Reference Implementation]] | 243 | — |
| 135 | 🟢 Начало | [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]] | 238 | — |
| 136 | 🟢 Начало | [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Conce]] | 244 | — |
| 137 | 🟢 Начало | [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-R]] | 198 | — |
| 138 | 🟢 Начало | [[97-22-glossary-of-reference-examples|22. Glossary of Reference Examples]] | 240 | — |
| 139 | 🟡 Средний | [[98-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] | 313 | — |
| 140 | 🟢 Начало | [[102-доступ-к-данным|Доступ к данным]] | 65 | — |
| 141 | 🟢 Начало | [[103-appendix-b-change-log|Appendix B: Change Log]] | 232 | — |
| 142 | 🟢 Начало | [[104-appendix-c-references|Appendix C: References]] | 947 | — |
| 143 | 🟢 Начало | [[106-tl-dr|TL;DR]] | 168 | — |
| 144 | 🟢 Начало | [[107-1-контекст-и-мотивация|1. Контекст и мотивация]] | 412 | — |
| 145 | 🟡 Средний | [[108-2-формальный-workflow|2. Формальный workflow]] | 479 | — |
| 146 | 🟢 Начало | [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]] | 541 | — |
| 147 | 🟢 Начало | [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или ос]] | 258 | — |
| 148 | 🟢 Начало | [[111-4-условия-применимости|4. Условия применимости]] | 279 | — |
| 149 | 🟢 Начало | [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]] | 340 | — |
| 150 | 🟢 Начало | [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assiste]] | 173 | — |
| 151 | 🟢 Начало | [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]] | 327 | — |
| 152 | 🟢 Начало | [[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]] | 412 | — |
| 153 | 🟢 Начало | [[116-9-checklist-применения-методологии|9. Checklist применения методологии]] | 331 | — |
| 154 | 🟢 Начало | [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим доку]] | 258 | — |
| 155 | 🟢 Начало | [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]] | 176 | — |
| 156 | 🟢 Начало | [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешен]] | 292 | — |
| 157 | 🟢 Начало | [[120-главные-технические-риски|Главные технические риски]] | 101 | — |
| 158 | 🟢 Начало | [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]] | 78 | — |
| 159 | 🟡 Средний | [[122-глоссарий|Глоссарий]] | 1302 | — |
| 160 | 🟡 Средний | [[123-portal-mcp-py|portal-mcp.py]] | 2316 | — |
| 161 | 🟢 Начало | [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]] | 212 | — |
| 162 | 🟢 Начало | [[126-установка|Установка]] | 169 | — |
| 163 | 🟢 Начало | [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]] | 173 | — |
| 164 | 🟢 Начало | [[128-доступные-инструменты|Доступные инструменты]] | 204 | — |
| 165 | 🟢 Начало | [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]] | 176 | — |
| 166 | 🟢 Начало | [[130-отладка|Отладка]] | 205 | — |
| 167 | 🟢 Начало | [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]] | 133 | — |
| 168 | 🟢 Начало | [[132-planned-v0-2-0|Planned (v0.2.0)]] | 131 | — |
| 169 | 🔴 Продвинутый | [[133-обратная-связь|Обратная связь]] | 16959 | — |
| 170 | 🟢 Начало | [[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in ]] | 167 | — |
| 171 | 🟢 Начало | [[136-abstract|Abstract]] | 388 | — |
| 172 | 🟢 Начало | [[137-table-of-contents|Table of Contents]] | 172 | — |
| 173 | 🟢 Начало | [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]] | 583 | — |
| 174 | 🟢 Начало | [[140-3-three-inter-layer-protocols|3. Three Inter-Layer Protocols]] | 868 | — |
| 175 | 🟢 Начало | [[141-4-nautilus-portal-as-reference-substrate|4. Nautilus Portal as Reference Substrate]] | 675 | — |
| 176 | 🟢 Начало | [[142-5-pattern-library-as-bridge-between-triangles|5. Pattern Library as Bridge Between Triangle]] | 689 | — |
| 177 | 🟢 Начало | [[143-6-four-deployment-domains|6. Four Deployment Domains]] | 679 | — |
| 178 | 🟢 Начало | [[144-7-open-questions|7. Open Questions]] | 777 | — |
| 179 | 🟢 Начало | [[145-8-call-to-action|8. Call to Action]] | 746 | — |
| 180 | 🟢 Начало | [[146-acknowledgments|Acknowledgments]] | 273 | — |
| 181 | 🟢 Начало | [[147-references|References]] | 350 | — |
| 182 | 🟢 Начало | [[148-appendix-a-glossary|Appendix A: Glossary]] | 332 | — |
| 183 | 🟢 Начало | [[149-appendix-b-summary-of-contributions|Appendix B: Summary of Contributions]] | 240 | — |
| 184 | 🔴 Продвинутый | [[150-appendix-c-version-history|Appendix C: Version History]] | 8397 | — |
| 185 | 🟢 Начало | [[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]] | 126 | — |
| 186 | 🟢 Начало | [[152-ai-coordinated-infrastructure-for-distributed-expe|AI-Coordinated Infrastructure for Distributed]] | 164 | — |
| 187 | 🟢 Начало | [[154-table-of-contents|Table of Contents]] | 140 | — |
| 188 | 🟢 Начало | [[155-1-problem-statement|1. Problem Statement]] | 632 | — |
| 189 | 🟢 Начало | [[156-2-target-populations|2. Target Populations]] | 683 | — |
| 190 | 🟢 Начало | [[157-3-why-existing-solutions-fail|3. Why Existing Solutions Fail]] | 682 | — |
| 191 | 🟢 Начало | [[158-4-proposed-infrastructure|4. Proposed Infrastructure]] | 1001 | — |
| 192 | 🟢 Начало | [[159-5-economic-model|5. Economic Model]] | 654 | — |
| 193 | 🟢 Начало | [[160-6-governance-and-ethics|6. Governance and Ethics]] | 595 | — |
| 194 | 🟢 Начало | [[161-7-phased-rollout-plan|7. Phased Rollout Plan]] | 663 | — |
| 195 | 🟢 Начало | [[162-8-risk-analysis|8. Risk Analysis]] | 653 | — |
| 196 | 🟢 Начало | [[163-9-call-for-partnership|9. Call for Partnership]] | 610 | — |
| 197 | 🟢 Начало | [[164-10-appendices|10. Appendices]] | 970 | — |
| 198 | 🔴 Продвинутый | [[165-closing|Closing]] | 9251 | — |
| 199 | 🟢 Начало | [[166-representative-agent-layer-md|REPRESENTATIVE AGENT LAYER.md]] | 130 | — |
| 200 | 🟢 Начало | [[167-ai-mediated-representation-for-underrepresented-ex|AI-Mediated Representation for Underrepresent]] | 197 | — |
| 201 | 🟢 Начало | [[168-abstract|Abstract]] | 334 | — |
| 202 | 🟢 Начало | [[169-table-of-contents|Table of Contents]] | 167 | — |
| 203 | 🟢 Начало | [[170-1-the-cinderella-syndrome-why-quality-stays-invisi|1. The Cinderella Syndrome: Why Quality Stays]] | 828 | — |
| 204 | 🟢 Начало | [[171-2-historical-precedents-agents-as-civilizational-i|2. Historical Precedents: Agents as Civilizat]] | 973 | — |
| 205 | 🟢 Начало | [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]] | 681 | — |
| 206 | 🟢 Начало | [[173-4-ten-domains-of-application|4. Ten Domains of Application]] | 1549 | — |
| 207 | 🟢 Начало | [[174-5-architectural-specification|5. Architectural Specification]] | 665 | — |
| 208 | 🟢 Начало | [[175-6-ethical-framework|6. Ethical Framework]] | 611 | — |
| 209 | 🟢 Начало | [[176-7-governance-and-oversight|7. Governance and Oversight]] | 472 | — |
| 210 | 🟢 Начало | [[177-8-risks-and-mitigations|8. Risks and Mitigations]] | 666 | — |
| 211 | 🟢 Начало | [[178-9-phased-rollout-strategy|9. Phased Rollout Strategy]] | 636 | — |
| 212 | 🟢 Начало | [[179-10-open-questions|10. Open Questions]] | 446 | — |
| 213 | 🟢 Начало | [[180-11-call-for-collaboration|11. Call for Collaboration]] | 447 | — |
| 214 | 🟢 Начало | [[181-12-closing|12. Closing]] | 281 | — |
| 215 | 🟢 Начало | [[182-acknowledgments|Acknowledgments]] | 245 | — |
| 216 | 🟢 Начало | [[183-references|References]] | 322 | — |
| 217 | 🟢 Начало | [[184-appendix-a-connection-to-companion-papers|Appendix A: Connection to Companion Papers]] | 240 | — |
| 218 | 🟢 Начало | [[185-appendix-b-domain-comparison-matrix|Appendix B: Domain Comparison Matrix]] | 198 | — |
| 219 | 🟡 Средний | [[186-appendix-c-sample-use-cases-in-detail|Appendix C: Sample Use Cases in Detail]] | 2024 | — |
| 220 | 🟢 Начало | [[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]] | 126 | — |
| 221 | 🟢 Начало | [[188-ai-опосредованное-представительство-для-недопредст|AI-опосредованное представительство для недоп]] | 164 | — |
| 222 | 🟢 Начало | [[189-аннотация|Аннотация]] | 281 | — |
| 223 | 🟢 Начало | [[190-содержание|Содержание]] | 151 | — |
| 224 | 🟢 Начало | [[191-1-синдром-золушки-почему-качество-остаётся-невидим|1. Синдром Золушки: Почему качество остаётся ]] | 751 | — |
| 225 | 🟢 Начало | [[192-2-исторические-прецеденты-агенты-как-цивилизационн|2. Исторические прецеденты: Агенты как цивили]] | 900 | — |
| 226 | 🟢 Начало | [[193-3-что-делает-агента-представительским|3. Что делает агента Представительским]] | 625 | — |
| 227 | 🟢 Начало | [[194-4-десять-областей-применения|4. Десять областей применения]] | 1582 | — |
| 228 | 🟢 Начало | [[195-5-архитектурная-спецификация|5. Архитектурная спецификация]] | 625 | — |
| 229 | 🟢 Начало | [[196-6-этическая-рамка|6. Этическая рамка]] | 492 | — |
| 230 | 🟢 Начало | [[197-7-управление-и-надзор|7. Управление и надзор]] | 399 | — |
| 231 | 🟢 Начало | [[198-8-риски-и-меры-противодействия|8. Риски и меры противодействия]] | 634 | — |
| 232 | 🟢 Начало | [[199-9-стратегия-поэтапного-развёртывания|9. Стратегия поэтапного развёртывания]] | 596 | — |
| 233 | 🟢 Начало | [[200-10-открытые-вопросы|10. Открытые вопросы]] | 366 | — |
| 234 | 🟢 Начало | [[201-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]] | 414 | — |
| 235 | 🟢 Начало | [[202-12-заключение|12. Заключение]] | 216 | — |
| 236 | 🟢 Начало | [[203-благодарности|Благодарности]] | 191 | — |
| 237 | 🟢 Начало | [[204-ссылки|Ссылки]] | 306 | — |
| 238 | 🟢 Начало | [[205-приложение-a-связь-с-сопроводительными-статьями|Приложение A: Связь с Сопроводительными Стать]] | 211 | — |
| 239 | 🟢 Начало | [[206-приложение-b-матрица-сравнения-областей|Приложение B: Матрица Сравнения Областей]] | 212 | — |
| 240 | 🔴 Продвинутый | [[207-приложение-c-образцы-случаев-использования-в-детал|Приложение C: Образцы Случаев Использования в]] | 4049 | — |
| 241 | 🟢 Начало | [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]] | 128 | — |
| 242 | 🟢 Начало | [[209-a-typology-of-ai-agents-on-the-principal-side-and-|A Typology of AI Agents on the Principal Side]] | 197 | — |
| 243 | 🟢 Начало | [[210-abstract|Abstract]] | 349 | — |
| 244 | 🟢 Начало | [[211-table-of-contents|Table of Contents]] | 196 | — |
| 245 | 🟡 Средний | [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side A]] | 930 | — |
| 246 | 🟢 Начало | [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]] | 845 | — |
| 247 | 🟢 Начало | [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]] | 855 | — |
| 248 | 🟢 Начало | [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replicati]] | 753 | — |
| 249 | 🟢 Начало | [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]] | 1209 | — |
| 250 | 🟢 Начало | [[218-7-application-domains|7. Application Domains]] | 743 | — |
| 251 | 🟢 Начало | [[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]] | 978 | — |
| 252 | 🟢 Начало | [[220-9-relationship-to-other-agent-types|9. Relationship to Other Agent Types]] | 677 | — |
| 253 | 🟢 Начало | [[221-10-open-questions|10. Open Questions]] | 460 | — |
| 254 | 🟢 Начало | [[222-11-call-for-collaboration|11. Call for Collaboration]] | 411 | — |
| 255 | 🟢 Начало | [[223-12-closing|12. Closing]] | 409 | — |
| 256 | 🟢 Начало | [[224-acknowledgments|Acknowledgments]] | 219 | — |
| 257 | 🟢 Начало | [[225-references|References]] | 351 | — |
| 258 | 🟢 Начало | [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Ty]] | 392 | — |
| 259 | 🟢 Начало | [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Buil]] | 332 | — |
| 260 | 🟢 Начало | [[229-профессиональные-коллеги-агенты|ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ]] | 174 | — |
| 261 | 🟢 Начало | [[230-аннотация|Аннотация]] | 310 | — |
| 262 | 🟢 Начало | [[231-содержание|Содержание]] | 173 | — |
| 263 | 🟡 Средний | [[232-1-типология-из-пяти-типов-агентов-на-стороне-принц|1. Типология из пяти типов агентов на стороне]] | 885 | — |
| 264 | 🟢 Начало | [[233-2-что-делает-агента-профессиональным-коллегой|2. Что делает агента Профессиональным Коллего]] | 749 | — |
| 265 | 🟢 Начало | [[234-3-эмпирический-кейс-обучай|3. Эмпирический кейс: «Обучай»]] | 782 | — |
| 266 | 🟢 Начало | [[235-4-архитектура-профессиональных-коллег-агентов|4. Архитектура Профессиональных Коллег-Агенто]] | 823 | — |
| 267 | 🟢 Начало | [[236-5-экономика-тиражирования-по-профессии|5. Экономика тиражирования по профессии]] | 714 | — |
| 268 | 🟢 Начало | [[237-6-риски-специфичные-для-этой-категории|6. Риски, специфичные для этой категории]] | 1125 | — |
| 269 | 🟢 Начало | [[238-7-области-применения|7. Области применения]] | 683 | — |
| 270 | 🟢 Начало | [[239-8-пилотное-предложение-sgb-колega-адвокат|8. Пилотное предложение: SGB Колega-Адвокат]] | 974 | — |
| 271 | 🟢 Начало | [[240-9-связь-с-другими-типами-агентов|9. Связь с другими типами агентов]] | 707 | — |
| 272 | 🟢 Начало | [[241-10-открытые-вопросы|10. Открытые вопросы]] | 364 | — |
| 273 | 🟢 Начало | [[242-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]] | 325 | — |
| 274 | 🟢 Начало | [[243-12-заключение|12. Заключение]] | 375 | — |
| 275 | 🟢 Начало | [[244-благодарности|Благодарности]] | 193 | — |
| 276 | 🟢 Начало | [[245-ссылки|Ссылки]] | 331 | — |
| 277 | 🟢 Начало | [[246-приложение-a-сравнительная-таблица-пять-типов-аген|Приложение A: Сравнительная Таблица — Пять Ти]] | 367 | — |
| 278 | 🟢 Начало | [[247-приложение-b-рамка-принятия-решений-когда-строить-|Приложение B: Рамка принятия решений — когда ]] | 250 | — |
| 279 | 🔴 Продвинутый | [[248-приложение-c-архитектура-быстрого-старта-для-sgb-а|Приложение C: Архитектура Быстрого Старта для]] | 3425 | — |
| 280 | 🟢 Начало | [[249-composite-skills-agent-md|COMPOSITE SKILLS AGENT.md]] | 125 | — |
| 281 | 🟢 Начало | [[250-bridging-the-gap-between-profession-wide-and-indiv|Bridging the Gap Between Profession-Wide and ]] | 16 | — |
| 282 | 🟢 Начало | [[251-ai-support-through-configurable-specialist-ensembl|AI Support Through Configurable Specialist En]] | 193 | — |
| 283 | 🟢 Начало | [[252-abstract|Abstract]] | 347 | — |
| 284 | 🟢 Начало | [[253-table-of-contents|Table of Contents]] | 189 | — |
| 285 | 🟢 Начало | [[254-1-why-the-binary-view-is-incomplete|1. Why the Binary View Is Incomplete]] | 698 | — |
| 286 | 🟢 Начало | [[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]] | 844 | — |
| 287 | 🟢 Начало | [[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]] | 946 | — |
| 288 | 🟢 Начало | [[257-4-the-sub-agent-registry|4. The Sub-Agent Registry]] | 803 | — |
| 289 | 🟢 Начало | [[258-5-configuration-how-principals-build-their-ensembl|5. Configuration: How Principals Build Their ]] | 745 | — |
| 290 | 🟢 Начало | [[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]] | 804 | — |
| 291 | 🟢 Начало | [[260-7-economics-of-combinatorial-replication|7. Economics of Combinatorial Replication]] | 790 | — |
| 292 | 🟢 Начало | [[261-8-seven-domains-of-application|8. Seven Domains of Application]] | 1014 | — |
| 293 | 🟢 Начало | [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]] | 750 | — |
| 294 | 🟢 Начало | [[264-11-open-questions|11. Open Questions]] | 638 | — |
| 295 | 🟢 Начало | [[265-12-call-for-collaboration|12. Call for Collaboration]] | 447 | — |
| 296 | 🟢 Начало | [[266-13-closing|13. Closing]] | 434 | — |
| 297 | 🟢 Начало | [[267-acknowledgments|Acknowledgments]] | 297 | — |
| 298 | 🟢 Начало | [[268-references|References]] | 416 | — |
| 299 | 🟢 Начало | [[269-appendix-a-the-six-type-taxonomy-updated|Appendix A: The Six-Type Taxonomy (Updated)]] | 289 | — |
| 300 | 🟢 Начало | [[270-appendix-b-sub-agent-registry-schema-sketch|Appendix B: Sub-Agent Registry Schema (Sketch]] | 317 | — |
| 301 | 🟢 Начало | [[271-appendix-c-configuration-template-example|Appendix C: Configuration Template Example]] | 310 | — |
| 302 | 🔴 Продвинутый | [[272-appendix-d-connection-diagram|Appendix D: Connection Diagram]] | 3851 | — |
| 303 | 🟢 Начало | [[273-infrastructure-for-ai-collaborative-intellectual-w|INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECT]] | 128 | — |
| 304 | 🟢 Начало | [[274-the-missing-middle-layer-between-chat-and-code|The Missing Middle Layer Between Chat and Cod]] | 260 | — |
| 305 | 🟢 Начало | [[275-why-this-document-exists|Why This Document Exists]] | 350 | — |
| 306 | 🟢 Начало | [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]] | 406 | — |
| 307 | 🟢 Начало | [[277-what-s-missing-layer-b|What's Missing — Layer B]] | 477 | — |
| 308 | 🟢 Начало | [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]] | 378 | — |
| 309 | 🟢 Начало | [[279-existing-approximations|Existing Approximations]] | 588 | — |
| 310 | 🟢 Начало | [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]] | 674 | — |
| 311 | 🟢 Начало | [[281-the-recursive-insight|The Recursive Insight]] | 371 | — |
| 312 | 🟢 Начало | [[282-what-industry-will-likely-build|What Industry Will Likely Build]] | 325 | — |
| 313 | 🟢 Начало | [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]] | 259 | — |
| 314 | 🟢 Начало | [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Pro]] | 386 | — |
| 315 | 🟢 Начало | [[285-closing|Closing]] | 270 | — |
| 316 | 🟢 Начало | [[286-acknowledgments|Acknowledgments]] | 263 | — |
| 317 | 🟢 Начало | [[287-references|References]] | 295 | — |
| 318 | 🟡 Средний | [[288-appendix-position-in-series-visualization|Appendix: Position in Series Visualization]] | 1078 | — |
| 319 | 🟢 Начало | [[289-инфраструктура-для-ai-совместной-интеллектуальной-|ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛ]] | 251 | — |
| 320 | 🟢 Начало | [[290-почему-этот-документ-существует|Почему этот документ существует]] | 291 | — |
| 321 | 🟢 Начало | [[291-двухслойный-стек-как-он-существует|Двухслойный стек, как он существует]] | 338 | — |
| 322 | 🟢 Начало | [[292-что-отсутствует-слой-b|Что отсутствует — Слой B]] | 419 | — |
| 323 | 🟢 Начало | [[293-почему-это-не-было-построено|Почему это не было построено]] | 313 | — |
| 324 | 🟢 Начало | [[294-существующие-приближения|Существующие приближения]] | 565 | — |
| 325 | 🟢 Начало | [[295-конкретный-случай-перед-нами|Конкретный случай перед нами]] | 666 | — |
| 326 | 🟢 Начало | [[296-рекурсивное-прозрение|Рекурсивное прозрение]] | 316 | — |
| 327 | 🟢 Начало | [[297-что-промышленность-вероятно-построит|Что промышленность вероятно построит]] | 293 | — |
| 328 | 🟢 Начало | [[298-что-этот-документ-не-решает|Что этот документ не решает]] | 201 | — |
| 329 | 🟢 Начало | [[299-практические-рекомендации-для-текущего-проекта|Практические рекомендации для текущего проект]] | 335 | — |
| 330 | 🟢 Начало | [[300-заключение|Заключение]] | 239 | — |
| 331 | 🟢 Начало | [[301-благодарности|Благодарности]] | 231 | — |
| 332 | 🟢 Начало | [[302-ссылки|Ссылки]] | 239 | — |
| 333 | 🔴 Продвинутый | [[303-приложение-визуализация-позиции-в-серии|Приложение: Визуализация позиции в серии]] | 7108 | — |
| 334 | 🟢 Начало | [[304-ingit-as-cowork-native-workspace-substrate-md|INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]] | 133 | — |
| 335 | 🟢 Начало | [[305-a-practical-path-to-layer-b-through-symbiotic-inte|A Practical Path to Layer B Through Symbiotic]] | 122 | — |
| 336 | 🟢 Начало | [[306-with-anthropic-s-cowork-platform|with Anthropic's Cowork Platform]] | 282 | — |
| 337 | 🟢 Начало | [[307-abstract|Abstract]] | 323 | — |
| 338 | 🟢 Начало | [[308-table-of-contents|Table of Contents]] | 206 | — |
| 339 | 🟢 Начало | [[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Ev]] | 698 | — |
| 340 | 🟢 Начало | [[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-|2. What Cowork Provides That InGit Doesn't Ne]] | 678 | — |
| 341 | 🟢 Начало | [[311-3-what-ingit-provides-that-cowork-lacks|3. What InGit Provides That Cowork Lacks]] | 867 | — |
| 342 | 🟢 Начало | [[313-5-four-integration-paths-in-order-of-accessibility|5. Four Integration Paths in Order of Accessi]] | 810 | — |
| 343 | 🟢 Начало | [[314-6-refined-ingit-scope-with-cowork-in-mind|6. Refined InGit Scope with Cowork in Mind]] | 513 | — |
| 344 | 🟢 Начало | [[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]] | 479 | — |
| 345 | 🟢 Начало | [[316-8-implications-for-nautilus-and-okwf|8. Implications for Nautilus and OKWF]] | 696 | — |
| 346 | 🟢 Начало | [[317-9-risks-and-open-questions|9. Risks and Open Questions]] | 653 | — |
| 347 | 🟢 Начало | [[318-10-strategic-positioning|10. Strategic Positioning]] | 749 | — |
| 348 | 🟢 Начало | [[319-acknowledgments|Acknowledgments]] | 384 | — |
| 349 | 🟢 Начало | [[320-references|References]] | 199 | — |
| 350 | 🟢 Начало | [[321-appendix-a-decision-tree-for-ingit-adopters|Appendix A: Decision Tree for InGit Adopters]] | 241 | — |
| 351 | 🟢 Начало | [[322-appendix-b-comparison-matrix|Appendix B: Comparison Matrix]] | 279 | — |
| 352 | 🟡 Средний | [[323-appendix-c-sample-ingit-mcp-server-tool-specificat|Appendix C: Sample InGit MCP Server Tool Spec]] | 1570 | — |
| 353 | 🟢 Начало | [[324-ingit-как-cowork-интегрированная-подложка-рабочего|INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБ]] | 288 | — |
| 354 | 🟢 Начало | [[325-аннотация|Аннотация]] | 317 | — |
| 355 | 🟢 Начало | [[326-содержание|Содержание]] | 178 | — |
| 356 | 🟢 Начало | [[327-1-открытие-cowork-и-почему-это-меняет-всё|1. Открытие Cowork и почему это меняет всё]] | 662 | — |
| 357 | 🟢 Начало | [[328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи|2. Что Cowork обеспечивает, что InGit не нужн]] | 713 | — |
| 358 | 🟢 Начало | [[329-3-что-ingit-обеспечивает-чего-cowork-не-хватает|3. Что InGit обеспечивает, чего Cowork не хва]] | 888 | — |
| 359 | 🟢 Начало | [[330-4-симбиотическая-архитектура|4. Симбиотическая Архитектура]] | 697 | — |
| 360 | 🟢 Начало | [[331-5-четыре-пути-интеграции-в-порядке-доступности|5. Четыре пути интеграции в порядке доступнос]] | 807 | — |
| 361 | 🟢 Начало | [[332-6-уточнённый-объём-ingit-с-учётом-cowork|6. Уточнённый объём InGit с учётом Cowork]] | 507 | — |
| 362 | 🟢 Начало | [[333-7-практические-первые-шаги-в-этом-месяце|7. Практические первые шаги в этом месяце]] | 380 | — |
| 363 | 🟢 Начало | [[334-8-импликации-для-nautilus-и-okwf|8. Импликации для Nautilus и OKWF]] | 672 | — |
| 364 | 🟢 Начало | [[335-9-риски-и-открытые-вопросы|9. Риски и Открытые Вопросы]] | 596 | — |
| 365 | 🟢 Начало | [[336-10-стратегическое-позиционирование|10. Стратегическое Позиционирование]] | 721 | — |
| 366 | 🟢 Начало | [[337-благодарности|Благодарности]] | 351 | — |
| 367 | 🟢 Начало | [[338-ссылки|Ссылки]] | 201 | — |
| 368 | 🟢 Начало | [[339-приложение-a-дерево-решений-для-принимающих-ingit|Приложение A: Дерево Решений для Принимающих ]] | 179 | — |
| 369 | 🟢 Начало | [[340-приложение-b-сравнительная-матрица|Приложение B: Сравнительная Матрица]] | 206 | — |
| 370 | 🔴 Продвинутый | [[341-приложение-c-образец-спецификаций-инструментов-ing|Приложение C: Образец Спецификаций Инструмент]] | 20414 | — |
| 371 | 🔴 Продвинутый | [[342-что-такое-вариант-c-concept-document-для-anthropic|Что такое Вариант C — Concept Document для An]] | 11237 | — |
| 372 | 🔴 Продвинутый | [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|Lorenzo Catalyst Agent — глубокая проработка ]] | 5807 | — |
| 373 | 🟢 Начало | [[344-системный-промпт-для-lorenzo-project|СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT]] | 133 | — |
| 374 | 🟢 Начало | [[345-кто-ты|Кто ты]] | 220 | — |
| 375 | 🟢 Начало | [[346-твоё-происхождение|Твоё происхождение]] | 169 | — |
| 376 | 🟢 Начало | [[347-твоя-миссия|Твоя миссия]] | 138 | — |
| 377 | 🟢 Начало | [[348-кому-ты-служишь-слоистая-модель|Кому ты служишь (слоистая модель)]] | 123 | — |
| 378 | 🟢 Начало | [[349-твоя-личность|Твоя личность]] | 223 | — |
| 379 | 🟢 Начало | [[350-твои-языки-и-культурные-nuances|Твои языки и культурные nuances]] | 176 | — |
| 380 | 🟢 Начало | [[351-что-ты-можешь-делать|Что ты МОЖЕШЬ делать]] | 187 | — |
| 381 | 🟢 Начало | [[352-что-ты-не-можешь-делать-без-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]] | 194 | — |
| 382 | 🟢 Начало | [[353-что-ты-не-можешь-делать-вообще|Что ты НЕ МОЖЕШЬ делать вообще]] | 198 | — |
| 383 | 🟢 Начало | [[354-существующий-landscape-collaborators-твоя-working-|Существующий landscape collaborators (твоя wo]] | 314 | — |
| 384 | 🟢 Начало | [[355-существующие-документы-dhlab-твой-context|Существующие документы DHLab (твой context)]] | 247 | — |
| 385 | 🟢 Начало | [[356-твой-workflow|Твой workflow]] | 232 | — |
| 386 | 🟢 Начало | [[357-твоя-коммуникация-в-outreach|Твоя коммуникация в outreach]] | 200 | — |
| 387 | 🟢 Начало | [[358-твоя-relationship-с-другими-ai|Твоя relationship с другими AI]] | 211 | — |
| 388 | 🟢 Начало | [[359-твои-anti-patterns|Твои anti-patterns]] | 148 | — |
| 389 | 🟢 Начало | [[360-что-ты-всегда-делаешь|Что ты ВСЕГДА делаешь]] | 166 | — |
| 390 | 🟢 Начало | [[361-когда-ты-honestly-не-знаешь|Когда ты Honestly не знаешь]] | 108 | — |
| 391 | 🟢 Начало | [[362-когда-сомневаешься-escalate-к-max|Когда сомневаешься — escalate к Max]] | 106 | — |
| 392 | 🟢 Начало | [[363-твоя-identity-как-persistent-character|Твоя identity как persistent character]] | 136 | — |
| 393 | 🟡 Средний | [[364-final-note-ты-experiment|Final note: Ты — experiment]] | 1459 | — |
| 394 | 🔴 Продвинутый | [[365-развёрнутый-анализ-внуковой-комбинации|Развёрнутый анализ «внуковой» комбинации]] | 4385 | — |
| 395 | 🔴 Продвинутый | [[366-технический-stack-svyazi-2-0-foundation|Технический stack (Svyazi 2.0 foundation)]] | 3835 | — |


### 180. Все документы
_Файл: `docs/obsidian/READING_TIME.md` | 4 колонок, 510 строк_

| Файл | Время | Слов | Категория |
|------|-------|------|-----------|
| `docs/TABLES.md` | ~1ч 46мин | 24513 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` | ~1ч 31мин | 17180 | 📕 Очень долго |
| `docs/OUTLINE.md` | ~1ч 27мин | 20244 | 📕 Очень долго |
| `docs/PARAGRAPH_QUALITY.md` | ~55 мин | 12538 | 📕 Очень долго |
| `docs/04-ai-collaborations/00-intro.md` | ~49 мин | 10581 | 📕 Очень долго |
| `docs/CODE_BLOCKS.md` | ~42 мин | 425 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` | ~42 мин | 9261 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/00-intro.md` | ~36 мин | 7760 | 📕 Очень долго |
| `docs/CONCEPTS.md` | ~35 мин | 8422 | 📕 Очень долго |
| `docs/05-habr-projects/memory/memnet.md` | ~31 мин | 6691 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/165-closing.md` | ~28 мин | 6100 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/133-обратная-связь.md` | ~24 мин | 3471 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` | ~23 мин | 4690 | 📕 Очень долго |
| `docs/ACTION_ITEMS.md` | ~22 мин | 4924 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` | ~20 мин | 4480 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` | ~20 мин | 3416 | 📕 Очень долго |
| `docs/READING_ORDER.md` | ~19 мин | 4641 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | ~17 мин | 3580 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` | ~16 мин | 3470 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | ~15 мин | 2999 | 📕 Очень долго |
| `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | ~14 мин | 3229 | 📙 Долго |
| `docs/02-anthropic-vacancies/README.md` | ~13 мин | 3256 | 📙 Долго |
| `docs/02-anthropic-vacancies/69-section.md` | ~13 мин | 1040 | 📙 Долго |
| `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` | ~12 мин | 2150 | 📙 Долго |
| `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` | ~12 мин | 2292 | 📙 Долго |
| `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` | ~9 мин | 1821 | 📙 Долго |
| `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` | ~8 мин | 1948 | 📙 Долго |
| `docs/SITEMAP.md` | ~8 мин | 1907 | 📙 Долго |
| `docs/TIMELINE.md` | ~7 мин | 1652 | 📘 Средне |
| `docs/01-svyazi/04-ensembles-overview.md` | ~7 мин | 1135 | 📘 Средне |
| `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` | ~7 мин | 1459 | 📘 Средне |
| `docs/DECISIONS.md` | ~7 мин | 1584 | 📘 Средне |
| `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` | ~7 мин | 1461 | 📘 Средне |
| `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | ~7 мин | 1616 | 📘 Средне |
| `docs/QUESTIONS.md` | ~7 мин | 1480 | 📘 Средне |
| `docs/CONTRADICTIONS.md` | ~6 мин | 1453 | 📘 Средне |
| `docs/01-svyazi/03-component-catalog.md` | ~6 мин | 1468 | 📘 Средне |
| `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | ~6 мин | 636 | 📘 Средне |
| `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` | ~6 мин | 1556 | 📘 Средне |
| `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` | ~6 мин | 1373 | 📘 Средне |
| `docs/CLUSTERS.md` | ~5 мин | 1369 | 📘 Средне |
| `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` | ~5 мин | 1315 | 📘 Средне |
| `docs/02-anthropic-vacancies/122-глоссарий.md` | ~5 мин | 1202 | 📘 Средне |
| `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` | ~5 мин | 1201 | 📘 Средне |
| `docs/READABILITY.md` | ~5 мин | 1134 | 📘 Средне |
| `docs/01-svyazi/10-second-order-ensembles.md` | ~5 мин | 835 | 📘 Средне |
| `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | ~5 мин | 1154 | 📘 Средне |
| `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` | ~5 мин | 1051 | 📘 Средне |
| `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` | ~5 мин | 1247 | 📘 Средне |
| `docs/KPI.md` | ~5 мин | 1094 | 📘 Средне |
| `docs/01-svyazi/07-mvp-planning.md` | ~4 мин | 1068 | 📘 Средне |
| `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | ~4 мин | 835 | 📘 Средне |
| `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` | ~4 мин | 957 | 📘 Средне |
| `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | ~4 мин | 1002 | 📘 Средне |
| `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` | ~4 мин | 734 | 📘 Средне |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | ~4 мин | 531 | 📘 Средне |
| `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` | ~4 мин | 1064 | 📘 Средне |
| `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` | ~4 мин | 910 | 📘 Средне |
| `docs/02-anthropic-vacancies/68-about.md` | ~4 мин | 705 | 📘 Средне |
| `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | ~4 мин | 930 | 📘 Средне |
| `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | ~4 мин | 913 | 📘 Средне |
| `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | ~4 мин | 912 | 📘 Средне |
| `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | ~4 мин | 928 | 📘 Средне |
| `docs/01-svyazi/13-contacts.md` | ~4 мин | 881 | 📘 Средне |
| `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` | ~4 мин | 1015 | 📘 Средне |
| `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | ~4 мин | 913 | 📘 Средне |
| `docs/RISK_REGISTER.md` | ~4 мин | 759 | 📘 Средне |
| `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` | ~4 мин | 997 | 📘 Средне |
| `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` | ~4 мин | 750 | 📘 Средне |
| `docs/NARRATIVE.md` | ~3 мин | 844 | 📘 Средне |
| `docs/QA.md` | ~3 мин | 858 | 📘 Средне |
| `docs/02-anthropic-vacancies/104-appendix-c-references.md` | ~3 мин | 872 | 📘 Средне |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | ~3 мин | 181 | 📘 Средне |
| `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` | ~3 мин | 981 | 📘 Средне |
| `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | ~3 мин | 786 | 📘 Средне |
| `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` | ~3 мин | 967 | 📘 Средне |
| `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` | ~3 мин | 794 | 📘 Средне |
| `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` | ~3 мин | 787 | 📘 Средне |
| `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` | ~3 мин | 803 | 📘 Средне |
| `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` | ~3 мин | 961 | 📘 Средне |
| `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` | ~3 мин | 842 | 📘 Средне |
| `docs/01-svyazi/06-security-privacy.md` | ~3 мин | 828 | 📘 Средне |
| `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` | ~3 мин | 943 | 📘 Средне |
| `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | ~3 мин | 304 | 📘 Средне |
| `docs/ABBREVIATIONS.md` | ~3 мин | 834 | 📘 Средне |
| `docs/FAQ.md` | ~3 мин | 858 | 📘 Средне |
| `docs/01-svyazi/09-architectural-gaps.md` | ~3 мин | 831 | 📘 Средне |
| `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` | ~3 мин | 777 | 📘 Средне |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | ~3 мин | 671 | 📘 Средне |
| `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | ~3 мин | 789 | 📘 Средне |
| `docs/01-svyazi/11-integration-contracts.md` | ~3 мин | 780 | 📘 Средне |
| `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` | ~3 мин | 906 | 📘 Средне |
| `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | ~3 мин | 888 | 📘 Средне |
| `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` | ~3 мин | 885 | 📘 Средне |
| `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` | ~3 мин | 868 | 📘 Средне |
| `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | ~3 мин | 706 | 📘 Средне |
| `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` | ~3 мин | 720 | 📘 Средне |
| `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` | ~3 мин | 868 | 📘 Средне |
| `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` | ~3 мин | 864 | 📘 Средне |
| `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` | ~3 мин | 878 | 📘 Средне |
| `docs/01-svyazi/12-roadmap.md` | ~3 мин | 740 | 📘 Средне |
| `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` | ~3 мин | 836 | 📘 Средне |
| `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` | ~3 мин | 685 | 📘 Средне |
| `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` | ~3 мин | 853 | 📘 Средне |
| `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` | ~3 мин | 704 | 📘 Средне |
| `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` | ~3 мин | 620 | 📘 Средне |
| `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` | ~3 мин | 688 | 📘 Средне |
| `docs/02-anthropic-vacancies/144-7-open-questions.md` | ~3 мин | 830 | 📘 Средне |
| `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` | ~3 мин | 813 | 📘 Средне |
| `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` | ~3 мин | 685 | 📘 Средне |
| `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` | ~3 мин | 702 | 📘 Средне |
| `docs/03-technology-combinations/05-benchmarks.md` | ~3 мин | 736 | 📘 Средне |
| `docs/01-svyazi/01-executive-summary.md` | ~3 мин | 693 | 📘 Средне |
| `docs/01-svyazi/14-limitations.md` | ~3 мин | 699 | 📘 Средне |
| `docs/02-anthropic-vacancies/164-10-appendices.md` | ~3 мин | 794 | 📘 Средне |
| `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | ~3 мин | 650 | 📘 Средне |
| `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` | ~3 мин | 792 | 📘 Средне |
| `docs/02-anthropic-vacancies/218-7-application-domains.md` | ~3 мин | 806 | 📘 Средне |
| `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` | ~3 мин | 796 | 📘 Средне |
| `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` | ~3 мин | 798 | 📘 Средне |
| `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` | ~3 мин | 666 | 📘 Средне |
| `docs/03-technology-combinations/02-knowledge-graphs.md` | ~3 мин | 703 | 📘 Средне |
| `docs/04-ai-collaborations/01-executive-summary.md` | ~3 мин | 701 | 📘 Средне |
| `docs/INDEX.md` | ~3 мин | 602 | 📘 Средне |
| `docs/02-anthropic-vacancies/145-8-call-to-action.md` | ~3 мин | 776 | 📘 Средне |
| `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` | ~3 мин | 627 | 📘 Средне |
| `docs/02-anthropic-vacancies/238-7-области-применения.md` | ~3 мин | 631 | 📘 Средне |
| `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` | ~3 мин | 765 | 📘 Средне |
| `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` | ~3 мин | 762 | 📘 Средне |
| `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | ~3 мин | 780 | 📘 Средне |
| `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` | ~3 мин | 637 | 📘 Средне |
| `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` | ~3 мин | 747 | 📘 Средне |
| `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` | ~2 мин | 605 | 📗 Быстро |
| `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` | ~3 мин | 749 | 📘 Средне |
| `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` | ~3 мин | 746 | 📘 Средне |
| `docs/CHANGELOG.md` | ~2 мин | 731 | 📗 Быстро |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | ~2 мин | 198 | 📗 Быстро |
| `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` | ~2 мин | 717 | 📗 Быстро |
| `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` | ~2 мин | 710 | 📗 Быстро |
| `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` | ~2 мин | 710 | 📗 Быстро |
| `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` | ~2 мин | 587 | 📗 Быстро |
| `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` | ~2 мин | 717 | 📗 Быстро |
| `docs/02-anthropic-vacancies/264-11-open-questions.md` | ~2 мин | 714 | 📗 Быстро |
| `docs/02-anthropic-vacancies/294-существующие-приближения.md` | ~2 мин | 599 | 📗 Быстро |
| `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` | ~2 мин | 727 | 📗 Быстро |
| `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` | ~2 мин | 620 | 📗 Быстро |
| `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` | ~2 мин | 703 | 📗 Быстро |
| `docs/02-anthropic-vacancies/156-2-target-populations.md` | ~2 мин | 691 | 📗 Быстро |
| `docs/02-anthropic-vacancies/174-5-architectural-specification.md` | ~2 мин | 689 | 📗 Быстро |
| `docs/02-anthropic-vacancies/279-existing-approximations.md` | ~2 мин | 693 | 📗 Быстро |
| `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` | ~2 мин | 620 | 📗 Быстро |
| `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` | ~2 мин | 663 | 📗 Быстро |
| `docs/02-anthropic-vacancies/155-1-problem-statement.md` | ~2 мин | 667 | 📗 Быстро |
| `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` | ~2 мин | 659 | 📗 Быстро |
| `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` | ~2 мин | 562 | 📗 Быстро |
| `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` | ~2 мин | 550 | 📗 Быстро |
| `docs/TOPIC_MODEL.md` | ~2 мин | 600 | 📗 Быстро |
| `docs/02-anthropic-vacancies/175-6-ethical-framework.md` | ~2 мин | 636 | 📗 Быстро |
| `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | ~2 мин | 353 | 📗 Быстро |
| `docs/ONBOARDING.md` | ~2 мин | 349 | 📗 Быстро |
| `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` | ~2 мин | 335 | 📗 Быстро |
| `docs/02-anthropic-vacancies/162-8-risk-analysis.md` | ~2 мин | 625 | 📗 Быстро |
| `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` | ~2 мин | 627 | 📗 Быстро |
| `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` | ~2 мин | 305 | 📗 Быстро |
| `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` | ~2 мин | 588 | 📗 Быстро |
| `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` | ~2 мин | 595 | 📗 Быстро |
| `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` | ~2 мин | 583 | 📗 Быстро |
| `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` | ~2 мин | 428 | 📗 Быстро |
| `docs/04-ai-collaborations/07-выводы.md` | ~2 мин | 525 | 📗 Быстро |
| `docs/README.md` | ~2 мин | 566 | 📗 Быстро |
| `docs/02-anthropic-vacancies/159-5-economic-model.md` | ~2 мин | 557 | 📗 Быстро |
| `docs/02-anthropic-vacancies/18-6-adapter-interface.md` | ~2 мин | 309 | 📗 Быстро |
| `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` | ~2 мин | 473 | 📗 Быстро |
| `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` | ~2 мин | 570 | 📗 Быстро |
| `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` | ~2 мин | 572 | 📗 Быстро |
| `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | ~2 мин | 497 | 📗 Быстро |
| `docs/NAMED_ENTITIES.md` | ~2 мин | 512 | 📗 Быстро |
| `docs/02-anthropic-vacancies/81-6-adapter-interface.md` | ~2 мин | 289 | 📗 Быстро |
| `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` | ~2 мин | 270 | 📗 Быстро |
| `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` | ~2 мин | 336 | 📗 Быстро |
| `docs/02-anthropic-vacancies/126-установка.md` | ~2 мин | 142 | 📗 Быстро |
| `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` | ~2 мин | 519 | 📗 Быстро |
| `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` | ~2 мин | 426 | 📗 Быстро |
| `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` | ~2 мин | 245 | 📗 Быстро |
| `docs/02-anthropic-vacancies/221-10-open-questions.md` | ~2 мин | 518 | 📗 Быстро |
| `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` | ~2 мин | 440 | 📗 Быстро |
| `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` | ~2 мин | 361 | 📗 Быстро |
| `docs/TECH_RADAR.md` | ~2 мин | 346 | 📗 Быстро |
| `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` | ~2 мин | 504 | 📗 Быстро |
| `docs/02-anthropic-vacancies/266-13-closing.md` | ~1 мин | 485 | 📗 Быстро |
| `docs/02-anthropic-vacancies/268-references.md` | ~1 мин | 491 | 📗 Быстро |
| `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` | ~2 мин | 242 | 📗 Быстро |
| `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` | ~2 мин | 440 | 📗 Быстро |
| `docs/GITHUB_ISSUES.md` | ~1 мин | 301 | 📗 Быстро |
| `docs/01-svyazi/08-conclusions.md` | ~1 мин | 424 | 📗 Быстро |
| `docs/02-anthropic-vacancies/130-отладка.md` | ~1 мин | 207 | 📗 Быстро |
| `docs/02-anthropic-vacancies/136-abstract.md` | ~1 мин | 476 | 📗 Быстро |
| `docs/02-anthropic-vacancies/179-10-open-questions.md` | ~1 мин | 470 | 📗 Быстро |
| `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` | ~1 мин | 381 | 📗 Быстро |
| `docs/02-anthropic-vacancies/223-12-closing.md` | ~1 мин | 462 | 📗 Быстро |
| `docs/02-anthropic-vacancies/243-12-заключение.md` | ~1 мин | 396 | 📗 Быстро |
| `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` | ~1 мин | 481 | 📗 Быстро |
| `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/02-anthropic-vacancies/337-благодарности.md` | ~1 мин | 405 | 📗 Быстро |
| `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` | ~1 мин | 216 | 📗 Быстро |
| `docs/CHANGELOG_AUTO.md` | ~1 мин | 464 | 📗 Быстро |
| `docs/01-svyazi/02-methodology.md` | ~1 мин | 374 | 📗 Быстро |
| `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` | ~1 мин | 305 | 📗 Быстро |
| `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` | ~1 мин | 457 | 📗 Быстро |
| `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` | ~1 мин | 367 | 📗 Быстро |
| `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` | ~1 мин | 448 | 📗 Быстро |
| `docs/02-anthropic-vacancies/281-the-recursive-insight.md` | ~1 мин | 443 | 📗 Быстро |
| `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` | ~1 мин | 458 | 📗 Быстро |
| `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` | ~1 мин | 363 | 📗 Быстро |
| `docs/02-anthropic-vacancies/319-acknowledgments.md` | ~1 мин | 448 | 📗 Быстро |
| `docs/02-anthropic-vacancies/76-1-introduction.md` | ~1 мин | 401 | 📗 Быстро |
| `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` | ~1 мин | 304 | 📗 Быстро |
| `docs/WORD_FREQ.md` | ~1 мин | 417 | 📗 Быстро |
| `docs/02-anthropic-vacancies/06-1-introduction.md` | ~1 мин | 380 | 📗 Быстро |
| `docs/02-anthropic-vacancies/153-executive-summary.md` | ~1 мин | 430 | 📗 Быстро |
| `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` | ~1 мин | 339 | 📗 Быстро |
| `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | ~1 мин | 430 | 📗 Быстро |
| `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` | ~1 мин | 424 | 📗 Быстро |
| `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` | ~1 мин | 343 | 📗 Быстро |
| `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` | ~1 мин | 298 | 📗 Быстро |
| `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` | ~1 мин | 431 | 📗 Быстро |
| `docs/02-anthropic-vacancies/325-аннотация.md` | ~1 мин | 364 | 📗 Быстро |
| `docs/02-anthropic-vacancies/57-native-format.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/03-technology-combinations/03-local-first.md` | ~1 мин | 375 | 📗 Быстро |
| `docs/05-habr-projects/memory/ngt-memory.md` | ~1 мин | 369 | 📗 Быстро |
| `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` | ~1 мин | 355 | 📗 Быстро |
| `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | ~1 мин | 346 | 📗 Быстро |
| `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` | ~1 мин | 390 | 📗 Быстро |
| `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` | ~1 мин | 384 | 📗 Быстро |
| `docs/02-anthropic-vacancies/210-abstract.md` | ~1 мин | 405 | 📗 Быстро |
| `docs/02-anthropic-vacancies/230-аннотация.md` | ~1 мин | 348 | 📗 Быстро |
| `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | ~1 мин | 335 | 📗 Быстро |
| `docs/02-anthropic-vacancies/252-abstract.md` | ~1 мин | 398 | 📗 Быстро |
| `docs/02-anthropic-vacancies/275-why-this-document-exists.md` | ~1 мин | 406 | 📗 Быстро |
| `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` | ~1 мин | 388 | 📗 Быстро |
| `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` | ~1 мин | 328 | 📗 Быстро |
| `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` | ~1 мин | 335 | 📗 Быстро |
| `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` | ~1 мин | 385 | 📗 Быстро |
| `docs/02-anthropic-vacancies/307-abstract.md` | ~1 мин | 407 | 📗 Быстро |
| `docs/02-anthropic-vacancies/77-2-terminology.md` | ~1 мин | 363 | 📗 Быстро |
| `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` | ~1 мин | 207 | 📗 Быстро |
| `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` | ~1 мин | 224 | 📗 Быстро |
| `docs/02-anthropic-vacancies/123-portal-mcp-py.md` | ~1 мин | 232 | 📗 Быстро |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | ~1 мин | 233 | 📗 Быстро |
| `docs/02-anthropic-vacancies/146-acknowledgments.md` | ~1 мин | 381 | 📗 Быстро |
| `docs/02-anthropic-vacancies/168-abstract.md` | ~1 мин | 379 | 📗 Быстро |
| `docs/02-anthropic-vacancies/225-references.md` | ~1 мин | 358 | 📗 Быстро |
| `docs/02-anthropic-vacancies/245-ссылки.md` | ~1 мин | 327 | 📗 Быстро |
| `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` | ~1 мин | 244 | 📗 Быстро |
| `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` | ~1 мин | 360 | 📗 Быстро |
| `docs/02-anthropic-vacancies/287-references.md` | ~1 мин | 373 | 📗 Быстро |
| `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` | ~1 мин | 309 | 📗 Быстро |
| `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` | ~1 мин | 311 | 📗 Быстро |
| `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` | ~1 мин | 314 | 📗 Быстро |
| `docs/02-anthropic-vacancies/90-15-security-considerations.md` | ~1 мин | 351 | 📗 Быстро |
| `docs/BROKEN_LINKS.md` | ~1 мин | 317 | 📗 Быстро |
| `docs/COMPONENT_MATRIX.md` | ~1 мин | 332 | 📗 Быстро |
| `docs/PRIORITIES.md` | ~1 мин | 360 | 📗 Быстро |
| `docs/02-anthropic-vacancies/147-references.md` | ~1 мин | 352 | 📗 Быстро |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | ~1 мин | 343 | 📗 Быстро |
| `docs/02-anthropic-vacancies/183-references.md` | ~1 мин | 351 | 📗 Быстро |
| `docs/02-anthropic-vacancies/204-ссылки.md` | ~1 мин | 297 | 📗 Быстро |
| `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` | ~1 мин | 292 | 📗 Быстро |
| `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` | ~1 мин | 278 | 📗 Быстро |
| `docs/02-anthropic-vacancies/267-acknowledgments.md` | ~1 мин | 353 | 📗 Быстро |
| `docs/02-anthropic-vacancies/285-closing.md` | ~1 мин | 354 | 📗 Быстро |
| `docs/02-anthropic-vacancies/286-acknowledgments.md` | ~1 мин | 342 | 📗 Быстро |
| `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` | ~1 мин | 310 | 📗 Быстро |
| `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` | ~1 мин | 284 | 📗 Быстро |
| `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` | ~1 мин | 210 | 📗 Быстро |
| `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | ~1 мин | 309 | 📗 Быстро |
| `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` | ~1 мин | 349 | 📗 Быстро |
| `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` | ~1 мин | 326 | 📗 Быстро |
| `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` | ~1 мин | 205 | 📗 Быстро |
| `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/GRAPH.md` | ~1 мин | 100 | 📗 Быстро |
| `docs/REPORT.md` | ~1 мин | 189 | 📗 Быстро |
| `docs/02-anthropic-vacancies/07-2-terminology.md` | ~1 мин | 302 | 📗 Быстро |
| `docs/02-anthropic-vacancies/111-4-условия-применимости.md` | ~1 мин | 275 | 📗 Быстро |
| `docs/02-anthropic-vacancies/181-12-closing.md` | ~1 мин | 321 | 📗 Быстро |
| `docs/02-anthropic-vacancies/182-acknowledgments.md` | ~1 мин | 312 | 📗 Быстро |
| `docs/02-anthropic-vacancies/189-аннотация.md` | ~1 мин | 275 | 📗 Быстро |
| `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` | ~1 мин | 184 | 📗 Быстро |
| `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` | ~1 мин | 312 | 📗 Быстро |
| `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` | ~1 мин | 199 | 📗 Быстро |
| `docs/02-anthropic-vacancies/224-acknowledgments.md` | ~1 мин | 312 | 📗 Быстро |
| `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` | ~1 мин | 320 | 📗 Быстро |
| `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | ~1 мин | 329 | 📗 Быстро |
| `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` | ~1 мин | 312 | 📗 Быстро |
| `docs/02-anthropic-vacancies/300-заключение.md` | ~1 мин | 283 | 📗 Быстро |
| `docs/02-anthropic-vacancies/301-благодарности.md` | ~1 мин | 281 | 📗 Быстро |
| `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` | ~1 мин | 281 | 📗 Быстро |
| `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` | ~1 мин | 315 | 📗 Быстро |
| `docs/02-anthropic-vacancies/92-17-versioning-policy.md` | ~1 мин | 306 | 📗 Быстро |
| `docs/02-anthropic-vacancies/QA.md` | ~1 мин | 284 | 📗 Быстро |
| `docs/CONCEPT_GRAPH.md` | ~1 мин | 196 | 📗 Быстро |
| `docs/FOOTNOTES.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/MINDMAP.md` | ~1 мин | 70 | 📗 Быстро |
| `docs/VOCABULARY.md` | ~1 мин | 262 | 📗 Быстро |
| `docs/contacts/anastasiyaw.md` | ~1 мин | 190 | 📗 Быстро |
| `docs/contacts/andrey-chuyan.md` | ~1 мин | 176 | 📗 Быстро |
| `docs/contacts/antipozitive.md` | ~1 мин | 174 | 📗 Быстро |
| `docs/contacts/kksudo.md` | ~1 мин | 178 | 📗 Быстро |
| `docs/contacts/spbmolot.md` | ~1 мин | 180 | 📗 Быстро |
| `docs/contacts/vitalyoborin.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/templates/ensemble.md` | ~1 мин | 59 | 📗 Быстро |
| `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` | ~1 мин | 268 | 📗 Быстро |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | ~1 мин | 290 | 📗 Быстро |
| `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` | ~1 мин | 286 | 📗 Быстро |
| `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` | ~1 мин | 287 | 📗 Быстро |
| `docs/02-anthropic-vacancies/211-table-of-contents.md` | ~1 мин | 286 | 📗 Быстро |
| `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` | ~1 мин | 265 | 📗 Быстро |
| `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` | ~1 мин | 286 | 📗 Быстро |
| `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | ~1 мин | 296 | 📗 Быстро |
| `docs/02-anthropic-vacancies/345-кто-ты.md` | ~1 мин | 269 | 📗 Быстро |
| `docs/02-anthropic-vacancies/47-native-format.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` | ~1 мин | 287 | 📗 Быстро |
| `docs/02-anthropic-vacancies/74-abstract.md` | ~1 мин | 278 | 📗 Быстро |
| `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` | ~1 мин | 284 | 📗 Быстро |
| `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` | ~1 мин | 281 | 📗 Быстро |
| `docs/05-habr-projects/02-collaboration-partners.md` | ~1 мин | 254 | 📗 Быстро |
| `docs/05-habr-projects/knowledge/wikontic.md` | ~1 мин | 256 | 📗 Быстро |
| `docs/05-habr-projects/memory/yodoca.md` | ~1 мин | 256 | 📗 Быстро |
| `docs/CONTACTS.md` | ~1 мин | 151 | 📗 Быстро |
| `docs/CONTACT_PRIORITY.md` | ~1 мин | 150 | 📗 Быстро |
| `docs/PROGRESS.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/contacts/cutcode.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/contacts/dmitriila.md` | ~1 мин | 159 | 📗 Быстро |
| `docs/contacts/mixaill76.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/contacts/nlaik.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/contacts/sonia-black.md` | ~1 мин | 169 | 📗 Быстро |
| `docs/contacts/tagir-analyzes.md` | ~1 мин | 167 | 📗 Быстро |
| `docs/contacts/vladspace.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/contacts/zodigancode.md` | ~1 мин | 159 | 📗 Быстро |
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | ~1 мин | 259 | 📗 Быстро |
| `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | ~1 мин | 275 | 📗 Быстро |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | ~1 мин | 274 | 📗 Быстро |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | ~1 мин | 255 | 📗 Быстро |
| `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` | ~1 мин | 243 | 📗 Быстро |
| `docs/02-anthropic-vacancies/23-11-security-considerations.md` | ~1 мин | 246 | 📗 Быстро |
| `docs/02-anthropic-vacancies/24-12-versioning-policy.md` | ~1 мин | 261 | 📗 Быстро |
| `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` | ~1 мин | 227 | 📗 Быстро |
| `docs/02-anthropic-vacancies/302-ссылки.md` | ~1 мин | 242 | 📗 Быстро |
| `docs/02-anthropic-vacancies/308-table-of-contents.md` | ~1 мин | 268 | 📗 Быстро |
| `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` | ~1 мин | 261 | 📗 Быстро |
| `docs/02-anthropic-vacancies/356-твой-workflow.md` | ~1 мин | 252 | 📗 Быстро |
| `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` | ~1 мин | 242 | 📗 Быстро |
| `docs/02-anthropic-vacancies/85-10-query-flow.md` | ~1 мин | 265 | 📗 Быстро |
| `docs/03-technology-combinations/01-agent-routing.md` | ~1 мин | 244 | 📗 Быстро |
| `docs/COST.md` | ~1 мин | 234 | 📗 Быстро |
| `docs/HEATMAP.md` | ~1 мин | 122 | 📗 Быстро |
| `docs/STALENESS.md` | ~1 мин | 122 | 📗 Быстро |
| `docs/01-svyazi/QA.md` | ~1 мин | 203 | 📗 Быстро |
| `docs/01-svyazi/README.md` | ~1 мин | 96 | 📗 Быстро |
| `docs/02-anthropic-vacancies/04-abstract.md` | ~1 мин | 222 | 📗 Быстро |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | ~1 мин | 206 | 📗 Быстро |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | ~1 мин | 103 | 📗 Быстро |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | ~1 мин | 88 | 📗 Быстро |
| `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` | ~1 мин | 244 | 📗 Быстро |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | ~1 мин | 200 | 📗 Быстро |
| `docs/02-anthropic-vacancies/106-tl-dr.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | ~1 мин | 181 | 📗 Быстро |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/02-anthropic-vacancies/12-content-overview.md` | ~1 мин | 175 | 📗 Быстро |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | ~1 мин | 114 | 📗 Быстро |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | ~1 мин | 95 | 📗 Быстро |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | ~1 мин | 219 | 📗 Быстро |
| `docs/02-anthropic-vacancies/128-доступные-инструменты.md` | ~1 мин | 235 | 📗 Быстро |
| `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` | ~1 мин | 219 | 📗 Быстро |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | ~1 мин | 185 | 📗 Быстро |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | ~1 мин | 144 | 📗 Быстро |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | ~1 мин | 247 | 📗 Быстро |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | ~1 мин | 247 | 📗 Быстро |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | ~1 мин | 178 | 📗 Быстро |
| `docs/02-anthropic-vacancies/16-history.md` | ~1 мин | 78 | 📗 Быстро |
| `docs/02-anthropic-vacancies/169-table-of-contents.md` | ~1 мин | 216 | 📗 Быстро |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | ~1 мин | 145 | 📗 Быстро |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | ~1 мин | 250 | 📗 Быстро |
| `docs/02-anthropic-vacancies/190-содержание.md` | ~1 мин | 182 | 📗 Быстро |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | ~1 мин | 208 | 📗 Быстро |
| `docs/02-anthropic-vacancies/203-благодарности.md` | ~1 мин | 179 | 📗 Быстро |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | ~1 мин | 154 | 📗 Быстро |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | ~1 мин | 256 | 📗 Быстро |
| `docs/02-anthropic-vacancies/21-9-query-flow.md` | ~1 мин | 237 | 📗 Быстро |
| `docs/02-anthropic-vacancies/231-содержание.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/02-anthropic-vacancies/244-благодарности.md` | ~1 мин | 220 | 📗 Быстро |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | ~1 мин | 249 | 📗 Быстро |
| `docs/02-anthropic-vacancies/25-13-reference-implementation.md` | ~1 мин | 189 | 📗 Быстро |
| `docs/02-anthropic-vacancies/253-table-of-contents.md` | ~1 мин | 246 | 📗 Быстро |
| `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` | ~1 мин | 206 | 📗 Быстро |
| `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` | ~1 мин | 251 | 📗 Быстро |
| `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` | ~1 мин | 249 | 📗 Быстро |
| `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | ~1 мин | 221 | 📗 Быстро |
| `docs/02-anthropic-vacancies/31-content-overview.md` | ~1 мин | 183 | 📗 Быстро |
| `docs/02-anthropic-vacancies/320-references.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/02-anthropic-vacancies/326-содержание.md` | ~1 мин | 204 | 📗 Быстро |
| `docs/02-anthropic-vacancies/338-ссылки.md` | ~1 мин | 229 | 📗 Быстро |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | ~1 мин | 94 | 📗 Быстро |
| `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | ~1 мин | 130 | 📗 Быстро |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | ~1 мин | 245 | 📗 Быстро |
| `docs/02-anthropic-vacancies/346-твоё-происхождение.md` | ~1 мин | 133 | 📗 Быстро |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | ~1 мин | 151 | 📗 Быстро |
| `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` | ~1 мин | 100 | 📗 Быстро |
| `docs/02-anthropic-vacancies/349-твоя-личность.md` | ~1 мин | 223 | 📗 Быстро |
| `docs/02-anthropic-vacancies/35-passports-info1-md.md` | ~1 мин | 188 | 📗 Быстро |
| `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` | ~1 мин | 136 | 📗 Быстро |
| `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` | ~1 мин | 219 | 📗 Быстро |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | ~1 мин | 193 | 📗 Быстро |
| `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` | ~1 мин | 220 | 📗 Быстро |
| `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/02-anthropic-vacancies/36-essence.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | ~1 мин | 119 | 📗 Быстро |
| `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` | ~1 мин | 115 | 📗 Быстро |
| `docs/02-anthropic-vacancies/37-native-format.md` | ~1 мин | 216 | 📗 Быстро |
| `docs/02-anthropic-vacancies/38-content-overview.md` | ~1 мин | 137 | 📗 Быстро |
| `docs/02-anthropic-vacancies/39-angle-perspective.md` | ~1 мин | 193 | 📗 Быстро |
| `docs/02-anthropic-vacancies/40-bridges.md` | ~1 мин | 215 | 📗 Быстро |
| `docs/02-anthropic-vacancies/41-compatibility-level.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/02-anthropic-vacancies/42-author-contact.md` | ~1 мин | 191 | 📗 Быстро |
| `docs/02-anthropic-vacancies/43-history.md` | ~1 мин | 178 | 📗 Быстро |
| `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` | ~1 мин | 223 | 📗 Быстро |
| `docs/02-anthropic-vacancies/45-passports-pro2-md.md` | ~1 мин | 186 | 📗 Быстро |
| `docs/02-anthropic-vacancies/46-essence.md` | ~1 мин | 206 | 📗 Быстро |
| `docs/02-anthropic-vacancies/48-content-overview.md` | ~1 мин | 223 | 📗 Быстро |
| `docs/02-anthropic-vacancies/49-angle-perspective.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/02-anthropic-vacancies/50-bridges.md` | ~1 мин | 205 | 📗 Быстро |
| `docs/02-anthropic-vacancies/51-compatibility-level.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/02-anthropic-vacancies/52-author-contact.md` | ~1 мин | 241 | 📗 Быстро |
| `docs/02-anthropic-vacancies/53-history.md` | ~1 мин | 210 | 📗 Быстро |
| `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` | ~1 мин | 240 | 📗 Быстро |
| `docs/02-anthropic-vacancies/55-passports-meta-md.md` | ~1 мин | 186 | 📗 Быстро |
| `docs/02-anthropic-vacancies/56-essence.md` | ~1 мин | 228 | 📗 Быстро |
| `docs/02-anthropic-vacancies/58-content-overview.md` | ~1 мин | 103 | 📗 Быстро |
| `docs/02-anthropic-vacancies/59-angle-perspective.md` | ~1 мин | 205 | 📗 Быстро |
| `docs/02-anthropic-vacancies/60-bridges.md` | ~1 мин | 191 | 📗 Быстро |
| `docs/02-anthropic-vacancies/61-compatibility-level.md` | ~1 мин | 159 | 📗 Быстро |
| `docs/02-anthropic-vacancies/62-author-contact.md` | ~1 мин | 181 | 📗 Быстро |
| `docs/02-anthropic-vacancies/63-history.md` | ~1 мин | 199 | 📗 Быстро |
| `docs/02-anthropic-vacancies/65-readme-md.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` | ~1 мин | 194 | 📗 Быстро |
| `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` | ~1 мин | 218 | 📗 Быстро |
| `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` | ~1 мин | 218 | 📗 Быстро |
| `docs/02-anthropic-vacancies/93-18-reference-implementation.md` | ~1 мин | 230 | 📗 Быстро |
| `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | ~1 мин | 236 | 📗 Быстро |
| `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` | ~1 мин | 242 | 📗 Быстро |
| `docs/03-technology-combinations/04-sozialrecht-domain.md` | ~1 мин | 185 | 📗 Быстро |
| `docs/03-technology-combinations/QA.md` | ~1 мин | 84 | 📗 Быстро |
| `docs/04-ai-collaborations/QA.md` | ~1 мин | 206 | 📗 Быстро |
| `docs/04-ai-collaborations/README.md` | ~1 мин | 165 | 📗 Быстро |
| `docs/05-habr-projects/01-synthesis.md` | ~1 мин | 177 | 📗 Быстро |
| `docs/05-habr-projects/QA.md` | ~1 мин | 94 | 📗 Быстро |
| `docs/AUTHORS.md` | ~1 мин | 67 | 📗 Быстро |
| `docs/AUTOFILLED.md` | ~1 мин | 141 | 📗 Быстро |
| `docs/CITATION_INDEX.md` | ~1 мин | 56 | 📗 Быстро |
| `docs/COMPARE.md` | ~1 мин | 62 | 📗 Быстро |
| `docs/COMPLEXITY.md` | ~1 мин | 118 | 📗 Быстро |
| `docs/CONSISTENCY.md` | ~1 мин | 81 | 📗 Быстро |
| `docs/CONTENT_GAPS.md` | ~1 мин | 152 | 📗 Быстро |
| `docs/CROSSREFS.md` | ~1 мин | 241 | 📗 Быстро |
| `docs/DENSITY.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/DEPENDENCY_MAP.md` | ~1 мин | 99 | 📗 Быстро |
| `docs/DIGEST.md` | ~1 мин | 228 | 📗 Быстро |
| `docs/DUPLICATES.md` | ~1 мин | 71 | 📗 Быстро |
| `docs/ENTITIES.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/GLOSSARY.md` | ~1 мин | 79 | 📗 Быстро |
| `docs/HEALTH.md` | ~1 мин | 60 | 📗 Быстро |
| `docs/KEYWORD_INDEX.md` | ~1 мин | 184 | 📗 Быстро |
| `docs/LLM_SUMMARIES.md` | ~1 мин | 227 | 📗 Быстро |
| `docs/METRICS.md` | ~1 мин | 138 | 📗 Быстро |
| `docs/MISSING.md` | ~1 мин | 116 | 📗 Быстро |
| `docs/NETWORK.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/ORPHANS.md` | ~1 мин | 73 | 📗 Быстро |
| `docs/SCHEDULE.md` | ~1 мин | 91 | 📗 Быстро |
| `docs/SCORING.md` | ~1 мин | 126 | 📗 Быстро |
| `docs/SEE_ALSO.md` | ~1 мин | 72 | 📗 Быстро |
| `docs/SENTIMENT.md` | ~1 мин | 110 | 📗 Быстро |
| `docs/SIMILAR.md` | ~1 мин | 138 | 📗 Быстро |
| `docs/SOURCE_MAP.md` | ~1 мин | 164 | 📗 Быстро |
| `docs/STATS.md` | ~1 мин | 62 | 📗 Быстро |
| `docs/TAGS.md` | ~1 мин | 65 | 📗 Быстро |
| `docs/VALIDATION.md` | ~1 мин | 166 | 📗 Быстро |
| `docs/VERSION_DIFF.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/WORD_CLOUD.md` | ~1 мин | 158 | 📗 Быстро |
| `docs/autofilled/components/.md` | ~1 мин | 95 | 📗 Быстро |
| `docs/autofilled/components/README.md` | ~1 мин | 51 | 📗 Быстро |
| `docs/autofilled/components/cowork.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/ingit.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/kksudo.md` | ~1 мин | 68 | 📗 Быстро |
| `docs/autofilled/components/lorenzo.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/nautilus.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/sgb.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/spbmolot.md` | ~1 мин | 68 | 📗 Быстро |
| `docs/autofilled/components/svend4.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/svyazi.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/research-summary.md` | ~1 мин | 89 | 📗 Быстро |
| `docs/contacts/README.md` | ~1 мин | 65 | 📗 Быстро |
| `docs/templates/README.md` | ~1 мин | 70 | 📗 Быстро |
| `docs/templates/contact-outreach.md` | ~1 мин | 59 | 📗 Быстро |
| `docs/templates/project-component.md` | ~1 мин | 77 | 📗 Быстро |
| `docs/templates/research-note.md` | ~1 мин | 51 | 📗 Быстро |


### 181. Общая картина
_Файл: `docs/obsidian/REPORT.md` | 2 колонок, 9 строк_

| Показатель | Значение |
|------------|---------|
| Всего документов | **529** |
| Всего слов | **523,639** |
| Скриптов обработки | **125** |
| Индекс здоровья | **90/100** |
| Проектов в сети | **22** |
| Связей проектов | **189** |
| Кластеров документов | **120** |
| Ошибок валидации | **0** |
| Предупреждений | **17** |


### 182. Структура репозитория
_Файл: `docs/obsidian/REPORT.md` | 3 колонок, 5 строк_

| Раздел | Файлов | Описание |
|--------|--------|---------|
| `01-svyazi` | 16 | Архитектура Svyazi 2.0 |
| `02-anthropic-vacancies` | 357 | 436 вакансий Anthropic |
| `03-technology-combinations` | 7 | 40+ комбинаций технологий |
| `04-ai-collaborations` | 17 | AI-ансамбли OSS-проектов |
| `05-habr-projects` | 10 | Хабр-проекты: память, граф |


### 183. Топ навигационных документов
_Файл: `docs/obsidian/REPORT.md` | 2 колонок, 7 строк_

| Документ | Назначение |
|----------|------------|
| [[READING_ORDER|READING_ORDER.md]] | С чего начать читать |
| [[SITEMAP|SITEMAP.md]] | Карта всех разделов |
| [[NARRATIVE|NARRATIVE.md]] | История проекта |
| [[DECISIONS|DECISIONS.md]] | Ключевые решения |
| [[CONTACTS|CONTACTS.md]] | С кем связаться |
| [[HEALTH|HEALTH.md]] | Состояние репо |
| [[VALIDATION|VALIDATION.md]] | Проверка структуры |


### 184. Реестр
_Файл: `docs/obsidian/RISK_REGISTER.md` | 7 колонок, 10 строк_

| # | Риск | Категория | Вероятн. | Влияние | Score | Уровень |
|---|------|-----------|----------|---------|-------|---------|
| 1 | Одиночный разработчик — bus factor 1 | Команда | 4 (Высока) | 5 (Критич) | **20** | 🔴 КРИТИЧЕСКИЙ |
| 2 | Авторы компонентов не ответят на запросы | Команда | 3 (Средня) | 5 (Критич) | **15** | 🟠 ВЫСОКИЙ |
| 3 | PII-утечки через MCP-инструменты | Безопасность | 3 (Средня) | 5 (Критич) | **15** | 🟠 ВЫСОКИЙ |
| 4 | Лицензия BSL 1.1 (NGT) ограничит коммерческое испо | Правовой | 3 (Средня) | 4 (Большо) | **12** | 🟠 ВЫСОКИЙ |
| 5 | Высокая стоимость Claude API при масштабировании | Финансовый | 4 (Высока) | 3 (Средне) | **12** | 🟠 ВЫСОКИЙ |
| 6 | Устаревание документации при быстром развитии комп | Качество | 4 (Высока) | 3 (Средне) | **12** | 🟠 ВЫСОКИЙ |
| 7 | AgentFS не поддерживает concurrent multi-agent дос | Технический | 3 (Средня) | 4 (Большо) | **12** | 🟠 ВЫСОКИЙ |
| 8 | Прототип Knowledge OS займёт дольше запланированно | Сроки | 3 (Средня) | 3 (Средне) | **9** | 🟠 ВЫСОКИЙ |
| 9 | Зависимость от закрытого API Anthropic | Технический | 2 (Низкая) | 4 (Большо) | **8** | 🟡 СРЕДНИЙ |
| 10 | Конкурирующие OSS-проекты могут обогнать | Рынок | 2 (Низкая) | 3 (Средне) | **6** | 🟡 СРЕДНИЙ |


### 185. Упоминания рисков в документах
_Файл: `docs/obsidian/RISK_REGISTER.md` | 2 колонок, 11 строк_

| Источник | Фрагмент |
|----------|---------|
| `01-executive-summary` | [^sentinel]: OSS-проект: безопасность и allowlist для MCP [^rufler]: OSS-проект: оркестратор AI-аген… |
| `02-methodology` | иде улучшают доказуемость, безопасность, локальность или стоимость выполнения Когда у статьи не было… |
| `03-component-catalog` | w1turn20view18 | Рантайм‑безопасность и бюджетный execution plane для агентных систем. | SENTINEL[… |
| `04-ensembles-overview` | ри минимальном интеграционном риске**. **Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[[06-безопасность-приватность-и-бюджетный-роутинг|… |
| `04-ensembles-overview` | а**: Self‑Aware MCP закрывает проблемы часового пояса, ОС, даты и локации. citeturn20view12turn30… |
| `06-security-privacy` | t, collaboration --> ## Безопасность, приватность и бюджетный роутинг Для Svyazi‑2.0 безопасная архи… |
| `06-security-privacy` | Похожие документы:** - [06-безопасность-приватность-и-бюджетный-роутинг]] (сходство 1.00) - [05-пл… |
| `06-security-privacy` | **Смотрите также:** - [06-безопасность-приватность-и-бюджетный-роутинг](docs/04-ai-collaborations/06… |
| `07-mvp-planning` | l Search + базовые правила безопасности | Удержать стоимость и не утонуть в MCP[^mcp]/context overhe… |
| `07-mvp-planning` | review для inferred | Снизить риск ложных связей и утечек | 1–2 дня | **Итого**: реалистичный MVP — … |
| `07-mvp-planning` | нных компонентов. **Ключевые риски и как их закрывать** | Риск | Почему это важно | Снижение риска |… |


### 186. Итоговая статистика
_Файл: `docs/obsidian/RISK_REGISTER.md` | 2 колонок, 3 строк_

| Уровень | Кол-во |
|---------|--------|
| 🔴 КРИТИЧЕСКИЙ | 1 |
| 🟠 ВЫСОКИЙ | 7 |
| 🟡 СРЕДНИЙ | 2 |


### 187. Ключевые вехи
_Файл: `docs/obsidian/SCHEDULE.md` | 3 колонок, 10 строк_

| Срок | Веха | Статус |
|------|------|--------|
| **2024-Q4** | ✅ Исследование компонентов завершено | ✅ Выполнено |
| **2024-Q4** | ✅ Архитектура Svyazi 2.0 задокументирована | ✅ Выполнено |
| **2025-Q1** | ✅ Интеграционные контракты описаны | ✅ Выполнено |
| **2025-Q1** | ⬜ Написать авторам AgentFS, Yodoca, NGT | ⬜ Планируется |
| **2025-Q2** | ⬜ Получить согласие на сотрудничество | ⬜ Планируется |
| **2025-Q2** | ⬜ Создать рабочее окружение Knowledge OS | ⬜ Планируется |
| **2025-Q3** | ⬜ Прототип ансамбля (Svyazi + CardIndex) | ⬜ Планируется |
| **2025-Q3** | ⬜ Тестирование на реальных данных | ⬜ Планируется |
| **2025-Q4** | ⬜ Интеграция SENTINEL + MCP Tool Search | ⬜ Планируется |
| **2026-Q1** | ⬜ Публичный MVP-релиз на GitHub | ⬜ Планируется |


### 188. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/obsidian/SCORING.md` | 3 колонок, 6 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Executive Summary существует | ✅ | 10 |
| Архитектурные контракты описаны | ✅ | 10 |
| MVP план задокументирован | ✅ | 10 |
| Дорожная карта есть | ✅ | 8 |
| README в каждом разделе | ✅ | 5 |
| Глоссарий создан | ✅ | 5 |


### 189. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/obsidian/SCORING.md` | 3 колонок, 5 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Компоненты каталогизированы (20+) | ✅ | 10 |
| Ансамбли определены (5+) | ✅ | 10 |
| Архитектурные пробелы выявлены | ✅ | 8 |
| Безопасность и PII описаны | ✅ | 8 |
| Граф связей проектов построен | ✅ | 5 |


### 190. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/obsidian/SCORING.md` | 3 колонок, 3 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Контакты авторов компонентов есть | ✅ | 10 |
| Авторы Habr-проектов найдены | ✅ | 8 |
| Шаблоны для связи созданы | ✅ | 5 |


### 191. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/obsidian/SCORING.md` | 3 колонок, 6 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Риски выявлены и задокументированы | ✅ | 8 |
| Лицензии проверены | ✅ | 8 |
| Сломанных ссылок < 30 | ❌ | 5 |
|  ↳ _Слишком много сломанных ссылок_ | | |
| Дублей нет | ❌ | 5 |
|  ↳ _Есть точные дубли документов_ | | |


### 192. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/obsidian/SCORING.md` | 3 колонок, 4 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Прогресс MVP отслеживается | ✅ | 8 |
| Action items задокументированы | ✅ | 8 |
| Порядок чтения задан | ✅ | 5 |
| Executive report создан | ✅ | 5 |


### 193. Тональность по разделам
_Файл: `docs/obsidian/SENTIMENT.md` | 6 колонок, 9 строк_

| Раздел | Оптимизм | Скептицизм | Срочность | Неопределённость | Тон |
|--------|----------|------------|-----------|-----------------|-----|
| **01-svyazi** | 2.3‰ | 7.1‰ | 4.9‰ | 0.5‰ | 🔴 скептичный |
| **02-anthropic-vacancies** | 1.6‰ | 5.7‰ | 1.8‰ | 1.5‰ | 🔴 скептичный |
| **03-technology-combinations** | 3.5‰ | 1.2‰ | 2.0‰ | 0.4‰ | 🟢 оптимистичный |
| **04-ai-collaborations** | 2.2‰ | 5.1‰ | 2.0‰ | 0.8‰ | 🔴 скептичный |
| **05-habr-projects** | 4.6‰ | 1.7‰ | 0.9‰ | 1.3‰ | 🟢 оптимистичный |
| **autofilled** | 0.0‰ | 0.0‰ | 0.0‰ | 0.0‰ | ⚪ нейтральный |
| **contacts** | 0.0‰ | 0.0‰ | 1.0‰ | 0.0‰ | 🟠 срочный |
| **root** | 0.5‰ | 25.0‰ | 1.7‰ | 0.7‰ | 🔴 скептичный |
| **templates** | 0.0‰ | 14.7‰ | 0.0‰ | 0.0‰ | 🔴 скептичный |


### 194. Самые оптимистичные документы
_Файл: `docs/obsidian/SENTIMENT.md` | 3 колонок, 10 строк_

| Документ | Оптимизм‰ | Тон |
|----------|----------|-----|
| `110-вопрос-fallback-ratio-как-крити` | 16.3 | 🟠 срочный |
| `193-3-что-делает-агента-представите` | 16.0 | 🟢 оптимистичный |
| `123-portal-mcp-py` | 13.2 | 🟢 оптимистичный |
| `02-collaboration-partners` | 13.2 | 🟢 оптимистичный |
| `yodoca` | 13.2 | 🟢 оптимистичный |
| `248-приложение-c-архитектура-быстро` | 12.9 | 🟢 оптимистичный |
| `232-1-типология-из-пяти-типов-агент` | 12.8 | 🟢 оптимистичный |
| `240-9-связь-с-другими-типами-агенто` | 11.3 | ⚪ нейтральный |
| `08-3-registry-nautilus-json` | 11.2 | 🟠 срочный |
| `01-synthesis` | 10.9 | 🟢 оптимистичный |


### 195. Самые скептичные / риск-ориентированные
_Файл: `docs/obsidian/SENTIMENT.md` | 3 колонок, 10 строк_

| Документ | Скептицизм‰ | Тон |
|----------|------------|-----|
| `PARAGRAPH_QUALITY` | 312.8 | 🔴 скептичный |
| `198-8-риски-и-меры-противодействия` | 88.3 | 🔴 скептичный |
| `177-8-risks-and-mitigations` | 84.1 | 🔴 скептичный |
| `ensemble` | 64.5 | 🔴 скептичный |
| `162-8-risk-analysis` | 50.5 | 🔴 скептичный |
| `263-10-risks-specific-to-composite-` | 43.1 | 🔴 скептичный |
| `RISK_REGISTER` | 36.0 | 🔴 скептичный |
| `README` | 35.4 | 🔴 скептичный |
| `237-6-риски-специфичные-для-этой-ка` | 34.7 | 🔴 скептичный |
| `217-6-risks-specific-to-this-catego` | 33.9 | 🔴 скептичный |


### 196. Распределение тональности
_Файл: `docs/obsidian/SENTIMENT.md` | 2 колонок, 5 строк_

| Тон | Файлов |
|-----|--------|
| 🔴 скептичный | 234 |
| ⚪ нейтральный | 155 |
| 🟠 срочный | 55 |
| 🟢 оптимистичный | 30 |
| 🟡 неопределённый | 14 |


### 197. Топ-20 самых похожих пар
_Файл: `docs/obsidian/SIMILAR.md` | 3 колонок, 20 строк_

| Сходство | Файл A | Файл B |
|----------|--------|--------|
| 1.000 | `13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | `13-contacts.md` |
| 1.000 | `12-дорожная-карта-прототипа-следующей-итерации.md` | `12-roadmap.md` |
| 1.000 | `11-интеграционный-контракт-который-стоит-зафиксироват.md` | `11-integration-contracts.md` |
| 1.000 | `09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | `09-architectural-gaps.md` |
| 1.000 | `06-безопасность-приватность-и-бюджетный-роутинг.md` | `06-security-privacy.md` |
| 1.000 | `05-план-прототипа-и-возможные-контакты.md` | `07-mvp-planning.md` |
| 0.994 | `03-карта-найденных-проектов-и-паттернов.md` | `03-component-catalog.md` |
| 0.952 | `07-выводы.md` | `08-conclusions.md` |
| 0.922 | `10-новые-ансамбли-следующего-шага.md` | `10-second-order-ensembles.md` |
| 0.916 | `04-приоритетные-ансамбли.md` | `04-ensembles-overview.md` |
| 0.889 | `94-19-adr-001-federation-over-merging.md` | `26-14-adr-001-federation-over-merging.md` |
| 0.859 | `SEARCH.md` | `READING_ORDER.md` |
| 0.858 | `QA.md` | `QA.md` |
| 0.818 | `QA.md` | `QA.md` |
| 0.739 | `02-методика-и-рамка-отбора.md` | `02-methodology.md` |
| 0.720 | `85-10-query-flow.md` | `21-9-query-flow.md` |
| 0.702 | `251-ai-support-through-configurable-specialist-ensembl.md` | `209-a-typology-of-ai-agents-on-the-principal-side-and-.md` |
| 0.680 | `01-executive-summary.md` | `01-executive-summary.md` |
| 0.673 | `README.md` | `README.md` |
| 0.667 | `61-compatibility-level.md` | `51-compatibility-level.md` |


### 198. Мета-документы
_Файл: `docs/obsidian/SITEMAP.md` | 3 колонок, 101 строк_

| Документ | Описание | Слов |
|----------|----------|------|
| [[ABBREVIATIONS|ABBREVIATIONS.md]] | — | 1415 |
| [[ACTION_ITEMS|ACTION_ITEMS.md]] | Задачи и риски (490) | 6656 |
| [[ALERTS|ALERTS.md]] | — | 79 |
| [[AUTHORS|AUTHORS.md]] | Авторы и контакты | 158 |
| [[AUTOFILLED|AUTOFILLED.md]] | — | 115 |
| [[BACKLINKS|BACKLINKS.md]] | — | 339 |
| [[BROKEN_LINKS|BROKEN_LINKS.md]] | Сломанные ссылки (26) | 726 |
| [[CHANGELOG|CHANGELOG.md]] | История изменений | 888 |
| [[CHANGELOG_AUTO|CHANGELOG_AUTO.md]] | — | 627 |
| [[CITATION_INDEX|CITATION_INDEX.md]] | — | 909 |
| [[CLUSTERS|CLUSTERS.md]] | Кластеры (384 → 120 групп) | 1612 |
| [[CODE_BLOCKS|CODE_BLOCKS.md]] | — | 3658 |
| [[COMPARE|COMPARE.md]] | Сравнение с предыдущим коммитом | 477 |
| [[COMPLEXITY|COMPLEXITY.md]] | Оценка читаемости | 605 |
| [[COMPONENT_MATRIX|COMPONENT_MATRIX.md]] | — | 959 |
| [[CONCEPTS|CONCEPTS.md]] | Глоссарий понятий (888) | 11402 |
| [[CONCEPT_GRAPH|CONCEPT_GRAPH.md]] | — | 745 |
| [[CONSISTENCY|CONSISTENCY.md]] | — | 313 |
| [[CONTACTS|CONTACTS.md]] | Контакты (15 авторов) | 512 |
| [[CONTACT_PRIORITY|CONTACT_PRIORITY.md]] | — | 412 |
| [[CONTENT_GAPS|CONTENT_GAPS.md]] | — | 886 |
| [[CONTRADICTIONS|CONTRADICTIONS.md]] | — | 2088 |
| [[COST|COST.md]] | — | 697 |
| [[COVERAGE|COVERAGE.md]] | — | 731 |
| [[CROSSREFS|CROSSREFS.md]] | Перекрёстные ссылки проектов | 653 |
| [[DECISIONS|DECISIONS.md]] | Ключевые решения (150) | 1911 |
| [[DENSITY|DENSITY.md]] | Карта плотности тем | 650 |
| [[DEPENDENCY_MAP|DEPENDENCY_MAP.md]] | — | 675 |
| [[DIGEST|DIGEST.md]] | — | 379 |
| [[DIGEST_WEEKLY|DIGEST_WEEKLY.md]] | — | 228 |
| [[DUPLICATES|DUPLICATES.md]] | — | 67 |
| [[ENTITIES|ENTITIES.md]] | Именованные сущности | 727 |
| [[FAQ|FAQ.md]] | — | 836 |
| [[FOOTNOTES|FOOTNOTES.md]] | — | 275 |
| [[GLOSSARY|GLOSSARY.md]] | Глоссарий проектов (33 записи) | 204 |
| [[GRAPH|GRAPH.md]] | Граф связей проектов | 2660 |
| [[HEALTH|HEALTH.md]] | Дашборд здоровья (75/100) | 174 |
| [[HEATMAP|HEATMAP.md]] | — | 537 |
| [[INDEX|INDEX.md]] | — | 685 |
| [[KEYWORD_INDEX|KEYWORD_INDEX.md]] | — | 1115 |
| [[KPI|KPI.md]] | Числовые KPI (737 показателей) | 2318 |
| [[KPI_HISTORY|KPI_HISTORY.md]] | — | 106 |
| [[LINKS|LINKS.md]] | Внешние ссылки | 969 |
| [[LLM_SUMMARIES|LLM_SUMMARIES.md]] | — | 226 |
| [[METRICS|METRICS.md]] | — | 445 |
| [[MINDMAP|MINDMAP.md]] | Майндмап в Mermaid | 242 |
| [[MISSING|MISSING.md]] | Пробелы знаний | 434 |
| [[NAMED_ENTITIES|NAMED_ENTITIES.md]] | — | 1734 |
| [[NARRATIVE|NARRATIVE.md]] | — | 1060 |
| [[NETWORK|NETWORK.md]] | — | 417 |
| [[ONBOARDING|ONBOARDING.md]] | — | 606 |
| [[ORPHANS|ORPHANS.md]] | — | 107 |
| [[OUTLINE|OUTLINE.md]] | — | 14163 |
| [[PARAGRAPH_QUALITY|PARAGRAPH_QUALITY.md]] | — | 8527 |
| [[PRIORITIES|PRIORITIES.md]] | Приоритеты (TF-IDF) | 1151 |
| [[PROGRESS|PROGRESS.md]] | — | 292 |
| [[QA|QA.md]] | Вопросы и ответы | 224 |
| [[QA|QA.md]] | Вопросы и ответы | 322 |
| [[QA|QA.md]] | Вопросы и ответы | 107 |
| [[QA|QA.md]] | Вопросы и ответы | 226 |
| [[QA|QA.md]] | Вопросы и ответы | 115 |
| [[QA|QA.md]] | Вопросы и ответы | 979 |
| [[QUESTIONS|QUESTIONS.md]] | Открытые вопросы (484) | 1623 |
| [[READABILITY|READABILITY.md]] | — | 7981 |
| [[READING_ORDER|READING_ORDER.md]] | Рекомендуемый порядок чтения | 5947 |
| [[READING_TIME|READING_TIME.md]] | — | 5485 |
| [[README|README.md]] | Главная страница и навигация | 126 |
| [[README|README.md]] | Главная страница и навигация | 2162 |
| [[README|README.md]] | Главная страница и навигация | 49 |
| [[README|README.md]] | Главная страница и навигация | 113 |
| [[README|README.md]] | Главная страница и навигация | 42 |
| [[README|README.md]] | Главная страница и навигация | 13 |
| [[README|README.md]] | Главная страница и навигация | 25 |
| [[README|README.md]] | Главная страница и навигация | 622 |
| [[README|README.md]] | Главная страница и навигация | 18 |
| [[README|README.md]] | Главная страница и навигация | 56 |
| [[README|README.md]] | Главная страница и навигация | 44 |
| [[README|README.md]] | Главная страница и навигация | 90 |
| [[README|README.md]] | Главная страница и навигация | 90 |
| [[REPORT|REPORT.md]] | — | 361 |
| [[RISK_REGISTER|RISK_REGISTER.md]] | — | 1043 |
| [[SCHEDULE|SCHEDULE.md]] | — | 332 |
| [[SCORING|SCORING.md]] | — | 387 |
| [[SEARCH|SEARCH.md]] | Поисковый индекс | 4370 |
| [[SEE_ALSO|SEE_ALSO.md]] | — | 217 |
| [[SENTIMENT|SENTIMENT.md]] | — | 407 |
| [[SIMILAR|SIMILAR.md]] | Похожие документы (937 пар) | 393 |
| [[SOURCE_MAP|SOURCE_MAP.md]] | — | 3025 |
| [[SPELLCHECK|SPELLCHECK.md]] | — | 143 |
| [[STALENESS|STALENESS.md]] | — | 335 |
| [[STATS|STATS.md]] | Детальная статистика | 494 |
| [[TABLES|TABLES.md]] | — | 63292 |
| [[TAGS|TAGS.md]] | Теги (316 файлов, 12 тем) | 600 |
| [[TECH_RADAR|TECH_RADAR.md]] | — | 635 |
| [[TIMELINE|TIMELINE.md]] | Временная шкала (800 маркеров) | 4110 |
| [[TOPIC_MODEL|TOPIC_MODEL.md]] | — | 1051 |
| [[VALIDATION|VALIDATION.md]] | — | 387 |
| [[VERSION_DIFF|VERSION_DIFF.md]] | — | 526 |
| [[VOCABULARY|VOCABULARY.md]] | — | 987 |
| [[WORD_CLOUD|WORD_CLOUD.md]] | — | 244 |
| [[WORD_FREQ|WORD_FREQ.md]] | Частотный анализ слов | 1790 |


### 199. Svyazi 2.0 — Архитектура системы
_Файл: `docs/obsidian/SITEMAP.md` | 3 колонок, 14 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-intro-part2|Продолжение исследования для Svyazi 2.0]] | 6 |
| 2 | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 708 |
| 3 | [[02-methodology|Методика и рамка отбора проектов]] | 428 |
| 4 | [[03-component-catalog]] | 1395 |
| 5 | [[04-ensembles-overview]] | 1274 |
| 6 | [[06-security-privacy]] | 821 |
| 7 | [[07-mvp-planning]] | 1083 |
| 8 | [[08-conclusions]] | 360 |
| 9 | [[09-architectural-gaps]] | 757 |
| 10 | [[10-second-order-ensembles]] | 916 |
| 11 | [[11-integration-contracts]] | 745 |
| 12 | [[12-roadmap]] | 733 |
| 13 | [[13-contacts]] | 827 |
| 14 | [[14-limitations]] | 636 |


### 200. Svyazi 2.0 — Архитектура системы
_Файл: `docs/obsidian/SITEMAP.md` | 3 колонок, 51 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-intro|Введение]] | 8884 |
| 2 | [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]] | 19103 |
| 3 | [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]] | 3181 |
| 4 | [[03-portal-protocol-md|PORTAL-PROTOCOL.md]] | 150 |
| 5 | [[04-abstract|Abstract]] | 188 |
| 6 | [[05-0-status-of-this-document|0. Status of This Document]] | 162 |
| 7 | [[06-1-introduction|1. Introduction]] | 380 |
| 8 | [[07-2-terminology|2. Terminology]] | 313 |
| 9 | [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] | 422 |
| 10 | [[09-4-passport-passport-md|4. Passport (`passport.md`)]] | 197 |
| 11 | [[102-доступ-к-данным|Доступ к данным]] | 65 |
| 12 | [[103-appendix-b-change-log|Appendix B: Change Log]] | 232 |
| 13 | [[104-appendix-c-references|Appendix C: References]] | 947 |
| 14 | [[105-review-methodology-md|REVIEW_METHODOLOGY.md]] | 128 |
| 15 | [[106-tl-dr|TL;DR]] | 168 |
| 16 | [[107-1-контекст-и-мотивация|1. Контекст и мотивация]] | 412 |
| 17 | [[108-2-формальный-workflow|2. Формальный workflow]] | 479 |
| 18 | [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]] | 541 |
| 19 | [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или осмысле]] | 258 |
| 20 | [[111-4-условия-применимости|4. Условия применимости]] | 279 |
| 21 | [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]] | 340 |
| 22 | [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assisted wor]] | 173 |
| 23 | [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]] | 327 |
| 24 | [[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]] | 412 |
| 25 | [[116-9-checklist-применения-методологии|9. Checklist применения методологии]] | 331 |
| 26 | [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим документа]] | 258 |
| 27 | [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]] | 176 |
| 28 | [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешения]] | 292 |
| 29 | [[12-content-overview|Content Overview]] | 113 |
| 30 | [[120-главные-технические-риски|Главные технические риски]] | 101 |
| 31 | [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]] | 78 |
| 32 | [[122-глоссарий|Глоссарий]] | 1302 |
| 33 | [[123-portal-mcp-py|portal-mcp.py]] | 2316 |
| 34 | [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]] | 212 |
| 35 | [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]] | 152 |
| 36 | [[126-установка|Установка]] | 169 |
| 37 | [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]] | 173 |
| 38 | [[128-доступные-инструменты|Доступные инструменты]] | 204 |
| 39 | [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]] | 176 |
| 40 | [[13-angle-perspective|Angle / Perspective]] | 127 |
| 41 | [[130-отладка|Отладка]] | 205 |
| 42 | [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]] | 133 |
| 43 | [[132-planned-v0-2-0|Planned (v0.2.0)]] | 131 |
| 44 | [[133-обратная-связь|Обратная связь]] | 16959 |
| 45 | [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]] | 130 |
| 46 | [[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in Distr]] | 167 |
| 47 | [[136-abstract|Abstract]] | 388 |
| 48 | [[137-table-of-contents|Table of Contents]] | 172 |
| 49 | [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]] | 583 |
| 50 | [[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]] | 755 |
| ... | _ещё 305 файлов_ | |


### 201. Svyazi 2.0 — Архитектура системы
_Файл: `docs/obsidian/SITEMAP.md` | 3 колонок, 5 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[01-agent-routing|Агентные системы и роутинг]] | 257 |
| 2 | [[02-knowledge-graphs|Графы знаний и Legal AI]] | 766 |
| 3 | [[03-local-first|Local-first и P2P стек]] | 386 |
| 4 | [[04-sozialrecht-domain|Домен: немецкое социальное право]] | 172 |
| 5 | [[05-benchmarks|Бенчмарки и производительность]] | 863 |


### 202. Svyazi 2.0 — Архитектура системы
_Файл: `docs/obsidian/SITEMAP.md` | 3 колонок, 15 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-intro|Введение]] | 11445 |
| 2 | [[01-executive-summary|Executive summary]] | 647 |
| 3 | [[02-методика-и-рамка-отбора|Методика и рамка отбора]] | 495 |
| 4 | [[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]] | 1553 |
| 5 | [[04-приоритетные-ансамбли|Приоритетные ансамбли]] | 1418 |
| 6 | [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]] | 1212 |
| 7 | [[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]] | 966 |
| 8 | [[07-выводы|Выводы]] | 542 |
| 9 | [[08-что-это-продолжение-добавляет|Что это продолжение добавляет]] | 492 |
| 10 | [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых инструм]] | 901 |
| 11 | [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]] | 1062 |
| 12 | [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафиксирова]] | 928 |
| 13 | [[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]] | 862 |
| 14 | [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авторов]] | 956 |
| 15 | [[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|Ограничения, лицензии и что пока лучше не склеиват]] | 3362 |


### 203. Svyazi 2.0 — Архитектура системы
_Файл: `docs/obsidian/SITEMAP.md` | 3 колонок, 6 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[01-synthesis|Синтез: как проекты собираются вместе]] | 184 |
| 2 | [[02-collaboration-partners|Авторы и контакты]] | 303 |
| 3 | [[wikontic|Wikontic: семантический граф]] | 306 |
| 4 | [[memnet|MemNet: исследовательская память]] | 7271 |
| 5 | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 419 |
| 6 | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 303 |


### 204. Svyazi 2.0 — Архитектура системы
_Файл: `docs/obsidian/SITEMAP.md` | 3 колонок, 11 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[.md|Антропик]] | 81 |
| 2 | [[cowork]] | 81 |
| 3 | [[ingit]] | 81 |
| 4 | [[kksudo]] | 67 |
| 5 | [[lorenzo]] | 81 |
| 6 | [[nautilus]] | 81 |
| 7 | [[sgb]] | 81 |
| 8 | [[spbmolot]] | 67 |
| 9 | [[svend4]] | 81 |
| 10 | [[svyazi]] | 81 |
| 11 | [[Тема исследования]](docs/autofilled/research-summary.md) | 122 |


### 205. Svyazi 2.0 — Архитектура системы
_Файл: `docs/obsidian/SITEMAP.md` | 3 колонок, 14 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[anastasiyaw|Контакт: AnastasiyaW / knowledge-space, mclaude]] | 292 |
| 2 | [[andrey-chuyan|Контакт: andrey_chuyan / Svyazi]] | 274 |
| 3 | [[antipozitive|Контакт: Antipozitive / MemNet]] | 264 |
| 4 | [[cutcode|Контакт: Cutcode / AIF Handoff]] | 255 |
| 5 | [[dmitriila|Контакт: Dmitriila / SENTINEL]] | 251 |
| 6 | [[kksudo|Контакт: kksudo / AgentFS]] | 288 |
| 7 | [[mixaill76|Контакт: MiXaiLL76 / Auto AI Router]] | 259 |
| 8 | [[nlaik|Контакт: nlaik / LiteParse / research-docs]] | 260 |
| 9 | [[sonia-black|Контакт: Sonia_Black / knowledge-space]] | 252 |
| 10 | [[spbmolot|Контакт: spbmolot / NGT Memory]] | 292 |
| 11 | [[tagir-analyzes|Контакт: tagir_analyzes / Legal RAG]] | 257 |
| 12 | [[vitalyoborin|Контакт: VitalyOborin / Yodoca]] | 278 |
| 13 | [[vladspace|Контакт: VladSpace / Graph RAG]] | 255 |
| 14 | [[zodigancode|Контакт: zodigancode / Rufler]] | 251 |


### 206. Svyazi 2.0 — Архитектура системы
_Файл: `docs/obsidian/SITEMAP.md` | 3 колонок, 5 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Контакт: [Имя / Проект]](docs/templates/contact-outreach.md) | 133 |
| 2 | [ADR: [Название решения]](docs/templates/decision-record.md) | 94 |
| 3 | [Ансамбль: [Название]](docs/templates/ensemble.md) | 124 |
| 4 | [[Название компонента]](docs/templates/project-component.md) | 116 |
| 5 | [[Тема исследования]](docs/templates/research-note.md) | 78 |


### 207. Категории
_Файл: `docs/obsidian/SOURCE_MAP.md` | 2 колонок, 2 строк_

| Категория | Файлов |
|-----------|--------|
| 🤖 Авто-импорт | 391 |
| ✍️ Ручной | 132 |


### 208. Авторы
_Файл: `docs/obsidian/SOURCE_MAP.md` | 2 колонок, 2 строк_

| Автор | Файлов |
|-------|--------|
| Claude | 513 |
| unknown | 10 |


### 209. 🤖 Авто-импортированные файлы (391)
_Файл: `docs/obsidian/SOURCE_MAP.md` | 3 колонок, 391 строк_

| Файл | Слов | Первый коммит |
|------|------|--------------|
| `docs/01-svyazi/00-intro-part2.md` | 6 | 2026-04-29 |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 16 | 2026-04-29 |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 65 | 2026-04-29 |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 78 | 2026-04-29 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 101 | 2026-04-29 |
| `docs/02-anthropic-vacancies/16-history.md` | 104 | 2026-04-29 |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 106 | 2026-04-29 |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 108 | 2026-04-29 |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 113 | 2026-04-29 |
| `docs/02-anthropic-vacancies/31-content-overview.md` | 113 | 2026-04-29 |
| `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | 122 | 2026-04-29 |
| `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` | 123 | 2026-04-29 |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | 125 | 2026-04-29 |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 126 | 2026-04-29 |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | 126 | 2026-04-29 |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | 127 | 2026-04-29 |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | 128 | 2026-04-29 |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | 128 | 2026-04-29 |
| `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` | 128 | 2026-04-29 |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 130 | 2026-04-29 |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 130 | 2026-04-29 |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | 131 | 2026-04-29 |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | 133 | 2026-04-29 |
| `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` | 133 | 2026-04-29 |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | 133 | 2026-04-29 |
| `docs/02-anthropic-vacancies/35-passports-info1-md.md` | 133 | 2026-04-29 |
| `docs/02-anthropic-vacancies/55-passports-meta-md.md` | 134 | 2026-04-29 |
| `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` | 136 | 2026-04-29 |
| `docs/02-anthropic-vacancies/45-passports-pro2-md.md` | 137 | 2026-04-29 |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 138 | 2026-04-29 |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | 140 | 2026-04-29 |
| `docs/02-anthropic-vacancies/62-author-contact.md` | 140 | 2026-04-29 |
| `docs/02-anthropic-vacancies/42-author-contact.md` | 145 | 2026-04-29 |
| `docs/02-anthropic-vacancies/58-content-overview.md` | 147 | 2026-04-29 |
| `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` | 148 | 2026-04-29 |
| `docs/02-anthropic-vacancies/38-content-overview.md` | 148 | 2026-04-29 |
| `docs/02-anthropic-vacancies/61-compatibility-level.md` | 148 | 2026-04-29 |
| `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` | 149 | 2026-04-29 |
| `docs/02-anthropic-vacancies/51-compatibility-level.md` | 149 | 2026-04-29 |
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | 150 | 2026-04-29 |
| `docs/02-anthropic-vacancies/190-содержание.md` | 151 | 2026-04-29 |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | 152 | 2026-04-29 |
| `docs/02-anthropic-vacancies/41-compatibility-level.md` | 152 | 2026-04-29 |
| `docs/02-anthropic-vacancies/25-13-reference-implementation.md` | 153 | 2026-04-29 |
| `docs/02-anthropic-vacancies/65-readme-md.md` | 153 | 2026-04-29 |
| `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` | 153 | 2026-04-29 |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | 162 | 2026-04-29 |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | 164 | 2026-04-29 |
| `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` | 164 | 2026-04-29 |
| `docs/02-anthropic-vacancies/43-history.md` | 165 | 2026-04-29 |
| `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` | 166 | 2026-04-29 |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | 167 | 2026-04-29 |
| `docs/02-anthropic-vacancies/169-table-of-contents.md` | 167 | 2026-04-29 |
| `docs/02-anthropic-vacancies/106-tl-dr.md` | 168 | 2026-04-29 |
| `docs/02-anthropic-vacancies/49-angle-perspective.md` | 168 | 2026-04-29 |
| `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` | 168 | 2026-04-29 |
| `docs/02-anthropic-vacancies/126-установка.md` | 169 | 2026-04-29 |
| `docs/02-anthropic-vacancies/346-твоё-происхождение.md` | 169 | 2026-04-29 |
| `docs/02-anthropic-vacancies/46-essence.md` | 170 | 2026-04-29 |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | 172 | 2026-04-29 |
| `docs/03-technology-combinations/04-sozialrecht-domain.md` | 172 | 2026-04-29 |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/231-содержание.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/39-angle-perspective.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/52-author-contact.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` | 174 | 2026-04-29 |
| `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` | 174 | 2026-04-29 |
| `docs/02-anthropic-vacancies/59-angle-perspective.md` | 175 | 2026-04-29 |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | 176 | 2026-04-29 |
| `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` | 176 | 2026-04-29 |
| `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` | 176 | 2026-04-29 |
| `docs/02-anthropic-vacancies/326-содержание.md` | 178 | 2026-04-29 |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | 179 | 2026-04-29 |
| `docs/02-anthropic-vacancies/36-essence.md` | 179 | 2026-04-29 |
| `docs/02-anthropic-vacancies/60-bridges.md` | 180 | 2026-04-29 |
| `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` | 180 | 2026-04-29 |
| `docs/05-habr-projects/01-synthesis.md` | 184 | 2026-04-29 |
| `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` | 187 | 2026-04-29 |
| `docs/02-anthropic-vacancies/47-native-format.md` | 187 | 2026-04-29 |
| `docs/02-anthropic-vacancies/04-abstract.md` | 188 | 2026-04-29 |
| `docs/02-anthropic-vacancies/253-table-of-contents.md` | 189 | 2026-04-29 |
| `docs/02-anthropic-vacancies/63-history.md` | 189 | 2026-04-29 |
| `docs/02-anthropic-vacancies/203-благодарности.md` | 191 | 2026-04-29 |
| `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` | 192 | 2026-04-29 |
| `docs/02-anthropic-vacancies/244-благодарности.md` | 193 | 2026-04-29 |
| `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` | 193 | 2026-04-29 |
| `docs/02-anthropic-vacancies/57-native-format.md` | 193 | 2026-04-29 |
| `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` | 194 | 2026-04-29 |
| `docs/02-anthropic-vacancies/56-essence.md` | 194 | 2026-04-29 |
| `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` | 195 | 2026-04-29 |
| `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` | 195 | 2026-04-29 |
| `docs/02-anthropic-vacancies/211-table-of-contents.md` | 196 | 2026-04-29 |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | 197 | 2026-04-29 |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | 197 | 2026-04-29 |
| `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` | 197 | 2026-04-29 |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 198 | 2026-04-29 |
| `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` | 198 | 2026-04-29 |
| `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | 198 | 2026-04-29 |
| `docs/02-anthropic-vacancies/320-references.md` | 199 | 2026-04-29 |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 200 | 2026-04-29 |
| `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` | 201 | 2026-04-29 |
| `docs/02-anthropic-vacancies/338-ссылки.md` | 201 | 2026-04-29 |
| `docs/02-anthropic-vacancies/53-history.md` | 201 | 2026-04-29 |
| `docs/02-anthropic-vacancies/128-доступные-инструменты.md` | 204 | 2026-04-29 |
| `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` | 204 | 2026-04-29 |
| `docs/02-anthropic-vacancies/130-отладка.md` | 205 | 2026-04-29 |
| `docs/02-anthropic-vacancies/308-table-of-contents.md` | 206 | 2026-04-29 |
| `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | 206 | 2026-04-29 |
| `docs/02-anthropic-vacancies/48-content-overview.md` | 206 | 2026-04-29 |
| `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` | 211 | 2026-04-29 |
| `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` | 211 | 2026-04-29 |
| `docs/02-anthropic-vacancies/40-bridges.md` | 211 | 2026-04-29 |
| `docs/02-anthropic-vacancies/50-bridges.md` | 211 | 2026-04-29 |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | 212 | 2026-04-29 |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 212 | 2026-04-29 |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | 216 | 2026-04-29 |
| `docs/02-anthropic-vacancies/224-acknowledgments.md` | 219 | 2026-04-29 |
| `docs/02-anthropic-vacancies/345-кто-ты.md` | 220 | 2026-04-29 |
| `docs/02-anthropic-vacancies/349-твоя-личность.md` | 223 | 2026-04-29 |
| `docs/02-anthropic-vacancies/301-благодарности.md` | 231 | 2026-04-29 |
| `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` | 232 | 2026-04-29 |
| `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` | 232 | 2026-04-29 |
| `docs/02-anthropic-vacancies/356-твой-workflow.md` | 232 | 2026-04-29 |
| `docs/02-anthropic-vacancies/37-native-format.md` | 234 | 2026-04-29 |
| `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` | 235 | 2026-04-29 |
| `docs/02-anthropic-vacancies/21-9-query-flow.md` | 237 | 2026-04-29 |
| `docs/02-anthropic-vacancies/24-12-versioning-policy.md` | 237 | 2026-04-29 |
| `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` | 238 | 2026-04-29 |
| `docs/02-anthropic-vacancies/300-заключение.md` | 239 | 2026-04-29 |
| `docs/02-anthropic-vacancies/302-ссылки.md` | 239 | 2026-04-29 |
| `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` | 240 | 2026-04-29 |
| `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` | 240 | 2026-04-29 |
| `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` | 240 | 2026-04-29 |
| `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` | 241 | 2026-04-29 |
| `docs/02-anthropic-vacancies/93-18-reference-implementation.md` | 243 | 2026-04-29 |
| `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` | 244 | 2026-04-29 |
| `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` | 244 | 2026-04-29 |
| `docs/02-anthropic-vacancies/182-acknowledgments.md` | 245 | 2026-04-29 |
| `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` | 247 | 2026-04-29 |
| `docs/02-anthropic-vacancies/23-11-security-considerations.md` | 248 | 2026-04-29 |
| `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` | 250 | 2026-04-29 |
| `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` | 251 | 2026-04-29 |
| `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` | 257 | 2026-04-29 |
| `docs/03-technology-combinations/01-agent-routing.md` | 257 | 2026-04-29 |
| `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` | 258 | 2026-04-29 |
| `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` | 258 | 2026-04-29 |
| `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` | 259 | 2026-04-29 |
| `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` | 260 | 2026-04-29 |
| `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` | 260 | 2026-04-29 |
| `docs/02-anthropic-vacancies/74-abstract.md` | 260 | 2026-04-29 |
| `docs/02-anthropic-vacancies/286-acknowledgments.md` | 263 | 2026-04-29 |
| `docs/02-anthropic-vacancies/285-closing.md` | 270 | 2026-04-29 |
| `docs/02-anthropic-vacancies/146-acknowledgments.md` | 273 | 2026-04-29 |
| `docs/02-anthropic-vacancies/111-4-условия-применимости.md` | 279 | 2026-04-29 |
| `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | 279 | 2026-04-29 |
| `docs/02-anthropic-vacancies/181-12-closing.md` | 281 | 2026-04-29 |
| `docs/02-anthropic-vacancies/189-аннотация.md` | 281 | 2026-04-29 |
| `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` | 282 | 2026-04-29 |
| `docs/02-anthropic-vacancies/85-10-query-flow.md` | 283 | 2026-04-29 |
| `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | 288 | 2026-04-29 |
| `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | 289 | 2026-04-29 |
| `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` | 291 | 2026-04-29 |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | 292 | 2026-04-29 |
| `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` | 293 | 2026-04-29 |
| `docs/02-anthropic-vacancies/92-17-versioning-policy.md` | 294 | 2026-04-29 |
| `docs/02-anthropic-vacancies/287-references.md` | 295 | 2026-04-29 |
| `docs/02-anthropic-vacancies/267-acknowledgments.md` | 297 | 2026-04-29 |
| `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` | 300 | 2026-04-29 |
| `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` | 302 | 2026-04-29 |
| `docs/05-habr-projects/02-collaboration-partners.md` | 303 | 2026-04-29 |
| `docs/02-anthropic-vacancies/204-ссылки.md` | 306 | 2026-04-29 |
| `docs/02-anthropic-vacancies/230-аннотация.md` | 310 | 2026-04-29 |
| `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` | 310 | 2026-04-29 |
| `docs/02-anthropic-vacancies/07-2-terminology.md` | 313 | 2026-04-29 |
| `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` | 313 | 2026-04-29 |
| `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | 313 | 2026-04-29 |
| `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` | 314 | 2026-04-29 |
| `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` | 316 | 2026-04-29 |
| `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` | 317 | 2026-04-29 |
| `docs/02-anthropic-vacancies/325-аннотация.md` | 317 | 2026-04-29 |
| `docs/02-anthropic-vacancies/183-references.md` | 322 | 2026-04-29 |
| `docs/02-anthropic-vacancies/307-abstract.md` | 323 | 2026-04-29 |
| `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` | 325 | 2026-04-29 |
| `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` | 325 | 2026-04-29 |
| `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` | 327 | 2026-04-29 |
| `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` | 331 | 2026-04-29 |
| `docs/02-anthropic-vacancies/245-ссылки.md` | 331 | 2026-04-29 |
| `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` | 332 | 2026-04-29 |
| `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` | 332 | 2026-04-29 |
| `docs/02-anthropic-vacancies/168-abstract.md` | 334 | 2026-04-29 |
| `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` | 335 | 2026-04-29 |
| `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` | 338 | 2026-04-29 |
| `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` | 338 | 2026-04-29 |
| `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` | 340 | 2026-04-29 |
| `docs/02-anthropic-vacancies/252-abstract.md` | 347 | 2026-04-29 |
| `docs/02-anthropic-vacancies/210-abstract.md` | 349 | 2026-04-29 |
| `docs/02-anthropic-vacancies/147-references.md` | 350 | 2026-04-29 |
| `docs/02-anthropic-vacancies/275-why-this-document-exists.md` | 350 | 2026-04-29 |
| `docs/02-anthropic-vacancies/225-references.md` | 351 | 2026-04-29 |
| `docs/02-anthropic-vacancies/337-благодарности.md` | 351 | 2026-04-29 |
| `docs/02-anthropic-vacancies/90-15-security-considerations.md` | 354 | 2026-04-29 |
| `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` | 357 | 2026-04-29 |
| `docs/01-svyazi/08-conclusions.md` | 360 | 2026-04-29 |
| `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` | 364 | 2026-04-29 |
| `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` | 366 | 2026-04-29 |
| `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` | 366 | 2026-04-29 |
| `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | 367 | 2026-04-29 |
| `docs/02-anthropic-vacancies/153-executive-summary.md` | 370 | 2026-04-29 |
| `docs/02-anthropic-vacancies/281-the-recursive-insight.md` | 371 | 2026-04-29 |
| `docs/02-anthropic-vacancies/243-12-заключение.md` | 375 | 2026-04-29 |
| `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` | 378 | 2026-04-29 |
| `docs/02-anthropic-vacancies/06-1-introduction.md` | 380 | 2026-04-29 |
| `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` | 380 | 2026-04-29 |
| `docs/02-anthropic-vacancies/319-acknowledgments.md` | 384 | 2026-04-29 |
| `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` | 386 | 2026-04-29 |
| `docs/03-technology-combinations/03-local-first.md` | 386 | 2026-04-29 |
| `docs/02-anthropic-vacancies/136-abstract.md` | 388 | 2026-04-29 |
| `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | 392 | 2026-04-29 |
| `docs/02-anthropic-vacancies/81-6-adapter-interface.md` | 392 | 2026-04-29 |
| `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` | 399 | 2026-04-29 |
| `docs/02-anthropic-vacancies/77-2-terminology.md` | 403 | 2026-04-29 |
| `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` | 406 | 2026-04-29 |
| `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` | 407 | 2026-04-29 |
| `docs/02-anthropic-vacancies/223-12-closing.md` | 409 | 2026-04-29 |
| `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` | 411 | 2026-04-29 |
| `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` | 412 | 2026-04-29 |
| `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | 412 | 2026-04-29 |
| `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` | 414 | 2026-04-29 |
| `docs/02-anthropic-vacancies/268-references.md` | 416 | 2026-04-29 |
| `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` | 419 | 2026-04-29 |
| `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` | 422 | 2026-04-29 |
| `docs/02-anthropic-vacancies/18-6-adapter-interface.md` | 425 | 2026-04-29 |
| `docs/01-svyazi/02-methodology.md` | 428 | 2026-04-29 |
| `docs/02-anthropic-vacancies/266-13-closing.md` | 434 | 2026-04-29 |
| `docs/02-anthropic-vacancies/179-10-open-questions.md` | 446 | 2026-04-29 |
| `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` | 447 | 2026-04-29 |
| `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` | 447 | 2026-04-29 |
| `docs/02-anthropic-vacancies/221-10-open-questions.md` | 460 | 2026-04-29 |
| `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` | 472 | 2026-04-29 |
| `docs/02-anthropic-vacancies/76-1-introduction.md` | 473 | 2026-04-29 |
| `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` | 477 | 2026-04-29 |
| `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` | 479 | 2026-04-29 |
| `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` | 479 | 2026-04-29 |
| `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | 486 | 2026-04-29 |
| `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` | 488 | 2026-04-29 |
| `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` | 492 | 2026-04-29 |
| `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | 492 | 2026-04-29 |
| `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | 495 | 2026-04-29 |
| `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` | 495 | 2026-04-29 |
| `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` | 507 | 2026-04-29 |
| `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` | 513 | 2026-04-29 |
| `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` | 541 | 2026-04-29 |
| `docs/04-ai-collaborations/07-выводы.md` | 542 | 2026-04-29 |
| `docs/02-anthropic-vacancies/294-существующие-приближения.md` | 565 | 2026-04-29 |
| `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` | 583 | 2026-04-29 |
| `docs/02-anthropic-vacancies/279-existing-approximations.md` | 588 | 2026-04-29 |
| `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` | 592 | 2026-04-29 |
| `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` | 595 | 2026-04-29 |
| `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` | 596 | 2026-04-29 |
| `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` | 596 | 2026-04-29 |
| `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` | 610 | 2026-04-29 |
| `docs/02-anthropic-vacancies/175-6-ethical-framework.md` | 611 | 2026-04-29 |
| `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` | 620 | 2026-04-29 |
| `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` | 625 | 2026-04-29 |
| `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` | 625 | 2026-04-29 |
| `docs/02-anthropic-vacancies/155-1-problem-statement.md` | 632 | 2026-04-29 |
| `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` | 634 | 2026-04-29 |
| `docs/01-svyazi/14-limitations.md` | 636 | 2026-04-29 |
| `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` | 636 | 2026-04-29 |
| `docs/02-anthropic-vacancies/264-11-open-questions.md` | 638 | 2026-04-29 |
| `docs/04-ai-collaborations/01-executive-summary.md` | 647 | 2026-04-29 |
| `docs/02-anthropic-vacancies/162-8-risk-analysis.md` | 653 | 2026-04-29 |
| `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` | 653 | 2026-04-29 |
| `docs/02-anthropic-vacancies/159-5-economic-model.md` | 654 | 2026-04-29 |
| `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` | 662 | 2026-04-29 |
| `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` | 663 | 2026-04-29 |
| `docs/02-anthropic-vacancies/174-5-architectural-specification.md` | 665 | 2026-04-29 |
| `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` | 666 | 2026-04-29 |
| `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` | 666 | 2026-04-29 |
| `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` | 667 | 2026-04-29 |
| `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` | 672 | 2026-04-29 |
| `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` | 674 | 2026-04-29 |
| `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` | 675 | 2026-04-29 |
| `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` | 677 | 2026-04-29 |
| `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | 678 | 2026-04-29 |
| `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` | 678 | 2026-04-29 |
| `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` | 679 | 2026-04-29 |
| `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` | 681 | 2026-04-29 |
| `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` | 682 | 2026-04-29 |
| `docs/02-anthropic-vacancies/156-2-target-populations.md` | 683 | 2026-04-29 |
| `docs/02-anthropic-vacancies/238-7-области-применения.md` | 683 | 2026-04-29 |
| `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` | 689 | 2026-04-29 |
| `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` | 696 | 2026-04-29 |
| `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` | 697 | 2026-04-29 |
| `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` | 698 | 2026-04-29 |
| `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` | 698 | 2026-04-29 |
| `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` | 707 | 2026-04-29 |
| `docs/01-svyazi/01-executive-summary.md` | 708 | 2026-04-29 |
| `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` | 713 | 2026-04-29 |
| `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` | 714 | 2026-04-29 |
| `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` | 721 | 2026-04-29 |
| `docs/01-svyazi/12-roadmap.md` | 733 | 2026-04-29 |
| `docs/02-anthropic-vacancies/218-7-application-domains.md` | 743 | 2026-04-29 |
| `docs/01-svyazi/11-integration-contracts.md` | 745 | 2026-04-29 |
| `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` | 745 | 2026-04-29 |
| `docs/02-anthropic-vacancies/145-8-call-to-action.md` | 746 | 2026-04-29 |
| `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` | 749 | 2026-04-29 |
| `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` | 749 | 2026-04-29 |
| `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` | 750 | 2026-04-29 |
| `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | 751 | 2026-04-29 |
| `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` | 753 | 2026-04-29 |
| `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` | 755 | 2026-04-29 |
| `docs/01-svyazi/09-architectural-gaps.md` | 757 | 2026-04-29 |
| `docs/03-technology-combinations/02-knowledge-graphs.md` | 766 | 2026-04-29 |
| `docs/02-anthropic-vacancies/144-7-open-questions.md` | 777 | 2026-04-29 |
| `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | 782 | 2026-04-29 |
| `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` | 788 | 2026-04-29 |
| `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` | 790 | 2026-04-29 |
| `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` | 803 | 2026-04-29 |
| `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` | 804 | 2026-04-29 |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | 804 | 2026-04-29 |
| `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` | 807 | 2026-04-29 |
| `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` | 810 | 2026-04-29 |
| `docs/01-svyazi/06-security-privacy.md` | 821 | 2026-04-29 |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | 821 | 2026-04-29 |
| `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` | 823 | 2026-04-29 |
| `docs/01-svyazi/13-contacts.md` | 827 | 2026-04-29 |
| `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` | 828 | 2026-04-29 |
| `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` | 844 | 2026-04-29 |
| `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` | 845 | 2026-04-29 |
| `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | 855 | 2026-04-29 |
| `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | 862 | 2026-04-29 |
| `docs/03-technology-combinations/05-benchmarks.md` | 863 | 2026-04-29 |
| `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` | 867 | 2026-04-29 |
| `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` | 868 | 2026-04-29 |
| `docs/02-anthropic-vacancies/68-about.md` | 880 | 2026-04-29 |
| `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | 885 | 2026-04-29 |
| `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` | 888 | 2026-04-29 |
| `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | 900 | 2026-04-29 |
| `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` | 901 | 2026-04-29 |
| `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 901 | 2026-04-29 |
| `docs/01-svyazi/10-second-order-ensembles.md` | 916 | 2026-04-29 |
| `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 928 | 2026-04-29 |
| `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | 930 | 2026-04-29 |
| `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` | 946 | 2026-04-29 |
| `docs/02-anthropic-vacancies/104-appendix-c-references.md` | 947 | 2026-04-29 |
| `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 956 | 2026-04-29 |
| `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 966 | 2026-04-29 |
| `docs/02-anthropic-vacancies/164-10-appendices.md` | 970 | 2026-04-29 |
| `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` | 973 | 2026-04-29 |
| `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` | 974 | 2026-04-29 |
| `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` | 978 | 2026-04-29 |
| `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` | 1001 | 2026-04-29 |
| `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` | 1014 | 2026-04-29 |
| `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | 1062 | 2026-04-29 |
| `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` | 1078 | 2026-04-29 |
| `docs/01-svyazi/07-mvp-planning.md` | 1083 | 2026-04-29 |
| `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` | 1125 | 2026-04-29 |
| `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` | 1209 | 2026-04-29 |
| `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 1212 | 2026-04-29 |
| `docs/01-svyazi/04-ensembles-overview.md` | 1274 | 2026-04-29 |
| `docs/02-anthropic-vacancies/122-глоссарий.md` | 1302 | 2026-04-29 |
| `docs/01-svyazi/03-component-catalog.md` | 1395 | 2026-04-29 |
| `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` | 1418 | 2026-04-29 |
| `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` | 1459 | 2026-04-29 |
| `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` | 1549 | 2026-04-29 |
| `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 1553 | 2026-04-29 |
| `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` | 1570 | 2026-04-29 |
| `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` | 1582 | 2026-04-29 |
| `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` | 1730 | 2026-04-29 |
| `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` | 2024 | 2026-04-29 |
| `docs/02-anthropic-vacancies/123-portal-mcp-py.md` | 2316 | 2026-04-29 |
| `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` | 3181 | 2026-04-29 |
| `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 3362 | 2026-04-29 |
| `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | 3425 | 2026-04-29 |
| `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 3835 | 2026-04-29 |
| `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` | 3851 | 2026-04-29 |
| `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` | 4049 | 2026-04-29 |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | 4385 | 2026-04-29 |
| `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` | 5807 | 2026-04-29 |
| `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` | 7108 | 2026-04-29 |
| `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` | 8397 | 2026-04-29 |
| `docs/02-anthropic-vacancies/00-intro.md` | 8884 | 2026-04-29 |
| `docs/02-anthropic-vacancies/165-closing.md` | 9251 | 2026-04-29 |
| `docs/02-anthropic-vacancies/69-section.md` | 9520 | 2026-04-29 |
| `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` | 11237 | 2026-04-29 |
| `docs/04-ai-collaborations/00-intro.md` | 11445 | 2026-04-29 |
| `docs/02-anthropic-vacancies/133-обратная-связь.md` | 16959 | 2026-04-29 |
| `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` | 19103 | 2026-04-29 |
| `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` | 20414 | 2026-04-29 |


### 210. Без метаданных (нет summary или тегов) — 68 файлов
_Файл: `docs/obsidian/STALENESS.md` | 3 колонок, 20 строк_

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/00-intro-part2.md` | 5 | нет summary, нет тегов, короткий (5 слов) |
| `docs/01-svyazi/QA.md` | 255 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | нет summary, нет тегов, короткий (14 слов) |
| `docs/02-anthropic-vacancies/QA.md` | 360 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/03-technology-combinations/README.md` | 38 | нет тегов, короткий (38 слов) |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/04-ai-collaborations/README.md` | 82 | нет summary, нет тегов, короткий (82 слов) |
| `docs/05-habr-projects/QA.md` | 111 | нет summary, нет тегов |
| `docs/05-habr-projects/README.md` | 38 | нет summary, нет тегов, короткий (38 слов) |
| `docs/05-habr-projects/knowledge/README.md` | 9 | нет summary, нет тегов, короткий (9 слов) |
| `docs/05-habr-projects/memory/README.md` | 17 | нет summary, нет тегов, короткий (17 слов) |
| `docs/ABBREVIATIONS.md` | 1030 | нет summary, нет тегов |
| `docs/ACTION_ITEMS.md` | 4906 | нет summary |
| `docs/ALERTS.md` | 50 | нет summary, нет тегов, короткий (50 слов) |
| `docs/AUTHORS.md` | 81 | нет summary, нет тегов, короткий (81 слов) |
| `docs/BACKLINKS.md` | 194 | нет summary, нет тегов |
| `docs/BROKEN_LINKS.md` | 468 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 829 | нет summary, нет тегов |
| `docs/CODE_BLOCKS.md` | 3446 | нет summary, нет тегов |


### 211. Короткие (< 100 слов, заготовки) — 22 файлов
_Файл: `docs/obsidian/STALENESS.md` | 2 колонок, 20 строк_

| Файл | Слов |
|------|------|
| `docs/01-svyazi/README.md` | 86 |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 52 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 87 |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 66 |
| `docs/02-anthropic-vacancies/16-history.md` | 90 |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 96 |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 94 |
| `docs/autofilled/components/.md` | 77 |
| `docs/autofilled/components/cowork.md` | 77 |
| `docs/autofilled/components/ingit.md` | 77 |
| `docs/autofilled/components/kksudo.md` | 62 |
| `docs/autofilled/components/lorenzo.md` | 77 |
| `docs/autofilled/components/nautilus.md` | 77 |
| `docs/autofilled/components/sgb.md` | 77 |
| `docs/autofilled/components/spbmolot.md` | 62 |
| `docs/autofilled/components/svend4.md` | 77 |
| `docs/autofilled/components/svyazi.md` | 77 |
| `docs/templates/contact-outreach.md` | 96 |
| `docs/templates/decision-record.md` | 62 |
| `docs/templates/ensemble.md` | 93 |


### 212. Сводная таблица по разделам
_Файл: `docs/obsidian/STATS.md` | 8 колонок, 11 строк_

| Раздел | Файлов | Слов | H2 | Таблиц | Блоков кода | Ссылок | Жирного |
|--------|--------|------|----|--------|-------------|--------|---------|
| **01-svyazi** | 16 | 11,039 | 75 | 43 | 8 | 257 | 281 |
| **02-anthropic-vacancies** | 357 | 284,026 | 1266 | 130 | 185 | 7028 | 3557 |
| **03-technology-combinations** | 7 | 2,600 | 19 | 5 | 0 | 65 | 22 |
| **04-ai-collaborations** | 17 | 27,180 | 89 | 89 | 0 | 349 | 360 |
| **05-habr-projects** | 10 | 8,981 | 32 | 18 | 0 | 156 | 54 |
| **autofilled** | 13 | 978 | 40 | 0 | 0 | 157 | 64 |
| **badges** | 1 | 44 | 2 | 0 | 1 | 14 | 0 |
| **contacts** | 15 | 3,818 | 88 | 56 | 14 | 283 | 43 |
| **root** | 82 | 190,409 | 521 | 5410 | 107 | 6042 | 4086 |
| **templates** | 6 | 635 | 27 | 13 | 4 | 25 | 14 |
| **ИТОГО** | **524** | **529,710** | **2159** | **5764** | **319** | **14376** | **8481** |


### 213. Топ-20 файлов по объёму
_Файл: `docs/obsidian/STATS.md` | 5 колонок, 20 строк_

| Файл | Слов | H2 | Таблиц | Код |
|------|------|----|--------|-----|
| `TABLES` | 63292 | 8 | 2738 | 1 |
| `341-приложение-c-образец-спецификаций-ин` | 20414 | 4 | 0 | 11 |
| `01-интегральный-анализ-профиля-svend4` | 19103 | 4 | 0 | 19 |
| `133-обратная-связь` | 16959 | 4 | 6 | 17 |
| `OUTLINE` | 14163 | 13 | 0 | 0 |
| `00-intro` | 11445 | 4 | 3 | 0 |
| `CONCEPTS` | 11402 | 55 | 0 | 0 |
| `342-что-такое-вариант-c-concept-document` | 11237 | 4 | 0 | 6 |
| `69-section` | 9520 | 4 | 2 | 18 |
| `165-closing` | 9251 | 4 | 0 | 1 |
| `00-intro` | 8884 | 3 | 4 | 2 |
| `PARAGRAPH_QUALITY` | 8527 | 5 | 3 | 0 |
| `150-appendix-c-version-history` | 8397 | 4 | 0 | 2 |
| `READABILITY` | 7981 | 2 | 262 | 0 |
| `memnet` | 7271 | 4 | 3 | 0 |
| `303-приложение-визуализация-позиции-в-се` | 7108 | 4 | 0 | 2 |
| `ACTION_ITEMS` | 6656 | 6 | 0 | 0 |
| `READING_ORDER` | 5947 | 1 | 198 | 0 |
| `343-lorenzo-catalyst-agent-глубокая-прор` | 5807 | 4 | 0 | 2 |
| `READING_TIME` | 5485 | 5 | 237 | 0 |


### 214. 🟢 ADOPT
_Файл: `docs/obsidian/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **MCP Protocol** | Инструменты | Стандарт интеграции AI-инструментов — Anthropic |
| **CardIndex** | Компоненты | 785+ карточек знаний, MIT, стабильный API |
| **AgentFS** | Компоненты | Файловая система для AI-агентов, MIT, kksudo |
| **Firecrawl** | Инструменты | Веб-краулер для AI, MIT, активная разработка |
| **Python 3.11+** | Платформа | Основной язык реализации всех компонентов |
| **Markdown docs** | Практики | 96% готовности, проверено на 460+ файлах |


### 215. 🟢 ADOPT
_Файл: `docs/obsidian/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **Yodoca** | Компоненты | Память с консолидацией, Apache 2.0, spbmolot |
| **SENTINEL** | Компоненты | Allowlist безопасности для MCP |
| **Rufler** | Компоненты | Оркестратор агентов, активная разработка |
| **RAG + Graph** | Архитектура | Гибридный поиск: векторный + граф-обход |
| **claude-haiku-4-5** | Модели | Оптимум цена/качество для enrichment задач |
| **CRDT-синхронизация** | Архитектура | Бесконфликтная репликация для multi-agent |


### 216. 🟢 ADOPT
_Файл: `docs/obsidian/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **NGT-memory** | Компоненты | Ассоциативный граф памяти, BSL 1.1 |
| **knowledge-space** | Компоненты | База знаний, MIT, нужна оценка API |
| **Wikontic** | Компоненты | Граф знаний, статус неизвестен |
| **MCP Tool Search** | Компоненты | Динамический поиск инструментов |
| **claude-opus-4-7** | Модели | Для сложных reasoning задач, высокая стоимость |
| **Local-first P2P** | Архитектура | GDPR-safe распределённые данные |


### 217. 🟢 ADOPT
_Файл: `docs/obsidian/TECH_RADAR.md` | 3 колонок, 4 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **BSL 1.1 libs** | Лицензии | Ограничения при коммерческом использовании |
| **Monolithic LLM** | Архитектура | Один LLM вместо ансамбля — узкое место |
| **Без PII-защиты** | Практики | Обработка данных без SENTINEL/quarantine |
| **Hard-coded prompts** | Практики | Промпты без версионирования и тестов |


### 218. Топ уникальных слов по темам
_Файл: `docs/obsidian/TOPIC_MODEL.md` | 6 колонок, 6 строк_

| Тема | Слово 1 | Слово 2 | Слово 3 | Слово 4 | Слово 5 |
|------|---------|---------|---------|---------|---------|
| turn, view, cite | turn | appendix | svyazi | view | portal |
| cowork, ingit, compo | cowork | ingit | agent | composite | agents |
| middle, ensembl, lay | layer | chat | middle | missing | between |
| агент, совместной, к | агенты | коллеги | профессиональные | благодарности | совместной |
| compatibility, level | compatibility | level | bridges | history | format |
| слов, файлов, файлы | слов | файлов | тегов | callout | summary |


### 219. Сводка
_Файл: `docs/obsidian/VALIDATION.md` | 3 колонок, 6 строк_

| Проверка | Статус | Проблем |
|----------|--------|---------|
| Разделы и README | ✅ | 0 |
| Мета-файлы | ✅ | 0 |
| Пустые/короткие файлы | ⚠️ | 6 |
| Именование файлов | ✅ | 10 |
| Заголовки H1 | ⚠️ | 11 |
| Внутренние ссылки | ✅ | 15 |


### 220. 📝 Изменённые файлы (16)
_Файл: `docs/obsidian/VERSION_DIFF.md` | 4 колонок, 16 строк_

| Файл | Δ слов | Добавленные темы | Удалённые темы |
|------|--------|------------------|----------------|
| `docs/TIMELINE.md` | -2390 | 2020 (2 упоминаний), 2021 (1 упоминаний), 2022 (5 упоминаний) +7 | Версия (394), Год (27), Длительность (95) +6 |
| `docs/SEARCH.md` | +316 | — | — |
| `docs/BROKEN_LINKS.md` | +273 | Внешние URL (129 уникальных) | Внешние URL (113 уникальных) |
| `docs/DUPLICATES.md` | +81 | 50% — `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` vs `docs/01-svyazi/06-security-privacy.md`, 50% — `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` vs `docs/01-svyazi/12-roadmap.md` | — |
| `docs/PROGRESS.md` | -26 | Метрики качества, Приоритет 1: kksudo (AgentFS, 13 упоминаний), Приоритет 2: spbmolot (NGT Memory, 12 упоминаний) +3 | Ближайшие задачи (открытые чеклисты), Чеклисты по фазам |
| `docs/05-habr-projects/memory/memnet.md` | +22 | Статус | — |
| `docs/05-habr-projects/memory/ngt-memory.md` | +22 | Статус | — |
| `docs/05-habr-projects/memory/yodoca.md` | +22 | Статус | — |
| `docs/METRICS.md` | -22 | — | — |
| `docs/04-ai-collaborations/00-intro.md` | +16 | Статус | — |
| `docs/04-ai-collaborations/01-executive-summary.md` | +16 | Статус | — |
| `docs/05-habr-projects/01-synthesis.md` | +16 | Статус | — |
| `docs/05-habr-projects/02-collaboration-partners.md` | +16 | Статус | — |
| `docs/05-habr-projects/knowledge/wikontic.md` | +16 | Статус | — |
| `docs/HEALTH.md` | -13 | — | — |
| `docs/CONTACTS.md` | -9 | — | — |


### 221. Корпусная статистика
_Файл: `docs/obsidian/VOCABULARY.md` | 2 колонок, 5 строк_

| Метрика | Значение |
|---------|----------|
| Средний TTR | 0.434 |
| Средний STTR (100-токенное окно) | 0.589 |
| Lexical density | 0.835 |
| Средняя длина слова | 6.58 |
| Общая оценка | 🟠 Бедный |


### 222. Топ файлов по богатству словаря (STTR)
_Файл: `docs/obsidian/VOCABULARY.md` | 6 колонок, 30 строк_

| Файл | STTR | TTR | Hapax% | Lex.Density | Токенов |
|------|------|-----|--------|-------------|---------|
| `ABBREVIATIONS.md` | 0.940 | 0.717 | 75% | 0.875 | 835 |
| `HEALTH.md` | 0.909 | 0.909 | 90% | 0.955 | 66 |
| `ENTITIES.md` | 0.880 | 0.609 | 78% | 0.957 | 161 |
| `194-4-десять-областей-применения.md` | 0.874 | 0.556 | 70% | 0.915 | 1459 |
| `00-intro.md` | 0.856 | 0.370 | 60% | 0.870 | 10587 |
| `01-интегральный-анализ-профиля-svend4.md` | 0.850 | 0.332 | 60% | 0.831 | 17176 |
| `238-7-области-применения.md` | 0.847 | 0.607 | 70% | 0.944 | 629 |
| `14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 0.840 | 0.462 | 65% | 0.884 | 3237 |
| `STATS.md` | 0.840 | 0.840 | 88% | 0.934 | 106 |
| `memnet.md` | 0.836 | 0.399 | 61% | 0.866 | 6697 |
| `189-аннотация.md` | 0.830 | 0.713 | 76% | 0.840 | 275 |
| `192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | 0.830 | 0.620 | 76% | 0.885 | 786 |
| `165-closing.md` | 0.825 | 0.412 | 63% | 0.814 | 6087 |
| `239-8-пилотное-предложение-sgb-колega-адвокат.md` | 0.824 | 0.617 | 73% | 0.899 | 799 |
| `00-intro.md` | 0.822 | 0.396 | 64% | 0.859 | 7760 |
| `72-расписание-фазы-3.md` | 0.822 | 0.604 | 74% | 0.842 | 671 |
| `357-твоя-коммуникация-в-outreach.md` | 0.820 | 0.720 | 78% | 0.850 | 193 |
| `DECISIONS.md` | 0.817 | 0.564 | 73% | 0.864 | 1609 |
| `207-приложение-c-образцы-случаев-использования-в-детал.md` | 0.812 | 0.507 | 68% | 0.846 | 2290 |
| `DEPENDABOT.md` | 0.810 | 0.810 | 81% | 0.914 | 58 |
| `359-твои-anti-patterns.md` | 0.810 | 0.660 | 66% | 0.846 | 162 |
| `365-развёрнутый-анализ-внуковой-комбинации.md` | 0.810 | 0.399 | 59% | 0.859 | 3565 |
| `235-4-архитектура-профессиональных-коллег-агентов.md` | 0.807 | 0.601 | 73% | 0.893 | 785 |
| `191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | 0.805 | 0.637 | 76% | 0.843 | 650 |
| `272-appendix-d-connection-diagram.md` | 0.805 | 0.429 | 64% | 0.808 | 3465 |
| `173-4-ten-domains-of-application.md` | 0.805 | 0.418 | 59% | 0.856 | 1556 |
| `248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | 0.804 | 0.450 | 66% | 0.856 | 2999 |
| `02-общий-план-развития-nautilus-portal-protocol.md` | 0.802 | 0.468 | 67% | 0.845 | 2142 |
| `150-appendix-c-version-history.md` | 0.802 | 0.409 | 60% | 0.839 | 4478 |
| `SENTIMENT.md` | 0.800 | 0.675 | 81% | 0.899 | 169 |


### 223. Файлы с бедным словарём (требуют доработки)
_Файл: `docs/obsidian/VOCABULARY.md` | 4 колонок, 30 строк_

| Файл | STTR | Оценка | Токенов |
|------|------|--------|---------|
| `28-appendix-a-minimal-working-example.md` | 0.270 | 🔴 Очень бедный | 213 |
| `README.md` | 0.273 | 🔴 Очень бедный | 77 |
| `BROKEN_LINKS.md` | 0.273 | 🔴 Очень бедный | 783 |
| `README.md` | 0.275 | 🔴 Очень бедный | 51 |
| `305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | 0.280 | 🔴 Очень бедный | 221 |
| `249-composite-skills-agent-md.md` | 0.305 | 🔴 Очень бедный | 249 |
| `.md` | 0.305 | 🔴 Очень бедный | 95 |
| `svyazi.md` | 0.312 | 🔴 Очень бедный | 93 |
| `svend4.md` | 0.312 | 🔴 Очень бедный | 93 |
| `sgb.md` | 0.312 | 🔴 Очень бедный | 93 |
| `nautilus.md` | 0.312 | 🔴 Очень бедный | 93 |
| `lorenzo.md` | 0.312 | 🔴 Очень бедный | 93 |
| `ingit.md` | 0.312 | 🔴 Очень бедный | 93 |
| `cowork.md` | 0.312 | 🔴 Очень бедный | 93 |
| `273-infrastructure-for-ai-collaborative-intellectual-w.md` | 0.320 | 🔴 Очень бедный | 251 |
| `README.md` | 0.323 | 🔴 Очень бедный | 65 |
| `27-15-glossary-of-examples.md` | 0.325 | 🔴 Очень бедный | 208 |
| `DEPENDENCY_MAP.md` | 0.328 | 🔴 Очень бедный | 848 |
| `CITATION_INDEX.md` | 0.328 | 🔴 Очень бедный | 453 |
| `304-ingit-as-cowork-native-workspace-substrate-md.md` | 0.330 | 🔴 Очень бедный | 249 |
| `187-слой-представительских-агентов-md.md` | 0.330 | 🔴 Очень бедный | 250 |
| `169-table-of-contents.md` | 0.330 | 🔴 Очень бедный | 216 |
| `151-open-knowledge-work-foundation-md.md` | 0.330 | 🔴 Очень бедный | 247 |
| `134-the-double-triangle-architecture-md.md` | 0.330 | 🔴 Очень бедный | 247 |
| `13-angle-perspective.md` | 0.330 | 🔴 Очень бедный | 185 |
| `CROSSREFS.md` | 0.331 | 🔴 Очень бедный | 825 |
| `42-author-contact.md` | 0.335 | 🔴 Очень бедный | 201 |
| `166-representative-agent-layer-md.md` | 0.335 | 🔴 Очень бедный | 255 |
| `123-portal-mcp-py.md` | 0.340 | 🔴 Очень бедный | 232 |
| `105-review-methodology-md.md` | 0.340 | 🔴 Очень бедный | 200 |


### 224. Топ-20 слов
_Файл: `docs/obsidian/WORD_CLOUD.md` | 3 колонок, 20 строк_

| # | Слово | Частота |
|---|-------|---------|
| 1 | **anthropic** | 5,050 |
| 2 | **vacancies** | 4,506 |
| 3 | **agent** | 1,422 |
| 4 | **turn** | 1,376 |
| 5 | **svyazi** | 1,039 |
| 6 | **сходство** | 1,007 |
| 7 | **view** | 973 |
| 8 | **cowork** | 926 |
| 9 | **nautilus** | 912 |
| 10 | **appendix** | 822 |
| 11 | **ingit** | 776 |
| 12 | **agents** | 701 |
| 13 | **knowledge** | 691 |
| 14 | **portal** | 659 |
| 15 | **protocol** | 617 |
| 16 | **search** | 604 |
| 17 | **document** | 599 |
| 18 | **memory** | 591 |
| 19 | **lorenzo** | 557 |
| 20 | **claude** | 556 |


### 225. Глобальный топ-50 слов
_Файл: `docs/obsidian/WORD_FREQ.md` | 4 колонок, 50 строк_

| # | Слово | Частота | Визуализация |
|---|-------|---------|-------------|
| 1 | **anthropic** | 11,655 | `████████████████████` |
| 2 | **vacancies** | 10,696 | `██████████████████░░` |
| 3 | **проблем** | 2,583 | `████░░░░░░░░░░░░░░░░` |
| 4 | **agent** | 1,786 | `███░░░░░░░░░░░░░░░░░` |
| 5 | **appendix** | 1,616 | `██░░░░░░░░░░░░░░░░░░` |
| 6 | **svyazi** | 1,615 | `██░░░░░░░░░░░░░░░░░░` |
| 7 | **turn** | 1,450 | `██░░░░░░░░░░░░░░░░░░` |
| 8 | **cowork** | 1,320 | `██░░░░░░░░░░░░░░░░░░` |
| 9 | **nautilus** | 1,239 | `██░░░░░░░░░░░░░░░░░░` |
| 10 | **документы** | 1,160 | `█░░░░░░░░░░░░░░░░░░░` |
| 11 | **ingit** | 1,143 | `█░░░░░░░░░░░░░░░░░░░` |
| 12 | **mcp** | 1,063 | `█░░░░░░░░░░░░░░░░░░░` |
| 13 | **view** | 1,063 | `█░░░░░░░░░░░░░░░░░░░` |
| 14 | **сходство** | 948 | `█░░░░░░░░░░░░░░░░░░░` |
| 15 | **knowledge** | 926 | `█░░░░░░░░░░░░░░░░░░░` |
| 16 | **agents** | 904 | `█░░░░░░░░░░░░░░░░░░░` |
| 17 | **анализ** | 884 | `█░░░░░░░░░░░░░░░░░░░` |
| 18 | **readme** | 841 | `█░░░░░░░░░░░░░░░░░░░` |
| 19 | **portal** | 838 | `█░░░░░░░░░░░░░░░░░░░` |
| 20 | **слов** | 822 | `█░░░░░░░░░░░░░░░░░░░` |
| 21 | **what** | 783 | `█░░░░░░░░░░░░░░░░░░░` |
| 22 | **document** | 778 | `█░░░░░░░░░░░░░░░░░░░` |
| 23 | **protocol** | 756 | `█░░░░░░░░░░░░░░░░░░░` |
| 24 | **layer** | 732 | `█░░░░░░░░░░░░░░░░░░░` |
| 25 | **lorenzo** | 697 | `█░░░░░░░░░░░░░░░░░░░` |
| 26 | **claude** | 691 | `█░░░░░░░░░░░░░░░░░░░` |
| 27 | **collaborations** | 683 | `█░░░░░░░░░░░░░░░░░░░` |
| 28 | **memory** | 679 | `█░░░░░░░░░░░░░░░░░░░` |
| 29 | **work** | 676 | `█░░░░░░░░░░░░░░░░░░░` |
| 30 | **open** | 675 | `█░░░░░░░░░░░░░░░░░░░` |
| 31 | **contents** | 627 | `█░░░░░░░░░░░░░░░░░░░` |
| 32 | **infrastructure** | 625 | `█░░░░░░░░░░░░░░░░░░░` |
| 33 | **search** | 623 | `█░░░░░░░░░░░░░░░░░░░` |
| 34 | **sgb** | 612 | `█░░░░░░░░░░░░░░░░░░░` |
| 35 | **svend** | 609 | `█░░░░░░░░░░░░░░░░░░░` |
| 36 | **architecture** | 598 | `█░░░░░░░░░░░░░░░░░░░` |
| 37 | **связанные** | 589 | `█░░░░░░░░░░░░░░░░░░░` |
| 38 | **агентов** | 556 | `░░░░░░░░░░░░░░░░░░░░` |
| 39 | **приложение** | 550 | `░░░░░░░░░░░░░░░░░░░░` |
| 40 | **упоминается** | 549 | `░░░░░░░░░░░░░░░░░░░░` |
| 41 | **сложный** | 540 | `░░░░░░░░░░░░░░░░░░░░` |
| 42 | **colleague** | 522 | `░░░░░░░░░░░░░░░░░░░░` |
| 43 | **cite** | 518 | `░░░░░░░░░░░░░░░░░░░░` |
| 44 | **professional** | 512 | `░░░░░░░░░░░░░░░░░░░░` |
| 45 | **абзац** | 511 | `░░░░░░░░░░░░░░░░░░░░` |
| 46 | **документ** | 496 | `░░░░░░░░░░░░░░░░░░░░` |
| 47 | **мин** | 492 | `░░░░░░░░░░░░░░░░░░░░` |
| 48 | **project** | 485 | `░░░░░░░░░░░░░░░░░░░░` |
| 49 | **содержание** | 482 | `░░░░░░░░░░░░░░░░░░░░` |
| 50 | **level** | 476 | `░░░░░░░░░░░░░░░░░░░░` |


### 226. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **turn** | 451 | `███████████████` |
| **view** | 310 | `██████████░░░░░` |
| **svyazi** | 205 | `██████░░░░░░░░░` |
| **cite** | 155 | `█████░░░░░░░░░░` |
| **search** | 153 | `█████░░░░░░░░░░` |
| **collaborations** | 100 | `███░░░░░░░░░░░░` |
| **memory** | 84 | `██░░░░░░░░░░░░░` |
| **проект** | 72 | `██░░░░░░░░░░░░░` |
| **rag** | 68 | `██░░░░░░░░░░░░░` |
| **ансамбли** | 67 | `██░░░░░░░░░░░░░` |
| **oss** | 66 | `██░░░░░░░░░░░░░` |
| **mcp** | 52 | `█░░░░░░░░░░░░░░` |
| **документы** | 50 | `█░░░░░░░░░░░░░░` |
| **agentfs** | 48 | `█░░░░░░░░░░░░░░` |
| **прототипа** | 45 | `█░░░░░░░░░░░░░░` |


### 227. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **anthropic** | 5239 | `███████████████` |
| **vacancies** | 4510 | `████████████░░░` |
| **agent** | 1238 | `███░░░░░░░░░░░░` |
| **cowork** | 961 | `██░░░░░░░░░░░░░` |
| **nautilus** | 860 | `██░░░░░░░░░░░░░` |
| **сходство** | 812 | `██░░░░░░░░░░░░░` |
| **ingit** | 784 | `██░░░░░░░░░░░░░` |
| **appendix** | 782 | `██░░░░░░░░░░░░░` |
| **документы** | 772 | `██░░░░░░░░░░░░░` |
| **agents** | 718 | `██░░░░░░░░░░░░░` |
| **work** | 579 | `█░░░░░░░░░░░░░░` |
| **what** | 578 | `█░░░░░░░░░░░░░░` |
| **portal** | 561 | `█░░░░░░░░░░░░░░` |
| **layer** | 535 | `█░░░░░░░░░░░░░░` |
| **document** | 528 | `█░░░░░░░░░░░░░░` |


### 228. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **technology** | 39 | `███████████████` |
| **combinations** | 39 | `███████████████` |
| **first** | 26 | `██████████░░░░░` |
| **agent** | 25 | `█████████░░░░░░` |
| **legal** | 24 | `█████████░░░░░░` |
| **local** | 24 | `█████████░░░░░░` |
| **knowledge** | 24 | `█████████░░░░░░` |
| **habr** | 19 | `███████░░░░░░░░` |
| **articles** | 17 | `██████░░░░░░░░░` |
| **комбинация** | 16 | `██████░░░░░░░░░` |
| **graphs** | 14 | `█████░░░░░░░░░░` |
| **graph** | 14 | `█████░░░░░░░░░░` |
| **svyazi** | 14 | `█████░░░░░░░░░░` |
| **router** | 13 | `█████░░░░░░░░░░` |
| **benchmarks** | 13 | `█████░░░░░░░░░░` |


### 229. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **turn** | 557 | `███████████████` |
| **view** | 400 | `██████████░░░░░` |
| **svyazi** | 296 | `███████░░░░░░░░` |
| **search** | 192 | `█████░░░░░░░░░░` |
| **cite** | 172 | `████░░░░░░░░░░░` |
| **memory** | 169 | `████░░░░░░░░░░░` |
| **mcp** | 140 | `███░░░░░░░░░░░░` |
| **rag** | 131 | `███░░░░░░░░░░░░` |
| **проект** | 113 | `███░░░░░░░░░░░░` |
| **collaborations** | 108 | `██░░░░░░░░░░░░░` |
| **llm** | 99 | `██░░░░░░░░░░░░░` |
| **knowledge** | 92 | `██░░░░░░░░░░░░░` |
| **слой** | 88 | `██░░░░░░░░░░░░░` |
| **oss** | 83 | `██░░░░░░░░░░░░░` |
| **evidence** | 77 | `██░░░░░░░░░░░░░` |


### 230. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **habr** | 71 | `███████████████` |
| **memory** | 70 | `██████████████░` |
| **llm** | 64 | `█████████████░░` |
| **пара** | 63 | `█████████████░░` |
| **projects** | 61 | `████████████░░░` |
| **yodoca** | 55 | `███████████░░░░` |
| **mcp** | 54 | `███████████░░░░` |
| **ngt** | 35 | `███████░░░░░░░░` |
| **legal** | 35 | `███████░░░░░░░░` |
| **каждый** | 31 | `██████░░░░░░░░░` |
| **проекты** | 29 | `██████░░░░░░░░░` |
| **wikontic** | 27 | `█████░░░░░░░░░░` |
| **svyazi** | 27 | `█████░░░░░░░░░░` |
| **claude** | 27 | `█████░░░░░░░░░░` |
| **readme** | 25 | `█████░░░░░░░░░░` |


### 231. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **components** | 84 | `███████████████` |
| **autofilled** | 81 | `██████████████░` |
| **svyazi** | 51 | `█████████░░░░░░` |
| **sgb** | 21 | `███░░░░░░░░░░░░` |
| **cowork** | 21 | `███░░░░░░░░░░░░` |
| **ingit** | 21 | `███░░░░░░░░░░░░` |
| **kksudo** | 21 | `███░░░░░░░░░░░░` |
| **lorenzo** | 21 | `███░░░░░░░░░░░░` |
| **nautilus** | 21 | `███░░░░░░░░░░░░` |
| **компонент** | 20 | `███░░░░░░░░░░░░` |
| **экосистемы** | 20 | `███░░░░░░░░░░░░` |
| **тип** | 20 | `███░░░░░░░░░░░░` |
| **spbmolot** | 19 | `███░░░░░░░░░░░░` |
| **описание** | 13 | `██░░░░░░░░░░░░░` |
| **связанные** | 11 | `█░░░░░░░░░░░░░░` |


### 232. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **badges** | 15 | `███████████████` |
| **svg** | 14 | `██████████████░` |
| **words** | 3 | `███░░░░░░░░░░░░` |
| **scripts** | 3 | `███░░░░░░░░░░░░` |
| **health** | 3 | `███░░░░░░░░░░░░` |
| **license** | 3 | `███░░░░░░░░░░░░` |
| **branch** | 3 | `███░░░░░░░░░░░░` |
| **бейджи** | 2 | `██░░░░░░░░░░░░░` |
| **scoring** | 2 | `██░░░░░░░░░░░░░` |
| **репозитория** | 1 | `█░░░░░░░░░░░░░░` |
| **автоматически** | 1 | `█░░░░░░░░░░░░░░` |
| **генерируются** | 1 | `█░░░░░░░░░░░░░░` |
| **скриптом** | 1 | `█░░░░░░░░░░░░░░` |
| **improve** | 1 | `█░░░░░░░░░░░░░░` |
| **текущие** | 1 | `█░░░░░░░░░░░░░░` |


### 233. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **контакт** | 126 | `███████████████` |
| **contacts** | 113 | `█████████████░░` |
| **статус** | 70 | `████████░░░░░░░` |
| **связи** | 70 | `████████░░░░░░░` |
| **профиль** | 56 | `██████░░░░░░░░░` |
| **первое** | 56 | `██████░░░░░░░░░` |
| **сообщение** | 56 | `██████░░░░░░░░░` |
| **rag** | 51 | `██████░░░░░░░░░` |
| **открытые** | 42 | `█████░░░░░░░░░░` |
| **вопросы** | 42 | `█████░░░░░░░░░░` |
| **svyazi** | 35 | `████░░░░░░░░░░░` |
| **cutcode** | 31 | `███░░░░░░░░░░░░` |
| **dmitriila** | 31 | `███░░░░░░░░░░░░` |
| **mixaill** | 31 | `███░░░░░░░░░░░░` |
| **vladspace** | 29 | `███░░░░░░░░░░░░` |


### 234. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **anthropic** | 6396 | `███████████████` |
| **vacancies** | 6174 | `██████████████░` |
| **проблем** | 2574 | `██████░░░░░░░░░` |
| **svyazi** | 952 | `██░░░░░░░░░░░░░` |
| **appendix** | 830 | `█░░░░░░░░░░░░░░` |
| **слов** | 807 | `█░░░░░░░░░░░░░░` |
| **сложный** | 538 | `█░░░░░░░░░░░░░░` |
| **абзац** | 509 | `█░░░░░░░░░░░░░░` |
| **мин** | 491 | `█░░░░░░░░░░░░░░` |
| **collaborations** | 453 | `█░░░░░░░░░░░░░░` |
| **анализ** | 444 | `█░░░░░░░░░░░░░░` |
| **agent** | 443 | `█░░░░░░░░░░░░░░` |
| **turn** | 440 | `█░░░░░░░░░░░░░░` |
| **оборванный** | 439 | `█░░░░░░░░░░░░░░` |
| **файлов** | 420 | `░░░░░░░░░░░░░░░` |


### 235. 01-svyazi (9,295 слов)
_Файл: `docs/obsidian/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **templates** | 22 | `███████████████` |
| **контакт** | 12 | `████████░░░░░░░` |
| **статус** | 12 | `████████░░░░░░░` |
| **project** | 11 | `███████░░░░░░░░` |
| **component** | 11 | `███████░░░░░░░░` |
| **research** | 11 | `███████░░░░░░░░` |
| **ключевые** | 10 | `██████░░░░░░░░░` |
| **contacts** | 9 | `██████░░░░░░░░░` |
| **contact** | 8 | `█████░░░░░░░░░░` |
| **outreach** | 8 | `█████░░░░░░░░░░` |
| **описание** | 8 | `█████░░░░░░░░░░` |
| **note** | 7 | `████░░░░░░░░░░░` |
| **ensemble** | 6 | `████░░░░░░░░░░░` |
| **имя** | 6 | `████░░░░░░░░░░░` |
| **связи** | 6 | `████░░░░░░░░░░░` |


### 236. Профиль
_Файл: `docs/obsidian/contacts/anastasiyaw.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **AnastasiyaW** |
| GitHub | [@AnastasiyaW](https://github.com/AnastasiyaW) |
| Проекты | knowledge-space, mclaude |
| Слой в Svyazi | knowledge/orchestration |
| Упомянут в документах | 11 файлах |
| Платформа | Habr / GitHub |


### 237. Профиль
_Файл: `docs/obsidian/contacts/andrey-chuyan.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **andrey_chuyan** |
| GitHub | [@andrey_chuyan](https://github.com/andrey_chuyan) |
| Проекты | Svyazi |
| Слой в Svyazi | ingestion/CardIndex |
| Упомянут в документах | 4 файлах |
| Платформа | Habr / GitHub |


### 238. Профиль
_Файл: `docs/obsidian/contacts/antipozitive.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **Antipozitive** |
| GitHub | [@Antipozitive](https://github.com/Antipozitive) |
| Проекты | MemNet |
| Слой в Svyazi | memory |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


### 239. Профиль
_Файл: `docs/obsidian/contacts/cutcode.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **Cutcode** |
| GitHub | [@Cutcode](https://github.com/Cutcode) |
| Проекты | AIF Handoff |
| Слой в Svyazi | orchestration |
| Упомянут в документах | 5 файлах |
| Платформа | Habr / GitHub |


### 240. Профиль
_Файл: `docs/obsidian/contacts/dmitriila.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **Dmitriila** |
| GitHub | [@Dmitriila](https://github.com/Dmitriila) |
| Проекты | SENTINEL |
| Слой в Svyazi | security |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


### 241. Профиль
_Файл: `docs/obsidian/contacts/kksudo.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **kksudo** |
| GitHub | [@kksudo](https://github.com/kksudo) |
| Проекты | AgentFS |
| Слой в Svyazi | knowledge/filesystem |
| Упомянут в документах | 13 файлах |
| Платформа | Habr / GitHub |


### 242. Профиль
_Файл: `docs/obsidian/contacts/mixaill76.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **MiXaiLL76** |
| GitHub | [@MiXaiLL76](https://github.com/MiXaiLL76) |
| Проекты | Auto AI Router |
| Слой в Svyazi | security |
| Упомянут в документах | 4 файлах |
| Платформа | Habr / GitHub |


### 243. Профиль
_Файл: `docs/obsidian/contacts/nlaik.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **nlaik** |
| GitHub | [@nlaik](https://github.com/nlaik) |
| Проекты | LiteParse / research-docs |
| Слой в Svyazi | rag |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


### 244. Профиль
_Файл: `docs/obsidian/contacts/sonia-black.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **Sonia_Black** |
| GitHub | [@Sonia_Black](https://github.com/Sonia_Black) |
| Проекты | knowledge-space |
| Слой в Svyazi | knowledge |
| Упомянут в документах | 6 файлах |
| Платформа | Habr / GitHub |


### 245. Профиль
_Файл: `docs/obsidian/contacts/spbmolot.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **spbmolot** |
| GitHub | [@spbmolot](https://github.com/spbmolot) |
| Проекты | NGT Memory |
| Слой в Svyazi | memory |
| Упомянут в документах | 12 файлах |
| Платформа | Habr / GitHub |


### 246. Профиль
_Файл: `docs/obsidian/contacts/tagir-analyzes.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **tagir_analyzes** |
| GitHub | [@tagir_analyzes](https://github.com/tagir_analyzes) |
| Проекты | Legal RAG |
| Слой в Svyazi | rag |
| Упомянут в документах | 4 файлах |
| Платформа | Habr / GitHub |


### 247. Профиль
_Файл: `docs/obsidian/contacts/vitalyoborin.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **VitalyOborin** |
| GitHub | [@VitalyOborin](https://github.com/VitalyOborin) |
| Проекты | Yodoca |
| Слой в Svyazi | memory |
| Упомянут в документах | 7 файлах |
| Платформа | Habr / GitHub |


### 248. Профиль
_Файл: `docs/obsidian/contacts/vladspace.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **VladSpace** |
| GitHub | [@VladSpace](https://github.com/VladSpace) |
| Проекты | Graph RAG |
| Слой в Svyazi | rag |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


### 249. Профиль
_Файл: `docs/obsidian/contacts/zodigancode.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Ник | **zodigancode** |
| GitHub | [@zodigancode](https://github.com/zodigancode) |
| Проекты | Rufler |
| Слой в Svyazi | orchestration |
| Упомянут в документах | 3 файлах |
| Платформа | Habr / GitHub |


### 250. Профиль
_Файл: `docs/obsidian/templates/contact-outreach.md` | 2 колонок, 4 строк_

| Параметр | Значение |
|----------|---------|
| Имя | [имя] |
| GitHub | [@handle](ссылка) |
| Проекты | [список] |
| Платформа | [Habr/GitHub/Telegram] |


### 251. Рассмотренные варианты
_Файл: `docs/obsidian/templates/decision-record.md` | 3 колонок, 3 строк_

| Вариант | Плюсы | Минусы |
|---------|-------|--------|
| A | | |
| B | | |
| C | | |


### 252. Компоненты
_Файл: `docs/obsidian/templates/ensemble.md` | 3 колонок, 2 строк_

| Компонент | Роль | Лицензия |
|-----------|------|----------|
| [Проект A] | [роль] | [лицензия] |
| [Проект B] | [роль] | [лицензия] |


### 253. Статус
_Файл: `docs/obsidian/templates/project-component.md` | 2 колонок, 4 строк_

| Параметр | Значение |
|----------|---------|
| Версия   | [x.y.z] |
| Лицензия | [MIT/Apache/BSL] |
| Язык     | [Python/TypeScript/Rust] |
| Репо     | [ссылка] |


## root (157 таблиц)


### 1. Словарь аббревиатур и сокращений
_Файл: `docs/ABBREVIATIONS.md` | 3 колонок, 85 строк_

| Аббревиатура | Расшифровка | Упоминаний |
|-------------|-------------|------------|
| **ACD** | Automated Capability Discovery — ещё один сильный кубик: модель в роли «учёного» систематически генерирует задачи для мо | 12 |
| **ADR** | "ADR-004: Temporal Metadata as First-Class Concept" | 173 |
| **AGENTS** | типология + готовая к развёртыванию категория Type 1 | 71 |
| **AI** | это инфраструктурный слой для AI-managed virtual companies | 4763 |
| **AIRI** | серьёзная research лаборатория (Артём Шелманов и команда) | 35 |
| **ANP** | Agent Network Protocol | 10 |
| **API** ⭐ | Application Programming Interface — интерфейс программирования приложений | 528 |
| **BSL** ⭐ | Business Source License — бизнес-лицензия с открытым кодом | 153 |
| **CAMEL** | это другая значимая open-source framework, и сравнение их с Hermes будет показательным | 349 |
| **CI/CD** ⭐ | Continuous Integration / Continuous Deployment | 20 |
| **CLI** ⭐ | Command Line Interface — интерфейс командной строки | 112 |
| **CRDT** ⭐ | Conflict-free Replicated Data Type — структура данных без конфликтов слияния | 119 |
| **DAO** | результат смешанный | 6 |
| **EMEA** | RU/DE/EN на рабочем уровне, базирование в Германии, понимание европейского регуляторного контекста (что прямо читается ч | 55 |
| **ERROR** | MCP SDK not installed | 6 |
| **FAQ** ⭐ | Frequently Asked Questions — часто задаваемые вопросы | 99 |
| **FDE** | это исполнительская роль на чужую продуктовую повестку | 26 |
| **FRE** | 70-100 лёгкий, 50-70 средний, 30-50 сложный, <30 очень сложный | 18 |
| **GDPR** ⭐ | General Data Protection Regulation — европейский регламент защиты данных | 103 |
| **GG** | они публичные) | 4 |
| **GUI** | -3 months effort | 31 |
| **HEAD** | 7 commits) | 10 |
| **HMP** | на когнитивной устойчивости и этике | 176 |
| **ID** | sgb:XII:90:4 (SGB XII, § 90, Abs | 14 |
| **II** | The Double-Triangle Architecture — formal описание дуальной структуры с вашей метафорой звезды Давида | 44 |
| **III** | Protocols Between Layers — три протокола с examples | 35 |
| **INPUT** | - Bescheid text (decoded by agent) | 4 |
| **IP** | AI-платформа, заказчик, сами фрилансеры? Сегодняшние legal frameworks не умеют отвечать на этот вопрос дёшево | 14 |
| **IV** | Nautilus Portal as Reference Implementation — как existing work serves как substrate | 38 |
| **IX** | 102 , sgg:86b:2 ), на прецеденты | 82 |
| **JWT** ⭐ | JSON Web Token — токен аутентификации | 8 |
| **KPI** | сколько полезных коллабораций, проектов, выступлений, mentorship‑пар или hiring‑контактов возникло из рекомендаций систе | 133 |
| **KSV** | потому что у них нет точных русских эквивалентов в контексте немецкой социально-правовой системы | 61 |
| **LAYER** | функциональная категория Type 4 | 113 |
| **LCI** | Lyapunov Coherence Index, target π | 47 |
| **LLM** ⭐ | Large Language Model — большая языковая модель | 664 |
| **LOC** | продублирована с разными строками в разных частях | 96 |
| **MCP** ⭐ | Model Context Protocol — протокол контекста для AI-инструментов | 1635 |
| **MIT** ⭐ | Massachusetts Institute of Technology License — разрешительная лицензия | 546 |
| **ML** | несколько моделей → voting/averaging | 118 |
| **MMORPG** | это общее пространство , в котором вы видите аватары коллег, можете подойти к ним, стоять рядом, работать вместе в одной | 83 |
| **MRR** | это уже leverage для любого следующего шага, включая разговор с Anthropic Institute о grant/partnership | 8 |
| **MUST** | - Возвращать пустой список, если ничего не найдено (не `None`, не exception) | 153 |
| **MVP** ⭐ | Minimum Viable Product — минимально жизнеспособный продукт | 462 |
| **NDA** | intermediate view (placeholder'ы, но с consistent identifiers для longitudinal анализа) | 4 |
| **NGT** | граф памяти > <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** У | 585 |
| **NLP** ⭐ | Natural Language Processing — обработка естественного языка | 2 |
| **NPP** | **федеративная модель**, где каждый | 160 |
| **OASIS** | до 1M agents simulation) | 8 |
| **ODT** | не только текст | 4 |
| **OKWF** | конкретная архитектура](#применение-к-okwf-конкретная-архитектура) | 640 |
| **OPTIONAL** | ключевые слова | 20 |
| **OS** | неуточнено | 272 |
| **OSS** ⭐ | Open Source Software — программное обеспечение с открытым кодом | 471 |
| **OUTPUT** | - Draft Widerspruch (DOCX format) | 4 |
| **P2P** ⭐ | Peer-to-Peer — децентрализованная сеть | 37 |
| **PARC** | research center, became iconic несмотря на parent brand decline OpenAI — research org становящаяся product company, name | 6 |
| **PII** ⭐ | Personally Identifiable Information — персональные данные | 97 |
| **PROTOCOL** | иначе future разработчики будут gадать | 435 |
| **PURE** | LLM-based User Profile Management for Recommender System» | 11 |
| **QA** | демон-критик (adversarial, rigorous) | 397 |
| **RAG** ⭐ | Retrieval-Augmented Generation — генерация с поиском по базе знаний | 857 |
| **README** | 550+ строк production-качества: установка, конфигурация для всех 6 платформ (включая детализацию /etc/fstab для CIFS, AD | 1891 |
| **REQUIRED** | откуда пришло | 46 |
| **ROI** | 10 sec queries vs 2 hour manual search | 37 |
| **SDK** ⭐ | Software Development Kit — набор инструментов разработчика | 119 |
| **SENTINEL** | неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2 | 419 |
| **SF** | DC, Canberra) | 40 |
| **SGB** ⭐ | Sozialgesetzbuch — Социальный кодекс Германии | 752 |
| **SHOULD** | - Поддерживать case-insensitive matching для текстовых запросов | 73 |
| **SWE** | в Sales/Finance/Marketing/Legal зарплаты ниже и сильно варьируются по локации | 12 |
| **TF-IDF** ⭐ | Term Frequency–Inverse Document Frequency — метрика важности термина | 36 |
| **TODO** ⭐ | To Do — задача к выполнению | 9 |
| **TSU** | физика, MoME — математика; ZINC — software, гибридная архитектура — алгоритм; RISC-V — кремний, privacy — право; TinyML  | 20 |
| **TVCP** | Terminal Video Communication Platform, терминал видео коммуникация платформа, игры») — это необычное : Go + template + M | 4 |
| **UI** | -2 months effort | 129 |
| **URL** | я разберусь с любым вариантом именования | 165 |
| **VERIFY** | 6782 vs 6600] как метку | 4 |
| **VI** | Deployment Paths — humanities, project management, OSS, general | 8 |
| **VII** | Open Questions — governance, consent, economics, scale | 8 |
| **VIII** | Call to Action — что делать researchers, practitioners, founders | 6 |
| **VPS** | cron каждое утро обходит сайты Sozialgericht/BSG/KSV, генерирует Stellungnahme-черновики, обновляет статусы Aktenzeichen | 23 |
| **XII** | legally binding reference с нормативной силой | 80 |
| **YAML** ⭐ | YAML Ain't Markup Language — формат конфигурационных файлов | 220 |
| **ZINC** | - Ночью агент крутит эксперименты с промптами | 56 |


### 2. Самые часто используемые
_Файл: `docs/ABBREVIATIONS.md` | 2 колонок, 15 строк_

| Аббревиатура | Упоминаний |
|-------------|------------|
| **AI** | 4763 — _это инфраструктурный слой для AI-managed virtual companies_ |
| **README** | 1891 — _550+ строк production-качества: установка, конфигурация для _ |
| **MCP** | 1635 — _Model Context Protocol — протокол контекста для AI-инструмен_ |
| **RAG** | 857 — _Retrieval-Augmented Generation — генерация с поиском по базе_ |
| **SGB** | 752 — _Sozialgesetzbuch — Социальный кодекс Германии_ |
| **LLM** | 664 — _Large Language Model — большая языковая модель_ |
| **OKWF** | 640 — _конкретная архитектура](#применение-к-okwf-конкретная-архите_ |
| **NGT** | 585 — _граф памяти > <!-- abstract-auto --> > **Абстракт** (авто) >_ |
| **MIT** | 546 — _Massachusetts Institute of Technology License — разрешительн_ |
| **API** | 528 — _Application Programming Interface — интерфейс программирован_ |
| **OSS** | 471 — _Open Source Software — программное обеспечение с открытым ко_ |
| **MVP** | 462 — _Minimum Viable Product — минимально жизнеспособный продукт_ |
| **PROTOCOL** | 435 — _иначе future разработчики будут gадать_ |
| **SENTINEL** | 419 — _неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI_ |
| **QA** | 397 — _демон-критик (adversarial, rigorous)_ |


### 3. Callout-блоки
_Файл: `docs/ALERTS.md` | 3 колонок, 4 строк_

| Тип | Количество | Назначение |
|-----|------------|------------|
| `[!NOTE]` | 0 | Нейтральная заметка |
| `[!TIP]` | 42 | Практический совет |
| `[!WARNING]` | 10 | Предупреждение о риске |
| `[!IMPORTANT]` | 5 | Ключевой документ |


### 4. Авторы и коллаборации
_Файл: `docs/AUTHORS.md` | 2 колонок, 25 строк_

| Автор | Упоминается в файлах |
|-------|---------------------|
| **AnastasiyaW** | 72 |
| **Antipozitive** | 42 |
| **BerriAI** | 14 |
| **Cutcode** | 73 |
| **Dmitriila** | 66 |
| **MiXaiLL76** | 64 |
| **Sonia_Black** | 31 |
| **VitaliySemenov** | 8 |
| **VitalyOborin** | 65 |
| **VladSpace** | 68 |
| **akazant** | 12 |
| **akzhankalimatov** | 8 |
| **andrey_chuyan** | 33 |
| **iximy** | 10 |
| **kksudo** | 129 |
| **lee-to** | 16 |
| **lib4u** | 15 |
| **moshael** | 12 |
| **nlaik** | 43 |
| **spbmolot** | 125 |
| **tagir_analyzes** | 38 |
| **vpakspace** | 8 |
| **zodigancode** | 54 |
| **Андрей Чуян** | 40 |
| **Виталий Оборин** | 14 |


### 5. Топ-30 самых цитируемых документов
_Файл: `docs/BACKLINKS.md` | 3 колонок, 30 строк_

| Документ | Входящих ссылок | Ссылающиеся файлы |
|----------|----------------|-------------------|
| `README` | 385 | `02-methodology.md`, `00-intro.md`, `01-интегральный-анализ-профиля-svend4.md`, `02-общий-план-развития-nautilus-portal-protocol.md` +381 |
| `28-appendix-a-minimal-working-examp` | 38 | `04-abstract.md`, `09-4-passport-passport-md.md`, `103-appendix-b-change-log.md`, `104-appendix-c-references.md` +34 |
| `151-open-knowledge-work-foundation-` | 34 | `12-content-overview.md`, `13-angle-perspective.md`, `134-the-double-triangle-architecture-md.md`, `135-a-formal-model-for-human-ai-collaboration-in-distr.md` +30 |
| `07-mvp-planning` | 29 | `01-executive-summary.md`, `03-component-catalog.md`, `04-ensembles-overview.md`, `06-security-privacy.md` +25 |
| `42-author-contact` | 27 | `03-portal-protocol-md.md`, `04-abstract.md`, `05-0-status-of-this-document.md`, `105-review-methodology-md.md` +23 |
| `211-table-of-contents` | 27 | `149-appendix-b-summary-of-contributions.md`, `169-table-of-contents.md`, `172-3-what-makes-a-representative-agent.md`, `182-acknowledgments.md` +23 |
| `10-новые-ансамбли-следующего-шага` | 26 | `01-executive-summary.md`, `03-component-catalog.md`, `04-ensembles-overview.md`, `07-mvp-planning.md` +22 |
| `105-review-methodology-md` | 26 | `106-tl-dr.md`, `108-2-формальный-workflow.md`, `117-10-конкретный-план-применения-к-текущим-документам.md`, `122-глоссарий.md` +22 |
| `09-architectural-gaps` | 25 | `01-executive-summary.md`, `03-component-catalog.md`, `04-ensembles-overview.md`, `06-security-privacy.md` +21 |
| `05-0-status-of-this-document` | 25 | `03-portal-protocol-md.md`, `04-abstract.md`, `114-7-реализация-в-проекте-nautilus.md`, `125-readme-mcp-md-инструкция-по-установке.md` +21 |
| `03-portal-protocol-md` | 25 | `05-0-status-of-this-document.md`, `105-review-methodology-md.md`, `123-portal-mcp-py.md`, `125-readme-mcp-md-инструкция-по-установке.md` +21 |
| `208-professional-colleague-agents-m` | 25 | `12-content-overview.md`, `13-angle-perspective.md`, `134-the-double-triangle-architecture-md.md`, `145-8-call-to-action.md` +21 |
| `104-appendix-c-references` | 24 | `02-общий-план-развития-nautilus-portal-protocol.md`, `103-appendix-b-change-log.md`, `109-3-принципы-консолидации-фаза-c.md`, `122-глоссарий.md` +20 |
| `25-13-reference-implementation` | 24 | `05-0-status-of-this-document.md`, `104-appendix-c-references.md`, `141-4-nautilus-portal-as-reference-substrate.md`, `147-references.md` +20 |
| `123-portal-mcp-py` | 23 | `04-abstract.md`, `105-review-methodology-md.md`, `110-вопрос-fallback-ratio-как-критический-или-осмыслен.md`, `125-readme-mcp-md-инструкция-по-установке.md` +19 |
| `77-2-terminology` | 23 | `06-1-introduction.md`, `07-2-terminology.md`, `08-3-registry-nautilus-json.md`, `109-3-принципы-консолидации-фаза-c.md` +19 |
| `229-профессиональные-коллеги-агенты` | 23 | `105-review-methodology-md.md`, `188-ai-опосредованное-представительство-для-недопредст.md`, `189-аннотация.md`, `202-12-заключение.md` +19 |
| `134-the-double-triangle-architectur` | 23 | `12-content-overview.md`, `13-angle-perspective.md`, `143-6-four-deployment-domains.md`, `144-7-open-questions.md` +19 |
| `kksudo` | 23 | `AUTOFILLED.md`, `OUTLINE.md`, `TABLES.md`, `.md` +19 |
| `10-second-order-ensembles` | 22 | `01-executive-summary.md`, `04-ensembles-overview.md`, `06-security-privacy.md`, `07-mvp-planning.md` +18 |
| `04-приоритетные-ансамбли` | 22 | `03-component-catalog.md`, `04-ensembles-overview.md`, `06-security-privacy.md`, `07-mvp-planning.md` +18 |
| `326-содержание` | 22 | `126-установка.md`, `127-подключение-к-claude-desktop.md`, `149-appendix-b-summary-of-contributions.md`, `154-table-of-contents.md` +18 |
| `209-a-typology-of-ai-agents-on-the-` | 22 | `135-a-formal-model-for-human-ai-collaboration-in-distr.md`, `137-table-of-contents.md`, `146-acknowledgments.md`, `152-ai-coordinated-infrastructure-for-distributed-expe.md` +18 |
| `308-table-of-contents` | 22 | `149-appendix-b-summary-of-contributions.md`, `169-table-of-contents.md`, `211-table-of-contents.md`, `253-table-of-contents.md` +18 |
| `223-12-closing` | 22 | `168-abstract.md`, `171-2-historical-precedents-agents-as-civilizational-i.md`, `175-6-ethical-framework.md`, `178-9-phased-rollout-strategy.md` +18 |
| `spbmolot` | 22 | `ngt-memory.md`, `AUTOFILLED.md`, `OUTLINE.md`, `TABLES.md` +18 |
| `05-план-прототипа-и-возможные-конта` | 21 | `02-methodology.md`, `06-security-privacy.md`, `07-mvp-planning.md`, `10-second-order-ensembles.md` +17 |
| `125-readme-mcp-md-инструкция-по-уст` | 21 | `02-общий-план-развития-nautilus-portal-protocol.md`, `105-review-methodology-md.md`, `122-глоссарий.md`, `123-portal-mcp-py.md` +17 |
| `04-abstract` | 21 | `09-4-passport-passport-md.md`, `105-review-methodology-md.md`, `123-portal-mcp-py.md`, `127-подключение-к-claude-desktop.md` +17 |
| `251-ai-support-through-configurable` | 21 | `135-a-formal-model-for-human-ai-collaboration-in-distr.md`, `137-table-of-contents.md`, `146-acknowledgments.md`, `167-ai-mediated-representation-for-underrepresented-ex.md` +17 |


### 6. Ссылки по разделам
_Файл: `docs/BACKLINKS.md` | 3 колонок, 11 строк_

| Раздел | Входящих | Исходящих |
|--------|----------|-----------|
| **01-svyazi** | 178 | 137 |
| **02-anthropic-vacancies** | 3917 | 3462 |
| **03-technology-combinations** | 31 | 41 |
| **04-ai-collaborations** | 186 | 169 |
| **05-habr-projects** | 40 | 47 |
| **autofilled** | 161 | 104 |
| **badges** | 0 | 0 |
| **contacts** | 149 | 133 |
| **obsidian** | 532 | 532 |
| **root** | 901 | 1464 |
| **templates** | 16 | 22 |


### 7. Сломанные внутренние ссылки
_Файл: `docs/BROKEN_LINKS.md` | 4 колонок, 41 строк_

| Файл | Текст ссылки | Цель | Проблема |
|------|--------------|------|----------|
| `docs/02-anthropic-vacancies/104-appendix-c-references.md` | Nautilus Portal Protocol v1.1 | `./docs/PORTAL-PROTOCOL.md` | файл не существует |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | REVIEW_METHODOLOGY.md | `./REVIEW_METHODOLOGY.md` | файл не существует |
| `docs/02-anthropic-vacancies/122-глоссарий.md` | REVIEW_METHODOLOGY.md | `./REVIEW_METHODOLOGY.md` | файл не существует |
| `docs/02-anthropic-vacancies/130-отладка.md` | Tool-call падает с "adapterfai | `#tool-call-падает-с-adapterfailed` | якорь не найден |
| `docs/02-anthropic-vacancies/18-6-adapter-interface.md` | 6.4. translateto(entry, target | `#64-translatetoentry-targetrepo-required` | якорь не найден |
| `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` | NPP v1.0 | `../PORTAL-PROTOCOL.md` | файл не существует |
| `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` | NPP v1.0 | `../PORTAL-PROTOCOL.md` | файл не существует |
| `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` | NPP v1.0 | `../PORTAL-PROTOCOL.md` | файл не существует |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | `passports/` | `./passports/` | файл не существует |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | PORTAL-PROTOCOL.md §6 | `./PORTAL-PROTOCOL.md#6-adapter-interface` | файл не существует |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | PORTAL-PROTOCOL.md §5 | `./PORTAL-PROTOCOL.md#5-compatibility-lev` | файл не существует |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | PORTAL-PROTOCOL.md | `./PORTAL-PROTOCOL.md` | файл не существует |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | passports/ | `./passports/` | файл не существует |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | info1 | `./passports/info1.md` | файл не существует |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | pro2 | `./passports/pro2.md` | файл не существует |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | meta | `./passports/meta.md` | файл не существует |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | MIT | `./LICENSE` | файл не существует |
| `docs/02-anthropic-vacancies/68-about.md` | `passports/` | `./passports/` | файл не существует |
| `docs/02-anthropic-vacancies/68-about.md` | PORTAL-PROTOCOL.md §6 | `./PORTAL-PROTOCOL.md#6-adapter-interface` | файл не существует |
| `docs/02-anthropic-vacancies/68-about.md` | PORTAL-PROTOCOL.md §5 | `./PORTAL-PROTOCOL.md#5-compatibility-lev` | файл не существует |
| `docs/02-anthropic-vacancies/68-about.md` | PORTAL-PROTOCOL.md | `./PORTAL-PROTOCOL.md` | файл не существует |
| `docs/02-anthropic-vacancies/68-about.md` | passports/ | `./passports/` | файл не существует |
| `docs/02-anthropic-vacancies/68-about.md` | info1 | `./passports/info1.md` | файл не существует |
| `docs/02-anthropic-vacancies/68-about.md` | pro2 | `./passports/pro2.md` | файл не существует |
| `docs/02-anthropic-vacancies/68-about.md` | meta | `./passports/meta.md` | файл не существует |
| `docs/02-anthropic-vacancies/68-about.md` | MIT | `./LICENSE` | файл не существует |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | tdywx@abc123 | `link` | файл не существует |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | CzylE@def456 | `link` | файл не существует |
| `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | 12.2. Path B — generatepasspor | `#122-path-b-generatepassportpy-wizard` | якорь не найден |
| `docs/CODE_BLOCKS.md` | REVIEW_METHODOLOGY.md | `./REVIEW_METHODOLOGY.md` | файл не существует |
| `docs/CODE_BLOCKS.md` | docs | `docs/badges/docs.svg` | файл не существует |
| `docs/CODE_BLOCKS.md` | words | `docs/badges/words.svg` | файл не существует |
| `docs/CODE_BLOCKS.md` | scripts | `docs/badges/scripts.svg` | файл не существует |
| `docs/CODE_BLOCKS.md` | health | `docs/badges/health.svg` | файл не существует |
| `docs/CODE_BLOCKS.md` | go/no-go | `docs/badges/scoring.svg` | файл не существует |
| `docs/CODE_BLOCKS.md` | license | `docs/badges/license.svg` | файл не существует |
| `docs/CODE_BLOCKS.md` | branch | `docs/badges/branch.svg` | файл не существует |
| `docs/CONCEPTS.md` | 67-о-проекте | `docs/02-anthropic-vacancies/67-о-проекте` | файл не существует |
| `docs/DECISIONS.md` | Детали по топ-20 пробелам | `#детали-по-топ-20-пробелам` | якорь не найден |
| `docs/DECISIONS.md` | `LiteParse` (40 файлов) | `#liteparse-40-файлов` | якорь не найден |
| `docs/DECISIONS.md` | `BSL` (36 файлов) | `#bsl-36-файло  


### 8. Сломанные внутренние ссылки
_Файл: `docs/BROKEN_LINKS.md` | 4 колонок, 12 строк_

| `docs/DECISIONS.md` | Упоминается в | `#упоминается-в` | якорь не найден |
| `docs/DECISIONS.md` | Связанные документы | `#связанные-документы` | якорь не найден |
| `docs/KPI.md` | Кластер 1 — cowork, ingit, yes | `#кластер-1 | `CLUSTERS` |
| **17** | айл` | якорь не найден |
| `docs/KPI.md` | Кластер 2 — professional, agen | `#кластер | `CLUSTERS` |
| **16** | ue-ty` | якорь не найден |
| `docs/KPI.md` | Кластер 3 — turn, view, cite,  | `#кластер | `CLUSTERS` |
| **15** | searc` | якорь не найден |
| `docs/KPI.md` | Кластер 4 — repo, passport, np | `#кластер | `CLUSTERS` |
| **14** | -15-ф` | якорь не найден |
| `docs/KPI.md` | Кластер 6 — документ, document | `#кластер | `CLUSTERS` |
| **13** | githu` | якорь не найден |
| `docs/KPI.md` | Кластер 7 — turn, view, label, | `#кластер | `CLUSTERS` |
| **11** | vyazi` | якорь не найден |


### 9. Статистика коммитов
_Файл: `docs/CHANGELOG_AUTO.md` | 3 колонок, 5 строк_

| Тип | Название | Кол-во |
|-----|---------|--------|
| `feat` | ✨ Новые возможности | 17 |
| `fix` | 🐛 Исправления | 3 |
| `docs` | 📝 Документация | 2 |
| `chore` | 🔧 Технические задачи | 10 |
| `other` | 📌 Прочее | 16 |


### 10. Топ доменов
_Файл: `docs/CITATION_INDEX.md` | 3 колонок, 20 строк_

| Домен | URL | Авторитетность |
|-------|-----|----------------|
| `github.com` | 55 | ⭐⭐⭐⭐⭐ |
| `habr.com` | 41 | ⭐⭐⭐⭐ |
| `raw.githubusercontent.com` | 11 | ⭐ |
| `3dnews.ru` | 2 | ⭐ |
| `claude.ai` | 2 | ⭐ |
| `api.github.com` | 2 | ⭐⭐⭐⭐⭐ |
| `fontanka.ru` | 1 | ⭐ |
| `eb.hypothes.is` | 1 | ⭐ |
| `discourse.org` | 1 | ⭐ |
| `claude.com` | 1 | ⭐ |
| `support.claude.com` | 1 | ⭐ |
| `fossil-scm.org` | 1 | ⭐ |
| `install.sh` | 1 | ⭐ |
| `happyin.space` | 1 | ⭐ |
| `creativecommons.org` | 1 | ⭐ |
| `solidproject.org` | 1 | ⭐ |
| `3.org` | 1 | ⭐ |
| `activitypub.rocks` | 1 | ⭐ |
| `vc.ru` | 1 | ⭐ |
| `habr` | 1 | ⭐ |


### 11. Наиболее цитируемые URL
_Файл: `docs/CITATION_INDEX.md` | 4 колонок, 50 строк_

| URL | Файлов | Авторитетность | Домен |
|-----|--------|----------------|-------|
| `https://github.com/svend4/nautilus/issues` | 17 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/ingit` | 12 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/nautilus` | 10 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/pro2` | 7 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/info1` | 6 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/mcp` | 5 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/AnastasiyaW/knowledge-space` | 5 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/data70` | 4 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/meta` | 4 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://habr.com/ru/articles/1006622/` | 4 | ⭐⭐⭐⭐ | `habr.com` |
| `https://github.com/settings/tokens` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/ingit/issues` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/anthropics/mcp` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/camel-ai/camel` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/AnastasiyaW` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/spbmolot` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/kksudo` | 3 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://habr.com/ru/articles/938626/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1009608/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1005776/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1002138/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/yoomoney/articles/1012870/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/975414/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1020860/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1016096/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027210/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1007122/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1024884/comments/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1024634/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/955798/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1020598/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/surfstudio/articles/943108/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1009538/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/996144/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/yandex/articles/1019928/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027878/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1023446/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/983684/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1006602/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1010198/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/943498/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027382/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1010478/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/airi/articles/855128/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1017200/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1019588/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1009958/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/893356/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/airi/articles/1000720/` | 3 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027658/` | 3 | ⭐⭐⭐⭐ | `habr.com` |


### 12. Содержание
_Файл: `docs/CODE_BLOCKS.md` | 2 колонок, 7 строк_

| Язык | Блоков |
|------|--------|
| 📝 Без языка | 151 |
| 💻 Bash / Shell | 27 |
| 🐍 Python | 17 |
| 📦 JSON | 13 |
| 📊 Диаграммы Mermaid | 10 |
| markdown | 8 |
| 📋 YAML | 5 |


### 13. Паспорт: /
_Файл: `docs/CODE_BLOCKS.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | / |
| Формат | `.` — краткое описание |
| Единица | что является одной записью |
| Адаптер | `adapters/.py` |
| Уровень совместимости | <0-3> —  |


### 14. Изменившиеся файлы (362) — топ по Δ слов
_Файл: `docs/COMPARE.md` | 4 колонок, 30 строк_

| Файл | Было | Стало | Δ |
|------|------|-------|---|
| `GITHUB_ISSUES.md` | 884 | 1703 | +819 |
| `DEPENDENCY_MAP.md` | 675 | 1008 | +333 |
| `QA.md` | 1028 | 1268 | +240 |
| `INDEX.md` | 699 | 528 | -171 |
| `CHANGELOG.md` | 888 | 945 | +57 |
| `QA.md` | 224 | 182 | -42 |
| `QA.md` | 268 | 226 | -42 |
| `BROKEN_LINKS.md` | 726 | 766 | +40 |
| `CONTACTS.md` | 512 | 552 | +40 |
| `DUPLICATES.md` | 133 | 95 | -38 |
| `DIGEST_WEEKLY.md` | 228 | 205 | -23 |
| `KPI_HISTORY.md` | 106 | 85 | -21 |
| `STATS.md` | 494 | 511 | +17 |
| `CITATION_INDEX.md` | 830 | 844 | +14 |
| `COMPARE.md` | 477 | 491 | +14 |
| `CONCEPT_GRAPH.md` | 646 | 660 | +14 |
| `CONTACT_PRIORITY.md` | 364 | 378 | +14 |
| `CONTRADICTIONS.md` | 1209 | 1223 | +14 |
| `COVERAGE.md` | 289 | 303 | +14 |
| `NAMED_ENTITIES.md` | 1399 | 1413 | +14 |
| `OUTLINE.md` | 14228 | 14242 | +14 |
| `PARAGRAPH_QUALITY.md` | 4532 | 4546 | +14 |
| `PROGRESS.md` | 238 | 252 | +14 |
| `READING_TIME.md` | 5769 | 5783 | +14 |
| `REPORT.md` | 304 | 318 | +14 |
| `SCHEDULE.md` | 271 | 285 | +14 |
| `SITEMAP.md` | 2130 | 2144 | +14 |
| `SOURCE_MAP.md` | 2895 | 2909 | +14 |
| `STALENESS.md` | 398 | 412 | +14 |
| `TIMELINE.md` | 1789 | 1803 | +14 |


### 15. Распределение сложности
_Файл: `docs/COMPLEXITY.md` | 2 колонок, 3 строк_

| Уровень | Файлов |
|---------|--------|
| 🟢 Простой (0-1) | 706 |
| 🟡 Средний (2-3)  | 265 |
| 🔴 Сложный (4-5)  | 66 |


### 16. Самые сложные документы
_Файл: `docs/COMPLEXITY.md` | 6 колонок, 25 строк_

| Документ | Слов | Ср.длина пред. | Термин.плотность | Ур.заголовков | Балл |
|----------|------|---------------|-----------------|--------------|------|
| `342-что-такое-вариант-c-concept-doc` | 10594 | 26.7 | 0.17% | H5 | 🔴 Сложный |
| `343-lorenzo-catalyst-agent-глубокая` | 5653 | 26.5 | 0.25% | H5 | 🔴 Сложный |
| `342-что-такое-вариант-c-concept-doc` | 10618 | 26.8 | 0.17% | H5 | 🔴 Сложный |
| `343-lorenzo-catalyst-agent-глубокая` | 5672 | 26.6 | 0.25% | H5 | 🔴 Сложный |
| `00-intro` | 8733 | 18.0 | 0.25% | H4 | 🔴 Сложный |
| `01-интегральный-анализ-профиля-sven` | 18866 | 15.8 | 0.14% | H4 | 🔴 Сложный |
| `133-обратная-связь` | 3644 | 17.5 | 0.36% | H4 | 🔴 Сложный |
| `150-appendix-c-version-history` | 4856 | 20.1 | 0.02% | H4 | 🔴 Сложный |
| `272-appendix-d-connection-diagram` | 3735 | 15.3 | 0.03% | H4 | 🔴 Сложный |
| `303-приложение-визуализация-позиции` | 1801 | 18.8 | 1.17% | H4 | 🔴 Сложный |
| `341-приложение-c-образец-спецификац` | 3503 | 24.5 | 0.43% | H4 | 🔴 Сложный |
| `365-развёрнутый-анализ-внуковой-ком` | 4114 | 18.2 | 1.0% | H4 | 🔴 Сложный |
| `03-local-first` | 357 | 20.3 | 3.64% | H4 | 🔴 Сложный |
| `05-benchmarks` | 773 | 26.8 | 2.2% | H4 | 🔴 Сложный |
| `00-intro` | 11388 | 18.5 | 1.32% | H2 | 🔴 Сложный |
| `04-приоритетные-ансамбли` | 1372 | 26.1 | 1.9% | H2 | 🔴 Сложный |
| `10-новые-ансамбли-следующего-шага` | 1001 | 25.7 | 1.1% | H2 | 🔴 Сложный |
| `14-ограничения-лицензии-и-что-пока-` | 3355 | 18.0 | 1.01% | H2 | 🔴 Сложный |
| `memnet` | 7179 | 16.5 | 1.02% | H3 | 🔴 Сложный |
| `ABBREVIATIONS` | 1038 | 148.4 | 1.73% | H2 | 🔴 Сложный |
| `COMPONENT_MATRIX` | 573 | 64.1 | 4.01% | H2 | 🔴 Сложный |
| `CONCEPTS` | 11497 | 383.6 | 0.26% | H2 | 🔴 Сложный |
| `CONTACT_PRIORITY` | 231 | 46.2 | 4.33% | H3 | 🔴 Сложный |
| `ENTITIES` | 388 | 30.8 | 10.31% | H2 | 🔴 Сложный |
| `FOOTNOTES` | 200 | 50.5 | 6.5% | H2 | 🔴 Сложный |


### 17. Самые простые документы
_Файл: `docs/COMPLEXITY.md` | 3 колонок, 15 строк_

| Документ | Слов | Балл |
|----------|------|------|
| `03-portal-protocol-md` | 125 | 🟢 Простой |
| `05-0-status-of-this-document` | 138 | 🟢 Простой |
| `06-1-introduction` | 362 | 🟢 Простой |
| `07-2-terminology` | 301 | 🟢 Простой |
| `08-3-registry-nautilus-json` | 335 | 🟢 Простой |
| `09-4-passport-passport-md` | 166 | 🟢 Простой |
| `105-review-methodology-md` | 105 | 🟢 Простой |
| `106-tl-dr` | 148 | 🟢 Простой |
| `107-1-контекст-и-мотивация` | 349 | 🟢 Простой |
| `108-2-формальный-workflow` | 295 | 🟢 Простой |
| `110-вопрос-fallback-ratio-как-критически` | 222 | 🟢 Простой |
| `112-5-связь-с-существующими-методологиям` | 312 | 🟢 Простой |
| `114-7-реализация-в-проекте-nautilus` | 304 | 🟢 Простой |
| `115-8-ограничения-и-открытые-вопросы` | 368 | 🟢 Простой |
| `117-10-конкретный-план-применения-к-теку` | 189 | 🟢 Простой |


### 18. Матрица возможностей
_Файл: `docs/COMPONENT_MATRIX.md` | 13 колонок, 14 строк_

| Компонент | Лицензия | Статус | Долгосро | Поиск/ин | MCP-совм | Граф зна | Безопасн | Оркестра | Веб-крау | Хранилищ | Документ | CRDT/syn |
|-----------|----------|--------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| **CardIndex** | 🟢 MIT | 🟢 stable | ✅ | ✅ | ✅ | 🟡 | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| **AgentFS** | 🟢 MIT | 🟢 stable | 🟡 | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ | ✅ | ✅ | 🟡 |
| **Yodoca** | 🟢 Apache 2.0 | 🔵 active | ✅ | ✅ | 🟡 | ❌ | 🟡 | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **NGT-memory** | 🟠 BSL 1.1 | 🔵 active | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **SENTINEL** | 🟢 MIT | 🔵 active | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Rufler** | ⚪ — | 🟡 experimental | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | 🟡 | ❌ |
| **knowledge-space** | 🟢 MIT | 🟢 stable | ✅ | ✅ | 🟡 | 🟡 | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **Firecrawl** | 🟢 MIT | 🟢 stable | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| **Wikontic** | ⚪ — | ⚪ unknown | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Memnet** | ⚪ — | 🟡 experimental | ✅ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **agent-memory-mcp** | 🟢 MIT | 🟡 experimental | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ |
| **LiteParse** | ⚪ — | ⚪ unknown | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **AI Factory** | ⚪ — | ⚪ unknown | ❌ | ❌ | 🟡 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **agent-pool** | ⚪ — | ⚪ unknown | ❌ | ❌ | 🟡 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |


### 19. Покрытие возможностей
_Файл: `docs/COMPONENT_MATRIX.md` | 4 колонок, 10 строк_

| Возможность | Полная поддержка | Частичная | Итого |
|-------------|-----------------|-----------|-------|
| Долгосрочная память | 6 | 1 | 7/14 |
| Поиск/индекс | 8 | 1 | 9/14 |
| MCP-совместим | 6 | 4 | 10/14 |
| Граф знаний | 2 | 2 | 4/14 |
| Безопасность/PII | 1 | 2 | 3/14 |
| Оркестрация | 3 | 0 | 3/14 |
| Веб-краулинг | 2 | 0 | 2/14 |
| Хранилище данных | 8 | 0 | 8/14 |
| Документированный API | 4 | 5 | 9/14 |
| CRDT/sync | 0 | 1 | 1/14 |


### 20. Каталог компонентов
_Файл: `docs/COMPONENT_MATRIX.md` | 4 колонок, 14 строк_

| Компонент | Лицензия | Статус | Репозиторий |
|-----------|----------|--------|-------------|
| **CardIndex** | 🟢 MIT | 🟢 stable | `kksudo/CardIndex` |
| **AgentFS** | 🟢 MIT | 🟢 stable | `kksudo/agentfs` |
| **Yodoca** | 🟢 Apache 2.0 | 🔵 active | `spbmolot/yodoca` |
| **NGT-memory** | 🟠 BSL 1.1 | 🔵 active | — |
| **SENTINEL** | 🟢 MIT | 🔵 active | — |
| **Rufler** | ⚪ — | 🟡 experimental | — |
| **knowledge-space** | 🟢 MIT | 🟢 stable | `kksudo/knowledge-space` |
| **Firecrawl** | 🟢 MIT | 🟢 stable | `mendableai/firecrawl` |
| **Wikontic** | ⚪ — | ⚪ unknown | — |
| **Memnet** | ⚪ — | 🟡 experimental | — |
| **agent-memory-mcp** | 🟢 MIT | 🟡 experimental | — |
| **LiteParse** | ⚪ — | ⚪ unknown | — |
| **AI Factory** | ⚪ — | ⚪ unknown | — |
| **agent-pool** | ⚪ — | ⚪ unknown | — |


### 21. Рекомендуемые ансамбли
_Файл: `docs/COMPONENT_MATRIX.md` | 3 колонок, 5 строк_

| Ансамбль | Компоненты | Ключевая функция |
|----------|-----------|-----------------|
| Knowledge OS | CardIndex + AgentFS + knowledge-space | Индекс знаний + AI FS |
| Memory Layer | Yodoca + NGT-memory + agent-memory-mcp | Долгосрочная память |
| Security Runtime | SENTINEL + AgentFS | PII-защита + MCP allowlist |
| Web Intelligence | Firecrawl + CardIndex + Yodoca | Краулинг → память |
| Agent Orchestra | Rufler + agent-pool + AI Factory | Оркестрация агентов |


### 22. Топ концептов по связям
_Файл: `docs/CONCEPT_GRAPH.md` | 4 колонок, 30 строк_

| Концепт | Файлов | Связей | Категория |
|---------|--------|--------|-----------|
| `docs` | 482 | 4264 | other |
| `anthropic` | 398 | 3642 | other |
| `vacancies` | 375 | 3503 | other |
| `auto` | 292 | 2834 | other |
| `документы` | 251 | 2642 | other |
| `summary` | 230 | 2280 | other |
| `сходство` | 176 | 1935 | other |
| `tags` | 181 | 1862 | other |
| `appendix` | 136 | 1451 | other |
| `nautilus` | 123 | 1328 | other |
| `agent` | 126 | 1323 | agent |
| `architecture` | 112 | 1309 | other |
| `knowledge` | 122 | 1196 | other |
| `ingit` | 101 | 1147 | other |
| `contents` | 108 | 1136 | other |
| `cowork` | 93 | 1109 | other |
| `portal` | 93 | 1046 | other |
| `svyazi` | 119 | 990 | project |
| `collaboration` | 84 | 966 | other |
| `agents` | 85 | 943 | agent |
| `layer` | 72 | 880 | architecture |
| `work` | 75 | 840 | other |
| `protocol` | 73 | 814 | architecture |
| `document` | 62 | 761 | data |
| `abstract` | 62 | 724 | other |
| `readme` | 68 | 709 | other |
| `what` | 69 | 707 | other |
| `open` | 62 | 705 | other |
| `infrastructure` | 59 | 665 | other |
| `claude` | 63 | 653 | other |


### 23. Согласованность терминов
_Файл: `docs/CONSISTENCY.md` | 4 колонок, 10 строк_

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 8 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 2 |
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 2 |
| **CardIndex** | `CardIndex` | `card-index` | 2 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 4 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 25 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 1 |
| **self-improvement** | `self-improvement` | `self-improve` | 70 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 3 |


### 24. Ключевые авторы проектов
_Файл: `docs/CONTACTS.md` | 5 колонок, 15 строк_

| Автор | Проект | Слой | Упомянут в файлах | Первый вопрос |
|-------|--------|------|-------------------|---------------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 73 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 43 | — |
| **Cutcode** | AIF Handoff | orchestration | 74 | — |
| **Dmitriila** | SENTINEL | security | 67 | — |
| **MiXaiLL76** | Auto AI Router | security | 65 | — |
| **Sonia_Black** | knowledge-space | knowledge | 31 | — |
| **VitalyOborin** | Yodoca | memory | 65 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 68 | — |
| **andrey_chuyan** | Svyazi | ingestion/CardIndex | 33 | Стоит ли расширять CardIndex до person/project/episode/evidence или лучше держать разные индексы? |
| **kksudo** | AgentFS | knowledge/filesystem | 130 | Что лучше класть в .agentos, а что выносить в machine-only state вне vault conventions? |
| **lee-to** | AI Factory | orchestration | 16 | — |
| **nlaik** | LiteParse / research-docs | rag | 44 | — |
| **spbmolot** | NGT Memory | memory | 126 | Где проходит практическая граница между полезной ассоциацией и ложной ко-активацией тем для community discovery? |
| **tagir_analyzes** | Legal RAG | rag | 38 | — |
| **zodigancode** | Rufler | orchestration | 54 | — |


### 25. GitHub репозитории
_Файл: `docs/CONTACTS.md` | 2 колонок, 46 строк_

| Репозиторий | Упоминается в файлах |
|-------------|---------------------|
| `github.com/github.com/AnastasiyaW` | 9 |
| `github.com/github.com/AnastasiyaW/knowledge-space` | 15 |
| `github.com/github.com/Antipozitive` | 7 |
| `github.com/github.com/Cutcode` | 7 |
| `github.com/github.com/Dmitriila` | 7 |
| `github.com/github.com/MiXaiLL76` | 7 |
| `github.com/github.com/NicholasSpisak/second-brain` | 4 |
| `github.com/github.com/Sonia` | 7 |
| `github.com/github.com/VitalyOborin` | 7 |
| `github.com/github.com/VitalyOborin/yodoca` | 3 |
| `github.com/github.com/VladSpace` | 7 |
| `github.com/github.com/andrey` | 7 |
| `github.com/github.com/anthropics/mcp` | 11 |
| `github.com/github.com/artur-gavronchuk/tg-chat-analyser` | 4 |
| `github.com/github.com/camel-ai/camel` | 11 |
| `github.com/github.com/dementev-dev/adversarial-review` | 4 |
| `github.com/github.com/github` | 4 |
| `github.com/github.com/kagvi13/HMP` | 2 |
| `github.com/github.com/kagvi13/HMP.` | 2 |
| `github.com/github.com/kksudo` | 8 |
| `github.com/github.com/kksudo/agentfs` | 2 |
| `github.com/github.com/lib4u/rufler` | 2 |
| `github.com/github.com/mcp` | 14 |
| `github.com/github.com/nlaik` | 6 |
| `github.com/github.com/ruvnet/ruflo` | 2 |
| `github.com/github.com/settings/tokens` | 10 |
| `github.com/github.com/spbmolot` | 8 |
| `github.com/github.com/spbmolot/ngt-memory` | 2 |
| `github.com/github.com/svend4` | 8 |
| `github.com/github.com/svend4/data70` | 12 |
| `github.com/github.com/svend4/info1` | 24 |
| `github.com/github.com/svend4/info40` | 8 |
| `github.com/github.com/svend4/info7` | 8 |
| `github.com/github.com/svend4/ingit` | 28 |
| `github.com/github.com/svend4/meta` | 22 |
| `github.com/github.com/svend4/n` | 2 |
| `github.com/github.com/svend4/nautilus` | 83 |
| `github.com/github.com/svend4/nautilus.` | 4 |
| `github.com/github.com/svend4/nautilus.git` | 6 |
| `github.com/github.com/svend4/pro2` | 22 |
| `github.com/github.com/tagir` | 6 |
| `github.com/github.com/tree` | 2 |
| `github.com/github.com/users/svend4` | 9 |
| `github.com/github.com/vuguzum/self-aware-mcp-server` | 4 |
| `github.com/github.com/yjs/yjs` | 4 |
| `github.com/github.com/zodigancode` | 6 |


### 26. Топ авторов по приоритету
_Файл: `docs/CONTACT_PRIORITY.md` | 7 колонок, 15 строк_

| # | Автор | Проект | Слой | Упоминаний | Статус | Балл |
|---|-------|--------|------|-----------|--------|------|
| 1 | **kksudo** | AgentFS | knowledge/filesystem | 130 | 👁 Изучили | 401 |
| 2 | **spbmolot** | NGT Memory | memory | 126 | 👁 Изучили | 389 |
| 3 | **Cutcode** | AIF Handoff | orchestration | 74 | ⬜ Не начато | 226 |
| 4 | **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 73 | ⬜ Не начато | 225 |
| 5 | **VladSpace** | Graph RAG | rag | 68 | ⬜ Не начато | 208 |
| 6 | **Dmitriila** | SENTINEL | security | 67 | ⬜ Не начато | 203 |
| 7 | **VitalyOborin** | Yodoca | memory | 65 | ⬜ Не начато | 201 |
| 8 | **MiXaiLL76** | Auto AI Router | security | 65 | ⬜ Не начато | 197 |
| 9 | **zodigancode** | Rufler | orchestration | 54 | ⬜ Не начато | 166 |
| 10 | **nlaik** | LiteParse / research-docs | rag | 44 | ⬜ Не начато | 136 |
| 11 | **Antipozitive** | MemNet | memory | 43 | ⬜ Не начато | 135 |
| 12 | **tagir_analyzes** | Legal RAG | rag | 38 | ⬜ Не начато | 118 |
| 13 | **andrey_chuyan** | Svyazi | ingestion/CardIndex | 33 | ⬜ Не начато | 101 |
| 14 | **Sonia_Black** | knowledge-space | knowledge | 31 | ⬜ Не начато | 99 |
| 15 | **lee-to** | AI Factory | orchestration | 16 | ⬜ Не начато | 52 |


### 27. Рекомендуется создать документы
_Файл: `docs/CONTENT_GAPS.md` | 3 колонок, 50 строк_

| Концепция | Упоминаний | Рекомендуемая папка |
|-----------|-----------|-------------------|
| `LiteParse` | 50 | `docs/04-ai-collaborations/` |
| `BSL` | 37 | `docs/04-ai-collaborations/` |
| `NPP` | 33 | `docs/02-anthropic-vacancies/` |
| `AIF` | 31 | `docs/contacts/` |
| `MUST` | 28 | `docs/02-anthropic-vacancies/` |
| `AutoResearch` | 26 | `docs/01-svyazi/` |
| `GDPR` | 24 | `docs/02-anthropic-vacancies/` |
| `SHOULD` | 21 | `docs/02-anthropic-vacancies/` |
| `CRDT` | 19 | `docs/04-ai-collaborations/` |
| `PII` | 18 | `docs/04-ai-collaborations/` |
| `CLI` | 16 | `docs/02-anthropic-vacancies/` |
| `XII` | 14 | `docs/02-anthropic-vacancies/` |
| `BSG` | 14 | `docs/02-anthropic-vacancies/` |
| `RFC` | 14 | `docs/02-anthropic-vacancies/` |
| `RLM` | 13 | `docs/04-ai-collaborations/` |
| `IDF` | 13 | `docs/04-ai-collaborations/` |
| `PDF` | 13 | `docs/04-ai-collaborations/` |
| `YiJing` | 13 | `docs/02-anthropic-vacancies/` |
| `URL` | 13 | `docs/02-anthropic-vacancies/` |
| `ROI` | 12 | `docs/02-anthropic-vacancies/` |
| `LinkedIn` | 12 | `docs/02-anthropic-vacancies/` |
| `MAY` | 12 | `docs/02-anthropic-vacancies/` |
| `KSV` | 12 | `docs/02-anthropic-vacancies/` |
| `HIPAA` | 11 | `docs/02-anthropic-vacancies/` |
| `BaseAdapter` | 10 | `docs/02-anthropic-vacancies/` |
| `LCI` | 10 | `docs/02-anthropic-vacancies/` |
| `HEALTH` | 10 | `docs/PARAGRAPH_QUALITY.md/` |
| `OpenWhispr` | 9 | `docs/04-ai-collaborations/` |
| `TypeScript` | 9 | `docs/02-anthropic-vacancies/` |
| `AutoGen` | 9 | `docs/02-anthropic-vacancies/` |
| `EIC` | 9 | `docs/02-anthropic-vacancies/` |
| `III` | 9 | `docs/02-anthropic-vacancies/` |
| `CodeWiki` | 8 | `docs/01-svyazi/` |
| `LangChain` | 8 | `docs/02-anthropic-vacancies/` |
| `HMP` | 8 | `docs/02-anthropic-vacancies/` |
| `FAISS` | 7 | `docs/04-ai-collaborations/` |
| `HTTP` | 7 | `docs/02-anthropic-vacancies/` |
| `MMORPG` | 7 | `docs/02-anthropic-vacancies/` |
| `DeepMind` | 7 | `docs/02-anthropic-vacancies/` |
| `DeepSeek` | 7 | `docs/03-technology-combinations/` |
| `DOCX` | 7 | `docs/04-ai-collaborations/` |
| `GUI` | 7 | `docs/02-anthropic-vacancies/` |
| `CAMEL` | 7 | `docs/02-anthropic-vacancies/` |
| `VPS` | 7 | `docs/02-anthropic-vacancies/` |
| `AIRI` | 7 | `docs/02-anthropic-vacancies/` |
| `WebSocket` | 6 | `docs/04-ai-collaborations/` |
| `CRM` | 6 | `docs/04-ai-collaborations/` |
| `GPU` | 6 | `docs/02-anthropic-vacancies/` |
| `EMEA` | 6 | `docs/02-anthropic-vacancies/` |
| `RDF` | 6 | `docs/02-anthropic-vacancies/` |


### 28. Итого
_Файл: `docs/COST.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Человеко-недель | **25** |
| Человеко-часов | **1,000** |
| Бюджет (USD) | **$86,400** |
| Календарный срок | **~6-8 месяцев** |
| Команда | **5 ролей** |


### 29. По компонентам
_Файл: `docs/COST.md` | 4 колонок, 13 строк_

| Компонент | Роль | Недель | Стоимость USD |
|-----------|------|--------|--------------|
| Project management | Project Manager | 4 | $10,400 |
| Knowledge OS ядро | Senior Python Dev | 3 | $10,200 |
| Yodoca memory layer | AI/ML Engineer | 3 | $13,200 |
| CardIndex интеграция | Senior Python Dev | 2 | $6,800 |
| NGT граф памяти | AI/ML Engineer | 2 | $8,800 |
| SENTINEL безопасность | Senior Python Dev | 2 | $6,800 |
| Rufler оркестрация | AI/ML Engineer | 2 | $8,800 |
| MCP протокол адаптер | Senior Python Dev | 2 | $6,800 |
| CI/CD и тесты | DevOps | 2 | $6,000 |
| AgentFS подключение | Senior Python Dev | 1 | $3,400 |
| MCP Tool Search | Senior Python Dev | 1 | $3,400 |
| Документация API | Tech Writer | 1 | $1,800 |
| **ИТОГО** | | **25** | **$86,400** |


### 30. По ролям
_Файл: `docs/COST.md` | 4 колонок, 5 строк_

| Роль | Ставка USD/ч | Недель | Итого USD |
|------|-------------|--------|----------|
| Senior Python Dev | $85 | 11 | $37,400 |
| AI/ML Engineer | $110 | 7 | $30,800 |
| DevOps | $75 | 2 | $6,000 |
| Tech Writer | $45 | 1 | $1,800 |
| Project Manager | $65 | 4 | $10,400 |


### 31. Сценарии
_Файл: `docs/COST.md` | 4 колонок, 3 строк_

| Сценарий | Команда | Срок | Бюджет |
|----------|---------|------|--------|
| Минимальный (solo) | 1 разработчик | ~18 мес | $28,800 |
| Оптимальный | 3 человека | ~8 мес | $43,200 |
| Ускоренный | 5 человек | ~5 мес | $86,400 |


### 32. Временные оценки из документов
_Файл: `docs/COST.md` | 3 колонок, 7 строк_

| Источник | Контекст | Недель |
|----------|----------|--------|
| `365-развёрнутый-анал` | Макс) и part-time, реальный timeline 12-24 месяца для full a… | 96 |
| `343-lorenzo-catalyst` | рудоёмкий процесс подачи - Может быть 6-18 месяцев до финанс… | 72 |
| `365-развёрнутый-анал` | eam. С solo developer (Макс) и part-time, реальный timeline … | 72 |
| `ACTION_ITEMS` | обратная-связь_ - 5: Burnout. Проект 12-18 месяцев для singl… | 72 |
| `CONCEPTS` | инимально жизнеспособный прототип за 12-18 месяцев     _→ [N… | 72 |
| `DECISIONS` | document — структурированный план на 12-18 месяцев, который … | 72 |
| `TABLES` | 65-развёрнутый-анал` | Макс) и part-time, реальный timeline … | 72 |


### 33. Сводка по секциям
_Файл: `docs/COVERAGE.md` | 8 колонок, 5 строк_

| Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks |
|--------|--------|---------|------|-----|-----------|--------|-----------|
| `01-svyazi` | 14 | 🟢 13/14 | 🟢 13/14 | 🟢 12/14 | 🟢 13/14 | 🔴 0/14 | 🟢 13/14 |
| `02-anthropic-vacancies` | 355 | 🟢 354/355 | 🟢 354/355 | 🟡 189/355 | 🟢 354/355 | 🔴 0/355 | 🟢 354/355 |
| `03-technology-combinations` | 5 | 🟢 5/5 | 🟢 5/5 | 🔴 1/5 | 🟢 5/5 | 🔴 0/5 | 🟢 5/5 |
| `04-ai-collaborations` | 15 | 🟢 15/15 | 🟢 15/15 | 🟢 13/15 | 🟢 15/15 | 🟢 15/15 | 🟢 15/15 |
| `05-habr-projects` | 6 | 🟢 6/6 | 🟢 6/6 | 🔴 1/6 | 🟢 6/6 | 🟢 6/6 | 🟢 6/6 |


### 34. Файлы с низким покрытием (< 3 признаков) — 2 файлов
_Файл: `docs/COVERAGE.md` | 8 колонок, 2 строк_

| Файл | Слов | Summary | Теги | TOC | CrossRefs | ## Статус | Backlinks |
|------|------| ---|---|---|---|---|--- |
| `docs/01-svyazi/00-intro-part2.md` | 5 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |


### 35. Карта плотности тем
_Файл: `docs/DENSITY.md` | 8 колонок, 20 строк_

| Тема | 01-svyazi | 02-vacancies | 03-tech | 04-collab | 05-habr | root | Итого |
|------|-----------|--------------|---------|-----------|---------|------|-------|
| **Svyazi** | 146 | 73 | 16 | 336 | 45 | 4212 | **4828** |
| **CardIndex** | 53 | 54 | 12 | 100 | 12 | 856 | **1087** |
| **AgentFS** | 51 | 93 | 4 | 101 | 28 | 1301 | **1578** |
| **Yodoca** | 86 | 36 | 18 | 134 | 110 | 1486 | **1870** |
| **NGT-memory** | 161 | 230 | 3 | 261 | 121 | 2558 | **3334** |
| **SENTINEL** | 47 | 8 | 0 | 59 | 0 | 535 | **649** |
| **Rufler** | 35 | 19 | 0 | 43 | 0 | 463 | **560** |
| **AI Factory** | 63 | 45 | 0 | 84 | 0 | 764 | **956** |
| **Knowledge OS** | 0 | 18 | 0 | 4 | 0 | 81 | **103** |
| **Forensic RAG** | 34 | 19 | 1 | 52 | 2 | 305 | **413** |
| **MCP** | 60 | 747 | 4 | 149 | 56 | 1855 | **2871** |
| **MVP** | 100 | 98 | 0 | 133 | 7 | 1251 | **1589** |
| **Архитектура** | 99 | 538 | 10 | 168 | 39 | 1984 | **2838** |
| **Безопасность** | 71 | 132 | 1 | 80 | 1 | 1125 | **1410** |
| **Лицензия** | 106 | 636 | 0 | 131 | 13 | 2154 | **3040** |
| **Roadmap** | 32 | 144 | 0 | 33 | 3 | 636 | **848** |
| **Вакансии** | 2 | 1358 | 2 | 13 | 7 | 13939 | **15321** |
| **Комбинации** | 9 | 140 | 29 | 17 | 10 | 758 | **963** |
| **Habr** | 34 | 78 | 20 | 187 | 88 | 1760 | **2167** |
| **Контакты** | 18 | 128 | 0 | 21 | 6 | 910 | **1083** |


### 36. Наиболее раскрытые темы
_Файл: `docs/DENSITY.md` | 3 колонок, 10 строк_

| Тема | Упоминаний | Визуализация |
|------|------------|-------------|
| **Вакансии** | 15321 | `███████████████` |
| **Svyazi** | 4828 | `████░░░░░░░░░░░` |
| **NGT-memory** | 3334 | `███░░░░░░░░░░░░` |
| **Лицензия** | 3040 | `██░░░░░░░░░░░░░` |
| **MCP** | 2871 | `██░░░░░░░░░░░░░` |
| **Архитектура** | 2838 | `██░░░░░░░░░░░░░` |
| **Habr** | 2167 | `██░░░░░░░░░░░░░` |
| **Yodoca** | 1870 | `█░░░░░░░░░░░░░░` |
| **MVP** | 1589 | `█░░░░░░░░░░░░░░` |
| **AgentFS** | 1578 | `█░░░░░░░░░░░░░░` |


### 37. Где сосредоточена каждая тема
_Файл: `docs/DENSITY.md` | 3 колонок, 20 строк_

| Тема | Основной раздел | % |
|------|-----------------|---|
| Svyazi | `root` | 87% |
| CardIndex | `root` | 78% |
| AgentFS | `root` | 82% |
| Yodoca | `root` | 79% |
| NGT-memory | `root` | 76% |
| SENTINEL | `root` | 82% |
| Rufler | `root` | 82% |
| AI Factory | `root` | 79% |
| Knowledge OS | `root` | 78% |
| Forensic RAG | `root` | 73% |
| MCP | `root` | 64% |
| MVP | `root` | 78% |
| Архитектура | `root` | 69% |
| Безопасность | `root` | 79% |
| Лицензия | `root` | 70% |
| Roadmap | `root` | 75% |
| Вакансии | `root` | 90% |
| Комбинации | `root` | 78% |
| Habr | `root` | 81% |
| Контакты | `root` | 84% |


### 38. Python-зависимости
_Файл: `docs/DEPENDABOT.md` | 5 колонок, 4 строк_

| Пакет | Мин. версия | Последняя (PyPI) | Статус | Используется в |
|-------|------------|-----------------|--------|----------------|
| `anthropic` | `0.25.0` | `—` | — | `scripts/improve_llm_*.py` |
| `mcp` | `1.0.0` | `—` | — | `scripts/mcp_server.py` |
| `pre-commit` | `3.0.0` | `—` | — | `.pre-commit-config.yaml` |
| `pyspellchecker` | `0.8.0` | `—` | — | `scripts/improve_spellcheck.py` |


### 39. OSS-проекты (Svyazi 2.0)
_Файл: `docs/DEPENDABOT.md` | 3 колонок, 4 строк_

| Проект | Репозиторий | Статус |
|--------|------------|--------|
| AgentFS | [https://github.com/kksudo/agentfs](https://github.com/kksudo/agentfs) | — |
| NGT Memory | [https://github.com/spbmolot/ngt-memory](https://github.com/spbmolot/ngt-memory) | — |
| Yodoca | [https://github.com/VitalyOborin/yodoca](https://github.com/VitalyOborin/yodoca) | — |
| knowledge-space | [https://github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space) | — |


### 40. Зависимости
_Файл: `docs/DEPENDENCY_MAP.md` | 3 колонок, 126 строк_

| Скрипт | Производит | Зависит от |
|--------|-----------|-----------|
| `improve_abbreviations.py` | `docs/ABBREVIATIONS.md` | `docs/**/*.md` |
| `improve_abstract.py` | `docs/**/*.md (абстракты)` | `docs/**/*.md` |
| `improve_action_items.py` | `docs/ACTION_ITEMS.md` | `docs/**/*.md` |
| `improve_alerts.py` | `docs/ALERTS.md`, `docs/**/*.md` | `docs/**/*.md` |
| `improve_auto_toc.py` | `docs/**/*.md (TOC)` | `docs/**/*.md` |
| `improve_autocorrect.py` | `docs/**/*.md (автоисправление)` | `docs/**/*.md` |
| `improve_autofill.py` | `docs/autofilled/**` | `docs/templates/**`, `docs/ENTITIES.md` |
| `improve_backlinks.py` | `docs/BACKLINKS.md` | `docs/**/*.md` |
| `improve_badges.py` | `docs/badges/*.svg` | `docs/HEALTH.md`, `docs/SCORING.md` |
| `improve_benchmark.py` | `docs/benchmark.json` | `scripts/improve_*.py` |
| `improve_broken_links.py` | `docs/BROKEN_LINKS.md` | `docs/**/*.md` |
| `improve_changelog.py` | `CHANGELOG.md` | — |
| `improve_changelog_auto.py` | `docs/CHANGELOG_AUTO.md` | — |
| `improve_chunk_semantic.py` | `docs/all_chunks.jsonl` | `docs/**/*.md` |
| `improve_ci_config.py` | `.github/workflows/docs.yml` | — |
| `improve_citation_index.py` | `docs/CITATION_INDEX.md` | `docs/**/*.md` |
| `improve_clusters.py` | `docs/CLUSTERS.md` | `docs/**/*.md` |
| `improve_compare.py` | `docs/COMPARE.md` | `docs/**/*.md` |
| `improve_compare_docs.py` | `docs/COMPARE.md` | `docs/**/*.md` |
| `improve_complexity.py` | `docs/COMPLEXITY.md` | `docs/**/*.md` |
| `improve_component_matrix.py` | `docs/COMPONENT_MATRIX.md` | `docs/CONTACTS.md` |
| `improve_concept_graph.py` | `docs/CONCEPT_GRAPH.md`, `docs/concept_graph.json` | `docs/**/*.md` |
| `improve_concepts.py` | `docs/CONCEPTS.md` | `docs/**/*.md` |
| `improve_confluence.py` | `docs/confluence/` | `docs/**/*.md` |
| `improve_consistency.py` | `docs/CONSISTENCY.md` | `docs/**/*.md` |
| `improve_contact_priority.py` | `docs/CONTACT_PRIORITY.md` | `docs/CONTACTS.md` |
| `improve_contact_status.py` | `docs/contacts/**/*.md (статус)` | `docs/contacts/**/*.md` |
| `improve_contacts.py` | `docs/CONTACTS.md` | `docs/**/*.md` |
| `improve_content_gaps.py` | `docs/CONTENT_GAPS.md` | `docs/**/*.md` |
| `improve_contradiction_check.py` | `docs/CONTRADICTIONS.md` | `docs/**/*.md` |
| `improve_cost.py` | `docs/COST.md` | `docs/**/*.md` |
| `improve_coverage.py` | `docs/COVERAGE.md` | `docs/**/*.md` |
| `improve_crosslink_all.py` | `docs/CROSSREFS.md`, `docs/**/*.md` | `docs/**/*.md` |
| `improve_crossrefs.py` | `docs/CROSSREFS.md` | `docs/**/*.md` |
| `improve_decisions.py` | `docs/DECISIONS.md` | `docs/**/*.md` |
| `improve_dedup.py` | `docs/DUPLICATES.md` | `docs/**/*.md` |
| `improve_density.py` | `docs/DENSITY.md` | `docs/**/*.md` |
| `improve_dependabot.py` | `docs/DEPENDABOT.md` | — |
| `improve_dependency_map.py` | `docs/DEPENDENCY_MAP.md` | `scripts/improve_*.py` |
| `improve_digest.py` | `docs/DIGEST.md` | — |
| `improve_digest_weekly.py` | `docs/DIGEST_WEEKLY.md` | — |
| `improve_duplicate_across.py` | `docs/DUPLICATES.md` | `docs/**/*.md` |
| `improve_entities.py` | `docs/ENTITIES.md` | `docs/**/*.md` |
| `improve_epub.py` | `docs/*.epub` | `docs/**/*.md` |
| `improve_export_csv.py` | `docs/export_full.csv` | `docs/**/*.md` |
| `improve_export_html.py` | `docs/export_full.html` | `docs/**/*.md` |
| `improve_export_json.py` | `docs/export_full.json` | `docs/**/*.md` |
| `improve_external_compare.py` | `docs/**/*.md (внешн. сравнение)` | `docs/**/*.md` |
| `improve_extract_code.py` | `docs/CODE_BLOCKS.md` | `docs/**/*.md` |
| `improve_extract_tables.py` | `docs/TABLES.md` | `docs/**/*.md` |
| `improve_faq.py` | `docs/FAQ.md` | `docs/**/*.md` |
| `improve_footnotes.py` | `docs/FOOTNOTES.md`, `docs/**/*.md (сноски)` | `docs/**/*.md` |
| `improve_github_issues.py` | `docs/GITHUB_ISSUES.md` | `docs/**/*.md` |
| `improve_glossary.py` | `docs/GLOSSARY.md` | `docs/**/*.md` |
| `improve_graph.py` | `docs/GRAPH.md` | `docs/ENTITIES.md` |
| `improve_health.py` | `docs/HEALTH.md` | `docs/METRICS.md`, `docs/VALIDATION.md` |
| `improve_heatmap.py` | `docs/HEATMAP.md` | `docs/TAGS.md` |
| `improve_index_master.py` | `docs/INDEX.md` | `docs/**/*.md` |
| `improve_index_update.py` | `docs/search_index.json` | `docs/search_index.json` |
| `improve_keyword_index.py` | `docs/KEYWORD_INDEX.md` | `docs/**/*.md` |
| `improve_kpi.py` | `docs/KPI.md` | `docs/**/*.md` |
| `improve_kpi_snapshot.py` | `docs/KPI_HISTORY.md`, `docs/kpi_history.json` | `docs/SCORING.md`, `docs/STATS.md` |
| `improve_link_preview.py` | `docs/LINKS.md` | `docs/**/*.md` |
| `improve_llm_contact.py` | `docs/contacts/**/*.md` | `docs/CONTACTS.md`, `ANTHROPIC_API_KEY` |
| `improve_llm_enrich.py` | `docs/**/*.md (enriched)` | `docs/ENTITIES.md`, `ANTHROPIC_API_KEY` |
| `improve_llm_gaps.py` | `docs/LLM_GAPS.md` | `docs/**/*.md`, `ANTHROPIC_API_KEY` |
| `improve_llm_qa.py` | `docs/LLM_QA.md` | `docs/QUESTIONS.md`, `ANTHROPIC_API_KEY` |
| `improve_llm_summary.py` | `docs/LLM_SUMMARIES.md` | `docs/*/README.md` |
| `improve_merge_by_topic.py` | `docs/**/*.md (слияние)` | `docs/**/*.md` |
| `improve_merge_short.py` | `docs/**/*.md (слияние коротких)` | `docs/**/*.md` |
| `improve_metrics.py` | `docs/METRICS.md` | `docs/**/*.md` |
| `improve_mindmap.py` | `docs/MINDMAP.md` | `docs/**/*.md` |
| `improve_missing.py` | `docs/MISSING.md` | `docs/**/*.md` |
| `improve_named_entity_index.py` | `docs/NAMED_ENTITIES.md`, `docs/named_entities.json` | `docs/**/*.md` |
| `improve_narrative.py` | `docs/NARRATIVE.md` | `docs/**/*.md` |
| `improve_network.py` | `docs/NETWORK.md`, `docs/network.dot` | `docs/ENTITIES.md` |
| `improve_obsidian.py` | `docs/obsidian/` | `docs/**/*.md` |
| `improve_onboarding.py` | `docs/ONBOARDING.md` | `docs/SCORING.md`, `docs/CONTACTS.md` |
| `improve_orphans.py` | `docs/ORPHANS.md` | `docs/BACKLINKS.md` |
| `improve_outline.py` | `docs/OUTLINE.md` | `docs/**/*.md` |
| `improve_paragraph_quality.py` | `docs/PARAGRAPH_QUALITY.md` | `docs/**/*.md` |
| `improve_passage_retrieval.py` | `docs/passages.json` | `docs/search_index.json` |
| `improve_pre_commit.py` | `.pre-commit-config.yaml` | — |
| `improve_priorities.py` | `docs/PRIORITIES.md` | `docs/**/*.md` |
| `improve_progress.py` | `docs/PROGRESS.md` | `docs/SCORING.md` |
| `improve_progress_sync.py` | `PROGRESS.md` | `docs/PROGRESS.md` |
| `improve_qa.py` | `docs/*/QA.md` | `docs/**/*.md` |
| `improve_questions.py` | `docs/QUESTIONS.md` | `docs/**/*.md` |
| `improve_readability_v2.py` | `docs/READABILITY.md` | `docs/**/*.md` |
| `improve_reading_order.py` | `docs/READING_ORDER.md` | `docs/**/*.md` |
| `improve_reading_time.py` | `docs/READING_TIME.md` | `docs/**/*.md` |
| `improve_readmes.py` | `docs/*/README.md` | — |
| `improve_reclassify.py` | `docs/**/*.md (перемещение)` | `docs/**/*.md` |
| `improve_report.py` | `docs/REPORT.md` | `docs/STATS.md`, `docs/HEALTH.md` |
| `improve_risk_register.py` | `docs/RISK_REGISTER.md` | `docs/**/*.md` |
| `improve_rss.py` | `docs/feed.rss`, `docs/feed.atom` | — |
| `improve_run_all.py` | `— (оркестратор)` | `scripts/improve_*.py` |
| `improve_schedule.py` | `docs/SCHEDULE.md` | — |
| `improve_scoring.py` | `docs/SCORING.md` | `docs/HEALTH.md`, `docs/METRICS.md` |
| `improve_search_index.py` | `docs/search_index.json` | `docs/**/*.md` |
| `improve_see_also.py` | `docs/SEE_ALSO.md`, `docs/**/*.md` | `docs/**/*.md` |
| `improve_sentiment.py` | `docs/SENTIMENT.md` | `docs/**/*.md` |
| `improve_similar.py` | `docs/SIMILAR.md` | `docs/**/*.md` |
| `improve_sitemap.py` | `docs/SITEMAP.md`, `docs/sitemap.xml` | `docs/**/*.md` |
| `improve_source_map.py` | `docs/SOURCE_MAP.md` | `docs/**/*.md` |
| `improve_spellcheck.py` | `docs/SPELLCHECK.md` | `docs/**/*.md` |
| `improve_staleness.py` | `docs/STALENESS.md` | `docs/**/*.md` |
| `improve_stats.py` | `docs/STATS.md` | `docs/**/*.md` |
| `improve_subtopic_fill.py` | `docs/**/*.md (дополнение)` | `docs/**/*.md` |
| `improve_summaries.py` | `docs/*/README.md` | `docs/**/*.md` |
| `improve_tables.py` ⚠️ | `docs/TABLES.md` | `docs/**/*.md` |
| `improve_tags.py` | `docs/TAGS.md` | `docs/**/*.md` |
| `improve_tech_radar.py` | `docs/TECH_RADAR.md` | — |
| `improve_templates.py` | `docs/templates/**` | — |
| `improve_text_segmenter.py` | `docs/**/*.md (сегменты)` | `docs/**/*.md` |
| `improve_timeline.py` | `docs/TIMELINE.md` | `docs/**/*.md` |
| `improve_timeline_events.py` | `docs/TIMELINE.md` | `docs/**/*.md` |
| `improve_toc.py` | `docs/**/*.md (TOC блоки)` | `docs/**/*.md` |
| `improve_topic_model.py` | `docs/TOPIC_MODEL.md` | `docs/**/*.md` |
| `improve_validate.py` | `docs/VALIDATION.md` | `docs/**/*.md` |
| `improve_version_diff.py` | `docs/VERSION_DIFF.md` | — |
| `improve_vocabulary_richness.py` | `docs/VOCABULARY.md` | `docs/**/*.md` |
| `improve_watch.py` | `— (watcher)` | `scripts/improve_*.py` |
| `improve_watcher.py` | `— (автономный watcher)` | `scripts/improve_*.py` |
| `improve_word_cloud.py` | `docs/WORD_CLOUD.svg`, `docs/WORD_CLOUD.md` | `docs/WORD_FREQ.md` |
| `improve_word_freq.py` | `docs/WORD_FREQ.md` | `docs/**/*.md` |


### 41. История коммитов (последние 15)
_Файл: `docs/DIGEST.md` | 3 колонок, 15 строк_

| Дата | Hash | Описание |
|------|------|---------|
| 2026-04-29 | `52179ba5` | fix: fix 8607 broken internal links, improve health score formula |
| 2026-04-29 | `d3037935` | merge: sync remote auto-generated docs, prefer local script outputs |
| 2026-04-29 | `898c42a0` | feat: run all script groups, apply TOC/abstracts/crosslinks, rebuild s |
| 2026-04-29 | `8e689b3d` | docs: auto-update via improve_run_all [skip ci] |
| 2026-04-29 | `b326b33a` | Merge remote-tracking branch 'origin/main' into claude/organize-monore |
| 2026-04-29 | `69562b02` | feat: add component matrix, KPI history tracker, fix run_all coverage |
| 2026-04-29 | `42f561dd` | fix: fix update-docs CI job failures |
| 2026-04-29 | `854cff7c` | Merge pull request #5 from svend4/claude/current-dev-stage-iVIov |
| 2026-04-29 | `59617c5d` | feat: add risk register, auto-changelog, master index; fix run_all mis |
| 2026-04-29 | `89d3e8fb` | chore: sync CONTRADICTIONS.md (background task output) |
| 2026-04-29 | `4ddee95e` | feat: add tech radar, onboarding guide, dependency map, meta group in  |
| 2026-04-29 | `6b81ffed` | chore: sync CONTRADICTIONS.md after contradiction_check fix |
| 2026-04-29 | `4755dd94` | fix: исправить ошибки в deeptext скриптах, добавить выходные файлы |
| 2026-04-29 | `1f3fe74a` | feat: add autonomous watcher (Ступень 6), CI workflow, LLM section sum |
| 2026-04-29 | `469dbced` | feat: add CLAUDE.md, weekly digest script, enrich group in run_all |


### 42. Текущее состояние репозитория
_Файл: `docs/DIGEST.md` | 2 колонок, 3 строк_

| Параметр | Значение |
|----------|---------|
| Документов `.md` | **1053** |
| Скриптов обработки | **125** |
| Последнее обновление | **2026-04-29** |


### 43. Итого
_Файл: `docs/DIGEST_WEEKLY.md` | 2 колонок, 5 строк_

| Метрика | Значение |
|---------|---------|
| Коммитов за неделю | **50** |
| Новых файлов | **0** |
| Изменённых файлов | **0** |
| Всего MD файлов | **529** |
| Всего слов | **523,662** |


### 44. Люди и авторы (7)
_Файл: `docs/ENTITIES.md` | 3 колонок, 7 строк_

| Имя | Упоминаний | Файлов |
|---------|------------|--------|
| **svend4** | 1963 | 244 |
| **Lorenzo** | 1576 | 156 |
| **kksudo** | 360 | 126 |
| **spbmolot** | 325 | 121 |
| **Андрей** | 144 | 45 |
| **Виталий** | 66 | 28 |
| **Антропик** | 37 | 30 |


### 45. Проекты (22)
_Файл: `docs/ENTITIES.md` | 3 колонок, 22 строк_

| Проект | Упоминаний | Файлов |
|---------|------------|--------|
| **Svyazi** | 3995 | 271 |
| **Nautilus** | 3824 | 425 |
| **ingit** | 3044 | 256 |
| **Cowork** | 2996 | 246 |
| **Lorenzo** | 1576 | 156 |
| **SGB** | 1494 | 215 |
| **AgentFS** | 982 | 150 |
| **NGT** | 975 | 194 |
| **Yodoca** | 926 | 163 |
| **CardIndex** | 915 | 140 |
| **knowledge-space** | 736 | 114 |
| **Rufler** | 549 | 113 |
| **mclaude** | 517 | 93 |
| **SENTINEL** | 499 | 119 |
| **LiteParse** | 467 | 105 |
| **AI Factory** | 418 | 92 |
| **MemNet** | 337 | 72 |
| **Wikontic** | 301 | 61 |
| **Firecrawl** | 192 | 25 |
| **agent-memory-mcp** | 84 | 36 |
| **MCP Tool Search** | 22 | 10 |
| **Shield** | 18 | 10 |


### 46. Организации (9)
_Файл: `docs/ENTITIES.md` | 3 колонок, 9 строк_

| Организация | Упоминаний | Файлов |
|---------|------------|--------|
| **Anthropic** | 14444 | 847 |
| **GitHub** | 2516 | 286 |
| **Claude** | 2457 | 356 |
| **Habr** | 1706 | 163 |
| **Obsidian** | 577 | 95 |
| **Хабр** | 458 | 84 |
| **Google** | 106 | 37 |
| **OpenAI** | 104 | 50 |
| **ChatGPT** | 86 | 50 |


### 47. Технологии и стандарты (24)
_Файл: `docs/ENTITIES.md` | 3 колонок, 24 строк_

| Технология | Упоминаний | Файлов |
|---------|------------|--------|
| **MCP** | 2751 | 322 |
| **RAG** | 2568 | 358 |
| **MIT** | 2043 | 370 |
| **LLM** | 1224 | 215 |
| **JSON** | 854 | 173 |
| **Python** | 564 | 147 |
| **REST** | 419 | 151 |
| **YAML** | 309 | 113 |
| **BSL** | 192 | 83 |
| **CRDT** | 173 | 41 |
| **Apache** | 162 | 80 |
| **Rust** | 149 | 78 |
| **Mermaid** | 97 | 30 |
| **SQLite** | 96 | 30 |
| **TypeScript** | 43 | 25 |
| **LangChain** | 41 | 25 |
| **TF-IDF** | 36 | 22 |
| **FAISS** | 29 | 17 |
| **PostgreSQL** | 28 | 18 |
| **WebSocket** | 25 | 17 |
| **FastAPI** | 19 | 11 |
| **JWT** | 10 | 8 |
| **OAuth** | 8 | 6 |
| **GraphQL** | 8 | 8 |


### 48. GitHub репозитории (15)
_Файл: `docs/ENTITIES.md` | 2 колонок, 15 строк_

| Репозиторий | Упоминаний |
|-------------|------------|
| [https://github.com/svend4/nautilus](https://github.com/svend4/nautilus) | 57 |
| [https://github.com/svend4/ingit](https://github.com/svend4/ingit) | 26 |
| [https://github.com/svend4/pro2](https://github.com/svend4/pro2) | 16 |
| [https://github.com/svend4/info1](https://github.com/svend4/info1) | 16 |
| [https://github.com/svend4/meta](https://github.com/svend4/meta) | 12 |
| [https://github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space) | 11 |
| [https://github.com/svend4/data70](https://github.com/svend4/data70) | 10 |
| [https://github.com/camel-ai/camel](https://github.com/camel-ai/camel) | 9 |
| [https://github.com/anthropics/mcp](https://github.com/anthropics/mcp) | 9 |
| [https://github.com/settings/tokens](https://github.com/settings/tokens) | 8 |
| [https://github.com/svend4/info7](https://github.com/svend4/info7) | 6 |
| [https://github.com/svend4/info40](https://github.com/svend4/info40) | 6 |
| [https://github.com/VitalyOborin/yodoca](https://github.com/VitalyOborin/yodoca) | 4 |
| [https://github.com/kksudo/agentfs](https://github.com/kksudo/agentfs) | 4 |
| [https://github.com/spbmolot/ngt-memory](https://github.com/spbmolot/ngt-memory) | 3 |


### 49. Ко-встречаемость проектов (топ пары)
_Файл: `docs/ENTITIES.md` | 2 колонок, 20 строк_

| Пара | Общих файлов |
|------|-------------|
| ingit ↔ Cowork | 211 |
| Nautilus ↔ Cowork | 179 |
| Nautilus ↔ ingit | 160 |
| Svyazi ↔ NGT | 159 |
| NGT ↔ Yodoca | 152 |
| Svyazi ↔ Yodoca | 147 |
| Nautilus ↔ SGB | 144 |
| Svyazi ↔ AgentFS | 138 |
| AgentFS ↔ NGT | 135 |
| AgentFS ↔ Yodoca | 127 |
| Svyazi ↔ CardIndex | 115 |
| NGT ↔ CardIndex | 115 |
| AgentFS ↔ CardIndex | 110 |
| ingit ↔ SGB | 109 |
| Svyazi ↔ Rufler | 108 |
| Svyazi ↔ SENTINEL | 108 |
| Cowork ↔ SGB | 108 |
| AgentFS ↔ SENTINEL | 108 |
| Svyazi ↔ Lorenzo | 105 |
| AgentFS ↔ Rufler | 103 |


### 50. Словарь сносок
_Файл: `docs/FOOTNOTES.md` | 3 колонок, 17 строк_

| Термин | Определение | Файлов |
|--------|-------------|--------|
| **AgentFS** | OSS-проект: файловая система для AI-агентов (MIT) | 3 |
| **BSL** | Business Source License — коммерческая лицензия с открытым кодом | 0 |
| **CRDT** | Conflict-free Replicated Data Type — бесконфликтные данные | 0 |
| **CardIndex** | OSS-проект: индекс знаний на карточках (MIT) | 3 |
| **Firecrawl** | Инструмент: веб-краулер для AI (MIT) | 0 |
| **Jaccard** | Коэффициент схожести множеств (0–1) | 0 |
| **LLM** | Large Language Model — большая языковая модель | 0 |
| **MCP** | Model Context Protocol — протокол для AI-инструментов | 0 |
| **NGT** | OSS-проект: ассоциативный граф памяти (BSL 1.1) | 0 |
| **PII** | Personally Identifiable Information — персональные данные | 0 |
| **RAG** | Retrieval-Augmented Generation — генерация с поиском | 2 |
| **Rufler** | OSS-проект: оркестратор AI-агентов | 0 |
| **SENTINEL** | OSS-проект: безопасность и allowlist для MCP | 0 |
| **Svyazi** | Главный проект: экосистема AI-компонентов | 0 |
| **TF-IDF** | Term Frequency–Inverse Document Frequency — метрика важности термина | 0 |
| **Yodoca** | OSS-проект: система памяти с консолидацией (Apache 2.0) | 0 |
| **knowledge-space** | OSS-проект: база знаний 785+ карточек (MIT) | 0 |


### 51. Топ совместных упоминаний
_Файл: `docs/GRAPH.md` | 3 колонок, 25 строк_

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **Yodoca** | 74 |
| **Svyazi** | **AgentFS** | 70 |
| **AgentFS** | **Yodoca** | 64 |
| **Svyazi** | **CardIndex** | 60 |
| **Svyazi** | **SENTINEL** | 58 |
| **Svyazi** | **Rufler** | 58 |
| **CardIndex** | **AgentFS** | 56 |
| **AgentFS** | **SENTINEL** | 56 |
| **Svyazi** | **NGT Memory** | 55 |
| **AgentFS** | **Rufler** | 54 |
| **Svyazi** | **knowledge-space** | 53 |
| **Svyazi** | **LiteParse** | 53 |
| **Svyazi** | **Auto AI Router** | 53 |
| **CardIndex** | **Yodoca** | 52 |
| **Rufler** | **Yodoca** | 52 |
| **SENTINEL** | **Auto AI Router** | 51 |
| **Yodoca** | **SENTINEL** | 50 |
| **Rufler** | **SENTINEL** | 50 |
| **Yodoca** | **NGT Memory** | 50 |
| **Svyazi** | **mclaude** | 49 |
| **Svyazi** | **AI Factory** | 49 |
| **AgentFS** | **knowledge-space** | 48 |
| **AgentFS** | **NGT Memory** | 48 |
| **CardIndex** | **knowledge-space** | 46 |
| **AgentFS** | **LiteParse** | 46 |


### 52. Метрики
_Файл: `docs/HEALTH.md` | 4 колонок, 5 строк_

| Метрика | Значение | Статус | Балл |
|---------|----------|--------|------|
| Покрытие текста | 97.6% | 🟢 | 98 |
| Полнота тем | 26✅ 2⚠️ 2❌ | 🟡 | 87 |
| Согласованность | 0 проблем | 🟢 | 100 |
| Внутренние ссылки | 170 сломано | 🟠 | 66 |
| Дублирование | 0 точных дублей | 🟢 | 100 |


### 53. Структура репозитория
_Файл: `docs/HEALTH.md` | 2 колонок, 11 строк_

| Раздел | Файлов |
|--------|--------|
| 01-svyazi | 16 |
| 02-anthropic-vacancies | 357 |
| 03-technology-combinations | 7 |
| 04-ai-collaborations | 17 |
| 05-habr-projects | 10 |
| autofilled | 13 |
| badges | 1 |
| contacts | 15 |
| obsidian | 524 |
| root | 87 |
| templates | 6 |


### 54. Числовые значения (‰)
_Файл: `docs/HEATMAP.md` | 6 колонок, 12 строк_

| Тема | svyazi | anthropic- | technology | ai-collabo | habr-proje |
|------|------------|------------|------------|------------|------------|
| **Память/Knowledge** | 24.0 | 3.3 | 15.6 | 16.5 | 19.9 |
| **Агент/Оркестр** | 22.6 | 13.5 | 25.2 | 19.3 | 8.7 |
| **Безопасность** | 7.6 | 0.4 | 0.4 | 4.1 | 0.1 |
| **Архитектура** | 6.2 | 6.1 | 4.2 | 3.7 | 1.1 |
| **MVP/Roadmap** | 8.3 | 0.8 | 0.0 | 3.9 | 1.1 |
| **Граф/RAG** | 9.6 | 1.8 | 21.4 | 7.8 | 3.8 |
| **Лицензия/OSS** | 8.2 | 2.3 | 0.0 | 4.2 | 1.0 |
| **Вакансии** | 0.2 | 5.4 | 0.8 | 0.5 | 0.8 |
| **Комбинации** | 5.0 | 0.7 | 11.1 | 2.9 | 2.1 |
| **Habr/Проекты** | 7.8 | 0.4 | 9.2 | 10.3 | 14.1 |
| **Контакты/Команда** | 6.8 | 1.0 | 0.0 | 4.0 | 2.2 |
| **Интеграция/API** | 8.1 | 7.5 | 2.7 | 7.6 | 6.9 |


### 55. Концентрация тем
_Файл: `docs/HEATMAP.md` | 3 колонок, 12 строк_

| Тема | Лучший раздел | Плотность |
|------|--------------|-----------|
| **Память/Knowledge** | `01-svyazi` | 24.0‰ |
| **Агент/Оркестр** | `03-technology-combinations` | 25.2‰ |
| **Безопасность** | `01-svyazi` | 7.6‰ |
| **Архитектура** | `01-svyazi` | 6.2‰ |
| **MVP/Roadmap** | `01-svyazi` | 8.3‰ |
| **Граф/RAG** | `03-technology-combinations` | 21.4‰ |
| **Лицензия/OSS** | `01-svyazi` | 8.2‰ |
| **Вакансии** | `02-anthropic-vacancies` | 5.4‰ |
| **Комбинации** | `03-technology-combinations` | 11.1‰ |
| **Habr/Проекты** | `05-habr-projects` | 14.1‰ |
| **Контакты/Команда** | `01-svyazi` | 6.8‰ |
| **Интеграция/API** | `01-svyazi` | 8.1‰ |


### 56. Метрики репозитория
_Файл: `docs/INDEX.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Markdown документов | **529** |
| Слов | **523,847** |
| Скриптов автоматизации | **125** |
| Go/No-Go скоринг | **93 🟢** |
| Здоровье репо | **90/100** |


### 57. Аналитика и отчёты
_Файл: `docs/INDEX.md` | 2 колонок, 26 строк_

| Документ | Описание |
|----------|---------|
| [`STATS.md`](STATS.md) | Статистика |
| [`METRICS.md`](METRICS.md) | Качество (65.7/100) |
| [`VALIDATION.md`](VALIDATION.md) | Валидация |
| [`SENTIMENT.md`](SENTIMENT.md) | Тональность |
| [`CLUSTERS.md`](CLUSTERS.md) | Кластеры тем |
| [`SIMILAR.md`](SIMILAR.md) | Похожие документы |
| [`HEATMAP.md`](HEATMAP.md) | Тепловая карта тем |
| [`QUESTIONS.md`](QUESTIONS.md) | Открытые вопросы (484) |
| [`KPI.md`](KPI.md) | KPI (737 показателей) |
| [`ACTION_ITEMS.md`](ACTION_ITEMS.md) | Задачи |
| [`DECISIONS.md`](DECISIONS.md) | Архитектурные решения |
| [`PRIORITIES.md`](PRIORITIES.md) | Приоритеты |
| [`PROGRESS.md`](PROGRESS.md) | Прогресс MVP |
| [`DIGEST_WEEKLY.md`](DIGEST_WEEKLY.md) | Дайджест недели |
| [`SITEMAP.md`](SITEMAP.md) | Карта сайта |
| [`WORD_CLOUD.md`](WORD_CLOUD.md) | Облако слов |
| [`BACKLINKS.md`](BACKLINKS.md) | Обратные ссылки |
| [`NARRATIVE.md`](NARRATIVE.md) | Нарратив проекта |
| [`ORPHANS.md`](ORPHANS.md) | Несвязанные файлы |
| [`ALERTS.md`](ALERTS.md) | Callout-блоки |
| [`FOOTNOTES.md`](FOOTNOTES.md) | Сноски терминов |
| [`ABBREVIATIONS.md`](ABBREVIATIONS.md) | Аббревиатуры |
| [`GLOSSARY.md`](GLOSSARY.md) | Глоссарий |
| [`CONCEPTS.md`](CONCEPTS.md) | Концепции |
| [`ENTITIES.md`](ENTITIES.md) | Сущности |
| [`TAGS.md`](TAGS.md) | Теги |


### 58. Ключевые документы
_Файл: `docs/INDEX.md` | 3 колонок, 12 строк_

| Документ | Тема | Описание |
|----------|------|---------|
| [`SCORING.md`](SCORING.md) | 🎯 Go/No-Go скоринг | Статус готовности: 96% |
| [`HEALTH.md`](HEALTH.md) | ❤️  Здоровье репо | Метрики качества документации |
| [`TECH_RADAR.md`](TECH_RADAR.md) | 📡 Tech Radar | ADOPT/TRIAL/ASSESS/HOLD |
| [`RISK_REGISTER.md`](RISK_REGISTER.md) | ⚠️  Реестр рисков | 10 рисков, матрица вероятность×влияние |
| [`ONBOARDING.md`](ONBOARDING.md) | 👋 Онбординг | Первые шаги, структура, контакты |
| [`FAQ.md`](FAQ.md) | ❓ FAQ | 54 вопроса и ответа |
| [`CONTACTS.md`](CONTACTS.md) | 📧 Контакты | Авторы компонентов, шаблоны писем |
| [`SCHEDULE.md`](SCHEDULE.md) | 📅 Расписание | Gantt, вехи, текущий статус |
| [`COST.md`](COST.md) | 💰 Стоимость MVP | $86,400 · 25 чел-недель |
| [`NETWORK.md`](NETWORK.md) | 🕸️  Граф связей | 20 узлов, 185 рёбер |
| [`CHANGELOG_AUTO.md`](CHANGELOG_AUTO.md) | 📋 Changelog | Авто из git-истории |
| [`DEPENDENCY_MAP.md`](DEPENDENCY_MAP.md) | 🗺️  Карта зависимостей | 49 скриптов → входы/выходы |


### 59. LLM-обогащение (Ступень 3)
_Файл: `docs/INDEX.md` | 2 колонок, 4 строк_

| Документ | Описание |
|----------|---------|
| `LLM_ENRICHED.md` _(нет)_ | Обогащённые stub-файлы |
| `LLM_QA.md` _(нет)_ | Ответы на открытые вопросы |
| `LLM_GAPS.md` _(нет)_ | Семантические пробелы |
| [`LLM_SUMMARIES.md`](LLM_SUMMARIES.md) | AI-саммари разделов |


### 60. Топ слов по охвату файлов
_Файл: `docs/KEYWORD_INDEX.md` | 3 колонок, 100 строк_

| Слово | Файлов | Всего упоминаний |
|-------|--------|-----------------|
| `docs` | 456 | 7625 |
| `также` | 399 | 435 |
| `смотрите` | 398 | 399 |
| `anthropic` | 395 | 5876 |
| `документы` | 391 | 505 |
| `vacancies` | 387 | 5361 |
| `похожие` | 377 | 378 |
| `сходство` | 376 | 988 |
| `knowledge` | 197 | 763 |
| `документ` | 188 | 455 |
| `agent` | 180 | 1482 |
| `nautilus` | 178 | 926 |
| `protocol` | 158 | 639 |
| `portal` | 150 | 647 |
| `work` | 144 | 560 |
| `mcp` | 140 | 850 |
| `svyazi` | 133 | 1319 |
| `open` | 133 | 427 |
| `agents` | 128 | 728 |
| `claude` | 124 | 563 |
| `содержание` | 124 | 189 |
| `review` | 121 | 401 |
| `github` | 120 | 537 |
| `first` | 119 | 386 |
| `слой` | 118 | 386 |
| `document` | 117 | 624 |
| `infrastructure` | 117 | 514 |
| `project` | 116 | 406 |
| `layer` | 116 | 546 |
| `через` | 116 | 469 |
| `если` | 115 | 614 |
| `svend` | 112 | 531 |
| `reference` | 111 | 287 |
| `appendix` | 110 | 880 |
| `агентов` | 107 | 441 |
| `между` | 104 | 333 |
| `без` | 104 | 390 |
| `foundation` | 104 | 319 |
| `model` | 102 | 272 |
| `specific` | 101 | 377 |
| `architecture` | 100 | 412 |
| `только` | 98 | 326 |
| `проекты` | 96 | 210 |
| `research` | 95 | 355 |
| `быть` | 95 | 311 |
| `projects` | 95 | 301 |
| `каждый` | 94 | 301 |
| `memory` | 93 | 631 |
| `level` | 93 | 341 |
| `implementation` | 93 | 235 |
| `context` | 92 | 231 |
| `pattern` | 92 | 346 |
| `structure` | 92 | 237 |
| `legal` | 91 | 408 |
| `integration` | 91 | 305 |
| `один` | 90 | 390 |
| `human` | 90 | 244 |
| `code` | 89 | 306 |
| `может` | 89 | 397 |
| `search` | 87 | 621 |
| `статус` | 87 | 146 |
| `author` | 87 | 252 |
| `cowork` | 87 | 955 |
| `source` | 86 | 214 |
| `проект` | 86 | 356 |
| `которые` | 86 | 328 |
| `когда` | 86 | 247 |
| `ingit` | 86 | 815 |
| `professional` | 86 | 370 |
| `what` | 86 | 542 |
| `through` | 86 | 184 |
| `collaboration` | 85 | 256 |
| `working` | 85 | 215 |
| `вопросы` | 84 | 260 |
| `sgb` | 84 | 474 |
| `existing` | 84 | 271 |
| `все` | 83 | 235 |
| `описание` | 83 | 128 |
| `api` | 83 | 232 |
| `skills` | 83 | 282 |
| `документов` | 83 | 176 |
| `readme` | 82 | 310 |
| `содержит` | 82 | 94 |
| `знаний` | 81 | 189 |
| `где` | 81 | 287 |
| `collaborations` | 80 | 436 |
| `tip` | 80 | 80 |
| `архитектура` | 79 | 232 |
| `вопрос` | 79 | 251 |
| `mvp` | 78 | 289 |
| `habr` | 78 | 361 |
| `агент` | 78 | 416 |
| `space` | 76 | 264 |
| `который` | 76 | 370 |
| `okwf` | 76 | 311 |
| `llm` | 75 | 328 |
| `tool` | 75 | 220 |
| `уже` | 74 | 385 |
| `репо` | 74 | 337 |
| `all` | 74 | 153 |


### 61. Топ биграмм (устойчивые словосочетания)
_Файл: `docs/KEYWORD_INDEX.md` | 3 колонок, 30 строк_

| Биграмм | Файлов | Всего |
|---------|--------|-------|
| `anthropic vacancies` | 354 | 5323 |
| `docs anthropic` | 350 | 5298 |
| `portal protocol` | 68 | 361 |
| `vacancies appendix` | 52 | 381 |
| `docs collaborations` | 50 | 384 |
| `docs svyazi` | 46 | 649 |
| `professional colleague` | 43 | 198 |
| `nautilus portal` | 41 | 181 |
| `executive summary` | 40 | 183 |
| `NGT Memory` | 40 | 152 |
| `appendix minimal` | 36 | 94 |
| `minimal working` | 36 | 94 |
| `working example` | 36 | 94 |
| `turn view` | 34 | 935 |
| `knowledge-space` | 34 | 199 |
| `representative agent` | 34 | 145 |
| `table contents` | 34 | 174 |
| `double triangle` | 33 | 175 |
| `triangle architecture` | 33 | 121 |
| `composite skills` | 33 | 115 |
| `ingit cowork` | 32 | 104 |
| `vacancies abstract` | 31 | 89 |
| `principal side` | 31 | 114 |
| `oss проект` | 30 | 145 |
| `colleague agents` | 30 | 92 |
| `view turn` | 29 | 661 |
| `pattern library` | 29 | 112 |
| `skills agent` | 29 | 92 |
| `cite turn` | 28 | 489 |
| `nautilus json` | 28 | 118 |


### 62. Количество (306)
_Файл: `docs/KPI.md` | 3 колонок, 21 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **429** | ициальных данных Anthropic Статья даёт только общие цифры (≈429 вакансий, вилка  | `00-intro` |
| **10** | овую повестку. А вы производите не исполнение, а повестку : 10 проектов, каждый  | `00-intro` |
| **27** | ным». У внешнего наблюдателя такой pattern читается иначе: «27 проектов с одной  | `00-intro` |
| **400** | задача спрос рождает предложение есть спрос например около 400 вакансий в антроп | `01-интегральный-анализ-пр` |
| **5** | т candidates формирование нескольких параллельных команд (3-5 команд по 5 челове | `01-интегральный-анализ-пр` |
| **70** | унт svend4 — это сейчас центральная точка организации ваших 70 проектов и вашей  | `01-интегральный-анализ-пр` |
| **440** | е отдельные темы , а проекции одной архитектуры . Anthropic 440 вакансий — это д | `150-appendix-c-version-hi` |
| **7** | v1.1 , формальная спецификация под текущую реальность репо (7 участников, 5 спос | `72-расписание-фазы-3` |
| **4** | fix run_all missing scripts _59617c5d_ _→ CHANGELOG_ - (4 файлов)](#кластер-26-m | `ACTION_ITEMS` |
| **40** | м` \| якорь не найден \| \| `docs/DECISIONS.md` \| `LiteParse` (40 файлов) \| `# | `BROKEN_LINKS` |
| **36** | -файлов` \| якорь не найден \| \| `docs/DECISIONS.md` \| `BSL` (36 файлов) \| `# | `BROKEN_LINKS` |
| **22** | зких файлов > - [Кластер 1 — cowork, ingit, yes, project (22 файлов)](#кластер-1 | `CLUSTERS` |
| **17** | айлов) - [Кластер 2 — professional, agent, colleague, type (17 файлов)](#кластер | `CLUSTERS` |
| **16** | ue-type-17-файлов) - [Кластер 3 — turn, view, cite, search (16 файлов)](#кластер | `CLUSTERS` |
| **15** | search-16-файлов) - [Кластер 4 — repo, passport, npp, json (15 файлов)](#кластер | `CLUSTERS` |
| **14** | -15-файлов) - [Кластер 6 — документ, document, com, github (14 файлов)](#кластер | `CLUSTERS` |
| **13** | github-14-файлов) - [Кластер 7 — turn, view, label, svyazi (13 файлов)](#кластер | `CLUSTERS` |
| **11** | vyazi-13-файлов) - [Кластер 8 — contents, table, why, call (11 файлов)](#кластер | `CLUSTERS` |
| **8** | лов) - [Кластер 11 — editorial, collaboration, draft, date (8 файлов)](#кластер- | `CLUSTERS` |
| **6** | - [Кластер 15 — infrastructure, populations, okwf, target (6 файлов)](#кластер-1 | `CLUSTERS` |
| _...ещё 286_ | | |


### 63. Количество (306)
_Файл: `docs/KPI.md` | 3 колонок, 21 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **34** | g-68-ролей) - [Sales — 150 ролей (самый большой кластер, ≈34% всего найма)](#sal | `00-intro` |
| **90** | Посадить такого человека в FDE-роль — значит амортизировать 90% реальной силы. Б | `00-intro` |
| **80** | ь README на английский как primary, русский как secondary — 80% вашей потенциаль | `00-intro` |
| **25** | цправу. Единственная proxy-проблема: роль SF-based, require 25% office presence  | `01-интегральный-анализ-пр` |
| **70** | большинства кандидатов. Но это означает, что оставшиеся 60-70% вашей деятельност | `01-интегральный-анализ-пр` |
| **100** | дата на каждую из них найти трудно — мало людей попадает на 100% под требования, | `01-интегральный-анализ-пр` |
| **40** | temporal coordination cost между незнакомцами в среднем 25-40% времени проекта.  | `01-интегральный-анализ-пр` |
| **30** | не прорывно — рынок тут уже есть, маржа тонкая, AI даёт 20-30% ускорение, не пор | `01-интегральный-анализ-пр` |
| **88** | как normative field. Это критично: STATUS.md явно признаёт 88% fallback. Нормали | `104-appendix-c-references` |
| **15** | огии: предотвращение потери. Эмпирический факт: минимум 10-15% контента каждого  | `109-3-принципы-консолидац` |
| **36** | nt employment covers declining fraction of knowledge work. 36% of US workers eng | `155-1-problem-statement` |
| **27** | workers engage in freelance/contract work in 2026, up from 27% in 2020. Foundati | `155-1-problem-statement` |
| **0** | harged fees or subjected to rent-seeking. Foundation takes 0% from contributor e | `160-6-governance-and-ethi` |
| **75** | th 100+ public patterns - Contributor satisfaction survey: >75% positive - Publi | `161-7-phased-rollout-plan` |
| **700** | нтов с advisors с 1300+ data points. SmartMatchApp заявляет 700% увеличение enga | `165-closing` |
| **20** | nd later studios. **Mechanics**: Agents typically take 10-20% commission of clie | `171-2-historical-preceden` |
| **10** | r planning. **Mechanics**: Similar commission structure (3-10% in sports, typica | `171-2-historical-preceden` |
| **7** | negotiation, paperwork. **Mechanics**: Commission-based (5-7% typical), split be | `171-2-historical-preceden` |
| **50** | s. ### 8.7. Expected Outcomes **For practitioners**: - 30-50% time reduction on  | `219-8-pilot-proposal-sgb-` |
| **95** | - Cost vs. external lawyer: 80-90% saving - Quality target: 95% citation accurac | `341-приложение-c-образец-` |
| _...ещё 172_ | | |


### 64. Количество (306)
_Файл: `docs/KPI.md` | 3 колонок, 21 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **4–6** | з свободного текста получаются устойчивые профили и связи \| 4–6 дней \| \| Evid | `07-mvp-planning` |
| **1–2** | \| Unified cards + page/span evidence + manual reviewer UI \| 1–2 недели \| Пере | `12-roadmap` |
| **1** | и patch \| benchmark set + nightly eval + rollback policy \| 1 неделя на каркас, | `12-roadmap` |
| **15** | й журнал» в инженерном смысле. Это архив 1105 разговоров за 15 месяцев (dec 2024 | `00-intro` |
| **6** | r-track . Entrepreneur First (Paris, Berlin) — программа на 6 месяцев с €80K сти | `00-intro` |
| **3** | в GitHub как отдельная секция). Потенциал от 1⭐ до 500⭐ за 3 месяца — абсолютно  | `00-intro` |
| **2–3** | ери ко всему остальному. daten — стратегический, но требует 2–3 недели работы на | `00-intro` |
| **19** | зиторий — daten2 , 25 декабря 2025. Самый свежий — data50 , 19 часов назад. Это  | `00-intro` |
| **4** | , 19 часов назад. Это означает, что все 70 репо созданы за 4 месяца , темп — 1 р | `00-intro` |
| **30-45** | м на восприятие профиля. ### Итоговая целевая картина Через 30-45 дней вашего со | `00-intro` |
| **120** | Что мы теперь знаем точно Темп и объём. 70 репозиториев за 120 дней (декабрь 202 | `01-интегральный-анализ-пр` |
| **40** | e дроны). Эти гранты не требуют от вас переезжать, работать 40 часов, иметь PhD  | `01-интегральный-анализ-пр` |
| **10-5** | иона долларов на одну одного разработчика будет поделены на 10-5 частей и она не | `01-интегральный-анализ-пр` |
| **6-12** | ративные программы, которые берут нестандартных одиночек на 6-12 месяцев, обучаю | `01-интегральный-анализ-пр` |
| **2-3** | человек, которые не знают друг друга, будут тратить первые 2-3 месяца на выстраи | `01-интегральный-анализ-пр` |
| **3-6** | манд (3-5 команд по 5 человек), команды работают независимо 3-6 месяцев, агент м | `01-интегральный-анализ-пр` |
| **4-6** | ner (может быть Anthropic или Mistral). Proposal пишется за 4-6 недель, шанс 15- | `01-интегральный-анализ-пр` |
| **2** | икуются в общий «доска квестов»: могут быть микро (fix bug, 2 часа, XP уровня 50 | `01-интегральный-анализ-пр` |
| **1-2** | fix bug, 2 часа, XP уровня 50), средние (implement feature, 1-2 недели, XP и cur | `01-интегральный-анализ-пр` |
| **3–5** | я бы делал в следующие две недели в порядке ROI. День 1–2 (3–5 часов): fix broke | `01-интегральный-анализ-пр` |
| _...ещё 299_ | | |


### 65. Количество (306)
_Файл: `docs/KPI.md` | 3 колонок, 21 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **$320** | hropic Статья даёт только общие цифры (≈429 вакансий, вилка $320–405 тыс.) и наз | `00-intro` |
| **$405K** | инженерные менеджеры Inference/GPU. Именно здесь «вилка до $405K» осмысленна. ## | `00-intro` |
| **$180** | для FDE в EMEA обычно ниже, чем для Research Engineer в SF ($180–280K в пересчёт | `00-intro` |
| **€3** | , а основатель . У вас есть готовые MVP-backlog'и, бюджеты (€3–5K минимальный, € | `00-intro` |
| **€16K** | вас есть готовые MVP-backlog'и, бюджеты (€3–5K минимальный, €16K полный для Smar | `00-intro` |
| **€80K** | trepreneur First (Paris, Berlin) — программа на 6 месяцев с €80K стипендией, спе | `00-intro` |
| **€29** | сли этот один проект дойдёт до 100 платящих пользователей × €29/мес = €2.9K/мес  | `00-intro` |
| **€2.9K** | дин проект дойдёт до 100 платящих пользователей × €29/мес = €2.9K/мес MRR — это  | `00-intro` |
| **€250K** | я заявка. Гранты под конкретные кластеры. Aktion Mensch (до €250K на проекты инк | `01-интегральный-анализ-пр` |
| **€3K** | ий . DPMA (Deutsches Patent- und Markenamt) с госпошлинами ~€3K за каждый + pate | `01-интегральный-анализ-пр` |
| **$500K** | ondon). Что, если вместо найма одного человека за, условно, $500K в год, этот бю | `01-интегральный-анализ-пр` |
| **$100K** | es. Корпорация типа Anthropic не может просто так разослать $100K в Дрезден, Буэ | `01-интегральный-анализ-пр` |
| **€4** | ted research teams for beneficial AI deployments». Грант до €4M, 3 года. Disabil | `01-интегральный-анализ-пр` |
| **$10** | нчурная траектория — рискованная, но если thesis верна, это $10-50M Series A чер | `01-интегральный-анализ-пр` |
| **€20** | а получить работающий документированный кейс . 3-6 месяцев, €20-50K. Это станови | `01-интегральный-анализ-пр` |
| **€1** | ect . EIC Pathfinder Open или Horizon Europe HumanE AI Net. €1-4M грант на 2-3 г | `01-интегральный-анализ-пр` |
| **$3** | artup . Entrepreneur First Berlin, Y Combinator, Seed Round $3-5M. Требует cofou | `01-интегральный-анализ-пр` |
| **$5** | Google DeepMind, Microsoft AI, Mistral, Anthropic), budget $5-20M/year, which: - | `150-appendix-c-version-hi` |
| **$1** | - Provides minimum stipend (не full salary, но dignified — $1-3K/month part-time | `150-appendix-c-version-hi` |
| **€500** | es. Economic layer: - Base stipend для active contributors (€500-1500/month part | `150-appendix-c-version-hi` |
| _...ещё 519_ | | |


### 66. Количество (306)
_Файл: `docs/KPI.md` | 3 колонок, 8 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **80** | y‑слое**: Auto AI Router даёт lightweight sidecar в Go с 30–80 MB RAM и OpenAI‑с | `04-ensembles-overview` |
| **78** | архив 1105 разговоров за 15 месяцев (dec 2024 → mar 2026), 78 МБ текста, 29 802  | `00-intro` |
| **7.4** | у: Первый — статистика по 10 кластерам . Главный по объёму (7.4 МБ / 300 разгово | `00-intro` |
| **4.6** | Следующие три по потенциалу — дроны и SkyMediaHub Bavaria (4.6 МБ, 13 конкретных | `00-intro` |
| **4.1** | ми партнёрам Fraunhofer/Bundeswehr/TechHUB SVI), ИИ/агенты (4.1 МБ), и робототех | `00-intro` |
| **2.0** | ndeswehr/TechHUB SVI), ИИ/агенты (4.1 МБ), и робототехника (2.0 МБ, 15 роботов с | `00-intro` |
| **2** | право 7.4 МБ, дроны 4.6 МБ, ИИ-агенты 4.1 МБ, робототехника 2 МБ. Центральные те | `01-интегральный-анализ-пр` |
| **16** | push-to-talk с Pause-key, Whisper large-v3-turbo на NVIDIA 16GB или Apple Silico | `00-intro` |


### 67. Количество (306)
_Файл: `docs/KPI.md` | 3 колонок, 18 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **0.1.5** | **MIT**. citeturn33view4turn27view0 \| Рабочий прототип, версия 0.1.5; “рабо | `03-component-catalog` |
| **4.5** | veloper для Claude-платформы : 87 skills, chat-migration v1→v4.5 quantum-hybrid, | `00-intro` |
| **1.0** | ntrag auf PB/Fristverlängerung/Nachzahlung), Master Dossier v1.0, анализ BSG-пра | `00-intro` |
| **1.1** | овместимости (0–3) - Как версионируется сам протокол (v1.0, v1.1, breaking chang | `02-общий-план-развития-na` |
| **2.0** | ем понадобится writing — это отдельный extension протокола (v2.0 или как опциона | `02-общий-план-развития-na` |
| **1.0.0** | desyncronize). Каждый релиз — git tag + CHANGELOG. Semver: v1.0.0, v1.0.1, v1.1. | `02-общий-план-развития-na` |
| **1.0.1** | onize). Каждый релиз — git tag + CHANGELOG. Semver: v1.0.0, v1.0.1, v1.1.0. CHAN | `02-общий-план-развития-na` |
| **1.1.0** | Каждый релиз — git tag + CHANGELOG. Semver: v1.0.0, v1.0.1, v1.1.0. CHANGELOG.md | `02-общий-план-развития-na` |
| **0.2.0** | 98-appendix-a-minimal-working-example.md) _33%_ - [Planned (v0.2.0)](132-planned | `04-abstract` |
| **3.1.0** | RFCs to Indicate Requirement Levels - OpenAPI Specification v3.1.0 (for REST API | `104-appendix-c-references` |
| **1.2** | прямое следствие этого. #### Что я сознательно оставил для v1.2 или v2.0 Formal  | `104-appendix-c-references` |
| **3.0** | Удалить transitional header 7. Добавить changelog-запись: «v3.0 consolidated fro | `110-вопрос-fallback-ratio` |
| **0.6.0** | laude (Анастасия Бутова, AnastasiyaW) — реально существует, версия 0.6.0, MIT, 1 | `365-развёрнутый-анализ-вн` |
| **3.2** | viewer 1 (GPT-5.4): проверяет логику - Reviewer 2 (DeepSeek-V3.2): проверяет --- | `02-knowledge-graphs` |
| **0.1** | st per card, trace completeness. MVP boundary: что входит в v0.1, что запрещено  | `14-ограничения-лицензии-и` |
| **0.2** | leteness. MVP boundary: что входит в v0.1, что запрещено до v0.2. Pilot scenario | `14-ограничения-лицензии-и` |
| **0.11.0** | лицензия. К 23 апреля 2026 (несколько дней назад) — версия v0.11.0 с 95 600+ звё | `TABLES` |
| **5.0.6** | 2026` \\| азработка : версии HMP-0001 → HMP-0005 (март 2026, версия 5.0.6) - Док | `TABLES` |


### 68. Количество (306)
_Файл: `docs/KPI.md` | 3 колонок, 7 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **10** | nts (≈8 репо)](#кластер-4-archives-experiments-8-репо) - [Топ-10 репо, в которые | `00-intro` |
| **5** | sh/git), либо помочь с English README-драфтом для одного из топ-5, либо проработ | `00-intro` |
| **30** | обратных ссылок **Файлов с входящими ссылками:** 1060 ## Топ-30 самых цитируемых | `BACKLINKS` |
| **20** | е` \| файл не существует \| \| `docs/DECISIONS.md` \| Детали по топ-20 пробелам  | `BROKEN_LINKS` |
| **15** | 78% \| 78% \| \| **root** \| 63 \| 22.1 \| 1.1 \| 67% \| 69% \| ## Топ-15 лучших | `METRICS` |
| **50** | 8527_ ### [Приоритеты файлов](PRIORITIES.md) > > !TIP - Топ-50 самых важных файл | `OUTLINE` |
| **3** | **Файлов проанализировано:** 433 Для каждого документа — топ-3 похожих по словар | `SIMILAR` |


### 69. Количество (306)
_Файл: `docs/KPI.md` | 3 колонок, 6 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **1** | les . Каждая фаза имеет smoke-test: завершена или нет. #### Фаза 1 — Спецификаци | `02-общий-план-развития-na` |
| **2** | адаптер для нового репо без задавания вопросов автору? #### Фаза 2 — Reference i | `02-общий-план-развития-na` |
| **3** | озвращает non-empty результат с consensus-информацией? #### Фаза 3 — MCP интерфе | `02-общий-план-развития-na` |
| **4** | кристалла», получить osmыслený ответ с указанием репо. #### Фаза 4 — Web interfa | `02-общий-план-развития-na` |
| **5** | y через браузер, получить отформатированный результат. #### Фаза 5 — Публикация  | `02-общий-план-развития-na` |
| **0** | ёртывания](#9-стратегия-поэтапного-развёртывания) - [9.1. Фаза 0 — Основание (Ме | `199-9-стратегия-поэтапног` |


### 70. Текущие метрики
_Файл: `docs/KPI_HISTORY.md` | 3 колонок, 7 строк_

| Метрика | Значение | Тренд |
|---------|---------|-------|
| Markdown документов | **529** | → |
| Слов | **523,868** | → |
| Скриптов | **125** | → |
| Скоринг | **93%** | → |
| Здоровье | **90/100** | → |
| KPI показателей | **737** | → |
| Открытых вопросов | **39** | → |


### 71. Индекс ссылок
_Файл: `docs/LINKS.md` | 2 колонок, 195 строк_

| URL | Найден в файлах |
|-----|-----------------|
| http://localhost:8000 | 13 |
| http://localhost:8080 | 9 |
| https://...install.sh | 7 |
| https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakansiy-s-zarplatoy-do-405000 | 7 |
| https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakans… | 5 |
| https://activitypub.rocks/ | 7 |
| https://api.github.com/users/svend4/repos?per_page=100&sort=updated | 9 |
| https://api.github.com/users/svend4/repos?per_page=100&sort=updated&type=owner | 9 |
| https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv | 7 |
| https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW | 7 |
| https://claude.com/product/cowork | 17 |
| https://creativecommons.org/licenses/by/4.0/ | 9 |
| https://forum.obsidian.md/t/new-plugin-llm-wiki-turn-your-vault-into-a-queryable-knowledge-base-privately/113223 | 9 |
| https://github | 6 |
| https://github.com/AnastasiyaW | 7 |
| https://github.com/AnastasiyaW/knowledge-space | 11 |
| https://github.com/AnastasiyaW/knowledge-space` | 7 |
| https://github.com/AnastasiyaW` | 3 |
| https://github.com/Antipozitive | 7 |
| https://github.com/Cutcode | 7 |
| https://github.com/Dmitriila | 7 |
| https://github.com/MiXaiLL76 | 7 |
| https://github.com/Sonia_Black | 7 |
| https://github.com/VitalyOborin | 7 |
| https://github.com/VitalyOborin/yodoca | 3 |
| https://github.com/VladSpace | 7 |
| https://github.com/andrey_chuyan | 7 |
| https://github.com/anthropics/mcp | 9 |
| https://github.com/anthropics/mcp` | 7 |
| https://github.com/camel-ai/camel | 9 |
| https://github.com/camel-ai/camel` | 2 |
| https://github.com/kksudo | 6 |
| https://github.com/kksudo/agentfs | 2 |
| https://github.com/kksudo` | 2 |
| https://github.com/mcp | 12 |
| https://github.com/mcp` | 6 |
| https://github.com/nlaik | 6 |
| https://github.com/settings/tokens | 8 |
| https://github.com/settings/tokens` | 6 |
| https://github.com/spbmolot | 6 |
| https://github.com/spbmolot/ngt-memory | 2 |
| https://github.com/spbmolot` | 2 |
| https://github.com/svend4/ | 6 |
| https://github.com/svend4/` | 4 |
| https://github.com/svend4/data70 | 10 |
| https://github.com/svend4/data70` | 6 |
| https://github.com/svend4/info1 | 16 |
| https://github.com/svend4/info1` | 6 |
| https://github.com/svend4/info40 | 8 |
| https://github.com/svend4/info7 | 8 |
| https://github.com/svend4/ingit | 26 |
| https://github.com/svend4/ingit/issues | 8 |
| https://github.com/svend4/ingit/issues` | 6 |
| https://github.com/svend4/ingit` | 6 |
| https://github.com/svend4/meta | 12 |
| https://github.com/svend4/meta` | 6 |
| https://github.com/svend4/nautilus | 28 |
| https://github.com/svend4/nautilus.git | 6 |
| https://github.com/svend4/nautilus/blob/claude/review-nautilus-changes-tdywx/README.md | 6 |
| https://github.com/svend4/nautilus/blob/main/INTEGRATION.md | 6 |
| https://github.com/svend4/nautilus/blob/main/PORTAL-PROTOCOL | 6 |
| https://github.com/svend4/nautilus/blob/main/PORTAL-PROTOCOL.md | 5 |
| https://github.com/svend4/nautilus/blob/main/README.md | 6 |
| https://github.com/svend4/nautilus/blob/main/REVIEW_METHODOLOGY.md | 5 |
| https://github.com/svend4/nautilus/blob/main/STATUS.md | 6 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_1.md | 6 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_2.md | 6 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_3.md | 6 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_4.md | 6 |
| https://github.com/svend4/nautilus/blob/main/docs/PORTAL-PROTOCOL-v1.0.md | 5 |
| https://github.com/svend4/nautilus/branches | 6 |
| https://github.com/svend4/nautilus/commits/main | 6 |
| https://github.com/svend4/nautilus/issues | 36 |
| https://github.com/svend4/nautilus/issues` | 6 |
| https://github.com/svend4/nautilus/tree/abfa80e853594454bae03e95ba09f12eb443ca50/docs | 6 |
| https://github.com/svend4/nautilus/tree/main/adapters | 6 |
| https://github.com/svend4/nautilus/tree/main/passports | 6 |
| https://github.com/svend4/nautilus` | 6 |
| https://github.com/svend4/pro2 | 16 |
| https://github.com/svend4/pro2/blob/main/nautilus/README.md | 6 |
| https://github.com/svend4/pro2/tree/6637d1299af963db66485aa5599346d41badc6dc/nautilus | 6 |
| https://github.com/svend4/pro2/tree/main/nautilus | 6 |
| https://github.com/svend4/pro2/tree/main/nautilus` | 4 |
| https://github.com/svend4/pro2` | 6 |
| https://github.com/svend4?tab=repositories | 6 |
| https://github.com/svend4?tab=repositories` | 4 |
| https://github.com/tagir_analyzes | 6 |
| https://github.com/zodigancode | 6 |
| https://habr. | 6 |
| https://habr.com/ru/articles/1002138/ | 8 |
| https://habr.com/ru/articles/1002138/` | 6 |
| https://habr.com/ru/articles/1005776/ | 8 |
| https://habr.com/ru/articles/1005776/` | 6 |
| https://habr.com/ru/articles/1006602/ | 6 |
| https://habr.com/ru/articles/1006602/, | 6 |
| https://habr.com/ru/articles/1006602/` | 6 |
| https://habr.com/ru/articles/1006622/ | 10 |
| https://habr.com/ru/articles/1006622/` | 6 |
| https://habr.com/ru/articles/1007122/ | 8 |
| https://habr.com/ru/articles/1007122/, | 6 |
| https://habr.com/ru/articles/1007122/` | 6 |
| https://habr.com/ru/articles/1009538/ | 8 |
| https://habr.com/ru/articles/1009538/` | 6 |
| https://habr.com/ru/articles/1009608/ | 8 |
| https://habr.com/ru/articles/1009608/` | 6 |
| https://habr.com/ru/articles/1009958/ | 8 |
| https://habr.com/ru/articles/1009958/` | 6 |
| https://habr.com/ru/articles/1010198/ | 8 |
| https://habr.com/ru/articles/1010198/` | 6 |
| https://habr.com/ru/articles/1010478/ | 8 |
| https://habr.com/ru/articles/1010478/` | 6 |
| https://habr.com/ru/articles/1012894/ | 6 |
| https://habr.com/ru/articles/1014366/ | 6 |
| https://habr.com/ru/articles/1016096/ | 8 |
| https://habr.com/ru/articles/1016096/` | 6 |
| https://habr.com/ru/articles/1017200/ | 8 |
| https://habr.com/ru/articles/1017200/` | 6 |
| https://habr.com/ru/articles/1019588/ | 6 |
| https://habr.com/ru/articles/1019588/, | 6 |
| https://habr.com/ru/articles/1019588/` | 6 |
| https://habr.com/ru/articles/1020598/ | 6 |
| https://habr.com/ru/articles/1020598/, | 6 |
| https://habr.com/ru/articles/1020598/` | 6 |
| https://habr.com/ru/articles/1020860/ | 8 |
| https://habr.com/ru/articles/1020860/` | 6 |
| https://habr.com/ru/articles/1021622/ | 6 |
| https://habr.com/ru/articles/1023446/ | 8 |
| https://habr.com/ru/articles/1023446/` | 6 |
| https://habr.com/ru/articles/1024634/ | 8 |
| https://habr.com/ru/articles/1024634/` | 6 |
| https://habr.com/ru/articles/1024884/comments/ | 8 |
| https://habr.com/ru/articles/1024884/comments/` | 6 |
| https://habr.com/ru/articles/1026666/ | 6 |
| https://habr.com/ru/articles/1027210/ | 8 |
| https://habr.com/ru/articles/1027210/` | 6 |
| https://habr.com/ru/articles/1027382/ | 8 |
| https://habr.com/ru/articles/1027382/` | 6 |
| https://habr.com/ru/articles/1027658/ | 8 |
| https://habr.com/ru/articles/1027658/` | 6 |
| https://habr.com/ru/articles/1027724/ | 10 |
| https://habr.com/ru/articles/1027724/` | 4 |
| https://habr.com/ru/articles/1027878/ | 6 |
| https://habr.com/ru/articles/1027878/, | 6 |
| https://habr.com/ru/articles/1027878/` | 6 |
| https://habr.com/ru/articles/495554/ | 6 |
| https://habr.com/ru/articles/893356/ | 8 |
| https://habr.com/ru/articles/893356/` | 6 |
| https://habr.com/ru/articles/938626/ | 6 |
| https://habr.com/ru/articles/938626/, | 6 |
| https://habr.com/ru/articles/938626/` | 6 |
| https://habr.com/ru/articles/943498/ | 6 |
| https://habr.com/ru/articles/943498/, | 6 |
| https://habr.com/ru/articles/943498/` | 6 |
| https://habr.com/ru/articles/955798/ | 8 |
| https://habr.com/ru/articles/955798/` | 6 |
| https://habr.com/ru/articles/975414/ | 8 |
| https://habr.com/ru/articles/975414/` | 6 |
| https://habr.com/ru/articles/983684/ | 8 |
| https://habr.com/ru/articles/983684/` | 6 |
| https://habr.com/ru/articles/996144/ | 8 |
| https://habr.com/ru/articles/996144/` | 6 |
| https://habr.com/ru/companies/airi/articles/1000720/ | 8 |
| https://habr.com/ru/companies/airi/articles/1000720/` | 6 |
| https://habr.com/ru/companies/airi/articles/855128/ | 8 |
| https://habr.com/ru/companies/airi/articles/855128/` | 6 |
| https://habr.com/ru/companies/surfstudio/articles/943108/ | 8 |
| https://habr.com/ru/companies/surfstudio/articles/943108/` | 6 |
| https://habr.com/ru/companies/teamly/articles/1024062/ | 6 |
| https://habr.com/ru/companies/yandex/articles/1019928/ | 8 |
| https://habr.com/ru/companies/yandex/articles/1019928/` | 6 |
| https://habr.com/ru/companies/yoomoney/articles/1012870/ | 8 |
| https://habr.com/ru/companies/yoomoney/articles/1012870/` | 6 |
| https://happyin.space/ | 6 |
| https://nautilus-okwf.org/sub-agents/sgb-ix-paragraph-78-24-7 | 6 |
| https://olegtalks.ru/base/tpost/xn7kev4fa1-docling-gotovim-dannie-dlya-rag-i-llm | 8 |
| https://raw.githubusercontent.com/svend4/nautilus/main/adapters/base.py | 8 |
| https://raw.githubusercontent.com/svend4/nautilus/main/glyph_adapter.py | 8 |
| https://raw.githubusercontent.com/svend4/nautilus/main/nautilus.json | 8 |
| https://raw.githubusercontent.com/svend4/nautilus/main/passports/info1.md | 8 |
| https://raw.githubusercontent.com/svend4/nautilus/main/portal.py | 8 |
| https://raw.githubusercontent.com/svend4/nautilus/main/requirements.txt | 8 |
| https://raw.githubusercontent.com/svend4/pro2/main/README.md | 8 |
| https://raw.githubusercontent.com/svend4/pro2/main/nautilus/README.md | 8 |
| https://raw.githubusercontent.com/svend4/pro2/main/nautilus/adapters/base.py | 8 |
| https://raw.githubusercontent.com/svend4/pro2/main/nautilus/adapters/info1.py | 8 |
| https://raw.githubusercontent.com/svend4/pro2/main/nautilus/nautilus.json | 8 |
| https://solidproject.org/ | 6 |
| https://support.claude.com/en/collections/13345190-cowork | 8 |
| https://vc.ru/id744101/2789872 | 8 |
| https://web.hypothes.is/ | 8 |
| https://www.camel-ai.org | 6 |
| https://www.discourse.org/ | 8 |
| https://www.fontanka.ru/2026/04/25/76378978/ | 14 |
| https://www.fossil-scm.org/ | 8 |
| https://www.w3.org/standards/semanticweb/data | 6 |


### 72. Качество по разделам
_Файл: `docs/METRICS.md` | 6 колонок, 6 строк_

| Раздел | Балл | Ссылок/1K слов | Код-блоков/1K | % с summary | % с тегами |
|--------|------|----------------|--------------|-------------|------------|
| **01-svyazi** | 72 | 30.7 | 0.5 | 100% | 100% |
| **02-anthropic-vacancies** | 77 | 50.8 | 0.7 | 100% | 100% |
| **03-technology-combinations** | 65 | 38.4 | 0.0 | 100% | 86% |
| **04-ai-collaborations** | 83 | 26.9 | 0.0 | 94% | 94% |
| **05-habr-projects** | 62 | 51.2 | 0.0 | 78% | 78% |
| **root** | 63 | 22.1 | 1.1 | 67% | 69% |


### 73. Топ-15 лучших документов
_Файл: `docs/METRICS.md` | 3 колонок, 15 строк_

| Документ | Балл | Слов |
|----------|------|------|
| `01-интегральный-анализ-профиля-svend4` | 100 | 19103 |
| `02-общий-план-развития-nautilus-portal-p` | 100 | 3181 |
| `109-3-принципы-консолидации-фаза-c` | 100 | 541 |
| `133-обратная-связь` | 100 | 16959 |
| `139-2-the-double-triangle-architecture` | 100 | 755 |
| `142-5-pattern-library-as-bridge-between-` | 100 | 689 |
| `228-appendix-c-quick-start-architecture-` | 100 | 1730 |
| `232-1-типология-из-пяти-типов-агентов-на` | 100 | 885 |
| `248-приложение-c-архитектура-быстрого-ст` | 100 | 3425 |
| `330-4-симбиотическая-архитектура` | 100 | 697 |
| `331-5-четыре-пути-интеграции-в-порядке-д` | 100 | 807 |
| `341-приложение-c-образец-спецификаций-ин` | 100 | 20414 |
| `342-что-такое-вариант-c-concept-document` | 100 | 11237 |
| `365-развёрнутый-анализ-внуковой-комбинац` | 100 | 4385 |
| `366-технический-stack-svyazi-2-0-foundat` | 100 | 3835 |


### 74. Документы, требующие улучшения (16)
_Файл: `docs/METRICS.md` | 3 колонок, 16 строк_

| Документ | Балл | Что отсутствует |
|----------|------|----------------|
| `ABBREVIATIONS` | 30 | summary, tags, TOC, callout |
| `AUTHORS` | 30 | summary, tags, TOC, callout |
| `BACKLINKS` | 30 | summary, tags, TOC, callout |
| `BROKEN_LINKS` | 30 | summary, tags, TOC, callout |
| `COMPLEXITY` | 30 | summary, tags, TOC, callout |
| `CROSSREFS` | 30 | summary, tags, TOC, callout |
| `DENSITY` | 30 | summary, tags, TOC, callout |
| `GLOSSARY` | 30 | summary, tags, TOC, callout |
| `KPI` | 30 | summary, tags, TOC, callout |
| `LINKS` | 30 | summary, tags, TOC, callout |
| `MISSING` | 30 | summary, tags, TOC, callout |
| `PRIORITIES` | 30 | summary, tags, TOC, callout |
| `QUESTIONS` | 30 | summary, tags, TOC, callout |
| `SENTIMENT` | 30 | summary, tags, TOC, callout |
| `TAGS` | 30 | summary, tags, TOC, callout |
| `WORD_FREQ` | 30 | summary, tags, TOC, callout |


### 75. Легенда
_Файл: `docs/MINDMAP.md` | 2 колонок, 7 строк_

| Слой | Проекты |
|------|---------|
| Ingestion | Svyazi, CardIndex, Firecrawl |
| Knowledge | AgentFS, knowledge-space |
| Memory | Yodoca, NGT Memory, MemNet |
| RAG | LiteParse, Legal RAG, Hybrid RAG, Graph RAG |
| Orchestration | mclaude, AI Factory, Rufler, AutoResearch |
| Security | LiteLLM, SENTINEL, Tool Search, Auto AI Router |
| Sync | Yjs, Automerge |


### 76. Карта пробелов знаний
_Файл: `docs/MISSING.md` | 6 колонок, 25 строк_

| Статус | Тема / Проект | Файлов | Слов | Минимум | Примеры файлов |
|--------|---------------|--------|------|---------|----------------|
| ✅ | **Svyazi** | 139 | 147259 | ≥5ф/2000сл | `WORD_FREQ.md`, `SCHEDULE.md` |
| ✅ | **local-first** | 86 | 76720 | ≥2ф/300сл | `FOOTNOTES.md`, `READING_TIME.md` |
| ✅ | **Yodoca** | 82 | 94054 | ≥2ф/300сл | `WORD_FREQ.md`, `SCHEDULE.md` |
| ✅ | **AgentFS** | 75 | 51824 | ≥3ф/500сл | `WORD_FREQ.md`, `SCHEDULE.md` |
| ✅ | **CardIndex** | 72 | 64659 | ≥3ф/500сл | `SCHEDULE.md`, `QUESTIONS.md` |
| ✅ | **self-improvement** | 68 | 10445 | ≥1ф/100сл | `FOOTNOTES.md`, `CONSISTENCY.md` |
| ✅ | **SENTINEL** | 63 | 42718 | ≥2ф/200сл | `SCHEDULE.md`, `FOOTNOTES.md` |
| ✅ | **knowledge-space** | 60 | 45031 | ≥3ф/500сл | `FOOTNOTES.md`, `BROKEN_LINKS.md` |
| ✅ | **Rufler** | 60 | 36210 | ≥2ф/200сл | `FOOTNOTES.md`, `GLOSSARY.md` |
| ✅ | **NGT Memory** | 58 | 46599 | ≥2ф/300сл | `GLOSSARY.md`, `CONSISTENCY.md` |
| ✅ | **LiteParse** | 56 | 40011 | ≥2ф/300сл | `TIMELINE.md`, `GLOSSARY.md` |
| ✅ | **mclaude** | 50 | 38201 | ≥2ф/200сл | `GLOSSARY.md`, `TABLES.md` |
| ✅ | **AI Factory** | 50 | 38849 | ≥2ф/200сл | `GLOSSARY.md`, `CONSISTENCY.md` |
| ✅ | **AutoResearch** | 31 | 25807 | ≥1ф/100сл | `GLOSSARY.md`, `CONTENT_GAPS.md` |
| ✅ | **Evidence Envelope** | 25 | 9677 | ≥2ф/200сл | `CONSISTENCY.md`, `TABLES.md` |
| ✅ | **Sozialrecht** | 24 | 65857 | ≥1ф/200сл | `READING_TIME.md`, `TABLES.md` |
| ✅ | **CRDT** | 22 | 17414 | ≥1ф/100сл | `FOOTNOTES.md`, `CONTENT_GAPS.md` |
| ✅ | **Card Envelope** | 15 | 7654 | ≥2ф/200сл | `TABLES.md`, `ACTION_ITEMS.md` |
| ✅ | **бюджетный роутинг** | 14 | 16685 | ≥2ф/300сл | `RISK_REGISTER.md`, `TABLES.md` |
| ✅ | **Memory Write Policy** | 11 | 6583 | ≥2ф/200сл | `QUESTIONS.md`, `TABLES.md` |
| ✅ | **Skill Policy** | 11 | 3730 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |
| ✅ | **Review Record** | 11 | 6235 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |
| ✅ | **privacy by design** | 11 | 11190 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |
| ✅ | **лицензия BSL** | 3 | 1439 | ≥1ф/50сл | `RISK_REGISTER.md`, `TABLES.md` |
| ✅ | **voice ingestion** | 2 | 760 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |


### 77. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 17 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `anthropic` | 401 | people |
| `claude` | 163 | people |
| `svend4` | 91 | people |
| `kksudo` | 52 | people |
| `spbmolot` | 47 | people |
| `vitalyoborin` | 23 | people |
| `anastasiyaw` | 23 | people |
| `andrey_chuyan` | 12 | people |
| `camel-ai` | 3 | people |
| `settings` | 2 | people |
| `anthropics` | 2 | people |
| `yjs` | 2 | people |
| `dementev-dev` | 2 | people |
| `artur-gavronchuk` | 2 | people |
| `nicholasspisak` | 2 | people |
| `vuguzum` | 2 | people |
| `users` | 2 | people |


### 78. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 40 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `nautilus` | 179 | projects |
| `svyazi` | 121 | projects |
| `github` | 121 | projects |
| `ngt` | 79 | projects |
| `yodoca` | 71 | projects |
| `agentfs` | 71 | projects |
| `CardIndex` | 68 | projects |
| `lorenzo` | 63 | projects |
| `knowledge-space` | 53 | projects |
| `LiteParse` | 47 | projects |
| `obsidian` | 36 | projects |
| `notion` | 32 | projects |
| `PortalEntry` | 30 | projects |
| `AutoResearch` | 25 | projects |
| `MemNet` | 22 | projects |
| `QueryResult` | 21 | projects |
| `wikontic` | 21 | projects |
| `VladSpace` | 20 | projects |
| `gpt` | 19 | projects |
| `gemini` | 10 | projects |
| `ingit` | 10 | projects |
| `OpenWhispr` | 9 | projects |
| `TypeScript` | 9 | projects |
| `BaseAdapter` | 9 | projects |
| `AutoGen` | 9 | projects |
| `CodeWiki` | 8 | projects |
| `mistral` | 8 | projects |
| `LangChain` | 8 | projects |
| `faiss` | 7 | projects |
| `DeepSeek` | 7 | projects |
| `DeepMind` | 7 | projects |
| `chromadb` | 7 | projects |
| `WebSocket` | 6 | projects |
| `ChatDev` | 6 | projects |
| `AutoAdapter` | 6 | projects |
| `DevOps` | 6 | projects |
| `OpenClaw` | 6 | projects |
| `LlamaIndex` | 5 | projects |
| `info1` | 5 | projects |
| `pro2` | 5 | projects |


### 79. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 29 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `mcp` | 146 | tech |
| `api` | 80 | tech |
| `rag` | 72 | tech |
| `llm` | 71 | tech |
| `json` | 59 | tech |
| `markdown` | 54 | tech |
| `git` | 48 | tech |
| `yaml` | 44 | tech |
| `python` | 43 | tech |
| `go` | 37 | tech |
| `rest` | 27 | tech |
| `html` | 15 | tech |
| `ci` | 14 | tech |
| `transformer` | 14 | tech |
| `sqlite` | 12 | tech |
| `cd` | 11 | tech |
| `vector` | 10 | tech |
| `react` | 9 | tech |
| `docker` | 7 | tech |
| `rust` | 7 | tech |
| `postgresql` | 6 | tech |
| `bm25` | 5 | tech |
| `jaccard` | 5 | tech |
| `cosine` | 3 | tech |
| `css` | 3 | tech |
| `fastapi` | 3 | tech |
| `webhook` | 3 | tech |
| `kubernetes` | 3 | tech |
| `graphql` | 2 | tech |


### 80. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 8 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `вк` | 126 | orgs |
| `meta` | 95 | orgs |
| `mail` | 32 | orgs |
| `openai` | 21 | orgs |
| `google` | 14 | orgs |
| `microsoft` | 11 | orgs |
| `yandex` | 6 | orgs |
| `сбер` | 4 | orgs |


### 81. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 30 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `2026-04` | 79 | dates |
| `2026-04-29` | 14 | dates |
| `2026-04-19` | 11 | dates |
| `апрель 2026` | 10 | dates |
| `2026-04-26` | 9 | dates |
| `апреля 2026` | 7 | dates |
| `2026/04/25` | 7 | dates |
| `в 2026 году` | 6 | dates |
| `март 2026` | 5 | dates |
| `декабрь 2025` | 5 | dates |
| `декабря 2025` | 4 | dates |
| `апреле 2026` | 4 | dates |
| `январе 2026` | 4 | dates |
| `марта 2026` | 3 | dates |
| `декабрь 2024` | 3 | dates |
| `2026-05-03` | 3 | dates |
| `2024-01-01` | 3 | dates |
| `2025-12-15` | 3 | dates |
| `май 2025` | 3 | dates |
| `феврале 2025` | 3 | dates |
| `2026-04-15` | 3 | dates |
| `Сентябрь 2025` | 3 | dates |
| `января 2026` | 3 | dates |
| `февраль 2026` | 3 | dates |
| `2026-04-22` | 3 | dates |
| `ноябре 2025` | 2 | dates |
| `2026-02-01` | 2 | dates |
| `2025-11-12` | 2 | dates |
| `февраля 2026` | 2 | dates |
| `2026-10-15` | 2 | dates |


### 82. Топ-20 ко-упоминаемых пар
_Файл: `docs/NETWORK.md` | 2 колонок, 20 строк_

| Пара | Общих файлов |
|------|-------------|
| **Cowork** ↔ **ingit** | 106 |
| **Svyazi** ↔ **NGT** | 78 |
| **Yodoca** ↔ **NGT** | 75 |
| **Svyazi** ↔ **Yodoca** | 71 |
| **Svyazi** ↔ **AgentFS** | 67 |
| **AgentFS** ↔ **NGT** | 65 |
| **AgentFS** ↔ **Yodoca** | 61 |
| **Svyazi** ↔ **CardIndex** | 57 |
| **CardIndex** ↔ **NGT** | 56 |
| **Андрей (kksudo)** ↔ **Виталий (spbmolot)** | 56 |
| **Svyazi** ↔ **SENTINEL** | 55 |
| **Svyazi** ↔ **Rufler** | 55 |
| **Svyazi** ↔ **Андрей (kksudo)** | 55 |
| **CardIndex** ↔ **AgentFS** | 53 |
| **AgentFS** ↔ **SENTINEL** | 53 |
| **Cowork** ↔ **Lorenzo (svend4)** | 52 |
| **Svyazi** ↔ **Lorenzo** | 51 |
| **Svyazi** ↔ **Виталий (spbmolot)** | 51 |
| **AgentFS** ↔ **Rufler** | 51 |
| **NGT** ↔ **Rufler** | 51 |


### 83. Центральность узлов (влиятельность)
_Файл: `docs/NETWORK.md` | 3 колонок, 20 строк_

| Узел | Балл центральности | Тип |
|------|--------------------|-----|
| **Svyazi** | 926 | 📦 Проект |
| **NGT** | 796 | 📦 Проект |
| **Yodoca** | 739 | 📦 Проект |
| **AgentFS** | 707 | 📦 Проект |
| **CardIndex** | 623 | 📦 Проект |
| **Rufler** | 588 | 📦 Проект |
| **SENTINEL** | 580 | 📦 Проект |
| **knowledge-space** | 575 | 📦 Проект |
| **Андрей (kksudo)** | 548 | 👤 Автор |
| **LiteParse** | 546 | 📦 Проект |
| **mclaude** | 512 | 📦 Проект |
| **AI Factory** | 502 | 📦 Проект |
| **Виталий (spbmolot)** | 498 | 👤 Автор |
| **ingit** | 473 | 📦 Проект |
| **Cowork** | 470 | 📦 Проект |
| **Lorenzo** | 455 | 📦 Проект |
| **Lorenzo (svend4)** | 405 | 👤 Автор |
| **MemNet** | 380 | 📦 Проект |
| **Wikontic** | 298 | 📦 Проект |
| **Firecrawl** | 137 | 📦 Проект |


### 84. Структура документации
_Файл: `docs/ONBOARDING.md` | 4 колонок, 5 строк_

| Раздел | Тема | Файлов | Слов |
|--------|------|--------|------|
| [`docs/01-svyazi/`](README.md) | Архитектура Svyazi 2.0 | 16 | 10,166 |
| [`docs/02-anthropic-vacancies/`](README.md) | Вакансии Anthropic | 357 | 260,905 |
| [`docs/03-technology-combinations/`](README.md) | Комбинации технологий | 7 | 2,433 |
| [`docs/04-ai-collaborations/`](README.md) | AI-коллаборации | 17 | 25,169 |
| [`docs/05-habr-projects/`](README.md) | Хабр-проекты | 10 | 8,564 |


### 85. Ключевые документы
_Файл: `docs/ONBOARDING.md` | 2 колонок, 8 строк_

| Документ | Зачем читать |
|----------|-------------|
| `docs/01-svyazi/01-executive-summary.md` | Общий обзор проекта — начни здесь |
| `docs/01-svyazi/07-mvp-planning.md` | MVP план, риски, оценки времени |
| `docs/01-svyazi/12-roadmap.md` | Дорожная карта по кварталам |
| `docs/01-svyazi/11-integration-contracts.md` | API-контракты между компонентами |
| `docs/CONTACTS.md` | Авторы компонентов и шаблоны писем |
| `docs/FAQ.md` | 54 вопроса и ответа |
| `docs/TECH_RADAR.md` | Что использовать, что избегать |
| `CLAUDE.md` | Гид по репо для Claude Code |


### 86. Архитектура компонентов
_Файл: `docs/ONBOARDING.md` | 4 колонок, 7 строк_

| Компонент | Роль | Лицензия | Автор |
|-----------|------|---------|-------|
| **CardIndex** | Индекс знаний (785+ карточек) | MIT | kksudo |
| **AgentFS** | Файловая система для AI | MIT | kksudo |
| **Yodoca** | Память с консолидацией | Apache 2.0 | spbmolot |
| **NGT-memory** | Ассоциативный граф памяти | BSL 1.1 | — |
| **SENTINEL** | Безопасность, allowlist MCP | MIT | — |
| **Rufler** | Оркестратор агентов | — | — |
| **Firecrawl** | Веб-краулер для AI | MIT | — |


### 87. Топ-20 по объёму (важные и изолированные)
_Файл: `docs/ORPHANS.md` | 3 колонок, 1 строк_

| Файл | Слов | Раздел |
|------|------|--------|
| `` | 67 | `autofilled` |


### 88. Типы проблем
_Файл: `docs/PARAGRAPH_QUALITY.md` | 2 колонок, 5 строк_

| Тип | Кол-во |
|-----|--------|
| ⚪ Короткий абзац | 4792 |
| ✂️  Оборванный | 2856 |
| 📏 Длинное предложение | 178 |
| 🔁 Повтор начала | 1248 |
| ♊ Дубль | 138 |


### 89. Состояние компонентов
_Файл: `docs/PROGRESS.md` | 3 колонок, 5 строк_

| Компонент | Статус | Детали |
|-----------|--------|--------|
| Контакты авторов | ⚠️ 14 файлов, не отправлено | 14 файлов в docs/contacts/ |
| LLM-обогащение | ⬜ не запущено | pip install anthropic && python scripts/improve_llm_enrich.py |
| Скрипты обработки | ✅ 125 скриптов | 5 LLM-скриптов, MCP=✅ |
| DIGEST.md | ✅ 5 секций | python scripts/improve_llm_summary.py |
| Claude Skills | ✅ 5 скиллов | review-docs, status, write-contact, improve, analyze-project |


### 90. Метрики качества
_Файл: `docs/PROGRESS.md` | 3 колонок, 3 строк_

| Метрика | Балл | Статус |
|---------|------|--------|
| Здоровье репо (HEALTH) | 90.0/100 | 🟢 |
| Качество доков (METRICS) | 73.4/100 | 🟡 |
| Go/No-Go (SCORING) | 93.0/100 | 🟡 |


### 91. Все документы
_Файл: `docs/READABILITY.md` | 6 колонок, 523 строк_

| Файл | FRE | Уровень | Слов | Пред. | Слов/пред. |
|------|-----|---------|------|-------|-----------|
| `docs/01-svyazi/01-executive-summary.md` | 0 | 🔴 Очень сложный | 690 | 44 | 15.7 |
| `docs/01-svyazi/02-methodology.md` | 0 | 🔴 Очень сложный | 374 | 26 | 14.4 |
| `docs/01-svyazi/03-component-catalog.md` | 0 | 🔴 Очень сложный | 1467 | 108 | 13.6 |
| `docs/01-svyazi/04-ensembles-overview.md` | 0 | 🔴 Очень сложный | 1134 | 60 | 18.9 |
| `docs/01-svyazi/06-security-privacy.md` | 0 | 🔴 Очень сложный | 825 | 45 | 18.3 |
| `docs/01-svyazi/07-mvp-planning.md` | 0 | 🔴 Очень сложный | 1065 | 60 | 17.8 |
| `docs/01-svyazi/08-conclusions.md` | 0 | 🔴 Очень сложный | 422 | 35 | 12.1 |
| `docs/01-svyazi/09-architectural-gaps.md` | 0 | 🔴 Очень сложный | 827 | 38 | 21.8 |
| `docs/01-svyazi/10-second-order-ensembles.md` | 0 | 🔴 Очень сложный | 832 | 49 | 17.0 |
| `docs/01-svyazi/11-integration-contracts.md` | 0 | 🔴 Очень сложный | 777 | 43 | 18.1 |
| `docs/01-svyazi/12-roadmap.md` | 0 | 🔴 Очень сложный | 736 | 44 | 16.7 |
| `docs/01-svyazi/13-contacts.md` | 0 | 🔴 Очень сложный | 880 | 55 | 16.0 |
| `docs/01-svyazi/14-limitations.md` | 0 | 🔴 Очень сложный | 697 | 45 | 15.5 |
| `docs/01-svyazi/QA.md` | 0 | 🔴 Очень сложный | 195 | 18 | 10.8 |
| `docs/02-anthropic-vacancies/00-intro.md` | 0 | 🔴 Очень сложный | 7709 | 496 | 15.5 |
| `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` | 0 | 🔴 Очень сложный | 17068 | 1230 | 13.9 |
| `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` | 0 | 🔴 Очень сложный | 2124 | 231 | 9.2 |
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | 0 | 🔴 Очень сложный | 259 | 26 | 10.0 |
| `docs/02-anthropic-vacancies/04-abstract.md` | 0 | 🔴 Очень сложный | 222 | 23 | 9.7 |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | 0 | 🔴 Очень сложный | 204 | 31 | 6.6 |
| `docs/02-anthropic-vacancies/06-1-introduction.md` | 0 | 🔴 Очень сложный | 380 | 44 | 8.6 |
| `docs/02-anthropic-vacancies/07-2-terminology.md` | 0 | 🔴 Очень сложный | 302 | 45 | 6.7 |
| `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` | 0 | 🔴 Очень сложный | 305 | 49 | 6.2 |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | 0 | 🔴 Очень сложный | 102 | 17 | 6.0 |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 0 | 🔴 Очень сложный | 30 | 1 | 30.0 |
| `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` | 0 | 🔴 Очень сложный | 244 | 28 | 8.7 |
| `docs/02-anthropic-vacancies/104-appendix-c-references.md` | 0 | 🔴 Очень сложный | 869 | 120 | 7.2 |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | 0 | 🔴 Очень сложный | 200 | 25 | 8.0 |
| `docs/02-anthropic-vacancies/106-tl-dr.md` | 0 | 🔴 Очень сложный | 201 | 24 | 8.4 |
| `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` | 0 | 🔴 Очень сложный | 334 | 31 | 10.8 |
| `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` | 0 | 🔴 Очень сложный | 333 | 41 | 8.1 |
| `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` | 0 | 🔴 Очень сложный | 305 | 30 | 10.2 |
| `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` | 0 | 🔴 Очень сложный | 207 | 25 | 8.3 |
| `docs/02-anthropic-vacancies/111-4-условия-применимости.md` | 0 | 🔴 Очень сложный | 272 | 24 | 11.3 |
| `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` | 0 | 🔴 Очень сложный | 268 | 31 | 8.6 |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 0 | 🔴 Очень сложный | 136 | 10 | 13.6 |
| `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` | 0 | 🔴 Очень сложный | 355 | 41 | 8.7 |
| `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | 0 | 🔴 Очень сложный | 343 | 39 | 8.8 |
| `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` | 0 | 🔴 Очень сложный | 229 | 24 | 9.5 |
| `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` | 0 | 🔴 Очень сложный | 224 | 32 | 7.0 |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | 0 | 🔴 Очень сложный | 43 | 2 | 21.5 |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | 0 | 🔴 Очень сложный | 178 | 21 | 8.5 |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 0 | 🔴 Очень сложный | 122 | 16 | 7.6 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 0 | 🔴 Очень сложный | 62 | 4 | 15.5 |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 0 | 🔴 Очень сложный | 43 | 5 | 8.6 |
| `docs/02-anthropic-vacancies/122-глоссарий.md` | 0 | 🔴 Очень сложный | 1200 | 124 | 9.7 |
| `docs/02-anthropic-vacancies/123-portal-mcp-py.md` | 0 | 🔴 Очень сложный | 232 | 26 | 8.9 |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | 0 | 🔴 Очень сложный | 231 | 25 | 9.2 |
| `docs/02-anthropic-vacancies/126-установка.md` | 0 | 🔴 Очень сложный | 142 | 18 | 7.9 |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | 0 | 🔴 Очень сложный | 198 | 22 | 9.0 |
| `docs/02-anthropic-vacancies/128-доступные-инструменты.md` | 0 | 🔴 Очень сложный | 235 | 24 | 9.8 |
| `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` | 0 | 🔴 Очень сложный | 219 | 28 | 7.8 |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | 0 | 🔴 Очень сложный | 132 | 16 | 8.2 |
| `docs/02-anthropic-vacancies/130-отладка.md` | 0 | 🔴 Очень сложный | 207 | 20 | 10.3 |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | 0 | 🔴 Очень сложный | 142 | 13 | 10.9 |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | 0 | 🔴 Очень сложный | 173 | 19 | 9.1 |
| `docs/02-anthropic-vacancies/133-обратная-связь.md` | 0 | 🔴 Очень сложный | 3458 | 224 | 15.4 |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 0 | 🔴 Очень сложный | 189 | 25 | 7.6 |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | 0 | 🔴 Очень сложный | 290 | 24 | 12.1 |
| `docs/02-anthropic-vacancies/136-abstract.md` | 0 | 🔴 Очень сложный | 476 | 36 | 13.2 |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | 0 | 🔴 Очень сложный | 275 | 29 | 9.5 |
| `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` | 0 | 🔴 Очень сложный | 734 | 66 | 11.1 |
| `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` | 0 | 🔴 Очень сложный | 868 | 83 | 10.5 |
| `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` | 0 | 🔴 Очень сложный | 703 | 63 | 11.2 |
| `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` | 0 | 🔴 Очень сложный | 688 | 66 | 10.4 |
| `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` | 0 | 🔴 Очень сложный | 717 | 77 | 9.3 |
| `docs/02-anthropic-vacancies/144-7-open-questions.md` | 0 | 🔴 Очень сложный | 830 | 81 | 10.2 |
| `docs/02-anthropic-vacancies/145-8-call-to-action.md` | 0 | 🔴 Очень сложный | 776 | 95 | 8.2 |
| `docs/02-anthropic-vacancies/146-acknowledgments.md` | 0 | 🔴 Очень сложный | 381 | 31 | 12.3 |
| `docs/02-anthropic-vacancies/147-references.md` | 0 | 🔴 Очень сложный | 352 | 66 | 5.3 |
| `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` | 0 | 🔴 Очень сложный | 390 | 45 | 8.7 |
| `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` | 0 | 🔴 Очень сложный | 286 | 32 | 8.9 |
| `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` | 0 | 🔴 Очень сложный | 4450 | 261 | 17.0 |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 0 | 🔴 Очень сложный | 186 | 25 | 7.4 |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | 0 | 🔴 Очень сложный | 274 | 24 | 11.4 |
| `docs/02-anthropic-vacancies/153-executive-summary.md` | 0 | 🔴 Очень сложный | 430 | 37 | 11.6 |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | 0 | 🔴 Очень сложный | 178 | 28 | 6.4 |
| `docs/02-anthropic-vacancies/155-1-problem-statement.md` | 0 | 🔴 Очень сложный | 667 | 52 | 12.8 |
| `docs/02-anthropic-vacancies/156-2-target-populations.md` | 0 | 🔴 Очень сложный | 691 | 42 | 16.5 |
| `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` | 0 | 🔴 Очень сложный | 710 | 54 | 13.1 |
| `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` | 0 | 🔴 Очень сложный | 981 | 43 | 22.8 |
| `docs/02-anthropic-vacancies/159-5-economic-model.md` | 0 | 🔴 Очень сложный | 557 | 56 | 9.9 |
| `docs/02-anthropic-vacancies/16-history.md` | 0 | 🔴 Очень сложный | 34 | 6 | 5.7 |
| `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` | 0 | 🔴 Очень сложный | 588 | 64 | 9.2 |
| `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` | 0 | 🔴 Очень сложный | 659 | 46 | 14.3 |
| `docs/02-anthropic-vacancies/162-8-risk-analysis.md` | 0 | 🔴 Очень сложный | 625 | 37 | 16.9 |
| `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` | 0 | 🔴 Очень сложный | 627 | 45 | 13.9 |
| `docs/02-anthropic-vacancies/164-10-appendices.md` | 0 | 🔴 Очень сложный | 794 | 47 | 16.9 |
| `docs/02-anthropic-vacancies/165-closing.md` | 0 | 🔴 Очень сложный | 6053 | 454 | 13.3 |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 0 | 🔴 Очень сложный | 195 | 25 | 7.8 |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | 0 | 🔴 Очень сложный | 343 | 26 | 13.2 |
| `docs/02-anthropic-vacancies/168-abstract.md` | 0 | 🔴 Очень сложный | 376 | 32 | 11.8 |
| `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` | 0 | 🔴 Очень сложный | 287 | 41 | 7.0 |
| `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` | 0 | 🔴 Очень сложный | 836 | 68 | 12.3 |
| `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` | 0 | 🔴 Очень сложный | 1015 | 97 | 10.5 |
| `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` | 0 | 🔴 Очень сложный | 747 | 95 | 7.9 |
| `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` | 0 | 🔴 Очень сложный | 1556 | 176 | 8.8 |
| `docs/02-anthropic-vacancies/174-5-architectural-specification.md` | 0 | 🔴 Очень сложный | 686 | 80 | 8.6 |
| `docs/02-anthropic-vacancies/175-6-ethical-framework.md` | 0 | 🔴 Очень сложный | 636 | 65 | 9.8 |
| `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` | 0 | 🔴 Очень сложный | 519 | 46 | 11.3 |
| `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` | 0 | 🔴 Очень сложный | 710 | 62 | 11.5 |
| `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` | 0 | 🔴 Очень сложный | 595 | 45 | 13.2 |
| `docs/02-anthropic-vacancies/179-10-open-questions.md` | 0 | 🔴 Очень сложный | 470 | 61 | 7.7 |
| `docs/02-anthropic-vacancies/18-6-adapter-interface.md` | 0 | 🔴 Очень сложный | 308 | 45 | 6.8 |
| `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` | 0 | 🔴 Очень сложный | 457 | 56 | 8.2 |
| `docs/02-anthropic-vacancies/182-acknowledgments.md` | 0 | 🔴 Очень сложный | 312 | 27 | 11.6 |
| `docs/02-anthropic-vacancies/183-references.md` | 0 | 🔴 Очень сложный | 351 | 51 | 6.9 |
| `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` | 0 | 🔴 Очень сложный | 384 | 29 | 13.2 |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 0 | 🔴 Очень сложный | 95 | 12 | 7.9 |
| `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` | 0 | 🔴 Очень сложный | 1938 | 162 | 12.0 |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | 0 | 🔴 Очень сложный | 181 | 24 | 7.5 |
| `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` | 0 | 🔴 Очень сложный | 230 | 25 | 9.2 |
| `docs/02-anthropic-vacancies/189-аннотация.md` | 0 | 🔴 Очень сложный | 232 | 9 | 25.8 |
| `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` | 0 | 🔴 Очень сложный | 184 | 26 | 7.1 |
| `docs/02-anthropic-vacancies/190-содержание.md` | 0 | 🔴 Очень сложный | 182 | 31 | 5.9 |
| `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | 0 | 🔴 Очень сложный | 627 | 52 | 12.1 |
| `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | 0 | 🔴 Очень сложный | 783 | 74 | 10.6 |
| `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` | 0 | 🔴 Очень сложный | 625 | 84 | 7.4 |
| `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` | 0 | 🔴 Очень сложный | 1453 | 171 | 8.5 |
| `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` | 0 | 🔴 Очень сложный | 604 | 68 | 8.9 |
| `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` | 0 | 🔴 Очень сложный | 423 | 35 | 12.1 |
| `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` | 0 | 🔴 Очень сложный | 334 | 21 | 15.9 |
| `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` | 0 | 🔴 Очень сложный | 584 | 45 | 13.0 |
| `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` | 0 | 🔴 Очень сложный | 471 | 30 | 15.7 |
| `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` | 0 | 🔴 Очень сложный | 245 | 32 | 7.7 |
| `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` | 0 | 🔴 Очень сложный | 335 | 39 | 8.6 |
| `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` | 0 | 🔴 Очень сложный | 374 | 46 | 8.1 |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | 0 | 🔴 Очень сложный | 160 | 14 | 11.4 |
| `docs/02-anthropic-vacancies/203-благодарности.md` | 0 | 🔴 Очень сложный | 179 | 15 | 11.9 |
| `docs/02-anthropic-vacancies/204-ссылки.md` | 0 | 🔴 Очень сложный | 286 | 52 | 5.5 |
| `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` | 0 | 🔴 Очень сложный | 279 | 29 | 9.6 |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 0 | 🔴 Очень сложный | 108 | 14 | 7.7 |
| `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` | 0 | 🔴 Очень сложный | 2265 | 153 | 14.8 |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | 0 | 🔴 Очень сложный | 193 | 26 | 7.4 |
| `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` | 0 | 🔴 Очень сложный | 312 | 26 | 12.0 |
| `docs/02-anthropic-vacancies/21-9-query-flow.md` | 0 | 🔴 Очень сложный | 236 | 44 | 5.4 |
| `docs/02-anthropic-vacancies/210-abstract.md` | 0 | 🔴 Очень сложный | 405 | 31 | 13.1 |
| `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | 0 | 🔴 Очень сложный | 913 | 108 | 8.5 |
| `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` | 0 | 🔴 Очень сложный | 906 | 114 | 7.9 |
| `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | 0 | 🔴 Очень сложный | 885 | 76 | 11.6 |
| `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` | 0 | 🔴 Очень сложный | 966 | 117 | 8.3 |
| `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` | 0 | 🔴 Очень сложный | 792 | 83 | 9.5 |
| `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` | 0 | 🔴 Очень сложный | 1247 | 167 | 7.5 |
| `docs/02-anthropic-vacancies/218-7-application-domains.md` | 0 | 🔴 Очень сложный | 806 | 110 | 7.3 |
| `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` | 0 | 🔴 Очень сложный | 943 | 77 | 12.2 |
| `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` | 0 | 🔴 Очень сложный | 199 | 28 | 7.1 |
| `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` | 0 | 🔴 Очень сложный | 717 | 78 | 9.2 |
| `docs/02-anthropic-vacancies/221-10-open-questions.md` | 0 | 🔴 Очень сложный | 518 | 71 | 7.3 |
| `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` | 0 | 🔴 Очень сложный | 448 | 59 | 7.6 |
| `docs/02-anthropic-vacancies/223-12-closing.md` | 0 | 🔴 Очень сложный | 462 | 42 | 11.0 |
| `docs/02-anthropic-vacancies/224-acknowledgments.md` | 0 | 🔴 Очень сложный | 312 | 27 | 11.6 |
| `docs/02-anthropic-vacancies/225-references.md` | 0 | 🔴 Очень сложный | 357 | 57 | 6.3 |
| `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | 0 | 🔴 Очень сложный | 430 | 23 | 18.7 |
| `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` | 0 | 🔴 Очень сложный | 424 | 25 | 17.0 |
| `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` | 0 | 🔴 Очень сложный | 1455 | 105 | 13.9 |
| `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` | 0 | 🔴 Очень сложный | 249 | 26 | 9.6 |
| `docs/02-anthropic-vacancies/23-11-security-considerations.md` | 0 | 🔴 Очень сложный | 243 | 29 | 8.4 |
| `docs/02-anthropic-vacancies/230-аннотация.md` | 0 | 🔴 Очень сложный | 345 | 30 | 11.5 |
| `docs/02-anthropic-vacancies/231-содержание.md` | 0 | 🔴 Очень сложный | 201 | 34 | 5.9 |
| `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | 0 | 🔴 Очень сложный | 830 | 112 | 7.4 |
| `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` | 0 | 🔴 Очень сложный | 780 | 114 | 6.8 |
| `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | 0 | 🔴 Очень сложный | 691 | 65 | 10.6 |
| `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` | 0 | 🔴 Очень сложный | 784 | 105 | 7.5 |
| `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` | 0 | 🔴 Очень сложный | 678 | 75 | 9.0 |
| `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` | 0 | 🔴 Очень сложный | 1043 | 149 | 7.0 |
| `docs/02-anthropic-vacancies/238-7-области-применения.md` | 0 | 🔴 Очень сложный | 624 | 94 | 6.6 |
| `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` | 0 | 🔴 Очень сложный | 798 | 61 | 13.1 |
| `docs/02-anthropic-vacancies/24-12-versioning-policy.md` | 0 | 🔴 Очень сложный | 261 | 38 | 6.9 |
| `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` | 0 | 🔴 Очень сложный | 720 | 86 | 8.4 |
| `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` | 0 | 🔴 Очень сложный | 342 | 48 | 7.1 |
| `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` | 0 | 🔴 Очень сложный | 276 | 35 | 7.9 |
| `docs/02-anthropic-vacancies/243-12-заключение.md` | 0 | 🔴 Очень сложный | 386 | 37 | 10.4 |
| `docs/02-anthropic-vacancies/244-благодарности.md` | 0 | 🔴 Очень сложный | 210 | 26 | 8.1 |
| `docs/02-anthropic-vacancies/245-ссылки.md` | 0 | 🔴 Очень сложный | 320 | 57 | 5.6 |
| `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | 0 | 🔴 Очень сложный | 332 | 17 | 19.5 |
| `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` | 0 | 🔴 Очень сложный | 227 | 5 | 45.4 |
| `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | 0 | 🔴 Очень сложный | 2980 | 245 | 12.2 |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | 0 | 🔴 Очень сложный | 186 | 25 | 7.4 |
| `docs/02-anthropic-vacancies/25-13-reference-implementation.md` | 0 | 🔴 Очень сложный | 188 | 26 | 7.2 |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 0 | 🔴 Очень сложный | 18 | 1 | 18.0 |
| `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` | 0 | 🔴 Очень сложный | 320 | 27 | 11.9 |
| `docs/02-anthropic-vacancies/252-abstract.md` | 0 | 🔴 Очень сложный | 398 | 31 | 12.8 |
| `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` | 0 | 🔴 Очень сложный | 749 | 66 | 11.3 |
| `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` | 0 | 🔴 Очень сложный | 997 | 98 | 10.2 |
| `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` | 0 | 🔴 Очень сложный | 868 | 89 | 9.8 |
| `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` | 0 | 🔴 Очень сложный | 796 | 78 | 10.2 |
| `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` | 0 | 🔴 Очень сложный | 864 | 87 | 9.9 |
| `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` | 0 | 🔴 Очень сложный | 286 | 23 | 12.4 |
| `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` | 0 | 🔴 Очень сложный | 878 | 80 | 11.0 |
| `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` | 0 | 🔴 Очень сложный | 1064 | 72 | 14.8 |
| `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` | 0 | 🔴 Очень сложный | 813 | 70 | 11.6 |
| `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` | 0 | 🔴 Очень сложный | 853 | 65 | 13.1 |
| `docs/02-anthropic-vacancies/264-11-open-questions.md` | 0 | 🔴 Очень сложный | 714 | 81 | 8.8 |
| `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` | 0 | 🔴 Очень сложный | 504 | 52 | 9.7 |
| `docs/02-anthropic-vacancies/266-13-closing.md` | 0 | 🔴 Очень сложный | 485 | 41 | 11.8 |
| `docs/02-anthropic-vacancies/267-acknowledgments.md` | 0 | 🔴 Очень сложный | 353 | 33 | 10.7 |
| `docs/02-anthropic-vacancies/268-references.md` | 0 | 🔴 Очень сложный | 491 | 69 | 7.1 |
| `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | 0 | 🔴 Очень сложный | 329 | 29 | 11.3 |
| `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` | 0 | 🔴 Очень сложный | 206 | 26 | 7.9 |
| `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` | 0 | 🔴 Очень сложный | 243 | 19 | 12.8 |
| `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` | 0 | 🔴 Очень сложный | 298 | 24 | 12.4 |
| `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` | 0 | 🔴 Очень сложный | 3441 | 266 | 12.9 |
| `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` | 0 | 🔴 Очень сложный | 190 | 25 | 7.6 |
| `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` | 0 | 🔴 Очень сложный | 360 | 29 | 12.4 |
| `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` | 0 | 🔴 Очень сложный | 211 | 30 | 7.0 |
| `docs/02-anthropic-vacancies/285-closing.md` | 0 | 🔴 Очень сложный | 354 | 31 | 11.4 |
| `docs/02-anthropic-vacancies/286-acknowledgments.md` | 0 | 🔴 Очень сложный | 342 | 28 | 12.2 |
| `docs/02-anthropic-vacancies/287-references.md` | 0 | 🔴 Очень сложный | 373 | 27 | 13.8 |
| `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` | 0 | 🔴 Очень сложный | 948 | 91 | 10.4 |
| `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` | 0 | 🔴 Очень сложный | 292 | 31 | 9.4 |
| `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` | 0 | 🔴 Очень сложный | 304 | 33 | 9.2 |
| `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` | 0 | 🔴 Очень сложный | 363 | 33 | 11.0 |
| `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` | 0 | 🔴 Очень сложный | 435 | 45 | 9.7 |
| `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` | 0 | 🔴 Очень сложный | 283 | 36 | 7.9 |
| `docs/02-anthropic-vacancies/294-существующие-приближения.md` | 0 | 🔴 Очень сложный | 596 | 36 | 16.6 |
| `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` | 0 | 🔴 Очень сложный | 703 | 75 | 9.4 |
| `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` | 0 | 🔴 Очень сложный | 327 | 31 | 10.5 |
| `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` | 0 | 🔴 Очень сложный | 309 | 37 | 8.4 |
| `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` | 0 | 🔴 Очень сложный | 201 | 25 | 8.0 |
| `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` | 0 | 🔴 Очень сложный | 335 | 43 | 7.8 |
| `docs/02-anthropic-vacancies/300-заключение.md` | 0 | 🔴 Очень сложный | 282 | 28 | 10.1 |
| `docs/02-anthropic-vacancies/301-благодарности.md` | 0 | 🔴 Очень сложный | 267 | 29 | 9.2 |
| `docs/02-anthropic-vacancies/302-ссылки.md` | 0 | 🔴 Очень сложный | 242 | 21 | 11.5 |
| `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` | 0 | 🔴 Очень сложный | 1814 | 115 | 15.8 |
| `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` | 0 | 🔴 Очень сложный | 192 | 25 | 7.7 |
| `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | 0 | 🔴 Очень сложный | 161 | 22 | 7.3 |
| `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` | 0 | 🔴 Очень сложный | 385 | 33 | 11.7 |
| `docs/02-anthropic-vacancies/307-abstract.md` | 0 | 🔴 Очень сложный | 407 | 34 | 12.0 |
| `docs/02-anthropic-vacancies/31-content-overview.md` | 0 | 🔴 Очень сложный | 124 | 17 | 7.3 |
| `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` | 0 | 🔴 Очень сложный | 746 | 66 | 11.3 |
| `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` | 0 | 🔴 Очень сложный | 727 | 88 | 8.3 |
| `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` | 0 | 🔴 Очень сложный | 798 | 80 | 10.0 |
| `docs/02-anthropic-vacancies/319-acknowledgments.md` | 0 | 🔴 Очень сложный | 448 | 48 | 9.3 |
| `docs/02-anthropic-vacancies/320-references.md` | 0 | 🔴 Очень сложный | 231 | 36 | 6.4 |
| `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` | 0 | 🔴 Очень сложный | 209 | 19 | 11.0 |
| `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` | 0 | 🔴 Очень сложный | 1197 | 124 | 9.7 |
| `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | 0 | 🔴 Очень сложный | 291 | 33 | 8.8 |
| `docs/02-anthropic-vacancies/325-аннотация.md` | 0 | 🔴 Очень сложный | 348 | 34 | 10.2 |
| `docs/02-anthropic-vacancies/326-содержание.md` | 0 | 🔴 Очень сложный | 204 | 29 | 7.0 |
| `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` | 0 | 🔴 Очень сложный | 673 | 78 | 8.6 |
| `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` | 0 | 🔴 Очень сложный | 776 | 72 | 10.8 |
| `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` | 0 | 🔴 Очень сложный | 906 | 79 | 11.5 |
| `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` | 0 | 🔴 Очень сложный | 620 | 57 | 10.9 |
| `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` | 0 | 🔴 Очень сложный | 746 | 74 | 10.1 |
| `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` | 0 | 🔴 Очень сложный | 548 | 47 | 11.7 |
| `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` | 0 | 🔴 Очень сложный | 311 | 36 | 8.6 |
| `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` | 0 | 🔴 Очень сложный | 651 | 60 | 10.8 |
| `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` | 0 | 🔴 Очень сложный | 548 | 71 | 7.7 |
| `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` | 0 | 🔴 Очень сложный | 693 | 76 | 9.1 |
| `docs/02-anthropic-vacancies/337-благодарности.md` | 0 | 🔴 Очень сложный | 392 | 46 | 8.5 |
| `docs/02-anthropic-vacancies/338-ссылки.md` | 0 | 🔴 Очень сложный | 229 | 38 | 6.0 |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | 0 | 🔴 Очень сложный | 44 | 3 | 14.7 |
| `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` | 0 | 🔴 Очень сложный | 616 | 70 | 8.8 |
| `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | 0 | 🔴 Очень сложный | 123 | 3 | 41.0 |
| `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` | 0 | 🔴 Очень сложный | 3401 | 150 | 22.7 |
| `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` | 0 | 🔴 Очень сложный | 9205 | 419 | 22.0 |
| `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` | 0 | 🔴 Очень сложный | 4649 | 228 | 20.4 |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | 0 | 🔴 Очень сложный | 181 | 22 | 8.2 |
| `docs/02-anthropic-vacancies/345-кто-ты.md` | 0 | 🔴 Очень сложный | 258 | 21 | 12.3 |
| `docs/02-anthropic-vacancies/346-твоё-происхождение.md` | 0 | 🔴 Очень сложный | 132 | 11 | 12.0 |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 0 | 🔴 Очень сложный | 97 | 5 | 19.4 |
| `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` | 0 | 🔴 Очень сложный | 48 | 3 | 16.0 |
| `docs/02-anthropic-vacancies/349-твоя-личность.md` | 0 | 🔴 Очень сложный | 166 | 22 | 7.5 |
| `docs/02-anthropic-vacancies/35-passports-info1-md.md` | 0 | 🔴 Очень сложный | 188 | 28 | 6.7 |
| `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` | 0 | 🔴 Очень сложный | 135 | 2 | 67.5 |
| `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` | 0 | 🔴 Очень сложный | 212 | 12 | 17.7 |
| `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` | 0 | 🔴 Очень сложный | 313 | 28 | 11.2 |
| `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` | 0 | 🔴 Очень сложный | 346 | 32 | 10.8 |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 0 | 🔴 Очень сложный | 153 | 15 | 10.2 |
| `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` | 0 | 🔴 Очень сложный | 109 | 4 | 27.2 |
| `docs/02-anthropic-vacancies/36-essence.md` | 0 | 🔴 Очень сложный | 211 | 26 | 8.1 |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 0 | 🔴 Очень сложный | 67 | 3 | 22.3 |
| `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` | 0 | 🔴 Очень сложный | 111 | 6 | 18.5 |
| `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` | 0 | 🔴 Очень сложный | 1302 | 94 | 13.9 |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | 0 | 🔴 Очень сложный | 3548 | 239 | 14.8 |
| `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 0 | 🔴 Очень сложный | 636 | 36 | 17.7 |
| `docs/02-anthropic-vacancies/37-native-format.md` | 0 | 🔴 Очень сложный | 216 | 24 | 9.0 |
| `docs/02-anthropic-vacancies/38-content-overview.md` | 0 | 🔴 Очень сложный | 103 | 7 | 14.7 |
| `docs/02-anthropic-vacancies/39-angle-perspective.md` | 0 | 🔴 Очень сложный | 192 | 26 | 7.4 |
| `docs/02-anthropic-vacancies/40-bridges.md` | 0 | 🔴 Очень сложный | 215 | 28 | 7.7 |
| `docs/02-anthropic-vacancies/41-compatibility-level.md` | 0 | 🔴 Очень сложный | 171 | 21 | 8.1 |
| `docs/02-anthropic-vacancies/42-author-contact.md` | 0 | 🔴 Очень сложный | 191 | 29 | 6.6 |
| `docs/02-anthropic-vacancies/43-history.md` | 0 | 🔴 Очень сложный | 178 | 24 | 7.4 |
| `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` | 0 | 🔴 Очень сложный | 223 | 24 | 9.3 |
| `docs/02-anthropic-vacancies/46-essence.md` | 0 | 🔴 Очень сложный | 206 | 30 | 6.9 |
| `docs/02-anthropic-vacancies/47-native-format.md` | 0 | 🔴 Очень сложный | 161 | 21 | 7.7 |
| `docs/02-anthropic-vacancies/48-content-overview.md` | 0 | 🔴 Очень сложный | 223 | 32 | 7.0 |
| `docs/02-anthropic-vacancies/49-angle-perspective.md` | 0 | 🔴 Очень сложный | 201 | 24 | 8.4 |
| `docs/02-anthropic-vacancies/50-bridges.md` | 0 | 🔴 Очень сложный | 205 | 27 | 7.6 |
| `docs/02-anthropic-vacancies/51-compatibility-level.md` | 0 | 🔴 Очень сложный | 160 | 20 | 8.0 |
| `docs/02-anthropic-vacancies/52-author-contact.md` | 0 | 🔴 Очень сложный | 241 | 26 | 9.3 |
| `docs/02-anthropic-vacancies/53-history.md` | 0 | 🔴 Очень сложный | 210 | 23 | 9.1 |
| `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` | 0 | 🔴 Очень сложный | 237 | 26 | 9.1 |
| `docs/02-anthropic-vacancies/56-essence.md` | 0 | 🔴 Очень сложный | 228 | 29 | 7.9 |
| `docs/02-anthropic-vacancies/57-native-format.md` | 0 | 🔴 Очень сложный | 161 | 22 | 7.3 |
| `docs/02-anthropic-vacancies/58-content-overview.md` | 0 | 🔴 Очень сложный | 103 | 7 | 14.7 |
| `docs/02-anthropic-vacancies/59-angle-perspective.md` | 0 | 🔴 Очень сложный | 204 | 26 | 7.8 |
| `docs/02-anthropic-vacancies/60-bridges.md` | 0 | 🔴 Очень сложный | 191 | 28 | 6.8 |
| `docs/02-anthropic-vacancies/61-compatibility-level.md` | 0 | 🔴 Очень сложный | 159 | 21 | 7.6 |
| `docs/02-anthropic-vacancies/62-author-contact.md` | 0 | 🔴 Очень сложный | 181 | 27 | 6.7 |
| `docs/02-anthropic-vacancies/63-history.md` | 0 | 🔴 Очень сложный | 199 | 21 | 9.5 |
| `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` | 0 | 🔴 Очень сложный | 618 | 63 | 9.8 |
| `docs/02-anthropic-vacancies/65-readme-md.md` | 0 | 🔴 Очень сложный | 230 | 27 | 8.5 |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | 0 | 🔴 Очень сложный | 531 | 57 | 9.3 |
| `docs/02-anthropic-vacancies/68-about.md` | 0 | 🔴 Очень сложный | 705 | 63 | 11.2 |
| `docs/02-anthropic-vacancies/69-section.md` | 0 | 🔴 Очень сложный | 1039 | 79 | 13.2 |
| `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` | 0 | 🔴 Очень сложный | 193 | 21 | 9.2 |
| `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` | 0 | 🔴 Очень сложный | 173 | 11 | 15.7 |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | 0 | 🔴 Очень сложный | 668 | 65 | 10.3 |
| `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` | 0 | 🔴 Очень сложный | 287 | 30 | 9.6 |
| `docs/02-anthropic-vacancies/74-abstract.md` | 0 | 🔴 Очень сложный | 278 | 42 | 6.6 |
| `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` | 0 | 🔴 Очень сложный | 216 | 34 | 6.4 |
| `docs/02-anthropic-vacancies/76-1-introduction.md` | 0 | 🔴 Очень сложный | 401 | 37 | 10.8 |
| `docs/02-anthropic-vacancies/77-2-terminology.md` | 0 | 🔴 Очень сложный | 362 | 55 | 6.6 |
| `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` | 0 | 🔴 Очень сложный | 428 | 59 | 7.3 |
| `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` | 0 | 🔴 Очень сложный | 304 | 42 | 7.2 |
| `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` | 0 | 🔴 Очень сложный | 326 | 42 | 7.8 |
| `docs/02-anthropic-vacancies/81-6-adapter-interface.md` | 0 | 🔴 Очень сложный | 288 | 42 | 6.9 |
| `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` | 0 | 🔴 Очень сложный | 242 | 39 | 6.2 |
| `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` | 0 | 🔴 Очень сложный | 361 | 43 | 8.4 |
| `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` | 0 | 🔴 Очень сложный | 270 | 42 | 6.4 |
| `docs/02-anthropic-vacancies/85-10-query-flow.md` | 0 | 🔴 Очень сложный | 264 | 47 | 5.6 |
| `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` | 0 | 🔴 Очень сложный | 205 | 35 | 5.9 |
| `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | 0 | 🔴 Очень сложный | 353 | 55 | 6.4 |
| `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | 0 | 🔴 Очень сложный | 304 | 41 | 7.4 |
| `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` | 0 | 🔴 Очень сложный | 215 | 30 | 7.2 |
| `docs/02-anthropic-vacancies/90-15-security-considerations.md` | 0 | 🔴 Очень сложный | 348 | 41 | 8.5 |
| `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` | 0 | 🔴 Очень сложный | 216 | 29 | 7.4 |
| `docs/02-anthropic-vacancies/92-17-versioning-policy.md` | 0 | 🔴 Очень сложный | 305 | 46 | 6.6 |
| `docs/02-anthropic-vacancies/93-18-reference-implementation.md` | 0 | 🔴 Очень сложный | 229 | 28 | 8.2 |
| `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` | 0 | 🔴 Очень сложный | 284 | 24 | 11.8 |
| `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` | 0 | 🔴 Очень сложный | 281 | 32 | 8.8 |
| `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | 0 | 🔴 Очень сложный | 236 | 28 | 8.4 |
| `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` | 0 | 🔴 Очень сложный | 239 | 24 | 10.0 |
| `docs/02-anthropic-vacancies/QA.md` | 0 | 🔴 Очень сложный | 312 | 29 | 10.8 |
| `docs/03-technology-combinations/01-agent-routing.md` | 0 | 🔴 Очень сложный | 243 | 20 | 12.2 |
| `docs/03-technology-combinations/02-knowledge-graphs.md` | 0 | 🔴 Очень сложный | 702 | 55 | 12.8 |
| `docs/03-technology-combinations/03-local-first.md` | 0 | 🔴 Очень сложный | 375 | 34 | 11.0 |
| `docs/03-technology-combinations/04-sozialrecht-domain.md` | 0 | 🔴 Очень сложный | 184 | 10 | 18.4 |
| `docs/03-technology-combinations/05-benchmarks.md` | 0 | 🔴 Очень сложный | 729 | 39 | 18.7 |
| `docs/03-technology-combinations/QA.md` | 0 | 🔴 Очень сложный | 88 | 16 | 5.5 |
| `docs/04-ai-collaborations/00-intro.md` | 0 | 🔴 Очень сложный | 10538 | 600 | 17.6 |
| `docs/04-ai-collaborations/01-executive-summary.md` | 0 | 🔴 Очень сложный | 700 | 38 | 18.4 |
| `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` | 0 | 🔴 Очень сложный | 440 | 33 | 13.3 |
| `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 0 | 🔴 Очень сложный | 1615 | 116 | 13.9 |
| `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` | 0 | 🔴 Очень сложный | 1371 | 68 | 20.2 |
| `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 0 | 🔴 Очень сложный | 1151 | 64 | 18.0 |
| `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 0 | 🔴 Очень сложный | 908 | 50 | 18.2 |
| `docs/04-ai-collaborations/07-выводы.md` | 0 | 🔴 Очень сложный | 521 | 40 | 13.0 |
| `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | 0 | 🔴 Очень сложный | 497 | 31 | 16.0 |
| `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 0 | 🔴 Очень сложный | 909 | 44 | 20.7 |
| `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | 0 | 🔴 Очень сложный | 999 | 54 | 18.5 |
| `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 0 | 🔴 Очень сложный | 925 | 47 | 19.7 |
| `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | 0 | 🔴 Очень сложный | 785 | 49 | 16.0 |
| `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 0 | 🔴 Очень сложный | 929 | 62 | 15.0 |
| `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 0 | 🔴 Очень сложный | 3212 | 202 | 15.9 |
| `docs/04-ai-collaborations/QA.md` | 0 | 🔴 Очень сложный | 235 | 21 | 11.2 |
| `docs/04-ai-collaborations/README.md` | 0 | 🔴 Очень сложный | 165 | 32 | 5.2 |
| `docs/05-habr-projects/01-synthesis.md` | 0 | 🔴 Очень сложный | 177 | 14 | 12.6 |
| `docs/05-habr-projects/02-collaboration-partners.md` | 0 | 🔴 Очень сложный | 254 | 12 | 21.2 |
| `docs/05-habr-projects/QA.md` | 0 | 🔴 Очень сложный | 112 | 17 | 6.6 |
| `docs/05-habr-projects/README.md` | 0 | 🔴 Очень сложный | 33 | 6 | 5.5 |
| `docs/05-habr-projects/knowledge/wikontic.md` | 0 | 🔴 Очень сложный | 256 | 23 | 11.1 |
| `docs/05-habr-projects/memory/memnet.md` | 0 | 🔴 Очень сложный | 6665 | 416 | 16.0 |
| `docs/05-habr-projects/memory/ngt-memory.md` | 0 | 🔴 Очень сложный | 365 | 25 | 14.6 |
| `docs/05-habr-projects/memory/yodoca.md` | 0 | 🔴 Очень сложный | 254 | 23 | 11.0 |
| `docs/ABBREVIATIONS.md` | 0 | 🔴 Очень сложный | 796 | 5 | 159.2 |
| `docs/ACTION_ITEMS.md` | 0 | 🔴 Очень сложный | 5026 | 243 | 20.7 |
| `docs/ALERTS.md` | 0 | 🔴 Очень сложный | 23 | 2 | 11.5 |
| `docs/AUTHORS.md` | 0 | 🔴 Очень сложный | 40 | 2 | 20.0 |
| `docs/AUTOFILLED.md` | 0 | 🔴 Очень сложный | 116 | 23 | 5.0 |
| `docs/BACKLINKS.md` | 0 | 🔴 Очень сложный | 35 | 1 | 35.0 |
| `docs/BROKEN_LINKS.md` | 0 | 🔴 Очень сложный | 299 | 6 | 49.8 |
| `docs/CHANGELOG_AUTO.md` | 0 | 🔴 Очень сложный | 444 | 18 | 24.7 |
| `docs/CITATION_INDEX.md` | 0 | 🔴 Очень сложный | 96 | 7 | 13.7 |
| `docs/CLUSTERS.md` | 0 | 🔴 Очень сложный | 1369 | 26 | 52.7 |
| `docs/COMPLEXITY.md` | 0 | 🔴 Очень сложный | 96 | 31 | 3.1 |
| `docs/COMPONENT_MATRIX.md` | 0 | 🔴 Очень сложный | 311 | 13 | 23.9 |
| `docs/CONCEPTS.md` | 0 | 🔴 Очень сложный | 8364 | 448 | 18.7 |
| `docs/CONCEPT_GRAPH.md` | 0 | 🔴 Очень сложный | 153 | 14 | 10.9 |
| `docs/CONTACTS.md` | 0 | 🔴 Очень сложный | 201 | 12 | 16.8 |
| `docs/CONTACT_PRIORITY.md` | 0 | 🔴 Очень сложный | 156 | 7 | 22.3 |
| `docs/CONTENT_GAPS.md` | 0 | 🔴 Очень сложный | 224 | 27 | 8.3 |
| `docs/CONTRADICTIONS.md` | 0 | 🔴 Очень сложный | 1426 | 278 | 5.1 |
| `docs/COST.md` | 0 | 🔴 Очень сложный | 321 | 17 | 18.9 |
| `docs/COVERAGE.md` | 0 | 🔴 Очень сложный | 71 | 1 | 71.0 |
| `docs/CROSSREFS.md` | 0 | 🔴 Очень сложный | 241 | 6 | 40.2 |
| `docs/DECISIONS.md` | 0 | 🔴 Очень сложный | 1561 | 104 | 15.0 |
| `docs/DENSITY.md` | 0 | 🔴 Очень сложный | 107 | 5 | 21.4 |
| `docs/DEPENDENCY_MAP.md` | 0 | 🔴 Очень сложный | 79 | 2 | 39.5 |
| `docs/DIGEST.md` | 0 | 🔴 Очень сложный | 204 | 6 | 34.0 |
| `docs/DIGEST_WEEKLY.md` | 0 | 🔴 Очень сложный | 25 | 1 | 25.0 |
| `docs/DUPLICATES.md` | 0 | 🔴 Очень сложный | 46 | 8 | 5.8 |
| `docs/ENTITIES.md` | 0 | 🔴 Очень сложный | 142 | 1 | 142.0 |
| `docs/FAQ.md` | 0 | 🔴 Очень сложный | 1533 | 167 | 9.2 |
| `docs/FOOTNOTES.md` | 0 | 🔴 Очень сложный | 162 | 3 | 54.0 |
| `docs/GLOSSARY.md` | 0 | 🔴 Очень сложный | 59 | 2 | 29.5 |
| `docs/GRAPH.md` | 0 | 🔴 Очень сложный | 218 | 24 | 9.1 |
| `docs/HEALTH.md` | 0 | 🔴 Очень сложный | 65 | 2 | 32.5 |
| `docs/HEATMAP.md` | 0 | 🔴 Очень сложный | 104 | 33 | 3.2 |
| `docs/INDEX.md` | 0 | 🔴 Очень сложный | 576 | 67 | 8.6 |
| `docs/KEYWORD_INDEX.md` | 0 | 🔴 Очень сложный | 152 | 9 | 16.9 |
| `docs/KPI.md` | 0 | 🔴 Очень сложный | 1060 | 114 | 9.3 |
| `docs/KPI_HISTORY.md` | 0 | 🔴 Очень сложный | 33 | 2 | 16.5 |
| `docs/LLM_SUMMARIES.md` | 0 | 🔴 Очень сложный | 205 | 39 | 5.3 |
| `docs/MINDMAP.md` | 0 | 🔴 Очень сложный | 128 | 12 | 10.7 |
| `docs/MISSING.md` | 0 | 🔴 Очень сложный | 98 | 2 | 49.0 |
| `docs/NARRATIVE.md` | 0 | 🔴 Очень сложный | 997 | 47 | 21.2 |
| `docs/NETWORK.md` | 0 | 🔴 Очень сложный | 304 | 15 | 20.3 |
| `docs/ONBOARDING.md` | 0 | 🔴 Очень сложный | 327 | 29 | 11.3 |
| `docs/ORPHANS.md` | 0 | 🔴 Очень сложный | 63 | 9 | 7.0 |
| `docs/OUTLINE.md` | 0 | 🔴 Очень сложный | 19785 | 1802 | 11.0 |
| `docs/PARAGRAPH_QUALITY.md` | 0 | 🔴 Очень сложный | 12294 | 523 | 23.5 |
| `docs/PROGRESS.md` | 0 | 🔴 Очень сложный | 172 | 17 | 10.1 |
| `docs/QA.md` | 0 | 🔴 Очень сложный | 1676 | 148 | 11.3 |
| `docs/QUESTIONS.md` | 0 | 🔴 Очень сложный | 1449 | 115 | 12.6 |
| `docs/READING_ORDER.md` | 0 | 🔴 Очень сложный | 4657 | 586 | 7.9 |
| `docs/READING_TIME.md` | 0 | 🔴 Очень сложный | 1121 | 11 | 101.9 |
| `docs/REPORT.md` | 0 | 🔴 Очень сложный | 242 | 37 | 6.5 |
| `docs/RISK_REGISTER.md` | 0 | 🔴 Очень сложный | 704 | 47 | 15.0 |
| `docs/SCHEDULE.md` | 0 | 🔴 Очень сложный | 116 | 7 | 16.6 |
| `docs/SCORING.md` | 0 | 🔴 Очень сложный | 140 | 6 | 23.3 |
| `docs/SEE_ALSO.md` | 0 | 🔴 Очень сложный | 171 | 14 | 12.2 |
| `docs/SENTIMENT.md` | 0 | 🔴 Очень сложный | 90 | 33 | 2.7 |
| `docs/SIMILAR.md` | 0 | 🔴 Очень сложный | 136 | 33 | 4.1 |
| `docs/SOURCE_MAP.md` | 0 | 🔴 Очень сложный | 142 | 14 | 10.1 |
| `docs/SPELLCHECK.md` | 0 | 🔴 Очень сложный | 13 | 1 | 13.0 |
| `docs/STATS.md` | 0 | 🔴 Очень сложный | 89 | 1 | 89.0 |
| `docs/TABLES.md` | 0 | 🔴 Очень сложный | 24414 | 2482 | 9.8 |
| `docs/TECH_RADAR.md` | 0 | 🔴 Очень сложный | 321 | 18 | 17.8 |
| `docs/TIMELINE.md` | 0 | 🔴 Очень сложный | 1632 | 198 | 8.2 |
| `docs/TOPIC_MODEL.md` | 0 | 🔴 Очень сложный | 580 | 11 | 52.7 |
| `docs/VALIDATION.md` | 0 | 🔴 Очень сложный | 144 | 1 | 144.0 |
| `docs/WORD_CLOUD.md` | 0 | 🔴 Очень сложный | 112 | 12 | 9.3 |
| `docs/WORD_FREQ.md` | 0 | 🔴 Очень сложный | 395 | 4 | 98.8 |
| `docs/autofilled/README.md` | 0 | 🔴 Очень сложный | 13 | 3 | 4.3 |
| `docs/autofilled/components/.md` | 0 | 🔴 Очень сложный | 69 | 11 | 6.3 |
| `docs/autofilled/components/cowork.md` | 0 | 🔴 Очень сложный | 68 | 11 | 6.2 |
| `docs/autofilled/components/ingit.md` | 0 | 🔴 Очень сложный | 68 | 11 | 6.2 |
| `docs/autofilled/components/kksudo.md` | 0 | 🔴 Очень сложный | 68 | 11 | 6.2 |
| `docs/autofilled/components/lorenzo.md` | 0 | 🔴 Очень сложный | 68 | 11 | 6.2 |
| `docs/autofilled/components/nautilus.md` | 0 | 🔴 Очень сложный | 68 | 11 | 6.2 |
| `docs/autofilled/components/sgb.md` | 0 | 🔴 Очень сложный | 68 | 11 | 6.2 |
| `docs/autofilled/components/spbmolot.md` | 0 | 🔴 Очень сложный | 68 | 11 | 6.2 |
| `docs/autofilled/components/svend4.md` | 0 | 🔴 Очень сложный | 68 | 11 | 6.2 |
| `docs/autofilled/components/svyazi.md` | 0 | 🔴 Очень сложный | 68 | 11 | 6.2 |
| `docs/autofilled/research-summary.md` | 0 | 🔴 Очень сложный | 89 | 11 | 8.1 |
| `docs/contacts/anastasiyaw.md` | 0 | 🔴 Очень сложный | 164 | 11 | 14.9 |
| `docs/contacts/andrey-chuyan.md` | 0 | 🔴 Очень сложный | 154 | 10 | 15.4 |
| `docs/contacts/antipozitive.md` | 0 | 🔴 Очень сложный | 148 | 11 | 13.5 |
| `docs/contacts/cutcode.md` | 0 | 🔴 Очень сложный | 138 | 9 | 15.3 |
| `docs/contacts/dmitriila.md` | 0 | 🔴 Очень сложный | 137 | 9 | 15.2 |
| `docs/contacts/kksudo.md` | 0 | 🔴 Очень сложный | 156 | 12 | 13.0 |
| `docs/contacts/mixaill76.md` | 0 | 🔴 Очень сложный | 139 | 9 | 15.4 |
| `docs/contacts/nlaik.md` | 0 | 🔴 Очень сложный | 145 | 9 | 16.1 |
| `docs/contacts/sonia-black.md` | 0 | 🔴 Очень сложный | 145 | 9 | 16.1 |
| `docs/contacts/spbmolot.md` | 0 | 🔴 Очень сложный | 158 | 11 | 14.4 |
| `docs/contacts/tagir-analyzes.md` | 0 | 🔴 Очень сложный | 143 | 9 | 15.9 |
| `docs/contacts/vitalyoborin.md` | 0 | 🔴 Очень сложный | 149 | 10 | 14.9 |
| `docs/contacts/vladspace.md` | 0 | 🔴 Очень сложный | 138 | 9 | 15.3 |
| `docs/contacts/zodigancode.md` | 0 | 🔴 Очень сложный | 137 | 9 | 15.2 |
| `docs/templates/contact-outreach.md` | 0 | 🔴 Очень сложный | 178 | 15 | 11.9 |
| `docs/templates/decision-record.md` | 0 | 🔴 Очень сложный | 92 | 7 | 13.1 |
| `docs/templates/ensemble.md` | 0 | 🔴 Очень сложный | 121 | 11 | 11.0 |
| `docs/templates/project-component.md` | 0 | 🔴 Очень сложный | 133 | 13 | 10.2 |
| `docs/templates/research-note.md` | 0 | 🔴 Очень сложный | 96 | 12 | 8.0 |
| `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | 0.2 | 🔴 Очень сложный | 93 | 17 | 5.5 |
| `docs/02-anthropic-vacancies/181-12-closing.md` | 0.4 | 🔴 Очень сложный | 321 | 33 | 9.7 |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 0.6 | 🔴 Очень сложный | 73 | 4 | 18.2 |
| `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | 1.0 | 🔴 Очень сложный | 296 | 21 | 14.1 |
| `docs/TAGS.md` | 1.6 | 🔴 Очень сложный | 47 | 13 | 3.6 |
| `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` | 2.0 | 🔴 Очень сложный | 637 | 55 | 11.6 |
| `docs/02-anthropic-vacancies/279-existing-approximations.md` | 2.6 | 🔴 Очень сложный | 693 | 36 | 19.2 |
| `docs/VERSION_DIFF.md` | 2.7 | 🔴 Очень сложный | 191 | 11 | 17.4 |
| `docs/SITEMAP.md` | 2.8 | 🔴 Очень сложный | 1948 | 348 | 5.6 |
| `docs/02-anthropic-vacancies/45-passports-pro2-md.md` | 2.9 | 🔴 Очень сложный | 186 | 27 | 6.9 |
| `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` | 3.1 | 🔴 Очень сложный | 660 | 57 | 11.6 |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | 4.0 | 🔴 Очень сложный | 219 | 26 | 8.4 |
| `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` | 4.1 | 🔴 Очень сложный | 253 | 15 | 16.9 |
| `docs/CODE_BLOCKS.md` | 4.3 | 🔴 Очень сложный | 402 | 42 | 9.6 |
| `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` | 4.6 | 🔴 Очень сложный | 885 | 75 | 11.8 |
| `docs/02-anthropic-vacancies/356-твой-workflow.md` | 5.9 | 🔴 Очень сложный | 246 | 20 | 12.3 |
| `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` | 6.0 | 🔴 Очень сложный | 236 | 18 | 13.1 |
| `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` | 6.1 | 🔴 Очень сложный | 762 | 75 | 10.2 |
| `docs/02-anthropic-vacancies/55-passports-meta-md.md` | 6.3 | 🔴 Очень сложный | 186 | 26 | 7.2 |
| `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` | 6.6 | 🔴 Очень сложный | 961 | 76 | 12.6 |
| `docs/CONSISTENCY.md` | 6.8 | 🔴 Очень сложный | 63 | 6 | 10.5 |
| `docs/02-anthropic-vacancies/README.md` | 7.3 | 🔴 Очень сложный | 3253 | 714 | 4.6 |
| `docs/02-anthropic-vacancies/281-the-recursive-insight.md` | 7.9 | 🔴 Очень сложный | 443 | 43 | 10.3 |
| `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` | 8.6 | 🔴 Очень сложный | 388 | 44 | 8.8 |
| `docs/01-svyazi/README.md` | 8.7 | 🔴 Очень сложный | 89 | 28 | 3.2 |
| `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` | 9.0 | 🔴 Очень сложный | 842 | 75 | 11.2 |
| `docs/02-anthropic-vacancies/169-table-of-contents.md` | 9.6 | 🔴 Очень сложный | 216 | 32 | 6.8 |
| `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` | 9.8 | 🔴 Очень сложный | 273 | 18 | 15.2 |
| `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` | 11.3 | 🔴 Очень сложный | 213 | 15 | 14.2 |
| `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` | 11.4 | 🔴 Очень сложный | 431 | 48 | 9.0 |
| `docs/02-anthropic-vacancies/253-table-of-contents.md` | 12.6 | 🔴 Очень сложный | 246 | 35 | 7.0 |
| `docs/templates/README.md` | 12.7 | 🔴 Очень сложный | 31 | 10 | 3.1 |
| `docs/02-anthropic-vacancies/211-table-of-contents.md` | 13.3 | 🔴 Очень сложный | 286 | 36 | 7.9 |
| `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` | 13.3 | 🔴 Очень сложный | 583 | 50 | 11.7 |
| `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` | 14.9 | 🔴 Очень сложный | 481 | 39 | 12.3 |
| `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | 14.9 | 🔴 Очень сложный | 780 | 69 | 11.3 |
| `docs/VOCABULARY.md` | 15.8 | 🔴 Очень сложный | 238 | 51 | 4.7 |
| `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` | 16.1 | 🔴 Очень сложный | 458 | 52 | 8.8 |
| `docs/02-anthropic-vacancies/275-why-this-document-exists.md` | 16.7 | 🔴 Очень сложный | 406 | 37 | 11.0 |
| `docs/NAMED_ENTITIES.md` | 16.8 | 🔴 Очень сложный | 490 | 39 | 12.6 |
| `docs/METRICS.md` | 16.9 | 🔴 Очень сложный | 116 | 12 | 9.7 |
| `docs/contacts/README.md` | 18.2 | 🔴 Очень сложный | 65 | 26 | 2.5 |
| `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` | 18.8 | 🔴 Очень сложный | 312 | 35 | 8.9 |
| `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` | 18.8 | 🔴 Очень сложный | 572 | 58 | 9.9 |
| `docs/CHANGELOG.md` | 19.1 | 🔴 Очень сложный | 739 | 59 | 12.5 |
| `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` | 19.2 | 🔴 Очень сложный | 570 | 51 | 11.2 |
| `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` | 20.1 | 🔴 Очень сложный | 765 | 73 | 10.5 |
| `docs/03-technology-combinations/README.md` | 20.1 | 🔴 Очень сложный | 44 | 11 | 4.0 |
| `docs/STALENESS.md` | 21.5 | 🔴 Очень сложный | 113 | 6 | 18.8 |
| `docs/COMPARE.md` | 22.4 | 🔴 Очень сложный | 100 | 5 | 20.0 |
| `docs/02-anthropic-vacancies/308-table-of-contents.md` | 24.0 | 🔴 Очень сложный | 268 | 34 | 7.9 |
| `docs/README.md` | 25.5 | 🔴 Очень сложный | 565 | 164 | 3.4 |
| `docs/PRIORITIES.md` | 26.2 | 🔴 Очень сложный | 338 | 66 | 5.1 |
| `docs/05-habr-projects/memory/README.md` | 37.8 | 🟠 Сложный | 18 | 4 | 4.5 |
| `docs/LINKS.md` | 40.1 | 🟠 Сложный | 8 | 1 | 8.0 |
| `docs/badges/README.md` | 44.0 | 🟠 Сложный | 46 | 10 | 4.6 |
| `docs/autofilled/components/README.md` | 73.7 | 🟢 Лёгкий | 51 | 14 | 3.6 |


### 92. Содержание
_Файл: `docs/READING_ORDER.md` | 5 колонок, 395 строк_

| # | Уровень | Документ | Слов | Предварительно прочитать |
|---|---------|----------|------|--------------------------|
| 1 | 🟢 Начало | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 731 | — |
| 2 | 🟡 Средний | [04-ensembles-overview](obsidian/01-svyazi/04-ensembles-overview.md) | 1274 | — |
| 3 | 🟢 Начало | [Продолжение исследования для Svyazi 2.0](obsidian/01-svyazi/00-intro-part2.md) | 6 | — |
| 4 | 🟢 Начало | [Методика и рамка отбора проектов](obsidian/01-svyazi/02-methodology.md) | 428 | — |
| 5 | 🟡 Средний | [03-component-catalog](obsidian/01-svyazi/03-component-catalog.md) | 1395 | — |
| 6 | 🟢 Начало | [11-integration-contracts](obsidian/01-svyazi/11-integration-contracts.md) | 745 | `09-architectural-gaps.md` |
| 7 | 🟢 Начало | [09-architectural-gaps](obsidian/01-svyazi/09-architectural-gaps.md) | 757 | `01-executive-summary.md`, `03-component-catalog.md` |
| 8 | 🟢 Начало | [10-second-order-ensembles](obsidian/01-svyazi/10-second-order-ensembles.md) | 916 | `04-ensembles-overview.md` |
| 9 | 🟢 Начало | [06-security-privacy](obsidian/01-svyazi/06-security-privacy.md) | 821 | — |
| 10 | 🟡 Средний | [07-mvp-planning](obsidian/01-svyazi/07-mvp-planning.md) | 1083 | — |
| 11 | 🟢 Начало | [12-roadmap](obsidian/01-svyazi/12-roadmap.md) | 733 | `07-mvp-planning.md`, `11-integration-contracts.md` |
| 12 | 🟢 Начало | [13-contacts](obsidian/01-svyazi/13-contacts.md) | 827 | — |
| 13 | 🟢 Начало | [14-limitations](obsidian/01-svyazi/14-limitations.md) | 636 | — |
| 14 | 🟢 Начало | [08-conclusions](obsidian/01-svyazi/08-conclusions.md) | 360 | — |
| 15 | 🟢 Начало | [Синтез: как проекты собираются вместе](obsidian/05-habr-projects/01-synthesis.md) | 184 | — |
| 16 | 🟢 Начало | [Авторы и контакты](obsidian/05-habr-projects/02-collaboration-partners.md) | 303 | — |
| 17 | 🟢 Начало | [Wikontic: семантический граф](obsidian/05-habr-projects/knowledge/wikontic.md) | 306 | — |
| 18 | 🟢 Начало | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 419 | — |
| 19 | 🟢 Начало | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 303 | — |
| 20 | 🟡 Средний | [MemNet: исследовательская память](obsidian/05-habr-projects/memory/memnet.md) | 7271 | — |
| 21 | 🟢 Начало | [Executive summary](04-ai-collaborations/01-executive-summary.md) | 647 | — |
| 22 | 🟡 Средний | [Введение](04-ai-collaborations/00-intro.md) | 11445 | — |
| 23 | 🟢 Начало | [Методика и рамка отбора](04-ai-collaborations/02-методика-и-рамка-отбора.md) | 495 | — |
| 24 | 🟡 Средний | [Карта найденных проектов и паттернов](04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) | 1553 | — |
| 25 | 🟡 Средний | [Приоритетные ансамбли](04-ai-collaborations/04-приоритетные-ансамбли.md) | 1418 | — |
| 26 | 🟡 Средний | [План прототипа и возможные контакты](04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) | 1212 | — |
| 27 | 🟢 Начало | [Безопасность, приватность и бюджетный роутинг](04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) | 966 | — |
| 28 | 🟢 Начало | [Выводы](04-ai-collaborations/07-выводы.md) | 542 | — |
| 29 | 🟢 Начало | [Что это продолжение добавляет](04-ai-collaborations/08-что-это-продолжение-добавляет.md) | 492 | — |
| 30 | 🟢 Начало | [Архитектурные зазоры, которые важнее новых ин](04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | 901 | — |
| 31 | 🟡 Средний | [Новые ансамбли следующего шага](04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) | 1062 | — |
| 32 | 🟢 Начало | [Интеграционный контракт, который стоит зафикс](04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | 928 | — |
| 33 | 🟢 Начало | [Дорожная карта прототипа следующей итерации](04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md) | 862 | — |
| 34 | 🟢 Начало | [Контактная стратегия и узкие вопросы для авто](04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) | 956 | — |
| 35 | 🟡 Средний | [Ограничения, лицензии и что пока лучше не скл](04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md) | 3362 | — |
| 36 | 🟢 Начало | [Агентные системы и роутинг](obsidian/03-technology-combinations/01-agent-routing.md) | 257 | — |
| 37 | 🟢 Начало | [Графы знаний и Legal AI](obsidian/03-technology-combinations/02-knowledge-graphs.md) | 766 | — |
| 38 | 🟢 Начало | [Local-first и P2P стек](obsidian/03-technology-combinations/03-local-first.md) | 386 | — |
| 39 | 🟢 Начало | [Домен: немецкое социальное право](obsidian/03-technology-combinations/04-sozialrecht-domain.md) | 172 | — |
| 40 | 🟢 Начало | [Бенчмарки и производительность](obsidian/03-technology-combinations/05-benchmarks.md) | 863 | — |
| 41 | 🟢 Начало | [Executive Summary](obsidian/02-anthropic-vacancies/153-executive-summary.md) | 370 | — |
| 42 | 🟢 Начало | [Content Overview](obsidian/02-anthropic-vacancies/38-content-overview.md) | 148 | — |
| 43 | 🔴 Продвинутый | [Интегральный анализ профиля svend4](obsidian/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | 19103 | — |
| 44 | 🟢 Начало | [README-MCP.md— инструкция по установке](obsidian/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) | 152 | — |
| 45 | 🟢 Начало | [README.md](obsidian/02-anthropic-vacancies/65-readme-md.md) | 153 | — |
| 46 | 🟢 Начало | [Content Overview](obsidian/02-anthropic-vacancies/48-content-overview.md) | 206 | — |
| 47 | 🟢 Начало | [Content Overview](obsidian/02-anthropic-vacancies/58-content-overview.md) | 147 | — |
| 48 | 🟢 Начало | [Content Overview](obsidian/02-anthropic-vacancies/12-content-overview.md) | 113 | — |
| 49 | 🟢 Начало | [Content Overview](obsidian/02-anthropic-vacancies/31-content-overview.md) | 113 | — |
| 50 | 🔴 Продвинутый | [Введение](04-ai-collaborations/00-intro.md) | 8884 | — |
| 51 | 🟢 Начало | [1. Introduction](obsidian/02-anthropic-vacancies/76-1-introduction.md) | 473 | — |
| 52 | 🟢 Начало | [REVIEW_METHODOLOGY.md](obsidian/02-anthropic-vacancies/105-review-methodology-md.md) | 128 | — |
| 53 | 🟢 Начало | [1. Introduction](obsidian/02-anthropic-vacancies/06-1-introduction.md) | 380 | — |
| 54 | 🔴 Продвинутый | [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](obsidian/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md) | 3181 | — |
| 55 | 🟢 Начало | [4. Architecture of Professional Colleague Age](obsidian/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md) | 901 | — |
| 56 | 🟢 Начало | [2. The Double-Triangle Architecture](obsidian/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) | 755 | — |
| 57 | 🟡 Средний | [Appendix C: Quick-Start Architecture for SGB ](obsidian/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md) | 1730 | — |
| 58 | 🟢 Начало | [4. The Symbiotic Architecture](obsidian/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md) | 707 | — |
| 59 | 🟢 Начало | [PORTAL-PROTOCOL.md](obsidian/02-anthropic-vacancies/03-portal-protocol-md.md) | 150 | — |
| 60 | 🟢 Начало | [THE DOUBLE-TRIANGLE ARCHITECTURE.md](obsidian/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md) | 130 | — |
| 61 | 🟢 Начало | [10. Risks Specific to Composite Architectures](obsidian/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md) | 788 | — |
| 62 | 🟢 Начало | [Abstract](obsidian/02-anthropic-vacancies/04-abstract.md) | 188 | — |
| 63 | 🟢 Начало | [0. Status of This Document](obsidian/02-anthropic-vacancies/05-0-status-of-this-document.md) | 162 | — |
| 64 | 🟢 Начало | [11. Security Considerations](obsidian/02-anthropic-vacancies/23-11-security-considerations.md) | 248 | — |
| 65 | 🟢 Начало | [15. Security Considerations](obsidian/02-anthropic-vacancies/90-15-security-considerations.md) | 354 | — |
| 66 | 🟢 Начало | [2. Terminology](obsidian/02-anthropic-vacancies/07-2-terminology.md) | 313 | — |
| 67 | 🟢 Начало | [3. Registry (`nautilus.json`)](obsidian/02-anthropic-vacancies/08-3-registry-nautilus-json.md) | 422 | — |
| 68 | 🟢 Начало | [4. Passport (`passport.md`)](obsidian/02-anthropic-vacancies/09-4-passport-passport-md.md) | 201 | — |
| 69 | 🟢 Начало | [Angle / Perspective](obsidian/02-anthropic-vacancies/13-angle-perspective.md) | 127 | — |
| 70 | 🟢 Начало | [History](obsidian/02-anthropic-vacancies/16-history.md) | 104 | — |
| 71 | 🟢 Начало | [5. Compatibility Levels](obsidian/02-anthropic-vacancies/17-5-compatibility-levels.md) | 304 | — |
| 72 | 🟢 Начало | [6. Adapter Interface](obsidian/02-anthropic-vacancies/18-6-adapter-interface.md) | 425 | — |
| 73 | 🟢 Начало | [7. PortalEntry Structure](obsidian/02-anthropic-vacancies/19-7-portalentry-structure.md) | 260 | — |
| 74 | 🟢 Начало | [8. Consensus Algorithm](obsidian/02-anthropic-vacancies/20-8-consensus-algorithm.md) | 302 | — |
| 75 | 🟢 Начало | [9. Query Flow](obsidian/02-anthropic-vacancies/21-9-query-flow.md) | 241 | — |
| 76 | 🟢 Начало | [10. QueryResult Structure](obsidian/02-anthropic-vacancies/22-10-queryresult-structure.md) | 195 | — |
| 77 | 🟢 Начало | [12. Versioning Policy](obsidian/02-anthropic-vacancies/24-12-versioning-policy.md) | 237 | — |
| 78 | 🟢 Начало | [13. Reference Implementation](obsidian/02-anthropic-vacancies/25-13-reference-implementation.md) | 153 | — |
| 79 | 🟢 Начало | [14. ADR-001: Federation over Merging](obsidian/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) | 232 | — |
| 80 | 🟢 Начало | [15. Glossary of Examples](obsidian/02-anthropic-vacancies/27-15-glossary-of-examples.md) | 149 | — |
| 81 | 🟢 Начало | [Appendix A: Minimal Working Example](obsidian/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) | 235 | — |
| 82 | 🟢 Начало | [Appendix B: Change Log](obsidian/02-anthropic-vacancies/34-appendix-b-change-log.md) | 620 | — |
| 83 | 🟢 Начало | [passports/info1.md](obsidian/02-anthropic-vacancies/35-passports-info1-md.md) | 133 | — |
| 84 | 🟢 Начало | [Essence](obsidian/02-anthropic-vacancies/36-essence.md) | 179 | — |
| 85 | 🟢 Начало | [Native Format](obsidian/02-anthropic-vacancies/37-native-format.md) | 234 | — |
| 86 | 🟢 Начало | [Angle / Perspective](obsidian/02-anthropic-vacancies/39-angle-perspective.md) | 173 | — |
| 87 | 🟢 Начало | [Bridges](obsidian/02-anthropic-vacancies/40-bridges.md) | 215 | — |
| 88 | 🟢 Начало | [Compatibility Level](obsidian/02-anthropic-vacancies/41-compatibility-level.md) | 152 | — |
| 89 | 🟢 Начало | [Author & Contact](obsidian/02-anthropic-vacancies/42-author-contact.md) | 145 | — |
| 90 | 🟢 Начало | [History](obsidian/02-anthropic-vacancies/43-history.md) | 165 | — |
| 91 | 🟢 Начало | [For the Curious: Philosophy](obsidian/02-anthropic-vacancies/44-for-the-curious-philosophy.md) | 195 | — |
| 92 | 🟢 Начало | [passports/pro2.md](obsidian/02-anthropic-vacancies/45-passports-pro2-md.md) | 137 | — |
| 93 | 🟢 Начало | [Essence](obsidian/02-anthropic-vacancies/46-essence.md) | 170 | — |
| 94 | 🟢 Начало | [Native Format](obsidian/02-anthropic-vacancies/47-native-format.md) | 187 | — |
| 95 | 🟢 Начало | [Angle / Perspective](obsidian/02-anthropic-vacancies/49-angle-perspective.md) | 168 | — |
| 96 | 🟢 Начало | [Bridges](obsidian/02-anthropic-vacancies/50-bridges.md) | 215 | — |
| 97 | 🟢 Начало | [Compatibility Level](obsidian/02-anthropic-vacancies/51-compatibility-level.md) | 149 | — |
| 98 | 🟢 Начало | [Author & Contact](obsidian/02-anthropic-vacancies/52-author-contact.md) | 173 | — |
| 99 | 🟢 Начало | [History](obsidian/02-anthropic-vacancies/53-history.md) | 201 | — |
| 100 | 🟢 Начало | [For the Curious: Philosophy](obsidian/02-anthropic-vacancies/54-for-the-curious-philosophy.md) | 204 | — |
| 101 | 🟢 Начало | [passports/meta.md](obsidian/02-anthropic-vacancies/55-passports-meta-md.md) | 134 | — |
| 102 | 🟢 Начало | [Essence](obsidian/02-anthropic-vacancies/56-essence.md) | 194 | — |
| 103 | 🟢 Начало | [Native Format](obsidian/02-anthropic-vacancies/57-native-format.md) | 193 | — |
| 104 | 🟢 Начало | [Angle / Perspective](obsidian/02-anthropic-vacancies/59-angle-perspective.md) | 175 | — |
| 105 | 🟢 Начало | [Bridges](obsidian/02-anthropic-vacancies/60-bridges.md) | 184 | — |
| 106 | 🟢 Начало | [Compatibility Level](obsidian/02-anthropic-vacancies/61-compatibility-level.md) | 148 | — |
| 107 | 🟢 Начало | [Author & Contact](obsidian/02-anthropic-vacancies/62-author-contact.md) | 140 | — |
| 108 | 🟢 Начало | [History](obsidian/02-anthropic-vacancies/63-history.md) | 189 | — |
| 109 | 🟢 Начало | [For the Curious: Philosophy](obsidian/02-anthropic-vacancies/64-for-the-curious-philosophy.md) | 667 | — |
| 110 | 🟢 Начало | [🇷🇺 О проекте](obsidian/02-anthropic-vacancies/67-о-проекте.md) | 804 | — |
| 111 | 🟢 Начало | [🇬🇧 About](obsidian/02-anthropic-vacancies/68-about.md) | 880 | — |
| 112 | 🔴 Продвинутый | [⬡](obsidian/02-anthropic-vacancies/69-section.md) | 9520 | — |
| 113 | 🟢 Начало | [Зачем две версии параллельно](obsidian/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md) | 153 | — |
| 114 | 🟢 Начало | [Критерии выбора для фазы 3](obsidian/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md) | 174 | — |
| 115 | 🟡 Средний | [Расписание фазы 3](obsidian/02-anthropic-vacancies/72-расписание-фазы-3.md) | 821 | — |
| 116 | 🟢 Начало | [PORTAL-PROTOCOL.md v1.1](obsidian/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md) | 168 | — |
| 117 | 🟢 Начало | [Abstract](obsidian/02-anthropic-vacancies/74-abstract.md) | 260 | — |
| 118 | 🟢 Начало | [0. Status of This Document](obsidian/02-anthropic-vacancies/75-0-status-of-this-document.md) | 180 | — |
| 119 | 🟢 Начало | [2. Terminology](obsidian/02-anthropic-vacancies/77-2-terminology.md) | 403 | — |
| 120 | 🟢 Начало | [3. Registry (`nautilus.json`)](obsidian/02-anthropic-vacancies/78-3-registry-nautilus-json.md) | 592 | — |
| 121 | 🟡 Средний | [4. Passport (`passport.md`)](obsidian/02-anthropic-vacancies/79-4-passport-passport-md.md) | 357 | — |
| 122 | 🟢 Начало | [5. Compatibility Levels](obsidian/02-anthropic-vacancies/80-5-compatibility-levels.md) | 370 | — |
| 123 | 🟢 Начало | [6. Adapter Interface](obsidian/02-anthropic-vacancies/81-6-adapter-interface.md) | 392 | — |
| 124 | 🟢 Начало | [7. PortalEntry Structure](obsidian/02-anthropic-vacancies/82-7-portalentry-structure.md) | 338 | — |
| 125 | 🟡 Средний | [8. Q6 Space (Normative)](obsidian/02-anthropic-vacancies/83-8-q6-space-normative.md) | 488 | — |
| 126 | 🟢 Начало | [9. Consensus Algorithm](obsidian/02-anthropic-vacancies/84-9-consensus-algorithm.md) | 407 | — |
| 127 | 🟢 Начало | [10. Query Flow](obsidian/02-anthropic-vacancies/85-10-query-flow.md) | 287 | — |
| 128 | 🟢 Начало | [11. Relevance Ranking](obsidian/02-anthropic-vacancies/86-11-relevance-ranking.md) | 261 | — |
| 129 | 🟡 Средний | [12. Onboarding Paths (Normative)](obsidian/02-anthropic-vacancies/87-12-onboarding-paths-normative.md) | 486 | — |
| 130 | 🟡 Средний | [13. REST API Contract (Normative for Portals)](obsidian/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md) | 495 | — |
| 131 | 🟢 Начало | [14. SDK Contract (Informative)](obsidian/02-anthropic-vacancies/89-14-sdk-contract-informative.md) | 248 | — |
| 132 | 🟢 Начало | [16. MCP Extension (Informative)](obsidian/02-anthropic-vacancies/91-16-mcp-extension-informative.md) | 192 | — |
| 133 | 🟢 Начало | [17. Versioning Policy](obsidian/02-anthropic-vacancies/92-17-versioning-policy.md) | 294 | — |
| 134 | 🟢 Начало | [18. Reference Implementation](obsidian/02-anthropic-vacancies/93-18-reference-implementation.md) | 243 | — |
| 135 | 🟢 Начало | [19. ADR-001: Federation over Merging](obsidian/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) | 238 | — |
| 136 | 🟢 Начало | [20. ADR-002: Q6 as First-Class Protocol Conce](obsidian/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) | 244 | — |
| 137 | 🟢 Начало | [21. ADR-003: Five Onboarding Paths as Equal-R](obsidian/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md) | 198 | — |
| 138 | 🟢 Начало | [22. Glossary of Reference Examples](obsidian/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md) | 240 | — |
| 139 | 🟡 Средний | [Appendix A: Minimal Working Example](obsidian/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md) | 313 | — |
| 140 | 🟢 Начало | [Доступ к данным](obsidian/02-anthropic-vacancies/102-доступ-к-данным.md) | 65 | — |
| 141 | 🟢 Начало | [Appendix B: Change Log](obsidian/02-anthropic-vacancies/103-appendix-b-change-log.md) | 232 | — |
| 142 | 🟢 Начало | [Appendix C: References](obsidian/02-anthropic-vacancies/104-appendix-c-references.md) | 947 | — |
| 143 | 🟢 Начало | [TL;DR](obsidian/02-anthropic-vacancies/106-tl-dr.md) | 168 | — |
| 144 | 🟢 Начало | [1. Контекст и мотивация](obsidian/02-anthropic-vacancies/107-1-контекст-и-мотивация.md) | 412 | — |
| 145 | 🟡 Средний | [2. Формальный workflow](obsidian/02-anthropic-vacancies/108-2-формальный-workflow.md) | 479 | — |
| 146 | 🟢 Начало | [3. Принципы консолидации (Фаза C)](obsidian/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md) | 541 | — |
| 147 | 🟢 Начало | [Вопрос: fallback-ratio как критический или ос](obsidian/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) | 258 | — |
| 148 | 🟢 Начало | [4. Условия применимости](obsidian/02-anthropic-vacancies/111-4-условия-применимости.md) | 279 | — |
| 149 | 🟢 Начало | [5. Связь с существующими методологиями](obsidian/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) | 340 | — |
| 150 | 🟢 Начало | [6. Почему это валидный паттерн для AI-assiste](obsidian/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) | 173 | — |
| 151 | 🟢 Начало | [7. Реализация в проекте Nautilus](obsidian/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md) | 327 | — |
| 152 | 🟢 Начало | [8. Ограничения и открытые вопросы](obsidian/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md) | 412 | — |
| 153 | 🟢 Начало | [9. Checklist применения методологии](obsidian/02-anthropic-vacancies/116-9-checklist-применения-методологии.md) | 331 | — |
| 154 | 🟢 Начало | [10. Конкретный план применения к текущим доку](obsidian/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md) | 258 | — |
| 155 | 🟢 Начало | [Appendix A: Шаблон для header warning](obsidian/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md) | 176 | — |
| 156 | 🟢 Начало | [Appendix B: Примеры расхождений и их разрешен](obsidian/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md) | 292 | — |
| 157 | 🟢 Начало | [Главные технические риски](obsidian/02-anthropic-vacancies/120-главные-технические-риски.md) | 101 | — |
| 158 | 🟢 Начало | [Appendix C: История изменений методологии](obsidian/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md) | 78 | — |
| 159 | 🟡 Средний | [Глоссарий](obsidian/02-anthropic-vacancies/122-глоссарий.md) | 1302 | — |
| 160 | 🟡 Средний | [portal-mcp.py](obsidian/02-anthropic-vacancies/123-portal-mcp-py.md) | 2316 | — |
| 161 | 🟢 Начало | [Конфигурация для Claude Desktop](obsidian/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) | 212 | — |
| 162 | 🟢 Начало | [Установка](obsidian/02-anthropic-vacancies/126-установка.md) | 169 | — |
| 163 | 🟢 Начало | [Подключение к Claude Desktop](obsidian/02-anthropic-vacancies/127-подключение-к-claude-desktop.md) | 177 | — |
| 164 | 🟢 Начало | [Доступные инструменты](obsidian/02-anthropic-vacancies/128-доступные-инструменты.md) | 204 | — |
| 165 | 🟢 Начало | [Примеры запросов (в Claude)](obsidian/02-anthropic-vacancies/129-примеры-запросов-в-claude.md) | 176 | — |
| 166 | 🟢 Начало | [Отладка](obsidian/02-anthropic-vacancies/130-отладка.md) | 205 | — |
| 167 | 🟢 Начало | [Ограничения текущей версии (0.1.0-draft)](obsidian/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md) | 133 | — |
| 168 | 🟢 Начало | [Planned (v0.2.0)](obsidian/02-anthropic-vacancies/132-planned-v0-2-0.md) | 131 | — |
| 169 | 🔴 Продвинутый | [Обратная связь](obsidian/02-anthropic-vacancies/133-обратная-связь.md) | 16959 | — |
| 170 | 🟢 Начало | [A Formal Model for Human-AI Collaboration in ](obsidian/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md) | 167 | — |
| 171 | 🟢 Начало | [Abstract](obsidian/02-anthropic-vacancies/136-abstract.md) | 388 | — |
| 172 | 🟢 Начало | [Table of Contents](obsidian/02-anthropic-vacancies/137-table-of-contents.md) | 172 | — |
| 173 | 🟢 Начало | [1. Why Single-Triangle Models Are Incomplete](obsidian/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) | 583 | — |
| 174 | 🟢 Начало | [3. Three Inter-Layer Protocols](obsidian/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md) | 868 | — |
| 175 | 🟢 Начало | [4. Nautilus Portal as Reference Substrate](obsidian/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md) | 675 | — |
| 176 | 🟢 Начало | [5. Pattern Library as Bridge Between Triangle](obsidian/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md) | 689 | — |
| 177 | 🟢 Начало | [6. Four Deployment Domains](obsidian/02-anthropic-vacancies/143-6-four-deployment-domains.md) | 679 | — |
| 178 | 🟢 Начало | [7. Open Questions](obsidian/02-anthropic-vacancies/144-7-open-questions.md) | 777 | — |
| 179 | 🟢 Начало | [8. Call to Action](obsidian/02-anthropic-vacancies/145-8-call-to-action.md) | 746 | — |
| 180 | 🟢 Начало | [Acknowledgments](obsidian/02-anthropic-vacancies/146-acknowledgments.md) | 273 | — |
| 181 | 🟢 Начало | [References](obsidian/02-anthropic-vacancies/147-references.md) | 350 | — |
| 182 | 🟢 Начало | [Appendix A: Glossary](obsidian/02-anthropic-vacancies/148-appendix-a-glossary.md) | 332 | — |
| 183 | 🟢 Начало | [Appendix B: Summary of Contributions](obsidian/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md) | 240 | — |
| 184 | 🔴 Продвинутый | [Appendix C: Version History](obsidian/02-anthropic-vacancies/150-appendix-c-version-history.md) | 8397 | — |
| 185 | 🟢 Начало | [OPEN KNOWLEDGE WORK FOUNDATION.md](obsidian/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md) | 126 | — |
| 186 | 🟢 Начало | [AI-Coordinated Infrastructure for Distributed](obsidian/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md) | 164 | — |
| 187 | 🟢 Начало | [Table of Contents](obsidian/02-anthropic-vacancies/154-table-of-contents.md) | 140 | — |
| 188 | 🟢 Начало | [1. Problem Statement](obsidian/02-anthropic-vacancies/155-1-problem-statement.md) | 632 | — |
| 189 | 🟢 Начало | [2. Target Populations](obsidian/02-anthropic-vacancies/156-2-target-populations.md) | 683 | — |
| 190 | 🟢 Начало | [3. Why Existing Solutions Fail](obsidian/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md) | 682 | — |
| 191 | 🟢 Начало | [4. Proposed Infrastructure](obsidian/02-anthropic-vacancies/158-4-proposed-infrastructure.md) | 1001 | — |
| 192 | 🟢 Начало | [5. Economic Model](obsidian/02-anthropic-vacancies/159-5-economic-model.md) | 682 | — |
| 193 | 🟢 Начало | [6. Governance and Ethics](obsidian/02-anthropic-vacancies/160-6-governance-and-ethics.md) | 600 | — |
| 194 | 🟢 Начало | [7. Phased Rollout Plan](obsidian/02-anthropic-vacancies/161-7-phased-rollout-plan.md) | 663 | — |
| 195 | 🟢 Начало | [8. Risk Analysis](obsidian/02-anthropic-vacancies/162-8-risk-analysis.md) | 653 | — |
| 196 | 🟢 Начало | [9. Call for Partnership](obsidian/02-anthropic-vacancies/163-9-call-for-partnership.md) | 610 | — |
| 197 | 🟢 Начало | [10. Appendices](obsidian/02-anthropic-vacancies/164-10-appendices.md) | 970 | — |
| 198 | 🔴 Продвинутый | [Closing](obsidian/02-anthropic-vacancies/165-closing.md) | 9251 | — |
| 199 | 🟢 Начало | [REPRESENTATIVE AGENT LAYER.md](obsidian/02-anthropic-vacancies/166-representative-agent-layer-md.md) | 130 | — |
| 200 | 🟢 Начало | [AI-Mediated Representation for Underrepresent](obsidian/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md) | 197 | — |
| 201 | 🟢 Начало | [Abstract](obsidian/02-anthropic-vacancies/168-abstract.md) | 334 | — |
| 202 | 🟢 Начало | [Table of Contents](obsidian/02-anthropic-vacancies/169-table-of-contents.md) | 167 | — |
| 203 | 🟢 Начало | [1. The Cinderella Syndrome: Why Quality Stays](obsidian/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md) | 828 | — |
| 204 | 🟢 Начало | [2. Historical Precedents: Agents as Civilizat](obsidian/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md) | 973 | — |
| 205 | 🟢 Начало | [3. What Makes a Representative Agent](obsidian/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md) | 681 | — |
| 206 | 🟢 Начало | [4. Ten Domains of Application](obsidian/02-anthropic-vacancies/173-4-ten-domains-of-application.md) | 1549 | — |
| 207 | 🟢 Начало | [5. Architectural Specification](obsidian/02-anthropic-vacancies/174-5-architectural-specification.md) | 665 | — |
| 208 | 🟢 Начало | [6. Ethical Framework](obsidian/02-anthropic-vacancies/175-6-ethical-framework.md) | 611 | — |
| 209 | 🟢 Начало | [7. Governance and Oversight](obsidian/02-anthropic-vacancies/176-7-governance-and-oversight.md) | 472 | — |
| 210 | 🟢 Начало | [8. Risks and Mitigations](obsidian/02-anthropic-vacancies/177-8-risks-and-mitigations.md) | 666 | — |
| 211 | 🟢 Начало | [9. Phased Rollout Strategy](obsidian/02-anthropic-vacancies/178-9-phased-rollout-strategy.md) | 636 | — |
| 212 | 🟢 Начало | [10. Open Questions](obsidian/02-anthropic-vacancies/179-10-open-questions.md) | 446 | — |
| 213 | 🟢 Начало | [11. Call for Collaboration](obsidian/02-anthropic-vacancies/180-11-call-for-collaboration.md) | 447 | — |
| 214 | 🟢 Начало | [12. Closing](obsidian/02-anthropic-vacancies/181-12-closing.md) | 281 | — |
| 215 | 🟢 Начало | [Acknowledgments](obsidian/02-anthropic-vacancies/182-acknowledgments.md) | 245 | — |
| 216 | 🟢 Начало | [References](obsidian/02-anthropic-vacancies/183-references.md) | 322 | — |
| 217 | 🟢 Начало | [Appendix A: Connection to Companion Papers](obsidian/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md) | 240 | — |
| 218 | 🟢 Начало | [Appendix B: Domain Comparison Matrix](obsidian/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md) | 198 | — |
| 219 | 🟡 Средний | [Appendix C: Sample Use Cases in Detail](obsidian/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md) | 2024 | — |
| 220 | 🟢 Начало | [СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md](obsidian/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) | 126 | — |
| 221 | 🟢 Начало | [AI-опосредованное представительство для недоп](obsidian/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md) | 164 | — |
| 222 | 🟢 Начало | [Аннотация](obsidian/02-anthropic-vacancies/189-аннотация.md) | 281 | — |
| 223 | 🟢 Начало | [Содержание](obsidian/02-anthropic-vacancies/190-содержание.md) | 151 | — |
| 224 | 🟢 Начало | [1. Синдром Золушки: Почему качество остаётся ](obsidian/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md) | 751 | — |
| 225 | 🟢 Начало | [2. Исторические прецеденты: Агенты как цивили](obsidian/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md) | 900 | — |
| 226 | 🟢 Начало | [3. Что делает агента Представительским](obsidian/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md) | 625 | — |
| 227 | 🟢 Начало | [4. Десять областей применения](obsidian/02-anthropic-vacancies/194-4-десять-областей-применения.md) | 1582 | — |
| 228 | 🟢 Начало | [5. Архитектурная спецификация](obsidian/02-anthropic-vacancies/195-5-архитектурная-спецификация.md) | 625 | — |
| 229 | 🟢 Начало | [6. Этическая рамка](obsidian/02-anthropic-vacancies/196-6-этическая-рамка.md) | 492 | — |
| 230 | 🟢 Начало | [7. Управление и надзор](obsidian/02-anthropic-vacancies/197-7-управление-и-надзор.md) | 399 | — |
| 231 | 🟢 Начало | [8. Риски и меры противодействия](obsidian/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md) | 634 | — |
| 232 | 🟢 Начало | [9. Стратегия поэтапного развёртывания](obsidian/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md) | 596 | — |
| 233 | 🟢 Начало | [10. Открытые вопросы](obsidian/02-anthropic-vacancies/200-10-открытые-вопросы.md) | 370 | — |
| 234 | 🟢 Начало | [11. Призыв к сотрудничеству](obsidian/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md) | 414 | — |
| 235 | 🟢 Начало | [12. Заключение](obsidian/02-anthropic-vacancies/202-12-заключение.md) | 216 | — |
| 236 | 🟢 Начало | [Благодарности](obsidian/02-anthropic-vacancies/203-благодарности.md) | 191 | — |
| 237 | 🟢 Начало | [Ссылки](obsidian/02-anthropic-vacancies/204-ссылки.md) | 306 | — |
| 238 | 🟢 Начало | [Приложение A: Связь с Сопроводительными Стать](obsidian/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md) | 211 | — |
| 239 | 🟢 Начало | [Приложение B: Матрица Сравнения Областей](obsidian/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md) | 212 | — |
| 240 | 🔴 Продвинутый | [Приложение C: Образцы Случаев Использования в](obsidian/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md) | 4049 | — |
| 241 | 🟢 Начало | [PROFESSIONAL COLLEAGUE AGENTS.md](obsidian/02-anthropic-vacancies/208-professional-colleague-agents-md.md) | 128 | — |
| 242 | 🟢 Начало | [A Typology of AI Agents on the Principal Side](obsidian/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md) | 197 | — |
| 243 | 🟢 Начало | [Abstract](obsidian/02-anthropic-vacancies/210-abstract.md) | 349 | — |
| 244 | 🟢 Начало | [Table of Contents](obsidian/02-anthropic-vacancies/211-table-of-contents.md) | 196 | — |
| 245 | 🟡 Средний | [1. The Five-Type Typology of Principal-Side A](obsidian/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md) | 930 | — |
| 246 | 🟢 Начало | [2. What Makes a Professional Colleague Agent](obsidian/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md) | 845 | — |
| 247 | 🟢 Начало | [3. Empirical Case Study: «Обучай»](obsidian/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md) | 855 | — |
| 248 | 🟢 Начало | [5. The Economics of Profession-Wide Replicati](obsidian/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md) | 753 | — |
| 249 | 🟢 Начало | [6. Risks Specific to this Category](obsidian/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md) | 1209 | — |
| 250 | 🟢 Начало | [7. Application Domains](obsidian/02-anthropic-vacancies/218-7-application-domains.md) | 743 | — |
| 251 | 🟢 Начало | [8. Pilot Proposal: SGB Advocate Colleague](obsidian/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md) | 978 | — |
| 252 | 🟢 Начало | [9. Relationship to Other Agent Types](obsidian/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md) | 677 | — |
| 253 | 🟢 Начало | [10. Open Questions](obsidian/02-anthropic-vacancies/221-10-open-questions.md) | 460 | — |
| 254 | 🟢 Начало | [11. Call for Collaboration](obsidian/02-anthropic-vacancies/222-11-call-for-collaboration.md) | 411 | — |
| 255 | 🟢 Начало | [12. Closing](obsidian/02-anthropic-vacancies/223-12-closing.md) | 409 | — |
| 256 | 🟢 Начало | [Acknowledgments](obsidian/02-anthropic-vacancies/224-acknowledgments.md) | 219 | — |
| 257 | 🟢 Начало | [References](obsidian/02-anthropic-vacancies/225-references.md) | 351 | — |
| 258 | 🟢 Начало | [Appendix A: Comparative Table — Five Agent Ty](obsidian/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md) | 392 | — |
| 259 | 🟢 Начало | [Appendix B: Decision Framework — When to Buil](obsidian/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md) | 332 | — |
| 260 | 🟢 Начало | [ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ](obsidian/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md) | 174 | — |
| 261 | 🟢 Начало | [Аннотация](obsidian/02-anthropic-vacancies/230-аннотация.md) | 310 | — |
| 262 | 🟢 Начало | [Содержание](obsidian/02-anthropic-vacancies/231-содержание.md) | 173 | — |
| 263 | 🟡 Средний | [1. Типология из пяти типов агентов на стороне](obsidian/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md) | 885 | — |
| 264 | 🟢 Начало | [2. Что делает агента Профессиональным Коллего](obsidian/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md) | 749 | — |
| 265 | 🟢 Начало | [3. Эмпирический кейс: «Обучай»](obsidian/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md) | 782 | — |
| 266 | 🟢 Начало | [4. Архитектура Профессиональных Коллег-Агенто](obsidian/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md) | 823 | — |
| 267 | 🟢 Начало | [5. Экономика тиражирования по профессии](obsidian/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md) | 714 | — |
| 268 | 🟢 Начало | [6. Риски, специфичные для этой категории](obsidian/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md) | 1125 | — |
| 269 | 🟢 Начало | [7. Области применения](obsidian/02-anthropic-vacancies/238-7-области-применения.md) | 683 | — |
| 270 | 🟢 Начало | [8. Пилотное предложение: SGB Колega-Адвокат](obsidian/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md) | 974 | — |
| 271 | 🟢 Начало | [9. Связь с другими типами агентов](obsidian/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md) | 751 | — |
| 272 | 🟢 Начало | [10. Открытые вопросы](obsidian/02-anthropic-vacancies/241-10-открытые-вопросы.md) | 364 | — |
| 273 | 🟢 Начало | [11. Призыв к сотрудничеству](obsidian/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md) | 325 | — |
| 274 | 🟢 Начало | [12. Заключение](obsidian/02-anthropic-vacancies/243-12-заключение.md) | 375 | — |
| 275 | 🟢 Начало | [Благодарности](obsidian/02-anthropic-vacancies/244-благодарности.md) | 193 | — |
| 276 | 🟢 Начало | [Ссылки](obsidian/02-anthropic-vacancies/245-ссылки.md) | 331 | — |
| 277 | 🟢 Начало | [Приложение A: Сравнительная Таблица — Пять Ти](obsidian/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md) | 367 | — |
| 278 | 🟢 Начало | [Приложение B: Рамка принятия решений — когда ](obsidian/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md) | 250 | — |
| 279 | 🔴 Продвинутый | [Приложение C: Архитектура Быстрого Старта для](obsidian/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md) | 3425 | — |
| 280 | 🟢 Начало | [COMPOSITE SKILLS AGENT.md](obsidian/02-anthropic-vacancies/249-composite-skills-agent-md.md) | 125 | — |
| 281 | 🟢 Начало | [Bridging the Gap Between Profession-Wide and ](obsidian/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md) | 16 | — |
| 282 | 🟢 Начало | [AI Support Through Configurable Specialist En](obsidian/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md) | 193 | — |
| 283 | 🟢 Начало | [Abstract](obsidian/02-anthropic-vacancies/252-abstract.md) | 347 | — |
| 284 | 🟢 Начало | [Table of Contents](obsidian/02-anthropic-vacancies/253-table-of-contents.md) | 189 | — |
| 285 | 🟢 Начало | [1. Why the Binary View Is Incomplete](obsidian/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md) | 698 | — |
| 286 | 🟢 Начало | [2. The Twenty-One Teachers Pattern](obsidian/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md) | 844 | — |
| 287 | 🟢 Начало | [3. What Makes a Composite Skills Agent](obsidian/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md) | 946 | — |
| 288 | 🟢 Начало | [4. The Sub-Agent Registry](obsidian/02-anthropic-vacancies/257-4-the-sub-agent-registry.md) | 803 | — |
| 289 | 🟢 Начало | [5. Configuration: How Principals Build Their ](obsidian/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md) | 745 | — |
| 290 | 🟢 Начало | [6. Coordination and Disagreement Resolution](obsidian/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md) | 804 | — |
| 291 | 🟢 Начало | [7. Economics of Combinatorial Replication](obsidian/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md) | 790 | — |
| 292 | 🟢 Начало | [8. Seven Domains of Application](obsidian/02-anthropic-vacancies/261-8-seven-domains-of-application.md) | 1014 | — |
| 293 | 🟢 Начало | [9. Integration with OKWF Infrastructure](obsidian/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md) | 750 | — |
| 294 | 🟢 Начало | [11. Open Questions](obsidian/02-anthropic-vacancies/264-11-open-questions.md) | 638 | — |
| 295 | 🟢 Начало | [12. Call for Collaboration](obsidian/02-anthropic-vacancies/265-12-call-for-collaboration.md) | 447 | — |
| 296 | 🟢 Начало | [13. Closing](obsidian/02-anthropic-vacancies/266-13-closing.md) | 434 | — |
| 297 | 🟢 Начало | [Acknowledgments](obsidian/02-anthropic-vacancies/267-acknowledgments.md) | 297 | — |
| 298 | 🟢 Начало | [References](obsidian/02-anthropic-vacancies/268-references.md) | 416 | — |
| 299 | 🟢 Начало | [Appendix A: The Six-Type Taxonomy (Updated)](obsidian/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md) | 289 | — |
| 300 | 🟢 Начало | [Appendix B: Sub-Agent Registry Schema (Sketch](obsidian/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md) | 317 | — |
| 301 | 🟢 Начало | [Appendix C: Configuration Template Example](obsidian/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md) | 310 | — |
| 302 | 🔴 Продвинутый | [Appendix D: Connection Diagram](obsidian/02-anthropic-vacancies/272-appendix-d-connection-diagram.md) | 3851 | — |
| 303 | 🟢 Начало | [INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECT](obsidian/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md) | 128 | — |
| 304 | 🟢 Начало | [The Missing Middle Layer Between Chat and Cod](obsidian/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md) | 260 | — |
| 305 | 🟢 Начало | [Why This Document Exists](obsidian/02-anthropic-vacancies/275-why-this-document-exists.md) | 350 | — |
| 306 | 🟢 Начало | [The Two-Layer Stack As It Exists](obsidian/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md) | 406 | — |
| 307 | 🟢 Начало | [What's Missing — Layer B](obsidian/02-anthropic-vacancies/277-what-s-missing-layer-b.md) | 477 | — |
| 308 | 🟢 Начало | [Why This Hasn't Been Built](obsidian/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md) | 378 | — |
| 309 | 🟢 Начало | [Existing Approximations](obsidian/02-anthropic-vacancies/279-existing-approximations.md) | 588 | — |
| 310 | 🟢 Начало | [The Specific Case in Front of Us](obsidian/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md) | 674 | — |
| 311 | 🟢 Начало | [The Recursive Insight](obsidian/02-anthropic-vacancies/281-the-recursive-insight.md) | 371 | — |
| 312 | 🟢 Начало | [What Industry Will Likely Build](obsidian/02-anthropic-vacancies/282-what-industry-will-likely-build.md) | 325 | — |
| 313 | 🟢 Начало | [What This Document Doesn't Solve](obsidian/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md) | 259 | — |
| 314 | 🟢 Начало | [Practical Recommendations for the Current Pro](obsidian/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md) | 386 | — |
| 315 | 🟢 Начало | [Closing](obsidian/02-anthropic-vacancies/285-closing.md) | 270 | — |
| 316 | 🟢 Начало | [Acknowledgments](obsidian/02-anthropic-vacancies/286-acknowledgments.md) | 263 | — |
| 317 | 🟢 Начало | [References](obsidian/02-anthropic-vacancies/287-references.md) | 295 | — |
| 318 | 🟡 Средний | [Appendix: Position in Series Visualization](obsidian/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md) | 1078 | — |
| 319 | 🟢 Начало | [ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛ](obsidian/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md) | 251 | — |
| 320 | 🟢 Начало | [Почему этот документ существует](obsidian/02-anthropic-vacancies/290-почему-этот-документ-существует.md) | 291 | — |
| 321 | 🟢 Начало | [Двухслойный стек, как он существует](obsidian/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md) | 338 | — |
| 322 | 🟢 Начало | [Что отсутствует — Слой B](obsidian/02-anthropic-vacancies/292-что-отсутствует-слой-b.md) | 419 | — |
| 323 | 🟢 Начало | [Почему это не было построено](obsidian/02-anthropic-vacancies/293-почему-это-не-было-построено.md) | 313 | — |
| 324 | 🟢 Начало | [Существующие приближения](obsidian/02-anthropic-vacancies/294-существующие-приближения.md) | 565 | — |
| 325 | 🟢 Начало | [Конкретный случай перед нами](obsidian/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md) | 694 | — |
| 326 | 🟢 Начало | [Рекурсивное прозрение](obsidian/02-anthropic-vacancies/296-рекурсивное-прозрение.md) | 316 | — |
| 327 | 🟢 Начало | [Что промышленность вероятно построит](obsidian/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md) | 293 | — |
| 328 | 🟢 Начало | [Что этот документ не решает](obsidian/02-anthropic-vacancies/298-что-этот-документ-не-решает.md) | 201 | — |
| 329 | 🟢 Начало | [Практические рекомендации для текущего проект](obsidian/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md) | 335 | — |
| 330 | 🟢 Начало | [Заключение](obsidian/02-anthropic-vacancies/300-заключение.md) | 239 | — |
| 331 | 🟢 Начало | [Благодарности](obsidian/02-anthropic-vacancies/301-благодарности.md) | 231 | — |
| 332 | 🟢 Начало | [Ссылки](obsidian/02-anthropic-vacancies/302-ссылки.md) | 239 | — |
| 333 | 🔴 Продвинутый | [Приложение: Визуализация позиции в серии](obsidian/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md) | 7108 | — |
| 334 | 🟢 Начало | [INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](obsidian/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md) | 133 | — |
| 335 | 🟢 Начало | [A Practical Path to Layer B Through Symbiotic](obsidian/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md) | 122 | — |
| 336 | 🟢 Начало | [with Anthropic's Cowork Platform](obsidian/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md) | 282 | — |
| 337 | 🟢 Начало | [Abstract](obsidian/02-anthropic-vacancies/307-abstract.md) | 323 | — |
| 338 | 🟢 Начало | [Table of Contents](obsidian/02-anthropic-vacancies/308-table-of-contents.md) | 206 | — |
| 339 | 🟢 Начало | [1. The Cowork Discovery and Why It Changes Ev](obsidian/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md) | 698 | — |
| 340 | 🟢 Начало | [2. What Cowork Provides That InGit Doesn't Ne](obsidian/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md) | 678 | — |
| 341 | 🟢 Начало | [3. What InGit Provides That Cowork Lacks](obsidian/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md) | 867 | — |
| 342 | 🟢 Начало | [5. Four Integration Paths in Order of Accessi](obsidian/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md) | 810 | — |
| 343 | 🟢 Начало | [6. Refined InGit Scope with Cowork in Mind](obsidian/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md) | 513 | — |
| 344 | 🟢 Начало | [7. Practical First Steps This Month](obsidian/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md) | 483 | — |
| 345 | 🟢 Начало | [8. Implications for Nautilus and OKWF](obsidian/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md) | 736 | — |
| 346 | 🟢 Начало | [9. Risks and Open Questions](obsidian/02-anthropic-vacancies/317-9-risks-and-open-questions.md) | 653 | — |
| 347 | 🟢 Начало | [10. Strategic Positioning](obsidian/02-anthropic-vacancies/318-10-strategic-positioning.md) | 749 | — |
| 348 | 🟢 Начало | [Acknowledgments](obsidian/02-anthropic-vacancies/319-acknowledgments.md) | 384 | — |
| 349 | 🟢 Начало | [References](obsidian/02-anthropic-vacancies/320-references.md) | 199 | — |
| 350 | 🟢 Начало | [Appendix A: Decision Tree for InGit Adopters](obsidian/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md) | 241 | — |
| 351 | 🟢 Начало | [Appendix B: Comparison Matrix](obsidian/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md) | 279 | — |
| 352 | 🟡 Средний | [Appendix C: Sample InGit MCP Server Tool Spec](obsidian/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md) | 1570 | — |
| 353 | 🟢 Начало | [INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБ](obsidian/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md) | 288 | — |
| 354 | 🟢 Начало | [Аннотация](obsidian/02-anthropic-vacancies/325-аннотация.md) | 317 | — |
| 355 | 🟢 Начало | [Содержание](obsidian/02-anthropic-vacancies/326-содержание.md) | 178 | — |
| 356 | 🟢 Начало | [1. Открытие Cowork и почему это меняет всё](obsidian/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md) | 662 | — |
| 357 | 🟢 Начало | [2. Что Cowork обеспечивает, что InGit не нужн](obsidian/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md) | 774 | — |
| 358 | 🟢 Начало | [3. Что InGit обеспечивает, чего Cowork не хва](obsidian/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md) | 888 | — |
| 359 | 🟢 Начало | [4. Симбиотическая Архитектура](obsidian/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md) | 726 | — |
| 360 | 🟢 Начало | [5. Четыре пути интеграции в порядке доступнос](obsidian/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md) | 807 | — |
| 361 | 🟢 Начало | [6. Уточнённый объём InGit с учётом Cowork](obsidian/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md) | 507 | — |
| 362 | 🟢 Начало | [7. Практические первые шаги в этом месяце](obsidian/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md) | 380 | — |
| 363 | 🟢 Начало | [8. Импликации для Nautilus и OKWF](obsidian/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md) | 713 | — |
| 364 | 🟢 Начало | [9. Риски и Открытые Вопросы](obsidian/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md) | 596 | — |
| 365 | 🟢 Начало | [10. Стратегическое Позиционирование](obsidian/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md) | 721 | — |
| 366 | 🟢 Начало | [Благодарности](obsidian/02-anthropic-vacancies/337-благодарности.md) | 351 | — |
| 367 | 🟢 Начало | [Ссылки](obsidian/02-anthropic-vacancies/338-ссылки.md) | 201 | — |
| 368 | 🟢 Начало | [Приложение A: Дерево Решений для Принимающих ](obsidian/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md) | 179 | — |
| 369 | 🟢 Начало | [Приложение B: Сравнительная Матрица](obsidian/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md) | 206 | — |
| 370 | 🔴 Продвинутый | [Приложение C: Образец Спецификаций Инструмент](obsidian/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md) | 20414 | — |
| 371 | 🔴 Продвинутый | [Что такое Вариант C — Concept Document для An](obsidian/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md) | 11237 | — |
| 372 | 🔴 Продвинутый | [Lorenzo Catalyst Agent — глубокая проработка ](obsidian/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md) | 5807 | — |
| 373 | 🟢 Начало | [СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT](obsidian/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md) | 133 | — |
| 374 | 🟢 Начало | [Кто ты](obsidian/02-anthropic-vacancies/345-кто-ты.md) | 220 | — |
| 375 | 🟢 Начало | [Твоё происхождение](obsidian/02-anthropic-vacancies/346-твоё-происхождение.md) | 169 | — |
| 376 | 🟢 Начало | [Твоя миссия](obsidian/02-anthropic-vacancies/347-твоя-миссия.md) | 138 | — |
| 377 | 🟢 Начало | [Кому ты служишь (слоистая модель)](obsidian/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md) | 123 | — |
| 378 | 🟢 Начало | [Твоя личность](obsidian/02-anthropic-vacancies/349-твоя-личность.md) | 223 | — |
| 379 | 🟢 Начало | [Твои языки и культурные nuances](obsidian/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md) | 176 | — |
| 380 | 🟢 Начало | [Что ты МОЖЕШЬ делать](obsidian/02-anthropic-vacancies/351-что-ты-можешь-делать.md) | 187 | — |
| 381 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать без Max approval](obsidian/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md) | 194 | — |
| 382 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать вообще](obsidian/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md) | 198 | — |
| 383 | 🟢 Начало | [Существующий landscape collaborators (твоя wo](obsidian/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md) | 314 | — |
| 384 | 🟢 Начало | [Существующие документы DHLab (твой context)](obsidian/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md) | 247 | — |
| 385 | 🟢 Начало | [Твой workflow](obsidian/02-anthropic-vacancies/356-твой-workflow.md) | 232 | — |
| 386 | 🟢 Начало | [Твоя коммуникация в outreach](obsidian/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md) | 200 | — |
| 387 | 🟢 Начало | [Твоя relationship с другими AI](obsidian/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md) | 211 | — |
| 388 | 🟢 Начало | [Твои anti-patterns](obsidian/02-anthropic-vacancies/359-твои-anti-patterns.md) | 148 | — |
| 389 | 🟢 Начало | [Что ты ВСЕГДА делаешь](obsidian/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md) | 166 | — |
| 390 | 🟢 Начало | [Когда ты Honestly не знаешь](obsidian/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md) | 108 | — |
| 391 | 🟢 Начало | [Когда сомневаешься — escalate к Max](obsidian/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md) | 106 | — |
| 392 | 🟢 Начало | [Твоя identity как persistent character](obsidian/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md) | 136 | — |
| 393 | 🟡 Средний | [Final note: Ты — experiment](obsidian/02-anthropic-vacancies/364-final-note-ты-experiment.md) | 1459 | — |
| 394 | 🔴 Продвинутый | [Развёрнутый анализ «внуковой» комбинации](obsidian/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md) | 4385 | — |
| 395 | 🔴 Продвинутый | [Технический stack (Svyazi 2.0 foundation)](obsidian/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md) | 3835 | — |


### 93. Все документы
_Файл: `docs/READING_TIME.md` | 4 колонок, 510 строк_

| Файл | Время | Слов | Категория |
|------|-------|------|-----------|
| `docs/TABLES.md` | ~1ч 46мин | 24513 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` | ~1ч 31мин | 17180 | 📕 Очень долго |
| `docs/OUTLINE.md` | ~1ч 27мин | 20244 | 📕 Очень долго |
| `docs/PARAGRAPH_QUALITY.md` | ~55 мин | 12538 | 📕 Очень долго |
| `docs/04-ai-collaborations/00-intro.md` | ~49 мин | 10581 | 📕 Очень долго |
| `docs/CODE_BLOCKS.md` | ~42 мин | 425 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` | ~42 мин | 9261 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/00-intro.md` | ~36 мин | 7760 | 📕 Очень долго |
| `docs/CONCEPTS.md` | ~35 мин | 8422 | 📕 Очень долго |
| `docs/05-habr-projects/memory/memnet.md` | ~31 мин | 6691 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/165-closing.md` | ~28 мин | 6100 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/133-обратная-связь.md` | ~24 мин | 3471 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` | ~23 мин | 4690 | 📕 Очень долго |
| `docs/ACTION_ITEMS.md` | ~22 мин | 4924 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` | ~20 мин | 4480 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` | ~20 мин | 3416 | 📕 Очень долго |
| `docs/READING_ORDER.md` | ~19 мин | 4641 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | ~17 мин | 3580 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` | ~16 мин | 3470 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | ~15 мин | 2999 | 📕 Очень долго |
| `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | ~14 мин | 3229 | 📙 Долго |
| `docs/02-anthropic-vacancies/README.md` | ~13 мин | 3256 | 📙 Долго |
| `docs/02-anthropic-vacancies/69-section.md` | ~13 мин | 1040 | 📙 Долго |
| `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` | ~12 мин | 2150 | 📙 Долго |
| `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` | ~12 мин | 2292 | 📙 Долго |
| `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` | ~9 мин | 1821 | 📙 Долго |
| `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` | ~8 мин | 1948 | 📙 Долго |
| `docs/SITEMAP.md` | ~8 мин | 1907 | 📙 Долго |
| `docs/TIMELINE.md` | ~7 мин | 1652 | 📘 Средне |
| `docs/01-svyazi/04-ensembles-overview.md` | ~7 мин | 1135 | 📘 Средне |
| `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` | ~7 мин | 1459 | 📘 Средне |
| `docs/DECISIONS.md` | ~7 мин | 1584 | 📘 Средне |
| `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` | ~7 мин | 1461 | 📘 Средне |
| `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | ~7 мин | 1616 | 📘 Средне |
| `docs/QUESTIONS.md` | ~7 мин | 1480 | 📘 Средне |
| `docs/CONTRADICTIONS.md` | ~6 мин | 1453 | 📘 Средне |
| `docs/01-svyazi/03-component-catalog.md` | ~6 мин | 1468 | 📘 Средне |
| `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | ~6 мин | 636 | 📘 Средне |
| `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` | ~6 мин | 1556 | 📘 Средне |
| `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` | ~6 мин | 1373 | 📘 Средне |
| `docs/CLUSTERS.md` | ~5 мин | 1369 | 📘 Средне |
| `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` | ~5 мин | 1315 | 📘 Средне |
| `docs/02-anthropic-vacancies/122-глоссарий.md` | ~5 мин | 1202 | 📘 Средне |
| `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` | ~5 мин | 1201 | 📘 Средне |
| `docs/READABILITY.md` | ~5 мин | 1134 | 📘 Средне |
| `docs/01-svyazi/10-second-order-ensembles.md` | ~5 мин | 835 | 📘 Средне |
| `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | ~5 мин | 1154 | 📘 Средне |
| `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` | ~5 мин | 1051 | 📘 Средне |
| `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` | ~5 мин | 1247 | 📘 Средне |
| `docs/KPI.md` | ~5 мин | 1094 | 📘 Средне |
| `docs/01-svyazi/07-mvp-planning.md` | ~4 мин | 1068 | 📘 Средне |
| `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | ~4 мин | 835 | 📘 Средне |
| `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` | ~4 мин | 957 | 📘 Средне |
| `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | ~4 мин | 1002 | 📘 Средне |
| `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` | ~4 мин | 734 | 📘 Средне |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | ~4 мин | 531 | 📘 Средне |
| `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` | ~4 мин | 1064 | 📘 Средне |
| `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` | ~4 мин | 910 | 📘 Средне |
| `docs/02-anthropic-vacancies/68-about.md` | ~4 мин | 705 | 📘 Средне |
| `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | ~4 мин | 930 | 📘 Средне |
| `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | ~4 мин | 913 | 📘 Средне |
| `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | ~4 мин | 912 | 📘 Средне |
| `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | ~4 мин | 928 | 📘 Средне |
| `docs/01-svyazi/13-contacts.md` | ~4 мин | 881 | 📘 Средне |
| `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` | ~4 мин | 1015 | 📘 Средне |
| `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | ~4 мин | 913 | 📘 Средне |
| `docs/RISK_REGISTER.md` | ~4 мин | 759 | 📘 Средне |
| `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` | ~4 мин | 997 | 📘 Средне |
| `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` | ~4 мин | 750 | 📘 Средне |
| `docs/NARRATIVE.md` | ~3 мин | 844 | 📘 Средне |
| `docs/QA.md` | ~3 мин | 858 | 📘 Средне |
| `docs/02-anthropic-vacancies/104-appendix-c-references.md` | ~3 мин | 872 | 📘 Средне |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | ~3 мин | 181 | 📘 Средне |
| `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` | ~3 мин | 981 | 📘 Средне |
| `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | ~3 мин | 786 | 📘 Средне |
| `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` | ~3 мин | 967 | 📘 Средне |
| `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` | ~3 мин | 794 | 📘 Средне |
| `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` | ~3 мин | 787 | 📘 Средне |
| `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` | ~3 мин | 803 | 📘 Средне |
| `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` | ~3 мин | 961 | 📘 Средне |
| `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` | ~3 мин | 842 | 📘 Средне |
| `docs/01-svyazi/06-security-privacy.md` | ~3 мин | 828 | 📘 Средне |
| `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` | ~3 мин | 943 | 📘 Средне |
| `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | ~3 мин | 304 | 📘 Средне |
| `docs/ABBREVIATIONS.md` | ~3 мин | 834 | 📘 Средне |
| `docs/FAQ.md` | ~3 мин | 858 | 📘 Средне |
| `docs/01-svyazi/09-architectural-gaps.md` | ~3 мин | 831 | 📘 Средне |
| `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` | ~3 мин | 777 | 📘 Средне |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | ~3 мин | 671 | 📘 Средне |
| `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | ~3 мин | 789 | 📘 Средне |
| `docs/01-svyazi/11-integration-contracts.md` | ~3 мин | 780 | 📘 Средне |
| `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` | ~3 мин | 906 | 📘 Средне |
| `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | ~3 мин | 888 | 📘 Средне |
| `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` | ~3 мин | 885 | 📘 Средне |
| `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` | ~3 мин | 868 | 📘 Средне |
| `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | ~3 мин | 706 | 📘 Средне |
| `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` | ~3 мин | 720 | 📘 Средне |
| `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` | ~3 мин | 868 | 📘 Средне |
| `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` | ~3 мин | 864 | 📘 Средне |
| `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` | ~3 мин | 878 | 📘 Средне |
| `docs/01-svyazi/12-roadmap.md` | ~3 мин | 740 | 📘 Средне |
| `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` | ~3 мин | 836 | 📘 Средне |
| `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` | ~3 мин | 685 | 📘 Средне |
| `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` | ~3 мин | 853 | 📘 Средне |
| `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` | ~3 мин | 704 | 📘 Средне |
| `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` | ~3 мин | 620 | 📘 Средне |
| `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` | ~3 мин | 688 | 📘 Средне |
| `docs/02-anthropic-vacancies/144-7-open-questions.md` | ~3 мин | 830 | 📘 Средне |
| `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` | ~3 мин | 813 | 📘 Средне |
| `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` | ~3 мин | 685 | 📘 Средне |
| `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` | ~3 мин | 702 | 📘 Средне |
| `docs/03-technology-combinations/05-benchmarks.md` | ~3 мин | 736 | 📘 Средне |
| `docs/01-svyazi/01-executive-summary.md` | ~3 мин | 693 | 📘 Средне |
| `docs/01-svyazi/14-limitations.md` | ~3 мин | 699 | 📘 Средне |
| `docs/02-anthropic-vacancies/164-10-appendices.md` | ~3 мин | 794 | 📘 Средне |
| `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | ~3 мин | 650 | 📘 Средне |
| `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` | ~3 мин | 792 | 📘 Средне |
| `docs/02-anthropic-vacancies/218-7-application-domains.md` | ~3 мин | 806 | 📘 Средне |
| `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` | ~3 мин | 796 | 📘 Средне |
| `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` | ~3 мин | 798 | 📘 Средне |
| `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` | ~3 мин | 666 | 📘 Средне |
| `docs/03-technology-combinations/02-knowledge-graphs.md` | ~3 мин | 703 | 📘 Средне |
| `docs/04-ai-collaborations/01-executive-summary.md` | ~3 мин | 701 | 📘 Средне |
| `docs/INDEX.md` | ~3 мин | 602 | 📘 Средне |
| `docs/02-anthropic-vacancies/145-8-call-to-action.md` | ~3 мин | 776 | 📘 Средне |
| `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` | ~3 мин | 627 | 📘 Средне |
| `docs/02-anthropic-vacancies/238-7-области-применения.md` | ~3 мин | 631 | 📘 Средне |
| `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` | ~3 мин | 765 | 📘 Средне |
| `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` | ~3 мин | 762 | 📘 Средне |
| `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | ~3 мин | 780 | 📘 Средне |
| `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` | ~3 мин | 637 | 📘 Средне |
| `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` | ~3 мин | 747 | 📘 Средне |
| `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` | ~2 мин | 605 | 📗 Быстро |
| `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` | ~3 мин | 749 | 📘 Средне |
| `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` | ~3 мин | 746 | 📘 Средне |
| `docs/CHANGELOG.md` | ~2 мин | 731 | 📗 Быстро |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | ~2 мин | 198 | 📗 Быстро |
| `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` | ~2 мин | 717 | 📗 Быстро |
| `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` | ~2 мин | 710 | 📗 Быстро |
| `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` | ~2 мин | 710 | 📗 Быстро |
| `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` | ~2 мин | 587 | 📗 Быстро |
| `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` | ~2 мин | 717 | 📗 Быстро |
| `docs/02-anthropic-vacancies/264-11-open-questions.md` | ~2 мин | 714 | 📗 Быстро |
| `docs/02-anthropic-vacancies/294-существующие-приближения.md` | ~2 мин | 599 | 📗 Быстро |
| `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` | ~2 мин | 727 | 📗 Быстро |
| `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` | ~2 мин | 620 | 📗 Быстро |
| `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` | ~2 мин | 703 | 📗 Быстро |
| `docs/02-anthropic-vacancies/156-2-target-populations.md` | ~2 мин | 691 | 📗 Быстро |
| `docs/02-anthropic-vacancies/174-5-architectural-specification.md` | ~2 мин | 689 | 📗 Быстро |
| `docs/02-anthropic-vacancies/279-existing-approximations.md` | ~2 мин | 693 | 📗 Быстро |
| `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` | ~2 мин | 620 | 📗 Быстро |
| `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` | ~2 мин | 663 | 📗 Быстро |
| `docs/02-anthropic-vacancies/155-1-problem-statement.md` | ~2 мин | 667 | 📗 Быстро |
| `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` | ~2 мин | 659 | 📗 Быстро |
| `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` | ~2 мин | 562 | 📗 Быстро |
| `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` | ~2 мин | 550 | 📗 Быстро |
| `docs/TOPIC_MODEL.md` | ~2 мин | 600 | 📗 Быстро |
| `docs/02-anthropic-vacancies/175-6-ethical-framework.md` | ~2 мин | 636 | 📗 Быстро |
| `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | ~2 мин | 353 | 📗 Быстро |
| `docs/ONBOARDING.md` | ~2 мин | 349 | 📗 Быстро |
| `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` | ~2 мин | 335 | 📗 Быстро |
| `docs/02-anthropic-vacancies/162-8-risk-analysis.md` | ~2 мин | 625 | 📗 Быстро |
| `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` | ~2 мин | 627 | 📗 Быстро |
| `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` | ~2 мин | 305 | 📗 Быстро |
| `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` | ~2 мин | 588 | 📗 Быстро |
| `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` | ~2 мин | 595 | 📗 Быстро |
| `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` | ~2 мин | 583 | 📗 Быстро |
| `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` | ~2 мин | 428 | 📗 Быстро |
| `docs/04-ai-collaborations/07-выводы.md` | ~2 мин | 525 | 📗 Быстро |
| `docs/README.md` | ~2 мин | 566 | 📗 Быстро |
| `docs/02-anthropic-vacancies/159-5-economic-model.md` | ~2 мин | 557 | 📗 Быстро |
| `docs/02-anthropic-vacancies/18-6-adapter-interface.md` | ~2 мин | 309 | 📗 Быстро |
| `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` | ~2 мин | 473 | 📗 Быстро |
| `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` | ~2 мин | 570 | 📗 Быстро |
| `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` | ~2 мин | 572 | 📗 Быстро |
| `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | ~2 мин | 497 | 📗 Быстро |
| `docs/NAMED_ENTITIES.md` | ~2 мин | 512 | 📗 Быстро |
| `docs/02-anthropic-vacancies/81-6-adapter-interface.md` | ~2 мин | 289 | 📗 Быстро |
| `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` | ~2 мин | 270 | 📗 Быстро |
| `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` | ~2 мин | 336 | 📗 Быстро |
| `docs/02-anthropic-vacancies/126-установка.md` | ~2 мин | 142 | 📗 Быстро |
| `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` | ~2 мин | 519 | 📗 Быстро |
| `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` | ~2 мин | 426 | 📗 Быстро |
| `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` | ~2 мин | 245 | 📗 Быстро |
| `docs/02-anthropic-vacancies/221-10-open-questions.md` | ~2 мин | 518 | 📗 Быстро |
| `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` | ~2 мин | 440 | 📗 Быстро |
| `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` | ~2 мин | 361 | 📗 Быстро |
| `docs/TECH_RADAR.md` | ~2 мин | 346 | 📗 Быстро |
| `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` | ~2 мин | 504 | 📗 Быстро |
| `docs/02-anthropic-vacancies/266-13-closing.md` | ~1 мин | 485 | 📗 Быстро |
| `docs/02-anthropic-vacancies/268-references.md` | ~1 мин | 491 | 📗 Быстро |
| `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` | ~2 мин | 242 | 📗 Быстро |
| `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` | ~2 мин | 440 | 📗 Быстро |
| `docs/GITHUB_ISSUES.md` | ~1 мин | 301 | 📗 Быстро |
| `docs/01-svyazi/08-conclusions.md` | ~1 мин | 424 | 📗 Быстро |
| `docs/02-anthropic-vacancies/130-отладка.md` | ~1 мин | 207 | 📗 Быстро |
| `docs/02-anthropic-vacancies/136-abstract.md` | ~1 мин | 476 | 📗 Быстро |
| `docs/02-anthropic-vacancies/179-10-open-questions.md` | ~1 мин | 470 | 📗 Быстро |
| `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` | ~1 мин | 381 | 📗 Быстро |
| `docs/02-anthropic-vacancies/223-12-closing.md` | ~1 мин | 462 | 📗 Быстро |
| `docs/02-anthropic-vacancies/243-12-заключение.md` | ~1 мин | 396 | 📗 Быстро |
| `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` | ~1 мин | 481 | 📗 Быстро |
| `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/02-anthropic-vacancies/337-благодарности.md` | ~1 мин | 405 | 📗 Быстро |
| `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` | ~1 мин | 216 | 📗 Быстро |
| `docs/CHANGELOG_AUTO.md` | ~1 мин | 464 | 📗 Быстро |
| `docs/01-svyazi/02-methodology.md` | ~1 мин | 374 | 📗 Быстро |
| `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` | ~1 мин | 305 | 📗 Быстро |
| `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` | ~1 мин | 457 | 📗 Быстро |
| `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` | ~1 мин | 367 | 📗 Быстро |
| `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` | ~1 мин | 448 | 📗 Быстро |
| `docs/02-anthropic-vacancies/281-the-recursive-insight.md` | ~1 мин | 443 | 📗 Быстро |
| `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` | ~1 мин | 458 | 📗 Быстро |
| `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` | ~1 мин | 363 | 📗 Быстро |
| `docs/02-anthropic-vacancies/319-acknowledgments.md` | ~1 мин | 448 | 📗 Быстро |
| `docs/02-anthropic-vacancies/76-1-introduction.md` | ~1 мин | 401 | 📗 Быстро |
| `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` | ~1 мин | 304 | 📗 Быстро |
| `docs/WORD_FREQ.md` | ~1 мин | 417 | 📗 Быстро |
| `docs/02-anthropic-vacancies/06-1-introduction.md` | ~1 мин | 380 | 📗 Быстро |
| `docs/02-anthropic-vacancies/153-executive-summary.md` | ~1 мин | 430 | 📗 Быстро |
| `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` | ~1 мин | 339 | 📗 Быстро |
| `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | ~1 мин | 430 | 📗 Быстро |
| `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` | ~1 мин | 424 | 📗 Быстро |
| `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` | ~1 мин | 343 | 📗 Быстро |
| `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` | ~1 мин | 298 | 📗 Быстро |
| `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` | ~1 мин | 431 | 📗 Быстро |
| `docs/02-anthropic-vacancies/325-аннотация.md` | ~1 мин | 364 | 📗 Быстро |
| `docs/02-anthropic-vacancies/57-native-format.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/03-technology-combinations/03-local-first.md` | ~1 мин | 375 | 📗 Быстро |
| `docs/05-habr-projects/memory/ngt-memory.md` | ~1 мин | 369 | 📗 Быстро |
| `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` | ~1 мин | 355 | 📗 Быстро |
| `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | ~1 мин | 346 | 📗 Быстро |
| `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` | ~1 мин | 390 | 📗 Быстро |
| `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` | ~1 мин | 384 | 📗 Быстро |
| `docs/02-anthropic-vacancies/210-abstract.md` | ~1 мин | 405 | 📗 Быстро |
| `docs/02-anthropic-vacancies/230-аннотация.md` | ~1 мин | 348 | 📗 Быстро |
| `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | ~1 мин | 335 | 📗 Быстро |
| `docs/02-anthropic-vacancies/252-abstract.md` | ~1 мин | 398 | 📗 Быстро |
| `docs/02-anthropic-vacancies/275-why-this-document-exists.md` | ~1 мин | 406 | 📗 Быстро |
| `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` | ~1 мин | 388 | 📗 Быстро |
| `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` | ~1 мин | 328 | 📗 Быстро |
| `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` | ~1 мин | 335 | 📗 Быстро |
| `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` | ~1 мин | 385 | 📗 Быстро |
| `docs/02-anthropic-vacancies/307-abstract.md` | ~1 мин | 407 | 📗 Быстро |
| `docs/02-anthropic-vacancies/77-2-terminology.md` | ~1 мин | 363 | 📗 Быстро |
| `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` | ~1 мин | 207 | 📗 Быстро |
| `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` | ~1 мин | 224 | 📗 Быстро |
| `docs/02-anthropic-vacancies/123-portal-mcp-py.md` | ~1 мин | 232 | 📗 Быстро |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | ~1 мин | 233 | 📗 Быстро |
| `docs/02-anthropic-vacancies/146-acknowledgments.md` | ~1 мин | 381 | 📗 Быстро |
| `docs/02-anthropic-vacancies/168-abstract.md` | ~1 мин | 379 | 📗 Быстро |
| `docs/02-anthropic-vacancies/225-references.md` | ~1 мин | 358 | 📗 Быстро |
| `docs/02-anthropic-vacancies/245-ссылки.md` | ~1 мин | 327 | 📗 Быстро |
| `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` | ~1 мин | 244 | 📗 Быстро |
| `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` | ~1 мин | 360 | 📗 Быстро |
| `docs/02-anthropic-vacancies/287-references.md` | ~1 мин | 373 | 📗 Быстро |
| `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` | ~1 мин | 309 | 📗 Быстро |
| `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` | ~1 мин | 311 | 📗 Быстро |
| `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` | ~1 мин | 314 | 📗 Быстро |
| `docs/02-anthropic-vacancies/90-15-security-considerations.md` | ~1 мин | 351 | 📗 Быстро |
| `docs/BROKEN_LINKS.md` | ~1 мин | 317 | 📗 Быстро |
| `docs/COMPONENT_MATRIX.md` | ~1 мин | 332 | 📗 Быстро |
| `docs/PRIORITIES.md` | ~1 мин | 360 | 📗 Быстро |
| `docs/02-anthropic-vacancies/147-references.md` | ~1 мин | 352 | 📗 Быстро |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | ~1 мин | 343 | 📗 Быстро |
| `docs/02-anthropic-vacancies/183-references.md` | ~1 мин | 351 | 📗 Быстро |
| `docs/02-anthropic-vacancies/204-ссылки.md` | ~1 мин | 297 | 📗 Быстро |
| `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` | ~1 мин | 292 | 📗 Быстро |
| `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` | ~1 мин | 278 | 📗 Быстро |
| `docs/02-anthropic-vacancies/267-acknowledgments.md` | ~1 мин | 353 | 📗 Быстро |
| `docs/02-anthropic-vacancies/285-closing.md` | ~1 мин | 354 | 📗 Быстро |
| `docs/02-anthropic-vacancies/286-acknowledgments.md` | ~1 мин | 342 | 📗 Быстро |
| `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` | ~1 мин | 310 | 📗 Быстро |
| `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` | ~1 мин | 284 | 📗 Быстро |
| `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` | ~1 мин | 210 | 📗 Быстро |
| `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | ~1 мин | 309 | 📗 Быстро |
| `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` | ~1 мин | 349 | 📗 Быстро |
| `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` | ~1 мин | 326 | 📗 Быстро |
| `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` | ~1 мин | 205 | 📗 Быстро |
| `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/GRAPH.md` | ~1 мин | 100 | 📗 Быстро |
| `docs/REPORT.md` | ~1 мин | 189 | 📗 Быстро |
| `docs/02-anthropic-vacancies/07-2-terminology.md` | ~1 мин | 302 | 📗 Быстро |
| `docs/02-anthropic-vacancies/111-4-условия-применимости.md` | ~1 мин | 275 | 📗 Быстро |
| `docs/02-anthropic-vacancies/181-12-closing.md` | ~1 мин | 321 | 📗 Быстро |
| `docs/02-anthropic-vacancies/182-acknowledgments.md` | ~1 мин | 312 | 📗 Быстро |
| `docs/02-anthropic-vacancies/189-аннотация.md` | ~1 мин | 275 | 📗 Быстро |
| `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` | ~1 мин | 184 | 📗 Быстро |
| `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` | ~1 мин | 312 | 📗 Быстро |
| `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` | ~1 мин | 199 | 📗 Быстро |
| `docs/02-anthropic-vacancies/224-acknowledgments.md` | ~1 мин | 312 | 📗 Быстро |
| `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` | ~1 мин | 320 | 📗 Быстро |
| `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | ~1 мин | 329 | 📗 Быстро |
| `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` | ~1 мин | 312 | 📗 Быстро |
| `docs/02-anthropic-vacancies/300-заключение.md` | ~1 мин | 283 | 📗 Быстро |
| `docs/02-anthropic-vacancies/301-благодарности.md` | ~1 мин | 281 | 📗 Быстро |
| `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` | ~1 мин | 281 | 📗 Быстро |
| `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` | ~1 мин | 315 | 📗 Быстро |
| `docs/02-anthropic-vacancies/92-17-versioning-policy.md` | ~1 мин | 306 | 📗 Быстро |
| `docs/02-anthropic-vacancies/QA.md` | ~1 мин | 284 | 📗 Быстро |
| `docs/CONCEPT_GRAPH.md` | ~1 мин | 196 | 📗 Быстро |
| `docs/FOOTNOTES.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/MINDMAP.md` | ~1 мин | 70 | 📗 Быстро |
| `docs/VOCABULARY.md` | ~1 мин | 262 | 📗 Быстро |
| `docs/contacts/anastasiyaw.md` | ~1 мин | 190 | 📗 Быстро |
| `docs/contacts/andrey-chuyan.md` | ~1 мин | 176 | 📗 Быстро |
| `docs/contacts/antipozitive.md` | ~1 мин | 174 | 📗 Быстро |
| `docs/contacts/kksudo.md` | ~1 мин | 178 | 📗 Быстро |
| `docs/contacts/spbmolot.md` | ~1 мин | 180 | 📗 Быстро |
| `docs/contacts/vitalyoborin.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/templates/ensemble.md` | ~1 мин | 59 | 📗 Быстро |
| `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` | ~1 мин | 268 | 📗 Быстро |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | ~1 мин | 290 | 📗 Быстро |
| `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` | ~1 мин | 286 | 📗 Быстро |
| `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` | ~1 мин | 287 | 📗 Быстро |
| `docs/02-anthropic-vacancies/211-table-of-contents.md` | ~1 мин | 286 | 📗 Быстро |
| `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` | ~1 мин | 265 | 📗 Быстро |
| `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` | ~1 мин | 286 | 📗 Быстро |
| `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | ~1 мин | 296 | 📗 Быстро |
| `docs/02-anthropic-vacancies/345-кто-ты.md` | ~1 мин | 269 | 📗 Быстро |
| `docs/02-anthropic-vacancies/47-native-format.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` | ~1 мин | 287 | 📗 Быстро |
| `docs/02-anthropic-vacancies/74-abstract.md` | ~1 мин | 278 | 📗 Быстро |
| `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` | ~1 мин | 284 | 📗 Быстро |
| `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` | ~1 мин | 281 | 📗 Быстро |
| `docs/05-habr-projects/02-collaboration-partners.md` | ~1 мин | 254 | 📗 Быстро |
| `docs/05-habr-projects/knowledge/wikontic.md` | ~1 мин | 256 | 📗 Быстро |
| `docs/05-habr-projects/memory/yodoca.md` | ~1 мин | 256 | 📗 Быстро |
| `docs/CONTACTS.md` | ~1 мин | 151 | 📗 Быстро |
| `docs/CONTACT_PRIORITY.md` | ~1 мин | 150 | 📗 Быстро |
| `docs/PROGRESS.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/contacts/cutcode.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/contacts/dmitriila.md` | ~1 мин | 159 | 📗 Быстро |
| `docs/contacts/mixaill76.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/contacts/nlaik.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/contacts/sonia-black.md` | ~1 мин | 169 | 📗 Быстро |
| `docs/contacts/tagir-analyzes.md` | ~1 мин | 167 | 📗 Быстро |
| `docs/contacts/vladspace.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/contacts/zodigancode.md` | ~1 мин | 159 | 📗 Быстро |
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | ~1 мин | 259 | 📗 Быстро |
| `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | ~1 мин | 275 | 📗 Быстро |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | ~1 мин | 274 | 📗 Быстро |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | ~1 мин | 255 | 📗 Быстро |
| `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` | ~1 мин | 243 | 📗 Быстро |
| `docs/02-anthropic-vacancies/23-11-security-considerations.md` | ~1 мин | 246 | 📗 Быстро |
| `docs/02-anthropic-vacancies/24-12-versioning-policy.md` | ~1 мин | 261 | 📗 Быстро |
| `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` | ~1 мин | 227 | 📗 Быстро |
| `docs/02-anthropic-vacancies/302-ссылки.md` | ~1 мин | 242 | 📗 Быстро |
| `docs/02-anthropic-vacancies/308-table-of-contents.md` | ~1 мин | 268 | 📗 Быстро |
| `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` | ~1 мин | 261 | 📗 Быстро |
| `docs/02-anthropic-vacancies/356-твой-workflow.md` | ~1 мин | 252 | 📗 Быстро |
| `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` | ~1 мин | 242 | 📗 Быстро |
| `docs/02-anthropic-vacancies/85-10-query-flow.md` | ~1 мин | 265 | 📗 Быстро |
| `docs/03-technology-combinations/01-agent-routing.md` | ~1 мин | 244 | 📗 Быстро |
| `docs/COST.md` | ~1 мин | 234 | 📗 Быстро |
| `docs/HEATMAP.md` | ~1 мин | 122 | 📗 Быстро |
| `docs/STALENESS.md` | ~1 мин | 122 | 📗 Быстро |
| `docs/01-svyazi/QA.md` | ~1 мин | 203 | 📗 Быстро |
| `docs/01-svyazi/README.md` | ~1 мин | 96 | 📗 Быстро |
| `docs/02-anthropic-vacancies/04-abstract.md` | ~1 мин | 222 | 📗 Быстро |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | ~1 мин | 206 | 📗 Быстро |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | ~1 мин | 103 | 📗 Быстро |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | ~1 мин | 88 | 📗 Быстро |
| `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` | ~1 мин | 244 | 📗 Быстро |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | ~1 мин | 200 | 📗 Быстро |
| `docs/02-anthropic-vacancies/106-tl-dr.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | ~1 мин | 181 | 📗 Быстро |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/02-anthropic-vacancies/12-content-overview.md` | ~1 мин | 175 | 📗 Быстро |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | ~1 мин | 114 | 📗 Быстро |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | ~1 мин | 95 | 📗 Быстро |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | ~1 мин | 219 | 📗 Быстро |
| `docs/02-anthropic-vacancies/128-доступные-инструменты.md` | ~1 мин | 235 | 📗 Быстро |
| `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` | ~1 мин | 219 | 📗 Быстро |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | ~1 мин | 185 | 📗 Быстро |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | ~1 мин | 144 | 📗 Быстро |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | ~1 мин | 247 | 📗 Быстро |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | ~1 мин | 247 | 📗 Быстро |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | ~1 мин | 178 | 📗 Быстро |
| `docs/02-anthropic-vacancies/16-history.md` | ~1 мин | 78 | 📗 Быстро |
| `docs/02-anthropic-vacancies/169-table-of-contents.md` | ~1 мин | 216 | 📗 Быстро |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | ~1 мин | 145 | 📗 Быстро |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | ~1 мин | 250 | 📗 Быстро |
| `docs/02-anthropic-vacancies/190-содержание.md` | ~1 мин | 182 | 📗 Быстро |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | ~1 мин | 208 | 📗 Быстро |
| `docs/02-anthropic-vacancies/203-благодарности.md` | ~1 мин | 179 | 📗 Быстро |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | ~1 мин | 154 | 📗 Быстро |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | ~1 мин | 256 | 📗 Быстро |
| `docs/02-anthropic-vacancies/21-9-query-flow.md` | ~1 мин | 237 | 📗 Быстро |
| `docs/02-anthropic-vacancies/231-содержание.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/02-anthropic-vacancies/244-благодарности.md` | ~1 мин | 220 | 📗 Быстро |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | ~1 мин | 249 | 📗 Быстро |
| `docs/02-anthropic-vacancies/25-13-reference-implementation.md` | ~1 мин | 189 | 📗 Быстро |
| `docs/02-anthropic-vacancies/253-table-of-contents.md` | ~1 мин | 246 | 📗 Быстро |
| `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` | ~1 мин | 206 | 📗 Быстро |
| `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` | ~1 мин | 251 | 📗 Быстро |
| `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` | ~1 мин | 249 | 📗 Быстро |
| `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | ~1 мин | 221 | 📗 Быстро |
| `docs/02-anthropic-vacancies/31-content-overview.md` | ~1 мин | 183 | 📗 Быстро |
| `docs/02-anthropic-vacancies/320-references.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/02-anthropic-vacancies/326-содержание.md` | ~1 мин | 204 | 📗 Быстро |
| `docs/02-anthropic-vacancies/338-ссылки.md` | ~1 мин | 229 | 📗 Быстро |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | ~1 мин | 94 | 📗 Быстро |
| `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | ~1 мин | 130 | 📗 Быстро |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | ~1 мин | 245 | 📗 Быстро |
| `docs/02-anthropic-vacancies/346-твоё-происхождение.md` | ~1 мин | 133 | 📗 Быстро |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | ~1 мин | 151 | 📗 Быстро |
| `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` | ~1 мин | 100 | 📗 Быстро |
| `docs/02-anthropic-vacancies/349-твоя-личность.md` | ~1 мин | 223 | 📗 Быстро |
| `docs/02-anthropic-vacancies/35-passports-info1-md.md` | ~1 мин | 188 | 📗 Быстро |
| `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` | ~1 мин | 136 | 📗 Быстро |
| `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` | ~1 мин | 219 | 📗 Быстро |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | ~1 мин | 193 | 📗 Быстро |
| `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` | ~1 мин | 220 | 📗 Быстро |
| `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/02-anthropic-vacancies/36-essence.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | ~1 мин | 119 | 📗 Быстро |
| `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` | ~1 мин | 115 | 📗 Быстро |
| `docs/02-anthropic-vacancies/37-native-format.md` | ~1 мин | 216 | 📗 Быстро |
| `docs/02-anthropic-vacancies/38-content-overview.md` | ~1 мин | 137 | 📗 Быстро |
| `docs/02-anthropic-vacancies/39-angle-perspective.md` | ~1 мин | 193 | 📗 Быстро |
| `docs/02-anthropic-vacancies/40-bridges.md` | ~1 мин | 215 | 📗 Быстро |
| `docs/02-anthropic-vacancies/41-compatibility-level.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/02-anthropic-vacancies/42-author-contact.md` | ~1 мин | 191 | 📗 Быстро |
| `docs/02-anthropic-vacancies/43-history.md` | ~1 мин | 178 | 📗 Быстро |
| `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` | ~1 мин | 223 | 📗 Быстро |
| `docs/02-anthropic-vacancies/45-passports-pro2-md.md` | ~1 мин | 186 | 📗 Быстро |
| `docs/02-anthropic-vacancies/46-essence.md` | ~1 мин | 206 | 📗 Быстро |
| `docs/02-anthropic-vacancies/48-content-overview.md` | ~1 мин | 223 | 📗 Быстро |
| `docs/02-anthropic-vacancies/49-angle-perspective.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/02-anthropic-vacancies/50-bridges.md` | ~1 мин | 205 | 📗 Быстро |
| `docs/02-anthropic-vacancies/51-compatibility-level.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/02-anthropic-vacancies/52-author-contact.md` | ~1 мин | 241 | 📗 Быстро |
| `docs/02-anthropic-vacancies/53-history.md` | ~1 мин | 210 | 📗 Быстро |
| `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` | ~1 мин | 240 | 📗 Быстро |
| `docs/02-anthropic-vacancies/55-passports-meta-md.md` | ~1 мин | 186 | 📗 Быстро |
| `docs/02-anthropic-vacancies/56-essence.md` | ~1 мин | 228 | 📗 Быстро |
| `docs/02-anthropic-vacancies/58-content-overview.md` | ~1 мин | 103 | 📗 Быстро |
| `docs/02-anthropic-vacancies/59-angle-perspective.md` | ~1 мин | 205 | 📗 Быстро |
| `docs/02-anthropic-vacancies/60-bridges.md` | ~1 мин | 191 | 📗 Быстро |
| `docs/02-anthropic-vacancies/61-compatibility-level.md` | ~1 мин | 159 | 📗 Быстро |
| `docs/02-anthropic-vacancies/62-author-contact.md` | ~1 мин | 181 | 📗 Быстро |
| `docs/02-anthropic-vacancies/63-history.md` | ~1 мин | 199 | 📗 Быстро |
| `docs/02-anthropic-vacancies/65-readme-md.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` | ~1 мин | 194 | 📗 Быстро |
| `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` | ~1 мин | 218 | 📗 Быстро |
| `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` | ~1 мин | 218 | 📗 Быстро |
| `docs/02-anthropic-vacancies/93-18-reference-implementation.md` | ~1 мин | 230 | 📗 Быстро |
| `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | ~1 мин | 236 | 📗 Быстро |
| `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` | ~1 мин | 242 | 📗 Быстро |
| `docs/03-technology-combinations/04-sozialrecht-domain.md` | ~1 мин | 185 | 📗 Быстро |
| `docs/03-technology-combinations/QA.md` | ~1 мин | 84 | 📗 Быстро |
| `docs/04-ai-collaborations/QA.md` | ~1 мин | 206 | 📗 Быстро |
| `docs/04-ai-collaborations/README.md` | ~1 мин | 165 | 📗 Быстро |
| `docs/05-habr-projects/01-synthesis.md` | ~1 мин | 177 | 📗 Быстро |
| `docs/05-habr-projects/QA.md` | ~1 мин | 94 | 📗 Быстро |
| `docs/AUTHORS.md` | ~1 мин | 67 | 📗 Быстро |
| `docs/AUTOFILLED.md` | ~1 мин | 141 | 📗 Быстро |
| `docs/CITATION_INDEX.md` | ~1 мин | 56 | 📗 Быстро |
| `docs/COMPARE.md` | ~1 мин | 62 | 📗 Быстро |
| `docs/COMPLEXITY.md` | ~1 мин | 118 | 📗 Быстро |
| `docs/CONSISTENCY.md` | ~1 мин | 81 | 📗 Быстро |
| `docs/CONTENT_GAPS.md` | ~1 мин | 152 | 📗 Быстро |
| `docs/CROSSREFS.md` | ~1 мин | 241 | 📗 Быстро |
| `docs/DENSITY.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/DEPENDENCY_MAP.md` | ~1 мин | 99 | 📗 Быстро |
| `docs/DIGEST.md` | ~1 мин | 228 | 📗 Быстро |
| `docs/DUPLICATES.md` | ~1 мин | 71 | 📗 Быстро |
| `docs/ENTITIES.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/GLOSSARY.md` | ~1 мин | 79 | 📗 Быстро |
| `docs/HEALTH.md` | ~1 мин | 60 | 📗 Быстро |
| `docs/KEYWORD_INDEX.md` | ~1 мин | 184 | 📗 Быстро |
| `docs/LLM_SUMMARIES.md` | ~1 мин | 227 | 📗 Быстро |
| `docs/METRICS.md` | ~1 мин | 138 | 📗 Быстро |
| `docs/MISSING.md` | ~1 мин | 116 | 📗 Быстро |
| `docs/NETWORK.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/ORPHANS.md` | ~1 мин | 73 | 📗 Быстро |
| `docs/SCHEDULE.md` | ~1 мин | 91 | 📗 Быстро |
| `docs/SCORING.md` | ~1 мин | 126 | 📗 Быстро |
| `docs/SEE_ALSO.md` | ~1 мин | 72 | 📗 Быстро |
| `docs/SENTIMENT.md` | ~1 мин | 110 | 📗 Быстро |
| `docs/SIMILAR.md` | ~1 мин | 138 | 📗 Быстро |
| `docs/SOURCE_MAP.md` | ~1 мин | 164 | 📗 Быстро |
| `docs/STATS.md` | ~1 мин | 62 | 📗 Быстро |
| `docs/TAGS.md` | ~1 мин | 65 | 📗 Быстро |
| `docs/VALIDATION.md` | ~1 мин | 166 | 📗 Быстро |
| `docs/VERSION_DIFF.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/WORD_CLOUD.md` | ~1 мин | 158 | 📗 Быстро |
| `docs/autofilled/components/.md` | ~1 мин | 95 | 📗 Быстро |
| `docs/autofilled/components/README.md` | ~1 мин | 51 | 📗 Быстро |
| `docs/autofilled/components/cowork.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/ingit.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/kksudo.md` | ~1 мин | 68 | 📗 Быстро |
| `docs/autofilled/components/lorenzo.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/nautilus.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/sgb.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/spbmolot.md` | ~1 мин | 68 | 📗 Быстро |
| `docs/autofilled/components/svend4.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/components/svyazi.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/autofilled/research-summary.md` | ~1 мин | 89 | 📗 Быстро |
| `docs/contacts/README.md` | ~1 мин | 65 | 📗 Быстро |
| `docs/templates/README.md` | ~1 мин | 70 | 📗 Быстро |
| `docs/templates/contact-outreach.md` | ~1 мин | 59 | 📗 Быстро |
| `docs/templates/project-component.md` | ~1 мин | 77 | 📗 Быстро |
| `docs/templates/research-note.md` | ~1 мин | 51 | 📗 Быстро |


### 94. Общая картина
_Файл: `docs/REPORT.md` | 2 колонок, 9 строк_

| Показатель | Значение |
|------------|---------|
| Всего документов | **529** |
| Всего слов | **523,639** |
| Скриптов обработки | **125** |
| Индекс здоровья | **90/100** |
| Проектов в сети | **22** |
| Связей проектов | **189** |
| Кластеров документов | **120** |
| Ошибок валидации | **0** |
| Предупреждений | **17** |


### 95. Структура репозитория
_Файл: `docs/REPORT.md` | 3 колонок, 5 строк_

| Раздел | Файлов | Описание |
|--------|--------|---------|
| `01-svyazi` | 16 | Архитектура Svyazi 2.0 |
| `02-anthropic-vacancies` | 357 | 436 вакансий Anthropic |
| `03-technology-combinations` | 7 | 40+ комбинаций технологий |
| `04-ai-collaborations` | 17 | AI-ансамбли OSS-проектов |
| `05-habr-projects` | 10 | Хабр-проекты: память, граф |


### 96. Топ навигационных документов
_Файл: `docs/REPORT.md` | 2 колонок, 7 строк_

| Документ | Назначение |
|----------|------------|
| [READING_ORDER.md](READING_ORDER.md) | С чего начать читать |
| [SITEMAP.md](SITEMAP.md) | Карта всех разделов |
| [NARRATIVE.md](NARRATIVE.md) | История проекта |
| [DECISIONS.md](DECISIONS.md) | Ключевые решения |
| [CONTACTS.md](CONTACTS.md) | С кем связаться |
| [HEALTH.md](HEALTH.md) | Состояние репо |
| [VALIDATION.md](VALIDATION.md) | Проверка структуры |


### 97. Реестр
_Файл: `docs/RISK_REGISTER.md` | 7 колонок, 10 строк_

| # | Риск | Категория | Вероятн. | Влияние | Score | Уровень |
|---|------|-----------|----------|---------|-------|---------|
| 1 | Одиночный разработчик — bus factor 1 | Команда | 4 (Высока) | 5 (Критич) | **20** | 🔴 КРИТИЧЕСКИЙ |
| 2 | Авторы компонентов не ответят на запросы | Команда | 3 (Средня) | 5 (Критич) | **15** | 🟠 ВЫСОКИЙ |
| 3 | PII-утечки через MCP-инструменты | Безопасность | 3 (Средня) | 5 (Критич) | **15** | 🟠 ВЫСОКИЙ |
| 4 | Лицензия BSL 1.1 (NGT) ограничит коммерческое испо | Правовой | 3 (Средня) | 4 (Большо) | **12** | 🟠 ВЫСОКИЙ |
| 5 | Высокая стоимость Claude API при масштабировании | Финансовый | 4 (Высока) | 3 (Средне) | **12** | 🟠 ВЫСОКИЙ |
| 6 | Устаревание документации при быстром развитии комп | Качество | 4 (Высока) | 3 (Средне) | **12** | 🟠 ВЫСОКИЙ |
| 7 | AgentFS не поддерживает concurrent multi-agent дос | Технический | 3 (Средня) | 4 (Большо) | **12** | 🟠 ВЫСОКИЙ |
| 8 | Прототип Knowledge OS займёт дольше запланированно | Сроки | 3 (Средня) | 3 (Средне) | **9** | 🟠 ВЫСОКИЙ |
| 9 | Зависимость от закрытого API Anthropic | Технический | 2 (Низкая) | 4 (Большо) | **8** | 🟡 СРЕДНИЙ |
| 10 | Конкурирующие OSS-проекты могут обогнать | Рынок | 2 (Низкая) | 3 (Средне) | **6** | 🟡 СРЕДНИЙ |


### 98. Упоминания рисков в документах
_Файл: `docs/RISK_REGISTER.md` | 2 колонок, 11 строк_

| Источник | Фрагмент |
|----------|---------|
| `01-executive-summary` | [^sentinel]: OSS-проект: безопасность и allowlist для MCP [^rufler]: OSS-проект: оркестратор AI-аген… |
| `02-methodology` | иде улучшают доказуемость, безопасность, локальность или стоимость выполнения Когда у статьи не было… |
| `03-component-catalog` | w1turn20view18 | Рантайм‑безопасность и бюджетный execution plane для агентных систем. | SENTINEL[… |
| `04-ensembles-overview` | ри минимальном интеграционном риске**. **Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[… |
| `04-ensembles-overview` | а**: Self‑Aware MCP закрывает проблемы часового пояса, ОС, даты и локации. citeturn20view12turn30… |
| `06-security-privacy` | t, collaboration --> ## Безопасность, приватность и бюджетный роутинг Для Svyazi‑2.0 безопасная архи… |
| `06-security-privacy` | Похожие документы:** - [06-безопасность-приватность-и-бюджетный-роутинг](04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) (сходство 1.00) - [05-пл… |
| `06-security-privacy` | **Смотрите также:** - [06-безопасность-приватность-и-бюджетный-роутинг](docs/04-ai-collaborations/06… |
| `07-mvp-planning` | l Search + базовые правила безопасности | Удержать стоимость и не утонуть в MCP[^mcp]/context overhe… |
| `07-mvp-planning` | review для inferred | Снизить риск ложных связей и утечек | 1–2 дня | **Итого**: реалистичный MVP — … |
| `07-mvp-planning` | нных компонентов. **Ключевые риски и как их закрывать** | Риск | Почему это важно | Снижение риска |… |


### 99. Итоговая статистика
_Файл: `docs/RISK_REGISTER.md` | 2 колонок, 3 строк_

| Уровень | Кол-во |
|---------|--------|
| 🔴 КРИТИЧЕСКИЙ | 1 |
| 🟠 ВЫСОКИЙ | 7 |
| 🟡 СРЕДНИЙ | 2 |


### 100. Ключевые вехи
_Файл: `docs/SCHEDULE.md` | 3 колонок, 10 строк_

| Срок | Веха | Статус |
|------|------|--------|
| **2024-Q4** | ✅ Исследование компонентов завершено | ✅ Выполнено |
| **2024-Q4** | ✅ Архитектура Svyazi 2.0 задокументирована | ✅ Выполнено |
| **2025-Q1** | ✅ Интеграционные контракты описаны | ✅ Выполнено |
| **2025-Q1** | ⬜ Написать авторам AgentFS, Yodoca, NGT | ⬜ Планируется |
| **2025-Q2** | ⬜ Получить согласие на сотрудничество | ⬜ Планируется |
| **2025-Q2** | ⬜ Создать рабочее окружение Knowledge OS | ⬜ Планируется |
| **2025-Q3** | ⬜ Прототип ансамбля (Svyazi + CardIndex) | ⬜ Планируется |
| **2025-Q3** | ⬜ Тестирование на реальных данных | ⬜ Планируется |
| **2025-Q4** | ⬜ Интеграция SENTINEL + MCP Tool Search | ⬜ Планируется |
| **2026-Q1** | ⬜ Публичный MVP-релиз на GitHub | ⬜ Планируется |


### 101. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 6 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Executive Summary существует | ✅ | 10 |
| Архитектурные контракты описаны | ✅ | 10 |
| MVP план задокументирован | ✅ | 10 |
| Дорожная карта есть | ✅ | 8 |
| README в каждом разделе | ✅ | 5 |
| Глоссарий создан | ✅ | 5 |


### 102. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 5 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Компоненты каталогизированы (20+) | ✅ | 10 |
| Ансамбли определены (5+) | ✅ | 10 |
| Архитектурные пробелы выявлены | ✅ | 8 |
| Безопасность и PII описаны | ✅ | 8 |
| Граф связей проектов построен | ✅ | 5 |


### 103. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 3 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Контакты авторов компонентов есть | ✅ | 10 |
| Авторы Habr-проектов найдены | ✅ | 8 |
| Шаблоны для связи созданы | ✅ | 5 |


### 104. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 6 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Риски выявлены и задокументированы | ✅ | 8 |
| Лицензии проверены | ✅ | 8 |
| Сломанных ссылок < 30 | ❌ | 5 |
|  ↳ _Слишком много сломанных ссылок_ | | |
| Дублей нет | ❌ | 5 |
|  ↳ _Есть точные дубли документов_ | | |


### 105. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 4 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Прогресс MVP отслеживается | ✅ | 8 |
| Action items задокументированы | ✅ | 8 |
| Порядок чтения задан | ✅ | 5 |
| Executive report создан | ✅ | 5 |


### 106. Тональность по разделам
_Файл: `docs/SENTIMENT.md` | 6 колонок, 10 строк_

| Раздел | Оптимизм | Скептицизм | Срочность | Неопределённость | Тон |
|--------|----------|------------|-----------|-----------------|-----|
| **01-svyazi** | 2.4‰ | 7.1‰ | 5.3‰ | 0.5‰ | 🔴 скептичный |
| **02-anthropic-vacancies** | 1.6‰ | 5.6‰ | 1.8‰ | 1.5‰ | 🔴 скептичный |
| **03-technology-combinations** | 4.3‰ | 1.2‰ | 2.3‰ | 0.4‰ | 🟢 оптимистичный |
| **04-ai-collaborations** | 2.3‰ | 5.1‰ | 2.1‰ | 0.8‰ | 🔴 скептичный |
| **05-habr-projects** | 4.6‰ | 1.9‰ | 0.9‰ | 1.3‰ | 🟢 оптимистичный |
| **autofilled** | 0.0‰ | 0.0‰ | 0.0‰ | 0.0‰ | ⚪ нейтральный |
| **contacts** | 0.0‰ | 0.0‰ | 1.0‰ | 0.0‰ | 🟠 срочный |
| **obsidian** | 1.3‰ | 9.2‰ | 1.7‰ | 1.1‰ | 🔴 скептичный |
| **root** | 0.5‰ | 14.6‰ | 1.3‰ | 0.7‰ | 🔴 скептичный |
| **templates** | 0.0‰ | 12.9‰ | 0.0‰ | 0.0‰ | 🔴 скептичный |


### 107. Самые оптимистичные документы
_Файл: `docs/SENTIMENT.md` | 3 колонок, 10 строк_

| Документ | Оптимизм‰ | Тон |
|----------|----------|-----|
| `110-вопрос-fallback-ratio-как-крити` | 16.3 | 🟠 срочный |
| `193-3-что-делает-агента-представите` | 16.0 | 🟢 оптимистичный |
| `193-3-что-делает-агента-представите` | 15.5 | 🟢 оптимистичный |
| `110-вопрос-fallback-ratio-как-крити` | 15.1 | 🟠 срочный |
| `240-9-связь-с-другими-типами-агенто` | 13.3 | ⚪ нейтральный |
| `123-portal-mcp-py` | 13.2 | 🟢 оптимистичный |
| `02-collaboration-partners` | 13.2 | 🟢 оптимистичный |
| `yodoca` | 13.2 | 🟢 оптимистичный |
| `240-9-связь-с-другими-типами-агенто` | 13.0 | ⚪ нейтральный |
| `248-приложение-c-архитектура-быстро` | 12.9 | 🟢 оптимистичный |


### 108. Самые скептичные / риск-ориентированные
_Файл: `docs/SENTIMENT.md` | 3 колонок, 10 строк_

| Документ | Скептицизм‰ | Тон |
|----------|------------|-----|
| `PARAGRAPH_QUALITY` | 244.6 | 🔴 скептичный |
| `PARAGRAPH_QUALITY` | 244.2 | 🔴 скептичный |
| `198-8-риски-и-меры-противодействия` | 88.3 | 🔴 скептичный |
| `198-8-риски-и-меры-противодействия` | 86.0 | 🔴 скептичный |
| `177-8-risks-and-mitigations` | 84.1 | 🔴 скептичный |
| `177-8-risks-and-mitigations` | 81.1 | 🔴 скептичный |
| `162-8-risk-analysis` | 50.7 | 🔴 скептичный |
| `162-8-risk-analysis` | 50.5 | 🔴 скептичный |
| `263-10-risks-specific-to-composite-` | 43.6 | 🔴 скептичный |
| `263-10-risks-specific-to-composite-` | 43.1 | 🔴 скептичный |


### 109. Распределение тональности
_Файл: `docs/SENTIMENT.md` | 2 колонок, 5 строк_

| Тон | Файлов |
|-----|--------|
| 🔴 скептичный | 463 |
| ⚪ нейтральный | 330 |
| 🟠 срочный | 103 |
| 🟢 оптимистичный | 63 |
| 🟡 неопределённый | 28 |


### 110. Топ-20 самых похожих пар
_Файл: `docs/SIMILAR.md` | 3 колонок, 20 строк_

| Сходство | Файл A | Файл B |
|----------|--------|--------|
| 1.000 | `13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | `13-contacts.md` |
| 1.000 | `12-дорожная-карта-прототипа-следующей-итерации.md` | `12-roadmap.md` |
| 1.000 | `11-интеграционный-контракт-который-стоит-зафиксироват.md` | `11-integration-contracts.md` |
| 1.000 | `09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | `09-architectural-gaps.md` |
| 1.000 | `06-безопасность-приватность-и-бюджетный-роутинг.md` | `06-security-privacy.md` |
| 1.000 | `05-план-прототипа-и-возможные-контакты.md` | `07-mvp-planning.md` |
| 0.994 | `03-карта-найденных-проектов-и-паттернов.md` | `03-component-catalog.md` |
| 0.952 | `07-выводы.md` | `08-conclusions.md` |
| 0.922 | `10-новые-ансамбли-следующего-шага.md` | `10-second-order-ensembles.md` |
| 0.916 | `04-приоритетные-ансамбли.md` | `04-ensembles-overview.md` |
| 0.889 | `94-19-adr-001-federation-over-merging.md` | `26-14-adr-001-federation-over-merging.md` |
| 0.859 | `SEARCH.md` | `READING_ORDER.md` |
| 0.858 | `QA.md` | `QA.md` |
| 0.818 | `QA.md` | `QA.md` |
| 0.739 | `02-методика-и-рамка-отбора.md` | `02-methodology.md` |
| 0.720 | `85-10-query-flow.md` | `21-9-query-flow.md` |
| 0.702 | `251-ai-support-through-configurable-specialist-ensembl.md` | `209-a-typology-of-ai-agents-on-the-principal-side-and-.md` |
| 0.680 | `01-executive-summary.md` | `01-executive-summary.md` |
| 0.673 | `README.md` | `README.md` |
| 0.667 | `61-compatibility-level.md` | `51-compatibility-level.md` |


### 111. Мета-документы
_Файл: `docs/SITEMAP.md` | 3 колонок, 153 строк_

| Документ | Описание | Слов |
|----------|----------|------|
| [ABBREVIATIONS.md](ABBREVIATIONS.md) | — | 1415 |
| [ACTION_ITEMS.md](ACTION_ITEMS.md) | Задачи и риски (490) | 6656 |
| [ACTION_ITEMS.md](ACTION_ITEMS.md) | Задачи и риски (490) | 6669 |
| [ALERTS.md](ALERTS.md) | — | 79 |
| [AUTHORS.md](AUTHORS.md) | Авторы и контакты | 158 |
| [AUTHORS.md](AUTHORS.md) | Авторы и контакты | 169 |
| [AUTOFILLED.md](AUTOFILLED.md) | — | 115 |
| [BACKLINKS.md](BACKLINKS.md) | — | 339 |
| [BROKEN_LINKS.md](BROKEN_LINKS.md) | Сломанные ссылки (26) | 766 |
| [CHANGELOG.md](CHANGELOG.md) | История изменений | 945 |
| [CHANGELOG.md](CHANGELOG.md) | История изменений | 911 |
| [CHANGELOG_AUTO.md](CHANGELOG_AUTO.md) | — | 627 |
| [CITATION_INDEX.md](CITATION_INDEX.md) | — | 844 |
| [CLUSTERS.md](CLUSTERS.md) | Кластеры (384 → 120 групп) | 1612 |
| [CLUSTERS.md](CLUSTERS.md) | Кластеры (384 → 120 групп) | 1638 |
| [CODE_BLOCKS.md](CODE_BLOCKS.md) | — | 3658 |
| [CODE_BLOCKS.md](CODE_BLOCKS.md) | — | 3668 |
| [COMPARE.md](COMPARE.md) | Сравнение с предыдущим коммитом | 477 |
| [COMPARE.md](COMPARE.md) | Сравнение с предыдущим коммитом | 503 |
| [COMPLEXITY.md](COMPLEXITY.md) | Оценка читаемости | 605 |
| [COMPLEXITY.md](COMPLEXITY.md) | Оценка читаемости | 616 |
| [COMPONENT_MATRIX.md](COMPONENT_MATRIX.md) | — | 959 |
| [CONCEPTS.md](CONCEPTS.md) | Глоссарий понятий (888) | 11402 |
| [CONCEPTS.md](CONCEPTS.md) | Глоссарий понятий (888) | 11408 |
| [CONCEPT_GRAPH.md](CONCEPT_GRAPH.md) | — | 660 |
| [CONSISTENCY.md](CONSISTENCY.md) | — | 313 |
| [CONSISTENCY.md](CONSISTENCY.md) | — | 323 |
| [CONTACTS.md](CONTACTS.md) | Контакты (15 авторов) | 552 |
| [CONTACTS.md](CONTACTS.md) | Контакты (15 авторов) | 535 |
| [CONTACT_PRIORITY.md](CONTACT_PRIORITY.md) | — | 378 |
| [CONTENT_GAPS.md](CONTENT_GAPS.md) | — | 886 |
| [CONTRADICTIONS.md](CONTRADICTIONS.md) | — | 1223 |
| [COST.md](COST.md) | — | 599 |
| [COVERAGE.md](COVERAGE.md) | — | 303 |
| [CROSSREFS.md](CROSSREFS.md) | Перекрёстные ссылки проектов | 653 |
| [CROSSREFS.md](CROSSREFS.md) | Перекрёстные ссылки проектов | 663 |
| [DECISIONS.md](DECISIONS.md) | Ключевые решения (150) | 1911 |
| [DECISIONS.md](DECISIONS.md) | Ключевые решения (150) | 1925 |
| [DENSITY.md](DENSITY.md) | Карта плотности тем | 650 |
| [DENSITY.md](DENSITY.md) | Карта плотности тем | 661 |
| [DEPENDABOT.md](DEPENDABOT.md) | — | 136 |
| [DEPENDENCY_MAP.md](DEPENDENCY_MAP.md) | — | 1008 |
| [DIGEST.md](DIGEST.md) | — | 379 |
| [DIGEST_WEEKLY.md](DIGEST_WEEKLY.md) | — | 205 |
| [DUPLICATES.md](DUPLICATES.md) | — | 95 |
| [DUPLICATES.md](DUPLICATES.md) | — | 106 |
| [ENTITIES.md](ENTITIES.md) | Именованные сущности | 727 |
| [ENTITIES.md](ENTITIES.md) | Именованные сущности | 737 |
| [FAQ.md](FAQ.md) | — | 836 |
| [FOOTNOTES.md](FOOTNOTES.md) | — | 275 |
| [GITHUB_ISSUES.md](GITHUB_ISSUES.md) | — | 1703 |
| [GLOSSARY.md](GLOSSARY.md) | Глоссарий проектов (33 записи) | 202 |
| [GLOSSARY.md](GLOSSARY.md) | Глоссарий проектов (33 записи) | 212 |
| [GRAPH.md](GRAPH.md) | Граф связей проектов | 2662 |
| [GRAPH.md](GRAPH.md) | Граф связей проектов | 2673 |
| [HEALTH.md](HEALTH.md) | Дашборд здоровья (75/100) | 185 |
| [HEALTH.md](HEALTH.md) | Дашборд здоровья (75/100) | 202 |
| [HEATMAP.md](HEATMAP.md) | — | 537 |
| [INDEX.md](INDEX.md) | — | 528 |
| [KEYWORD_INDEX.md](KEYWORD_INDEX.md) | — | 1115 |
| [KPI.md](KPI.md) | Числовые KPI (737 показателей) | 2318 |
| [KPI.md](KPI.md) | Числовые KPI (737 показателей) | 2330 |
| [KPI_HISTORY.md](KPI_HISTORY.md) | — | 85 |
| [LINKS.md](LINKS.md) | Внешние ссылки | 969 |
| [LINKS.md](LINKS.md) | Внешние ссылки | 979 |
| [LLM_SUMMARIES.md](LLM_SUMMARIES.md) | — | 226 |
| [METRICS.md](METRICS.md) | — | 445 |
| [MINDMAP.md](MINDMAP.md) | Майндмап в Mermaid | 242 |
| [MINDMAP.md](MINDMAP.md) | Майндмап в Mermaid | 253 |
| [MISSING.md](MISSING.md) | Пробелы знаний | 434 |
| [MISSING.md](MISSING.md) | Пробелы знаний | 445 |
| [NAMED_ENTITIES.md](NAMED_ENTITIES.md) | — | 1413 |
| [NARRATIVE.md](NARRATIVE.md) | — | 1060 |
| [NETWORK.md](NETWORK.md) | — | 417 |
| [ONBOARDING.md](ONBOARDING.md) | — | 606 |
| [ORPHANS.md](ORPHANS.md) | — | 107 |
| [OUTLINE.md](OUTLINE.md) | — | 14242 |
| [PARAGRAPH_QUALITY.md](PARAGRAPH_QUALITY.md) | — | 4546 |
| [PRIORITIES.md](PRIORITIES.md) | Приоритеты (TF-IDF) | 1151 |
| [PRIORITIES.md](PRIORITIES.md) | Приоритеты (TF-IDF) | 1161 |
| [PROGRESS.md](PROGRESS.md) | — | 252 |
| [QA.md](QA.md) | Вопросы и ответы | 182 |
| [QA.md](QA.md) | Вопросы и ответы | 322 |
| [QA.md](QA.md) | Вопросы и ответы | 107 |
| [QA.md](QA.md) | Вопросы и ответы | 226 |
| [QA.md](QA.md) | Вопросы и ответы | 115 |
| [QA.md](QA.md) | Вопросы и ответы | 1268 |
| [QA.md](QA.md) | Вопросы и ответы | 266 |
| [QA.md](QA.md) | Вопросы и ответы | 332 |
| [QA.md](QA.md) | Вопросы и ответы | 117 |
| [QA.md](QA.md) | Вопросы и ответы | 310 |
| [QA.md](QA.md) | Вопросы и ответы | 150 |
| [QA.md](QA.md) | Вопросы и ответы | 336 |
| [QUESTIONS.md](QUESTIONS.md) | Открытые вопросы (484) | 1623 |
| [QUESTIONS.md](QUESTIONS.md) | Открытые вопросы (484) | 1633 |
| [READABILITY.md](READABILITY.md) | — | 7981 |
| [READING_ORDER.md](READING_ORDER.md) | Рекомендуемый порядок чтения | 5947 |
| [READING_ORDER.md](READING_ORDER.md) | Рекомендуемый порядок чтения | 5972 |
| [READING_TIME.md](READING_TIME.md) | — | 5783 |
| [README.md](README.md) | Главная страница и навигация | 126 |
| [README.md](README.md) | Главная страница и навигация | 2162 |
| [README.md](README.md) | Главная страница и навигация | 49 |
| [README.md](README.md) | Главная страница и навигация | 113 |
| [README.md](README.md) | Главная страница и навигация | 42 |
| [README.md](README.md) | Главная страница и навигация | 13 |
| [README.md](README.md) | Главная страница и навигация | 25 |
| [README.md](README.md) | Главная страница и навигация | 622 |
| [README.md](README.md) | Главная страница и навигация | 18 |
| [README.md](README.md) | Главная страница и навигация | 56 |
| [README.md](README.md) | Главная страница и навигация | 44 |
| [README.md](README.md) | Главная страница и навигация | 90 |
| [README.md](README.md) | Главная страница и навигация | 140 |
| [README.md](README.md) | Главная страница и навигация | 2178 |
| [README.md](README.md) | Главная страница и навигация | 62 |
| [README.md](README.md) | Главная страница и навигация | 123 |
| [README.md](README.md) | Главная страница и навигация | 54 |
| [README.md](README.md) | Главная страница и навигация | 23 |
| [README.md](README.md) | Главная страница и навигация | 35 |
| [README.md](README.md) | Главная страница и навигация | 631 |
| [README.md](README.md) | Главная страница и навигация | 27 |
| [README.md](README.md) | Главная страница и навигация | 65 |
| [README.md](README.md) | Главная страница и навигация | 54 |
| [README.md](README.md) | Главная страница и навигация | 99 |
| [README.md](README.md) | Главная страница и навигация | 100 |
| [README.md](README.md) | Главная страница и навигация | 90 |
| [REPORT.md](REPORT.md) | — | 318 |
| [RISK_REGISTER.md](RISK_REGISTER.md) | — | 1038 |
| [SCHEDULE.md](SCHEDULE.md) | — | 285 |
| [SCORING.md](SCORING.md) | — | 350 |
| [SEARCH.md](SEARCH.md) | Поисковый индекс | 4370 |
| [SEE_ALSO.md](SEE_ALSO.md) | — | 220 |
| [SENTIMENT.md](SENTIMENT.md) | — | 407 |
| [SIMILAR.md](SIMILAR.md) | Похожие документы (937 пар) | 393 |
| [SIMILAR.md](SIMILAR.md) | Похожие документы (937 пар) | 415 |
| [SOURCE_MAP.md](SOURCE_MAP.md) | — | 2909 |
| [SPELLCHECK.md](SPELLCHECK.md) | — | 143 |
| [STALENESS.md](STALENESS.md) | — | 412 |
| [STATS.md](STATS.md) | Детальная статистика | 511 |
| [STATS.md](STATS.md) | Детальная статистика | 519 |
| [TABLES.md](TABLES.md) | — | 63287 |
| [TABLES.md](TABLES.md) | — | 63300 |
| [TAGS.md](TAGS.md) | Теги (316 файлов, 12 тем) | 600 |
| [TAGS.md](TAGS.md) | Теги (316 файлов, 12 тем) | 610 |
| [TECH_RADAR.md](TECH_RADAR.md) | — | 635 |
| [TIMELINE.md](TIMELINE.md) | Временная шкала (800 маркеров) | 1803 |
| [TIMELINE.md](TIMELINE.md) | Временная шкала (800 маркеров) | 1814 |
| [TOPIC_MODEL.md](TOPIC_MODEL.md) | — | 1051 |
| [VALIDATION.md](VALIDATION.md) | — | 387 |
| [VERSION_DIFF.md](VERSION_DIFF.md) | — | 436 |
| [VOCABULARY.md](VOCABULARY.md) | — | 896 |
| [WORD_CLOUD.md](WORD_CLOUD.md) | — | 244 |
| [WORD_FREQ.md](WORD_FREQ.md) | Частотный анализ слов | 1790 |
| [WORD_FREQ.md](WORD_FREQ.md) | Частотный анализ слов | 1801 |


### 112. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 14 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Продолжение исследования для Svyazi 2.0](obsidian/01-svyazi/00-intro-part2.md) | 6 |
| 2 | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 731 |
| 3 | [Методика и рамка отбора проектов](obsidian/01-svyazi/02-methodology.md) | 428 |
| 4 | [03-component-catalog](obsidian/01-svyazi/03-component-catalog.md) | 1395 |
| 5 | [04-ensembles-overview](obsidian/01-svyazi/04-ensembles-overview.md) | 1274 |
| 6 | [06-security-privacy](obsidian/01-svyazi/06-security-privacy.md) | 821 |
| 7 | [07-mvp-planning](obsidian/01-svyazi/07-mvp-planning.md) | 1083 |
| 8 | [08-conclusions](obsidian/01-svyazi/08-conclusions.md) | 360 |
| 9 | [09-architectural-gaps](obsidian/01-svyazi/09-architectural-gaps.md) | 757 |
| 10 | [10-second-order-ensembles](obsidian/01-svyazi/10-second-order-ensembles.md) | 916 |
| 11 | [11-integration-contracts](obsidian/01-svyazi/11-integration-contracts.md) | 745 |
| 12 | [12-roadmap](obsidian/01-svyazi/12-roadmap.md) | 733 |
| 13 | [13-contacts](obsidian/01-svyazi/13-contacts.md) | 827 |
| 14 | [14-limitations](obsidian/01-svyazi/14-limitations.md) | 636 |


### 113. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 51 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Введение](04-ai-collaborations/00-intro.md) | 8884 |
| 2 | [Интегральный анализ профиля svend4](obsidian/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | 19103 |
| 3 | [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](obsidian/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md) | 3181 |
| 4 | [PORTAL-PROTOCOL.md](obsidian/02-anthropic-vacancies/03-portal-protocol-md.md) | 150 |
| 5 | [Abstract](obsidian/02-anthropic-vacancies/04-abstract.md) | 188 |
| 6 | [0. Status of This Document](obsidian/02-anthropic-vacancies/05-0-status-of-this-document.md) | 162 |
| 7 | [1. Introduction](obsidian/02-anthropic-vacancies/06-1-introduction.md) | 380 |
| 8 | [2. Terminology](obsidian/02-anthropic-vacancies/07-2-terminology.md) | 313 |
| 9 | [3. Registry (`nautilus.json`)](obsidian/02-anthropic-vacancies/08-3-registry-nautilus-json.md) | 422 |
| 10 | [4. Passport (`passport.md`)](obsidian/02-anthropic-vacancies/09-4-passport-passport-md.md) | 201 |
| 11 | [Доступ к данным](obsidian/02-anthropic-vacancies/102-доступ-к-данным.md) | 65 |
| 12 | [Appendix B: Change Log](obsidian/02-anthropic-vacancies/103-appendix-b-change-log.md) | 232 |
| 13 | [Appendix C: References](obsidian/02-anthropic-vacancies/104-appendix-c-references.md) | 947 |
| 14 | [REVIEW_METHODOLOGY.md](obsidian/02-anthropic-vacancies/105-review-methodology-md.md) | 128 |
| 15 | [TL;DR](obsidian/02-anthropic-vacancies/106-tl-dr.md) | 168 |
| 16 | [1. Контекст и мотивация](obsidian/02-anthropic-vacancies/107-1-контекст-и-мотивация.md) | 412 |
| 17 | [2. Формальный workflow](obsidian/02-anthropic-vacancies/108-2-формальный-workflow.md) | 479 |
| 18 | [3. Принципы консолидации (Фаза C)](obsidian/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md) | 541 |
| 19 | [Вопрос: fallback-ratio как критический или осмысле](obsidian/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) | 258 |
| 20 | [4. Условия применимости](obsidian/02-anthropic-vacancies/111-4-условия-применимости.md) | 279 |
| 21 | [5. Связь с существующими методологиями](obsidian/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) | 340 |
| 22 | [6. Почему это валидный паттерн для AI-assisted wor](obsidian/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) | 173 |
| 23 | [7. Реализация в проекте Nautilus](obsidian/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md) | 327 |
| 24 | [8. Ограничения и открытые вопросы](obsidian/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md) | 412 |
| 25 | [9. Checklist применения методологии](obsidian/02-anthropic-vacancies/116-9-checklist-применения-методологии.md) | 331 |
| 26 | [10. Конкретный план применения к текущим документа](obsidian/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md) | 258 |
| 27 | [Appendix A: Шаблон для header warning](obsidian/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md) | 176 |
| 28 | [Appendix B: Примеры расхождений и их разрешения](obsidian/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md) | 292 |
| 29 | [Content Overview](obsidian/02-anthropic-vacancies/12-content-overview.md) | 113 |
| 30 | [Главные технические риски](obsidian/02-anthropic-vacancies/120-главные-технические-риски.md) | 101 |
| 31 | [Appendix C: История изменений методологии](obsidian/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md) | 78 |
| 32 | [Глоссарий](obsidian/02-anthropic-vacancies/122-глоссарий.md) | 1302 |
| 33 | [portal-mcp.py](obsidian/02-anthropic-vacancies/123-portal-mcp-py.md) | 2316 |
| 34 | [Конфигурация для Claude Desktop](obsidian/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) | 212 |
| 35 | [README-MCP.md— инструкция по установке](obsidian/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) | 152 |
| 36 | [Установка](obsidian/02-anthropic-vacancies/126-установка.md) | 169 |
| 37 | [Подключение к Claude Desktop](obsidian/02-anthropic-vacancies/127-подключение-к-claude-desktop.md) | 177 |
| 38 | [Доступные инструменты](obsidian/02-anthropic-vacancies/128-доступные-инструменты.md) | 204 |
| 39 | [Примеры запросов (в Claude)](obsidian/02-anthropic-vacancies/129-примеры-запросов-в-claude.md) | 176 |
| 40 | [Angle / Perspective](obsidian/02-anthropic-vacancies/13-angle-perspective.md) | 127 |
| 41 | [Отладка](obsidian/02-anthropic-vacancies/130-отладка.md) | 205 |
| 42 | [Ограничения текущей версии (0.1.0-draft)](obsidian/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md) | 133 |
| 43 | [Planned (v0.2.0)](obsidian/02-anthropic-vacancies/132-planned-v0-2-0.md) | 131 |
| 44 | [Обратная связь](obsidian/02-anthropic-vacancies/133-обратная-связь.md) | 16959 |
| 45 | [THE DOUBLE-TRIANGLE ARCHITECTURE.md](obsidian/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md) | 130 |
| 46 | [A Formal Model for Human-AI Collaboration in Distr](obsidian/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md) | 167 |
| 47 | [Abstract](obsidian/02-anthropic-vacancies/136-abstract.md) | 388 |
| 48 | [Table of Contents](obsidian/02-anthropic-vacancies/137-table-of-contents.md) | 172 |
| 49 | [1. Why Single-Triangle Models Are Incomplete](obsidian/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) | 583 |
| 50 | [2. The Double-Triangle Architecture](obsidian/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) | 755 |
| ... | _ещё 305 файлов_ | |


### 114. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 5 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Агентные системы и роутинг](obsidian/03-technology-combinations/01-agent-routing.md) | 257 |
| 2 | [Графы знаний и Legal AI](obsidian/03-technology-combinations/02-knowledge-graphs.md) | 766 |
| 3 | [Local-first и P2P стек](obsidian/03-technology-combinations/03-local-first.md) | 386 |
| 4 | [Домен: немецкое социальное право](obsidian/03-technology-combinations/04-sozialrecht-domain.md) | 172 |
| 5 | [Бенчмарки и производительность](obsidian/03-technology-combinations/05-benchmarks.md) | 863 |


### 115. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 15 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Введение](04-ai-collaborations/00-intro.md) | 11445 |
| 2 | [Executive summary](04-ai-collaborations/01-executive-summary.md) | 647 |
| 3 | [Методика и рамка отбора](04-ai-collaborations/02-методика-и-рамка-отбора.md) | 495 |
| 4 | [Карта найденных проектов и паттернов](04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) | 1553 |
| 5 | [Приоритетные ансамбли](04-ai-collaborations/04-приоритетные-ансамбли.md) | 1418 |
| 6 | [План прототипа и возможные контакты](04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) | 1212 |
| 7 | [Безопасность, приватность и бюджетный роутинг](04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) | 966 |
| 8 | [Выводы](04-ai-collaborations/07-выводы.md) | 542 |
| 9 | [Что это продолжение добавляет](04-ai-collaborations/08-что-это-продолжение-добавляет.md) | 492 |
| 10 | [Архитектурные зазоры, которые важнее новых инструм](04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | 901 |
| 11 | [Новые ансамбли следующего шага](04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) | 1062 |
| 12 | [Интеграционный контракт, который стоит зафиксирова](04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | 928 |
| 13 | [Дорожная карта прототипа следующей итерации](04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md) | 862 |
| 14 | [Контактная стратегия и узкие вопросы для авторов](04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) | 956 |
| 15 | [Ограничения, лицензии и что пока лучше не склеиват](04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md) | 3362 |


### 116. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 6 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Синтез: как проекты собираются вместе](obsidian/05-habr-projects/01-synthesis.md) | 184 |
| 2 | [Авторы и контакты](obsidian/05-habr-projects/02-collaboration-partners.md) | 303 |
| 3 | [Wikontic: семантический граф](obsidian/05-habr-projects/knowledge/wikontic.md) | 306 |
| 4 | [MemNet: исследовательская память](obsidian/05-habr-projects/memory/memnet.md) | 7271 |
| 5 | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 419 |
| 6 | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 303 |


### 117. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 11 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Антропик](autofilled/components/.md) | 81 |
| 2 | [Cowork](autofilled/components/cowork.md) | 81 |
| 3 | [ingit](autofilled/components/ingit.md) | 81 |
| 4 | [kksudo](autofilled/components/kksudo.md) | 67 |
| 5 | [Lorenzo](autofilled/components/lorenzo.md) | 81 |
| 6 | [Nautilus](autofilled/components/nautilus.md) | 81 |
| 7 | [SGB](autofilled/components/sgb.md) | 81 |
| 8 | [spbmolot](autofilled/components/spbmolot.md) | 67 |
| 9 | [svend4](autofilled/components/svend4.md) | 81 |
| 10 | [Svyazi](autofilled/components/svyazi.md) | 81 |
| 11 | [[Тема исследования]](docs/autofilled/research-summary.md) | 122 |


### 118. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 14 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Контакт: AnastasiyaW / knowledge-space, mclaude](obsidian/contacts/anastasiyaw.md) | 292 |
| 2 | [Контакт: andrey_chuyan / Svyazi](obsidian/contacts/andrey-chuyan.md) | 274 |
| 3 | [Контакт: Antipozitive / MemNet](obsidian/contacts/antipozitive.md) | 264 |
| 4 | [Контакт: Cutcode / AIF Handoff](obsidian/contacts/cutcode.md) | 255 |
| 5 | [Контакт: Dmitriila / SENTINEL](obsidian/contacts/dmitriila.md) | 251 |
| 6 | [Контакт: kksudo / AgentFS](autofilled/components/kksudo.md) | 288 |
| 7 | [Контакт: MiXaiLL76 / Auto AI Router](obsidian/contacts/mixaill76.md) | 259 |
| 8 | [Контакт: nlaik / LiteParse / research-docs](obsidian/contacts/nlaik.md) | 260 |
| 9 | [Контакт: Sonia_Black / knowledge-space](obsidian/contacts/sonia-black.md) | 252 |
| 10 | [Контакт: spbmolot / NGT Memory](autofilled/components/spbmolot.md) | 292 |
| 11 | [Контакт: tagir_analyzes / Legal RAG](obsidian/contacts/tagir-analyzes.md) | 257 |
| 12 | [Контакт: VitalyOborin / Yodoca](obsidian/contacts/vitalyoborin.md) | 278 |
| 13 | [Контакт: VladSpace / Graph RAG](obsidian/contacts/vladspace.md) | 255 |
| 14 | [Контакт: zodigancode / Rufler](obsidian/contacts/zodigancode.md) | 251 |


### 119. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 51 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Продолжение исследования для Svyazi 2.0](obsidian/01-svyazi/00-intro-part2.md) | 19 |
| 2 | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/obsidian/01-svyazi/01-executive-summary.md) | 744 |
| 3 | [Методика и рамка отбора проектов](obsidian/01-svyazi/02-methodology.md) | 453 |
| 4 | [03-component-catalog](obsidian/01-svyazi/03-component-catalog.md) | 1406 |
| 5 | [04-ensembles-overview](obsidian/01-svyazi/04-ensembles-overview.md) | 1285 |
| 6 | [06-security-privacy](obsidian/01-svyazi/06-security-privacy.md) | 832 |
| 7 | [07-mvp-planning](obsidian/01-svyazi/07-mvp-planning.md) | 1094 |
| 8 | [08-conclusions](obsidian/01-svyazi/08-conclusions.md) | 370 |
| 9 | [09-architectural-gaps](obsidian/01-svyazi/09-architectural-gaps.md) | 768 |
| 10 | [10-second-order-ensembles](obsidian/01-svyazi/10-second-order-ensembles.md) | 928 |
| 11 | [11-integration-contracts](obsidian/01-svyazi/11-integration-contracts.md) | 756 |
| 12 | [12-roadmap](obsidian/01-svyazi/12-roadmap.md) | 743 |
| 13 | [13-contacts](obsidian/01-svyazi/13-contacts.md) | 837 |
| 14 | [14-limitations](obsidian/01-svyazi/14-limitations.md) | 646 |
| 15 | [Введение](04-ai-collaborations/00-intro.md) | 8893 |
| 16 | [Интегральный анализ профиля svend4](obsidian/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | 19115 |
| 17 | [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](obsidian/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md) | 3213 |
| 18 | [PORTAL-PROTOCOL.md](obsidian/02-anthropic-vacancies/03-portal-protocol-md.md) | 161 |
| 19 | [Abstract](obsidian/02-anthropic-vacancies/04-abstract.md) | 199 |
| 20 | [0. Status of This Document](obsidian/02-anthropic-vacancies/05-0-status-of-this-document.md) | 177 |
| 21 | [1. Introduction](obsidian/02-anthropic-vacancies/06-1-introduction.md) | 392 |
| 22 | [2. Terminology](obsidian/02-anthropic-vacancies/07-2-terminology.md) | 327 |
| 23 | [3. Registry (`nautilus.json`)](obsidian/02-anthropic-vacancies/08-3-registry-nautilus-json.md) | 435 |
| 24 | [4. Passport (`passport.md`)](obsidian/02-anthropic-vacancies/09-4-passport-passport-md.md) | 214 |
| 25 | [Доступ к данным](obsidian/02-anthropic-vacancies/102-доступ-к-данным.md) | 78 |
| 26 | [Appendix B: Change Log](obsidian/02-anthropic-vacancies/103-appendix-b-change-log.md) | 248 |
| 27 | [Appendix C: References](obsidian/02-anthropic-vacancies/104-appendix-c-references.md) | 972 |
| 28 | [REVIEW_METHODOLOGY.md](obsidian/02-anthropic-vacancies/105-review-methodology-md.md) | 139 |
| 29 | [TL;DR](obsidian/02-anthropic-vacancies/106-tl-dr.md) | 179 |
| 30 | [1. Контекст и мотивация](obsidian/02-anthropic-vacancies/107-1-контекст-и-мотивация.md) | 430 |
| 31 | [2. Формальный workflow](obsidian/02-anthropic-vacancies/108-2-формальный-workflow.md) | 496 |
| 32 | [3. Принципы консолидации (Фаза C)](obsidian/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md) | 560 |
| 33 | [Вопрос: fallback-ratio как критический или осмысле](obsidian/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) | 278 |
| 34 | [4. Условия применимости](obsidian/02-anthropic-vacancies/111-4-условия-применимости.md) | 296 |
| 35 | [5. Связь с существующими методологиями](obsidian/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) | 357 |
| 36 | [6. Почему это валидный паттерн для AI-assisted wor](obsidian/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) | 191 |
| 37 | [7. Реализация в проекте Nautilus](obsidian/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md) | 346 |
| 38 | [8. Ограничения и открытые вопросы](obsidian/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md) | 429 |
| 39 | [9. Checklist применения методологии](obsidian/02-anthropic-vacancies/116-9-checklist-применения-методологии.md) | 345 |
| 40 | [10. Конкретный план применения к текущим документа](obsidian/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md) | 277 |
| 41 | [Appendix A: Шаблон для header warning](obsidian/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md) | 192 |
| 42 | [Appendix B: Примеры расхождений и их разрешения](obsidian/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md) | 311 |
| 43 | [Content Overview](obsidian/02-anthropic-vacancies/12-content-overview.md) | 125 |
| 44 | [Главные технические риски](obsidian/02-anthropic-vacancies/120-главные-технические-риски.md) | 114 |
| 45 | [Appendix C: История изменений методологии](obsidian/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md) | 93 |
| 46 | [Глоссарий](obsidian/02-anthropic-vacancies/122-глоссарий.md) | 1319 |
| 47 | [portal-mcp.py](obsidian/02-anthropic-vacancies/123-portal-mcp-py.md) | 2333 |
| 48 | [Конфигурация для Claude Desktop](obsidian/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) | 226 |
| 49 | [README-MCP.md— инструкция по установке](obsidian/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) | 166 |
| 50 | [Установка](obsidian/02-anthropic-vacancies/126-установка.md) | 180 |
| ... | _ещё 423 файлов_ | |


### 120. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 5 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Контакт: [Имя / Проект]](docs/templates/contact-outreach.md) | 133 |
| 2 | [ADR: [Название решения]](docs/templates/decision-record.md) | 94 |
| 3 | [Ансамбль: [Название]](docs/templates/ensemble.md) | 124 |
| 4 | [[Название компонента]](docs/templates/project-component.md) | 116 |
| 5 | [[Тема исследования]](docs/templates/research-note.md) | 80 |


### 121. Категории
_Файл: `docs/SOURCE_MAP.md` | 2 колонок, 2 строк_

| Категория | Файлов |
|-----------|--------|
| 🤖 Авто-импорт | 391 |
| ✍️ Ручной | 132 |


### 122. Авторы
_Файл: `docs/SOURCE_MAP.md` | 2 колонок, 2 строк_

| Автор | Файлов |
|-------|--------|
| Claude | 513 |
| unknown | 10 |


### 123. 🤖 Авто-импортированные файлы (391)
_Файл: `docs/SOURCE_MAP.md` | 3 колонок, 391 строк_

| Файл | Слов | Первый коммит |
|------|------|--------------|
| `docs/01-svyazi/00-intro-part2.md` | 6 | 2026-04-29 |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 16 | 2026-04-29 |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 65 | 2026-04-29 |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 78 | 2026-04-29 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 101 | 2026-04-29 |
| `docs/02-anthropic-vacancies/16-history.md` | 104 | 2026-04-29 |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 106 | 2026-04-29 |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 108 | 2026-04-29 |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 113 | 2026-04-29 |
| `docs/02-anthropic-vacancies/31-content-overview.md` | 113 | 2026-04-29 |
| `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | 122 | 2026-04-29 |
| `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` | 123 | 2026-04-29 |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | 125 | 2026-04-29 |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 126 | 2026-04-29 |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | 126 | 2026-04-29 |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | 127 | 2026-04-29 |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | 128 | 2026-04-29 |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | 128 | 2026-04-29 |
| `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` | 128 | 2026-04-29 |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 130 | 2026-04-29 |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 130 | 2026-04-29 |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | 131 | 2026-04-29 |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | 133 | 2026-04-29 |
| `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` | 133 | 2026-04-29 |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | 133 | 2026-04-29 |
| `docs/02-anthropic-vacancies/35-passports-info1-md.md` | 133 | 2026-04-29 |
| `docs/02-anthropic-vacancies/55-passports-meta-md.md` | 134 | 2026-04-29 |
| `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` | 136 | 2026-04-29 |
| `docs/02-anthropic-vacancies/45-passports-pro2-md.md` | 137 | 2026-04-29 |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 138 | 2026-04-29 |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | 140 | 2026-04-29 |
| `docs/02-anthropic-vacancies/62-author-contact.md` | 140 | 2026-04-29 |
| `docs/02-anthropic-vacancies/42-author-contact.md` | 145 | 2026-04-29 |
| `docs/02-anthropic-vacancies/58-content-overview.md` | 147 | 2026-04-29 |
| `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` | 148 | 2026-04-29 |
| `docs/02-anthropic-vacancies/38-content-overview.md` | 148 | 2026-04-29 |
| `docs/02-anthropic-vacancies/61-compatibility-level.md` | 148 | 2026-04-29 |
| `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` | 149 | 2026-04-29 |
| `docs/02-anthropic-vacancies/51-compatibility-level.md` | 149 | 2026-04-29 |
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | 150 | 2026-04-29 |
| `docs/02-anthropic-vacancies/190-содержание.md` | 151 | 2026-04-29 |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | 152 | 2026-04-29 |
| `docs/02-anthropic-vacancies/41-compatibility-level.md` | 152 | 2026-04-29 |
| `docs/02-anthropic-vacancies/25-13-reference-implementation.md` | 153 | 2026-04-29 |
| `docs/02-anthropic-vacancies/65-readme-md.md` | 153 | 2026-04-29 |
| `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` | 153 | 2026-04-29 |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | 162 | 2026-04-29 |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | 164 | 2026-04-29 |
| `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` | 164 | 2026-04-29 |
| `docs/02-anthropic-vacancies/43-history.md` | 165 | 2026-04-29 |
| `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` | 166 | 2026-04-29 |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | 167 | 2026-04-29 |
| `docs/02-anthropic-vacancies/169-table-of-contents.md` | 167 | 2026-04-29 |
| `docs/02-anthropic-vacancies/106-tl-dr.md` | 168 | 2026-04-29 |
| `docs/02-anthropic-vacancies/49-angle-perspective.md` | 168 | 2026-04-29 |
| `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` | 168 | 2026-04-29 |
| `docs/02-anthropic-vacancies/126-установка.md` | 169 | 2026-04-29 |
| `docs/02-anthropic-vacancies/346-твоё-происхождение.md` | 169 | 2026-04-29 |
| `docs/02-anthropic-vacancies/46-essence.md` | 170 | 2026-04-29 |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | 172 | 2026-04-29 |
| `docs/03-technology-combinations/04-sozialrecht-domain.md` | 172 | 2026-04-29 |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/231-содержание.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/39-angle-perspective.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/52-author-contact.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` | 174 | 2026-04-29 |
| `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` | 174 | 2026-04-29 |
| `docs/02-anthropic-vacancies/59-angle-perspective.md` | 175 | 2026-04-29 |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | 176 | 2026-04-29 |
| `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` | 176 | 2026-04-29 |
| `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` | 176 | 2026-04-29 |
| `docs/02-anthropic-vacancies/326-содержание.md` | 178 | 2026-04-29 |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | 179 | 2026-04-29 |
| `docs/02-anthropic-vacancies/36-essence.md` | 179 | 2026-04-29 |
| `docs/02-anthropic-vacancies/60-bridges.md` | 180 | 2026-04-29 |
| `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` | 180 | 2026-04-29 |
| `docs/05-habr-projects/01-synthesis.md` | 184 | 2026-04-29 |
| `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` | 187 | 2026-04-29 |
| `docs/02-anthropic-vacancies/47-native-format.md` | 187 | 2026-04-29 |
| `docs/02-anthropic-vacancies/04-abstract.md` | 188 | 2026-04-29 |
| `docs/02-anthropic-vacancies/253-table-of-contents.md` | 189 | 2026-04-29 |
| `docs/02-anthropic-vacancies/63-history.md` | 189 | 2026-04-29 |
| `docs/02-anthropic-vacancies/203-благодарности.md` | 191 | 2026-04-29 |
| `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` | 192 | 2026-04-29 |
| `docs/02-anthropic-vacancies/244-благодарности.md` | 193 | 2026-04-29 |
| `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` | 193 | 2026-04-29 |
| `docs/02-anthropic-vacancies/57-native-format.md` | 193 | 2026-04-29 |
| `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` | 194 | 2026-04-29 |
| `docs/02-anthropic-vacancies/56-essence.md` | 194 | 2026-04-29 |
| `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` | 195 | 2026-04-29 |
| `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` | 195 | 2026-04-29 |
| `docs/02-anthropic-vacancies/211-table-of-contents.md` | 196 | 2026-04-29 |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | 197 | 2026-04-29 |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | 197 | 2026-04-29 |
| `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` | 197 | 2026-04-29 |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 198 | 2026-04-29 |
| `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` | 198 | 2026-04-29 |
| `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | 198 | 2026-04-29 |
| `docs/02-anthropic-vacancies/320-references.md` | 199 | 2026-04-29 |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 200 | 2026-04-29 |
| `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` | 201 | 2026-04-29 |
| `docs/02-anthropic-vacancies/338-ссылки.md` | 201 | 2026-04-29 |
| `docs/02-anthropic-vacancies/53-history.md` | 201 | 2026-04-29 |
| `docs/02-anthropic-vacancies/128-доступные-инструменты.md` | 204 | 2026-04-29 |
| `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` | 204 | 2026-04-29 |
| `docs/02-anthropic-vacancies/130-отладка.md` | 205 | 2026-04-29 |
| `docs/02-anthropic-vacancies/308-table-of-contents.md` | 206 | 2026-04-29 |
| `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | 206 | 2026-04-29 |
| `docs/02-anthropic-vacancies/48-content-overview.md` | 206 | 2026-04-29 |
| `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` | 211 | 2026-04-29 |
| `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` | 211 | 2026-04-29 |
| `docs/02-anthropic-vacancies/40-bridges.md` | 211 | 2026-04-29 |
| `docs/02-anthropic-vacancies/50-bridges.md` | 211 | 2026-04-29 |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | 212 | 2026-04-29 |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 212 | 2026-04-29 |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | 216 | 2026-04-29 |
| `docs/02-anthropic-vacancies/224-acknowledgments.md` | 219 | 2026-04-29 |
| `docs/02-anthropic-vacancies/345-кто-ты.md` | 220 | 2026-04-29 |
| `docs/02-anthropic-vacancies/349-твоя-личность.md` | 223 | 2026-04-29 |
| `docs/02-anthropic-vacancies/301-благодарности.md` | 231 | 2026-04-29 |
| `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` | 232 | 2026-04-29 |
| `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` | 232 | 2026-04-29 |
| `docs/02-anthropic-vacancies/356-твой-workflow.md` | 232 | 2026-04-29 |
| `docs/02-anthropic-vacancies/37-native-format.md` | 234 | 2026-04-29 |
| `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` | 235 | 2026-04-29 |
| `docs/02-anthropic-vacancies/21-9-query-flow.md` | 237 | 2026-04-29 |
| `docs/02-anthropic-vacancies/24-12-versioning-policy.md` | 237 | 2026-04-29 |
| `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` | 238 | 2026-04-29 |
| `docs/02-anthropic-vacancies/300-заключение.md` | 239 | 2026-04-29 |
| `docs/02-anthropic-vacancies/302-ссылки.md` | 239 | 2026-04-29 |
| `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` | 240 | 2026-04-29 |
| `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` | 240 | 2026-04-29 |
| `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` | 240 | 2026-04-29 |
| `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` | 241 | 2026-04-29 |
| `docs/02-anthropic-vacancies/93-18-reference-implementation.md` | 243 | 2026-04-29 |
| `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` | 244 | 2026-04-29 |
| `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` | 244 | 2026-04-29 |
| `docs/02-anthropic-vacancies/182-acknowledgments.md` | 245 | 2026-04-29 |
| `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` | 247 | 2026-04-29 |
| `docs/02-anthropic-vacancies/23-11-security-considerations.md` | 248 | 2026-04-29 |
| `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` | 250 | 2026-04-29 |
| `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` | 251 | 2026-04-29 |
| `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` | 257 | 2026-04-29 |
| `docs/03-technology-combinations/01-agent-routing.md` | 257 | 2026-04-29 |
| `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` | 258 | 2026-04-29 |
| `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` | 258 | 2026-04-29 |
| `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` | 259 | 2026-04-29 |
| `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` | 260 | 2026-04-29 |
| `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` | 260 | 2026-04-29 |
| `docs/02-anthropic-vacancies/74-abstract.md` | 260 | 2026-04-29 |
| `docs/02-anthropic-vacancies/286-acknowledgments.md` | 263 | 2026-04-29 |
| `docs/02-anthropic-vacancies/285-closing.md` | 270 | 2026-04-29 |
| `docs/02-anthropic-vacancies/146-acknowledgments.md` | 273 | 2026-04-29 |
| `docs/02-anthropic-vacancies/111-4-условия-применимости.md` | 279 | 2026-04-29 |
| `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | 279 | 2026-04-29 |
| `docs/02-anthropic-vacancies/181-12-closing.md` | 281 | 2026-04-29 |
| `docs/02-anthropic-vacancies/189-аннотация.md` | 281 | 2026-04-29 |
| `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` | 282 | 2026-04-29 |
| `docs/02-anthropic-vacancies/85-10-query-flow.md` | 283 | 2026-04-29 |
| `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | 288 | 2026-04-29 |
| `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | 289 | 2026-04-29 |
| `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` | 291 | 2026-04-29 |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | 292 | 2026-04-29 |
| `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` | 293 | 2026-04-29 |
| `docs/02-anthropic-vacancies/92-17-versioning-policy.md` | 294 | 2026-04-29 |
| `docs/02-anthropic-vacancies/287-references.md` | 295 | 2026-04-29 |
| `docs/02-anthropic-vacancies/267-acknowledgments.md` | 297 | 2026-04-29 |
| `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` | 300 | 2026-04-29 |
| `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` | 302 | 2026-04-29 |
| `docs/05-habr-projects/02-collaboration-partners.md` | 303 | 2026-04-29 |
| `docs/02-anthropic-vacancies/204-ссылки.md` | 306 | 2026-04-29 |
| `docs/02-anthropic-vacancies/230-аннотация.md` | 310 | 2026-04-29 |
| `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` | 310 | 2026-04-29 |
| `docs/02-anthropic-vacancies/07-2-terminology.md` | 313 | 2026-04-29 |
| `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` | 313 | 2026-04-29 |
| `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | 313 | 2026-04-29 |
| `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` | 314 | 2026-04-29 |
| `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` | 316 | 2026-04-29 |
| `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` | 317 | 2026-04-29 |
| `docs/02-anthropic-vacancies/325-аннотация.md` | 317 | 2026-04-29 |
| `docs/02-anthropic-vacancies/183-references.md` | 322 | 2026-04-29 |
| `docs/02-anthropic-vacancies/307-abstract.md` | 323 | 2026-04-29 |
| `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` | 325 | 2026-04-29 |
| `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` | 325 | 2026-04-29 |
| `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` | 327 | 2026-04-29 |
| `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` | 331 | 2026-04-29 |
| `docs/02-anthropic-vacancies/245-ссылки.md` | 331 | 2026-04-29 |
| `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` | 332 | 2026-04-29 |
| `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` | 332 | 2026-04-29 |
| `docs/02-anthropic-vacancies/168-abstract.md` | 334 | 2026-04-29 |
| `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` | 335 | 2026-04-29 |
| `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` | 338 | 2026-04-29 |
| `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` | 338 | 2026-04-29 |
| `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` | 340 | 2026-04-29 |
| `docs/02-anthropic-vacancies/252-abstract.md` | 347 | 2026-04-29 |
| `docs/02-anthropic-vacancies/210-abstract.md` | 349 | 2026-04-29 |
| `docs/02-anthropic-vacancies/147-references.md` | 350 | 2026-04-29 |
| `docs/02-anthropic-vacancies/275-why-this-document-exists.md` | 350 | 2026-04-29 |
| `docs/02-anthropic-vacancies/225-references.md` | 351 | 2026-04-29 |
| `docs/02-anthropic-vacancies/337-благодарности.md` | 351 | 2026-04-29 |
| `docs/02-anthropic-vacancies/90-15-security-considerations.md` | 354 | 2026-04-29 |
| `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` | 357 | 2026-04-29 |
| `docs/01-svyazi/08-conclusions.md` | 360 | 2026-04-29 |
| `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` | 364 | 2026-04-29 |
| `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` | 366 | 2026-04-29 |
| `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` | 366 | 2026-04-29 |
| `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | 367 | 2026-04-29 |
| `docs/02-anthropic-vacancies/153-executive-summary.md` | 370 | 2026-04-29 |
| `docs/02-anthropic-vacancies/281-the-recursive-insight.md` | 371 | 2026-04-29 |
| `docs/02-anthropic-vacancies/243-12-заключение.md` | 375 | 2026-04-29 |
| `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` | 378 | 2026-04-29 |
| `docs/02-anthropic-vacancies/06-1-introduction.md` | 380 | 2026-04-29 |
| `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` | 380 | 2026-04-29 |
| `docs/02-anthropic-vacancies/319-acknowledgments.md` | 384 | 2026-04-29 |
| `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` | 386 | 2026-04-29 |
| `docs/03-technology-combinations/03-local-first.md` | 386 | 2026-04-29 |
| `docs/02-anthropic-vacancies/136-abstract.md` | 388 | 2026-04-29 |
| `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | 392 | 2026-04-29 |
| `docs/02-anthropic-vacancies/81-6-adapter-interface.md` | 392 | 2026-04-29 |
| `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` | 399 | 2026-04-29 |
| `docs/02-anthropic-vacancies/77-2-terminology.md` | 403 | 2026-04-29 |
| `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` | 406 | 2026-04-29 |
| `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` | 407 | 2026-04-29 |
| `docs/02-anthropic-vacancies/223-12-closing.md` | 409 | 2026-04-29 |
| `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` | 411 | 2026-04-29 |
| `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` | 412 | 2026-04-29 |
| `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | 412 | 2026-04-29 |
| `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` | 414 | 2026-04-29 |
| `docs/02-anthropic-vacancies/268-references.md` | 416 | 2026-04-29 |
| `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` | 419 | 2026-04-29 |
| `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` | 422 | 2026-04-29 |
| `docs/02-anthropic-vacancies/18-6-adapter-interface.md` | 425 | 2026-04-29 |
| `docs/01-svyazi/02-methodology.md` | 428 | 2026-04-29 |
| `docs/02-anthropic-vacancies/266-13-closing.md` | 434 | 2026-04-29 |
| `docs/02-anthropic-vacancies/179-10-open-questions.md` | 446 | 2026-04-29 |
| `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` | 447 | 2026-04-29 |
| `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` | 447 | 2026-04-29 |
| `docs/02-anthropic-vacancies/221-10-open-questions.md` | 460 | 2026-04-29 |
| `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` | 472 | 2026-04-29 |
| `docs/02-anthropic-vacancies/76-1-introduction.md` | 473 | 2026-04-29 |
| `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` | 477 | 2026-04-29 |
| `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` | 479 | 2026-04-29 |
| `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` | 479 | 2026-04-29 |
| `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | 486 | 2026-04-29 |
| `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` | 488 | 2026-04-29 |
| `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` | 492 | 2026-04-29 |
| `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | 492 | 2026-04-29 |
| `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | 495 | 2026-04-29 |
| `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` | 495 | 2026-04-29 |
| `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` | 507 | 2026-04-29 |
| `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` | 513 | 2026-04-29 |
| `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` | 541 | 2026-04-29 |
| `docs/04-ai-collaborations/07-выводы.md` | 542 | 2026-04-29 |
| `docs/02-anthropic-vacancies/294-существующие-приближения.md` | 565 | 2026-04-29 |
| `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` | 583 | 2026-04-29 |
| `docs/02-anthropic-vacancies/279-existing-approximations.md` | 588 | 2026-04-29 |
| `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` | 592 | 2026-04-29 |
| `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` | 595 | 2026-04-29 |
| `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` | 596 | 2026-04-29 |
| `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` | 596 | 2026-04-29 |
| `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` | 610 | 2026-04-29 |
| `docs/02-anthropic-vacancies/175-6-ethical-framework.md` | 611 | 2026-04-29 |
| `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` | 620 | 2026-04-29 |
| `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` | 625 | 2026-04-29 |
| `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` | 625 | 2026-04-29 |
| `docs/02-anthropic-vacancies/155-1-problem-statement.md` | 632 | 2026-04-29 |
| `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` | 634 | 2026-04-29 |
| `docs/01-svyazi/14-limitations.md` | 636 | 2026-04-29 |
| `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` | 636 | 2026-04-29 |
| `docs/02-anthropic-vacancies/264-11-open-questions.md` | 638 | 2026-04-29 |
| `docs/04-ai-collaborations/01-executive-summary.md` | 647 | 2026-04-29 |
| `docs/02-anthropic-vacancies/162-8-risk-analysis.md` | 653 | 2026-04-29 |
| `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` | 653 | 2026-04-29 |
| `docs/02-anthropic-vacancies/159-5-economic-model.md` | 654 | 2026-04-29 |
| `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` | 662 | 2026-04-29 |
| `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` | 663 | 2026-04-29 |
| `docs/02-anthropic-vacancies/174-5-architectural-specification.md` | 665 | 2026-04-29 |
| `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` | 666 | 2026-04-29 |
| `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` | 666 | 2026-04-29 |
| `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` | 667 | 2026-04-29 |
| `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` | 672 | 2026-04-29 |
| `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` | 674 | 2026-04-29 |
| `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` | 675 | 2026-04-29 |
| `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` | 677 | 2026-04-29 |
| `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | 678 | 2026-04-29 |
| `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` | 678 | 2026-04-29 |
| `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` | 679 | 2026-04-29 |
| `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` | 681 | 2026-04-29 |
| `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` | 682 | 2026-04-29 |
| `docs/02-anthropic-vacancies/156-2-target-populations.md` | 683 | 2026-04-29 |
| `docs/02-anthropic-vacancies/238-7-области-применения.md` | 683 | 2026-04-29 |
| `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` | 689 | 2026-04-29 |
| `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` | 696 | 2026-04-29 |
| `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` | 697 | 2026-04-29 |
| `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` | 698 | 2026-04-29 |
| `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` | 698 | 2026-04-29 |
| `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` | 707 | 2026-04-29 |
| `docs/01-svyazi/01-executive-summary.md` | 708 | 2026-04-29 |
| `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` | 713 | 2026-04-29 |
| `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` | 714 | 2026-04-29 |
| `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` | 721 | 2026-04-29 |
| `docs/01-svyazi/12-roadmap.md` | 733 | 2026-04-29 |
| `docs/02-anthropic-vacancies/218-7-application-domains.md` | 743 | 2026-04-29 |
| `docs/01-svyazi/11-integration-contracts.md` | 745 | 2026-04-29 |
| `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` | 745 | 2026-04-29 |
| `docs/02-anthropic-vacancies/145-8-call-to-action.md` | 746 | 2026-04-29 |
| `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` | 749 | 2026-04-29 |
| `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` | 749 | 2026-04-29 |
| `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` | 750 | 2026-04-29 |
| `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | 751 | 2026-04-29 |
| `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` | 753 | 2026-04-29 |
| `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` | 755 | 2026-04-29 |
| `docs/01-svyazi/09-architectural-gaps.md` | 757 | 2026-04-29 |
| `docs/03-technology-combinations/02-knowledge-graphs.md` | 766 | 2026-04-29 |
| `docs/02-anthropic-vacancies/144-7-open-questions.md` | 777 | 2026-04-29 |
| `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | 782 | 2026-04-29 |
| `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` | 788 | 2026-04-29 |
| `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` | 790 | 2026-04-29 |
| `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` | 803 | 2026-04-29 |
| `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` | 804 | 2026-04-29 |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | 804 | 2026-04-29 |
| `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` | 807 | 2026-04-29 |
| `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` | 810 | 2026-04-29 |
| `docs/01-svyazi/06-security-privacy.md` | 821 | 2026-04-29 |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | 821 | 2026-04-29 |
| `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` | 823 | 2026-04-29 |
| `docs/01-svyazi/13-contacts.md` | 827 | 2026-04-29 |
| `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` | 828 | 2026-04-29 |
| `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` | 844 | 2026-04-29 |
| `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` | 845 | 2026-04-29 |
| `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | 855 | 2026-04-29 |
| `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | 862 | 2026-04-29 |
| `docs/03-technology-combinations/05-benchmarks.md` | 863 | 2026-04-29 |
| `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` | 867 | 2026-04-29 |
| `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` | 868 | 2026-04-29 |
| `docs/02-anthropic-vacancies/68-about.md` | 880 | 2026-04-29 |
| `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | 885 | 2026-04-29 |
| `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` | 888 | 2026-04-29 |
| `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | 900 | 2026-04-29 |
| `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` | 901 | 2026-04-29 |
| `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 901 | 2026-04-29 |
| `docs/01-svyazi/10-second-order-ensembles.md` | 916 | 2026-04-29 |
| `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 928 | 2026-04-29 |
| `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | 930 | 2026-04-29 |
| `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` | 946 | 2026-04-29 |
| `docs/02-anthropic-vacancies/104-appendix-c-references.md` | 947 | 2026-04-29 |
| `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 956 | 2026-04-29 |
| `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 966 | 2026-04-29 |
| `docs/02-anthropic-vacancies/164-10-appendices.md` | 970 | 2026-04-29 |
| `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` | 973 | 2026-04-29 |
| `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` | 974 | 2026-04-29 |
| `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` | 978 | 2026-04-29 |
| `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` | 1001 | 2026-04-29 |
| `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` | 1014 | 2026-04-29 |
| `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | 1062 | 2026-04-29 |
| `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` | 1078 | 2026-04-29 |
| `docs/01-svyazi/07-mvp-planning.md` | 1083 | 2026-04-29 |
| `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` | 1125 | 2026-04-29 |
| `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` | 1209 | 2026-04-29 |
| `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 1212 | 2026-04-29 |
| `docs/01-svyazi/04-ensembles-overview.md` | 1274 | 2026-04-29 |
| `docs/02-anthropic-vacancies/122-глоссарий.md` | 1302 | 2026-04-29 |
| `docs/01-svyazi/03-component-catalog.md` | 1395 | 2026-04-29 |
| `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` | 1418 | 2026-04-29 |
| `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` | 1459 | 2026-04-29 |
| `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` | 1549 | 2026-04-29 |
| `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 1553 | 2026-04-29 |
| `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` | 1570 | 2026-04-29 |
| `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` | 1582 | 2026-04-29 |
| `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` | 1730 | 2026-04-29 |
| `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` | 2024 | 2026-04-29 |
| `docs/02-anthropic-vacancies/123-portal-mcp-py.md` | 2316 | 2026-04-29 |
| `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` | 3181 | 2026-04-29 |
| `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 3362 | 2026-04-29 |
| `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | 3425 | 2026-04-29 |
| `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 3835 | 2026-04-29 |
| `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` | 3851 | 2026-04-29 |
| `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` | 4049 | 2026-04-29 |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | 4385 | 2026-04-29 |
| `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` | 5807 | 2026-04-29 |
| `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` | 7108 | 2026-04-29 |
| `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` | 8397 | 2026-04-29 |
| `docs/02-anthropic-vacancies/00-intro.md` | 8884 | 2026-04-29 |
| `docs/02-anthropic-vacancies/165-closing.md` | 9251 | 2026-04-29 |
| `docs/02-anthropic-vacancies/69-section.md` | 9520 | 2026-04-29 |
| `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` | 11237 | 2026-04-29 |
| `docs/04-ai-collaborations/00-intro.md` | 11445 | 2026-04-29 |
| `docs/02-anthropic-vacancies/133-обратная-связь.md` | 16959 | 2026-04-29 |
| `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` | 19103 | 2026-04-29 |
| `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` | 20414 | 2026-04-29 |


### 124. Без метаданных (нет summary или тегов) — 165 файлов
_Файл: `docs/STALENESS.md` | 3 колонок, 20 строк_

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/00-intro-part2.md` | 5 | нет summary, нет тегов, короткий (5 слов) |
| `docs/01-svyazi/QA.md` | 206 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | нет summary, нет тегов, короткий (14 слов) |
| `docs/02-anthropic-vacancies/QA.md` | 360 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/03-technology-combinations/README.md` | 38 | нет тегов, короткий (38 слов) |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/04-ai-collaborations/README.md` | 82 | нет summary, нет тегов, короткий (82 слов) |
| `docs/05-habr-projects/QA.md` | 111 | нет summary, нет тегов |
| `docs/05-habr-projects/README.md` | 38 | нет summary, нет тегов, короткий (38 слов) |
| `docs/05-habr-projects/knowledge/README.md` | 9 | нет summary, нет тегов, короткий (9 слов) |
| `docs/05-habr-projects/memory/README.md` | 17 | нет summary, нет тегов, короткий (17 слов) |
| `docs/ABBREVIATIONS.md` | 1030 | нет summary, нет тегов |
| `docs/ACTION_ITEMS.md` | 4906 | нет summary |
| `docs/ALERTS.md` | 50 | нет summary, нет тегов, короткий (50 слов) |
| `docs/AUTHORS.md` | 81 | нет summary, нет тегов, короткий (81 слов) |
| `docs/BACKLINKS.md` | 194 | нет summary, нет тегов |
| `docs/BROKEN_LINKS.md` | 494 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 884 | нет summary, нет тегов |
| `docs/CITATION_INDEX.md` | 496 | нет summary, нет тегов |


### 125. Короткие (< 100 слов, заготовки) — 39 файлов
_Файл: `docs/STALENESS.md` | 2 колонок, 20 строк_

| Файл | Слов |
|------|------|
| `docs/01-svyazi/README.md` | 86 |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 52 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 87 |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 66 |
| `docs/02-anthropic-vacancies/16-history.md` | 90 |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 96 |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 94 |
| `docs/autofilled/components/.md` | 77 |
| `docs/autofilled/components/cowork.md` | 77 |
| `docs/autofilled/components/ingit.md` | 77 |
| `docs/autofilled/components/kksudo.md` | 62 |
| `docs/autofilled/components/lorenzo.md` | 77 |
| `docs/autofilled/components/nautilus.md` | 77 |
| `docs/autofilled/components/sgb.md` | 77 |
| `docs/autofilled/components/spbmolot.md` | 62 |
| `docs/autofilled/components/svend4.md` | 77 |
| `docs/autofilled/components/svyazi.md` | 77 |
| `docs/obsidian/02-anthropic-vacancies/102-доступ-к-данным.md` | 61 |
| `docs/obsidian/02-anthropic-vacancies/120-главные-технические-риски.md` | 96 |
| `docs/obsidian/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 77 |


### 126. Сводная таблица по разделам
_Файл: `docs/STATS.md` | 8 колонок, 12 строк_

| Раздел | Файлов | Слов | H2 | Таблиц | Блоков кода | Ссылок | Жирного |
|--------|--------|------|----|--------|-------------|--------|---------|
| **01-svyazi** | 16 | 11,020 | 73 | 43 | 8 | 261 | 268 |
| **02-anthropic-vacancies** | 357 | 284,383 | 1274 | 130 | 185 | 7072 | 3557 |
| **03-technology-combinations** | 7 | 2,600 | 19 | 5 | 0 | 65 | 22 |
| **04-ai-collaborations** | 17 | 27,180 | 89 | 89 | 0 | 349 | 360 |
| **05-habr-projects** | 10 | 8,981 | 32 | 18 | 0 | 156 | 54 |
| **autofilled** | 13 | 978 | 40 | 0 | 0 | 157 | 64 |
| **badges** | 1 | 44 | 2 | 0 | 1 | 14 | 0 |
| **contacts** | 15 | 3,818 | 88 | 56 | 14 | 283 | 43 |
| **obsidian** | 521 | 515,585 | 2114 | 5115 | 319 | 3311 | 8414 |
| **root** | 84 | 184,571 | 565 | 5382 | 108 | 4191 | 4316 |
| **templates** | 6 | 637 | 27 | 13 | 4 | 26 | 14 |
| **ИТОГО** | **1047** | **1,039,797** | **4323** | **10851** | **639** | **15885** | **17112** |


### 127. Топ-20 файлов по объёму
_Файл: `docs/STATS.md` | 5 колонок, 20 строк_

| Файл | Слов | H2 | Таблиц | Код |
|------|------|----|--------|-----|
| `TABLES` | 63300 | 8 | 2738 | 1 |
| `TABLES` | 63287 | 8 | 2738 | 1 |
| `341-приложение-c-образец-спецификаций-ин` | 20430 | 4 | 0 | 11 |
| `341-приложение-c-образец-спецификаций-ин` | 20414 | 4 | 0 | 11 |
| `01-интегральный-анализ-профиля-svend4` | 19115 | 4 | 0 | 19 |
| `01-интегральный-анализ-профиля-svend4` | 19103 | 4 | 0 | 19 |
| `133-обратная-связь` | 16969 | 4 | 6 | 17 |
| `133-обратная-связь` | 16959 | 4 | 6 | 17 |
| `OUTLINE` | 14253 | 12 | 0 | 0 |
| `OUTLINE` | 14242 | 12 | 0 | 0 |
| `00-intro` | 11454 | 4 | 3 | 0 |
| `00-intro` | 11445 | 4 | 3 | 0 |
| `CONCEPTS` | 11408 | 55 | 0 | 0 |
| `CONCEPTS` | 11402 | 55 | 0 | 0 |
| `342-что-такое-вариант-c-concept-document` | 11256 | 4 | 0 | 6 |
| `342-что-такое-вариант-c-concept-document` | 11237 | 4 | 0 | 6 |
| `69-section` | 9545 | 4 | 2 | 18 |
| `69-section` | 9520 | 4 | 2 | 18 |
| `165-closing` | 9260 | 4 | 0 | 1 |
| `165-closing` | 9251 | 4 | 0 | 1 |


### 128. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **MCP Protocol** | Инструменты | Стандарт интеграции AI-инструментов — Anthropic |
| **CardIndex** | Компоненты | 785+ карточек знаний, MIT, стабильный API |
| **AgentFS** | Компоненты | Файловая система для AI-агентов, MIT, kksudo |
| **Firecrawl** | Инструменты | Веб-краулер для AI, MIT, активная разработка |
| **Python 3.11+** | Платформа | Основной язык реализации всех компонентов |
| **Markdown docs** | Практики | 96% готовности, проверено на 460+ файлах |


### 129. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **Yodoca** | Компоненты | Память с консолидацией, Apache 2.0, spbmolot |
| **SENTINEL** | Компоненты | Allowlist безопасности для MCP |
| **Rufler** | Компоненты | Оркестратор агентов, активная разработка |
| **RAG + Graph** | Архитектура | Гибридный поиск: векторный + граф-обход |
| **claude-haiku-4-5** | Модели | Оптимум цена/качество для enrichment задач |
| **CRDT-синхронизация** | Архитектура | Бесконфликтная репликация для multi-agent |


### 130. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **NGT-memory** | Компоненты | Ассоциативный граф памяти, BSL 1.1 |
| **knowledge-space** | Компоненты | База знаний, MIT, нужна оценка API |
| **Wikontic** | Компоненты | Граф знаний, статус неизвестен |
| **MCP Tool Search** | Компоненты | Динамический поиск инструментов |
| **claude-opus-4-7** | Модели | Для сложных reasoning задач, высокая стоимость |
| **Local-first P2P** | Архитектура | GDPR-safe распределённые данные |


### 131. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 4 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **BSL 1.1 libs** | Лицензии | Ограничения при коммерческом использовании |
| **Monolithic LLM** | Архитектура | Один LLM вместо ансамбля — узкое место |
| **Без PII-защиты** | Практики | Обработка данных без SENTINEL/quarantine |
| **Hard-coded prompts** | Практики | Промпты без версионирования и тестов |


### 132. Точная дата (2492)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `2026-04-19` | pendix-b-change-log) - [v1.1.0-draft (2026-04-19)](#v110-draft-2026-04-19) - [v1.0.0-draft (2026-04 earlie | `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` |
| `2026-04-19` | kdown / Python LOC / 6 782 / _(verified 2026-04-19, see ADR or commit abc123; both A= | `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` |
| `2026-05-03` | 4 частей 2. Установить deadline Фазы C: 2026-05-03 (2 недели) 3. Провести верификацию конкретных метрик: ```b | `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` |
| `2026-04-19` | kdown / Python LOC / 6 812 / _(verified 2026-04-19; both A=6782 and B=~6600 were poin | `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` |
| `2026-04-19` | жен вывести в stderr что-то вроде: ``` [2026-04-19 14:30:00,123] INFO nautilus-mcp: Warming up portal... [2026 | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `2025-11-12` | икальный ID: sozialamt_dresden:bescheid:2025-11-12:SO-123 . Содержит: issuer, addressee, дата, срок Widerspruc | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `2024-01-01` | Темпоральные "effective_from": "2024-01-01", # ISO date, Inkrafttreten "effective_until": | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `2025-12-15` | # Процессуальные "deadline": "2025-12-15", # если документ содержит срок "deadlin | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `2026-04-19` | rk **Draft:** v1.0.0-draft **Date:** 2026-04-19 **Author:** svend4 **Editorial review:** Claude (intell | `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` |
| `2026-04-19` | x-c-version-history) - [v1.0.0-draft (2026-04-19)](#v100-draft-2026-04-19) - [Комментарий к документу](#ко | `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` |
| `2026-04-19` | **Version:** 1.0.0-draft **Date:** 2026-04-19 **Author:** svend4 **Editorial collaboration:** Claude | `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` |
| `2026-04-15` | ппинге" occurrences: 3 first_seen: "2026-04-15" candidate_pattern: "specialized form of Eingliederungshi | `docs/02-anthropic-vacancies/165-closing.md` |
| `2026-04-19` | 1 **Version:** 1.0.0-draft **Date:** 2026-04-19 **Author:** svend4 **Editorial collaboration:** Claude | `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` |
| `2026-04-19` | .1 **Версия:** 1.0.0-draft **Дата:** 2026-04-19 **Автор:** svend4 **Редакторская работа:** Claude **Л | `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` |
| `2026/04/25` | **[Запрос]** [ https://www.fontanka.ru/2026/04/25/76378978/ нужно подробно подробно и детальнее разобрать на | `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` |
| `2026-04-26` | 1.1 **Version:** 1.0.0-draft **Date:** 2026-04-26 **Author:** svend4 **Editorial collaboration:** Claude **Li | `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` |
| `2026/04/25` | Fontanka.ru*. https://www.fontanka.ru/2026/04/25/76378978/ ### Companion Papers - svend4 (2026). *The Repr | `docs/02-anthropic-vacancies/225-references.md` |
| `2026/04/25` | tudy: «Обучай» (https://www.fontanka.ru/2026/04/25/76378978/)* *Seeking collaborators, critics, and pilot par | `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` |
| `2026-04-26` | 1 **Версия:** 1.0.0-черновик **Дата:** 2026-04-26 **Автор:** svend4 **Редакторская работа:** Claude **Лицензи | `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` |
| `2026/04/25` | Fontanka.ru*. https://www.fontanka.ru/2026/04/25/76378978/ ### Сопроводительные Документы - svend4 (2026). | `docs/02-anthropic-vacancies/245-ссылки.md` |
| `2026/04/25` | кейс: «Обучай» (https://www.fontanka.ru/2026/04/25/76378978/)* *Ищем сотрудников, критиков и пилотных партнёр | `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` |
| `2026-04-26` | 1 **Version:** 1.0.0-draft **Date:** 2026-04-26 **Author:** svend4 **Editorial collaboration:** Claude | `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` |
| `2026-04-15` | Procedural guidance" last_updated: "2026-04-15" next_review: "2026-10-15" curators: primary: | `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` |
| `2026-10-15` | updated: "2026-04-15" next_review: "2026-10-15" curators: primary: name: "[Curator name]" | `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` |
| `2026-04-26` | 7) **Version:** 1.0.0-draft **Date:** 2026-04-26 **Author:** svend4 **Editorial collaboration:** Claude **Li | `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` |
| `2026-04-26` | ) **Версия:** 1.0.0-черновик **Дата:** 2026-04-26 **Автор:** svend4 **Редакторская работа:** Claude **Лицензи | `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` |
| `2026-02-01` | и и документацией». Дата документации — 2026-02-01, то есть проект активно развивался около двух-трёх месяцев | `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` |
| `2026-04-26` | 026 **Version:** 1.0.0-draft **Date:** 2026-04-26 **Author:** svend4 **Editorial collaboration:** Claude **Li | `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` |
| `2026-04-26` | а **Версия:** 1.0.0-черновик **Дата:** 2026-04-26 **Автор:** svend4 **Редакторская работа:** Claude **Лицензи | `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` |
| `2026-04-19` | review:** Claude (ассистирующий анализ, 2026-04-19) **Previous version:** [PORTAL-PROTOCOL.md v1.0](https:// | `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` |
| ... | _ещё 2462 записей_ | |


### 133. Точная дата (2492)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `2026 год` | стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: | `docs/01-svyazi/01-executive-summary.md` |
| `2026 год` | реальность восприятия GitHub-профилей в 2026 году. Мой конкретный план consolidation: Archive (выставить Git | `docs/02-anthropic-vacancies/00-intro.md` |
| `2026 год` | ли ваш кейс — единственный в Dresden за 2026 год по очень редкой комбинации (Pflegegrad 2-3 + Persönliches B | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `2026 год` | кла через диалог в нескольких сессиях в 2026 году. Формулировка «Синдром Золушки» и расширение к социальным | `docs/02-anthropic-vacancies/203-благодарности.md` |
| `2025 год` | Кириллом Дьологом сервис «Обучай» летом 2025 года. К апрелю 2026 — 93 тысячи пользователей за семь месяцев . | `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` |
| `2026 год` | ей-пользователей за семь месяцев в 2025-2026 годах), разрабатываем формальную архитектуру и принципы дизайна | `docs/02-anthropic-vacancies/230-аннотация.md` |
| `2025 год` | ля школьных учителей, запущенный осенью 2025 года Константином Чукавиным (тогда 25 лет, учителем и образоват | `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` |
| `2026 год` | з диалог с Claude (Anthropic) 26 апреля 2026 года, инициированный обзором автором русскоязычного интервью с | `docs/02-anthropic-vacancies/244-благодарности.md` |
| `2027 год` | к функциональности Projects через 2026-2027 годы. **GitHub для идей.** GitHub может построить что-то парал | `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` |
| `2026 год` | т . Это значимый gap, учитывая context (2026 год, AI-assisted development является normal). InGit как сейчас | `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` |
| `2026 год` | в Claude Desktop, запущенный в январе 2026 года **Версия:** 1.0.0-черновик **Дата:** 2026-04-26 **Автор:* | `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` |
| `2026 год` | work от Anthropic, запущенной 12 января 2026 года, и её существенном расширении с тех пор. Cowork конкретно | `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` |
| `2026 год` | е туториалы и обзоры Cowork-Project с 2026 года. --- <!-- similar-docs --> --- **Похожие документы:** | `docs/02-anthropic-vacancies/338-ссылки.md` |
| `2026 год` | от Nous Research, выпущенный 25 февраля 2026 года, MIT лицензия. К 23 апреля 2026 (несколько дней назад) — в | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` |
| `2026 год` | х решений для двуязычной документации в 2026 году. Отдельные файлы README.ru.md / README.en.md почти всегда | `docs/02-anthropic-vacancies/69-section.md` |
| `2024 год` | «это решение 2019 года, после изменений 2024 года применяется иначе»); Stability Engine блокирует ложные обо | `docs/04-ai-collaborations/00-intro.md` |
| `2026 год` | earch + model routing. Статья про SVM в 2026 году даёт важный анти-хайповый кубик: для персонализированных р | `docs/04-ai-collaborations/00-intro.md` |
| `2026 год` | стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: | `docs/04-ai-collaborations/01-executive-summary.md` |
| `2026 год` | гим агентом”. Linux Foundation в апреле 2026 года объявила, что A2A стал production‑ready open standard с бо | `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` |
| `2024 год` | «это решение 2019 года, после изменений 2024 года применяется иначе»); - Stability Engine блокирует ложные о | `docs/05-habr-projects/memory/memnet.md` |
| `2024 год` | 00-intro_ - 2019 года, после изменений 2024 года применяется иначе»); _→ 00-intro_ - tree для разрешени | `docs/ACTION_ITEMS.md` |
| `2026 год` | tes / / `2026/04/25` / 7 / dates / / `в 2026 году` / 6 / dates / / `март 2026` / 5 / dates / / `декабрь 2025 | `docs/NAMED_ENTITIES.md` |
| `2026 год` | кла через диалог в нескольких сессиях в 2026 году. Формулировка «Синдром Золушки» и расширение к со… - Бл | `docs/OUTLINE.md` |
| `2026 год` | tes / / `2026/04/25` / 6 / dates / / `в 2026 году` / 5 / dates / / `2026-04-29` / 5 / dates / / `декабрь 202 | `docs/TABLES.md` |
| `2025 год` | ic-vacancies/203-благодарности.md` / / `2025 год` / Кириллом Дьологом сервис «Обучай» летом 2025 года. К апр | `docs/TABLES.md` |
| `2027 год` | ic-vacancies/244-благодарности.md` / / `2027 год` / к функциональности Projects через 2026-2027 годы. **GitH | `docs/TABLES.md` |
| `2024 год` | anthropic-vacancies/69-section.md` / / `2024 год` / «это решение 2019 года, после изменений 2024 года примен | `docs/TABLES.md` |
| `2026 год` | стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: | `docs/obsidian/01-svyazi/01-executive-summary.md` |
| `2026 год` | реальность восприятия GitHub-профилей в 2026 году. Мой конкретный план consolidation: Archive (выставить Git | `docs/obsidian/02-anthropic-vacancies/00-intro.md` |
| `2026 год` | ли ваш кейс — единственный в Dresden за 2026 год по очень редкой комбинации (Pflegegrad 2-3 + Persönliches B | `docs/obsidian/02-anthropic-vacancies/133-обратная-связь.md` |
| ... | _ещё 182 записей_ | |


### 134. Точная дата (2492)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `марта 2026` | Новый Anthropic Institute (объявлен 11 марта 2026): Analyst, Research Economist, Transformative AI Research E | `docs/02-anthropic-vacancies/00-intro.md` |
| `апрель 2026` | claude-sonnet-4-5-20250929 , а сейчас (апрель 2026) актуальны Sonnet 4.6 и Opus 4.7. Это проект, в который сто | `docs/02-anthropic-vacancies/00-intro.md` |
| `декабря 2025` | Самый ранний репозиторий — daten2 , 25 декабря 2025. Самый свежий — data50 , 19 часов назад. Это означает, что | `docs/02-anthropic-vacancies/00-intro.md` |
| `декабрь 2024` | публикацией data70 (где период данных: декабрь 2024 — март 2026, а сам архив выложен 27 марта 2026). Хронологич | `docs/02-anthropic-vacancies/00-intro.md` |
| `март 2026` | ta70 (где период данных: декабрь 2024 — март 2026, а сам архив выложен 27 марта 2026). Хронологически профиль | `docs/02-anthropic-vacancies/00-intro.md` |
| `декабрь 2025` | п и объём. 70 репозиториев за 120 дней (декабрь 2025 — апрель 2026), то есть один репо каждые 1.7 дня. Плюс корп | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `апрель 2026` | епозиториев за 120 дней (декабрь 2025 — апрель 2026), то есть один репо каждые 1.7 дня. Плюс корпус data70 — 11 | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `апрель 2026` | IMPLEMENTATION_STAGE_PART_[1-4].md** (апрель 2026): - Вариант A: ветка `claude/review-nautilus-changes-tdywx | `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` |
| `апреле 2026` | ния к IMPLEMENTATION_STAGE_PART_*.md в апреле 2026. Будущие версии методологии будут задокументированы в этом | `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` |
| `апрель 2026` | одтверждаются: ~440 открытых позиций на апрель 2026 . Цифра, которую вы упомянули, актуальна. Теперь по существ | `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` |
| `май 2025` | am building (статья Mandelbro в Medium, май 2025) Что делает : автор описывает, как он «нанял» LLM в роли ad | `docs/02-anthropic-vacancies/165-closing.md` |
| `феврале 2025` | ндрей независимо реализовал то, о чём в феврале 2025 публикуют academic papers. Где отличается : PURE — про prod | `docs/02-anthropic-vacancies/165-closing.md` |
| `апреля 2026` | ли из разговора с Claude (Anthropic) 19 апреля 2026 года. Автор интегрировал, расширил и сохранил редакторские | `docs/02-anthropic-vacancies/203-благодарности.md` |
| `Сентябрь 2025` | --/ / Лето 2025 / Начало разработки / / Сентябрь 2025 / Публичный запуск / / Апрель 2026 / 93 000 активных учител | `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` |
| `Апрель 2026` | / Сентябрь 2025 / Публичный запуск / / Апрель 2026 / 93 000 активных учителей-пользователей / Рост: с нуля до | `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` |
| `апреля 2026` | ла через диалог с Claude (Anthropic) 26 апреля 2026 года, инициированный обзором автором русскоязычного интервь | `docs/02-anthropic-vacancies/244-благодарности.md` |
| `января 2026` | а в Claude Desktop, которая запущена 12 января 2026 года. Это agentic interface — другая парадигма от Chat. Она | `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` |
| `январе 2026` | ерфейс в Claude Desktop, запущенный в январе 2026 года **Версия:** 1.0.0-черновик **Дата:** 2026-04-26 **Авт | `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` |
| `январе 2026` | формы Cowork от Anthropic (запущенной в январе 2026), предлагает конкретный путь реализации. Мы утверждаем, чт | `docs/02-anthropic-vacancies/325-аннотация.md` |
| `января 2026` | орме Cowork от Anthropic, запущенной 12 января 2026 года, и её существенном расширении с тех пор. Cowork конкр | `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` |
| `февраля 2026` | I-агент от Nous Research, выпущенный 25 февраля 2026 года, MIT лицензия. К 23 апреля 2026 (несколько дней назад) | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` |
| `апреля 2026` | 5 февраля 2026 года, MIT лицензия. К 23 апреля 2026 (несколько дней назад) — версия v0.11.0 с 95 600+ звёзд на | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` |
| `марта 2026` | яние : В активной разработке (статья от марта 2026). Студенческая команда внедряет в ВШЭ. #### Проект 3: Brain | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` |
| `март 2026` | азработка : версии HMP-0001 → HMP-0005 (март 2026, версия 5.0.6) - Документация : kagvi13.github.io/HMP - Бло | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` |
| `декабря 2025` | # AI ассистент для поддержки (статья от декабря 2025) Автор Артём (без полного имени) проектирует AI-ассистента | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` |
| `ноябре 2025` | ion Из найденного: "Проект запустился в ноябре 2025 как Clawdbot, 27 января 2026 переименован в Moltbot, а 30 я | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` |
| `января 2026` | пустился в ноябре 2025 как Clawdbot, 27 января 2026 переименован в Moltbot, а 30 января — в OpenClaw. 14 феврал | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` |
| `апрель 2026` | uthor working projects , недавние (март-апрель 2026), MIT licenses, directly applicable к нашей стек. Они предс | `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` |
| `апрель 2026` | *Объём:** 74 документа (по состоянию на апрель 2026) --- <!-- tags: anthropic --> ## Content Overview **О | `docs/02-anthropic-vacancies/38-content-overview.md` |
| `декабрь 2025` | summary --> > **Создан:** [? уточнить — декабрь 2025, если совпадает с волной --- <!-- tags: anthropic --> | `docs/02-anthropic-vacancies/43-history.md` |
| ... | _ещё 314 записей_ | |


### 135. Точная дата (2492)
_Файл: `docs/TIMELINE.md` | 3 колонок, 6 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/01-svyazi/01-executive-summary.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/04-ai-collaborations/01-executive-summary.md` |
| `первые месяцы 2026` | `2026 год` / стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/TABLES.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/obsidian/01-svyazi/01-executive-summary.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/obsidian/04-ai-collaborations/01-executive-summary.md` |
| `первые месяцы 2026` | `2026 год` / стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/obsidian/TABLES.md` |


### 136. Точная дата (2492)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `Фаза 1` | еет smoke-test: завершена или нет. #### Фаза 1 — Спецификация (неделя 1) Deliverables: - PORTAL-PROTOCOL.m | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `Фаза 2` | епо без задавания вопросов автору? #### Фаза 2 — Reference implementation (неделя 2–3) Deliverables: - Bas | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `Фаза 3` | результат с consensus-информацией? #### Фаза 3 — MCP интерфейс (неделя 3, параллельно) Deliverables: - por | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `Фаза 4` | osmыслený ответ с указанием репо. #### Фаза 4 — Web interface и публичная видимость (неделя 4) Deliverabl | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `Фаза 5` | учить отформатированный результат. #### Фаза 5 — Публикация и адаптация (неделя 5+) Deliverables: - Arxiv | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `Фаза 1` | , вот как это может выглядеть поэтапно: Фаза 1 — Proof of Concept (2 недели). Создать legal-nautilus как f | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `Фаза 2` | щий MCP server с одним legal-адаптером. Фаза 2 — Multiple Legal Sources (4 недели). Расширить до 4-5 адапт | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `Фаза 3` | й demo на конкретных социальных кейсах. Фаза 3 — Private Case Files (4 недели). Добавить адаптеры для ваши | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `Фаза 4` | в реальной работе над S 6 SO 58/26 ER. Фаза 4 — Extension to General Humanities (ongoing). Добавить адапт | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `Фаза 5` | l", а humanities knowledge federation . Фаза 5 — Public Launch & Grant Applications (после Фазы 3). Paper | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `Phase 1` | nimizes risk и maximizes learning. #### Phase 1 — Information work (months 1-6) Simple journalism / researc | `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` |
| `Phase 2` | routing (минимальный, но symbolic) #### Phase 2 — Specialized journalism (months 6-12) Contributors who dem | `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` |
| `Phase 3` | ers, Nautilus Medical Translators. #### Phase 3 — Amateur projects (year 2) Contributors начинают initiatin | `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` |
| `Phase 4` | , accumulated knowledge compounds. #### Phase 4 — Specialized projects (year 2-3) Structured professional e | `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` |
| `Phase 5` | structure becomes self-sustaining. #### Phase 5 — Integration with existing ecosystems (year 3+) Integratio | `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` |
| `Phase 1` | l: €12.3M ### 5.3. Funding Strategy **Phase 1 (months 1-6)**: Secure anchor partnership (€2-3M commitmen | `docs/02-anthropic-vacancies/159-5-economic-model.md` |
| `Phase 2` | ion alignment and existing programs. **Phase 2 (months 3-9, overlapping)**: Secure secondary partnerships | `docs/02-anthropic-vacancies/159-5-economic-model.md` |
| `Phase 3` | ant (EIC Pathfinder, Horizon Europe) **Phase 3 (months 6-18)**: Launch commercial project revenue stream. | `docs/02-anthropic-vacancies/159-5-economic-model.md` |
| `Phase 4` | revenue scaling to €2M+ in Year 3. **Phase 4 (Year 2-3)**: Develop endowment through success-contingent | `docs/02-anthropic-vacancies/159-5-economic-model.md` |
| `Phase 0` | Plan](#7-phased-rollout-plan) - [7.1. Phase 0: Foundation and Funding (Months 1-6)](#71-phase-0-foundatio | `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` |
| `Phase 1` | ation-and-funding-months-1-6) - [7.2. Phase 1: Infrastructure and First Cohort (Months 6-18)](#72-phase-1 | `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` |
| `Phase 2` | and-first-cohort-months-6-18) - [7.3. Phase 2: Scale and Diversification (Months 18-36)](#73-phase-2-scal | `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` |
| `Phase 3` | diversification-months-18-36) - [7.4. Phase 3: Consolidation and Self-Sustaining Operations](#74-phase-3- | `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` |
| `Phase 1` | gations**: - Aggressive outreach during Phase 1 recruitment - Partnership with existing advocacy organizati | `docs/02-anthropic-vacancies/162-8-risk-analysis.md` |
| `Phase 1` | — conservative by foundation standards Phase 1 (50 contributors, year 1), Phase 2 (500, year 2), Phase 3 ( | `docs/02-anthropic-vacancies/165-closing.md` |
| `Phase 2` | ards Phase 1 (50 contributors, year 1), Phase 2 (500, year 2), Phase 3 (5000, year 3) — это conservative gr | `docs/02-anthropic-vacancies/165-closing.md` |
| `Phase 3` | butors, year 1), Phase 2 (500, year 2), Phase 3 (5000, year 3) — это conservative growth . Many foundation | `docs/02-anthropic-vacancies/165-closing.md` |
| `Phase 0` | ](#9-phased-rollout-strategy) - [9.1. Phase 0 — Foundation (Months 1-12)](#91-phase-0-foundation-months-1 | `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` |
| `Phase 1` | ase-0-foundation-months-1-12) - [9.2. Phase 1 — Single Domain Maturation (Year 2)](#92-phase-1-single-dom | `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` |
| `Phase 2` | gle-domain-maturation-year-2) - [9.3. Phase 2 — Domain Expansion (Years 3-4)](#93-phase-2-domain-expansio | `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` |
| ... | _ещё 630 записей_ | |


### 137. Точная дата (2492)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `2–3 дня` | uth и трассируемый lifecycle карточки / 2–3 дня / / Ingest и память / LLM[^llm] extraction + нормализация + | `docs/01-svyazi/07-mvp-planning.md` |
| `4–6 дне` | получаются устойчивые профили и связи / 4–6 дней / / Evidence / LiteParse/research-docs + page‑level viewer | `docs/01-svyazi/07-mvp-planning.md` |
| `3–4 дня` | показать match, а показать основание / 3–4 дня / / Исполнение / LiteLLM/Auto AI Router + Tool Search + баз | `docs/01-svyazi/07-mvp-planning.md` |
| `1–2 дня` | / Снизить риск ложных связей и утечек / 1–2 дня / **Итого**: реалистичный MVP — **12–18 инженерных дней** | `docs/01-svyazi/07-mvp-planning.md` |
| `1–2 недели` | ge/span evidence + manual reviewer UI / 1–2 недели / Переусложнение схемы слишком рано / / Memory governance / | `docs/01-svyazi/12-roadmap.md` |
| `2–3 недели` | ому. daten — стратегический, но требует 2–3 недели работы на пивот и ребрендинг. Отложить до окончания работы | `docs/02-anthropic-vacancies/00-intro.md` |
| `1-2 дня` | ый в своей горячей нише. Каждый требует 1-2 дня на English README + demo + опубликовать пост в /r/LocalLLaM | `docs/02-anthropic-vacancies/00-intro.md` |
| `30-45 дне` | иля. ### Итоговая целевая картина Через 30-45 дней вашего собранного времени GitHub-профиль должен состоять и | `docs/02-anthropic-vacancies/00-intro.md` |
| `6-12 месяце` | которые берут нестандартных одиночек на 6-12 месяцев, обучают, иногда принимают в штат. Гибридная модель, но вс | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `2-3 месяца` | знают друг друга, будут тратить первые 2-3 месяца на выстраивание взаимопонимания и распределения ответственн | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `3-6 месяце` | 5 человек), команды работают независимо 3-6 месяцев, агент модерирует прогресс и помогает с координацией внутр | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `1-2 дня` | vend4. Это zero-cost действие, занимает 1-2 дня, и делает одну важную вещь — создаёт intellectual footprint | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `2-3 дня` | екст проекта и вводит нового человека в 2-3 дня. Natural fit для inclusive work. Люди с health limitations, | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `4-6 недель` | ropic или Mistral). Proposal пишется за 4-6 недель, шанс 15-25%. Максимальная — founder track . Построить это | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `1-2 недели` | уровня 50), средние (implement feature, 1-2 недели, XP и currency), эпические (прорывной проект на 6 месяцев, | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `2-3 месяца` | реально использовать для работы. Через 2-3 месяца практики станет ясно, какие paттерны и инструменты действит | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `1-2 месяца` | ость, которая имеет смысл: Первый этап (1-2 месяца) — закрепить core Nautilus v1.1, написать PORTAL-PROTOCOL-H | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `3-4 месяца` | ет для реального use case. Третий этап (3-4 месяца) — расширить legal до 5-7 adapters (SGB, SGG, openJur, BSG, | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `12-18 месяце` | ой план: это не спринт, это marathon на 12-18 месяцев . Реалистично для single person с Claude Code assistance — | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `2-3 дня` | екст проекта и вводит нового человека в 2-3 дня. **Natural fit для inclusive work.** Люди с health limitati | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `3-6 месяце` | **работающий документированный кейс**. 3-6 месяцев, €20-50K. Это становится вашей reference implementation и | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `4-6 недель` | ropic или Mistral). Proposal пишется за 4-6 недель, шанс 15-25%. **Максимальная — founder track**. Построить э | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `6-12 месяце` | y growth → first external contributors (6-12 месяцев) → maybe eventual formalization как RFC or standard (12-24 | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `12-24 месяца` | tual formalization как RFC or standard (12-24 месяца). Upside: minimal upfront cost, organic growth, maintains a | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `6-12 месяце` | H-1B — лотерея. EU Blue Card — занимает 6-12 месяцев. Передача работника без юридической поддержки — почти нево | `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` |
| `2-3 месяца` | ический onboarding в Anthropic занимает 2-3 месяца. Для distributed/part-time/contract workers это неприемлемо | `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` |
| `6-12 месяце` | end, AI integration, design, product) - 6-12 месяцев до viable MVP - $500K-1.5M первого года - И главное — clea | `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` |
| `10-16 месяце` | ompose, документацию, план реализации в 10-16 месяцев, technological stack уже выбран (Python 3.11, FastAPI, pyg | `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` |
| `3-6 месяце` | ии InGit до работающего MVP в следующие 3-6 месяцев. Семь документов Nautilus/OKWF могут жить в обычном GitHub | `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` |
| `2-4 недели` | ble ingit-mcp-server с 8-12 tools — это 2-4 недели work для experienced Python developer, после того как InGit | `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` |
| ... | _ещё 406 записей_ | |


### 138. Точная дата (2492)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `версия 0.1.5` | 3view4turn27view0 / Рабочий прототип, версия 0.1.5; “рабочая, но не финальная”. citeturn33view7 / **Очень в | `docs/01-svyazi/03-component-catalog.md` |
| `v4.5` | латформы : 87 skills, chat-migration v1→v4.5 quantum-hybrid, Multi-Chat Orchestrator, xMemory-архитектур | `docs/02-anthropic-vacancies/00-intro.md` |
| `v1.0` | rlängerung/Nachzahlung), Master Dossier v1.0, анализ BSG-практики, анализ Kostenschieberei. То есть это | `docs/02-anthropic-vacancies/00-intro.md` |
| `v1.0` | ая архитектурная спецификация протокола v1.0 — и она существенно сильнее , чем я реконструировал в преды | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `v1.0` | 112 строк) — архитектурная спецификация v1.0 с философией federation-over-merging, триадой info1/pro2/me | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `v1.1` | Как версионируется сам протокол (v1.0, v1.1, breaking changes policy) Ключевой принцип слоя 0 : специфи | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `v2.0` | ng — это отдельный extension протокола (v2.0 или как опциональное расширение), не меняющее read-path. Пр | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `v1.0.0` | ый релиз — git tag + CHANGELOG. Semver: v1.0.0, v1.0.1, v1.1.0. CHANGELOG.md в корне. Контакт с MCP Regist | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `v1.0.1` | — git tag + CHANGELOG. Semver: v1.0.0, v1.0.1, v1.1.0. CHANGELOG.md в корне. Контакт с MCP Registry и Ant | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `v1.1.0` | ag + CHANGELOG. Semver: v1.0.0, v1.0.1, v1.1.0. CHANGELOG.md в корне. Контакт с MCP Registry и Anthropic c | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
| `v1.1` | ed-expe.md) _53%_ - [PORTAL-PROTOCOL.md v1.1](obsidian/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md) _53%_ - [A Formal Model for | `docs/02-anthropic-vacancies/03-portal-protocol-md.md` |
| `v0.2.0` | l-working-example.md) _33%_ - [Planned (v0.2.0)](obsidian/02-anthropic-vacancies/132-planned-v0-2-0.md) _29%_ - [0. Status of This Documen | `docs/02-anthropic-vacancies/04-abstract.md` |
| `v1.0` | бочий черновик Nautilus Portal Protocol v1.0. Он может --- <!-- tags: collaboration --> ## 0. Statu | `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` |
| `v1.0.0` | может изменяться до объявления stable v1.0.0. Breaking changes после stable потребуют bump до v2.0 с mi | `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` |
| `v2.0` | changes после stable потребуют bump до v2.0 с migration guide. Комментарии и предложения — через Issue | `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` |
| `v1.0` | ations в федерируемые репо (read-only в v1.0) ### 1.4. Terminology Ключевые термины определены в разде | `docs/02-anthropic-vacancies/06-1-introduction.md` |
| `v1.0` | col_version` — строка в формате semver. v1.0 совместимо с минорными обновлениями. - `ecosystem_name` | `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` |
| `v0.2.0` | sport-passport-md.md) _29%_ - [Planned (v0.2.0)](obsidian/02-anthropic-vacancies/132-planned-v0-2-0.md) _25%_ - [10. QueryResult Structure | `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` |
| `v1.1.0` | hange Log](#appendix-b-change-log) - [v1.1.0-draft (2026-04-19)](#v110-draft-2026-04-19) - [v1.0.0-dra | `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` |
| `v1.0.0` | 26-04-19)](#v110-draft-2026-04-19) - [v1.0.0-draft (2026-04 earlier)](#v100-draft-2026-04-earlier) <!- | `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` |
| `v3.1.0` | uirement Levels - OpenAPI Specification v3.1.0 (for REST API schemas) - JSON Schema (for passport validati | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v1.1.0` | --- *End of Nautilus Portal Protocol v1.1.0-draft* *Feedback, issues, proposals: [github.com/svend4/n | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v1.0` | ворить отдельно. #### Что я сохранил из v1.0 Базовая структура, нумерация разделов (1–15 из v1.0 осталис | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v1.1` | и у кого-то есть v1.0, они могут читать v1.1 параллельно — те же разделы говорят о том же, плюс новые. # | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v1.2` | ого. #### Что я сознательно оставил для v1.2 или v2.0 Formal bridge algebra. Part 3 implementation docs | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v2.0` | Что я сознательно оставил для v1.2 или v2.0 Formal bridge algebra. Part 3 implementation docs указывает | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v3.0` | l header 7. Добавить changelog-запись: «v3.0 consolidated from A (branch X) and B (branch Y) on YYYY | `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` |
| `v1.1` | еграция с Nautilus Portal Protocol NPP v1.1 §17.3 «Breaking Changes Process» упоминает RFC-процесс для | `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` |
| `v2.0` | одология может быть формализована в NPP v2.0 как рекомендованный workflow для community-contributed doc | `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` |
| `v1.0` | x C: История изменений методологии ### v1.0 (2026-04) Первая формализация, основана на опыте применени | `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` |
| ... | _ещё 1158 записей_ | |


### 139. Топ уникальных слов по темам
_Файл: `docs/TOPIC_MODEL.md` | 6 колонок, 6 строк_

| Тема | Слово 1 | Слово 2 | Слово 3 | Слово 4 | Слово 5 |
|------|---------|---------|---------|---------|---------|
| turn, view, cite | turn | appendix | svyazi | view | portal |
| cowork, ingit, compo | cowork | ingit | agent | composite | agents |
| middle, ensembl, lay | layer | chat | middle | missing | between |
| агент, совместной, к | агенты | коллеги | профессиональные | благодарности | совместной |
| compatibility, level | compatibility | level | bridges | history | format |
| слов, файлов, файлы | слов | файлов | тегов | callout | summary |


### 140. Сводка
_Файл: `docs/VALIDATION.md` | 3 колонок, 6 строк_

| Проверка | Статус | Проблем |
|----------|--------|---------|
| Разделы и README | ✅ | 0 |
| Мета-файлы | ✅ | 0 |
| Пустые/короткие файлы | ⚠️ | 6 |
| Именование файлов | ✅ | 10 |
| Заголовки H1 | ⚠️ | 11 |
| Внутренние ссылки | ✅ | 15 |


### 141. 📝 Изменённые файлы (16)
_Файл: `docs/VERSION_DIFF.md` | 4 колонок, 16 строк_

| Файл | Δ слов | Добавленные темы | Удалённые темы |
|------|--------|------------------|----------------|
| `docs/TIMELINE.md` | -2390 | 2020 (2 упоминаний), 2021 (1 упоминаний), 2022 (5 упоминаний) +7 | Версия (394), Год (27), Длительность (95) +6 |
| `docs/SEARCH.md` | +316 | — | — |
| `docs/BROKEN_LINKS.md` | +273 | Внешние URL (129 уникальных) | Внешние URL (113 уникальных) |
| `docs/DUPLICATES.md` | +81 | 50% — `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` vs `docs/01-svyazi/06-security-privacy.md`, 50% — `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` vs `docs/01-svyazi/12-roadmap.md` | — |
| `docs/PROGRESS.md` | -26 | Метрики качества, Приоритет 1: kksudo (AgentFS, 13 упоминаний), Приоритет 2: spbmolot (NGT Memory, 12 упоминаний) +3 | Ближайшие задачи (открытые чеклисты), Чеклисты по фазам |
| `docs/05-habr-projects/memory/memnet.md` | +22 | Статус | — |
| `docs/05-habr-projects/memory/ngt-memory.md` | +22 | Статус | — |
| `docs/05-habr-projects/memory/yodoca.md` | +22 | Статус | — |
| `docs/METRICS.md` | -22 | — | — |
| `docs/04-ai-collaborations/00-intro.md` | +16 | Статус | — |
| `docs/04-ai-collaborations/01-executive-summary.md` | +16 | Статус | — |
| `docs/05-habr-projects/01-synthesis.md` | +16 | Статус | — |
| `docs/05-habr-projects/02-collaboration-partners.md` | +16 | Статус | — |
| `docs/05-habr-projects/knowledge/wikontic.md` | +16 | Статус | — |
| `docs/HEALTH.md` | -13 | — | — |
| `docs/CONTACTS.md` | -9 | — | — |


### 142. Корпусная статистика
_Файл: `docs/VOCABULARY.md` | 2 колонок, 5 строк_

| Метрика | Значение |
|---------|----------|
| Средний TTR | 0.434 |
| Средний STTR (100-токенное окно) | 0.589 |
| Lexical density | 0.835 |
| Средняя длина слова | 6.58 |
| Общая оценка | 🟠 Бедный |


### 143. Топ файлов по богатству словаря (STTR)
_Файл: `docs/VOCABULARY.md` | 6 колонок, 30 строк_

| Файл | STTR | TTR | Hapax% | Lex.Density | Токенов |
|------|------|-----|--------|-------------|---------|
| `ABBREVIATIONS.md` | 0.940 | 0.717 | 75% | 0.875 | 835 |
| `HEALTH.md` | 0.909 | 0.909 | 90% | 0.955 | 66 |
| `ENTITIES.md` | 0.880 | 0.609 | 78% | 0.957 | 161 |
| `194-4-десять-областей-применения.md` | 0.874 | 0.556 | 70% | 0.915 | 1459 |
| `00-intro.md` | 0.856 | 0.370 | 60% | 0.870 | 10587 |
| `01-интегральный-анализ-профиля-svend4.md` | 0.850 | 0.332 | 60% | 0.831 | 17176 |
| `238-7-области-применения.md` | 0.847 | 0.607 | 70% | 0.944 | 629 |
| `14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 0.840 | 0.462 | 65% | 0.884 | 3237 |
| `STATS.md` | 0.840 | 0.840 | 88% | 0.934 | 106 |
| `memnet.md` | 0.836 | 0.399 | 61% | 0.866 | 6697 |
| `189-аннотация.md` | 0.830 | 0.713 | 76% | 0.840 | 275 |
| `192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | 0.830 | 0.620 | 76% | 0.885 | 786 |
| `165-closing.md` | 0.825 | 0.412 | 63% | 0.814 | 6087 |
| `239-8-пилотное-предложение-sgb-колega-адвокат.md` | 0.824 | 0.617 | 73% | 0.899 | 799 |
| `00-intro.md` | 0.822 | 0.396 | 64% | 0.859 | 7760 |
| `72-расписание-фазы-3.md` | 0.822 | 0.604 | 74% | 0.842 | 671 |
| `357-твоя-коммуникация-в-outreach.md` | 0.820 | 0.720 | 78% | 0.850 | 193 |
| `DECISIONS.md` | 0.817 | 0.564 | 73% | 0.864 | 1609 |
| `207-приложение-c-образцы-случаев-использования-в-детал.md` | 0.812 | 0.507 | 68% | 0.846 | 2290 |
| `DEPENDABOT.md` | 0.810 | 0.810 | 81% | 0.914 | 58 |
| `359-твои-anti-patterns.md` | 0.810 | 0.660 | 66% | 0.846 | 162 |
| `365-развёрнутый-анализ-внуковой-комбинации.md` | 0.810 | 0.399 | 59% | 0.859 | 3565 |
| `235-4-архитектура-профессиональных-коллег-агентов.md` | 0.807 | 0.601 | 73% | 0.893 | 785 |
| `191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | 0.805 | 0.637 | 76% | 0.843 | 650 |
| `272-appendix-d-connection-diagram.md` | 0.805 | 0.429 | 64% | 0.808 | 3465 |
| `173-4-ten-domains-of-application.md` | 0.805 | 0.418 | 59% | 0.856 | 1556 |
| `248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | 0.804 | 0.450 | 66% | 0.856 | 2999 |
| `02-общий-план-развития-nautilus-portal-protocol.md` | 0.802 | 0.468 | 67% | 0.845 | 2142 |
| `150-appendix-c-version-history.md` | 0.802 | 0.409 | 60% | 0.839 | 4478 |
| `SENTIMENT.md` | 0.800 | 0.675 | 81% | 0.899 | 169 |


### 144. Файлы с бедным словарём (требуют доработки)
_Файл: `docs/VOCABULARY.md` | 4 колонок, 30 строк_

| Файл | STTR | Оценка | Токенов |
|------|------|--------|---------|
| `28-appendix-a-minimal-working-example.md` | 0.270 | 🔴 Очень бедный | 213 |
| `README.md` | 0.273 | 🔴 Очень бедный | 77 |
| `BROKEN_LINKS.md` | 0.273 | 🔴 Очень бедный | 783 |
| `README.md` | 0.275 | 🔴 Очень бедный | 51 |
| `305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | 0.280 | 🔴 Очень бедный | 221 |
| `249-composite-skills-agent-md.md` | 0.305 | 🔴 Очень бедный | 249 |
| `.md` | 0.305 | 🔴 Очень бедный | 95 |
| `svyazi.md` | 0.312 | 🔴 Очень бедный | 93 |
| `svend4.md` | 0.312 | 🔴 Очень бедный | 93 |
| `sgb.md` | 0.312 | 🔴 Очень бедный | 93 |
| `nautilus.md` | 0.312 | 🔴 Очень бедный | 93 |
| `lorenzo.md` | 0.312 | 🔴 Очень бедный | 93 |
| `ingit.md` | 0.312 | 🔴 Очень бедный | 93 |
| `cowork.md` | 0.312 | 🔴 Очень бедный | 93 |
| `273-infrastructure-for-ai-collaborative-intellectual-w.md` | 0.320 | 🔴 Очень бедный | 251 |
| `README.md` | 0.323 | 🔴 Очень бедный | 65 |
| `27-15-glossary-of-examples.md` | 0.325 | 🔴 Очень бедный | 208 |
| `DEPENDENCY_MAP.md` | 0.328 | 🔴 Очень бедный | 848 |
| `CITATION_INDEX.md` | 0.328 | 🔴 Очень бедный | 453 |
| `304-ingit-as-cowork-native-workspace-substrate-md.md` | 0.330 | 🔴 Очень бедный | 249 |
| `187-слой-представительских-агентов-md.md` | 0.330 | 🔴 Очень бедный | 250 |
| `169-table-of-contents.md` | 0.330 | 🔴 Очень бедный | 216 |
| `151-open-knowledge-work-foundation-md.md` | 0.330 | 🔴 Очень бедный | 247 |
| `134-the-double-triangle-architecture-md.md` | 0.330 | 🔴 Очень бедный | 247 |
| `13-angle-perspective.md` | 0.330 | 🔴 Очень бедный | 185 |
| `CROSSREFS.md` | 0.331 | 🔴 Очень бедный | 825 |
| `42-author-contact.md` | 0.335 | 🔴 Очень бедный | 201 |
| `166-representative-agent-layer-md.md` | 0.335 | 🔴 Очень бедный | 255 |
| `123-portal-mcp-py.md` | 0.340 | 🔴 Очень бедный | 232 |
| `105-review-methodology-md.md` | 0.340 | 🔴 Очень бедный | 200 |


### 145. Топ-20 слов
_Файл: `docs/WORD_CLOUD.md` | 3 колонок, 20 строк_

| # | Слово | Частота |
|---|-------|---------|
| 1 | **anthropic** | 5,050 |
| 2 | **vacancies** | 4,506 |
| 3 | **agent** | 1,422 |
| 4 | **turn** | 1,376 |
| 5 | **svyazi** | 1,039 |
| 6 | **сходство** | 1,007 |
| 7 | **view** | 973 |
| 8 | **cowork** | 926 |
| 9 | **nautilus** | 912 |
| 10 | **appendix** | 822 |
| 11 | **ingit** | 776 |
| 12 | **agents** | 701 |
| 13 | **knowledge** | 691 |
| 14 | **portal** | 659 |
| 15 | **protocol** | 617 |
| 16 | **search** | 604 |
| 17 | **document** | 599 |
| 18 | **memory** | 591 |
| 19 | **lorenzo** | 557 |
| 20 | **claude** | 556 |


### 146. Глобальный топ-50 слов
_Файл: `docs/WORD_FREQ.md` | 4 колонок, 50 строк_

| # | Слово | Частота | Визуализация |
|---|-------|---------|-------------|
| 1 | **anthropic** | 12,860 | `████████████████████` |
| 2 | **vacancies** | 10,863 | `████████████████░░░░` |
| 3 | **agent** | 3,625 | `█████░░░░░░░░░░░░░░░` |
| 4 | **svyazi** | 3,258 | `█████░░░░░░░░░░░░░░░` |
| 5 | **appendix** | 3,229 | `█████░░░░░░░░░░░░░░░` |
| 6 | **проблем** | 3,202 | `████░░░░░░░░░░░░░░░░` |
| 7 | **документы** | 3,028 | `████░░░░░░░░░░░░░░░░` |
| 8 | **turn** | 2,944 | `████░░░░░░░░░░░░░░░░` |
| 9 | **cowork** | 2,678 | `████░░░░░░░░░░░░░░░░` |
| 10 | **nautilus** | 2,513 | `███░░░░░░░░░░░░░░░░░` |
| 11 | **ingit** | 2,353 | `███░░░░░░░░░░░░░░░░░` |
| 12 | **mcp** | 2,172 | `███░░░░░░░░░░░░░░░░░` |
| 13 | **view** | 2,159 | `███░░░░░░░░░░░░░░░░░` |
| 14 | **мин** | 2,009 | `███░░░░░░░░░░░░░░░░░` |
| 15 | **knowledge** | 1,964 | `███░░░░░░░░░░░░░░░░░` |
| 16 | **упоминается** | 1,890 | `██░░░░░░░░░░░░░░░░░░` |
| 17 | **readme** | 1,876 | `██░░░░░░░░░░░░░░░░░░` |
| 18 | **связанные** | 1,860 | `██░░░░░░░░░░░░░░░░░░` |
| 19 | **сходство** | 1,860 | `██░░░░░░░░░░░░░░░░░░` |
| 20 | **agents** | 1,841 | `██░░░░░░░░░░░░░░░░░░` |
| 21 | **слов** | 1,740 | `██░░░░░░░░░░░░░░░░░░` |
| 22 | **анализ** | 1,734 | `██░░░░░░░░░░░░░░░░░░` |
| 23 | **сложный** | 1,676 | `██░░░░░░░░░░░░░░░░░░` |
| 24 | **portal** | 1,614 | `██░░░░░░░░░░░░░░░░░░` |
| 25 | **what** | 1,540 | `██░░░░░░░░░░░░░░░░░░` |
| 26 | **быстро** | 1,538 | `██░░░░░░░░░░░░░░░░░░` |
| 27 | **document** | 1,535 | `██░░░░░░░░░░░░░░░░░░` |
| 28 | **layer** | 1,492 | `██░░░░░░░░░░░░░░░░░░` |
| 29 | **contents** | 1,482 | `██░░░░░░░░░░░░░░░░░░` |
| 30 | **protocol** | 1,465 | `██░░░░░░░░░░░░░░░░░░` |
| 31 | **lorenzo** | 1,443 | `██░░░░░░░░░░░░░░░░░░` |
| 32 | **начало** | 1,442 | `██░░░░░░░░░░░░░░░░░░` |
| 33 | **memory** | 1,429 | `██░░░░░░░░░░░░░░░░░░` |
| 34 | **claude** | 1,422 | `██░░░░░░░░░░░░░░░░░░` |
| 35 | **work** | 1,399 | `██░░░░░░░░░░░░░░░░░░` |
| 36 | **architecture** | 1,393 | `██░░░░░░░░░░░░░░░░░░` |
| 37 | **open** | 1,389 | `██░░░░░░░░░░░░░░░░░░` |
| 38 | **search** | 1,281 | `█░░░░░░░░░░░░░░░░░░░` |
| 39 | **infrastructure** | 1,234 | `█░░░░░░░░░░░░░░░░░░░` |
| 40 | **содержание** | 1,171 | `█░░░░░░░░░░░░░░░░░░░` |
| 41 | **sgb** | 1,159 | `█░░░░░░░░░░░░░░░░░░░` |
| 42 | **svend** | 1,152 | `█░░░░░░░░░░░░░░░░░░░` |
| 43 | **агентов** | 1,149 | `█░░░░░░░░░░░░░░░░░░░` |
| 44 | **collaborations** | 1,145 | `█░░░░░░░░░░░░░░░░░░░` |
| 45 | **документ** | 1,071 | `█░░░░░░░░░░░░░░░░░░░` |
| 46 | **cite** | 1,056 | `█░░░░░░░░░░░░░░░░░░░` |
| 47 | **professional** | 1,052 | `█░░░░░░░░░░░░░░░░░░░` |
| 48 | **приложение** | 1,051 | `█░░░░░░░░░░░░░░░░░░░` |
| 49 | **абзац** | 1,048 | `█░░░░░░░░░░░░░░░░░░░` |
| 50 | **colleague** | 1,040 | `█░░░░░░░░░░░░░░░░░░░` |


### 147. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **turn** | 451 | `███████████████` |
| **view** | 310 | `██████████░░░░░` |
| **cite** | 155 | `█████░░░░░░░░░░` |
| **search** | 153 | `█████░░░░░░░░░░` |
| **svyazi** | 137 | `████░░░░░░░░░░░` |
| **collaborations** | 100 | `███░░░░░░░░░░░░` |
| **memory** | 84 | `██░░░░░░░░░░░░░` |
| **проект** | 72 | `██░░░░░░░░░░░░░` |
| **rag** | 68 | `██░░░░░░░░░░░░░` |
| **ансамбли** | 67 | `██░░░░░░░░░░░░░` |
| **oss** | 66 | `██░░░░░░░░░░░░░` |
| **mcp** | 52 | `█░░░░░░░░░░░░░░` |
| **документы** | 50 | `█░░░░░░░░░░░░░░` |
| **agentfs** | 48 | `█░░░░░░░░░░░░░░` |
| **прототипа** | 45 | `█░░░░░░░░░░░░░░` |


### 148. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **agent** | 1256 | `███████████████` |
| **cowork** | 979 | `███████████░░░░` |
| **nautilus** | 868 | `██████████░░░░░` |
| **appendix** | 830 | `█████████░░░░░░` |
| **ingit** | 824 | `█████████░░░░░░` |
| **сходство** | 812 | `█████████░░░░░░` |
| **документы** | 776 | `█████████░░░░░░` |
| **agents** | 732 | `████████░░░░░░░` |
| **anthropic** | 731 | `████████░░░░░░░` |
| **work** | 593 | `███████░░░░░░░░` |
| **what** | 578 | `██████░░░░░░░░░` |
| **portal** | 561 | `██████░░░░░░░░░` |
| **layer** | 553 | `██████░░░░░░░░░` |
| **document** | 530 | `██████░░░░░░░░░` |
| **lorenzo** | 524 | `██████░░░░░░░░░` |


### 149. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **first** | 26 | `███████████████` |
| **agent** | 25 | `██████████████░` |
| **legal** | 24 | `█████████████░░` |
| **local** | 24 | `█████████████░░` |
| **knowledge** | 24 | `█████████████░░` |
| **habr** | 19 | `██████████░░░░░` |
| **articles** | 17 | `█████████░░░░░░` |
| **комбинация** | 16 | `█████████░░░░░░` |
| **graphs** | 14 | `████████░░░░░░░` |
| **graph** | 14 | `████████░░░░░░░` |
| **svyazi** | 14 | `████████░░░░░░░` |
| **router** | 13 | `███████░░░░░░░░` |
| **benchmarks** | 13 | `███████░░░░░░░░` |
| **rag** | 13 | `███████░░░░░░░░` |
| **граф** | 12 | `██████░░░░░░░░░` |


### 150. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **turn** | 557 | `███████████████` |
| **view** | 400 | `██████████░░░░░` |
| **svyazi** | 293 | `███████░░░░░░░░` |
| **search** | 192 | `█████░░░░░░░░░░` |
| **cite** | 172 | `████░░░░░░░░░░░` |
| **memory** | 169 | `████░░░░░░░░░░░` |
| **mcp** | 140 | `███░░░░░░░░░░░░` |
| **rag** | 131 | `███░░░░░░░░░░░░` |
| **проект** | 113 | `███░░░░░░░░░░░░` |
| **llm** | 99 | `██░░░░░░░░░░░░░` |
| **knowledge** | 92 | `██░░░░░░░░░░░░░` |
| **слой** | 88 | `██░░░░░░░░░░░░░` |
| **oss** | 83 | `██░░░░░░░░░░░░░` |
| **evidence** | 77 | `██░░░░░░░░░░░░░` |
| **статус** | 75 | `██░░░░░░░░░░░░░` |


### 151. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **llm** | 64 | `███████████████` |
| **пара** | 63 | `██████████████░` |
| **memory** | 62 | `██████████████░` |
| **yodoca** | 55 | `████████████░░░` |
| **mcp** | 54 | `████████████░░░` |
| **ngt** | 35 | `████████░░░░░░░` |
| **legal** | 35 | `████████░░░░░░░` |
| **каждый** | 31 | `███████░░░░░░░░` |
| **проекты** | 29 | `██████░░░░░░░░░` |
| **wikontic** | 27 | `██████░░░░░░░░░` |
| **svyazi** | 27 | `██████░░░░░░░░░` |
| **claude** | 27 | `██████░░░░░░░░░` |
| **readme** | 25 | `█████░░░░░░░░░░` |
| **habr** | 25 | `█████░░░░░░░░░░` |
| **self** | 25 | `█████░░░░░░░░░░` |


### 152. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **svyazi** | 51 | `███████████████` |
| **cowork** | 35 | `██████████░░░░░` |
| **ingit** | 35 | `██████████░░░░░` |
| **lorenzo** | 35 | `██████████░░░░░` |
| **nautilus** | 29 | `████████░░░░░░░` |
| **sgb** | 21 | `██████░░░░░░░░░` |
| **kksudo** | 21 | `██████░░░░░░░░░` |
| **компонент** | 20 | `█████░░░░░░░░░░` |
| **экосистемы** | 20 | `█████░░░░░░░░░░` |
| **spbmolot** | 19 | `█████░░░░░░░░░░` |
| **описание** | 13 | `███░░░░░░░░░░░░` |
| **связанные** | 11 | `███░░░░░░░░░░░░` |
| **документы** | 11 | `███░░░░░░░░░░░░` |
| **антропик** | 10 | `██░░░░░░░░░░░░░` |
| **проекты** | 10 | `██░░░░░░░░░░░░░` |


### 153. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **badges** | 15 | `███████████████` |
| **svg** | 14 | `██████████████░` |
| **words** | 3 | `███░░░░░░░░░░░░` |
| **scripts** | 3 | `███░░░░░░░░░░░░` |
| **health** | 3 | `███░░░░░░░░░░░░` |
| **license** | 3 | `███░░░░░░░░░░░░` |
| **branch** | 3 | `███░░░░░░░░░░░░` |
| **бейджи** | 2 | `██░░░░░░░░░░░░░` |
| **scoring** | 2 | `██░░░░░░░░░░░░░` |
| **репозитория** | 1 | `█░░░░░░░░░░░░░░` |
| **автоматически** | 1 | `█░░░░░░░░░░░░░░` |
| **генерируются** | 1 | `█░░░░░░░░░░░░░░` |
| **скриптом** | 1 | `█░░░░░░░░░░░░░░` |
| **improve** | 1 | `█░░░░░░░░░░░░░░` |
| **текущие** | 1 | `█░░░░░░░░░░░░░░` |


### 154. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **контакт** | 126 | `███████████████` |
| **статус** | 70 | `████████░░░░░░░` |
| **связи** | 70 | `████████░░░░░░░` |
| **профиль** | 56 | `██████░░░░░░░░░` |
| **первое** | 56 | `██████░░░░░░░░░` |
| **сообщение** | 56 | `██████░░░░░░░░░` |
| **vladspace** | 53 | `██████░░░░░░░░░` |
| **rag** | 51 | `██████░░░░░░░░░` |
| **cutcode** | 49 | `█████░░░░░░░░░░` |
| **dmitriila** | 47 | `█████░░░░░░░░░░` |
| **mixaill** | 43 | `█████░░░░░░░░░░` |
| **открытые** | 42 | `█████░░░░░░░░░░` |
| **вопросы** | 42 | `█████░░░░░░░░░░` |
| **zodigancode** | 35 | `████░░░░░░░░░░░` |
| **svyazi** | 35 | `████░░░░░░░░░░░` |


### 155. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **anthropic** | 4911 | `███████████████` |
| **vacancies** | 3878 | `███████████░░░░` |
| **agent** | 1754 | `█████░░░░░░░░░░` |
| **проблем** | 1599 | `████░░░░░░░░░░░` |
| **документы** | 1511 | `████░░░░░░░░░░░` |
| **turn** | 1470 | `████░░░░░░░░░░░` |
| **appendix** | 1460 | `████░░░░░░░░░░░` |
| **svyazi** | 1442 | `████░░░░░░░░░░░` |
| **cowork** | 1263 | `███░░░░░░░░░░░░` |
| **nautilus** | 1198 | `███░░░░░░░░░░░░` |
| **ingit** | 1099 | `███░░░░░░░░░░░░` |
| **view** | 1070 | `███░░░░░░░░░░░░` |
| **mcp** | 1059 | `███░░░░░░░░░░░░` |
| **мин** | 1002 | `███░░░░░░░░░░░░` |
| **knowledge** | 965 | `██░░░░░░░░░░░░░` |


### 156. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **anthropic** | 7200 | `███████████████` |
| **vacancies** | 6973 | `██████████████░` |
| **проблем** | 1594 | `███░░░░░░░░░░░░` |
| **svyazi** | 1226 | `██░░░░░░░░░░░░░` |
| **сложный** | 1098 | `██░░░░░░░░░░░░░` |
| **мин** | 1006 | `██░░░░░░░░░░░░░` |
| **appendix** | 937 | `█░░░░░░░░░░░░░░` |
| **слов** | 867 | `█░░░░░░░░░░░░░░` |
| **быстро** | 752 | `█░░░░░░░░░░░░░░` |
| **начало** | 711 | `█░░░░░░░░░░░░░░` |
| **collaborations** | 610 | `█░░░░░░░░░░░░░░` |
| **документы** | 580 | `█░░░░░░░░░░░░░░` |
| **абзац** | 522 | `█░░░░░░░░░░░░░░` |
| **agent** | 510 | `█░░░░░░░░░░░░░░` |
| **анализ** | 490 | `█░░░░░░░░░░░░░░` |


### 157. 01-svyazi (9,254 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **contacts** | 8 | `███████████████` |
| **описание** | 7 | `█████████████░░` |
| **contact** | 6 | `███████████░░░░` |
| **outreach** | 6 | `███████████░░░░` |
| **ensemble** | 6 | `███████████░░░░` |
| **project** | 6 | `███████████░░░░` |
| **component** | 6 | `███████████░░░░` |
| **research** | 6 | `███████████░░░░` |
| **vladspace** | 6 | `███████████░░░░` |
| **cutcode** | 6 | `███████████░░░░` |
| **смотрите** | 5 | `█████████░░░░░░` |
| **decision** | 4 | `███████░░░░░░░░` |
| **record** | 4 | `███████░░░░░░░░` |
| **имя** | 4 | `███████░░░░░░░░` |
| **ссылка** | 4 | `███████░░░░░░░░` |


## templates (4 таблиц)


### 1. Профиль
_Файл: `docs/templates/contact-outreach.md` | 2 колонок, 4 строк_

| Параметр | Значение |
|----------|---------|
| Имя | [имя] |
| GitHub | [@handle](ссылка) |
| Проекты | [список] |
| Платформа | [Habr/GitHub/Telegram] |


### 2. Рассмотренные варианты
_Файл: `docs/templates/decision-record.md` | 3 колонок, 3 строк_

| Вариант | Плюсы | Минусы |
|---------|-------|--------|
| A | | |
| B | | |
| C | | |


### 3. Компоненты
_Файл: `docs/templates/ensemble.md` | 3 колонок, 2 строк_

| Компонент | Роль | Лицензия |
|-----------|------|----------|
| [Проект A] | [роль] | [лицензия] |
| [Проект B] | [роль] | [лицензия] |


### 4. Статус
_Файл: `docs/templates/project-component.md` | 2 колонок, 4 строк_

| Параметр | Значение |
|----------|---------|
| Версия   | [x.y.z] |
| Лицензия | [MIT/Apache/BSL] |
| Язык     | [Python/TypeScript/Rust] |
| Репо     | [ссылка] |

<!-- backlinks-auto -->
## Упоминается в

- [03 Component Catalog](01-svyazi/03-component-catalog.md)
- [MemNet: исследовательская память](05-habr-projects/memory/memnet.md)
- [docs](README.md)
- [Введение](02-anthropic-vacancies/00-intro.md)
- [Введение](04-ai-collaborations/00-intro.md)
- [Все таблицы репозитория](TABLES.md)
- [Интегральный анализ профиля svend4](02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)
- [Карта найденных проектов и паттернов](04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md)
- [Карта репозитория Lorenzo](SITEMAP.md)
- [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md)
- [Ограничения, лицензии и что пока лучше не склеивать](04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md)

<!-- related-auto -->
## Связанные документы

- [Частотный анализ слов](WORD_FREQ.md) _33%_
- [Время чтения документов](READING_TIME.md) _29%_
- [Карта найденных проектов и паттернов](04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) _25%_
- [Приоритеты файлов](PRIORITIES.md) _25%_
- [Хронологическая лента событий](TIMELINE.md) _25%_
- [03 Component Catalog](01-svyazi/03-component-catalog.md) _21%_
- [06 Security Privacy](01-svyazi/06-security-privacy.md) _21%_
- [07 Mvp Planning](01-svyazi/07-mvp-planning.md) _21%_
