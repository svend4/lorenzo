# Резюме документов (TextRank)

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** citeturn21view0turn21view1turn18search1 Комментарии к статье Yodoca и GitHub issues/discussions в repo.
> 🔧 **Подход:** В‑третьих, нужен memory governance layer , который не даёт ассоциативной памяти записывать предлагаемое как истинное.
> ✅ **Результат:** В‑третьих, нужен memory governance layer , который не даёт ассоциативной памяти записывать предлагаемое как истинное.
> 🏷️ **Ключевые слова:** `anthropic`, `vacancies`, `svyazi`, `triangle`, `nautilus`, `portal`, `protocol`, `double`
>


<!-- toc-auto -->
## Contents

- [docs/01-svyazi/01-executive-summary.md](#docs01-svyazi01-executive-summarymd)
- [docs/01-svyazi/02-methodology.md](#docs01-svyazi02-methodologymd)
- [docs/01-svyazi/03-component-catalog.md](#docs01-svyazi03-component-catalogmd)
- [docs/01-svyazi/04-ensembles-overview.md](#docs01-svyazi04-ensembles-overviewmd)
- [docs/01-svyazi/06-security-privacy.md](#docs01-svyazi06-security-privacymd)
- [docs/01-svyazi/07-mvp-planning.md](#docs01-svyazi07-mvp-planningmd)
- [docs/01-svyazi/08-conclusions.md](#docs01-svyazi08-conclusionsmd)
- [docs/01-svyazi/09-architectural-gaps.md](#docs01-svyazi09-architectural-gapsmd)
- [docs/01-svyazi/10-second-order-ensembles.md](#docs01-svyazi10-second-order-ensemblesmd)
- [docs/01-svyazi/11-integration-contracts.md](#docs01-svyazi11-integration-contractsmd)
- [docs/01-svyazi/12-roadmap.md](#docs01-svyazi12-roadmapmd)
- [docs/01-svyazi/13-contacts.md](#docs01-svyazi13-contactsmd)
- [docs/01-svyazi/14-limitations.md](#docs01-svyazi14-limitationsmd)
- [docs/01-svyazi/README.md](#docs01-svyazireadmemd)
- [docs/02-anthropic-vacancies/00-intro.md](#docs02-anthropic-vacancies00-intromd)
- [docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md](#docs02-anthropic-vacancies01-интегральный-анализ-профиля-svend4md)
- [docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md](#docs02-anthropic-vacancies02-общий-план-развития-nautilus-portal-protocolmd)
- [docs/02-anthropic-vacancies/06-1-introduction.md](#docs02-anthropic-vacancies06-1-introductionmd)
- [docs/02-anthropic-vacancies/07-2-terminology.md](#docs02-anthropic-vacancies07-2-terminologymd)
- [docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md](#docs02-anthropic-vacancies08-3-registry-nautilus-jsonmd)
- [docs/02-anthropic-vacancies/104-appendix-c-references.md](#docs02-anthropic-vacancies104-appendix-c-referencesmd)
- [docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md](#docs02-anthropic-vacancies107-1-контекст-и-мотивацияmd)
- [docs/02-anthropic-vacancies/108-2-формальный-workflow.md](#docs02-anthropic-vacancies108-2-формальный-workflowmd)
- [docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md](#docs02-anthropic-vacancies109-3-принципы-консолидации-фаза-cmd)
- [docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md](#docs02-anthropic-vacancies110-вопрос-fallback-ratio-как-критический-или-осмысленmd)
- [docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md](#docs02-anthropic-vacancies112-5-связь-с-существующими-методологиямиmd)
- [docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md](#docs02-anthropic-vacancies114-7-реализация-в-проекте-nautilusmd)
- [docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md](#docs02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd)
- [docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md](#docs02-anthropic-vacancies116-9-checklist-применения-методологииmd)
- [docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md](#docs02-anthropic-vacancies117-10-конкретный-план-применения-к-текущим-документамmd)
- [docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md](#docs02-anthropic-vacancies119-appendix-b-примеры-расхождений-и-их-разрешенияmd)
- [docs/02-anthropic-vacancies/122-глоссарий.md](#docs02-anthropic-vacancies122-глоссарийmd)
- [docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md](#docs02-anthropic-vacancies124-конфигурация-для-claude-desktopmd)
- [docs/02-anthropic-vacancies/130-отладка.md](#docs02-anthropic-vacancies130-отладкаmd)
- [docs/02-anthropic-vacancies/133-обратная-связь.md](#docs02-anthropic-vacancies133-обратная-связьmd)
- [docs/02-anthropic-vacancies/136-abstract.md](#docs02-anthropic-vacancies136-abstractmd)
- [docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md](#docs02-anthropic-vacancies138-1-why-single-triangle-models-are-incompletemd)
- [docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md](#docs02-anthropic-vacancies139-2-the-double-triangle-architecturemd)
- [docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md](#docs02-anthropic-vacancies140-3-three-inter-layer-protocolsmd)
- [docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md](#docs02-anthropic-vacancies141-4-nautilus-portal-as-reference-substratemd)
- [docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md](#docs02-anthropic-vacancies142-5-pattern-library-as-bridge-between-trianglesmd)
- [docs/02-anthropic-vacancies/143-6-four-deployment-domains.md](#docs02-anthropic-vacancies143-6-four-deployment-domainsmd)
- [docs/02-anthropic-vacancies/144-7-open-questions.md](#docs02-anthropic-vacancies144-7-open-questionsmd)
- [docs/02-anthropic-vacancies/145-8-call-to-action.md](#docs02-anthropic-vacancies145-8-call-to-actionmd)
- [docs/02-anthropic-vacancies/146-acknowledgments.md](#docs02-anthropic-vacancies146-acknowledgmentsmd)
- [docs/02-anthropic-vacancies/147-references.md](#docs02-anthropic-vacancies147-referencesmd)
- [docs/02-anthropic-vacancies/148-appendix-a-glossary.md](#docs02-anthropic-vacancies148-appendix-a-glossarymd)
- [docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md](#docs02-anthropic-vacancies149-appendix-b-summary-of-contributionsmd)
- [docs/02-anthropic-vacancies/150-appendix-c-version-history.md](#docs02-anthropic-vacancies150-appendix-c-version-historymd)
- [docs/02-anthropic-vacancies/153-executive-summary.md](#docs02-anthropic-vacancies153-executive-summarymd)


_Обновлено: 2026-04-29_

Файлов: **291** | Предложений: **3** на документ

## `docs/01-svyazi/01-executive-summary.md`

_Svyazi[^svyazi] 2.0 — Исполнительное резюме_

> Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для Svyazi‑2.0 : ingestion и нормализация профи Проекты: Svyazi, CardIndex ^cardindex , AgentFS ^agentfs , mclaude, AI Factory, Rufler ^rufler , LiteParse, Legal RAG ^rag --- Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для Svyazi‑2.0 : ingestion и нормализация профилей из свободного текста, agent‑first knowledge base, файлосистемная память для агентов, ассоциативная и консолидируемая долговременная память, визуально проверяемый RAG, многоагентная оркестрация, безопасный MCP ^mcp ‑слой, локальный voice→vault вход и бюджетно‑осознанный роутинг моделей. Для многоагентной работы уже есть mclaude, AI Factory, AIF Handoff, Rufler и протокол Sequential; для forensic‑режима — research-docs/LiteParse, Legal RAG, Hybrid RAG и Graph RAG; для безопасного и дешёвого исполнения — Tool Search, LiteLLM, Auto AI Router, RLM-Toolkit и SENTINEL ^sentinel . Первое — Svyazi + AgentFS + NGT/Yodoca + LiteParse: даёт уже полезный MVP 2.

## `docs/01-svyazi/02-methodology.md`

_Методика и рамка отбора проектов_

> Поиск вёлся с приоритетом на Хабр как первичный слой описания идеи и на репозитории как первичный слой верификации лицензии, зрелости и интеграционного интерфейса . Проекты: Svyazi ^svyazi , LiteParse, Legal RAG ^rag , Graph RAG --- Поиск вёлся с приоритетом на Хабр как первичный слой описания идеи и на репозитории как первичный слой верификации лицензии, зрелости и интеграционного интерфейса . Доказуемость — можно ли проверить, что слой работает правильно?

## `docs/01-svyazi/03-component-catalog.md`

_03-component-catalog_

> citeturn33view1turn37search1 Высокая : это внешний knowledge layer для агентов и нормализатора. citeturn22view3turn32search2 Очень высокая : быстрый ассоциативный memory‑слой для discovery и matching. citeturn15search3turn39view3 Высокая : слой typed memory и governance для более поздних итераций.

## `docs/01-svyazi/04-ensembles-overview.md`

_04-ensembles-overview_

> citeturn20view11 Ансамбль D — Voice‑first local knowledge mesh Для реальных пользователей и операторов Svyazi‑2.0 важно не только “искать по базе”, но и пополнять её без боли. citeturn21view10turn35search0 - Локальная обработка вместо облачной утечки контекста : и локальный speech‑to‑text, и local‑first workspace, и CRDT ^crdt ‑sync работают в модели “данные принадлежат устройству пользователя”. citeturn11search2turn39view0turn39view1turn20view18turn20view10 Ожидаемые новые свойства: - Реальная экономия контекста ещё до первого токена работы : в кейсе Tool Search MCP‑overhead упал с 82k до 5.7k токенов, а свободное окно выросло на 76k.

## `docs/01-svyazi/06-security-privacy.md`

_06-security-privacy_

> Для Svyazi ^svyazi ‑2.0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP ^mcp servers, импорты документов и memory writes потенциально недоверенными . Это не паранойя, Проекты: Svyazi, AgentFS ^agentfs , AI Factory, agent-memory-mcp, SENTINEL ^sentinel , LiteLLM, Auto AI Router, Tool Search --- Для Svyazi‑2.0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP servers, импорты документов и memory writes потенциально недоверенными . Если нужен самый дешёвый режим — запускать extraction, indexing и basic memory на локальной модели, а в облако отправлять только ambiguous ranking и финальное объяснение.

## `docs/01-svyazi/07-mvp-planning.md`

_07-mvp-planning_

> citeturn33view3turn20view2turn37search0 Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn21view0turn21view1turn18search1 Комментарии к статье Yodoca и GitHub issues/discussions в repo. citeturn22view4turn22view5 Комментарии к статье NGT Memory и GitHub repository.

## `docs/01-svyazi/08-conclusions.md`

_08-conclusions_

> По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитектуры заново. Самый дефицитный слой — не память, не RAG ^rag и не оркестр Проекты: Svyazi ^svyazi , CardIndex ^cardindex , AgentFS ^agentfs , mclaude, AI Factory, Rufler ^rufler , LiteParse, Yodoca ^yodoca --- По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитектуры заново. citeturn41search0turn27view0turn22view4turn21view0turn20view5turn20view6turn20view11turn20view10turn39view1turn39view0 Если ранжировать найденные направления по практической силе именно для старта, то порядок такой.

## `docs/01-svyazi/09-architectural-gaps.md`

_09-architectural-gaps_

> Svyazi ^svyazi хорошо закрывает ingest и нормализацию; AgentFS ^agentfs даёт .agentos и compile‑to‑runtime политику Проекты: Svyazi, CardIndex ^cardindex , AgentFS, knowledge-space ^knowledge space , mclaude, AI Factory, Rufler ^rufler , LiteParse --- После первичного обзора видно, что дефицит уже не в наличии компонентов, а в стыках между ними . Svyazi хорошо закрывает ingest и нормализацию; AgentFS даёт .agentos и compile‑to‑runtime политику; knowledge-space формирует agent‑readable reference cards; NGT ^ngt Memory и Yodoca ^yodoca решают разные режимы памяти; research-docs/LiteParse и Legal RAG ^rag решают доказуемость; LiteLLM, Auto AI Router и Tool Search — execution plane; SENTINEL ^sentinel и path‑guard практики — безопасность. В‑третьих, нужен memory governance layer , который не даёт ассоциативной памяти записывать предлагаемое как истинное.

## `docs/01-svyazi/10-second-order-ensembles.md`

_10-second-order-ensembles_

> citeturn41search0turn21view0turn20view5turn20view6 Второй ансамбль — Federated Local‑First Community Graph . citeturn27view0turn11search0turn11search11turn22view4turn20view12turn39view0turn20view10 Главное новое свойство здесь — не только privacy, но и архитектурная живучесть . citeturn33view2turn20view15turn12search2turn20view2turn20view3turn20view4turn20view19turn20view11 Здесь появляется новое свойство, которого нет у большинства “умных CRM” и “matching‑ботов”: изменение качества системы становится повторяемым артефактом .

## `docs/01-svyazi/11-integration-contracts.md`

_11-integration-contracts_

> Чтобы все эти ансамбли не рассыпались, полезно зафиксировать минимальный интерфейсный контракт между слоями. Это не заменяет будущую реализацию, но резко уменьшает риск того, что через две недели Проекты: Svyazi ^svyazi , CardIndex ^cardindex , AgentFS ^agentfs , mclaude, AI Factory, LiteParse, Legal RAG ^rag , Hybrid RAG --- Чтобы все эти ансамбли не рассыпались, полезно зафиксировать минимальный интерфейсный контракт между слоями. citeturn21view0turn22view4turn20view16turn39view3 Четвёртый контракт — Skill and Tool Policy .

## `docs/01-svyazi/12-roadmap.md`

_12-roadmap_

> Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти три короткие итерации , каждая из которых поднимает один новый класс свойств. Первая итерация должна закрепить Проекты: Svyazi ^svyazi , mclaude, AI Factory, Yodoca ^yodoca , NGT ^ngt Memory --- Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти три короткие итерации , каждая из которых поднимает один новый класс свойств. citeturn41search0turn20view5turn34view2turn20view6 Во второй итерации имеет смысл включить двухуровневую память и review queue .

## `docs/01-svyazi/13-contacts.md`

_13-contacts_

> citeturn22view4turn22view5turn32search2 Пятый разговор имеет смысл вести с авторами knowledge-space и mclaude, потому что именно здесь хорошо сходятся agent‑readable knowledge এবং multi‑session coordination. citeturn33view2turn20view2turn37search0turn20view3 Чтобы не перегружать первые обращения, ниже — более короткие шаблоны на один вопрос. citeturn22view4turn22view5 авторы knowledge-space / mclaude Держать операционные benchmark/gotcha cards в одной базе с reference cards или отдельным слоем?

## `docs/01-svyazi/14-limitations.md`

_14-limitations_

> Svyazi ^svyazi как базовый паттерн остаётся авторским закрытым п Проекты: Svyazi, mclaude, AI Factory, Rufler ^rufler , NGT ^ngt Memory, AutoResearch, Whisper, Yttri --- Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зрелости и лицензирования. Поэтому self-improvement контур разумно активировать только тогда, когда вы уже можете померить quality of match, quality of evidence и false positive rate по review‑очереди. Лучший следующий шаг — не искать ещё двадцать новых проектов , а собрать второй, более строгий слой поверх уже найденных: Card Envelope, Evidence Envelope, Memory Write Policy, Skill Policy и Review Record.

## `docs/01-svyazi/README.md`

_Svyazi[^svyazi] 2.0 — Архитектура и исследование_

> Файлов: 14 - 00-intro-part2.md 00-intro-part2.md — - 01-executive-summary.md 01-executive-summary.md — Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже слож… - 02-methodology.md 02-methodology.md — Поиск вёлся с приоритетом на Хабр как первичный слой описания идеи и на репозитории как первичный слой верификации… - 03-component-catalog.md 03-component-catalog.md — Проект или связка Автор Ссылка на статью и репо Краткое описание Ключевые компоненты и паттерны Лицензия M… - 04-ensembles-overview.md 04-ensembles-overview.md — Ниже — не все теоретически возможные комбинации, а пять ансамблей с максимальным приростом свойств при минимальном инт… - 06-security-privacy.md 06-security-privacy.md — Для Svyazi‑2.0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP ^mcp servers, и… - 07-mvp-planning.md 07-mvp-planning.md — Наиболее рациональный прототип — не собирать всё сразу , а доказать одну центральную способность: система находит и … - 08-conclusions.md 08-conclusions.md — По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей , не придумывая пол… - 09-architectural-gaps.md 09-architectural-gaps.md — После первичного обзора видно, что дефицит уже не в наличии компонентов, а в стыках между ними . Svyazi хорошо закрыв… - 10-second-order-ensembles.md 10-second-order-ensembles.md — Самые интересные продолжения — не просто добавление ещё одного инструмента в уже найденные пять ансамблей, а сборка тр… - 11-integration-contracts.md 11-integration-contracts.md — Чтобы все эти ансамбли не рассыпались, полезно зафиксировать минимальный интерфейсный контракт между слоями. Это не … - 12-roadmap.md 12-roadmap.md — Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти три короткие итерации , каждая… - 13-contacts.md 13-contacts.md — С практической точки зрения следующие письма или комментарии лучше строить не вокруг общей фразы “давайте сделаем Svyazi… - 14-limitations.md 14-limitations.md — Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зре… - ensembles/ ensembles/ — Ансамбли проектов --- Похожие документы: - README docs/04-ai-collaborations/README.md сходство 0.67 - PRIORITIES docs/PRIORITIES.md сходство 0.11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов

## `docs/02-anthropic-vacancies/00-intro.md`

_Введение_

> Параллельно в AI Research & Engineering есть Research Engineer / Research Scientist, Societal Impacts SF, 2 роли . Если и есть ваш «главный проект», который стоит довести до shipping — это он. daten ⭐1 Python, Jan 12 — pinned, основной «иос», уже разбирали.

## `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md`

_Интегральный анализ профиля svend4_

> Если ваш nautilus использует MCP как protocol — это современный и правильный выбор. Пришлёте мне README info1, pro2, meta если есть , и один пример nautilus.json + один адаптер из adapters/ . Если его нет — значит GitHub уже отозвал автоматически.

## `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md`

_ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL_

> --- - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL #общий-план-развития-nautilus-portal-protocol - Часть 1. Чтобы подключить репо к Nautilus — нужен только nautilus.json 10–20 строк JSON и passport.md 1 страница markdown . Nautilus не читает приватные репо через MCP по умолчанию.

## `docs/02-anthropic-vacancies/06-1-introduction.md`

_1. Introduction_

> Современные системы управления знаниями Notion, Obsidian, Roam, Logseq, --- Современные системы управления знаниями Notion, Obsidian, Roam, Logseq, Coda, Confluence требуют от пользователя миграции в их единый формат. Homogenization : разные типы знаний методология, семантика, символизм принудительно приводятся к одной структуре, что уменьшает выразительность. NPP не пытается: - Заменить существующие системы знаний Notion, Obsidian — они дополняются, не заменяются - Обеспечить real-time sync между репо федерация асинхронна по дизайну - Формализовать онтологии bridges между репо — свободные текстовые описания, не OWL/RDF - Обеспечить write-operations в федерируемые репо read-only в v1.0 Ключевые термины определены в разделе 2.

## `docs/02-anthropic-vacancies/07-2-terminology.md`

_2. Terminology_

> Repository-participant далее — Repo — Git-репозиторий, содержащий минимум nautilus.json и passport.md в корне. Native format — исходный формат данных в Repo, определяемый автором. Registry — файл nautilus.json в корне Portal-репо, перечисляющий все Repos экосистемы с их метаданными.

## `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md`

_3. Registry (`nautilus.json`)_

> Registry — central source of truth о том, какие Repos входят в --- Registry — central source of truth о том, какие Repos входят в экосистему и как их интерпретировать. Registry MUST быть валидным JSON со следующей структурой: - protocol version — строка в формате semver. - ecosystem name — короткое уникальное имя latin, без пробелов .

## `docs/02-anthropic-vacancies/104-appendix-c-references.md`

_Appendix C: References_

> Создать docs/PORTAL-PROTOCOL.md в репо с этим содержимым или PORTAL-PROTOCOL.md в корне, если хотите более заметно 2. Добавить ссылку из README.md: в footer заменить Nautilus Portal Protocol v1.1 на Nautilus Portal Protocol v1.1 ./docs/PORTAL-PROTOCOL.md с рабочим линком 3. Коммит с сообщением docs: add formal PORTAL-PROTOCOL.md v1.1 specification 4.

## `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md`

_1. Контекст и мотивация_

> Проект Nautilus разрабатывается в паре «автор + Claude Code агент». --- Проект Nautilus разрабатывается в паре «автор + Claude Code агент». Параллельное сохранение Фазы A и B — оба варианта коммитятся в main друг под другом, с дубликатами 2.

## `docs/02-anthropic-vacancies/108-2-формальный-workflow.md`

_2. Формальный workflow_

> Фаза A Фаза B Фаза C --- Методология применяется только к критически важным документам , где стоимость потери информации высока. Примеры из Nautilus: - STATUS.md — отчёт о состоянии проекта - IMPLEMENTATION STAGE PART .md — технико-концептуальный review - PORTAL-PROTOCOL.md — formal specification Для routine документов README, adapter docs, passport templates достаточно single-pass review. Критерий применения : если потеря одной вашей фразы в документе может повлиять на архитектурное решение, grant application или academic reviewer — применяйте трёхфазный метод.

## `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md`

_3. Принципы консолидации (Фаза C)_

> Если A и B сообщают одинаковое число например, «60 тестов» в обеих — взять это значение, удалить дубликат. Если A и B сообщают разные числа например, «6782 LOC» в A, «6600 LOC» в B — провести реальную проверку и зафиксировать проверенное значение. Если один вариант содержит раздел, которого нет в другом — автоматически включить в v3 .

## `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md`

_Вопрос: fallback-ratio как критический или осмысленный?_

> Python LOC — базовая метрика масштаба проекта 2. Q6 coverage — ключевая метрика конкретного проекта 4. Commit count — временная метрика Всё остальное даты, версии, названия веток — проверяется при встрече, но не в приоритете.

## `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md`

_5. Связь с существующими методологиями_

> Теоретическим прародителем является N-version programming --- Теоретическим прародителем является N-version programming Chen & Avizienis, 1977–78 — написание нескольких независимых имплементаций одной спецификации для повышения reliability. Отличия: - N-version programming: про код, цель — fault-tolerance - Трёхфазная методология: про документацию, цель — completeness of insights В академической рецензии две независимые peer reviews могут противоречить друг другу . Отличия: - ML ensembles: разрешение автоматическое, по правилу - Наша методология: разрешение ручное, через правила 1-5 В security и public policy используется структура red vs blue : один агент критикует, другой защищает.

## `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md`

_7. Реализация в проекте Nautilus_

> Первое применение — IMPLEMENTATION STAGE PART 1-4 .md --- Первое применение — IMPLEMENTATION STAGE PART 1-4 .md апрель 2026 : - Вариант A: ветка claude/review-nautilus-changes-tdywx - Вариант B: ветка claude/project-implementation-stage-CzylE - Текущий статус: Merged-to-main with parallel blocks, Фаза C не пройдена Повторное применение — STATUS.md апрель 2026 : - Пройдена Фаза A единожды single-pass - Статус: канонично, трёхфазная методология не применялась - Осмысленность: документ достаточно простой для single-pass Пример, что методология применяется селективно , только там, где польза оправдывает overhead. Исходные draft ветки claude/ — как audit trail 2. Финальная консолидированная — после Фазы C Удалять исходные ветки не следует до завершения Фазы C — они могут содержать контекст, нужный для разрешения неочевидных расхождений.

## `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md`

_8. Ограничения и открытые вопросы_

> Q4 : Как долго может оставаться документ в transitional state? Если Фаза C откладывается дольше, transitional state становится постоянным, что подрывает доверие. Option Freeze : явно пометить документ как «frozen at transitional state», не удалять header warning, принять репутационный debt 3.

## `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md`

_9. Checklist применения методологии_

> - Есть время на Фазу C в течение 2 недель? - Две ветки будут работать на полностью независимых prompts не «продолжи вариант A» ? - Агенты работают в разных ветках не в одной - Prompt'ы для A и B идентичны иначе это не независимое воспроизведение - Каждый агент не видит результат другого - Header warning добавлен см.

## `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md`

_10. Конкретный план применения к текущим документам_

> Текущий статус : Merged-to-main, Фаза C не пройдена, header --- Текущий статус : Merged-to-main, Фаза C не пройдена, header warning отсутствует . Добавить header warning §2.4 в каждую из 4 частей 2. Установить deadline Фазы C: 2026-05-03 2 недели 3.

## `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md`

_Appendix B: Примеры расхождений и их разрешения_

> Из IMPLEMENTATION STAGE PART 1.md реальный пример : --- Из IMPLEMENTATION STAGE PART 1.md реальный пример : Разрешение через Правило 2 §3.1 : Финальная запись : Правило: итоговое число — точное, верифицированное , не среднее между A и B. Из IMPLEMENTATION STAGE PART 1.md : Это существенное расхождение почти в 2 раза . Гипотетический пример : Разрешение : оба риска реальны, приоритезация зависит от цели проекта.

## `docs/02-anthropic-vacancies/122-глоссарий.md`

_Глоссарий_

> Commit: docs: add REVIEW METHODOLOGY for three-phase review process . REVIEW METHODOLOGY.md v1.0 — meta-документ о вашем workflow с AI-agents Плюс то, что уже в репо: 1. Пишу portal-mcp.py — MCP wrapper над Nautilus Portal.

## `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md`

_Конфигурация для Claude Desktop_

> После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигурации MCP. Путь зависит от ОС: --- После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигурации MCP. После сохранения конфигурации и перезапуска Claude Desktop в чате появится индикатор подключения MCP-сервера, и tools станут доступны для использования.

## `docs/02-anthropic-vacancies/130-отладка.md`

_Отладка_

> Проверить логи Claude Desktop: - macOS: ~/Library/Logs/Claude/mcp .log - Windows: %APPDATA%\Claude\logs\mcp .log - Linux: ~/.config/Claude/logs/mcp .log 2. Проверить: Если portal тоже падает — проблема не в MCP, а в самом адаптере. Проверить синтаксис claude desktop config.json валидный JSON 2.

## `docs/02-anthropic-vacancies/133-обратная-связь.md`

_Обратная связь_

> Key property: meta-agent не видит, какие assistant'ы использует Node . - Node level : Node disagrees с meta-agent's task assignment. - Meta level : два Node disagree on architecture.

## `docs/02-anthropic-vacancies/136-abstract.md`

_Abstract_

> We introduce the Double-Triangle Architecture for human-AI --- We introduce the Double-Triangle Architecture for human-AI collaboration in distributed knowledge work. These two triangles superimpose to form a six-pointed star topology, which we argue is the correct architectural primitive for the next generation of AI-managed knowledge work. Formal specification of the Double-Triangle Architecture, including three inter-layer protocols and six architectural invariants 2.

## `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md`

_1. Why Single-Triangle Models Are Incomplete_

> In reality, every knowledge worker simultaneously occupies both positions : - A software engineer uses Copilot to write code lower triangle: human conducts assistant - At the same time, their team lead coordinates the engineer alongside five others toward a sprint goal upper triangle: meta-agent coordinates human The engineer's decisions about what Copilot generates depend on the sprint context coming from upper triangle . This creates what we call the coordination gap : personal AI assistants don't know about team context, and team-level coordination tools don't know about assistant-generated artifacts. Information has to be manually translated by humans across this gap, constantly.

## `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md`

_2. The Double-Triangle Architecture_

> Six Architectural Invariants #23-six-architectural-invariants - Bridges #bridges --- We formalize the architecture using two triangles sharing a common vertex: Lower triangle per human Node N : where A 1, A 2, A 3 are AI assistants personalized to N's work. Each human N is simultaneously the vertex of a lower triangle their own and a base node of an upper triangle their team's . Lower triangle assistants have broad autonomy to execute tasks within their scope, but the human Node retains final authority on what propagates upward to team context.

## `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md`

_3. Three Inter-Layer Protocols_

> Protocol 2 — Meta-Agent Coordinates Nodes #32-protocol-2-meta-agent-coordinates-nodes - 3.3. Protocol 3 — Assistant-to-Meta Negotiation #33-protocol-3-assistant-to-meta-negotiation - 3.4. Direction: Assistant A of Node N → Meta-agent M upward across triangles Semantics.

## `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md`

_4. Nautilus Portal as Reference Substrate_

> Required Extensions to NPP for Double-Triangle #42-required-extensions-to-npp-for-double-triangle - 4.3. We propose NPP as the reference substrate for Double-Triangle implementations. A Double-Triangle implementation is an NPP v1.1 implementation plus these extensions.

## `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md`

_5. Pattern Library as Bridge Between Triangles_

> Private instance points to public pattern it uses as a template. Private instance generates anonymized pattern to contribute back to public library. Direction: instance → pattern through anonymization pipeline .

## `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md`

_6. Four Deployment Domains_

> The Double-Triangle Architecture is domain-agnostic but benefits --- - 6. Generic Knowledge Work Domain #64-generic-knowledge-work-domain --- The Double-Triangle Architecture is domain-agnostic but benefits from concrete deployment analysis. This domain is perhaps the broadest application of Double-Triangle architecture.

## `docs/02-anthropic-vacancies/144-7-open-questions.md`

_7. Open Questions_

> The Double-Triangle Architecture is proposed as a framework, not --- - 7. Adversarial Dynamics #76-adversarial-dynamics --- The Double-Triangle Architecture is proposed as a framework, not a complete solution. Does the architecture scale to very large organizations?

## `docs/02-anthropic-vacancies/145-8-call-to-action.md`

_8. Call to Action_

> The Double-Triangle Architecture is a framework awaiting --- - 8. For the First Author #85-for-the-first-author --- The Double-Triangle Architecture is a framework awaiting implementation and validation. Deploy Double-Triangle architecture in specific domains — legal practice, medical coordination, engineering teams, research groups.

## `docs/02-anthropic-vacancies/146-acknowledgments.md`

_Acknowledgments_

> This work emerged through extensive collaboration with Anthropic's --- This work emerged through extensive collaboration with Anthropic's Claude primarily Claude Opus 4.7 across multiple sessions in 2026. This dependency on AI assistance is not a footnote but a core observation: the Double-Triangle Architecture is the emerging pattern of its own construction. This paper was written by one human working with multiple AI assistants, which is exactly the lower triangle it describes.

## `docs/02-anthropic-vacancies/147-references.md`

_References_

> Artificial Intelligence: A Modern Approach , 4th ed. "Architectural Styles and the Design of Network-based Software Architectures". Design Patterns: Elements of Reusable Object-Oriented Software .

## `docs/02-anthropic-vacancies/148-appendix-a-glossary.md`

_Appendix A: Glossary_

> - Upper triangle : Meta-agent + multiple human participants. - Protocol 1 : Downward communication within lower triangle Node to Assistants . - Protocol 2 : Downward communication within upper triangle Meta-agent to Nodes .

## `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md`

_Appendix B: Summary of Contributions_

> Topological formalization of Double-Triangle Architecture with Star of David metaphor 2. Three inter-layer protocols specification only Protocols 1 and 2 are currently partially implemented; Protocol 3 is novel 4. Nautilus Portal Protocol v1.1 reference substrate with documented gaps requiring three specific extensions 6.

## `docs/02-anthropic-vacancies/150-appendix-c-version-history.md`

_Appendix C: Version History_

> Infrastructure layer — open-source platform built on Nautilus Portal Protocol. Написать 10-page concept document «Open Knowledge Work Foundation: AI-Coordinated Infrastructure for Distributed Expert Contribution». Интегрирует всё: Nautilus Portal Protocol, Double-Triangle Architecture, Foundation Model, humanities extension, MMORPG-like engagement, pattern library.

## `docs/02-anthropic-vacancies/153-executive-summary.md`

_Executive Summary_

> Existing staffing platforms Deel, Toptal, Upwork, Mercor treat these populations as transactional labor, not as dignified contributors with persistent professional identity. Nautilus Portal Protocol — open technical substrate for federated knowledge work 2. Double-Triangle Architecture — human-AI collaboration pattern preserving individual autonomy 3.

