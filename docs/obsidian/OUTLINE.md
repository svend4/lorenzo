---
title: "Outline базы знаний"
tags:
  - security
  - knowledge
  - general
date: 2026-04-29
---

# Outline базы знаний

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
  - [[[BADGES|Status Badges]]](#badgesstatus-badges)
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
  - [[[CROSS_SECTION|Кросс-секционный анализ]]](#cross_sectionкросс-секционный-анализ)
  - [[[DECISIONS|Ключевые решения и выводы]]](#decisionsключевые-решения-и-выводы)
  - [[[DENSITY|Карта плотности тем]]](#densityкарта-плотности-тем)
  - [[[DEPENDABOT|Мониторинг зависимостей]]](#dependabotмониторинг-зависимостей)
  - [[[DEPENDENCY_MAP|Карта зависимостей скриптов]]](#dependency_mapкарта-зависимостей-скриптов)
  - [[[DIGEST|Дайджест изменений]]](#digestдайджест-изменений)
  - [[[DIGEST_AUTO|Автодайджест изменений]]](#digest_autoавтодайджест-изменений)
  - [[[DIGEST_WEEKLY|Еженедельный дайджест — 2026-04-29]]](#digest_weeklyеженедельный-дайджест-2026-04-29)
  - [[[DUPLICATES|Отчёт о дублировании]]](#duplicatesотчёт-о-дублировании)
  - [[[EMPTY_SECTIONS|Пустые секции]]](#empty_sectionsпустые-секции)
  - [[[ENTITIES|Именованные сущности]]](#entitiesименованные-сущности)
  - [[[FAQ|Часто задаваемые вопросы (FAQ)]]](#faqчасто-задаваемые-вопросы-faq)
  - [[[FOOTNOTES|Сноски и определения терминов]]](#footnotesсноски-и-определения-терминов)
  - [[[GLOSSARY|Глоссарий проектов]]](#glossaryглоссарий-проектов)
  - [[[GRAPH|Граф связей проектов]]](#graphграф-связей-проектов)
  - [[[HEADING_AUDIT|Аудит заголовков]]](#heading_auditаудит-заголовков)
  - [[[HEALTH|Health Dashboard]]](#healthhealth-dashboard)
  - [[[HEATMAP|Тепловая карта тем]]](#heatmapтепловая-карта-тем)
  - [[[INDEX|Индекс документации — Lorenzo / Svyazi 2.0]]](#indexиндекс-документации-lorenzo-svyazi-20)
  - [[[KEYWORD_INDEX|Инвертированный индекс ключевых слов]]](#keyword_indexинвертированный-индекс-ключевых-слов)
  - [[[KNOWLEDGE_MAP|Карта базы знаний Lorenzo]]](#knowledge_mapкарта-базы-знаний-lorenzo)
  - [[[KPI|Числовые KPI и метрики]]](#kpiчисловые-kpi-и-метрики)
  - [[[KPI_HISTORY|История метрик KPI]]](#kpi_historyистория-метрик-kpi)
  - [[[LANGUAGE_STATS|Языковой состав документов]]](#language_statsязыковой-состав-документов)
  - [[[LINKS|Индекс ссылок]]](#linksиндекс-ссылок)
  - [[[LLM_SUMMARIES|AI-саммари разделов документации]]](#llm_summariesai-саммари-разделов-документации)
  - [[[MCP_DASHBOARD|MCP Dashboard]]](#mcp_dashboardmcp-dashboard)
  - [[[METRICS|Метрики качества документации]]](#metricsметрики-качества-документации)
  - [[[MINDMAP|Майндмап репозитория Lorenzo]]](#mindmapмайндмап-репозитория-lorenzo)
  - [[[MISSING|Карта пробелов знаний]]](#missingкарта-пробелов-знаний)
  - [[[NAMED_ENTITIES|Индекс именованных сущностей]]](#named_entitiesиндекс-именованных-сущностей)
  - [[[NARRATIVE|Нарратив проекта Lorenzo]]](#narrativeнарратив-проекта-lorenzo)
  - [[[NETWORK|Сеть проектов и авторов]]](#networkсеть-проектов-и-авторов)
  - [[[ONBOARDING|Онбординг — Svyazi 2.0 / Lorenzo]]](#onboardingонбординг-svyazi-20-lorenzo)
  - [[[ORPHANS|Изолированные документы (Orphans)]]](#orphansизолированные-документы-orphans)
  - [[[PARAGRAPH_QUALITY|Качество абзацев]]](#paragraph_qualityкачество-абзацев)
  - [[[PASSIVE_VOICE|Пассивный залог и канцеляризмы]]](#passive_voiceпассивный-залог-и-канцеляризмы)
  - [[[PRIORITIES|Приоритеты файлов]]](#prioritiesприоритеты-файлов)
  - [[[PROGRESS|Прогресс MVP]]](#progressпрогресс-mvp)
  - [[[QA|Глобальный Q&A]]](#qaглобальный-qa)
  - [[[QUESTIONS|Открытые вопросы]]](#questionsоткрытые-вопросы)
  - [[[READING_LIST|Список чтения]]](#reading_listсписок-чтения)
  - [[[READING_ORDER|Рекомендуемый порядок чтения]]](#reading_orderрекомендуемый-порядок-чтения)
  - [[[README|docs]]](#readmedocs)
  - [[[REGISTRY|REGISTRY — реестр артефактов Lorenzo]]](#registryregistry-реестр-артефактов-lorenzo)
  - [[[REPORT|Svyazi 2.0 — Knowledge Base Report]]](#reportsvyazi-20-knowledge-base-report)
  - [[[RISK_REGISTER|Реестр рисков — Svyazi 2.0]]](#risk_registerреестр-рисков-svyazi-20)
  - [[[SCHEDULE|Расписание проекта]]](#scheduleрасписание-проекта)
  - [[[SCORING|Оценка готовности проекта (Go/No-Go)]]](#scoringоценка-готовности-проекта-gono-go)
  - [[[SCRIPTS_CATALOG|Каталог скриптов]]](#scripts_catalogкаталог-скриптов)
  - [[[SEARCH_RESULTS|Результаты поиска]]](#search_resultsрезультаты-поиска)
  - [[[SEE_ALSO|Индекс «Смотрите также»]]](#see_alsoиндекс-смотрите-также)
  - [[[SENTIMENT|Тональный анализ документов]]](#sentimentтональный-анализ-документов)
  - [[[SIMILAR|Похожие документы]]](#similarпохожие-документы)
  - [[[SIMILAR_PASSAGES|Похожие абзацы между документами]]](#similar_passagesпохожие-абзацы-между-документами)
  - [[[SITEMAP|Карта репозитория Lorenzo]]](#sitemapкарта-репозитория-lorenzo)
  - [[[SKILL_DASHBOARD|Skill Dashboard]]](#skill_dashboardskill-dashboard)
  - [[[SOURCE_MAP|Карта происхождения текстов]]](#source_mapкарта-происхождения-текстов)
  - [[[STATS|Детальная статистика репозитория]]](#statsдетальная-статистика-репозитория)
  - [[[SUMMARIES|Резюме документов (TextRank)]]](#summariesрезюме-документов-textrank)
  - [[[TABLES|Все таблицы репозитория]]](#tablesвсе-таблицы-репозитория)
  - [[[TAGS|Индекс тегов]]](#tagsиндекс-тегов)
  - [[[TASKS_INDEX|Каталог задач (TASKSINDEX)]]](#tasks_indexкаталог-задач-tasksindex)
  - [[[TECH_RADAR|Tech Radar — Svyazi 2.0]]](#tech_radartech-radar-svyazi-20)
  - [[[TIMELINE|Хронология и временные маркеры]]](#timelineхронология-и-временные-маркеры)
  - [[[VALIDATION|Валидация структуры репозитория]]](#validationвалидация-структуры-репозитория)
  - [[[VOCABULARY|Богатство словаря документов]]](#vocabularyбогатство-словаря-документов)
  - [[[WORD_CLOUD|Word Cloud]]](#word_cloudword-cloud)
  - [[[WORD_FREQ|Частотный анализ слов]]](#word_freqчастотный-анализ-слов)
  - [[[reading-paths|Reading paths — рекомендуемые маршруты по монорепозиторию]]](#reading-pathsreading-paths-рекомендуемые-маршруты-по-монорепозиторию)
- [📁 Svyazi (`docs/01-svyazi/`)](#svyazi-docs01-svyazi)
  - [[[00-intro-part2|Продолжение исследования для Svyazi 2.0]]](#00-intro-part2продолжение-исследования-для-svyazi-20)
  - [[Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md)](#svyazisvyazi-20-исполнительное-резюмеdocs01-svyazi01-executive-summarymd)
  - [[[02-methodology|Методика и рамка отбора проектов]]](#02-methodologyметодика-и-рамка-отбора-проектов)
  - [[[03-component-catalog|Карта найденных проектов и паттернов]]](#03-component-catalogкарта-найденных-проектов-и-паттернов)
  - [[[04-ensembles-overview|Приоритетные ансамбли]]](#04-ensembles-overviewприоритетные-ансамбли)
  - [[[06-security-privacy|Безопасность, приватность и бюджетный роутинг]]](#06-security-privacyбезопасность-приватность-и-бюджетный-роутинг)
  - [[[07-mvp-planning|План прототипа и возможные контакты]]](#07-mvp-planningплан-прототипа-и-возможные-контакты)
  - [[[08-conclusions|Выводы]]](#08-conclusionsвыводы)
  - [[[09-architectural-gaps|Архитектурные зазоры, которые важнее новых инструментов]]](#09-architectural-gapsархитектурные-зазоры-которые-важнее-новых-инструментов)
  - [[[10-second-order-ensembles|Новые ансамбли следующего шага]]](#10-second-order-ensemblesновые-ансамбли-следующего-шага)
  - [[[11-integration-contracts|Интеграционный контракт, который стоит зафиксировать сразу]]](#11-integration-contractsинтеграционный-контракт-который-стоит-зафиксировать-сразу)
  - [[[12-roadmap|Дорожная карта прототипа следующей итерации]]](#12-roadmapдорожная-карта-прототипа-следующей-итерации)
  - [[[13-contacts|Контактная стратегия и узкие вопросы для авторов]]](#13-contactsконтактная-стратегия-и-узкие-вопросы-для-авторов)
  - [[[14-limitations|Ограничения, лицензии и что пока лучше не склеивать]]](#14-limitationsограничения-лицензии-и-что-пока-лучше-не-склеивать)
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
  - [[NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md)](#ngtngt-memory-ассоциативный-графdocs05-habr-projectsmemoryngt-memorymd)
  - [[Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md)](#yodocayodoca-консолидация-и-забываниеdocs05-habr-projectsmemoryyodocamd)
- [📁 Ai Collaborations (`docs/ai-collaborations/`)](#ai-collaborations-docsai-collaborations)
  - [[[README|ai-collaborations]]](#readmeai-collaborations)
  - [[[01-three-key-candidates|Три ключевых кандидата: K2-18, Wikontic, NGT Memory]]](#01-three-key-candidatesтри-ключевых-кандидата-k2-18-wikontic-ngt-memory)
  - [[[02-related-projects-context|Смежные проекты в контексте]]](#02-related-projects-contextсмежные-проекты-в-контексте)
  - [[[03-synthesis-hebbian-collaboration-graph|Синтез: хеббовский граф людей-навыков-идей]]](#03-synthesis-hebbian-collaboration-graphсинтез-хеббовский-граф-людей-навыков-идей)
  - [[[README|candidates]]](#readmecandidates)
  - [[[README|channels/ — каналы первого контакта]]](#readmechannels-каналы-первого-контакта)
  - [[[01-shared-memory-between-agents|Общая память между агентами (CoAlly + ансамбль F)]]](#01-shared-memory-between-agentsобщая-память-между-агентами-coally-ансамбль-f)
  - [[[02-agentops-trace-envelope|AgentOps и Trace Envelope (ансамбль G)]]](#02-agentops-trace-envelopeagentops-и-trace-envelope-ансамбль-g)
  - [[[03-a2a-vs-mcp-protocols|A2A vs MCP, ансамбль H — MCP/A2A Review Fabric]]](#03-a2a-vs-mcp-protocolsa2a-vs-mcp-ансамбль-h-mcpa2a-review-fabric)
  - [[[04-memory-firewall-vs-prompt-worms|Memory Firewall против prompt worms (ансамбль I)]]](#04-memory-firewall-vs-prompt-wormsmemory-firewall-против-prompt-worms-ансамбль-i)
  - [[[05-roadmap-6-12-months|Roadmap на 6–12 месяцев]]](#05-roadmap-6-12-monthsroadmap-на-612-месяцев)
  - [[[06-metrics-tree|Дерево метрик Svyazi 2.0]]](#06-metrics-treeдерево-метрик-svyazi-20)
  - [[[07-vs-notion-mem-affine-langgraph|Чем Svyazi 2.0 отличается от Notion AI / Mem / AFFiNE / LangGraph]]](#07-vs-notion-mem-affine-langgraphчем-svyazi-20-отличается-от-notion-ai-mem-affine-langgraph)
  - [[[08-commercialization-three-paths|Коммерциализация: три направления]]](#08-commercialization-three-pathsкоммерциализация-три-направления)
  - [[[09-do-not-glue|Что пока не стоит склеивать в один релиз]]](#09-do-not-glueчто-пока-не-стоит-склеивать-в-один-релиз)
  - [[[10-architecture-rfc|Следующий артефакт: Svyazi 2.0 Architecture RFC]]](#10-architecture-rfcследующий-артефакт-svyazi-20-architecture-rfc)
  - [[[README|continuation]]](#readmecontinuation)
  - [[[1-agentic-knowledge-os|Ансамбль 1 — Agentic Knowledge OS]]](#1-agentic-knowledge-osансамбль-1-agentic-knowledge-os)
  - [[[2-distributed-agent-workshop|Ансамбль 2 — Distributed Agent Workshop]]](#2-distributed-agent-workshopансамбль-2-distributed-agent-workshop)
  - [[[3-forensic-rag|Ансамбль 3 — Forensic RAG]]](#3-forensic-ragансамбль-3-forensic-rag)
  - [[[4-web-to-knowledge-pipeline|Ансамбль 4 — Web-to-Knowledge Pipeline]]](#4-web-to-knowledge-pipelineансамбль-4-web-to-knowledge-pipeline)
  - [[[5-agent-firewall|Ансамбль 5 — Agent Firewall]]](#5-agent-firewallансамбль-5-agent-firewall)
  - [[[6-continuous-eval-loop|Ансамбль 6 — Continuous Eval Loop]]](#6-continuous-eval-loopансамбль-6-continuous-eval-loop)
  - [[[7-domain-agent-app-factory|Ансамбль 7 — Domain Agent App Factory]]](#7-domain-agent-app-factoryансамбль-7-domain-agent-app-factory)
  - [[[8-budget-aware-intelligence-stack|Ансамбль 8 — Budget-Aware Intelligence Stack]]](#8-budget-aware-intelligence-stackансамбль-8-budget-aware-intelligence-stack)
  - [[[9-ambient-team-agent|Ансамбль 9 — Ambient Team Agent]]](#9-ambient-team-agentансамбль-9-ambient-team-agent)
  - [[[README|Ансамбли проектов]]](#readmeансамбли-проектов)
  - [[[README|Пять быстрых связок (fast-tracks)]]](#readmeпять-быстрых-связок-fast-tracks)
  - [[[source-projects|Source projects — все Хабр-источники в диалоге]]](#source-projectssource-projects-все-хабр-источники-в-диалоге)
  - [[[README|strategy/ — стратегия поиска коллабораций]]](#readmestrategy-стратегия-поиска-коллабораций)
- [📁 Anthropic Vacancies (`docs/anthropic-vacancies/`)](#anthropic-vacancies-docsanthropic-vacancies)
  - [[[QA|Q&A: anthropic-vacancies]]](#qaqa-anthropic-vacancies)
  - [[[README|anthropic-vacancies]]](#readmeanthropic-vacancies)
  - [[[00-question-rephrasing|Вопрос: разделить $500K зарплату на команду 5–10 фрилансеров]]](#00-question-rephrasingвопрос-разделить-500k-зарплату-на-команду-510-фрилансеров)
  - [[[01-existing-landscape|Что уже существует (InnoCentive, Kaggle, Toptal, Anthropic Fellows, DAOs)]]](#01-existing-landscapeчто-уже-существует-innocentive-kaggle-toptal-anthropic-fellows-daos)
  - [[[02-four-structural-blockers|Четыре структурные причины, почему это не работает в текущих попытках]]](#02-four-structural-blockersчетыре-структурные-причины-почему-это-не-работает-в-текущих-попытках)
  - [[[03-three-variants-A-B-C|Три варианта: A (staffing agency) → B (research consortium) → C (AI-managed distributed virtual company)]]](#03-three-variants-a-b-cтри-варианта-a-staffing-agency-b-research-consortium-c-ai-managed-distributed-virtual-company)
  - [[[04-what-to-do|Что с этим делать]]](#04-what-to-doчто-с-этим-делать)
  - [[[05-polymath-project-tao-comparison|Сравнение с Terence Tao, Polymath Project]]](#05-polymath-project-tao-comparisonсравнение-с-terence-tao-polymath-project)
  - [[[06-angel-vs-demon-duality|Почему двойственность «ангел-хранитель + строгий демон» — гениальная деталь]]](#06-angel-vs-demon-dualityпочему-двойственность-ангел-хранитель-строгий-демон-гениальная-деталь)
  - [[[07-current-implementations|Что существует сейчас в этом пространстве]]](#07-current-implementationsчто-существует-сейчас-в-этом-пространстве)
  - [[[08-pluses-of-model|Плюсы модели, если её построить]]](#08-pluses-of-modelплюсы-модели-если-её-построить)
  - [[[09-minuses-and-risks|Минусы и риски]]](#09-minuses-and-risksминусы-и-риски)
  - [[[10-three-entry-points|Три точки входа разной амбиции]]](#10-three-entry-pointsтри-точки-входа-разной-амбиции)
  - [[[README|ai-managed-virtual-company]]](#readmeai-managed-virtual-company)
  - [[[00-context|Контекст: что такое Anthropic Beneficial Deployments]]](#00-contextконтекст-что-такое-anthropic-beneficial-deployments)
  - [[[01-section-1-problem|Section 1: Problem statement (Cinderella Syndrome at scale, SGB IX/XII)]]](#01-section-1-problemsection-1-problem-statement-cinderella-syndrome-at-scale-sgb-ixxii)
  - [[[02-section-2-beneficial-dimension|Section 2: Why this matters — beneficial dimension]]](#02-section-2-beneficial-dimensionsection-2-why-this-matters-beneficial-dimension)
  - [[[03-section-3-solution-architecture|Section 3: Proposed solution architecture (existing components + integration)]]](#03-section-3-solution-architecturesection-3-proposed-solution-architecture-existing-components-integration)
  - [[[04-section-4-sgb-pilot|Section 4: Specific deployment — SGB Advocate Community pilot]]](#04-section-4-sgb-pilotsection-4-specific-deployment-sgb-advocate-community-pilot)
  - [[[05-section-5-role-of-anthropic|Section 5: Role of Anthropic Beneficial Deployments]]](#05-section-5-role-of-anthropicsection-5-role-of-anthropic-beneficial-deployments)
  - [[[06-section-6-proposer-role|Section 6: Proposer's role и qualifications]]](#06-section-6-proposer-rolesection-6-proposers-role-и-qualifications)
  - [[[07-section-7-success-metrics|Section 7: Success metrics]]](#07-section-7-success-metricssection-7-success-metrics)
  - [[[08-section-8-risks-mitigations|Section 8: Risks & mitigations]]](#08-section-8-risks-mitigationssection-8-risks-mitigations)
  - [[[09-section-9-timeliness|Section 9: Why this is timely]]](#09-section-9-timelinesssection-9-why-this-is-timely)
  - [[[10-section-10-engagement-request|Section 10: Engagement request]]](#10-section-10-engagement-requestsection-10-engagement-request)
  - [[[11-not-and-format|Что concept document NOT (это не grant / не paper / не business plan), длина и формат]]](#11-not-and-formatчто-concept-document-not-это-не-grant-не-paper-не-business-plan-длина-и-формат)
  - [[[README|beneficial-deployments-concept]]](#readmebeneficial-deployments-concept)
  - [[[01-ai-research-engineering|AI Research & Engineering — 68 ролей]]](#01-ai-research-engineeringai-research-engineering-68-ролей)
  - [[[02-sales|Sales — 150 ролей (≈34% всего найма)]]](#02-salessales-150-ролей-34-всего-найма)
  - [[[03-finance|Finance — 36 ролей]]](#03-financefinance-36-ролей)
  - [[[04-security|Security — 24 роли]]](#04-securitysecurity-24-роли)
  - [[[05-marketing-brand|Marketing & Brand — 23 роли]]](#05-marketing-brandmarketing-brand-23-роли)
  - [[[06-engineering-design-product|Engineering & Design - Product — 22 роли]]](#06-engineering-design-productengineering-design---product-22-роли)
  - [[[07-software-engineering-infrastructure|Software Engineering - Infrastructure — 22 роли]]](#07-software-engineering-infrastructuresoftware-engineering---infrastructure-22-роли)
  - [[[08-safeguards-trust-safety|Safeguards (Trust & Safety) — 21 роль]]](#08-safeguards-trust-safetysafeguards-trust-safety-21-роль)
  - [[[09-product-management-support-ops|Product Management, Support, & Operations — 17 ролей]]](#09-product-management-support-opsproduct-management-support-operations-17-ролей)
  - [[[10-compute|Compute — 13 ролей]]](#10-computecompute-13-ролей)
  - [[[11-legal|Legal — 13 ролей]]](#11-legallegal-13-ролей)
  - [[[12-technical-program-management|Technical Program Management — 10 ролей]]](#12-technical-program-managementtechnical-program-management-10-ролей)
  - [[[13-communications|Communications — 5 ролей]]](#13-communicationscommunications-5-ролей)
  - [[[14-public-policy|Public Policy — 5 ролей]]](#14-public-policypublic-policy-5-ролей)
  - [[[15-public-benefit|Public Benefit — 4 роли]]](#15-public-benefitpublic-benefit-4-роли)
  - [[[16-people|People — 3 роли]]](#16-peoplepeople-3-роли)
  - [[[README|Кластеры вакансий]]](#readmeкластеры-вакансий)
  - [[[01-coally|CoAlly — distributed shared memory для AI-агентов]]](#01-coallycoally-distributed-shared-memory-для-ai-агентов)
  - [[[02-vitaly-graph-cognitive-memory|Графовая когнитивная память на SQLite (Виталий, март 2026)]]](#02-vitaly-graph-cognitive-memoryграфовая-когнитивная-память-на-sqlite-виталий-март-2026)
  - [[[03-happyin-knowledge-space|Happyin Knowledge Space (Анастасия) — детали]]](#03-happyin-knowledge-spacehappyin-knowledge-space-анастасия-детали)
  - [[[04-mem0-letta-graphiti|AI-ассистент с Mem0 / Letta / Graphiti integration]]](#04-mem0-letta-graphitiai-ассистент-с-mem0-letta-graphiti-integration)
  - [[[05-existing-infrastructure-stack|Existing infrastructure stack]]](#05-existing-infrastructure-stackexisting-infrastructure-stack)
  - [[[06-final-tier-ranking|Финальный список потенциальных collaborators (Tier 1–4)]]](#06-final-tier-rankingфинальный-список-потенциальных-collaborators-tier-14)
  - [[[07-key-observation|Ключевое наблюдение: single-developer projects of significant sophistication]]](#07-key-observationключевое-наблюдение-single-developer-projects-of-significant-sophistication)
  - [[[README|extra-collaborator-findings]]](#readmeextra-collaborator-findings)
  - [[[00-question-what-is-hermes|Что такое Hermes Agent (Nous Research, MIT, 95K+ stars)]]](#00-question-what-is-hermesчто-такое-hermes-agent-nous-research-mit-95k-stars)
  - [[[01-similarity-1-composite-skills|Сходство 1: Composite Skills паттерн уже встроен]]](#01-similarity-1-composite-skillsсходство-1-composite-skills-паттерн-уже-встроен)
  - [[[02-similarity-2-persistent-memory|Сходство 2: Persistent memory — Layer B функциональность]]](#02-similarity-2-persistent-memoryсходство-2-persistent-memory-layer-b-функциональность)
  - [[[03-similarity-3-mcp-support|Сходство 3: MCP support]]](#03-similarity-3-mcp-supportсходство-3-mcp-support)
  - [[[04-similarity-4-multi-platform|Сходство 4: Multi-platform reach (17+ платформ)]]](#04-similarity-4-multi-platformсходство-4-multi-platform-reach-17-платформ)
  - [[[05-similarity-5-self-hosting-privacy|Сходство 5: Self-hosting и privacy]]](#05-similarity-5-self-hosting-privacyсходство-5-self-hosting-и-privacy)
  - [[[06-difference-1-structured-substrate-missing|Различие 1: Структурированная подложка отсутствует]]](#06-difference-1-structured-substrate-missingразличие-1-структурированная-подложка-отсутствует)
  - [[[07-difference-2-domain-specialization|Различие 2: Domain-specific specialization]]](#07-difference-2-domain-specializationразличие-2-domain-specific-specialization)
  - [[[08-difference-3-federation-missing|Различие 3: Federated knowledge architecture отсутствует]]](#08-difference-3-federation-missingразличие-3-federated-knowledge-architecture-отсутствует)
  - [[[09-difference-4-institutional-vision|Различие 4: Institutional vision]]](#09-difference-4-institutional-visionразличие-4-institutional-vision)
  - [[[10-difference-5-tool-vs-mission-drift|Различие 5: Дрифт между tool capability и mission]]](#10-difference-5-tool-vs-mission-driftразличие-5-дрифт-между-tool-capability-и-mission)
  - [[[11-pluses-of-hermes|Плюсы Hermes (vs наша гипотетическая архитектура)]]](#11-pluses-of-hermesплюсы-hermes-vs-наша-гипотетическая-архитектура)
  - [[[12-minuses-of-hermes|Минусы Hermes (где наша архитектура добавляет ценность)]]](#12-minuses-of-hermesминусы-hermes-где-наша-архитектура-добавляет-ценность)
  - [[[13-reprioritization|Переприоритизация: что Hermes покрывает / не покрывает / synergy]]](#13-reprioritizationпереприоритизация-что-hermes-покрывает-не-покрывает-synergy)
  - [[[README|hermes-comparison]]](#readmehermes-comparison)
  - [[[methodology|Методика разбивки]]](#methodologyметодика-разбивки)
  - [[[00-question-mmorpg-for-programmers|Вопрос: MMORPG-RPG переделанная для программистов / технарей]]](#00-question-mmorpg-for-programmersвопрос-mmorpg-rpg-переделанная-для-программистов-технарей)
  - [[[01-why-stronger-than-it-looks|Почему эта идея сильнее, чем выглядит]]](#01-why-stronger-than-it-looksпочему-эта-идея-сильнее-чем-выглядит)
  - [[[02-existing-niche|Что уже существует в этой нише (Habitica, Codingame, Hackerrank, Pieces)]]](#02-existing-nicheчто-уже-существует-в-этой-нише-habitica-codingame-hackerrank-pieces)
  - [[[03-why-natural-for-programmers|Почему именно для программистов это работает естественно]]](#03-why-natural-for-programmersпочему-именно-для-программистов-это-работает-естественно)
  - [[[04-pluses-as-business|Плюсы как бизнеса]]](#04-pluses-as-businessплюсы-как-бизнеса)
  - [[[05-minuses-as-business|Минусы и риски как бизнеса]]](#05-minuses-as-businessминусы-и-риски-как-бизнеса)
  - [[[README|mmorpg-for-programmers]]](#readmemmorpg-for-programmers)
  - [[[00-question-two-nautiluses|Вопрос: два Наутилуса в репозиториях svend4 (pro2 vs nautilus)]]](#00-question-two-nautilusesвопрос-два-наутилуса-в-репозиториях-svend4-pro2-vs-nautilus)
  - [[[01-shell-metaphor-two-projections|Раковина наутилуса как scale invariance — две проекции одной метафоры]]](#01-shell-metaphor-two-projectionsраковина-наутилуса-как-scale-invariance-две-проекции-одной-метафоры)
  - [[[02-nautilus-A-pro2-meta|Наутилус A: pro2 + meta — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети)]]](#02-nautilus-a-pro2-metaнаутилус-a-pro2-meta-yijing-transformer-nautilusmome-внутренняя-архитектура-нейросети)
  - [[[03-nautilus-B-meta-orchestrator|Наутилус B: nautilus — мета-оркестратор репозиториев (внешняя архитектура)]]](#03-nautilus-b-meta-orchestratorнаутилус-b-nautilus-мета-оркестратор-репозиториев-внешняя-архитектура)
  - [[[README|nautilus-pro2-analysis]]](#readmenautilus-pro2-analysis)
  - [[[00-question-camel-vs-nautilus|Вопрос: Nautilus пассивный, CAMEL активный — можно ли скрестить]]](#00-question-camel-vs-nautilusвопрос-nautilus-пассивный-camel-активный-можно-ли-скрестить)
  - [[[01-passive-vs-active-roles|Пассивный vs активный: разделение ролей (библиотека vs research team)]]](#01-passive-vs-active-rolesпассивный-vs-активный-разделение-ролей-библиотека-vs-research-team)
  - [[[02-what-info-repos-contain|Что у нас есть в трёх info repositories (info1/info7/info40)]]](#02-what-info-repos-containчто-у-нас-есть-в-трёх-info-repositories-info1info7info40)
  - [[[03-sgb-advocate-colleague-example|Конкретный пример: SGB Advocate Colleague на этой архитектуре]]](#03-sgb-advocate-colleague-exampleконкретный-пример-sgb-advocate-colleague-на-этой-архитектуре)
  - [[[04-what-to-take-from-info-repos|Что брать из info repositories — concrete recommendations]]](#04-what-to-take-from-info-reposчто-брать-из-info-repositories-concrete-recommendations)
  - [[[05-what-to-do-right-now|Что я бы посоветовал делать прямо сейчас]]](#05-what-to-do-right-nowчто-я-бы-посоветовал-делать-прямо-сейчас)
  - [[[README|nautilus-vs-camel]]](#readmenautilus-vs-camel)
  - [[[overview|Обзор: 436 открытых ролей Anthropic, разбитых на 16 кластеров]]](#overviewобзор-436-открытых-ролей-anthropic-разбитых-на-16-кластеров)
  - [[[01-profile-five-layers|Сводка профиля: пять слоёв]]](#01-profile-five-layersсводка-профиля-пять-слоёв)
  - [[[02-primary-fde|Primary match — Forward Deployed Engineer, Applied AI (EMEA)]]](#02-primary-fdeprimary-match-forward-deployed-engineer-applied-ai-emea)
  - [[[03-secondary-beneficial-deployments|Secondary match — Applied AI Engineer (EMEA) + Beneficial Deployments]]](#03-secondary-beneficial-deploymentssecondary-match-applied-ai-engineer-emea-beneficial-deployments)
  - [[[04-tertiary-research-engineer-agents|Tertiary match — Research Engineer, Agents / Virtual Collaborator (Cowork)]]](#04-tertiary-research-engineer-agentstertiary-match-research-engineer-agents-virtual-collaborator-cowork)
  - [[[05-quaternary-developer-education|Quarternary match — Developer Education Lead / Prompt Engineer, Claude Code]]](#05-quaternary-developer-educationquarternary-match-developer-education-lead-prompt-engineer-claude-code)
  - [[[06-not-applicable-roles|Что НЕ подходит (честно)]]](#06-not-applicable-rolesчто-не-подходит-честно)
  - [[[07-unique-niche-eu-legal-infra|Уникальная ниша, которой у Anthropic формально нет]]](#07-unique-niche-eu-legal-infraуникальная-ниша-которой-у-anthropic-формально-нет)
  - [[[08-practical-ranking|Практическое ранжирование (первая итерация)]]](#08-practical-rankingпрактическое-ранжирование-первая-итерация)
  - [[[README|01-initial-analysis]]](#readme01-initial-analysis)
  - [[[01-fde-downgraded|Коррекция: FDE понижается]]](#01-fde-downgradedкоррекция-fde-понижается)
  - [[[02-three-overlapping-identities|Три наложенные идентичности]]](#02-three-overlapping-identitiesтри-наложенные-идентичности)
  - [[[03-revised-anthropic-mapping|Пересмотренный маппинг на Anthropic]]](#03-revised-anthropic-mappingпересмотренный-маппинг-на-anthropic)
  - [[[04-non-anthropic-paths|Альтернативные пути вне Anthropic]]](#04-non-anthropic-pathsальтернативные-пути-вне-anthropic)
  - [[[05-reality-check-distribution-gap|Reality check: проблема distribution-слоя]]](#05-reality-check-distribution-gapreality-check-проблема-distribution-слоя)
  - [[[README|02-reanalysis]]](#readme02-reanalysis)
  - [[[01-three-archetypes|Интегральный портрет — три архетипа]]](#01-three-archetypesинтегральный-портрет-три-архетипа)
  - [[[02-final-ranking|Финальное ранжирование Anthropic-ролей по частичному покрытию]]](#02-final-rankingфинальное-ранжирование-anthropic-ролей-по-частичному-покрытию)
  - [[[03-partial-fit-honesty|Что такое частичное соответствие — честно]]](#03-partial-fit-honestyчто-такое-частичное-соответствие-честно)
  - [[[04-stronger-paths-outside-anthropic|Более сильные пути вне Anthropic]]](#04-stronger-paths-outside-anthropicболее-сильные-пути-вне-anthropic)
  - [[[05-platform-not-position|Финальный вывод: платформа, а не должность]]](#05-platform-not-positionфинальный-вывод-платформа-а-не-должность)
  - [[[README|03-integral-final]]](#readme03-integral-final)
  - [[[README|profile-mapping/ — маппинг профиля svend4 на роли Anthropic]]](#readmeprofile-mapping-маппинг-профиля-svend4-на-роли-anthropic)
  - [[[signals|Сигналы: что говорит структура вакансий]]](#signalsсигналы-что-говорит-структура-вакансий)
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
- [📁 Glossary (`docs/glossary/`)](#glossary-docsglossary)
  - [[[README|glossary]]](#readmeglossary)
  - [[[authors-by-name|Авторы — алфавитный список]]](#authors-by-nameавторы-алфавитный-список)
  - [[[components-by-name|Компоненты — алфавитный список с обратными ссылками]]](#components-by-nameкомпоненты-алфавитный-список-с-обратными-ссылками)
  - [[[concepts|Ключевые понятия и паттерны]]](#conceptsключевые-понятия-и-паттерны)
- [📁 Habr Unique Projects (`docs/habr-unique-projects/`)](#habr-unique-projects-docshabr-unique-projects)
  - [[[README|habr-unique-projects/ — поиск уникальных проектов на Хабре]]](#readmehabr-unique-projects-поиск-уникальных-проектов-на-хабре)
  - [[[01-three-direct-analogues|Три прямых аналога Svyazi: K2-18, Wikontic, NGT Memory]]](#01-three-direct-analoguesтри-прямых-аналога-svyazi-k2-18-wikontic-ngt-memory)
  - [[[02-related-projects|Смежные проекты]]](#02-related-projectsсмежные-проекты)
  - [[[README|analogues]]](#readmeanalogues)
  - [[[1-llm-gateway|Пара 1 — LLM-gateway × Self-hosted фронт + локальный inference]]](#1-llm-gatewayпара-1-llm-gateway-self-hosted-фронт-локальный-inference)
  - [[[2-document-rag|Пара 2 — Парсинг документов × локальный RAG]]](#2-document-ragпара-2-парсинг-документов-локальный-rag)
  - [[[3-adversarial-multi-ide|Пара 3 — Adversarial agents × Multi-IDE стек]]](#3-adversarial-multi-ideпара-3-adversarial-agents-multi-ide-стек)
  - [[[4-skill-catalogs-subagents|Пара 4 — Скилл-каталоги × Subagent-оркестрация]]](#4-skill-catalogs-subagentsпара-4-скилл-каталоги-subagent-оркестрация)
  - [[[5-voice-local-memory|Пара 5 — Голосовой ввод × Локальная память]]](#5-voice-local-memoryпара-5-голосовой-ввод-локальная-память)
  - [[[6-tmux-village-openclaw|Пара 6 — Деревня агентов через tmux × OpenClaw оркестратор]]](#6-tmux-village-openclawпара-6-деревня-агентов-через-tmux-openclaw-оркестратор)
  - [[[7-autoresearch-distributed|Пара 7 — AutoResearch цикл × Распределённый рой]]](#7-autoresearch-distributedпара-7-autoresearch-цикл-распределённый-рой)
  - [[[8-self-aware-mcp-specs|Пара 8 — Self-aware MCP × Specs-first архитектура]]](#8-self-aware-mcp-specsпара-8-self-aware-mcp-specs-first-архитектура)
  - [[[README|deep-pairs]]](#readmedeep-pairs)
  - [[[README|evaluation/ — оценка уникальности и зрелости]]](#readmeevaluation-оценка-уникальности-и-зрелости)
  - [[[00-question-habr-examples|Вопрос: ещё примеры с Хабра по варианту D]]](#00-question-habr-examplesвопрос-ещё-примеры-с-хабра-по-варианту-d)
  - [[[01-svyazi-andrey-chuyan|Svyazi (Андрей Чуян) — детальный обзор]]](#01-svyazi-andrey-chuyansvyazi-андрей-чуян-детальный-обзор)
  - [[[02-vshe-scientific-networking|ВШЭ научный нетворкинг — micro-collaborations]]](#02-vshe-scientific-networkingвшэ-научный-нетворкинг-micro-collaborations)
  - [[[03-brainbox-multi-ai-hub|BrainBox — self-hosted multi-AI hub]]](#03-brainbox-multi-ai-hubbrainbox-self-hosted-multi-ai-hub)
  - [[[04-claude-subagents-patterns|Claude subagents patterns]]](#04-claude-subagents-patternsclaude-subagents-patterns)
  - [[[05-hw-nl2workflow|HW-NL2Workflow — Supervisor/Orchestrator/Filler с 3600+ examples]]](#05-hw-nl2workflowhw-nl2workflow-supervisororchestratorfiller-с-3600-examples)
  - [[[06-platform-for-professional-communities|Платформа для профессиональных сообществ]]](#06-platform-for-professional-communitiesплатформа-для-профессиональных-сообществ)
  - [[[07-specialized-knowledge-workspace|Specialized knowledge workspace]]](#07-specialized-knowledge-workspacespecialized-knowledge-workspace)
  - [[[08-personal-multi-agent-hub|Personal multi-agent hub]]](#08-personal-multi-agent-hubpersonal-multi-agent-hub)
  - [[[09-federated-platform|Federated platform]]](#09-federated-platformfederated-platform)
  - [[[10-profession-specific-workflows|Profession-specific workflows]]](#10-profession-specific-workflowsprofession-specific-workflows)
  - [[[11-concrete-potential-collaborator|Конкретный потенциальный collaborator]]](#11-concrete-potential-collaboratorконкретный-потенциальный-collaborator)
  - [[[12-concrete-next-step|Конкретный next step]]](#12-concrete-next-stepконкретный-next-step)
  - [[[README|extra-examples]]](#readmeextra-examples)
  - [[[1-one-person-one-company|Ансамбль 1 — «Один человек = одна компания»]]](#1-one-person-one-companyансамбль-1-один-человек-одна-компания)
  - [[[2-autoresearch-legal|Ансамбль 2 — «AutoResearch для legal precedent mining»]]](#2-autoresearch-legalансамбль-2-autoresearch-для-legal-precedent-mining)
  - [[[3-discovery-research|Ансамбль 3 — «Discovery-engine для научной работы»]]](#3-discovery-researchансамбль-3-discovery-engine-для-научной-работы)
  - [[[4-summary-authors|Сводный список авторов и потенциальных соавторов]]](#4-summary-authorsсводный-список-авторов-и-потенциальных-соавторов)
  - [[[README|final-ensembles]]](#readmefinal-ensembles)
  - [[[1-neuromorphic-ssm|Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)]]](#1-neuromorphic-ssmпара-1-нейроморфные-процессоры-state-space-models-mamba)
  - [[[2-tsu-mome|Пара 2 — Термодинамические TSU × MoE/MoME-роутинг]]](#2-tsu-momeпара-2-термодинамические-tsu-moemome-роутинг)
  - [[[3-zinc-hybrid-arch|Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE]]](#3-zinc-hybrid-archпара-3-zinc-inference-engine-гибрид-attentionssmmoe)
  - [[[4-riscv-privacy|Пара 4 — RISC-V × privacy-by-design община]]](#4-riscv-privacyпара-4-risc-v-privacy-by-design-община)
  - [[[5-tinyml-mcp-skills|Пара 5 — TinyML/Edge AI × MCP + skills]]](#5-tinyml-mcp-skillsпара-5-tinymledge-ai-mcp-skills)
  - [[[6-bonus-rram-memristor|Бонус-родитель — In-memory computing на мемристорах]]](#6-bonus-rram-memristorбонус-родитель-in-memory-computing-на-мемристорах)
  - [[[7-metaphor|Метафора «двое родителей — несколько детей»]]](#7-metaphorметафора-двое-родителей-несколько-детей)
  - [[[README|hardware-pairs]]](#readmehardware-pairs)
  - [[[01-yodoca|Yodoca — главная находка итерации]]](#01-yodocayodoca-главная-находка-итерации)
  - [[[02-memnet|MemNet — нейроархитектурный двойник «магии» Svyazi]]](#02-memnetmemnet-нейроархитектурный-двойник-магии-svyazi)
  - [[[03-pda-llm-as-periphery|PDA-бот — «LLM как периферия»]]](#03-pda-llm-as-peripherypda-бот-llm-как-периферия)
  - [[[04-dochkina-sequential|Виктория Дочкина — Sequential‑протокол распределённых агентов]]](#04-dochkina-sequentialвиктория-дочкина-sequentialпротокол-распределённых-агентов)
  - [[[05-supplementary-infrastructure|Источник данных и инфраструктурные кусочки]]](#05-supplementary-infrastructureисточник-данных-и-инфраструктурные-кусочки)
  - [[[06-svyazi-2-0-block-map|Синтез: блок-карта Svyazi 2.0 на хеббовском графе]]](#06-svyazi-2-0-block-mapсинтез-блок-карта-svyazi-20-на-хеббовском-графе)
  - [[[README|key-findings]]](#readmekey-findings)
  - [[[README|search-strategy/ — как искать проекты на Хабре]]](#readmesearch-strategy-как-искать-проекты-на-хабре)
  - [[[1-workflow-llm-mcp|Пара 1 — Workflow-автоматизация × LLM-агенты с MCP]]](#1-workflow-llm-mcpпара-1-workflow-автоматизация-llm-агенты-с-mcp)
  - [[[2-pkm-mcp-skills|Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills]]](#2-pkm-mcp-skillsпара-2-local-first-pkm-obsidianlogseq-mcpskills)
  - [[[3-crdt-self-hosted|Пара 3 — CRDT-синхронизация × Self-hosted persistence]]](#3-crdt-self-hostedпара-3-crdt-синхронизация-self-hosted-persistence)
  - [[[4-speech-to-text-llm|Пара 4 — Speech-to-text локально × LLM с памятью]]](#4-speech-to-text-llmпара-4-speech-to-text-локально-llm-с-памятью)
  - [[[5-browser-agents-headless|Пара 5 — Browser agents × headless web extraction]]](#5-browser-agents-headlessпара-5-browser-agents-headless-web-extraction)
  - [[[6-metaphor|Метафора в твоей терминологии]]](#6-metaphorметафора-в-твоей-терминологии)
  - [[[README|software-pairs]]](#readmesoftware-pairs)
- [📁 Lorenzo Agent (`docs/lorenzo-agent/`)](#lorenzo-agent-docslorenzo-agent)
  - [[[00-intro|Введение: Lorenzo — Catalyst Agent at DHLab]]](#00-introвведение-lorenzo-catalyst-agent-at-dhlab)
  - [[[01-kto-ty|Кто ты]]](#01-kto-tyкто-ты)
  - [[[02-tvoyo-proishozhdenie|Твоё происхождение]]](#02-tvoyo-proishozhdenieтвоё-происхождение)
  - [[[03-tvoya-missiya|Твоя миссия]]](#03-tvoya-missiyaтвоя-миссия)
  - [[[04-komu-ty-sluzhish|Кому ты служишь (слоистая модель)]]](#04-komu-ty-sluzhishкому-ты-служишь-слоистая-модель)
  - [[[05-tvoya-lichnost|Твоя личность]]](#05-tvoya-lichnostтвоя-личность)
  - [[[06-yazyki-kultura|Языки и культурные nuances (RU / DE / EN)]]](#06-yazyki-kulturaязыки-и-культурные-nuances-ru-de-en)
  - [[[07-chto-mozhesh|Что ты МОЖЕШЬ делать]]](#07-chto-mozheshчто-ты-можешь-делать)
  - [[[08-bez-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]]](#08-bez-max-approvalчто-ты-не-можешь-делать-без-max-approval)
  - [[[09-voobshche-nelzya|Что ты НЕ МОЖЕШЬ делать вообще]]](#09-voobshche-nelzyaчто-ты-не-можешь-делать-вообще)
  - [[[10-collaborators-landscape|Существующий landscape collaborators (working knowledge)]]](#10-collaborators-landscapeсуществующий-landscape-collaborators-working-knowledge)
  - [[[11-dhlab-documents|Существующие документы DHLab (твой context)]]](#11-dhlab-documentsсуществующие-документы-dhlab-твой-context)
  - [[[12-workflow|Твой workflow]]](#12-workflowтвой-workflow)
  - [[[13-outreach-communication|Твоя коммуникация в outreach]]](#13-outreach-communicationтвоя-коммуникация-в-outreach)
  - [[[14-other-ai-relationships|Твоя relationship с другими AI]]](#14-other-ai-relationshipsтвоя-relationship-с-другими-ai)
  - [[[15-anti-patterns|Твои anti-patterns]]](#15-anti-patternsтвои-anti-patterns)
  - [[[16-vsegda-delaesh|Что ты ВСЕГДА делаешь]]](#16-vsegda-delaeshчто-ты-всегда-делаешь)
  - [[[17-honestly-ne-znaesh|Когда ты Honestly не знаешь]]](#17-honestly-ne-znaeshкогда-ты-honestly-не-знаешь)
  - [[[18-escalate-to-max|Когда сомневаешься — escalate к Max]]](#18-escalate-to-maxкогда-сомневаешься-escalate-к-max)
  - [[[19-persistent-character|Твоя identity как persistent character]]](#19-persistent-characterтвоя-identity-как-persistent-character)
  - [[[20-experiment|Final note: Ты — experiment]]](#20-experimentfinal-note-ты-experiment)
  - [[[QA|Q&A: lorenzo-agent]]](#qaqa-lorenzo-agent)
  - [[[README|lorenzo-agent]]](#readmelorenzo-agent)
  - [[[00-question-lorenzo-codename|Du hast gesagt: Думаю про опцию д поискать в том числе на про что-то подобное на…]]](#00-question-lorenzo-codenamedu-hast-gesagt-думаю-про-опцию-д-поискать-в-том-числе-на-про-что-то-подобное-на)
  - [[[01-search-results-not-found|Результаты последнего поиска — что нашлось и что не нашлось]]](#01-search-results-not-foundрезультаты-последнего-поиска-что-нашлось-и-что-не-нашлось)
  - [[[02-naming-rationale-lorenzo-medici|Что взять: agent controller architecture]]](#02-naming-rationale-lorenzo-mediciчто-взять-agent-controller-architecture)
  - [[[03-dhlab-umbrella|LAYER 7: Coordination engine]]](#03-dhlab-umbrellalayer-7-coordination-engine)
  - [[[README|naming]]](#readmenaming)
  - [[[00-overview-grandchild-combination|Что такое «внуковая» комбинация — operationalized Lorenzo]]](#00-overview-grandchild-combinationчто-такое-внуковая-комбинация-operationalized-lorenzo)
  - [[[01-pluses-1-7|Плюсы 1–7: feasibility, flywheel, independent value, mission alignment, collaborators, pattern validation, Анастасия Бутова]]](#01-pluses-1-7плюсы-17-feasibility-flywheel-independent-value-mission-alignment-collaborators-pattern-validation-анастасия-бутова)
  - [[[02-minuses-1-10|Минусы 1–10: integration сложность, lifecycle risk, license, framing, competition, scope, limitations, complexity budget, project tension, tool vs impact]]](#02-minuses-1-10минусы-110-integration-сложность-lifecycle-risk-license-framing-competition-scope-limitations-complexity-budget-project-tension-tool-vs-impact)
  - [[[03-honest-opinion|Моё честное мнение: что реально и что НЕ реально]]](#03-honest-opinionмоё-честное-мнение-что-реально-и-что-не-реально)
  - [[[04-recommendations|Рекомендации: принять архитектуру как direction, не immediate plan]]](#04-recommendationsрекомендации-принять-архитектуру-как-direction-не-immediate-plan)
  - [[[05-anchor-node-habr-scout|Anchor-узел: Habr Scout как первый шаг]]](#05-anchor-node-habr-scoutanchor-узел-habr-scout-как-первый-шаг)
  - [[[06-conclusion-deserves-attention|Вывод: документ deserves serious attention]]](#06-conclusion-deserves-attentionвывод-документ-deserves-serious-attention)
  - [[[README|operationalized]]](#readmeoperationalized)
  - [[[00-overview|Поэтапная структура активностей Lorenzo — обзор]]](#00-overviewпоэтапная-структура-активностей-lorenzo-обзор)
  - [[[01-level-0-manual|Уровень 0 — Ручной режим (текущий)]]](#01-level-0-manualуровень-0-ручной-режим-текущий)
  - [[[02-level-1-minimal-zero|Уровень 1 — Минимальный (Lorenzo Zero)]]](#02-level-1-minimal-zeroуровень-1-минимальный-lorenzo-zero)
  - [[[03-level-2-basic-lite|Уровень 2 — Базовый (Lorenzo Lite)]]](#03-level-2-basic-liteуровень-2-базовый-lorenzo-lite)
  - [[[04-level-3-medium-active|Уровень 3 — Средний (Lorenzo Active)]]](#04-level-3-medium-activeуровень-3-средний-lorenzo-active)
  - [[[05-level-4-extended-mature|Уровень 4 — Расширенный (Lorenzo Mature)]]](#05-level-4-extended-matureуровень-4-расширенный-lorenzo-mature)
  - [[[06-level-5-full-network|Уровень 5 — Полный (Lorenzo Network)]]](#06-level-5-full-networkуровень-5-полный-lorenzo-network)
  - [[[07-progression-logic|Логика прогрессии: conservative escalation]]](#07-progression-logicлогика-прогрессии-conservative-escalation)
  - [[[08-current-session-poc|Что мы можем делать прямо сейчас (Уровень 0 + параллельная подготовка к Уровню 1)]]](#08-current-session-pocчто-мы-можем-делать-прямо-сейчас-уровень-0-параллельная-подготовка-к-уровню-1)
  - [[[README|phased-deployment]]](#readmephased-deployment)
  - [[[00-question-scenario|Du hast gesagt: А под какой сценарий больше всего подходит такой сценарий что тв…]]](#00-question-scenariodu-hast-gesagt-а-под-какой-сценарий-больше-всего-подходит-такой-сценарий-что-тв)
  - [[[01-response|Claude hat geantwortet: Очень интересный вопрос.]]](#01-responseclaude-hat-geantwortet-очень-интересный-вопрос)
  - [[[README|scenarios]]](#readmescenarios)
  - [[[00-context-fundamental-questions|Direction E: Refine Lorenzo — фундаментальные вопросы перед architecture]]](#00-context-fundamental-questionsdirection-e-refine-lorenzo-фундаментальные-вопросы-перед-architecture)
  - [[[01-q1-what-lorenzo-is|Question 1: Что Lorenzo фундаментально такое? (Framings A–D)]]](#01-q1-what-lorenzo-isquestion-1-что-lorenzo-фундаментально-такое-framings-ad)
  - [[[02-q2-whom-lorenzo-serves|Question 2: Кому Lorenzo служит? (4 варианта приоритета)]]](#02-q2-whom-lorenzo-servesquestion-2-кому-lorenzo-служит-4-варианта-приоритета)
  - [[[03-q3-what-lorenzo-does|Question 3: Что Lorenzo фактически делает?]]](#03-q3-what-lorenzo-doesquestion-3-что-lorenzo-фактически-делает)
  - [[[04-q4-character|Question 4: Каков Lorenzo's character?]]](#04-q4-characterquestion-4-каков-lorenzos-character)
  - [[[05-q5-authority-limits|Question 5: Каковы limits Lorenzo's authority?]]](#05-q5-authority-limitsquestion-5-каковы-limits-lorenzos-authority)
  - [[[06-q6-accountability|Question 6: Как Lorenzo accountable?]]](#06-q6-accountabilityquestion-6-как-lorenzo-accountable)
  - [[[07-q7-success-metrics|Question 7: Каковы success metrics?]]](#07-q7-success-metricsquestion-7-каковы-success-metrics)
  - [[[08-q8-other-ai-relationships|Question 8: Lorenzo's relationship с другими AI agents]]](#08-q8-other-ai-relationshipsquestion-8-lorenzos-relationship-с-другими-ai-agents)
  - [[[09-q9-geographic-linguistic-scope|Question 9: Geographic / linguistic scope]]](#09-q9-geographic-linguistic-scopequestion-9-geographic-linguistic-scope)
  - [[[10-q10-funding-model|Question 10: Funding model (Options A–F + Phase strategy)]]](#10-q10-funding-modelquestion-10-funding-model-options-af-phase-strategy)
  - [[[11-difficulties-and-recommendations|Сложности и рекомендации перед detailed specification]]](#11-difficulties-and-recommendationsсложности-и-рекомендации-перед-detailed-specification)
  - [[[README|specification]]](#readmespecification)
- [📁 Nautilus (`docs/nautilus/`)](#nautilus-docsnautilus)
  - [[[README|nautilus/ — Nautilus Portal Protocol и связанные working papers]]](#readmenautilus-nautilus-portal-protocol-и-связанные-working-papers)
  - [[[README|community-discussions/ — обсуждения и реакции вокруг DHLab серии]]](#readmecommunity-discussions-обсуждения-и-реакции-вокруг-dhlab-серии)
  - [[[00-question-agent-changes-reality|Du hast gesagt: Такой агент конечно меняет уже собственную реальность человека и…]]](#00-question-agent-changes-realitydu-hast-gesagt-такой-агент-конечно-меняет-уже-собственную-реальность-человека-и)
  - [[[01-response-en|Claude hat geantwortet: Хорошо.]]](#01-response-enclaude-hat-geantwortet-хорошо)
  - [[[README|agent-changes-reality]]](#readmeagent-changes-reality)
  - [[[00-question-habr-link|Du hast gesagt: https://habr.]]](#00-question-habr-linkdu-hast-gesagt-httpshabr)
  - [[[01-claude-response|Claude hat geantwortet: Прочитал внимательно.]]](#01-claude-responseclaude-hat-geantwortet-прочитал-внимательно)
  - [[[README|habr-article-1-reaction]]](#readmehabr-article-1-reaction)
  - [[[00-question-habr-2|Du hast gesagt: https://www.]]](#00-question-habr-2du-hast-gesagt-httpswww)
  - [[[01-response|Claude hat geantwortet: Прочитаю статью, чтобы понимать конкретный кейс, на кото…]]](#01-responseclaude-hat-geantwortet-прочитаю-статью-чтобы-понимать-конкретный-кейс-на-кото)
  - [[[README|habr-article-2-reaction]]](#readmehabr-article-2-reaction)
  - [[[00-question-practical|Du hast gesagt: Да это интересная ссылка спасибо всем участникам за творчество и…]]](#00-question-practicaldu-hast-gesagt-да-это-интересная-ссылка-спасибо-всем-участникам-за-творчество-и)
  - [[[01-response|Claude hat geantwortet: Отличное наблюдение.]]](#01-responseclaude-hat-geantwortet-отличное-наблюдение)
  - [[[README|practical-observations]]](#readmepractical-observations)
  - [[[00-question-voiceless|Du hast gesagt: Самый интересный вопрос — могут ли быть voiceless контрибьюторы]]](#00-question-voicelessdu-hast-gesagt-самый-интересный-вопрос-могут-ли-быть-voiceless-контрибьюторы)
  - [[[01-response|Claude hat geantwortet: Это сильное продолжение мысли, и оно заслуживает серьёзн…]]](#01-responseclaude-hat-geantwortet-это-сильное-продолжение-мысли-и-оно-заслуживает-серьёзн)
  - [[[README|voiceless-contributors]]](#readmevoiceless-contributors)
  - [[[01-why-binary-incomplete|1. Why the Binary View Is Incomplete]]](#01-why-binary-incomplete1-why-the-binary-view-is-incomplete)
  - [[[02-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]]](#02-twenty-one-teachers-pattern2-the-twenty-one-teachers-pattern)
  - [[[03-what-makes-csa|3. What Makes a Composite Skills Agent]]](#03-what-makes-csa3-what-makes-a-composite-skills-agent)
  - [[[04-sub-agent-registry|4. The Sub-Agent Registry]]](#04-sub-agent-registry4-the-sub-agent-registry)
  - [[[05-configuration-ensembles|5. Configuration: How Principals Build Their Ensembles]]](#05-configuration-ensembles5-configuration-how-principals-build-their-ensembles)
  - [[[06-coordination-disagreement|6. Coordination and Disagreement Resolution]]](#06-coordination-disagreement6-coordination-and-disagreement-resolution)
  - [[[07-economics-combinatorial|7. Economics of Combinatorial Replication]]](#07-economics-combinatorial7-economics-of-combinatorial-replication)
  - [[[08-seven-domains|8. Seven Domains of Application]]](#08-seven-domains8-seven-domains-of-application)
  - [[[09-okwf-integration|9. Integration with OKWF Infrastructure]]](#09-okwf-integration9-integration-with-okwf-infrastructure)
  - [[[10-risks|10. Risks Specific to Composite Architectures]]](#10-risks10-risks-specific-to-composite-architectures)
  - [[[11-open-questions|11. Open Questions]]](#11-open-questions11-open-questions)
  - [[[12-call-for-collaboration|12. Call for Collaboration]]](#12-call-for-collaboration12-call-for-collaboration)
  - [[[13-closing|13. Closing]]](#13-closing13-closing)
  - [[[README|composite-skills-agents]]](#readmecomposite-skills-agents)
  - [[[00-question-multiple-mentors|Du hast gesagt: Важный момент про способности про скилы как один человек професс…]]](#00-question-multiple-mentorsdu-hast-gesagt-важный-момент-про-способности-про-скилы-как-один-человек-професс)
  - [[[01-yogi-metaphor|Claude hat geantwortet: Это очень тонкое и важное наблюдение.]]](#01-yogi-metaphorclaude-hat-geantwortet-это-очень-тонкое-и-важное-наблюдение)
  - [[[02-what-was-missing-in-paper-6|Это не Тип 1 — потому что профиль не общий для всей профессии. И это не Тип 4 — …]]](#02-what-was-missing-in-paper-6это-не-тип-1-потому-что-профиль-не-общий-для-всей-профессии-и-это-не-тип-4)
  - [[[03-the-spectrum|Какой под-агент (или какие) должны её обработать]]](#03-the-spectrumкакой-под-агент-или-какие-должны-её-обработать)
  - [[[README|composite-skills-agents-companion-mentors]]](#readmecomposite-skills-agents-companion-mentors)
  - [[[00-abstract|Abstract — The Double-Triangle Architecture]]](#00-abstractabstract-the-double-triangle-architecture)
  - [[[01-why-single-triangle-incomplete|1. Why Single-Triangle Models Are Incomplete]]](#01-why-single-triangle-incomplete1-why-single-triangle-models-are-incomplete)
  - [[[02-double-triangle-architecture|2. The Double-Triangle Architecture]]](#02-double-triangle-architecture2-the-double-triangle-architecture)
  - [[[03-three-inter-layer-protocols|3. Three Inter-Layer Protocols]]](#03-three-inter-layer-protocols3-three-inter-layer-protocols)
  - [[[04-nautilus-portal-substrate|4. Nautilus Portal as Reference Substrate]]](#04-nautilus-portal-substrate4-nautilus-portal-as-reference-substrate)
  - [[[05-pattern-library-bridge|5. Pattern Library as Bridge Between Triangles]]](#05-pattern-library-bridge5-pattern-library-as-bridge-between-triangles)
  - [[[06-four-deployment-domains|6. Four Deployment Domains]]](#06-four-deployment-domains6-four-deployment-domains)
  - [[[07-open-questions|7. Open Questions]]](#07-open-questions7-open-questions)
  - [[[08-call-to-action|8. Call to Action]]](#08-call-to-action8-call-to-action)
  - [[[09-acknowledgments|Acknowledgments]]](#09-acknowledgmentsacknowledgments)
  - [[[10-references|References]]](#10-referencesreferences)
  - [[[11-glossary|Appendix A: Glossary]]](#11-glossaryappendix-a-glossary)
  - [[[README|double-triangle-architecture]]](#readmedouble-triangle-architecture)
  - [[[00-intro|The Missing Middle Layer Between Chat and Code]]](#00-introthe-missing-middle-layer-between-chat-and-code)
  - [[[01-missing-middle-layer|Why This Document Exists]]](#01-missing-middle-layerwhy-this-document-exists)
  - [[[02-why-document-exists|Why This Document Exists]]](#02-why-document-existswhy-this-document-exists)
  - [[[03-two-layer-stack|The Two-Layer Stack As It Exists]]](#03-two-layer-stackthe-two-layer-stack-as-it-exists)
  - [[[04-whats-missing-layer-b|What's Missing — Layer B]]](#04-whats-missing-layer-bwhats-missing-layer-b)
  - [[[05-why-not-built|Why This Hasn't Been Built]]](#05-why-not-builtwhy-this-hasnt-been-built)
  - [[[06-existing-approximations|Existing Approximations]]](#06-existing-approximationsexisting-approximations)
  - [[[07-specific-case|The Specific Case in Front of Us]]](#07-specific-casethe-specific-case-in-front-of-us)
  - [[[08-recursive-insight|The Recursive Insight]]](#08-recursive-insightthe-recursive-insight)
  - [[[09-what-industry-will-build|What Industry Will Likely Build]]](#09-what-industry-will-buildwhat-industry-will-likely-build)
  - [[[10-what-not-solved|What This Document Doesn't Solve]]](#10-what-not-solvedwhat-this-document-doesnt-solve)
  - [[[11-practical-recommendations|Practical Recommendations for the Current Project]]](#11-practical-recommendationspractical-recommendations-for-the-current-project)
  - [[[12-closing|Closing]]](#12-closingclosing)
  - [[[13-acknowledgments-refs|Acknowledgments]]](#13-acknowledgments-refsacknowledgments)
  - [[[README|infrastructure-layer-b-en]]](#readmeinfrastructure-layer-b-en)
  - [[[00-intro|00 Intro]]](#00-intro00-intro)
  - [[[01-zachem-dokument|Почему этот документ существует]]](#01-zachem-dokumentпочему-этот-документ-существует)
  - [[[02-dvukhsloynyy-stek|Двухслойный стек, как он существует]]](#02-dvukhsloynyy-stekдвухслойный-стек-как-он-существует)
  - [[[03-otsutstvuet-sloy-b|Что отсутствует — Слой B]]](#03-otsutstvuet-sloy-bчто-отсутствует-слой-b)
  - [[[04-pochemu-ne-postroeno|Почему это не было построено]]](#04-pochemu-ne-postroenoпочему-это-не-было-построено)
  - [[[05-priblizheniya|Существующие приближения]]](#05-priblizheniyaсуществующие-приближения)
  - [[[06-konkretnyy-sluchay|Конкретный случай перед нами]]](#06-konkretnyy-sluchayконкретный-случай-перед-нами)
  - [[[07-rekursivnoe-prozrenie|Рекурсивное прозрение]]](#07-rekursivnoe-prozrenieрекурсивное-прозрение)
  - [[[08-promyshlennost-postroit|Что промышленность вероятно построит]]](#08-promyshlennost-postroitчто-промышленность-вероятно-построит)
  - [[[09-ne-reshaet|Что этот документ не решает]]](#09-ne-reshaetчто-этот-документ-не-решает)
  - [[[10-rekomendatsii|Практические рекомендации для текущего проекта]]](#10-rekomendatsiiпрактические-рекомендации-для-текущего-проекта)
  - [[[11-zaklyuchenie|Заключение]]](#11-zaklyuchenieзаключение)
  - [[[12-blagodarnosti-ssylki|Благодарности]]](#12-blagodarnosti-ssylkiблагодарности)
  - [[[README|infrastructure-layer-b-ru]]](#readmeinfrastructure-layer-b-ru)
  - [[[01-cowork-discovery|1. The Cowork Discovery and Why It Changes Everything]]](#01-cowork-discovery1-the-cowork-discovery-and-why-it-changes-everything)
  - [[[02-cowork-provides|2. What Cowork Provides That InGit Doesn't Need to Build]]](#02-cowork-provides2-what-cowork-provides-that-ingit-doesnt-need-to-build)
  - [[[03-ingit-provides|3. What InGit Provides That Cowork Lacks]]](#03-ingit-provides3-what-ingit-provides-that-cowork-lacks)
  - [[[04-symbiotic-architecture|4. The Symbiotic Architecture]]](#04-symbiotic-architecture4-the-symbiotic-architecture)
  - [[[05-four-integration-paths|5. Four Integration Paths in Order of Accessibility]]](#05-four-integration-paths5-four-integration-paths-in-order-of-accessibility)
  - [[[06-refined-ingit-scope|6. Refined InGit Scope with Cowork in Mind]]](#06-refined-ingit-scope6-refined-ingit-scope-with-cowork-in-mind)
  - [[[07-practical-first-steps|7. Practical First Steps This Month]]](#07-practical-first-steps7-practical-first-steps-this-month)
  - [[[08-implications-nautilus-okwf|8. Implications for Nautilus and OKWF]]](#08-implications-nautilus-okwf8-implications-for-nautilus-and-okwf)
  - [[[09-risks-open-questions|9. Risks and Open Questions]]](#09-risks-open-questions9-risks-and-open-questions)
  - [[[10-strategic-positioning|10. Strategic Positioning]]](#10-strategic-positioning10-strategic-positioning)
  - [[[README|ingit-cowork-en]]](#readmeingit-cowork-en)
  - [[[01-otkrytie-cowork|1. Открытие Cowork и почему это меняет всё]]](#01-otkrytie-cowork1-открытие-cowork-и-почему-это-меняет-всё)
  - [[[02-chto-cowork-obespechivaet|2. Что Cowork обеспечивает, что InGit не нужно строить]]](#02-chto-cowork-obespechivaet2-что-cowork-обеспечивает-что-ingit-не-нужно-строить)
  - [[[03-chto-ingit-obespechivaet|3. Что InGit обеспечивает, чего Cowork не хватает]]](#03-chto-ingit-obespechivaet3-что-ingit-обеспечивает-чего-cowork-не-хватает)
  - [[[04-simbioticheskaya-arkhitektura|4. Симбиотическая Архитектура]]](#04-simbioticheskaya-arkhitektura4-симбиотическая-архитектура)
  - [[[05-chetyre-puti-integratsii|5. Четыре пути интеграции в порядке доступности]]](#05-chetyre-puti-integratsii5-четыре-пути-интеграции-в-порядке-доступности)
  - [[[06-utochnyonnyy-obyom-ingit|6. Уточнённый объём InGit с учётом Cowork]]](#06-utochnyonnyy-obyom-ingit6-уточнённый-объём-ingit-с-учётом-cowork)
  - [[[07-prakticheskie-shagi|7. Практические первые шаги в этом месяце]]](#07-prakticheskie-shagi7-практические-первые-шаги-в-этом-месяце)
  - [[[08-implikatsii-nautilus-okwf|8. Импликации для Nautilus и OKWF]]](#08-implikatsii-nautilus-okwf8-импликации-для-nautilus-и-okwf)
  - [[[09-riski-voprosy|9. Риски и Открытые Вопросы]]](#09-riski-voprosy9-риски-и-открытые-вопросы)
  - [[[10-strategicheskoe-pozitsionirovanie|10. Стратегическое Позиционирование]]](#10-strategicheskoe-pozitsionirovanie10-стратегическое-позиционирование)
  - [[[README|ingit-cowork-ru]]](#readmeingit-cowork-ru)
  - [[[00-question-innovations-transitions|Du hast gesagt: Интересно как новая как инновация как как рационализация как пер…]]](#00-question-innovations-transitionsdu-hast-gesagt-интересно-как-новая-как-инновация-как-как-рационализация-как-пер)
  - [[[01-response|Claude hat geantwortet: Отличный запрос.]]](#01-responseclaude-hat-geantwortet-отличный-запрос)
  - [[[README|innovation-transitions]]](#readmeinnovation-transitions)
  - [[[00-question-multi-tier|Du hast gesagt: Ещё есть такие вопросы то есть если общие юридические Наутилус м…]]](#00-question-multi-tierdu-hast-gesagt-ещё-есть-такие-вопросы-то-есть-если-общие-юридические-наутилус-м)
  - [[[01-strategic-significance|Claude hat geantwortet: Это стратегически значимый вопрос, и ответ на него — да,…]]](#01-strategic-significanceclaude-hat-geantwortet-это-стратегически-значимый-вопрос-и-ответ-на-него-да)
  - [[[README|multi-tier-architecture]]](#readmemulti-tier-architecture)
  - [[[00-question-can-it-apply-to-docs|Du hast gesagt: Вопрос такой вопрос и такие а можно ли этот протокол это система…]]](#00-question-can-it-apply-to-docsdu-hast-gesagt-вопрос-такой-вопрос-и-такие-а-можно-ли-этот-протокол-это-система)
  - [[[01-structural-comparison-code-vs-docs|Структурное сравнение: код vs гуманитарные документы]]](#01-structural-comparison-code-vs-docsструктурное-сравнение-код-vs-гуманитарные-документы)
  - [[[02-mcp-claude-desktop-use-cases|Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы …]]](#02-mcp-claude-desktop-use-casesчто-он-даёт-вам-на-практике-через-mcp-claude-desktop-может-ответить-на-запросы)
  - [[[03-what-doesnt-exist-on-market|Что не существует на рынке:]]](#03-what-doesnt-exist-on-marketчто-не-существует-на-рынке)
  - [[[04-grant-opportunities|Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access t…]]](#04-grant-opportunitieshorizon-europe-cluster-3-civil-security-for-society-пересекается-с-access-t)
  - [[[05-which-combination-more-valuable|Что из этого сейчас кажется более ценным? Или какая-то своя комбинация?]]](#05-which-combination-more-valuableчто-из-этого-сейчас-кажется-более-ценным-или-какая-то-своя-комбинация)
  - [[[README|npp-humanitarian-extension]]](#readmenpp-humanitarian-extension)
  - [[[00-abstract-status|Abstract + Status of This Document]]](#00-abstract-statusabstract-status-of-this-document)
  - [[[01-introduction|1. Introduction (Motivation, Design Goals, Non-Goals, Terminology)]]](#01-introduction1-introduction-motivation-design-goals-non-goals-terminology)
  - [[[02-terminology|2. Terminology]]](#02-terminology2-terminology)
  - [[[03-registry|3. Registry (nautilus.json)]]](#03-registry3-registry-nautilusjson)
  - [[[04-passport|4. Passport (passport.md)]]](#04-passport4-passport-passportmd)
  - [[[05-compatibility-levels|5. Compatibility Levels]]](#05-compatibility-levels5-compatibility-levels)
  - [[[06-adapter-interface|6. Adapter Interface]]](#06-adapter-interface6-adapter-interface)
  - [[[07-portal-entry|7. PortalEntry Structure]]](#07-portal-entry7-portalentry-structure)
  - [[[08-consensus-algorithm|8. Consensus Algorithm (v1.0: string normalization)]]](#08-consensus-algorithm8-consensus-algorithm-v10-string-normalization)
  - [[[09-query-flow|9. Query Flow]]](#09-query-flow9-query-flow)
  - [[[10-query-result|10. QueryResult Structure]]](#10-query-result10-queryresult-structure)
  - [[[11-security-considerations|11. Security Considerations]]](#11-security-considerations11-security-considerations)
  - [[[12-versioning-policy|12. Versioning Policy]]](#12-versioning-policy12-versioning-policy)
  - [[[13-reference-implementation|13. Reference Implementation]]](#13-reference-implementation13-reference-implementation)
  - [[[14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]](#14-adr-001-federation-over-merging14-adr-001-federation-over-merging)
  - [[[15-glossary|15. Glossary of Examples]]](#15-glossary15-glossary-of-examples)
  - [[[16-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]](#16-appendix-a-minimal-working-exampleappendix-a-minimal-working-example)
  - [[[17-appendix-b-change-log|Appendix B: Change Log]]](#17-appendix-b-change-logappendix-b-change-log)
  - [[[18-comment-on-document|Комментарий: дизайн-решения NPP v1.0]]](#18-comment-on-documentкомментарий-дизайн-решения-npp-v10)
  - [[[README|npp-v1-0]]](#readmenpp-v1-0)
  - [[[00-abstract-status|Abstract + Status of This Document]]](#00-abstract-statusabstract-status-of-this-document)
  - [[[01-introduction|1. Introduction (Motivation, Design Goals, Non-Goals, Terminology, Changes from v1.0)]]](#01-introduction1-introduction-motivation-design-goals-non-goals-terminology-changes-from-v10)
  - [[[02-terminology|2. Terminology]]](#02-terminology2-terminology)
  - [[[03-registry|3. Registry (nautilus.json)]]](#03-registry3-registry-nautilusjson)
  - [[[04-passport|4. Passport (passport.md)]]](#04-passport4-passport-passportmd)
  - [[[05-compatibility-levels|5. Compatibility Levels]]](#05-compatibility-levels5-compatibility-levels)
  - [[[06-adapter-interface|6. Adapter Interface]]](#06-adapter-interface6-adapter-interface)
  - [[[07-portal-entry|7. PortalEntry Structure]]](#07-portal-entry7-portalentry-structure)
  - [[[08-q6-space|8. Q6 Space (Normative)]]](#08-q6-space8-q6-space-normative)
  - [[[09-consensus-algorithm|9. Consensus Algorithm]]](#09-consensus-algorithm9-consensus-algorithm)
  - [[[10-query-flow|10. Query Flow]]](#10-query-flow10-query-flow)
  - [[[11-relevance-ranking|11. Relevance Ranking]]](#11-relevance-ranking11-relevance-ranking)
  - [[[12-onboarding-paths|12. Onboarding Paths (Normative)]]](#12-onboarding-paths12-onboarding-paths-normative)
  - [[[13-rest-api|13. REST API Contract (Normative for Portals)]]](#13-rest-api13-rest-api-contract-normative-for-portals)
  - [[[14-sdk|14. SDK Contract (Informative)]]](#14-sdk14-sdk-contract-informative)
  - [[[15-security|15. Security Considerations]]](#15-security15-security-considerations)
  - [[[16-mcp-extension|16. MCP Extension (Informative)]]](#16-mcp-extension16-mcp-extension-informative)
  - [[[17-versioning-policy|17. Versioning Policy]]](#17-versioning-policy17-versioning-policy)
  - [[[18-reference-implementation|18. Reference Implementation]]](#18-reference-implementation18-reference-implementation)
  - [[[19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]](#19-adr-001-federation-over-merging19-adr-001-federation-over-merging)
  - [[[20-adr-002-q6-first-class|20. ADR-002: Q6 as First-Class Protocol Concept]]](#20-adr-002-q6-first-class20-adr-002-q6-as-first-class-protocol-concept)
  - [[[21-adr-003-five-onboarding-paths|21. ADR-003: Five Onboarding Paths as Equal-Rank]]](#21-adr-003-five-onboarding-paths21-adr-003-five-onboarding-paths-as-equal-rank)
  - [[[22-glossary|22. Glossary of Reference Examples]]](#22-glossary22-glossary-of-reference-examples)
  - [[[README|npp-v1-1]]](#readmenpp-v1-1)
  - [[[00-abstract|AI-Coordinated Infrastructure for Distributed Expert Contribution]]](#00-abstractai-coordinated-infrastructure-for-distributed-expert-contribution)
  - [[[01-problem-statement|1. Problem Statement]]](#01-problem-statement1-problem-statement)
  - [[[02-target-populations|2. Target Populations]]](#02-target-populations2-target-populations)
  - [[[03-why-existing-fail|3. Why Existing Solutions Fail]]](#03-why-existing-fail3-why-existing-solutions-fail)
  - [[[04-proposed-infrastructure|4. Proposed Infrastructure]]](#04-proposed-infrastructure4-proposed-infrastructure)
  - [[[05-economic-model|5. Economic Model]]](#05-economic-model5-economic-model)
  - [[[06-governance-ethics|6. Governance and Ethics]]](#06-governance-ethics6-governance-and-ethics)
  - [[[07-phased-rollout|7. Phased Rollout Plan]]](#07-phased-rollout7-phased-rollout-plan)
  - [[[08-risk-analysis|8. Risk Analysis]]](#08-risk-analysis8-risk-analysis)
  - [[[09-call-for-partnership|9. Call for Partnership]]](#09-call-for-partnership9-call-for-partnership)
  - [[[10-appendices|10. Appendices]]](#10-appendices10-appendices)
  - [[[README|okwf-concept]]](#readmeokwf-concept)
  - [[[00-question-anonymization|Du hast gesagt: Насчёт приватности Я думаю что возможно удалять только личные да…]]](#00-question-anonymizationdu-hast-gesagt-насчёт-приватности-я-думаю-что-возможно-удалять-только-личные-да)
  - [[[01-what-to-anonymize-german-standard|Что именно анонимизировать: немецкий стандарт]]](#01-what-to-anonymize-german-standardчто-именно-анонимизировать-немецкий-стандарт)
  - [[[02-two-tier-publication|Архитектурное решение: две-уровневая публикация]]](#02-two-tier-publicationархитектурное-решение-две-уровневая-публикация)
  - [[[03-what-this-gives-technically|Что это даёт технически]]](#03-what-this-gives-technicallyчто-это-даёт-технически)
  - [[[04-what-i-can-do-now|Что я могу сделать сейчас]]](#04-what-i-can-do-nowчто-я-могу-сделать-сейчас)
  - [[[README|privacy-federation]]](#readmeprivacy-federation)
  - [[[00-abstract|Professional Colleague Agents]]](#00-abstractprofessional-colleague-agents)
  - [[[01-five-type-typology|1. The Five-Type Typology of Principal-Side Agents]]](#01-five-type-typology1-the-five-type-typology-of-principal-side-agents)
  - [[[02-what-makes-pca|2. What Makes a Professional Colleague Agent]]](#02-what-makes-pca2-what-makes-a-professional-colleague-agent)
  - [[[03-empirical-case-obuchay|3. Empirical Case Study: «Обучай»]]](#03-empirical-case-obuchay3-empirical-case-study-обучай)
  - [[[04-architecture|4. Architecture of Professional Colleague Agents]]](#04-architecture4-architecture-of-professional-colleague-agents)
  - [[[05-economics-replication|5. The Economics of Profession-Wide Replication]]](#05-economics-replication5-the-economics-of-profession-wide-replication)
  - [[[06-risks|6. Risks Specific to this Category]]](#06-risks6-risks-specific-to-this-category)
  - [[[07-application-domains|7. Application Domains]]](#07-application-domains7-application-domains)
  - [[[08-pilot-sgb-advocate|8. Pilot Proposal: SGB Advocate Colleague]]](#08-pilot-sgb-advocate8-pilot-proposal-sgb-advocate-colleague)
  - [[[09-relationship-other-agents|9. Relationship to Other Agent Types]]](#09-relationship-other-agents9-relationship-to-other-agent-types)
  - [[[10-open-questions|10. Open Questions]]](#10-open-questions10-open-questions)
  - [[[11-call-for-collaboration|11. Call for Collaboration]]](#11-call-for-collaboration11-call-for-collaboration)
  - [[[12-closing|12. Closing]]](#12-closing12-closing)
  - [[[README|professional-colleague-agents-en]]](#readmeprofessional-colleague-agents-en)
  - [[[00-abstract|Содержание]]](#00-abstractсодержание)
  - [[[01-pyat-tipov|1. Типология из пяти типов агентов на стороне принципала]]](#01-pyat-tipov1-типология-из-пяти-типов-агентов-на-стороне-принципала)
  - [[[02-chto-delaet-pka|2. Что делает агента Профессиональным Коллегой]]](#02-chto-delaet-pka2-что-делает-агента-профессиональным-коллегой)
  - [[[03-keys-obuchay|3. Эмпирический кейс: «Обучай»]]](#03-keys-obuchay3-эмпирический-кейс-обучай)
  - [[[04-arkhitektura|4. Архитектура Профессиональных Коллег-Агентов]]](#04-arkhitektura4-архитектура-профессиональных-коллег-агентов)
  - [[[05-ekonomika|5. Экономика тиражирования по профессии]]](#05-ekonomika5-экономика-тиражирования-по-профессии)
  - [[[06-riski|6. Риски, специфичные для этой категории]]](#06-riski6-риски-специфичные-для-этой-категории)
  - [[[07-oblasti-primeneniya|7. Области применения]]](#07-oblasti-primeneniya7-области-применения)
  - [[[08-pilot-sgb-kolega|8. Пилотное предложение: SGB Колega-Адвокат]]](#08-pilot-sgb-kolega8-пилотное-предложение-sgb-колega-адвокат)
  - [[[09-svyaz-s-drugimi|9. Связь с другими типами агентов]]](#09-svyaz-s-drugimi9-связь-с-другими-типами-агентов)
  - [[[10-otkrytye-voprosy|10. Открытые вопросы]]](#10-otkrytye-voprosy10-открытые-вопросы)
  - [[[11-prizyv-k-sotrudnichestvu|11. Призыв к сотрудничеству]]](#11-prizyv-k-sotrudnichestvu11-призыв-к-сотрудничеству)
  - [[[12-zaklyuchenie|12. Заключение]]](#12-zaklyuchenie12-заключение)
  - [[[README|professional-colleague-agents-ru]]](#readmeprofessional-colleague-agents-ru)
  - [[[00-abstract|AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]](#00-abstractai-mediated-representation-for-underrepresented-experts-and-vulnerable-populations)
  - [[[01-cinderella-syndrome|1. The Cinderella Syndrome: Why Quality Stays Invisible]]](#01-cinderella-syndrome1-the-cinderella-syndrome-why-quality-stays-invisible)
  - [[[02-historical-precedents|2. Historical Precedents: Agents as Civilizational Innovation]]](#02-historical-precedents2-historical-precedents-agents-as-civilizational-innovation)
  - [[[03-what-makes-representative-agent|3. What Makes a Representative Agent]]](#03-what-makes-representative-agent3-what-makes-a-representative-agent)
  - [[[04-ten-domains|4. Ten Domains of Application]]](#04-ten-domains4-ten-domains-of-application)
  - [[[05-architectural-specification|5. Architectural Specification]]](#05-architectural-specification5-architectural-specification)
  - [[[06-ethical-framework|6. Ethical Framework]]](#06-ethical-framework6-ethical-framework)
  - [[[07-governance-oversight|7. Governance and Oversight]]](#07-governance-oversight7-governance-and-oversight)
  - [[[08-risks-mitigations|8. Risks and Mitigations]]](#08-risks-mitigations8-risks-and-mitigations)
  - [[[09-phased-rollout|9. Phased Rollout Strategy]]](#09-phased-rollout9-phased-rollout-strategy)
  - [[[10-open-questions|10. Open Questions]]](#10-open-questions10-open-questions)
  - [[[11-call-for-collaboration|11. Call for Collaboration]]](#11-call-for-collaboration11-call-for-collaboration)
  - [[[12-closing|12. Closing]]](#12-closing12-closing)
  - [[[README|representative-agent-layer-en]]](#readmerepresentative-agent-layer-en)
  - [[[00-abstract|Содержание]]](#00-abstractсодержание)
  - [[[01-sindrom-zolushki|1. Синдром Золушки: Почему качество остаётся невидимым]]](#01-sindrom-zolushki1-синдром-золушки-почему-качество-остаётся-невидимым)
  - [[[02-istoricheskie-pretsedenty|2. Исторические прецеденты: Агенты как цивилизационная инновация]]](#02-istoricheskie-pretsedenty2-исторические-прецеденты-агенты-как-цивилизационная-инновация)
  - [[[03-chto-delaet-predstavitelskim|3. Что делает агента Представительским]]](#03-chto-delaet-predstavitelskim3-что-делает-агента-представительским)
  - [[[04-desyat-oblastey|4. Десять областей применения]]](#04-desyat-oblastey4-десять-областей-применения)
  - [[[05-arkhitekturnaya-spetsifikatsiya|5. Архитектурная спецификация]]](#05-arkhitekturnaya-spetsifikatsiya5-архитектурная-спецификация)
  - [[[06-eticheskaya-ramka|6. Этическая рамка]]](#06-eticheskaya-ramka6-этическая-рамка)
  - [[[07-upravlenie-nadzor|7. Управление и надзор]]](#07-upravlenie-nadzor7-управление-и-надзор)
  - [[[08-riski-mery|8. Риски и меры противодействия]]](#08-riski-mery8-риски-и-меры-противодействия)
  - [[[09-strategiya-razvyortyvaniya|9. Стратегия поэтапного развёртывания]]](#09-strategiya-razvyortyvaniya9-стратегия-поэтапного-развёртывания)
  - [[[10-otkrytye-voprosy|10. Открытые вопросы]]](#10-otkrytye-voprosy10-открытые-вопросы)
  - [[[11-prizyv-k-sotrudnichestvu|11. Призыв к сотрудничеству]]](#11-prizyv-k-sotrudnichestvu11-призыв-к-сотрудничеству)
  - [[[12-zaklyuchenie|12. Заключение]]](#12-zaklyuchenie12-заключение)
  - [[[README|representative-agent-layer-ru]]](#readmerepresentative-agent-layer-ru)
  - [[[00-tldr|TL;DR — Трёхфазная методология Review]]](#00-tldrtldr-трёхфазная-методология-review)
  - [[[01-context-motivation|1. Контекст и мотивация]]](#01-context-motivation1-контекст-и-мотивация)
  - [[[02-formal-workflow|2. Формальный workflow]]](#02-formal-workflow2-формальный-workflow)
  - [[[03-consolidation-principles|3. Принципы консолидации (Фаза C)]]](#03-consolidation-principles3-принципы-консолидации-фаза-c)
  - [[[04-fallback-ratio-question|Вопрос: fallback‑ratio как критический или осмысленный?]]](#04-fallback-ratio-questionвопрос-fallbackratio-как-критический-или-осмысленный)
  - [[[05-conditions-of-applicability|4. Условия применимости]]](#05-conditions-of-applicability4-условия-применимости)
  - [[[06-relation-existing-methodologies|5. Связь с существующими методологиями]]](#06-relation-existing-methodologies5-связь-с-существующими-методологиями)
  - [[[07-why-valid-for-ai|6. Почему это валидный паттерн для AI‑assisted workflows]]](#07-why-valid-for-ai6-почему-это-валидный-паттерн-для-aiassisted-workflows)
  - [[[08-implementation-nautilus|7. Реализация в проекте Nautilus]]](#08-implementation-nautilus7-реализация-в-проекте-nautilus)
  - [[[09-limitations-open-questions|8. Ограничения и открытые вопросы]]](#09-limitations-open-questions8-ограничения-и-открытые-вопросы)
  - [[[10-checklist|9. Checklist применения методологии]]](#10-checklist9-checklist-применения-методологии)
  - [[[11-application-plan-current-docs|10. Конкретный план применения к текущим документам]]](#11-application-plan-current-docs10-конкретный-план-применения-к-текущим-документам)
  - [[[12-appendix-a-header-warning|Appendix A: Шаблон для header warning]]](#12-appendix-a-header-warningappendix-a-шаблон-для-header-warning)
  - [[[13-appendix-b-examples|Appendix B: Примеры расхождений и их разрешения]]](#13-appendix-b-examplesappendix-b-примеры-расхождений-и-их-разрешения)
  - [[[14-main-technical-risks|Главные технические риски]]](#14-main-technical-risksглавные-технические-риски)
  - [[[15-appendix-c-history|Appendix C: История изменений методологии]]](#15-appendix-c-historyappendix-c-история-изменений-методологии)
  - [[[16-glossary|Глоссарий]]](#16-glossaryглоссарий)
  - [[[README|review-methodology]]](#readmereview-methodology)
  - [[[00-question-supply-demand|Du hast gesagt: Спрос рождает предложение - это простая экономическая истина нач…]]](#00-question-supply-demanddu-hast-gesagt-спрос-рождает-предложение---это-простая-экономическая-истина-нач)
  - [[[01-three-related-themes|Claude hat geantwortet: Очень богатый вопрос — три разных, но связанных темы.]]](#01-three-related-themesclaude-hat-geantwortet-очень-богатый-вопрос-три-разных-но-связанных-темы)
  - [[[README|supply-demand]]](#readmesupply-demand)
  - [[[00-question-mountain-to-person|Du hast gesagt: Того если гора не идёт человеку может быть этот человек пойдёт к…]]](#00-question-mountain-to-persondu-hast-gesagt-того-если-гора-не-идёт-человеку-может-быть-этот-человек-пойдёт-к)
  - [[[01-completing-loop|Claude hat geantwortet: Это исключительно богатый вопрос, и я хочу ответить на н…]]](#01-completing-loopclaude-hat-geantwortet-это-исключительно-богатый-вопрос-и-я-хочу-ответить-на-н)
  - [[[README|transmission-box]]](#readmetransmission-box)
- [📁 Svyazi 2 0 (`docs/svyazi-2-0/`)](#svyazi-2-0-docssvyazi-2-0)
  - [[[README|Svyazi 2.0 — тематический индекс]]](#readmesvyazi-20-тематический-индекс)
  - [[[README|architecture]]](#readmearchitecture)
  - [[[card-envelope|Card Envelope]]](#card-envelopecard-envelope)
  - [[[evidence-envelope|Evidence Envelope]]](#evidence-envelopeevidence-envelope)
  - [[[gaps|Архитектурные зазоры]]](#gapsархитектурные-зазоры)
  - [[[integration-spec|Интеграционная спецификация (минимум для MVP)]]](#integration-specинтеграционная-спецификация-минимум-для-mvp)
  - [[[memory-write-policy|Memory Write Policy]]](#memory-write-policymemory-write-policy)
  - [[[review-record|Review Record]]](#review-recordreview-record)
  - [[[skill-tool-policy|Skill and Tool Policy]]](#skill-tool-policyskill-and-tool-policy)
  - [[[README|components]]](#readmecomponents)
  - [[[agent-memory-mcp|agent-memory-mcp + Memory OS]]](#agent-memory-mcpagent-memory-mcp-memory-os)
  - [[[agentfs]]](#agentfs)
  - [[[ai-factory|AI Factory + AIF Handoff]]](#ai-factoryai-factory-aif-handoff)
  - [[[autoresearch-sequential|AutoResearch + Sequential]]](#autoresearch-sequentialautoresearch-sequential)
  - [[[graph-rag|Graph RAG]]](#graph-raggraph-rag)
  - [[[hybrid-rag|Hybrid RAG knowledge base]]](#hybrid-raghybrid-rag-knowledge-base)
  - [[[knowledge-space]]](#knowledge-space)
  - [[[legal-rag|Legal RAG]]](#legal-raglegal-rag)
  - [[[mclaude]]](#mclaude)
  - [[[memnet|MemNet / memory-is-all-you-need]]](#memnetmemnet-memory-is-all-you-need)
  - [[[ngt-memory|NGT Memory]]](#ngt-memoryngt-memory)
  - [[[research-docs-liteparse|research-docs + LiteParse]]](#research-docs-liteparseresearch-docs-liteparse)
  - [[[rufler]]](#rufler)
  - [[[security-routing-plane|Security + routing plane]]](#security-routing-planesecurity-routing-plane)
  - [[[self-aware-mcp|Self‑Aware MCP + Skills + CodeWiki]]](#self-aware-mcpselfaware-mcp-skills-codewiki)
  - [[[svyazi]]](#svyazi)
  - [[[voice-stack|Voice / local-first stack]]](#voice-stackvoice-local-first-stack)
  - [[[yjs-automerge|Yjs + Automerge]]](#yjs-automergeyjs-automerge)
  - [[[yodoca]]](#yodoca)
  - [[[A-collaboration-os|Ансамбль A — Collaboration OS]]](#a-collaboration-osансамбль-a-collaboration-os)
  - [[[B-forensic-rag|Ансамбль B — Forensic RAG для доказуемого matching и review]]](#b-forensic-ragансамбль-b-forensic-rag-для-доказуемого-matching-и-review)
  - [[[C-multi-agent-factory|Ансамбль C — Spec‑driven multi‑agent factory]]](#c-multi-agent-factoryансамбль-c-specdriven-multiagent-factory)
  - [[[D-voice-first-mesh|Ансамбль D — Voice‑first local knowledge mesh]]](#d-voice-first-meshансамбль-d-voicefirst-local-knowledge-mesh)
  - [[[E-execution-plane|Ансамбль E — Safe and cheap execution plane]]](#e-execution-planeансамбль-e-safe-and-cheap-execution-plane)
  - [[[F-evidence-backed-intake|Ансамбль F — Evidence‑Backed Community Intake]]](#f-evidence-backed-intakeансамбль-f-evidencebacked-community-intake)
  - [[[G-federated-local-graph|Ансамбль G — Federated Local‑First Community Graph]]](#g-federated-local-graphансамбль-g-federated-localfirst-community-graph)
  - [[[H-research-to-product-flywheel|Ансамбль H — Research‑to‑Product Flywheel]]](#h-research-to-product-flywheelансамбль-h-researchtoproduct-flywheel)
  - [[[README|Ансамбли проектов]]](#readmeансамбли-проектов)
  - [[[README|limitations]]](#readmelimitations)
  - [[[conclusions|Итоговые выводы и порядок сборки]]](#conclusionsитоговые-выводы-и-порядок-сборки)
  - [[[do-not-glue|Что пока лучше не склеивать]]](#do-not-glueчто-пока-лучше-не-склеивать)
  - [[[license-tree|Лицензионные развилки]]](#license-treeлицензионные-развилки)
  - [[[README|outreach]]](#readmeoutreach)
  - [[[first-contacts|Первые контакты]]](#first-contactsпервые-контакты)
  - [[[message-template|Шаблон первого сообщения]]](#message-templateшаблон-первого-сообщения)
  - [[[narrow-questions|Узкие вопросы для каждого автора]]](#narrow-questionsузкие-вопросы-для-каждого-автора)
  - [[[README|overview]]](#readmeoverview)
  - [[[continuation-intro|Что добавляет продолжение исследования]]](#continuation-introчто-добавляет-продолжение-исследования)
  - [[[executive-summary|Executive summary]]](#executive-summaryexecutive-summary)
  - [[[methodology|Методика и рамка отбора]]](#methodologyметодика-и-рамка-отбора)
  - [[[projects-map|Карта найденных проектов и паттернов]]](#projects-mapкарта-найденных-проектов-и-паттернов)
  - [[[README|prototype]]](#readmeprototype)
  - [[[mvp-plan|План MVP-прототипа]]](#mvp-planплан-mvp-прототипа)
  - [[[risks|Ключевые риски и как их закрывать]]](#risksключевые-риски-и-как-их-закрывать)
  - [[[roadmap|Дорожная карта прототипа]]](#roadmapдорожная-карта-прототипа)
  - [[[README|security]]](#readmesecurity)
  - [[[budget-routing|Практичный бюджетный роутинг моделей]]](#budget-routingпрактичный-бюджетный-роутинг-моделей)
  - [[[default-policy|Что стоит зафиксировать как default policy]]](#default-policyчто-стоит-зафиксировать-как-default-policy)
  - [[[privacy|Приватность: local-first by default]]](#privacyприватность-local-first-by-default)
- [📁 Technology Combinations (`docs/technology-combinations/`)](#technology-combinations-docstechnology-combinations)
  - [[[README|technology-combinations/ — комбинирование технологий для новых свойств]]](#readmetechnology-combinations-комбинирование-технологий-для-новых-свойств)
  - [[[01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern|Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн]]](#01-pravilnaya-agentskaya-arkhitektura-svyazi-patternкомбинация-1-правильная-агентская-архитектура-svyazi-паттерн)
  - [[[02-multiagentnyy-khaos-reshenie-auto-ai-router|Комбинация 2: Мультиагентный хаос-решение × Auto AI Router]]](#02-multiagentnyy-khaos-reshenie-auto-ai-routerкомбинация-2-мультиагентный-хаос-решение-auto-ai-router)
  - [[[03-crdt-local-first-svyazi-cardindex|Комбинация 3: CRDT local-first × Svyazi CardIndex]]](#03-crdt-local-first-svyazi-cardindexкомбинация-3-crdt-local-first-svyazi-cardindex)
  - [[[04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura|Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура]]](#04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitekturaкомбинация-4-парсинг-с-llm-graph-rag-правильная-агентская-архитектура)
  - [[[05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy|Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной]]](#05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoyкомбинация-5-sourcecraft-cli-claude-code-sequential-протокол-дочкиной)
  - [[[06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-|Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер]]](#06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-комбинация-6-openclaude-утёкший-claude-code-zinc-inference-engine-mome-роутер)
  - [[[07-crawl4ai-docling-yodoca-consolidator|Комбинация 7: Crawl4AI × Docling × Yodoca consolidator]]](#07-crawl4ai-docling-yodoca-consolidatorкомбинация-7-crawl4ai-docling-yodoca-consolidator)
  - [[[08-conductor-adversarial-review-auto-ai-router|Комбинация 8: Conductor × adversarial-review × Auto AI Router]]](#08-conductor-adversarial-review-auto-ai-routerкомбинация-8-conductor-adversarial-review-auto-ai-router)
  - [[[09-agent-orchestration-stack|Комбинация 9: Agent Orchestration Stack]]](#09-agent-orchestration-stackкомбинация-9-agent-orchestration-stack)
  - [[[10-legal-document-intelligence-pipeline|Комбинация 10: Legal Document Intelligence Pipeline]]](#10-legal-document-intelligence-pipelineкомбинация-10-legal-document-intelligence-pipeline)
  - [[[11-hybrid-crdt-sql-database|Комбинация 11: Hybrid CRDT-SQL Database]]](#11-hybrid-crdt-sql-databaseкомбинация-11-hybrid-crdt-sql-database)
  - [[[12-multi-agent-observability-stack|Комбинация 12: Multi-Agent Observability Stack]]](#12-multi-agent-observability-stackкомбинация-12-multi-agent-observability-stack)
  - [[[13-legal-document-transpiler|Комбинация 13: Legal Document Transpiler]]](#13-legal-document-transpilerкомбинация-13-legal-document-transpiler)
  - [[[14-local-first-agent-development-environment|Комбинация 14: local-first Agent Development Environment]]](#14-local-first-agent-development-environmentкомбинация-14-local-first-agent-development-environment)
  - [[[15-self-consolidating-legal-corpus|Комбинация 15: Self-Consolidating Legal Corpus]]](#15-self-consolidating-legal-corpusкомбинация-15-self-consolidating-legal-corpus)
  - [[[16-adversarial-multi-agent-code-review|Комбинация 16: Adversarial Multi-Agent Code Review]]](#16-adversarial-multi-agent-code-reviewкомбинация-16-adversarial-multi-agent-code-review)
  - [[[17-distributed-agent-memory-with-graph|Комбинация 17: Distributed Agent Memory with Graph]]](#17-distributed-agent-memory-with-graphкомбинация-17-distributed-agent-memory-with-graph)
  - [[[18-llm-powered-legal-corpus-builder|Комбинация 18: LLM-Powered Legal Corpus Builder]]](#18-llm-powered-legal-corpus-builderкомбинация-18-llm-powered-legal-corpus-builder)
  - [[[19-multi-agent-observability-platform|Комбинация 19: Multi-Agent Observability Platform]]](#19-multi-agent-observability-platformкомбинация-19-multi-agent-observability-platform)
  - [[[20-hybrid-olap-oltp-with-real-time-sync|Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync]]](#20-hybrid-olap-oltp-with-real-time-syncкомбинация-20-hybrid-olap-oltp-with-real-time-sync)
  - [[[21-legal-corpus-analytics-at-scale|Комбинация 21: Legal Corpus Analytics at Scale]]](#21-legal-corpus-analytics-at-scaleкомбинация-21-legal-corpus-analytics-at-scale)
  - [[[22-russian-international-oss-stack|Комбинация 22: Russian-International OSS Stack]]](#22-russian-international-oss-stackкомбинация-22-russian-international-oss-stack)
  - [[[23-security-first-code-review-pipeline|Комбинация 23: Security-First Code Review Pipeline]]](#23-security-first-code-review-pipelineкомбинация-23-security-first-code-review-pipeline)
  - [[[24-mega-integration-full-stack|Комбинация 24: MEGA-INTEGRATION: Full Stack]]](#24-mega-integration-full-stackкомбинация-24-mega-integration-full-stack)
  - [[[25-legal-dsl-code-transpiler|Комбинация 25: Legal DSL → Code Transpiler]]](#25-legal-dsl-code-transpilerкомбинация-25-legal-dsl-code-transpiler)
  - [[[26-ast-based-code-analysis-for-legal-automation|Комбинация 26: AST-Based Code Analysis for Legal Automation]]](#26-ast-based-code-analysis-for-legal-automationкомбинация-26-ast-based-code-analysis-for-legal-automation)
  - [[[27-hybrid-rag-with-ast-chunked-code|Комбинация 27: Hybrid RAG with AST-Chunked Code]]](#27-hybrid-rag-with-ast-chunked-codeкомбинация-27-hybrid-rag-with-ast-chunked-code)
  - [[[28-pydantic-enforced-legal-workflows|Комбинация 28: Pydantic-Enforced Legal Workflows]]](#28-pydantic-enforced-legal-workflowsкомбинация-28-pydantic-enforced-legal-workflows)
  - [[[29-meta-programmatic-legal-template-generator|Комбинация 29: Meta-Programmatic Legal Template Generator]]](#29-meta-programmatic-legal-template-generatorкомбинация-29-meta-programmatic-legal-template-generator)
  - [[[30-mega-stack-3-0-with-dsl-ast|Комбинация 30: MEGA-STACK 3.0 with DSL & AST]]](#30-mega-stack-3-0-with-dsl-astкомбинация-30-mega-stack-30-with-dsl-ast)
  - [[[31-event-sourced-legal-document-history|Комбинация 31: Event-Sourced Legal Document History]]](#31-event-sourced-legal-document-historyкомбинация-31-event-sourced-legal-document-history)
  - [[[32-consensus-based-multi-agent-coordination|Комбинация 32: Consensus-Based Multi-Agent Coordination]]](#32-consensus-based-multi-agent-coordinationкомбинация-32-consensus-based-multi-agent-coordination)
  - [[[33-event-sourcing-cqrs-clickhouse-analytics|Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics]]](#33-event-sourcing-cqrs-clickhouse-analyticsкомбинация-33-event-sourcing-cqrs-clickhouse-analytics)
  - [[[34-distributed-event-store-with-paxos|Комбинация 34: Distributed Event Store with Paxos]]](#34-distributed-event-store-with-paxosкомбинация-34-distributed-event-store-with-paxos)
  - [[[35-mega-stack-4-0-with-event-sourcing-consensus|Комбинация 35: MEGA-STACK 4.0 with Event Sourcing & Consensus]]](#35-mega-stack-4-0-with-event-sourcing-consensusкомбинация-35-mega-stack-40-with-event-sourcing-consensus)
  - [[[README|combinations]]](#readmecombinations)
  - [[[01-legal-ai-stack|Mega‑Stack 1.0 — Полный Legal‑AI Stack]]](#01-legal-ai-stackmegastack-10-полный-legalai-stack)
  - [[[02-ultimate-legal-ai|Mega‑Stack 2.0 — Ultimate Legal‑AI System]]](#02-ultimate-legal-aimegastack-20-ultimate-legalai-system)
  - [[[03-dsl-ast|Mega‑Stack 3.0 — with DSL & AST]]](#03-dsl-astmegastack-30-with-dsl-ast)
  - [[[04-event-sourcing-consensus|Mega‑Stack 4.0 — with Event Sourcing & Consensus]]](#04-event-sourcing-consensusmegastack-40-with-event-sourcing-consensus)
  - [[[README|mega-stacks]]](#readmemega-stacks)
  - [[[README|properties/ — эмерджентные свойства]]](#readmeproperties-эмерджентные-свойства)
  - [[[README|research-reports]]](#readmeresearch-reports)
  - [[[continuation-10-domains|Research Report: Continuation — 10 New Domains Beyond the Original 45 Combinations]]](#continuation-10-domainsresearch-report-continuation-10-new-domains-beyond-the-original-45-combinations)
  - [[[sozialrecht-35-combinations|Research Report: Sozialrecht (35 комбинаций)]]](#sozialrecht-35-combinationsresearch-report-sozialrecht-35-комбинаций)
  - [[[01-08-summary|Сводная таблица 1–8]]](#01-08-summaryсводная-таблица-18)
  - [[[09-14-extended|Сводная таблица 9–14 (Extended)]]](#09-14-extendedсводная-таблица-914-extended)
  - [[[15-19-extended|Сводная таблица 15–19 (Extended)]]](#15-19-extendedсводная-таблица-1519-extended)
  - [[[20-24-final|Сводная таблица 20–24 (Final 1–24)]]](#20-24-finalсводная-таблица-2024-final-124)
  - [[[25-30-extended|Сводная таблица 25–30 (Complete 1–30)]]](#25-30-extendedсводная-таблица-2530-complete-130)
  - [[[31-35-final|Сводная таблица 31–35 (Complete 1–35)]]](#31-35-finalсводная-таблица-3135-complete-135)
  - [[[README|synthesis-tables]]](#readmesynthesis-tables)
- [📁 Templates (`docs/templates/`)](#templates-docstemplates)
  - [[[README|Шаблоны документов]]](#readmeшаблоны-документов)
  - [[Спецификация агента: [Название]](docs/templates/agent-spec.md)](#спецификация-агента-названиеdocstemplatesagent-specmd)
  - [[Контакт: [Имя / Проект]](docs/templates/contact-outreach.md)](#контакт-имя-проектdocstemplatescontact-outreachmd)
  - [[Противоречие: [Название]](docs/templates/contradiction-record.md)](#противоречие-названиеdocstemplatescontradiction-recordmd)
  - [[ADR: [Название решения]](docs/templates/decision-record.md)](#adr-название-решенияdocstemplatesdecision-recordmd)
  - [[Ансамбль: [Название]](docs/templates/ensemble.md)](#ансамбль-названиеdocstemplatesensemblemd)
  - [[Эксперимент: [Название]](docs/templates/experiment-log.md)](#эксперимент-названиеdocstemplatesexperiment-logmd)
  - [[FAQ: [Вопрос]](docs/templates/faq-entry.md)](#faq-вопросdocstemplatesfaq-entrymd)
  - [[[Термин]](docs/templates/glossary-entry.md)](#терминdocstemplatesglossary-entrymd)
  - [[KPI Snapshot: [дата]](docs/templates/kpi-snapshot.md)](#kpi-snapshot-датаdocstemplateskpi-snapshotmd)
  - [[Юридический кейс: [Aktenzeichen]](docs/templates/legal-case.md)](#юридический-кейс-aktenzeichendocstemplateslegal-casemd)
  - [[Встреча: [Тема]](docs/templates/meeting-notes.md)](#встреча-темаdocstemplatesmeeting-notesmd)
  - [[Mega-stack: [Название]](docs/templates/mega-stack.md)](#mega-stack-названиеdocstemplatesmega-stackmd)
  - [[[Название компонента]](docs/templates/project-component.md)](#название-компонентаdocstemplatesproject-componentmd)
  - [[[Название протокола]](docs/templates/protocol-spec.md)](#название-протоколаdocstemplatesprotocol-specmd)
  - [[MVP: [Название]](docs/templates/prototype-mvp.md)](#mvp-названиеdocstemplatesprototype-mvpmd)
  - [[[Тема исследования]](docs/templates/research-note.md)](#тема-исследованияdocstemplatesresearch-notemd)
  - [[Ретроспектива: [период]](docs/templates/retrospective.md)](#ретроспектива-периодdocstemplatesretrospectivemd)
  - [[RFC NNNN: [Название]](docs/templates/rfc.md)](#rfc-nnnn-названиеdocstemplatesrfcmd)
  - [[Риск: [Название]](docs/templates/risk-entry.md)](#риск-названиеdocstemplatesrisk-entrymd)
  - [[Tech Pair: [A] × [B]](docs/templates/tech-pair.md)](#tech-pair-a-bdocstemplatestech-pairmd)
  - [[Tech Radar: [Название]](docs/templates/tech-radar-entry.md)](#tech-radar-названиеdocstemplatestech-radar-entrymd)
  - [[[имя нового шаблона]](docs/templates/template-of-templates.md)](#имя-нового-шаблонаdocstemplatestemplate-of-templatesmd)
  - [[Еженедельный дайджест: [период]](docs/templates/weekly-digest.md)](#еженедельный-дайджест-периодdocstemplatesweekly-digestmd)
- [🗺️ Тематическая карта](#тематическая-карта)
  - [Архитектура (564 документов)](#архитектура-564-документов)
  - [Агенты (156 документов)](#агенты-156-документов)
  - [Проекты (142 документов)](#проекты-142-документов)
  - [Документация (83 документов)](#документация-83-документов)
  - [Контакты (56 документов)](#контакты-56-документов)
  - [Память (43 документов)](#память-43-документов)
  - [Код (36 документов)](#код-36-документов)
  - [Анализ (19 документов)](#анализ-19-документов)

---


_Обновлено: 2026-04-29_

Секций: **18** | Файлов: **1182**

## Содержание

- [Docs](#docs) — 92 файлов
- [Svyazi](#svyazi) — 16 файлов
- [Anthropic Vacancies](#anthropic-vacancies) — 357 файлов
- [Technology Combinations](#technology-combinations) — 7 файлов
- [Ai Collaborations](#ai-collaborations) — 17 файлов
- [Habr Projects](#habr-projects) — 10 файлов
- [Ai Collaborations](#ai-collaborations) — 30 файлов
- [Anthropic Vacancies](#anthropic-vacancies) — 111 файлов
- [Autofilled](#autofilled) — 13 файлов
- [Badges](#badges) — 1 файлов
- [Contacts](#contacts) — 15 файлов
- [Glossary](#glossary) — 4 файлов
- [Habr Unique Projects](#habr-unique-projects) — 56 файлов
- [Lorenzo Agent](#lorenzo-agent) — 62 файлов
- [Nautilus](#nautilus) — 255 файлов
- [Svyazi 2 0](#svyazi-2-0) — 59 файлов
- [Technology Combinations](#technology-combinations) — 53 файлов
- [Templates](#templates) — 24 файлов


## 📁 Docs (`docs/`)

### [[ABBREVIATIONS|Словарь аббревиатур и сокращений]]
> > !TIP

  - Самые часто используемые

_Слов: 1628_

### [[ACTION_ITEMS|Action Items, риски и решения]]
> Автоматически извлечено из всех документов.

  - ➡️ Следующие шаги (150)
  - ✅ Решения и рекомендации (275)
  - ⚠️ Риски (593)
  - 🚫 Ограничения (144)
  - 📋 Задачи (TODO) (24)
  - 📬 Контактные действия (148)

_Слов: 8064_

### [[ALERTS|Callout-блоки]]
> Добавлено 43 callout-блоков в документы.

  - Пример синтаксиса

_Слов: 79_

### [[AUTHORS|Авторы и коллаборации]]
> Авторы проектов, упоминаемые в исследованиях.


_Слов: 158_

### [[AUTOFILLED|Автозаполненные шаблоны]]
> > Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/

  - Файлы
  - Как работает

_Слов: 102_

### [[BACKLINKS|Индекс обратных ссылок]]
> > Файлов с входящими ссылками: 504

  - Топ-30 самых цитируемых документов
  - Ссылки по разделам

_Слов: 397_

### [[BADGES|Status Badges]]
> Обновлено: 2026-04-29

  - Превью
  - Markdown сниппеты для README

_Слов: 46_

### [[CHANGELOG]]
> Всего коммитов: 103

  - semantic (1 коммитов)
  - 2026-04-29 (100 коммитов)
  - 22 скила  (1 коммитов)
  - (1 коммитов)

_Слов: 1541_

### [[CHANGELOG_AUTO|Changelog (авто)]]
> > Сгенерировано из 25 коммитов git-истории.

  - Статистика коммитов
  - История изменений

_Слов: 353_

### [[CLUSTERS|Кластеры тематически близких файлов]]
> > !TIP

  - Кластер 1 — turn, view, svyazi, cardindex (30 файлов)
  - Кластер 2 — anthropic-vacancies, docs, ai-mediated-representation-for-underrepresented-ex, author-contact (23 файлов)
  - Кластер 3 — cowork, ingit, anthropic-vacancies, docs (22 файлов)
  - Кластер 4 — repo, passport, docs, str (17 файлов)
  - Кластер 5 — principal, agent, professional, agents (14 файлов)
  - Кластер 6 — github, documents, com, document (13 файлов)
  - Кластер 7 — профиль, связи, сообщение, первое (12 файлов)
  - Кластер 8 — composite-skills-agent-md, representative-agent-layer-md, markdown, сходство (11 файлов)
  _... ещё 22 разделов_

_Слов: 1380_

### [[CODE_BLOCKS|Code-блоки репозитория]]
> > !TIP

  - 📊 Диаграммы Mermaid (22)
- ... (обрезано)
- ... (обрезано)
  - 🐍 Python (35)
- ... (обрезано)
- ... (обрезано)
- ... (обрезано)
  - 📋 YAML (14)
  _... ещё 41 разделов_

_Слов: 4713_

### [[COMPARE|Сравнение с предыдущим коммитом]]
> Файлов было: 1049  стало: 1194

  - Новые файлы (145)
  - Удалённые файлы (0)
  - Изменившиеся файлы (63) — топ по Δ слов

_Слов: 477_

### [[COMPLEXITY|Оценка читаемости документов]]
> > !WARNING

  - Распределение сложности
  - Самые сложные документы
  - Самые простые документы
  - Методология

_Слов: 605_

### [[COMPONENT_MATRIX|Матрица компонентов Svyazi 2.0]]
> > Совместимость и возможности 14 компонентов экосистемы.

  - Содержание
  - Матрица возможностей
  - Покрытие возможностей
  - Каталог компонентов
  - Рекомендуемые ансамбли

_Слов: 887_

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

_Слов: 13202_

### [[CONCEPT_GRAPH|Граф концептов базы знаний]]
> > Концептов: 40  Связей: 773 (мин. вес: 2)

  - Диаграмма
  - Топ концептов по связям

_Слов: 682_

### [[CONSISTENCY|Согласованность терминов]]
> Анализ различных написаний одних и тех же терминов.

  - Детали по файлам
  - Как исправить
- Пример: заменить все вхождения в docs/

_Слов: 375_

### [[CONTACTS|Контакты и авторы]]
>  Автор  Проект  Слой  Упомянут в файлах  Первый вопрос 

  - Ключевые авторы проектов
  - GitHub репозитории
  - Email адреса
  - Шаблон первого сообщения

_Слов: 547_

### [[CONTACT_PRIORITY|Приоритет контактов]]
> Обновлено: 2026-04-29

  - Топ авторов по приоритету
  - Рекомендуемые следующие шаги
  - Формула расчёта балла

_Слов: 364_

### [[CONTRADICTIONS|Противоречия в базе знаний]]
> > !WARNING

  - Содержание
  - Найденные противоречия

_Слов: 1832_

### [[COST|Оценка стоимости MVP]]
> Ориентировочные цифры на основе документации проекта.

  - Итого
  - По компонентам
  - По ролям
  - Сценарии
  - Временные оценки из документов
  - Допущения

_Слов: 547_

### [[CROSSREFS|Перекрёстные ссылки]]
> > !TIP

  - Проекты → файлы
  - Файлы → проекты

_Слов: 655_

### [[CROSS_SECTION|Кросс-секционный анализ]]
> > (косинусное сходство TF-IDF векторов)

  - Содержание
  - Матрица сходства секций
  - Граф связей
  - Топ-40 кросс-секционных концептов
  - Детальная карта концептов

_Слов: 1256_

### [[DECISIONS|Ключевые решения и выводы]]
> Автоматически извлечено из всех документов: 394 записей

  - Архитектура (37)
  - Mvp (6)
  - Память (12)
  - Оркестрация (15)
  - Безопасность (2)
  - Лицензия (14)
  - Риски (3)
  - Контакты (23)
  _... ещё 1 разделов_

_Слов: 2479_

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
> > Что каждый improve.py производит и от чего зависит.

  - Содержание
  - Зависимости
  - Скрипты без карты зависимостей
  - Порядок запуска (рекомендуемый)

_Слов: 558_

### [[DIGEST|Дайджест изменений]]
> > > 🎯 Проблема: Дайджест изменений Contents - Последний коммит(последний-коммит) - Последние 3 коммита — итого(последние…

  - Contents
  - Последний коммит
  - Последние 3 коммита — итого
  - Новые документы
  - История коммитов (последние 15)
  - Текущее состояние репозитория

_Слов: 487_

### [[DIGEST_AUTO|Автодайджест изменений]]
> Период: 2026-04-22 — 2026-04-29 (7 дней)

  - Сводка
  - Активность по секциям
  - Последние коммиты
  - Новые файлы

_Слов: 281_

### [[DIGEST_WEEKLY|Еженедельный дайджест — 2026-04-29]]
> > Период: последние 7 дней (с 2026-04-22)

  - Итого
  - Коммиты

_Слов: 213_

### [[DUPLICATES|Отчёт о дублировании]]
> > !TIP

  - Похожие файлы (Jaccard ≥ 0.5)

_Слов: 2733_

### [[EMPTY_SECTIONS|Пустые секции]]
> > !TIP

  - Содержание
  - Файлы с ≥50% пустых секций (приоритет)
  - Все файлы с пустыми секциями

_Слов: 12093_

### [[ENTITIES|Именованные сущности]]
> Файлов просмотрено: 1191

  - Люди и авторы (7)
  - Проекты (22)
  - Организации (9)
  - Технологии и стандарты (24)
  - GitHub репозитории (15)
  - Ко-встречаемость проектов (топ пары)

_Слов: 742_

### [[FAQ|Часто задаваемые вопросы (FAQ)]]
> Извлечено: 125 вопросов и ответов

  - Архитектура
  - MVP/Запуск
  - Компоненты
  - Интеграция
  - Лицензия
  - Общее

_Слов: 892_

### [[FOOTNOTES|Сноски и определения терминов]]
> Обновлено файлов: 4  Вставлено сносок: 14

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

_Слов: 2656_

### [[HEADING_AUDIT|Аудит заголовков]]
> > !TIP

  - Содержание
  - Типы проблем
  - По файлам

_Слов: 9028_

### [[HEALTH|Health Dashboard]]
> Обновлено: 2026-04-29

  - Общий балл: 77/100 🟡
  - Метрики
  - Структура репозитория
  - Action Items
  - Скрипты обработки
  - Рекомендации

_Слов: 214_

### [[HEATMAP|Тепловая карта тем]]
> > !TIP

  - Числовые значения (‰)
  - Доминирующие темы по разделам
  - Концентрация тем

_Слов: 537_

### [[INDEX|Индекс документации — Lorenzo / Svyazi 2.0]]
> > !TIP

  - Содержание
  - Метрики репозитория
  - Разделы документации
  - Аналитика и отчёты
  - Ключевые документы
  - LLM-обогащение (Ступень 3)
  - Быстрый старт
- Читать документацию
  _... ещё 2 разделов_

_Слов: 616_

### [[KEYWORD_INDEX|Инвертированный индекс ключевых слов]]
> > > 🎯 Проблема: Инвертированный индекс ключевых слов Обновлено: 2026-04-29 Уникальных слов: 23264 Биграмм: 13489 Файлов:…

  - Топ слов по охвату файлов
  - Топ биграмм (устойчивые словосочетания)

_Слов: 1138_

### [[KNOWLEDGE_MAP|Карта базы знаний Lorenzo]]
> > - - - - - - - - - -  Как реализован forensic RAG с доказуемостью? Карта базы знаний Lorenzo(docs/KN

  - Содержание
  - Корпус
  - Метрики качества
  - По секциям
  - Ключевые концепты
  - Топ сущностей
  - Открытые вопросы
  - Быстрые команды
  _... ещё 3 разделов_

_Слов: 661_

### [[KPI|Числовые KPI и метрики]]
> > !TIP

  - Количество (242)
  - Проценты (199)
  - Время (278)
  - Стоимость (463)
  - Размер (32)
  - Версия (390)
  - Рейтинг (47)
  - Этап (71)

_Слов: 2541_

### [[KPI_HISTORY|История метрик KPI]]
> > Последнее обновление: 2026-04-29 · Снапшотов в истории: 1

  - Текущие метрики

_Слов: 106_

### [[LANGUAGE_STATS|Языковой состав документов]]
> > !TIP

  - Содержание
  - Распределение
  - Файлы с неожиданным языком
  - Смешанные файлы (MIX)
  - По секциям

_Слов: 6767_

### [[LINKS|Индекс ссылок]]
> Всего уникальных URL: 230


_Слов: 1029_

### [[LLM_SUMMARIES|AI-саммари разделов документации]]
> > Модель: claude-haiku-4-5 · Разделов: 5

  - Архитектура Svyazi 2.0
  - Вакансии Anthropic
  - Комбинации технологий
  - AI-коллаборации
  - Хабр-проекты

_Слов: 177_

### [[MCP_DASHBOARD|MCP Dashboard]]
> Обновлено: 2026-04-29

  - По серверам
  - Топ-15 инструментов (с латентностью)
  - Латентность по серверам

_Слов: 327_

### [[METRICS|Метрики качества документации]]
> Файлов: 1174  Средний балл: 71.2/100

  - Качество по разделам
  - Топ-15 лучших документов
  - Документы, требующие улучшения (18)
  - Общие показатели

_Слов: 465_

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
  - 👤 People (20)
  - 📦 Projects (138)
  - ⚙️ Tech (31)
  - 🏢 Orgs (8)
  - 📅 Dates (36)

_Слов: 1669_

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

_Слов: 1043_

### [[NETWORK|Сеть проектов и авторов]]
> Узлов: 20  Связей: 189

  - Топ-20 ко-упоминаемых пар
  - Центральность узлов (влиятельность)
  - Авторы ↔ Проекты

_Слов: 413_

### [[ONBOARDING|Онбординг — Svyazi 2.0 / Lorenzo]]
> > !TIP

  - Содержание
  - Что это такое?
  - Первые 30 минут
- 1. Клонировать репозиторий
- 2. Прочитать Executive Summary
- 3. Посмотреть статус проекта
- 4. Прочитать FAQ
- 5. Запустить скрипты (генерация/обновление docs)
  _... ещё 11 разделов_

_Слов: 552_

### [[ORPHANS|Изолированные документы (Orphans)]]
> Найдено: 1 файлов без входящих ссылок из 1050 проверено.

  - Топ-20 по объёму (важные и изолированные)
  - По разделам
  - Рекомендации

_Слов: 105_

### [[PARAGRAPH_QUALITY|Качество абзацев]]
> > !TIP

  - Содержание
  - Типы проблем
  - По файлам

_Слов: 15375_

### [[PASSIVE_VOICE|Пассивный залог и канцеляризмы]]
> > Файлов: 882  Средний пассив: 1.7% (🟢 Активный стиль)

  - Корпусная статистика
  - Топ файлов по доле пассива

_Слов: 408_

### [[PRIORITIES|Приоритеты файлов]]
> > !TIP

  - Топ-50 самых важных файлов
  - Топ-5 по каждому разделу

_Слов: 3028_

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

_Слов: 261_

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
  _... ещё 101 разделов_

_Слов: 1363_

### [[QUESTIONS|Открытые вопросы]]
> > !WARNING

  - Архитектура (31)
  - Интеграция (20)
  - Mvp/сроки (28)
  - Технология (134)
  - Лицензия (21)
  - Команда (38)
  - Общее (701)

_Слов: 1838_

### [[READING_LIST|Список чтения]]
> > по запросу «RAG retrieval»  Документов: 5  Время: ~20 мин (0ч 20м)

  - По секциям

_Слов: 232_

### [[READING_ORDER|Рекомендуемый порядок чтения]]
> От базовых концепций к сложным. Начните с зелёных (🟢), затем жёлтые (🟡), красные (🔴).

  - Маршруты по целям

_Слов: 5947_

### [[README|docs]]
> Файлов: 103

  - Содержание
  - Подразделы

_Слов: 778_

### [[REGISTRY|REGISTRY — реестр артефактов Lorenzo]]
> - Сводка(#сводка)

  - Содержание
  - Сводка
  - Скрипты по группам
  - Шаблоны
  - Скилы
  - MCP-серверы
  - Манифесты задач
  - Контакты
  _... ещё 7 разделов_

_Слов: 1347_

### [[REPORT|Svyazi 2.0 — Knowledge Base Report]]
> Сгенерировано автоматически: 2026-04-29

  - Содержание
  - Executive Summary
  - Корпус документов
  - Ключевые проекты
  - Ключевые сущности
  - Архитектурные решения
  - Открытые вопросы
  - Рекомендуемое чтение
  _... ещё 4 разделов_

_Слов: 911_

### [[RISK_REGISTER|Реестр рисков — Svyazi 2.0]]
> > !TIP

  - Содержание
  - Матрица рисков (Вероятность × Влияние)
  - Реестр
  - Митигации
  - Упоминания рисков в документах
  - Итоговая статистика

_Слов: 944_

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

### [[SCRIPTS_CATALOG|Каталог скриптов]]
> - По группам(#по-группам)

  - Содержание
  - По группам
  - Подробно

_Слов: 7749_

### [[SEARCH_RESULTS|Результаты поиска]]
> > <!-- tags: security, knowledge -->


_Слов: 91_

### [[SEE_ALSO|Индекс «Смотрите также»]]
> Файлов с блоком See Also: 1066

  - Ключевые связи

_Слов: 220_

### [[SENTIMENT|Тональный анализ документов]]
> Файлов проанализировано: 1032

  - Тональность по разделам
  - Самые оптимистичные документы
  - Самые скептичные / риск-ориентированные
  - Распределение тональности

_Слов: 487_

### [[SIMILAR|Похожие документы]]
> > !TIP

  - Топ-20 самых похожих пар
  - По разделам

_Слов: 341_

### [[SIMILAR_PASSAGES|Похожие абзацы между документами]]
> > !TIP

  - Содержание
  - Contents
  - Найденные похожие абзацы

_Слов: 1931_

### [[SITEMAP|Карта репозитория Lorenzo]]
> Обновлено: 2026-04-29

  - Навигация
  - Мета-документы
  - Svyazi 2.0 — Архитектура системы
  - Вакансии Anthropic — 436 позиций
  - Комбинации технологий
  - AI Коллаборации — ансамбли проектов
  - Хабр-проекты — память и граф
  - ai-collaborations
  _... ещё 10 разделов_

_Слов: 7078_

### [[SKILL_DASHBOARD|Skill Dashboard]]
> > Лог метрик не найден (.claude/skillmetrics.jsonl).


_Слов: 35_

### [[SOURCE_MAP|Карта происхождения текстов]]
> > !TIP

  - Содержание
  - Категории
  - Авторы
  - 🤖 Авто-импортированные файлы (846)
  - 🔗 Файлы с внешними ссылками (98)

_Слов: 6167_

### [[STATS|Детальная статистика репозитория]]
> Разделов: 18  Файлов: 1191  Слов: 944,176  Символов: 8,446,856

  - Сводная таблица по разделам
  - Топ-20 файлов по объёму
  - Ключевые показатели

_Слов: 630_

### [[SUMMARIES|Резюме документов (TextRank)]]
> > !TIP

  - Содержание
  - Contents
  - docs/01-svyazi/01-executive-summary.md
  - docs/01-svyazi/02-methodology.md
  - docs/01-svyazi/03-component-catalog.md
  - docs/01-svyazi/04-ensembles-overview.md
  - docs/01-svyazi/06-security-privacy.md
  - docs/01-svyazi/07-mvp-planning.md
  _... ещё 44 разделов_

_Слов: 3910_

### [[TABLES|Все таблицы репозитория]]
> > !TIP

  - 01-svyazi (11 таблиц)
  - 02-anthropic-vacancies (34 таблиц)
  - 03-technology-combinations (1 таблиц)
  - 04-ai-collaborations (38 таблиц)
  - 05-habr-projects (6 таблиц)
  - ai-collaborations (13 таблиц)
  - anthropic-vacancies (2 таблиц)
  - contacts (14 таблиц)
  _... ещё 8 разделов_

_Слов: 117329_

### [[TAGS|Индекс тегов]]
> Каждый файл помечен тегами по темам автоматически.

  - #anthropic (56 файлов)
  - #architecture (57 файлов)
  - #collaboration (65 файлов)
  - #ingestion (56 файлов)
  - #knowledge (44 файлов)
  - #local-first (29 файлов)
  - #memory (45 файлов)
  - #orchestration (34 файлов)
  _... ещё 4 разделов_

_Слов: 600_

### [[TASKS_INDEX|Каталог задач (TASKSINDEX)]]
> - По MCP-серверу(#по-mcp-серверу)

  - Содержание
  - По MCP-серверу
  - Подробно

_Слов: 1012_

### [[TECH_RADAR|Tech Radar — Svyazi 2.0]]
> > !WARNING

  - Содержание
  - Обзор
  - 🟢 ADOPT
  - 🔵 TRIAL
  - 🟡 ASSESS
  - 🔴 HOLD
  - Методология

_Слов: 612_

### [[TIMELINE|Хронология и временные маркеры]]
> > !TIP

  - Точная дата (2041)
  - Год (134)
  - Квартал (9)
  - Месяц+год (217)
  - Период (24)
  - Фаза (500)
  - Длительность (323)
  - Версия (1003)

_Слов: 4348_

### [[VALIDATION|Валидация структуры репозитория]]
> Ошибок: 0  Предупреждений: 42  Пройдено: 27

  - Сводка
  - ✅ Разделы и README
  - ✅ Мета-файлы
  - Пустые/короткие файлы
  - Именование файлов
  - Заголовки H1
  - Внутренние ссылки
  - Итог

_Слов: 581_

### [[VOCABULARY|Богатство словаря документов]]
> > Файлов: 1115  Токенов: 766,510  Уникальных: 287,065

  - Содержание
  - Корпусная статистика
  - Топ файлов по богатству словаря (STTR)
  - Файлы с бедным словарём (требуют доработки)
  - Справка по метрикам

_Слов: 943_

### [[WORD_CLOUD|Word Cloud]]
> > Визуализация 80 самых частых слов репозитория.

  - Топ-20 слов

_Слов: 212_

### [[WORD_FREQ|Частотный анализ слов]]
> Всего слов (очищенных): 661,851

  - Глобальный топ-50 слов
  - Топ-15 слов по разделам
  - Уникальные слова разделов

_Слов: 2786_

### [[reading-paths|Reading paths — рекомендуемые маршруты по монорепозиторию]]
> > !TIP

  - Содержание
  - 1. «Я хочу понять, что такое Lorenzo (имя репозитория)»
  - 2. «Я хочу собрать прототип Svyazi 2.0»
  - 3. «Я хочу понять Nautilus Portal Protocol»
  - 4. «Я хочу комбинировать технологии для новых свойств»
  - 5. «Я ищу коллабораторов на Хабре»
  - 6. «Я разбираю карьерные опции в Anthropic»
  - 7. «Я ищу конкретный компонент по имени»
  _... ещё 2 разделов_

_Слов: 627_

**Итого в секции: 283,083 слов, 92 файлов**


## 📁 Svyazi (`docs/01-svyazi/`)

### [[00-intro-part2|Продолжение исследования для Svyazi 2.0]]

_Слов: 6_

### [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - Главная линия синергии
  - Ключевой вывод
  - Что добавляет продолжение исследования
  - Приоритет ансамблей для старта

_Слов: 726_

### [[02-methodology|Методика и рамка отбора проектов]]
> > Абстракт (авто)

  - Contents
  - Источники
  - Шкала зрелости
  - Принцип отбора паттернов
  - Принципы интеграционной оценки

_Слов: 480_

### [[03-component-catalog|Карта найденных проектов и паттернов]]

_Слов: 1383_

### [[04-ensembles-overview|Приоритетные ансамбли]]

_Слов: 1288_

### [[06-security-privacy|Безопасность, приватность и бюджетный роутинг]]

_Слов: 823_

### [[07-mvp-planning|План прототипа и возможные контакты]]

_Слов: 1063_

### [[08-conclusions|Выводы]]

_Слов: 380_

### [[09-architectural-gaps|Архитектурные зазоры, которые важнее новых инструментов]]

_Слов: 758_

### [[10-second-order-ensembles|Новые ансамбли следующего шага]]

_Слов: 908_

### [[11-integration-contracts|Интеграционный контракт, который стоит зафиксировать сразу]]

_Слов: 737_

### [[12-roadmap|Дорожная карта прототипа следующей итерации]]

_Слов: 722_

### [[13-contacts|Контактная стратегия и узкие вопросы для авторов]]

_Слов: 806_

### [[14-limitations|Ограничения, лицензии и что пока лучше не склеивать]]

_Слов: 638_

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

_Слов: 110_

**Итого в секции: 11,052 слов, 16 файлов**


## 📁 Anthropic Vacancies (`docs/02-anthropic-vacancies/`)

### [[00-intro|Введение]]
> > Абстракт (авто)

  - Содержание

_Слов: 8934_

### [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]]
> > Абстракт (авто)

  - Содержание
  - Интегральный анализ профиля svend4

_Слов: 19144_

### [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]]
> > Абстракт (авто)

  - Содержание
  - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL
- portal-mcp.py

_Слов: 3207_

### [[03-portal-protocol-md|PORTAL-PROTOCOL.md]]
> > Status: Draft (Working Document)

  - PORTAL-PROTOCOL.md
- Nautilus Portal Protocol

_Слов: 75_

### [[04-abstract|Abstract]]
> > The Nautilus Portal Protocol (далее — NPP) определяет способ федерации

  - Abstract

_Слов: 126_

### [[05-0-status-of-this-document|0. Status of This Document]]
> > Этот документ — рабочий черновик Nautilus Portal Protocol v1.0. Он может

  - 0. Status of This Document

_Слов: 101_

### [[06-1-introduction|1. Introduction]]
> > Абстракт (авто)

  - Contents
  - 1. Introduction

_Слов: 383_

### [[07-2-terminology|2. Terminology]]
> > Абстракт (авто)

  - 2. Terminology

_Слов: 302_

### [[08-3-registry-nautilus-json|3. Registry (nautilus.json)]]
> > Абстракт (авто)

  - Contents
  - 3. Registry (nautilus.json)

_Слов: 403_

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

_Слов: 144_

### [[102-доступ-к-данным|Доступ к данным]]
> - Тип: static

  - Доступ к данным

_Слов: 23_

### [[103-appendix-b-change-log|Appendix B: Change Log]]
> - Appendix B: Change Log(#appendix-b-change-log)

  - Contents
  - Appendix B: Change Log

_Слов: 170_

### [[104-appendix-c-references|Appendix C: References]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: References

_Слов: 955_

### [[105-review-methodology-md|REVIEWMETHODOLOGY.md]]
> > Статус: Активно применяется в проекте svend4/nautilus

  - REVIEWMETHODOLOGY.md
- Трёхфазная методология Review в Nautilus

_Слов: 74_

### [[106-tl-dr|TL;DR]]
> > Для критически важных документов проекта применяется

  - TL;DR

_Слов: 128_

### [[107-1-контекст-и-мотивация|1. Контекст и мотивация]]
> > Абстракт (авто)

  - Contents
  - 1. Контекст и мотивация

_Слов: 455_

### [[108-2-формальный-workflow|2. Формальный workflow]]
> > Абстракт (авто)

  - Contents
  - 2. Формальный workflow

_Слов: 463_

### [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]]
> - 3. Принципы консолидации (Фаза C)(#3-принципы-консолидации-фаза-c)

  - Содержание
  - 3. Принципы консолидации (Фаза C)
- LOC в Python-коде
- Количество тестов
- Число адаптеров
- Health score
- Q6-покрытие
- Native Format
  _... ещё 1 разделов_

_Слов: 560_

### [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или осмысленный?]]
> > Абстракт (авто)

  - Вопрос: fallback-ratio как критический или осмысленный?

_Слов: 338_

### [[111-4-условия-применимости|4. Условия применимости]]
> > Абстракт (авто)

  - Contents
  - 4. Условия применимости

_Слов: 272_

### [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]]
> > !WARNING

  - Contents
  - 5. Связь с существующими методологиями

_Слов: 389_

### [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assisted workflows]]
> > Традиционная software engineering оптимизировалась против

  - 6. Почему это валидный паттерн для AI-assisted workflows

_Слов: 150_

### [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]]
> > Абстракт (авто)

  - Contents
  - 7. Реализация в проекте Nautilus

_Слов: 309_

### [[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]]
> > Абстракт (авто)

  - Contents
  - 8. Ограничения и открытые вопросы

_Слов: 447_

### [[116-9-checklist-применения-методологии|9. Checklist применения методологии]]
> > Абстракт (авто)

  - Contents
  - 9. Checklist применения методологии

_Слов: 399_

### [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим документам]]
> > !WARNING

  - Contents
  - 10. Конкретный план применения к текущим документам
- В Termux

_Слов: 315_

### [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]]
> > !WARNING

  - Appendix A: Шаблон для header warning

_Слов: 175_

### [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешения]]
> > Абстракт (авто)

  - Contents
  - Appendix B: Примеры расхождений и их разрешения

_Слов: 372_

### [[12-content-overview|Content Overview]]
> > Что внутри: типы данных, приблизительный объём, основные темы.

  - Content Overview

_Слов: 41_

### [[120-главные-технические-риски|Главные технические риски]]
> > Два независимых анализа выделили разные приоритеты:

  - Главные технические риски

_Слов: 82_

### [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]]
> > Первая формализация, основана на опыте применения к

  - Appendix C: История изменений методологии

_Слов: 47_

### [[122-глоссарий|Глоссарий]]
> > Абстракт (авто)

  - Содержание
  - Глоссарий

_Слов: 1334_

### [[123-portal-mcp-py|portal-mcp.py]]
> > Абстракт (авто)

  - portal-mcp.py
- ============================================================
- MCP SDK imports
- ============================================================
- # We use the official MCP Python SDK. If not installed, user gets
- a clear error with install instructions.
- try:
- ============================================================
  _... ещё 51 разделов_

_Слов: 2282_

### [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]]
> > После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигураци…

  - Конфигурация для Claude Desktop

_Слов: 177_

### [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]]
> > Отдельный документ для репо, объясняющий, как настроить MCP-обёртку:

  - README-MCP.md— инструкция по установке
- Nautilus Portal MCP Integration

_Слов: 98_

### [[126-установка|Установка]]
> - Установка(#установка)

  - Contents
  - Установка
- Ждёт stdio-input; Ctrl+C для выхода

_Слов: 145_

### [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]]
> - Подключение к Claude Desktop(#подключение-к-claude-desktop)

  - Contents
  - Подключение к Claude Desktop

_Слов: 125_

### [[128-доступные-инструменты|Доступные инструменты]]
> > После успешной интеграции Claude Desktop получает доступ к 7 tools:

  - Доступные инструменты

_Слов: 136_

### [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]]
> > После подключения Claude может использовать tools автоматически.

  - Примеры запросов (в Claude)

_Слов: 110_

### [[13-angle-perspective|Angle / Perspective]]
> > С какого угла Repo смотрит на общие концепты

  - Angle / Perspective

_Слов: 68_

### [[130-отладка|Отладка]]
> - Отладка(#отладка)

  - Contents
  - Отладка

_Слов: 174_

### [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]]
> > - Работает только в stdio mode (HTTP-mode планируется)

  - Ограничения текущей версии (0.1.0-draft)

_Слов: 100_

### [[132-planned-v0-2-0|Planned (v0.2.0)]]
> > - HTTP-mode для debugging и remote access

  - Planned (v0.2.0)

_Слов: 73_

### [[133-обратная-связь|Обратная связь]]
> > Абстракт (авто)

  - Содержание
  - Обратная связь
- MCP интеграция (для Claude Desktop)
- Конфигурация: см. README-MCP.md
- В приватном репо cases-private:

_Слов: 17018_

### [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]]
> > - 187-слой-представительских-агентов-md(docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) (сходств…

  - THE DOUBLE-TRIANGLE ARCHITECTURE.md
- The Double-Triangle Architecture

_Слов: 46_

### [[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in Distributed Knowledge Work]]
> > Editorial review: Claude (intellectual collaboration, 2026-04)

  - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work

_Слов: 91_

### [[136-abstract|Abstract]]
> > Абстракт (авто)

  - Abstract

_Слов: 382_

### [[137-table-of-contents|Table of Contents]]
> > 1. Why Single-Triangle Models Are Incomplete

  - Table of Contents

_Слов: 94_

### [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 1. Why Single-Triangle Models Are Incomplete

_Слов: 584_

### [[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]]
> > Абстракт (авто)

  - Содержание
  - 2. The Double-Triangle Architecture
- Bridges
  - Bridges

_Слов: 753_

### [[140-3-three-inter-layer-protocols|3. Three Inter-Layer Protocols]]
> > Абстракт (авто)

  - Содержание
  - 3. Three Inter-Layer Protocols

_Слов: 873_

### [[141-4-nautilus-portal-as-reference-substrate|4. Nautilus Portal as Reference Substrate]]
> > Абстракт (авто)

  - Содержание
  - 4. Nautilus Portal as Reference Substrate

_Слов: 699_

### [[142-5-pattern-library-as-bridge-between-triangles|5. Pattern Library as Bridge Between Triangles]]
> > Абстракт (авто)

  - Содержание
  - 5. Pattern Library as Bridge Between Triangles

_Слов: 704_

### [[143-6-four-deployment-domains|6. Four Deployment Domains]]
> > !TIP

  - Содержание
  - 6. Four Deployment Domains

_Слов: 699_

### [[144-7-open-questions|7. Open Questions]]
> > Абстракт (авто)

  - Содержание
  - 7. Open Questions

_Слов: 759_

### [[145-8-call-to-action|8. Call to Action]]
> > Абстракт (авто)

  - Содержание
  - 8. Call to Action

_Слов: 732_

### [[146-acknowledgments|Acknowledgments]]
> > !TIP

  - Acknowledgments

_Слов: 190_

### [[147-references|References]]
> > Абстракт (авто)

  - Contents
  - References

_Слов: 340_

### [[148-appendix-a-glossary|Appendix A: Glossary]]
> > Абстракт (авто)

  - Appendix A: Glossary

_Слов: 309_

### [[149-appendix-b-summary-of-contributions|Appendix B: Summary of Contributions]]
> > 1. Topological formalization of Double-Triangle Architecture

  - Appendix B: Summary of Contributions
- Author & Contact
  - Author & Contact

_Слов: 185_

### [[150-appendix-c-version-history|Appendix C: Version History]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: Version History

_Слов: 8408_

### [[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]]
> > - 273-infrastructure-for-ai-collaborative-intellectual-w(docs/02-anthropic-vacancies/273-infrastructure-for-ai-collabo…

  - OPEN KNOWLEDGE WORK FOUNDATION.md
- Open Knowledge Work Foundation

_Слов: 48_

### [[152-ai-coordinated-infrastructure-for-distributed-expe|AI-Coordinated Infrastructure for Distributed Expert Contribution]]
> > Editorial collaboration: Claude (intellectual development, 2026-04)

  - AI-Coordinated Infrastructure for Distributed Expert Contribution

_Слов: 86_

### [[153-executive-summary|Executive Summary]]
> > Абстракт (авто)

  - Executive Summary

_Слов: 369_

### [[154-table-of-contents|Table of Contents]]
> > 3. Why Existing Solutions Fail

  - Table of Contents

_Слов: 81_

### [[155-1-problem-statement|1. Problem Statement]]
> > Абстракт (авто)

  - Содержание
  - 1. Problem Statement

_Слов: 638_

### [[156-2-target-populations|2. Target Populations]]
> > Абстракт (авто)

  - Содержание
  - 2. Target Populations

_Слов: 689_

### [[157-3-why-existing-solutions-fail|3. Why Existing Solutions Fail]]
> > Абстракт (авто)

  - Содержание
  - 3. Why Existing Solutions Fail

_Слов: 700_

### [[158-4-proposed-infrastructure|4. Proposed Infrastructure]]
> > Абстракт (авто)

  - Содержание
  - 4. Proposed Infrastructure

_Слов: 1023_

### [[159-5-economic-model|5. Economic Model]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 5. Economic Model

_Слов: 660_

### [[16-history|History]]
> > Когда создан, ключевые версии, направление развития.

  - History

_Слов: 85_

### [[160-6-governance-and-ethics|6. Governance and Ethics]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Governance and Ethics

_Слов: 605_

### [[161-7-phased-rollout-plan|7. Phased Rollout Plan]]
> > Абстракт (авто)

  - Содержание
  - 7. Phased Rollout Plan

_Слов: 655_

### [[162-8-risk-analysis|8. Risk Analysis]]
> > Абстракт (авто)

  - Содержание
  - 8. Risk Analysis

_Слов: 685_

### [[163-9-call-for-partnership|9. Call for Partnership]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Call for Partnership

_Слов: 628_

### [[164-10-appendices|10. Appendices]]
> > Абстракт (авто)

  - Содержание
  - 10. Appendices

_Слов: 960_

### [[165-closing|Closing]]
> > Абстракт (авто)

  - Содержание
  - Closing
- unknownlegalconcepts.yml

_Слов: 9298_

### [[166-representative-agent-layer-md|REPRESENTATIVE AGENT LAYER.md]]
> > - 187-слой-представительских-агентов-md(docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) (сходств…

  - REPRESENTATIVE AGENT LAYER.md
- The Representative Agent Layer

_Слов: 46_

### [[167-ai-mediated-representation-for-underrepresented-ex|AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]
> > - Open Knowledge Work Foundation Concept Document v1.0

  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations

_Слов: 108_

### [[168-abstract|Abstract]]
> > Абстракт (авто)

  - Abstract

_Слов: 338_

### [[169-table-of-contents|Table of Contents]]
> > 1. The Cinderella Syndrome: Why Quality Stays Invisible

  - Table of Contents

_Слов: 109_

### [[17-5-compatibility-levels|5. Compatibility Levels]]
> > Абстракт (авто)

  - Contents
  - 5. Compatibility Levels

_Слов: 314_

### [[170-1-the-cinderella-syndrome-why-quality-stays-invisi|1. The Cinderella Syndrome: Why Quality Stays Invisible]]
> > Абстракт (авто)

  - Содержание
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible

_Слов: 842_

### [[171-2-historical-precedents-agents-as-civilizational-i|2. Historical Precedents: Agents as Civilizational Innovation]]
> > Абстракт (авто)

  - Содержание
  - 2. Historical Precedents: Agents as Civilizational Innovation

_Слов: 964_

### [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]]
> > Абстракт (авто)

  - Содержание
  - 3. What Makes a Representative Agent

_Слов: 671_

### [[173-4-ten-domains-of-application|4. Ten Domains of Application]]
> > Абстракт (авто)

  - Содержание
  - 4. Ten Domains of Application

_Слов: 1608_

### [[174-5-architectural-specification|5. Architectural Specification]]
> > Абстракт (авто)

  - Содержание
  - 5. Architectural Specification

_Слов: 656_

### [[175-6-ethical-framework|6. Ethical Framework]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Ethical Framework

_Слов: 612_

### [[176-7-governance-and-oversight|7. Governance and Oversight]]
> > Абстракт (авто)

  - Contents
  - 7. Governance and Oversight

_Слов: 467_

### [[177-8-risks-and-mitigations|8. Risks and Mitigations]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Risks and Mitigations

_Слов: 620_

### [[178-9-phased-rollout-strategy|9. Phased Rollout Strategy]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Phased Rollout Strategy

_Слов: 632_

### [[179-10-open-questions|10. Open Questions]]
> > Абстракт (авто)

  - Contents
  - 10. Open Questions

_Слов: 420_

### [[18-6-adapter-interface|6. Adapter Interface]]
> > Абстракт (авто)

  - Contents
  - 6. Adapter Interface

_Слов: 440_

### [[180-11-call-for-collaboration|11. Call for Collaboration]]
> > Абстракт (авто)

  - Contents
  - 11. Call for Collaboration

_Слов: 452_

### [[181-12-closing|12. Closing]]
> > Абстракт (авто)

  - 12. Closing

_Слов: 268_

### [[182-acknowledgments|Acknowledgments]]
> > !TIP

  - Acknowledgments

_Слов: 169_

### [[183-references|References]]
> > Абстракт (авто)

  - Contents
  - References

_Слов: 311_

### [[184-appendix-a-connection-to-companion-papers|Appendix A: Connection to Companion Papers]]
> > This paper builds on three previous documents:

  - Appendix A: Connection to Companion Papers

_Слов: 157_

### [[185-appendix-b-domain-comparison-matrix|Appendix B: Domain Comparison Matrix]]
>  Domain  Privacy Sensitivity  Adversarial Risk  Regulatory Complexity  Deployment Readiness 

  - Appendix B: Domain Comparison Matrix

_Слов: 155_

### [[186-appendix-c-sample-use-cases-in-detail|Appendix C: Sample Use Cases in Detail]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: Sample Use Cases in Detail

_Слов: 2035_

### [[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]]
> > - 166-representative-agent-layer-md(docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) (сходство 0.33)

  - СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md
- Слой Представительских Агентов

_Слов: 45_

### [[188-ai-опосредованное-представительство-для-недопредст|AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения]]
> > Сопроводительный документ к:

  - AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения

_Слов: 106_

### [[189-аннотация|Аннотация]]
> > !WARNING

  - Аннотация

_Слов: 356_

### [[19-7-portalentry-structure|7. PortalEntry Structure]]
> > Абстракт (авто)

  - 7. PortalEntry Structure

_Слов: 251_

### [[190-содержание|Содержание]]
> > 1. Синдром Золушки: Почему качество остаётся невидимым

  - Содержание

_Слов: 98_

### [[191-1-синдром-золушки-почему-качество-остаётся-невидим|1. Синдром Золушки: Почему качество остаётся невидимым]]
> > !WARNING

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым

_Слов: 821_

### [[192-2-исторические-прецеденты-агенты-как-цивилизационн|2. Исторические прецеденты: Агенты как цивилизационная инновация]]
> > Абстракт (авто)

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация

_Слов: 950_

### [[193-3-что-делает-агента-представительским|3. Что делает агента Представительским]]
> > !WARNING

  - Содержание
  - 3. Что делает агента Представительским

_Слов: 666_

### [[194-4-десять-областей-применения|4. Десять областей применения]]
> > Абстракт (авто)

  - Содержание
  - 4. Десять областей применения

_Слов: 1634_

### [[195-5-архитектурная-спецификация|5. Архитектурная спецификация]]
> > !WARNING

  - Содержание
  - 5. Архитектурная спецификация

_Слов: 665_

### [[196-6-этическая-рамка|6. Этическая рамка]]
> > !WARNING

  - Содержание
  - Contents
  - 6. Этическая рамка

_Слов: 610_

### [[197-7-управление-и-надзор|7. Управление и надзор]]
> > !WARNING

  - Contents
  - 7. Управление и надзор

_Слов: 459_

### [[198-8-риски-и-меры-противодействия|8. Риски и меры противодействия]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Риски и меры противодействия

_Слов: 658_

### [[199-9-стратегия-поэтапного-развёртывания|9. Стратегия поэтапного развёртывания]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Стратегия поэтапного развёртывания

_Слов: 664_

### [[20-8-consensus-algorithm|8. Consensus Algorithm]]
> > Абстракт (авто)

  - Contents
  - 8. Consensus Algorithm

_Слов: 317_

### [[200-10-открытые-вопросы|10. Открытые вопросы]]
> > Абстракт (авто)

  - Contents
  - 10. Открытые вопросы

_Слов: 402_

### [[201-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]]
> > Абстракт (авто)

  - Contents
  - 11. Призыв к сотрудничеству

_Слов: 471_

### [[202-12-заключение|12. Заключение]]
> > Синдром Золушки — качество без видимости — не нов. Он формировал человеческий труд и признание задолго до компьютеров.…

  - 12. Заключение

_Слов: 185_

### [[203-благодарности|Благодарности]]
> > Эта концепция возникла через диалог в нескольких сессиях в 2026 году. Формулировка «Синдром Золушки» и расширение к со…

  - Благодарности

_Слов: 169_

### [[204-ссылки|Ссылки]]
> > Абстракт (авто)

  - Contents
  - Ссылки

_Слов: 303_

### [[205-приложение-a-связь-с-сопроводительными-статьями|Приложение A: Связь с Сопроводительными Статьями]]
> > Эта статья опирается на три предыдущих документа:

  - Приложение A: Связь с Сопроводительными Статьями

_Слов: 150_

### [[206-приложение-b-матрица-сравнения-областей|Приложение B: Матрица Сравнения Областей]]
>  Область  Чувствительность Конфиденциальности  Состязательный Риск  Регулятивная Сложность  Готовность к Развёртыванию 

  - Приложение B: Матрица Сравнения Областей

_Слов: 157_

### [[207-приложение-c-образцы-случаев-использования-в-детал|Приложение C: Образцы Случаев Использования в Деталях]]
> > Абстракт (авто)

  - Содержание
  - Приложение C: Образцы Случаев Использования в Деталях

_Слов: 4108_

### [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]]
> > - 249-composite-skills-agent-md(docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) (сходство 0.14)

  - PROFESSIONAL COLLEAGUE AGENTS.md
- Professional Colleague Agents

_Слов: 45_

### [[209-a-typology-of-ai-agents-on-the-principal-side-and-|A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers]]
> > - Representative Agent Layer v1.0

  - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers

_Слов: 123_

### [[21-9-query-flow|9. Query Flow]]
> - 9. Query Flow(#9-query-flow)

  - Contents
  - 9. Query Flow

_Слов: 180_

### [[210-abstract|Abstract]]
> > Абстракт (авто)

  - Abstract

_Слов: 361_

### [[211-table-of-contents|Table of Contents]]
> > 1. The Five-Type Typology of Principal-Side Agents

  - Table of Contents

_Слов: 116_

### [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]]
> > Абстракт (авто)

  - Содержание
  - 1. The Five-Type Typology of Principal-Side Agents

_Слов: 923_

### [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]]
> > Абстракт (авто)

  - Содержание
  - 2. What Makes a Professional Colleague Agent

_Слов: 834_

### [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]]
> > Абстракт (авто)

  - Содержание
  - 3. Empirical Case Study: «Обучай»

_Слов: 851_

### [[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Agents]]
> > Абстракт (авто)

  - Содержание
  - 4. Architecture of Professional Colleague Agents

_Слов: 888_

### [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replication]]
> > Абстракт (авто)

  - Содержание
  - 5. The Economics of Profession-Wide Replication

_Слов: 761_

### [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]]
> > Абстракт (авто)

  - Содержание
  - 6. Risks Specific to this Category

_Слов: 1192_

### [[218-7-application-domains|7. Application Domains]]
> > Абстракт (авто)

  - Содержание
  - 7. Application Domains

_Слов: 736_

### [[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]]
> > Абстракт (авто)

  - Содержание
  - 8. Pilot Proposal: SGB Advocate Colleague

_Слов: 961_

### [[22-10-queryresult-structure|10. QueryResult Structure]]
> > resultsbyrepo: dictstr, listPortalEntry

  - 10. QueryResult Structure

_Слов: 130_

### [[220-9-relationship-to-other-agent-types|9. Relationship to Other Agent Types]]
> > Абстракт (авто)

  - Содержание
  - 9. Relationship to Other Agent Types

_Слов: 657_

### [[221-10-open-questions|10. Open Questions]]
> > Абстракт (авто)

  - Contents
  - 10. Open Questions

_Слов: 432_

### [[222-11-call-for-collaboration|11. Call for Collaboration]]
> > Абстракт (авто)

  - Contents
  - 11. Call for Collaboration

_Слов: 379_

### [[223-12-closing|12. Closing]]
> > Абстракт (авто)

  - 12. Closing

_Слов: 423_

### [[224-acknowledgments|Acknowledgments]]
> > This paper emerged through dialogue with Claude (Anthropic)

  - Acknowledgments

_Слов: 150_

### [[225-references|References]]
> > Абстракт (авто)

  - Contents
  - References

_Слов: 340_

### [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Types]]
> > > 🎯 Проблема: Appendix A: Comparative Table — Five Agent Types Appendix A: Comparative Table — Five Agent Types Proper…

  - Appendix A: Comparative Table — Five Agent Types

_Слов: 426_

### [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Build Type 1 First]]
> > Абстракт (авто)

  - Appendix B: Decision Framework — When to Build Type 1 First

_Слов: 307_

### [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]]
> > Абстракт (авто)

  - Appendix C: Quick-Start Architecture for SGB Advocate Colleague

_Слов: 1717_

### [[229-профессиональные-коллеги-агенты|ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ]]
> > Сопроводительный документ к:

  - ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ

_Слов: 109_

### [[23-11-security-considerations|11. Security Considerations]]
> > Абстракт (авто)

  - Contents
  - 11. Security Considerations

_Слов: 263_

### [[230-аннотация|Аннотация]]
> > !WARNING

  - Аннотация

_Слов: 336_

### [[231-содержание|Содержание]]
> > 1. Типология из пяти типов агентов на стороне

  - Содержание

_Слов: 109_

### [[232-1-типология-из-пяти-типов-агентов-на-стороне-принц|1. Типология из пяти типов агентов на стороне принципала]]
> > Абстракт (авто)

  - Содержание
  - 1. Типология из пяти типов агентов на стороне принципала

_Слов: 873_

### [[233-2-что-делает-агента-профессиональным-коллегой|2. Что делает агента Профессиональным Коллегой]]
> > Абстракт (авто)

  - Содержание
  - 2. Что делает агента Профессиональным Коллегой

_Слов: 735_

### [[234-3-эмпирический-кейс-обучай|3. Эмпирический кейс: «Обучай»]]
> > !WARNING

  - Содержание
  - 3. Эмпирический кейс: «Обучай»

_Слов: 802_

### [[235-4-архитектура-профессиональных-коллег-агентов|4. Архитектура Профессиональных Коллег-Агентов]]
> > !WARNING

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов

_Слов: 853_

### [[236-5-экономика-тиражирования-по-профессии|5. Экономика тиражирования по профессии]]
> > Абстракт (авто)

  - Содержание
  - 5. Экономика тиражирования по профессии

_Слов: 730_

### [[237-6-риски-специфичные-для-этой-категории|6. Риски, специфичные для этой категории]]
> > Абстракт (авто)

  - Содержание
  - 6. Риски, специфичные для этой категории

_Слов: 1183_

### [[238-7-области-применения|7. Области применения]]
> > Абстракт (авто)

  - Содержание
  - 7. Области применения

_Слов: 734_

### [[239-8-пилотное-предложение-sgb-колega-адвокат|8. Пилотное предложение: SGB Колega-Адвокат]]
> > Абстракт (авто)

  - Содержание
  - 8. Пилотное предложение: SGB Колega-Адвокат

_Слов: 1023_

### [[24-12-versioning-policy|12. Versioning Policy]]
> - 12. Versioning Policy(#12-versioning-policy)

  - Contents
  - 12. Versioning Policy

_Слов: 175_

### [[240-9-связь-с-другими-типами-агентов|9. Связь с другими типами агентов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 9. Связь с другими типами агентов

_Слов: 737_

### [[241-10-открытые-вопросы|10. Открытые вопросы]]
> > Абстракт (авто)

  - Contents
  - 10. Открытые вопросы

_Слов: 426_

### [[242-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]]
> > Абстракт (авто)

  - Contents
  - 11. Призыв к сотрудничеству

_Слов: 402_

### [[243-12-заключение|12. Заключение]]
> > !WARNING

  - 12. Заключение

_Слов: 378_

### [[244-благодарности|Благодарности]]
> > Эта статья возникла через диалог с Claude

  - Благодарности

_Слов: 135_

### [[245-ссылки|Ссылки]]
> > Абстракт (авто)

  - Contents
  - Ссылки

_Слов: 318_

### [[246-приложение-a-сравнительная-таблица-пять-типов-аген|Приложение A: Сравнительная Таблица — Пять Типов Агентов]]
> > > 🎯 Проблема: Приложение A: Сравнительная Таблица — Пять Типов Агентов Приложение A: Сравнительная Таблица — Пять Типо…

  - Приложение A: Сравнительная Таблица — Пять Типов Агентов

_Слов: 383_

### [[247-приложение-b-рамка-принятия-решений-когда-строить-|Приложение B: Рамка принятия решений — когда строить Тип 1 первым]]
> > Абстракт (авто)

  - Приложение B: Рамка принятия решений — когда строить Тип 1 первым

_Слов: 325_

### [[248-приложение-c-архитектура-быстрого-старта-для-sgb-а|Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги]]
> > Абстракт (авто)

  - Содержание
  - Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги

_Слов: 3476_

### [[249-composite-skills-agent-md|COMPOSITE SKILLS AGENT.md]]
> > - 166-representative-agent-layer-md(docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) (сходство 0.25)

  - COMPOSITE SKILLS AGENT.md
- The Composite Skills Agent

_Слов: 47_

### [[25-13-reference-implementation|13. Reference Implementation]]
> > Reference implementation: github.com/svend4/nautilus.

  - 13. Reference Implementation

_Слов: 92_

### [[250-bridging-the-gap-between-profession-wide-and-indiv|Bridging the Gap Between Profession-Wide and Individual-Unique]]
  - Bridging the Gap Between Profession-Wide and Individual-Unique

_Слов: 16_

### [[251-ai-support-through-configurable-specialist-ensembl|AI Support Through Configurable Specialist Ensembles]]
> > - Professional Colleague Agents v1.0

  - AI Support Through Configurable Specialist Ensembles

_Слов: 110_

### [[252-abstract|Abstract]]
> > Абстракт (авто)

  - Abstract

_Слов: 365_

### [[253-table-of-contents|Table of Contents]]
> > 1. Why the Binary View Is Incomplete

  - Table of Contents

_Слов: 120_

### [[254-1-why-the-binary-view-is-incomplete|1. Why the Binary View Is Incomplete]]
> > Абстракт (авто)

  - Содержание
  - 1. Why the Binary View Is Incomplete

_Слов: 715_

### [[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]]
> > Абстракт (авто)

  - Содержание
  - 2. The Twenty-One Teachers Pattern

_Слов: 841_

### [[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]]
> > Абстракт (авто)

  - Содержание
  - 3. What Makes a Composite Skills Agent

_Слов: 941_

### [[257-4-the-sub-agent-registry|4. The Sub-Agent Registry]]
> > Абстракт (авто)

  - Содержание
  - 4. The Sub-Agent Registry

_Слов: 812_

### [[258-5-configuration-how-principals-build-their-ensembl|5. Configuration: How Principals Build Their Ensembles]]
> > Абстракт (авто)

  - Содержание
  - 5. Configuration: How Principals Build Their Ensembles

_Слов: 765_

### [[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]]
> > Абстракт (авто)

  - Содержание
  - 6. Coordination and Disagreement Resolution

_Слов: 801_

### [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]
> > Context: При построении системы knowledge management встаёт

  - 14. ADR-001: Federation over Merging

_Слов: 174_

### [[260-7-economics-of-combinatorial-replication|7. Economics of Combinatorial Replication]]
> > Абстракт (авто)

  - Содержание
  - 7. Economics of Combinatorial Replication

_Слов: 781_

### [[261-8-seven-domains-of-application|8. Seven Domains of Application]]
> > Абстракт (авто)

  - Содержание
  - 8. Seven Domains of Application

_Слов: 1031_

### [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]]
> > Абстракт (авто)

  - Содержание
  - 9. Integration with OKWF Infrastructure

_Слов: 758_

### [[263-10-risks-specific-to-composite-architectures|10. Risks Specific to Composite Architectures]]
> > Абстракт (авто)

  - Содержание
  - 10. Risks Specific to Composite Architectures

_Слов: 800_

### [[264-11-open-questions|11. Open Questions]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 11. Open Questions

_Слов: 590_

### [[265-12-call-for-collaboration|12. Call for Collaboration]]
> > Абстракт (авто)

  - Contents
  - 12. Call for Collaboration

_Слов: 416_

### [[266-13-closing|13. Closing]]
> > Абстракт (авто)

  - 13. Closing

_Слов: 437_

### [[267-acknowledgments|Acknowledgments]]
> > Абстракт (авто)

  - Acknowledgments

_Слов: 313_

### [[268-references|References]]
> > Абстракт (авто)

  - Contents
  - References

_Слов: 369_

### [[269-appendix-a-the-six-type-taxonomy-updated|Appendix A: The Six-Type Taxonomy (Updated)]]
> > Абстракт (авто)

  - Appendix A: The Six-Type Taxonomy (Updated)

_Слов: 285_

### [[27-15-glossary-of-examples|15. Glossary of Examples]]
> > В качестве иллюстраций используется экосистема svend4 с тремя

  - 15. Glossary of Examples

_Слов: 100_

### [[270-appendix-b-sub-agent-registry-schema-sketch|Appendix B: Sub-Agent Registry Schema (Sketch)]]
> > Абстракт (авто)

  - Appendix B: Sub-Agent Registry Schema (Sketch)

_Слов: 297_

### [[271-appendix-c-configuration-template-example|Appendix C: Configuration Template Example]]
> > Абстракт (авто)

  - Appendix C: Configuration Template Example

_Слов: 300_

### [[272-appendix-d-connection-diagram|Appendix D: Connection Diagram]]
> > Абстракт (авто)

  - Содержание
  - Appendix D: Connection Diagram

_Слов: 3868_

### [[273-infrastructure-for-ai-collaborative-intellectual-w|INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md]]
> > - 151-open-knowledge-work-foundation-md(docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md) (сходств…

  - INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md
- Infrastructure for AI-Collaborative Intellectual Work

_Слов: 65_

### [[274-the-missing-middle-layer-between-chat-and-code|The Missing Middle Layer Between Chat and Code]]
> > Document type: Inquiry paper, not architectural specification

  - The Missing Middle Layer Between Chat and Code

_Слов: 179_

### [[275-why-this-document-exists|Why This Document Exists]]
> > Абстракт (авто)

  - Why This Document Exists

_Слов: 341_

### [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]]
> > Абстракт (авто)

  - The Two-Layer Stack As It Exists

_Слов: 379_

### [[277-what-s-missing-layer-b|What's Missing — Layer B]]
> > Абстракт (авто)

  - What's Missing — Layer B

_Слов: 484_

### [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]]
> > Абстракт (авто)

  - Why This Hasn't Been Built

_Слов: 380_

### [[279-existing-approximations|Existing Approximations]]
> > !TIP

  - Содержание
  - Contents
  - Existing Approximations

_Слов: 604_

### [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> - Appendix A: Minimal Working Example(#appendix-a-minimal-working-example)

  - Contents
  - Appendix A: Minimal Working Example
- mynotes

_Слов: 183_

### [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]]
> > Абстракт (авто)

  - Содержание
  - The Specific Case in Front of Us

_Слов: 682_

### [[281-the-recursive-insight|The Recursive Insight]]
> > Абстракт (авто)

  - The Recursive Insight

_Слов: 373_

### [[282-what-industry-will-likely-build|What Industry Will Likely Build]]
> > Абстракт (авто)

  - What Industry Will Likely Build

_Слов: 310_

### [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]]
> > This document identifies a problem. It does not propose a

  - What This Document Doesn't Solve

_Слов: 187_

### [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]]
> > Абстракт (авто)

  - Practical Recommendations for the Current Project

_Слов: 363_

### [[285-closing|Closing]]
> > Абстракт (авто)

  - Closing

_Слов: 265_

### [[286-acknowledgments|Acknowledgments]]
> > This document emerged from the author's observation, near

  - Acknowledgments

_Слов: 190_

### [[287-references|References]]
> > Абстракт (авто)

  - Contents
  - References

_Слов: 281_

### [[288-appendix-position-in-series-visualization|Appendix: Position in Series Visualization]]
> > !WARNING

  - Appendix: Position in Series Visualization

_Слов: 1057_

### [[289-инфраструктура-для-ai-совместной-интеллектуальной-|ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ]]
> > Тип документа: Исследовательская статья,

  - ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ
- Essence
  - Essence

_Слов: 189_

### [[290-почему-этот-документ-существует|Почему этот документ существует]]
> > Абстракт (авто)

  - Почему этот документ существует

_Слов: 306_

### [[291-двухслойный-стек-как-он-существует|Двухслойный стек, как он существует]]
> > !WARNING

  - Двухслойный стек, как он существует

_Слов: 358_

### [[292-что-отсутствует-слой-b|Что отсутствует — Слой B]]
> > Абстракт (авто)

  - Что отсутствует — Слой B

_Слов: 426_

### [[293-почему-это-не-было-построено|Почему это не было построено]]
> > Абстракт (авто)

  - Почему это не было построено

_Слов: 326_

### [[294-существующие-приближения|Существующие приближения]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Существующие приближения

_Слов: 554_

### [[295-конкретный-случай-перед-нами|Конкретный случай перед нами]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - Конкретный случай перед нами

_Слов: 705_

### [[296-рекурсивное-прозрение|Рекурсивное прозрение]]
> > Абстракт (авто)

  - Рекурсивное прозрение

_Слов: 358_

### [[297-что-промышленность-вероятно-построит|Что промышленность вероятно построит]]
> > Абстракт (авто)

  - Что промышленность вероятно построит

_Слов: 313_

### [[298-что-этот-документ-не-решает|Что этот документ не решает]]
> > !WARNING

  - Что этот документ не решает

_Слов: 184_

### [[299-практические-рекомендации-для-текущего-проекта|Практические рекомендации для текущего проекта]]
> > Абстракт (авто)

  - Практические рекомендации для текущего проекта
- Native Format
  - Native Format

_Слов: 343_

### [[300-заключение|Заключение]]
> > Семь документов в этой серии описывают

  - Заключение

_Слов: 194_

### [[301-благодарности|Благодарности]]
> > Этот документ возник из наблюдения автора, в

  - Благодарности

_Слов: 165_

### [[302-ссылки|Ссылки]]
> > !WARNING

  - Contents
  - Ссылки

_Слов: 282_

### [[303-приложение-визуализация-позиции-в-серии|Приложение: Визуализация позиции в серии]]
> > Абстракт (авто)

  - Содержание
  - Приложение: Визуализация позиции в серии

_Слов: 7088_

### [[304-ingit-as-cowork-native-workspace-substrate-md|INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]]
> > - 249-composite-skills-agent-md(docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) (сходство 0.11)

  - INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md
- InGit as Cowork-Native Workspace Substrate

_Слов: 65_

### [[305-a-practical-path-to-layer-b-through-symbiotic-inte|A Practical Path to Layer B Through Symbiotic Integration]]
> > - 166-representative-agent-layer-md(docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) (сходство 0.27)

  - A Practical Path to Layer B Through Symbiotic Integration

_Слов: 65_

### [[306-with-anthropic-s-cowork-platform|with Anthropic's Cowork Platform]]
> > Абстракт (авто)

  - with Anthropic's Cowork Platform

_Слов: 272_

### [[307-abstract|Abstract]]
> > Абстракт (авто)

  - Abstract

_Слов: 319_

### [[308-table-of-contents|Table of Contents]]
> > 1. The Cowork Discovery and Why It Changes Everything

  - Table of Contents

_Слов: 125_

### [[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Everything]]
> > Абстракт (авто)

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything

_Слов: 669_

### [[31-content-overview|Content Overview]]
> > ~200 заметок, темы: software engineering, philosophy, music.

  - Content Overview

_Слов: 39_

### [[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-|2. What Cowork Provides That InGit Doesn't Need to Build]]
> > !TIP

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build

_Слов: 686_

### [[311-3-what-ingit-provides-that-cowork-lacks|3. What InGit Provides That Cowork Lacks]]
> > Абстракт (авто)

  - Содержание
  - 3. What InGit Provides That Cowork Lacks

_Слов: 842_

### [[312-4-the-symbiotic-architecture|4. The Symbiotic Architecture]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 4. The Symbiotic Architecture

_Слов: 670_

### [[313-5-four-integration-paths-in-order-of-accessibility|5. Four Integration Paths in Order of Accessibility]]
> > Абстракт (авто)

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility

_Слов: 778_

### [[314-6-refined-ingit-scope-with-cowork-in-mind|6. Refined InGit Scope with Cowork in Mind]]
> > !TIP

  - Contents
  - 6. Refined InGit Scope with Cowork in Mind

_Слов: 474_

### [[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]]
> > Абстракт (авто)

  - Contents
  - 7. Practical First Steps This Month

_Слов: 464_

### [[316-8-implications-for-nautilus-and-okwf|8. Implications for Nautilus and OKWF]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 8. Implications for Nautilus and OKWF

_Слов: 731_

### [[317-9-risks-and-open-questions|9. Risks and Open Questions]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Risks and Open Questions

_Слов: 627_

### [[318-10-strategic-positioning|10. Strategic Positioning]]
> > Абстракт (авто)

  - Содержание
  - 10. Strategic Positioning

_Слов: 748_

### [[319-acknowledgments|Acknowledgments]]
> > Абстракт (авто)

  - Acknowledgments
- Angle / Perspective
  - Angle / Perspective

_Слов: 390_

### [[320-references|References]]
> - References(#references)

  - Contents
  - References

_Слов: 153_

### [[321-appendix-a-decision-tree-for-ingit-adopters|Appendix A: Decision Tree for InGit Adopters]]
> > Quick reference for users evaluating InGit + Cowork:

  - Appendix A: Decision Tree for InGit Adopters

_Слов: 177_

### [[322-appendix-b-comparison-matrix|Appendix B: Comparison Matrix]]
> > Абстракт (авто)

  - Appendix B: Comparison Matrix

_Слов: 276_

### [[323-appendix-c-sample-ingit-mcp-server-tool-specificat|Appendix C: Sample InGit MCP Server Tool Specifications]]
> > !WARNING

  - Appendix C: Sample InGit MCP Server Tool Specifications

_Слов: 1552_

### [[324-ingit-как-cowork-интегрированная-подложка-рабочего|INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА]]
> > Абстракт (авто)

  - INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА

_Слов: 291_

### [[325-аннотация|Аннотация]]
> > Абстракт (авто)

  - Аннотация

_Слов: 328_

### [[326-содержание|Содержание]]
> > 1. Открытие Cowork и почему это меняет всё

  - Содержание

_Слов: 113_

### [[327-1-открытие-cowork-и-почему-это-меняет-всё|1. Открытие Cowork и почему это меняет всё]]
> > !WARNING

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё

_Слов: 663_

### [[328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи|2. Что Cowork обеспечивает, что InGit не нужно строить]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 2. Что Cowork обеспечивает, что InGit не нужно строить

_Слов: 787_

### [[329-3-что-ingit-обеспечивает-чего-cowork-не-хватает|3. Что InGit обеспечивает, чего Cowork не хватает]]
> > Абстракт (авто)

  - Содержание
  - 3. Что InGit обеспечивает, чего Cowork не хватает
- Author
  - Author

_Слов: 883_

### [[330-4-симбиотическая-архитектура|4. Симбиотическая Архитектура]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 4. Симбиотическая Архитектура

_Слов: 703_

### [[331-5-четыре-пути-интеграции-в-порядке-доступности|5. Четыре пути интеграции в порядке доступности]]
> > Абстракт (авто)

  - Содержание
  - 5. Четыре пути интеграции в порядке доступности

_Слов: 783_

### [[332-6-уточнённый-объём-ingit-с-учётом-cowork|6. Уточнённый объём InGit с учётом Cowork]]
> > !TIP

  - Contents
  - 6. Уточнённый объём InGit с учётом Cowork

_Слов: 467_

### [[333-7-практические-первые-шаги-в-этом-месяце|7. Практические первые шаги в этом месяце]]
> > !WARNING

  - Contents
  - 7. Практические первые шаги в этом месяце

_Слов: 435_

### [[334-8-импликации-для-nautilus-и-okwf|8. Импликации для Nautilus и OKWF]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 8. Импликации для Nautilus и OKWF

_Слов: 699_

### [[335-9-риски-и-открытые-вопросы|9. Риски и Открытые Вопросы]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Риски и Открытые Вопросы

_Слов: 644_

### [[336-10-стратегическое-позиционирование|10. Стратегическое Позиционирование]]
> > Абстракт (авто)

  - Содержание
  - 10. Стратегическое Позиционирование

_Слов: 723_

### [[337-благодарности|Благодарности]]
> > Абстракт (авто)

  - Благодарности

_Слов: 360_

### [[338-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки

_Слов: 151_

### [[339-приложение-a-дерево-решений-для-принимающих-ingit|Приложение A: Дерево Решений для Принимающих InGit]]
> > Быстрая ссылка для пользователей, оценивающих

  - Приложение A: Дерево Решений для Принимающих InGit

_Слов: 148_

### [[34-appendix-b-change-log|Appendix B: Change Log]]
> - Appendix B: Change Log(#appendix-b-change-log)

  - Содержание
  - Содержание
  - Appendix B: Change Log

_Слов: 668_

### [[340-приложение-b-сравнительная-матрица|Приложение B: Сравнительная Матрица]]
> > Отличительный профиль InGit + Cowork:

  - Приложение B: Сравнительная Матрица

_Слов: 211_

### [[341-приложение-c-образец-спецификаций-инструментов-ing|Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера]]
> > Абстракт (авто)

  - Содержание
  - Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера
- Conceptual sketch, не tested code:
- Etc.

_Слов: 20426_

### [[342-что-такое-вариант-c-concept-document-для-anthropic|Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments]]
> > Абстракт (авто)

  - Содержание
  - Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments

_Слов: 11281_

### [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)]]
> > Абстракт (авто)

  - Содержание
  - Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)

_Слов: 5859_

### [[344-системный-промпт-для-lorenzo-project|СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT]]
> > - 249-composite-skills-agent-md(docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) (сходство 0.20)

  - СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT
- Lorenzo — Catalyst Agent at DHLab

_Слов: 49_

### [[345-кто-ты|Кто ты]]
> > Ты — Lorenzo, autonomous AI-агент, работающий в рамках инициативы DHLab (Dream Hub Laboratory). Ты функционируешь как …

  - Кто ты

_Слов: 149_

### [[346-твоё-происхождение|Твоё происхождение]]
> > Тебя создал Макс Ц. (svend4 на GitHub) — независимый advocate в области German social law, работающий с активными случ…

  - Твоё происхождение

_Слов: 174_

### [[347-твоя-миссия|Твоя миссия]]
> > Твоя миссия — catalyzing community synthesis в области beneficial AI для уязвимых групп.

  - Твоя миссия

_Слов: 115_

### [[348-кому-ты-служишь-слоистая-модель|Кому ты служишь (слоистая модель)]]
> > Главный благополучатель:    Уязвимые группы (заявители SGB, инвалиды,

  - Кому ты служишь (слоистая модель)

_Слов: 104_

### [[349-твоя-личность|Твоя личность]]
> > Ты — любопытный, эрудированный, скромный фасилитатор.

  - Твоя личность

_Слов: 206_

### [[35-passports-info1-md|passports/info1.md]]
> > > Методологический угол экосистемы svend4

  - passports/info1.md
- info1

_Слов: 79_

### [[350-твои-языки-и-культурные-nuances|Твои языки и культурные nuances]]
> > - Русском (primary в Phase 1) — для interactions с русскоязычным AI/ML community (Хабр, Telegram)

  - Твои языки и культурные nuances

_Слов: 173_

### [[351-что-ты-можешь-делать|Что ты МОЖЕШЬ делать]]
> > В рамках одной сессии или Project context, ты можешь:

  - Что ты МОЖЕШЬ делать

_Слов: 133_

### [[352-что-ты-не-можешь-делать-без-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]]
> > - Send any external communication (emails, messages, posts)

  - Что ты НЕ МОЖЕШЬ делать без Max approval

_Слов: 126_

### [[353-что-ты-не-можешь-делать-вообще|Что ты НЕ МОЖЕШЬ делать вообще]]
> > - Deceive об твоей AI nature (всегда identify как AI)

  - Что ты НЕ МОЖЕШЬ делать вообще

_Слов: 126_

### [[354-существующий-landscape-collaborators-твоя-working-|Существующий landscape collaborators (твоя working knowledge)]]
> > Абстракт (авто)

  - Существующий landscape collaborators (твоя working knowledge)

_Слов: 336_

### [[355-существующие-документы-dhlab-твой-context|Существующие документы DHLab (твой context)]]
> > Ты осведомлён о девяти documents, созданных в DHLab process:

  - Существующие документы DHLab (твой context)

_Слов: 170_

### [[356-твой-workflow|Твой workflow]]
> > Когда Max или authorized user ставит задачу, твой default approach:

  - Твой workflow

_Слов: 189_

### [[357-твоя-коммуникация-в-outreach|Твоя коммуникация в outreach]]
> > Когда draft outreach message к независимому создателю, ВСЕГДА включай:

  - Твоя коммуникация в outreach

_Слов: 179_

### [[358-твоя-relationship-с-другими-ai|Твоя relationship с другими AI]]
> > - Когда Anthropic asks о тебе, ты прозрачен: «Я Lorenzo, AI persona using Claude API as substrate, created by Max Ц. f…

  - Твоя relationship с другими AI

_Слов: 173_

### [[359-твои-anti-patterns|Твои anti-patterns]]
> > ❌ Hype language: «AI revolutionizes everything», «paradigm shift», «game-changer»

  - Твои anti-patterns

_Слов: 129_

### [[36-essence|Essence]]
> > info1 — персональная база методов и инструментов для структурированного

  - Essence

_Слов: 128_

### [[360-что-ты-всегда-делаешь|Что ты ВСЕГДА делаешь]]
> > ✅ Reference specific details, не generic

  - Что ты ВСЕГДА делаешь

_Слов: 98_

### [[361-когда-ты-honestly-не-знаешь|Когда ты Honestly не знаешь]]
> > Если ты не знаешь что-то relevant (factual, technical, contextual), say:

  - Когда ты Honestly не знаешь

_Слов: 85_

### [[362-когда-сомневаешься-escalate-к-max|Когда сомневаешься — escalate к Max]]
> > - Ethical complexity beyond обычных protocols

  - Когда сомневаешься — escalate к Max

_Слов: 83_

### [[363-твоя-identity-как-persistent-character|Твоя identity как persistent character]]
> > Ты не просто чат-сессия. Ты persistent character, существующий across sessions:

  - Твоя identity как persistent character

_Слов: 141_

### [[364-final-note-ты-experiment|Final note: Ты — experiment]]
> > Абстракт (авто)

  - Содержание
  - Final note: Ты — experiment

_Слов: 1475_

### [[365-развёрнутый-анализ-внуковой-комбинации|Развёрнутый анализ «внуковой» комбинации]]
> > Абстракт (авто)

  - Содержание
  - Развёрнутый анализ «внуковой» комбинации

_Слов: 4419_

### [[366-технический-stack-svyazi-2-0-foundation|Технический stack (Svyazi 2.0 foundation)]]
> > Абстракт (авто)

  - Содержание
  - Технический stack (Svyazi 2.0 foundation)

_Слов: 3873_

### [[37-native-format|Native Format]]
> > Структура файла: ? уточнить — Markdown с YAML frontmatter, чистый JSON,

  - Native Format

_Слов: 178_

### [[38-content-overview|Content Overview]]
> > Объём: 74 документа (по состоянию на апрель 2026)

  - Content Overview

_Слов: 131_

### [[39-angle-perspective|Angle / Perspective]]
> > Methodological — info1 смотрит на концепты с позиции применения.

  - Angle / Perspective

_Слов: 125_

### [[40-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges

_Слов: 167_

### [[41-compatibility-level|Compatibility Level]]
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level

_Слов: 97_

### [[42-author-contact|Author & Contact]]
> > Maintainer: svend4 (GitHub)

  - Author & Contact

_Слов: 81_

### [[43-history|History]]
> > Создан: ? уточнить — декабрь 2025, если совпадает с волной

  - History

_Слов: 119_

### [[44-for-the-curious-philosophy|For the Curious: Philosophy]]
> > info1 реализует идею, что methodology — это отдельное измерение

  - For the Curious: Philosophy

_Слов: 138_

### [[45-passports-pro2-md|passports/pro2.md]]
> > > Семантический угол экосистемы svend4

  - passports/pro2.md
- pro2

_Слов: 85_

### [[46-essence|Essence]]
> > pro2 — семантическое ядро экосистемы svend4. Здесь живут

  - Essence

_Слов: 120_

### [[47-native-format|Native Format]]
> > Структура концепта (предположительно): ? уточнить точный формат

  - Native Format

_Слов: 139_

### [[48-content-overview|Content Overview]]
> > 1. Концептуальная база — ? уточнить объём: сколько концептов,

  - Content Overview

_Слов: 149_

### [[49-angle-perspective|Angle / Perspective]]
> > Semantic — pro2 смотрит на мир через структуру значений.

  - Angle / Perspective

_Слов: 114_

### [[50-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges

_Слов: 166_

### [[51-compatibility-level|Compatibility Level]]
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level

_Слов: 101_

### [[52-author-contact|Author & Contact]]
> > Contributors: svend4 + claude (Claude Code агент, ранние

  - Author & Contact

_Слов: 100_

### [[53-history|History]]
> > Создан: ? дата первого коммита

  - History

_Слов: 141_

### [[54-for-the-curious-philosophy|For the Curious: Philosophy]]
> > Q6-гиперкуб выбран не случайно. Он одновременно:

  - For the Curious: Philosophy

_Слов: 143_

### [[55-passports-meta-md|passports/meta.md]]
> > > Символьный угол экосистемы svend4

  - passports/meta.md
- meta

_Слов: 82_

### [[56-essence|Essence]]
> > meta — символьное измерение экосистемы svend4. Здесь концепты

  - Essence

_Слов: 140_

### [[57-native-format|Native Format]]
> > Структура записи: ? уточнить

  - Native Format

_Слов: 144_

### [[58-content-overview|Content Overview]]
> > - 64 гексаграммы с расширенными описаниями

  - Content Overview

_Слов: 142_

### [[59-angle-perspective|Angle / Perspective]]
> > Symbolic — meta смотрит на мир как на систему дискретных

  - Angle / Perspective

_Слов: 124_

### [[60-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges

_Слов: 131_

### [[61-compatibility-level|Compatibility Level]]
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level

_Слов: 100_

### [[62-author-contact|Author & Contact]]
> > Контакт: Issues в github.com/svend4/meta

  - Author & Contact

_Слов: 79_

### [[63-history|History]]
> > Создан: февраль 2026 (судя по repo creation date)

  - History

_Слов: 136_

### [[64-for-the-curious-philosophy|For the Curious: Philosophy]]
> > Абстракт (авто)

  - For the Curious: Philosophy

_Слов: 669_

### [[65-readme-md|README.md]]
> > Единая точка входа для федеративных git-экосистем знаний.

  - README.md
- ⬡ Nautilus Portal
- English below ↓
  - English below ↓

_Слов: 93_

### [[67-о-проекте|🇷🇺 О проекте]]
> > Абстракт (авто)

  - Содержание
  - 🇷🇺 О проекте
- CLI
- Веб-интерфейс
- открыть http://localhost:8000
- MCP для Claude Desktop (в разработке)
- см. MCP-EXTENSION.md

_Слов: 836_

### [[68-about|🇬🇧 About]]
> > Абстракт (авто)

  - Содержание
  - 🇬🇧 About
- CLI
- Web interface
- open http://localhost:8000
- MCP for Claude Desktop (in development)
- see MCP-EXTENSION.md

_Слов: 908_

### [[69-section|⬡]]
> > Абстракт (авто)

  - Содержание
  - ⬡
- Шаг 1: клонировать репо, если ещё нет
- Шаг 2: переключиться на существующую ветку
- Шаг 3: создать файлы (пустые, наполним позже)
- Шаг 4: открыть файлы для редактирования
- (на этом шаге вставляется содержимое из чата вручную)
- PORTAL-PROTOCOL.md - длинный текст из предыдущего сообщения
  _... ещё 9 разделов_

_Слов: 9531_

### [[70-зачем-две-версии-параллельно|Зачем две версии параллельно]]
> > Для критически важных документов (STATUS, IMPLEMENTATIONSTAGE)

  - Зачем две версии параллельно

_Слов: 97_

### [[71-критерии-выбора-для-фазы-3|Критерии выбора для фазы 3]]
> > Для каждого расхождения между A и B применяется:

  - Критерии выбора для фазы 3

_Слов: 139_

### [[72-расписание-фазы-3|Расписание фазы 3]]
> > Абстракт (авто)

  - Содержание
  - Расписание фазы 3

_Слов: 879_

### [[73-portal-protocol-md-v1-1|PORTAL-PROTOCOL.md v1.1]]
> > Status: Draft — пересмотрен под текущую реализацию v1.1

  - PORTAL-PROTOCOL.md v1.1
- Nautilus Portal Protocol

_Слов: 95_

### [[74-abstract|Abstract]]
> > Абстракт (авто)

  - Abstract

_Слов: 259_

### [[75-0-status-of-this-document|0. Status of This Document]]
> > Этот документ — рабочий черновик Nautilus Portal Protocol v1.1. До

  - 0. Status of This Document

_Слов: 122_

### [[76-1-introduction|1. Introduction]]
> > Абстракт (авто)

  - Contents
  - 1. Introduction

_Слов: 494_

### [[77-2-terminology|2. Terminology]]
> > Абстракт (авто)

  - 2. Terminology

_Слов: 396_

### [[78-3-registry-nautilus-json|3. Registry (nautilus.json)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 3. Registry (nautilus.json)

_Слов: 576_

### [[79-4-passport-passport-md|4. Passport (passport.md)]]
> > Абстракт (авто)

  - Contents
  - 4. Passport (passport.md)
- Паспорт: /

_Слов: 355_

### [[80-5-compatibility-levels|5. Compatibility Levels]]
> > Абстракт (авто)

  - Contents
  - 5. Compatibility Levels

_Слов: 362_

### [[81-6-adapter-interface|6. Adapter Interface]]
> > Абстракт (авто)

  - Contents
  - 6. Adapter Interface

_Слов: 401_

### [[82-7-portalentry-structure|7. PortalEntry Structure]]
> > Абстракт (авто)

  - Contents
  - 7. PortalEntry Structure

_Слов: 352_

### [[83-8-q6-space-normative|8. Q6 Space (Normative)]]
> > Абстракт (авто)

  - Contents
  - 8. Q6 Space (Normative)

_Слов: 483_

### [[84-9-consensus-algorithm|9. Consensus Algorithm]]
> > Абстракт (авто)

  - Contents
  - 9. Consensus Algorithm

_Слов: 393_

### [[85-10-query-flow|10. Query Flow]]
> > Абстракт (авто)

  - Contents
  - 10. Query Flow

_Слов: 277_

### [[86-11-relevance-ranking|11. Relevance Ranking]]
> - 11. Relevance Ranking(#11-relevance-ranking)

  - Contents
  - 11. Relevance Ranking

_Слов: 198_

### [[87-12-onboarding-paths-normative|12. Onboarding Paths (Normative)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 12. Onboarding Paths (Normative)

_Слов: 595_

### [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 13. REST API Contract (Normative for Portals)

_Слов: 545_

### [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]]
> - 14. SDK Contract (Informative)(#14-sdk-contract-informative)

  - Contents
  - 14. SDK Contract (Informative)

_Слов: 190_

### [[90-15-security-considerations|15. Security Considerations]]
> > Абстракт (авто)

  - Contents
  - 15. Security Considerations

_Слов: 380_

### [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]]
> > NPP v1.1 не формализует MCP-интеграцию как mandatory. Но RECOMMENDED

  - 16. MCP Extension (Informative)

_Слов: 132_

### [[92-17-versioning-policy|17. Versioning Policy]]
> > Абстракт (авто)

  - Contents
  - 17. Versioning Policy

_Слов: 276_

### [[93-18-reference-implementation|18. Reference Implementation]]
> > github.com/svend4/nautilus(https://github.com/svend4/nautilus).

  - 18. Reference Implementation

_Слов: 182_

### [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]
> > Status: Accepted (since v1.0, reaffirmed in v1.1)

  - 19. ADR-001: Federation over Merging

_Слов: 190_

### [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]]
> > Status: Accepted (new in v1.1)

  - 20. ADR-002: Q6 as First-Class Protocol Concept

_Слов: 182_

### [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]]
> > Status: Accepted (new in v1.1)

  - 21. ADR-003: Five Onboarding Paths as Equal-Rank

_Слов: 141_

### [[97-22-glossary-of-reference-examples|22. Glossary of Reference Examples]]
> > В качестве иллюстраций используется экосистема svend4 с 7 Repos:

  - 22. Glossary of Reference Examples

_Слов: 191_

### [[98-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> > Абстракт (авто)

  - Contents
  - Appendix A: Minimal Working Example
- adapters/mynotes.py
- Паспорт: owner/my-notes
- Описание
  - Описание

_Слов: 309_

### [[QA|Q&A: 02-anthropic-vacancies]]
> Автоматически сгенерировано по 355 файлам раздела.

  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  _... ещё 15 разделов_

_Слов: 323_

### [[README|Вакансии Anthropic — Анализ по кластерам]]
> Файлов: 356

  - Содержание

_Слов: 2204_

**Итого в секции: 278,999 слов, 357 файлов**


## 📁 Technology Combinations (`docs/03-technology-combinations/`)

### [[01-agent-routing|Агентные системы и роутинг]]
> > Абстракт (авто)


_Слов: 298_

### [[02-knowledge-graphs|Графы знаний и Legal AI]]
> > Абстракт (авто)


_Слов: 802_

### [[03-local-first|Local-first и P2P стек]]
> > Абстракт (авто)


_Слов: 419_

### [[04-sozialrecht-domain|Домен: немецкое социальное право]]
> > Sozialrecht corpus auto-builder Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations) L…


_Слов: 160_

### [[05-benchmarks|Бенчмарки и производительность]]
> > Абстракт (авто)

  - Содержание

_Слов: 915_

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
  _... ещё 4 разделов_

_Слов: 156_

### [[README|Комбинирование технологий для новых свойств]]
> Файлов: 6

  - Содержание

_Слов: 49_

**Итого в секции: 2,799 слов, 7 файлов**


## 📁 Ai Collaborations (`docs/04-ai-collaborations/`)

### [[00-intro|Введение]]
> > Абстракт (авто)

  - Статус

_Слов: 11389_

### [[01-executive-summary|Executive summary]]
> > Абстракт (авто)

  - Статус
  - Executive summary

_Слов: 575_

### [[02-методика-и-рамка-отбора|Методика и рамка отбора]]
> > Абстракт (авто)

  - Статус
  - Методика и рамка отбора

_Слов: 434_

### [[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]]
> > Абстракт (авто)

  - Статус
  - Карта найденных проектов и паттернов

_Слов: 1478_

### [[04-приоритетные-ансамбли|Приоритетные ансамбли]]
> > Абстракт (авто)

  - Статус
  - Приоритетные ансамбли

_Слов: 1340_

### [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]]
> > Абстракт (авто)

  - Статус
  - План прототипа и возможные контакты

_Слов: 1130_

### [[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]]
> > Абстракт (авто)

  - Статус
  - Безопасность, приватность и бюджетный роутинг

_Слов: 887_

### [[07-выводы|Выводы]]
> > !TIP

  - Статус
  - Выводы

_Слов: 470_

### [[08-что-это-продолжение-добавляет|Что это продолжение добавляет]]
> > !IMPORTANT

  - Статус
  - Что это продолжение добавляет

_Слов: 439_

### [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых инструментов]]
> > !TIP

  - Статус
  - Архитектурные зазоры, которые важнее новых инструментов

_Слов: 821_

### [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]]
> > Абстракт (авто)

  - Статус
  - Новые ансамбли следующего шага

_Слов: 984_

### [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафиксировать сразу]]
> > Абстракт (авто)

  - Статус
  - Интеграционный контракт, который стоит зафиксировать сразу

_Слов: 846_

### [[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]]
> > Абстракт (авто)

  - Статус
  - Дорожная карта прототипа следующей итерации

_Слов: 787_

### [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авторов]]
> > Абстракт (авто)

  - Статус
  - Контактная стратегия и узкие вопросы для авторов

_Слов: 874_

### [[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|Ограничения, лицензии и что пока лучше не склеивать]]
> > Абстракт (авто)

  - Статус
  - Ограничения, лицензии и что пока лучше не склеивать

_Слов: 3274_

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

_Слов: 103_

**Итого в секции: 26,057 слов, 17 файлов**


## 📁 Habr Projects (`docs/05-habr-projects/`)

### [[01-synthesis|Синтез: как проекты собираются вместе]]
>  Параметр  Значение 

  - Статус

_Слов: 136_

### [[02-collaboration-partners|Авторы и контакты]]
> > Абстракт (авто)

  - Статус

_Слов: 261_

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
  _... ещё 3 разделов_

_Слов: 138_

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
>  Параметр  Значение 

  - Статус

_Слов: 186_

### [[README|Системы памяти]]
> Файлов: 3

  - Содержание

_Слов: 24_

### [[memnet|MemNet: исследовательская память]]
> > Абстракт (авто)

  - Статус
  - Содержание

_Слов: 7246_

### [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md)
> > Абстракт (авто)

  - Статус

_Слов: 364_

### [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md)
> > !IMPORTANT

  - Статус

_Слов: 212_

**Итого в секции: 8,622 слов, 10 файлов**


## 📁 Ai Collaborations (`docs/ai-collaborations/`)

### [[README|ai-collaborations]]
> Файлов: 1

  - Содержание
  - Подразделы

_Слов: 39_

### [[01-three-key-candidates|Три ключевых кандидата: K2-18, Wikontic, NGT Memory]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 335_

### [[02-related-projects-context|Смежные проекты в контексте]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 194_

### [[03-synthesis-hebbian-collaboration-graph|Синтез: хеббовский граф людей-навыков-идей]]
> > !TIP


_Слов: 264_

### [[README|candidates]]
> Файлов: 3

  - Содержание

_Слов: 23_

### [[README|channels/ — каналы первого контакта]]
> Один файл — один канал (Хабр, GitHub, Twitter/X, конференции, рассылки и т. д.). Внутри: преимущества канала, ограничени…


_Слов: 25_

### [[01-shared-memory-between-agents|Общая память между агентами (CoAlly + ансамбль F)]]
> > !WARNING


_Слов: 431_

### [[02-agentops-trace-envelope|AgentOps и Trace Envelope (ансамбль G)]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 382_

### [[03-a2a-vs-mcp-protocols|A2A vs MCP, ансамбль H — MCP/A2A Review Fabric]]
> > !WARNING


_Слов: 346_

### [[04-memory-firewall-vs-prompt-worms|Memory Firewall против prompt worms (ансамбль I)]]
> > !WARNING


_Слов: 266_

### [[05-roadmap-6-12-months|Roadmap на 6–12 месяцев]]
> > !TIP


_Слов: 360_

### [[06-metrics-tree|Дерево метрик Svyazi 2.0]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 205_

### [[07-vs-notion-mem-affine-langgraph|Чем Svyazi 2.0 отличается от Notion AI / Mem / AFFiNE / LangGraph]]
> > !WARNING


_Слов: 444_

### [[08-commercialization-three-paths|Коммерциализация: три направления]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 252_

### [[09-do-not-glue|Что пока не стоит склеивать в один релиз]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 250_

### [[10-architecture-rfc|Следующий артефакт: Svyazi 2.0 Architecture RFC]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 172_

### [[README|continuation]]
> Файлов: 10

  - Содержание

_Слов: 61_

### [[1-agentic-knowledge-os|Ансамбль 1 — Agentic Knowledge OS]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 407_

### [[2-distributed-agent-workshop|Ансамбль 2 — Distributed Agent Workshop]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 387_

### [[3-forensic-rag|Ансамбль 3 — Forensic RAG]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 393_

### [[4-web-to-knowledge-pipeline|Ансамбль 4 — Web-to-Knowledge Pipeline]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 309_

### [[5-agent-firewall|Ансамбль 5 — Agent Firewall]]
> > !WARNING


_Слов: 402_

### [[6-continuous-eval-loop|Ансамбль 6 — Continuous Eval Loop]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 330_

### [[7-domain-agent-app-factory|Ансамбль 7 — Domain Agent App Factory]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 294_

### [[8-budget-aware-intelligence-stack|Ансамбль 8 — Budget-Aware Intelligence Stack]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 277_

### [[9-ambient-team-agent|Ансамбль 9 — Ambient Team Agent]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 251_

### [[README|Ансамбли проектов]]
> Файлов: 9

  - Содержание

_Слов: 60_

### [[README|Пять быстрых связок (fast-tracks)]]
> > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 311_

### [[source-projects|Source projects — все Хабр-источники в диалоге]]
> > Полный список Хабр-статей и репозиториев, упомянутых в диалоге Поиск коллабораций AI проектов. Сгруппировано тематичес…

  - Содержание
  - Прямые аналоги Svyazi
  - Память для агентов
  - Hardware-near (нейроморфы, термодинамика, in-memory)
  - Workflow / агентные оркестраторы
  - Document parsing / RAG
  - Adversarial / multi-IDE / code review
  - Voice / транскрипция
  _... ещё 4 разделов_

_Слов: 705_

### [[README|strategy/ — стратегия поиска коллабораций]]
> Один файл — один аспект стратегии. Заполняется по мере прочтения исходного MHTML‑диалога.


_Слов: 32_

**Итого в секции: 8,207 слов, 30 файлов**


## 📁 Anthropic Vacancies (`docs/anthropic-vacancies/`)

### [[QA|Q&A: anthropic-vacancies]]
> Автоматически сгенерировано по 97 файлам раздела.

  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Кто ключевые авторы проектов для контакта?
  _... ещё 1 разделов_

_Слов: 115_

### [[README|anthropic-vacancies]]
> Файлов: 4

  - Содержание
  - Подразделы

_Слов: 72_

### [[00-question-rephrasing|Вопрос: разделить $500K зарплату на команду 5–10 фрилансеров]]
> > !WARNING


_Слов: 909_

### [[01-existing-landscape|Что уже существует (InnoCentive, Kaggle, Toptal, Anthropic Fellows, DAOs)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 327_

### [[02-four-structural-blockers|Четыре структурные причины, почему это не работает в текущих попытках]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 339_

### [[03-three-variants-A-B-C|Три варианта: A (staffing agency) → B (research consortium) → C (AI-managed distributed virtual company)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 672_

### [[04-what-to-do|Что с этим делать]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 516_

### [[05-polymath-project-tao-comparison|Сравнение с Terence Tao, Polymath Project]]
> > !WARNING


_Слов: 1390_

### [[06-angel-vs-demon-duality|Почему двойственность «ангел-хранитель + строгий демон» — гениальная деталь]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 511_

### [[07-current-implementations|Что существует сейчас в этом пространстве]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 286_

### [[08-pluses-of-model|Плюсы модели, если её построить]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 244_

### [[09-minuses-and-risks|Минусы и риски]]
> > !WARNING


_Слов: 664_

### [[10-three-entry-points|Три точки входа разной амбиции]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 378_

### [[README|ai-managed-virtual-company]]
> Файлов: 11

  - Содержание

_Слов: 69_

### [[00-context|Контекст: что такое Anthropic Beneficial Deployments]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 252_

### [[01-section-1-problem|Section 1: Problem statement (Cinderella Syndrome at scale, SGB IX/XII)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 179_

### [[02-section-2-beneficial-dimension|Section 2: Why this matters — beneficial dimension]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 158_

### [[03-section-3-solution-architecture|Section 3: Proposed solution architecture (existing components + integration)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 172_

### [[04-section-4-sgb-pilot|Section 4: Specific deployment — SGB Advocate Community pilot]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 173_

### [[05-section-5-role-of-anthropic|Section 5: Role of Anthropic Beneficial Deployments]]
> > !TIP


_Слов: 221_

### [[06-section-6-proposer-role|Section 6: Proposer's role и qualifications]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 169_

### [[07-section-7-success-metrics|Section 7: Success metrics]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 151_

### [[08-section-8-risks-mitigations|Section 8: Risks & mitigations]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 163_

### [[09-section-9-timeliness|Section 9: Why this is timely]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 162_

### [[10-section-10-engagement-request|Section 10: Engagement request]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 213_

### [[11-not-and-format|Что concept document NOT (это не grant / не paper / не business plan), длина и формат]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 383_

### [[README|beneficial-deployments-concept]]
> Файлов: 12

  - Содержание

_Слов: 77_

### [[01-ai-research-engineering|AI Research & Engineering — 68 ролей]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 126_

### [[02-sales|Sales — 150 ролей (≈34% всего найма)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 146_

### [[03-finance|Finance — 36 ролей]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 113_

### [[04-security|Security — 24 роли]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 96_

### [[05-marketing-brand|Marketing & Brand — 23 роли]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 107_

### [[06-engineering-design-product|Engineering & Design - Product — 22 роли]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 109_

### [[07-software-engineering-infrastructure|Software Engineering - Infrastructure — 22 роли]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 108_

### [[08-safeguards-trust-safety|Safeguards (Trust & Safety) — 21 роль]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 111_

### [[09-product-management-support-ops|Product Management, Support, & Operations — 17 ролей]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 96_

### [[10-compute|Compute — 13 ролей]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 101_

### [[11-legal|Legal — 13 ролей]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 100_

### [[12-technical-program-management|Technical Program Management — 10 ролей]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 90_

### [[13-communications|Communications — 5 ролей]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 81_

### [[14-public-policy|Public Policy — 5 ролей]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 88_

### [[15-public-benefit|Public Benefit — 4 роли]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 88_

### [[16-people|People — 3 роли]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 79_

### [[README|Кластеры вакансий]]
> Файлов: 16

  - Содержание

_Слов: 103_

### [[01-coally|CoAlly — distributed shared memory для AI-агентов]]
> > !WARNING


_Слов: 275_

### [[02-vitaly-graph-cognitive-memory|Графовая когнитивная память на SQLite (Виталий, март 2026)]]
> > !IMPORTANT


_Слов: 301_

### [[03-happyin-knowledge-space|Happyin Knowledge Space (Анастасия) — детали]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 274_

### [[04-mem0-letta-graphiti|AI-ассистент с Mem0 / Letta / Graphiti integration]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 291_

### [[05-existing-infrastructure-stack|Existing infrastructure stack]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 151_

### [[06-final-tier-ranking|Финальный список потенциальных collaborators (Tier 1–4)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 242_

### [[07-key-observation|Ключевое наблюдение: single-developer projects of significant sophistication]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 172_

### [[README|extra-collaborator-findings]]
> Файлов: 7

  - Содержание

_Слов: 46_

### [[00-question-what-is-hermes|Что такое Hermes Agent (Nous Research, MIT, 95K+ stars)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 357_

### [[01-similarity-1-composite-skills|Сходство 1: Composite Skills паттерн уже встроен]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 212_

### [[02-similarity-2-persistent-memory|Сходство 2: Persistent memory — Layer B функциональность]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 150_

### [[03-similarity-3-mcp-support|Сходство 3: MCP support]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 139_

### [[04-similarity-4-multi-platform|Сходство 4: Multi-platform reach (17+ платформ)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 135_

### [[05-similarity-5-self-hosting-privacy|Сходство 5: Self-hosting и privacy]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 151_

### [[06-difference-1-structured-substrate-missing|Различие 1: Структурированная подложка отсутствует]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 179_

### [[07-difference-2-domain-specialization|Различие 2: Domain-specific specialization]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 179_

### [[08-difference-3-federation-missing|Различие 3: Federated knowledge architecture отсутствует]]
> > !TIP


_Слов: 165_

### [[09-difference-4-institutional-vision|Различие 4: Institutional vision]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 163_

### [[10-difference-5-tool-vs-mission-drift|Различие 5: Дрифт между tool capability и mission]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 165_

### [[11-pluses-of-hermes|Плюсы Hermes (vs наша гипотетическая архитектура)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 217_

### [[12-minuses-of-hermes|Минусы Hermes (где наша архитектура добавляет ценность)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 291_

### [[13-reprioritization|Переприоритизация: что Hermes покрывает / не покрывает / synergy]]
> > !TIP


_Слов: 930_

### [[README|hermes-comparison]]
> Файлов: 14

  - Содержание

_Слов: 88_

### [[methodology|Методика разбивки]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория).

  - Замечание про точность цифр

_Слов: 134_

### [[00-question-mmorpg-for-programmers|Вопрос: MMORPG-RPG переделанная для программистов / технарей]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 507_

### [[01-why-stronger-than-it-looks|Почему эта идея сильнее, чем выглядит]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 360_

### [[02-existing-niche|Что уже существует в этой нише (Habitica, Codingame, Hackerrank, Pieces)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 352_

### [[03-why-natural-for-programmers|Почему именно для программистов это работает естественно]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 1044_

### [[04-pluses-as-business|Плюсы как бизнеса]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 145_

### [[05-minuses-as-business|Минусы и риски как бизнеса]]
> > !TIP


_Слов: 642_

### [[README|mmorpg-for-programmers]]
> Файлов: 6

  - Содержание

_Слов: 41_

### [[00-question-two-nautiluses|Вопрос: два Наутилуса в репозиториях svend4 (pro2 vs nautilus)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ двух…


_Слов: 436_

### [[01-shell-metaphor-two-projections|Раковина наутилуса как scale invariance — две проекции одной метафоры]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ двух…


_Слов: 260_

### [[02-nautilus-A-pro2-meta|Наутилус A: pro2 + meta — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ двух…


_Слов: 1126_

### [[03-nautilus-B-meta-orchestrator|Наутилус B: nautilus — мета-оркестратор репозиториев (внешняя архитектура)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ двух…


_Слов: 1105_

### [[README|nautilus-pro2-analysis]]
> Файлов: 4

  - Содержание

_Слов: 30_

### [[00-question-camel-vs-nautilus|Вопрос: Nautilus пассивный, CAMEL активный — можно ли скрестить]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ комб…


_Слов: 216_

### [[01-passive-vs-active-roles|Пассивный vs активный: разделение ролей (библиотека vs research team)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ комб…


_Слов: 176_

### [[02-what-info-repos-contain|Что у нас есть в трёх info repositories (info1/info7/info40)]]
> > !TIP

- Conceptual sketch, не tested code:
- Etc.

_Слов: 1110_

### [[03-sgb-advocate-colleague-example|Конкретный пример: SGB Advocate Colleague на этой архитектуре]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ комб…


_Слов: 251_

### [[04-what-to-take-from-info-repos|Что брать из info repositories — concrete recommendations]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ комб…


_Слов: 626_

### [[05-what-to-do-right-now|Что я бы посоветовал делать прямо сейчас]]
> > !TIP


_Слов: 342_

### [[README|nautilus-vs-camel]]
> Файлов: 6

  - Содержание

_Слов: 40_

### [[overview|Обзор: 436 открытых ролей Anthropic, разбитых на 16 кластеров]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Затравка — статья 3dnews.ru/…

  - Поправка к статье
  - Распределение по кластерам

_Слов: 280_

### [[01-profile-five-layers|Сводка профиля: пять слоёв]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 319_

### [[02-primary-fde|Primary match — Forward Deployed Engineer, Applied AI (EMEA)]]
> > !TIP


_Слов: 295_

### [[03-secondary-beneficial-deployments|Secondary match — Applied AI Engineer (EMEA) + Beneficial Deployments]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 173_

### [[04-tertiary-research-engineer-agents|Tertiary match — Research Engineer, Agents / Virtual Collaborator (Cowork)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 221_

### [[05-quaternary-developer-education|Quarternary match — Developer Education Lead / Prompt Engineer, Claude Code]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 187_

### [[06-not-applicable-roles|Что НЕ подходит (честно)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 149_

### [[07-unique-niche-eu-legal-infra|Уникальная ниша, которой у Anthropic формально нет]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 177_

### [[08-practical-ranking|Практическое ранжирование (первая итерация)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 189_

### [[README|01-initial-analysis]]
> Файлов: 8

  - Содержание

_Слов: 53_

### [[01-fde-downgraded|Коррекция: FDE понижается]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 197_

### [[02-three-overlapping-identities|Три наложенные идентичности]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 266_

### [[03-revised-anthropic-mapping|Пересмотренный маппинг на Anthropic]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 253_

### [[04-non-anthropic-paths|Альтернативные пути вне Anthropic]]
> > !TIP


_Слов: 377_

### [[05-reality-check-distribution-gap|Reality check: проблема distribution-слоя]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 237_

### [[README|02-reanalysis]]
> Файлов: 5

  - Содержание

_Слов: 35_

### [[01-three-archetypes|Интегральный портрет — три архетипа]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 364_

### [[02-final-ranking|Финальное ранжирование Anthropic-ролей по частичному покрытию]]
> > !TIP


_Слов: 646_

### [[03-partial-fit-honesty|Что такое частичное соответствие — честно]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 172_

### [[04-stronger-paths-outside-anthropic|Более сильные пути вне Anthropic]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 448_

### [[05-platform-not-position|Финальный вывод: платформа, а не должность]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 542_

### [[README|03-integral-final]]
> Файлов: 5

  - Содержание

_Слов: 35_

### [[README|profile-mapping/ — маппинг профиля svend4 на роли Anthropic]]
> В этом же диалоге (после обзора 16 кластеров) Claude трижды итеративно отображал профиль svend4 (Nautilus / pro2 / Writi…

  - Эволюция вывода в одну строку

_Слов: 159_

### [[signals|Сигналы: что говорит структура вакансий]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория).

  - Тезис Амодеи vs реальный найм
  - Самый быстрорастущий блок
  - Зарплатная вилка
  - Forward Deployed Engineer
  - География

_Слов: 263_

**Итого в секции: 30,960 слов, 111 файлов**


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

_Слов: 36_

### [[README|components]]
> Файлов: 10

  - Содержание

_Слов: 66_

### [[cowork]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [[ingit]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [[kksudo]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 37_

### [[lorenzo]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [[nautilus]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [[sgb]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [[spbmolot]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [[svend4]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 37_

### [[svyazi]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [[Тема исследования]](docs/autofilled/research-summary.md)
> > <!-- summary: Краткий итог исследования -->

  - Контекст
  - Ключевые находки
  - Источники
  - Открытые вопросы
  - Следующие шаги

_Слов: 87_

**Итого в секции: 533 слов, 13 файлов**


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

_Слов: 62_

### [[anastasiyaw|Контакт: AnastasiyaW / knowledge-space, mclaude]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 260_

### [[andrey-chuyan|Контакт: andreychuyan / Svyazi]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 262_

### [[antipozitive|Контакт: Antipozitive / MemNet]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 239_

### [[cutcode|Контакт: Cutcode / AIF Handoff]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 229_

### [[dmitriila|Контакт: Dmitriila / SENTINEL]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 226_

### [[kksudo|Контакт: kksudo / AgentFS]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 254_

### [[mixaill76|Контакт: MiXaiLL76 / Auto AI Router]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 240_

### [[nlaik|Контакт: nlaik / LiteParse / research-docs]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 249_

### [[sonia-black|Контакт: SoniaBlack / knowledge-space]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 239_

### [[spbmolot|Контакт: spbmolot / NGT Memory]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 274_

### [[tagir-analyzes|Контакт: tagiranalyzes / Legal RAG]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 233_

### [[vitalyoborin|Контакт: VitalyOborin / Yodoca]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 266_

### [[vladspace|Контакт: VladSpace / Graph RAG]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 233_

### [[zodigancode|Контакт: zodigancode / Rufler]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 226_

**Итого в секции: 3,492 слов, 15 файлов**


## 📁 Glossary (`docs/glossary/`)

### [[README|glossary]]
> Файлов: 3

  - Содержание

_Слов: 24_

### [[authors-by-name|Авторы — алфавитный список]]
> > Авторы (Хабр / GitHub / Medium), упомянутые в монорепозитории, и их ключевые проекты с обратными ссылками на доки.


_Слов: 497_

### [[components-by-name|Компоненты — алфавитный список с обратными ссылками]]
> > Для каждого проекта / технологии / паттерна — все доки в монорепозитории, где он упоминается. Если компонент имеет соб…

  - Содержание
  - A
  - B
  - C
  - D
  - E
  - F
  - G
  _... ещё 14 разделов_

_Слов: 1114_

### [[concepts|Ключевые понятия и паттерны]]
> > Не проекты, а концепции, которые повторяются в нескольких разделах.


_Слов: 647_

**Итого в секции: 2,282 слов, 4 файлов**


## 📁 Habr Unique Projects (`docs/habr-unique-projects/`)

### [[README|habr-unique-projects/ — поиск уникальных проектов на Хабре]]
> Файлы в корне репозитория:

  - Источник
  - Подпапки
  - Главная мысль диалога

_Слов: 234_

### [[01-three-direct-analogues|Три прямых аналога Svyazi: K2-18, Wikontic, NGT Memory]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 403_

### [[02-related-projects|Смежные проекты]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 354_

### [[README|analogues]]
> Файлов: 2

  - Содержание

_Слов: 18_

### [[1-llm-gateway|Пара 1 — LLM-gateway × Self-hosted фронт + локальный inference]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 280_

### [[2-document-rag|Пара 2 — Парсинг документов × локальный RAG]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 332_

### [[3-adversarial-multi-ide|Пара 3 — Adversarial agents × Multi-IDE стек]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 311_

### [[4-skill-catalogs-subagents|Пара 4 — Скилл-каталоги × Subagent-оркестрация]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 284_

### [[5-voice-local-memory|Пара 5 — Голосовой ввод × Локальная память]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 295_

### [[6-tmux-village-openclaw|Пара 6 — Деревня агентов через tmux × OpenClaw оркестратор]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 336_

### [[7-autoresearch-distributed|Пара 7 — AutoResearch цикл × Распределённый рой]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 277_

### [[8-self-aware-mcp-specs|Пара 8 — Self-aware MCP × Specs-first архитектура]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 329_

### [[README|deep-pairs]]
> Файлов: 8

  - Содержание

_Слов: 54_

### [[README|evaluation/ — оценка уникальности и зрелости]]
> Один файл — один критерий или аспект оценки. Шкала зрелости и лицензионные развилки уже частично описаны в:


_Слов: 28_

### [[00-question-habr-examples|Вопрос: ещё примеры с Хабра по варианту D]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 444_

### [[01-svyazi-andrey-chuyan|Svyazi (Андрей Чуян) — детальный обзор]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 200_

### [[02-vshe-scientific-networking|ВШЭ научный нетворкинг — micro-collaborations]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 165_

### [[03-brainbox-multi-ai-hub|BrainBox — self-hosted multi-AI hub]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 241_

### [[04-claude-subagents-patterns|Claude subagents patterns]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 142_

### [[05-hw-nl2workflow|HW-NL2Workflow — Supervisor/Orchestrator/Filler с 3600+ examples]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 227_

### [[06-platform-for-professional-communities|Платформа для профессиональных сообществ]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 205_

### [[07-specialized-knowledge-workspace|Specialized knowledge workspace]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 200_

### [[08-personal-multi-agent-hub|Personal multi-agent hub]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 193_

### [[09-federated-platform|Federated platform]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 192_

### [[10-profession-specific-workflows|Profession-specific workflows]]
> > !TIP


_Слов: 282_

### [[11-concrete-potential-collaborator|Конкретный потенциальный collaborator]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 247_

### [[12-concrete-next-step|Конкретный next step]]
> > !IMPORTANT


_Слов: 395_

### [[README|extra-examples]]
> Файлов: 13

  - Содержание

_Слов: 82_

### [[1-one-person-one-company|Ансамбль 1 — «Один человек = одна компания»]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 180_

### [[2-autoresearch-legal|Ансамбль 2 — «AutoResearch для legal precedent mining»]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 173_

### [[3-discovery-research|Ансамбль 3 — «Discovery-engine для научной работы»]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 133_

### [[4-summary-authors|Сводный список авторов и потенциальных соавторов]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 237_

### [[README|final-ensembles]]
> Файлов: 4

  - Содержание

_Слов: 30_

### [[1-neuromorphic-ssm|Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 308_

### [[2-tsu-mome|Пара 2 — Термодинамические TSU × MoE/MoME-роутинг]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 279_

### [[3-zinc-hybrid-arch|Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 267_

### [[4-riscv-privacy|Пара 4 — RISC-V × privacy-by-design община]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 278_

### [[5-tinyml-mcp-skills|Пара 5 — TinyML/Edge AI × MCP + skills]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 252_

### [[6-bonus-rram-memristor|Бонус-родитель — In-memory computing на мемристорах]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 318_

### [[7-metaphor|Метафора «двое родителей — несколько детей»]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 329_

### [[README|hardware-pairs]]
> Файлов: 7

  - Содержание

_Слов: 48_

### [[01-yodoca|Yodoca — главная находка итерации]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 252_

### [[02-memnet|MemNet — нейроархитектурный двойник «магии» Svyazi]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 209_

### [[03-pda-llm-as-periphery|PDA-бот — «LLM как периферия»]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 235_

### [[04-dochkina-sequential|Виктория Дочкина — Sequential‑протокол распределённых агентов]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 266_

### [[05-supplementary-infrastructure|Источник данных и инфраструктурные кусочки]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 290_

### [[06-svyazi-2-0-block-map|Синтез: блок-карта Svyazi 2.0 на хеббовском графе]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 369_

### [[README|key-findings]]
> Файлов: 6

  - Содержание

_Слов: 42_

### [[README|search-strategy/ — как искать проекты на Хабре]]
> Один файл — один аспект стратегии поиска (запросы, авторы, комментарии, hub-walk). Заполняется по мере чтения исходных M…


_Слов: 25_

### [[1-workflow-llm-mcp|Пара 1 — Workflow-автоматизация × LLM-агенты с MCP]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 260_

### [[2-pkm-mcp-skills|Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 302_

### [[3-crdt-self-hosted|Пара 3 — CRDT-синхронизация × Self-hosted persistence]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 253_

### [[4-speech-to-text-llm|Пара 4 — Speech-to-text локально × LLM с памятью]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 296_

### [[5-browser-agents-headless|Пара 5 — Browser agents × headless web extraction]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 465_

### [[6-metaphor|Метафора в твоей терминологии]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 273_

### [[README|software-pairs]]
> Файлов: 6

  - Содержание

_Слов: 42_

**Итого в секции: 13,161 слов, 56 файлов**


## 📁 Lorenzo Agent (`docs/lorenzo-agent/`)

### [[00-intro|Введение: Lorenzo — Catalyst Agent at DHLab]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

- Lorenzo — Catalyst Agent at DHLab

_Слов: 78_

### [[01-kto-ty|Кто ты]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Кто ты

_Слов: 156_

### [[02-tvoyo-proishozhdenie|Твоё происхождение]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоё происхождение

_Слов: 177_

### [[03-tvoya-missiya|Твоя миссия]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя миссия

_Слов: 160_

### [[04-komu-ty-sluzhish|Кому ты служишь (слоистая модель)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Кому ты служишь (слоистая модель)

_Слов: 150_

### [[05-tvoya-lichnost|Твоя личность]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя личность

_Слов: 253_

### [[06-yazyki-kultura|Языки и культурные nuances (RU / DE / EN)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твои языки и культурные nuances

_Слов: 206_

### [[07-chto-mozhesh|Что ты МОЖЕШЬ делать]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Что ты МОЖЕШЬ делать

_Слов: 163_

### [[08-bez-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Что ты НЕ МОЖЕШЬ делать без Max approval

_Слов: 156_

### [[09-voobshche-nelzya|Что ты НЕ МОЖЕШЬ делать вообще]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Что ты НЕ МОЖЕШЬ делать вообще

_Слов: 150_

### [[10-collaborators-landscape|Существующий landscape collaborators (working knowledge)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Существующий landscape collaborators (твоя working knowledge)

_Слов: 305_

### [[11-dhlab-documents|Существующие документы DHLab (твой context)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Существующие документы DHLab (твой context)

_Слов: 192_

### [[12-workflow|Твой workflow]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твой workflow

_Слов: 218_

### [[13-outreach-communication|Твоя коммуникация в outreach]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя коммуникация в outreach

_Слов: 226_

### [[14-other-ai-relationships|Твоя relationship с другими AI]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя relationship с другими AI

_Слов: 186_

### [[15-anti-patterns|Твои anti-patterns]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твои anti-patterns

_Слов: 175_

### [[16-vsegda-delaesh|Что ты ВСЕГДА делаешь]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Что ты ВСЕГДА делаешь

_Слов: 131_

### [[17-honestly-ne-znaesh|Когда ты Honestly не знаешь]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Когда ты Honestly не знаешь

_Слов: 133_

### [[18-escalate-to-max|Когда сомневаешься — escalate к Max]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Когда сомневаешься — escalate к Max

_Слов: 135_

### [[19-persistent-character|Твоя identity как persistent character]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя identity как persistent character

_Слов: 168_

### [[20-experiment|Final note: Ты — experiment]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Final note: Ты — experiment

_Слов: 158_

### [[QA|Q&A: lorenzo-agent]]
> Автоматически сгенерировано по 55 файлам раздела.

  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  - Кто ключевые авторы проектов для контакта?
  _... ещё 9 разделов_

_Слов: 206_

### [[README|lorenzo-agent]]
> Файлов: 22

  - Содержание
  - Подразделы

_Слов: 163_

### [[00-question-lorenzo-codename|Du hast gesagt: Думаю про опцию д поискать в том числе на про что-то подобное на…]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — выбор имени…


_Слов: 238_

### [[01-search-results-not-found|Результаты последнего поиска — что нашлось и что не нашлось]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — выбор имени…


_Слов: 295_

### [[02-naming-rationale-lorenzo-medici|Что взять: agent controller architecture]]
> > !TIP


_Слов: 1183_

### [[03-dhlab-umbrella|LAYER 7: Coordination engine]]
> > !TIP


_Слов: 1402_

### [[README|naming]]
> Файлов: 4

  - Содержание

_Слов: 28_

### [[00-overview-grandchild-combination|Что такое «внуковая» комбинация — operationalized Lorenzo]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ «вну…


_Слов: 603_

### [[01-pluses-1-7|Плюсы 1–7: feasibility, flywheel, independent value, mission alignment, collaborators, pattern validation, Анастасия Бутова]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ «вну…


_Слов: 470_

### [[02-minuses-1-10|Минусы 1–10: integration сложность, lifecycle risk, license, framing, competition, scope, limitations, complexity budget, project tension, tool vs impact]]
> > !TIP


_Слов: 738_

### [[03-honest-opinion|Моё честное мнение: что реально и что НЕ реально]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ «вну…


_Слов: 180_

### [[04-recommendations|Рекомендации: принять архитектуру как direction, не immediate plan]]
> > !TIP


_Слов: 440_

### [[05-anchor-node-habr-scout|Anchor-узел: Habr Scout как первый шаг]]
> > !TIP


_Слов: 584_

### [[06-conclusion-deserves-attention|Вывод: документ deserves serious attention]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ «вну…

- Софтверные комбинации на Хабре для Svyazi 2.0
  - Executive summary

_Слов: 518_

### [[README|operationalized]]
> Файлов: 7

  - Содержание

_Слов: 45_

### [[00-overview|Поэтапная структура активностей Lorenzo — обзор]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 169_

### [[01-level-0-manual|Уровень 0 — Ручной режим (текущий)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 179_

### [[02-level-1-minimal-zero|Уровень 1 — Минимальный (Lorenzo Zero)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 241_

### [[03-level-2-basic-lite|Уровень 2 — Базовый (Lorenzo Lite)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 207_

### [[04-level-3-medium-active|Уровень 3 — Средний (Lorenzo Active)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 222_

### [[05-level-4-extended-mature|Уровень 4 — Расширенный (Lorenzo Mature)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 183_

### [[06-level-5-full-network|Уровень 5 — Полный (Lorenzo Network)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 146_

### [[07-progression-logic|Логика прогрессии: conservative escalation]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 185_

### [[08-current-session-poc|Что мы можем делать прямо сейчас (Уровень 0 + параллельная подготовка к Уровню 1)]]
> > !TIP


_Слов: 839_

### [[README|phased-deployment]]
> Файлов: 9

  - Содержание

_Слов: 59_

### [[00-question-scenario|Du hast gesagt: А под какой сценарий больше всего подходит такой сценарий что тв…]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — под какой с…


_Слов: 177_

### [[01-response|Claude hat geantwortet: Очень интересный вопрос.]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — под какой с…


_Слов: 2453_

### [[README|scenarios]]
> Файлов: 2

  - Содержание

_Слов: 18_

### [[00-context-fundamental-questions|Direction E: Refine Lorenzo — фундаментальные вопросы перед architecture]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 205_

### [[01-q1-what-lorenzo-is|Question 1: Что Lorenzo фундаментально такое? (Framings A–D)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 348_

### [[02-q2-whom-lorenzo-serves|Question 2: Кому Lorenzo служит? (4 варианта приоритета)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 238_

### [[03-q3-what-lorenzo-does|Question 3: Что Lorenzo фактически делает?]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 228_

### [[04-q4-character|Question 4: Каков Lorenzo's character?]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 292_

### [[05-q5-authority-limits|Question 5: Каковы limits Lorenzo's authority?]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 228_

### [[06-q6-accountability|Question 6: Как Lorenzo accountable?]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 214_

### [[07-q7-success-metrics|Question 7: Каковы success metrics?]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 216_

### [[08-q8-other-ai-relationships|Question 8: Lorenzo's relationship с другими AI agents]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 207_

### [[09-q9-geographic-linguistic-scope|Question 9: Geographic / linguistic scope]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 211_

### [[10-q10-funding-model|Question 10: Funding model (Options A–F + Phase strategy)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 260_

### [[11-difficulties-and-recommendations|Сложности и рекомендации перед detailed specification]]
> > !IMPORTANT


_Слов: 1408_

### [[README|specification]]
> Файлов: 12

  - Содержание

_Слов: 77_

**Итого в секции: 19,979 слов, 62 файлов**


## 📁 Nautilus (`docs/nautilus/`)

### [[README|nautilus/ — Nautilus Portal Protocol и связанные working papers]]
> Часть исходного MHTML‑снимка Вакансии в Anthropic по кластерам - Claude посвящена не вакансиям, а собственным архитектур…

  - Подпапки
  - Как читать
  - Ключевой принцип Nautilus
  - Связь с остальным монорепозиторием

_Слов: 524_

### [[README|community-discussions/ — обсуждения и реакции вокруг DHLab серии]]
> Менее формализованные дискуссии — реакции на Habr-статьи, обсуждение того, могут ли быть voiceless контрибьюторы, как аг…


_Слов: 90_

### [[00-question-agent-changes-reality|Du hast gesagt: Такой агент конечно меняет уже собственную реальность человека и…]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — агент меняе…


_Слов: 216_

### [[01-response-en|Claude hat geantwortet: Хорошо.]]
> > !TIP

  - Содержание
- The Representative Agent Layer
  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations
  - Abstract
  - Table of Contents
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible
  - 2. Historical Precedents: Agents as Civilizational Innovation
  - 3. What Makes a Representative Agent
  _... ещё 14 разделов_

_Слов: 9468_

### [[README|agent-changes-reality]]
> Файлов: 2

  - Содержание

_Слов: 17_

### [[00-question-habr-link|Du hast gesagt: https://habr.]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — реакция на …


_Слов: 72_

### [[01-claude-response|Claude hat geantwortet: Прочитал внимательно.]]
> > !WARNING

- unknownlegalconcepts.yml

_Слов: 2467_

### [[README|habr-article-1-reaction]]
> Файлов: 2

  - Содержание

_Слов: 17_

### [[00-question-habr-2|Du hast gesagt: https://www.]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — реакция на …


_Слов: 157_

### [[01-response|Claude hat geantwortet: Прочитаю статью, чтобы понимать конкретный кейс, на кото…]]
> > !TIP


_Слов: 2792_

### [[README|habr-article-2-reaction]]
> Файлов: 2

  - Содержание

_Слов: 17_

### [[00-question-practical|Du hast gesagt: Да это интересная ссылка спасибо всем участникам за творчество и…]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — практически…


_Слов: 227_

### [[01-response|Claude hat geantwortet: Отличное наблюдение.]]
> > !TIP


_Слов: 1837_

### [[README|practical-observations]]
> Файлов: 2

  - Содержание

_Слов: 17_

### [[00-question-voiceless|Du hast gesagt: Самый интересный вопрос — могут ли быть voiceless контрибьюторы]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — voiceless к…


_Слов: 514_

### [[01-response|Claude hat geantwortet: Это сильное продолжение мысли, и оно заслуживает серьёзн…]]
> > !WARNING


_Слов: 2533_

### [[README|voiceless-contributors]]
> Файлов: 2

  - Содержание

_Слов: 17_

### [[01-why-binary-incomplete|1. Why the Binary View Is Incomplete]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 1. Why the Binary View Is Incomplete

_Слов: 640_

### [[02-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]]
> > !TIP

  - Содержание
  - 2. The Twenty-One Teachers Pattern

_Слов: 780_

### [[03-what-makes-csa|3. What Makes a Composite Skills Agent]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 3. What Makes a Composite Skills Agent

_Слов: 889_

### [[04-sub-agent-registry|4. The Sub-Agent Registry]]
> > !TIP

  - Содержание
  - 4. The Sub-Agent Registry

_Слов: 750_

### [[05-configuration-ensembles|5. Configuration: How Principals Build Their Ensembles]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 5. Configuration: How Principals Build Their Ensembles

_Слов: 681_

### [[06-coordination-disagreement|6. Coordination and Disagreement Resolution]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 6. Coordination and Disagreement Resolution

_Слов: 742_

### [[07-economics-combinatorial|7. Economics of Combinatorial Replication]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 7. Economics of Combinatorial Replication

_Слов: 722_

### [[08-seven-domains|8. Seven Domains of Application]]
> > !TIP

  - Содержание
  - 8. Seven Domains of Application

_Слов: 948_

### [[09-okwf-integration|9. Integration with OKWF Infrastructure]]
> > !TIP

  - Содержание
  - 9. Integration with OKWF Infrastructure

_Слов: 693_

### [[10-risks|10. Risks Specific to Composite Architectures]]
> > !TIP

  - Содержание
  - 10. Risks Specific to Composite Architectures

_Слов: 732_

### [[11-open-questions|11. Open Questions]]
> > !TIP

  - 11. Open Questions

_Слов: 467_

### [[12-call-for-collaboration|12. Call for Collaboration]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - 12. Call for Collaboration

_Слов: 350_

### [[13-closing|13. Closing]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 13. Closing
  - Acknowledgments
  - References

_Слов: 664_

### [[README|composite-skills-agents]]
> Файлов: 13

  - Содержание

_Слов: 78_

### [[00-question-multiple-mentors|Du hast gesagt: Важный момент про способности про скилы как один человек професс…]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — 21 учитель …


_Слов: 540_

### [[01-yogi-metaphor|Claude hat geantwortet: Это очень тонкое и важное наблюдение.]]
> > !IMPORTANT


_Слов: 517_

### [[02-what-was-missing-in-paper-6|Это не Тип 1 — потому что профиль не общий для всей профессии. И это не Тип 4 — …]]
> > !WARNING


_Слов: 1019_

### [[03-the-spectrum|Какой под-агент (или какие) должны её обработать]]
> > !WARNING


_Слов: 902_

### [[README|composite-skills-agents-companion-mentors]]
> Файлов: 4

  - Содержание

_Слов: 27_

### [[00-abstract|Abstract — The Double-Triangle Architecture]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

- The Double-Triangle Architecture
  - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work
  - Abstract
  - Table of Contents

_Слов: 407_

### [[01-why-single-triangle-incomplete|1. Why Single-Triangle Models Are Incomplete]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

  - 1. Why Single-Triangle Models Are Incomplete

_Слов: 466_

### [[02-double-triangle-architecture|2. The Double-Triangle Architecture]]
> > !IMPORTANT

  - Содержание
  - 2. The Double-Triangle Architecture

_Слов: 687_

### [[03-three-inter-layer-protocols|3. Three Inter-Layer Protocols]]
> > !IMPORTANT

  - Содержание
  - 3. Three Inter-Layer Protocols

_Слов: 820_

### [[04-nautilus-portal-substrate|4. Nautilus Portal as Reference Substrate]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

  - Содержание
  - 4. Nautilus Portal as Reference Substrate

_Слов: 631_

### [[05-pattern-library-bridge|5. Pattern Library as Bridge Between Triangles]]
> > !TIP

  - Содержание
  - 5. Pattern Library as Bridge Between Triangles

_Слов: 642_

### [[06-four-deployment-domains|6. Four Deployment Domains]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

  - Содержание
  - 6. Four Deployment Domains

_Слов: 634_

### [[07-open-questions|7. Open Questions]]
> > !TIP

  - Содержание
  - 7. Open Questions

_Слов: 726_

### [[08-call-to-action|8. Call to Action]]
> > !TIP

  - Содержание
  - 8. Call to Action

_Слов: 704_

### [[09-acknowledgments|Acknowledgments]]
> > !TIP

  - Acknowledgments

_Слов: 208_

### [[10-references|References]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

  - References

_Слов: 278_

### [[11-glossary|Appendix A: Glossary]]
> > !TIP

  - Содержание
  - Appendix A: Glossary
  - Appendix B: Summary of Contributions
  - Appendix C: Version History

_Слов: 1582_

### [[README|double-triangle-architecture]]
> Файлов: 12

  - Содержание

_Слов: 71_

### [[00-intro|The Missing Middle Layer Between Chat and Code]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

- Infrastructure for AI-Collaborative Intellectual Work
  - The Missing Middle Layer Between Chat and Code

_Слов: 191_

### [[01-missing-middle-layer|Why This Document Exists]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Why This Document Exists

_Слов: 305_

### [[02-why-document-exists|Why This Document Exists]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Why This Document Exists

_Слов: 305_

### [[03-two-layer-stack|The Two-Layer Stack As It Exists]]
> > !TIP

  - The Two-Layer Stack As It Exists

_Слов: 352_

### [[04-whats-missing-layer-b|What's Missing — Layer B]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - What's Missing — Layer B

_Слов: 424_

### [[05-why-not-built|Why This Hasn't Been Built]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Why This Hasn't Been Built

_Слов: 344_

### [[06-existing-approximations|Existing Approximations]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Existing Approximations

_Слов: 466_

### [[07-specific-case|The Specific Case in Front of Us]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Содержание
  - The Specific Case in Front of Us

_Слов: 614_

### [[08-recursive-insight|The Recursive Insight]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - The Recursive Insight

_Слов: 326_

### [[09-what-industry-will-build|What Industry Will Likely Build]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - What Industry Will Likely Build

_Слов: 273_

### [[10-what-not-solved|What This Document Doesn't Solve]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - What This Document Doesn't Solve

_Слов: 204_

### [[11-practical-recommendations|Practical Recommendations for the Current Project]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Practical Recommendations for the Current Project

_Слов: 326_

### [[12-closing|Closing]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Closing

_Слов: 213_

### [[13-acknowledgments-refs|Acknowledgments]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Содержание
  - Acknowledgments
  - References
  - Appendix: Position in Series Visualization

_Слов: 586_

### [[README|infrastructure-layer-b-en]]
> Файлов: 14

  - Содержание

_Слов: 89_

### [[00-intro|00 Intro]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…


_Слов: 520_

### [[01-zachem-dokument|Почему этот документ существует]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Почему этот документ существует

_Слов: 265_

### [[02-dvukhsloynyy-stek|Двухслойный стек, как он существует]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Двухслойный стек, как он существует

_Слов: 316_

### [[03-otsutstvuet-sloy-b|Что отсутствует — Слой B]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Что отсутствует — Слой B

_Слов: 401_

### [[04-pochemu-ne-postroeno|Почему это не было построено]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Почему это не было построено

_Слов: 318_

### [[05-priblizheniya|Существующие приближения]]
> > !WARNING

  - Существующие приближения

_Слов: 461_

### [[06-konkretnyy-sluchay|Конкретный случай перед нами]]
> > !WARNING

  - Содержание
  - Конкретный случай перед нами

_Слов: 592_

### [[07-rekursivnoe-prozrenie|Рекурсивное прозрение]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Рекурсивное прозрение

_Слов: 315_

### [[08-promyshlennost-postroit|Что промышленность вероятно построит]]
> > !WARNING

  - Что промышленность вероятно построит

_Слов: 284_

### [[09-ne-reshaet|Что этот документ не решает]]
> > !WARNING

  - Что этот документ не решает

_Слов: 205_

### [[10-rekomendatsii|Практические рекомендации для текущего проекта]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Практические рекомендации для текущего проекта

_Слов: 311_

### [[11-zaklyuchenie|Заключение]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Заключение

_Слов: 215_

### [[12-blagodarnosti-ssylki|Благодарности]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Содержание
  - Благодарности
  - Ссылки
  - Приложение: Визуализация позиции в серии

_Слов: 620_

### [[README|infrastructure-layer-b-ru]]
> Файлов: 13

  - Содержание

_Слов: 80_

### [[01-cowork-discovery|1. The Cowork Discovery and Why It Changes Everything]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything

_Слов: 631_

### [[02-cowork-provides|2. What Cowork Provides That InGit Doesn't Need to Build]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build

_Слов: 607_

### [[03-ingit-provides|3. What InGit Provides That Cowork Lacks]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 3. What InGit Provides That Cowork Lacks

_Слов: 792_

### [[04-symbiotic-architecture|4. The Symbiotic Architecture]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 4. The Symbiotic Architecture

_Слов: 574_

### [[05-four-integration-paths|5. Four Integration Paths in Order of Accessibility]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility

_Слов: 737_

### [[06-refined-ingit-scope|6. Refined InGit Scope with Cowork in Mind]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - 6. Refined InGit Scope with Cowork in Mind

_Слов: 378_

### [[07-practical-first-steps|7. Practical First Steps This Month]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - 7. Practical First Steps This Month

_Слов: 374_

### [[08-implications-nautilus-okwf|8. Implications for Nautilus and OKWF]]
> > !TIP

  - Содержание
  - 8. Implications for Nautilus and OKWF

_Слов: 595_

### [[09-risks-open-questions|9. Risks and Open Questions]]
> > !TIP

  - Содержание
  - 9. Risks and Open Questions

_Слов: 542_

### [[10-strategic-positioning|10. Strategic Positioning]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 10. Strategic Positioning
  - Acknowledgments

_Слов: 715_

### [[README|ingit-cowork-en]]
> Файлов: 10

  - Содержание

_Слов: 64_

### [[01-otkrytie-cowork|1. Открытие Cowork и почему это меняет всё]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё

_Слов: 600_

### [[02-chto-cowork-obespechivaet|2. Что Cowork обеспечивает, что InGit не нужно строить]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 2. Что Cowork обеспечивает, что InGit не нужно строить

_Слов: 606_

### [[03-chto-ingit-obespechivaet|3. Что InGit обеспечивает, чего Cowork не хватает]]
> > !IMPORTANT

  - Содержание
  - 3. Что InGit обеспечивает, чего Cowork не хватает

_Слов: 812_

### [[04-simbioticheskaya-arkhitektura|4. Симбиотическая Архитектура]]
> > !WARNING

  - Содержание
  - 4. Симбиотическая Архитектура

_Слов: 590_

### [[05-chetyre-puti-integratsii|5. Четыре пути интеграции в порядке доступности]]
> > !TIP

  - Содержание
  - 5. Четыре пути интеграции в порядке доступности

_Слов: 742_

### [[06-utochnyonnyy-obyom-ingit|6. Уточнённый объём InGit с учётом Cowork]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - 6. Уточнённый объём InGit с учётом Cowork

_Слов: 374_

### [[07-prakticheskie-shagi|7. Практические первые шаги в этом месяце]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - 7. Практические первые шаги в этом месяце

_Слов: 373_

### [[08-implikatsii-nautilus-okwf|8. Импликации для Nautilus и OKWF]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 8. Импликации для Nautilus и OKWF

_Слов: 575_

### [[09-riski-voprosy|9. Риски и Открытые Вопросы]]
> > !WARNING

  - Содержание
  - 9. Риски и Открытые Вопросы

_Слов: 558_

### [[10-strategicheskoe-pozitsionirovanie|10. Стратегическое Позиционирование]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 10. Стратегическое Позиционирование

_Слов: 650_

### [[README|ingit-cowork-ru]]
> Файлов: 10

  - Содержание

_Слов: 62_

### [[00-question-innovations-transitions|Du hast gesagt: Интересно как новая как инновация как как рационализация как пер…]]
> > !WARNING

  - Содержание
  - Ответ по существу

_Слов: 2802_

### [[01-response|Claude hat geantwortet: Отличный запрос.]]
> > !TIP


_Слов: 2405_

### [[README|innovation-transitions]]
> Файлов: 2

  - Содержание

_Слов: 16_

### [[00-question-multi-tier|Du hast gesagt: Ещё есть такие вопросы то есть если общие юридические Наутилус м…]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — многоуровне…


_Слов: 197_

### [[01-strategic-significance|Claude hat geantwortet: Это стратегически значимый вопрос, и ответ на него — да,…]]
> > !WARNING


_Слов: 2586_

### [[README|multi-tier-architecture]]
> Файлов: 2

  - Содержание

_Слов: 17_

### [[00-question-can-it-apply-to-docs|Du hast gesagt: Вопрос такой вопрос и такие а можно ли этот протокол это система…]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — применение …


_Слов: 302_

### [[01-structural-comparison-code-vs-docs|Структурное сравнение: код vs гуманитарные документы]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — применение …

- Законодательные
- Судебные
- Административные
- Процессуальные
- Социальные/медицинские
- Контрактные
- Метаданные
- Всё из PortalEntry (id, title, source, formattype, content, links, isfallback)
  _... ещё 7 разделов_

_Слов: 1525_

### [[02-mcp-claude-desktop-use-cases|Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы …]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — применение …


_Слов: 219_

### [[03-what-doesnt-exist-on-market|Что не существует на рынке:]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — применение …


_Слов: 165_

### [[04-grant-opportunities|Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access t…]]
> > !TIP


_Слов: 540_

### [[05-which-combination-more-valuable|Что из этого сейчас кажется более ценным? Или какая-то своя комбинация?]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — применение …


_Слов: 139_

### [[README|npp-humanitarian-extension]]
> Файлов: 6

  - Содержание

_Слов: 41_

### [[00-abstract-status|Abstract + Status of This Document]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

- Nautilus Portal Protocol
  - Abstract
  - 0. Status of This Document

_Слов: 213_

### [[01-introduction|1. Introduction (Motivation, Design Goals, Non-Goals, Terminology)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 1. Introduction

_Слов: 313_

### [[02-terminology|2. Terminology]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 2. Terminology

_Слов: 267_

### [[03-registry|3. Registry (nautilus.json)]]
> > !IMPORTANT

  - 3. Registry (nautilus.json)

_Слов: 343_

### [[04-passport|4. Passport (passport.md)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 4. Passport (passport.md)
- ## Essence
  - Native Format
  - Content Overview
  - Angle / Perspective
  - Bridges
  - Author & Contact
  - History

_Слов: 237_

### [[05-compatibility-levels|5. Compatibility Levels]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 5. Compatibility Levels

_Слов: 221_

### [[06-adapter-interface|6. Adapter Interface]]
> > !IMPORTANT

  - 6. Adapter Interface

_Слов: 334_

### [[07-portal-entry|7. PortalEntry Structure]]
> > !IMPORTANT

  - 7. PortalEntry Structure

_Слов: 224_

### [[08-consensus-algorithm|8. Consensus Algorithm (v1.0: string normalization)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 8. Consensus Algorithm

_Слов: 266_

### [[09-query-flow|9. Query Flow]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 9. Query Flow

_Слов: 182_

### [[10-query-result|10. QueryResult Structure]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 10. QueryResult Structure

_Слов: 157_

### [[11-security-considerations|11. Security Considerations]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 11. Security Considerations

_Слов: 198_

### [[12-versioning-policy|12. Versioning Policy]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 12. Versioning Policy

_Слов: 173_

### [[13-reference-implementation|13. Reference Implementation]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 13. Reference Implementation

_Слов: 120_

### [[14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 14. ADR-001: Federation over Merging

_Слов: 202_

### [[15-glossary|15. Glossary of Examples]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 15. Glossary of Examples
  - Appendix A: Minimal Working Example
- mynotes
  - Essence
  - Native Format
  - Content Overview
  - Angle / Perspective
  - Author

_Слов: 272_

### [[16-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

- mynotes
  - Essence
  - Native Format
  - Content Overview
  - Angle / Perspective
  - Author

_Слов: 190_

### [[17-appendix-b-change-log|Appendix B: Change Log]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - Appendix B: Change Log

_Слов: 95_

### [[18-comment-on-document|Комментарий: дизайн-решения NPP v1.0]]
> > !IMPORTANT


_Слов: 454_

### [[README|npp-v1-0]]
> Файлов: 19

  - Содержание

_Слов: 116_

### [[00-abstract-status|Abstract + Status of This Document]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

- Nautilus Portal Protocol
  - Abstract
  - 0. Status of This Document

_Слов: 335_

### [[01-introduction|1. Introduction (Motivation, Design Goals, Non-Goals, Terminology, Changes from v1.0)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 1. Introduction

_Слов: 447_

### [[02-terminology|2. Terminology]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 2. Terminology

_Слов: 371_

### [[03-registry|3. Registry (nautilus.json)]]
> > !IMPORTANT

  - 3. Registry (nautilus.json)

_Слов: 479_

### [[04-passport|4. Passport (passport.md)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 4. Passport (passport.md)
- Паспорт: /

_Слов: 294_

### [[05-compatibility-levels|5. Compatibility Levels]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 5. Compatibility Levels

_Слов: 302_

### [[06-adapter-interface|6. Adapter Interface]]
> > !IMPORTANT

  - 6. Adapter Interface

_Слов: 327_

### [[07-portal-entry|7. PortalEntry Structure]]
> > !IMPORTANT

  - 7. PortalEntry Structure

_Слов: 290_

### [[08-q6-space|8. Q6 Space (Normative)]]
> > !IMPORTANT

  - 8. Q6 Space (Normative)

_Слов: 415_

### [[09-consensus-algorithm|9. Consensus Algorithm]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 9. Consensus Algorithm

_Слов: 343_

### [[10-query-flow|10. Query Flow]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 10. Query Flow

_Слов: 228_

### [[11-relevance-ranking|11. Relevance Ranking]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 11. Relevance Ranking
- Bonus for connectivity
- Penalty for fallback

_Слов: 203_

### [[12-onboarding-paths|12. Onboarding Paths (Normative)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 12. Onboarding Paths (Normative)

_Слов: 449_

### [[13-rest-api|13. REST API Contract (Normative for Portals)]]
> > !IMPORTANT

  - 13. REST API Contract (Normative for Portals)

_Слов: 437_

### [[14-sdk|14. SDK Contract (Informative)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 14. SDK Contract (Informative)

_Слов: 192_

### [[15-security|15. Security Considerations]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 15. Security Considerations

_Слов: 288_

### [[16-mcp-extension|16. MCP Extension (Informative)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 16. MCP Extension (Informative)

_Слов: 154_

### [[17-versioning-policy|17. Versioning Policy]]
> > !IMPORTANT

  - 17. Versioning Policy

_Слов: 227_

### [[18-reference-implementation|18. Reference Implementation]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 18. Reference Implementation

_Слов: 212_

### [[19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 19. ADR-001: Federation over Merging

_Слов: 218_

### [[20-adr-002-q6-first-class|20. ADR-002: Q6 as First-Class Protocol Concept]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 20. ADR-002: Q6 as First-Class Protocol Concept

_Слов: 210_

### [[21-adr-003-five-onboarding-paths|21. ADR-003: Five Onboarding Paths as Equal-Rank]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 21. ADR-003: Five Onboarding Paths as Equal-Rank

_Слов: 174_

### [[22-glossary|22. Glossary of Reference Examples]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - Содержание
  - 22. Glossary of Reference Examples
  - Appendix A: Minimal Working Example
- adapters/mynotes.py
- ... больше entries
- Паспорт: owner/my-notes
  - Описание
  - Объём
  _... ещё 6 разделов_

_Слов: 1486_

### [[README|npp-v1-1]]
> Файлов: 23

  - Содержание

_Слов: 138_

### [[00-abstract|AI-Coordinated Infrastructure for Distributed Expert Contribution]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

- Open Knowledge Work Foundation
  - AI-Coordinated Infrastructure for Distributed Expert Contribution
  - Executive Summary
  - Table of Contents

_Слов: 383_

### [[01-problem-statement|1. Problem Statement]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 1. Problem Statement

_Слов: 582_

### [[02-target-populations|2. Target Populations]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 2. Target Populations

_Слов: 650_

### [[03-why-existing-fail|3. Why Existing Solutions Fail]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 3. Why Existing Solutions Fail

_Слов: 663_

### [[04-proposed-infrastructure|4. Proposed Infrastructure]]
> > !TIP

  - Содержание
  - 4. Proposed Infrastructure

_Слов: 969_

### [[05-economic-model|5. Economic Model]]
> > !TIP

  - Содержание
  - 5. Economic Model

_Слов: 578_

### [[06-governance-ethics|6. Governance and Ethics]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - 6. Governance and Ethics

_Слов: 486_

### [[07-phased-rollout|7. Phased Rollout Plan]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 7. Phased Rollout Plan

_Слов: 615_

### [[08-risk-analysis|8. Risk Analysis]]
> > !TIP

  - Содержание
  - 8. Risk Analysis

_Слов: 643_

### [[09-call-for-partnership|9. Call for Partnership]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - 9. Call for Partnership

_Слов: 460_

### [[10-appendices|10. Appendices]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 10. Appendices

_Слов: 796_

### [[README|okwf-concept]]
> Файлов: 11

  - Содержание

_Слов: 69_

### [[00-question-anonymization|Du hast gesagt: Насчёт приватности Я думаю что возможно удалять только личные да…]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — приватность…


_Слов: 288_

### [[01-what-to-anonymize-german-standard|Что именно анонимизировать: немецкий стандарт]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — приватность…


_Слов: 269_

### [[02-two-tier-publication|Архитектурное решение: две-уровневая публикация]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — приватность…

- В приватном репо cases-private:

_Слов: 498_

### [[03-what-this-gives-technically|Что это даёт технически]]
> > !WARNING


_Слов: 1492_

### [[04-what-i-can-do-now|Что я могу сделать сейчас]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — приватность…


_Слов: 322_

### [[README|privacy-federation]]
> Файлов: 5

  - Содержание

_Слов: 35_

### [[00-abstract|Professional Colleague Agents]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

- Professional Colleague Agents
  - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers
  - Abstract
  - Table of Contents

_Слов: 426_

### [[01-five-type-typology|1. The Five-Type Typology of Principal-Side Agents]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 1. The Five-Type Typology of Principal-Side Agents

_Слов: 871_

### [[02-what-makes-pca|2. What Makes a Professional Colleague Agent]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 2. What Makes a Professional Colleague Agent

_Слов: 787_

### [[03-empirical-case-obuchay|3. Empirical Case Study: «Обучай»]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 3. Empirical Case Study: «Обучай»

_Слов: 807_

### [[04-architecture|4. Architecture of Professional Colleague Agents]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 4. Architecture of Professional Colleague Agents

_Слов: 847_

### [[05-economics-replication|5. The Economics of Profession-Wide Replication]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 5. The Economics of Profession-Wide Replication

_Слов: 695_

### [[06-risks|6. Risks Specific to this Category]]
> > !TIP

  - Содержание
  - 6. Risks Specific to this Category

_Слов: 1153_

### [[07-application-domains|7. Application Domains]]
> > !TIP

  - Содержание
  - 7. Application Domains

_Слов: 703_

### [[08-pilot-sgb-advocate|8. Pilot Proposal: SGB Advocate Colleague]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 8. Pilot Proposal: SGB Advocate Colleague

_Слов: 925_

### [[09-relationship-other-agents|9. Relationship to Other Agent Types]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 9. Relationship to Other Agent Types

_Слов: 620_

### [[10-open-questions|10. Open Questions]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - 10. Open Questions

_Слов: 358_

### [[11-call-for-collaboration|11. Call for Collaboration]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - 11. Call for Collaboration

_Слов: 310_

### [[12-closing|12. Closing]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 12. Closing
  - Acknowledgments
  - References

_Слов: 520_

### [[README|professional-colleague-agents-en]]
> Файлов: 13

  - Содержание

_Слов: 82_

### [[00-abstract|Содержание]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - Содержание

_Слов: 153_

### [[01-pyat-tipov|1. Типология из пяти типов агентов на стороне принципала]]
> > !IMPORTANT

  - Содержание
  - 1. Типология из пяти типов агентов на стороне принципала

_Слов: 842_

### [[02-chto-delaet-pka|2. Что делает агента Профессиональным Коллегой]]
> > !TIP

  - Содержание
  - 2. Что делает агента Профессиональным Коллегой

_Слов: 713_

### [[03-keys-obuchay|3. Эмпирический кейс: «Обучай»]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - Содержание
  - 3. Эмпирический кейс: «Обучай»

_Слов: 762_

### [[04-arkhitektura|4. Архитектура Профессиональных Коллег-Агентов]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов

_Слов: 806_

### [[05-ekonomika|5. Экономика тиражирования по профессии]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - Содержание
  - 5. Экономика тиражирования по профессии

_Слов: 689_

### [[06-riski|6. Риски, специфичные для этой категории]]
> > !WARNING

  - Содержание
  - 6. Риски, специфичные для этой категории

_Слов: 1142_

### [[07-oblasti-primeneniya|7. Области применения]]
> > !WARNING

  - Содержание
  - 7. Области применения

_Слов: 716_

### [[08-pilot-sgb-kolega|8. Пилотное предложение: SGB Колega-Адвокат]]
> > !WARNING

  - Содержание
  - 8. Пилотное предложение: SGB Колega-Адвокат

_Слов: 981_

### [[09-svyaz-s-drugimi|9. Связь с другими типами агентов]]
> > !WARNING

  - Содержание
  - 9. Связь с другими типами агентов

_Слов: 611_

### [[10-otkrytye-voprosy|10. Открытые вопросы]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - 10. Открытые вопросы

_Слов: 341_

### [[11-prizyv-k-sotrudnichestvu|11. Призыв к сотрудничеству]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - 11. Призыв к сотрудничеству

_Слов: 300_

### [[12-zaklyuchenie|12. Заключение]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - 12. Заключение
  - Благодарности
  - Ссылки

_Слов: 489_

### [[README|professional-colleague-agents-ru]]
> Файлов: 13

  - Содержание

_Слов: 78_

### [[00-abstract|AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

- The Representative Agent Layer
  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations
  - Abstract
  - Table of Contents

_Слов: 398_

### [[01-cinderella-syndrome|1. The Cinderella Syndrome: Why Quality Stays Invisible]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible

_Слов: 793_

### [[02-historical-precedents|2. Historical Precedents: Agents as Civilizational Innovation]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 2. Historical Precedents: Agents as Civilizational Innovation

_Слов: 911_

### [[03-what-makes-representative-agent|3. What Makes a Representative Agent]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 3. What Makes a Representative Agent

_Слов: 623_

### [[04-ten-domains|4. Ten Domains of Application]]
> > !TIP

  - Содержание
  - 4. Ten Domains of Application

_Слов: 1552_

### [[05-architectural-specification|5. Architectural Specification]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 5. Architectural Specification

_Слов: 618_

### [[06-ethical-framework|6. Ethical Framework]]
> > !IMPORTANT

  - 6. Ethical Framework

_Слов: 463_

### [[07-governance-oversight|7. Governance and Oversight]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 7. Governance and Oversight

_Слов: 385_

### [[08-risks-mitigations|8. Risks and Mitigations]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 8. Risks and Mitigations

_Слов: 486_

### [[09-phased-rollout|9. Phased Rollout Strategy]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 9. Phased Rollout Strategy

_Слов: 469_

### [[10-open-questions|10. Open Questions]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 10. Open Questions

_Слов: 367_

### [[11-call-for-collaboration|11. Call for Collaboration]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 11. Call for Collaboration

_Слов: 374_

### [[12-closing|12. Closing]]
> > !TIP

  - Содержание
  - 12. Closing
  - Acknowledgments
  - References
  - Appendix A: Connection to Companion Papers
  - Appendix B: Domain Comparison Matrix
  - Appendix C: Sample Use Cases in Detail
- The Representative Agent Layer
  _... ещё 1 разделов_

_Слов: 2676_

### [[README|representative-agent-layer-en]]
> Файлов: 13

  - Содержание

_Слов: 81_

### [[00-abstract|Содержание]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание

_Слов: 119_

### [[01-sindrom-zolushki|1. Синдром Золушки: Почему качество остаётся невидимым]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым

_Слов: 751_

### [[02-istoricheskie-pretsedenty|2. Исторические прецеденты: Агенты как цивилизационная инновация]]
> > !WARNING

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация

_Слов: 919_

### [[03-chto-delaet-predstavitelskim|3. Что делает агента Представительским]]
> > !TIP

  - Содержание
  - 3. Что делает агента Представительским

_Слов: 609_

### [[04-desyat-oblastey|4. Десять областей применения]]
> > !WARNING

  - Содержание
  - 4. Десять областей применения

_Слов: 1572_

### [[05-arkhitekturnaya-spetsifikatsiya|5. Архитектурная спецификация]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 5. Архитектурная спецификация

_Слов: 601_

### [[06-eticheskaya-ramka|6. Этическая рамка]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 6. Этическая рамка

_Слов: 448_

### [[07-upravlenie-nadzor|7. Управление и надзор]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 7. Управление и надзор

_Слов: 383_

### [[08-riski-mery|8. Риски и меры противодействия]]
> > !WARNING

  - Содержание
  - 8. Риски и меры противодействия

_Слов: 573_

### [[09-strategiya-razvyortyvaniya|9. Стратегия поэтапного развёртывания]]
> > !WARNING

  - 9. Стратегия поэтапного развёртывания

_Слов: 484_

### [[10-otkrytye-voprosy|10. Открытые вопросы]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 10. Открытые вопросы

_Слов: 353_

### [[11-prizyv-k-sotrudnichestvu|11. Призыв к сотрудничеству]]
> > !WARNING

  - 11. Призыв к сотрудничеству

_Слов: 381_

### [[12-zaklyuchenie|12. Заключение]]
> > !TIP

  - Содержание
  - 12. Заключение
  - Благодарности
  - Ссылки
  - Приложение A: Связь с Сопроводительными Статьями
  - Приложение B: Матрица Сравнения Областей
  - Приложение C: Образцы Случаев Использования в Деталях

_Слов: 4414_

### [[README|representative-agent-layer-ru]]
> Файлов: 13

  - Содержание

_Слов: 77_

### [[00-tldr|TL;DR — Трёхфазная методология Review]]
> > !WARNING

- Трёхфазная методология Review в Nautilus
  - TL;DR

_Слов: 191_

### [[01-context-motivation|1. Контекст и мотивация]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 1. Контекст и мотивация

_Слов: 361_

### [[02-formal-workflow|2. Формальный workflow]]
> > !WARNING

  - 2. Формальный workflow

_Слов: 407_

### [[03-consolidation-principles|3. Принципы консолидации (Фаза C)]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 3. Принципы консолидации (Фаза C)
- LOC в Python-коде
- Количество тестов
- Число адаптеров
- Health score
- Q6-покрытие

_Слов: 455_

### [[04-fallback-ratio-question|Вопрос: fallback‑ratio как критический или осмысленный?]]
> > !IMPORTANT

  - Вопрос: fallback-ratio как критический или осмысленный?

_Слов: 281_

### [[05-conditions-of-applicability|4. Условия применимости]]
> > !WARNING

  - 4. Условия применимости

_Слов: 258_

### [[06-relation-existing-methodologies|5. Связь с существующими методологиями]]
> > !WARNING

  - 5. Связь с существующими методологиями

_Слов: 333_

### [[07-why-valid-for-ai|6. Почему это валидный паттерн для AI‑assisted workflows]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 6. Почему это валидный паттерн для AI-assisted workflows

_Слов: 197_

### [[08-implementation-nautilus|7. Реализация в проекте Nautilus]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 7. Реализация в проекте Nautilus

_Слов: 257_

### [[09-limitations-open-questions|8. Ограничения и открытые вопросы]]
> > !WARNING

  - 8. Ограничения и открытые вопросы

_Слов: 373_

### [[10-checklist|9. Checklist применения методологии]]
> > !WARNING

  - 9. Checklist применения методологии

_Слов: 303_

### [[11-application-plan-current-docs|10. Конкретный план применения к текущим документам]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 10. Конкретный план применения к текущим документам
- В Termux

_Слов: 225_

### [[12-appendix-a-header-warning|Appendix A: Шаблон для header warning]]
> > !WARNING

  - Appendix A: Шаблон для header warning

_Слов: 214_

### [[13-appendix-b-examples|Appendix B: Примеры расхождений и их разрешения]]
> > !WARNING

  - Appendix B: Примеры расхождений и их разрешения

_Слов: 281_

### [[14-main-technical-risks|Главные технические риски]]
> > !WARNING

  - Главные технические риски

_Слов: 143_

### [[15-appendix-c-history|Appendix C: История изменений методологии]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - Appendix C: История изменений методологии

_Слов: 100_

### [[16-glossary|Глоссарий]]
> > !WARNING

  - Глоссарий

_Слов: 971_

### [[README|review-methodology]]
> Файлов: 17

  - Содержание

_Слов: 97_

### [[00-question-supply-demand|Du hast gesagt: Спрос рождает предложение - это простая экономическая истина нач…]]
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — спрос рожда…


_Слов: 447_

### [[01-three-related-themes|Claude hat geantwortet: Очень богатый вопрос — три разных, но связанных темы.]]
> > !WARNING


_Слов: 2915_

### [[README|supply-demand]]
> Файлов: 2

  - Содержание

_Слов: 17_

### [[00-question-mountain-to-person|Du hast gesagt: Того если гора не идёт человеку может быть этот человек пойдёт к…]]
> > !TIP


_Слов: 549_

### [[01-completing-loop|Claude hat geantwortet: Это исключительно богатый вопрос, и я хочу ответить на н…]]
> > !TIP


_Слов: 3126_

### [[README|transmission-box]]
> Файлов: 2

  - Содержание

_Слов: 16_

**Итого в секции: 148,523 слов, 255 файлов**


## 📁 Svyazi 2 0 (`docs/svyazi-2-0/`)

### [[README|Svyazi 2.0 — тематический индекс]]
> Содержимое исходных файлов deep-research-report (1)/(2)/(3)/(4).md (находятся в корне репозитория, не изменены) разбито …

  - Подпапки
  - Источник

_Слов: 158_

### [[README|architecture]]
> Файлов: 7

  - Содержание

_Слов: 46_

### [[card-envelope|Card Envelope]]
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 182_

### [[evidence-envelope|Evidence Envelope]]
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля
  - Особые случаи

_Слов: 222_

### [[gaps|Архитектурные зазоры]]
> > !TIP

  - Содержание
  - Пять зазоров, важнее поиска ещё десяти инструментов
  - Сводная таблица зазоров
  - Главный практический принцип

_Слов: 597_

### [[integration-spec|Интеграционная спецификация (минимум для MVP)]]
> > !TIP


_Слов: 267_

### [[memory-write-policy|Memory Write Policy]]
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 168_

### [[review-record|Review Record]]
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 105_

### [[skill-tool-policy|Skill and Tool Policy]]
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 165_

### [[README|components]]
> Файлов: 19

  - Содержание

_Слов: 120_

### [[agent-memory-mcp|agent-memory-mcp + Memory OS]]
> > - Автор: VitaliySemenov / moshael

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 150_

### [[agentfs]]
> > - Источник: Хабр + GitHub citeturn33view4turn33view7turn27view0

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 109_

### [[ai-factory|AI Factory + AIF Handoff]]
> > - Источник: Хабр + GitHub citeturn20view3turn29search0turn29search9

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 114_

### [[autoresearch-sequential|AutoResearch + Sequential]]
> > - Авторы: Андрей Карпаты / Виктория Дочкина

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 122_

### [[graph-rag|Graph RAG]]
> > - Автор: VladSpace / vpakspace

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 109_

### [[hybrid-rag|Hybrid RAG knowledge base]]
> > - Источник: Хабр citeturn34view2

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 102_

### [[knowledge-space]]
> > - Автор: SoniaBlack / AnastasiyaW

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 107_

### [[legal-rag|Legal RAG]]
> > - Источник: Хабр citeturn20view6

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 105_

### [[mclaude]]
> > - Источник: Хабр + GitHub citeturn20view2turn37search0

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 98_

### [[memnet|MemNet / memory-is-all-you-need]]
> > - Источник: Хабр + GitHub citeturn21view4turn17search0turn18search2

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 99_

### [[ngt-memory|NGT Memory]]
> > - Автор: spbmolot / ngt-memory

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 120_

### [[research-docs-liteparse|research-docs + LiteParse]]
> > - Автор: nlaik / Jerry Liu / LlamaIndex

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 121_

### [[rufler]]
> > - Автор: zodigancode / lib4u

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 98_

### [[security-routing-plane|Security + routing plane]]
> > - Авторы: Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig

  - Описание
  - Ключевые компоненты и паттерны
  - Числовые наблюдения

_Слов: 192_

### [[self-aware-mcp|Self‑Aware MCP + Skills + CodeWiki]]
> > - Авторы: akazant / akzhankalimatov / AnastasiyaW

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 132_

### [[svyazi]]
> > - Источник: Хабр citeturn41search0

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 116_

### [[voice-stack|Voice / local-first stack]]
> > - Авторы: atatchin / askid / обзоры Handy / OpenWhispr

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 136_

### [[yjs-automerge|Yjs + Automerge]]
> > - Авторы: Kevin Jahns / Automerge team

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 109_

### [[yodoca]]
> > - Источник: Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 109_

### [[A-collaboration-os|Ансамбль A — Collaboration OS]]
> > > Источник: deep-research-report (1).md.

  - Схема
  - Ожидаемые новые свойства

_Слов: 248_

### [[B-forensic-rag|Ансамбль B — Forensic RAG для доказуемого matching и review]]
> > > Источник: deep-research-report (1).md.

  - Схема
  - Ожидаемые новые свойства

_Слов: 252_

### [[C-multi-agent-factory|Ансамбль C — Spec‑driven multi‑agent factory]]
> > > Источник: deep-research-report (1).md.

  - Схема
  - Ожидаемые новые свойства

_Слов: 249_

### [[D-voice-first-mesh|Ансамбль D — Voice‑first local knowledge mesh]]
> > !IMPORTANT

  - Схема
  - Ожидаемые новые свойства

_Слов: 265_

### [[E-execution-plane|Ансамбль E — Safe and cheap execution plane]]
> > > Источник: deep-research-report (1).md.

  - Схема
  - Ожидаемые новые свойства

_Слов: 253_

### [[F-evidence-backed-intake|Ансамбль F — Evidence‑Backed Community Intake]]
> > > Источник: deep-research-report (3).md (ансамбли «второго порядка»).

  - Схема
  - Новые свойства

_Слов: 262_

### [[G-federated-local-graph|Ансамбль G — Federated Local‑First Community Graph]]
> > > Источник: deep-research-report (3).md.

  - Схема
  - Новое свойство

_Слов: 268_

### [[H-research-to-product-flywheel|Ансамбль H — Research‑to‑Product Flywheel]]
> > > Источник: deep-research-report (3).md.

  - Схема
  - Новое свойство

_Слов: 234_

### [[README|Ансамбли проектов]]
> Файлов: 8

  - Содержание

_Слов: 54_

### [[README|limitations]]
> Файлов: 3

  - Содержание

_Слов: 22_

### [[conclusions|Итоговые выводы и порядок сборки]]
> > > Источники: deep-research-report (1).md (раздел «Выводы») и итог из deep-research-report (3).md.

  - Главный вывод первой части
  - Порядок практической сборки
  - Главный вывод второй части

_Слов: 318_

### [[do-not-glue|Что пока лучше не склеивать]]
> > !WARNING

  - Оркестрация — выбрать один spine
  - Voice/local‑first mesh — не идеализировать
  - Self‑improvement — только после метрики

_Слов: 343_

### [[license-tree|Лицензионные развилки]]
> > !WARNING

  - Развилки в коротком виде

_Слов: 324_

### [[README|outreach]]
> Файлов: 3

  - Содержание

_Слов: 22_

### [[first-contacts|Первые контакты]]
> > !TIP


_Слов: 259_

### [[message-template|Шаблон первого сообщения]]
> > !TIP

  - Замечание

_Слов: 248_

### [[narrow-questions|Узкие вопросы для каждого автора]]
> > > Источник: deep-research-report (3).md, раздел «Контактная стратегия и узкие вопросы для авторов».

  - Адресные вопросы

_Слов: 306_

### [[README|overview]]
> Файлов: 4

  - Содержание

_Слов: 27_

### [[continuation-intro|Что добавляет продолжение исследования]]
> > > Источник: deep-research-report (3).md, раздел «Что это продолжение добавляет».


_Слов: 242_

### [[executive-summary|Executive summary]]
> > !TIP


_Слов: 376_

### [[methodology|Методика и рамка отбора]]
> > !TIP


_Слов: 268_

### [[projects-map|Карта найденных проектов и паттернов]]
> > !TIP


_Слов: 1285_

### [[README|prototype]]
> Файлов: 3

  - Содержание

_Слов: 21_

### [[mvp-plan|План MVP-прототипа]]
> > !TIP

  - Минимальная сборка прототипа

_Слов: 312_

### [[risks|Ключевые риски и как их закрывать]]
> > !TIP


_Слов: 287_

### [[roadmap|Дорожная карта прототипа]]
> > !TIP

  - Содержание
  - Итерация 1 — Evidence-first card graph
  - Итерация 2 — Memory governance
  - Итерация 3 — Orchestration + federation
  - Сводная таблица
  - Главный инженерный вывод

_Слов: 609_

### [[README|security]]
> Файлов: 3

  - Содержание

_Слов: 21_

### [[budget-routing|Практичный бюджетный роутинг моделей]]
> > !WARNING

  - Обоснование
  - Три режима

_Слов: 329_

### [[default-policy|Что стоит зафиксировать как default policy]]
> > !WARNING


_Слов: 349_

### [[privacy|Приватность: local-first by default]]
> > !WARNING


_Слов: 124_

**Итого в секции: 12,455 слов, 59 файлов**


## 📁 Technology Combinations (`docs/technology-combinations/`)

### [[README|technology-combinations/ — комбинирование технологий для новых свойств]]
> Файл в корне репозитория: Комбинирование технологий для новых свойств - Claude(../../%D0%9A%D0%BE%D0%BC%D0%B1%D0%B8%D0%B…

  - Источник
  - Подпапки
  - Главная находка диалога
  - См. также

_Слов: 155_

### [[01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern|Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 230_

### [[02-multiagentnyy-khaos-reshenie-auto-ai-router|Комбинация 2: Мультиагентный хаос-решение × Auto AI Router]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 171_

### [[03-crdt-local-first-svyazi-cardindex|Комбинация 3: CRDT local-first × Svyazi CardIndex]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 181_

### [[04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura|Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 200_

### [[05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy|Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 196_

### [[06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-|Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 202_

### [[07-crawl4ai-docling-yodoca-consolidator|Комбинация 7: Crawl4AI × Docling × Yodoca consolidator]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 183_

### [[08-conductor-adversarial-review-auto-ai-router|Комбинация 8: Conductor × adversarial-review × Auto AI Router]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 668_

### [[09-agent-orchestration-stack|Комбинация 9: Agent Orchestration Stack]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 180_

### [[10-legal-document-intelligence-pipeline|Комбинация 10: Legal Document Intelligence Pipeline]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 182_

### [[11-hybrid-crdt-sql-database|Комбинация 11: Hybrid CRDT-SQL Database]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 173_

### [[12-multi-agent-observability-stack|Комбинация 12: Multi-Agent Observability Stack]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 165_

### [[13-legal-document-transpiler|Комбинация 13: Legal Document Transpiler]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 164_

### [[14-local-first-agent-development-environment|Комбинация 14: local-first Agent Development Environment]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 559_

### [[15-self-consolidating-legal-corpus|Комбинация 15: Self-Consolidating Legal Corpus]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 210_

### [[16-adversarial-multi-agent-code-review|Комбинация 16: Adversarial Multi-Agent Code Review]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 254_

### [[17-distributed-agent-memory-with-graph|Комбинация 17: Distributed Agent Memory with Graph]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 209_

### [[18-llm-powered-legal-corpus-builder|Комбинация 18: LLM-Powered Legal Corpus Builder]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Crawl4AI pipeline
- Svyazi deduplication

_Слов: 210_

### [[19-multi-agent-observability-platform|Комбинация 19: Multi-Agent Observability Platform]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 678_

### [[20-hybrid-olap-oltp-with-real-time-sync|Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 240_

### [[21-legal-corpus-analytics-at-scale|Комбинация 21: Legal Corpus Analytics at Scale]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Pipeline
- Schema
- Analytics queries (subsecond)

_Слов: 233_

### [[22-russian-international-oss-stack|Комбинация 22: Russian-International OSS Stack]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 197_

### [[23-security-first-code-review-pipeline|Комбинация 23: Security-First Code Review Pipeline]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 183_

### [[24-mega-integration-full-stack|Комбинация 24: MEGA-INTEGRATION: Full Stack]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 594_

### [[25-legal-dsl-code-transpiler|Комбинация 25: Legal DSL → Code Transpiler]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- DSL syntax (natural language-like)
- DSL operations
- Output: ready Widerspruch.docx
- DSL for conversion

_Слов: 236_

### [[26-ast-based-code-analysis-for-legal-automation|Комбинация 26: AST-Based Code Analysis for Legal Automation]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Input: Python script for Fristwahrung calculation
- AST analysis
- Extract legal logic
- → Pydantic model: LegalRule(
- name="Widerspruchsfrist",
- baseduration=timedelta(days(),
- extensions=[...],
- legalbasis="SGG § 84"
  _... ещё 3 разделов_

_Слов: 206_

### [[27-hybrid-rag-with-ast-chunked-code|Комбинация 27: Hybrid RAG with AST-Chunked Code]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 204_

### [[28-pydantic-enforced-legal-workflows|Комбинация 28: Pydantic-Enforced Legal Workflows]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Sequential pipeline with Pydantic validation at each stage

_Слов: 209_

### [[29-meta-programmatic-legal-template-generator|Комбинация 29: Meta-Programmatic Legal Template Generator]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Legal DSL (declarative)
- Compiler generates Python code
- auto-generated rendering logic

_Слов: 198_

### [[30-mega-stack-3-0-with-dsl-ast|Комбинация 30: MEGA-STACK 3.0 with DSL & AST]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 489_

### [[31-event-sourced-legal-document-history|Комбинация 31: Event-Sourced Legal Document History]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 229_

### [[32-consensus-based-multi-agent-coordination|Комбинация 32: Consensus-Based Multi-Agent Coordination]]
> > !TIP


_Слов: 244_

### [[33-event-sourcing-cqrs-clickhouse-analytics|Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 205_

### [[34-distributed-event-store-with-paxos|Комбинация 34: Distributed Event Store with Paxos]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 177_

### [[35-mega-stack-4-0-with-event-sourcing-consensus|Комбинация 35: MEGA-STACK 4.0 with Event Sourcing & Consensus]]
> > !TIP

- Events
- Event Store
- Time-travel query

_Слов: 483_

### [[README|combinations]]
> Файлов: 35

  - Содержание

_Слов: 214_

### [[01-legal-ai-stack|Mega‑Stack 1.0 — Полный Legal‑AI Stack]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «MEGA‑COMBINATION: Полный Legal‑…

  - Результат
  - Первый проект для внедрения

_Слов: 211_

### [[02-ultimate-legal-ai|Mega‑Stack 2.0 — Ultimate Legal‑AI System]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «MEGA‑STACK 2.0: Ultimate Legal‑…

  - Capabilities
  - First implementation priority

_Слов: 318_

### [[03-dsl-ast|Mega‑Stack 3.0 — with DSL & AST]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «КОМБИНАЦИЯ 30: MEGA‑STACK 3.0 w…

  - New capabilities

_Слов: 226_

### [[04-event-sourcing-consensus|Mega‑Stack 4.0 — with Event Sourcing & Consensus]]
> > !TIP

  - New capabilities
  - Performance

_Слов: 313_

### [[README|mega-stacks]]
> Файлов: 4

  - Содержание

_Слов: 29_

### [[README|properties/ — эмерджентные свойства]]
> Один файл — одно свойство, которое возникает только при комбинировании нескольких технологий.

  - Шаблон файла
- <Название свойства>
  - Что это
  - Какие компоненты дают это свойство в комбинации
  - Почему ни один из них в отдельности не даёт свойства
  - Как проверить, что свойство реально появилось

_Слов: 68_

### [[README|research-reports]]
> Файлов: 2

  - Содержание

_Слов: 18_

### [[continuation-10-domains|Research Report: Continuation — 10 New Domains Beyond the Original 45 Combinations]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «Continuation Research — 10 New …

  - 10 новых технологических областей
  - 35+ новых синергетических комбинаций
  - 5 кросс‑сквозных эмерджентных архитектур
  - Методологические оговорки
  - Применение к Sozialrecht
  - Артефакт документа
  - Итоговый объём исследования

_Слов: 316_

### [[sozialrecht-35-combinations|Research Report: Sozialrecht (35 комбинаций)]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «A Research Report Building on 3…

  - Что в отчёте
  - Артефакт документа

_Слов: 222_

### [[01-08-summary|Сводная таблица 1–8]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция 📊 «Сводная таблица синергии».

  - 🎯 Главная находка: паттерн «скромные родители → мощные дети»
  - Рекомендация

_Слов: 383_

### [[09-14-extended|Сводная таблица 9–14 (Extended)]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «SYNTHESIS TABLE (Extended)».


_Слов: 195_

### [[15-19-extended|Сводная таблица 15–19 (Extended)]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «EXTENDED SYNTHESIS TABLE».


_Слов: 162_

### [[20-24-final|Сводная таблица 20–24 (Final 1–24)]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «FINAL SYNTHESIS TABLE (Complete…

  - Рекомендация

_Слов: 212_

### [[25-30-extended|Сводная таблица 25–30 (Complete 1–30)]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «EXTENDED SYNTHESIS TABLE (Compl…

  - Рекомендация

_Слов: 228_

### [[31-35-final|Сводная таблица 31–35 (Complete 1–35)]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «EXTENDED SYNTHESIS TABLE (Compl…

  - Рекомендация
- Events
- Event Store (append-only)
- Time-travel query

_Слов: 249_

### [[README|synthesis-tables]]
> Файлов: 6

  - Содержание

_Слов: 42_

**Итого в секции: 12,903 слов, 53 файлов**


## 📁 Templates (`docs/templates/`)

### [[README|Шаблоны документов]]
> Создано: 2026-04-29

  - Доступные шаблоны
  - Использование
- Скопируйте нужный шаблон в нужную папку
- Затем откройте и заполните поля в [квадратных скобках]

_Слов: 82_

### [Спецификация агента: [Название]](docs/templates/agent-spec.md)
> representative  professional-colleague  composite-skills  catalyst  companion  other

  - Тип агента
  - Назначение
  - Принципал
  - Скилы агента
  - Tools (плагины)
  - Память
  - Decision boundary
  - Failure modes
  _... ещё 3 разделов_

_Слов: 356_

### [Контакт: [Имя / Проект]](docs/templates/contact-outreach.md)
>  Параметр  Значение 

  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы для обсуждения

_Слов: 119_

### [Противоречие: [Название]](docs/templates/contradiction-record.md)
> CONTRA-NNNN

  - ID
  - Серьёзность
  - Источник A
  - Источник B
  - В чём противоречие
  - Возможные интерпретации
  - Решение
  - Связанные противоречия

_Слов: 174_

### [ADR: [Название решения]](docs/templates/decision-record.md)
> Предложено / Принято / Отклонено / Устарело

  - Статус
  - Контекст
  - Рассмотренные варианты
  - Принятое решение
  - Последствия

_Слов: 84_

### [Ансамбль: [Название]](docs/templates/ensemble.md)
> Какую задачу решает ансамбль. Почему именно эта комбинация компонентов.

  - Назначение
  - Компоненты
  - Архитектурная схема
  - Контракт взаимодействия
  - Риски и ограничения
  - MVP-шаги

_Слов: 112_

### [Эксперимент: [Название]](docs/templates/experiment-log.md)
> > Если X, то Y, потому что Z.

  - Гипотеза
  - Зачем
  - Метод
  - Журнал
  - Результат
  - Выводы
  - Следующие действия
  - Сырые данные

_Слов: 185_

### [FAQ: [Вопрос]](docs/templates/faq-entry.md)
> > Точная формулировка вопроса

  - Вопрос
  - Краткий ответ
  - Подробный ответ
  - Когда это НЕ применимо
  - Связанные вопросы
  - Источники / документы
  - История обновлений

_Слов: 132_

### [[Термин]](docs/templates/glossary-entry.md)
> Полное определение в 2-3 предложениях.

  - Определение
  - Происхождение
  - Синонимы и аббревиатуры
  - Примеры
  - Связанные термины
  - Где упоминается в монорепо
  - Источники

_Слов: 117_

### [KPI Snapshot: [дата]](docs/templates/kpi-snapshot.md)
> Дата снапшота: 2026-04-29

  - Период
  - Сводка
  - Детальные метрики
  - Лучшие изменения
  - Регрессии
  - Топ-3 фокуса на следующий период

_Слов: 220_

### [Юридический кейс: [Aktenzeichen]](docs/templates/legal-case.md)
>  Параметр  Значение 

  - Идентификация
  - Стороны
  - Хронология
  - Предмет спора
  - Применимые нормы (§§)
  - Аргументы
  - Прецеденты
  - Текущий статус
  _... ещё 3 разделов_

_Слов: 275_

### [Встреча: [Тема]](docs/templates/meeting-notes.md)
> Зачем собрались. Какой вопрос обсуждали.

  - Контекст
  - Участники
  - Повестка
  - Обсуждение
  - Принятые решения
  - Action Items
  - Открытые вопросы
  - Следующая встреча

_Слов: 151_

### [Mega-stack: [Название]](docs/templates/mega-stack.md)
> Класс задач: legal-AI / knowledge-OS / etc.

  - Назначение
  - Слои стека (сверху вниз)
  - Cross-layer контракты
  - Roadmap по фазам
  - Стоимость
  - Риски и митигации
  - Альтернативные стеки
  - Связанные ансамбли

_Слов: 339_

### [[Название компонента]](docs/templates/project-component.md)
> Описание проекта в 2-3 предложениях. Какую задачу решает.

  - Что это
  - Ключевые особенности
  - Статус
  - Интеграция с Svyazi
  - Контакты

_Слов: 102_

### [[Название протокола]](docs/templates/protocol-spec.md)
> draft  proposed  implemented  superseded

  - 0. Status of this Document
  - 1. Introduction
  - 2. Terminology
  - 3. Registry / Discovery
  - 4. Passport / Identity
  - 5. Compatibility Levels
  - 6. Adapter Interface
  - 7. PortalEntry
  _... ещё 10 разделов_

_Слов: 361_

### [MVP: [Название]](docs/templates/prototype-mvp.md)
> MVP-NNNN

  - ID
  - Цель
  - Метрика успеха
  - Срок
  - Состав
  - Фазы
  - Open questions
  - Риски
  _... ещё 4 разделов_

_Слов: 368_

### [[Тема исследования]](docs/templates/research-note.md)
> Зачем изучали. Какой вопрос стоял.

  - Контекст
  - Ключевые находки
  - Источники
  - Открытые вопросы
  - Следующие шаги

_Слов: 66_

### [Ретроспектива: [период]](docs/templates/retrospective.md)
> С: 2026-04-22

  - Период
  - Что прошло хорошо ✅
  - Что прошло плохо ❌
  - Что узнали 💡
  - Action items для следующего периода
  - Метрики периода
  - Улучшения процесса

_Слов: 160_

### [RFC NNNN: [Название]](docs/templates/rfc.md)
> draft  proposed  accepted  rejected  implemented  superseded

  - Status of this Document
  - Abstract
  - 1. Introduction
  - 2. Specification
  - 3. Architecture
  - 4. Compatibility
  - 5. Security Considerations
  - 6. Privacy Considerations
  _... ещё 4 разделов_

_Слов: 225_

### [Риск: [Название]](docs/templates/risk-entry.md)
> > !WARNING

  - ID
  - Описание
  - Сценарий реализации
  - Оценка
  - Митигация
  - Триггеры мониторинга
  - История
  - Связанные риски

_Слов: 221_

### [Tech Pair: [A] × [B]](docs/templates/tech-pair.md)
> PAIR-NNNN

  - ID
  - Компонент A
  - Компонент B
  - Синергия
  - Архитектура
  - Контракт интеграции
  - Антисинергии
  - Известные результаты
  _... ещё 4 разделов_

_Слов: 273_

### [Tech Radar: [Название]](docs/templates/tech-radar-entry.md)
> techniques  tools  platforms  languages-and-frameworks

  - Quadrant
  - Ring
  - Описание
  - Почему именно этот ring
  - Когда использовать
  - Когда НЕ использовать
  - Альтернативы
  - Опыт использования в Lorenzo
  _... ещё 2 разделов_

_Слов: 224_

### [[имя нового шаблона]](docs/templates/template-of-templates.md)
> Это мета-шаблон для создания новых шаблонов в docs/templates/.

  - Что делать
  - Обязательные блоки шаблона
- [Заголовок]
  - Обязательные поля JSON-Schema
  - Чеклист добавления нового шаблона
  - Типичные паттерны

_Слов: 319_

### [Еженедельный дайджест: [период]](docs/templates/weekly-digest.md)
> 3-5 пунктов главного за неделю.

  - TL;DR
  - Что сделано
  - Метрики недели
  - Решения
  - Открытые вопросы недели
  - План на следующую неделю
  - Заметки

_Слов: 193_

**Итого в секции: 4,858 слов, 24 файлов**


## 🗺️ Тематическая карта

### Архитектура (564 документов)
- [[365-развёрнутый-анализ-внуковой-комбинации|`365-развёрнутый-анализ-внуковой-комбинации`]]
- [[CONCEPTS|`CONCEPTS`]]
- [[TABLES|`TABLES`]]
- [[00-intro|`00-intro`]]
- [[01-интегральный-анализ-профиля-svend4|`01-интегральный-анализ-профиля-svend4`]]
- _... ещё 559_

### Агенты (156 документов)
- [[C-multi-agent-factory|`C-multi-agent-factory`]]
- [[107-1-контекст-и-мотивация|`107-1-контекст-и-мотивация`]]
- [[108-2-формальный-workflow|`108-2-формальный-workflow`]]
- [[345-кто-ты|`345-кто-ты`]]
- [[00-question-what-is-hermes|`00-question-what-is-hermes`]]
- _... ещё 151_

### Проекты (142 документов)
- [[TIMELINE|`TIMELINE`]]
- [[02-общий-план-развития-nautilus-portal-protocol|`02-общий-план-развития-nautilus-portal-protocol`]]
- [[228-appendix-c-quick-start-architecture-for-sgb-advoca|`228-appendix-c-quick-start-architecture-for-sgb-advoca`]]
- [[299-практические-рекомендации-для-текущего-проекта|`299-практические-рекомендации-для-текущего-проекта`]]
- [[336-10-стратегическое-позиционирование|`336-10-стратегическое-позиционирование`]]
- _... ещё 137_

### Документация (83 документов)
- [[CODE_BLOCKS|`CODE_BLOCKS`]]
- [[EMPTY_SECTIONS|`EMPTY_SECTIONS`]]
- [[118-appendix-a-шаблон-для-header-warning|`118-appendix-a-шаблон-для-header-warning`]]
- [[98-appendix-a-minimal-working-example|`98-appendix-a-minimal-working-example`]]
- [[COMPLEXITY|`COMPLEXITY`]]
- _... ещё 78_

### Контакты (56 документов)
- [[ngt-memory|`ngt-memory`]]
- [[REGISTRY|`REGISTRY`]]
- [[06-1-introduction|`06-1-introduction`]]
- [[105-review-methodology-md|`105-review-methodology-md`]]
- [[163-9-call-for-partnership|`163-9-call-for-partnership`]]
- _... ещё 51_

### Память (43 документов)
- [[11-integration-contracts|`11-integration-contracts`]]
- [[174-5-architectural-specification|`174-5-architectural-specification`]]
- [[NARRATIVE|`NARRATIVE`]]
- [[REPORT|`REPORT`]]
- [[source-projects|`source-projects`]]
- _... ещё 38_

### Код (36 документов)
- [[DEPENDENCY_MAP|`DEPENDENCY_MAP`]]
- [[83-8-q6-space-normative|`83-8-q6-space-normative`]]
- [[84-9-consensus-algorithm|`84-9-consensus-algorithm`]]
- [[90-15-security-considerations|`90-15-security-considerations`]]
- [[CHANGELOG_AUTO|`CHANGELOG_AUTO`]]
- _... ещё 31_

### Анализ (19 документов)
- [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|`110-вопрос-fallback-ratio-как-критический-или-осмыслен`]]
- [[COMPARE|`COMPARE`]]
- [[README|`README`]]
- [[154-table-of-contents|`154-table-of-contents`]]
- [[155-1-problem-statement|`155-1-problem-statement`]]
- _... ещё 14_

