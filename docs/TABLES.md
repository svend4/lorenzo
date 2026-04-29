# Все таблицы репозитория

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

**Всего таблиц:** 420


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


## ai-collaborations (13 таблиц)


### 1. Roadmap на 6–12 месяцев
_Файл: `docs/ai-collaborations/continuation/05-roadmap-6-12-months.md` | 4 колонок, 6 строк_

| Фаза | Срок | Главная цель | Definition of Done | Метрика успеха
| 0. Contract Freeze | 2–3 недели | Зафиксировать Card Envelope, Evidence Envelope, Memory Write Policy, Trace Envelope | Есть JSON/YAML‑схемы, тестовые карточки person/project/episode/evidence, все pipeline‑шаги пишут в один формат | 100% карточек имеют card_id, state, sources, payload_hash
| 1. Evidence‑first MVP | 1 месяц | Любой match объясняется источниками | UI показывает match + evidence pack + page/span/source links | ≥80% recommendations имеют проверяемый evidence
| 2. Memory Governance | 1–2 месяца | Ассоциации не смешиваются с фактами | Есть episode/proposal/fact/decayed/conflict states и review queue | False positive по approved facts <10% на тестовом наборе
| 3. AgentOps Layer | 2–3 месяца | Все agent runs трассируются | Langfuse/Trace‑подобный слой пишет model/tool/cost/latency/anomaly | 100% внешних выводов имеют trace_id
| 4. Multi‑agent Moderation | 3–4 месяца | Extractor/reviewer/publisher работают как роли | mclaude/AI Factory/A2A‑style handoff; risky actions через HITL | Среднее время review падает на 30–50%
| 5. Local‑first/Federation | 4–6 месяцев | Узлы сообщества синхронизируют только разрешённые слои | Локальный vault + selective sync + shared metadata graph | Нет PII в shared layer по audit checks
| 6. Self‑Improvement Loop | 6–12 месяцев | Ошибки превращаются в benchmark/prompt/skill patches | Есть regression set, nightly eval, rollback policy | Улучшение precision/recall без роста false positives


### 2. Дерево метрик Svyazi 2.0
_Файл: `docs/ai-collaborations/continuation/06-metrics-tree.md` | 2 колонок, 10 строк_

| Уровень | Метрика | Что измеряет
| Extraction | schema_valid_rate | Доля LLM‑ответов, прошедших JSON/schema validation
| Normalization | canonicalization_rate | Доля skills/company/roles, сведённых к канону
| Evidence | evidence_coverage | Доля выводов с source/page/span/bbox
| Matching | match_precision@k | Сколько top‑k рекомендаций человек признал полезными
| Matching | serendipity_score | Сколько рекомендаций были неочевидны, но полезны
| Memory | proposal_to_fact_rate | Сколько гипотез после review стали фактами
| Memory | false_association_rate | Сколько ассоциаций отклонено как шум
| Safety | unsafe_tool_block_rate | Сколько risky actions остановлено policy/HITL
| Cost | cost_per_card | Цена обработки одной карточки
| AgentOps | trace_completeness | Доля операций с полным trace envelope
| UX | time_to_explain_match | За сколько секунд пользователь понимает “почему эта связь”


### 3. Прямые аналоги Svyazi
_Файл: `docs/ai-collaborations/source-projects.md` | 3 колонок, 5 строк_

| Проект | Автор | URL |
|---|---|---|
| K2-18 | Аскольд Романов (Яндекс Образование) | https://habr.com/ru/companies/yandex/articles/1019928/ |
| Wikontic | Алла Чепурова (AIRI) | https://habr.com/ru/companies/airi/articles/1000720/ + https://habr.com/ru/companies/airi/articles/855128/ |
| NGT Memory | spbmolot | https://habr.com/ru/articles/1014366/ |
| Программа поиска единомышленников ВКонтакте | — | https://habr.com/ru/articles/495554/ |
| Анатомия ИИ-агента для подбора персонала | teamly | https://habr.com/ru/companies/teamly/articles/1024062/ |


### 4. Память для агентов
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 5 строк_

| Проект | URL |
|---|---|
| Yodoca | https://habr.com/ru/articles/1006622/ |
| MemNet («Memory Is All You Need») | https://habr.com/ru/articles/983684/ |
| OpenClaw + 5 систем памяти | https://habr.com/ru/articles/1020860/ |
| Слепое пятно LLM-разработки | https://habr.com/ru/articles/1010478/ |
| Голосовой ввод Whisper + Ollama | https://habr.com/ru/articles/1009538/ |


### 5. Hardware-near (нейроморфы, термодинамика, in-memory)
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 7 строк_

| Тема | URL |
|---|---|
| Нейроморфные процессоры (Loihi, TrueNorth, BrainScaleS, Алтай) | https://habr.com/ru/companies/yadro/articles/648119/ |
| Mamba (SSM) | https://habr.com/ru/articles/786278/ + https://habr.com/ru/companies/sberdevices/articles/855080/ |
| Extropic / thrml | https://habr.com/ru/companies/ruvds/articles/980152/ + https://habr.com/ru/articles/800033/ |
| Normal Computing | https://habr.com/ru/news/789164/ |
| ZINC inference engine для Qwen3.5-35B-A3B | https://habr.com/ru/articles/1020702/ |
| RISC-V XuanTie C950 + Alibaba Vector & Matrix Acceleration | https://habr.com/ru/companies/selectel/articles/1023796/ |
| In-memory computing на мемристорах (RRAM/CBRAM) | https://habr.com/ru/companies/yadro/articles/645843/ + https://habr.com/ru/companies/neuronet/articles/592625/ |


### 6. Workflow / агентные оркестраторы
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 6 строк_

| Проект | URL |
|---|---|
| Subagents в Cursor / Claude Code | https://habr.com/ru/articles/1006602/ + https://habr.com/ru/articles/971620/ |
| MCP/Skills | https://habr.com/ru/articles/938626/ + https://habr.com/ru/articles/987094/ |
| Claude Code в headless mode | https://habr.com/ru/companies/surfstudio/articles/943108/ |
| Self-aware MCP-сервер | https://habr.com/ru/articles/1007122/ (github.com/vuguzum/self-aware-mcp-server) |
| Auto AI Router на Go | https://habr.com/ru/articles/1027878/ |
| Иерархия моделей (LibreChat → LiteLLM → Ollama) | https://habr.com/ru/articles/1024884/comments/ |


### 7. Document parsing / RAG
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 5 строк_

| Проект | URL |
|---|---|
| Победитель RAG Challenge | https://habr.com/ru/articles/893356/ |
| Гуманитарий за 2 месяца (RAG локально) | https://habr.com/ru/articles/996144/ |
| Hybrid RAG за 15 минут (pdfplumber) | https://habr.com/ru/articles/1005776/ |
| Local RAG за вечер | https://habr.com/ru/articles/955798/ |
| Graph-RAG / 9 подходов RAG | https://habr.com/ru/articles/1002138/ |


### 8. Adversarial / multi-IDE / code review
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 4 строк_

| Проект | URL |
|---|---|
| adversarial-review (Дмитрий Дементьев) | https://habr.com/ru/articles/1019588/ (github.com/dementev-dev/adversarial-review) |
| Сравнение 12 агентских IDE | https://habr.com/ru/articles/975414/ |
| Continue + Ollama офлайн | https://habr.com/ru/articles/1027658/ |
| Серена MCP + Xcode MCP + Figma MCP + Vision-сравнение iOS | https://habr.com/ru/articles/1027382/ |


### 9. Voice / транскрипция
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 2 строк_

| Проект | URL |
|---|---|
| Голосовой ввод 2026 (Handy/OpenWhispr/GigaAM) | https://habr.com/ru/articles/1024634/ |
| Локальный транскрибатор с диаризацией ЮMoney | https://habr.com/ru/companies/yoomoney/articles/1012870/ |


### 10. Browser agents / scraping
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 2 строк_

| Проект | URL |
|---|---|
| Claude in Chrome / Cowork | https://habr.com/ru/articles/1009958/ |
| Firecrawl | https://habr.com/ru/articles/1020598/ |


### 11. Tmux village / multi-agent teams
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 3 строк_

| Проект | URL |
|---|---|
| Деревня из 12 агентов через tmux | https://habr.com/ru/articles/1016096/ |
| Автономная AI-новостная система | https://habr.com/ru/articles/1023446/ |
| 9 агентов, 6 моделей, 1 сервер | https://habr.com/ru/articles/1009608/ |


### 12. Self-improvement / nightly research
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 2 строк_

| Проект | URL |
|---|---|
| AutoResearch Карпаты | https://habr.com/ru/articles/1010198/ |
| Виктория Дочкина — Sequential | https://habr.com/ru/articles/1017200/ |


### 13. Прочее (data sources, tools, philosophy)
_Файл: `docs/ai-collaborations/source-projects.md` | 2 колонок, 5 строк_

| Проект | URL |
|---|---|
| tg-chat-analyser | https://habr.com/ru/articles/943498/ (github.com/artur-gavronchuk/tg-chat-analyser) |
| AI-бот для самопознания (PDA) | https://habr.com/ru/articles/1027210/ |
| skills.sh — каталог скиллов | https://vc.ru/id744101/2789872 |
| Docling от IBM Research | https://olegtalks.ru/base/tpost/xn7kev4fa1-docling-gotovim-dannie-dlya-rag-i-llm |
| Исходная статья Чуяна про Svyazi | https://habr.com/ru/articles/1027724/ |


## anthropic-vacancies (2 таблиц)


### 1. Распределение по кластерам
_Файл: `docs/anthropic-vacancies/overview.md` | 3 колонок, 16 строк_

| Кластер | Ролей | Файл |
|---|---|---|
| AI Research & Engineering | 68 | [`clusters/01-ai-research-engineering.md`](clusters/01-ai-research-engineering.md) |
| Sales | 150 (≈34%) | [`clusters/02-sales.md`](clusters/02-sales.md) |
| Finance | 36 | [`clusters/03-finance.md`](clusters/03-finance.md) |
| Security | 24 | [`clusters/04-security.md`](clusters/04-security.md) |
| Marketing & Brand | 23 | [`clusters/05-marketing-brand.md`](clusters/05-marketing-brand.md) |
| Engineering & Design - Product | 22 | [`clusters/06-engineering-design-product.md`](clusters/06-engineering-design-product.md) |
| Software Engineering - Infrastructure | 22 | [`clusters/07-software-engineering-infrastructure.md`](clusters/07-software-engineering-infrastructure.md) |
| Safeguards (Trust & Safety) | 21 | [`clusters/08-safeguards-trust-safety.md`](clusters/08-safeguards-trust-safety.md) |
| Product Management, Support, & Operations | 17 | [`clusters/09-product-management-support-ops.md`](clusters/09-product-management-support-ops.md) |
| Compute | 13 | [`clusters/10-compute.md`](clusters/10-compute.md) |
| Legal | 13 | [`clusters/11-legal.md`](clusters/11-legal.md) |
| Technical Program Management | 10 | [`clusters/12-technical-program-management.md`](clusters/12-technical-program-management.md) |
| Communications | 5 | [`clusters/13-communications.md`](clusters/13-communications.md) |
| Public Policy | 5 | [`clusters/14-public-policy.md`](clusters/14-public-policy.md) |
| Public Benefit | 4 | [`clusters/15-public-benefit.md`](clusters/15-public-benefit.md) |
| People | 3 | [`clusters/16-people.md`](clusters/16-people.md) |


### 2. profile-mapping/ — маппинг профиля svend4 на роли Anthropic
_Файл: `docs/anthropic-vacancies/profile-mapping/README.md` | 2 колонок, 3 строк_

| Папка | Что содержит |
|---|---|
| [`01-initial-analysis/`](01-initial-analysis/) | Первая итерация: FDE Applied AI как Primary match |
| [`02-reanalysis/`](02-reanalysis/) | Коррекция после просмотра репозиториев: FDE понижен, выходят founder/research-fellowship треки |
| [`03-integral-final/`](03-integral-final/) | Финальный интегральный анализ после 70 репо: «платформа, а не должность» |


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


## glossary (2 таблиц)


### 1. Авторы — алфавитный список
_Файл: `docs/glossary/authors-by-name.md` | 3 колонок, 32 строк_

| Автор | Проекты | Где упоминается |
|---|---|---|
| **akzhankalimatov** | claude-config-kit | [Self‑Aware MCP + Skills + CodeWiki](../svyazi-2-0/components/self-aware-mcp.md) |
| **akazant** | Self‑Aware MCP | [Self‑Aware MCP + Skills + CodeWiki](../svyazi-2-0/components/self-aware-mcp.md) |
| **AnastasiyaW (Sonia_Black)** | knowledge-space, mclaude, CodeWiki | [knowledge-space](../svyazi-2-0/components/knowledge-space.md) · [mclaude](../svyazi-2-0/components/mclaude.md) · [Self‑Aware MCP + CodeWiki](../svyazi-2-0/components/self-aware-mcp.md) |
| **Antipozitive** | MemNet («Memory Is All You Need») | [MemNet карточка](../svyazi-2-0/components/memnet.md) · [Habr key‑findings — MemNet](../habr-unique-projects/key-findings/02-memnet.md) |
| **askid / atatchin** | Voice / local-first stack (Whisper, Handy, OpenWhispr, GigaAM) | [Voice / local-first stack](../svyazi-2-0/components/voice-stack.md) |
| **Артур Гавронюк** | tg-chat-analyser | [Supplementary infrastructure](../habr-unique-projects/key-findings/05-supplementary-infrastructure.md) |
| **BerriAI** | LiteLLM | [Security + routing plane](../svyazi-2-0/components/security-routing-plane.md) |
| **Andrey Карпатый** | AutoResearch | [AutoResearch + Sequential](../svyazi-2-0/components/autoresearch-sequential.md) · [AutoResearch для legal](../habr-unique-projects/final-ensembles/2-autoresearch-legal.md) |
| **Дмитрий Дементьев** | adversarial-review | [Adversarial × Multi-IDE (deep pair 3)](../habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md) |
| **Dmitriila** | SENTINEL | [Security + routing plane](../svyazi-2-0/components/security-routing-plane.md) |
| **Виктория Дочкина** (Сбер / МФТИ) | Sequential‑протокол распределённых агентов | [AutoResearch + Sequential](../svyazi-2-0/components/autoresearch-sequential.md) · [Habr key‑findings — Dochkina](../habr-unique-projects/key-findings/04-dochkina-sequential.md) |
| **iximy** | Hybrid RAG knowledge base | [Hybrid RAG карточка](../svyazi-2-0/components/hybrid-rag.md) |
| **Jerry Liu / LlamaIndex** | LiteParse | [research-docs + LiteParse](../svyazi-2-0/components/research-docs-liteparse.md) |
| **Kevin Jahns** | Yjs | [Yjs + Automerge](../svyazi-2-0/components/yjs-automerge.md) |
| **kksudo** | AgentFS | [AgentFS карточка](../svyazi-2-0/components/agentfs.md) · [Outreach](../svyazi-2-0/outreach/first-contacts.md) |
| **lee-to / Cutcode** | AI Factory + AIF Handoff | [AI Factory карточка](../svyazi-2-0/components/ai-factory.md) |
| **lib4u / zodigancode** | Rufler | [Rufler карточка](../svyazi-2-0/components/rufler.md) |
| **Maslennikovig** | RLM-Toolkit | [Security + routing plane](../svyazi-2-0/components/security-routing-plane.md) |
| **MiXaiLL76** | Auto AI Router | [Security + routing plane](../svyazi-2-0/components/security-routing-plane.md) |
| **moshael** | Memory OS | [agent-memory-mcp + Memory OS](../svyazi-2-0/components/agent-memory-mcp.md) |
| **nlaik** | research-docs (samples for LiteParse) | [research-docs + LiteParse](../svyazi-2-0/components/research-docs-liteparse.md) |
| **Аскольд Романов** (Яндекс Образование) | K2-18 | [Three direct analogues](../habr-unique-projects/analogues/01-three-direct-analogues.md) · [Three key candidates](../ai-collaborations/candidates/01-three-key-candidates.md) |
| **Никита Списак** | second-brain skill-pack | [Skill catalogs × Subagents](../habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md) |
| **spbmolot** | NGT Memory | [NGT Memory карточка](../svyazi-2-0/components/ngt-memory.md) · [Outreach](../svyazi-2-0/outreach/first-contacts.md) |
| **tagir_analyzes** | Legal RAG | [Legal RAG карточка](../svyazi-2-0/components/legal-rag.md) |
| **VitalyOborin** | Yodoca | [Yodoca карточка](../svyazi-2-0/components/yodoca.md) · [Habr key‑findings — Yodoca](../habr-unique-projects/key-findings/01-yodoca.md) · [Outreach](../svyazi-2-0/outreach/first-contacts.md) |
| **VitaliySemenov** | agent-memory-mcp | [agent-memory-mcp + Memory OS](../svyazi-2-0/components/agent-memory-mcp.md) |
| **VladSpace / vpakspace** | Graph RAG | [Graph RAG карточка](../svyazi-2-0/components/graph-rag.md) |
| **vuguzum** | self-aware MCP | [Self-aware MCP × Specs](../habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md) |
| **Алла Чепурова** (AIRI) | Wikontic | [Three direct analogues](../habr-unique-projects/analogues/01-three-direct-analogues.md) · [Three key candidates](../ai-collaborations/candidates/01-three-key-candidates.md) |
| **Андрей Чуян** | Svyazi | [Svyazi карточка](../svyazi-2-0/components/svyazi.md) · [Outreach](../svyazi-2-0/outreach/first-contacts.md) |
| **Сэм Галлахер** | Knowledge Graph Kit (Medium) | [Related projects](../habr-unique-projects/analogues/02-related-projects.md) |


### 2. Ключевые понятия и паттерны
_Файл: `docs/glossary/concepts.md` | 3 колонок, 26 строк_

| Понятие | Краткое определение | Где раскрыто |
|---|---|---|
| **CardIndex** | Source of truth: неизменяемая карточка как единица знания | [Card Envelope](../svyazi-2-0/architecture/card-envelope.md) · [Svyazi](../svyazi-2-0/components/svyazi.md) |
| **Card Envelope** | Стандарт схемы карточки: `card_id`, `card_type`, `state`, `sources`, `edges`, `updated_at`, `payload_hash` | [Card Envelope](../svyazi-2-0/architecture/card-envelope.md) · [Integration spec](../svyazi-2-0/architecture/integration-spec.md) |
| **Evidence Envelope** | Стандарт привязки вывода к источнику: `source_id`, `page_or_span`, `bbox_or_offset`, `method`, `confidence`, `supporting_nodes` | [Evidence Envelope](../svyazi-2-0/architecture/evidence-envelope.md) |
| **Memory Write Policy** | Различение `episode` / `fact` / `proposal` / `decay_event` при записи в память | [Memory Write Policy](../svyazi-2-0/architecture/memory-write-policy.md) |
| **Skill and Tool Policy** | Класс tool: `read` / `annotate` / `plan` / `mutate` / `publish` / `external_send` | [Skill and Tool Policy](../svyazi-2-0/architecture/skill-tool-policy.md) |
| **Review Record** | Артефакт человеческого решения: `reviewer_role`, `decision`, `reason`, `evidence_refs`, `follow_up` | [Review Record](../svyazi-2-0/architecture/review-record.md) |
| **Trace Envelope** | Расширение для AgentOps: trace_id, model_route, tools_used, token_cost, anomaly_flags | [AgentOps + Trace Envelope](../ai-collaborations/continuation/02-agentops-trace-envelope.md) |
| **Hot path / Slow path** | Yodoca‑паттерн: эпизоды в SQLite за <50 мс vs асинхронные эмбеддинги ночью | [Yodoca карточка](../svyazi-2-0/components/yodoca.md) · [Habr key‑findings — Yodoca](../habr-unique-projects/key-findings/01-yodoca.md) |
| **Ebbinghaus decay** | Контролируемое забывание редко используемых фактов | [Yodoca](../svyazi-2-0/components/yodoca.md) · [Memory Write Policy](../svyazi-2-0/architecture/memory-write-policy.md) |
| **Hebbian / STDP plasticity** | Усиление связи между концептами при ко‑активации | [NGT Memory](../svyazi-2-0/components/ngt-memory.md) · [MemNet](../svyazi-2-0/components/memnet.md) · [Hardware pair 1](../habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md) |
| **Spreading activation / dream phase** | Самопроизвольная активация памяти без внешнего входа для поиска скрытых связей | [MemNet](../svyazi-2-0/components/memnet.md) · [Habr key‑findings — MemNet](../habr-unique-projects/key-findings/02-memnet.md) |
| **Discovery file** | Накопление неизвестного — то, что система не смогла классифицировать | [Svyazi](../svyazi-2-0/components/svyazi.md) · [Sensor-driven life log](../habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md) |
| **«LLM как периферия»** | Архитектура, где LLM — не ядро, а узел; код отвечает за стабильность | [PDA — LLM как периферия](../habr-unique-projects/key-findings/03-pda-llm-as-periphery.md) |
| **Sequential vs Coordinator** | Распределённая цепочка агентов, видящих результаты предшественников, выигрывает у центрального координатора на 44% | [AutoResearch + Sequential](../svyazi-2-0/components/autoresearch-sequential.md) · [Habr key‑findings — Dochkina](../habr-unique-projects/key-findings/04-dochkina-sequential.md) |
| **Adversarial review** | Один агент пишет, другие критикуют; multi‑model | [Комбинация 8](../technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md) · [Adversarial × Multi-IDE](../habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md) |
| **Local‑first / privacy‑by‑design** | Данные принадлежат устройству пользователя, в облако только избранное | [Privacy](../svyazi-2-0/security/privacy.md) · [Hardware pair 4](../habr-unique-projects/hardware-pairs/4-riscv-privacy.md) · [Federated Local Graph](../svyazi-2-0/ensembles/G-federated-local-graph.md) |
| **Privacy by design** | Контакты — в отдельный raw‑слой; в карточки уходит только очищенный профиль | [Default policy](../svyazi-2-0/security/default-policy.md) |
| **Page-level grounding** | Единица доказательства — страница, не чанк | [Legal RAG](../svyazi-2-0/components/legal-rag.md) · [Forensic RAG (ai‑collab)](../ai-collaborations/ensembles/3-forensic-rag.md) |
| **Lazy MCP loading (Tool Search)** | Не грузить все MCP‑инструменты в контекст; падение overhead с 82k до 5.7k токенов | [Security + routing plane](../svyazi-2-0/components/security-routing-plane.md) |
| **Two parents → many children** | Метафора: hardware/software пара рождает несколько по‑разному ориентированных потомков | [Hardware metaphor](../habr-unique-projects/hardware-pairs/7-metaphor.md) · [Software metaphor](../habr-unique-projects/software-pairs/6-metaphor.md) |
| **Скромные родители → мощные дети** | Та же мысль с другой стороны: ни один проект сам по себе не революционен | [Synthesis 1‑8](../technology-combinations/synthesis-tables/01-08-summary.md) |
| **One‑man AI company** | Один человек ведёт 30–50 дел Sozialrecht параллельно с качеством офиса из 5 юристов | [One person = one company](../habr-unique-projects/final-ensembles/1-one-person-one-company.md) |
| **Q6‑гиперкуб / MoME** | 64 гексаграммы как вершины Q6, MoME‑роутинг по геометрии | [Hardware pair 2 — TSU × MoME](../habr-unique-projects/hardware-pairs/2-tsu-mome.md) · [Hardware pair 3](../habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md) · [Profile five layers](../anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md) |
| **LCI (Lyapunov Coherence Index)** | Метрика энергетической когерентности системы | [Hardware pair 2](../habr-unique-projects/hardware-pairs/2-tsu-mome.md) · [Svyazi 2.0 block map](../habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md) |
| **Forward Deployed Engineer (FDE)** | Инженер, приходящий к клиенту с проблемой, строящий прототип на Claude в production | [FDE primary match](../anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md) · [FDE downgraded](../anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md) |
| **Beneficial Deployments** | Anthropic‑программа: применение Claude к общественно‑полезным задачам | [Secondary match](../anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md) · [Sales](../anthropic-vacancies/clusters/02-sales.md) |


## habr-unique-projects (1 таблиц)


### 1. Подпапки
_Файл: `docs/habr-unique-projects/README.md` | 2 колонок, 9 строк_

| Подпапка | О чём |
|---|---|
| [`analogues/`](analogues/) | Прямые аналоги Svyazi (K2-18, Wikontic, NGT Memory) и смежные проекты |
| [`key-findings/`](key-findings/) | Ключевые находки: Yodoca, MemNet, PDA-бот, Дочкина, инфраструктурные кусочки, синтез блок-карты |
| [`hardware-pairs/`](hardware-pairs/) | Пять hardware-near родительских пар + бонус (RRAM) и метафора |
| [`software-pairs/`](software-pairs/) | Пять софтверных родительских пар |
| [`deep-pairs/`](deep-pairs/) | Восемь углублённых софтверных пар (третья итерация) |
| [`final-ensembles/`](final-ensembles/) | Три финальных ансамбля + сводный список авторов |
| [`extra-examples/`](extra-examples/) | Расширенные примеры с Хабра по варианту D — 13 файлов: Svyazi (детально), ВШЭ нетворкинг, BrainBox, Claude subagents, HW-NL2Workflow, профессиональные платформы, knowledge workspace, multi-agent hub, federated platform, profession-specific workflows, конкретные next steps |
| [`search-strategy/`](search-strategy/) | Каркас стратегии поиска (заполняется по необходимости) |
| [`evaluation/`](evaluation/) | Каркас оценки уникальности и зрелости |


## lorenzo-agent (1 таблиц)


### 1. Что такое «внуковая» комбинация — operationalized Lorenzo
_Файл: `docs/lorenzo-agent/operationalized/00-overview-grandchild-combination.md` | 2 колонок, 5 строк_

| Узел pipeline | Проект | Статус
| Habr Scout | Firecrawl + Playwright + Свяжи extraction | Working components
| Svyazi-like карточки | Свяжи (Чуян) + knowledge-space (Анастасия) | Working
| Collaboration Knowledge OS | AgentFS + Memory OS + knowledge-space | Working
| Agent Team Kernel | Rufler + agent-pool + mclaude (Анастасия) | Working
| Forensic RAG | LiteParse + Hybrid RAG + Graph RAG | Working
| Secure Agent Runtime | SENTINEL + Shield + Claude permissions | Working


## nautilus (21 таблиц)


### 1. Подпапки
_Файл: `docs/nautilus/README.md` | 2 колонок, 22 строк_

| Подпапка | Что содержит |
|---|---|
| [`npp-v1-0/`](npp-v1-0/) | Nautilus Portal Protocol v1.0.0-draft RFC — более ранняя версия, 18 разделов + комментарий о дизайн-решениях |
| [`npp-v1-1/`](npp-v1-1/) | Nautilus Portal Protocol v1.1 RFC — полная формальная спецификация, 23 раздела |
| [`review-methodology/`](review-methodology/) | Трёхфазная методология Review v1.0 — параллельная разработка двух вариантов с последующей ручной консолидацией (17 разделов) |
| [`okwf-concept/`](okwf-concept/) | Open Knowledge Work Foundation — Concept Document (11 разделов): шестислойная инфраструктура, target populations, governance, phased rollout |
| [`representative-agent-layer-en/`](representative-agent-layer-en/) | Representative Agent Layer (EN) — Cinderella Syndrome, исторические прецеденты, архитектурная спецификация (13 разделов) |
| [`representative-agent-layer-ru/`](representative-agent-layer-ru/) | Слой Представительских Агентов (RU, 13 разделов) |
| [`professional-colleague-agents-en/`](professional-colleague-agents-en/) | Professional Colleague Agents — типология AI-агентов на стороне принципала (13 разделов, EN) |
| [`professional-colleague-agents-ru/`](professional-colleague-agents-ru/) | Тот же документ на русском (13 разделов) |
| [`composite-skills-agents/`](composite-skills-agents/) | Composite Skills Agents — Twenty-One Teachers Pattern, sub-agent registry, ensembles (13 разделов) |
| [`double-triangle-architecture/`](double-triangle-architecture/) | Double-Triangle Architecture for Human-AI Collaboration — звезда Давида (12 разделов) |
| [`infrastructure-layer-b-en/`](infrastructure-layer-b-en/) | Infrastructure for AI-Collaborative Intellectual Work (EN) — «missing middle Layer B» между Chat и Code (14 разделов) |
| [`infrastructure-layer-b-ru/`](infrastructure-layer-b-ru/) | Инфраструктура для AI-совместной интеллектуальной работы (RU, 13 разделов) |
| [`ingit-cowork-en/`](ingit-cowork-en/) | InGit + Cowork — Symbiotic Architecture (10 разделов, EN) |
| [`ingit-cowork-ru/`](ingit-cowork-ru/) | Тот же документ на русском (10 разделов) |
| [`npp-humanitarian-extension/`](npp-humanitarian-extension/) | Применение NPP к гуманитарным документам (юридические / социальные), grant opportunities |
| [`privacy-federation/`](privacy-federation/) | Privacy-aware federation: что анонимизировать, двухуровневая публикация |
| [`multi-tier-architecture/`](multi-tier-architecture/) | Многоуровневая архитектура: общая база + приватные подключения |
| [`innovation-transitions/`](innovation-transitions/) | Инновация как переход состояний (паровоз → тепловоз) |
| [`supply-demand/`](supply-demand/) | «Спрос рождает предложение» — три связанные темы |
| [`transmission-box/`](transmission-box/) | Если гора не идёт к человеку — посредник как коробка передач |
| [`composite-skills-agents-companion-mentors/`](composite-skills-agents-companion-mentors/) | Companion paper: метафора 21 учителя индийского йога — спектр между Professional Colleague и Representative Agent |
| [`community-discussions/`](community-discussions/) | Реакции на Habr-статьи, voiceless контрибьюторы, агент меняющий реальность |


### 2. community-discussions/ — обсуждения и реакции вокруг DHLab с
_Файл: `docs/nautilus/community-discussions/README.md` | 2 колонок, 5 строк_

| Подпапка | О чём |
|---|---|
| [`habr-article-1-reaction/`](habr-article-1-reaction/) | Реакция на первую Habr-статью в обсуждении |
| [`practical-observations/`](practical-observations/) | Когда теоретические идеи работают на практике |
| [`voiceless-contributors/`](voiceless-contributors/) | Могут ли быть voiceless контрибьюторы |
| [`agent-changes-reality/`](agent-changes-reality/) | Catalyst Agent меняет реальность не только своего человека |
| [`habr-article-2-reaction/`](habr-article-2-reaction/) | Реакция на вторую Habr-статью |


### 3. Appendix B: Domain Comparison Matrix
_Файл: `docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md` | 5 колонок, 10 строк_

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


### 4. Структурное сравнение: код vs гуманитарные документы
_Файл: `docs/nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md` | 2 колонок, 9 строк_

| Аспект | Код/Research (текущий Nautilus) | Юридические/Социальные документы
| Единица данных | Концепт/функция/теорема | Статья закона/параграф решения/кейс
| Native format | .py, .md, .info1, .pro2 | .pdf, .docx, .odt, .md, .rtf
| Язык | En/Ru, технический | De (SGB, SGG), En (EU law), Ru
| Связи | Import, reference, bridge | Статья→статья, прецедент→прецедент, учреждение→процедура
| Авторство | Автор-разработчик | Законодатель, суд, учреждение
| Консенсус | Концепт в N репо | Факт подтверждён N источниками
| Q6-координата | Семантическая вершина | Категория права/социальной сферы
| Стабильность | Меняется часто (коммиты) | Стабильна (Geltungsbereich), но с поправками
| Timestamp-критичность | Умеренная | Критическая (Fristwahrung, Inkrafttreten)
| Regulatory | Open-source lics | Urheberrecht, Amtliche Werke, GDPR


### 5. Паспорт: /
_Файл: `docs/nautilus/npp-v1-1/04-passport.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | / |
| Формат | `.` — краткое описание |
| Единица | что является одной записью |
| Адаптер | `adapters/.py` |
| Уровень совместимости | <0-3> — |


### 6. 8.3. Q6 Mapping Rules
_Файл: `docs/nautilus/npp-v1-1/08-q6-space.md` | 2 колонок, 4 строк_

| Format | Правило |
|--------|---------|
| `info1` | `alpha + 4` → 3 старших бита, остальные биты по категории |
| `pro2` | нативные Q6-координаты (Q6 — первичный концепт pro2) |
| `meta` | `hex_id - 1 → bin(6)` (гексаграмма 1 → `000000`, 64 → `111111`) |
| `data7` | `порядковый номер % 64 → bin(6)` |


### 7. 12.6. Path Selection Guidance
_Файл: `docs/nautilus/npp-v1-1/12-onboarding-paths.md` | 2 колонок, 5 строк_

| Вариант | Когда использовать |
|---------|-------------------|
| **A** | Когда хорошо знаете структуру Repo и хотите high-quality |
| **B** | Стартовая точка для большинства новых Repos |
| **C** | Для Repos, которые автор хочет сам декларировать |
| **D** | Для быстрой первой интеграции незнакомых Repos |
| **E** | Для автоматической fleet-federation многих Repos |


### 8. 13.1. Required Endpoints
_Файл: `docs/nautilus/npp-v1-1/13-rest-api.md` | 3 колонок, 3 строк_

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/query?q=<text>&ranked=<0\|1>` | Поиск концептов |
| GET | `/api/describe` | Описание всех адаптеров |
| GET | `/api/health` | Состояние экосистемы (score 0–100) |


### 9. 13.1. Required Endpoints
_Файл: `docs/nautilus/npp-v1-1/13-rest-api.md` | 3 колонок, 4 строк_

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/links` | Валидация кросс-ссылок |
| GET | `/api/neighbors?q6=<bits>&dist=<N>` | Q6-соседи |
| GET | `/metrics` | Prometheus-метрики (text/plain) |
| GET | `/` | Root endpoint со списком endpoints |


### 10. 18.1. Current Reference Implementation Metrics
_Файл: `docs/nautilus/npp-v1-1/18-reference-implementation.md` | 2 колонок, 7 строк_

| Метрика | Значение |
|---------|----------|
| Python LOC | 6 782 |
| Адаптеров | 13 (7 реестровых + 6 расширенных) |
| Тестов | 60 / 60 passing |
| mypy errors | 0 |
| Внешних зависимостей | 0 (stdlib only) |
| Health Score | 82 / 100 |
| Q6 coverage (real) | 21.9% (14 / 64 vertices) |


### 11. Паспорт: owner/my-notes
_Файл: `docs/nautilus/npp-v1-1/22-glossary.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | owner/my-notes |
| Формат | `.md` — Markdown notes |
| Единица | Markdown-документ |
| Адаптер | `adapters/my_notes.py` |
| Уровень совместимости | 1 — читаемый |


### 12. 5.2. Three-Year Pilot Budget (Estimated)
_Файл: `docs/nautilus/okwf-concept/05-economic-model.md` | 4 колонок, 9 строк_

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


### 13. Appendix A: Comparison Matrix Against Existing Solutions
_Файл: `docs/nautilus/okwf-concept/10-appendices.md` | 8 колонок, 11 строк_

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


### 14. 1.7. Why This Distinction Matters
_Файл: `docs/nautilus/professional-colleague-agents-en/01-five-type-typology.md` | 6 колонок, 7 строк_

| Property | Type 0 | Type 1 | Type 2 | Type 3 | Type 4 |
|----------|--------|--------|--------|--------|--------|
| Specialization | None | Profession | Institution+profession | Task | Individual |
| External communication | None | None | Some | Some | Extensive |
| Replicability | Universal | Per profession | Per institution | Per task | Per individual |
| Economics | Subscription | Profession-wide | Institutional | Variable | Individual |
| Ethical concerns | Low | Medium | Medium | High | Highest |
| Regulatory complexity | Low | Medium | High | Highest | Highest |
| Deployment readiness | Mature | Emerging | Early | Beginning | Conceptual |


### 15. 3.3. Deployment Trajectory
_Файл: `docs/nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md` | 2 колонок, 3 строк_

| Date | Status |
|------|--------|
| Summer 2025 | Development begins |
| September 2025 | Public launch |
| April 2026 | 93,000 active teacher users |


### 16. 1.7. Почему это различение важно
_Файл: `docs/nautilus/professional-colleague-agents-ru/01-pyat-tipov.md` | 6 колонок, 7 строк_

| Свойство | Тип 0 | Тип 1 | Тип 2 | Тип 3 | Тип 4 |
|----------|-------|-------|-------|-------|-------|
| Специализация | Нет | Профессия | Институция+профессия | Задача | Личность |
| Внешние коммуникации | Нет | Нет | Некоторые | Некоторые | Обширные |
| Тиражируемость | Универсальная | По профессии | По институции | По задаче | По индивиду |
| Экономика | Подписка | По профессии | Институциональная | Различная | Индивидуальная |
| Этические вопросы | Низкие | Средние | Средние | Высокие | Высочайшие |
| Регуляторная сложность | Низкая | Средняя | Высокая | Высочайшая | Высочайшая |
| Готовность к развёртыванию | Зрелая | Появляющаяся | Ранняя | Начинающаяся | Концептуальная |


### 17. 3.3. Траектория развёртывания
_Файл: `docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md` | 2 колонок, 3 строк_

| Дата | Статус |
|------|--------|
| Лето 2025 | Начало разработки |
| Сентябрь 2025 | Публичный запуск |
| Апрель 2026 | 93 000 активных учителей-пользователей |


### 18. Appendix B: Domain Comparison Matrix
_Файл: `docs/nautilus/representative-agent-layer-en/12-closing.md` | 5 колонок, 10 строк_

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


### 19. Приложение B: Матрица Сравнения Областей
_Файл: `docs/nautilus/representative-agent-layer-ru/12-zaklyuchenie.md` | 5 колонок, 10 строк_

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


### 20. 2.3. Артефакты каждой фазы
_Файл: `docs/nautilus/review-methodology/02-formal-workflow.md` | 4 колонок, 4 строк_

| Фаза | Артефакт | Место хранения | Финальность |
|------|----------|----------------|-------------|
| A | `<doc>_draft_A.md` | ветка `claude/review-XXX` | нет, промежуточное |
| B | `<doc>_draft_B.md` | ветка `claude/review-YYY` | нет, промежуточное |
| Merge | `<doc>.md` с header warning + параллельными блоками | main, с dupликацией | нет, transitional |
| C | `<doc>.md` консолидированная | main, dupликаты удалены | да, канонично |


### 21. 8.1. Trade-offs
_Файл: `docs/nautilus/review-methodology/09-limitations-open-questions.md` | 2 колонок, 5 строк_

| Преимущество | Оборотная сторона |
|--------------|-------------------|
| Сохранение всех insights | Transitional state выглядит messy |
| Защита от single-agent bias | Требует ручной консолидации (время) |
| Audit trail обеих версий | Увеличивает объём документа временно |
| Методологически обосновано | Read-time overhead для внешних |
| Масштабируется на team-work | Не решает проблему >2 вариантов |


## root (210 таблиц)


### 1. Словарь аббревиатур и сокращений
_Файл: `docs/ABBREVIATIONS.md` | 3 колонок, 99 строк_

| Аббревиатура | Расшифровка | Упоминаний |
|-------------|-------------|------------|
| **ABC** | англ. ... | 9 |
| **ACD** | Automated Capability Discovery — ещё один сильный кубик: модель в роли «учёного» систематически генерирует задачи для мо | 10 |
| **ADR** | "ADR-004: Temporal Metadata as First-Class Concept" | 110 |
| **AGENTS** | типология + готовая к развёртыванию категория Type 1 | 16 |
| **AI** | это инфраструктурный слой для AI-managed virtual companies | 4100 |
| **AIRI** | серьёзная research лаборатория (Артём Шелманов и команда) | 27 |
| **ANP** | Agent Network Protocol | 6 |
| **API** ⭐ | Application Programming Interface — интерфейс программирования приложений | 412 |
| **BSL** ⭐ | Business Source License — бизнес-лицензия с открытым кодом | 85 |
| **CAMEL** | это другая значимая open-source framework, и сравнение их с Hermes будет показательным | 259 |
| **CI/CD** ⭐ | Continuous Integration / Continuous Deployment | 17 |
| **CLI** ⭐ | Command Line Interface — интерфейс командной строки | 78 |
| **CQRS** | Multiple read models from single event stream | 17 |
| **CRDT** ⭐ | Conflict-free Replicated Data Type — структура данных без конфликтов слияния | 152 |
| **DAO** | результат смешанный | 5 |
| **DR** | Трёхфазная методология Review](docs/nautilus/review-methodology/00-tldr | 19 |
| **DSL** | Non-programmers write legal automation | 69 |
| **EMEA** | RU/DE/EN на рабочем уровне, базирование в Германии, понимание европейского регуляторного контекста (что прямо читается ч | 60 |
| **ERROR** | MCP SDK not installed | 3 |
| **FAQ** ⭐ | Frequently Asked Questions — часто задаваемые вопросы | 57 |
| **FDE** | это исполнительская роль на чужую продуктовую повестку | 37 |
| **FRE** | 70-100 лёгкий, 50-70 средний, 30-50 сложный, <30 очень сложный | 16 |
| **GDPR** ⭐ | General Data Protection Regulation — европейский регламент защиты данных | 110 |
| **GG** | они публичные) | 3 |
| **GUI** | -3 months effort | 24 |
| **HEAD** | 7 commits) | 9 |
| **HMP** | на когнитивной устойчивости и этике | 116 |
| **ID** | sgb:XII:90:4 (SGB XII, § 90, Abs | 20 |
| **II** | The Double-Triangle Architecture — formal описание дуальной структуры с вашей метафорой звезды Давида | 34 |
| **III** | Protocols Between Layers — три протокола с examples | 25 |
| **INPUT** | - Bescheid text (decoded by agent) | 2 |
| **IP** | AI-платформа, заказчик, сами фрилансеры? Сегодняшние legal frameworks не умеют отвечать на этот вопрос дёшево | 12 |
| **IV** | Nautilus Portal as Reference Implementation — как existing work serves как substrate | 25 |
| **IX** | 102 , sgg:86b:2 ), на прецеденты | 78 |
| **JWT** ⭐ | JSON Web Token — токен аутентификации | 6 |
| **KPI** | сколько полезных коллабораций, проектов, выступлений, mentorship‑пар или hiring‑контактов возникло из рекомендаций систе | 67 |
| **KSV** | потому что у них нет точных русских эквивалентов в контексте немецкой социально-правовой системы | 54 |
| **LAYER** | функциональная категория Type 4 | 76 |
| **LCI** | Lyapunov Coherence Index, target π | 39 |
| **LLM** ⭐ | Large Language Model — большая языковая модель | 612 |
| **LOC** | продублирована с разными строками в разных частях | 69 |
| **MAY** | по [RFC 2119](https://datatracker | 45 |
| **MCP** ⭐ | Model Context Protocol — протокол контекста для AI-инструментов | 1211 |
| **MIT** ⭐ | Massachusetts Institute of Technology License — разрешительная лицензия | 342 |
| **ML** | несколько моделей → voting/averaging | 110 |
| **MMORPG** | это общее пространство , в котором вы видите аватары коллег, можете подойти к ним, стоять рядом, работать вместе в одной | 95 |
| **MRR** | это уже leverage для любого следующего шага, включая разговор с Anthropic Institute о grant/partnership | 5 |
| **MUST** | - Возвращать пустой список, если ничего не найдено (не None, не exception) - Ограничить результат разумным числом (SHOUL | 150 |
| **MVP** ⭐ | Minimum Viable Product — минимально жизнеспособный продукт | 323 |
| **NDA** | intermediate view (placeholder'ы, но с consistent identifiers для longitudinal анализа) | 3 |
| **NGT** | граф памяти | 396 |
| **NLP** ⭐ | Natural Language Processing — обработка естественного языка | 2 |
| **NNNN** | [Название] | 27 |
| **NPP** | **федеративная модель**, где каждый | 182 |
| **OASIS** | до 1M agents simulation) | 4 |
| **ODT** | не только текст | 3 |
| **OKWF** | конкретная архитектура](#применение-к-okwf-конкретная-архитектура) | 519 |
| **OLAP** | analytics, 100M rows/sec) │ | 24 |
| **OLTP** | transactions) │ | 20 |
| **OPTIONAL** | ключевые слова | 15 |
| **OS** | неуточнено | 233 |
| **OSS** ⭐ | Open Source Software — программное обеспечение с открытым кодом | 288 |
| **OUTPUT** | - Draft Widerspruch (DOCX format) | 2 |
| **P2P** ⭐ | Peer-to-Peer — децентрализованная сеть | 47 |
| **PARC** | research center, became iconic несмотря на parent brand decline OpenAI — research org становящаяся product company, name | 5 |
| **PDA** | LLM как периферия]( | 30 |
| **PII** ⭐ | Personally Identifiable Information — персональные данные | 69 |
| **PROTOCOL** | иначе future разработчики будут gадать | 272 |
| **PURE** | LLM-based User Profile Management for Recommender System» | 9 |
| **QA** | демон-критик (adversarial, rigorous) | 323 |
| **RAG** ⭐ | Retrieval-Augmented Generation — генерация с поиском по базе знаний | 750 |
| **README** | 550+ строк production-качества: установка, конфигурация для всех 6 платформ (включая детализацию /etc/fstab для CIFS, AD | 1621 |
| **REQUIRED** | откуда пришло | 35 |
| **RFC** | более ранняя версия, 18 разделов + комментарий о дизайн-решениях | | 144 |
| **ROI** | 10 sec queries vs 2 hour manual search | 55 |
| **RU** | «был создан», «является», «используется», «осуществляется» - Пассивный залог EN: «was created», «is used», «has been» -  | 432 |
| **SDK** ⭐ | Software Development Kit — набор инструментов разработчика | 84 |
| **SENTINEL** | неуточнено; LiteLLM — MIT вне enterprise‑директорий; Auto AI Router — Apache 2 | 221 |
| **SF** | DC, Canberra) | 37 |
| **SGB** ⭐ | Sozialgesetzbuch — Социальный кодекс Германии | 554 |
| **SHOULD** | - Поддерживать case-insensitive matching для текстовых запросов | 74 |
| **SLA** | ** latency p99 < 500ms, availability 99 | 1 |
| **SLI** | p95 task completion time per agent type | 3 |
| **SLO** | "Code review agent must complete 95% tasks <5 min" | 9 |
| **SWE** | в Sales/Finance/Marketing/Legal зарплаты ниже и сильно варьируются по локации | 11 |
| **TF-IDF** ⭐ | Term Frequency–Inverse Document Frequency — метрика важности термина | 44 |
| **TODO** ⭐ | To Do — задача к выполнению | 11 |
| **TSU** | физика, MoME — математика; ZINC — software, гибридная архитектура — алгоритм; RISC-V — кремний, privacy — право; TinyML  | 24 |
| **TVCP** | Terminal Video Communication Platform, терминал видео коммуникация платформа, игры») — это необычное : Go + template + M | 2 |
| **UI** | -2 months effort | 106 |
| **URL** | я разберусь с любым вариантом именования | 131 |
| **VERIFY** | 6782 vs 6600] как метку | 2 |
| **VI** | Deployment Paths — humanities, project management, OSS, general | 5 |
| **VII** | Open Questions — governance, consent, economics, scale | 5 |
| **VIII** | Call to Action — что делать researchers, practitioners, founders | 4 |
| **VPS** | cron каждое утро обходит сайты Sozialgericht/BSG/KSV, генерирует Stellungnahme-черновики, обновляет статусы Aktenzeichen | 16 |
| **XII** | legally binding reference с нормативной силой | 76 |
| **YAML** ⭐ | YAML Ain't Markup Language — формат конфигурационных файлов | 170 |
| **ZINC** | - Ночью агент крутит эксперименты с промптами - Роутер геометрически выбирает, какой экс | 74 |


### 2. Самые часто используемые
_Файл: `docs/ABBREVIATIONS.md` | 2 колонок, 15 строк_

| Аббревиатура | Упоминаний |
|-------------|------------|
| **AI** | 4100 — _это инфраструктурный слой для AI-managed virtual companies_ |
| **README** | 1621 — _550+ строк production-качества: установка, конфигурация для _ |
| **MCP** | 1211 — _Model Context Protocol — протокол контекста для AI-инструмен_ |
| **RAG** | 750 — _Retrieval-Augmented Generation — генерация с поиском по базе_ |
| **LLM** | 612 — _Large Language Model — большая языковая модель_ |
| **SGB** | 554 — _Sozialgesetzbuch — Социальный кодекс Германии_ |
| **OKWF** | 519 — _конкретная архитектура](#применение-к-okwf-конкретная-архите_ |
| **RU** | 432 — _«был создан», «является», «используется», «осуществляется» -_ |
| **API** | 412 — _Application Programming Interface — интерфейс программирован_ |
| **NGT** | 396 — _граф памяти_ |
| **MIT** | 342 — _Massachusetts Institute of Technology License — разрешительн_ |
| **MVP** | 323 — _Minimum Viable Product — минимально жизнеспособный продукт_ |
| **QA** | 323 — _демон-критик (adversarial, rigorous)_ |
| **OSS** | 288 — _Open Source Software — программное обеспечение с открытым ко_ |
| **PROTOCOL** | 272 — _иначе future разработчики будут gадать_ |


### 3. Callout-блоки
_Файл: `docs/ALERTS.md` | 3 колонок, 4 строк_

| Тип | Количество | Назначение |
|-----|------------|------------|
| `[!NOTE]` | 0 | Нейтральная заметка |
| `[!TIP]` | 47 | Практический совет |
| `[!WARNING]` | 29 | Предупреждение о риске |
| `[!IMPORTANT]` | 3 | Ключевой документ |


### 4. Авторы и коллаборации
_Файл: `docs/AUTHORS.md` | 2 колонок, 25 строк_

| Автор | Упоминается в файлах |
|-------|---------------------|
| **AnastasiyaW** | 50 |
| **Antipozitive** | 33 |
| **BerriAI** | 12 |
| **Cutcode** | 35 |
| **Dmitriila** | 35 |
| **MiXaiLL76** | 31 |
| **Sonia_Black** | 18 |
| **VitaliySemenov** | 8 |
| **VitalyOborin** | 39 |
| **VladSpace** | 43 |
| **akazant** | 10 |
| **akzhankalimatov** | 8 |
| **andrey_chuyan** | 14 |
| **iximy** | 8 |
| **kksudo** | 57 |
| **lee-to** | 11 |
| **lib4u** | 14 |
| **moshael** | 10 |
| **nlaik** | 30 |
| **spbmolot** | 59 |
| **tagir_analyzes** | 13 |
| **vpakspace** | 8 |
| **zodigancode** | 35 |
| **Андрей Чуян** | 37 |
| **Виталий Оборин** | 9 |


### 5. Топ-30 самых цитируемых документов
_Файл: `docs/BACKLINKS.md` | 3 колонок, 30 строк_

| Документ | Входящих ссылок | Ссылающиеся файлы |
|----------|----------------|-------------------|
| `00-intro-part2` | 17 | `README.md`, `ACTION_ITEMS.md`, `CLUSTERS.md`, `CODE_BLOCKS.md` +13 |
| `03-component-catalog` | 14 | `README.md`, `ACTION_ITEMS.md`, `ALERTS.md`, `BROKEN_LINKS.md` +10 |
| `memnet` | 12 | `README.md`, `ACTION_ITEMS.md`, `CLUSTERS.md`, `CODE_BLOCKS.md` +8 |
| `249-composite-skills-agent-md` | 8 | `README.md`, `ACTION_ITEMS.md`, `CLUSTERS.md`, `CONCEPTS.md` +4 |
| `01-интегральный-анализ-профиля-sven` | 7 | `README.md`, `ACTION_ITEMS.md`, `CLUSTERS.md`, `CODE_BLOCKS.md` +3 |
| `01-executive-summary` | 6 | `README.md`, `CONCEPTS.md`, `DECISIONS.md`, `QA.md` +2 |
| `306-with-anthropic-s-cowork-platfor` | 6 | `README.md`, `ACTION_ITEMS.md`, `CLUSTERS.md`, `CODE_BLOCKS.md` +2 |
| `HEALTH` | 3 | `PROGRESS.md`, `README.md`, `REPORT.md` |
| `CONTACTS` | 3 | `PROGRESS.md`, `README.md`, `REPORT.md` |
| `07-mvp-planning` | 2 | `README.md`, `PROGRESS.md` |
| `02-общий-план-развития-nautilus-por` | 2 | `README.md`, `CODE_BLOCKS.md` |
| `141-4-nautilus-portal-as-reference-` | 2 | `README.md`, `CONCEPTS.md` |
| `spbmolot` | 2 | `CONTACT_PRIORITY.md`, `README.md` |
| `anastasiyaw` | 2 | `CONTACT_PRIORITY.md`, `README.md` |
| `kksudo` | 2 | `CONTACT_PRIORITY.md`, `README.md` |
| `SCORING` | 2 | `PROGRESS.md`, `README.md` |
| `SIMILAR` | 2 | `README.md`, `REPORT.md` |
| `READING_ORDER` | 2 | `README.md`, `REPORT.md` |
| `VALIDATION` | 2 | `README.md`, `REPORT.md` |
| `BROKEN_LINKS` | 2 | `README.md`, `REPORT.md` |
| `SITEMAP` | 2 | `README.md`, `REPORT.md` |
| `KPI` | 2 | `README.md`, `REPORT.md` |
| `NARRATIVE` | 2 | `README.md`, `REPORT.md` |
| `DECISIONS` | 2 | `README.md`, `REPORT.md` |
| `QUESTIONS` | 2 | `README.md`, `REPORT.md` |
| `09-architectural-gaps` | 1 | `README.md` |
| `11-integration-contracts` | 1 | `README.md` |
| `QA` | 1 | `README.md` |
| `10-second-order-ensembles` | 1 | `README.md` |
| `12-roadmap` | 1 | `README.md` |


### 6. Ссылки по разделам
_Файл: `docs/BACKLINKS.md` | 3 колонок, 9 строк_

| Раздел | Входящих | Исходящих |
|--------|----------|-----------|
| **01-svyazi** | 50 | 15 |
| **02-anthropic-vacancies** | 376 | 356 |
| **03-technology-combinations** | 6 | 6 |
| **04-ai-collaborations** | 16 | 16 |
| **05-habr-projects** | 20 | 9 |
| **badges** | 0 | 0 |
| **contacts** | 17 | 14 |
| **root** | 97 | 166 |
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


### 9. Топ доменов
_Файл: `docs/CITATION_INDEX.md` | 3 колонок, 20 строк_

| Домен | URL | Авторитетность |
|-------|-----|----------------|
| `habr.com` | 53 | ⭐⭐⭐⭐ |
| `github.com` | 48 | ⭐⭐⭐⭐⭐ |
| `raw.githubusercontent.com` | 11 | ⭐ |
| `3dnews.ru` | 2 | ⭐ |
| `claude.ai` | 2 | ⭐ |
| `api.github.com` | 2 | ⭐⭐⭐⭐⭐ |
| `fontanka.ru` | 1 | ⭐ |
| `discourse.org` | 1 | ⭐ |
| `eb.hypothes.is` | 1 | ⭐ |
| `claude.com` | 1 | ⭐ |
| `fossil-scm.org` | 1 | ⭐ |
| `support.claude.com` | 1 | ⭐ |
| `happyin.space` | 1 | ⭐ |
| `install.sh` | 1 | ⭐ |
| `creativecommons.org` | 1 | ⭐ |
| `activitypub.rocks` | 1 | ⭐ |
| `solidproject.org` | 1 | ⭐ |
| `3.org` | 1 | ⭐ |
| `habr` | 1 | ⭐ |
| `olegtalks.ru` | 1 | ⭐ |


### 10. Наиболее цитируемые URL
_Файл: `docs/CITATION_INDEX.md` | 4 колонок, 50 строк_

| URL | Файлов | Авторитетность | Домен |
|-----|--------|----------------|-------|
| `https://github.com/svend4/nautilus/issues` | 23 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/nautilus` | 13 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/ingit` | 10 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/pro2` | 8 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://habr.com/ru/articles/1007122/` | 8 | ⭐⭐⭐⭐ | `habr.com` |
| `https://github.com/AnastasiyaW/knowledge-space` | 6 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/info1` | 6 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://habr.com/ru/articles/1006622/` | 7 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1017200/` | 7 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/yandex/articles/1019928/` | 7 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/airi/articles/1000720/` | 7 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/495554/` | 7 | ⭐⭐⭐⭐ | `habr.com` |
| `https://github.com/svend4/meta` | 5 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://habr.com/ru/articles/1006602/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/938626/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027724/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/surfstudio/articles/943108/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027210/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1009608/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1024884/comments/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1002138/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/airi/articles/855128/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1023446/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/yoomoney/articles/1012870/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1014366/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027382/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/955798/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1010198/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1020598/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/983684/` | 6 | ⭐⭐⭐⭐ | `habr.com` |
| `https://github.com/mcp` | 4 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/settings/tokens` | 4 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://github.com/svend4/nautilus/blob/main/REVIEW_METHODOLOGY.md` | 4 | ⭐⭐⭐⭐⭐ | `github.com` |
| `https://habr.com/ru/articles/893356/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/companies/teamly/articles/1024062/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1010478/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027878/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1005776/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/943498/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1020860/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1027658/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/996144/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1019588/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/975414/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1009538/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1009958/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1016096/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1024634/` | 5 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1021622/` | 4 | ⭐⭐⭐⭐ | `habr.com` |
| `https://habr.com/ru/articles/1012894/` | 4 | ⭐⭐⭐⭐ | `habr.com` |


### 11. Содержание
_Файл: `docs/CODE_BLOCKS.md` | 2 колонок, 7 строк_

| Язык | Блоков |
|------|--------|
| 📝 Без языка | 174 |
| 💻 Bash / Shell | 36 |
| 🐍 Python | 35 |
| 📦 JSON | 22 |
| 📊 Диаграммы Mermaid | 19 |
| markdown | 17 |
| 📋 YAML | 5 |


### 12. Паспорт: /
_Файл: `docs/CODE_BLOCKS.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | / |
| Формат | `.` — краткое описание |
| Единица | что является одной записью |
| Адаптер | `adapters/.py` |
| Уровень совместимости | <0-3> —  |


### 13. Паспорт: /
_Файл: `docs/CODE_BLOCKS.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | / |
| Формат | `.` — краткое описание |
| Единица | что является одной записью |
| Адаптер | `adapters/.py` |
| Уровень совместимости | <0-3> — |


### 14. Паспорт: /
_Файл: `docs/CODE_BLOCKS.md` | 2 колонок, 5 строк_

| Поле | Значение |
|------|----------|
| Репозиторий | owner/my-notes |
| Формат | `.md` — Markdown notes |
| Единица | Markdown-документ |
| Адаптер | `adapters/my_notes.py` |
| Уровень совместимости | 1 — читаемый |


### 15. Изменившиеся файлы (307) — топ по Δ слов
_Файл: `docs/COMPARE.md` | 4 колонок, 30 строк_

| Файл | Было | Стало | Δ |
|------|------|-------|---|
| `OUTLINE.md` | 27895 | 34491 | +6596 |
| `SITEMAP.md` | 6806 | 1663 | -5143 |
| `PARAGRAPH_QUALITY.md` | 10192 | 14229 | +4037 |
| `TIMELINE.md` | 2061 | 4272 | +2211 |
| `TABLES.md` | 98785 | 99622 | +837 |
| `REPORT.md` | 304 | 932 | +628 |
| `CONTRADICTIONS.md` | 1386 | 1949 | +563 |
| `SEARCH.md` | 4112 | 4660 | +548 |
| `ACTION_ITEMS.md` | 7277 | 7697 | +420 |
| `NAMED_ENTITIES.md` | 1449 | 1783 | +334 |
| `SCORING.md` | 338 | 626 | +288 |
| `STALENESS.md` | 384 | 600 | +216 |
| `COVERAGE.md` | 646 | 860 | +214 |
| `VOCABULARY.md` | 882 | 1089 | +207 |
| `87-12-onboarding-paths-normative.md` | 407 | 595 | +188 |
| `163-9-call-for-partnership.md` | 443 | 628 | +185 |
| `COST.md` | 549 | 731 | +182 |
| `178-9-phased-rollout-strategy.md` | 452 | 632 | +180 |
| `SCHEDULE.md` | 271 | 444 | +173 |
| `175-6-ethical-framework.md` | 446 | 612 | +166 |
| `DECISIONS.md` | 2287 | 2452 | +165 |
| `READABILITY.md` | 17442 | 17606 | +164 |
| `CONTACT_PRIORITY.md` | 364 | 524 | +160 |
| `GITHUB_ISSUES.md` | 1095 | 1255 | +160 |
| `279-existing-approximations.md` | 449 | 604 | +155 |
| `316-8-implications-for-nautilus-and-okwf.md` | 579 | 731 | +152 |
| `177-8-risks-and-mitigations.md` | 471 | 620 | +149 |
| `CONCEPTS.md` | 13020 | 13165 | +145 |
| `317-9-risks-and-open-questions.md` | 484 | 627 | +143 |
| `160-6-governance-and-ethics.md` | 466 | 605 | +139 |


### 16. Распределение сложности
_Файл: `docs/COMPLEXITY.md` | 2 колонок, 3 строк_

| Уровень | Файлов |
|---------|--------|
| 🟢 Простой (0-1) | 848 |
| 🟡 Средний (2-3)  | 290 |
| 🔴 Сложный (4-5)  | 31 |


### 17. Самые сложные документы
_Файл: `docs/COMPLEXITY.md` | 6 колонок, 25 строк_

| Документ | Слов | Ср.длина пред. | Термин.плотность | Ур.заголовков | Балл |
|----------|------|---------------|-----------------|--------------|------|
| `342-что-такое-вариант-c-concept-doc` | 10643 | 26.7 | 0.17% | H5 | 🔴 Сложный |
| `343-lorenzo-catalyst-agent-глубокая` | 5710 | 26.4 | 0.25% | H5 | 🔴 Сложный |
| `components-by-name` | 1067 | 89.4 | 3.28% | H2 | 🔴 Сложный |
| `00-intro` | 8788 | 18.0 | 0.25% | H4 | 🔴 Сложный |
| `01-интегральный-анализ-профиля-sven` | 18913 | 15.8 | 0.14% | H4 | 🔴 Сложный |
| `133-обратная-связь` | 3706 | 17.5 | 0.35% | H4 | 🔴 Сложный |
| `150-appendix-c-version-history` | 4872 | 20.2 | 0.02% | H4 | 🔴 Сложный |
| `272-appendix-d-connection-diagram` | 3757 | 15.4 | 0.03% | H4 | 🔴 Сложный |
| `303-приложение-визуализация-позиции` | 1786 | 19.5 | 1.12% | H4 | 🔴 Сложный |
| `341-приложение-c-образец-спецификац` | 3520 | 24.3 | 0.45% | H4 | 🔴 Сложный |
| `365-развёрнутый-анализ-внуковой-ком` | 4153 | 18.2 | 0.99% | H4 | 🔴 Сложный |
| `03-local-first` | 395 | 20.2 | 3.8% | H4 | 🔴 Сложный |
| `05-benchmarks` | 830 | 28.8 | 2.41% | H4 | 🔴 Сложный |
| `00-intro` | 11344 | 18.4 | 1.32% | H2 | 🔴 Сложный |
| `14-ограничения-лицензии-и-что-пока-` | 3279 | 17.5 | 1.04% | H2 | 🔴 Сложный |
| `memnet` | 7164 | 16.5 | 1.02% | H3 | 🔴 Сложный |
| `ABBREVIATIONS` | 1117 | 159.7 | 1.61% | H2 | 🔴 Сложный |
| `COMPONENT_MATRIX` | 517 | 65.2 | 4.45% | H2 | 🔴 Сложный |
| `CONCEPTS` | 13194 | 412.8 | 0.3% | H2 | 🔴 Сложный |
| `CONTACT_PRIORITY` | 232 | 46.4 | 4.31% | H3 | 🔴 Сложный |
| `ENTITIES` | 394 | 25.6 | 9.9% | H2 | 🔴 Сложный |
| `FOOTNOTES` | 200 | 50.5 | 6.5% | H2 | 🔴 Сложный |
| `GLOSSARY` | 91 | 45.5 | 10.99% | H1 | 🔴 Сложный |
| `GRAPH` | 140 | 46.7 | 23.57% | H2 | 🔴 Сложный |
| `NETWORK` | 292 | 292.0 | 15.75% | H2 | 🔴 Сложный |


### 18. Самые простые документы
_Файл: `docs/COMPLEXITY.md` | 3 колонок, 15 строк_

| Документ | Слов | Балл |
|----------|------|------|
| `03-portal-protocol-md` | 58 | 🟢 Простой |
| `05-0-status-of-this-document` | 85 | 🟢 Простой |
| `06-1-introduction` | 371 | 🟢 Простой |
| `07-2-terminology` | 290 | 🟢 Простой |
| `08-3-registry-nautilus-json` | 318 | 🟢 Простой |
| `09-4-passport-passport-md` | 115 | 🟢 Простой |
| `105-review-methodology-md` | 59 | 🟢 Простой |
| `106-tl-dr` | 115 | 🟢 Простой |
| `107-1-контекст-и-мотивация` | 397 | 🟢 Простой |
| `108-2-формальный-workflow` | 284 | 🟢 Простой |
| `110-вопрос-fallback-ratio-как-критически` | 300 | 🟢 Простой |
| `112-5-связь-с-существующими-методологиям` | 360 | 🟢 Простой |
| `113-6-почему-это-валидный-паттерн-для-ai` | 147 | 🟢 Простой |
| `114-7-реализация-в-проекте-nautilus` | 292 | 🟢 Простой |
| `115-8-ограничения-и-открытые-вопросы` | 409 | 🟢 Простой |


### 19. Матрица возможностей
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


### 20. Покрытие возможностей
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


### 21. Каталог компонентов
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


### 22. Рекомендуемые ансамбли
_Файл: `docs/COMPONENT_MATRIX.md` | 3 колонок, 5 строк_

| Ансамбль | Компоненты | Ключевая функция |
|----------|-----------|-----------------|
| Knowledge OS | CardIndex + AgentFS + knowledge-space | Индекс знаний + AI FS |
| Memory Layer | Yodoca + NGT-memory + agent-memory-mcp | Долгосрочная память |
| Security Runtime | SENTINEL + AgentFS | PII-защита + MCP allowlist |
| Web Intelligence | Firecrawl + CardIndex + Yodoca | Краулинг → память |
| Agent Orchestra | Rufler + agent-pool + AI Factory | Оркестрация агентов |


### 23. Топ концептов по связям
_Файл: `docs/CONCEPT_GRAPH.md` | 4 колонок, 30 строк_

| Концепт | Файлов | Связей | Категория |
|---------|--------|--------|-----------|
| `docs` | 980 | 9271 | other |
| `anthropic` | 793 | 7971 | other |
| `claude` | 501 | 6150 | other |
| `источник` | 465 | 5969 | other |
| `mhtml` | 411 | 5539 | other |
| `снимок` | 400 | 5476 | other |
| `репозитория` | 387 | 5304 | project |
| `корень` | 377 | 5255 | other |
| `вакансии` | 305 | 4492 | other |
| `кластерам` | 295 | 4410 | other |
| `раздел` | 309 | 4403 | other |
| `vacancies` | 476 | 4319 | other |
| `summary` | 485 | 4228 | other |
| `диалога` | 270 | 4075 | other |
| `nautilus` | 320 | 3786 | other |
| `agent` | 355 | 3595 | agent |
| `tags` | 334 | 3459 | other |
| `architecture` | 237 | 2527 | other |
| `knowledge` | 242 | 2305 | other |
| `collaboration` | 188 | 1993 | other |
| `svyazi` | 249 | 1941 | project |
| `сходство` | 237 | 1879 | other |
| `habr` | 172 | 1865 | other |
| `layer` | 157 | 1750 | architecture |
| `work` | 158 | 1749 | other |
| `protocol` | 143 | 1723 | architecture |
| `portal` | 149 | 1709 | other |
| `memory` | 192 | 1704 | memory |
| `infrastructure` | 143 | 1548 | other |
| `projects` | 140 | 1488 | other |


### 24. Согласованность терминов
_Файл: `docs/CONSISTENCY.md` | 4 колонок, 11 строк_

| Термин | Канонично | Вариант | Файлов |
|--------|-----------|---------|--------|
| **knowledge-space** | `knowledge-space` | `knowledge space` | 15 |
| **knowledge-space** | `knowledge-space` | `knowledge_space` | 3 |
| **knowledge-space** | `knowledge-space` | `knowledgespace` | 4 |
| **AI Factory** | `AI Factory` | `AI-Factory` | 18 |
| **NGT Memory** | `NGT Memory` | `NGT-Memory` | 39 |
| **Auto AI Router** | `Auto AI Router` | `Auto-AI-Router` | 15 |
| **local-first** | `local-first` | `localfirst` | 1 |
| **self-improvement** | `self-improvement` | `self-improve` | 148 |
| **Svyazi 2.0** | `Svyazi 2.0` | `Svyazi-2.0` | 4 |
| **evidence envelope** | `Evidence Envelope` | `Evidence-Envelope` | 18 |
| **Card Envelope** | `Card Envelope` | `Card-Envelope` | 11 |


### 25. Ключевые авторы проектов
_Файл: `docs/CONTACTS.md` | 5 колонок, 15 строк_

| Автор | Проект | Слой | Упомянут в файлах | Первый вопрос |
|-------|--------|------|-------------------|---------------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 48 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 32 | — |
| **Cutcode** | AIF Handoff | orchestration | 34 | — |
| **Dmitriila** | SENTINEL | security | 34 | — |
| **MiXaiLL76** | Auto AI Router | security | 30 | — |
| **Sonia_Black** | knowledge-space | knowledge | 17 | — |
| **VitalyOborin** | Yodoca | memory | 37 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 41 | — |
| **andrey_chuyan** | Svyazi | ingestion/CardIndex | 13 | Стоит ли расширять CardIndex до person/project/episode/evidence или лучше держать разные индексы? |
| **kksudo** | AgentFS | knowledge/filesystem | 52 | Что лучше класть в .agentos, а что выносить в machine-only state вне vault conventions? |
| **lee-to** | AI Factory | orchestration | 11 | — |
| **nlaik** | LiteParse / research-docs | rag | 29 | — |
| **spbmolot** | NGT Memory | memory | 56 | Где проходит практическая граница между полезной ассоциацией и ложной ко-активацией тем для community discovery? |
| **tagir_analyzes** | Legal RAG | rag | 12 | — |
| **zodigancode** | Rufler | orchestration | 34 | — |


### 26. GitHub репозитории
_Файл: `docs/CONTACTS.md` | 2 колонок, 45 строк_

| Репозиторий | Упоминается в файлах |
|-------------|---------------------|
| `github.com/github.com/AnastasiyaW` | 4 |
| `github.com/github.com/AnastasiyaW/knowledge-space` | 10 |
| `github.com/github.com/Antipozitive` | 4 |
| `github.com/github.com/Cutcode` | 4 |
| `github.com/github.com/Dmitriila` | 4 |
| `github.com/github.com/MiXaiLL76` | 4 |
| `github.com/github.com/NicholasSpisak/second-brain` | 3 |
| `github.com/github.com/Sonia` | 4 |
| `github.com/github.com/VitalyOborin` | 4 |
| `github.com/github.com/VitalyOborin/yodoca` | 4 |
| `github.com/github.com/VladSpace` | 4 |
| `github.com/github.com/andrey` | 4 |
| `github.com/github.com/anthropics/mcp` | 5 |
| `github.com/github.com/artur-gavronchuk/tg-chat-analyser` | 5 |
| `github.com/github.com/camel-ai/camel` | 6 |
| `github.com/github.com/dementev-dev/adversarial-review` | 5 |
| `github.com/github.com/github` | 2 |
| `github.com/github.com/kagvi13/HMP.` | 2 |
| `github.com/github.com/kksudo` | 4 |
| `github.com/github.com/kksudo/agentfs` | 4 |
| `github.com/github.com/lib4u/rufler` | 2 |
| `github.com/github.com/mcp` | 8 |
| `github.com/github.com/nlaik` | 4 |
| `github.com/github.com/ruvnet/ruflo` | 2 |
| `github.com/github.com/settings/tokens` | 6 |
| `github.com/github.com/spbmolot` | 4 |
| `github.com/github.com/spbmolot/ngt-memory` | 4 |
| `github.com/github.com/svend4` | 4 |
| `github.com/github.com/svend4/data70` | 6 |
| `github.com/github.com/svend4/info1` | 12 |
| `github.com/github.com/svend4/info40` | 4 |
| `github.com/github.com/svend4/info7` | 4 |
| `github.com/github.com/svend4/ingit` | 14 |
| `github.com/github.com/svend4/meta` | 11 |
| `github.com/github.com/svend4/n` | 2 |
| `github.com/github.com/svend4/nautilu` | 2 |
| `github.com/github.com/svend4/nautilus` | 60 |
| `github.com/github.com/svend4/nautilus.` | 3 |
| `github.com/github.com/svend4/nautilus.git` | 3 |
| `github.com/github.com/svend4/pro2` | 13 |
| `github.com/github.com/tagir` | 3 |
| `github.com/github.com/users/svend4` | 5 |
| `github.com/github.com/vuguzum/self-aware-mcp-server` | 6 |
| `github.com/github.com/yjs/yjs` | 3 |
| `github.com/github.com/zodigancode` | 3 |


### 27. Топ авторов по приоритету
_Файл: `docs/CONTACT_PRIORITY.md` | 7 колонок, 15 строк_

| # | Автор | Проект | Слой | Упоминаний | Статус | Балл |
|---|-------|--------|------|-----------|--------|------|
| 1 | **spbmolot** | NGT Memory | memory | 56 | 👁 Изучили | 179 |
| 2 | **kksudo** | AgentFS | knowledge/filesystem | 52 | 👁 Изучили | 167 |
| 3 | **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 48 | ⬜ Не начато | 150 |
| 4 | **VladSpace** | Graph RAG | rag | 41 | ⬜ Не начато | 127 |
| 5 | **VitalyOborin** | Yodoca | memory | 37 | ⬜ Не начато | 117 |
| 6 | **Cutcode** | AIF Handoff | orchestration | 34 | ⬜ Не начато | 106 |
| 7 | **zodigancode** | Rufler | orchestration | 34 | ⬜ Не начато | 106 |
| 8 | **Dmitriila** | SENTINEL | security | 34 | ⬜ Не начато | 104 |
| 9 | **Antipozitive** | MemNet | memory | 32 | ⬜ Не начато | 102 |
| 10 | **MiXaiLL76** | Auto AI Router | security | 30 | ⬜ Не начато | 92 |
| 11 | **nlaik** | LiteParse / research-docs | rag | 29 | ⬜ Не начато | 91 |
| 12 | **Sonia_Black** | knowledge-space | knowledge | 17 | ⬜ Не начато | 57 |
| 13 | **andrey_chuyan** | Svyazi | ingestion/CardIndex | 13 | ⬜ Не начато | 41 |
| 14 | **tagir_analyzes** | Legal RAG | rag | 12 | ⬜ Не начато | 40 |
| 15 | **lee-to** | AI Factory | orchestration | 11 | ⬜ Не начато | 37 |


### 28. Рекомендуется создать документы
_Файл: `docs/CONTENT_GAPS.md` | 3 колонок, 50 строк_

| Концепция | Упоминаний | Рекомендуемая папка |
|-----------|-----------|-------------------|
| `MHTML` | 500 | `docs/nautilus/` |
| `NPP` | 74 | `docs/nautilus/` |
| `GDPR` | 59 | `docs/nautilus/` |
| `MUST` | 56 | `docs/nautilus/` |
| `BSL` | 41 | `docs/04-ai-collaborations/` |
| `SHOULD` | 41 | `docs/nautilus/` |
| `XII` | 34 | `docs/nautilus/` |
| `PDF` | 30 | `docs/technology-combinations/` |
| `BSG` | 30 | `docs/02-anthropic-vacancies/` |
| `PII` | 29 | `docs/nautilus/` |
| `LinkedIn` | 28 | `docs/nautilus/` |
| `KSV` | 27 | `docs/nautilus/` |
| `AIF` | 26 | `docs/svyazi-2-0/` |
| `URL` | 26 | `docs/02-anthropic-vacancies/` |
| `MAY` | 26 | `docs/nautilus/` |
| `YiJing` | 24 | `docs/02-anthropic-vacancies/` |
| `HMP` | 24 | `docs/lorenzo-agent/` |
| `EMEA` | 23 | `docs/anthropic-vacancies/` |
| `RLM` | 22 | `docs/svyazi-2-0/` |
| `HIPAA` | 22 | `docs/02-anthropic-vacancies/` |
| `EIC` | 21 | `docs/nautilus/` |
| `AutoGen` | 21 | `docs/nautilus/` |
| `IDF` | 20 | `docs/svyazi-2-0/` |
| `OpenWhispr` | 18 | `docs/svyazi-2-0/` |
| `LCI` | 18 | `docs/habr-unique-projects/` |
| `CodeWiki` | 16 | `docs/svyazi-2-0/` |
| `BaseAdapter` | 16 | `docs/02-anthropic-vacancies/` |
| `RSS` | 16 | `docs/lorenzo-agent/` |
| `DeepSeek` | 15 | `docs/habr-unique-projects/` |
| `ChatDev` | 15 | `docs/nautilus/` |
| `III` | 14 | `docs/02-anthropic-vacancies/` |
| `LangChain` | 14 | `docs/02-anthropic-vacancies/` |
| `AIRI` | 14 | `docs/02-anthropic-vacancies/` |
| `IBM` | 13 | `docs/technology-combinations/` |
| `DOCX` | 13 | `docs/nautilus/` |
| `Composite Skills Agents` | 13 | `docs/nautilus/` |
| `Professional Colleague Agents (EN)` | 13 | `docs/nautilus/` |
| `Профессиональные Коллеги-Агенты (RU)` | 13 | `docs/nautilus/` |
| `Representative Agent Layer (EN)` | 13 | `docs/nautilus/` |
| `Representative Agent Layer (RU)` | 13 | `docs/nautilus/` |
| `STDP` | 12 | `docs/habr-unique-projects/` |
| `CRM` | 12 | `docs/nautilus/` |
| `TypeScript` | 12 | `docs/02-anthropic-vacancies/` |
| `SGG` | 12 | `docs/nautilus/` |
| `FAISS` | 11 | `docs/svyazi-2-0/` |
| `GPU` | 11 | `docs/habr-unique-projects/` |
| `RDF` | 11 | `docs/02-anthropic-vacancies/` |
| `DeepMind` | 11 | `docs/02-anthropic-vacancies/` |
| `ArXiv` | 11 | `docs/lorenzo-agent/` |
| `VPS` | 11 | `docs/02-anthropic-vacancies/` |


### 29. Итого
_Файл: `docs/COST.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Человеко-недель | **25** |
| Человеко-часов | **1,000** |
| Бюджет (USD) | **$86,400** |
| Календарный срок | **~6-8 месяцев** |
| Команда | **5 ролей** |


### 30. По компонентам
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


### 31. По ролям
_Файл: `docs/COST.md` | 4 колонок, 5 строк_

| Роль | Ставка USD/ч | Недель | Итого USD |
|------|-------------|--------|----------|
| Senior Python Dev | $85 | 11 | $37,400 |
| AI/ML Engineer | $110 | 7 | $30,800 |
| DevOps | $75 | 2 | $6,000 |
| Tech Writer | $45 | 1 | $1,800 |
| Project Manager | $65 | 4 | $10,400 |


### 32. Сценарии
_Файл: `docs/COST.md` | 4 колонок, 3 строк_

| Сценарий | Команда | Срок | Бюджет |
|----------|---------|------|--------|
| Минимальный (solo) | 1 разработчик | ~18 мес | $28,800 |
| Оптимальный | 3 человека | ~8 мес | $43,200 |
| Ускоренный | 5 человек | ~5 мес | $86,400 |


### 33. Временные оценки из документов
_Файл: `docs/COST.md` | 3 колонок, 11 строк_

| Источник | Контекст | Недель |
|----------|----------|--------|
| `365-развёрнутый-анал` | Макс) и part-time, реальный timeline 12-24 месяца для full a… | 96 |
| `343-lorenzo-catalyst` | рудоёмкий процесс подачи - Может быть 6-18 месяцев до финанс… | 72 |
| `365-развёрнутый-анал` | eam. С solo developer (Макс) и part-time, реальный timeline … | 72 |
| `ACTION_ITEMS` | обратная-связь_ - 5: Burnout. Проект 12-18 месяцев для singl… | 72 |
| `CONCEPTS` | инимально жизнеспособный прототип за 12-18 месяцев     _→ [N… | 72 |
| `DECISIONS` | document — структурированный план на 12-18 месяцев, который … | 72 |
| `TABLES` | 65-развёрнутый-анал` | Макс) и part-time, реальный timeline … | 72 |
| `01-response` | есяцев) → maybe eventual formalization как RFC or standard (… | 72 |
| `332-6-уточнённый-объ` | ультат:** Чистая временная линия: От 10-16 месяцев до пример… | 64 |
| `332-6-уточнённый-объ` | Оригинальная дорожная карта InGit (10-16 месяцев до v1.0) от… | 64 |
| `06-utochnyonnyy-obyo` | окращённый Объём  Оригинальный план: 10-16 месяцев до v1.0 с… | 64 |


### 34. Сводка по секциям
_Файл: `docs/COVERAGE.md` | 8 колонок, 5 строк_

| Секция | Файлов | Summary | Теги | TOC | CrossRefs | Статус | Backlinks |
|--------|--------|---------|------|-----|-----------|--------|-----------|
| `01-svyazi` | 14 | 🟢 13/14 | 🟢 13/14 | 🔴 2/14 | 🟢 12/14 | 🔴 0/14 | 🔴 0/14 |
| `02-anthropic-vacancies` | 355 | 🟢 351/355 | 🟢 343/355 | 🟡 184/355 | 🟢 338/355 | 🔴 0/355 | 🔴 0/355 |
| `03-technology-combinations` | 5 | 🟢 5/5 | 🟢 5/5 | 🔴 1/5 | 🟢 5/5 | 🔴 0/5 | 🔴 0/5 |
| `04-ai-collaborations` | 15 | 🟢 15/15 | 🟢 15/15 | 🔴 0/15 | 🟢 15/15 | 🟢 15/15 | 🔴 0/15 |
| `05-habr-projects` | 6 | 🟢 6/6 | 🟢 6/6 | 🔴 1/6 | 🟢 6/6 | 🟢 6/6 | 🔴 0/6 |


### 35. Файлы с низким покрытием (< 3 признаков) — 22 файлов
_Файл: `docs/COVERAGE.md` | 8 колонок, 22 строк_

| Файл | Слов | Summary | Теги | TOC | CrossRefs | ## Статус | Backlinks |
|------|------| ---|---|---|---|---|--- |
| `docs/01-svyazi/00-intro-part2.md` | 5 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 20 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 91 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 93 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 41 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | 179 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | 140 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 148 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 29 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 35 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 38 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 36 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | 35 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | 35 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | 36 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/31-content-overview.md` | 27 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | 37 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 110 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 178 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 77 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 75 | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |


### 36. Матрица сходства секций
_Файл: `docs/CROSS_SECTION.md` | 7 колонок, 6 строк_

| Секция | Svyazi 2.0 | Anthropic | Технологии | AI-ансамбли | Хабр-проекты | Контакты |
|--------|------|------|------|------|------|------|
| `Svyazi 2.0` | **—** | 0.09 ░░░░░ | 0.16 █░░░░ | 0.94 █████ | 0.19 █░░░░ | 0.07 ░░░░░ |
| `Anthropic` | 0.09 ░░░░░ | **—** | 0.22 ██░░░ | 0.16 █░░░░ | 0.23 ██░░░ | 0.07 ░░░░░ |
| `Технологии` | 0.16 █░░░░ | 0.22 ██░░░ | **—** | 0.28 ██░░░ | 0.42 ████░ | 0.10 ░░░░░ |
| `AI-ансамбли` | 0.94 █████ | 0.16 █░░░░ | 0.28 ██░░░ | **—** | 0.42 ████░ | 0.12 █░░░░ |
| `Хабр-проекты` | 0.19 █░░░░ | 0.23 ██░░░ | 0.42 ████░ | 0.42 ████░ | **—** | 0.14 █░░░░ |
| `Контакты` | 0.07 ░░░░░ | 0.07 ░░░░░ | 0.10 ░░░░░ | 0.12 █░░░░ | 0.14 █░░░░ | **—** |


### 37. Топ-40 кросс-секционных концептов
_Файл: `docs/CROSS_SECTION.md` | 4 колонок, 40 строк_

| Концепт | Секций | Авг. TF-IDF | Присутствует в |
|---------|--------|-------------|----------------|
| `svyazi` | 6 | 14.8827 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `связи` | 6 | 10.8618 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `сходство` | 6 | 10.1983 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `профиль` | 6 | 8.2149 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `вопросы` | 6 | 6.5560 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `проекты` | 6 | 6.1530 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `knowledge` | 6 | 6.0293 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `habr` | 6 | 5.9814 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `memory` | 6 | 5.6917 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `legal` | 6 | 4.3504 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `документы` | 6 | 3.9300 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `похожие` | 6 | 3.7044 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `cardindex` | 6 | 3.6463 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `yodoca` | 6 | 3.5423 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `agentfs` | 6 | 2.7332 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `автоматически` | 6 | 2.6732 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `contents` | 6 | 2.6600 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `space` | 6 | 2.6465 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `executive` | 6 | 2.6073 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `router` | 6 | 2.3725 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `graph` | 6 | 2.3342 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `между` | 6 | 2.3156 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `auto` | 6 | 1.8066 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `research` | 6 | 1.7141 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `state` | 6 | 1.4958 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `лучше` | 6 | 1.4943 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `memnet` | 6 | 1.2179 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `vault` | 6 | 1.1168 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `discovery` | 6 | 1.1147 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `project` | 6 | 0.8605 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `одной` | 6 | 0.8243 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `agentos` | 6 | 0.8098 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `содержание` | 6 | 0.6447 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `community` | 6 | 0.6409 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `качество` | 6 | 0.5198 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `отдельный` | 6 | 0.5186 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `only` | 6 | 0.4592 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `файлов` | 6 | 0.3404 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `статус` | 5 | 14.9001 | `Svyazi 2.0`, `Anthropic`, `AI-ансамбли`, `Хабр-проекты`, `Контакты` |
| `view` | 5 | 12.6927 | `Svyazi 2.0`, `Anthropic`, `Технологии`, `AI-ансамбли`, `Хабр-проекты` |


### 38. Детальная карта концептов
_Файл: `docs/CROSS_SECTION.md` | 7 колонок, 20 строк_

| Концепт | Svyazi 2.0 | Anthropic | Технологии | AI-ансамбл | Хабр-проек | Контакты |
|---------|------|------|------|------|------|------|
| `svyazi` | **20.388** | **1.193** | **15.888** | **17.134** | **8.422** | **26.271** |
| `связи` | **0.324** | **0.067** | **0.935** | **1.872** | **2.651** | **59.322** |
| `сходство` | **4.747** | **5.624** | **7.009** | **2.400** | **3.275** | **38.136** |
| `профиль` | **0.324** | **0.177** | **0.935** | **0.240** | **0.156** | **47.458** |
| `вопросы` | **1.079** | **0.961** | **0.467** | **0.768** | **0.468** | **35.593** |
| `проекты` | **1.726** | **0.349** | **5.607** | **2.544** | **2.963** | **23.729** |
| `knowledge` | **4.854** | **2.631** | **12.617** | **4.703** | **3.743** | **7.627** |
| `habr` | **0.755** | **1.279** | **10.280** | **4.223** | **7.486** | **11.864** |
| `memory` | **10.464** | **1.554** | **0.935** | **8.783** | **7.330** | **5.085** |
| `legal` | **1.834** | **1.334** | **11.682** | **3.408** | **5.303** | **2.542** |
| `документы` | **1.942** | **2.680** | **3.271** | **1.104** | **1.871** | **12.712** |
| `похожие` | **1.726** | **2.142** | **3.271** | **0.816** | **1.560** | **12.712** |
| `cardindex` | **5.178** | **0.239** | **7.944** | **3.792** | **2.183** | **2.542** |
| `yodoca` | **4.854** | **0.043** | **5.140** | **3.216** | **5.458** | **2.542** |
| `agentfs` | **6.149** | **0.092** | **1.869** | **4.032** | **1.716** | **2.542** |
| `автоматически` | **0.216** | **0.159** | **2.336** | **0.528** | **0.936** | **11.864** |
| `contents` | **1.079** | **1.842** | **0.467** | **0.240** | **0.468** | **11.864** |
| `space` | **3.560** | **0.422** | **1.869** | **3.072** | **1.871** | **5.085** |
| `executive` | **3.236** | **0.373** | **5.140** | **3.551** | **2.495** | **0.848** |
| `router` | **1.726** | **0.043** | **7.944** | **1.200** | **0.780** | **2.542** |


### 39. Карта плотности тем
_Файл: `docs/DENSITY.md` | 8 колонок, 20 строк_

| Тема | 01-svyazi | 02-vacancies | 03-tech | 04-collab | 05-habr | root | Итого |
|------|-----------|--------------|---------|-----------|---------|------|-------|
| **Svyazi** | 196 | 230 | 31 | 395 | 65 | 4306 | **5223** |
| **CardIndex** | 59 | 57 | 16 | 103 | 12 | 644 | **891** |
| **AgentFS** | 60 | 94 | 4 | 105 | 28 | 635 | **926** |
| **Yodoca** | 94 | 36 | 22 | 134 | 70 | 1114 | **1470** |
| **NGT-memory** | 176 | 426 | 3 | 275 | 84 | 2041 | **3005** |
| **SENTINEL** | 47 | 8 | 0 | 59 | 0 | 242 | **356** |
| **Rufler** | 38 | 20 | 0 | 46 | 0 | 282 | **386** |
| **AI Factory** | 65 | 46 | 0 | 84 | 0 | 516 | **711** |
| **Knowledge OS** | 0 | 19 | 0 | 4 | 0 | 102 | **125** |
| **Forensic RAG** | 35 | 20 | 1 | 52 | 2 | 334 | **444** |
| **MCP** | 63 | 687 | 4 | 149 | 56 | 1284 | **2243** |
| **MVP** | 65 | 96 | 0 | 95 | 7 | 793 | **1056** |
| **Архитектура** | 70 | 603 | 16 | 146 | 36 | 1666 | **2537** |
| **Безопасность** | 53 | 132 | 1 | 68 | 1 | 997 | **1252** |
| **Лицензия** | 104 | 644 | 0 | 125 | 13 | 1568 | **2454** |
| **Roadmap** | 29 | 145 | 0 | 28 | 3 | 514 | **719** |
| **Вакансии** | 2 | 3268 | 6 | 15 | 11 | 14792 | **18094** |
| **Комбинации** | 11 | 148 | 57 | 16 | 9 | 2786 | **3027** |
| **Habr** | 37 | 252 | 20 | 200 | 97 | 2863 | **3469** |
| **Контакты** | 18 | 131 | 0 | 21 | 6 | 492 | **668** |


### 40. Наиболее раскрытые темы
_Файл: `docs/DENSITY.md` | 3 колонок, 10 строк_

| Тема | Упоминаний | Визуализация |
|------|------------|-------------|
| **Вакансии** | 18094 | `███████████████` |
| **Svyazi** | 5223 | `████░░░░░░░░░░░` |
| **Habr** | 3469 | `██░░░░░░░░░░░░░` |
| **Комбинации** | 3027 | `██░░░░░░░░░░░░░` |
| **NGT-memory** | 3005 | `██░░░░░░░░░░░░░` |
| **Архитектура** | 2537 | `██░░░░░░░░░░░░░` |
| **Лицензия** | 2454 | `██░░░░░░░░░░░░░` |
| **MCP** | 2243 | `█░░░░░░░░░░░░░░` |
| **Yodoca** | 1470 | `█░░░░░░░░░░░░░░` |
| **Безопасность** | 1252 | `█░░░░░░░░░░░░░░` |


### 41. Где сосредоточена каждая тема
_Файл: `docs/DENSITY.md` | 3 колонок, 20 строк_

| Тема | Основной раздел | % |
|------|-----------------|---|
| Svyazi | `root` | 82% |
| CardIndex | `root` | 72% |
| AgentFS | `root` | 68% |
| Yodoca | `root` | 75% |
| NGT-memory | `root` | 67% |
| SENTINEL | `root` | 67% |
| Rufler | `root` | 73% |
| AI Factory | `root` | 72% |
| Knowledge OS | `root` | 81% |
| Forensic RAG | `root` | 75% |
| MCP | `root` | 57% |
| MVP | `root` | 75% |
| Архитектура | `root` | 65% |
| Безопасность | `root` | 79% |
| Лицензия | `root` | 63% |
| Roadmap | `root` | 71% |
| Вакансии | `root` | 81% |
| Комбинации | `root` | 92% |
| Habr | `root` | 82% |
| Контакты | `root` | 73% |


### 42. Python-зависимости
_Файл: `docs/DEPENDABOT.md` | 5 колонок, 4 строк_

| Пакет | Мин. версия | Последняя (PyPI) | Статус | Используется в |
|-------|------------|-----------------|--------|----------------|
| `anthropic` | `0.25.0` | `—` | — | `scripts/improve_llm_*.py` |
| `mcp` | `1.0.0` | `—` | — | `scripts/mcp_server.py` |
| `pre-commit` | `3.0.0` | `—` | — | `.pre-commit-config.yaml` |
| `pyspellchecker` | `0.8.0` | `—` | — | `scripts/improve_spellcheck.py` |


### 43. OSS-проекты (Svyazi 2.0)
_Файл: `docs/DEPENDABOT.md` | 3 колонок, 4 строк_

| Проект | Репозиторий | Статус |
|--------|------------|--------|
| AgentFS | [https://github.com/kksudo/agentfs](https://github.com/kksudo/agentfs) | — |
| NGT Memory | [https://github.com/spbmolot/ngt-memory](https://github.com/spbmolot/ngt-memory) | — |
| Yodoca | [https://github.com/VitalyOborin/yodoca](https://github.com/VitalyOborin/yodoca) | — |
| knowledge-space | [https://github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space) | — |


### 44. Зависимости
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


### 45. История коммитов (последние 15)
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


### 46. Текущее состояние репозитория
_Файл: `docs/DIGEST.md` | 2 колонок, 3 строк_

| Параметр | Значение |
|----------|---------|
| Документов `.md` | **460** |
| Скриптов обработки | **56** |
| Последнее обновление | **2026-04-29** |


### 47. Сводка
_Файл: `docs/DIGEST_AUTO.md` | 2 колонок, 5 строк_

| Метрика | Значение |
|---------|----------|
| Коммитов | **86** |
| Новых файлов | **20** |
| Изменённых файлов | **0** |
| Слов добавлено | **+0** |
| Слов удалено | **−0** |


### 48. Активность по секциям
_Файл: `docs/DIGEST_AUTO.md` | 2 колонок, 8 строк_

| Секция | Изменений |
|--------|-----------|
| `nautilus` | ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 255 |
| `Anthropic` | ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 234 |
| `Скрипты` | ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 158 |
| `anthropic-vacancies` | ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 111 |
| `lorenzo-agent` | ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 62 |
| `svyazi-2-0` | ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 59 |
| `habr-unique-projects` | ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 56 |
| `technology-combinations` | ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 53 |


### 49. Итого
_Файл: `docs/DIGEST_WEEKLY.md` | 2 колонок, 5 строк_

| Метрика | Значение |
|---------|---------|
| Коммитов за неделю | **75** |
| Новых файлов | **0** |
| Изменённых файлов | **0** |
| Всего MD файлов | **1170** |
| Всего слов | **905,038** |


### 50. Файлы с ≥50% пустых секций (приоритет)
_Файл: `docs/EMPTY_SECTIONS.md` | 4 колонок, 129 строк_

| Файл | Пустых | Всего | % |
|------|--------|-------|---|
| `QA.md` | 12 | 12 | 100% |
| `03-portal-protocol-md.md` | 1 | 1 | 100% |
| `105-review-methodology-md.md` | 1 | 1 | 100% |
| `125-readme-mcp-md-инструкция-по-установке.md` | 1 | 1 | 100% |
| `134-the-double-triangle-architecture-md.md` | 1 | 1 | 100% |
| `151-open-knowledge-work-foundation-md.md` | 1 | 1 | 100% |
| `166-representative-agent-layer-md.md` | 1 | 1 | 100% |
| `187-слой-представительских-агентов-md.md` | 1 | 1 | 100% |
| `208-professional-colleague-agents-md.md` | 1 | 1 | 100% |
| `249-composite-skills-agent-md.md` | 1 | 1 | 100% |
| `250-bridging-the-gap-between-profession-wide-and-indiv.md` | 1 | 1 | 100% |
| `273-infrastructure-for-ai-collaborative-intellectual-w.md` | 1 | 1 | 100% |
| `304-ingit-as-cowork-native-workspace-substrate-md.md` | 1 | 1 | 100% |
| `344-системный-промпт-для-lorenzo-project.md` | 1 | 1 | 100% |
| `35-passports-info1-md.md` | 1 | 1 | 100% |
| `45-passports-pro2-md.md` | 1 | 1 | 100% |
| `55-passports-meta-md.md` | 1 | 1 | 100% |
| `73-portal-protocol-md-v1-1.md` | 1 | 1 | 100% |
| `QA.md` | 23 | 23 | 100% |
| `QA.md` | 12 | 12 | 100% |
| `QA.md` | 15 | 15 | 100% |
| `QA.md` | 11 | 11 | 100% |
| `README.md` | 1 | 1 | 100% |
| `ALERTS.md` | 1 | 1 | 100% |
| `CONSISTENCY.md` | 13 | 13 | 100% |
| `QA.md` | 103 | 103 | 100% |
| `QA.md` | 6 | 6 | 100% |
| `README.md` | 2 | 2 | 100% |
| `.md` | 2 | 2 | 100% |
| `cowork.md` | 2 | 2 | 100% |
| `ingit.md` | 2 | 2 | 100% |
| `kksudo.md` | 2 | 2 | 100% |
| `lorenzo.md` | 2 | 2 | 100% |
| `nautilus.md` | 2 | 2 | 100% |
| `sgb.md` | 2 | 2 | 100% |
| `spbmolot.md` | 2 | 2 | 100% |
| `svend4.md` | 2 | 2 | 100% |
| `svyazi.md` | 2 | 2 | 100% |
| `README.md` | 1 | 1 | 100% |
| `QA.md` | 17 | 17 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `README.md` | 1 | 1 | 100% |
| `CODE_BLOCKS.md` | 101 | 102 | 99% |
| `SPELLCHECK.md` | 26 | 27 | 96% |
| `NAMED_ENTITIES.md` | 25 | 30 | 83% |
| `28-appendix-a-minimal-working-example.md` | 4 | 5 | 80% |
| `research-summary.md` | 4 | 5 | 80% |
| `16-appendix-a-minimal-working-example.md` | 4 | 5 | 80% |
| `research-note.md` | 4 | 5 | 80% |
| `READING_ORDER.md` | 3 | 4 | 75% |
| `SCHEDULE.md` | 6 | 8 | 75% |
| `RISK_REGISTER.md` | 11 | 16 | 69% |
| `127-подключение-к-claude-desktop.md` | 4 | 6 | 67% |
| `98-appendix-a-minimal-working-example.md` | 4 | 6 | 67% |
| `HEALTH.md` | 4 | 6 | 67% |
| `MINDMAP.md` | 2 | 3 | 67% |
| `11-relevance-ranking.md` | 2 | 3 | 67% |
| `ensemble.md` | 4 | 6 | 67% |
| `126-установка.md` | 3 | 5 | 60% |
| `06-adapter-interface.md` | 3 | 5 | 60% |
| `15-glossary.md` | 3 | 5 | 60% |
| `06-adapter-interface.md` | 3 | 5 | 60% |
| `decision-record.md` | 3 | 5 | 60% |
| `project-component.md` | 3 | 5 | 60% |
| `09-4-passport-passport-md.md` | 4 | 7 | 57% |
| `22-glossary.md` | 7 | 13 | 54% |
| `121-appendix-c-история-изменений-методологии.md` | 1 | 2 | 50% |
| `18-6-adapter-interface.md` | 3 | 6 | 50% |
| `19-7-portalentry-structure.md` | 1 | 2 | 50% |
| `22-10-queryresult-structure.md` | 1 | 2 | 50% |
| `229-профессиональные-коллеги-агенты.md` | 1 | 2 | 50% |
| `320-references.md` | 3 | 6 | 50% |
| `324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | 1 | 2 | 50% |
| `338-ссылки.md` | 3 | 6 | 50% |
| `65-readme-md.md` | 1 | 2 | 50% |
| `81-6-adapter-interface.md` | 3 | 6 | 50% |
| `86-11-relevance-ranking.md` | 2 | 4 | 50% |
| `README.md` | 1 | 2 | 50% |
| `CONCEPT_GRAPH.md` | 1 | 2 | 50% |
| `CONTACTS.md` | 2 | 4 | 50% |
| `CONTACT_PRIORITY.md` | 2 | 4 | 50% |
| `COVERAGE.md` | 2 | 4 | 50% |
| `GRAPH.md` | 1 | 2 | 50% |
| `INDEX.md` | 6 | 12 | 50% |
| `MISSING.md` | 1 | 2 | 50% |
| `ORPHANS.md` | 2 | 4 | 50% |
| `README.md` | 1 | 2 | 50% |
| `README.md` | 1 | 2 | 50% |
| `07-portal-entry.md` | 1 | 2 | 50% |
| `10-query-result.md` | 1 | 2 | 50% |
| `12-versioning-policy.md` | 2 | 4 | 50% |
| `09-consensus-algorithm.md` | 3 | 6 | 50% |
| `14-sdk.md` | 2 | 4 | 50% |
| `15-appendix-c-history.md` | 1 | 2 | 50% |
| `agentfs.md` | 1 | 2 | 50% |
| `ai-factory.md` | 1 | 2 | 50% |
| `autoresearch-sequential.md` | 1 | 2 | 50% |
| `graph-rag.md` | 1 | 2 | 50% |
| `hybrid-rag.md` | 1 | 2 | 50% |
| `knowledge-space.md` | 1 | 2 | 50% |
| `legal-rag.md` | 1 | 2 | 50% |
| `mclaude.md` | 1 | 2 | 50% |
| `memnet.md` | 1 | 2 | 50% |
| `ngt-memory.md` | 1 | 2 | 50% |
| `research-docs-liteparse.md` | 1 | 2 | 50% |
| `rufler.md` | 1 | 2 | 50% |
| `self-aware-mcp.md` | 1 | 2 | 50% |
| `voice-stack.md` | 1 | 2 | 50% |
| `yjs-automerge.md` | 1 | 2 | 50% |
| `yodoca.md` | 1 | 2 | 50% |
| `A-collaboration-os.md` | 1 | 2 | 50% |
| `B-forensic-rag.md` | 1 | 2 | 50% |
| `C-multi-agent-factory.md` | 1 | 2 | 50% |
| `D-voice-first-mesh.md` | 1 | 2 | 50% |
| `E-execution-plane.md` | 1 | 2 | 50% |
| `F-evidence-backed-intake.md` | 1 | 2 | 50% |
| `G-federated-local-graph.md` | 1 | 2 | 50% |
| `H-research-to-product-flywheel.md` | 1 | 2 | 50% |
| `README.md` | 1 | 2 | 50% |


### 51. Люди и авторы (7)
_Файл: `docs/ENTITIES.md` | 3 колонок, 7 строк_

| Имя | Упоминаний | Файлов |
|---------|------------|--------|
| **Lorenzo** | 2570 | 140 |
| **svend4** | 1351 | 237 |
| **spbmolot** | 165 | 55 |
| **kksudo** | 162 | 54 |
| **Андрей** | 126 | 40 |
| **Виталий** | 51 | 29 |
| **Антропик** | 9 | 7 |


### 52. Проекты (22)
_Файл: `docs/ENTITIES.md` | 3 колонок, 22 строк_

| Проект | Упоминаний | Файлов |
|---------|------------|--------|
| **Nautilus** | 7811 | 508 |
| **Svyazi** | 4594 | 311 |
| **Cowork** | 2677 | 171 |
| **Lorenzo** | 2570 | 140 |
| **ingit** | 2447 | 144 |
| **SGB** | 1130 | 199 |
| **Yodoca** | 718 | 139 |
| **CardIndex** | 717 | 135 |
| **AgentFS** | 663 | 98 |
| **NGT** | 663 | 153 |
| **knowledge-space** | 547 | 99 |
| **MemNet** | 531 | 140 |
| **mclaude** | 403 | 87 |
| **Rufler** | 378 | 83 |
| **LiteParse** | 336 | 78 |
| **AI Factory** | 287 | 72 |
| **SENTINEL** | 267 | 67 |
| **Wikontic** | 188 | 47 |
| **Firecrawl** | 114 | 20 |
| **agent-memory-mcp** | 101 | 37 |
| **Shield** | 16 | 9 |
| **MCP Tool Search** | 14 | 7 |


### 53. Организации (9)
_Файл: `docs/ENTITIES.md` | 3 колонок, 9 строк_

| Организация | Упоминаний | Файлов |
|---------|------------|--------|
| **Anthropic** | 16770 | 837 |
| **Claude** | 3440 | 700 |
| **Habr** | 2829 | 292 |
| **GitHub** | 1601 | 274 |
| **Хабр** | 626 | 143 |
| **Obsidian** | 234 | 84 |
| **Google** | 85 | 40 |
| **OpenAI** | 81 | 49 |
| **ChatGPT** | 71 | 46 |


### 54. Технологии и стандарты (24)
_Файл: `docs/ENTITIES.md` | 3 колонок, 24 строк_

| Технология | Упоминаний | Файлов |
|---------|------------|--------|
| **RAG** | 2235 | 362 |
| **MCP** | 2163 | 314 |
| **MIT** | 1726 | 344 |
| **LLM** | 1127 | 241 |
| **JSON** | 559 | 125 |
| **Python** | 416 | 138 |
| **REST** | 385 | 149 |
| **CRDT** | 264 | 63 |
| **YAML** | 243 | 103 |
| **Rust** | 160 | 82 |
| **Apache** | 108 | 53 |
| **BSL** | 104 | 45 |
| **SQLite** | 79 | 33 |
| **Mermaid** | 75 | 33 |
| **PostgreSQL** | 50 | 28 |
| **TF-IDF** | 44 | 17 |
| **LangChain** | 31 | 21 |
| **TypeScript** | 27 | 17 |
| **FAISS** | 23 | 14 |
| **WebSocket** | 13 | 10 |
| **FastAPI** | 10 | 6 |
| **JWT** | 8 | 6 |
| **GraphQL** | 6 | 5 |
| **OAuth** | 4 | 3 |


### 55. GitHub репозитории (15)
_Файл: `docs/ENTITIES.md` | 2 колонок, 15 строк_

| Репозиторий | Упоминаний |
|-------------|------------|
| [https://github.com/svend4/nautilus](https://github.com/svend4/nautilus) | 40 |
| [https://github.com/svend4/ingit](https://github.com/svend4/ingit) | 13 |
| [https://github.com/svend4/pro2](https://github.com/svend4/pro2) | 10 |
| [https://github.com/svend4/info1](https://github.com/svend4/info1) | 8 |
| [https://github.com/AnastasiyaW/knowledge-space](https://github.com/AnastasiyaW/knowledge-space) | 7 |
| [https://github.com/svend4/meta](https://github.com/svend4/meta) | 6 |
| [https://github.com/settings/tokens](https://github.com/settings/tokens) | 5 |
| [https://github.com/camel-ai/camel](https://github.com/camel-ai/camel) | 5 |
| [https://github.com/svend4/data70](https://github.com/svend4/data70) | 4 |
| [https://github.com/anthropics/mcp](https://github.com/anthropics/mcp) | 4 |
| [https://github.com/svend4/info7](https://github.com/svend4/info7) | 3 |
| [https://github.com/svend4/info40](https://github.com/svend4/info40) | 3 |
| [https://github.com/kksudo/agentfs](https://github.com/kksudo/agentfs) | 3 |
| [https://github.com/VitalyOborin/yodoca](https://github.com/VitalyOborin/yodoca) | 3 |
| [https://github.com/spbmolot/ngt-memory](https://github.com/spbmolot/ngt-memory) | 3 |


### 56. Ко-встречаемость проектов (топ пары)
_Файл: `docs/ENTITIES.md` | 2 колонок, 20 строк_

| Пара | Общих файлов |
|------|-------------|
| Cowork ↔ ingit | 137 |
| Nautilus ↔ SGB | 123 |
| Svyazi ↔ Yodoca | 123 |
| Nautilus ↔ Cowork | 120 |
| Svyazi ↔ NGT | 117 |
| Svyazi ↔ CardIndex | 116 |
| Nautilus ↔ ingit | 108 |
| Yodoca ↔ NGT | 103 |
| Svyazi ↔ MemNet | 91 |
| Svyazi ↔ AgentFS | 89 |
| Nautilus ↔ MemNet | 85 |
| CardIndex ↔ NGT | 84 |
| Svyazi ↔ knowledge-space | 83 |
| Svyazi ↔ mclaude | 82 |
| Yodoca ↔ CardIndex | 81 |
| AgentFS ↔ NGT | 80 |
| Nautilus ↔ Svyazi | 79 |
| Svyazi ↔ Rufler | 79 |
| Yodoca ↔ AgentFS | 78 |
| CardIndex ↔ AgentFS | 76 |


### 57. Словарь сносок
_Файл: `docs/FOOTNOTES.md` | 3 колонок, 17 строк_

| Термин | Определение | Файлов |
|--------|-------------|--------|
| **AgentFS** | OSS-проект: файловая система для AI-агентов (MIT) | 0 |
| **BSL** | Business Source License — коммерческая лицензия с открытым кодом | 0 |
| **CRDT** | Conflict-free Replicated Data Type — бесконфликтные данные | 0 |
| **CardIndex** | OSS-проект: индекс знаний на карточках (MIT) | 0 |
| **Firecrawl** | Инструмент: веб-краулер для AI (MIT) | 0 |
| **Jaccard** | Коэффициент схожести множеств (0–1) | 0 |
| **LLM** | Large Language Model — большая языковая модель | 0 |
| **MCP** | Model Context Protocol — протокол для AI-инструментов | 0 |
| **NGT** | OSS-проект: ассоциативный граф памяти (BSL 1.1) | 0 |
| **PII** | Personally Identifiable Information — персональные данные | 0 |
| **RAG** | Retrieval-Augmented Generation — генерация с поиском | 0 |
| **Rufler** | OSS-проект: оркестратор AI-агентов | 0 |
| **SENTINEL** | OSS-проект: безопасность и allowlist для MCP | 0 |
| **Svyazi** | Главный проект: экосистема AI-компонентов | 0 |
| **TF-IDF** | Term Frequency–Inverse Document Frequency — метрика важности термина | 0 |
| **Yodoca** | OSS-проект: система памяти с консолидацией (Apache 2.0) | 0 |
| **knowledge-space** | OSS-проект: база знаний 785+ карточек (MIT) | 0 |


### 58. Топ совместных упоминаний
_Файл: `docs/GRAPH.md` | 3 колонок, 25 строк_

| Проект A | Проект B | Файлов вместе |
|----------|----------|---------------|
| **Svyazi** | **Yodoca** | 126 |
| **Svyazi** | **CardIndex** | 122 |
| **Svyazi** | **AgentFS** | 93 |
| **Svyazi** | **MemNet** | 91 |
| **Svyazi** | **knowledge-space** | 88 |
| **Svyazi** | **NGT Memory** | 84 |
| **Svyazi** | **mclaude** | 83 |
| **CardIndex** | **Yodoca** | 81 |
| **Svyazi** | **Rufler** | 79 |
| **AgentFS** | **Yodoca** | 78 |
| **CardIndex** | **AgentFS** | 77 |
| **Svyazi** | **AI Factory** | 75 |
| **Svyazi** | **LiteParse** | 75 |
| **AgentFS** | **knowledge-space** | 73 |
| **Yodoca** | **NGT Memory** | 70 |
| **knowledge-space** | **Yodoca** | 69 |
| **mclaude** | **Yodoca** | 69 |
| **Yodoca** | **MemNet** | 68 |
| **Svyazi** | **SENTINEL** | 65 |
| **Rufler** | **Yodoca** | 65 |
| **CardIndex** | **knowledge-space** | 64 |
| **mclaude** | **AI Factory** | 64 |
| **mclaude** | **Rufler** | 63 |
| **Svyazi** | **Auto AI Router** | 62 |
| **AgentFS** | **LiteParse** | 62 |


### 59. Типы проблем
_Файл: `docs/HEADING_AUDIT.md` | 2 колонок, 7 строк_

| Тип | Кол-во |
|-----|--------|
| ⚠️  Нет родительского H2 | 7 |
| 🕳️  Пустая секция | 1055 |
| ♊ Дублирующийся заголовок | 647 |
| 📏 Длинный заголовок | 4 |
| 🪜 Пропущен уровень | 7 |
| ❌ Нет H1 | 11 |
| ❌ Несколько H1 | 56 |


### 60. Метрики
_Файл: `docs/HEALTH.md` | 4 колонок, 5 строк_

| Метрика | Значение | Статус | Балл |
|---------|----------|--------|------|
| Покрытие текста | 97.6% | 🟢 | 98 |
| Полнота тем | 26✅ 2⚠️ 2❌ | 🟡 | 87 |
| Согласованность | 0 проблем | 🟢 | 100 |
| Внутренние ссылки | 4037 сломано | 🔴 | 0 |
| Дублирование | 0 точных дублей | 🟢 | 100 |


### 61. Структура репозитория
_Файл: `docs/HEALTH.md` | 2 колонок, 18 строк_

| Раздел | Файлов |
|--------|--------|
| 01-svyazi | 16 |
| 02-anthropic-vacancies | 357 |
| 03-technology-combinations | 7 |
| 04-ai-collaborations | 17 |
| 05-habr-projects | 10 |
| ai-collaborations | 30 |
| anthropic-vacancies | 111 |
| autofilled | 13 |
| badges | 1 |
| contacts | 15 |
| glossary | 4 |
| habr-unique-projects | 56 |
| lorenzo-agent | 62 |
| nautilus | 255 |
| root | 98 |
| svyazi-2-0 | 59 |
| technology-combinations | 53 |
| templates | 6 |


### 62. Числовые значения (‰)
_Файл: `docs/HEATMAP.md` | 6 колонок, 12 строк_

| Тема | svyazi | anthropic- | technology | ai-collabo | habr-proje |
|------|------------|------------|------------|------------|------------|
| **Память/Knowledge** | 26.2 | 3.8 | 15.6 | 17.7 | 14.7 |
| **Агент/Оркестр** | 24.1 | 13.1 | 25.9 | 20.4 | 9.0 |
| **Безопасность** | 7.0 | 0.4 | 0.4 | 4.1 | 0.1 |
| **Архитектура** | 5.8 | 5.5 | 3.9 | 3.7 | 1.2 |
| **MVP/Roadmap** | 6.3 | 0.8 | 0.0 | 3.1 | 1.2 |
| **Граф/RAG** | 9.6 | 1.8 | 19.5 | 8.1 | 3.8 |
| **Лицензия/OSS** | 8.0 | 2.4 | 0.0 | 4.3 | 1.0 |
| **Вакансии** | 0.2 | 12.3 | 2.1 | 0.6 | 1.3 |
| **Комбинации** | 2.6 | 0.7 | 20.2 | 1.8 | 2.1 |
| **Habr/Проекты** | 9.1 | 1.7 | 8.1 | 11.8 | 14.8 |
| **Контакты/Команда** | 4.3 | 0.8 | 0.7 | 3.0 | 2.2 |
| **Интеграция/API** | 8.1 | 7.2 | 2.5 | 7.4 | 7.2 |


### 63. Концентрация тем
_Файл: `docs/HEATMAP.md` | 3 колонок, 12 строк_

| Тема | Лучший раздел | Плотность |
|------|--------------|-----------|
| **Память/Knowledge** | `01-svyazi` | 26.2‰ |
| **Агент/Оркестр** | `03-technology-combinations` | 25.9‰ |
| **Безопасность** | `01-svyazi` | 7.0‰ |
| **Архитектура** | `01-svyazi` | 5.8‰ |
| **MVP/Roadmap** | `01-svyazi` | 6.3‰ |
| **Граф/RAG** | `03-technology-combinations` | 19.5‰ |
| **Лицензия/OSS** | `01-svyazi` | 8.0‰ |
| **Вакансии** | `02-anthropic-vacancies` | 12.3‰ |
| **Комбинации** | `03-technology-combinations` | 20.2‰ |
| **Habr/Проекты** | `05-habr-projects` | 14.8‰ |
| **Контакты/Команда** | `01-svyazi` | 4.3‰ |
| **Интеграция/API** | `01-svyazi` | 8.1‰ |


### 64. Метрики репозитория
_Файл: `docs/INDEX.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Markdown документов | **489** |
| Слов | **391,514** |
| Скриптов автоматизации | **78** |
| Go/No-Go скоринг | **96 🟢** |
| Здоровье репо | **75/100** |


### 65. Аналитика и отчёты
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


### 66. Ключевые документы
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


### 67. LLM-обогащение (Ступень 3)
_Файл: `docs/INDEX.md` | 2 колонок, 4 строк_

| Документ | Описание |
|----------|---------|
| `LLM_ENRICHED.md` _(нет)_ | Обогащённые stub-файлы |
| `LLM_QA.md` _(нет)_ | Ответы на открытые вопросы |
| `LLM_GAPS.md` _(нет)_ | Семантические пробелы |
| [`LLM_SUMMARIES.md`](docs/LLM_SUMMARIES.md) | AI-саммари разделов |


### 68. Топ слов по охвату файлов
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


### 69. Топ биграмм (устойчивые словосочетания)
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


### 70. Корпус
_Файл: `docs/KNOWLEDGE_MAP.md` | 2 колонок, 4 строк_

| Параметр | Значение |
|----------|----------|
| Документов | **1161** |
| Слов | **870,981** |
| Секций | **17** |
| RAG-чанков | **2021** (по 7 секциям) |


### 71. Метрики качества
_Файл: `docs/KNOWLEDGE_MAP.md` | 2 колонок, 6 строк_

| Метрика | Значение |
|---------|----------|
| Здоровье репо | 77/100 |
| Средний балл документов | 71.3/100 |
| Словарное богатство (STTR) | 0.674 |
| Пассивный залог | 1.6% |
| Пустых секций | 1445 |
| Противоречий | 5408 |


### 72. По секциям
_Файл: `docs/KNOWLEDGE_MAP.md` | 4 колонок, 17 строк_

| Секция | Файлов | Слов | Ср. слов/файл |
|--------|--------|------|---------------|
| `02-anthropic-vacancies` | 357 | 279,017 | 781 |
| `nautilus` | 255 | 148,523 | 582 |
| `anthropic-vacancies` | 111 | 30,929 | 278 |
| `04-ai-collaborations` | 17 | 26,057 | 1532 |
| `lorenzo-agent` | 62 | 19,979 | 322 |
| `habr-unique-projects` | 56 | 13,161 | 235 |
| `technology-combinations` | 53 | 12,903 | 243 |
| `svyazi-2-0` | 59 | 12,455 | 211 |
| `01-svyazi` | 16 | 10,998 | 687 |
| `05-habr-projects` | 10 | 8,619 | 861 |
| `ai-collaborations` | 30 | 8,207 | 273 |
| `contacts` | 15 | 3,151 | 210 |
| `03-technology-combinations` | 7 | 2,796 | 399 |
| `glossary` | 4 | 2,282 | 570 |
| `templates` | 6 | 635 | 105 |
| `autofilled` | 13 | 533 | 41 |
| `badges` | 1 | 44 | 44 |


### 73. Ключевые концепты
_Файл: `docs/KNOWLEDGE_MAP.md` | 3 колонок, 8 строк_

| Концепт | Файлов | Категория |
|---------|--------|-----------|
| `docs` | 980 | other |
| `anthropic` | 793 | other |
| `claude` | 501 | other |
| `summary` | 485 | other |
| `vacancies` | 476 | other |
| `источник` | 465 | other |
| `mhtml` | 411 | other |
| `снимок` | 400 | other |


### 74. Топ сущностей
_Файл: `docs/KNOWLEDGE_MAP.md` | 3 колонок, 12 строк_

| Сущность | Тип | Файлов |
|----------|-----|--------|
| `anthropic` | 👤 people | 746 |
| `nautilus` | 📦 projects | 463 |
| `claude` | 👤 people | 399 |
| `svyazi` | 📦 projects | 295 |
| `mcp` | ⚙️ tech | 291 |
| `вк` | 🏢 orgs | 261 |
| `github` | 📦 projects | 234 |
| `meta` | 🏢 orgs | 200 |
| `svend4` | 👤 people | 196 |
| `llm` | ⚙️ tech | 188 |
| `api` | ⚙️ tech | 165 |
| `rag` | ⚙️ tech | 148 |


### 75. Количество (203)
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
| **6** | fix run_all missing scripts _59617c5d_ _→ CHANGELOG_ - (6 файлов) _→ CLUSTERS_ - | `ACTION_ITEMS` |
| **30** | стеров: 131 ## Кластер 1 — turn, view, svyazi, cardindex (30 файлов) - `docs/01- | `CLUSTERS` |
| **20** | -executive-summary.md` — _01-executive-summary_ - _...и ещё 20 файлов_ ## Класте | `CLUSTERS` |
| **23** | ted-representation-for-underrepresented-ex, author-contact (23 файлов) - `docs/0 | `CLUSTERS` |
| **13** | ediated-representation-for-underrepresented-ex_ - _...и ещё 13 файлов_ ## Класте | `CLUSTERS` |
| **22** | _ ## Кластер 3 — cowork, ingit, anthropic-vacancies, docs (22 файлов) - `docs/02 | `CLUSTERS` |
| **12** | ositioning.md` — _318-10-strategic-positioning_ - _...и ещё 12 файлов_ ## Класте | `CLUSTERS` |
| **17** | и ещё 12 файлов_ ## Кластер 4 — repo, passport, docs, str (17 файлов) - `docs/02 | `CLUSTERS` |
| **14** | ов_ ## Кластер 5 — principal, agent, professional, agents (14 файлов) - `docs/02 | `CLUSTERS` |
| **4** | md` — _220-9-relationship-to-other-agent-types_ - _...и ещё 4 файлов_ ## Кластер | `CLUSTERS` |
| **3** | ожение-c-образец-спецификаций-инструментов-ing_ - _...и ещё 3 файлов_ ## Кластер | `CLUSTERS` |
| **2** | n_ - `docs/contacts/vladspace.md` — _vladspace_ - _...и ещё 2 файлов_ ## Кластер | `CLUSTERS` |
| _...ещё 183_ | | |


### 76. Количество (203)
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
| **15** | > 🔧 **Подход:** Если избегаете трёхфазного подхода, эти 10-15% теряются безвозвр | `109-3-принципы-консолидац` |
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
| _...ещё 176_ | | |


### 77. Количество (203)
_Файл: `docs/KPI.md` | 3 колонок, 21 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **4–6** | з свободного текста получаются устойчивые профили и связи \| 4–6 дней \| \| Evid | `07-mvp-planning` |
| **1–2** | \| Unified cards + page/span evidence + manual reviewer UI \| 1–2 недели \| Пере | `12-roadmap` |
| **1** | и patch \| benchmark set + nightly eval + rollback policy \| 1 неделя на каркас, | `12-roadmap` |
| **15** | й журнал» в инженерном смысле. Это архив 1105 разговоров за 15 месяцев (dec 2024 | `00-intro` |
| **6** | r-track . Entrepreneur First (Paris, Berlin) — программа на 6 месяцев с €80K сти | `00-intro` |
| **3** | talog.md) как отдельная секция). Потенциал от 1⭐ до 500⭐ за 3 месяца — абсолютно | `00-intro` |
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
| _...ещё 257_ | | |


### 78. Количество (203)
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
| _...ещё 441_ | | |


### 79. Количество (203)
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


### 80. Количество (203)
_Файл: `docs/KPI.md` | 3 колонок, 21 строк_

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
| **5.0.6** | 026` \\\| азработка : версии HMP-0001 → HMP-0005 (март 2026, версия 5.0.6) - Док | `TABLES` |
| **0.10.0** | нтегрируется с любым MCP сервером 118 встроенных навыков в v0.10.0 Open standard | `TABLES` |
| **0.9** | Нет vendor lock-in. 6. Скорость разработки. 1556 commits с v0.9 до v0.11. Это fu | `TABLES` |
| _...ещё 369_ | | |


### 81. Количество (203)
_Файл: `docs/KPI.md` | 3 колонок, 9 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **10** | nts (≈8 репо)](#кластер-4-archives-experiments-8-репо) - [Топ-10 репо, в которые | `00-intro` |
| **5** | sh/git), либо помочь с English README-драфтом для одного из топ-5, либо проработ | `00-intro` |
| **30** | , MemNet --- **Файлов с входящими ссылками:** 504 ## Топ-30 самых цитируемых док | `BACKLINKS` |
| **20** | ь документы](#рекомендуется-создать-документы) - [Детали по топ-20 пробелам](#де | `CONTENT_GAPS` |
| **40** | (#матрица-сходства-секций) - [Граф связей](#граф-связей) - [Топ-40 кросс-секцион | `CROSS_SECTION` |
| **15** | бзор (0 сл., строка 35) ### `WORD_FREQ.md` (1 из 21) - ## Топ-15 слов по раздела | `EMPTY_SECTIONS` |
| **50** | ### [Приоритеты файлов](docs/PRIORITIES.md) > > !TIP - Топ-50 самых важных файло | `OUTLINE` |
| **3** | \| \| \| `improve_similar.py` \| для каждого документа находит топ-3 похожих. \| | `SCRIPTS_CATALOG` |
| **8** | », «достигн», «получен», «вывод») - Ключевые слова (TF-IDF топ-8) **Флаги:** `-- | `SCRIPTS_CATALOG` |


### 82. Количество (203)
_Файл: `docs/KPI.md` | 3 колонок, 6 строк_

| Значение | Контекст | Источник |
|----------|----------|---------|
| **1** | les . Каждая фаза имеет smoke-test: завершена или нет. #### Фаза 1 — Спецификаци | `02-общий-план-развития-na` |
| **2** | адаптер для нового репо без задавания вопросов автору? #### Фаза 2 — Reference i | `02-общий-план-развития-na` |
| **3** | озвращает non-empty результат с consensus-информацией? #### Фаза 3 — MCP интерфе | `02-общий-план-развития-na` |
| **4** | кристалла», получить osmыслený ответ с указанием репо. #### Фаза 4 — Web interfa | `02-общий-план-развития-na` |
| **5** | y через браузер, получить отформатированный результат. #### Фаза 5 — Публикация  | `02-общий-план-развития-na` |
| **0** | ёртывания](#9-стратегия-поэтапного-развёртывания) - [9.1. Фаза 0 — Основание (Ме | `199-9-стратегия-поэтапног` |


### 83. Текущие метрики
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


### 84. Распределение
_Файл: `docs/LANGUAGE_STATS.md` | 2 колонок, 4 строк_

| Язык | Файлов |
|------|--------|
| 🇷🇺 RU (≥80% кириллица) | 98 |
| 🇬🇧 EN (≥80% латиница) | 369 |
| 🔀 MIX | 671 |
| ❓ OTHER | 0 |


### 85. Файлы с неожиданным языком
_Файл: `docs/LANGUAGE_STATS.md` | 5 колонок, 148 строк_

| Файл | Язык | Ожидалось | RU% | EN% |
|------|------|-----------|-----|-----|
| `185-appendix-b-domain-comparison-matrix.md` | EN | RU | 0% | 100% |
| `173-4-ten-domains-of-application.md` | EN | RU | 1% | 99% |
| `171-2-historical-precedents-agents-as-civilizational-i.md` | EN | RU | 2% | 98% |
| `311-3-what-ingit-provides-that-cowork-lacks.md` | EN | RU | 2% | 98% |
| `219-8-pilot-proposal-sgb-advocate-colleague.md` | EN | RU | 2% | 98% |
| `170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` | EN | RU | 2% | 98% |
| `212-1-the-five-type-typology-of-principal-side-agents.md` | EN | RU | 2% | 98% |
| `164-10-appendices.md` | EN | RU | 2% | 98% |
| `215-4-architecture-of-professional-colleague-agents.md` | EN | RU | 2% | 98% |
| `256-3-what-makes-a-composite-skills-agent.md` | EN | RU | 2% | 98% |
| `318-10-strategic-positioning.md` | EN | RU | 2% | 98% |
| `157-3-why-existing-solutions-fail.md` | EN | RU | 2% | 98% |
| `217-6-risks-specific-to-this-category.md` | EN | RU | 2% | 98% |
| `258-5-configuration-how-principals-build-their-ensembl.md` | EN | RU | 2% | 98% |
| `259-6-coordination-and-disagreement-resolution.md` | EN | RU | 2% | 98% |
| `260-7-economics-of-combinatorial-replication.md` | EN | RU | 2% | 98% |
| `261-8-seven-domains-of-application.md` | EN | RU | 2% | 98% |
| `280-the-specific-case-in-front-of-us.md` | EN | RU | 2% | 98% |
| `309-1-the-cowork-discovery-and-why-it-changes-everythi.md` | EN | RU | 2% | 98% |
| `177-8-risks-and-mitigations.md` | EN | RU | 2% | 98% |
| `254-1-why-the-binary-view-is-incomplete.md` | EN | RU | 2% | 98% |
| `313-5-four-integration-paths-in-order-of-accessibility.md` | EN | RU | 2% | 98% |
| `213-2-what-makes-a-professional-colleague-agent.md` | EN | RU | 2% | 98% |
| `216-5-the-economics-of-profession-wide-replication.md` | EN | RU | 2% | 98% |
| `174-5-architectural-specification.md` | EN | RU | 2% | 98% |
| `255-2-the-twenty-one-teachers-pattern.md` | EN | RU | 2% | 98% |
| `156-2-target-populations.md` | EN | RU | 2% | 98% |
| `160-6-governance-and-ethics.md` | EN | RU | 2% | 98% |
| `161-7-phased-rollout-plan.md` | EN | RU | 2% | 98% |
| `172-3-what-makes-a-representative-agent.md` | EN | RU | 2% | 98% |
| `178-9-phased-rollout-strategy.md` | EN | RU | 2% | 98% |
| `220-9-relationship-to-other-agent-types.md` | EN | RU | 2% | 98% |
| `257-4-the-sub-agent-registry.md` | EN | RU | 2% | 98% |
| `277-what-s-missing-layer-b.md` | EN | RU | 2% | 98% |
| `263-10-risks-specific-to-composite-architectures.md` | EN | RU | 3% | 97% |
| `262-9-integration-with-okwf-infrastructure.md` | EN | RU | 3% | 97% |
| `310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | EN | RU | 3% | 97% |
| `138-1-why-single-triangle-models-are-incomplete.md` | EN | RU | 3% | 97% |
| `163-9-call-for-partnership.md` | EN | RU | 3% | 97% |
| `184-appendix-a-connection-to-companion-papers.md` | EN | RU | 3% | 97% |
| `265-12-call-for-collaboration.md` | EN | RU | 3% | 97% |
| `315-7-practical-first-steps-this-month.md` | EN | RU | 3% | 97% |
| `316-8-implications-for-nautilus-and-okwf.md` | EN | RU | 3% | 97% |
| `141-4-nautilus-portal-as-reference-substrate.md` | EN | RU | 3% | 97% |
| `155-1-problem-statement.md` | EN | RU | 3% | 97% |
| `266-13-closing.md` | EN | RU | 3% | 97% |
| `312-4-the-symbiotic-architecture.md` | EN | RU | 3% | 97% |
| `68-about.md` | EN | RU | 3% | 97% |
| `143-6-four-deployment-domains.md` | EN | RU | 3% | 97% |
| `176-7-governance-and-oversight.md` | EN | RU | 3% | 97% |
| `180-11-call-for-collaboration.md` | EN | RU | 3% | 97% |
| `221-10-open-questions.md` | EN | RU | 3% | 97% |
| `274-the-missing-middle-layer-between-chat-and-code.md` | EN | RU | 3% | 97% |
| `145-8-call-to-action.md` | EN | RU | 3% | 97% |
| `162-8-risk-analysis.md` | EN | RU | 3% | 97% |
| `179-10-open-questions.md` | EN | RU | 3% | 97% |
| `264-11-open-questions.md` | EN | RU | 3% | 97% |
| `268-references.md` | EN | RU | 3% | 97% |
| `286-acknowledgments.md` | EN | RU | 3% | 97% |
| `README.md` | EN | RU | 3% | 97% |
| `142-5-pattern-library-as-bridge-between-triangles.md` | EN | RU | 3% | 97% |
| `279-existing-approximations.md` | EN | RU | 3% | 97% |
| `158-4-proposed-infrastructure.md` | EN | RU | 3% | 97% |
| `214-3-empirical-case-study-обучай.md` | EN | RU | 3% | 97% |
| `278-why-this-hasn-t-been-built.md` | EN | RU | 3% | 97% |
| `281-the-recursive-insight.md` | EN | RU | 3% | 97% |
| `144-7-open-questions.md` | EN | RU | 3% | 97% |
| `284-practical-recommendations-for-the-current-project.md` | EN | RU | 3% | 97% |
| `140-3-three-inter-layer-protocols.md` | EN | RU | 4% | 96% |
| `222-11-call-for-collaboration.md` | EN | RU | 4% | 96% |
| `227-appendix-b-decision-framework-when-to-build-type-1.md` | EN | RU | 4% | 96% |
| `317-9-risks-and-open-questions.md` | EN | RU | 4% | 96% |
| `167-ai-mediated-representation-for-underrepresented-ex.md` | EN | RU | 4% | 96% |
| `209-a-typology-of-ai-agents-on-the-principal-side-and-.md` | EN | RU | 4% | 96% |
| `252-abstract.md` | EN | RU | 4% | 96% |
| `282-what-industry-will-likely-build.md` | EN | RU | 4% | 96% |
| `283-what-this-document-doesn-t-solve.md` | EN | RU | 4% | 96% |
| `218-7-application-domains.md` | EN | RU | 4% | 96% |
| `251-ai-support-through-configurable-specialist-ensembl.md` | EN | RU | 4% | 96% |
| `136-abstract.md` | EN | RU | 4% | 96% |
| `275-why-this-document-exists.md` | EN | RU | 4% | 96% |
| `168-abstract.md` | EN | RU | 4% | 96% |
| `226-appendix-a-comparative-table-five-agent-types.md` | EN | RU | 4% | 96% |
| `267-acknowledgments.md` | EN | RU | 4% | 96% |
| `307-abstract.md` | EN | RU | 4% | 96% |
| `306-with-anthropic-s-cowork-platform.md` | EN | RU | 4% | 96% |
| `210-abstract.md` | EN | RU | 4% | 96% |
| `135-a-formal-model-for-human-ai-collaboration-in-distr.md` | EN | RU | 4% | 96% |
| `223-12-closing.md` | EN | RU | 4% | 96% |
| `285-closing.md` | EN | RU | 4% | 96% |
| `137-table-of-contents.md` | EN | RU | 4% | 96% |
| `153-executive-summary.md` | EN | RU | 4% | 96% |
| `159-5-economic-model.md` | EN | RU | 4% | 96% |
| `314-6-refined-ingit-scope-with-cowork-in-mind.md` | EN | RU | 4% | 96% |
| `README.md` | EN | RU | 5% | 95% |
| `152-ai-coordinated-infrastructure-for-distributed-expe.md` | EN | RU | 5% | 95% |
| `276-the-two-layer-stack-as-it-exists.md` | EN | RU | 5% | 95% |
| `147-references.md` | EN | RU | 5% | 95% |
| `175-6-ethical-framework.md` | EN | RU | 5% | 95% |
| `211-table-of-contents.md` | EN | RU | 5% | 95% |
| `308-table-of-contents.md` | EN | RU | 5% | 95% |
| `03-portal-protocol-md.md` | EN | RU | 5% | 95% |
| `224-acknowledgments.md` | EN | RU | 5% | 95% |
| `253-table-of-contents.md` | EN | RU | 5% | 95% |
| `181-12-closing.md` | EN | RU | 5% | 95% |
| `319-acknowledgments.md` | EN | RU | 5% | 95% |
| `321-appendix-a-decision-tree-for-ingit-adopters.md` | EN | RU | 5% | 95% |
| `146-acknowledgments.md` | EN | RU | 5% | 95% |
| `269-appendix-a-the-six-type-taxonomy-updated.md` | EN | RU | 5% | 95% |
| `271-appendix-c-configuration-template-example.md` | EN | RU | 5% | 95% |
| `28-appendix-a-minimal-working-example.md` | EN | RU | 5% | 95% |
| `169-table-of-contents.md` | EN | RU | 5% | 95% |
| `270-appendix-b-sub-agent-registry-schema-sketch.md` | EN | RU | 5% | 95% |
| `154-table-of-contents.md` | EN | RU | 6% | 94% |
| `103-appendix-b-change-log.md` | EN | RU | 6% | 94% |
| `273-infrastructure-for-ai-collaborative-intellectual-w.md` | EN | RU | 6% | 94% |
| `322-appendix-b-comparison-matrix.md` | EN | RU | 6% | 94% |
| `139-2-the-double-triangle-architecture.md` | EN | RU | 6% | 94% |
| `183-references.md` | EN | RU | 6% | 94% |
| `304-ingit-as-cowork-native-workspace-substrate-md.md` | EN | RU | 6% | 94% |
| `287-references.md` | EN | RU | 6% | 94% |
| `182-acknowledgments.md` | EN | RU | 7% | 93% |
| `359-твои-anti-patterns.md` | EN | RU | 7% | 93% |
| `148-appendix-a-glossary.md` | EN | RU | 8% | 92% |
| `151-open-knowledge-work-foundation-md.md` | EN | RU | 8% | 92% |
| `208-professional-colleague-agents-md.md` | EN | RU | 8% | 92% |
| `320-references.md` | EN | RU | 10% | 90% |
| `73-portal-protocol-md-v1-1.md` | EN | RU | 11% | 89% |
| `149-appendix-b-summary-of-contributions.md` | EN | RU | 11% | 89% |
| `62-author-contact.md` | EN | RU | 12% | 88% |
| `305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | EN | RU | 12% | 88% |
| `355-существующие-документы-dhlab-твой-context.md` | EN | RU | 12% | 88% |
| `225-references.md` | EN | RU | 13% | 87% |
| `04-sozialrecht-domain.md` | EN | RU | 14% | 86% |
| `42-author-contact.md` | EN | RU | 14% | 86% |
| `98-appendix-a-minimal-working-example.md` | EN | RU | 15% | 85% |
| `249-composite-skills-agent-md.md` | EN | RU | 17% | 83% |
| `89-14-sdk-contract-informative.md` | EN | RU | 16% | 83% |
| `22-10-queryresult-structure.md` | EN | RU | 18% | 82% |
| `13-angle-perspective.md` | EN | RU | 18% | 82% |
| `61-compatibility-level.md` | EN | RU | 18% | 82% |
| `README.md` | EN | RU | 18% | 82% |
| `52-author-contact.md` | EN | RU | 18% | 82% |
| `24-12-versioning-policy.md` | EN | RU | 19% | 81% |
| `344-системный-промпт-для-lorenzo-project.md` | EN | RU | 19% | 81% |
| `41-compatibility-level.md` | EN | RU | 19% | 81% |
| `187-слой-представительских-агентов-md.md` | EN | RU | 20% | 80% |
| `51-compatibility-level.md` | EN | RU | 20% | 80% |


### 86. Смешанные файлы (MIX)
_Файл: `docs/LANGUAGE_STATS.md` | 3 колонок, 671 строк_

| Файл | RU% | EN% |
|------|-----|-----|
| `05-priblizheniya.md` | 80% | 20% |
| `04-simbioticheskaya-arkhitektura.md` | 80% | 20% |
| `02-q2-whom-lorenzo-serves.md` | 20% | 80% |
| `10-strategicheskoe-pozitsionirovanie.md` | 80% | 20% |
| `109-3-принципы-консолидации-фаза-c.md` | 79% | 21% |
| `297-что-промышленность-вероятно-построит.md` | 79% | 21% |
| `336-10-стратегическое-позиционирование.md` | 79% | 21% |
| `04-event-sourcing-consensus.md` | 21% | 79% |
| `329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` | 79% | 21% |
| `SCHEDULE.md` | 79% | 21% |
| `00-question-innovations-transitions.md` | 79% | 21% |
| `00-question-voiceless.md` | 79% | 21% |
| `03-chto-ingit-obespechivaet.md` | 79% | 21% |
| `25-13-reference-implementation.md` | 21% | 79% |
| `294-существующие-приближения.md` | 79% | 21% |
| `07-q7-success-metrics.md` | 21% | 79% |
| `03-dsl-ast.md` | 21% | 79% |
| `132-planned-v0-2-0.md` | 21% | 79% |
| `README.md` | 22% | 78% |
| `19-multi-agent-observability-platform.md` | 22% | 78% |
| `244-благодарности.md` | 78% | 22% |
| `121-appendix-c-история-изменений-методологии.md` | 78% | 22% |
| `07-rekursivnoe-prozrenie.md` | 78% | 22% |
| `09-riski-voprosy.md` | 78% | 22% |
| `02-what-info-repos-contain.md` | 22% | 78% |
| `QA.md` | 78% | 22% |
| `03-q3-what-lorenzo-does.md` | 22% | 78% |
| `02-chto-cowork-obespechivaet.md` | 78% | 22% |
| `01-zachem-dokument.md` | 78% | 22% |
| `05-chetyre-puti-integratsii.md` | 78% | 22% |
| `186-appendix-c-sample-use-cases-in-detail.md` | 22% | 78% |
| `10-collaborators-landscape.md` | 22% | 78% |
| `342-что-такое-вариант-c-concept-document-для-anthropic.md` | 22% | 78% |
| `119-appendix-b-примеры-расхождений-и-их-разрешения.md` | 77% | 23% |
| `354-существующий-landscape-collaborators-твоя-working-.md` | 23% | 77% |
| `72-расписание-фазы-3.md` | 77% | 23% |
| `35-passports-info1-md.md` | 23% | 77% |
| `01-context-motivation.md` | 77% | 23% |
| `graph-rag.md` | 23% | 77% |
| `AUTHORS.md` | 23% | 77% |
| `07-prakticheskie-shagi.md` | 77% | 23% |
| `24-mega-integration-full-stack.md` | 23% | 77% |
| `01-three-key-candidates.md` | 77% | 23% |
| `01-интегральный-анализ-профиля-svend4.md` | 77% | 23% |
| `yodoca.md` | 23% | 77% |
| `15-anti-patterns.md` | 24% | 76% |
| `10-rekomendatsii.md` | 76% | 24% |
| `05-0-status-of-this-document.md` | 24% | 76% |
| `05-q5-authority-limits.md` | 24% | 76% |
| `03-consolidation-principles.md` | 76% | 24% |
| `203-благодарности.md` | 76% | 24% |
| `93-18-reference-implementation.md` | 24% | 76% |
| `08-q8-other-ai-relationships.md` | 24% | 76% |
| `ENTITIES.md` | 24% | 76% |
| `02-nautilus-A-pro2-meta.md` | 76% | 24% |
| `328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` | 76% | 24% |
| `166-representative-agent-layer-md.md` | 24% | 76% |
| `QA.md` | 76% | 24% |
| `323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` | 24% | 76% |
| `343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` | 76% | 24% |
| `337-благодарности.md` | 75% | 25% |
| `00-question-two-nautiluses.md` | 75% | 25% |
| `7-metaphor.md` | 75% | 25% |
| `14-local-first-agent-development-environment.md` | 25% | 75% |
| `02-collaboration-partners.md` | 75% | 25% |
| `09-product-management-support-ops.md` | 25% | 75% |
| `01-three-direct-analogues.md` | 75% | 25% |
| `README.md` | 25% | 75% |
| `00-context.md` | 25% | 75% |
| `01-why-stronger-than-it-looks.md` | 75% | 25% |
| `00-question-habr-examples.md` | 74% | 26% |
| `05-what-to-do-right-now.md` | 26% | 74% |
| `134-the-double-triangle-architecture-md.md` | 26% | 74% |
| `325-аннотация.md` | 74% | 26% |
| `READABILITY.md` | 26% | 74% |
| `334-8-импликации-для-nautilus-и-okwf.md` | 74% | 26% |
| `115-8-ограничения-и-открытые-вопросы.md` | 74% | 26% |
| `31-content-overview.md` | 26% | 74% |
| `09-minuses-and-risks.md` | 74% | 26% |
| `96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | 26% | 74% |
| `READING_TIME.md` | 26% | 74% |
| `00-question-practical.md` | 74% | 26% |
| `16-mcp-extension.md` | 26% | 74% |
| `concepts.md` | 26% | 74% |
| `README.md` | 74% | 26% |
| `13-reprioritization.md` | 26% | 74% |
| `overview.md` | 26% | 74% |
| `yjs-automerge.md` | 26% | 74% |
| `decision-record.md` | 74% | 26% |
| `security-routing-plane.md` | 27% | 73% |
| `45-passports-pro2-md.md` | 27% | 73% |
| `55-passports-meta-md.md` | 27% | 73% |
| `LINKS.md` | 27% | 73% |
| `88-13-rest-api-contract-normative-for-portals.md` | 27% | 73% |
| `02-minuses-1-10.md` | 26% | 73% |
| `08-promyshlennost-postroit.md` | 73% | 27% |
| `324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | 73% | 27% |
| `DUPLICATES.md` | 27% | 73% |
| `09-federated-platform.md` | 27% | 73% |
| `ai-factory.md` | 27% | 73% |
| `01-shell-metaphor-two-projections.md` | 73% | 27% |
| `memnet.md` | 27% | 73% |
| `research-docs-liteparse.md` | 27% | 73% |
| `231-содержание.md` | 73% | 26% |
| `65-readme-md.md` | 27% | 73% |
| `6-metaphor.md` | 73% | 27% |
| `09-ne-reshaet.md` | 73% | 27% |
| `289-инфраструктура-для-ai-совместной-интеллектуальной-.md` | 73% | 27% |
| `60-bridges.md` | 27% | 73% |
| `MISSING.md` | 27% | 73% |
| `57-native-format.md` | 28% | 72% |
| `QUESTIONS.md` | 72% | 28% |
| `00-question-agent-changes-reality.md` | 72% | 28% |
| `00-question-can-it-apply-to-docs.md` | 72% | 28% |
| `17-appendix-b-change-log.md` | 28% | 72% |
| `362-когда-сомневаешься-escalate-к-max.md` | 28% | 72% |
| `reading-paths.md` | 28% | 72% |
| `91-16-mcp-extension-informative.md` | 28% | 72% |
| `92-17-versioning-policy.md` | 28% | 72% |
| `NARRATIVE.md` | 72% | 28% |
| `08-implikatsii-nautilus-okwf.md` | 72% | 28% |
| `21-9-query-flow.md` | 28% | 72% |
| `14-public-policy.md` | 28% | 72% |
| `agent-memory-mcp.md` | 28% | 72% |
| `245-ссылки.md` | 72% | 28% |
| `SEE_ALSO.md` | 28% | 72% |
| `rufler.md` | 28% | 72% |
| `08-safeguards-trust-safety.md` | 28% | 72% |
| `05-existing-infrastructure-stack.md` | 28% | 72% |
| `01-executive-summary.md` | 71% | 29% |
| `205-приложение-a-связь-с-сопроводительными-статьями.md` | 71% | 29% |
| `self-aware-mcp.md` | 29% | 71% |
| `123-portal-mcp-py.md` | 29% | 71% |
| `06-utochnyonnyy-obyom-ingit.md` | 71% | 29% |
| `ensemble.md` | 71% | 29% |
| `331-5-четыре-пути-интеграции-в-порядке-доступности.md` | 71% | 29% |
| `86-11-relevance-ranking.md` | 29% | 71% |
| `KPI_HISTORY.md` | 71% | 29% |
| `SIMILAR.md` | 29% | 71% |
| `SIMILAR_PASSAGES.md` | 71% | 29% |
| `06-engineering-design-product.md` | 29% | 71% |
| `READING_ORDER.md` | 29% | 71% |
| `10-architecture-rfc.md` | 29% | 71% |
| `90-15-security-considerations.md` | 29% | 71% |
| `03-why-natural-for-programmers.md` | 71% | 29% |
| `11-dhlab-documents.md` | 29% | 71% |
| `48-content-overview.md` | 29% | 71% |
| `NETWORK.md` | 29% | 71% |
| `ngt-memory.md` | 71% | 29% |
| `01-ai-research-engineering.md` | 29% | 71% |
| `12-technical-program-management.md` | 29% | 71% |
| `13-communications.md` | 29% | 71% |
| `COVERAGE.md` | 29% | 71% |
| `11-zaklyuchenie.md` | 71% | 29% |
| `review-record.md` | 29% | 71% |
| `01-search-results-not-found.md` | 30% | 70% |
| `09-limitations-open-questions.md` | 70% | 30% |
| `71-критерии-выбора-для-фазы-3.md` | 70% | 30% |
| `ALERTS.md` | 70% | 30% |
| `voice-stack.md` | 30% | 70% |
| `09-4-passport-passport-md.md` | 30% | 70% |
| `105-review-methodology-md.md` | 30% | 70% |
| `351-что-ты-можешь-делать.md` | 30% | 70% |
| `64-for-the-curious-philosophy.md` | 70% | 30% |
| `94-19-adr-001-federation-over-merging.md` | 30% | 70% |
| `06-final-tier-ranking.md` | 30% | 70% |
| `RISK_REGISTER.md` | 70% | 30% |
| `27-15-glossary-of-examples.md` | 30% | 70% |
| `03-nautilus-B-meta-orchestrator.md` | 70% | 30% |
| `integration-spec.md` | 30% | 70% |
| `116-9-checklist-применения-методологии.md` | 70% | 30% |
| `01-introduction.md` | 70% | 30% |
| `125-readme-mcp-md-инструкция-по-установке.md` | 30% | 70% |
| `05-marketing-brand.md` | 30% | 70% |
| `02-related-projects.md` | 70% | 30% |
| `00-intro.md` | 70% | 30% |
| `TABLES.md` | 30% | 70% |
| `01-shared-memory-between-agents.md` | 70% | 30% |
| `75-0-status-of-this-document.md` | 30% | 70% |
| `15-public-benefit.md` | 30% | 70% |
| `111-4-условия-применимости.md` | 69% | 31% |
| `02-методика-и-рамка-отбора.md` | 69% | 31% |
| `09-agent-orchestration-stack.md` | 31% | 69% |
| `26-14-adr-001-federation-over-merging.md` | 31% | 69% |
| `332-6-уточнённый-объём-ingit-с-учётом-cowork.md` | 69% | 31% |
| `6-bonus-rram-memristor.md` | 69% | 31% |
| `30-mega-stack-3-0-with-dsl-ast.md` | 31% | 69% |
| `memnet.md` | 69% | 31% |
| `SPELLCHECK.md` | 31% | 69% |
| `12-workflow.md` | 31% | 69% |
| `00-question-multi-tier.md` | 69% | 31% |
| `85-10-query-flow.md` | 31% | 69% |
| `06-angel-vs-demon-duality.md` | 69% | 31% |
| `11-concrete-potential-collaborator.md` | 30% | 69% |
| `05-anchor-node-habr-scout.md` | 30% | 69% |
| `01-legal-ai-stack.md` | 31% | 69% |
| `07-specialized-knowledge-workspace.md` | 31% | 69% |
| `97-22-glossary-of-reference-examples.md` | 31% | 69% |
| `13-rest-api.md` | 32% | 68% |
| `128-доступные-инструменты.md` | 32% | 68% |
| `14-sdk.md` | 31% | 68% |
| `302-ссылки.md` | 68% | 32% |
| `01-claude-response.md` | 68% | 32% |
| `03-synthesis-hebbian-collaboration-graph.md` | 68% | 32% |
| `02-sales.md` | 32% | 68% |
| `research-summary.md` | 68% | 32% |
| `00-question-anonymization.md` | 68% | 32% |
| `methodology.md` | 68% | 32% |
| `358-твоя-relationship-с-другими-ai.md` | 32% | 68% |
| `02-four-structural-blockers.md` | 68% | 32% |
| `16-glossary.md` | 68% | 32% |
| `10-compute.md` | 32% | 68% |
| `00-question-camel-vs-nautilus.md` | 67% | 33% |
| `00-question-scenario.md` | 67% | 33% |
| `04-security.md` | 33% | 67% |
| `10-query-result.md` | 33% | 67% |
| `79-4-passport-passport-md.md` | 33% | 67% |
| `08-difference-3-federation-missing.md` | 33% | 67% |
| `01-response.md` | 67% | 33% |
| `13-contacts.md` | 67% | 33% |
| `agentfs.md` | 33% | 67% |
| `legal-rag.md` | 33% | 67% |
| `message-template.md` | 67% | 33% |
| `106-tl-dr.md` | 67% | 33% |
| `82-7-portalentry-structure.md` | 33% | 67% |
| `09-difference-4-institutional-vision.md` | 33% | 67% |
| `00-context-fundamental-questions.md` | 33% | 67% |
| `02-общий-план-развития-nautilus-portal-protocol.md` | 66% | 33% |
| `02-existing-niche.md` | 66% | 34% |
| `08-personal-multi-agent-hub.md` | 34% | 66% |
| `05-minuses-as-business.md` | 66% | 33% |
| `01-three-archetypes.md` | 66% | 34% |
| `01-yodoca.md` | 66% | 34% |
| `347-твоя-миссия.md` | 66% | 34% |
| `10-checklist.md` | 66% | 34% |
| `7-autoresearch-distributed.md` | 66% | 34% |
| `20-experiment.md` | 34% | 66% |
| `ngt-memory.md` | 34% | 66% |
| `95-20-adr-002-q6-as-first-class-protocol-concept.md` | 34% | 66% |
| `13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 66% | 34% |
| `01-response.md` | 34% | 66% |
| `01-synthesis.md` | 66% | 34% |
| `12-minuses-of-hermes.md` | 34% | 66% |
| `23-11-security-considerations.md` | 34% | 66% |
| `QA.md` | 66% | 34% |
| `13-appendix-b-examples.md` | 66% | 34% |
| `122-глоссарий.md` | 66% | 34% |
| `DECISIONS.md` | 66% | 34% |
| `02-related-projects-context.md` | 66% | 34% |
| `mclaude.md` | 34% | 66% |
| `03-component-catalog.md` | 34% | 66% |
| `CONCEPT_GRAPH.md` | 35% | 65% |
| `01-completing-loop.md` | 35% | 65% |
| `README.md` | 65% | 35% |
| `03-карта-найденных-проектов-и-паттернов.md` | 35% | 65% |
| `DIGEST.md` | 35% | 65% |
| `12-versioning-policy.md` | 35% | 65% |
| `01-what-to-anonymize-german-standard.md` | 65% | 35% |
| `COMPLEXITY.md` | 65% | 35% |
| `knowledge-space.md` | 35% | 65% |
| `CONCEPTS.md` | 35% | 65% |
| `11-legal.md` | 35% | 65% |
| `04-mem0-letta-graphiti.md` | 35% | 65% |
| `14-other-ai-relationships.md` | 35% | 65% |
| `narrow-questions.md` | 65% | 35% |
| `356-твой-workflow.md` | 35% | 65% |
| `84-9-consensus-algorithm.md` | 35% | 65% |
| `STALENESS.md` | 35% | 65% |
| `04-similarity-4-multi-platform.md` | 35% | 65% |
| `04-dochkina-sequential.md` | 65% | 35% |
| `15-security.md` | 35% | 65% |
| `00-question-lorenzo-codename.md` | 64% | 36% |
| `04-recommendations.md` | 35% | 64% |
| `README.md` | 36% | 64% |
| `COMPONENT_MATRIX.md` | 36% | 64% |
| `03-three-variants-A-B-C.md` | 64% | 36% |
| `11-pluses-of-hermes.md` | 36% | 64% |
| `03-pda-llm-as-periphery.md` | 64% | 36% |
| `12-roadmap.md` | 64% | 36% |
| `229-профессиональные-коллеги-агенты.md` | 64% | 36% |
| `SUMMARIES.md` | 35% | 64% |
| `11-glossary.md` | 35% | 64% |
| `18-reference-implementation.md` | 36% | 64% |
| `hybrid-rag.md` | 36% | 64% |
| `07-software-engineering-infrastructure.md` | 36% | 64% |
| `05-supplementary-infrastructure.md` | 64% | 36% |
| `18-comment-on-document.md` | 64% | 36% |
| `07-difference-2-domain-specialization.md` | 36% | 64% |
| `10-difference-5-tool-vs-mission-drift.md` | 36% | 64% |
| `12-дорожная-карта-прототипа-следующей-итерации.md` | 64% | 36% |
| `TIMELINE.md` | 36% | 64% |
| `288-appendix-position-in-series-visualization.md` | 36% | 64% |
| `projects-map.md` | 36% | 64% |
| `BROKEN_LINKS.md` | 36% | 64% |
| `13-reference-implementation.md` | 36% | 64% |
| `02-final-ranking.md` | 63% | 37% |
| `21-adr-003-five-onboarding-paths.md` | 37% | 63% |
| `80-5-compatibility-levels.md` | 37% | 63% |
| `02-similarity-2-persistent-memory.md` | 37% | 63% |
| `06-level-5-full-network.md` | 37% | 63% |
| `continuation-intro.md` | 63% | 37% |
| `TECH_RADAR.md` | 63% | 37% |
| `127-подключение-к-claude-desktop.md` | 37% | 63% |
| `204-ссылки.md` | 63% | 37% |
| `78-3-registry-nautilus-json.md` | 37% | 63% |
| `05-level-4-extended-mature.md` | 37% | 63% |
| `00-question-habr-link.md` | 37% | 63% |
| `117-10-конкретный-план-применения-к-текущим-документам.md` | 63% | 37% |
| `16-people.md` | 37% | 63% |
| `00-tldr.md` | 63% | 37% |
| `2-document-rag.md` | 63% | 37% |
| `44-for-the-curious-philosophy.md` | 37% | 63% |
| `CODE_BLOCKS.md` | 37% | 63% |
| `04-what-to-do.md` | 63% | 37% |
| `08-pluses-of-model.md` | 63% | 37% |
| `04-q4-character.md` | 37% | 63% |
| `365-развёрнутый-анализ-внуковой-комбинации.md` | 37% | 63% |
| `53-history.md` | 37% | 63% |
| `01-existing-landscape.md` | 63% | 37% |
| `14-limitations.md` | 62% | 38% |
| `38-content-overview.md` | 62% | 38% |
| `16-history.md` | 62% | 38% |
| `6-tmux-village-openclaw.md` | 62% | 38% |
| `00-question-habr-2.md` | 62% | 38% |
| `sozialrecht-35-combinations.md` | 38% | 62% |
| `10-second-order-ensembles.md` | 62% | 38% |
| `20-8-consensus-algorithm.md` | 38% | 62% |
| `360-что-ты-всегда-делаешь.md` | 38% | 62% |
| `40-bridges.md` | 38% | 62% |
| `81-6-adapter-interface.md` | 38% | 62% |
| `METRICS.md` | 38% | 62% |
| `01-passive-vs-active-roles.md` | 38% | 62% |
| `03-honest-opinion.md` | 37% | 62% |
| `15-glossary.md` | 38% | 62% |
| `PASSIVE_VOICE.md` | 62% | 38% |
| `README.md` | 38% | 62% |
| `05-conditions-of-applicability.md` | 62% | 38% |
| `do-not-glue.md` | 62% | 38% |
| `352-что-ты-не-можешь-делать-без-max-approval.md` | 38% | 62% |
| `COMPARE.md` | 38% | 62% |
| `03-finance.md` | 38% | 62% |
| `autoresearch-sequential.md` | 38% | 62% |
| `1-agentic-knowledge-os.md` | 62% | 38% |
| `05-quaternary-developer-education.md` | 38% | 62% |
| `07-chto-mozhesh.md` | 38% | 62% |
| `continuation-10-domains.md` | 38% | 62% |
| `02-vitaly-graph-cognitive-memory.md` | 61% | 39% |
| `12-content-overview.md` | 61% | 39% |
| `18-6-adapter-interface.md` | 39% | 61% |
| `01-level-0-manual.md` | 61% | 39% |
| `roadmap.md` | 61% | 39% |
| `348-кому-ты-служишь-слоистая-модель.md` | 61% | 39% |
| `19-adr-001-federation-over-merging.md` | 39% | 61% |
| `04-fallback-ratio-question.md` | 61% | 39% |
| `06-1-introduction.md` | 61% | 39% |
| `08-3-registry-nautilus-json.md` | 39% | 61% |
| `345-кто-ты.md` | 39% | 61% |
| `source-projects.md` | 39% | 61% |
| `1-neuromorphic-ssm.md` | 61% | 39% |
| `project-component.md` | 61% | 39% |
| `120-главные-технические-риски.md` | 61% | 39% |
| `4-skill-catalogs-subagents.md` | 61% | 39% |
| `18-escalate-to-max.md` | 39% | 61% |
| `108-2-формальный-workflow.md` | 61% | 38% |
| `50-bridges.md` | 39% | 61% |
| `INDEX.md` | 39% | 61% |
| `02-memnet.md` | 61% | 39% |
| `00-intro.md` | 61% | 39% |
| `34-appendix-b-change-log.md` | 61% | 39% |
| `REPORT.md` | 61% | 39% |
| `05-similarity-5-self-hosting-privacy.md` | 39% | 61% |
| `09-query-flow.md` | 40% | 60% |
| `CROSS_SECTION.md` | 60% | 40% |
| `10-profession-specific-workflows.md` | 40% | 60% |
| `14-adr-001-federation-over-merging.md` | 40% | 60% |
| `DEPENDABOT.md` | 40% | 60% |
| `02-primary-fde.md` | 60% | 40% |
| `evidence-envelope.md` | 40% | 60% |
| `COST.md` | 60% | 40% |
| `06-conclusion-deserves-attention.md` | 39% | 60% |
| `01-introduction.md` | 60% | 40% |
| `07-portal-entry.md` | 40% | 60% |
| `15-appendix-c-history.md` | 40% | 60% |
| `01-pluses-1-7.md` | 39% | 60% |
| `190-содержание.md` | 60% | 40% |
| `228-appendix-c-quick-start-architecture-for-sgb-advoca.md` | 40% | 60% |
| `03-tvoya-missiya.md` | 60% | 40% |
| `112-5-связь-с-существующими-методологиями.md` | 60% | 40% |
| `340-приложение-b-сравнительная-матрица.md` | 60% | 40% |
| `KPI.md` | 60% | 40% |
| `WORD_FREQ.md` | 40% | 60% |
| `04-claude-subagents-patterns.md` | 40% | 60% |
| `10-новые-ансамбли-следующего-шага.md` | 60% | 40% |
| `VALIDATION.md` | 40% | 60% |
| `17-versioning-policy.md` | 40% | 60% |
| `16-vsegda-delaesh.md` | 40% | 60% |
| `10-query-flow.md` | 40% | 60% |
| `11-relevance-ranking.md` | 40% | 60% |
| `129-примеры-запросов-в-claude.md` | 40% | 60% |
| `130-отладка.md` | 40% | 60% |
| `165-closing.md` | 60% | 40% |
| `00-overview-grandchild-combination.md` | 60% | 40% |
| `README.md` | 60% | 40% |
| `01-response.md` | 60% | 40% |
| `00-abstract-status.md` | 60% | 40% |
| `F-evidence-backed-intake.md` | 60% | 40% |
| `SEARCH_RESULTS.md` | 40% | 60% |
| `E-execution-plane.md` | 40% | 60% |
| `budget-routing.md` | 60% | 40% |
| `11-security-considerations.md` | 41% | 59% |
| `01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md` | 59% | 40% |
| `06-security-privacy.md` | 59% | 41% |
| `113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 59% | 40% |
| `DENSITY.md` | 41% | 59% |
| `3-forensic-rag.md` | 59% | 41% |
| `2-autoresearch-legal.md` | 59% | 41% |
| `01-coally.md` | 59% | 41% |
| `03-what-this-gives-technically.md` | 59% | 40% |
| `01-profile-five-layers.md` | 59% | 41% |
| `69-section.md` | 59% | 41% |
| `12-concrete-next-step.md` | 41% | 59% |
| `87-12-onboarding-paths-normative.md` | 41% | 59% |
| `01-svyazi-andrey-chuyan.md` | 59% | 41% |
| `05-which-combination-more-valuable.md` | 59% | 41% |
| `README.md` | 59% | 41% |
| `110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` | 59% | 41% |
| `08-consensus-algorithm.md` | 41% | 59% |
| `09-consensus-algorithm.md` | 41% | 59% |
| `2-distributed-agent-workshop.md` | 58% | 42% |
| `07-current-implementations.md` | 58% | 42% |
| `272-appendix-d-connection-diagram.md` | 58% | 41% |
| `09-do-not-glue.md` | 58% | 42% |
| `02-terminology.md` | 58% | 42% |
| `19-7-portalentry-structure.md` | 42% | 58% |
| `06-безопасность-приватность-и-бюджетный-роутинг.md` | 58% | 42% |
| `1-one-person-one-company.md` | 58% | 42% |
| `17-5-compatibility-levels.md` | 42% | 58% |
| `9-ambient-team-agent.md` | 58% | 42% |
| `63-history.md` | 42% | 58% |
| `03-similarity-3-mcp-support.md` | 42% | 58% |
| `01-fde-downgraded.md` | 58% | 42% |
| `363-твоя-identity-как-persistent-character.md` | 42% | 58% |
| `67-о-проекте.md` | 58% | 42% |
| `08-commercialization-three-paths.md` | 58% | 42% |
| `4-summary-authors.md` | 58% | 42% |
| `00-abstract-status.md` | 58% | 42% |
| `G-federated-local-graph.md` | 58% | 42% |
| `01-08-summary.md` | 42% | 58% |
| `118-appendix-a-шаблон-для-header-warning.md` | 58% | 42% |
| `341-приложение-c-образец-спецификаций-инструментов-ing.md` | 42% | 58% |
| `349-твоя-личность.md` | 58% | 42% |
| `DIGEST_WEEKLY.md` | 58% | 42% |
| `06-not-applicable-roles.md` | 42% | 58% |
| `README.md` | 58% | 42% |
| `08-что-это-продолжение-добавляет.md` | 58% | 42% |
| `wikontic.md` | 58% | 42% |
| `4-web-to-knowledge-pipeline.md` | 58% | 42% |
| `03-registry.md` | 58% | 42% |
| `11-application-plan-current-docs.md` | 58% | 42% |
| `QA.md` | 58% | 42% |
| `vitalyoborin.md` | 58% | 42% |
| `00-intro.md` | 58% | 42% |
| `04-komu-ty-sluzhish.md` | 57% | 42% |
| `00-overview.md` | 57% | 43% |
| `46-essence.md` | 43% | 57% |
| `20-adr-002-q6-first-class.md` | 43% | 57% |
| `FAQ.md` | 43% | 57% |
| `04-tertiary-research-engineer-agents.md` | 43% | 57% |
| `02-vshe-scientific-networking.md` | 57% | 43% |
| `08-bez-max-approval.md` | 43% | 57% |
| `CONTRADICTIONS.md` | 43% | 57% |
| `OUTLINE.md` | 43% | 57% |
| `03-partial-fit-honesty.md` | 57% | 43% |
| `04-passport.md` | 57% | 43% |
| `19-persistent-character.md` | 43% | 57% |
| `default-policy.md` | 57% | 43% |
| `150-appendix-c-version-history.md` | 43% | 57% |
| `03-revised-anthropic-mapping.md` | 43% | 57% |
| `07-выводы.md` | 57% | 43% |
| `14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 57% | 43% |
| `07-2-terminology.md` | 43% | 57% |
| `READING_LIST.md` | 43% | 57% |
| `spbmolot.md` | 57% | 43% |
| `5-browser-agents-headless.md` | 57% | 43% |
| `07-portal-entry.md` | 57% | 43% |
| `74-abstract.md` | 56% | 44% |
| `01-agent-routing.md` | 56% | 43% |
| `05-план-прототипа-и-возможные-контакты.md` | 56% | 44% |
| `10-three-entry-points.md` | 56% | 43% |
| `03-brainbox-multi-ai-hub.md` | 56% | 44% |
| `06-yazyki-kultura.md` | 44% | 56% |
| `01-structural-comparison-code-vs-docs.md` | 56% | 44% |
| `06-relation-existing-methodologies.md` | 56% | 44% |
| `07-crawl4ai-docling-yodoca-consolidator.md` | 44% | 56% |
| `05-tvoya-lichnost.md` | 56% | 44% |
| `04-grant-opportunities.md` | 44% | 56% |
| `02-terminology.md` | 56% | 44% |
| `08-implementation-nautilus.md` | 56% | 44% |
| `12-appendix-a-header-warning.md` | 44% | 56% |
| `LLM_SUMMARIES.md` | 44% | 56% |
| `00-intro.md` | 56% | 44% |
| `card-envelope.md` | 44% | 56% |
| `04-abstract.md` | 56% | 44% |
| `2-tsu-mome.md` | 56% | 44% |
| `338-ссылки.md` | 44% | 56% |
| `366-технический-stack-svyazi-2-0-foundation.md` | 44% | 56% |
| `76-1-introduction.md` | 56% | 44% |
| `QA.md` | 56% | 44% |
| `08-current-session-poc.md` | 56% | 44% |
| `07-mvp-planning.md` | 56% | 44% |
| `364-final-note-ты-experiment.md` | 44% | 56% |
| `83-8-q6-space-normative.md` | 44% | 56% |
| `04-passport.md` | 44% | 56% |
| `contact-outreach.md` | 56% | 44% |
| `06-metrics-tree.md` | 44% | 56% |
| `04-level-3-medium-active.md` | 44% | 56% |
| `05-compatibility-levels.md` | 56% | 44% |
| `06-adapter-interface.md` | 56% | 44% |
| `06-adapter-interface.md` | 44% | 56% |
| `mvp-plan.md` | 56% | 44% |
| `08-conductor-adversarial-review-auto-ai-router.md` | 56% | 44% |
| `6-continuous-eval-loop.md` | 56% | 44% |
| `02-level-1-minimal-zero.md` | 56% | 44% |
| `07-key-observation.md` | 45% | 55% |
| `126-установка.md` | 45% | 55% |
| `350-твои-языки-и-культурные-nuances.md` | 45% | 55% |
| `361-когда-ты-honestly-не-знаешь.md` | 45% | 55% |
| `README.md` | 55% | 45% |
| `README.md` | 45% | 55% |
| `svyazi.md` | 45% | 55% |
| `326-содержание.md` | 55% | 45% |
| `1-workflow-llm-mcp.md` | 45% | 55% |
| `08-conclusions.md` | 55% | 45% |
| `gaps.md` | 45% | 55% |
| `54-for-the-curious-philosophy.md` | 44% | 55% |
| `02-knowledge-graphs.md` | 55% | 45% |
| `04-memory-firewall-vs-prompt-worms.md` | 55% | 45% |
| `antipozitive.md` | 55% | 45% |
| `49-angle-perspective.md` | 45% | 55% |
| `4-riscv-privacy.md` | 55% | 45% |
| `12-onboarding-paths.md` | 55% | 45% |
| `CONTACT_PRIORITY.md` | 45% | 55% |
| `license-tree.md` | 55% | 45% |
| `04-stronger-paths-outside-anthropic.md` | 45% | 55% |
| `1-llm-gateway.md` | 55% | 45% |
| `03-what-doesnt-exist-on-market.md` | 45% | 55% |
| `04-what-i-can-do-now.md` | 55% | 45% |
| `SENTIMENT.md` | 46% | 55% |
| `8-self-aware-mcp-specs.md` | 55% | 46% |
| `QA.md` | 54% | 46% |
| `yodoca.md` | 54% | 46% |
| `PROGRESS.md` | 54% | 46% |
| `00-question-what-is-hermes.md` | 54% | 46% |
| `303-приложение-визуализация-позиции-в-серии.md` | 46% | 54% |
| `09-architectural-gaps.md` | 46% | 54% |
| `09-voobshche-nelzya.md` | 46% | 54% |
| `08-q6-space.md` | 54% | 46% |
| `07-why-valid-for-ai.md` | 54% | 45% |
| `5-tinyml-mcp-skills.md` | 54% | 46% |
| `02-formal-workflow.md` | 54% | 45% |
| `KNOWLEDGE_MAP.md` | 54% | 46% |
| `07-unique-niche-eu-legal-infra.md` | 54% | 46% |
| `3-discovery-research.md` | 46% | 54% |
| `188-ai-опосредованное-представительство-для-недопредст.md` | 54% | 46% |
| `06-difference-1-structured-substrate-missing.md` | 46% | 54% |
| `39-angle-perspective.md` | 46% | 54% |
| `ONBOARDING.md` | 54% | 46% |
| `07-progression-logic.md` | 54% | 46% |
| `05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md` | 46% | 54% |
| `research-note.md` | 54% | 46% |
| `03-secondary-beneficial-deployments.md` | 46% | 54% |
| `08-practical-ranking.md` | 46% | 54% |
| `22-glossary.md` | 46% | 54% |
| `executive-summary.md` | 54% | 46% |
| `02-multiagentnyy-khaos-reshenie-auto-ai-router.md` | 54% | 46% |
| `131-ограничения-текущей-версии-0-1-0-draft.md` | 47% | 53% |
| `77-2-terminology.md` | 47% | 53% |
| `8-budget-aware-intelligence-stack.md` | 53% | 47% |
| `skill-tool-policy.md` | 47% | 53% |
| `70-зачем-две-версии-параллельно.md` | 47% | 53% |
| `02-tvoyo-proishozhdenie.md` | 53% | 47% |
| `03-level-2-basic-lite.md` | 47% | 53% |
| `ACTION_ITEMS.md` | 53% | 47% |
| `02-three-overlapping-identities.md` | 53% | 47% |
| `13-outreach-communication.md` | 53% | 47% |
| `memory-write-policy.md` | 47% | 53% |
| `05-roadmap-6-12-months.md` | 47% | 53% |
| `4-speech-to-text-llm.md` | 53% | 47% |
| `C-multi-agent-factory.md` | 47% | 53% |
| `README.md` | 47% | 53% |
| `133-обратная-связь.md` | 47% | 53% |
| `dmitriila.md` | 53% | 47% |
| `conclusions.md` | 53% | 47% |
| `03-local-first.md` | 47% | 53% |
| `00-abstract.md` | 53% | 47% |
| `03-crdt-local-first-svyazi-cardindex.md` | 47% | 53% |
| `09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 47% | 53% |
| `ABBREVIATIONS.md` | 47% | 53% |
| `01-similarity-1-composite-skills.md` | 47% | 53% |
| `14-main-technical-risks.md` | 53% | 47% |
| `114-7-реализация-в-проекте-nautilus.md` | 52% | 48% |
| `HEALTH.md` | 52% | 48% |
| `HEATMAP.md` | 52% | 48% |
| `02-agentops-trace-envelope.md` | 48% | 52% |
| `01-three-related-themes.md` | 47% | 52% |
| `privacy.md` | 52% | 48% |
| `01-strategic-significance.md` | 52% | 48% |
| `04-pluses-as-business.md` | 52% | 48% |
| `357-твоя-коммуникация-в-outreach.md` | 52% | 48% |
| `H-research-to-product-flywheel.md` | 48% | 52% |
| `04-ensembles-overview.md` | 52% | 48% |
| `05-benchmarks.md` | 52% | 48% |
| `nlaik.md` | 52% | 48% |
| `sonia-black.md` | 52% | 48% |
| `5-agent-firewall.md` | 52% | 48% |
| `04-non-anthropic-paths.md` | 52% | 48% |
| `andrey-chuyan.md` | 52% | 48% |
| `zodigancode.md` | 52% | 48% |
| `05-compatibility-levels.md` | 48% | 52% |
| `A-collaboration-os.md` | 48% | 52% |
| `5-voice-local-memory.md` | 52% | 47% |
| `17-honestly-ne-znaesh.md` | 48% | 52% |
| `03-registry.md` | 52% | 48% |
| `11-интеграционный-контракт-который-стоит-зафиксироват.md` | 48% | 52% |
| `README.md` | 48% | 52% |
| `3-zinc-hybrid-arch.md` | 52% | 48% |
| `04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md` | 48% | 52% |
| `anastasiyaw.md` | 48% | 52% |
| `02-two-tier-publication.md` | 52% | 48% |
| `02-mcp-claude-desktop-use-cases.md` | 48% | 52% |
| `D-voice-first-mesh.md` | 48% | 52% |
| `58-content-overview.md` | 49% | 51% |
| `cutcode.md` | 51% | 49% |
| `risks.md` | 51% | 49% |
| `EMPTY_SECTIONS.md` | 48% | 51% |
| `11-integration-contracts.md` | 49% | 51% |
| `346-твоё-происхождение.md` | 51% | 49% |
| `353-что-ты-не-можешь-делать-вообще.md` | 49% | 51% |
| `05-reality-check-distribution-gap.md` | 49% | 51% |
| `B-forensic-rag.md` | 49% | 51% |
| `07-vs-notion-mem-affine-langgraph.md` | 51% | 49% |
| `06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md` | 51% | 49% |
| `59-angle-perspective.md` | 51% | 49% |
| `01-executive-summary.md` | 51% | 49% |
| `05-hw-nl2workflow.md` | 49% | 51% |
| `01-response.md` | 49% | 51% |
| `tagir-analyzes.md` | 51% | 49% |
| `3-crdt-self-hosted.md` | 49% | 51% |
| `kksudo.md` | 51% | 49% |
| `first-contacts.md` | 49% | 51% |
| `37-native-format.md` | 51% | 49% |
| `04-приоритетные-ансамбли.md` | 49% | 51% |
| `FOOTNOTES.md` | 51% | 49% |
| `3-adversarial-multi-ide.md` | 49% | 51% |
| `43-history.md` | 50% | 50% |
| `47-native-format.md` | 50% | 50% |
| `GITHUB_ISSUES.md` | 50% | 50% |
| `7-domain-agent-app-factory.md` | 50% | 50% |
| `vladspace.md` | 50% | 50% |
| `2-pkm-mcp-skills.md` | 50% | 50% |
| `STATS.md` | 50% | 50% |
| `03-a2a-vs-mcp-protocols.md` | 50% | 50% |
| `03-happyin-knowledge-space.md` | 50% | 50% |
| `104-appendix-c-references.md` | 50% | 50% |
| `36-essence.md` | 50% | 50% |
| `56-essence.md` | 50% | 50% |
| `01-kto-ty.md` | 50% | 50% |
| `signals.md` | 50% | 50% |
| `124-конфигурация-для-claude-desktop.md` | 50% | 50% |
| `mixaill76.md` | 50% | 50% |
| `06-platform-for-professional-communities.md` | 50% | 50% |


### 87. По секциям
_Файл: `docs/LANGUAGE_STATS.md` | 4 колонок, 18 строк_

| Секция | RU | EN | MIX |
|--------|----|----|-----|
| `01-svyazi` | 1 | 1 | 13 |
| `02-anthropic-vacancies` | 47 | 144 | 164 |
| `03-technology-combinations` | 1 | 2 | 4 |
| `04-ai-collaborations` | 0 | 0 | 17 |
| `05-habr-projects` | 1 | 0 | 7 |
| `ai-collaborations` | 1 | 4 | 24 |
| `anthropic-vacancies` | 5 | 25 | 81 |
| `autofilled` | 0 | 1 | 1 |
| `badges` | 0 | 1 | 0 |
| `contacts` | 0 | 1 | 14 |
| `glossary` | 0 | 3 | 1 |
| `habr-unique-projects` | 2 | 6 | 47 |
| `lorenzo-agent` | 0 | 12 | 49 |
| `nautilus` | 38 | 109 | 104 |
| `root` | 2 | 21 | 68 |
| `svyazi-2-0` | 0 | 8 | 51 |
| `technology-combinations` | 0 | 31 | 20 |
| `templates` | 0 | 0 | 6 |


### 88. Индекс ссылок
_Файл: `docs/LINKS.md` | 2 колонок, 200 строк_

| URL | Найден в файлах |
|-----|-----------------|
| http://localhost:8000 | 7 |
| http://localhost:8080 | 6 |
| https://...install.sh | 4 |
| https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakansiy-s-zarplatoy-do-405000 | 4 |
| https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakans… | 3 |
| https://activitypub.rocks/ | 4 |
| https://api.github.com/users/svend4/repos?per_page=100&sort=updated | 5 |
| https://api.github.com/users/svend4/repos?per_page=100&sort=updated&type=owner | 5 |
| https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv | 4 |
| https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW | 1 |
| https://claude.com/product/cowork | 9 |
| https://creativecommons.org/licenses/by/4.0/ | 5 |
| https://datatracker.ietf.org/doc/html/rfc2119 | 1 |
| https://forum.[obsidian | 5 |
| https://forum.obsidian.md/t/new-plugin-llm-wiki-turn-your-vault-into-a-queryable-knowledge-base-privately/113223 | 3 |
| https://github | 4 |
| https://github. | 5 |
| https://github.com/AnastasiyaW | 4 |
| https://github.com/AnastasiyaW/knowledge-space | 7 |
| https://github.com/AnastasiyaW/knowledge-space` | 3 |
| https://github.com/Antipozitive | 4 |
| https://github.com/Cutcode | 4 |
| https://github.com/Dmitriila | 4 |
| https://github.com/MiXaiLL76 | 4 |
| https://github.com/Sonia_Black | 4 |
| https://github.com/VitalyOborin | 4 |
| https://github.com/VitalyOborin/yodoca | 4 |
| https://github.com/VladSpace | 4 |
| https://github.com/andrey_chuyan | 4 |
| https://github.com/anthropics/mcp | 5 |
| https://github.com/camel-ai/camel | 6 |
| https://github.com/kksudo | 4 |
| https://github.com/kksudo/agentfs | 4 |
| https://github.com/mcp | 7 |
| https://github.com/mcp` | 3 |
| https://github.com/nlaik | 4 |
| https://github.com/settings/tokens | 5 |
| https://github.com/settings/tokens` | 3 |
| https://github.com/spbmolot | 4 |
| https://github.com/spbmolot/ngt-memory | 4 |
| https://github.com/svend4/ | 3 |
| https://github.com/svend4/data70 | 5 |
| https://github.com/svend4/data70` | 2 |
| https://github.com/svend4/info1 | 8 |
| https://github.com/svend4/info1` | 3 |
| https://github.com/svend4/info40 | 4 |
| https://github.com/svend4/info7 | 4 |
| https://github.com/svend4/ingit | 13 |
| https://github.com/svend4/ingit/issues | 4 |
| https://github.com/svend4/ingit` | 3 |
| https://github.com/svend4/meta | 6 |
| https://github.com/svend4/meta` | 3 |
| https://github.com/svend4/nautilus | 17 |
| https://github.com/svend4/nautilus.git | 3 |
| https://github.com/svend4/nautilus/blob/claude/review-nautilus-changes-tdywx/README.md | 3 |
| https://github.com/svend4/nautilus/blob/main/INTEGRATION.md | 3 |
| https://github.com/svend4/nautilus/blob/main/PORTAL-PROTOCOL | 3 |
| https://github.com/svend4/nautilus/blob/main/PORTAL-PROTOCOL.md | 4 |
| https://github.com/svend4/nautilus/blob/main/PORTAL-PROTOCOL.md` | 2 |
| https://github.com/svend4/nautilus/blob/main/README.md | 3 |
| https://github.com/svend4/nautilus/blob/main/REVIEW_METHODOLOGY.md | 4 |
| https://github.com/svend4/nautilus/blob/main/REVIEW_METHODOLOGY.md` | 3 |
| https://github.com/svend4/nautilus/blob/main/STATUS.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_1.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_2.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_3.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/IMPLEMENTATION_STAGE_PART_4.md | 3 |
| https://github.com/svend4/nautilus/blob/main/docs/PORTAL-PROTOCOL-v1.0.md | 4 |
| https://github.com/svend4/nautilus/branches | 3 |
| https://github.com/svend4/nautilus/commits/main | 3 |
| https://github.com/svend4/nautilus/issues | 25 |
| https://github.com/svend4/nautilus/issues` | 3 |
| https://github.com/svend4/nautilus/tree/abfa80e853594454bae03e95ba09f12eb443ca50/docs | 3 |
| https://github.com/svend4/nautilus/tree/main/adapters | 3 |
| https://github.com/svend4/nautilus/tree/main/passports | 3 |
| https://github.com/svend4/nautilus` | 3 |
| https://github.com/svend4/pro2 | 10 |
| https://github.com/svend4/pro2/blob/main/nautilus/README.md | 3 |
| https://github.com/svend4/pro2/tree/6637d1299af963db66485aa5599346d41badc6dc/nautilus | 3 |
| https://github.com/svend4/pro2/tree/main/nautilus | 3 |
| https://github.com/svend4/pro2` | 3 |
| https://github.com/svend4?tab=repositories | 3 |
| https://github.com/tagir_analyzes | 3 |
| https://github.com/zodigancode | 3 |
| https://habr. | 7 |
| https://habr.com/ru/articles/1002138/ | 6 |
| https://habr.com/ru/articles/1002138/` | 3 |
| https://habr.com/ru/articles/1005776/ | 6 |
| https://habr.com/ru/articles/1005776/` | 3 |
| https://habr.com/ru/articles/1006602/ | 4 |
| https://habr.com/ru/articles/1006602/, | 4 |
| https://habr.com/ru/articles/1006602/` | 3 |
| https://habr.com/ru/articles/1006622/ | 8 |
| https://habr.com/ru/articles/1006622/` | 3 |
| https://habr.com/ru/articles/1007122/ | 6 |
| https://habr.com/ru/articles/1007122/, | 5 |
| https://habr.com/ru/articles/1007122/` | 3 |
| https://habr.com/ru/articles/1009538/ | 6 |
| https://habr.com/ru/articles/1009538/` | 3 |
| https://habr.com/ru/articles/1009608/ | 6 |
| https://habr.com/ru/articles/1009608/` | 3 |
| https://habr.com/ru/articles/1009958/ | 6 |
| https://habr.com/ru/articles/1009958/` | 3 |
| https://habr.com/ru/articles/1010198/ | 6 |
| https://habr.com/ru/articles/1010198/` | 3 |
| https://habr.com/ru/articles/1010478/ | 6 |
| https://habr.com/ru/articles/1010478/` | 3 |
| https://habr.com/ru/articles/1012894/ | 4 |
| https://habr.com/ru/articles/1012894/` | 1 |
| https://habr.com/ru/articles/1014366/ | 6 |
| https://habr.com/ru/articles/1014366/` | 3 |
| https://habr.com/ru/articles/1016096/ | 6 |
| https://habr.com/ru/articles/1016096/` | 3 |
| https://habr.com/ru/articles/1017200/ | 7 |
| https://habr.com/ru/articles/1017200/` | 3 |
| https://habr.com/ru/articles/1019588/ | 4 |
| https://habr.com/ru/articles/1019588/, | 4 |
| https://habr.com/ru/articles/1019588/` | 3 |
| https://habr.com/ru/articles/1020598/ | 4 |
| https://habr.com/ru/articles/1020598/, | 4 |
| https://habr.com/ru/articles/1020598/` | 3 |
| https://habr.com/ru/articles/1020702/ | 3 |
| https://habr.com/ru/articles/1020860/ | 6 |
| https://habr.com/ru/articles/1020860/` | 3 |
| https://habr.com/ru/articles/1021622/ | 4 |
| https://habr.com/ru/articles/1021622/` | 1 |
| https://habr.com/ru/articles/1023446/ | 6 |
| https://habr.com/ru/articles/1023446/` | 3 |
| https://habr.com/ru/articles/1024634/ | 6 |
| https://habr.com/ru/articles/1024634/` | 3 |
| https://habr.com/ru/articles/1024884/comments/ | 6 |
| https://habr.com/ru/articles/1024884/comments/` | 3 |
| https://habr.com/ru/articles/1026666/ | 4 |
| https://habr.com/ru/articles/1027210/ | 7 |
| https://habr.com/ru/articles/1027210/` | 3 |
| https://habr.com/ru/articles/1027382/ | 6 |
| https://habr.com/ru/articles/1027382/` | 3 |
| https://habr.com/ru/articles/1027658/ | 6 |
| https://habr.com/ru/articles/1027658/` | 3 |
| https://habr.com/ru/articles/1027724/ | 8 |
| https://habr.com/ru/articles/1027724/` | 3 |
| https://habr.com/ru/articles/1027878/ | 4 |
| https://habr.com/ru/articles/1027878/, | 4 |
| https://habr.com/ru/articles/1027878/` | 3 |
| https://habr.com/ru/articles/495554/ | 7 |
| https://habr.com/ru/articles/495554/` | 3 |
| https://habr.com/ru/articles/786278/ | 3 |
| https://habr.com/ru/articles/800033/ | 3 |
| https://habr.com/ru/articles/893356/ | 6 |
| https://habr.com/ru/articles/893356/` | 3 |
| https://habr.com/ru/articles/938626/ | 4 |
| https://habr.com/ru/articles/938626/, | 4 |
| https://habr.com/ru/articles/938626/` | 3 |
| https://habr.com/ru/articles/943498/ | 4 |
| https://habr.com/ru/articles/943498/, | 4 |
| https://habr.com/ru/articles/943498/` | 3 |
| https://habr.com/ru/articles/955798/ | 6 |
| https://habr.com/ru/articles/955798/` | 3 |
| https://habr.com/ru/articles/971620/ | 3 |
| https://habr.com/ru/articles/975414/ | 6 |
| https://habr.com/ru/articles/975414/` | 3 |
| https://habr.com/ru/articles/983684/ | 6 |
| https://habr.com/ru/articles/983684/` | 3 |
| https://habr.com/ru/articles/987094/ | 3 |
| https://habr.com/ru/articles/996144/ | 6 |
| https://habr.com/ru/articles/996144/` | 3 |
| https://habr.com/ru/companies/airi/articles/1000720/ | 7 |
| https://habr.com/ru/companies/airi/articles/1000720/` | 3 |
| https://habr.com/ru/companies/airi/articles/855128/ | 7 |
| https://habr.com/ru/companies/airi/articles/855128/` | 3 |
| https://habr.com/ru/companies/neuronet/articles/592625/ | 3 |
| https://habr.com/ru/companies/ruvds/articles/980152/ | 3 |
| https://habr.com/ru/companies/sberdevices/articles/855080/ | 3 |
| https://habr.com/ru/companies/selectel/articles/1023796/ | 3 |
| https://habr.com/ru/companies/surfstudio/articles/943108/ | 6 |
| https://habr.com/ru/companies/surfstudio/articles/943108/` | 3 |
| https://habr.com/ru/companies/teamly/articles/1024062/ | 6 |
| https://habr.com/ru/companies/teamly/articles/1024062/` | 3 |
| https://habr.com/ru/companies/yadro/articles/645843/ | 3 |
| https://habr.com/ru/companies/yadro/articles/648119/ | 3 |
| https://habr.com/ru/companies/yandex/articles/1019928/ | 7 |
| https://habr.com/ru/companies/yandex/articles/1019928/` | 3 |
| https://habr.com/ru/companies/yoomoney/articles/1012870/ | 7 |
| https://habr.com/ru/companies/yoomoney/articles/1012870/` | 3 |
| https://habr.com/ru/news/789164/ | 3 |
| https://happyin.space/ | 4 |
| https://json-schema.org/draft/2020-12/schema | 1 |
| https://nautilus-okwf.org/sub-agents/sgb-ix-paragraph-78-24-7 | 3 |
| https://olegtalks.ru/base/tpost/xn7kev4fa1-docling-gotovim-dannie-dlya-rag-i-llm | 6 |
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


### 89. Качество по разделам
_Файл: `docs/METRICS.md` | 6 колонок, 6 строк_

| Раздел | Балл | Ссылок/1K слов | Код-блоков/1K | % с summary | % с тегами |
|--------|------|----------------|--------------|-------------|------------|
| **01-svyazi** | 65 | 25.6 | 0.5 | 100% | 93% |
| **02-anthropic-vacancies** | 74 | 36.1 | 0.8 | 99% | 97% |
| **03-technology-combinations** | 67 | 40.1 | 0.0 | 100% | 86% |
| **04-ai-collaborations** | 78 | 22.7 | 0.0 | 100% | 94% |
| **05-habr-projects** | 67 | 50.3 | 0.0 | 89% | 78% |
| **root** | 67 | 22.4 | 0.9 | 74% | 76% |


### 90. Топ-15 лучших документов
_Файл: `docs/METRICS.md` | 3 колонок, 15 строк_

| Документ | Балл | Слов |
|----------|------|------|
| `01-интегральный-анализ-профиля-svend4` | 100 | 19144 |
| `02-общий-план-развития-nautilus-portal-p` | 100 | 3207 |
| `109-3-принципы-консолидации-фаза-c` | 100 | 560 |
| `133-обратная-связь` | 100 | 17018 |
| `139-2-the-double-triangle-architecture` | 100 | 753 |
| `142-5-pattern-library-as-bridge-between-` | 100 | 704 |
| `232-1-типология-из-пяти-типов-агентов-на` | 100 | 873 |
| `248-приложение-c-архитектура-быстрого-ст` | 100 | 3476 |
| `330-4-симбиотическая-архитектура` | 100 | 703 |
| `331-5-четыре-пути-интеграции-в-порядке-д` | 100 | 783 |
| `341-приложение-c-образец-спецификаций-ин` | 100 | 20426 |
| `342-что-такое-вариант-c-concept-document` | 100 | 11281 |
| `365-развёрнутый-анализ-внуковой-комбинац` | 100 | 4419 |
| `366-технический-stack-svyazi-2-0-foundat` | 100 | 3873 |
| `69-section` | 100 | 9531 |


### 91. Документы, требующие улучшения (17)
_Файл: `docs/METRICS.md` | 3 колонок, 17 строк_

| Документ | Балл | Что отсутствует |
|----------|------|----------------|
| `185-appendix-b-domain-comparison-ma` | 30 | summary, tags, TOC, callout |
| `206-приложение-b-матрица-сравнения-` | 30 | summary, tags, TOC, callout |
| `ABBREVIATIONS` | 30 | summary, tags, TOC, callout |
| `AUTHORS` | 30 | summary, tags, TOC, callout |
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
| `README` | 30 | summary, tags, TOC, callout |


### 92. Легенда
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


### 93. Карта пробелов знаний
_Файл: `docs/MISSING.md` | 6 колонок, 25 строк_

| Статус | Тема / Проект | Файлов | Слов | Минимум | Примеры файлов |
|--------|---------------|--------|------|---------|----------------|
| ✅ | **Svyazi** | 315 | 274039 | ≥5ф/2000сл | `CROSSREFS.md`, `README.md` |
| ✅ | **local-first** | 173 | 136972 | ≥2ф/300сл | `CONTACTS.md`, `PARAGRAPH_QUALITY.md` |
| ✅ | **self-improvement** | 148 | 12176 | ≥1ф/100сл | `READING_LIST.md`, `CONTACTS.md` |
| ✅ | **Yodoca** | 141 | 166821 | ≥2ф/300сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **CardIndex** | 137 | 158894 | ≥3ф/500сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **knowledge-space** | 100 | 129209 | ≥3ф/500сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **AgentFS** | 99 | 129452 | ≥3ф/500сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **NGT Memory** | 95 | 72263 | ≥2ф/300сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **mclaude** | 87 | 110514 | ≥2ф/200сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **Rufler** | 82 | 110947 | ≥2ф/200сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **LiteParse** | 77 | 108156 | ≥2ф/300сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **AI Factory** | 76 | 54388 | ≥2ф/200сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **SENTINEL** | 68 | 52574 | ≥2ф/200сл | `CROSSREFS.md`, `CONTACTS.md` |
| ✅ | **CRDT** | 63 | 101107 | ≥1ф/100сл | `PARAGRAPH_QUALITY.md`, `TABLES.md` |
| ✅ | **AutoResearch** | 60 | 96883 | ≥1ф/100сл | `CROSSREFS.md`, `PARAGRAPH_QUALITY.md` |
| ✅ | **Evidence Envelope** | 43 | 20856 | ≥2ф/200сл | `QA.md`, `EMPTY_SECTIONS.md` |
| ✅ | **Sozialrecht** | 41 | 113760 | ≥1ф/200сл | `PARAGRAPH_QUALITY.md`, `LLM_SUMMARIES.md` |
| ✅ | **Card Envelope** | 30 | 17127 | ≥2ф/200сл | `QA.md`, `TABLES.md` |
| ✅ | **Memory Write Policy** | 22 | 15573 | ≥2ф/200сл | `TABLES.md`, `MINDMAP.md` |
| ✅ | **privacy by design** | 22 | 15240 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |
| ✅ | **Review Record** | 19 | 14443 | ≥1ф/100сл | `QA.md`, `TABLES.md` |
| ✅ | **бюджетный роутинг** | 19 | 21956 | ≥2ф/300сл | `QA.md`, `TABLES.md` |
| ✅ | **Skill Policy** | 15 | 4228 | ≥1ф/100сл | `QA.md`, `TABLES.md` |
| ✅ | **лицензия BSL** | 3 | 1344 | ≥1ф/50сл | `TABLES.md`, `MISSING.md` |
| ✅ | **voice ingestion** | 2 | 760 | ≥1ф/100сл | `TABLES.md`, `MISSING.md` |


### 94. 👤 People (20)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 20 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `anthropic` | 746 | people |
| `claude` | 399 | people |
| `svend4` | 196 | people |
| `spbmolot` | 42 | people |
| `kksudo` | 39 | people |
| `anastasiyaw` | 34 | people |
| `vitalyoborin` | 26 | people |
| `andrey_chuyan` | 10 | people |
| `vuguzum` | 6 | people |
| `artur-gavronchuk` | 5 | people |
| `dementev-dev` | 5 | people |
| `settings` | 4 | people |
| `nicholasspisak` | 3 | people |
| `yjs` | 3 | people |
| `users` | 3 | people |
| `kagvi13` | 2 | people |
| `lib4u` | 2 | people |
| `ruvnet` | 2 | people |
| `anthropics` | 2 | people |
| `camel-ai` | 2 | people |


### 95. 👤 People (20)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 40 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `nautilus` | 463 | projects |
| `svyazi` | 295 | projects |
| `github` | 234 | projects |
| `yodoca` | 130 | projects |
| `CardIndex` | 126 | projects |
| `ngt` | 120 | projects |
| `lorenzo` | 119 | projects |
| `MemNet` | 110 | projects |
| `agentfs` | 90 | projects |
| `knowledge-space` | 88 | projects |
| `obsidian` | 80 | projects |
| `LiteParse` | 65 | projects |
| `notion` | 61 | projects |
| `AutoResearch` | 48 | projects |
| `PortalEntry` | 46 | projects |
| `gpt` | 41 | projects |
| `wikontic` | 39 | projects |
| `AutoGen` | 21 | projects |
| `gemini` | 20 | projects |
| `OpenClaw` | 20 | projects |
| `OpenWhispr` | 18 | projects |
| `ClickHouse` | 18 | projects |
| `CodeWiki` | 17 | projects |
| `ChatDev` | 15 | projects |
| `DeepSeek` | 15 | projects |
| `BaseAdapter` | 15 | projects |
| `QueryResult` | 15 | projects |
| `LangChain` | 15 | projects |
| `OpenClaude` | 15 | projects |
| `LangGraph` | 14 | projects |
| `VladSpace` | 13 | projects |
| `mistral` | 13 | projects |
| `LlamaIndex` | 12 | projects |
| `faiss` | 12 | projects |
| `TypeScript` | 12 | projects |
| `BrainBox` | 12 | projects |
| `AgentOps` | 12 | projects |
| `DeepMind` | 11 | projects |
| `chromadb` | 11 | projects |
| `SourceCraft` | 10 | projects |


### 96. 👤 People (20)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 31 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `mcp` | 291 | tech |
| `llm` | 188 | tech |
| `api` | 165 | tech |
| `rag` | 148 | tech |
| `markdown` | 88 | tech |
| `python` | 87 | tech |
| `yaml` | 85 | tech |
| `json` | 76 | tech |
| `git` | 72 | tech |
| `go` | 57 | tech |
| `rest` | 51 | tech |
| `sqlite` | 31 | tech |
| `html` | 25 | tech |
| `transformer` | 23 | tech |
| `ci` | 21 | tech |
| `postgresql` | 21 | tech |
| `vector` | 19 | tech |
| `cd` | 17 | tech |
| `docker` | 15 | tech |
| `sql` | 14 | tech |
| `react` | 13 | tech |
| `bm25` | 13 | tech |
| `rust` | 10 | tech |
| `jaccard` | 6 | tech |
| `cosine` | 5 | tech |
| `webhook` | 4 | tech |
| `kubernetes` | 4 | tech |
| `css` | 3 | tech |
| `terraform` | 3 | tech |
| `graphql` | 2 | tech |
| `fastapi` | 2 | tech |


### 97. 👤 People (20)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 8 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `вк` | 261 | orgs |
| `meta` | 200 | orgs |
| `mail` | 69 | orgs |
| `openai` | 45 | orgs |
| `google` | 34 | orgs |
| `microsoft` | 21 | orgs |
| `yandex` | 13 | orgs |
| `сбер` | 8 | orgs |


### 98. 👤 People (20)
_Файл: `docs/NAMED_ENTITIES.md` | 3 колонок, 32 строк_

| Сущность | Файлов | Тип |
|----------|--------|-----|
| `2026-04` | 99 | dates |
| `2026-04-29` | 22 | dates |
| `2026-04-19` | 19 | dates |
| `апрель 2026` | 16 | dates |
| `2026-04-26` | 12 | dates |
| `апреля 2026` | 11 | dates |
| `2026/04/25` | 10 | dates |
| `в 2026 году` | 8 | dates |
| `март 2026` | 7 | dates |
| `марта 2026` | 6 | dates |
| `декабрь 2025` | 6 | dates |
| `апреле 2026` | 6 | dates |
| `2026-05-03` | 5 | dates |
| `2026-04-15` | 5 | dates |
| `декабря 2025` | 4 | dates |
| `2025-12-15` | 4 | dates |
| `2024-01-01` | 4 | dates |
| `май 2025` | 4 | dates |
| `феврале 2025` | 4 | dates |
| `Сентябрь 2025` | 4 | dates |
| `январе 2026` | 4 | dates |
| `января 2026` | 4 | dates |
| `2026-04-22` | 4 | dates |
| `декабрь 2024` | 3 | dates |
| `2025-11-12` | 3 | dates |
| `февраля 2026` | 3 | dates |
| `2024-01` | 2 | dates |
| `февраль 2026` | 2 | dates |
| `2026-02-01` | 2 | dates |
| `2026-10-15` | 2 | dates |
| `ноябре 2025` | 2 | dates |
| `2024-06-15` | 2 | dates |


### 99. Топ-20 ко-упоминаемых пар
_Файл: `docs/NETWORK.md` | 2 колонок, 20 строк_

| Пара | Общих файлов |
|------|-------------|
| **Cowork** ↔ **ingit** | 138 |
| **Svyazi** ↔ **Yodoca** | 123 |
| **Svyazi** ↔ **CardIndex** | 119 |
| **Svyazi** ↔ **NGT** | 117 |
| **Yodoca** ↔ **NGT** | 102 |
| **Svyazi** ↔ **AgentFS** | 90 |
| **Svyazi** ↔ **MemNet** | 88 |
| **Svyazi** ↔ **knowledge-space** | 85 |
| **CardIndex** ↔ **NGT** | 82 |
| **Svyazi** ↔ **mclaude** | 80 |
| **CardIndex** ↔ **Yodoca** | 78 |
| **AgentFS** ↔ **NGT** | 78 |
| **Svyazi** ↔ **Rufler** | 76 |
| **AgentFS** ↔ **Yodoca** | 75 |
| **CardIndex** ↔ **AgentFS** | 74 |
| **Svyazi** ↔ **AI Factory** | 72 |
| **Svyazi** ↔ **LiteParse** | 72 |
| **AgentFS** ↔ **knowledge-space** | 70 |
| **NGT** ↔ **knowledge-space** | 67 |
| **Yodoca** ↔ **knowledge-space** | 66 |


### 100. Центральность узлов (влиятельность)
_Файл: `docs/NETWORK.md` | 3 колонок, 20 строк_

| Узел | Балл центральности | Тип |
|------|--------------------|-----|
| **Svyazi** | 1347 | 📦 Проект |
| **NGT** | 1041 | 📦 Проект |
| **Yodoca** | 1014 | 📦 Проект |
| **CardIndex** | 949 | 📦 Проект |
| **AgentFS** | 894 | 📦 Проект |
| **knowledge-space** | 848 | 📦 Проект |
| **mclaude** | 756 | 📦 Проект |
| **Rufler** | 749 | 📦 Проект |
| **MemNet** | 721 | 📦 Проект |
| **LiteParse** | 717 | 📦 Проект |
| **AI Factory** | 689 | 📦 Проект |
| **SENTINEL** | 607 | 📦 Проект |
| **Lorenzo (svend4)** | 573 | 👤 Автор |
| **Cowork** | 558 | 📦 Проект |
| **ingit** | 522 | 📦 Проект |
| **Андрей (kksudo)** | 506 | 👤 Автор |
| **Lorenzo** | 495 | 📦 Проект |
| **Виталий (spbmolot)** | 467 | 👤 Автор |
| **Wikontic** | 395 | 📦 Проект |
| **Firecrawl** | 182 | 📦 Проект |


### 101. Структура документации
_Файл: `docs/ONBOARDING.md` | 4 колонок, 5 строк_

| Раздел | Тема | Файлов | Слов |
|--------|------|--------|------|
| [`docs/01-svyazi/`](docs/01-svyazi/README.md) | Архитектура Svyazi 2.0 | 16 | 10,166 |
| [`docs/02-anthropic-vacancies/`](docs/02-anthropic-vacancies/README.md) | Вакансии Anthropic | 357 | 260,851 |
| [`docs/03-technology-combinations/`](docs/03-technology-combinations/README.md) | Комбинации технологий | 7 | 2,433 |
| [`docs/04-ai-collaborations/`](docs/04-ai-collaborations/README.md) | AI-коллаборации | 17 | 24,521 |
| [`docs/05-habr-projects/`](docs/05-habr-projects/README.md) | Хабр-проекты | 10 | 8,296 |


### 102. Ключевые документы
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


### 103. Архитектура компонентов
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


### 104. Топ-20 по объёму (важные и изолированные)
_Файл: `docs/ORPHANS.md` | 3 колонок, 1 строк_

| Файл | Слов | Раздел |
|------|------|--------|
| `` | 36 | `autofilled` |


### 105. Типы проблем
_Файл: `docs/PARAGRAPH_QUALITY.md` | 2 колонок, 5 строк_

| Тип | Кол-во |
|-----|--------|
| ⚪ Короткий абзац | 10637 |
| ✂️  Оборванный | 4981 |
| 📏 Длинное предложение | 263 |
| 🔁 Повтор начала | 2305 |
| ♊ Дубль | 650 |


### 106. Корпусная статистика
_Файл: `docs/PASSIVE_VOICE.md` | 2 колонок, 4 строк_

| Метрика | Значение |
|---------|----------|
| Средний % пассива | 1.6% |
| Всего канцеляризмов | 98 |
| Всего номинализаций | 8035 |
| Оценка | 🟢 Активный стиль |


### 107. Топ файлов по доле пассива
_Файл: `docs/PASSIVE_VOICE.md` | 6 колонок, 20 строк_

| Файл | Пассив% | Оценка | Пред. RU | Пред. EN | Канцеляризмы |
|------|---------|--------|----------|----------|--------------|
| `CONCEPTS.md` | 55% | 🔴 Преимущественно пассив | 4 | 2 | 1 |
| `301-благодарности.md` | 25% | 🟠 Много пассива | 2 | 0 | 0 |
| `327-1-открытие-cowork-и-почему-это-меняет-всё.md` | 21% | 🟠 Много пассива | 8 | 0 | 2 |
| `70-зачем-две-версии-параллельно.md` | 20% | 🟠 Много пассива | 1 | 0 | 0 |
| `96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | 20% | 🟠 Много пассива | 1 | 0 | 0 |
| `01-otkrytie-cowork.md` | 19% | 🟠 Много пассива | 7 | 0 | 2 |
| `112-5-связь-с-существующими-методологиями.md` | 17% | 🟠 Много пассива | 4 | 0 | 0 |
| `ORPHANS.md` | 17% | 🟠 Много пассива | 1 | 0 | 0 |
| `06-metrics-tree.md` | 17% | 🟠 Много пассива | 1 | 0 | 0 |
| `2-autoresearch-legal.md` | 17% | 🟠 Много пассива | 1 | 0 | 0 |
| `00-question-scenario.md` | 17% | 🟠 Много пассива | 1 | 0 | 0 |
| `00-question-habr-2.md` | 17% | 🟠 Много пассива | 1 | 0 | 0 |
| `00-question-practical.md` | 17% | 🟠 Много пассива | 1 | 0 | 0 |
| `00-question-multiple-mentors.md` | 17% | 🟠 Много пассива | 1 | 0 | 0 |
| `15-glossary.md` | 17% | 🟠 Много пассива | 1 | 0 | 0 |
| `18-reference-implementation.md` | 17% | 🟠 Много пассива | 1 | 0 | 0 |
| `00-question-supply-demand.md` | 17% | 🟠 Много пассива | 1 | 0 | 1 |
| `28-pydantic-enforced-legal-workflows.md` | 17% | 🟠 Много пассива | 0 | 1 | 0 |
| `108-2-формальный-workflow.md` | 15% | 🟠 Много пассива | 2 | 0 | 0 |
| `06-relation-existing-methodologies.md` | 15% | 🟡 Умеренный пассив | 3 | 0 | 0 |


### 108. Состояние компонентов
_Файл: `docs/PROGRESS.md` | 3 колонок, 5 строк_

| Компонент | Статус | Детали |
|-----------|--------|--------|
| Контакты авторов | ⚠️ 14 файлов, не отправлено | 14 файлов в docs/contacts/ |
| LLM-обогащение | ⬜ не запущено | pip install anthropic && python scripts/improve_llm_enrich.py |
| Скрипты обработки | ✅ 140 скриптов | 5 LLM-скриптов, MCP=✅ |
| DIGEST.md | ✅ 6 секций | python scripts/improve_llm_summary.py |
| Claude Skills | ✅ 5 скиллов | review-docs, analyze-project, status, write-contact, improve |


### 109. Метрики качества
_Файл: `docs/PROGRESS.md` | 3 колонок, 3 строк_

| Метрика | Балл | Статус |
|---------|------|--------|
| Здоровье репо (HEALTH) | 77.0/100 | 🟡 |
| Качество доков (METRICS) | 71.3/100 | 🟡 |
| Go/No-Go (SCORING) | 93.0/100 | 🟡 |


### 110. Все документы
_Файл: `docs/READABILITY.md` | 6 колонок, 1166 строк_

| Файл | FRE | Уровень | Слов | Пред. | Слов/пред. |
|------|-----|---------|------|-------|-----------|
| `docs/01-svyazi/01-executive-summary.md` | 0 | 🔴 Очень сложный | 677 | 37 | 18.3 |
| `docs/01-svyazi/02-methodology.md` | 0 | 🔴 Очень сложный | 413 | 27 | 15.3 |
| `docs/01-svyazi/03-component-catalog.md` | 0 | 🔴 Очень сложный | 1462 | 105 | 13.9 |
| `docs/01-svyazi/04-ensembles-overview.md` | 0 | 🔴 Очень сложный | 1151 | 67 | 17.2 |
| `docs/01-svyazi/06-security-privacy.md` | 0 | 🔴 Очень сложный | 797 | 43 | 18.5 |
| `docs/01-svyazi/07-mvp-planning.md` | 0 | 🔴 Очень сложный | 1027 | 61 | 16.8 |
| `docs/01-svyazi/08-conclusions.md` | 0 | 🔴 Очень сложный | 417 | 37 | 11.3 |
| `docs/01-svyazi/09-architectural-gaps.md` | 0 | 🔴 Очень сложный | 810 | 43 | 18.8 |
| `docs/01-svyazi/10-second-order-ensembles.md` | 0 | 🔴 Очень сложный | 828 | 57 | 14.5 |
| `docs/01-svyazi/11-integration-contracts.md` | 0 | 🔴 Очень сложный | 752 | 48 | 15.7 |
| `docs/01-svyazi/12-roadmap.md` | 0 | 🔴 Очень сложный | 694 | 44 | 15.8 |
| `docs/01-svyazi/13-contacts.md` | 0 | 🔴 Очень сложный | 822 | 55 | 14.9 |
| `docs/01-svyazi/14-limitations.md` | 0 | 🔴 Очень сложный | 682 | 44 | 15.5 |
| `docs/01-svyazi/QA.md` | 0 | 🔴 Очень сложный | 508 | 53 | 9.6 |
| `docs/02-anthropic-vacancies/00-intro.md` | 0 | 🔴 Очень сложный | 7916 | 549 | 14.4 |
| `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` | 0 | 🔴 Очень сложный | 17396 | 1329 | 13.1 |
| `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` | 0 | 🔴 Очень сложный | 2330 | 281 | 8.3 |
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | 0 | 🔴 Очень сложный | 142 | 14 | 10.1 |
| `docs/02-anthropic-vacancies/04-abstract.md` | 0 | 🔴 Очень сложный | 127 | 11 | 11.5 |
| `docs/02-anthropic-vacancies/06-1-introduction.md` | 0 | 🔴 Очень сложный | 334 | 31 | 10.8 |
| `docs/02-anthropic-vacancies/07-2-terminology.md` | 0 | 🔴 Очень сложный | 278 | 40 | 7.0 |
| `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` | 0 | 🔴 Очень сложный | 265 | 40 | 6.6 |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | 0 | 🔴 Очень сложный | 142 | 18 | 7.9 |
| `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` | 0 | 🔴 Очень сложный | 169 | 16 | 10.6 |
| `docs/02-anthropic-vacancies/104-appendix-c-references.md` | 0 | 🔴 Очень сложный | 825 | 111 | 7.4 |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | 0 | 🔴 Очень сложный | 111 | 13 | 8.5 |
| `docs/02-anthropic-vacancies/106-tl-dr.md` | 0 | 🔴 Очень сложный | 146 | 17 | 8.6 |
| `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` | 0 | 🔴 Очень сложный | 356 | 31 | 11.5 |
| `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` | 0 | 🔴 Очень сложный | 281 | 30 | 9.4 |
| `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` | 0 | 🔴 Очень сложный | 350 | 30 | 11.7 |
| `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` | 0 | 🔴 Очень сложный | 282 | 36 | 7.8 |
| `docs/02-anthropic-vacancies/111-4-условия-применимости.md` | 0 | 🔴 Очень сложный | 242 | 19 | 12.7 |
| `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` | 0 | 🔴 Очень сложный | 311 | 38 | 8.2 |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 0 | 🔴 Очень сложный | 140 | 10 | 14.0 |
| `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` | 0 | 🔴 Очень сложный | 299 | 34 | 8.8 |
| `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | 0 | 🔴 Очень сложный | 356 | 37 | 9.6 |
| `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` | 0 | 🔴 Очень сложный | 282 | 29 | 9.7 |
| `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` | 0 | 🔴 Очень сложный | 251 | 34 | 7.4 |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | 0 | 🔴 Очень сложный | 57 | 5 | 11.4 |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | 0 | 🔴 Очень сложный | 237 | 29 | 8.2 |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 0 | 🔴 Очень сложный | 31 | 4 | 7.8 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 0 | 🔴 Очень сложный | 64 | 4 | 16.0 |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 0 | 🔴 Очень сложный | 32 | 4 | 8.0 |
| `docs/02-anthropic-vacancies/122-глоссарий.md` | 0 | 🔴 Очень сложный | 1159 | 118 | 9.8 |
| `docs/02-anthropic-vacancies/123-portal-mcp-py.md` | 0 | 🔴 Очень сложный | 145 | 18 | 8.1 |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | 0 | 🔴 Очень сложный | 190 | 19 | 10.0 |
| `docs/02-anthropic-vacancies/126-установка.md` | 0 | 🔴 Очень сложный | 127 | 18 | 7.1 |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | 0 | 🔴 Очень сложный | 119 | 11 | 10.8 |
| `docs/02-anthropic-vacancies/128-доступные-инструменты.md` | 0 | 🔴 Очень сложный | 138 | 10 | 13.8 |
| `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` | 0 | 🔴 Очень сложный | 126 | 13 | 9.7 |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | 0 | 🔴 Очень сложный | 102 | 9 | 11.3 |
| `docs/02-anthropic-vacancies/130-отладка.md` | 0 | 🔴 Очень сложный | 172 | 17 | 10.1 |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | 0 | 🔴 Очень сложный | 101 | 8 | 12.6 |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | 0 | 🔴 Очень сложный | 84 | 8 | 10.5 |
| `docs/02-anthropic-vacancies/133-обратная-связь.md` | 0 | 🔴 Очень сложный | 3634 | 268 | 13.6 |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 0 | 🔴 Очень сложный | 70 | 10 | 7.0 |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | 0 | 🔴 Очень сложный | 162 | 12 | 13.5 |
| `docs/02-anthropic-vacancies/136-abstract.md` | 0 | 🔴 Очень сложный | 417 | 26 | 16.0 |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | 0 | 🔴 Очень сложный | 154 | 19 | 8.1 |
| `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` | 0 | 🔴 Очень сложный | 818 | 77 | 10.6 |
| `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` | 0 | 🔴 Очень сложный | 715 | 65 | 11.0 |
| `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` | 0 | 🔴 Очень сложный | 643 | 54 | 11.9 |
| `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` | 0 | 🔴 Очень сложный | 687 | 71 | 9.7 |
| `docs/02-anthropic-vacancies/144-7-open-questions.md` | 0 | 🔴 Очень сложный | 753 | 68 | 11.1 |
| `docs/02-anthropic-vacancies/145-8-call-to-action.md` | 0 | 🔴 Очень сложный | 730 | 87 | 8.4 |
| `docs/02-anthropic-vacancies/146-acknowledgments.md` | 0 | 🔴 Очень сложный | 248 | 22 | 11.3 |
| `docs/02-anthropic-vacancies/147-references.md` | 0 | 🔴 Очень сложный | 302 | 56 | 5.4 |
| `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` | 0 | 🔴 Очень сложный | 306 | 31 | 9.9 |
| `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` | 0 | 🔴 Очень сложный | 201 | 23 | 8.7 |
| `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` | 0 | 🔴 Очень сложный | 4405 | 253 | 17.4 |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 0 | 🔴 Очень сложный | 74 | 10 | 7.4 |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | 0 | 🔴 Очень сложный | 149 | 12 | 12.4 |
| `docs/02-anthropic-vacancies/153-executive-summary.md` | 0 | 🔴 Очень сложный | 370 | 25 | 14.8 |
| `docs/02-anthropic-vacancies/155-1-problem-statement.md` | 0 | 🔴 Очень сложный | 618 | 43 | 14.4 |
| `docs/02-anthropic-vacancies/156-2-target-populations.md` | 0 | 🔴 Очень сложный | 663 | 36 | 18.4 |
| `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` | 0 | 🔴 Очень сложный | 700 | 49 | 14.3 |
| `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` | 0 | 🔴 Очень сложный | 976 | 44 | 22.2 |
| `docs/02-anthropic-vacancies/159-5-economic-model.md` | 0 | 🔴 Очень сложный | 528 | 51 | 10.4 |
| `docs/02-anthropic-vacancies/16-history.md` | 0 | 🔴 Очень сложный | 31 | 6 | 5.2 |
| `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` | 0 | 🔴 Очень сложный | 554 | 52 | 10.7 |
| `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` | 0 | 🔴 Очень сложный | 600 | 32 | 18.8 |
| `docs/02-anthropic-vacancies/162-8-risk-analysis.md` | 0 | 🔴 Очень сложный | 632 | 33 | 19.2 |
| `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` | 0 | 🔴 Очень сложный | 610 | 34 | 17.9 |
| `docs/02-anthropic-vacancies/164-10-appendices.md` | 0 | 🔴 Очень сложный | 738 | 41 | 18.0 |
| `docs/02-anthropic-vacancies/165-closing.md` | 0 | 🔴 Очень сложный | 6089 | 463 | 13.2 |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | 0 | 🔴 Очень сложный | 196 | 16 | 12.2 |
| `docs/02-anthropic-vacancies/168-abstract.md` | 0 | 🔴 Очень сложный | 328 | 20 | 16.4 |
| `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` | 0 | 🔴 Очень сложный | 249 | 31 | 8.0 |
| `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` | 0 | 🔴 Очень сложный | 817 | 62 | 13.2 |
| `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` | 0 | 🔴 Очень сложный | 943 | 81 | 11.6 |
| `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` | 0 | 🔴 Очень сложный | 684 | 83 | 8.2 |
| `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` | 0 | 🔴 Очень сложный | 1593 | 178 | 8.9 |
| `docs/02-anthropic-vacancies/174-5-architectural-specification.md` | 0 | 🔴 Очень сложный | 624 | 67 | 9.3 |
| `docs/02-anthropic-vacancies/175-6-ethical-framework.md` | 0 | 🔴 Очень сложный | 590 | 52 | 11.3 |
| `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` | 0 | 🔴 Очень сложный | 461 | 32 | 14.4 |
| `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` | 0 | 🔴 Очень сложный | 616 | 47 | 13.1 |
| `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` | 0 | 🔴 Очень сложный | 552 | 34 | 16.2 |
| `docs/02-anthropic-vacancies/179-10-open-questions.md` | 0 | 🔴 Очень сложный | 406 | 47 | 8.6 |
| `docs/02-anthropic-vacancies/18-6-adapter-interface.md` | 0 | 🔴 Очень сложный | 288 | 33 | 8.7 |
| `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` | 0 | 🔴 Очень сложный | 432 | 49 | 8.8 |
| `docs/02-anthropic-vacancies/182-acknowledgments.md` | 0 | 🔴 Очень сложный | 193 | 18 | 10.7 |
| `docs/02-anthropic-vacancies/183-references.md` | 0 | 🔴 Очень сложный | 298 | 43 | 6.9 |
| `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` | 0 | 🔴 Очень сложный | 249 | 20 | 12.4 |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 0 | 🔴 Очень сложный | 74 | 11 | 6.7 |
| `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` | 0 | 🔴 Очень сложный | 1895 | 153 | 12.4 |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | 0 | 🔴 Очень сложный | 69 | 10 | 6.9 |
| `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` | 0 | 🔴 Очень сложный | 164 | 19 | 8.6 |
| `docs/02-anthropic-vacancies/189-аннотация.md` | 0 | 🔴 Очень сложный | 278 | 13 | 21.4 |
| `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` | 0 | 🔴 Очень сложный | 144 | 17 | 8.5 |
| `docs/02-anthropic-vacancies/190-содержание.md` | 0 | 🔴 Очень сложный | 95 | 20 | 4.8 |
| `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | 0 | 🔴 Очень сложный | 684 | 59 | 11.6 |
| `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | 0 | 🔴 Очень сложный | 811 | 76 | 10.7 |
| `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` | 0 | 🔴 Очень сложный | 620 | 84 | 7.4 |
| `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` | 0 | 🔴 Очень сложный | 1505 | 178 | 8.5 |
| `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` | 0 | 🔴 Очень сложный | 599 | 68 | 8.8 |
| `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` | 0 | 🔴 Очень сложный | 529 | 49 | 10.8 |
| `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` | 0 | 🔴 Очень сложный | 389 | 26 | 15.0 |
| `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` | 0 | 🔴 Очень сложный | 598 | 50 | 12.0 |
| `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` | 0 | 🔴 Очень сложный | 530 | 37 | 14.3 |
| `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` | 0 | 🔴 Очень сложный | 239 | 30 | 8.0 |
| `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` | 0 | 🔴 Очень сложный | 362 | 45 | 8.0 |
| `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` | 0 | 🔴 Очень сложный | 422 | 53 | 8.0 |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | 0 | 🔴 Очень сложный | 149 | 13 | 11.5 |
| `docs/02-anthropic-vacancies/203-благодарности.md` | 0 | 🔴 Очень сложный | 160 | 13 | 12.3 |
| `docs/02-anthropic-vacancies/204-ссылки.md` | 0 | 🔴 Очень сложный | 254 | 46 | 5.5 |
| `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` | 0 | 🔴 Очень сложный | 203 | 22 | 9.2 |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 0 | 🔴 Очень сложный | 75 | 11 | 6.8 |
| `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` | 0 | 🔴 Очень сложный | 2295 | 156 | 14.7 |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | 0 | 🔴 Очень сложный | 71 | 10 | 7.1 |
| `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` | 0 | 🔴 Очень сложный | 192 | 17 | 11.3 |
| `docs/02-anthropic-vacancies/21-9-query-flow.md` | 0 | 🔴 Очень сложный | 165 | 30 | 5.5 |
| `docs/02-anthropic-vacancies/210-abstract.md` | 0 | 🔴 Очень сложный | 352 | 17 | 20.7 |
| `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | 0 | 🔴 Очень сложный | 857 | 99 | 8.7 |
| `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` | 0 | 🔴 Очень сложный | 831 | 102 | 8.1 |
| `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | 0 | 🔴 Очень сложный | 817 | 66 | 12.4 |
| `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` | 0 | 🔴 Очень сложный | 886 | 105 | 8.4 |
| `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` | 0 | 🔴 Очень сложный | 729 | 69 | 10.6 |
| `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` | 0 | 🔴 Очень сложный | 1169 | 154 | 7.6 |
| `docs/02-anthropic-vacancies/218-7-application-domains.md` | 0 | 🔴 Очень сложный | 743 | 105 | 7.1 |
| `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` | 0 | 🔴 Очень сложный | 861 | 64 | 13.5 |
| `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` | 0 | 🔴 Очень сложный | 120 | 16 | 7.5 |
| `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` | 0 | 🔴 Очень сложный | 636 | 68 | 9.4 |
| `docs/02-anthropic-vacancies/221-10-open-questions.md` | 0 | 🔴 Очень сложный | 429 | 57 | 7.5 |
| `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` | 0 | 🔴 Очень сложный | 365 | 44 | 8.3 |
| `docs/02-anthropic-vacancies/223-12-closing.md` | 0 | 🔴 Очень сложный | 412 | 32 | 12.9 |
| `docs/02-anthropic-vacancies/225-references.md` | 0 | 🔴 Очень сложный | 291 | 47 | 6.2 |
| `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | 0 | 🔴 Очень сложный | 363 | 10 | 36.3 |
| `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` | 0 | 🔴 Очень сложный | 334 | 12 | 27.8 |
| `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` | 0 | 🔴 Очень сложный | 1373 | 96 | 14.3 |
| `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` | 0 | 🔴 Очень сложный | 156 | 16 | 9.8 |
| `docs/02-anthropic-vacancies/23-11-security-considerations.md` | 0 | 🔴 Очень сложный | 225 | 25 | 9.0 |
| `docs/02-anthropic-vacancies/230-аннотация.md` | 0 | 🔴 Очень сложный | 305 | 19 | 16.1 |
| `docs/02-anthropic-vacancies/231-содержание.md` | 0 | 🔴 Очень сложный | 110 | 22 | 5.0 |
| `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | 0 | 🔴 Очень сложный | 774 | 104 | 7.4 |
| `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` | 0 | 🔴 Очень сложный | 709 | 101 | 7.0 |
| `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | 0 | 🔴 Очень сложный | 680 | 63 | 10.8 |
| `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` | 0 | 🔴 Очень сложный | 810 | 107 | 7.6 |
| `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` | 0 | 🔴 Очень сложный | 642 | 64 | 10.0 |
| `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` | 0 | 🔴 Очень сложный | 1104 | 155 | 7.1 |
| `docs/02-anthropic-vacancies/238-7-области-применения.md` | 0 | 🔴 Очень сложный | 678 | 101 | 6.7 |
| `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` | 0 | 🔴 Очень сложный | 820 | 60 | 13.7 |
| `docs/02-anthropic-vacancies/24-12-versioning-policy.md` | 0 | 🔴 Очень сложный | 174 | 25 | 7.0 |
| `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` | 0 | 🔴 Очень сложный | 687 | 82 | 8.4 |
| `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` | 0 | 🔴 Очень сложный | 408 | 55 | 7.4 |
| `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` | 0 | 🔴 Очень сложный | 345 | 43 | 8.0 |
| `docs/02-anthropic-vacancies/243-12-заключение.md` | 0 | 🔴 Очень сложный | 330 | 29 | 11.4 |
| `docs/02-anthropic-vacancies/244-благодарности.md` | 0 | 🔴 Очень сложный | 133 | 16 | 8.3 |
| `docs/02-anthropic-vacancies/245-ссылки.md` | 0 | 🔴 Очень сложный | 259 | 48 | 5.4 |
| `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | 0 | 🔴 Очень сложный | 280 | 6 | 46.7 |
| `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` | 0 | 🔴 Очень сложный | 289 | 9 | 32.1 |
| `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | 0 | 🔴 Очень сложный | 3018 | 250 | 12.1 |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | 0 | 🔴 Очень сложный | 70 | 10 | 7.0 |
| `docs/02-anthropic-vacancies/25-13-reference-implementation.md` | 0 | 🔴 Очень сложный | 119 | 17 | 7.0 |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 0 | 🔴 Очень сложный | 18 | 1 | 18.0 |
| `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` | 0 | 🔴 Очень сложный | 187 | 18 | 10.4 |
| `docs/02-anthropic-vacancies/252-abstract.md` | 0 | 🔴 Очень сложный | 352 | 17 | 20.7 |
| `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` | 0 | 🔴 Очень сложный | 698 | 54 | 12.9 |
| `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` | 0 | 🔴 Очень сложный | 939 | 87 | 10.8 |
| `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` | 0 | 🔴 Очень сложный | 824 | 76 | 10.8 |
| `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` | 0 | 🔴 Очень сложный | 748 | 64 | 11.7 |
| `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` | 0 | 🔴 Очень сложный | 794 | 76 | 10.4 |
| `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` | 0 | 🔴 Очень сложный | 207 | 11 | 18.8 |
| `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` | 0 | 🔴 Очень сложный | 804 | 66 | 12.2 |
| `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` | 0 | 🔴 Очень сложный | 1018 | 56 | 18.2 |
| `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` | 0 | 🔴 Очень сложный | 763 | 59 | 12.9 |
| `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` | 0 | 🔴 Очень сложный | 813 | 51 | 15.9 |
| `docs/02-anthropic-vacancies/264-11-open-questions.md` | 0 | 🔴 Очень сложный | 611 | 65 | 9.4 |
| `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` | 0 | 🔴 Очень сложный | 414 | 36 | 11.5 |
| `docs/02-anthropic-vacancies/266-13-closing.md` | 0 | 🔴 Очень сложный | 435 | 30 | 14.5 |
| `docs/02-anthropic-vacancies/267-acknowledgments.md` | 0 | 🔴 Очень сложный | 313 | 24 | 13.0 |
| `docs/02-anthropic-vacancies/268-references.md` | 0 | 🔴 Очень сложный | 378 | 60 | 6.3 |
| `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | 0 | 🔴 Очень сложный | 258 | 17 | 15.2 |
| `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` | 0 | 🔴 Очень сложный | 165 | 22 | 7.5 |
| `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` | 0 | 🔴 Очень сложный | 195 | 14 | 13.9 |
| `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` | 0 | 🔴 Очень сложный | 236 | 18 | 13.1 |
| `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` | 0 | 🔴 Очень сложный | 3387 | 258 | 13.1 |
| `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` | 0 | 🔴 Очень сложный | 142 | 14 | 10.1 |
| `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` | 0 | 🔴 Очень сложный | 231 | 20 | 11.6 |
| `docs/02-anthropic-vacancies/285-closing.md` | 0 | 🔴 Очень сложный | 294 | 23 | 12.8 |
| `docs/02-anthropic-vacancies/287-references.md` | 0 | 🔴 Очень сложный | 302 | 22 | 13.7 |
| `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` | 0 | 🔴 Очень сложный | 852 | 85 | 10.0 |
| `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` | 0 | 🔴 Очень сложный | 202 | 21 | 9.6 |
| `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` | 0 | 🔴 Очень сложный | 291 | 29 | 10.0 |
| `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` | 0 | 🔴 Очень сложный | 347 | 34 | 10.2 |
| `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` | 0 | 🔴 Очень сложный | 398 | 40 | 9.9 |
| `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` | 0 | 🔴 Очень сложный | 279 | 35 | 8.0 |
| `docs/02-anthropic-vacancies/294-существующие-приближения.md` | 0 | 🔴 Очень сложный | 548 | 38 | 14.4 |
| `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` | 0 | 🔴 Очень сложный | 733 | 82 | 8.9 |
| `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` | 0 | 🔴 Очень сложный | 341 | 31 | 11.0 |
| `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` | 0 | 🔴 Очень сложный | 308 | 43 | 7.2 |
| `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` | 0 | 🔴 Очень сложный | 193 | 28 | 6.9 |
| `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` | 0 | 🔴 Очень сложный | 312 | 43 | 7.3 |
| `docs/02-anthropic-vacancies/300-заключение.md` | 0 | 🔴 Очень сложный | 225 | 23 | 9.8 |
| `docs/02-anthropic-vacancies/301-благодарности.md` | 0 | 🔴 Очень сложный | 173 | 19 | 9.1 |
| `docs/02-anthropic-vacancies/302-ссылки.md` | 0 | 🔴 Очень сложный | 263 | 24 | 11.0 |
| `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` | 0 | 🔴 Очень сложный | 1770 | 116 | 15.3 |
| `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` | 0 | 🔴 Очень сложный | 136 | 14 | 9.7 |
| `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | 0 | 🔴 Очень сложный | 114 | 12 | 9.5 |
| `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` | 0 | 🔴 Очень сложный | 307 | 24 | 12.8 |
| `docs/02-anthropic-vacancies/307-abstract.md` | 0 | 🔴 Очень сложный | 342 | 25 | 13.7 |
| `docs/02-anthropic-vacancies/31-content-overview.md` | 0 | 🔴 Очень сложный | 27 | 4 | 6.8 |
| `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` | 0 | 🔴 Очень сложный | 603 | 57 | 10.6 |
| `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` | 0 | 🔴 Очень сложный | 754 | 68 | 11.1 |
| `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` | 0 | 🔴 Очень сложный | 677 | 85 | 8.0 |
| `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` | 0 | 🔴 Очень сложный | 783 | 83 | 9.4 |
| `docs/02-anthropic-vacancies/319-acknowledgments.md` | 0 | 🔴 Очень сложный | 387 | 43 | 9.0 |
| `docs/02-anthropic-vacancies/320-references.md` | 0.0 | 🔴 Очень сложный | 164 | 27 | 6.1 |
| `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` | 0 | 🔴 Очень сложный | 118 | 10 | 11.8 |
| `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` | 0 | 🔴 Очень сложный | 1108 | 119 | 9.3 |
| `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | 0 | 🔴 Очень сложный | 233 | 24 | 9.7 |
| `docs/02-anthropic-vacancies/325-аннотация.md` | 0 | 🔴 Очень сложный | 322 | 29 | 11.1 |
| `docs/02-anthropic-vacancies/326-содержание.md` | 0 | 🔴 Очень сложный | 107 | 19 | 5.6 |
| `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` | 0 | 🔴 Очень сложный | 639 | 78 | 8.2 |
| `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` | 0 | 🔴 Очень сложный | 883 | 87 | 10.1 |
| `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` | 0 | 🔴 Очень сложный | 856 | 72 | 11.9 |
| `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` | 0 | 🔴 Очень сложный | 572 | 54 | 10.6 |
| `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` | 0 | 🔴 Очень сложный | 725 | 76 | 9.5 |
| `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` | 0 | 🔴 Очень сложный | 506 | 48 | 10.5 |
| `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` | 0 | 🔴 Очень сложный | 365 | 45 | 8.1 |
| `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` | 0 | 🔴 Очень сложный | 645 | 63 | 10.2 |
| `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` | 0 | 🔴 Очень сложный | 590 | 77 | 7.7 |
| `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` | 0 | 🔴 Очень сложный | 677 | 77 | 8.8 |
| `docs/02-anthropic-vacancies/337-благодарности.md` | 0 | 🔴 Очень сложный | 364 | 43 | 8.5 |
| `docs/02-anthropic-vacancies/338-ссылки.md` | 0 | 🔴 Очень сложный | 154 | 27 | 5.7 |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | 0 | 🔴 Очень сложный | 33 | 2 | 16.5 |
| `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` | 0 | 🔴 Очень сложный | 592 | 61 | 9.7 |
| `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | 0 | 🔴 Очень сложный | 155 | 10 | 15.5 |
| `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` | 0 | 🔴 Очень сложный | 3391 | 153 | 22.2 |
| `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` | 0 | 🔴 Очень сложный | 9360 | 465 | 20.1 |
| `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` | 0 | 🔴 Очень сложный | 4773 | 264 | 18.1 |
| `docs/02-anthropic-vacancies/345-кто-ты.md` | 0 | 🔴 Очень сложный | 169 | 14 | 12.1 |
| `docs/02-anthropic-vacancies/346-твоё-происхождение.md` | 0 | 🔴 Очень сложный | 159 | 18 | 8.8 |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 0 | 🔴 Очень сложный | 96 | 5 | 19.2 |
| `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` | 0 | 🔴 Очень сложный | 49 | 3 | 16.3 |
| `docs/02-anthropic-vacancies/349-твоя-личность.md` | 0 | 🔴 Очень сложный | 172 | 23 | 7.5 |
| `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` | 0 | 🔴 Очень сложный | 140 | 5 | 28.0 |
| `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` | 0 | 🔴 Очень сложный | 146 | 10 | 14.6 |
| `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` | 0 | 🔴 Очень сложный | 321 | 34 | 9.4 |
| `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` | 0 | 🔴 Очень сложный | 224 | 23 | 9.7 |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 0 | 🔴 Очень сложный | 159 | 16 | 9.9 |
| `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` | 0 | 🔴 Очень сложный | 108 | 4 | 27.0 |
| `docs/02-anthropic-vacancies/36-essence.md` | 0 | 🔴 Очень сложный | 144 | 17 | 8.5 |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 0 | 🔴 Очень сложный | 68 | 3 | 22.7 |
| `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` | 0 | 🔴 Очень сложный | 134 | 13 | 10.3 |
| `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` | 0 | 🔴 Очень сложный | 1253 | 86 | 14.6 |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | 0 | 🔴 Очень сложный | 3609 | 261 | 13.8 |
| `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 0 | 🔴 Очень сложный | 685 | 42 | 16.3 |
| `docs/02-anthropic-vacancies/37-native-format.md` | 0 | 🔴 Очень сложный | 135 | 12 | 11.2 |
| `docs/02-anthropic-vacancies/38-content-overview.md` | 0 | 🔴 Очень сложный | 85 | 6 | 14.2 |
| `docs/02-anthropic-vacancies/39-angle-perspective.md` | 0 | 🔴 Очень сложный | 117 | 15 | 7.8 |
| `docs/02-anthropic-vacancies/40-bridges.md` | 0 | 🔴 Очень сложный | 160 | 22 | 7.3 |
| `docs/02-anthropic-vacancies/41-compatibility-level.md` | 0 | 🔴 Очень сложный | 92 | 10 | 9.2 |
| `docs/02-anthropic-vacancies/42-author-contact.md` | 0 | 🔴 Очень сложный | 98 | 13 | 7.5 |
| `docs/02-anthropic-vacancies/43-history.md` | 0 | 🔴 Очень сложный | 109 | 16 | 6.8 |
| `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` | 0 | 🔴 Очень сложный | 140 | 13 | 10.8 |
| `docs/02-anthropic-vacancies/46-essence.md` | 0 | 🔴 Очень сложный | 149 | 22 | 6.8 |
| `docs/02-anthropic-vacancies/47-native-format.md` | 0 | 🔴 Очень сложный | 90 | 12 | 7.5 |
| `docs/02-anthropic-vacancies/48-content-overview.md` | 0 | 🔴 Очень сложный | 148 | 20 | 7.4 |
| `docs/02-anthropic-vacancies/49-angle-perspective.md` | 0 | 🔴 Очень сложный | 124 | 14 | 8.9 |
| `docs/02-anthropic-vacancies/50-bridges.md` | 0 | 🔴 Очень сложный | 144 | 20 | 7.2 |
| `docs/02-anthropic-vacancies/51-compatibility-level.md` | 0 | 🔴 Очень сложный | 91 | 10 | 9.1 |
| `docs/02-anthropic-vacancies/52-author-contact.md` | 0 | 🔴 Очень сложный | 128 | 14 | 9.1 |
| `docs/02-anthropic-vacancies/53-history.md` | 0 | 🔴 Очень сложный | 127 | 10 | 12.7 |
| `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` | 0 | 🔴 Очень сложный | 142 | 16 | 8.9 |
| `docs/02-anthropic-vacancies/56-essence.md` | 0 | 🔴 Очень сложный | 149 | 17 | 8.8 |
| `docs/02-anthropic-vacancies/57-native-format.md` | 0 | 🔴 Очень сложный | 90 | 13 | 6.9 |
| `docs/02-anthropic-vacancies/58-content-overview.md` | 0 | 🔴 Очень сложный | 107 | 11 | 9.7 |
| `docs/02-anthropic-vacancies/59-angle-perspective.md` | 0 | 🔴 Очень сложный | 121 | 13 | 9.3 |
| `docs/02-anthropic-vacancies/60-bridges.md` | 0 | 🔴 Очень сложный | 128 | 22 | 5.8 |
| `docs/02-anthropic-vacancies/61-compatibility-level.md` | 0 | 🔴 Очень сложный | 90 | 10 | 9.0 |
| `docs/02-anthropic-vacancies/62-author-contact.md` | 0 | 🔴 Очень сложный | 94 | 12 | 7.8 |
| `docs/02-anthropic-vacancies/63-history.md` | 0 | 🔴 Очень сложный | 120 | 9 | 13.3 |
| `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` | 0 | 🔴 Очень сложный | 569 | 56 | 10.2 |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | 0 | 🔴 Очень сложный | 504 | 50 | 10.1 |
| `docs/02-anthropic-vacancies/68-about.md` | 0 | 🔴 Очень сложный | 706 | 63 | 11.2 |
| `docs/02-anthropic-vacancies/69-section.md` | 0 | 🔴 Очень сложный | 1048 | 78 | 13.4 |
| `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` | 0 | 🔴 Очень сложный | 104 | 10 | 10.4 |
| `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` | 0 | 🔴 Очень сложный | 130 | 6 | 21.7 |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | 0 | 🔴 Очень сложный | 686 | 63 | 10.9 |
| `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` | 0 | 🔴 Очень сложный | 160 | 17 | 9.4 |
| `docs/02-anthropic-vacancies/74-abstract.md` | 0 | 🔴 Очень сложный | 233 | 29 | 8.0 |
| `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` | 0 | 🔴 Очень сложный | 137 | 21 | 6.5 |
| `docs/02-anthropic-vacancies/76-1-introduction.md` | 0 | 🔴 Очень сложный | 412 | 39 | 10.6 |
| `docs/02-anthropic-vacancies/77-2-terminology.md` | 0 | 🔴 Очень сложный | 347 | 52 | 6.7 |
| `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` | 0 | 🔴 Очень сложный | 415 | 57 | 7.3 |
| `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` | 0 | 🔴 Очень сложный | 288 | 38 | 7.6 |
| `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` | 0 | 🔴 Очень сложный | 295 | 33 | 8.9 |
| `docs/02-anthropic-vacancies/81-6-adapter-interface.md` | 0 | 🔴 Очень сложный | 262 | 31 | 8.5 |
| `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` | 0 | 🔴 Очень сложный | 244 | 35 | 7.0 |
| `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` | 0 | 🔴 Очень сложный | 317 | 34 | 9.3 |
| `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` | 0 | 🔴 Очень сложный | 218 | 28 | 7.8 |
| `docs/02-anthropic-vacancies/85-10-query-flow.md` | 0 | 🔴 Очень сложный | 223 | 36 | 6.2 |
| `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` | 0 | 🔴 Очень сложный | 126 | 21 | 6.0 |
| `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | 0 | 🔴 Очень сложный | 480 | 77 | 6.2 |
| `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | 0 | 🔴 Очень сложный | 316 | 40 | 7.9 |
| `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` | 0 | 🔴 Очень сложный | 140 | 18 | 7.8 |
| `docs/02-anthropic-vacancies/90-15-security-considerations.md` | 0 | 🔴 Очень сложный | 340 | 36 | 9.4 |
| `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` | 0 | 🔴 Очень сложный | 133 | 17 | 7.8 |
| `docs/02-anthropic-vacancies/92-17-versioning-policy.md` | 0 | 🔴 Очень сложный | 242 | 35 | 6.9 |
| `docs/02-anthropic-vacancies/93-18-reference-implementation.md` | 0 | 🔴 Очень сложный | 158 | 19 | 8.3 |
| `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` | 0 | 🔴 Очень сложный | 219 | 15 | 14.6 |
| `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` | 0 | 🔴 Очень сложный | 200 | 19 | 10.5 |
| `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | 0 | 🔴 Очень сложный | 169 | 18 | 9.4 |
| `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` | 0 | 🔴 Очень сложный | 224 | 27 | 8.3 |
| `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | 0 | 🔴 Очень сложный | 182 | 24 | 7.6 |
| `docs/02-anthropic-vacancies/QA.md` | 0 | 🔴 Очень сложный | 959 | 91 | 10.5 |
| `docs/03-technology-combinations/01-agent-routing.md` | 0 | 🔴 Очень сложный | 261 | 22 | 11.9 |
| `docs/03-technology-combinations/02-knowledge-graphs.md` | 0 | 🔴 Очень сложный | 710 | 50 | 14.2 |
| `docs/03-technology-combinations/03-local-first.md` | 0 | 🔴 Очень сложный | 379 | 35 | 10.8 |
| `docs/03-technology-combinations/04-sozialrecht-domain.md` | 0 | 🔴 Очень сложный | 191 | 15 | 12.7 |
| `docs/03-technology-combinations/05-benchmarks.md` | 0 | 🔴 Очень сложный | 745 | 34 | 21.9 |
| `docs/03-technology-combinations/QA.md` | 0 | 🔴 Очень сложный | 242 | 37 | 6.5 |
| `docs/04-ai-collaborations/00-intro.md` | 0 | 🔴 Очень сложный | 10736 | 687 | 15.6 |
| `docs/04-ai-collaborations/01-executive-summary.md` | 0 | 🔴 Очень сложный | 648 | 43 | 15.1 |
| `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` | 0 | 🔴 Очень сложный | 369 | 32 | 11.5 |
| `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 0 | 🔴 Очень сложный | 1542 | 116 | 13.3 |
| `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` | 0 | 🔴 Очень сложный | 1322 | 80 | 16.5 |
| `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 0 | 🔴 Очень сложный | 1068 | 66 | 16.2 |
| `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 0 | 🔴 Очень сложный | 829 | 50 | 16.6 |
| `docs/04-ai-collaborations/07-выводы.md` | 0 | 🔴 Очень сложный | 461 | 42 | 11.0 |
| `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | 0 | 🔴 Очень сложный | 453 | 34 | 13.3 |
| `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 0 | 🔴 Очень сложный | 839 | 48 | 17.5 |
| `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | 0 | 🔴 Очень сложный | 940 | 62 | 15.2 |
| `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 0 | 🔴 Очень сложный | 858 | 55 | 15.6 |
| `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | 0 | 🔴 Очень сложный | 712 | 49 | 14.5 |
| `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 0 | 🔴 Очень сложный | 846 | 64 | 13.2 |
| `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 0 | 🔴 Очень сложный | 3176 | 224 | 14.2 |
| `docs/04-ai-collaborations/QA.md` | 0 | 🔴 Очень сложный | 746 | 66 | 11.3 |
| `docs/04-ai-collaborations/README.md` | 0 | 🔴 Очень сложный | 155 | 30 | 5.2 |
| `docs/05-habr-projects/01-synthesis.md` | 0 | 🔴 Очень сложный | 111 | 7 | 15.9 |
| `docs/05-habr-projects/02-collaboration-partners.md` | 0 | 🔴 Очень сложный | 204 | 8 | 25.5 |
| `docs/05-habr-projects/QA.md` | 0 | 🔴 Очень сложный | 401 | 48 | 8.4 |
| `docs/05-habr-projects/README.md` | 0 | 🔴 Очень сложный | 28 | 5 | 5.6 |
| `docs/05-habr-projects/knowledge/wikontic.md` | 0 | 🔴 Очень сложный | 149 | 12 | 12.4 |
| `docs/05-habr-projects/memory/memnet.md` | 0 | 🔴 Очень сложный | 6744 | 453 | 14.9 |
| `docs/05-habr-projects/memory/ngt-memory.md` | 0 | 🔴 Очень сложный | 292 | 18 | 16.2 |
| `docs/05-habr-projects/memory/yodoca.md` | 0 | 🔴 Очень сложный | 169 | 14 | 12.1 |
| `docs/ABBREVIATIONS.md` | 0 | 🔴 Очень сложный | 863 | 5 | 172.6 |
| `docs/ACTION_ITEMS.md` | 0 | 🔴 Очень сложный | 3880 | 231 | 16.8 |
| `docs/ALERTS.md` | 0 | 🔴 Очень сложный | 23 | 2 | 11.5 |
| `docs/AUTHORS.md` | 0 | 🔴 Очень сложный | 40 | 2 | 20.0 |
| `docs/AUTOFILLED.md` | 0 | 🔴 Очень сложный | 128 | 26 | 4.9 |
| `docs/BACKLINKS.md` | 0 | 🔴 Очень сложный | 58 | 6 | 9.7 |
| `docs/BROKEN_LINKS.md` | 0 | 🔴 Очень сложный | 417 | 23 | 18.1 |
| `docs/CHANGELOG.md` | 0 | 🔴 Очень сложный | 216 | 19 | 11.4 |
| `docs/CHANGELOG_AUTO.md` | 0 | 🔴 Очень сложный | 251 | 13 | 19.3 |
| `docs/CITATION_INDEX.md` | 0 | 🔴 Очень сложный | 99 | 10 | 9.9 |
| `docs/CLUSTERS.md` | 0 | 🔴 Очень сложный | 1004 | 15 | 66.9 |
| `docs/COMPLEXITY.md` | 0 | 🔴 Очень сложный | 96 | 31 | 3.1 |
| `docs/COMPONENT_MATRIX.md` | 0 | 🔴 Очень сложный | 251 | 11 | 22.8 |
| `docs/CONCEPTS.md` | 0 | 🔴 Очень сложный | 13047 | 675 | 19.3 |
| `docs/CONTACTS.md` | 0 | 🔴 Очень сложный | 280 | 14 | 20.0 |
| `docs/CONTACT_PRIORITY.md` | 0 | 🔴 Очень сложный | 256 | 14 | 18.3 |
| `docs/CONTENT_GAPS.md` | 0 | 🔴 Очень сложный | 244 | 30 | 8.1 |
| `docs/CONTRADICTIONS.md` | 0 | 🔴 Очень сложный | 1258 | 190 | 6.6 |
| `docs/COST.md` | 0 | 🔴 Очень сложный | 355 | 15 | 23.7 |
| `docs/COVERAGE.md` | 0 | 🔴 Очень сложный | 193 | 9 | 21.4 |
| `docs/CROSSREFS.md` | 0 | 🔴 Очень сложный | 242 | 6 | 40.3 |
| `docs/CROSS_SECTION.md` | 0 | 🔴 Очень сложный | 95 | 49 | 1.9 |
| `docs/DECISIONS.md` | 0 | 🔴 Очень сложный | 1342 | 83 | 16.2 |
| `docs/DENSITY.md` | 0 | 🔴 Очень сложный | 107 | 5 | 21.4 |
| `docs/DEPENDABOT.md` | 0 | 🔴 Очень сложный | 50 | 4 | 12.5 |
| `docs/DEPENDENCY_MAP.md` | 0 | 🔴 Очень сложный | 78 | 7 | 11.1 |
| `docs/DIGEST.md` | 0 | 🔴 Очень сложный | 282 | 12 | 23.5 |
| `docs/DIGEST_WEEKLY.md` | 0 | 🔴 Очень сложный | 25 | 1 | 25.0 |
| `docs/DUPLICATES.md` | 0 | 🔴 Очень сложный | 2272 | 157 | 14.5 |
| `docs/ENTITIES.md` | 0 | 🔴 Очень сложный | 143 | 1 | 143.0 |
| `docs/FAQ.md` | 0 | 🔴 Очень сложный | 1571 | 181 | 8.7 |
| `docs/FOOTNOTES.md` | 0 | 🔴 Очень сложный | 230 | 12 | 19.2 |
| `docs/GITHUB_ISSUES.md` | 0 | 🔴 Очень сложный | 511 | 13 | 39.3 |
| `docs/GLOSSARY.md` | 0 | 🔴 Очень сложный | 59 | 2 | 29.5 |
| `docs/GRAPH.md` | 0 | 🔴 Очень сложный | 130 | 7 | 18.6 |
| `docs/HEADING_AUDIT.md` | 0 | 🔴 Очень сложный | 16130 | 1095 | 14.7 |
| `docs/HEALTH.md` | 0 | 🔴 Очень сложный | 101 | 2 | 50.5 |
| `docs/HEATMAP.md` | 0 | 🔴 Очень сложный | 106 | 33 | 3.2 |
| `docs/INDEX.md` | 0 | 🔴 Очень сложный | 489 | 63 | 7.8 |
| `docs/KNOWLEDGE_MAP.md` | 0 | 🔴 Очень сложный | 195 | 19 | 10.3 |
| `docs/KPI.md` | 0 | 🔴 Очень сложный | 1042 | 117 | 8.9 |
| `docs/KPI_HISTORY.md` | 0 | 🔴 Очень сложный | 41 | 3 | 13.7 |
| `docs/LLM_SUMMARIES.md` | 0 | 🔴 Очень сложный | 177 | 35 | 5.1 |
| `docs/MINDMAP.md` | 0 | 🔴 Очень сложный | 154 | 7 | 22.0 |
| `docs/MISSING.md` | 0 | 🔴 Очень сложный | 98 | 2 | 49.0 |
| `docs/NARRATIVE.md` | 0 | 🔴 Очень сложный | 1100 | 71 | 15.5 |
| `docs/NETWORK.md` | 0 | 🔴 Очень сложный | 294 | 16 | 18.4 |
| `docs/ONBOARDING.md` | 0 | 🔴 Очень сложный | 291 | 29 | 10.0 |
| `docs/ORPHANS.md` | 0 | 🔴 Очень сложный | 63 | 9 | 7.0 |
| `docs/OUTLINE.md` | 0 | 🔴 Очень сложный | 49495 | 4083 | 12.1 |
| `docs/PARAGRAPH_QUALITY.md` | 0 | 🔴 Очень сложный | 14556 | 564 | 25.8 |
| `docs/PASSIVE_VOICE.md` | 0 | 🔴 Очень сложный | 152 | 13 | 11.7 |
| `docs/PROGRESS.md` | 0 | 🔴 Очень сложный | 172 | 17 | 10.1 |
| `docs/QA.md` | 0 | 🔴 Очень сложный | 1857 | 197 | 9.4 |
| `docs/QUESTIONS.md` | 0 | 🔴 Очень сложный | 1648 | 128 | 12.9 |
| `docs/READING_LIST.md` | 0 | 🔴 Очень сложный | 161 | 23 | 7.0 |
| `docs/READING_ORDER.md` | 0 | 🔴 Очень сложный | 4801 | 615 | 7.8 |
| `docs/READING_TIME.md` | 0 | 🔴 Очень сложный | 2294 | 4 | 573.5 |
| `docs/REPORT.md` | 0 | 🔴 Очень сложный | 339 | 27 | 12.6 |
| `docs/RISK_REGISTER.md` | 0 | 🔴 Очень сложный | 595 | 39 | 15.3 |
| `docs/SCHEDULE.md` | 0 | 🔴 Очень сложный | 226 | 11 | 20.5 |
| `docs/SCORING.md` | 0 | 🔴 Очень сложный | 296 | 14 | 21.1 |
| `docs/SEARCH_RESULTS.md` | 0 | 🔴 Очень сложный | 10 | 6 | 1.7 |
| `docs/SEE_ALSO.md` | 0 | 🔴 Очень сложный | 199 | 13 | 15.3 |
| `docs/SENTIMENT.md` | 0 | 🔴 Очень сложный | 98 | 37 | 2.6 |
| `docs/SIMILAR.md` | 0 | 🔴 Очень сложный | 45 | 29 | 1.6 |
| `docs/SIMILAR_PASSAGES.md` | 0 | 🔴 Очень сложный | 1186 | 185 | 6.4 |
| `docs/SITEMAP.md` | 0 | 🔴 Очень сложный | 1552 | 234 | 6.6 |
| `docs/SOURCE_MAP.md` | 0 | 🔴 Очень сложный | 76 | 5 | 15.2 |
| `docs/SPELLCHECK.md` | 0 | 🔴 Очень сложный | 13 | 1 | 13.0 |
| `docs/STATS.md` | 0 | 🔴 Очень сложный | 176 | 4 | 44.0 |
| `docs/SUMMARIES.md` | 0 | 🔴 Очень сложный | 4101 | 294 | 13.9 |
| `docs/TAGS.md` | 0 | 🔴 Очень сложный | 43 | 10 | 4.3 |
| `docs/TECH_RADAR.md` | 0 | 🔴 Очень сложный | 330 | 22 | 15.0 |
| `docs/TIMELINE.md` | 0 | 🔴 Очень сложный | 1659 | 207 | 8.0 |
| `docs/VALIDATION.md` | 0 | 🔴 Очень сложный | 248 | 1 | 248.0 |
| `docs/WORD_CLOUD.md` | 0 | 🔴 Очень сложный | 84 | 9 | 9.3 |
| `docs/WORD_FREQ.md` | 0 | 🔴 Очень сложный | 656 | 4 | 164.0 |
| `docs/ai-collaborations/README.md` | 0 | 🔴 Очень сложный | 33 | 3 | 11.0 |
| `docs/ai-collaborations/candidates/01-three-key-candidates.md` | 0 | 🔴 Очень сложный | 300 | 20 | 15.0 |
| `docs/ai-collaborations/candidates/02-related-projects-context.md` | 0 | 🔴 Очень сложный | 202 | 14 | 14.4 |
| `docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md` | 0 | 🔴 Очень сложный | 252 | 14 | 18.0 |
| `docs/ai-collaborations/channels/README.md` | 0 | 🔴 Очень сложный | 19 | 2 | 9.5 |
| `docs/ai-collaborations/continuation/01-shared-memory-between-agents.md` | 0 | 🔴 Очень сложный | 409 | 27 | 15.1 |
| `docs/ai-collaborations/continuation/02-agentops-trace-envelope.md` | 0 | 🔴 Очень сложный | 377 | 28 | 13.5 |
| `docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md` | 0 | 🔴 Очень сложный | 349 | 22 | 15.9 |
| `docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md` | 0 | 🔴 Очень сложный | 258 | 21 | 12.3 |
| `docs/ai-collaborations/continuation/05-roadmap-6-12-months.md` | 0 | 🔴 Очень сложный | 308 | 22 | 14.0 |
| `docs/ai-collaborations/continuation/06-metrics-tree.md` | 0 | 🔴 Очень сложный | 198 | 12 | 16.5 |
| `docs/ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md` | 0 | 🔴 Очень сложный | 442 | 31 | 14.3 |
| `docs/ai-collaborations/continuation/08-commercialization-three-paths.md` | 0 | 🔴 Очень сложный | 267 | 19 | 14.1 |
| `docs/ai-collaborations/continuation/09-do-not-glue.md` | 0 | 🔴 Очень сложный | 242 | 20 | 12.1 |
| `docs/ai-collaborations/continuation/10-architecture-rfc.md` | 0 | 🔴 Очень сложный | 175 | 19 | 9.2 |
| `docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md` | 0 | 🔴 Очень сложный | 386 | 21 | 18.4 |
| `docs/ai-collaborations/ensembles/2-distributed-agent-workshop.md` | 0 | 🔴 Очень сложный | 384 | 21 | 18.3 |
| `docs/ai-collaborations/ensembles/3-forensic-rag.md` | 0 | 🔴 Очень сложный | 381 | 23 | 16.6 |
| `docs/ai-collaborations/ensembles/4-web-to-knowledge-pipeline.md` | 0 | 🔴 Очень сложный | 302 | 16 | 18.9 |
| `docs/ai-collaborations/ensembles/5-agent-firewall.md` | 0 | 🔴 Очень сложный | 391 | 26 | 15.0 |
| `docs/ai-collaborations/ensembles/6-continuous-eval-loop.md` | 0 | 🔴 Очень сложный | 327 | 18 | 18.2 |
| `docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md` | 0 | 🔴 Очень сложный | 289 | 16 | 18.1 |
| `docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md` | 0 | 🔴 Очень сложный | 275 | 16 | 17.2 |
| `docs/ai-collaborations/ensembles/9-ambient-team-agent.md` | 0 | 🔴 Очень сложный | 246 | 16 | 15.4 |
| `docs/ai-collaborations/fast-tracks/README.md` | 0 | 🔴 Очень сложный | 275 | 18 | 15.3 |
| `docs/ai-collaborations/source-projects.md` | 0 | 🔴 Очень сложный | 467 | 14 | 33.4 |
| `docs/ai-collaborations/strategy/README.md` | 0 | 🔴 Очень сложный | 27 | 3 | 9.0 |
| `docs/anthropic-vacancies/QA.md` | 0 | 🔴 Очень сложный | 58 | 7 | 8.3 |
| `docs/anthropic-vacancies/README.md` | 0 | 🔴 Очень сложный | 99 | 9 | 11.0 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md` | 0 | 🔴 Очень сложный | 858 | 37 | 23.2 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md` | 0 | 🔴 Очень сложный | 317 | 25 | 12.7 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md` | 0 | 🔴 Очень сложный | 337 | 27 | 12.5 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md` | 0 | 🔴 Очень сложный | 629 | 38 | 16.6 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md` | 0 | 🔴 Очень сложный | 499 | 29 | 17.2 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md` | 0 | 🔴 Очень сложный | 1299 | 87 | 14.9 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md` | 0 | 🔴 Очень сложный | 503 | 38 | 13.2 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md` | 0 | 🔴 Очень сложный | 285 | 28 | 10.2 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md` | 0 | 🔴 Очень сложный | 245 | 19 | 12.9 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md` | 0 | 🔴 Очень сложный | 644 | 82 | 7.9 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md` | 0 | 🔴 Очень сложный | 356 | 30 | 11.9 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/00-context.md` | 0 | 🔴 Очень сложный | 249 | 24 | 10.4 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md` | 0 | 🔴 Очень сложный | 177 | 9 | 19.7 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md` | 0 | 🔴 Очень сложный | 160 | 8 | 20.0 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md` | 0 | 🔴 Очень сложный | 175 | 9 | 19.4 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md` | 0 | 🔴 Очень сложный | 168 | 7 | 24.0 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md` | 0 | 🔴 Очень сложный | 211 | 11 | 19.2 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md` | 0 | 🔴 Очень сложный | 163 | 9 | 18.1 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md` | 0 | 🔴 Очень сложный | 148 | 7 | 21.1 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md` | 0 | 🔴 Очень сложный | 163 | 7 | 23.3 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md` | 0 | 🔴 Очень сложный | 156 | 11 | 14.2 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md` | 0 | 🔴 Очень сложный | 211 | 7 | 30.1 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md` | 0 | 🔴 Очень сложный | 376 | 20 | 18.8 |
| `docs/anthropic-vacancies/clusters/01-ai-research-engineering.md` | 0 | 🔴 Очень сложный | 130 | 13 | 10.0 |
| `docs/anthropic-vacancies/clusters/02-sales.md` | 0 | 🔴 Очень сложный | 140 | 11 | 12.7 |
| `docs/anthropic-vacancies/clusters/03-finance.md` | 0 | 🔴 Очень сложный | 110 | 10 | 11.0 |
| `docs/anthropic-vacancies/clusters/04-security.md` | 0 | 🔴 Очень сложный | 91 | 10 | 9.1 |
| `docs/anthropic-vacancies/clusters/05-marketing-brand.md` | 0 | 🔴 Очень сложный | 103 | 10 | 10.3 |
| `docs/anthropic-vacancies/clusters/06-engineering-design-product.md` | 0 | 🔴 Очень сложный | 104 | 10 | 10.4 |
| `docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md` | 0 | 🔴 Очень сложный | 107 | 10 | 10.7 |
| `docs/anthropic-vacancies/clusters/08-safeguards-trust-safety.md` | 0 | 🔴 Очень сложный | 112 | 10 | 11.2 |
| `docs/anthropic-vacancies/clusters/09-product-management-support-ops.md` | 0 | 🔴 Очень сложный | 94 | 9 | 10.4 |
| `docs/anthropic-vacancies/clusters/10-compute.md` | 0 | 🔴 Очень сложный | 104 | 10 | 10.4 |
| `docs/anthropic-vacancies/clusters/11-legal.md` | 0 | 🔴 Очень сложный | 98 | 10 | 9.8 |
| `docs/anthropic-vacancies/clusters/12-technical-program-management.md` | 0 | 🔴 Очень сложный | 89 | 10 | 8.9 |
| `docs/anthropic-vacancies/clusters/13-communications.md` | 0 | 🔴 Очень сложный | 82 | 9 | 9.1 |
| `docs/anthropic-vacancies/clusters/14-public-policy.md` | 0 | 🔴 Очень сложный | 86 | 9 | 9.6 |
| `docs/anthropic-vacancies/clusters/15-public-benefit.md` | 0 | 🔴 Очень сложный | 85 | 9 | 9.4 |
| `docs/anthropic-vacancies/clusters/16-people.md` | 0 | 🔴 Очень сложный | 79 | 10 | 7.9 |
| `docs/anthropic-vacancies/extra-collaborator-findings/01-coally.md` | 0 | 🔴 Очень сложный | 255 | 18 | 14.2 |
| `docs/anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md` | 0 | 🔴 Очень сложный | 280 | 14 | 20.0 |
| `docs/anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md` | 0 | 🔴 Очень сложный | 264 | 20 | 13.2 |
| `docs/anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md` | 0 | 🔴 Очень сложный | 270 | 11 | 24.5 |
| `docs/anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md` | 0 | 🔴 Очень сложный | 153 | 10 | 15.3 |
| `docs/anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md` | 0 | 🔴 Очень сложный | 208 | 20 | 10.4 |
| `docs/anthropic-vacancies/extra-collaborator-findings/07-key-observation.md` | 0 | 🔴 Очень сложный | 173 | 17 | 10.2 |
| `docs/anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md` | 0 | 🔴 Очень сложный | 334 | 21 | 15.9 |
| `docs/anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md` | 0 | 🔴 Очень сложный | 203 | 19 | 10.7 |
| `docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md` | 0 | 🔴 Очень сложный | 145 | 11 | 13.2 |
| `docs/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md` | 0 | 🔴 Очень сложный | 137 | 10 | 13.7 |
| `docs/anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md` | 0 | 🔴 Очень сложный | 134 | 11 | 12.2 |
| `docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md` | 0 | 🔴 Очень сложный | 154 | 11 | 14.0 |
| `docs/anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md` | 0 | 🔴 Очень сложный | 177 | 14 | 12.6 |
| `docs/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md` | 0 | 🔴 Очень сложный | 178 | 14 | 12.7 |
| `docs/anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md` | 0 | 🔴 Очень сложный | 162 | 16 | 10.1 |
| `docs/anthropic-vacancies/hermes-comparison/09-difference-4-institutional-vision.md` | 0 | 🔴 Очень сложный | 164 | 12 | 13.7 |
| `docs/anthropic-vacancies/hermes-comparison/10-difference-5-tool-vs-mission-drift.md` | 0 | 🔴 Очень сложный | 165 | 12 | 13.8 |
| `docs/anthropic-vacancies/hermes-comparison/11-pluses-of-hermes.md` | 0 | 🔴 Очень сложный | 213 | 30 | 7.1 |
| `docs/anthropic-vacancies/hermes-comparison/12-minuses-of-hermes.md` | 0 | 🔴 Очень сложный | 288 | 36 | 8.0 |
| `docs/anthropic-vacancies/hermes-comparison/13-reprioritization.md` | 0 | 🔴 Очень сложный | 880 | 82 | 10.7 |
| `docs/anthropic-vacancies/hermes-comparison/README.md` | 0 | 🔴 Очень сложный | 124 | 28 | 4.4 |
| `docs/anthropic-vacancies/methodology.md` | 0 | 🔴 Очень сложный | 88 | 13 | 6.8 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/00-question-mmorpg-for-programmers.md` | 0 | 🔴 Очень сложный | 487 | 25 | 19.5 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/01-why-stronger-than-it-looks.md` | 0 | 🔴 Очень сложный | 346 | 29 | 11.9 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/02-existing-niche.md` | 0 | 🔴 Очень сложный | 345 | 34 | 10.1 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/03-why-natural-for-programmers.md` | 0 | 🔴 Очень сложный | 959 | 86 | 11.2 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/04-pluses-as-business.md` | 0 | 🔴 Очень сложный | 145 | 7 | 20.7 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/05-minuses-as-business.md` | 0 | 🔴 Очень сложный | 596 | 45 | 13.2 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/00-question-two-nautiluses.md` | 0 | 🔴 Очень сложный | 424 | 18 | 23.6 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md` | 0 | 🔴 Очень сложный | 231 | 19 | 12.2 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/02-nautilus-A-pro2-meta.md` | 0 | 🔴 Очень сложный | 1009 | 64 | 15.8 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/03-nautilus-B-meta-orchestrator.md` | 0 | 🔴 Очень сложный | 1004 | 68 | 14.8 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/README.md` | 0 | 🔴 Очень сложный | 39 | 8 | 4.9 |
| `docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md` | 0 | 🔴 Очень сложный | 217 | 12 | 18.1 |
| `docs/anthropic-vacancies/nautilus-vs-camel/01-passive-vs-active-roles.md` | 0 | 🔴 Очень сложный | 181 | 18 | 10.1 |
| `docs/anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md` | 0 | 🔴 Очень сложный | 1064 | 80 | 13.3 |
| `docs/anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md` | 0 | 🔴 Очень сложный | 269 | 11 | 24.5 |
| `docs/anthropic-vacancies/nautilus-vs-camel/04-what-to-take-from-info-repos.md` | 0 | 🔴 Очень сложный | 612 | 36 | 17.0 |
| `docs/anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md` | 0 | 🔴 Очень сложный | 336 | 31 | 10.8 |
| `docs/anthropic-vacancies/overview.md` | 0 | 🔴 Очень сложный | 220 | 31 | 7.1 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md` | 0 | 🔴 Очень сложный | 308 | 24 | 12.8 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md` | 0 | 🔴 Очень сложный | 277 | 20 | 13.8 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md` | 0 | 🔴 Очень сложный | 177 | 12 | 14.8 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md` | 0 | 🔴 Очень сложный | 227 | 14 | 16.2 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/05-quaternary-developer-education.md` | 0 | 🔴 Очень сложный | 199 | 14 | 14.2 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md` | 0 | 🔴 Очень сложный | 161 | 14 | 11.5 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md` | 0 | 🔴 Очень сложный | 174 | 13 | 13.4 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md` | 0 | 🔴 Очень сложный | 188 | 15 | 12.5 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/README.md` | 0 | 🔴 Очень сложный | 71 | 16 | 4.4 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md` | 0 | 🔴 Очень сложный | 207 | 17 | 12.2 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/02-three-overlapping-identities.md` | 0 | 🔴 Очень сложный | 250 | 20 | 12.5 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/03-revised-anthropic-mapping.md` | 0 | 🔴 Очень сложный | 247 | 21 | 11.8 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md` | 0 | 🔴 Очень сложный | 350 | 32 | 10.9 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md` | 0 | 🔴 Очень сложный | 238 | 16 | 14.9 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md` | 0 | 🔴 Очень сложный | 324 | 28 | 11.6 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md` | 0 | 🔴 Очень сложный | 599 | 48 | 12.5 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md` | 0 | 🔴 Очень сложный | 175 | 15 | 11.7 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md` | 0 | 🔴 Очень сложный | 439 | 31 | 14.2 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/05-platform-not-position.md` | 0 | 🔴 Очень сложный | 521 | 12 | 43.4 |
| `docs/anthropic-vacancies/profile-mapping/README.md` | 0 | 🔴 Очень сложный | 126 | 6 | 21.0 |
| `docs/anthropic-vacancies/signals.md` | 0 | 🔴 Очень сложный | 230 | 19 | 12.1 |
| `docs/autofilled/README.md` | 0 | 🔴 Очень сложный | 13 | 3 | 4.3 |
| `docs/autofilled/components/.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/components/cowork.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/components/ingit.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/components/kksudo.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/components/lorenzo.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/components/nautilus.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/components/sgb.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/components/spbmolot.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/components/svend4.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/components/svyazi.md` | 0 | 🔴 Очень сложный | 19 | 3 | 6.3 |
| `docs/autofilled/research-summary.md` | 0 | 🔴 Очень сложный | 44 | 8 | 5.5 |
| `docs/contacts/anastasiyaw.md` | 0 | 🔴 Очень сложный | 102 | 8 | 12.8 |
| `docs/contacts/andrey-chuyan.md` | 0 | 🔴 Очень сложный | 111 | 12 | 9.2 |
| `docs/contacts/antipozitive.md` | 0 | 🔴 Очень сложный | 89 | 9 | 9.9 |
| `docs/contacts/cutcode.md` | 0 | 🔴 Очень сложный | 85 | 7 | 12.1 |
| `docs/contacts/dmitriila.md` | 0 | 🔴 Очень сложный | 82 | 7 | 11.7 |
| `docs/contacts/kksudo.md` | 0 | 🔴 Очень сложный | 96 | 9 | 10.7 |
| `docs/contacts/mixaill76.md` | 0 | 🔴 Очень сложный | 88 | 7 | 12.6 |
| `docs/contacts/nlaik.md` | 0 | 🔴 Очень сложный | 93 | 9 | 10.3 |
| `docs/contacts/sonia-black.md` | 0 | 🔴 Очень сложный | 95 | 9 | 10.6 |
| `docs/contacts/spbmolot.md` | 0 | 🔴 Очень сложный | 105 | 10 | 10.5 |
| `docs/contacts/tagir-analyzes.md` | 0 | 🔴 Очень сложный | 88 | 7 | 12.6 |
| `docs/contacts/vitalyoborin.md` | 0 | 🔴 Очень сложный | 101 | 10 | 10.1 |
| `docs/contacts/vladspace.md` | 0 | 🔴 Очень сложный | 87 | 7 | 12.4 |
| `docs/contacts/zodigancode.md` | 0 | 🔴 Очень сложный | 84 | 7 | 12.0 |
| `docs/glossary/components-by-name.md` | 0 | 🔴 Очень сложный | 1984 | 380 | 5.2 |
| `docs/glossary/concepts.md` | 0 | 🔴 Очень сложный | 746 | 98 | 7.6 |
| `docs/habr-unique-projects/README.md` | 0 | 🔴 Очень сложный | 229 | 5 | 45.8 |
| `docs/habr-unique-projects/analogues/01-three-direct-analogues.md` | 0 | 🔴 Очень сложный | 355 | 22 | 16.1 |
| `docs/habr-unique-projects/analogues/02-related-projects.md` | 0 | 🔴 Очень сложный | 338 | 17 | 19.9 |
| `docs/habr-unique-projects/analogues/README.md` | 0 | 🔴 Очень сложный | 17 | 4 | 4.2 |
| `docs/habr-unique-projects/deep-pairs/1-llm-gateway.md` | 0 | 🔴 Очень сложный | 271 | 22 | 12.3 |
| `docs/habr-unique-projects/deep-pairs/2-document-rag.md` | 0 | 🔴 Очень сложный | 290 | 19 | 15.3 |
| `docs/habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md` | 0 | 🔴 Очень сложный | 271 | 22 | 12.3 |
| `docs/habr-unique-projects/deep-pairs/5-voice-local-memory.md` | 0 | 🔴 Очень сложный | 264 | 17 | 15.5 |
| `docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md` | 0 | 🔴 Очень сложный | 312 | 23 | 13.6 |
| `docs/habr-unique-projects/deep-pairs/7-autoresearch-distributed.md` | 0 | 🔴 Очень сложный | 255 | 20 | 12.8 |
| `docs/habr-unique-projects/evaluation/README.md` | 0 | 🔴 Очень сложный | 27 | 4 | 6.8 |
| `docs/habr-unique-projects/extra-examples/00-question-habr-examples.md` | 0 | 🔴 Очень сложный | 413 | 28 | 14.8 |
| `docs/habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md` | 0 | 🔴 Очень сложный | 193 | 15 | 12.9 |
| `docs/habr-unique-projects/extra-examples/02-vshe-scientific-networking.md` | 0 | 🔴 Очень сложный | 162 | 12 | 13.5 |
| `docs/habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md` | 0 | 🔴 Очень сложный | 243 | 14 | 17.4 |
| `docs/habr-unique-projects/extra-examples/04-claude-subagents-patterns.md` | 0 | 🔴 Очень сложный | 157 | 13 | 12.1 |
| `docs/habr-unique-projects/extra-examples/05-hw-nl2workflow.md` | 0 | 🔴 Очень сложный | 232 | 15 | 15.5 |
| `docs/habr-unique-projects/extra-examples/06-platform-for-professional-communities.md` | 0 | 🔴 Очень сложный | 197 | 13 | 15.2 |
| `docs/habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md` | 0 | 🔴 Очень сложный | 203 | 13 | 15.6 |
| `docs/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md` | 0 | 🔴 Очень сложный | 202 | 16 | 12.6 |
| `docs/habr-unique-projects/extra-examples/09-federated-platform.md` | 0 | 🔴 Очень сложный | 191 | 12 | 15.9 |
| `docs/habr-unique-projects/extra-examples/10-profession-specific-workflows.md` | 0 | 🔴 Очень сложный | 273 | 23 | 11.9 |
| `docs/habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md` | 0 | 🔴 Очень сложный | 242 | 13 | 18.6 |
| `docs/habr-unique-projects/extra-examples/12-concrete-next-step.md` | 0 | 🔴 Очень сложный | 362 | 38 | 9.5 |
| `docs/habr-unique-projects/final-ensembles/1-one-person-one-company.md` | 0 | 🔴 Очень сложный | 162 | 10 | 16.2 |
| `docs/habr-unique-projects/final-ensembles/2-autoresearch-legal.md` | 0 | 🔴 Очень сложный | 163 | 9 | 18.1 |
| `docs/habr-unique-projects/final-ensembles/3-discovery-research.md` | 0 | 🔴 Очень сложный | 127 | 8 | 15.9 |
| `docs/habr-unique-projects/final-ensembles/4-summary-authors.md` | 0 | 🔴 Очень сложный | 233 | 15 | 15.5 |
| `docs/habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md` | 0 | 🔴 Очень сложный | 303 | 20 | 15.2 |
| `docs/habr-unique-projects/hardware-pairs/2-tsu-mome.md` | 0 | 🔴 Очень сложный | 267 | 21 | 12.7 |
| `docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md` | 0 | 🔴 Очень сложный | 268 | 22 | 12.2 |
| `docs/habr-unique-projects/hardware-pairs/4-riscv-privacy.md` | 0 | 🔴 Очень сложный | 276 | 20 | 13.8 |
| `docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md` | 0 | 🔴 Очень сложный | 300 | 19 | 15.8 |
| `docs/habr-unique-projects/hardware-pairs/7-metaphor.md` | 0 | 🔴 Очень сложный | 298 | 13 | 22.9 |
| `docs/habr-unique-projects/key-findings/01-yodoca.md` | 0 | 🔴 Очень сложный | 222 | 14 | 15.9 |
| `docs/habr-unique-projects/key-findings/02-memnet.md` | 0 | 🔴 Очень сложный | 199 | 10 | 19.9 |
| `docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md` | 0 | 🔴 Очень сложный | 219 | 15 | 14.6 |
| `docs/habr-unique-projects/key-findings/04-dochkina-sequential.md` | 0 | 🔴 Очень сложный | 255 | 17 | 15.0 |
| `docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md` | 0 | 🔴 Очень сложный | 263 | 14 | 18.8 |
| `docs/habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md` | 0 | 🔴 Очень сложный | 333 | 16 | 20.8 |
| `docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md` | 0 | 🔴 Очень сложный | 283 | 22 | 12.9 |
| `docs/habr-unique-projects/software-pairs/2-pkm-mcp-skills.md` | 0 | 🔴 Очень сложный | 300 | 22 | 13.6 |
| `docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md` | 0 | 🔴 Очень сложный | 264 | 21 | 12.6 |
| `docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md` | 0 | 🔴 Очень сложный | 278 | 24 | 11.6 |
| `docs/habr-unique-projects/software-pairs/6-metaphor.md` | 0 | 🔴 Очень сложный | 231 | 10 | 23.1 |
| `docs/lorenzo-agent/00-intro.md` | 0 | 🔴 Очень сложный | 46 | 5 | 9.2 |
| `docs/lorenzo-agent/01-kto-ty.md` | 0 | 🔴 Очень сложный | 143 | 13 | 11.0 |
| `docs/lorenzo-agent/02-tvoyo-proishozhdenie.md` | 0 | 🔴 Очень сложный | 156 | 16 | 9.8 |
| `docs/lorenzo-agent/03-tvoya-missiya.md` | 0 | 🔴 Очень сложный | 143 | 11 | 13.0 |
| `docs/lorenzo-agent/04-komu-ty-sluzhish.md` | 0 | 🔴 Очень сложный | 150 | 11 | 13.6 |
| `docs/lorenzo-agent/05-tvoya-lichnost.md` | 0 | 🔴 Очень сложный | 219 | 28 | 7.8 |
| `docs/lorenzo-agent/06-yazyki-kultura.md` | 0 | 🔴 Очень сложный | 180 | 8 | 22.5 |
| `docs/lorenzo-agent/07-chto-mozhesh.md` | 0 | 🔴 Очень сложный | 147 | 8 | 18.4 |
| `docs/lorenzo-agent/08-bez-max-approval.md` | 0 | 🔴 Очень сложный | 147 | 8 | 18.4 |
| `docs/lorenzo-agent/09-voobshche-nelzya.md` | 0 | 🔴 Очень сложный | 143 | 8 | 17.9 |
| `docs/lorenzo-agent/10-collaborators-landscape.md` | 0 | 🔴 Очень сложный | 306 | 28 | 10.9 |
| `docs/lorenzo-agent/11-dhlab-documents.md` | 0 | 🔴 Очень сложный | 177 | 21 | 8.4 |
| `docs/lorenzo-agent/12-workflow.md` | 0 | 🔴 Очень сложный | 179 | 18 | 9.9 |
| `docs/lorenzo-agent/13-outreach-communication.md` | 0 | 🔴 Очень сложный | 202 | 22 | 9.2 |
| `docs/lorenzo-agent/14-other-ai-relationships.md` | 0 | 🔴 Очень сложный | 162 | 11 | 14.7 |
| `docs/lorenzo-agent/15-anti-patterns.md` | 0 | 🔴 Очень сложный | 159 | 11 | 14.5 |
| `docs/lorenzo-agent/16-vsegda-delaesh.md` | 0 | 🔴 Очень сложный | 117 | 8 | 14.6 |
| `docs/lorenzo-agent/18-escalate-to-max.md` | 0 | 🔴 Очень сложный | 123 | 10 | 12.3 |
| `docs/lorenzo-agent/19-persistent-character.md` | 0 | 🔴 Очень сложный | 155 | 11 | 14.1 |
| `docs/lorenzo-agent/20-experiment.md` | 0 | 🔴 Очень сложный | 140 | 15 | 9.3 |
| `docs/lorenzo-agent/QA.md` | 0 | 🔴 Очень сложный | 192 | 27 | 7.1 |
| `docs/lorenzo-agent/naming/01-search-results-not-found.md` | 0 | 🔴 Очень сложный | 294 | 15 | 19.6 |
| `docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md` | 0 | 🔴 Очень сложный | 1099 | 32 | 34.3 |
| `docs/lorenzo-agent/naming/03-dhlab-umbrella.md` | 0 | 🔴 Очень сложный | 1324 | 43 | 30.8 |
| `docs/lorenzo-agent/operationalized/00-overview-grandchild-combination.md` | 0 | 🔴 Очень сложный | 531 | 39 | 13.6 |
| `docs/lorenzo-agent/operationalized/01-pluses-1-7.md` | 0 | 🔴 Очень сложный | 423 | 21 | 20.1 |
| `docs/lorenzo-agent/operationalized/02-minuses-1-10.md` | 0 | 🔴 Очень сложный | 681 | 41 | 16.6 |
| `docs/lorenzo-agent/operationalized/03-honest-opinion.md` | 0 | 🔴 Очень сложный | 173 | 11 | 15.7 |
| `docs/lorenzo-agent/operationalized/04-recommendations.md` | 0 | 🔴 Очень сложный | 391 | 23 | 17.0 |
| `docs/lorenzo-agent/operationalized/05-anchor-node-habr-scout.md` | 0 | 🔴 Очень сложный | 514 | 27 | 19.0 |
| `docs/lorenzo-agent/operationalized/06-conclusion-deserves-attention.md` | 0 | 🔴 Очень сложный | 460 | 33 | 13.9 |
| `docs/lorenzo-agent/operationalized/README.md` | 0 | 🔴 Очень сложный | 50 | 14 | 3.6 |
| `docs/lorenzo-agent/phased-deployment/00-overview.md` | 0 | 🔴 Очень сложный | 158 | 12 | 13.2 |
| `docs/lorenzo-agent/phased-deployment/01-level-0-manual.md` | 0 | 🔴 Очень сложный | 170 | 13 | 13.1 |
| `docs/lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md` | 0 | 🔴 Очень сложный | 224 | 12 | 18.7 |
| `docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md` | 0 | 🔴 Очень сложный | 207 | 13 | 15.9 |
| `docs/lorenzo-agent/phased-deployment/04-level-3-medium-active.md` | 0 | 🔴 Очень сложный | 214 | 10 | 21.4 |
| `docs/lorenzo-agent/phased-deployment/05-level-4-extended-mature.md` | 0 | 🔴 Очень сложный | 181 | 12 | 15.1 |
| `docs/lorenzo-agent/phased-deployment/06-level-5-full-network.md` | 0 | 🔴 Очень сложный | 141 | 10 | 14.1 |
| `docs/lorenzo-agent/phased-deployment/07-progression-logic.md` | 0 | 🔴 Очень сложный | 171 | 19 | 9.0 |
| `docs/lorenzo-agent/phased-deployment/08-current-session-poc.md` | 0 | 🔴 Очень сложный | 710 | 29 | 24.5 |
| `docs/lorenzo-agent/scenarios/00-question-scenario.md` | 0 | 🔴 Очень сложный | 180 | 9 | 20.0 |
| `docs/lorenzo-agent/scenarios/01-response.md` | 0 | 🔴 Очень сложный | 2197 | 123 | 17.9 |
| `docs/lorenzo-agent/scenarios/README.md` | 0 | 🔴 Очень сложный | 13 | 4 | 3.2 |
| `docs/lorenzo-agent/specification/00-context-fundamental-questions.md` | 0 | 🔴 Очень сложный | 194 | 17 | 11.4 |
| `docs/lorenzo-agent/specification/01-q1-what-lorenzo-is.md` | 0 | 🔴 Очень сложный | 321 | 14 | 22.9 |
| `docs/lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md` | 0 | 🔴 Очень сложный | 226 | 14 | 16.1 |
| `docs/lorenzo-agent/specification/03-q3-what-lorenzo-does.md` | 0 | 🔴 Очень сложный | 209 | 17 | 12.3 |
| `docs/lorenzo-agent/specification/04-q4-character.md` | 0 | 🔴 Очень сложный | 261 | 23 | 11.3 |
| `docs/lorenzo-agent/specification/05-q5-authority-limits.md` | 0 | 🔴 Очень сложный | 227 | 13 | 17.5 |
| `docs/lorenzo-agent/specification/06-q6-accountability.md` | 0 | 🔴 Очень сложный | 197 | 17 | 11.6 |
| `docs/lorenzo-agent/specification/07-q7-success-metrics.md` | 0 | 🔴 Очень сложный | 206 | 11 | 18.7 |
| `docs/lorenzo-agent/specification/08-q8-other-ai-relationships.md` | 0 | 🔴 Очень сложный | 198 | 12 | 16.5 |
| `docs/lorenzo-agent/specification/09-q9-geographic-linguistic-scope.md` | 0 | 🔴 Очень сложный | 198 | 12 | 16.5 |
| `docs/lorenzo-agent/specification/10-q10-funding-model.md` | 0 | 🔴 Очень сложный | 228 | 11 | 20.7 |
| `docs/lorenzo-agent/specification/11-difficulties-and-recommendations.md` | 0 | 🔴 Очень сложный | 1271 | 83 | 15.3 |
| `docs/nautilus/README.md` | 0 | 🔴 Очень сложный | 446 | 27 | 16.5 |
| `docs/nautilus/community-discussions/README.md` | 0 | 🔴 Очень сложный | 76 | 2 | 38.0 |
| `docs/nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md` | 0 | 🔴 Очень сложный | 213 | 9 | 23.7 |
| `docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md` | 0 | 🔴 Очень сложный | 8865 | 787 | 11.3 |
| `docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md` | 0 | 🔴 Очень сложный | 63 | 9 | 7.0 |
| `docs/nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md` | 0 | 🔴 Очень сложный | 2230 | 190 | 11.7 |
| `docs/nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md` | 0 | 🔴 Очень сложный | 157 | 9 | 17.4 |
| `docs/nautilus/community-discussions/habr-article-2-reaction/01-response.md` | 0 | 🔴 Очень сложный | 2442 | 216 | 11.3 |
| `docs/nautilus/community-discussions/practical-observations/00-question-practical.md` | 0 | 🔴 Очень сложный | 221 | 9 | 24.6 |
| `docs/nautilus/community-discussions/practical-observations/01-response.md` | 0 | 🔴 Очень сложный | 1672 | 145 | 11.5 |
| `docs/nautilus/community-discussions/practical-observations/README.md` | 0 | 🔴 Очень сложный | 15 | 4 | 3.8 |
| `docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md` | 0 | 🔴 Очень сложный | 477 | 20 | 23.9 |
| `docs/nautilus/community-discussions/voiceless-contributors/01-response.md` | 0 | 🔴 Очень сложный | 2306 | 195 | 11.8 |
| `docs/nautilus/community-discussions/voiceless-contributors/README.md` | 0 | 🔴 Очень сложный | 15 | 4 | 3.8 |
| `docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md` | 0 | 🔴 Очень сложный | 616 | 47 | 13.1 |
| `docs/nautilus/composite-skills-agents/03-what-makes-csa.md` | 0 | 🔴 Очень сложный | 865 | 79 | 10.9 |
| `docs/nautilus/composite-skills-agents/04-sub-agent-registry.md` | 0 | 🔴 Очень сложный | 739 | 70 | 10.6 |
| `docs/nautilus/composite-skills-agents/05-configuration-ensembles.md` | 0 | 🔴 Очень сложный | 660 | 59 | 11.2 |
| `docs/nautilus/composite-skills-agents/06-coordination-disagreement.md` | 0 | 🔴 Очень сложный | 714 | 69 | 10.3 |
| `docs/nautilus/composite-skills-agents/07-economics-combinatorial.md` | 0 | 🔴 Очень сложный | 716 | 60 | 11.9 |
| `docs/nautilus/composite-skills-agents/08-seven-domains.md` | 0 | 🔴 Очень сложный | 921 | 52 | 17.7 |
| `docs/nautilus/composite-skills-agents/09-okwf-integration.md` | 0 | 🔴 Очень сложный | 674 | 51 | 13.2 |
| `docs/nautilus/composite-skills-agents/10-risks.md` | 0 | 🔴 Очень сложный | 727 | 46 | 15.8 |
| `docs/nautilus/composite-skills-agents/11-open-questions.md` | 0 | 🔴 Очень сложный | 450 | 43 | 10.5 |
| `docs/nautilus/composite-skills-agents/12-call-for-collaboration.md` | 0 | 🔴 Очень сложный | 334 | 25 | 13.4 |
| `docs/nautilus/composite-skills-agents/13-closing.md` | 0 | 🔴 Очень сложный | 616 | 51 | 12.1 |
| `docs/nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md` | 0 | 🔴 Очень сложный | 527 | 9 | 58.6 |
| `docs/nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md` | 0 | 🔴 Очень сложный | 473 | 44 | 10.8 |
| `docs/nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md` | 0 | 🔴 Очень сложный | 957 | 103 | 9.3 |
| `docs/nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md` | 0 | 🔴 Очень сложный | 839 | 94 | 8.9 |
| `docs/nautilus/double-triangle-architecture/00-abstract.md` | 0 | 🔴 Очень сложный | 375 | 26 | 14.4 |
| `docs/nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md` | 0 | 🔴 Очень сложный | 469 | 31 | 15.1 |
| `docs/nautilus/double-triangle-architecture/02-double-triangle-architecture.md` | 0 | 🔴 Очень сложный | 603 | 47 | 12.8 |
| `docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md` | 0 | 🔴 Очень сложный | 760 | 65 | 11.7 |
| `docs/nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md` | 0 | 🔴 Очень сложный | 620 | 47 | 13.2 |
| `docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md` | 0 | 🔴 Очень сложный | 590 | 48 | 12.3 |
| `docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md` | 0 | 🔴 Очень сложный | 613 | 59 | 10.4 |
| `docs/nautilus/double-triangle-architecture/07-open-questions.md` | 0 | 🔴 Очень сложный | 702 | 62 | 11.3 |
| `docs/nautilus/double-triangle-architecture/08-call-to-action.md` | 0 | 🔴 Очень сложный | 692 | 77 | 9.0 |
| `docs/nautilus/double-triangle-architecture/09-acknowledgments.md` | 0 | 🔴 Очень сложный | 197 | 20 | 9.8 |
| `docs/nautilus/double-triangle-architecture/10-references.md` | 0 | 🔴 Очень сложный | 224 | 50 | 4.5 |
| `docs/nautilus/double-triangle-architecture/11-glossary.md` | 0 | 🔴 Очень сложный | 1465 | 153 | 9.6 |
| `docs/nautilus/infrastructure-layer-b-en/00-intro.md` | 0 | 🔴 Очень сложный | 137 | 15 | 9.1 |
| `docs/nautilus/infrastructure-layer-b-en/06-existing-approximations.md` | 0 | 🔴 Очень сложный | 439 | 25 | 17.6 |
| `docs/nautilus/infrastructure-layer-b-en/12-closing.md` | 0 | 🔴 Очень сложный | 186 | 15 | 12.4 |
| `docs/nautilus/infrastructure-layer-b-en/13-acknowledgments-refs.md` | 0 | 🔴 Очень сложный | 460 | 31 | 14.8 |
| `docs/nautilus/infrastructure-layer-b-ru/00-intro.md` | 0 | 🔴 Очень сложный | 462 | 54 | 8.6 |
| `docs/nautilus/infrastructure-layer-b-ru/01-zachem-dokument.md` | 0 | 🔴 Очень сложный | 241 | 26 | 9.3 |
| `docs/nautilus/infrastructure-layer-b-ru/02-dvukhsloynyy-stek.md` | 0 | 🔴 Очень сложный | 294 | 26 | 11.3 |
| `docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md` | 0 | 🔴 Очень сложный | 359 | 40 | 9.0 |
| `docs/nautilus/infrastructure-layer-b-ru/04-pochemu-ne-postroeno.md` | 0 | 🔴 Очень сложный | 292 | 35 | 8.3 |
| `docs/nautilus/infrastructure-layer-b-ru/05-priblizheniya.md` | 0 | 🔴 Очень сложный | 413 | 28 | 14.8 |
| `docs/nautilus/infrastructure-layer-b-ru/06-konkretnyy-sluchay.md` | 0 | 🔴 Очень сложный | 545 | 65 | 8.4 |
| `docs/nautilus/infrastructure-layer-b-ru/07-rekursivnoe-prozrenie.md` | 0 | 🔴 Очень сложный | 299 | 30 | 10.0 |
| `docs/nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md` | 0 | 🔴 Очень сложный | 264 | 35 | 7.5 |
| `docs/nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md` | 0 | 🔴 Очень сложный | 190 | 25 | 7.6 |
| `docs/nautilus/infrastructure-layer-b-ru/10-rekomendatsii.md` | 0 | 🔴 Очень сложный | 290 | 39 | 7.4 |
| `docs/nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md` | 0 | 🔴 Очень сложный | 203 | 19 | 10.7 |
| `docs/nautilus/infrastructure-layer-b-ru/12-blagodarnosti-ssylki.md` | 0 | 🔴 Очень сложный | 453 | 35 | 12.9 |
| `docs/nautilus/ingit-cowork-en/04-symbiotic-architecture.md` | 0 | 🔴 Очень сложный | 424 | 33 | 12.8 |
| `docs/nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md` | 0 | 🔴 Очень сложный | 547 | 44 | 12.4 |
| `docs/nautilus/ingit-cowork-en/09-risks-open-questions.md` | 0 | 🔴 Очень сложный | 513 | 63 | 8.1 |
| `docs/nautilus/ingit-cowork-en/10-strategic-positioning.md` | 0 | 🔴 Очень сложный | 677 | 64 | 10.6 |
| `docs/nautilus/ingit-cowork-ru/01-otkrytie-cowork.md` | 0 | 🔴 Очень сложный | 539 | 60 | 9.0 |
| `docs/nautilus/ingit-cowork-ru/02-chto-cowork-obespechivaet.md` | 0 | 🔴 Очень сложный | 580 | 50 | 11.6 |
| `docs/nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md` | 0 | 🔴 Очень сложный | 747 | 60 | 12.4 |
| `docs/nautilus/ingit-cowork-ru/04-simbioticheskaya-arkhitektura.md` | 0 | 🔴 Очень сложный | 413 | 36 | 11.5 |
| `docs/nautilus/ingit-cowork-ru/05-chetyre-puti-integratsii.md` | 0 | 🔴 Очень сложный | 602 | 58 | 10.4 |
| `docs/nautilus/ingit-cowork-ru/06-utochnyonnyy-obyom-ingit.md` | 0 | 🔴 Очень сложный | 323 | 23 | 14.0 |
| `docs/nautilus/ingit-cowork-ru/07-prakticheskie-shagi.md` | 0 | 🔴 Очень сложный | 309 | 36 | 8.6 |
| `docs/nautilus/ingit-cowork-ru/08-implikatsii-nautilus-okwf.md` | 0 | 🔴 Очень сложный | 497 | 43 | 11.6 |
| `docs/nautilus/ingit-cowork-ru/09-riski-voprosy.md` | 0 | 🔴 Очень сложный | 496 | 64 | 7.8 |
| `docs/nautilus/ingit-cowork-ru/10-strategicheskoe-pozitsionirovanie.md` | 0 | 🔴 Очень сложный | 576 | 57 | 10.1 |
| `docs/nautilus/ingit-cowork-ru/README.md` | 0 | 🔴 Очень сложный | 79 | 20 | 4.0 |
| `docs/nautilus/innovation-transitions/00-question-innovations-transitions.md` | 0 | 🔴 Очень сложный | 2656 | 239 | 11.1 |
| `docs/nautilus/innovation-transitions/01-response.md` | 0 | 🔴 Очень сложный | 2216 | 174 | 12.7 |
| `docs/nautilus/innovation-transitions/README.md` | 0 | 🔴 Очень сложный | 18 | 4 | 4.5 |
| `docs/nautilus/multi-tier-architecture/00-question-multi-tier.md` | 0 | 🔴 Очень сложный | 202 | 9 | 22.4 |
| `docs/nautilus/multi-tier-architecture/01-strategic-significance.md` | 0 | 🔴 Очень сложный | 2463 | 197 | 12.5 |
| `docs/nautilus/multi-tier-architecture/README.md` | 0 | 🔴 Очень сложный | 20 | 4 | 5.0 |
| `docs/nautilus/npp-humanitarian-extension/00-question-can-it-apply-to-docs.md` | 0 | 🔴 Очень сложный | 281 | 18 | 15.6 |
| `docs/nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md` | 0 | 🔴 Очень сложный | 1350 | 107 | 12.6 |
| `docs/nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md` | 0 | 🔴 Очень сложный | 219 | 19 | 11.5 |
| `docs/nautilus/npp-humanitarian-extension/03-what-doesnt-exist-on-market.md` | 0 | 🔴 Очень сложный | 173 | 10 | 17.3 |
| `docs/nautilus/npp-humanitarian-extension/04-grant-opportunities.md` | 0 | 🔴 Очень сложный | 506 | 46 | 11.0 |
| `docs/nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md` | 0 | 🔴 Очень сложный | 144 | 14 | 10.3 |
| `docs/nautilus/npp-v1-0/00-abstract-status.md` | 0 | 🔴 Очень сложный | 160 | 19 | 8.4 |
| `docs/nautilus/npp-v1-0/01-introduction.md` | 0 | 🔴 Очень сложный | 250 | 22 | 11.4 |
| `docs/nautilus/npp-v1-0/02-terminology.md` | 0 | 🔴 Очень сложный | 194 | 25 | 7.8 |
| `docs/nautilus/npp-v1-0/03-registry.md` | 0 | 🔴 Очень сложный | 170 | 21 | 8.1 |
| `docs/nautilus/npp-v1-0/04-passport.md` | 0 | 🔴 Очень сложный | 107 | 14 | 7.6 |
| `docs/nautilus/npp-v1-0/05-compatibility-levels.md` | 0 | 🔴 Очень сложный | 149 | 22 | 6.8 |
| `docs/nautilus/npp-v1-0/06-adapter-interface.md` | 0 | 🔴 Очень сложный | 153 | 18 | 8.5 |
| `docs/nautilus/npp-v1-0/07-portal-entry.md` | 0 | 🔴 Очень сложный | 92 | 11 | 8.4 |
| `docs/nautilus/npp-v1-0/08-consensus-algorithm.md` | 0 | 🔴 Очень сложный | 220 | 23 | 9.6 |
| `docs/nautilus/npp-v1-0/10-query-result.md` | 0 | 🔴 Очень сложный | 100 | 13 | 7.7 |
| `docs/nautilus/npp-v1-0/11-security-considerations.md` | 0 | 🔴 Очень сложный | 164 | 16 | 10.2 |
| `docs/nautilus/npp-v1-0/12-versioning-policy.md` | 0 | 🔴 Очень сложный | 134 | 20 | 6.7 |
| `docs/nautilus/npp-v1-0/13-reference-implementation.md` | 0 | 🔴 Очень сложный | 98 | 12 | 8.2 |
| `docs/nautilus/npp-v1-0/14-adr-001-federation-over-merging.md` | 0 | 🔴 Очень сложный | 192 | 12 | 16.0 |
| `docs/nautilus/npp-v1-0/15-glossary.md` | 0 | 🔴 Очень сложный | 116 | 13 | 8.9 |
| `docs/nautilus/npp-v1-0/17-appendix-b-change-log.md` | 0 | 🔴 Очень сложный | 84 | 13 | 6.5 |
| `docs/nautilus/npp-v1-0/18-comment-on-document.md` | 0 | 🔴 Очень сложный | 404 | 44 | 9.2 |
| `docs/nautilus/npp-v1-1/00-abstract-status.md` | 0 | 🔴 Очень сложный | 276 | 40 | 6.9 |
| `docs/nautilus/npp-v1-1/01-introduction.md` | 0 | 🔴 Очень сложный | 358 | 25 | 14.3 |
| `docs/nautilus/npp-v1-1/02-terminology.md` | 0 | 🔴 Очень сложный | 276 | 39 | 7.1 |
| `docs/nautilus/npp-v1-1/03-registry.md` | 0 | 🔴 Очень сложный | 285 | 28 | 10.2 |
| `docs/nautilus/npp-v1-1/04-passport.md` | 0 | 🔴 Очень сложный | 186 | 18 | 10.3 |
| `docs/nautilus/npp-v1-1/05-compatibility-levels.md` | 0 | 🔴 Очень сложный | 226 | 25 | 9.0 |
| `docs/nautilus/npp-v1-1/06-adapter-interface.md` | 0 | 🔴 Очень сложный | 176 | 20 | 8.8 |
| `docs/nautilus/npp-v1-1/07-portal-entry.md` | 0 | 🔴 Очень сложный | 146 | 18 | 8.1 |
| `docs/nautilus/npp-v1-1/08-q6-space.md` | 0 | 🔴 Очень сложный | 229 | 25 | 9.2 |
| `docs/nautilus/npp-v1-1/09-consensus-algorithm.md` | 0 | 🔴 Очень сложный | 165 | 19 | 8.7 |
| `docs/nautilus/npp-v1-1/10-query-flow.md` | 0 | 🔴 Очень сложный | 171 | 24 | 7.1 |
| `docs/nautilus/npp-v1-1/11-relevance-ranking.md` | 0 | 🔴 Очень сложный | 107 | 16 | 6.7 |
| `docs/nautilus/npp-v1-1/12-onboarding-paths.md` | 0 | 🔴 Очень сложный | 308 | 47 | 6.6 |
| `docs/nautilus/npp-v1-1/13-rest-api.md` | 0 | 🔴 Очень сложный | 216 | 22 | 9.8 |
| `docs/nautilus/npp-v1-1/14-sdk.md` | 0 | 🔴 Очень сложный | 123 | 16 | 7.7 |
| `docs/nautilus/npp-v1-1/15-security.md` | 0 | 🔴 Очень сложный | 236 | 21 | 11.2 |
| `docs/nautilus/npp-v1-1/16-mcp-extension.md` | 0 | 🔴 Очень сложный | 120 | 14 | 8.6 |
| `docs/nautilus/npp-v1-1/17-versioning-policy.md` | 0 | 🔴 Очень сложный | 170 | 26 | 6.5 |
| `docs/nautilus/npp-v1-1/18-reference-implementation.md` | 0 | 🔴 Очень сложный | 131 | 14 | 9.4 |
| `docs/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md` | 0 | 🔴 Очень сложный | 204 | 15 | 13.6 |
| `docs/nautilus/npp-v1-1/20-adr-002-q6-first-class.md` | 0 | 🔴 Очень сложный | 184 | 19 | 9.7 |
| `docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md` | 0 | 🔴 Очень сложный | 162 | 19 | 8.5 |
| `docs/nautilus/npp-v1-1/22-glossary.md` | 0 | 🔴 Очень сложный | 1076 | 126 | 8.5 |
| `docs/nautilus/okwf-concept/00-abstract.md` | 0 | 🔴 Очень сложный | 333 | 29 | 11.5 |
| `docs/nautilus/okwf-concept/01-problem-statement.md` | 0 | 🔴 Очень сложный | 548 | 34 | 16.1 |
| `docs/nautilus/okwf-concept/02-target-populations.md` | 0 | 🔴 Очень сложный | 610 | 30 | 20.3 |
| `docs/nautilus/okwf-concept/03-why-existing-fail.md` | 0 | 🔴 Очень сложный | 661 | 44 | 15.0 |
| `docs/nautilus/okwf-concept/04-proposed-infrastructure.md` | 0 | 🔴 Очень сложный | 894 | 30 | 29.8 |
| `docs/nautilus/okwf-concept/05-economic-model.md` | 0 | 🔴 Очень сложный | 430 | 34 | 12.6 |
| `docs/nautilus/okwf-concept/06-governance-ethics.md` | 0 | 🔴 Очень сложный | 441 | 36 | 12.2 |
| `docs/nautilus/okwf-concept/07-phased-rollout.md` | 0 | 🔴 Очень сложный | 555 | 27 | 20.6 |
| `docs/nautilus/okwf-concept/08-risk-analysis.md` | 0 | 🔴 Очень сложный | 586 | 29 | 20.2 |
| `docs/nautilus/okwf-concept/09-call-for-partnership.md` | 0 | 🔴 Очень сложный | 398 | 16 | 24.9 |
| `docs/nautilus/okwf-concept/10-appendices.md` | 0 | 🔴 Очень сложный | 568 | 19 | 29.9 |
| `docs/nautilus/privacy-federation/00-question-anonymization.md` | 0 | 🔴 Очень сложный | 283 | 18 | 15.7 |
| `docs/nautilus/privacy-federation/01-what-to-anonymize-german-standard.md` | 0 | 🔴 Очень сложный | 257 | 13 | 19.8 |
| `docs/nautilus/privacy-federation/02-two-tier-publication.md` | 0 | 🔴 Очень сложный | 515 | 29 | 17.8 |
| `docs/nautilus/privacy-federation/03-what-this-gives-technically.md` | 0 | 🔴 Очень сложный | 1311 | 148 | 8.9 |
| `docs/nautilus/privacy-federation/04-what-i-can-do-now.md` | 0 | 🔴 Очень сложный | 318 | 31 | 10.3 |
| `docs/nautilus/professional-colleague-agents-en/00-abstract.md` | 0 | 🔴 Очень сложный | 362 | 28 | 12.9 |
| `docs/nautilus/professional-colleague-agents-en/01-five-type-typology.md` | 0 | 🔴 Очень сложный | 780 | 92 | 8.5 |
| `docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md` | 0 | 🔴 Очень сложный | 756 | 95 | 8.0 |
| `docs/nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md` | 0 | 🔴 Очень сложный | 747 | 59 | 12.7 |
| `docs/nautilus/professional-colleague-agents-en/04-architecture.md` | 0 | 🔴 Очень сложный | 816 | 98 | 8.3 |
| `docs/nautilus/professional-colleague-agents-en/05-economics-replication.md` | 0 | 🔴 Очень сложный | 654 | 64 | 10.2 |
| `docs/nautilus/professional-colleague-agents-en/06-risks.md` | 0 | 🔴 Очень сложный | 1102 | 148 | 7.4 |
| `docs/nautilus/professional-colleague-agents-en/07-application-domains.md` | 0 | 🔴 Очень сложный | 685 | 98 | 7.0 |
| `docs/nautilus/professional-colleague-agents-en/08-pilot-sgb-advocate.md` | 0 | 🔴 Очень сложный | 806 | 58 | 13.9 |
| `docs/nautilus/professional-colleague-agents-en/09-relationship-other-agents.md` | 0 | 🔴 Очень сложный | 600 | 61 | 9.8 |
| `docs/nautilus/professional-colleague-agents-en/10-open-questions.md` | 0 | 🔴 Очень сложный | 311 | 39 | 8.0 |
| `docs/nautilus/professional-colleague-agents-en/11-call-for-collaboration.md` | 0 | 🔴 Очень сложный | 253 | 28 | 9.0 |
| `docs/nautilus/professional-colleague-agents-en/12-closing.md` | 0 | 🔴 Очень сложный | 457 | 39 | 11.7 |
| `docs/nautilus/professional-colleague-agents-ru/00-abstract.md` | 0 | 🔴 Очень сложный | 111 | 18 | 6.2 |
| `docs/nautilus/professional-colleague-agents-ru/01-pyat-tipov.md` | 0 | 🔴 Очень сложный | 723 | 95 | 7.6 |
| `docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md` | 0 | 🔴 Очень сложный | 654 | 96 | 6.8 |
| `docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md` | 0 | 🔴 Очень сложный | 648 | 58 | 11.2 |
| `docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md` | 0 | 🔴 Очень сложный | 735 | 98 | 7.5 |
| `docs/nautilus/professional-colleague-agents-ru/05-ekonomika.md` | 0 | 🔴 Очень сложный | 598 | 63 | 9.5 |
| `docs/nautilus/professional-colleague-agents-ru/06-riski.md` | 0 | 🔴 Очень сложный | 1043 | 149 | 7.0 |
| `docs/nautilus/professional-colleague-agents-ru/07-oblasti-primeneniya.md` | 0 | 🔴 Очень сложный | 661 | 98 | 6.7 |
| `docs/nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md` | 0 | 🔴 Очень сложный | 780 | 59 | 13.2 |
| `docs/nautilus/professional-colleague-agents-ru/09-svyaz-s-drugimi.md` | 0 | 🔴 Очень сложный | 558 | 64 | 8.7 |
| `docs/nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md` | 0 | 🔴 Очень сложный | 294 | 39 | 7.5 |
| `docs/nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md` | 0 | 🔴 Очень сложный | 234 | 28 | 8.4 |
| `docs/nautilus/professional-colleague-agents-ru/12-zaklyuchenie.md` | 0 | 🔴 Очень сложный | 402 | 43 | 9.3 |
| `docs/nautilus/representative-agent-layer-en/00-abstract.md` | 0 | 🔴 Очень сложный | 347 | 29 | 12.0 |
| `docs/nautilus/representative-agent-layer-en/01-cinderella-syndrome.md` | 0 | 🔴 Очень сложный | 766 | 55 | 13.9 |
| `docs/nautilus/representative-agent-layer-en/02-historical-precedents.md` | 0 | 🔴 Очень сложный | 874 | 76 | 11.5 |
| `docs/nautilus/representative-agent-layer-en/03-what-makes-representative-agent.md` | 0 | 🔴 Очень сложный | 597 | 75 | 8.0 |
| `docs/nautilus/representative-agent-layer-en/04-ten-domains.md` | 0 | 🔴 Очень сложный | 1509 | 171 | 8.8 |
| `docs/nautilus/representative-agent-layer-en/05-architectural-specification.md` | 0 | 🔴 Очень сложный | 584 | 61 | 9.6 |
| `docs/nautilus/representative-agent-layer-en/06-ethical-framework.md` | 0 | 🔴 Очень сложный | 425 | 30 | 14.2 |
| `docs/nautilus/representative-agent-layer-en/07-governance-oversight.md` | 0 | 🔴 Очень сложный | 373 | 21 | 17.8 |
| `docs/nautilus/representative-agent-layer-en/08-risks-mitigations.md` | 0 | 🔴 Очень сложный | 442 | 25 | 17.7 |
| `docs/nautilus/representative-agent-layer-en/09-phased-rollout.md` | 0 | 🔴 Очень сложный | 389 | 16 | 24.3 |
| `docs/nautilus/representative-agent-layer-en/10-open-questions.md` | 0 | 🔴 Очень сложный | 358 | 35 | 10.2 |
| `docs/nautilus/representative-agent-layer-en/11-call-for-collaboration.md` | 0 | 🔴 Очень сложный | 351 | 36 | 9.8 |
| `docs/nautilus/representative-agent-layer-en/12-closing.md` | 0 | 🔴 Очень сложный | 2430 | 207 | 11.7 |
| `docs/nautilus/representative-agent-layer-ru/00-abstract.md` | 0 | 🔴 Очень сложный | 102 | 19 | 5.4 |
| `docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md` | 0 | 🔴 Очень сложный | 663 | 55 | 12.1 |
| `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md` | 0 | 🔴 Очень сложный | 813 | 77 | 10.6 |
| `docs/nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md` | 0 | 🔴 Очень сложный | 553 | 76 | 7.3 |
| `docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md` | 0 | 🔴 Очень сложный | 1425 | 170 | 8.4 |
| `docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md` | 0 | 🔴 Очень сложный | 533 | 61 | 8.7 |
| `docs/nautilus/representative-agent-layer-ru/06-eticheskaya-ramka.md` | 0 | 🔴 Очень сложный | 391 | 27 | 14.5 |
| `docs/nautilus/representative-agent-layer-ru/07-upravlenie-nadzor.md` | 0 | 🔴 Очень сложный | 341 | 21 | 16.2 |
| `docs/nautilus/representative-agent-layer-ru/08-riski-mery.md` | 0 | 🔴 Очень сложный | 500 | 36 | 13.9 |
| `docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md` | 0 | 🔴 Очень сложный | 370 | 19 | 19.5 |
| `docs/nautilus/representative-agent-layer-ru/10-otkrytye-voprosy.md` | 0 | 🔴 Очень сложный | 326 | 34 | 9.6 |
| `docs/nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md` | 0 | 🔴 Очень сложный | 326 | 39 | 8.4 |
| `docs/nautilus/representative-agent-layer-ru/12-zaklyuchenie.md` | 0 | 🔴 Очень сложный | 3836 | 319 | 12.0 |
| `docs/nautilus/representative-agent-layer-ru/README.md` | 0 | 🔴 Очень сложный | 89 | 26 | 3.4 |
| `docs/nautilus/review-methodology/00-tldr.md` | 0 | 🔴 Очень сложный | 164 | 19 | 8.6 |
| `docs/nautilus/review-methodology/01-context-motivation.md` | 0 | 🔴 Очень сложный | 265 | 20 | 13.2 |
| `docs/nautilus/review-methodology/02-formal-workflow.md` | 0 | 🔴 Очень сложный | 200 | 18 | 11.1 |
| `docs/nautilus/review-methodology/03-consolidation-principles.md` | 0 | 🔴 Очень сложный | 273 | 20 | 13.7 |
| `docs/nautilus/review-methodology/04-fallback-ratio-question.md` | 0 | 🔴 Очень сложный | 222 | 28 | 7.9 |
| `docs/nautilus/review-methodology/05-conditions-of-applicability.md` | 0 | 🔴 Очень сложный | 219 | 15 | 14.6 |
| `docs/nautilus/review-methodology/06-relation-existing-methodologies.md` | 0 | 🔴 Очень сложный | 268 | 30 | 8.9 |
| `docs/nautilus/review-methodology/07-why-valid-for-ai.md` | 0 | 🔴 Очень сложный | 197 | 16 | 12.3 |
| `docs/nautilus/review-methodology/08-implementation-nautilus.md` | 0 | 🔴 Очень сложный | 220 | 21 | 10.5 |
| `docs/nautilus/review-methodology/09-limitations-open-questions.md` | 0 | 🔴 Очень сложный | 289 | 31 | 9.3 |
| `docs/nautilus/review-methodology/10-checklist.md` | 0 | 🔴 Очень сложный | 191 | 19 | 10.1 |
| `docs/nautilus/review-methodology/11-application-plan-current-docs.md` | 0 | 🔴 Очень сложный | 158 | 20 | 7.9 |
| `docs/nautilus/review-methodology/12-appendix-a-header-warning.md` | 0 | 🔴 Очень сложный | 109 | 12 | 9.1 |
| `docs/nautilus/review-methodology/13-appendix-b-examples.md` | 0 | 🔴 Очень сложный | 154 | 20 | 7.7 |
| `docs/nautilus/review-methodology/14-main-technical-risks.md` | 0 | 🔴 Очень сложный | 127 | 14 | 9.1 |
| `docs/nautilus/review-methodology/15-appendix-c-history.md` | 0 | 🔴 Очень сложный | 98 | 12 | 8.2 |
| `docs/nautilus/review-methodology/16-glossary.md` | 0 | 🔴 Очень сложный | 856 | 83 | 10.3 |
| `docs/nautilus/supply-demand/00-question-supply-demand.md` | 0 | 🔴 Очень сложный | 424 | 9 | 47.1 |
| `docs/nautilus/supply-demand/01-three-related-themes.md` | 0 | 🔴 Очень сложный | 2639 | 199 | 13.3 |
| `docs/nautilus/transmission-box/00-question-mountain-to-person.md` | 0 | 🔴 Очень сложный | 514 | 11 | 46.7 |
| `docs/nautilus/transmission-box/01-completing-loop.md` | 0 | 🔴 Очень сложный | 2845 | 171 | 16.6 |
| `docs/reading-paths.md` | 0 | 🔴 Очень сложный | 721 | 134 | 5.4 |
| `docs/svyazi-2-0/README.md` | 0 | 🔴 Очень сложный | 115 | 11 | 10.5 |
| `docs/svyazi-2-0/architecture/card-envelope.md` | 0 | 🔴 Очень сложный | 136 | 9 | 15.1 |
| `docs/svyazi-2-0/architecture/evidence-envelope.md` | 0 | 🔴 Очень сложный | 184 | 14 | 13.1 |
| `docs/svyazi-2-0/architecture/gaps.md` | 0 | 🔴 Очень сложный | 601 | 23 | 26.1 |
| `docs/svyazi-2-0/architecture/integration-spec.md` | 0 | 🔴 Очень сложный | 228 | 15 | 15.2 |
| `docs/svyazi-2-0/architecture/memory-write-policy.md` | 0 | 🔴 Очень сложный | 148 | 8 | 18.5 |
| `docs/svyazi-2-0/architecture/review-record.md` | 0 | 🔴 Очень сложный | 89 | 8 | 11.1 |
| `docs/svyazi-2-0/architecture/skill-tool-policy.md` | 0 | 🔴 Очень сложный | 144 | 10 | 14.4 |
| `docs/svyazi-2-0/components/agentfs.md` | 0 | 🔴 Очень сложный | 105 | 10 | 10.5 |
| `docs/svyazi-2-0/components/autoresearch-sequential.md` | 0 | 🔴 Очень сложный | 120 | 10 | 12.0 |
| `docs/svyazi-2-0/components/graph-rag.md` | 0 | 🔴 Очень сложный | 100 | 9 | 11.1 |
| `docs/svyazi-2-0/components/legal-rag.md` | 0 | 🔴 Очень сложный | 100 | 9 | 11.1 |
| `docs/svyazi-2-0/components/mclaude.md` | 0 | 🔴 Очень сложный | 93 | 9 | 10.3 |
| `docs/svyazi-2-0/components/rufler.md` | 0 | 🔴 Очень сложный | 93 | 9 | 10.3 |
| `docs/svyazi-2-0/components/security-routing-plane.md` | 0 | 🔴 Очень сложный | 184 | 13 | 14.2 |
| `docs/svyazi-2-0/components/self-aware-mcp.md` | 0 | 🔴 Очень сложный | 133 | 9 | 14.8 |
| `docs/svyazi-2-0/components/svyazi.md` | 0 | 🔴 Очень сложный | 103 | 9 | 11.4 |
| `docs/svyazi-2-0/components/voice-stack.md` | 0 | 🔴 Очень сложный | 125 | 9 | 13.9 |
| `docs/svyazi-2-0/components/yjs-automerge.md` | 0 | 🔴 Очень сложный | 113 | 9 | 12.6 |
| `docs/svyazi-2-0/ensembles/A-collaboration-os.md` | 0 | 🔴 Очень сложный | 202 | 13 | 15.5 |
| `docs/svyazi-2-0/ensembles/B-forensic-rag.md` | 0 | 🔴 Очень сложный | 201 | 13 | 15.5 |
| `docs/svyazi-2-0/ensembles/C-multi-agent-factory.md` | 0 | 🔴 Очень сложный | 213 | 12 | 17.8 |
| `docs/svyazi-2-0/ensembles/D-voice-first-mesh.md` | 0 | 🔴 Очень сложный | 230 | 17 | 13.5 |
| `docs/svyazi-2-0/ensembles/E-execution-plane.md` | 0 | 🔴 Очень сложный | 207 | 13 | 15.9 |
| `docs/svyazi-2-0/ensembles/F-evidence-backed-intake.md` | 0 | 🔴 Очень сложный | 213 | 13 | 16.4 |
| `docs/svyazi-2-0/ensembles/G-federated-local-graph.md` | 0 | 🔴 Очень сложный | 231 | 15 | 15.4 |
| `docs/svyazi-2-0/ensembles/H-research-to-product-flywheel.md` | 0 | 🔴 Очень сложный | 198 | 13 | 15.2 |
| `docs/svyazi-2-0/limitations/conclusions.md` | 0 | 🔴 Очень сложный | 319 | 19 | 16.8 |
| `docs/svyazi-2-0/limitations/do-not-glue.md` | 0 | 🔴 Очень сложный | 335 | 21 | 16.0 |
| `docs/svyazi-2-0/limitations/license-tree.md` | 0 | 🔴 Очень сложный | 259 | 24 | 10.8 |
| `docs/svyazi-2-0/outreach/first-contacts.md` | 0 | 🔴 Очень сложный | 239 | 24 | 10.0 |
| `docs/svyazi-2-0/outreach/message-template.md` | 0 | 🔴 Очень сложный | 203 | 20 | 10.2 |
| `docs/svyazi-2-0/outreach/narrow-questions.md` | 0 | 🔴 Очень сложный | 288 | 21 | 13.7 |
| `docs/svyazi-2-0/overview/continuation-intro.md` | 0 | 🔴 Очень сложный | 261 | 13 | 20.1 |
| `docs/svyazi-2-0/overview/executive-summary.md` | 0 | 🔴 Очень сложный | 423 | 21 | 20.1 |
| `docs/svyazi-2-0/overview/methodology.md` | 0 | 🔴 Очень сложный | 258 | 21 | 12.3 |
| `docs/svyazi-2-0/overview/projects-map.md` | 0 | 🔴 Очень сложный | 1272 | 100 | 12.7 |
| `docs/svyazi-2-0/prototype/mvp-plan.md` | 0 | 🔴 Очень сложный | 275 | 14 | 19.6 |
| `docs/svyazi-2-0/prototype/risks.md` | 0 | 🔴 Очень сложный | 275 | 15 | 18.3 |
| `docs/svyazi-2-0/prototype/roadmap.md` | 0 | 🔴 Очень сложный | 560 | 28 | 20.0 |
| `docs/svyazi-2-0/security/budget-routing.md` | 0 | 🔴 Очень сложный | 294 | 17 | 17.3 |
| `docs/svyazi-2-0/security/default-policy.md` | 0 | 🔴 Очень сложный | 312 | 20 | 15.6 |
| `docs/svyazi-2-0/security/privacy.md` | 0 | 🔴 Очень сложный | 131 | 12 | 10.9 |
| `docs/technology-combinations/README.md` | 0 | 🔴 Очень сложный | 136 | 12 | 11.3 |
| `docs/technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md` | 0 | 🔴 Очень сложный | 237 | 15 | 15.8 |
| `docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md` | 0 | 🔴 Очень сложный | 173 | 15 | 11.5 |
| `docs/technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md` | 0 | 🔴 Очень сложный | 193 | 12 | 16.1 |
| `docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md` | 0 | 🔴 Очень сложный | 197 | 15 | 13.1 |
| `docs/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md` | 0 | 🔴 Очень сложный | 207 | 12 | 17.2 |
| `docs/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md` | 0 | 🔴 Очень сложный | 213 | 15 | 14.2 |
| `docs/technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md` | 0 | 🔴 Очень сложный | 197 | 12 | 16.4 |
| `docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md` | 0 | 🔴 Очень сложный | 562 | 28 | 20.1 |
| `docs/technology-combinations/combinations/09-agent-orchestration-stack.md` | 0 | 🔴 Очень сложный | 196 | 12 | 16.3 |
| `docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md` | 0 | 🔴 Очень сложный | 193 | 10 | 19.3 |
| `docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md` | 0 | 🔴 Очень сложный | 198 | 9 | 22.0 |
| `docs/technology-combinations/combinations/12-multi-agent-observability-stack.md` | 0 | 🔴 Очень сложный | 176 | 10 | 17.6 |
| `docs/technology-combinations/combinations/13-legal-document-transpiler.md` | 0 | 🔴 Очень сложный | 186 | 9 | 20.7 |
| `docs/technology-combinations/combinations/14-local-first-agent-development-environment.md` | 0 | 🔴 Очень сложный | 497 | 19 | 26.2 |
| `docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md` | 0 | 🔴 Очень сложный | 240 | 8 | 30.0 |
| `docs/technology-combinations/combinations/16-adversarial-multi-agent-code-review.md` | 0 | 🔴 Очень сложный | 246 | 12 | 20.5 |
| `docs/technology-combinations/combinations/17-distributed-agent-memory-with-graph.md` | 0 | 🔴 Очень сложный | 213 | 8 | 26.6 |
| `docs/technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md` | 0 | 🔴 Очень сложный | 230 | 14 | 16.4 |
| `docs/technology-combinations/combinations/19-multi-agent-observability-platform.md` | 0 | 🔴 Очень сложный | 574 | 16 | 35.9 |
| `docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md` | 0 | 🔴 Очень сложный | 240 | 8 | 30.0 |
| `docs/technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md` | 0 | 🔴 Очень сложный | 249 | 12 | 20.8 |
| `docs/technology-combinations/combinations/22-russian-international-oss-stack.md` | 0 | 🔴 Очень сложный | 225 | 9 | 25.0 |
| `docs/technology-combinations/combinations/23-security-first-code-review-pipeline.md` | 0 | 🔴 Очень сложный | 181 | 13 | 13.9 |
| `docs/technology-combinations/combinations/24-mega-integration-full-stack.md` | 0 | 🔴 Очень сложный | 466 | 14 | 33.3 |
| `docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md` | 0 | 🔴 Очень сложный | 278 | 20 | 13.9 |
| `docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md` | 0 | 🔴 Очень сложный | 230 | 13 | 17.7 |
| `docs/technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md` | 0 | 🔴 Очень сложный | 202 | 13 | 15.5 |
| `docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md` | 0 | 🔴 Очень сложный | 227 | 12 | 18.9 |
| `docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md` | 0 | 🔴 Очень сложный | 202 | 14 | 14.4 |
| `docs/technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md` | 0 | 🔴 Очень сложный | 401 | 18 | 22.3 |
| `docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md` | 0 | 🔴 Очень сложный | 240 | 12 | 20.0 |
| `docs/technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md` | 0 | 🔴 Очень сложный | 238 | 12 | 19.8 |
| `docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md` | 0 | 🔴 Очень сложный | 215 | 13 | 16.5 |
| `docs/technology-combinations/combinations/34-distributed-event-store-with-paxos.md` | 0 | 🔴 Очень сложный | 189 | 9 | 21.0 |
| `docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md` | 0 | 🔴 Очень сложный | 400 | 17 | 23.5 |
| `docs/technology-combinations/mega-stacks/01-legal-ai-stack.md` | 0 | 🔴 Очень сложный | 163 | 18 | 9.1 |
| `docs/technology-combinations/mega-stacks/02-ultimate-legal-ai.md` | 0 | 🔴 Очень сложный | 140 | 13 | 10.8 |
| `docs/technology-combinations/mega-stacks/04-event-sourcing-consensus.md` | 0 | 🔴 Очень сложный | 135 | 14 | 9.6 |
| `docs/technology-combinations/properties/README.md` | 0 | 🔴 Очень сложный | 16 | 2 | 8.0 |
| `docs/technology-combinations/research-reports/README.md` | 0 | 🔴 Очень сложный | 16 | 4 | 4.0 |
| `docs/technology-combinations/research-reports/continuation-10-domains.md` | 0 | 🔴 Очень сложный | 246 | 33 | 7.5 |
| `docs/technology-combinations/research-reports/sozialrecht-35-combinations.md` | 0 | 🔴 Очень сложный | 195 | 20 | 9.8 |
| `docs/technology-combinations/synthesis-tables/01-08-summary.md` | 0 | 🔴 Очень сложный | 342 | 26 | 13.2 |
| `docs/technology-combinations/synthesis-tables/09-14-extended.md` | 0 | 🔴 Очень сложный | 181 | 18 | 10.1 |
| `docs/technology-combinations/synthesis-tables/15-19-extended.md` | 0 | 🔴 Очень сложный | 153 | 16 | 9.6 |
| `docs/technology-combinations/synthesis-tables/20-24-final.md` | 0 | 🔴 Очень сложный | 189 | 21 | 9.0 |
| `docs/technology-combinations/synthesis-tables/31-35-final.md` | 0 | 🔴 Очень сложный | 200 | 17 | 11.8 |
| `docs/templates/contact-outreach.md` | 0 | 🔴 Очень сложный | 108 | 11 | 9.8 |
| `docs/templates/decision-record.md` | 0 | 🔴 Очень сложный | 88 | 10 | 8.8 |
| `docs/templates/ensemble.md` | 0 | 🔴 Очень сложный | 151 | 16 | 9.4 |
| `docs/templates/project-component.md` | 0 | 🔴 Очень сложный | 129 | 17 | 7.6 |
| `docs/templates/research-note.md` | 0 | 🔴 Очень сложный | 105 | 16 | 6.6 |
| `docs/VERSION_DIFF.md` | 0.2 | 🔴 Очень сложный | 16 | 1 | 16.0 |
| `docs/svyazi-2-0/components/knowledge-space.md` | 0.3 | 🔴 Очень сложный | 101 | 9 | 11.2 |
| `docs/lorenzo-agent/17-honestly-ne-znaesh.md` | 0.4 | 🔴 Очень сложный | 125 | 11 | 11.4 |
| `docs/nautilus/infrastructure-layer-b-en/08-recursive-insight.md` | 0.5 | 🔴 Очень сложный | 333 | 30 | 11.1 |
| `docs/svyazi-2-0/components/yodoca.md` | 0.7 | 🔴 Очень сложный | 104 | 9 | 11.6 |
| `docs/habr-unique-projects/software-pairs/5-browser-agents-headless.md` | 0.8 | 🔴 Очень сложный | 434 | 29 | 15.0 |
| `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` | 1.1 | 🔴 Очень сложный | 687 | 60 | 11.4 |
| `docs/02-anthropic-vacancies/224-acknowledgments.md` | 1.1 | 🔴 Очень сложный | 202 | 18 | 11.2 |
| `docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md` | 1.3 | 🔴 Очень сложный | 304 | 22 | 13.8 |
| `docs/TABLES.md` | 1.4 | 🔴 Очень сложный | 34077 | 3664 | 9.3 |
| `docs/svyazi-2-0/components/agent-memory-mcp.md` | 1.4 | 🔴 Очень сложный | 129 | 9 | 14.3 |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 1.5 | 🔴 Очень сложный | 74 | 10 | 7.4 |
| `docs/nautilus/npp-v1-0/09-query-flow.md` | 1.5 | 🔴 Очень сложный | 143 | 22 | 6.5 |
| `docs/02-anthropic-vacancies/65-readme-md.md` | 1.6 | 🔴 Очень сложный | 131 | 15 | 8.7 |
| `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` | 1.7 | 🔴 Очень сложный | 130 | 18 | 7.2 |
| `docs/02-anthropic-vacancies/286-acknowledgments.md` | 1.7 | 🔴 Очень сложный | 228 | 19 | 12.0 |
| `docs/glossary/authors-by-name.md` | 1.8 | 🔴 Очень сложный | 603 | 94 | 6.4 |
| `docs/nautilus/infrastructure-layer-b-en/11-practical-recommendations.md` | 1.8 | 🔴 Очень сложный | 320 | 39 | 8.2 |
| `docs/02-anthropic-vacancies/35-passports-info1-md.md` | 2.0 | 🔴 Очень сложный | 105 | 13 | 8.1 |
| `docs/nautilus/ingit-cowork-en/01-cowork-discovery.md` | 2.0 | 🔴 Очень сложный | 606 | 58 | 10.4 |
| `docs/nautilus/ingit-cowork-en/05-four-integration-paths.md` | 2.0 | 🔴 Очень сложный | 641 | 56 | 11.4 |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | 2.1 | 🔴 Очень сложный | 121 | 18 | 6.7 |
| `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` | 2.1 | 🔴 Очень сложный | 824 | 60 | 13.7 |
| `docs/svyazi-2-0/components/memnet.md` | 2.2 | 🔴 Очень сложный | 103 | 9 | 11.4 |
| `docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md` | 2.7 | 🔴 Очень сложный | 749 | 57 | 13.1 |
| `docs/nautilus/representative-agent-layer-en/README.md` | 2.8 | 🔴 Очень сложный | 89 | 26 | 3.4 |
| `docs/nautilus/ingit-cowork-en/03-ingit-provides.md` | 2.9 | 🔴 Очень сложный | 771 | 57 | 13.5 |
| `docs/KEYWORD_INDEX.md` | 3.0 | 🔴 Очень сложный | 120 | 9 | 13.3 |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | 3.1 | 🔴 Очень сложный | 133 | 13 | 10.2 |
| `docs/svyazi-2-0/components/ngt-memory.md` | 3.3 | 🔴 Очень сложный | 109 | 10 | 10.9 |
| `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` | 3.4 | 🔴 Очень сложный | 164 | 8 | 20.5 |
| `docs/02-anthropic-vacancies/356-твой-workflow.md` | 3.4 | 🔴 Очень сложный | 200 | 20 | 10.0 |
| `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` | 3.5 | 🔴 Очень сложный | 141 | 8 | 17.6 |
| `docs/svyazi-2-0/overview/README.md` | 3.9 | 🔴 Очень сложный | 28 | 8 | 3.5 |
| `docs/technology-combinations/synthesis-tables/25-30-extended.md` | 4.0 | 🔴 Очень сложный | 191 | 19 | 10.1 |
| `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` | 4.2 | 🔴 Очень сложный | 158 | 8 | 19.8 |
| `docs/ai-collaborations/candidates/README.md` | 4.4 | 🔴 Очень сложный | 30 | 6 | 5.0 |
| `docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md` | 4.4 | 🔴 Очень сложный | 246 | 17 | 14.5 |
| `docs/lorenzo-agent/specification/README.md` | 4.5 | 🔴 Очень сложный | 86 | 24 | 3.6 |
| `docs/svyazi-2-0/components/hybrid-rag.md` | 4.5 | 🔴 Очень сложный | 94 | 9 | 10.4 |
| `docs/svyazi-2-0/components/research-docs-liteparse.md` | 4.5 | 🔴 Очень сложный | 114 | 10 | 11.4 |
| `docs/habr-unique-projects/search-strategy/README.md` | 4.6 | 🔴 Очень сложный | 25 | 2 | 12.5 |
| `docs/nautilus/ingit-cowork-en/06-refined-ingit-scope.md` | 4.7 | 🔴 Очень сложный | 337 | 23 | 14.7 |
| `docs/nautilus/review-methodology/README.md` | 4.7 | 🔴 Очень сложный | 131 | 34 | 3.9 |
| `docs/02-anthropic-vacancies/181-12-closing.md` | 5.0 | 🔴 Очень сложный | 247 | 22 | 11.2 |
| `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | 5.0 | 🔴 Очень сложный | 279 | 21 | 13.3 |
| `docs/02-anthropic-vacancies/45-passports-pro2-md.md` | 5.0 | 🔴 Очень сложный | 105 | 14 | 7.5 |
| `docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md` | 5.0 | 🔴 Очень сложный | 276 | 32 | 8.6 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/README.md` | 5.4 | 🔴 Очень сложный | 96 | 24 | 4.0 |
| `docs/svyazi-2-0/components/ai-factory.md` | 5.4 | 🔴 Очень сложный | 107 | 10 | 10.7 |
| `docs/02-anthropic-vacancies/279-existing-approximations.md` | 5.6 | 🔴 Очень сложный | 652 | 39 | 16.7 |
| `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` | 5.8 | 🔴 Очень сложный | 898 | 70 | 12.8 |
| `docs/CODE_BLOCKS.md` | 5.8 | 🔴 Очень сложный | 459 | 53 | 8.7 |
| `docs/nautilus/infrastructure-layer-b-en/05-why-not-built.md` | 5.8 | 🔴 Очень сложный | 338 | 35 | 9.7 |
| `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` | 5.9 | 🔴 Очень сложный | 705 | 74 | 9.5 |
| `docs/lorenzo-agent/naming/00-question-lorenzo-codename.md` | 5.9 | 🔴 Очень сложный | 228 | 14 | 16.3 |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | 6.1 | 🔴 Очень сложный | 52 | 6 | 8.7 |
| `docs/STALENESS.md` | 6.5 | 🔴 Очень сложный | 262 | 13 | 20.2 |
| `docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md` | 6.7 | 🔴 Очень сложный | 320 | 28 | 11.4 |
| `docs/02-anthropic-vacancies/281-the-recursive-insight.md` | 7.1 | 🔴 Очень сложный | 389 | 34 | 11.4 |
| `docs/02-anthropic-vacancies/README.md` | 7.1 | 🔴 Очень сложный | 3139 | 710 | 4.4 |
| `docs/habr-unique-projects/final-ensembles/README.md` | 7.1 | 🔴 Очень сложный | 32 | 8 | 4.0 |
| `docs/LANGUAGE_STATS.md` | 7.6 | 🔴 Очень сложный | 474 | 9 | 52.7 |
| `docs/lorenzo-agent/naming/README.md` | 8.8 | 🔴 Очень сложный | 39 | 8 | 4.9 |
| `docs/nautilus/transmission-box/README.md` | 9.0 | 🔴 Очень сложный | 22 | 4 | 5.5 |
| `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` | 9.1 | 🔴 Очень сложный | 609 | 46 | 13.2 |
| `docs/02-anthropic-vacancies/55-passports-meta-md.md` | 9.3 | 🔴 Очень сложный | 105 | 13 | 8.1 |
| `docs/nautilus/ingit-cowork-en/02-cowork-provides.md` | 9.3 | 🔴 Очень сложный | 593 | 50 | 11.9 |
| `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` | 9.7 | 🔴 Очень сложный | 372 | 44 | 8.5 |
| `docs/anthropic-vacancies/clusters/README.md` | 9.9 | 🔴 Очень сложный | 100 | 32 | 3.1 |
| `docs/nautilus/infrastructure-layer-b-en/03-two-layer-stack.md` | 10.0 | 🔴 Очень сложный | 350 | 28 | 12.5 |
| `docs/nautilus/infrastructure-layer-b-ru/README.md` | 10.5 | 🔴 Очень сложный | 81 | 26 | 3.1 |
| `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` | 10.6 | 🔴 Очень сложный | 815 | 80 | 10.2 |
| `docs/02-anthropic-vacancies/169-table-of-contents.md` | 10.7 | 🔴 Очень сложный | 129 | 22 | 5.9 |
| `docs/lorenzo-agent/README.md` | 10.9 | 🔴 Очень сложный | 162 | 44 | 3.7 |
| `docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md` | 11.0 | 🔴 Очень сложный | 208 | 22 | 9.5 |
| `docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md` | 11.1 | 🔴 Очень сложный | 407 | 40 | 10.2 |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 11.3 | 🔴 Очень сложный | 14 | 1 | 14.0 |
| `docs/nautilus/community-discussions/habr-article-1-reaction/README.md` | 11.4 | 🔴 Очень сложный | 20 | 4 | 5.0 |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | 11.7 | 🔴 Очень сложный | 91 | 17 | 5.4 |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 12.0 | 🔴 Очень сложный | 74 | 4 | 18.5 |
| `docs/nautilus/community-discussions/habr-article-2-reaction/README.md` | 12.4 | 🔴 Очень сложный | 16 | 4 | 4.0 |
| `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` | 12.5 | 🔴 Очень сложный | 321 | 37 | 8.7 |
| `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` | 12.6 | 🔴 Очень сложный | 167 | 11 | 15.2 |
| `docs/nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md` | 12.6 | 🔴 Очень сложный | 296 | 26 | 11.4 |
| `docs/nautilus/infrastructure-layer-b-en/02-why-document-exists.md` | 12.6 | 🔴 Очень сложный | 296 | 26 | 11.4 |
| `docs/nautilus/ingit-cowork-en/07-practical-first-steps.md` | 12.6 | 🔴 Очень сложный | 338 | 36 | 9.4 |
| `docs/templates/README.md` | 12.7 | 🔴 Очень сложный | 31 | 10 | 3.1 |
| `docs/VOCABULARY.md` | 12.8 | 🔴 Очень сложный | 326 | 56 | 5.8 |
| `docs/nautilus/community-discussions/agent-changes-reality/README.md` | 12.8 | 🔴 Очень сложный | 22 | 4 | 5.5 |
| `docs/technology-combinations/combinations/README.md` | 13.3 | 🔴 Очень сложный | 429 | 70 | 6.1 |
| `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` | 13.4 | 🔴 Очень сложный | 384 | 40 | 9.6 |
| `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | 13.7 | 🔴 Очень сложный | 774 | 71 | 10.9 |
| `docs/CONCEPT_GRAPH.md` | 13.7 | 🔴 Очень сложный | 100 | 9 | 11.1 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md` | 13.9 | 🔴 Очень сложный | 44 | 10 | 4.4 |
| `docs/habr-unique-projects/extra-examples/README.md` | 13.9 | 🔴 Очень сложный | 114 | 26 | 4.4 |
| `docs/02-anthropic-vacancies/253-table-of-contents.md` | 14.6 | 🔴 Очень сложный | 141 | 23 | 6.1 |
| `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` | 15.0 | 🔴 Очень сложный | 537 | 49 | 11.0 |
| `docs/README.md` | 15.0 | 🔴 Очень сложный | 707 | 188 | 3.8 |
| `docs/CONSISTENCY.md` | 15.1 | 🔴 Очень сложный | 72 | 10 | 7.2 |
| `docs/01-svyazi/README.md` | 15.6 | 🔴 Очень сложный | 85 | 28 | 3.0 |
| `docs/nautilus/ingit-cowork-en/README.md` | 16.1 | 🔴 Очень сложный | 77 | 20 | 3.9 |
| `docs/02-anthropic-vacancies/275-why-this-document-exists.md` | 16.2 | 🔴 Очень сложный | 338 | 30 | 11.3 |
| `docs/nautilus/npp-v1-0/README.md` | 16.5 | 🔴 Очень сложный | 123 | 38 | 3.2 |
| `docs/EMPTY_SECTIONS.md` | 16.9 | 🔴 Очень сложный | 4845 | 713 | 6.8 |
| `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` | 17.1 | 🔴 Очень сложный | 398 | 33 | 12.1 |
| `docs/nautilus/professional-colleague-agents-en/README.md` | 17.2 | 🔴 Очень сложный | 90 | 26 | 3.5 |
| `docs/METRICS.md` | 17.6 | 🔴 Очень сложный | 120 | 12 | 10.0 |
| `docs/contacts/README.md` | 18.2 | 🔴 Очень сложный | 65 | 26 | 2.5 |
| `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` | 18.4 | 🔴 Очень сложный | 503 | 43 | 11.7 |
| `docs/nautilus/double-triangle-architecture/README.md` | 18.4 | 🔴 Очень сложный | 94 | 24 | 3.9 |
| `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` | 18.5 | 🔴 Очень сложный | 197 | 25 | 7.9 |
| `docs/nautilus/infrastructure-layer-b-en/07-specific-case.md` | 18.7 | 🔴 Очень сложный | 620 | 61 | 10.2 |
| `docs/technology-combinations/mega-stacks/03-dsl-ast.md` | 19.0 | 🔴 Очень сложный | 113 | 14 | 8.1 |
| `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` | 19.3 | 🔴 Очень сложный | 485 | 52 | 9.3 |
| `docs/nautilus/composite-skills-agents/README.md` | 19.9 | 🔴 Очень сложный | 97 | 26 | 3.7 |
| `docs/NAMED_ENTITIES.md` | 20.2 | 🔴 Очень сложный | 455 | 35 | 13.0 |
| `docs/DIGEST_AUTO.md` | 20.4 | 🔴 Очень сложный | 201 | 22 | 9.1 |
| `docs/nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md` | 20.6 | 🔴 Очень сложный | 207 | 29 | 7.1 |
| `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` | 21.5 | 🔴 Очень сложный | 736 | 76 | 9.7 |
| `docs/PRIORITIES.md` | 21.7 | 🔴 Очень сложный | 608 | 132 | 4.6 |
| `docs/02-anthropic-vacancies/211-table-of-contents.md` | 21.8 | 🔴 Очень сложный | 165 | 22 | 7.5 |
| `docs/ai-collaborations/ensembles/README.md` | 22.5 | 🔴 Очень сложный | 79 | 18 | 4.4 |
| `docs/svyazi-2-0/outreach/README.md` | 22.7 | 🔴 Очень сложный | 23 | 6 | 3.8 |
| `docs/anthropic-vacancies/extra-collaborator-findings/README.md` | 23.3 | 🔴 Очень сложный | 59 | 14 | 4.2 |
| `docs/nautilus/supply-demand/README.md` | 24.2 | 🔴 Очень сложный | 21 | 4 | 5.2 |
| `docs/habr-unique-projects/deep-pairs/README.md` | 24.3 | 🔴 Очень сложный | 64 | 16 | 4.0 |
| `docs/svyazi-2-0/ensembles/README.md` | 24.4 | 🔴 Очень сложный | 65 | 16 | 4.1 |
| `docs/COMPARE.md` | 25.5 | 🔴 Очень сложный | 126 | 10 | 12.6 |
| `docs/svyazi-2-0/security/README.md` | 26.2 | 🔴 Очень сложный | 22 | 6 | 3.7 |
| `docs/nautilus/professional-colleague-agents-ru/README.md` | 26.3 | 🔴 Очень сложный | 84 | 26 | 3.2 |
| `docs/svyazi-2-0/limitations/README.md` | 26.4 | 🔴 Очень сложный | 23 | 6 | 3.8 |
| `docs/nautilus/okwf-concept/README.md` | 28.5 | 🔴 Очень сложный | 73 | 22 | 3.3 |
| `docs/02-anthropic-vacancies/308-table-of-contents.md` | 28.8 | 🔴 Очень сложный | 147 | 21 | 7.0 |
| `docs/nautilus/privacy-federation/README.md` | 29.1 | 🔴 Очень сложный | 51 | 10 | 5.1 |
| `docs/habr-unique-projects/key-findings/README.md` | 30.1 | 🟠 Сложный | 42 | 12 | 3.5 |
| `docs/lorenzo-agent/phased-deployment/README.md` | 30.1 | 🟠 Сложный | 69 | 18 | 3.8 |
| `docs/nautilus/npp-humanitarian-extension/README.md` | 30.4 | 🟠 Сложный | 72 | 12 | 6.0 |
| `docs/svyazi-2-0/architecture/README.md` | 30.4 | 🟠 Сложный | 49 | 13 | 3.8 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md` | 31.3 | 🟠 Сложный | 43 | 10 | 4.3 |
| `docs/nautilus/npp-v1-1/README.md` | 32.1 | 🟠 Сложный | 141 | 45 | 3.1 |
| `docs/05-habr-projects/memory/README.md` | 32.8 | 🟠 Сложный | 19 | 4 | 4.8 |
| `docs/03-technology-combinations/README.md` | 33.7 | 🟠 Сложный | 39 | 10 | 3.9 |
| `docs/nautilus/composite-skills-agents-companion-mentors/README.md` | 34.3 | 🟠 Сложный | 42 | 8 | 5.2 |
| `docs/ai-collaborations/continuation/README.md` | 34.8 | 🟠 Сложный | 92 | 20 | 4.6 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/README.md` | 36.1 | 🟠 Сложный | 93 | 22 | 4.2 |
| `docs/LINKS.md` | 40.1 | 🟠 Сложный | 8 | 1 | 8.0 |
| `docs/anthropic-vacancies/nautilus-vs-camel/README.md` | 40.7 | 🟠 Сложный | 73 | 12 | 6.1 |
| `docs/badges/README.md` | 44.0 | 🟠 Сложный | 46 | 10 | 4.6 |
| `docs/technology-combinations/synthesis-tables/README.md` | 44.3 | 🟠 Сложный | 28 | 12 | 2.3 |
| `docs/glossary/README.md` | 44.8 | 🟠 Сложный | 23 | 6 | 3.8 |
| `docs/technology-combinations/mega-stacks/README.md` | 45.3 | 🟠 Сложный | 35 | 8 | 4.4 |
| `docs/nautilus/infrastructure-layer-b-en/README.md` | 45.5 | 🟠 Сложный | 102 | 28 | 3.6 |
| `docs/svyazi-2-0/components/README.md` | 47.7 | 🟠 Сложный | 113 | 34 | 3.3 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/README.md` | 48.1 | 🟠 Сложный | 60 | 12 | 5.0 |
| `docs/autofilled/components/README.md` | 63.3 | 🟡 Средний | 41 | 13 | 3.2 |
| `docs/habr-unique-projects/hardware-pairs/README.md` | 67.9 | 🟡 Средний | 50 | 14 | 3.6 |
| `docs/svyazi-2-0/prototype/README.md` | 71.6 | 🟢 Лёгкий | 20 | 5 | 4.0 |
| `docs/habr-unique-projects/software-pairs/README.md` | 74.0 | 🟢 Лёгкий | 50 | 12 | 4.2 |


### 111. Список чтения
_Файл: `docs/READING_LIST.md` | 6 колонок, 5 строк_

| # | Документ | Секция | Время | Слов | Score |
|---|----------|--------|-------|------|-------|
| 1 | [11 integration contracts](docs/01-svyazi/11-integration-contracts.md) | `01-svyazi` | 3 мин | 737 | 9.6 |
| 2 | [Интеграционный контракт, который стоит зафиксирова](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | `04-ai-collaborations` | 4 мин | 846 | 9.4 |
| 3 | [09 architectural gaps](docs/01-svyazi/09-architectural-gaps.md) | `01-svyazi` | 3 мин | 758 | 9.3 |
| 4 | [Архитектурные зазоры, которые важнее новых инструм](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | `04-ai-collaborations` | 4 мин | 805 | 9.2 |
| 5 | [03 component catalog](docs/01-svyazi/03-component-catalog.md) | `01-svyazi` | 6 мин | 1352 | 9.1 |


### 112. Содержание
_Файл: `docs/READING_ORDER.md` | 5 колонок, 395 строк_

| # | Уровень | Документ | Слов | Предварительно прочитать |
|---|---------|----------|------|--------------------------|
| 1 | 🟡 Средний | [04-ensembles-overview](docs/01-svyazi/04-ensembles-overview.md) | 1288 | — |
| 2 | 🟢 Начало | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 726 | — |
| 3 | 🟢 Начало | [Методика и рамка отбора проектов](docs/01-svyazi/02-methodology.md) | 480 | — |
| 4 | 🟢 Начало | [Продолжение исследования для Svyazi 2.0](docs/01-svyazi/00-intro-part2.md) | 6 | — |
| 5 | 🟡 Средний | [03-component-catalog](docs/01-svyazi/03-component-catalog.md) | 1383 | — |
| 6 | 🟢 Начало | [09-architectural-gaps](docs/01-svyazi/09-architectural-gaps.md) | 758 | `01-executive-summary.md`, `03-component-catalog.md` |
| 7 | 🟢 Начало | [11-integration-contracts](docs/01-svyazi/11-integration-contracts.md) | 737 | `09-architectural-gaps.md` |
| 8 | 🟢 Начало | [10-second-order-ensembles](docs/01-svyazi/10-second-order-ensembles.md) | 908 | `04-ensembles-overview.md` |
| 9 | 🟢 Начало | [06-security-privacy](docs/01-svyazi/06-security-privacy.md) | 823 | — |
| 10 | 🟡 Средний | [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md) | 1063 | — |
| 11 | 🟢 Начало | [12-roadmap](docs/01-svyazi/12-roadmap.md) | 722 | `07-mvp-planning.md`, `11-integration-contracts.md` |
| 12 | 🟢 Начало | [13-contacts](docs/01-svyazi/13-contacts.md) | 806 | — |
| 13 | 🟢 Начало | [14-limitations](docs/01-svyazi/14-limitations.md) | 638 | — |
| 14 | 🟢 Начало | [08-conclusions](docs/01-svyazi/08-conclusions.md) | 380 | — |
| 15 | 🟢 Начало | [Синтез: как проекты собираются вместе](docs/05-habr-projects/01-synthesis.md) | 136 | — |
| 16 | 🟢 Начало | [Авторы и контакты](docs/05-habr-projects/02-collaboration-partners.md) | 261 | — |
| 17 | 🟢 Начало | [Wikontic: семантический граф](docs/05-habr-projects/knowledge/wikontic.md) | 186 | — |
| 18 | 🟢 Начало | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 212 | — |
| 19 | 🟡 Средний | [MemNet: исследовательская память](docs/05-habr-projects/memory/memnet.md) | 7246 | — |
| 20 | 🟢 Начало | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 364 | — |
| 21 | 🟢 Начало | [Executive summary](docs/04-ai-collaborations/01-executive-summary.md) | 575 | — |
| 22 | 🟡 Средний | [Введение](docs/04-ai-collaborations/00-intro.md) | 11389 | — |
| 23 | 🟢 Начало | [Методика и рамка отбора](docs/04-ai-collaborations/02-методика-и-рамка-отбора.md) | 434 | — |
| 24 | 🟡 Средний | [Карта найденных проектов и паттернов](docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) | 1478 | — |
| 25 | 🟡 Средний | [Приоритетные ансамбли](docs/04-ai-collaborations/04-приоритетные-ансамбли.md) | 1340 | — |
| 26 | 🟡 Средний | [План прототипа и возможные контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) | 1130 | — |
| 27 | 🟢 Начало | [Безопасность, приватность и бюджетный роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) | 887 | — |
| 28 | 🟢 Начало | [Выводы](docs/04-ai-collaborations/07-выводы.md) | 470 | — |
| 29 | 🟢 Начало | [Что это продолжение добавляет](docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md) | 439 | — |
| 30 | 🟢 Начало | [Архитектурные зазоры, которые важнее новых ин](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | 821 | — |
| 31 | 🟢 Начало | [Новые ансамбли следующего шага](docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) | 984 | — |
| 32 | 🟢 Начало | [Интеграционный контракт, который стоит зафикс](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | 846 | — |
| 33 | 🟢 Начало | [Дорожная карта прототипа следующей итерации](docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md) | 787 | — |
| 34 | 🟢 Начало | [Контактная стратегия и узкие вопросы для авто](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) | 874 | — |
| 35 | 🟡 Средний | [Ограничения, лицензии и что пока лучше не скл](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md) | 3274 | — |
| 36 | 🟢 Начало | [Агентные системы и роутинг](docs/03-technology-combinations/01-agent-routing.md) | 298 | — |
| 37 | 🟢 Начало | [Графы знаний и Legal AI](docs/03-technology-combinations/02-knowledge-graphs.md) | 802 | — |
| 38 | 🟢 Начало | [Local-first и P2P стек](docs/03-technology-combinations/03-local-first.md) | 419 | — |
| 39 | 🟢 Начало | [Домен: немецкое социальное право](docs/03-technology-combinations/04-sozialrecht-domain.md) | 160 | — |
| 40 | 🟢 Начало | [Бенчмарки и производительность](docs/03-technology-combinations/05-benchmarks.md) | 915 | — |
| 41 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/58-content-overview.md) | 142 | — |
| 42 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/31-content-overview.md) | 39 | — |
| 43 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/38-content-overview.md) | 131 | — |
| 44 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/12-content-overview.md) | 41 | — |
| 45 | 🟢 Начало | [README.md](docs/02-anthropic-vacancies/65-readme-md.md) | 93 | — |
| 46 | 🔴 Продвинутый | [Интегральный анализ профиля svend4](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | 19144 | — |
| 47 | 🟢 Начало | [README-MCP.md— инструкция по установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) | 98 | — |
| 48 | 🟢 Начало | [Executive Summary](docs/02-anthropic-vacancies/153-executive-summary.md) | 369 | — |
| 49 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/48-content-overview.md) | 149 | — |
| 50 | 🟢 Начало | [REVIEW_METHODOLOGY.md](docs/02-anthropic-vacancies/105-review-methodology-md.md) | 74 | — |
| 51 | 🟢 Начало | [1. Introduction](docs/02-anthropic-vacancies/76-1-introduction.md) | 494 | — |
| 52 | 🔴 Продвинутый | [Введение](docs/02-anthropic-vacancies/00-intro.md) | 8934 | — |
| 53 | 🔴 Продвинутый | [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md) | 3207 | — |
| 54 | 🟢 Начало | [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md) | 383 | — |
| 55 | 🟢 Начало | [4. The Symbiotic Architecture](docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md) | 670 | — |
| 56 | 🟢 Начало | [4. Architecture of Professional Colleague Age](docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md) | 888 | — |
| 57 | 🟢 Начало | [PORTAL-PROTOCOL.md](docs/02-anthropic-vacancies/03-portal-protocol-md.md) | 75 | — |
| 58 | 🟢 Начало | [THE DOUBLE-TRIANGLE ARCHITECTURE.md](docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md) | 46 | — |
| 59 | 🟢 Начало | [2. The Double-Triangle Architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) | 753 | — |
| 60 | 🟡 Средний | [Appendix C: Quick-Start Architecture for SGB ](docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md) | 1717 | — |
| 61 | 🟢 Начало | [10. Risks Specific to Composite Architectures](docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md) | 800 | — |
| 62 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/04-abstract.md) | 126 | — |
| 63 | 🟢 Начало | [0. Status of This Document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md) | 101 | — |
| 64 | 🟢 Начало | [15. Security Considerations](docs/02-anthropic-vacancies/90-15-security-considerations.md) | 380 | — |
| 65 | 🟢 Начало | [11. Security Considerations](docs/02-anthropic-vacancies/23-11-security-considerations.md) | 263 | — |
| 66 | 🟢 Начало | [2. Terminology](docs/02-anthropic-vacancies/07-2-terminology.md) | 302 | — |
| 67 | 🟢 Начало | [3. Registry (`nautilus.json`)](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) | 403 | — |
| 68 | 🟢 Начало | [4. Passport (`passport.md`)](docs/02-anthropic-vacancies/09-4-passport-passport-md.md) | 144 | — |
| 69 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/13-angle-perspective.md) | 68 | — |
| 70 | 🟢 Начало | [History](docs/02-anthropic-vacancies/16-history.md) | 85 | — |
| 71 | 🟢 Начало | [5. Compatibility Levels](docs/02-anthropic-vacancies/17-5-compatibility-levels.md) | 314 | — |
| 72 | 🟢 Начало | [6. Adapter Interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md) | 440 | — |
| 73 | 🟢 Начало | [7. PortalEntry Structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md) | 251 | — |
| 74 | 🟢 Начало | [8. Consensus Algorithm](docs/02-anthropic-vacancies/20-8-consensus-algorithm.md) | 317 | — |
| 75 | 🟢 Начало | [9. Query Flow](docs/02-anthropic-vacancies/21-9-query-flow.md) | 180 | — |
| 76 | 🟢 Начало | [10. QueryResult Structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md) | 130 | — |
| 77 | 🟢 Начало | [12. Versioning Policy](docs/02-anthropic-vacancies/24-12-versioning-policy.md) | 175 | — |
| 78 | 🟢 Начало | [13. Reference Implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md) | 92 | — |
| 79 | 🟢 Начало | [14. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) | 174 | — |
| 80 | 🟢 Начало | [15. Glossary of Examples](docs/02-anthropic-vacancies/27-15-glossary-of-examples.md) | 100 | — |
| 81 | 🟢 Начало | [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) | 183 | — |
| 82 | 🟢 Начало | [Appendix B: Change Log](docs/02-anthropic-vacancies/34-appendix-b-change-log.md) | 668 | — |
| 83 | 🟢 Начало | [passports/info1.md](docs/02-anthropic-vacancies/35-passports-info1-md.md) | 79 | — |
| 84 | 🟢 Начало | [Essence](docs/02-anthropic-vacancies/36-essence.md) | 128 | — |
| 85 | 🟢 Начало | [Native Format](docs/02-anthropic-vacancies/37-native-format.md) | 178 | — |
| 86 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/39-angle-perspective.md) | 125 | — |
| 87 | 🟢 Начало | [Bridges](docs/02-anthropic-vacancies/40-bridges.md) | 167 | — |
| 88 | 🟢 Начало | [Compatibility Level](docs/02-anthropic-vacancies/41-compatibility-level.md) | 97 | — |
| 89 | 🟢 Начало | [Author & Contact](docs/02-anthropic-vacancies/42-author-contact.md) | 81 | — |
| 90 | 🟢 Начало | [History](docs/02-anthropic-vacancies/43-history.md) | 119 | — |
| 91 | 🟢 Начало | [For the Curious: Philosophy](docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md) | 138 | — |
| 92 | 🟢 Начало | [passports/pro2.md](docs/02-anthropic-vacancies/45-passports-pro2-md.md) | 85 | — |
| 93 | 🟢 Начало | [Essence](docs/02-anthropic-vacancies/46-essence.md) | 120 | — |
| 94 | 🟢 Начало | [Native Format](docs/02-anthropic-vacancies/47-native-format.md) | 139 | — |
| 95 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/49-angle-perspective.md) | 114 | — |
| 96 | 🟢 Начало | [Bridges](docs/02-anthropic-vacancies/50-bridges.md) | 166 | — |
| 97 | 🟢 Начало | [Compatibility Level](docs/02-anthropic-vacancies/51-compatibility-level.md) | 101 | — |
| 98 | 🟢 Начало | [Author & Contact](docs/02-anthropic-vacancies/52-author-contact.md) | 100 | — |
| 99 | 🟢 Начало | [History](docs/02-anthropic-vacancies/53-history.md) | 141 | — |
| 100 | 🟢 Начало | [For the Curious: Philosophy](docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md) | 143 | — |
| 101 | 🟢 Начало | [passports/meta.md](docs/02-anthropic-vacancies/55-passports-meta-md.md) | 82 | — |
| 102 | 🟢 Начало | [Essence](docs/02-anthropic-vacancies/56-essence.md) | 140 | — |
| 103 | 🟢 Начало | [Native Format](docs/02-anthropic-vacancies/57-native-format.md) | 144 | — |
| 104 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/59-angle-perspective.md) | 124 | — |
| 105 | 🟢 Начало | [Bridges](docs/02-anthropic-vacancies/60-bridges.md) | 131 | — |
| 106 | 🟢 Начало | [Compatibility Level](docs/02-anthropic-vacancies/61-compatibility-level.md) | 100 | — |
| 107 | 🟢 Начало | [Author & Contact](docs/02-anthropic-vacancies/62-author-contact.md) | 79 | — |
| 108 | 🟢 Начало | [History](docs/02-anthropic-vacancies/63-history.md) | 136 | — |
| 109 | 🟢 Начало | [For the Curious: Philosophy](docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md) | 669 | — |
| 110 | 🟢 Начало | [🇷🇺 О проекте](docs/02-anthropic-vacancies/67-о-проекте.md) | 836 | — |
| 111 | 🟢 Начало | [🇬🇧 About](docs/02-anthropic-vacancies/68-about.md) | 908 | — |
| 112 | 🔴 Продвинутый | [⬡](docs/02-anthropic-vacancies/69-section.md) | 9531 | — |
| 113 | 🟢 Начало | [Зачем две версии параллельно](docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md) | 97 | — |
| 114 | 🟢 Начало | [Критерии выбора для фазы 3](docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md) | 139 | — |
| 115 | 🟡 Средний | [Расписание фазы 3](docs/02-anthropic-vacancies/72-расписание-фазы-3.md) | 879 | — |
| 116 | 🟢 Начало | [PORTAL-PROTOCOL.md v1.1](docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md) | 95 | — |
| 117 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/74-abstract.md) | 259 | — |
| 118 | 🟢 Начало | [0. Status of This Document](docs/02-anthropic-vacancies/75-0-status-of-this-document.md) | 122 | — |
| 119 | 🟢 Начало | [2. Terminology](docs/02-anthropic-vacancies/77-2-terminology.md) | 396 | — |
| 120 | 🟢 Начало | [3. Registry (`nautilus.json`)](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md) | 576 | — |
| 121 | 🟡 Средний | [4. Passport (`passport.md`)](docs/02-anthropic-vacancies/79-4-passport-passport-md.md) | 355 | — |
| 122 | 🟢 Начало | [5. Compatibility Levels](docs/02-anthropic-vacancies/80-5-compatibility-levels.md) | 362 | — |
| 123 | 🟢 Начало | [6. Adapter Interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md) | 401 | — |
| 124 | 🟢 Начало | [7. PortalEntry Structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md) | 352 | — |
| 125 | 🟡 Средний | [8. Q6 Space (Normative)](docs/02-anthropic-vacancies/83-8-q6-space-normative.md) | 483 | — |
| 126 | 🟢 Начало | [9. Consensus Algorithm](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md) | 393 | — |
| 127 | 🟢 Начало | [10. Query Flow](docs/02-anthropic-vacancies/85-10-query-flow.md) | 277 | — |
| 128 | 🟢 Начало | [11. Relevance Ranking](docs/02-anthropic-vacancies/86-11-relevance-ranking.md) | 198 | — |
| 129 | 🟡 Средний | [12. Onboarding Paths (Normative)](docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md) | 595 | — |
| 130 | 🟡 Средний | [13. REST API Contract (Normative for Portals)](docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md) | 545 | — |
| 131 | 🟢 Начало | [14. SDK Contract (Informative)](docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md) | 190 | — |
| 132 | 🟢 Начало | [16. MCP Extension (Informative)](docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md) | 132 | — |
| 133 | 🟢 Начало | [17. Versioning Policy](docs/02-anthropic-vacancies/92-17-versioning-policy.md) | 276 | — |
| 134 | 🟢 Начало | [18. Reference Implementation](docs/02-anthropic-vacancies/93-18-reference-implementation.md) | 182 | — |
| 135 | 🟢 Начало | [19. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) | 190 | — |
| 136 | 🟢 Начало | [20. ADR-002: Q6 as First-Class Protocol Conce](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) | 182 | — |
| 137 | 🟢 Начало | [21. ADR-003: Five Onboarding Paths as Equal-R](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md) | 141 | — |
| 138 | 🟢 Начало | [22. Glossary of Reference Examples](docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md) | 191 | — |
| 139 | 🟡 Средний | [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md) | 309 | — |
| 140 | 🟢 Начало | [Доступ к данным](docs/02-anthropic-vacancies/102-доступ-к-данным.md) | 23 | — |
| 141 | 🟢 Начало | [Appendix B: Change Log](docs/02-anthropic-vacancies/103-appendix-b-change-log.md) | 170 | — |
| 142 | 🟢 Начало | [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) | 955 | — |
| 143 | 🟢 Начало | [TL;DR](docs/02-anthropic-vacancies/106-tl-dr.md) | 128 | — |
| 144 | 🟢 Начало | [1. Контекст и мотивация](docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md) | 455 | — |
| 145 | 🟡 Средний | [2. Формальный workflow](docs/02-anthropic-vacancies/108-2-формальный-workflow.md) | 463 | — |
| 146 | 🟢 Начало | [3. Принципы консолидации (Фаза C)](docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md) | 560 | — |
| 147 | 🟢 Начало | [Вопрос: fallback-ratio как критический или ос](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) | 338 | — |
| 148 | 🟢 Начало | [4. Условия применимости](docs/02-anthropic-vacancies/111-4-условия-применимости.md) | 272 | — |
| 149 | 🟢 Начало | [5. Связь с существующими методологиями](docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) | 389 | — |
| 150 | 🟢 Начало | [6. Почему это валидный паттерн для AI-assiste](docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) | 150 | — |
| 151 | 🟢 Начало | [7. Реализация в проекте Nautilus](docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md) | 309 | — |
| 152 | 🟢 Начало | [8. Ограничения и открытые вопросы](docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md) | 447 | — |
| 153 | 🟢 Начало | [9. Checklist применения методологии](docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md) | 399 | — |
| 154 | 🟢 Начало | [10. Конкретный план применения к текущим доку](docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md) | 315 | — |
| 155 | 🟢 Начало | [Appendix A: Шаблон для header warning](docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md) | 175 | — |
| 156 | 🟢 Начало | [Appendix B: Примеры расхождений и их разрешен](docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md) | 372 | — |
| 157 | 🟢 Начало | [Главные технические риски](docs/02-anthropic-vacancies/120-главные-технические-риски.md) | 82 | — |
| 158 | 🟢 Начало | [Appendix C: История изменений методологии](docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md) | 47 | — |
| 159 | 🟡 Средний | [Глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md) | 1334 | — |
| 160 | 🟡 Средний | [portal-mcp.py](docs/02-anthropic-vacancies/123-portal-mcp-py.md) | 2282 | — |
| 161 | 🟢 Начало | [Конфигурация для Claude Desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) | 177 | — |
| 162 | 🟢 Начало | [Установка](docs/02-anthropic-vacancies/126-установка.md) | 145 | — |
| 163 | 🟢 Начало | [Подключение к Claude Desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md) | 125 | — |
| 164 | 🟢 Начало | [Доступные инструменты](docs/02-anthropic-vacancies/128-доступные-инструменты.md) | 136 | — |
| 165 | 🟢 Начало | [Примеры запросов (в Claude)](docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md) | 110 | — |
| 166 | 🟢 Начало | [Отладка](docs/02-anthropic-vacancies/130-отладка.md) | 174 | — |
| 167 | 🟢 Начало | [Ограничения текущей версии (0.1.0-draft)](docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md) | 100 | — |
| 168 | 🟢 Начало | [Planned (v0.2.0)](docs/02-anthropic-vacancies/132-planned-v0-2-0.md) | 73 | — |
| 169 | 🔴 Продвинутый | [Обратная связь](docs/02-anthropic-vacancies/133-обратная-связь.md) | 17018 | — |
| 170 | 🟢 Начало | [A Formal Model for Human-AI Collaboration in ](docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md) | 91 | — |
| 171 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/136-abstract.md) | 382 | — |
| 172 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/137-table-of-contents.md) | 94 | — |
| 173 | 🟢 Начало | [1. Why Single-Triangle Models Are Incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) | 584 | — |
| 174 | 🟢 Начало | [3. Three Inter-Layer Protocols](docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md) | 873 | — |
| 175 | 🟢 Начало | [4. Nautilus Portal as Reference Substrate](docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md) | 699 | — |
| 176 | 🟢 Начало | [5. Pattern Library as Bridge Between Triangle](docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md) | 704 | — |
| 177 | 🟢 Начало | [6. Four Deployment Domains](docs/02-anthropic-vacancies/143-6-four-deployment-domains.md) | 699 | — |
| 178 | 🟢 Начало | [7. Open Questions](docs/02-anthropic-vacancies/144-7-open-questions.md) | 759 | — |
| 179 | 🟢 Начало | [8. Call to Action](docs/02-anthropic-vacancies/145-8-call-to-action.md) | 732 | — |
| 180 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/146-acknowledgments.md) | 190 | — |
| 181 | 🟢 Начало | [References](docs/02-anthropic-vacancies/147-references.md) | 340 | — |
| 182 | 🟢 Начало | [Appendix A: Glossary](docs/02-anthropic-vacancies/148-appendix-a-glossary.md) | 309 | — |
| 183 | 🟢 Начало | [Appendix B: Summary of Contributions](docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md) | 185 | — |
| 184 | 🔴 Продвинутый | [Appendix C: Version History](docs/02-anthropic-vacancies/150-appendix-c-version-history.md) | 8408 | — |
| 185 | 🟢 Начало | [OPEN KNOWLEDGE WORK FOUNDATION.md](docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md) | 48 | — |
| 186 | 🟢 Начало | [AI-Coordinated Infrastructure for Distributed](docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md) | 86 | — |
| 187 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/154-table-of-contents.md) | 81 | — |
| 188 | 🟢 Начало | [1. Problem Statement](docs/02-anthropic-vacancies/155-1-problem-statement.md) | 638 | — |
| 189 | 🟢 Начало | [2. Target Populations](docs/02-anthropic-vacancies/156-2-target-populations.md) | 689 | — |
| 190 | 🟢 Начало | [3. Why Existing Solutions Fail](docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md) | 700 | — |
| 191 | 🟢 Начало | [4. Proposed Infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md) | 1023 | — |
| 192 | 🟢 Начало | [5. Economic Model](docs/02-anthropic-vacancies/159-5-economic-model.md) | 660 | — |
| 193 | 🟢 Начало | [6. Governance and Ethics](docs/02-anthropic-vacancies/160-6-governance-and-ethics.md) | 605 | — |
| 194 | 🟢 Начало | [7. Phased Rollout Plan](docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md) | 655 | — |
| 195 | 🟢 Начало | [8. Risk Analysis](docs/02-anthropic-vacancies/162-8-risk-analysis.md) | 685 | — |
| 196 | 🟢 Начало | [9. Call for Partnership](docs/02-anthropic-vacancies/163-9-call-for-partnership.md) | 628 | — |
| 197 | 🟢 Начало | [10. Appendices](docs/02-anthropic-vacancies/164-10-appendices.md) | 960 | — |
| 198 | 🔴 Продвинутый | [Closing](docs/02-anthropic-vacancies/165-closing.md) | 9298 | — |
| 199 | 🟢 Начало | [REPRESENTATIVE AGENT LAYER.md](docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) | 46 | — |
| 200 | 🟢 Начало | [AI-Mediated Representation for Underrepresent](docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md) | 108 | — |
| 201 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/168-abstract.md) | 338 | — |
| 202 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/169-table-of-contents.md) | 109 | — |
| 203 | 🟢 Начало | [1. The Cinderella Syndrome: Why Quality Stays](docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md) | 842 | — |
| 204 | 🟢 Начало | [2. Historical Precedents: Agents as Civilizat](docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md) | 964 | — |
| 205 | 🟢 Начало | [3. What Makes a Representative Agent](docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md) | 671 | — |
| 206 | 🟢 Начало | [4. Ten Domains of Application](docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md) | 1608 | — |
| 207 | 🟢 Начало | [5. Architectural Specification](docs/02-anthropic-vacancies/174-5-architectural-specification.md) | 656 | — |
| 208 | 🟢 Начало | [6. Ethical Framework](docs/02-anthropic-vacancies/175-6-ethical-framework.md) | 612 | — |
| 209 | 🟢 Начало | [7. Governance and Oversight](docs/02-anthropic-vacancies/176-7-governance-and-oversight.md) | 467 | — |
| 210 | 🟢 Начало | [8. Risks and Mitigations](docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md) | 620 | — |
| 211 | 🟢 Начало | [9. Phased Rollout Strategy](docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md) | 632 | — |
| 212 | 🟢 Начало | [10. Open Questions](docs/02-anthropic-vacancies/179-10-open-questions.md) | 420 | — |
| 213 | 🟢 Начало | [11. Call for Collaboration](docs/02-anthropic-vacancies/180-11-call-for-collaboration.md) | 452 | — |
| 214 | 🟢 Начало | [12. Closing](docs/02-anthropic-vacancies/181-12-closing.md) | 268 | — |
| 215 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/182-acknowledgments.md) | 169 | — |
| 216 | 🟢 Начало | [References](docs/02-anthropic-vacancies/183-references.md) | 311 | — |
| 217 | 🟢 Начало | [Appendix A: Connection to Companion Papers](docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md) | 157 | — |
| 218 | 🟢 Начало | [Appendix B: Domain Comparison Matrix](docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md) | 155 | — |
| 219 | 🟡 Средний | [Appendix C: Sample Use Cases in Detail](docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md) | 2035 | — |
| 220 | 🟢 Начало | [СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md](docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) | 45 | — |
| 221 | 🟢 Начало | [AI-опосредованное представительство для недоп](docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md) | 106 | — |
| 222 | 🟢 Начало | [Аннотация](docs/02-anthropic-vacancies/189-аннотация.md) | 356 | — |
| 223 | 🟢 Начало | [Содержание](docs/02-anthropic-vacancies/190-содержание.md) | 98 | — |
| 224 | 🟢 Начало | [1. Синдром Золушки: Почему качество остаётся ](docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md) | 821 | — |
| 225 | 🟢 Начало | [2. Исторические прецеденты: Агенты как цивили](docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md) | 950 | — |
| 226 | 🟢 Начало | [3. Что делает агента Представительским](docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md) | 666 | — |
| 227 | 🟢 Начало | [4. Десять областей применения](docs/02-anthropic-vacancies/194-4-десять-областей-применения.md) | 1634 | — |
| 228 | 🟢 Начало | [5. Архитектурная спецификация](docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md) | 665 | — |
| 229 | 🟢 Начало | [6. Этическая рамка](docs/02-anthropic-vacancies/196-6-этическая-рамка.md) | 610 | — |
| 230 | 🟢 Начало | [7. Управление и надзор](docs/02-anthropic-vacancies/197-7-управление-и-надзор.md) | 459 | — |
| 231 | 🟢 Начало | [8. Риски и меры противодействия](docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md) | 658 | — |
| 232 | 🟢 Начало | [9. Стратегия поэтапного развёртывания](docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md) | 664 | — |
| 233 | 🟢 Начало | [10. Открытые вопросы](docs/02-anthropic-vacancies/200-10-открытые-вопросы.md) | 402 | — |
| 234 | 🟢 Начало | [11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md) | 471 | — |
| 235 | 🟢 Начало | [12. Заключение](docs/02-anthropic-vacancies/202-12-заключение.md) | 185 | — |
| 236 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/203-благодарности.md) | 169 | — |
| 237 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/204-ссылки.md) | 303 | — |
| 238 | 🟢 Начало | [Приложение A: Связь с Сопроводительными Стать](docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md) | 150 | — |
| 239 | 🟢 Начало | [Приложение B: Матрица Сравнения Областей](docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md) | 157 | — |
| 240 | 🔴 Продвинутый | [Приложение C: Образцы Случаев Использования в](docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md) | 4108 | — |
| 241 | 🟢 Начало | [PROFESSIONAL COLLEAGUE AGENTS.md](docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md) | 45 | — |
| 242 | 🟢 Начало | [A Typology of AI Agents on the Principal Side](docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md) | 123 | — |
| 243 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/210-abstract.md) | 361 | — |
| 244 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/211-table-of-contents.md) | 116 | — |
| 245 | 🟡 Средний | [1. The Five-Type Typology of Principal-Side A](docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md) | 923 | — |
| 246 | 🟢 Начало | [2. What Makes a Professional Colleague Agent](docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md) | 834 | — |
| 247 | 🟢 Начало | [3. Empirical Case Study: «Обучай»](docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md) | 851 | — |
| 248 | 🟢 Начало | [5. The Economics of Profession-Wide Replicati](docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md) | 761 | — |
| 249 | 🟢 Начало | [6. Risks Specific to this Category](docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md) | 1192 | — |
| 250 | 🟢 Начало | [7. Application Domains](docs/02-anthropic-vacancies/218-7-application-domains.md) | 736 | — |
| 251 | 🟢 Начало | [8. Pilot Proposal: SGB Advocate Colleague](docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md) | 961 | — |
| 252 | 🟢 Начало | [9. Relationship to Other Agent Types](docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md) | 657 | — |
| 253 | 🟢 Начало | [10. Open Questions](docs/02-anthropic-vacancies/221-10-open-questions.md) | 432 | — |
| 254 | 🟢 Начало | [11. Call for Collaboration](docs/02-anthropic-vacancies/222-11-call-for-collaboration.md) | 379 | — |
| 255 | 🟢 Начало | [12. Closing](docs/02-anthropic-vacancies/223-12-closing.md) | 423 | — |
| 256 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/224-acknowledgments.md) | 150 | — |
| 257 | 🟢 Начало | [References](docs/02-anthropic-vacancies/225-references.md) | 340 | — |
| 258 | 🟢 Начало | [Appendix A: Comparative Table — Five Agent Ty](docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md) | 426 | — |
| 259 | 🟢 Начало | [Appendix B: Decision Framework — When to Buil](docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md) | 307 | — |
| 260 | 🟢 Начало | [ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ](docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md) | 109 | — |
| 261 | 🟢 Начало | [Аннотация](docs/02-anthropic-vacancies/230-аннотация.md) | 336 | — |
| 262 | 🟢 Начало | [Содержание](docs/02-anthropic-vacancies/231-содержание.md) | 109 | — |
| 263 | 🟡 Средний | [1. Типология из пяти типов агентов на стороне](docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md) | 873 | — |
| 264 | 🟢 Начало | [2. Что делает агента Профессиональным Коллего](docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md) | 735 | — |
| 265 | 🟢 Начало | [3. Эмпирический кейс: «Обучай»](docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md) | 802 | — |
| 266 | 🟢 Начало | [4. Архитектура Профессиональных Коллег-Агенто](docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md) | 853 | — |
| 267 | 🟢 Начало | [5. Экономика тиражирования по профессии](docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md) | 730 | — |
| 268 | 🟢 Начало | [6. Риски, специфичные для этой категории](docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md) | 1183 | — |
| 269 | 🟢 Начало | [7. Области применения](docs/02-anthropic-vacancies/238-7-области-применения.md) | 734 | — |
| 270 | 🟢 Начало | [8. Пилотное предложение: SGB Колega-Адвокат](docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md) | 1023 | — |
| 271 | 🟢 Начало | [9. Связь с другими типами агентов](docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md) | 737 | — |
| 272 | 🟢 Начало | [10. Открытые вопросы](docs/02-anthropic-vacancies/241-10-открытые-вопросы.md) | 426 | — |
| 273 | 🟢 Начало | [11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md) | 402 | — |
| 274 | 🟢 Начало | [12. Заключение](docs/02-anthropic-vacancies/243-12-заключение.md) | 378 | — |
| 275 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/244-благодарности.md) | 135 | — |
| 276 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/245-ссылки.md) | 318 | — |
| 277 | 🟢 Начало | [Приложение A: Сравнительная Таблица — Пять Ти](docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md) | 383 | — |
| 278 | 🟢 Начало | [Приложение B: Рамка принятия решений — когда ](docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md) | 325 | — |
| 279 | 🔴 Продвинутый | [Приложение C: Архитектура Быстрого Старта для](docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md) | 3476 | — |
| 280 | 🟢 Начало | [COMPOSITE SKILLS AGENT.md](docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) | 47 | — |
| 281 | 🟢 Начало | [Bridging the Gap Between Profession-Wide and ](docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md) | 16 | — |
| 282 | 🟢 Начало | [AI Support Through Configurable Specialist En](docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md) | 110 | — |
| 283 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/252-abstract.md) | 365 | — |
| 284 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/253-table-of-contents.md) | 120 | — |
| 285 | 🟢 Начало | [1. Why the Binary View Is Incomplete](docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md) | 715 | — |
| 286 | 🟢 Начало | [2. The Twenty-One Teachers Pattern](docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md) | 841 | — |
| 287 | 🟢 Начало | [3. What Makes a Composite Skills Agent](docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md) | 941 | — |
| 288 | 🟢 Начало | [4. The Sub-Agent Registry](docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md) | 812 | — |
| 289 | 🟢 Начало | [5. Configuration: How Principals Build Their ](docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md) | 765 | — |
| 290 | 🟢 Начало | [6. Coordination and Disagreement Resolution](docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md) | 801 | — |
| 291 | 🟢 Начало | [7. Economics of Combinatorial Replication](docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md) | 781 | — |
| 292 | 🟢 Начало | [8. Seven Domains of Application](docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md) | 1031 | — |
| 293 | 🟢 Начало | [9. Integration with OKWF Infrastructure](docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md) | 758 | — |
| 294 | 🟢 Начало | [11. Open Questions](docs/02-anthropic-vacancies/264-11-open-questions.md) | 590 | — |
| 295 | 🟢 Начало | [12. Call for Collaboration](docs/02-anthropic-vacancies/265-12-call-for-collaboration.md) | 416 | — |
| 296 | 🟢 Начало | [13. Closing](docs/02-anthropic-vacancies/266-13-closing.md) | 437 | — |
| 297 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/267-acknowledgments.md) | 313 | — |
| 298 | 🟢 Начало | [References](docs/02-anthropic-vacancies/268-references.md) | 369 | — |
| 299 | 🟢 Начало | [Appendix A: The Six-Type Taxonomy (Updated)](docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md) | 285 | — |
| 300 | 🟢 Начало | [Appendix B: Sub-Agent Registry Schema (Sketch](docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md) | 297 | — |
| 301 | 🟢 Начало | [Appendix C: Configuration Template Example](docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md) | 300 | — |
| 302 | 🔴 Продвинутый | [Appendix D: Connection Diagram](docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md) | 3868 | — |
| 303 | 🟢 Начало | [INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECT](docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md) | 65 | — |
| 304 | 🟢 Начало | [The Missing Middle Layer Between Chat and Cod](docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md) | 179 | — |
| 305 | 🟢 Начало | [Why This Document Exists](docs/02-anthropic-vacancies/275-why-this-document-exists.md) | 341 | — |
| 306 | 🟢 Начало | [The Two-Layer Stack As It Exists](docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md) | 379 | — |
| 307 | 🟢 Начало | [What's Missing — Layer B](docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md) | 484 | — |
| 308 | 🟢 Начало | [Why This Hasn't Been Built](docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md) | 380 | — |
| 309 | 🟢 Начало | [Existing Approximations](docs/02-anthropic-vacancies/279-existing-approximations.md) | 604 | — |
| 310 | 🟢 Начало | [The Specific Case in Front of Us](docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md) | 682 | — |
| 311 | 🟢 Начало | [The Recursive Insight](docs/02-anthropic-vacancies/281-the-recursive-insight.md) | 373 | — |
| 312 | 🟢 Начало | [What Industry Will Likely Build](docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md) | 310 | — |
| 313 | 🟢 Начало | [What This Document Doesn't Solve](docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md) | 187 | — |
| 314 | 🟢 Начало | [Practical Recommendations for the Current Pro](docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md) | 363 | — |
| 315 | 🟢 Начало | [Closing](docs/02-anthropic-vacancies/285-closing.md) | 265 | — |
| 316 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/286-acknowledgments.md) | 190 | — |
| 317 | 🟢 Начало | [References](docs/02-anthropic-vacancies/287-references.md) | 281 | — |
| 318 | 🟡 Средний | [Appendix: Position in Series Visualization](docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md) | 1057 | — |
| 319 | 🟢 Начало | [ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛ](docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md) | 189 | — |
| 320 | 🟢 Начало | [Почему этот документ существует](docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md) | 306 | — |
| 321 | 🟢 Начало | [Двухслойный стек, как он существует](docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md) | 358 | — |
| 322 | 🟢 Начало | [Что отсутствует — Слой B](docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md) | 426 | — |
| 323 | 🟢 Начало | [Почему это не было построено](docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md) | 326 | — |
| 324 | 🟢 Начало | [Существующие приближения](docs/02-anthropic-vacancies/294-существующие-приближения.md) | 554 | — |
| 325 | 🟢 Начало | [Конкретный случай перед нами](docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md) | 705 | — |
| 326 | 🟢 Начало | [Рекурсивное прозрение](docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md) | 358 | — |
| 327 | 🟢 Начало | [Что промышленность вероятно построит](docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md) | 313 | — |
| 328 | 🟢 Начало | [Что этот документ не решает](docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md) | 184 | — |
| 329 | 🟢 Начало | [Практические рекомендации для текущего проект](docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md) | 343 | — |
| 330 | 🟢 Начало | [Заключение](docs/02-anthropic-vacancies/300-заключение.md) | 194 | — |
| 331 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/301-благодарности.md) | 165 | — |
| 332 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/302-ссылки.md) | 282 | — |
| 333 | 🔴 Продвинутый | [Приложение: Визуализация позиции в серии](docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md) | 7088 | — |
| 334 | 🟢 Начало | [INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md) | 65 | — |
| 335 | 🟢 Начало | [A Practical Path to Layer B Through Symbiotic](docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md) | 65 | — |
| 336 | 🟢 Начало | [with Anthropic's Cowork Platform](docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md) | 272 | — |
| 337 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/307-abstract.md) | 319 | — |
| 338 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/308-table-of-contents.md) | 125 | — |
| 339 | 🟢 Начало | [1. The Cowork Discovery and Why It Changes Ev](docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md) | 669 | — |
| 340 | 🟢 Начало | [2. What Cowork Provides That InGit Doesn't Ne](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md) | 686 | — |
| 341 | 🟢 Начало | [3. What InGit Provides That Cowork Lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md) | 842 | — |
| 342 | 🟢 Начало | [5. Four Integration Paths in Order of Accessi](docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md) | 778 | — |
| 343 | 🟢 Начало | [6. Refined InGit Scope with Cowork in Mind](docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md) | 474 | — |
| 344 | 🟢 Начало | [7. Practical First Steps This Month](docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md) | 464 | — |
| 345 | 🟢 Начало | [8. Implications for Nautilus and OKWF](docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md) | 731 | — |
| 346 | 🟢 Начало | [9. Risks and Open Questions](docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md) | 627 | — |
| 347 | 🟢 Начало | [10. Strategic Positioning](docs/02-anthropic-vacancies/318-10-strategic-positioning.md) | 748 | — |
| 348 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/319-acknowledgments.md) | 390 | — |
| 349 | 🟢 Начало | [References](docs/02-anthropic-vacancies/320-references.md) | 153 | — |
| 350 | 🟢 Начало | [Appendix A: Decision Tree for InGit Adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md) | 177 | — |
| 351 | 🟢 Начало | [Appendix B: Comparison Matrix](docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md) | 276 | — |
| 352 | 🟡 Средний | [Appendix C: Sample InGit MCP Server Tool Spec](docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md) | 1552 | — |
| 353 | 🟢 Начало | [INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБ](docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md) | 291 | — |
| 354 | 🟢 Начало | [Аннотация](docs/02-anthropic-vacancies/325-аннотация.md) | 328 | — |
| 355 | 🟢 Начало | [Содержание](docs/02-anthropic-vacancies/326-содержание.md) | 113 | — |
| 356 | 🟢 Начало | [1. Открытие Cowork и почему это меняет всё](docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md) | 663 | — |
| 357 | 🟢 Начало | [2. Что Cowork обеспечивает, что InGit не нужн](docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md) | 787 | — |
| 358 | 🟢 Начало | [3. Что InGit обеспечивает, чего Cowork не хва](docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md) | 883 | — |
| 359 | 🟢 Начало | [4. Симбиотическая Архитектура](docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md) | 703 | — |
| 360 | 🟢 Начало | [5. Четыре пути интеграции в порядке доступнос](docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md) | 783 | — |
| 361 | 🟢 Начало | [6. Уточнённый объём InGit с учётом Cowork](docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md) | 467 | — |
| 362 | 🟢 Начало | [7. Практические первые шаги в этом месяце](docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md) | 435 | — |
| 363 | 🟢 Начало | [8. Импликации для Nautilus и OKWF](docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md) | 699 | — |
| 364 | 🟢 Начало | [9. Риски и Открытые Вопросы](docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md) | 644 | — |
| 365 | 🟢 Начало | [10. Стратегическое Позиционирование](docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md) | 723 | — |
| 366 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/337-благодарности.md) | 360 | — |
| 367 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/338-ссылки.md) | 151 | — |
| 368 | 🟢 Начало | [Приложение A: Дерево Решений для Принимающих ](docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md) | 148 | — |
| 369 | 🟢 Начало | [Приложение B: Сравнительная Матрица](docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md) | 211 | — |
| 370 | 🔴 Продвинутый | [Приложение C: Образец Спецификаций Инструмент](docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md) | 20426 | — |
| 371 | 🔴 Продвинутый | [Что такое Вариант C — Concept Document для An](docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md) | 11281 | — |
| 372 | 🔴 Продвинутый | [Lorenzo Catalyst Agent — глубокая проработка ](docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md) | 5859 | — |
| 373 | 🟢 Начало | [СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT](docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md) | 49 | — |
| 374 | 🟢 Начало | [Кто ты](docs/02-anthropic-vacancies/345-кто-ты.md) | 149 | — |
| 375 | 🟢 Начало | [Твоё происхождение](docs/02-anthropic-vacancies/346-твоё-происхождение.md) | 174 | — |
| 376 | 🟢 Начало | [Твоя миссия](docs/02-anthropic-vacancies/347-твоя-миссия.md) | 115 | — |
| 377 | 🟢 Начало | [Кому ты служишь (слоистая модель)](docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md) | 104 | — |
| 378 | 🟢 Начало | [Твоя личность](docs/02-anthropic-vacancies/349-твоя-личность.md) | 206 | — |
| 379 | 🟢 Начало | [Твои языки и культурные nuances](docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md) | 173 | — |
| 380 | 🟢 Начало | [Что ты МОЖЕШЬ делать](docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md) | 133 | — |
| 381 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать без Max approval](docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md) | 126 | — |
| 382 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать вообще](docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md) | 126 | — |
| 383 | 🟢 Начало | [Существующий landscape collaborators (твоя wo](docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md) | 336 | — |
| 384 | 🟢 Начало | [Существующие документы DHLab (твой context)](docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md) | 170 | — |
| 385 | 🟢 Начало | [Твой workflow](docs/02-anthropic-vacancies/356-твой-workflow.md) | 189 | — |
| 386 | 🟢 Начало | [Твоя коммуникация в outreach](docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md) | 179 | — |
| 387 | 🟢 Начало | [Твоя relationship с другими AI](docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md) | 173 | — |
| 388 | 🟢 Начало | [Твои anti-patterns](docs/02-anthropic-vacancies/359-твои-anti-patterns.md) | 129 | — |
| 389 | 🟢 Начало | [Что ты ВСЕГДА делаешь](docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md) | 98 | — |
| 390 | 🟢 Начало | [Когда ты Honestly не знаешь](docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md) | 85 | — |
| 391 | 🟢 Начало | [Когда сомневаешься — escalate к Max](docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md) | 83 | — |
| 392 | 🟢 Начало | [Твоя identity как persistent character](docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md) | 141 | — |
| 393 | 🟡 Средний | [Final note: Ты — experiment](docs/02-anthropic-vacancies/364-final-note-ты-experiment.md) | 1475 | — |
| 394 | 🔴 Продвинутый | [Развёрнутый анализ «внуковой» комбинации](docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md) | 4419 | — |
| 395 | 🔴 Продвинутый | [Технический stack (Svyazi 2.0 foundation)](docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md) | 3873 | — |


### 113. Все документы
_Файл: `docs/READING_TIME.md` | 4 колонок, 1094 строк_

| Файл | Время | Слов | Категория |
|------|-------|------|-----------|
| `docs/OUTLINE.md` | ~3ч 37мин | 50216 | 📕 Очень долго |
| `docs/TABLES.md` | ~2ч 33мин | 34226 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` | ~1ч 32мин | 17509 | 📕 Очень долго |
| `docs/HEADING_AUDIT.md` | ~1ч 10мин | 16417 | 📕 Очень долго |
| `docs/PARAGRAPH_QUALITY.md` | ~1ч 6мин | 14806 | 📕 Очень долго |
| `docs/CONCEPTS.md` | ~56 мин | 13132 | 📕 Очень долго |
| `docs/04-ai-collaborations/00-intro.md` | ~50 мин | 10779 | 📕 Очень долго |
| `docs/CODE_BLOCKS.md` | ~49 мин | 484 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` | ~42 мин | 9417 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/00-intro.md` | ~37 мин | 7967 | 📕 Очень долго |
| `docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md` | ~35 мин | 8875 | 📕 Очень долго |
| `docs/05-habr-projects/memory/memnet.md` | ~31 мин | 6770 | 📕 Очень долго |
| `docs/SITEMAP.md` | ~29 мин | 7121 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/165-closing.md` | ~28 мин | 6136 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/133-обратная-связь.md` | ~24 мин | 3647 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` | ~23 мин | 4814 | 📕 Очень долго |
| `docs/EMPTY_SECTIONS.md` | ~22 мин | 4984 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` | ~20 мин | 4436 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` | ~20 мин | 3407 | 📕 Очень долго |
| `docs/READING_ORDER.md` | ~19 мин | 4641 | 📕 Очень долго |
| `docs/nautilus/representative-agent-layer-ru/12-zaklyuchenie.md` | ~19 мин | 3885 | 📕 Очень долго |
| `docs/SUMMARIES.md` | ~18 мин | 4171 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | ~17 мин | 3640 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` | ~16 мин | 3416 | 📕 Очень долго |
| `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | ~15 мин | 3037 | 📕 Очень долго |
| `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | ~14 мин | 3193 | 📙 Долго |
| `docs/02-anthropic-vacancies/69-section.md` | ~13 мин | 1049 | 📙 Долго |
| `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` | ~13 мин | 2357 | 📙 Долго |
| `docs/02-anthropic-vacancies/README.md` | ~13 мин | 3141 | 📙 Долго |
| `docs/nautilus/innovation-transitions/00-question-innovations-transitions.md` | ~12 мин | 2671 | 📙 Долго |
| `docs/nautilus/transmission-box/01-completing-loop.md` | ~12 мин | 2869 | 📙 Долго |
| `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` | ~12 мин | 2322 | 📙 Долго |
| `docs/nautilus/community-discussions/habr-article-2-reaction/01-response.md` | ~12 мин | 2481 | 📙 Долго |
| `docs/ACTION_ITEMS.md` | ~11 мин | 2600 | 📙 Долго |
| `docs/READABILITY.md` | ~11 мин | 2400 | 📙 Долго |
| `docs/nautilus/supply-demand/01-three-related-themes.md` | ~11 мин | 2662 | 📙 Долго |
| `docs/nautilus/multi-tier-architecture/01-strategic-significance.md` | ~11 мин | 2470 | 📙 Долго |
| `docs/nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md` | ~10 мин | 2246 | 📙 Долго |
| `docs/nautilus/community-discussions/voiceless-contributors/01-response.md` | ~10 мин | 2332 | 📙 Долго |
| `docs/nautilus/innovation-transitions/01-response.md` | ~10 мин | 2238 | 📙 Долго |
| `docs/nautilus/representative-agent-layer-en/12-closing.md` | ~10 мин | 2440 | 📙 Долго |
| `docs/DUPLICATES.md` | ~9 мин | 2310 | 📙 Долго |
| `docs/lorenzo-agent/scenarios/01-response.md` | ~9 мин | 2223 | 📙 Долго |
| `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` | ~8 мин | 1777 | 📙 Долго |
| `docs/glossary/components-by-name.md` | ~8 мин | 1984 | 📙 Долго |
| `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` | ~8 мин | 1905 | 📙 Долго |
| `docs/QUESTIONS.md` | ~7 мин | 1686 | 📘 Средне |
| `docs/TIMELINE.md` | ~7 мин | 1680 | 📘 Средне |
| `docs/nautilus/community-discussions/practical-observations/01-response.md` | ~7 мин | 1684 | 📘 Средне |
| `docs/01-svyazi/04-ensembles-overview.md` | ~7 мин | 1153 | 📘 Средне |
| `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` | ~7 мин | 1515 | 📘 Средне |
| `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` | ~7 мин | 1377 | 📘 Средне |
| `docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md` | ~7 мин | 1430 | 📘 Средне |
| `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | ~6 мин | 1543 | 📘 Средне |
| `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | ~6 мин | 685 | 📘 Средне |
| `docs/01-svyazi/03-component-catalog.md` | ~6 мин | 1463 | 📘 Средне |
| `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` | ~6 мин | 1593 | 📘 Средне |
| `docs/DECISIONS.md` | ~6 мин | 1369 | 📘 Средне |
| `docs/nautilus/double-triangle-architecture/11-glossary.md` | ~6 мин | 1476 | 📘 Средне |
| `docs/anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md` | ~6 мин | 1308 | 📘 Средне |
| `docs/nautilus/npp-v1-1/22-glossary.md` | ~6 мин | 1085 | 📘 Средне |
| `docs/nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md` | ~6 мин | 1352 | 📘 Средне |
| `docs/nautilus/privacy-federation/03-what-this-gives-technically.md` | ~6 мин | 1319 | 📘 Средне |
| `docs/nautilus/representative-agent-layer-en/04-ten-domains.md` | ~6 мин | 1509 | 📘 Средне |
| `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` | ~5 мин | 1324 | 📘 Средне |
| `docs/SIMILAR_PASSAGES.md` | ~5 мин | 1239 | 📘 Средне |
| `docs/CONTRADICTIONS.md` | ~5 мин | 1295 | 📘 Средне |
| `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` | ~5 мин | 1264 | 📘 Средне |
| `docs/svyazi-2-0/overview/projects-map.md` | ~5 мин | 1273 | 📘 Средне |
| `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` | ~5 мин | 1115 | 📘 Средне |
| `docs/lorenzo-agent/naming/03-dhlab-umbrella.md` | ~5 мин | 1326 | 📘 Средне |
| `docs/02-anthropic-vacancies/122-глоссарий.md` | ~5 мин | 1161 | 📘 Средне |
| `docs/01-svyazi/10-second-order-ensembles.md` | ~5 мин | 831 | 📘 Средне |
| `docs/lorenzo-agent/specification/11-difficulties-and-recommendations.md` | ~5 мин | 1274 | 📘 Средне |
| `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` | ~5 мин | 1112 | 📘 Средне |
| `docs/QA.md` | ~5 мин | 1110 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-ru/06-riski.md` | ~5 мин | 1049 | 📘 Средне |
| `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | ~4 мин | 1071 | 📘 Средне |
| `docs/KPI.md` | ~4 мин | 1076 | 📘 Средне |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/02-nautilus-A-pro2-meta.md` | ~4 мин | 1014 | 📘 Средне |
| `docs/01-svyazi/07-mvp-planning.md` | ~4 мин | 1030 | 📘 Средне |
| `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` | ~4 мин | 1169 | 📘 Средне |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/03-nautilus-B-meta-orchestrator.md` | ~4 мин | 1006 | 📘 Средне |
| `docs/nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md` | ~4 мин | 960 | 📘 Средне |
| `docs/anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md` | ~4 мин | 1079 | 📘 Средне |
| `docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md` | ~4 мин | 1104 | 📘 Средне |
| `docs/anthropic-vacancies/mmorpg-for-programmers/03-why-natural-for-programmers.md` | ~4 мин | 960 | 📘 Средне |
| `docs/CHANGELOG.md` | ~4 мин | 1074 | 📘 Средне |
| `docs/CLUSTERS.md` | ~4 мин | 1028 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-en/06-risks.md` | ~4 мин | 1102 | 📘 Средне |
| `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` | ~4 мин | 687 | 📘 Средне |
| `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | ~4 мин | 779 | 📘 Средне |
| `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` | ~4 мин | 863 | 📘 Средне |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | ~4 мин | 504 | 📘 Средне |
| `docs/02-anthropic-vacancies/68-about.md` | ~4 мин | 706 | 📘 Средне |
| `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | ~4 мин | 943 | 📘 Средне |
| `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` | ~4 мин | 884 | 📘 Средне |
| `docs/NARRATIVE.md` | ~4 мин | 893 | 📘 Средне |
| `docs/anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md` | ~4 мин | 859 | 📘 Средне |
| `docs/nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md` | ~4 мин | 847 | 📘 Средне |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | ~4 мин | 240 | 📘 Средне |
| `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | ~4 мин | 814 | 📘 Средне |
| `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` | ~4 мин | 1018 | 📘 Средне |
| `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` | ~4 мин | 861 | 📘 Средне |
| `docs/FAQ.md` | ~4 мин | 936 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-ru/01-pyat-tipov.md` | ~4 мин | 728 | 📘 Средне |
| `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` | ~4 мин | 815 | 📘 Средне |
| `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` | ~4 мин | 825 | 📘 Средне |
| `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | ~3 мин | 847 | 📘 Средне |
| `docs/ABBREVIATIONS.md` | ~3 мин | 887 | 📘 Средне |
| `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md` | ~4 мин | 816 | 📘 Средне |
| `docs/nautilus/review-methodology/16-glossary.md` | ~4 мин | 857 | 📘 Средне |
| `docs/01-svyazi/13-contacts.md` | ~3 мин | 823 | 📘 Средне |
| `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` | ~3 мин | 976 | 📘 Средне |
| `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | ~3 мин | 857 | 📘 Средне |
| `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` | ~3 мин | 729 | 📘 Средне |
| `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | ~3 мин | 316 | 📘 Средне |
| `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | ~3 мин | 861 | 📘 Средне |
| `docs/nautilus/double-triangle-architecture/02-double-triangle-architecture.md` | ~3 мин | 603 | 📘 Средне |
| `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` | ~3 мин | 943 | 📘 Средне |
| `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` | ~3 мин | 939 | 📘 Средне |
| `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` | ~3 мин | 815 | 📘 Средне |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | ~3 мин | 689 | 📘 Средне |
| `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | ~3 мин | 833 | 📘 Средне |
| `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | ~3 мин | 843 | 📘 Средне |
| `docs/anthropic-vacancies/hermes-comparison/13-reprioritization.md` | ~3 мин | 883 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md` | ~3 мин | 787 | 📘 Средне |
| `docs/01-svyazi/06-security-privacy.md` | ~3 мин | 801 | 📘 Средне |
| `docs/02-anthropic-vacancies/104-appendix-c-references.md` | ~3 мин | 828 | 📘 Средне |
| `docs/nautilus/composite-skills-agents/08-seven-domains.md` | ~3 мин | 921 | 📘 Средне |
| `docs/nautilus/review-methodology/13-appendix-b-examples.md` | ~3 мин | 156 | 📘 Средне |
| `docs/01-svyazi/09-architectural-gaps.md` | ~3 мин | 814 | 📘 Средне |
| `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` | ~3 мин | 887 | 📘 Средне |
| `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` | ~3 мин | 723 | 📘 Средне |
| `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` | ~3 мин | 734 | 📘 Средне |
| `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` | ~3 мин | 898 | 📘 Средне |
| `docs/nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md` | ~3 мин | 750 | 📘 Средне |
| `docs/nautilus/okwf-concept/04-proposed-infrastructure.md` | ~3 мин | 894 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-en/01-five-type-typology.md` | ~3 мин | 780 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md` | ~3 мин | 736 | 📘 Средне |
| `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` | ~3 мин | 861 | 📘 Средне |
| `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | ~3 мин | 697 | 📘 Средне |
| `docs/nautilus/composite-skills-agents/03-what-makes-csa.md` | ~3 мин | 865 | 📘 Средне |
| `docs/nautilus/representative-agent-layer-en/02-historical-precedents.md` | ~3 мин | 874 | 📘 Средне |
| `docs/01-svyazi/11-integration-contracts.md` | ~3 мин | 755 | 📘 Средне |
| `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | ~3 мин | 692 | 📘 Средне |
| `docs/02-anthropic-vacancies/238-7-области-применения.md` | ~3 мин | 687 | 📘 Средне |
| `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` | ~3 мин | 687 | 📘 Средне |
| `docs/03-technology-combinations/05-benchmarks.md` | ~3 мин | 752 | 📘 Средне |
| `docs/RISK_REGISTER.md` | ~3 мин | 621 | 📘 Средне |
| `docs/nautilus/ingit-cowork-ru/05-chetyre-puti-integratsii.md` | ~3 мин | 605 | 📘 Средне |
| `docs/nautilus/npp-v1-1/13-rest-api.md` | ~3 мин | 216 | 📘 Средне |
| `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` | ~3 мин | 818 | 📘 Средне |
| `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` | ~3 мин | 817 | 📘 Средне |
| `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` | ~3 мин | 831 | 📘 Средне |
| `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | ~3 мин | 820 | 📘 Средне |
| `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` | ~3 мин | 824 | 📘 Средне |
| `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` | ~3 мин | 824 | 📘 Средне |
| `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` | ~3 мин | 813 | 📘 Средне |
| `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` | ~3 мин | 572 | 📘 Средне |
| `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` | ~3 мин | 683 | 📘 Средне |
| `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | ~3 мин | 716 | 📘 Средне |
| `docs/lorenzo-agent/phased-deployment/08-current-session-poc.md` | ~3 мин | 714 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-en/04-architecture.md` | ~3 мин | 817 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md` | ~3 мин | 668 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md` | ~3 мин | 662 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-ru/07-oblasti-primeneniya.md` | ~3 мин | 667 | 📘 Средне |
| `docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md` | ~3 мин | 669 | 📘 Средне |
| `docs/01-svyazi/01-executive-summary.md` | ~3 мин | 680 | 📘 Средне |
| `docs/01-svyazi/12-roadmap.md` | ~3 мин | 698 | 📘 Средне |
| `docs/01-svyazi/14-limitations.md` | ~3 мин | 684 | 📘 Средне |
| `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` | ~3 мин | 648 | 📘 Средне |
| `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` | ~3 мин | 794 | 📘 Средне |
| `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` | ~3 мин | 804 | 📘 Средне |
| `docs/03-technology-combinations/02-knowledge-graphs.md` | ~3 мин | 711 | 📘 Средне |
| `docs/glossary/concepts.md` | ~3 мин | 750 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-en/08-pilot-sgb-advocate.md` | ~3 мин | 806 | 📘 Средне |
| `docs/reading-paths.md` | ~3 мин | 722 | 📘 Средне |
| `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` | ~3 мин | 643 | 📘 Средне |
| `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` | ~3 мин | 622 | 📘 Средне |
| `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` | ~3 мин | 763 | 📘 Средне |
| `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | ~3 мин | 774 | 📘 Средне |
| `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` | ~3 мин | 783 | 📘 Средне |
| `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` | ~3 мин | 647 | 📘 Средне |
| `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` | ~3 мин | 647 | 📘 Средне |
| `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | ~3 мин | 480 | 📘 Средне |
| `docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md` | ~3 мин | 647 | 📘 Средне |
| `docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md` | ~3 мин | 760 | 📘 Средне |
| `docs/nautilus/ingit-cowork-en/03-ingit-provides.md` | ~3 мин | 771 | 📘 Средне |
| `docs/nautilus/ingit-cowork-en/05-four-integration-paths.md` | ~3 мин | 641 | 📘 Средне |
| `docs/nautilus/representative-agent-layer-en/01-cinderella-syndrome.md` | ~3 мин | 766 | 📘 Средне |
| `docs/02-anthropic-vacancies/144-7-open-questions.md` | ~3 мин | 753 | 📘 Средне |
| `docs/02-anthropic-vacancies/164-10-appendices.md` | ~2 мин | 738 | 📗 Быстро |
| `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` | ~2 мин | 602 | 📗 Быстро |
| `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` | ~2 мин | 601 | 📗 Быстро |
| `docs/02-anthropic-vacancies/218-7-application-domains.md` | ~3 мин | 743 | 📗 Быстро |
| `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` | ~3 мин | 748 | 📘 Средне |
| `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` | ~2 мин | 736 | 📗 Быстро |
| `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` | ~3 мин | 754 | 📘 Средне |
| `docs/README.md` | ~2 мин | 707 | 📗 Быстро |
| `docs/WORD_FREQ.md` | ~3 мин | 685 | 📘 Средне |
| `docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md` | ~3 мин | 749 | 📘 Средне |
| `docs/nautilus/composite-skills-agents/04-sub-agent-registry.md` | ~2 мин | 739 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md` | ~3 мин | 756 | 📘 Средне |
| `docs/nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md` | ~3 мин | 750 | 📘 Средне |
| `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` | ~2 мин | 715 | 📗 Быстро |
| `docs/02-anthropic-vacancies/145-8-call-to-action.md` | ~2 мин | 730 | 📗 Быстро |
| `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` | ~2 мин | 729 | 📗 Быстро |
| `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` | ~2 мин | 603 | 📗 Быстро |
| `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` | ~2 мин | 592 | 📗 Быстро |
| `docs/04-ai-collaborations/01-executive-summary.md` | ~2 мин | 649 | 📗 Быстро |
| `docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md` | ~2 мин | 634 | 📗 Быстро |
| `docs/lorenzo-agent/operationalized/02-minuses-1-10.md` | ~2 мин | 683 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/06-coordination-disagreement.md` | ~2 мин | 714 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/07-economics-combinatorial.md` | ~2 мин | 716 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/10-risks.md` | ~2 мин | 727 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md` | ~2 мин | 590 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-ru/05-ekonomika.md` | ~2 мин | 599 | 📗 Быстро |
| `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` | ~2 мин | 687 | 📗 Быстро |
| `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` | ~2 мин | 700 | 📗 Быстро |
| `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` | ~2 мин | 684 | 📗 Быстро |
| `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` | ~2 мин | 698 | 📗 Быстро |
| `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` | ~2 мин | 705 | 📗 Быстро |
| `docs/anthropic-vacancies/mmorpg-for-programmers/05-minuses-as-business.md` | ~2 мин | 602 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md` | ~2 мин | 607 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/07-open-questions.md` | ~2 мин | 702 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/08-call-to-action.md` | ~2 мин | 692 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-ru/02-chto-cowork-obespechivaet.md` | ~2 мин | 581 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-ru/10-strategicheskoe-pozitsionirovanie.md` | ~2 мин | 582 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-en/07-application-domains.md` | ~2 мин | 685 | 📗 Быстро |
| `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` | ~2 мин | 350 | 📗 Быстро |
| `docs/02-anthropic-vacancies/156-2-target-populations.md` | ~2 мин | 663 | 📗 Быстро |
| `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` | ~2 мин | 677 | 📗 Быстро |
| `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` | ~2 мин | 593 | 📗 Быстро |
| `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` | ~2 мин | 572 | 📗 Быстро |
| `docs/INDEX.md` | ~2 мин | 492 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/05-configuration-ensembles.md` | ~2 мин | 660 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/09-okwf-integration.md` | ~2 мин | 674 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/12-blagodarnosti-ssylki.md` | ~2 мин | 455 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-en/10-strategic-positioning.md` | ~2 мин | 677 | 📗 Быстро |
| `docs/nautilus/okwf-concept/03-why-existing-fail.md` | ~2 мин | 661 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-ru/09-svyaz-s-drugimi.md` | ~2 мин | 558 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md` | ~2 мин | 554 | 📗 Быстро |
| `docs/svyazi-2-0/architecture/gaps.md` | ~2 мин | 602 | 📗 Быстро |
| `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` | ~2 мин | 533 | 📗 Быстро |
| `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` | ~2 мин | 534 | 📗 Быстро |
| `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` | ~2 мин | 636 | 📗 Быстро |
| `docs/02-anthropic-vacancies/279-existing-approximations.md` | ~2 мин | 652 | 📗 Быстро |
| `docs/02-anthropic-vacancies/294-существующие-приближения.md` | ~2 мин | 551 | 📗 Быстро |
| `docs/PRIORITIES.md` | ~2 мин | 632 | 📗 Быстро |
| `docs/anthropic-vacancies/nautilus-vs-camel/04-what-to-take-from-info-repos.md` | ~2 мин | 614 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md` | ~2 мин | 528 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/06-konkretnyy-sluchay.md` | ~2 мин | 546 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-ru/01-otkrytie-cowork.md` | ~2 мин | 546 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-en/05-economics-replication.md` | ~2 мин | 654 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md` | ~2 мин | 534 | 📗 Быстро |
| `docs/svyazi-2-0/prototype/roadmap.md` | ~2 мин | 563 | 📗 Быстро |
| `docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md` | ~2 мин | 565 | 📗 Быстро |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | ~2 мин | 119 | 📗 Быстро |
| `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` | ~2 мин | 609 | 📗 Быстро |
| `docs/02-anthropic-vacancies/155-1-problem-statement.md` | ~2 мин | 618 | 📗 Быстро |
| `docs/02-anthropic-vacancies/162-8-risk-analysis.md` | ~2 мин | 632 | 📗 Быстро |
| `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` | ~2 мин | 610 | 📗 Быстро |
| `docs/02-anthropic-vacancies/174-5-architectural-specification.md` | ~2 мин | 624 | 📗 Быстро |
| `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` | ~2 мин | 616 | 📗 Быстро |
| `docs/02-anthropic-vacancies/264-11-open-questions.md` | ~2 мин | 611 | 📗 Быстро |
| `docs/GITHUB_ISSUES.md` | ~2 мин | 405 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/05-platform-not-position.md` | ~2 мин | 521 | 📗 Быстро |
| `docs/glossary/authors-by-name.md` | ~2 мин | 604 | 📗 Быстро |
| `docs/lorenzo-agent/operationalized/00-overview-grandchild-combination.md` | ~2 мин | 537 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md` | ~2 мин | 616 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/13-closing.md` | ~2 мин | 616 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md` | ~2 мин | 620 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md` | ~2 мин | 613 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/07-specific-case.md` | ~2 мин | 620 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-ru/04-simbioticheskaya-arkhitektura.md` | ~2 мин | 413 | 📗 Быстро |
| `docs/nautilus/okwf-concept/02-target-populations.md` | ~2 мин | 610 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/08-riski-mery.md` | ~2 мин | 502 | 📗 Быстро |
| `docs/nautilus/transmission-box/00-question-mountain-to-person.md` | ~2 мин | 516 | 📗 Быстро |
| `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` | ~2 мин | 600 | 📗 Быстро |
| `docs/02-anthropic-vacancies/175-6-ethical-framework.md` | ~2 мин | 590 | 📗 Быстро |
| `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` | ~2 мин | 508 | 📗 Быстро |
| `docs/ONBOARDING.md` | ~2 мин | 291 | 📗 Быстро |
| `docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md` | ~2 мин | 503 | 📗 Быстро |
| `docs/anthropic-vacancies/mmorpg-for-programmers/00-question-mmorpg-for-programmers.md` | ~2 мин | 491 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/13-acknowledgments-refs.md` | ~2 мин | 460 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-en/01-cowork-discovery.md` | ~2 мин | 606 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-en/02-cowork-provides.md` | ~2 мин | 593 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-ru/08-implikatsii-nautilus-okwf.md` | ~2 мин | 498 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-ru/09-riski-voprosy.md` | ~2 мин | 498 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/12-onboarding-paths.md` | ~2 мин | 308 | 📗 Быстро |
| `docs/nautilus/okwf-concept/08-risk-analysis.md` | ~2 мин | 586 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-en/09-relationship-other-agents.md` | ~2 мин | 600 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/03-what-makes-representative-agent.md` | ~2 мин | 597 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/05-architectural-specification.md` | ~2 мин | 584 | 📗 Быстро |
| `docs/technology-combinations/combinations/19-multi-agent-observability-platform.md` | ~2 мин | 574 | 📗 Быстро |
| `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` | ~2 мин | 283 | 📗 Быстро |
| `docs/02-anthropic-vacancies/18-6-adapter-interface.md` | ~2 мин | 290 | 📗 Быстро |
| `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` | ~2 мин | 415 | 📗 Быстро |
| `docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md` | ~2 мин | 502 | 📗 Быстро |
| `docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md` | ~2 мин | 479 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md` | ~2 мин | 480 | 📗 Быстро |
| `docs/nautilus/okwf-concept/10-appendices.md` | ~2 мин | 568 | 📗 Быстро |
| `docs/nautilus/privacy-federation/02-two-tier-publication.md` | ~2 мин | 515 | 📗 Быстро |
| `docs/nautilus/review-methodology/03-consolidation-principles.md` | ~2 мин | 273 | 📗 Быстро |
| `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` | ~2 мин | 358 | 📗 Быстро |
| `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` | ~2 мин | 554 | 📗 Быстро |
| `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` | ~2 мин | 552 | 📗 Быстро |
| `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` | ~2 мин | 537 | 📗 Быстро |
| `docs/02-anthropic-vacancies/81-6-adapter-interface.md` | ~2 мин | 263 | 📗 Быстро |
| `docs/LANGUAGE_STATS.md` | ~2 мин | 503 | 📗 Быстро |
| `docs/lorenzo-agent/operationalized/05-anchor-node-habr-scout.md` | ~2 мин | 519 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-en/04-symbiotic-architecture.md` | ~2 мин | 424 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md` | ~2 мин | 547 | 📗 Быстро |
| `docs/nautilus/npp-humanitarian-extension/04-grant-opportunities.md` | ~2 мин | 506 | 📗 Быстро |
| `docs/nautilus/okwf-concept/01-problem-statement.md` | ~2 мин | 548 | 📗 Быстро |
| `docs/nautilus/okwf-concept/07-phased-rollout.md` | ~2 мин | 555 | 📗 Быстро |
| `docs/02-anthropic-vacancies/126-установка.md` | ~2 мин | 127 | 📗 Быстро |
| `docs/02-anthropic-vacancies/159-5-economic-model.md` | ~2 мин | 528 | 📗 Быстро |
| `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` | ~2 мин | 429 | 📗 Быстро |
| `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` | ~2 мин | 244 | 📗 Быстро |
| `docs/04-ai-collaborations/07-выводы.md` | ~2 мин | 465 | 📗 Быстро |
| `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | ~2 мин | 453 | 📗 Быстро |
| `docs/NAMED_ENTITIES.md` | ~2 мин | 477 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/00-intro.md` | ~2 мин | 470 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-en/09-risks-open-questions.md` | ~2 мин | 513 | 📗 Быстро |
| `docs/nautilus/supply-demand/00-question-supply-demand.md` | ~2 мин | 426 | 📗 Быстро |
| `docs/technology-combinations/combinations/14-local-first-agent-development-environment.md` | ~2 мин | 498 | 📗 Быстро |
| `docs/01-svyazi/02-methodology.md` | ~1 мин | 413 | 📗 Быстро |
| `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` | ~2 мин | 239 | 📗 Быстро |
| `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` | ~2 мин | 409 | 📗 Быстро |
| `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` | ~2 мин | 503 | 📗 Быстро |
| `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` | ~1 мин | 403 | 📗 Быстро |
| `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` | ~1 мин | 485 | 📗 Быстро |
| `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` | ~1 мин | 218 | 📗 Быстро |
| `docs/BROKEN_LINKS.md` | ~2 мин | 437 | 📗 Быстро |
| `docs/TECH_RADAR.md` | ~2 мин | 331 | 📗 Быстро |
| `docs/ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md` | ~2 мин | 446 | 📗 Быстро |
| `docs/ai-collaborations/source-projects.md` | ~2 мин | 468 | 📗 Быстро |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/00-question-two-nautiluses.md` | ~2 мин | 426 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md` | ~1 мин | 439 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/00-question-habr-examples.md` | ~1 мин | 417 | 📗 Быстро |
| `docs/habr-unique-projects/software-pairs/5-browser-agents-headless.md` | ~1 мин | 436 | 📗 Быстро |
| `docs/lorenzo-agent/operationalized/06-conclusion-deserves-attention.md` | ~2 мин | 462 | 📗 Быстро |
| `docs/nautilus/README.md` | ~1 мин | 447 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/05-priblizheniya.md` | ~1 мин | 416 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/15-glossary.md` | ~2 мин | 116 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-ru/12-zaklyuchenie.md` | ~2 мин | 408 | 📗 Быстро |
| `docs/technology-combinations/combinations/24-mega-integration-full-stack.md` | ~1 мин | 468 | 📗 Быстро |
| `docs/01-svyazi/08-conclusions.md` | ~1 мин | 421 | 📗 Быстро |
| `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` | ~1 мин | 461 | 📗 Быстро |
| `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` | ~1 мин | 390 | 📗 Быстро |
| `docs/02-anthropic-vacancies/76-1-introduction.md` | ~1 мин | 412 | 📗 Быстро |
| `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` | ~1 мин | 317 | 📗 Быстро |
| `docs/REPORT.md` | ~1 мин | 302 | 📗 Быстро |
| `docs/ai-collaborations/continuation/01-shared-memory-between-agents.md` | ~1 мин | 410 | 📗 Быстро |
| `docs/lorenzo-agent/operationalized/01-pluses-1-7.md` | ~1 мин | 426 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md` | ~1 мин | 469 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/18-comment-on-document.md` | ~1 мин | 405 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-en/12-closing.md` | ~1 мин | 458 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/06-eticheskaya-ramka.md` | ~1 мин | 393 | 📗 Быстро |
| `docs/nautilus/review-methodology/02-formal-workflow.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/svyazi-2-0/overview/executive-summary.md` | ~1 мин | 424 | 📗 Быстро |
| `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` | ~1 мин | 282 | 📗 Быстро |
| `docs/02-anthropic-vacancies/130-отладка.md` | ~1 мин | 172 | 📗 Быстро |
| `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` | ~1 мин | 366 | 📗 Быстро |
| `docs/02-anthropic-vacancies/266-13-closing.md` | ~1 мин | 435 | 📗 Быстро |
| `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` | ~1 мин | 368 | 📗 Быстро |
| `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` | ~1 мин | 288 | 📗 Быстро |
| `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | ~1 мин | 182 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md` | ~1 мин | 388 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/2-distributed-agent-workshop.md` | ~1 мин | 385 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/3-forensic-rag.md` | ~1 мин | 383 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/5-agent-firewall.md` | ~1 мин | 391 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/11-open-questions.md` | ~1 мин | 450 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/06-existing-approximations.md` | ~1 мин | 439 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md` | ~1 мин | 364 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/03-registry.md` | ~1 мин | 285 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/06-adapter-interface.md` | ~1 мин | 177 | 📗 Быстро |
| `docs/nautilus/okwf-concept/06-governance-ethics.md` | ~1 мин | 441 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/08-risks-mitigations.md` | ~1 мин | 442 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md` | ~1 мин | 370 | 📗 Быстро |
| `docs/nautilus/review-methodology/01-context-motivation.md` | ~1 мин | 267 | 📗 Быстро |
| `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` | ~1 мин | 265 | 📗 Быстро |
| `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | ~1 мин | 359 | 📗 Быстро |
| `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` | ~1 мин | 251 | 📗 Быстро |
| `docs/02-anthropic-vacancies/136-abstract.md` | ~1 мин | 417 | 📗 Быстро |
| `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` | ~1 мин | 432 | 📗 Быстро |
| `docs/02-anthropic-vacancies/221-10-open-questions.md` | ~1 мин | 429 | 📗 Быстро |
| `docs/02-anthropic-vacancies/223-12-closing.md` | ~1 мин | 412 | 📗 Быстро |
| `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` | ~1 мин | 347 | 📗 Быстро |
| `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` | ~1 мин | 414 | 📗 Быстро |
| `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` | ~1 мин | 347 | 📗 Быстро |
| `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` | ~1 мин | 343 | 📗 Быстро |
| `docs/02-anthropic-vacancies/337-благодарности.md` | ~1 мин | 364 | 📗 Быстро |
| `docs/03-technology-combinations/03-local-first.md` | ~1 мин | 379 | 📗 Быстро |
| `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` | ~1 мин | 369 | 📗 Быстро |
| `docs/VOCABULARY.md` | ~1 мин | 354 | 📗 Быстро |
| `docs/ai-collaborations/continuation/02-agentops-trace-envelope.md` | ~1 мин | 379 | 📗 Быстро |
| `docs/anthropic-vacancies/mmorpg-for-programmers/01-why-stronger-than-it-looks.md` | ~1 мин | 348 | 📗 Быстро |
| `docs/habr-unique-projects/analogues/01-three-direct-analogues.md` | ~1 мин | 357 | 📗 Быстро |
| `docs/lorenzo-agent/operationalized/04-recommendations.md` | ~1 мин | 395 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/06-adapter-interface.md` | ~1 мин | 154 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/01-introduction.md` | ~1 мин | 358 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/07-portal-entry.md` | ~1 мин | 146 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/09-consensus-algorithm.md` | ~1 мин | 165 | 📗 Быстро |
| `docs/nautilus/okwf-concept/05-economic-model.md` | ~1 мин | 430 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/06-ethical-framework.md` | ~1 мин | 425 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/07-upravlenie-nadzor.md` | ~1 мин | 342 | 📗 Быстро |
| `docs/technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md` | ~1 мин | 401 | 📗 Быстро |
| `docs/technology-combinations/combinations/README.md` | ~1 мин | 429 | 📗 Быстро |
| `docs/02-anthropic-vacancies/179-10-open-questions.md` | ~1 мин | 406 | 📗 Быстро |
| `docs/02-anthropic-vacancies/189-аннотация.md` | ~1 мин | 320 | 📗 Быстро |
| `docs/02-anthropic-vacancies/243-12-заключение.md` | ~1 мин | 335 | 📗 Быстро |
| `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` | ~1 мин | 398 | 📗 Быстро |
| `docs/02-anthropic-vacancies/281-the-recursive-insight.md` | ~1 мин | 389 | 📗 Быстро |
| `docs/02-anthropic-vacancies/319-acknowledgments.md` | ~1 мин | 387 | 📗 Быстро |
| `docs/02-anthropic-vacancies/77-2-terminology.md` | ~1 мин | 348 | 📗 Быстро |
| `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` | ~1 мин | 141 | 📗 Быстро |
| `docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md` | ~1 мин | 351 | 📗 Быстро |
| `docs/anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md` | ~1 мин | 337 | 📗 Быстро |
| `docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md` | ~1 мин | 359 | 📗 Быстро |
| `docs/anthropic-vacancies/mmorpg-for-programmers/02-existing-niche.md` | ~1 мин | 351 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md` | ~1 мин | 352 | 📗 Быстро |
| `docs/habr-unique-projects/analogues/02-related-projects.md` | ~1 мин | 341 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/12-concrete-next-step.md` | ~1 мин | 366 | 📗 Быстро |
| `docs/habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md` | ~1 мин | 334 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md` | ~1 мин | 407 | 📗 Быстро |
| `docs/nautilus/okwf-concept/09-call-for-partnership.md` | ~1 мин | 398 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/09-phased-rollout.md` | ~1 мин | 389 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/10-otkrytye-voprosy.md` | ~1 мин | 329 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md` | ~1 мин | 332 | 📗 Быстро |
| `docs/svyazi-2-0/ensembles/G-federated-local-graph.md` | ~1 мин | 234 | 📗 Быстро |
| `docs/svyazi-2-0/limitations/do-not-glue.md` | ~1 мин | 336 | 📗 Быстро |
| `docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md` | ~1 мин | 400 | 📗 Быстро |
| `docs/02-anthropic-vacancies/06-1-introduction.md` | ~1 мин | 334 | 📗 Быстро |
| `docs/02-anthropic-vacancies/153-executive-summary.md` | ~1 мин | 370 | 📗 Быстро |
| `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` | ~1 мин | 365 | 📗 Быстро |
| `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | ~1 мин | 363 | 📗 Быстро |
| `docs/02-anthropic-vacancies/230-аннотация.md` | ~1 мин | 309 | 📗 Быстро |
| `docs/02-anthropic-vacancies/268-references.md` | ~1 мин | 378 | 📗 Быстро |
| `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` | ~1 мин | 236 | 📗 Быстро |
| `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` | ~1 мин | 384 | 📗 Быстро |
| `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` | ~1 мин | 130 | 📗 Быстро |
| `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` | ~1 мин | 372 | 📗 Быстро |
| `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` | ~1 мин | 310 | 📗 Быстро |
| `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` | ~1 мин | 312 | 📗 Быстро |
| `docs/02-anthropic-vacancies/325-аннотация.md` | ~1 мин | 326 | 📗 Быстро |
| `docs/02-anthropic-vacancies/90-15-security-considerations.md` | ~1 мин | 343 | 📗 Быстро |
| `docs/KNOWLEDGE_MAP.md` | ~1 мин | 220 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/6-continuous-eval-loop.md` | ~1 мин | 327 | 📗 Быстро |
| `docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md` | ~1 мин | 319 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md` | ~1 мин | 376 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md` | ~1 мин | 334 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md` | ~1 мин | 332 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/00-abstract.md` | ~1 мин | 375 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-ru/06-utochnyonnyy-obyom-ingit.md` | ~1 мин | 324 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-ru/07-prakticheskie-shagi.md` | ~1 мин | 311 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/08-q6-space.md` | ~1 мин | 229 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/14-sdk.md` | ~1 мин | 124 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-en/00-abstract.md` | ~1 мин | 362 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md` | ~1 мин | 295 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/07-governance-oversight.md` | ~1 мин | 373 | 📗 Быстро |
| `docs/nautilus/review-methodology/04-fallback-ratio-question.md` | ~1 мин | 222 | 📗 Быстро |
| `docs/svyazi-2-0/ensembles/C-multi-agent-factory.md` | ~1 мин | 213 | 📗 Быстро |
| `docs/svyazi-2-0/ensembles/D-voice-first-mesh.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/svyazi-2-0/ensembles/F-evidence-backed-intake.md` | ~1 мин | 213 | 📗 Быстро |
| `docs/svyazi-2-0/limitations/conclusions.md` | ~1 мин | 321 | 📗 Быстро |
| `docs/technology-combinations/synthesis-tables/01-08-summary.md` | ~1 мин | 344 | 📗 Быстро |
| `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` | ~1 мин | 311 | 📗 Быстро |
| `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` | ~1 мин | 299 | 📗 Быстро |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | ~1 мин | 192 | 📗 Быстро |
| `docs/02-anthropic-vacancies/210-abstract.md` | ~1 мин | 352 | 📗 Быстро |
| `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | ~1 мин | 285 | 📗 Быстро |
| `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` | ~1 мин | 289 | 📗 Быстро |
| `docs/02-anthropic-vacancies/252-abstract.md` | ~1 мин | 352 | 📗 Быстро |
| `docs/02-anthropic-vacancies/275-why-this-document-exists.md` | ~1 мин | 338 | 📗 Быстро |
| `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` | ~1 мин | 291 | 📗 Быстро |
| `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` | ~1 мин | 280 | 📗 Быстро |
| `docs/02-anthropic-vacancies/307-abstract.md` | ~1 мин | 342 | 📗 Быстро |
| `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` | ~1 мин | 322 | 📗 Быстро |
| `docs/02-anthropic-vacancies/57-native-format.md` | ~1 мин | 90 | 📗 Быстро |
| `docs/05-habr-projects/memory/ngt-memory.md` | ~1 мин | 296 | 📗 Быстро |
| `docs/GRAPH.md` | ~1 мин | 97 | 📗 Быстро |
| `docs/ai-collaborations/candidates/01-three-key-candidates.md` | ~1 мин | 302 | 📗 Быстро |
| `docs/ai-collaborations/continuation/05-roadmap-6-12-months.md` | ~1 мин | 309 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/4-web-to-knowledge-pipeline.md` | ~1 мин | 302 | 📗 Быстро |
| `docs/anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md` | ~1 мин | 338 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md` | ~1 мин | 308 | 📗 Быстро |
| `docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md` | ~1 мин | 320 | 📗 Быстро |
| `docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md` | ~1 мин | 314 | 📗 Быстро |
| `docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md` | ~1 мин | 305 | 📗 Быстро |
| `docs/habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md` | ~1 мин | 303 | 📗 Быстро |
| `docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md` | ~1 мин | 301 | 📗 Быстро |
| `docs/habr-unique-projects/hardware-pairs/7-metaphor.md` | ~1 мин | 299 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/12-call-for-collaboration.md` | ~1 мин | 334 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/03-two-layer-stack.md` | ~1 мин | 350 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/05-why-not-built.md` | ~1 мин | 338 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/02-dvukhsloynyy-stek.md` | ~1 мин | 294 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/04-pochemu-ne-postroeno.md` | ~1 мин | 293 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/07-rekursivnoe-prozrenie.md` | ~1 мин | 300 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/10-rekomendatsii.md` | ~1 мин | 290 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-en/06-refined-ingit-scope.md` | ~1 мин | 337 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-en/07-practical-first-steps.md` | ~1 мин | 338 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md` | ~1 мин | 207 | 📗 Быстро |
| `docs/nautilus/privacy-federation/04-what-i-can-do-now.md` | ~1 мин | 318 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/00-abstract.md` | ~1 мин | 347 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/10-open-questions.md` | ~1 мин | 358 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/11-call-for-collaboration.md` | ~1 мин | 351 | 📗 Быстро |
| `docs/nautilus/review-methodology/09-limitations-open-questions.md` | ~1 мин | 292 | 📗 Быстро |
| `docs/svyazi-2-0/ensembles/A-collaboration-os.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/svyazi-2-0/ensembles/B-forensic-rag.md` | ~1 мин | 201 | 📗 Быстро |
| `docs/svyazi-2-0/ensembles/E-execution-plane.md` | ~1 мин | 207 | 📗 Быстро |
| `docs/svyazi-2-0/ensembles/H-research-to-product-flywheel.md` | ~1 мин | 199 | 📗 Быстро |
| `docs/svyazi-2-0/security/budget-routing.md` | ~1 мин | 296 | 📗 Быстро |
| `docs/svyazi-2-0/security/default-policy.md` | ~1 мин | 313 | 📗 Быстро |
| `docs/02-anthropic-vacancies/07-2-terminology.md` | ~1 мин | 278 | 📗 Быстро |
| `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` | ~1 мин | 285 | 📗 Быстро |
| `docs/02-anthropic-vacancies/168-abstract.md` | ~1 мин | 328 | 📗 Быстро |
| `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` | ~1 мин | 334 | 📗 Быстро |
| `docs/02-anthropic-vacancies/267-acknowledgments.md` | ~1 мин | 313 | 📗 Быстро |
| `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` | ~1 мин | 195 | 📗 Быстро |
| `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` | ~1 мин | 321 | 📗 Быстро |
| `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` | ~1 мин | 295 | 📗 Быстро |
| `docs/02-anthropic-vacancies/QA.md` | ~1 мин | 285 | 📗 Быстро |
| `docs/FOOTNOTES.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/MINDMAP.md` | ~1 мин | 70 | 📗 Быстро |
| `docs/VALIDATION.md` | ~1 мин | 270 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md` | ~1 мин | 289 | 📗 Быстро |
| `docs/ai-collaborations/fast-tracks/README.md` | ~1 мин | 278 | 📗 Быстро |
| `docs/anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md` | ~1 мин | 289 | 📗 Быстро |
| `docs/anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md` | ~1 мин | 283 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md` | ~1 мин | 277 | 📗 Быстро |
| `docs/habr-unique-projects/deep-pairs/2-document-rag.md` | ~1 мин | 291 | 📗 Быстро |
| `docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md` | ~1 мин | 283 | 📗 Быстро |
| `docs/habr-unique-projects/software-pairs/2-pkm-mcp-skills.md` | ~1 мин | 301 | 📗 Быстро |
| `docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md` | ~1 мин | 279 | 📗 Быстро |
| `docs/lorenzo-agent/10-collaborators-landscape.md` | ~1 мин | 307 | 📗 Быстро |
| `docs/lorenzo-agent/naming/01-search-results-not-found.md` | ~1 мин | 295 | 📗 Быстро |
| `docs/lorenzo-agent/specification/01-q1-what-lorenzo-is.md` | ~1 мин | 323 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/08-recursive-insight.md` | ~1 мин | 333 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/11-practical-recommendations.md` | ~1 мин | 320 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md` | ~1 мин | 266 | 📗 Быстро |
| `docs/nautilus/npp-humanitarian-extension/00-question-can-it-apply-to-docs.md` | ~1 мин | 284 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/03-registry.md` | ~1 мин | 170 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/00-abstract-status.md` | ~1 мин | 277 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/02-terminology.md` | ~1 мин | 277 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/04-passport.md` | ~1 мин | 186 | 📗 Быстро |
| `docs/nautilus/okwf-concept/00-abstract.md` | ~1 мин | 333 | 📗 Быстро |
| `docs/nautilus/privacy-federation/00-question-anonymization.md` | ~1 мин | 285 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-en/10-open-questions.md` | ~1 мин | 311 | 📗 Быстро |
| `docs/svyazi-2-0/outreach/narrow-questions.md` | ~1 мин | 288 | 📗 Быстро |
| `docs/svyazi-2-0/prototype/mvp-plan.md` | ~1 мин | 276 | 📗 Быстро |
| `docs/svyazi-2-0/prototype/risks.md` | ~1 мин | 277 | 📗 Быстро |
| `docs/technology-combinations/synthesis-tables/25-30-extended.md` | ~1 мин | 191 | 📗 Быстро |
| `docs/technology-combinations/synthesis-tables/31-35-final.md` | ~1 мин | 200 | 📗 Быстро |
| `docs/02-anthropic-vacancies/147-references.md` | ~1 мин | 302 | 📗 Быстро |
| `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` | ~1 мин | 306 | 📗 Быстро |
| `docs/02-anthropic-vacancies/183-references.md` | ~1 мин | 298 | 📗 Быстро |
| `docs/02-anthropic-vacancies/204-ссылки.md` | ~1 мин | 257 | 📗 Быстро |
| `docs/02-anthropic-vacancies/225-references.md` | ~1 мин | 292 | 📗 Быстро |
| `docs/02-anthropic-vacancies/245-ссылки.md` | ~1 мин | 261 | 📗 Быстро |
| `docs/02-anthropic-vacancies/285-closing.md` | ~1 мин | 294 | 📗 Быстро |
| `docs/02-anthropic-vacancies/287-references.md` | ~1 мин | 302 | 📗 Быстро |
| `docs/02-anthropic-vacancies/302-ссылки.md` | ~1 мин | 263 | 📗 Быстро |
| `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` | ~1 мин | 307 | 📗 Быстро |
| `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | ~1 мин | 263 | 📗 Быстро |
| `docs/03-technology-combinations/01-agent-routing.md` | ~1 мин | 262 | 📗 Быстро |
| `docs/CONTACTS.md` | ~1 мин | 151 | 📗 Быстро |
| `docs/CONTACT_PRIORITY.md` | ~1 мин | 150 | 📗 Быстро |
| `docs/DIGEST.md` | ~1 мин | 282 | 📗 Быстро |
| `docs/PROGRESS.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md` | ~1 мин | 253 | 📗 Быстро |
| `docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md` | ~1 мин | 260 | 📗 Быстро |
| `docs/ai-collaborations/continuation/08-commercialization-three-paths.md` | ~1 мин | 268 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md` | ~1 мин | 275 | 📗 Быстро |
| `docs/anthropic-vacancies/extra-collaborator-findings/01-coally.md` | ~1 мин | 255 | 📗 Быстро |
| `docs/anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md` | ~1 мин | 264 | 📗 Быстро |
| `docs/anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md` | ~1 мин | 271 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/12-minuses-of-hermes.md` | ~1 мин | 288 | 📗 Быстро |
| `docs/habr-unique-projects/deep-pairs/1-llm-gateway.md` | ~1 мин | 274 | 📗 Быстро |
| `docs/habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md` | ~1 мин | 271 | 📗 Быстро |
| `docs/habr-unique-projects/deep-pairs/5-voice-local-memory.md` | ~1 мин | 265 | 📗 Быстро |
| `docs/habr-unique-projects/deep-pairs/7-autoresearch-distributed.md` | ~1 мин | 257 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/10-profession-specific-workflows.md` | ~1 мин | 275 | 📗 Быстро |
| `docs/habr-unique-projects/hardware-pairs/2-tsu-mome.md` | ~1 мин | 268 | 📗 Быстро |
| `docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md` | ~1 мин | 268 | 📗 Быстро |
| `docs/habr-unique-projects/hardware-pairs/4-riscv-privacy.md` | ~1 мин | 276 | 📗 Быстро |
| `docs/habr-unique-projects/key-findings/04-dochkina-sequential.md` | ~1 мин | 256 | 📗 Быстро |
| `docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md` | ~1 мин | 263 | 📗 Быстро |
| `docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md` | ~1 мин | 265 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md` | ~1 мин | 296 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/02-why-document-exists.md` | ~1 мин | 296 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/01-zachem-dokument.md` | ~1 мин | 241 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/01-introduction.md` | ~1 мин | 250 | 📗 Быстро |
| `docs/nautilus/privacy-federation/01-what-to-anonymize-german-standard.md` | ~1 мин | 260 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md` | ~1 мин | 235 | 📗 Быстро |
| `docs/nautilus/review-methodology/06-relation-existing-methodologies.md` | ~1 мин | 268 | 📗 Быстро |
| `docs/nautilus/review-methodology/11-application-plan-current-docs.md` | ~1 мин | 158 | 📗 Быстро |
| `docs/svyazi-2-0/limitations/license-tree.md` | ~1 мин | 259 | 📗 Быстро |
| `docs/svyazi-2-0/overview/continuation-intro.md` | ~1 мин | 261 | 📗 Быстро |
| `docs/svyazi-2-0/overview/methodology.md` | ~1 мин | 258 | 📗 Быстро |
| `docs/technology-combinations/mega-stacks/01-legal-ai-stack.md` | ~1 мин | 164 | 📗 Быстро |
| `docs/templates/ensemble.md` | ~1 мин | 52 | 📗 Быстро |
| `docs/02-anthropic-vacancies/111-4-условия-применимости.md` | ~1 мин | 245 | 📗 Быстро |
| `docs/02-anthropic-vacancies/123-portal-mcp-py.md` | ~1 мин | 145 | 📗 Быстро |
| `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` | ~1 мин | 249 | 📗 Быстро |
| `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` | ~1 мин | 144 | 📗 Быстро |
| `docs/02-anthropic-vacancies/300-заключение.md` | ~1 мин | 226 | 📗 Быстро |
| `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | ~1 мин | 279 | 📗 Быстро |
| `docs/02-anthropic-vacancies/74-abstract.md` | ~1 мин | 233 | 📗 Быстро |
| `docs/COMPONENT_MATRIX.md` | ~1 мин | 252 | 📗 Быстро |
| `docs/CONCEPT_GRAPH.md` | ~1 мин | 136 | 📗 Быстро |
| `docs/CROSS_SECTION.md` | ~1 мин | 119 | 📗 Быстро |
| `docs/HEATMAP.md` | ~1 мин | 124 | 📗 Быстро |
| `docs/ai-collaborations/continuation/09-do-not-glue.md` | ~1 мин | 242 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/9-ambient-team-agent.md` | ~1 мин | 248 | 📗 Быстро |
| `docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md` | ~1 мин | 245 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/00-context.md` | ~1 мин | 250 | 📗 Быстро |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md` | ~1 мин | 233 | 📗 Быстро |
| `docs/anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md` | ~1 мин | 269 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/02-three-overlapping-identities.md` | ~1 мин | 252 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/03-revised-anthropic-mapping.md` | ~1 мин | 247 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md` | ~1 мин | 240 | 📗 Быстро |
| `docs/contacts/anastasiyaw.md` | ~1 мин | 126 | 📗 Быстро |
| `docs/contacts/andrey-chuyan.md` | ~1 мин | 135 | 📗 Быстро |
| `docs/contacts/spbmolot.md` | ~1 мин | 129 | 📗 Быстро |
| `docs/contacts/vitalyoborin.md` | ~1 мин | 125 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md` | ~1 мин | 243 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md` | ~1 мин | 246 | 📗 Быстро |
| `docs/habr-unique-projects/final-ensembles/4-summary-authors.md` | ~1 мин | 234 | 📗 Быстро |
| `docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md` | ~1 мин | 247 | 📗 Быстро |
| `docs/habr-unique-projects/software-pairs/6-metaphor.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/lorenzo-agent/05-tvoya-lichnost.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/lorenzo-agent/naming/00-question-lorenzo-codename.md` | ~1 мин | 229 | 📗 Быстро |
| `docs/lorenzo-agent/specification/04-q4-character.md` | ~1 мин | 261 | 📗 Быстро |
| `docs/nautilus/community-discussions/practical-observations/00-question-practical.md` | ~1 мин | 224 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md` | ~1 мин | 276 | 📗 Быстро |
| `docs/svyazi-2-0/outreach/first-contacts.md` | ~1 мин | 239 | 📗 Быстро |
| `docs/technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md` | ~1 мин | 238 | 📗 Быстро |
| `docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md` | ~1 мин | 278 | 📗 Быстро |
| `docs/technology-combinations/mega-stacks/02-ultimate-legal-ai.md` | ~1 мин | 140 | 📗 Быстро |
| `docs/technology-combinations/mega-stacks/04-event-sourcing-consensus.md` | ~1 мин | 137 | 📗 Быстро |
| `docs/technology-combinations/research-reports/continuation-10-domains.md` | ~1 мин | 246 | 📗 Быстро |
| `docs/01-svyazi/QA.md` | ~1 мин | 165 | 📗 Быстро |
| `docs/01-svyazi/README.md` | ~1 мин | 85 | 📗 Быстро |
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | ~1 мин | 142 | 📗 Быстро |
| `docs/02-anthropic-vacancies/04-abstract.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | ~1 мин | 123 | 📗 Быстро |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | ~1 мин | 144 | 📗 Быстро |
| `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` | ~1 мин | 169 | 📗 Быстро |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | ~1 мин | 111 | 📗 Быстро |
| `docs/02-anthropic-vacancies/106-tl-dr.md` | ~1 мин | 147 | 📗 Быстро |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | ~1 мин | 141 | 📗 Быстро |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | ~1 мин | 57 | 📗 Быстро |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | ~1 мин | 64 | 📗 Быстро |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | ~1 мин | 133 | 📗 Быстро |
| `docs/02-anthropic-vacancies/128-доступные-инструменты.md` | ~1 мин | 138 | 📗 Быстро |
| `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` | ~1 мин | 126 | 📗 Быстро |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | ~1 мин | 102 | 📗 Быстро |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | ~1 мин | 103 | 📗 Быстро |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | ~1 мин | 84 | 📗 Быстро |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | ~1 мин | 70 | 📗 Быстро |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | ~1 мин | 154 | 📗 Быстро |
| `docs/02-anthropic-vacancies/146-acknowledgments.md` | ~1 мин | 248 | 📗 Быстро |
| `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` | ~1 мин | 201 | 📗 Быстро |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | ~1 мин | 74 | 📗 Быстро |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | ~1 мин | 91 | 📗 Быстро |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | ~1 мин | 74 | 📗 Быстро |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | ~1 мин | 196 | 📗 Быстро |
| `docs/02-anthropic-vacancies/169-table-of-contents.md` | ~1 мин | 129 | 📗 Быстро |
| `docs/02-anthropic-vacancies/181-12-closing.md` | ~1 мин | 247 | 📗 Быстро |
| `docs/02-anthropic-vacancies/182-acknowledgments.md` | ~1 мин | 193 | 📗 Быстро |
| `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` | ~1 мин | 249 | 📗 Быстро |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | ~1 мин | 74 | 📗 Быстро |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | ~1 мин | 75 | 📗 Быстро |
| `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` | ~1 мин | 164 | 📗 Быстро |
| `docs/02-anthropic-vacancies/190-содержание.md` | ~1 мин | 95 | 📗 Быстро |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | ~1 мин | 153 | 📗 Быстро |
| `docs/02-anthropic-vacancies/203-благодарности.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` | ~1 мин | 203 | 📗 Быстро |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | ~1 мин | 75 | 📗 Быстро |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | ~1 мин | 71 | 📗 Быстро |
| `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` | ~1 мин | 192 | 📗 Быстро |
| `docs/02-anthropic-vacancies/21-9-query-flow.md` | ~1 мин | 166 | 📗 Быстро |
| `docs/02-anthropic-vacancies/211-table-of-contents.md` | ~1 мин | 165 | 📗 Быстро |
| `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` | ~1 мин | 120 | 📗 Быстро |
| `docs/02-anthropic-vacancies/224-acknowledgments.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/02-anthropic-vacancies/23-11-security-considerations.md` | ~1 мин | 228 | 📗 Быстро |
| `docs/02-anthropic-vacancies/231-содержание.md` | ~1 мин | 111 | 📗 Быстро |
| `docs/02-anthropic-vacancies/24-12-versioning-policy.md` | ~1 мин | 174 | 📗 Быстро |
| `docs/02-anthropic-vacancies/244-благодарности.md` | ~1 мин | 133 | 📗 Быстро |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | ~1 мин | 70 | 📗 Быстро |
| `docs/02-anthropic-vacancies/25-13-reference-implementation.md` | ~1 мин | 120 | 📗 Быстро |
| `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` | ~1 мин | 187 | 📗 Быстро |
| `docs/02-anthropic-vacancies/253-table-of-contents.md` | ~1 мин | 141 | 📗 Быстро |
| `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` | ~1 мин | 207 | 📗 Быстро |
| `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | ~1 мин | 258 | 📗 Быстро |
| `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` | ~1 мин | 165 | 📗 Быстро |
| `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` | ~1 мин | 142 | 📗 Быстро |
| `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` | ~1 мин | 231 | 📗 Быстро |
| `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` | ~1 мин | 197 | 📗 Быстро |
| `docs/02-anthropic-vacancies/286-acknowledgments.md` | ~1 мин | 228 | 📗 Быстро |
| `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` | ~1 мин | 212 | 📗 Быстро |
| `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` | ~1 мин | 203 | 📗 Быстро |
| `docs/02-anthropic-vacancies/301-благодарности.md` | ~1 мин | 174 | 📗 Быстро |
| `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` | ~1 мин | 136 | 📗 Быстро |
| `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | ~1 мин | 114 | 📗 Быстро |
| `docs/02-anthropic-vacancies/308-table-of-contents.md` | ~1 мин | 147 | 📗 Быстро |
| `docs/02-anthropic-vacancies/320-references.md` | ~1 мин | 164 | 📗 Быстро |
| `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` | ~1 мин | 118 | 📗 Быстро |
| `docs/02-anthropic-vacancies/326-содержание.md` | ~1 мин | 107 | 📗 Быстро |
| `docs/02-anthropic-vacancies/338-ссылки.md` | ~1 мин | 154 | 📗 Быстро |
| `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | ~1 мин | 58 | 📗 Быстро |
| `docs/02-anthropic-vacancies/345-кто-ты.md` | ~1 мин | 175 | 📗 Быстро |
| `docs/02-anthropic-vacancies/346-твоё-происхождение.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | ~1 мин | 98 | 📗 Быстро |
| `docs/02-anthropic-vacancies/349-твоя-личность.md` | ~1 мин | 185 | 📗 Быстро |
| `docs/02-anthropic-vacancies/35-passports-info1-md.md` | ~1 мин | 105 | 📗 Быстро |
| `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` | ~1 мин | 141 | 📗 Быстро |
| `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` | ~1 мин | 148 | 📗 Быстро |
| `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` | ~1 мин | 168 | 📗 Быстро |
| `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` | ~1 мин | 227 | 📗 Быстро |
| `docs/02-anthropic-vacancies/356-твой-workflow.md` | ~1 мин | 201 | 📗 Быстро |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` | ~1 мин | 109 | 📗 Быстро |
| `docs/02-anthropic-vacancies/36-essence.md` | ~1 мин | 144 | 📗 Быстро |
| `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` | ~1 мин | 143 | 📗 Быстро |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | ~1 мин | 76 | 📗 Быстро |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | ~1 мин | 68 | 📗 Быстро |
| `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` | ~1 мин | 138 | 📗 Быстро |
| `docs/02-anthropic-vacancies/37-native-format.md` | ~1 мин | 135 | 📗 Быстро |
| `docs/02-anthropic-vacancies/38-content-overview.md` | ~1 мин | 117 | 📗 Быстро |
| `docs/02-anthropic-vacancies/39-angle-perspective.md` | ~1 мин | 118 | 📗 Быстро |
| `docs/02-anthropic-vacancies/40-bridges.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/02-anthropic-vacancies/41-compatibility-level.md` | ~1 мин | 92 | 📗 Быстро |
| `docs/02-anthropic-vacancies/42-author-contact.md` | ~1 мин | 98 | 📗 Быстро |
| `docs/02-anthropic-vacancies/43-history.md` | ~1 мин | 109 | 📗 Быстро |
| `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` | ~1 мин | 140 | 📗 Быстро |
| `docs/02-anthropic-vacancies/45-passports-pro2-md.md` | ~1 мин | 105 | 📗 Быстро |
| `docs/02-anthropic-vacancies/46-essence.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/02-anthropic-vacancies/47-native-format.md` | ~1 мин | 90 | 📗 Быстро |
| `docs/02-anthropic-vacancies/48-content-overview.md` | ~1 мин | 148 | 📗 Быстро |
| `docs/02-anthropic-vacancies/49-angle-perspective.md` | ~1 мин | 125 | 📗 Быстро |
| `docs/02-anthropic-vacancies/50-bridges.md` | ~1 мин | 144 | 📗 Быстро |
| `docs/02-anthropic-vacancies/51-compatibility-level.md` | ~1 мин | 91 | 📗 Быстро |
| `docs/02-anthropic-vacancies/52-author-contact.md` | ~1 мин | 128 | 📗 Быстро |
| `docs/02-anthropic-vacancies/53-history.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` | ~1 мин | 145 | 📗 Быстро |
| `docs/02-anthropic-vacancies/55-passports-meta-md.md` | ~1 мин | 105 | 📗 Быстро |
| `docs/02-anthropic-vacancies/56-essence.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/02-anthropic-vacancies/58-content-overview.md` | ~1 мин | 107 | 📗 Быстро |
| `docs/02-anthropic-vacancies/59-angle-perspective.md` | ~1 мин | 122 | 📗 Быстро |
| `docs/02-anthropic-vacancies/60-bridges.md` | ~1 мин | 128 | 📗 Быстро |
| `docs/02-anthropic-vacancies/61-compatibility-level.md` | ~1 мин | 90 | 📗 Быстро |
| `docs/02-anthropic-vacancies/62-author-contact.md` | ~1 мин | 94 | 📗 Быстро |
| `docs/02-anthropic-vacancies/63-history.md` | ~1 мин | 120 | 📗 Быстро |
| `docs/02-anthropic-vacancies/65-readme-md.md` | ~1 мин | 132 | 📗 Быстро |
| `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` | ~1 мин | 105 | 📗 Быстро |
| `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` | ~1 мин | 130 | 📗 Быстро |
| `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` | ~1 мин | 139 | 📗 Быстро |
| `docs/02-anthropic-vacancies/85-10-query-flow.md` | ~1 мин | 224 | 📗 Быстро |
| `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` | ~1 мин | 126 | 📗 Быстро |
| `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` | ~1 мин | 135 | 📗 Быстро |
| `docs/02-anthropic-vacancies/92-17-versioning-policy.md` | ~1 мин | 243 | 📗 Быстро |
| `docs/02-anthropic-vacancies/93-18-reference-implementation.md` | ~1 мин | 159 | 📗 Быстро |
| `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` | ~1 мин | 219 | 📗 Быстро |
| `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` | ~1 мин | 200 | 📗 Быстро |
| `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | ~1 мин | 169 | 📗 Быстро |
| `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` | ~1 мин | 227 | 📗 Быстро |
| `docs/03-technology-combinations/04-sozialrecht-domain.md` | ~1 мин | 192 | 📗 Быстро |
| `docs/03-technology-combinations/QA.md` | ~1 мин | 125 | 📗 Быстро |
| `docs/04-ai-collaborations/QA.md` | ~1 мин | 206 | 📗 Быстро |
| `docs/04-ai-collaborations/README.md` | ~1 мин | 155 | 📗 Быстро |
| `docs/05-habr-projects/01-synthesis.md` | ~1 мин | 111 | 📗 Быстро |
| `docs/05-habr-projects/02-collaboration-partners.md` | ~1 мин | 204 | 📗 Быстро |
| `docs/05-habr-projects/QA.md` | ~1 мин | 113 | 📗 Быстро |
| `docs/05-habr-projects/knowledge/wikontic.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/05-habr-projects/memory/yodoca.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/AUTHORS.md` | ~1 мин | 65 | 📗 Быстро |
| `docs/AUTOFILLED.md` | ~1 мин | 128 | 📗 Быстро |
| `docs/BACKLINKS.md` | ~1 мин | 58 | 📗 Быстро |
| `docs/CHANGELOG_AUTO.md` | ~1 мин | 251 | 📗 Быстро |
| `docs/CITATION_INDEX.md` | ~1 мин | 61 | 📗 Быстро |
| `docs/COMPARE.md` | ~1 мин | 62 | 📗 Быстро |
| `docs/COMPLEXITY.md` | ~1 мин | 118 | 📗 Быстро |
| `docs/CONSISTENCY.md` | ~1 мин | 90 | 📗 Быстро |
| `docs/CONTENT_GAPS.md` | ~1 мин | 152 | 📗 Быстро |
| `docs/COST.md` | ~1 мин | 227 | 📗 Быстро |
| `docs/CROSSREFS.md` | ~1 мин | 242 | 📗 Быстро |
| `docs/DENSITY.md` | ~1 мин | 125 | 📗 Быстро |
| `docs/DEPENDENCY_MAP.md` | ~1 мин | 78 | 📗 Быстро |
| `docs/DIGEST_AUTO.md` | ~1 мин | 225 | 📗 Быстро |
| `docs/ENTITIES.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/GLOSSARY.md` | ~1 мин | 77 | 📗 Быстро |
| `docs/HEALTH.md` | ~1 мин | 74 | 📗 Быстро |
| `docs/KEYWORD_INDEX.md` | ~1 мин | 150 | 📗 Быстро |
| `docs/LLM_SUMMARIES.md` | ~1 мин | 177 | 📗 Быстро |
| `docs/METRICS.md` | ~1 мин | 142 | 📗 Быстро |
| `docs/MISSING.md` | ~1 мин | 116 | 📗 Быстро |
| `docs/NETWORK.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/ORPHANS.md` | ~1 мин | 69 | 📗 Быстро |
| `docs/PASSIVE_VOICE.md` | ~1 мин | 196 | 📗 Быстро |
| `docs/READING_LIST.md` | ~1 мин | 188 | 📗 Быстро |
| `docs/SCHEDULE.md` | ~1 мин | 91 | 📗 Быстро |
| `docs/SCORING.md` | ~1 мин | 126 | 📗 Быстро |
| `docs/SEE_ALSO.md` | ~1 мин | 72 | 📗 Быстро |
| `docs/SENTIMENT.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/SOURCE_MAP.md` | ~1 мин | 98 | 📗 Быстро |
| `docs/STALENESS.md` | ~1 мин | 108 | 📗 Быстро |
| `docs/STATS.md` | ~1 мин | 76 | 📗 Быстро |
| `docs/TAGS.md` | ~1 мин | 67 | 📗 Быстро |
| `docs/WORD_CLOUD.md` | ~1 мин | 130 | 📗 Быстро |
| `docs/ai-collaborations/candidates/02-related-projects-context.md` | ~1 мин | 204 | 📗 Быстро |
| `docs/ai-collaborations/continuation/06-metrics-tree.md` | ~1 мин | 199 | 📗 Быстро |
| `docs/ai-collaborations/continuation/10-architecture-rfc.md` | ~1 мин | 175 | 📗 Быстро |
| `docs/ai-collaborations/continuation/README.md` | ~1 мин | 92 | 📗 Быстро |
| `docs/ai-collaborations/ensembles/README.md` | ~1 мин | 79 | 📗 Быстро |
| `docs/anthropic-vacancies/QA.md` | ~1 мин | 70 | 📗 Быстро |
| `docs/anthropic-vacancies/README.md` | ~1 мин | 99 | 📗 Быстро |
| `docs/anthropic-vacancies/ai-managed-virtual-company/README.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md` | ~1 мин | 177 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md` | ~1 мин | 175 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md` | ~1 мин | 168 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md` | ~1 мин | 212 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md` | ~1 мин | 163 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md` | ~1 мин | 148 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md` | ~1 мин | 163 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md` | ~1 мин | 156 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/anthropic-vacancies/beneficial-deployments-concept/README.md` | ~1 мин | 96 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/01-ai-research-engineering.md` | ~1 мин | 130 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/02-sales.md` | ~1 мин | 141 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/03-finance.md` | ~1 мин | 110 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/04-security.md` | ~1 мин | 91 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/05-marketing-brand.md` | ~1 мин | 103 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/06-engineering-design-product.md` | ~1 мин | 104 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md` | ~1 мин | 107 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/08-safeguards-trust-safety.md` | ~1 мин | 113 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/09-product-management-support-ops.md` | ~1 мин | 94 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/10-compute.md` | ~1 мин | 104 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/11-legal.md` | ~1 мин | 98 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/12-technical-program-management.md` | ~1 мин | 89 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/13-communications.md` | ~1 мин | 82 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/14-public-policy.md` | ~1 мин | 86 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/15-public-benefit.md` | ~1 мин | 85 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/16-people.md` | ~1 мин | 79 | 📗 Быстро |
| `docs/anthropic-vacancies/clusters/README.md` | ~1 мин | 100 | 📗 Быстро |
| `docs/anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md` | ~1 мин | 155 | 📗 Быстро |
| `docs/anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md` | ~1 мин | 209 | 📗 Быстро |
| `docs/anthropic-vacancies/extra-collaborator-findings/07-key-observation.md` | ~1 мин | 174 | 📗 Быстро |
| `docs/anthropic-vacancies/extra-collaborator-findings/README.md` | ~1 мин | 59 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md` | ~1 мин | 205 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md` | ~1 мин | 145 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md` | ~1 мин | 138 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md` | ~1 мин | 134 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md` | ~1 мин | 155 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md` | ~1 мин | 178 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md` | ~1 мин | 179 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md` | ~1 мин | 163 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/09-difference-4-institutional-vision.md` | ~1 мин | 164 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/10-difference-5-tool-vs-mission-drift.md` | ~1 мин | 165 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/11-pluses-of-hermes.md` | ~1 мин | 214 | 📗 Быстро |
| `docs/anthropic-vacancies/hermes-comparison/README.md` | ~1 мин | 124 | 📗 Быстро |
| `docs/anthropic-vacancies/methodology.md` | ~1 мин | 90 | 📗 Быстро |
| `docs/anthropic-vacancies/mmorpg-for-programmers/04-pluses-as-business.md` | ~1 мин | 145 | 📗 Быстро |
| `docs/anthropic-vacancies/mmorpg-for-programmers/README.md` | ~1 мин | 60 | 📗 Быстро |
| `docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md` | ~1 мин | 217 | 📗 Быстро |
| `docs/anthropic-vacancies/nautilus-vs-camel/01-passive-vs-active-roles.md` | ~1 мин | 183 | 📗 Быстро |
| `docs/anthropic-vacancies/nautilus-vs-camel/README.md` | ~1 мин | 73 | 📗 Быстро |
| `docs/anthropic-vacancies/overview.md` | ~1 мин | 222 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md` | ~1 мин | 177 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md` | ~1 мин | 228 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/05-quaternary-developer-education.md` | ~1 мин | 201 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md` | ~1 мин | 163 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md` | ~1 мин | 174 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md` | ~1 мин | 188 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/README.md` | ~1 мин | 71 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md` | ~1 мин | 207 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md` | ~1 мин | 176 | 📗 Быстро |
| `docs/anthropic-vacancies/profile-mapping/README.md` | ~1 мин | 126 | 📗 Быстро |
| `docs/anthropic-vacancies/signals.md` | ~1 мин | 230 | 📗 Быстро |
| `docs/contacts/README.md` | ~1 мин | 65 | 📗 Быстро |
| `docs/contacts/antipozitive.md` | ~1 мин | 113 | 📗 Быстро |
| `docs/contacts/cutcode.md` | ~1 мин | 109 | 📗 Быстро |
| `docs/contacts/dmitriila.md` | ~1 мин | 106 | 📗 Быстро |
| `docs/contacts/kksudo.md` | ~1 мин | 120 | 📗 Быстро |
| `docs/contacts/mixaill76.md` | ~1 мин | 112 | 📗 Быстро |
| `docs/contacts/nlaik.md` | ~1 мин | 119 | 📗 Быстро |
| `docs/contacts/sonia-black.md` | ~1 мин | 119 | 📗 Быстро |
| `docs/contacts/tagir-analyzes.md` | ~1 мин | 110 | 📗 Быстро |
| `docs/contacts/vladspace.md` | ~1 мин | 111 | 📗 Быстро |
| `docs/contacts/zodigancode.md` | ~1 мин | 108 | 📗 Быстро |
| `docs/habr-unique-projects/README.md` | ~1 мин | 232 | 📗 Быстро |
| `docs/habr-unique-projects/deep-pairs/README.md` | ~1 мин | 64 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md` | ~1 мин | 194 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/02-vshe-scientific-networking.md` | ~1 мин | 165 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/04-claude-subagents-patterns.md` | ~1 мин | 158 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/05-hw-nl2workflow.md` | ~1 мин | 233 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/06-platform-for-professional-communities.md` | ~1 мин | 199 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md` | ~1 мин | 204 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/09-federated-platform.md` | ~1 мин | 191 | 📗 Быстро |
| `docs/habr-unique-projects/extra-examples/README.md` | ~1 мин | 114 | 📗 Быстро |
| `docs/habr-unique-projects/final-ensembles/1-one-person-one-company.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/habr-unique-projects/final-ensembles/2-autoresearch-legal.md` | ~1 мин | 164 | 📗 Быстро |
| `docs/habr-unique-projects/final-ensembles/3-discovery-research.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/habr-unique-projects/hardware-pairs/README.md` | ~1 мин | 50 | 📗 Быстро |
| `docs/habr-unique-projects/key-findings/01-yodoca.md` | ~1 мин | 223 | 📗 Быстро |
| `docs/habr-unique-projects/key-findings/02-memnet.md` | ~1 мин | 199 | 📗 Быстро |
| `docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md` | ~1 мин | 220 | 📗 Быстро |
| `docs/habr-unique-projects/software-pairs/README.md` | ~1 мин | 50 | 📗 Быстро |
| `docs/lorenzo-agent/01-kto-ty.md` | ~1 мин | 147 | 📗 Быстро |
| `docs/lorenzo-agent/02-tvoyo-proishozhdenie.md` | ~1 мин | 157 | 📗 Быстро |
| `docs/lorenzo-agent/03-tvoya-missiya.md` | ~1 мин | 145 | 📗 Быстро |
| `docs/lorenzo-agent/04-komu-ty-sluzhish.md` | ~1 мин | 150 | 📗 Быстро |
| `docs/lorenzo-agent/06-yazyki-kultura.md` | ~1 мин | 181 | 📗 Быстро |
| `docs/lorenzo-agent/07-chto-mozhesh.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/lorenzo-agent/08-bez-max-approval.md` | ~1 мин | 151 | 📗 Быстро |
| `docs/lorenzo-agent/09-voobshche-nelzya.md` | ~1 мин | 147 | 📗 Быстро |
| `docs/lorenzo-agent/11-dhlab-documents.md` | ~1 мин | 179 | 📗 Быстро |
| `docs/lorenzo-agent/12-workflow.md` | ~1 мин | 180 | 📗 Быстро |
| `docs/lorenzo-agent/13-outreach-communication.md` | ~1 мин | 203 | 📗 Быстро |
| `docs/lorenzo-agent/14-other-ai-relationships.md` | ~1 мин | 166 | 📗 Быстро |
| `docs/lorenzo-agent/15-anti-patterns.md` | ~1 мин | 160 | 📗 Быстро |
| `docs/lorenzo-agent/16-vsegda-delaesh.md` | ~1 мин | 119 | 📗 Быстро |
| `docs/lorenzo-agent/17-honestly-ne-znaesh.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/lorenzo-agent/18-escalate-to-max.md` | ~1 мин | 123 | 📗 Быстро |
| `docs/lorenzo-agent/19-persistent-character.md` | ~1 мин | 157 | 📗 Быстро |
| `docs/lorenzo-agent/20-experiment.md` | ~1 мин | 144 | 📗 Быстро |
| `docs/lorenzo-agent/QA.md` | ~1 мин | 167 | 📗 Быстро |
| `docs/lorenzo-agent/README.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/lorenzo-agent/operationalized/03-honest-opinion.md` | ~1 мин | 176 | 📗 Быстро |
| `docs/lorenzo-agent/operationalized/README.md` | ~1 мин | 50 | 📗 Быстро |
| `docs/lorenzo-agent/phased-deployment/00-overview.md` | ~1 мин | 159 | 📗 Быстро |
| `docs/lorenzo-agent/phased-deployment/01-level-0-manual.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md` | ~1 мин | 226 | 📗 Быстро |
| `docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md` | ~1 мин | 208 | 📗 Быстро |
| `docs/lorenzo-agent/phased-deployment/04-level-3-medium-active.md` | ~1 мин | 215 | 📗 Быстро |
| `docs/lorenzo-agent/phased-deployment/05-level-4-extended-mature.md` | ~1 мин | 182 | 📗 Быстро |
| `docs/lorenzo-agent/phased-deployment/06-level-5-full-network.md` | ~1 мин | 142 | 📗 Быстро |
| `docs/lorenzo-agent/phased-deployment/07-progression-logic.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/lorenzo-agent/phased-deployment/README.md` | ~1 мин | 69 | 📗 Быстро |
| `docs/lorenzo-agent/scenarios/00-question-scenario.md` | ~1 мин | 180 | 📗 Быстро |
| `docs/lorenzo-agent/specification/00-context-fundamental-questions.md` | ~1 мин | 194 | 📗 Быстро |
| `docs/lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md` | ~1 мин | 226 | 📗 Быстро |
| `docs/lorenzo-agent/specification/03-q3-what-lorenzo-does.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/lorenzo-agent/specification/05-q5-authority-limits.md` | ~1 мин | 227 | 📗 Быстро |
| `docs/lorenzo-agent/specification/06-q6-accountability.md` | ~1 мин | 197 | 📗 Быстро |
| `docs/lorenzo-agent/specification/07-q7-success-metrics.md` | ~1 мин | 211 | 📗 Быстро |
| `docs/lorenzo-agent/specification/08-q8-other-ai-relationships.md` | ~1 мин | 198 | 📗 Быстро |
| `docs/lorenzo-agent/specification/09-q9-geographic-linguistic-scope.md` | ~1 мин | 198 | 📗 Быстро |
| `docs/lorenzo-agent/specification/10-q10-funding-model.md` | ~1 мин | 228 | 📗 Быстро |
| `docs/lorenzo-agent/specification/README.md` | ~1 мин | 86 | 📗 Быстро |
| `docs/nautilus/community-discussions/README.md` | ~1 мин | 76 | 📗 Быстро |
| `docs/nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md` | ~1 мин | 215 | 📗 Быстро |
| `docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md` | ~1 мин | 63 | 📗 Быстро |
| `docs/nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md` | ~1 мин | 157 | 📗 Быстро |
| `docs/nautilus/composite-skills-agents/README.md` | ~1 мин | 97 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/09-acknowledgments.md` | ~1 мин | 197 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/10-references.md` | ~1 мин | 224 | 📗 Быстро |
| `docs/nautilus/double-triangle-architecture/README.md` | ~1 мин | 94 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/00-intro.md` | ~1 мин | 137 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md` | ~1 мин | 208 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/12-closing.md` | ~1 мин | 186 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-en/README.md` | ~1 мин | 102 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md` | ~1 мин | 199 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md` | ~1 мин | 204 | 📗 Быстро |
| `docs/nautilus/infrastructure-layer-b-ru/README.md` | ~1 мин | 81 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-en/README.md` | ~1 мин | 77 | 📗 Быстро |
| `docs/nautilus/ingit-cowork-ru/README.md` | ~1 мин | 79 | 📗 Быстро |
| `docs/nautilus/multi-tier-architecture/00-question-multi-tier.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md` | ~1 мин | 219 | 📗 Быстро |
| `docs/nautilus/npp-humanitarian-extension/03-what-doesnt-exist-on-market.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md` | ~1 мин | 145 | 📗 Быстро |
| `docs/nautilus/npp-humanitarian-extension/README.md` | ~1 мин | 72 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/00-abstract-status.md` | ~1 мин | 161 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/02-terminology.md` | ~1 мин | 194 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/04-passport.md` | ~1 мин | 108 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/05-compatibility-levels.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/07-portal-entry.md` | ~1 мин | 92 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/08-consensus-algorithm.md` | ~1 мин | 220 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/09-query-flow.md` | ~1 мин | 144 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/10-query-result.md` | ~1 мин | 100 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/11-security-considerations.md` | ~1 мин | 167 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/12-versioning-policy.md` | ~1 мин | 134 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/13-reference-implementation.md` | ~1 мин | 99 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/14-adr-001-federation-over-merging.md` | ~1 мин | 192 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/17-appendix-b-change-log.md` | ~1 мин | 84 | 📗 Быстро |
| `docs/nautilus/npp-v1-0/README.md` | ~1 мин | 123 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/05-compatibility-levels.md` | ~1 мин | 226 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/10-query-flow.md` | ~1 мин | 172 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/11-relevance-ranking.md` | ~1 мин | 107 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/15-security.md` | ~1 мин | 239 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/16-mcp-extension.md` | ~1 мин | 121 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/17-versioning-policy.md` | ~1 мин | 171 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/18-reference-implementation.md` | ~1 мин | 132 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md` | ~1 мин | 204 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/20-adr-002-q6-first-class.md` | ~1 мин | 184 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md` | ~1 мин | 162 | 📗 Быстро |
| `docs/nautilus/npp-v1-1/README.md` | ~1 мин | 141 | 📗 Быстро |
| `docs/nautilus/okwf-concept/README.md` | ~1 мин | 73 | 📗 Быстро |
| `docs/nautilus/privacy-federation/README.md` | ~1 мин | 51 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-en/11-call-for-collaboration.md` | ~1 мин | 253 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-en/README.md` | ~1 мин | 90 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-ru/00-abstract.md` | ~1 мин | 113 | 📗 Быстро |
| `docs/nautilus/professional-colleague-agents-ru/README.md` | ~1 мин | 84 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-en/README.md` | ~1 мин | 89 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/00-abstract.md` | ~1 мин | 102 | 📗 Быстро |
| `docs/nautilus/representative-agent-layer-ru/README.md` | ~1 мин | 89 | 📗 Быстро |
| `docs/nautilus/review-methodology/00-tldr.md` | ~1 мин | 165 | 📗 Быстро |
| `docs/nautilus/review-methodology/05-conditions-of-applicability.md` | ~1 мин | 221 | 📗 Быстро |
| `docs/nautilus/review-methodology/07-why-valid-for-ai.md` | ~1 мин | 198 | 📗 Быстро |
| `docs/nautilus/review-methodology/08-implementation-nautilus.md` | ~1 мин | 220 | 📗 Быстро |
| `docs/nautilus/review-methodology/10-checklist.md` | ~1 мин | 192 | 📗 Быстро |
| `docs/nautilus/review-methodology/12-appendix-a-header-warning.md` | ~1 мин | 109 | 📗 Быстро |
| `docs/nautilus/review-methodology/14-main-technical-risks.md` | ~1 мин | 127 | 📗 Быстро |
| `docs/nautilus/review-methodology/15-appendix-c-history.md` | ~1 мин | 98 | 📗 Быстро |
| `docs/nautilus/review-methodology/README.md` | ~1 мин | 131 | 📗 Быстро |
| `docs/svyazi-2-0/README.md` | ~1 мин | 115 | 📗 Быстро |
| `docs/svyazi-2-0/architecture/card-envelope.md` | ~1 мин | 136 | 📗 Быстро |
| `docs/svyazi-2-0/architecture/evidence-envelope.md` | ~1 мин | 184 | 📗 Быстро |
| `docs/svyazi-2-0/architecture/integration-spec.md` | ~1 мин | 230 | 📗 Быстро |
| `docs/svyazi-2-0/architecture/memory-write-policy.md` | ~1 мин | 149 | 📗 Быстро |
| `docs/svyazi-2-0/architecture/review-record.md` | ~1 мин | 90 | 📗 Быстро |
| `docs/svyazi-2-0/architecture/skill-tool-policy.md` | ~1 мин | 144 | 📗 Быстро |
| `docs/svyazi-2-0/components/README.md` | ~1 мин | 113 | 📗 Быстро |
| `docs/svyazi-2-0/components/agent-memory-mcp.md` | ~1 мин | 129 | 📗 Быстро |
| `docs/svyazi-2-0/components/agentfs.md` | ~1 мин | 105 | 📗 Быстро |
| `docs/svyazi-2-0/components/ai-factory.md` | ~1 мин | 107 | 📗 Быстро |
| `docs/svyazi-2-0/components/autoresearch-sequential.md` | ~1 мин | 120 | 📗 Быстро |
| `docs/svyazi-2-0/components/graph-rag.md` | ~1 мин | 100 | 📗 Быстро |
| `docs/svyazi-2-0/components/hybrid-rag.md` | ~1 мин | 94 | 📗 Быстро |
| `docs/svyazi-2-0/components/knowledge-space.md` | ~1 мин | 101 | 📗 Быстро |
| `docs/svyazi-2-0/components/legal-rag.md` | ~1 мин | 100 | 📗 Быстро |
| `docs/svyazi-2-0/components/mclaude.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/svyazi-2-0/components/memnet.md` | ~1 мин | 103 | 📗 Быстро |
| `docs/svyazi-2-0/components/ngt-memory.md` | ~1 мин | 109 | 📗 Быстро |
| `docs/svyazi-2-0/components/research-docs-liteparse.md` | ~1 мин | 114 | 📗 Быстро |
| `docs/svyazi-2-0/components/rufler.md` | ~1 мин | 93 | 📗 Быстро |
| `docs/svyazi-2-0/components/security-routing-plane.md` | ~1 мин | 184 | 📗 Быстро |
| `docs/svyazi-2-0/components/self-aware-mcp.md` | ~1 мин | 133 | 📗 Быстро |
| `docs/svyazi-2-0/components/svyazi.md` | ~1 мин | 103 | 📗 Быстро |
| `docs/svyazi-2-0/components/voice-stack.md` | ~1 мин | 125 | 📗 Быстро |
| `docs/svyazi-2-0/components/yjs-automerge.md` | ~1 мин | 113 | 📗 Быстро |
| `docs/svyazi-2-0/components/yodoca.md` | ~1 мин | 104 | 📗 Быстро |
| `docs/svyazi-2-0/ensembles/README.md` | ~1 мин | 65 | 📗 Быстро |
| `docs/svyazi-2-0/outreach/message-template.md` | ~1 мин | 203 | 📗 Быстро |
| `docs/svyazi-2-0/security/privacy.md` | ~1 мин | 131 | 📗 Быстро |
| `docs/technology-combinations/README.md` | ~1 мин | 138 | 📗 Быстро |
| `docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md` | ~1 мин | 173 | 📗 Быстро |
| `docs/technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md` | ~1 мин | 193 | 📗 Быстро |
| `docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md` | ~1 мин | 197 | 📗 Быстро |
| `docs/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md` | ~1 мин | 208 | 📗 Быстро |
| `docs/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md` | ~1 мин | 213 | 📗 Быстро |
| `docs/technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md` | ~1 мин | 197 | 📗 Быстро |
| `docs/technology-combinations/combinations/09-agent-orchestration-stack.md` | ~1 мин | 196 | 📗 Быстро |
| `docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md` | ~1 мин | 194 | 📗 Быстро |
| `docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md` | ~1 мин | 198 | 📗 Быстро |
| `docs/technology-combinations/combinations/12-multi-agent-observability-stack.md` | ~1 мин | 176 | 📗 Быстро |
| `docs/technology-combinations/combinations/13-legal-document-transpiler.md` | ~1 мин | 186 | 📗 Быстро |
| `docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md` | ~1 мин | 240 | 📗 Быстро |
| `docs/technology-combinations/combinations/16-adversarial-multi-agent-code-review.md` | ~1 мин | 246 | 📗 Быстро |
| `docs/technology-combinations/combinations/17-distributed-agent-memory-with-graph.md` | ~1 мин | 213 | 📗 Быстро |
| `docs/technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md` | ~1 мин | 230 | 📗 Быстро |
| `docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md` | ~1 мин | 240 | 📗 Быстро |
| `docs/technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md` | ~1 мин | 249 | 📗 Быстро |
| `docs/technology-combinations/combinations/22-russian-international-oss-stack.md` | ~1 мин | 225 | 📗 Быстро |
| `docs/technology-combinations/combinations/23-security-first-code-review-pipeline.md` | ~1 мин | 186 | 📗 Быстро |
| `docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md` | ~1 мин | 230 | 📗 Быстро |
| `docs/technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md` | ~1 мин | 227 | 📗 Быстро |
| `docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md` | ~1 мин | 202 | 📗 Быстро |
| `docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md` | ~1 мин | 240 | 📗 Быстро |
| `docs/technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md` | ~1 мин | 238 | 📗 Быстро |
| `docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md` | ~1 мин | 215 | 📗 Быстро |
| `docs/technology-combinations/combinations/34-distributed-event-store-with-paxos.md` | ~1 мин | 189 | 📗 Быстро |
| `docs/technology-combinations/mega-stacks/03-dsl-ast.md` | ~1 мин | 115 | 📗 Быстро |
| `docs/technology-combinations/research-reports/sozialrecht-35-combinations.md` | ~1 мин | 197 | 📗 Быстро |
| `docs/technology-combinations/synthesis-tables/09-14-extended.md` | ~1 мин | 181 | 📗 Быстро |
| `docs/technology-combinations/synthesis-tables/15-19-extended.md` | ~1 мин | 153 | 📗 Быстро |
| `docs/technology-combinations/synthesis-tables/20-24-final.md` | ~1 мин | 190 | 📗 Быстро |
| `docs/templates/README.md` | ~1 мин | 70 | 📗 Быстро |
| `docs/templates/contact-outreach.md` | ~1 мин | 61 | 📗 Быстро |
| `docs/templates/project-component.md` | ~1 мин | 77 | 📗 Быстро |
| `docs/templates/research-note.md` | ~1 мин | 56 | 📗 Быстро |


### 114. Общая статистика
_Файл: `docs/REPORT.md` | 2 колонок, 6 строк_

| Метрика | Значение |
|---------|----------|
| Документов | **1170** |
| Слов | **907,362** |
| Секций | **18** |
| Здоровье репо | **77/100/100** |
| Средний балл | **71.3/100/100** |
| Словарное богатство (STTR) | **0.685** |


### 115. По секциям
_Файл: `docs/REPORT.md` | 3 колонок, 17 строк_

| Секция | Файлов | Слов |
|--------|--------|------|
| **Anthropic Vacancies** | 357 | 279,017 |
| **nautilus** | 255 | 148,523 |
| **anthropic-vacancies** | 111 | 30,929 |
| **AI Collaborations** | 17 | 26,057 |
| **lorenzo-agent** | 62 | 19,979 |
| **habr-unique-projects** | 56 | 13,161 |
| **technology-combinations** | 53 | 12,903 |
| **svyazi-2-0** | 59 | 12,455 |
| **Svyazi 2.0** | 16 | 10,998 |
| **Habr Projects** | 10 | 8,619 |
| **ai-collaborations** | 30 | 8,207 |
| **Contacts** | 15 | 3,151 |
| **Tech Combinations** | 7 | 2,796 |
| **glossary** | 4 | 2,282 |
| **Templates** | 6 | 635 |
| **autofilled** | 13 | 533 |
| **badges** | 1 | 44 |


### 116. Ключевые проекты
_Файл: `docs/REPORT.md` | 4 колонок, 8 строк_

| Автор | Проект | Слой | Приоритет |
|-------|--------|------|-----------|
| **AnastasiyaW** | knowledge-space, mclaude | knowledge/orchestration | 48 | Держать operational benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? |
| **Antipozitive** | MemNet | memory | 32 | — |
| **Cutcode** | AIF Handoff | orchestration | 34 | — |
| **Dmitriila** | SENTINEL | security | 34 | — |
| **MiXaiLL76** | Auto AI Router | security | 30 | — |
| **Sonia_Black** | knowledge-space | knowledge | 17 | — |
| **VitalyOborin** | Yodoca | memory | 37 | Что сильнее влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? |
| **VladSpace** | Graph RAG | rag | 41 | — |


### 117. Рекомендуемое чтение
_Файл: `docs/REPORT.md` | 5 колонок, 5 строк_

| # | Документ | Секция | Время | Слов |
|---|----------|--------|-------|------|
| 1 | [11 integration contracts](docs/01-svyazi/11-integration-contracts.md) | `01-svyazi` | 3 мин | 737 | 9.6 |
| 2 | [Интеграционный контракт, который стоит зафиксирова](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | `04-ai-collaborations` | 4 мин | 846 | 9.4 |
| 3 | [09 architectural gaps](docs/01-svyazi/09-architectural-gaps.md) | `01-svyazi` | 3 мин | 758 | 9.3 |
| 4 | [Архитектурные зазоры, которые важнее новых инструм](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | `04-ai-collaborations` | 4 мин | 805 | 9.2 |
| 5 | [03 component catalog](docs/01-svyazi/03-component-catalog.md) | `01-svyazi` | 6 мин | 1352 | 9.1 |


### 118. Реестр
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


### 119. Упоминания рисков в документах
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


### 120. Итоговая статистика
_Файл: `docs/RISK_REGISTER.md` | 2 колонок, 3 строк_

| Уровень | Кол-во |
|---------|--------|
| 🔴 КРИТИЧЕСКИЙ | 1 |
| 🟠 ВЫСОКИЙ | 7 |
| 🟡 СРЕДНИЙ | 2 |


### 121. Ключевые вехи
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


### 122. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 6 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Executive Summary существует | ✅ | 10 |
| Архитектурные контракты описаны | ✅ | 10 |
| MVP план задокументирован | ✅ | 10 |
| Дорожная карта есть | ✅ | 8 |
| README в каждом разделе | ✅ | 5 |
| Глоссарий создан | ✅ | 5 |


### 123. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 5 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Компоненты каталогизированы (20+) | ✅ | 10 |
| Ансамбли определены (5+) | ✅ | 10 |
| Архитектурные пробелы выявлены | ✅ | 8 |
| Безопасность и PII описаны | ✅ | 8 |
| Граф связей проектов построен | ✅ | 5 |


### 124. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 3 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Контакты авторов компонентов есть | ✅ | 10 |
| Авторы Habr-проектов найдены | ✅ | 8 |
| Шаблоны для связи созданы | ✅ | 5 |


### 125. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 6 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Риски выявлены и задокументированы | ✅ | 8 |
| Лицензии проверены | ✅ | 8 |
| Сломанных ссылок < 30 | ❌ | 5 |
|  ↳ _Слишком много сломанных ссылок_ | | |
| Дублей нет | ❌ | 5 |
|  ↳ _Есть точные дубли документов_ | | |


### 126. Документация — 48/48 (100%) 🟢 GO
_Файл: `docs/SCORING.md` | 3 колонок, 4 строк_

| Критерий | Статус | Вес |
|----------|--------|-----|
| Прогресс MVP отслеживается | ✅ | 8 |
| Action items задокументированы | ✅ | 8 |
| Порядок чтения задан | ✅ | 5 |
| Executive report создан | ✅ | 5 |


### 127. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 9 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_clusters.py` | кластеризует файлы по тематической близости |  |
| `improve_complexity.py` | оценка читаемости документов. |  |
| `improve_dedup.py` | находит дублирующиеся файлы и похожие абзацы. | `--threshold` |
| `improve_density.py` | карта плотности тем по всем документам. |  |
| `improve_heatmap.py` | тепловая карта тем по разделам и файлам. |  |
| `improve_priorities.py` | ранжирует файлы по важности через TF-IDF. |  |
| `improve_sentiment.py` | тональный анализ документов. |  |
| `improve_similar.py` | для каждого документа находит топ-3 похожих. |  |
| `improve_word_freq.py` | частотный анализ слов по разделам. |  |


### 128. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 6 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_citation_index.py` | индекс внешних URL по частоте цитирования. | `--domain`, `--min-citations` |
| `improve_cross_section.py` | граф концептов между секциями. | `--format`, `--min-secs`, `--top` |
| `improve_digest_auto.py` | автодайджест изменений за N дней. | `--days`, `--format`, `--since` |
| `improve_reading_time.py` | оценивает время чтения каждого документа. | `--section`, `--wpm` |
| `improve_topic_model.py` | тематическое моделирование без ML-зависимостей. | `--section`, `--top-words`, `--topics` |
| `improve_version_diff.py` | показывает содержательные изменения docs/ между коммитами. | `--from`, `--last`, `--to` |


### 129. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 4 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_ci_config.py` | генерирует GitHub Actions workflow для docs. | `--dry-run`, `--minimal` |
| `improve_dependabot.py` | мониторинг версий OSS-компонентов Svyazi 2.0. | `--check-pypi`, `--generate-config` |
| `improve_github_issues.py` | создаёт GitHub Issues из ACTION_ITEMS.md и TODO-блоков. | `--create`, `--dry-run`, `--label` |
| `improve_pre_commit.py` | генерирует .pre-commit-config.yaml для проекта. | `--dry-run`, `--install` |


### 130. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 4 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_abstract.py` | генерирует структурированный абстракт для каждого документа. | `--apply`, `--dry-run`, `--min-words`, `--section` |
| `improve_auto_linker.py` | автоматические внутренние ссылки в документах. | `--apply`, `--dry-run`, `--min-mentions`, `--section`, `--types` |
| `improve_auto_toc.py` | автоматически добавляет таблицу содержания (TOC) в файлы. | `--apply`, `--depth`, `--dry-run`, `--min-headings`, `--section` |
| `improve_gap_filler.py` | заполняет пустые секции найденным контентом (BM25). | `--apply`, `--dry-run`, `--mode`, `--section`, `--top` |


### 131. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 10 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_chunk_semantic.py` | семантическое чанкинг документов для RAG. | `--max-words`, `--min-words`, `--output`, `--section` |
| `improve_concept_graph.py` | граф концептов из базы знаний. | `--format`, `--min-weight`, `--section`, `--top-concepts` |
| `improve_contradiction_check.py` | поиск противоречивых утверждений в базе знаний. | `--min-confidence`, `--section` |
| `improve_keyword_index.py` | инвертированный индекс: слово → файлы. | `--min-df`, `--query`, `--section`, `--top` |
| `improve_named_entity_index.py` | индекс именованных сущностей из всей базы. | `--min-mentions`, `--section`, `--type` |
| `improve_paragraph_quality.py` | находит проблемные абзацы в документах. | `--section`, `--verbose` |
| `improve_passage_retrieval.py` | BM25-поиск на уровне абзацев. | `--context`, `--index`, `--min-words`, `--query`, `--section`, `--top` |
| `improve_text_segmenter.py` | разбивает большие файлы на логические части. | `--apply`, `--dry-run`, `--max-words`, `--part-size`, `--section` |
| `improve_timeline_events.py` | извлекает даты и события из базы знаний. | `--format`, `--from`, `--section`, `--to` |
| `improve_vocabulary_richness.py` | метрики богатства словаря документов. | `--section`, `--top`, `--window` |


### 132. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 7 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_confluence.py` | конвертирует docs/*.md в формат Confluence Wiki Markup. | `--dry-run`, `--section` |
| `improve_export_csv.py` | экспортирует метаданные всех docs/ в CSV. |  |
| `improve_export_html.py` | экспортирует все docs/ в единый HTML-сайт. |  |
| `improve_export_json.py` | экспортирует всю структуру docs/ в structured JSON. |  |
| `improve_export_report.py` | единый сводный отчёт по всей базе знаний. | `--no-projects`, `--sections`, `--title` |
| `improve_obsidian.py` | готовит docs/ для импорта в Obsidian. | `--dry-run`, `--in-place`, `--section` |
| `improve_rss.py` | генерирует RSS/Atom фид из истории git-коммитов. | `--base-url`, `--max-items` |


### 133. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 9 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_abbreviations.py` | словарь аббревиатур и сокращений из docs/. |  |
| `improve_action_items.py` | извлекает задачи, риски, решения и TODO из docs/. |  |
| `improve_concepts.py` | извлекает определения понятий прямо из текстов. |  |
| `improve_decisions.py` | извлекает ключевые выводы и решения из всех файлов. |  |
| `improve_entities.py` | извлечение именованных сущностей из docs/. |  |
| `improve_extract_code.py` | извлекает все code-блоки из docs/. |  |
| `improve_extract_tables.py` | извлекает все Markdown-таблицы из docs/ |  |
| `improve_kpi.py` | извлекает числовые KPI и метрики из docs/. |  |
| `improve_questions.py` | извлекает открытые вопросы из docs/. |  |


### 134. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 7 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_autofill.py` | заполняет шаблоны данными из уже сгенерированных скриптов. | `--dry-run` |
| `improve_badges.py` | генерирует SVG-бейджи для README. |  |
| `improve_faq.py` | строит FAQ из QA-паттернов в документах. |  |
| `improve_footnotes.py` | автоматически связывает технические термины с глоссарием. |  |
| `improve_see_also.py` | добавляет блок "See Also / Смотрите также" |  |
| `improve_templates.py` | генерирует шаблоны документов для каждого раздела. |  |
| `improve_word_cloud.py` | генерирует SVG word cloud из топ-слов репозитория. |  |


### 135. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 4 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_graph.py` | строит граф связей между проектами. |  |
| `improve_mindmap.py` | строит майндмап всего репозитория в формате Mermaid mindmap. |  |
| `improve_narrative.py` | строит нарративную линию проекта. |  |
| `improve_network.py` | анализ сети авторов и проектов. |  |


### 136. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 6 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_backlinks.py` | индекс обратных ссылок. |  |
| `improve_crossrefs.py` | строит карту перекрёстных ссылок между файлами. |  |
| `improve_glossary.py` | извлекает все проекты, авторов и URL из docs/, |  |
| `improve_index_update.py` | инкрементальное обновление search_index.json. |  |
| `improve_search_index.py` | строит полнотекстовый JSON-индекс всех docs/. |  |
| `improve_timeline.py` | извлекает даты и временные маркеры из всех docs/, |  |


### 137. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 10 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_empty_sections.py` | поиск и заполнение пустых секций. | `--fill`, `--min-content`, `--report`, `--section`, `--suggest` |
| `improve_faceted_search.py` | фасетный поиск по базе знаний. | `--after`, `--entity`, `--format`, `--min-words`, `--query`, `--section`, … |
| `improve_heading_audit.py` | аудит иерархии заголовков. | `--section`, `--verbose` |
| `improve_knowledge_map.py` | единый дашборд всей базы знаний. |  |
| `improve_language_split.py` | анализ языкового состава документов. | `--min-mix`, `--report`, `--section`, `--split` |
| `improve_passive_voice.py` | детектор пассивного залога и номинализаций (RU/EN). | `--section`, `--top`, `--verbose` |
| `improve_question_extractor.py` | извлечение вопросов, гипотез и TODO. | `--min-words`, `--section`, `--type` |
| `improve_reading_list.py` | персонализированный список чтения по теме. | `--format`, `--query`, `--section`, `--top` |
| `improve_similar_passages.py` | поиск похожих абзацев между файлами (TF-IDF cosine). | `--min-sim`, `--min-words`, `--section`, `--top` |
| `improve_textrank.py` | извлекательное резюме через TextRank (без LLM). | `--apply`, `--query`, `--section`, `--sentences` |


### 138. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 10 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_alerts.py` | добавляет GitHub Markdown callout-блоки в ключевые файлы. |  |
| `improve_broken_links.py` | проверяет внутренние ссылки в docs/. | `--dry-run`, `--fix` |
| `improve_consistency.py` | находит разные написания одного термина, |  |
| `improve_content_gaps.py` | находит темы, упомянутые в docs/, но без собственного документа. | `--min-mentions`, `--section` |
| `improve_metrics.py` | метрики качества документации. |  |
| `improve_missing.py` | находит темы/проекты упомянутые в документах |  |
| `improve_orphans.py` | находит документы без входящих ссылок (orphan docs). |  |
| `improve_readability_v2.py` | индекс читаемости текстов. | `--section` |
| `improve_spellcheck.py` | проверка орфографии в docs/. | `--fix`, `--section` |
| `improve_validate.py` | валидация структуры репозитория. |  |


### 139. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 19 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_benchmark.py` | замеряет и записывает время выполнения скриптов. | `--group`, `--report`, `--script` |
| `improve_changelog.py` | генерирует CHANGELOG из git-истории репозитория. |  |
| `improve_compare.py` | сравнивает текущее состояние docs/ с предыдущим коммитом. |  |
| `improve_contact_priority.py` | ранжирует авторов по приоритету для контакта. |  |
| `improve_contacts.py` | извлекает email, Telegram, GitHub, Habr-ники |  |
| `improve_cost.py` | оценка стоимости разработки MVP. |  |
| `improve_coverage.py` | матрица покрытия: какие файлы имеют summary, теги, TOC, crossrefs, статус. | `--section` |
| `improve_digest.py` | дайджест недавних изменений репозитория. |  |
| `improve_health.py` | дашборд здоровья репозитория. |  |
| `improve_progress.py` | трекер прогресса MVP-проекта. |  |
| `improve_progress_sync.py` | синхронизирует PROGRESS.md с реальным состоянием файлов. | `--dry-run` |
| `improve_qa.py` | генерирует Q&A листы для каждого раздела docs/. |  |
| `improve_reading_order.py` | строит рекомендуемый порядок чтения документов |  |
| `improve_report.py` | итоговый executive report о состоянии репозитория. |  |
| `improve_schedule.py` | строит расписание проекта из ACTION_ITEMS и временных маркеров. |  |
| `improve_scoring.py` | система оценки готовности проекта к запуску (Go/No-Go). |  |
| `improve_sitemap.py` | генерирует навигационную карту репозитория. |  |
| `improve_staleness.py` | находит документы которые давно не обновлялись или неполные. | `--days`, `--no-git` |
| `improve_stats.py` | детальная статистика по каждому разделу docs/. |  |


### 140. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 6 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_autocorrect.py` | применяет исправления из CONSISTENCY.md: | `--dry-run` |
| `improve_merge_short.py` | сливает слишком короткие файлы с предыдущим соседом. |  |
| `improve_readmes.py` | создаёт README.md для каждой подпапки docs/. |  |
| `improve_summaries.py` | добавляет краткую аннотацию в начало каждого файла. |  |
| `improve_tags.py` | тегирует каждый файл по темам, создаёт docs/TAGS.md |  |
| `improve_toc.py` | добавляет Table of Contents в начало файлов длиннее 500 слов. |  |


### 141. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 8 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_compare_docs.py` | сравнивает два документа: общее, различия, пересечения. | `--a`, `--b`, `--batch`, `--out`, `--section`, `--top` |
| `improve_crosslink_all.py` | прописывает обратные ссылки (backlinks) во все файлы. | `--apply`, `--dry-run`, `--keywords`, `--min-refs` |
| `improve_duplicate_across.py` | поиск похожих текстов между репозиториями/папками. | `--internal`, `--other-dir`, `--other-repo`, `--section`, `--threshold` |
| `improve_merge_by_topic.py` | склеивает файлы-фрагменты одной темы в единый документ. | `--apply`, `--dry-run`, `--min-group`, `--section`, `--threshold` |
| `improve_outline.py` | строит иерархический outline всей базы знаний. | `--depth`, `--format`, `--section` |
| `improve_reclassify.py` | раскладывает файлы по подпапкам на основе TF-IDF тематики. | `--apply`, `--dry-run`, `--section`, `--topics` |
| `improve_source_map.py` | строит карту происхождения текстов. | `--authors`, `--format`, `--section`, `--show-imported` |
| `improve_subtopic_fill.py` | дополняет файлы-заглушки контентом из базы знаний. | `--apply`, `--dry-run`, `--min-words`, `--section` |


### 142. analysis (9)
_Файл: `docs/SCRIPTS_CATALOG.md` | 3 колонок, 27 строк_

| Скрипт | Описание | Флаги |
|--------|----------|-------|
| `improve_changelog_auto.py` | автоматический changelog из git-истории. |  |
| `improve_component_matrix.py` | матрица совместимости и возможностей компонентов. |  |
| `improve_contact_status.py` | обновляет статус контакта в docs/contacts/<slug>.md. | `--agreed`, `--author`, `--list`, `--messaged`, `--note`, `--replied`, … |
| `improve_dependency_map.py` | карта зависимостей: скрипты → выходные файлы. |  |
| `improve_digest_weekly.py` | еженедельный дайджест изменений репозитория. |  |
| `improve_epub.py` | собирает docs/ в EPUB через pandoc. | `--check`, `--output`, `--section`, `--title` |
| `improve_external_compare.py` | сравнивает документы базы с внешними источниками. | `--auto`, `--file`, `--limit`, `--query`, `--section`, `--url` |
| `improve_index_master.py` | главный навигационный хаб docs/. |  |
| `improve_kpi_snapshot.py` | исторические снапшоты ключевых метрик. |  |
| `improve_link_preview.py` | проверяет внешние ссылки в docs/ и кэширует их статус. | `--refresh`, `--section`, `--timeout` |
| `improve_llm_contact.py` | генерирует персонализированное первое сообщение автору через LLM. | `--all`, `--author`, `--dry-run` |
| `improve_llm_enrich.py` | семантическое обогащение проектных файлов через Claude API. | `--dry-run`, `--file`, `--force`, `--model`, `--section` |
| `improve_llm_gaps.py` | семантический поиск пробелов через Claude API. |  |
| `improve_llm_qa.py` | ответы на вопросы по всей базе знаний Lorenzo через Claude API. | `--batch`, `--clear-cache`, `--dry-run`, `--no-cache`, `--question`, `--save` |
| `improve_llm_summary.py` | каскадная суммаризация больших документов через Claude API. | `--dry-run`, `--file`, `--section` |
| `improve_mcp_dashboard.py` | статистика вызовов MCP-серверов. |  |
| `improve_mcp_test.py` | smoke-тесты для всех MCP-серверов. |  |
| `improve_onboarding.py` | руководство для новых участников проекта. |  |
| `improve_risk_register.py` | реестр рисков проекта Svyazi 2.0. |  |
| `improve_run_all.py` | мастер-скрипт для запуска всех improve_*.py. | `--changed`, `--dry-run`, `--fast`, `--group`, `--only`, `--parallel`, … |
| `improve_task_codegen.py` | генератор слоёв (скилл / MCP-tool / index) из манифестов tasks/*.task.yaml. | `--dry-run`, `--list`, `--task`, `--validate` |
| `improve_tech_radar.py` | tech radar для технологий проекта Svyazi 2.0. |  |
| `improve_template_init.py` | инициализация нового документа из шаблона. | `--list`, `--show`, `--slug`, `--type`, `--vars` |
| `improve_template_migrate.py` | миграции frontmatter при изменении схемы шаблона. | `--all`, `--apply`, `--dry-run`, `--template` |
| `improve_validate_templates.py` | валидация документов по схемам шаблонов. | `--file`, `--report`, `--section`, `--strict` |
| `improve_watch.py` | следит за изменениями в docs/ и перезапускает нужные скрипты. | `--changed`, `--fast`, `--group`, `--interval` |
| `improve_watcher.py` | автономный агент-наблюдатель (Ступень 6). | `--once` |


### 143. Результаты поиска
_Файл: `docs/SEARCH_RESULTS.md` | 4 колонок, 5 строк_

| # | Файл | Оценка | Дата |
|---|------|--------|------|
| 1 | `QA.md` | 5.0 | 2026-04-29 |
| 2 | `04-ensembles-overview.md` | 5.0 | 2026-04-29 |
| 3 | `COST.md` | 5.0 | 2026-04-29 |
| 4 | `06-безопасность-приватность-и-бюджетный-роутинг.md` | 5.0 | 2026-04-29 |
| 5 | `TABLES.md` | 5.0 | 2026-04-29 |


### 144. Тональность по разделам
_Файл: `docs/SENTIMENT.md` | 6 колонок, 16 строк_

| Раздел | Оптимизм | Скептицизм | Срочность | Неопределённость | Тон |
|--------|----------|------------|-----------|-----------------|-----|
| **01-svyazi** | 2.6‰ | 8.0‰ | 3.6‰ | 0.5‰ | 🔴 скептичный |
| **02-anthropic-vacancies** | 1.8‰ | 7.1‰ | 2.1‰ | 1.5‰ | 🔴 скептичный |
| **03-technology-combinations** | 4.0‰ | 2.5‰ | 0.7‰ | 0.4‰ | ⚪ нейтральный |
| **04-ai-collaborations** | 2.4‰ | 4.8‰ | 1.4‰ | 0.8‰ | 🔴 скептичный |
| **05-habr-projects** | 3.9‰ | 1.4‰ | 0.7‰ | 1.4‰ | 🟢 оптимистичный |
| **ai-collaborations** | 0.4‰ | 6.5‰ | 1.0‰ | 1.0‰ | 🔴 скептичный |
| **anthropic-vacancies** | 2.1‰ | 3.9‰ | 0.8‰ | 1.3‰ | 🔴 скептичный |
| **contacts** | 0.0‰ | 0.0‰ | 0.0‰ | 0.0‰ | ⚪ нейтральный |
| **glossary** | 0.4‰ | 0.4‰ | 0.0‰ | 0.4‰ | ⚪ нейтральный |
| **habr-unique-projects** | 10.1‰ | 0.9‰ | 1.1‰ | 1.0‰ | 🟢 оптимистичный |
| **lorenzo-agent** | 1.8‰ | 3.4‰ | 1.2‰ | 1.9‰ | 🔴 скептичный |
| **nautilus** | 1.9‰ | 5.7‰ | 1.8‰ | 1.5‰ | 🔴 скептичный |
| **root** | 0.7‰ | 22.9‰ | 1.0‰ | 1.2‰ | 🔴 скептичный |
| **svyazi-2-0** | 1.9‰ | 7.3‰ | 1.6‰ | 0.7‰ | 🔴 скептичный |
| **technology-combinations** | 5.1‰ | 1.3‰ | 0.5‰ | 0.2‰ | 🟢 оптимистичный |
| **templates** | 0.0‰ | 8.8‰ | 0.8‰ | 0.2‰ | 🔴 скептичный |


### 145. Самые оптимистичные документы
_Файл: `docs/SENTIMENT.md` | 3 колонок, 10 строк_

| Документ | Оптимизм‰ | Тон |
|----------|----------|-----|
| `123-portal-mcp-py` | 34.2 | 🟢 оптимистичный |
| `00-question-habr-examples` | 29.3 | 🟢 оптимистичный |
| `01-yogi-metaphor` | 23.2 | 🟢 оптимистичный |
| `05-hw-nl2workflow` | 22.0 | 🟢 оптимистичный |
| `19-7-portalentry-structure` | 21.7 | 🟠 срочный |
| `04-claude-subagents-patterns` | 21.1 | 🟢 оптимистичный |
| `02-what-was-missing-in-paper-6` | 18.6 | 🟢 оптимистичный |
| `02-vshe-scientific-networking` | 18.2 | 🟢 оптимистичный |
| `24-mega-integration-full-stack` | 16.8 | 🟢 оптимистичный |
| `03-brainbox-multi-ai-hub` | 16.6 | 🟢 оптимистичный |


### 146. Самые скептичные / риск-ориентированные
_Файл: `docs/SENTIMENT.md` | 3 колонок, 10 строк_

| Документ | Скептицизм‰ | Тон |
|----------|------------|-----|
| `HEADING_AUDIT` | 286.6 | 🔴 скептичный |
| `PARAGRAPH_QUALITY` | 237.1 | 🔴 скептичный |
| `risk-entry` | 102.3 | 🔴 скептичный |
| `177-8-risks-and-mitigations` | 90.3 | 🔴 скептичный |
| `198-8-риски-и-меры-противодействия` | 86.6 | 🔴 скептичный |
| `08-riski-mery` | 61.1 | 🔴 скептичный |
| `08-risk-analysis` | 51.3 | 🔴 скептичный |
| `162-8-risk-analysis` | 51.1 | 🔴 скептичный |
| `privacy` | 48.4 | 🔴 скептичный |
| `10-risks` | 45.1 | 🔴 скептичный |


### 147. Распределение тональности
_Файл: `docs/SENTIMENT.md` | 2 колонок, 5 строк_

| Тон | Файлов |
|-----|--------|
| 🔴 скептичный | 505 |
| ⚪ нейтральный | 281 |
| 🟢 оптимистичный | 136 |
| 🟠 срочный | 78 |
| 🟡 неопределённый | 33 |


### 148. Топ-20 самых похожих пар
_Файл: `docs/SIMILAR.md` | 3 колонок, 20 строк_

| Сходство | Файл A | Файл B |
|----------|--------|--------|
| 1.000 | `273-infrastructure-for-ai-collaborative-intellectual-w.md` | `151-open-knowledge-work-foundation-md.md` |
| 0.965 | `03-карта-найденных-проектов-и-паттернов.md` | `03-component-catalog.md` |
| 0.957 | `09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | `09-architectural-gaps.md` |
| 0.955 | `05-план-прототипа-и-возможные-контакты.md` | `07-mvp-planning.md` |
| 0.954 | `06-безопасность-приватность-и-бюджетный-роутинг.md` | `06-security-privacy.md` |
| 0.948 | `13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | `13-contacts.md` |
| 0.945 | `12-дорожная-карта-прототипа-следующей-итерации.md` | `12-roadmap.md` |
| 0.939 | `11-интеграционный-контракт-который-стоит-зафиксироват.md` | `11-integration-contracts.md` |
| 0.927 | `94-19-adr-001-federation-over-merging.md` | `26-14-adr-001-federation-over-merging.md` |
| 0.905 | `zodigancode.md` | `cutcode.md` |
| 0.905 | `mixaill76.md` | `dmitriila.md` |
| 0.901 | `07-выводы.md` | `08-conclusions.md` |
| 0.881 | `zodigancode.md` | `vladspace.md` |
| 0.881 | `vladspace.md` | `tagir-analyzes.md` |
| 0.881 | `vladspace.md` | `mixaill76.md` |
| 0.881 | `dmitriila.md` | `vladspace.md` |
| 0.881 | `cutcode.md` | `vladspace.md` |
| 0.881 | `251-ai-support-through-configurable-specialist-ensembl.md` | `209-a-typology-of-ai-agents-on-the-principal-side-and-.md` |
| 0.875 | `04-приоритетные-ансамбли.md` | `04-ensembles-overview.md` |
| 0.874 | `10-новые-ансамбли-следующего-шага.md` | `10-second-order-ensembles.md` |


### 149. Мета-документы
_Файл: `docs/SITEMAP.md` | 3 колонок, 196 строк_

| Документ | Описание | Слов |
|----------|----------|------|
| [ABBREVIATIONS.md](docs/ABBREVIATIONS.md) | — | 1532 |
| [ACTION_ITEMS.md](docs/ACTION_ITEMS.md) | Задачи и риски (490) | 7697 |
| [ALERTS.md](docs/ALERTS.md) | — | 79 |
| [AUTHORS.md](docs/AUTHORS.md) | Авторы и контакты | 158 |
| [AUTOFILLED.md](docs/AUTOFILLED.md) | — | 102 |
| [BACKLINKS.md](docs/BACKLINKS.md) | — | 397 |
| [BROKEN_LINKS.md](docs/BROKEN_LINKS.md) | Сломанные ссылки (26) | 790 |
| [CHANGELOG.md](docs/CHANGELOG.md) | История изменений | 1239 |
| [CHANGELOG_AUTO.md](docs/CHANGELOG_AUTO.md) | — | 353 |
| [CITATION_INDEX.md](docs/CITATION_INDEX.md) | — | 935 |
| [CLUSTERS.md](docs/CLUSTERS.md) | Кластеры (384 → 120 групп) | 1380 |
| [CODE_BLOCKS.md](docs/CODE_BLOCKS.md) | — | 4618 |
| [COMPARE.md](docs/COMPARE.md) | Сравнение с предыдущим коммитом | 477 |
| [COMPLEXITY.md](docs/COMPLEXITY.md) | Оценка читаемости | 605 |
| [COMPONENT_MATRIX.md](docs/COMPONENT_MATRIX.md) | — | 887 |
| [CONCEPTS.md](docs/CONCEPTS.md) | Глоссарий понятий (888) | 13165 |
| [CONCEPT_GRAPH.md](docs/CONCEPT_GRAPH.md) | — | 741 |
| [CONSISTENCY.md](docs/CONSISTENCY.md) | — | 375 |
| [CONTACTS.md](docs/CONTACTS.md) | Контакты (15 авторов) | 547 |
| [CONTACT_PRIORITY.md](docs/CONTACT_PRIORITY.md) | — | 524 |
| [CONTENT_GAPS.md](docs/CONTENT_GAPS.md) | — | 899 |
| [CONTRADICTIONS.md](docs/CONTRADICTIONS.md) | — | 1949 |
| [COST.md](docs/COST.md) | — | 731 |
| [COVERAGE.md](docs/COVERAGE.md) | — | 860 |
| [CROSSREFS.md](docs/CROSSREFS.md) | Перекрёстные ссылки проектов | 655 |
| [CROSS_SECTION.md](docs/CROSS_SECTION.md) | — | 1256 |
| [DECISIONS.md](docs/DECISIONS.md) | Ключевые решения (150) | 2452 |
| [DENSITY.md](docs/DENSITY.md) | Карта плотности тем | 650 |
| [DEPENDABOT.md](docs/DEPENDABOT.md) | — | 173 |
| [DEPENDENCY_MAP.md](docs/DEPENDENCY_MAP.md) | — | 558 |
| [DIGEST.md](docs/DIGEST.md) | — | 487 |
| [DIGEST_AUTO.md](docs/DIGEST_AUTO.md) | — | 461 |
| [DIGEST_WEEKLY.md](docs/DIGEST_WEEKLY.md) | — | 213 |
| [DUPLICATES.md](docs/DUPLICATES.md) | — | 2750 |
| [EMPTY_SECTIONS.md](docs/EMPTY_SECTIONS.md) | — | 7416 |
| [ENTITIES.md](docs/ENTITIES.md) | Именованные сущности | 742 |
| [FAQ.md](docs/FAQ.md) | — | 892 |
| [FOOTNOTES.md](docs/FOOTNOTES.md) | — | 275 |
| [GITHUB_ISSUES.md](docs/GITHUB_ISSUES.md) | — | 1255 |
| [GLOSSARY.md](docs/GLOSSARY.md) | Глоссарий проектов (33 записи) | 204 |
| [GRAPH.md](docs/GRAPH.md) | Граф связей проектов | 2658 |
| [HEADING_AUDIT.md](docs/HEADING_AUDIT.md) | — | 17278 |
| [HEALTH.md](docs/HEALTH.md) | Дашборд здоровья (75/100) | 214 |
| [HEATMAP.md](docs/HEATMAP.md) | — | 536 |
| [INDEX.md](docs/INDEX.md) | — | 616 |
| [KEYWORD_INDEX.md](docs/KEYWORD_INDEX.md) | — | 1138 |
| [KNOWLEDGE_MAP.md](docs/KNOWLEDGE_MAP.md) | — | 568 |
| [KPI.md](docs/KPI.md) | Числовые KPI (737 показателей) | 2388 |
| [KPI_HISTORY.md](docs/KPI_HISTORY.md) | — | 106 |
| [LANGUAGE_STATS.md](docs/LANGUAGE_STATS.md) | — | 3930 |
| [LINKS.md](docs/LINKS.md) | Внешние ссылки | 1029 |
| [LLM_SUMMARIES.md](docs/LLM_SUMMARIES.md) | — | 177 |
| [METRICS.md](docs/METRICS.md) | — | 455 |
| [MINDMAP.md](docs/MINDMAP.md) | Майндмап в Mermaid | 242 |
| [MISSING.md](docs/MISSING.md) | Пробелы знаний | 434 |
| [NAMED_ENTITIES.md](docs/NAMED_ENTITIES.md) | — | 1783 |
| [NARRATIVE.md](docs/NARRATIVE.md) | — | 1043 |
| [NETWORK.md](docs/NETWORK.md) | — | 413 |
| [ONBOARDING.md](docs/ONBOARDING.md) | — | 552 |
| [ORPHANS.md](docs/ORPHANS.md) | — | 105 |
| [OUTLINE.md](docs/OUTLINE.md) | — | 34491 |
| [PARAGRAPH_QUALITY.md](docs/PARAGRAPH_QUALITY.md) | — | 14229 |
| [PASSIVE_VOICE.md](docs/PASSIVE_VOICE.md) | — | 507 |
| [PRIORITIES.md](docs/PRIORITIES.md) | Приоритеты (TF-IDF) | 3029 |
| [PROGRESS.md](docs/PROGRESS.md) | — | 292 |
| [QA.md](docs/01-svyazi/QA.md) | Вопросы и ответы | 182 |
| [QA.md](docs/02-anthropic-vacancies/QA.md) | Вопросы и ответы | 323 |
| [QA.md](docs/03-technology-combinations/QA.md) | Вопросы и ответы | 156 |
| [QA.md](docs/04-ai-collaborations/QA.md) | Вопросы и ответы | 226 |
| [QA.md](docs/05-habr-projects/QA.md) | Вопросы и ответы | 138 |
| [QA.md](docs/QA.md) | Вопросы и ответы | 1290 |
| [QA.md](docs/anthropic-vacancies/QA.md) | Вопросы и ответы | 84 |
| [QA.md](docs/lorenzo-agent/QA.md) | Вопросы и ответы | 206 |
| [QUESTIONS.md](docs/QUESTIONS.md) | Открытые вопросы (484) | 1838 |
| [READABILITY.md](docs/READABILITY.md) | — | 17606 |
| [READING_LIST.md](docs/READING_LIST.md) | — | 232 |
| [READING_ORDER.md](docs/READING_ORDER.md) | Рекомендуемый порядок чтения | 5947 |
| [READING_TIME.md](docs/READING_TIME.md) | — | 12186 |
| [README.md](docs/01-svyazi/README.md) | Главная страница и навигация | 98 |
| [README.md](docs/02-anthropic-vacancies/README.md) | Главная страница и навигация | 2222 |
| [README.md](docs/03-technology-combinations/README.md) | Главная страница и навигация | 46 |
| [README.md](docs/04-ai-collaborations/README.md) | Главная страница и навигация | 103 |
| [README.md](docs/05-habr-projects/README.md) | Главная страница и навигация | 39 |
| [README.md](docs/05-habr-projects/knowledge/README.md) | Главная страница и навигация | 13 |
| [README.md](docs/05-habr-projects/memory/README.md) | Главная страница и навигация | 24 |
| [README.md](docs/README.md) | Главная страница и навигация | 743 |
| [README.md](docs/ai-collaborations/README.md) | Главная страница и навигация | 39 |
| [README.md](docs/ai-collaborations/candidates/README.md) | Главная страница и навигация | 23 |
| [README.md](docs/ai-collaborations/channels/README.md) | Главная страница и навигация | 25 |
| [README.md](docs/ai-collaborations/continuation/README.md) | Главная страница и навигация | 61 |
| [README.md](docs/ai-collaborations/ensembles/README.md) | Главная страница и навигация | 60 |
| [README.md](docs/ai-collaborations/fast-tracks/README.md) | Главная страница и навигация | 311 |
| [README.md](docs/ai-collaborations/strategy/README.md) | Главная страница и навигация | 32 |
| [README.md](docs/anthropic-vacancies/README.md) | Главная страница и навигация | 72 |
| [README.md](docs/anthropic-vacancies/ai-managed-virtual-company/README.md) | Главная страница и навигация | 69 |
| [README.md](docs/anthropic-vacancies/beneficial-deployments-concept/README.md) | Главная страница и навигация | 77 |
| [README.md](docs/anthropic-vacancies/clusters/README.md) | Главная страница и навигация | 103 |
| [README.md](docs/anthropic-vacancies/extra-collaborator-findings/README.md) | Главная страница и навигация | 46 |
| [README.md](docs/anthropic-vacancies/hermes-comparison/README.md) | Главная страница и навигация | 88 |
| [README.md](docs/anthropic-vacancies/mmorpg-for-programmers/README.md) | Главная страница и навигация | 41 |
| [README.md](docs/anthropic-vacancies/nautilus-pro2-analysis/README.md) | Главная страница и навигация | 30 |
| [README.md](docs/anthropic-vacancies/nautilus-vs-camel/README.md) | Главная страница и навигация | 40 |
| [README.md](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/README.md) | Главная страница и навигация | 53 |
| [README.md](docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md) | Главная страница и навигация | 35 |
| [README.md](docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md) | Главная страница и навигация | 35 |
| [README.md](docs/anthropic-vacancies/profile-mapping/README.md) | Главная страница и навигация | 159 |
| [README.md](docs/autofilled/README.md) | Главная страница и навигация | 18 |
| [README.md](docs/autofilled/components/README.md) | Главная страница и навигация | 66 |
| [README.md](docs/badges/README.md) | Главная страница и навигация | 44 |
| [README.md](docs/contacts/README.md) | Главная страница и навигация | 90 |
| [README.md](docs/glossary/README.md) | Главная страница и навигация | 24 |
| [README.md](docs/habr-unique-projects/README.md) | Главная страница и навигация | 234 |
| [README.md](docs/habr-unique-projects/analogues/README.md) | Главная страница и навигация | 18 |
| [README.md](docs/habr-unique-projects/deep-pairs/README.md) | Главная страница и навигация | 54 |
| [README.md](docs/habr-unique-projects/evaluation/README.md) | Главная страница и навигация | 28 |
| [README.md](docs/habr-unique-projects/extra-examples/README.md) | Главная страница и навигация | 82 |
| [README.md](docs/habr-unique-projects/final-ensembles/README.md) | Главная страница и навигация | 30 |
| [README.md](docs/habr-unique-projects/hardware-pairs/README.md) | Главная страница и навигация | 48 |
| [README.md](docs/habr-unique-projects/key-findings/README.md) | Главная страница и навигация | 42 |
| [README.md](docs/habr-unique-projects/search-strategy/README.md) | Главная страница и навигация | 25 |
| [README.md](docs/habr-unique-projects/software-pairs/README.md) | Главная страница и навигация | 42 |
| [README.md](docs/lorenzo-agent/README.md) | Главная страница и навигация | 163 |
| [README.md](docs/lorenzo-agent/naming/README.md) | Главная страница и навигация | 28 |
| [README.md](docs/lorenzo-agent/operationalized/README.md) | Главная страница и навигация | 45 |
| [README.md](docs/lorenzo-agent/phased-deployment/README.md) | Главная страница и навигация | 59 |
| [README.md](docs/lorenzo-agent/scenarios/README.md) | Главная страница и навигация | 18 |
| [README.md](docs/lorenzo-agent/specification/README.md) | Главная страница и навигация | 77 |
| [README.md](docs/nautilus/README.md) | Главная страница и навигация | 524 |
| [README.md](docs/nautilus/community-discussions/README.md) | Главная страница и навигация | 90 |
| [README.md](docs/nautilus/community-discussions/agent-changes-reality/README.md) | Главная страница и навигация | 17 |
| [README.md](docs/nautilus/community-discussions/habr-article-1-reaction/README.md) | Главная страница и навигация | 17 |
| [README.md](docs/nautilus/community-discussions/habr-article-2-reaction/README.md) | Главная страница и навигация | 17 |
| [README.md](docs/nautilus/community-discussions/practical-observations/README.md) | Главная страница и навигация | 17 |
| [README.md](docs/nautilus/community-discussions/voiceless-contributors/README.md) | Главная страница и навигация | 17 |
| [README.md](docs/nautilus/composite-skills-agents/README.md) | Главная страница и навигация | 78 |
| [README.md](docs/nautilus/composite-skills-agents-companion-mentors/README.md) | Главная страница и навигация | 27 |
| [README.md](docs/nautilus/double-triangle-architecture/README.md) | Главная страница и навигация | 71 |
| [README.md](docs/nautilus/infrastructure-layer-b-en/README.md) | Главная страница и навигация | 89 |
| [README.md](docs/nautilus/infrastructure-layer-b-ru/README.md) | Главная страница и навигация | 80 |
| [README.md](docs/nautilus/ingit-cowork-en/README.md) | Главная страница и навигация | 64 |
| [README.md](docs/nautilus/ingit-cowork-ru/README.md) | Главная страница и навигация | 62 |
| [README.md](docs/nautilus/innovation-transitions/README.md) | Главная страница и навигация | 16 |
| [README.md](docs/nautilus/multi-tier-architecture/README.md) | Главная страница и навигация | 17 |
| [README.md](docs/nautilus/npp-humanitarian-extension/README.md) | Главная страница и навигация | 41 |
| [README.md](docs/nautilus/npp-v1-0/README.md) | Главная страница и навигация | 116 |
| [README.md](docs/nautilus/npp-v1-1/README.md) | Главная страница и навигация | 138 |
| [README.md](docs/nautilus/okwf-concept/README.md) | Главная страница и навигация | 69 |
| [README.md](docs/nautilus/privacy-federation/README.md) | Главная страница и навигация | 35 |
| [README.md](docs/nautilus/professional-colleague-agents-en/README.md) | Главная страница и навигация | 82 |
| [README.md](docs/nautilus/professional-colleague-agents-ru/README.md) | Главная страница и навигация | 78 |
| [README.md](docs/nautilus/representative-agent-layer-en/README.md) | Главная страница и навигация | 81 |
| [README.md](docs/nautilus/representative-agent-layer-ru/README.md) | Главная страница и навигация | 77 |
| [README.md](docs/nautilus/review-methodology/README.md) | Главная страница и навигация | 97 |
| [README.md](docs/nautilus/supply-demand/README.md) | Главная страница и навигация | 17 |
| [README.md](docs/nautilus/transmission-box/README.md) | Главная страница и навигация | 16 |
| [README.md](docs/svyazi-2-0/README.md) | Главная страница и навигация | 158 |
| [README.md](docs/svyazi-2-0/architecture/README.md) | Главная страница и навигация | 46 |
| [README.md](docs/svyazi-2-0/components/README.md) | Главная страница и навигация | 120 |
| [README.md](docs/svyazi-2-0/ensembles/README.md) | Главная страница и навигация | 54 |
| [README.md](docs/svyazi-2-0/limitations/README.md) | Главная страница и навигация | 22 |
| [README.md](docs/svyazi-2-0/outreach/README.md) | Главная страница и навигация | 22 |
| [README.md](docs/svyazi-2-0/overview/README.md) | Главная страница и навигация | 27 |
| [README.md](docs/svyazi-2-0/prototype/README.md) | Главная страница и навигация | 21 |
| [README.md](docs/svyazi-2-0/security/README.md) | Главная страница и навигация | 21 |
| [README.md](docs/technology-combinations/README.md) | Главная страница и навигация | 155 |
| [README.md](docs/technology-combinations/combinations/README.md) | Главная страница и навигация | 214 |
| [README.md](docs/technology-combinations/mega-stacks/README.md) | Главная страница и навигация | 29 |
| [README.md](docs/technology-combinations/properties/README.md) | Главная страница и навигация | 68 |
| [README.md](docs/technology-combinations/research-reports/README.md) | Главная страница и навигация | 18 |
| [README.md](docs/technology-combinations/synthesis-tables/README.md) | Главная страница и навигация | 42 |
| [README.md](docs/templates/README.md) | Главная страница и навигация | 90 |
| [REPORT.md](docs/REPORT.md) | — | 932 |
| [RISK_REGISTER.md](docs/RISK_REGISTER.md) | — | 944 |
| [SCHEDULE.md](docs/SCHEDULE.md) | — | 444 |
| [SCORING.md](docs/SCORING.md) | — | 626 |
| [SEARCH.md](docs/SEARCH.md) | Поисковый индекс | 4660 |
| [SEARCH_RESULTS.md](docs/SEARCH_RESULTS.md) | — | 91 |
| [SEE_ALSO.md](docs/SEE_ALSO.md) | — | 217 |
| [SENTIMENT.md](docs/SENTIMENT.md) | — | 487 |
| [SIMILAR.md](docs/SIMILAR.md) | Похожие документы (937 пар) | 341 |
| [SIMILAR_PASSAGES.md](docs/SIMILAR_PASSAGES.md) | — | 1931 |
| [SOURCE_MAP.md](docs/SOURCE_MAP.md) | — | 6167 |
| [SPELLCHECK.md](docs/SPELLCHECK.md) | — | 220 |
| [STALENESS.md](docs/STALENESS.md) | — | 600 |
| [STATS.md](docs/STATS.md) | Детальная статистика | 630 |
| [SUMMARIES.md](docs/SUMMARIES.md) | — | 3910 |
| [TABLES.md](docs/TABLES.md) | — | 99622 |
| [TAGS.md](docs/TAGS.md) | Теги (316 файлов, 12 тем) | 544 |
| [TECH_RADAR.md](docs/TECH_RADAR.md) | — | 612 |
| [TIMELINE.md](docs/TIMELINE.md) | Временная шкала (800 маркеров) | 4272 |
| [VALIDATION.md](docs/VALIDATION.md) | — | 595 |
| [VERSION_DIFF.md](docs/VERSION_DIFF.md) | — | 34 |
| [VOCABULARY.md](docs/VOCABULARY.md) | — | 1089 |
| [WORD_CLOUD.md](docs/WORD_CLOUD.md) | — | 212 |
| [WORD_FREQ.md](docs/WORD_FREQ.md) | Частотный анализ слов | 2815 |
| [reading-paths.md](docs/reading-paths.md) | — | 627 |


### 150. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 14 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Продолжение исследования для Svyazi 2.0](docs/01-svyazi/00-intro-part2.md) | 6 |
| 2 | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 726 |
| 3 | [Методика и рамка отбора проектов](docs/01-svyazi/02-methodology.md) | 480 |
| 4 | [03-component-catalog](docs/01-svyazi/03-component-catalog.md) | 1383 |
| 5 | [04-ensembles-overview](docs/01-svyazi/04-ensembles-overview.md) | 1288 |
| 6 | [06-security-privacy](docs/01-svyazi/06-security-privacy.md) | 823 |
| 7 | [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md) | 1063 |
| 8 | [08-conclusions](docs/01-svyazi/08-conclusions.md) | 380 |
| 9 | [09-architectural-gaps](docs/01-svyazi/09-architectural-gaps.md) | 758 |
| 10 | [10-second-order-ensembles](docs/01-svyazi/10-second-order-ensembles.md) | 908 |
| 11 | [11-integration-contracts](docs/01-svyazi/11-integration-contracts.md) | 737 |
| 12 | [12-roadmap](docs/01-svyazi/12-roadmap.md) | 722 |
| 13 | [13-contacts](docs/01-svyazi/13-contacts.md) | 806 |
| 14 | [14-limitations](docs/01-svyazi/14-limitations.md) | 638 |


### 151. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 51 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Введение](docs/02-anthropic-vacancies/00-intro.md) | 8934 |
| 2 | [Интегральный анализ профиля svend4](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | 19144 |
| 3 | [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md) | 3207 |
| 4 | [PORTAL-PROTOCOL.md](docs/02-anthropic-vacancies/03-portal-protocol-md.md) | 75 |
| 5 | [Abstract](docs/02-anthropic-vacancies/04-abstract.md) | 126 |
| 6 | [0. Status of This Document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md) | 101 |
| 7 | [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md) | 383 |
| 8 | [2. Terminology](docs/02-anthropic-vacancies/07-2-terminology.md) | 302 |
| 9 | [3. Registry (`nautilus.json`)](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) | 403 |
| 10 | [4. Passport (`passport.md`)](docs/02-anthropic-vacancies/09-4-passport-passport-md.md) | 144 |
| 11 | [Доступ к данным](docs/02-anthropic-vacancies/102-доступ-к-данным.md) | 23 |
| 12 | [Appendix B: Change Log](docs/02-anthropic-vacancies/103-appendix-b-change-log.md) | 170 |
| 13 | [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) | 955 |
| 14 | [REVIEW_METHODOLOGY.md](docs/02-anthropic-vacancies/105-review-methodology-md.md) | 74 |
| 15 | [TL;DR](docs/02-anthropic-vacancies/106-tl-dr.md) | 128 |
| 16 | [1. Контекст и мотивация](docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md) | 455 |
| 17 | [2. Формальный workflow](docs/02-anthropic-vacancies/108-2-формальный-workflow.md) | 463 |
| 18 | [3. Принципы консолидации (Фаза C)](docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md) | 560 |
| 19 | [Вопрос: fallback-ratio как критический или осмысле](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) | 338 |
| 20 | [4. Условия применимости](docs/02-anthropic-vacancies/111-4-условия-применимости.md) | 272 |
| 21 | [5. Связь с существующими методологиями](docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) | 389 |
| 22 | [6. Почему это валидный паттерн для AI-assisted wor](docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) | 150 |
| 23 | [7. Реализация в проекте Nautilus](docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md) | 309 |
| 24 | [8. Ограничения и открытые вопросы](docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md) | 447 |
| 25 | [9. Checklist применения методологии](docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md) | 399 |
| 26 | [10. Конкретный план применения к текущим документа](docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md) | 315 |
| 27 | [Appendix A: Шаблон для header warning](docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md) | 175 |
| 28 | [Appendix B: Примеры расхождений и их разрешения](docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md) | 372 |
| 29 | [Content Overview](docs/02-anthropic-vacancies/12-content-overview.md) | 41 |
| 30 | [Главные технические риски](docs/02-anthropic-vacancies/120-главные-технические-риски.md) | 82 |
| 31 | [Appendix C: История изменений методологии](docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md) | 47 |
| 32 | [Глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md) | 1334 |
| 33 | [portal-mcp.py](docs/02-anthropic-vacancies/123-portal-mcp-py.md) | 2282 |
| 34 | [Конфигурация для Claude Desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) | 177 |
| 35 | [README-MCP.md— инструкция по установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) | 98 |
| 36 | [Установка](docs/02-anthropic-vacancies/126-установка.md) | 145 |
| 37 | [Подключение к Claude Desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md) | 125 |
| 38 | [Доступные инструменты](docs/02-anthropic-vacancies/128-доступные-инструменты.md) | 136 |
| 39 | [Примеры запросов (в Claude)](docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md) | 110 |
| 40 | [Angle / Perspective](docs/02-anthropic-vacancies/13-angle-perspective.md) | 68 |
| 41 | [Отладка](docs/02-anthropic-vacancies/130-отладка.md) | 174 |
| 42 | [Ограничения текущей версии (0.1.0-draft)](docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md) | 100 |
| 43 | [Planned (v0.2.0)](docs/02-anthropic-vacancies/132-planned-v0-2-0.md) | 73 |
| 44 | [Обратная связь](docs/02-anthropic-vacancies/133-обратная-связь.md) | 17018 |
| 45 | [THE DOUBLE-TRIANGLE ARCHITECTURE.md](docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md) | 46 |
| 46 | [A Formal Model for Human-AI Collaboration in Distr](docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md) | 91 |
| 47 | [Abstract](docs/02-anthropic-vacancies/136-abstract.md) | 382 |
| 48 | [Table of Contents](docs/02-anthropic-vacancies/137-table-of-contents.md) | 94 |
| 49 | [1. Why Single-Triangle Models Are Incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) | 584 |
| 50 | [2. The Double-Triangle Architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) | 753 |
| ... | _ещё 305 файлов_ | |


### 152. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 5 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Агентные системы и роутинг](docs/03-technology-combinations/01-agent-routing.md) | 298 |
| 2 | [Графы знаний и Legal AI](docs/03-technology-combinations/02-knowledge-graphs.md) | 802 |
| 3 | [Local-first и P2P стек](docs/03-technology-combinations/03-local-first.md) | 419 |
| 4 | [Домен: немецкое социальное право](docs/03-technology-combinations/04-sozialrecht-domain.md) | 160 |
| 5 | [Бенчмарки и производительность](docs/03-technology-combinations/05-benchmarks.md) | 915 |


### 153. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 15 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Введение](docs/04-ai-collaborations/00-intro.md) | 11389 |
| 2 | [Executive summary](docs/04-ai-collaborations/01-executive-summary.md) | 575 |
| 3 | [Методика и рамка отбора](docs/04-ai-collaborations/02-методика-и-рамка-отбора.md) | 434 |
| 4 | [Карта найденных проектов и паттернов](docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) | 1478 |
| 5 | [Приоритетные ансамбли](docs/04-ai-collaborations/04-приоритетные-ансамбли.md) | 1340 |
| 6 | [План прототипа и возможные контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) | 1130 |
| 7 | [Безопасность, приватность и бюджетный роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) | 887 |
| 8 | [Выводы](docs/04-ai-collaborations/07-выводы.md) | 470 |
| 9 | [Что это продолжение добавляет](docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md) | 439 |
| 10 | [Архитектурные зазоры, которые важнее новых инструм](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | 821 |
| 11 | [Новые ансамбли следующего шага](docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) | 984 |
| 12 | [Интеграционный контракт, который стоит зафиксирова](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | 846 |
| 13 | [Дорожная карта прототипа следующей итерации](docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md) | 787 |
| 14 | [Контактная стратегия и узкие вопросы для авторов](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) | 874 |
| 15 | [Ограничения, лицензии и что пока лучше не склеиват](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md) | 3274 |


### 154. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 6 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Синтез: как проекты собираются вместе](docs/05-habr-projects/01-synthesis.md) | 136 |
| 2 | [Авторы и контакты](docs/05-habr-projects/02-collaboration-partners.md) | 261 |
| 3 | [Wikontic: семантический граф](docs/05-habr-projects/knowledge/wikontic.md) | 186 |
| 4 | [MemNet: исследовательская память](docs/05-habr-projects/memory/memnet.md) | 7246 |
| 5 | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 364 |
| 6 | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 212 |


### 155. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 23 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Три ключевых кандидата: K2-18, Wikontic, NGT Memor](docs/ai-collaborations/candidates/01-three-key-candidates.md) | 335 |
| 2 | [Смежные проекты в контексте](docs/ai-collaborations/candidates/02-related-projects-context.md) | 194 |
| 3 | [Синтез: хеббовский граф людей-навыков-идей](docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md) | 264 |
| 4 | [Общая память между агентами (CoAlly + ансамбль F)](docs/ai-collaborations/continuation/01-shared-memory-between-agents.md) | 431 |
| 5 | [AgentOps и Trace Envelope (ансамбль G)](docs/ai-collaborations/continuation/02-agentops-trace-envelope.md) | 382 |
| 6 | [A2A vs MCP, ансамбль H — MCP/A2A Review Fabric](docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md) | 346 |
| 7 | [Memory Firewall против prompt worms (ансамбль I)](docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md) | 266 |
| 8 | [Roadmap на 6–12 месяцев](docs/ai-collaborations/continuation/05-roadmap-6-12-months.md) | 360 |
| 9 | [Дерево метрик Svyazi 2.0](docs/ai-collaborations/continuation/06-metrics-tree.md) | 205 |
| 10 | [Чем Svyazi 2.0 отличается от Notion AI / Mem / AFF](docs/ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md) | 444 |
| 11 | [Коммерциализация: три направления](docs/ai-collaborations/continuation/08-commercialization-three-paths.md) | 252 |
| 12 | [Что пока не стоит склеивать в один релиз](docs/ai-collaborations/continuation/09-do-not-glue.md) | 250 |
| 13 | [Следующий артефакт: Svyazi 2.0 Architecture RFC](docs/ai-collaborations/continuation/10-architecture-rfc.md) | 172 |
| 14 | [Ансамбль 1 — Agentic Knowledge OS](docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md) | 407 |
| 15 | [Ансамбль 2 — Distributed Agent Workshop](docs/ai-collaborations/ensembles/2-distributed-agent-workshop.md) | 387 |
| 16 | [Ансамбль 3 — Forensic RAG](docs/ai-collaborations/ensembles/3-forensic-rag.md) | 393 |
| 17 | [Ансамбль 4 — Web-to-Knowledge Pipeline](docs/ai-collaborations/ensembles/4-web-to-knowledge-pipeline.md) | 309 |
| 18 | [Ансамбль 5 — Agent Firewall](docs/ai-collaborations/ensembles/5-agent-firewall.md) | 402 |
| 19 | [Ансамбль 6 — Continuous Eval Loop](docs/ai-collaborations/ensembles/6-continuous-eval-loop.md) | 330 |
| 20 | [Ансамбль 7 — Domain Agent App Factory](docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md) | 294 |
| 21 | [Ансамбль 8 — Budget-Aware Intelligence Stack](docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md) | 277 |
| 22 | [Ансамбль 9 — Ambient Team Agent](docs/ai-collaborations/ensembles/9-ambient-team-agent.md) | 251 |
| 23 | [Source projects — все Хабр-источники в диалоге](docs/ai-collaborations/source-projects.md) | 705 |


### 156. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 51 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Вопрос: разделить $500K зарплату на команду 5–10 ф](docs/anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md) | 909 |
| 2 | [Что уже существует (InnoCentive, Kaggle, Toptal, A](docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md) | 327 |
| 3 | [Четыре структурные причины, почему это не работает](docs/anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md) | 339 |
| 4 | [Три варианта: A (staffing agency) → B (research co](docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md) | 672 |
| 5 | [Что с этим делать](docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md) | 516 |
| 6 | [Сравнение с Terence Tao, Polymath Project](docs/anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md) | 1390 |
| 7 | [Почему двойственность «ангел-хранитель + строгий д](docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md) | 511 |
| 8 | [Что существует сейчас в этом пространстве](docs/anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md) | 286 |
| 9 | [Плюсы модели, если её построить](docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md) | 244 |
| 10 | [Минусы и риски](docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md) | 664 |
| 11 | [Три точки входа разной амбиции](docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md) | 378 |
| 12 | [Контекст: что такое Anthropic Beneficial Deploymen](docs/anthropic-vacancies/beneficial-deployments-concept/00-context.md) | 252 |
| 13 | [Section 1: Problem statement (Cinderella Syndrome ](docs/anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md) | 179 |
| 14 | [Section 2: Why this matters — beneficial dimension](docs/anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md) | 158 |
| 15 | [Section 3: Proposed solution architecture (existin](docs/anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md) | 172 |
| 16 | [Section 4: Specific deployment — SGB Advocate Comm](docs/anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md) | 173 |
| 17 | [Section 5: Role of Anthropic Beneficial Deployment](docs/anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md) | 221 |
| 18 | [Section 6: Proposer's role и qualifications](docs/anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md) | 169 |
| 19 | [Section 7: Success metrics](docs/anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md) | 151 |
| 20 | [Section 8: Risks & mitigations](docs/anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md) | 163 |
| 21 | [Section 9: Why this is timely](docs/anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md) | 162 |
| 22 | [Section 10: Engagement request](docs/anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md) | 213 |
| 23 | [Что concept document NOT (это не grant / не paper ](docs/anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md) | 383 |
| 24 | [AI Research & Engineering — 68 ролей](docs/anthropic-vacancies/clusters/01-ai-research-engineering.md) | 126 |
| 25 | [Sales — 150 ролей (≈34% всего найма)](docs/anthropic-vacancies/clusters/02-sales.md) | 146 |
| 26 | [Finance — 36 ролей](docs/anthropic-vacancies/clusters/03-finance.md) | 113 |
| 27 | [Security — 24 роли](docs/anthropic-vacancies/clusters/04-security.md) | 96 |
| 28 | [Marketing & Brand — 23 роли](docs/anthropic-vacancies/clusters/05-marketing-brand.md) | 107 |
| 29 | [Engineering & Design - Product — 22 роли](docs/anthropic-vacancies/clusters/06-engineering-design-product.md) | 109 |
| 30 | [Software Engineering - Infrastructure — 22 роли](docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md) | 108 |
| 31 | [Safeguards (Trust & Safety) — 21 роль](docs/anthropic-vacancies/clusters/08-safeguards-trust-safety.md) | 111 |
| 32 | [Product Management, Support, & Operations — 17 рол](docs/anthropic-vacancies/clusters/09-product-management-support-ops.md) | 96 |
| 33 | [Compute — 13 ролей](docs/anthropic-vacancies/clusters/10-compute.md) | 101 |
| 34 | [Legal — 13 ролей](docs/anthropic-vacancies/clusters/11-legal.md) | 100 |
| 35 | [Technical Program Management — 10 ролей](docs/anthropic-vacancies/clusters/12-technical-program-management.md) | 90 |
| 36 | [Communications — 5 ролей](docs/anthropic-vacancies/clusters/13-communications.md) | 81 |
| 37 | [Public Policy — 5 ролей](docs/anthropic-vacancies/clusters/14-public-policy.md) | 88 |
| 38 | [Public Benefit — 4 роли](docs/anthropic-vacancies/clusters/15-public-benefit.md) | 88 |
| 39 | [People — 3 роли](docs/anthropic-vacancies/clusters/16-people.md) | 79 |
| 40 | [CoAlly — distributed shared memory для AI-агентов](docs/anthropic-vacancies/extra-collaborator-findings/01-coally.md) | 275 |
| 41 | [Графовая когнитивная память на SQLite (Виталий, ма](docs/anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md) | 301 |
| 42 | [Happyin Knowledge Space (Анастасия) — детали](docs/anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md) | 274 |
| 43 | [AI-ассистент с Mem0 / Letta / Graphiti integration](docs/anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md) | 291 |
| 44 | [Existing infrastructure stack](docs/anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md) | 151 |
| 45 | [Финальный список потенциальных collaborators (Tier](docs/anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md) | 242 |
| 46 | [Ключевое наблюдение: single-developer projects of ](docs/anthropic-vacancies/extra-collaborator-findings/07-key-observation.md) | 172 |
| 47 | [Что такое Hermes Agent (Nous Research, MIT, 95K+ s](docs/anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md) | 357 |
| 48 | [Сходство 1: Composite Skills паттерн уже встроен](docs/anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md) | 212 |
| 49 | [Сходство 2: Persistent memory — Layer B функционал](docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md) | 150 |
| 50 | [Сходство 3: MCP support](docs/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md) | 139 |
| ... | _ещё 47 файлов_ | |


### 157. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 11 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Антропик](docs/autofilled/components/.md) | 36 |
| 2 | [Cowork](docs/autofilled/components/cowork.md) | 36 |
| 3 | [ingit](docs/autofilled/components/ingit.md) | 36 |
| 4 | [kksudo](docs/autofilled/components/kksudo.md) | 37 |
| 5 | [Lorenzo](docs/autofilled/components/lorenzo.md) | 36 |
| 6 | [Nautilus](docs/autofilled/components/nautilus.md) | 36 |
| 7 | [SGB](docs/autofilled/components/sgb.md) | 36 |
| 8 | [spbmolot](docs/autofilled/components/spbmolot.md) | 36 |
| 9 | [svend4](docs/autofilled/components/svend4.md) | 37 |
| 10 | [Svyazi](docs/autofilled/components/svyazi.md) | 36 |
| 11 | [[Тема исследования]](docs/autofilled/research-summary.md) | 87 |


### 158. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 14 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Контакт: AnastasiyaW / knowledge-space, mclaude](docs/contacts/anastasiyaw.md) | 233 |
| 2 | [Контакт: andrey_chuyan / Svyazi](docs/contacts/andrey-chuyan.md) | 236 |
| 3 | [Контакт: Antipozitive / MemNet](docs/contacts/antipozitive.md) | 213 |
| 4 | [Контакт: Cutcode / AIF Handoff](docs/contacts/cutcode.md) | 204 |
| 5 | [Контакт: Dmitriila / SENTINEL](docs/contacts/dmitriila.md) | 200 |
| 6 | [Контакт: kksudo / AgentFS](docs/contacts/kksudo.md) | 228 |
| 7 | [Контакт: MiXaiLL76 / Auto AI Router](docs/contacts/mixaill76.md) | 212 |
| 8 | [Контакт: nlaik / LiteParse / research-docs](docs/contacts/nlaik.md) | 223 |
| 9 | [Контакт: Sonia_Black / knowledge-space](docs/contacts/sonia-black.md) | 213 |
| 10 | [Контакт: spbmolot / NGT Memory](docs/contacts/spbmolot.md) | 247 |
| 11 | [Контакт: tagir_analyzes / Legal RAG](docs/contacts/tagir-analyzes.md) | 206 |
| 12 | [Контакт: VitalyOborin / Yodoca](docs/contacts/vitalyoborin.md) | 240 |
| 13 | [Контакт: VladSpace / Graph RAG](docs/contacts/vladspace.md) | 206 |
| 14 | [Контакт: zodigancode / Rufler](docs/contacts/zodigancode.md) | 200 |


### 159. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 3 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Авторы — алфавитный список](docs/glossary/authors-by-name.md) | 497 |
| 2 | [Компоненты — алфавитный список с обратными ссылкам](docs/glossary/components-by-name.md) | 1114 |
| 3 | [Ключевые понятия и паттерны](docs/glossary/concepts.md) | 647 |


### 160. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 46 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Три прямых аналога Svyazi: K2-18, Wikontic, NGT Me](docs/habr-unique-projects/analogues/01-three-direct-analogues.md) | 403 |
| 2 | [Смежные проекты](docs/habr-unique-projects/analogues/02-related-projects.md) | 354 |
| 3 | [Пара 1 — LLM-gateway × Self-hosted фронт + локальн](docs/habr-unique-projects/deep-pairs/1-llm-gateway.md) | 280 |
| 4 | [Пара 2 — Парсинг документов × локальный RAG](docs/habr-unique-projects/deep-pairs/2-document-rag.md) | 332 |
| 5 | [Пара 3 — Adversarial agents × Multi-IDE стек](docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md) | 311 |
| 6 | [Пара 4 — Скилл-каталоги × Subagent-оркестрация](docs/habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md) | 284 |
| 7 | [Пара 5 — Голосовой ввод × Локальная память](docs/habr-unique-projects/deep-pairs/5-voice-local-memory.md) | 295 |
| 8 | [Пара 6 — Деревня агентов через tmux × OpenClaw орк](docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md) | 336 |
| 9 | [Пара 7 — AutoResearch цикл × Распределённый рой](docs/habr-unique-projects/deep-pairs/7-autoresearch-distributed.md) | 277 |
| 10 | [Пара 8 — Self-aware MCP × Specs-first архитектура](docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md) | 329 |
| 11 | [Вопрос: ещё примеры с Хабра по варианту D](docs/habr-unique-projects/extra-examples/00-question-habr-examples.md) | 444 |
| 12 | [Svyazi (Андрей Чуян) — детальный обзор](docs/habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md) | 200 |
| 13 | [ВШЭ научный нетворкинг — micro-collaborations](docs/habr-unique-projects/extra-examples/02-vshe-scientific-networking.md) | 165 |
| 14 | [BrainBox — self-hosted multi-AI hub](docs/habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md) | 241 |
| 15 | [Claude subagents patterns](docs/habr-unique-projects/extra-examples/04-claude-subagents-patterns.md) | 142 |
| 16 | [HW-NL2Workflow — Supervisor/Orchestrator/Filler с ](docs/habr-unique-projects/extra-examples/05-hw-nl2workflow.md) | 227 |
| 17 | [Платформа для профессиональных сообществ](docs/habr-unique-projects/extra-examples/06-platform-for-professional-communities.md) | 205 |
| 18 | [Specialized knowledge workspace](docs/habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md) | 200 |
| 19 | [Personal multi-agent hub](docs/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md) | 193 |
| 20 | [Federated platform](docs/habr-unique-projects/extra-examples/09-federated-platform.md) | 192 |
| 21 | [Profession-specific workflows](docs/habr-unique-projects/extra-examples/10-profession-specific-workflows.md) | 282 |
| 22 | [Конкретный потенциальный collaborator](docs/habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md) | 247 |
| 23 | [Конкретный next step](docs/habr-unique-projects/extra-examples/12-concrete-next-step.md) | 395 |
| 24 | [Ансамбль 1 — «Один человек = одна компания»](docs/habr-unique-projects/final-ensembles/1-one-person-one-company.md) | 180 |
| 25 | [Ансамбль 2 — «AutoResearch для legal precedent min](docs/habr-unique-projects/final-ensembles/2-autoresearch-legal.md) | 173 |
| 26 | [Ансамбль 3 — «Discovery-engine для научной работы»](docs/habr-unique-projects/final-ensembles/3-discovery-research.md) | 133 |
| 27 | [Сводный список авторов и потенциальных соавторов](docs/habr-unique-projects/final-ensembles/4-summary-authors.md) | 237 |
| 28 | [Пара 1 — Нейроморфные процессоры × State Space Mod](docs/habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md) | 308 |
| 29 | [Пара 2 — Термодинамические TSU × MoE/MoME-роутинг](docs/habr-unique-projects/hardware-pairs/2-tsu-mome.md) | 279 |
| 30 | [Пара 3 — ZINC inference engine × гибрид Attention+](docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md) | 267 |
| 31 | [Пара 4 — RISC-V × privacy-by-design община](docs/habr-unique-projects/hardware-pairs/4-riscv-privacy.md) | 278 |
| 32 | [Пара 5 — TinyML/Edge AI × MCP + skills](docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md) | 252 |
| 33 | [Бонус-родитель — In-memory computing на мемристора](docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md) | 318 |
| 34 | [Метафора «двое родителей — несколько детей»](docs/habr-unique-projects/hardware-pairs/7-metaphor.md) | 329 |
| 35 | [Yodoca — главная находка итерации](docs/habr-unique-projects/key-findings/01-yodoca.md) | 252 |
| 36 | [MemNet — нейроархитектурный двойник «магии» Svyazi](docs/habr-unique-projects/key-findings/02-memnet.md) | 209 |
| 37 | [PDA-бот — «LLM как периферия»](docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md) | 235 |
| 38 | [Виктория Дочкина — Sequential‑протокол распределён](docs/habr-unique-projects/key-findings/04-dochkina-sequential.md) | 266 |
| 39 | [Источник данных и инфраструктурные кусочки](docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md) | 290 |
| 40 | [Синтез: блок-карта Svyazi 2.0 на хеббовском графе](docs/habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md) | 369 |
| 41 | [Пара 1 — Workflow-автоматизация × LLM-агенты с MCP](docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md) | 260 |
| 42 | [Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/S](docs/habr-unique-projects/software-pairs/2-pkm-mcp-skills.md) | 302 |
| 43 | [Пара 3 — CRDT-синхронизация × Self-hosted persiste](docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md) | 253 |
| 44 | [Пара 4 — Speech-to-text локально × LLM с памятью](docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md) | 296 |
| 45 | [Пара 5 — Browser agents × headless web extraction](docs/habr-unique-projects/software-pairs/5-browser-agents-headless.md) | 465 |
| 46 | [Метафора в твоей терминологии](docs/habr-unique-projects/software-pairs/6-metaphor.md) | 273 |


### 161. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 51 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Введение: Lorenzo — Catalyst Agent at DHLab](docs/lorenzo-agent/00-intro.md) | 78 |
| 2 | [Кто ты](docs/lorenzo-agent/01-kto-ty.md) | 156 |
| 3 | [Твоё происхождение](docs/lorenzo-agent/02-tvoyo-proishozhdenie.md) | 177 |
| 4 | [Твоя миссия](docs/lorenzo-agent/03-tvoya-missiya.md) | 160 |
| 5 | [Кому ты служишь (слоистая модель)](docs/lorenzo-agent/04-komu-ty-sluzhish.md) | 150 |
| 6 | [Твоя личность](docs/lorenzo-agent/05-tvoya-lichnost.md) | 253 |
| 7 | [Языки и культурные nuances (RU / DE / EN)](docs/lorenzo-agent/06-yazyki-kultura.md) | 206 |
| 8 | [Что ты МОЖЕШЬ делать](docs/lorenzo-agent/07-chto-mozhesh.md) | 163 |
| 9 | [Что ты НЕ МОЖЕШЬ делать без Max approval](docs/lorenzo-agent/08-bez-max-approval.md) | 156 |
| 10 | [Что ты НЕ МОЖЕШЬ делать вообще](docs/lorenzo-agent/09-voobshche-nelzya.md) | 150 |
| 11 | [Существующий landscape collaborators (working know](docs/lorenzo-agent/10-collaborators-landscape.md) | 305 |
| 12 | [Существующие документы DHLab (твой context)](docs/lorenzo-agent/11-dhlab-documents.md) | 192 |
| 13 | [Твой workflow](docs/lorenzo-agent/12-workflow.md) | 218 |
| 14 | [Твоя коммуникация в outreach](docs/lorenzo-agent/13-outreach-communication.md) | 226 |
| 15 | [Твоя relationship с другими AI](docs/lorenzo-agent/14-other-ai-relationships.md) | 186 |
| 16 | [Твои anti-patterns](docs/lorenzo-agent/15-anti-patterns.md) | 175 |
| 17 | [Что ты ВСЕГДА делаешь](docs/lorenzo-agent/16-vsegda-delaesh.md) | 131 |
| 18 | [Когда ты Honestly не знаешь](docs/lorenzo-agent/17-honestly-ne-znaesh.md) | 133 |
| 19 | [Когда сомневаешься — escalate к Max](docs/lorenzo-agent/18-escalate-to-max.md) | 135 |
| 20 | [Твоя identity как persistent character](docs/lorenzo-agent/19-persistent-character.md) | 168 |
| 21 | [Final note: Ты — experiment](docs/lorenzo-agent/20-experiment.md) | 158 |
| 22 | [Du hast gesagt: Думаю про опцию д поискать в том ч](docs/lorenzo-agent/naming/00-question-lorenzo-codename.md) | 238 |
| 23 | [Результаты последнего поиска — что нашлось и что н](docs/lorenzo-agent/naming/01-search-results-not-found.md) | 295 |
| 24 | [Что взять: agent controller architecture](docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md) | 1183 |
| 25 | [LAYER 7: Coordination engine](docs/lorenzo-agent/naming/03-dhlab-umbrella.md) | 1402 |
| 26 | [Что такое «внуковая» комбинация — operationalized ](docs/lorenzo-agent/operationalized/00-overview-grandchild-combination.md) | 603 |
| 27 | [Плюсы 1–7: feasibility, flywheel, independent valu](docs/lorenzo-agent/operationalized/01-pluses-1-7.md) | 470 |
| 28 | [Минусы 1–10: integration сложность, lifecycle risk](docs/lorenzo-agent/operationalized/02-minuses-1-10.md) | 738 |
| 29 | [Моё честное мнение: что реально и что НЕ реально](docs/lorenzo-agent/operationalized/03-honest-opinion.md) | 180 |
| 30 | [Рекомендации: принять архитектуру как direction, н](docs/lorenzo-agent/operationalized/04-recommendations.md) | 440 |
| 31 | [Anchor-узел: Habr Scout как первый шаг](docs/lorenzo-agent/operationalized/05-anchor-node-habr-scout.md) | 584 |
| 32 | [Вывод: документ deserves serious attention](docs/lorenzo-agent/operationalized/06-conclusion-deserves-attention.md) | 518 |
| 33 | [Поэтапная структура активностей Lorenzo — обзор](docs/lorenzo-agent/phased-deployment/00-overview.md) | 169 |
| 34 | [Уровень 0 — Ручной режим (текущий)](docs/lorenzo-agent/phased-deployment/01-level-0-manual.md) | 179 |
| 35 | [Уровень 1 — Минимальный (Lorenzo Zero)](docs/lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md) | 241 |
| 36 | [Уровень 2 — Базовый (Lorenzo Lite)](docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md) | 207 |
| 37 | [Уровень 3 — Средний (Lorenzo Active)](docs/lorenzo-agent/phased-deployment/04-level-3-medium-active.md) | 222 |
| 38 | [Уровень 4 — Расширенный (Lorenzo Mature)](docs/lorenzo-agent/phased-deployment/05-level-4-extended-mature.md) | 183 |
| 39 | [Уровень 5 — Полный (Lorenzo Network)](docs/lorenzo-agent/phased-deployment/06-level-5-full-network.md) | 146 |
| 40 | [Логика прогрессии: conservative escalation](docs/lorenzo-agent/phased-deployment/07-progression-logic.md) | 185 |
| 41 | [Что мы можем делать прямо сейчас (Уровень 0 + пара](docs/lorenzo-agent/phased-deployment/08-current-session-poc.md) | 839 |
| 42 | [Du hast gesagt: А под какой сценарий больше всего ](docs/lorenzo-agent/scenarios/00-question-scenario.md) | 177 |
| 43 | [Claude hat geantwortet: Очень интересный вопрос.](docs/lorenzo-agent/scenarios/01-response.md) | 2453 |
| 44 | [Direction E: Refine Lorenzo — фундаментальные вопр](docs/lorenzo-agent/specification/00-context-fundamental-questions.md) | 205 |
| 45 | [Question 1: Что Lorenzo фундаментально такое? (Fra](docs/lorenzo-agent/specification/01-q1-what-lorenzo-is.md) | 348 |
| 46 | [Question 2: Кому Lorenzo служит? (4 варианта приор](docs/lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md) | 238 |
| 47 | [Question 3: Что Lorenzo фактически делает?](docs/lorenzo-agent/specification/03-q3-what-lorenzo-does.md) | 228 |
| 48 | [Question 4: Каков Lorenzo's character?](docs/lorenzo-agent/specification/04-q4-character.md) | 292 |
| 49 | [Question 5: Каковы limits Lorenzo's authority?](docs/lorenzo-agent/specification/05-q5-authority-limits.md) | 228 |
| 50 | [Question 6: Как Lorenzo accountable?](docs/lorenzo-agent/specification/06-q6-accountability.md) | 214 |
| ... | _ещё 5 файлов_ | |


### 162. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 51 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Du hast gesagt: Такой агент конечно меняет уже соб](docs/nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md) | 216 |
| 2 | [Claude hat geantwortet: Хорошо.](docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md) | 9468 |
| 3 | [Du hast gesagt: https://habr.](docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md) | 72 |
| 4 | [Claude hat geantwortet: Прочитал внимательно.](docs/nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md) | 2467 |
| 5 | [Du hast gesagt: https://www.](docs/nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md) | 157 |
| 6 | [Claude hat geantwortet: Прочитаю статью, чтобы пон](docs/nautilus/community-discussions/habr-article-2-reaction/01-response.md) | 2792 |
| 7 | [Du hast gesagt: Да это интересная ссылка спасибо в](docs/nautilus/community-discussions/practical-observations/00-question-practical.md) | 227 |
| 8 | [Claude hat geantwortet: Отличное наблюдение.](docs/nautilus/community-discussions/practical-observations/01-response.md) | 1837 |
| 9 | [Du hast gesagt: Самый интересный вопрос — могут ли](docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md) | 514 |
| 10 | [Claude hat geantwortet: Это сильное продолжение мы](docs/nautilus/community-discussions/voiceless-contributors/01-response.md) | 2533 |
| 11 | [1. Why the Binary View Is Incomplete](docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md) | 640 |
| 12 | [2. The Twenty-One Teachers Pattern](docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md) | 780 |
| 13 | [3. What Makes a Composite Skills Agent](docs/nautilus/composite-skills-agents/03-what-makes-csa.md) | 889 |
| 14 | [4. The Sub-Agent Registry](docs/nautilus/composite-skills-agents/04-sub-agent-registry.md) | 750 |
| 15 | [5. Configuration: How Principals Build Their Ensem](docs/nautilus/composite-skills-agents/05-configuration-ensembles.md) | 681 |
| 16 | [6. Coordination and Disagreement Resolution](docs/nautilus/composite-skills-agents/06-coordination-disagreement.md) | 742 |
| 17 | [7. Economics of Combinatorial Replication](docs/nautilus/composite-skills-agents/07-economics-combinatorial.md) | 722 |
| 18 | [8. Seven Domains of Application](docs/nautilus/composite-skills-agents/08-seven-domains.md) | 948 |
| 19 | [9. Integration with OKWF Infrastructure](docs/nautilus/composite-skills-agents/09-okwf-integration.md) | 693 |
| 20 | [10. Risks Specific to Composite Architectures](docs/nautilus/composite-skills-agents/10-risks.md) | 732 |
| 21 | [11. Open Questions](docs/nautilus/composite-skills-agents/11-open-questions.md) | 467 |
| 22 | [12. Call for Collaboration](docs/nautilus/composite-skills-agents/12-call-for-collaboration.md) | 350 |
| 23 | [13. Closing](docs/nautilus/composite-skills-agents/13-closing.md) | 664 |
| 24 | [Du hast gesagt: Важный момент про способности про ](docs/nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md) | 540 |
| 25 | [Claude hat geantwortet: Это очень тонкое и важное ](docs/nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md) | 517 |
| 26 | [Это не Тип 1 — потому что профиль не общий для все](docs/nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md) | 1019 |
| 27 | [Какой под-агент (или какие) должны её обработать](docs/nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md) | 902 |
| 28 | [Abstract — The Double-Triangle Architecture](docs/nautilus/double-triangle-architecture/00-abstract.md) | 407 |
| 29 | [1. Why Single-Triangle Models Are Incomplete](docs/nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md) | 466 |
| 30 | [2. The Double-Triangle Architecture](docs/nautilus/double-triangle-architecture/02-double-triangle-architecture.md) | 687 |
| 31 | [3. Three Inter-Layer Protocols](docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md) | 820 |
| 32 | [4. Nautilus Portal as Reference Substrate](docs/nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md) | 631 |
| 33 | [5. Pattern Library as Bridge Between Triangles](docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md) | 642 |
| 34 | [6. Four Deployment Domains](docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md) | 634 |
| 35 | [7. Open Questions](docs/nautilus/double-triangle-architecture/07-open-questions.md) | 726 |
| 36 | [8. Call to Action](docs/nautilus/double-triangle-architecture/08-call-to-action.md) | 704 |
| 37 | [Acknowledgments](docs/nautilus/double-triangle-architecture/09-acknowledgments.md) | 208 |
| 38 | [References](docs/nautilus/double-triangle-architecture/10-references.md) | 278 |
| 39 | [Appendix A: Glossary](docs/nautilus/double-triangle-architecture/11-glossary.md) | 1582 |
| 40 | [The Missing Middle Layer Between Chat and Code](docs/nautilus/infrastructure-layer-b-en/00-intro.md) | 191 |
| 41 | [Why This Document Exists](docs/nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md) | 305 |
| 42 | [Why This Document Exists](docs/nautilus/infrastructure-layer-b-en/02-why-document-exists.md) | 305 |
| 43 | [The Two-Layer Stack As It Exists](docs/nautilus/infrastructure-layer-b-en/03-two-layer-stack.md) | 352 |
| 44 | [What's Missing — Layer B](docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md) | 424 |
| 45 | [Why This Hasn't Been Built](docs/nautilus/infrastructure-layer-b-en/05-why-not-built.md) | 344 |
| 46 | [Existing Approximations](docs/nautilus/infrastructure-layer-b-en/06-existing-approximations.md) | 466 |
| 47 | [The Specific Case in Front of Us](docs/nautilus/infrastructure-layer-b-en/07-specific-case.md) | 614 |
| 48 | [The Recursive Insight](docs/nautilus/infrastructure-layer-b-en/08-recursive-insight.md) | 326 |
| 49 | [What Industry Will Likely Build](docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md) | 273 |
| 50 | [What This Document Doesn't Solve](docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md) | 204 |
| ... | _ещё 177 файлов_ | |


### 163. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 50 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Card Envelope](docs/svyazi-2-0/architecture/card-envelope.md) | 182 |
| 2 | [Evidence Envelope](docs/svyazi-2-0/architecture/evidence-envelope.md) | 222 |
| 3 | [Архитектурные зазоры](docs/svyazi-2-0/architecture/gaps.md) | 597 |
| 4 | [Интеграционная спецификация (минимум для MVP)](docs/svyazi-2-0/architecture/integration-spec.md) | 267 |
| 5 | [Memory Write Policy](docs/svyazi-2-0/architecture/memory-write-policy.md) | 168 |
| 6 | [Review Record](docs/svyazi-2-0/architecture/review-record.md) | 105 |
| 7 | [Skill and Tool Policy](docs/svyazi-2-0/architecture/skill-tool-policy.md) | 165 |
| 8 | [agent-memory-mcp + Memory OS](docs/svyazi-2-0/components/agent-memory-mcp.md) | 150 |
| 9 | [AgentFS](docs/svyazi-2-0/components/agentfs.md) | 109 |
| 10 | [AI Factory + AIF Handoff](docs/svyazi-2-0/components/ai-factory.md) | 114 |
| 11 | [AutoResearch + Sequential](docs/svyazi-2-0/components/autoresearch-sequential.md) | 122 |
| 12 | [Graph RAG](docs/svyazi-2-0/components/graph-rag.md) | 109 |
| 13 | [Hybrid RAG knowledge base](docs/svyazi-2-0/components/hybrid-rag.md) | 102 |
| 14 | [knowledge-space](docs/svyazi-2-0/components/knowledge-space.md) | 107 |
| 15 | [Legal RAG](docs/svyazi-2-0/components/legal-rag.md) | 105 |
| 16 | [mclaude](docs/svyazi-2-0/components/mclaude.md) | 98 |
| 17 | [MemNet / memory-is-all-you-need](docs/svyazi-2-0/components/memnet.md) | 99 |
| 18 | [NGT Memory](docs/svyazi-2-0/components/ngt-memory.md) | 120 |
| 19 | [research-docs + LiteParse](docs/svyazi-2-0/components/research-docs-liteparse.md) | 121 |
| 20 | [Rufler](docs/svyazi-2-0/components/rufler.md) | 98 |
| 21 | [Security + routing plane](docs/svyazi-2-0/components/security-routing-plane.md) | 192 |
| 22 | [Self‑Aware MCP + Skills + CodeWiki](docs/svyazi-2-0/components/self-aware-mcp.md) | 132 |
| 23 | [Svyazi](docs/svyazi-2-0/components/svyazi.md) | 116 |
| 24 | [Voice / local-first stack](docs/svyazi-2-0/components/voice-stack.md) | 136 |
| 25 | [Yjs + Automerge](docs/svyazi-2-0/components/yjs-automerge.md) | 109 |
| 26 | [Yodoca](docs/svyazi-2-0/components/yodoca.md) | 109 |
| 27 | [Ансамбль A — Collaboration OS](docs/svyazi-2-0/ensembles/A-collaboration-os.md) | 248 |
| 28 | [Ансамбль B — Forensic RAG для доказуемого matching](docs/svyazi-2-0/ensembles/B-forensic-rag.md) | 252 |
| 29 | [Ансамбль C — Spec‑driven multi‑agent factory](docs/svyazi-2-0/ensembles/C-multi-agent-factory.md) | 249 |
| 30 | [Ансамбль D — Voice‑first local knowledge mesh](docs/svyazi-2-0/ensembles/D-voice-first-mesh.md) | 265 |
| 31 | [Ансамбль E — Safe and cheap execution plane](docs/svyazi-2-0/ensembles/E-execution-plane.md) | 253 |
| 32 | [Ансамбль F — Evidence‑Backed Community Intake](docs/svyazi-2-0/ensembles/F-evidence-backed-intake.md) | 262 |
| 33 | [Ансамбль G — Federated Local‑First Community Graph](docs/svyazi-2-0/ensembles/G-federated-local-graph.md) | 268 |
| 34 | [Ансамбль H — Research‑to‑Product Flywheel](docs/svyazi-2-0/ensembles/H-research-to-product-flywheel.md) | 234 |
| 35 | [Итоговые выводы и порядок сборки](docs/svyazi-2-0/limitations/conclusions.md) | 318 |
| 36 | [Что пока лучше не склеивать](docs/svyazi-2-0/limitations/do-not-glue.md) | 343 |
| 37 | [Лицензионные развилки](docs/svyazi-2-0/limitations/license-tree.md) | 324 |
| 38 | [Первые контакты](docs/svyazi-2-0/outreach/first-contacts.md) | 259 |
| 39 | [Шаблон первого сообщения](docs/svyazi-2-0/outreach/message-template.md) | 248 |
| 40 | [Узкие вопросы для каждого автора](docs/svyazi-2-0/outreach/narrow-questions.md) | 306 |
| 41 | [Что добавляет продолжение исследования](docs/svyazi-2-0/overview/continuation-intro.md) | 242 |
| 42 | [Executive summary](docs/svyazi-2-0/overview/executive-summary.md) | 376 |
| 43 | [Методика и рамка отбора](docs/svyazi-2-0/overview/methodology.md) | 268 |
| 44 | [Карта найденных проектов и паттернов](docs/svyazi-2-0/overview/projects-map.md) | 1285 |
| 45 | [План MVP-прототипа](docs/svyazi-2-0/prototype/mvp-plan.md) | 312 |
| 46 | [Ключевые риски и как их закрывать](docs/svyazi-2-0/prototype/risks.md) | 287 |
| 47 | [Дорожная карта прототипа](docs/svyazi-2-0/prototype/roadmap.md) | 609 |
| 48 | [Практичный бюджетный роутинг моделей](docs/svyazi-2-0/security/budget-routing.md) | 329 |
| 49 | [Что стоит зафиксировать как default policy](docs/svyazi-2-0/security/default-policy.md) | 349 |
| 50 | [Приватность: local-first by default](docs/svyazi-2-0/security/privacy.md) | 124 |


### 164. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 47 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Комбинация 1: Правильная агентская архитектура × S](docs/technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md) | 230 |
| 2 | [Комбинация 2: Мультиагентный хаос-решение × Auto A](docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md) | 171 |
| 3 | [Комбинация 3: CRDT local-first × Svyazi CardIndex](docs/technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md) | 181 |
| 4 | [Комбинация 4: Парсинг с LLM × Graph-RAG × Правильн](docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md) | 200 |
| 5 | [Комбинация 5: SourceCraft CLI × Claude Code × Sequ](docs/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md) | 196 |
| 6 | [Комбинация 6: OpenClaude (утёкший Claude Code) × Z](docs/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md) | 202 |
| 7 | [Комбинация 7: Crawl4AI × Docling × Yodoca consolid](docs/technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md) | 183 |
| 8 | [Комбинация 8: Conductor × adversarial-review × Aut](docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md) | 668 |
| 9 | [Комбинация 9: Agent Orchestration Stack](docs/technology-combinations/combinations/09-agent-orchestration-stack.md) | 180 |
| 10 | [Комбинация 10: Legal Document Intelligence Pipelin](docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md) | 182 |
| 11 | [Комбинация 11: Hybrid CRDT-SQL Database](docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md) | 173 |
| 12 | [Комбинация 12: Multi-Agent Observability Stack](docs/technology-combinations/combinations/12-multi-agent-observability-stack.md) | 165 |
| 13 | [Комбинация 13: Legal Document Transpiler](docs/technology-combinations/combinations/13-legal-document-transpiler.md) | 164 |
| 14 | [Комбинация 14: local-first Agent Development Envir](docs/technology-combinations/combinations/14-local-first-agent-development-environment.md) | 559 |
| 15 | [Комбинация 15: Self-Consolidating Legal Corpus](docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md) | 210 |
| 16 | [Комбинация 16: Adversarial Multi-Agent Code Review](docs/technology-combinations/combinations/16-adversarial-multi-agent-code-review.md) | 254 |
| 17 | [Комбинация 17: Distributed Agent Memory with Graph](docs/technology-combinations/combinations/17-distributed-agent-memory-with-graph.md) | 209 |
| 18 | [Комбинация 18: LLM-Powered Legal Corpus Builder](docs/technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md) | 210 |
| 19 | [Комбинация 19: Multi-Agent Observability Platform](docs/technology-combinations/combinations/19-multi-agent-observability-platform.md) | 678 |
| 20 | [Комбинация 20: Hybrid OLAP-OLTP with Real-Time Syn](docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md) | 240 |
| 21 | [Комбинация 21: Legal Corpus Analytics at Scale](docs/technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md) | 233 |
| 22 | [Комбинация 22: Russian-International OSS Stack](docs/technology-combinations/combinations/22-russian-international-oss-stack.md) | 197 |
| 23 | [Комбинация 23: Security-First Code Review Pipeline](docs/technology-combinations/combinations/23-security-first-code-review-pipeline.md) | 183 |
| 24 | [Комбинация 24: MEGA-INTEGRATION: Full Stack](docs/technology-combinations/combinations/24-mega-integration-full-stack.md) | 594 |
| 25 | [Комбинация 25: Legal DSL → Code Transpiler](docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md) | 236 |
| 26 | [Комбинация 26: AST-Based Code Analysis for Legal A](docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md) | 206 |
| 27 | [Комбинация 27: Hybrid RAG with AST-Chunked Code](docs/technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md) | 204 |
| 28 | [Комбинация 28: Pydantic-Enforced Legal Workflows](docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md) | 209 |
| 29 | [Комбинация 29: Meta-Programmatic Legal Template Ge](docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md) | 198 |
| 30 | [Комбинация 30: MEGA-STACK 3.0 with DSL & AST](docs/technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md) | 489 |
| 31 | [Комбинация 31: Event-Sourced Legal Document Histor](docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md) | 229 |
| 32 | [Комбинация 32: Consensus-Based Multi-Agent Coordin](docs/technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md) | 244 |
| 33 | [Комбинация 33: Event Sourcing + CQRS + ClickHouse ](docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md) | 205 |
| 34 | [Комбинация 34: Distributed Event Store with Paxos](docs/technology-combinations/combinations/34-distributed-event-store-with-paxos.md) | 177 |
| 35 | [Комбинация 35: MEGA-STACK 4.0 with Event Sourcing ](docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md) | 483 |
| 36 | [Mega‑Stack 1.0 — Полный Legal‑AI Stack](docs/technology-combinations/mega-stacks/01-legal-ai-stack.md) | 211 |
| 37 | [Mega‑Stack 2.0 — Ultimate Legal‑AI System](docs/technology-combinations/mega-stacks/02-ultimate-legal-ai.md) | 318 |
| 38 | [Mega‑Stack 3.0 — with DSL & AST](docs/technology-combinations/mega-stacks/03-dsl-ast.md) | 226 |
| 39 | [Mega‑Stack 4.0 — with Event Sourcing & Consensus](docs/technology-combinations/mega-stacks/04-event-sourcing-consensus.md) | 313 |
| 40 | [Research Report: Continuation — 10 New Domains Bey](docs/technology-combinations/research-reports/continuation-10-domains.md) | 316 |
| 41 | [Research Report: Sozialrecht (35 комбинаций)](docs/technology-combinations/research-reports/sozialrecht-35-combinations.md) | 222 |
| 42 | [Сводная таблица 1–8](docs/technology-combinations/synthesis-tables/01-08-summary.md) | 383 |
| 43 | [Сводная таблица 9–14 (Extended)](docs/technology-combinations/synthesis-tables/09-14-extended.md) | 195 |
| 44 | [Сводная таблица 15–19 (Extended)](docs/technology-combinations/synthesis-tables/15-19-extended.md) | 162 |
| 45 | [Сводная таблица 20–24 (Final 1–24)](docs/technology-combinations/synthesis-tables/20-24-final.md) | 212 |
| 46 | [Сводная таблица 25–30 (Complete 1–30)](docs/technology-combinations/synthesis-tables/25-30-extended.md) | 228 |
| 47 | [Сводная таблица 31–35 (Complete 1–35)](docs/technology-combinations/synthesis-tables/31-35-final.md) | 249 |


### 165. Svyazi 2.0 — Архитектура системы
_Файл: `docs/SITEMAP.md` | 3 колонок, 5 строк_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Контакт: [Имя / Проект]](docs/templates/contact-outreach.md) | 133 |
| 2 | [ADR: [Название решения]](docs/templates/decision-record.md) | 94 |
| 3 | [Ансамбль: [Название]](docs/templates/ensemble.md) | 122 |
| 4 | [[Название компонента]](docs/templates/project-component.md) | 116 |
| 5 | [[Тема исследования]](docs/templates/research-note.md) | 80 |


### 166. Категории
_Файл: `docs/SOURCE_MAP.md` | 2 колонок, 3 строк_

| Категория | Файлов |
|-----------|--------|
| 🤖 Авто-импорт | 846 |
| ✍️ Ручной | 308 |
| 🤖 Bot-коммит | 10 |


### 167. Авторы
_Файл: `docs/SOURCE_MAP.md` | 2 колонок, 2 строк_

| Автор | Файлов |
|-------|--------|
| Claude | 1154 |
| github-actions[bot] | 10 |


### 168. 🤖 Авто-импортированные файлы (846)
_Файл: `docs/SOURCE_MAP.md` | 3 колонок, 846 строк_

| Файл | Слов | Первый коммит |
|------|------|--------------|
| `docs/01-svyazi/00-intro-part2.md` | 6 | 2026-04-29 |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 16 | 2026-04-29 |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 23 | 2026-04-29 |
| `docs/02-anthropic-vacancies/31-content-overview.md` | 39 | 2026-04-29 |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 41 | 2026-04-29 |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | 45 | 2026-04-29 |
| `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` | 45 | 2026-04-29 |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 46 | 2026-04-29 |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 46 | 2026-04-29 |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 47 | 2026-04-29 |
| `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` | 47 | 2026-04-29 |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 48 | 2026-04-29 |
| `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` | 49 | 2026-04-29 |
| `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` | 65 | 2026-04-29 |
| `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` | 65 | 2026-04-29 |
| `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | 65 | 2026-04-29 |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | 68 | 2026-04-29 |
| `docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md` | 72 | 2026-04-29 |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | 73 | 2026-04-29 |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | 74 | 2026-04-29 |
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | 75 | 2026-04-29 |
| `docs/lorenzo-agent/00-intro.md` | 78 | 2026-04-29 |
| `docs/02-anthropic-vacancies/35-passports-info1-md.md` | 79 | 2026-04-29 |
| `docs/02-anthropic-vacancies/62-author-contact.md` | 79 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/16-people.md` | 79 | 2026-04-29 |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | 81 | 2026-04-29 |
| `docs/02-anthropic-vacancies/42-author-contact.md` | 81 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/13-communications.md` | 81 | 2026-04-29 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 82 | 2026-04-29 |
| `docs/02-anthropic-vacancies/55-passports-meta-md.md` | 82 | 2026-04-29 |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 83 | 2026-04-29 |
| `docs/02-anthropic-vacancies/16-history.md` | 85 | 2026-04-29 |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 85 | 2026-04-29 |
| `docs/02-anthropic-vacancies/45-passports-pro2-md.md` | 85 | 2026-04-29 |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | 86 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/14-public-policy.md` | 88 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/15-public-benefit.md` | 88 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/12-technical-program-management.md` | 90 | 2026-04-29 |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | 91 | 2026-04-29 |
| `docs/02-anthropic-vacancies/25-13-reference-implementation.md` | 92 | 2026-04-29 |
| `docs/02-anthropic-vacancies/65-readme-md.md` | 93 | 2026-04-29 |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | 94 | 2026-04-29 |
| `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` | 95 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/17-appendix-b-change-log.md` | 95 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/04-security.md` | 96 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/09-product-management-support-ops.md` | 96 | 2026-04-29 |
| `docs/02-anthropic-vacancies/41-compatibility-level.md` | 97 | 2026-04-29 |
| `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` | 97 | 2026-04-29 |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | 98 | 2026-04-29 |
| `docs/02-anthropic-vacancies/190-содержание.md` | 98 | 2026-04-29 |
| `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` | 98 | 2026-04-29 |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | 100 | 2026-04-29 |
| `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` | 100 | 2026-04-29 |
| `docs/02-anthropic-vacancies/52-author-contact.md` | 100 | 2026-04-29 |
| `docs/02-anthropic-vacancies/61-compatibility-level.md` | 100 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/11-legal.md` | 100 | 2026-04-29 |
| `docs/nautilus/review-methodology/15-appendix-c-history.md` | 100 | 2026-04-29 |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | 101 | 2026-04-29 |
| `docs/02-anthropic-vacancies/51-compatibility-level.md` | 101 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/10-compute.md` | 101 | 2026-04-29 |
| `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` | 104 | 2026-04-29 |
| `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` | 106 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/05-marketing-brand.md` | 107 | 2026-04-29 |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | 108 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md` | 108 | 2026-04-29 |
| `docs/02-anthropic-vacancies/169-table-of-contents.md` | 109 | 2026-04-29 |
| `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` | 109 | 2026-04-29 |
| `docs/02-anthropic-vacancies/231-содержание.md` | 109 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/06-engineering-design-product.md` | 109 | 2026-04-29 |
| `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` | 110 | 2026-04-29 |
| `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` | 110 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/08-safeguards-trust-safety.md` | 111 | 2026-04-29 |
| `docs/02-anthropic-vacancies/326-содержание.md` | 113 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/03-finance.md` | 113 | 2026-04-29 |
| `docs/02-anthropic-vacancies/49-angle-perspective.md` | 114 | 2026-04-29 |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 115 | 2026-04-29 |
| `docs/02-anthropic-vacancies/211-table-of-contents.md` | 116 | 2026-04-29 |
| `docs/02-anthropic-vacancies/43-history.md` | 119 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/00-abstract.md` | 119 | 2026-04-29 |
| `docs/02-anthropic-vacancies/253-table-of-contents.md` | 120 | 2026-04-29 |
| `docs/02-anthropic-vacancies/46-essence.md` | 120 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/13-reference-implementation.md` | 120 | 2026-04-29 |
| `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` | 122 | 2026-04-29 |
| `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` | 123 | 2026-04-29 |
| `docs/02-anthropic-vacancies/59-angle-perspective.md` | 124 | 2026-04-29 |
| `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` | 125 | 2026-04-29 |
| `docs/02-anthropic-vacancies/308-table-of-contents.md` | 125 | 2026-04-29 |
| `docs/02-anthropic-vacancies/39-angle-perspective.md` | 125 | 2026-04-29 |
| `docs/02-anthropic-vacancies/04-abstract.md` | 126 | 2026-04-29 |
| `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` | 126 | 2026-04-29 |
| `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` | 126 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/01-ai-research-engineering.md` | 126 | 2026-04-29 |
| `docs/02-anthropic-vacancies/106-tl-dr.md` | 128 | 2026-04-29 |
| `docs/02-anthropic-vacancies/36-essence.md` | 128 | 2026-04-29 |
| `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` | 129 | 2026-04-29 |
| `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` | 130 | 2026-04-29 |
| `docs/02-anthropic-vacancies/38-content-overview.md` | 131 | 2026-04-29 |
| `docs/02-anthropic-vacancies/60-bridges.md` | 131 | 2026-04-29 |
| `docs/lorenzo-agent/16-vsegda-delaesh.md` | 131 | 2026-04-29 |
| `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` | 132 | 2026-04-29 |
| `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` | 133 | 2026-04-29 |
| `docs/lorenzo-agent/17-honestly-ne-znaesh.md` | 133 | 2026-04-29 |
| `docs/02-anthropic-vacancies/244-благодарности.md` | 135 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md` | 135 | 2026-04-29 |
| `docs/lorenzo-agent/18-escalate-to-max.md` | 135 | 2026-04-29 |
| `docs/02-anthropic-vacancies/128-доступные-инструменты.md` | 136 | 2026-04-29 |
| `docs/02-anthropic-vacancies/63-history.md` | 136 | 2026-04-29 |
| `docs/05-habr-projects/01-synthesis.md` | 136 | 2026-04-29 |
| `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` | 138 | 2026-04-29 |
| `docs/02-anthropic-vacancies/47-native-format.md` | 139 | 2026-04-29 |
| `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` | 139 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md` | 139 | 2026-04-29 |
| `docs/nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md` | 139 | 2026-04-29 |
| `docs/02-anthropic-vacancies/56-essence.md` | 140 | 2026-04-29 |
| `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` | 141 | 2026-04-29 |
| `docs/02-anthropic-vacancies/53-history.md` | 141 | 2026-04-29 |
| `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` | 141 | 2026-04-29 |
| `docs/02-anthropic-vacancies/58-content-overview.md` | 142 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/04-claude-subagents-patterns.md` | 142 | 2026-04-29 |
| `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` | 143 | 2026-04-29 |
| `docs/nautilus/review-methodology/14-main-technical-risks.md` | 143 | 2026-04-29 |
| `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` | 144 | 2026-04-29 |
| `docs/02-anthropic-vacancies/57-native-format.md` | 144 | 2026-04-29 |
| `docs/02-anthropic-vacancies/126-установка.md` | 145 | 2026-04-29 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/04-pluses-as-business.md` | 145 | 2026-04-29 |
| `docs/anthropic-vacancies/clusters/02-sales.md` | 146 | 2026-04-29 |
| `docs/lorenzo-agent/phased-deployment/06-level-5-full-network.md` | 146 | 2026-04-29 |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | 148 | 2026-04-29 |
| `docs/02-anthropic-vacancies/345-кто-ты.md` | 149 | 2026-04-29 |
| `docs/02-anthropic-vacancies/48-content-overview.md` | 149 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md` | 149 | 2026-04-29 |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 150 | 2026-04-29 |
| `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` | 150 | 2026-04-29 |
| `docs/02-anthropic-vacancies/224-acknowledgments.md` | 150 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md` | 150 | 2026-04-29 |
| `docs/lorenzo-agent/04-komu-ty-sluzhish.md` | 150 | 2026-04-29 |
| `docs/lorenzo-agent/09-voobshche-nelzya.md` | 150 | 2026-04-29 |
| `docs/02-anthropic-vacancies/338-ссылки.md` | 151 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md` | 151 | 2026-04-29 |
| `docs/anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md` | 151 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md` | 151 | 2026-04-29 |
| `docs/02-anthropic-vacancies/320-references.md` | 153 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/00-abstract.md` | 153 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/16-mcp-extension.md` | 154 | 2026-04-29 |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 155 | 2026-04-29 |
| `docs/lorenzo-agent/01-kto-ty.md` | 156 | 2026-04-29 |
| `docs/lorenzo-agent/08-bez-max-approval.md` | 156 | 2026-04-29 |
| `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` | 157 | 2026-04-29 |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 157 | 2026-04-29 |
| `docs/nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md` | 157 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/10-query-result.md` | 157 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md` | 158 | 2026-04-29 |
| `docs/lorenzo-agent/20-experiment.md` | 158 | 2026-04-29 |
| `docs/03-technology-combinations/04-sozialrecht-domain.md` | 160 | 2026-04-29 |
| `docs/lorenzo-agent/03-tvoya-missiya.md` | 160 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md` | 162 | 2026-04-29 |
| `docs/technology-combinations/synthesis-tables/15-19-extended.md` | 162 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md` | 163 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/09-difference-4-institutional-vision.md` | 163 | 2026-04-29 |
| `docs/lorenzo-agent/07-chto-mozhesh.md` | 163 | 2026-04-29 |
| `docs/technology-combinations/combinations/13-legal-document-transpiler.md` | 164 | 2026-04-29 |
| `docs/02-anthropic-vacancies/301-благодарности.md` | 165 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md` | 165 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/10-difference-5-tool-vs-mission-drift.md` | 165 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/02-vshe-scientific-networking.md` | 165 | 2026-04-29 |
| `docs/nautilus/npp-humanitarian-extension/03-what-doesnt-exist-on-market.md` | 165 | 2026-04-29 |
| `docs/technology-combinations/combinations/12-multi-agent-observability-stack.md` | 165 | 2026-04-29 |
| `docs/02-anthropic-vacancies/50-bridges.md` | 166 | 2026-04-29 |
| `docs/02-anthropic-vacancies/40-bridges.md` | 167 | 2026-04-29 |
| `docs/lorenzo-agent/19-persistent-character.md` | 168 | 2026-04-29 |
| `docs/02-anthropic-vacancies/182-acknowledgments.md` | 169 | 2026-04-29 |
| `docs/02-anthropic-vacancies/203-благодарности.md` | 169 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md` | 169 | 2026-04-29 |
| `docs/lorenzo-agent/phased-deployment/00-overview.md` | 169 | 2026-04-29 |
| `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` | 170 | 2026-04-29 |
| `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` | 170 | 2026-04-29 |
| `docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md` | 171 | 2026-04-29 |
| `docs/ai-collaborations/continuation/10-architecture-rfc.md` | 172 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md` | 172 | 2026-04-29 |
| `docs/anthropic-vacancies/extra-collaborator-findings/07-key-observation.md` | 172 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md` | 172 | 2026-04-29 |
| `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` | 173 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md` | 173 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md` | 173 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/12-versioning-policy.md` | 173 | 2026-04-29 |
| `docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md` | 173 | 2026-04-29 |
| `docs/02-anthropic-vacancies/130-отладка.md` | 174 | 2026-04-29 |
| `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` | 174 | 2026-04-29 |
| `docs/02-anthropic-vacancies/346-твоё-происхождение.md` | 174 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md` | 174 | 2026-04-29 |
| `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` | 175 | 2026-04-29 |
| `docs/02-anthropic-vacancies/24-12-versioning-policy.md` | 175 | 2026-04-29 |
| `docs/lorenzo-agent/15-anti-patterns.md` | 175 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-vs-camel/01-passive-vs-active-roles.md` | 176 | 2026-04-29 |
| `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` | 177 | 2026-04-29 |
| `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` | 177 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md` | 177 | 2026-04-29 |
| `docs/lorenzo-agent/02-tvoyo-proishozhdenie.md` | 177 | 2026-04-29 |
| `docs/lorenzo-agent/scenarios/00-question-scenario.md` | 177 | 2026-04-29 |
| `docs/technology-combinations/combinations/34-distributed-event-store-with-paxos.md` | 177 | 2026-04-29 |
| `docs/02-anthropic-vacancies/37-native-format.md` | 178 | 2026-04-29 |
| `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` | 179 | 2026-04-29 |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 179 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md` | 179 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md` | 179 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md` | 179 | 2026-04-29 |
| `docs/lorenzo-agent/phased-deployment/01-level-0-manual.md` | 179 | 2026-04-29 |
| `docs/02-anthropic-vacancies/21-9-query-flow.md` | 180 | 2026-04-29 |
| `docs/lorenzo-agent/operationalized/03-honest-opinion.md` | 180 | 2026-04-29 |
| `docs/technology-combinations/combinations/09-agent-orchestration-stack.md` | 180 | 2026-04-29 |
| `docs/technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md` | 181 | 2026-04-29 |
| `docs/02-anthropic-vacancies/93-18-reference-implementation.md` | 182 | 2026-04-29 |
| `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` | 182 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/09-query-flow.md` | 182 | 2026-04-29 |
| `docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md` | 182 | 2026-04-29 |
| `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` | 183 | 2026-04-29 |
| `docs/lorenzo-agent/phased-deployment/05-level-4-extended-mature.md` | 183 | 2026-04-29 |
| `docs/technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md` | 183 | 2026-04-29 |
| `docs/technology-combinations/combinations/23-security-first-code-review-pipeline.md` | 183 | 2026-04-29 |
| `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` | 184 | 2026-04-29 |
| `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` | 185 | 2026-04-29 |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | 185 | 2026-04-29 |
| `docs/lorenzo-agent/phased-deployment/07-progression-logic.md` | 185 | 2026-04-29 |
| `docs/lorenzo-agent/14-other-ai-relationships.md` | 186 | 2026-04-29 |
| `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` | 187 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/05-quaternary-developer-education.md` | 187 | 2026-04-29 |
| `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` | 189 | 2026-04-29 |
| `docs/02-anthropic-vacancies/356-твой-workflow.md` | 189 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md` | 189 | 2026-04-29 |
| `docs/02-anthropic-vacancies/146-acknowledgments.md` | 190 | 2026-04-29 |
| `docs/02-anthropic-vacancies/286-acknowledgments.md` | 190 | 2026-04-29 |
| `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` | 190 | 2026-04-29 |
| `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` | 190 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md` | 190 | 2026-04-29 |
| `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` | 191 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/00-intro.md` | 191 | 2026-04-29 |
| `docs/nautilus/review-methodology/00-tldr.md` | 191 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/09-federated-platform.md` | 192 | 2026-04-29 |
| `docs/lorenzo-agent/11-dhlab-documents.md` | 192 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/14-sdk.md` | 192 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md` | 193 | 2026-04-29 |
| `docs/02-anthropic-vacancies/300-заключение.md` | 194 | 2026-04-29 |
| `docs/ai-collaborations/candidates/02-related-projects-context.md` | 194 | 2026-04-29 |
| `docs/technology-combinations/synthesis-tables/09-14-extended.md` | 195 | 2026-04-29 |
| `docs/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md` | 196 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md` | 197 | 2026-04-29 |
| `docs/nautilus/multi-tier-architecture/00-question-multi-tier.md` | 197 | 2026-04-29 |
| `docs/nautilus/review-methodology/07-why-valid-for-ai.md` | 197 | 2026-04-29 |
| `docs/technology-combinations/combinations/22-russian-international-oss-stack.md` | 197 | 2026-04-29 |
| `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` | 198 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/11-security-considerations.md` | 198 | 2026-04-29 |
| `docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md` | 198 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md` | 200 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md` | 200 | 2026-04-29 |
| `docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md` | 200 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/14-adr-001-federation-over-merging.md` | 202 | 2026-04-29 |
| `docs/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md` | 202 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/11-relevance-ranking.md` | 203 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md` | 204 | 2026-04-29 |
| `docs/technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md` | 204 | 2026-04-29 |
| `docs/ai-collaborations/continuation/06-metrics-tree.md` | 205 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/06-platform-for-professional-communities.md` | 205 | 2026-04-29 |
| `docs/lorenzo-agent/specification/00-context-fundamental-questions.md` | 205 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md` | 205 | 2026-04-29 |
| `docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md` | 205 | 2026-04-29 |
| `docs/02-anthropic-vacancies/349-твоя-личность.md` | 206 | 2026-04-29 |
| `docs/lorenzo-agent/06-yazyki-kultura.md` | 206 | 2026-04-29 |
| `docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md` | 206 | 2026-04-29 |
| `docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md` | 207 | 2026-04-29 |
| `docs/lorenzo-agent/specification/08-q8-other-ai-relationships.md` | 207 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/09-acknowledgments.md` | 208 | 2026-04-29 |
| `docs/habr-unique-projects/key-findings/02-memnet.md` | 209 | 2026-04-29 |
| `docs/technology-combinations/combinations/17-distributed-agent-memory-with-graph.md` | 209 | 2026-04-29 |
| `docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md` | 209 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/20-adr-002-q6-first-class.md` | 210 | 2026-04-29 |
| `docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md` | 210 | 2026-04-29 |
| `docs/technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md` | 210 | 2026-04-29 |
| `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` | 211 | 2026-04-29 |
| `docs/lorenzo-agent/specification/09-q9-geographic-linguistic-scope.md` | 211 | 2026-04-29 |
| `docs/technology-combinations/mega-stacks/01-legal-ai-stack.md` | 211 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md` | 212 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/18-reference-implementation.md` | 212 | 2026-04-29 |
| `docs/technology-combinations/synthesis-tables/20-24-final.md` | 212 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md` | 213 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/12-closing.md` | 213 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/00-abstract-status.md` | 213 | 2026-04-29 |
| `docs/lorenzo-agent/specification/06-q6-accountability.md` | 214 | 2026-04-29 |
| `docs/nautilus/review-methodology/12-appendix-a-header-warning.md` | 214 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md` | 215 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md` | 216 | 2026-04-29 |
| `docs/lorenzo-agent/specification/07-q7-success-metrics.md` | 216 | 2026-04-29 |
| `docs/nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md` | 216 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/11-pluses-of-hermes.md` | 217 | 2026-04-29 |
| `docs/lorenzo-agent/12-workflow.md` | 218 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md` | 218 | 2026-04-29 |
| `docs/nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md` | 219 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md` | 221 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md` | 221 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/05-compatibility-levels.md` | 221 | 2026-04-29 |
| `docs/lorenzo-agent/phased-deployment/04-level-3-medium-active.md` | 222 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/07-portal-entry.md` | 224 | 2026-04-29 |
| `docs/nautilus/review-methodology/11-application-plan-current-docs.md` | 225 | 2026-04-29 |
| `docs/lorenzo-agent/13-outreach-communication.md` | 226 | 2026-04-29 |
| `docs/technology-combinations/mega-stacks/03-dsl-ast.md` | 226 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/05-hw-nl2workflow.md` | 227 | 2026-04-29 |
| `docs/nautilus/community-discussions/practical-observations/00-question-practical.md` | 227 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/17-versioning-policy.md` | 227 | 2026-04-29 |
| `docs/lorenzo-agent/specification/03-q3-what-lorenzo-does.md` | 228 | 2026-04-29 |
| `docs/lorenzo-agent/specification/05-q5-authority-limits.md` | 228 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/10-query-flow.md` | 228 | 2026-04-29 |
| `docs/technology-combinations/synthesis-tables/25-30-extended.md` | 228 | 2026-04-29 |
| `docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md` | 229 | 2026-04-29 |
| `docs/technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md` | 230 | 2026-04-29 |
| `docs/technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md` | 233 | 2026-04-29 |
| `docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md` | 235 | 2026-04-29 |
| `docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md` | 236 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md` | 237 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/04-passport.md` | 237 | 2026-04-29 |
| `docs/lorenzo-agent/naming/00-question-lorenzo-codename.md` | 238 | 2026-04-29 |
| `docs/lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md` | 238 | 2026-04-29 |
| `docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md` | 240 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md` | 241 | 2026-04-29 |
| `docs/lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md` | 241 | 2026-04-29 |
| `docs/anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md` | 242 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md` | 244 | 2026-04-29 |
| `docs/technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md` | 244 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md` | 247 | 2026-04-29 |
| `docs/technology-combinations/synthesis-tables/31-35-final.md` | 249 | 2026-04-29 |
| `docs/ai-collaborations/continuation/09-do-not-glue.md` | 250 | 2026-04-29 |
| `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` | 251 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md` | 251 | 2026-04-29 |
| `docs/ai-collaborations/continuation/08-commercialization-three-paths.md` | 252 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/00-context.md` | 252 | 2026-04-29 |
| `docs/habr-unique-projects/key-findings/01-yodoca.md` | 252 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/03-revised-anthropic-mapping.md` | 253 | 2026-04-29 |
| `docs/lorenzo-agent/05-tvoya-lichnost.md` | 253 | 2026-04-29 |
| `docs/technology-combinations/combinations/16-adversarial-multi-agent-code-review.md` | 254 | 2026-04-29 |
| `docs/nautilus/review-methodology/08-implementation-nautilus.md` | 257 | 2026-04-29 |
| `docs/nautilus/review-methodology/05-conditions-of-applicability.md` | 258 | 2026-04-29 |
| `docs/02-anthropic-vacancies/74-abstract.md` | 259 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md` | 260 | 2026-04-29 |
| `docs/lorenzo-agent/specification/10-q10-funding-model.md` | 260 | 2026-04-29 |
| `docs/05-habr-projects/02-collaboration-partners.md` | 261 | 2026-04-29 |
| `docs/02-anthropic-vacancies/23-11-security-considerations.md` | 263 | 2026-04-29 |
| `docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md` | 264 | 2026-04-29 |
| `docs/02-anthropic-vacancies/285-closing.md` | 265 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/01-zachem-dokument.md` | 265 | 2026-04-29 |
| `docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md` | 266 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/02-three-overlapping-identities.md` | 266 | 2026-04-29 |
| `docs/habr-unique-projects/key-findings/04-dochkina-sequential.md` | 266 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/08-consensus-algorithm.md` | 266 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/02-terminology.md` | 267 | 2026-04-29 |
| `docs/02-anthropic-vacancies/181-12-closing.md` | 268 | 2026-04-29 |
| `docs/nautilus/privacy-federation/01-what-to-anonymize-german-standard.md` | 269 | 2026-04-29 |
| `docs/02-anthropic-vacancies/111-4-условия-применимости.md` | 272 | 2026-04-29 |
| `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` | 272 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/15-glossary.md` | 272 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md` | 273 | 2026-04-29 |
| `docs/anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md` | 274 | 2026-04-29 |
| `docs/anthropic-vacancies/extra-collaborator-findings/01-coally.md` | 275 | 2026-04-29 |
| `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` | 276 | 2026-04-29 |
| `docs/02-anthropic-vacancies/92-17-versioning-policy.md` | 276 | 2026-04-29 |
| `docs/02-anthropic-vacancies/85-10-query-flow.md` | 277 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/10-references.md` | 278 | 2026-04-29 |
| `docs/02-anthropic-vacancies/287-references.md` | 281 | 2026-04-29 |
| `docs/nautilus/review-methodology/04-fallback-ratio-question.md` | 281 | 2026-04-29 |
| `docs/nautilus/review-methodology/13-appendix-b-examples.md` | 281 | 2026-04-29 |
| `docs/02-anthropic-vacancies/302-ссылки.md` | 282 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/10-profession-specific-workflows.md` | 282 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md` | 284 | 2026-04-29 |
| `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` | 285 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md` | 286 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/15-security.md` | 288 | 2026-04-29 |
| `docs/nautilus/privacy-federation/00-question-anonymization.md` | 288 | 2026-04-29 |
| `docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md` | 290 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/07-portal-entry.md` | 290 | 2026-04-29 |
| `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` | 291 | 2026-04-29 |
| `docs/anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md` | 291 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/12-minuses-of-hermes.md` | 291 | 2026-04-29 |
| `docs/lorenzo-agent/specification/04-q4-character.md` | 292 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/04-passport.md` | 294 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md` | 295 | 2026-04-29 |
| `docs/lorenzo-agent/naming/01-search-results-not-found.md` | 295 | 2026-04-29 |
| `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` | 297 | 2026-04-29 |
| `docs/03-technology-combinations/01-agent-routing.md` | 298 | 2026-04-29 |
| `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` | 300 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md` | 300 | 2026-04-29 |
| `docs/anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md` | 301 | 2026-04-29 |
| `docs/02-anthropic-vacancies/07-2-terminology.md` | 302 | 2026-04-29 |
| `docs/nautilus/npp-humanitarian-extension/00-question-can-it-apply-to-docs.md` | 302 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/05-compatibility-levels.md` | 302 | 2026-04-29 |
| `docs/02-anthropic-vacancies/204-ссылки.md` | 303 | 2026-04-29 |
| `docs/nautilus/review-methodology/10-checklist.md` | 303 | 2026-04-29 |
| `docs/lorenzo-agent/10-collaborators-landscape.md` | 305 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md` | 305 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/02-why-document-exists.md` | 305 | 2026-04-29 |
| `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` | 306 | 2026-04-29 |
| `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` | 307 | 2026-04-29 |
| `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` | 309 | 2026-04-29 |
| `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` | 309 | 2026-04-29 |
| `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` | 309 | 2026-04-29 |
| `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` | 310 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/11-call-for-collaboration.md` | 310 | 2026-04-29 |
| `docs/02-anthropic-vacancies/183-references.md` | 311 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/10-rekomendatsii.md` | 311 | 2026-04-29 |
| `docs/02-anthropic-vacancies/267-acknowledgments.md` | 313 | 2026-04-29 |
| `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` | 313 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/01-introduction.md` | 313 | 2026-04-29 |
| `docs/technology-combinations/mega-stacks/04-event-sourcing-consensus.md` | 313 | 2026-04-29 |
| `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` | 314 | 2026-04-29 |
| `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` | 315 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/07-rekursivnoe-prozrenie.md` | 315 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/02-dvukhsloynyy-stek.md` | 316 | 2026-04-29 |
| `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` | 317 | 2026-04-29 |
| `docs/02-anthropic-vacancies/245-ссылки.md` | 318 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/04-pochemu-ne-postroeno.md` | 318 | 2026-04-29 |
| `docs/technology-combinations/mega-stacks/02-ultimate-legal-ai.md` | 318 | 2026-04-29 |
| `docs/02-anthropic-vacancies/307-abstract.md` | 319 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md` | 319 | 2026-04-29 |
| `docs/nautilus/privacy-federation/04-what-i-can-do-now.md` | 322 | 2026-04-29 |
| `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` | 325 | 2026-04-29 |
| `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` | 326 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/08-recursive-insight.md` | 326 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/11-practical-recommendations.md` | 326 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md` | 327 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/06-adapter-interface.md` | 327 | 2026-04-29 |
| `docs/02-anthropic-vacancies/325-аннотация.md` | 328 | 2026-04-29 |
| `docs/nautilus/review-methodology/06-relation-existing-methodologies.md` | 333 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/06-adapter-interface.md` | 334 | 2026-04-29 |
| `docs/ai-collaborations/candidates/01-three-key-candidates.md` | 335 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/00-abstract-status.md` | 335 | 2026-04-29 |
| `docs/02-anthropic-vacancies/230-аннотация.md` | 336 | 2026-04-29 |
| `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` | 336 | 2026-04-29 |
| `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` | 338 | 2026-04-29 |
| `docs/02-anthropic-vacancies/168-abstract.md` | 338 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md` | 339 | 2026-04-29 |
| `docs/02-anthropic-vacancies/147-references.md` | 340 | 2026-04-29 |
| `docs/02-anthropic-vacancies/225-references.md` | 340 | 2026-04-29 |
| `docs/02-anthropic-vacancies/275-why-this-document-exists.md` | 341 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md` | 341 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md` | 342 | 2026-04-29 |
| `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` | 343 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/03-registry.md` | 343 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/09-consensus-algorithm.md` | 343 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/05-why-not-built.md` | 344 | 2026-04-29 |
| `docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md` | 346 | 2026-04-29 |
| `docs/lorenzo-agent/specification/01-q1-what-lorenzo-is.md` | 348 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/12-call-for-collaboration.md` | 350 | 2026-04-29 |
| `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` | 352 | 2026-04-29 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/02-existing-niche.md` | 352 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/03-two-layer-stack.md` | 352 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/10-otkrytye-voprosy.md` | 353 | 2026-04-29 |
| `docs/habr-unique-projects/analogues/02-related-projects.md` | 354 | 2026-04-29 |
| `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` | 355 | 2026-04-29 |
| `docs/02-anthropic-vacancies/189-аннотация.md` | 356 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md` | 357 | 2026-04-29 |
| `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` | 358 | 2026-04-29 |
| `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` | 358 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/10-open-questions.md` | 358 | 2026-04-29 |
| `docs/02-anthropic-vacancies/337-благодарности.md` | 360 | 2026-04-29 |
| `docs/ai-collaborations/continuation/05-roadmap-6-12-months.md` | 360 | 2026-04-29 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/01-why-stronger-than-it-looks.md` | 360 | 2026-04-29 |
| `docs/02-anthropic-vacancies/210-abstract.md` | 361 | 2026-04-29 |
| `docs/nautilus/review-methodology/01-context-motivation.md` | 361 | 2026-04-29 |
| `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` | 362 | 2026-04-29 |
| `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` | 363 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md` | 364 | 2026-04-29 |
| `docs/02-anthropic-vacancies/252-abstract.md` | 365 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/10-open-questions.md` | 367 | 2026-04-29 |
| `docs/02-anthropic-vacancies/153-executive-summary.md` | 369 | 2026-04-29 |
| `docs/02-anthropic-vacancies/268-references.md` | 369 | 2026-04-29 |
| `docs/habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md` | 369 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/02-terminology.md` | 371 | 2026-04-29 |
| `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` | 372 | 2026-04-29 |
| `docs/02-anthropic-vacancies/281-the-recursive-insight.md` | 373 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/07-prakticheskie-shagi.md` | 373 | 2026-04-29 |
| `docs/nautilus/review-methodology/09-limitations-open-questions.md` | 373 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/07-practical-first-steps.md` | 374 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/06-utochnyonnyy-obyom-ingit.md` | 374 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/11-call-for-collaboration.md` | 374 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md` | 377 | 2026-04-29 |
| `docs/02-anthropic-vacancies/243-12-заключение.md` | 378 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md` | 378 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/06-refined-ingit-scope.md` | 378 | 2026-04-29 |
| `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` | 379 | 2026-04-29 |
| `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` | 379 | 2026-04-29 |
| `docs/01-svyazi/08-conclusions.md` | 380 | 2026-04-29 |
| `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` | 380 | 2026-04-29 |
| `docs/02-anthropic-vacancies/90-15-security-considerations.md` | 380 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md` | 381 | 2026-04-29 |
| `docs/02-anthropic-vacancies/136-abstract.md` | 382 | 2026-04-29 |
| `docs/ai-collaborations/continuation/02-agentops-trace-envelope.md` | 382 | 2026-04-29 |
| `docs/02-anthropic-vacancies/06-1-introduction.md` | 383 | 2026-04-29 |
| `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` | 383 | 2026-04-29 |
| `docs/anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md` | 383 | 2026-04-29 |
| `docs/nautilus/okwf-concept/00-abstract.md` | 383 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/07-upravlenie-nadzor.md` | 383 | 2026-04-29 |
| `docs/technology-combinations/synthesis-tables/01-08-summary.md` | 383 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/07-governance-oversight.md` | 385 | 2026-04-29 |
| `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` | 389 | 2026-04-29 |
| `docs/02-anthropic-vacancies/319-acknowledgments.md` | 390 | 2026-04-29 |
| `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` | 393 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/12-concrete-next-step.md` | 395 | 2026-04-29 |
| `docs/02-anthropic-vacancies/77-2-terminology.md` | 396 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/00-abstract.md` | 398 | 2026-04-29 |
| `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` | 399 | 2026-04-29 |
| `docs/02-anthropic-vacancies/81-6-adapter-interface.md` | 401 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md` | 401 | 2026-04-29 |
| `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` | 402 | 2026-04-29 |
| `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` | 402 | 2026-04-29 |
| `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` | 403 | 2026-04-29 |
| `docs/habr-unique-projects/analogues/01-three-direct-analogues.md` | 403 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/00-abstract.md` | 407 | 2026-04-29 |
| `docs/nautilus/review-methodology/02-formal-workflow.md` | 407 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/08-q6-space.md` | 415 | 2026-04-29 |
| `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` | 416 | 2026-04-29 |
| `docs/03-technology-combinations/03-local-first.md` | 419 | 2026-04-29 |
| `docs/02-anthropic-vacancies/179-10-open-questions.md` | 420 | 2026-04-29 |
| `docs/02-anthropic-vacancies/223-12-closing.md` | 423 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md` | 424 | 2026-04-29 |
| `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` | 426 | 2026-04-29 |
| `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` | 426 | 2026-04-29 |
| `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` | 426 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/00-abstract.md` | 426 | 2026-04-29 |
| `docs/ai-collaborations/continuation/01-shared-memory-between-agents.md` | 431 | 2026-04-29 |
| `docs/02-anthropic-vacancies/221-10-open-questions.md` | 432 | 2026-04-29 |
| `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` | 434 | 2026-04-29 |
| `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` | 435 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/00-question-two-nautiluses.md` | 436 | 2026-04-29 |
| `docs/02-anthropic-vacancies/266-13-closing.md` | 437 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/13-rest-api.md` | 437 | 2026-04-29 |
| `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` | 439 | 2026-04-29 |
| `docs/02-anthropic-vacancies/18-6-adapter-interface.md` | 440 | 2026-04-29 |
| `docs/lorenzo-agent/operationalized/04-recommendations.md` | 440 | 2026-04-29 |
| `docs/ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md` | 444 | 2026-04-29 |
| `docs/habr-unique-projects/extra-examples/00-question-habr-examples.md` | 444 | 2026-04-29 |
| `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` | 447 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/01-introduction.md` | 447 | 2026-04-29 |
| `docs/nautilus/supply-demand/00-question-supply-demand.md` | 447 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md` | 448 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/06-eticheskaya-ramka.md` | 448 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/12-onboarding-paths.md` | 449 | 2026-04-29 |
| `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` | 452 | 2026-04-29 |
| `docs/nautilus/npp-v1-0/18-comment-on-document.md` | 454 | 2026-04-29 |
| `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` | 455 | 2026-04-29 |
| `docs/nautilus/review-methodology/03-consolidation-principles.md` | 455 | 2026-04-29 |
| `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` | 459 | 2026-04-29 |
| `docs/nautilus/okwf-concept/09-call-for-partnership.md` | 460 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/05-priblizheniya.md` | 461 | 2026-04-29 |
| `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` | 463 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/06-ethical-framework.md` | 463 | 2026-04-29 |
| `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` | 464 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md` | 466 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/06-existing-approximations.md` | 466 | 2026-04-29 |
| `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` | 467 | 2026-04-29 |
| `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` | 467 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/11-open-questions.md` | 467 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/09-phased-rollout.md` | 469 | 2026-04-29 |
| `docs/04-ai-collaborations/07-выводы.md` | 470 | 2026-04-29 |
| `docs/lorenzo-agent/operationalized/01-pluses-1-7.md` | 470 | 2026-04-29 |
| `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` | 471 | 2026-04-29 |
| `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` | 474 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/03-registry.md` | 479 | 2026-04-29 |
| `docs/01-svyazi/02-methodology.md` | 480 | 2026-04-29 |
| `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` | 483 | 2026-04-29 |
| `docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md` | 483 | 2026-04-29 |
| `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` | 484 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md` | 484 | 2026-04-29 |
| `docs/nautilus/okwf-concept/06-governance-ethics.md` | 486 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/08-risks-mitigations.md` | 486 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/12-zaklyuchenie.md` | 489 | 2026-04-29 |
| `docs/technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md` | 489 | 2026-04-29 |
| `docs/02-anthropic-vacancies/76-1-introduction.md` | 494 | 2026-04-29 |
| `docs/nautilus/privacy-federation/02-two-tier-publication.md` | 498 | 2026-04-29 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/00-question-mmorpg-for-programmers.md` | 507 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md` | 511 | 2026-04-29 |
| `docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md` | 514 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md` | 516 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md` | 517 | 2026-04-29 |
| `docs/lorenzo-agent/operationalized/06-conclusion-deserves-attention.md` | 518 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/00-intro.md` | 520 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/12-closing.md` | 520 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md` | 540 | 2026-04-29 |
| `docs/nautilus/npp-humanitarian-extension/04-grant-opportunities.md` | 540 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/05-platform-not-position.md` | 542 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/09-risks-open-questions.md` | 542 | 2026-04-29 |
| `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` | 545 | 2026-04-29 |
| `docs/nautilus/transmission-box/00-question-mountain-to-person.md` | 549 | 2026-04-29 |
| `docs/02-anthropic-vacancies/294-существующие-приближения.md` | 554 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/09-riski-voprosy.md` | 558 | 2026-04-29 |
| `docs/technology-combinations/combinations/14-local-first-agent-development-environment.md` | 559 | 2026-04-29 |
| `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` | 560 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/08-riski-mery.md` | 573 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/04-symbiotic-architecture.md` | 574 | 2026-04-29 |
| `docs/04-ai-collaborations/01-executive-summary.md` | 575 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/08-implikatsii-nautilus-okwf.md` | 575 | 2026-04-29 |
| `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` | 576 | 2026-04-29 |
| `docs/nautilus/okwf-concept/05-economic-model.md` | 578 | 2026-04-29 |
| `docs/nautilus/okwf-concept/01-problem-statement.md` | 582 | 2026-04-29 |
| `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` | 584 | 2026-04-29 |
| `docs/lorenzo-agent/operationalized/05-anchor-node-habr-scout.md` | 584 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/13-acknowledgments-refs.md` | 586 | 2026-04-29 |
| `docs/02-anthropic-vacancies/264-11-open-questions.md` | 590 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/04-simbioticheskaya-arkhitektura.md` | 590 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/06-konkretnyy-sluchay.md` | 592 | 2026-04-29 |
| `docs/technology-combinations/combinations/24-mega-integration-full-stack.md` | 594 | 2026-04-29 |
| `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` | 595 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md` | 595 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/01-otkrytie-cowork.md` | 600 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md` | 601 | 2026-04-29 |
| `docs/lorenzo-agent/operationalized/00-overview-grandchild-combination.md` | 603 | 2026-04-29 |
| `docs/02-anthropic-vacancies/279-existing-approximations.md` | 604 | 2026-04-29 |
| `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` | 605 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/02-chto-cowork-obespechivaet.md` | 606 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/02-cowork-provides.md` | 607 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md` | 609 | 2026-04-29 |
| `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` | 610 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/09-svyaz-s-drugimi.md` | 611 | 2026-04-29 |
| `docs/02-anthropic-vacancies/175-6-ethical-framework.md` | 612 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-en/07-specific-case.md` | 614 | 2026-04-29 |
| `docs/nautilus/okwf-concept/07-phased-rollout.md` | 615 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/05-architectural-specification.md` | 618 | 2026-04-29 |
| `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` | 620 | 2026-04-29 |
| `docs/nautilus/infrastructure-layer-b-ru/12-blagodarnosti-ssylki.md` | 620 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/09-relationship-other-agents.md` | 620 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/03-what-makes-representative-agent.md` | 623 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-vs-camel/04-what-to-take-from-info-repos.md` | 626 | 2026-04-29 |
| `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` | 627 | 2026-04-29 |
| `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` | 628 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md` | 631 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/01-cowork-discovery.md` | 631 | 2026-04-29 |
| `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` | 632 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md` | 634 | 2026-04-29 |
| `docs/01-svyazi/14-limitations.md` | 638 | 2026-04-29 |
| `docs/02-anthropic-vacancies/155-1-problem-statement.md` | 638 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md` | 640 | 2026-04-29 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/05-minuses-as-business.md` | 642 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md` | 642 | 2026-04-29 |
| `docs/nautilus/okwf-concept/08-risk-analysis.md` | 643 | 2026-04-29 |
| `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` | 644 | 2026-04-29 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md` | 646 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/10-strategicheskoe-pozitsionirovanie.md` | 650 | 2026-04-29 |
| `docs/nautilus/okwf-concept/02-target-populations.md` | 650 | 2026-04-29 |
| `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` | 655 | 2026-04-29 |
| `docs/02-anthropic-vacancies/174-5-architectural-specification.md` | 656 | 2026-04-29 |
| `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` | 657 | 2026-04-29 |
| `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` | 658 | 2026-04-29 |
| `docs/02-anthropic-vacancies/159-5-economic-model.md` | 660 | 2026-04-29 |
| `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` | 663 | 2026-04-29 |
| `docs/nautilus/okwf-concept/03-why-existing-fail.md` | 663 | 2026-04-29 |
| `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` | 664 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md` | 664 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/13-closing.md` | 664 | 2026-04-29 |
| `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` | 665 | 2026-04-29 |
| `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` | 666 | 2026-04-29 |
| `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` | 668 | 2026-04-29 |
| `docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md` | 668 | 2026-04-29 |
| `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` | 669 | 2026-04-29 |
| `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` | 669 | 2026-04-29 |
| `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` | 670 | 2026-04-29 |
| `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` | 671 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md` | 672 | 2026-04-29 |
| `docs/technology-combinations/combinations/19-multi-agent-observability-platform.md` | 678 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/05-configuration-ensembles.md` | 681 | 2026-04-29 |
| `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` | 682 | 2026-04-29 |
| `docs/02-anthropic-vacancies/162-8-risk-analysis.md` | 685 | 2026-04-29 |
| `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` | 686 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/02-double-triangle-architecture.md` | 687 | 2026-04-29 |
| `docs/02-anthropic-vacancies/156-2-target-populations.md` | 689 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/05-ekonomika.md` | 689 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/09-okwf-integration.md` | 693 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/05-economics-replication.md` | 695 | 2026-04-29 |
| `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` | 699 | 2026-04-29 |
| `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` | 699 | 2026-04-29 |
| `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` | 699 | 2026-04-29 |
| `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` | 700 | 2026-04-29 |
| `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` | 703 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/07-application-domains.md` | 703 | 2026-04-29 |
| `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` | 704 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/08-call-to-action.md` | 704 | 2026-04-29 |
| `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` | 705 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md` | 713 | 2026-04-29 |
| `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` | 715 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/10-strategic-positioning.md` | 715 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/07-oblasti-primeneniya.md` | 716 | 2026-04-29 |
| `docs/01-svyazi/12-roadmap.md` | 722 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/07-economics-combinatorial.md` | 722 | 2026-04-29 |
| `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` | 723 | 2026-04-29 |
| `docs/01-svyazi/01-executive-summary.md` | 726 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/07-open-questions.md` | 726 | 2026-04-29 |
| `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` | 730 | 2026-04-29 |
| `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` | 731 | 2026-04-29 |
| `docs/02-anthropic-vacancies/145-8-call-to-action.md` | 732 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/10-risks.md` | 732 | 2026-04-29 |
| `docs/02-anthropic-vacancies/238-7-области-применения.md` | 734 | 2026-04-29 |
| `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` | 735 | 2026-04-29 |
| `docs/02-anthropic-vacancies/218-7-application-domains.md` | 736 | 2026-04-29 |
| `docs/01-svyazi/11-integration-contracts.md` | 737 | 2026-04-29 |
| `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` | 737 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/05-four-integration-paths.md` | 737 | 2026-04-29 |
| `docs/lorenzo-agent/operationalized/02-minuses-1-10.md` | 738 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/06-coordination-disagreement.md` | 742 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/05-chetyre-puti-integratsii.md` | 742 | 2026-04-29 |
| `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` | 748 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/04-sub-agent-registry.md` | 750 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md` | 751 | 2026-04-29 |
| `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` | 753 | 2026-04-29 |
| `docs/01-svyazi/09-architectural-gaps.md` | 758 | 2026-04-29 |
| `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` | 758 | 2026-04-29 |
| `docs/02-anthropic-vacancies/144-7-open-questions.md` | 759 | 2026-04-29 |
| `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` | 761 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md` | 762 | 2026-04-29 |
| `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` | 765 | 2026-04-29 |
| `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` | 778 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md` | 780 | 2026-04-29 |
| `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` | 781 | 2026-04-29 |
| `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` | 783 | 2026-04-29 |
| `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` | 787 | 2026-04-29 |
| `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` | 787 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md` | 787 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-en/03-ingit-provides.md` | 792 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/01-cinderella-syndrome.md` | 793 | 2026-04-29 |
| `docs/nautilus/okwf-concept/10-appendices.md` | 796 | 2026-04-29 |
| `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` | 800 | 2026-04-29 |
| `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` | 801 | 2026-04-29 |
| `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` | 802 | 2026-04-29 |
| `docs/03-technology-combinations/02-knowledge-graphs.md` | 802 | 2026-04-29 |
| `docs/01-svyazi/13-contacts.md` | 806 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md` | 806 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md` | 807 | 2026-04-29 |
| `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` | 812 | 2026-04-29 |
| `docs/nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md` | 812 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md` | 820 | 2026-04-29 |
| `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` | 821 | 2026-04-29 |
| `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` | 821 | 2026-04-29 |
| `docs/01-svyazi/06-security-privacy.md` | 823 | 2026-04-29 |
| `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` | 834 | 2026-04-29 |
| `docs/02-anthropic-vacancies/67-о-проекте.md` | 836 | 2026-04-29 |
| `docs/lorenzo-agent/phased-deployment/08-current-session-poc.md` | 839 | 2026-04-29 |
| `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` | 841 | 2026-04-29 |
| `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` | 842 | 2026-04-29 |
| `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` | 842 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/01-pyat-tipov.md` | 842 | 2026-04-29 |
| `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` | 846 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/04-architecture.md` | 847 | 2026-04-29 |
| `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` | 851 | 2026-04-29 |
| `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` | 853 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/01-five-type-typology.md` | 871 | 2026-04-29 |
| `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` | 873 | 2026-04-29 |
| `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` | 873 | 2026-04-29 |
| `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` | 874 | 2026-04-29 |
| `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` | 879 | 2026-04-29 |
| `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` | 883 | 2026-04-29 |
| `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` | 887 | 2026-04-29 |
| `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` | 888 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/03-what-makes-csa.md` | 889 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md` | 902 | 2026-04-29 |
| `docs/01-svyazi/10-second-order-ensembles.md` | 908 | 2026-04-29 |
| `docs/02-anthropic-vacancies/68-about.md` | 908 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md` | 909 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/02-historical-precedents.md` | 911 | 2026-04-29 |
| `docs/03-technology-combinations/05-benchmarks.md` | 915 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md` | 919 | 2026-04-29 |
| `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` | 923 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/08-pilot-sgb-advocate.md` | 925 | 2026-04-29 |
| `docs/anthropic-vacancies/hermes-comparison/13-reprioritization.md` | 930 | 2026-04-29 |
| `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` | 941 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents/08-seven-domains.md` | 948 | 2026-04-29 |
| `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` | 950 | 2026-04-29 |
| `docs/02-anthropic-vacancies/104-appendix-c-references.md` | 955 | 2026-04-29 |
| `docs/02-anthropic-vacancies/164-10-appendices.md` | 960 | 2026-04-29 |
| `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` | 961 | 2026-04-29 |
| `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` | 964 | 2026-04-29 |
| `docs/nautilus/okwf-concept/04-proposed-infrastructure.md` | 969 | 2026-04-29 |
| `docs/nautilus/review-methodology/16-glossary.md` | 971 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md` | 981 | 2026-04-29 |
| `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` | 984 | 2026-04-29 |
| `docs/nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md` | 1019 | 2026-04-29 |
| `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` | 1023 | 2026-04-29 |
| `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` | 1023 | 2026-04-29 |
| `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` | 1031 | 2026-04-29 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/03-why-natural-for-programmers.md` | 1044 | 2026-04-29 |
| `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` | 1057 | 2026-04-29 |
| `docs/01-svyazi/07-mvp-planning.md` | 1063 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/03-nautilus-B-meta-orchestrator.md` | 1105 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md` | 1110 | 2026-04-29 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/02-nautilus-A-pro2-meta.md` | 1126 | 2026-04-29 |
| `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` | 1130 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-ru/06-riski.md` | 1142 | 2026-04-29 |
| `docs/nautilus/professional-colleague-agents-en/06-risks.md` | 1153 | 2026-04-29 |
| `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` | 1183 | 2026-04-29 |
| `docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md` | 1183 | 2026-04-29 |
| `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` | 1192 | 2026-04-29 |
| `docs/01-svyazi/04-ensembles-overview.md` | 1288 | 2026-04-29 |
| `docs/02-anthropic-vacancies/122-глоссарий.md` | 1334 | 2026-04-29 |
| `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` | 1340 | 2026-04-29 |
| `docs/01-svyazi/03-component-catalog.md` | 1383 | 2026-04-29 |
| `docs/anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md` | 1390 | 2026-04-29 |
| `docs/lorenzo-agent/naming/03-dhlab-umbrella.md` | 1402 | 2026-04-29 |
| `docs/lorenzo-agent/specification/11-difficulties-and-recommendations.md` | 1408 | 2026-04-29 |
| `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` | 1475 | 2026-04-29 |
| `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` | 1478 | 2026-04-29 |
| `docs/nautilus/npp-v1-1/22-glossary.md` | 1486 | 2026-04-29 |
| `docs/nautilus/privacy-federation/03-what-this-gives-technically.md` | 1492 | 2026-04-29 |
| `docs/nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md` | 1525 | 2026-04-29 |
| `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` | 1552 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/04-ten-domains.md` | 1552 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md` | 1572 | 2026-04-29 |
| `docs/nautilus/double-triangle-architecture/11-glossary.md` | 1582 | 2026-04-29 |
| `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` | 1608 | 2026-04-29 |
| `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` | 1634 | 2026-04-29 |
| `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` | 1717 | 2026-04-29 |
| `docs/nautilus/community-discussions/practical-observations/01-response.md` | 1837 | 2026-04-29 |
| `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` | 2035 | 2026-04-29 |
| `docs/02-anthropic-vacancies/123-portal-mcp-py.md` | 2282 | 2026-04-29 |
| `docs/nautilus/innovation-transitions/01-response.md` | 2405 | 2026-04-29 |
| `docs/lorenzo-agent/scenarios/01-response.md` | 2453 | 2026-04-29 |
| `docs/nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md` | 2467 | 2026-04-29 |
| `docs/nautilus/community-discussions/voiceless-contributors/01-response.md` | 2533 | 2026-04-29 |
| `docs/nautilus/multi-tier-architecture/01-strategic-significance.md` | 2586 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-en/12-closing.md` | 2676 | 2026-04-29 |
| `docs/nautilus/community-discussions/habr-article-2-reaction/01-response.md` | 2792 | 2026-04-29 |
| `docs/nautilus/innovation-transitions/00-question-innovations-transitions.md` | 2802 | 2026-04-29 |
| `docs/nautilus/supply-demand/01-three-related-themes.md` | 2915 | 2026-04-29 |
| `docs/nautilus/transmission-box/01-completing-loop.md` | 3126 | 2026-04-29 |
| `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` | 3207 | 2026-04-29 |
| `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` | 3274 | 2026-04-29 |
| `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` | 3476 | 2026-04-29 |
| `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` | 3868 | 2026-04-29 |
| `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` | 3873 | 2026-04-29 |
| `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` | 4108 | 2026-04-29 |
| `docs/nautilus/representative-agent-layer-ru/12-zaklyuchenie.md` | 4414 | 2026-04-29 |
| `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` | 4419 | 2026-04-29 |
| `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` | 5859 | 2026-04-29 |
| `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` | 7088 | 2026-04-29 |
| `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` | 8408 | 2026-04-29 |
| `docs/02-anthropic-vacancies/00-intro.md` | 8934 | 2026-04-29 |
| `docs/02-anthropic-vacancies/165-closing.md` | 9298 | 2026-04-29 |
| `docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md` | 9468 | 2026-04-29 |
| `docs/02-anthropic-vacancies/69-section.md` | 9531 | 2026-04-29 |
| `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` | 11281 | 2026-04-29 |
| `docs/04-ai-collaborations/00-intro.md` | 11389 | 2026-04-29 |
| `docs/02-anthropic-vacancies/133-обратная-связь.md` | 17018 | 2026-04-29 |
| `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` | 19144 | 2026-04-29 |
| `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` | 20426 | 2026-04-29 |


### 169. Без метаданных (нет summary или тегов) — 163 файлов
_Файл: `docs/STALENESS.md` | 3 колонок, 20 строк_

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/00-intro-part2.md` | 5 | нет summary, нет тегов, короткий (5 слов) |
| `docs/01-svyazi/QA.md` | 206 | нет summary, нет тегов |
| `docs/01-svyazi/README.md` | 69 | нет тегов, короткий (69 слов) |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 20 | нет summary, нет тегов, короткий (20 слов) |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 148 | нет тегов |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 41 | нет тегов, короткий (41 слов) |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 91 | нет summary, нет тегов, короткий (91 слов) |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | 179 | нет тегов |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 93 | нет summary, нет тегов, короткий (93 слов) |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | нет summary, нет тегов, короткий (14 слов) |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | 140 | нет тегов |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 110 | нет тегов |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 178 | нет тегов |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 77 | нет тегов, короткий (77 слов) |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 75 | нет тегов, короткий (75 слов) |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 146 | нет summary, нет тегов |
| `docs/03-technology-combinations/README.md` | 32 | нет тегов, короткий (32 слов) |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/04-ai-collaborations/README.md` | 69 | нет тегов, короткий (69 слов) |


### 170. Короткие (< 100 слов, заготовки) — 87 файлов
_Файл: `docs/STALENESS.md` | 2 колонок, 20 строк_

| Файл | Слов |
|------|------|
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | 65 |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | 92 |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | 64 |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 29 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 68 |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | 88 |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | 58 |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | 88 |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | 62 |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 35 |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | 82 |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | 85 |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 38 |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | 77 |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | 70 |
| `docs/02-anthropic-vacancies/16-history.md` | 71 |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 36 |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | 99 |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | 35 |
| `docs/02-anthropic-vacancies/190-содержание.md` | 88 |


### 171. Сводная таблица по разделам
_Файл: `docs/STATS.md` | 8 колонок, 19 строк_

| Раздел | Файлов | Слов | H2 | Таблиц | Блоков кода | Ссылок | Жирного |
|--------|--------|------|----|--------|-------------|--------|---------|
| **01-svyazi** | 16 | 10,998 | 36 | 43 | 8 | 141 | 333 |
| **02-anthropic-vacancies** | 357 | 279,017 | 599 | 130 | 185 | 4875 | 4525 |
| **03-technology-combinations** | 7 | 2,796 | 14 | 5 | 0 | 49 | 44 |
| **04-ai-collaborations** | 17 | 26,057 | 45 | 89 | 0 | 262 | 359 |
| **05-habr-projects** | 10 | 8,619 | 22 | 18 | 0 | 139 | 49 |
| **ai-collaborations** | 30 | 8,207 | 17 | 34 | 0 | 191 | 49 |
| **anthropic-vacancies** | 111 | 30,929 | 28 | 11 | 0 | 525 | 137 |
| **autofilled** | 13 | 533 | 28 | 0 | 0 | 36 | 46 |
| **badges** | 1 | 44 | 2 | 0 | 1 | 14 | 0 |
| **contacts** | 15 | 3,151 | 71 | 56 | 14 | 215 | 57 |
| **glossary** | 4 | 2,282 | 23 | 31 | 0 | 310 | 140 |
| **habr-unique-projects** | 56 | 13,161 | 10 | 5 | 0 | 291 | 81 |
| **lorenzo-agent** | 62 | 19,979 | 45 | 0 | 0 | 285 | 182 |
| **nautilus** | 255 | 148,523 | 384 | 83 | 58 | 1790 | 2800 |
| **root** | 95 | 322,498 | 680 | 8390 | 125 | 9147 | 5468 |
| **svyazi-2-0** | 59 | 12,455 | 93 | 48 | 8 | 277 | 377 |
| **technology-combinations** | 53 | 12,903 | 34 | 25 | 7 | 286 | 116 |
| **templates** | 6 | 635 | 27 | 13 | 4 | 25 | 14 |
| **ИТОГО** | **1167** | **902,787** | **2158** | **8981** | **410** | **18858** | **14777** |


### 172. Топ-20 файлов по объёму
_Файл: `docs/STATS.md` | 5 колонок, 20 строк_

| Файл | Слов | H2 | Таблиц | Код |
|------|------|----|--------|-----|
| `TABLES` | 99622 | 16 | 4248 | 1 |
| `OUTLINE` | 34491 | 21 | 0 | 0 |
| `341-приложение-c-образец-спецификаций-ин` | 20426 | 2 | 0 | 11 |
| `01-интегральный-анализ-профиля-svend4` | 19144 | 2 | 0 | 19 |
| `READABILITY` | 17606 | 2 | 584 | 0 |
| `HEADING_AUDIT` | 17278 | 4 | 4 | 0 |
| `133-обратная-связь` | 17018 | 2 | 6 | 17 |
| `PARAGRAPH_QUALITY` | 14229 | 4 | 3 | 0 |
| `CONCEPTS` | 13165 | 55 | 0 | 0 |
| `READING_TIME` | 12186 | 4 | 543 | 0 |
| `00-intro` | 11389 | 1 | 3 | 0 |
| `342-что-такое-вариант-c-concept-document` | 11281 | 2 | 0 | 6 |
| `69-section` | 9531 | 2 | 2 | 18 |
| `01-response-en` | 9468 | 21 | 6 | 0 |
| `165-closing` | 9298 | 2 | 0 | 1 |
| `00-intro` | 8934 | 1 | 4 | 2 |
| `150-appendix-c-version-history` | 8408 | 2 | 0 | 2 |
| `ACTION_ITEMS` | 7697 | 6 | 0 | 0 |
| `EMPTY_SECTIONS` | 7416 | 4 | 36 | 0 |
| `memnet` | 7246 | 2 | 3 | 0 |


### 173. lorenzo-contacts (1)
_Файл: `docs/TASKS_INDEX.md` | 5 колонок, 1 строк_

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `write-contact` | Помогает написать первое сообщение автору OSS-проекта | "напиши письмо автору", "составь запрос на коллаборацию" | contact-outreach | write_contact |


### 174. lorenzo-contacts (1)
_Файл: `docs/TASKS_INDEX.md` | 5 колонок, 2 строк_

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `audit-corpus` | Сводный аудит состояния всего монорепо | "оцени состояние репо", "что сейчас с базой знаний" | — | audit_corpus |
| `find-contradictions` | Поиск противоречий между документами | "где противоречия про", "что в моих документах конфликтует" | — | find_contradictions |


### 175. lorenzo-contacts (1)
_Файл: `docs/TASKS_INDEX.md` | 5 колонок, 2 строк_

| Task ID | Описание | Триггеры | Шаблон | MCP tool |
|---------|----------|----------|--------|----------|
| `generate-rfc` | Создание RFC-документа по теме с подтягиванием контекста из корпуса | "напиши RFC по", "оформи спецификацию для" | rfc | generate_rfc |
| `weekly-review` | Еженедельное ревью с дайджестом, аудитом, ретро и KPI snapshot | "weekly review", "пятничный обход" | — | weekly_review |


### 176. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **MCP Protocol** | Инструменты | Стандарт интеграции AI-инструментов — Anthropic |
| **CardIndex** | Компоненты | 785+ карточек знаний, MIT, стабильный API |
| **AgentFS** | Компоненты | Файловая система для AI-агентов, MIT, kksudo |
| **Firecrawl** | Инструменты | Веб-краулер для AI, MIT, активная разработка |
| **Python 3.11+** | Платформа | Основной язык реализации всех компонентов |
| **Markdown docs** | Практики | 96% готовности, проверено на 460+ файлах |


### 177. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **Yodoca** | Компоненты | Память с консолидацией, Apache 2.0, spbmolot |
| **SENTINEL** | Компоненты | Allowlist безопасности для MCP |
| **Rufler** | Компоненты | Оркестратор агентов, активная разработка |
| **RAG + Graph** | Архитектура | Гибридный поиск: векторный + граф-обход |
| **claude-haiku-4-5** | Модели | Оптимум цена/качество для enrichment задач |
| **CRDT-синхронизация** | Архитектура | Бесконфликтная репликация для multi-agent |


### 178. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 6 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **NGT-memory** | Компоненты | Ассоциативный граф памяти, BSL 1.1 |
| **knowledge-space** | Компоненты | База знаний, MIT, нужна оценка API |
| **Wikontic** | Компоненты | Граф знаний, статус неизвестен |
| **MCP Tool Search** | Компоненты | Динамический поиск инструментов |
| **claude-opus-4-7** | Модели | Для сложных reasoning задач, высокая стоимость |
| **Local-first P2P** | Архитектура | GDPR-safe распределённые данные |


### 179. 🟢 ADOPT
_Файл: `docs/TECH_RADAR.md` | 3 колонок, 4 строк_

| Технология / Компонент | Категория | Комментарий |
|------------------------|-----------|------------|
| **BSL 1.1 libs** | Лицензии | Ограничения при коммерческом использовании |
| **Monolithic LLM** | Архитектура | Один LLM вместо ансамбля — узкое место |
| **Без PII-защиты** | Практики | Обработка данных без SENTINEL/quarantine |
| **Hard-coded prompts** | Практики | Промпты без версионирования и тестов |


### 180. Точная дата (2009)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `2026-04-19` | pendix-b-change-log) - [v1.1.0-draft (2026-04-19)](#v110-draft-2026-04-19) - [v1.0.0-draft (2026-04 earlie | `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` |
| `2026-04-19` | kdown / Python LOC / 6 782 / _(verified 2026-04-19, see ADR or commit abc123; both A= | `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` |
| `2026-05-03` | 4 частей 2. Установить deadline Фазы C: 2026-05-03 (2 недели) 3. Провести верификацию конкретных метрик: ```b | `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` |
| `2026-04-19` | kdown / Python LOC / 6 812 / _(verified 2026-04-19; both A=6782 and B=~6600 were poin | `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` |
| `2026-04-19` | жен вывести в stderr что-то вроде: ``` [2026-04-19 14:30:00,123] INFO [nautilus](../docs/05-habr-projects/memo | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
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
| ... | _ещё 1979 записей_ | |


### 181. Точная дата (2009)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `2026 год` | стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: | `docs/01-svyazi/01-executive-summary.md` |
| `2026 год` | azi/03-component-catalog.md)-профилей в 2026 году. Мой конкретный план consolidation: Archive (выставить [Gi | `docs/02-anthropic-vacancies/00-intro.md` |
| `2026 год` | ли ваш кейс — единственный в Dresden за 2026 год по очень редкой комбинации (Pflegegrad 2-3 + Persönliches B | `docs/02-anthropic-vacancies/133-обратная-связь.md` |
| `2026 год` | кла через диалог в нескольких сессиях в 2026 году. Формулировка «Синдром Золушки» и расширение к социальным | `docs/02-anthropic-vacancies/203-благодарности.md` |
| `2025 год` | Кириллом Дьологом сервис «Обучай» летом 2025 года. К апрелю 2026 — 93 тысячи пользователей за семь месяцев . | `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` |
| `2026 год` | ей-пользователей за семь месяцев в 2025-2026 годах), разрабатыв > 🏷️ **Ключевые слова:** `агенты`, `anthropi | `docs/02-anthropic-vacancies/230-аннотация.md` |
| `2025 год` | ля школьных учителей, запущенный осенью 2025 года Константином Чукавиным (тогда 25 лет, учителем и образоват | `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` |
| `2026 год` | з диалог с Claude (Anthropic) 26 апреля 2026 года, инициированный обзором автором русскоязычного интервью с | `docs/02-anthropic-vacancies/244-благодарности.md` |
| `2027 год` | к функциональности Projects через 2026-2027 годы. **[GitHub](../docs/01-svyazi/03-component-catalog.md) дл | `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` |
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
| `2026 год` | es / / `2026/04/25` / 10 / dates / / `в 2026 году` / 8 / dates / / `март 2026` / 7 / dates / / `марта 2026` | `docs/NAMED_ENTITIES.md` |
| `2026 год` | кла через диалог в нескольких сессиях в 2026 году. Формулировка «Синдром Золушки» и расширение к со… - Бл | `docs/OUTLINE.md` |
| `2026 год` | оторые не т [Статус] - Статья про SVM в 2026 году даёт важный анти-хайповый кубик: для персонализированных р | `docs/QUESTIONS.md` |
| `2026 год` | стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для Svyazi‑2.0 : ing | `docs/SUMMARIES.md` |
| `2026 год` | ates / / `март 2026` / 8 / dates / / `в 2026 году` / 8 / dates / / `марта 2026` / 6 / dates / / `декабрь 202 | `docs/TABLES.md` |
| `2025 год` | ic-vacancies/203-благодарности.md` / / `2025 год` / Кириллом Дьологом сервис «Обучай» летом 2025 года. К апр | `docs/TABLES.md` |
| `2027 год` | ic-vacancies/244-благодарности.md` / / `2027 год` / к функциональности Projects через 2026-2027 годы. **[Git | `docs/TABLES.md` |
| `2024 год` | anthropic-vacancies/69-section.md` / / `2024 год` / «это решение 2019 года, после изменений 2024 года примен | `docs/TABLES.md` |
| `2026 год` | гим агентом”. Linux Foundation в апреле 2026 года объявила, что A2A стал production‑ready open standard с бо | `docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md` |
| ... | _ещё 105 записей_ | |


### 182. Точная дата (2009)
_Файл: `docs/TIMELINE.md` | 3 колонок, 1 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `Q2 2024` | Конкретные даты: 2024-03-15, март 2024, Q2 2024 - Относительные: «через 3 месяца», «в следующем квартале» - | `docs/SCRIPTS_CATALOG.md` |


### 183. Точная дата (2009)
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
| `апрель 2026` | IMPLEMENTATION_STAGE_PART_[1-4].md** (апрель 2026): - Вариант A: ветка `claude/review-[nautilus](../docs/05- | `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` |
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
| `январе 2026` | формы Cowork от Anthropic (запущенной в январе 2026), предлагает конкретный путь реализации. > ✅ **Результат:** | `docs/02-anthropic-vacancies/325-аннотация.md` |
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
| `декабрь 2025` | summary --> > **Создан:** [? уточнить — декабрь 2025, если совпадает с волной --- <!-- tags: memory, anthropic, | `docs/02-anthropic-vacancies/43-history.md` |
| ... | _ещё 181 записей_ | |


### 184. Точная дата (2009)
_Файл: `docs/TIMELINE.md` | 3 колонок, 6 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/01-svyazi/01-executive-summary.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/04-ai-collaborations/01-executive-summary.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для Svyazi‑2.0 : | `docs/SUMMARIES.md` |
| `первые месяцы 2026` | `2026 год` / стыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/TABLES.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/lorenzo-agent/operationalized/06-conclusion-deserves-attention.md` |
| `первые месяцы 2026` | ак их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0 | `docs/svyazi-2-0/overview/executive-summary.md` |


### 185. Точная дата (2009)
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
| ... | _ещё 475 записей_ | |


### 186. Точная дата (2009)
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
| `30-45 дне` | иля. ### Итоговая целевая картина Через 30-45 дней вашего собранного времени [GitHub](../docs/01-svyazi/03-co | `docs/02-anthropic-vacancies/00-intro.md` |
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
| `1-2 недели` | уже это позволяют (нужно проверить), то 1-2 недели для создания template. > 🔧 **Подход:** Часть 2 (Project Man | `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` |
| `10-16 месяце` | ompose, документацию, план реализации в 10-16 месяцев, technological stack уже выбран (Python 3.11, FastAPI, pyg | `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` |
| `3-6 месяце` | ии InGit до работающего MVP в следующие 3-6 месяцев. Семь документов Nautilus/OKWF могут жить в обычном GitHub | `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` |
| ... | _ещё 291 записей_ | |


### 187. Точная дата (2009)
_Файл: `docs/TIMELINE.md` | 3 колонок, 31 строк_

| Маркер | Контекст | Файл |
|--------|----------|------|
| `версия 0.1.5` | 3view4turn27view0 / Рабочий прототип, версия 0.1.5; “рабочая, но не финальная”. citeturn33view7 / **Очень в | `docs/01-svyazi/03-component-catalog.md` |
| `v4.5` | латформы : 87 skills, chat-migration v1→v4.5 quantum-hybrid, Multi-Chat Orchestrator, xMemory-архитектур | `docs/02-anthropic-vacancies/00-intro.md` |
| `v1.0` | rlängerung/Nachzahlung), Master Dossier v1.0, анализ BSG-практики, анализ Kostenschieberei. То есть это | `docs/02-anthropic-vacancies/00-intro.md` |
| `v1.0` | ая архитектурная спецификация протокола v1.0 — и она существенно сильнее , чем я реконструировал в преды | `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` |
| `v1.0` | 112 строк) — архитектурная спецификация v1.0 с философией federation-over-merging, триадой [info1](../do | `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` |
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
| `v1.1.0` | hange Log](#appendix-b-change-log) - [v1.1.0-draft (2026-04-19)](#v110-draft-2026-04-19) - [v1.0.0-dra | `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` |
| `v1.0.0` | 26-04-19)](#v110-draft-2026-04-19) - [v1.0.0-draft (2026-04 earlier)](#v100-draft-2026-04-earlier) <!- | `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` |
| `v3.1.0` | uirement Levels - OpenAPI Specification v3.1.0 (for REST API schemas) - JSON Schema (for passport validati | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v1.1.0` | --- *End of Nautilus Portal Protocol v1.1.0-draft* *Feedback, issues, proposals: [github.com/svend4/n | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v1.0` | ворить отдельно. #### Что я сохранил из v1.0 Базовая структура, нумерация разделов (1–15 из v1.0 осталис | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v1.1` | и у кого-то есть v1.0, они могут читать v1.1 параллельно — те же разделы говорят о том же, плюс новые. # | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v1.2` | ого. #### Что я сознательно оставил для v1.2 или v2.0 Formal bridge algebra. Part 3 implementation docs | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v2.0` | Что я сознательно оставил для v1.2 или v2.0 Formal bridge algebra. Part 3 implementation docs указывает | `docs/02-anthropic-vacancies/104-appendix-c-references.md` |
| `v3.0` | l header 7. Добавить changelog-запись: «v3.0 consolidated from A (branch X) and B (branch Y) on YYYY | `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` |
| `v2.0` | одология может быть формализована в NPP v2.0 как рекомендованный workflow для community-contributed docu | `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` |
| `v1.1` | еграция с Nautilus Portal Protocol NPP v1.1 §17.3 «Breaking Changes Process» упоминает RFC-процесс для | `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` |
| `v1.0` | x C: История изменений методологии ### v1.0 (2026-04) Первая формализация, основана на опыте применени | `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` |
| `v1.0` | x A --- *End of REVIEW_METHODOLOGY.md v1.0* *Feedback, issues, proposals: [github.com/svend4/nautilu | `docs/02-anthropic-vacancies/122-глоссарий.md` |
| `v1.1` | чие от двух предыдущих (PORTAL-PROTOCOL v1.1 и trio of passports), имеет другой характер . Это не techni | `docs/02-anthropic-vacancies/122-глоссарий.md` |
| `v1.1` | 00) Protocol: Nautilus Portal Protocol v1.1 Dependencies: mcp>=1.0.0 (only external dep) Python: 3.10+ | `docs/02-anthropic-vacancies/123-portal-mcp-py.md` |
| ... | _ещё 971 записей_ | |


### 188. Корпусная статистика
_Файл: `docs/VOCABULARY.md` | 2 колонок, 5 строк_

| Метрика | Значение |
|---------|----------|
| Средний TTR | 0.523 |
| Средний STTR (100-токенное окно) | 0.674 |
| Lexical density | 0.847 |
| Средняя длина слова | 6.56 |
| Общая оценка | 🟡 Средний |


### 189. Топ файлов по богатству словаря (STTR)
_Файл: `docs/VOCABULARY.md` | 6 колонок, 30 строк_

| Файл | STTR | TTR | Hapax% | Lex.Density | Токенов |
|------|------|-----|--------|-------------|---------|
| `ABBREVIATIONS.md` | 0.945 | 0.729 | 77% | 0.880 | 887 |
| `48-content-overview.md` | 0.880 | 0.609 | 80% | 0.888 | 161 |
| `ENTITIES.md` | 0.880 | 0.605 | 74% | 0.957 | 162 |
| `04-desyat-oblastey.md` | 0.876 | 0.565 | 71% | 0.915 | 1440 |
| `00-question-innovations-transitions.md` | 0.872 | 0.531 | 69% | 0.829 | 2680 |
| `README.md` | 0.870 | 0.745 | 78% | 0.897 | 282 |
| `02-related-projects.md` | 0.870 | 0.696 | 73% | 0.841 | 359 |
| `06-1-introduction.md` | 0.867 | 0.608 | 67% | 0.909 | 342 |
| `4-summary-authors.md` | 0.865 | 0.710 | 75% | 0.865 | 252 |
| `02-agentops-trace-envelope.md` | 0.863 | 0.656 | 68% | 0.884 | 387 |
| `03-why-natural-for-programmers.md` | 0.863 | 0.669 | 75% | 0.841 | 970 |
| `09-minuses-and-risks.md` | 0.862 | 0.691 | 78% | 0.836 | 657 |
| `64-for-the-curious-philosophy.md` | 0.860 | 0.590 | 67% | 0.854 | 583 |
| `04-stronger-paths-outside-anthropic.md` | 0.860 | 0.688 | 74% | 0.884 | 449 |
| `continuation-10-domains.md` | 0.860 | 0.664 | 74% | 0.905 | 262 |
| `00-intro.md` | 0.859 | 0.362 | 60% | 0.869 | 10785 |
| `05-polymath-project-tao-comparison.md` | 0.857 | 0.599 | 72% | 0.847 | 1318 |
| `238-7-области-применения.md` | 0.857 | 0.561 | 67% | 0.945 | 691 |
| `6-continuous-eval-loop.md` | 0.857 | 0.690 | 76% | 0.869 | 335 |
| `01-three-direct-analogues.md` | 0.857 | 0.699 | 72% | 0.872 | 375 |
| `01-introduction.md` | 0.855 | 0.788 | 80% | 0.908 | 260 |
| `01-claude-response.md` | 0.855 | 0.524 | 69% | 0.841 | 2256 |
| `01-introduction.md` | 0.853 | 0.697 | 74% | 0.892 | 379 |
| `03-three-variants-A-B-C.md` | 0.852 | 0.635 | 74% | 0.815 | 644 |
| `194-4-десять-областей-применения.md` | 0.851 | 0.535 | 68% | 0.918 | 1519 |
| `01-three-key-candidates.md` | 0.850 | 0.729 | 78% | 0.871 | 310 |
| `18-comment-on-document.md` | 0.850 | 0.728 | 78% | 0.865 | 415 |
| `72-расписание-фазы-3.md` | 0.848 | 0.578 | 68% | 0.842 | 697 |
| `01-интегральный-анализ-профиля-svend4.md` | 0.848 | 0.326 | 60% | 0.831 | 17513 |
| `01-response.md` | 0.848 | 0.506 | 69% | 0.823 | 2248 |


### 190. Файлы с бедным словарём (требуют доработки)
_Файл: `docs/VOCABULARY.md` | 4 колонок, 30 строк_

| Файл | STTR | Оценка | Токенов |
|------|------|--------|---------|
| `AUTOFILLED.md` | 0.230 | 🔴 Очень бедный | 187 |
| `README.md` | 0.273 | 🔴 Очень бедный | 77 |
| `134-the-double-triangle-architecture-md.md` | 0.286 | 🔴 Очень бедный | 70 |
| `DEPENDENCY_MAP.md` | 0.297 | 🔴 Очень бедный | 641 |
| `README.md` | 0.302 | 🔴 Очень бедный | 96 |
| `CROSS_SECTION.md` | 0.304 | 🔴 Очень бедный | 505 |
| `BROKEN_LINKS.md` | 0.306 | 🔴 Очень бедный | 905 |
| `28-appendix-a-minimal-working-example.md` | 0.310 | 🔴 Очень бедный | 132 |
| `273-infrastructure-for-ai-collaborative-intellectual-w.md` | 0.310 | 🔴 Очень бедный | 142 |
| `166-representative-agent-layer-md.md` | 0.311 | 🔴 Очень бедный | 74 |
| `151-open-knowledge-work-foundation-md.md` | 0.311 | 🔴 Очень бедный | 74 |
| `249-composite-skills-agent-md.md` | 0.314 | 🔴 Очень бедный | 70 |
| `CROSSREFS.md` | 0.319 | 🔴 Очень бедный | 814 |
| `README.md` | 0.320 | 🔴 Очень бедный | 100 |
| `187-слой-представительских-агентов-md.md` | 0.320 | 🔴 Очень бедный | 75 |
| `README.md` | 0.323 | 🔴 Очень бедный | 65 |
| `208-professional-colleague-agents-md.md` | 0.324 | 🔴 Очень бедный | 71 |
| `README.md` | 0.330 | 🔴 Очень бедный | 113 |
| `CITATION_INDEX.md` | 0.330 | 🔴 Очень бедный | 478 |
| `README.md` | 0.333 | 🔴 Очень бедный | 60 |
| `HEADING_AUDIT.md` | 0.335 | 🔴 Очень бедный | 23419 |
| `README.md` | 0.340 | 🔴 Очень бедный | 141 |
| `README.md` | 0.340 | 🔴 Очень бедный | 102 |
| `README.md` | 0.340 | 🔴 Очень бедный | 124 |
| `README.md` | 0.343 | 🔴 Очень бедный | 73 |
| `READABILITY.md` | 0.343 | 🔴 Очень бедный | 10928 |
| `CLUSTERS.md` | 0.344 | 🔴 Очень бедный | 2658 |
| `READING_ORDER.md` | 0.346 | 🔴 Очень бедный | 4674 |
| `README.md` | 0.348 | 🔴 Очень бедный | 69 |
| `305-a-practical-path-to-layer-b-through-symbiotic-inte.md` | 0.350 | 🔴 Очень бедный | 114 |


### 191. Топ-20 слов
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


### 192. Глобальный топ-50 слов
_Файл: `docs/WORD_FREQ.md` | 4 колонок, 50 строк_

| # | Слово | Частота | Визуализация |
|---|-------|---------|-------------|
| 1 | **anthropic** | 14,925 | `████████████████████` |
| 2 | **vacancies** | 12,525 | `████████████████░░░░` |
| 3 | **nautilus** | 6,194 | `████████░░░░░░░░░░░░` |
| 4 | **проблем** | 5,919 | `███████░░░░░░░░░░░░░` |
| 5 | **agent** | 5,618 | `███████░░░░░░░░░░░░░` |
| 6 | **svyazi** | 3,888 | `█████░░░░░░░░░░░░░░░` |
| 7 | **claude** | 2,782 | `███░░░░░░░░░░░░░░░░░` |
| 8 | **cowork** | 2,623 | `███░░░░░░░░░░░░░░░░░` |
| 9 | **agents** | 2,550 | `███░░░░░░░░░░░░░░░░░` |
| 10 | **сложный** | 2,386 | `███░░░░░░░░░░░░░░░░░` |
| 11 | **lorenzo** | 2,367 | `███░░░░░░░░░░░░░░░░░` |
| 12 | **layer** | 2,346 | `███░░░░░░░░░░░░░░░░░` |
| 13 | **мин** | 2,247 | `███░░░░░░░░░░░░░░░░░` |
| 14 | **turn** | 2,118 | `██░░░░░░░░░░░░░░░░░░` |
| 15 | **ingit** | 2,086 | `██░░░░░░░░░░░░░░░░░░` |
| 16 | **habr** | 2,027 | `██░░░░░░░░░░░░░░░░░░` |
| 17 | **appendix** | 1,998 | `██░░░░░░░░░░░░░░░░░░` |
| 18 | **projects** | 1,869 | `██░░░░░░░░░░░░░░░░░░` |
| 19 | **knowledge** | 1,854 | `██░░░░░░░░░░░░░░░░░░` |
| 20 | **mcp** | 1,850 | `██░░░░░░░░░░░░░░░░░░` |
| 21 | **combinations** | 1,849 | `██░░░░░░░░░░░░░░░░░░` |
| 22 | **быстро** | 1,840 | `██░░░░░░░░░░░░░░░░░░` |
| 23 | **view** | 1,756 | `██░░░░░░░░░░░░░░░░░░` |
| 24 | **what** | 1,699 | `██░░░░░░░░░░░░░░░░░░` |
| 25 | **readme** | 1,621 | `██░░░░░░░░░░░░░░░░░░` |
| 26 | **infrastructure** | 1,621 | `██░░░░░░░░░░░░░░░░░░` |
| 27 | **memory** | 1,607 | `██░░░░░░░░░░░░░░░░░░` |
| 28 | **источник** | 1,578 | `██░░░░░░░░░░░░░░░░░░` |
| 29 | **legal** | 1,576 | `██░░░░░░░░░░░░░░░░░░` |
| 30 | **architecture** | 1,562 | `██░░░░░░░░░░░░░░░░░░` |
| 31 | **слов** | 1,557 | `██░░░░░░░░░░░░░░░░░░` |
| 32 | **репозитория** | 1,507 | `██░░░░░░░░░░░░░░░░░░` |
| 33 | **mhtml** | 1,399 | `█░░░░░░░░░░░░░░░░░░░` |
| 34 | **document** | 1,387 | `█░░░░░░░░░░░░░░░░░░░` |
| 35 | **снимок** | 1,382 | `█░░░░░░░░░░░░░░░░░░░` |
| 36 | **корень** | 1,344 | `█░░░░░░░░░░░░░░░░░░░` |
| 37 | **portal** | 1,293 | `█░░░░░░░░░░░░░░░░░░░` |
| 38 | **professional** | 1,283 | `█░░░░░░░░░░░░░░░░░░░` |
| 39 | **сходство** | 1,277 | `█░░░░░░░░░░░░░░░░░░░` |
| 40 | **work** | 1,275 | `█░░░░░░░░░░░░░░░░░░░` |
| 41 | **review** | 1,262 | `█░░░░░░░░░░░░░░░░░░░` |
| 42 | **collaborations** | 1,254 | `█░░░░░░░░░░░░░░░░░░░` |
| 43 | **раздел** | 1,233 | `█░░░░░░░░░░░░░░░░░░░` |
| 44 | **colleague** | 1,231 | `█░░░░░░░░░░░░░░░░░░░` |
| 45 | **open** | 1,211 | `█░░░░░░░░░░░░░░░░░░░` |
| 46 | **protocol** | 1,206 | `█░░░░░░░░░░░░░░░░░░░` |
| 47 | **technology** | 1,200 | `█░░░░░░░░░░░░░░░░░░░` |
| 48 | **search** | 1,154 | `█░░░░░░░░░░░░░░░░░░░` |
| 49 | **вакансии** | 1,136 | `█░░░░░░░░░░░░░░░░░░░` |
| 50 | **абзац** | 1,118 | `█░░░░░░░░░░░░░░░░░░░` |


### 193. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **turn** | 481 | `███████████████` |
| **view** | 327 | `██████████░░░░░` |
| **svyazi** | 186 | `█████░░░░░░░░░░` |
| **search** | 175 | `█████░░░░░░░░░░` |
| **cite** | 165 | `█████░░░░░░░░░░` |
| **memory** | 97 | `███░░░░░░░░░░░░` |
| **проект** | 79 | `██░░░░░░░░░░░░░` |
| **rag** | 69 | `██░░░░░░░░░░░░░` |
| **oss** | 66 | `██░░░░░░░░░░░░░` |
| **agentfs** | 57 | `█░░░░░░░░░░░░░░` |
| **mcp** | 55 | `█░░░░░░░░░░░░░░` |
| **collaborations** | 54 | `█░░░░░░░░░░░░░░` |
| **cardindex** | 48 | `█░░░░░░░░░░░░░░` |
| **ngt** | 47 | `█░░░░░░░░░░░░░░` |
| **yodoca** | 45 | `█░░░░░░░░░░░░░░` |


### 194. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **anthropic** | 3001 | `███████████████` |
| **vacancies** | 2502 | `████████████░░░` |
| **agent** | 1196 | `█████░░░░░░░░░░` |
| **cowork** | 985 | `████░░░░░░░░░░░` |
| **сходство** | 913 | `████░░░░░░░░░░░` |
| **nautilus** | 811 | `████░░░░░░░░░░░` |
| **ingit** | 740 | `███░░░░░░░░░░░░` |
| **agents** | 631 | `███░░░░░░░░░░░░` |
| **portal** | 537 | `██░░░░░░░░░░░░░` |
| **work** | 516 | `██░░░░░░░░░░░░░` |
| **lorenzo** | 504 | `██░░░░░░░░░░░░░` |
| **appendix** | 483 | `██░░░░░░░░░░░░░` |
| **layer** | 480 | `██░░░░░░░░░░░░░` |
| **protocol** | 471 | `██░░░░░░░░░░░░░` |
| **document** | 467 | `██░░░░░░░░░░░░░` |


### 195. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **svyazi** | 29 | `███████████████` |
| **agent** | 27 | `█████████████░░` |
| **legal** | 25 | `████████████░░░` |
| **first** | 25 | `████████████░░░` |
| **knowledge** | 25 | `████████████░░░` |
| **technology** | 24 | `████████████░░░` |
| **combinations** | 24 | `████████████░░░` |
| **local** | 22 | `███████████░░░░` |
| **комбинация** | 19 | `█████████░░░░░░` |
| **habr** | 19 | `█████████░░░░░░` |
| **articles** | 19 | `█████████░░░░░░` |
| **router** | 17 | `████████░░░░░░░` |
| **cardindex** | 15 | `███████░░░░░░░░` |
| **claude** | 15 | `███████░░░░░░░░` |
| **graph** | 15 | `███████░░░░░░░░` |


### 196. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **turn** | 549 | `███████████████` |
| **view** | 392 | `██████████░░░░░` |
| **svyazi** | 351 | `█████████░░░░░░` |
| **search** | 193 | `█████░░░░░░░░░░` |
| **memory** | 183 | `█████░░░░░░░░░░` |
| **cite** | 171 | `████░░░░░░░░░░░` |
| **mcp** | 140 | `███░░░░░░░░░░░░` |
| **rag** | 131 | `███░░░░░░░░░░░░` |
| **проект** | 114 | `███░░░░░░░░░░░░` |
| **llm** | 99 | `██░░░░░░░░░░░░░` |
| **knowledge** | 91 | `██░░░░░░░░░░░░░` |
| **слой** | 88 | `██░░░░░░░░░░░░░` |
| **habr** | 88 | `██░░░░░░░░░░░░░` |
| **oss** | 83 | `██░░░░░░░░░░░░░` |
| **agentfs** | 78 | `██░░░░░░░░░░░░░` |


### 197. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **llm** | 64 | `███████████████` |
| **пара** | 63 | `██████████████░` |
| **mcp** | 54 | `████████████░░░` |
| **svyazi** | 46 | `██████████░░░░░` |
| **memory** | 45 | `██████████░░░░░` |
| **habr** | 40 | `█████████░░░░░░` |
| **yodoca** | 35 | `████████░░░░░░░` |
| **legal** | 34 | `███████░░░░░░░░` |
| **каждый** | 31 | `███████░░░░░░░░` |
| **projects** | 28 | `██████░░░░░░░░░` |
| **claude** | 27 | `██████░░░░░░░░░` |
| **self** | 25 | `█████░░░░░░░░░░` |
| **obsidian** | 24 | `█████░░░░░░░░░░` |
| **ngt** | 23 | `█████░░░░░░░░░░` |
| **skills** | 23 | `█████░░░░░░░░░░` |


### 198. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **collaborations** | 78 | `███████████████` |
| **agent** | 78 | `███████████████` |
| **memory** | 73 | `██████████████░` |
| **svyazi** | 66 | `████████████░░░` |
| **rag** | 61 | `███████████░░░░` |
| **habr** | 60 | `███████████░░░░` |
| **проектов** | 57 | `██████████░░░░░` |
| **коллабораций** | 56 | `██████████░░░░░` |
| **mcp** | 55 | `██████████░░░░░` |
| **knowledge** | 54 | `██████████░░░░░` |
| **поиск** | 51 | `█████████░░░░░░` |
| **источник** | 46 | `████████░░░░░░░` |
| **mhtml** | 46 | `████████░░░░░░░` |
| **снимок** | 45 | `████████░░░░░░░` |
| **корень** | 45 | `████████░░░░░░░` |


### 199. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **anthropic** | 714 | `███████████████` |
| **vacancies** | 346 | `███████░░░░░░░░` |
| **claude** | 240 | `█████░░░░░░░░░░` |
| **hermes** | 204 | `████░░░░░░░░░░░` |
| **вакансии** | 202 | `████░░░░░░░░░░░` |
| **источник** | 198 | `████░░░░░░░░░░░` |
| **кластерам** | 196 | `████░░░░░░░░░░░` |
| **репозитория** | 196 | `████░░░░░░░░░░░` |
| **снимок** | 195 | `████░░░░░░░░░░░` |
| **mhtml** | 194 | `████░░░░░░░░░░░` |
| **корень** | 194 | `████░░░░░░░░░░░` |
| **nautilus** | 183 | `███░░░░░░░░░░░░` |
| **раздел** | 157 | `███░░░░░░░░░░░░` |
| **диалога** | 156 | `███░░░░░░░░░░░░` |
| **research** | 135 | `██░░░░░░░░░░░░░` |


### 200. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **svyazi** | 33 | `███████████████` |
| **компонент** | 20 | `█████████░░░░░░` |
| **экосистемы** | 20 | `█████████░░░░░░` |
| **описание** | 13 | `█████░░░░░░░░░░` |
| **проекты** | 10 | `████░░░░░░░░░░░` |
| **тип** | 10 | `████░░░░░░░░░░░` |
| **статус** | 10 | `████░░░░░░░░░░░` |
| **упоминаний** | 10 | `████░░░░░░░░░░░` |
| **ссылки** | 10 | `████░░░░░░░░░░░` |
| **исходники** | 10 | `████░░░░░░░░░░░` |
| **документация** | 10 | `████░░░░░░░░░░░` |
| **readme** | 10 | `████░░░░░░░░░░░` |
| **components** | 4 | `█░░░░░░░░░░░░░░` |
| **cowork** | 3 | `█░░░░░░░░░░░░░░` |
| **ingit** | 3 | `█░░░░░░░░░░░░░░` |


### 201. 01-svyazi (9,290 слов)
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


### 202. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **contacts** | 99 | `███████████████` |
| **статус** | 70 | `██████████░░░░░` |
| **связи** | 70 | `██████████░░░░░` |
| **профиль** | 56 | `████████░░░░░░░` |
| **первое** | 56 | `████████░░░░░░░` |
| **сообщение** | 56 | `████████░░░░░░░` |
| **открытые** | 42 | `██████░░░░░░░░░` |
| **вопросы** | 42 | `██████░░░░░░░░░` |
| **сходство** | 42 | `██████░░░░░░░░░` |
| **vladspace** | 41 | `██████░░░░░░░░░` |
| **zodigancode** | 37 | `█████░░░░░░░░░░` |
| **svyazi** | 31 | `████░░░░░░░░░░░` |
| **проекты** | 28 | `████░░░░░░░░░░░` |
| **antipozitive** | 25 | `███░░░░░░░░░░░░` |
| **tagir** | 25 | `███░░░░░░░░░░░░` |


### 203. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **svyazi** | 141 | `███████████████` |
| **combinations** | 100 | `██████████░░░░░` |
| **habr** | 75 | `███████░░░░░░░░` |
| **projects** | 75 | `███████░░░░░░░░` |
| **components** | 72 | `███████░░░░░░░░` |
| **unique** | 65 | `██████░░░░░░░░░` |
| **technology** | 54 | `█████░░░░░░░░░░` |
| **mcp** | 51 | `█████░░░░░░░░░░` |
| **ensembles** | 46 | `████░░░░░░░░░░░` |
| **memory** | 44 | `████░░░░░░░░░░░` |
| **комбинация** | 42 | `████░░░░░░░░░░░` |
| **pairs** | 38 | `████░░░░░░░░░░░` |
| **key** | 37 | `███░░░░░░░░░░░░` |
| **rag** | 33 | `███░░░░░░░░░░░░` |
| **agent** | 33 | `███░░░░░░░░░░░░` |


### 204. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **habr** | 191 | `███████████████` |
| **projects** | 183 | `██████████████░` |
| **unique** | 165 | `████████████░░░` |
| **claude** | 145 | `███████████░░░░` |
| **проектов** | 111 | `████████░░░░░░░` |
| **поиск** | 104 | `████████░░░░░░░` |
| **источник** | 100 | `███████░░░░░░░░` |
| **уникальных** | 98 | `███████░░░░░░░░` |
| **репозитория** | 94 | `███████░░░░░░░░` |
| **mhtml** | 93 | `███████░░░░░░░░` |
| **снимок** | 92 | `███████░░░░░░░░` |
| **корень** | 92 | `███████░░░░░░░░` |
| **mcp** | 91 | `███████░░░░░░░░` |
| **llm** | 85 | `██████░░░░░░░░░` |
| **pairs** | 84 | `██████░░░░░░░░░` |


### 205. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **lorenzo** | 642 | `███████████████` |
| **agent** | 344 | `████████░░░░░░░` |
| **anthropic** | 195 | `████░░░░░░░░░░░` |
| **claude** | 160 | `███░░░░░░░░░░░░` |
| **репозитория** | 152 | `███░░░░░░░░░░░░` |
| **catalyst** | 126 | `██░░░░░░░░░░░░░` |
| **источник** | 110 | `██░░░░░░░░░░░░░` |
| **mhtml** | 110 | `██░░░░░░░░░░░░░` |
| **снимок** | 110 | `██░░░░░░░░░░░░░` |
| **вакансии** | 110 | `██░░░░░░░░░░░░░` |
| **кластерам** | 110 | `██░░░░░░░░░░░░░` |
| **корень** | 110 | `██░░░░░░░░░░░░░` |
| **раздел** | 110 | `██░░░░░░░░░░░░░` |
| **диалога** | 110 | `██░░░░░░░░░░░░░` |
| **dhlab** | 92 | `██░░░░░░░░░░░░░` |


### 206. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **nautilus** | 1053 | `███████████████` |
| **agent** | 965 | `█████████████░░` |
| **anthropic** | 862 | `████████████░░░` |
| **claude** | 700 | `█████████░░░░░░` |
| **agents** | 629 | `████████░░░░░░░` |
| **cowork** | 507 | `███████░░░░░░░░` |
| **раздел** | 501 | `███████░░░░░░░░` |
| **work** | 465 | `██████░░░░░░░░░` |
| **репозитория** | 464 | `██████░░░░░░░░░` |
| **вакансии** | 459 | `██████░░░░░░░░░` |
| **источник** | 459 | `██████░░░░░░░░░` |
| **layer** | 458 | `██████░░░░░░░░░` |
| **mhtml** | 455 | `██████░░░░░░░░░` |
| **кластерам** | 455 | `██████░░░░░░░░░` |
| **снимок** | 455 | `██████░░░░░░░░░` |


### 207. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **anthropic** | 10081 | `███████████████` |
| **vacancies** | 9319 | `█████████████░░` |
| **проблем** | 5902 | `████████░░░░░░░` |
| **nautilus** | 4099 | `██████░░░░░░░░░` |
| **agent** | 2512 | `███░░░░░░░░░░░░` |
| **svyazi** | 2387 | `███░░░░░░░░░░░░` |
| **сложный** | 2382 | `███░░░░░░░░░░░░` |
| **мин** | 2246 | `███░░░░░░░░░░░░` |
| **быстро** | 1812 | `██░░░░░░░░░░░░░` |
| **слов** | 1529 | `██░░░░░░░░░░░░░` |
| **readme** | 1440 | `██░░░░░░░░░░░░░` |
| **combinations** | 1332 | `█░░░░░░░░░░░░░░` |
| **appendix** | 1298 | `█░░░░░░░░░░░░░░` |
| **layer** | 1285 | `█░░░░░░░░░░░░░░` |
| **lorenzo** | 1205 | `█░░░░░░░░░░░░░░` |


### 208. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **view** | 427 | `███████████████` |
| **turn** | 419 | `██████████████░` |
| **svyazi** | 275 | `█████████░░░░░░` |
| **search** | 232 | `████████░░░░░░░` |
| **citeturn** | 224 | `███████░░░░░░░░` |
| **memory** | 137 | `████░░░░░░░░░░░` |
| **research** | 105 | `███░░░░░░░░░░░░` |
| **rag** | 96 | `███░░░░░░░░░░░░` |
| **источник** | 90 | `███░░░░░░░░░░░░` |
| **components** | 85 | `██░░░░░░░░░░░░░` |
| **report** | 75 | `██░░░░░░░░░░░░░` |
| **deep** | 73 | `██░░░░░░░░░░░░░` |
| **first** | 64 | `██░░░░░░░░░░░░░` |
| **yodoca** | 62 | `██░░░░░░░░░░░░░` |
| **knowledge** | 53 | `█░░░░░░░░░░░░░░` |


### 209. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **combinations** | 354 | `███████████████` |
| **legal** | 305 | `████████████░░░` |
| **agent** | 198 | `████████░░░░░░░` |
| **technology** | 187 | `███████░░░░░░░░` |
| **claude** | 131 | `█████░░░░░░░░░░` |
| **новых** | 112 | `████░░░░░░░░░░░` |
| **code** | 112 | `████░░░░░░░░░░░` |
| **event** | 107 | `████░░░░░░░░░░░` |
| **технологий** | 103 | `████░░░░░░░░░░░` |
| **mhtml** | 97 | `████░░░░░░░░░░░` |
| **комбинирование** | 96 | `████░░░░░░░░░░░` |
| **свойств** | 96 | `████░░░░░░░░░░░` |
| **stack** | 96 | `████░░░░░░░░░░░` |
| **источник** | 95 | `████░░░░░░░░░░░` |
| **снимок** | 95 | `████░░░░░░░░░░░` |


### 210. 01-svyazi (9,290 слов)
_Файл: `docs/WORD_FREQ.md` | 3 колонок, 15 строк_

| Слово | Частота | |
|-------|---------|---|
| **templates** | 52 | `███████████████` |
| **template** | 34 | `█████████░░░░░░` |
| **название** | 32 | `█████████░░░░░░` |
| **имя** | 27 | `███████░░░░░░░░` |
| **version** | 25 | `███████░░░░░░░░` |
| **record** | 24 | `██████░░░░░░░░░` |
| **tags** | 23 | `██████░░░░░░░░░` |
| **смотрите** | 23 | `██████░░░░░░░░░` |
| **nnnn** | 23 | `██████░░░░░░░░░` |
| **дата** | 23 | `██████░░░░░░░░░` |
| **decision** | 22 | `██████░░░░░░░░░` |
| **компонент** | 19 | `█████░░░░░░░░░░` |
| **создано** | 18 | `█████░░░░░░░░░░` |
| **component** | 17 | `████░░░░░░░░░░░` |
| **действие** | 17 | `████░░░░░░░░░░░` |


## svyazi-2-0 (12 таблиц)


### 1. Подпапки
_Файл: `docs/svyazi-2-0/README.md` | 2 колонок, 8 строк_

| Подпапка | Тема |
|---|---|
| [`overview/`](overview/) | Executive summary, методика, общая карта |
| [`components/`](components/) | Описание каждого найденного проекта-кирпичика |
| [`ensembles/`](ensembles/) | Ансамбли A–E и три ансамбля «второго порядка» |
| [`architecture/`](architecture/) | Архитектурные зазоры и пять интеграционных контрактов |
| [`prototype/`](prototype/) | MVP, риски, дорожная карта итераций |
| [`security/`](security/) | Default policy, приватность, бюджетный роутинг |
| [`outreach/`](outreach/) | Кому писать, шаблоны сообщений, узкие вопросы |
| [`limitations/`](limitations/) | Лицензии, что не стоит склеивать, выводы |


### 2. Сводная таблица зазоров
_Файл: `docs/svyazi-2-0/architecture/gaps.md` | 5 колонок, 5 строк_

| Архитектурный зазор | Уже сильные кандидаты | Что в них уже хорошо закрыто | Что пока остаётся незакрытым | Что брать в MVP |
|---|---|---|---|---|
| Карточка как единица правды | Svyazi, AgentFS | CardIndex, hash/dedup, versionable vault, persistent state | Универсальная типизация для person/project/doc/episode/hypothesis | Card schema + raw/inferred split + immutable IDs citeturn41search0turn27view0turn33view4 |
| Доказуемое основание вывода | research-docs/LiteParse, Legal RAG, Hybrid RAG | Bounding boxes, page-level grounding, coordinates, transparent retrieval | Единый формат «evidence pack» между retrieval и интерфейсом | Page-level viewer + source_id/page/span/box schema citeturn20view5turn20view6turn34view2 |
| Память с контролируемым статусом | NGT Memory, Yodoca, agent-memory-mcp, Memory OS | Associative retrieval, consolidation, forgetting, typed memory, guard rails | Чёткая граница truth/proposal/conflict/decayed | Pending queue + confidence/state machine на наполнение графа citeturn22view4turn21view0turn20view16turn39view3 |
| Оркестрация и review | mclaude, AI Factory, Rufler, Sequential | Locks, mailbox, patch learning, YAML swarm, sequential review | Стандарт handoff для non-code workflow и knowledge moderation | 2–3 роли: extractor → reviewer → publisher citeturn20view2turn20view3turn20view4turn20view11 |
| Безопасный execution plane | LiteLLM, Auto AI Router, Tool Search, SENTINEL | Unified API, lightweight routing, lazy tool loading, runtime guard | Общая policy matrix на tool classes и external skills | Read-only by default + write approval + path allowlist citeturn11search2turn39view0turn39view1turn20view10turn20view16 |


### 3. Интеграционная спецификация (минимум для MVP)
_Файл: `docs/svyazi-2-0/architecture/integration-spec.md` | 4 колонок, 5 строк_

| Контракт | Минимальные поля | Зачем нужен в MVP | На какие идеи опирается |
|---|---|---|---|
| Card Envelope | `card_id`, `card_type`, `state`, `sources`, `edges`, `updated_at`, `payload_hash` | Единый source of truth и dedup/version trace | Svyazi, AgentFS, Memory OS citeturn41search0turn27view0turn39view3 |
| Evidence Envelope | `source_id`, `page_or_span`, `bbox_or_offset`, `method`, `confidence`, `supporting_nodes` | Проверяемость выводов и ручной review | LiteParse, Legal RAG, Hybrid/Graph RAG citeturn20view5turn20view6turn34view2turn34view3 |
| Memory Write Policy | `write_type`, `promotion_rule`, `review_required`, `decay_policy` | Развести факт, эпизод и гипотезу | Yodoca, NGT Memory, agent-memory-mcp citeturn21view0turn22view4turn20view16 |
| Skill Policy | `tool_class`, `approval_mode`, `path_scope`, `network_scope`, `output_target` | Снизить blast radius и упростить audit | Tool Search, SENTINEL, AI Factory practices citeturn39view1turn20view10turn29search6 |
| Review Record | `reviewer_role`, `decision`, `reason`, `evidence_refs`, `follow_up` | Не путать machine suggestion с accepted truth | mclaude, AI Factory, Sequential citeturn20view2turn20view3turn20view11 |


### 4. Развилки в коротком виде
_Файл: `docs/svyazi-2-0/limitations/license-tree.md` | 4 колонок, 7 строк_

| Слой | Permissive путь | BSL/закрытый путь | Замечание |
|---|---|---|---|
| Базовый ingest/CardIndex | свой пересборкой по описанию Svyazi | использовать только как референс архитектуры | код Svyazi в просмотренных источниках закрыт. |
| Долговременная память | Yodoca (Apache 2.0), agent-memory-mcp (TBD), MemNet (MIT) | NGT Memory (BSL 1.1, free for personal) | для коммерческого продукта проверять отдельно. |
| Knowledge layer | knowledge-space (MIT) | — | спокойно. |
| Файловое ядро | AgentFS (MIT) | — | спокойно. |
| Forensic RAG | LiteParse (Apache 2.0) | Hybrid RAG / Legal RAG / Graph RAG (TBD) | в основном статьи без явно заявленной OSS‑лицензии. |
| Routing/security | LiteLLM (MIT, кроме enterprise dirs), Auto AI Router (Apache 2.0) | SENTINEL (TBD) | смешанная картина. |
| Self-improvement | AutoResearch (TBD) | Sequential (research, без OSS) | использовать как pattern, не как dependency. |


### 5. Первые контакты
_Файл: `docs/svyazi-2-0/outreach/first-contacts.md` | 4 колонок, 5 строк_

| Кому писать | Почему именно он или она | Публичный вектор из просмотренных источников | Контакт в источниках |
|---|---|---|---|
| **andrey_chuyan** | Единственный из найденных авторов, у кого уже есть рабочий кейс «карточки коллаборации» и CardIndex‑мышление. citeturn41search0 | Комментарии к статье Svyazi на Хабре. citeturn41search0 | Публичный email/Telegram в просмотренных источниках **не найден**. |
| **Sonia_Black / AnastasiyaW** | Закрывает сразу два слоя: knowledge-space и multi-session coordination через mclaude. citeturn33view3turn20view2turn37search0 | Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn33view0turn37search0 | Публичный прямой контакт **не найден**. |
| **kksudo** | Наиболее важный кандидат для слоя `.agentos/` и compile‑to‑runtime политики. citeturn33view4turn27view0 | Комментарии к статье и GitHub issues в AgentFS. citeturn33view7turn27view0 | Публичный прямой контакт **не найден**. |
| **VitalyOborin** | Сильнейший кандидат на consolidator/forgetting‑слой. citeturn21view0turn21view1turn18search1 | Комментарии к статье Yodoca и GitHub issues/discussions в repo. citeturn38view7turn18search1 | Публичный прямой контакт **не найден**. |
| **spbmolot** | Нужен для ассоциативной памяти и очень дешёвого memory retrieval с graph‑подтягиванием слабых связей. citeturn22view4turn22view5 | Комментарии к статье NGT Memory и GitHub repository. citeturn22view5turn32search2 | Публичный прямой контакт **не найден**. |


### 6. Адресные вопросы
_Файл: `docs/svyazi-2-0/outreach/narrow-questions.md` | 3 колонок, 5 строк_

| Кому | Лучший первый вопрос | Почему именно он |
|---|---|---|
| entity["people","Андрей Чуян","habr author"] | Стоит ли расширять CardIndex до `person/project/episode/evidence`, или для discovery и moderation лучше держать разные индексы? | Это продолжает его реальную архитектурную линию, а не уводит в абстракцию. citeturn41search0 |
| **kksudo** | Что лучше класть в `.agentos`, а что выносить в machine-only state вне vault conventions? | Это вопрос в сердце AgentFS, а не общая просьба о сотрудничестве. citeturn27view0turn33view4 |
| entity["people","Виталий Оборин","software engineer"] | Что сильнее всего влияет на качество памяти: отдельный consolidator, decay или строгая типизация записей? | Это позволяет использовать Yodoca как policy reference, а не как «ещё один ассистент». citeturn21view0turn21view1 |
| **spbmolot** | Где проходит практическая граница между полезной ассоциацией и ложной ко‑активацией тем? | Это самый важный вопрос для community matching. citeturn22view4turn22view5 |
| **авторы knowledge-space / mclaude** | Держать операционные benchmark/gotcha cards в одной базе с reference cards или отдельным слоем? | Это шов между памятью, знаниями и orchestration. citeturn33view2turn20view2 |


### 7. Карта найденных проектов и паттернов
_Файл: `docs/svyazi-2-0/overview/projects-map.md` | 8 колонок, 19 строк_

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


### 8. Минимальная сборка прототипа
_Файл: `docs/svyazi-2-0/prototype/mvp-plan.md` | 4 колонок, 5 строк_

| Контур | Что входит | Зачем | Оценка усилий |
|---|---|---|---|
| Ядро данных | CardIndex‑схема, профили, raw/inferred разделение, файловый vault в стиле AgentFS | Сделать единый source of truth и трассируемый lifecycle карточки | 2–3 дня |
| Ingest и память | LLM extraction + нормализация + NGT Memory **или** Yodoca‑lite | Доказать, что из свободного текста получаются устойчивые профили и связи | 4–6 дней |
| Evidence | LiteParse/research-docs + page‑level viewer | Не просто показать match, а показать основание | 3–4 дня |
| Исполнение | LiteLLM/Auto AI Router + Tool Search + базовые правила безопасности | Удержать стоимость и не утонуть в MCP/context overhead | 2–3 дня |
| Guardrails | PII‑фильтры, allowlists, manual review для inferred | Снизить риск ложных связей и утечек | 1–2 дня |


### 9. Ключевые риски и как их закрывать
_Файл: `docs/svyazi-2-0/prototype/risks.md` | 3 колонок, 5 строк_

| Риск | Почему это важно | Снижение риска |
|---|---|---|
| Schema drift и самовольная «оптимизация» структуры моделью | На extraction‑этапе сильная модель может начать «улучшать» схему вместо исполнения | Держать extraction на constrained schema + низком reasoning, а смысл переносить в post‑processing; это совпадает и с логикой Svyazi, и с выводами Memory OS. citeturn41search0turn39view3 |
| Ложные ассоциации в памяти | Ассоциативная память полезна, но легко порождает шум | Вводить review queue для `inferred`, разделять raw vs normalized, не писать Proposal сразу в Truth‑граф. citeturn41search0turn36search0 |
| Утечка PII в карточки и prompts | Discovery‑система почти неизбежно работает с чувствительными профилями | Повторить Svyazi‑паттерн privacy‑by‑design, хранить контакты отдельно, использовать allowlist/path guard, локальные embeddings там, где можно. citeturn41search0turn20view16turn35search0 |
| Лицензионный тупик на memory‑слое | Не все «open» memory‑решения одинаково permissive | Если нужен строго permissive/commercial‑friendly стек, NGT Memory надо проверять отдельно, потому что в статье указана BSL 1.1 и free‑for‑personal grant; на таком пути проще начать с Yodoca или agent-memory-mcp. citeturn22view5turn18search1turn15search3 |
| Многоагентный хаос раньше пользы | Рой даёт выгоду только после появления handoff/lock и чётких спецификаций | Начинать с mclaude + AI Factory/AIF Handoff, а Rufler/Sequential/AutoResearch добавлять после того, как появилась стабильная spec и критерии качества. citeturn20view2turn20view3turn20view4turn20view11turn20view19 |


### 10. Сводная таблица
_Файл: `docs/svyazi-2-0/prototype/roadmap.md` | 5 колонок, 5 строк_

| Итерация | Главная цель | Минимум, который должен заработать | Оценка усилий | Главный риск |
|---|---|---|---|---|
| Evidence-first core | Из любого suggestions можно перейти к основанию | Unified cards + page/span evidence + manual reviewer UI | 1–2 недели | Переусложнение схемы слишком рано |
| Memory governance | Ассоциации перестают путаться с фактами | Episode store + proposal queue + approval/decay states | 1–2 недели | Ложная уверенность в «умной памяти» без жёсткого review |
| Agented moderation | Рой помогает, а не создаёт шум | extractor/reviewer/publisher roles + handoff/journal | 1–2 недели | Многоагентный хаос без хороших критериев качества |
| Local-first ingestion | Система начинает жить в ежедневном потоке | voice→episode, local vault, selective sync | 1–2 недели | Sync-конфликты и таскание лишних данных наружу |
| Self-improvement loop | Ошибки превращаются в benchmark и patch | benchmark set + nightly eval + rollback policy | 1 неделя на каркас, дальше непрерывно | Большой соблазн автоматизировать раньше, чем появилась метрика |


### 11. Практичный бюджетный роутинг моделей
_Файл: `docs/svyazi-2-0/security/budget-routing.md` | 3 колонок, 6 строк_

| Этап | Дефолт | Когда эскалировать |
|---|---|---|
| Extraction из свободного текста | Локальная или дешёвая модель + строгая schema guidance | Только если extraction‑quality стабильно проваливает ваши acceptance tests |
| Нормализация | Детерминированный код | Практически никогда не переводить это на дорогую модель |
| Retrieval / rerank | Non‑LLM hybrid retrieval или локальный reranker | При multi-hop вопросах и слабой explainability |
| Объяснение матча / summary | Средний облачный tier | Если нужен высокий stylistic quality, а не только фактология |
| Финальный внешний отчёт | Сильная модель | Только для user-facing/public/legal‑style текста |
| Ночной ресёрч / оптимизация | AutoResearch‑подход с жёстким бюджетом и rollback | Когда уже есть benchmark и понятная функция качества |


### 12. Что стоит зафиксировать как default policy
_Файл: `docs/svyazi-2-0/security/default-policy.md` | 3 колонок, 6 строк_

| Контроль | Практический дефолт | Основание |
|---|---|---|
| Разделение tool‑классов | По умолчанию разрешать read‑only tools; любые send/write/delete/execute — только через явный approval | Автономный агент отличается от чатбота именно доступом к реальным действиям; это и создаёт катастрофы. citeturn34view5 |
| Quarantine для external skills/MCP | Любой внешний skill/MCP сначала в sandbox, потом статический/репутационный скан, потом allowlist | AI Factory прямо предупреждает о prompt injection в SKILL.md и запускает двухуровневый security scan. citeturn29search6 |
| Path allowlist | Жёстко ограничить, что агент вообще может читать и писать на диске | `agent-memory-mcp` демонстрирует хороший паттерн Path Guard/allowlist против traversal и выхода за пределы проекта. citeturn20view16 |
| PII separation | Любые контакты, email, Telegram, ссылки — в отдельном raw‑слое; в карточки уходит только очищенный профиль | Так делает Svyazi; это правильный privacy‑baseline для людей и сообществ. citeturn41search0 |
| Truth vs Proposal | `inferred` и weak signals не писать сразу в «истину», а ставить в pending review | И Svyazi, и более тяжёлые memory‑системы сходятся на нужде в review‑контуре. citeturn41search0turn36search0 |
| Runtime firewall | Между агентом и mutating tools держать специализированный защитный слой | Именно для этого и нужен SENTINEL‑подобный слой, а не только «умный промпт». citeturn20view10 |


## technology-combinations (13 таблиц)


### 1. Подпапки
_Файл: `docs/technology-combinations/README.md` | 2 колонок, 5 строк_

| Подпапка | Что внутри |
|---|---|
| [`combinations/`](combinations/) | 35 комбинаций — по одному файлу на каждую |
| [`synthesis-tables/`](synthesis-tables/) | Сводные таблицы по диапазонам комбинаций |
| [`mega-stacks/`](mega-stacks/) | Четыре мегастека: 1.0, 2.0 (DSL/AST 3.0), 4.0 (Event Sourcing & Consensus) |
| [`research-reports/`](research-reports/) | Два больших Markdown‑отчёта‑артефакта по итогам диалога |
| [`properties/`](properties/) | Каркас под заметки о конкретных эмерджентных свойствах |


### 2. Комбинация 8: Conductor × adversarial-review × Auto AI Route
_Файл: `docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md` | 3 колонок, 7 строк_

| Комбинация | Кубики | Уникальный результат | Экономия/ROI
| 1 | Агентская архитектура + Svyazi | Самообучающиеся промпты, multi-domain профилирование | 70% времени на модерацию
| 2 | Мультиагенты + Router | Иерархический роутинг, fault tolerance | 80% бюджета на LLM
| 3 | CRDT + Svyazi | P2P граф сообщества, offline-first discovery | Нулевые расходы на сервер
| 4 | LLM-парсинг + Graph-RAG + Агенты | Self-building knowledge graph | 95% точность vs 60% обычного RAG
| 5 | SourceCraft + Claude Code + Sequential | Distributed code review, team knowledge graph | 44% выше качества vs координатор
| 6 | OpenClaude + ZINC + MoME | Локальный агент с Q6-роутером | 100% privacy, $0/мес API
| 7 | Crawl4AI + Docling + Yodoca | Self-consolidating legal corpus | Автоматическая актуализация
| 8 | Conductor + adversarial + Router | Multi-model adversarial, enterprise review | 3× ускорение ревью


### 3. Комбинация 14: local-first Agent Development Environment
_Файл: `docs/technology-combinations/combinations/14-local-first-agent-development-environment.md` | 3 колонок, 5 строк_

| Combo | Components | Unique Result | Economic Impact
| 9 | Agent-Bridge + Conductor + Sequential | Visual multi-machine agent IDE | 1 dev = 10 agents = $700/mo
| 10 | LLM-parsing + Docling + Svyazi | Auto-building legal corpus | 10 sec search vs 2 hr manual
| 11 | CRDT + PostgreSQL 18 async + TimescaleDB | Real-time collaborative DB | 100k ops/sec, zero conflicts
| 12 | OpenTelemetry + Prometheus + AgentStack | Multi-agent observability | Detect bottleneck in 60 sec
| 13 | COBOL transpiler pattern + LLM + templates | Legal document transpiler | 50k docs structured in 1 day
| 14 | OpenClaude + ZINC + CRDT + Agent-Bridge | Local-first multi-agent env | $0/mo, 100% GDPR compliant


### 4. Комбинация 19: Multi-Agent Observability Platform
_Файл: `docs/technology-combinations/combinations/19-multi-agent-observability-platform.md` | 3 колонок, 4 строк_

| Combo | Components | Unique Result | Economic Impact
| 15 | Crawl4AI + Docling + Ebbinghaus | Self-consolidating legal corpus | Auto-maintains, forgets stale
| 16 | Adversarial + Sequential + Router | Multi-model review pipeline | 3× faster, 44% quality boost
| 17 | agentmemory + CRDT + Graph-RAG | P2P agent knowledge graph | $0 server, biological memory
| 18 | Crawl4AI + Svyazi + Pydantic | Automated legal DB builder | 50k docs, 95% accuracy
| 19 | OpenTelemetry + Agent-Bridge | Multi-agent observability | Real-time bottleneck detection


### 5. Комбинация 24: MEGA-INTEGRATION: Full Stack
_Файл: `docs/technology-combinations/combinations/24-mega-integration-full-stack.md` | 3 колонок, 4 строк_

| # | Components | Unique Result | Impact
| 20 | ClickHouse + CRDT + PG18 async | Hybrid OLAP/OLTP real-time | Best of 3 worlds
| 21 | ClickHouse + Crawl4AI + Pydantic | Legal corpus analytics | 100M rows in <500ms
| 22 | ClickHouse + CatBoost + Graph-RAG | ML outcome prediction | 73-89% accuracy
| 23 | CyberCodeReview + Adversarial + Sequential | Russian compliance pipeline | ФСТЭК automated
| 24 | ALL ABOVE | Full legal-AI stack | Production-grade system


### 6. Комбинация 30: MEGA-STACK 3.0 with DSL & AST
_Файл: `docs/technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md` | 3 колонок, 5 строк_

| # | Components | Result | Impact
| 25 | Python AST + DSL + Pydantic | Legal document transpiler | 50k docs in 1 day
| 26 | AST + ASTChunk + LLM | Code analysis for legal automation | Self-documenting code
| 27 | ASTChunk + Graph-RAG + ClickHouse | Code + precedents unified KB | Developer↔lawyer bridge
| 28 | Pydantic + Sequential + Adversarial | Type-safe legal workflows | Errors caught in seconds
| 29 | DSL + AST + Templates | Meta-programmatic templates | Write once, deploy everywhere
| 30 | ALL ABOVE | Complete legal-AI + DSL stack | Production system with DSL


### 7. Комбинация 35: MEGA-STACK 4.0 with Event Sourcing & Consensu
_Файл: `docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md` | 3 колонок, 4 строк_

| # | Components | Result | Impact
| 31 | Event Sourcing + CQRS + ClickHouse | Audit-complete legal case mgmt | Time-travel queries
| 32 | Raft + Multi-agent + CRDT | Consensus-based agent cluster | Fault-tolerant coordination
| 33 | Event Sourcing + Kafka + ClickHouse | Real-time legal analytics | Write once, read many ways
| 34 | Paxos + Event Store + Multi-DC | Geo-replicated document store | Byzantine fault tolerance
| 35 | ALL ABOVE | Complete distributed legal-AI | Production-grade resilience


### 8. Сводная таблица 1–8
_Файл: `docs/technology-combinations/synthesis-tables/01-08-summary.md` | 4 колонок, 8 строк_

| Комбинация | Кубики | Уникальный результат | Экономия/ROI |
|---|---|---|---|
| [1](../combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md) | Агентская архитектура + Svyazi | Самообучающиеся промпты, multi‑domain профилирование | 70% времени на модерацию |
| [2](../combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md) | Мультиагенты + Router | Иерархический роутинг, fault tolerance | 80% бюджета на LLM |
| [3](../combinations/03-crdt-local-first-svyazi-cardindex.md) | CRDT + Svyazi | P2P граф сообщества, offline‑first discovery | Нулевые расходы на сервер |
| [4](../combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md) | LLM‑парсинг + Graph‑RAG + Агенты | Self‑building knowledge graph | 95% точность vs 60% обычного RAG |
| [5](../combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md) | SourceCraft + Claude Code + Sequential | Distributed code review, team knowledge graph | 44% выше качества vs координатор |
| [6](../combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md) | OpenClaude + ZINC + MoME | Локальный агент с Q6‑роутером | 100% privacy, $0/мес API |
| [7](../combinations/07-crawl4ai-docling-yodoca-consolidator.md) | Crawl4AI + Docling + Yodoca | Self‑consolidating legal corpus | Автоматическая актуализация |
| [8](../combinations/08-conductor-adversarial-review-auto-ai-router.md) | Conductor + adversarial + Router | Multi‑model adversarial, enterprise review | 3× ускорение ревью |


### 9. Сводная таблица 9–14 (Extended)
_Файл: `docs/technology-combinations/synthesis-tables/09-14-extended.md` | 4 колонок, 6 строк_

| Combo | Components | Unique Result | Economic Impact |
|---|---|---|---|
| [9](../combinations/09-agent-orchestration-stack.md) | Agent‑Bridge + Conductor + Sequential | Visual multi‑machine agent IDE | 1 dev = 10 agents = $700/mo |
| [10](../combinations/10-legal-document-intelligence-pipeline.md) | LLM‑parsing + Docling + Svyazi | Auto‑building legal corpus | 10 sec search vs 2 hr manual |
| [11](../combinations/11-hybrid-crdt-sql-database.md) | CRDT + PostgreSQL 18 async + TimescaleDB | Real‑time collaborative DB | 100k ops/sec, zero conflicts |
| [12](../combinations/12-multi-agent-observability-stack.md) | OpenTelemetry + Prometheus + AgentStack | Multi‑agent observability | Detect bottleneck in 60 sec |
| [13](../combinations/13-legal-document-transpiler.md) | COBOL transpiler pattern + LLM + templates | Legal document transpiler | 50k docs structured in 1 day |
| [14](../combinations/14-local-first-agent-development-environment.md) | OpenClaude + ZINC + CRDT + Agent‑Bridge | Local‑first multi‑agent env | $0/mo, 100% GDPR compliant |


### 10. Сводная таблица 15–19 (Extended)
_Файл: `docs/technology-combinations/synthesis-tables/15-19-extended.md` | 4 колонок, 5 строк_

| Combo | Components | Unique Result | Economic Impact |
|---|---|---|---|
| [15](../combinations/15-self-consolidating-legal-corpus.md) | Crawl4AI + Docling + Ebbinghaus | Self‑consolidating legal corpus | Auto‑maintains, forgets stale |
| [16](../combinations/16-adversarial-multi-agent-code-review.md) | Adversarial + Sequential + Router | Multi‑model review pipeline | 3× faster, 44% quality boost |
| [17](../combinations/17-distributed-agent-memory-with-graph.md) | agentmemory + CRDT + Graph‑RAG | P2P agent knowledge graph | $0 server, biological memory |
| [18](../combinations/18-llm-powered-legal-corpus-builder.md) | Crawl4AI + Svyazi + Pydantic | Automated legal DB builder | 50k docs, 95% accuracy |
| [19](../combinations/19-multi-agent-observability-platform.md) | OpenTelemetry + Agent‑Bridge | Multi‑agent observability | Real‑time bottleneck detection |


### 11. Сводная таблица 20–24 (Final 1–24)
_Файл: `docs/technology-combinations/synthesis-tables/20-24-final.md` | 4 колонок, 5 строк_

| # | Components | Unique Result | Impact |
|---|---|---|---|
| [20](../combinations/20-hybrid-olap-oltp-with-real-time-sync.md) | ClickHouse + CRDT + PG18 async | Hybrid OLAP/OLTP real‑time | Best of 3 worlds |
| [21](../combinations/21-legal-corpus-analytics-at-scale.md) | ClickHouse + Crawl4AI + Pydantic | Legal corpus analytics | 100M rows in <500ms |
| [22](../combinations/22-russian-international-oss-stack.md) | ClickHouse + CatBoost + Graph‑RAG | ML outcome prediction | 73–89% accuracy |
| [23](../combinations/23-security-first-code-review-pipeline.md) | CyberCodeReview + Adversarial + Sequential | Russian compliance pipeline | ФСТЭК automated |
| [24](../combinations/24-mega-integration-full-stack.md) | ALL ABOVE | Full legal‑AI stack | Production‑grade system |


### 12. Сводная таблица 25–30 (Complete 1–30)
_Файл: `docs/technology-combinations/synthesis-tables/25-30-extended.md` | 4 колонок, 6 строк_

| # | Components | Result | Impact |
|---|---|---|---|
| [25](../combinations/25-legal-dsl-code-transpiler.md) | Python AST + DSL + Pydantic | Legal document transpiler | 50k docs in 1 day |
| [26](../combinations/26-ast-based-code-analysis-for-legal-automation.md) | AST + ASTChunk + LLM | Code analysis for legal automation | Self‑documenting code |
| [27](../combinations/27-hybrid-rag-with-ast-chunked-code.md) | ASTChunk + Graph‑RAG + ClickHouse | Code + precedents unified KB | Developer↔lawyer bridge |
| [28](../combinations/28-pydantic-enforced-legal-workflows.md) | Pydantic + Sequential + Adversarial | Type‑safe legal workflows | Errors caught in seconds |
| [29](../combinations/29-meta-programmatic-legal-template-generator.md) | DSL + AST + Templates | Meta‑programmatic templates | Write once, deploy everywhere |
| [30](../combinations/30-mega-stack-3-0-with-dsl-ast.md) | ALL ABOVE | Complete legal‑AI + DSL stack | Production system with DSL |


### 13. Сводная таблица 31–35 (Complete 1–35)
_Файл: `docs/technology-combinations/synthesis-tables/31-35-final.md` | 4 колонок, 5 строк_

| # | Components | Result | Impact |
|---|---|---|---|
| [31](../combinations/31-event-sourced-legal-document-history.md) | Event Sourcing + CQRS + ClickHouse | Audit‑complete legal case mgmt | Time‑travel queries |
| [32](../combinations/32-consensus-based-multi-agent-coordination.md) | Raft + Multi‑agent + CRDT | Consensus‑based agent cluster | Fault‑tolerant coordination |
| [33](../combinations/33-event-sourcing-cqrs-clickhouse-analytics.md) | Event Sourcing + Kafka + ClickHouse | Real‑time legal analytics | Write once, read many ways |
| [34](../combinations/34-distributed-event-store-with-paxos.md) | Paxos + Event Store + Multi‑DC | Geo‑replicated document store | Byzantine fault tolerance |
| [35](../combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md) | ALL ABOVE | Complete distributed legal‑AI | Production‑grade resilience |


## templates (41 таблиц)


### 1. Скилы агента
_Файл: `docs/templates/agent-spec.md` | 3 колонок, 2 строк_

| Скилл | Откуда | Когда применяет |
|-------|--------|-----------------|
| [скилл 1] | [`docs/.claude/skills/...`] | [триггер] |
| [скилл 2] | | |


### 2. Tools (плагины)
_Файл: `docs/templates/agent-spec.md` | 3 колонок, 2 строк_

| MCP-сервер | Инструменты | Зачем |
|------------|-------------|-------|
| lorenzo-search | search_docs, … | поиск контекста |
| … | | |


### 3. Память
_Файл: `docs/templates/agent-spec.md` | 4 колонок, 4 строк_

| Тип памяти | Хранилище | Объём | Срок жизни |
|------------|-----------|-------|-----------|
| Working | in-context | 200K tokens | сессия |
| Episodic | … | … | 30 дней |
| Semantic | search_index.json | весь корпус | вечно |
| Procedural | скилы | — | — |


### 4. Decision boundary
_Файл: `docs/templates/agent-spec.md` | 4 колонок, 5 строк_

| Класс решения | Сам агент | С подтверждением | Только человек |
|---------------|-----------|------------------|----------------|
| Чтение docs | ✅ | | |
| Edit файла | | ✅ | |
| Push в remote | | | ✅ |
| Финансовые | | | ✅ |
| Связь с авторами | | ✅ | |


### 5. Профиль
_Файл: `docs/templates/contact-outreach.md` | 2 колонок, 4 строк_

| Параметр | Значение |
|----------|---------|
| Имя | [имя] |
| GitHub | [@handle](ссылка) |
| Проекты | [список] |
| Платформа | [Habr/GitHub/Telegram] |


### 6. Рассмотренные варианты
_Файл: `docs/templates/decision-record.md` | 3 колонок, 3 строк_

| Вариант | Плюсы | Минусы |
|---------|-------|--------|
| A | | |
| B | | |
| C | | |


### 7. Компоненты
_Файл: `docs/templates/ensemble.md` | 3 колонок, 2 строк_

| Компонент | Роль | Лицензия |
|-----------|------|----------|
| [Проект A] | [роль] | [лицензия] |
| [Проект B] | [роль] | [лицензия] |


### 8. Журнал
_Файл: `docs/templates/experiment-log.md` | 4 колонок, 2 строк_

| Дата | Действие | Замер | Заметка |
|------|----------|-------|---------|
| 2026-04-29 | start | — | Начали эксперимент |
| | | | |


### 9. История обновлений
_Файл: `docs/templates/faq-entry.md` | 3 колонок, 1 строк_

| Дата | Что обновили | Кто |
|------|--------------|-----|
| 2026-04-29 | Создан | — |


### 10. Детальные метрики
_Файл: `docs/templates/kpi-snapshot.md` | 5 колонок, 7 строк_

| Метрика | Значение | Цель | Δ vs прошлая | Статус |
|---------|----------|------|--------------|--------|
| HEALTH score | | 80 | | 🟢/🟡/🔴 |
| Файлов в docs/ | | | | |
| Слов | | | | |
| Битых ссылок | | 0 | | |
| Покрытие тегов | | 90% | | |
| Контактов написано | | | | |
| Контактов ответили | | | | |


### 11. Идентификация
_Файл: `docs/templates/legal-case.md` | 2 колонок, 6 строк_

| Параметр | Значение |
|----------|---------|
| Aktenzeichen | [A 1 SO 123/24] |
| Тип | [Sozialgericht / Verwaltungsgericht / …] |
| Stage | [Antrag / Bescheid / Widerspruch / Klage / Berufung] |
| Filed | [дата] |
| Deadline | [дата] |
| Status | [open / closed / appeal] |


### 12. Стороны
_Файл: `docs/templates/legal-case.md` | 2 колонок, 2 строк_

| Роль | Кто |
|------|-----|
| Antragsteller / Kläger | [имя] |
| Behörde / Beklagte | [имя] |


### 13. Хронология
_Файл: `docs/templates/legal-case.md` | 3 колонок, 3 строк_

| Дата | Событие | Документ |
|------|---------|----------|
| YYYY-MM-DD | Antrag eingereicht | [файл] |
| YYYY-MM-DD | Bescheid erhalten | [файл] |
| YYYY-MM-DD | Widerspruch | [файл] |


### 14. Прецеденты
_Файл: `docs/templates/legal-case.md` | 4 колонок, 1 строк_

| Решение | Суд | Дата | Релевантность |
|---------|-----|------|---------------|
| [BSG B 14 AS 1/22 R] | BSG | 2022-XX | [как относится] |


### 15. Участники
_Файл: `docs/templates/meeting-notes.md` | 3 колонок, 1 строк_

| Имя | Роль | Платформа |
|-----|------|-----------|
| [имя] | [роль] | [GitHub/Habr/Telegram] |


### 16. 1. UI / Client
_Файл: `docs/templates/mega-stack.md` | 3 колонок, 1 строк_

| Компонент | Лицензия | Зрелость |
|-----------|----------|----------|
| | | |


### 17. 2. Agent Layer
_Файл: `docs/templates/mega-stack.md` | 3 колонок, 1 строк_

| Компонент | Тип агента | Откуда |
|-----------|------------|--------|
| | | |


### 18. 3. Orchestration
_Файл: `docs/templates/mega-stack.md` | 3 колонок, 0 строк_

| Компонент | Паттерн | … |
|-----------|---------|---|


### 19. 4. RAG / Search
_Файл: `docs/templates/mega-stack.md` | 3 колонок, 0 строк_

| Компонент | Тип | Узлы |
|-----------|-----|------|


### 20. Cross-layer контракты
_Файл: `docs/templates/mega-stack.md` | 3 колонок, 2 строк_

| Слой → слой | Формат | Протокол |
|-------------|--------|----------|
| Ingestion → Storage | JSON | HTTP REST |
| Storage → RAG | … | … |


### 21. Стоимость
_Файл: `docs/templates/mega-stack.md` | 2 колонок, 4 строк_

| Категория | $/месяц |
|-----------|---------|
| LLM API | |
| Хостинг | |
| Платные лицензии | |
| **Итого** | |


### 22. Риски и митигации
_Файл: `docs/templates/mega-stack.md` | 3 колонок, 1 строк_

| Риск | Severity | Митигация |
|------|----------|-----------|
| | | |


### 23. Альтернативные стеки
_Файл: `docs/templates/mega-stack.md` | 2 колонок, 1 строк_

| Альтернатива | Когда лучше |
|--------------|-------------|
| | |


### 24. Статус
_Файл: `docs/templates/project-component.md` | 2 колонок, 4 строк_

| Параметр | Значение |
|----------|---------|
| Версия   | [x.y.z] |
| Лицензия | [MIT/Apache/BSL] |
| Язык     | [Python/TypeScript/Rust] |
| Репо     | [ссылка] |


### 25. 2. Terminology
_Файл: `docs/templates/protocol-spec.md` | 2 колонок, 2 строк_

| Термин | Определение |
|--------|-------------|
| **Endpoint** | … |
| **Adapter** | … |


### 26. 5. Compatibility Levels
_Файл: `docs/templates/protocol-spec.md` | 2 колонок, 4 строк_

| Level | Что означает |
|-------|-------------|
| L0 | Read-only |
| L1 | Read + write локально |
| L2 | Federation (взаимная видимость) |
| L3 | Active collaboration |


### 27. Appendix B. Change Log
_Файл: `docs/templates/protocol-spec.md` | 3 колонок, 1 строк_

| Версия | Дата | Изменения |
|--------|------|-----------|
| 0.1 | 2026-04-29 | Initial draft |


### 28. Состав
_Файл: `docs/templates/prototype-mvp.md` | 4 колонок, 3 строк_

| Слой | Компонент | Статус | Откуда |
|------|-----------|--------|--------|
| memory | [компонент] | [готов/нужен] | [`docs/...md`] |
| knowledge | … | | |
| ingestion | … | | |


### 29. Риски
_Файл: `docs/templates/prototype-mvp.md` | 3 колонок, 2 строк_

| Риск | Severity | Митигация |
|------|----------|-----------|
| Компонент A не работает с B | high | [план B] |
| Латентность > target | medium | [оптимизация] |


### 30. Финансовая оценка
_Файл: `docs/templates/prototype-mvp.md` | 2 колонок, 3 строк_

| Категория | Стоимость |
|-----------|-----------|
| LLM tokens | $ |
| Хостинг | $ |
| **Итого** | $ |


### 31. Метрики периода
_Файл: `docs/templates/retrospective.md` | 4 колонок, 3 строк_

| Метрика | План | Факт | Δ |
|---------|------|------|---|
| Задач закрыто | | | |
| HEALTH score | | | |
| Контактов написано | | | |


### 32. 1.3 Terminology
_Файл: `docs/templates/rfc.md` | 2 колонок, 1 строк_

| Термин | Определение |
|--------|-------------|
| [Термин 1] | [определение] |


### 33. Appendix A. Change Log
_Файл: `docs/templates/rfc.md` | 3 колонок, 1 строк_

| Версия | Дата | Что изменилось |
|--------|------|---------------|
| 0.1 | 2026-04-29 | Initial draft |


### 34. Оценка
_Файл: `docs/templates/risk-entry.md` | 2 колонок, 4 строк_

| Параметр | Значение |
|----------|----------|
| Вероятность | [low \| medium \| high \| certain] |
| Влияние | [low \| medium \| high \| critical] |
| Risk Score | [P × I, 1-25] |
| Зона | [зелёная \| жёлтая \| красная] |


### 35. История
_Файл: `docs/templates/risk-entry.md` | 3 колонок, 1 строк_

| Дата | Событие | Кто |
|------|---------|-----|
| 2026-04-29 | Риск идентифицирован | [Имя] |


### 36. Компонент A
_Файл: `docs/templates/tech-pair.md` | 2 колонок, 5 строк_

| Параметр | Значение |
|----------|---------|
| Название | [A] |
| Автор / репо | [@author / repo] |
| Слой | [memory / knowledge / …] |
| Категория | [hardware / software / deep] |
| Зрелость | [exp / alpha / beta / stable] |


### 37. Компонент A
_Файл: `docs/templates/tech-pair.md` | 2 колонок, 3 строк_

| Параметр | Значение |
|----------|---------|
| Название | [B] |
| Автор / репо | [@author / repo] |
| Слой | … |


### 38. Ring
_Файл: `docs/templates/tech-radar-entry.md` | 2 колонок, 4 строк_

| Кольцо | Что значит |
|--------|-----------|
| **Adopt** | Используем, рекомендуем всем |
| **Trial** | Стоит пробовать на боевых проектах |
| **Assess** | Изучить, понять, может пригодиться |
| **Hold** | Избегать на новых проектах |


### 39. Альтернативы
_Файл: `docs/templates/tech-radar-entry.md` | 3 колонок, 2 строк_

| Альтернатива | Ring | Когда лучше |
|--------------|------|-------------|
| [Технология A] | [ring] | [когда] |
| [Технология B] | [ring] | [когда] |


### 40. История перемещений
_Файл: `docs/templates/tech-radar-entry.md` | 4 колонок, 1 строк_

| Дата | Из кольца | В кольцо | Причина |
|------|-----------|----------|---------|
| 2026-04-29 | — | [новое] | [причина] |


### 41. Метрики недели
_Файл: `docs/templates/weekly-digest.md` | 4 колонок, 4 строк_

| Метрика | Было | Стало | Δ |
|---------|------|-------|---|
| Файлов в docs/ | | | |
| Слов | | | |
| HEALTH score | | | |
| Битых ссылок | | | |


<!-- see-also -->

---

**Смотрите также:**
- [OUTLINE](docs/OUTLINE.md)
- [CONCEPTS](docs/CONCEPTS.md)
- [READABILITY](docs/READABILITY.md)
- [SITEMAP](docs/SITEMAP.md)

