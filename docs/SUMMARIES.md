# Резюме документов (TextRank)

<!-- toc -->
## Содержание

- [`docs/01-svyazi/00-intro-part2.md`](#docs01-svyazi00-intro-part2md)
- [`docs/01-svyazi/01-executive-summary.md`](#docs01-svyazi01-executive-summarymd)
- [`docs/01-svyazi/02-methodology.md`](#docs01-svyazi02-methodologymd)
- [`docs/01-svyazi/03-component-catalog.md`](#docs01-svyazi03-component-catalogmd)
- [`docs/01-svyazi/04-ensembles-overview.md`](#docs01-svyazi04-ensembles-overviewmd)
- [`docs/01-svyazi/06-security-privacy.md`](#docs01-svyazi06-security-privacymd)
- [`docs/01-svyazi/07-mvp-planning.md`](#docs01-svyazi07-mvp-planningmd)
- [`docs/01-svyazi/08-conclusions.md`](#docs01-svyazi08-conclusionsmd)
- [`docs/01-svyazi/09-architectural-gaps.md`](#docs01-svyazi09-architectural-gapsmd)
- [`docs/01-svyazi/10-second-order-ensembles.md`](#docs01-svyazi10-second-order-ensemblesmd)
- [`docs/01-svyazi/11-integration-contracts.md`](#docs01-svyazi11-integration-contractsmd)
- [`docs/01-svyazi/12-roadmap.md`](#docs01-svyazi12-roadmapmd)
- [`docs/01-svyazi/13-contacts.md`](#docs01-svyazi13-contactsmd)
- [`docs/01-svyazi/14-limitations.md`](#docs01-svyazi14-limitationsmd)
- [`docs/01-svyazi/QA.md`](#docs01-svyaziqamd)
- [`docs/01-svyazi/README.md`](#docs01-svyazireadmemd)
- [`docs/02-anthropic-vacancies/00-intro.md`](#docs02-anthropic-vacancies00-intromd)
- [`docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md`](#docs02-anthropic-vacancies01-интегральный-анализ-профиля-svend4md)
- [`docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md`](#docs02-anthropic-vacancies02-общий-план-развития-nautilus-portal-protocolmd)
- [`docs/02-anthropic-vacancies/03-portal-protocol-md.md`](#docs02-anthropic-vacancies03-portal-protocol-mdmd)
- [`docs/02-anthropic-vacancies/04-abstract.md`](#docs02-anthropic-vacancies04-abstractmd)
- [`docs/02-anthropic-vacancies/05-0-status-of-this-document.md`](#docs02-anthropic-vacancies05-0-status-of-this-documentmd)
- [`docs/02-anthropic-vacancies/06-1-introduction.md`](#docs02-anthropic-vacancies06-1-introductionmd)
- [`docs/02-anthropic-vacancies/07-2-terminology.md`](#docs02-anthropic-vacancies07-2-terminologymd)
- [`docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md`](#docs02-anthropic-vacancies08-3-registry-nautilus-jsonmd)
- [`docs/02-anthropic-vacancies/09-4-passport-passport-md.md`](#docs02-anthropic-vacancies09-4-passport-passport-mdmd)
- [`docs/02-anthropic-vacancies/102-доступ-к-данным.md`](#docs02-anthropic-vacancies102-доступ-к-даннымmd)
- [`docs/02-anthropic-vacancies/103-appendix-b-change-log.md`](#docs02-anthropic-vacancies103-appendix-b-change-logmd)
- [`docs/02-anthropic-vacancies/104-appendix-c-references.md`](#docs02-anthropic-vacancies104-appendix-c-referencesmd)
- [`docs/02-anthropic-vacancies/105-review-methodology-md.md`](#docs02-anthropic-vacancies105-review-methodology-mdmd)
- [`docs/02-anthropic-vacancies/106-tl-dr.md`](#docs02-anthropic-vacancies106-tl-drmd)
- [`docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md`](#docs02-anthropic-vacancies107-1-контекст-и-мотивацияmd)
- [`docs/02-anthropic-vacancies/108-2-формальный-workflow.md`](#docs02-anthropic-vacancies108-2-формальный-workflowmd)
- [`docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md`](#docs02-anthropic-vacancies109-3-принципы-консолидации-фаза-cmd)
- [`docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md`](#docs02-anthropic-vacancies110-вопрос-fallback-ratio-как-критический-или-осмысленmd)
- [`docs/02-anthropic-vacancies/111-4-условия-применимости.md`](#docs02-anthropic-vacancies111-4-условия-применимостиmd)
- [`docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md`](#docs02-anthropic-vacancies112-5-связь-с-существующими-методологиямиmd)
- [`docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md`](#docs02-anthropic-vacancies113-6-почему-это-валидный-паттерн-для-ai-assisted-workmd)
- [`docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md`](#docs02-anthropic-vacancies114-7-реализация-в-проекте-nautilusmd)
- [`docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md`](#docs02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd)
- [`docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md`](#docs02-anthropic-vacancies116-9-checklist-применения-методологииmd)
- [`docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md`](#docs02-anthropic-vacancies117-10-конкретный-план-применения-к-текущим-документамmd)
- [`docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md`](#docs02-anthropic-vacancies118-appendix-a-шаблон-для-header-warningmd)
- [`docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md`](#docs02-anthropic-vacancies119-appendix-b-примеры-расхождений-и-их-разрешенияmd)
- [`docs/02-anthropic-vacancies/12-content-overview.md`](#docs02-anthropic-vacancies12-content-overviewmd)
- [`docs/02-anthropic-vacancies/120-главные-технические-риски.md`](#docs02-anthropic-vacancies120-главные-технические-рискиmd)
- [`docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md`](#docs02-anthropic-vacancies121-appendix-c-история-изменений-методологииmd)
- [`docs/02-anthropic-vacancies/122-глоссарий.md`](#docs02-anthropic-vacancies122-глоссарийmd)
- [`docs/02-anthropic-vacancies/123-portal-mcp-py.md`](#docs02-anthropic-vacancies123-portal-mcp-pymd)
- [`docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md`](#docs02-anthropic-vacancies124-конфигурация-для-claude-desktopmd)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

---


<!-- toc-auto -->

> [!NOTE]
> Раздел `SUMMARIES` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: summaries, docs -->


<!-- summary -->
> `SUMMARIES` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-11_

Файлов: **1097** | Предложений: **3** на документ

## `docs/01-svyazi/00-intro-part2.md`

_Продолжение исследования для Svyazi[^svyazi] 2.0_

> - README README.md — раздел 01-svyazi - 01-executive-summary 01-executive-summary.md — резюме проекта - PROTOTYPE SPEC ../PROTOTYPE SPEC.md — спецификация прототипа Документ индексирован в базе знаний репозитория. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов.

## `docs/01-svyazi/01-executive-summary.md`

_Svyazi[^svyazi] 2.0 — Исполнительное резюме_

> - Главная линия синергии #главная-линия-синергии - Ключевой вывод #ключевой-вывод - Что добавляет продолжение исследования #что-добавляет-продолжение-исследования - Приоритет ансамблей для старта #приоритет-ансамблей-для-старта --- Абстракт авто 🎯 Проблема: Svyazi^svyazi 2.0 — Исполнительное резюме Contents - Главная линия синергии главная-линия-синергии - Ключевой вывод ключевой-вывод - Что добавляет продолжение исследования что-до ✅ Результат: Первое — Svyazi + AgentFS + NGT/Yodoca + LiteParse: даёт уже полезный MVP 2. 🏷️ Ключевые слова: svyazi , проект , cardindex , agentfs , добавляет , продолжение , rufler , memory !IMPORTANT Главный документ проекта. Первое — Svyazi + AgentFS + NGT/Yodoca + LiteParse: даёт уже полезный MVP 2.

## `docs/01-svyazi/02-methodology.md`

_Методика и рамка отбора проектов_

> 🏷️ Ключевые слова: отбора , методика , рамка , зрелости , collaborations , шкала , первичный , svyazi !TIP Этот документ описывает MVP-подход. Поиск вёлся с приоритетом на Хабр как первичный слой описания идеи и на репозитории как первичный слой верификации лицензии, зрелости и интеграционного интерфейса . Проекты: Svyazi ^svyazi , LiteParse 01-executive-summary.md , Legal RAG ^rag , Graph RAG --- Поиск вёлся с приоритетом на Хабр как первичный слой описания идеи и на репозитории как первичный слой верификации лицензии, зрелости и интеграционного интерфейса .

## `docs/01-svyazi/03-component-catalog.md`

_Каталог компонентов Svyazi 2.0_

> citeturn33view1turn37search1 Высокая : это внешний knowledge layer для агентов и нормализатора. citeturn22view3turn32search2 Очень высокая : быстрый ассоциативный memory‑слой для discovery и matching. citeturn15search3turn39view3 Высокая : слой typed memory и governance для более поздних итераций.

## `docs/01-svyazi/04-ensembles-overview.md`

_Приоритетные ансамбли проектов_

> citeturn21view10turn35search0 - Локальная обработка вместо облачной утечки контекста : и локальный speech‑to‑text, и local‑first workspace, и CRDT ^crdt ‑sync работают в модели “данные принадлежат устройству пользователя”. citeturn35search0 - Контекст реального мира доступен агенту как tool, а не как догадка : Self‑Aware MCP закрывает проблемы часового пояса, ОС, даты и локации. citeturn11search2turn39view0turn39view1turn20view18turn20view10 Ожидаемые новые свойства: - Реальная экономия контекста ещё до первого токена работы : в кейсе Tool Search MCP‑overhead упал с 82k до 5.7k токенов, а свободное окно выросло на 76k.

## `docs/01-svyazi/06-security-privacy.md`

_Безопасность и приватность_

> 🏷️ Ключевые слова: search , memory , только , svyazi , безопасность , бюджетный , роутинг , нужен !WARNING Документ описывает ограничения, риски или требования безопасности. Для Svyazi ^svyazi ‑2.0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP ^mcp servers, импорты документов и memory writes потенциально недоверенными . Это не паранойя, Проекты: Svyazi, AgentFS ^agentfs , AI Factory, agent-memory-mcp, SENTINEL ^sentinel , LiteLLM, Auto AI Router, Tool Search --- Для Svyazi‑2.0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP servers, импорты документов и memory writes потенциально недоверенными .

## `docs/01-svyazi/07-mvp-planning.md`

_Планирование MVP_

> Абстракт авто 🎯 Проблема: citeturn33view3turn20view2turn37search0 Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn33view3turn20view2turn37search0 Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn21view0turn21view1turn18search1 Комментарии к статье Yodoca и GitHub issues/discussions в repo.

## `docs/01-svyazi/08-conclusions.md`

_Выводы_

> 🔧 Подход: По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей, не придумывая половину архитектуры заново. По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитектуры заново. Самый дефицитный слой — не память, не RAG ^rag и не оркестр Проекты: Svyazi ^svyazi , CardIndex ^cardindex , AgentFS ^agentfs , mclaude, AI Factory, Rufler ^rufler , LiteParse 01-executive-summary.md , Yodoca ^yodoca --- По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитектуры заново.

## `docs/01-svyazi/09-architectural-gaps.md`

_Архитектурные зазоры_

> ✅ Результат: Наоборот, даже средний model tier даёт много пользы, если extract/normalize/review/evidence и memory status already pinned. Svyazi ^svyazi хорошо закрывает ingest и нормализацию; AgentFS ^agentfs даёт .agentos и compile‑to‑runtime политику Проекты: Svyazi, CardIndex ^cardindex , AgentFS, knowledge-space 03-component-catalog.md ^knowledge-space , mclaude, AI Factory, Rufler ^rufler , LiteParse --- После первичного обзора видно, что дефицит уже не в наличии компонентов, а в стыках между ними . Наоборот, даже средний model tier даёт много пользы, если extract/normalize/review/evidence и memory status already pinned.

## `docs/01-svyazi/10-second-order-ensembles.md`

_Ансамбли следующего шага_

> 🔧 Подход: citeturn27view0turn11search0turn11search11turn22view4turn20view12turn39view0turn20view10 Главное новое свойство здесь — не только privacy, но и архитектурная живучесть. citeturn41search0turn21view0turn20view5turn20view6 Второй ансамбль — Federated Local‑First Community Graph . citeturn27view0turn11search0turn11search11turn22view4turn20view12turn39view0turn20view10 Главное новое свойство здесь — не только privacy, но и архитектурная живучесть .

## `docs/01-svyazi/11-integration-contracts.md`

_Интеграционные контракты_

> 🔧 Подход: Любой retrieval‑ответ, match suggestion, profile enrichment или auto‑summary должен возвращать не только текст, но и sourceid, page, span, box, retrievalmethod, confidence, support ✅ Результат: Это не “идеальная онтология”, а минимальный договор, который позволяет системам вообще разговаривать между собой. 🏷️ Ключевые слова: контракт , memory , svyazi , который , через , search , проект , agentfs !IMPORTANT Нормативный документ. Это не заменяет будущую реализацию, но резко уменьшает риск того, что через две недели Проекты: Svyazi ^svyazi , CardIndex ^cardindex , AgentFS ^agentfs , mclaude, AI Factory, LiteParse 01-executive-summary.md , Legal RAG ^rag , Hybrid RAG --- Чтобы все эти ансамбли не рассыпались, полезно зафиксировать минимальный интерфейсный контракт между слоями.

## `docs/01-svyazi/12-roadmap.md`

_Дорожная карта прототипа_

> 🏷️ Ключевые слова: итерации , svyazi , memory , дорожная , карта , first , evidence , local !TIP Обзорный документ. Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти три короткие итерации , каждая из которых поднимает один новый класс свойств. Первая итерация должна закрепить Проекты: Svyazi ^svyazi , mclaude, AI Factory, Yodoca ^yodoca , NGT ^ngt Memory --- Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти три короткие итерации , каждая из которых поднимает один новый класс свойств.

## `docs/01-svyazi/13-contacts.md`

_Контактная стратегия_

> 🏷️ Ключевые слова: вопрос , knowledge , space , лучше , cardindex , agentfs , search , между !TIP Обзорный документ. citeturn33view2turn20view2turn37search0turn20view3 Чтобы не перегружать первые обращения, ниже — более короткие шаблоны на один вопрос. citeturn22view4turn22view5 авторы knowledge-space / mclaude Держать операционные benchmark/gotcha cards в одной базе с reference cards или отдельным слоем?

## `docs/01-svyazi/14-limitations.md`

_Ограничения и лицензии_

> Абстракт авто 🎯 Проблема: Такой порядок согласуется и с Yttri‑подходом к workspace вокруг записей, и с простыми локальными whisper‑сценариями, и с идеей local-first sync как следующего, а не первого слоя сл 🔧 Подход: Такой порядок согласуется и с Yttri‑подходом к workspace вокруг записей, и с простыми локальными whisper‑сценариями, и с идеей local-first sync как следующего, а не первого слоя сл ✅ Результат: citeturn41search0turn27view0turn20view5turn21view0turn39view1turn20view10 --- Похожие документы: - 14-ограничения-лицензии-и-что-пока-лучше-не-склеивать docs/04-ai-collabor 🏷️ Ключевые слова: svyazi , memory , лучше , search , rufler , roadmap , ограничения , лицензии !WARNING Документ описывает ограничения, риски или требования безопасности. Svyazi ^svyazi как базовый паттерн остаётся авторским закрытым п Проекты: Svyazi, mclaude, AI Factory, Rufler ^rufler , NGT ^ngt Memory, AutoResearch 01-executive-summary.md , Whisper, Yttri --- Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зрелости и лицензирования. Лучший следующий шаг — не искать ещё двадцать новых проектов , а собрать второй, более строгий слой поверх уже найденных: Card Envelope, Evidence Envelope, Memory Write Policy, Skill Policy и Review Record.

## `docs/01-svyazi/QA.md`

_Q&A: 01-svyazi_

> !NOTE Раздел QA формируется автоматически из данных репозитория. Проекты: Svyazi ^svyazi , LiteParse, Legal RAG ^rag , Hybrid RAG, Graph RAG, SENTINEL ^sentinel , LiteLLM, Auto AI Router --- Автоматически сгенерировано по 14 файлам раздела. Упоминаются: зазор , карточка , evidence , memory governance , agent contract Упоминаются: card envelope , Evidence Envelope , memory write , skill policy , review record Упоминаются: liteparse , bounding box , page-level , evidence Упоминаются: Evidence Envelope , source id , page , span Упоминаются: Legal RAG , Hybrid RAG , Graph RAG , LiteParse Упоминаются: SENTINEL , LiteLLM , Tool Search , Auto AI Router Упоминаются: read-only , allowlist , path guard , quarantine Упоминаются: routing , budget , litellm Упоминаются: mvp , 12-18 , итерац , фаза , неделя Упоминаются: evidence-first , unified card , page/span , manual review Упоминаются: Андрей Чуян , Виталий Оборин , kksudo , spbmolot Упоминаются: первый вопрос , архитектурный , шаблон , контакт --- Кто ссылается на этот документ 6 : - README README.md - OUTLINE ../OUTLINE.md - READABILITY ../READABILITY.md - READING TIME ../READING TIME.md - SEARCH ../SEARCH.md - TABLES ../TABLES.md --- Похожие документы: - QA ../obsidian/01-svyazi/QA.md сходство 0.99 - QA ../04-ai-collaborations/QA.md сходство 0.85 - QA ../obsidian/04-ai-collaborations/QA.md сходство 0.84 --- ^rag : Retrieval-Augmented Generation — генерация с поиском ^sentinel : OSS-проект: безопасность и allowlist для MCP ^svyazi : Главный проект: экосистема AI-компонентов

## `docs/01-svyazi/README.md`

_Svyazi[^svyazi] 2.0 — Архитектура и исследование_

> Файлов: 15 - 00-intro-part2.md 00-intro-part2.md — - 01-executive-summary.md 01-executive-summary.md — Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже слож… - 02-methodology.md 02-methodology.md — Поиск вёлся с приоритетом на Хабр как первичный слой описания идеи и на репозитории как первичный слой верификации… - 03-component-catalog.md 03-component-catalog.md — Проект или связка Автор Ссылка на статью и репо Краткое описание Ключевые компоненты и паттерны Лицензия M… - 04-ensembles-overview.md 04-ensembles-overview.md — Ниже — не все теоретически возможные комбинации, а пять ансамблей с максимальным приростом свойств при минимальном инт… - 06-security-privacy.md 06-security-privacy.md — Для Svyazi‑2.0 безопасная архитектура — не "добавить сканер в конце", а с самого начала считать skills, MCP ^mcp servers, и… - 07-mvp-planning.md 07-mvp-planning.md — Наиболее рациональный прототип — не собирать всё сразу , а доказать одну центральную способность: система находит и … - 08-conclusions.md 08-conclusions.md — По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей , не придумывая пол… - 09-architectural-gaps.md 09-architectural-gaps.md — После первичного обзора видно, что дефицит уже не в наличии компонентов, а в стыках между ними . Svyazi хорошо закрыв… - 10-second-order-ensembles.md 10-second-order-ensembles.md — Самые интересные продолжения — не просто добавление ещё одного инструмента в уже найденные пять ансамблей, а сборка тр… - 11-integration-contracts.md 11-integration-contracts.md — Чтобы все эти ансамбли не рассыпались, полезно зафиксировать минимальный интерфейсный контракт между слоями. Это не … - 12-roadmap.md 12-roadmap.md — Если идти дальше после базового MVP, то лучшая стратегия — не "добавить всё", а пройти три короткие итерации , каждая… - 13-contacts.md 13-contacts.md — С практической точки зрения следующие письма или комментарии лучше строить не вокруг общей фразы "давайте сделаем Svyazi… - 14-limitations.md 14-limitations.md — Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зре… - QA.md QA.md — Вопросы и ответы по разделу: архитектура, компоненты, MVP, ансамбли - ensembles/ ensembles/ — Ансамбли проектов --- - README ../04-ai-collaborations/README.md сходство 0.67 - PRIORITIES ../PRIORITIES.md сходство 0.11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов --- Кто ссылается на этот документ 13 : - 00-intro-part2 00-intro-part2.md - 03-component-catalog 03-component-catalog.md - 07-mvp-planning 07-mvp-planning.md - 09-architectural-gaps 09-architectural-gaps.md - 10-second-order-ensembles 10-second-order-ensembles.md - 11-integration-contracts 11-integration-contracts.md - README ../04-ai-collaborations/README.md - INDEX ../INDEX.md - ...ещё 5

## `docs/02-anthropic-vacancies/00-intro.md`

_Введение_

> Параллельно в AI Research & Engineering есть Research Engineer / Research Scientist, Societal Impacts SF, 2 роли . Если и есть ваш «главный проект», который стоит довести до shipping — это он. daten ⭐1 Python, Jan 12 — pinned, основной «иос», уже разбирали.

## `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md`

_Интегральный анализ профиля svend4_

> Если ваш nautilus ../05-habr-projects/memory/memnet.md использует MCP как protocol — это современный и правильный выбор. Если в nautilus ../05-habr-projects/memory/memnet.md уже есть эти 4 компонента, это готовая инфраструктура для того, чтобы упаковать ваши 70 репо в coherent navigable portal. Пришлёте мне README info1, pro2, meta если есть , и один пример nautilus ../05-habr-projects/memory/memnet.md .json + один адаптер из adapters/ .

## `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md`

_ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL_

> --- - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL #общий-план-развития-nautilus-portal-protocol - Часть 1. Чтобы подключить репо к Nautilus — нужен только nautilus ../05-habr-projects/memory/memnet.md .json 10–20 строк JSON и passport.md 1 страница markdown . nautilus ../05-habr-projects/memory/memnet.md .json включает поле protocol version .

## `docs/02-anthropic-vacancies/03-portal-protocol-md.md`

_PORTAL-PROTOCOL.md_

> markdown bash python scripts/improve semantic search.py --query "PORTAL PROTOCOL md" - 152-ai-coordinated-infrastructure-for-distributed-expe 152-ai-coordinated-infrastructure-for-distributed-expe.md - 73-portal-protocol-md-v1-1 73-portal-protocol-md-v1-1.md - 135-a-formal-model-for-human-ai-collaboration-in-distr 135-a-formal-model-for-human-ai-collaboration-in-distr.md - 167-ai-mediated-representation-for-underrepresented-ex 167-ai-mediated-representation-for-underrepresented-ex.md - 0. Versioning Policy 24-12-versioning-policy.md 21% - AI-Coordinated Infrastructure for Distributed Expert Contribution 152-ai-coordinated-infrastructure-for-distributed-expe.md 53% - PORTAL-PROTOCOL.md v1.1 73-portal-protocol-md-v1-1.md 53% - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work 135-a-formal-model-for-human-ai-collaboration-in-distr.md 48% - 0. Versioning Policy 24-12-versioning-policy.md 25% - Author & Contact 42-author-contact.md 25% - Author & Contact 52-author-contact.md 25% --- - 05-0-status-of-this-document 05-0-status-of-this-document.md - 105-review-methodology-md 105-review-methodology-md.md - 123-portal-mcp-py 123-portal-mcp-py.md - 125-readme-mcp-md-инструкция-по-установке 125-readme-mcp-md-инструкция-по-установке.md - 129-примеры-запросов-в-claude 129-примеры-запросов-в-claude.md - 135-a-formal-model-for-human-ai-collaboration-in-distr 135-a-formal-model-for-human-ai-collaboration-in-distr.md - 152-ai-coordinated-infrastructure-for-distributed-expe 152-ai-coordinated-infrastructure-for-distributed-expe.md - 164-10-appendices 164-10-appendices.md - ...ещё 14

## `docs/02-anthropic-vacancies/04-abstract.md`

_Abstract_

> --- --- - 74-abstract 74-abstract.md сходство 0.43 --- - 74-abstract 74-abstract.md - 98-appendix-a-minimal-working-example 98-appendix-a-minimal-working-example.md - 42-author-contact 42-author-contact.md - 65-readme-md 65-readme-md.md - 14. Passport passport.md 09-4-passport-passport-md.md - Abstract 74-abstract.md - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md - Appendix B: Change Log 34-appendix-b-change-log.md - For the Curious: Philosophy 44-for-the-curious-philosophy.md - For the Curious: Philosophy 54-for-the-curious-philosophy.md - Native Format 37-native-format.md - Native Format 47-native-format.md - Planned v0.2.0 132-planned-v0-2-0.md - README.md 65-readme-md.md - REVIEW METHODOLOGY.md 105-review-methodology-md.md - portal- mcp.py 123-portal-mcp-py.md - Вакансии Anthropic — Анализ по кластерам README.md - Инвертированный индекс ключевых слов ../KEYWORD INDEX.md - Подключение к Claude Desktop 127-подключение-к-claude-desktop.md - Что ты ВСЕГДА делаешь 360-что-ты-всегда-делаешь.md - ⬡ 69-section.md - Вакансии Anthropic — Анализ по кластерам ../README.md - portal- mcp.py 123-portal-mcp-py.md 37% - For the Curious: Philosophy 54-for-the-curious-philosophy.md 37% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 33% - For the Curious: Philosophy 44-for-the-curious-philosophy.md 33% - For the Curious: Philosophy 64-for-the-curious-philosophy.md 33% - Abstract 74-abstract.md 33% - REVIEW METHODOLOGY.md 105-review-methodology-md.md 29% - Индекс «Смотрите также» ../SEE ALSO.md 29% - Abstract 74-abstract.md 42% - portal- mcp.py 123-portal-mcp-py.md 33% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 33% - For the Curious: Philosophy 44-for-the-curious-philosophy.md 33% - For the Curious: Philosophy 54-for-the-curious-philosophy.md 33% - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md 33% - Planned v0.2.0 132-planned-v0-2-0.md 29% - 0. Status of This Document 05-0-status-of-this-document.md 25% --- - 05-0-status-of-this-document 05-0-status-of-this-document.md - 09-4-passport-passport-md 09-4-passport-passport-md.md - 105-review-methodology-md 105-review-methodology-md.md - 123-portal- mcp-py 123-portal-mcp-py.md - 125-readme- mcp-md-инструкция-по-установке 125-readme-mcp-md-инструкция-по-установке.md - 127-подключение-к- claude-desktop 127-подключение-к-claude-desktop.md - 132-planned-v0-2-0 132-planned-v0-2-0.md - 164-10-appendices 164-10-appendices.md - ...ещё 11

## `docs/02-anthropic-vacancies/05-0-status-of-this-document.md`

_0. Status of This Document_

> Этот документ — рабочий черновик Nautilus Portal Protocol v1.0. --- --- - 75-0-status-of-this-document 75-0-status-of-this-document.md сходство 0.55 - 03-portal-protocol-md 03-portal-protocol-md.md сходство 0.22 - 42-author-contact 42-author-contact.md сходство 0.20 --- - 75-0-status-of-this-document 75-0-status-of-this-document.md - 42-author-contact 42-author-contact.md - 62-author-contact 62-author-contact.md - 03-portal-protocol-md 03-portal-protocol-md.md - 0. Status of This Document 75-0-status-of-this-document.md 90% - Author & Contact 42-author-contact.md 53% - Author & Contact 62-author-contact.md 42% - 13.

## `docs/02-anthropic-vacancies/06-1-introduction.md`

_1. Introduction_

> Абстракт авто 🎯 Проблема: Design Goals Протокол спроектирован так, чтобы одновременно достичь: - Low barrier to entry: подключение существующего репо к федерации требует не больше 5 минут работы два файла 🔧 Подход: Homogenization: разные типы знаний методология, семантика, символизм принудительно приводятся к одной структуре, что уменьшает выразительность. 🏷️ Ключевые слова: introduction , goals , anthropic , vacancies , проекте , federation , merging , motivation Современные системы управления знаниями Notion, Obsidian, Roam, Logseq, --- Современные системы управления знаниями Notion, Obsidian, Roam, Logseq, Coda, Confluence требуют от пользователя миграции в их единый формат. --- --- - 76-1-introduction 76-1-introduction.md сходство 0.53 - 67-о-проекте 67-о-проекте.md сходство 0.12 --- - 76-1-introduction 76-1-introduction.md - 67-о-проекте 67-о-проекте.md - 26-14-adr-001-federation-over-merging 26-14-adr-001-federation-over-merging.md - 94-19-adr-001-federation-over-merging 94-19-adr-001-federation-over-merging.md --- - 26-14-adr-001-federation-over-merging 26-14-adr-001-federation-over-merging.md - 67-о-проекте 67-о-проекте.md - 94-19-adr-001-federation-over-merging 94-19-adr-001-federation-over-merging.md - 95-20-adr-002-q6-as-first-class-protocol-concept 95-20-adr-002-q6-as-first-class-protocol-concept.md - README README.md

## `docs/02-anthropic-vacancies/07-2-terminology.md`

_2. Terminology_

> Repository-participant далее — Repo — Git-репозиторий, содержащий минимум nautilus ../05-habr-projects/memory/memnet.md .json и passport.md в корне. Registry — файл nautilus ../05-habr-projects/memory/memnet.md .json в корне Portal-репо, перечисляющий все Repos экосистемы с их метаданными. Описан в nautilus ../05-habr-projects/memory/memnet.md .json в поле bridges .

## `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md`

_3. Registry (`nautilus.json`)_

> Validation Rules #35-validation-rules !IMPORTANT Ключевой документ для понимания архитектуры. Registry — central source of truth о том, какие Repos входят в --- Registry — central source of truth о том, какие Repos входят в экосистему и как их интерпретировать. Registry MUST быть валидным JSON со следующей структурой: - protocol version — строка в формате semver.

## `docs/02-anthropic-vacancies/09-4-passport-passport-md.md`

_4. Passport (`passport.md`)_

> Compatibility Levels 80-5-compatibility-levels.md - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md - Compatibility Level 41-compatibility-level.md - History 63-history.md - Native Format 37-native-format.md - Planned v0.2.0 132-planned-v0-2-0.md - Вакансии Anthropic — Анализ по кластерам README.md - Что ты ВСЕГДА делаешь 360-что-ты-всегда-делаешь.md - Вакансии Anthropic — Анализ по кластерам ../README.md - Compatibility Level 41-compatibility-level.md 33% - Planned v0.2.0 132-planned-v0-2-0.md 25% - Native Format 37-native-format.md 25% - 5. Compatibility Levels 17-5-compatibility-levels.md 21% - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md 33% - Compatibility Level 41-compatibility-level.md 29% - 4. QueryResult Structure 22-10-queryresult-structure.md 25% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 25% - History 63-history.md 25% - Abstract 04-abstract.md 21% --- - 04-abstract 04-abstract.md - 127-подключение-к-claude-desktop 127-подключение-к-claude-desktop.md - 132-planned-v0-2-0 132-planned-v0-2-0.md - 22-10-queryresult-structure 22-10-queryresult-structure.md - 37-native-format 37-native-format.md - 41-compatibility-level 41-compatibility-level.md - 63-history 63-history.md - README README.md

## `docs/02-anthropic-vacancies/102-доступ-к-данным.md`

_Доступ к данным_

> - Доступ к данным #доступ-к-данным !WARNING Документ содержит описание рисков и ограничений. - Fallback: всегда возвращает static entries --- - Тип: static - Требует токен: нет - Fallback: всегда возвращает static entries bash python scripts/improve semantic search.py --query "Доступ к данным" - 339-приложение-a-дерево-решений-для-принимающих-ingit 339-приложение-a-дерево-решений-для-принимающих-ingit.md - 118-appendix-a-шаблон-для-header-warning 118-appendix-a-шаблон-для-header-warning.md - 121-appendix-c-история-изменений-методологии 121-appendix-c-история-изменений-методологии.md - 348-кому-ты-служишь-слоистая-модель 348-кому-ты-служишь-слоистая-модель.md - Appendix C: История изменений методологии 121-appendix-c-история-изменений-методологии.md 60% - Приложение A: Дерево Решений для Принимающих InGit 339-приложение-a-дерево-решений-для-принимающих-ingit.md 60% - Кому ты служишь слоистая модель 348-кому-ты-служишь-слоистая-модель.md 53% - Appendix A: Шаблон для header warning 118-appendix-a-шаблон-для-header-warning.md 42% - Когда ты Honestly не знаешь 361-когда-ты-honestly-не-знаешь.md 42% - Appendix B: Domain Comparison Matrix 185-appendix-b-domain-comparison-matrix.md 29% - Твоя миссия 347-твоя-миссия.md 29% - Главные технические риски 120-главные-технические-риски.md 25% --- - 121-appendix-c-история-изменений-методологии 121-appendix-c-история-изменений-методологии.md - 16-history 16-history.md - 185-appendix-b-domain-comparison-matrix 185-appendix-b-domain-comparison-matrix.md - 202-12-заключение 202-12-заключение.md - 206-приложение-b-матрица-сравнения-областей 206-приложение-b-матрица-сравнения-областей.md - 339-приложение-a-дерево-решений-для-принимающих-ingit 339-приложение-a-дерево-решений-для-принимающих-ingit.md - README README.md Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска. --- Похожие документы: - 102-доступ-к-данным ../obsidian/02-anthropic-vacancies/102-доступ-к-данным.md сходство 0.97 - 339-приложение-a-дерево-решений-для-принимающих-ingit 339-приложение-a-дерево-решений-для-принимающих-ingit.md сходство 0.54 - 339-приложение-a-дерево-решений-для-принимающих-ingit ../obsidian/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md сходство 0.53

## `docs/02-anthropic-vacancies/103-appendix-b-change-log.md`

_Appendix B: Change Log_

> Q6 Space Normative 83-8-q6-space-normative.md - Appendix C: References 104-appendix-c-references.md - Вакансии Anthropic — Анализ по кластерам README.md - Доступные инструменты 128-доступные-инструменты.md - Вакансии Anthropic — Анализ по кластерам ../README.md - 14. MCP Extension Informative 91-16-mcp-extension-informative.md 25% - Доступные инструменты 128-доступные-инструменты.md 21% - Appendix B: Change Log 34-appendix-b-change-log.md 21% - 6. Q6 Space Normative 83-8-q6-space-normative.md 21% --- - 104-appendix-c-references 104-appendix-c-references.md - 128-доступные-инструменты 128-доступные-инструменты.md - 22-10-queryresult-structure 22-10-queryresult-structure.md - 34-appendix-b-change-log 34-appendix-b-change-log.md - 91-16- mcp-extension-informative 91-16-mcp-extension-informative.md - 93-18-reference-implementation 93-18-reference-implementation.md - README README.md

## `docs/02-anthropic-vacancies/104-appendix-c-references.md`

_Appendix C: References_

> Nautilus Portal as Reference Substrate 141-4-nautilus-portal-as-reference-substrate.md - Appendix B: Change Log 103-appendix-b-change-log.md - Appendix B: Change Log 34-appendix-b-change-log.md - For the Curious: Philosophy 64-for-the-curious-philosophy.md - References 147-references.md - Вакансии Anthropic — Анализ по кластерам README.md - Глоссарий 122-глоссарий.md - Доступные инструменты 128-доступные-инструменты.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL 02-общий-план-развития-nautilus-portal-protocol.md - ⬡ 69-section.md - 🇬🇧 About 68-about.md - 🇷🇺 О проекте 67-о-проекте.md - Вакансии Anthropic — Анализ по кластерам ../README.md - 18. Reference Implementation 25-13-reference-implementation.md 25% - Appendix B: Change Log 34-appendix-b-change-log.md 21% - ⬡ 69-section.md 21% - Appendix B: Change Log 103-appendix-b-change-log.md 17% - Глоссарий 122-глоссарий.md 17% - References 147-references.md 17% - For the Curious: Philosophy 64-for-the-curious-philosophy.md 17% - 18. Reference Implementation 25-13-reference-implementation.md 29% - For the Curious: Philosophy 64-for-the-curious-philosophy.md 29% - 🇬🇧 About 68-about.md 29% - Appendix B: Change Log 103-appendix-b-change-log.md 25% - Глоссарий 122-глоссарий.md 25% - 4.

## `docs/02-anthropic-vacancies/105-review-methodology-md.md`

_REVIEW_METHODOLOGY.md_

> - REVIEW METHODOLOGY.md #review methodologymd !NOTE Документ создан на основе исследования. Статус: Активно применяется в проекте svend4/nautilus --- !NOTE Документ создан на основе исследования. markdown bash python scripts/improve semantic search.py --query "REVIEW METHODOLOGY md" - 28-appendix-a-minimal-working-example 28-appendix-a-minimal-working-example.md - 03-portal-protocol-md 03-portal-protocol-md.md - 42-author-contact 42-author-contact.md - 188-ai-опосредованное-представительство-для-недопредст 188-ai-опосредованное-представительство-для-недопредст.md - 10.

## `docs/02-anthropic-vacancies/106-tl-dr.md`

_TL;DR_

> --- --- - 70-зачем-две-версии-параллельно 70-зачем-две-версии-параллельно.md сходство 0.35 - 108-2-формальный-workflow 108-2-формальный-workflow.md сходство 0.14 - 107-1-контекст-и-мотивация 107-1-контекст-и-мотивация.md сходство 0.12 --- - 70-зачем-две-версии-параллельно 70-зачем-две-версии-параллельно.md - 108-2-формальный-workflow 108-2-формальный-workflow.md - 107-1-контекст-и-мотивация 107-1-контекст-и-мотивация.md - 105-review-methodology-md 105-review-methodology-md.md - 1. Условия применимости 111-4-условия-применимости.md - Вакансии Anthropic — Анализ по кластерам README.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md - Критерии выбора для фазы 3 71-критерии-выбора-для-фазы-3.md - Вакансии Anthropic — Анализ по кластерам ../README.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md 33% - Расписание фазы 3 72-расписание-фазы-3.md 17% - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md 42% - REVIEW METHODOLOGY.md 105-review-methodology-md.md 17% - 2. Формальный workflow 108-2-формальный-workflow.md 17% - Критерии выбора для фазы 3 71-критерии-выбора-для-фазы-3.md 17% --- - 105-review-methodology-md 105-review-methodology-md.md - 70-зачем-две-версии-параллельно 70-зачем-две-версии-параллельно.md - 71-критерии-выбора-для-фазы-3 71-критерии-выбора-для-фазы-3.md - 72-расписание-фазы-3 72-расписание-фазы-3.md - README README.md

## `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md`

_1. Контекст и мотивация_

> ✅ Результат: Каждый запуск создаёт отдельную ветку, на которой агент работает независимо от других. Проект Nautilus разрабатывается в паре «автор + Claude Code агент». Каждый запуск создаёт отдельную ветку, на которой агент работает независимо от других.

## `docs/02-anthropic-vacancies/108-2-формальный-workflow.md`

_2. Формальный workflow_

> Фаза A Фаза B Фаза C --- Методология применяется только к критически важным документам , где стоимость потери информации высока. Примеры из Nautilus: - STATUS.md — отчёт о состоянии проекта - IMPLEMENTATION STAGE PART .md — технико-концептуальный review - PORTAL-PROTOCOL.md — formal specification Для routine документов README, adapter docs, passport templates достаточно single-pass review. --- --- - 114-7-реализация-в-проекте-nautilus 114-7-реализация-в-проекте-nautilus.md сходство 0.18 - 117-10-конкретный-план-применения-к-текущим-документам 117-10-конкретный-план-применения-к-текущим-документам.md сходство 0.14 - 106-tl-dr 106-tl-dr.md сходство 0.14 --- - 114-7-реализация-в-проекте-nautilus 114-7-реализация-в-проекте-nautilus.md - 117-10-конкретный-план-применения-к-текущим-документам 117-10-конкретный-план-применения-к-текущим-документам.md - 106-tl-dr 106-tl-dr.md - COMPLEXITY ../COMPLEXITY.md --- - 105-review-methodology-md 105-review-methodology-md.md - 106-tl-dr 106-tl-dr.md - 109-3-принципы-консолидации-фаза-c 109-3-принципы-консолидации-фаза-c.md - 122-глоссарий 122-глоссарий.md - 72-расписание-фазы-3 72-расписание-фазы-3.md - README README.md

## `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md`

_3. Принципы консолидации (Фаза C)_

> Для каждого расхождения применяются правила #31-для-каждого-расхождения-применяются-правила - Native Format #native-format --- Абстракт авто 🎯 Проблема: Пример: - A: «88% fallback — критическая проблема, требует срочного решения» - B: «88% fallback — осмысленный tradeoff, приоритет средний» → В финальной версии обе позиции сохраняю 🔧 Подход: Если избегаете трёхфазного подхода, эти 10-15% теряются безвозвратно. --- - 71-критерии-выбора-для-фазы-3 71-критерии-выбора-для-фазы-3.md сходство 0.21 --- - 71-критерии-выбора-для-фазы-3 71-критерии-выбора-для-фазы-3.md - 107-1-контекст-и-мотивация 107-1-контекст-и-мотивация.md - 108-2-формальный-workflow 108-2-формальный-workflow.md - 82-7-portalentry-structure 82-7-portalentry-structure.md - 2. Terminology 77-2-terminology.md 17% --- - 104-appendix-c-references 104-appendix-c-references.md - 64-for-the-curious-philosophy 64-for-the-curious-philosophy.md - 71-критерии-выбора-для-фазы-3 71-критерии-выбора-для-фазы-3.md - 74-abstract 74-abstract.md - README README.md

## `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md`

_Вопрос: fallback-ratio как критический или осмысленный?_

> #вопрос-fallback-ratio-как-критический-или-осмысленный Абстракт авто 🎯 Проблема: Два независимых анализа пришли к разным выводам: - Позиция A: 88% fallback критично, требует срочных живых адаптеров для info1/pro2/meta/data2 - Позиция B: 88% fallback — осмысленн 🔧 Подход: !IMPORTANT Ключевой документ для понимания архитектуры. 🏷️ Ключевые слова: fallback , anthropic , vacancies , решение , проекта , версии , метрика , count !IMPORTANT Ключевой документ для понимания архитектуры. Два независимых анализа пришли к разным выводам: --- Два независимых анализа пришли к разным выводам: - Позиция A : 88% fallback критично, требует срочных живых адаптеров для info1 01-интегральный-анализ-профиля-svend4.md /pro2/meta/data2 - Позиция B : 88% fallback — осмысленное решение для early-stage проекта, приоритет средний Текущее решение автора : ваше решение + обоснование 1.

## `docs/02-anthropic-vacancies/111-4-условия-применимости.md`

_4. Условия применимости_

> 🔧 Подход: Когда оппонирует 43-когда-оппонирует Методология не универсальна. 🏷️ Ключевые слова: когда , применять , anthropic , vacancies , условия , применимости , формальный , workflow Методология не универсальна. Она уместна при следующих условиях : --- Методология не универсальна.

## `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md`

_5. Связь с существующими методологиями_

> 🔧 Подход: Новое в данной методологии 55-новое-в-данной-методологии Теоретическим прародителем является N-version programming --- 5. 🏷️ Ключевые слова: version , programming , связь , существующими , методологиями , reviews , ensembles , отличия Теоретическим прародителем является N-version programming --- Теоретическим прародителем является N-version programming Chen & Avizienis, 1977–78 — написание нескольких независимых имплементаций одной спецификации для повышения reliability. Отличия: - ML ensembles: разрешение автоматическое, по правилу - Наша методология: разрешение ручное, через правила 1-5 В security и public policy используется структура red vs blue : один агент критикует, другой защищает.

## `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md`

_6. Почему это валидный паттерн для AI-assisted workflows_

> Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска. Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска. Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска.

## `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md`

_7. Реализация в проекте Nautilus_

> Первое применение — IMPLEMENTATION STAGE PART 1-4 .md --- Первое применение — IMPLEMENTATION STAGE PART 1-4 .md апрель 2026 : - Вариант A: ветка claude/review- nautilus ../05-habr-projects/memory/memnet.md -changes-tdywx - Вариант B: ветка claude/project-implementation-stage-CzylE - Текущий статус: Merged-to-main with parallel blocks, Фаза C не пройдена Повторное применение — STATUS.md апрель 2026 : - Пройдена Фаза A единожды single-pass - Статус: канонично, трёхфазная методология не применялась - Осмысленность: документ достаточно простой для single-pass Пример, что методология применяется селективно , только там, где польза оправдывает overhead. Исходные draft ветки claude/ — как audit trail 2. Финальная консолидированная — после Фазы C Удалять исходные ветки не следует до завершения Фазы C — они могут содержать контекст, нужный для разрешения неочевидных расхождений.

## `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md`

_8. Ограничения и открытые вопросы_

> Что делать, если ресурсов на Фазу C нет #83-что-делать-если-ресурсов-на-фазу-c-нет - Похожие документы #похожие-документы - Использование #использование - Смотрите также #смотрите-также --- Абстракт авто 🎯 Проблема: Вернуться к формулировке задачи, уточнить scope, и только потом запускать параллельные review заново. 🔧 Подход: Что делать, если ресурсов на Фазу C нет Если трёхфазная методология применена к документу, но времени на Фазу C нет и не предвидится в течение 2 недель : 1. Если трёхфазная методология применена к документу, но времени на Фазу C нет и не предвидится в течение 2 недель : 1.

## `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md`

_9. Checklist применения методологии_

> Во время Фазы A и B #92-во-время-фазы-a-и-b - 9.3. ✅ Результат: Во время Фазы A и B - Агенты работают в разных ветках не в одной - Prompt'ы для A и B идентичны иначе это не независимое воспроизведение - Каждый агент не видит результат друго 🏷️ Ключевые слова: checklist , применения , методологии , перед , время , документ , началом , phase !WARNING Документ содержит описание рисков и ограничений. - Агенты работают в разных ветках не в одной - Prompt'ы для A и B идентичны иначе это не независимое воспроизведение - Каждый агент не видит результат другого - Header warning добавлен см.

## `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md`

_10. Конкретный план применения к текущим документам_

> Конкретный план применения к текущим документам #10-конкретный-план-применения-к-текущим-документам - 10.1. Абстракт авто 🎯 Проблема: Конкретный план применения к текущим документам Contents - 10. 🔧 Подход: Будущие применения Планируемые кандидаты на трёхфазную методологию: - ARCHITECTURE.md если создаётся — формальное описание архитектуры - CONTRIBUTING.md если создаётся — guidel ✅ Результат: Провести верификацию конкретных метрик: Результат — вставить в финальный консолидированный документ вместо обоих вариантов.

## `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md`

_Appendix A: Шаблон для header warning_

> Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. --- Похожие документы: - 118-appendix-a-шаблон-для-header-warning ../obsidian/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md сходство 0.93 - 12-appendix-a-header-warning ../obsidian/nautilus/review-methodology/12-appendix-a-header-warning.md сходство 0.64 - 12-appendix-a-header-warning ../nautilus/review-methodology/12-appendix-a-header-warning.md сходство 0.61

## `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md`

_Appendix B: Примеры расхождений и их разрешения_

> 🔧 Подход: Расхождение в концептуальных выводах Правило 5 Гипотетический пример: Разрешение: оба риска реальны, приоритезация зависит от цели проекта. ✅ Результат: Расхождение в концептуальных выводах Правило 5 Гипотетический пример: Разрешение: оба риска реальны, приоритезация зависит от цели проекта. Гипотетический пример : Разрешение : оба риска реальны, приоритезация зависит от цели проекта.

## `docs/02-anthropic-vacancies/12-content-overview.md`

_Content Overview_

> - Content Overview #content-overview - Похожие документы #похожие-документы - Упоминается в #упоминается-в - Упоминается в #упоминается-в-1 - Связанные документы #связанные-документы - Связанные документы #связанные-документы-1 - Использование #использование - Смотрите также #смотрите-также - Кто ссылается на этот документ 10 #кто-ссылается-на-этот-документ-10 !NOTE Документ создан на основе исследования. Что внутри: типы данных, приблизительный объём, основные темы. --- Что внутри: типы данных, приблизительный объём, основные темы.

## `docs/02-anthropic-vacancies/120-главные-технические-риски.md`

_Главные технические риски_

> - Главные технические риски #главные-технические-риски !NOTE Документ создан на основе исследования. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo.

## `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md`

_Appendix C: История изменений методологии_

> - Appendix C: История изменений методологии #appendix-c-история-изменений-методологии - v1.0 2026-04 #v10-2026-04 - Упоминается в #упоминается-в - Упоминается в #упоминается-в-1 - Использование #использование - Смотрите также #смотрите-также - Связанные документы #связанные-документы - Кто ссылается на этот документ 6 #кто-ссылается-на-этот-документ-6 !WARNING Документ содержит описание рисков и ограничений. Будущие версии методологии будут задокументированы в этом appendix. Почему это валидный паттерн для AI-assisted workflows 113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md - Appendix A: Шаблон для header warning 118-appendix-a-шаблон-для-header-warning.md - Appendix B: Domain Comparison Matrix 185-appendix-b-domain-comparison-matrix.md - History 16-history.md - Вакансии Anthropic — Анализ по кластерам README.md - Главные технические риски 120-главные-технические-риски.md - Доступ к данным 102-доступ-к-данным.md - Когда ты Honestly не знаешь 361-когда-ты-honestly-не-знаешь.md - Кому ты служишь слоистая модель 348-кому-ты-служишь-слоистая-модель.md - Приложение A: Дерево Решений для Принимающих InGit 339-приложение-a-дерево-решений-для-принимающих-ingit.md - Приложение B: Матрица Сравнения Областей 206-приложение-b-матрица-сравнения-областей.md - Твои anti-patterns 359-твои-anti-patterns.md - Твоя миссия 347-твоя-миссия.md - Вакансии Anthropic — Анализ по кластерам ../README.md --- - 102-доступ-к-данным 102-доступ-к-данным.md - 118-appendix-a-шаблон-для-header-warning 118-appendix-a-шаблон-для-header-warning.md - 339-приложение-a-дерево-решений-для-принимающих-ingit 339-приложение-a-дерево-решений-для-принимающих-ingit.md - 185-appendix-b-domain-comparison-matrix 185-appendix-b-domain-comparison-matrix.md - Доступ к данным 102-доступ-к-данным.md 60% - Приложение A: Дерево Решений для Принимающих InGit 339-приложение-a-дерево-решений-для-принимающих-ingit.md 60% - Кому ты служишь слоистая модель 348-кому-ты-служишь-слоистая-модель.md 53% - Appendix A: Шаблон для header warning 118-appendix-a-шаблон-для-header-warning.md 42% - Когда ты Honestly не знаешь 361-когда-ты-honestly-не-знаешь.md 42% - Appendix B: Domain Comparison Matrix 185-appendix-b-domain-comparison-matrix.md 29% - Твоя миссия 347-твоя-миссия.md 29% - Главные технические риски 120-главные-технические-риски.md 25% --- - 102-доступ-к-данным 102-доступ-к-данным.md - 16-history 16-history.md - 185-appendix-b-domain-comparison-matrix 185-appendix-b-domain-comparison-matrix.md - 206-приложение-b-матрица-сравнения-областей 206-приложение-b-матрица-сравнения-областей.md - 339-приложение-a-дерево-решений-для-принимающих-ingit 339-приложение-a-дерево-решений-для-принимающих-ingit.md - README README.md --- Похожие документы: - 121-appendix-c-история-изменений-методологии ../obsidian/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md сходство 0.97 - 339-приложение-a-дерево-решений-для-принимающих-ingit 339-приложение-a-дерево-решений-для-принимающих-ingit.md сходство 0.65 - 339-приложение-a-дерево-решений-для-принимающих-ingit ../obsidian/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md сходство 0.63

## `docs/02-anthropic-vacancies/122-глоссарий.md`

_Глоссарий_

> ✅ Результат: IMPLEMENTATIONSTAGEPART1-4.md — технико-концептуальный review в transitional state, готовый к Фазе C После того, как PORTAL-PROTOCOL и REVIEWMETHODOLOGY скоммитятся в репо, у вас д 🏷️ Ключевые слова: review , portal , methodology , документ , appendix , nautilus , методология , protocol !WARNING Документ содержит описание рисков и ограничений. Реализация в проекте Nautilus 114-7-реализация-в-проекте-nautilus.md - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md - Appendix B: Change Log 34-appendix-b-change-log.md - Appendix C: References 104-appendix-c-references.md - For the Curious: Philosophy 64-for-the-curious-philosophy.md - README-MCP.md— инструкция по установке 125-readme-mcp-md-инструкция-по-установке.md - REVIEW METHODOLOGY.md 105-review-methodology-md.md - Вакансии Anthropic — Анализ по кластерам README.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md - Конфигурация для Claude Desktop 124-конфигурация-для-claude-desktop.md - Расписание фазы 3 72-расписание-фазы-3.md - ⬡ 69-section.md - 🇷🇺 О проекте 67-о-проекте.md - Вакансии Anthropic — Анализ по кластерам ../README.md - README-MCP.md— инструкция по установке 125-readme-mcp-md-инструкция-по-установке.md 25% - ⬡ 69-section.md 21% - Расписание фазы 3 72-расписание-фазы-3.md 21% - Индекс обратных ссылок ../BACKLINKS.md 21% - Appendix C: References 104-appendix-c-references.md 17% - REVIEW METHODOLOGY.md 105-review-methodology-md.md 17% - 13. Reference Implementation 25-13-reference-implementation.md 17% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 17% - README-MCP.md— инструкция по установке 125-readme-mcp-md-инструкция-по-установке.md 33% - REVIEW METHODOLOGY.md 105-review-methodology-md.md 29% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 29% - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md 29% - Расписание фазы 3 72-расписание-фазы-3.md 29% - Appendix C: References 104-appendix-c-references.md 25% - Appendix B: Change Log 34-appendix-b-change-log.md 25% - For the Curious: Philosophy 64-for-the-curious-philosophy.md 25% --- - 02-общий-план-развития-nautilus-portal-protocol 02-общий-план-развития-nautilus-portal-protocol.md - 104-appendix-c-references 104-appendix-c-references.md - 105-review-methodology-md 105-review-methodology-md.md - 124-конфигурация-для-claude-desktop 124-конфигурация-для-claude-desktop.md - 125-readme-mcp-md-инструкция-по-установке 125-readme-mcp-md-инструкция-по-установке.md - 34-appendix-b-change-log 34-appendix-b-change-log.md - 64-for-the-curious-philosophy 64-for-the-curious-philosophy.md - 67-о-проекте 67-о-проекте.md - ...ещё 3

## `docs/02-anthropic-vacancies/123-portal-mcp-py.md`

_portal-mcp.py_

> Абстракт авто 🎯 Проблема: portal-mcp.py !IMPORTANT Ключевой документ для понимания архитектуры. 🔧 Подход: portal-mcp.py !IMPORTANT Ключевой документ для понимания архитектуры. 🏷️ Ключевые слова: anthropic , vacancies , readme , appendix , minimal , working , example , portal !IMPORTANT Ключевой документ для понимания архитектуры.

## `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md`

_Конфигурация для Claude Desktop_

> После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигурации MCP. Путь зависит от ОС: --- После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигурации MCP. Terminology 77-2-terminology.md 17% --- - 122-глоссарий 122-глоссарий.md - 125-readme- mcp-md-инструкция-по-установке 125-readme-mcp-md-инструкция-по-установке.md - 127-подключение-к- claude-desktop 127-подключение-к-claude-desktop.md - 129-примеры-запросов-в-claude 129-примеры-запросов-в-claude.md - 130-отладка 130-отладка.md - README README.md



## Использование
```bash
# Запуск
python scripts/improve_summaries.py
```
```bash
# Вариант 2
python scripts/improve_summaries.py --dry-run
```
```bash
# Вариант 3
python scripts/improve_summaries.py --dry-run
```

## Смотрите также
- [Главная](README.md)
- [Метрики](METRICS.md)
- [Здоровье](HEALTH.md)
- [Глоссарий](GLOSSARY.md)
- [Сущности](ENTITIES.md)
- [Решения](DECISIONS.md)
- [Контакты](CONTACTS.md)
- [Оценка](SCORING.md)
- [Теги](TAGS.md)
- [Задачи](ACTION_ITEMS.md)

<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [CONCEPTS](CONCEPTS.md)
- [OUTLINE](OUTLINE.md)
- [READABILITY](READABILITY.md)
- [READING_TIME](READING_TIME.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [TABLES](TABLES.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [SUMMARIES](obsidian/SUMMARIES.md) (сходство 1.00)
- [READING_ORDER](READING_ORDER.md) (сходство 0.22)
- [READING_ORDER](obsidian/READING_ORDER.md) (сходство 0.22)

