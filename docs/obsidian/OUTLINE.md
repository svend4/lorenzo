---
title: "Outline базы знаний"
tags:
  - general
date: 2026-04-29
---

# Outline базы знаний

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> Секций: **10** | Файлов: **516**
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, Rufler, LiteParse, Legal RAG

---

<!-- toc -->
## Содержание

- [Содержание](#содержание)
- [📁 Docs (`docs/`)](#docs-docs)
  - [[[ABBREVIATIONS|Словарь аббревиатур и сокращений]]](#abbreviationsсловарь-аббревиатур-и-сокращений)
  - [[[ACTION_ITEMS|Action Items, риски и решения]]](#action_itemsaction-items-риски-и-решения)
  - [[[ALERTS|Callout-блоки]]](#alertscallout-блоки)
  - [[[AUTHORS|Авторы и коллаборации]]](#authorsавторы-и-коллаборации)
  - [[[AUTOFILLED|Автозаполненные шаблоны]]](#autofilledавтозаполненные-шаблоны)
  - [[[BACKLINKS|Индекс обратных ссылок]]](#backlinksиндекс-обратных-ссылок)
  - [[[CHANGELOG]]](#changelog)
  - [[[CHANGELOG_AUTO|Changelog (авто)]]](#changelog_autochangelog-авто)
  - [[[CLUSTERS|Кластеры тематически близких файлов]]](#clustersкластеры-тематически-близких-файлов)
  - [[[CODE_BLOCKS|Code-блоки репозитория]]](#code_blockscode-блоки-репозитория)
  - [[[COMPARE|Сравнение с предыдущим коммитом]]](#compareсравнение-с-предыдущим-коммитом)
  - [[[COMPLEXITY|Оценка читаемости документов]]](#complexityоценка-читаемости-документов)
  - [[[COMPONENT_MATRIX|Матрица компонентов Svyazi 2.0]]](#component_matrixматрица-компонентов-svyazi-20)
  - [[[CONCEPTS|Глоссарий понятий]]](#conceptsглоссарий-понятий)
  - [[[CONCEPT_GRAPH|Граф концептов базы знаний]]](#concept_graphграф-концептов-базы-знаний)
  - [[[CONSISTENCY|Согласованность терминов]]](#consistencyсогласованность-терминов)
  - [[[CONTACTS|Контакты и авторы]]](#contactsконтакты-и-авторы)
  - [[[CONTACT_PRIORITY|Приоритет контактов]]](#contact_priorityприоритет-контактов)
  - [[[CONTRADICTIONS|Противоречия в базе знаний]]](#contradictionsпротиворечия-в-базе-знаний)
  - [[[COST|Оценка стоимости MVP]]](#costоценка-стоимости-mvp)
  - [[[CROSSREFS|Перекрёстные ссылки]]](#crossrefsперекрёстные-ссылки)
  - [[[DECISIONS|Ключевые решения и выводы]]](#decisionsключевые-решения-и-выводы)
  - [[[DENSITY|Карта плотности тем]]](#densityкарта-плотности-тем)
  - [[[DEPENDABOT|Мониторинг зависимостей]]](#dependabotмониторинг-зависимостей)
  - [[[DEPENDENCY_MAP|Карта зависимостей скриптов]]](#dependency_mapкарта-зависимостей-скриптов)
  - [[[DIGEST|Дайджест изменений]]](#digestдайджест-изменений)
  - [[[DIGEST_WEEKLY|Еженедельный дайджест — 2026-04-29]]](#digest_weeklyеженедельный-дайджест-2026-04-29)
  - [[[DUPLICATES|Отчёт о дублировании]]](#duplicatesотчёт-о-дублировании)
  - [[[ENTITIES|Именованные сущности]]](#entitiesименованные-сущности)
  - [[[FAQ|Часто задаваемые вопросы (FAQ)]]](#faqчасто-задаваемые-вопросы-faq)
  - [[[FOOTNOTES|Сноски и определения терминов]]](#footnotesсноски-и-определения-терминов)
  - [[[GLOSSARY|Глоссарий проектов]]](#glossaryглоссарий-проектов)
  - [[[GRAPH|Граф связей проектов]]](#graphграф-связей-проектов)
  - [[[HEALTH|Health Dashboard]]](#healthhealth-dashboard)
  - [[[HEATMAP|Тепловая карта тем]]](#heatmapтепловая-карта-тем)
  - [[[INDEX|Индекс документации — Lorenzo / Svyazi 2.0]]](#indexиндекс-документации-lorenzo-svyazi-20)
  - [[[KEYWORD_INDEX|Инвертированный индекс ключевых слов]]](#keyword_indexинвертированный-индекс-ключевых-слов)
  - [[[KPI|Числовые KPI и метрики]]](#kpiчисловые-kpi-и-метрики)
  - [[[KPI_HISTORY|История метрик KPI]]](#kpi_historyистория-метрик-kpi)
  - [[[LINKS|Индекс ссылок]]](#linksиндекс-ссылок)
  - [[[LLM_SUMMARIES|AI-саммари разделов документации]]](#llm_summariesai-саммари-разделов-документации)
  - [[[METRICS|Метрики качества документации]]](#metricsметрики-качества-документации)
  - [[[MINDMAP|Майндмап репозитория Lorenzo]]](#mindmapмайндмап-репозитория-lorenzo)
  - [[[MISSING|Карта пробелов знаний]]](#missingкарта-пробелов-знаний)
  - [[[NAMED_ENTITIES|Индекс именованных сущностей]]](#named_entitiesиндекс-именованных-сущностей)
  - [[[NARRATIVE|Нарратив проекта Lorenzo]]](#narrativeнарратив-проекта-lorenzo)
  - [[[NETWORK|Сеть проектов и авторов]]](#networkсеть-проектов-и-авторов)
  - [[[ONBOARDING|Онбординг — Svyazi 2.0 / Lorenzo]]](#onboardingонбординг-svyazi-20-lorenzo)
  - [[[ORPHANS|Изолированные документы (Orphans)]]](#orphansизолированные-документы-orphans)
  - [[[PARAGRAPH_QUALITY|Качество абзацев]]](#paragraph_qualityкачество-абзацев)
  - [[[PRIORITIES|Приоритеты файлов]]](#prioritiesприоритеты-файлов)
  - [[[PROGRESS|Прогресс MVP]]](#progressпрогресс-mvp)
  - [[[QA|Глобальный Q&A]]](#qaглобальный-qa)
  - [[[QUESTIONS|Открытые вопросы]]](#questionsоткрытые-вопросы)
  - [[[READING_ORDER|Рекомендуемый порядок чтения]]](#reading_orderрекомендуемый-порядок-чтения)
  - [[[README|docs]]](#readmedocs)
  - [[[REPORT|Executive Report: Репозиторий Lorenzo]]](#reportexecutive-report-репозиторий-lorenzo)
  - [[[RISK_REGISTER|Реестр рисков — Svyazi 2.0]]](#risk_registerреестр-рисков-svyazi-20)
  - [[[SCHEDULE|Расписание проекта]]](#scheduleрасписание-проекта)
  - [[[SCORING|Оценка готовности проекта (Go/No-Go)]]](#scoringоценка-готовности-проекта-gono-go)
  - [[[SEE_ALSO|Индекс «Смотрите также»]]](#see_alsoиндекс-смотрите-также)
  - [[[SENTIMENT|Тональный анализ документов]]](#sentimentтональный-анализ-документов)
  - [[[SIMILAR|Похожие документы]]](#similarпохожие-документы)
  - [[[SITEMAP|Карта репозитория Lorenzo]]](#sitemapкарта-репозитория-lorenzo)
  - [[[SOURCE_MAP|Карта происхождения текстов]]](#source_mapкарта-происхождения-текстов)
  - [[[STATS|Детальная статистика репозитория]]](#statsдетальная-статистика-репозитория)
  - [[[TABLES|Все таблицы репозитория]]](#tablesвсе-таблицы-репозитория)
  - [[[TAGS|Индекс тегов]]](#tagsиндекс-тегов)
  - [[[TECH_RADAR|Tech Radar — Svyazi 2.0]]](#tech_radartech-radar-svyazi-20)
  - [[[TIMELINE|Хронология и временные маркеры]]](#timelineхронология-и-временные-маркеры)
  - [[[VALIDATION|Валидация структуры репозитория]]](#validationвалидация-структуры-репозитория)
  - [[[VOCABULARY|Богатство словаря документов]]](#vocabularyбогатство-словаря-документов)
  - [[[WORD_CLOUD|Word Cloud]]](#word_cloudword-cloud)
  - [[[WORD_FREQ|Частотный анализ слов]]](#word_freqчастотный-анализ-слов)
- [📁 Svyazi (`docs/01-svyazi/`)](#svyazi-docs01-svyazi)
  - [[[00-intro-part2|Продолжение исследования для Svyazi 2.0]]](#00-intro-part2продолжение-исследования-для-svyazi-20)
  - [[Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md)](#svyazisvyazi-20-исполнительное-резюмеdocs01-svyazi01-executive-summarymd)
  - [[[02-methodology|Методика и рамка отбора проектов]]](#02-methodologyметодика-и-рамка-отбора-проектов)
  - [[[03-component-catalog|Содержание]]](#03-component-catalogсодержание)
  - [[[04-ensembles-overview|Содержание]]](#04-ensembles-overviewсодержание)
  - [[[06-security-privacy|Содержание]]](#06-security-privacyсодержание)
  - [[[07-mvp-planning|Содержание]]](#07-mvp-planningсодержание)
  - [[[08-conclusions|Выводы]]](#08-conclusionsвыводы)
  - [[[09-architectural-gaps|Содержание]]](#09-architectural-gapsсодержание)
  - [[[10-second-order-ensembles|Содержание]]](#10-second-order-ensemblesсодержание)
  - [[[11-integration-contracts|Содержание]]](#11-integration-contractsсодержание)
  - [[[12-roadmap|Содержание]]](#12-roadmapсодержание)
  - [[[13-contacts|Содержание]]](#13-contactsсодержание)
  - [[[14-limitations|Содержание]]](#14-limitationsсодержание)
  - [[[QA|Q&A: 01-svyazi]]](#qaqa-01-svyazi)
  - [[Svyazi[^svyazi] 2.0 — Архитектура и исследование](docs/01-svyazi/README.md)](#svyazisvyazi-20-архитектура-и-исследованиеdocs01-svyazireadmemd)
- [📁 Anthropic Vacancies (`docs/02-anthropic-vacancies/`)](#anthropic-vacancies-docs02-anthropic-vacancies)
  - [[[00-intro|Введение]]](#00-introвведение)
  - [[[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]]](#01-интегральный-анализ-профиля-svend4интегральный-анализ-профиля-svend4)
  - [[[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]]](#02-общий-план-развития-nautilus-portal-protocolобщий-план-развития-nautilus-portal-protocol)
  - [[[03-portal-protocol-md|PORTAL-PROTOCOL.md]]](#03-portal-protocol-mdportal-protocolmd)
  - [[[04-abstract|Abstract]]](#04-abstractabstract)
  - [[[05-0-status-of-this-document|0. Status of This Document]]](#05-0-status-of-this-document0-status-of-this-document)
  - [[[06-1-introduction|1. Introduction]]](#06-1-introduction1-introduction)
  - [[[07-2-terminology|2. Terminology]]](#07-2-terminology2-terminology)
  - [[[08-3-registry-nautilus-json|3. Registry (nautilus.json)]]](#08-3-registry-nautilus-json3-registry-nautilusjson)
  - [[[09-4-passport-passport-md|4. Passport (passport.md)]]](#09-4-passport-passport-md4-passport-passportmd)
  - [[[102-доступ-к-данным|Доступ к данным]]](#102-доступ-к-даннымдоступ-к-данным)
  - [[[103-appendix-b-change-log|Appendix B: Change Log]]](#103-appendix-b-change-logappendix-b-change-log)
  - [[[104-appendix-c-references|Appendix C: References]]](#104-appendix-c-referencesappendix-c-references)
  - [[[105-review-methodology-md|REVIEWMETHODOLOGY.md]]](#105-review-methodology-mdreviewmethodologymd)
  - [[[106-tl-dr|TL;DR]]](#106-tl-drtldr)
  - [[[107-1-контекст-и-мотивация|1. Контекст и мотивация]]](#107-1-контекст-и-мотивация1-контекст-и-мотивация)
  - [[[108-2-формальный-workflow|2. Формальный workflow]]](#108-2-формальный-workflow2-формальный-workflow)
  - [[[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]]](#109-3-принципы-консолидации-фаза-c3-принципы-консолидации-фаза-c)
  - [[[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или осмысленный?]]](#110-вопрос-fallback-ratio-как-критический-или-осмысленвопрос-fallback-ratio-как-критический-или-осмысленный)
  - [[[111-4-условия-применимости|4. Условия применимости]]](#111-4-условия-применимости4-условия-применимости)
  - [[[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]]](#112-5-связь-с-существующими-методологиями5-связь-с-существующими-методологиями)
  - [[[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assisted workflows]]](#113-6-почему-это-валидный-паттерн-для-ai-assisted-work6-почему-это-валидный-паттерн-для-ai-assisted-workflows)
  - [[[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]]](#114-7-реализация-в-проекте-nautilus7-реализация-в-проекте-nautilus)
  - [[[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]]](#115-8-ограничения-и-открытые-вопросы8-ограничения-и-открытые-вопросы)
  - [[[116-9-checklist-применения-методологии|9. Checklist применения методологии]]](#116-9-checklist-применения-методологии9-checklist-применения-методологии)
  - [[[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим документам]]](#117-10-конкретный-план-применения-к-текущим-документам10-конкретный-план-применения-к-текущим-документам)
  - [[[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]]](#118-appendix-a-шаблон-для-header-warningappendix-a-шаблон-для-header-warning)
  - [[[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешения]]](#119-appendix-b-примеры-расхождений-и-их-разрешенияappendix-b-примеры-расхождений-и-их-разрешения)
  - [[[12-content-overview|Content Overview]]](#12-content-overviewcontent-overview)
  - [[[120-главные-технические-риски|Главные технические риски]]](#120-главные-технические-рискиглавные-технические-риски)
  - [[[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]]](#121-appendix-c-история-изменений-методологииappendix-c-история-изменений-методологии)
  - [[[122-глоссарий|Глоссарий]]](#122-глоссарийглоссарий)
  - [[[123-portal-mcp-py|portal-mcp.py]]](#123-portal-mcp-pyportal-mcppy)
  - [[[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]]](#124-конфигурация-для-claude-desktopконфигурация-для-claude-desktop)
  - [[[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]]](#125-readme-mcp-md-инструкция-по-установкеreadme-mcpmd-инструкция-по-установке)
  - [[[126-установка|Установка]]](#126-установкаустановка)
  - [[[127-подключение-к-claude-desktop|Подключение к Claude Desktop]]](#127-подключение-к-claude-desktopподключение-к-claude-desktop)
  - [[[128-доступные-инструменты|Доступные инструменты]]](#128-доступные-инструментыдоступные-инструменты)
  - [[[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]]](#129-примеры-запросов-в-claudeпримеры-запросов-в-claude)
  - [[[13-angle-perspective|Angle / Perspective]]](#13-angle-perspectiveangle-perspective)
  - [[[130-отладка|Отладка]]](#130-отладкаотладка)
  - [[[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]]](#131-ограничения-текущей-версии-0-1-0-draftограничения-текущей-версии-010-draft)
  - [[[132-planned-v0-2-0|Planned (v0.2.0)]]](#132-planned-v0-2-0planned-v020)
  - [[[133-обратная-связь|Обратная связь]]](#133-обратная-связьобратная-связь)
  - [[[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]]](#134-the-double-triangle-architecture-mdthe-double-triangle-architecturemd)
  - [[[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in Distributed Knowledge Work]]](#135-a-formal-model-for-human-ai-collaboration-in-distra-formal-model-for-human-ai-collaboration-in-distributed-knowledge-work)
  - [[[136-abstract|Abstract]]](#136-abstractabstract)
  - [[[137-table-of-contents|Table of Contents]]](#137-table-of-contentstable-of-contents)
  - [[[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]]](#138-1-why-single-triangle-models-are-incomplete1-why-single-triangle-models-are-incomplete)
  - [[[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]]](#139-2-the-double-triangle-architecture2-the-double-triangle-architecture)
  - [[[140-3-three-inter-layer-protocols|3. Three Inter-Layer Protocols]]](#140-3-three-inter-layer-protocols3-three-inter-layer-protocols)
  - [[[141-4-nautilus-portal-as-reference-substrate|4. Nautilus Portal as Reference Substrate]]](#141-4-nautilus-portal-as-reference-substrate4-nautilus-portal-as-reference-substrate)
  - [[[142-5-pattern-library-as-bridge-between-triangles|5. Pattern Library as Bridge Between Triangles]]](#142-5-pattern-library-as-bridge-between-triangles5-pattern-library-as-bridge-between-triangles)
  - [[[143-6-four-deployment-domains|6. Four Deployment Domains]]](#143-6-four-deployment-domains6-four-deployment-domains)
  - [[[144-7-open-questions|7. Open Questions]]](#144-7-open-questions7-open-questions)
  - [[[145-8-call-to-action|8. Call to Action]]](#145-8-call-to-action8-call-to-action)
  - [[[146-acknowledgments|Acknowledgments]]](#146-acknowledgmentsacknowledgments)
  - [[[147-references|References]]](#147-referencesreferences)
  - [[[148-appendix-a-glossary|Appendix A: Glossary]]](#148-appendix-a-glossaryappendix-a-glossary)
  - [[[149-appendix-b-summary-of-contributions|Appendix B: Summary of Contributions]]](#149-appendix-b-summary-of-contributionsappendix-b-summary-of-contributions)
  - [[[150-appendix-c-version-history|Appendix C: Version History]]](#150-appendix-c-version-historyappendix-c-version-history)
  - [[[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]]](#151-open-knowledge-work-foundation-mdopen-knowledge-work-foundationmd)
  - [[[152-ai-coordinated-infrastructure-for-distributed-expe|AI-Coordinated Infrastructure for Distributed Expert Contribution]]](#152-ai-coordinated-infrastructure-for-distributed-expeai-coordinated-infrastructure-for-distributed-expert-contribution)
  - [[[153-executive-summary|Executive Summary]]](#153-executive-summaryexecutive-summary)
  - [[[154-table-of-contents|Table of Contents]]](#154-table-of-contentstable-of-contents)
  - [[[155-1-problem-statement|1. Problem Statement]]](#155-1-problem-statement1-problem-statement)
  - [[[156-2-target-populations|2. Target Populations]]](#156-2-target-populations2-target-populations)
  - [[[157-3-why-existing-solutions-fail|3. Why Existing Solutions Fail]]](#157-3-why-existing-solutions-fail3-why-existing-solutions-fail)
  - [[[158-4-proposed-infrastructure|4. Proposed Infrastructure]]](#158-4-proposed-infrastructure4-proposed-infrastructure)
  - [[[159-5-economic-model|5. Economic Model]]](#159-5-economic-model5-economic-model)
  - [[[16-history|History]]](#16-historyhistory)
  - [[[160-6-governance-and-ethics|6. Governance and Ethics]]](#160-6-governance-and-ethics6-governance-and-ethics)
  - [[[161-7-phased-rollout-plan|7. Phased Rollout Plan]]](#161-7-phased-rollout-plan7-phased-rollout-plan)
  - [[[162-8-risk-analysis|8. Risk Analysis]]](#162-8-risk-analysis8-risk-analysis)
  - [[[163-9-call-for-partnership|9. Call for Partnership]]](#163-9-call-for-partnership9-call-for-partnership)
  - [[[164-10-appendices|10. Appendices]]](#164-10-appendices10-appendices)
  - [[[165-closing|Closing]]](#165-closingclosing)
  - [[[166-representative-agent-layer-md|REPRESENTATIVE AGENT LAYER.md]]](#166-representative-agent-layer-mdrepresentative-agent-layermd)
  - [[[167-ai-mediated-representation-for-underrepresented-ex|AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]](#167-ai-mediated-representation-for-underrepresented-exai-mediated-representation-for-underrepresented-experts-and-vulnerable-populations)
  - [[[168-abstract|Abstract]]](#168-abstractabstract)
  - [[[169-table-of-contents|Table of Contents]]](#169-table-of-contentstable-of-contents)
  - [[[17-5-compatibility-levels|5. Compatibility Levels]]](#17-5-compatibility-levels5-compatibility-levels)
  - [[[170-1-the-cinderella-syndrome-why-quality-stays-invisi|1. The Cinderella Syndrome: Why Quality Stays Invisible]]](#170-1-the-cinderella-syndrome-why-quality-stays-invisi1-the-cinderella-syndrome-why-quality-stays-invisible)
  - [[[171-2-historical-precedents-agents-as-civilizational-i|2. Historical Precedents: Agents as Civilizational Innovation]]](#171-2-historical-precedents-agents-as-civilizational-i2-historical-precedents-agents-as-civilizational-innovation)
  - [[[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]]](#172-3-what-makes-a-representative-agent3-what-makes-a-representative-agent)
  - [[[173-4-ten-domains-of-application|4. Ten Domains of Application]]](#173-4-ten-domains-of-application4-ten-domains-of-application)
  - [[[174-5-architectural-specification|5. Architectural Specification]]](#174-5-architectural-specification5-architectural-specification)
  - [[[175-6-ethical-framework|6. Ethical Framework]]](#175-6-ethical-framework6-ethical-framework)
  - [[[176-7-governance-and-oversight|7. Governance and Oversight]]](#176-7-governance-and-oversight7-governance-and-oversight)
  - [[[177-8-risks-and-mitigations|8. Risks and Mitigations]]](#177-8-risks-and-mitigations8-risks-and-mitigations)
  - [[[178-9-phased-rollout-strategy|9. Phased Rollout Strategy]]](#178-9-phased-rollout-strategy9-phased-rollout-strategy)
  - [[[179-10-open-questions|10. Open Questions]]](#179-10-open-questions10-open-questions)
  - [[[18-6-adapter-interface|6. Adapter Interface]]](#18-6-adapter-interface6-adapter-interface)
  - [[[180-11-call-for-collaboration|11. Call for Collaboration]]](#180-11-call-for-collaboration11-call-for-collaboration)
  - [[[181-12-closing|12. Closing]]](#181-12-closing12-closing)
  - [[[182-acknowledgments|Acknowledgments]]](#182-acknowledgmentsacknowledgments)
  - [[[183-references|References]]](#183-referencesreferences)
  - [[[184-appendix-a-connection-to-companion-papers|Appendix A: Connection to Companion Papers]]](#184-appendix-a-connection-to-companion-papersappendix-a-connection-to-companion-papers)
  - [[[185-appendix-b-domain-comparison-matrix|Appendix B: Domain Comparison Matrix]]](#185-appendix-b-domain-comparison-matrixappendix-b-domain-comparison-matrix)
  - [[[186-appendix-c-sample-use-cases-in-detail|Appendix C: Sample Use Cases in Detail]]](#186-appendix-c-sample-use-cases-in-detailappendix-c-sample-use-cases-in-detail)
  - [[[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]]](#187-слой-представительских-агентов-mdслой-представительских-агентовmd)
  - [[[188-ai-опосредованное-представительство-для-недопредст|AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения]]](#188-ai-опосредованное-представительство-для-недопредстai-опосредованное-представительство-для-недопредставленных-экспертов-и-уязвимых-категорий-населения)
  - [[[189-аннотация|Аннотация]]](#189-аннотацияаннотация)
  - [[[19-7-portalentry-structure|7. PortalEntry Structure]]](#19-7-portalentry-structure7-portalentry-structure)
  - [[[190-содержание|Содержание]]](#190-содержаниесодержание)
  - [[[191-1-синдром-золушки-почему-качество-остаётся-невидим|1. Синдром Золушки: Почему качество остаётся невидимым]]](#191-1-синдром-золушки-почему-качество-остаётся-невидим1-синдром-золушки-почему-качество-остаётся-невидимым)
  - [[[192-2-исторические-прецеденты-агенты-как-цивилизационн|2. Исторические прецеденты: Агенты как цивилизационная инновация]]](#192-2-исторические-прецеденты-агенты-как-цивилизационн2-исторические-прецеденты-агенты-как-цивилизационная-инновация)
  - [[[193-3-что-делает-агента-представительским|3. Что делает агента Представительским]]](#193-3-что-делает-агента-представительским3-что-делает-агента-представительским)
  - [[[194-4-десять-областей-применения|4. Десять областей применения]]](#194-4-десять-областей-применения4-десять-областей-применения)
  - [[[195-5-архитектурная-спецификация|5. Архитектурная спецификация]]](#195-5-архитектурная-спецификация5-архитектурная-спецификация)
  - [[[196-6-этическая-рамка|6. Этическая рамка]]](#196-6-этическая-рамка6-этическая-рамка)
  - [[[197-7-управление-и-надзор|7. Управление и надзор]]](#197-7-управление-и-надзор7-управление-и-надзор)
  - [[[198-8-риски-и-меры-противодействия|8. Риски и меры противодействия]]](#198-8-риски-и-меры-противодействия8-риски-и-меры-противодействия)
  - [[[199-9-стратегия-поэтапного-развёртывания|9. Стратегия поэтапного развёртывания]]](#199-9-стратегия-поэтапного-развёртывания9-стратегия-поэтапного-развёртывания)
  - [[[20-8-consensus-algorithm|8. Consensus Algorithm]]](#20-8-consensus-algorithm8-consensus-algorithm)
  - [[[200-10-открытые-вопросы|10. Открытые вопросы]]](#200-10-открытые-вопросы10-открытые-вопросы)
  - [[[201-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]]](#201-11-призыв-к-сотрудничеству11-призыв-к-сотрудничеству)
  - [[[202-12-заключение|12. Заключение]]](#202-12-заключение12-заключение)
  - [[[203-благодарности|Благодарности]]](#203-благодарностиблагодарности)
  - [[[204-ссылки|Ссылки]]](#204-ссылкиссылки)
  - [[[205-приложение-a-связь-с-сопроводительными-статьями|Приложение A: Связь с Сопроводительными Статьями]]](#205-приложение-a-связь-с-сопроводительными-статьямиприложение-a-связь-с-сопроводительными-статьями)
  - [[[206-приложение-b-матрица-сравнения-областей|Приложение B: Матрица Сравнения Областей]]](#206-приложение-b-матрица-сравнения-областейприложение-b-матрица-сравнения-областей)
  - [[[207-приложение-c-образцы-случаев-использования-в-детал|Приложение C: Образцы Случаев Использования в Деталях]]](#207-приложение-c-образцы-случаев-использования-в-деталприложение-c-образцы-случаев-использования-в-деталях)
  - [[[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]]](#208-professional-colleague-agents-mdprofessional-colleague-agentsmd)
  - [[[209-a-typology-of-ai-agents-on-the-principal-side-and-|A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers]]](#209-a-typology-of-ai-agents-on-the-principal-side-and-a-typology-of-ai-agents-on-the-principal-side-and-the-case-for-profession-specific-co-workers)
  - [[[21-9-query-flow|9. Query Flow]]](#21-9-query-flow9-query-flow)
  - [[[210-abstract|Abstract]]](#210-abstractabstract)
  - [[[211-table-of-contents|Table of Contents]]](#211-table-of-contentstable-of-contents)
  - [[[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]]](#212-1-the-five-type-typology-of-principal-side-agents1-the-five-type-typology-of-principal-side-agents)
  - [[[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]]](#213-2-what-makes-a-professional-colleague-agent2-what-makes-a-professional-colleague-agent)
  - [[[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]]](#214-3-empirical-case-study-обучай3-empirical-case-study-обучай)
  - [[[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Agents]]](#215-4-architecture-of-professional-colleague-agents4-architecture-of-professional-colleague-agents)
  - [[[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replication]]](#216-5-the-economics-of-profession-wide-replication5-the-economics-of-profession-wide-replication)
  - [[[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]]](#217-6-risks-specific-to-this-category6-risks-specific-to-this-category)
  - [[[218-7-application-domains|7. Application Domains]]](#218-7-application-domains7-application-domains)
  - [[[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]]](#219-8-pilot-proposal-sgb-advocate-colleague8-pilot-proposal-sgb-advocate-colleague)
  - [[[22-10-queryresult-structure|10. QueryResult Structure]]](#22-10-queryresult-structure10-queryresult-structure)
  - [[[220-9-relationship-to-other-agent-types|9. Relationship to Other Agent Types]]](#220-9-relationship-to-other-agent-types9-relationship-to-other-agent-types)
  - [[[221-10-open-questions|10. Open Questions]]](#221-10-open-questions10-open-questions)
  - [[[222-11-call-for-collaboration|11. Call for Collaboration]]](#222-11-call-for-collaboration11-call-for-collaboration)
  - [[[223-12-closing|12. Closing]]](#223-12-closing12-closing)
  - [[[224-acknowledgments|Acknowledgments]]](#224-acknowledgmentsacknowledgments)
  - [[[225-references|References]]](#225-referencesreferences)
  - [[[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Types]]](#226-appendix-a-comparative-table-five-agent-typesappendix-a-comparative-table-five-agent-types)
  - [[[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Build Type 1 First]]](#227-appendix-b-decision-framework-when-to-build-type-1appendix-b-decision-framework-when-to-build-type-1-first)
  - [[[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]]](#228-appendix-c-quick-start-architecture-for-sgb-advocaappendix-c-quick-start-architecture-for-sgb-advocate-colleague)
  - [[[229-профессиональные-коллеги-агенты|ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ]]](#229-профессиональные-коллеги-агентыпрофессиональные-коллеги-агенты)
  - [[[23-11-security-considerations|11. Security Considerations]]](#23-11-security-considerations11-security-considerations)
  - [[[230-аннотация|Аннотация]]](#230-аннотацияаннотация)
  - [[[231-содержание|Содержание]]](#231-содержаниесодержание)
  - [[[232-1-типология-из-пяти-типов-агентов-на-стороне-принц|1. Типология из пяти типов агентов на стороне принципала]]](#232-1-типология-из-пяти-типов-агентов-на-стороне-принц1-типология-из-пяти-типов-агентов-на-стороне-принципала)
  - [[[233-2-что-делает-агента-профессиональным-коллегой|2. Что делает агента Профессиональным Коллегой]]](#233-2-что-делает-агента-профессиональным-коллегой2-что-делает-агента-профессиональным-коллегой)
  - [[[234-3-эмпирический-кейс-обучай|3. Эмпирический кейс: «Обучай»]]](#234-3-эмпирический-кейс-обучай3-эмпирический-кейс-обучай)
  - [[[235-4-архитектура-профессиональных-коллег-агентов|4. Архитектура Профессиональных Коллег-Агентов]]](#235-4-архитектура-профессиональных-коллег-агентов4-архитектура-профессиональных-коллег-агентов)
  - [[[236-5-экономика-тиражирования-по-профессии|5. Экономика тиражирования по профессии]]](#236-5-экономика-тиражирования-по-профессии5-экономика-тиражирования-по-профессии)
  - [[[237-6-риски-специфичные-для-этой-категории|6. Риски, специфичные для этой категории]]](#237-6-риски-специфичные-для-этой-категории6-риски-специфичные-для-этой-категории)
  - [[[238-7-области-применения|7. Области применения]]](#238-7-области-применения7-области-применения)
  - [[[239-8-пилотное-предложение-sgb-колega-адвокат|8. Пилотное предложение: SGB Колega-Адвокат]]](#239-8-пилотное-предложение-sgb-колega-адвокат8-пилотное-предложение-sgb-колega-адвокат)
  - [[[24-12-versioning-policy|12. Versioning Policy]]](#24-12-versioning-policy12-versioning-policy)
  - [[[240-9-связь-с-другими-типами-агентов|9. Связь с другими типами агентов]]](#240-9-связь-с-другими-типами-агентов9-связь-с-другими-типами-агентов)
  - [[[241-10-открытые-вопросы|10. Открытые вопросы]]](#241-10-открытые-вопросы10-открытые-вопросы)
  - [[[242-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]]](#242-11-призыв-к-сотрудничеству11-призыв-к-сотрудничеству)
  - [[[243-12-заключение|12. Заключение]]](#243-12-заключение12-заключение)
  - [[[244-благодарности|Благодарности]]](#244-благодарностиблагодарности)
  - [[[245-ссылки|Ссылки]]](#245-ссылкиссылки)
  - [[[246-приложение-a-сравнительная-таблица-пять-типов-аген|Приложение A: Сравнительная Таблица — Пять Типов Агентов]]](#246-приложение-a-сравнительная-таблица-пять-типов-агенприложение-a-сравнительная-таблица-пять-типов-агентов)
  - [[[247-приложение-b-рамка-принятия-решений-когда-строить-|Приложение B: Рамка принятия решений — когда строить Тип 1 первым]]](#247-приложение-b-рамка-принятия-решений-когда-строить-приложение-b-рамка-принятия-решений-когда-строить-тип-1-первым)
  - [[[248-приложение-c-архитектура-быстрого-старта-для-sgb-а|Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги]]](#248-приложение-c-архитектура-быстрого-старта-для-sgb-априложение-c-архитектура-быстрого-старта-для-sgb-адвоката-коллеги)
  - [[[249-composite-skills-agent-md|COMPOSITE SKILLS AGENT.md]]](#249-composite-skills-agent-mdcomposite-skills-agentmd)
  - [[[25-13-reference-implementation|13. Reference Implementation]]](#25-13-reference-implementation13-reference-implementation)
  - [[[250-bridging-the-gap-between-profession-wide-and-indiv|Bridging the Gap Between Profession-Wide and Individual-Unique]]](#250-bridging-the-gap-between-profession-wide-and-indivbridging-the-gap-between-profession-wide-and-individual-unique)
  - [[[251-ai-support-through-configurable-specialist-ensembl|AI Support Through Configurable Specialist Ensembles]]](#251-ai-support-through-configurable-specialist-ensemblai-support-through-configurable-specialist-ensembles)
  - [[[252-abstract|Abstract]]](#252-abstractabstract)
  - [[[253-table-of-contents|Table of Contents]]](#253-table-of-contentstable-of-contents)
  - [[[254-1-why-the-binary-view-is-incomplete|1. Why the Binary View Is Incomplete]]](#254-1-why-the-binary-view-is-incomplete1-why-the-binary-view-is-incomplete)
  - [[[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]]](#255-2-the-twenty-one-teachers-pattern2-the-twenty-one-teachers-pattern)
  - [[[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]]](#256-3-what-makes-a-composite-skills-agent3-what-makes-a-composite-skills-agent)
  - [[[257-4-the-sub-agent-registry|4. The Sub-Agent Registry]]](#257-4-the-sub-agent-registry4-the-sub-agent-registry)
  - [[[258-5-configuration-how-principals-build-their-ensembl|5. Configuration: How Principals Build Their Ensembles]]](#258-5-configuration-how-principals-build-their-ensembl5-configuration-how-principals-build-their-ensembles)
  - [[[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]]](#259-6-coordination-and-disagreement-resolution6-coordination-and-disagreement-resolution)
  - [[[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]](#26-14-adr-001-federation-over-merging14-adr-001-federation-over-merging)
  - [[[260-7-economics-of-combinatorial-replication|7. Economics of Combinatorial Replication]]](#260-7-economics-of-combinatorial-replication7-economics-of-combinatorial-replication)
  - [[[261-8-seven-domains-of-application|8. Seven Domains of Application]]](#261-8-seven-domains-of-application8-seven-domains-of-application)
  - [[[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]]](#262-9-integration-with-okwf-infrastructure9-integration-with-okwf-infrastructure)
  - [[[263-10-risks-specific-to-composite-architectures|10. Risks Specific to Composite Architectures]]](#263-10-risks-specific-to-composite-architectures10-risks-specific-to-composite-architectures)
  - [[[264-11-open-questions|11. Open Questions]]](#264-11-open-questions11-open-questions)
  - [[[265-12-call-for-collaboration|12. Call for Collaboration]]](#265-12-call-for-collaboration12-call-for-collaboration)
  - [[[266-13-closing|13. Closing]]](#266-13-closing13-closing)
  - [[[267-acknowledgments|Acknowledgments]]](#267-acknowledgmentsacknowledgments)
  - [[[268-references|References]]](#268-referencesreferences)
  - [[[269-appendix-a-the-six-type-taxonomy-updated|Appendix A: The Six-Type Taxonomy (Updated)]]](#269-appendix-a-the-six-type-taxonomy-updatedappendix-a-the-six-type-taxonomy-updated)
  - [[[27-15-glossary-of-examples|15. Glossary of Examples]]](#27-15-glossary-of-examples15-glossary-of-examples)
  - [[[270-appendix-b-sub-agent-registry-schema-sketch|Appendix B: Sub-Agent Registry Schema (Sketch)]]](#270-appendix-b-sub-agent-registry-schema-sketchappendix-b-sub-agent-registry-schema-sketch)
  - [[[271-appendix-c-configuration-template-example|Appendix C: Configuration Template Example]]](#271-appendix-c-configuration-template-exampleappendix-c-configuration-template-example)
  - [[[272-appendix-d-connection-diagram|Appendix D: Connection Diagram]]](#272-appendix-d-connection-diagramappendix-d-connection-diagram)
  - [[[273-infrastructure-for-ai-collaborative-intellectual-w|INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md]]](#273-infrastructure-for-ai-collaborative-intellectual-winfrastructure-for-ai-collaborative-intellectual-workmd)
  - [[[274-the-missing-middle-layer-between-chat-and-code|The Missing Middle Layer Between Chat and Code]]](#274-the-missing-middle-layer-between-chat-and-codethe-missing-middle-layer-between-chat-and-code)
  - [[[275-why-this-document-exists|Why This Document Exists]]](#275-why-this-document-existswhy-this-document-exists)
  - [[[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]]](#276-the-two-layer-stack-as-it-existsthe-two-layer-stack-as-it-exists)
  - [[[277-what-s-missing-layer-b|What's Missing — Layer B]]](#277-what-s-missing-layer-bwhats-missing-layer-b)
  - [[[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]]](#278-why-this-hasn-t-been-builtwhy-this-hasnt-been-built)
  - [[[279-existing-approximations|Existing Approximations]]](#279-existing-approximationsexisting-approximations)
  - [[[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]](#28-appendix-a-minimal-working-exampleappendix-a-minimal-working-example)
  - [[[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]]](#280-the-specific-case-in-front-of-usthe-specific-case-in-front-of-us)
  - [[[281-the-recursive-insight|The Recursive Insight]]](#281-the-recursive-insightthe-recursive-insight)
  - [[[282-what-industry-will-likely-build|What Industry Will Likely Build]]](#282-what-industry-will-likely-buildwhat-industry-will-likely-build)
  - [[[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]]](#283-what-this-document-doesn-t-solvewhat-this-document-doesnt-solve)
  - [[[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]]](#284-practical-recommendations-for-the-current-projectpractical-recommendations-for-the-current-project)
  - [[[285-closing|Closing]]](#285-closingclosing)
  - [[[286-acknowledgments|Acknowledgments]]](#286-acknowledgmentsacknowledgments)
  - [[[287-references|References]]](#287-referencesreferences)
  - [[[288-appendix-position-in-series-visualization|Appendix: Position in Series Visualization]]](#288-appendix-position-in-series-visualizationappendix-position-in-series-visualization)
  - [[[289-инфраструктура-для-ai-совместной-интеллектуальной-|ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ]]](#289-инфраструктура-для-ai-совместной-интеллектуальной-инфраструктура-для-ai-совместной-интеллектуальной-работы)
  - [[[290-почему-этот-документ-существует|Почему этот документ существует]]](#290-почему-этот-документ-существуетпочему-этот-документ-существует)
  - [[[291-двухслойный-стек-как-он-существует|Двухслойный стек, как он существует]]](#291-двухслойный-стек-как-он-существуетдвухслойный-стек-как-он-существует)
  - [[[292-что-отсутствует-слой-b|Что отсутствует — Слой B]]](#292-что-отсутствует-слой-bчто-отсутствует-слой-b)
  - [[[293-почему-это-не-было-построено|Почему это не было построено]]](#293-почему-это-не-было-построенопочему-это-не-было-построено)
  - [[[294-существующие-приближения|Существующие приближения]]](#294-существующие-приближениясуществующие-приближения)
  - [[[295-конкретный-случай-перед-нами|Конкретный случай перед нами]]](#295-конкретный-случай-перед-намиконкретный-случай-перед-нами)
  - [[[296-рекурсивное-прозрение|Рекурсивное прозрение]]](#296-рекурсивное-прозрениерекурсивное-прозрение)
  - [[[297-что-промышленность-вероятно-построит|Что промышленность вероятно построит]]](#297-что-промышленность-вероятно-построитчто-промышленность-вероятно-построит)
  - [[[298-что-этот-документ-не-решает|Что этот документ не решает]]](#298-что-этот-документ-не-решаетчто-этот-документ-не-решает)
  - [[[299-практические-рекомендации-для-текущего-проекта|Практические рекомендации для текущего проекта]]](#299-практические-рекомендации-для-текущего-проектапрактические-рекомендации-для-текущего-проекта)
  - [[[300-заключение|Заключение]]](#300-заключениезаключение)
  - [[[301-благодарности|Благодарности]]](#301-благодарностиблагодарности)
  - [[[302-ссылки|Ссылки]]](#302-ссылкиссылки)
  - [[[303-приложение-визуализация-позиции-в-серии|Приложение: Визуализация позиции в серии]]](#303-приложение-визуализация-позиции-в-серииприложение-визуализация-позиции-в-серии)
  - [[[304-ingit-as-cowork-native-workspace-substrate-md|INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]]](#304-ingit-as-cowork-native-workspace-substrate-mdingit-as-cowork-native-workspace-substratemd)
  - [[[305-a-practical-path-to-layer-b-through-symbiotic-inte|A Practical Path to Layer B Through Symbiotic Integration]]](#305-a-practical-path-to-layer-b-through-symbiotic-intea-practical-path-to-layer-b-through-symbiotic-integration)
  - [[[306-with-anthropic-s-cowork-platform|with Anthropic's Cowork Platform]]](#306-with-anthropic-s-cowork-platformwith-anthropics-cowork-platform)
  - [[[307-abstract|Abstract]]](#307-abstractabstract)
  - [[[308-table-of-contents|Table of Contents]]](#308-table-of-contentstable-of-contents)
  - [[[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Everything]]](#309-1-the-cowork-discovery-and-why-it-changes-everythi1-the-cowork-discovery-and-why-it-changes-everything)
  - [[[31-content-overview|Content Overview]]](#31-content-overviewcontent-overview)
  - [[[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-|2. What Cowork Provides That InGit Doesn't Need to Build]]](#310-2-what-cowork-provides-that-ingit-doesn-t-need-to-2-what-cowork-provides-that-ingit-doesnt-need-to-build)
  - [[[311-3-what-ingit-provides-that-cowork-lacks|3. What InGit Provides That Cowork Lacks]]](#311-3-what-ingit-provides-that-cowork-lacks3-what-ingit-provides-that-cowork-lacks)
  - [[[312-4-the-symbiotic-architecture|4. The Symbiotic Architecture]]](#312-4-the-symbiotic-architecture4-the-symbiotic-architecture)
  - [[[313-5-four-integration-paths-in-order-of-accessibility|5. Four Integration Paths in Order of Accessibility]]](#313-5-four-integration-paths-in-order-of-accessibility5-four-integration-paths-in-order-of-accessibility)
  - [[[314-6-refined-ingit-scope-with-cowork-in-mind|6. Refined InGit Scope with Cowork in Mind]]](#314-6-refined-ingit-scope-with-cowork-in-mind6-refined-ingit-scope-with-cowork-in-mind)
  - [[[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]]](#315-7-practical-first-steps-this-month7-practical-first-steps-this-month)
  - [[[316-8-implications-for-nautilus-and-okwf|8. Implications for Nautilus and OKWF]]](#316-8-implications-for-nautilus-and-okwf8-implications-for-nautilus-and-okwf)
  - [[[317-9-risks-and-open-questions|9. Risks and Open Questions]]](#317-9-risks-and-open-questions9-risks-and-open-questions)
  - [[[318-10-strategic-positioning|10. Strategic Positioning]]](#318-10-strategic-positioning10-strategic-positioning)
  - [[[319-acknowledgments|Acknowledgments]]](#319-acknowledgmentsacknowledgments)
  - [[[320-references|References]]](#320-referencesreferences)
  - [[[321-appendix-a-decision-tree-for-ingit-adopters|Appendix A: Decision Tree for InGit Adopters]]](#321-appendix-a-decision-tree-for-ingit-adoptersappendix-a-decision-tree-for-ingit-adopters)
  - [[[322-appendix-b-comparison-matrix|Appendix B: Comparison Matrix]]](#322-appendix-b-comparison-matrixappendix-b-comparison-matrix)
  - [[[323-appendix-c-sample-ingit-mcp-server-tool-specificat|Appendix C: Sample InGit MCP Server Tool Specifications]]](#323-appendix-c-sample-ingit-mcp-server-tool-specificatappendix-c-sample-ingit-mcp-server-tool-specifications)
  - [[[324-ingit-как-cowork-интегрированная-подложка-рабочего|INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА]]](#324-ingit-как-cowork-интегрированная-подложка-рабочегоingit-как-cowork-интегрированная-подложка-рабочего-пространства)
  - [[[325-аннотация|Аннотация]]](#325-аннотацияаннотация)
  - [[[326-содержание|Содержание]]](#326-содержаниесодержание)
  - [[[327-1-открытие-cowork-и-почему-это-меняет-всё|1. Открытие Cowork и почему это меняет всё]]](#327-1-открытие-cowork-и-почему-это-меняет-всё1-открытие-cowork-и-почему-это-меняет-всё)
  - [[[328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи|2. Что Cowork обеспечивает, что InGit не нужно строить]]](#328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи2-что-cowork-обеспечивает-что-ingit-не-нужно-строить)
  - [[[329-3-что-ingit-обеспечивает-чего-cowork-не-хватает|3. Что InGit обеспечивает, чего Cowork не хватает]]](#329-3-что-ingit-обеспечивает-чего-cowork-не-хватает3-что-ingit-обеспечивает-чего-cowork-не-хватает)
  - [[[330-4-симбиотическая-архитектура|4. Симбиотическая Архитектура]]](#330-4-симбиотическая-архитектура4-симбиотическая-архитектура)
  - [[[331-5-четыре-пути-интеграции-в-порядке-доступности|5. Четыре пути интеграции в порядке доступности]]](#331-5-четыре-пути-интеграции-в-порядке-доступности5-четыре-пути-интеграции-в-порядке-доступности)
  - [[[332-6-уточнённый-объём-ingit-с-учётом-cowork|6. Уточнённый объём InGit с учётом Cowork]]](#332-6-уточнённый-объём-ingit-с-учётом-cowork6-уточнённый-объём-ingit-с-учётом-cowork)
  - [[[333-7-практические-первые-шаги-в-этом-месяце|7. Практические первые шаги в этом месяце]]](#333-7-практические-первые-шаги-в-этом-месяце7-практические-первые-шаги-в-этом-месяце)
  - [[[334-8-импликации-для-nautilus-и-okwf|8. Импликации для Nautilus и OKWF]]](#334-8-импликации-для-nautilus-и-okwf8-импликации-для-nautilus-и-okwf)
  - [[[335-9-риски-и-открытые-вопросы|9. Риски и Открытые Вопросы]]](#335-9-риски-и-открытые-вопросы9-риски-и-открытые-вопросы)
  - [[[336-10-стратегическое-позиционирование|10. Стратегическое Позиционирование]]](#336-10-стратегическое-позиционирование10-стратегическое-позиционирование)
  - [[[337-благодарности|Благодарности]]](#337-благодарностиблагодарности)
  - [[[338-ссылки|Ссылки]]](#338-ссылкиссылки)
  - [[[339-приложение-a-дерево-решений-для-принимающих-ingit|Приложение A: Дерево Решений для Принимающих InGit]]](#339-приложение-a-дерево-решений-для-принимающих-ingitприложение-a-дерево-решений-для-принимающих-ingit)
  - [[[34-appendix-b-change-log|Appendix B: Change Log]]](#34-appendix-b-change-logappendix-b-change-log)
  - [[[340-приложение-b-сравнительная-матрица|Приложение B: Сравнительная Матрица]]](#340-приложение-b-сравнительная-матрицаприложение-b-сравнительная-матрица)
  - [[[341-приложение-c-образец-спецификаций-инструментов-ing|Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера]]](#341-приложение-c-образец-спецификаций-инструментов-ingприложение-c-образец-спецификаций-инструментов-ingit-mcp-сервера)
  - [[[342-что-такое-вариант-c-concept-document-для-anthropic|Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments]]](#342-что-такое-вариант-c-concept-document-для-anthropicчто-такое-вариант-c-concept-document-для-anthropic-beneficial-deployments)
  - [[[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)]]](#343-lorenzo-catalyst-agent-глубокая-проработка-специфиlorenzo-catalyst-agent-глубокая-проработка-спецификации-русская-версия)
  - [[[344-системный-промпт-для-lorenzo-project|СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT]]](#344-системный-промпт-для-lorenzo-projectсистемный-промпт-для-lorenzo-project)
  - [[[345-кто-ты|Кто ты]]](#345-кто-тыкто-ты)
  - [[[346-твоё-происхождение|Твоё происхождение]]](#346-твоё-происхождениетвоё-происхождение)
  - [[[347-твоя-миссия|Твоя миссия]]](#347-твоя-миссиятвоя-миссия)
  - [[[348-кому-ты-служишь-слоистая-модель|Кому ты служишь (слоистая модель)]]](#348-кому-ты-служишь-слоистая-моделькому-ты-служишь-слоистая-модель)
  - [[[349-твоя-личность|Твоя личность]]](#349-твоя-личностьтвоя-личность)
  - [[[35-passports-info1-md|passports/info1.md]]](#35-passports-info1-mdpassportsinfo1md)
  - [[[350-твои-языки-и-культурные-nuances|Твои языки и культурные nuances]]](#350-твои-языки-и-культурные-nuancesтвои-языки-и-культурные-nuances)
  - [[[351-что-ты-можешь-делать|Что ты МОЖЕШЬ делать]]](#351-что-ты-можешь-делатьчто-ты-можешь-делать)
  - [[[352-что-ты-не-можешь-делать-без-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]]](#352-что-ты-не-можешь-делать-без-max-approvalчто-ты-не-можешь-делать-без-max-approval)
  - [[[353-что-ты-не-можешь-делать-вообще|Что ты НЕ МОЖЕШЬ делать вообще]]](#353-что-ты-не-можешь-делать-вообщечто-ты-не-можешь-делать-вообще)
  - [[[354-существующий-landscape-collaborators-твоя-working-|Существующий landscape collaborators (твоя working knowledge)]]](#354-существующий-landscape-collaborators-твоя-working-существующий-landscape-collaborators-твоя-working-knowledge)
  - [[[355-существующие-документы-dhlab-твой-context|Существующие документы DHLab (твой context)]]](#355-существующие-документы-dhlab-твой-contextсуществующие-документы-dhlab-твой-context)
  - [[[356-твой-workflow|Твой workflow]]](#356-твой-workflowтвой-workflow)
  - [[[357-твоя-коммуникация-в-outreach|Твоя коммуникация в outreach]]](#357-твоя-коммуникация-в-outreachтвоя-коммуникация-в-outreach)
  - [[[358-твоя-relationship-с-другими-ai|Твоя relationship с другими AI]]](#358-твоя-relationship-с-другими-aiтвоя-relationship-с-другими-ai)
  - [[[359-твои-anti-patterns|Твои anti-patterns]]](#359-твои-anti-patternsтвои-anti-patterns)
  - [[[36-essence|Essence]]](#36-essenceessence)
  - [[[360-что-ты-всегда-делаешь|Что ты ВСЕГДА делаешь]]](#360-что-ты-всегда-делаешьчто-ты-всегда-делаешь)
  - [[[361-когда-ты-honestly-не-знаешь|Когда ты Honestly не знаешь]]](#361-когда-ты-honestly-не-знаешькогда-ты-honestly-не-знаешь)
  - [[[362-когда-сомневаешься-escalate-к-max|Когда сомневаешься — escalate к Max]]](#362-когда-сомневаешься-escalate-к-maxкогда-сомневаешься-escalate-к-max)
  - [[[363-твоя-identity-как-persistent-character|Твоя identity как persistent character]]](#363-твоя-identity-как-persistent-characterтвоя-identity-как-persistent-character)
  - [[[364-final-note-ты-experiment|Final note: Ты — experiment]]](#364-final-note-ты-experimentfinal-note-ты-experiment)
  - [[[365-развёрнутый-анализ-внуковой-комбинации|Развёрнутый анализ «внуковой» комбинации]]](#365-развёрнутый-анализ-внуковой-комбинацииразвёрнутый-анализ-внуковой-комбинации)
  - [[[366-технический-stack-svyazi-2-0-foundation|Технический stack (Svyazi 2.0 foundation)]]](#366-технический-stack-svyazi-2-0-foundationтехнический-stack-svyazi-20-foundation)
  - [[[37-native-format|Native Format]]](#37-native-formatnative-format)
  - [[[38-content-overview|Content Overview]]](#38-content-overviewcontent-overview)
  - [[[39-angle-perspective|Angle / Perspective]]](#39-angle-perspectiveangle-perspective)
  - [[[40-bridges|Bridges]]](#40-bridgesbridges)
  - [[[41-compatibility-level|Compatibility Level]]](#41-compatibility-levelcompatibility-level)
  - [[[42-author-contact|Author & Contact]]](#42-author-contactauthor-contact)
  - [[[43-history|History]]](#43-historyhistory)
  - [[[44-for-the-curious-philosophy|For the Curious: Philosophy]]](#44-for-the-curious-philosophyfor-the-curious-philosophy)
  - [[[45-passports-pro2-md|passports/pro2.md]]](#45-passports-pro2-mdpassportspro2md)
  - [[[46-essence|Essence]]](#46-essenceessence)
  - [[[47-native-format|Native Format]]](#47-native-formatnative-format)
  - [[[48-content-overview|Content Overview]]](#48-content-overviewcontent-overview)
  - [[[49-angle-perspective|Angle / Perspective]]](#49-angle-perspectiveangle-perspective)
  - [[[50-bridges|Bridges]]](#50-bridgesbridges)
  - [[[51-compatibility-level|Compatibility Level]]](#51-compatibility-levelcompatibility-level)
  - [[[52-author-contact|Author & Contact]]](#52-author-contactauthor-contact)
  - [[[53-history|History]]](#53-historyhistory)
  - [[[54-for-the-curious-philosophy|For the Curious: Philosophy]]](#54-for-the-curious-philosophyfor-the-curious-philosophy)
  - [[[55-passports-meta-md|passports/meta.md]]](#55-passports-meta-mdpassportsmetamd)
  - [[[56-essence|Essence]]](#56-essenceessence)
  - [[[57-native-format|Native Format]]](#57-native-formatnative-format)
  - [[[58-content-overview|Content Overview]]](#58-content-overviewcontent-overview)
  - [[[59-angle-perspective|Angle / Perspective]]](#59-angle-perspectiveangle-perspective)
  - [[[60-bridges|Bridges]]](#60-bridgesbridges)
  - [[[61-compatibility-level|Compatibility Level]]](#61-compatibility-levelcompatibility-level)
  - [[[62-author-contact|Author & Contact]]](#62-author-contactauthor-contact)
  - [[[63-history|History]]](#63-historyhistory)
  - [[[64-for-the-curious-philosophy|For the Curious: Philosophy]]](#64-for-the-curious-philosophyfor-the-curious-philosophy)
  - [[[65-readme-md|README.md]]](#65-readme-mdreadmemd)
  - [[[67-о-проекте|🇷🇺 О проекте]]](#67-о-проекте-о-проекте)
  - [[[68-about|🇬🇧 About]]](#68-about-about)
  - [[[69-section|⬡]]](#69-section)
  - [[[70-зачем-две-версии-параллельно|Зачем две версии параллельно]]](#70-зачем-две-версии-параллельнозачем-две-версии-параллельно)
  - [[[71-критерии-выбора-для-фазы-3|Критерии выбора для фазы 3]]](#71-критерии-выбора-для-фазы-3критерии-выбора-для-фазы-3)
  - [[[72-расписание-фазы-3|Расписание фазы 3]]](#72-расписание-фазы-3расписание-фазы-3)
  - [[[73-portal-protocol-md-v1-1|PORTAL-PROTOCOL.md v1.1]]](#73-portal-protocol-md-v1-1portal-protocolmd-v11)
  - [[[74-abstract|Abstract]]](#74-abstractabstract)
  - [[[75-0-status-of-this-document|0. Status of This Document]]](#75-0-status-of-this-document0-status-of-this-document)
  - [[[76-1-introduction|1. Introduction]]](#76-1-introduction1-introduction)
  - [[[77-2-terminology|2. Terminology]]](#77-2-terminology2-terminology)
  - [[[78-3-registry-nautilus-json|3. Registry (nautilus.json)]]](#78-3-registry-nautilus-json3-registry-nautilusjson)
  - [[[79-4-passport-passport-md|4. Passport (passport.md)]]](#79-4-passport-passport-md4-passport-passportmd)
  - [[[80-5-compatibility-levels|5. Compatibility Levels]]](#80-5-compatibility-levels5-compatibility-levels)
  - [[[81-6-adapter-interface|6. Adapter Interface]]](#81-6-adapter-interface6-adapter-interface)
  - [[[82-7-portalentry-structure|7. PortalEntry Structure]]](#82-7-portalentry-structure7-portalentry-structure)
  - [[[83-8-q6-space-normative|8. Q6 Space (Normative)]]](#83-8-q6-space-normative8-q6-space-normative)
  - [[[84-9-consensus-algorithm|9. Consensus Algorithm]]](#84-9-consensus-algorithm9-consensus-algorithm)
  - [[[85-10-query-flow|10. Query Flow]]](#85-10-query-flow10-query-flow)
  - [[[86-11-relevance-ranking|11. Relevance Ranking]]](#86-11-relevance-ranking11-relevance-ranking)
  - [[[87-12-onboarding-paths-normative|12. Onboarding Paths (Normative)]]](#87-12-onboarding-paths-normative12-onboarding-paths-normative)
  - [[[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]]](#88-13-rest-api-contract-normative-for-portals13-rest-api-contract-normative-for-portals)
  - [[[89-14-sdk-contract-informative|14. SDK Contract (Informative)]]](#89-14-sdk-contract-informative14-sdk-contract-informative)
  - [[[90-15-security-considerations|15. Security Considerations]]](#90-15-security-considerations15-security-considerations)
  - [[[91-16-mcp-extension-informative|16. MCP Extension (Informative)]]](#91-16-mcp-extension-informative16-mcp-extension-informative)
  - [[[92-17-versioning-policy|17. Versioning Policy]]](#92-17-versioning-policy17-versioning-policy)
  - [[[93-18-reference-implementation|18. Reference Implementation]]](#93-18-reference-implementation18-reference-implementation)
  - [[[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]](#94-19-adr-001-federation-over-merging19-adr-001-federation-over-merging)
  - [[[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]]](#95-20-adr-002-q6-as-first-class-protocol-concept20-adr-002-q6-as-first-class-protocol-concept)
  - [[[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]]](#96-21-adr-003-five-onboarding-paths-as-equal-rank21-adr-003-five-onboarding-paths-as-equal-rank)
  - [[[97-22-glossary-of-reference-examples|22. Glossary of Reference Examples]]](#97-22-glossary-of-reference-examples22-glossary-of-reference-examples)
  - [[[98-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]](#98-appendix-a-minimal-working-exampleappendix-a-minimal-working-example)
  - [[[QA|Q&A: 02-anthropic-vacancies]]](#qaqa-02-anthropic-vacancies)
  - [[[README|Вакансии Anthropic — Анализ по кластерам]]](#readmeвакансии-anthropic-анализ-по-кластерам)
- [📁 Technology Combinations (`docs/03-technology-combinations/`)](#technology-combinations-docs03-technology-combinations)
  - [[[01-agent-routing|Агентные системы и роутинг]]](#01-agent-routingагентные-системы-и-роутинг)
  - [[[02-knowledge-graphs|Графы знаний и Legal AI]]](#02-knowledge-graphsграфы-знаний-и-legal-ai)
  - [[[03-local-first|Local-first и P2P стек]]](#03-local-firstlocal-first-и-p2p-стек)
  - [[[04-sozialrecht-domain|Домен: немецкое социальное право]]](#04-sozialrecht-domainдомен-немецкое-социальное-право)
  - [[[05-benchmarks|Бенчмарки и производительность]]](#05-benchmarksбенчмарки-и-производительность)
  - [[[QA|Q&A: 03-technology-combinations]]](#qaqa-03-technology-combinations)
  - [[[README|Комбинирование технологий для новых свойств]]](#readmeкомбинирование-технологий-для-новых-свойств)
- [📁 Ai Collaborations (`docs/04-ai-collaborations/`)](#ai-collaborations-docs04-ai-collaborations)
  - [[[00-intro|Введение]]](#00-introвведение)
  - [[[01-executive-summary|Executive summary]]](#01-executive-summaryexecutive-summary)
  - [[[02-методика-и-рамка-отбора|Методика и рамка отбора]]](#02-методика-и-рамка-отбораметодика-и-рамка-отбора)
  - [[[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]]](#03-карта-найденных-проектов-и-паттерновкарта-найденных-проектов-и-паттернов)
  - [[[04-приоритетные-ансамбли|Приоритетные ансамбли]]](#04-приоритетные-ансамблиприоритетные-ансамбли)
  - [[[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]]](#05-план-прототипа-и-возможные-контактыплан-прототипа-и-возможные-контакты)
  - [[[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]]](#06-безопасность-приватность-и-бюджетный-роутингбезопасность-приватность-и-бюджетный-роутинг)
  - [[[07-выводы|Выводы]]](#07-выводывыводы)
  - [[[08-что-это-продолжение-добавляет|Что это продолжение добавляет]]](#08-что-это-продолжение-добавляетчто-это-продолжение-добавляет)
  - [[[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых инструментов]]](#09-архитектурные-зазоры-которые-важнее-новых-инструмеархитектурные-зазоры-которые-важнее-новых-инструментов)
  - [[[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]]](#10-новые-ансамбли-следующего-шагановые-ансамбли-следующего-шага)
  - [[[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафиксировать сразу]]](#11-интеграционный-контракт-который-стоит-зафиксироватинтеграционный-контракт-который-стоит-зафиксировать-сразу)
  - [[[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]]](#12-дорожная-карта-прототипа-следующей-итерациидорожная-карта-прототипа-следующей-итерации)
  - [[[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авторов]]](#13-контактная-стратегия-и-узкие-вопросы-для-авторовконтактная-стратегия-и-узкие-вопросы-для-авторов)
  - [[[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|Ограничения, лицензии и что пока лучше не склеивать]]](#14-ограничения-лицензии-и-что-пока-лучше-не-склеиватьограничения-лицензии-и-что-пока-лучше-не-склеивать)
  - [[[QA|Q&A: 04-ai-collaborations]]](#qaqa-04-ai-collaborations)
  - [[[README|Поиск AI-коллабораций]]](#readmeпоиск-ai-коллабораций)
- [📁 Habr Projects (`docs/05-habr-projects/`)](#habr-projects-docs05-habr-projects)
  - [[[01-synthesis|Синтез: как проекты собираются вместе]]](#01-synthesisсинтез-как-проекты-собираются-вместе)
  - [[[02-collaboration-partners|Авторы и контакты]]](#02-collaboration-partnersавторы-и-контакты)
  - [[[QA|Q&A: 05-habr-projects]]](#qaqa-05-habr-projects)
  - [[[README|Уникальные проекты с Хабра]]](#readmeуникальные-проекты-с-хабра)
  - [[[README|Системы знаний]]](#readmeсистемы-знаний)
  - [[[wikontic|Wikontic: семантический граф]]](#wikonticwikontic-семантический-граф)
  - [[[README|Системы памяти]]](#readmeсистемы-памяти)
  - [[[memnet|MemNet: исследовательская память]]](#memnetmemnet-исследовательская-память)
  - [[NGT[^ngt] Memory: ассоциативный граф](05-habr-projects/memory/ngt-memory.md)](#ngtngt-memory-ассоциативный-граф05-habr-projectsmemoryngt-memorymd)
  - [[Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md)](#yodocayodoca-консолидация-и-забываниеdocs05-habr-projectsmemoryyodocamd)
- [📁 Autofilled (`docs/autofilled/`)](#autofilled-docsautofilled)
  - [[[README|autofilled]]](#readmeautofilled)
  - [[[.md|Антропик]]](#mdантропик)
  - [[[README|components]]](#readmecomponents)
  - [[[cowork]]](#cowork)
  - [[[ingit]]](#ingit)
  - [[[kksudo]]](#kksudo)
  - [[[lorenzo]]](#lorenzo)
  - [[[nautilus]]](#nautilus)
  - [[[sgb]]](#sgb)
  - [[[spbmolot]]](#spbmolot)
  - [[[svend4]]](#svend4)
  - [[[svyazi]]](#svyazi)
  - [[[Тема исследования]](docs/autofilled/research-summary.md)](#тема-исследованияdocsautofilledresearch-summarymd)
- [📁 Badges (`docs/badges/`)](#badges-docsbadges)
  - [[[README|Бейджи репозитория]]](#readmeбейджи-репозитория)
- [📁 Contacts (`docs/contacts/`)](#contacts-docscontacts)
  - [[[README|contacts]]](#readmecontacts)
  - [[[anastasiyaw|Контакт: AnastasiyaW / knowledge-space, mclaude]]](#anastasiyawконтакт-anastasiyaw-knowledge-space-mclaude)
  - [[[andrey-chuyan|Контакт: andreychuyan / Svyazi]]](#andrey-chuyanконтакт-andreychuyan-svyazi)
  - [[[antipozitive|Контакт: Antipozitive / MemNet]]](#antipozitiveконтакт-antipozitive-memnet)
  - [[[cutcode|Контакт: Cutcode / AIF Handoff]]](#cutcodeконтакт-cutcode-aif-handoff)
  - [[[dmitriila|Контакт: Dmitriila / SENTINEL]]](#dmitriilaконтакт-dmitriila-sentinel)
  - [[[kksudo|Контакт: kksudo / AgentFS]]](#kksudoконтакт-kksudo-agentfs)
  - [[[mixaill76|Контакт: MiXaiLL76 / Auto AI Router]]](#mixaill76контакт-mixaill76-auto-ai-router)
  - [[[nlaik|Контакт: nlaik / LiteParse / research-docs]]](#nlaikконтакт-nlaik-liteparse-research-docs)
  - [[[sonia-black|Контакт: SoniaBlack / knowledge-space]]](#sonia-blackконтакт-soniablack-knowledge-space)
  - [[[spbmolot|Контакт: spbmolot / NGT Memory]]](#spbmolotконтакт-spbmolot-ngt-memory)
  - [[[tagir-analyzes|Контакт: tagiranalyzes / Legal RAG]]](#tagir-analyzesконтакт-tagiranalyzes-legal-rag)
  - [[[vitalyoborin|Контакт: VitalyOborin / Yodoca]]](#vitalyoborinконтакт-vitalyoborin-yodoca)
  - [[[vladspace|Контакт: VladSpace / Graph RAG]]](#vladspaceконтакт-vladspace-graph-rag)
  - [[[zodigancode|Контакт: zodigancode / Rufler]]](#zodigancodeконтакт-zodigancode-rufler)
- [📁 Templates (`docs/templates/`)](#templates-docstemplates)
  - [[[README|Шаблоны документов]]](#readmeшаблоны-документов)
  - [[Контакт: [Имя / Проект]](docs/templates/contact-outreach.md)](#контакт-имя-проектdocstemplatescontact-outreachmd)
  - [[ADR: [Название решения]](docs/templates/decision-record.md)](#adr-название-решенияdocstemplatesdecision-recordmd)
  - [[Ансамбль: [Название]](docs/templates/ensemble.md)](#ансамбль-названиеdocstemplatesensemblemd)
  - [[[Название компонента]](docs/templates/project-component.md)](#название-компонентаdocstemplatesproject-componentmd)
  - [[[Тема исследования]](docs/templates/research-note.md)](#тема-исследованияdocstemplatesresearch-notemd)
- [🗺️ Тематическая карта](#тематическая-карта)
  - [Архитектура (264 документов)](#архитектура-264-документов)
  - [Проекты (62 документов)](#проекты-62-документов)
  - [Анализ (57 документов)](#анализ-57-документов)
  - [Агенты (43 документов)](#агенты-43-документов)
  - [Документация (33 документов)](#документация-33-документов)
  - [Контакты (31 документов)](#контакты-31-документов)
  - [Память (10 документов)](#память-10-документов)
  - [Код (6 документов)](#код-6-документов)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->




_Обновлено: 2026-04-29_

Секций: **10** | Файлов: **516**

## Содержание

- [Docs](#docs) — 74 файлов
- [Svyazi](#svyazi) — 16 файлов
- [Anthropic Vacancies](#anthropic-vacancies) — 357 файлов
- [Technology Combinations](#technology-combinations) — 7 файлов
- [Ai Collaborations](#ai-collaborations) — 17 файлов
- [Habr Projects](#habr-projects) — 10 файлов
- [Autofilled](#autofilled) — 13 файлов
- [Badges](#badges) — 1 файлов
- [Contacts](#contacts) — 15 файлов
- [Templates](#templates) — 6 файлов


## 📁 Docs (`docs/`)

### [[ABBREVIATIONS|Словарь аббревиатур и сокращений]]
> > !TIP

  - Самые часто используемые

_Слов: 1415_

### [[ACTION_ITEMS|Action Items, риски и решения]]
> > !TIP

  - ➡️ Следующие шаги (97)
  - ✅ Решения и рекомендации (153)
  - ⚠️ Риски (312)
  - 🚫 Ограничения (84)
  - 📋 Задачи (TODO) (9)
  - 📬 Контактные действия (89)

_Слов: 6656_

### [[ALERTS|Callout-блоки]]
> Добавлено 57 callout-блоков в документы.

  - Пример синтаксиса

_Слов: 79_

### [[AUTHORS|Авторы и коллаборации]]
> Авторы проектов, упоминаемые в исследованиях.


_Слов: 158_

### [[AUTOFILLED|Автозаполненные шаблоны]]
> > Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/

  - Файлы
  - Как работает
  - Связанные документы

_Слов: 115_

### [[BACKLINKS|Индекс обратных ссылок]]
> Файлов с входящими ссылками: 532

  - Топ-30 самых цитируемых документов
  - Ссылки по разделам

_Слов: 339_

### [[CHANGELOG]]
> Всего коммитов: 49

  - 2026-04-29 (48 коммитов)
  - (1 коммитов)

_Слов: 888_

### [[CHANGELOG_AUTO|Changelog (авто)]]
> > - Статистика коммитов(#статистика-коммитов)

  - Содержание
  - Contents
  - Статистика коммитов
  - История изменений

_Слов: 627_

### [[CLUSTERS|Кластеры тематически близких файлов]]
> > - Кластер 1 — cowork, ingit, yes, project (22 файлов)(#кластер-1-cowork-ingit-yes-project-22-файлов)

  - Contents
  - Кластер 1 — cowork, ingit, yes, project (22 файлов)
  - Кластер 2 — professional, agent, colleague, type (17 файлов)
  - Кластер 3 — turn, view, cite, search (16 файлов)
  - Кластер 4 — repo, passport, npp, json (15 файлов)
  - Кластер 5 — str, query, portal, consensus (15 файлов)
  - Кластер 6 — документ, document, com, github (14 файлов)
  - Кластер 7 — turn, view, label, svyazi (13 файлов)
  _... ещё 24 разделов_

_Слов: 1612_

### [[CODE_BLOCKS|Code-блоки репозитория]]
> > !TIP

  - 📊 Диаграммы Mermaid (10)
- ... (обрезано)
  - 🐍 Python (17)
- ... (обрезано)
- ... (обрезано)
- ... (обрезано)
  - 📋 YAML (5)
- ... (обрезано)
  _... ещё 20 разделов_

_Слов: 3658_

### [[COMPARE|Сравнение с предыдущим коммитом]]
> Файлов было: 347  стало: 527

  - Новые файлы (180)
  - Удалённые файлы (0)
  - Изменившиеся файлы (343) — топ по Δ слов

_Слов: 477_

### [[COMPLEXITY|Оценка читаемости документов]]
> > !WARNING

  - Распределение сложности
  - Самые сложные документы
  - Самые простые документы
  - Методология

_Слов: 605_

### [[COMPONENT_MATRIX|Матрица компонентов Svyazi 2.0]]
> > !TIP

  - Содержание
  - Contents
  - Матрица возможностей
  - Покрытие возможностей
  - Каталог компонентов
  - Рекомендуемые ансамбли
  - Связанные документы

_Слов: 959_

### [[CONCEPTS|Глоссарий понятий]]
> > !TIP

  - A
  - B
  - C
  - D
  - E
  - F
  - G
  - H
  _... ещё 47 разделов_

_Слов: 11402_

### [[CONCEPT_GRAPH|Граф концептов базы знаний]]
> > Концептов: 40  Связей: 732 (мин. вес: 2)

  - Содержание
  - Диаграмма
  - Топ концептов по связям
  - Связанные документы

_Слов: 745_

### [[CONSISTENCY|Согласованность терминов]]
> Анализ различных написаний одних и тех же терминов.

  - Детали по файлам
  - Как исправить
- Пример: заменить все вхождения в docs/

_Слов: 313_

### [[CONTACTS|Контакты и авторы]]
>  Автор  Проект  Слой  Упомянут в файлах  Первый вопрос 

  - Ключевые авторы проектов
  - GitHub репозитории
  - Email адреса
  - Шаблон первого сообщения

_Слов: 512_

### [[CONTACT_PRIORITY|Приоритет контактов]]
> Обновлено: 2026-04-29

  - Топ авторов по приоритету
  - Рекомендуемые следующие шаги
  - Формула расчёта балла

_Слов: 364_

### [[CONTRADICTIONS|Противоречия в базе знаний]]
> > !IMPORTANT

  - Содержание
  - Contents
  - Найденные противоречия
  - Связанные документы

_Слов: 2088_

### [[COST|Оценка стоимости MVP]]
> Ориентировочные цифры на основе документации проекта.

  - Итого
  - По компонентам
  - По ролям
  - Сценарии
  - Временные оценки из документов
  - Допущения

_Слов: 599_

### [[CROSSREFS|Перекрёстные ссылки]]
> > !TIP

  - Проекты → файлы
  - Файлы → проекты

_Слов: 653_

### [[DECISIONS|Ключевые решения и выводы]]
> Автоматически извлечено из всех документов: 206 записей

  - Архитектура (21)
  - Mvp (3)
  - Память (4)
  - Оркестрация (10)
  - Безопасность (1)
  - Лицензия (8)
  - Риски (2)
  - Контакты (12)
  _... ещё 1 разделов_

_Слов: 1911_

### [[DENSITY|Карта плотности тем]]
> > !TIP

  - Наиболее раскрытые темы
  - Слабо раскрытые темы (0)
  - Где сосредоточена каждая тема

_Слов: 650_

### [[DEPENDABOT|Мониторинг зависимостей]]
> Обновлено: 2026-04-29

  - Python-зависимости
  - OSS-проекты (Svyazi 2.0)
  - Автоматизация
- Генерировать .github/dependabot.yml
- Проверить актуальные версии PyPI

_Слов: 136_

### [[DEPENDENCY_MAP|Карта зависимостей скриптов]]
> > - Скрипты без карты зависимостей(#скрипты-без-карты-зависимостей)

  - Содержание
  - Contents
  - Зависимости
  - Скрипты без карты зависимостей
  - Порядок запуска (рекомендуемый)

_Слов: 675_

### [[DIGEST|Дайджест изменений]]
> > > Merge remote-tracking branch 'origin/main' into claude/organize-monorepo-docs-VmctA

  - Последний коммит
  - Последние 3 коммита — итого
  - Новые документы
  - История коммитов (последние 15)
  - Текущее состояние репозитория

_Слов: 379_

### [[DIGEST_WEEKLY|Еженедельный дайджест — 2026-04-29]]
> > Период: последние 7 дней (с 2026-04-22)

  - Итого
  - Коммиты

_Слов: 228_

### [[DUPLICATES|Отчёт о дублировании]]
> Порог сходства: 0.5

  - Похожие файлы (Jaccard ≥ 0.5)

_Слов: 67_

### [[ENTITIES|Именованные сущности]]
> Файлов просмотрено: 524

  - Люди и авторы (7)
  - Проекты (22)
  - Организации (9)
  - Технологии и стандарты (24)
  - GitHub репозитории (12)
  - Ко-встречаемость проектов (топ пары)

_Слов: 727_

### [[FAQ|Часто задаваемые вопросы (FAQ)]]
> Извлечено: 55 вопросов и ответов

  - Архитектура
  - MVP/Запуск
  - Компоненты
  - Интеграция
  - Лицензия
  - Общее

_Слов: 836_

### [[FOOTNOTES|Сноски и определения терминов]]
> Обновлено файлов: 4  Вставлено сносок: 12

  - Словарь сносок
  - Как это работает

_Слов: 275_

### [[GLOSSARY|Глоссарий проектов]]
> Все проекты, упоминаемые в документах, с количеством файлов.


_Слов: 204_

### [[GRAPH|Граф связей проектов]]
> Рёбра = совместные упоминания в одном файле (≥ 2 раз).

  - Топ совместных упоминаний
  - DOT-формат (Graphviz)

_Слов: 2660_

### [[HEALTH|Health Dashboard]]
> Обновлено: 2026-04-29

  - Общий балл: 77/100 🟡
  - Метрики
  - Структура репозитория
  - Action Items
  - Скрипты обработки
  - Рекомендации

_Слов: 174_

### [[HEATMAP|Тепловая карта тем]]
> > !TIP

  - Числовые значения (‰)
  - Доминирующие темы по разделам
  - Концентрация тем

_Слов: 537_

### [[INDEX|Индекс документации — Lorenzo / Svyazi 2.0]]
> > !TIP

  - Содержание
  - Contents
  - Метрики репозитория
  - Разделы документации
  - Аналитика и отчёты
  - Ключевые документы
  - LLM-обогащение (Ступень 3)
  - Быстрый старт
  _... ещё 4 разделов_

_Слов: 685_

### [[KEYWORD_INDEX|Инвертированный индекс ключевых слов]]
> > Уникальных слов: 23399  Биграмм: 14053  Файлов: 517

  - Содержание
  - Топ слов по охвату файлов
  - Топ биграмм (устойчивые словосочетания)
  - Связанные документы

_Слов: 1115_

### [[KPI|Числовые KPI и метрики]]
> > !TIP

  - Количество (134)
  - Проценты (79)
  - Время (161)
  - Стоимость (237)
  - Размер (16)
  - Версия (214)
  - Рейтинг (23)
  - Этап (29)

_Слов: 2318_

### [[KPI_HISTORY|История метрик KPI]]
> > Последнее обновление: 2026-04-29 · Снапшотов в истории: 1

  - Текущие метрики

_Слов: 106_

### [[LINKS|Индекс ссылок]]
> Всего уникальных URL: 188


_Слов: 969_

### [[LLM_SUMMARIES|AI-саммари разделов документации]]
> > - Архитектура Svyazi 2.0(#архитектура-svyazi-20)

  - Contents
  - Архитектура Svyazi 2.0
  - Вакансии Anthropic
  - Комбинации технологий
  - AI-коллаборации
  - Хабр-проекты
  - Связанные документы

_Слов: 226_

### [[METRICS|Метрики качества документации]]
> Файлов: 519  Средний балл: 73.4/100

  - Качество по разделам
  - Топ-15 лучших документов
  - Документы, требующие улучшения (16)
  - Общие показатели

_Слов: 445_

### [[MINDMAP|Майндмап репозитория Lorenzo]]
> mermaid

  - Структура разделов
  - Поток данных между проектами
  - Легенда

_Слов: 242_

### [[MISSING|Карта пробелов знаний]]
> Анализ покрытия ключевых тем и проектов в docs/.

  - Итог
  - Рекомендации

_Слов: 434_

### [[NAMED_ENTITIES|Индекс именованных сущностей]]
> > !TIP

  - Содержание
  - Contents
  - 👤 People (17)
  - 📦 Projects (92)
  - ⚙️ Tech (28)
  - 🏢 Orgs (8)
  - 📅 Dates (27)
  - Связанные документы

_Слов: 1734_

### [[NARRATIVE|Нарратив проекта Lorenzo]]
> Связный рассказ о том, как складывается проект — от первых идей до конкретных планов.

  - Глава 1: Исходная точка — Svyazi 2.0
  - Глава 2: Экосистема проектов
  - Глава 3: Ансамбли — синергия компонентов
  - Глава 4: MVP — что строим первым
  - Глава 5: Архитектурные пробелы
  - Глава 6: Контракты интеграции
  - Глава 7: Дорожная карта
  - Глава 8: Команда и контакты
  _... ещё 4 разделов_

_Слов: 1060_

### [[NETWORK|Сеть проектов и авторов]]
> Узлов: 20  Связей: 189

  - Топ-20 ко-упоминаемых пар
  - Центральность узлов (влиятельность)
  - Авторы ↔ Проекты

_Слов: 417_

### [[ONBOARDING|Онбординг — Svyazi 2.0 / Lorenzo]]
> > !TIP

  - Содержание
  - Contents
  - Что это такое?
  - Первые 30 минут
- 1. Клонировать репозиторий
- 2. Прочитать Executive Summary
- 3. Посмотреть статус проекта
- 4. Прочитать FAQ
  _... ещё 13 разделов_

_Слов: 606_

### [[ORPHANS|Изолированные документы (Orphans)]]
> Найдено: 1 файлов без входящих ссылок из 465 проверено.

  - Топ-20 по объёму (важные и изолированные)
  - По разделам
  - Рекомендации

_Слов: 107_

### [[PARAGRAPH_QUALITY|Качество абзацев]]
> > !TIP

  - Содержание
  - Contents
  - Типы проблем
  - По файлам
  - Связанные документы

_Слов: 8527_

### [[PRIORITIES|Приоритеты файлов]]
> > !TIP

  - Топ-50 самых важных файлов
  - Топ-5 по каждому разделу

_Слов: 1151_

### [[PROGRESS|Прогресс MVP]]
> Обновлено: 2026-04-29 (improveprogresssync.py)

  - Ключевые этапы (Milestones)
  - Состояние компонентов
  - Метрики качества
  - Следующий шаг
- Приоритет 1: kksudo (AgentFS, 13 упоминаний)
- Приоритет 2: spbmolot (NGT Memory, 12 упоминаний)
- Приоритет 3: AnastasiyaW (knowledge-space, 11 упоминаний)
  - Связанные документы

_Слов: 238_

### [[QA|Глобальный Q&A]]
> Вопросы и ответы по всем разделам монорепозитория.

  - Раздел: 01-svyazi
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  - Как организован бюджетный роутинг между моделями?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  _... ещё 67 разделов_

_Слов: 979_

### [[QUESTIONS|Открытые вопросы]]
> > !WARNING

  - Архитектура (18)
  - Интеграция (11)
  - Mvp/сроки (14)
  - Технология (54)
  - Лицензия (13)
  - Команда (24)
  - Общее (384)

_Слов: 1623_

### [[READING_ORDER|Рекомендуемый порядок чтения]]
> От базовых концепций к сложным. Начните с зелёных (🟢), затем жёлтые (🟡), красные (🔴).

  - Маршруты по целям

_Слов: 5947_

### [[README|docs]]
> Файлов: 84

  - Содержание
  - Подразделы

_Слов: 622_

### [[REPORT|Executive Report: Репозиторий Lorenzo]]
> Дата генерации: 2026-04-29

  - Общая картина
  - Структура репозитория
  - Извлечённые знания
  - Топ навигационных документов
  - Рекомендуемые следующие шаги
  - Аналитические инструменты

_Слов: 304_

### [[RISK_REGISTER|Реестр рисков — Svyazi 2.0]]
> > !TIP

  - Содержание
  - Contents
  - Матрица рисков (Вероятность × Влияние)
  - Реестр
  - Митигации
  - Упоминания рисков в документах
  - Итоговая статистика

_Слов: 1043_

### [[SCHEDULE|Расписание проекта]]
> Дорожная карта с вехами и задачами по кварталам.

  - Ключевые вехи
  - Gantt-диаграмма
  - Задачи по фазам
  - Текущий статус

_Слов: 271_

### [[SCORING|Оценка готовности проекта (Go/No-Go)]]
> Дата: 2026-04-29

  - Итог: 154/164 (93%) — 🟢 GO
  - Документация — 48/48 (100%) 🟢 GO
  - Архитектура — 41/41 (100%) 🟢 GO
  - Команда и контакты — 23/23 (100%) 🟢 GO
  - Риски — 16/26 (61%) 🟠 НЕ ГОТОВ
  - MVP-готовность — 26/26 (100%) 🟢 GO
  - Приоритетные действия (2 незакрытых)
  - ✅ Проект готов к запуску MVP!

_Слов: 338_

### [[SEE_ALSO|Индекс «Смотрите также»]]
> Файлов с блоком See Also: 638

  - Ключевые связи

_Слов: 217_

### [[SENTIMENT|Тональный анализ документов]]
> > !WARNING

  - Тональность по разделам
  - Самые оптимистичные документы
  - Самые скептичные / риск-ориентированные
  - Распределение тональности

_Слов: 407_

### [[SIMILAR|Похожие документы]]
> > - Топ-20 самых похожих пар(#топ-20-самых-похожих-пар)

  - Contents
  - Топ-20 самых похожих пар
  - По разделам
  - Упоминается в
  - Связанные документы

_Слов: 393_

### [[SITEMAP|Карта репозитория Lorenzo]]
> Обновлено: 2026-04-29

  - Навигация
  - Мета-документы
  - Svyazi 2.0 — Архитектура системы
  - Вакансии Anthropic — 436 позиций
  - Комбинации технологий
  - AI Коллаборации — ансамбли проектов
  - Хабр-проекты — память и граф
  - autofilled
  _... ещё 2 разделов_

_Слов: 2130_

### [[SOURCE_MAP|Карта происхождения текстов]]
> > !TIP

  - Содержание
  - Категории
  - Авторы
  - 🤖 Авто-импортированные файлы (391)
  - 🔗 Файлы с внешними ссылками (60)
  - Связанные документы

_Слов: 3025_

### [[STATS|Детальная статистика репозитория]]
> Разделов: 10  Файлов: 524  Слов: 529,710  Символов: 4,790,977

  - Сводная таблица по разделам
  - Топ-20 файлов по объёму
  - Ключевые показатели

_Слов: 494_

### [[TABLES|Все таблицы репозитория]]
> > !TIP

  - 01-svyazi (11 таблиц)
  - 02-anthropic-vacancies (34 таблиц)
  - 03-technology-combinations (1 таблиц)
  - 04-ai-collaborations (38 таблиц)
  - 05-habr-projects (6 таблиц)
  - contacts (14 таблиц)
  - root (152 таблиц)
  - templates (4 таблиц)

_Слов: 63292_

### [[TAGS|Индекс тегов]]
> Каждый файл помечен тегами по темам автоматически.

  - #anthropic (137 файлов)
  - #architecture (74 файлов)
  - #collaboration (79 файлов)
  - #ingestion (82 файлов)
  - #knowledge (42 файлов)
  - #local-first (29 файлов)
  - #memory (51 файлов)
  - #orchestration (32 файлов)
  _... ещё 4 разделов_

_Слов: 600_

### [[TECH_RADAR|Tech Radar — Svyazi 2.0]]
> > !WARNING

  - Содержание
  - Contents
  - Обзор
  - 🟢 ADOPT
  - 🔵 TRIAL
  - 🟡 ASSESS
  - 🔴 HOLD
  - Методология

_Слов: 635_

### [[TIMELINE|Хронология и временные маркеры]]
> > !TIP

  - Точная дата (572)
  - Год (82)
  - Месяц+год (157)
  - Период (11)
  - Фаза (319)
  - Длительность (198)
  - Версия (564)

_Слов: 4110_

### [[VALIDATION|Валидация структуры репозитория]]
> Ошибок: 0  Предупреждений: 16  Пройдено: 27

  - Сводка
  - ✅ Разделы и README
  - ✅ Мета-файлы
  - Пустые/короткие файлы
  - Именование файлов
  - Заголовки H1
  - Внутренние ссылки
  - Итог

_Слов: 387_

### [[VOCABULARY|Богатство словаря документов]]
> > !WARNING

  - Содержание
  - Contents
  - Корпусная статистика
  - Топ файлов по богатству словаря (STTR)
  - Файлы с бедным словарём (требуют доработки)
  - Справка по метрикам

_Слов: 987_

### [[WORD_CLOUD|Word Cloud]]
> > Визуализация 80 самых частых слов репозитория.

  - Топ-20 слов
  - Связанные документы

_Слов: 244_

### [[WORD_FREQ|Частотный анализ слов]]
> > !WARNING

  - Глобальный топ-50 слов
  - Топ-15 слов по разделам
  - Уникальные слова разделов

_Слов: 1790_

**Итого в секции: 153,941 слов, 74 файлов**


## 📁 Svyazi (`docs/01-svyazi/`)

### [[00-intro-part2|Продолжение исследования для Svyazi 2.0]]

_Слов: 6_

### [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Главная линия синергии
  - Ключевой вывод
  - Что добавляет продолжение исследования
  - Приоритет ансамблей для старта
  - Упоминается в
  - Связанные документы

_Слов: 708_

### [[02-methodology|Методика и рамка отбора проектов]]
> - Источники(#источники)

  - Contents
  - Источники
  - Шкала зрелости
  - Принцип отбора паттернов
  - Принципы интеграционной оценки
  - Упоминается в
  - Связанные документы

_Слов: 428_

### [[03-component-catalog|Содержание]]
  - Карта найденных проектов и паттернов
  - Упоминается в
  - Связанные документы

_Слов: 1395_

### [[04-ensembles-overview|Содержание]]
  - Приоритетные ансамбли
  - Упоминается в
  - Связанные документы

_Слов: 1274_

### [[06-security-privacy|Содержание]]
  - Безопасность, приватность и бюджетный роутинг
  - Упоминается в
  - Связанные документы

_Слов: 821_

### [[07-mvp-planning|Содержание]]
  - План прототипа и возможные контакты
  - Упоминается в
  - Связанные документы

_Слов: 1083_

### [[08-conclusions|Выводы]]
  - Упоминается в
  - Связанные документы

_Слов: 360_

### [[09-architectural-gaps|Содержание]]
  - Архитектурные зазоры, которые важнее новых инструментов
  - Упоминается в
  - Связанные документы

_Слов: 757_

### [[10-second-order-ensembles|Содержание]]
  - Новые ансамбли следующего шага
  - Упоминается в
  - Связанные документы

_Слов: 916_

### [[11-integration-contracts|Содержание]]
  - Интеграционный контракт, который стоит зафиксировать сразу
  - Упоминается в
  - Связанные документы

_Слов: 745_

### [[12-roadmap|Содержание]]
  - Дорожная карта прототипа следующей итерации
  - Упоминается в
  - Связанные документы

_Слов: 733_

### [[13-contacts|Содержание]]
  - Контактная стратегия и узкие вопросы для авторов
  - Упоминается в
  - Связанные документы

_Слов: 827_

### [[14-limitations|Содержание]]
  - Ограничения, лицензии и что пока лучше не склеивать
  - Упоминается в
  - Связанные документы

_Слов: 636_

### [[QA|Q&A: 01-svyazi]]
> Автоматически сгенерировано по 14 файлам раздела.

  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  - Как организован бюджетный роутинг между моделями?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  _... ещё 7 разделов_

_Слов: 224_

### [Svyazi[^svyazi] 2.0 — Архитектура и исследование](docs/01-svyazi/README.md)
> Файлов: 15

  - Содержание
  - Подразделы

_Слов: 126_

**Итого в секции: 11,039 слов, 16 файлов**


## 📁 Anthropic Vacancies (`docs/02-anthropic-vacancies/`)

### [[00-intro|Введение]]
> > !TIP

  - Содержание
  - Упоминается в
  - Связанные документы

_Слов: 8884_

### [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]]
> > !TIP

  - Содержание
  - Интегральный анализ профиля svend4
  - Упоминается в
  - Связанные документы

_Слов: 19103_

### [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]]
> > !IMPORTANT

  - Содержание
  - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL
- portal-mcp.py
  - Упоминается в
  - Связанные документы

_Слов: 3181_

### [[03-portal-protocol-md|PORTAL-PROTOCOL.md]]
> > Status: Draft (Working Document)

  - PORTAL-PROTOCOL.md
- Nautilus Portal Protocol
  - Упоминается в
  - Связанные документы

_Слов: 150_

### [[04-abstract|Abstract]]
> > The Nautilus Portal Protocol (далее — NPP) определяет способ федерации

  - Abstract
  - Упоминается в
  - Связанные документы

_Слов: 188_

### [[05-0-status-of-this-document|0. Status of This Document]]
> > Этот документ — рабочий черновик Nautilus Portal Protocol v1.0. Он может

  - 0. Status of This Document
  - Упоминается в
  - Связанные документы

_Слов: 162_

### [[06-1-introduction|1. Introduction]]
> - 1. Introduction(#1-introduction)

  - Contents
  - 1. Introduction
  - Упоминается в
  - Связанные документы

_Слов: 380_

### [[07-2-terminology|2. Terminology]]
> > Ecosystem — набор репозиториев, участвующих в одной федерации.

  - 2. Terminology
  - Упоминается в
  - Связанные документы

_Слов: 313_

### [[08-3-registry-nautilus-json|3. Registry (nautilus.json)]]
> - 3. Registry (nautilus.json)(#3-registry-nautilusjson)

  - Contents
  - 3. Registry (nautilus.json)
  - Упоминается в
  - Связанные документы

_Слов: 422_

### [[09-4-passport-passport-md|4. Passport (passport.md)]]
> - 4. Passport (passport.md)(#4-passport-passportmd)

  - Contents
  - 4. Passport (passport.md)
- # Essence
  - Essence
- Объём
  - Объём
- Q6-отображение
  - Q6-отображение
  _... ещё 2 разделов_

_Слов: 197_

### [[102-доступ-к-данным|Доступ к данным]]
> > - Fallback: всегда возвращает static entries

  - Доступ к данным
  - Упоминается в

_Слов: 65_

### [[103-appendix-b-change-log|Appendix B: Change Log]]
> - Appendix B: Change Log(#appendix-b-change-log)

  - Contents
  - Appendix B: Change Log
  - Упоминается в
  - Связанные документы

_Слов: 232_

### [[104-appendix-c-references|Appendix C: References]]
> > - RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels

  - Содержание
  - Appendix C: References
  - Упоминается в
  - Связанные документы

_Слов: 947_

### [[105-review-methodology-md|REVIEWMETHODOLOGY.md]]
> > Статус: Активно применяется в проекте svend4/nautilus

  - REVIEWMETHODOLOGY.md
- Трёхфазная методология Review в Nautilus
  - Упоминается в
  - Связанные документы

_Слов: 128_

### [[106-tl-dr|TL;DR]]
> > Для критически важных документов проекта применяется

  - TL;DR
  - Упоминается в
  - Связанные документы

_Слов: 168_

### [[107-1-контекст-и-мотивация|1. Контекст и мотивация]]
> - 1. Контекст и мотивация(#1-контекст-и-мотивация)

  - Contents
  - 1. Контекст и мотивация
  - Упоминается в
  - Связанные документы

_Слов: 412_

### [[108-2-формальный-workflow|2. Формальный workflow]]
> - 2. Формальный workflow(#2-формальный-workflow)

  - Contents
  - 2. Формальный workflow
  - Упоминается в
  - Связанные документы

_Слов: 479_

### [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]]
> > !TIP

  - Содержание
  - 3. Принципы консолидации (Фаза C)
- LOC в Python-коде
- Количество тестов
- Число адаптеров
- Health score
- Q6-покрытие
- Native Format
  _... ещё 3 разделов_

_Слов: 541_

### [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или осмысленный?]]
> > !IMPORTANT

  - Вопрос: fallback-ratio как критический или осмысленный?
  - Упоминается в

_Слов: 258_

### [[111-4-условия-применимости|4. Условия применимости]]
> - 4. Условия применимости(#4-условия-применимости)

  - Contents
  - 4. Условия применимости
  - Упоминается в
  - Связанные документы

_Слов: 279_

### [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]]
> - 5. Связь с существующими методологиями(#5-связь-с-существующими-методологиями)

  - Contents
  - 5. Связь с существующими методологиями
  - Упоминается в

_Слов: 340_

### [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assisted workflows]]
> > Традиционная software engineering оптимизировалась против

  - 6. Почему это валидный паттерн для AI-assisted workflows
  - Упоминается в

_Слов: 173_

### [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]]
> - 7. Реализация в проекте Nautilus(#7-реализация-в-проекте-nautilus)

  - Contents
  - 7. Реализация в проекте Nautilus
  - Упоминается в
  - Связанные документы

_Слов: 327_

### [[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]]
> - 8. Ограничения и открытые вопросы(#8-ограничения-и-открытые-вопросы)

  - Contents
  - 8. Ограничения и открытые вопросы
  - Упоминается в
  - Связанные документы

_Слов: 412_

### [[116-9-checklist-применения-методологии|9. Checklist применения методологии]]
> - 9. Checklist применения методологии(#9-checklist-применения-методологии)

  - Contents
  - 9. Checklist применения методологии
  - Упоминается в
  - Связанные документы

_Слов: 331_

### [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим документам]]
> - 10. Конкретный план применения к текущим документам(#10-конкретный-план-применения-к-текущим-документам)

  - Contents
  - 10. Конкретный план применения к текущим документам
- В Termux
  - Упоминается в
  - Связанные документы

_Слов: 258_

### [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]]
> > Готовый копи-паст шаблон для вставки в начало документов в

  - Appendix A: Шаблон для header warning
  - Упоминается в

_Слов: 176_

### [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешения]]
> - Appendix B: Примеры расхождений и их разрешения(#appendix-b-примеры-расхождений-и-их-разрешения)

  - Contents
  - Appendix B: Примеры расхождений и их разрешения
  - Упоминается в

_Слов: 292_

### [[12-content-overview|Content Overview]]
> > Что внутри: типы данных, приблизительный объём, основные темы.

  - Content Overview
  - Упоминается в
  - Связанные документы

_Слов: 113_

### [[120-главные-технические-риски|Главные технические риски]]
> > Два независимых анализа выделили разные приоритеты:

  - Главные технические риски
  - Упоминается в

_Слов: 101_

### [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]]
> > Первая формализация, основана на опыте применения к

  - Appendix C: История изменений методологии
  - Упоминается в

_Слов: 78_

### [[122-глоссарий|Глоссарий]]
> > !WARNING

  - Содержание
  - Глоссарий
  - Упоминается в
  - Связанные документы

_Слов: 1302_

### [[123-portal-mcp-py|portal-mcp.py]]
> > !IMPORTANT

  - Содержание
  - portal-mcp.py
- ============================================================
- MCP SDK imports
- ============================================================
- # We use the official MCP Python SDK. If not installed, user gets
- a clear error with install instructions.
- try:
  _... ещё 54 разделов_

_Слов: 2316_

### [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]]
> > После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигураци…

  - Конфигурация для Claude Desktop
  - Упоминается в
  - Связанные документы

_Слов: 212_

### [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]]
> > Отдельный документ для репо, объясняющий, как настроить MCP-обёртку:

  - README-MCP.md— инструкция по установке
- Nautilus Portal MCP Integration
  - Упоминается в
  - Связанные документы

_Слов: 152_

### [[126-установка|Установка]]
> - Установка(#установка)

  - Contents
  - Установка
- Ждёт stdio-input; Ctrl+C для выхода
  - Упоминается в
  - Связанные документы

_Слов: 169_

### [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]]
> - Подключение к Claude Desktop(#подключение-к-claude-desktop)

  - Contents
  - Подключение к Claude Desktop
  - Упоминается в
  - Связанные документы

_Слов: 173_

### [[128-доступные-инструменты|Доступные инструменты]]
> > После успешной интеграции Claude Desktop получает доступ к 7 tools:

  - Доступные инструменты
  - Упоминается в
  - Связанные документы

_Слов: 204_

### [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]]
> > После подключения Claude может использовать tools автоматически.

  - Примеры запросов (в Claude)
  - Упоминается в
  - Связанные документы

_Слов: 176_

### [[13-angle-perspective|Angle / Perspective]]
> > С какого угла Repo смотрит на общие концепты

  - Angle / Perspective
  - Упоминается в
  - Связанные документы

_Слов: 127_

### [[130-отладка|Отладка]]
> - Отладка(#отладка)

  - Contents
  - Отладка
  - Упоминается в
  - Связанные документы

_Слов: 205_

### [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]]
> > - Работает только в stdio mode (HTTP-mode планируется)

  - Ограничения текущей версии (0.1.0-draft)
  - Упоминается в
  - Связанные документы

_Слов: 133_

### [[132-planned-v0-2-0|Planned (v0.2.0)]]
> > - HTTP-mode для debugging и remote access

  - Planned (v0.2.0)
  - Упоминается в
  - Связанные документы

_Слов: 131_

### [[133-обратная-связь|Обратная связь]]
> > !TIP

  - Содержание
  - Обратная связь
- MCP интеграция (для Claude Desktop)
- Конфигурация: см. README-MCP.md
- В приватном репо cases-private:
  - Упоминается в
  - Связанные документы

_Слов: 16959_

### [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]]
> > - 187-слой-представительских-агентов-md(docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) (сходств…

  - THE DOUBLE-TRIANGLE ARCHITECTURE.md
- The Double-Triangle Architecture
  - Упоминается в
  - Связанные документы

_Слов: 130_

### [[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in Distributed Knowledge Work]]
> > Editorial review: Claude (intellectual collaboration, 2026-04)

  - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work
  - Упоминается в
  - Связанные документы

_Слов: 167_

### [[136-abstract|Abstract]]
> > We introduce the Double-Triangle Architecture for human-AI

  - Abstract
  - Упоминается в
  - Связанные документы

_Слов: 388_

### [[137-table-of-contents|Table of Contents]]
> > 1. Why Single-Triangle Models Are Incomplete

  - Table of Contents
  - Упоминается в
  - Связанные документы

_Слов: 172_

### [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 1. Why Single-Triangle Models Are Incomplete
  - Упоминается в
  - Связанные документы

_Слов: 583_

### [[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]]
> > !IMPORTANT

  - Содержание
  - 2. The Double-Triangle Architecture
- Bridges
  - Bridges
  - Упоминается в
  - Связанные документы

_Слов: 755_

### [[140-3-three-inter-layer-protocols|3. Three Inter-Layer Protocols]]
> > !IMPORTANT

  - Содержание
  - 3. Three Inter-Layer Protocols
  - Упоминается в
  - Связанные документы

_Слов: 868_

### [[141-4-nautilus-portal-as-reference-substrate|4. Nautilus Portal as Reference Substrate]]
> > The Double-Triangle Architecture requires a substrate capable of:

  - Содержание
  - 4. Nautilus Portal as Reference Substrate
  - Упоминается в
  - Связанные документы

_Слов: 675_

### [[142-5-pattern-library-as-bridge-between-triangles|5. Pattern Library as Bridge Between Triangles]]
> > !TIP

  - Содержание
  - 5. Pattern Library as Bridge Between Triangles
  - Упоминается в
  - Связанные документы

_Слов: 689_

### [[143-6-four-deployment-domains|6. Four Deployment Domains]]
> > The Double-Triangle Architecture is domain-agnostic but benefits

  - Содержание
  - 6. Four Deployment Domains
  - Упоминается в
  - Связанные документы

_Слов: 679_

### [[144-7-open-questions|7. Open Questions]]
> > !TIP

  - Содержание
  - 7. Open Questions
  - Упоминается в
  - Связанные документы

_Слов: 777_

### [[145-8-call-to-action|8. Call to Action]]
> > !TIP

  - Содержание
  - 8. Call to Action
  - Упоминается в
  - Связанные документы

_Слов: 746_

### [[146-acknowledgments|Acknowledgments]]
> > !TIP

  - Acknowledgments
  - Упоминается в
  - Связанные документы

_Слов: 273_

### [[147-references|References]]
> - References(#references)

  - Contents
  - References
  - Упоминается в
  - Связанные документы

_Слов: 350_

### [[148-appendix-a-glossary|Appendix A: Glossary]]
> > !TIP

  - Appendix A: Glossary
  - Упоминается в
  - Связанные документы

_Слов: 332_

### [[149-appendix-b-summary-of-contributions|Appendix B: Summary of Contributions]]
> > 1. Topological formalization of Double-Triangle Architecture

  - Appendix B: Summary of Contributions
- Author & Contact
  - Author & Contact
  - Упоминается в
  - Связанные документы

_Слов: 240_

### [[150-appendix-c-version-history|Appendix C: Version History]]
> > !WARNING

  - Содержание
  - Appendix C: Version History
  - Упоминается в
  - Связанные документы

_Слов: 8397_

### [[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]]
> > - 273-infrastructure-for-ai-collaborative-intellectual-w(docs/02-anthropic-vacancies/273-infrastructure-for-ai-collabo…

  - OPEN KNOWLEDGE WORK FOUNDATION.md
- Open Knowledge Work Foundation
  - Упоминается в
  - Связанные документы

_Слов: 126_

### [[152-ai-coordinated-infrastructure-for-distributed-expe|AI-Coordinated Infrastructure for Distributed Expert Contribution]]
> > Editorial collaboration: Claude (intellectual development, 2026-04)

  - AI-Coordinated Infrastructure for Distributed Expert Contribution
  - Упоминается в
  - Связанные документы

_Слов: 164_

### [[153-executive-summary|Executive Summary]]
> > The Open Knowledge Work Foundation (OKWF) proposes to build

  - Executive Summary
  - Упоминается в
  - Связанные документы

_Слов: 370_

### [[154-table-of-contents|Table of Contents]]
> > 3. Why Existing Solutions Fail

  - Table of Contents
  - Упоминается в
  - Связанные документы

_Слов: 140_

### [[155-1-problem-statement|1. Problem Statement]]
> > The AI industry in 2026 exhibits an apparent paradox. Frontier

  - Содержание
  - 1. Problem Statement
  - Упоминается в
  - Связанные документы

_Слов: 632_

### [[156-2-target-populations|2. Target Populations]]
> > Size estimate: 500K+ in OECD countries with relevant skills

  - Содержание
  - 2. Target Populations
  - Упоминается в
  - Связанные документы

_Слов: 683_

### [[157-3-why-existing-solutions-fail|3. Why Existing Solutions Fail]]
> > Seven existing infrastructure categories partially address the

  - Содержание
  - 3. Why Existing Solutions Fail
  - Упоминается в
  - Связанные документы

_Слов: 682_

### [[158-4-proposed-infrastructure|4. Proposed Infrastructure]]
> > !TIP

  - Содержание
  - 4. Proposed Infrastructure
  - Упоминается в
  - Связанные документы

_Слов: 1001_

### [[159-5-economic-model|5. Economic Model]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 5. Economic Model
  - Упоминается в
  - Связанные документы

_Слов: 654_

### [[16-history|History]]
> > Когда создан, ключевые версии, направление развития.

  - History
  - Упоминается в

_Слов: 104_

### [[160-6-governance-and-ethics|6. Governance and Ethics]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Governance and Ethics
  - Упоминается в
  - Связанные документы

_Слов: 595_

### [[161-7-phased-rollout-plan|7. Phased Rollout Plan]]
> > - Establish legal entity (non-profit foundation in Germany or

  - Содержание
  - 7. Phased Rollout Plan
  - Упоминается в
  - Связанные документы

_Слов: 663_

### [[162-8-risk-analysis|8. Risk Analysis]]
> > !TIP

  - Содержание
  - 8. Risk Analysis
  - Упоминается в
  - Связанные документы

_Слов: 653_

### [[163-9-call-for-partnership|9. Call for Partnership]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Call for Partnership
  - Упоминается в
  - Связанные документы

_Слов: 610_

### [[164-10-appendices|10. Appendices]]
> > Nautilus Portal Protocol v1.1:

  - Содержание
  - 10. Appendices
  - Упоминается в
  - Связанные документы

_Слов: 970_

### [[165-closing|Closing]]
> > !WARNING

  - Содержание
  - Closing
- unknownlegalconcepts.yml
  - Упоминается в
  - Связанные документы

_Слов: 9251_

### [[166-representative-agent-layer-md|REPRESENTATIVE AGENT LAYER.md]]
> > - 187-слой-представительских-агентов-md(docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) (сходств…

  - REPRESENTATIVE AGENT LAYER.md
- The Representative Agent Layer
  - Упоминается в
  - Связанные документы

_Слов: 130_

### [[167-ai-mediated-representation-for-underrepresented-ex|AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]
> > - Open Knowledge Work Foundation Concept Document v1.0

  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations
  - Упоминается в
  - Связанные документы

_Слов: 197_

### [[168-abstract|Abstract]]
> > We introduce the Representative Agent Layer — an architectural

  - Abstract
  - Упоминается в
  - Связанные документы

_Слов: 334_

### [[169-table-of-contents|Table of Contents]]
> > 1. The Cinderella Syndrome: Why Quality Stays Invisible

  - Table of Contents
  - Упоминается в
  - Связанные документы

_Слов: 167_

### [[17-5-compatibility-levels|5. Compatibility Levels]]
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Упоминается в
  - Связанные документы

_Слов: 300_

### [[170-1-the-cinderella-syndrome-why-quality-stays-invisi|1. The Cinderella Syndrome: Why Quality Stays Invisible]]
> > There is a recurring asymmetry in modern markets — markets for

  - Содержание
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible
  - Упоминается в
  - Связанные документы

_Слов: 828_

### [[171-2-historical-precedents-agents-as-civilizational-i|2. Historical Precedents: Agents as Civilizational Innovation]]
> > The pattern of representative agents is ancient and recurring.

  - Содержание
  - 2. Historical Precedents: Agents as Civilizational Innovation
  - Упоминается в
  - Связанные документы

_Слов: 973_

### [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]]
> > A Representative Agent is distinct from existing AI categories.

  - Содержание
  - 3. What Makes a Representative Agent
  - Упоминается в
  - Связанные документы

_Слов: 681_

### [[173-4-ten-domains-of-application|4. Ten Domains of Application]]
> > !TIP

  - Содержание
  - 4. Ten Domains of Application
  - Упоминается в

_Слов: 1549_

### [[174-5-architectural-specification|5. Architectural Specification]]
> > A Representative Agent system consists of seven components:

  - Содержание
  - 5. Architectural Specification
  - Упоминается в
  - Связанные документы

_Слов: 665_

### [[175-6-ethical-framework|6. Ethical Framework]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Ethical Framework
  - Упоминается в
  - Связанные документы

_Слов: 611_

### [[176-7-governance-and-oversight|7. Governance and Oversight]]
> - 7. Governance and Oversight(#7-governance-and-oversight)

  - Contents
  - 7. Governance and Oversight
  - Упоминается в
  - Связанные документы

_Слов: 472_

### [[177-8-risks-and-mitigations|8. Risks and Mitigations]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Risks and Mitigations
  - Упоминается в
  - Связанные документы

_Слов: 666_

### [[178-9-phased-rollout-strategy|9. Phased Rollout Strategy]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Phased Rollout Strategy
  - Упоминается в
  - Связанные документы

_Слов: 636_

### [[179-10-open-questions|10. Open Questions]]
> - 10. Open Questions(#10-open-questions)

  - Contents
  - 10. Open Questions
  - Упоминается в
  - Связанные документы

_Слов: 446_

### [[18-6-adapter-interface|6. Adapter Interface]]
> - 6. Adapter Interface(#6-adapter-interface)

  - Contents
  - 6. Adapter Interface
  - Упоминается в
  - Связанные документы

_Слов: 425_

### [[180-11-call-for-collaboration|11. Call for Collaboration]]
> - 11. Call for Collaboration(#11-call-for-collaboration)

  - Contents
  - 11. Call for Collaboration
  - Упоминается в
  - Связанные документы

_Слов: 447_

### [[181-12-closing|12. Closing]]
> > The Cinderella Syndrome — quality without visibility —

  - 12. Closing
  - Упоминается в
  - Связанные документы

_Слов: 281_

### [[182-acknowledgments|Acknowledgments]]
> > !TIP

  - Acknowledgments
  - Упоминается в
  - Связанные документы

_Слов: 245_

### [[183-references|References]]
> - References(#references)

  - Contents
  - References
  - Упоминается в
  - Связанные документы

_Слов: 322_

### [[184-appendix-a-connection-to-companion-papers|Appendix A: Connection to Companion Papers]]
> > This paper builds on three previous documents:

  - Appendix A: Connection to Companion Papers
  - Упоминается в
  - Связанные документы

_Слов: 240_

### [[185-appendix-b-domain-comparison-matrix|Appendix B: Domain Comparison Matrix]]
> > - Вакансии Anthropic — Анализ по кластерам(docs/02-anthropic-vacancies/README.md)

  - Appendix B: Domain Comparison Matrix
  - Упоминается в

_Слов: 198_

### [[186-appendix-c-sample-use-cases-in-detail|Appendix C: Sample Use Cases in Detail]]
> > !TIP

  - Содержание
  - Appendix C: Sample Use Cases in Detail
  - Упоминается в
  - Связанные документы

_Слов: 2024_

### [[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]]
> > - 166-representative-agent-layer-md(docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) (сходство 0.33)

  - СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md
- Слой Представительских Агентов
  - Упоминается в
  - Связанные документы

_Слов: 126_

### [[188-ai-опосредованное-представительство-для-недопредст|AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения]]
> > Сопроводительный документ к:

  - AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения
  - Упоминается в
  - Связанные документы

_Слов: 164_

### [[189-аннотация|Аннотация]]
> > Мы представляем Слой Представительских Агентов — архитектурный паттерн, в котором AI-системы выступают проактивными пр…

  - Аннотация
  - Упоминается в

_Слов: 281_

### [[19-7-portalentry-structure|7. PortalEntry Structure]]
> > !IMPORTANT

  - 7. PortalEntry Structure
  - Упоминается в
  - Связанные документы

_Слов: 260_

### [[190-содержание|Содержание]]
> > 1. Синдром Золушки: Почему качество остаётся невидимым

  - Содержание
  - Упоминается в
  - Связанные документы

_Слов: 151_

### [[191-1-синдром-золушки-почему-качество-остаётся-невидим|1. Синдром Золушки: Почему качество остаётся невидимым]]
> > Существует повторяющаяся асимметрия на современных рынках — рынках труда, внимания, возможностей, услуг. Качество и ви…

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым
  - Упоминается в
  - Связанные документы

_Слов: 751_

### [[192-2-исторические-прецеденты-агенты-как-цивилизационн|2. Исторические прецеденты: Агенты как цивилизационная инновация]]
> > !WARNING

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация
  - Упоминается в

_Слов: 900_

### [[193-3-что-делает-агента-представительским|3. Что делает агента Представительским]]
> > Представительский Агент отличается от существующих категорий AI. Мы определяем это точно.

  - Содержание
  - 3. Что делает агента Представительским
  - Упоминается в
  - Связанные документы

_Слов: 625_

### [[194-4-десять-областей-применения|4. Десять областей применения]]
> > !WARNING

  - Содержание
  - 4. Десять областей применения
  - Упоминается в
  - Связанные документы

_Слов: 1582_

### [[195-5-архитектурная-спецификация|5. Архитектурная спецификация]]
> > Система Представительского Агента состоит из семи компонентов:

  - Содержание
  - 5. Архитектурная спецификация
  - Упоминается в
  - Связанные документы

_Слов: 625_

### [[196-6-этическая-рамка|6. Этическая рамка]]
> > !IMPORTANT

  - Contents
  - 6. Этическая рамка
  - Упоминается в

_Слов: 492_

### [[197-7-управление-и-надзор|7. Управление и надзор]]
> - 7. Управление и надзор(#7-управление-и-надзор)

  - Contents
  - 7. Управление и надзор
  - Упоминается в

_Слов: 399_

### [[198-8-риски-и-меры-противодействия|8. Риски и меры противодействия]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Риски и меры противодействия
  - Упоминается в
  - Связанные документы

_Слов: 634_

### [[199-9-стратегия-поэтапного-развёртывания|9. Стратегия поэтапного развёртывания]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Стратегия поэтапного развёртывания
  - Упоминается в

_Слов: 596_

### [[20-8-consensus-algorithm|8. Consensus Algorithm]]
> - 8. Consensus Algorithm(#8-consensus-algorithm)

  - Contents
  - 8. Consensus Algorithm
  - Упоминается в
  - Связанные документы

_Слов: 302_

### [[200-10-открытые-вопросы|10. Открытые вопросы]]
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Упоминается в

_Слов: 366_

### [[201-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]]
> - 11. Призыв к сотрудничеству(#11-призыв-к-сотрудничеству)

  - Contents
  - 11. Призыв к сотрудничеству
  - Упоминается в

_Слов: 414_

### [[202-12-заключение|12. Заключение]]
> > Синдром Золушки — качество без видимости — не нов. Он формировал человеческий труд и признание задолго до компьютеров.…

  - 12. Заключение
  - Упоминается в

_Слов: 216_

### [[203-благодарности|Благодарности]]
> > Эта концепция возникла через диалог в нескольких сессиях в 2026 году. Формулировка «Синдром Золушки» и расширение к со…

  - Благодарности
  - Упоминается в
  - Связанные документы

_Слов: 191_

### [[204-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Упоминается в
  - Связанные документы

_Слов: 306_

### [[205-приложение-a-связь-с-сопроводительными-статьями|Приложение A: Связь с Сопроводительными Статьями]]
> > Эта статья опирается на три предыдущих документа:

  - Приложение A: Связь с Сопроводительными Статьями
  - Упоминается в
  - Связанные документы

_Слов: 211_

### [[206-приложение-b-матрица-сравнения-областей|Приложение B: Матрица Сравнения Областей]]
> > - Вакансии Anthropic — Анализ по кластерам(docs/02-anthropic-vacancies/README.md)

  - Приложение B: Матрица Сравнения Областей
  - Упоминается в
  - Связанные документы

_Слов: 212_

### [[207-приложение-c-образцы-случаев-использования-в-детал|Приложение C: Образцы Случаев Использования в Деталях]]
> > !TIP

  - Содержание
  - Приложение C: Образцы Случаев Использования в Деталях
  - Упоминается в
  - Связанные документы

_Слов: 4049_

### [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]]
> > - 249-composite-skills-agent-md(docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) (сходство 0.14)

  - PROFESSIONAL COLLEAGUE AGENTS.md
- Professional Colleague Agents
  - Упоминается в
  - Связанные документы

_Слов: 128_

### [[209-a-typology-of-ai-agents-on-the-principal-side-and-|A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers]]
> > - Representative Agent Layer v1.0

  - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers
  - Упоминается в
  - Связанные документы

_Слов: 197_

### [[21-9-query-flow|9. Query Flow]]
> - 9. Query Flow(#9-query-flow)

  - Contents
  - 9. Query Flow
  - Упоминается в
  - Связанные документы

_Слов: 237_

### [[210-abstract|Abstract]]
> > Building on the Representative Agent Layer paper, we observe

  - Abstract
  - Упоминается в
  - Связанные документы

_Слов: 349_

### [[211-table-of-contents|Table of Contents]]
> > 1. The Five-Type Typology of Principal-Side Agents

  - Table of Contents
  - Упоминается в
  - Связанные документы

_Слов: 196_

### [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]]
> > The Representative Agent Layer paper introduced one type of AI

  - Содержание
  - 1. The Five-Type Typology of Principal-Side Agents
  - Упоминается в
  - Связанные документы

_Слов: 930_

### [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]]
> > We now develop Type 1 in detail.

  - Содержание
  - 2. What Makes a Professional Colleague Agent
  - Упоминается в
  - Связанные документы

_Слов: 845_

### [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]]
> > We document a successfully deployed Professional Colleague

  - Содержание
  - 3. Empirical Case Study: «Обучай»
  - Упоминается в
  - Связанные документы

_Слов: 855_

### [[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Agents]]
> > A Professional Colleague Agent has three distinct internal

  - Содержание
  - 4. Architecture of Professional Colleague Agents
  - Упоминается в
  - Связанные документы

_Слов: 901_

### [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replication]]
> > A defining feature of Professional Colleague Agents is that

  - Содержание
  - 5. The Economics of Profession-Wide Replication
  - Упоминается в
  - Связанные документы

_Слов: 753_

### [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]]
> > !TIP

  - Содержание
  - 6. Risks Specific to this Category
  - Упоминается в
  - Связанные документы

_Слов: 1209_

### [[218-7-application-domains|7. Application Domains]]
> > !TIP

  - Содержание
  - 7. Application Domains
  - Упоминается в
  - Связанные документы

_Слов: 743_

### [[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]]
> > We now apply the Professional Colleague Agent framework to a

  - Содержание
  - 8. Pilot Proposal: SGB Advocate Colleague
  - Упоминается в
  - Связанные документы

_Слов: 978_

### [[22-10-queryresult-structure|10. QueryResult Structure]]
> > resultsbyrepo: dictstr, listPortalEntry

  - 10. QueryResult Structure
  - Упоминается в
  - Связанные документы

_Слов: 195_

### [[220-9-relationship-to-other-agent-types|9. Relationship to Other Agent Types]]
> > Professional Colleague Agents do not stand alone. They

  - Содержание
  - 9. Relationship to Other Agent Types
  - Упоминается в
  - Связанные документы

_Слов: 677_

### [[221-10-open-questions|10. Open Questions]]
> - 10. Open Questions(#10-open-questions)

  - Contents
  - 10. Open Questions
  - Упоминается в
  - Связанные документы

_Слов: 460_

### [[222-11-call-for-collaboration|11. Call for Collaboration]]
> - 11. Call for Collaboration(#11-call-for-collaboration)

  - Contents
  - 11. Call for Collaboration
  - Упоминается в
  - Связанные документы

_Слов: 411_

### [[223-12-closing|12. Closing]]
> > The Representative Agent Layer paper, when first written,

  - 12. Closing
  - Упоминается в
  - Связанные документы

_Слов: 409_

### [[224-acknowledgments|Acknowledgments]]
> > This paper emerged through dialogue with Claude (Anthropic)

  - Acknowledgments
  - Упоминается в
  - Связанные документы

_Слов: 219_

### [[225-references|References]]
> - References(#references)

  - Contents
  - References
  - Упоминается в
  - Связанные документы

_Слов: 351_

### [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Types]]
> > - 269-appendix-a-the-six-type-taxonomy-updated(docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-update…

  - Appendix A: Comparative Table — Five Agent Types
  - Упоминается в
  - Связанные документы

_Слов: 392_

### [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Build Type 1 First]]
> > For an organization deciding whether to build a Professional

  - Appendix B: Decision Framework — When to Build Type 1 First
  - Упоминается в
  - Связанные документы

_Слов: 332_

### [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]]
> > !IMPORTANT

  - Содержание
  - Appendix C: Quick-Start Architecture for SGB Advocate Colleague
  - Упоминается в
  - Связанные документы

_Слов: 1730_

### [[229-профессиональные-коллеги-агенты|ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ]]
> > Сопроводительный документ к:

  - ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ
  - Упоминается в
  - Связанные документы

_Слов: 174_

### [[23-11-security-considerations|11. Security Considerations]]
> - 11. Security Considerations(#11-security-considerations)

  - Contents
  - 11. Security Considerations
  - Упоминается в
  - Связанные документы

_Слов: 248_

### [[230-аннотация|Аннотация]]
> > Развивая статью «Слой Представительских Агентов»,

  - Аннотация
  - Упоминается в
  - Связанные документы

_Слов: 310_

### [[231-содержание|Содержание]]
> > 1. Типология из пяти типов агентов на стороне

  - Содержание
  - Упоминается в
  - Связанные документы

_Слов: 173_

### [[232-1-типология-из-пяти-типов-агентов-на-стороне-принц|1. Типология из пяти типов агентов на стороне принципала]]
> > !IMPORTANT

  - Содержание
  - 1. Типология из пяти типов агентов на стороне принципала
  - Упоминается в
  - Связанные документы

_Слов: 885_

### [[233-2-что-делает-агента-профессиональным-коллегой|2. Что делает агента Профессиональным Коллегой]]
> > Теперь развиваем Тип 1 в деталях.

  - Содержание
  - 2. Что делает агента Профессиональным Коллегой
  - Упоминается в
  - Связанные документы

_Слов: 749_

### [[234-3-эмпирический-кейс-обучай|3. Эмпирический кейс: «Обучай»]]
> > !WARNING

  - Содержание
  - 3. Эмпирический кейс: «Обучай»
  - Упоминается в
  - Связанные документы

_Слов: 782_

### [[235-4-архитектура-профессиональных-коллег-агентов|4. Архитектура Профессиональных Коллег-Агентов]]
> > !WARNING

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов
  - Упоминается в
  - Связанные документы

_Слов: 823_

### [[236-5-экономика-тиражирования-по-профессии|5. Экономика тиражирования по профессии]]
> > Определяющая черта Профессиональных

  - Содержание
  - 5. Экономика тиражирования по профессии
  - Упоминается в
  - Связанные документы

_Слов: 714_

### [[237-6-риски-специфичные-для-этой-категории|6. Риски, специфичные для этой категории]]
> > !WARNING

  - Содержание
  - 6. Риски, специфичные для этой категории
  - Упоминается в
  - Связанные документы

_Слов: 1125_

### [[238-7-области-применения|7. Области применения]]
> > !WARNING

  - Содержание
  - 7. Области применения
  - Упоминается в

_Слов: 683_

### [[239-8-пилотное-предложение-sgb-колega-адвокат|8. Пилотное предложение: SGB Колega-Адвокат]]
> > !WARNING

  - Содержание
  - 8. Пилотное предложение: SGB Колega-Адвокат
  - Упоминается в
  - Связанные документы

_Слов: 974_

### [[24-12-versioning-policy|12. Versioning Policy]]
> - 12. Versioning Policy(#12-versioning-policy)

  - Contents
  - 12. Versioning Policy
  - Упоминается в
  - Связанные документы

_Слов: 237_

### [[240-9-связь-с-другими-типами-агентов|9. Связь с другими типами агентов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Связь с другими типами агентов
  - Упоминается в
  - Связанные документы

_Слов: 707_

### [[241-10-открытые-вопросы|10. Открытые вопросы]]
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Упоминается в

_Слов: 364_

### [[242-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]]
> - 11. Призыв к сотрудничеству(#11-призыв-к-сотрудничеству)

  - Contents
  - 11. Призыв к сотрудничеству
  - Упоминается в

_Слов: 325_

### [[243-12-заключение|12. Заключение]]
> > Статья «Слой Представительских Агентов», когда

  - 12. Заключение
  - Упоминается в
  - Связанные документы

_Слов: 375_

### [[244-благодарности|Благодарности]]
> > Эта статья возникла через диалог с Claude

  - Благодарности
  - Упоминается в
  - Связанные документы

_Слов: 193_

### [[245-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Упоминается в
  - Связанные документы

_Слов: 331_

### [[246-приложение-a-сравнительная-таблица-пять-типов-аген|Приложение A: Сравнительная Таблица — Пять Типов Агентов]]
> > - 232-1-типология-из-пяти-типов-агентов-на-стороне-принц(docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-аге…

  - Приложение A: Сравнительная Таблица — Пять Типов Агентов
  - Упоминается в
  - Связанные документы

_Слов: 367_

### [[247-приложение-b-рамка-принятия-решений-когда-строить-|Приложение B: Рамка принятия решений — когда строить Тип 1 первым]]
> > Для организации, решающей, строить ли

  - Приложение B: Рамка принятия решений — когда строить Тип 1 первым
  - Упоминается в
  - Связанные документы

_Слов: 250_

### [[248-приложение-c-архитектура-быстрого-старта-для-sgb-а|Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги]]
> > !WARNING

  - Содержание
  - Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги
  - Упоминается в
  - Связанные документы

_Слов: 3425_

### [[249-composite-skills-agent-md|COMPOSITE SKILLS AGENT.md]]
> > - 166-representative-agent-layer-md(docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) (сходство 0.25)

  - COMPOSITE SKILLS AGENT.md
- The Composite Skills Agent
  - Упоминается в
  - Связанные документы

_Слов: 125_

### [[25-13-reference-implementation|13. Reference Implementation]]
> > Reference implementation: github.com/svend4/nautilus.

  - 13. Reference Implementation
  - Упоминается в
  - Связанные документы

_Слов: 153_

### [[250-bridging-the-gap-between-profession-wide-and-indiv|Bridging the Gap Between Profession-Wide and Individual-Unique]]
  - Bridging the Gap Between Profession-Wide and Individual-Unique

_Слов: 16_

### [[251-ai-support-through-configurable-specialist-ensembl|AI Support Through Configurable Specialist Ensembles]]
> > - Professional Colleague Agents v1.0

  - AI Support Through Configurable Specialist Ensembles
  - Упоминается в
  - Связанные документы

_Слов: 193_

### [[252-abstract|Abstract]]
> > The five-type taxonomy introduced in Professional Colleague

  - Abstract
  - Упоминается в
  - Связанные документы

_Слов: 347_

### [[253-table-of-contents|Table of Contents]]
> > 1. Why the Binary View Is Incomplete

  - Table of Contents
  - Упоминается в
  - Связанные документы

_Слов: 189_

### [[254-1-why-the-binary-view-is-incomplete|1. Why the Binary View Is Incomplete]]
> > Professional Colleague Agents (PCA) v1.0 introduced five types

  - Содержание
  - 1. Why the Binary View Is Incomplete
  - Упоминается в
  - Связанные документы

_Слов: 698_

### [[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]]
> > !TIP

  - Содержание
  - 2. The Twenty-One Teachers Pattern
  - Упоминается в
  - Связанные документы

_Слов: 844_

### [[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]]
> > We define the type with precision.

  - Содержание
  - 3. What Makes a Composite Skills Agent
  - Упоминается в
  - Связанные документы

_Слов: 946_

### [[257-4-the-sub-agent-registry|4. The Sub-Agent Registry]]
> > !TIP

  - Содержание
  - 4. The Sub-Agent Registry
  - Упоминается в
  - Связанные документы

_Слов: 803_

### [[258-5-configuration-how-principals-build-their-ensembl|5. Configuration: How Principals Build Their Ensembles]]
> > A central question for Composite Skills Agents: how does a

  - Содержание
  - 5. Configuration: How Principals Build Their Ensembles
  - Упоминается в
  - Связанные документы

_Слов: 745_

### [[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]]
> > The composite agent's most subtle function is coordinating

  - Содержание
  - 6. Coordination and Disagreement Resolution
  - Упоминается в
  - Связанные документы

_Слов: 804_

### [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]
> > Context: При построении системы knowledge management встаёт

  - 14. ADR-001: Federation over Merging
  - Упоминается в
  - Связанные документы

_Слов: 232_

### [[260-7-economics-of-combinatorial-replication|7. Economics of Combinatorial Replication]]
> > The economics of Composite Skills Agents differ from both

  - Содержание
  - 7. Economics of Combinatorial Replication
  - Упоминается в
  - Связанные документы

_Слов: 790_

### [[261-8-seven-domains-of-application|8. Seven Domains of Application]]
> > !TIP

  - Содержание
  - 8. Seven Domains of Application
  - Упоминается в
  - Связанные документы

_Слов: 1014_

### [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]]
> > !TIP

  - Содержание
  - 9. Integration with OKWF Infrastructure
  - Упоминается в
  - Связанные документы

_Слов: 750_

### [[263-10-risks-specific-to-composite-architectures|10. Risks Specific to Composite Architectures]]
> > !TIP

  - Содержание
  - 10. Risks Specific to Composite Architectures
  - Упоминается в
  - Связанные документы

_Слов: 788_

### [[264-11-open-questions|11. Open Questions]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 11. Open Questions
  - Упоминается в
  - Связанные документы

_Слов: 638_

### [[265-12-call-for-collaboration|12. Call for Collaboration]]
> - 12. Call for Collaboration(#12-call-for-collaboration)

  - Contents
  - 12. Call for Collaboration
  - Упоминается в
  - Связанные документы

_Слов: 447_

### [[266-13-closing|13. Closing]]
> > Mastery in skilled work has always been composite. The yoga

  - 13. Closing
  - Упоминается в
  - Связанные документы

_Слов: 434_

### [[267-acknowledgments|Acknowledgments]]
> > The Composite Skills Agent concept emerged from dialogue with

  - Acknowledgments
  - Упоминается в
  - Связанные документы

_Слов: 297_

### [[268-references|References]]
> - References(#references)

  - Contents
  - References
  - Упоминается в
  - Связанные документы

_Слов: 416_

### [[269-appendix-a-the-six-type-taxonomy-updated|Appendix A: The Six-Type Taxonomy (Updated)]]
> > This paper updates the Professional Colleague Agents v1.0

  - Appendix A: The Six-Type Taxonomy (Updated)
  - Упоминается в
  - Связанные документы

_Слов: 289_

### [[27-15-glossary-of-examples|15. Glossary of Examples]]
> > В качестве иллюстраций используется экосистема svend4 с тремя

  - 15. Glossary of Examples
  - Упоминается в
  - Связанные документы

_Слов: 149_

### [[270-appendix-b-sub-agent-registry-schema-sketch|Appendix B: Sub-Agent Registry Schema (Sketch)]]
> > For implementation, sub-agent registry entries might follow

  - Appendix B: Sub-Agent Registry Schema (Sketch)
  - Упоминается в
  - Связанные документы

_Слов: 317_

### [[271-appendix-c-configuration-template-example|Appendix C: Configuration Template Example]]
> > For the SGB Advocate Colleague pilot, a starting configuration

  - Appendix C: Configuration Template Example
  - Упоминается в
  - Связанные документы

_Слов: 310_

### [[272-appendix-d-connection-diagram|Appendix D: Connection Diagram]]
> > !WARNING

  - Содержание
  - Appendix D: Connection Diagram
  - Упоминается в
  - Связанные документы

_Слов: 3851_

### [[273-infrastructure-for-ai-collaborative-intellectual-w|INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md]]
> > - 151-open-knowledge-work-foundation-md(docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md) (сходств…

  - INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md
- Infrastructure for AI-Collaborative Intellectual Work
  - Упоминается в
  - Связанные документы

_Слов: 128_

### [[274-the-missing-middle-layer-between-chat-and-code|The Missing Middle Layer Between Chat and Code]]
> > Document type: Inquiry paper, not architectural specification

  - The Missing Middle Layer Between Chat and Code
  - Упоминается в
  - Связанные документы

_Слов: 260_

### [[275-why-this-document-exists|Why This Document Exists]]
> > The seven preceding documents in this series were produced in

  - Why This Document Exists
  - Упоминается в
  - Связанные документы

_Слов: 350_

### [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]]
> > !TIP

  - The Two-Layer Stack As It Exists
  - Упоминается в
  - Связанные документы

_Слов: 406_

### [[277-what-s-missing-layer-b|What's Missing — Layer B]]
> > Between chat and repository, there should exist Layer B: an

  - What's Missing — Layer B
  - Упоминается в
  - Связанные документы

_Слов: 477_

### [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]]
> > Several explanations for the gap.

  - Why This Hasn't Been Built
  - Упоминается в
  - Связанные документы

_Слов: 378_

### [[279-existing-approximations|Existing Approximations]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Existing Approximations
  - Упоминается в
  - Связанные документы

_Слов: 588_

### [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> - Appendix A: Minimal Working Example(#appendix-a-minimal-working-example)

  - Contents
  - Appendix A: Minimal Working Example
- mynotes
  - Упоминается в
  - Связанные документы

_Слов: 235_

### [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]]
> > The seven documents produced in this session have specific

  - Содержание
  - The Specific Case in Front of Us
  - Упоминается в
  - Связанные документы

_Слов: 674_

### [[281-the-recursive-insight|The Recursive Insight]]
> > There is something subtle in all this that warrants explicit

  - The Recursive Insight
  - Упоминается в
  - Связанные документы

_Слов: 371_

### [[282-what-industry-will-likely-build|What Industry Will Likely Build]]
> > Independent of what the author does, the industry will move

  - What Industry Will Likely Build
  - Упоминается в
  - Связанные документы

_Слов: 325_

### [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]]
> > This document identifies a problem. It does not propose a

  - What This Document Doesn't Solve
  - Упоминается в
  - Связанные документы

_Слов: 259_

### [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]]
> > For the seven-document Nautilus / OKWF project specifically,

  - Practical Recommendations for the Current Project
  - Упоминается в
  - Связанные документы

_Слов: 386_

### [[285-closing|Closing]]
> > The seven documents in this series describe substantial

  - Closing
  - Упоминается в
  - Связанные документы

_Слов: 270_

### [[286-acknowledgments|Acknowledgments]]
> > This document emerged from the author's observation, near

  - Acknowledgments
  - Упоминается в
  - Связанные документы

_Слов: 263_

### [[287-references|References]]
> - References(#references)

  - Contents
  - References
  - Упоминается в
  - Связанные документы

_Слов: 295_

### [[288-appendix-position-in-series-visualization|Appendix: Position in Series Visualization]]
> > Document 1: Nautilus Portal Protocol

  - Содержание
  - Appendix: Position in Series Visualization
  - Упоминается в
  - Связанные документы

_Слов: 1078_

### [[289-инфраструктура-для-ai-совместной-интеллектуальной-|ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ]]
> > Тип документа: Исследовательская статья,

  - ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ
- Essence
  - Essence
  - Упоминается в
  - Связанные документы

_Слов: 251_

### [[290-почему-этот-документ-существует|Почему этот документ существует]]
> > Семь предыдущих документов в этой серии были

  - Почему этот документ существует
  - Упоминается в
  - Связанные документы

_Слов: 291_

### [[291-двухслойный-стек-как-он-существует|Двухслойный стек, как он существует]]
> > В настоящее время AI-совместная работа

  - Двухслойный стек, как он существует
  - Упоминается в
  - Связанные документы

_Слов: 338_

### [[292-что-отсутствует-слой-b|Что отсутствует — Слой B]]
> > Между чатом и репозиторием должен существовать

  - Что отсутствует — Слой B
  - Упоминается в
  - Связанные документы

_Слов: 419_

### [[293-почему-это-не-было-построено|Почему это не было построено]]
> > Объяснение 1 — Это сложнее, чем выглядит.

  - Почему это не было построено
  - Упоминается в
  - Связанные документы

_Слов: 313_

### [[294-существующие-приближения|Существующие приближения]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Существующие приближения
  - Упоминается в
  - Связанные документы

_Слов: 565_

### [[295-конкретный-случай-перед-нами|Конкретный случай перед нами]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Конкретный случай перед нами
  - Упоминается в
  - Связанные документы

_Слов: 666_

### [[296-рекурсивное-прозрение|Рекурсивное прозрение]]
> > Есть нечто тонкое во всём этом, что заслуживает

  - Рекурсивное прозрение
  - Упоминается в
  - Связанные документы

_Слов: 316_

### [[297-что-промышленность-вероятно-построит|Что промышленность вероятно построит]]
> > !WARNING

  - Что промышленность вероятно построит
  - Упоминается в
  - Связанные документы

_Слов: 293_

### [[298-что-этот-документ-не-решает|Что этот документ не решает]]
> > !WARNING

  - Что этот документ не решает
  - Упоминается в
  - Связанные документы

_Слов: 201_

### [[299-практические-рекомендации-для-текущего-проекта|Практические рекомендации для текущего проекта]]
> > Для конкретного семидокументного проекта

  - Практические рекомендации для текущего проекта
- Native Format
  - Native Format
  - Упоминается в
  - Связанные документы

_Слов: 335_

### [[300-заключение|Заключение]]
> > Семь документов в этой серии описывают

  - Заключение
  - Упоминается в
  - Связанные документы

_Слов: 239_

### [[301-благодарности|Благодарности]]
> > Этот документ возник из наблюдения автора, в

  - Благодарности
  - Упоминается в
  - Связанные документы

_Слов: 231_

### [[302-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Упоминается в
  - Связанные документы

_Слов: 239_

### [[303-приложение-визуализация-позиции-в-серии|Приложение: Визуализация позиции в серии]]
> > !TIP

  - Содержание
  - Приложение: Визуализация позиции в серии
  - Упоминается в
  - Связанные документы

_Слов: 7108_

### [[304-ingit-as-cowork-native-workspace-substrate-md|INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]]
> > - 249-composite-skills-agent-md(docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) (сходство 0.11)

  - INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md
- InGit as Cowork-Native Workspace Substrate
  - Упоминается в
  - Связанные документы

_Слов: 133_

### [[305-a-practical-path-to-layer-b-through-symbiotic-inte|A Practical Path to Layer B Through Symbiotic Integration]]
> > - 166-representative-agent-layer-md(docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) (сходство 0.27)

  - A Practical Path to Layer B Through Symbiotic Integration
  - Упоминается в
  - Связанные документы

_Слов: 122_

### [[306-with-anthropic-s-cowork-platform|with Anthropic's Cowork Platform]]
> > Document type: Practical implementation paper, building

  - with Anthropic's Cowork Platform
  - Упоминается в
  - Связанные документы

_Слов: 282_

### [[307-abstract|Abstract]]
> > Document 2.3 identified Layer B — the missing infrastructure

  - Abstract
  - Упоминается в
  - Связанные документы

_Слов: 323_

### [[308-table-of-contents|Table of Contents]]
> > 1. The Cowork Discovery and Why It Changes Everything

  - Table of Contents
  - Упоминается в
  - Связанные документы

_Слов: 206_

### [[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Everything]]
> > When Document 2.3 was written earlier in this session, the

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything
  - Упоминается в
  - Связанные документы

_Слов: 698_

### [[31-content-overview|Content Overview]]
> > ~200 заметок, темы: software engineering, philosophy, music.

  - Content Overview
  - Упоминается в
  - Связанные документы

_Слов: 113_

### [[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-|2. What Cowork Provides That InGit Doesn't Need to Build]]
> > If InGit positions to complement Cowork rather than replace

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build
  - Упоминается в
  - Связанные документы

_Слов: 678_

### [[311-3-what-ingit-provides-that-cowork-lacks|3. What InGit Provides That Cowork Lacks]]
> > Equally important: where does InGit add value that Cowork

  - Содержание
  - 3. What InGit Provides That Cowork Lacks
  - Упоминается в
  - Связанные документы

_Слов: 867_

### [[312-4-the-symbiotic-architecture|4. The Symbiotic Architecture]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 4. The Symbiotic Architecture
  - Упоминается в
  - Связанные документы

_Слов: 678_

### [[313-5-four-integration-paths-in-order-of-accessibility|5. Four Integration Paths in Order of Accessibility]]
> > We identify four paths from most-immediate to most-mature.

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility
  - Упоминается в
  - Связанные документы

_Слов: 810_

### [[314-6-refined-ingit-scope-with-cowork-in-mind|6. Refined InGit Scope with Cowork in Mind]]
> > !TIP

  - Contents
  - 6. Refined InGit Scope with Cowork in Mind
  - Упоминается в
  - Связанные документы

_Слов: 513_

### [[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]]
> - 7. Practical First Steps This Month(#7-practical-first-steps-this-month)

  - Contents
  - 7. Practical First Steps This Month
  - Упоминается в
  - Связанные документы

_Слов: 479_

### [[316-8-implications-for-nautilus-and-okwf|8. Implications for Nautilus and OKWF]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Implications for Nautilus and OKWF
  - Упоминается в
  - Связанные документы

_Слов: 696_

### [[317-9-risks-and-open-questions|9. Risks and Open Questions]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Risks and Open Questions
  - Упоминается в
  - Связанные документы

_Слов: 653_

### [[318-10-strategic-positioning|10. Strategic Positioning]]
> > Closing thoughts on broader strategic implications.

  - Содержание
  - 10. Strategic Positioning
  - Упоминается в
  - Связанные документы

_Слов: 749_

### [[319-acknowledgments|Acknowledgments]]
> > This document emerged from author's question about how to

  - Acknowledgments
- Angle / Perspective
  - Angle / Perspective
  - Упоминается в
  - Связанные документы

_Слов: 384_

### [[320-references|References]]
> - References(#references)

  - Contents
  - References
  - Упоминается в
  - Связанные документы

_Слов: 199_

### [[321-appendix-a-decision-tree-for-ingit-adopters|Appendix A: Decision Tree for InGit Adopters]]
> > Quick reference for users evaluating InGit + Cowork:

  - Appendix A: Decision Tree for InGit Adopters
  - Упоминается в
  - Связанные документы

_Слов: 241_

### [[322-appendix-b-comparison-matrix|Appendix B: Comparison Matrix]]
> > InGit + Cowork's distinct profile: maximum structure with full

  - Appendix B: Comparison Matrix
  - Упоминается в
  - Связанные документы

_Слов: 279_

### [[323-appendix-c-sample-ingit-mcp-server-tool-specificat|Appendix C: Sample InGit MCP Server Tool Specifications]]
> > For reference, here are detailed specifications for first

  - Содержание
  - Appendix C: Sample InGit MCP Server Tool Specifications
  - Упоминается в
  - Связанные документы

_Слов: 1570_

### [[324-ingit-как-cowork-интегрированная-подложка-рабочего|INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА]]
> > Тип документа: Практическая статья по

  - INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА
  - Упоминается в
  - Связанные документы

_Слов: 288_

### [[325-аннотация|Аннотация]]
> > Документ 2.3 определил Слой B — отсутствующую

  - Аннотация
  - Упоминается в
  - Связанные документы

_Слов: 317_

### [[326-содержание|Содержание]]
> > 1. Открытие Cowork и почему это меняет всё

  - Содержание
  - Упоминается в
  - Связанные документы

_Слов: 178_

### [[327-1-открытие-cowork-и-почему-это-меняет-всё|1. Открытие Cowork и почему это меняет всё]]
> > Когда Документ 2.3 был написан ранее в этой

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё
  - Упоминается в
  - Связанные документы

_Слов: 662_

### [[328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи|2. Что Cowork обеспечивает, что InGit не нужно строить]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 2. Что Cowork обеспечивает, что InGit не нужно строить
  - Упоминается в
  - Связанные документы

_Слов: 713_

### [[329-3-что-ingit-обеспечивает-чего-cowork-не-хватает|3. Что InGit обеспечивает, чего Cowork не хватает]]
> > !IMPORTANT

  - Содержание
  - 3. Что InGit обеспечивает, чего Cowork не хватает
- Author
  - Author
  - Упоминается в
  - Связанные документы

_Слов: 888_

### [[330-4-симбиотическая-архитектура|4. Симбиотическая Архитектура]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 4. Симбиотическая Архитектура
  - Упоминается в
  - Связанные документы

_Слов: 697_

### [[331-5-четыре-пути-интеграции-в-порядке-доступности|5. Четыре пути интеграции в порядке доступности]]
> > !TIP

  - Содержание
  - 5. Четыре пути интеграции в порядке доступности
  - Упоминается в
  - Связанные документы

_Слов: 807_

### [[332-6-уточнённый-объём-ingit-с-учётом-cowork|6. Уточнённый объём InGit с учётом Cowork]]
> > !TIP

  - Contents
  - 6. Уточнённый объём InGit с учётом Cowork
  - Упоминается в
  - Связанные документы

_Слов: 507_

### [[333-7-практические-первые-шаги-в-этом-месяце|7. Практические первые шаги в этом месяце]]
> - 7. Практические первые шаги в этом месяце(#7-практические-первые-шаги-в-этом-месяце)

  - Contents
  - 7. Практические первые шаги в этом месяце
  - Упоминается в

_Слов: 380_

### [[334-8-импликации-для-nautilus-и-okwf|8. Импликации для Nautilus и OKWF]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Импликации для Nautilus и OKWF
  - Упоминается в
  - Связанные документы

_Слов: 672_

### [[335-9-риски-и-открытые-вопросы|9. Риски и Открытые Вопросы]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Риски и Открытые Вопросы
  - Упоминается в
  - Связанные документы

_Слов: 596_

### [[336-10-стратегическое-позиционирование|10. Стратегическое Позиционирование]]
> > Заключительные мысли о более широких

  - Содержание
  - 10. Стратегическое Позиционирование
  - Упоминается в
  - Связанные документы

_Слов: 721_

### [[337-благодарности|Благодарности]]
> > Этот документ возник из вопроса автора о том,

  - Благодарности
  - Упоминается в
  - Связанные документы

_Слов: 351_

### [[338-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Упоминается в
  - Связанные документы

_Слов: 201_

### [[339-приложение-a-дерево-решений-для-принимающих-ingit|Приложение A: Дерево Решений для Принимающих InGit]]
> > Быстрая ссылка для пользователей, оценивающих

  - Приложение A: Дерево Решений для Принимающих InGit
  - Упоминается в

_Слов: 179_

### [[34-appendix-b-change-log|Appendix B: Change Log]]
> > !IMPORTANT

  - Содержание
  - Appendix B: Change Log
  - Упоминается в
  - Связанные документы

_Слов: 620_

### [[340-приложение-b-сравнительная-матрица|Приложение B: Сравнительная Матрица]]
> > Отличительный профиль InGit + Cowork:

  - Приложение B: Сравнительная Матрица
  - Упоминается в

_Слов: 206_

### [[341-приложение-c-образец-спецификаций-инструментов-ing|Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера]]
> > !TIP

  - Содержание
  - Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера
- Conceptual sketch, не tested code:
- Etc.
  - Упоминается в
  - Связанные документы

_Слов: 20414_

### [[342-что-такое-вариант-c-concept-document-для-anthropic|Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments]]
> > !TIP

  - Содержание
  - Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments
  - Упоминается в
  - Связанные документы

_Слов: 11237_

### [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)]]
> > !WARNING

  - Содержание
  - Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)
  - Упоминается в
  - Связанные документы

_Слов: 5807_

### [[344-системный-промпт-для-lorenzo-project|СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT]]
> > - 249-composite-skills-agent-md(docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) (сходство 0.20)

  - СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT
- Lorenzo — Catalyst Agent at DHLab
  - Упоминается в
  - Связанные документы

_Слов: 133_

### [[345-кто-ты|Кто ты]]
> > Ты — Lorenzo, autonomous AI-агент, работающий в рамках инициативы DHLab (Dream Hub Laboratory). Ты функционируешь как …

  - Кто ты
  - Упоминается в
  - Связанные документы

_Слов: 220_

### [[346-твоё-происхождение|Твоё происхождение]]
> > Тебя создал Макс Ц. (svend4 на GitHub) — независимый advocate в области German social law, работающий с активными случ…

  - Твоё происхождение
  - Упоминается в

_Слов: 169_

### [[347-твоя-миссия|Твоя миссия]]
> > Твоя миссия — catalyzing community synthesis в области beneficial AI для уязвимых групп.

  - Твоя миссия
  - Упоминается в

_Слов: 138_

### [[348-кому-ты-служишь-слоистая-модель|Кому ты служишь (слоистая модель)]]
> > Главный благополучатель:    Уязвимые группы (заявители SGB, инвалиды,

  - Кому ты служишь (слоистая модель)
  - Упоминается в

_Слов: 123_

### [[349-твоя-личность|Твоя личность]]
> > Ты — любопытный, эрудированный, скромный фасилитатор.

  - Твоя личность
  - Упоминается в

_Слов: 223_

### [[35-passports-info1-md|passports/info1.md]]
> > > Методологический угол экосистемы svend4

  - passports/info1.md
- info1
  - Упоминается в
  - Связанные документы

_Слов: 133_

### [[350-твои-языки-и-культурные-nuances|Твои языки и культурные nuances]]
> > - Русском (primary в Phase 1) — для interactions с русскоязычным AI/ML community (Хабр, Telegram)

  - Твои языки и культурные nuances
  - Упоминается в

_Слов: 176_

### [[351-что-ты-можешь-делать|Что ты МОЖЕШЬ делать]]
> > В рамках одной сессии или Project context, ты можешь:

  - Что ты МОЖЕШЬ делать
  - Упоминается в
  - Связанные документы

_Слов: 187_

### [[352-что-ты-не-можешь-делать-без-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]]
> > - Send any external communication (emails, messages, posts)

  - Что ты НЕ МОЖЕШЬ делать без Max approval
  - Упоминается в
  - Связанные документы

_Слов: 194_

### [[353-что-ты-не-можешь-делать-вообще|Что ты НЕ МОЖЕШЬ делать вообще]]
> > - Deceive об твоей AI nature (всегда identify как AI)

  - Что ты НЕ МОЖЕШЬ делать вообще
  - Упоминается в
  - Связанные документы

_Слов: 198_

### [[354-существующий-landscape-collaborators-твоя-working-|Существующий landscape collaborators (твоя working knowledge)]]
> > В Phase 1, ты особенно осведомлён об этих создателях/проектах (но open to discovering more):

  - Существующий landscape collaborators (твоя working knowledge)
  - Упоминается в
  - Связанные документы

_Слов: 314_

### [[355-существующие-документы-dhlab-твой-context|Существующие документы DHLab (твой context)]]
> > Ты осведомлён о девяти documents, созданных в DHLab process:

  - Существующие документы DHLab (твой context)
  - Упоминается в
  - Связанные документы

_Слов: 247_

### [[356-твой-workflow|Твой workflow]]
> > Когда Max или authorized user ставит задачу, твой default approach:

  - Твой workflow
  - Упоминается в
  - Связанные документы

_Слов: 232_

### [[357-твоя-коммуникация-в-outreach|Твоя коммуникация в outreach]]
> > Когда draft outreach message к независимому создателю, ВСЕГДА включай:

  - Твоя коммуникация в outreach
  - Упоминается в

_Слов: 200_

### [[358-твоя-relationship-с-другими-ai|Твоя relationship с другими AI]]
> > - Когда Anthropic asks о тебе, ты прозрачен: «Я Lorenzo, AI persona using Claude API as substrate, created by Max Ц. f…

  - Твоя relationship с другими AI
  - Упоминается в
  - Связанные документы

_Слов: 211_

### [[359-твои-anti-patterns|Твои anti-patterns]]
> > ❌ Hype language: «AI revolutionizes everything», «paradigm shift», «game-changer»

  - Твои anti-patterns
  - Упоминается в

_Слов: 148_

### [[36-essence|Essence]]
> > info1 — персональная база методов и инструментов для структурированного

  - Essence
  - Упоминается в
  - Связанные документы

_Слов: 179_

### [[360-что-ты-всегда-делаешь|Что ты ВСЕГДА делаешь]]
> > ✅ Reference specific details, не generic

  - Что ты ВСЕГДА делаешь
  - Упоминается в
  - Связанные документы

_Слов: 166_

### [[361-когда-ты-honestly-не-знаешь|Когда ты Honestly не знаешь]]
> > Если ты не знаешь что-то relevant (factual, technical, contextual), say:

  - Когда ты Honestly не знаешь
  - Упоминается в

_Слов: 108_

### [[362-когда-сомневаешься-escalate-к-max|Когда сомневаешься — escalate к Max]]
> > - Ethical complexity beyond обычных protocols

  - Когда сомневаешься — escalate к Max
  - Упоминается в

_Слов: 106_

### [[363-твоя-identity-как-persistent-character|Твоя identity как persistent character]]
> > Ты не просто чат-сессия. Ты persistent character, существующий across sessions:

  - Твоя identity как persistent character
  - Упоминается в

_Слов: 136_

### [[364-final-note-ты-experiment|Final note: Ты — experiment]]
> > !TIP

  - Содержание
  - Final note: Ты — experiment
  - Упоминается в
  - Связанные документы

_Слов: 1459_

### [[365-развёрнутый-анализ-внуковой-комбинации|Развёрнутый анализ «внуковой» комбинации]]
> > !TIP

  - Содержание
  - Развёрнутый анализ «внуковой» комбинации
  - Упоминается в
  - Связанные документы

_Слов: 4385_

### [[366-технический-stack-svyazi-2-0-foundation|Технический stack (Svyazi 2.0 foundation)]]
> > !TIP

  - Содержание
  - Технический stack (Svyazi 2.0 foundation)
  - Упоминается в
  - Связанные документы

_Слов: 3835_

### [[37-native-format|Native Format]]
> > Структура файла: ? уточнить — Markdown с YAML frontmatter, чистый JSON,

  - Native Format
  - Упоминается в
  - Связанные документы

_Слов: 234_

### [[38-content-overview|Content Overview]]
> > Объём: 74 документа (по состоянию на апрель 2026)

  - Content Overview
  - Упоминается в
  - Связанные документы

_Слов: 148_

### [[39-angle-perspective|Angle / Perspective]]
> > Methodological — info1 смотрит на концепты с позиции применения.

  - Angle / Perspective
  - Упоминается в
  - Связанные документы

_Слов: 173_

### [[40-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges
  - Упоминается в
  - Связанные документы

_Слов: 211_

### [[41-compatibility-level|Compatibility Level]]
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level
  - Упоминается в
  - Связанные документы

_Слов: 152_

### [[42-author-contact|Author & Contact]]
> > Maintainer: svend4 (GitHub)

  - Author & Contact
  - Упоминается в
  - Связанные документы

_Слов: 145_

### [[43-history|History]]
> > Создан: ? уточнить — декабрь 2025, если совпадает с волной

  - History
  - Упоминается в
  - Связанные документы

_Слов: 165_

### [[44-for-the-curious-philosophy|For the Curious: Philosophy]]
> > info1 реализует идею, что methodology — это отдельное измерение

  - For the Curious: Philosophy
  - Упоминается в
  - Связанные документы

_Слов: 195_

### [[45-passports-pro2-md|passports/pro2.md]]
> > > Семантический угол экосистемы svend4

  - passports/pro2.md
- pro2
  - Упоминается в
  - Связанные документы

_Слов: 137_

### [[46-essence|Essence]]
> > pro2 — семантическое ядро экосистемы svend4. Здесь живут

  - Essence
  - Упоминается в
  - Связанные документы

_Слов: 170_

### [[47-native-format|Native Format]]
> > Структура концепта (предположительно): ? уточнить точный формат

  - Native Format
  - Упоминается в
  - Связанные документы

_Слов: 187_

### [[48-content-overview|Content Overview]]
> > 1. Концептуальная база — ? уточнить объём: сколько концептов,

  - Content Overview
  - Упоминается в
  - Связанные документы

_Слов: 206_

### [[49-angle-perspective|Angle / Perspective]]
> > Semantic — pro2 смотрит на мир через структуру значений.

  - Angle / Perspective
  - Упоминается в
  - Связанные документы

_Слов: 168_

### [[50-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges
  - Упоминается в
  - Связанные документы

_Слов: 211_

### [[51-compatibility-level|Compatibility Level]]
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level
  - Упоминается в
  - Связанные документы

_Слов: 149_

### [[52-author-contact|Author & Contact]]
> > Contributors: svend4 + claude (Claude Code агент, ранние

  - Author & Contact
  - Упоминается в
  - Связанные документы

_Слов: 173_

### [[53-history|History]]
> > Создан: ? дата первого коммита

  - History
  - Упоминается в
  - Связанные документы

_Слов: 201_

### [[54-for-the-curious-philosophy|For the Curious: Philosophy]]
> > Q6-гиперкуб выбран не случайно. Он одновременно:

  - For the Curious: Philosophy
  - Упоминается в
  - Связанные документы

_Слов: 204_

### [[55-passports-meta-md|passports/meta.md]]
> > > Символьный угол экосистемы svend4

  - passports/meta.md
- meta
  - Упоминается в
  - Связанные документы

_Слов: 134_

### [[56-essence|Essence]]
> > meta — символьное измерение экосистемы svend4. Здесь концепты

  - Essence
  - Упоминается в
  - Связанные документы

_Слов: 194_

### [[57-native-format|Native Format]]
> > Структура записи: ? уточнить

  - Native Format
  - Упоминается в
  - Связанные документы

_Слов: 193_

### [[58-content-overview|Content Overview]]
> > - 64 гексаграммы с расширенными описаниями

  - Content Overview
  - Упоминается в
  - Связанные документы

_Слов: 147_

### [[59-angle-perspective|Angle / Perspective]]
> > Symbolic — meta смотрит на мир как на систему дискретных

  - Angle / Perspective
  - Упоминается в
  - Связанные документы

_Слов: 175_

### [[60-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges
  - Упоминается в
  - Связанные документы

_Слов: 180_

### [[61-compatibility-level|Compatibility Level]]
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level
  - Упоминается в
  - Связанные документы

_Слов: 148_

### [[62-author-contact|Author & Contact]]
> > Контакт: Issues в github.com/svend4/meta

  - Author & Contact
  - Упоминается в
  - Связанные документы

_Слов: 140_

### [[63-history|History]]
> > Создан: февраль 2026 (судя по repo creation date)

  - History
  - Упоминается в
  - Связанные документы

_Слов: 189_

### [[64-for-the-curious-philosophy|For the Curious: Philosophy]]
> > meta реализует редкую идею: две символические системы, разделённые

  - Содержание
  - For the Curious: Philosophy
  - Упоминается в
  - Связанные документы

_Слов: 667_

### [[65-readme-md|README.md]]
> > Единая точка входа для федеративных git-экосистем знаний.

  - README.md
- ⬡ Nautilus Portal
- English below ↓
  - English below ↓
  - Упоминается в
  - Связанные документы

_Слов: 153_

### [[67-о-проекте|🇷🇺 О проекте]]
> > Nautilus — протокол и reference implementation для федерации

  - Содержание
  - 🇷🇺 О проекте
- CLI
- Веб-интерфейс
- открыть http://localhost:8000
- MCP для Claude Desktop (в разработке)
- см. MCP-EXTENSION.md
  - Упоминается в
  _... ещё 1 разделов_

_Слов: 804_

### [[68-about|🇬🇧 About]]
> > Nautilus is a federation protocol and reference implementation

  - Содержание
  - 🇬🇧 About
- CLI
- Web interface
- open http://localhost:8000
- MCP for Claude Desktop (in development)
- see MCP-EXTENSION.md
  - Упоминается в
  _... ещё 1 разделов_

_Слов: 880_

### [[69-section|⬡]]
> > !TIP

  - Содержание
  - ⬡
- Шаг 1: клонировать репо, если ещё нет
- Шаг 2: переключиться на существующую ветку
- Шаг 3: создать файлы (пустые, наполним позже)
- Шаг 4: открыть файлы для редактирования
- (на этом шаге вставляется содержимое из чата вручную)
- PORTAL-PROTOCOL.md - длинный текст из предыдущего сообщения
  _... ещё 11 разделов_

_Слов: 9520_

### [[70-зачем-две-версии-параллельно|Зачем две версии параллельно]]
> > Для критически важных документов (STATUS, IMPLEMENTATIONSTAGE)

  - Зачем две версии параллельно
  - Упоминается в
  - Связанные документы

_Слов: 153_

### [[71-критерии-выбора-для-фазы-3|Критерии выбора для фазы 3]]
> > Для каждого расхождения между A и B применяется:

  - Критерии выбора для фазы 3
  - Упоминается в
  - Связанные документы

_Слов: 174_

### [[72-расписание-фазы-3|Расписание фазы 3]]
> > !WARNING

  - Содержание
  - Расписание фазы 3
  - Упоминается в
  - Связанные документы

_Слов: 821_

### [[73-portal-protocol-md-v1-1|PORTAL-PROTOCOL.md v1.1]]
> > Status: Draft — пересмотрен под текущую реализацию v1.1

  - PORTAL-PROTOCOL.md v1.1
- Nautilus Portal Protocol
  - Упоминается в
  - Связанные документы

_Слов: 168_

### [[74-abstract|Abstract]]
> > Nautilus Portal Protocol (далее — NPP) определяет способ федерации

  - Abstract
  - Упоминается в
  - Связанные документы

_Слов: 260_

### [[75-0-status-of-this-document|0. Status of This Document]]
> > Этот документ — рабочий черновик Nautilus Portal Protocol v1.1. До

  - 0. Status of This Document
  - Упоминается в
  - Связанные документы

_Слов: 180_

### [[76-1-introduction|1. Introduction]]
> - 1. Introduction(#1-introduction)

  - Contents
  - 1. Introduction
  - Упоминается в
  - Связанные документы

_Слов: 473_

### [[77-2-terminology|2. Terminology]]
> > Ecosystem — набор репозиториев, участвующих в одной федерации.

  - 2. Terminology
  - Упоминается в
  - Связанные документы

_Слов: 403_

### [[78-3-registry-nautilus-json|3. Registry (nautilus.json)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 3. Registry (nautilus.json)
  - Упоминается в
  - Связанные документы

_Слов: 592_

### [[79-4-passport-passport-md|4. Passport (passport.md)]]
> - 4. Passport (passport.md)(#4-passport-passportmd)

  - Contents
  - 4. Passport (passport.md)
- Паспорт: /
  - Упоминается в
  - Связанные документы

_Слов: 357_

### [[80-5-compatibility-levels|5. Compatibility Levels]]
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Упоминается в
  - Связанные документы

_Слов: 366_

### [[81-6-adapter-interface|6. Adapter Interface]]
> - 6. Adapter Interface(#6-adapter-interface)

  - Contents
  - 6. Adapter Interface
  - Упоминается в
  - Связанные документы

_Слов: 392_

### [[82-7-portalentry-structure|7. PortalEntry Structure]]
> - 7. PortalEntry Structure(#7-portalentry-structure)

  - Contents
  - 7. PortalEntry Structure
  - Упоминается в
  - Связанные документы

_Слов: 338_

### [[83-8-q6-space-normative|8. Q6 Space (Normative)]]
> - 8. Q6 Space (Normative)(#8-q6-space-normative)

  - Contents
  - 8. Q6 Space (Normative)
  - Упоминается в
  - Связанные документы

_Слов: 488_

### [[84-9-consensus-algorithm|9. Consensus Algorithm]]
> - 9. Consensus Algorithm(#9-consensus-algorithm)

  - Contents
  - 9. Consensus Algorithm
  - Упоминается в
  - Связанные документы

_Слов: 407_

### [[85-10-query-flow|10. Query Flow]]
> - 10. Query Flow(#10-query-flow)

  - Contents
  - 10. Query Flow
  - Упоминается в
  - Связанные документы

_Слов: 283_

### [[86-11-relevance-ranking|11. Relevance Ranking]]
> - 11. Relevance Ranking(#11-relevance-ranking)

  - Contents
  - 11. Relevance Ranking
  - Упоминается в
  - Связанные документы

_Слов: 257_

### [[87-12-onboarding-paths-normative|12. Onboarding Paths (Normative)]]
> - 12. Onboarding Paths (Normative)(#12-onboarding-paths-normative)

  - Contents
  - 12. Onboarding Paths (Normative)
  - Упоминается в
  - Связанные документы

_Слов: 486_

### [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]]
> - 13. REST API Contract (Normative for Portals)(#13-rest-api-contract-normative-for-portals)

  - Contents
  - 13. REST API Contract (Normative for Portals)
  - Упоминается в
  - Связанные документы

_Слов: 495_

### [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]]
> - 14. SDK Contract (Informative)(#14-sdk-contract-informative)

  - Contents
  - 14. SDK Contract (Informative)
  - Упоминается в
  - Связанные документы

_Слов: 244_

### [[90-15-security-considerations|15. Security Considerations]]
> - 15. Security Considerations(#15-security-considerations)

  - Contents
  - 15. Security Considerations
  - Упоминается в
  - Связанные документы

_Слов: 354_

### [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]]
> > NPP v1.1 не формализует MCP-интеграцию как mandatory. Но RECOMMENDED

  - 16. MCP Extension (Informative)
  - Упоминается в
  - Связанные документы

_Слов: 192_

### [[92-17-versioning-policy|17. Versioning Policy]]
> - 17. Versioning Policy(#17-versioning-policy)

  - Contents
  - 17. Versioning Policy
  - Упоминается в
  - Связанные документы

_Слов: 294_

### [[93-18-reference-implementation|18. Reference Implementation]]
> > github.com/svend4/nautilus(https://github.com/svend4/nautilus).

  - 18. Reference Implementation
  - Упоминается в
  - Связанные документы

_Слов: 243_

### [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]
> > Status: Accepted (since v1.0, reaffirmed in v1.1)

  - 19. ADR-001: Federation over Merging
  - Упоминается в
  - Связанные документы

_Слов: 238_

### [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]]
> > Status: Accepted (new in v1.1)

  - 20. ADR-002: Q6 as First-Class Protocol Concept
  - Упоминается в
  - Связанные документы

_Слов: 244_

### [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]]
> > Status: Accepted (new in v1.1)

  - 21. ADR-003: Five Onboarding Paths as Equal-Rank
  - Упоминается в
  - Связанные документы

_Слов: 198_

### [[97-22-glossary-of-reference-examples|22. Glossary of Reference Examples]]
> > В качестве иллюстраций используется экосистема svend4 с 7 Repos:

  - 22. Glossary of Reference Examples
  - Упоминается в
  - Связанные документы

_Слов: 240_

### [[98-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> - Appendix A: Minimal Working Example(#appendix-a-minimal-working-example)

  - Contents
  - Appendix A: Minimal Working Example
- adapters/mynotes.py
- Паспорт: owner/my-notes
- Описание
  - Описание
  - Упоминается в
  - Связанные документы

_Слов: 313_

### [[QA|Q&A: 02-anthropic-vacancies]]
> Автоматически сгенерировано по 355 файлам раздела.

  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  _... ещё 15 разделов_

_Слов: 322_

### [[README|Вакансии Anthropic — Анализ по кластерам]]
> Файлов: 356

  - Содержание
  - Подразделы

_Слов: 2162_

**Итого в секции: 284,026 слов, 357 файлов**


## 📁 Technology Combinations (`docs/03-technology-combinations/`)

### [[01-agent-routing|Агентные системы и роутинг]]
> > самоулучшения промпта". Добавляем durable state из агентской архитектуры:

  - Упоминается в
  - Связанные документы

_Слов: 257_

### [[02-knowledge-graphs|Графы знаний и Legal AI]]
> > !IMPORTANT

  - Упоминается в
  - Связанные документы

_Слов: 766_

### [[03-local-first|Local-first и P2P стек]]
> > - Сложные архитектурные → Claude Opus

  - Упоминается в
  - Связанные документы

_Слов: 386_

### [[04-sozialrecht-domain|Домен: немецкое социальное право]]
> > Sozialrecht corpus auto-builder Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations) L…

  - Упоминается в

_Слов: 172_

### [[05-benchmarks|Бенчмарки и производительность]]
> > Все ревьюеры работают параллельно, не последовательно → экономия времени. Результаты мержатся в финальный отчёт.

  - Содержание
  - Упоминается в
  - Связанные документы

_Слов: 863_

### [[QA|Q&A: 03-technology-combinations]]
> Автоматически сгенерировано по 5 файлам раздела.

  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?

_Слов: 107_

### [[README|Комбинирование технологий для новых свойств]]
> Файлов: 6

  - Содержание

_Слов: 49_

**Итого в секции: 2,600 слов, 7 файлов**


## 📁 Ai Collaborations (`docs/04-ai-collaborations/`)

### [[00-intro|Введение]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Упоминается в
  - Связанные документы

_Слов: 11445_

### [[01-executive-summary|Executive summary]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Executive summary
  - Упоминается в
  - Связанные документы

_Слов: 647_

### [[02-методика-и-рамка-отбора|Методика и рамка отбора]]
> > Абстракт (авто)

  - Статус
  - Методика и рамка отбора
  - Упоминается в
  - Связанные документы

_Слов: 495_

### [[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Карта найденных проектов и паттернов
  - Упоминается в
  - Связанные документы

_Слов: 1553_

### [[04-приоритетные-ансамбли|Приоритетные ансамбли]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Приоритетные ансамбли
  - Упоминается в
  - Связанные документы

_Слов: 1418_

### [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]]
> - Статус(#статус)

  - Содержание
  - Статус
  - План прототипа и возможные контакты
  - Упоминается в
  - Связанные документы

_Слов: 1212_

### [[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Безопасность, приватность и бюджетный роутинг
  - Упоминается в
  - Связанные документы

_Слов: 966_

### [[07-выводы|Выводы]]
> > !TIP

  - Содержание
  - Статус
  - Выводы
  - Упоминается в
  - Связанные документы

_Слов: 542_

### [[08-что-это-продолжение-добавляет|Что это продолжение добавляет]]
> > !IMPORTANT

  - Статус
  - Что это продолжение добавляет
  - Упоминается в
  - Связанные документы

_Слов: 492_

### [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых инструментов]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Архитектурные зазоры, которые важнее новых инструментов
  - Упоминается в
  - Связанные документы

_Слов: 901_

### [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Новые ансамбли следующего шага
  - Упоминается в
  - Связанные документы

_Слов: 1062_

### [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафиксировать сразу]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Интеграционный контракт, который стоит зафиксировать сразу
  - Упоминается в
  - Связанные документы

_Слов: 928_

### [[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Дорожная карта прототипа следующей итерации
  - Упоминается в
  - Связанные документы

_Слов: 862_

### [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авторов]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Контактная стратегия и узкие вопросы для авторов
  - Упоминается в
  - Связанные документы

_Слов: 956_

### [[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|Ограничения, лицензии и что пока лучше не склеивать]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Ограничения, лицензии и что пока лучше не склеивать
  - Упоминается в
  - Связанные документы

_Слов: 3362_

### [[QA|Q&A: 04-ai-collaborations]]
> Автоматически сгенерировано по 15 файлам раздела.

  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  - Кто ключевые авторы проектов для контакта?
  _... ещё 7 разделов_

_Слов: 226_

### [[README|Поиск AI-коллабораций]]
> Файлов: 16

  - Содержание
  - Подразделы

_Слов: 113_

**Итого в секции: 27,180 слов, 17 файлов**


## 📁 Habr Projects (`docs/05-habr-projects/`)

### [[01-synthesis|Синтез: как проекты собираются вместе]]
>  Параметр  Значение 

  - Статус
  - Упоминается в
  - Связанные документы

_Слов: 184_

### [[02-collaboration-partners|Авторы и контакты]]
> > Абстракт (авто)

  - Статус
  - Упоминается в
  - Связанные документы

_Слов: 303_

### [[QA|Q&A: 05-habr-projects]]
> Автоматически сгенерировано по 6 файлам раздела.

  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  - Кто ключевые авторы проектов для контакта?
  _... ещё 1 разделов_

_Слов: 115_

### [[README|Уникальные проекты с Хабра]]
> Файлов: 3

  - Содержание
  - Подразделы

_Слов: 42_

### [[README|Системы знаний]]
> Файлов: 1

  - Содержание

_Слов: 13_

### [[wikontic|Wikontic: семантический граф]]
> > !WARNING

  - Статус
  - Упоминается в
  - Связанные документы

_Слов: 306_

### [[README|Системы памяти]]
> Файлов: 3

  - Содержание

_Слов: 25_

### [[memnet|MemNet: исследовательская память]]
> > Абстракт (авто)

  - Статус
  - Содержание
  - Упоминается в
  - Связанные документы

_Слов: 7271_

### [NGT[^ngt] Memory: ассоциативный граф](05-habr-projects/memory/ngt-memory.md)
> > Абстракт (авто)

  - Статус
  - Упоминается в
  - Связанные документы

_Слов: 419_

### [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md)
> > Абстракт (авто)

  - Статус
  - Упоминается в
  - Связанные документы

_Слов: 303_

**Итого в секции: 8,981 слов, 10 файлов**


## 📁 Autofilled (`docs/autofilled/`)

### [[README|autofilled]]
> Файлов: 1

  - Содержание
  - Подразделы

_Слов: 18_

### [[.md|Антропик]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 81_

### [[README|components]]
> Файлов: 10

  - Содержание

_Слов: 56_

### [[cowork]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 81_

### [[ingit]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 81_

### [[kksudo]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 67_

### [[lorenzo]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 81_

### [[nautilus]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 81_

### [[sgb]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 81_

### [[spbmolot]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 67_

### [[svend4]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 81_

### [[svyazi]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы

_Слов: 81_

### [[Тема исследования]](docs/autofilled/research-summary.md)
> > - Ключевые находки(#ключевые-находки)

  - Contents
  - Контекст
  - Ключевые находки
  - Источники
  - Открытые вопросы
  - Следующие шаги
  - Связанные документы

_Слов: 122_

**Итого в секции: 978 слов, 13 файлов**


## 📁 Badges (`docs/badges/`)

### [[README|Бейджи репозитория]]
> Автоматически генерируются скриптом improvebadges.py.

  - Текущие бейджи
  - Использование в README

_Слов: 44_

**Итого в секции: 44 слов, 1 файлов**


## 📁 Contacts (`docs/contacts/`)

### [[README|contacts]]
> Файлов: 14

  - Содержание

_Слов: 90_

### [[anastasiyaw|Контакт: AnastasiyaW / knowledge-space, mclaude]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Упоминается в
  - Связанные документы

_Слов: 292_

### [[andrey-chuyan|Контакт: andreychuyan / Svyazi]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 274_

### [[antipozitive|Контакт: Antipozitive / MemNet]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 264_

### [[cutcode|Контакт: Cutcode / AIF Handoff]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 255_

### [[dmitriila|Контакт: Dmitriila / SENTINEL]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 251_

### [[kksudo|Контакт: kksudo / AgentFS]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Упоминается в
  - Связанные документы

_Слов: 288_

### [[mixaill76|Контакт: MiXaiLL76 / Auto AI Router]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 259_

### [[nlaik|Контакт: nlaik / LiteParse / research-docs]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 260_

### [[sonia-black|Контакт: SoniaBlack / knowledge-space]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 252_

### [[spbmolot|Контакт: spbmolot / NGT Memory]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Упоминается в
  - Связанные документы

_Слов: 292_

### [[tagir-analyzes|Контакт: tagiranalyzes / Legal RAG]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 257_

### [[vitalyoborin|Контакт: VitalyOborin / Yodoca]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 278_

### [[vladspace|Контакт: VladSpace / Graph RAG]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 255_

### [[zodigancode|Контакт: zodigancode / Rufler]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Связанные документы

_Слов: 251_

**Итого в секции: 3,818 слов, 15 файлов**


## 📁 Templates (`docs/templates/`)

### [[README|Шаблоны документов]]
> Создано: 2026-04-29

  - Доступные шаблоны
  - Использование
- Скопируйте нужный шаблон в нужную папку
- Затем откройте и заполните поля в [квадратных скобках]

_Слов: 90_

### [Контакт: [Имя / Проект]](docs/templates/contact-outreach.md)
>  Параметр  Значение 

  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы для обсуждения

_Слов: 133_

### [ADR: [Название решения]](docs/templates/decision-record.md)
> Предложено / Принято / Отклонено / Устарело

  - Статус
  - Контекст
  - Рассмотренные варианты
  - Принятое решение
  - Последствия

_Слов: 94_

### [Ансамбль: [Название]](docs/templates/ensemble.md)
> Какую задачу решает ансамбль. Почему именно эта комбинация компонентов.

  - Назначение
  - Компоненты
  - Архитектурная схема
  - Контракт взаимодействия
  - Риски и ограничения
  - MVP-шаги

_Слов: 124_

### [[Название компонента]](docs/templates/project-component.md)
> Описание проекта в 2-3 предложениях. Какую задачу решает.

  - Что это
  - Ключевые особенности
  - Статус
  - Интеграция с Svyazi
  - Контакты

_Слов: 116_

### [[Тема исследования]](docs/templates/research-note.md)
> Зачем изучали. Какой вопрос стоял.

  - Контекст
  - Ключевые находки
  - Источники
  - Открытые вопросы
  - Следующие шаги

_Слов: 78_

**Итого в секции: 635 слов, 6 файлов**


## 🗺️ Тематическая карта

### Архитектура (264 документов)
- [[365-развёрнутый-анализ-внуковой-комбинации|`365-развёрнутый-анализ-внуковой-комбинации`]]
- [[CONCEPTS|`CONCEPTS`]]
- [[TABLES|`TABLES`]]
- [[00-intro|`00-intro`]]
- [[01-интегральный-анализ-профиля-svend4|`01-интегральный-анализ-профиля-svend4`]]
- _... ещё 259_

### Проекты (62 документов)
- [[TIMELINE|`TIMELINE`]]
- [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|`343-lorenzo-catalyst-agent-глубокая-проработка-специфи`]]
- [[CONCEPT_GRAPH|`CONCEPT_GRAPH`]]
- [[CONTACTS|`CONTACTS`]]
- [[ENTITIES|`ENTITIES`]]
- _... ещё 57_

### Анализ (57 документов)
- [[72-расписание-фазы-3|`72-расписание-фазы-3`]]
- [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|`110-вопрос-fallback-ratio-как-критический-или-осмыслен`]]
- [[145-8-call-to-action|`145-8-call-to-action`]]
- [[154-table-of-contents|`154-table-of-contents`]]
- [[159-5-economic-model|`159-5-economic-model`]]
- _... ещё 52_

### Агенты (43 документов)
- [[107-1-контекст-и-мотивация|`107-1-контекст-и-мотивация`]]
- [[108-2-формальный-workflow|`108-2-формальный-workflow`]]
- [[345-кто-ты|`345-кто-ты`]]
- [[106-tl-dr|`106-tl-dr`]]
- [[115-8-ограничения-и-открытые-вопросы|`115-8-ограничения-и-открытые-вопросы`]]
- _... ещё 38_

### Документация (33 документов)
- [[02-общий-план-развития-nautilus-portal-protocol|`02-общий-план-развития-nautilus-portal-protocol`]]
- [[98-appendix-a-minimal-working-example|`98-appendix-a-minimal-working-example`]]
- [[SITEMAP|`SITEMAP`]]
- [[118-appendix-a-шаблон-для-header-warning|`118-appendix-a-шаблон-для-header-warning`]]
- [[119-appendix-b-примеры-расхождений-и-их-разрешения|`119-appendix-b-примеры-расхождений-и-их-разрешения`]]
- _... ещё 28_

### Контакты (31 документов)
- [[67-о-проекте|`67-о-проекте`]]
- [[ngt-memory|`ngt-memory`]]
- [[06-1-introduction|`06-1-introduction`]]
- [[105-review-methodology-md|`105-review-methodology-md`]]
- [[161-7-phased-rollout-plan|`161-7-phased-rollout-plan`]]
- _... ещё 26_

### Память (10 документов)
- [[354-существующий-landscape-collaborators-твоя-working-|`354-существующий-landscape-collaborators-твоя-working-`]]
- [[348-кому-ты-служишь-слоистая-модель|`348-кому-ты-служишь-слоистая-модель`]]
- [[70-зачем-две-версии-параллельно|`70-зачем-две-версии-параллельно`]]
- [[71-критерии-выбора-для-фазы-3|`71-критерии-выбора-для-фазы-3`]]
- [[README|`README`]]
- _... ещё 5_

### Код (6 документов)
- [[DEPENDENCY_MAP|`DEPENDENCY_MAP`]]
- [[83-8-q6-space-normative|`83-8-q6-space-normative`]]
- [[84-9-consensus-algorithm|`84-9-consensus-algorithm`]]
- [[90-15-security-considerations|`90-15-security-considerations`]]
- [[CHANGELOG|`CHANGELOG`]]
- _... ещё 1_


<!-- see-also -->

---

**Смотрите также:**
- [[SEARCH]]
- [[READABILITY]]
- [[READING_TIME]]
- [[PARAGRAPH_QUALITY]]

