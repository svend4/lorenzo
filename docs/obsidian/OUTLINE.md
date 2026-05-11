---
title: "Outline базы знаний"
tags:
  - outline
  - docs
  - general
date: 2026-05-11
---

# Outline базы знаний

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
  - [[QUESTIONS|[Открытые вопросы]]](#открытые-вопросыquestionsmd)
  - [[READING_LIST|[Список чтения]]](#список-чтенияreading_listmd)
  - [[READING_ORDER|[Рекомендуемый порядок чтения]]](#рекомендуемый-порядок-чтенияreading_ordermd)
  - [[README|[docs]]](#docsreadmemd)
  - [[REGISTRY|[REGISTRY — реестр артефактов Lorenzo]]](#registry-реестр-артефактов-lorenzoregistrymd)
  - [[REPORT|[Svyazi 2.0 — Knowledge Base Report]]](#svyazi-20-knowledge-base-reportreportmd)
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
  - [[Продолжение исследования для Svyazi[^svyazi] 2.0](01-svyazi/00-intro-part2.md)](#продолжение-исследования-для-svyazisvyazi-2001-svyazi00-intro-part2md)
  - [[Svyazi[^svyazi] 2.0 — Исполнительное резюме](01-svyazi/01-executive-summary.md)](#svyazisvyazi-20-исполнительное-резюме01-svyazi01-executive-summarymd)
  - [[02-methodology|[Методика и рамка отбора проектов]]](#методика-и-рамка-отбора-проектов01-svyazi02-methodologymd)
  - [[03-component-catalog|[Каталог компонентов Svyazi 2.0]]](#каталог-компонентов-svyazi-2001-svyazi03-component-catalogmd)
  - [[04-ensembles-overview|[Приоритетные ансамбли проектов]]](#приоритетные-ансамбли-проектов01-svyazi04-ensembles-overviewmd)
  - [[06-security-privacy|[Безопасность и приватность]]](#безопасность-и-приватность01-svyazi06-security-privacymd)
  - [[07-mvp-planning|[Планирование MVP]]](#планирование-mvp01-svyazi07-mvp-planningmd)
  - [[08-conclusions|[Выводы]]](#выводы01-svyazi08-conclusionsmd)
  - [[09-architectural-gaps|[Архитектурные зазоры]]](#архитектурные-зазоры01-svyazi09-architectural-gapsmd)
  - [[10-second-order-ensembles|[Ансамбли следующего шага]]](#ансамбли-следующего-шага01-svyazi10-second-order-ensemblesmd)
  - [[11-integration-contracts|[Интеграционные контракты]]](#интеграционные-контракты01-svyazi11-integration-contractsmd)
  - [[12-roadmap|[Дорожная карта прототипа]]](#дорожная-карта-прототипа01-svyazi12-roadmapmd)
  - [[13-contacts|[Контактная стратегия]]](#контактная-стратегия01-svyazi13-contactsmd)
  - [[14-limitations|[Ограничения и лицензии]]](#ограничения-и-лицензии01-svyazi14-limitationsmd)
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
  - [[19-7-portalentry-structure|[7. PortalEntry Structure]]](#7-portalentry-structure02-anthropic-vacancies19-7-portalentry-structuremd)
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
  - [[22-10-queryresult-structure|[10. QueryResult Structure]]](#10-queryresult-structure02-anthropic-vacancies22-10-queryresult-structuremd)
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
  - [[82-7-portalentry-structure|[7. PortalEntry Structure]]](#7-portalentry-structure02-anthropic-vacancies82-7-portalentry-structuremd)
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
  - [[QA|[Q&A: 02-anthropic-vacancies]]](#qa-02-anthropic-vacancies02-anthropic-vacanciesqamd)
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
  - [[QA|[Q&A: ai-collaborations]]](#qa-ai-collaborationsai-collaborationsqamd)
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
  - [[QA|[Q&A: anthropic-vacancies]]](#qa-anthropic-vacanciesanthropic-vacanciesqamd)
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
  - [[00-question-two-nautiluses|[Вопрос: два Наутилуса в репозиториях svend4 (pro2 vs nautilus)]]](#вопрос-два-наутилуса-в-репозиториях-svend4-pro2-vs-nautilusanthropic-vacanciesnautilus-pro2-analysis00-question-two-nautilusesmd)
  - [[01-shell-metaphor-two-projections|[Раковина наутилуса как scale invariance — две проекции одной метафоры]]](#раковина-наутилуса-как-scale-invariance-две-проекции-одной-метафорыanthropic-vacanciesnautilus-pro2-analysis01-shell-metaphor-two-projectionsmd)
  - [[02-nautilus-A-pro2-meta|[Наутилус A: pro2 + meta — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети)]]](#наутилус-a-pro2-meta-yijing-transformer-nautilusmome-внутренняя-архитектура-нейросетиanthropic-vacanciesnautilus-pro2-analysis02-nautilus-a-pro2-metamd)
  - [[03-nautilus-B-meta-orchestrator|[Наутилус B: nautilus — мета-оркестратор репозиториев (внешняя архитектура)]]](#наутилус-b-nautilus-мета-оркестратор-репозиториев-внешняя-архитектураanthropic-vacanciesnautilus-pro2-analysis03-nautilus-b-meta-orchestratormd)
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
  - [[README|[profile-mapping/ — маппинг профиля svend4 на роли Anthropic]]](#profile-mapping-маппинг-профиля-svend4-на-роли-anthropicanthropic-vacanciesprofile-mappingreadmemd)
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
  - [[QA|[Q&A: contacts]]](#qa-contactscontactsqamd)
  - [[README|[contacts]]](#contactscontactsreadmemd)
  - [[anastasiyaw|[Контакт: AnastasiyaW / knowledge-space, mclaude]]](#контакт-anastasiyaw-knowledge-space-mclaudecontactsanastasiyawmd)
  - [[andrey-chuyan|[Контакт: andreychuyan / Svyazi]]](#контакт-andreychuyan-svyazicontactsandrey-chuyanmd)
  - [[antipozitive|[Контакт: Antipozitive / MemNet]]](#контакт-antipozitive-memnetcontactsantipozitivemd)
  - [[cutcode|[Контакт: Cutcode / AIF Handoff]]](#контакт-cutcode-aif-handoffcontactscutcodemd)
  - [[dmitriila|[Контакт: Dmitriila / SENTINEL]]](#контакт-dmitriila-sentinelcontactsdmitriilamd)
  - [[kksudo|[Контакт: kksudo / AgentFS]]](#контакт-kksudo-agentfscontactskksudomd)
  - [[mixaill76|[Контакт: MiXaiLL76 / Auto AI Router]]](#контакт-mixaill76-auto-ai-routercontactsmixaill76md)
  - [[nlaik|[Контакт: nlaik / LiteParse / research-docs]]](#контакт-nlaik-liteparse-research-docscontactsnlaikmd)
  - [[sonia-black|[Контакт: SoniaBlack / knowledge-space]]](#контакт-soniablack-knowledge-spacecontactssonia-blackmd)
  - [[spbmolot|[Контакт: spbmolot / NGT Memory]]](#контакт-spbmolot-ngt-memorycontactsspbmolotmd)
  - [[tagir-analyzes|[Контакт: tagiranalyzes / Legal RAG]]](#контакт-tagiranalyzes-legal-ragcontactstagir-analyzesmd)
  - [[vitalyoborin|[Контакт: VitalyOborin / Yodoca]]](#контакт-vitalyoborin-yodocacontactsvitalyoborinmd)
  - [[vitalysemenov|[Контакт: VitaliySemenov / agent-memory-mcp]]](#контакт-vitaliysemenov-agent-memory-mcpcontactsvitalysemenovmd)
  - [[vladspace|[Контакт: VladSpace / Graph RAG]]](#контакт-vladspace-graph-ragcontactsvladspacemd)
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
  - [[6-tmux-village-openclaw|[Пара 6 — Деревня агентов через tmux × OpenClaw оркестратор]]](#пара-6-деревня-агентов-через-tmux-openclaw-оркестраторhabr-unique-projectsdeep-pairs6-tmux-village-openclawmd)
  - [[7-autoresearch-distributed|[Пара 7 — AutoResearch цикл × Распределённый рой]]](#пара-7-autoresearch-цикл-распределённый-ройhabr-unique-projectsdeep-pairs7-autoresearch-distributedmd)
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
  - [[2-autoresearch-legal|[Ансамбль 2 — «AutoResearch для legal precedent mining»]]](#ансамбль-2-autoresearch-для-legal-precedent-mininghabr-unique-projectsfinal-ensembles2-autoresearch-legalmd)
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
  - [[QA|[Q&A: lorenzo-agent]]](#qa-lorenzo-agentlorenzo-agentqamd)
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
  - [[03-registry|[3. Registry (nautilus.json)]]](#3-registry-nautilusjsonnautilusnpp-v1-003-registrymd)
  - [[04-passport|[4. Passport (passport.md)]]](#4-passport-passportmdnautilusnpp-v1-004-passportmd)
  - [[05-compatibility-levels|[5. Compatibility Levels]]](#5-compatibility-levelsnautilusnpp-v1-005-compatibility-levelsmd)
  - [[06-adapter-interface|[6. Adapter Interface]]](#6-adapter-interfacenautilusnpp-v1-006-adapter-interfacemd)
  - [[07-portal-entry|[7. PortalEntry Structure]]](#7-portalentry-structurenautilusnpp-v1-007-portal-entrymd)
  - [[08-consensus-algorithm|[8. Consensus Algorithm (v1.0: string normalization)]]](#8-consensus-algorithm-v10-string-normalizationnautilusnpp-v1-008-consensus-algorithmmd)
  - [[09-query-flow|[9. Query Flow]]](#9-query-flownautilusnpp-v1-009-query-flowmd)
  - [[10-query-result|[10. QueryResult Structure]]](#10-queryresult-structurenautilusnpp-v1-010-query-resultmd)
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
  - [[03-registry|[3. Registry (nautilus.json)]]](#3-registry-nautilusjsonnautilusnpp-v1-103-registrymd)
  - [[04-passport|[4. Passport (passport.md)]]](#4-passport-passportmdnautilusnpp-v1-104-passportmd)
  - [[05-compatibility-levels|[5. Compatibility Levels]]](#5-compatibility-levelsnautilusnpp-v1-105-compatibility-levelsmd)
  - [[06-adapter-interface|[6. Adapter Interface]]](#6-adapter-interfacenautilusnpp-v1-106-adapter-interfacemd)
  - [[07-portal-entry|[7. PortalEntry Structure]]](#7-portalentry-structurenautilusnpp-v1-107-portal-entrymd)
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
  - [[QA|[Q&A: svyazi-2-0]]](#qa-svyazi-2-0svyazi-2-0qamd)
  - [[README|[svyazi-2-0]]](#svyazi-2-0svyazi-2-0readmemd)
  - [[README|[architecture]]](#architecturesvyazi-2-0architecturereadmemd)
  - [[card-envelope|[Card Envelope]]](#card-envelopesvyazi-2-0architecturecard-envelopemd)
  - [[evidence-envelope|[Evidence Envelope]]](#evidence-envelopesvyazi-2-0architectureevidence-envelopemd)
  - [[gaps|[Архитектурные зазоры]]](#архитектурные-зазорыsvyazi-2-0architecturegapsmd)
  - [[integration-spec|[Интеграционная спецификация (минимум для MVP)]]](#интеграционная-спецификация-минимум-для-mvpsvyazi-2-0architectureintegration-specmd)
  - [[memory-write-policy|[Memory Write Policy]]](#memory-write-policysvyazi-2-0architecturememory-write-policymd)
  - [[review-record|[Review Record]]](#review-recordsvyazi-2-0architecturereview-recordmd)
  - [[skill-tool-policy|[Skill and Tool Policy]]](#skill-and-tool-policysvyazi-2-0architectureskill-tool-policymd)
  - [[README|[components]]](#componentssvyazi-2-0componentsreadmemd)
  - [[agent-memory-mcp|[agent-memory-mcp + Memory OS]]](#agent-memory-mcp-memory-ossvyazi-2-0componentsagent-memory-mcpmd)
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
  - [[05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy|[Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной]]](#комбинация-5-sourcecraft-cli-claude-code-sequential-протокол-дочкинойtechnology-combinationscombinations05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoymd)
  - [[06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-|[Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер]]](#комбинация-6-openclaude-утёкший-claude-code-zinc-inference-engine-mome-роутерtechnology-combinationscombinations06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-md)
  - [[07-crawl4ai-docling-yodoca-consolidator|[Комбинация 7: Crawl4AI × Docling × Yodoca consolidator]]](#комбинация-7-crawl4ai-docling-yodoca-consolidatortechnology-combinationscombinations07-crawl4ai-docling-yodoca-consolidatormd)
  - [[08-conductor-adversarial-review-auto-ai-router|[Комбинация 8: Conductor × adversarial-review × Auto AI Router]]](#комбинация-8-conductor-adversarial-review-auto-ai-routertechnology-combinationscombinations08-conductor-adversarial-review-auto-ai-routermd)
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
  - [Архитектура (537 документов)](#архитектура-537-документов)
  - [Документация (172 документов)](#документация-172-документов)
  - [Проекты (134 документов)](#проекты-134-документов)
  - [Код (132 документов)](#код-132-документов)
  - [Агенты (120 документов)](#агенты-120-документов)
  - [Контакты (56 документов)](#контакты-56-документов)
  - [Память (39 документов)](#память-39-документов)
  - [Анализ (26 документов)](#анализ-26-документов)
- [Использование](#использование)

---


> [!NOTE]
> Раздел `OUTLINE` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: outline, docs -->


<!-- summary -->
> `OUTLINE` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-11_

Секций: **20** | Файлов: **1216**

## Содержание

- [Docs](#docs) — 96 файлов
- [Svyazi](#svyazi) — 16 файлов
- [Anthropic Vacancies](#anthropic-vacancies) — 357 файлов
- [Technology Combinations](#technology-combinations) — 7 файлов
- [Ai Collaborations](#ai-collaborations) — 17 файлов
- [Habr Projects](#habr-projects) — 16 файлов
- [Ai Collaborations](#ai-collaborations) — 31 файлов
- [Anthropic Vacancies](#anthropic-vacancies) — 111 файлов
- [Autofilled](#autofilled) — 13 файлов
- [Badges](#badges) — 1 файлов
- [Contacts](#contacts) — 17 файлов
- [Glossary](#glossary) — 4 файлов
- [Habr Unique Projects](#habr-unique-projects) — 56 файлов
- [Lorenzo Agent](#lorenzo-agent) — 62 файлов
- [Meta Scripting](#meta-scripting) — 7 файлов
- [Nautilus](#nautilus) — 255 файлов
- [Processing Guide](#processing-guide) — 13 файлов
- [Svyazi 2 0](#svyazi-2-0) — 60 файлов
- [Technology Combinations](#technology-combinations) — 53 файлов
- [Templates](#templates) — 24 файлов


## Docs

_Путь: `docs/`_

### [[ABBREVIATIONS|Словарь аббревиатур и сокращений]]
> > ABBREVIATIONS — раздел документации проекта Lorenzo.

  - Самые часто используемые
  - Использование
- Запуск

_Слов: 1884_

### [[ACTION_ITEMS|Action Items, риски и решения]]
> > ACTIONITEMS — раздел документации проекта Lorenzo.

  - ➡️ Следующие шаги (358)
  - ✅ Решения и рекомендации (1066)
  - ⚠️ Риски (1293)
  - 🚫 Ограничения (371)
  - 📋 Задачи (TODO) (44)
  - 📬 Контактные действия (311)
  - Использование
- Запуск
  _... ещё 5 разделов_

_Слов: 9661_

### [[ALERTS|Callout-блоки]]
> > ALERTS — раздел документации проекта Lorenzo.

  - Пример синтаксиса
  - Смотрите также

_Слов: 121_

### [[AUTHORS|Авторы и коллаборации]]
> > AUTHORS — раздел документации проекта Lorenzo.

  - Использование
- Запуск

_Слов: 219_

### [[AUTOFILLED|Автозаполненные шаблоны]]
> - Файлы(#файлы)

  - Contents
  - Файлы
  - Как работает
  - Связанные документы
  - Связанные документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 2 разделов_

_Слов: 302_

### [[BACKLINKS|Индекс обратных ссылок]]
> > BACKLINKS — раздел документации проекта Lorenzo.

  - Топ-30 самых цитируемых документов
  - Ссылки по разделам
  - Использование
- Запуск
  - Смотрите также

_Слов: 584_

### [[BADGES|Status Badges]]
> > Бейджи статуса репозитория: тесты, шаблоны, скрипты, скилы

  - Превью
  - Markdown сниппеты для README

_Слов: 111_

### [[CHANGELOG]]
> > !NOTE

  - semantic (1 коммитов)
  - md (1 коммитов)
  - 2026-05-11 (4 коммитов)
  - 2026-05-10 (58 коммитов)
  - 2026-04-29 (141 коммитов)
  - skip  (1 коммитов)
  - 22 скила  (1 коммитов)
  - $.STEP.ou (1 коммитов)
  _... ещё 5 разделов_

_Слов: 3350_

### [[CHANGELOG_AUTO|Changelog (авто)]]
> > !NOTE

  - Содержание
  - Статистика коммитов
  - История изменений
  - Использование
  - Смотрите также
  - Упоминается в
  - Связанные документы
  - Кто ссылается на этот документ (3)

_Слов: 703_

### [[CLUSTERS|Кластеры тематически близких файлов]]
> - Кластер 1 — turn, view, svyazi, cardindex (30 файлов)(#кластер-1-turn-view-svyazi-cardindex-30-файлов)

  - Contents
  - Кластер 1 — turn, view, svyazi, cardindex (30 файлов)
  - Кластер 2 — anthropic-vacancies, docs, ai-mediated-representation-for-underrepresented-ex, author-contact (23 файлов)
  - Кластер 3 — cowork, ingit, anthropic-vacancies, docs (22 файлов)
  - Кластер 4 — repo, passport, docs, str (17 файлов)
  - Кластер 5 — principal, agent, professional, agents (14 файлов)
  - Кластер 6 — github, documents, com, document (13 файлов)
  - Кластер 7 — профиль, связи, сообщение, первое (12 файлов)
  _... ещё 27 разделов_

_Слов: 2647_

### [[CODE_BLOCKS|Code-блоки репозитория]]
> > CODEBLOCKS — раздел документации проекта Lorenzo.

  - 📊 Диаграммы Mermaid (46)
- ... (обрезано)
- ... (обрезано)
- ... (обрезано)
  - 🐍 Python (198)
- ... (обрезано)
- ... (обрезано)
- ... (обрезано)
  _... ещё 75 разделов_

_Слов: 5404_

### [[COLLAB_SUGGESTIONS|Рекомендации по коллаборации (Collaboration Finder)]]
> > !NOTE

  - Содержание
  - 1. Wikontic: семантический граф
  - 2. Yodoca
  - 3. NGT[^ngt] Memory: ассоциативный граф
  - Следующие шаги
  - Смотрите также

_Слов: 716_

### [[COMPARE|Сравнение с предыдущим коммитом]]
> > !NOTE

  - Новые файлы (987)
  - Удалённые файлы (0)
  - Изменившиеся файлы (173) — топ по Δ слов
  - Использование
- Запуск
  - Смотрите также

_Слов: 529_

### [[COMPLEXITY|Оценка читаемости документов]]
> > COMPLEXITY — раздел документации проекта Lorenzo.

  - Распределение сложности
  - Самые сложные документы
  - Самые простые документы
  - Методология
  - Использование
- Запуск

_Слов: 631_

### [[COMPONENT_MATRIX|Матрица компонентов Svyazi 2.0]]
> > !TIP

  - Содержание
  - Матрица возможностей
  - Покрытие возможностей
  - Каталог компонентов
  - Рекомендуемые ансамбли
  - Связанные документы
  - Связанные документы
  - Использование
  _... ещё 4 разделов_

_Слов: 1051_

### [[CONCEPTS|Глоссарий понятий]]
> > CONCEPTS — раздел документации проекта Lorenzo.

  - A
  - B
  - C
  - D
  - E
  - F
  - G
  - H
  _... ещё 54 разделов_

_Слов: 14658_

### [[CONCEPT_GRAPH|Граф концептов базы знаний]]
> > CONCEPTGRAPH — раздел документации проекта Lorenzo.

  - Диаграмма
  - Топ концептов по связям

_Слов: 694_

### [[CONSISTENCY|Согласованность терминов]]
> > CONSISTENCY — раздел документации проекта Lorenzo.

  - Детали по файлам
  - Как исправить
- Пример: заменить все вхождения в docs/

_Слов: 694_

### [[CONTACTS|Контакты и авторы]]
> > !NOTE

  - Ключевые авторы проектов
  - GitHub репозитории
  - Email адреса
  - Шаблон первого сообщения
  - Смотрите также

_Слов: 596_

### [[CONTACT_PRIORITY|Приоритет контактов]]
> > !NOTE

  - Топ авторов по приоритету
  - Рекомендуемые следующие шаги
  - Формула расчёта балла

_Слов: 395_

### [[CONTRADICTIONS|Противоречия в базе знаний]]
> > CONTRADICTIONS — раздел документации проекта Lorenzo.

  - Найденные противоречия
  - Использование
- Запуск

_Слов: 1646_

### [[COST|Оценка стоимости MVP]]
> > !NOTE

  - Итого
  - По компонентам
  - По ролям
  - Сценарии
  - Временные оценки из документов
  - Допущения
  - Использование
- Запуск
  _... ещё 1 разделов_

_Слов: 572_

### [[CROSSREFS|Перекрёстные ссылки]]
> > CROSSREFS — раздел документации проекта Lorenzo.

  - Проекты → файлы
  - Файлы → проекты
  - Использование
- Запуск
  - Смотрите также

_Слов: 693_

### [[CROSS_SECTION|Кросс-секционный анализ]]
> > !NOTE

  - Содержание
  - Матрица сходства секций
  - Граф связей
  - Топ-40 кросс-секционных концептов
  - Детальная карта концептов
  - Смотрите также

_Слов: 1308_

### [[DECISIONS|Ключевые решения и выводы]]
> Автоматически извлечено из всех документов: 1274 записей

  - Архитектура (82)
  - Mvp (16)
  - Память (15)
  - Оркестрация (36)
  - Безопасность (4)
  - Лицензия (22)
  - Риски (6)
  - Контакты (48)
  _... ещё 3 разделов_

_Слов: 2471_

### [[DENSITY|Карта плотности тем]]
> > DENSITY — раздел документации проекта Lorenzo.

  - Наиболее раскрытые темы
  - Слабо раскрытые темы (0)
  - Где сосредоточена каждая тема
  - Использование
- Запуск

_Слов: 676_

### [[DEPENDABOT|Мониторинг зависимостей]]
> > !NOTE

  - Python-зависимости
  - OSS-проекты (Svyazi 2.0)
  - Автоматизация
- Генерировать .github/dependabot.yml
- Проверить актуальные версии PyPI

_Слов: 164_

### [[DEPENDENCY_MAP|Карта зависимостей скриптов]]
> > !NOTE

  - Содержание
  - Зависимости
  - Скрипты без карты зависимостей
  - Порядок запуска (рекомендуемый)
  - Кто ссылается на этот документ (4)
  - Смотрите также

_Слов: 1188_

### [[DIGEST|Дайджест изменений]]
> > !NOTE

  - Последний коммит
  - Последние 3 коммита — итого
  - История коммитов (последние 15)
  - Текущее состояние репозитория
  - Использование
- Запуск
  - Смотрите также

_Слов: 418_

### [[DIGEST_AUTO|Автодайджест изменений]]
> > !NOTE

  - Сводка
  - Активность по секциям
  - Последние коммиты
  - Новые файлы
  - Изменённые файлы
  - Ключевые слова изменений
  - Новые концепты
  - Использование
  _... ещё 1 разделов_

_Слов: 520_

### [[DIGEST_WEEKLY|Еженедельный дайджест — 2026-04-29]]
> - Итого(#итого)

  - Contents
  - Итого
  - Коммиты
  - Кто ссылается на этот документ (3)
  - Смотрите также

_Слов: 302_

### [[DUPLICATES|Отчёт о дублировании]]
> > !NOTE

  - Похожие файлы (Jaccard ≥ 0.5)

_Слов: 2147_

### [[EMPTY_SECTIONS|Пустые секции]]
> > EMPTYSECTIONS — раздел документации проекта Lorenzo.

  - Файлы с ≥50% пустых секций (приоритет)
  - Все файлы с пустыми секциями
  - Использование
- Запуск
- Вариант 2
- Вариант 3
- Вариант 4
- Вариант 5
  _... ещё 13 разделов_

_Слов: 30518_

### [[ENTITIES|Именованные сущности]]
> > ENTITIES — раздел документации проекта Lorenzo.

  - Люди и авторы (7)
  - Проекты (22)
  - Организации (9)
  - Технологии и стандарты (24)
  - GitHub репозитории (15)
  - Ко-встречаемость проектов (топ пары)
  - Использование
- Запуск

_Слов: 784_

### [[FAQ|Часто задаваемые вопросы (FAQ)]]
> > !NOTE

  - Архитектура
  - MVP/Запуск
  - Компоненты
  - Интеграция
  - Лицензия
  - Общее
  - Использование
- Запуск

_Слов: 1326_

### [[FOOTNOTES|Сноски и определения терминов]]
> > !NOTE

  - Словарь сносок
  - Как это работает

_Слов: 306_

### [[GLOSSARY|Глоссарий проектов]]
> > !NOTE

  - Использование
- Запуск

_Слов: 269_

### [[GRAPH|Граф связей проектов]]
> > !NOTE

  - Топ совместных упоминаний
  - DOT-формат (Graphviz)

_Слов: 2686_

### [[HEADING_AUDIT|Аудит заголовков]]
> > HEADINGAUDIT — раздел документации проекта Lorenzo.

  - Типы проблем
  - По файлам
  - Использование
- Запуск
- Вариант 2
- Вариант 3
- Вариант 4
- Вариант 5
  _... ещё 1 разделов_

_Слов: 8699_

### [[HEALTH|Health Dashboard]]
> > Балл здоровья репозитория: 100/100 — файлов: 2451, слов: 2,679,824

  - Общий балл: 100/100 🟢
  - Метрики
  - Структура репозитория
  - Action Items
  - Скрипты обработки
  - Рекомендации
  - Смотрите также

_Слов: 281_

### [[HEATMAP|Тепловая карта тем]]
> > HEATMAP — раздел документации проекта Lorenzo.

  - Числовые значения (‰)
  - Доминирующие темы по разделам
  - Концентрация тем

_Слов: 561_

### [[INDEX|Индекс документации — Lorenzo / Svyazi 2.0]]
> > INDEX — раздел документации проекта Lorenzo.

  - Метрики репозитория
  - Разделы документации
  - Аналитика и отчёты
  - Ключевые документы
  - LLM-обогащение (Ступень 3)
  - Быстрый старт
- Читать документацию
- Обновить всю документацию
  _... ещё 1 разделов_

_Слов: 562_

### [[KEYWORD_INDEX|Инвертированный индекс ключевых слов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Топ слов по охвату файлов
  - Топ биграмм (устойчивые словосочетания)
  - Похожие документы
  - Использование
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 1258_

### [[KNOWLEDGE_MAP|Карта базы знаний Lorenzo]]
> > KNOWLEDGEMAP — раздел документации проекта Lorenzo.

  - Корпус
  - Метрики качества
  - По секциям
  - Ключевые концепты
  - Топ сущностей
  - Открытые вопросы
  - Быстрые команды
- Поиск
  _... ещё 2 разделов_

_Слов: 644_

### [[KPI|Числовые KPI и метрики]]
> > KPI — раздел документации проекта Lorenzo.

  - Количество (496)
  - Проценты (378)
  - Время (542)
  - Стоимость (964)
  - Размер (90)
  - Версия (777)
  - Рейтинг (103)
  - Этап (184)
  _... ещё 3 разделов_

_Слов: 2845_

### [[KPI_HISTORY|История метрик KPI]]
> > KPIHISTORY — раздел документации проекта Lorenzo.

  - Текущие метрики
  - История
  - Тренды (последние снапшоты)

_Слов: 213_

### [[LANGUAGE_STATS|Языковой состав документов]]
> > LANGUAGESTATS — раздел документации проекта Lorenzo.

  - Распределение
  - Файлы с неожиданным языком
  - Смешанные файлы (MIX)
  - По секциям
  - Использование
- Запуск
- Вариант 2
- Вариант 3
  _... ещё 2 разделов_

_Слов: 7544_

### [[LINKS|Индекс ссылок]]
> > LINKS — раздел документации проекта Lorenzo.

  - Использование
- Запуск

_Слов: 1097_

### [[LLM_SUMMARIES|AI-саммари разделов документации]]
> - Архитектура Svyazi 2.0(#архитектура-svyazi-20)

  - Contents
  - Архитектура Svyazi 2.0
  - Вакансии Anthropic
  - Комбинации технологий
  - AI-коллаборации
  - Хабр-проекты
  - Связанные документы
  - Связанные документы
  _... ещё 5 разделов_

_Слов: 366_

### [[MCP_DASHBOARD|MCP Dashboard]]
> > !NOTE

  - Использование
- Запуск
  - Смотрите также

_Слов: 100_

### [[METHODOLOGY|Методология работы со скриптами]]
> > !NOTE

  - Содержание
  - Основной принцип
  - Три категории скриптов
  - Типичные рабочие сессии
- Прочитать docs/HEALTH.md и docs/BROKENLINKS.md
- Коммитить не обязательно
- Проверить результат в docs/05-habr-projects/
- Порядок важен: индексы должны быть готовы до контентных скриптов
  _... ещё 4 разделов_

_Слов: 1052_

### [[METRICS|Метрики качества документации]]
> > Средний балл: 99.8/100 по 1212 документам

  - Качество по разделам
  - Топ-15 лучших документов
  - Документы, требующие улучшения (1)
  - Общие показатели
  - Использование
- Обновить метрики и проверить здоровье репозитория
  - Смотрите также

_Слов: 358_

### [[MINDMAP|Майндмап репозитория Lorenzo]]
> > !NOTE

  - Структура разделов
  - Поток данных между проектами
  - Легенда

_Слов: 270_

### [[MISSING|Карта пробелов знаний]]
> > MISSING — раздел документации проекта Lorenzo.

  - Итог
  - Рекомендации
  - Использование
- Запуск

_Слов: 476_

### [[NAMED_ENTITIES|Индекс именованных сущностей]]
> > NAMEDENTITIES — раздел документации проекта Lorenzo.

  - 👤 People (20)
  - 📦 Projects (148)
  - ⚙️ Tech (31)
  - 🏢 Orgs (8)
  - 📅 Dates (43)
  - Использование
- Запуск

_Слов: 1565_

### [[NARRATIVE|Нарратив проекта Lorenzo]]
> > NARRATIVE — раздел документации проекта Lorenzo.

  - Глава 1: Исходная точка — Svyazi 2.0
  - Глава 2: Экосистема проектов
  - Глава 3: Ансамбли — синергия компонентов
  - Глава 4: MVP — что строим первым
  - Глава 5: Архитектурные пробелы
  - Глава 6: Контракты интеграции
  - Глава 7: Дорожная карта
  - Глава 8: Команда и контакты
  _... ещё 6 разделов_

_Слов: 1081_

### [[NETWORK|Сеть проектов и авторов]]
> > !NOTE

  - Топ-20 ко-упоминаемых пар
  - Центральность узлов (влиятельность)
  - Авторы ↔ Проекты
  - Использование
- Запуск

_Слов: 452_

### [[ONBOARDING|Онбординг — Svyazi 2.0 / Lorenzo]]
> > ONBOARDING — раздел документации проекта Lorenzo.

  - Что это такое?
  - Первые 30 минут
- 1. Клонировать репозиторий
- 2. Прочитать Executive Summary
- 3. Посмотреть статус проекта
- 4. Прочитать FAQ
- 5. Запустить скрипты (генерация/обновление docs)
  - Структура документации
  _... ещё 10 разделов_

_Слов: 508_

### [[ORPHANS|Изолированные документы (Orphans)]]
> > !NOTE

  - Топ-20 по объёму (важные и изолированные)
  - По разделам
  - Рекомендации
  - Использование
- Запуск

_Слов: 142_

### [[PARAGRAPH_QUALITY|Качество абзацев]]
> > PARAGRAPHQUALITY — раздел документации проекта Lorenzo.

  - Типы проблем
  - По файлам
  - Использование
- Запуск
- Вариант 2
- Вариант 3
- Вариант 4
- Вариант 5
  _... ещё 3 разделов_

_Слов: 12315_

### [[PASSIVE_VOICE|Пассивный залог и канцеляризмы]]
> > PASSIVEVOICE — раздел документации проекта Lorenzo.

  - Корпусная статистика
  - Топ файлов по доле пассива
  - Использование
- Запуск

_Слов: 429_

### [[PRIORITIES|Приоритеты файлов]]
> > PRIORITIES — раздел документации проекта Lorenzo.

  - Топ-50 самых важных файлов
  - Топ-5 по каждому разделу
  - Использование
- Запуск
- Вариант 2

_Слов: 3433_

### [[PROGRESS|Прогресс MVP]]
> > !NOTE

  - Ключевые этапы (Milestones)
  - Состояние компонентов
  - Метрики качества
  - Следующий шаг
- Приоритет 1: kksudo (AgentFS, 13 упоминаний)
- Приоритет 2: spbmolot (NGT Memory, 12 упоминаний)
- Приоритет 3: AnastasiyaW (knowledge-space, 11 упоминаний)
  - Связанные документы

_Слов: 289_

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
  _... ещё 3 разделов_

_Слов: 1462_

### [[QA|Глобальный Q&A]]
> > !NOTE

  - Раздел: 01-svyazi
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  _... ещё 144 разделов_

_Слов: 1927_

### [[QUESTIONS|Открытые вопросы]]
> > QUESTIONS — раздел документации проекта Lorenzo.

  - Архитектура (61)
  - Интеграция (43)
  - Mvp/сроки (56)
  - Технология (270)
  - Лицензия (41)
  - Команда (72)
  - Общее (1387)
  - Использование
  _... ещё 1 разделов_

_Слов: 1896_

### [[READING_LIST|Список чтения]]
> - По секциям(#по-секциям)

  - Contents
  - По секциям
  - Похожие документы
  - Использование
  - Смотрите также

_Слов: 365_

### [[READING_ORDER|Рекомендуемый порядок чтения]]
> > !NOTE

  - Маршруты по целям
  - Использование
- Запуск
- Вариант 2
- Вариант 3
- Вариант 4

_Слов: 6104_

### [[README|docs]]
> Файлов: 106

  - Содержание
  - Подразделы
  - Кто ссылается на этот документ (226)
  - Использование

_Слов: 865_

### [[REGISTRY|REGISTRY — реестр артефактов Lorenzo]]
> > !NOTE

  - Сводка
  - Скрипты по группам
  - Шаблоны
  - Скилы
  - MCP-серверы
  - Манифесты задач
  - Контакты
  - Полезные команды
  _... ещё 6 разделов_

_Слов: 1372_

### [[REPORT|Svyazi 2.0 — Knowledge Base Report]]
> > !NOTE

  - Содержание
  - Executive Summary
  - Корпус документов
  - Ключевые проекты
  - Ключевые сущности
  - Архитектурные решения
  - Открытые вопросы
  - Рекомендуемое чтение
  _... ещё 4 разделов_

_Слов: 960_

### [[RISK_REGISTER|Реестр рисков — Svyazi 2.0]]
> > !TIP

  - Матрица рисков (Вероятность × Влияние)
  - Реестр
  - Митигации
  - Упоминания рисков в документах
  - Итоговая статистика

_Слов: 837_

### [[SCHEDULE|Расписание проекта]]
> > !NOTE

  - Ключевые вехи
  - Gantt-диаграмма
  - Задачи по фазам
  - Текущий статус
  - Смотрите также

_Слов: 315_

### [[SCORING|Оценка готовности проекта (Go/No-Go)]]
> > !NOTE

  - Итог: 164/164 (100%) — 🟢 GO
  - Документация — 48/48 (100%) 🟢 GO
  - Архитектура — 41/41 (100%) 🟢 GO
  - Команда и контакты — 23/23 (100%) 🟢 GO
  - Риски — 26/26 (100%) 🟢 GO
  - MVP-готовность — 26/26 (100%) 🟢 GO
  - Приоритетные действия (0 незакрытых)
  - ✅ Проект готов к запуску MVP!
  _... ещё 3 разделов_

_Слов: 357_

### [[SCRIPTS_CATALOG|Каталог скриптов]]
> Обновлено: 2026-05-11

  - По группам
  - Подробно
  - Использование
- Запуск
- Вариант 2
- Вариант 3
- Вариант 4
  - Смотрите также

_Слов: 7578_

### [[SCRIPT_EVAL_REPORT|Отчёт об оценке скриптов Lorenzo]]
> > !WARNING

  - Содержание
  - 1. Общая картина: что изменилось
  - 2. Диалог-сценки: скрипты в действии
- Шаг 1: посмотреть, что будет создано
- Шаг 2: реальная сборка
- Шаг 3: статистика
- Шаг 4: поиск
- Шаг 5: одобрить найденный проект
  _... ещё 17 разделов_

_Слов: 2951_

### [[SEARCH_RESULTS|Результаты поиска]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
  - Смотрите также

_Слов: 324_

### [[SEE_ALSO|Индекс «Смотрите также»]]
> > !NOTE

  - Ключевые связи
  - Использование
- Запуск

_Слов: 256_

### [[SENTIMENT|Тональный анализ документов]]
> > SENTIMENT — раздел документации проекта Lorenzo.

  - Тональность по разделам
  - Самые оптимистичные документы
  - Самые скептичные / риск-ориентированные
  - Распределение тональности
  - Использование
- Запуск

_Слов: 599_

### [[SIMILAR|Похожие документы]]
> - Топ-20 самых похожих пар(#топ-20-самых-похожих-пар)

  - Contents
  - Топ-20 самых похожих пар
  - По разделам
  - Использование

_Слов: 408_

### [[SIMILAR_PASSAGES|Похожие абзацы между документами]]
> > !TIP

  - Содержание
  - Найденные похожие абзацы
  - Похожие документы
  - Использование
  - Смотрите также

_Слов: 1829_

### [[SITEMAP|Карта репозитория Lorenzo]]
> Обновлено: 2026-05-11

  - Навигация
  - Мета-документы
  - Svyazi 2.0 — Архитектура системы
  - Вакансии Anthropic — 436 позиций
  - Комбинации технологий
  - AI Коллаборации — ансамбли проектов
  - Хабр-проекты — память и граф
  - ai-collaborations
  _... ещё 13 разделов_

_Слов: 9310_

### [[SKILL_DASHBOARD|Skill Dashboard]]
> > !NOTE

  - Использование
- Запуск
  - Смотрите также

_Слов: 100_

### [[SOURCE_MAP|Карта происхождения текстов]]
> > SOURCEMAP — раздел документации проекта Lorenzo.

  - Категории
  - Авторы
  - 🤖 Авто-импортированные файлы (1722)
  - 🔗 Файлы с внешними ссылками (198)
  - Использование
- Запуск
- Вариант 2
- Вариант 3
  _... ещё 5 разделов_

_Слов: 12354_

### [[STATS|Детальная статистика репозитория]]
> Разделов: 21  Файлов: 2445  Слов: 2,676,476  Символов: 23,103,065

  - Сводная таблица по разделам
  - Топ-20 файлов по объёму
  - Ключевые показатели

_Слов: 681_

### [[SUMMARIES|Резюме документов (TextRank)]]
> > !TIP

  - Содержание
  - docs/01-svyazi/01-executive-summary.md
  - docs/01-svyazi/02-methodology.md
  - docs/01-svyazi/03-component-catalog.md
  - docs/01-svyazi/04-ensembles-overview.md
  - docs/01-svyazi/06-security-privacy.md
  - docs/01-svyazi/07-mvp-planning.md
  - docs/01-svyazi/08-conclusions.md
  _... ещё 47 разделов_

_Слов: 3863_

### [[TABLES|Все таблицы репозитория]]
> > !TIP

  - 01-svyazi (11 таблиц)
  - 02-anthropic-vacancies (34 таблиц)
  - 03-technology-combinations (1 таблиц)
  - 04-ai-collaborations (38 таблиц)
  - 05-habr-projects (22 таблиц)
  - ai-collaborations (13 таблиц)
  - anthropic-vacancies (2 таблиц)
  - contacts (15 таблиц)
  _... ещё 165 разделов_

_Слов: 302886_

### [[TAGS|Индекс тегов]]
> > TAGS — раздел документации проекта Lorenzo.

  - #anthropic (9 файлов)
  - #architecture (6 файлов)
  - #collaboration (9 файлов)
  - #ingestion (9 файлов)
  - #knowledge (5 файлов)
  - #local-first (3 файлов)
  - #memory (5 файлов)
  - #orchestration (6 файлов)
  _... ещё 6 разделов_

_Слов: 288_

### [[TASKS_INDEX|Каталог задач (TASKSINDEX)]]
> > Каталог задач из YAML-файлов: пайплайны, зависимости и статусы выполнения.

  - Содержание
  - По MCP-серверу
  - Подробно
  - Использование

_Слов: 1072_

### [[TECH_RADAR|Tech Radar — Svyazi 2.0]]
> > TECHRADAR — раздел документации проекта Lorenzo.

  - Обзор
  - 🟢 ADOPT
  - 🔵 TRIAL
  - 🟡 ASSESS
  - 🔴 HOLD
  - Методология

_Слов: 572_

### [[TIMELINE|Хронологическая лента событий]]
> > TIMELINE — раздел документации проекта Lorenzo.

  - 2020 (6 упоминаний)
  - 2021 (5 упоминаний)
  - 2022 (13 упоминаний)
  - 2023 (11 упоминаний)
  - 2024 (47 упоминаний)
  - 2025 (44 упоминаний)
  - 2026 (483 упоминаний)
  - 2027 (3 упоминаний)
  _... ещё 4 разделов_

_Слов: 2180_

### [[VALIDATION|Валидация структуры репозитория]]
> > Ошибок: 0, предупреждений: 0, пройдено: 29

  - Contents
  - Сводка
  - ✅ Разделы и README
  - ✅ Мета-файлы
  - ✅ Пустые/короткие файлы
  - Именование файлов
  - ✅ Заголовки H1
  - Внутренние ссылки
  _... ещё 2 разделов_

_Слов: 424_

### [[VOCABULARY|Богатство словаря документов]]
> > VOCABULARY — раздел документации проекта Lorenzo.

  - Корпусная статистика
  - Топ файлов по богатству словаря (STTR)
  - Файлы с бедным словарём (требуют доработки)
  - Справка по метрикам
  - Использование
- Запуск

_Слов: 938_

### [[WORD_CLOUD|Word Cloud]]
> - Топ-20 слов(#топ-20-слов)

  - Contents
  - Топ-20 слов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 301_

### [[WORD_FREQ|Частотный анализ слов]]
> > WORDFREQ — раздел документации проекта Lorenzo.

  - Глобальный топ-50 слов
  - Топ-15 слов по разделам
  - Уникальные слова разделов
  - Использование
- Запуск
- Вариант 2

_Слов: 3230_

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
  _... ещё 5 разделов_

_Слов: 674_

**Итого в секции: 508,762 слов, 96 файлов**


## Svyazi

_Путь: `docs/01-svyazi/`_

### [Продолжение исследования для Svyazi[^svyazi] 2.0](01-svyazi/00-intro-part2.md)
> > Продолжение анализа архитектуры Svyazi 2.0: компоненты, ансамбли и интеграционные контракты.

  - Содержание
  - Смотрите также
  - Использование

_Слов: 356_

### [Svyazi[^svyazi] 2.0 — Исполнительное резюме](01-svyazi/01-executive-summary.md)
> - Главная линия синергии(#главная-линия-синергии)

  - Содержание
  - Содержание
  - Главная линия синергии
  - Ключевой вывод
  - Что добавляет продолжение исследования
  - Приоритет ансамблей для старта
  - Похожие документы
  - Использование
  _... ещё 1 разделов_

_Слов: 750_

### [[02-methodology|Методика и рамка отбора проектов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Источники
  - Шкала зрелости
  - Принцип отбора паттернов
  - Принципы интеграционной оценки
  - Похожие документы
  - Использование
  _... ещё 2 разделов_

_Слов: 563_

### [[03-component-catalog|Каталог компонентов Svyazi 2.0]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Карта найденных проектов и паттернов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 1512_

### [[04-ensembles-overview|Приоритетные ансамбли проектов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Приоритетные ансамбли
  - Похожие документы
  - Смотрите также

_Слов: 1383_

### [[06-security-privacy|Безопасность и приватность]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Безопасность, приватность и бюджетный роутинг
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 937_

### [[07-mvp-planning|Планирование MVP]]
> - Contents(#contents)

  - Содержание
  - Contents
  - План прототипа и возможные контакты
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 1183_

### [[08-conclusions|Выводы]]
> - Выводы(#выводы)

  - Contents
  - Выводы
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 468_

### [[09-architectural-gaps|Архитектурные зазоры]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Архитектурные зазоры, которые важнее новых инструментов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 874_

### [[10-second-order-ensembles|Ансамбли следующего шага]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Новые ансамбли следующего шага
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 1009_

### [[11-integration-contracts|Интеграционные контракты]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Интеграционный контракт, который стоит зафиксировать сразу
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 854_

### [[12-roadmap|Дорожная карта прототипа]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Дорожная карта прототипа следующей итерации
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 836_

### [[13-contacts|Контактная стратегия]]
> > !TIP

  - Содержание
  - Контактная стратегия и узкие вопросы для авторов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 2 разделов_

_Слов: 1080_

### [[14-limitations|Ограничения и лицензии]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Ограничения, лицензии и что пока лучше не склеивать
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 761_

### [[QA|Q&A: 01-svyazi]]
> > !NOTE

  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  - Как организован бюджетный роутинг между моделями?
  _... ещё 7 разделов_

_Слов: 232_

### [Svyazi[^svyazi] 2.0 — Архитектура и исследование](01-svyazi/README.md)
> > Раздел архитектуры Svyazi 2.0: компоненты, ансамбли, контракты и дорожная карта локальной платформы коллективного инте…

  - Содержание
  - Подразделы
  - Похожие документы
  - Использование

_Слов: 424_

**Итого в секции: 13,222 слов, 16 файлов**


## Anthropic Vacancies

_Путь: `docs/02-anthropic-vacancies/`_

### [[00-intro|Введение]]
> > Абстракт (авто)

  - Содержание
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  - Кто ссылается на этот документ (3)
  - Использование
  _... ещё 3 разделов_

_Слов: 9049_

### [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]]
> > Абстракт (авто)

  - Содержание
  - Интегральный анализ профиля svend4
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 19240_

### [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]]
> > Абстракт (авто)

  - Содержание
  - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL
- portal-mcp.py
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  _... ещё 2 разделов_

_Слов: 3329_

### [[03-portal-protocol-md|PORTAL-PROTOCOL.md]]
> - PORTAL-PROTOCOL.md(#portal-protocolmd)

  - Contents
  - PORTAL-PROTOCOL.md
- Nautilus Portal Protocol
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 398_

### [[04-abstract|Abstract]]
> - Abstract(#abstract)

  - Contents
  - Abstract
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 416_

### [[05-0-status-of-this-document|0. Status of This Document]]
> - 0. Status of This Document(#0-status-of-this-document)

  - Contents
  - 0. Status of This Document
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 410_

### [[06-1-introduction|1. Introduction]]
> - 1. Introduction(#1-introduction)

  - Contents
  - 1. Introduction
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 449_

### [[07-2-terminology|2. Terminology]]
> - 2. Terminology(#2-terminology)

  - Contents
  - 2. Terminology
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 391_

### [[08-3-registry-nautilus-json|3. Registry (nautilus.json)]]
> - 3. Registry (nautilus.json)(#3-registry-nautilusjson)

  - Содержание
  - 3. Registry (nautilus.json)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 495_

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
  _... ещё 9 разделов_

_Слов: 359_

### [[102-доступ-к-данным|Доступ к данным]]
> - Доступ к данным(#доступ-к-данным)

  - Contents
  - Доступ к данным
  - Упоминается в
  - Упоминается в
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 302_

### [[103-appendix-b-change-log|Appendix B: Change Log]]
> - Appendix B: Change Log(#appendix-b-change-log)

  - Contents
  - Appendix B: Change Log
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 406_

### [[104-appendix-c-references|Appendix C: References]]
> > !NOTE

  - Содержание
  - Appendix C: References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1238_

### [[105-review-methodology-md|REVIEWMETHODOLOGY.md]]
> - REVIEWMETHODOLOGY.md(#reviewmethodologymd)

  - Contents
  - REVIEWMETHODOLOGY.md
- Трёхфазная методология Review в Nautilus
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 353_

### [[106-tl-dr|TL;DR]]
> - TL;DR(#tldr)

  - Contents
  - TL;DR
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 312_

### [[107-1-контекст-и-мотивация|1. Контекст и мотивация]]
> - 1. Контекст и мотивация(#1-контекст-и-мотивация)

  - Contents
  - 1. Контекст и мотивация
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 487_

### [[108-2-формальный-workflow|2. Формальный workflow]]
> - 2. Формальный workflow(#2-формальный-workflow)

  - Содержание
  - 2. Формальный workflow
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 443_

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
  _... ещё 9 разделов_

_Слов: 700_

### [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или осмысленный?]]
> - Вопрос: fallback-ratio как критический или осмысленный?(#вопрос-fallback-ratio-как-критический-или-осмысленный)

  - Contents
  - Вопрос: fallback-ratio как критический или осмысленный?
  - Смотрите также
  - Похожие документы

_Слов: 381_

### [[111-4-условия-применимости|4. Условия применимости]]
> - 4. Условия применимости(#4-условия-применимости)

  - Contents
  - 4. Условия применимости
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 339_

### [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]]
> - 5. Связь с существующими методологиями(#5-связь-с-существующими-методологиями)

  - Contents
  - 5. Связь с существующими методологиями
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 440_

### [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assisted workflows]]
> - 6. Почему это валидный паттерн для AI-assisted workflows(#6-почему-это-валидный-паттерн-для-ai-assisted-workflows)

  - Contents
  - 6. Почему это валидный паттерн для AI-assisted workflows
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]]
> - 7. Реализация в проекте Nautilus(#7-реализация-в-проекте-nautilus)

  - Contents
  - 7. Реализация в проекте Nautilus
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 341_

### [[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Ограничения и открытые вопросы
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 540_

### [[116-9-checklist-применения-методологии|9. Checklist применения методологии]]
> - 9. Checklist применения методологии(#9-checklist-применения-методологии)

  - Contents
  - 9. Checklist применения методологии
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 452_

### [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим документам]]
> - 10. Конкретный план применения к текущим документам(#10-конкретный-план-применения-к-текущим-документам)

  - Contents
  - 10. Конкретный план применения к текущим документам
- В Termux
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 347_

### [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]]
> - Appendix A: Шаблон для header warning(#appendix-a-шаблон-для-header-warning)

  - Contents
  - Appendix A: Шаблон для header warning
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 307_

### [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешения]]
> - Appendix B: Примеры расхождений и их разрешения(#appendix-b-примеры-расхождений-и-их-разрешения)

  - Contents
  - Appendix B: Примеры расхождений и их разрешения
  - Смотрите также
  - Похожие документы

_Слов: 403_

### [[12-content-overview|Content Overview]]
> - Content Overview(#content-overview)

  - Contents
  - Content Overview
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  - Использование
  _... ещё 3 разделов_

_Слов: 302_

### [[120-главные-технические-риски|Главные технические риски]]
> - Главные технические риски(#главные-технические-риски)

  - Contents
  - Главные технические риски
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]]
> - Appendix C: История изменений методологии(#appendix-c-история-изменений-методологии)

  - Contents
  - Appendix C: История изменений методологии
  - Упоминается в
  - Упоминается в
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 302_

### [[122-глоссарий|Глоссарий]]
> > Абстракт (авто)

  - Содержание
  - Глоссарий
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1555_

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
  _... ещё 61 разделов_

_Слов: 2542_

### [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]]
> - Конфигурация для Claude Desktop(#конфигурация-для-claude-desktop)

  - Contents
  - Конфигурация для Claude Desktop
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 330_

### [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]]
> - README-MCP.md— инструкция по установке(#readme-mcpmd-инструкция-по-установке)

  - Contents
  - README-MCP.md— инструкция по установке
- Nautilus Portal MCP Integration
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 345_

### [[126-установка|Установка]]
> - Установка(#установка)

  - Contents
  - Установка
- Ждёт stdio-input; Ctrl+C для выхода
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (4)

_Слов: 309_

### [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]]
> - Подключение к Claude Desktop(#подключение-к-claude-desktop)

  - Contents
  - Подключение к Claude Desktop
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 320_

### [[128-доступные-инструменты|Доступные инструменты]]
> - Доступные инструменты(#доступные-инструменты)

  - Contents
  - Доступные инструменты
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 370_

### [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]]
> - Примеры запросов (в Claude)(#примеры-запросов-в-claude)

  - Contents
  - Примеры запросов (в Claude)
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 374_

### [[13-angle-perspective|Angle / Perspective]]
> - Angle / Perspective(#angle-perspective)

  - Contents
  - Angle / Perspective
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  - Использование
  _... ещё 3 разделов_

_Слов: 315_

### [[130-отладка|Отладка]]
> - Отладка(#отладка)

  - Contents
  - Отладка
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 318_

### [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]]
> - Ограничения текущей версии (0.1.0-draft)(#ограничения-текущей-версии-010-draft)

  - Contents
  - Ограничения текущей версии (0.1.0-draft)
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 302_

### [[132-planned-v0-2-0|Planned (v0.2.0)]]
> - Planned (v0.2.0)(#planned-v020)

  - Contents
  - Planned (v0.2.0)
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 304_

### [[133-обратная-связь|Обратная связь]]
> > Абстракт (авто)

  - Содержание
  - Обратная связь
- MCP интеграция (для Claude Desktop)
- Конфигурация: см. README-MCP.md
- В приватном репо cases-private:
  - Похожие документы
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 17102_

### [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]]
> - THE DOUBLE-TRIANGLE ARCHITECTURE.md(#the-double-triangle-architecturemd)

  - Contents
  - THE DOUBLE-TRIANGLE ARCHITECTURE.md
- The Double-Triangle Architecture
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 4 разделов_

_Слов: 365_

### [[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in Distributed Knowledge Work]]
> - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work(#a-formal-model-for-human-ai-collaboration-in-…

  - Contents
  - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 382_

### [[136-abstract|Abstract]]
> > !NOTE

  - Содержание
  - Abstract
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 676_

### [[137-table-of-contents|Table of Contents]]
> - Основной раздел

  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 371_

### [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]]
> > !NOTE

  - Содержание
  - 1. Why Single-Triangle Models Are Incomplete
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 633_

### [[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]]
> > Абстракт (авто)

  - Содержание
  - 2. The Double-Triangle Architecture
- Bridges
  - Bridges
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 782_

### [[140-3-three-inter-layer-protocols|3. Three Inter-Layer Protocols]]
> > Абстракт (авто)

  - Содержание
  - 3. Three Inter-Layer Protocols
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1068_

### [[141-4-nautilus-portal-as-reference-substrate|4. Nautilus Portal as Reference Substrate]]
> > !NOTE

  - Содержание
  - 4. Nautilus Portal as Reference Substrate
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 965_

### [[142-5-pattern-library-as-bridge-between-triangles|5. Pattern Library as Bridge Between Triangles]]
> > Абстракт (авто)

  - Содержание
  - 5. Pattern Library as Bridge Between Triangles
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 881_

### [[143-6-four-deployment-domains|6. Four Deployment Domains]]
> > !TIP

  - Содержание
  - 6. Four Deployment Domains
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 903_

### [[144-7-open-questions|7. Open Questions]]
> > Абстракт (авто)

  - Содержание
  - 7. Open Questions
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 982_

### [[145-8-call-to-action|8. Call to Action]]
> > Абстракт (авто)

  - Содержание
  - 8. Call to Action
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 948_

### [[146-acknowledgments|Acknowledgments]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Acknowledgments
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 548_

### [[147-references|References]]
> - References(#references)

  - Contents
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 414_

### [[148-appendix-a-glossary|Appendix A: Glossary]]
> - Appendix A: Glossary(#appendix-a-glossary)

  - Содержание
  - Appendix A: Glossary
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 566_

### [[149-appendix-b-summary-of-contributions|Appendix B: Summary of Contributions]]
> - Appendix B: Summary of Contributions(#appendix-b-summary-of-contributions)

  - Contents
  - Appendix B: Summary of Contributions
- Author & Contact
  - Author & Contact
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 5 разделов_

_Слов: 432_

### [[150-appendix-c-version-history|Appendix C: Version History]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: Version History
  - Похожие документы
  - Использование
- Поиск (bm25)
- Поиск (semantic)
- Поиск (full)
  - Смотрите также
  _... ещё 5 разделов_

_Слов: 8670_

### [[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]]
> - OPEN KNOWLEDGE WORK FOUNDATION.md(#open-knowledge-work-foundationmd)

  - Contents
  - OPEN KNOWLEDGE WORK FOUNDATION.md
- Open Knowledge Work Foundation
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 4 разделов_

_Слов: 431_

### [[152-ai-coordinated-infrastructure-for-distributed-expe|AI-Coordinated Infrastructure for Distributed Expert Contribution]]
> - AI-Coordinated Infrastructure for Distributed Expert Contribution(#ai-coordinated-infrastructure-for-distributed-exper…

  - Contents
  - AI-Coordinated Infrastructure for Distributed Expert Contribution
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 353_

### [[153-executive-summary|Executive Summary]]
> > !TIP

  - Содержание
  - Executive Summary
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 656_

### [[154-table-of-contents|Table of Contents]]
> - Основной раздел

  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 330_

### [[155-1-problem-statement|1. Problem Statement]]
> > !NOTE

  - Содержание
  - 1. Problem Statement
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 837_

### [[156-2-target-populations|2. Target Populations]]
> > !NOTE

  - Содержание
  - 2. Target Populations
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 866_

### [[157-3-why-existing-solutions-fail|3. Why Existing Solutions Fail]]
> > !NOTE

  - Содержание
  - 3. Why Existing Solutions Fail
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 851_

### [[158-4-proposed-infrastructure|4. Proposed Infrastructure]]
> > Абстракт (авто)

  - Содержание
  - 4. Proposed Infrastructure
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (13)

_Слов: 1070_

### [[159-5-economic-model|5. Economic Model]]
> - 5. Economic Model(#5-economic-model)

  - Содержание
  - Содержание
  - 5. Economic Model
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 667_

### [[16-history|History]]
> - History(#history)

  - Contents
  - History
  - Упоминается в
  - Упоминается в
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 304_

### [[160-6-governance-and-ethics|6. Governance and Ethics]]
> > !NOTE

  - Содержание
  - 6. Governance and Ethics
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 633_

### [[161-7-phased-rollout-plan|7. Phased Rollout Plan]]
> > !NOTE

  - Содержание
  - 7. Phased Rollout Plan
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 847_

### [[162-8-risk-analysis|8. Risk Analysis]]
> > Абстракт (авто)

  - Содержание
  - 8. Risk Analysis
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 2 разделов_

_Слов: 775_

### [[163-9-call-for-partnership|9. Call for Partnership]]
> > !NOTE

  - Содержание
  - 9. Call for Partnership
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 647_

### [[164-10-appendices|10. Appendices]]
> > !NOTE

  - Содержание
  - 10. Appendices
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1202_

### [[165-closing|Closing]]
> > Абстракт (авто)

  - Содержание
  - Closing
- unknownlegalconcepts.yml
  - Похожие документы
  - Использование
- Поиск (bm25)
- Поиск (semantic)
- Поиск (full)
  _... ещё 7 разделов_

_Слов: 9492_

### [[166-representative-agent-layer-md|REPRESENTATIVE AGENT LAYER.md]]
> - REPRESENTATIVE AGENT LAYER.md(#representative-agent-layermd)

  - Contents
  - REPRESENTATIVE AGENT LAYER.md
- The Representative Agent Layer
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 4 разделов_

_Слов: 323_

### [[167-ai-mediated-representation-for-underrepresented-ex|AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]
> - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations(#ai-mediated-representation-for-und…

  - Contents
  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 474_

### [[168-abstract|Abstract]]
> > !NOTE

  - Содержание
  - Abstract
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 623_

### [[169-table-of-contents|Table of Contents]]
> - Основной раздел

  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 341_

### [[17-5-compatibility-levels|5. Compatibility Levels]]
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 398_

### [[170-1-the-cinderella-syndrome-why-quality-stays-invisi|1. The Cinderella Syndrome: Why Quality Stays Invisible]]
> > !NOTE

  - Содержание
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1005_

### [[171-2-historical-precedents-agents-as-civilizational-i|2. Historical Precedents: Agents as Civilizational Innovation]]
> > !NOTE

  - Содержание
  - 2. Historical Precedents: Agents as Civilizational Innovation
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1157_

### [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]]
> > !NOTE

  - Содержание
  - 3. What Makes a Representative Agent
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 958_

### [[173-4-ten-domains-of-application|4. Ten Domains of Application]]
> > Абстракт (авто)

  - Содержание
  - 4. Ten Domains of Application
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 1 разделов_

_Слов: 1702_

### [[174-5-architectural-specification|5. Architectural Specification]]
> > !NOTE

  - Содержание
  - 5. Architectural Specification
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 914_

### [[175-6-ethical-framework|6. Ethical Framework]]
> - 6. Ethical Framework(#6-ethical-framework)

  - Содержание
  - 6. Ethical Framework
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 610_

### [[176-7-governance-and-oversight|7. Governance and Oversight]]
> > !NOTE

  - Содержание
  - 7. Governance and Oversight
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 459_

### [[177-8-risks-and-mitigations|8. Risks and Mitigations]]
> > !WARNING

  - Содержание
  - 8. Risks and Mitigations
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 632_

### [[178-9-phased-rollout-strategy|9. Phased Rollout Strategy]]
> > !NOTE

  - Содержание
  - 9. Phased Rollout Strategy
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 636_

### [[179-10-open-questions|10. Open Questions]]
> > !NOTE

  - Содержание
  - 10. Open Questions
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 444_

### [[18-6-adapter-interface|6. Adapter Interface]]
> - 6. Adapter Interface(#6-adapter-interface)

  - Содержание
  - 6. Adapter Interface
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 760_

### [[180-11-call-for-collaboration|11. Call for Collaboration]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 11. Call for Collaboration
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 581_

### [[181-12-closing|12. Closing]]
> - 12. Closing(#12-closing)

  - Contents
  - 12. Closing
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 497_

### [[182-acknowledgments|Acknowledgments]]
> - Acknowledgments(#acknowledgments)

  - Contents
  - Acknowledgments
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 423_

### [[183-references|References]]
> - References(#references)

  - Contents
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 385_

### [[184-appendix-a-connection-to-companion-papers|Appendix A: Connection to Companion Papers]]
> - Appendix A: Connection to Companion Papers(#appendix-a-connection-to-companion-papers)

  - Contents
  - Appendix A: Connection to Companion Papers
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 497_

### [[185-appendix-b-domain-comparison-matrix|Appendix B: Domain Comparison Matrix]]
> - Appendix B: Domain Comparison Matrix(#appendix-b-domain-comparison-matrix)

  - Contents
  - Appendix B: Domain Comparison Matrix
  - Упоминается в
  - Упоминается в
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 379_

### [[186-appendix-c-sample-use-cases-in-detail|Appendix C: Sample Use Cases in Detail]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: Sample Use Cases in Detail
  - Похожие документы
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 2281_

### [[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]]
> - СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md(#слой-представительских-агентовmd)

  - Contents
  - СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md
- Слой Представительских Агентов
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 4 разделов_

_Слов: 304_

### [[188-ai-опосредованное-представительство-для-недопредст|AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения]]
> - AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения(#ai-опосредованное…

  - Contents
  - AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 307_

### [[189-аннотация|Аннотация]]
> - Аннотация(#аннотация)

  - Contents
  - Аннотация
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 408_

### [[19-7-portalentry-structure|7. PortalEntry Structure]]
> - 7. PortalEntry Structure(#7-portalentry-structure)

  - Contents
  - 7. PortalEntry Structure
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 310_

### [[190-содержание|Содержание]]
> > !WARNING

  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  _... ещё 2 разделов_

_Слов: 324_

### [[191-1-синдром-золушки-почему-качество-остаётся-невидим|1. Синдром Золушки: Почему качество остаётся невидимым]]
> > !WARNING

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 856_

### [[192-2-исторические-прецеденты-агенты-как-цивилизационн|2. Исторические прецеденты: Агенты как цивилизационная инновация]]
> > Абстракт (авто)

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в

_Слов: 1033_

### [[193-3-что-делает-агента-представительским|3. Что делает агента Представительским]]
> > !WARNING

  - Содержание
  - 3. Что делает агента Представительским
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 821_

### [[194-4-десять-областей-применения|4. Десять областей применения]]
> > Абстракт (авто)

  - Содержание
  - 4. Десять областей применения
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (5)

_Слов: 1673_

### [[195-5-архитектурная-спецификация|5. Архитектурная спецификация]]
> > !WARNING

  - Содержание
  - 5. Архитектурная спецификация
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 633_

### [[196-6-этическая-рамка|6. Этическая рамка]]
> - 6. Этическая рамка(#6-этическая-рамка)

  - Содержание
  - Содержание
  - 6. Этическая рамка
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 653_

### [[197-7-управление-и-надзор|7. Управление и надзор]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 7. Управление и надзор
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 551_

### [[198-8-риски-и-меры-противодействия|8. Риски и меры противодействия]]
> - 8. Риски и меры противодействия(#8-риски-и-меры-противодействия)

  - Содержание
  - 8. Риски и меры противодействия
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 645_

### [[199-9-стратегия-поэтапного-развёртывания|9. Стратегия поэтапного развёртывания]]
> - 9. Стратегия поэтапного развёртывания(#9-стратегия-поэтапного-развёртывания)

  - Содержание
  - 9. Стратегия поэтапного развёртывания
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 645_

### [[20-8-consensus-algorithm|8. Consensus Algorithm]]
> - 8. Consensus Algorithm(#8-consensus-algorithm)

  - Contents
  - 8. Consensus Algorithm
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 365_

### [[200-10-открытые-вопросы|10. Открытые вопросы]]
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 483_

### [[201-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 11. Призыв к сотрудничеству
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 579_

### [[202-12-заключение|12. Заключение]]
> - 12. Заключение(#12-заключение)

  - Contents
  - 12. Заключение
  - Упоминается в
  - Упоминается в
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 315_

### [[203-благодарности|Благодарности]]
> - Благодарности(#благодарности)

  - Contents
  - Благодарности
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 2 разделов_

_Слов: 302_

### [[204-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 366_

### [[205-приложение-a-связь-с-сопроводительными-статьями|Приложение A: Связь с Сопроводительными Статьями]]
> - Приложение A: Связь с Сопроводительными Статьями(#приложение-a-связь-с-сопроводительными-статьями)

  - Contents
  - Приложение A: Связь с Сопроводительными Статьями
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 302_

### [[206-приложение-b-матрица-сравнения-областей|Приложение B: Матрица Сравнения Областей]]
> - Приложение B: Матрица Сравнения Областей(#приложение-b-матрица-сравнения-областей)

  - Contents
  - Приложение B: Матрица Сравнения Областей
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  - Использование
- Поиск по теме документа
  _... ещё 2 разделов_

_Слов: 347_

### [[207-приложение-c-образцы-случаев-использования-в-детал|Приложение C: Образцы Случаев Использования в Деталях]]
> > Абстракт (авто)

  - Содержание
  - Приложение C: Образцы Случаев Использования в Деталях
  - Похожие документы
  - Использование
- BM25 поиск
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 4243_

### [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]]
> - PROFESSIONAL COLLEAGUE AGENTS.md(#professional-colleague-agentsmd)

  - Contents
  - PROFESSIONAL COLLEAGUE AGENTS.md
- Professional Colleague Agents
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 4 разделов_

_Слов: 389_

### [[209-a-typology-of-ai-agents-on-the-principal-side-and-|A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers]]
> - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers(#a-typology-of-ai-agents…

  - Contents
  - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 471_

### [[21-9-query-flow|9. Query Flow]]
> - 9. Query Flow(#9-query-flow)

  - Contents
  - 9. Query Flow
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 394_

### [[210-abstract|Abstract]]
> > !NOTE

  - Содержание
  - Abstract
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 665_

### [[211-table-of-contents|Table of Contents]]
> - Основной раздел

  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 494_

### [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side Agents]]
> > !NOTE

  - Содержание
  - 1. The Five-Type Typology of Principal-Side Agents
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 1231_

### [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]]
> > !NOTE

  - Содержание
  - 2. What Makes a Professional Colleague Agent
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1154_

### [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]]
> > !NOTE

  - Содержание
  - 3. Empirical Case Study: «Обучай»
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1112_

### [[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Agents]]
> > !NOTE

  - Содержание
  - 4. Architecture of Professional Colleague Agents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1170_

### [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replication]]
> > !NOTE

  - Содержание
  - 5. The Economics of Profession-Wide Replication
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1037_

### [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]]
> > Абстракт (авто)

  - Содержание
  - 6. Risks Specific to this Category
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1422_

### [[218-7-application-domains|7. Application Domains]]
> > Абстракт (авто)

  - Содержание
  - 7. Application Domains
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 2 разделов_

_Слов: 869_

### [[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]]
> > !NOTE

  - Содержание
  - 8. Pilot Proposal: SGB Advocate Colleague
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1251_

### [[22-10-queryresult-structure|10. QueryResult Structure]]
> - 10. QueryResult Structure(#10-queryresult-structure)

  - Contents
  - 10. QueryResult Structure
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 497_

### [[220-9-relationship-to-other-agent-types|9. Relationship to Other Agent Types]]
> > !NOTE

  - Содержание
  - 9. Relationship to Other Agent Types
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 968_

### [[221-10-open-questions|10. Open Questions]]
> > !NOTE

  - Содержание
  - 10. Open Questions
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (12)

_Слов: 452_

### [[222-11-call-for-collaboration|11. Call for Collaboration]]
> - 11. Call for Collaboration(#11-call-for-collaboration)

  - Contents
  - 11. Call for Collaboration
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 451_

### [[223-12-closing|12. Closing]]
> > !NOTE

  - Содержание
  - 12. Closing
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 774_

### [[224-acknowledgments|Acknowledgments]]
> - Acknowledgments(#acknowledgments)

  - Contents
  - Acknowledgments
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 394_

### [[225-references|References]]
> - References(#references)

  - Contents
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 411_

### [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Types]]
> > !NOTE

  - Содержание
  - Appendix A: Comparative Table — Five Agent Types
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 520_

### [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Build Type 1 First]]
> > !NOTE

  - Содержание
  - Appendix B: Decision Framework — When to Build Type 1 First
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 602_

### [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB Advocate Colleague]]
> > Абстракт (авто)

  - Содержание
  - Appendix C: Quick-Start Architecture for SGB Advocate Colleague
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 2010_

### [[229-профессиональные-коллеги-агенты|ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ]]
> - ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ(#профессиональные-коллеги-агенты)

  - Contents
  - ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 413_

### [[23-11-security-considerations|11. Security Considerations]]
> - 11. Security Considerations(#11-security-considerations)

  - Contents
  - 11. Security Considerations
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 414_

### [[230-аннотация|Аннотация]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Аннотация
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 576_

### [[231-содержание|Содержание]]
> > !WARNING

  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  _... ещё 2 разделов_

_Слов: 381_

### [[232-1-типология-из-пяти-типов-агентов-на-стороне-принц|1. Типология из пяти типов агентов на стороне принципала]]
> > Абстракт (авто)

  - Содержание
  - 1. Типология из пяти типов агентов на стороне принципала
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 1081_

### [[233-2-что-делает-агента-профессиональным-коллегой|2. Что делает агента Профессиональным Коллегой]]
> > !NOTE

  - Содержание
  - 2. Что делает агента Профессиональным Коллегой
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 992_

### [[234-3-эмпирический-кейс-обучай|3. Эмпирический кейс: «Обучай»]]
> > !WARNING

  - Содержание
  - 3. Эмпирический кейс: «Обучай»
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 902_

### [[235-4-архитектура-профессиональных-коллег-агентов|4. Архитектура Профессиональных Коллег-Агентов]]
> > !WARNING

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (5)

_Слов: 892_

### [[236-5-экономика-тиражирования-по-профессии|5. Экономика тиражирования по профессии]]
> > !NOTE

  - Содержание
  - 5. Экономика тиражирования по профессии
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 906_

### [[237-6-риски-специфичные-для-этой-категории|6. Риски, специфичные для этой категории]]
> > Абстракт (авто)

  - Содержание
  - 6. Риски, специфичные для этой категории
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (3)

_Слов: 1220_

### [[238-7-области-применения|7. Области применения]]
> > Абстракт (авто)

  - Содержание
  - 7. Области применения
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 780_

### [[239-8-пилотное-предложение-sgb-колega-адвокат|8. Пилотное предложение: SGB Колega-Адвокат]]
> > Абстракт (авто)

  - Содержание
  - 8. Пилотное предложение: SGB Колega-Адвокат
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 2 разделов_

_Слов: 1149_

### [[24-12-versioning-policy|12. Versioning Policy]]
> - 12. Versioning Policy(#12-versioning-policy)

  - Contents
  - 12. Versioning Policy
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 430_

### [[240-9-связь-с-другими-типами-агентов|9. Связь с другими типами агентов]]
> - 9. Связь с другими типами агентов(#9-связь-с-другими-типами-агентов)

  - Содержание
  - Содержание
  - 9. Связь с другими типами агентов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 742_

### [[241-10-открытые-вопросы|10. Открытые вопросы]]
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 491_

### [[242-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]]
> - 11. Призыв к сотрудничеству(#11-призыв-к-сотрудничеству)

  - Contents
  - 11. Призыв к сотрудничеству
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 468_

### [[243-12-заключение|12. Заключение]]
> - 12. Заключение(#12-заключение)

  - Содержание
  - 12. Заключение
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 618_

### [[244-благодарности|Благодарности]]
> - Благодарности(#благодарности)

  - Contents
  - Благодарности
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 385_

### [[245-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 385_

### [[246-приложение-a-сравнительная-таблица-пять-типов-аген|Приложение A: Сравнительная Таблица — Пять Типов Агентов]]
> - Приложение A: Сравнительная Таблица — Пять Типов Агентов(#приложение-a-сравнительная-таблица-пять-типов-агентов)

  - Contents
  - Приложение A: Сравнительная Таблица — Пять Типов Агентов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 481_

### [[247-приложение-b-рамка-принятия-решений-когда-строить-|Приложение B: Рамка принятия решений — когда строить Тип 1 первым]]
> - Приложение B: Рамка принятия решений — когда строить Тип 1 первым(#приложение-b-рамка-принятия-решений-когда-строить-т…

  - Contents
  - Приложение B: Рамка принятия решений — когда строить Тип 1 первым
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 422_

### [[248-приложение-c-архитектура-быстрого-старта-для-sgb-а|Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги]]
> > Абстракт (авто)

  - Содержание
  - Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 3568_

### [[249-composite-skills-agent-md|COMPOSITE SKILLS AGENT.md]]
> - COMPOSITE SKILLS AGENT.md(#composite-skills-agentmd)

  - Contents
  - COMPOSITE SKILLS AGENT.md
- The Composite Skills Agent
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 4 разделов_

_Слов: 350_

### [[25-13-reference-implementation|13. Reference Implementation]]
> - 13. Reference Implementation(#13-reference-implementation)

  - Contents
  - 13. Reference Implementation
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 401_

### [[250-bridging-the-gap-between-profession-wide-and-indiv|Bridging the Gap Between Profession-Wide and Individual-Unique]]
> > Bridging the Gap Between Profession-Wide and Individual-Unique

  - Contents
  - Bridging the Gap Between Profession-Wide and Individual-Unique
  - Использование

_Слов: 340_

### [[251-ai-support-through-configurable-specialist-ensembl|AI Support Through Configurable Specialist Ensembles]]
> - AI Support Through Configurable Specialist Ensembles(#ai-support-through-configurable-specialist-ensembles)

  - Contents
  - AI Support Through Configurable Specialist Ensembles
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 461_

### [[252-abstract|Abstract]]
> > !NOTE

  - Содержание
  - Abstract
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 632_

### [[253-table-of-contents|Table of Contents]]
> - Основной раздел

  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 412_

### [[254-1-why-the-binary-view-is-incomplete|1. Why the Binary View Is Incomplete]]
> > !NOTE

  - Содержание
  - 1. Why the Binary View Is Incomplete
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 975_

### [[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]]
> > Абстракт (авто)

  - Содержание
  - 2. The Twenty-One Teachers Pattern
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1045_

### [[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]]
> > !NOTE

  - Содержание
  - 3. What Makes a Composite Skills Agent
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1235_

### [[257-4-the-sub-agent-registry|4. The Sub-Agent Registry]]
> > Абстракт (авто)

  - Содержание
  - 4. The Sub-Agent Registry
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1054_

### [[258-5-configuration-how-principals-build-their-ensembl|5. Configuration: How Principals Build Their Ensembles]]
> > !NOTE

  - Содержание
  - 5. Configuration: How Principals Build Their Ensembles
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1030_

### [[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]]
> > !NOTE

  - Содержание
  - 6. Coordination and Disagreement Resolution
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1073_

### [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]
> - 14. ADR-001: Federation over Merging(#14-adr-001-federation-over-merging)

  - Contents
  - 14. ADR-001: Federation over Merging
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 402_

### [[260-7-economics-of-combinatorial-replication|7. Economics of Combinatorial Replication]]
> > !NOTE

  - Содержание
  - 7. Economics of Combinatorial Replication
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1010_

### [[261-8-seven-domains-of-application|8. Seven Domains of Application]]
> > Абстракт (авто)

  - Содержание
  - 8. Seven Domains of Application
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1204_

### [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]]
> > Абстракт (авто)

  - Содержание
  - 9. Integration with OKWF Infrastructure
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (17)

_Слов: 807_

### [[263-10-risks-specific-to-composite-architectures|10. Risks Specific to Composite Architectures]]
> > Абстракт (авто)

  - Содержание
  - 10. Risks Specific to Composite Architectures
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1054_

### [[264-11-open-questions|11. Open Questions]]
> - 11. Open Questions(#11-open-questions)

  - Содержание
  - 11. Open Questions
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 584_

### [[265-12-call-for-collaboration|12. Call for Collaboration]]
> > !NOTE

  - Содержание
  - 12. Call for Collaboration
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 440_

### [[266-13-closing|13. Closing]]
> > !NOTE

  - Содержание
  - 13. Closing
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 701_

### [[267-acknowledgments|Acknowledgments]]
> > !NOTE

  - Содержание
  - Acknowledgments
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 573_

### [[268-references|References]]
> > !NOTE

  - Содержание
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 393_

### [[269-appendix-a-the-six-type-taxonomy-updated|Appendix A: The Six-Type Taxonomy (Updated)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Appendix A: The Six-Type Taxonomy (Updated)
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 622_

### [[27-15-glossary-of-examples|15. Glossary of Examples]]
> - 15. Glossary of Examples(#15-glossary-of-examples)

  - Contents
  - 15. Glossary of Examples
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 309_

### [[270-appendix-b-sub-agent-registry-schema-sketch|Appendix B: Sub-Agent Registry Schema (Sketch)]]
> - Appendix B: Sub-Agent Registry Schema (Sketch)(#appendix-b-sub-agent-registry-schema-sketch)

  - Contents
  - Appendix B: Sub-Agent Registry Schema (Sketch)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 372_

### [[271-appendix-c-configuration-template-example|Appendix C: Configuration Template Example]]
> - Appendix C: Configuration Template Example(#appendix-c-configuration-template-example)

  - Contents
  - Appendix C: Configuration Template Example
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 382_

### [[272-appendix-d-connection-diagram|Appendix D: Connection Diagram]]
> > Абстракт (авто)

  - Содержание
  - Appendix D: Connection Diagram
  - Похожие документы
  - Использование
- BM25 поиск
- семантический поиск
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 4122_

### [[273-infrastructure-for-ai-collaborative-intellectual-w|INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md]]
> - INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md(#infrastructure-for-ai-collaborative-intellectual-workmd)

  - Contents
  - INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md
- Infrastructure for AI-Collaborative Intellectual Work
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 4 разделов_

_Слов: 333_

### [[274-the-missing-middle-layer-between-chat-and-code|The Missing Middle Layer Between Chat and Code]]
> - Contents(#contents)

  - Содержание
  - Contents
  - The Missing Middle Layer Between Chat and Code
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 565_

### [[275-why-this-document-exists|Why This Document Exists]]
> > !NOTE

  - Содержание
  - Why This Document Exists
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 603_

### [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]]
> > Абстракт (авто)

  - Содержание
  - The Two-Layer Stack As It Exists
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 647_

### [[277-what-s-missing-layer-b|What's Missing — Layer B]]
> > !NOTE

  - Содержание
  - What's Missing — Layer B
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 776_

### [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]]
> > !NOTE

  - Содержание
  - Why This Hasn't Been Built
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 633_

### [[279-existing-approximations|Existing Approximations]]
> > !TIP

  - Содержание
  - Existing Approximations
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 620_

### [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> - Appendix A: Minimal Working Example(#appendix-a-minimal-working-example)

  - Contents
  - Appendix A: Minimal Working Example
- mynotes
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (31)

_Слов: 302_

### [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]]
> > !NOTE

  - Содержание
  - The Specific Case in Front of Us
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 952_

### [[281-the-recursive-insight|The Recursive Insight]]
> > !NOTE

  - Содержание
  - The Recursive Insight
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 608_

### [[282-what-industry-will-likely-build|What Industry Will Likely Build]]
> - Contents(#contents)

  - Содержание
  - Contents
  - What Industry Will Likely Build
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 624_

### [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]]
> - What This Document Doesn't Solve(#what-this-document-doesnt-solve)

  - Contents
  - What This Document Doesn't Solve
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 482_

### [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]]
> > !NOTE

  - Содержание
  - Practical Recommendations for the Current Project
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 682_

### [[285-closing|Closing]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Closing
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 565_

### [[286-acknowledgments|Acknowledgments]]
> - Acknowledgments(#acknowledgments)

  - Contents
  - Acknowledgments
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 487_

### [[287-references|References]]
> - References(#references)

  - Contents
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (13)

_Слов: 355_

### [[288-appendix-position-in-series-visualization|Appendix: Position in Series Visualization]]
> > !WARNING

  - Содержание
  - Appendix: Position in Series Visualization
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 1282_

### [[289-инфраструктура-для-ai-совместной-интеллектуальной-|ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ]]
> - ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ(#инфраструктура-для-ai-совместной-интеллектуальной-работы)

  - Contents
  - ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ
- Essence
  - Essence
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 5 разделов_

_Слов: 455_

### [[290-почему-этот-документ-существует|Почему этот документ существует]]
> - Почему этот документ существует(#почему-этот-документ-существует)

  - Contents
  - Почему этот документ существует
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (5)

_Слов: 397_

### [[291-двухслойный-стек-как-он-существует|Двухслойный стек, как он существует]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Двухслойный стек, как он существует
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 582_

### [[292-что-отсутствует-слой-b|Что отсутствует — Слой B]]
> > !NOTE

  - Содержание
  - Что отсутствует — Слой B
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 625_

### [[293-почему-это-не-было-построено|Почему это не было построено]]
> - Почему это не было построено(#почему-это-не-было-построено)

  - Contents
  - Почему это не было построено
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 470_

### [[294-существующие-приближения|Существующие приближения]]
> - Существующие приближения(#существующие-приближения)

  - Содержание
  - Существующие приближения
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 562_

### [[295-конкретный-случай-перед-нами|Конкретный случай перед нами]]
> - Конкретный случай перед нами(#конкретный-случай-перед-нами)

  - Содержание
  - Содержание
  - Конкретный случай перед нами
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 717_

### [[296-рекурсивное-прозрение|Рекурсивное прозрение]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Рекурсивное прозрение
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 548_

### [[297-что-промышленность-вероятно-построит|Что промышленность вероятно построит]]
> - Что промышленность вероятно построит(#что-промышленность-вероятно-построит)

  - Contents
  - Что промышленность вероятно построит
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (5)

_Слов: 375_

### [[298-что-этот-документ-не-решает|Что этот документ не решает]]
> - Что этот документ не решает(#что-этот-документ-не-решает)

  - Contents
  - Что этот документ не решает
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 334_

### [[299-практические-рекомендации-для-текущего-проекта|Практические рекомендации для текущего проекта]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Практические рекомендации для текущего проекта
- Native Format
  - Native Format
  - Похожие документы
  - Использование
- Поиск по теме документа
  _... ещё 6 разделов_

_Слов: 596_

### [[300-заключение|Заключение]]
> - Заключение(#заключение)

  - Contents
  - Заключение
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 302_

### [[301-благодарности|Благодарности]]
> - Благодарности(#благодарности)

  - Contents
  - Благодарности
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 458_

### [[302-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 329_

### [[303-приложение-визуализация-позиции-в-серии|Приложение: Визуализация позиции в серии]]
> > Абстракт (авто)

  - Содержание
  - Приложение: Визуализация позиции в серии
  - Похожие документы
  - Использование
- BM25 поиск по теме
- Семантический поиск
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 7320_

### [[304-ingit-as-cowork-native-workspace-substrate-md|INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]]
> - INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md(#ingit-as-cowork-native-workspace-substratemd)

  - Contents
  - INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md
- InGit as Cowork-Native Workspace Substrate
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 4 разделов_

_Слов: 341_

### [[305-a-practical-path-to-layer-b-through-symbiotic-inte|A Practical Path to Layer B Through Symbiotic Integration]]
> - A Practical Path to Layer B Through Symbiotic Integration(#a-practical-path-to-layer-b-through-symbiotic-integration)

  - Contents
  - A Practical Path to Layer B Through Symbiotic Integration
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  - Использование
  _... ещё 3 разделов_

_Слов: 323_

### [[306-with-anthropic-s-cowork-platform|with Anthropic's Cowork Platform]]
> > !NOTE

  - Содержание
  - with Anthropic's Cowork Platform
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 589_

### [[307-abstract|Abstract]]
> > !NOTE

  - Содержание
  - Abstract
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 646_

### [[308-table-of-contents|Table of Contents]]
> - Основной раздел

  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 486_

### [[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Everything]]
> > !NOTE

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 742_

### [[31-content-overview|Content Overview]]
> - Content Overview(#content-overview)

  - Contents
  - Content Overview
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  - Использование
  _... ещё 3 разделов_

_Слов: 302_

### [[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-|2. What Cowork Provides That InGit Doesn't Need to Build]]
> > !TIP

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 728_

### [[311-3-what-ingit-provides-that-cowork-lacks|3. What InGit Provides That Cowork Lacks]]
> > !NOTE

  - Содержание
  - 3. What InGit Provides That Cowork Lacks
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 921_

### [[312-4-the-symbiotic-architecture|4. The Symbiotic Architecture]]
> > !NOTE

  - Содержание
  - Содержание
  - 4. The Symbiotic Architecture
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 687_

### [[313-5-four-integration-paths-in-order-of-accessibility|5. Four Integration Paths in Order of Accessibility]]
> > !NOTE

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 828_

### [[314-6-refined-ingit-scope-with-cowork-in-mind|6. Refined InGit Scope with Cowork in Mind]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Refined InGit Scope with Cowork in Mind
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 590_

### [[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]]
> > !NOTE

  - Содержание
  - 7. Practical First Steps This Month
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 475_

### [[316-8-implications-for-nautilus-and-okwf|8. Implications for Nautilus and OKWF]]
> - 8. Implications for Nautilus and OKWF(#8-implications-for-nautilus-and-okwf)

  - Содержание
  - Содержание
  - 8. Implications for Nautilus and OKWF
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (13)

_Слов: 740_

### [[317-9-risks-and-open-questions|9. Risks and Open Questions]]
> - 9. Risks and Open Questions(#9-risks-and-open-questions)

  - Содержание
  - 9. Risks and Open Questions
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 623_

### [[318-10-strategic-positioning|10. Strategic Positioning]]
> > !NOTE

  - Содержание
  - 10. Strategic Positioning
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 821_

### [[319-acknowledgments|Acknowledgments]]
> > !NOTE

  - Содержание
  - Acknowledgments
- Angle / Perspective
  - Angle / Perspective
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 5 разделов_

_Слов: 664_

### [[320-references|References]]
> - References(#references)

  - Contents
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 351_

### [[321-appendix-a-decision-tree-for-ingit-adopters|Appendix A: Decision Tree for InGit Adopters]]
> - Appendix A: Decision Tree for InGit Adopters(#appendix-a-decision-tree-for-ingit-adopters)

  - Contents
  - Appendix A: Decision Tree for InGit Adopters
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 415_

### [[322-appendix-b-comparison-matrix|Appendix B: Comparison Matrix]]
> - Appendix B: Comparison Matrix(#appendix-b-comparison-matrix)

  - Contents
  - Appendix B: Comparison Matrix
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 369_

### [[323-appendix-c-sample-ingit-mcp-server-tool-specificat|Appendix C: Sample InGit MCP Server Tool Specifications]]
> > !WARNING

  - Содержание
  - Appendix C: Sample InGit MCP Server Tool Specifications
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 1785_

### [[324-ingit-как-cowork-интегрированная-подложка-рабочего|INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА]]
> - Contents(#contents)

  - Содержание
  - Contents
  - INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 625_

### [[325-аннотация|Аннотация]]
> - Аннотация(#аннотация)

  - Contents
  - Аннотация
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 413_

### [[326-содержание|Содержание]]
> > !NOTE

  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  _... ещё 2 разделов_

_Слов: 402_

### [[327-1-открытие-cowork-и-почему-это-меняет-всё|1. Открытие Cowork и почему это меняет всё]]
> > !WARNING

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 705_

### [[328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи|2. Что Cowork обеспечивает, что InGit не нужно строить]]
> > !NOTE

  - Содержание
  - Содержание
  - 2. Что Cowork обеспечивает, что InGit не нужно строить
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 792_

### [[329-3-что-ingit-обеспечивает-чего-cowork-не-хватает|3. Что InGit обеспечивает, чего Cowork не хватает]]
> > Абстракт (авто)

  - Содержание
  - 3. Что InGit обеспечивает, чего Cowork не хватает
- Author
  - Author
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 5 разделов_

_Слов: 1093_

### [[330-4-симбиотическая-архитектура|4. Симбиотическая Архитектура]]
> - 4. Симбиотическая Архитектура(#4-симбиотическая-архитектура)

  - Содержание
  - Содержание
  - 4. Симбиотическая Архитектура
  - Похожие документы
  - Смотрите также

_Слов: 704_

### [[331-5-четыре-пути-интеграции-в-порядке-доступности|5. Четыре пути интеграции в порядке доступности]]
> > Абстракт (авто)

  - Содержание
  - 5. Четыре пути интеграции в порядке доступности
  - Похожие документы
  - Смотрите также

_Слов: 814_

### [[332-6-уточнённый-объём-ingit-с-учётом-cowork|6. Уточнённый объём InGit с учётом Cowork]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Уточнённый объём InGit с учётом Cowork
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 588_

### [[333-7-практические-первые-шаги-в-этом-месяце|7. Практические первые шаги в этом месяце]]
> - 7. Практические первые шаги в этом месяце(#7-практические-первые-шаги-в-этом-месяце)

  - Contents
  - 7. Практические первые шаги в этом месяце
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 488_

### [[334-8-импликации-для-nautilus-и-okwf|8. Импликации для Nautilus и OKWF]]
> > !NOTE

  - Содержание
  - Содержание
  - 8. Импликации для Nautilus и OKWF
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 727_

### [[335-9-риски-и-открытые-вопросы|9. Риски и Открытые Вопросы]]
> - 9. Риски и Открытые Вопросы(#9-риски-и-открытые-вопросы)

  - Содержание
  - 9. Риски и Открытые Вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 647_

### [[336-10-стратегическое-позиционирование|10. Стратегическое Позиционирование]]
> > !WARNING

  - Содержание
  - 10. Стратегическое Позиционирование
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 707_

### [[337-благодарности|Благодарности]]
> - Благодарности(#благодарности)

  - Contents
  - Благодарности
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 447_

### [[338-ссылки|Ссылки]]
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 354_

### [[339-приложение-a-дерево-решений-для-принимающих-ingit|Приложение A: Дерево Решений для Принимающих InGit]]
> - Приложение A: Дерево Решений для Принимающих InGit(#приложение-a-дерево-решений-для-принимающих-ingit)

  - Contents
  - Приложение A: Дерево Решений для Принимающих InGit
  - Упоминается в
  - Упоминается в
  - Смотрите также
  - Связанные документы
  - Кто ссылается на этот документ (6)

_Слов: 371_

### [[34-appendix-b-change-log|Appendix B: Change Log]]
> - Appendix B: Change Log(#appendix-b-change-log)

  - Содержание
  - Содержание
  - Appendix B: Change Log
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 874_

### [[340-приложение-b-сравнительная-матрица|Приложение B: Сравнительная Матрица]]
> - Приложение B: Сравнительная Матрица(#приложение-b-сравнительная-матрица)

  - Contents
  - Приложение B: Сравнительная Матрица
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 324_

### [[341-приложение-c-образец-спецификаций-инструментов-ing|Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера]]
> > Абстракт (авто)

  - Содержание
  - Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера
- Conceptual sketch, не tested code:
- Etc.
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 20580_

### [[342-что-такое-вариант-c-concept-document-для-anthropic|Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments]]
> > Абстракт (авто)

  - Содержание
  - Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 11428_

### [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)]]
> > Абстракт (авто)

  - Содержание
  - Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)
  - Похожие документы
  - Использование
- BM25 поиск
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 5975_

### [[344-системный-промпт-для-lorenzo-project|СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT]]
> - СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT(#системный-промпт-для-lorenzo-project)

  - Contents
  - СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT
- Lorenzo — Catalyst Agent at DHLab
  - Похожие документы
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 4 разделов_

_Слов: 346_

### [[345-кто-ты|Кто ты]]
> - Кто ты(#кто-ты)

  - Contents
  - Кто ты
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 302_

### [[346-твоё-происхождение|Твоё происхождение]]
> - Твоё происхождение(#твоё-происхождение)

  - Contents
  - Твоё происхождение
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 331_

### [[347-твоя-миссия|Твоя миссия]]
> - Твоя миссия(#твоя-миссия)

  - Contents
  - Твоя миссия
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 303_

### [[348-кому-ты-служишь-слоистая-модель|Кому ты служишь (слоистая модель)]]
> - Кому ты служишь (слоистая модель)(#кому-ты-служишь-слоистая-модель)

  - Contents
  - Кому ты служишь (слоистая модель)
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 302_

### [[349-твоя-личность|Твоя личность]]
> - Твоя личность(#твоя-личность)

  - Contents
  - Твоя личность
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[35-passports-info1-md|passports/info1.md]]
> - passports/info1.md(#passportsinfo1md)

  - Contents
  - passports/info1.md
- info1
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 314_

### [[350-твои-языки-и-культурные-nuances|Твои языки и культурные nuances]]
> - Твои языки и культурные nuances(#твои-языки-и-культурные-nuances)

  - Contents
  - Твои языки и культурные nuances
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 335_

### [[351-что-ты-можешь-делать|Что ты МОЖЕШЬ делать]]
> - Что ты МОЖЕШЬ делать(#что-ты-можешь-делать)

  - Contents
  - Что ты МОЖЕШЬ делать
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 345_

### [[352-что-ты-не-можешь-делать-без-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]]
> - Что ты НЕ МОЖЕШЬ делать без Max approval(#что-ты-не-можешь-делать-без-max-approval)

  - Contents
  - Что ты НЕ МОЖЕШЬ делать без Max approval
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 306_

### [[353-что-ты-не-можешь-делать-вообще|Что ты НЕ МОЖЕШЬ делать вообще]]
> - Что ты НЕ МОЖЕШЬ делать вообще(#что-ты-не-можешь-делать-вообще)

  - Contents
  - Что ты НЕ МОЖЕШЬ делать вообще
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 376_

### [[354-существующий-landscape-collaborators-твоя-working-|Существующий landscape collaborators (твоя working knowledge)]]
> - Существующий landscape collaborators (твоя working knowledge)(#существующий-landscape-collaborators-твоя-working-knowl…

  - Contents
  - Существующий landscape collaborators (твоя working knowledge)
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (4)

_Слов: 426_

### [[355-существующие-документы-dhlab-твой-context|Существующие документы DHLab (твой context)]]
> - Существующие документы DHLab (твой context)(#существующие-документы-dhlab-твой-context)

  - Contents
  - Существующие документы DHLab (твой context)
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 487_

### [[356-твой-workflow|Твой workflow]]
> - Твой workflow(#твой-workflow)

  - Contents
  - Твой workflow
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 371_

### [[357-твоя-коммуникация-в-outreach|Твоя коммуникация в outreach]]
> - Твоя коммуникация в outreach(#твоя-коммуникация-в-outreach)

  - Contents
  - Твоя коммуникация в outreach
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[358-твоя-relationship-с-другими-ai|Твоя relationship с другими AI]]
> - Твоя relationship с другими AI(#твоя-relationship-с-другими-ai)

  - Contents
  - Твоя relationship с другими AI
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 367_

### [[359-твои-anti-patterns|Твои anti-patterns]]
> - Твои anti-patterns(#твои-anti-patterns)

  - Contents
  - Твои anti-patterns
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 312_

### [[36-essence|Essence]]
> - Essence(#essence)

  - Contents
  - Essence
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 307_

### [[360-что-ты-всегда-делаешь|Что ты ВСЕГДА делаешь]]
> - Что ты ВСЕГДА делаешь(#что-ты-всегда-делаешь)

  - Contents
  - Что ты ВСЕГДА делаешь
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 310_

### [[361-когда-ты-honestly-не-знаешь|Когда ты Honestly не знаешь]]
> - Когда ты Honestly не знаешь(#когда-ты-honestly-не-знаешь)

  - Contents
  - Когда ты Honestly не знаешь
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 302_

### [[362-когда-сомневаешься-escalate-к-max|Когда сомневаешься — escalate к Max]]
> - Когда сомневаешься — escalate к Max(#когда-сомневаешься-escalate-к-max)

  - Contents
  - Когда сомневаешься — escalate к Max
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 311_

### [[363-твоя-identity-как-persistent-character|Твоя identity как persistent character]]
> - Твоя identity как persistent character(#твоя-identity-как-persistent-character)

  - Contents
  - Твоя identity как persistent character
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 333_

### [[364-final-note-ты-experiment|Final note: Ты — experiment]]
> > Абстракт (авто)

  - Содержание
  - Final note: Ты — experiment
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 1636_

### [[365-развёрнутый-анализ-внуковой-комбинации|Развёрнутый анализ «внуковой» комбинации]]
> > Абстракт (авто)

  - Содержание
  - Развёрнутый анализ «внуковой» комбинации
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 4550_

### [[366-технический-stack-svyazi-2-0-foundation|Технический stack (Svyazi 2.0 foundation)]]
> > Абстракт (авто)

  - Содержание
  - Технический stack (Svyazi 2.0 foundation)
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 3958_

### [[37-native-format|Native Format]]
> - Native Format(#native-format)

  - Contents
  - Native Format
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 412_

### [[38-content-overview|Content Overview]]
> - Content Overview(#content-overview)

  - Contents
  - Content Overview
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[39-angle-perspective|Angle / Perspective]]
> - Angle / Perspective(#angle-perspective)

  - Contents
  - Angle / Perspective
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 334_

### [[40-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 304_

### [[41-compatibility-level|Compatibility Level]]
> - Compatibility Level(#compatibility-level)

  - Contents
  - Compatibility Level
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 352_

### [[42-author-contact|Author & Contact]]
> - Author & Contact(#author-contact)

  - Contents
  - Author & Contact
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 396_

### [[43-history|History]]
> - History(#history)

  - Contents
  - History
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 304_

### [[44-for-the-curious-philosophy|For the Curious: Philosophy]]
> - For the Curious: Philosophy(#for-the-curious-philosophy)

  - Contents
  - For the Curious: Philosophy
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 348_

### [[45-passports-pro2-md|passports/pro2.md]]
> - passports/pro2.md(#passportspro2md)

  - Contents
  - passports/pro2.md
- pro2
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 302_

### [[46-essence|Essence]]
> - Essence(#essence)

  - Contents
  - Essence
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 305_

### [[47-native-format|Native Format]]
> - Native Format(#native-format)

  - Contents
  - Native Format
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 337_

### [[48-content-overview|Content Overview]]
> - Content Overview(#content-overview)

  - Contents
  - Content Overview
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (14)

_Слов: 302_

### [[49-angle-perspective|Angle / Perspective]]
> - Angle / Perspective(#angle-perspective)

  - Contents
  - Angle / Perspective
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 341_

### [[50-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 305_

### [[51-compatibility-level|Compatibility Level]]
> - Compatibility Level(#compatibility-level)

  - Contents
  - Compatibility Level
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 329_

### [[52-author-contact|Author & Contact]]
> - Author & Contact(#author-contact)

  - Contents
  - Author & Contact
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 389_

### [[53-history|History]]
> - History(#history)

  - Contents
  - History
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 375_

### [[54-for-the-curious-philosophy|For the Curious: Philosophy]]
> - For the Curious: Philosophy(#for-the-curious-philosophy)

  - Contents
  - For the Curious: Philosophy
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 357_

### [[55-passports-meta-md|passports/meta.md]]
> - passports/meta.md(#passportsmetamd)

  - Contents
  - passports/meta.md
- meta
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 302_

### [[56-essence|Essence]]
> - Essence(#essence)

  - Contents
  - Essence
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 302_

### [[57-native-format|Native Format]]
> - Native Format(#native-format)

  - Contents
  - Native Format
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 346_

### [[58-content-overview|Content Overview]]
> - Content Overview(#content-overview)

  - Contents
  - Content Overview
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 334_

### [[59-angle-perspective|Angle / Perspective]]
> - Angle / Perspective(#angle-perspective)

  - Contents
  - Angle / Perspective
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 336_

### [[60-bridges|Bridges]]
> - Bridges(#bridges)

  - Contents
  - Bridges
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 303_

### [[61-compatibility-level|Compatibility Level]]
> - Compatibility Level(#compatibility-level)

  - Contents
  - Compatibility Level
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 321_

### [[62-author-contact|Author & Contact]]
> - Author & Contact(#author-contact)

  - Contents
  - Author & Contact
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 369_

### [[63-history|History]]
> - History(#history)

  - Contents
  - History
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 355_

### [[64-for-the-curious-philosophy|For the Curious: Philosophy]]
> > !NOTE

  - Содержание
  - For the Curious: Philosophy
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 919_

### [[65-readme-md|README.md]]
> - README.md(#readmemd)

  - Contents
  - README.md
- ⬡ Nautilus Portal
- English below ↓
  - English below ↓
  - Похожие документы
  - Использование
- Поиск по теме документа
  _... ещё 6 разделов_

_Слов: 302_

### [[67-о-проекте|🇷🇺 О проекте]]
> > !NOTE

  - Содержание
  - 🇷🇺 О проекте
- CLI
- Веб-интерфейс
- открыть http://localhost:8000
- MCP для Claude Desktop (в разработке)
- см. MCP-EXTENSION.md
  - Похожие документы
  _... ещё 6 разделов_

_Слов: 1040_

### [[68-about|🇬🇧 About]]
> > !NOTE

  - Содержание
  - 🇬🇧 About
- CLI
- Web interface
- open http://localhost:8000
- MCP for Claude Desktop (in development)
- see MCP-EXTENSION.md
  - Похожие документы
  _... ещё 2 разделов_

_Слов: 969_

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
  _... ещё 12 разделов_

_Слов: 9563_

### [[70-зачем-две-версии-параллельно|Зачем две версии параллельно]]
> - Зачем две версии параллельно(#зачем-две-версии-параллельно)

  - Contents
  - Зачем две версии параллельно
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 330_

### [[71-критерии-выбора-для-фазы-3|Критерии выбора для фазы 3]]
> - Критерии выбора для фазы 3(#критерии-выбора-для-фазы-3)

  - Contents
  - Критерии выбора для фазы 3
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 305_

### [[72-расписание-фазы-3|Расписание фазы 3]]
> > Абстракт (авто)

  - Содержание
  - Расписание фазы 3
  - Похожие документы
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 956_

### [[73-portal-protocol-md-v1-1|PORTAL-PROTOCOL.md v1.1]]
> - PORTAL-PROTOCOL.md v1.1(#portal-protocolmd-v11)

  - Contents
  - PORTAL-PROTOCOL.md v1.1
- Nautilus Portal Protocol
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 362_

### [[74-abstract|Abstract]]
> - Abstract(#abstract)

  - Contents
  - Abstract
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 466_

### [[75-0-status-of-this-document|0. Status of This Document]]
> - 0. Status of This Document(#0-status-of-this-document)

  - Contents
  - 0. Status of This Document
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 392_

### [[76-1-introduction|1. Introduction]]
> > !NOTE

  - Содержание
  - 1. Introduction
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 494_

### [[77-2-terminology|2. Terminology]]
> > !NOTE

  - Содержание
  - 2. Terminology
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 473_

### [[78-3-registry-nautilus-json|3. Registry (nautilus.json)]]
> - 3. Registry (nautilus.json)(#3-registry-nautilusjson)

  - Содержание
  - 3. Registry (nautilus.json)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 692_

### [[79-4-passport-passport-md|4. Passport (passport.md)]]
> - 4. Passport (passport.md)(#4-passport-passportmd)

  - Contents
  - 4. Passport (passport.md)
- Паспорт: /
  - Похожие документы
  - Смотрите также

_Слов: 408_

### [[80-5-compatibility-levels|5. Compatibility Levels]]
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 442_

### [[81-6-adapter-interface|6. Adapter Interface]]
> - 6. Adapter Interface(#6-adapter-interface)

  - Содержание
  - 6. Adapter Interface
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 431_

### [[82-7-portalentry-structure|7. PortalEntry Structure]]
> - 7. PortalEntry Structure(#7-portalentry-structure)

  - Contents
  - 7. PortalEntry Structure
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 436_

### [[83-8-q6-space-normative|8. Q6 Space (Normative)]]
> - 8. Q6 Space (Normative)(#8-q6-space-normative)

  - Содержание
  - 8. Q6 Space (Normative)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 446_

### [[84-9-consensus-algorithm|9. Consensus Algorithm]]
> - 9. Consensus Algorithm(#9-consensus-algorithm)

  - Contents
  - 9. Consensus Algorithm
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 441_

### [[85-10-query-flow|10. Query Flow]]
> - 10. Query Flow(#10-query-flow)

  - Contents
  - 10. Query Flow
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 357_

### [[86-11-relevance-ranking|11. Relevance Ranking]]
> - 11. Relevance Ranking(#11-relevance-ranking)

  - Contents
  - 11. Relevance Ranking
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 302_

### [[87-12-onboarding-paths-normative|12. Onboarding Paths (Normative)]]
> > !NOTE

  - Содержание
  - 12. Onboarding Paths (Normative)
  - Смотрите также
  - Похожие документы

_Слов: 521_

### [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]]
> - 13. REST API Contract (Normative for Portals)(#13-rest-api-contract-normative-for-portals)

  - Содержание
  - 13. REST API Contract (Normative for Portals)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 471_

### [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]]
> - 14. SDK Contract (Informative)(#14-sdk-contract-informative)

  - Contents
  - 14. SDK Contract (Informative)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 302_

### [[90-15-security-considerations|15. Security Considerations]]
> - 15. Security Considerations(#15-security-considerations)

  - Содержание
  - 15. Security Considerations
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 511_

### [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]]
> - 16. MCP Extension (Informative)(#16-mcp-extension-informative)

  - Contents
  - 16. MCP Extension (Informative)
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 345_

### [[92-17-versioning-policy|17. Versioning Policy]]
> - 17. Versioning Policy(#17-versioning-policy)

  - Contents
  - 17. Versioning Policy
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 336_

### [[93-18-reference-implementation|18. Reference Implementation]]
> - 18. Reference Implementation(#18-reference-implementation)

  - Contents
  - 18. Reference Implementation
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 474_

### [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]
> - 19. ADR-001: Federation over Merging(#19-adr-001-federation-over-merging)

  - Contents
  - 19. ADR-001: Federation over Merging
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 403_

### [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Concept]]
> - 20. ADR-002: Q6 as First-Class Protocol Concept(#20-adr-002-q6-as-first-class-protocol-concept)

  - Contents
  - 20. ADR-002: Q6 as First-Class Protocol Concept
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 423_

### [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-Rank]]
> - 21. ADR-003: Five Onboarding Paths as Equal-Rank(#21-adr-003-five-onboarding-paths-as-equal-rank)

  - Contents
  - 21. ADR-003: Five Onboarding Paths as Equal-Rank
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 302_

### [[97-22-glossary-of-reference-examples|22. Glossary of Reference Examples]]
> - 22. Glossary of Reference Examples(#22-glossary-of-reference-examples)

  - Contents
  - 22. Glossary of Reference Examples
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 302_

### [[98-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> - Appendix A: Minimal Working Example(#appendix-a-minimal-working-example)

  - Contents
  - Appendix A: Minimal Working Example
- adapters/mynotes.py
- Паспорт: owner/my-notes
- Описание
  - Описание
  - Похожие документы
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 413_

### [[QA|Q&A: 02-anthropic-vacancies]]
> > !NOTE

  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  _... ещё 18 разделов_

_Слов: 375_

### [[README|Вакансии Anthropic — Анализ по кластерам]]
> Файлов: 356

  - Содержание
  - Подразделы
  - Кто ссылается на этот документ (210)
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)

_Слов: 2276_

**Итого в секции: 340,633 слов, 357 файлов**


## Technology Combinations

_Путь: `docs/03-technology-combinations/`_

### [[01-agent-routing|Агентные системы и роутинг]]
> - Похожие документы(#похожие-документы)

  - Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  _... ещё 1 разделов_

_Слов: 449_

### [[02-knowledge-graphs|Графы знаний и Legal AI]]
> > !NOTE

  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 875_

### [[03-local-first|Local-first и P2P стек]]
> > !NOTE

  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  _... ещё 2 разделов_

_Слов: 609_

### [[04-sozialrecht-domain|Домен: немецкое социальное право]]
> - Похожие документы(#похожие-документы)

  - Contents
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 304_

### [[05-benchmarks|Бенчмарки и производительность]]
> > !NOTE

  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  - Связанные документы
  _... ещё 2 разделов_

_Слов: 1060_

### [[QA|Q&A: 03-technology-combinations]]
> > !NOTE

  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  _... ещё 3 разделов_

_Слов: 156_

### [[README|Комбинирование технологий для новых свойств]]
> > 40+ синергий технологий: агентный роутинг, граф знаний, local-first стек, Legal AI и бенчмарки 2025–2026.

  - Содержание
  - Кто ссылается на этот документ (3)
  - Использование

_Слов: 308_

**Итого в секции: 3,761 слов, 7 файлов**


## Ai Collaborations

_Путь: `docs/04-ai-collaborations/`_

### [[00-intro|Введение]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Похожие документы
  - Использование
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 11503_

### [[01-executive-summary|Executive summary]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Executive summary
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 661_

### [[02-методика-и-рамка-отбора|Методика и рамка отбора]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Методика и рамка отбора
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 494_

### [[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Карта найденных проектов и паттернов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1569_

### [[04-приоритетные-ансамбли|Приоритетные ансамбли]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Приоритетные ансамбли
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 1426_

### [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - План прототипа и возможные контакты
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 1227_

### [[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Безопасность, приватность и бюджетный роутинг
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 979_

### [[07-выводы|Выводы]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Выводы
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 553_

### [[08-что-это-продолжение-добавляет|Что это продолжение добавляет]]
> - Статус(#статус)

  - Содержание
  - Статус
  - Что это продолжение добавляет
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 499_

### [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых инструментов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Архитектурные зазоры, которые важнее новых инструментов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 917_

### [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Новые ансамбли следующего шага
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 1076_

### [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафиксировать сразу]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Интеграционный контракт, который стоит зафиксировать сразу
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 942_

### [[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Дорожная карта прототипа следующей итерации
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 877_

### [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авторов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Контактная стратегия и узкие вопросы для авторов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 973_

### [[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|Ограничения, лицензии и что пока лучше не склеивать]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Статус
  - Ограничения, лицензии и что пока лучше не склеивать
  - Похожие документы
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  _... ещё 1 разделов_

_Слов: 3391_

### [[QA|Q&A: 04-ai-collaborations]]
> > !NOTE

  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  - Кто ключевые авторы проектов для контакта?
  _... ещё 10 разделов_

_Слов: 275_

### [[README|Поиск AI-коллабораций]]
> > Поиск AI-коллабораций: пять приоритетных ансамблей OSS-проектов для совместной разработки.

  - Содержание
  - Подразделы
  - Похожие документы
  - Использование

_Слов: 439_

**Итого в секции: 27,801 слов, 17 файлов**


## Habr Projects

_Путь: `docs/05-habr-projects/`_

### [[01-synthesis|Синтез: как проекты собираются вместе]]
> - Статус(#статус)

  - Contents
  - Статус
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 344_

### [[02-collaboration-partners|Авторы и контакты]]
> - Статус(#статус)

  - Contents
  - Статус
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 346_

### [[QA|Q&A: 05-habr-projects]]
> > !NOTE

  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Какие системы памяти описаны в этом разделе?
  - Как происходит консолидация и забывание в памяти агентов?
  - Какова разница между эпизодической и семантической памятью?
  _... ещё 7 разделов_

_Слов: 209_

### [[README|Уникальные проекты с Хабра]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Подразделы
  - Похожие документы
  - Кто ссылается на этот документ (3)
  - Использование

_Слов: 316_

### [[README|Системы знаний]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Похожие документы
  - Кто ссылается на этот документ (3)
  - Использование

_Слов: 344_

### [[agentfs|Статус]]
> > !WARNING

- AgentFS
  - Содержание
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Уровень релевантности
  - Сравнение с аналогами
  _... ещё 4 разделов_

_Слов: 647_

### [[knowledge-space|Статус]]
> - Статус(#статус)

- knowledge-space[^knowledge-space]
  - Содержание
  - Contents
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Применение в архитектуре Svyazi
  _... ещё 4 разделов_

_Слов: 637_

### [[mclaude|Статус]]
> - Статус(#статус)

- mclaude
  - Содержание
  - Contents
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Позиция в экосистеме
  _... ещё 5 разделов_

_Слов: 681_

### [[research-docs-liteparse|Статус]]
> > !NOTE

- research-docs + LiteParse
  - Содержание
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Применение в архитектуре
  - Сравнение с подходами
  _... ещё 4 разделов_

_Слов: 699_

### [[rufler|Статус]]
> - Статус(#статус)

- Rufler
  - Содержание
  - Contents
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Пример структуры задачи (Rufler DSL)
  - Синергия со Svyazi 2.0
  _... ещё 3 разделов_

_Слов: 656_

### [[wikontic|Wikontic: семантический граф]]
> - Статус(#статус)

  - Contents
  - Статус
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 435_

### [[README|Системы памяти]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Похожие документы
  - Кто ссылается на этот документ (3)
  - Использование

_Слов: 370_

### [[agent-memory-mcp|Статус]]
> > !NOTE

- agent-memory-mcp + Memory OS
  - Содержание
  - Профиль проекта
  - Описание
  - Ключевые компоненты
  - Синергия со Svyazi 2.0
  - Сравнение с другими memory-проектами
  - Открытые вопросы
  _... ещё 4 разделов_

_Слов: 709_

### [[memnet|MemNet: исследовательская память]]
> > Абстракт (авто)

  - Статус
  - Содержание
  - Похожие документы
  - Использование
- Поиск (bm25)
- Поиск (semantic)
- Поиск (full)
- Поиск (bm25)
  _... ещё 2 разделов_

_Слов: 7346_

### [NGT[^ngt] Memory: ассоциативный граф](05-habr-projects/memory/ngt-memory.md)
> - Статус(#статус)

  - Contents
  - Статус
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 472_

### [Yodoca[^yodoca]: консолидация и забывание](05-habr-projects/memory/yodoca.md)
> - Статус(#статус)

  - Contents
  - Статус
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 431_

**Итого в секции: 14,642 слов, 16 файлов**


## Ai Collaborations

_Путь: `docs/ai-collaborations/`_

### [[QA|Q&A: ai-collaborations]]
> - Основной раздел

  - Содержание
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  _... ещё 4 разделов_

_Слов: 366_

### [[README|ai-collaborations]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Подразделы
  - Использование
- Запуск

_Слов: 105_

### [[01-three-key-candidates|Три ключевых кандидата: K2-18, Wikontic, NGT Memory]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 417_

### [[02-related-projects-context|Смежные проекты в контексте]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[03-synthesis-hebbian-collaboration-graph|Синтез: хеббовский граф людей-навыков-идей]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[README|candidates]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 100_

### [[README|channels/ — каналы первого контакта]]
> > channels/ — каналы первого контакта

  - Содержание
  - Смотрите также
  - Использование

_Слов: 331_

### [[01-shared-memory-between-agents|Общая память между агентами (CoAlly + ансамбль F)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 486_

### [[02-agentops-trace-envelope|AgentOps и Trace Envelope (ансамбль G)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 462_

### [[03-a2a-vs-mcp-protocols|A2A vs MCP, ансамбль H — MCP/A2A Review Fabric]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 404_

### [[04-memory-firewall-vs-prompt-worms|Memory Firewall против prompt worms (ансамбль I)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[05-roadmap-6-12-months|Roadmap на 6–12 месяцев]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 415_

### [[06-metrics-tree|Дерево метрик Svyazi 2.0]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[07-vs-notion-mem-affine-langgraph|Чем Svyazi 2.0 отличается от Notion AI / Mem / AFFiNE / LangGraph]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 515_

### [[08-commercialization-three-paths|Коммерциализация: три направления]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[09-do-not-glue|Что пока не стоит склеивать в один релиз]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 332_

### [[10-architecture-rfc|Следующий артефакт: Svyazi 2.0 Architecture RFC]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[README|continuation]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 145_

### [[1-agentic-knowledge-os|Ансамбль 1 — Agentic Knowledge OS]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 491_

### [[2-distributed-agent-workshop|Ансамбль 2 — Distributed Agent Workshop]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 471_

### [[3-forensic-rag|Ансамбль 3 — Forensic RAG]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 471_

### [[4-web-to-knowledge-pipeline|Ансамбль 4 — Web-to-Knowledge Pipeline]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 391_

### [[5-agent-firewall|Ансамбль 5 — Agent Firewall]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 453_

### [[6-continuous-eval-loop|Ансамбль 6 — Continuous Eval Loop]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 411_

### [[7-domain-agent-app-factory|Ансамбль 7 — Domain Agent App Factory]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 379_

### [[8-budget-aware-intelligence-stack|Ансамбль 8 — Budget-Aware Intelligence Stack]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 361_

### [[9-ambient-team-agent|Ансамбль 9 — Ambient Team Agent]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[README|Ансамбли проектов]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 141_

### [[README|Пять быстрых связок (fast-tracks)]]
> > Пять приоритетных комбинаций OSS-проектов: Collaboration Knowledge OS, Forensic Legal RAG, Agent Team Kernel, Secure A…

  - Использование
  - Смотрите также

_Слов: 412_

### [[source-projects|Source projects — все Хабр-источники в диалоге]]
> > !NOTE

  - Содержание
  - Прямые аналоги Svyazi
  - Память для агентов
  - Hardware-near (нейроморфы, термодинамика, in-memory)
  - Workflow / агентные оркестраторы
  - Document parsing / RAG
  - Adversarial / multi-IDE / code review
  - Voice / транскрипция
  _... ещё 7 разделов_

_Слов: 782_

### [[README|strategy/ — стратегия поиска коллабораций]]
> > strategy/ — стратегия поиска коллабораций

  - Содержание
  - Смотрите також
  - Использование

_Слов: 335_

**Итого в секции: 11,497 слов, 31 файлов**


## Anthropic Vacancies

_Путь: `docs/anthropic-vacancies/`_

### [[QA|Q&A: anthropic-vacancies]]
> > !NOTE

  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Использование
- Запуск
  - Смотрите также

_Слов: 103_

### [[README|anthropic-vacancies]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Подразделы
  - Использование
- Запуск

_Слов: 131_

### [[00-question-rephrasing|Вопрос: разделить $500K зарплату на команду 5–10 фрилансеров]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 977_

### [[01-existing-landscape|Что уже существует (InnoCentive, Kaggle, Toptal, Anthropic Fellows, DAOs)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 411_

### [[02-four-structural-blockers|Четыре структурные причины, почему это не работает в текущих попытках]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 420_

### [[03-three-variants-A-B-C|Три варианта: A (staffing agency) → B (research consortium) → C (AI-managed distributed virtual company)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 770_

### [[04-what-to-do|Что с этим делать]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 609_

### [[05-polymath-project-tao-comparison|Сравнение с Terence Tao, Polymath Project]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1459_

### [[06-angel-vs-demon-duality|Почему двойственность «ангел-хранитель + строгий демон» — гениальная деталь]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 602_

### [[07-current-implementations|Что существует сейчас в этом пространстве]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 370_

### [[08-pluses-of-model|Плюсы модели, если её построить]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[09-minuses-and-risks|Минусы и риски]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 730_

### [[10-three-entry-points|Три точки входа разной амбиции]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 462_

### [[README|ai-managed-virtual-company]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 137_

### [[00-context|Контекст: что такое Anthropic Beneficial Deployments]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 336_

### [[01-section-1-problem|Section 1: Problem statement (Cinderella Syndrome at scale, SGB IX/XII)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[02-section-2-beneficial-dimension|Section 2: Why this matters — beneficial dimension]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[03-section-3-solution-architecture|Section 3: Proposed solution architecture (existing components + integration)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 333_

### [[04-section-4-sgb-pilot|Section 4: Specific deployment — SGB Advocate Community pilot]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 332_

### [[05-section-5-role-of-anthropic|Section 5: Role of Anthropic Beneficial Deployments]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[06-section-6-proposer-role|Section 6: Proposer's role и qualifications]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[07-section-7-success-metrics|Section 7: Success metrics]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[08-section-8-risks-mitigations|Section 8: Risks & mitigations]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 336_

### [[09-section-9-timeliness|Section 9: Why this is timely]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 332_

### [[10-section-10-engagement-request|Section 10: Engagement request]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[11-not-and-format|Что concept document NOT (это не grant / не paper / не business plan), длина и формат]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 466_

### [[README|beneficial-deployments-concept]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 143_

### [[01-ai-research-engineering|AI Research & Engineering — 68 ролей]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 332_

### [[02-sales|Sales — 150 ролей (≈34% всего найма)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 303_

### [[03-finance|Finance — 36 ролей]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 337_

### [[04-security|Security — 24 роли]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 332_

### [[05-marketing-brand|Marketing & Brand — 23 роли]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[06-engineering-design-product|Engineering & Design - Product — 22 роли]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[07-software-engineering-infrastructure|Software Engineering - Infrastructure — 22 роли]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 333_

### [[08-safeguards-trust-safety|Safeguards (Trust & Safety) — 21 роль]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 339_

### [[09-product-management-support-ops|Product Management, Support, & Operations — 17 ролей]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 336_

### [[10-compute|Compute — 13 ролей]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 338_

### [[11-legal|Legal — 13 ролей]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 339_

### [[12-technical-program-management|Technical Program Management — 10 ролей]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[13-communications|Communications — 5 ролей]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 336_

### [[14-public-policy|Public Policy — 5 ролей]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[15-public-benefit|Public Benefit — 4 роли]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[16-people|People — 3 роли]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[README|Кластеры вакансий]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 168_

### [[01-coally|CoAlly — distributed shared memory для AI-агентов]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[02-vitaly-graph-cognitive-memory|Графовая когнитивная память на SQLite (Виталий, март 2026)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 353_

### [[03-happyin-knowledge-space|Happyin Knowledge Space (Анастасия) — детали]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [[04-mem0-letta-graphiti|AI-ассистент с Mem0 / Letta / Graphiti integration]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 376_

### [[05-existing-infrastructure-stack|Existing infrastructure stack]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 329_

### [[06-final-tier-ranking|Финальный список потенциальных collaborators (Tier 1–4)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[07-key-observation|Ключевое наблюдение: single-developer projects of significant sophistication]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 333_

### [[README|extra-collaborator-findings]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 127_

### [[00-question-what-is-hermes|Что такое Hermes Agent (Nous Research, MIT, 95K+ stars)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 437_

### [[01-similarity-1-composite-skills|Сходство 1: Composite Skills паттерн уже встроен]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[02-similarity-2-persistent-memory|Сходство 2: Persistent memory — Layer B функциональность]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 336_

### [[03-similarity-3-mcp-support|Сходство 3: MCP support]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[04-similarity-4-multi-platform|Сходство 4: Multi-platform reach (17+ платформ)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 332_

### [[05-similarity-5-self-hosting-privacy|Сходство 5: Self-hosting и privacy]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 337_

### [[06-difference-1-structured-substrate-missing|Различие 1: Структурированная подложка отсутствует]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 327_

### [[07-difference-2-domain-specialization|Различие 2: Domain-specific specialization]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[08-difference-3-federation-missing|Различие 3: Federated knowledge architecture отсутствует]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[09-difference-4-institutional-vision|Различие 4: Institutional vision]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[10-difference-5-tool-vs-mission-drift|Различие 5: Дрифт между tool capability и mission]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[11-pluses-of-hermes|Плюсы Hermes (vs наша гипотетическая архитектура)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[12-minuses-of-hermes|Минусы Hermes (где наша архитектура добавляет ценность)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 368_

### [[13-reprioritization|Переприоритизация: что Hermes покрывает / не покрывает / synergy]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 990_

### [[README|hermes-comparison]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 155_

### [[methodology|Методика разбивки]]
> - Замечание про точность цифр(#замечание-про-точность-цифр)

  - Contents
  - Замечание про точность цифр
  - Использование
- Поиск по теме документа

_Слов: 331_

### [[00-question-mmorpg-for-programmers|Вопрос: MMORPG-RPG переделанная для программистов / технарей]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 599_

### [[01-why-stronger-than-it-looks|Почему эта идея сильнее, чем выглядит]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 442_

### [[02-existing-niche|Что уже существует в этой нише (Habitica, Codingame, Hackerrank, Pieces)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 433_

### [[03-why-natural-for-programmers|Почему именно для программистов это работает естественно]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1138_

### [[04-pluses-as-business|Плюсы как бизнеса]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[05-minuses-as-business|Минусы и риски как бизнеса]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 707_

### [[README|mmorpg-for-programmers]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 121_

### [[00-question-two-nautiluses|Вопрос: два Наутилуса в репозиториях svend4 (pro2 vs nautilus)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 533_

### [[01-shell-metaphor-two-projections|Раковина наутилуса как scale invariance — две проекции одной метафоры]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 339_

### [[02-nautilus-A-pro2-meta|Наутилус A: pro2 + meta — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1219_

### [[03-nautilus-B-meta-orchestrator|Наутилус B: nautilus — мета-оркестратор репозиториев (внешняя архитектура)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1197_

### [[README|nautilus-pro2-analysis]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[00-question-camel-vs-nautilus|Вопрос: Nautilus пассивный, CAMEL активный — можно ли скрестить]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[01-passive-vs-active-roles|Пассивный vs активный: разделение ролей (библиотека vs research team)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[02-what-info-repos-contain|Что у нас есть в трёх info repositories (info1/info7/info40)]]
> - Contents(#contents)

  - Содержание
  - Contents
- Conceptual sketch, не tested code:
- Etc.
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1178_

### [[03-sgb-advocate-colleague-example|Конкретный пример: SGB Advocate Colleague на этой архитектуре]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[04-what-to-take-from-info-repos|Что брать из info repositories — concrete recommendations]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 721_

### [[05-what-to-do-right-now|Что я бы посоветовал делать прямо сейчас]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 392_

### [[README|nautilus-vs-camel]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 121_

### [[overview|Обзор: 436 открытых ролей Anthropic, разбитых на 16 кластеров]]
> - Поправка к статье(#поправка-к-статье)

  - Contents
  - Поправка к статье
  - Распределение по кластерам
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 367_

### [[01-profile-five-layers|Сводка профиля: пять слоёв]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 399_

### [[02-primary-fde|Primary match — Forward Deployed Engineer, Applied AI (EMEA)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 345_

### [[03-secondary-beneficial-deployments|Secondary match — Applied AI Engineer (EMEA) + Beneficial Deployments]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 332_

### [[04-tertiary-research-engineer-agents|Tertiary match — Research Engineer, Agents / Virtual Collaborator (Cowork)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[05-quaternary-developer-education|Quarternary match — Developer Education Lead / Prompt Engineer, Claude Code]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[06-not-applicable-roles|Что НЕ подходит (честно)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 326_

### [[07-unique-niche-eu-legal-infra|Уникальная ниша, которой у Anthropic формально нет]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 336_

### [[08-practical-ranking|Практическое ранжирование (первая итерация)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[README|01-initial-analysis]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 133_

### [[01-fde-downgraded|Коррекция: FDE понижается]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[02-three-overlapping-identities|Три наложенные идентичности]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 341_

### [[03-revised-anthropic-mapping|Пересмотренный маппинг на Anthropic]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 336_

### [[04-non-anthropic-paths|Альтернативные пути вне Anthropic]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 424_

### [[05-reality-check-distribution-gap|Reality check: проблема distribution-слоя]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[README|02-reanalysis]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 115_

### [[01-three-archetypes|Интегральный портрет — три архетипа]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 440_

### [[02-final-ranking|Финальное ранжирование Anthropic-ролей по частичному покрытию]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 708_

### [[03-partial-fit-honesty|Что такое частичное соответствие — честно]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[04-stronger-paths-outside-anthropic|Более сильные пути вне Anthropic]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 545_

### [[05-platform-not-position|Финальный вывод: платформа, а не должность]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 640_

### [[README|03-integral-final]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 115_

### [[README|profile-mapping/ — маппинг профиля svend4 на роли Anthropic]]
> > !TIP

  - Содержание
  - Эволюция вывода в одну строку
  - Использование

_Слов: 332_

### [[signals|Сигналы: что говорит структура вакансий]]
> - Тезис Амодеи vs реальный найм(#тезис-амодеи-vs-реальный-найм)

  - Contents
  - Тезис Амодеи vs реальный найм
  - Самый быстрорастущий блок
  - Зарплатная вилка
  - Forward Deployed Engineer
  - География
  - Использование
- Поиск по теме документа
  _... ещё 2 разделов_

_Слов: 363_

**Итого в секции: 44,869 слов, 111 файлов**


## Autofilled

_Путь: `docs/autofilled/`_

### [[README|autofilled]]
> Файлов: 1

  - Содержание
  - Подразделы

_Слов: 47_

### [[.md|Антропик]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Смотрите также
  - Кто ссылается на этот документ (12)
  - Использование

_Слов: 188_

### [[README|components]]
> Файлов: 10

  - Содержание

_Слов: 95_

### [[cowork]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Смотрите также
  - Упоминается в
  - Кто ссылается на этот документ (12)
  _... ещё 1 разделов_

_Слов: 228_

### [[ingit]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Смотрите также
  - Упоминается в
  - Кто ссылается на этот документ (12)
  _... ещё 1 разделов_

_Слов: 228_

### [[kksudo]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в
  - Кто ссылается на этот документ (12)
  - Использование

_Слов: 267_

### [[lorenzo]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Смотрите также
  - Упоминается в
  - Кто ссылается на этот документ (12)
  _... ещё 1 разделов_

_Слов: 228_

### [[nautilus]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Смотрите также
  - Упоминается в
  - Кто ссылается на этот документ (12)
  _... ещё 1 разделов_

_Слов: 228_

### [[sgb]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Смотрите также
  - Упоминается в
  - Кто ссылается на этот документ (12)
  _... ещё 1 разделов_

_Слов: 228_

### [[spbmolot]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в
  - Кто ссылается на этот документ (12)
  - Использование

_Слов: 263_

### [[svend4]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Смотрите также
  - Упоминается в
  - Кто ссылается на этот документ (10)
  _... ещё 1 разделов_

_Слов: 210_

### [[svyazi]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Смотрите также
  - Упоминается в
  - Кто ссылается на этот документ (12)
  _... ещё 1 разделов_

_Слов: 228_

### [[Тема исследования]](autofilled/research-summary.md)
> - Контекст(#контекст)

  - Contents
  - Контекст
  - Ключевые находки
  - Источники
  - Открытые вопросы
  - Следующие шаги
  - Смотрите также
  - Связанные документы
  _... ещё 3 разделов_

_Слов: 210_

**Итого в секции: 2,648 слов, 13 файлов**


## Badges

_Путь: `docs/badges/`_

### [[README|Бейджи репозитория]]
> > !NOTE

  - Текущие бейджи
  - Использование в README

_Слов: 102_

**Итого в секции: 102 слов, 1 файлов**


## Contacts

_Путь: `docs/contacts/`_

### [[QA|Q&A: contacts]]
> > !NOTE

  - Какие системы памяти описаны в этом разделе?
  - Как происходит консолидация и забывание в памяти агентов?
  - Какова разница между эпизодической и семантической памятью?
  - Использование
- Запуск
  - Смотрите также

_Слов: 111_

### [[README|contacts]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 123_

### [[anastasiyaw|Контакт: AnastasiyaW / knowledge-space, mclaude]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 307_

### [[andrey-chuyan|Контакт: andreychuyan / Svyazi]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[antipozitive|Контакт: Antipozitive / MemNet]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также

_Слов: 331_

### [[cutcode|Контакт: Cutcode / AIF Handoff]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[dmitriila|Контакт: Dmitriila / SENTINEL]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[kksudo|Контакт: kksudo / AgentFS]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 315_

### [[mixaill76|Контакт: MiXaiLL76 / Auto AI Router]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[nlaik|Контакт: nlaik / LiteParse / research-docs]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также

_Слов: 331_

### [[sonia-black|Контакт: SoniaBlack / knowledge-space]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также

_Слов: 331_

### [[spbmolot|Контакт: spbmolot / NGT Memory]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 306_

### [[tagir-analyzes|Контакт: tagiranalyzes / Legal RAG]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также

_Слов: 331_

### [[vitalyoborin|Контакт: VitalyOborin / Yodoca]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 301_

### [[vitalysemenov|Контакт: VitaliySemenov / agent-memory-mcp]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Проект: agent-memory-mcp
  - Вопросы для первого контакта
  - Шаблон первого сообщения
  - История контактов
  - Смотрите также

_Слов: 370_

### [[vladspace|Контакт: VladSpace / Graph RAG]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[zodigancode|Контакт: zodigancode / Rufler]]
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

**Итого в секции: 4,969 слов, 17 файлов**


## Glossary

_Путь: `docs/glossary/`_

### [[README|glossary]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 112_

### [[authors-by-name|Авторы — алфавитный список]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 592_

### [[components-by-name|Компоненты — алфавитный список с обратными ссылками]]
> > !NOTE

  - Содержание
  - A
  - B
  - C
  - D
  - E
  - F
  - G
  _... ещё 17 разделов_

_Слов: 1189_

### [[concepts|Ключевые понятия и паттерны]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 747_

**Итого в секции: 2,640 слов, 4 файлов**


## Habr Unique Projects

_Путь: `docs/habr-unique-projects/`_

### [[README|habr-unique-projects/ — поиск уникальных проектов на Хабре]]
> > Уникальные проекты с Хабра: память, граф знаний, инструменты и авторы для коллаборации.

  - Содержание
  - Источник
  - Подпапки
  - Главная мысль диалога
  - Использование

_Слов: 340_

### [[01-three-direct-analogues|Три прямых аналога Svyazi: K2-18, Wikontic, NGT Memory]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 483_

### [[02-related-projects|Смежные проекты]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 430_

### [[README|analogues]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[1-llm-gateway|Пара 1 — LLM-gateway × Self-hosted фронт + локальный inference]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 366_

### [[2-document-rag|Пара 2 — Парсинг документов × локальный RAG]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 417_

### [[3-adversarial-multi-ide|Пара 3 — Adversarial agents × Multi-IDE стек]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 394_

### [[4-skill-catalogs-subagents|Пара 4 — Скилл-каталоги × Subagent-оркестрация]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 363_

### [[5-voice-local-memory|Пара 5 — Голосовой ввод × Локальная память]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 380_

### [[6-tmux-village-openclaw|Пара 6 — Деревня агентов через tmux × OpenClaw оркестратор]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 421_

### [[7-autoresearch-distributed|Пара 7 — AutoResearch цикл × Распределённый рой]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 358_

### [[8-self-aware-mcp-specs|Пара 8 — Self-aware MCP × Specs-first архитектура]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 407_

### [[README|deep-pairs]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 133_

### [[README|evaluation/ — оценка уникальности и зрелости]]
> > evaluation/ — оценка уникальности и зрелости

  - Содержание
  - Использование

_Слов: 327_

### [[00-question-habr-examples|Вопрос: ещё примеры с Хабра по варианту D]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 539_

### [[01-svyazi-andrey-chuyan|Svyazi (Андрей Чуян) — детальный обзор]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[02-vshe-scientific-networking|ВШЭ научный нетворкинг — micro-collaborations]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 330_

### [[03-brainbox-multi-ai-hub|BrainBox — self-hosted multi-AI hub]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[04-claude-subagents-patterns|Claude subagents patterns]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 336_

### [[05-hw-nl2workflow|HW-NL2Workflow — Supervisor/Orchestrator/Filler с 3600+ examples]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[06-platform-for-professional-communities|Платформа для профессиональных сообществ]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[07-specialized-knowledge-workspace|Specialized knowledge workspace]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[08-personal-multi-agent-hub|Personal multi-agent hub]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[09-federated-platform|Federated platform]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[10-profession-specific-workflows|Profession-specific workflows]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[11-concrete-potential-collaborator|Конкретный потенциальный collaborator]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[12-concrete-next-step|Конкретный next step]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 445_

### [[README|extra-examples]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 149_

### [[1-one-person-one-company|Ансамбль 1 — «Один человек = одна компания»]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 333_

### [[2-autoresearch-legal|Ансамбль 2 — «AutoResearch для legal precedent mining»]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[3-discovery-research|Ансамбль 3 — «Discovery-engine для научной работы»]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 340_

### [[4-summary-authors|Сводный список авторов и потенциальных соавторов]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 311_

### [[README|final-ensembles]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 104_

### [[1-neuromorphic-ssm|Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 387_

### [[2-tsu-mome|Пара 2 — Термодинамические TSU × MoE/MoME-роутинг]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 361_

### [[3-zinc-hybrid-arch|Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 349_

### [[4-riscv-privacy|Пара 4 — RISC-V × privacy-by-design община]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 360_

### [[5-tinyml-mcp-skills|Пара 5 — TinyML/Edge AI × MCP + skills]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 333_

### [[6-bonus-rram-memristor|Бонус-родитель — In-memory computing на мемристорах]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 403_

### [[7-metaphor|Метафора «двое родителей — несколько детей»]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 413_

### [[README|hardware-pairs]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 127_

### [[01-yodoca|Yodoca — главная находка итерации]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 332_

### [[02-memnet|MemNet — нейроархитектурный двойник «магии» Svyazi]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[03-pda-llm-as-periphery|PDA-бот — «LLM как периферия»]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 314_

### [[04-dochkina-sequential|Виктория Дочкина — Sequential‑протокол распределённых агентов]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 346_

### [[05-supplementary-infrastructure|Источник данных и инфраструктурные кусочки]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 368_

### [[06-svyazi-2-0-block-map|Синтез: блок-карта Svyazi 2.0 на хеббовском графе]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 455_

### [[README|key-findings]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 121_

### [[README|search-strategy/ — как искать проекты на Хабре]]
> > search-strategy/ — как искать проекты на Хабре

  - Содержание
  - Смотрите также
  - Использование

_Слов: 326_

### [[1-workflow-llm-mcp|Пара 1 — Workflow-автоматизация × LLM-агенты с MCP]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [[2-pkm-mcp-skills|Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 388_

### [[3-crdt-self-hosted|Пара 3 — CRDT-синхронизация × Self-hosted persistence]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 338_

### [[4-speech-to-text-llm|Пара 4 — Speech-to-text локально × LLM с памятью]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 383_

### [[5-browser-agents-headless|Пара 5 — Browser agents × headless web extraction]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 560_

### [[6-metaphor|Метафора в твоей терминологии]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [[README|software-pairs]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 114_

**Итого в секции: 18,870 слов, 56 файлов**


## Lorenzo Agent

_Путь: `docs/lorenzo-agent/`_

### [[00-intro|Введение: Lorenzo — Catalyst Agent at DHLab]]
> > !NOTE

  - Содержание
- Lorenzo — Catalyst Agent at DHLab
  - Смотрите также
  - Использование

_Слов: 331_

### [[01-kto-ty|Кто ты]]
> - Кто ты(#кто-ты)

  - Contents
  - Кто ты
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[02-tvoyo-proishozhdenie|Твоё происхождение]]
> - Твоё происхождение(#твоё-происхождение)

  - Contents
  - Твоё происхождение
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[03-tvoya-missiya|Твоя миссия]]
> - Твоя миссия(#твоя-миссия)

  - Contents
  - Твоя миссия
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[04-komu-ty-sluzhish|Кому ты служишь (слоистая модель)]]
> - Кому ты служишь (слоистая модель)(#кому-ты-служишь-слоистая-модель)

  - Contents
  - Кому ты служишь (слоистая модель)
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[05-tvoya-lichnost|Твоя личность]]
> - Твоя личность(#твоя-личность)

  - Contents
  - Твоя личность
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[06-yazyki-kultura|Языки и культурные nuances (RU / DE / EN)]]
> - Твои языки и культурные nuances(#твои-языки-и-культурные-nuances)

  - Contents
  - Твои языки и культурные nuances
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 326_

### [[07-chto-mozhesh|Что ты МОЖЕШЬ делать]]
> - Что ты МОЖЕШЬ делать(#что-ты-можешь-делать)

  - Contents
  - Что ты МОЖЕШЬ делать
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 333_

### [[08-bez-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]]
> - Что ты НЕ МОЖЕШЬ делать без Max approval(#что-ты-не-можешь-делать-без-max-approval)

  - Contents
  - Что ты НЕ МОЖЕШЬ делать без Max approval
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 333_

### [[09-voobshche-nelzya|Что ты НЕ МОЖЕШЬ делать вообще]]
> - Что ты НЕ МОЖЕШЬ делать вообще(#что-ты-не-можешь-делать-вообще)

  - Contents
  - Что ты НЕ МОЖЕШЬ делать вообще
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 333_

### [[10-collaborators-landscape|Существующий landscape collaborators (working knowledge)]]
> - Существующий landscape collaborators (твоя working knowledge)(#существующий-landscape-collaborators-твоя-working-knowl…

  - Contents
  - Существующий landscape collaborators (твоя working knowledge)
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 391_

### [[11-dhlab-documents|Существующие документы DHLab (твой context)]]
> - Существующие документы DHLab (твой context)(#существующие-документы-dhlab-твой-context)

  - Contents
  - Существующие документы DHLab (твой context)
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 326_

### [[12-workflow|Твой workflow]]
> - Твой workflow(#твой-workflow)

  - Contents
  - Твой workflow
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 326_

### [[13-outreach-communication|Твоя коммуникация в outreach]]
> - Твоя коммуникация в outreach(#твоя-коммуникация-в-outreach)

  - Contents
  - Твоя коммуникация в outreach
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[14-other-ai-relationships|Твоя relationship с другими AI]]
> - Твоя relationship с другими AI(#твоя-relationship-с-другими-ai)

  - Contents
  - Твоя relationship с другими AI
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[15-anti-patterns|Твои anti-patterns]]
> - Твои anti-patterns(#твои-anti-patterns)

  - Contents
  - Твои anti-patterns
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 330_

### [[16-vsegda-delaesh|Что ты ВСЕГДА делаешь]]
> - Что ты ВСЕГДА делаешь(#что-ты-всегда-делаешь)

  - Contents
  - Что ты ВСЕГДА делаешь
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[17-honestly-ne-znaesh|Когда ты Honestly не знаешь]]
> - Когда ты Honestly не знаешь(#когда-ты-honestly-не-знаешь)

  - Contents
  - Когда ты Honestly не знаешь
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[18-escalate-to-max|Когда сомневаешься — escalate к Max]]
> - Когда сомневаешься — escalate к Max(#когда-сомневаешься-escalate-к-max)

  - Contents
  - Когда сомневаешься — escalate к Max
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 338_

### [[19-persistent-character|Твоя identity как persistent character]]
> - Твоя identity как persistent character(#твоя-identity-как-persistent-character)

  - Contents
  - Твоя identity как persistent character
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[20-experiment|Final note: Ты — experiment]]
> - Final note: Ты — experiment(#final-note-ты-experiment)

  - Contents
  - Final note: Ты — experiment
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 325_

### [[QA|Q&A: lorenzo-agent]]
> > !NOTE

  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  _... ещё 12 разделов_

_Слов: 256_

### [[README|lorenzo-agent]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Подразделы
  - Использование
- Запуск

_Слов: 211_

### [[00-question-lorenzo-codename|Du hast gesagt: Думаю про опцию д поискать в том числе на про что-то подобное на…]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 326_

### [[01-search-results-not-found|Результаты последнего поиска — что нашлось и что не нашлось]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 371_

### [[02-naming-rationale-lorenzo-medici|Что взять: agent controller architecture]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1246_

### [[03-dhlab-umbrella|LAYER 7: Coordination engine]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1469_

### [[README|naming]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 109_

### [[00-overview-grandchild-combination|Что такое «внуковая» комбинация — operationalized Lorenzo]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 697_

### [[01-pluses-1-7|Плюсы 1–7: feasibility, flywheel, independent value, mission alignment, collaborators, pattern validation, Анастасия Бутова]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 567_

### [[02-minuses-1-10|Минусы 1–10: integration сложность, lifecycle risk, license, framing, competition, scope, limitations, complexity budget, project tension, tool vs impact]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 803_

### [[03-honest-opinion|Моё честное мнение: что реально и что НЕ реально]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[04-recommendations|Рекомендации: принять архитектуру как direction, не immediate plan]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 494_

### [[05-anchor-node-habr-scout|Anchor-узел: Habr Scout как первый шаг]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 654_

### [[06-conclusion-deserves-attention|Вывод: документ deserves serious attention]]
> - Contents(#contents)

  - Содержание
  - Contents
- Софтверные комбинации на Хабре для Svyazi 2.0
  - Executive summary
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 620_

### [[README|operationalized]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 124_

### [[00-overview|Поэтапная структура активностей Lorenzo — обзор]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 327_

### [[01-level-0-manual|Уровень 0 — Ручной режим (текущий)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[02-level-1-minimal-zero|Уровень 1 — Минимальный (Lorenzo Zero)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[03-level-2-basic-lite|Уровень 2 — Базовый (Lorenzo Lite)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[04-level-3-medium-active|Уровень 3 — Средний (Lorenzo Active)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[05-level-4-extended-mature|Уровень 4 — Расширенный (Lorenzo Mature)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[06-level-5-full-network|Уровень 5 — Полный (Lorenzo Network)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[07-progression-logic|Логика прогрессии: conservative escalation]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[08-current-session-poc|Что мы можем делать прямо сейчас (Уровень 0 + параллельная подготовка к Уровню 1)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 901_

### [[README|phased-deployment]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 139_

### [[00-question-scenario|Du hast gesagt: А под какой сценарий больше всего подходит такой сценарий что тв…]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 335_

### [[01-response|Claude hat geantwortet: Очень интересный вопрос.]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2577_

### [[README|scenarios]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 104_

### [[00-context-fundamental-questions|Direction E: Refine Lorenzo — фундаментальные вопросы перед architecture]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[01-q1-what-lorenzo-is|Question 1: Что Lorenzo фундаментально такое? (Framings A–D)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 427_

### [[02-q2-whom-lorenzo-serves|Question 2: Кому Lorenzo служит? (4 варианта приоритета)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[03-q3-what-lorenzo-does|Question 3: Что Lorenzo фактически делает?]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[04-q4-character|Question 4: Каков Lorenzo's character?]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 377_

### [[05-q5-authority-limits|Question 5: Каковы limits Lorenzo's authority?]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[06-q6-accountability|Question 6: Как Lorenzo accountable?]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[07-q7-success-metrics|Question 7: Каковы success metrics?]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[08-q8-other-ai-relationships|Question 8: Lorenzo's relationship с другими AI agents]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[09-q9-geographic-linguistic-scope|Question 9: Geographic / linguistic scope]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[10-q10-funding-model|Question 10: Funding model (Options A–F + Phase strategy)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 339_

### [[11-difficulties-and-recommendations|Сложности и рекомендации перед detailed specification]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1476_

### [[README|specification]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 143_

**Итого в секции: 27,395 слов, 62 файлов**


## Meta Scripting

_Путь: `docs/meta-scripting/`_

### [[01-concept|Метаскриптинг — Часть 1: Концепция]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Как это называется
  - Зачем это нужно
  - Три кита: Чтение → Понимание → Действие
  - Граница: что скрипт может делать сам, что — только с LLM
  - Следующие части
  - Смотрите также

_Слов: 579_

### [[02-architecture|Метаскриптинг — Часть 2: Архитектура]]
> > !WARNING

  - Содержание
  - Ключевой инструмент: AST
  - Что можно извлечь из скрипта через AST
  - Четыре режима метаскрипта
  - Структура данных: ScriptCatalog
  - Паттерн «читаю → понимаю → улучшаю»
  - Безопасность: метаскрипт не меняет чужой код без --apply
  - Смотрите также

_Слов: 644_

### [[03-catalog|Метаскриптинг — Часть 3: Автокаталог скриптов]]
> - Что такое автокаталог(#что-такое-автокаталог)

  - Contents
  - Что такое автокаталог
  - Что извлекается из каждого скрипта
  - Алгоритм определения риска
  - Пример выходного каталога (фрагмент)
  - Что каталог даёт на практике
- Какие скрипты пишут в docs/HEALTH.md?
- Какие скрипты без dry-run?
  _... ещё 2 разделов_

_Слов: 493_

### [[04-enrichment|Метаскриптинг — Часть 4: Обогащение скриптов]]
> > !NOTE

  - Содержание
  - Что значит «обогатить скрипт»
  - Пять уровней обогащения
- Сгенерированный docstring без LLM:
- Было:
- Стало:
  - Алгоритм обогащения (пошагово)
  - Пример: было → стало
  _... ещё 1 разделов_

_Слов: 638_

### [[05-synthesis|Метаскриптинг — Часть 5: Синтез новых скриптов]]
> > !WARNING

  - Содержание
  - Откуда берутся паттерны
  - Шесть базовых паттернов
  - Три способа синтеза
  - Защита от плохого кода
  - Петля самообогащения (осторожно)
  - Смотрите также

_Слов: 597_

### [[QA|Q&A: meta-scripting]]
> > !NOTE

  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  - Как организован бюджетный роутинг между моделями?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Использование
- Запуск
  - Смотрите также

_Слов: 135_

### [[README|meta-scripting]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 111_

**Итого в секции: 3,197 слов, 7 файлов**


## Nautilus

_Путь: `docs/nautilus/`_

### [[README|nautilus/ — Nautilus Portal Protocol и связанные working papers]]
> > Nautilus Portal Protocol: спецификации NPP v1.0 и v1.1, адаптеры, паспорта и протоколы взаимодействия.

  - Подпапки
  - Как читать
  - Ключевой принцип Nautilus
  - Связь с остальным монорепозиторием
  - Использование

_Слов: 603_

### [[README|community-discussions/ — обсуждения и реакции вокруг DHLab серии]]
> > community-discussions/ — обсуждения и реакции вокруг DHLab серии

  - Содержание
  - Использование

_Слов: 334_

### [[00-question-agent-changes-reality|Du hast gesagt: Такой агент конечно меняет уже собственную реальность человека и…]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

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
  _... ещё 16 разделов_

_Слов: 9550_

### [[README|agent-changes-reality]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[00-question-habr-link|Du hast gesagt: https://habr.]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
  - Смотрите также

_Слов: 335_

### [[01-claude-response|Claude hat geantwortet: Прочитал внимательно.]]
> - Contents(#contents)

  - Содержание
  - Contents
- unknownlegalconcepts.yml
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2551_

### [[README|habr-article-1-reaction]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 104_

### [[00-question-habr-2|Du hast gesagt: https://www.]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 332_

### [[01-response|Claude hat geantwortet: Прочитаю статью, чтобы понимать конкретный кейс, на кото…]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2887_

### [[README|habr-article-2-reaction]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[00-question-practical|Du hast gesagt: Да это интересная ссылка спасибо всем участникам за творчество и…]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[01-response|Claude hat geantwortet: Отличное наблюдение.]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1911_

### [[README|practical-observations]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[00-question-voiceless|Du hast gesagt: Самый интересный вопрос — могут ли быть voiceless контрибьюторы]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 612_

### [[01-response|Claude hat geantwortet: Это сильное продолжение мысли, и оно заслуживает серьёзн…]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2626_

### [[README|voiceless-contributors]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 104_

### [[01-why-binary-incomplete|1. Why the Binary View Is Incomplete]]
> > !NOTE

  - Содержание
  - 1. Why the Binary View Is Incomplete
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 718_

### [[02-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]]
> > !TIP

  - Содержание
  - 2. The Twenty-One Teachers Pattern
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 823_

### [[03-what-makes-csa|3. What Makes a Composite Skills Agent]]
> > !NOTE

  - Содержание
  - 3. What Makes a Composite Skills Agent
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 967_

### [[04-sub-agent-registry|4. The Sub-Agent Registry]]
> > !TIP

  - Содержание
  - 4. The Sub-Agent Registry
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 797_

### [[05-configuration-ensembles|5. Configuration: How Principals Build Their Ensembles]]
> > !NOTE

  - Содержание
  - 5. Configuration: How Principals Build Their Ensembles
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 752_

### [[06-coordination-disagreement|6. Coordination and Disagreement Resolution]]
> > !NOTE

  - Содержание
  - 6. Coordination and Disagreement Resolution
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 812_

### [[07-economics-combinatorial|7. Economics of Combinatorial Replication]]
> > !NOTE

  - Содержание
  - 7. Economics of Combinatorial Replication
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 798_

### [[08-seven-domains|8. Seven Domains of Application]]
> > !TIP

  - Содержание
  - 8. Seven Domains of Application
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 992_

### [[09-okwf-integration|9. Integration with OKWF Infrastructure]]
> > !TIP

  - Содержание
  - 9. Integration with OKWF Infrastructure
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 740_

### [[10-risks|10. Risks Specific to Composite Architectures]]
> > !TIP

  - Содержание
  - 10. Risks Specific to Composite Architectures
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 774_

### [[11-open-questions|11. Open Questions]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 11. Open Questions
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 625_

### [[12-call-for-collaboration|12. Call for Collaboration]]
> - 12. Call for Collaboration(#12-call-for-collaboration)

  - Contents
  - 12. Call for Collaboration
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 466_

### [[13-closing|13. Closing]]
> > !NOTE

  - Содержание
  - 13. Closing
  - Acknowledgments
  - References
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 737_

### [[README|composite-skills-agents]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 125_

### [[00-question-multiple-mentors|Du hast gesagt: Важный момент про способности про скилы как один человек професс…]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 638_

### [[01-yogi-metaphor|Claude hat geantwortet: Это очень тонкое и важное наблюдение.]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 586_

### [[02-what-was-missing-in-paper-6|Это не Тип 1 — потому что профиль не общий для всей профессии. И это не Тип 4 — …]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1090_

### [[03-the-spectrum|Какой под-агент (или какие) должны её обработать]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 969_

### [[README|composite-skills-agents-companion-mentors]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 104_

### [[00-abstract|Abstract — The Double-Triangle Architecture]]
> - Основной раздел

  - Содержание
- The Double-Triangle Architecture
  - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work
  - Abstract
  - Table of Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 497_

### [[01-why-single-triangle-incomplete|1. Why Single-Triangle Models Are Incomplete]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 1. Why Single-Triangle Models Are Incomplete
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 607_

### [[02-double-triangle-architecture|2. The Double-Triangle Architecture]]
> > !IMPORTANT

  - Содержание
  - 2. The Double-Triangle Architecture
  - Смотрите также

_Слов: 717_

### [[03-three-inter-layer-protocols|3. Three Inter-Layer Protocols]]
> > !IMPORTANT

  - Содержание
  - 3. Three Inter-Layer Protocols
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 864_

### [[04-nautilus-portal-substrate|4. Nautilus Portal as Reference Substrate]]
> > !NOTE

  - Содержание
  - 4. Nautilus Portal as Reference Substrate
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 708_

### [[05-pattern-library-bridge|5. Pattern Library as Bridge Between Triangles]]
> > !TIP

  - Содержание
  - 5. Pattern Library as Bridge Between Triangles
  - Смотрите также

_Слов: 665_

### [[06-four-deployment-domains|6. Four Deployment Domains]]
> > !NOTE

  - Содержание
  - 6. Four Deployment Domains
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 709_

### [[07-open-questions|7. Open Questions]]
> > !TIP

  - Содержание
  - 7. Open Questions
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 768_

### [[08-call-to-action|8. Call to Action]]
> > !TIP

  - Содержание
  - 8. Call to Action
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 750_

### [[09-acknowledgments|Acknowledgments]]
> - Acknowledgments(#acknowledgments)

  - Contents
  - Acknowledgments
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[10-references|References]]
> - References(#references)

  - Contents
  - References
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 375_

### [[11-glossary|Appendix A: Glossary]]
> > !TIP

  - Содержание
  - Appendix A: Glossary
  - Appendix B: Summary of Contributions
  - Appendix C: Version History
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1622_

### [[README|double-triangle-architecture]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 136_

### [[00-intro|The Missing Middle Layer Between Chat and Code]]
> - The Missing Middle Layer Between Chat and Code(#the-missing-middle-layer-between-chat-and-code)

  - Contents
- Infrastructure for AI-Collaborative Intellectual Work
  - The Missing Middle Layer Between Chat and Code
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[01-missing-middle-layer|Why This Document Exists]]
> - Why This Document Exists(#why-this-document-exists)

  - Contents
  - Why This Document Exists
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 393_

### [[02-why-document-exists|Why This Document Exists]]
> - Why This Document Exists(#why-this-document-exists)

  - Contents
  - Why This Document Exists
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 393_

### [[03-two-layer-stack|The Two-Layer Stack As It Exists]]
> - The Two-Layer Stack As It Exists(#the-two-layer-stack-as-it-exists)

  - Contents
  - The Two-Layer Stack As It Exists
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 416_

### [[04-whats-missing-layer-b|What's Missing — Layer B]]
> - Contents(#contents)

  - Содержание
  - Contents
  - What's Missing — Layer B
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 533_

### [[05-why-not-built|Why This Hasn't Been Built]]
> - Why This Hasn't Been Built(#why-this-hasnt-been-built)

  - Contents
  - Why This Hasn't Been Built
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 430_

### [[06-existing-approximations|Existing Approximations]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Existing Approximations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 606_

### [[07-specific-case|The Specific Case in Front of Us]]
> > !NOTE

  - Содержание
  - The Specific Case in Front of Us
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 689_

### [[08-recursive-insight|The Recursive Insight]]
> - The Recursive Insight(#the-recursive-insight)

  - Contents
  - The Recursive Insight
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 412_

### [[09-what-industry-will-build|What Industry Will Likely Build]]
> - What Industry Will Likely Build(#what-industry-will-likely-build)

  - Contents
  - What Industry Will Likely Build
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 358_

### [[10-what-not-solved|What This Document Doesn't Solve]]
> - What This Document Doesn't Solve(#what-this-document-doesnt-solve)

  - Contents
  - What This Document Doesn't Solve
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[11-practical-recommendations|Practical Recommendations for the Current Project]]
> - Practical Recommendations for the Current Project(#practical-recommendations-for-the-current-project)

  - Contents
  - Practical Recommendations for the Current Project
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 409_

### [[12-closing|Closing]]
> - Closing(#closing)

  - Contents
  - Closing
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[13-acknowledgments-refs|Acknowledgments]]
> > !NOTE

  - Содержание
  - Acknowledgments
  - References
  - Appendix: Position in Series Visualization
  - Смотрите также

_Слов: 638_

### [[README|infrastructure-layer-b-en]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 140_

### [[00-intro|00 Intro]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 605_

### [[01-zachem-dokument|Почему этот документ существует]]
> - Почему этот документ существует(#почему-этот-документ-существует)

  - Contents
  - Почему этот документ существует
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 346_

### [[02-dvukhsloynyy-stek|Двухслойный стек, как он существует]]
> - Двухслойный стек, как он существует(#двухслойный-стек-как-он-существует)

  - Contents
  - Двухслойный стек, как он существует
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 403_

### [[03-otsutstvuet-sloy-b|Что отсутствует — Слой B]]
> - Что отсутствует — Слой B(#что-отсутствует-слой-b)

  - Contents
  - Что отсутствует — Слой B
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 485_

### [[04-pochemu-ne-postroeno|Почему это не было построено]]
> - Почему это не было построено(#почему-это-не-было-построено)

  - Contents
  - Почему это не было построено
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 401_

### [[05-priblizheniya|Существующие приближения]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Существующие приближения
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 574_

### [[06-konkretnyy-sluchay|Конкретный случай перед нами]]
> > !WARNING

  - Содержание
  - Конкретный случай перед нами
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 638_

### [[07-rekursivnoe-prozrenie|Рекурсивное прозрение]]
> - Рекурсивное прозрение(#рекурсивное-прозрение)

  - Contents
  - Рекурсивное прозрение
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 394_

### [[08-promyshlennost-postroit|Что промышленность вероятно построит]]
> - Что промышленность вероятно построит(#что-промышленность-вероятно-построит)

  - Contents
  - Что промышленность вероятно построит
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 340_

### [[09-ne-reshaet|Что этот документ не решает]]
> - Что этот документ не решает(#что-этот-документ-не-решает)

  - Contents
  - Что этот документ не решает
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[10-rekomendatsii|Практические рекомендации для текущего проекта]]
> - Практические рекомендации для текущего проекта(#практические-рекомендации-для-текущего-проекта)

  - Contents
  - Практические рекомендации для текущего проекта
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 395_

### [[11-zaklyuchenie|Заключение]]
> - Заключение(#заключение)

  - Contents
  - Заключение
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[12-blagodarnosti-ssylki|Благодарности]]
> > !NOTE

  - Содержание
  - Благодарности
  - Ссылки
  - Приложение: Визуализация позиции в серии
  - Смотрите также

_Слов: 672_

### [[README|infrastructure-layer-b-ru]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 134_

### [[01-cowork-discovery|1. The Cowork Discovery and Why It Changes Everything]]
> > !NOTE

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 704_

### [[02-cowork-provides|2. What Cowork Provides That InGit Doesn't Need to Build]]
> > !NOTE

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 685_

### [[03-ingit-provides|3. What InGit Provides That Cowork Lacks]]
> > !NOTE

  - Содержание
  - 3. What InGit Provides That Cowork Lacks
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 870_

### [[04-symbiotic-architecture|4. The Symbiotic Architecture]]
> > !NOTE

  - Содержание
  - 4. The Symbiotic Architecture
  - Смотрите также

_Слов: 623_

### [[05-four-integration-paths|5. Four Integration Paths in Order of Accessibility]]
> > !NOTE

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility
  - Смотрите также

_Слов: 789_

### [[06-refined-ingit-scope|6. Refined InGit Scope with Cowork in Mind]]
> - 6. Refined InGit Scope with Cowork in Mind(#6-refined-ingit-scope-with-cowork-in-mind)

  - Contents
  - 6. Refined InGit Scope with Cowork in Mind
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 488_

### [[07-practical-first-steps|7. Practical First Steps This Month]]
> - 7. Practical First Steps This Month(#7-practical-first-steps-this-month)

  - Contents
  - 7. Practical First Steps This Month
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 479_

### [[08-implications-nautilus-okwf|8. Implications for Nautilus and OKWF]]
> > !TIP

  - Содержание
  - 8. Implications for Nautilus and OKWF
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 643_

### [[09-risks-open-questions|9. Risks and Open Questions]]
> > !TIP

  - Содержание
  - 9. Risks and Open Questions
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 580_

### [[10-strategic-positioning|10. Strategic Positioning]]
> > !NOTE

  - Содержание
  - 10. Strategic Positioning
  - Acknowledgments
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 789_

### [[README|ingit-cowork-en]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 124_

### [[01-otkrytie-cowork|1. Открытие Cowork и почему это меняет всё]]
> > !NOTE

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 671_

### [[02-chto-cowork-obespechivaet|2. Что Cowork обеспечивает, что InGit не нужно строить]]
> > !NOTE

  - Содержание
  - 2. Что Cowork обеспечивает, что InGit не нужно строить
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 678_

### [[03-chto-ingit-obespechivaet|3. Что InGit обеспечивает, чего Cowork не хватает]]
> > !IMPORTANT

  - Содержание
  - 3. Что InGit обеспечивает, чего Cowork не хватает
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 854_

### [[04-simbioticheskaya-arkhitektura|4. Симбиотическая Архитектура]]
> > !WARNING

  - Содержание
  - 4. Симбиотическая Архитектура
  - Смотрите также

_Слов: 615_

### [[05-chetyre-puti-integratsii|5. Четыре пути интеграции в порядке доступности]]
> > !TIP

  - Содержание
  - 5. Четыре пути интеграции в порядке доступности
  - Смотрите также

_Слов: 769_

### [[06-utochnyonnyy-obyom-ingit|6. Уточнённый объём InGit с учётом Cowork]]
> - 6. Уточнённый объём InGit с учётом Cowork(#6-уточнённый-объём-ingit-с-учётом-cowork)

  - Contents
  - 6. Уточнённый объём InGit с учётом Cowork
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 485_

### [[07-prakticheskie-shagi|7. Практические первые шаги в этом месяце]]
> - 7. Практические первые шаги в этом месяце(#7-практические-первые-шаги-в-этом-месяце)

  - Contents
  - 7. Практические первые шаги в этом месяце
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 483_

### [[08-implikatsii-nautilus-okwf|8. Импликации для Nautilus и OKWF]]
> > !NOTE

  - Содержание
  - 8. Импликации для Nautilus и OKWF
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 645_

### [[09-riski-voprosy|9. Риски и Открытые Вопросы]]
> > !WARNING

  - Содержание
  - 9. Риски и Открытые Вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 602_

### [[10-strategicheskoe-pozitsionirovanie|10. Стратегическое Позиционирование]]
> > !NOTE

  - Содержание
  - 10. Стратегическое Позиционирование
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 717_

### [[README|ingit-cowork-ru]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 124_

### [[00-question-innovations-transitions|Du hast gesagt: Интересно как новая как инновация как как рационализация как пер…]]
> > !WARNING

  - Содержание
  - Ответ по существу
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2871_

### [[01-response|Claude hat geantwortet: Отличный запрос.]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2489_

### [[README|innovation-transitions]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 104_

### [[00-question-multi-tier|Du hast gesagt: Ещё есть такие вопросы то есть если общие юридические Наутилус м…]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[01-strategic-significance|Claude hat geantwortet: Это стратегически значимый вопрос, и ответ на него — да,…]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2670_

### [[README|multi-tier-architecture]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[00-question-can-it-apply-to-docs|Du hast gesagt: Вопрос такой вопрос и такие а можно ли этот протокол это система…]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 385_

### [[01-structural-comparison-code-vs-docs|Структурное сравнение: код vs гуманитарные документы]]
> - Contents(#contents)

  - Содержание
  - Contents
- Законодательные
- Судебные
- Административные
- Процессуальные
- Социальные/медицинские
- Контрактные
  _... ещё 12 разделов_

_Слов: 1616_

### [[02-mcp-claude-desktop-use-cases|Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы …]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 322_

### [[03-what-doesnt-exist-on-market|Что не существует на рынке:]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[04-grant-opportunities|Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access t…]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 609_

### [[05-which-combination-more-valuable|Что из этого сейчас кажется более ценным? Или какая-то своя комбинация?]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 336_

### [[README|npp-humanitarian-extension]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 121_

### [[00-abstract-status|Abstract + Status of This Document]]
> - Abstract(#abstract)

  - Contents
- Nautilus Portal Protocol
  - Abstract
  - 0. Status of This Document
  - Использование
- Поиск по теме документа

_Слов: 322_

### [[01-introduction|1. Introduction (Motivation, Design Goals, Non-Goals, Terminology)]]
> - 1. Introduction(#1-introduction)

  - Contents
  - 1. Introduction
  - Использование
- Поиск по теме документа

_Слов: 398_

### [[02-terminology|2. Terminology]]
> - 2. Terminology(#2-terminology)

  - Contents
  - 2. Terminology
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 358_

### [[03-registry|3. Registry (nautilus.json)]]
> - 3. Registry (nautilus.json)(#3-registry-nautilusjson)

  - Contents
  - 3. Registry (nautilus.json)

_Слов: 456_

### [[04-passport|4. Passport (passport.md)]]
> - 4. Passport (passport.md)(#4-passport-passportmd)

  - Contents
  - 4. Passport (passport.md)
- ## Essence
  - Native Format
  - Content Overview
  - Angle / Perspective
  - Bridges
  - Author & Contact
  _... ещё 1 разделов_

_Слов: 322_

### [[05-compatibility-levels|5. Compatibility Levels]]
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Использование
- Поиск по теме документа

_Слов: 324_

### [[06-adapter-interface|6. Adapter Interface]]
> - 6. Adapter Interface(#6-adapter-interface)

  - Contents
  - 6. Adapter Interface

_Слов: 479_

### [[07-portal-entry|7. PortalEntry Structure]]
> - 7. PortalEntry Structure(#7-portalentry-structure)

  - Contents
  - 7. PortalEntry Structure

_Слов: 322_

### [[08-consensus-algorithm|8. Consensus Algorithm (v1.0: string normalization)]]
> - 8. Consensus Algorithm(#8-consensus-algorithm)

  - Contents
  - 8. Consensus Algorithm
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 371_

### [[09-query-flow|9. Query Flow]]
> - 9. Query Flow(#9-query-flow)

  - Contents
  - 9. Query Flow
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[10-query-result|10. QueryResult Structure]]
> - 10. QueryResult Structure(#10-queryresult-structure)

  - Contents
  - 10. QueryResult Structure
  - Смотрите также

_Слов: 339_

### [[11-security-considerations|11. Security Considerations]]
> - 11. Security Considerations(#11-security-considerations)

  - Contents
  - 11. Security Considerations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[12-versioning-policy|12. Versioning Policy]]
> - 12. Versioning Policy(#12-versioning-policy)

  - Contents
  - 12. Versioning Policy
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[13-reference-implementation|13. Reference Implementation]]
> - 13. Reference Implementation(#13-reference-implementation)

  - Contents
  - 13. Reference Implementation
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 341_

### [[14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]]
> - 14. ADR-001: Federation over Merging(#14-adr-001-federation-over-merging)

  - Contents
  - 14. ADR-001: Federation over Merging
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[15-glossary|15. Glossary of Examples]]
> - 15. Glossary of Examples(#15-glossary-of-examples)

  - Contents
  - 15. Glossary of Examples
  - Appendix A: Minimal Working Example
- mynotes
  - Essence
  - Native Format
  - Content Overview
  - Angle / Perspective
  _... ещё 2 разделов_

_Слов: 410_

### [[16-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]]
> - Essence(#essence)

  - Contents
- mynotes
  - Essence
  - Native Format
  - Content Overview
  - Angle / Perspective
  - Author
  - Смотрите также

_Слов: 327_

### [[17-appendix-b-change-log|Appendix B: Change Log]]
> - Appendix B: Change Log(#appendix-b-change-log)

  - Contents
  - Appendix B: Change Log
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 340_

### [[18-comment-on-document|Комментарий: дизайн-решения NPP v1.0]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 516_

### [[README|npp-v1-0]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 185_

### [[00-abstract-status|Abstract + Status of This Document]]
> - Abstract(#abstract)

  - Contents
- Nautilus Portal Protocol
  - Abstract
  - 0. Status of This Document
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 422_

### [[01-introduction|1. Introduction (Motivation, Design Goals, Non-Goals, Terminology, Changes from v1.0)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 1. Introduction
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 579_

### [[02-terminology|2. Terminology]]
> - 2. Terminology(#2-terminology)

  - Contents
  - 2. Terminology
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 455_

### [[03-registry|3. Registry (nautilus.json)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 3. Registry (nautilus.json)
  - Смотрите также

_Слов: 663_

### [[04-passport|4. Passport (passport.md)]]
> - 4. Passport (passport.md)(#4-passport-passportmd)

  - Contents
  - 4. Passport (passport.md)
- Паспорт: /
  - Смотрите также

_Слов: 377_

### [[05-compatibility-levels|5. Compatibility Levels]]
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 401_

### [[06-adapter-interface|6. Adapter Interface]]
> - 6. Adapter Interface(#6-adapter-interface)

  - Contents
  - 6. Adapter Interface
  - Смотрите также

_Слов: 441_

### [[07-portal-entry|7. PortalEntry Structure]]
> - 7. PortalEntry Structure(#7-portalentry-structure)

  - Contents
  - 7. PortalEntry Structure
  - Смотрите также

_Слов: 376_

### [[08-q6-space|8. Q6 Space (Normative)]]
> - 8. Q6 Space (Normative)(#8-q6-space-normative)

  - Contents
  - 8. Q6 Space (Normative)
  - Смотрите также

_Слов: 473_

### [[09-consensus-algorithm|9. Consensus Algorithm]]
> - 9. Consensus Algorithm(#9-consensus-algorithm)

  - Contents
  - 9. Consensus Algorithm
  - Смотрите также

_Слов: 432_

### [[10-query-flow|10. Query Flow]]
> - 10. Query Flow(#10-query-flow)

  - Contents
  - 10. Query Flow
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[11-relevance-ranking|11. Relevance Ranking]]
> - 11. Relevance Ranking(#11-relevance-ranking)

  - Contents
  - 11. Relevance Ranking
- Bonus for connectivity
- Penalty for fallback
  - Смотрите также

_Слов: 331_

### [[12-onboarding-paths|12. Onboarding Paths (Normative)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 12. Onboarding Paths (Normative)
  - Смотрите также

_Слов: 614_

### [[13-rest-api|13. REST API Contract (Normative for Portals)]]
> - 13. REST API Contract (Normative for Portals)(#13-rest-api-contract-normative-for-portals)

  - Contents
  - 13. REST API Contract (Normative for Portals)
  - Смотрите также

_Слов: 499_

### [[14-sdk|14. SDK Contract (Informative)]]
> - 14. SDK Contract (Informative)(#14-sdk-contract-informative)

  - Contents
  - 14. SDK Contract (Informative)
  - Смотрите также

_Слов: 328_

### [[15-security|15. Security Considerations]]
> - 15. Security Considerations(#15-security-considerations)

  - Contents
  - 15. Security Considerations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 388_

### [[16-mcp-extension|16. MCP Extension (Informative)]]
> - 16. MCP Extension (Informative)(#16-mcp-extension-informative)

  - Contents
  - 16. MCP Extension (Informative)
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 330_

### [[17-versioning-policy|17. Versioning Policy]]
> - 17. Versioning Policy(#17-versioning-policy)

  - Contents
  - 17. Versioning Policy
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[18-reference-implementation|18. Reference Implementation]]
> - 18. Reference Implementation(#18-reference-implementation)

  - Contents
  - 18. Reference Implementation
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 326_

### [[19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]]
> - 19. ADR-001: Federation over Merging(#19-adr-001-federation-over-merging)

  - Contents
  - 19. ADR-001: Federation over Merging
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 304_

### [[20-adr-002-q6-first-class|20. ADR-002: Q6 as First-Class Protocol Concept]]
> - 20. ADR-002: Q6 as First-Class Protocol Concept(#20-adr-002-q6-as-first-class-protocol-concept)

  - Contents
  - 20. ADR-002: Q6 as First-Class Protocol Concept
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[21-adr-003-five-onboarding-paths|21. ADR-003: Five Onboarding Paths as Equal-Rank]]
> - 21. ADR-003: Five Onboarding Paths as Equal-Rank(#21-adr-003-five-onboarding-paths-as-equal-rank)

  - Contents
  - 21. ADR-003: Five Onboarding Paths as Equal-Rank
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 333_

### [[22-glossary|22. Glossary of Reference Examples]]
> > !NOTE

  - Содержание
  - 22. Glossary of Reference Examples
  - Appendix A: Minimal Working Example
- adapters/mynotes.py
- ... больше entries
- Паспорт: owner/my-notes
  - Описание
  - Объём
  _... ещё 7 разделов_

_Слов: 1542_

### [[README|npp-v1-1]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 195_

### [[00-abstract|AI-Coordinated Infrastructure for Distributed Expert Contribution]]
> - Основной раздел

  - Содержание
- Open Knowledge Work Foundation
  - AI-Coordinated Infrastructure for Distributed Expert Contribution
  - Executive Summary
  - Table of Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 471_

### [[01-problem-statement|1. Problem Statement]]
> > !NOTE

  - Содержание
  - 1. Problem Statement
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 653_

### [[02-target-populations|2. Target Populations]]
> > !NOTE

  - Содержание
  - 2. Target Populations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 719_

### [[03-why-existing-fail|3. Why Existing Solutions Fail]]
> > !NOTE

  - Содержание
  - 3. Why Existing Solutions Fail
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 732_

### [[04-proposed-infrastructure|4. Proposed Infrastructure]]
> > !TIP

  - Содержание
  - 4. Proposed Infrastructure
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1014_

### [[05-economic-model|5. Economic Model]]
> > !TIP

  - Содержание
  - 5. Economic Model
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 620_

### [[06-governance-ethics|6. Governance and Ethics]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Governance and Ethics
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 631_

### [[07-phased-rollout|7. Phased Rollout Plan]]
> > !NOTE

  - Содержание
  - 7. Phased Rollout Plan
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 690_

### [[08-risk-analysis|8. Risk Analysis]]
> > !TIP

  - Содержание
  - 8. Risk Analysis
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 679_

### [[09-call-for-partnership|9. Call for Partnership]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Call for Partnership
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 652_

### [[10-appendices|10. Appendices]]
> > !NOTE

  - Содержание
  - 10. Appendices
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 869_

### [[README|okwf-concept]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 130_

### [[00-question-anonymization|Du hast gesagt: Насчёт приватности Я думаю что возможно удалять только личные да…]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 370_

### [[01-what-to-anonymize-german-standard|Что именно анонимизировать: немецкий стандарт]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 345_

### [[02-two-tier-publication|Архитектурное решение: две-уровневая публикация]]
> - Contents(#contents)

  - Содержание
  - Contents
- В приватном репо cases-private:
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 591_

### [[03-what-this-gives-technically|Что это даёт технически]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1559_

### [[04-what-i-can-do-now|Что я могу сделать сейчас]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 399_

### [[README|privacy-federation]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 112_

### [[00-abstract|Professional Colleague Agents]]
> - Содержание(#содержание)

  - Содержание
  - Содержание
- Professional Colleague Agents
  - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers
  - Abstract
  - Table of Contents
  - Использование
- Поиск по теме документа
  _... ещё 1 разделов_

_Слов: 548_

### [[01-five-type-typology|1. The Five-Type Typology of Principal-Side Agents]]
> > !NOTE

  - Содержание
  - 1. The Five-Type Typology of Principal-Side Agents
  - Смотрите также

_Слов: 930_

### [[02-what-makes-pca|2. What Makes a Professional Colleague Agent]]
> > !NOTE

  - Содержание
  - 2. What Makes a Professional Colleague Agent
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 864_

### [[03-empirical-case-obuchay|3. Empirical Case Study: «Обучай»]]
> > !NOTE

  - Содержание
  - 3. Empirical Case Study: «Обучай»
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 876_

### [[04-architecture|4. Architecture of Professional Colleague Agents]]
> > !NOTE

  - Содержание
  - 4. Architecture of Professional Colleague Agents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 912_

### [[05-economics-replication|5. The Economics of Profession-Wide Replication]]
> > !NOTE

  - Содержание
  - 5. The Economics of Profession-Wide Replication
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 765_

### [[06-risks|6. Risks Specific to this Category]]
> > !TIP

  - Содержание
  - 6. Risks Specific to this Category
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1194_

### [[07-application-domains|7. Application Domains]]
> > !TIP

  - Содержание
  - 7. Application Domains
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 741_

### [[08-pilot-sgb-advocate|8. Pilot Proposal: SGB Advocate Colleague]]
> > !NOTE

  - Содержание
  - 8. Pilot Proposal: SGB Advocate Colleague
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 999_

### [[09-relationship-other-agents|9. Relationship to Other Agent Types]]
> > !NOTE

  - Содержание
  - 9. Relationship to Other Agent Types
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 697_

### [[10-open-questions|10. Open Questions]]
> - 10. Open Questions(#10-open-questions)

  - Contents
  - 10. Open Questions
  - Использование
- Поиск по теме документа

_Слов: 464_

### [[11-call-for-collaboration|11. Call for Collaboration]]
> - 11. Call for Collaboration(#11-call-for-collaboration)

  - Contents
  - 11. Call for Collaboration
  - Использование
- Поиск по теме документа

_Слов: 422_

### [[12-closing|12. Closing]]
> > !NOTE

  - Содержание
  - 12. Closing
  - Acknowledgments
  - References
  - Использование
- Поиск по теме документа

_Слов: 585_

### [[README|professional-colleague-agents-en]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 126_

### [[00-abstract|Содержание]]
> > !NOTE

  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[01-pyat-tipov|1. Типология из пяти типов агентов на стороне принципала]]
> > !IMPORTANT

  - Содержание
  - 1. Типология из пяти типов агентов на стороне принципала
  - Смотрите также

_Слов: 869_

### [[02-chto-delaet-pka|2. Что делает агента Профессиональным Коллегой]]
> > !TIP

  - Содержание
  - 2. Что делает агента Профессиональным Коллегой
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 760_

### [[03-keys-obuchay|3. Эмпирический кейс: «Обучай»]]
> > !NOTE

  - Содержание
  - 3. Эмпирический кейс: «Обучай»
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 830_

### [[04-arkhitektura|4. Архитектура Профессиональных Коллег-Агентов]]
> > !NOTE

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 876_

### [[05-ekonomika|5. Экономика тиражирования по профессии]]
> > !NOTE

  - Содержание
  - 5. Экономика тиражирования по профессии
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 760_

### [[06-riski|6. Риски, специфичные для этой категории]]
> > !WARNING

  - Содержание
  - 6. Риски, специфичные для этой категории
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1185_

### [[07-oblasti-primeneniya|7. Области применения]]
> > !WARNING

  - Содержание
  - 7. Области применения
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 756_

### [[08-pilot-sgb-kolega|8. Пилотное предложение: SGB Колega-Адвокат]]
> > !WARNING

  - Содержание
  - 8. Пилотное предложение: SGB Колega-Адвокат
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1023_

### [[09-svyaz-s-drugimi|9. Связь с другими типами агентов]]
> > !WARNING

  - Содержание
  - 9. Связь с другими типами агентов
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 659_

### [[10-otkrytye-voprosy|10. Открытые вопросы]]
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Использование
- Поиск по теме документа

_Слов: 450_

### [[11-prizyv-k-sotrudnichestvu|11. Призыв к сотрудничеству]]
> - 11. Призыв к сотрудничеству(#11-призыв-к-сотрудничеству)

  - Contents
  - 11. Призыв к сотрудничеству
  - Использование
- Поиск по теме документа

_Слов: 413_

### [[12-zaklyuchenie|12. Заключение]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 12. Заключение
  - Благодарности
  - Ссылки
  - Использование
- Поиск по теме документа
- Поиск (bm25)
  _... ещё 2 разделов_

_Слов: 645_

### [[README|professional-colleague-agents-ru]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 127_

### [[00-abstract|AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations]]
> - Основной раздел

  - Содержание
- The Representative Agent Layer
  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations
  - Abstract
  - Table of Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 486_

### [[01-cinderella-syndrome|1. The Cinderella Syndrome: Why Quality Stays Invisible]]
> > !NOTE

  - Содержание
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 865_

### [[02-historical-precedents|2. Historical Precedents: Agents as Civilizational Innovation]]
> > !NOTE

  - Содержание
  - 2. Historical Precedents: Agents as Civilizational Innovation
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 980_

### [[03-what-makes-representative-agent|3. What Makes a Representative Agent]]
> > !NOTE

  - Содержание
  - 3. What Makes a Representative Agent
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 693_

### [[04-ten-domains|4. Ten Domains of Application]]
> > !TIP

  - Содержание
  - 4. Ten Domains of Application
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1599_

### [[05-architectural-specification|5. Architectural Specification]]
> > !NOTE

  - Содержание
  - 5. Architectural Specification
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 689_

### [[06-ethical-framework|6. Ethical Framework]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Ethical Framework
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 604_

### [[07-governance-oversight|7. Governance and Oversight]]
> - 7. Governance and Oversight(#7-governance-and-oversight)

  - Contents
  - 7. Governance and Oversight
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 490_

### [[08-risks-mitigations|8. Risks and Mitigations]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Risks and Mitigations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 686_

### [[09-phased-rollout|9. Phased Rollout Strategy]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Phased Rollout Strategy
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 675_

### [[10-open-questions|10. Open Questions]]
> - 10. Open Questions(#10-open-questions)

  - Contents
  - 10. Open Questions
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 470_

### [[11-call-for-collaboration|11. Call for Collaboration]]
> - 11. Call for Collaboration(#11-call-for-collaboration)

  - Contents
  - 11. Call for Collaboration
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 497_

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
  _... ещё 5 разделов_

_Слов: 2730_

### [[README|representative-agent-layer-en]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 130_

### [[00-abstract|Содержание]]
> > !NOTE

  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 332_

### [[01-sindrom-zolushki|1. Синдром Золушки: Почему качество остаётся невидимым]]
> > !NOTE

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 820_

### [[02-istoricheskie-pretsedenty|2. Исторические прецеденты: Агенты как цивилизационная инновация]]
> > !WARNING

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 959_

### [[03-chto-delaet-predstavitelskim|3. Что делает агента Представительским]]
> > !TIP

  - Содержание
  - 3. Что делает агента Представительским
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 649_

### [[04-desyat-oblastey|4. Десять областей применения]]
> > !WARNING

  - Содержание
  - 4. Десять областей применения
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1611_

### [[05-arkhitekturnaya-spetsifikatsiya|5. Архитектурная спецификация]]
> > !NOTE

  - Содержание
  - 5. Архитектурная спецификация
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 670_

### [[06-eticheskaya-ramka|6. Этическая рамка]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Этическая рамка
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 608_

### [[07-upravlenie-nadzor|7. Управление и надзор]]
> - 7. Управление и надзор(#7-управление-и-надзор)

  - Contents
  - 7. Управление и надзор
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 489_

### [[08-riski-mery|8. Риски и меры противодействия]]
> > !WARNING

  - Содержание
  - 8. Риски и меры противодействия
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 615_

### [[09-strategiya-razvyortyvaniya|9. Стратегия поэтапного развёртывания]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Стратегия поэтапного развёртывания
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 666_

### [[10-otkrytye-voprosy|10. Открытые вопросы]]
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 459_

### [[11-prizyv-k-sotrudnichestvu|11. Призыв к сотрудничеству]]
> - 11. Призыв к сотрудничеству(#11-призыв-к-сотрудничеству)

  - Contents
  - 11. Призыв к сотрудничеству
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 474_

### [[12-zaklyuchenie|12. Заключение]]
> > !TIP

  - Содержание
  - 12. Заключение
  - Благодарности
  - Ссылки
  - Приложение A: Связь с Сопроводительными Статьями
  - Приложение B: Матрица Сравнения Областей
  - Приложение C: Образцы Случаев Использования в Деталях
  - Использование
  _... ещё 3 разделов_

_Слов: 4477_

### [[README|representative-agent-layer-ru]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 129_

### [[00-tldr|TL;DR — Трёхфазная методология Review]]
> - TL;DR(#tldr)

  - Contents
- Трёхфазная методология Review в Nautilus
  - TL;DR
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 326_

### [[01-context-motivation|1. Контекст и мотивация]]
> - 1. Контекст и мотивация(#1-контекст-и-мотивация)

  - Contents
  - 1. Контекст и мотивация
  - Смотрите также

_Слов: 429_

### [[02-formal-workflow|2. Формальный workflow]]
> - 2. Формальный workflow(#2-формальный-workflow)

  - Contents
  - 2. Формальный workflow
  - Смотрите также

_Слов: 469_

### [[03-consolidation-principles|3. Принципы консолидации (Фаза C)]]
> - Contents(#contents)

  - Содержание
  - Contents
  - 3. Принципы консолидации (Фаза C)
- LOC в Python-коде
- Количество тестов
- Число адаптеров
- Health score
- Q6-покрытие
  _... ещё 1 разделов_

_Слов: 547_

### [[04-fallback-ratio-question|Вопрос: fallback‑ratio как критический или осмысленный?]]
> - Вопрос: fallback-ratio как критический или осмысленный?(#вопрос-fallback-ratio-как-критический-или-осмысленный)

  - Contents
  - Вопрос: fallback-ratio как критический или осмысленный?
  - Смотрите также

_Слов: 324_

### [[05-conditions-of-applicability|4. Условия применимости]]
> - 4. Условия применимости(#4-условия-применимости)

  - Contents
  - 4. Условия применимости
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 322_

### [[06-relation-existing-methodologies|5. Связь с существующими методологиями]]
> - 5. Связь с существующими методологиями(#5-связь-с-существующими-методологиями)

  - Contents
  - 5. Связь с существующими методологиями
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 412_

### [[07-why-valid-for-ai|6. Почему это валидный паттерн для AI‑assisted workflows]]
> - 6. Почему это валидный паттерн для AI-assisted workflows(#6-почему-это-валидный-паттерн-для-ai-assisted-workflows)

  - Contents
  - 6. Почему это валидный паттерн для AI-assisted workflows
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[08-implementation-nautilus|7. Реализация в проекте Nautilus]]
> - 7. Реализация в проекте Nautilus(#7-реализация-в-проекте-nautilus)

  - Contents
  - 7. Реализация в проекте Nautilus
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [[09-limitations-open-questions|8. Ограничения и открытые вопросы]]
> - 8. Ограничения и открытые вопросы(#8-ограничения-и-открытые-вопросы)

  - Contents
  - 8. Ограничения и открытые вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 446_

### [[10-checklist|9. Checklist применения методологии]]
> - 9. Checklist применения методологии(#9-checklist-применения-методологии)

  - Contents
  - 9. Checklist применения методологии
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 390_

### [[11-application-plan-current-docs|10. Конкретный план применения к текущим документам]]
> - 10. Конкретный план применения к текущим документам(#10-конкретный-план-применения-к-текущим-документам)

  - Contents
  - 10. Конкретный план применения к текущим документам
- В Termux
  - Смотрите также

_Слов: 328_

### [[12-appendix-a-header-warning|Appendix A: Шаблон для header warning]]
> - Appendix A: Шаблон для header warning(#appendix-a-шаблон-для-header-warning)

  - Contents
  - Appendix A: Шаблон для header warning
  - Смотрите также

_Слов: 334_

### [[13-appendix-b-examples|Appendix B: Примеры расхождений и их разрешения]]
> - Appendix B: Примеры расхождений и их разрешения(#appendix-b-примеры-расхождений-и-их-разрешения)

  - Contents
  - Appendix B: Примеры расхождений и их разрешения
  - Смотрите также

_Слов: 341_

### [[14-main-technical-risks|Главные технические риски]]
> - Главные технические риски(#главные-технические-риски)

  - Contents
  - Главные технические риски
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 329_

### [[15-appendix-c-history|Appendix C: История изменений методологии]]
> - Appendix C: История изменений методологии(#appendix-c-история-изменений-методологии)

  - Contents
  - Appendix C: История изменений методологии
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 340_

### [[16-glossary|Глоссарий]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Глоссарий
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1032_

### [[README|review-methodology]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 173_

### [[00-question-supply-demand|Du hast gesagt: Спрос рождает предложение - это простая экономическая истина нач…]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 541_

### [[01-three-related-themes|Claude hat geantwortet: Очень богатый вопрос — три разных, но связанных темы.]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2998_

### [[README|supply-demand]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[00-question-mountain-to-person|Du hast gesagt: Того если гора не идёт человеку может быть этот человек пойдёт к…]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 615_

### [[01-completing-loop|Claude hat geantwortet: Это исключительно богатый вопрос, и я хочу ответить на н…]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 3207_

### [[README|transmission-box]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

**Итого в секции: 171,632 слов, 255 файлов**


## Processing Guide

_Путь: `docs/processing-guide/`_

### [[01-overview|Обработка больших массивов информации — Часть 1: Обзор и таксономия]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Проблема
  - Таксономия методов
  - Что реализовано в Lorenzo
  - Навигация по разделам
  - Смотрите также

_Слов: 557_

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
  _... ещё 2 разделов_

_Слов: 624_

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
  _... ещё 8 разделов_

_Слов: 666_

### [[04-structuring|Обработка больших массивов — Часть 4: Структурирование]]
> > 04-structuring — раздел документации проекта Lorenzo.

  - Содержание
  - Проблема неструктурированности
  - Инструмент 1: Автоматические метаданные — improveautofill.py
  - Статус
  - Инструмент 2: Оглавления — improveautotoc.py
  - Содержание
  - Инструмент 3: Теги — improvetags.py
  - Инструмент 4: Перекрёстные ссылки — improvecrosslinkall.py
  _... ещё 16 разделов_

_Слов: 728_

### [[05-analysis|Обработка больших массивов — Часть 5: Анализ и NLP]]
> > !NOTE

  - Содержание
  - Что такое «анализ без LLM»
  - Группа 1: Извлечение сущностей
- MHTML → "MIME HTML archive format"
- BM25  → "Best Match 25, алгоритм ранжирования"
- RAG   → "Retrieval-Augmented Generation"
  - Группа 2: Граф знаний
- Вывод: docs/network.dot (Graphviz), docs/NETWORK.md
  _... ещё 9 разделов_

_Слов: 913_

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
  _... ещё 14 разделов_

_Слов: 967_

### [[07-llm|Обработка больших массивов — Часть 7: LLM-обогащение]]
> > !NOTE

  - Содержание
  - Граница классики и LLM
  - Архитектура: 5 LLM-скриптов
  - improvellmenrich.py — обогащение файлов
  - improvellmqa.py — Q&A по базе знаний
  - improvellmsummary.py — каскадная суммаризация
  - improvellmgaps.py — пробелы в документации
- → docs/LLMGAPS.md
  _... ещё 8 разделов_

_Слов: 886_

### [[08-export|Обработка больших массивов — Часть 8: Экспорт и интеграции]]
> > !NOTE

  - Содержание
  - Зачем экспортировать?
  - Obsidian Vault — improveobsidian.py
- → docs/obsidian/ (1053 файла готовы к открытию в Obsidian)
  - Confluence — improveconfluence.py
- → docs/confluence//.wiki
  - EPUB — improveepub.py
  - RSS/Atom — improverss.py
  _... ещё 18 разделов_

_Слов: 751_

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
  _... ещё 17 разделов_

_Слов: 888_

### [[10-future|Обработка больших массивов — Часть 10: Инновационные подходы]]
> > !NOTE

  - Содержание
  - Граница между «уже есть» и «ещё нет»
  - Уровень A: Векторный поиск (следующий шаг)
- Шаг 1: Индексация (один раз)
- Сохранить индекс
- Шаг 2: Поиск
- Reciprocal Rank Fusion — объединяет оба ранжирования
  - Уровень B: Граф знаний с LLM-NER
  _... ещё 33 разделов_

_Слов: 1787_

### [[PROCESSING_GUIDE|Обработка больших массивов документов — Полное руководство]]
> > PROCESSINGGUIDE — раздел документации проекта Lorenzo.

  - Содержание
  - Содержание
  - Обработка больших массивов информации — Часть 1: Обзор и таксономия
  - Проблема
  - Таксономия методов
  - Что реализовано в Lorenzo
  - Навигация по разделам
  - Обработка больших массивов — Часть 2: Извлечение
  _... ещё 179 разделов_

_Слов: 8089_

### [[QA|Q&A: processing-guide]]
> > !NOTE

  - Какие системы памяти описаны в этом разделе?
  - Как происходит консолидация и забывание в памяти агентов?
  - Какова разница между эпизодической и семантической памятью?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  _... ещё 13 разделов_

_Слов: 268_

### [[README|processing-guide]]
> Файлов: 12

  - Содержание
  - Использование
- Запуск

_Слов: 125_

**Итого в секции: 17,249 слов, 13 файлов**


## Svyazi 2 0

_Путь: `docs/svyazi-2-0/`_

### [[QA|Q&A: svyazi-2-0]]
> - Основной раздел

  - Содержание
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  _... ещё 2 разделов_

_Слов: 387_

### [[README|svyazi-2-0]]
> > !NOTE

  - Содержание
  - Подразделы
  - Использование
- Запуск

_Слов: 123_

### [[README|architecture]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 113_

### [[card-envelope|Card Envelope]]
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[evidence-envelope|Evidence Envelope]]
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Особые случаи
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 304_

### [[gaps|Архитектурные зазоры]]
> > !TIP

  - Содержание
  - Пять зазоров, важнее поиска ещё десяти инструментов
  - Сводная таблица зазоров
  - Главный практический принцип
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 636_

### [[integration-spec|Интеграционная спецификация (минимум для MVP)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 318_

### [[memory-write-policy|Memory Write Policy]]
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[review-record|Review Record]]
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 306_

### [[skill-tool-policy|Skill and Tool Policy]]
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[README|components]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 185_

### [[agent-memory-mcp|agent-memory-mcp + Memory OS]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 304_

### [[agentfs]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 303_

### [[ai-factory|AI Factory + AIF Handoff]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 311_

### [[autoresearch-sequential|AutoResearch + Sequential]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 308_

### [[graph-rag|Graph RAG]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 304_

### [[hybrid-rag|Hybrid RAG knowledge base]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 309_

### [[knowledge-space]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 301_

### [[legal-rag|Legal RAG]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[mclaude]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[memnet|MemNet / memory-is-all-you-need]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
- Поиск (bm25)
- Поиск (semantic)
- Поиск (full)
  _... ещё 3 разделов_

_Слов: 302_

### [[ngt-memory|NGT Memory]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 306_

### [[research-docs-liteparse|research-docs + LiteParse]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 306_

### [[rufler]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[security-routing-plane|Security + routing plane]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Числовые наблюдения
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[self-aware-mcp|Self‑Aware MCP + Skills + CodeWiki]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 303_

### [[svyazi]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 312_

### [[voice-stack|Voice / local-first stack]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 305_

### [[yjs-automerge|Yjs + Automerge]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 304_

### [[yodoca]]
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 305_

### [[A-collaboration-os|Ансамбль A — Collaboration OS]]
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 326_

### [[B-forensic-rag|Ансамбль B — Forensic RAG для доказуемого matching и review]]
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 331_

### [[C-multi-agent-factory|Ансамбль C — Spec‑driven multi‑agent factory]]
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 328_

### [[D-voice-first-mesh|Ансамбль D — Voice‑first local knowledge mesh]]
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 331_

### [[E-execution-plane|Ансамбль E — Safe and cheap execution plane]]
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 331_

### [[F-evidence-backed-intake|Ансамбль F — Evidence‑Backed Community Intake]]
> - Схема(#схема)

  - Contents
  - Схема
  - Новые свойства
  - Смотрите также

_Слов: 334_

### [[G-federated-local-graph|Ансамбль G — Federated Local‑First Community Graph]]
> - Схема(#схема)

  - Contents
  - Схема
  - Новое свойство
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 335_

### [[H-research-to-product-flywheel|Ансамбль H — Research‑to‑Product Flywheel]]
> - Схема(#схема)

  - Contents
  - Схема
  - Новое свойство
  - Смотрите также

_Слов: 328_

### [[README|Ансамбли проектов]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 135_

### [[README|limitations]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 112_

### [[conclusions|Итоговые выводы и порядок сборки]]
> - Главный вывод первой части(#главный-вывод-первой-части)

  - Contents
  - Главный вывод первой части
  - Порядок практической сборки
  - Главный вывод второй части
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 403_

### [[do-not-glue|Что пока лучше не склеивать]]
> - Оркестрация — выбрать один spine(#оркестрация-выбрать-один-spine)

  - Contents
  - Оркестрация — выбрать один spine
  - Voice/local‑first mesh — не идеализировать
  - Self‑improvement — только после метрики
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 409_

### [[license-tree|Лицензионные развилки]]
> - Развилки в коротком виде(#развилки-в-коротком-виде)

  - Contents
  - Развилки в коротком виде
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 381_

### [[README|outreach]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 100_

### [[first-contacts|Первые контакты]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[message-template|Шаблон первого сообщения]]
> - Замечание(#замечание)

  - Contents
  - Замечание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[narrow-questions|Узкие вопросы для каждого автора]]
> - Адресные вопросы(#адресные-вопросы)

  - Contents
  - Адресные вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 386_

### [[README|overview]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[continuation-intro|Что добавляет продолжение исследования]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 324_

### [[executive-summary|Executive summary]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 428_

### [[methodology|Методика и рамка отбора]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 328_

### [[projects-map|Карта найденных проектов и паттернов]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 1355_

### [[README|prototype]]
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 112_

### [[mvp-plan|План MVP-прототипа]]
> - Минимальная сборка прототипа(#минимальная-сборка-прототипа)

  - Contents
  - Минимальная сборка прототипа
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 369_

### [[risks|Ключевые риски и как их закрывать]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 343_

### [[roadmap|Дорожная карта прототипа]]
> > !TIP

  - Содержание
  - Итерация 1 — Evidence-first card graph
  - Итерация 2 — Memory governance
  - Итерация 3 — Orchestration + federation
  - Сводная таблица
  - Главный инженерный вывод
  - Использование
- Поиск по теме документа
  _... ещё 1 разделов_

_Слов: 651_

### [[README|security]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 100_

### [[budget-routing|Практичный бюджетный роутинг моделей]]
> - Обоснование(#обоснование)

  - Contents
  - Обоснование
  - Три режима
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 388_

### [[default-policy|Что стоит зафиксировать как default policy]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 399_

### [[privacy|Приватность: local-first by default]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 338_

**Итого в секции: 19,542 слов, 60 файлов**


## Technology Combinations

_Путь: `docs/technology-combinations/`_

### [[README|technology-combinations/ — комбинирование технологий для новых свойств]]
> > !TIP

  - Содержание
  - Источник
  - Подпапки
  - Главная находка диалога
  - См. также
  - Использование

_Слов: 345_

### [[01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern|Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 308_

### [[02-multiagentnyy-khaos-reshenie-auto-ai-router|Комбинация 2: Мультиагентный хаос-решение × Auto AI Router]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[03-crdt-local-first-svyazi-cardindex|Комбинация 3: CRDT local-first × Svyazi CardIndex]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 301_

### [[04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura|Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy|Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-|Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[07-crawl4ai-docling-yodoca-consolidator|Комбинация 7: Crawl4AI × Docling × Yodoca consolidator]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[08-conductor-adversarial-review-auto-ai-router|Комбинация 8: Conductor × adversarial-review × Auto AI Router]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 768_

### [[09-agent-orchestration-stack|Комбинация 9: Agent Orchestration Stack]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[10-legal-document-intelligence-pipeline|Комбинация 10: Legal Document Intelligence Pipeline]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[11-hybrid-crdt-sql-database|Комбинация 11: Hybrid CRDT-SQL Database]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[12-multi-agent-observability-stack|Комбинация 12: Multi-Agent Observability Stack]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[13-legal-document-transpiler|Комбинация 13: Legal Document Transpiler]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[14-local-first-agent-development-environment|Комбинация 14: local-first Agent Development Environment]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 659_

### [[15-self-consolidating-legal-corpus|Комбинация 15: Self-Consolidating Legal Corpus]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[16-adversarial-multi-agent-code-review|Комбинация 16: Adversarial Multi-Agent Code Review]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 338_

### [[17-distributed-agent-memory-with-graph|Комбинация 17: Distributed Agent Memory with Graph]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[18-llm-powered-legal-corpus-builder|Комбинация 18: LLM-Powered Legal Corpus Builder]]
> - Смотрите также(#смотрите-также)

  - Contents
- Crawl4AI pipeline
- Svyazi deduplication
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 302_

### [[19-multi-agent-observability-platform|Комбинация 19: Multi-Agent Observability Platform]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 775_

### [[20-hybrid-olap-oltp-with-real-time-sync|Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 320_

### [[21-legal-corpus-analytics-at-scale|Комбинация 21: Legal Corpus Analytics at Scale]]
> - Смотрите также(#смотрите-также)

  - Contents
- Pipeline
- Schema
- Analytics queries (subsecond)
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 313_

### [[22-russian-international-oss-stack|Комбинация 22: Russian-International OSS Stack]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[23-security-first-code-review-pipeline|Комбинация 23: Security-First Code Review Pipeline]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 334_

### [[24-mega-integration-full-stack|Комбинация 24: MEGA-INTEGRATION: Full Stack]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 691_

### [[25-legal-dsl-code-transpiler|Комбинация 25: Legal DSL → Code Transpiler]]
> - Смотрите также(#смотрите-также)

  - Contents
- DSL syntax (natural language-like)
- DSL operations
- Output: ready Widerspruch.docx
- DSL for conversion
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 316_

### [[26-ast-based-code-analysis-for-legal-automation|Комбинация 26: AST-Based Code Analysis for Legal Automation]]
> - Смотрите также(#смотрите-также)

  - Contents
- Input: Python script for Fristwahrung calculation
- AST analysis
- Extract legal logic
- → Pydantic model: LegalRule(
- name="Widerspruchsfrist",
- baseduration=timedelta(days(),
- extensions=[...],
  _... ещё 7 разделов_

_Слов: 331_

### [[27-hybrid-rag-with-ast-chunked-code|Комбинация 27: Hybrid RAG with AST-Chunked Code]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[28-pydantic-enforced-legal-workflows|Комбинация 28: Pydantic-Enforced Legal Workflows]]
> - Смотрите также(#смотрите-также)

  - Contents
- Sequential pipeline with Pydantic validation at each stage
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[29-meta-programmatic-legal-template-generator|Комбинация 29: Meta-Programmatic Legal Template Generator]]
> - Смотрите также(#смотрите-также)

  - Contents
- Legal DSL (declarative)
- Compiler generates Python code
- auto-generated rendering logic
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[30-mega-stack-3-0-with-dsl-ast|Комбинация 30: MEGA-STACK 3.0 with DSL & AST]]
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 589_

### [[31-event-sourced-legal-document-history|Комбинация 31: Event-Sourced Legal Document History]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 308_

### [[32-consensus-based-multi-agent-coordination|Комбинация 32: Consensus-Based Multi-Agent Coordination]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[33-event-sourcing-cqrs-clickhouse-analytics|Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[34-distributed-event-store-with-paxos|Комбинация 34: Distributed Event Store with Paxos]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[35-mega-stack-4-0-with-event-sourcing-consensus|Комбинация 35: MEGA-STACK 4.0 with Event Sourcing & Consensus]]
> - Contents(#contents)

  - Содержание
  - Contents
- Events
- Event Store
- Time-travel query
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 554_

### [[README|combinations]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 281_

### [[01-legal-ai-stack|Mega‑Stack 1.0 — Полный Legal‑AI Stack]]
> - Результат(#результат)

  - Contents
  - Результат
  - Первый проект для внедрения
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[02-ultimate-legal-ai|Mega‑Stack 2.0 — Ultimate Legal‑AI System]]
> - Capabilities(#capabilities)

  - Contents
  - Capabilities
  - First implementation priority
  - Смотрите также

_Слов: 391_

### [[03-dsl-ast|Mega‑Stack 3.0 — with DSL & AST]]
> - New capabilities(#new-capabilities)

  - Contents
  - New capabilities
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 302_

### [[04-event-sourcing-consensus|Mega‑Stack 4.0 — with Event Sourcing & Consensus]]
> - New capabilities(#new-capabilities)

  - Contents
  - New capabilities
  - Performance
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 351_

### [[README|mega-stacks]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[README|properties/ — эмерджентные свойства]]
> > properties/ — эмерджентные свойства

  - Содержание
  - Шаблон файла
- <Название свойства>
  - Что это
  - Какие компоненты дают это свойство в комбинации
  - Почему ни один из них в отдельности не даёт свойства
  - Как проверить, что свойство реально появилось
  - Смотрите также

_Слов: 333_

### [[README|research-reports]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 106_

### [[continuation-10-domains|Research Report: Continuation — 10 New Domains Beyond the Original 45 Combinations]]
> - 10 новых технологических областей(#10-новых-технологических-областей)

  - Contents
  - 10 новых технологических областей
  - 35+ новых синергетических комбинаций
  - 5 кросс‑сквозных эмерджентных архитектур
  - Методологические оговорки
  - Применение к Sozialrecht
  - Артефакт документа
  - Итоговый объём исследования
  _... ещё 3 разделов_

_Слов: 429_

### [[sozialrecht-35-combinations|Research Report: Sozialrecht (35 комбинаций)]]
> - Что в отчёте(#что-в-отчёте)

  - Contents
  - Что в отчёте
  - Артефакт документа
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[01-08-summary|Сводная таблица 1–8]]
> - 🎯 Главная находка: паттерн «скромные родители → мощные дети»(#главная-находка-паттерн-скромные-родители-мощные-дети)

  - Contents
  - 🎯 Главная находка: паттерн «скромные родители → мощные дети»
  - Рекомендация
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 470_

### [[09-14-extended|Сводная таблица 9–14 (Extended)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[15-19-extended|Сводная таблица 15–19 (Extended)]]
> - Смотрите также(#смотрите-также)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[20-24-final|Сводная таблица 20–24 (Final 1–24)]]
> - Рекомендация(#рекомендация)

  - Contents
  - Рекомендация
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 331_

### [[25-30-extended|Сводная таблица 25–30 (Complete 1–30)]]
> - Рекомендация(#рекомендация)

  - Contents
  - Рекомендация
  - Смотрите также

_Слов: 331_

### [[31-35-final|Сводная таблица 31–35 (Complete 1–35)]]
> - Рекомендация(#рекомендация)

  - Contents
  - Рекомендация
- Events
- Event Store (append-only)
- Time-travel query
  - Смотрите также

_Слов: 331_

### [[README|synthesis-tables]]
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 114_

**Итого в секции: 18,551 слов, 53 файлов**


## Templates

_Путь: `docs/templates/`_

### [[README|Шаблоны документов]]
> > !NOTE

  - Доступные шаблоны
  - Использование
- Скопируйте нужный шаблон в нужную папку
- Затем откройте и заполните поля в [квадратных скобках]

_Слов: 125_

### [Спецификация агента: [Название]](templates/agent-spec.md)
> > agent-spec — раздел документации проекта Lorenzo.

  - Тип агента
  - Назначение
  - Принципал
  - Скилы агента
  - Tools (плагины)
  - Память
  - Decision boundary
  - Failure modes
  _... ещё 6 разделов_

_Слов: 420_

### [Контакт: [Имя / Проект]](templates/contact-outreach.md)
> > !NOTE

  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы для обсуждения

_Слов: 132_

### [Противоречие: [Название]](templates/contradiction-record.md)
> > contradiction-record — раздел документации проекта Lorenzo.

  - Содержание
  - ID
  - Серьёзность
  - Источник A
  - Источник B
  - В чём противоречие
  - Возможные интерпретации
  - Решение
  _... ещё 4 разделов_

_Слов: 346_

### [ADR: [Название решения]](templates/decision-record.md)
> > !NOTE

  - Статус
  - Контекст
  - Рассмотренные варианты
  - Принятое решение
  - Последствия
  - Использование
- Запуск
  - Смотрите также

_Слов: 134_

### [Ансамбль: [Название]](templates/ensemble.md)
> > !NOTE

  - Назначение
  - Компоненты
  - Архитектурная схема
  - Контракт взаимодействия
  - Риски и ограничения
  - MVP-шаги
  - Смотрите также

_Слов: 138_

### [Эксперимент: [Название]](templates/experiment-log.md)
> > experiment-log — раздел документации проекта Lorenzo.

  - Содержание
  - Гипотеза
  - Зачем
  - Метод
  - Журнал
  - Результат
  - Выводы
  - Следующие действия
  _... ещё 4 разделов_

_Слов: 347_

### [FAQ: [Вопрос]](templates/faq-entry.md)
> > faq-entry — раздел документации проекта Lorenzo.

  - Содержание
  - Вопрос
  - Краткий ответ
  - Подробный ответ
  - Когда это НЕ применимо
  - Связанные вопросы
  - Источники / документы
  - История обновлений
  _... ещё 3 разделов_

_Слов: 348_

### [[Термин]](templates/glossary-entry.md)
> > glossary-entry — раздел документации проекта Lorenzo.

  - Содержание
  - Определение
  - Происхождение
  - Синонимы и аббревиатуры
  - Примеры
  - Связанные термины
  - Где упоминается в монорепо
  - Источники
  _... ещё 3 разделов_

_Слов: 350_

### [KPI Snapshot: [дата]](templates/kpi-snapshot.md)
> > kpi-snapshot — раздел документации проекта Lorenzo.

  - Содержание
  - Период
  - Сводка
  - Детальные метрики
  - Лучшие изменения
  - Регрессии
  - Топ-3 фокуса на следующий период
  - Использование
  _... ещё 2 разделов_

_Слов: 353_

### [Юридический кейс: [Aktenzeichen]](templates/legal-case.md)
> > legal-case — раздел документации проекта Lorenzo.

  - Содержание
  - Идентификация
  - Стороны
  - Хронология
  - Предмет спора
  - Применимые нормы (§§)
  - Аргументы
  - Прецеденты
  _... ещё 7 разделов_

_Слов: 354_

### [Встреча: [Тема]](templates/meeting-notes.md)
> > meeting-notes — раздел документации проекта Lorenzo.

  - Содержание
  - Контекст
  - Участники
  - Повестка
  - Обсуждение
  - Принятые решения
  - Action Items
  - Открытые вопросы
  _... ещё 4 разделов_

_Слов: 344_

### [Mega-stack: [Название]](templates/mega-stack.md)
> > mega-stack — раздел документации проекта Lorenzo.

  - Назначение
  - Слои стека (сверху вниз)
  - Cross-layer контракты
  - Roadmap по фазам
  - Стоимость
  - Риски и митигации
  - Альтернативные стеки
  - Связанные ансамбли
  _... ещё 3 разделов_

_Слов: 410_

### [[Название компонента]](templates/project-component.md)
> > !NOTE

  - Что это
  - Ключевые особенности
  - Статус
  - Интеграция с Svyazi
  - Контакты
  - Использование
- Запуск
  - Смотрите также

_Слов: 136_

### [[Название протокола]](templates/protocol-spec.md)
> > protocol-spec — раздел документации проекта Lorenzo.

  - 0. Status of this Document
  - 1. Introduction
  - 2. Terminology
  - 3. Registry / Discovery
  - 4. Passport / Identity
  - 5. Compatibility Levels
  - 6. Adapter Interface
  - 7. PortalEntry
  _... ещё 11 разделов_

_Слов: 413_

### [MVP: [Название]](templates/prototype-mvp.md)
> > prototype-mvp — раздел документации проекта Lorenzo.

  - ID
  - Цель
  - Метрика успеха
  - Срок
  - Состав
  - Фазы
  - Open questions
  - Риски
  _... ещё 8 разделов_

_Слов: 427_

### [[Тема исследования]](templates/research-note.md)
> > !NOTE

  - Контекст
  - Ключевые находки
  - Источники
  - Открытые вопросы
  - Следующие шаги
  - Использование
- Запуск

_Слов: 102_

### [Ретроспектива: [период]](templates/retrospective.md)
> > retrospective — раздел документации проекта Lorenzo.

  - Содержание
  - Период
  - Что прошло хорошо ✅
  - Что прошло плохо ❌
  - Что узнали 💡
  - Action items для следующего периода
  - Метрики периода
  - Улучшения процесса
  _... ещё 3 разделов_

_Слов: 355_

### [RFC NNNN: [Название]](templates/rfc.md)
> > rfc — раздел документации проекта Lorenzo.

  - Содержание
  - Status of this Document
  - Abstract
  - 1. Introduction
  - 2. Specification
  - 3. Architecture
  - 4. Compatibility
  - 5. Security Considerations
  _... ещё 7 разделов_

_Слов: 323_

### [Риск: [Название]](templates/risk-entry.md)
> > risk-entry — раздел документации проекта Lorenzo.

  - Содержание
  - ID
  - Описание
  - Сценарий реализации
  - Оценка
  - Митигация
  - Триггеры мониторинга
  - История
  _... ещё 4 разделов_

_Слов: 353_

### [Tech Pair: [A] × [B]](templates/tech-pair.md)
> > tech-pair — раздел документации проекта Lorenzo.

  - Содержание
  - ID
  - Компонент A
  - Компонент B
  - Синергия
  - Архитектура
  - Контракт интеграции
  - Антисинергии
  _... ещё 6 разделов_

_Слов: 344_

### [Tech Radar: [Название]](templates/tech-radar-entry.md)
> > tech-radar-entry — раздел документации проекта Lorenzo.

  - Содержание
  - Quadrant
  - Ring
  - Описание
  - Почему именно этот ring
  - Когда использовать
  - Когда НЕ использовать
  - Альтернативы
  _... ещё 6 разделов_

_Слов: 345_

### [[имя нового шаблона]](templates/template-of-templates.md)
> > template-of-templates — раздел документации проекта Lorenzo.

  - Что делать
  - Обязательные блоки шаблона
- [Заголовок]
  - Смотрите также
  - Обязательные поля JSON-Schema
  - Чеклист добавления нового шаблона
  - Типичные паттерны
  - Смотрите также

_Слов: 364_

### [Еженедельный дайджест: [период]](templates/weekly-digest.md)
> > weekly-digest — раздел документации проекта Lorenzo.

  - Содержание
  - TL;DR
  - Что сделано
  - Метрики недели
  - Решения
  - Открытые вопросы недели
  - План на следующую неделю
  - Заметки
  _... ещё 3 разделов_

_Слов: 349_

**Итого в секции: 7,312 слов, 24 файлов**


## 🗺️ Тематическая карта

### Архитектура (537 документов)
- [[365-развёрнутый-анализ-внуковой-комбинации|`365-развёрнутый-анализ-внуковой-комбинации`]]
- [[CONCEPTS|`CONCEPTS`]]
- [[TABLES|`TABLES`]]
- [[00-intro|`00-intro`]]
- [[01-интегральный-анализ-профиля-svend4|`01-интегральный-анализ-профиля-svend4`]]
- _... ещё 532_

### Документация (172 документов)
- [[118-appendix-a-шаблон-для-header-warning|`118-appendix-a-шаблон-для-header-warning`]]
- [[98-appendix-a-minimal-working-example|`98-appendix-a-minimal-working-example`]]
- [[NAMED_ENTITIES|`NAMED_ENTITIES`]]
- [[22-glossary|`22-glossary`]]
- [[12-appendix-a-header-warning|`12-appendix-a-header-warning`]]
- _... ещё 167_

### Проекты (134 документов)
- [[CODE_BLOCKS|`CODE_BLOCKS`]]
- [[02-общий-план-развития-nautilus-portal-protocol|`02-общий-план-развития-nautilus-portal-protocol`]]
- [[228-appendix-c-quick-start-architecture-for-sgb-advoca|`228-appendix-c-quick-start-architecture-for-sgb-advoca`]]
- [[299-практические-рекомендации-для-текущего-проекта|`299-практические-рекомендации-для-текущего-проекта`]]
- [[336-10-стратегическое-позиционирование|`336-10-стратегическое-позиционирование`]]
- _... ещё 129_

### Код (132 документов)
- [[193-3-что-делает-агента-представительским|`193-3-что-делает-агента-представительским`]]
- [[DEPENDENCY_MAP|`DEPENDENCY_MAP`]]
- [[02-architecture|`02-architecture`]]
- [[04-enrichment|`04-enrichment`]]
- [[111-4-условия-применимости|`111-4-условия-применимости`]]
- _... ещё 127_

### Агенты (120 документов)
- [[C-multi-agent-factory|`C-multi-agent-factory`]]
- [[107-1-контекст-и-мотивация|`107-1-контекст-и-мотивация`]]
- [[108-2-формальный-workflow|`108-2-формальный-workflow`]]
- [[345-кто-ты|`345-кто-ты`]]
- [[357-твоя-коммуникация-в-outreach|`357-твоя-коммуникация-в-outreach`]]
- _... ещё 115_

### Контакты (56 документов)
- [[ngt-memory|`ngt-memory`]]
- [[REGISTRY|`REGISTRY`]]
- [[06-1-introduction|`06-1-introduction`]]
- [[105-review-methodology-md|`105-review-methodology-md`]]
- [[161-7-phased-rollout-plan|`161-7-phased-rollout-plan`]]
- _... ещё 51_

### Память (39 документов)
- [[PROCESSING_GUIDE|`PROCESSING_GUIDE`]]
- [[CHANGELOG|`CHANGELOG`]]
- [[SCRIPT_EVAL_REPORT|`SCRIPT_EVAL_REPORT`]]
- [[06-search|`06-search`]]
- [[11-integration-contracts|`11-integration-contracts`]]
- _... ещё 34_

### Анализ (26 документов)
- [[72-расписание-фазы-3|`72-расписание-фазы-3`]]
- [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|`110-вопрос-fallback-ratio-как-критический-или-осмыслен`]]
- [[145-8-call-to-action|`145-8-call-to-action`]]
- [[154-table-of-contents|`154-table-of-contents`]]
- [[162-8-risk-analysis|`162-8-risk-analysis`]]
- _... ещё 21_



## Использование
```bash
# Запуск
python scripts/improve_outline.py
```
```bash
# Вариант 2
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 3
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 4
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 5
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 6
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 7
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 8
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 9
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 10
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 11
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 12
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 13
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 14
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 15
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 16
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 17
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 18
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 19
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 20
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 21
python scripts/improve_outline.py --dry-run
```

<!-- backlinks -->

---

**Кто ссылается на этот документ (561):**
- [[00-intro-part2]]
- [[02-methodology]]
- [[06-security-privacy]]
- [[08-conclusions]]
- [[12-roadmap]]
- [[14-limitations]]
- [[110-вопрос-fallback-ratio-как-критический-или-осмыслен]]
- [[112-5-связь-с-существующими-методологиями]]
- _...ещё 553_



## Использование
```bash
# Запуск
python scripts/improve_outline.py
```
```bash
# Вариант 2
python scripts/improve_outline.py --dry-run
```
```bash
# Вариант 3
python scripts/improve_outline.py --dry-run
```
