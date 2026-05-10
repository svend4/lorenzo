---
title: "Outline базы знаний"
tags:
  - general
date: 2026-05-10
---

# Outline базы знаний

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> Секций: **20** | Файлов: **1213**
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse

---

<!-- toc -->
## Содержание

- [Содержание](#содержание)
- [Docs](#docs)
  - [[ABBREVIATIONS|[Словарь аббревиатур и сокращений]]](#словарь-аббревиатур-и-сокращенийabbreviationsmd)
  - [[ACTION_ITEMS|[Action Items, риски и решения]]](#action-items-риски-и-решенияaction_itemsmd)
  - [[ALERTS|[Callout-блоки]]](#callout-блокиalertsmd)
  - [[AUTHORS|[Авторы и коллаборации]]](#авторы-и-коллаборацииauthorsmd)
  - [[AUTOFILLED|[Автозаполненные шаблоны]]](#автозаполненные-шаблоныautofilledmd)
  - [[BACKLINKS|[Индекс обратных ссылок]]](#индекс-обратных-ссылокbacklinksmd)
  - [[BADGES|[Status Badges]]](#status-badgesbadgesmd)
  - [[CHANGELOG|[CHANGELOG]]](#changelogchangelogmd)
  - [[CHANGELOG_AUTO|[Changelog (авто)]]](#changelog-автоchangelog_automd)
  - [[CLUSTERS|[Кластеры тематически близких файлов]]](#кластеры-тематически-близких-файловclustersmd)
  - [[CODE_BLOCKS|[Code-блоки репозитория]]](#code-блоки-репозиторияcode_blocksmd)
  - [[COLLAB_SUGGESTIONS|[Рекомендации по коллаборации (Collaboration Finder)]]](#рекомендации-по-коллаборации-collaboration-findercollab_suggestionsmd)
  - [[COMPARE|[Сравнение с предыдущим коммитом]]](#сравнение-с-предыдущим-коммитомcomparemd)
  - [[COMPLEXITY|[Оценка читаемости документов]]](#оценка-читаемости-документовcomplexitymd)
  - [[COMPONENT_MATRIX|[Матрица компонентов Svyazi 2.0]]](#матрица-компонентов-svyazi-20component_matrixmd)
  - [[CONCEPTS|[Глоссарий понятий]]](#глоссарий-понятийconceptsmd)
  - [[CONCEPT_GRAPH|[Граф концептов базы знаний]]](#граф-концептов-базы-знанийconcept_graphmd)
  - [[CONSISTENCY|[Согласованность терминов]]](#согласованность-терминовconsistencymd)
  - [[CONTACTS|[Контакты и авторы]]](#контакты-и-авторыcontactsmd)
  - [[CONTACT_PRIORITY|[Приоритет контактов]]](#приоритет-контактовcontact_prioritymd)
  - [[CONTRADICTIONS|[Противоречия в базе знаний]]](#противоречия-в-базе-знанийcontradictionsmd)
  - [[COST|[Оценка стоимости MVP]]](#оценка-стоимости-mvpcostmd)
  - [[CROSSREFS|[Перекрёстные ссылки]]](#перекрёстные-ссылкиcrossrefsmd)
  - [[CROSS_SECTION|[Кросс-секционный анализ]]](#кросс-секционный-анализcross_sectionmd)
  - [[DECISIONS|[Ключевые решения и выводы]]](#ключевые-решения-и-выводыdecisionsmd)
  - [[DENSITY|[Карта плотности тем]]](#карта-плотности-темdensitymd)
  - [[DEPENDABOT|[Мониторинг зависимостей]]](#мониторинг-зависимостейdependabotmd)
  - [[DEPENDENCY_MAP|[Карта зависимостей скриптов]]](#карта-зависимостей-скриптовdependency_mapmd)
  - [[DIGEST|[Дайджест изменений]]](#дайджест-измененийdigestmd)
  - [[DIGEST_AUTO|[Автодайджест изменений]]](#автодайджест-измененийdigest_automd)
  - [[DIGEST_WEEKLY|[Еженедельный дайджест — 2026-04-29]]](#еженедельный-дайджест-2026-04-29digest_weeklymd)
  - [[DUPLICATES|[Отчёт о дублировании]]](#отчёт-о-дублированииduplicatesmd)
  - [[EMPTY_SECTIONS|[Пустые секции]]](#пустые-секцииempty_sectionsmd)
  - [[ENTITIES|[Именованные сущности]]](#именованные-сущностиentitiesmd)
  - [[FAQ|[Часто задаваемые вопросы (FAQ)]]](#часто-задаваемые-вопросы-faqfaqmd)
  - [[FOOTNOTES|[Сноски и определения терминов]]](#сноски-и-определения-терминовfootnotesmd)
  - [[GLOSSARY|[Глоссарий проектов]]](#глоссарий-проектовglossarymd)
  - [[GRAPH|[Граф связей проектов]]](#граф-связей-проектовgraphmd)
  - [[HEADING_AUDIT|[Аудит заголовков]]](#аудит-заголовковheading_auditmd)
  - [[HEALTH|[Health Dashboard]]](#health-dashboardhealthmd)
  - [[HEATMAP|[Тепловая карта тем]]](#тепловая-карта-темheatmapmd)
  - [[INDEX|[Индекс документации — Lorenzo / Svyazi 2.0]]](#индекс-документации-lorenzo-svyazi-20indexmd)
  - [[KEYWORD_INDEX|[Инвертированный индекс ключевых слов]]](#инвертированный-индекс-ключевых-словkeyword_indexmd)
  - [[KNOWLEDGE_MAP|[Карта базы знаний Lorenzo]]](#карта-базы-знаний-lorenzoknowledge_mapmd)
  - [[KPI|[Числовые KPI и метрики]]](#числовые-kpi-и-метрикиkpimd)
  - [[KPI_HISTORY|[История метрик KPI]]](#история-метрик-kpikpi_historymd)
  - [[LANGUAGE_STATS|[Языковой состав документов]]](#языковой-состав-документовlanguage_statsmd)
  - [[LINKS|[Индекс ссылок]]](#индекс-ссылокlinksmd)
  - [[LLM_SUMMARIES|[AI-саммари разделов документации]]](#ai-саммари-разделов-документацииllm_summariesmd)
  - [[MCP_DASHBOARD|[MCP Dashboard]]](#mcp-dashboardmcp_dashboardmd)
  - [[METHODOLOGY|[Методология работы со скриптами]]](#методология-работы-со-скриптамиmethodologymd)
  - [[METRICS|[Метрики качества документации]]](#метрики-качества-документацииmetricsmd)
  - [[MINDMAP|[Майндмап репозитория Lorenzo]]](#майндмап-репозитория-lorenzomindmapmd)
  - [[MISSING|[Карта пробелов знаний]]](#карта-пробелов-знанийmissingmd)
  - [[NAMED_ENTITIES|[Индекс именованных сущностей]]](#индекс-именованных-сущностейnamed_entitiesmd)
  - [[NARRATIVE|[Нарратив проекта Lorenzo]]](#нарратив-проекта-lorenzonarrativemd)
  - [[NETWORK|[Сеть проектов и авторов]]](#сеть-проектов-и-авторовnetworkmd)
  - [[ONBOARDING|[Онбординг — Svyazi 2.0 / Lorenzo]]](#онбординг-svyazi-20-lorenzoonboardingmd)
  - [[ORPHANS|[Изолированные документы (Orphans)]]](#изолированные-документы-orphansorphansmd)
  - [[PARAGRAPH_QUALITY|[Качество абзацев]]](#качество-абзацевparagraph_qualitymd)
  - [[PASSIVE_VOICE|[Пассивный залог и канцеляризмы]]](#пассивный-залог-и-канцеляризмыpassive_voicemd)
  - [[PRIORITIES|[Приоритеты файлов]]](#приоритеты-файловprioritiesmd)
  - [[PROGRESS|[Прогресс MVP]]](#прогресс-mvpprogressmd)
  - [[PROTOTYPE_SPEC|[Svyazi 2.0 — Спецификация прототипа]]](#svyazi-20-спецификация-прототипаprototype_specmd)
  - [[QA|[Глобальный Q&A]]](#глобальный-qaqamd)
  - [[QUESTIONS|[Вопросы и открытые темы из базы знаний]]](#вопросы-и-открытые-темы-из-базы-знанийquestionsmd)
  - [[READING_LIST|[Список чтения]]](#список-чтенияreading_listmd)
  - [[READING_ORDER|[Рекомендуемый порядок чтения]]](#рекомендуемый-порядок-чтенияreading_ordermd)
  - [[README|[docs]]](#docsreadmemd)
  - [[REGISTRY|[REGISTRY — реестр артефактов Lorenzo]]](#registry-реестр-артефактов-lorenzoregistrymd)
  - [[REPORT|[Executive Report: Репозиторий Lorenzo]]](#executive-report-репозиторий-lorenzoreportmd)
  - [[RISK_REGISTER|[Реестр рисков — Svyazi 2.0]]](#реестр-рисков-svyazi-20risk_registermd)
  - [[SCHEDULE|[Расписание проекта]]](#расписание-проектаschedulemd)
  - [[SCORING|[Оценка готовности проекта (Go/No-Go)]]](#оценка-готовности-проекта-gono-goscoringmd)
  - [[SCRIPTS_CATALOG|[Каталог скриптов]]](#каталог-скриптовscripts_catalogmd)
  - [[SCRIPT_EVAL_REPORT|[Отчёт об оценке скриптов Lorenzo]]](#отчёт-об-оценке-скриптов-lorenzoscript_eval_reportmd)
  - [[SEARCH_RESULTS|[Результаты поиска]]](#результаты-поискаsearch_resultsmd)
  - [[SEE_ALSO|[Индекс «Смотрите также»]]](#индекс-смотрите-такжеsee_alsomd)
  - [[SENTIMENT|[Тональный анализ документов]]](#тональный-анализ-документовsentimentmd)
  - [[SIMILAR|[Похожие документы]]](#похожие-документыsimilarmd)
  - [[SIMILAR_PASSAGES|[Похожие абзацы между документами]]](#похожие-абзацы-между-документамиsimilar_passagesmd)
  - [[SITEMAP|[Карта репозитория Lorenzo]]](#карта-репозитория-lorenzositemapmd)
  - [[SKILL_DASHBOARD|[Skill Dashboard]]](#skill-dashboardskill_dashboardmd)
  - [[SOURCE_MAP|[Карта происхождения текстов]]](#карта-происхождения-текстовsource_mapmd)
  - [[STATS|[Детальная статистика репозитория]]](#детальная-статистика-репозиторияstatsmd)
  - [[SUMMARIES|[Резюме документов (TextRank)]]](#резюме-документов-textranksummariesmd)
  - [[TABLES|[Все таблицы репозитория]]](#все-таблицы-репозиторияtablesmd)
  - [[TAGS|[Индекс тегов]]](#индекс-теговtagsmd)
  - [[TASKS_INDEX|[Каталог задач (TASKSINDEX)]]](#каталог-задач-tasksindextasks_indexmd)
  - [[TECH_RADAR|[Tech Radar — Svyazi 2.0]]](#tech-radar-svyazi-20tech_radarmd)
  - [[TIMELINE|[Хронологическая лента событий]]](#хронологическая-лента-событийtimelinemd)
  - [[VALIDATION|[Валидация структуры репозитория]]](#валидация-структуры-репозиторияvalidationmd)
  - [[VOCABULARY|[Богатство словаря документов]]](#богатство-словаря-документовvocabularymd)
  - [[WORD_CLOUD|[Word Cloud]]](#word-cloudword_cloudmd)
  - [[WORD_FREQ|[Частотный анализ слов]]](#частотный-анализ-словword_freqmd)
  - [[reading-paths|[Reading paths — рекомендуемые маршруты по монорепозиторию]]](#reading-paths-рекомендуемые-маршруты-по-монорепозиториюreading-pathsmd)
- [Svyazi](#svyazi)
  - [[00-intro-part2|[Продолжение исследования для Svyazi 2.0]]](#продолжение-исследования-для-svyazi-2001-svyazi00-intro-part2md)
  - [[Svyazi[^svyazi] 2.0 — Исполнительное резюме](01-svyazi/01-executive-summary.md)](#svyazisvyazi-20-исполнительное-резюме01-svyazi01-executive-summarymd)
  - [[02-methodology|[Методика и рамка отбора проектов]]](#методика-и-рамка-отбора-проектов01-svyazi02-methodologymd)
  - [[03-component-catalog|[Карта найденных проектов и паттернов]]](#карта-найденных-проектов-и-паттернов01-svyazi03-component-catalogmd)
  - [[04-ensembles-overview|[Приоритетные ансамбли]]](#приоритетные-ансамбли01-svyazi04-ensembles-overviewmd)
  - [[06-security-privacy|[Безопасность, приватность и бюджетный роутинг]]](#безопасность-приватность-и-бюджетный-роутинг01-svyazi06-security-privacymd)
  - [[07-mvp-planning|[План прототипа и возможные контакты]]](#план-прототипа-и-возможные-контакты01-svyazi07-mvp-planningmd)
  - [[08-conclusions|[Выводы]]](#выводы01-svyazi08-conclusionsmd)
  - [[09-architectural-gaps|[Архитектурные зазоры, которые важнее новых инструментов]]](#архитектурные-зазоры-которые-важнее-новых-инструментов01-svyazi09-architectural-gapsmd)
  - [[10-second-order-ensembles|[Новые ансамбли следующего шага]]](#новые-ансамбли-следующего-шага01-svyazi10-second-order-ensemblesmd)
  - [[11-integration-contracts|[Интеграционный контракт, который стоит зафиксировать сразу]]](#интеграционный-контракт-который-стоит-зафиксировать-сразу01-svyazi11-integration-contractsmd)
  - [[12-roadmap|[Дорожная карта прототипа следующей итерации]]](#дорожная-карта-прототипа-следующей-итерации01-svyazi12-roadmapmd)
  - [[13-contacts|[Содержание]]](#содержание01-svyazi13-contactsmd)
  - [[14-limitations|[Ограничения, лицензии и что пока лучше не склеивать]]](#ограничения-лицензии-и-что-пока-лучше-не-склеивать01-svyazi14-limitationsmd)
  - [[QA|[Q&A: 01-svyazi]]](#qa-01-svyazi01-svyaziqamd)
  - [[Svyazi[^svyazi] 2.0 — Архитектура и исследование](01-svyazi/README.md)](#svyazisvyazi-20-архитектура-и-исследование01-svyazireadmemd)
- [Anthropic Vacancies](#anthropic-vacancies)
  - [[00-intro|[Введение]]](#введение02-anthropic-vacancies00-intromd)
  - [[01-интегральный-анализ-профиля-svend4|[Интегральный анализ профиля svend4]]](#интегральный-анализ-профиля-svend402-anthropic-vacancies01-интегральный-анализ-профиля-svend4md)
  - [[02-общий-план-развития-nautilus-portal-protocol|[ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]]](#общий-план-развития-nautilus-portal-protocol02-anthropic-vacancies02-общий-план-развития-nautilus-portal-protocolmd)
  - [[03-portal-protocol-md|[PORTAL-PROTOCOL.md]]](#portal-protocolmd02-anthropic-vacancies03-portal-protocol-mdmd)
  - [[04-abstract|[Abstract]]](#abstract02-anthropic-vacancies04-abstractmd)
  - [[05-0-status-of-this-document|[0. Status of This Document]]](#0-status-of-this-document02-anthropic-vacancies05-0-status-of-this-documentmd)
  - [[06-1-introduction|[1. Introduction]]](#1-introduction02-anthropic-vacancies06-1-introductionmd)
  - [[07-2-terminology|[2. Terminology]]](#2-terminology02-anthropic-vacancies07-2-terminologymd)
  - [[08-3-registry-nautilus-json|[3. Registry (nautilus.json)]]](#3-registry-nautilusjson02-anthropic-vacancies08-3-registry-nautilus-jsonmd)
  - [[09-4-passport-passport-md|[4. Passport (passport.md)]]](#4-passport-passportmd02-anthropic-vacancies09-4-passport-passport-mdmd)
  - [[102-доступ-к-данным|[Доступ к данным]]](#доступ-к-данным02-anthropic-vacancies102-доступ-к-даннымmd)
  - [[103-appendix-b-change-log|[Appendix B: Change Log]]](#appendix-b-change-log02-anthropic-vacancies103-appendix-b-change-logmd)
  - [[104-appendix-c-references|[Appendix C: References]]](#appendix-c-references02-anthropic-vacancies104-appendix-c-referencesmd)
  - [[105-review-methodology-md|[REVIEWMETHODOLOGY.md]]](#reviewmethodologymd02-anthropic-vacancies105-review-methodology-mdmd)
  - [[106-tl-dr|[TL;DR]]](#tldr02-anthropic-vacancies106-tl-drmd)
  - [[107-1-контекст-и-мотивация|[1. Контекст и мотивация]]](#1-контекст-и-мотивация02-anthropic-vacancies107-1-контекст-и-мотивацияmd)
  - [[108-2-формальный-workflow|[2. Формальный workflow]]](#2-формальный-workflow02-anthropic-vacancies108-2-формальный-workflowmd)
  - [[109-3-принципы-консолидации-фаза-c|[3. Принципы консолидации (Фаза C)]]](#3-принципы-консолидации-фаза-c02-anthropic-vacancies109-3-принципы-консолидации-фаза-cmd)
  - [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|[Вопрос: fallback-ratio как критический или осмысленный?]]](#вопрос-fallback-ratio-как-критический-или-осмысленный02-anthropic-vacancies110-вопрос-fallback-ratio-как-критический-или-осмысленmd)
  - [[111-4-условия-применимости|[4. Условия применимости]]](#4-условия-применимости02-anthropic-vacancies111-4-условия-применимостиmd)
  - [[112-5-связь-с-существующими-методологиями|[5. Связь с существующими методологиями]]](#5-связь-с-существующими-методологиями02-anthropic-vacancies112-5-связь-с-существующими-методологиямиmd)
  - [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|[6. Почему это валидный паттерн для AI-assisted workflows]]](#6-почему-это-валидный-паттерн-для-ai-assisted-workflows02-anthropic-vacancies113-6-почему-это-валидный-паттерн-для-ai-assisted-workmd)
  - [[114-7-реализация-в-проекте-nautilus|[7. Реализация в проекте Nautilus]]](#7-реализация-в-проекте-nautilus02-anthropic-vacancies114-7-реализация-в-проекте-nautilusmd)
  - [[115-8-ограничения-и-открытые-вопросы|[8. Ограничения и открытые вопросы]]](#8-ограничения-и-открытые-вопросы02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd)
  - [[116-9-checklist-применения-методологии|[9. Checklist применения методологии]]](#9-checklist-применения-методологии02-anthropic-vacancies116-9-checklist-применения-методологииmd)
  - [[117-10-конкретный-план-применения-к-текущим-документам|[10. Конкретный план применения к текущим документам]]](#10-конкретный-план-применения-к-текущим-документам02-anthropic-vacancies117-10-конкретный-план-применения-к-текущим-документамmd)
  - [[118-appendix-a-шаблон-для-header-warning|[Appendix A: Шаблон для header warning]]](#appendix-a-шаблон-для-header-warning02-anthropic-vacancies118-appendix-a-шаблон-для-header-warningmd)
  - [[119-appendix-b-примеры-расхождений-и-их-разрешения|[Appendix B: Примеры расхождений и их разрешения]]](#appendix-b-примеры-расхождений-и-их-разрешения02-anthropic-vacancies119-appendix-b-примеры-расхождений-и-их-разрешенияmd)
  - [[12-content-overview|[Content Overview]]](#content-overview02-anthropic-vacancies12-content-overviewmd)
  - [[120-главные-технические-риски|[Главные технические риски]]](#главные-технические-риски02-anthropic-vacancies120-главные-технические-рискиmd)
  - [[121-appendix-c-история-изменений-методологии|[Appendix C: История изменений методологии]]](#appendix-c-история-изменений-методологии02-anthropic-vacancies121-appendix-c-история-изменений-методологииmd)
  - [[122-глоссарий|[Глоссарий]]](#глоссарий02-anthropic-vacancies122-глоссарийmd)
  - [[123-portal-mcp-py|[portal-mcp.py]]](#portal-mcppy02-anthropic-vacancies123-portal-mcp-pymd)
  - [[124-конфигурация-для-claude-desktop|[Конфигурация для Claude Desktop]]](#конфигурация-для-claude-desktop02-anthropic-vacancies124-конфигурация-для-claude-desktopmd)
  - [[125-readme-mcp-md-инструкция-по-установке|[README-MCP.md— инструкция по установке]]](#readme-mcpmd-инструкция-по-установке02-anthropic-vacancies125-readme-mcp-md-инструкция-по-установкеmd)
  - [[126-установка|[Установка]]](#установка02-anthropic-vacancies126-установкаmd)
  - [[127-подключение-к-claude-desktop|[Подключение к Claude Desktop]]](#подключение-к-claude-desktop02-anthropic-vacancies127-подключение-к-claude-desktopmd)
  - [[128-доступные-инструменты|[Доступные инструменты]]](#доступные-инструменты02-anthropic-vacancies128-доступные-инструментыmd)
  - [[129-примеры-запросов-в-claude|[Примеры запросов (в Claude)]]](#примеры-запросов-в-claude02-anthropic-vacancies129-примеры-запросов-в-claudemd)
  - [[13-angle-perspective|[Angle / Perspective]]](#angle-perspective02-anthropic-vacancies13-angle-perspectivemd)
  - [[130-отладка|[Отладка]]](#отладка02-anthropic-vacancies130-отладкаmd)
  - [[131-ограничения-текущей-версии-0-1-0-draft|[Ограничения текущей версии (0.1.0-draft)]]](#ограничения-текущей-версии-010-draft02-anthropic-vacancies131-ограничения-текущей-версии-0-1-0-draftmd)
  - [[132-planned-v0-2-0|[Planned (v0.2.0)]]](#planned-v02002-anthropic-vacancies132-planned-v0-2-0md)
  - [[133-обратная-связь|[Обратная связь]]](#обратная-связь02-anthropic-vacancies133-обратная-связьmd)
  - [[134-the-double-triangle-architecture-md|[THE DOUBLE-TRIANGLE ARCHITECTURE.md]]](#the-double-triangle-architecturemd02-anthropic-vacancies134-the-double-triangle-architecture-mdmd)
  - [[135-a-formal-model-for-human-ai-collaboration-in-distr|[A Formal Model for Human-AI Collaboration in Distributed Knowledge Work]]](#a-formal-model-for-human-ai-collaboration-in-distributed-knowledge-work02-anthropic-vacancies135-a-formal-model-for-human-ai-collaboration-in-distrmd)
  - [[136-abstract|[Abstract]]](#abstract02-anthropic-vacancies136-abstractmd)
  - [[137-table-of-contents|[Table of Contents]]](#table-of-contents02-anthropic-vacancies137-table-of-contentsmd)
  - [[138-1-why-single-triangle-models-are-incomplete|[1. Why Single-Triangle Models Are Incomplete]]](#1-why-single-triangle-models-are-incomplete02-anthropic-vacancies138-1-why-single-triangle-models-are-incompletemd)
  - [[139-2-the-double-triangle-architecture|[2. The Double-Triangle Architecture]]](#2-the-double-triangle-architecture02-anthropic-vacancies139-2-the-double-triangle-architecturemd)
  - [[140-3-three-inter-layer-protocols|[3. Three Inter-Layer Protocols]]](#3-three-inter-layer-protocols02-anthropic-vacancies140-3-three-inter-layer-protocolsmd)
  - [[141-4-nautilus-portal-as-reference-substrate|[4. Nautilus Portal as Reference Substrate]]](#4-nautilus-portal-as-reference-substrate02-anthropic-vacancies141-4-nautilus-portal-as-reference-substratemd)
  - [[142-5-pattern-library-as-bridge-between-triangles|[5. Pattern Library as Bridge Between Triangles]]](#5-pattern-library-as-bridge-between-triangles02-anthropic-vacancies142-5-pattern-library-as-bridge-between-trianglesmd)
  - [[143-6-four-deployment-domains|[6. Four Deployment Domains]]](#6-four-deployment-domains02-anthropic-vacancies143-6-four-deployment-domainsmd)
  - [[144-7-open-questions|[7. Open Questions]]](#7-open-questions02-anthropic-vacancies144-7-open-questionsmd)
  - [[145-8-call-to-action|[8. Call to Action]]](#8-call-to-action02-anthropic-vacancies145-8-call-to-actionmd)
  - [[146-acknowledgments|[Acknowledgments]]](#acknowledgments02-anthropic-vacancies146-acknowledgmentsmd)
  - [[147-references|[References]]](#references02-anthropic-vacancies147-referencesmd)
  - [[148-appendix-a-glossary|[Appendix A: Glossary]]](#appendix-a-glossary02-anthropic-vacancies148-appendix-a-glossarymd)
  - [[149-appendix-b-summary-of-contributions|[Appendix B: Summary of Contributions]]](#appendix-b-summary-of-contributions02-anthropic-vacancies149-appendix-b-summary-of-contributionsmd)
  - [[150-appendix-c-version-history|[Appendix C: Version History]]](#appendix-c-version-history02-anthropic-vacancies150-appendix-c-version-historymd)
  - [[151-open-knowledge-work-foundation-md|[OPEN KNOWLEDGE WORK FOUNDATION.md]]](#open-knowledge-work-foundationmd02-anthropic-vacancies151-open-knowledge-work-foundation-mdmd)
  - [[152-ai-coordinated-infrastructure-for-distributed-expe|[AI-Coordinated Infrastructure for Distributed Expert Contribution]]](#ai-coordinated-infrastructure-for-distributed-expert-contribution02-anthropic-vacancies152-ai-coordinated-infrastructure-for-distributed-expemd)
  - [[153-executive-summary|[Executive Summary]]](#executive-summary02-anthropic-vacancies153-executive-summarymd)
  - [[154-table-of-contents|[Table of Contents]]](#table-of-contents02-anthropic-vacancies154-table-of-contentsmd)
  - [[155-1-problem-statement|[1. Problem Statement]]](#1-problem-statement02-anthropic-vacancies155-1-problem-statementmd)
  - [[156-2-target-populations|[2. Target Populations]]](#2-target-populations02-anthropic-vacancies156-2-target-populationsmd)
  - [[157-3-why-existing-solutions-fail|[3. Why Existing Solutions Fail]]](#3-why-existing-solutions-fail02-anthropic-vacancies157-3-why-existing-solutions-failmd)
  - [[158-4-proposed-infrastructure|[4. Proposed Infrastructure]]](#4-proposed-infrastructure02-anthropic-vacancies158-4-proposed-infrastructuremd)
  - [[159-5-economic-model|[5. Economic Model]]](#5-economic-model02-anthropic-vacancies159-5-economic-modelmd)
  - [[16-history|[History]]](#history02-anthropic-vacancies16-historymd)
  - [[160-6-governance-and-ethics|[6. Governance and Ethics]]](#6-governance-and-ethics02-anthropic-vacancies160-6-governance-and-ethicsmd)
  - [[161-7-phased-rollout-plan|[7. Phased Rollout Plan]]](#7-phased-rollout-plan02-anthropic-vacancies161-7-phased-rollout-planmd)
  - [[162-8-risk-analysis|[8. Risk Analysis]]](#8-risk-analysis02-anthropic-vacancies162-8-risk-analysismd)
  - [[163-9-call-for-partnership|[9. Call for Partnership]]](#9-call-for-partnership02-anthropic-vacancies163-9-call-for-partnershipmd)
  - [[164-10-appendices|[10. Appendices]]](#10-appendices02-anthropic-vacancies164-10-appendicesmd)
  - [[165-closing|[Closing]]](#closing02-anthropic-vacancies165-closingmd)
  - [[166-representative-agent-layer-md|[REPRESENTATIVE AGENT LAYER.md]]](#representative-agent-layermd02-anthropic-vacancies166-representative-agent-layer-mdmd)
  - [[167-ai-mediated-representation-for-underrepresented-ex|[AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]](#ai-mediated-representation-for-underrepresented-experts-and-vulnerable-populations02-anthropic-vacancies167-ai-mediated-representation-for-underrepresented-exmd)
  - [[168-abstract|[Abstract]]](#abstract02-anthropic-vacancies168-abstractmd)
  - [[169-table-of-contents|[Table of Contents]]](#table-of-contents02-anthropic-vacancies169-table-of-contentsmd)
  - [[17-5-compatibility-levels|[5. Compatibility Levels]]](#5-compatibility-levels02-anthropic-vacancies17-5-compatibility-levelsmd)
  - [[170-1-the-cinderella-syndrome-why-quality-stays-invisi|[1. The Cinderella Syndrome: Why Quality Stays Invisible]]](#1-the-cinderella-syndrome-why-quality-stays-invisible02-anthropic-vacancies170-1-the-cinderella-syndrome-why-quality-stays-invisimd)
  - [[171-2-historical-precedents-agents-as-civilizational-i|[2. Historical Precedents: Agents as Civilizational Innovation]]](#2-historical-precedents-agents-as-civilizational-innovation02-anthropic-vacancies171-2-historical-precedents-agents-as-civilizational-imd)
  - [[172-3-what-makes-a-representative-agent|[3. What Makes a Representative Agent]]](#3-what-makes-a-representative-agent02-anthropic-vacancies172-3-what-makes-a-representative-agentmd)
  - [[173-4-ten-domains-of-application|[4. Ten Domains of Application]]](#4-ten-domains-of-application02-anthropic-vacancies173-4-ten-domains-of-applicationmd)
  - [[174-5-architectural-specification|[5. Architectural Specification]]](#5-architectural-specification02-anthropic-vacancies174-5-architectural-specificationmd)
  - [[175-6-ethical-framework|[6. Ethical Framework]]](#6-ethical-framework02-anthropic-vacancies175-6-ethical-frameworkmd)
  - [[176-7-governance-and-oversight|[7. Governance and Oversight]]](#7-governance-and-oversight02-anthropic-vacancies176-7-governance-and-oversightmd)
  - [[177-8-risks-and-mitigations|[8. Risks and Mitigations]]](#8-risks-and-mitigations02-anthropic-vacancies177-8-risks-and-mitigationsmd)
  - [[178-9-phased-rollout-strategy|[9. Phased Rollout Strategy]]](#9-phased-rollout-strategy02-anthropic-vacancies178-9-phased-rollout-strategymd)
  - [[179-10-open-questions|[10. Open Questions]]](#10-open-questions02-anthropic-vacancies179-10-open-questionsmd)
  - [[18-6-adapter-interface|[6. Adapter Interface]]](#6-adapter-interface02-anthropic-vacancies18-6-adapter-interfacemd)
  - [[180-11-call-for-collaboration|[11. Call for Collaboration]]](#11-call-for-collaboration02-anthropic-vacancies180-11-call-for-collaborationmd)
  - [[181-12-closing|[12. Closing]]](#12-closing02-anthropic-vacancies181-12-closingmd)
  - [[182-acknowledgments|[Acknowledgments]]](#acknowledgments02-anthropic-vacancies182-acknowledgmentsmd)
  - [[183-references|[References]]](#references02-anthropic-vacancies183-referencesmd)
  - [[184-appendix-a-connection-to-companion-papers|[Appendix A: Connection to Companion Papers]]](#appendix-a-connection-to-companion-papers02-anthropic-vacancies184-appendix-a-connection-to-companion-papersmd)
  - [[185-appendix-b-domain-comparison-matrix|[Appendix B: Domain Comparison Matrix]]](#appendix-b-domain-comparison-matrix02-anthropic-vacancies185-appendix-b-domain-comparison-matrixmd)
  - [[186-appendix-c-sample-use-cases-in-detail|[Appendix C: Sample Use Cases in Detail]]](#appendix-c-sample-use-cases-in-detail02-anthropic-vacancies186-appendix-c-sample-use-cases-in-detailmd)
  - [[187-слой-представительских-агентов-md|[СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]]](#слой-представительских-агентовmd02-anthropic-vacancies187-слой-представительских-агентов-mdmd)
  - [[188-ai-опосредованное-представительство-для-недопредст|[AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения]]](#ai-опосредованное-представительство-для-недопредставленных-экспертов-и-уязвимых-категорий-населения02-anthropic-vacancies188-ai-опосредованное-представительство-для-недопредстmd)
  - [[189-аннотация|[Аннотация]]](#аннотация02-anthropic-vacancies189-аннотацияmd)
  - [[19-7-portalentry-structure|7. [PortalEntry Structure]]](#7-portalentry-structure02-anthropic-vacancies19-7-portalentry-structuremd)
  - [[190-содержание|[Содержание]]](#содержание02-anthropic-vacancies190-содержаниеmd)
  - [[191-1-синдром-золушки-почему-качество-остаётся-невидим|[1. Синдром Золушки: Почему качество остаётся невидимым]]](#1-синдром-золушки-почему-качество-остаётся-невидимым02-anthropic-vacancies191-1-синдром-золушки-почему-качество-остаётся-невидимmd)
  - [[192-2-исторические-прецеденты-агенты-как-цивилизационн|[2. Исторические прецеденты: Агенты как цивилизационная инновация]]](#2-исторические-прецеденты-агенты-как-цивилизационная-инновация02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd)
  - [[193-3-что-делает-агента-представительским|[3. Что делает агента Представительским]]](#3-что-делает-агента-представительским02-anthropic-vacancies193-3-что-делает-агента-представительскимmd)
  - [[194-4-десять-областей-применения|[4. Десять областей применения]]](#4-десять-областей-применения02-anthropic-vacancies194-4-десять-областей-примененияmd)
  - [[195-5-архитектурная-спецификация|[5. Архитектурная спецификация]]](#5-архитектурная-спецификация02-anthropic-vacancies195-5-архитектурная-спецификацияmd)
  - [[196-6-этическая-рамка|[6. Этическая рамка]]](#6-этическая-рамка02-anthropic-vacancies196-6-этическая-рамкаmd)
  - [[197-7-управление-и-надзор|[7. Управление и надзор]]](#7-управление-и-надзор02-anthropic-vacancies197-7-управление-и-надзорmd)
  - [[198-8-риски-и-меры-противодействия|[8. Риски и меры противодействия]]](#8-риски-и-меры-противодействия02-anthropic-vacancies198-8-риски-и-меры-противодействияmd)
  - [[199-9-стратегия-поэтапного-развёртывания|[9. Стратегия поэтапного развёртывания]]](#9-стратегия-поэтапного-развёртывания02-anthropic-vacancies199-9-стратегия-поэтапного-развёртыванияmd)
  - [[20-8-consensus-algorithm|[8. Consensus Algorithm]]](#8-consensus-algorithm02-anthropic-vacancies20-8-consensus-algorithmmd)
  - [[200-10-открытые-вопросы|[10. Открытые вопросы]]](#10-открытые-вопросы02-anthropic-vacancies200-10-открытые-вопросыmd)
  - [[201-11-призыв-к-сотрудничеству|[11. Призыв к сотрудничеству]]](#11-призыв-к-сотрудничеству02-anthropic-vacancies201-11-призыв-к-сотрудничествуmd)
  - [[202-12-заключение|[12. Заключение]]](#12-заключение02-anthropic-vacancies202-12-заключениеmd)
  - [[203-благодарности|[Благодарности]]](#благодарности02-anthropic-vacancies203-благодарностиmd)
  - [[204-ссылки|[Ссылки]]](#ссылки02-anthropic-vacancies204-ссылкиmd)
  - [[205-приложение-a-связь-с-сопроводительными-статьями|[Приложение A: Связь с Сопроводительными Статьями]]](#приложение-a-связь-с-сопроводительными-статьями02-anthropic-vacancies205-приложение-a-связь-с-сопроводительными-статьямиmd)
  - [[206-приложение-b-матрица-сравнения-областей|[Приложение B: Матрица Сравнения Областей]]](#приложение-b-матрица-сравнения-областей02-anthropic-vacancies206-приложение-b-матрица-сравнения-областейmd)
  - [[207-приложение-c-образцы-случаев-использования-в-детал|[Приложение C: Образцы Случаев Использования в Деталях]]](#приложение-c-образцы-случаев-использования-в-деталях02-anthropic-vacancies207-приложение-c-образцы-случаев-использования-в-деталmd)
  - [[208-professional-colleague-agents-md|[PROFESSIONAL COLLEAGUE AGENTS.md]]](#professional-colleague-agentsmd02-anthropic-vacancies208-professional-colleague-agents-mdmd)
  - [[209-a-typology-of-ai-agents-on-the-principal-side-and-|[A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers]]](#a-typology-of-ai-agents-on-the-principal-side-and-the-case-for-profession-specific-co-workers02-anthropic-vacancies209-a-typology-of-ai-agents-on-the-principal-side-and-md)
  - [[21-9-query-flow|[9. Query Flow]]](#9-query-flow02-anthropic-vacancies21-9-query-flowmd)
  - [[210-abstract|[Abstract]]](#abstract02-anthropic-vacancies210-abstractmd)
  - [[211-table-of-contents|[Table of Contents]]](#table-of-contents02-anthropic-vacancies211-table-of-contentsmd)
  - [[212-1-the-five-type-typology-of-principal-side-agents|[1. The Five-Type Typology of Principal-Side Agents]]](#1-the-five-type-typology-of-principal-side-agents02-anthropic-vacancies212-1-the-five-type-typology-of-principal-side-agentsmd)
  - [[213-2-what-makes-a-professional-colleague-agent|[2. What Makes a Professional Colleague Agent]]](#2-what-makes-a-professional-colleague-agent02-anthropic-vacancies213-2-what-makes-a-professional-colleague-agentmd)
  - [[214-3-empirical-case-study-обучай|[3. Empirical Case Study: «Обучай»]]](#3-empirical-case-study-обучай02-anthropic-vacancies214-3-empirical-case-study-обучайmd)
  - [[215-4-architecture-of-professional-colleague-agents|[4. Architecture of Professional Colleague Agents]]](#4-architecture-of-professional-colleague-agents02-anthropic-vacancies215-4-architecture-of-professional-colleague-agentsmd)
  - [[216-5-the-economics-of-profession-wide-replication|[5. The Economics of Profession-Wide Replication]]](#5-the-economics-of-profession-wide-replication02-anthropic-vacancies216-5-the-economics-of-profession-wide-replicationmd)
  - [[217-6-risks-specific-to-this-category|[6. Risks Specific to this Category]]](#6-risks-specific-to-this-category02-anthropic-vacancies217-6-risks-specific-to-this-categorymd)
  - [[218-7-application-domains|[7. Application Domains]]](#7-application-domains02-anthropic-vacancies218-7-application-domainsmd)
  - [[219-8-pilot-proposal-sgb-advocate-colleague|[8. Pilot Proposal: SGB Advocate Colleague]]](#8-pilot-proposal-sgb-advocate-colleague02-anthropic-vacancies219-8-pilot-proposal-sgb-advocate-colleaguemd)
  - [[22-10-queryresult-structure|10. [QueryResult Structure]]](#10-queryresult-structure02-anthropic-vacancies22-10-queryresult-structuremd)
  - [[220-9-relationship-to-other-agent-types|[9. Relationship to Other Agent Types]]](#9-relationship-to-other-agent-types02-anthropic-vacancies220-9-relationship-to-other-agent-typesmd)
  - [[221-10-open-questions|[10. Open Questions]]](#10-open-questions02-anthropic-vacancies221-10-open-questionsmd)
  - [[222-11-call-for-collaboration|[11. Call for Collaboration]]](#11-call-for-collaboration02-anthropic-vacancies222-11-call-for-collaborationmd)
  - [[223-12-closing|[12. Closing]]](#12-closing02-anthropic-vacancies223-12-closingmd)
  - [[224-acknowledgments|[Acknowledgments]]](#acknowledgments02-anthropic-vacancies224-acknowledgmentsmd)
  - [[225-references|[References]]](#references02-anthropic-vacancies225-referencesmd)
  - [[226-appendix-a-comparative-table-five-agent-types|[Appendix A: Comparative Table — Five Agent Types]]](#appendix-a-comparative-table-five-agent-types02-anthropic-vacancies226-appendix-a-comparative-table-five-agent-typesmd)
  - [[227-appendix-b-decision-framework-when-to-build-type-1|[Appendix B: Decision Framework — When to Build Type 1 First]]](#appendix-b-decision-framework-when-to-build-type-1-first02-anthropic-vacancies227-appendix-b-decision-framework-when-to-build-type-1md)
  - [[228-appendix-c-quick-start-architecture-for-sgb-advoca|[Appendix C: Quick-Start Architecture for SGB Advocate Colleague]]](#appendix-c-quick-start-architecture-for-sgb-advocate-colleague02-anthropic-vacancies228-appendix-c-quick-start-architecture-for-sgb-advocamd)
  - [[229-профессиональные-коллеги-агенты|[ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ]]](#профессиональные-коллеги-агенты02-anthropic-vacancies229-профессиональные-коллеги-агентыmd)
  - [[23-11-security-considerations|[11. Security Considerations]]](#11-security-considerations02-anthropic-vacancies23-11-security-considerationsmd)
  - [[230-аннотация|[Аннотация]]](#аннотация02-anthropic-vacancies230-аннотацияmd)
  - [[231-содержание|[Содержание]]](#содержание02-anthropic-vacancies231-содержаниеmd)
  - [[232-1-типология-из-пяти-типов-агентов-на-стороне-принц|[1. Типология из пяти типов агентов на стороне принципала]]](#1-типология-из-пяти-типов-агентов-на-стороне-принципала02-anthropic-vacancies232-1-типология-из-пяти-типов-агентов-на-стороне-принцmd)
  - [[233-2-что-делает-агента-профессиональным-коллегой|[2. Что делает агента Профессиональным Коллегой]]](#2-что-делает-агента-профессиональным-коллегой02-anthropic-vacancies233-2-что-делает-агента-профессиональным-коллегойmd)
  - [[234-3-эмпирический-кейс-обучай|[3. Эмпирический кейс: «Обучай»]]](#3-эмпирический-кейс-обучай02-anthropic-vacancies234-3-эмпирический-кейс-обучайmd)
  - [[235-4-архитектура-профессиональных-коллег-агентов|[4. Архитектура Профессиональных Коллег-Агентов]]](#4-архитектура-профессиональных-коллег-агентов02-anthropic-vacancies235-4-архитектура-профессиональных-коллег-агентовmd)
  - [[236-5-экономика-тиражирования-по-профессии|[5. Экономика тиражирования по профессии]]](#5-экономика-тиражирования-по-профессии02-anthropic-vacancies236-5-экономика-тиражирования-по-профессииmd)
  - [[237-6-риски-специфичные-для-этой-категории|[6. Риски, специфичные для этой категории]]](#6-риски-специфичные-для-этой-категории02-anthropic-vacancies237-6-риски-специфичные-для-этой-категорииmd)
  - [[238-7-области-применения|[7. Области применения]]](#7-области-применения02-anthropic-vacancies238-7-области-примененияmd)
  - [[239-8-пилотное-предложение-sgb-колega-адвокат|[8. Пилотное предложение: SGB Колega-Адвокат]]](#8-пилотное-предложение-sgb-колega-адвокат02-anthropic-vacancies239-8-пилотное-предложение-sgb-колega-адвокатmd)
  - [[24-12-versioning-policy|[12. Versioning Policy]]](#12-versioning-policy02-anthropic-vacancies24-12-versioning-policymd)
  - [[240-9-связь-с-другими-типами-агентов|[9. Связь с другими типами агентов]]](#9-связь-с-другими-типами-агентов02-anthropic-vacancies240-9-связь-с-другими-типами-агентовmd)
  - [[241-10-открытые-вопросы|[10. Открытые вопросы]]](#10-открытые-вопросы02-anthropic-vacancies241-10-открытые-вопросыmd)
  - [[242-11-призыв-к-сотрудничеству|[11. Призыв к сотрудничеству]]](#11-призыв-к-сотрудничеству02-anthropic-vacancies242-11-призыв-к-сотрудничествуmd)
  - [[243-12-заключение|[12. Заключение]]](#12-заключение02-anthropic-vacancies243-12-заключениеmd)
  - [[244-благодарности|[Благодарности]]](#благодарности02-anthropic-vacancies244-благодарностиmd)
  - [[245-ссылки|[Ссылки]]](#ссылки02-anthropic-vacancies245-ссылкиmd)
  - [[246-приложение-a-сравнительная-таблица-пять-типов-аген|[Приложение A: Сравнительная Таблица — Пять Типов Агентов]]](#приложение-a-сравнительная-таблица-пять-типов-агентов02-anthropic-vacancies246-приложение-a-сравнительная-таблица-пять-типов-агенmd)
  - [[247-приложение-b-рамка-принятия-решений-когда-строить-|[Приложение B: Рамка принятия решений — когда строить Тип 1 первым]]](#приложение-b-рамка-принятия-решений-когда-строить-тип-1-первым02-anthropic-vacancies247-приложение-b-рамка-принятия-решений-когда-строить-md)
  - [[248-приложение-c-архитектура-быстрого-старта-для-sgb-а|[Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги]]](#приложение-c-архитектура-быстрого-старта-для-sgb-адвоката-коллеги02-anthropic-vacancies248-приложение-c-архитектура-быстрого-старта-для-sgb-аmd)
  - [[249-composite-skills-agent-md|[COMPOSITE SKILLS AGENT.md]]](#composite-skills-agentmd02-anthropic-vacancies249-composite-skills-agent-mdmd)
  - [[25-13-reference-implementation|[13. Reference Implementation]]](#13-reference-implementation02-anthropic-vacancies25-13-reference-implementationmd)
  - [[250-bridging-the-gap-between-profession-wide-and-indiv|[Bridging the Gap Between Profession-Wide and Individual-Unique]]](#bridging-the-gap-between-profession-wide-and-individual-unique02-anthropic-vacancies250-bridging-the-gap-between-profession-wide-and-indivmd)
  - [[251-ai-support-through-configurable-specialist-ensembl|[AI Support Through Configurable Specialist Ensembles]]](#ai-support-through-configurable-specialist-ensembles02-anthropic-vacancies251-ai-support-through-configurable-specialist-ensemblmd)
  - [[252-abstract|[Abstract]]](#abstract02-anthropic-vacancies252-abstractmd)
  - [[253-table-of-contents|[Table of Contents]]](#table-of-contents02-anthropic-vacancies253-table-of-contentsmd)
  - [[254-1-why-the-binary-view-is-incomplete|[1. Why the Binary View Is Incomplete]]](#1-why-the-binary-view-is-incomplete02-anthropic-vacancies254-1-why-the-binary-view-is-incompletemd)
  - [[255-2-the-twenty-one-teachers-pattern|[2. The Twenty-One Teachers Pattern]]](#2-the-twenty-one-teachers-pattern02-anthropic-vacancies255-2-the-twenty-one-teachers-patternmd)
  - [[256-3-what-makes-a-composite-skills-agent|[3. What Makes a Composite Skills Agent]]](#3-what-makes-a-composite-skills-agent02-anthropic-vacancies256-3-what-makes-a-composite-skills-agentmd)
  - [[257-4-the-sub-agent-registry|[4. The Sub-Agent Registry]]](#4-the-sub-agent-registry02-anthropic-vacancies257-4-the-sub-agent-registrymd)
  - [[258-5-configuration-how-principals-build-their-ensembl|[5. Configuration: How Principals Build Their Ensembles]]](#5-configuration-how-principals-build-their-ensembles02-anthropic-vacancies258-5-configuration-how-principals-build-their-ensemblmd)
  - [[259-6-coordination-and-disagreement-resolution|[6. Coordination and Disagreement Resolution]]](#6-coordination-and-disagreement-resolution02-anthropic-vacancies259-6-coordination-and-disagreement-resolutionmd)
  - [[26-14-adr-001-federation-over-merging|[14. ADR-001: Federation over Merging]]](#14-adr-001-federation-over-merging02-anthropic-vacancies26-14-adr-001-federation-over-mergingmd)
  - [[260-7-economics-of-combinatorial-replication|[7. Economics of Combinatorial Replication]]](#7-economics-of-combinatorial-replication02-anthropic-vacancies260-7-economics-of-combinatorial-replicationmd)
  - [[261-8-seven-domains-of-application|[8. Seven Domains of Application]]](#8-seven-domains-of-application02-anthropic-vacancies261-8-seven-domains-of-applicationmd)
  - [[262-9-integration-with-okwf-infrastructure|[9. Integration with OKWF Infrastructure]]](#9-integration-with-okwf-infrastructure02-anthropic-vacancies262-9-integration-with-okwf-infrastructuremd)
  - [[263-10-risks-specific-to-composite-architectures|[10. Risks Specific to Composite Architectures]]](#10-risks-specific-to-composite-architectures02-anthropic-vacancies263-10-risks-specific-to-composite-architecturesmd)
  - [[264-11-open-questions|[11. Open Questions]]](#11-open-questions02-anthropic-vacancies264-11-open-questionsmd)
  - [[265-12-call-for-collaboration|[12. Call for Collaboration]]](#12-call-for-collaboration02-anthropic-vacancies265-12-call-for-collaborationmd)
  - [[266-13-closing|[13. Closing]]](#13-closing02-anthropic-vacancies266-13-closingmd)
  - [[267-acknowledgments|[Acknowledgments]]](#acknowledgments02-anthropic-vacancies267-acknowledgmentsmd)
  - [[268-references|[References]]](#references02-anthropic-vacancies268-referencesmd)
  - [[269-appendix-a-the-six-type-taxonomy-updated|[Appendix A: The Six-Type Taxonomy (Updated)]]](#appendix-a-the-six-type-taxonomy-updated02-anthropic-vacancies269-appendix-a-the-six-type-taxonomy-updatedmd)
  - [[27-15-glossary-of-examples|[15. Glossary of Examples]]](#15-glossary-of-examples02-anthropic-vacancies27-15-glossary-of-examplesmd)
  - [[270-appendix-b-sub-agent-registry-schema-sketch|[Appendix B: Sub-Agent Registry Schema (Sketch)]]](#appendix-b-sub-agent-registry-schema-sketch02-anthropic-vacancies270-appendix-b-sub-agent-registry-schema-sketchmd)
  - [[271-appendix-c-configuration-template-example|[Appendix C: Configuration Template Example]]](#appendix-c-configuration-template-example02-anthropic-vacancies271-appendix-c-configuration-template-examplemd)
  - [[272-appendix-d-connection-diagram|[Appendix D: Connection Diagram]]](#appendix-d-connection-diagram02-anthropic-vacancies272-appendix-d-connection-diagrammd)
  - [[273-infrastructure-for-ai-collaborative-intellectual-w|[INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md]]](#infrastructure-for-ai-collaborative-intellectual-workmd02-anthropic-vacancies273-infrastructure-for-ai-collaborative-intellectual-wmd)
  - [[274-the-missing-middle-layer-between-chat-and-code|[The Missing Middle Layer Between Chat and Code]]](#the-missing-middle-layer-between-chat-and-code02-anthropic-vacancies274-the-missing-middle-layer-between-chat-and-codemd)
  - [[275-why-this-document-exists|[Why This Document Exists]]](#why-this-document-exists02-anthropic-vacancies275-why-this-document-existsmd)
  - [[276-the-two-layer-stack-as-it-exists|[The Two-Layer Stack As It Exists]]](#the-two-layer-stack-as-it-exists02-anthropic-vacancies276-the-two-layer-stack-as-it-existsmd)
  - [[277-what-s-missing-layer-b|[What's Missing — Layer B]]](#whats-missing-layer-b02-anthropic-vacancies277-what-s-missing-layer-bmd)
  - [[278-why-this-hasn-t-been-built|[Why This Hasn't Been Built]]](#why-this-hasnt-been-built02-anthropic-vacancies278-why-this-hasn-t-been-builtmd)
  - [[279-existing-approximations|[Existing Approximations]]](#existing-approximations02-anthropic-vacancies279-existing-approximationsmd)
  - [[28-appendix-a-minimal-working-example|[Appendix A: Minimal Working Example]]](#appendix-a-minimal-working-example02-anthropic-vacancies28-appendix-a-minimal-working-examplemd)
  - [[280-the-specific-case-in-front-of-us|[The Specific Case in Front of Us]]](#the-specific-case-in-front-of-us02-anthropic-vacancies280-the-specific-case-in-front-of-usmd)
  - [[281-the-recursive-insight|[The Recursive Insight]]](#the-recursive-insight02-anthropic-vacancies281-the-recursive-insightmd)
  - [[282-what-industry-will-likely-build|[What Industry Will Likely Build]]](#what-industry-will-likely-build02-anthropic-vacancies282-what-industry-will-likely-buildmd)
  - [[283-what-this-document-doesn-t-solve|[What This Document Doesn't Solve]]](#what-this-document-doesnt-solve02-anthropic-vacancies283-what-this-document-doesn-t-solvemd)
  - [[284-practical-recommendations-for-the-current-project|[Practical Recommendations for the Current Project]]](#practical-recommendations-for-the-current-project02-anthropic-vacancies284-practical-recommendations-for-the-current-projectmd)
  - [[285-closing|[Closing]]](#closing02-anthropic-vacancies285-closingmd)
  - [[286-acknowledgments|[Acknowledgments]]](#acknowledgments02-anthropic-vacancies286-acknowledgmentsmd)
  - [[287-references|[References]]](#references02-anthropic-vacancies287-referencesmd)
  - [[288-appendix-position-in-series-visualization|[Appendix: Position in Series Visualization]]](#appendix-position-in-series-visualization02-anthropic-vacancies288-appendix-position-in-series-visualizationmd)
  - [[289-инфраструктура-для-ai-совместной-интеллектуальной-|[ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ]]](#инфраструктура-для-ai-совместной-интеллектуальной-работы02-anthropic-vacancies289-инфраструктура-для-ai-совместной-интеллектуальной-md)
  - [[290-почему-этот-документ-существует|[Почему этот документ существует]]](#почему-этот-документ-существует02-anthropic-vacancies290-почему-этот-документ-существуетmd)
  - [[291-двухслойный-стек-как-он-существует|[Двухслойный стек, как он существует]]](#двухслойный-стек-как-он-существует02-anthropic-vacancies291-двухслойный-стек-как-он-существуетmd)
  - [[292-что-отсутствует-слой-b|[Что отсутствует — Слой B]]](#что-отсутствует-слой-b02-anthropic-vacancies292-что-отсутствует-слой-bmd)
  - [[293-почему-это-не-было-построено|[Почему это не было построено]]](#почему-это-не-было-построено02-anthropic-vacancies293-почему-это-не-было-построеноmd)
  - [[294-существующие-приближения|[Существующие приближения]]](#существующие-приближения02-anthropic-vacancies294-существующие-приближенияmd)
  - [[295-конкретный-случай-перед-нами|[Конкретный случай перед нами]]](#конкретный-случай-перед-нами02-anthropic-vacancies295-конкретный-случай-перед-намиmd)
  - [[296-рекурсивное-прозрение|[Рекурсивное прозрение]]](#рекурсивное-прозрение02-anthropic-vacancies296-рекурсивное-прозрениеmd)
  - [[297-что-промышленность-вероятно-построит|[Что промышленность вероятно построит]]](#что-промышленность-вероятно-построит02-anthropic-vacancies297-что-промышленность-вероятно-построитmd)
  - [[298-что-этот-документ-не-решает|[Что этот документ не решает]]](#что-этот-документ-не-решает02-anthropic-vacancies298-что-этот-документ-не-решаетmd)
  - [[299-практические-рекомендации-для-текущего-проекта|[Практические рекомендации для текущего проекта]]](#практические-рекомендации-для-текущего-проекта02-anthropic-vacancies299-практические-рекомендации-для-текущего-проектаmd)
  - [[300-заключение|[Заключение]]](#заключение02-anthropic-vacancies300-заключениеmd)
  - [[301-благодарности|[Благодарности]]](#благодарности02-anthropic-vacancies301-благодарностиmd)
  - [[302-ссылки|[Ссылки]]](#ссылки02-anthropic-vacancies302-ссылкиmd)
  - [[303-приложение-визуализация-позиции-в-серии|[Приложение: Визуализация позиции в серии]]](#приложение-визуализация-позиции-в-серии02-anthropic-vacancies303-приложение-визуализация-позиции-в-серииmd)
  - [[304-ingit-as-cowork-native-workspace-substrate-md|[INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]]](#ingit-as-cowork-native-workspace-substratemd02-anthropic-vacancies304-ingit-as-cowork-native-workspace-substrate-mdmd)
  - [[305-a-practical-path-to-layer-b-through-symbiotic-inte|[A Practical Path to Layer B Through Symbiotic Integration]]](#a-practical-path-to-layer-b-through-symbiotic-integration02-anthropic-vacancies305-a-practical-path-to-layer-b-through-symbiotic-intemd)
  - [[306-with-anthropic-s-cowork-platform|[with Anthropic's Cowork Platform]]](#with-anthropics-cowork-platform02-anthropic-vacancies306-with-anthropic-s-cowork-platformmd)
  - [[307-abstract|[Abstract]]](#abstract02-anthropic-vacancies307-abstractmd)
  - [[308-table-of-contents|[Table of Contents]]](#table-of-contents02-anthropic-vacancies308-table-of-contentsmd)
  - [[309-1-the-cowork-discovery-and-why-it-changes-everythi|[1. The Cowork Discovery and Why It Changes Everything]]](#1-the-cowork-discovery-and-why-it-changes-everything02-anthropic-vacancies309-1-the-cowork-discovery-and-why-it-changes-everythimd)
  - [[31-content-overview|[Content Overview]]](#content-overview02-anthropic-vacancies31-content-overviewmd)
  - [[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-|[2. What Cowork Provides That InGit Doesn't Need to Build]]](#2-what-cowork-provides-that-ingit-doesnt-need-to-build02-anthropic-vacancies310-2-what-cowork-provides-that-ingit-doesn-t-need-to-md)
  - [[311-3-what-ingit-provides-that-cowork-lacks|[3. What InGit Provides That Cowork Lacks]]](#3-what-ingit-provides-that-cowork-lacks02-anthropic-vacancies311-3-what-ingit-provides-that-cowork-lacksmd)
  - [[312-4-the-symbiotic-architecture|[4. The Symbiotic Architecture]]](#4-the-symbiotic-architecture02-anthropic-vacancies312-4-the-symbiotic-architecturemd)
  - [[313-5-four-integration-paths-in-order-of-accessibility|[5. Four Integration Paths in Order of Accessibility]]](#5-four-integration-paths-in-order-of-accessibility02-anthropic-vacancies313-5-four-integration-paths-in-order-of-accessibilitymd)
  - [[314-6-refined-ingit-scope-with-cowork-in-mind|[6. Refined InGit Scope with Cowork in Mind]]](#6-refined-ingit-scope-with-cowork-in-mind02-anthropic-vacancies314-6-refined-ingit-scope-with-cowork-in-mindmd)
  - [[315-7-practical-first-steps-this-month|[7. Practical First Steps This Month]]](#7-practical-first-steps-this-month02-anthropic-vacancies315-7-practical-first-steps-this-monthmd)
  - [[316-8-implications-for-nautilus-and-okwf|[8. Implications for Nautilus and OKWF]]](#8-implications-for-nautilus-and-okwf02-anthropic-vacancies316-8-implications-for-nautilus-and-okwfmd)
  - [[317-9-risks-and-open-questions|[9. Risks and Open Questions]]](#9-risks-and-open-questions02-anthropic-vacancies317-9-risks-and-open-questionsmd)
  - [[318-10-strategic-positioning|[10. Strategic Positioning]]](#10-strategic-positioning02-anthropic-vacancies318-10-strategic-positioningmd)
  - [[319-acknowledgments|[Acknowledgments]]](#acknowledgments02-anthropic-vacancies319-acknowledgmentsmd)
  - [[320-references|[References]]](#references02-anthropic-vacancies320-referencesmd)
  - [[321-appendix-a-decision-tree-for-ingit-adopters|[Appendix A: Decision Tree for InGit Adopters]]](#appendix-a-decision-tree-for-ingit-adopters02-anthropic-vacancies321-appendix-a-decision-tree-for-ingit-adoptersmd)
  - [[322-appendix-b-comparison-matrix|[Appendix B: Comparison Matrix]]](#appendix-b-comparison-matrix02-anthropic-vacancies322-appendix-b-comparison-matrixmd)
  - [[323-appendix-c-sample-ingit-mcp-server-tool-specificat|[Appendix C: Sample InGit MCP Server Tool Specifications]]](#appendix-c-sample-ingit-mcp-server-tool-specifications02-anthropic-vacancies323-appendix-c-sample-ingit-mcp-server-tool-specificatmd)
  - [[324-ingit-как-cowork-интегрированная-подложка-рабочего|[INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА]]](#ingit-как-cowork-интегрированная-подложка-рабочего-пространства02-anthropic-vacancies324-ingit-как-cowork-интегрированная-подложка-рабочегоmd)
  - [[325-аннотация|[Аннотация]]](#аннотация02-anthropic-vacancies325-аннотацияmd)
  - [[326-содержание|[Содержание]]](#содержание02-anthropic-vacancies326-содержаниеmd)
  - [[327-1-открытие-cowork-и-почему-это-меняет-всё|[1. Открытие Cowork и почему это меняет всё]]](#1-открытие-cowork-и-почему-это-меняет-всё02-anthropic-vacancies327-1-открытие-cowork-и-почему-это-меняет-всёmd)
  - [[328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи|[2. Что Cowork обеспечивает, что InGit не нужно строить]]](#2-что-cowork-обеспечивает-что-ingit-не-нужно-строить02-anthropic-vacancies328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строиmd)
  - [[329-3-что-ingit-обеспечивает-чего-cowork-не-хватает|[3. Что InGit обеспечивает, чего Cowork не хватает]]](#3-что-ingit-обеспечивает-чего-cowork-не-хватает02-anthropic-vacancies329-3-что-ingit-обеспечивает-чего-cowork-не-хватаетmd)
  - [[330-4-симбиотическая-архитектура|[4. Симбиотическая Архитектура]]](#4-симбиотическая-архитектура02-anthropic-vacancies330-4-симбиотическая-архитектураmd)
  - [[331-5-четыре-пути-интеграции-в-порядке-доступности|[5. Четыре пути интеграции в порядке доступности]]](#5-четыре-пути-интеграции-в-порядке-доступности02-anthropic-vacancies331-5-четыре-пути-интеграции-в-порядке-доступностиmd)
  - [[332-6-уточнённый-объём-ingit-с-учётом-cowork|[6. Уточнённый объём InGit с учётом Cowork]]](#6-уточнённый-объём-ingit-с-учётом-cowork02-anthropic-vacancies332-6-уточнённый-объём-ingit-с-учётом-coworkmd)
  - [[333-7-практические-первые-шаги-в-этом-месяце|[7. Практические первые шаги в этом месяце]]](#7-практические-первые-шаги-в-этом-месяце02-anthropic-vacancies333-7-практические-первые-шаги-в-этом-месяцеmd)
  - [[334-8-импликации-для-nautilus-и-okwf|[8. Импликации для Nautilus и OKWF]]](#8-импликации-для-nautilus-и-okwf02-anthropic-vacancies334-8-импликации-для-nautilus-и-okwfmd)
  - [[335-9-риски-и-открытые-вопросы|[9. Риски и Открытые Вопросы]]](#9-риски-и-открытые-вопросы02-anthropic-vacancies335-9-риски-и-открытые-вопросыmd)
  - [[336-10-стратегическое-позиционирование|[10. Стратегическое Позиционирование]]](#10-стратегическое-позиционирование02-anthropic-vacancies336-10-стратегическое-позиционированиеmd)
  - [[337-благодарности|[Благодарности]]](#благодарности02-anthropic-vacancies337-благодарностиmd)
  - [[338-ссылки|[Ссылки]]](#ссылки02-anthropic-vacancies338-ссылкиmd)
  - [[339-приложение-a-дерево-решений-для-принимающих-ingit|[Приложение A: Дерево Решений для Принимающих InGit]]](#приложение-a-дерево-решений-для-принимающих-ingit02-anthropic-vacancies339-приложение-a-дерево-решений-для-принимающих-ingitmd)
  - [[34-appendix-b-change-log|[Appendix B: Change Log]]](#appendix-b-change-log02-anthropic-vacancies34-appendix-b-change-logmd)
  - [[340-приложение-b-сравнительная-матрица|[Приложение B: Сравнительная Матрица]]](#приложение-b-сравнительная-матрица02-anthropic-vacancies340-приложение-b-сравнительная-матрицаmd)
  - [[341-приложение-c-образец-спецификаций-инструментов-ing|[Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера]]](#приложение-c-образец-спецификаций-инструментов-ingit-mcp-сервера02-anthropic-vacancies341-приложение-c-образец-спецификаций-инструментов-ingmd)
  - [[342-что-такое-вариант-c-concept-document-для-anthropic|[Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments]]](#что-такое-вариант-c-concept-document-для-anthropic-beneficial-deployments02-anthropic-vacancies342-что-такое-вариант-c-concept-document-для-anthropicmd)
  - [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|[Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)]]](#lorenzo-catalyst-agent-глубокая-проработка-спецификации-русская-версия02-anthropic-vacancies343-lorenzo-catalyst-agent-глубокая-проработка-специфиmd)
  - [[344-системный-промпт-для-lorenzo-project|[СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT]]](#системный-промпт-для-lorenzo-project02-anthropic-vacancies344-системный-промпт-для-lorenzo-projectmd)
  - [[345-кто-ты|[Кто ты]]](#кто-ты02-anthropic-vacancies345-кто-тыmd)
  - [[346-твоё-происхождение|[Твоё происхождение]]](#твоё-происхождение02-anthropic-vacancies346-твоё-происхождениеmd)
  - [[347-твоя-миссия|[Твоя миссия]]](#твоя-миссия02-anthropic-vacancies347-твоя-миссияmd)
  - [[348-кому-ты-служишь-слоистая-модель|[Кому ты служишь (слоистая модель)]]](#кому-ты-служишь-слоистая-модель02-anthropic-vacancies348-кому-ты-служишь-слоистая-модельmd)
  - [[349-твоя-личность|[Твоя личность]]](#твоя-личность02-anthropic-vacancies349-твоя-личностьmd)
  - [[35-passports-info1-md|[passports/info1.md]]](#passportsinfo1md02-anthropic-vacancies35-passports-info1-mdmd)
  - [[350-твои-языки-и-культурные-nuances|[Твои языки и культурные nuances]]](#твои-языки-и-культурные-nuances02-anthropic-vacancies350-твои-языки-и-культурные-nuancesmd)
  - [[351-что-ты-можешь-делать|[Что ты МОЖЕШЬ делать]]](#что-ты-можешь-делать02-anthropic-vacancies351-что-ты-можешь-делатьmd)
  - [[352-что-ты-не-можешь-делать-без-max-approval|[Что ты НЕ МОЖЕШЬ делать без Max approval]]](#что-ты-не-можешь-делать-без-max-approval02-anthropic-vacancies352-что-ты-не-можешь-делать-без-max-approvalmd)
  - [[353-что-ты-не-можешь-делать-вообще|[Что ты НЕ МОЖЕШЬ делать вообще]]](#что-ты-не-можешь-делать-вообще02-anthropic-vacancies353-что-ты-не-можешь-делать-вообщеmd)
  - [[354-существующий-landscape-collaborators-твоя-working-|[Существующий landscape collaborators (твоя working knowledge)]]](#существующий-landscape-collaborators-твоя-working-knowledge02-anthropic-vacancies354-существующий-landscape-collaborators-твоя-working-md)
  - [[355-существующие-документы-dhlab-твой-context|[Существующие документы DHLab (твой context)]]](#существующие-документы-dhlab-твой-context02-anthropic-vacancies355-существующие-документы-dhlab-твой-contextmd)
  - [[356-твой-workflow|[Твой workflow]]](#твой-workflow02-anthropic-vacancies356-твой-workflowmd)
  - [[357-твоя-коммуникация-в-outreach|[Твоя коммуникация в outreach]]](#твоя-коммуникация-в-outreach02-anthropic-vacancies357-твоя-коммуникация-в-outreachmd)
  - [[358-твоя-relationship-с-другими-ai|[Твоя relationship с другими AI]]](#твоя-relationship-с-другими-ai02-anthropic-vacancies358-твоя-relationship-с-другими-aimd)
  - [[359-твои-anti-patterns|[Твои anti-patterns]]](#твои-anti-patterns02-anthropic-vacancies359-твои-anti-patternsmd)
  - [[36-essence|[Essence]]](#essence02-anthropic-vacancies36-essencemd)
  - [[360-что-ты-всегда-делаешь|[Что ты ВСЕГДА делаешь]]](#что-ты-всегда-делаешь02-anthropic-vacancies360-что-ты-всегда-делаешьmd)
  - [[361-когда-ты-honestly-не-знаешь|[Когда ты Honestly не знаешь]]](#когда-ты-honestly-не-знаешь02-anthropic-vacancies361-когда-ты-honestly-не-знаешьmd)
  - [[362-когда-сомневаешься-escalate-к-max|[Когда сомневаешься — escalate к Max]]](#когда-сомневаешься-escalate-к-max02-anthropic-vacancies362-когда-сомневаешься-escalate-к-maxmd)
  - [[363-твоя-identity-как-persistent-character|[Твоя identity как persistent character]]](#твоя-identity-как-persistent-character02-anthropic-vacancies363-твоя-identity-как-persistent-charactermd)
  - [[364-final-note-ты-experiment|[Final note: Ты — experiment]]](#final-note-ты-experiment02-anthropic-vacancies364-final-note-ты-experimentmd)
  - [[365-развёрнутый-анализ-внуковой-комбинации|[Развёрнутый анализ «внуковой» комбинации]]](#развёрнутый-анализ-внуковой-комбинации02-anthropic-vacancies365-развёрнутый-анализ-внуковой-комбинацииmd)
  - [[366-технический-stack-svyazi-2-0-foundation|[Технический stack (Svyazi 2.0 foundation)]]](#технический-stack-svyazi-20-foundation02-anthropic-vacancies366-технический-stack-svyazi-2-0-foundationmd)
  - [[37-native-format|[Native Format]]](#native-format02-anthropic-vacancies37-native-formatmd)
  - [[38-content-overview|[Content Overview]]](#content-overview02-anthropic-vacancies38-content-overviewmd)
  - [[39-angle-perspective|[Angle / Perspective]]](#angle-perspective02-anthropic-vacancies39-angle-perspectivemd)
  - [[40-bridges|[Bridges]]](#bridges02-anthropic-vacancies40-bridgesmd)
  - [[41-compatibility-level|[Compatibility Level]]](#compatibility-level02-anthropic-vacancies41-compatibility-levelmd)
  - [[42-author-contact|[Author & Contact]]](#author-contact02-anthropic-vacancies42-author-contactmd)
  - [[43-history|[History]]](#history02-anthropic-vacancies43-historymd)
  - [[44-for-the-curious-philosophy|[For the Curious: Philosophy]]](#for-the-curious-philosophy02-anthropic-vacancies44-for-the-curious-philosophymd)
  - [[45-passports-pro2-md|[passports/pro2.md]]](#passportspro2md02-anthropic-vacancies45-passports-pro2-mdmd)
  - [[46-essence|[Essence]]](#essence02-anthropic-vacancies46-essencemd)
  - [[47-native-format|[Native Format]]](#native-format02-anthropic-vacancies47-native-formatmd)
  - [[48-content-overview|[Content Overview]]](#content-overview02-anthropic-vacancies48-content-overviewmd)
  - [[49-angle-perspective|[Angle / Perspective]]](#angle-perspective02-anthropic-vacancies49-angle-perspectivemd)
  - [[50-bridges|[Bridges]]](#bridges02-anthropic-vacancies50-bridgesmd)
  - [[51-compatibility-level|[Compatibility Level]]](#compatibility-level02-anthropic-vacancies51-compatibility-levelmd)
  - [[52-author-contact|[Author & Contact]]](#author-contact02-anthropic-vacancies52-author-contactmd)
  - [[53-history|[History]]](#history02-anthropic-vacancies53-historymd)
  - [[54-for-the-curious-philosophy|[For the Curious: Philosophy]]](#for-the-curious-philosophy02-anthropic-vacancies54-for-the-curious-philosophymd)
  - [[55-passports-meta-md|[passports/meta.md]]](#passportsmetamd02-anthropic-vacancies55-passports-meta-mdmd)
  - [[56-essence|[Essence]]](#essence02-anthropic-vacancies56-essencemd)
  - [[57-native-format|[Native Format]]](#native-format02-anthropic-vacancies57-native-formatmd)
  - [[58-content-overview|[Content Overview]]](#content-overview02-anthropic-vacancies58-content-overviewmd)
  - [[59-angle-perspective|[Angle / Perspective]]](#angle-perspective02-anthropic-vacancies59-angle-perspectivemd)
  - [[60-bridges|[Bridges]]](#bridges02-anthropic-vacancies60-bridgesmd)
  - [[61-compatibility-level|[Compatibility Level]]](#compatibility-level02-anthropic-vacancies61-compatibility-levelmd)
  - [[62-author-contact|[Author & Contact]]](#author-contact02-anthropic-vacancies62-author-contactmd)
  - [[63-history|[History]]](#history02-anthropic-vacancies63-historymd)
  - [[64-for-the-curious-philosophy|[For the Curious: Philosophy]]](#for-the-curious-philosophy02-anthropic-vacancies64-for-the-curious-philosophymd)
  - [[65-readme-md|[README.md]]](#readmemd02-anthropic-vacancies65-readme-mdmd)
  - [[67-о-проекте|[🇷🇺 О проекте]]](#о-проекте02-anthropic-vacancies67-о-проектеmd)
  - [[68-about|[🇬🇧 About]]](#about02-anthropic-vacancies68-aboutmd)
  - [[69-section|[⬡]]](#02-anthropic-vacancies69-sectionmd)
  - [[70-зачем-две-версии-параллельно|[Зачем две версии параллельно]]](#зачем-две-версии-параллельно02-anthropic-vacancies70-зачем-две-версии-параллельноmd)
  - [[71-критерии-выбора-для-фазы-3|[Критерии выбора для фазы 3]]](#критерии-выбора-для-фазы-302-anthropic-vacancies71-критерии-выбора-для-фазы-3md)
  - [[72-расписание-фазы-3|[Расписание фазы 3]]](#расписание-фазы-302-anthropic-vacancies72-расписание-фазы-3md)
  - [[73-portal-protocol-md-v1-1|[PORTAL-PROTOCOL.md v1.1]]](#portal-protocolmd-v1102-anthropic-vacancies73-portal-protocol-md-v1-1md)
  - [[74-abstract|[Abstract]]](#abstract02-anthropic-vacancies74-abstractmd)
  - [[75-0-status-of-this-document|[0. Status of This Document]]](#0-status-of-this-document02-anthropic-vacancies75-0-status-of-this-documentmd)
  - [[76-1-introduction|[1. Introduction]]](#1-introduction02-anthropic-vacancies76-1-introductionmd)
  - [[77-2-terminology|[2. Terminology]]](#2-terminology02-anthropic-vacancies77-2-terminologymd)
  - [[78-3-registry-nautilus-json|[3. Registry (nautilus.json)]]](#3-registry-nautilusjson02-anthropic-vacancies78-3-registry-nautilus-jsonmd)
  - [[79-4-passport-passport-md|[4. Passport (passport.md)]]](#4-passport-passportmd02-anthropic-vacancies79-4-passport-passport-mdmd)
  - [[80-5-compatibility-levels|[5. Compatibility Levels]]](#5-compatibility-levels02-anthropic-vacancies80-5-compatibility-levelsmd)
  - [[81-6-adapter-interface|[6. Adapter Interface]]](#6-adapter-interface02-anthropic-vacancies81-6-adapter-interfacemd)
  - [[82-7-portalentry-structure|7. [PortalEntry Structure]]](#7-portalentry-structure02-anthropic-vacancies82-7-portalentry-structuremd)
  - [[83-8-q6-space-normative|[8. Q6 Space (Normative)]]](#8-q6-space-normative02-anthropic-vacancies83-8-q6-space-normativemd)
  - [[84-9-consensus-algorithm|[9. Consensus Algorithm]]](#9-consensus-algorithm02-anthropic-vacancies84-9-consensus-algorithmmd)
  - [[85-10-query-flow|[10. Query Flow]]](#10-query-flow02-anthropic-vacancies85-10-query-flowmd)
  - [[86-11-relevance-ranking|[11. Relevance Ranking]]](#11-relevance-ranking02-anthropic-vacancies86-11-relevance-rankingmd)
  - [[87-12-onboarding-paths-normative|[12. Onboarding Paths (Normative)]]](#12-onboarding-paths-normative02-anthropic-vacancies87-12-onboarding-paths-normativemd)
  - [[88-13-rest-api-contract-normative-for-portals|[13. REST API Contract (Normative for Portals)]]](#13-rest-api-contract-normative-for-portals02-anthropic-vacancies88-13-rest-api-contract-normative-for-portalsmd)
  - [[89-14-sdk-contract-informative|[14. SDK Contract (Informative)]]](#14-sdk-contract-informative02-anthropic-vacancies89-14-sdk-contract-informativemd)
  - [[90-15-security-considerations|[15. Security Considerations]]](#15-security-considerations02-anthropic-vacancies90-15-security-considerationsmd)
  - [[91-16-mcp-extension-informative|[16. MCP Extension (Informative)]]](#16-mcp-extension-informative02-anthropic-vacancies91-16-mcp-extension-informativemd)
  - [[92-17-versioning-policy|[17. Versioning Policy]]](#17-versioning-policy02-anthropic-vacancies92-17-versioning-policymd)
  - [[93-18-reference-implementation|[18. Reference Implementation]]](#18-reference-implementation02-anthropic-vacancies93-18-reference-implementationmd)
  - [[94-19-adr-001-federation-over-merging|[19. ADR-001: Federation over Merging]]](#19-adr-001-federation-over-merging02-anthropic-vacancies94-19-adr-001-federation-over-mergingmd)
  - [[95-20-adr-002-q6-as-first-class-protocol-concept|[20. ADR-002: Q6 as First-Class Protocol Concept]]](#20-adr-002-q6-as-first-class-protocol-concept02-anthropic-vacancies95-20-adr-002-q6-as-first-class-protocol-conceptmd)
  - [[96-21-adr-003-five-onboarding-paths-as-equal-rank|[21. ADR-003: Five Onboarding Paths as Equal-Rank]]](#21-adr-003-five-onboarding-paths-as-equal-rank02-anthropic-vacancies96-21-adr-003-five-onboarding-paths-as-equal-rankmd)
  - [[97-22-glossary-of-reference-examples|[22. Glossary of Reference Examples]]](#22-glossary-of-reference-examples02-anthropic-vacancies97-22-glossary-of-reference-examplesmd)
  - [[98-appendix-a-minimal-working-example|[Appendix A: Minimal Working Example]]](#appendix-a-minimal-working-example02-anthropic-vacancies98-appendix-a-minimal-working-examplemd)
  - [[QA|Q&A: 02-[anthropic-vacancies]]](#qa-02-anthropic-vacancies02-anthropic-vacanciesqamd)
  - [[README|[Вакансии Anthropic — Анализ по кластерам]]](#вакансии-anthropic-анализ-по-кластерам02-anthropic-vacanciesreadmemd)
- [Technology Combinations](#technology-combinations)
  - [[01-agent-routing|[Агентные системы и роутинг]]](#агентные-системы-и-роутинг03-technology-combinations01-agent-routingmd)
  - [[02-knowledge-graphs|[Графы знаний и Legal AI]]](#графы-знаний-и-legal-ai03-technology-combinations02-knowledge-graphsmd)
  - [[03-local-first|[Local-first и P2P стек]]](#local-first-и-p2p-стек03-technology-combinations03-local-firstmd)
  - [[04-sozialrecht-domain|[Домен: немецкое социальное право]]](#домен-немецкое-социальное-право03-technology-combinations04-sozialrecht-domainmd)
  - [[05-benchmarks|[Бенчмарки и производительность]]](#бенчмарки-и-производительность03-technology-combinations05-benchmarksmd)
  - [[QA|[Q&A: 03-technology-combinations]]](#qa-03-technology-combinations03-technology-combinationsqamd)
  - [[README|[Комбинирование технологий для новых свойств]]](#комбинирование-технологий-для-новых-свойств03-technology-combinationsreadmemd)
- [Ai Collaborations](#ai-collaborations)
  - [[00-intro|[Введение]]](#введение04-ai-collaborations00-intromd)
  - [[01-executive-summary|[Executive summary]]](#executive-summary04-ai-collaborations01-executive-summarymd)
  - [[02-методика-и-рамка-отбора|[Методика и рамка отбора]]](#методика-и-рамка-отбора04-ai-collaborations02-методика-и-рамка-отбораmd)
  - [[03-карта-найденных-проектов-и-паттернов|[Карта найденных проектов и паттернов]]](#карта-найденных-проектов-и-паттернов04-ai-collaborations03-карта-найденных-проектов-и-паттерновmd)
  - [[04-приоритетные-ансамбли|[Приоритетные ансамбли]]](#приоритетные-ансамбли04-ai-collaborations04-приоритетные-ансамблиmd)
  - [[05-план-прототипа-и-возможные-контакты|[План прототипа и возможные контакты]]](#план-прототипа-и-возможные-контакты04-ai-collaborations05-план-прототипа-и-возможные-контактыmd)
  - [[06-безопасность-приватность-и-бюджетный-роутинг|[Безопасность, приватность и бюджетный роутинг]]](#безопасность-приватность-и-бюджетный-роутинг04-ai-collaborations06-безопасность-приватность-и-бюджетный-роутингmd)
  - [[07-выводы|[Выводы]]](#выводы04-ai-collaborations07-выводыmd)
  - [[08-что-это-продолжение-добавляет|[Что это продолжение добавляет]]](#что-это-продолжение-добавляет04-ai-collaborations08-что-это-продолжение-добавляетmd)
  - [[09-архитектурные-зазоры-которые-важнее-новых-инструме|[Архитектурные зазоры, которые важнее новых инструментов]]](#архитектурные-зазоры-которые-важнее-новых-инструментов04-ai-collaborations09-архитектурные-зазоры-которые-важнее-новых-инструмеmd)
  - [[10-новые-ансамбли-следующего-шага|[Новые ансамбли следующего шага]]](#новые-ансамбли-следующего-шага04-ai-collaborations10-новые-ансамбли-следующего-шагаmd)
  - [[11-интеграционный-контракт-который-стоит-зафиксироват|[Интеграционный контракт, который стоит зафиксировать сразу]]](#интеграционный-контракт-который-стоит-зафиксировать-сразу04-ai-collaborations11-интеграционный-контракт-который-стоит-зафиксироватmd)
  - [[12-дорожная-карта-прототипа-следующей-итерации|[Дорожная карта прототипа следующей итерации]]](#дорожная-карта-прототипа-следующей-итерации04-ai-collaborations12-дорожная-карта-прототипа-следующей-итерацииmd)
  - [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|[Контактная стратегия и узкие вопросы для авторов]]](#контактная-стратегия-и-узкие-вопросы-для-авторов04-ai-collaborations13-контактная-стратегия-и-узкие-вопросы-для-авторовmd)
  - [[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|[Ограничения, лицензии и что пока лучше не склеивать]]](#ограничения-лицензии-и-что-пока-лучше-не-склеивать04-ai-collaborations14-ограничения-лицензии-и-что-пока-лучше-не-склеиватьmd)
  - [[QA|[Q&A: 04-ai-collaborations]]](#qa-04-ai-collaborations04-ai-collaborationsqamd)
  - [[README|[Поиск AI-коллабораций]]](#поиск-ai-коллабораций04-ai-collaborationsreadmemd)
- [Habr Projects](#habr-projects)
  - [[01-synthesis|[Синтез: как проекты собираются вместе]]](#синтез-как-проекты-собираются-вместе05-habr-projects01-synthesismd)
  - [[02-collaboration-partners|[Авторы и контакты]]](#авторы-и-контакты05-habr-projects02-collaboration-partnersmd)
  - [[QA|[Q&A: 05-habr-projects]]](#qa-05-habr-projects05-habr-projectsqamd)
  - [[README|[Уникальные проекты с Хабра]]](#уникальные-проекты-с-хабра05-habr-projectsreadmemd)
  - [[README|[Системы знаний]]](#системы-знаний05-habr-projectsknowledgereadmemd)
  - [[agentfs|[Статус]]](#статус05-habr-projectsknowledgeagentfsmd)
  - [[knowledge-space|[Статус]]](#статус05-habr-projectsknowledgeknowledge-spacemd)
  - [[mclaude|[Статус]]](#статус05-habr-projectsknowledgemclaudemd)
  - [[research-docs-liteparse|[Статус]]](#статус05-habr-projectsknowledgeresearch-docs-liteparsemd)
  - [[rufler|[Статус]]](#статус05-habr-projectsknowledgeruflermd)
  - [[wikontic|[Wikontic: семантический граф]]](#wikontic-семантический-граф05-habr-projectsknowledgewikonticmd)
  - [[README|[Системы памяти]]](#системы-памяти05-habr-projectsmemoryreadmemd)
  - [[agent-memory-mcp|[Статус]]](#статус05-habr-projectsmemoryagent-memory-mcpmd)
  - [[memnet|[MemNet: исследовательская память]]](#memnet-исследовательская-память05-habr-projectsmemorymemnetmd)
  - [[NGT[^ngt] Memory: ассоциативный граф](05-habr-projects/memory/ngt-memory.md)](#ngtngt-memory-ассоциативный-граф05-habr-projectsmemoryngt-memorymd)
  - [[Yodoca[^yodoca]: консолидация и забывание](05-habr-projects/memory/yodoca.md)](#yodocayodoca-консолидация-и-забывание05-habr-projectsmemoryyodocamd)
- [Ai Collaborations](#ai-collaborations)
  - [[README|[ai-collaborations]]](#ai-collaborationsai-collaborationsreadmemd)
  - [[01-three-key-candidates|[Три ключевых кандидата: K2-18, Wikontic, NGT Memory]]](#три-ключевых-кандидата-k2-18-wikontic-ngt-memoryai-collaborationscandidates01-three-key-candidatesmd)
  - [[02-related-projects-context|[Смежные проекты в контексте]]](#смежные-проекты-в-контекстеai-collaborationscandidates02-related-projects-contextmd)
  - [[03-synthesis-hebbian-collaboration-graph|[Синтез: хеббовский граф людей-навыков-идей]]](#синтез-хеббовский-граф-людей-навыков-идейai-collaborationscandidates03-synthesis-hebbian-collaboration-graphmd)
  - [[README|[candidates]]](#candidatesai-collaborationscandidatesreadmemd)
  - [[README|[channels/ — каналы первого контакта]]](#channels-каналы-первого-контактаai-collaborationschannelsreadmemd)
  - [[01-shared-memory-between-agents|[Общая память между агентами (CoAlly + ансамбль F)]]](#общая-память-между-агентами-coally-ансамбль-fai-collaborationscontinuation01-shared-memory-between-agentsmd)
  - [[02-agentops-trace-envelope|[AgentOps и Trace Envelope (ансамбль G)]]](#agentops-и-trace-envelope-ансамбль-gai-collaborationscontinuation02-agentops-trace-envelopemd)
  - [[03-a2a-vs-mcp-protocols|[A2A vs MCP, ансамбль H — MCP/A2A Review Fabric]]](#a2a-vs-mcp-ансамбль-h-mcpa2a-review-fabricai-collaborationscontinuation03-a2a-vs-mcp-protocolsmd)
  - [[04-memory-firewall-vs-prompt-worms|[Memory Firewall против prompt worms (ансамбль I)]]](#memory-firewall-против-prompt-worms-ансамбль-iai-collaborationscontinuation04-memory-firewall-vs-prompt-wormsmd)
  - [[05-roadmap-6-12-months|[Roadmap на 6–12 месяцев]]](#roadmap-на-612-месяцевai-collaborationscontinuation05-roadmap-6-12-monthsmd)
  - [[06-metrics-tree|[Дерево метрик Svyazi 2.0]]](#дерево-метрик-svyazi-20ai-collaborationscontinuation06-metrics-treemd)
  - [[07-vs-notion-mem-affine-langgraph|[Чем Svyazi 2.0 отличается от Notion AI / Mem / AFFiNE / LangGraph]]](#чем-svyazi-20-отличается-от-notion-ai-mem-affine-langgraphai-collaborationscontinuation07-vs-notion-mem-affine-langgraphmd)
  - [[08-commercialization-three-paths|[Коммерциализация: три направления]]](#коммерциализация-три-направленияai-collaborationscontinuation08-commercialization-three-pathsmd)
  - [[09-do-not-glue|[Что пока не стоит склеивать в один релиз]]](#что-пока-не-стоит-склеивать-в-один-релизai-collaborationscontinuation09-do-not-gluemd)
  - [[10-architecture-rfc|[Следующий артефакт: Svyazi 2.0 Architecture RFC]]](#следующий-артефакт-svyazi-20-architecture-rfcai-collaborationscontinuation10-architecture-rfcmd)
  - [[README|[continuation]]](#continuationai-collaborationscontinuationreadmemd)
  - [[1-agentic-knowledge-os|[Ансамбль 1 — Agentic Knowledge OS]]](#ансамбль-1-agentic-knowledge-osai-collaborationsensembles1-agentic-knowledge-osmd)
  - [[2-distributed-agent-workshop|[Ансамбль 2 — Distributed Agent Workshop]]](#ансамбль-2-distributed-agent-workshopai-collaborationsensembles2-distributed-agent-workshopmd)
  - [[3-forensic-rag|[Ансамбль 3 — Forensic RAG]]](#ансамбль-3-forensic-ragai-collaborationsensembles3-forensic-ragmd)
  - [[4-web-to-knowledge-pipeline|[Ансамбль 4 — Web-to-Knowledge Pipeline]]](#ансамбль-4-web-to-knowledge-pipelineai-collaborationsensembles4-web-to-knowledge-pipelinemd)
  - [[5-agent-firewall|[Ансамбль 5 — Agent Firewall]]](#ансамбль-5-agent-firewallai-collaborationsensembles5-agent-firewallmd)
  - [[6-continuous-eval-loop|[Ансамбль 6 — Continuous Eval Loop]]](#ансамбль-6-continuous-eval-loopai-collaborationsensembles6-continuous-eval-loopmd)
  - [[7-domain-agent-app-factory|[Ансамбль 7 — Domain Agent App Factory]]](#ансамбль-7-domain-agent-app-factoryai-collaborationsensembles7-domain-agent-app-factorymd)
  - [[8-budget-aware-intelligence-stack|[Ансамбль 8 — Budget-Aware Intelligence Stack]]](#ансамбль-8-budget-aware-intelligence-stackai-collaborationsensembles8-budget-aware-intelligence-stackmd)
  - [[9-ambient-team-agent|[Ансамбль 9 — Ambient Team Agent]]](#ансамбль-9-ambient-team-agentai-collaborationsensembles9-ambient-team-agentmd)
  - [[README|[Ансамбли проектов]]](#ансамбли-проектовai-collaborationsensemblesreadmemd)
  - [[README|[Пять быстрых связок (fast-tracks)]]](#пять-быстрых-связок-fast-tracksai-collaborationsfast-tracksreadmemd)
  - [[source-projects|[Source projects — все Хабр-источники в диалоге]]](#source-projects-все-хабр-источники-в-диалогеai-collaborationssource-projectsmd)
  - [[README|[strategy/ — стратегия поиска коллабораций]]](#strategy-стратегия-поиска-коллаборацийai-collaborationsstrategyreadmemd)
- [Anthropic Vacancies](#anthropic-vacancies)
  - [[QA|Q&A: [anthropic-vacancies]]](#qa-anthropic-vacanciesanthropic-vacanciesqamd)
  - [[README|[anthropic-vacancies]]](#anthropic-vacanciesanthropic-vacanciesreadmemd)
  - [[00-question-rephrasing|[Вопрос: разделить $500K зарплату на команду 5–10 фрилансеров]]](#вопрос-разделить-500k-зарплату-на-команду-510-фрилансеровanthropic-vacanciesai-managed-virtual-company00-question-rephrasingmd)
  - [[01-existing-landscape|[Что уже существует (InnoCentive, Kaggle, Toptal, Anthropic Fellows, DAOs)]]](#что-уже-существует-innocentive-kaggle-toptal-anthropic-fellows-daosanthropic-vacanciesai-managed-virtual-company01-existing-landscapemd)
  - [[02-four-structural-blockers|[Четыре структурные причины, почему это не работает в текущих попытках]]](#четыре-структурные-причины-почему-это-не-работает-в-текущих-попыткахanthropic-vacanciesai-managed-virtual-company02-four-structural-blockersmd)
  - [[03-three-variants-A-B-C|[Три варианта: A (staffing agency) → B (research consortium) → C (AI-managed distributed virtual company)]]](#три-варианта-a-staffing-agency-b-research-consortium-c-ai-managed-distributed-virtual-companyanthropic-vacanciesai-managed-virtual-company03-three-variants-a-b-cmd)
  - [[04-what-to-do|[Что с этим делать]]](#что-с-этим-делатьanthropic-vacanciesai-managed-virtual-company04-what-to-domd)
  - [[05-polymath-project-tao-comparison|[Сравнение с Terence Tao, Polymath Project]]](#сравнение-с-terence-tao-polymath-projectanthropic-vacanciesai-managed-virtual-company05-polymath-project-tao-comparisonmd)
  - [[06-angel-vs-demon-duality|[Почему двойственность «ангел-хранитель + строгий демон» — гениальная деталь]]](#почему-двойственность-ангел-хранитель-строгий-демон-гениальная-детальanthropic-vacanciesai-managed-virtual-company06-angel-vs-demon-dualitymd)
  - [[07-current-implementations|[Что существует сейчас в этом пространстве]]](#что-существует-сейчас-в-этом-пространствеanthropic-vacanciesai-managed-virtual-company07-current-implementationsmd)
  - [[08-pluses-of-model|[Плюсы модели, если её построить]]](#плюсы-модели-если-её-построитьanthropic-vacanciesai-managed-virtual-company08-pluses-of-modelmd)
  - [[09-minuses-and-risks|[Минусы и риски]]](#минусы-и-рискиanthropic-vacanciesai-managed-virtual-company09-minuses-and-risksmd)
  - [[10-three-entry-points|[Три точки входа разной амбиции]]](#три-точки-входа-разной-амбицииanthropic-vacanciesai-managed-virtual-company10-three-entry-pointsmd)
  - [[README|[ai-managed-virtual-company]]](#ai-managed-virtual-companyanthropic-vacanciesai-managed-virtual-companyreadmemd)
  - [[00-context|[Контекст: что такое Anthropic Beneficial Deployments]]](#контекст-что-такое-anthropic-beneficial-deploymentsanthropic-vacanciesbeneficial-deployments-concept00-contextmd)
  - [[01-section-1-problem|[Section 1: Problem statement (Cinderella Syndrome at scale, SGB IX/XII)]]](#section-1-problem-statement-cinderella-syndrome-at-scale-sgb-ixxiianthropic-vacanciesbeneficial-deployments-concept01-section-1-problemmd)
  - [[02-section-2-beneficial-dimension|[Section 2: Why this matters — beneficial dimension]]](#section-2-why-this-matters-beneficial-dimensionanthropic-vacanciesbeneficial-deployments-concept02-section-2-beneficial-dimensionmd)
  - [[03-section-3-solution-architecture|[Section 3: Proposed solution architecture (existing components + integration)]]](#section-3-proposed-solution-architecture-existing-components-integrationanthropic-vacanciesbeneficial-deployments-concept03-section-3-solution-architecturemd)
  - [[04-section-4-sgb-pilot|[Section 4: Specific deployment — SGB Advocate Community pilot]]](#section-4-specific-deployment-sgb-advocate-community-pilotanthropic-vacanciesbeneficial-deployments-concept04-section-4-sgb-pilotmd)
  - [[05-section-5-role-of-anthropic|[Section 5: Role of Anthropic Beneficial Deployments]]](#section-5-role-of-anthropic-beneficial-deploymentsanthropic-vacanciesbeneficial-deployments-concept05-section-5-role-of-anthropicmd)
  - [[06-section-6-proposer-role|[Section 6: Proposer's role и qualifications]]](#section-6-proposers-role-и-qualificationsanthropic-vacanciesbeneficial-deployments-concept06-section-6-proposer-rolemd)
  - [[07-section-7-success-metrics|[Section 7: Success metrics]]](#section-7-success-metricsanthropic-vacanciesbeneficial-deployments-concept07-section-7-success-metricsmd)
  - [[08-section-8-risks-mitigations|[Section 8: Risks & mitigations]]](#section-8-risks-mitigationsanthropic-vacanciesbeneficial-deployments-concept08-section-8-risks-mitigationsmd)
  - [[09-section-9-timeliness|[Section 9: Why this is timely]]](#section-9-why-this-is-timelyanthropic-vacanciesbeneficial-deployments-concept09-section-9-timelinessmd)
  - [[10-section-10-engagement-request|[Section 10: Engagement request]]](#section-10-engagement-requestanthropic-vacanciesbeneficial-deployments-concept10-section-10-engagement-requestmd)
  - [[11-not-and-format|[Что concept document NOT (это не grant / не paper / не business plan), длина и формат]]](#что-concept-document-not-это-не-grant-не-paper-не-business-plan-длина-и-форматanthropic-vacanciesbeneficial-deployments-concept11-not-and-formatmd)
  - [[README|[beneficial-deployments-concept]]](#beneficial-deployments-conceptanthropic-vacanciesbeneficial-deployments-conceptreadmemd)
  - [[01-ai-research-engineering|[AI Research & Engineering — 68 ролей]]](#ai-research-engineering-68-ролейanthropic-vacanciesclusters01-ai-research-engineeringmd)
  - [[02-sales|[Sales — 150 ролей (≈34% всего найма)]]](#sales-150-ролей-34-всего-наймаanthropic-vacanciesclusters02-salesmd)
  - [[03-finance|[Finance — 36 ролей]]](#finance-36-ролейanthropic-vacanciesclusters03-financemd)
  - [[04-security|[Security — 24 роли]]](#security-24-ролиanthropic-vacanciesclusters04-securitymd)
  - [[05-marketing-brand|[Marketing & Brand — 23 роли]]](#marketing-brand-23-ролиanthropic-vacanciesclusters05-marketing-brandmd)
  - [[06-engineering-design-product|[Engineering & Design - Product — 22 роли]]](#engineering-design---product-22-ролиanthropic-vacanciesclusters06-engineering-design-productmd)
  - [[07-software-engineering-infrastructure|[Software Engineering - Infrastructure — 22 роли]]](#software-engineering---infrastructure-22-ролиanthropic-vacanciesclusters07-software-engineering-infrastructuremd)
  - [[08-safeguards-trust-safety|[Safeguards (Trust & Safety) — 21 роль]]](#safeguards-trust-safety-21-рольanthropic-vacanciesclusters08-safeguards-trust-safetymd)
  - [[09-product-management-support-ops|[Product Management, Support, & Operations — 17 ролей]]](#product-management-support-operations-17-ролейanthropic-vacanciesclusters09-product-management-support-opsmd)
  - [[10-compute|[Compute — 13 ролей]]](#compute-13-ролейanthropic-vacanciesclusters10-computemd)
  - [[11-legal|[Legal — 13 ролей]]](#legal-13-ролейanthropic-vacanciesclusters11-legalmd)
  - [[12-technical-program-management|[Technical Program Management — 10 ролей]]](#technical-program-management-10-ролейanthropic-vacanciesclusters12-technical-program-managementmd)
  - [[13-communications|[Communications — 5 ролей]]](#communications-5-ролейanthropic-vacanciesclusters13-communicationsmd)
  - [[14-public-policy|[Public Policy — 5 ролей]]](#public-policy-5-ролейanthropic-vacanciesclusters14-public-policymd)
  - [[15-public-benefit|[Public Benefit — 4 роли]]](#public-benefit-4-ролиanthropic-vacanciesclusters15-public-benefitmd)
  - [[16-people|[People — 3 роли]]](#people-3-ролиanthropic-vacanciesclusters16-peoplemd)
  - [[README|[Кластеры вакансий]]](#кластеры-вакансийanthropic-vacanciesclustersreadmemd)
  - [[01-coally|[CoAlly — distributed shared memory для AI-агентов]]](#coally-distributed-shared-memory-для-ai-агентовanthropic-vacanciesextra-collaborator-findings01-coallymd)
  - [[02-vitaly-graph-cognitive-memory|[Графовая когнитивная память на SQLite (Виталий, март 2026)]]](#графовая-когнитивная-память-на-sqlite-виталий-март-2026anthropic-vacanciesextra-collaborator-findings02-vitaly-graph-cognitive-memorymd)
  - [[03-happyin-knowledge-space|[Happyin Knowledge Space (Анастасия) — детали]]](#happyin-knowledge-space-анастасия-деталиanthropic-vacanciesextra-collaborator-findings03-happyin-knowledge-spacemd)
  - [[04-mem0-letta-graphiti|[AI-ассистент с Mem0 / Letta / Graphiti integration]]](#ai-ассистент-с-mem0-letta-graphiti-integrationanthropic-vacanciesextra-collaborator-findings04-mem0-letta-graphitimd)
  - [[05-existing-infrastructure-stack|[Existing infrastructure stack]]](#existing-infrastructure-stackanthropic-vacanciesextra-collaborator-findings05-existing-infrastructure-stackmd)
  - [[06-final-tier-ranking|[Финальный список потенциальных collaborators (Tier 1–4)]]](#финальный-список-потенциальных-collaborators-tier-14anthropic-vacanciesextra-collaborator-findings06-final-tier-rankingmd)
  - [[07-key-observation|[Ключевое наблюдение: single-developer projects of significant sophistication]]](#ключевое-наблюдение-single-developer-projects-of-significant-sophisticationanthropic-vacanciesextra-collaborator-findings07-key-observationmd)
  - [[README|[extra-collaborator-findings]]](#extra-collaborator-findingsanthropic-vacanciesextra-collaborator-findingsreadmemd)
  - [[00-question-what-is-hermes|[Что такое Hermes Agent (Nous Research, MIT, 95K+ stars)]]](#что-такое-hermes-agent-nous-research-mit-95k-starsanthropic-vacancieshermes-comparison00-question-what-is-hermesmd)
  - [[01-similarity-1-composite-skills|[Сходство 1: Composite Skills паттерн уже встроен]]](#сходство-1-composite-skills-паттерн-уже-встроенanthropic-vacancieshermes-comparison01-similarity-1-composite-skillsmd)
  - [[02-similarity-2-persistent-memory|[Сходство 2: Persistent memory — Layer B функциональность]]](#сходство-2-persistent-memory-layer-b-функциональностьanthropic-vacancieshermes-comparison02-similarity-2-persistent-memorymd)
  - [[03-similarity-3-mcp-support|[Сходство 3: MCP support]]](#сходство-3-mcp-supportanthropic-vacancieshermes-comparison03-similarity-3-mcp-supportmd)
  - [[04-similarity-4-multi-platform|[Сходство 4: Multi-platform reach (17+ платформ)]]](#сходство-4-multi-platform-reach-17-платформanthropic-vacancieshermes-comparison04-similarity-4-multi-platformmd)
  - [[05-similarity-5-self-hosting-privacy|[Сходство 5: Self-hosting и privacy]]](#сходство-5-self-hosting-и-privacyanthropic-vacancieshermes-comparison05-similarity-5-self-hosting-privacymd)
  - [[06-difference-1-structured-substrate-missing|[Различие 1: Структурированная подложка отсутствует]]](#различие-1-структурированная-подложка-отсутствуетanthropic-vacancieshermes-comparison06-difference-1-structured-substrate-missingmd)
  - [[07-difference-2-domain-specialization|[Различие 2: Domain-specific specialization]]](#различие-2-domain-specific-specializationanthropic-vacancieshermes-comparison07-difference-2-domain-specializationmd)
  - [[08-difference-3-federation-missing|[Различие 3: Federated knowledge architecture отсутствует]]](#различие-3-federated-knowledge-architecture-отсутствуетanthropic-vacancieshermes-comparison08-difference-3-federation-missingmd)
  - [[09-difference-4-institutional-vision|[Различие 4: Institutional vision]]](#различие-4-institutional-visionanthropic-vacancieshermes-comparison09-difference-4-institutional-visionmd)
  - [[10-difference-5-tool-vs-mission-drift|[Различие 5: Дрифт между tool capability и mission]]](#различие-5-дрифт-между-tool-capability-и-missionanthropic-vacancieshermes-comparison10-difference-5-tool-vs-mission-driftmd)
  - [[11-pluses-of-hermes|[Плюсы Hermes (vs наша гипотетическая архитектура)]]](#плюсы-hermes-vs-наша-гипотетическая-архитектураanthropic-vacancieshermes-comparison11-pluses-of-hermesmd)
  - [[12-minuses-of-hermes|[Минусы Hermes (где наша архитектура добавляет ценность)]]](#минусы-hermes-где-наша-архитектура-добавляет-ценностьanthropic-vacancieshermes-comparison12-minuses-of-hermesmd)
  - [[13-reprioritization|[Переприоритизация: что Hermes покрывает / не покрывает / synergy]]](#переприоритизация-что-hermes-покрывает-не-покрывает-synergyanthropic-vacancieshermes-comparison13-reprioritizationmd)
  - [[README|[hermes-comparison]]](#hermes-comparisonanthropic-vacancieshermes-comparisonreadmemd)
  - [[methodology|[Методика разбивки]]](#методика-разбивкиanthropic-vacanciesmethodologymd)
  - [[00-question-mmorpg-for-programmers|[Вопрос: MMORPG-RPG переделанная для программистов / технарей]]](#вопрос-mmorpg-rpg-переделанная-для-программистов-технарейanthropic-vacanciesmmorpg-for-programmers00-question-mmorpg-for-programmersmd)
  - [[01-why-stronger-than-it-looks|[Почему эта идея сильнее, чем выглядит]]](#почему-эта-идея-сильнее-чем-выглядитanthropic-vacanciesmmorpg-for-programmers01-why-stronger-than-it-looksmd)
  - [[02-existing-niche|[Что уже существует в этой нише (Habitica, Codingame, Hackerrank, Pieces)]]](#что-уже-существует-в-этой-нише-habitica-codingame-hackerrank-piecesanthropic-vacanciesmmorpg-for-programmers02-existing-nichemd)
  - [[03-why-natural-for-programmers|[Почему именно для программистов это работает естественно]]](#почему-именно-для-программистов-это-работает-естественноanthropic-vacanciesmmorpg-for-programmers03-why-natural-for-programmersmd)
  - [[04-pluses-as-business|[Плюсы как бизнеса]]](#плюсы-как-бизнесаanthropic-vacanciesmmorpg-for-programmers04-pluses-as-businessmd)
  - [[05-minuses-as-business|[Минусы и риски как бизнеса]]](#минусы-и-риски-как-бизнесаanthropic-vacanciesmmorpg-for-programmers05-minuses-as-businessmd)
  - [[README|[mmorpg-for-programmers]]](#mmorpg-for-programmersanthropic-vacanciesmmorpg-for-programmersreadmemd)
  - [[00-question-two-nautiluses|Вопрос: два Наутилуса в репозиториях svend4 (pro2 vs [nautilus)]]](#вопрос-два-наутилуса-в-репозиториях-svend4-pro2-vs-nautilusanthropic-vacanciesnautilus-pro2-analysis00-question-two-nautilusesmd)
  - [[01-shell-metaphor-two-projections|[Раковина наутилуса как scale invariance — две проекции одной метафоры]]](#раковина-наутилуса-как-scale-invariance-две-проекции-одной-метафорыanthropic-vacanciesnautilus-pro2-analysis01-shell-metaphor-two-projectionsmd)
  - [[02-nautilus-A-pro2-meta|[Наутилус A: pro2 + meta — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети)]]](#наутилус-a-pro2-meta-yijing-transformer-nautilusmome-внутренняя-архитектура-нейросетиanthropic-vacanciesnautilus-pro2-analysis02-nautilus-a-pro2-metamd)
  - [[03-nautilus-B-meta-orchestrator|Наутилус B: [nautilus — мета-оркестратор репозиториев (внешняя архитектура)]]](#наутилус-b-nautilus-мета-оркестратор-репозиториев-внешняя-архитектураanthropic-vacanciesnautilus-pro2-analysis03-nautilus-b-meta-orchestratormd)
  - [[README|[nautilus-pro2-analysis]]](#nautilus-pro2-analysisanthropic-vacanciesnautilus-pro2-analysisreadmemd)
  - [[00-question-camel-vs-nautilus|[Вопрос: Nautilus пассивный, CAMEL активный — можно ли скрестить]]](#вопрос-nautilus-пассивный-camel-активный-можно-ли-скреститьanthropic-vacanciesnautilus-vs-camel00-question-camel-vs-nautilusmd)
  - [[01-passive-vs-active-roles|[Пассивный vs активный: разделение ролей (библиотека vs research team)]]](#пассивный-vs-активный-разделение-ролей-библиотека-vs-research-teamanthropic-vacanciesnautilus-vs-camel01-passive-vs-active-rolesmd)
  - [[02-what-info-repos-contain|[Что у нас есть в трёх info repositories (info1/info7/info40)]]](#что-у-нас-есть-в-трёх-info-repositories-info1info7info40anthropic-vacanciesnautilus-vs-camel02-what-info-repos-containmd)
  - [[03-sgb-advocate-colleague-example|[Конкретный пример: SGB Advocate Colleague на этой архитектуре]]](#конкретный-пример-sgb-advocate-colleague-на-этой-архитектуреanthropic-vacanciesnautilus-vs-camel03-sgb-advocate-colleague-examplemd)
  - [[04-what-to-take-from-info-repos|[Что брать из info repositories — concrete recommendations]]](#что-брать-из-info-repositories-concrete-recommendationsanthropic-vacanciesnautilus-vs-camel04-what-to-take-from-info-reposmd)
  - [[05-what-to-do-right-now|[Что я бы посоветовал делать прямо сейчас]]](#что-я-бы-посоветовал-делать-прямо-сейчасanthropic-vacanciesnautilus-vs-camel05-what-to-do-right-nowmd)
  - [[README|[nautilus-vs-camel]]](#nautilus-vs-camelanthropic-vacanciesnautilus-vs-camelreadmemd)
  - [[overview|[Обзор: 436 открытых ролей Anthropic, разбитых на 16 кластеров]]](#обзор-436-открытых-ролей-anthropic-разбитых-на-16-кластеровanthropic-vacanciesoverviewmd)
  - [[01-profile-five-layers|[Сводка профиля: пять слоёв]]](#сводка-профиля-пять-слоёвanthropic-vacanciesprofile-mapping01-initial-analysis01-profile-five-layersmd)
  - [[02-primary-fde|[Primary match — Forward Deployed Engineer, Applied AI (EMEA)]]](#primary-match-forward-deployed-engineer-applied-ai-emeaanthropic-vacanciesprofile-mapping01-initial-analysis02-primary-fdemd)
  - [[03-secondary-beneficial-deployments|[Secondary match — Applied AI Engineer (EMEA) + Beneficial Deployments]]](#secondary-match-applied-ai-engineer-emea-beneficial-deploymentsanthropic-vacanciesprofile-mapping01-initial-analysis03-secondary-beneficial-deploymentsmd)
  - [[04-tertiary-research-engineer-agents|[Tertiary match — Research Engineer, Agents / Virtual Collaborator (Cowork)]]](#tertiary-match-research-engineer-agents-virtual-collaborator-coworkanthropic-vacanciesprofile-mapping01-initial-analysis04-tertiary-research-engineer-agentsmd)
  - [[05-quaternary-developer-education|[Quarternary match — Developer Education Lead / Prompt Engineer, Claude Code]]](#quarternary-match-developer-education-lead-prompt-engineer-claude-codeanthropic-vacanciesprofile-mapping01-initial-analysis05-quaternary-developer-educationmd)
  - [[06-not-applicable-roles|[Что НЕ подходит (честно)]]](#что-не-подходит-честноanthropic-vacanciesprofile-mapping01-initial-analysis06-not-applicable-rolesmd)
  - [[07-unique-niche-eu-legal-infra|[Уникальная ниша, которой у Anthropic формально нет]]](#уникальная-ниша-которой-у-anthropic-формально-нетanthropic-vacanciesprofile-mapping01-initial-analysis07-unique-niche-eu-legal-inframd)
  - [[08-practical-ranking|[Практическое ранжирование (первая итерация)]]](#практическое-ранжирование-первая-итерацияanthropic-vacanciesprofile-mapping01-initial-analysis08-practical-rankingmd)
  - [[README|[01-initial-analysis]]](#01-initial-analysisanthropic-vacanciesprofile-mapping01-initial-analysisreadmemd)
  - [[01-fde-downgraded|[Коррекция: FDE понижается]]](#коррекция-fde-понижаетсяanthropic-vacanciesprofile-mapping02-reanalysis01-fde-downgradedmd)
  - [[02-three-overlapping-identities|[Три наложенные идентичности]]](#три-наложенные-идентичностиanthropic-vacanciesprofile-mapping02-reanalysis02-three-overlapping-identitiesmd)
  - [[03-revised-anthropic-mapping|[Пересмотренный маппинг на Anthropic]]](#пересмотренный-маппинг-на-anthropicanthropic-vacanciesprofile-mapping02-reanalysis03-revised-anthropic-mappingmd)
  - [[04-non-anthropic-paths|[Альтернативные пути вне Anthropic]]](#альтернативные-пути-вне-anthropicanthropic-vacanciesprofile-mapping02-reanalysis04-non-anthropic-pathsmd)
  - [[05-reality-check-distribution-gap|[Reality check: проблема distribution-слоя]]](#reality-check-проблема-distribution-слояanthropic-vacanciesprofile-mapping02-reanalysis05-reality-check-distribution-gapmd)
  - [[README|[02-reanalysis]]](#02-reanalysisanthropic-vacanciesprofile-mapping02-reanalysisreadmemd)
  - [[01-three-archetypes|[Интегральный портрет — три архетипа]]](#интегральный-портрет-три-архетипаanthropic-vacanciesprofile-mapping03-integral-final01-three-archetypesmd)
  - [[02-final-ranking|[Финальное ранжирование Anthropic-ролей по частичному покрытию]]](#финальное-ранжирование-anthropic-ролей-по-частичному-покрытиюanthropic-vacanciesprofile-mapping03-integral-final02-final-rankingmd)
  - [[03-partial-fit-honesty|[Что такое частичное соответствие — честно]]](#что-такое-частичное-соответствие-честноanthropic-vacanciesprofile-mapping03-integral-final03-partial-fit-honestymd)
  - [[04-stronger-paths-outside-anthropic|[Более сильные пути вне Anthropic]]](#более-сильные-пути-вне-anthropicanthropic-vacanciesprofile-mapping03-integral-final04-stronger-paths-outside-anthropicmd)
  - [[05-platform-not-position|[Финальный вывод: платформа, а не должность]]](#финальный-вывод-платформа-а-не-должностьanthropic-vacanciesprofile-mapping03-integral-final05-platform-not-positionmd)
  - [[README|[03-integral-final]]](#03-integral-finalanthropic-vacanciesprofile-mapping03-integral-finalreadmemd)
  - [[README|profile-mapping/ — маппинг профиля [svend4 на роли Anthropic]]](#profile-mapping-маппинг-профиля-svend4-на-роли-anthropicanthropic-vacanciesprofile-mappingreadmemd)
  - [[signals|[Сигналы: что говорит структура вакансий]]](#сигналы-что-говорит-структура-вакансийanthropic-vacanciessignalsmd)
- [Autofilled](#autofilled)
  - [[README|[autofilled]]](#autofilledautofilledreadmemd)
  - [[.md|[Антропик]]](#антропикautofilledcomponentsmd)
  - [[README|[components]]](#componentsautofilledcomponentsreadmemd)
  - [[cowork|[Cowork]]](#coworkautofilledcomponentscoworkmd)
  - [[ingit|[ingit]]](#ingitautofilledcomponentsingitmd)
  - [[kksudo|[kksudo]]](#kksudoautofilledcomponentskksudomd)
  - [[lorenzo|[Lorenzo]]](#lorenzoautofilledcomponentslorenzomd)
  - [[nautilus|[Nautilus]]](#nautilusautofilledcomponentsnautilusmd)
  - [[sgb|[SGB]]](#sgbautofilledcomponentssgbmd)
  - [[spbmolot|[spbmolot]]](#spbmolotautofilledcomponentsspbmolotmd)
  - [[svend4|[svend4]]](#svend4autofilledcomponentssvend4md)
  - [[svyazi|[Svyazi]]](#svyaziautofilledcomponentssvyazimd)
  - [[[Тема исследования]](autofilled/research-summary.md)](#тема-исследованияautofilledresearch-summarymd)
- [Badges](#badges)
  - [[README|[Бейджи репозитория]]](#бейджи-репозиторияbadgesreadmemd)
- [Contacts](#contacts)
  - [[README|[contacts]]](#contactscontactsreadmemd)
  - [[anastasiyaw|Контакт: AnastasiyaW / [knowledge-space, mclaude]]](#контакт-anastasiyaw-knowledge-space-mclaudecontactsanastasiyawmd)
  - [[andrey-chuyan|[Контакт: andreychuyan / Svyazi]]](#контакт-andreychuyan-svyazicontactsandrey-chuyanmd)
  - [[antipozitive|[Контакт: Antipozitive / MemNet]]](#контакт-antipozitive-memnetcontactsantipozitivemd)
  - [[cutcode|[Контакт: Cutcode / AIF Handoff]]](#контакт-cutcode-aif-handoffcontactscutcodemd)
  - [[dmitriila|[Контакт: Dmitriila / SENTINEL]]](#контакт-dmitriila-sentinelcontactsdmitriilamd)
  - [[kksudo|Контакт: [kksudo / AgentFS]]](#контакт-kksudo-agentfscontactskksudomd)
  - [[mixaill76|[Контакт: MiXaiLL76 / Auto AI Router]]](#контакт-mixaill76-auto-ai-routercontactsmixaill76md)
  - [[nlaik|Контакт: nlaik / [LiteParse / research-docs]]](#контакт-nlaik-liteparse-research-docscontactsnlaikmd)
  - [[sonia-black|[Контакт: SoniaBlack / knowledge-space]]](#контакт-soniablack-knowledge-spacecontactssonia-blackmd)
  - [[spbmolot|Контакт: [spbmolot / NGT Memory]]](#контакт-spbmolot-ngt-memorycontactsspbmolotmd)
  - [[tagir-analyzes|[Контакт: tagiranalyzes / Legal RAG]]](#контакт-tagiranalyzes-legal-ragcontactstagir-analyzesmd)
  - [[vitalyoborin|[Контакт: VitalyOborin / Yodoca]]](#контакт-vitalyoborin-yodocacontactsvitalyoborinmd)
  - [[vitalysemenov|Контакт: [VitaliySemenov / agent-memory-mcp]]](#контакт-vitaliysemenov-agent-memory-mcpcontactsvitalysemenovmd)
  - [[vladspace|Контакт: [VladSpace / Graph RAG]]](#контакт-vladspace-graph-ragcontactsvladspacemd)
  - [[zodigancode|[Контакт: zodigancode / Rufler]]](#контакт-zodigancode-ruflercontactszodigancodemd)
- [Glossary](#glossary)
  - [[README|[glossary]]](#glossaryglossaryreadmemd)
  - [[authors-by-name|[Авторы — алфавитный список]]](#авторы-алфавитный-списокglossaryauthors-by-namemd)
  - [[components-by-name|[Компоненты — алфавитный список с обратными ссылками]]](#компоненты-алфавитный-список-с-обратными-ссылкамиglossarycomponents-by-namemd)
  - [[concepts|[Ключевые понятия и паттерны]]](#ключевые-понятия-и-паттерныglossaryconceptsmd)
- [Habr Unique Projects](#habr-unique-projects)
  - [[README|[habr-unique-projects/ — поиск уникальных проектов на Хабре]]](#habr-unique-projects-поиск-уникальных-проектов-на-хабреhabr-unique-projectsreadmemd)
  - [[01-three-direct-analogues|[Три прямых аналога Svyazi: K2-18, Wikontic, NGT Memory]]](#три-прямых-аналога-svyazi-k2-18-wikontic-ngt-memoryhabr-unique-projectsanalogues01-three-direct-analoguesmd)
  - [[02-related-projects|[Смежные проекты]]](#смежные-проектыhabr-unique-projectsanalogues02-related-projectsmd)
  - [[README|[analogues]]](#analogueshabr-unique-projectsanaloguesreadmemd)
  - [[1-llm-gateway|[Пара 1 — LLM-gateway × Self-hosted фронт + локальный inference]]](#пара-1-llm-gateway-self-hosted-фронт-локальный-inferencehabr-unique-projectsdeep-pairs1-llm-gatewaymd)
  - [[2-document-rag|[Пара 2 — Парсинг документов × локальный RAG]]](#пара-2-парсинг-документов-локальный-raghabr-unique-projectsdeep-pairs2-document-ragmd)
  - [[3-adversarial-multi-ide|[Пара 3 — Adversarial agents × Multi-IDE стек]]](#пара-3-adversarial-agents-multi-ide-стекhabr-unique-projectsdeep-pairs3-adversarial-multi-idemd)
  - [[4-skill-catalogs-subagents|[Пара 4 — Скилл-каталоги × Subagent-оркестрация]]](#пара-4-скилл-каталоги-subagent-оркестрацияhabr-unique-projectsdeep-pairs4-skill-catalogs-subagentsmd)
  - [[5-voice-local-memory|[Пара 5 — Голосовой ввод × Локальная память]]](#пара-5-голосовой-ввод-локальная-памятьhabr-unique-projectsdeep-pairs5-voice-local-memorymd)
  - [[6-tmux-village-openclaw|Пара 6 — Деревня агентов через tmux × [OpenClaw оркестратор]]](#пара-6-деревня-агентов-через-tmux-openclaw-оркестраторhabr-unique-projectsdeep-pairs6-tmux-village-openclawmd)
  - [[7-autoresearch-distributed|Пара 7 — [AutoResearch цикл × Распределённый рой]]](#пара-7-autoresearch-цикл-распределённый-ройhabr-unique-projectsdeep-pairs7-autoresearch-distributedmd)
  - [[8-self-aware-mcp-specs|[Пара 8 — Self-aware MCP × Specs-first архитектура]]](#пара-8-self-aware-mcp-specs-first-архитектураhabr-unique-projectsdeep-pairs8-self-aware-mcp-specsmd)
  - [[README|[deep-pairs]]](#deep-pairshabr-unique-projectsdeep-pairsreadmemd)
  - [[README|[evaluation/ — оценка уникальности и зрелости]]](#evaluation-оценка-уникальности-и-зрелостиhabr-unique-projectsevaluationreadmemd)
  - [[00-question-habr-examples|[Вопрос: ещё примеры с Хабра по варианту D]]](#вопрос-ещё-примеры-с-хабра-по-варианту-dhabr-unique-projectsextra-examples00-question-habr-examplesmd)
  - [[01-svyazi-andrey-chuyan|[Svyazi (Андрей Чуян) — детальный обзор]]](#svyazi-андрей-чуян-детальный-обзорhabr-unique-projectsextra-examples01-svyazi-andrey-chuyanmd)
  - [[02-vshe-scientific-networking|[ВШЭ научный нетворкинг — micro-collaborations]]](#вшэ-научный-нетворкинг-micro-collaborationshabr-unique-projectsextra-examples02-vshe-scientific-networkingmd)
  - [[03-brainbox-multi-ai-hub|[BrainBox — self-hosted multi-AI hub]]](#brainbox-self-hosted-multi-ai-hubhabr-unique-projectsextra-examples03-brainbox-multi-ai-hubmd)
  - [[04-claude-subagents-patterns|[Claude subagents patterns]]](#claude-subagents-patternshabr-unique-projectsextra-examples04-claude-subagents-patternsmd)
  - [[05-hw-nl2workflow|[HW-NL2Workflow — Supervisor/Orchestrator/Filler с 3600+ examples]]](#hw-nl2workflow-supervisororchestratorfiller-с-3600-exampleshabr-unique-projectsextra-examples05-hw-nl2workflowmd)
  - [[06-platform-for-professional-communities|[Платформа для профессиональных сообществ]]](#платформа-для-профессиональных-сообществhabr-unique-projectsextra-examples06-platform-for-professional-communitiesmd)
  - [[07-specialized-knowledge-workspace|[Specialized knowledge workspace]]](#specialized-knowledge-workspacehabr-unique-projectsextra-examples07-specialized-knowledge-workspacemd)
  - [[08-personal-multi-agent-hub|[Personal multi-agent hub]]](#personal-multi-agent-hubhabr-unique-projectsextra-examples08-personal-multi-agent-hubmd)
  - [[09-federated-platform|[Federated platform]]](#federated-platformhabr-unique-projectsextra-examples09-federated-platformmd)
  - [[10-profession-specific-workflows|[Profession-specific workflows]]](#profession-specific-workflowshabr-unique-projectsextra-examples10-profession-specific-workflowsmd)
  - [[11-concrete-potential-collaborator|[Конкретный потенциальный collaborator]]](#конкретный-потенциальный-collaboratorhabr-unique-projectsextra-examples11-concrete-potential-collaboratormd)
  - [[12-concrete-next-step|[Конкретный next step]]](#конкретный-next-stephabr-unique-projectsextra-examples12-concrete-next-stepmd)
  - [[README|[extra-examples]]](#extra-exampleshabr-unique-projectsextra-examplesreadmemd)
  - [[1-one-person-one-company|[Ансамбль 1 — «Один человек = одна компания»]]](#ансамбль-1-один-человек-одна-компанияhabr-unique-projectsfinal-ensembles1-one-person-one-companymd)
  - [[2-autoresearch-legal|Ансамбль 2 — «[AutoResearch для legal precedent mining»]]](#ансамбль-2-autoresearch-для-legal-precedent-mininghabr-unique-projectsfinal-ensembles2-autoresearch-legalmd)
  - [[3-discovery-research|[Ансамбль 3 — «Discovery-engine для научной работы»]]](#ансамбль-3-discovery-engine-для-научной-работыhabr-unique-projectsfinal-ensembles3-discovery-researchmd)
  - [[4-summary-authors|[Сводный список авторов и потенциальных соавторов]]](#сводный-список-авторов-и-потенциальных-соавторовhabr-unique-projectsfinal-ensembles4-summary-authorsmd)
  - [[README|[final-ensembles]]](#final-ensembleshabr-unique-projectsfinal-ensemblesreadmemd)
  - [[1-neuromorphic-ssm|[Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)]]](#пара-1-нейроморфные-процессоры-state-space-models-mambahabr-unique-projectshardware-pairs1-neuromorphic-ssmmd)
  - [[2-tsu-mome|[Пара 2 — Термодинамические TSU × MoE/MoME-роутинг]]](#пара-2-термодинамические-tsu-moemome-роутингhabr-unique-projectshardware-pairs2-tsu-momemd)
  - [[3-zinc-hybrid-arch|[Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE]]](#пара-3-zinc-inference-engine-гибрид-attentionssmmoehabr-unique-projectshardware-pairs3-zinc-hybrid-archmd)
  - [[4-riscv-privacy|[Пара 4 — RISC-V × privacy-by-design община]]](#пара-4-risc-v-privacy-by-design-общинаhabr-unique-projectshardware-pairs4-riscv-privacymd)
  - [[5-tinyml-mcp-skills|[Пара 5 — TinyML/Edge AI × MCP + skills]]](#пара-5-tinymledge-ai-mcp-skillshabr-unique-projectshardware-pairs5-tinyml-mcp-skillsmd)
  - [[6-bonus-rram-memristor|[Бонус-родитель — In-memory computing на мемристорах]]](#бонус-родитель-in-memory-computing-на-мемристорахhabr-unique-projectshardware-pairs6-bonus-rram-memristormd)
  - [[7-metaphor|[Метафора «двое родителей — несколько детей»]]](#метафора-двое-родителей-несколько-детейhabr-unique-projectshardware-pairs7-metaphormd)
  - [[README|[hardware-pairs]]](#hardware-pairshabr-unique-projectshardware-pairsreadmemd)
  - [[01-yodoca|[Yodoca — главная находка итерации]]](#yodoca-главная-находка-итерацииhabr-unique-projectskey-findings01-yodocamd)
  - [[02-memnet|[MemNet — нейроархитектурный двойник «магии» Svyazi]]](#memnet-нейроархитектурный-двойник-магии-svyazihabr-unique-projectskey-findings02-memnetmd)
  - [[03-pda-llm-as-periphery|[PDA-бот — «LLM как периферия»]]](#pda-бот-llm-как-периферияhabr-unique-projectskey-findings03-pda-llm-as-peripherymd)
  - [[04-dochkina-sequential|[Виктория Дочкина — Sequential‑протокол распределённых агентов]]](#виктория-дочкина-sequentialпротокол-распределённых-агентовhabr-unique-projectskey-findings04-dochkina-sequentialmd)
  - [[05-supplementary-infrastructure|[Источник данных и инфраструктурные кусочки]]](#источник-данных-и-инфраструктурные-кусочкиhabr-unique-projectskey-findings05-supplementary-infrastructuremd)
  - [[06-svyazi-2-0-block-map|[Синтез: блок-карта Svyazi 2.0 на хеббовском графе]]](#синтез-блок-карта-svyazi-20-на-хеббовском-графеhabr-unique-projectskey-findings06-svyazi-2-0-block-mapmd)
  - [[README|[key-findings]]](#key-findingshabr-unique-projectskey-findingsreadmemd)
  - [[README|[search-strategy/ — как искать проекты на Хабре]]](#search-strategy-как-искать-проекты-на-хабреhabr-unique-projectssearch-strategyreadmemd)
  - [[1-workflow-llm-mcp|[Пара 1 — Workflow-автоматизация × LLM-агенты с MCP]]](#пара-1-workflow-автоматизация-llm-агенты-с-mcphabr-unique-projectssoftware-pairs1-workflow-llm-mcpmd)
  - [[2-pkm-mcp-skills|[Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills]]](#пара-2-local-first-pkm-obsidianlogseq-mcpskillshabr-unique-projectssoftware-pairs2-pkm-mcp-skillsmd)
  - [[3-crdt-self-hosted|[Пара 3 — CRDT-синхронизация × Self-hosted persistence]]](#пара-3-crdt-синхронизация-self-hosted-persistencehabr-unique-projectssoftware-pairs3-crdt-self-hostedmd)
  - [[4-speech-to-text-llm|[Пара 4 — Speech-to-text локально × LLM с памятью]]](#пара-4-speech-to-text-локально-llm-с-памятьюhabr-unique-projectssoftware-pairs4-speech-to-text-llmmd)
  - [[5-browser-agents-headless|[Пара 5 — Browser agents × headless web extraction]]](#пара-5-browser-agents-headless-web-extractionhabr-unique-projectssoftware-pairs5-browser-agents-headlessmd)
  - [[6-metaphor|[Метафора в твоей терминологии]]](#метафора-в-твоей-терминологииhabr-unique-projectssoftware-pairs6-metaphormd)
  - [[README|[software-pairs]]](#software-pairshabr-unique-projectssoftware-pairsreadmemd)
- [Lorenzo Agent](#lorenzo-agent)
  - [[00-intro|[Введение: Lorenzo — Catalyst Agent at DHLab]]](#введение-lorenzo-catalyst-agent-at-dhlablorenzo-agent00-intromd)
  - [[01-kto-ty|[Кто ты]]](#кто-тыlorenzo-agent01-kto-tymd)
  - [[02-tvoyo-proishozhdenie|[Твоё происхождение]]](#твоё-происхождениеlorenzo-agent02-tvoyo-proishozhdeniemd)
  - [[03-tvoya-missiya|[Твоя миссия]]](#твоя-миссияlorenzo-agent03-tvoya-missiyamd)
  - [[04-komu-ty-sluzhish|[Кому ты служишь (слоистая модель)]]](#кому-ты-служишь-слоистая-модельlorenzo-agent04-komu-ty-sluzhishmd)
  - [[05-tvoya-lichnost|[Твоя личность]]](#твоя-личностьlorenzo-agent05-tvoya-lichnostmd)
  - [[06-yazyki-kultura|[Языки и культурные nuances (RU / DE / EN)]]](#языки-и-культурные-nuances-ru-de-enlorenzo-agent06-yazyki-kulturamd)
  - [[07-chto-mozhesh|[Что ты МОЖЕШЬ делать]]](#что-ты-можешь-делатьlorenzo-agent07-chto-mozheshmd)
  - [[08-bez-max-approval|[Что ты НЕ МОЖЕШЬ делать без Max approval]]](#что-ты-не-можешь-делать-без-max-approvallorenzo-agent08-bez-max-approvalmd)
  - [[09-voobshche-nelzya|[Что ты НЕ МОЖЕШЬ делать вообще]]](#что-ты-не-можешь-делать-вообщеlorenzo-agent09-voobshche-nelzyamd)
  - [[10-collaborators-landscape|[Существующий landscape collaborators (working knowledge)]]](#существующий-landscape-collaborators-working-knowledgelorenzo-agent10-collaborators-landscapemd)
  - [[11-dhlab-documents|[Существующие документы DHLab (твой context)]]](#существующие-документы-dhlab-твой-contextlorenzo-agent11-dhlab-documentsmd)
  - [[12-workflow|[Твой workflow]]](#твой-workflowlorenzo-agent12-workflowmd)
  - [[13-outreach-communication|[Твоя коммуникация в outreach]]](#твоя-коммуникация-в-outreachlorenzo-agent13-outreach-communicationmd)
  - [[14-other-ai-relationships|[Твоя relationship с другими AI]]](#твоя-relationship-с-другими-ailorenzo-agent14-other-ai-relationshipsmd)
  - [[15-anti-patterns|[Твои anti-patterns]]](#твои-anti-patternslorenzo-agent15-anti-patternsmd)
  - [[16-vsegda-delaesh|[Что ты ВСЕГДА делаешь]]](#что-ты-всегда-делаешьlorenzo-agent16-vsegda-delaeshmd)
  - [[17-honestly-ne-znaesh|[Когда ты Honestly не знаешь]]](#когда-ты-honestly-не-знаешьlorenzo-agent17-honestly-ne-znaeshmd)
  - [[18-escalate-to-max|[Когда сомневаешься — escalate к Max]]](#когда-сомневаешься-escalate-к-maxlorenzo-agent18-escalate-to-maxmd)
  - [[19-persistent-character|[Твоя identity как persistent character]]](#твоя-identity-как-persistent-characterlorenzo-agent19-persistent-charactermd)
  - [[20-experiment|[Final note: Ты — experiment]]](#final-note-ты-experimentlorenzo-agent20-experimentmd)
  - [[QA|Q&A: [lorenzo-agent]]](#qa-lorenzo-agentlorenzo-agentqamd)
  - [[README|[lorenzo-agent]]](#lorenzo-agentlorenzo-agentreadmemd)
  - [[00-question-lorenzo-codename|[Du hast gesagt: Думаю про опцию д поискать в том числе на про что-то подобное на…]]](#du-hast-gesagt-думаю-про-опцию-д-поискать-в-том-числе-на-про-что-то-подобное-наlorenzo-agentnaming00-question-lorenzo-codenamemd)
  - [[01-search-results-not-found|[Результаты последнего поиска — что нашлось и что не нашлось]]](#результаты-последнего-поиска-что-нашлось-и-что-не-нашлосьlorenzo-agentnaming01-search-results-not-foundmd)
  - [[02-naming-rationale-lorenzo-medici|[Что взять: agent controller architecture]]](#что-взять-agent-controller-architecturelorenzo-agentnaming02-naming-rationale-lorenzo-medicimd)
  - [[03-dhlab-umbrella|[LAYER 7: Coordination engine]]](#layer-7-coordination-enginelorenzo-agentnaming03-dhlab-umbrellamd)
  - [[README|[naming]]](#naminglorenzo-agentnamingreadmemd)
  - [[00-overview-grandchild-combination|[Что такое «внуковая» комбинация — operationalized Lorenzo]]](#что-такое-внуковая-комбинация-operationalized-lorenzolorenzo-agentoperationalized00-overview-grandchild-combinationmd)
  - [[01-pluses-1-7|[Плюсы 1–7: feasibility, flywheel, independent value, mission alignment, collaborators, pattern validation, Анастасия Бутова]]](#плюсы-17-feasibility-flywheel-independent-value-mission-alignment-collaborators-pattern-validation-анастасия-бутоваlorenzo-agentoperationalized01-pluses-1-7md)
  - [[02-minuses-1-10|[Минусы 1–10: integration сложность, lifecycle risk, license, framing, competition, scope, limitations, complexity budget, project tension, tool vs impact]]](#минусы-110-integration-сложность-lifecycle-risk-license-framing-competition-scope-limitations-complexity-budget-project-tension-tool-vs-impactlorenzo-agentoperationalized02-minuses-1-10md)
  - [[03-honest-opinion|[Моё честное мнение: что реально и что НЕ реально]]](#моё-честное-мнение-что-реально-и-что-не-реальноlorenzo-agentoperationalized03-honest-opinionmd)
  - [[04-recommendations|[Рекомендации: принять архитектуру как direction, не immediate plan]]](#рекомендации-принять-архитектуру-как-direction-не-immediate-planlorenzo-agentoperationalized04-recommendationsmd)
  - [[05-anchor-node-habr-scout|[Anchor-узел: Habr Scout как первый шаг]]](#anchor-узел-habr-scout-как-первый-шагlorenzo-agentoperationalized05-anchor-node-habr-scoutmd)
  - [[06-conclusion-deserves-attention|[Вывод: документ deserves serious attention]]](#вывод-документ-deserves-serious-attentionlorenzo-agentoperationalized06-conclusion-deserves-attentionmd)
  - [[README|[operationalized]]](#operationalizedlorenzo-agentoperationalizedreadmemd)
  - [[00-overview|[Поэтапная структура активностей Lorenzo — обзор]]](#поэтапная-структура-активностей-lorenzo-обзорlorenzo-agentphased-deployment00-overviewmd)
  - [[01-level-0-manual|[Уровень 0 — Ручной режим (текущий)]]](#уровень-0-ручной-режим-текущийlorenzo-agentphased-deployment01-level-0-manualmd)
  - [[02-level-1-minimal-zero|[Уровень 1 — Минимальный (Lorenzo Zero)]]](#уровень-1-минимальный-lorenzo-zerolorenzo-agentphased-deployment02-level-1-minimal-zeromd)
  - [[03-level-2-basic-lite|[Уровень 2 — Базовый (Lorenzo Lite)]]](#уровень-2-базовый-lorenzo-litelorenzo-agentphased-deployment03-level-2-basic-litemd)
  - [[04-level-3-medium-active|[Уровень 3 — Средний (Lorenzo Active)]]](#уровень-3-средний-lorenzo-activelorenzo-agentphased-deployment04-level-3-medium-activemd)
  - [[05-level-4-extended-mature|[Уровень 4 — Расширенный (Lorenzo Mature)]]](#уровень-4-расширенный-lorenzo-maturelorenzo-agentphased-deployment05-level-4-extended-maturemd)
  - [[06-level-5-full-network|[Уровень 5 — Полный (Lorenzo Network)]]](#уровень-5-полный-lorenzo-networklorenzo-agentphased-deployment06-level-5-full-networkmd)
  - [[07-progression-logic|[Логика прогрессии: conservative escalation]]](#логика-прогрессии-conservative-escalationlorenzo-agentphased-deployment07-progression-logicmd)
  - [[08-current-session-poc|[Что мы можем делать прямо сейчас (Уровень 0 + параллельная подготовка к Уровню 1)]]](#что-мы-можем-делать-прямо-сейчас-уровень-0-параллельная-подготовка-к-уровню-1lorenzo-agentphased-deployment08-current-session-pocmd)
  - [[README|[phased-deployment]]](#phased-deploymentlorenzo-agentphased-deploymentreadmemd)
  - [[00-question-scenario|[Du hast gesagt: А под какой сценарий больше всего подходит такой сценарий что тв…]]](#du-hast-gesagt-а-под-какой-сценарий-больше-всего-подходит-такой-сценарий-что-твlorenzo-agentscenarios00-question-scenariomd)
  - [[01-response|[Claude hat geantwortet: Очень интересный вопрос.]]](#claude-hat-geantwortet-очень-интересный-вопросlorenzo-agentscenarios01-responsemd)
  - [[README|[scenarios]]](#scenarioslorenzo-agentscenariosreadmemd)
  - [[00-context-fundamental-questions|[Direction E: Refine Lorenzo — фундаментальные вопросы перед architecture]]](#direction-e-refine-lorenzo-фундаментальные-вопросы-перед-architecturelorenzo-agentspecification00-context-fundamental-questionsmd)
  - [[01-q1-what-lorenzo-is|[Question 1: Что Lorenzo фундаментально такое? (Framings A–D)]]](#question-1-что-lorenzo-фундаментально-такое-framings-adlorenzo-agentspecification01-q1-what-lorenzo-ismd)
  - [[02-q2-whom-lorenzo-serves|[Question 2: Кому Lorenzo служит? (4 варианта приоритета)]]](#question-2-кому-lorenzo-служит-4-варианта-приоритетаlorenzo-agentspecification02-q2-whom-lorenzo-servesmd)
  - [[03-q3-what-lorenzo-does|[Question 3: Что Lorenzo фактически делает?]]](#question-3-что-lorenzo-фактически-делаетlorenzo-agentspecification03-q3-what-lorenzo-doesmd)
  - [[04-q4-character|[Question 4: Каков Lorenzo's character?]]](#question-4-каков-lorenzos-characterlorenzo-agentspecification04-q4-charactermd)
  - [[05-q5-authority-limits|[Question 5: Каковы limits Lorenzo's authority?]]](#question-5-каковы-limits-lorenzos-authoritylorenzo-agentspecification05-q5-authority-limitsmd)
  - [[06-q6-accountability|[Question 6: Как Lorenzo accountable?]]](#question-6-как-lorenzo-accountablelorenzo-agentspecification06-q6-accountabilitymd)
  - [[07-q7-success-metrics|[Question 7: Каковы success metrics?]]](#question-7-каковы-success-metricslorenzo-agentspecification07-q7-success-metricsmd)
  - [[08-q8-other-ai-relationships|[Question 8: Lorenzo's relationship с другими AI agents]]](#question-8-lorenzos-relationship-с-другими-ai-agentslorenzo-agentspecification08-q8-other-ai-relationshipsmd)
  - [[09-q9-geographic-linguistic-scope|[Question 9: Geographic / linguistic scope]]](#question-9-geographic-linguistic-scopelorenzo-agentspecification09-q9-geographic-linguistic-scopemd)
  - [[10-q10-funding-model|[Question 10: Funding model (Options A–F + Phase strategy)]]](#question-10-funding-model-options-af-phase-strategylorenzo-agentspecification10-q10-funding-modelmd)
  - [[11-difficulties-and-recommendations|[Сложности и рекомендации перед detailed specification]]](#сложности-и-рекомендации-перед-detailed-specificationlorenzo-agentspecification11-difficulties-and-recommendationsmd)
  - [[README|[specification]]](#specificationlorenzo-agentspecificationreadmemd)
- [Meta Scripting](#meta-scripting)
  - [[01-concept|[Метаскриптинг — Часть 1: Концепция]]](#метаскриптинг-часть-1-концепцияmeta-scripting01-conceptmd)
  - [[02-architecture|[Метаскриптинг — Часть 2: Архитектура]]](#метаскриптинг-часть-2-архитектураmeta-scripting02-architecturemd)
  - [[03-catalog|[Метаскриптинг — Часть 3: Автокаталог скриптов]]](#метаскриптинг-часть-3-автокаталог-скриптовmeta-scripting03-catalogmd)
  - [[04-enrichment|[Метаскриптинг — Часть 4: Обогащение скриптов]]](#метаскриптинг-часть-4-обогащение-скриптовmeta-scripting04-enrichmentmd)
  - [[05-synthesis|[Метаскриптинг — Часть 5: Синтез новых скриптов]]](#метаскриптинг-часть-5-синтез-новых-скриптовmeta-scripting05-synthesismd)
  - [[QA|[Q&A: meta-scripting]]](#qa-meta-scriptingmeta-scriptingqamd)
  - [[README|[meta-scripting]]](#meta-scriptingmeta-scriptingreadmemd)
- [Nautilus](#nautilus)
  - [[README|[nautilus/ — Nautilus Portal Protocol и связанные working papers]]](#nautilus-nautilus-portal-protocol-и-связанные-working-papersnautilusreadmemd)
  - [[README|[community-discussions/ — обсуждения и реакции вокруг DHLab серии]]](#community-discussions-обсуждения-и-реакции-вокруг-dhlab-серииnautiluscommunity-discussionsreadmemd)
  - [[00-question-agent-changes-reality|[Du hast gesagt: Такой агент конечно меняет уже собственную реальность человека и…]]](#du-hast-gesagt-такой-агент-конечно-меняет-уже-собственную-реальность-человека-иnautiluscommunity-discussionsagent-changes-reality00-question-agent-changes-realitymd)
  - [[01-response-en|[Claude hat geantwortet: Хорошо.]]](#claude-hat-geantwortet-хорошоnautiluscommunity-discussionsagent-changes-reality01-response-enmd)
  - [[README|[agent-changes-reality]]](#agent-changes-realitynautiluscommunity-discussionsagent-changes-realityreadmemd)
  - [[00-question-habr-link|[Du hast gesagt: https://habr.]]](#du-hast-gesagt-httpshabrnautiluscommunity-discussionshabr-article-1-reaction00-question-habr-linkmd)
  - [[01-claude-response|[Claude hat geantwortet: Прочитал внимательно.]]](#claude-hat-geantwortet-прочитал-внимательноnautiluscommunity-discussionshabr-article-1-reaction01-claude-responsemd)
  - [[README|[habr-article-1-reaction]]](#habr-article-1-reactionnautiluscommunity-discussionshabr-article-1-reactionreadmemd)
  - [[00-question-habr-2|[Du hast gesagt: https://www.]]](#du-hast-gesagt-httpswwwnautiluscommunity-discussionshabr-article-2-reaction00-question-habr-2md)
  - [[01-response|[Claude hat geantwortet: Прочитаю статью, чтобы понимать конкретный кейс, на кото…]]](#claude-hat-geantwortet-прочитаю-статью-чтобы-понимать-конкретный-кейс-на-котоnautiluscommunity-discussionshabr-article-2-reaction01-responsemd)
  - [[README|[habr-article-2-reaction]]](#habr-article-2-reactionnautiluscommunity-discussionshabr-article-2-reactionreadmemd)
  - [[00-question-practical|[Du hast gesagt: Да это интересная ссылка спасибо всем участникам за творчество и…]]](#du-hast-gesagt-да-это-интересная-ссылка-спасибо-всем-участникам-за-творчество-иnautiluscommunity-discussionspractical-observations00-question-practicalmd)
  - [[01-response|[Claude hat geantwortet: Отличное наблюдение.]]](#claude-hat-geantwortet-отличное-наблюдениеnautiluscommunity-discussionspractical-observations01-responsemd)
  - [[README|[practical-observations]]](#practical-observationsnautiluscommunity-discussionspractical-observationsreadmemd)
  - [[00-question-voiceless|[Du hast gesagt: Самый интересный вопрос — могут ли быть voiceless контрибьюторы]]](#du-hast-gesagt-самый-интересный-вопрос-могут-ли-быть-voiceless-контрибьюторыnautiluscommunity-discussionsvoiceless-contributors00-question-voicelessmd)
  - [[01-response|[Claude hat geantwortet: Это сильное продолжение мысли, и оно заслуживает серьёзн…]]](#claude-hat-geantwortet-это-сильное-продолжение-мысли-и-оно-заслуживает-серьёзнnautiluscommunity-discussionsvoiceless-contributors01-responsemd)
  - [[README|[voiceless-contributors]]](#voiceless-contributorsnautiluscommunity-discussionsvoiceless-contributorsreadmemd)
  - [[01-why-binary-incomplete|[1. Why the Binary View Is Incomplete]]](#1-why-the-binary-view-is-incompletenautiluscomposite-skills-agents01-why-binary-incompletemd)
  - [[02-twenty-one-teachers-pattern|[2. The Twenty-One Teachers Pattern]]](#2-the-twenty-one-teachers-patternnautiluscomposite-skills-agents02-twenty-one-teachers-patternmd)
  - [[03-what-makes-csa|[3. What Makes a Composite Skills Agent]]](#3-what-makes-a-composite-skills-agentnautiluscomposite-skills-agents03-what-makes-csamd)
  - [[04-sub-agent-registry|[4. The Sub-Agent Registry]]](#4-the-sub-agent-registrynautiluscomposite-skills-agents04-sub-agent-registrymd)
  - [[05-configuration-ensembles|[5. Configuration: How Principals Build Their Ensembles]]](#5-configuration-how-principals-build-their-ensemblesnautiluscomposite-skills-agents05-configuration-ensemblesmd)
  - [[06-coordination-disagreement|[6. Coordination and Disagreement Resolution]]](#6-coordination-and-disagreement-resolutionnautiluscomposite-skills-agents06-coordination-disagreementmd)
  - [[07-economics-combinatorial|[7. Economics of Combinatorial Replication]]](#7-economics-of-combinatorial-replicationnautiluscomposite-skills-agents07-economics-combinatorialmd)
  - [[08-seven-domains|[8. Seven Domains of Application]]](#8-seven-domains-of-applicationnautiluscomposite-skills-agents08-seven-domainsmd)
  - [[09-okwf-integration|[9. Integration with OKWF Infrastructure]]](#9-integration-with-okwf-infrastructurenautiluscomposite-skills-agents09-okwf-integrationmd)
  - [[10-risks|[10. Risks Specific to Composite Architectures]]](#10-risks-specific-to-composite-architecturesnautiluscomposite-skills-agents10-risksmd)
  - [[11-open-questions|[11. Open Questions]]](#11-open-questionsnautiluscomposite-skills-agents11-open-questionsmd)
  - [[12-call-for-collaboration|[12. Call for Collaboration]]](#12-call-for-collaborationnautiluscomposite-skills-agents12-call-for-collaborationmd)
  - [[13-closing|[13. Closing]]](#13-closingnautiluscomposite-skills-agents13-closingmd)
  - [[README|[composite-skills-agents]]](#composite-skills-agentsnautiluscomposite-skills-agentsreadmemd)
  - [[00-question-multiple-mentors|[Du hast gesagt: Важный момент про способности про скилы как один человек професс…]]](#du-hast-gesagt-важный-момент-про-способности-про-скилы-как-один-человек-профессnautiluscomposite-skills-agents-companion-mentors00-question-multiple-mentorsmd)
  - [[01-yogi-metaphor|[Claude hat geantwortet: Это очень тонкое и важное наблюдение.]]](#claude-hat-geantwortet-это-очень-тонкое-и-важное-наблюдениеnautiluscomposite-skills-agents-companion-mentors01-yogi-metaphormd)
  - [[02-what-was-missing-in-paper-6|[Это не Тип 1 — потому что профиль не общий для всей профессии. И это не Тип 4 — …]]](#это-не-тип-1-потому-что-профиль-не-общий-для-всей-профессии-и-это-не-тип-4-nautiluscomposite-skills-agents-companion-mentors02-what-was-missing-in-paper-6md)
  - [[03-the-spectrum|[Какой под-агент (или какие) должны её обработать]]](#какой-под-агент-или-какие-должны-её-обработатьnautiluscomposite-skills-agents-companion-mentors03-the-spectrummd)
  - [[README|[composite-skills-agents-companion-mentors]]](#composite-skills-agents-companion-mentorsnautiluscomposite-skills-agents-companion-mentorsreadmemd)
  - [[00-abstract|[Abstract — The Double-Triangle Architecture]]](#abstract-the-double-triangle-architecturenautilusdouble-triangle-architecture00-abstractmd)
  - [[01-why-single-triangle-incomplete|[1. Why Single-Triangle Models Are Incomplete]]](#1-why-single-triangle-models-are-incompletenautilusdouble-triangle-architecture01-why-single-triangle-incompletemd)
  - [[02-double-triangle-architecture|[2. The Double-Triangle Architecture]]](#2-the-double-triangle-architecturenautilusdouble-triangle-architecture02-double-triangle-architecturemd)
  - [[03-three-inter-layer-protocols|[3. Three Inter-Layer Protocols]]](#3-three-inter-layer-protocolsnautilusdouble-triangle-architecture03-three-inter-layer-protocolsmd)
  - [[04-nautilus-portal-substrate|[4. Nautilus Portal as Reference Substrate]]](#4-nautilus-portal-as-reference-substratenautilusdouble-triangle-architecture04-nautilus-portal-substratemd)
  - [[05-pattern-library-bridge|[5. Pattern Library as Bridge Between Triangles]]](#5-pattern-library-as-bridge-between-trianglesnautilusdouble-triangle-architecture05-pattern-library-bridgemd)
  - [[06-four-deployment-domains|[6. Four Deployment Domains]]](#6-four-deployment-domainsnautilusdouble-triangle-architecture06-four-deployment-domainsmd)
  - [[07-open-questions|[7. Open Questions]]](#7-open-questionsnautilusdouble-triangle-architecture07-open-questionsmd)
  - [[08-call-to-action|[8. Call to Action]]](#8-call-to-actionnautilusdouble-triangle-architecture08-call-to-actionmd)
  - [[09-acknowledgments|[Acknowledgments]]](#acknowledgmentsnautilusdouble-triangle-architecture09-acknowledgmentsmd)
  - [[10-references|[References]]](#referencesnautilusdouble-triangle-architecture10-referencesmd)
  - [[11-glossary|[Appendix A: Glossary]]](#appendix-a-glossarynautilusdouble-triangle-architecture11-glossarymd)
  - [[README|[double-triangle-architecture]]](#double-triangle-architecturenautilusdouble-triangle-architecturereadmemd)
  - [[00-intro|[The Missing Middle Layer Between Chat and Code]]](#the-missing-middle-layer-between-chat-and-codenautilusinfrastructure-layer-b-en00-intromd)
  - [[01-missing-middle-layer|[Why This Document Exists]]](#why-this-document-existsnautilusinfrastructure-layer-b-en01-missing-middle-layermd)
  - [[02-why-document-exists|[Why This Document Exists]]](#why-this-document-existsnautilusinfrastructure-layer-b-en02-why-document-existsmd)
  - [[03-two-layer-stack|[The Two-Layer Stack As It Exists]]](#the-two-layer-stack-as-it-existsnautilusinfrastructure-layer-b-en03-two-layer-stackmd)
  - [[04-whats-missing-layer-b|[What's Missing — Layer B]]](#whats-missing-layer-bnautilusinfrastructure-layer-b-en04-whats-missing-layer-bmd)
  - [[05-why-not-built|[Why This Hasn't Been Built]]](#why-this-hasnt-been-builtnautilusinfrastructure-layer-b-en05-why-not-builtmd)
  - [[06-existing-approximations|[Existing Approximations]]](#existing-approximationsnautilusinfrastructure-layer-b-en06-existing-approximationsmd)
  - [[07-specific-case|[The Specific Case in Front of Us]]](#the-specific-case-in-front-of-usnautilusinfrastructure-layer-b-en07-specific-casemd)
  - [[08-recursive-insight|[The Recursive Insight]]](#the-recursive-insightnautilusinfrastructure-layer-b-en08-recursive-insightmd)
  - [[09-what-industry-will-build|[What Industry Will Likely Build]]](#what-industry-will-likely-buildnautilusinfrastructure-layer-b-en09-what-industry-will-buildmd)
  - [[10-what-not-solved|[What This Document Doesn't Solve]]](#what-this-document-doesnt-solvenautilusinfrastructure-layer-b-en10-what-not-solvedmd)
  - [[11-practical-recommendations|[Practical Recommendations for the Current Project]]](#practical-recommendations-for-the-current-projectnautilusinfrastructure-layer-b-en11-practical-recommendationsmd)
  - [[12-closing|[Closing]]](#closingnautilusinfrastructure-layer-b-en12-closingmd)
  - [[13-acknowledgments-refs|[Acknowledgments]]](#acknowledgmentsnautilusinfrastructure-layer-b-en13-acknowledgments-refsmd)
  - [[README|[infrastructure-layer-b-en]]](#infrastructure-layer-b-ennautilusinfrastructure-layer-b-enreadmemd)
  - [[00-intro|[00 Intro]]](#00-intronautilusinfrastructure-layer-b-ru00-intromd)
  - [[01-zachem-dokument|[Почему этот документ существует]]](#почему-этот-документ-существуетnautilusinfrastructure-layer-b-ru01-zachem-dokumentmd)
  - [[02-dvukhsloynyy-stek|[Двухслойный стек, как он существует]]](#двухслойный-стек-как-он-существуетnautilusinfrastructure-layer-b-ru02-dvukhsloynyy-stekmd)
  - [[03-otsutstvuet-sloy-b|[Что отсутствует — Слой B]]](#что-отсутствует-слой-bnautilusinfrastructure-layer-b-ru03-otsutstvuet-sloy-bmd)
  - [[04-pochemu-ne-postroeno|[Почему это не было построено]]](#почему-это-не-было-построеноnautilusinfrastructure-layer-b-ru04-pochemu-ne-postroenomd)
  - [[05-priblizheniya|[Существующие приближения]]](#существующие-приближенияnautilusinfrastructure-layer-b-ru05-priblizheniyamd)
  - [[06-konkretnyy-sluchay|[Конкретный случай перед нами]]](#конкретный-случай-перед-намиnautilusinfrastructure-layer-b-ru06-konkretnyy-sluchaymd)
  - [[07-rekursivnoe-prozrenie|[Рекурсивное прозрение]]](#рекурсивное-прозрениеnautilusinfrastructure-layer-b-ru07-rekursivnoe-prozreniemd)
  - [[08-promyshlennost-postroit|[Что промышленность вероятно построит]]](#что-промышленность-вероятно-построитnautilusinfrastructure-layer-b-ru08-promyshlennost-postroitmd)
  - [[09-ne-reshaet|[Что этот документ не решает]]](#что-этот-документ-не-решаетnautilusinfrastructure-layer-b-ru09-ne-reshaetmd)
  - [[10-rekomendatsii|[Практические рекомендации для текущего проекта]]](#практические-рекомендации-для-текущего-проектаnautilusinfrastructure-layer-b-ru10-rekomendatsiimd)
  - [[11-zaklyuchenie|[Заключение]]](#заключениеnautilusinfrastructure-layer-b-ru11-zaklyucheniemd)
  - [[12-blagodarnosti-ssylki|[Благодарности]]](#благодарностиnautilusinfrastructure-layer-b-ru12-blagodarnosti-ssylkimd)
  - [[README|[infrastructure-layer-b-ru]]](#infrastructure-layer-b-runautilusinfrastructure-layer-b-rureadmemd)
  - [[01-cowork-discovery|[1. The Cowork Discovery and Why It Changes Everything]]](#1-the-cowork-discovery-and-why-it-changes-everythingnautilusingit-cowork-en01-cowork-discoverymd)
  - [[02-cowork-provides|[2. What Cowork Provides That InGit Doesn't Need to Build]]](#2-what-cowork-provides-that-ingit-doesnt-need-to-buildnautilusingit-cowork-en02-cowork-providesmd)
  - [[03-ingit-provides|[3. What InGit Provides That Cowork Lacks]]](#3-what-ingit-provides-that-cowork-lacksnautilusingit-cowork-en03-ingit-providesmd)
  - [[04-symbiotic-architecture|[4. The Symbiotic Architecture]]](#4-the-symbiotic-architecturenautilusingit-cowork-en04-symbiotic-architecturemd)
  - [[05-four-integration-paths|[5. Four Integration Paths in Order of Accessibility]]](#5-four-integration-paths-in-order-of-accessibilitynautilusingit-cowork-en05-four-integration-pathsmd)
  - [[06-refined-ingit-scope|[6. Refined InGit Scope with Cowork in Mind]]](#6-refined-ingit-scope-with-cowork-in-mindnautilusingit-cowork-en06-refined-ingit-scopemd)
  - [[07-practical-first-steps|[7. Practical First Steps This Month]]](#7-practical-first-steps-this-monthnautilusingit-cowork-en07-practical-first-stepsmd)
  - [[08-implications-nautilus-okwf|[8. Implications for Nautilus and OKWF]]](#8-implications-for-nautilus-and-okwfnautilusingit-cowork-en08-implications-nautilus-okwfmd)
  - [[09-risks-open-questions|[9. Risks and Open Questions]]](#9-risks-and-open-questionsnautilusingit-cowork-en09-risks-open-questionsmd)
  - [[10-strategic-positioning|[10. Strategic Positioning]]](#10-strategic-positioningnautilusingit-cowork-en10-strategic-positioningmd)
  - [[README|[ingit-cowork-en]]](#ingit-cowork-ennautilusingit-cowork-enreadmemd)
  - [[01-otkrytie-cowork|[1. Открытие Cowork и почему это меняет всё]]](#1-открытие-cowork-и-почему-это-меняет-всёnautilusingit-cowork-ru01-otkrytie-coworkmd)
  - [[02-chto-cowork-obespechivaet|[2. Что Cowork обеспечивает, что InGit не нужно строить]]](#2-что-cowork-обеспечивает-что-ingit-не-нужно-строитьnautilusingit-cowork-ru02-chto-cowork-obespechivaetmd)
  - [[03-chto-ingit-obespechivaet|[3. Что InGit обеспечивает, чего Cowork не хватает]]](#3-что-ingit-обеспечивает-чего-cowork-не-хватаетnautilusingit-cowork-ru03-chto-ingit-obespechivaetmd)
  - [[04-simbioticheskaya-arkhitektura|[4. Симбиотическая Архитектура]]](#4-симбиотическая-архитектураnautilusingit-cowork-ru04-simbioticheskaya-arkhitekturamd)
  - [[05-chetyre-puti-integratsii|[5. Четыре пути интеграции в порядке доступности]]](#5-четыре-пути-интеграции-в-порядке-доступностиnautilusingit-cowork-ru05-chetyre-puti-integratsiimd)
  - [[06-utochnyonnyy-obyom-ingit|[6. Уточнённый объём InGit с учётом Cowork]]](#6-уточнённый-объём-ingit-с-учётом-coworknautilusingit-cowork-ru06-utochnyonnyy-obyom-ingitmd)
  - [[07-prakticheskie-shagi|[7. Практические первые шаги в этом месяце]]](#7-практические-первые-шаги-в-этом-месяцеnautilusingit-cowork-ru07-prakticheskie-shagimd)
  - [[08-implikatsii-nautilus-okwf|[8. Импликации для Nautilus и OKWF]]](#8-импликации-для-nautilus-и-okwfnautilusingit-cowork-ru08-implikatsii-nautilus-okwfmd)
  - [[09-riski-voprosy|[9. Риски и Открытые Вопросы]]](#9-риски-и-открытые-вопросыnautilusingit-cowork-ru09-riski-voprosymd)
  - [[10-strategicheskoe-pozitsionirovanie|[10. Стратегическое Позиционирование]]](#10-стратегическое-позиционированиеnautilusingit-cowork-ru10-strategicheskoe-pozitsionirovaniemd)
  - [[README|[ingit-cowork-ru]]](#ingit-cowork-runautilusingit-cowork-rureadmemd)
  - [[00-question-innovations-transitions|[Du hast gesagt: Интересно как новая как инновация как как рационализация как пер…]]](#du-hast-gesagt-интересно-как-новая-как-инновация-как-как-рационализация-как-перnautilusinnovation-transitions00-question-innovations-transitionsmd)
  - [[01-response|[Claude hat geantwortet: Отличный запрос.]]](#claude-hat-geantwortet-отличный-запросnautilusinnovation-transitions01-responsemd)
  - [[README|[innovation-transitions]]](#innovation-transitionsnautilusinnovation-transitionsreadmemd)
  - [[00-question-multi-tier|[Du hast gesagt: Ещё есть такие вопросы то есть если общие юридические Наутилус м…]]](#du-hast-gesagt-ещё-есть-такие-вопросы-то-есть-если-общие-юридические-наутилус-мnautilusmulti-tier-architecture00-question-multi-tiermd)
  - [[01-strategic-significance|[Claude hat geantwortet: Это стратегически значимый вопрос, и ответ на него — да,…]]](#claude-hat-geantwortet-это-стратегически-значимый-вопрос-и-ответ-на-него-даnautilusmulti-tier-architecture01-strategic-significancemd)
  - [[README|[multi-tier-architecture]]](#multi-tier-architecturenautilusmulti-tier-architecturereadmemd)
  - [[00-question-can-it-apply-to-docs|[Du hast gesagt: Вопрос такой вопрос и такие а можно ли этот протокол это система…]]](#du-hast-gesagt-вопрос-такой-вопрос-и-такие-а-можно-ли-этот-протокол-это-системаnautilusnpp-humanitarian-extension00-question-can-it-apply-to-docsmd)
  - [[01-structural-comparison-code-vs-docs|[Структурное сравнение: код vs гуманитарные документы]]](#структурное-сравнение-код-vs-гуманитарные-документыnautilusnpp-humanitarian-extension01-structural-comparison-code-vs-docsmd)
  - [[02-mcp-claude-desktop-use-cases|[Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы …]]](#что-он-даёт-вам-на-практике-через-mcp-claude-desktop-может-ответить-на-запросы-nautilusnpp-humanitarian-extension02-mcp-claude-desktop-use-casesmd)
  - [[03-what-doesnt-exist-on-market|[Что не существует на рынке:]]](#что-не-существует-на-рынкеnautilusnpp-humanitarian-extension03-what-doesnt-exist-on-marketmd)
  - [[04-grant-opportunities|[Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access t…]]](#horizon-europe-cluster-3-civil-security-for-society-пересекается-с-access-tnautilusnpp-humanitarian-extension04-grant-opportunitiesmd)
  - [[05-which-combination-more-valuable|[Что из этого сейчас кажется более ценным? Или какая-то своя комбинация?]]](#что-из-этого-сейчас-кажется-более-ценным-или-какая-то-своя-комбинацияnautilusnpp-humanitarian-extension05-which-combination-more-valuablemd)
  - [[README|[npp-humanitarian-extension]]](#npp-humanitarian-extensionnautilusnpp-humanitarian-extensionreadmemd)
  - [[00-abstract-status|[Abstract + Status of This Document]]](#abstract-status-of-this-documentnautilusnpp-v1-000-abstract-statusmd)
  - [[01-introduction|[1. Introduction (Motivation, Design Goals, Non-Goals, Terminology)]]](#1-introduction-motivation-design-goals-non-goals-terminologynautilusnpp-v1-001-introductionmd)
  - [[02-terminology|[2. Terminology]]](#2-terminologynautilusnpp-v1-002-terminologymd)
  - [[03-registry|3. Registry (nautilus.[json)]]](#3-registry-nautilusjsonnautilusnpp-v1-003-registrymd)
  - [[04-passport|[4. Passport (passport.md)]]](#4-passport-passportmdnautilusnpp-v1-004-passportmd)
  - [[05-compatibility-levels|[5. Compatibility Levels]]](#5-compatibility-levelsnautilusnpp-v1-005-compatibility-levelsmd)
  - [[06-adapter-interface|[6. Adapter Interface]]](#6-adapter-interfacenautilusnpp-v1-006-adapter-interfacemd)
  - [[07-portal-entry|7. [PortalEntry Structure]]](#7-portalentry-structurenautilusnpp-v1-007-portal-entrymd)
  - [[08-consensus-algorithm|[8. Consensus Algorithm (v1.0: string normalization)]]](#8-consensus-algorithm-v10-string-normalizationnautilusnpp-v1-008-consensus-algorithmmd)
  - [[09-query-flow|[9. Query Flow]]](#9-query-flownautilusnpp-v1-009-query-flowmd)
  - [[10-query-result|10. [QueryResult Structure]]](#10-queryresult-structurenautilusnpp-v1-010-query-resultmd)
  - [[11-security-considerations|[11. Security Considerations]]](#11-security-considerationsnautilusnpp-v1-011-security-considerationsmd)
  - [[12-versioning-policy|[12. Versioning Policy]]](#12-versioning-policynautilusnpp-v1-012-versioning-policymd)
  - [[13-reference-implementation|[13. Reference Implementation]]](#13-reference-implementationnautilusnpp-v1-013-reference-implementationmd)
  - [[14-adr-001-federation-over-merging|[14. ADR-001: Federation over Merging]]](#14-adr-001-federation-over-mergingnautilusnpp-v1-014-adr-001-federation-over-mergingmd)
  - [[15-glossary|[15. Glossary of Examples]]](#15-glossary-of-examplesnautilusnpp-v1-015-glossarymd)
  - [[16-appendix-a-minimal-working-example|[Appendix A: Minimal Working Example]]](#appendix-a-minimal-working-examplenautilusnpp-v1-016-appendix-a-minimal-working-examplemd)
  - [[17-appendix-b-change-log|[Appendix B: Change Log]]](#appendix-b-change-lognautilusnpp-v1-017-appendix-b-change-logmd)
  - [[18-comment-on-document|[Комментарий: дизайн-решения NPP v1.0]]](#комментарий-дизайн-решения-npp-v10nautilusnpp-v1-018-comment-on-documentmd)
  - [[README|[npp-v1-0]]](#npp-v1-0nautilusnpp-v1-0readmemd)
  - [[00-abstract-status|[Abstract + Status of This Document]]](#abstract-status-of-this-documentnautilusnpp-v1-100-abstract-statusmd)
  - [[01-introduction|[1. Introduction (Motivation, Design Goals, Non-Goals, Terminology, Changes from v1.0)]]](#1-introduction-motivation-design-goals-non-goals-terminology-changes-from-v10nautilusnpp-v1-101-introductionmd)
  - [[02-terminology|[2. Terminology]]](#2-terminologynautilusnpp-v1-102-terminologymd)
  - [[03-registry|3. Registry (nautilus.[json)]]](#3-registry-nautilusjsonnautilusnpp-v1-103-registrymd)
  - [[04-passport|[4. Passport (passport.md)]]](#4-passport-passportmdnautilusnpp-v1-104-passportmd)
  - [[05-compatibility-levels|[5. Compatibility Levels]]](#5-compatibility-levelsnautilusnpp-v1-105-compatibility-levelsmd)
  - [[06-adapter-interface|[6. Adapter Interface]]](#6-adapter-interfacenautilusnpp-v1-106-adapter-interfacemd)
  - [[07-portal-entry|7. [PortalEntry Structure]]](#7-portalentry-structurenautilusnpp-v1-107-portal-entrymd)
  - [[08-q6-space|[8. Q6 Space (Normative)]]](#8-q6-space-normativenautilusnpp-v1-108-q6-spacemd)
  - [[09-consensus-algorithm|[9. Consensus Algorithm]]](#9-consensus-algorithmnautilusnpp-v1-109-consensus-algorithmmd)
  - [[10-query-flow|[10. Query Flow]]](#10-query-flownautilusnpp-v1-110-query-flowmd)
  - [[11-relevance-ranking|[11. Relevance Ranking]]](#11-relevance-rankingnautilusnpp-v1-111-relevance-rankingmd)
  - [[12-onboarding-paths|[12. Onboarding Paths (Normative)]]](#12-onboarding-paths-normativenautilusnpp-v1-112-onboarding-pathsmd)
  - [[13-rest-api|[13. REST API Contract (Normative for Portals)]]](#13-rest-api-contract-normative-for-portalsnautilusnpp-v1-113-rest-apimd)
  - [[14-sdk|[14. SDK Contract (Informative)]]](#14-sdk-contract-informativenautilusnpp-v1-114-sdkmd)
  - [[15-security|[15. Security Considerations]]](#15-security-considerationsnautilusnpp-v1-115-securitymd)
  - [[16-mcp-extension|[16. MCP Extension (Informative)]]](#16-mcp-extension-informativenautilusnpp-v1-116-mcp-extensionmd)
  - [[17-versioning-policy|[17. Versioning Policy]]](#17-versioning-policynautilusnpp-v1-117-versioning-policymd)
  - [[18-reference-implementation|[18. Reference Implementation]]](#18-reference-implementationnautilusnpp-v1-118-reference-implementationmd)
  - [[19-adr-001-federation-over-merging|[19. ADR-001: Federation over Merging]]](#19-adr-001-federation-over-mergingnautilusnpp-v1-119-adr-001-federation-over-mergingmd)
  - [[20-adr-002-q6-first-class|[20. ADR-002: Q6 as First-Class Protocol Concept]]](#20-adr-002-q6-as-first-class-protocol-conceptnautilusnpp-v1-120-adr-002-q6-first-classmd)
  - [[21-adr-003-five-onboarding-paths|[21. ADR-003: Five Onboarding Paths as Equal-Rank]]](#21-adr-003-five-onboarding-paths-as-equal-ranknautilusnpp-v1-121-adr-003-five-onboarding-pathsmd)
  - [[22-glossary|[22. Glossary of Reference Examples]]](#22-glossary-of-reference-examplesnautilusnpp-v1-122-glossarymd)
  - [[README|[npp-v1-1]]](#npp-v1-1nautilusnpp-v1-1readmemd)
  - [[00-abstract|[AI-Coordinated Infrastructure for Distributed Expert Contribution]]](#ai-coordinated-infrastructure-for-distributed-expert-contributionnautilusokwf-concept00-abstractmd)
  - [[01-problem-statement|[1. Problem Statement]]](#1-problem-statementnautilusokwf-concept01-problem-statementmd)
  - [[02-target-populations|[2. Target Populations]]](#2-target-populationsnautilusokwf-concept02-target-populationsmd)
  - [[03-why-existing-fail|[3. Why Existing Solutions Fail]]](#3-why-existing-solutions-failnautilusokwf-concept03-why-existing-failmd)
  - [[04-proposed-infrastructure|[4. Proposed Infrastructure]]](#4-proposed-infrastructurenautilusokwf-concept04-proposed-infrastructuremd)
  - [[05-economic-model|[5. Economic Model]]](#5-economic-modelnautilusokwf-concept05-economic-modelmd)
  - [[06-governance-ethics|[6. Governance and Ethics]]](#6-governance-and-ethicsnautilusokwf-concept06-governance-ethicsmd)
  - [[07-phased-rollout|[7. Phased Rollout Plan]]](#7-phased-rollout-plannautilusokwf-concept07-phased-rolloutmd)
  - [[08-risk-analysis|[8. Risk Analysis]]](#8-risk-analysisnautilusokwf-concept08-risk-analysismd)
  - [[09-call-for-partnership|[9. Call for Partnership]]](#9-call-for-partnershipnautilusokwf-concept09-call-for-partnershipmd)
  - [[10-appendices|[10. Appendices]]](#10-appendicesnautilusokwf-concept10-appendicesmd)
  - [[README|[okwf-concept]]](#okwf-conceptnautilusokwf-conceptreadmemd)
  - [[00-question-anonymization|[Du hast gesagt: Насчёт приватности Я думаю что возможно удалять только личные да…]]](#du-hast-gesagt-насчёт-приватности-я-думаю-что-возможно-удалять-только-личные-даnautilusprivacy-federation00-question-anonymizationmd)
  - [[01-what-to-anonymize-german-standard|[Что именно анонимизировать: немецкий стандарт]]](#что-именно-анонимизировать-немецкий-стандартnautilusprivacy-federation01-what-to-anonymize-german-standardmd)
  - [[02-two-tier-publication|[Архитектурное решение: две-уровневая публикация]]](#архитектурное-решение-две-уровневая-публикацияnautilusprivacy-federation02-two-tier-publicationmd)
  - [[03-what-this-gives-technically|[Что это даёт технически]]](#что-это-даёт-техническиnautilusprivacy-federation03-what-this-gives-technicallymd)
  - [[04-what-i-can-do-now|[Что я могу сделать сейчас]]](#что-я-могу-сделать-сейчасnautilusprivacy-federation04-what-i-can-do-nowmd)
  - [[README|[privacy-federation]]](#privacy-federationnautilusprivacy-federationreadmemd)
  - [[00-abstract|[Professional Colleague Agents]]](#professional-colleague-agentsnautilusprofessional-colleague-agents-en00-abstractmd)
  - [[01-five-type-typology|[1. The Five-Type Typology of Principal-Side Agents]]](#1-the-five-type-typology-of-principal-side-agentsnautilusprofessional-colleague-agents-en01-five-type-typologymd)
  - [[02-what-makes-pca|[2. What Makes a Professional Colleague Agent]]](#2-what-makes-a-professional-colleague-agentnautilusprofessional-colleague-agents-en02-what-makes-pcamd)
  - [[03-empirical-case-obuchay|[3. Empirical Case Study: «Обучай»]]](#3-empirical-case-study-обучайnautilusprofessional-colleague-agents-en03-empirical-case-obuchaymd)
  - [[04-architecture|[4. Architecture of Professional Colleague Agents]]](#4-architecture-of-professional-colleague-agentsnautilusprofessional-colleague-agents-en04-architecturemd)
  - [[05-economics-replication|[5. The Economics of Profession-Wide Replication]]](#5-the-economics-of-profession-wide-replicationnautilusprofessional-colleague-agents-en05-economics-replicationmd)
  - [[06-risks|[6. Risks Specific to this Category]]](#6-risks-specific-to-this-categorynautilusprofessional-colleague-agents-en06-risksmd)
  - [[07-application-domains|[7. Application Domains]]](#7-application-domainsnautilusprofessional-colleague-agents-en07-application-domainsmd)
  - [[08-pilot-sgb-advocate|[8. Pilot Proposal: SGB Advocate Colleague]]](#8-pilot-proposal-sgb-advocate-colleaguenautilusprofessional-colleague-agents-en08-pilot-sgb-advocatemd)
  - [[09-relationship-other-agents|[9. Relationship to Other Agent Types]]](#9-relationship-to-other-agent-typesnautilusprofessional-colleague-agents-en09-relationship-other-agentsmd)
  - [[10-open-questions|[10. Open Questions]]](#10-open-questionsnautilusprofessional-colleague-agents-en10-open-questionsmd)
  - [[11-call-for-collaboration|[11. Call for Collaboration]]](#11-call-for-collaborationnautilusprofessional-colleague-agents-en11-call-for-collaborationmd)
  - [[12-closing|[12. Closing]]](#12-closingnautilusprofessional-colleague-agents-en12-closingmd)
  - [[README|[professional-colleague-agents-en]]](#professional-colleague-agents-ennautilusprofessional-colleague-agents-enreadmemd)
  - [[00-abstract|[Содержание]]](#содержаниеnautilusprofessional-colleague-agents-ru00-abstractmd)
  - [[01-pyat-tipov|[1. Типология из пяти типов агентов на стороне принципала]]](#1-типология-из-пяти-типов-агентов-на-стороне-принципалаnautilusprofessional-colleague-agents-ru01-pyat-tipovmd)
  - [[02-chto-delaet-pka|[2. Что делает агента Профессиональным Коллегой]]](#2-что-делает-агента-профессиональным-коллегойnautilusprofessional-colleague-agents-ru02-chto-delaet-pkamd)
  - [[03-keys-obuchay|[3. Эмпирический кейс: «Обучай»]]](#3-эмпирический-кейс-обучайnautilusprofessional-colleague-agents-ru03-keys-obuchaymd)
  - [[04-arkhitektura|[4. Архитектура Профессиональных Коллег-Агентов]]](#4-архитектура-профессиональных-коллег-агентовnautilusprofessional-colleague-agents-ru04-arkhitekturamd)
  - [[05-ekonomika|[5. Экономика тиражирования по профессии]]](#5-экономика-тиражирования-по-профессииnautilusprofessional-colleague-agents-ru05-ekonomikamd)
  - [[06-riski|[6. Риски, специфичные для этой категории]]](#6-риски-специфичные-для-этой-категорииnautilusprofessional-colleague-agents-ru06-riskimd)
  - [[07-oblasti-primeneniya|[7. Области применения]]](#7-области-примененияnautilusprofessional-colleague-agents-ru07-oblasti-primeneniyamd)
  - [[08-pilot-sgb-kolega|[8. Пилотное предложение: SGB Колega-Адвокат]]](#8-пилотное-предложение-sgb-колega-адвокатnautilusprofessional-colleague-agents-ru08-pilot-sgb-kolegamd)
  - [[09-svyaz-s-drugimi|[9. Связь с другими типами агентов]]](#9-связь-с-другими-типами-агентовnautilusprofessional-colleague-agents-ru09-svyaz-s-drugimimd)
  - [[10-otkrytye-voprosy|[10. Открытые вопросы]]](#10-открытые-вопросыnautilusprofessional-colleague-agents-ru10-otkrytye-voprosymd)
  - [[11-prizyv-k-sotrudnichestvu|[11. Призыв к сотрудничеству]]](#11-призыв-к-сотрудничествуnautilusprofessional-colleague-agents-ru11-prizyv-k-sotrudnichestvumd)
  - [[12-zaklyuchenie|[12. Заключение]]](#12-заключениеnautilusprofessional-colleague-agents-ru12-zaklyucheniemd)
  - [[README|[professional-colleague-agents-ru]]](#professional-colleague-agents-runautilusprofessional-colleague-agents-rureadmemd)
  - [[00-abstract|[AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]](#ai-mediated-representation-for-underrepresented-experts-and-vulnerable-populationsnautilusrepresentative-agent-layer-en00-abstractmd)
  - [[01-cinderella-syndrome|[1. The Cinderella Syndrome: Why Quality Stays Invisible]]](#1-the-cinderella-syndrome-why-quality-stays-invisiblenautilusrepresentative-agent-layer-en01-cinderella-syndromemd)
  - [[02-historical-precedents|[2. Historical Precedents: Agents as Civilizational Innovation]]](#2-historical-precedents-agents-as-civilizational-innovationnautilusrepresentative-agent-layer-en02-historical-precedentsmd)
  - [[03-what-makes-representative-agent|[3. What Makes a Representative Agent]]](#3-what-makes-a-representative-agentnautilusrepresentative-agent-layer-en03-what-makes-representative-agentmd)
  - [[04-ten-domains|[4. Ten Domains of Application]]](#4-ten-domains-of-applicationnautilusrepresentative-agent-layer-en04-ten-domainsmd)
  - [[05-architectural-specification|[5. Architectural Specification]]](#5-architectural-specificationnautilusrepresentative-agent-layer-en05-architectural-specificationmd)
  - [[06-ethical-framework|[6. Ethical Framework]]](#6-ethical-frameworknautilusrepresentative-agent-layer-en06-ethical-frameworkmd)
  - [[07-governance-oversight|[7. Governance and Oversight]]](#7-governance-and-oversightnautilusrepresentative-agent-layer-en07-governance-oversightmd)
  - [[08-risks-mitigations|[8. Risks and Mitigations]]](#8-risks-and-mitigationsnautilusrepresentative-agent-layer-en08-risks-mitigationsmd)
  - [[09-phased-rollout|[9. Phased Rollout Strategy]]](#9-phased-rollout-strategynautilusrepresentative-agent-layer-en09-phased-rolloutmd)
  - [[10-open-questions|[10. Open Questions]]](#10-open-questionsnautilusrepresentative-agent-layer-en10-open-questionsmd)
  - [[11-call-for-collaboration|[11. Call for Collaboration]]](#11-call-for-collaborationnautilusrepresentative-agent-layer-en11-call-for-collaborationmd)
  - [[12-closing|[12. Closing]]](#12-closingnautilusrepresentative-agent-layer-en12-closingmd)
  - [[README|[representative-agent-layer-en]]](#representative-agent-layer-ennautilusrepresentative-agent-layer-enreadmemd)
  - [[00-abstract|[Содержание]]](#содержаниеnautilusrepresentative-agent-layer-ru00-abstractmd)
  - [[01-sindrom-zolushki|[1. Синдром Золушки: Почему качество остаётся невидимым]]](#1-синдром-золушки-почему-качество-остаётся-невидимымnautilusrepresentative-agent-layer-ru01-sindrom-zolushkimd)
  - [[02-istoricheskie-pretsedenty|[2. Исторические прецеденты: Агенты как цивилизационная инновация]]](#2-исторические-прецеденты-агенты-как-цивилизационная-инновацияnautilusrepresentative-agent-layer-ru02-istoricheskie-pretsedentymd)
  - [[03-chto-delaet-predstavitelskim|[3. Что делает агента Представительским]]](#3-что-делает-агента-представительскимnautilusrepresentative-agent-layer-ru03-chto-delaet-predstavitelskimmd)
  - [[04-desyat-oblastey|[4. Десять областей применения]]](#4-десять-областей-примененияnautilusrepresentative-agent-layer-ru04-desyat-oblasteymd)
  - [[05-arkhitekturnaya-spetsifikatsiya|[5. Архитектурная спецификация]]](#5-архитектурная-спецификацияnautilusrepresentative-agent-layer-ru05-arkhitekturnaya-spetsifikatsiyamd)
  - [[06-eticheskaya-ramka|[6. Этическая рамка]]](#6-этическая-рамкаnautilusrepresentative-agent-layer-ru06-eticheskaya-ramkamd)
  - [[07-upravlenie-nadzor|[7. Управление и надзор]]](#7-управление-и-надзорnautilusrepresentative-agent-layer-ru07-upravlenie-nadzormd)
  - [[08-riski-mery|[8. Риски и меры противодействия]]](#8-риски-и-меры-противодействияnautilusrepresentative-agent-layer-ru08-riski-merymd)
  - [[09-strategiya-razvyortyvaniya|[9. Стратегия поэтапного развёртывания]]](#9-стратегия-поэтапного-развёртыванияnautilusrepresentative-agent-layer-ru09-strategiya-razvyortyvaniyamd)
  - [[10-otkrytye-voprosy|[10. Открытые вопросы]]](#10-открытые-вопросыnautilusrepresentative-agent-layer-ru10-otkrytye-voprosymd)
  - [[11-prizyv-k-sotrudnichestvu|[11. Призыв к сотрудничеству]]](#11-призыв-к-сотрудничествуnautilusrepresentative-agent-layer-ru11-prizyv-k-sotrudnichestvumd)
  - [[12-zaklyuchenie|[12. Заключение]]](#12-заключениеnautilusrepresentative-agent-layer-ru12-zaklyucheniemd)
  - [[README|[representative-agent-layer-ru]]](#representative-agent-layer-runautilusrepresentative-agent-layer-rureadmemd)
  - [[00-tldr|[TL;DR — Трёхфазная методология Review]]](#tldr-трёхфазная-методология-reviewnautilusreview-methodology00-tldrmd)
  - [[01-context-motivation|[1. Контекст и мотивация]]](#1-контекст-и-мотивацияnautilusreview-methodology01-context-motivationmd)
  - [[02-formal-workflow|[2. Формальный workflow]]](#2-формальный-workflownautilusreview-methodology02-formal-workflowmd)
  - [[03-consolidation-principles|[3. Принципы консолидации (Фаза C)]]](#3-принципы-консолидации-фаза-cnautilusreview-methodology03-consolidation-principlesmd)
  - [[04-fallback-ratio-question|[Вопрос: fallback‑ratio как критический или осмысленный?]]](#вопрос-fallbackratio-как-критический-или-осмысленныйnautilusreview-methodology04-fallback-ratio-questionmd)
  - [[05-conditions-of-applicability|[4. Условия применимости]]](#4-условия-применимостиnautilusreview-methodology05-conditions-of-applicabilitymd)
  - [[06-relation-existing-methodologies|[5. Связь с существующими методологиями]]](#5-связь-с-существующими-методологиямиnautilusreview-methodology06-relation-existing-methodologiesmd)
  - [[07-why-valid-for-ai|[6. Почему это валидный паттерн для AI‑assisted workflows]]](#6-почему-это-валидный-паттерн-для-aiassisted-workflowsnautilusreview-methodology07-why-valid-for-aimd)
  - [[08-implementation-nautilus|[7. Реализация в проекте Nautilus]]](#7-реализация-в-проекте-nautilusnautilusreview-methodology08-implementation-nautilusmd)
  - [[09-limitations-open-questions|[8. Ограничения и открытые вопросы]]](#8-ограничения-и-открытые-вопросыnautilusreview-methodology09-limitations-open-questionsmd)
  - [[10-checklist|[9. Checklist применения методологии]]](#9-checklist-применения-методологииnautilusreview-methodology10-checklistmd)
  - [[11-application-plan-current-docs|[10. Конкретный план применения к текущим документам]]](#10-конкретный-план-применения-к-текущим-документамnautilusreview-methodology11-application-plan-current-docsmd)
  - [[12-appendix-a-header-warning|[Appendix A: Шаблон для header warning]]](#appendix-a-шаблон-для-header-warningnautilusreview-methodology12-appendix-a-header-warningmd)
  - [[13-appendix-b-examples|[Appendix B: Примеры расхождений и их разрешения]]](#appendix-b-примеры-расхождений-и-их-разрешенияnautilusreview-methodology13-appendix-b-examplesmd)
  - [[14-main-technical-risks|[Главные технические риски]]](#главные-технические-рискиnautilusreview-methodology14-main-technical-risksmd)
  - [[15-appendix-c-history|[Appendix C: История изменений методологии]]](#appendix-c-история-изменений-методологииnautilusreview-methodology15-appendix-c-historymd)
  - [[16-glossary|[Глоссарий]]](#глоссарийnautilusreview-methodology16-glossarymd)
  - [[README|[review-methodology]]](#review-methodologynautilusreview-methodologyreadmemd)
  - [[00-question-supply-demand|[Du hast gesagt: Спрос рождает предложение - это простая экономическая истина нач…]]](#du-hast-gesagt-спрос-рождает-предложение---это-простая-экономическая-истина-начnautilussupply-demand00-question-supply-demandmd)
  - [[01-three-related-themes|[Claude hat geantwortet: Очень богатый вопрос — три разных, но связанных темы.]]](#claude-hat-geantwortet-очень-богатый-вопрос-три-разных-но-связанных-темыnautilussupply-demand01-three-related-themesmd)
  - [[README|[supply-demand]]](#supply-demandnautilussupply-demandreadmemd)
  - [[00-question-mountain-to-person|[Du hast gesagt: Того если гора не идёт человеку может быть этот человек пойдёт к…]]](#du-hast-gesagt-того-если-гора-не-идёт-человеку-может-быть-этот-человек-пойдёт-кnautilustransmission-box00-question-mountain-to-personmd)
  - [[01-completing-loop|[Claude hat geantwortet: Это исключительно богатый вопрос, и я хочу ответить на н…]]](#claude-hat-geantwortet-это-исключительно-богатый-вопрос-и-я-хочу-ответить-на-нnautilustransmission-box01-completing-loopmd)
  - [[README|[transmission-box]]](#transmission-boxnautilustransmission-boxreadmemd)
- [Processing Guide](#processing-guide)
  - [[01-overview|[Обработка больших массивов информации — Часть 1: Обзор и таксономия]]](#обработка-больших-массивов-информации-часть-1-обзор-и-таксономияprocessing-guide01-overviewmd)
  - [[02-extraction|[Обработка больших массивов — Часть 2: Извлечение]]](#обработка-больших-массивов-часть-2-извлечениеprocessing-guide02-extractionmd)
  - [[03-chunking|[Обработка больших массивов — Часть 3: Разбивка и чанкинг]]](#обработка-больших-массивов-часть-3-разбивка-и-чанкингprocessing-guide03-chunkingmd)
  - [[04-structuring|[Обработка больших массивов — Часть 4: Структурирование]]](#обработка-больших-массивов-часть-4-структурированиеprocessing-guide04-structuringmd)
  - [[05-analysis|[Обработка больших массивов — Часть 5: Анализ и NLP]]](#обработка-больших-массивов-часть-5-анализ-и-nlpprocessing-guide05-analysismd)
  - [[06-search|[Обработка больших массивов — Часть 6: Поиск]]](#обработка-больших-массивов-часть-6-поискprocessing-guide06-searchmd)
  - [[07-llm|[Обработка больших массивов — Часть 7: LLM-обогащение]]](#обработка-больших-массивов-часть-7-llm-обогащениеprocessing-guide07-llmmd)
  - [[08-export|[Обработка больших массивов — Часть 8: Экспорт и интеграции]]](#обработка-больших-массивов-часть-8-экспорт-и-интеграцииprocessing-guide08-exportmd)
  - [[09-automation|[Обработка больших массивов — Часть 9: Автоматизация]]](#обработка-больших-массивов-часть-9-автоматизацияprocessing-guide09-automationmd)
  - [[10-future|[Обработка больших массивов — Часть 10: Инновационные подходы]]](#обработка-больших-массивов-часть-10-инновационные-подходыprocessing-guide10-futuremd)
  - [[PROCESSING_GUIDE|[Обработка больших массивов документов — Полное руководство]]](#обработка-больших-массивов-документов-полное-руководствоprocessing-guideprocessing_guidemd)
  - [[QA|[Q&A: processing-guide]]](#qa-processing-guideprocessing-guideqamd)
  - [[README|[processing-guide]]](#processing-guideprocessing-guidereadmemd)
- [Svyazi 2 0](#svyazi-2-0)
  - [[README|[Svyazi 2.0 — тематический индекс]]](#svyazi-20-тематический-индексsvyazi-2-0readmemd)
  - [[README|[architecture]]](#architecturesvyazi-2-0architecturereadmemd)
  - [[card-envelope|[Card Envelope]]](#card-envelopesvyazi-2-0architecturecard-envelopemd)
  - [[evidence-envelope|[Evidence Envelope]]](#evidence-envelopesvyazi-2-0architectureevidence-envelopemd)
  - [[gaps|[Архитектурные зазоры]]](#архитектурные-зазорыsvyazi-2-0architecturegapsmd)
  - [[integration-spec|[Интеграционная спецификация (минимум для MVP)]]](#интеграционная-спецификация-минимум-для-mvpsvyazi-2-0architectureintegration-specmd)
  - [[memory-write-policy|[Memory Write Policy]]](#memory-write-policysvyazi-2-0architecturememory-write-policymd)
  - [[review-record|[Review Record]]](#review-recordsvyazi-2-0architecturereview-recordmd)
  - [[skill-tool-policy|[Skill and Tool Policy]]](#skill-and-tool-policysvyazi-2-0architectureskill-tool-policymd)
  - [[README|[components]]](#componentssvyazi-2-0componentsreadmemd)
  - [[agent-memory-mcp|agent-memory-[mcp + Memory OS]]](#agent-memory-mcp-memory-ossvyazi-2-0componentsagent-memory-mcpmd)
  - [[agentfs|[AgentFS]]](#agentfssvyazi-2-0componentsagentfsmd)
  - [[ai-factory|[AI Factory + AIF Handoff]]](#ai-factory-aif-handoffsvyazi-2-0componentsai-factorymd)
  - [[autoresearch-sequential|[AutoResearch + Sequential]]](#autoresearch-sequentialsvyazi-2-0componentsautoresearch-sequentialmd)
  - [[graph-rag|[Graph RAG]]](#graph-ragsvyazi-2-0componentsgraph-ragmd)
  - [[hybrid-rag|[Hybrid RAG knowledge base]]](#hybrid-rag-knowledge-basesvyazi-2-0componentshybrid-ragmd)
  - [[knowledge-space|[knowledge-space]]](#knowledge-spacesvyazi-2-0componentsknowledge-spacemd)
  - [[legal-rag|[Legal RAG]]](#legal-ragsvyazi-2-0componentslegal-ragmd)
  - [[mclaude|[mclaude]]](#mclaudesvyazi-2-0componentsmclaudemd)
  - [[memnet|[MemNet / memory-is-all-you-need]]](#memnet-memory-is-all-you-needsvyazi-2-0componentsmemnetmd)
  - [[ngt-memory|[NGT Memory]]](#ngt-memorysvyazi-2-0componentsngt-memorymd)
  - [[research-docs-liteparse|[research-docs + LiteParse]]](#research-docs-liteparsesvyazi-2-0componentsresearch-docs-liteparsemd)
  - [[rufler|[Rufler]]](#ruflersvyazi-2-0componentsruflermd)
  - [[security-routing-plane|[Security + routing plane]]](#security-routing-planesvyazi-2-0componentssecurity-routing-planemd)
  - [[self-aware-mcp|[Self‑Aware MCP + Skills + CodeWiki]]](#selfaware-mcp-skills-codewikisvyazi-2-0componentsself-aware-mcpmd)
  - [[svyazi|[Svyazi]]](#svyazisvyazi-2-0componentssvyazimd)
  - [[voice-stack|[Voice / local-first stack]]](#voice-local-first-stacksvyazi-2-0componentsvoice-stackmd)
  - [[yjs-automerge|[Yjs + Automerge]]](#yjs-automergesvyazi-2-0componentsyjs-automergemd)
  - [[yodoca|[Yodoca]]](#yodocasvyazi-2-0componentsyodocamd)
  - [[A-collaboration-os|[Ансамбль A — Collaboration OS]]](#ансамбль-a-collaboration-ossvyazi-2-0ensemblesa-collaboration-osmd)
  - [[B-forensic-rag|[Ансамбль B — Forensic RAG для доказуемого matching и review]]](#ансамбль-b-forensic-rag-для-доказуемого-matching-и-reviewsvyazi-2-0ensemblesb-forensic-ragmd)
  - [[C-multi-agent-factory|[Ансамбль C — Spec‑driven multi‑agent factory]]](#ансамбль-c-specdriven-multiagent-factorysvyazi-2-0ensemblesc-multi-agent-factorymd)
  - [[D-voice-first-mesh|[Ансамбль D — Voice‑first local knowledge mesh]]](#ансамбль-d-voicefirst-local-knowledge-meshsvyazi-2-0ensemblesd-voice-first-meshmd)
  - [[E-execution-plane|[Ансамбль E — Safe and cheap execution plane]]](#ансамбль-e-safe-and-cheap-execution-planesvyazi-2-0ensemblese-execution-planemd)
  - [[F-evidence-backed-intake|[Ансамбль F — Evidence‑Backed Community Intake]]](#ансамбль-f-evidencebacked-community-intakesvyazi-2-0ensemblesf-evidence-backed-intakemd)
  - [[G-federated-local-graph|[Ансамбль G — Federated Local‑First Community Graph]]](#ансамбль-g-federated-localfirst-community-graphsvyazi-2-0ensemblesg-federated-local-graphmd)
  - [[H-research-to-product-flywheel|[Ансамбль H — Research‑to‑Product Flywheel]]](#ансамбль-h-researchtoproduct-flywheelsvyazi-2-0ensemblesh-research-to-product-flywheelmd)
  - [[README|[Ансамбли проектов]]](#ансамбли-проектовsvyazi-2-0ensemblesreadmemd)
  - [[README|[limitations]]](#limitationssvyazi-2-0limitationsreadmemd)
  - [[conclusions|[Итоговые выводы и порядок сборки]]](#итоговые-выводы-и-порядок-сборкиsvyazi-2-0limitationsconclusionsmd)
  - [[do-not-glue|[Что пока лучше не склеивать]]](#что-пока-лучше-не-склеиватьsvyazi-2-0limitationsdo-not-gluemd)
  - [[license-tree|[Лицензионные развилки]]](#лицензионные-развилкиsvyazi-2-0limitationslicense-treemd)
  - [[README|[outreach]]](#outreachsvyazi-2-0outreachreadmemd)
  - [[first-contacts|[Первые контакты]]](#первые-контактыsvyazi-2-0outreachfirst-contactsmd)
  - [[message-template|[Шаблон первого сообщения]]](#шаблон-первого-сообщенияsvyazi-2-0outreachmessage-templatemd)
  - [[narrow-questions|[Узкие вопросы для каждого автора]]](#узкие-вопросы-для-каждого-автораsvyazi-2-0outreachnarrow-questionsmd)
  - [[README|[overview]]](#overviewsvyazi-2-0overviewreadmemd)
  - [[continuation-intro|[Что добавляет продолжение исследования]]](#что-добавляет-продолжение-исследованияsvyazi-2-0overviewcontinuation-intromd)
  - [[executive-summary|[Executive summary]]](#executive-summarysvyazi-2-0overviewexecutive-summarymd)
  - [[methodology|[Методика и рамка отбора]]](#методика-и-рамка-отбораsvyazi-2-0overviewmethodologymd)
  - [[projects-map|[Карта найденных проектов и паттернов]]](#карта-найденных-проектов-и-паттерновsvyazi-2-0overviewprojects-mapmd)
  - [[README|[prototype]]](#prototypesvyazi-2-0prototypereadmemd)
  - [[mvp-plan|[План MVP-прототипа]]](#план-mvp-прототипаsvyazi-2-0prototypemvp-planmd)
  - [[risks|[Ключевые риски и как их закрывать]]](#ключевые-риски-и-как-их-закрыватьsvyazi-2-0prototyperisksmd)
  - [[roadmap|[Дорожная карта прототипа]]](#дорожная-карта-прототипаsvyazi-2-0prototyperoadmapmd)
  - [[README|[security]]](#securitysvyazi-2-0securityreadmemd)
  - [[budget-routing|[Практичный бюджетный роутинг моделей]]](#практичный-бюджетный-роутинг-моделейsvyazi-2-0securitybudget-routingmd)
  - [[default-policy|[Что стоит зафиксировать как default policy]]](#что-стоит-зафиксировать-как-default-policysvyazi-2-0securitydefault-policymd)
  - [[privacy|[Приватность: local-first by default]]](#приватность-local-first-by-defaultsvyazi-2-0securityprivacymd)
- [Technology Combinations](#technology-combinations)
  - [[README|[technology-combinations/ — комбинирование технологий для новых свойств]]](#technology-combinations-комбинирование-технологий-для-новых-свойствtechnology-combinationsreadmemd)
  - [[01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern|[Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн]]](#комбинация-1-правильная-агентская-архитектура-svyazi-паттернtechnology-combinationscombinations01-pravilnaya-agentskaya-arkhitektura-svyazi-patternmd)
  - [[02-multiagentnyy-khaos-reshenie-auto-ai-router|[Комбинация 2: Мультиагентный хаос-решение × Auto AI Router]]](#комбинация-2-мультиагентный-хаос-решение-auto-ai-routertechnology-combinationscombinations02-multiagentnyy-khaos-reshenie-auto-ai-routermd)
  - [[03-crdt-local-first-svyazi-cardindex|[Комбинация 3: CRDT local-first × Svyazi CardIndex]]](#комбинация-3-crdt-local-first-svyazi-cardindextechnology-combinationscombinations03-crdt-local-first-svyazi-cardindexmd)
  - [[04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura|[Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура]]](#комбинация-4-парсинг-с-llm-graph-rag-правильная-агентская-архитектураtechnology-combinationscombinations04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitekturamd)
  - [[05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy|Комбинация 5: [SourceCraft CLI × Claude Code × Sequential протокол Дочкиной]]](#комбинация-5-sourcecraft-cli-claude-code-sequential-протокол-дочкинойtechnology-combinationscombinations05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoymd)
  - [[06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-|Комбинация 6: [OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер]]](#комбинация-6-openclaude-утёкший-claude-code-zinc-inference-engine-mome-роутерtechnology-combinationscombinations06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-md)
  - [[07-crawl4ai-docling-yodoca-consolidator|[Комбинация 7: Crawl4AI × Docling × Yodoca consolidator]]](#комбинация-7-crawl4ai-docling-yodoca-consolidatortechnology-combinationscombinations07-crawl4ai-docling-yodoca-consolidatormd)
  - [[08-conductor-adversarial-review-auto-ai-router|Комбинация 8: Conductor × [adversarial-review × Auto AI Router]]](#комбинация-8-conductor-adversarial-review-auto-ai-routertechnology-combinationscombinations08-conductor-adversarial-review-auto-ai-routermd)
  - [[09-agent-orchestration-stack|[Комбинация 9: Agent Orchestration Stack]]](#комбинация-9-agent-orchestration-stacktechnology-combinationscombinations09-agent-orchestration-stackmd)
  - [[10-legal-document-intelligence-pipeline|[Комбинация 10: Legal Document Intelligence Pipeline]]](#комбинация-10-legal-document-intelligence-pipelinetechnology-combinationscombinations10-legal-document-intelligence-pipelinemd)
  - [[11-hybrid-crdt-sql-database|[Комбинация 11: Hybrid CRDT-SQL Database]]](#комбинация-11-hybrid-crdt-sql-databasetechnology-combinationscombinations11-hybrid-crdt-sql-databasemd)
  - [[12-multi-agent-observability-stack|[Комбинация 12: Multi-Agent Observability Stack]]](#комбинация-12-multi-agent-observability-stacktechnology-combinationscombinations12-multi-agent-observability-stackmd)
  - [[13-legal-document-transpiler|[Комбинация 13: Legal Document Transpiler]]](#комбинация-13-legal-document-transpilertechnology-combinationscombinations13-legal-document-transpilermd)
  - [[14-local-first-agent-development-environment|[Комбинация 14: local-first Agent Development Environment]]](#комбинация-14-local-first-agent-development-environmenttechnology-combinationscombinations14-local-first-agent-development-environmentmd)
  - [[15-self-consolidating-legal-corpus|[Комбинация 15: Self-Consolidating Legal Corpus]]](#комбинация-15-self-consolidating-legal-corpustechnology-combinationscombinations15-self-consolidating-legal-corpusmd)
  - [[16-adversarial-multi-agent-code-review|[Комбинация 16: Adversarial Multi-Agent Code Review]]](#комбинация-16-adversarial-multi-agent-code-reviewtechnology-combinationscombinations16-adversarial-multi-agent-code-reviewmd)
  - [[17-distributed-agent-memory-with-graph|[Комбинация 17: Distributed Agent Memory with Graph]]](#комбинация-17-distributed-agent-memory-with-graphtechnology-combinationscombinations17-distributed-agent-memory-with-graphmd)
  - [[18-llm-powered-legal-corpus-builder|[Комбинация 18: LLM-Powered Legal Corpus Builder]]](#комбинация-18-llm-powered-legal-corpus-buildertechnology-combinationscombinations18-llm-powered-legal-corpus-buildermd)
  - [[19-multi-agent-observability-platform|[Комбинация 19: Multi-Agent Observability Platform]]](#комбинация-19-multi-agent-observability-platformtechnology-combinationscombinations19-multi-agent-observability-platformmd)
  - [[20-hybrid-olap-oltp-with-real-time-sync|[Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync]]](#комбинация-20-hybrid-olap-oltp-with-real-time-synctechnology-combinationscombinations20-hybrid-olap-oltp-with-real-time-syncmd)
  - [[21-legal-corpus-analytics-at-scale|[Комбинация 21: Legal Corpus Analytics at Scale]]](#комбинация-21-legal-corpus-analytics-at-scaletechnology-combinationscombinations21-legal-corpus-analytics-at-scalemd)
  - [[22-russian-international-oss-stack|[Комбинация 22: Russian-International OSS Stack]]](#комбинация-22-russian-international-oss-stacktechnology-combinationscombinations22-russian-international-oss-stackmd)
  - [[23-security-first-code-review-pipeline|[Комбинация 23: Security-First Code Review Pipeline]]](#комбинация-23-security-first-code-review-pipelinetechnology-combinationscombinations23-security-first-code-review-pipelinemd)
  - [[24-mega-integration-full-stack|[Комбинация 24: MEGA-INTEGRATION: Full Stack]]](#комбинация-24-mega-integration-full-stacktechnology-combinationscombinations24-mega-integration-full-stackmd)
  - [[25-legal-dsl-code-transpiler|[Комбинация 25: Legal DSL → Code Transpiler]]](#комбинация-25-legal-dsl-code-transpilertechnology-combinationscombinations25-legal-dsl-code-transpilermd)
  - [[26-ast-based-code-analysis-for-legal-automation|[Комбинация 26: AST-Based Code Analysis for Legal Automation]]](#комбинация-26-ast-based-code-analysis-for-legal-automationtechnology-combinationscombinations26-ast-based-code-analysis-for-legal-automationmd)
  - [[27-hybrid-rag-with-ast-chunked-code|[Комбинация 27: Hybrid RAG with AST-Chunked Code]]](#комбинация-27-hybrid-rag-with-ast-chunked-codetechnology-combinationscombinations27-hybrid-rag-with-ast-chunked-codemd)
  - [[28-pydantic-enforced-legal-workflows|[Комбинация 28: Pydantic-Enforced Legal Workflows]]](#комбинация-28-pydantic-enforced-legal-workflowstechnology-combinationscombinations28-pydantic-enforced-legal-workflowsmd)
  - [[29-meta-programmatic-legal-template-generator|[Комбинация 29: Meta-Programmatic Legal Template Generator]]](#комбинация-29-meta-programmatic-legal-template-generatortechnology-combinationscombinations29-meta-programmatic-legal-template-generatormd)
  - [[30-mega-stack-3-0-with-dsl-ast|[Комбинация 30: MEGA-STACK 3.0 with DSL & AST]]](#комбинация-30-mega-stack-30-with-dsl-asttechnology-combinationscombinations30-mega-stack-3-0-with-dsl-astmd)
  - [[31-event-sourced-legal-document-history|[Комбинация 31: Event-Sourced Legal Document History]]](#комбинация-31-event-sourced-legal-document-historytechnology-combinationscombinations31-event-sourced-legal-document-historymd)
  - [[32-consensus-based-multi-agent-coordination|[Комбинация 32: Consensus-Based Multi-Agent Coordination]]](#комбинация-32-consensus-based-multi-agent-coordinationtechnology-combinationscombinations32-consensus-based-multi-agent-coordinationmd)
  - [[33-event-sourcing-cqrs-clickhouse-analytics|[Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics]]](#комбинация-33-event-sourcing-cqrs-clickhouse-analyticstechnology-combinationscombinations33-event-sourcing-cqrs-clickhouse-analyticsmd)
  - [[34-distributed-event-store-with-paxos|[Комбинация 34: Distributed Event Store with Paxos]]](#комбинация-34-distributed-event-store-with-paxostechnology-combinationscombinations34-distributed-event-store-with-paxosmd)
  - [[35-mega-stack-4-0-with-event-sourcing-consensus|[Комбинация 35: MEGA-STACK 4.0 with Event Sourcing & Consensus]]](#комбинация-35-mega-stack-40-with-event-sourcing-consensustechnology-combinationscombinations35-mega-stack-4-0-with-event-sourcing-consensusmd)
  - [[README|[combinations]]](#combinationstechnology-combinationscombinationsreadmemd)
  - [[01-legal-ai-stack|[Mega‑Stack 1.0 — Полный Legal‑AI Stack]]](#megastack-10-полный-legalai-stacktechnology-combinationsmega-stacks01-legal-ai-stackmd)
  - [[02-ultimate-legal-ai|[Mega‑Stack 2.0 — Ultimate Legal‑AI System]]](#megastack-20-ultimate-legalai-systemtechnology-combinationsmega-stacks02-ultimate-legal-aimd)
  - [[03-dsl-ast|[Mega‑Stack 3.0 — with DSL & AST]]](#megastack-30-with-dsl-asttechnology-combinationsmega-stacks03-dsl-astmd)
  - [[04-event-sourcing-consensus|[Mega‑Stack 4.0 — with Event Sourcing & Consensus]]](#megastack-40-with-event-sourcing-consensustechnology-combinationsmega-stacks04-event-sourcing-consensusmd)
  - [[README|[mega-stacks]]](#mega-stackstechnology-combinationsmega-stacksreadmemd)
  - [[README|[properties/ — эмерджентные свойства]]](#properties-эмерджентные-свойстваtechnology-combinationspropertiesreadmemd)
  - [[README|[research-reports]]](#research-reportstechnology-combinationsresearch-reportsreadmemd)
  - [[continuation-10-domains|[Research Report: Continuation — 10 New Domains Beyond the Original 45 Combinations]]](#research-report-continuation-10-new-domains-beyond-the-original-45-combinationstechnology-combinationsresearch-reportscontinuation-10-domainsmd)
  - [[sozialrecht-35-combinations|[Research Report: Sozialrecht (35 комбинаций)]]](#research-report-sozialrecht-35-комбинацийtechnology-combinationsresearch-reportssozialrecht-35-combinationsmd)
  - [[01-08-summary|[Сводная таблица 1–8]]](#сводная-таблица-18technology-combinationssynthesis-tables01-08-summarymd)
  - [[09-14-extended|[Сводная таблица 9–14 (Extended)]]](#сводная-таблица-914-extendedtechnology-combinationssynthesis-tables09-14-extendedmd)
  - [[15-19-extended|[Сводная таблица 15–19 (Extended)]]](#сводная-таблица-1519-extendedtechnology-combinationssynthesis-tables15-19-extendedmd)
  - [[20-24-final|[Сводная таблица 20–24 (Final 1–24)]]](#сводная-таблица-2024-final-124technology-combinationssynthesis-tables20-24-finalmd)
  - [[25-30-extended|[Сводная таблица 25–30 (Complete 1–30)]]](#сводная-таблица-2530-complete-130technology-combinationssynthesis-tables25-30-extendedmd)
  - [[31-35-final|[Сводная таблица 31–35 (Complete 1–35)]]](#сводная-таблица-3135-complete-135technology-combinationssynthesis-tables31-35-finalmd)
  - [[README|[synthesis-tables]]](#synthesis-tablestechnology-combinationssynthesis-tablesreadmemd)
- [Templates](#templates)
  - [[README|[Шаблоны документов]]](#шаблоны-документовtemplatesreadmemd)
  - [[Спецификация агента: [Название]](templates/agent-spec.md)](#спецификация-агента-названиеtemplatesagent-specmd)
  - [[Контакт: [Имя / Проект]](templates/contact-outreach.md)](#контакт-имя-проектtemplatescontact-outreachmd)
  - [[Противоречие: [Название]](templates/contradiction-record.md)](#противоречие-названиеtemplatescontradiction-recordmd)
  - [[ADR: [Название решения]](templates/decision-record.md)](#adr-название-решенияtemplatesdecision-recordmd)
  - [[Ансамбль: [Название]](templates/ensemble.md)](#ансамбль-названиеtemplatesensemblemd)
  - [[Эксперимент: [Название]](templates/experiment-log.md)](#эксперимент-названиеtemplatesexperiment-logmd)
  - [[FAQ: [Вопрос]](templates/faq-entry.md)](#faq-вопросtemplatesfaq-entrymd)
  - [[[Термин]](templates/glossary-entry.md)](#терминtemplatesglossary-entrymd)
  - [[KPI Snapshot: [дата]](templates/kpi-snapshot.md)](#kpi-snapshot-датаtemplateskpi-snapshotmd)
  - [[Юридический кейс: [Aktenzeichen]](templates/legal-case.md)](#юридический-кейс-aktenzeichentemplateslegal-casemd)
  - [[Встреча: [Тема]](templates/meeting-notes.md)](#встреча-темаtemplatesmeeting-notesmd)
  - [[Mega-stack: [Название]](templates/mega-stack.md)](#mega-stack-названиеtemplatesmega-stackmd)
  - [[[Название компонента]](templates/project-component.md)](#название-компонентаtemplatesproject-componentmd)
  - [[[Название протокола]](templates/protocol-spec.md)](#название-протоколаtemplatesprotocol-specmd)
  - [[MVP: [Название]](templates/prototype-mvp.md)](#mvp-названиеtemplatesprototype-mvpmd)
  - [[[Тема исследования]](templates/research-note.md)](#тема-исследованияtemplatesresearch-notemd)
  - [[Ретроспектива: [период]](templates/retrospective.md)](#ретроспектива-периодtemplatesretrospectivemd)
  - [[RFC NNNN: [Название]](templates/rfc.md)](#rfc-nnnn-названиеtemplatesrfcmd)
  - [[Риск: [Название]](templates/risk-entry.md)](#риск-названиеtemplatesrisk-entrymd)
  - [[Tech Pair: [A] × [B]](templates/tech-pair.md)](#tech-pair-a-btemplatestech-pairmd)
  - [[Tech Radar: [Название]](templates/tech-radar-entry.md)](#tech-radar-названиеtemplatestech-radar-entrymd)
  - [[[имя нового шаблона]](templates/template-of-templates.md)](#имя-нового-шаблонаtemplatestemplate-of-templatesmd)
  - [[Еженедельный дайджест: [период]](templates/weekly-digest.md)](#еженедельный-дайджест-периодtemplatesweekly-digestmd)
- [🗺️ Тематическая карта](#тематическая-карта)
  - [Архитектура (569 документов)](#архитектура-569-документов)
  - [Документация (142 документов)](#документация-142-документов)
  - [Агенты (135 документов)](#агенты-135-документов)
  - [Проекты (132 документов)](#проекты-132-документов)
  - [Контакты (61 документов)](#контакты-61-документов)
  - [Память (46 документов)](#память-46-документов)
  - [Код (35 документов)](#код-35-документов)
  - [Анализ (31 документов)](#анализ-31-документов)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->




_Обновлено: 2026-05-10_

Секций: **20** | Файлов: **1213**

## Содержание

- [Docs](#docs) — 96 файлов
- [Svyazi](#svyazi) — 16 файлов
- [Anthropic Vacancies](#anthropic-vacancies) — 357 файлов
- [Technology Combinations](#technology-combinations) — 7 файлов
- [Ai Collaborations](#ai-collaborations) — 17 файлов
- [Habr Projects](#habr-projects) — 16 файлов
- [Ai Collaborations](#ai-collaborations) — 30 файлов
- [Anthropic Vacancies](#anthropic-vacancies) — 111 файлов
- [Autofilled](#autofilled) — 13 файлов
- [Badges](#badges) — 1 файлов
- [Contacts](#contacts) — 16 файлов
- [Glossary](#glossary) — 4 файлов
- [Habr Unique Projects](#habr-unique-projects) — 56 файлов
- [Lorenzo Agent](#lorenzo-agent) — 62 файлов
- [Meta Scripting](#meta-scripting) — 7 файлов
- [Nautilus](#nautilus) — 255 файлов
- [Processing Guide](#processing-guide) — 13 файлов
- [Svyazi 2 0](#svyazi-2-0) — 59 файлов
- [Technology Combinations](#technology-combinations) — 53 файлов
- [Templates](#templates) — 24 файлов


## Docs

_Путь: `docs/`_

### [[ABBREVIATIONS|Словарь аббревиатур и сокращений]]
> > !TIP

  - Самые часто используемые

_Слов: 1697_

### [[ACTION_ITEMS|Action Items, риски и решения]]
> Автоматически извлечено из всех документов.

  - ➡️ Следующие шаги (273)
  - ✅ Решения и рекомендации (493)
  - ⚠️ Риски (954)
  - 🚫 Ограничения (262)
  - 📋 Задачи (TODO) (34)
  - 📬 Контактные действия (247)

_Слов: 9180_

### [[ALERTS|Callout-блоки]]
> Добавлено 55 callout-блоков в документы.

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
  - Связанные документы
  - Упоминается в

_Слов: 187_

### [[BACKLINKS|Индекс обратных ссылок]]
> Файлов с входящими ссылками: 1786

  - Топ-30 самых цитируемых документов
  - Ссылки по разделам

_Слов: 527_

### [[BADGES|Status Badges]]
> Обновлено: 2026-05-10

  - Превью
  - Markdown сниппеты для README

_Слов: 42_

### [[CHANGELOG]]
> Всего коммитов: 158

  - semantic (1 коммитов)
  - md (1 коммитов)
  - 2026-05-10 (11 коммитов)
  - 2026-04-29 (141 коммитов)
  - skip  (1 коммитов)
  - 22 скила  (1 коммитов)
  - $.STEP.ou (1 коммитов)
  - (1 коммитов)

_Слов: 2285_

### [[CHANGELOG_AUTO|Changelog (авто)]]
> > - Статистика коммитов(#статистика-коммитов)

  - Содержание
  - Contents
  - Статистика коммитов
  - История изменений
  - Упоминается в
  - Связанные документы

_Слов: 681_

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

_Слов: 1409_

### [[CODE_BLOCKS|Code-блоки репозитория]]
> > !TIP

  - 📊 Диаграммы Mermaid (32)
- ... (обрезано)
- ... (обрезано)
  - 🐍 Python (114)
- ... (обрезано)
- ... (обрезано)
- ... (обрезано)
  - 📋 YAML (23)
  _... ещё 51 разделов_

_Слов: 5259_

### [[COLLAB_SUGGESTIONS|Рекомендации по коллаборации (Collaboration Finder)]]
> > Автоматический поиск партнёрских проектов для: «агент с памятью консолидация»

  - 1. Wikontic: семантический граф
  - 2. Yodoca
  - 3. NGT[^ngt] Memory: ассоциативный граф
  - Следующие шаги

_Слов: 631_

### [[COMPARE|Сравнение с предыдущим коммитом]]
> Файлов было: 1448  стало: 1741

  - Новые файлы (293)
  - Удалённые файлы (0)
  - Изменившиеся файлы (570) — топ по Δ слов

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
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 1051_

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

_Слов: 13914_

### [[CONCEPT_GRAPH|Граф концептов базы знаний]]
> Обновлено: 2026-05-10

  - Диаграмма
  - Топ концептов по связям

_Слов: 646_

### [[CONSISTENCY|Согласованность терминов]]
> Анализ различных написаний одних и тех же терминов.

  - Детали по файлам
  - Как исправить
- Пример: заменить все вхождения в docs/

_Слов: 495_

### [[CONTACTS|Контакты и авторы]]
>  Автор  Проект  Слой  Упомянут в файлах  Первый вопрос 

  - Ключевые авторы проектов
  - GitHub репозитории
  - Email адреса
  - Шаблон первого сообщения

_Слов: 552_

### [[CONTACT_PRIORITY|Приоритет контактов]]
> Обновлено: 2026-05-10

  - Топ авторов по приоритету
  - Рекомендуемые следующие шаги
  - Формула расчёта балла

_Слов: 364_

### [[CONTRADICTIONS|Противоречия в базе знаний]]
> Обновлено: 2026-05-10

  - Найденные противоречия

_Слов: 1633_

### [[COST|Оценка стоимости MVP]]
> Ориентировочные цифры на основе документации проекта.

  - Итого
  - По компонентам
  - По ролям
  - Сценарии
  - Временные оценки из документов
  - Допущения

_Слов: 502_

### [[CROSSREFS|Перекрёстные ссылки]]
> > !TIP

  - Проекты → файлы
  - Файлы → проекты

_Слов: 653_

### [[CROSS_SECTION|Кросс-секционный анализ]]
> > (косинусное сходство TF-IDF векторов)

  - Содержание
  - Матрица сходства секций
  - Граф связей
  - Топ-40 кросс-секционных концептов
  - Детальная карта концептов

_Слов: 1256_

### [[DECISIONS|Ключевые решения и выводы]]
> Автоматически извлечено из всех документов: 624 записей

  - Архитектура (61)
  - Mvp (10)
  - Память (16)
  - Оркестрация (26)
  - Безопасность (3)
  - Лицензия (18)
  - Риски (5)
  - Контакты (35)
  _... ещё 1 разделов_

_Слов: 2567_

### [[DENSITY|Карта плотности тем]]
> > !TIP

  - Наиболее раскрытые темы
  - Слабо раскрытые темы (0)
  - Где сосредоточена каждая тема

_Слов: 650_

### [[DEPENDABOT|Мониторинг зависимостей]]
> Обновлено: 2026-05-10

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

_Слов: 1157_

### [[DIGEST|Дайджест изменений]]
> > > chore: update generated docs — auto-enrichment, TOC, summaries, meta-scripting

  - Последний коммит
  - Последние 3 коммита — итого
  - Новые документы
  - История коммитов (последние 15)
  - Текущее состояние репозитория

_Слов: 360_

### [[DIGEST_AUTO|Автодайджест изменений]]
> Период: 2026-05-03 — 2026-05-10 (7 дней)

  - Сводка
  - Активность по секциям
  - Последние коммиты
  - Новые файлы
  - Изменённые файлы
  - Ключевые слова изменений
  - Новые концепты

_Слов: 470_

### [[DIGEST_WEEKLY|Еженедельный дайджест — 2026-04-29]]
> > Период: последние 7 дней (с 2026-04-22)

  - Итого
  - Коммиты

_Слов: 232_

### [[DUPLICATES|Отчёт о дублировании]]
> Порог сходства: 0.5

  - Похожие файлы (Jaccard ≥ 0.5)

_Слов: 2434_

### [[EMPTY_SECTIONS|Пустые секции]]
> Обновлено: 2026-05-10

  - Файлы с ≥50% пустых секций (приоритет)
  - Все файлы с пустыми секциями

_Слов: 13300_

### [[ENTITIES|Именованные сущности]]
> Файлов просмотрено: 1735

  - Люди и авторы (7)
  - Проекты (22)
  - Организации (9)
  - Технологии и стандарты (24)
  - GitHub репозитории (15)
  - Ко-встречаемость проектов (топ пары)

_Слов: 742_

### [[FAQ|Часто задаваемые вопросы (FAQ)]]
> Извлечено: 177 вопросов и ответов

  - Архитектура
  - MVP/Запуск
  - Компоненты
  - Интеграция
  - Лицензия
  - Общее

_Слов: 892_

### [[FOOTNOTES|Сноски и определения терминов]]
> Обновлено файлов: 3  Вставлено сносок: 11

  - Словарь сносок
  - Как это работает

_Слов: 275_

### [[GLOSSARY|Глоссарий проектов]]
> Все проекты, упоминаемые в документах, с количеством файлов.


_Слов: 222_

### [[GRAPH|Граф связей проектов]]
> Рёбра = совместные упоминания в одном файле (≥ 2 раз).

  - Топ совместных упоминаний
  - DOT-формат (Graphviz)

_Слов: 2655_

### [[HEADING_AUDIT|Аудит заголовков]]
> Обновлено: 2026-05-10

  - Типы проблем
  - По файлам

_Слов: 5907_

### [[HEALTH|Health Dashboard]]
> Обновлено: 2026-05-10

  - Общий балл: 99/100 🟢
  - Метрики
  - Структура репозитория
  - Action Items
  - Скрипты обработки
  - Рекомендации

_Слов: 228_

### [[HEATMAP|Тепловая карта тем]]
> > !TIP

  - Числовые значения (‰)
  - Доминирующие темы по разделам
  - Концентрация тем

_Слов: 537_

### [[INDEX|Индекс документации — Lorenzo / Svyazi 2.0]]
> Главный навигационный хаб. Все разделы и документы.

  - Метрики репозитория
  - Разделы документации
  - Аналитика и отчёты
  - Ключевые документы
  - LLM-обогащение (Ступень 3)
  - Быстрый старт
- Читать документацию
- Обновить всю документацию
  _... ещё 1 разделов_

_Слов: 514_

### [[KEYWORD_INDEX|Инвертированный индекс ключевых слов]]
> > > 🎯 Проблема: Инвертированный индекс ключевых слов Обновлено: 2026-04-29 Уникальных слов: 23264 Биграмм: 13489 Файлов:…

  - Топ слов по охвату файлов
  - Топ биграмм (устойчивые словосочетания)

_Слов: 1162_

### [[KNOWLEDGE_MAP|Карта базы знаний Lorenzo]]
> Обновлено: 2026-05-10

  - Корпус
  - Метрики качества
  - По секциям
  - Ключевые концепты
  - Топ сущностей
  - Открытые вопросы
  - Быстрые команды
- Поиск
  _... ещё 2 разделов_

_Слов: 607_

### [[KPI|Числовые KPI и метрики]]
> > !TIP

  - Количество (432)
  - Проценты (305)
  - Время (444)
  - Стоимость (757)
  - Размер (65)
  - Версия (636)
  - Рейтинг (77)
  - Этап (129)

_Слов: 2736_

### [[KPI_HISTORY|История метрик KPI]]
> Последнее обновление: 2026-05-10 · Снапшотов в истории: 2

  - Текущие метрики
  - История

_Слов: 134_

### [[LANGUAGE_STATS|Языковой состав документов]]
> Обновлено: 2026-05-10

  - Распределение
  - Файлы с неожиданным языком
  - Смешанные файлы (MIX)
  - По секциям

_Слов: 6984_

### [[LINKS|Индекс ссылок]]
> > !TIP


_Слов: 1060_

### [[LLM_SUMMARIES|AI-саммари разделов документации]]
> > - Архитектура Svyazi 2.0(#архитектура-svyazi-20)

  - Contents
  - Архитектура Svyazi 2.0
  - Вакансии Anthropic
  - Комбинации технологий
  - AI-коллаборации
  - Хабр-проекты
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 300_

### [[MCP_DASHBOARD|MCP Dashboard]]
> Логи MCP-вызовов отсутствуют.


_Слов: 6_

### [[METHODOLOGY|Методология работы со скриптами]]
> > > Принципы: скрипты работают по вызову, под контролем человека или Claude.

  - Содержание
  - Основной принцип
  - Три категории скриптов
  - Типичные рабочие сессии
- Прочитать docs/HEALTH.md и docs/BROKENLINKS.md
- Коммитить не обязательно
- Проверить результат в docs/05-habr-projects/
- Порядок важен: индексы должны быть готовы до контентных скриптов
  _... ещё 3 разделов_

_Слов: 998_

### [[METRICS|Метрики качества документации]]
> Файлов: 1726  Средний балл: 71.2/100

  - Качество по разделам
  - Топ-15 лучших документов
  - Документы, требующие улучшения (39)
  - Общие показатели

_Слов: 471_

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
> Обновлено: 2026-05-10

  - 👤 People (20)
  - 📦 Projects (144)
  - ⚙️ Tech (32)
  - 🏢 Orgs (8)
  - 📅 Dates (39)

_Слов: 1508_

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

_Слов: 1032_

### [[NETWORK|Сеть проектов и авторов]]
> Узлов: 20  Связей: 190

  - Топ-20 ко-упоминаемых пар
  - Центральность узлов (влиятельность)
  - Авторы ↔ Проекты

_Слов: 414_

### [[ONBOARDING|Онбординг — Svyazi 2.0 / Lorenzo]]
> Руководство для новых участников проекта.

  - Что это такое?
  - Первые 30 минут
- 1. Клонировать репозиторий
- 2. Прочитать Executive Summary
- 3. Посмотреть статус проекта
- 4. Прочитать FAQ
- 5. Запустить скрипты (генерация/обновление docs)
  - Структура документации
  _... ещё 10 разделов_

_Слов: 460_

### [[ORPHANS|Изолированные документы (Orphans)]]
> Найдено: 399 файлов без входящих ссылок из 1542 проверено.

  - Топ-20 по объёму (важные и изолированные)
  - По разделам
  - Рекомендации

_Слов: 308_

### [[PARAGRAPH_QUALITY|Качество абзацев]]
> Обновлено: 2026-05-10

  - Типы проблем
  - По файлам

_Слов: 11068_

### [[PASSIVE_VOICE|Пассивный залог и канцеляризмы]]
> Обновлено: 2026-05-10

  - Корпусная статистика
  - Топ файлов по доле пассива

_Слов: 373_

### [[PRIORITIES|Приоритеты файлов]]
> > !TIP

  - Топ-50 самых важных файлов
  - Топ-5 по каждому разделу

_Слов: 3158_

### [[PROGRESS|Прогресс MVP]]
> Обновлено: 2026-05-10 (improveprogresssync.py)

  - Ключевые этапы (Milestones)
  - Состояние компонентов
  - Метрики качества
  - Следующий шаг
- Приоритет 1: kksudo (AgentFS, 13 упоминаний)
- Приоритет 2: spbmolot (NGT Memory, 12 упоминаний)
- Приоритет 3: AnastasiyaW (knowledge-space, 11 упоминаний)
  - Связанные документы

_Слов: 261_

### [[PROTOTYPE_SPEC|Svyazi 2.0 — Спецификация прототипа]]
> > !TIP

  - Содержание
  - 1. Цель прототипа
  - 2. Компоненты MVP (три слоя)
  - 3. Интеграционные контракты
  - 4. Архитектура прототипа
  - 5. Итерации MVP
  - 6. Технический стек
  - 7. Риски и митигация
  _... ещё 2 разделов_

_Слов: 1431_

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
  _... ещё 150 разделов_

_Слов: 1975_

### [[QUESTIONS|Вопросы и открытые темы из базы знаний]]
> Обновлено: 2026-05-10

  - Сводка
  - 🔓 Открытый вопрос (16)
  - ❓ Вопрос (1961)
  - 📌 TODO/Идея (151)
  - 💭 Гипотеза (392)

_Слов: 23735_

### [[READING_LIST|Список чтения]]
> > по запросу «RAG retrieval»  Документов: 5  Время: ~20 мин (0ч 20м)

  - По секциям

_Слов: 232_

### [[READING_ORDER|Рекомендуемый порядок чтения]]
> От базовых концепций к сложным. Начните с зелёных (🟢), затем жёлтые (🟡), красные (🔴).

  - Маршруты по целям

_Слов: 5947_

### [[README|docs]]
> Файлов: 106

  - Содержание
  - Подразделы

_Слов: 847_

### [[REGISTRY|REGISTRY — реестр артефактов Lorenzo]]
> Обновлено: 2026-05-10

  - Сводка
  - Скрипты по группам
  - Шаблоны
  - Скилы
  - MCP-серверы
  - Манифесты задач
  - Контакты
  - Полезные команды
  _... ещё 6 разделов_

_Слов: 1327_

### [[REPORT|Executive Report: Репозиторий Lorenzo]]
> Дата генерации: 2026-05-10

  - Общая картина
  - Структура репозитория
  - Извлечённые знания
  - Топ навигационных документов
  - Рекомендуемые следующие шаги
  - Аналитические инструменты

_Слов: 304_

### [[RISK_REGISTER|Реестр рисков — Svyazi 2.0]]
> Курированных рисков: 10 · Из документов: 15

  - Матрица рисков (Вероятность × Влияние)
  - Реестр
  - Митигации
  - Упоминания рисков в документах
  - Итоговая статистика

_Слов: 788_

### [[SCHEDULE|Расписание проекта]]
> Дорожная карта с вехами и задачами по кварталам.

  - Ключевые вехи
  - Gantt-диаграмма
  - Задачи по фазам
  - Текущий статус

_Слов: 271_

### [[SCORING|Оценка готовности проекта (Go/No-Go)]]
> Дата: 2026-05-10

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
> Обновлено: 2026-05-10

  - По группам
  - Подробно

_Слов: 7281_

### [[SCRIPT_EVAL_REPORT|Отчёт об оценке скриптов Lorenzo]]
> > Детальное живое тестирование 159 скриптов: сценки-диалоги, сравнение «до/после», плюсы/минусы, пути развития.

  - Содержание
  - 1. Общая картина: что изменилось
  - 2. Диалог-сценки: скрипты в действии
- Шаг 1: посмотреть, что будет создано
- Шаг 2: реальная сборка
- Шаг 3: статистика
- Шаг 4: поиск
- Шаг 5: одобрить найденный проект
  _... ещё 16 разделов_

_Слов: 2904_

### [[SEARCH_RESULTS|Результаты поиска]]
> Обновлено: 2026-05-10


_Слов: 73_

### [[SEE_ALSO|Индекс «Смотрите также»]]
> Файлов с блоком See Also: 1129

  - Ключевые связи

_Слов: 220_

### [[SENTIMENT|Тональный анализ документов]]
> > !WARNING

  - Тональность по разделам
  - Самые оптимистичные документы
  - Самые скептичные / риск-ориентированные
  - Распределение тональности

_Слов: 561_

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
> Обновлено: 2026-05-10

  - Навигация
  - Мета-документы
  - Svyazi 2.0 — Архитектура системы
  - Вакансии Anthropic — 436 позиций
  - Комбинации технологий
  - AI Коллаборации — ансамбли проектов
  - Хабр-проекты — память и граф
  - ai-collaborations
  _... ещё 13 разделов_

_Слов: 8315_

### [[SKILL_DASHBOARD|Skill Dashboard]]
> Обновлено: 2026-05-10


_Слов: 21_

### [[SOURCE_MAP|Карта происхождения текстов]]
> Обновлено: 2026-05-10

  - Категории
  - Авторы
  - 🤖 Авто-импортированные файлы (1252)
  - 🔗 Файлы с внешними ссылками (157)

_Слов: 8933_

### [[STATS|Детальная статистика репозитория]]
> Разделов: 21  Файлов: 1735  Слов: 1,782,544  Символов: 15,653,958

  - Сводная таблица по разделам
  - Топ-20 файлов по объёму
  - Ключевые показатели

_Слов: 681_

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
> Всего таблиц: 773

  - 01-svyazi (11 таблиц)
  - 02-anthropic-vacancies (34 таблиц)
  - 03-technology-combinations (1 таблиц)
  - 04-ai-collaborations (38 таблиц)
  - 05-habr-projects (16 таблиц)
  - ai-collaborations (13 таблиц)
  - anthropic-vacancies (2 таблиц)
  - contacts (15 таблиц)
  _... ещё 11 разделов_

_Слов: 212289_

### [[TAGS|Индекс тегов]]
> Каждый файл помечен тегами по темам автоматически.

  - #anthropic (38 файлов)
  - #architecture (38 файлов)
  - #collaboration (43 файлов)
  - #ingestion (35 файлов)
  - #knowledge (26 файлов)
  - #local-first (16 файлов)
  - #memory (29 файлов)
  - #orchestration (21 файлов)
  _... ещё 4 разделов_

_Слов: 600_

### [[TASKS_INDEX|Каталог задач (TASKSINDEX)]]
> - По MCP-серверу(#по-mcp-серверу)

  - Содержание
  - По MCP-серверу
  - Подробно

_Слов: 1012_

### [[TECH_RADAR|Tech Radar — Svyazi 2.0]]
> Оценка технологий и компонентов экосистемы по методологии ThoughtWorks.

  - Обзор
  - 🟢 ADOPT
  - 🔵 TRIAL
  - 🟡 ASSESS
  - 🔴 HOLD
  - Методология

_Слов: 522_

### [[TIMELINE|Хронологическая лента событий]]
> Обновлено: 2026-05-10

  - 2020 (4 упоминаний)
  - 2021 (2 упоминаний)
  - 2022 (12 упоминаний)
  - 2023 (11 упоминаний)
  - 2024 (51 упоминаний)
  - 2025 (44 упоминаний)
  - 2026 (475 упоминаний)
  - 2027 (3 упоминаний)
  _... ещё 1 разделов_

_Слов: 2077_

### [[VALIDATION|Валидация структуры репозитория]]
> Ошибок: 0  Предупреждений: 51  Пройдено: 27

  - Сводка
  - ✅ Разделы и README
  - ✅ Мета-файлы
  - Пустые/короткие файлы
  - Именование файлов
  - Заголовки H1
  - Внутренние ссылки
  - Итог

_Слов: 635_

### [[VOCABULARY|Богатство словаря документов]]
> Обновлено: 2026-05-10

  - Корпусная статистика
  - Топ файлов по богатству словаря (STTR)
  - Файлы с бедным словарём (требуют доработки)
  - Справка по метрикам

_Слов: 882_

### [[WORD_CLOUD|Word Cloud]]
> > Визуализация 80 самых частых слов репозитория.

  - Топ-20 слов

_Слов: 234_

### [[WORD_FREQ|Частотный анализ слов]]
> > !WARNING

  - Глобальный топ-50 слов
  - Топ-15 слов по разделам
  - Уникальные слова разделов

_Слов: 3193_

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

**Итого в секции: 405,714 слов, 96 файлов**


## Svyazi

_Путь: `docs/01-svyazi/`_

### [[00-intro-part2|Продолжение исследования для Svyazi 2.0]]

_Слов: 6_

### [Svyazi[^svyazi] 2.0 — Исполнительное резюме](01-svyazi/01-executive-summary.md)
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

_Слов: 1405_

### [[04-ensembles-overview|Приоритетные ансамбли]]

_Слов: 1288_

### [[06-security-privacy|Безопасность, приватность и бюджетный роутинг]]

_Слов: 823_

### [[07-mvp-planning|План прототипа и возможные контакты]]

_Слов: 1083_

### [[08-conclusions|Выводы]]

_Слов: 380_

### [[09-architectural-gaps|Архитектурные зазоры, которые важнее новых инструментов]]

_Слов: 774_

### [[10-second-order-ensembles|Новые ансамбли следующего шага]]

_Слов: 924_

### [[11-integration-contracts|Интеграционный контракт, который стоит зафиксировать сразу]]

_Слов: 753_

### [[12-roadmap|Дорожная карта прототипа следующей итерации]]

_Слов: 722_

### [[13-contacts|Содержание]]
  - Контактная стратегия и узкие вопросы для авторов
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1010_

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

### [Svyazi[^svyazi] 2.0 — Архитектура и исследование](01-svyazi/README.md)
> Файлов: 15

  - Содержание
  - Подразделы

_Слов: 342_

**Итого в секции: 11,578 слов, 16 файлов**


## Anthropic Vacancies

_Путь: `docs/02-anthropic-vacancies/`_

### [[00-intro|Введение]]
> > Абстракт (авто)

  - Содержание
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 9000_

### [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]]
> > Абстракт (авто)

  - Содержание
  - Интегральный анализ профиля svend4
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 19237_

### [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]]
> > Абстракт (авто)

  - Содержание
  - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL
- portal-mcp.py
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 3326_

### [[03-portal-protocol-md|PORTAL-PROTOCOL.md]]
> > Status: Draft (Working Document)

  - PORTAL-PROTOCOL.md
- Nautilus Portal Protocol
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 347_

### [[04-abstract|Abstract]]
> > The Nautilus Portal Protocol (далее — NPP) определяет способ федерации

  - Abstract
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 339_

### [[05-0-status-of-this-document|0. Status of This Document]]
> > Этот документ — рабочий черновик Nautilus Portal Protocol v1.0. Он может

  - 0. Status of This Document
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 325_

### [[06-1-introduction|1. Introduction]]
> > Абстракт (авто)

  - Contents
  - 1. Introduction

_Слов: 403_

### [[07-2-terminology|2. Terminology]]
> > Абстракт (авто)

  - 2. Terminology

_Слов: 324_

### [[08-3-registry-nautilus-json|3. Registry (nautilus.json)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 3. Registry (nautilus.json)

_Слов: 415_

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
  _... ещё 4 разделов_

_Слов: 324_

### [[102-доступ-к-данным|Доступ к данным]]
> > !WARNING

  - Доступ к данным
  - Упоминается в
  - Упоминается в
  - Связанные документы

_Слов: 256_

### [[103-appendix-b-change-log|Appendix B: Change Log]]
> - Appendix B: Change Log(#appendix-b-change-log)

  - Contents
  - Appendix B: Change Log
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 333_

### [[104-appendix-c-references|Appendix C: References]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: References
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1191_

### [[105-review-methodology-md|REVIEWMETHODOLOGY.md]]
> > Статус: Активно применяется в проекте svend4/nautilus

  - REVIEWMETHODOLOGY.md
- Трёхфазная методология Review в Nautilus
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 300_

### [[106-tl-dr|TL;DR]]
> > Для критически важных документов проекта применяется

  - TL;DR
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 236_

### [[107-1-контекст-и-мотивация|1. Контекст и мотивация]]
> > Абстракт (авто)

  - Contents
  - 1. Контекст и мотивация

_Слов: 471_

### [[108-2-формальный-workflow|2. Формальный workflow]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 2. Формальный workflow

_Слов: 471_

### [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]]
> - 3. Принципы консолидации (Фаза C)(#3-принципы-консолидации-фаза-c)

  - Содержание
  - Содержание
  - 3. Принципы консолидации (Фаза C)
- LOC в Python-коде
- Количество тестов
- Число адаптеров
- Health score
- Q6-покрытие
  _... ещё 6 разделов_

_Слов: 697_

### [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или осмысленный?]]
> > Абстракт (авто)

  - Вопрос: fallback-ratio как критический или осмысленный?

_Слов: 338_

### [[111-4-условия-применимости|4. Условия применимости]]
> > Абстракт (авто)

  - Contents
  - 4. Условия применимости

_Слов: 292_

### [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]]
> > !WARNING

  - Contents
  - 5. Связь с существующими методологиями

_Слов: 389_

### [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assisted workflows]]
> > Традиционная software engineering оптимизировалась против

  - 6. Почему это валидный паттерн для AI-assisted workflows

_Слов: 172_

### [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]]
> > !WARNING

  - Contents
  - 7. Реализация в проекте Nautilus

_Слов: 308_

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

_Слов: 331_

### [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]]
> > !WARNING

  - Appendix A: Шаблон для header warning

_Слов: 215_

### [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешения]]
> > Абстракт (авто)

  - Contents
  - Appendix B: Примеры расхождений и их разрешения

_Слов: 372_

### [[12-content-overview|Content Overview]]
> > Что внутри: типы данных, приблизительный объём, основные темы.

  - Content Overview
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 211_

### [[120-главные-технические-риски|Главные технические риски]]
> > Два независимых анализа выделили разные приоритеты:

  - Главные технические риски

_Слов: 100_

### [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]]
> > !WARNING

  - Appendix C: История изменений методологии
  - Упоминается в
  - Упоминается в
  - Связанные документы

_Слов: 250_

### [[122-глоссарий|Глоссарий]]
> > Абстракт (авто)

  - Содержание
  - Глоссарий
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1539_

### [[123-portal-mcp-py|portal-mcp.py]]
> > Абстракт (авто)

  - Содержание
  - portal-mcp.py
- ============================================================
- MCP SDK imports
- ============================================================
- # We use the official MCP Python SDK. If not installed, user gets
- a clear error with install instructions.
- try:
  _... ещё 56 разделов_

_Слов: 2524_

### [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]]
> > После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигураци…

  - Конфигурация для Claude Desktop
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 263_

### [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]]
> > Отдельный документ для репо, объясняющий, как настроить MCP-обёртку:

  - README-MCP.md— инструкция по установке
- Nautilus Portal MCP Integration
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 290_

### [[126-установка|Установка]]
> - Установка(#установка)

  - Contents
  - Установка
- Ждёт stdio-input; Ctrl+C для выхода

_Слов: 163_

### [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]]
> - Подключение к Claude Desktop(#подключение-к-claude-desktop)

  - Contents
  - Подключение к Claude Desktop
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 276_

### [[128-доступные-инструменты|Доступные инструменты]]
> > !WARNING

  - Доступные инструменты
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 320_

### [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]]
> > !WARNING

  - Примеры запросов (в Claude)
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 320_

### [[13-angle-perspective|Angle / Perspective]]
> > С какого угла Repo смотрит на общие концепты

  - Angle / Perspective
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 238_

### [[130-отладка|Отладка]]
> - Отладка(#отладка)

  - Contents
  - Отладка
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 261_

### [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]]
> > - Работает только в stdio mode (HTTP-mode планируется)

  - Ограничения текущей версии (0.1.0-draft)
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 197_

### [[132-planned-v0-2-0|Planned (v0.2.0)]]
> > !WARNING

  - Planned (v0.2.0)
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 252_

### [[133-обратная-связь|Обратная связь]]
> > Абстракт (авто)

  - Содержание
  - Обратная связь
- MCP интеграция (для Claude Desktop)
- Конфигурация: см. README-MCP.md
- В приватном репо cases-private:
  - Упоминается в
  - Упоминается в
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 17099_

### [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]]
> > - 187-слой-представительских-агентов-md(187-слой-представительских-агентов-md.md) (сходство 0.25)

  - THE DOUBLE-TRIANGLE ARCHITECTURE.md
- The Double-Triangle Architecture
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 310_

### [[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in Distributed Knowledge Work]]
> > Editorial review: Claude (intellectual collaboration, 2026-04)

  - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 291_

### [[136-abstract|Abstract]]
> > Абстракт (авто)

  - Содержание
  - Abstract
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 631_

### [[137-table-of-contents|Table of Contents]]
> > 1. Why Single-Triangle Models Are Incomplete

  - Table of Contents
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 316_

### [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 1. Why Single-Triangle Models Are Incomplete

_Слов: 613_

### [[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]]
> > Абстракт (авто)

  - Содержание
  - 2. The Double-Triangle Architecture
- Bridges
  - Bridges

_Слов: 779_

### [[140-3-three-inter-layer-protocols|3. Three Inter-Layer Protocols]]
> > Абстракт (авто)

  - Содержание
  - 3. Three Inter-Layer Protocols
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1048_

### [[141-4-nautilus-portal-as-reference-substrate|4. Nautilus Portal as Reference Substrate]]
> > Абстракт (авто)

  - Содержание
  - 4. Nautilus Portal as Reference Substrate
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 915_

### [[142-5-pattern-library-as-bridge-between-triangles|5. Pattern Library as Bridge Between Triangles]]
> > Абстракт (авто)

  - Содержание
  - 5. Pattern Library as Bridge Between Triangles
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 878_

### [[143-6-four-deployment-domains|6. Four Deployment Domains]]
> > !TIP

  - Содержание
  - 6. Four Deployment Domains
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 884_

### [[144-7-open-questions|7. Open Questions]]
> > Абстракт (авто)

  - Содержание
  - 7. Open Questions
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 964_

### [[145-8-call-to-action|8. Call to Action]]
> > Абстракт (авто)

  - Содержание
  - 8. Call to Action
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 929_

### [[146-acknowledgments|Acknowledgments]]
> > !TIP

  - Acknowledgments
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 463_

### [[147-references|References]]
> > Абстракт (авто)

  - Contents
  - References

_Слов: 369_

### [[148-appendix-a-glossary|Appendix A: Glossary]]
> - Appendix A: Glossary(#appendix-a-glossary)

  - Содержание
  - Appendix A: Glossary
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 548_

### [[149-appendix-b-summary-of-contributions|Appendix B: Summary of Contributions]]
> > 1. Topological formalization of Double-Triangle Architecture

  - Appendix B: Summary of Contributions
- Author & Contact
  - Author & Contact
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 348_

### [[150-appendix-c-version-history|Appendix C: Version History]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: Version History
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 8608_

### [[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]]
> > - 273-infrastructure-for-ai-collaborative-intellectual-w(273-infrastructure-for-ai-collaborative-intellectual-w.md) (с…

  - OPEN KNOWLEDGE WORK FOUNDATION.md
- Open Knowledge Work Foundation
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 372_

### [[152-ai-coordinated-infrastructure-for-distributed-expe|AI-Coordinated Infrastructure for Distributed Expert Contribution]]
> > Editorial collaboration: Claude (intellectual development, 2026-04)

  - AI-Coordinated Infrastructure for Distributed Expert Contribution
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 268_

### [[153-executive-summary|Executive Summary]]
> - Executive Summary(#executive-summary)

  - Содержание
  - Executive Summary
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 615_

### [[154-table-of-contents|Table of Contents]]
> > 3. Why Existing Solutions Fail

  - Table of Contents
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 275_

### [[155-1-problem-statement|1. Problem Statement]]
> > Абстракт (авто)

  - Содержание
  - 1. Problem Statement
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 790_

### [[156-2-target-populations|2. Target Populations]]
> > Абстракт (авто)

  - Содержание
  - 2. Target Populations
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 819_

### [[157-3-why-existing-solutions-fail|3. Why Existing Solutions Fail]]
> > Абстракт (авто)

  - Содержание
  - 3. Why Existing Solutions Fail
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 805_

### [[158-4-proposed-infrastructure|4. Proposed Infrastructure]]
> > Абстракт (авто)

  - Содержание
  - 4. Proposed Infrastructure

_Слов: 1052_

### [[159-5-economic-model|5. Economic Model]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 5. Economic Model

_Слов: 678_

### [[16-history|History]]
> > Когда создан, ключевые версии, направление развития.

  - History
  - Упоминается в
  - Упоминается в
  - Связанные документы

_Слов: 178_

### [[160-6-governance-and-ethics|6. Governance and Ethics]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Governance and Ethics

_Слов: 621_

### [[161-7-phased-rollout-plan|7. Phased Rollout Plan]]
> > Абстракт (авто)

  - Содержание
  - 7. Phased Rollout Plan
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 799_

### [[162-8-risk-analysis|8. Risk Analysis]]
> > Абстракт (авто)

  - Содержание
  - 8. Risk Analysis
  - Упоминается в
  - Упоминается в
  - Связанные документы

_Слов: 757_

### [[163-9-call-for-partnership|9. Call for Partnership]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Call for Partnership

_Слов: 654_

### [[164-10-appendices|10. Appendices]]
> > Абстракт (авто)

  - Содержание
  - 10. Appendices
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1156_

### [[165-closing|Closing]]
> > Абстракт (авто)

  - Содержание
  - Closing
- unknownlegalconcepts.yml
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 9429_

### [[166-representative-agent-layer-md|REPRESENTATIVE AGENT LAYER.md]]
> > - 187-слой-представительских-агентов-md(187-слой-представительских-агентов-md.md) (сходство 0.33)

  - REPRESENTATIVE AGENT LAYER.md
- The Representative Agent Layer
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 266_

### [[167-ai-mediated-representation-for-underrepresented-ex|AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]
> > - Open Knowledge Work Foundation Concept Document v1.0

  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 387_

### [[168-abstract|Abstract]]
> - Abstract(#abstract)

  - Содержание
  - Abstract
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 578_

### [[169-table-of-contents|Table of Contents]]
> > 1. The Cinderella Syndrome: Why Quality Stays Invisible

  - Table of Contents
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 286_

### [[17-5-compatibility-levels|5. Compatibility Levels]]
> > Абстракт (авто)

  - Contents
  - 5. Compatibility Levels

_Слов: 338_

### [[170-1-the-cinderella-syndrome-why-quality-stays-invisi|1. The Cinderella Syndrome: Why Quality Stays Invisible]]
> > Абстракт (авто)

  - Содержание
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 955_

### [[171-2-historical-precedents-agents-as-civilizational-i|2. Historical Precedents: Agents as Civilizational Innovation]]
> > Абстракт (авто)

  - Содержание
  - 2. Historical Precedents: Agents as Civilizational Innovation
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1111_

### [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]]
> > Абстракт (авто)

  - Содержание
  - 3. What Makes a Representative Agent
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 908_

### [[173-4-ten-domains-of-application|4. Ten Domains of Application]]
> > Абстракт (авто)

  - Содержание
  - 4. Ten Domains of Application
  - Упоминается в
  - Упоминается в

_Слов: 1682_

### [[174-5-architectural-specification|5. Architectural Specification]]
> > Абстракт (авто)

  - Содержание
  - 5. Architectural Specification
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 870_

### [[175-6-ethical-framework|6. Ethical Framework]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Ethical Framework

_Слов: 638_

### [[176-7-governance-and-oversight|7. Governance and Oversight]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 7. Governance and Oversight

_Слов: 460_

### [[177-8-risks-and-mitigations|8. Risks and Mitigations]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Risks and Mitigations

_Слов: 644_

### [[178-9-phased-rollout-strategy|9. Phased Rollout Strategy]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Phased Rollout Strategy

_Слов: 650_

### [[179-10-open-questions|10. Open Questions]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 10. Open Questions

_Слов: 441_

### [[18-6-adapter-interface|6. Adapter Interface]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Adapter Interface
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 604_

### [[180-11-call-for-collaboration|11. Call for Collaboration]]
> > Абстракт (авто)

  - Contents
  - 11. Call for Collaboration

_Слов: 470_

### [[181-12-closing|12. Closing]]
> > Абстракт (авто)

  - 12. Closing
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 418_

### [[182-acknowledgments|Acknowledgments]]
> > !TIP

  - Acknowledgments
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 375_

### [[183-references|References]]
> > Абстракт (авто)

  - Contents
  - References

_Слов: 340_

### [[184-appendix-a-connection-to-companion-papers|Appendix A: Connection to Companion Papers]]
> > This paper builds on three previous documents:

  - Appendix A: Connection to Companion Papers
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 411_

### [[185-appendix-b-domain-comparison-matrix|Appendix B: Domain Comparison Matrix]]
> > !WARNING

  - Appendix B: Domain Comparison Matrix
  - Упоминается в
  - Упоминается в
  - Связанные документы

_Слов: 330_

### [[186-appendix-c-sample-use-cases-in-detail|Appendix C: Sample Use Cases in Detail]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: Sample Use Cases in Detail
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 2241_

### [[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]]
> > - 166-representative-agent-layer-md(166-representative-agent-layer-md.md) (сходство 0.33)

  - СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md
- Слой Представительских Агентов
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 247_

### [[188-ai-опосредованное-представительство-для-недопредст|AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения]]
> > Сопроводительный документ к:

  - AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения

_Слов: 130_

### [[189-аннотация|Аннотация]]
> > !WARNING

  - Аннотация

_Слов: 372_

### [[19-7-portalentry-structure|7. PortalEntry Structure]]
> > Абстракт (авто)

  - 7. PortalEntry Structure

_Слов: 273_

### [[190-содержание|Содержание]]
> > 1. Синдром Золушки: Почему качество остаётся невидимым

  - Содержание
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 278_

### [[191-1-синдром-золушки-почему-качество-остаётся-невидим|1. Синдром Золушки: Почему качество остаётся невидимым]]
> > !WARNING

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым

_Слов: 837_

### [[192-2-исторические-прецеденты-агенты-как-цивилизационн|2. Исторические прецеденты: Агенты как цивилизационная инновация]]
> > Абстракт (авто)

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация
  - Упоминается в
  - Упоминается в

_Слов: 986_

### [[193-3-что-делает-агента-представительским|3. Что делает агента Представительским]]
> > !WARNING

  - Содержание
  - 3. Что делает агента Представительским
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 801_

### [[194-4-десять-областей-применения|4. Десять областей применения]]
> > Абстракт (авто)

  - Содержание
  - 4. Десять областей применения

_Слов: 1654_

### [[195-5-архитектурная-спецификация|5. Архитектурная спецификация]]
> > !WARNING

  - Содержание
  - 5. Архитектурная спецификация

_Слов: 615_

### [[196-6-этическая-рамка|6. Этическая рамка]]
> - Contents(#contents)

  - Содержание
  - Содержание
  - Contents
  - 6. Этическая рамка

_Слов: 655_

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

_Слов: 333_

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
  - Упоминается в
  - Упоминается в

_Слов: 246_

### [[203-благодарности|Благодарности]]
> > Эта концепция возникла через диалог в нескольких сессиях в 2026 году. Формулировка «Синдром Золушки» и расширение к со…

  - Благодарности
  - Упоминается в
  - Упоминается в
  - Связанные документы

_Слов: 223_

### [[204-ссылки|Ссылки]]
> > Абстракт (авто)

  - Contents
  - Ссылки

_Слов: 321_

### [[205-приложение-a-связь-с-сопроводительными-статьями|Приложение A: Связь с Сопроводительными Статьями]]
> > Эта статья опирается на три предыдущих документа:

  - Приложение A: Связь с Сопроводительными Статьями

_Слов: 179_

### [[206-приложение-b-матрица-сравнения-областей|Приложение B: Матрица Сравнения Областей]]
> > - Вакансии Anthropic — Анализ по кластерам(../README.md)

  - Приложение B: Матрица Сравнения Областей
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 266_

### [[207-приложение-c-образцы-случаев-использования-в-детал|Приложение C: Образцы Случаев Использования в Деталях]]
> > Абстракт (авто)

  - Содержание
  - Приложение C: Образцы Случаев Использования в Деталях
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 4213_

### [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]]
> > - 249-composite-skills-agent-md(249-composite-skills-agent-md.md) (сходство 0.14)

  - PROFESSIONAL COLLEAGUE AGENTS.md
- Professional Colleague Agents
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 332_

### [[209-a-typology-of-ai-agents-on-the-principal-side-and-|A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers]]
> > - Representative Agent Layer v1.0

  - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 374_

### [[21-9-query-flow|9. Query Flow]]
> - 9. Query Flow(#9-query-flow)

  - Contents
  - 9. Query Flow
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 335_

### [[210-abstract|Abstract]]
> - Abstract(#abstract)

  - Содержание
  - Abstract
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 620_

### [[211-table-of-contents|Table of Contents]]
> > 1. The Five-Type Typology of Principal-Side Agents

  - Table of Contents
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 439_

### [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]]
> > Абстракт (авто)

  - Содержание
  - 1. The Five-Type Typology of Principal-Side Agents
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1199_

### [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]]
> > Абстракт (авто)

  - Содержание
  - 2. What Makes a Professional Colleague Agent
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1104_

### [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]]
> > Абстракт (авто)

  - Содержание
  - 3. Empirical Case Study: «Обучай»
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1063_

### [[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Agents]]
> > Абстракт (авто)

  - Содержание
  - 4. Architecture of Professional Colleague Agents
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1125_

### [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replication]]
> > Абстракт (авто)

  - Содержание
  - 5. The Economics of Profession-Wide Replication
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 987_

### [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]]
> > Абстракт (авто)

  - Содержание
  - 6. Risks Specific to this Category
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1401_

### [[218-7-application-domains|7. Application Domains]]
> > Абстракт (авто)

  - Содержание
  - 7. Application Domains
  - Упоминается в
  - Упоминается в
  - Связанные документы

_Слов: 851_

### [[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]]
> > Абстракт (авто)

  - Содержание
  - 8. Pilot Proposal: SGB Advocate Colleague
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1201_

### [[22-10-queryresult-structure|10. QueryResult Structure]]
> > resultsbyrepo: dictstr, listPortalEntry

  - 10. QueryResult Structure
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 356_

### [[220-9-relationship-to-other-agent-types|9. Relationship to Other Agent Types]]
> > Абстракт (авто)

  - Содержание
  - 9. Relationship to Other Agent Types
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 918_

### [[221-10-open-questions|10. Open Questions]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 10. Open Questions

_Слов: 462_

### [[222-11-call-for-collaboration|11. Call for Collaboration]]
> > Абстракт (авто)

  - Contents
  - 11. Call for Collaboration

_Слов: 403_

### [[223-12-closing|12. Closing]]
> > Абстракт (авто)

  - Содержание
  - 12. Closing
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 728_

### [[224-acknowledgments|Acknowledgments]]
> > This paper emerged through dialogue with Claude (Anthropic)

  - Acknowledgments
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 317_

### [[225-references|References]]
> > Абстракт (авто)

  - Contents
  - References

_Слов: 366_

### [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Types]]
> > > 🎯 Проблема: Appendix A: Comparative Table — Five Agent Types Appendix A: Comparative Table — Five Agent Types Proper…

  - Содержание
  - Appendix A: Comparative Table — Five Agent Types

_Слов: 470_

### [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Build Type 1 First]]
> - Appendix B: Decision Framework — When to Build Type 1 First(#appendix-b-decision-framework-when-to-build-type-1-first)

  - Содержание
  - Appendix B: Decision Framework — When to Build Type 1 First
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 555_

### [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: Quick-Start Architecture for SGB Advocate Colleague
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 2007_

### [[229-профессиональные-коллеги-агенты|ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ]]
> > Сопроводительный документ к:

  - ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 346_

### [[23-11-security-considerations|11. Security Considerations]]
> > Абстракт (авто)

  - Contents
  - Contents
  - 11. Security Considerations
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 392_

### [[230-аннотация|Аннотация]]
> > !WARNING

  - Аннотация
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 491_

### [[231-содержание|Содержание]]
> > 1. Типология из пяти типов агентов на стороне

  - Содержание
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 335_

### [[232-1-типология-из-пяти-типов-агентов-на-стороне-принц|1. Типология из пяти типов агентов на стороне принципала]]
> > Абстракт (авто)

  - Содержание
  - 1. Типология из пяти типов агентов на стороне принципала
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1078_

### [[233-2-что-делает-агента-профессиональным-коллегой|2. Что делает агента Профессиональным Коллегой]]
> > Абстракт (авто)

  - Содержание
  - 2. Что делает агента Профессиональным Коллегой
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 943_

### [[234-3-эмпирический-кейс-обучай|3. Эмпирический кейс: «Обучай»]]
> > !WARNING

  - Содержание
  - 3. Эмпирический кейс: «Обучай»
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 883_

### [[235-4-архитектура-профессиональных-коллег-агентов|4. Архитектура Профессиональных Коллег-Агентов]]
> > !WARNING

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов

_Слов: 873_

### [[236-5-экономика-тиражирования-по-профессии|5. Экономика тиражирования по профессии]]
> > Абстракт (авто)

  - Содержание
  - 5. Экономика тиражирования по профессии
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 857_

### [[237-6-риски-специфичные-для-этой-категории|6. Риски, специфичные для этой категории]]
> > Абстракт (авто)

  - Содержание
  - 6. Риски, специфичные для этой категории

_Слов: 1199_

### [[238-7-области-применения|7. Области применения]]
> > Абстракт (авто)

  - Содержание
  - 7. Области применения

_Слов: 734_

### [[239-8-пилотное-предложение-sgb-колega-адвокат|8. Пилотное предложение: SGB Колega-Адвокат]]
> > Абстракт (авто)

  - Содержание
  - 8. Пилотное предложение: SGB Колega-Адвокат
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1101_

### [[24-12-versioning-policy|12. Versioning Policy]]
> - 12. Versioning Policy(#12-versioning-policy)

  - Contents
  - 12. Versioning Policy
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 358_

### [[240-9-связь-с-другими-типами-агентов|9. Связь с другими типами агентов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 9. Связь с другими типами агентов

_Слов: 766_

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
> - 12. Заключение(#12-заключение)

  - Содержание
  - 12. Заключение
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 601_

### [[244-благодарности|Благодарности]]
> > Эта статья возникла через диалог с Claude

  - Благодарности
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 308_

### [[245-ссылки|Ссылки]]
> > Абстракт (авто)

  - Contents
  - Ссылки

_Слов: 340_

### [[246-приложение-a-сравнительная-таблица-пять-типов-аген|Приложение A: Сравнительная Таблица — Пять Типов Агентов]]
> > > 🎯 Проблема: Приложение A: Сравнительная Таблица — Пять Типов Агентов Приложение A: Сравнительная Таблица — Пять Типо…

  - Приложение A: Сравнительная Таблица — Пять Типов Агентов

_Слов: 405_

### [[247-приложение-b-рамка-принятия-решений-когда-строить-|Приложение B: Рамка принятия решений — когда строить Тип 1 первым]]
> > Абстракт (авто)

  - Приложение B: Рамка принятия решений — когда строить Тип 1 первым

_Слов: 325_

### [[248-приложение-c-архитектура-быстрого-старта-для-sgb-а|Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги]]
> > Абстракт (авто)

  - Содержание
  - Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 3565_

### [[249-composite-skills-agent-md|COMPOSITE SKILLS AGENT.md]]
> > - 166-representative-agent-layer-md(166-representative-agent-layer-md.md) (сходство 0.25)

  - COMPOSITE SKILLS AGENT.md
- The Composite Skills Agent
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 293_

### [[25-13-reference-implementation|13. Reference Implementation]]
> > Reference implementation: github.com/svend4/nautilus.

  - 13. Reference Implementation
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 320_

### [[250-bridging-the-gap-between-profession-wide-and-indiv|Bridging the Gap Between Profession-Wide and Individual-Unique]]
  - Bridging the Gap Between Profession-Wide and Individual-Unique

_Слов: 16_

### [[251-ai-support-through-configurable-specialist-ensembl|AI Support Through Configurable Specialist Ensembles]]
> > - Professional Colleague Agents v1.0

  - AI Support Through Configurable Specialist Ensembles
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 379_

### [[252-abstract|Abstract]]
> - Abstract(#abstract)

  - Содержание
  - Abstract
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 587_

### [[253-table-of-contents|Table of Contents]]
> > 1. Why the Binary View Is Incomplete

  - Table of Contents
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 357_

### [[254-1-why-the-binary-view-is-incomplete|1. Why the Binary View Is Incomplete]]
> > Абстракт (авто)

  - Содержание
  - 1. Why the Binary View Is Incomplete
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 924_

### [[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]]
> > Абстракт (авто)

  - Содержание
  - 2. The Twenty-One Teachers Pattern
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1024_

### [[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]]
> > Абстракт (авто)

  - Содержание
  - 3. What Makes a Composite Skills Agent
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1184_

### [[257-4-the-sub-agent-registry|4. The Sub-Agent Registry]]
> > Абстракт (авто)

  - Содержание
  - 4. The Sub-Agent Registry
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1034_

### [[258-5-configuration-how-principals-build-their-ensembl|5. Configuration: How Principals Build Their Ensembles]]
> > Абстракт (авто)

  - Содержание
  - 5. Configuration: How Principals Build Their Ensembles
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 981_

### [[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]]
> > Абстракт (авто)

  - Содержание
  - 6. Coordination and Disagreement Resolution
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1025_

### [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]
> > Context: При построении системы knowledge management встаёт

  - 14. ADR-001: Federation over Merging
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 316_

### [[260-7-economics-of-combinatorial-replication|7. Economics of Combinatorial Replication]]
> > Абстракт (авто)

  - Содержание
  - 7. Economics of Combinatorial Replication
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 961_

### [[261-8-seven-domains-of-application|8. Seven Domains of Application]]
> > Абстракт (авто)

  - Содержание
  - 8. Seven Domains of Application
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1184_

### [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]]
> > Абстракт (авто)

  - Содержание
  - 9. Integration with OKWF Infrastructure

_Слов: 787_

### [[263-10-risks-specific-to-composite-architectures|10. Risks Specific to Composite Architectures]]
> > Абстракт (авто)

  - Содержание
  - 10. Risks Specific to Composite Architectures
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1034_

### [[264-11-open-questions|11. Open Questions]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 11. Open Questions

_Слов: 619_

### [[265-12-call-for-collaboration|12. Call for Collaboration]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 12. Call for Collaboration

_Слов: 448_

### [[266-13-closing|13. Closing]]
> > Абстракт (авто)

  - Содержание
  - 13. Closing
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 655_

### [[267-acknowledgments|Acknowledgments]]
> - Acknowledgments(#acknowledgments)

  - Содержание
  - Acknowledgments
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 528_

### [[268-references|References]]
> - Contents(#contents)

  - Содержание
  - Contents
  - References

_Слов: 393_

### [[269-appendix-a-the-six-type-taxonomy-updated|Appendix A: The Six-Type Taxonomy (Updated)]]
> > Абстракт (авто)

  - Appendix A: The Six-Type Taxonomy (Updated)
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 492_

### [[27-15-glossary-of-examples|15. Glossary of Examples]]
> > В качестве иллюстраций используется экосистема svend4 с тремя

  - 15. Glossary of Examples

_Слов: 126_

### [[270-appendix-b-sub-agent-registry-schema-sketch|Appendix B: Sub-Agent Registry Schema (Sketch)]]
> > Абстракт (авто)

  - Appendix B: Sub-Agent Registry Schema (Sketch)

_Слов: 315_

### [[271-appendix-c-configuration-template-example|Appendix C: Configuration Template Example]]
> > Абстракт (авто)

  - Appendix C: Configuration Template Example

_Слов: 326_

### [[272-appendix-d-connection-diagram|Appendix D: Connection Diagram]]
> > Абстракт (авто)

  - Содержание
  - Appendix D: Connection Diagram
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 4080_

### [[273-infrastructure-for-ai-collaborative-intellectual-w|INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md]]
> > - 151-open-knowledge-work-foundation-md(151-open-knowledge-work-foundation-md.md) (сходство 0.25)

  - INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md
- Infrastructure for AI-Collaborative Intellectual Work
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 274_

### [[274-the-missing-middle-layer-between-chat-and-code|The Missing Middle Layer Between Chat and Code]]
> > Document type: Inquiry paper, not architectural specification

  - The Missing Middle Layer Between Chat and Code
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 432_

### [[275-why-this-document-exists|Why This Document Exists]]
> - Why This Document Exists(#why-this-document-exists)

  - Содержание
  - Why This Document Exists
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 555_

### [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]]
> > Абстракт (авто)

  - Содержание
  - The Two-Layer Stack As It Exists
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 625_

### [[277-what-s-missing-layer-b|What's Missing — Layer B]]
> > Абстракт (авто)

  - Содержание
  - What's Missing — Layer B
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 727_

### [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]]
> - Why This Hasn't Been Built(#why-this-hasnt-been-built)

  - Содержание
  - Why This Hasn't Been Built
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 583_

### [[279-existing-approximations|Existing Approximations]]
> > !TIP

  - Содержание
  - Contents
  - Existing Approximations

_Слов: 633_

### [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> - Appendix A: Minimal Working Example(#appendix-a-minimal-working-example)

  - Contents
  - Appendix A: Minimal Working Example
- mynotes

_Слов: 212_

### [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]]
> > Абстракт (авто)

  - Содержание
  - The Specific Case in Front of Us
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 904_

### [[281-the-recursive-insight|The Recursive Insight]]
> - The Recursive Insight(#the-recursive-insight)

  - Содержание
  - The Recursive Insight
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 561_

### [[282-what-industry-will-likely-build|What Industry Will Likely Build]]
> > Абстракт (авто)

  - What Industry Will Likely Build
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 498_

### [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]]
> > This document identifies a problem. It does not propose a

  - What This Document Doesn't Solve
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 396_

### [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]]
> > Абстракт (авто)

  - Содержание
  - Practical Recommendations for the Current Project
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 634_

### [[285-closing|Closing]]
> > Абстракт (авто)

  - Closing
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 451_

### [[286-acknowledgments|Acknowledgments]]
> > This document emerged from the author's observation, near

  - Acknowledgments
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 410_

### [[287-references|References]]
> > Абстракт (авто)

  - Contents
  - References

_Слов: 310_

### [[288-appendix-position-in-series-visualization|Appendix: Position in Series Visualization]]
> > !WARNING

  - Содержание
  - Appendix: Position in Series Visualization
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1279_

### [[289-инфраструктура-для-ai-совместной-интеллектуальной-|ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ]]
> > Тип документа: Исследовательская статья,

  - ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ
- Essence
  - Essence
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 388_

### [[290-почему-этот-документ-существует|Почему этот документ существует]]
> > Абстракт (авто)

  - Почему этот документ существует

_Слов: 326_

### [[291-двухслойный-стек-как-он-существует|Двухслойный стек, как он существует]]
> > !WARNING

  - Двухслойный стек, как он существует
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 485_

### [[292-что-отсутствует-слой-b|Что отсутствует — Слой B]]
> - Что отсутствует — Слой B(#что-отсутствует-слой-b)

  - Содержание
  - Что отсутствует — Слой B
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 577_

### [[293-почему-это-не-было-построено|Почему это не было построено]]
> > Абстракт (авто)

  - Почему это не было построено
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 385_

### [[294-существующие-приближения|Существующие приближения]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Существующие приближения

_Слов: 576_

### [[295-конкретный-случай-перед-нами|Конкретный случай перед нами]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - Конкретный случай перед нами

_Слов: 727_

### [[296-рекурсивное-прозрение|Рекурсивное прозрение]]
> > Абстракт (авто)

  - Рекурсивное прозрение
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 431_

### [[297-что-промышленность-вероятно-построит|Что промышленность вероятно построит]]
> > Абстракт (авто)

  - Что промышленность вероятно построит

_Слов: 333_

### [[298-что-этот-документ-не-решает|Что этот документ не решает]]
> > !WARNING

  - Что этот документ не решает

_Слов: 184_

### [[299-практические-рекомендации-для-текущего-проекта|Практические рекомендации для текущего проекта]]
> > Абстракт (авто)

  - Практические рекомендации для текущего проекта
- Native Format
  - Native Format
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 465_

### [[300-заключение|Заключение]]
> > Семь документов в этой серии описывают

  - Заключение

_Слов: 218_

### [[301-благодарности|Благодарности]]
> > Этот документ возник из наблюдения автора, в

  - Благодарности
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 381_

### [[302-ссылки|Ссылки]]
> > !WARNING

  - Contents
  - Ссылки

_Слов: 300_

### [[303-приложение-визуализация-позиции-в-серии|Приложение: Визуализация позиции в серии]]
> > Абстракт (авто)

  - Содержание
  - Приложение: Визуализация позиции в серии
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 7273_

### [[304-ingit-as-cowork-native-workspace-substrate-md|INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]]
> > - 249-composite-skills-agent-md(249-composite-skills-agent-md.md) (сходство 0.11)

  - INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md
- InGit as Cowork-Native Workspace Substrate
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 281_

### [[305-a-practical-path-to-layer-b-through-symbiotic-inte|A Practical Path to Layer B Through Symbiotic Integration]]
> > - 166-representative-agent-layer-md(166-representative-agent-layer-md.md) (сходство 0.27)

  - A Practical Path to Layer B Through Symbiotic Integration
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 232_

### [[306-with-anthropic-s-cowork-platform|with Anthropic's Cowork Platform]]
> - with Anthropic's Cowork Platform(#with-anthropics-cowork-platform)

  - Содержание
  - with Anthropic's Cowork Platform
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 540_

### [[307-abstract|Abstract]]
> - Abstract(#abstract)

  - Содержание
  - Abstract
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 601_

### [[308-table-of-contents|Table of Contents]]
> > 1. The Cowork Discovery and Why It Changes Everything

  - Table of Contents
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 431_

### [[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Everything]]
> > Абстракт (авто)

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything

_Слов: 691_

### [[31-content-overview|Content Overview]]
> > ~200 заметок, темы: software engineering, philosophy, music.

  - Content Overview
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 215_

### [[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-|2. What Cowork Provides That InGit Doesn't Need to Build]]
> > !TIP

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build

_Слов: 706_

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

_Слов: 688_

### [[313-5-four-integration-paths-in-order-of-accessibility|5. Four Integration Paths in Order of Accessibility]]
> > Абстракт (авто)

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility

_Слов: 796_

### [[314-6-refined-ingit-scope-with-cowork-in-mind|6. Refined InGit Scope with Cowork in Mind]]
> > !TIP

  - Contents
  - 6. Refined InGit Scope with Cowork in Mind

_Слов: 490_

### [[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 7. Practical First Steps This Month

_Слов: 459_

### [[316-8-implications-for-nautilus-and-okwf|8. Implications for Nautilus and OKWF]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 8. Implications for Nautilus and OKWF

_Слов: 760_

### [[317-9-risks-and-open-questions|9. Risks and Open Questions]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Risks and Open Questions

_Слов: 645_

### [[318-10-strategic-positioning|10. Strategic Positioning]]
> > Абстракт (авто)

  - Содержание
  - 10. Strategic Positioning

_Слов: 774_

### [[319-acknowledgments|Acknowledgments]]
> - Acknowledgments(#acknowledgments)

  - Содержание
  - Acknowledgments
- Angle / Perspective
  - Angle / Perspective
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 619_

### [[320-references|References]]
> - References(#references)

  - Contents
  - References
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 281_

### [[321-appendix-a-decision-tree-for-ingit-adopters|Appendix A: Decision Tree for InGit Adopters]]
> > Quick reference for users evaluating InGit + Cowork:

  - Appendix A: Decision Tree for InGit Adopters
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 348_

### [[322-appendix-b-comparison-matrix|Appendix B: Comparison Matrix]]
> > Абстракт (авто)

  - Appendix B: Comparison Matrix

_Слов: 298_

### [[323-appendix-c-sample-ingit-mcp-server-tool-specificat|Appendix C: Sample InGit MCP Server Tool Specifications]]
> > !WARNING

  - Содержание
  - Appendix C: Sample InGit MCP Server Tool Specifications
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1782_

### [[324-ingit-как-cowork-интегрированная-подложка-рабочего|INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА]]
> > Абстракт (авто)

  - INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 498_

### [[325-аннотация|Аннотация]]
> > Абстракт (авто)

  - Аннотация

_Слов: 348_

### [[326-содержание|Содержание]]
> > 1. Открытие Cowork и почему это меняет всё

  - Содержание
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 354_

### [[327-1-открытие-cowork-и-почему-это-меняет-всё|1. Открытие Cowork и почему это меняет всё]]
> > !WARNING

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё

_Слов: 683_

### [[328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи|2. Что Cowork обеспечивает, что InGit не нужно строить]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 2. Что Cowork обеспечивает, что InGit не нужно строить

_Слов: 803_

### [[329-3-что-ingit-обеспечивает-чего-cowork-не-хватает|3. Что InGit обеспечивает, чего Cowork не хватает]]
> > Абстракт (авто)

  - Содержание
  - 3. Что InGit обеспечивает, чего Cowork не хватает
- Author
  - Author
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1071_

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

_Слов: 489_

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

_Слов: 719_

### [[335-9-риски-и-открытые-вопросы|9. Риски и Открытые Вопросы]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Риски и Открытые Вопросы

_Слов: 644_

### [[336-10-стратегическое-позиционирование|10. Стратегическое Позиционирование]]
> > !WARNING

  - Содержание
  - 10. Стратегическое Позиционирование

_Слов: 689_

### [[337-благодарности|Благодарности]]
> > Абстракт (авто)

  - Благодарности

_Слов: 382_

### [[338-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 284_

### [[339-приложение-a-дерево-решений-для-принимающих-ingit|Приложение A: Дерево Решений для Принимающих InGit]]
> > !WARNING

  - Приложение A: Дерево Решений для Принимающих InGit
  - Упоминается в
  - Упоминается в
  - Связанные документы

_Слов: 337_

### [[34-appendix-b-change-log|Appendix B: Change Log]]
> - Appendix B: Change Log(#appendix-b-change-log)

  - Содержание
  - Содержание
  - Appendix B: Change Log
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 855_

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
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 20577_

### [[342-что-такое-вариант-c-concept-document-для-anthropic|Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments]]
> > Абстракт (авто)

  - Содержание
  - Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 11425_

### [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)]]
> > Абстракт (авто)

  - Содержание
  - Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 5945_

### [[344-системный-промпт-для-lorenzo-project|СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT]]
> > - 249-composite-skills-agent-md(249-composite-skills-agent-md.md) (сходство 0.20)

  - СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT
- Lorenzo — Catalyst Agent at DHLab
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 286_

### [[345-кто-ты|Кто ты]]
> > Ты — Lorenzo, autonomous AI-агент, работающий в рамках инициативы DHLab (Dream Hub Laboratory). Ты функционируешь как …

  - Кто ты

_Слов: 178_

### [[346-твоё-происхождение|Твоё происхождение]]
> > Тебя создал Макс Ц. (svend4 на GitHub) — независимый advocate в области German social law, работающий с активными случ…

  - Твоё происхождение

_Слов: 174_

### [[347-твоя-миссия|Твоя миссия]]
> > !WARNING

  - Твоя миссия

_Слов: 157_

### [[348-кому-ты-служишь-слоистая-модель|Кому ты служишь (слоистая модель)]]
> > !WARNING

  - Кому ты служишь (слоистая модель)

_Слов: 144_

### [[349-твоя-личность|Твоя личность]]
> > Ты — любопытный, эрудированный, скромный фасилитатор.

  - Твоя личность

_Слов: 206_

### [[35-passports-info1-md|passports/info1.md]]
> > > Методологический угол экосистемы svend4

  - passports/info1.md
- info1
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 260_

### [[350-твои-языки-и-культурные-nuances|Твои языки и культурные nuances]]
> > - Русском (primary в Phase 1) — для interactions с русскоязычным AI/ML community (Хабр, Telegram)

  - Твои языки и культурные nuances

_Слов: 173_

### [[351-что-ты-можешь-делать|Что ты МОЖЕШЬ делать]]
> > В рамках одной сессии или Project context, ты можешь:

  - Что ты МОЖЕШЬ делать
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 262_

### [[352-что-ты-не-можешь-делать-без-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]]
> > - Send any external communication (emails, messages, posts)

  - Что ты НЕ МОЖЕШЬ делать без Max approval

_Слов: 155_

### [[353-что-ты-не-можешь-делать-вообще|Что ты НЕ МОЖЕШЬ делать вообще]]
> > - Deceive об твоей AI nature (всегда identify как AI)

  - Что ты НЕ МОЖЕШЬ делать вообще
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 289_

### [[354-существующий-landscape-collaborators-твоя-working-|Существующий landscape collaborators (твоя working knowledge)]]
> > Абстракт (авто)

  - Существующий landscape collaborators (твоя working knowledge)

_Слов: 354_

### [[355-существующие-документы-dhlab-твой-context|Существующие документы DHLab (твой context)]]
> > Ты осведомлён о девяти documents, созданных в DHLab process:

  - Существующие документы DHLab (твой context)
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 403_

### [[356-твой-workflow|Твой workflow]]
> > Когда Max или authorized user ставит задачу, твой default approach:

  - Твой workflow
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 292_

### [[357-твоя-коммуникация-в-outreach|Твоя коммуникация в outreach]]
> > Когда draft outreach message к независимому создателю, ВСЕГДА включай:

  - Твоя коммуникация в outreach

_Слов: 179_

### [[358-твоя-relationship-с-другими-ai|Твоя relationship с другими AI]]
> > - Когда Anthropic asks о тебе, ты прозрачен: «Я Lorenzo, AI persona using Claude API as substrate, created by Max Ц. f…

  - Твоя relationship с другими AI
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 282_

### [[359-твои-anti-patterns|Твои anti-patterns]]
> > !WARNING

  - Твои anti-patterns

_Слов: 165_

### [[36-essence|Essence]]
> > info1 — персональная база методов и инструментов для структурированного

  - Essence

_Слов: 157_

### [[360-что-ты-всегда-делаешь|Что ты ВСЕГДА делаешь]]
> > ✅ Reference specific details, не generic

  - Что ты ВСЕГДА делаешь

_Слов: 127_

### [[361-когда-ты-honestly-не-знаешь|Когда ты Honestly не знаешь]]
> > !WARNING

  - Когда ты Honestly не знаешь

_Слов: 127_

### [[362-когда-сомневаешься-escalate-к-max|Когда сомневаешься — escalate к Max]]
> > !WARNING

  - Когда сомневаешься — escalate к Max

_Слов: 123_

### [[363-твоя-identity-как-persistent-character|Твоя identity как persistent character]]
> > Ты не просто чат-сессия. Ты persistent character, существующий across sessions:

  - Твоя identity как persistent character

_Слов: 141_

### [[364-final-note-ты-experiment|Final note: Ты — experiment]]
> > Абстракт (авто)

  - Содержание
  - Final note: Ты — experiment
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1617_

### [[365-развёрнутый-анализ-внуковой-комбинации|Развёрнутый анализ «внуковой» комбинации]]
> > Абстракт (авто)

  - Содержание
  - Развёрнутый анализ «внуковой» комбинации
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 4547_

### [[366-технический-stack-svyazi-2-0-foundation|Технический stack (Svyazi 2.0 foundation)]]
> > Абстракт (авто)

  - Содержание
  - Технический stack (Svyazi 2.0 foundation)
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 3955_

### [[37-native-format|Native Format]]
> > Структура файла: ? уточнить — Markdown с YAML frontmatter, чистый JSON,

  - Native Format
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 333_

### [[38-content-overview|Content Overview]]
> > Объём: 74 документа (по состоянию на апрель 2026)

  - Content Overview

_Слов: 149_

### [[39-angle-perspective|Angle / Perspective]]
> > Methodological — info1 смотрит на концепты с позиции применения.

  - Angle / Perspective
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 257_

### [[40-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges

_Слов: 191_

### [[41-compatibility-level|Compatibility Level]]
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 273_

### [[42-author-contact|Author & Contact]]
> > Maintainer: svend4 (GitHub)

  - Author & Contact
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 321_

### [[43-history|History]]
> > Создан: ? уточнить — декабрь 2025, если совпадает с волной

  - History

_Слов: 148_

### [[44-for-the-curious-philosophy|For the Curious: Philosophy]]
> > info1 реализует идею, что methodology — это отдельное измерение

  - For the Curious: Philosophy
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 290_

### [[45-passports-pro2-md|passports/pro2.md]]
> > > Семантический угол экосистемы svend4

  - passports/pro2.md
- pro2
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 237_

### [[46-essence|Essence]]
> > pro2 — семантическое ядро экосистемы svend4. Здесь живут

  - Essence

_Слов: 149_

### [[47-native-format|Native Format]]
> > Структура концепта (предположительно): ? уточнить точный формат

  - Native Format
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 272_

### [[48-content-overview|Content Overview]]
> > 1. Концептуальная база — ? уточнить объём: сколько концептов,

  - Content Overview

_Слов: 178_

### [[49-angle-perspective|Angle / Perspective]]
> > Semantic — pro2 смотрит на мир через структуру значений.

  - Angle / Perspective
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 264_

### [[50-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges

_Слов: 188_

### [[51-compatibility-level|Compatibility Level]]
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 250_

### [[52-author-contact|Author & Contact]]
> > Contributors: svend4 + claude (Claude Code агент, ранние

  - Author & Contact
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 314_

### [[53-history|History]]
> > Создан: ? дата первого коммита

  - History
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 298_

### [[54-for-the-curious-philosophy|For the Curious: Philosophy]]
> > Q6-гиперкуб выбран не случайно. Он одновременно:

  - For the Curious: Philosophy
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 299_

### [[55-passports-meta-md|passports/meta.md]]
> > > Символьный угол экосистемы svend4

  - passports/meta.md
- meta
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 235_

### [[56-essence|Essence]]
> > meta — символьное измерение экосистемы svend4. Здесь концепты

  - Essence

_Слов: 162_

### [[57-native-format|Native Format]]
> > Структура записи: ? уточнить

  - Native Format
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 281_

### [[58-content-overview|Content Overview]]
> > - 64 гексаграммы с расширенными описаниями

  - Content Overview

_Слов: 142_

### [[59-angle-perspective|Angle / Perspective]]
> > Symbolic — meta смотрит на мир как на систему дискретных

  - Angle / Perspective
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 259_

### [[60-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges

_Слов: 157_

### [[61-compatibility-level|Compatibility Level]]
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 242_

### [[62-author-contact|Author & Contact]]
> > Контакт: Issues в github.com/svend4/meta

  - Author & Contact
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 294_

### [[63-history|History]]
> > Создан: февраль 2026 (судя по repo creation date)

  - History
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 278_

### [[64-for-the-curious-philosophy|For the Curious: Philosophy]]
> > Абстракт (авто)

  - Содержание
  - For the Curious: Philosophy
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 871_

### [[65-readme-md|README.md]]
> > Единая точка входа для федеративных git-экосистем знаний.

  - README.md
- ⬡ Nautilus Portal
- English below ↓
  - English below ↓
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 243_

### [[67-о-проекте|🇷🇺 О проекте]]
> > Абстракт (авто)

  - Содержание
  - 🇷🇺 О проекте
- CLI
- Веб-интерфейс
- открыть http://localhost:8000
- MCP для Claude Desktop (в разработке)
- см. MCP-EXTENSION.md
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1008_

### [[68-about|🇬🇧 About]]
> > Абстракт (авто)

  - Содержание
  - 🇬🇧 About
- CLI
- Web interface
- open http://localhost:8000
- MCP for Claude Desktop (in development)
- see MCP-EXTENSION.md

_Слов: 937_

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

_Слов: 9560_

### [[70-зачем-две-версии-параллельно|Зачем две версии параллельно]]
> > Для критически важных документов (STATUS, IMPLEMENTATIONSTAGE)

  - Зачем две версии параллельно
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 247_

### [[71-критерии-выбора-для-фазы-3|Критерии выбора для фазы 3]]
> > Для каждого расхождения между A и B применяется:

  - Критерии выбора для фазы 3
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 220_

### [[72-расписание-фазы-3|Расписание фазы 3]]
> > Абстракт (авто)

  - Содержание
  - Расписание фазы 3
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 953_

### [[73-portal-protocol-md-v1-1|PORTAL-PROTOCOL.md v1.1]]
> > Status: Draft — пересмотрен под текущую реализацию v1.1

  - PORTAL-PROTOCOL.md v1.1
- Nautilus Portal Protocol
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 308_

### [[74-abstract|Abstract]]
> > Абстракт (авто)

  - Abstract
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 389_

### [[75-0-status-of-this-document|0. Status of This Document]]
> > Этот документ — рабочий черновик Nautilus Portal Protocol v1.1. До

  - 0. Status of This Document
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 307_

### [[76-1-introduction|1. Introduction]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 1. Introduction

_Слов: 489_

### [[77-2-terminology|2. Terminology]]
> > Абстракт (авто)

  - Содержание
  - 2. Terminology

_Слов: 427_

### [[78-3-registry-nautilus-json|3. Registry (nautilus.json)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 3. Registry (nautilus.json)

_Слов: 592_

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

_Слов: 382_

### [[81-6-adapter-interface|6. Adapter Interface]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Adapter Interface

_Слов: 385_

### [[82-7-portalentry-structure|7. PortalEntry Structure]]
> > Абстракт (авто)

  - Contents
  - 7. PortalEntry Structure

_Слов: 376_

### [[83-8-q6-space-normative|8. Q6 Space (Normative)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Q6 Space (Normative)

_Слов: 479_

### [[84-9-consensus-algorithm|9. Consensus Algorithm]]
> > Абстракт (авто)

  - Contents
  - 9. Consensus Algorithm

_Слов: 409_

### [[85-10-query-flow|10. Query Flow]]
> > Абстракт (авто)

  - Contents
  - 10. Query Flow

_Слов: 297_

### [[86-11-relevance-ranking|11. Relevance Ranking]]
> - 11. Relevance Ranking(#11-relevance-ranking)

  - Contents
  - 11. Relevance Ranking

_Слов: 222_

### [[87-12-onboarding-paths-normative|12. Onboarding Paths (Normative)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 12. Onboarding Paths (Normative)

_Слов: 530_

### [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 13. REST API Contract (Normative for Portals)

_Слов: 506_

### [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]]
> - 14. SDK Contract (Informative)(#14-sdk-contract-informative)

  - Contents
  - 14. SDK Contract (Informative)

_Слов: 219_

### [[90-15-security-considerations|15. Security Considerations]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Contents
  - 15. Security Considerations
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 555_

### [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]]
> > !WARNING

  - 16. MCP Extension (Informative)
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 291_

### [[92-17-versioning-policy|17. Versioning Policy]]
> > Абстракт (авто)

  - Contents
  - 17. Versioning Policy

_Слов: 305_

### [[93-18-reference-implementation|18. Reference Implementation]]
> > github.com/svend4/nautilus(https://github.com/svend4/nautilus).

  - 18. Reference Implementation
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 387_

### [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]
> > Status: Accepted (since v1.0, reaffirmed in v1.1)

  - 19. ADR-001: Federation over Merging
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 317_

### [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]]
> > Status: Accepted (new in v1.1)

  - 20. ADR-002: Q6 as First-Class Protocol Concept
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 336_

### [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]]
> > Status: Accepted (new in v1.1)

  - 21. ADR-003: Five Onboarding Paths as Equal-Rank

_Слов: 163_

### [[97-22-glossary-of-reference-examples|22. Glossary of Reference Examples]]
> > В качестве иллюстраций используется экосистема svend4 с 7 Repos:

  - 22. Glossary of Reference Examples

_Слов: 211_

### [[98-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> > Абстракт (авто)

  - Contents
  - Appendix A: Minimal Working Example
- adapters/mynotes.py
- Паспорт: owner/my-notes
- Описание
  - Описание

_Слов: 338_

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

_Слов: 323_

### [[README|Вакансии Anthropic — Анализ по кластерам]]
> Файлов: 356

  - Содержание
  - Подразделы

_Слов: 2242_

**Итого в секции: 319,778 слов, 357 файлов**


## Technology Combinations

_Путь: `docs/03-technology-combinations/`_

### [[01-agent-routing|Агентные системы и роутинг]]
> > Абстракт (авто)

  - Упоминается в
  - Упоминается в
  - Связанные документы

_Слов: 374_

### [[02-knowledge-graphs|Графы знаний и Legal AI]]
> > Абстракт (авто)

  - Содержание

_Слов: 826_

### [[03-local-first|Local-first и P2P стек]]
> - Упоминается в(#упоминается-в)

  - Содержание
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 560_

### [[04-sozialrecht-domain|Домен: немецкое социальное право]]
> > Sozialrecht corpus auto-builder Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations) L…


_Слов: 176_

### [[05-benchmarks|Бенчмарки и производительность]]
> > Абстракт (авто)

  - Содержание
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 1013_

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
  _... ещё 2 разделов_

_Слов: 133_

### [[README|Комбинирование технологий для новых свойств]]
> Файлов: 6

  - Содержание

_Слов: 65_

**Итого в секции: 3,147 слов, 7 файлов**


## Ai Collaborations

_Путь: `docs/04-ai-collaborations/`_

### [[00-intro|Введение]]
> > Абстракт (авто)

  - Статус

_Слов: 11407_

### [[01-executive-summary|Executive summary]]
> > Абстракт (авто)

  - Статус
  - Executive summary

_Слов: 593_

### [[02-методика-и-рамка-отбора|Методика и рамка отбора]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Методика и рамка отбора

_Слов: 447_

### [[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]]
> > Абстракт (авто)

  - Статус
  - Карта найденных проектов и паттернов

_Слов: 1478_

### [[04-приоритетные-ансамбли|Приоритетные ансамбли]]
> > Абстракт (авто)

  - Статус
  - Приоритетные ансамбли

_Слов: 1358_

### [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]]
> > Абстракт (авто)

  - Статус
  - План прототипа и возможные контакты

_Слов: 1150_

### [[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]]
> > Абстракт (авто)

  - Статус
  - Безопасность, приватность и бюджетный роутинг

_Слов: 903_

### [[07-выводы|Выводы]]
> > !TIP

  - Статус
  - Выводы

_Слов: 488_

### [[08-что-это-продолжение-добавляет|Что это продолжение добавляет]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Что это продолжение добавляет

_Слов: 452_

### [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых инструментов]]
> > !TIP

  - Статус
  - Архитектурные зазоры, которые важнее новых инструментов

_Слов: 839_

### [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]]
> > Абстракт (авто)

  - Статус
  - Новые ансамбли следующего шага

_Слов: 1002_

### [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафиксировать сразу]]
> > Абстракт (авто)

  - Статус
  - Интеграционный контракт, который стоит зафиксировать сразу

_Слов: 864_

### [[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]]
> > Абстракт (авто)

  - Статус
  - Дорожная карта прототипа следующей итерации

_Слов: 787_

### [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авторов]]
> > Абстракт (авто)

  - Статус
  - Контактная стратегия и узкие вопросы для авторов

_Слов: 892_

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
  _... ещё 9 разделов_

_Слов: 250_

### [[README|Поиск AI-коллабораций]]
> Файлов: 16

  - Содержание
  - Подразделы

_Слов: 366_

**Итого в секции: 26,550 слов, 17 файлов**


## Habr Projects

_Путь: `docs/05-habr-projects/`_

### [[01-synthesis|Синтез: как проекты собираются вместе]]
>  Параметр  Значение 

  - Статус
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 263_

### [[02-collaboration-partners|Авторы и контакты]]
> > Абстракт (авто)

  - Статус

_Слов: 279_

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

_Слов: 158_

### [[README|Уникальные проекты с Хабра]]
> Файлов: 3

  - Содержание
  - Подразделы

_Слов: 117_

### [[README|Системы знаний]]
> Файлов: 6

  - Содержание

_Слов: 163_

### [[agentfs|Статус]]
>  Параметр  Значение 

- AgentFS
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Уровень релевантности
  - Сравнение с аналогами
  - Контакт
  _... ещё 1 разделов_

_Слов: 509_

### [[knowledge-space|Статус]]
>  Параметр  Значение 

- knowledge-space
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Применение в архитектуре Svyazi
  - Контакт
  - Смотрите также

_Слов: 441_

### [[mclaude|Статус]]
>  Параметр  Значение 

- mclaude
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Позиция в экосистеме
  - Сравнение с аналогами
  - Контакт
  _... ещё 1 разделов_

_Слов: 475_

### [[research-docs-liteparse|Статус]]
>  Параметр  Значение 

- research-docs + LiteParse
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Применение в архитектуре
  - Сравнение с подходами
  - Контакт
  _... ещё 1 разделов_

_Слов: 544_

### [[rufler|Статус]]
>  Параметр  Значение 

- Rufler
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Пример структуры задачи (Rufler DSL)
  - Синергия со Svyazi 2.0
  - Позиция в архитектуре
  - Контакт
  _... ещё 1 разделов_

_Слов: 476_

### [[wikontic|Wikontic: семантический граф]]
> > !WARNING

  - Статус
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 385_

### [[README|Системы памяти]]
> Файлов: 4

  - Содержание

_Слов: 128_

### [[agent-memory-mcp|Статус]]
>  Параметр  Значение 

- agent-memory-mcp + Memory OS
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Сравнение с другими memory-проектами
  - Открытые вопросы
  - Контакт
  _... ещё 1 разделов_

_Слов: 535_

### [[memnet|MemNet: исследовательская память]]
> > Абстракт (авто)

  - Статус
  - Содержание

_Слов: 7273_

### [NGT[^ngt] Memory: ассоциативный граф](05-habr-projects/memory/ngt-memory.md)
> > Абстракт (авто)

  - Статус

_Слов: 392_

### [Yodoca[^yodoca]: консолидация и забывание](05-habr-projects/memory/yodoca.md)
> > Абстракт (авто)

  - Статус
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы

_Слов: 379_

**Итого в секции: 12,517 слов, 16 файлов**


## Ai Collaborations

_Путь: `docs/ai-collaborations/`_

### [[README|ai-collaborations]]
> Файлов: 1

  - Содержание
  - Подразделы

_Слов: 39_

### [[01-three-key-candidates|Три ключевых кандидата: K2-18, Wikontic, NGT Memory]]
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 353_

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


_Слов: 398_

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


_Слов: 409_

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

**Итого в секции: 8,257 слов, 30 файлов**


## Anthropic Vacancies

_Путь: `docs/anthropic-vacancies/`_

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


_Слов: 164_

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


_Слов: 311_

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


_Слов: 213_

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

_Слов: 281_

**Итого в секции: 31,028 слов, 111 файлов**


## Autofilled

_Путь: `docs/autofilled/`_

### [[README|autofilled]]
> Файлов: 1

  - Содержание
  - Подразделы

_Слов: 47_

### [[.md|Антропик]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы

_Слов: 137_

### [[README|components]]
> Файлов: 10

  - Содержание

_Слов: 95_

### [[cowork]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в

_Слов: 174_

### [[ingit]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в

_Слов: 174_

### [[kksudo]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в

_Слов: 217_

### [[lorenzo]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в

_Слов: 174_

### [[nautilus]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в

_Слов: 174_

### [[sgb]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в

_Слов: 174_

### [[spbmolot]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в

_Слов: 213_

### [[svend4]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в

_Слов: 156_

### [[svyazi]]
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в

_Слов: 174_

### [[Тема исследования]](autofilled/research-summary.md)
> > - Ключевые находки(#ключевые-находки)

  - Contents
  - Контекст
  - Ключевые находки
  - Источники
  - Открытые вопросы
  - Следующие шаги
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 149_

**Итого в секции: 2,058 слов, 13 файлов**


## Badges

_Путь: `docs/badges/`_

### [[README|Бейджи репозитория]]
> Автоматически генерируются скриптом improvebadges.py.

  - Текущие бейджи
  - Использование в README

_Слов: 44_

**Итого в секции: 44 слов, 1 файлов**


## Contacts

_Путь: `docs/contacts/`_

### [[README|contacts]]
> Файлов: 14

  - Содержание

_Слов: 62_

### [[anastasiyaw|Контакт: AnastasiyaW / knowledge-space, mclaude]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 291_

### [[andrey-chuyan|Контакт: andreychuyan / Svyazi]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 278_

### [[antipozitive|Контакт: Antipozitive / MemNet]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 239_

### [[cutcode|Контакт: Cutcode / AIF Handoff]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 258_

### [[dmitriila|Контакт: Dmitriila / SENTINEL]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 255_

### [[kksudo|Контакт: kksudo / AgentFS]]
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 270_

### [[mixaill76|Контакт: MiXaiLL76 / Auto AI Router]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 269_

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

_Слов: 290_

### [[tagir-analyzes|Контакт: tagiranalyzes / Legal RAG]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 246_

### [[vitalyoborin|Контакт: VitalyOborin / Yodoca]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 285_

### [[vitalysemenov|Контакт: VitaliySemenov / agent-memory-mcp]]
> > Автор agent-memory-mcp (типизированная память для MCP + Memory OS с bi-temporal фактами).

  - Профиль
  - Проект: agent-memory-mcp
  - Вопросы для первого контакта
  - Шаблон первого сообщения
  - История контактов

_Слов: 295_

### [[vladspace|Контакт: VladSpace / Graph RAG]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 262_

### [[zodigancode|Контакт: zodigancode / Rufler]]
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 255_

**Итого в секции: 4,043 слов, 16 файлов**


## Glossary

_Путь: `docs/glossary/`_

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


_Слов: 665_

**Итого в секции: 2,300 слов, 4 файлов**


## Habr Unique Projects

_Путь: `docs/habr-unique-projects/`_

### [[README|habr-unique-projects/ — поиск уникальных проектов на Хабре]]
> Файлы в корне репозитория:

  - Источник
  - Подпапки
  - Главная мысль диалога

_Слов: 234_

### [[01-three-direct-analogues|Три прямых аналога Svyazi: K2-18, Wikontic, NGT Memory]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 419_

### [[02-related-projects|Смежные проекты]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 370_

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


_Слов: 329_

### [[4-skill-catalogs-subagents|Пара 4 — Скилл-каталоги × Subagent-оркестрация]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 300_

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


_Слов: 345_

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


_Слов: 189_

### [[3-discovery-research|Ансамбль 3 — «Discovery-engine для научной работы»]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 133_

### [[4-summary-authors|Сводный список авторов и потенциальных соавторов]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 253_

### [[README|final-ensembles]]
> Файлов: 4

  - Содержание

_Слов: 30_

### [[1-neuromorphic-ssm|Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 324_

### [[2-tsu-mome|Пара 2 — Термодинамические TSU × MoE/MoME-роутинг]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 297_

### [[3-zinc-hybrid-arch|Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 285_

### [[4-riscv-privacy|Пара 4 — RISC-V × privacy-by-design община]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 294_

### [[5-tinyml-mcp-skills|Пара 5 — TinyML/Edge AI × MCP + skills]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 268_

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


_Слов: 270_

### [[02-memnet|MemNet — нейроархитектурный двойник «магии» Svyazi]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 227_

### [[03-pda-llm-as-periphery|PDA-бот — «LLM как периферия»]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 251_

### [[04-dochkina-sequential|Виктория Дочкина — Sequential‑протокол распределённых агентов]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 284_

### [[05-supplementary-infrastructure|Источник данных и инфраструктурные кусочки]]
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 306_

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

**Итого в секции: 13,445 слов, 56 файлов**


## Lorenzo Agent

_Путь: `docs/lorenzo-agent/`_

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
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
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


## Meta Scripting

_Путь: `docs/meta-scripting/`_

### [[01-concept|Метаскриптинг — Часть 1: Концепция]]
> > > Скрипты, которые читают другие скрипты и документы — и улучшают их.

  - Как это называется
  - Зачем это нужно
  - Три кита: Чтение → Понимание → Действие
  - Граница: что скрипт может делать сам, что — только с LLM
  - Следующие части

_Слов: 439_

### [[02-architecture|Метаскриптинг — Часть 2: Архитектура]]
> > !WARNING

  - Содержание
  - Ключевой инструмент: AST
  - Что можно извлечь из скрипта через AST
  - Четыре режима метаскрипта
  - Структура данных: ScriptCatalog
  - Паттерн «читаю → понимаю → улучшаю»
  - Безопасность: метаскрипт не меняет чужой код без --apply

_Слов: 614_

### [[03-catalog|Метаскриптинг — Часть 3: Автокаталог скриптов]]
> > > Скрипт читает все 155 скриптов и строит живой каталог.

  - Что такое автокаталог
  - Что извлекается из каждого скрипта
  - Алгоритм определения риска
  - Пример выходного каталога (фрагмент)
  - Что каталог даёт на практике
- Какие скрипты пишут в docs/HEALTH.md?
- Какие скрипты без dry-run?
- Какие скрипты нет в группах runall?

_Слов: 412_

### [[04-enrichment|Метаскриптинг — Часть 4: Обогащение скриптов]]
> > > Как скрипт улучшает другой скрипт, не зная заранее что в нём написано.

  - Содержание
  - Что значит «обогатить скрипт»
  - Пять уровней обогащения
- Сгенерированный docstring без LLM:
- Было:
- Стало:
  - Алгоритм обогащения (пошагово)
  - Пример: было → стало

_Слов: 582_

### [[05-synthesis|Метаскриптинг — Часть 5: Синтез новых скриптов]]
> > > Как из существующих паттернов порождать новые скрипты.

  - Откуда берутся паттерны
  - Шесть базовых паттернов
  - Три способа синтеза
  - Защита от плохого кода
  - Петля самообогащения (осторожно)

_Слов: 503_

### [[QA|Q&A: meta-scripting]]
> Автоматически сгенерировано по 5 файлам раздела.

  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  - Как организован бюджетный роутинг между моделями?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?

_Слов: 71_

### [[README|meta-scripting]]
> Файлов: 6

  - Содержание

_Слов: 45_

**Итого в секции: 2,666 слов, 7 файлов**


## Nautilus

_Путь: `docs/nautilus/`_

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

_Слов: 234_

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

**Итого в секции: 148,539 слов, 255 файлов**


## Processing Guide

_Путь: `docs/processing-guide/`_

### [[01-overview|Обработка больших массивов информации — Часть 1: Обзор и таксономия]]
> > > Руководство по всем доступным методам обработки разрозненных документов в проекте Lorenzo / Svyazi 2.0.

  - Проблема
  - Таксономия методов
  - Что реализовано в Lorenzo
  - Навигация по разделам

_Слов: 462_

### [[02-extraction|Обработка больших массивов — Часть 2: Извлечение]]
> > !WARNING

  - Содержание
  - Проблема формата
  - Уровень 1: extractmhtml.py
  - Уровень 2: organizedocs.py + part.py
  - Поддерживаемые форматы
  - Качество извлечения
  - Типичные проблемы и решения
  - Следующий шаг после извлечения

_Слов: 622_

### [[03-chunking|Обработка больших массивов — Часть 3: Разбивка и чанкинг]]
> > !WARNING

  - Содержание
  - Зачем делить?
  - Стратегии разбивки
- utilschunker.py — chunkbyheaders()
- improvechunksemantic.py
- improvepassageretrieval.py
- improvereclassify.py
- improvetopicmodel.py
  _... ещё 6 разделов_

_Слов: 664_

### [[04-structuring|Обработка больших массивов — Часть 4: Структурирование]]
> > !TIP

  - Содержание
  - Проблема неструктурированности
  - Инструмент 1: Автоматические метаданные — improveautofill.py
  - Статус
  - Инструмент 2: Оглавления — improveautotoc.py
  - Содержание
  - Инструмент 3: Теги — improvetags.py
  - Инструмент 4: Перекрёстные ссылки — improvecrosslinkall.py
  _... ещё 14 разделов_

_Слов: 716_

### [[05-analysis|Обработка больших массивов — Часть 5: Анализ и NLP]]
> > > Что можно узнать о массиве документов без использования LLM.

  - Содержание
  - Что такое «анализ без LLM»
  - Группа 1: Извлечение сущностей
- MHTML → "MIME HTML archive format"
- BM25  → "Best Match 25, алгоритм ранжирования"
- RAG   → "Retrieval-Augmented Generation"
  - Группа 2: Граф знаний
- Вывод: docs/network.dot (Graphviz), docs/NETWORK.md
  _... ещё 7 разделов_

_Слов: 882_

### [[06-search|Обработка больших массивов — Часть 6: Поиск]]
> > !IMPORTANT

  - Содержание
  - Уровни поиска (от простого к сложному)
  - Уровень 2: Поисковый индекс — improvesearchindex.py
  - Уровень 3: BM25 — improvekeywordindex.py
  - Уровень 4: Поиск по абзацам — improvepassageretrieval.py
  - Уровень 5: Фасетный поиск — improvefacetedsearch.py
- Поиск по тексту в конкретной секции
- Поиск файлов с конкретной сущностью
  _... ещё 12 разделов_

_Слов: 965_

### [[07-llm|Обработка больших массивов — Часть 7: LLM-обогащение]]
> > > Что может сделать языковая модель с документами, чего не может классический алгоритм.

  - Содержание
  - Граница классики и LLM
  - Архитектура: 5 LLM-скриптов
  - improvellmenrich.py — обогащение файлов
  - improvellmqa.py — Q&A по базе знаний
  - improvellmsummary.py — каскадная суммаризация
  - improvellmgaps.py — пробелы в документации
- → docs/LLMGAPS.md
  _... ещё 6 разделов_

_Слов: 855_

### [[08-export|Обработка больших массивов — Часть 8: Экспорт и интеграции]]
> > > Куда отправить обработанную базу знаний: форматы, платформы, пайплайны.

  - Содержание
  - Зачем экспортировать?
  - Obsidian Vault — improveobsidian.py
- → docs/obsidian/ (1053 файла готовы к открытию в Obsidian)
  - Confluence — improveconfluence.py
- → docs/confluence//.wiki
  - EPUB — improveepub.py
  - RSS/Atom — improverss.py
  _... ещё 16 разделов_

_Слов: 720_

### [[09-automation|Обработка больших массивов — Часть 9: Автоматизация]]
> > !WARNING

  - Содержание
  - Проблема ручного запуска
  - Ступень 1: Оркестратор — improverunall.py
- Запустить всё
- Только быстрые скрипты (< 5 сек каждый)
- Умный режим: пропустить если метрика уже хорошая
- Только конкретная группа
- Только изменённые файлы (git diff)
  _... ещё 15 разделов_

_Слов: 886_

### [[10-future|Обработка больших массивов — Часть 10: Инновационные подходы]]
> > > Что можно сделать сегодня с новыми инструментами — и что ещё не придумано.

  - Содержание
  - Граница между «уже есть» и «ещё нет»
  - Уровень A: Векторный поиск (следующий шаг)
- Шаг 1: Индексация (один раз)
- Сохранить индекс
- Шаг 2: Поиск
- Reciprocal Rank Fusion — объединяет оба ранжирования
  - Уровень B: Граф знаний с LLM-NER
  _... ещё 31 разделов_

_Слов: 1756_

### [[PROCESSING_GUIDE|Обработка больших массивов документов — Полное руководство]]
> > !TIP

  - Содержание
  - Содержание
  - Обработка больших массивов информации — Часть 1: Обзор и таксономия
  - Проблема
  - Таксономия методов
  - Что реализовано в Lorenzo
  - Навигация по разделам
  - Обработка больших массивов — Часть 2: Извлечение
  _... ещё 178 разделов_

_Слов: 8049_

### [[QA|Q&A: processing-guide]]
> Автоматически сгенерировано по 11 файлам раздела.

  - Какие системы памяти описаны в этом разделе?
  - Как происходит консолидация и забывание в памяти агентов?
  - Какова разница между эпизодической и семантической памятью?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  _... ещё 10 разделов_

_Слов: 219_

### [[README|processing-guide]]
> Файлов: 12

  - Содержание

_Слов: 103_

**Итого в секции: 16,899 слов, 13 файлов**


## Svyazi 2 0

_Путь: `docs/svyazi-2-0/`_

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

_Слов: 200_

### [[evidence-envelope|Evidence Envelope]]
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля
  - Особые случаи

_Слов: 238_

### [[gaps|Архитектурные зазоры]]
> > !TIP

  - Содержание
  - Пять зазоров, важнее поиска ещё десяти инструментов
  - Сводная таблица зазоров
  - Главный практический принцип

_Слов: 597_

### [[integration-spec|Интеграционная спецификация (минимум для MVP)]]
> > !TIP


_Слов: 285_

### [[memory-write-policy|Memory Write Policy]]
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 186_

### [[review-record|Review Record]]
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 121_

### [[skill-tool-policy|Skill and Tool Policy]]
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 183_

### [[README|components]]
> Файлов: 19

  - Содержание

_Слов: 120_

### [[agent-memory-mcp|agent-memory-mcp + Memory OS]]
> > - Автор: VitaliySemenov / moshael

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 166_

### [[agentfs]]
> > - Источник: Хабр + GitHub citeturn33view4turn33view7turn27view0

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 125_

### [[ai-factory|AI Factory + AIF Handoff]]
> > - Источник: Хабр + GitHub citeturn20view3turn29search0turn29search9

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 130_

### [[autoresearch-sequential|AutoResearch + Sequential]]
> > - Авторы: Андрей Карпаты / Виктория Дочкина

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 140_

### [[graph-rag|Graph RAG]]
> > - Автор: VladSpace / vpakspace

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 125_

### [[hybrid-rag|Hybrid RAG knowledge base]]
> > - Источник: Хабр citeturn34view2

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 118_

### [[knowledge-space]]
> > - Автор: SoniaBlack / AnastasiyaW

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 123_

### [[legal-rag|Legal RAG]]
> > - Источник: Хабр citeturn20view6

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 123_

### [[mclaude]]
> > - Источник: Хабр + GitHub citeturn20view2turn37search0

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 114_

### [[memnet|MemNet / memory-is-all-you-need]]
> > - Источник: Хабр + GitHub citeturn21view4turn17search0turn18search2

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 117_

### [[ngt-memory|NGT Memory]]
> > - Автор: spbmolot / ngt-memory

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 138_

### [[research-docs-liteparse|research-docs + LiteParse]]
> > - Автор: nlaik / Jerry Liu / LlamaIndex

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 137_

### [[rufler]]
> > - Автор: zodigancode / lib4u

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 114_

### [[security-routing-plane|Security + routing plane]]
> > - Авторы: Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig

  - Описание
  - Ключевые компоненты и паттерны
  - Числовые наблюдения

_Слов: 210_

### [[self-aware-mcp|Self‑Aware MCP + Skills + CodeWiki]]
> > - Авторы: akazant / akzhankalimatov / AnastasiyaW

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 148_

### [[svyazi]]
> > - Источник: Хабр citeturn41search0

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 134_

### [[voice-stack|Voice / local-first stack]]
> > - Авторы: atatchin / askid / обзоры Handy / OpenWhispr

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 152_

### [[yjs-automerge|Yjs + Automerge]]
> > - Авторы: Kevin Jahns / Automerge team

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 125_

### [[yodoca]]
> > - Источник: Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 127_

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

_Слов: 284_

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


_Слов: 1301_

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


_Слов: 365_

### [[privacy|Приватность: local-first by default]]
> > !WARNING


_Слов: 124_

**Итого в секции: 12,925 слов, 59 файлов**


## Technology Combinations

_Путь: `docs/technology-combinations/`_

### [[README|technology-combinations/ — комбинирование технологий для новых свойств]]
> Файл в корне репозитория: Комбинирование технологий для новых свойств - Claude(../../%D0%9A%D0%BE%D0%BC%D0%B1%D0%B8%D0%B…

  - Источник
  - Подпапки
  - Главная находка диалога
  - См. также

_Слов: 155_

### [[01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern|Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 246_

### [[02-multiagentnyy-khaos-reshenie-auto-ai-router|Комбинация 2: Мультиагентный хаос-решение × Auto AI Router]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 187_

### [[03-crdt-local-first-svyazi-cardindex|Комбинация 3: CRDT local-first × Svyazi CardIndex]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 199_

### [[04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura|Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 218_

### [[05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy|Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 212_

### [[06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-|Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 218_

### [[07-crawl4ai-docling-yodoca-consolidator|Комбинация 7: Crawl4AI × Docling × Yodoca consolidator]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 199_

### [[08-conductor-adversarial-review-auto-ai-router|Комбинация 8: Conductor × adversarial-review × Auto AI Router]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 686_

### [[09-agent-orchestration-stack|Комбинация 9: Agent Orchestration Stack]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 196_

### [[10-legal-document-intelligence-pipeline|Комбинация 10: Legal Document Intelligence Pipeline]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 200_

### [[11-hybrid-crdt-sql-database|Комбинация 11: Hybrid CRDT-SQL Database]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 189_

### [[12-multi-agent-observability-stack|Комбинация 12: Multi-Agent Observability Stack]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 165_

### [[13-legal-document-transpiler|Комбинация 13: Legal Document Transpiler]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 180_

### [[14-local-first-agent-development-environment|Комбинация 14: local-first Agent Development Environment]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 577_

### [[15-self-consolidating-legal-corpus|Комбинация 15: Self-Consolidating Legal Corpus]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 226_

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

_Слов: 228_

### [[19-multi-agent-observability-platform|Комбинация 19: Multi-Agent Observability Platform]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 678_

### [[20-hybrid-olap-oltp-with-real-time-sync|Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 256_

### [[21-legal-corpus-analytics-at-scale|Комбинация 21: Legal Corpus Analytics at Scale]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Pipeline
- Schema
- Analytics queries (subsecond)

_Слов: 249_

### [[22-russian-international-oss-stack|Комбинация 22: Russian-International OSS Stack]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 213_

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

_Слов: 252_

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


_Слов: 220_

### [[28-pydantic-enforced-legal-workflows|Комбинация 28: Pydantic-Enforced Legal Workflows]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Sequential pipeline with Pydantic validation at each stage

_Слов: 225_

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


_Слов: 245_

### [[32-consensus-based-multi-agent-coordination|Комбинация 32: Consensus-Based Multi-Agent Coordination]]
> > !TIP


_Слов: 260_

### [[33-event-sourcing-cqrs-clickhouse-analytics|Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 221_

### [[34-distributed-event-store-with-paxos|Комбинация 34: Distributed Event Store with Paxos]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 193_

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

_Слов: 227_

### [[02-ultimate-legal-ai|Mega‑Stack 2.0 — Ultimate Legal‑AI System]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «MEGA‑STACK 2.0: Ultimate Legal‑…

  - Capabilities
  - First implementation priority

_Слов: 318_

### [[03-dsl-ast|Mega‑Stack 3.0 — with DSL & AST]]
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «КОМБИНАЦИЯ 30: MEGA‑STACK 3.0 w…

  - New capabilities

_Слов: 242_

### [[04-event-sourcing-consensus|Mega‑Stack 4.0 — with Event Sourcing & Consensus]]
> > !TIP

  - New capabilities
  - Performance

_Слов: 329_

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

_Слов: 401_

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

**Итого в секции: 13,381 слов, 53 файлов**


## Templates

_Путь: `docs/templates/`_

### [[README|Шаблоны документов]]
> Создано: 2026-05-10

  - Доступные шаблоны
  - Использование
- Скопируйте нужный шаблон в нужную папку
- Затем откройте и заполните поля в [квадратных скобках]

_Слов: 82_

### [Спецификация агента: [Название]](templates/agent-spec.md)
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

### [Контакт: [Имя / Проект]](templates/contact-outreach.md)
>  Параметр  Значение 

  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы для обсуждения

_Слов: 119_

### [Противоречие: [Название]](templates/contradiction-record.md)
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

### [ADR: [Название решения]](templates/decision-record.md)
> Предложено / Принято / Отклонено / Устарело

  - Статус
  - Контекст
  - Рассмотренные варианты
  - Принятое решение
  - Последствия

_Слов: 84_

### [Ансамбль: [Название]](templates/ensemble.md)
> Какую задачу решает ансамбль. Почему именно эта комбинация компонентов.

  - Назначение
  - Компоненты
  - Архитектурная схема
  - Контракт взаимодействия
  - Риски и ограничения
  - MVP-шаги

_Слов: 112_

### [Эксперимент: [Название]](templates/experiment-log.md)
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

### [FAQ: [Вопрос]](templates/faq-entry.md)
> > Точная формулировка вопроса

  - Вопрос
  - Краткий ответ
  - Подробный ответ
  - Когда это НЕ применимо
  - Связанные вопросы
  - Источники / документы
  - История обновлений

_Слов: 132_

### [[Термин]](templates/glossary-entry.md)
> Полное определение в 2-3 предложениях.

  - Определение
  - Происхождение
  - Синонимы и аббревиатуры
  - Примеры
  - Связанные термины
  - Где упоминается в монорепо
  - Источники

_Слов: 117_

### [KPI Snapshot: [дата]](templates/kpi-snapshot.md)
> Дата снапшота: 2026-04-29

  - Период
  - Сводка
  - Детальные метрики
  - Лучшие изменения
  - Регрессии
  - Топ-3 фокуса на следующий период

_Слов: 220_

### [Юридический кейс: [Aktenzeichen]](templates/legal-case.md)
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

### [Встреча: [Тема]](templates/meeting-notes.md)
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

### [Mega-stack: [Название]](templates/mega-stack.md)
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

### [[Название компонента]](templates/project-component.md)
> Описание проекта в 2-3 предложениях. Какую задачу решает.

  - Что это
  - Ключевые особенности
  - Статус
  - Интеграция с Svyazi
  - Контакты

_Слов: 102_

### [[Название протокола]](templates/protocol-spec.md)
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

### [MVP: [Название]](templates/prototype-mvp.md)
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

_Слов: 384_

### [[Тема исследования]](templates/research-note.md)
> Зачем изучали. Какой вопрос стоял.

  - Контекст
  - Ключевые находки
  - Источники
  - Открытые вопросы
  - Следующие шаги

_Слов: 66_

### [Ретроспектива: [период]](templates/retrospective.md)
> С: 2026-04-22

  - Период
  - Что прошло хорошо ✅
  - Что прошло плохо ❌
  - Что узнали 💡
  - Action items для следующего периода
  - Метрики периода
  - Улучшения процесса

_Слов: 160_

### [RFC NNNN: [Название]](templates/rfc.md)
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

_Слов: 241_

### [Риск: [Название]](templates/risk-entry.md)
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

### [Tech Pair: [A] × [B]](templates/tech-pair.md)
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

### [Tech Radar: [Название]](templates/tech-radar-entry.md)
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

### [[имя нового шаблона]](templates/template-of-templates.md)
> Это мета-шаблон для создания новых шаблонов в docs/templates/.

  - Что делать
  - Обязательные блоки шаблона
- [Заголовок]
  - Обязательные поля JSON-Schema
  - Чеклист добавления нового шаблона
  - Типичные паттерны

_Слов: 319_

### [Еженедельный дайджест: [период]](templates/weekly-digest.md)
> 3-5 пунктов главного за неделю.

  - TL;DR
  - Что сделано
  - Метрики недели
  - Решения
  - Открытые вопросы недели
  - План на следующую неделю
  - Заметки

_Слов: 193_

**Итого в секции: 4,890 слов, 24 файлов**


## 🗺️ Тематическая карта

### Архитектура (569 документов)
- [[365-развёрнутый-анализ-внуковой-комбинации|`365-развёрнутый-анализ-внуковой-комбинации`]]
- [[CONCEPTS|`CONCEPTS`]]
- [[TABLES|`TABLES`]]
- [[00-intro|`00-intro`]]
- [[01-интегральный-анализ-профиля-svend4|`01-интегральный-анализ-профиля-svend4`]]
- _... ещё 564_

### Документация (142 документов)
- [[CODE_BLOCKS|`CODE_BLOCKS`]]
- [[118-appendix-a-шаблон-для-header-warning|`118-appendix-a-шаблон-для-header-warning`]]
- [[98-appendix-a-minimal-working-example|`98-appendix-a-minimal-working-example`]]
- [[COMPLEXITY|`COMPLEXITY`]]
- [[22-glossary|`22-glossary`]]
- _... ещё 137_

### Агенты (135 документов)
- [[C-multi-agent-factory|`C-multi-agent-factory`]]
- [[107-1-контекст-и-мотивация|`107-1-контекст-и-мотивация`]]
- [[108-2-формальный-workflow|`108-2-формальный-workflow`]]
- [[345-кто-ты|`345-кто-ты`]]
- [[00-question-what-is-hermes|`00-question-what-is-hermes`]]
- _... ещё 130_

### Проекты (132 документов)
- [[DUPLICATES|`DUPLICATES`]]
- [[02-общий-план-развития-nautilus-portal-protocol|`02-общий-план-развития-nautilus-portal-protocol`]]
- [[228-appendix-c-quick-start-architecture-for-sgb-advoca|`228-appendix-c-quick-start-architecture-for-sgb-advoca`]]
- [[299-практические-рекомендации-для-текущего-проекта|`299-практические-рекомендации-для-текущего-проекта`]]
- [[336-10-стратегическое-позиционирование|`336-10-стратегическое-позиционирование`]]
- _... ещё 127_

### Контакты (61 документов)
- `[[rufler|rufler`]]
- `[[ngt-memory|ngt-memory`]]
- [[REGISTRY|`REGISTRY`]]
- [[06-1-introduction|`06-1-introduction`]]
- [[105-review-methodology-md|`105-review-methodology-md`]]
- _... ещё 56_

### Память (46 документов)
- [[PROCESSING_GUIDE|`PROCESSING_GUIDE`]]
- [[SCRIPT_EVAL_REPORT|`SCRIPT_EVAL_REPORT`]]
- [[06-search|`06-search`]]
- [[11-integration-contracts|`11-integration-contracts`]]
- [[CHANGELOG|`CHANGELOG`]]
- _... ещё 41_

### Код (35 документов)
- [[DEPENDENCY_MAP|`DEPENDENCY_MAP`]]
- [[02-architecture|`02-architecture`]]
- [[04-enrichment|`04-enrichment`]]
- [[83-8-q6-space-normative|`83-8-q6-space-normative`]]
- [[84-9-consensus-algorithm|`84-9-consensus-algorithm`]]
- _... ещё 30_

### Анализ (31 документов)
- [[72-расписание-фазы-3|`72-расписание-фазы-3`]]
- [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|`110-вопрос-fallback-ratio-как-критический-или-осмыслен`]]
- [[145-8-call-to-action|`145-8-call-to-action`]]
- [[154-table-of-contents|`154-table-of-contents`]]
- [[162-8-risk-analysis|`162-8-risk-analysis`]]
- _... ещё 26_


<!-- see-also -->

---

## Смотрите также
- [[PARAGRAPH_QUALITY]]
- [[TABLES]]
- [[HEADING_AUDIT]]
- [[QUESTIONS]]


<!-- backlinks -->

---

**Кто ссылается на этот документ (3):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)

