# Все таблицы репозитория

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

**Всего таблиц:** 248


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
| Контакт | [@Antipozitive](docs/contacts/antipozitive.md) |
| Статус связи | не писали |


### 5. Статус
_Файл: `docs/05-habr-projects/memory/ngt-memory.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 260 |
| Слой | memory |
| Контакт | [@spbmolot](docs/contacts/spbmolot.md) |
| Статус связи | не писали |


### 6. Статус
_Файл: `docs/05-habr-projects/memory/yodoca.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 229 |
| Слой | memory |
| Контакт | [@VitalyOborin](docs/contacts/vitalyoborin.md) |
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


## root (140 таблиц)


### 1. Словарь аббревиатур и сокращений
_Файл: `docs/ABBREVIATIONS.md` | 3 колонок, 84 строк_

| Аббревиатура | Расшифровка | Упоминаний |
|-------------|-------------|------------|
| **ACD** | Automated Capability Discovery — ещё один сильный кубик: модель в роли «учёного» систематически генерирует задачи для мо | 4 |
| **ADR** | "ADR-004: Temporal Metadata as First-Class Concept" | 44 |
| **AGENTS** | типология + готовая к развёртыванию категория Type 1 | 8 |
| **AI** | это инфраструктурный слой для AI-managed virtual companies | 2124 |
| **AIRI** | серьёзная research лаборатория (Артём Шелманов и команда) | 15 |
| **ANP** | Agent Network Protocol | 4 |
| **API** ⭐ | Application Programming Interface — интерфейс программирования приложений | 238 |
| **BSL** ⭐ | Business Source License — бизнес-лицензия с открытым кодом | 58 |
| **CAMEL** | это другая значимая open-source framework, и сравнение их с Hermes будет показательным | 172 |
| **CI/CD** ⭐ | Continuous Integration / Continuous Deployment | 8 |
| **CLI** ⭐ | Command Line Interface — интерфейс командной строки | 43 |
| **CRDT** ⭐ | Conflict-free Replicated Data Type — структура данных без конфликтов слияния | 51 |
| **DAO** | результат смешанный | 2 |
| **EMEA** | RU/DE/EN на рабочем уровне, базирование в Германии, понимание европейского регуляторного контекста (что прямо читается ч | 25 |
| **ERROR** | MCP SDK not installed | 2 |
| **FAQ** ⭐ | Frequently Asked Questions — часто задаваемые вопросы | 20 |
| **FDE** | это исполнительская роль на чужую продуктовую повестку | 10 |
| **GDPR** ⭐ | General Data Protection Regulation — европейский регламент защиты данных | 47 |
| **GG** | они публичные) | 1 |
| **GUI** | -3 months effort | 13 |
| **HEAD** | 7 commits) | 1 |
| **HMP** | на когнитивной устойчивости и этике | 83 |
| **ID** | sgb:XII:90:4 (SGB XII, § 90, Abs | 6 |
| **II** | The Double-Triangle Architecture — formal описание дуальной структуры с вашей метафорой звезды Давида | 21 |
| **III** | Protocols Between Layers — три протокола с examples | 15 |
| **INPUT** | - Bescheid text (decoded by agent) | 1 |
| **IP** | AI-платформа, заказчик, сами фрилансеры? Сегодняшние legal frameworks не умеют отвечать на этот вопрос дёшево | 6 |
| **IV** | Nautilus Portal as Reference Implementation — как existing work serves как substrate | 18 |
| **IX** | 102 , sgg:86b:2 ), на прецеденты | 40 |
| **JWT** ⭐ | JSON Web Token — токен аутентификации | 2 |
| **KPI** | сколько полезных коллабораций, проектов, выступлений, mentorship‑пар или hiring‑контактов возникло из рекомендаций систе | 25 |
| **KSV** | потому что у них нет точных русских эквивалентов в контексте немецкой социально-правовой системы | 27 |
| **LAYER** | функциональная категория Type 4 | 41 |
| **LCI** | Lyapunov Coherence Index, target π | 21 |
| **LLM** ⭐ | Large Language Model — большая языковая модель | 310 |
| **LOC** | продублирована с разными строками в разных частях | 47 |
| **MCP** ⭐ | Model Context Protocol — протокол контекста для AI-инструментов | 712 |
| **MIT** ⭐ | Massachusetts Institute of Technology License — разрешительная лицензия | 241 |
| **ML** | несколько моделей → voting/averaging | 51 |
| **MMORPG** | это общее пространство , в котором вы видите аватары коллег, можете подойти к ним, стоять рядом, работать вместе в одной | 40 |
| **MRR** | это уже leverage для любого следующего шага, включая разговор с Anthropic Institute о grant/partnership | 2 |
| **MUST** | - Возвращать пустой список, если ничего не найдено (не `None`, не exception) | 73 |
| **MVP** ⭐ | Minimum Viable Product — минимально жизнеспособный продукт | 202 |
| **NDA** | intermediate view (placeholder'ы, но с consistent identifiers для longitudinal анализа) | 1 |
| **NGT** | граф памяти](#глава-11-ngt-граф-памяти) | 240 |
| **NLP** ⭐ | Natural Language Processing — обработка естественного языка | 0 |
| **NPP** | **федеративная модель**, где каждый | 75 |
| **OASIS** | до 1M agents simulation) | 3 |
| **ODT** | не только текст | 1 |
| **OKWF** | конкретная архитектура](#применение-к-okwf-конкретная-архитектура) | 261 |
| **OPTIONAL** | ключевые слова | 9 |
| **OS** | неуточнено | 127 |
| **OSS** ⭐ | Open Source Software — программное обеспечение с открытым кодом | 217 |
| **OUTPUT** | - Draft Widerspruch (DOCX format) | 1 |
| **P2P** ⭐ | Peer-to-Peer — децентрализованная сеть | 9 |
| **PARC** | research center, became iconic несмотря на parent brand decline OpenAI — research org становящаяся product company, name | 2 |
| **PII** ⭐ | Personally Identifiable Information — персональные данные | 38 |
| **PROTOCOL** | иначе future разработчики будут gадать | 190 |
| **PURE** | LLM-based User Profile Management for Recommender System» | 5 |
| **QA** | демон-критик (adversarial, rigorous) | 183 |
| **RAG** ⭐ | Retrieval-Augmented Generation — генерация с поиском по базе знаний | 373 |
| **README** | 550+ строк production-качества: установка, конфигурация для всех 6 платформ (включая детализацию /etc/fstab для CIFS, AD | 354 |
| **REQUIRED** | откуда пришло | 22 |
| **ROI** | 10 sec queries vs 2 hour manual search | 14 |
| **SDK** ⭐ | Software Development Kit — набор инструментов разработчика | 41 |
| **SENTINEL** | неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2 | 154 |
| **SF** | DC, Canberra) | 17 |
| **SGB** ⭐ | Sozialgesetzbuch — Социальный кодекс Германии | 316 |
| **SHOULD** | - Поддерживать case-insensitive matching для текстовых запросов | 33 |
| **SWE** | в Sales/Finance/Marketing/Legal зарплаты ниже и сильно варьируются по локации | 5 |
| **TF-IDF** ⭐ | Term Frequency–Inverse Document Frequency — метрика важности термина | 11 |
| **TODO** ⭐ | To Do — задача к выполнению | 2 |
| **TSU** | физика, MoME — математика; ZINC — software, гибридная архитектура — алгоритм; RISC-V — кремний, privacy — право; TinyML  | 9 |
| **TVCP** | Terminal Video Communication Platform, терминал видео коммуникация платформа, игры») — это необычное : Go + template + M | 1 |
| **UI** | -2 months effort | 61 |
| **URL** | я разберусь с любым вариантом именования | 60 |
| **VERIFY** | 6782 vs 6600] как метку | 1 |
| **VI** | Deployment Paths — humanities, project management, OSS, general | 3 |
| **VII** | Open Questions — governance, consent, economics, scale | 3 |
| **VIII** | Call to Action — что делать researchers, practitioners, founders | 2 |
| **VPS** | cron каждое утро обходит сайты Sozialgericht/BSG/KSV, генерирует Stellungnahme-черновики, обновляет статусы Aktenzeichen | 9 |
| **XII** | legally binding reference с нормативной силой | 34 |
| **YAML** ⭐ | YAML Ain't Markup Language — формат конфигурационных файлов | 103 |
| **ZINC** | - Ночью агент крутит эксперименты с промптами | 25 |


### 2. Самые часто используемые
_Файл: `docs/ABBREVIATIONS.md` | 2 колонок, 15 строк_

| Аббревиатура | Упоминаний |
|-------------|------------|
| **AI** | 2124 — _это инфраструктурный слой для AI-managed virtual companies_ |
| **MCP** | 712 — _Model Context Protocol — протокол контекста для AI-инструмен_ |
| **RAG** | 373 — _Retrieval-Augmented Generation — генерация с поиском по базе_ |
| **README** | 354 — _550+ строк production-качества: установка, конфигурация для _ |
| **SGB** | 316 — _Sozialgesetzbuch — Социальный кодекс Германии_ |
| **LLM** | 310 — _Large Language Model — большая языковая модель_ |
| **OKWF** | 261 — _конкретная архитектура](#применение-к-okwf-конкретная-архите_ |
| **MIT** | 241 — _Massachusetts Institute of Technology License — разрешительн_ |
| **NGT** | 240 — _граф памяти](#глава-11-ngt-граф-памяти)_ |
| **API** | 238 — _Application Programming Interface — интерфейс программирован_ |
| **OSS** | 217 — _Open Source Software — программное обеспечение с открытым ко_ |
| **MVP** | 202 — _Minimum Viable Product — минимально жизнеспособный продукт_ |
| **PROTOCOL** | 190 — _иначе future разработчики будут gадать_ |
| **QA** | 183 — _демон-критик (adversarial, rigorous)_ |
| **CAMEL** | 172 — _это другая значимая open-source framework, и сравнение их с _ |


### 3. Callout-блоки
_Файл: `docs/ALERTS.md` | 3 колонок, 4 строк_

| Тип | Количество | Назначение |
|-----|------------|------------|
| `[!NOTE]` | 0 | Нейтральная заметка |
| `[!TIP]` | 70 | Практический совет |
| `[!WARNING]` | 34 | Предупреждение о риске |
| `[!IMPORTANT]` | 25 | Ключевой документ |


### 4. Авторы и коллаборации
_Файл: `docs/AUTHORS.md` | 2 колонок, 25 строк_

| Автор | Упоминается в файлах |
|-------|---------------------|
| **AnastasiyaW** | 25 |
| **Antipozitive** | 12 |
| **BerriAI** | 7 |
| **Cutcode** | 13 |
| **Dmitriila** | 11 |
| **MiXaiLL76** | 12 |
| **Sonia_Black** | 11 |
| **VitaliySemenov** | 4 |
| **VitalyOborin** | 19 |
| **VladSpace** | 12 |
| **akazant** | 6 |
| **akzhankalimatov** | 4 |
| **andrey_chuyan** | 10 |
| **iximy** | 5 |
| **kksudo** | 34 |
| **lee-to** | 8 |
| **lib4u** | 7 |
| **moshael** | 6 |
| **nlaik** | 11 |
| **spbmolot** | 33 |
| **tagir_analyzes** | 8 |
| **vpakspace** | 4 |
| **zodigancode** | 10 |
| **Андрей Чуян** | 21 |
| **Виталий Оборин** | 7 |


### 5. Топ-30 самых цитируемых документов
_Файл: `docs/BACKLINKS.md` | 3 колонок, 30 строк_

| Документ | Входящих ссылок | Ссылающиеся файлы |
|----------|----------------|-------------------|
| `README` | 10 | `.md`, `cowork.md`, `ingit.md`, `kksudo.md` +6 |
| `07-mvp-planning` | 3 | `README.md`, `PROGRESS.md`, `REPORT.md` |
| `HEALTH` | 3 | `PROGRESS.md`, `README.md`, `REPORT.md` |
| `CONTACTS` | 3 | `PROGRESS.md`, `README.md`, `REPORT.md` |
| `kksudo` | 2 | `CONTACT_PRIORITY.md`, `README.md` |
| `spbmolot` | 2 | `CONTACT_PRIORITY.md`, `README.md` |
| `anastasiyaw` | 2 | `CONTACT_PRIORITY.md`, `README.md` |
| `SCORING` | 2 | `PROGRESS.md`, `README.md` |
| `VALIDATION` | 2 | `README.md`, `REPORT.md` |
| `NARRATIVE` | 2 | `README.md`, `REPORT.md` |
| `SIMILAR` | 2 | `README.md`, `REPORT.md` |
| `SITEMAP` | 2 | `README.md`, `REPORT.md` |
| `QUESTIONS` | 2 | `README.md`, `REPORT.md` |
| `DECISIONS` | 2 | `README.md`, `REPORT.md` |
| `KPI` | 2 | `README.md`, `REPORT.md` |
| `BROKEN_LINKS` | 2 | `README.md`, `REPORT.md` |
| `READING_ORDER` | 2 | `README.md`, `REPORT.md` |
| `QA` | 1 | `README.md` |
| `00-intro-part2` | 1 | `README.md` |
| `12-roadmap` | 1 | `README.md` |
| `13-contacts` | 1 | `README.md` |
| `04-ensembles-overview` | 1 | `README.md` |
| `14-limitations` | 1 | `README.md` |
| `02-methodology` | 1 | `README.md` |
| `10-second-order-ensembles` | 1 | `README.md` |
| `11-integration-contracts` | 1 | `README.md` |
| `08-conclusions` | 1 | `README.md` |
| `09-architectural-gaps` | 1 | `README.md` |
| `01-executive-summary` | 1 | `README.md` |
| `03-component-catalog` | 1 | `README.md` |


### 6. Ссылки по разделам
_Файл: `docs/BACKLINKS.md` | 3 колонок, 10 строк_

| Раздел | Входящих | Исходящих |
|--------|----------|-----------|
| **01-svyazi** | 17 | 15 |
| **02-anthropic-vacancies** | 356 | 356 |
| **03-technology-combinations** | 6 | 6 |
| **04-ai-collaborations** | 16 | 16 |
| **05-habr-projects** | 9 | 9 |
| **autofilled** | 22 | 22 |
| **badges** | 0 | 0 |
| **contacts** | 17 | 14 |
| **root** | 100 | 105 |
| **templates** | 5 | 5 |


### 7. Сломанные внутренние ссылки
_Файл: `docs/BROKEN_LINKS.md` | 4 колонок, 50 строк_

| Файл | Текст ссылки | Цель | Проблема |
|------|--------------|------|----------|
| `docs/01-svyazi/01-executive-summary.md` | 01-executive-summary | `docs/04-ai-collaborations/01-executive-s` | файл не существует |
| `docs/01-svyazi/01-executive-summary.md` | 08-что-это-продолжение-добавля | `docs/04-ai-collaborations/08-что-это-про` | файл не существует |
| `docs/01-svyazi/01-executive-summary.md` | 07-выводы | `docs/04-ai-collaborations/07-выводы.md` | файл не существует |
| `docs/01-svyazi/02-methodology.md` | 02-методика-и-рамка-отбора | `docs/04-ai-collaborations/02-методика-и-` | файл не существует |
| `docs/01-svyazi/02-methodology.md` | README | `docs/04-ai-collaborations/README.md` | файл не существует |
| `docs/01-svyazi/02-methodology.md` | 02-методика-и-рамка-отбора | `docs/04-ai-collaborations/02-методика-и-` | файл не существует |
| `docs/01-svyazi/02-methodology.md` | 01-executive-summary | `docs/04-ai-collaborations/01-executive-s` | файл не существует |
| `docs/01-svyazi/02-methodology.md` | 05-план-прототипа-и-возможные- | `docs/04-ai-collaborations/05-план-протот` | файл не существует |
| `docs/01-svyazi/02-methodology.md` | DUPLICATES | `docs/DUPLICATES.md` | файл не существует |
| `docs/01-svyazi/03-component-catalog.md` | 03-карта-найденных-проектов-и- | `docs/04-ai-collaborations/03-карта-найде` | файл не существует |
| `docs/01-svyazi/03-component-catalog.md` | TABLES | `docs/TABLES.md` | файл не существует |
| `docs/01-svyazi/03-component-catalog.md` | 04-приоритетные-ансамбли | `docs/04-ai-collaborations/04-приоритетны` | файл не существует |
| `docs/01-svyazi/03-component-catalog.md` | 03-карта-найденных-проектов-и- | `docs/04-ai-collaborations/03-карта-найде` | файл не существует |
| `docs/01-svyazi/03-component-catalog.md` | TABLES | `docs/TABLES.md` | файл не существует |
| `docs/01-svyazi/03-component-catalog.md` | 04-приоритетные-ансамбли | `docs/04-ai-collaborations/04-приоритетны` | файл не существует |
| `docs/01-svyazi/03-component-catalog.md` | 04-ensembles-overview | `docs/01-svyazi/04-ensembles-overview.md` | файл не существует |
| `docs/01-svyazi/04-ensembles-overview.md` | 04-приоритетные-ансамбли | `docs/04-ai-collaborations/04-приоритетны` | файл не существует |
| `docs/01-svyazi/04-ensembles-overview.md` | 03-карта-найденных-проектов-и- | `docs/04-ai-collaborations/03-карта-найде` | файл не существует |
| `docs/01-svyazi/04-ensembles-overview.md` | 03-component-catalog | `docs/01-svyazi/03-component-catalog.md` | файл не существует |
| `docs/01-svyazi/04-ensembles-overview.md` | 04-приоритетные-ансамбли | `docs/04-ai-collaborations/04-приоритетны` | файл не существует |
| `docs/01-svyazi/04-ensembles-overview.md` | 03-карта-найденных-проектов-и- | `docs/04-ai-collaborations/03-карта-найде` | файл не существует |
| `docs/01-svyazi/04-ensembles-overview.md` | 03-component-catalog | `docs/01-svyazi/03-component-catalog.md` | файл не существует |
| `docs/01-svyazi/04-ensembles-overview.md` | 01-executive-summary | `docs/04-ai-collaborations/01-executive-s` | файл не существует |
| `docs/01-svyazi/06-security-privacy.md` | 06-безопасность-приватность-и- | `docs/04-ai-collaborations/06-безопасност` | файл не существует |
| `docs/01-svyazi/06-security-privacy.md` | 05-план-прототипа-и-возможные- | `docs/04-ai-collaborations/05-план-протот` | файл не существует |
| `docs/01-svyazi/06-security-privacy.md` | 07-mvp-planning | `docs/01-svyazi/07-mvp-planning.md` | файл не существует |
| `docs/01-svyazi/06-security-privacy.md` | 06-безопасность-приватность-и- | `docs/04-ai-collaborations/06-безопасност` | файл не существует |
| `docs/01-svyazi/06-security-privacy.md` | 05-план-прототипа-и-возможные- | `docs/04-ai-collaborations/05-план-протот` | файл не существует |
| `docs/01-svyazi/06-security-privacy.md` | 07-mvp-planning | `docs/01-svyazi/07-mvp-planning.md` | файл не существует |
| `docs/01-svyazi/06-security-privacy.md` | 04-приоритетные-ансамбли | `docs/04-ai-collaborations/04-приоритетны` | файл не существует |
| `docs/01-svyazi/07-mvp-planning.md` | 05-план-прототипа-и-возможные- | `docs/04-ai-collaborations/05-план-протот` | файл не существует |
| `docs/01-svyazi/07-mvp-planning.md` | 09-архитектурные-зазоры-которы | `docs/04-ai-collaborations/09-архитектурн` | файл не существует |
| `docs/01-svyazi/07-mvp-planning.md` | 09-architectural-gaps | `docs/01-svyazi/09-architectural-gaps.md` | файл не существует |
| `docs/01-svyazi/07-mvp-planning.md` | 09-architectural-gaps | `docs/01-svyazi/09-architectural-gaps.md` | файл не существует |
| `docs/01-svyazi/07-mvp-planning.md` | 11-integration-contracts | `docs/01-svyazi/11-integration-contracts.` | файл не существует |
| `docs/01-svyazi/07-mvp-planning.md` | 12-roadmap | `docs/01-svyazi/12-roadmap.md` | файл не существует |
| `docs/01-svyazi/08-conclusions.md` | 07-выводы | `docs/04-ai-collaborations/07-выводы.md` | файл не существует |
| `docs/01-svyazi/08-conclusions.md` | 01-executive-summary | `docs/01-svyazi/01-executive-summary.md` | файл не существует |
| `docs/01-svyazi/08-conclusions.md` | 01-executive-summary | `docs/04-ai-collaborations/01-executive-s` | файл не существует |
| `docs/01-svyazi/08-conclusions.md` | 07-выводы | `docs/04-ai-collaborations/07-выводы.md` | файл не существует |
| `docs/01-svyazi/08-conclusions.md` | 08-что-это-продолжение-добавля | `docs/04-ai-collaborations/08-что-это-про` | файл не существует |
| `docs/01-svyazi/08-conclusions.md` | 01-executive-summary | `docs/04-ai-collaborations/01-executive-s` | файл не существует |
| `docs/01-svyazi/08-conclusions.md` | MISSING | `docs/MISSING.md` | файл не существует |
| `docs/01-svyazi/09-architectural-gaps.md` | 09-архитектурные-зазоры-которы | `docs/04-ai-collaborations/09-архитектурн` | файл не существует |
| `docs/01-svyazi/09-architectural-gaps.md` | QA | `docs/QA.md` | файл не существует |
| `docs/01-svyazi/09-architectural-gaps.md` | 11-интеграционный-контракт-кот | `docs/04-ai-collaborations/11-интеграцион` | файл не существует |
| `docs/01-svyazi/09-architectural-gaps.md` | 11-integration-contracts | `docs/01-svyazi/11-integration-contracts.` | файл не существует |
| `docs/01-svyazi/09-architectural-gaps.md` | 06-security-privacy | `docs/01-svyazi/06-security-privacy.md` | файл не существует |
| `docs/01-svyazi/09-architectural-gaps.md` | 07-mvp-planning | `docs/01-svyazi/07-mvp-planning.md` | файл не существует |
| `docs/01-svyazi/10-second-order-ensembles.md` | 10-новые-ансамбли-следующего-ш | `docs/04-ai-collaborations/10-новые-ансам` | файл не существует |


### 8. Статистика коммитов
_Файл: `docs/CHANGELOG_AUTO.md` | 3 колонок, 3 строк_

| Тип | Название | Кол-во |
|-----|---------|--------|
| `feat` | ✨ Новые возможности | 5 |
| `chore` | 🔧 Технические задачи | 4 |
| `other` | 📌 Прочее | 16 |


### 9. Содержание
_Файл: `docs/CODE_BLOCKS.md` | 2 колонок, 7 строк_

| Язык | Блоков |
|------|--------|
| 📝 Без языка | 132 |
| 💻 Bash / Shell | 19 |
| 🐍 Python | 18 |
| 📦 JSON | 13 |
| 📊 Диаграммы Mermaid | 8 |
| markdown | 5 |
| 📋 YAML | 4 |


### 10. Паспорт: /
_Файл: `docs/CODE_BLOCKS.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | / |
| Формат | `.` — краткое описание |
| Единица | что является одной записью |
| Адаптер | `adapters/.py` |
| Уровень совместимости | <0-3> —  |


### 11. Изменившиеся файлы (83) — топ по Δ слов
_Файл: `docs/COMPARE.md` | 4 колонок, 30 строк_

| Файл | Было | Стало | Δ |
|------|------|-------|---|
| `QA.md` | 935 | 1473 | +538 |
| `00-intro.md` | 8477 | 8819 | +342 |
| `69-section.md` | 9162 | 9414 | +252 |
| `memnet.md` | 6765 | 7010 | +245 |
| `165-closing.md` | 8956 | 9170 | +214 |
| `150-appendix-c-version-history.md` | 8113 | 8274 | +161 |
| `173-4-ten-domains-of-application.md` | 1381 | 1491 | +110 |
| `261-8-seven-domains-of-application.md` | 808 | 890 | +82 |
| `272-appendix-d-connection-diagram.md` | 3658 | 3736 | +78 |
| `212-1-the-five-type-typology-of-principal-side-agents.md` | 754 | 819 | +65 |
| `157-3-why-existing-solutions-fail.md` | 549 | 612 | +63 |
| `263-10-risks-specific-to-composite-architectures.md` | 613 | 674 | +61 |
| `310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | 501 | 561 | +60 |
| `311-3-what-ingit-provides-that-cowork-lacks.md` | 687 | 747 | +60 |
| `218-7-application-domains.md` | 576 | 634 | +58 |
| `217-6-risks-specific-to-this-category.md` | 1027 | 1084 | +57 |
| `313-5-four-integration-paths-in-order-of-accessibility.md` | 634 | 691 | +57 |
| `186-appendix-c-sample-use-cases-in-detail.md` | 1856 | 1910 | +54 |
| `158-4-proposed-infrastructure.md` | 852 | 905 | +53 |
| `161-7-phased-rollout-plan.md` | 512 | 565 | +53 |
| `162-8-risk-analysis.md` | 524 | 576 | +52 |
| `171-2-historical-precedents-agents-as-civilizational-i.md` | 813 | 865 | +52 |
| `164-10-appendices.md` | 820 | 871 | +51 |
| `262-9-integration-with-okwf-infrastructure.md` | 587 | 636 | +49 |
| `142-5-pattern-library-as-bridge-between-triangles.md` | 531 | 578 | +47 |
| `219-8-pilot-proposal-sgb-advocate-colleague.md` | 825 | 872 | +47 |
| `220-9-relationship-to-other-agent-types.md` | 519 | 565 | +46 |
| `256-3-what-makes-a-composite-skills-agent.md` | 796 | 842 | +46 |
| `68-about.md` | 744 | 788 | +44 |
| `254-1-why-the-binary-view-is-incomplete.md` | 552 | 595 | +43 |


### 12. Распределение сложности
_Файл: `docs/COMPLEXITY.md` | 2 колонок, 3 строк_

| Уровень | Файлов |
|---------|--------|
| 🟢 Простой (0-1) | 354 |
| 🟡 Средний (2-3)  | 129 |
| 🔴 Сложный (4-5)  | 26 |


### 13. Самые сложные документы
_Файл: `docs/COMPLEXITY.md` | 6 колонок, 25 строк_

| Документ | Слов | Ср.длина пред. | Термин.плотность | Ур.заголовков | Балл |
|----------|------|---------------|-----------------|--------------|------|
| `342-что-такое-вариант-c-concept-doc` | 10559 | 26.7 | 0.17% | H5 | 🔴 Сложный |
| `343-lorenzo-catalyst-agent-глубокая` | 5629 | 26.4 | 0.25% | H5 | 🔴 Сложный |
| `365-развёрнутый-анализ-внуковой-ком` | 4071 | 18.2 | 1.01% | H4 | 🔴 Сложный |
| `00-intro` | 8710 | 18.0 | 0.25% | H4 | 🔴 Сложный |
| `01-интегральный-анализ-профиля-sven` | 18837 | 15.8 | 0.14% | H4 | 🔴 Сложный |
| `133-обратная-связь` | 3628 | 17.4 | 0.36% | H4 | 🔴 Сложный |
| `150-appendix-c-version-history` | 4791 | 20.1 | 0.02% | H4 | 🔴 Сложный |
| `272-appendix-d-connection-diagram` | 3678 | 15.2 | 0.03% | H4 | 🔴 Сложный |
| `303-приложение-визуализация-позиции` | 1712 | 19.3 | 1.17% | H4 | 🔴 Сложный |
| `341-приложение-c-образец-спецификац` | 3446 | 24.2 | 0.44% | H4 | 🔴 Сложный |
| `03-local-first` | 304 | 17.4 | 4.28% | H4 | 🔴 Сложный |
| `05-benchmarks` | 740 | 25.7 | 2.3% | H4 | 🔴 Сложный |
| `00-intro` | 11272 | 18.4 | 1.31% | H2 | 🔴 Сложный |
| `14-ограничения-лицензии-и-что-пока-` | 3198 | 17.5 | 1.0% | H2 | 🔴 Сложный |
| `ABBREVIATIONS` | 1016 | 145.3 | 1.77% | H2 | 🔴 Сложный |
| `COMPONENT_MATRIX` | 504 | 63.6 | 4.56% | H2 | 🔴 Сложный |
| `CONCEPTS` | 11401 | 356.7 | 0.26% | H2 | 🔴 Сложный |
| `CONTACT_PRIORITY` | 232 | 46.4 | 4.31% | H3 | 🔴 Сложный |
| `ENTITIES` | 423 | 25.8 | 8.51% | H2 | 🔴 Сложный |
| `FOOTNOTES` | 189 | 63.7 | 6.88% | H2 | 🔴 Сложный |
| `GLOSSARY` | 91 | 45.5 | 10.99% | H1 | 🔴 Сложный |
| `GRAPH` | 163 | 27.7 | 17.18% | H2 | 🔴 Сложный |
| `NETWORK` | 300 | 300.0 | 15.33% | H2 | 🔴 Сложный |
| `andrey-chuyan` | 82 | 27.0 | 6.1% | H2 | 🔴 Сложный |
| `tagir-analyzes` | 76 | 25.3 | 6.58% | H2 | 🔴 Сложный |


### 14. Самые простые документы
_Файл: `docs/COMPLEXITY.md` | 3 колонок, 15 строк_

| Документ | Слов | Балл |
|----------|------|------|
| `03-portal-protocol-md` | 58 | 🟢 Простой |
| `05-0-status-of-this-document` | 85 | 🟢 Простой |
| `06-1-introduction` | 289 | 🟢 Простой |
| `07-2-terminology` | 248 | 🟢 Простой |
| `08-3-registry-nautilus-json` | 259 | 🟢 Простой |
| `09-4-passport-passport-md` | 103 | 🟢 Простой |
| `105-review-methodology-md` | 59 | 🟢 Простой |
| `106-tl-dr` | 115 | 🟢 Простой |
| `108-2-формальный-workflow` | 215 | 🟢 Простой |
| `110-вопрос-fallback-ratio-как-критически` | 213 | 🟢 Простой |
| `112-5-связь-с-существующими-методологиям` | 256 | 🟢 Простой |
| `114-7-реализация-в-проекте-nautilus` | 225 | 🟢 Простой |
| `115-8-ограничения-и-открытые-вопросы` | 320 | 🟢 Простой |
| `117-10-конкретный-план-применения-к-теку` | 145 | 🟢 Простой |
| `119-appendix-b-примеры-расхождений-и-их-` | 141 | 🟢 Простой |


### 15. Матрица возможностей
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


### 16. Покрытие возможностей
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


### 17. Каталог компонентов
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


### 18. Рекомендуемые ансамбли
_Файл: `docs/COMPONENT_MATRIX.md` | 3 колонок, 5 строк_

| Ансамбль | Компоненты | Ключевая функция |
|----------|-----------|-----------------|
| Knowledge OS | CardIndex + AgentFS + knowledge-space | Индекс знаний + AI FS |
| Memory Layer | Yodoca + NGT-memory + agent-memory-mcp | Долгосрочная память |
| Security Runtime | SENTINEL + AgentFS | PII-защита + MCP allowlist |
| Web Intelligence | Firecrawl + CardIndex + Yodoca | Краулинг → память |
| Agent Orchestra | Rufler + agent-pool + AI Factory | Оркестрация агентов |


### 19. Топ концептов по связям
_Файл: `docs/CONCEPT_GRAPH.md` | 4 колонок, 30 строк_

| Концепт | Файлов | Связей | Категория |
|---------|--------|--------|-----------|
| `docs` | 412 | 3265 | other |
| `anthropic` | 347 | 2926 | other |
| `vacancies` | 333 | 2807 | other |
| `сходство` | 225 | 1990 | other |
| `summary` | 241 | 1875 | other |
| `tags` | 164 | 1432 | other |
| `architecture` | 113 | 1123 | other |
| `agent` | 118 | 1120 | agent |
| `nautilus` | 104 | 1040 | other |
| `knowledge` | 105 | 905 | other |
| `portal` | 88 | 872 | other |
| `collaboration` | 83 | 855 | other |
| `appendix` | 88 | 797 | other |
| `protocol` | 72 | 761 | architecture |
| `work` | 75 | 746 | other |
| `agents` | 76 | 739 | agent |
| `cowork` | 63 | 708 | other |
| `layer` | 63 | 699 | architecture |
| `ingit` | 61 | 648 | other |
| `svyazi` | 92 | 640 | project |
| `document` | 53 | 612 | data |
| `infrastructure` | 59 | 595 | other |
| `документы` | 65 | 593 | other |
| `claude` | 59 | 587 | other |
| `what` | 61 | 574 | other |
| `first` | 59 | 536 | other |
| `документ` | 62 | 532 | other |
| `слой` | 70 | 515 | architecture |
| `svend` | 49 | 507 | other |
| `memory` | 65 | 494 | memory |


### 20. Согласованность терминов
_Файл: `docs/CONSISTENCY.md` | 4 колонок, 6 строк_

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 2 |
| **knowledge-space** | `knowledge-space` | `knowledge space` | 6 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 1 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 5 |
| **self-improvement** | `self-improvement` | `self-improve` | 48 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |


### 21. Ключевые авторы проектов
_Файл: `docs/CONTACTS.md` | 5 колонок, 15 строк_

| Автор | Проект | Слой | Упомянут в файлах | Первый вопрос |
|-------|--------|------|-------------------|---------------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 20 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 7 | — |
| **Cutcode** | AIF Handoff | orchestration | 8 | — |
| **Dmitriila** | SENTINEL | security | 6 | — |
| **MiXaiLL76** | Auto AI Router | security | 7 | — |
| **Sonia_Black** | knowledge-space | knowledge | 9 | — |
| **VitalyOborin** | Yodoca | memory | 12 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 6 | — |
| **andrey_chuyan** | Svyazi | ingestion/CardIndex | 7 | Стоит ли расширять CardIndex до person/project/episode/evidence или лучше держать разные индексы? |
| **kksudo** | AgentFS | knowledge/filesystem | 21 | Что лучше класть в .agentos, а что выносить в machine-only state вне vault conventions? |
| **lee-to** | AI Factory | orchestration | 7 | — |
| **nlaik** | LiteParse / research-docs | rag | 6 | — |
| **spbmolot** | NGT Memory | memory | 20 | Где проходит практическая граница между полезной ассоциацией и ложной ко-активацией тем для community discovery? |
| **tagir_analyzes** | Legal RAG | rag | 7 | — |
| **zodigancode** | Rufler | orchestration | 6 | — |


### 22. GitHub репозитории
_Файл: `docs/CONTACTS.md` | 2 колонок, 24 строк_

| Репозиторий | Упоминается в файлах |
|-------------|---------------------|
| `github.com/github.com/AnastasiyaW/knowledge-space` | 6 |
| `github.com/github.com/NicholasSpisak/second-brain` | 2 |
| `github.com/github.com/anthropics/mcp` | 5 |
| `github.com/github.com/artur-gavronchuk/tg-chat-analyser` | 2 |
| `github.com/github.com/camel-ai/camel` | 5 |
| `github.com/github.com/dementev-dev/adversarial-review` | 2 |
| `github.com/github.com/github` | 2 |
| `github.com/github.com/mcp` | 7 |
| `github.com/github.com/settings/tokens` | 5 |
| `github.com/github.com/svend4` | 5 |
| `github.com/github.com/svend4/data70` | 5 |
| `github.com/github.com/svend4/info1` | 11 |
| `github.com/github.com/svend4/info40` | 5 |
| `github.com/github.com/svend4/info7` | 5 |
| `github.com/github.com/svend4/ingit` | 13 |
| `github.com/github.com/svend4/meta` | 10 |
| `github.com/github.com/svend4/n` | 2 |
| `github.com/github.com/svend4/nautilu` | 2 |
| `github.com/github.com/svend4/nautilus` | 41 |
| `github.com/github.com/svend4/nautilus.git` | 4 |
| `github.com/github.com/svend4/pro2` | 9 |
| `github.com/github.com/users/svend4` | 5 |
| `github.com/github.com/vuguzum/self-aware-mcp-server` | 2 |
| `github.com/github.com/yjs/yjs` | 2 |


### 23. Топ авторов по приоритету
_Файл: `docs/CONTACT_PRIORITY.md` | 7 колонок, 15 строк_

| # | Автор | Проект | Слой | Упоминаний | Статус | Балл |
|---|-------|--------|------|-----------|--------|------|
| 1 | **kksudo** | AgentFS | knowledge/filesystem | 21 | 👁 Изучили | 74 |
| 2 | **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 20 | ⬜ Не начато | 66 |
| 3 | **spbmolot** | NGT Memory | memory | 20 | ⬜ Не начато | 66 |
| 4 | **VitalyOborin** | Yodoca | memory | 12 | ⬜ Не начато | 42 |
| 5 | **Sonia_Black** | knowledge-space | knowledge | 9 | ⬜ Не начато | 33 |
| 6 | **Cutcode** | AIF Handoff | orchestration | 8 | ⬜ Не начато | 28 |
| 7 | **Antipozitive** | MemNet | memory | 7 | ⬜ Не начато | 27 |
| 8 | **lee-to** | AI Factory | orchestration | 7 | ⬜ Не начато | 25 |
| 9 | **tagir_analyzes** | Legal RAG | rag | 7 | ⬜ Не начато | 25 |
| 10 | **MiXaiLL76** | Auto AI Router | security | 7 | ⬜ Не начато | 23 |
| 11 | **andrey_chuyan** | Svyazi | ingestion/CardIndex | 7 | ⬜ Не начато | 23 |
| 12 | **VladSpace** | Graph RAG | rag | 6 | ⬜ Не начато | 22 |
| 13 | **nlaik** | LiteParse / research-docs | rag | 6 | ⬜ Не начато | 22 |
| 14 | **zodigancode** | Rufler | orchestration | 6 | ⬜ Не начато | 22 |
| 15 | **Dmitriila** | SENTINEL | security | 6 | ⬜ Не начато | 20 |


### 24. Итого
_Файл: `docs/COST.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Человеко-недель | **25** |
| Человеко-часов | **1,000** |
| Бюджет (USD) | **$86,400** |
| Календарный срок | **~6-8 месяцев** |
| Команда | **5 ролей** |


### 25. По компонентам
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


### 26. По ролям
_Файл: `docs/COST.md` | 4 колонок, 5 строк_

| Роль | Ставка USD/ч | Недель | Итого USD |
|------|-------------|--------|----------|
| Senior Python Dev | $85 | 11 | $37,400 |
| AI/ML Engineer | $110 | 7 | $30,800 |
| DevOps | $75 | 2 | $6,000 |
| Tech Writer | $45 | 1 | $1,800 |
| Project Manager | $65 | 4 | $10,400 |


### 27. Сценарии
_Файл: `docs/COST.md` | 4 колонок, 3 строк_

| Сценарий | Команда | Срок | Бюджет |
|----------|---------|------|--------|
| Минимальный (solo) | 1 разработчик | ~18 мес | $28,800 |
| Оптимальный | 3 человека | ~8 мес | $43,200 |
| Ускоренный | 5 человек | ~5 мес | $86,400 |


### 28. Временные оценки из документов
_Файл: `docs/COST.md` | 3 колонок, 15 строк_

| Источник | Контекст | Недель |
|----------|----------|--------|
| `365-развёрнутый-анал` | Макс) и part-time, реальный timeline 12-24 месяца для full a… | 96 |
| `343-lorenzo-catalyst` | рудоёмкий процесс подачи - Может быть 6-18 месяцев до финанс… | 72 |
| `365-развёрнутый-анал` | eam. С solo developer (Макс) и part-time, реальный timeline … | 72 |
| `ACTION_ITEMS` | обратная-связь_ - 5: Burnout. Проект 12-18 месяцев для singl… | 72 |
| `DECISIONS` | document — структурированный план на 12-18 месяцев, который … | 72 |
| `NARRATIVE` | инимально жизнеспособный прототип за 12-18 месяцев 4. **Кома… | 72 |
| `332-6-уточнённый-объ` | Оригинальная дорожная карта InGit (10-16 месяцев до v1.0) от… | 64 |
| `332-6-уточнённый-объ` | окращённый Объём  Оригинальный план: 10-16 месяцев до v1.0 с… | 64 |
| `00-intro` | ом смысле. Это архив 1105 разговоров за 15 месяцев (dec 2024… | 60 |
| `00-intro` | — это ChatGPT-корпус 1105 разговоров за 15 месяцев + аналити… | 60 |
| `01-интегральный-анал` | на личном примере, пропустив через себя 15 месяцев диалогов … | 60 |
| `133-обратная-связь` | ы и интерес. Временной план: это не спринт, это marathon на … | 60 |
| `133-обратная-связь` | бственные кейсы, не other people's. Риск 5: Burnout. Проект … | 60 |
| `133-обратная-связь` | вить strategic roadmap document — структурированный план на … | 60 |
| `ACTION_ITEMS` | llout, acce     _→ 133-обратная-связь_ - 5: Burnout. Проект … | 60 |


### 29. Сводка по секциям
_Файл: `docs/COVERAGE.md` | 8 колонок, 5 строк_

| Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks |
|--------|--------|---------|------|-----|-----------|--------|-----------|
| `01-svyazi` | 14 | 🟢 12/14 | 🟢 13/14 | 🔴 0/14 | 🟢 12/14 | 🔴 0/14 | 🔴 0/14 |
| `02-anthropic-vacancies` | 355 | 🟢 336/355 | 🟡 277/355 | 🔴 93/355 | 🟢 319/355 | 🔴 0/355 | 🔴 0/355 |
| `03-technology-combinations` | 5 | 🟢 5/5 | 🟢 5/5 | 🔴 1/5 | 🟢 5/5 | 🔴 0/5 | 🔴 0/5 |
| `04-ai-collaborations` | 15 | 🟢 15/15 | 🟢 15/15 | 🔴 0/15 | 🟢 15/15 | 🟢 15/15 | 🔴 0/15 |
| `05-habr-projects` | 6 | 🟢 6/6 | 🟢 6/6 | 🔴 1/6 | 🟢 6/6 | 🟢 6/6 | 🔴 0/6 |


### 30. Файлы с низким покрытием (< 3 признаков) — 87 файлов
_Файл: `docs/COVERAGE.md` | 8 колонок, 40 строк_

| Файл | Слов | Summary | Теги | TOC | CrossRefs | ## Статус | Backlinks |
|------|------| ---|---|---|---|---|--- |
| `docs/01-svyazi/00-intro-part2.md` | 5 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 20 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 20 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | 34 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 29 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 32 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 91 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 93 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | 29 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | 30 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` | 35 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` | 35 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/31-content-overview.md` | 19 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | 31 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 142 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | 129 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 41 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 30 | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | 29 | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | 179 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | 214 | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | 207 | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | 36 | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | 140 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 104 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 169 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 71 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 69 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/38-content-overview.md` | 97 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/01-svyazi/01-executive-summary.md` | 597 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/01-svyazi/03-component-catalog.md` | 1149 | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/04-abstract.md` | 116 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | 109 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | 221 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 62 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | 165 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | 83 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | 87 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/16-history.md` | 65 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |


### 31. Карта плотности тем
_Файл: `docs/DENSITY.md` | 8 колонок, 20 строк_

| Тема | 01-svyazi | 02-vacancies | 03-tech | 04-collab | 05-habr | root | Итого |
|------|-----------|--------------|---------|-----------|---------|------|-------|
| **Svyazi** | 126 | 72 | 16 | 243 | 44 | 1286 | **1787** |
| **CardIndex** | 53 | 54 | 12 | 99 | 14 | 326 | **558** |
| **AgentFS** | 51 | 85 | 4 | 98 | 29 | 320 | **587** |
| **Yodoca** | 86 | 36 | 18 | 130 | 68 | 390 | **728** |
| **NGT-memory** | 162 | 230 | 2 | 244 | 82 | 641 | **1361** |
| **SENTINEL** | 47 | 8 | 0 | 58 | 0 | 141 | **254** |
| **Rufler** | 35 | 19 | 0 | 43 | 0 | 148 | **245** |
| **AI Factory** | 63 | 45 | 0 | 82 | 0 | 321 | **511** |
| **Knowledge OS** | 0 | 18 | 0 | 4 | 0 | 20 | **42** |
| **Forensic RAG** | 34 | 18 | 1 | 52 | 2 | 81 | **188** |
| **MCP** | 60 | 648 | 4 | 146 | 56 | 256 | **1170** |
| **MVP** | 65 | 90 | 0 | 92 | 10 | 366 | **623** |
| **Архитектура** | 62 | 504 | 9 | 135 | 35 | 402 | **1147** |
| **Безопасность** | 54 | 120 | 1 | 67 | 1 | 295 | **538** |
| **Лицензия** | 100 | 620 | 0 | 127 | 16 | 391 | **1254** |
| **Roadmap** | 30 | 143 | 0 | 27 | 3 | 177 | **380** |
| **Вакансии** | 4 | 2549 | 4 | 15 | 7 | 3957 | **6536** |
| **Комбинации** | 5 | 132 | 50 | 16 | 10 | 176 | **389** |
| **Habr** | 34 | 78 | 20 | 184 | 97 | 347 | **760** |
| **Контакты** | 18 | 128 | 0 | 21 | 5 | 162 | **334** |


### 32. Наиболее раскрытые темы
_Файл: `docs/DENSITY.md` | 3 колонок, 10 строк_

| Тема | Упоминаний | Визуализация |
|------|------------|-------------|
| **Вакансии** | 6536 | `███████████████` |
| **Svyazi** | 1787 | `████░░░░░░░░░░░` |
| **NGT-memory** | 1361 | `███░░░░░░░░░░░░` |
| **Лицензия** | 1254 | `██░░░░░░░░░░░░░` |
| **MCP** | 1170 | `██░░░░░░░░░░░░░` |
| **Архитектура** | 1147 | `██░░░░░░░░░░░░░` |
| **Habr** | 760 | `█░░░░░░░░░░░░░░` |
| **Yodoca** | 728 | `█░░░░░░░░░░░░░░` |
| **MVP** | 623 | `█░░░░░░░░░░░░░░` |
| **AgentFS** | 587 | `█░░░░░░░░░░░░░░` |


### 33. Где сосредоточена каждая тема
_Файл: `docs/DENSITY.md` | 3 колонок, 20 строк_

| Тема | Основной раздел | % |
|------|-----------------|---|
| Svyazi | `root` | 71% |
| CardIndex | `root` | 58% |
| AgentFS | `root` | 54% |
| Yodoca | `root` | 53% |
| NGT-memory | `root` | 47% |
| SENTINEL | `root` | 55% |
| Rufler | `root` | 60% |
| AI Factory | `root` | 62% |
| Knowledge OS | `root` | 47% |
| Forensic RAG | `root` | 43% |
| MCP | `02-anthropic-vacancies` | 55% |
| MVP | `root` | 58% |
| Архитектура | `02-anthropic-vacancies` | 43% |
| Безопасность | `root` | 54% |
| Лицензия | `02-anthropic-vacancies` | 49% |
| Roadmap | `root` | 46% |
| Вакансии | `root` | 60% |
| Комбинации | `root` | 45% |
| Habr | `root` | 45% |
| Контакты | `root` | 48% |


### 34. Зависимости
_Файл: `docs/DEPENDENCY_MAP.md` | 3 колонок, 49 строк_

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


### 35. История коммитов (последние 15)
_Файл: `docs/DIGEST.md` | 3 колонок, 15 строк_

| Дата | Hash | Описание |
|------|------|---------|
| 2026-04-29 | `a48150bf` | improve: batch 11 — orphans, alerts, metrics, index update, master run |
| 2026-04-29 | `a25efe45` | improve: batch 10 — backlinks, heatmap, templates, validation, executi |
| 2026-04-29 | `873b8c58` | improve: batch 9 — abbreviations, sentiment, narrative, JSON export, n |
| 2026-04-29 | `ff8fe0fa` | improve: batch 8 — stats, similar docs, questions, KPI, sitemap |
| 2026-04-29 | `1c9ceeaa` | improve: batch 7 — compare, density, complexity, entities, concepts |
| 2026-04-29 | `0952c336` | improve: batch 6 — autocorrect, TOC, tables/code extraction, word freq |
| 2026-04-29 | `14f735a7` | improve: consistency check, broken links, changelog, CSV export |
| 2026-04-29 | `4e7137c4` | improve: action items, gap analysis, clustering, mindmap, HTML export |
| 2026-04-29 | `e787c21f` | improve: add Q&A sheets, priority ranking, and contacts extraction |
| 2026-04-29 | `b3d7d0bf` | improve: add tags, search index, and project relationship graph |
| 2026-04-29 | `75f1b3e4` | improve: add summaries, cross-refs, dedup report, timeline |
| 2026-04-29 | `91dd9685` | improve: verify coverage, merge short files, add READMEs and glossary |
| 2026-04-29 | `7658df5b` | chore: add .gitignore for Python cache files |
| 2026-04-29 | `ff8a8161` | chore: add extract_mhtml.py and ignore pycache |
| 2026-04-29 | `d49a1f0f` | feat: organize docs into monorepo structure with topic-based subfolder |


### 36. Текущее состояние репозитория
_Файл: `docs/DIGEST.md` | 2 колонок, 3 строк_

| Параметр | Значение |
|----------|---------|
| Документов `.md` | **460** |
| Скриптов обработки | **56** |
| Последнее обновление | **2026-04-29** |


### 37. Итого
_Файл: `docs/DIGEST_WEEKLY.md` | 2 колонок, 5 строк_

| Метрика | Значение |
|---------|---------|
| Коммитов за неделю | **22** |
| Новых файлов | **0** |
| Изменённых файлов | **0** |
| Всего MD файлов | **482** |
| Всего слов | **388,554** |


### 38. Точные дубли (одинаковое содержимое)
_Файл: `docs/DUPLICATES.md` | 2 колонок, 1 строк_

| Группа | Файлы |
|--------|-------|
| #1 | `docs/templates/research-note.md`, `docs/autofilled/research-summary.md` |


### 39. Люди и авторы (7)
_Файл: `docs/ENTITIES.md` | 3 колонок, 7 строк_

| Имя | Упоминаний | Файлов |
|---------|------------|--------|
| **svend4** | 854 | 113 |
| **Lorenzo** | 625 | 45 |
| **kksudo** | 76 | 35 |
| **Андрей** | 70 | 23 |
| **spbmolot** | 66 | 34 |
| **Виталий** | 29 | 14 |
| **Антропик** | 2 | 2 |


### 40. Проекты (22)
_Файл: `docs/ENTITIES.md` | 3 колонок, 22 строк_

| Проект | Упоминаний | Файлов |
|---------|------------|--------|
| **Nautilus** | 1548 | 185 |
| **Svyazi** | 1546 | 133 |
| **ingit** | 1103 | 85 |
| **Cowork** | 1073 | 86 |
| **SGB** | 637 | 86 |
| **Lorenzo** | 625 | 45 |
| **CardIndex** | 472 | 70 |
| **AgentFS** | 449 | 61 |
| **NGT** | 389 | 81 |
| **Yodoca** | 360 | 67 |
| **knowledge-space** | 313 | 52 |
| **mclaude** | 268 | 45 |
| **Rufler** | 244 | 46 |
| **AI Factory** | 228 | 48 |
| **LiteParse** | 222 | 47 |
| **SENTINEL** | 192 | 47 |
| **MemNet** | 123 | 31 |
| **Wikontic** | 114 | 24 |
| **Firecrawl** | 84 | 12 |
| **agent-memory-mcp** | 37 | 17 |
| **Shield** | 8 | 5 |
| **MCP Tool Search** | 7 | 4 |


### 41. Организации (9)
_Файл: `docs/ENTITIES.md` | 3 колонок, 9 строк_

| Организация | Упоминаний | Файлов |
|---------|------------|--------|
| **Anthropic** | 6465 | 403 |
| **Claude** | 1095 | 168 |
| **GitHub** | 912 | 134 |
| **Habr** | 525 | 76 |
| **Хабр** | 232 | 38 |
| **Obsidian** | 135 | 40 |
| **Google** | 45 | 17 |
| **OpenAI** | 44 | 24 |
| **ChatGPT** | 41 | 25 |


### 42. Технологии и стандарты (24)
_Файл: `docs/ENTITIES.md` | 3 колонок, 24 строк_

| Технология | Упоминаний | Файлов |
|---------|------------|--------|
| **RAG** | 1131 | 155 |
| **MCP** | 1124 | 141 |
| **MIT** | 847 | 161 |
| **LLM** | 526 | 93 |
| **JSON** | 319 | 79 |
| **Python** | 262 | 71 |
| **REST** | 180 | 73 |
| **YAML** | 144 | 54 |
| **Apache** | 73 | 40 |
| **CRDT** | 72 | 20 |
| **BSL** | 72 | 38 |
| **Rust** | 67 | 38 |
| **SQLite** | 46 | 15 |
| **Mermaid** | 41 | 13 |
| **TypeScript** | 17 | 11 |
| **LangChain** | 17 | 11 |
| **PostgreSQL** | 12 | 8 |
| **TF-IDF** | 11 | 9 |
| **FAISS** | 10 | 8 |
| **WebSocket** | 9 | 8 |
| **FastAPI** | 8 | 6 |
| **OAuth** | 3 | 2 |
| **JWT** | 3 | 3 |
| **GraphQL** | 2 | 2 |


### 43. GitHub репозитории (12)
_Файл: `docs/ENTITIES.md` | 2 колонок, 12 строк_

| Репозиторий | Упоминаний |
|-------------|------------|
| [https://github.com/svend4/nautilus](https://github.com/svend4/nautilus) | 26 |
| [https://github.com/svend4/ingit](https://github.com/svend4/ingit) | 11 |
| [https://github.com/svend4/pro2](https://github.com/svend4/pro2) | 6 |
| [https://github.com/svend4/info1](https://github.com/svend4/info1) | 6 |
| [https://github.com/svend4/meta](https://github.com/svend4/meta) | 5 |
| [https://github.com/settings/tokens](https://github.com/settings/tokens) | 4 |
| [https://github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space) | 4 |
| [https://github.com/camel-ai/camel](https://github.com/camel-ai/camel) | 4 |
| [https://github.com/anthropics/mcp](https://github.com/anthropics/mcp) | 4 |
| [https://github.com/svend4/data70](https://github.com/svend4/data70) | 3 |
| [https://github.com/svend4/info7](https://github.com/svend4/info7) | 3 |
| [https://github.com/svend4/info40](https://github.com/svend4/info40) | 3 |


### 44. Ко-встречаемость проектов (топ пары)
_Файл: `docs/ENTITIES.md` | 2 колонок, 20 строк_

| Пара | Общих файлов |
|------|-------------|
| ingit ↔ Cowork | 71 |
| Svyazi ↔ NGT | 68 |
| Svyazi ↔ Yodoca | 62 |
| NGT ↔ Yodoca | 62 |
| Svyazi ↔ CardIndex | 61 |
| Nautilus ↔ Cowork | 59 |
| Svyazi ↔ AgentFS | 59 |
| CardIndex ↔ NGT | 56 |
| Nautilus ↔ ingit | 55 |
| AgentFS ↔ NGT | 55 |
| CardIndex ↔ AgentFS | 54 |
| Nautilus ↔ SGB | 52 |
| AgentFS ↔ Yodoca | 52 |
| CardIndex ↔ Yodoca | 50 |
| Svyazi ↔ knowledge-space | 49 |
| Svyazi ↔ AI Factory | 48 |
| Svyazi ↔ LiteParse | 47 |
| NGT ↔ AI Factory | 46 |
| Svyazi ↔ mclaude | 45 |
| Svyazi ↔ Rufler | 45 |


### 45. Словарь сносок
_Файл: `docs/FOOTNOTES.md` | 3 колонок, 17 строк_

| Термин | Определение | Файлов |
|--------|-------------|--------|
| **AgentFS** | OSS-проект: файловая система для AI-агентов (MIT) | 23 |
| **BSL** | Business Source License — коммерческая лицензия с открытым кодом | 6 |
| **CRDT** | Conflict-free Replicated Data Type — бесконфликтные данные | 8 |
| **CardIndex** | OSS-проект: индекс знаний на карточках (MIT) | 24 |
| **Firecrawl** | Инструмент: веб-краулер для AI (MIT) | 2 |
| **Jaccard** | Коэффициент схожести множеств (0–1) | 0 |
| **LLM** | Large Language Model — большая языковая модель | 16 |
| **MCP** | Model Context Protocol — протокол для AI-инструментов | 19 |
| **NGT** | OSS-проект: ассоциативный граф памяти (BSL 1.1) | 23 |
| **PII** | Personally Identifiable Information — персональные данные | 6 |
| **RAG** | Retrieval-Augmented Generation — генерация с поиском | 24 |
| **Rufler** | OSS-проект: оркестратор AI-агентов | 16 |
| **SENTINEL** | OSS-проект: безопасность и allowlist для MCP | 16 |
| **Svyazi** | Главный проект: экосистема AI-компонентов | 34 |
| **TF-IDF** | Term Frequency–Inverse Document Frequency — метрика важности термина | 0 |
| **Yodoca** | OSS-проект: система памяти с консолидацией (Apache 2.0) | 22 |
| **knowledge-space** | OSS-проект: база знаний 785+ карточек (MIT) | 0 |


### 46. Топ совместных упоминаний
_Файл: `docs/GRAPH.md` | 3 колонок, 25 строк_

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **CardIndex** | 32 |
| **Svyazi** | **AI Factory** | 30 |
| **Svyazi** | **Yodoca** | 30 |
| **Svyazi** | **NGT Memory** | 29 |
| **Svyazi** | **mclaude** | 28 |
| **Svyazi** | **AgentFS** | 27 |
| **CardIndex** | **NGT Memory** | 27 |
| **AgentFS** | **AI Factory** | 27 |
| **mclaude** | **AI Factory** | 27 |
| **AI Factory** | **Yodoca** | 27 |
| **Yodoca** | **NGT Memory** | 27 |
| **Svyazi** | **LiteParse** | 26 |
| **CardIndex** | **Yodoca** | 26 |
| **mclaude** | **Yodoca** | 26 |
| **AI Factory** | **NGT Memory** | 26 |
| **CardIndex** | **AgentFS** | 25 |
| **CardIndex** | **mclaude** | 25 |
| **CardIndex** | **AI Factory** | 25 |
| **AgentFS** | **Yodoca** | 25 |
| **mclaude** | **NGT Memory** | 25 |
| **AgentFS** | **mclaude** | 24 |
| **Svyazi** | **Auto AI Router** | 23 |
| **CardIndex** | **LiteParse** | 23 |
| **AgentFS** | **LiteParse** | 23 |
| **AgentFS** | **NGT Memory** | 23 |


### 47. Метрики
_Файл: `docs/HEALTH.md` | 4 колонок, 5 строк_

| Метрика | Значение | Статус | Балл |
|---------|----------|--------|------|
| Покрытие текста | 97.6% | 🟢 | 98 |
| Полнота тем | 23✅ 3⚠️ 4❌ | 🟡 | 77 |
| Согласованность | 0 проблем | 🟢 | 100 |
| Внутренние ссылки | 26 сломано | 🔴 | 0 |
| Дублирование | 0 точных дублей | 🟢 | 100 |


### 48. Структура репозитория
_Файл: `docs/HEALTH.md` | 2 колонок, 9 строк_

| Раздел | Файлов |
|--------|--------|
| 01-svyazi | 16 |
| 02-anthropic-vacancies | 357 |
| 03-technology-combinations | 7 |
| 04-ai-collaborations | 17 |
| 05-habr-projects | 10 |
| badges | 1 |
| contacts | 14 |
| root | 56 |
| templates | 6 |


### 49. Числовые значения (‰)
_Файл: `docs/HEATMAP.md` | 6 колонок, 12 строк_

| Тема | svyazi | anthropic- | technology | ai-collabo | habr-proje |
|------|------------|------------|------------|------------|------------|
| **Память/Knowledge** | 26.6 | 3.2 | 15.6 | 17.0 | 14.9 |
| **Агент/Оркестр** | 24.8 | 12.8 | 25.5 | 20.6 | 9.6 |
| **Безопасность** | 7.9 | 0.4 | 0.4 | 4.2 | 0.1 |
| **Архитектура** | 6.3 | 5.5 | 4.5 | 3.7 | 1.2 |
| **MVP/Roadmap** | 6.8 | 0.9 | 0.0 | 3.0 | 1.3 |
| **Граф/RAG** | 10.8 | 1.9 | 22.2 | 8.5 | 3.7 |
| **Лицензия/OSS** | 8.6 | 2.4 | 0.0 | 4.6 | 1.4 |
| **Вакансии** | 0.4 | 10.4 | 1.6 | 0.6 | 0.8 |
| **Комбинации** | 2.3 | 0.6 | 20.6 | 1.9 | 2.2 |
| **Habr/Проекты** | 8.6 | 0.5 | 9.1 | 10.8 | 15.2 |
| **Контакты/Команда** | 4.7 | 0.8 | 0.0 | 2.8 | 1.9 |
| **Интеграция/API** | 8.5 | 7.2 | 2.9 | 7.5 | 7.3 |


### 50. Концентрация тем
_Файл: `docs/HEATMAP.md` | 3 колонок, 12 строк_

| Тема | Лучший раздел | Плотность |
|------|--------------|-----------|
| **Память/Knowledge** | `01-svyazi` | 26.6‰ |
| **Агент/Оркестр** | `03-technology-combinations` | 25.5‰ |
| **Безопасность** | `01-svyazi` | 7.9‰ |
| **Архитектура** | `01-svyazi` | 6.3‰ |
| **MVP/Roadmap** | `01-svyazi` | 6.8‰ |
| **Граф/RAG** | `03-technology-combinations` | 22.2‰ |
| **Лицензия/OSS** | `01-svyazi` | 8.6‰ |
| **Вакансии** | `02-anthropic-vacancies` | 10.4‰ |
| **Комбинации** | `03-technology-combinations` | 20.6‰ |
| **Habr/Проекты** | `05-habr-projects` | 15.2‰ |
| **Контакты/Команда** | `01-svyazi` | 4.7‰ |
| **Интеграция/API** | `01-svyazi` | 8.5‰ |


### 51. Метрики репозитория
_Файл: `docs/INDEX.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Markdown документов | **489** |
| Слов | **391,514** |
| Скриптов автоматизации | **78** |
| Go/No-Go скоринг | **96 🟢** |
| Здоровье репо | **75/100** |


### 52. Аналитика и отчёты
_Файл: `docs/INDEX.md` | 2 колонок, 26 строк_

| Документ | Описание |
|----------|---------|
| [`STATS.md`](docs/STATS.md) | Статистика |
| [`METRICS.md`](docs/METRICS.md) | Качество (65.7/100) |
| [`VALIDATION.md`](docs/VALIDATION.md) | Валидация |
| [`SENTIMENT.md`](docs/SENTIMENT.md) | Тональность |
| [`CLUSTERS.md`](docs/CLUSTERS.md) | Кластеры тем |
| [`SIMILAR.md`](docs/SIMILAR.md) | Похожие документы |
| [`HEATMAP.md`](docs/HEATMAP.md) | Тепловая карта тем |
| [`QUESTIONS.md`](docs/QUESTIONS.md) | Открытые вопросы (484) |
| [`KPI.md`](docs/KPI.md) | KPI (737 показателей) |
| [`ACTION_ITEMS.md`](docs/ACTION_ITEMS.md) | Задачи |
| [`DECISIONS.md`](docs/DECISIONS.md) | Архитектурные решения |
| [`PRIORITIES.md`](docs/PRIORITIES.md) | Приоритеты |
| [`PROGRESS.md`](docs/PROGRESS.md) | Прогресс MVP |
| [`DIGEST_WEEKLY.md`](docs/DIGEST_WEEKLY.md) | Дайджест недели |
| [`SITEMAP.md`](docs/SITEMAP.md) | Карта сайта |
| [`WORD_CLOUD.md`](docs/WORD_CLOUD.md) | Облако слов |
| [`BACKLINKS.md`](docs/BACKLINKS.md) | Обратные ссылки |
| [`NARRATIVE.md`](docs/NARRATIVE.md) | Нарратив проекта |
| [`ORPHANS.md`](docs/ORPHANS.md) | Несвязанные файлы |
| [`ALERTS.md`](docs/ALERTS.md) | Callout-блоки |
| [`FOOTNOTES.md`](docs/FOOTNOTES.md) | Сноски терминов |
| [`ABBREVIATIONS.md`](docs/ABBREVIATIONS.md) | Аббревиатуры |
| [`GLOSSARY.md`](docs/GLOSSARY.md) | Глоссарий |
| [`CONCEPTS.md`](docs/CONCEPTS.md) | Концепции |
| [`ENTITIES.md`](docs/ENTITIES.md) | Сущности |
| [`TAGS.md`](docs/TAGS.md) | Теги |


### 53. Ключевые документы
_Файл: `docs/INDEX.md` | 3 колонок, 12 строк_

| Документ | Тема | Описание |
|----------|------|---------|
| [`SCORING.md`](docs/SCORING.md) | 🎯 Go/No-Go скоринг | Статус готовности: 96% |
| [`HEALTH.md`](docs/HEALTH.md) | ❤️  Здоровье репо | Метрики качества документации |
| [`TECH_RADAR.md`](docs/TECH_RADAR.md) | 📡 Tech Radar | ADOPT/TRIAL/ASSESS/HOLD |
| [`RISK_REGISTER.md`](docs/RISK_REGISTER.md) | ⚠️  Реестр рисков | 10 рисков, матрица вероятность×влияние |
| [`ONBOARDING.md`](docs/ONBOARDING.md) | 👋 Онбординг | Первые шаги, структура, контакты |
| [`FAQ.md`](docs/FAQ.md) | ❓ FAQ | 54 вопроса и ответа |
| [`CONTACTS.md`](docs/CONTACTS.md) | 📧 Контакты | Авторы компонентов, шаблоны писем |
| [`SCHEDULE.md`](docs/SCHEDULE.md) | 📅 Расписание | Gantt, вехи, текущий статус |
| [`COST.md`](docs/COST.md) | 💰 Стоимость MVP | $86,400 · 25 чел-недель |
| [`NETWORK.md`](docs/NETWORK.md) | 🕸️  Граф связей | 20 узлов, 185 рёбер |
| [`CHANGELOG_AUTO.md`](docs/CHANGELOG_AUTO.md) | 📋 Changelog | Авто из git-истории |
| [`DEPENDENCY_MAP.md`](docs/DEPENDENCY_MAP.md) | 🗺️  Карта зависимостей | 49 скриптов → входы/выходы |


### 54. LLM-обогащение (Ступень 3)
_Файл: `docs/INDEX.md` | 2 колонок, 4 строк_

| Документ | Описание |
|----------|---------|
| `LLM_ENRICHED.md` _(нет)_ | Обогащённые stub-файлы |
| `LLM_QA.md` _(нет)_ | Ответы на открытые вопросы |
| `LLM_GAPS.md` _(нет)_ | Семантические пробелы |
| [`LLM_SUMMARIES.md`](docs/LLM_SUMMARIES.md) | AI-саммари разделов |


### 55. Топ слов по охвату файлов
_Файл: `docs/KEYWORD_INDEX.md` | 3 колонок, 100 строк_

| Слово | Файлов | Всего упоминаний |
|-------|--------|-----------------|
| `docs` | 439 | 5892 |
| `также` | 401 | 437 |
| `смотрите` | 400 | 401 |
| `документы` | 385 | 485 |
| `anthropic` | 382 | 4906 |
| `похожие` | 377 | 378 |
| `сходство` | 377 | 993 |
| `vacancies` | 377 | 4413 |
| `knowledge` | 186 | 735 |
| `agent` | 170 | 1437 |
| `nautilus` | 169 | 895 |
| `документ` | 168 | 425 |
| `protocol` | 151 | 609 |
| `portal` | 144 | 629 |
| `work` | 141 | 555 |
| `mcp` | 131 | 801 |
| `open` | 130 | 413 |
| `agents` | 125 | 710 |
| `содержание` | 120 | 180 |
| `review` | 119 | 399 |
| `github` | 117 | 513 |
| `claude` | 116 | 546 |
| `через` | 115 | 466 |
| `слой` | 114 | 379 |
| `если` | 113 | 610 |
| `first` | 113 | 375 |
| `infrastructure` | 113 | 503 |
| `project` | 112 | 398 |
| `document` | 112 | 607 |
| `layer` | 111 | 521 |
| `svyazi` | 109 | 1162 |
| `reference` | 108 | 278 |
| `appendix` | 104 | 810 |
| `между` | 102 | 331 |
| `svend` | 101 | 510 |
| `агентов` | 99 | 420 |
| `foundation` | 99 | 310 |
| `specific` | 99 | 371 |
| `model` | 98 | 251 |
| `только` | 97 | 325 |
| `без` | 97 | 381 |
| `architecture` | 96 | 397 |
| `быть` | 95 | 309 |
| `проекты` | 92 | 202 |
| `каждый` | 92 | 298 |
| `legal` | 91 | 408 |
| `research` | 91 | 348 |
| `level` | 90 | 324 |
| `implementation` | 90 | 230 |
| `один` | 89 | 389 |
| `может` | 89 | 397 |
| `pattern` | 89 | 341 |
| `context` | 88 | 205 |
| `human` | 88 | 242 |
| `structure` | 88 | 228 |
| `source` | 86 | 214 |
| `integration` | 86 | 295 |
| `projects` | 85 | 262 |
| `которые` | 84 | 325 |
| `code` | 84 | 298 |
| `author` | 84 | 243 |
| `memory` | 83 | 596 |
| `проект` | 83 | 346 |
| `working` | 83 | 209 |
| `professional` | 83 | 359 |
| `what` | 83 | 521 |
| `through` | 83 | 178 |
| `когда` | 82 | 239 |
| `existing` | 82 | 267 |
| `search` | 81 | 609 |
| `все` | 80 | 232 |
| `вопросы` | 80 | 245 |
| `collaboration` | 80 | 243 |
| `где` | 80 | 284 |
| `skills` | 78 | 271 |
| `агент` | 77 | 409 |
| `cowork` | 77 | 918 |
| `sgb` | 76 | 454 |
| `ingit` | 76 | 776 |
| `знаний` | 75 | 180 |
| `который` | 75 | 371 |
| `документов` | 75 | 146 |
| `вопрос` | 75 | 247 |
| `уже` | 74 | 385 |
| `api` | 73 | 216 |
| `содержит` | 73 | 81 |
| `okwf` | 73 | 304 |
| `статус` | 71 | 121 |
| `architectural` | 71 | 193 |
| `tool` | 70 | 215 |
| `mvp` | 70 | 261 |
| `collaborations` | 70 | 338 |
| `архитектура` | 70 | 208 |
| `репо` | 70 | 328 |
| `all` | 70 | 144 |
| `case` | 70 | 227 |
| `space` | 69 | 251 |
| `tip` | 68 | 68 |
| `работает` | 68 | 207 |
| `habr` | 68 | 285 |


### 56. Топ биграмм (устойчивые словосочетания)
_Файл: `docs/KEYWORD_INDEX.md` | 3 колонок, 30 строк_

| Биграмм | Файлов | Всего |
|---------|--------|-------|
| `anthropic vacancies` | 346 | 4378 |
| `docs anthropic` | 342 | 4353 |
| `portal protocol` | 64 | 350 |
| `vacancies appendix` | 47 | 315 |
| `docs collaborations` | 43 | 295 |
| `docs svyazi` | 40 | 540 |
| `professional colleague` | 40 | 189 |
| `NGT Memory` | 38 | 147 |
| `nautilus portal` | 38 | 174 |
| `executive summary` | 35 | 164 |
| `appendix minimal` | 34 | 90 |
| `minimal working` | 34 | 90 |
| `working example` | 34 | 90 |
| `knowledge-space` | 32 | 191 |
| `table contents` | 32 | 162 |
| `turn view` | 31 | 917 |
| `double triangle` | 31 | 171 |
| `triangle architecture` | 31 | 117 |
| `representative agent` | 31 | 139 |
| `composite skills` | 31 | 111 |
| `ingit cowork` | 30 | 100 |
| `oss проект` | 29 | 143 |
| `vacancies abstract` | 29 | 75 |
| `pattern library` | 29 | 112 |
| `principal side` | 29 | 110 |
| `view turn` | 28 | 657 |
| `abstract docs` | 28 | 67 |
| `cite turn` | 27 | 487 |
| `skills agent` | 27 | 88 |
| `colleague agents` | 27 | 86 |


### 57. Количество (98)
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
| **4** | → 14-ограничения-лицензии-и-что-пока-лучше-не-склеивать_ - (4 файлов) _→ CLUSTER | `ACTION_ITEMS` |
| **22** | ластеров: 120 ## Кластер 1 — cowork, ingit, yes, project (22 файлов) - `docs/02- | `CLUSTERS` |
| **12** | vacancies/326-содержание.md` — _326-содержание_ - _...и ещё 12 файлов_ ## Класте | `CLUSTERS` |
| **17** | йлов_ ## Кластер 2 — professional, agent, colleague, type (17 файлов) - `docs/02 | `CLUSTERS` |
| **16** | ..и ещё 7 файлов_ ## Кластер 3 — turn, view, cite, search (16 файлов) - `docs/01 | `CLUSTERS` |
| **6** | md` — _03-карта-найденных-проектов-и-паттернов_ - _...и ещё 6 файлов_ ## Кластер | `CLUSTERS` |
| **15** | .и ещё 6 файлов_ ## Кластер 4 — repo, passport, npp, json (15 файлов) - `docs/02 | `CLUSTERS` |
| **14** | 5 файлов_ ## Кластер 6 — документ, document, com, github (14 файлов) - `docs/02- | `CLUSTERS` |
| **13** | .и ещё 4 файлов_ ## Кластер 7 — turn, view, label, svyazi (13 файлов) - `docs/01 | `CLUSTERS` |
| **3** | авляет.md` — _08-что-это-продолжение-добавляет_ - _...и ещё 3 файлов_ ## Кластер | `CLUSTERS` |
| **11** | и ещё 3 файлов_ ## Кластер 8 — contents, table, why, call (11 файлов) - `docs/02 | `CLUSTERS` |
| **1** | table-of-contents.md` — _253-table-of-contents_ - _...и ещё 1 файлов_ ## Кластер | `CLUSTERS` |
| _...ещё 78_ | | |


### 58. Количество (98)
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
| _...ещё 59_ | | |


### 59. Количество (98)
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
| _...ещё 140_ | | |


### 60. Количество (98)
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
| _...ещё 217_ | | |


### 61. Количество (98)
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


### 62. Количество (98)
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
| **3.1.0** | RFCs to Indicate Requirement Levels - OpenAPI Specification v3.1.0 (for REST API | `104-appendix-c-references` |
| **1.2** | прямое следствие этого. #### Что я сознательно оставил для v1.2 или v2.0 Formal  | `104-appendix-c-references` |
| **3.0** | Удалить transitional header 7. Добавить changelog-запись: «v3.0 consolidated fro | `110-вопрос-fallback-ratio` |
| **0.2.0** | # Planned (v0.2.0) > - HTTP-mode для debugging и remote access --- ## | `132-planned-v0-2-0` |
| **0.6.0** | laude (Анастасия Бутова, AnastasiyaW) — реально существует, версия 0.6.0, MIT, 1 | `365-развёрнутый-анализ-вн` |
| **3.2** | viewer 1 (GPT-5.4): проверяет логику - Reviewer 2 (DeepSeek-V3.2): проверяет --- | `02-knowledge-graphs` |
| **0.1** | st per card, trace completeness. MVP boundary: что входит в v0.1, что запрещено  | `14-ограничения-лицензии-и` |
| **0.2** | leteness. MVP boundary: что входит в v0.1, что запрещено до v0.2. Pilot scenario | `14-ограничения-лицензии-и` |
| **0.11.0** | лицензия. К 23 апреля 2026 (несколько дней назад) — версия v0.11.0 с 95 600+ звё | `TABLES` |
| **5.0.6** | 2026` \| азработка : версии HMP-0001 → HMP-0005 (март 2026, версия 5.0.6) - Доку | `TABLES` |


### 63. Количество (98)
_Файл: `docs/KPI.md` | 3 колонок, 7 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **10** | nts (≈8 репо)](#кластер-4-archives-experiments-8-репо) - [Топ-10 репо, в которые | `00-intro` |
| **5** | sh/git), либо помочь с English README-драфтом для одного из топ-5, либо проработ | `00-intro` |
| **30** | с обратных ссылок **Файлов с входящими ссылками:** 520 ## Топ-30 самых цитируемы | `BACKLINKS` |
| **20** | svyazi/04-ensembles-overview.md` +41 \| ## Файлы → проекты Топ-20 файлов с наибо | `CROSSREFS` |
| **15** | \| 60% \| 60% \| \| **root** \| 50 \| 17.6 \| 1.3 \| 6% \| 4% \| ## Топ-15 лучши | `METRICS` |
| **50** | ключевым терминам архитектуры). **Всего файлов:** 488 ## Топ-50 самых важных фай | `PRIORITIES` |
| **3** | **Файлов проанализировано:** 433 Для каждого документа — топ-3 похожих по словар | `SIMILAR` |


### 64. Количество (98)
_Файл: `docs/KPI.md` | 3 колонок, 6 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **1** | les . Каждая фаза имеет smoke-test: завершена или нет. #### Фаза 1 — Спецификаци | `02-общий-план-развития-na` |
| **2** | адаптер для нового репо без задавания вопросов автору? #### Фаза 2 — Reference i | `02-общий-план-развития-na` |
| **3** | озвращает non-empty результат с consensus-информацией? #### Фаза 3 — MCP интерфе | `02-общий-план-развития-na` |
| **4** | кристалла», получить osmыслený ответ с указанием репо. #### Фаза 4 — Web interfa | `02-общий-план-развития-na` |
| **5** | y через браузер, получить отформатированный результат. #### Фаза 5 — Публикация  | `02-общий-план-развития-na` |
| **0** | Представительского Агента происходит в пять фаз. ### 9.1. Фаза 0 — Основание (Ме | `199-9-стратегия-поэтапног` |


### 65. Текущие метрики
_Файл: `docs/KPI_HISTORY.md` | 3 колонок, 7 строк_

| Метрика | Значение | Тренд |
|---------|---------|-------|
| Markdown документов | **491** | → |
| Слов | **392,850** | → |
| Скриптов | **80** | → |
| Скоринг | **96%** | → |
| Здоровье | **75/100** | → |
| KPI показателей | **737** | → |
| Открытых вопросов | **35** | → |


### 66. Индекс ссылок
_Файл: `docs/LINKS.md` | 2 колонок, 136 строк_

| URL | Найден в файлах |
|-----|-----------------|
| http://localhost:8000 | 6 |
| http://localhost:8080 | 5 |
| https://...install.sh | 4 |
| https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakansiy-s-zarplatoy-do-405000 | 4 |
| https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakans… | 3 |
| https://activitypub.rocks/ | 4 |
| https://api.github.com/users/svend4/repos?per_page=100&sort=updated | 5 |
| https://api.github.com/users/svend4/repos?per_page=100&sort=updated&type=owner | 5 |
| https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv | 2 |
| https://claude.com/product/cowork | 9 |
| https://creativecommons.org/licenses/by/4.0/ | 5 |
| https://forum.obsidian.md/t/new-plugin-llm-wiki-turn-your-vault-into-a-queryable-knowledge-base-privately/113223 | 5 |
| https://github | 2 |
| https://github.com/AnastasiyaW | 2 |
| https://github.com/AnastasiyaW/knowledge-space | 5 |
| https://github.com/Antipozitive | 2 |
| https://github.com/Cutcode | 2 |
| https://github.com/Dmitriila | 2 |
| https://github.com/MiXaiLL76 | 2 |
| https://github.com/Sonia_Black | 2 |
| https://github.com/VitalyOborin | 2 |
| https://github.com/VladSpace | 2 |
| https://github.com/andrey_chuyan | 2 |
| https://github.com/anthropics/mcp | 5 |
| https://github.com/camel-ai/camel | 5 |
| https://github.com/kksudo | 2 |
| https://github.com/mcp | 7 |
| https://github.com/nlaik | 2 |
| https://github.com/settings/tokens | 5 |
| https://github.com/spbmolot | 2 |
| https://github.com/svend4/ | 3 |
| https://github.com/svend4/data70 | 4 |
| https://github.com/svend4/info1 | 7 |
| https://github.com/svend4/info40 | 4 |
| https://github.com/svend4/info7 | 4 |
| https://github.com/svend4/ingit | 12 |
| https://github.com/svend4/ingit/issues | 4 |
| https://github.com/svend4/meta | 6 |
| https://github.com/svend4/nautilus | 12 |
| https://github.com/svend4/nautilus.git | 3 |
| https://github.com/svend4/nautilus/blob/claude/review-nautilus-changes-tdywx/README.md | 3 |
| https://github.com/svend4/nautilus/blob/main/INTEGRATION.md | 3 |
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
| https://github.com/svend4/nautilus/issues | 17 |
| https://github.com/svend4/nautilus/tree/abfa80e853594454bae03e95ba09f12eb443ca50/docs | 3 |
| https://github.com/svend4/nautilus/tree/main/adapters | 3 |
| https://github.com/svend4/nautilus/tree/main/passports | 3 |
| https://github.com/svend4/pro2 | 7 |
| https://github.com/svend4/pro2/blob/main/nautilus/README.md | 3 |
| https://github.com/svend4/pro2/tree/6637d1299af963db66485aa5599346d41badc6dc/nautilus | 3 |
| https://github.com/svend4/pro2/tree/main/nautilus | 3 |
| https://github.com/svend4?tab=repositories | 3 |
| https://github.com/tagir_analyzes | 1 |
| https://github.com/zodigancode | 1 |
| https://habr. | 3 |
| https://habr.com/ru/articles/1002138/ | 4 |
| https://habr.com/ru/articles/1005776/ | 4 |
| https://habr.com/ru/articles/1006602/ | 3 |
| https://habr.com/ru/articles/1006602/, | 3 |
| https://habr.com/ru/articles/1006622/ | 6 |
| https://habr.com/ru/articles/1007122/ | 4 |
| https://habr.com/ru/articles/1007122/, | 3 |
| https://habr.com/ru/articles/1009538/ | 4 |
| https://habr.com/ru/articles/1009608/ | 4 |
| https://habr.com/ru/articles/1009958/ | 4 |
| https://habr.com/ru/articles/1010198/ | 4 |
| https://habr.com/ru/articles/1010478/ | 4 |
| https://habr.com/ru/articles/1012894/ | 3 |
| https://habr.com/ru/articles/1014366/ | 3 |
| https://habr.com/ru/articles/1016096/ | 4 |
| https://habr.com/ru/articles/1017200/ | 4 |
| https://habr.com/ru/articles/1019588/ | 3 |
| https://habr.com/ru/articles/1019588/, | 3 |
| https://habr.com/ru/articles/1020598/ | 3 |
| https://habr.com/ru/articles/1020598/, | 3 |
| https://habr.com/ru/articles/1020860/ | 4 |
| https://habr.com/ru/articles/1021622/ | 3 |
| https://habr.com/ru/articles/1023446/ | 4 |
| https://habr.com/ru/articles/1024634/ | 4 |
| https://habr.com/ru/articles/1024884/comments/ | 4 |
| https://habr.com/ru/articles/1026666/ | 3 |
| https://habr.com/ru/articles/1027210/ | 4 |
| https://habr.com/ru/articles/1027382/ | 4 |
| https://habr.com/ru/articles/1027658/ | 4 |
| https://habr.com/ru/articles/1027724/ | 6 |
| https://habr.com/ru/articles/1027878/ | 3 |
| https://habr.com/ru/articles/1027878/, | 3 |
| https://habr.com/ru/articles/495554/ | 3 |
| https://habr.com/ru/articles/893356/ | 4 |
| https://habr.com/ru/articles/938626/ | 3 |
| https://habr.com/ru/articles/938626/, | 3 |
| https://habr.com/ru/articles/943498/ | 3 |
| https://habr.com/ru/articles/943498/, | 3 |
| https://habr.com/ru/articles/955798/ | 4 |
| https://habr.com/ru/articles/975414/ | 4 |
| https://habr.com/ru/articles/983684/ | 4 |
| https://habr.com/ru/articles/996144/ | 4 |
| https://habr.com/ru/companies/airi/articles/1000720/ | 4 |
| https://habr.com/ru/companies/airi/articles/855128/ | 4 |
| https://habr.com/ru/companies/surfstudio/articles/943108/ | 4 |
| https://habr.com/ru/companies/teamly/articles/1024062/ | 3 |
| https://habr.com/ru/companies/yandex/articles/1019928/ | 4 |
| https://habr.com/ru/companies/yoomoney/articles/1012870/ | 4 |
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


### 67. Качество по разделам
_Файл: `docs/METRICS.md` | 6 колонок, 6 строк_

| Раздел | Балл | Ссылок/1K слов | Код-блоков/1K | % с summary | % с тегами |
|--------|------|----------------|--------------|-------------|------------|
| **01-svyazi** | 62 | 13.1 | 0.5 | 80% | 87% |
| **02-anthropic-vacancies** | 70 | 29.6 | 1.0 | 94% | 78% |
| **03-technology-combinations** | 61 | 28.4 | 0.0 | 71% | 71% |
| **04-ai-collaborations** | 74 | 12.2 | 0.0 | 88% | 88% |
| **05-habr-projects** | 57 | 45.1 | 0.0 | 60% | 60% |
| **root** | 50 | 17.6 | 1.3 | 6% | 4% |


### 68. Топ-15 лучших документов
_Файл: `docs/METRICS.md` | 3 колонок, 15 строк_

| Документ | Балл | Слов |
|----------|------|------|
| `01-интегральный-анализ-профиля-svend4` | 100 | 19066 |
| `02-общий-план-развития-nautilus-portal-p` | 100 | 3128 |
| `133-обратная-связь` | 100 | 16935 |
| `139-2-the-double-triangle-architecture` | 100 | 686 |
| `142-5-pattern-library-as-bridge-between-` | 100 | 623 |
| `232-1-типология-из-пяти-типов-агентов-на` | 100 | 818 |
| `248-приложение-c-архитектура-быстрого-ст` | 100 | 3397 |
| `331-5-четыре-пути-интеграции-в-порядке-д` | 100 | 718 |
| `341-приложение-c-образец-спецификаций-ин` | 100 | 20349 |
| `342-что-такое-вариант-c-concept-document` | 100 | 11194 |
| `365-развёрнутый-анализ-внуковой-комбинац` | 100 | 4334 |
| `366-технический-stack-svyazi-2-0-foundat` | 100 | 3810 |
| `69-section` | 100 | 9462 |
| `72-расписание-фазы-3` | 100 | 788 |
| `00-intro` | 90 | 8853 |


### 69. Документы, требующие улучшения (6)
_Файл: `docs/METRICS.md` | 3 колонок, 6 строк_

| Документ | Балл | Что отсутствует |
|----------|------|----------------|
| `185-appendix-b-domain-comparison-ma` | 30 | summary, tags, TOC, callout |
| `206-приложение-b-матрица-сравнения-` | 30 | summary, tags, TOC, callout |
| `BACKLINKS` | 30 | summary, tags, TOC, callout |
| `COST` | 30 | summary, tags, TOC, callout |
| `SCORING` | 30 | summary, tags, TOC, callout |
| `SEE_ALSO` | 30 | summary, tags, TOC, callout |


### 70. Легенда
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


### 71. Карта пробелов знаний
_Файл: `docs/MISSING.md` | 6 колонок, 25 строк_

| Статус | Тема / Проект | Файлов | Слов | Минимум | Примеры файлов |
|--------|---------------|--------|------|---------|----------------|
| ⚠️ | **бюджетный роутинг** | 6 | 68 | ≥2ф/300сл | `QA.md`, `06-безопасность-приватность-и-бюджетный-роутинг.md` |
| ❌ | **лицензия BSL** | 0 | 0 | ≥1ф/50сл |  |
| ❌ | **voice ingestion** | 0 | 0 | ≥1ф/100сл |  |
| ✅ | **local-first** | 61 | 21753 | ≥2ф/300сл | `TAGS.md`, `SEARCH.md` |
| ✅ | **Svyazi** | 57 | 56070 | ≥5ф/2000сл | `TIMELINE.md`, `GLOSSARY.md` |
| ✅ | **CardIndex** | 48 | 47361 | ≥3ф/500сл | `GLOSSARY.md`, `ACTION_ITEMS.md` |
| ✅ | **Yodoca** | 38 | 32559 | ≥2ф/300сл | `GLOSSARY.md`, `ACTION_ITEMS.md` |
| ✅ | **NGT Memory** | 38 | 36916 | ≥2ф/300сл | `GLOSSARY.md`, `ACTION_ITEMS.md` |
| ✅ | **AgentFS** | 36 | 28843 | ≥3ф/500сл | `GLOSSARY.md`, `ACTION_ITEMS.md` |
| ✅ | **AI Factory** | 36 | 27516 | ≥2ф/200сл | `GLOSSARY.md`, `ACTION_ITEMS.md` |
| ✅ | **mclaude** | 34 | 26502 | ≥2ф/200сл | `GLOSSARY.md`, `ACTION_ITEMS.md` |
| ✅ | **LiteParse** | 32 | 22839 | ≥2ф/300сл | `TIMELINE.md`, `GLOSSARY.md` |
| ✅ | **knowledge-space** | 31 | 28051 | ≥3ф/500сл | `GLOSSARY.md`, `ACTION_ITEMS.md` |
| ✅ | **SENTINEL** | 30 | 25678 | ≥2ф/200сл | `GLOSSARY.md`, `ACTION_ITEMS.md` |
| ✅ | **Rufler** | 28 | 19734 | ≥2ф/200сл | `GLOSSARY.md`, `ACTION_ITEMS.md` |
| ✅ | **AutoResearch** | 23 | 19280 | ≥1ф/100сл | `GLOSSARY.md`, `GRAPH.md` |
| ✅ | **Evidence Envelope** | 17 | 7437 | ≥2ф/200сл | `ACTION_ITEMS.md`, `QA.md` |
| ✅ | **Card Envelope** | 12 | 6635 | ≥2ф/200сл | `ACTION_ITEMS.md`, `QA.md` |
| ✅ | **CRDT** | 12 | 9270 | ≥1ф/100сл | `03-карта-найденных-проектов-и-паттернов.md`, `04-приоритетные-ансамбли.md` |
| ✅ | **Sozialrecht** | 11 | 13812 | ≥1ф/200сл | `SEARCH.md`, `PRIORITIES.md` |
| ✅ | **Skill Policy** | 9 | 2809 | ≥1ф/100сл | `QA.md`, `11-интеграционный-контракт-который-стоит-зафиксироват.md` |
| ✅ | **Review Record** | 9 | 5311 | ≥1ф/100сл | `QA.md`, `11-интеграционный-контракт-который-стоит-зафиксироват.md` |
| ✅ | **privacy by design** | 9 | 9069 | ≥1ф/100сл | `03-карта-найденных-проектов-и-паттернов.md`, `09-архитектурные-зазоры-которые-важнее-новых-инструме.md` |
| ✅ | **Memory Write Policy** | 7 | 5531 | ≥2ф/200сл | `11-интеграционный-контракт-который-стоит-зафиксироват.md`, `13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` |
| ✅ | **self-improvement** | 6 | 7604 | ≥1ф/100сл | `12-дорожная-карта-прототипа-следующей-итерации.md`, `14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` |


### 72. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 17 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `anthropic` | 374 | people |
| `claude` | 143 | people |
| `svend4` | 84 | people |
| `kksudo` | 20 | people |
| `spbmolot` | 18 | people |
| `anastasiyaw` | 14 | people |
| `vitalyoborin` | 11 | people |
| `andrey_chuyan` | 7 | people |
| `settings` | 4 | people |
| `anthropics` | 4 | people |
| `camel-ai` | 3 | people |
| `users` | 3 | people |
| `dementev-dev` | 2 | people |
| `nicholasspisak` | 2 | people |
| `yjs` | 2 | people |
| `artur-gavronchuk` | 2 | people |
| `vuguzum` | 2 | people |


### 73. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 40 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `nautilus` | 147 | projects |
| `GitHub` | 118 | projects |
| `svyazi` | 100 | projects |
| `CardIndex` | 60 | projects |
| `yodoca` | 57 | projects |
| `ngt` | 57 | projects |
| `agentfs` | 50 | projects |
| `knowledge-space` | 41 | projects |
| `LiteParse` | 38 | projects |
| `obsidian` | 37 | projects |
| `notion` | 33 | projects |
| `lorenzo` | 28 | projects |
| `AutoResearch` | 24 | projects |
| `PortalEntry` | 21 | projects |
| `MemNet` | 17 | projects |
| `gpt` | 16 | projects |
| `wikontic` | 16 | projects |
| `ingit` | 10 | projects |
| `OpenWhispr` | 9 | projects |
| `BaseAdapter` | 9 | projects |
| `gemini` | 9 | projects |
| `CodeWiki` | 8 | projects |
| `TypeScript` | 8 | projects |
| `AutoGen` | 8 | projects |
| `faiss` | 7 | projects |
| `VladSpace` | 7 | projects |
| `QueryResult` | 7 | projects |
| `langchain` | 7 | projects |
| `WebSocket` | 6 | projects |
| `mistral` | 6 | projects |
| `chromadb` | 6 | projects |
| `llamaindex` | 5 | projects |
| `pro2` | 5 | projects |
| `DeepSeek` | 5 | projects |
| `DeepMind` | 5 | projects |
| `ChatDev` | 5 | projects |
| `info1` | 5 | projects |
| `AutoAdapter` | 5 | projects |
| `DevOps` | 5 | projects |
| `OpenClaw` | 5 | projects |


### 74. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 28 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `mcp` | 126 | tech |
| `api` | 72 | tech |
| `llm` | 64 | tech |
| `rag` | 58 | tech |
| `markdown` | 52 | tech |
| `json` | 47 | tech |
| `git` | 44 | tech |
| `yaml` | 42 | tech |
| `python` | 38 | tech |
| `rest` | 24 | tech |
| `go` | 22 | tech |
| `html` | 15 | tech |
| `sqlite` | 14 | tech |
| `transformer` | 12 | tech |
| `cd` | 10 | tech |
| `vector` | 9 | tech |
| `ci` | 8 | tech |
| `react` | 8 | tech |
| `docker` | 7 | tech |
| `rust` | 6 | tech |
| `postgresql` | 5 | tech |
| `bm25` | 4 | tech |
| `jaccard` | 4 | tech |
| `cosine` | 3 | tech |
| `css` | 2 | tech |
| `fastapi` | 2 | tech |
| `webhook` | 2 | tech |
| `kubernetes` | 2 | tech |


### 75. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 8 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `вк` | 115 | orgs |
| `meta` | 83 | orgs |
| `mail` | 31 | orgs |
| `openai` | 19 | orgs |
| `google` | 12 | orgs |
| `microsoft` | 9 | orgs |
| `yandex` | 6 | orgs |
| `сбер` | 3 | orgs |


### 76. 👤 People (17)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 28 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `2026-04` | 66 | dates |
| `2026-04-19` | 11 | dates |
| `апрель 2026` | 9 | dates |
| `2026-04-26` | 9 | dates |
| `2026/04/25` | 7 | dates |
| `март 2026` | 6 | dates |
| `в 2026 году` | 6 | dates |
| `апреля 2026` | 6 | dates |
| `декабрь 2025` | 4 | dates |
| `апреле 2026` | 4 | dates |
| `январе 2026` | 4 | dates |
| `декабря 2025` | 3 | dates |
| `декабрь 2024` | 3 | dates |
| `марта 2026` | 3 | dates |
| `2026-05-03` | 3 | dates |
| `2025-12-15` | 3 | dates |
| `2024-01-01` | 3 | dates |
| `2026-04-15` | 3 | dates |
| `май 2025` | 3 | dates |
| `феврале 2025` | 3 | dates |
| `Сентябрь 2025` | 3 | dates |
| `января 2026` | 3 | dates |
| `2026-04-29` | 3 | dates |
| `2026-10-15` | 2 | dates |
| `2026-02-01` | 2 | dates |
| `2025-11-12` | 2 | dates |
| `ноябре 2025` | 2 | dates |
| `февраля 2026` | 2 | dates |


### 77. Топ-20 ко-упоминаемых пар
_Файл: `docs/NETWORK.md` | 2 колонок, 20 строк_

| Пара | Общих файлов |
|------|-------------|
| **Cowork** ↔ **ingit** | 59 |
| **Svyazi** ↔ **NGT** | 50 |
| **Svyazi** ↔ **CardIndex** | 48 |
| **Svyazi** ↔ **Yodoca** | 46 |
| **Svyazi** ↔ **AgentFS** | 44 |
| **Svyazi** ↔ **AI Factory** | 44 |
| **CardIndex** ↔ **NGT** | 44 |
| **Yodoca** ↔ **NGT** | 44 |
| **CardIndex** ↔ **AgentFS** | 42 |
| **NGT** ↔ **AI Factory** | 42 |
| **Svyazi** ↔ **mclaude** | 40 |
| **AgentFS** ↔ **AI Factory** | 40 |
| **Yodoca** ↔ **AI Factory** | 40 |
| **CardIndex** ↔ **Yodoca** | 39 |
| **AgentFS** ↔ **Yodoca** | 39 |
| **AgentFS** ↔ **NGT** | 39 |
| **NGT** ↔ **mclaude** | 39 |
| **AI Factory** ↔ **mclaude** | 39 |
| **Svyazi** ↔ **LiteParse** | 38 |
| **CardIndex** ↔ **AI Factory** | 38 |


### 78. Центральность узлов (влиятельность)
_Файл: `docs/NETWORK.md` | 3 колонок, 20 строк_

| Узел | Балл центральности | Тип |
|------|--------------------|-----|
| **Svyazi** | 553 | 📦 Проект |
| **NGT** | 515 | 📦 Проект |
| **CardIndex** | 493 | 📦 Проект |
| **Yodoca** | 475 | 📦 Проект |
| **AgentFS** | 466 | 📦 Проект |
| **AI Factory** | 457 | 📦 Проект |
| **mclaude** | 431 | 📦 Проект |
| **knowledge-space** | 409 | 📦 Проект |
| **LiteParse** | 403 | 📦 Проект |
| **Rufler** | 395 | 📦 Проект |
| **SENTINEL** | 383 | 📦 Проект |
| **Lorenzo (svend4)** | 271 | 👤 Автор |
| **MemNet** | 228 | 📦 Проект |
| **Cowork** | 214 | 📦 Проект |
| **ingit** | 213 | 📦 Проект |
| **Lorenzo** | 191 | 📦 Проект |
| **Андрей (kksudo)** | 181 | 👤 Автор |
| **Виталий (spbmolot)** | 150 | 👤 Автор |
| **Wikontic** | 140 | 📦 Проект |
| **Firecrawl** | 90 | 📦 Проект |


### 79. Структура документации
_Файл: `docs/ONBOARDING.md` | 4 колонок, 5 строк_

| Раздел | Тема | Файлов | Слов |
|--------|------|--------|------|
| [`docs/01-svyazi/`](docs/01-svyazi/README.md) | Архитектура Svyazi 2.0 | 16 | 10,166 |
| [`docs/02-anthropic-vacancies/`](docs/02-anthropic-vacancies/README.md) | Вакансии Anthropic | 357 | 260,851 |
| [`docs/03-technology-combinations/`](docs/03-technology-combinations/README.md) | Комбинации технологий | 7 | 2,433 |
| [`docs/04-ai-collaborations/`](docs/04-ai-collaborations/README.md) | AI-коллаборации | 17 | 24,521 |
| [`docs/05-habr-projects/`](docs/05-habr-projects/README.md) | Хабр-проекты | 10 | 8,296 |


### 80. Ключевые документы
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


### 81. Архитектура компонентов
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


### 82. Топ-20 по объёму (важные и изолированные)
_Файл: `docs/ORPHANS.md` | 3 колонок, 0 строк_

| Файл | Слов | Раздел |
|------|------|--------|


### 83. Типы проблем
_Файл: `docs/PARAGRAPH_QUALITY.md` | 2 колонок, 5 строк_

| Тип | Кол-во |
|-----|--------|
| ⚪ Короткий абзац | 3783 |
| ✂️  Оборванный | 2186 |
| 📏 Длинное предложение | 174 |
| 🔁 Повтор начала | 1021 |
| ♊ Дубль | 54 |


### 84. Состояние компонентов
_Файл: `docs/PROGRESS.md` | 3 колонок, 5 строк_

| Компонент | Статус | Детали |
|-----------|--------|--------|
| Контакты авторов | ⚠️ 14 файлов, не отправлено | 14 файлов в docs/contacts/ |
| LLM-обогащение | ⬜ не запущено | pip install anthropic && python scripts/improve_llm_enrich.py |
| Скрипты обработки | ✅ 114 скриптов | 4 LLM-скриптов, MCP=✅ |
| DIGEST.md | ✅ 5 секций | python scripts/improve_llm_summary.py |
| Claude Skills | ✅ 5 скиллов | review-docs, status, write-contact, improve, analyze-project |


### 85. Метрики качества
_Файл: `docs/PROGRESS.md` | 3 колонок, 3 строк_

| Метрика | Балл | Статус |
|---------|------|--------|
| Здоровье репо (HEALTH) | 75.0/100 | 🟡 |
| Качество доков (METRICS) | 67.5/100 | 🟡 |
| Go/No-Go (SCORING) | 96.0/100 | 🟢 |


### 86. Содержание
_Файл: `docs/READING_ORDER.md` | 5 колонок, 395 строк_

| # | Уровень | Документ | Слов | Предварительно прочитать |
|---|---------|----------|------|--------------------------|
| 1 | 🟢 Начало | [Svyazi 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 496 | — |
| 2 | 🟡 Средний | [04-ensembles-overview](docs/01-svyazi/04-ensembles-overview.md) | 1087 | — |
| 3 | 🟢 Начало | [Продолжение исследования для Svyazi 2.0](docs/01-svyazi/00-intro-part2.md) | 6 | — |
| 4 | 🟢 Начало | [Методика и рамка отбора проектов](docs/01-svyazi/02-methodology.md) | 325 | — |
| 5 | 🟡 Средний | [03-component-catalog](docs/01-svyazi/03-component-catalog.md) | 1201 | — |
| 6 | 🟢 Начало | [11-integration-contracts](docs/01-svyazi/11-integration-contracts.md) | 566 | `09-architectural-gaps.md` |
| 7 | 🟢 Начало | [09-architectural-gaps](docs/01-svyazi/09-architectural-gaps.md) | 580 | `01-executive-summary.md`, `03-component-catalog.md` |
| 8 | 🟢 Начало | [10-second-order-ensembles](docs/01-svyazi/10-second-order-ensembles.md) | 740 | `04-ensembles-overview.md` |
| 9 | 🟢 Начало | [06-security-privacy](docs/01-svyazi/06-security-privacy.md) | 662 | — |
| 10 | 🟢 Начало | [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md) | 863 | — |
| 11 | 🟢 Начало | [12-roadmap](docs/01-svyazi/12-roadmap.md) | 577 | `07-mvp-planning.md`, `11-integration-contracts.md` |
| 12 | 🟢 Начало | [13-contacts](docs/01-svyazi/13-contacts.md) | 661 | — |
| 13 | 🟢 Начало | [14-limitations](docs/01-svyazi/14-limitations.md) | 487 | — |
| 14 | 🟢 Начало | [08-conclusions](docs/01-svyazi/08-conclusions.md) | 220 | — |
| 15 | 🟢 Начало | [Синтез: как проекты собираются вместе](docs/05-habr-projects/01-synthesis.md) | 70 | — |
| 16 | 🟢 Начало | [Авторы и контакты](docs/05-habr-projects/02-collaboration-partners.md) | 128 | — |
| 17 | 🟢 Начало | [Wikontic: семантический граф](docs/05-habr-projects/knowledge/wikontic.md) | 116 | — |
| 18 | 🟢 Начало | [NGT Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 207 | — |
| 19 | 🟢 Начало | [Yodoca: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 105 | — |
| 20 | 🟡 Средний | [MemNet: исследовательская память](docs/05-habr-projects/memory/memnet.md) | 7010 | — |
| 21 | 🟢 Начало | [Executive summary](docs/04-ai-collaborations/01-executive-summary.md) | 367 | — |
| 22 | 🟡 Средний | [Введение](docs/04-ai-collaborations/00-intro.md) | 11115 | — |
| 23 | 🟢 Начало | [Методика и рамка отбора](docs/04-ai-collaborations/02-методика-и-рамка-отбора.md) | 250 | — |
| 24 | 🟡 Средний | [Карта найденных проектов и паттернов](docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) | 1251 | — |
| 25 | 🟢 Начало | [Приоритетные ансамбли](docs/04-ai-collaborations/04-приоритетные-ансамбли.md) | 1086 | — |
| 26 | 🟢 Начало | [План прототипа и возможные контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) | 870 | — |
| 27 | 🟢 Начало | [Безопасность, приватность и бюджетный роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) | 668 | — |
| 28 | 🟢 Начало | [Выводы](docs/04-ai-collaborations/07-выводы.md) | 234 | — |
| 29 | 🟢 Начало | [Что это продолжение добавляет](docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md) | 233 | — |
| 30 | 🟢 Начало | [Архитектурные зазоры, которые важнее новых ин](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | 583 | — |
| 31 | 🟢 Начало | [Новые ансамбли следующего шага](docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) | 745 | — |
| 32 | 🟢 Начало | [Интеграционный контракт, который стоит зафикс](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | 611 | — |
| 33 | 🟢 Начало | [Дорожная карта прототипа следующей итерации](docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md) | 584 | — |
| 34 | 🟢 Начало | [Контактная стратегия и узкие вопросы для авто](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) | 671 | — |
| 35 | 🟡 Средний | [Ограничения, лицензии и что пока лучше не скл](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md) | 3004 | — |
| 36 | 🟢 Начало | [Агентные системы и роутинг](docs/03-technology-combinations/01-agent-routing.md) | 197 | — |
| 37 | 🟢 Начало | [Графы знаний и Legal AI](docs/03-technology-combinations/02-knowledge-graphs.md) | 676 | — |
| 38 | 🟢 Начало | [Local-first и P2P стек](docs/03-technology-combinations/03-local-first.md) | 293 | — |
| 39 | 🟢 Начало | [Домен: немецкое социальное право](docs/03-technology-combinations/04-sozialrecht-domain.md) | 136 | — |
| 40 | 🟢 Начало | [Бенчмарки и производительность](docs/03-technology-combinations/05-benchmarks.md) | 794 | — |
| 41 | 🟢 Начало | [Executive Summary](docs/02-anthropic-vacancies/153-executive-summary.md) | 266 | — |
| 42 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/38-content-overview.md) | 103 | — |
| 43 | 🔴 Продвинутый | [Интегральный анализ профиля svend4](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | 19018 | — |
| 44 | 🟢 Начало | [README-MCP.md— инструкция по установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) | 66 | — |
| 45 | 🟢 Начало | [README.md](docs/02-anthropic-vacancies/65-readme-md.md) | 57 | — |
| 46 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/48-content-overview.md) | 117 | — |
| 47 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/58-content-overview.md) | 112 | — |
| 48 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/12-content-overview.md) | 14 | — |
| 49 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/31-content-overview.md) | 13 | — |
| 50 | 🔴 Продвинутый | [Введение](docs/02-anthropic-vacancies/00-intro.md) | 8819 | — |
| 51 | 🟢 Начало | [1. Introduction](docs/02-anthropic-vacancies/76-1-introduction.md) | 384 | — |
| 52 | 🟢 Начало | [REVIEW_METHODOLOGY.md](docs/02-anthropic-vacancies/105-review-methodology-md.md) | 42 | — |
| 53 | 🟢 Начало | [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md) | 267 | — |
| 54 | 🔴 Продвинутый | [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md) | 3080 | — |
| 55 | 🟢 Начало | [4. Architecture of Professional Colleague Age](docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md) | 792 | — |
| 56 | 🟢 Начало | [2. The Double-Triangle Architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) | 638 | — |
| 57 | 🟡 Средний | [Appendix C: Quick-Start Architecture for SGB ](docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md) | 1584 | — |
| 58 | 🟢 Начало | [4. The Symbiotic Architecture](docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md) | 499 | — |
| 59 | 🟢 Начало | [PORTAL-PROTOCOL.md](docs/02-anthropic-vacancies/03-portal-protocol-md.md) | 43 | — |
| 60 | 🟢 Начало | [THE DOUBLE-TRIANGLE ARCHITECTURE.md](docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md) | 14 | — |
| 61 | 🟢 Начало | [10. Risks Specific to Composite Architectures](docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md) | 674 | — |
| 62 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/04-abstract.md) | 98 | — |
| 63 | 🟢 Начало | [0. Status of This Document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md) | 69 | — |
| 64 | 🟢 Начало | [11. Security Considerations](docs/02-anthropic-vacancies/23-11-security-considerations.md) | 139 | — |
| 65 | 🟢 Начало | [15. Security Considerations](docs/02-anthropic-vacancies/90-15-security-considerations.md) | 228 | — |
| 66 | 🟢 Начало | [2. Terminology](docs/02-anthropic-vacancies/07-2-terminology.md) | 226 | — |
| 67 | 🟢 Начало | [3. Registry (`nautilus.json`)](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) | 290 | — |
| 68 | 🟢 Начало | [4. Passport (`passport.md`)](docs/02-anthropic-vacancies/09-4-passport-passport-md.md) | 92 | — |
| 69 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/13-angle-perspective.md) | 23 | — |
| 70 | 🟢 Начало | [History](docs/02-anthropic-vacancies/16-history.md) | 77 | — |
| 71 | 🟢 Начало | [5. Compatibility Levels](docs/02-anthropic-vacancies/17-5-compatibility-levels.md) | 178 | — |
| 72 | 🟢 Начало | [6. Adapter Interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md) | 274 | — |
| 73 | 🟢 Начало | [7. PortalEntry Structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md) | 161 | — |
| 74 | 🟢 Начало | [8. Consensus Algorithm](docs/02-anthropic-vacancies/20-8-consensus-algorithm.md) | 213 | — |
| 75 | 🟢 Начало | [9. Query Flow](docs/02-anthropic-vacancies/21-9-query-flow.md) | 121 | — |
| 76 | 🟢 Начало | [10. QueryResult Structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md) | 94 | — |
| 77 | 🟢 Начало | [12. Versioning Policy](docs/02-anthropic-vacancies/24-12-versioning-policy.md) | 121 | — |
| 78 | 🟢 Начало | [13. Reference Implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md) | 60 | — |
| 79 | 🟢 Начало | [14. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) | 146 | — |
| 80 | 🟢 Начало | [15. Glossary of Examples](docs/02-anthropic-vacancies/27-15-glossary-of-examples.md) | 68 | — |
| 81 | 🟢 Начало | [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) | 128 | — |
| 82 | 🟢 Начало | [Appendix B: Change Log](docs/02-anthropic-vacancies/34-appendix-b-change-log.md) | 488 | — |
| 83 | 🟢 Начало | [passports/info1.md](docs/02-anthropic-vacancies/35-passports-info1-md.md) | 47 | — |
| 84 | 🟢 Начало | [Essence](docs/02-anthropic-vacancies/36-essence.md) | 96 | — |
| 85 | 🟢 Начало | [Native Format](docs/02-anthropic-vacancies/37-native-format.md) | 149 | — |
| 86 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/39-angle-perspective.md) | 88 | — |
| 87 | 🟢 Начало | [Bridges](docs/02-anthropic-vacancies/40-bridges.md) | 105 | — |
| 88 | 🟢 Начало | [Compatibility Level](docs/02-anthropic-vacancies/41-compatibility-level.md) | 60 | — |
| 89 | 🟢 Начало | [Author & Contact](docs/02-anthropic-vacancies/42-author-contact.md) | 49 | — |
| 90 | 🟢 Начало | [History](docs/02-anthropic-vacancies/43-history.md) | 89 | — |
| 91 | 🟢 Начало | [For the Curious: Philosophy](docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md) | 114 | — |
| 92 | 🟢 Начало | [passports/pro2.md](docs/02-anthropic-vacancies/45-passports-pro2-md.md) | 53 | — |
| 93 | 🟢 Начало | [Essence](docs/02-anthropic-vacancies/46-essence.md) | 88 | — |
| 94 | 🟢 Начало | [Native Format](docs/02-anthropic-vacancies/47-native-format.md) | 110 | — |
| 95 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/49-angle-perspective.md) | 77 | — |
| 96 | 🟢 Начало | [Bridges](docs/02-anthropic-vacancies/50-bridges.md) | 114 | — |
| 97 | 🟢 Начало | [Compatibility Level](docs/02-anthropic-vacancies/51-compatibility-level.md) | 64 | — |
| 98 | 🟢 Начало | [Author & Contact](docs/02-anthropic-vacancies/52-author-contact.md) | 68 | — |
| 99 | 🟢 Начало | [History](docs/02-anthropic-vacancies/53-history.md) | 113 | — |
| 100 | 🟢 Начало | [For the Curious: Philosophy](docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md) | 119 | — |
| 101 | 🟢 Начало | [passports/meta.md](docs/02-anthropic-vacancies/55-passports-meta-md.md) | 50 | — |
| 102 | 🟢 Начало | [Essence](docs/02-anthropic-vacancies/56-essence.md) | 108 | — |
| 103 | 🟢 Начало | [Native Format](docs/02-anthropic-vacancies/57-native-format.md) | 108 | — |
| 104 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/59-angle-perspective.md) | 91 | — |
| 105 | 🟢 Начало | [Bridges](docs/02-anthropic-vacancies/60-bridges.md) | 75 | — |
| 106 | 🟢 Начало | [Compatibility Level](docs/02-anthropic-vacancies/61-compatibility-level.md) | 63 | — |
| 107 | 🟢 Начало | [Author & Contact](docs/02-anthropic-vacancies/62-author-contact.md) | 47 | — |
| 108 | 🟢 Начало | [History](docs/02-anthropic-vacancies/63-history.md) | 108 | — |
| 109 | 🟢 Начало | [For the Curious: Philosophy](docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md) | 558 | — |
| 110 | 🟢 Начало | [🇷🇺 О проекте](docs/02-anthropic-vacancies/67-о-проекте.md) | 715 | — |
| 111 | 🟢 Начало | [🇬🇧 About](docs/02-anthropic-vacancies/68-about.md) | 788 | — |
| 112 | 🔴 Продвинутый | [⬡](docs/02-anthropic-vacancies/69-section.md) | 9414 | — |
| 113 | 🟢 Начало | [Зачем две версии параллельно](docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md) | 73 | — |
| 114 | 🟢 Начало | [Критерии выбора для фазы 3](docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md) | 109 | — |
| 115 | 🟡 Средний | [Расписание фазы 3](docs/02-anthropic-vacancies/72-расписание-фазы-3.md) | 742 | — |
| 116 | 🟢 Начало | [PORTAL-PROTOCOL.md v1.1](docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md) | 63 | — |
| 117 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/74-abstract.md) | 172 | — |
| 118 | 🟢 Начало | [0. Status of This Document](docs/02-anthropic-vacancies/75-0-status-of-this-document.md) | 90 | — |
| 119 | 🟢 Начало | [2. Terminology](docs/02-anthropic-vacancies/77-2-terminology.md) | 316 | — |
| 120 | 🟢 Начало | [3. Registry (`nautilus.json`)](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md) | 412 | — |
| 121 | 🟡 Средний | [4. Passport (`passport.md`)](docs/02-anthropic-vacancies/79-4-passport-passport-md.md) | 238 | — |
| 122 | 🟢 Начало | [5. Compatibility Levels](docs/02-anthropic-vacancies/80-5-compatibility-levels.md) | 245 | — |
| 123 | 🟢 Начало | [6. Adapter Interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md) | 256 | — |
| 124 | 🟢 Начало | [7. PortalEntry Structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md) | 216 | — |
| 125 | 🟡 Средний | [8. Q6 Space (Normative)](docs/02-anthropic-vacancies/83-8-q6-space-normative.md) | 342 | — |
| 126 | 🟢 Начало | [9. Consensus Algorithm](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md) | 289 | — |
| 127 | 🟢 Начало | [10. Query Flow](docs/02-anthropic-vacancies/85-10-query-flow.md) | 167 | — |
| 128 | 🟢 Начало | [11. Relevance Ranking](docs/02-anthropic-vacancies/86-11-relevance-ranking.md) | 144 | — |
| 129 | 🟡 Средний | [12. Onboarding Paths (Normative)](docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md) | 395 | — |
| 130 | 🟡 Средний | [13. REST API Contract (Normative for Portals)](docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md) | 367 | — |
| 131 | 🟢 Начало | [14. SDK Contract (Informative)](docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md) | 132 | — |
| 132 | 🟢 Начало | [16. MCP Extension (Informative)](docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md) | 100 | — |
| 133 | 🟢 Начало | [17. Versioning Policy](docs/02-anthropic-vacancies/92-17-versioning-policy.md) | 159 | — |
| 134 | 🟢 Начало | [18. Reference Implementation](docs/02-anthropic-vacancies/93-18-reference-implementation.md) | 150 | — |
| 135 | 🟢 Начало | [19. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) | 162 | — |
| 136 | 🟢 Начало | [20. ADR-002: Q6 as First-Class Protocol Conce](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) | 149 | — |
| 137 | 🟢 Начало | [21. ADR-003: Five Onboarding Paths as Equal-R](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md) | 113 | — |
| 138 | 🟢 Начало | [22. Glossary of Reference Examples](docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md) | 163 | — |
| 139 | 🟡 Средний | [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md) | 203 | — |
| 140 | 🟢 Начало | [Доступ к данным](docs/02-anthropic-vacancies/102-доступ-к-данным.md) | 23 | — |
| 141 | 🟢 Начало | [Appendix B: Change Log](docs/02-anthropic-vacancies/103-appendix-b-change-log.md) | 121 | — |
| 142 | 🟢 Начало | [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) | 852 | — |
| 143 | 🟢 Начало | [TL;DR](docs/02-anthropic-vacancies/106-tl-dr.md) | 96 | — |
| 144 | 🟢 Начало | [1. Контекст и мотивация](docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md) | 314 | — |
| 145 | 🟡 Средний | [2. Формальный workflow](docs/02-anthropic-vacancies/108-2-формальный-workflow.md) | 338 | — |
| 146 | 🟢 Начало | [3. Принципы консолидации (Фаза C)](docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md) | 417 | — |
| 147 | 🟢 Начало | [Вопрос: fallback-ratio как критический или ос](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) | 215 | — |
| 148 | 🟢 Начало | [4. Условия применимости](docs/02-anthropic-vacancies/111-4-условия-применимости.md) | 191 | — |
| 149 | 🟢 Начало | [5. Связь с существующими методологиями](docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) | 263 | — |
| 150 | 🟢 Начало | [6. Почему это валидный паттерн для AI-assiste](docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) | 142 | — |
| 151 | 🟢 Начало | [7. Реализация в проекте Nautilus](docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md) | 204 | — |
| 152 | 🟢 Начало | [8. Ограничения и открытые вопросы](docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md) | 310 | — |
| 153 | 🟢 Начало | [9. Checklist применения методологии](docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md) | 237 | — |
| 154 | 🟢 Начало | [10. Конкретный план применения к текущим доку](docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md) | 176 | — |
| 155 | 🟢 Начало | [Appendix A: Шаблон для header warning](docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md) | 145 | — |
| 156 | 🟢 Начало | [Appendix B: Примеры расхождений и их разрешен](docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md) | 207 | — |
| 157 | 🟢 Начало | [Главные технические риски](docs/02-anthropic-vacancies/120-главные-технические-риски.md) | 74 | — |
| 158 | 🟢 Начало | [Appendix C: История изменений методологии](docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md) | 47 | — |
| 159 | 🟡 Средний | [Глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md) | 1189 | — |
| 160 | 🟡 Средний | [portal-mcp.py](docs/02-anthropic-vacancies/123-portal-mcp-py.md) | 2194 | — |
| 161 | 🟢 Начало | [Конфигурация для Claude Desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) | 145 | — |
| 162 | 🟢 Начало | [Установка](docs/02-anthropic-vacancies/126-установка.md) | 96 | — |
| 163 | 🟢 Начало | [Подключение к Claude Desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md) | 71 | — |
| 164 | 🟢 Начало | [Доступные инструменты](docs/02-anthropic-vacancies/128-доступные-инструменты.md) | 104 | — |
| 165 | 🟢 Начало | [Примеры запросов (в Claude)](docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md) | 78 | — |
| 166 | 🟢 Начало | [Отладка](docs/02-anthropic-vacancies/130-отладка.md) | 123 | — |
| 167 | 🟢 Начало | [Ограничения текущей версии (0.1.0-draft)](docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md) | 70 | — |
| 168 | 🟢 Начало | [Planned (v0.2.0)](docs/02-anthropic-vacancies/132-planned-v0-2-0.md) | 49 | — |
| 169 | 🔴 Продвинутый | [Обратная связь](docs/02-anthropic-vacancies/133-обратная-связь.md) | 16887 | — |
| 170 | 🟢 Начало | [A Formal Model for Human-AI Collaboration in ](docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md) | 59 | — |
| 171 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/136-abstract.md) | 284 | — |
| 172 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/137-table-of-contents.md) | 62 | — |
| 173 | 🟢 Начало | [1. Why Single-Triangle Models Are Incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) | 417 | — |
| 174 | 🟢 Начало | [3. Three Inter-Layer Protocols](docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md) | 754 | — |
| 175 | 🟢 Начало | [4. Nautilus Portal as Reference Substrate](docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md) | 580 | — |
| 176 | 🟢 Начало | [5. Pattern Library as Bridge Between Triangle](docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md) | 578 | — |
| 177 | 🟢 Начало | [6. Four Deployment Domains](docs/02-anthropic-vacancies/143-6-four-deployment-domains.md) | 582 | — |
| 178 | 🟢 Начало | [7. Open Questions](docs/02-anthropic-vacancies/144-7-open-questions.md) | 663 | — |
| 179 | 🟢 Начало | [8. Call to Action](docs/02-anthropic-vacancies/145-8-call-to-action.md) | 639 | — |
| 180 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/146-acknowledgments.md) | 145 | — |
| 181 | 🟢 Начало | [References](docs/02-anthropic-vacancies/147-references.md) | 230 | — |
| 182 | 🟢 Начало | [Appendix A: Glossary](docs/02-anthropic-vacancies/148-appendix-a-glossary.md) | 216 | — |
| 183 | 🟢 Начало | [Appendix B: Summary of Contributions](docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md) | 153 | — |
| 184 | 🔴 Продвинутый | [Appendix C: Version History](docs/02-anthropic-vacancies/150-appendix-c-version-history.md) | 8274 | — |
| 185 | 🟢 Начало | [OPEN KNOWLEDGE WORK FOUNDATION.md](docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md) | 17 | — |
| 186 | 🟢 Начало | [AI-Coordinated Infrastructure for Distributed](docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md) | 54 | — |
| 187 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/154-table-of-contents.md) | 57 | — |
| 188 | 🟢 Начало | [1. Problem Statement](docs/02-anthropic-vacancies/155-1-problem-statement.md) | 534 | — |
| 189 | 🟢 Начало | [2. Target Populations](docs/02-anthropic-vacancies/156-2-target-populations.md) | 601 | — |
| 190 | 🟢 Начало | [3. Why Existing Solutions Fail](docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md) | 612 | — |
| 191 | 🟢 Начало | [4. Proposed Infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md) | 905 | — |
| 192 | 🟢 Начало | [5. Economic Model](docs/02-anthropic-vacancies/159-5-economic-model.md) | 490 | — |
| 193 | 🟢 Начало | [6. Governance and Ethics](docs/02-anthropic-vacancies/160-6-governance-and-ethics.md) | 429 | — |
| 194 | 🟢 Начало | [7. Phased Rollout Plan](docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md) | 565 | — |
| 195 | 🟢 Начало | [8. Risk Analysis](docs/02-anthropic-vacancies/162-8-risk-analysis.md) | 576 | — |
| 196 | 🟢 Начало | [9. Call for Partnership](docs/02-anthropic-vacancies/163-9-call-for-partnership.md) | 411 | — |
| 197 | 🟢 Начало | [10. Appendices](docs/02-anthropic-vacancies/164-10-appendices.md) | 871 | — |
| 198 | 🔴 Продвинутый | [Closing](docs/02-anthropic-vacancies/165-closing.md) | 9170 | — |
| 199 | 🟢 Начало | [REPRESENTATIVE AGENT LAYER.md](docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) | 19 | — |
| 200 | 🟢 Начало | [AI-Mediated Representation for Underrepresent](docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md) | 76 | — |
| 201 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/168-abstract.md) | 246 | — |
| 202 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/169-table-of-contents.md) | 77 | — |
| 203 | 🟢 Начало | [1. The Cinderella Syndrome: Why Quality Stays](docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md) | 749 | — |
| 204 | 🟢 Начало | [2. Historical Precedents: Agents as Civilizat](docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md) | 865 | — |
| 205 | 🟢 Начало | [3. What Makes a Representative Agent](docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md) | 577 | — |
| 206 | 🟢 Начало | [4. Ten Domains of Application](docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md) | 1491 | — |
| 207 | 🟢 Начало | [5. Architectural Specification](docs/02-anthropic-vacancies/174-5-architectural-specification.md) | 571 | — |
| 208 | 🟢 Начало | [6. Ethical Framework](docs/02-anthropic-vacancies/175-6-ethical-framework.md) | 398 | — |
| 209 | 🟢 Начало | [7. Governance and Oversight](docs/02-anthropic-vacancies/176-7-governance-and-oversight.md) | 335 | — |
| 210 | 🟢 Начало | [8. Risks and Mitigations](docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md) | 439 | — |
| 211 | 🟢 Начало | [9. Phased Rollout Strategy](docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md) | 420 | — |
| 212 | 🟢 Начало | [10. Open Questions](docs/02-anthropic-vacancies/179-10-open-questions.md) | 319 | — |
| 213 | 🟢 Начало | [11. Call for Collaboration](docs/02-anthropic-vacancies/180-11-call-for-collaboration.md) | 327 | — |
| 214 | 🟢 Начало | [12. Closing](docs/02-anthropic-vacancies/181-12-closing.md) | 178 | — |
| 215 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/182-acknowledgments.md) | 124 | — |
| 216 | 🟢 Начало | [References](docs/02-anthropic-vacancies/183-references.md) | 209 | — |
| 217 | 🟢 Начало | [Appendix A: Connection to Companion Papers](docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md) | 120 | — |
| 218 | 🟢 Начало | [Appendix B: Domain Comparison Matrix](docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md) | 155 | — |
| 219 | 🟡 Средний | [Appendix C: Sample Use Cases in Detail](docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md) | 1910 | — |
| 220 | 🟢 Начало | [СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md](docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) | 18 | — |
| 221 | 🟢 Начало | [AI-опосредованное представительство для недоп](docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md) | 74 | — |
| 222 | 🟢 Начало | [Аннотация](docs/02-anthropic-vacancies/189-аннотация.md) | 254 | — |
| 223 | 🟢 Начало | [Содержание](docs/02-anthropic-vacancies/190-содержание.md) | 70 | — |
| 224 | 🟢 Начало | [1. Синдром Золушки: Почему качество остаётся ](docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md) | 721 | — |
| 225 | 🟢 Начало | [2. Исторические прецеденты: Агенты как цивили](docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md) | 861 | — |
| 226 | 🟢 Начало | [3. Что делает агента Представительским](docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md) | 553 | — |
| 227 | 🟢 Начало | [4. Десять областей применения](docs/02-anthropic-vacancies/194-4-десять-областей-применения.md) | 1524 | — |
| 228 | 🟢 Начало | [5. Архитектурная спецификация](docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md) | 553 | — |
| 229 | 🟢 Начало | [6. Этическая рамка](docs/02-anthropic-vacancies/196-6-этическая-рамка.md) | 409 | — |
| 230 | 🟢 Начало | [7. Управление и надзор](docs/02-anthropic-vacancies/197-7-управление-и-надзор.md) | 337 | — |
| 231 | 🟢 Начало | [8. Риски и меры противодействия](docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md) | 448 | — |
| 232 | 🟢 Начало | [9. Стратегия поэтапного развёртывания](docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md) | 419 | — |
| 233 | 🟢 Начало | [10. Открытые вопросы](docs/02-anthropic-vacancies/200-10-открытые-вопросы.md) | 306 | — |
| 234 | 🟢 Начало | [11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md) | 320 | — |
| 235 | 🟢 Начало | [12. Заключение](docs/02-anthropic-vacancies/202-12-заключение.md) | 185 | — |
| 236 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/203-благодарности.md) | 145 | — |
| 237 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/204-ссылки.md) | 203 | — |
| 238 | 🟢 Начало | [Приложение A: Связь с Сопроводительными Стать](docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md) | 118 | — |
| 239 | 🟢 Начало | [Приложение B: Матрица Сравнения Областей](docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md) | 157 | — |
| 240 | 🔴 Продвинутый | [Приложение C: Образцы Случаев Использования в](docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md) | 3972 | — |
| 241 | 🟢 Начало | [PROFESSIONAL COLLEAGUE AGENTS.md](docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md) | 14 | — |
| 242 | 🟢 Начало | [A Typology of AI Agents on the Principal Side](docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md) | 91 | — |
| 243 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/210-abstract.md) | 255 | — |
| 244 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/211-table-of-contents.md) | 80 | — |
| 245 | 🟡 Средний | [1. The Five-Type Typology of Principal-Side A](docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md) | 819 | — |
| 246 | 🟢 Начало | [2. What Makes a Professional Colleague Agent](docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md) | 731 | — |
| 247 | 🟢 Начало | [3. Empirical Case Study: «Обучай»](docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md) | 751 | — |
| 248 | 🟢 Начало | [5. The Economics of Profession-Wide Replicati](docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md) | 641 | — |
| 249 | 🟢 Начало | [6. Risks Specific to this Category](docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md) | 1084 | — |
| 250 | 🟢 Начало | [7. Application Domains](docs/02-anthropic-vacancies/218-7-application-domains.md) | 634 | — |
| 251 | 🟢 Начало | [8. Pilot Proposal: SGB Advocate Colleague](docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md) | 872 | — |
| 252 | 🟢 Начало | [9. Relationship to Other Agent Types](docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md) | 565 | — |
| 253 | 🟢 Начало | [10. Open Questions](docs/02-anthropic-vacancies/221-10-open-questions.md) | 314 | — |
| 254 | 🟢 Начало | [11. Call for Collaboration](docs/02-anthropic-vacancies/222-11-call-for-collaboration.md) | 267 | — |
| 255 | 🟢 Начало | [12. Closing](docs/02-anthropic-vacancies/223-12-closing.md) | 303 | — |
| 256 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/224-acknowledgments.md) | 118 | — |
| 257 | 🟢 Начало | [References](docs/02-anthropic-vacancies/225-references.md) | 225 | — |
| 258 | 🟢 Начало | [Appendix A: Comparative Table — Five Agent Ty](docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md) | 269 | — |
| 259 | 🟢 Начало | [Appendix B: Decision Framework — When to Buil](docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md) | 221 | — |
| 260 | 🟢 Начало | [ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ](docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md) | 77 | — |
| 261 | 🟢 Начало | [Аннотация](docs/02-anthropic-vacancies/230-аннотация.md) | 220 | — |
| 262 | 🟢 Начало | [Содержание](docs/02-anthropic-vacancies/231-содержание.md) | 77 | — |
| 263 | 🟡 Средний | [1. Типология из пяти типов агентов на стороне](docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md) | 770 | — |
| 264 | 🟢 Начало | [2. Что делает агента Профессиональным Коллего](docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md) | 645 | — |
| 265 | 🟢 Начало | [3. Эмпирический кейс: «Обучай»](docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md) | 705 | — |
| 266 | 🟢 Начало | [4. Архитектура Профессиональных Коллег-Агенто](docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md) | 749 | — |
| 267 | 🟢 Начало | [5. Экономика тиражирования по профессии](docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md) | 632 | — |
| 268 | 🟢 Начало | [6. Риски, специфичные для этой категории](docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md) | 1067 | — |
| 269 | 🟢 Начало | [7. Области применения](docs/02-anthropic-vacancies/238-7-области-применения.md) | 642 | — |
| 270 | 🟢 Начало | [8. Пилотное предложение: SGB Колega-Адвокат](docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md) | 906 | — |
| 271 | 🟢 Начало | [9. Связь с другими типами агентов](docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md) | 493 | — |
| 272 | 🟢 Начало | [10. Открытые вопросы](docs/02-anthropic-vacancies/241-10-открытые-вопросы.md) | 298 | — |
| 273 | 🟢 Начало | [11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md) | 258 | — |
| 274 | 🟢 Начало | [12. Заключение](docs/02-anthropic-vacancies/243-12-заключение.md) | 282 | — |
| 275 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/244-благодарности.md) | 107 | — |
| 276 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/245-ссылки.md) | 210 | — |
| 277 | 🟢 Начало | [Приложение A: Сравнительная Таблица — Пять Ти](docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md) | 272 | — |
| 278 | 🟢 Начало | [Приложение B: Рамка принятия решений — когда ](docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md) | 211 | — |
| 279 | 🔴 Продвинутый | [Приложение C: Архитектура Быстрого Старта для](docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md) | 3347 | — |
| 280 | 🟢 Начало | [COMPOSITE SKILLS AGENT.md](docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) | 15 | — |
| 281 | 🟢 Начало | [Bridging the Gap Between Profession-Wide and ](docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md) | 16 | — |
| 282 | 🟢 Начало | [AI Support Through Configurable Specialist En](docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md) | 78 | — |
| 283 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/252-abstract.md) | 252 | — |
| 284 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/253-table-of-contents.md) | 84 | — |
| 285 | 🟢 Начало | [1. Why the Binary View Is Incomplete](docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md) | 595 | — |
| 286 | 🟢 Начало | [2. The Twenty-One Teachers Pattern](docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md) | 724 | — |
| 287 | 🟢 Начало | [3. What Makes a Composite Skills Agent](docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md) | 842 | — |
| 288 | 🟢 Начало | [4. The Sub-Agent Registry](docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md) | 691 | — |
| 289 | 🟢 Начало | [5. Configuration: How Principals Build Their ](docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md) | 635 | — |
| 290 | 🟢 Начало | [6. Coordination and Disagreement Resolution](docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md) | 697 | — |
| 291 | 🟢 Начало | [7. Economics of Combinatorial Replication](docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md) | 679 | — |
| 292 | 🟢 Начало | [8. Seven Domains of Application](docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md) | 890 | — |
| 293 | 🟢 Начало | [9. Integration with OKWF Infrastructure](docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md) | 636 | — |
| 294 | 🟢 Начало | [11. Open Questions](docs/02-anthropic-vacancies/264-11-open-questions.md) | 410 | — |
| 295 | 🟢 Начало | [12. Call for Collaboration](docs/02-anthropic-vacancies/265-12-call-for-collaboration.md) | 305 | — |
| 296 | 🟢 Начало | [13. Closing](docs/02-anthropic-vacancies/266-13-closing.md) | 344 | — |
| 297 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/267-acknowledgments.md) | 203 | — |
| 298 | 🟢 Начало | [References](docs/02-anthropic-vacancies/268-references.md) | 269 | — |
| 299 | 🟢 Начало | [Appendix A: The Six-Type Taxonomy (Updated)](docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md) | 173 | — |
| 300 | 🟢 Начало | [Appendix B: Sub-Agent Registry Schema (Sketch](docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md) | 223 | — |
| 301 | 🟢 Начало | [Appendix C: Configuration Template Example](docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md) | 210 | — |
| 302 | 🔴 Продвинутый | [Appendix D: Connection Diagram](docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md) | 3736 | — |
| 303 | 🟢 Начало | [INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECT](docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md) | 20 | — |
| 304 | 🟢 Начало | [The Missing Middle Layer Between Chat and Cod](docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md) | 147 | — |
| 305 | 🟢 Начало | [Why This Document Exists](docs/02-anthropic-vacancies/275-why-this-document-exists.md) | 256 | — |
| 306 | 🟢 Начало | [The Two-Layer Stack As It Exists](docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md) | 291 | — |
| 307 | 🟢 Начало | [What's Missing — Layer B](docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md) | 375 | — |
| 308 | 🟢 Начало | [Why This Hasn't Been Built](docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md) | 291 | — |
| 309 | 🟢 Начало | [Existing Approximations](docs/02-anthropic-vacancies/279-existing-approximations.md) | 417 | — |
| 310 | 🟢 Начало | [The Specific Case in Front of Us](docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md) | 565 | — |
| 311 | 🟢 Начало | [The Recursive Insight](docs/02-anthropic-vacancies/281-the-recursive-insight.md) | 277 | — |
| 312 | 🟢 Начало | [What Industry Will Likely Build](docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md) | 225 | — |
| 313 | 🟢 Начало | [What This Document Doesn't Solve](docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md) | 155 | — |
| 314 | 🟢 Начало | [Practical Recommendations for the Current Pro](docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md) | 276 | — |
| 315 | 🟢 Начало | [Closing](docs/02-anthropic-vacancies/285-closing.md) | 176 | — |
| 316 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/286-acknowledgments.md) | 153 | — |
| 317 | 🟢 Начало | [References](docs/02-anthropic-vacancies/287-references.md) | 164 | — |
| 318 | 🟢 Начало | [Appendix: Position in Series Visualization](docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md) | 945 | — |
| 319 | 🟢 Начало | [ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛ](docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md) | 157 | — |
| 320 | 🟢 Начало | [Почему этот документ существует](docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md) | 213 | — |
| 321 | 🟢 Начало | [Двухслойный стек, как он существует](docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md) | 263 | — |
| 322 | 🟢 Начало | [Что отсутствует — Слой B](docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md) | 348 | — |
| 323 | 🟢 Начало | [Почему это не было построено](docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md) | 267 | — |
| 324 | 🟢 Начало | [Существующие приближения](docs/02-anthropic-vacancies/294-существующие-приближения.md) | 389 | — |
| 325 | 🟢 Начало | [Конкретный случай перед нами](docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md) | 494 | — |
| 326 | 🟢 Начало | [Рекурсивное прозрение](docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md) | 264 | — |
| 327 | 🟢 Начало | [Что промышленность вероятно построит](docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md) | 214 | — |
| 328 | 🟢 Начало | [Что этот документ не решает](docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md) | 134 | — |
| 329 | 🟢 Начало | [Практические рекомендации для текущего проект](docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md) | 268 | — |
| 330 | 🟢 Начало | [Заключение](docs/02-anthropic-vacancies/300-заключение.md) | 162 | — |
| 331 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/301-благодарности.md) | 133 | — |
| 332 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/302-ссылки.md) | 152 | — |
| 333 | 🔴 Продвинутый | [Приложение: Визуализация позиции в серии](docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md) | 6963 | — |
| 334 | 🟢 Начало | [INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md) | 20 | — |
| 335 | 🟢 Начало | [A Practical Path to Layer B Through Symbiotic](docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md) | 24 | — |
| 336 | 🟢 Начало | [with Anthropic's Cowork Platform](docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md) | 172 | — |
| 337 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/307-abstract.md) | 215 | — |
| 338 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/308-table-of-contents.md) | 89 | — |
| 339 | 🟢 Начало | [1. The Cowork Discovery and Why It Changes Ev](docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md) | 587 | — |
| 340 | 🟢 Начало | [2. What Cowork Provides That InGit Doesn't Ne](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md) | 561 | — |
| 341 | 🟢 Начало | [3. What InGit Provides That Cowork Lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md) | 747 | — |
| 342 | 🟢 Начало | [5. Four Integration Paths in Order of Accessi](docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md) | 691 | — |
| 343 | 🟢 Начало | [6. Refined InGit Scope with Cowork in Mind](docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md) | 332 | — |
| 344 | 🟢 Начало | [7. Practical First Steps This Month](docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md) | 322 | — |
| 345 | 🟢 Начало | [8. Implications for Nautilus and OKWF](docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md) | 494 | — |
| 346 | 🟢 Начало | [9. Risks and Open Questions](docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md) | 439 | — |
| 347 | 🟢 Начало | [10. Strategic Positioning](docs/02-anthropic-vacancies/318-10-strategic-positioning.md) | 645 | — |
| 348 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/319-acknowledgments.md) | 278 | — |
| 349 | 🟢 Начало | [References](docs/02-anthropic-vacancies/320-references.md) | 98 | — |
| 350 | 🟢 Начало | [Appendix A: Decision Tree for InGit Adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md) | 149 | — |
| 351 | 🟢 Начало | [Appendix B: Comparison Matrix](docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md) | 181 | — |
| 352 | 🟡 Средний | [Appendix C: Sample InGit MCP Server Tool Spec](docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md) | 1431 | — |
| 353 | 🟢 Начало | [INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБ](docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md) | 195 | — |
| 354 | 🟢 Начало | [Аннотация](docs/02-anthropic-vacancies/325-аннотация.md) | 210 | — |
| 355 | 🟢 Начало | [Содержание](docs/02-anthropic-vacancies/326-содержание.md) | 85 | — |
| 356 | 🟢 Начало | [1. Открытие Cowork и почему это меняет всё](docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md) | 554 | — |
| 357 | 🟢 Начало | [2. Что Cowork обеспечивает, что InGit не нужн](docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md) | 496 | — |
| 358 | 🟢 Начало | [3. Что InGit обеспечивает, чего Cowork не хва](docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md) | 759 | — |
| 359 | 🟢 Начало | [4. Симбиотическая Архитектура](docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md) | 494 | — |
| 360 | 🟢 Начало | [5. Четыре пути интеграции в порядке доступнос](docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md) | 681 | — |
| 361 | 🟢 Начало | [6. Уточнённый объём InGit с учётом Cowork](docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md) | 324 | — |
| 362 | 🟢 Начало | [7. Практические первые шаги в этом месяце](docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md) | 323 | — |
| 363 | 🟢 Начало | [8. Импликации для Nautilus и OKWF](docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md) | 484 | — |
| 364 | 🟢 Начало | [9. Риски и Открытые Вопросы](docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md) | 449 | — |
| 365 | 🟢 Начало | [10. Стратегическое Позиционирование](docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md) | 627 | — |
| 366 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/337-благодарности.md) | 253 | — |
| 367 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/338-ссылки.md) | 96 | — |
| 368 | 🟢 Начало | [Приложение A: Дерево Решений для Принимающих ](docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md) | 148 | — |
| 369 | 🟢 Начало | [Приложение B: Сравнительная Матрица](docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md) | 185 | — |
| 370 | 🔴 Продвинутый | [Приложение C: Образец Спецификаций Инструмент](docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md) | 20301 | — |
| 371 | 🔴 Продвинутый | [Что такое Вариант C — Concept Document для An](docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md) | 11149 | — |
| 372 | 🔴 Продвинутый | [Lorenzo Catalyst Agent — глубокая проработка ](docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md) | 5725 | — |
| 373 | 🟢 Начало | [СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT](docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md) | 21 | — |
| 374 | 🟢 Начало | [Кто ты](docs/02-anthropic-vacancies/345-кто-ты.md) | 125 | — |
| 375 | 🟢 Начало | [Твоё происхождение](docs/02-anthropic-vacancies/346-твоё-происхождение.md) | 148 | — |
| 376 | 🟢 Начало | [Твоя миссия](docs/02-anthropic-vacancies/347-твоя-миссия.md) | 107 | — |
| 377 | 🟢 Начало | [Кому ты служишь (слоистая модель)](docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md) | 96 | — |
| 378 | 🟢 Начало | [Твоя личность](docs/02-anthropic-vacancies/349-твоя-личность.md) | 196 | — |
| 379 | 🟢 Начало | [Твои языки и культурные nuances](docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md) | 155 | — |
| 380 | 🟢 Начало | [Что ты МОЖЕШЬ делать](docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md) | 109 | — |
| 381 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать без Max approval](docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md) | 98 | — |
| 382 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать вообще](docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md) | 94 | — |
| 383 | 🟢 Начало | [Существующий landscape collaborators (твоя wo](docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md) | 258 | — |
| 384 | 🟢 Начало | [Существующие документы DHLab (твой context)](docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md) | 138 | — |
| 385 | 🟢 Начало | [Твой workflow](docs/02-anthropic-vacancies/356-твой-workflow.md) | 165 | — |
| 386 | 🟢 Начало | [Твоя коммуникация в outreach](docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md) | 169 | — |
| 387 | 🟢 Начало | [Твоя relationship с другими AI](docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md) | 149 | — |
| 388 | 🟢 Начало | [Твои anti-patterns](docs/02-anthropic-vacancies/359-твои-anti-patterns.md) | 121 | — |
| 389 | 🟢 Начало | [Что ты ВСЕГДА делаешь](docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md) | 74 | — |
| 390 | 🟢 Начало | [Когда ты Honestly не знаешь](docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md) | 77 | — |
| 391 | 🟢 Начало | [Когда сомневаешься — escalate к Max](docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md) | 75 | — |
| 392 | 🟢 Начало | [Твоя identity как persistent character](docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md) | 115 | — |
| 393 | 🟡 Средний | [Final note: Ты — experiment](docs/02-anthropic-vacancies/364-final-note-ты-experiment.md) | 1337 | — |
| 394 | 🔴 Продвинутый | [Развёрнутый анализ «внуковой» комбинации](docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md) | 4286 | — |
| 395 | 🔴 Продвинутый | [Технический stack (Svyazi 2.0 foundation)](docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md) | 3765 | — |


### 87. Общая картина
_Файл: `docs/REPORT.md` | 2 колонок, 9 строк_

| Показатель | Значение |
|------------|---------|
| Всего документов | **456** |
| Всего слов | **374,611** |
| Скриптов обработки | **50** |
| Индекс здоровья | **75/100** |
| Проектов в сети | **22** |
| Связей проектов | **185** |
| Кластеров документов | **120** |
| Ошибок валидации | **0** |
| Предупреждений | **16** |


### 88. Структура репозитория
_Файл: `docs/REPORT.md` | 3 колонок, 5 строк_

| Раздел | Файлов | Описание |
|--------|--------|---------|
| `01-svyazi` | 16 | Архитектура Svyazi 2.0 |
| `02-anthropic-vacancies` | 357 | 436 вакансий Anthropic |
| `03-technology-combinations` | 7 | 40+ комбинаций технологий |
| `04-ai-collaborations` | 17 | AI-ансамбли OSS-проектов |
| `05-habr-projects` | 10 | Хабр-проекты: память, граф |


### 89. Топ навигационных документов
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


### 90. Реестр
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


### 91. Упоминания рисков в документах
_Файл: `docs/RISK_REGISTER.md` | 2 колонок, 12 строк_

| Источник | Фрагмент |
|----------|---------|
| `01-executive-summary` | [^sentinel]: OSS-проект: безопасность и allowlist для MCP [^rufler]: OSS-проект: оркестратор AI-аген… |
| `02-methodology` | иде улучшают доказуемость, безопасность, локальность или стоимость выполнения Когда у статьи не было… |
| `03-component-catalog` | w1turn20view18 | Рантайм‑безопасность и бюджетный execution plane для агентных систем. | SENTINEL[… |
| `04-ensembles-overview` | ри минимальном интеграционном риске**. **Проекты:** Svyazi[^svyazi], CardIndex[^cardindex], AgentFS[… |
| `04-ensembles-overview` | а**: Self‑Aware MCP закрывает проблемы часового пояса, ОС, даты и локации. citeturn20view12turn30… |
| `06-security-privacy` | t, collaboration --> ## Безопасность, приватность и бюджетный роутинг Для Svyazi‑2.0 безопасная архи… |
| `06-security-privacy` | Похожие документы:** - [06-безопасность-приватность-и-бюджетный-роутинг](docs/04-ai-collaborations/0… |
| `06-security-privacy` | cs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) (сходство 1.00) - [05-пл… |
| `06-security-privacy` | **Смотрите также:** - [06-безопасность-приватность-и-бюджетный-роутинг](docs/04-ai-collaborations/06… |
| `07-mvp-planning` | l Search + базовые правила безопасности | Удержать стоимость и не утонуть в MCP[^mcp]/context overhe… |
| `07-mvp-planning` | review для inferred | Снизить риск ложных связей и утечек | 1–2 дня | **Итого**: реалистичный MVP — … |
| `07-mvp-planning` | нных компонентов. **Ключевые риски и как их закрывать** | Риск | Почему это важно | Снижение риска |… |


### 92. Итоговая статистика
_Файл: `docs/RISK_REGISTER.md` | 2 колонок, 3 строк_

| Уровень | Кол-во |
|---------|--------|
| 🔴 КРИТИЧЕСКИЙ | 1 |
| 🟠 ВЫСОКИЙ | 7 |
| 🟡 СРЕДНИЙ | 2 |


### 93. Ключевые вехи
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


### 94. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 6 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Executive Summary существует | ✅ | 10 |
| Архитектурные контракты описаны | ✅ | 10 |
| MVP план задокументирован | ✅ | 10 |
| Дорожная карта есть | ✅ | 8 |
| README в каждом разделе | ✅ | 5 |
| Глоссарий создан | ✅ | 5 |


### 95. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 5 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Компоненты каталогизированы (20+) | ✅ | 10 |
| Ансамбли определены (5+) | ✅ | 10 |
| Архитектурные пробелы выявлены | ✅ | 8 |
| Безопасность и PII описаны | ✅ | 8 |
| Граф связей проектов построен | ✅ | 5 |


### 96. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 3 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Контакты авторов компонентов есть | ✅ | 10 |
| Авторы Habr-проектов найдены | ✅ | 8 |
| Шаблоны для связи созданы | ✅ | 5 |


### 97. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 5 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Риски выявлены и задокументированы | ✅ | 8 |
| Лицензии проверены | ✅ | 8 |
| Сломанных ссылок < 30 | ✅ | 5 |
| Дублей нет | ❌ | 5 |
|  ↳ _Есть точные дубли документов_ | | |


### 98. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 4 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Прогресс MVP отслеживается | ✅ | 8 |
| Action items задокументированы | ✅ | 8 |
| Порядок чтения задан | ✅ | 5 |
| Executive report создан | ✅ | 5 |


### 99. Тональность по разделам
_Файл: `docs/SENTIMENT.md` | 6 колонок, 8 строк_

| Раздел | Оптимизм | Скептицизм | Срочность | Неопределённость | Тон |
|--------|----------|------------|-----------|-----------------|-----|
| **01-svyazi** | 2.3‰ | 6.5‰ | 2.9‰ | 0.5‰ | 🔴 скептичный |
| **02-anthropic-vacancies** | 1.8‰ | 5.6‰ | 1.9‰ | 1.6‰ | 🔴 скептичный |
| **03-technology-combinations** | 3.8‰ | 1.3‰ | 0.8‰ | 0.4‰ | 🟢 оптимистичный |
| **04-ai-collaborations** | 2.4‰ | 4.2‰ | 1.4‰ | 0.8‰ | 🔴 скептичный |
| **05-habr-projects** | 3.7‰ | 1.1‰ | 0.6‰ | 1.4‰ | 🟢 оптимистичный |
| **contacts** | 0.0‰ | 0.0‰ | 0.0‰ | 0.0‰ | ⚪ нейтральный |
| **root** | 0.5‰ | 21.3‰ | 1.5‰ | 0.7‰ | 🔴 скептичный |
| **templates** | 0.0‰ | 20.5‰ | 0.0‰ | 0.0‰ | 🔴 скептичный |


### 100. Самые оптимистичные документы
_Файл: `docs/SENTIMENT.md` | 3 колонок, 10 строк_

| Документ | Оптимизм‰ | Тон |
|----------|----------|-----|
| `193-3-что-делает-агента-представите` | 17.3 | 🟢 оптимистичный |
| `110-вопрос-fallback-ratio-как-крити` | 17.2 | 🟠 срочный |
| `128-доступные-инструменты` | 14.7 | 🟢 оптимистичный |
| `08-3-registry-nautilus-json` | 14.7 | 🟠 срочный |
| `19-7-portalentry-structure` | 14.3 | 🟠 срочный |
| `232-1-типология-из-пяти-типов-агент` | 13.9 | 🟢 оптимистичный |
| `248-приложение-c-архитектура-быстро` | 13.0 | 🟢 оптимистичный |
| `23-11-security-considerations` | 10.8 | 🟠 срочный |
| `78-3-registry-nautilus-json` | 10.3 | 🟠 срочный |
| `82-7-portalentry-structure` | 10.3 | 🟠 срочный |


### 101. Самые скептичные / риск-ориентированные
_Файл: `docs/SENTIMENT.md` | 3 колонок, 10 строк_

| Документ | Скептицизм‰ | Тон |
|----------|------------|-----|
| `PARAGRAPH_QUALITY` | 247.8 | 🔴 скептичный |
| `ensemble` | 59.3 | 🔴 скептичный |
| `162-8-risk-analysis` | 49.9 | 🔴 скептичный |
| `263-10-risks-specific-to-composite-` | 44.5 | 🔴 скептичный |
| `README` | 39.2 | 🔴 скептичный |
| `198-8-риски-и-меры-противодействия` | 37.5 | 🔴 скептичный |
| `RISK_REGISTER` | 34.2 | 🔴 скептичный |
| `177-8-risks-and-mitigations` | 34.0 | 🔴 скептичный |
| `237-6-риски-специфичные-для-этой-ка` | 33.7 | 🔴 скептичный |
| `217-6-risks-specific-to-this-catego` | 32.8 | 🔴 скептичный |


### 102. Распределение тональности
_Файл: `docs/SENTIMENT.md` | 2 колонок, 5 строк_

| Тон | Файлов |
|-----|--------|
| 🔴 скептичный | 213 |
| ⚪ нейтральный | 133 |
| 🟠 срочный | 44 |
| 🟢 оптимистичный | 33 |
| 🟡 неопределённый | 14 |


### 103. Топ-20 самых похожих пар
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


### 104. Мета-документы
_Файл: `docs/SITEMAP.md` | 3 колонок, 47 строк_

| Документ | Описание | Слов |
|----------|----------|------|
| [ACTION_ITEMS.md](docs/ACTION_ITEMS.md) | Задачи и риски (490) | 5786 |
| [AUTHORS.md](docs/AUTHORS.md) | Авторы и контакты | 164 |
| [BROKEN_LINKS.md](docs/BROKEN_LINKS.md) | Сломанные ссылки (26) | 406 |
| [CHANGELOG.md](docs/CHANGELOG.md) | История изменений | 189 |
| [CLUSTERS.md](docs/CLUSTERS.md) | Кластеры (384 → 120 групп) | 1201 |
| [CODE_BLOCKS.md](docs/CODE_BLOCKS.md) | — | 3500 |
| [COMPARE.md](docs/COMPARE.md) | Сравнение с предыдущим коммитом | 477 |
| [COMPLEXITY.md](docs/COMPLEXITY.md) | Оценка читаемости | 591 |
| [CONCEPTS.md](docs/CONCEPTS.md) | Глоссарий понятий (888) | 11283 |
| [CONSISTENCY.md](docs/CONSISTENCY.md) | — | 222 |
| [CONTACTS.md](docs/CONTACTS.md) | Контакты (15 авторов) | 436 |
| [CROSSREFS.md](docs/CROSSREFS.md) | Перекрёстные ссылки проектов | 638 |
| [DECISIONS.md](docs/DECISIONS.md) | Ключевые решения (150) | 1747 |
| [DENSITY.md](docs/DENSITY.md) | Карта плотности тем | 638 |
| [DUPLICATES.md](docs/DUPLICATES.md) | — | 85 |
| [ENTITIES.md](docs/ENTITIES.md) | Именованные сущности | 736 |
| [GLOSSARY.md](docs/GLOSSARY.md) | Глоссарий проектов (33 записи) | 231 |
| [GRAPH.md](docs/GRAPH.md) | Граф связей проектов | 2670 |
| [HEALTH.md](docs/HEALTH.md) | Дашборд здоровья (75/100) | 154 |
| [KPI.md](docs/KPI.md) | Числовые KPI (737 показателей) | 2293 |
| [LINKS.md](docs/LINKS.md) | Внешние ссылки | 633 |
| [MINDMAP.md](docs/MINDMAP.md) | Майндмап в Mermaid | 245 |
| [MISSING.md](docs/MISSING.md) | Пробелы знаний | 434 |
| [PRIORITIES.md](docs/PRIORITIES.md) | Приоритеты (TF-IDF) | 1016 |
| [QA.md](docs/01-svyazi/QA.md) | Вопросы и ответы | 200 |
| [QA.md](docs/02-anthropic-vacancies/QA.md) | Вопросы и ответы | 340 |
| [QA.md](docs/03-technology-combinations/QA.md) | Вопросы и ответы | 125 |
| [QA.md](docs/04-ai-collaborations/QA.md) | Вопросы и ответы | 244 |
| [QA.md](docs/05-habr-projects/QA.md) | Вопросы и ответы | 131 |
| [QA.md](docs/QA.md) | Вопросы и ответы | 1491 |
| [QUESTIONS.md](docs/QUESTIONS.md) | Открытые вопросы (484) | 1555 |
| [READING_ORDER.md](docs/READING_ORDER.md) | Рекомендуемый порядок чтения | 5965 |
| [README.md](docs/01-svyazi/README.md) | Главная страница и навигация | 313 |
| [README.md](docs/02-anthropic-vacancies/README.md) | Главная страница и навигация | 3693 |
| [README.md](docs/03-technology-combinations/README.md) | Главная страница и навигация | 76 |
| [README.md](docs/04-ai-collaborations/README.md) | Главная страница и навигация | 328 |
| [README.md](docs/05-habr-projects/README.md) | Главная страница и навигация | 70 |
| [README.md](docs/05-habr-projects/knowledge/README.md) | Главная страница и навигация | 39 |
| [README.md](docs/05-habr-projects/memory/README.md) | Главная страница и навигация | 73 |
| [README.md](docs/README.md) | Главная страница и навигация | 54 |
| [SEARCH.md](docs/SEARCH.md) | Поисковый индекс | 3494 |
| [SIMILAR.md](docs/SIMILAR.md) | Похожие документы (937 пар) | 284 |
| [STATS.md](docs/STATS.md) | Детальная статистика | 426 |
| [TABLES.md](docs/TABLES.md) | — | 15624 |
| [TAGS.md](docs/TAGS.md) | Теги (316 файлов, 12 тем) | 604 |
| [TIMELINE.md](docs/TIMELINE.md) | Временная шкала (800 маркеров) | 3975 |
| [WORD_FREQ.md](docs/WORD_FREQ.md) | Частотный анализ слов | 1248 |


### 105. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 14 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Продолжение исследования для Svyazi 2.0](docs/01-svyazi/00-intro-part2.md) | 6 |
| 2 | [Svyazi 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 514 |
| 3 | [Методика и рамка отбора проектов](docs/01-svyazi/02-methodology.md) | 339 |
| 4 | [03-component-catalog](docs/01-svyazi/03-component-catalog.md) | 1219 |
| 5 | [04-ensembles-overview](docs/01-svyazi/04-ensembles-overview.md) | 1105 |
| 6 | [06-security-privacy](docs/01-svyazi/06-security-privacy.md) | 680 |
| 7 | [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md) | 881 |
| 8 | [08-conclusions](docs/01-svyazi/08-conclusions.md) | 238 |
| 9 | [09-architectural-gaps](docs/01-svyazi/09-architectural-gaps.md) | 598 |
| 10 | [10-second-order-ensembles](docs/01-svyazi/10-second-order-ensembles.md) | 758 |
| 11 | [11-integration-contracts](docs/01-svyazi/11-integration-contracts.md) | 584 |
| 12 | [12-roadmap](docs/01-svyazi/12-roadmap.md) | 595 |
| 13 | [13-contacts](docs/01-svyazi/13-contacts.md) | 679 |
| 14 | [14-limitations](docs/01-svyazi/14-limitations.md) | 505 |


### 106. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 51 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Введение](docs/02-anthropic-vacancies/00-intro.md) | 8837 |
| 2 | [Интегральный анализ профиля svend4](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | 19036 |
| 3 | [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md) | 3098 |
| 4 | [PORTAL-PROTOCOL.md](docs/02-anthropic-vacancies/03-portal-protocol-md.md) | 61 |
| 5 | [Abstract](docs/02-anthropic-vacancies/04-abstract.md) | 108 |
| 6 | [0. Status of This Document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md) | 87 |
| 7 | [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md) | 281 |
| 8 | [2. Terminology](docs/02-anthropic-vacancies/07-2-terminology.md) | 244 |
| 9 | [3. Registry (`nautilus.json`)](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) | 308 |
| 10 | [4. Passport (`passport.md`)](docs/02-anthropic-vacancies/09-4-passport-passport-md.md) | 106 |
| 11 | [Доступ к данным](docs/02-anthropic-vacancies/102-доступ-к-данным.md) | 23 |
| 12 | [Appendix B: Change Log](docs/02-anthropic-vacancies/103-appendix-b-change-log.md) | 139 |
| 13 | [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) | 870 |
| 14 | [REVIEW_METHODOLOGY.md](docs/02-anthropic-vacancies/105-review-methodology-md.md) | 60 |
| 15 | [TL;DR](docs/02-anthropic-vacancies/106-tl-dr.md) | 114 |
| 16 | [1. Контекст и мотивация](docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md) | 328 |
| 17 | [2. Формальный workflow](docs/02-anthropic-vacancies/108-2-формальный-workflow.md) | 356 |
| 18 | [3. Принципы консолидации (Фаза C)](docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md) | 427 |
| 19 | [Вопрос: fallback-ratio как критический или осмысле](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) | 215 |
| 20 | [4. Условия применимости](docs/02-anthropic-vacancies/111-4-условия-применимости.md) | 201 |
| 21 | [5. Связь с существующими методологиями](docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) | 263 |
| 22 | [6. Почему это валидный паттерн для AI-assisted wor](docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) | 142 |
| 23 | [7. Реализация в проекте Nautilus](docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md) | 222 |
| 24 | [8. Ограничения и открытые вопросы](docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md) | 320 |
| 25 | [9. Checklist применения методологии](docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md) | 237 |
| 26 | [10. Конкретный план применения к текущим документа](docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md) | 190 |
| 27 | [Appendix A: Шаблон для header warning](docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md) | 145 |
| 28 | [Appendix B: Примеры расхождений и их разрешения](docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md) | 207 |
| 29 | [Content Overview](docs/02-anthropic-vacancies/12-content-overview.md) | 24 |
| 30 | [Главные технические риски](docs/02-anthropic-vacancies/120-главные-технические-риски.md) | 74 |
| 31 | [Appendix C: История изменений методологии](docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md) | 47 |
| 32 | [Глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md) | 1207 |
| 33 | [portal-mcp.py](docs/02-anthropic-vacancies/123-portal-mcp-py.md) | 2212 |
| 34 | [Конфигурация для Claude Desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) | 159 |
| 35 | [README-MCP.md— инструкция по установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) | 84 |
| 36 | [Установка](docs/02-anthropic-vacancies/126-установка.md) | 96 |
| 37 | [Подключение к Claude Desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md) | 85 |
| 38 | [Доступные инструменты](docs/02-anthropic-vacancies/128-доступные-инструменты.md) | 122 |
| 39 | [Примеры запросов (в Claude)](docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md) | 96 |
| 40 | [Angle / Perspective](docs/02-anthropic-vacancies/13-angle-perspective.md) | 37 |
| 41 | [Отладка](docs/02-anthropic-vacancies/130-отладка.md) | 137 |
| 42 | [Ограничения текущей версии (0.1.0-draft)](docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md) | 80 |
| 43 | [Planned (v0.2.0)](docs/02-anthropic-vacancies/132-planned-v0-2-0.md) | 59 |
| 44 | [Обратная связь](docs/02-anthropic-vacancies/133-обратная-связь.md) | 16905 |
| 45 | [THE DOUBLE-TRIANGLE ARCHITECTURE.md](docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md) | 32 |
| 46 | [A Formal Model for Human-AI Collaboration in Distr](docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md) | 77 |
| 47 | [Abstract](docs/02-anthropic-vacancies/136-abstract.md) | 302 |
| 48 | [Table of Contents](docs/02-anthropic-vacancies/137-table-of-contents.md) | 80 |
| 49 | [1. Why Single-Triangle Models Are Incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) | 435 |
| 50 | [2. The Double-Triangle Architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) | 656 |
| ... | _ещё 305 файлов_ | |


### 107. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 5 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Агентные системы и роутинг](docs/03-technology-combinations/01-agent-routing.md) | 207 |
| 2 | [Графы знаний и Legal AI](docs/03-technology-combinations/02-knowledge-graphs.md) | 690 |
| 3 | [Local-first и P2P стек](docs/03-technology-combinations/03-local-first.md) | 311 |
| 4 | [Домен: немецкое социальное право](docs/03-technology-combinations/04-sozialrecht-domain.md) | 146 |
| 5 | [Бенчмарки и производительность](docs/03-technology-combinations/05-benchmarks.md) | 808 |


### 108. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 15 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Введение](docs/04-ai-collaborations/00-intro.md) | 11133 |
| 2 | [Executive summary](docs/04-ai-collaborations/01-executive-summary.md) | 385 |
| 3 | [Методика и рамка отбора](docs/04-ai-collaborations/02-методика-и-рамка-отбора.md) | 264 |
| 4 | [Карта найденных проектов и паттернов](docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) | 1269 |
| 5 | [Приоритетные ансамбли](docs/04-ai-collaborations/04-приоритетные-ансамбли.md) | 1104 |
| 6 | [План прототипа и возможные контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) | 888 |
| 7 | [Безопасность, приватность и бюджетный роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) | 686 |
| 8 | [Выводы](docs/04-ai-collaborations/07-выводы.md) | 252 |
| 9 | [Что это продолжение добавляет](docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md) | 251 |
| 10 | [Архитектурные зазоры, которые важнее новых инструм](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | 601 |
| 11 | [Новые ансамбли следующего шага](docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) | 763 |
| 12 | [Интеграционный контракт, который стоит зафиксирова](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | 629 |
| 13 | [Дорожная карта прототипа следующей итерации](docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md) | 602 |
| 14 | [Контактная стратегия и узкие вопросы для авторов](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) | 689 |
| 15 | [Ограничения, лицензии и что пока лучше не склеиват](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md) | 3022 |


### 109. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 6 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Синтез: как проекты собираются вместе](docs/05-habr-projects/01-synthesis.md) | 80 |
| 2 | [Авторы и контакты](docs/05-habr-projects/02-collaboration-partners.md) | 138 |
| 3 | [Wikontic: семантический граф](docs/05-habr-projects/knowledge/wikontic.md) | 130 |
| 4 | [MemNet: исследовательская память](docs/05-habr-projects/memory/memnet.md) | 7028 |
| 5 | [NGT Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 217 |
| 6 | [Yodoca: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 115 |


### 110. Без метаданных (нет summary или тегов) — 150 файлов
_Файл: `docs/STALENESS.md` | 3 колонок, 20 строк_

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/00-intro-part2.md` | 5 | нет summary, нет тегов, короткий (5 слов) |
| `docs/01-svyazi/03-component-catalog.md` | 1149 | нет summary |
| `docs/01-svyazi/QA.md` | 245 | нет summary, нет тегов |
| `docs/01-svyazi/README.md` | 339 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/04-abstract.md` | 116 | нет тегов |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | 109 | нет тегов |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 20 | нет summary, нет тегов, короткий (20 слов) |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 142 | нет тегов |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | 129 | нет тегов |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | 221 | нет тегов |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 20 | нет summary, нет тегов, короткий (20 слов) |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 41 | нет тегов, короткий (41 слов) |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | 165 | нет тегов |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | 83 | нет тегов, короткий (83 слов) |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | 34 | нет summary, нет тегов, короткий (34 слов) |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | 87 | нет тегов, короткий (87 слов) |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 29 | нет summary, нет тегов, короткий (29 слов) |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 32 | нет summary, нет тегов, короткий (32 слов) |
| `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` | 461 | нет тегов |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 30 | нет summary, короткий (30 слов) |


### 111. Короткие (< 100 слов, заготовки) — 39 файлов
_Файл: `docs/STALENESS.md` | 2 колонок, 20 строк_

| Файл | Слов |
|------|------|
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | 65 |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | 92 |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | 64 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 62 |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | 88 |
| `docs/02-anthropic-vacancies/126-установка.md` | 86 |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | 62 |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | 82 |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | 85 |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | 77 |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | 70 |
| `docs/02-anthropic-vacancies/16-history.md` | 65 |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | 99 |
| `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` | 96 |
| `docs/02-anthropic-vacancies/190-содержание.md` | 88 |
| `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` | 98 |
| `docs/02-anthropic-vacancies/25-13-reference-implementation.md` | 85 |
| `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` | 94 |
| `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` | 84 |
| `docs/02-anthropic-vacancies/35-passports-info1-md.md` | 64 |


### 112. Сводная таблица по разделам
_Файл: `docs/STATS.md` | 8 колонок, 7 строк_

| Раздел | Файлов | Слов | H2 | Таблиц | Блоков кода | Ссылок | Жирного |
|--------|--------|------|----|--------|-------------|--------|---------|
| **01-svyazi** | 16 | 8,952 | 33 | 43 | 8 | 15 | 249 |
| **02-anthropic-vacancies** | 357 | 250,120 | 475 | 130 | 189 | 1571 | 2976 |
| **03-technology-combinations** | 7 | 2,269 | 10 | 5 | 0 | 9 | 12 |
| **04-ai-collaborations** | 17 | 22,808 | 31 | 39 | 0 | 64 | 265 |
| **05-habr-projects** | 10 | 7,877 | 14 | 0 | 0 | 86 | 21 |
| **root** | 29 | 64,876 | 244 | 1397 | 83 | 1749 | 2117 |
| **ИТОГО** | **436** | **356,902** | **807** | **1614** | **280** | **3494** | **5640** |


### 113. Топ-20 файлов по объёму
_Файл: `docs/STATS.md` | 5 колонок, 20 строк_

| Файл | Слов | H2 | Таблиц | Код |
|------|------|----|--------|-----|
| `341-приложение-c-образец-спецификаций-ин` | 20301 | 2 | 0 | 11 |
| `01-интегральный-анализ-профиля-svend4` | 19018 | 2 | 0 | 19 |
| `133-обратная-связь` | 16887 | 2 | 6 | 17 |
| `TABLES` | 15606 | 5 | 474 | 1 |
| `CONCEPTS` | 11265 | 54 | 0 | 0 |
| `342-что-такое-вариант-c-concept-document` | 11149 | 2 | 0 | 6 |
| `00-intro` | 11115 | 0 | 0 | 0 |
| `69-section` | 9414 | 2 | 2 | 18 |
| `165-closing` | 9170 | 2 | 0 | 1 |
| `00-intro` | 8819 | 1 | 4 | 2 |
| `150-appendix-c-version-history` | 8274 | 2 | 0 | 2 |
| `memnet` | 7010 | 1 | 0 | 0 |
| `303-приложение-визуализация-позиции-в-се` | 6963 | 2 | 0 | 2 |
| `READING_ORDER` | 5947 | 1 | 198 | 0 |
| `ACTION_ITEMS` | 5768 | 7 | 0 | 0 |
| `343-lorenzo-catalyst-agent-глубокая-прор` | 5725 | 2 | 0 | 2 |
| `365-развёрнутый-анализ-внуковой-комбинац` | 4286 | 2 | 4 | 3 |
| `207-приложение-c-образцы-случаев-использ` | 3972 | 2 | 0 | 2 |
| `TIMELINE` | 3957 | 8 | 95 | 1 |
| `366-технический-stack-svyazi-2-0-foundat` | 3765 | 2 | 13 | 7 |


### 114. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **MCP Protocol** | Инструменты | Стандарт интеграции AI-инструментов — Anthropic |
| **CardIndex** | Компоненты | 785+ карточек знаний, MIT, стабильный API |
| **AgentFS** | Компоненты | Файловая система для AI-агентов, MIT, kksudo |
| **Firecrawl** | Инструменты | Веб-краулер для AI, MIT, активная разработка |
| **Python 3.11+** | Платформа | Основной язык реализации всех компонентов |
| **Markdown docs** | Практики | 96% готовности, проверено на 460+ файлах |


### 115. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **Yodoca** | Компоненты | Память с консолидацией, Apache 2.0, spbmolot |
| **SENTINEL** | Компоненты | Allowlist безопасности для MCP |
| **Rufler** | Компоненты | Оркестратор агентов, активная разработка |
| **RAG + Graph** | Архитектура | Гибридный поиск: векторный + граф-обход |
| **claude-haiku-4-5** | Модели | Оптимум цена/качество для enrichment задач |
| **CRDT-синхронизация** | Архитектура | Бесконфликтная репликация для multi-agent |


### 116. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **NGT-memory** | Компоненты | Ассоциативный граф памяти, BSL 1.1 |
| **knowledge-space** | Компоненты | База знаний, MIT, нужна оценка API |
| **Wikontic** | Компоненты | Граф знаний, статус неизвестен |
| **MCP Tool Search** | Компоненты | Динамический поиск инструментов |
| **claude-opus-4-7** | Модели | Для сложных reasoning задач, высокая стоимость |
| **Local-first P2P** | Архитектура | GDPR-safe распределённые данные |


### 117. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 4 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **BSL 1.1 libs** | Лицензии | Ограничения при коммерческом использовании |
| **Monolithic LLM** | Архитектура | Один LLM вместо ансамбля — узкое место |
| **Без PII-защиты** | Практики | Обработка данных без SENTINEL/quarantine |
| **Hard-coded prompts** | Практики | Промпты без версионирования и тестов |


### 118. Точная дата (152)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `2026-04-19` | pendix B: Change Log ### v1.1.0-draft (2026-04-19) - **New**: Q6 as normative concept (section 8, ADR-002) - | `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` |
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
| ... | _ещё 122 записей_ | |


### 119. Точная дата (152)
_Файл: `docs/TIMELINE.md` | 3 колонок, 28 строк_

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
| `2024 год` | 00-intro_ - 2019 года, после изменений 2024 года применяется иначе»); _→ 00-intro_ - 2019 года, после и | `docs/ACTION_ITEMS.md` |
| `2026 год` | стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор **B:** `docs/01-sv | `docs/CONTRADICTIONS.md` |
| `2026 год` | ates / / `март 2026` / 6 / dates / / `в 2026 году` / 6 / dates / / `апреля 2026` / 6 / dates / / `декабрь 20 | `docs/NAMED_ENTITIES.md` |
| `2026 год` | стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: | `docs/NARRATIVE.md` |
| `2026 год` | Файл / /--------/----------/------/ / `2026 год` / стыковать, то на Хабре за первые месяцы 2026 года уже сл | `docs/TABLES.md` |
| `2025 год` | ic-vacancies/203-благодарности.md` / / `2025 год` / Кириллом Дьологом сервис «Обучай» летом 2025 года. К апр | `docs/TABLES.md` |
| `2027 год` | ic-vacancies/244-благодарности.md` / / `2027 год` / к функциональности Projects через 2026-2027 годы. **GitH | `docs/TABLES.md` |
| `2024 год` | anthropic-vacancies/69-section.md` / / `2024 год` / «это решение 2019 года, после изменений 2024 года примен | `docs/TABLES.md` |


### 120. Точная дата (152)
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
| `апрель 2026` | *Объём:** 74 документа (по состоянию на апрель 2026) --- ## Content Overview **Объём:** 74 документа (по с | `docs/02-anthropic-vacancies/38-content-overview.md` |
| `декабрь 2025` | summary --> > **Создан:** [? уточнить — декабрь 2025, если совпадает с волной --- <!-- tags: anthropic --> | `docs/02-anthropic-vacancies/43-history.md` |
| ... | _ещё 120 записей_ | |


### 121. Точная дата (152)
_Файл: `docs/TIMELINE.md` | 3 колонок, 5 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/01-svyazi/01-executive-summary.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/04-ai-collaborations/01-executive-summary.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор **B:** `docs/0 | `docs/CONTRADICTIONS.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/NARRATIVE.md` |
| `первые месяцы 2026` | `2026 год` / стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/TABLES.md` |


### 122. Точная дата (152)
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
| `Phase 0` | ogy proceeds in five phases. ### 9.1. Phase 0 — Foundation (Months 1-12) **Activities**: - Establish gov | `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` |
| `Phase 1` | safety incidents - Funding secured for Phase 1 ### 9.2. Phase 1 — Single Domain Maturation (Year 2) **Ac | `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` |
| `Phase 2` | gulatory dialogue established ### 9.3. Phase 2 — Domain Expansion (Years 3-4) **Activities**: - Add domai | `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` |
| ... | _ещё 261 записей_ | |


### 123. Точная дата (152)
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
| ... | _ещё 168 записей_ | |


### 124. Точная дата (152)
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
| `v1.0` | бочий черновик Nautilus Portal Protocol v1.0. Он может --- <!-- tags: collaboration --> ## 0. Statu | `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` |
| `v1.0.0` | может изменяться до объявления stable v1.0.0. Breaking changes после stable потребуют bump до v2.0 с mi | `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` |
| `v2.0` | changes после stable потребуют bump до v2.0 с migration guide. Комментарии и предложения — через Issue | `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` |
| `v1.0` | ations в федерируемые репо (read-only в v1.0) ### 1.4. Terminology Ключевые термины определены в разде | `docs/02-anthropic-vacancies/06-1-introduction.md` |
| `v1.0` | col_version` — строка в формате semver. v1.0 совместимо с минорными обновлениями. - `ecosystem_name` | `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` |
| `v1.1.0` | --> ## Appendix B: Change Log ### v1.1.0-draft (2026-04-19) - **New**: Q6 as normative concept (sec | `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` |
| `v1.0.0` | out RECOMMENDED 5 seconds (was 10) ### v1.0.0-draft (2026-04 earlier) - Initial draft published --- <! | `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` |
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
| `v1.0` | x A --- *End of REVIEW_METHODOLOGY.md v1.0* *Feedback, issues, proposals: [github.com/svend4/nautilu | `docs/02-anthropic-vacancies/122-глоссарий.md` |
| `v1.1` | чие от двух предыдущих (PORTAL-PROTOCOL v1.1 и trio of passports), имеет другой характер . Это не techni | `docs/02-anthropic-vacancies/122-глоссарий.md` |
| `v1.1` | 00) Protocol: Nautilus Portal Protocol v1.1 Dependencies: mcp>=1.0.0 (only external dep) Python: 3.10+ | `docs/02-anthropic-vacancies/123-portal-mcp-py.md` |
| ... | _ещё 494 записей_ | |


### 125. Сводка
_Файл: `docs/VALIDATION.md` | 3 колонок, 6 строк_

| Проверка | Статус | Проблем |
|----------|--------|---------|
| Разделы и README | ✅ | 0 |
| Мета-файлы | ✅ | 0 |
| Пустые/короткие файлы | ⚠️ | 5 |
| Именование файлов | ✅ | 10 |
| Заголовки H1 | ⚠️ | 11 |
| Внутренние ссылки | ✅ | 15 |


### 126. Корпусная статистика
_Файл: `docs/VOCABULARY.md` | 2 колонок, 5 строк_

| Метрика | Значение |
|---------|----------|
| Средний TTR | 0.525 |
| Средний STTR (100-токенное окно) | 0.675 |
| Lexical density | 0.836 |
| Средняя длина слова | 6.61 |
| Общая оценка | 🟡 Средний |


### 127. Топ файлов по богатству словаря (STTR)
_Файл: `docs/VOCABULARY.md` | 6 колонок, 30 строк_

| Файл | STTR | TTR | Hapax% | Lex.Density | Токенов |
|------|------|-----|--------|-------------|---------|
| `ABBREVIATIONS.md` | 0.951 | 0.732 | 76% | 0.872 | 794 |
| `HEALTH.md` | 0.908 | 0.908 | 90% | 0.954 | 65 |
| `DECISIONS.md` | 0.900 | 0.686 | 74% | 0.851 | 175 |
| `METRICS.md` | 0.900 | 0.720 | 85% | 0.923 | 143 |
| `06-1-introduction.md` | 0.895 | 0.732 | 84% | 0.899 | 276 |
| `76-1-introduction.md` | 0.883 | 0.702 | 78% | 0.887 | 362 |
| `ENTITIES.md` | 0.880 | 0.552 | 76% | 0.918 | 183 |
| `194-4-десять-областей-применения.md` | 0.874 | 0.560 | 70% | 0.916 | 1434 |
| `230-аннотация.md` | 0.870 | 0.661 | 84% | 0.856 | 257 |
| `234-3-эмпирический-кейс-обучай.md` | 0.870 | 0.658 | 77% | 0.873 | 655 |
| `48-content-overview.md` | 0.870 | 0.619 | 79% | 0.891 | 147 |
| `vitalyoborin.md` | 0.865 | 0.865 | 87% | 0.942 | 52 |
| `83-8-q6-space-normative.md` | 0.855 | 0.681 | 78% | 0.884 | 251 |
| `00-intro.md` | 0.855 | 0.373 | 60% | 0.870 | 10467 |
| `14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 0.853 | 0.480 | 67% | 0.886 | 3053 |
| `199-9-стратегия-поэтапного-развёртывания.md` | 0.850 | 0.737 | 79% | 0.948 | 346 |
| `01-интегральный-анализ-профиля-svend4.md` | 0.850 | 0.333 | 60% | 0.831 | 17129 |
| `238-7-области-применения.md` | 0.847 | 0.610 | 70% | 0.947 | 618 |
| `kksudo.md` | 0.846 | 0.846 | 84% | 0.962 | 52 |
| `241-10-открытые-вопросы.md` | 0.845 | 0.725 | 79% | 0.873 | 291 |
| `58-content-overview.md` | 0.842 | 0.842 | 84% | 0.878 | 82 |
| `302-ссылки.md` | 0.840 | 0.647 | 77% | 0.882 | 170 |
| `STATS.md` | 0.840 | 0.767 | 81% | 0.915 | 129 |
| `memnet.md` | 0.837 | 0.402 | 62% | 0.865 | 6608 |
| `spbmolot.md` | 0.836 | 0.836 | 85% | 0.964 | 55 |
| `335-9-риски-и-открытые-вопросы.md` | 0.833 | 0.692 | 81% | 0.893 | 441 |
| `115-8-ограничения-и-открытые-вопросы.md` | 0.830 | 0.650 | 73% | 0.857 | 286 |
| `189-аннотация.md` | 0.830 | 0.783 | 81% | 0.832 | 226 |
| `192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | 0.830 | 0.622 | 76% | 0.886 | 775 |
| `64-for-the-curious-philosophy.md` | 0.828 | 0.654 | 75% | 0.855 | 517 |


### 128. Файлы с бедным словарём (требуют доработки)
_Файл: `docs/VOCABULARY.md` | 4 колонок, 30 строк_

| Файл | STTR | Оценка | Токенов |
|------|------|--------|---------|
| `BROKEN_LINKS.md` | 0.254 | 🔴 Очень бедный | 741 |
| `28-appendix-a-minimal-working-example.md` | 0.270 | 🔴 Очень бедный | 104 |
| `README.md` | 0.273 | 🔴 Очень бедный | 77 |
| `CROSSREFS.md` | 0.331 | 🔴 Очень бедный | 843 |
| `READING_ORDER.md` | 0.350 | 🔴 Очень бедный | 4719 |
| `134-the-double-triangle-architecture-md.md` | 0.351 | 🔴 Очень бедный | 57 |
| `273-infrastructure-for-ai-collaborative-intellectual-w.md` | 0.354 | 🔴 Очень бедный | 65 |
| `55-passports-meta-md.md` | 0.360 | 🔴 Очень бедный | 105 |
| `35-passports-info1-md.md` | 0.360 | 🔴 Очень бедный | 105 |
| `304-ingit-as-cowork-native-workspace-substrate-md.md` | 0.369 | 🔴 Очень бедный | 65 |
| `CLUSTERS.md` | 0.372 | 🔴 Очень бедный | 2418 |
| `PARAGRAPH_QUALITY.md` | 0.374 | 🔴 Очень бедный | 4707 |
| `166-representative-agent-layer-md.md` | 0.377 | 🔴 Очень бедный | 61 |
| `NETWORK.md` | 0.380 | 🔴 Очень бедный | 165 |
| `GRAPH.md` | 0.380 | 🔴 Очень бедный | 118 |
| `61-compatibility-level.md` | 0.380 | 🔴 Очень бедный | 101 |
| `51-compatibility-level.md` | 0.380 | 🔴 Очень бедный | 102 |
| `03-portal-protocol-md.md` | 0.380 | 🔴 Очень бедный | 142 |
| `249-composite-skills-agent-md.md` | 0.386 | 🔴 Очень бедный | 57 |
| `187-слой-представительских-агентов-md.md` | 0.387 | 🔴 Очень бедный | 62 |
| `LINKS.md` | 0.390 | 🔴 Очень бедный | 59 |
| `151-open-knowledge-work-foundation-md.md` | 0.390 | 🔴 Очень бедный | 59 |
| `62-author-contact.md` | 0.390 | 🔴 Очень бедный | 102 |
| `42-author-contact.md` | 0.390 | 🔴 Очень бедный | 108 |
| `41-compatibility-level.md` | 0.390 | 🔴 Очень бедный | 102 |
| `105-review-methodology-md.md` | 0.390 | 🔴 Очень бедный | 111 |
| `CODE_BLOCKS.md` | 0.391 | 🔴 Очень бедный | 967 |
| `57-native-format.md` | 0.396 | 🔴 Очень бедный | 91 |
| `208-professional-colleague-agents-md.md` | 0.397 | 🔴 Очень бедный | 58 |
| `VALIDATION.md` | 0.398 | 🔴 Очень бедный | 503 |


### 129. Топ-20 слов
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


### 130. Глобальный топ-50 слов
_Файл: `docs/WORD_FREQ.md` | 4 колонок, 50 строк_

| # | Слово | Частота | Визуализация |
|---|-------|---------|-------------|
| 1 | **anthropic** | 5,527 | `████████████████████` |
| 2 | **vacancies** | 5,016 | `██████████████████░░` |
| 3 | **проблем** | 1,458 | `█████░░░░░░░░░░░░░░░` |
| 4 | **agent** | 1,434 | `█████░░░░░░░░░░░░░░░` |
| 5 | **turn** | 1,381 | `████░░░░░░░░░░░░░░░░` |
| 6 | **svyazi** | 1,153 | `████░░░░░░░░░░░░░░░░` |
| 7 | **view** | 980 | `███░░░░░░░░░░░░░░░░░` |
| 8 | **сходство** | 976 | `███░░░░░░░░░░░░░░░░░` |
| 9 | **nautilus** | 943 | `███░░░░░░░░░░░░░░░░░` |
| 10 | **cowork** | 927 | `███░░░░░░░░░░░░░░░░░` |
| 11 | **appendix** | 887 | `███░░░░░░░░░░░░░░░░░` |
| 12 | **mcp** | 849 | `███░░░░░░░░░░░░░░░░░` |
| 13 | **ingit** | 793 | `██░░░░░░░░░░░░░░░░░░` |
| 14 | **knowledge** | 758 | `██░░░░░░░░░░░░░░░░░░` |
| 15 | **agents** | 707 | `██░░░░░░░░░░░░░░░░░░` |
| 16 | **portal** | 657 | `██░░░░░░░░░░░░░░░░░░` |
| 17 | **protocol** | 638 | `██░░░░░░░░░░░░░░░░░░` |
| 18 | **document** | 604 | `██░░░░░░░░░░░░░░░░░░` |
| 19 | **search** | 601 | `██░░░░░░░░░░░░░░░░░░` |
| 20 | **claude** | 579 | `██░░░░░░░░░░░░░░░░░░` |
| 21 | **lorenzo** | 570 | `██░░░░░░░░░░░░░░░░░░` |
| 22 | **work** | 562 | `██░░░░░░░░░░░░░░░░░░` |
| 23 | **memory** | 559 | `██░░░░░░░░░░░░░░░░░░` |
| 24 | **svend** | 544 | `█░░░░░░░░░░░░░░░░░░░` |
| 25 | **layer** | 533 | `█░░░░░░░░░░░░░░░░░░░` |
| 26 | **what** | 530 | `█░░░░░░░░░░░░░░░░░░░` |
| 27 | **infrastructure** | 510 | `█░░░░░░░░░░░░░░░░░░░` |
| 28 | **документы** | 499 | `█░░░░░░░░░░░░░░░░░░░` |
| 29 | **cite** | 495 | `█░░░░░░░░░░░░░░░░░░░` |
| 30 | **абзац** | 480 | `█░░░░░░░░░░░░░░░░░░░` |
| 31 | **sgb** | 473 | `█░░░░░░░░░░░░░░░░░░░` |
| 32 | **документ** | 454 | `█░░░░░░░░░░░░░░░░░░░` |
| 33 | **анализ** | 445 | `█░░░░░░░░░░░░░░░░░░░` |
| 34 | **агентов** | 439 | `█░░░░░░░░░░░░░░░░░░░` |
| 35 | **оборванный** | 429 | `█░░░░░░░░░░░░░░░░░░░` |
| 36 | **legal** | 424 | `█░░░░░░░░░░░░░░░░░░░` |
| 37 | **open** | 422 | `█░░░░░░░░░░░░░░░░░░░` |
| 38 | **агент** | 408 | `█░░░░░░░░░░░░░░░░░░░` |
| 39 | **rag** | 407 | `█░░░░░░░░░░░░░░░░░░░` |
| 40 | **review** | 404 | `█░░░░░░░░░░░░░░░░░░░` |
| 41 | **project** | 403 | `█░░░░░░░░░░░░░░░░░░░` |
| 42 | **architecture** | 400 | `█░░░░░░░░░░░░░░░░░░░` |
| 43 | **смотрите** | 396 | `█░░░░░░░░░░░░░░░░░░░` |
| 44 | **слой** | 381 | `█░░░░░░░░░░░░░░░░░░░` |
| 45 | **collaborations** | 380 | `█░░░░░░░░░░░░░░░░░░░` |
| 46 | **first** | 376 | `█░░░░░░░░░░░░░░░░░░░` |
| 47 | **похожие** | 371 | `█░░░░░░░░░░░░░░░░░░░` |
| 48 | **начало** | 371 | `█░░░░░░░░░░░░░░░░░░░` |
| 49 | **specific** | 368 | `█░░░░░░░░░░░░░░░░░░░` |
| 50 | **research** | 360 | `█░░░░░░░░░░░░░░░░░░░` |


### 131. 01-svyazi (8,350 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **turn** | 451 | `███████████████` |
| **view** | 310 | `██████████░░░░░` |
| **cite** | 155 | `█████░░░░░░░░░░` |
| **search** | 153 | `█████░░░░░░░░░░` |
| **svyazi** | 117 | `███░░░░░░░░░░░░` |
| **memory** | 84 | `██░░░░░░░░░░░░░` |
| **проект** | 72 | `██░░░░░░░░░░░░░` |
| **rag** | 70 | `██░░░░░░░░░░░░░` |
| **oss** | 66 | `██░░░░░░░░░░░░░` |
| **collaborations** | 53 | `█░░░░░░░░░░░░░░` |
| **mcp** | 52 | `█░░░░░░░░░░░░░░` |
| **agentfs** | 48 | `█░░░░░░░░░░░░░░` |
| **ngt** | 44 | `█░░░░░░░░░░░░░░` |
| **cardindex** | 42 | `█░░░░░░░░░░░░░░` |
| **yodoca** | 41 | `█░░░░░░░░░░░░░░` |


### 132. 01-svyazi (8,350 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **anthropic** | 2327 | `███████████████` |
| **vacancies** | 1988 | `████████████░░░` |
| **agent** | 1050 | `██████░░░░░░░░░` |
| **сходство** | 815 | `█████░░░░░░░░░░` |
| **cowork** | 753 | `████░░░░░░░░░░░` |
| **nautilus** | 717 | `████░░░░░░░░░░░` |
| **ingit** | 629 | `████░░░░░░░░░░░` |
| **agents** | 592 | `███░░░░░░░░░░░░` |
| **work** | 496 | `███░░░░░░░░░░░░` |
| **lorenzo** | 486 | `███░░░░░░░░░░░░` |
| **portal** | 478 | `███░░░░░░░░░░░░` |
| **protocol** | 435 | `██░░░░░░░░░░░░░` |
| **document** | 432 | `██░░░░░░░░░░░░░` |
| **layer** | 431 | `██░░░░░░░░░░░░░` |
| **what** | 426 | `██░░░░░░░░░░░░░` |


### 133. 01-svyazi (8,350 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **agent** | 23 | `███████████████` |
| **legal** | 22 | `██████████████░` |
| **technology** | 22 | `██████████████░` |
| **combinations** | 22 | `██████████████░` |
| **knowledge** | 22 | `██████████████░` |
| **first** | 20 | `█████████████░░` |
| **habr** | 19 | `████████████░░░` |
| **local** | 18 | `███████████░░░░` |
| **articles** | 17 | `███████████░░░░` |
| **комбинация** | 16 | `██████████░░░░░` |
| **graph** | 14 | `█████████░░░░░░` |
| **svyazi** | 14 | `█████████░░░░░░` |
| **router** | 13 | `████████░░░░░░░` |
| **rag** | 13 | `████████░░░░░░░` |
| **граф** | 12 | `███████░░░░░░░░` |


### 134. 01-svyazi (8,350 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **turn** | 513 | `███████████████` |
| **view** | 366 | `██████████░░░░░` |
| **svyazi** | 207 | `██████░░░░░░░░░` |
| **search** | 175 | `█████░░░░░░░░░░` |
| **cite** | 163 | `████░░░░░░░░░░░` |
| **memory** | 154 | `████░░░░░░░░░░░` |
| **mcp** | 137 | `████░░░░░░░░░░░` |
| **rag** | 133 | `███░░░░░░░░░░░░` |
| **проект** | 110 | `███░░░░░░░░░░░░` |
| **llm** | 96 | `██░░░░░░░░░░░░░` |
| **knowledge** | 86 | `██░░░░░░░░░░░░░` |
| **oss** | 86 | `██░░░░░░░░░░░░░` |
| **слой** | 81 | `██░░░░░░░░░░░░░` |
| **habr** | 74 | `██░░░░░░░░░░░░░` |
| **evidence** | 73 | `██░░░░░░░░░░░░░` |


### 135. 01-svyazi (8,350 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **пара** | 63 | `███████████████` |
| **llm** | 61 | `██████████████░` |
| **mcp** | 54 | `████████████░░░` |
| **memory** | 43 | `██████████░░░░░` |
| **habr** | 40 | `█████████░░░░░░` |
| **yodoca** | 34 | `████████░░░░░░░` |
| **legal** | 33 | `███████░░░░░░░░` |
| **каждый** | 30 | `███████░░░░░░░░` |
| **svyazi** | 28 | `██████░░░░░░░░░` |
| **projects** | 26 | `██████░░░░░░░░░` |
| **claude** | 26 | `██████░░░░░░░░░` |
| **self** | 25 | `█████░░░░░░░░░░` |
| **ngt** | 23 | `█████░░░░░░░░░░` |
| **obsidian** | 23 | `█████░░░░░░░░░░` |
| **skills** | 22 | `█████░░░░░░░░░░` |


### 136. 01-svyazi (8,350 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **svyazi** | 33 | `███████████████` |
| **компонент** | 20 | `█████████░░░░░░` |
| **экосистемы** | 20 | `█████████░░░░░░` |
| **тип** | 20 | `█████████░░░░░░` |
| **описание** | 13 | `█████░░░░░░░░░░` |
| **проекты** | 10 | `████░░░░░░░░░░░` |
| **статус** | 10 | `████░░░░░░░░░░░` |
| **упоминаний** | 10 | `████░░░░░░░░░░░` |
| **ссылки** | 10 | `████░░░░░░░░░░░` |
| **исходники** | 10 | `████░░░░░░░░░░░` |
| **документация** | 10 | `████░░░░░░░░░░░` |
| **readme** | 10 | `████░░░░░░░░░░░` |
| **components** | 4 | `█░░░░░░░░░░░░░░` |
| **cowork** | 3 | `█░░░░░░░░░░░░░░` |
| **ingit** | 3 | `█░░░░░░░░░░░░░░` |


### 137. 01-svyazi (8,350 слов)
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


### 138. 01-svyazi (8,350 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **svyazi** | 30 | `███████████████` |
| **проекты** | 28 | `██████████████░` |
| **профиль** | 28 | `██████████████░` |
| **первое** | 28 | `██████████████░` |
| **сообщение** | 28 | `██████████████░` |
| **вопрос** | 23 | `███████████░░░░` |
| **контакт** | 14 | `███████░░░░░░░░` |
| **параметр** | 14 | `███████░░░░░░░░` |
| **значение** | 14 | `███████░░░░░░░░` |
| **ник** | 14 | `███████░░░░░░░░` |
| **слой** | 14 | `███████░░░░░░░░` |
| **упомянут** | 14 | `███████░░░░░░░░` |
| **документах** | 14 | `███████░░░░░░░░` |
| **файлах** | 14 | `███████░░░░░░░░` |
| **платформа** | 14 | `███████░░░░░░░░` |


### 139. 01-svyazi (8,350 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **anthropic** | 3177 | `███████████████` |
| **vacancies** | 3013 | `██████████████░` |
| **проблем** | 1450 | `██████░░░░░░░░░` |
| **svyazi** | 691 | `███░░░░░░░░░░░░` |
| **абзац** | 478 | `██░░░░░░░░░░░░░` |
| **appendix** | 463 | `██░░░░░░░░░░░░░` |
| **оборванный** | 429 | `██░░░░░░░░░░░░░` |
| **turn** | 415 | `█░░░░░░░░░░░░░░` |
| **анализ** | 373 | `█░░░░░░░░░░░░░░` |
| **начало** | 362 | `█░░░░░░░░░░░░░░` |
| **svend** | 347 | `█░░░░░░░░░░░░░░` |
| **интегральный** | 294 | `█░░░░░░░░░░░░░░` |
| **agent** | 281 | `█░░░░░░░░░░░░░░` |
| **профиля** | 271 | `█░░░░░░░░░░░░░░` |
| **collaborations** | 269 | `█░░░░░░░░░░░░░░` |


### 140. 01-svyazi (8,350 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **templates** | 12 | `███████████████` |
| **project** | 10 | `████████████░░░` |
| **component** | 10 | `████████████░░░` |
| **описание** | 9 | `███████████░░░░` |
| **contact** | 6 | `███████░░░░░░░░` |
| **outreach** | 6 | `███████░░░░░░░░` |
| **ensemble** | 6 | `███████░░░░░░░░` |
| **research** | 6 | `███████░░░░░░░░` |
| **note** | 6 | `███████░░░░░░░░` |
| **смотрите** | 5 | `██████░░░░░░░░░` |
| **decision** | 4 | `█████░░░░░░░░░░` |
| **record** | 4 | `█████░░░░░░░░░░` |
| **имя** | 4 | `█████░░░░░░░░░░` |
| **ссылка** | 4 | `█████░░░░░░░░░░` |
| **статус** | 4 | `█████░░░░░░░░░░` |


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


<!-- see-also -->

---

**Смотрите также:**
- [TIMELINE](docs/TIMELINE.md)
- [CONCEPTS](docs/CONCEPTS.md)
- [ACTION_ITEMS](docs/ACTION_ITEMS.md)
- [01-интегральный-анализ-профиля-svend4](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)

