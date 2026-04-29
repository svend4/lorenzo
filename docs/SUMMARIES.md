# Резюме документов (TextRank)

_Обновлено: 2026-04-29_

Файлов: **903** | Предложений: **3** на документ

## `docs/01-svyazi/01-executive-summary.md`

_Svyazi[^svyazi] 2.0 — Исполнительное резюме_

> - Contents #contents - Главная линия синергии #главная-линия-синергии - Ключевой вывод #ключевой-вывод - Что добавляет продолжение исследования #что-добавляет-продолжение-исследования - Приоритет ансамблей для старта #приоритет-ансамблей-для-старта --- Абстракт авто 🎯 Проблема: Svyazi^svyazi 2.0 — Исполнительное резюме Contents - Главная линия синергии главная-линия-синергии - Ключевой вывод ключевой-вывод - Что добавляет продолжение исследования что-до ✅ Результат: Первое — Svyazi + AgentFS + NGT/Yodoca + LiteParse: даёт уже полезный MVP 2. 🏷️ Ключевые слова: svyazi , проект , cardindex , agentfs , добавляет , продолжение , rufler , memory - Главная линия синергии #главная-линия-синергии - Ключевой вывод #ключевой-вывод - Что добавляет продолжение исследования #что-добавляет-продолжение-исследования - Приоритет ансамблей для старта #приоритет-ансамблей-для-старта !IMPORTANT Главный документ проекта. Первое — Svyazi + AgentFS + NGT/Yodoca + LiteParse: даёт уже полезный MVP 2.

## `docs/01-svyazi/02-methodology.md`

_Методика и рамка отбора проектов_

> Абстракт авто 🎯 Проблема: Методика и рамка отбора проектов Contents - Источники источники - Шкала зрелости шкала-зрелости - Принцип отбора паттернов принцип-отбора-паттернов - Принципы интеграционной оце 🔧 Подход: Методика и рамка отбора проектов Contents - Источники источники - Шкала зрелости шкала-зрелости - Принцип отбора паттернов принцип-отбора-паттернов - Принципы интеграционной оце ✅ Результат: Лицензия — позволяет ли лицензия встроить в более широкую систему? Поиск вёлся с приоритетом на Хабр как первичный слой описания идеи и на репозитории как первичный слой верификации лицензии, зрелости и интеграционного интерфейса . Проекты: Svyazi ^svyazi , LiteParse ../docs/01-svyazi/01-executive-summary.md , Legal RAG ^rag , Graph RAG --- Поиск вёлся с приоритетом на Хабр как первичный слой описания идеи и на репозитории как первичный слой верификации лицензии, зрелости и интеграционного интерфейса .

## `docs/01-svyazi/03-component-catalog.md`

_03-component-catalog_

> citeturn33view1turn37search1 Высокая : это внешний knowledge layer для агентов и нормализатора. citeturn22view3turn32search2 Очень высокая : быстрый ассоциативный memory‑слой для discovery и matching. citeturn15search3turn39view3 Высокая : слой typed memory и governance для более поздних итераций.

## `docs/01-svyazi/04-ensembles-overview.md`

_04-ensembles-overview_

> citeturn33view3turn37search1 Ансамбль B — Forensic RAG ^rag для доказуемого matching и review Если Svyazi‑2.0 должен не только находить людей и идеи, но и объяснять, почему возникла рекомендация, нужен evidence‑first слой. citeturn21view10turn35search0 - Локальная обработка вместо облачной утечки контекста : и локальный speech‑to‑text, и local‑first workspace, и CRDT ^crdt ‑sync работают в модели “данные принадлежат устройству пользователя”. citeturn35search0 - Контекст реального мира доступен агенту как tool, а не как догадка : Self‑Aware MCP закрывает проблемы часового пояса, ОС, даты и локации.

## `docs/01-svyazi/06-security-privacy.md`

_06-security-privacy_

> 🏷️ Ключевые слова: search , memory , только , svyazi , безопасность , бюджетный , роутинг , нужен Для Svyazi ^svyazi ‑2.0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP ^mcp servers, импорты документов и memory writes потенциально недоверенными . Это не паранойя, Проекты: Svyazi, AgentFS ^agentfs , AI Factory, agent-memory-mcp, SENTINEL ^sentinel , LiteLLM, Auto AI Router, Tool Search --- Для Svyazi‑2.0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP servers, импорты документов и memory writes потенциально недоверенными . В‑третьих, Auto AI Router и LiteLLM позволяют скрыть провайдерную сложность за единым API, а RLM‑Toolkit прямо формализует budget‑first / privacy‑first конфигурации.

## `docs/01-svyazi/07-mvp-planning.md`

_07-mvp-planning_

> Абстракт авто 🎯 Проблема: citeturn33view3turn20view2turn37search0 Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn33view3turn20view2turn37search0 Комментарии к статьям; issues/discussions в репозиториях knowledge-space и mclaude. citeturn21view0turn21view1turn18search1 Комментарии к статье Yodoca и GitHub issues/discussions в repo.

## `docs/01-svyazi/08-conclusions.md`

_08-conclusions_

> 🔧 Подход: По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей, не придумывая половину архитектуры заново. 🏷️ Ключевые слова: summary , svyazi , executive , проект , выводы , collaborations , first , cardindex По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитектуры заново. Самый дефицитный слой — не память, не RAG ^rag и не оркестр Проекты: Svyazi ^svyazi , CardIndex ^cardindex , AgentFS ^agentfs , mclaude, AI Factory, Rufler ^rufler , LiteParse ../docs/01-svyazi/01-executive-summary.md , Yodoca ^yodoca --- По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитектуры заново.

## `docs/01-svyazi/09-architectural-gaps.md`

_09-architectural-gaps_

> ✅ Результат: Наоборот, даже средний model tier даёт много пользы, если extract/normalize/review/evidence и memory status already pinned. В‑третьих, нужен memory governance layer , который не даёт ассоциативной памяти записывать предлагаемое как истинное. Наоборот, даже средний model tier даёт много пользы, если extract/normalize/review/evidence и memory status already pinned.

## `docs/01-svyazi/10-second-order-ensembles.md`

_10-second-order-ensembles_

> 🔧 Подход: citeturn27view0turn11search0turn11search11turn22view4turn20view12turn39view0turn20view10 Главное новое свойство здесь — не только privacy, но и архитектурная живучесть. 🏷️ Ключевые слова: svyazi , ансамбли , новые , search , проект , просто , knowledge , space Самые интересные продолжения — не просто добавление ещё одного инструмента в уже найденные пять ансамблей, а сборка трёх новых ансамблей второго порядка , где компоненты перестают быть “рядами функ Проекты: Svyazi ^svyazi , CardIndex ^cardindex , AgentFS ^agentfs , knowledge-space ../docs/01-svyazi/03-component-catalog.md ^knowledge-space , mclaude, AI Factory, Rufler ^rufler , LiteParse --- Самые интересные продолжения — не просто добавление ещё одного инструмента в уже найденные пять ансамблей, а сборка трёх новых ансамблей второго порядка , где компоненты перестают быть “рядами функций” и начинают образовывать новые свойства на уровне процесса сообщества, исследовательской группы или прототипной фабрики. citeturn27view0turn11search0turn11search11turn22view4turn20view12turn39view0turn20view10 Главное новое свойство здесь — не только privacy, но и архитектурная живучесть .

## `docs/01-svyazi/11-integration-contracts.md`

_11-integration-contracts_

> 🔧 Подход: Любой retrieval‑ответ, match suggestion, profile enrichment или auto‑summary должен возвращать не только текст, но и sourceid, page, span, box, retrievalmethod, confidence, support ✅ Результат: Это не “идеальная онтология”, а минимальный договор, который позволяет системам вообще разговаривать между собой. 🏷️ Ключевые слова: контракт , memory , svyazi , который , через , search , проект , agentfs Чтобы все эти ансамбли не рассыпались, полезно зафиксировать минимальный интерфейсный контракт между слоями. Это не заменяет будущую реализацию, но резко уменьшает риск того, что через две недели Проекты: Svyazi ^svyazi , CardIndex ^cardindex , AgentFS ^agentfs , mclaude, AI Factory, LiteParse ../docs/01-svyazi/01-executive-summary.md , Legal RAG ^rag , Hybrid RAG --- Чтобы все эти ансамбли не рассыпались, полезно зафиксировать минимальный интерфейсный контракт между слоями.

## `docs/01-svyazi/12-roadmap.md`

_12-roadmap_

> 🏷️ Ключевые слова: итерации , svyazi , memory , дорожная , карта , first , evidence , local Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти три короткие итерации , каждая из которых поднимает один новый класс свойств. Первая итерация должна закрепить Проекты: Svyazi ^svyazi , mclaude, AI Factory, Yodoca ^yodoca , NGT ^ngt Memory --- Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти три короткие итерации , каждая из которых поднимает один новый класс свойств. Это хорошая новость: такую архитектуру можно собрать без огромной команды, если с самого начала дисциплинировать стыки.

## `docs/01-svyazi/13-contacts.md`

_13-contacts_

> citeturn41search0turn33view2turn27view0turn21view0turn22view4 Самый логичный первый контакт — entity "people","Андрей Чуян","habr author"  , потому что именно у него уже есть работающий кейс карт коллабораций и CardIndex ../docs/01-svyazi/01-executive-summary.md ‑мышление. citeturn22view4turn22view5turn32search2 Пятый разговор имеет смысл вести с авторами knowledge-space ../docs/01-svyazi/03-component-catalog.md и mclaude, потому что именно здесь хорошо сходятся agent‑readable knowledge এবং multi‑session coordination. citeturn22view4turn22view5 авторы knowledge-space / mclaude Держать операционные benchmark/gotcha cards в одной базе с reference cards или отдельным слоем?

## `docs/01-svyazi/14-limitations.md`

_14-limitations_

> Абстракт авто 🎯 Проблема: Такой порядок согласуется и с Yttri‑подходом к workspace вокруг записей, и с простыми локальными whisper‑сценариями, и с идеей local-first sync как следующего, а не первого слоя сл 🔧 Подход: Такой порядок согласуется и с Yttri‑подходом к workspace вокруг записей, и с простыми локальными whisper‑сценариями, и с идеей local-first sync как следующего, а не первого слоя сл ✅ Результат: citeturn41search0turn27view0turn20view5turn21view0turn39view1turn20view10 --- Похожие документы: - 14-ограничения-лицензии-и-что-пока-лучше-не-склеивать docs/04-ai-collabor 🏷️ Ключевые слова: svyazi , memory , лучше , search , rufler , roadmap , ограничения , лицензии Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зрелости и лицензирования. Svyazi ^svyazi как базовый паттерн остаётся авторским закрытым п Проекты: Svyazi, mclaude, AI Factory, Rufler ^rufler , NGT ^ngt Memory, AutoResearch ../docs/01-svyazi/01-executive-summary.md , Whisper, Yttri --- Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зрелости и лицензирования. Лучший следующий шаг — не искать ещё двадцать новых проектов , а собрать второй, более строгий слой поверх уже найденных: Card Envelope, Evidence Envelope, Memory Write Policy, Skill Policy и Review Record.

## `docs/01-svyazi/README.md`

_Svyazi[^svyazi] 2.0 — Архитектура и исследование_

> Файлов: 14 - 00-intro-part2.md 00-intro-part2.md — - 01-executive-summary.md 01-executive-summary.md — Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже слож… - 02-methodology.md 02-methodology.md — Поиск вёлся с приоритетом на Хабр как первичный слой описания идеи и на репозитории как первичный слой верификации… - 03-component-catalog.md 03-component-catalog.md — Проект или связка Автор Ссылка на статью и репо Краткое описание Ключевые компоненты и паттерны Лицензия M… - 04-ensembles-overview.md 04-ensembles-overview.md — Ниже — не все теоретически возможные комбинации, а пять ансамблей с максимальным приростом свойств при минимальном инт… - 06-security-privacy.md 06-security-privacy.md — Для Svyazi‑2.0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP ^mcp servers, и… - 07-mvp-planning.md 07-mvp-planning.md — Наиболее рациональный прототип — не собирать всё сразу , а доказать одну центральную способность: система находит и … - 08-conclusions.md 08-conclusions.md — По итогам поиска видно, что Svyazi‑2.0 уже можно собирать из существующих software‑first кирпичей , не придумывая пол… - 09-architectural-gaps.md 09-architectural-gaps.md — После первичного обзора видно, что дефицит уже не в наличии компонентов, а в стыках между ними . Svyazi хорошо закрыв… - 10-second-order-ensembles.md 10-second-order-ensembles.md — Самые интересные продолжения — не просто добавление ещё одного инструмента в уже найденные пять ансамблей, а сборка тр… - 11-integration-contracts.md 11-integration-contracts.md — Чтобы все эти ансамбли не рассыпались, полезно зафиксировать минимальный интерфейсный контракт между слоями. Это не … - 12-roadmap.md 12-roadmap.md — Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти три короткие итерации , каждая… - 13-contacts.md 13-contacts.md — С практической точки зрения следующие письма или комментарии лучше строить не вокруг общей фразы “давайте сделаем Svyazi… - 14-limitations.md 14-limitations.md — Самое важное ограничение не техническое, а управленческое: часть самых ценных компонентов находится в разных режимах зре… - ensembles/ ensembles/ — Ансамбли проектов --- Похожие документы: - README docs/04-ai-collaborations/README.md сходство 0.67 - PRIORITIES docs/PRIORITIES.md сходство 0.11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов

## `docs/02-anthropic-vacancies/00-intro.md`

_Введение_

> Параллельно в AI Research & Engineering есть Research Engineer / Research Scientist, Societal Impacts SF, 2 роли . Если и есть ваш «главный проект», который стоит довести до shipping — это он. daten ⭐1 Python, Jan 12 — pinned, основной «иос», уже разбирали.

## `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md`

_Интегральный анализ профиля svend4_

> Если в nautilus ../docs/05-habr-projects/memory/memnet.md уже есть эти 4 компонента, это готовая инфраструктура для того, чтобы упаковать ваши 70 репо в coherent navigable portal. nautilus ../docs/05-habr-projects/memory/memnet.md — это папка внутри pro2 , а не отдельный самостоятельный проект. Пришлёте мне README info1, pro2, meta если есть , и один пример nautilus ../docs/05-habr-projects/memory/memnet.md .json + один адаптер из adapters/ .

## `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md`

_ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL_

> --- - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL #общий-план-развития- nautilus ../docs/05-habr-projects/memory/memnet.md -portal-protocol - Часть 1. Чтобы подключить репо к Nautilus — нужен только nautilus ../docs/05-habr-projects/memory/memnet.md .json 10–20 строк JSON и passport.md 1 страница markdown . nautilus ../docs/05-habr-projects/memory/memnet.md .json включает поле protocol version .

## `docs/02-anthropic-vacancies/03-portal-protocol-md.md`

_PORTAL-PROTOCOL.md_

> Status: Draft Working Document --- markdown markdown Version: 1.0.0-draft Status: Draft Working Document Author: svend4 License: CC BY 4.0 documentation / MIT reference implementation Date: 2026-04 --- --- Похожие документы: - 73-portal-protocol-md-v1-1 73-portal-protocol-md-v1-1.md сходство 0.47 - 167-ai-mediated-representation-for-underrepresented-ex 167-ai-mediated-representation-for-underrepresented-ex.md сходство 0.38 - 152-ai-coordinated-infrastructure-for-distributed-expe 152-ai-coordinated-infrastructure-for-distributed-expe.md сходство 0.36 --- Смотрите также: - 152-ai-coordinated-infrastructure-for-distributed-expe 152-ai-coordinated-infrastructure-for-distributed-expe.md - 73-portal-protocol-md-v1-1 73-portal-protocol-md-v1-1.md - 135-a-formal-model-for-human-ai-collaboration-in-distr 135-a-formal-model-for-human-ai-collaboration-in-distr.md - 167-ai-mediated-representation-for-underrepresented-ex 167-ai-mediated-representation-for-underrepresented-ex.md - 0. Reference Implementation 93-18-reference-implementation.md - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work 135-a-formal-model-for-human-ai-collaboration-in-distr.md - AI-Coordinated Infrastructure for Distributed Expert Contribution 152-ai-coordinated-infrastructure-for-distributed-expe.md - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md - Author & Contact 42-author-contact.md - Author & Contact 62-author-contact.md - For the Curious: Philosophy 54-for-the-curious-philosophy.md - PORTAL-PROTOCOL.md v1.1 73-portal-protocol-md-v1-1.md - README-MCP.md— инструкция по установке 125-readme-mcp-md-инструкция-по-установке.md - README.md 65-readme-md.md - REVIEW METHODOLOGY.md 105-review-methodology-md.md - portal-mcp.py 123-portal-mcp-py.md - Вакансии Anthropic — Анализ по кластерам README.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md - Примеры запросов в Claude 129-примеры-запросов-в-claude.md - Ссылки 338-ссылки.md - Вакансии Anthropic — Анализ по кластерам ../README.md - PORTAL-PROTOCOL.md v1.1 73-portal-protocol-md-v1-1.md 81% - AI-Coordinated Infrastructure for Distributed Expert Contribution 152-ai-coordinated-infrastructure-for-distributed-expe.md 60% - Author & Contact 52-author-contact.md 53% - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work 135-a-formal-model-for-human-ai-collaboration-in-distr.md 48% - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations 167-ai-mediated-representation-for-underrepresented-ex.md 25% - 0. Versioning Policy 24-12-versioning-policy.md 21% - AI-Coordinated Infrastructure for Distributed Expert Contribution 152-ai-coordinated-infrastructure-for-distributed-expe.md 53% - PORTAL-PROTOCOL.md v1.1 73-portal-protocol-md-v1-1.md 53% - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work 135-a-formal-model-for-human-ai-collaboration-in-distr.md 48% - 0.

## `docs/02-anthropic-vacancies/04-abstract.md`

_Abstract_

> The Nautilus Portal Protocol далее — NPP определяет способ федерации --- The Nautilus Portal Protocol далее — NPP определяет способ федерации независимых Git-репозиториев, содержащих знания в разных native-форматах, без их принудительного слияния в единую схему. --- --- Похожие документы: - 74-abstract 74-abstract.md сходство 0.43 --- Смотрите также: - 74-abstract 74-abstract.md - 98-appendix-a-minimal-working-example 98-appendix-a-minimal-working-example.md - 42-author-contact 42-author-contact.md - 65-readme-md 65-readme-md.md - 14. Passport passport.md 09-4-passport-passport-md.md - Abstract 74-abstract.md - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md - Appendix B: Change Log 34-appendix-b-change-log.md - For the Curious: Philosophy 44-for-the-curious-philosophy.md - For the Curious: Philosophy 54-for-the-curious-philosophy.md - Native Format 37-native-format.md - Native Format 47-native-format.md - Planned v0.2.0 132-planned-v0-2-0.md - README.md 65-readme-md.md - REVIEW METHODOLOGY.md 105-review-methodology-md.md - portal-mcp.py 123-portal-mcp-py.md - Вакансии Anthropic — Анализ по кластерам README.md - Инвертированный индекс ключевых слов ../KEYWORD INDEX.md - Подключение к Claude Desktop 127-подключение-к-claude-desktop.md - Что ты ВСЕГДА делаешь 360-что-ты-всегда-делаешь.md - ⬡ 69-section.md - Вакансии Anthropic — Анализ по кластерам ../README.md - portal-mcp.py 123-portal-mcp-py.md 37% - For the Curious: Philosophy 54-for-the-curious-philosophy.md 37% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 33% - For the Curious: Philosophy 44-for-the-curious-philosophy.md 33% - For the Curious: Philosophy 64-for-the-curious-philosophy.md 33% - Abstract 74-abstract.md 33% - REVIEW METHODOLOGY.md 105-review-methodology-md.md 29% - Индекс «Смотрите также» ../SEE ALSO.md 29% - Abstract 74-abstract.md 42% - portal-mcp.py 123-portal-mcp-py.md 33% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 33% - For the Curious: Philosophy 44-for-the-curious-philosophy.md 33% - For the Curious: Philosophy 54-for-the-curious-philosophy.md 33% - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md 33% - Planned v0.2.0 132-planned-v0-2-0.md 29% - 0.

## `docs/02-anthropic-vacancies/05-0-status-of-this-document.md`

_0. Status of This Document_

> Reference Implementation 25-13-reference-implementation.md 48% - Author & Contact 42-author-contact.md 48% - 18. Reference Implementation 93-18-reference-implementation.md 48% - Author & Contact 62-author-contact.md 42% - Content Overview 48-content-overview.md 33% - 12. Status of This Document 75-0-status-of-this-document.md 90% - Author & Contact 42-author-contact.md 53% - Author & Contact 62-author-contact.md 42% - 13.

## `docs/02-anthropic-vacancies/06-1-introduction.md`

_1. Introduction_

> Абстракт авто 🎯 Проблема: Design Goals Протокол спроектирован так, чтобы одновременно достичь: - Low barrier to entry: подключение существующего репо к федерации требует не больше 5 минут работы два файла 🔧 Подход: Homogenization: разные типы знаний методология, семантика, символизм принудительно приводятся к одной структуре, что уменьшает выразительность. 🏷️ Ключевые слова: introduction , goals , anthropic , vacancies , проекте , federation , merging , motivation - 1. Terminology #14-terminology Современные системы управления знаниями Notion, Obsidian, Roam, Logseq, --- Современные системы управления знаниями Notion, Obsidian, Roam, Logseq, Coda, Confluence требуют от пользователя миграции в их единый формат.

## `docs/02-anthropic-vacancies/07-2-terminology.md`

_2. Terminology_

> Repository-participant далее — Repo — Git-репозиторий, содержащий минимум nautilus ../docs/05-habr-projects/memory/memnet.md .json и passport.md в корне. Registry — файл nautilus ../docs/05-habr-projects/memory/memnet.md .json в корне Portal-репо, перечисляющий все Repos экосистемы с их метаданными. --- --- Похожие документы: - 77-2-terminology docs/02-anthropic-vacancies/77-2-terminology.md сходство 0.63 - 08-3-registry- nautilus ../docs/05-habr-projects/memory/memnet.md -json docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md сходство 0.16 - 67-о-проекте docs/02-anthropic-vacancies/67-о-проекте.md сходство 0.16 --- Смотрите также: - 77-2-terminology docs/02-anthropic-vacancies/77-2-terminology.md - 08-3-registry- nautilus ../docs/05-habr-projects/memory/memnet.md -json docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md - 67-о-проекте docs/02-anthropic-vacancies/67-о-проекте.md - 78-3-registry- nautilus ../docs/05-habr-projects/memory/memnet.md -json docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md

## `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md`

_3. Registry (`nautilus.json`)_

> Абстракт авто 🎯 Проблема: Registry nautilus.json 3-registry-nautilusjson - 3.1. 🔧 Подход: Validation Rules 35-validation-rules !IMPORTANT Ключевой документ для понимания архитектуры. 🏷️ Ключевые слова: registry , nautilus , fields , anthropic , vacancies , terminology , required , optional - 3.

## `docs/02-anthropic-vacancies/09-4-passport-passport-md.md`

_4. Passport (`passport.md`)_

> --- Похожие документы: - 79-4-passport-passport-md 79-4-passport-passport-md.md сходство 0.24 - 08-3-registry-nautilus-json 08-3-registry-nautilus-json.md сходство 0.10 --- Смотрите также: - 79-4-passport-passport-md 79-4-passport-passport-md.md - 28-appendix-a-minimal-working-example 28-appendix-a-minimal-working-example.md - 98-appendix-a-minimal-working-example 98-appendix-a-minimal-working-example.md - 41-compatibility-level 41-compatibility-level.md - 10. Compatibility Levels 17-5-compatibility-levels.md 21% - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md 33% - Compatibility Level 41-compatibility-level.md 29% - 4. QueryResult Structure 22-10-queryresult-structure.md 25% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 25% - History 63-history.md 25% - Abstract 04-abstract.md 21%

## `docs/02-anthropic-vacancies/103-appendix-b-change-log.md`

_Appendix B: Change Log_

> Q6 Space Normative 83-8-q6-space-normative.md - Appendix C: References 104-appendix-c-references.md - Вакансии Anthropic — Анализ по кластерам README.md - Доступные инструменты 128-доступные-инструменты.md - Вакансии Anthropic — Анализ по кластерам ../README.md - 14. SDK Contract Informative 89-14-sdk-contract-informative.md 29% - Доступные инструменты 128-доступные-инструменты.md 21% - 10. MCP Extension Informative 91-16-mcp-extension-informative.md 25% - Доступные инструменты 128-доступные-инструменты.md 21% - Appendix B: Change Log 34-appendix-b-change-log.md 21% - 6.

## `docs/02-anthropic-vacancies/104-appendix-c-references.md`

_Appendix C: References_

> Коммит с сообщением docs: add formal PORTAL-PROTOCOL.md v1.1 specification 4. Nautilus Portal as Reference Substrate 141-4-nautilus-portal-as-reference-substrate.md - Appendix B: Change Log 103-appendix-b-change-log.md - Appendix B: Change Log 34-appendix-b-change-log.md - For the Curious: Philosophy 64-for-the-curious-philosophy.md - References 147-references.md - Вакансии Anthropic — Анализ по кластерам README.md - Глоссарий 122-глоссарий.md - Доступные инструменты 128-доступные-инструменты.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL 02-общий-план-развития-nautilus-portal-protocol.md - ⬡ 69-section.md - 🇬🇧 About 68-about.md - 🇷🇺 О проекте 67-о-проекте.md - Вакансии Anthropic — Анализ по кластерам ../README.md - 18. Reference Implementation 25-13-reference-implementation.md 25% - Appendix B: Change Log 34-appendix-b-change-log.md 21% - ⬡ 69-section.md 21% - Appendix B: Change Log 103-appendix-b-change-log.md 17% - Глоссарий 122-глоссарий.md 17% - References 147-references.md 17% - For the Curious: Philosophy 64-for-the-curious-philosophy.md 17% - 18.

## `docs/02-anthropic-vacancies/105-review-methodology-md.md`

_REVIEW_METHODOLOGY.md_

> Статус: Активно применяется в проекте svend4/nautilus --- markdown markdown Дата: 2026-04 Статус: Активно применяется в проекте svend4/nautilus Автор: svend4 Licensing: CC BY 4.0 --- --- Похожие документы: - 03-portal-protocol-md 03-portal-protocol-md.md сходство 0.20 - 73-portal-protocol-md-v1-1 73-portal-protocol-md-v1-1.md сходство 0.17 - 229-профессиональные-коллеги-агенты 229-профессиональные-коллеги-агенты.md сходство 0.17 --- Смотрите также: - 28-appendix-a-minimal-working-example 28-appendix-a-minimal-working-example.md - 03-portal-protocol-md 03-portal-protocol-md.md - 42-author-contact 42-author-contact.md - 188-ai-опосредованное-представительство-для-недопредст 188-ai-опосредованное-представительство-для-недопредст.md - 10. Конкретный план применения к текущим документам 117-10-конкретный-план-применения-к-текущим-документам.md - 2. Связь с другими типами агентов 240-9-связь-с-другими-типами-агентов.md - AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения 188-ai-опосредованное-представительство-для-недопредст.md - Abstract 74-abstract.md - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md - Appendix B: Change Log 34-appendix-b-change-log.md - PORTAL-PROTOCOL.md v1.1 73-portal-protocol-md-v1-1.md - README-MCP.md— инструкция по установке 125-readme-mcp-md-инструкция-по-установке.md - README.md 65-readme-md.md - TL;DR 106-tl-dr.md - portal-mcp.py 123-portal-mcp-py.md - Аннотация 230-аннотация.md - Благодарности 301-благодарности.md - Вакансии Anthropic — Анализ по кластерам README.md - Глоссарий 122-глоссарий.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md - ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ 289-инфраструктура-для-ai-совместной-интеллектуальной-.md - ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ 229-профессиональные-коллеги-агенты.md - Содержание 190-содержание.md - Ссылки 245-ссылки.md - ⬡ 69-section.md - 🇷🇺 О проекте 67-о-проекте.md - Вакансии Anthropic — Анализ по кластерам ../README.md - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 42% - README.md 65-readme-md.md 37% - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md 37% - README-MCP.md— инструкция по установке 125-readme-mcp-md-инструкция-по-установке.md 33% - Abstract 04-abstract.md 29% - portal-mcp.py 123-portal-mcp-py.md 29% - For the Curious: Philosophy 64-for-the-curious-philosophy.md 29% - Содержание 190-содержание.md 25% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 37% - README-MCP.md— инструкция по установке 125-readme-mcp-md-инструкция-по-установке.md 33% - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md 33% - Глоссарий 122-глоссарий.md 29% - README.md 65-readme-md.md 29% - Abstract 04-abstract.md 25% - portal-mcp.py 123-portal-mcp-py.md 25% - Содержание 190-содержание.md 25%

## `docs/02-anthropic-vacancies/106-tl-dr.md`

_TL;DR_

> Вариант A создаётся независимо первым Claude-агентом ветка 1 2. Вариант B создаётся независимо вторым Claude-агентом ветка 2 3. Условия применимости 111-4-условия-применимости.md - Вакансии Anthropic — Анализ по кластерам README.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md - Критерии выбора для фазы 3 71-критерии-выбора-для-фазы-3.md - Вакансии Anthropic — Анализ по кластерам ../README.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md 33% - Расписание фазы 3 72-расписание-фазы-3.md 17% - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md 42% - REVIEW METHODOLOGY.md 105-review-methodology-md.md 17% - 2.

## `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md`

_1. Контекст и мотивация_

> ✅ Результат: Каждый запуск создаёт отдельную ветку, на которой агент работает независимо от других. Проект Nautilus разрабатывается в паре «автор + Claude Code агент». Каждый запуск создаёт отдельную ветку, на которой агент работает независимо от других.

## `docs/02-anthropic-vacancies/108-2-формальный-workflow.md`

_2. Формальный workflow_

> 🔧 Подход: Условия для применения методологии Методология применяется только к критически важным документам, где стоимость потери информации высока. 🏷️ Ключевые слова: применения , anthropic , vacancies , документам , nautilus , формальный , workflow , review - 2. Фаза A Фаза B Фаза C --- Методология применяется только к критически важным документам , где стоимость потери информации высока.

## `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md`

_3. Принципы консолидации (Фаза C)_

> Для каждого расхождения применяются правила #31-для-каждого-расхождения-применяются-правила - Native Format #native-format --- Абстракт авто 🎯 Проблема: Пример: - A: «88% fallback — критическая проблема, требует срочного решения» - B: «88% fallback — осмысленный tradeoff, приоритет средний» → В финальной версии обе позиции сохраняю 🔧 Подход: Если избегаете трёхфазного подхода, эти 10-15% теряются безвозвратно. ✅ Результат: Правило 5: Конфликтующие выводы Редкий, но важный случай: A и B приходят к противоположным выводам не числа расходятся, а интерпретация . --- Похожие документы: - 71-критерии-выбора-для-фазы-3 71-критерии-выбора-для-фазы-3.md сходство 0.21 --- Смотрите также: - 71-критерии-выбора-для-фазы-3 71-критерии-выбора-для-фазы-3.md - 107-1-контекст-и-мотивация 107-1-контекст-и-мотивация.md - 108-2-формальный-workflow 108-2-формальный-workflow.md - 82-7-portalentry-structure 82-7-portalentry-structure.md - 2.

## `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md`

_Вопрос: fallback-ratio как критический или осмысленный?_

> Абстракт авто 🎯 Проблема: Два независимых анализа пришли к разным выводам: - Позиция A: 88% fallback критично, требует срочных живых адаптеров для info1/pro2/meta/data2 - Позиция B: 88% fallback — осмысленн 🔧 Подход: !IMPORTANT Ключевой документ для понимания архитектуры. 🏷️ Ключевые слова: fallback , anthropic , vacancies , решение , проекта , версии , метрика , count !IMPORTANT Ключевой документ для понимания архитектуры. Два независимых анализа пришли к разным выводам: --- Два независимых анализа пришли к разным выводам: - Позиция A : 88% fallback критично, требует срочных живых адаптеров для info1 ../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md /pro2/meta/data2 - Позиция B : 88% fallback — осмысленное решение для early-stage проекта, приоритет средний Текущее решение автора : ваше решение + обоснование 1.

## `docs/02-anthropic-vacancies/111-4-условия-применимости.md`

_4. Условия применимости_

> 🔧 Подход: Когда оппонирует 43-когда-оппонирует Методология не универсальна. 🏷️ Ключевые слова: когда , применять , anthropic , vacancies , условия , применимости , формальный , workflow - 4. Она уместна при следующих условиях : --- Методология не универсальна.

## `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md`

_5. Связь с существующими методологиями_

> 🔧 Подход: Новое в данной методологии 55-новое-в-данной-методологии Теоретическим прародителем является N-version programming --- 5. 🏷️ Ключевые слова: version , programming , связь , существующими , методологиями , reviews , ensembles , отличия - 5. Отличия: - ML ensembles: разрешение автоматическое, по правилу - Наша методология: разрешение ручное, через правила 1-5 В security и public policy используется структура red vs blue : один агент критикует, другой защищает.

## `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md`

_6. Почему это валидный паттерн для AI-assisted workflows_

> Традиционная software engineering оптимизировалась против --- Традиционная software engineering оптимизировалась против дублирования кода и документации — это разумно, когда каждая работа стоит человеческих часов. ROI меняется в другую сторону : избыточность больше не люкс, а страховка. Старые правила «избегай дублирования» требуют переосмысления, когда unit cost меняется в 10-100 раз.

## `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md`

_7. Реализация в проекте Nautilus_

> Абстракт авто 🎯 Проблема: Реализация в проекте Nautilus Contents - 7. 🏷️ Ключевые слова: nautilus , применения , anthropic , vacancies , status , workflow , реализация , проекте - 7. Реализация в проекте Nautilus #7-реализация-в-проекте- nautilus ../docs/05-habr-projects/memory/memnet.md - 7.1.

## `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md`

_8. Ограничения и открытые вопросы_

> 🔧 Подход: Что делать, если ресурсов на Фазу C нет Если трёхфазная методология применена к документу, но времени на Фазу C нет и не предвидится в течение 2 недель : 1. Что делать, если ресурсов на Фазу C нет #83-что-делать-если-ресурсов-на-фазу-c-нет !WARNING Документ содержит описание рисков и ограничений. Если трёхфазная методология применена к документу, но времени на Фазу C нет и не предвидится в течение 2 недель : 1.

## `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md`

_9. Checklist применения методологии_

> Абстракт авто 🎯 Проблема: Checklist применения методологии Contents - 9. 🔧 Подход: Checklist применения методологии 9-checklist-применения-методологии - 9.1. ✅ Результат: Во время Фазы A и B - Агенты работают в разных ветках не в одной - Prompt'ы для A и B идентичны иначе это не независимое воспроизведение - Каждый агент не видит результат друго 🏷️ Ключевые слова: checklist , применения , методологии , перед , время , документ , началом , phase - 9.

## `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md`

_10. Конкретный план применения к текущим документам_

> Абстракт авто 🎯 Проблема: Конкретный план применения к текущим документам Contents - 10. 🔧 Подход: Будущие применения Планируемые кандидаты на трёхфазную методологию: - ARCHITECTURE.md если создаётся — формальное описание архитектуры - CONTRIBUTING.md если создаётся — guidel ✅ Результат: Провести верификацию конкретных метрик: Результат — вставить в финальный консолидированный документ вместо обоих вариантов. Конкретный план применения к текущим документам #10-конкретный-план-применения-к-текущим-документам - 10.1.

## `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md`

_Appendix B: Примеры расхождений и их разрешения_

> 🔧 Подход: Расхождение в концептуальных выводах Правило 5 Гипотетический пример: Разрешение: оба риска реальны, приоритезация зависит от цели проекта. ✅ Результат: Расхождение в концептуальных выводах Правило 5 Гипотетический пример: Разрешение: оба риска реальны, приоритезация зависит от цели проекта. Гипотетический пример : Разрешение : оба риска реальны, приоритезация зависит от цели проекта.

## `docs/02-anthropic-vacancies/12-content-overview.md`

_Content Overview_

> Что внутри: типы данных, приблизительный объём, основные темы. --- Что внутри: типы данных, приблизительный объём, основные темы. --- Похожие документы: - 31-content-overview 31-content-overview.md сходство 0.21 - 4.

## `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md`

_Appendix C: История изменений методологии_

> Первая формализация, основана на опыте применения к --- Первая формализация, основана на опыте применения к IMPLEMENTATION STAGE PART .md в апреле 2026. Будущие версии методологии будут задокументированы в этом appendix. Почему это валидный паттерн для AI-assisted workflows 113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md - Appendix A: Шаблон для header warning 118-appendix-a-шаблон-для-header-warning.md - Appendix B: Domain Comparison Matrix 185-appendix-b-domain-comparison-matrix.md - History 16-history.md - Вакансии Anthropic — Анализ по кластерам README.md - Главные технические риски 120-главные-технические-риски.md - Доступ к данным 102-доступ-к-данным.md - Когда ты Honestly не знаешь 361-когда-ты-honestly-не-знаешь.md - Кому ты служишь слоистая модель 348-кому-ты-служишь-слоистая-модель.md - Приложение A: Дерево Решений для Принимающих InGit 339-приложение-a-дерево-решений-для-принимающих-ingit.md - Приложение B: Матрица Сравнения Областей 206-приложение-b-матрица-сравнения-областей.md - Твои anti-patterns 359-твои-anti-patterns.md - Твоя миссия 347-твоя-миссия.md - Вакансии Anthropic — Анализ по кластерам ../README.md --- Смотрите также: - 102-доступ-к-данным 102-доступ-к-данным.md - 118-appendix-a-шаблон-для-header-warning 118-appendix-a-шаблон-для-header-warning.md - 339-приложение-a-дерево-решений-для-принимающих-ingit 339-приложение-a-дерево-решений-для-принимающих-ingit.md - 185-appendix-b-domain-comparison-matrix 185-appendix-b-domain-comparison-matrix.md - Доступ к данным 102-доступ-к-данным.md 60% - Приложение A: Дерево Решений для Принимающих InGit 339-приложение-a-дерево-решений-для-принимающих-ingit.md 60% - Кому ты служишь слоистая модель 348-кому-ты-служишь-слоистая-модель.md 53% - Appendix A: Шаблон для header warning 118-appendix-a-шаблон-для-header-warning.md 42% - Когда ты Honestly не знаешь 361-когда-ты-honestly-не-знаешь.md 42% - Appendix B: Domain Comparison Matrix 185-appendix-b-domain-comparison-matrix.md 29% - Твоя миссия 347-твоя-миссия.md 29% - Главные технические риски 120-главные-технические-риски.md 25% --- Похожие документы: - 102-доступ-к-данным docs/02-anthropic-vacancies/102-доступ-к-данным.md сходство 0.70 - 339-приложение-a-дерево-решений-для-принимающих-ingit docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md сходство 0.59 - 121-appendix-c-история-изменений-методологии docs/obsidian/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md сходство 0.58

## `docs/02-anthropic-vacancies/122-глоссарий.md`

_Глоссарий_

> ✅ Результат: IMPLEMENTATIONSTAGEPART1-4.md — технико-концептуальный review в transitional state, готовый к Фазе C После того, как PORTAL-PROTOCOL и REVIEWMETHODOLOGY скоммитятся в репо, у вас д 🏷️ Ключевые слова: review , portal , methodology , документ , appendix , nautilus , методология , protocol !WARNING Документ содержит описание рисков и ограничений. REVIEW METHODOLOGY.md — это ваш публичный тезис: «вот как мы работаем с AI, и это не хаос, а осмысленный инженерный процесс». REVIEW METHODOLOGY.md v1.0 — meta-документ о вашем workflow с AI-agents Плюс то, что уже в репо: 1.

## `docs/02-anthropic-vacancies/123-portal-mcp-py.md`

_portal-mcp.py_

> Абстракт авто 🎯 Проблема: portal-mcp.py !IMPORTANT Ключевой документ для понимания архитектуры. 🔧 Подход: portal-mcp.py !IMPORTANT Ключевой документ для понимания архитектуры. 🏷️ Ключевые слова: anthropic , vacancies , readme , appendix , minimal , working , example , portal !IMPORTANT Ключевой документ для понимания архитектуры.

## `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md`

_Конфигурация для Claude Desktop_

> После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигурации MCP. Путь зависит от ОС: --- После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигурации MCP. После сохранения конфигурации и перезапуска Claude Desktop в чате появится индикатор подключения MCP-сервера, и tools станут доступны для использования.

## `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md`

_README-MCP.md— инструкция по установке_

> Отдельный документ для репо, объясняющий, как настроить MCP-обёртку: --- Отдельный документ для репо, объясняющий, как настроить MCP-обёртку: markdown markdown Подключение Nautilus Portal к LLM-клиентам через Model Context Protocol MCP . --- Похожие документы: - 123-portal-mcp-py 123-portal-mcp-py.md сходство 0.21 - 03-portal-protocol-md 03-portal-protocol-md.md сходство 0.18 - 73-portal-protocol-md-v1-1 73-portal-protocol-md-v1-1.md сходство 0.16 --- Смотрите также: - 123-portal-mcp-py 123-portal-mcp-py.md - 105-review-methodology-md 105-review-methodology-md.md - 42-author-contact 42-author-contact.md - 65-readme-md 65-readme-md.md - Abstract 74-abstract.md - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md - Appendix B: Change Log 34-appendix-b-change-log.md - PORTAL-PROTOCOL.md v1.1 73-portal-protocol-md-v1-1.md - README.md 65-readme-md.md - REVIEW METHODOLOGY.md 105-review-methodology-md.md - References 320-references.md - portal-mcp.py 123-portal-mcp-py.md - Благодарности 203-благодарности.md - Вакансии Anthropic — Анализ по кластерам README.md - Глоссарий 122-глоссарий.md - Зачем две версии параллельно 70-зачем-две-версии-параллельно.md - Конфигурация для Claude Desktop 124-конфигурация-для-claude-desktop.md - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL 02-общий-план-развития-nautilus-portal-protocol.md - Отладка 130-отладка.md - Подключение к Claude Desktop 127-подключение-к-claude-desktop.md - Расписание фазы 3 72-расписание-фазы-3.md - Ссылки 338-ссылки.md - ⬡ 69-section.md - Вакансии Anthropic — Анализ по кластерам ../README.md - REVIEW METHODOLOGY.md 105-review-methodology-md.md 33% - README.md 65-readme-md.md 33% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 29% - Глоссарий 122-глоссарий.md 25% - portal-mcp.py 123-portal-mcp-py.md 25% - Appendix A: Minimal Working Example 98-appendix-a-minimal-working-example.md 25% - Abstract 04-abstract.md 21% - 0. Status of This Document 05-0-status-of-this-document.md 21% - REVIEW METHODOLOGY.md 105-review-methodology-md.md 33% - Глоссарий 122-глоссарий.md 33% - portal-mcp.py 123-portal-mcp-py.md 33% - README.md 65-readme-md.md 33% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 29% - Appendix B: Change Log 34-appendix-b-change-log.md 29% - 0.

## `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md`

_Подключение к Claude Desktop_

> --- Похожие документы: - 124-конфигурация-для-claude-desktop 124-конфигурация-для-claude-desktop.md сходство 0.23 - 130-отладка 130-отладка.md сходство 0.15 --- Смотрите также: - 124-конфигурация-для-claude-desktop 124-конфигурация-для-claude-desktop.md - 130-отладка 130-отладка.md - 28-appendix-a-minimal-working-example 28-appendix-a-minimal-working-example.md - 125-readme-mcp-md-инструкция-по-установке 125-readme-mcp-md-инструкция-по-установке.md - History 63-history.md - Planned v0.2.0 132-planned-v0-2-0.md - README.md 65-readme-md.md - portal-mcp.py 123-portal-mcp-py.md - Вакансии Anthropic — Анализ по кластерам README.md - Конфигурация для Claude Desktop 124-конфигурация-для-claude-desktop.md - Отладка 130-отладка.md - Что ты ВСЕГДА делаешь 360-что-ты-всегда-делаешь.md - Вакансии Anthropic — Анализ по кластерам ../README.md - portal-mcp.py 123-portal-mcp-py.md 33% - Compatibility Level 41-compatibility-level.md 29% - Table of Contents 154-table-of-contents.md 25% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 25% - Abstract 04-abstract.md 21% - 4. Passport passport.md 09-4-passport-passport-md.md 21% - Конфигурация для Claude Desktop 124-конфигурация-для-claude-desktop.md 21% - Отладка 130-отладка.md 21% - portal-mcp.py 123-portal-mcp-py.md 33% - Abstract 04-abstract.md 25% - Конфигурация для Claude Desktop 124-конфигурация-для-claude-desktop.md 25% - Отладка 130-отладка.md 25% - Содержание 190-содержание.md 25% - 10. QueryResult Structure 22-10-queryresult-structure.md 25% - Appendix A: Minimal Working Example 28-appendix-a-minimal-working-example.md 25% - Содержание 326-содержание.md 25%

## `docs/02-anthropic-vacancies/128-доступные-инструменты.md`

_Доступные инструменты_

> MCP Extension Informative 91-16-mcp-extension-informative.md - Appendix B: Change Log 103-appendix-b-change-log.md - Вакансии Anthropic — Анализ по кластерам README.md - Ограничения текущей версии 0.1.0-draft 131-ограничения-текущей-версии-0-1-0-draft.md - Примеры запросов в Claude 129-примеры-запросов-в-claude.md - Вакансии Anthropic — Анализ по кластерам ../README.md - 16. MCP Extension Informative 91-16-mcp-extension-informative.md 37% - Примеры запросов в Claude 129-примеры-запросов-в-claude.md 33% - Appendix B: Change Log 103-appendix-b-change-log.md 21% - Ограничения текущей версии 0.1.0-draft 131-ограничения-текущей-версии-0-1-0-draft.md 21% - 13. REST API Contract Normative for Portals 88-13-rest-api-contract-normative-for-portals.md 29% - Appendix B: Change Log 103-appendix-b-change-log.md 21% - 18.

## `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md`

_Примеры запросов (в Claude)_

> Status of This Document 05-0-status-of-this-document.md 25% - Ограничения текущей версии 0.1.0-draft 131-ограничения-текущей-версии-0-1-0-draft.md 21% - 18. Status of This Document 05-0-status-of-this-document.md 29% - Ограничения текущей версии 0.1.0-draft 131-ограничения-текущей-версии-0-1-0-draft.md 29% - Author & Contact 42-author-contact.md 25% - 0. Status of This Document 75-0-status-of-this-document.md 25% - 7.

## `docs/02-anthropic-vacancies/130-отладка.md`

_Отладка_

> Проверить логи Claude Desktop: - macOS: ~/Library/Logs/Claude/mcp .log - Windows: %APPDATA%\Claude\logs\mcp .log - Linux: ~/.config/Claude/logs/mcp .log 2. Проверить: Если portal тоже падает — проблема не в MCP, а в самом адаптере. Проверить синтаксис claude desktop config.json валидный JSON 2.

