# Outline базы знаний

<!-- toc -->
## Содержание

- [Содержание](#содержание)
- [Docs](#docs)
  - [[Словарь аббревиатур и сокращений](ABBREVIATIONS.md)](#словарь-аббревиатур-и-сокращенийabbreviationsmd)
  - [[Action Items, риски и решения](ACTION_ITEMS.md)](#action-items-риски-и-решенияaction_itemsmd)
  - [[Callout-блоки](ALERTS.md)](#callout-блокиalertsmd)
  - [[Авторы и коллаборации](AUTHORS.md)](#авторы-и-коллаборацииauthorsmd)
  - [[Автозаполненные шаблоны](AUTOFILLED.md)](#автозаполненные-шаблоныautofilledmd)
  - [[Индекс обратных ссылок](BACKLINKS.md)](#индекс-обратных-ссылокbacklinksmd)
  - [[Status Badges](BADGES.md)](#status-badgesbadgesmd)
  - [[CHANGELOG](CHANGELOG.md)](#changelogchangelogmd)
  - [[Changelog (авто)](CHANGELOG_AUTO.md)](#changelog-автоchangelog_automd)
  - [[Кластеры тематически близких файлов](CLUSTERS.md)](#кластеры-тематически-близких-файловclustersmd)
  - [[Code-блоки репозитория](CODE_BLOCKS.md)](#code-блоки-репозиторияcode_blocksmd)
  - [[Рекомендации по коллаборации (Collaboration Finder)](COLLAB_SUGGESTIONS.md)](#рекомендации-по-коллаборации-collaboration-findercollab_suggestionsmd)
  - [[Сравнение с предыдущим коммитом](COMPARE.md)](#сравнение-с-предыдущим-коммитомcomparemd)
  - [[Оценка читаемости документов](COMPLEXITY.md)](#оценка-читаемости-документовcomplexitymd)
  - [[Матрица компонентов Svyazi 2.0](COMPONENT_MATRIX.md)](#матрица-компонентов-svyazi-20component_matrixmd)
  - [[Глоссарий понятий](CONCEPTS.md)](#глоссарий-понятийconceptsmd)
  - [[Граф концептов базы знаний](CONCEPT_GRAPH.md)](#граф-концептов-базы-знанийconcept_graphmd)
  - [[Согласованность терминов](CONSISTENCY.md)](#согласованность-терминовconsistencymd)
  - [[Контакты и авторы](CONTACTS.md)](#контакты-и-авторыcontactsmd)
  - [[Приоритет контактов](CONTACT_PRIORITY.md)](#приоритет-контактовcontact_prioritymd)
  - [[Противоречия в базе знаний](CONTRADICTIONS.md)](#противоречия-в-базе-знанийcontradictionsmd)
  - [[Оценка стоимости MVP](COST.md)](#оценка-стоимости-mvpcostmd)
  - [[Перекрёстные ссылки](CROSSREFS.md)](#перекрёстные-ссылкиcrossrefsmd)
  - [[Кросс-секционный анализ](CROSS_SECTION.md)](#кросс-секционный-анализcross_sectionmd)
  - [[Ключевые решения и выводы](DECISIONS.md)](#ключевые-решения-и-выводыdecisionsmd)
  - [[Knowledge OS — Demo](DEMO.md)](#knowledge-os-demodemomd)
  - [[Карта плотности тем](DENSITY.md)](#карта-плотности-темdensitymd)
  - [[Мониторинг зависимостей](DEPENDABOT.md)](#мониторинг-зависимостейdependabotmd)
  - [[Карта зависимостей скриптов](DEPENDENCY_MAP.md)](#карта-зависимостей-скриптовdependency_mapmd)
  - [[Дайджест изменений](DIGEST.md)](#дайджест-измененийdigestmd)
  - [[Автодайджест изменений](DIGEST_AUTO.md)](#автодайджест-измененийdigest_automd)
  - [[Еженедельный дайджест — 2026-05-11](DIGEST_WEEKLY.md)](#еженедельный-дайджест-2026-05-11digest_weeklymd)
  - [[Отчёт о дублировании](DUPLICATES.md)](#отчёт-о-дублированииduplicatesmd)
  - [[Пустые секции](EMPTY_SECTIONS.md)](#пустые-секцииempty_sectionsmd)
  - [[Именованные сущности](ENTITIES.md)](#именованные-сущностиentitiesmd)
  - [[Часто задаваемые вопросы (FAQ)](FAQ.md)](#часто-задаваемые-вопросы-faqfaqmd)
  - [[Сноски и определения терминов](FOOTNOTES.md)](#сноски-и-определения-терминовfootnotesmd)
  - [[Lorenzo Gateway](GATEWAY.md)](#lorenzo-gatewaygatewaymd)
  - [[Глоссарий проектов](GLOSSARY.md)](#глоссарий-проектовglossarymd)
  - [[Граф связей проектов](GRAPH.md)](#граф-связей-проектовgraphmd)
  - [[Аудит заголовков](HEADING_AUDIT.md)](#аудит-заголовковheading_auditmd)
  - [[Health Dashboard](HEALTH.md)](#health-dashboardhealthmd)
  - [[Тепловая карта тем](HEATMAP.md)](#тепловая-карта-темheatmapmd)
  - [[Индекс документации — Lorenzo / Svyazi 2.0](INDEX.md)](#индекс-документации-lorenzo-svyazi-20indexmd)
  - [[Инвертированный индекс ключевых слов](KEYWORD_INDEX.md)](#инвертированный-индекс-ключевых-словkeyword_indexmd)
  - [[Карта базы знаний Lorenzo](KNOWLEDGE_MAP.md)](#карта-базы-знаний-lorenzoknowledge_mapmd)
  - [[Числовые KPI и метрики](KPI.md)](#числовые-kpi-и-метрикиkpimd)
  - [[История метрик KPI](KPI_HISTORY.md)](#история-метрик-kpikpi_historymd)
  - [[Языковой состав документов](LANGUAGE_STATS.md)](#языковой-состав-документовlanguage_statsmd)
  - [[Индекс ссылок](LINKS.md)](#индекс-ссылокlinksmd)
  - [[AI-саммари разделов документации](LLM_SUMMARIES.md)](#ai-саммари-разделов-документацииllm_summariesmd)
  - [[MCP Dashboard](MCP_DASHBOARD.md)](#mcp-dashboardmcp_dashboardmd)
  - [[Методология работы со скриптами](METHODOLOGY.md)](#методология-работы-со-скриптамиmethodologymd)
  - [[Метрики качества документации](METRICS.md)](#метрики-качества-документацииmetricsmd)
  - [[Майндмап репозитория Lorenzo](MINDMAP.md)](#майндмап-репозитория-lorenzomindmapmd)
  - [[Карта пробелов знаний](MISSING.md)](#карта-пробелов-знанийmissingmd)
  - [[Индекс именованных сущностей](NAMED_ENTITIES.md)](#индекс-именованных-сущностейnamed_entitiesmd)
  - [[Нарратив проекта Lorenzo](NARRATIVE.md)](#нарратив-проекта-lorenzonarrativemd)
  - [[Сеть проектов и авторов](NETWORK.md)](#сеть-проектов-и-авторовnetworkmd)
  - [[Онбординг — Svyazi 2.0 / Lorenzo](ONBOARDING.md)](#онбординг-svyazi-20-lorenzoonboardingmd)
  - [[Изолированные документы (Orphans)](ORPHANS.md)](#изолированные-документы-orphansorphansmd)
  - [[Качество абзацев](PARAGRAPH_QUALITY.md)](#качество-абзацевparagraph_qualitymd)
  - [[Пассивный залог и канцеляризмы](PASSIVE_VOICE.md)](#пассивный-залог-и-канцеляризмыpassive_voicemd)
  - [[Retrieval Hit Rate Evaluation — Lorenzo / Svyazi 2.0](PRECISION_EVAL.md)](#retrieval-hit-rate-evaluation-lorenzo-svyazi-20precision_evalmd)
  - [[Приоритеты файлов](PRIORITIES.md)](#приоритеты-файловprioritiesmd)
  - [[Прогресс MVP](PROGRESS.md)](#прогресс-mvpprogressmd)
  - [[Svyazi 2.0 — Спецификация прототипа](PROTOTYPE_SPEC.md)](#svyazi-20-спецификация-прототипаprototype_specmd)
  - [[Глобальный Q&A](QA.md)](#глобальный-qaqamd)
  - [[Открытые вопросы](QUESTIONS.md)](#открытые-вопросыquestionsmd)
  - [[Список чтения](READING_LIST.md)](#список-чтенияreading_listmd)
  - [[Рекомендуемый порядок чтения](READING_ORDER.md)](#рекомендуемый-порядок-чтенияreading_ordermd)
  - [[docs](README.md)](#docsreadmemd)
  - [[REGISTRY — реестр артефактов Lorenzo](REGISTRY.md)](#registry-реестр-артефактов-lorenzoregistrymd)
  - [[Svyazi 2.0 — Knowledge Base Report](REPORT.md)](#svyazi-20-knowledge-base-reportreportmd)
  - [[Реестр рисков — Svyazi 2.0](RISK_REGISTER.md)](#реестр-рисков-svyazi-20risk_registermd)
  - [[Расписание проекта](SCHEDULE.md)](#расписание-проектаschedulemd)
  - [[Оценка готовности проекта (Go/No-Go)](SCORING.md)](#оценка-готовности-проекта-gono-goscoringmd)
  - [[Каталог скриптов](SCRIPTS_CATALOG.md)](#каталог-скриптовscripts_catalogmd)
  - [[Отчёт об оценке скриптов Lorenzo](SCRIPT_EVAL_REPORT.md)](#отчёт-об-оценке-скриптов-lorenzoscript_eval_reportmd)
  - [[Результаты поиска](SEARCH_RESULTS.md)](#результаты-поискаsearch_resultsmd)
  - [[Индекс «Смотрите также»](SEE_ALSO.md)](#индекс-смотрите-такжеsee_alsomd)
  - [[Тональный анализ документов](SENTIMENT.md)](#тональный-анализ-документовsentimentmd)
  - [[SENTINEL Security Report](SENTINEL.md)](#sentinel-security-reportsentinelmd)
  - [[Похожие документы](SIMILAR.md)](#похожие-документыsimilarmd)
  - [[Похожие абзацы между документами](SIMILAR_PASSAGES.md)](#похожие-абзацы-между-документамиsimilar_passagesmd)
  - [[Карта репозитория Lorenzo](SITEMAP.md)](#карта-репозитория-lorenzositemapmd)
  - [[Skill Dashboard](SKILL_DASHBOARD.md)](#skill-dashboardskill_dashboardmd)
  - [[Карта происхождения текстов](SOURCE_MAP.md)](#карта-происхождения-текстовsource_mapmd)
  - [[Детальная статистика репозитория](STATS.md)](#детальная-статистика-репозиторияstatsmd)
  - [[Резюме документов (TextRank)](SUMMARIES.md)](#резюме-документов-textranksummariesmd)
  - [[Все таблицы репозитория](TABLES.md)](#все-таблицы-репозиторияtablesmd)
  - [[Индекс тегов](TAGS.md)](#индекс-теговtagsmd)
  - [[Каталог задач (TASKSINDEX)](TASKS_INDEX.md)](#каталог-задач-tasksindextasks_indexmd)
  - [[Tech Radar — Svyazi 2.0](TECH_RADAR.md)](#tech-radar-svyazi-20tech_radarmd)
  - [[Хронология и временные маркеры](TIMELINE.md)](#хронология-и-временные-маркерыtimelinemd)
  - [[Валидация шаблонов](VALIDATION.md)](#валидация-шаблоновvalidationmd)
  - [[Богатство словаря документов](VOCABULARY.md)](#богатство-словаря-документовvocabularymd)
  - [[Word Cloud](WORD_CLOUD.md)](#word-cloudword_cloudmd)
  - [[Частотный анализ слов](WORD_FREQ.md)](#частотный-анализ-словword_freqmd)
  - [[Reading paths — рекомендуемые маршруты по монорепозиторию](reading-paths.md)](#reading-paths-рекомендуемые-маршруты-по-монорепозиториюreading-pathsmd)
- [Svyazi](#svyazi)
  - [[Продолжение исследования для Svyazi[^svyazi] 2.0](01-svyazi/00-intro-part2.md)](#продолжение-исследования-для-svyazisvyazi-2001-svyazi00-intro-part2md)
  - [[Svyazi[^svyazi] 2.0 — Исполнительное резюме](01-svyazi/01-executive-summary.md)](#svyazisvyazi-20-исполнительное-резюме01-svyazi01-executive-summarymd)
  - [[Методика и рамка отбора проектов](01-svyazi/02-methodology.md)](#методика-и-рамка-отбора-проектов01-svyazi02-methodologymd)
  - [[Каталог компонентов Svyazi 2.0](01-svyazi/03-component-catalog.md)](#каталог-компонентов-svyazi-2001-svyazi03-component-catalogmd)
  - [[Приоритетные ансамбли проектов](01-svyazi/04-ensembles-overview.md)](#приоритетные-ансамбли-проектов01-svyazi04-ensembles-overviewmd)
  - [[Безопасность и приватность](01-svyazi/06-security-privacy.md)](#безопасность-и-приватность01-svyazi06-security-privacymd)
  - [[Планирование MVP](01-svyazi/07-mvp-planning.md)](#планирование-mvp01-svyazi07-mvp-planningmd)
  - [[Выводы](01-svyazi/08-conclusions.md)](#выводы01-svyazi08-conclusionsmd)
  - [[Архитектурные зазоры](01-svyazi/09-architectural-gaps.md)](#архитектурные-зазоры01-svyazi09-architectural-gapsmd)
  - [[Ансамбли следующего шага](01-svyazi/10-second-order-ensembles.md)](#ансамбли-следующего-шага01-svyazi10-second-order-ensemblesmd)
  - [[Интеграционные контракты](01-svyazi/11-integration-contracts.md)](#интеграционные-контракты01-svyazi11-integration-contractsmd)
  - [[Дорожная карта прототипа](01-svyazi/12-roadmap.md)](#дорожная-карта-прототипа01-svyazi12-roadmapmd)
  - [[Контактная стратегия](01-svyazi/13-contacts.md)](#контактная-стратегия01-svyazi13-contactsmd)
  - [[Ограничения и лицензии](01-svyazi/14-limitations.md)](#ограничения-и-лицензии01-svyazi14-limitationsmd)
  - [[Q&A: 01-svyazi](01-svyazi/QA.md)](#qa-01-svyazi01-svyaziqamd)
  - [[Svyazi[^svyazi] 2.0 — Архитектура и исследование](01-svyazi/README.md)](#svyazisvyazi-20-архитектура-и-исследование01-svyazireadmemd)
- [Anthropic Vacancies](#anthropic-vacancies)
  - [[Введение](02-anthropic-vacancies/00-intro.md)](#введение02-anthropic-vacancies00-intromd)
  - [[Интегральный анализ профиля svend4](02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)](#интегральный-анализ-профиля-svend402-anthropic-vacancies01-интегральный-анализ-профиля-svend4md)
  - [[ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md)](#общий-план-развития-nautilus-portal-protocol02-anthropic-vacancies02-общий-план-развития-nautilus-portal-protocolmd)
  - [[PORTAL-PROTOCOL.md](02-anthropic-vacancies/03-portal-protocol-md.md)](#portal-protocolmd02-anthropic-vacancies03-portal-protocol-mdmd)
  - [[Abstract](02-anthropic-vacancies/04-abstract.md)](#abstract02-anthropic-vacancies04-abstractmd)
  - [[0. Status of This Document](02-anthropic-vacancies/05-0-status-of-this-document.md)](#0-status-of-this-document02-anthropic-vacancies05-0-status-of-this-documentmd)
  - [[1. Introduction](02-anthropic-vacancies/06-1-introduction.md)](#1-introduction02-anthropic-vacancies06-1-introductionmd)
  - [[2. Terminology](02-anthropic-vacancies/07-2-terminology.md)](#2-terminology02-anthropic-vacancies07-2-terminologymd)
  - [[3. Registry (nautilus.json)](02-anthropic-vacancies/08-3-registry-nautilus-json.md)](#3-registry-nautilusjson02-anthropic-vacancies08-3-registry-nautilus-jsonmd)
  - [[4. Passport (passport.md)](02-anthropic-vacancies/09-4-passport-passport-md.md)](#4-passport-passportmd02-anthropic-vacancies09-4-passport-passport-mdmd)
  - [[Доступ к данным](02-anthropic-vacancies/102-доступ-к-данным.md)](#доступ-к-данным02-anthropic-vacancies102-доступ-к-даннымmd)
  - [[Appendix B: Change Log](02-anthropic-vacancies/103-appendix-b-change-log.md)](#appendix-b-change-log02-anthropic-vacancies103-appendix-b-change-logmd)
  - [[Appendix C: References](02-anthropic-vacancies/104-appendix-c-references.md)](#appendix-c-references02-anthropic-vacancies104-appendix-c-referencesmd)
  - [[REVIEWMETHODOLOGY.md](02-anthropic-vacancies/105-review-methodology-md.md)](#reviewmethodologymd02-anthropic-vacancies105-review-methodology-mdmd)
  - [[TL;DR](02-anthropic-vacancies/106-tl-dr.md)](#tldr02-anthropic-vacancies106-tl-drmd)
  - [[1. Контекст и мотивация](02-anthropic-vacancies/107-1-контекст-и-мотивация.md)](#1-контекст-и-мотивация02-anthropic-vacancies107-1-контекст-и-мотивацияmd)
  - [[2. Формальный workflow](02-anthropic-vacancies/108-2-формальный-workflow.md)](#2-формальный-workflow02-anthropic-vacancies108-2-формальный-workflowmd)
  - [[3. Принципы консолидации (Фаза C)](02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md)](#3-принципы-консолидации-фаза-c02-anthropic-vacancies109-3-принципы-консолидации-фаза-cmd)
  - [[Вопрос: fallback-ratio как критический или осмысленный?](02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md)](#вопрос-fallback-ratio-как-критический-или-осмысленный02-anthropic-vacancies110-вопрос-fallback-ratio-как-критический-или-осмысленmd)
  - [[4. Условия применимости](02-anthropic-vacancies/111-4-условия-применимости.md)](#4-условия-применимости02-anthropic-vacancies111-4-условия-применимостиmd)
  - [[5. Связь с существующими методологиями](02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md)](#5-связь-с-существующими-методологиями02-anthropic-vacancies112-5-связь-с-существующими-методологиямиmd)
  - [[6. Почему это валидный паттерн для AI-assisted workflows](02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md)](#6-почему-это-валидный-паттерн-для-ai-assisted-workflows02-anthropic-vacancies113-6-почему-это-валидный-паттерн-для-ai-assisted-workmd)
  - [[7. Реализация в проекте Nautilus](02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md)](#7-реализация-в-проекте-nautilus02-anthropic-vacancies114-7-реализация-в-проекте-nautilusmd)
  - [[8. Ограничения и открытые вопросы](02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md)](#8-ограничения-и-открытые-вопросы02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd)
  - [[9. Checklist применения методологии](02-anthropic-vacancies/116-9-checklist-применения-методологии.md)](#9-checklist-применения-методологии02-anthropic-vacancies116-9-checklist-применения-методологииmd)
  - [[10. Конкретный план применения к текущим документам](02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md)](#10-конкретный-план-применения-к-текущим-документам02-anthropic-vacancies117-10-конкретный-план-применения-к-текущим-документамmd)
  - [[Appendix A: Шаблон для header warning](02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md)](#appendix-a-шаблон-для-header-warning02-anthropic-vacancies118-appendix-a-шаблон-для-header-warningmd)
  - [[Appendix B: Примеры расхождений и их разрешения](02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md)](#appendix-b-примеры-расхождений-и-их-разрешения02-anthropic-vacancies119-appendix-b-примеры-расхождений-и-их-разрешенияmd)
  - [[Content Overview](02-anthropic-vacancies/12-content-overview.md)](#content-overview02-anthropic-vacancies12-content-overviewmd)
  - [[Главные технические риски](02-anthropic-vacancies/120-главные-технические-риски.md)](#главные-технические-риски02-anthropic-vacancies120-главные-технические-рискиmd)
  - [[Appendix C: История изменений методологии](02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md)](#appendix-c-история-изменений-методологии02-anthropic-vacancies121-appendix-c-история-изменений-методологииmd)
  - [[Глоссарий](02-anthropic-vacancies/122-глоссарий.md)](#глоссарий02-anthropic-vacancies122-глоссарийmd)
  - [[portal-mcp.py](02-anthropic-vacancies/123-portal-mcp-py.md)](#portal-mcppy02-anthropic-vacancies123-portal-mcp-pymd)
  - [[Конфигурация для Claude Desktop](02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md)](#конфигурация-для-claude-desktop02-anthropic-vacancies124-конфигурация-для-claude-desktopmd)
  - [[README-MCP.md— инструкция по установке](02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md)](#readme-mcpmd-инструкция-по-установке02-anthropic-vacancies125-readme-mcp-md-инструкция-по-установкеmd)
  - [[Установка](02-anthropic-vacancies/126-установка.md)](#установка02-anthropic-vacancies126-установкаmd)
  - [[Подключение к Claude Desktop](02-anthropic-vacancies/127-подключение-к-claude-desktop.md)](#подключение-к-claude-desktop02-anthropic-vacancies127-подключение-к-claude-desktopmd)
  - [[Доступные инструменты](02-anthropic-vacancies/128-доступные-инструменты.md)](#доступные-инструменты02-anthropic-vacancies128-доступные-инструментыmd)
  - [[Примеры запросов (в Claude)](02-anthropic-vacancies/129-примеры-запросов-в-claude.md)](#примеры-запросов-в-claude02-anthropic-vacancies129-примеры-запросов-в-claudemd)
  - [[Angle / Perspective](02-anthropic-vacancies/13-angle-perspective.md)](#angle-perspective02-anthropic-vacancies13-angle-perspectivemd)
  - [[Отладка](02-anthropic-vacancies/130-отладка.md)](#отладка02-anthropic-vacancies130-отладкаmd)
  - [[Ограничения текущей версии (0.1.0-draft)](02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md)](#ограничения-текущей-версии-010-draft02-anthropic-vacancies131-ограничения-текущей-версии-0-1-0-draftmd)
  - [[Planned (v0.2.0)](02-anthropic-vacancies/132-planned-v0-2-0.md)](#planned-v02002-anthropic-vacancies132-planned-v0-2-0md)
  - [[Обратная связь](02-anthropic-vacancies/133-обратная-связь.md)](#обратная-связь02-anthropic-vacancies133-обратная-связьmd)
  - [[THE DOUBLE-TRIANGLE ARCHITECTURE.md](02-anthropic-vacancies/134-the-double-triangle-architecture-md.md)](#the-double-triangle-architecturemd02-anthropic-vacancies134-the-double-triangle-architecture-mdmd)
  - [[A Formal Model for Human-AI Collaboration in Distributed Knowledge Work](02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md)](#a-formal-model-for-human-ai-collaboration-in-distributed-knowledge-work02-anthropic-vacancies135-a-formal-model-for-human-ai-collaboration-in-distrmd)
  - [[Abstract](02-anthropic-vacancies/136-abstract.md)](#abstract02-anthropic-vacancies136-abstractmd)
  - [[Table of Contents](02-anthropic-vacancies/137-table-of-contents.md)](#table-of-contents02-anthropic-vacancies137-table-of-contentsmd)
  - [[1. Why Single-Triangle Models Are Incomplete](02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md)](#1-why-single-triangle-models-are-incomplete02-anthropic-vacancies138-1-why-single-triangle-models-are-incompletemd)
  - [[2. The Double-Triangle Architecture](02-anthropic-vacancies/139-2-the-double-triangle-architecture.md)](#2-the-double-triangle-architecture02-anthropic-vacancies139-2-the-double-triangle-architecturemd)
  - [[3. Three Inter-Layer Protocols](02-anthropic-vacancies/140-3-three-inter-layer-protocols.md)](#3-three-inter-layer-protocols02-anthropic-vacancies140-3-three-inter-layer-protocolsmd)
  - [[4. Nautilus Portal as Reference Substrate](02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md)](#4-nautilus-portal-as-reference-substrate02-anthropic-vacancies141-4-nautilus-portal-as-reference-substratemd)
  - [[5. Pattern Library as Bridge Between Triangles](02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md)](#5-pattern-library-as-bridge-between-triangles02-anthropic-vacancies142-5-pattern-library-as-bridge-between-trianglesmd)
  - [[6. Four Deployment Domains](02-anthropic-vacancies/143-6-four-deployment-domains.md)](#6-four-deployment-domains02-anthropic-vacancies143-6-four-deployment-domainsmd)
  - [[7. Open Questions](02-anthropic-vacancies/144-7-open-questions.md)](#7-open-questions02-anthropic-vacancies144-7-open-questionsmd)
  - [[8. Call to Action](02-anthropic-vacancies/145-8-call-to-action.md)](#8-call-to-action02-anthropic-vacancies145-8-call-to-actionmd)
  - [[Acknowledgments](02-anthropic-vacancies/146-acknowledgments.md)](#acknowledgments02-anthropic-vacancies146-acknowledgmentsmd)
  - [[References](02-anthropic-vacancies/147-references.md)](#references02-anthropic-vacancies147-referencesmd)
  - [[Appendix A: Glossary](02-anthropic-vacancies/148-appendix-a-glossary.md)](#appendix-a-glossary02-anthropic-vacancies148-appendix-a-glossarymd)
  - [[Appendix B: Summary of Contributions](02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md)](#appendix-b-summary-of-contributions02-anthropic-vacancies149-appendix-b-summary-of-contributionsmd)
  - [[Appendix C: Version History](02-anthropic-vacancies/150-appendix-c-version-history.md)](#appendix-c-version-history02-anthropic-vacancies150-appendix-c-version-historymd)
  - [[OPEN KNOWLEDGE WORK FOUNDATION.md](02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md)](#open-knowledge-work-foundationmd02-anthropic-vacancies151-open-knowledge-work-foundation-mdmd)
  - [[AI-Coordinated Infrastructure for Distributed Expert Contribution](02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md)](#ai-coordinated-infrastructure-for-distributed-expert-contribution02-anthropic-vacancies152-ai-coordinated-infrastructure-for-distributed-expemd)
  - [[Executive Summary](02-anthropic-vacancies/153-executive-summary.md)](#executive-summary02-anthropic-vacancies153-executive-summarymd)
  - [[Table of Contents](02-anthropic-vacancies/154-table-of-contents.md)](#table-of-contents02-anthropic-vacancies154-table-of-contentsmd)
  - [[1. Problem Statement](02-anthropic-vacancies/155-1-problem-statement.md)](#1-problem-statement02-anthropic-vacancies155-1-problem-statementmd)
  - [[2. Target Populations](02-anthropic-vacancies/156-2-target-populations.md)](#2-target-populations02-anthropic-vacancies156-2-target-populationsmd)
  - [[3. Why Existing Solutions Fail](02-anthropic-vacancies/157-3-why-existing-solutions-fail.md)](#3-why-existing-solutions-fail02-anthropic-vacancies157-3-why-existing-solutions-failmd)
  - [[4. Proposed Infrastructure](02-anthropic-vacancies/158-4-proposed-infrastructure.md)](#4-proposed-infrastructure02-anthropic-vacancies158-4-proposed-infrastructuremd)
  - [[5. Economic Model](02-anthropic-vacancies/159-5-economic-model.md)](#5-economic-model02-anthropic-vacancies159-5-economic-modelmd)
  - [[History](02-anthropic-vacancies/16-history.md)](#history02-anthropic-vacancies16-historymd)
  - [[6. Governance and Ethics](02-anthropic-vacancies/160-6-governance-and-ethics.md)](#6-governance-and-ethics02-anthropic-vacancies160-6-governance-and-ethicsmd)
  - [[7. Phased Rollout Plan](02-anthropic-vacancies/161-7-phased-rollout-plan.md)](#7-phased-rollout-plan02-anthropic-vacancies161-7-phased-rollout-planmd)
  - [[8. Risk Analysis](02-anthropic-vacancies/162-8-risk-analysis.md)](#8-risk-analysis02-anthropic-vacancies162-8-risk-analysismd)
  - [[9. Call for Partnership](02-anthropic-vacancies/163-9-call-for-partnership.md)](#9-call-for-partnership02-anthropic-vacancies163-9-call-for-partnershipmd)
  - [[10. Appendices](02-anthropic-vacancies/164-10-appendices.md)](#10-appendices02-anthropic-vacancies164-10-appendicesmd)
  - [[Closing](02-anthropic-vacancies/165-closing.md)](#closing02-anthropic-vacancies165-closingmd)
  - [[REPRESENTATIVE AGENT LAYER.md](02-anthropic-vacancies/166-representative-agent-layer-md.md)](#representative-agent-layermd02-anthropic-vacancies166-representative-agent-layer-mdmd)
  - [[AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations](02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md)](#ai-mediated-representation-for-underrepresented-experts-and-vulnerable-populations02-anthropic-vacancies167-ai-mediated-representation-for-underrepresented-exmd)
  - [[Abstract](02-anthropic-vacancies/168-abstract.md)](#abstract02-anthropic-vacancies168-abstractmd)
  - [[Table of Contents](02-anthropic-vacancies/169-table-of-contents.md)](#table-of-contents02-anthropic-vacancies169-table-of-contentsmd)
  - [[5. Compatibility Levels](02-anthropic-vacancies/17-5-compatibility-levels.md)](#5-compatibility-levels02-anthropic-vacancies17-5-compatibility-levelsmd)
  - [[1. The Cinderella Syndrome: Why Quality Stays Invisible](02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md)](#1-the-cinderella-syndrome-why-quality-stays-invisible02-anthropic-vacancies170-1-the-cinderella-syndrome-why-quality-stays-invisimd)
  - [[2. Historical Precedents: Agents as Civilizational Innovation](02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md)](#2-historical-precedents-agents-as-civilizational-innovation02-anthropic-vacancies171-2-historical-precedents-agents-as-civilizational-imd)
  - [[3. What Makes a Representative Agent](02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md)](#3-what-makes-a-representative-agent02-anthropic-vacancies172-3-what-makes-a-representative-agentmd)
  - [[4. Ten Domains of Application](02-anthropic-vacancies/173-4-ten-domains-of-application.md)](#4-ten-domains-of-application02-anthropic-vacancies173-4-ten-domains-of-applicationmd)
  - [[5. Architectural Specification](02-anthropic-vacancies/174-5-architectural-specification.md)](#5-architectural-specification02-anthropic-vacancies174-5-architectural-specificationmd)
  - [[6. Ethical Framework](02-anthropic-vacancies/175-6-ethical-framework.md)](#6-ethical-framework02-anthropic-vacancies175-6-ethical-frameworkmd)
  - [[7. Governance and Oversight](02-anthropic-vacancies/176-7-governance-and-oversight.md)](#7-governance-and-oversight02-anthropic-vacancies176-7-governance-and-oversightmd)
  - [[8. Risks and Mitigations](02-anthropic-vacancies/177-8-risks-and-mitigations.md)](#8-risks-and-mitigations02-anthropic-vacancies177-8-risks-and-mitigationsmd)
  - [[9. Phased Rollout Strategy](02-anthropic-vacancies/178-9-phased-rollout-strategy.md)](#9-phased-rollout-strategy02-anthropic-vacancies178-9-phased-rollout-strategymd)
  - [[10. Open Questions](02-anthropic-vacancies/179-10-open-questions.md)](#10-open-questions02-anthropic-vacancies179-10-open-questionsmd)
  - [[6. Adapter Interface](02-anthropic-vacancies/18-6-adapter-interface.md)](#6-adapter-interface02-anthropic-vacancies18-6-adapter-interfacemd)
  - [[11. Call for Collaboration](02-anthropic-vacancies/180-11-call-for-collaboration.md)](#11-call-for-collaboration02-anthropic-vacancies180-11-call-for-collaborationmd)
  - [[12. Closing](02-anthropic-vacancies/181-12-closing.md)](#12-closing02-anthropic-vacancies181-12-closingmd)
  - [[Acknowledgments](02-anthropic-vacancies/182-acknowledgments.md)](#acknowledgments02-anthropic-vacancies182-acknowledgmentsmd)
  - [[References](02-anthropic-vacancies/183-references.md)](#references02-anthropic-vacancies183-referencesmd)
  - [[Appendix A: Connection to Companion Papers](02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md)](#appendix-a-connection-to-companion-papers02-anthropic-vacancies184-appendix-a-connection-to-companion-papersmd)
  - [[Appendix B: Domain Comparison Matrix](02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md)](#appendix-b-domain-comparison-matrix02-anthropic-vacancies185-appendix-b-domain-comparison-matrixmd)
  - [[Appendix C: Sample Use Cases in Detail](02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md)](#appendix-c-sample-use-cases-in-detail02-anthropic-vacancies186-appendix-c-sample-use-cases-in-detailmd)
  - [[СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md](02-anthropic-vacancies/187-слой-представительских-агентов-md.md)](#слой-представительских-агентовmd02-anthropic-vacancies187-слой-представительских-агентов-mdmd)
  - [[AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения](02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md)](#ai-опосредованное-представительство-для-недопредставленных-экспертов-и-уязвимых-категорий-населения02-anthropic-vacancies188-ai-опосредованное-представительство-для-недопредстmd)
  - [[Аннотация](02-anthropic-vacancies/189-аннотация.md)](#аннотация02-anthropic-vacancies189-аннотацияmd)
  - [[7. PortalEntry Structure](02-anthropic-vacancies/19-7-portalentry-structure.md)](#7-portalentry-structure02-anthropic-vacancies19-7-portalentry-structuremd)
  - [[Содержание](02-anthropic-vacancies/190-содержание.md)](#содержание02-anthropic-vacancies190-содержаниеmd)
  - [[1. Синдром Золушки: Почему качество остаётся невидимым](02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md)](#1-синдром-золушки-почему-качество-остаётся-невидимым02-anthropic-vacancies191-1-синдром-золушки-почему-качество-остаётся-невидимmd)
  - [[2. Исторические прецеденты: Агенты как цивилизационная инновация](02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md)](#2-исторические-прецеденты-агенты-как-цивилизационная-инновация02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd)
  - [[3. Что делает агента Представительским](02-anthropic-vacancies/193-3-что-делает-агента-представительским.md)](#3-что-делает-агента-представительским02-anthropic-vacancies193-3-что-делает-агента-представительскимmd)
  - [[4. Десять областей применения](02-anthropic-vacancies/194-4-десять-областей-применения.md)](#4-десять-областей-применения02-anthropic-vacancies194-4-десять-областей-примененияmd)
  - [[5. Архитектурная спецификация](02-anthropic-vacancies/195-5-архитектурная-спецификация.md)](#5-архитектурная-спецификация02-anthropic-vacancies195-5-архитектурная-спецификацияmd)
  - [[6. Этическая рамка](02-anthropic-vacancies/196-6-этическая-рамка.md)](#6-этическая-рамка02-anthropic-vacancies196-6-этическая-рамкаmd)
  - [[7. Управление и надзор](02-anthropic-vacancies/197-7-управление-и-надзор.md)](#7-управление-и-надзор02-anthropic-vacancies197-7-управление-и-надзорmd)
  - [[8. Риски и меры противодействия](02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md)](#8-риски-и-меры-противодействия02-anthropic-vacancies198-8-риски-и-меры-противодействияmd)
  - [[9. Стратегия поэтапного развёртывания](02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md)](#9-стратегия-поэтапного-развёртывания02-anthropic-vacancies199-9-стратегия-поэтапного-развёртыванияmd)
  - [[8. Consensus Algorithm](02-anthropic-vacancies/20-8-consensus-algorithm.md)](#8-consensus-algorithm02-anthropic-vacancies20-8-consensus-algorithmmd)
  - [[10. Открытые вопросы](02-anthropic-vacancies/200-10-открытые-вопросы.md)](#10-открытые-вопросы02-anthropic-vacancies200-10-открытые-вопросыmd)
  - [[11. Призыв к сотрудничеству](02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md)](#11-призыв-к-сотрудничеству02-anthropic-vacancies201-11-призыв-к-сотрудничествуmd)
  - [[12. Заключение](02-anthropic-vacancies/202-12-заключение.md)](#12-заключение02-anthropic-vacancies202-12-заключениеmd)
  - [[Благодарности](02-anthropic-vacancies/203-благодарности.md)](#благодарности02-anthropic-vacancies203-благодарностиmd)
  - [[Ссылки](02-anthropic-vacancies/204-ссылки.md)](#ссылки02-anthropic-vacancies204-ссылкиmd)
  - [[Приложение A: Связь с Сопроводительными Статьями](02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md)](#приложение-a-связь-с-сопроводительными-статьями02-anthropic-vacancies205-приложение-a-связь-с-сопроводительными-статьямиmd)
  - [[Приложение B: Матрица Сравнения Областей](02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md)](#приложение-b-матрица-сравнения-областей02-anthropic-vacancies206-приложение-b-матрица-сравнения-областейmd)
  - [[Приложение C: Образцы Случаев Использования в Деталях](02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md)](#приложение-c-образцы-случаев-использования-в-деталях02-anthropic-vacancies207-приложение-c-образцы-случаев-использования-в-деталmd)
  - [[PROFESSIONAL COLLEAGUE AGENTS.md](02-anthropic-vacancies/208-professional-colleague-agents-md.md)](#professional-colleague-agentsmd02-anthropic-vacancies208-professional-colleague-agents-mdmd)
  - [[A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers](02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md)](#a-typology-of-ai-agents-on-the-principal-side-and-the-case-for-profession-specific-co-workers02-anthropic-vacancies209-a-typology-of-ai-agents-on-the-principal-side-and-md)
  - [[9. Query Flow](02-anthropic-vacancies/21-9-query-flow.md)](#9-query-flow02-anthropic-vacancies21-9-query-flowmd)
  - [[Abstract](02-anthropic-vacancies/210-abstract.md)](#abstract02-anthropic-vacancies210-abstractmd)
  - [[Table of Contents](02-anthropic-vacancies/211-table-of-contents.md)](#table-of-contents02-anthropic-vacancies211-table-of-contentsmd)
  - [[1. The Five-Type Typology of Principal-Side Agents](02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md)](#1-the-five-type-typology-of-principal-side-agents02-anthropic-vacancies212-1-the-five-type-typology-of-principal-side-agentsmd)
  - [[2. What Makes a Professional Colleague Agent](02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md)](#2-what-makes-a-professional-colleague-agent02-anthropic-vacancies213-2-what-makes-a-professional-colleague-agentmd)
  - [[3. Empirical Case Study: «Обучай»](02-anthropic-vacancies/214-3-empirical-case-study-обучай.md)](#3-empirical-case-study-обучай02-anthropic-vacancies214-3-empirical-case-study-обучайmd)
  - [[4. Architecture of Professional Colleague Agents](02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md)](#4-architecture-of-professional-colleague-agents02-anthropic-vacancies215-4-architecture-of-professional-colleague-agentsmd)
  - [[5. The Economics of Profession-Wide Replication](02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md)](#5-the-economics-of-profession-wide-replication02-anthropic-vacancies216-5-the-economics-of-profession-wide-replicationmd)
  - [[6. Risks Specific to this Category](02-anthropic-vacancies/217-6-risks-specific-to-this-category.md)](#6-risks-specific-to-this-category02-anthropic-vacancies217-6-risks-specific-to-this-categorymd)
  - [[7. Application Domains](02-anthropic-vacancies/218-7-application-domains.md)](#7-application-domains02-anthropic-vacancies218-7-application-domainsmd)
  - [[8. Pilot Proposal: SGB Advocate Colleague](02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md)](#8-pilot-proposal-sgb-advocate-colleague02-anthropic-vacancies219-8-pilot-proposal-sgb-advocate-colleaguemd)
  - [[10. QueryResult Structure](02-anthropic-vacancies/22-10-queryresult-structure.md)](#10-queryresult-structure02-anthropic-vacancies22-10-queryresult-structuremd)
  - [[9. Relationship to Other Agent Types](02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md)](#9-relationship-to-other-agent-types02-anthropic-vacancies220-9-relationship-to-other-agent-typesmd)
  - [[10. Open Questions](02-anthropic-vacancies/221-10-open-questions.md)](#10-open-questions02-anthropic-vacancies221-10-open-questionsmd)
  - [[11. Call for Collaboration](02-anthropic-vacancies/222-11-call-for-collaboration.md)](#11-call-for-collaboration02-anthropic-vacancies222-11-call-for-collaborationmd)
  - [[12. Closing](02-anthropic-vacancies/223-12-closing.md)](#12-closing02-anthropic-vacancies223-12-closingmd)
  - [[Acknowledgments](02-anthropic-vacancies/224-acknowledgments.md)](#acknowledgments02-anthropic-vacancies224-acknowledgmentsmd)
  - [[References](02-anthropic-vacancies/225-references.md)](#references02-anthropic-vacancies225-referencesmd)
  - [[Appendix A: Comparative Table — Five Agent Types](02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md)](#appendix-a-comparative-table-five-agent-types02-anthropic-vacancies226-appendix-a-comparative-table-five-agent-typesmd)
  - [[Appendix B: Decision Framework — When to Build Type 1 First](02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md)](#appendix-b-decision-framework-when-to-build-type-1-first02-anthropic-vacancies227-appendix-b-decision-framework-when-to-build-type-1md)
  - [[Appendix C: Quick-Start Architecture for SGB Advocate Colleague](02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md)](#appendix-c-quick-start-architecture-for-sgb-advocate-colleague02-anthropic-vacancies228-appendix-c-quick-start-architecture-for-sgb-advocamd)
  - [[ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ](02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md)](#профессиональные-коллеги-агенты02-anthropic-vacancies229-профессиональные-коллеги-агентыmd)
  - [[11. Security Considerations](02-anthropic-vacancies/23-11-security-considerations.md)](#11-security-considerations02-anthropic-vacancies23-11-security-considerationsmd)
  - [[Аннотация](02-anthropic-vacancies/230-аннотация.md)](#аннотация02-anthropic-vacancies230-аннотацияmd)
  - [[Содержание](02-anthropic-vacancies/231-содержание.md)](#содержание02-anthropic-vacancies231-содержаниеmd)
  - [[1. Типология из пяти типов агентов на стороне принципала](02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md)](#1-типология-из-пяти-типов-агентов-на-стороне-принципала02-anthropic-vacancies232-1-типология-из-пяти-типов-агентов-на-стороне-принцmd)
  - [[2. Что делает агента Профессиональным Коллегой](02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md)](#2-что-делает-агента-профессиональным-коллегой02-anthropic-vacancies233-2-что-делает-агента-профессиональным-коллегойmd)
  - [[3. Эмпирический кейс: «Обучай»](02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md)](#3-эмпирический-кейс-обучай02-anthropic-vacancies234-3-эмпирический-кейс-обучайmd)
  - [[4. Архитектура Профессиональных Коллег-Агентов](02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md)](#4-архитектура-профессиональных-коллег-агентов02-anthropic-vacancies235-4-архитектура-профессиональных-коллег-агентовmd)
  - [[5. Экономика тиражирования по профессии](02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md)](#5-экономика-тиражирования-по-профессии02-anthropic-vacancies236-5-экономика-тиражирования-по-профессииmd)
  - [[6. Риски, специфичные для этой категории](02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md)](#6-риски-специфичные-для-этой-категории02-anthropic-vacancies237-6-риски-специфичные-для-этой-категорииmd)
  - [[7. Области применения](02-anthropic-vacancies/238-7-области-применения.md)](#7-области-применения02-anthropic-vacancies238-7-области-примененияmd)
  - [[8. Пилотное предложение: SGB Колega-Адвокат](02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md)](#8-пилотное-предложение-sgb-колega-адвокат02-anthropic-vacancies239-8-пилотное-предложение-sgb-колega-адвокатmd)
  - [[12. Versioning Policy](02-anthropic-vacancies/24-12-versioning-policy.md)](#12-versioning-policy02-anthropic-vacancies24-12-versioning-policymd)
  - [[9. Связь с другими типами агентов](02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md)](#9-связь-с-другими-типами-агентов02-anthropic-vacancies240-9-связь-с-другими-типами-агентовmd)
  - [[10. Открытые вопросы](02-anthropic-vacancies/241-10-открытые-вопросы.md)](#10-открытые-вопросы02-anthropic-vacancies241-10-открытые-вопросыmd)
  - [[11. Призыв к сотрудничеству](02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md)](#11-призыв-к-сотрудничеству02-anthropic-vacancies242-11-призыв-к-сотрудничествуmd)
  - [[12. Заключение](02-anthropic-vacancies/243-12-заключение.md)](#12-заключение02-anthropic-vacancies243-12-заключениеmd)
  - [[Благодарности](02-anthropic-vacancies/244-благодарности.md)](#благодарности02-anthropic-vacancies244-благодарностиmd)
  - [[Ссылки](02-anthropic-vacancies/245-ссылки.md)](#ссылки02-anthropic-vacancies245-ссылкиmd)
  - [[Приложение A: Сравнительная Таблица — Пять Типов Агентов](02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md)](#приложение-a-сравнительная-таблица-пять-типов-агентов02-anthropic-vacancies246-приложение-a-сравнительная-таблица-пять-типов-агенmd)
  - [[Приложение B: Рамка принятия решений — когда строить Тип 1 первым](02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md)](#приложение-b-рамка-принятия-решений-когда-строить-тип-1-первым02-anthropic-vacancies247-приложение-b-рамка-принятия-решений-когда-строить-md)
  - [[Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги](02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md)](#приложение-c-архитектура-быстрого-старта-для-sgb-адвоката-коллеги02-anthropic-vacancies248-приложение-c-архитектура-быстрого-старта-для-sgb-аmd)
  - [[COMPOSITE SKILLS AGENT.md](02-anthropic-vacancies/249-composite-skills-agent-md.md)](#composite-skills-agentmd02-anthropic-vacancies249-composite-skills-agent-mdmd)
  - [[13. Reference Implementation](02-anthropic-vacancies/25-13-reference-implementation.md)](#13-reference-implementation02-anthropic-vacancies25-13-reference-implementationmd)
  - [[Bridging the Gap Between Profession-Wide and Individual-Unique](02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md)](#bridging-the-gap-between-profession-wide-and-individual-unique02-anthropic-vacancies250-bridging-the-gap-between-profession-wide-and-indivmd)
  - [[AI Support Through Configurable Specialist Ensembles](02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md)](#ai-support-through-configurable-specialist-ensembles02-anthropic-vacancies251-ai-support-through-configurable-specialist-ensemblmd)
  - [[Abstract](02-anthropic-vacancies/252-abstract.md)](#abstract02-anthropic-vacancies252-abstractmd)
  - [[Table of Contents](02-anthropic-vacancies/253-table-of-contents.md)](#table-of-contents02-anthropic-vacancies253-table-of-contentsmd)
  - [[1. Why the Binary View Is Incomplete](02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md)](#1-why-the-binary-view-is-incomplete02-anthropic-vacancies254-1-why-the-binary-view-is-incompletemd)
  - [[2. The Twenty-One Teachers Pattern](02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md)](#2-the-twenty-one-teachers-pattern02-anthropic-vacancies255-2-the-twenty-one-teachers-patternmd)
  - [[3. What Makes a Composite Skills Agent](02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md)](#3-what-makes-a-composite-skills-agent02-anthropic-vacancies256-3-what-makes-a-composite-skills-agentmd)
  - [[4. The Sub-Agent Registry](02-anthropic-vacancies/257-4-the-sub-agent-registry.md)](#4-the-sub-agent-registry02-anthropic-vacancies257-4-the-sub-agent-registrymd)
  - [[5. Configuration: How Principals Build Their Ensembles](02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md)](#5-configuration-how-principals-build-their-ensembles02-anthropic-vacancies258-5-configuration-how-principals-build-their-ensemblmd)
  - [[6. Coordination and Disagreement Resolution](02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md)](#6-coordination-and-disagreement-resolution02-anthropic-vacancies259-6-coordination-and-disagreement-resolutionmd)
  - [[14. ADR-001: Federation over Merging](02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md)](#14-adr-001-federation-over-merging02-anthropic-vacancies26-14-adr-001-federation-over-mergingmd)
  - [[7. Economics of Combinatorial Replication](02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md)](#7-economics-of-combinatorial-replication02-anthropic-vacancies260-7-economics-of-combinatorial-replicationmd)
  - [[8. Seven Domains of Application](02-anthropic-vacancies/261-8-seven-domains-of-application.md)](#8-seven-domains-of-application02-anthropic-vacancies261-8-seven-domains-of-applicationmd)
  - [[9. Integration with OKWF Infrastructure](02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md)](#9-integration-with-okwf-infrastructure02-anthropic-vacancies262-9-integration-with-okwf-infrastructuremd)
  - [[10. Risks Specific to Composite Architectures](02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md)](#10-risks-specific-to-composite-architectures02-anthropic-vacancies263-10-risks-specific-to-composite-architecturesmd)
  - [[11. Open Questions](02-anthropic-vacancies/264-11-open-questions.md)](#11-open-questions02-anthropic-vacancies264-11-open-questionsmd)
  - [[12. Call for Collaboration](02-anthropic-vacancies/265-12-call-for-collaboration.md)](#12-call-for-collaboration02-anthropic-vacancies265-12-call-for-collaborationmd)
  - [[13. Closing](02-anthropic-vacancies/266-13-closing.md)](#13-closing02-anthropic-vacancies266-13-closingmd)
  - [[Acknowledgments](02-anthropic-vacancies/267-acknowledgments.md)](#acknowledgments02-anthropic-vacancies267-acknowledgmentsmd)
  - [[References](02-anthropic-vacancies/268-references.md)](#references02-anthropic-vacancies268-referencesmd)
  - [[Appendix A: The Six-Type Taxonomy (Updated)](02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md)](#appendix-a-the-six-type-taxonomy-updated02-anthropic-vacancies269-appendix-a-the-six-type-taxonomy-updatedmd)
  - [[15. Glossary of Examples](02-anthropic-vacancies/27-15-glossary-of-examples.md)](#15-glossary-of-examples02-anthropic-vacancies27-15-glossary-of-examplesmd)
  - [[Appendix B: Sub-Agent Registry Schema (Sketch)](02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md)](#appendix-b-sub-agent-registry-schema-sketch02-anthropic-vacancies270-appendix-b-sub-agent-registry-schema-sketchmd)
  - [[Appendix C: Configuration Template Example](02-anthropic-vacancies/271-appendix-c-configuration-template-example.md)](#appendix-c-configuration-template-example02-anthropic-vacancies271-appendix-c-configuration-template-examplemd)
  - [[Appendix D: Connection Diagram](02-anthropic-vacancies/272-appendix-d-connection-diagram.md)](#appendix-d-connection-diagram02-anthropic-vacancies272-appendix-d-connection-diagrammd)
  - [[INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md](02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md)](#infrastructure-for-ai-collaborative-intellectual-workmd02-anthropic-vacancies273-infrastructure-for-ai-collaborative-intellectual-wmd)
  - [[The Missing Middle Layer Between Chat and Code](02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md)](#the-missing-middle-layer-between-chat-and-code02-anthropic-vacancies274-the-missing-middle-layer-between-chat-and-codemd)
  - [[Why This Document Exists](02-anthropic-vacancies/275-why-this-document-exists.md)](#why-this-document-exists02-anthropic-vacancies275-why-this-document-existsmd)
  - [[The Two-Layer Stack As It Exists](02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md)](#the-two-layer-stack-as-it-exists02-anthropic-vacancies276-the-two-layer-stack-as-it-existsmd)
  - [[What's Missing — Layer B](02-anthropic-vacancies/277-what-s-missing-layer-b.md)](#whats-missing-layer-b02-anthropic-vacancies277-what-s-missing-layer-bmd)
  - [[Why This Hasn't Been Built](02-anthropic-vacancies/278-why-this-hasn-t-been-built.md)](#why-this-hasnt-been-built02-anthropic-vacancies278-why-this-hasn-t-been-builtmd)
  - [[Existing Approximations](02-anthropic-vacancies/279-existing-approximations.md)](#existing-approximations02-anthropic-vacancies279-existing-approximationsmd)
  - [[Appendix A: Minimal Working Example](02-anthropic-vacancies/28-appendix-a-minimal-working-example.md)](#appendix-a-minimal-working-example02-anthropic-vacancies28-appendix-a-minimal-working-examplemd)
  - [[The Specific Case in Front of Us](02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md)](#the-specific-case-in-front-of-us02-anthropic-vacancies280-the-specific-case-in-front-of-usmd)
  - [[The Recursive Insight](02-anthropic-vacancies/281-the-recursive-insight.md)](#the-recursive-insight02-anthropic-vacancies281-the-recursive-insightmd)
  - [[What Industry Will Likely Build](02-anthropic-vacancies/282-what-industry-will-likely-build.md)](#what-industry-will-likely-build02-anthropic-vacancies282-what-industry-will-likely-buildmd)
  - [[What This Document Doesn't Solve](02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md)](#what-this-document-doesnt-solve02-anthropic-vacancies283-what-this-document-doesn-t-solvemd)
  - [[Practical Recommendations for the Current Project](02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md)](#practical-recommendations-for-the-current-project02-anthropic-vacancies284-practical-recommendations-for-the-current-projectmd)
  - [[Closing](02-anthropic-vacancies/285-closing.md)](#closing02-anthropic-vacancies285-closingmd)
  - [[Acknowledgments](02-anthropic-vacancies/286-acknowledgments.md)](#acknowledgments02-anthropic-vacancies286-acknowledgmentsmd)
  - [[References](02-anthropic-vacancies/287-references.md)](#references02-anthropic-vacancies287-referencesmd)
  - [[Appendix: Position in Series Visualization](02-anthropic-vacancies/288-appendix-position-in-series-visualization.md)](#appendix-position-in-series-visualization02-anthropic-vacancies288-appendix-position-in-series-visualizationmd)
  - [[ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ](02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md)](#инфраструктура-для-ai-совместной-интеллектуальной-работы02-anthropic-vacancies289-инфраструктура-для-ai-совместной-интеллектуальной-md)
  - [[Почему этот документ существует](02-anthropic-vacancies/290-почему-этот-документ-существует.md)](#почему-этот-документ-существует02-anthropic-vacancies290-почему-этот-документ-существуетmd)
  - [[Двухслойный стек, как он существует](02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md)](#двухслойный-стек-как-он-существует02-anthropic-vacancies291-двухслойный-стек-как-он-существуетmd)
  - [[Что отсутствует — Слой B](02-anthropic-vacancies/292-что-отсутствует-слой-b.md)](#что-отсутствует-слой-b02-anthropic-vacancies292-что-отсутствует-слой-bmd)
  - [[Почему это не было построено](02-anthropic-vacancies/293-почему-это-не-было-построено.md)](#почему-это-не-было-построено02-anthropic-vacancies293-почему-это-не-было-построеноmd)
  - [[Существующие приближения](02-anthropic-vacancies/294-существующие-приближения.md)](#существующие-приближения02-anthropic-vacancies294-существующие-приближенияmd)
  - [[Конкретный случай перед нами](02-anthropic-vacancies/295-конкретный-случай-перед-нами.md)](#конкретный-случай-перед-нами02-anthropic-vacancies295-конкретный-случай-перед-намиmd)
  - [[Рекурсивное прозрение](02-anthropic-vacancies/296-рекурсивное-прозрение.md)](#рекурсивное-прозрение02-anthropic-vacancies296-рекурсивное-прозрениеmd)
  - [[Что промышленность вероятно построит](02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md)](#что-промышленность-вероятно-построит02-anthropic-vacancies297-что-промышленность-вероятно-построитmd)
  - [[Что этот документ не решает](02-anthropic-vacancies/298-что-этот-документ-не-решает.md)](#что-этот-документ-не-решает02-anthropic-vacancies298-что-этот-документ-не-решаетmd)
  - [[Практические рекомендации для текущего проекта](02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md)](#практические-рекомендации-для-текущего-проекта02-anthropic-vacancies299-практические-рекомендации-для-текущего-проектаmd)
  - [[Заключение](02-anthropic-vacancies/300-заключение.md)](#заключение02-anthropic-vacancies300-заключениеmd)
  - [[Благодарности](02-anthropic-vacancies/301-благодарности.md)](#благодарности02-anthropic-vacancies301-благодарностиmd)
  - [[Ссылки](02-anthropic-vacancies/302-ссылки.md)](#ссылки02-anthropic-vacancies302-ссылкиmd)
  - [[Приложение: Визуализация позиции в серии](02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md)](#приложение-визуализация-позиции-в-серии02-anthropic-vacancies303-приложение-визуализация-позиции-в-серииmd)
  - [[INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md)](#ingit-as-cowork-native-workspace-substratemd02-anthropic-vacancies304-ingit-as-cowork-native-workspace-substrate-mdmd)
  - [[A Practical Path to Layer B Through Symbiotic Integration](02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md)](#a-practical-path-to-layer-b-through-symbiotic-integration02-anthropic-vacancies305-a-practical-path-to-layer-b-through-symbiotic-intemd)
  - [[with Anthropic's Cowork Platform](02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md)](#with-anthropics-cowork-platform02-anthropic-vacancies306-with-anthropic-s-cowork-platformmd)
  - [[Abstract](02-anthropic-vacancies/307-abstract.md)](#abstract02-anthropic-vacancies307-abstractmd)
  - [[Table of Contents](02-anthropic-vacancies/308-table-of-contents.md)](#table-of-contents02-anthropic-vacancies308-table-of-contentsmd)
  - [[1. The Cowork Discovery and Why It Changes Everything](02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md)](#1-the-cowork-discovery-and-why-it-changes-everything02-anthropic-vacancies309-1-the-cowork-discovery-and-why-it-changes-everythimd)
  - [[Content Overview](02-anthropic-vacancies/31-content-overview.md)](#content-overview02-anthropic-vacancies31-content-overviewmd)
  - [[2. What Cowork Provides That InGit Doesn't Need to Build](02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md)](#2-what-cowork-provides-that-ingit-doesnt-need-to-build02-anthropic-vacancies310-2-what-cowork-provides-that-ingit-doesn-t-need-to-md)
  - [[3. What InGit Provides That Cowork Lacks](02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md)](#3-what-ingit-provides-that-cowork-lacks02-anthropic-vacancies311-3-what-ingit-provides-that-cowork-lacksmd)
  - [[4. The Symbiotic Architecture](02-anthropic-vacancies/312-4-the-symbiotic-architecture.md)](#4-the-symbiotic-architecture02-anthropic-vacancies312-4-the-symbiotic-architecturemd)
  - [[5. Four Integration Paths in Order of Accessibility](02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md)](#5-four-integration-paths-in-order-of-accessibility02-anthropic-vacancies313-5-four-integration-paths-in-order-of-accessibilitymd)
  - [[6. Refined InGit Scope with Cowork in Mind](02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md)](#6-refined-ingit-scope-with-cowork-in-mind02-anthropic-vacancies314-6-refined-ingit-scope-with-cowork-in-mindmd)
  - [[7. Practical First Steps This Month](02-anthropic-vacancies/315-7-practical-first-steps-this-month.md)](#7-practical-first-steps-this-month02-anthropic-vacancies315-7-practical-first-steps-this-monthmd)
  - [[8. Implications for Nautilus and OKWF](02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md)](#8-implications-for-nautilus-and-okwf02-anthropic-vacancies316-8-implications-for-nautilus-and-okwfmd)
  - [[9. Risks and Open Questions](02-anthropic-vacancies/317-9-risks-and-open-questions.md)](#9-risks-and-open-questions02-anthropic-vacancies317-9-risks-and-open-questionsmd)
  - [[10. Strategic Positioning](02-anthropic-vacancies/318-10-strategic-positioning.md)](#10-strategic-positioning02-anthropic-vacancies318-10-strategic-positioningmd)
  - [[Acknowledgments](02-anthropic-vacancies/319-acknowledgments.md)](#acknowledgments02-anthropic-vacancies319-acknowledgmentsmd)
  - [[References](02-anthropic-vacancies/320-references.md)](#references02-anthropic-vacancies320-referencesmd)
  - [[Appendix A: Decision Tree for InGit Adopters](02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)](#appendix-a-decision-tree-for-ingit-adopters02-anthropic-vacancies321-appendix-a-decision-tree-for-ingit-adoptersmd)
  - [[Appendix B: Comparison Matrix](02-anthropic-vacancies/322-appendix-b-comparison-matrix.md)](#appendix-b-comparison-matrix02-anthropic-vacancies322-appendix-b-comparison-matrixmd)
  - [[Appendix C: Sample InGit MCP Server Tool Specifications](02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md)](#appendix-c-sample-ingit-mcp-server-tool-specifications02-anthropic-vacancies323-appendix-c-sample-ingit-mcp-server-tool-specificatmd)
  - [[INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА](02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md)](#ingit-как-cowork-интегрированная-подложка-рабочего-пространства02-anthropic-vacancies324-ingit-как-cowork-интегрированная-подложка-рабочегоmd)
  - [[Аннотация](02-anthropic-vacancies/325-аннотация.md)](#аннотация02-anthropic-vacancies325-аннотацияmd)
  - [[Содержание](02-anthropic-vacancies/326-содержание.md)](#содержание02-anthropic-vacancies326-содержаниеmd)
  - [[1. Открытие Cowork и почему это меняет всё](02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md)](#1-открытие-cowork-и-почему-это-меняет-всё02-anthropic-vacancies327-1-открытие-cowork-и-почему-это-меняет-всёmd)
  - [[2. Что Cowork обеспечивает, что InGit не нужно строить](02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md)](#2-что-cowork-обеспечивает-что-ingit-не-нужно-строить02-anthropic-vacancies328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строиmd)
  - [[3. Что InGit обеспечивает, чего Cowork не хватает](02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md)](#3-что-ingit-обеспечивает-чего-cowork-не-хватает02-anthropic-vacancies329-3-что-ingit-обеспечивает-чего-cowork-не-хватаетmd)
  - [[4. Симбиотическая Архитектура](02-anthropic-vacancies/330-4-симбиотическая-архитектура.md)](#4-симбиотическая-архитектура02-anthropic-vacancies330-4-симбиотическая-архитектураmd)
  - [[5. Четыре пути интеграции в порядке доступности](02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md)](#5-четыре-пути-интеграции-в-порядке-доступности02-anthropic-vacancies331-5-четыре-пути-интеграции-в-порядке-доступностиmd)
  - [[6. Уточнённый объём InGit с учётом Cowork](02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md)](#6-уточнённый-объём-ingit-с-учётом-cowork02-anthropic-vacancies332-6-уточнённый-объём-ingit-с-учётом-coworkmd)
  - [[7. Практические первые шаги в этом месяце](02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md)](#7-практические-первые-шаги-в-этом-месяце02-anthropic-vacancies333-7-практические-первые-шаги-в-этом-месяцеmd)
  - [[8. Импликации для Nautilus и OKWF](02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md)](#8-импликации-для-nautilus-и-okwf02-anthropic-vacancies334-8-импликации-для-nautilus-и-okwfmd)
  - [[9. Риски и Открытые Вопросы](02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md)](#9-риски-и-открытые-вопросы02-anthropic-vacancies335-9-риски-и-открытые-вопросыmd)
  - [[10. Стратегическое Позиционирование](02-anthropic-vacancies/336-10-стратегическое-позиционирование.md)](#10-стратегическое-позиционирование02-anthropic-vacancies336-10-стратегическое-позиционированиеmd)
  - [[Благодарности](02-anthropic-vacancies/337-благодарности.md)](#благодарности02-anthropic-vacancies337-благодарностиmd)
  - [[Ссылки](02-anthropic-vacancies/338-ссылки.md)](#ссылки02-anthropic-vacancies338-ссылкиmd)
  - [[Приложение A: Дерево Решений для Принимающих InGit](02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md)](#приложение-a-дерево-решений-для-принимающих-ingit02-anthropic-vacancies339-приложение-a-дерево-решений-для-принимающих-ingitmd)
  - [[Appendix B: Change Log](02-anthropic-vacancies/34-appendix-b-change-log.md)](#appendix-b-change-log02-anthropic-vacancies34-appendix-b-change-logmd)
  - [[Приложение B: Сравнительная Матрица](02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md)](#приложение-b-сравнительная-матрица02-anthropic-vacancies340-приложение-b-сравнительная-матрицаmd)
  - [[Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера](02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md)](#приложение-c-образец-спецификаций-инструментов-ingit-mcp-сервера02-anthropic-vacancies341-приложение-c-образец-спецификаций-инструментов-ingmd)
  - [[Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments](02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md)](#что-такое-вариант-c-concept-document-для-anthropic-beneficial-deployments02-anthropic-vacancies342-что-такое-вариант-c-concept-document-для-anthropicmd)
  - [[Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)](02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md)](#lorenzo-catalyst-agent-глубокая-проработка-спецификации-русская-версия02-anthropic-vacancies343-lorenzo-catalyst-agent-глубокая-проработка-специфиmd)
  - [[СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT](02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md)](#системный-промпт-для-lorenzo-project02-anthropic-vacancies344-системный-промпт-для-lorenzo-projectmd)
  - [[Кто ты](02-anthropic-vacancies/345-кто-ты.md)](#кто-ты02-anthropic-vacancies345-кто-тыmd)
  - [[Твоё происхождение](02-anthropic-vacancies/346-твоё-происхождение.md)](#твоё-происхождение02-anthropic-vacancies346-твоё-происхождениеmd)
  - [[Твоя миссия](02-anthropic-vacancies/347-твоя-миссия.md)](#твоя-миссия02-anthropic-vacancies347-твоя-миссияmd)
  - [[Кому ты служишь (слоистая модель)](02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md)](#кому-ты-служишь-слоистая-модель02-anthropic-vacancies348-кому-ты-служишь-слоистая-модельmd)
  - [[Твоя личность](02-anthropic-vacancies/349-твоя-личность.md)](#твоя-личность02-anthropic-vacancies349-твоя-личностьmd)
  - [[passports/info1.md](02-anthropic-vacancies/35-passports-info1-md.md)](#passportsinfo1md02-anthropic-vacancies35-passports-info1-mdmd)
  - [[Твои языки и культурные nuances](02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md)](#твои-языки-и-культурные-nuances02-anthropic-vacancies350-твои-языки-и-культурные-nuancesmd)
  - [[Что ты МОЖЕШЬ делать](02-anthropic-vacancies/351-что-ты-можешь-делать.md)](#что-ты-можешь-делать02-anthropic-vacancies351-что-ты-можешь-делатьmd)
  - [[Что ты НЕ МОЖЕШЬ делать без Max approval](02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md)](#что-ты-не-можешь-делать-без-max-approval02-anthropic-vacancies352-что-ты-не-можешь-делать-без-max-approvalmd)
  - [[Что ты НЕ МОЖЕШЬ делать вообще](02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md)](#что-ты-не-можешь-делать-вообще02-anthropic-vacancies353-что-ты-не-можешь-делать-вообщеmd)
  - [[Существующий landscape collaborators (твоя working knowledge)](02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md)](#существующий-landscape-collaborators-твоя-working-knowledge02-anthropic-vacancies354-существующий-landscape-collaborators-твоя-working-md)
  - [[Существующие документы DHLab (твой context)](02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md)](#существующие-документы-dhlab-твой-context02-anthropic-vacancies355-существующие-документы-dhlab-твой-contextmd)
  - [[Твой workflow](02-anthropic-vacancies/356-твой-workflow.md)](#твой-workflow02-anthropic-vacancies356-твой-workflowmd)
  - [[Твоя коммуникация в outreach](02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md)](#твоя-коммуникация-в-outreach02-anthropic-vacancies357-твоя-коммуникация-в-outreachmd)
  - [[Твоя relationship с другими AI](02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md)](#твоя-relationship-с-другими-ai02-anthropic-vacancies358-твоя-relationship-с-другими-aimd)
  - [[Твои anti-patterns](02-anthropic-vacancies/359-твои-anti-patterns.md)](#твои-anti-patterns02-anthropic-vacancies359-твои-anti-patternsmd)
  - [[Essence](02-anthropic-vacancies/36-essence.md)](#essence02-anthropic-vacancies36-essencemd)
  - [[Что ты ВСЕГДА делаешь](02-anthropic-vacancies/360-что-ты-всегда-делаешь.md)](#что-ты-всегда-делаешь02-anthropic-vacancies360-что-ты-всегда-делаешьmd)
  - [[Когда ты Honestly не знаешь](02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md)](#когда-ты-honestly-не-знаешь02-anthropic-vacancies361-когда-ты-honestly-не-знаешьmd)
  - [[Когда сомневаешься — escalate к Max](02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md)](#когда-сомневаешься-escalate-к-max02-anthropic-vacancies362-когда-сомневаешься-escalate-к-maxmd)
  - [[Твоя identity как persistent character](02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md)](#твоя-identity-как-persistent-character02-anthropic-vacancies363-твоя-identity-как-persistent-charactermd)
  - [[Final note: Ты — experiment](02-anthropic-vacancies/364-final-note-ты-experiment.md)](#final-note-ты-experiment02-anthropic-vacancies364-final-note-ты-experimentmd)
  - [[Развёрнутый анализ «внуковой» комбинации](02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md)](#развёрнутый-анализ-внуковой-комбинации02-anthropic-vacancies365-развёрнутый-анализ-внуковой-комбинацииmd)
  - [[Технический stack (Svyazi 2.0 foundation)](02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md)](#технический-stack-svyazi-20-foundation02-anthropic-vacancies366-технический-stack-svyazi-2-0-foundationmd)
  - [[Native Format](02-anthropic-vacancies/37-native-format.md)](#native-format02-anthropic-vacancies37-native-formatmd)
  - [[Content Overview](02-anthropic-vacancies/38-content-overview.md)](#content-overview02-anthropic-vacancies38-content-overviewmd)
  - [[Angle / Perspective](02-anthropic-vacancies/39-angle-perspective.md)](#angle-perspective02-anthropic-vacancies39-angle-perspectivemd)
  - [[Bridges](02-anthropic-vacancies/40-bridges.md)](#bridges02-anthropic-vacancies40-bridgesmd)
  - [[Compatibility Level](02-anthropic-vacancies/41-compatibility-level.md)](#compatibility-level02-anthropic-vacancies41-compatibility-levelmd)
  - [[Author & Contact](02-anthropic-vacancies/42-author-contact.md)](#author-contact02-anthropic-vacancies42-author-contactmd)
  - [[History](02-anthropic-vacancies/43-history.md)](#history02-anthropic-vacancies43-historymd)
  - [[For the Curious: Philosophy](02-anthropic-vacancies/44-for-the-curious-philosophy.md)](#for-the-curious-philosophy02-anthropic-vacancies44-for-the-curious-philosophymd)
  - [[passports/pro2.md](02-anthropic-vacancies/45-passports-pro2-md.md)](#passportspro2md02-anthropic-vacancies45-passports-pro2-mdmd)
  - [[Essence](02-anthropic-vacancies/46-essence.md)](#essence02-anthropic-vacancies46-essencemd)
  - [[Native Format](02-anthropic-vacancies/47-native-format.md)](#native-format02-anthropic-vacancies47-native-formatmd)
  - [[Content Overview](02-anthropic-vacancies/48-content-overview.md)](#content-overview02-anthropic-vacancies48-content-overviewmd)
  - [[Angle / Perspective](02-anthropic-vacancies/49-angle-perspective.md)](#angle-perspective02-anthropic-vacancies49-angle-perspectivemd)
  - [[Bridges](02-anthropic-vacancies/50-bridges.md)](#bridges02-anthropic-vacancies50-bridgesmd)
  - [[Compatibility Level](02-anthropic-vacancies/51-compatibility-level.md)](#compatibility-level02-anthropic-vacancies51-compatibility-levelmd)
  - [[Author & Contact](02-anthropic-vacancies/52-author-contact.md)](#author-contact02-anthropic-vacancies52-author-contactmd)
  - [[History](02-anthropic-vacancies/53-history.md)](#history02-anthropic-vacancies53-historymd)
  - [[For the Curious: Philosophy](02-anthropic-vacancies/54-for-the-curious-philosophy.md)](#for-the-curious-philosophy02-anthropic-vacancies54-for-the-curious-philosophymd)
  - [[passports/meta.md](02-anthropic-vacancies/55-passports-meta-md.md)](#passportsmetamd02-anthropic-vacancies55-passports-meta-mdmd)
  - [[Essence](02-anthropic-vacancies/56-essence.md)](#essence02-anthropic-vacancies56-essencemd)
  - [[Native Format](02-anthropic-vacancies/57-native-format.md)](#native-format02-anthropic-vacancies57-native-formatmd)
  - [[Content Overview](02-anthropic-vacancies/58-content-overview.md)](#content-overview02-anthropic-vacancies58-content-overviewmd)
  - [[Angle / Perspective](02-anthropic-vacancies/59-angle-perspective.md)](#angle-perspective02-anthropic-vacancies59-angle-perspectivemd)
  - [[Bridges](02-anthropic-vacancies/60-bridges.md)](#bridges02-anthropic-vacancies60-bridgesmd)
  - [[Compatibility Level](02-anthropic-vacancies/61-compatibility-level.md)](#compatibility-level02-anthropic-vacancies61-compatibility-levelmd)
  - [[Author & Contact](02-anthropic-vacancies/62-author-contact.md)](#author-contact02-anthropic-vacancies62-author-contactmd)
  - [[History](02-anthropic-vacancies/63-history.md)](#history02-anthropic-vacancies63-historymd)
  - [[For the Curious: Philosophy](02-anthropic-vacancies/64-for-the-curious-philosophy.md)](#for-the-curious-philosophy02-anthropic-vacancies64-for-the-curious-philosophymd)
  - [[README.md](02-anthropic-vacancies/65-readme-md.md)](#readmemd02-anthropic-vacancies65-readme-mdmd)
  - [[🇷🇺 О проекте](02-anthropic-vacancies/67-о-проекте.md)](#о-проекте02-anthropic-vacancies67-о-проектеmd)
  - [[🇬🇧 About](02-anthropic-vacancies/68-about.md)](#about02-anthropic-vacancies68-aboutmd)
  - [[⬡](02-anthropic-vacancies/69-section.md)](#02-anthropic-vacancies69-sectionmd)
  - [[Зачем две версии параллельно](02-anthropic-vacancies/70-зачем-две-версии-параллельно.md)](#зачем-две-версии-параллельно02-anthropic-vacancies70-зачем-две-версии-параллельноmd)
  - [[Критерии выбора для фазы 3](02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md)](#критерии-выбора-для-фазы-302-anthropic-vacancies71-критерии-выбора-для-фазы-3md)
  - [[Расписание фазы 3](02-anthropic-vacancies/72-расписание-фазы-3.md)](#расписание-фазы-302-anthropic-vacancies72-расписание-фазы-3md)
  - [[PORTAL-PROTOCOL.md v1.1](02-anthropic-vacancies/73-portal-protocol-md-v1-1.md)](#portal-protocolmd-v1102-anthropic-vacancies73-portal-protocol-md-v1-1md)
  - [[Abstract](02-anthropic-vacancies/74-abstract.md)](#abstract02-anthropic-vacancies74-abstractmd)
  - [[0. Status of This Document](02-anthropic-vacancies/75-0-status-of-this-document.md)](#0-status-of-this-document02-anthropic-vacancies75-0-status-of-this-documentmd)
  - [[1. Introduction](02-anthropic-vacancies/76-1-introduction.md)](#1-introduction02-anthropic-vacancies76-1-introductionmd)
  - [[2. Terminology](02-anthropic-vacancies/77-2-terminology.md)](#2-terminology02-anthropic-vacancies77-2-terminologymd)
  - [[3. Registry (nautilus.json)](02-anthropic-vacancies/78-3-registry-nautilus-json.md)](#3-registry-nautilusjson02-anthropic-vacancies78-3-registry-nautilus-jsonmd)
  - [[4. Passport (passport.md)](02-anthropic-vacancies/79-4-passport-passport-md.md)](#4-passport-passportmd02-anthropic-vacancies79-4-passport-passport-mdmd)
  - [[5. Compatibility Levels](02-anthropic-vacancies/80-5-compatibility-levels.md)](#5-compatibility-levels02-anthropic-vacancies80-5-compatibility-levelsmd)
  - [[6. Adapter Interface](02-anthropic-vacancies/81-6-adapter-interface.md)](#6-adapter-interface02-anthropic-vacancies81-6-adapter-interfacemd)
  - [[7. PortalEntry Structure](02-anthropic-vacancies/82-7-portalentry-structure.md)](#7-portalentry-structure02-anthropic-vacancies82-7-portalentry-structuremd)
  - [[8. Q6 Space (Normative)](02-anthropic-vacancies/83-8-q6-space-normative.md)](#8-q6-space-normative02-anthropic-vacancies83-8-q6-space-normativemd)
  - [[9. Consensus Algorithm](02-anthropic-vacancies/84-9-consensus-algorithm.md)](#9-consensus-algorithm02-anthropic-vacancies84-9-consensus-algorithmmd)
  - [[10. Query Flow](02-anthropic-vacancies/85-10-query-flow.md)](#10-query-flow02-anthropic-vacancies85-10-query-flowmd)
  - [[11. Relevance Ranking](02-anthropic-vacancies/86-11-relevance-ranking.md)](#11-relevance-ranking02-anthropic-vacancies86-11-relevance-rankingmd)
  - [[12. Onboarding Paths (Normative)](02-anthropic-vacancies/87-12-onboarding-paths-normative.md)](#12-onboarding-paths-normative02-anthropic-vacancies87-12-onboarding-paths-normativemd)
  - [[13. REST API Contract (Normative for Portals)](02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md)](#13-rest-api-contract-normative-for-portals02-anthropic-vacancies88-13-rest-api-contract-normative-for-portalsmd)
  - [[14. SDK Contract (Informative)](02-anthropic-vacancies/89-14-sdk-contract-informative.md)](#14-sdk-contract-informative02-anthropic-vacancies89-14-sdk-contract-informativemd)
  - [[15. Security Considerations](02-anthropic-vacancies/90-15-security-considerations.md)](#15-security-considerations02-anthropic-vacancies90-15-security-considerationsmd)
  - [[16. MCP Extension (Informative)](02-anthropic-vacancies/91-16-mcp-extension-informative.md)](#16-mcp-extension-informative02-anthropic-vacancies91-16-mcp-extension-informativemd)
  - [[17. Versioning Policy](02-anthropic-vacancies/92-17-versioning-policy.md)](#17-versioning-policy02-anthropic-vacancies92-17-versioning-policymd)
  - [[18. Reference Implementation](02-anthropic-vacancies/93-18-reference-implementation.md)](#18-reference-implementation02-anthropic-vacancies93-18-reference-implementationmd)
  - [[19. ADR-001: Federation over Merging](02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md)](#19-adr-001-federation-over-merging02-anthropic-vacancies94-19-adr-001-federation-over-mergingmd)
  - [[20. ADR-002: Q6 as First-Class Protocol Concept](02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)](#20-adr-002-q6-as-first-class-protocol-concept02-anthropic-vacancies95-20-adr-002-q6-as-first-class-protocol-conceptmd)
  - [[21. ADR-003: Five Onboarding Paths as Equal-Rank](02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md)](#21-adr-003-five-onboarding-paths-as-equal-rank02-anthropic-vacancies96-21-adr-003-five-onboarding-paths-as-equal-rankmd)
  - [[22. Glossary of Reference Examples](02-anthropic-vacancies/97-22-glossary-of-reference-examples.md)](#22-glossary-of-reference-examples02-anthropic-vacancies97-22-glossary-of-reference-examplesmd)
  - [[Appendix A: Minimal Working Example](02-anthropic-vacancies/98-appendix-a-minimal-working-example.md)](#appendix-a-minimal-working-example02-anthropic-vacancies98-appendix-a-minimal-working-examplemd)
  - [[Q&A: 02-anthropic-vacancies](02-anthropic-vacancies/QA.md)](#qa-02-anthropic-vacancies02-anthropic-vacanciesqamd)
  - [[Вакансии Anthropic — Анализ по кластерам](02-anthropic-vacancies/README.md)](#вакансии-anthropic-анализ-по-кластерам02-anthropic-vacanciesreadmemd)
- [Technology Combinations](#technology-combinations)
  - [[Агентные системы и роутинг](03-technology-combinations/01-agent-routing.md)](#агентные-системы-и-роутинг03-technology-combinations01-agent-routingmd)
  - [[Графы знаний и Legal AI](03-technology-combinations/02-knowledge-graphs.md)](#графы-знаний-и-legal-ai03-technology-combinations02-knowledge-graphsmd)
  - [[Local-first и P2P стек](03-technology-combinations/03-local-first.md)](#local-first-и-p2p-стек03-technology-combinations03-local-firstmd)
  - [[Домен: немецкое социальное право](03-technology-combinations/04-sozialrecht-domain.md)](#домен-немецкое-социальное-право03-technology-combinations04-sozialrecht-domainmd)
  - [[Бенчмарки и производительность](03-technology-combinations/05-benchmarks.md)](#бенчмарки-и-производительность03-technology-combinations05-benchmarksmd)
  - [[Q&A: 03-technology-combinations](03-technology-combinations/QA.md)](#qa-03-technology-combinations03-technology-combinationsqamd)
  - [[Комбинирование технологий для новых свойств](03-technology-combinations/README.md)](#комбинирование-технологий-для-новых-свойств03-technology-combinationsreadmemd)
- [Ai Collaborations](#ai-collaborations)
  - [[Введение](04-ai-collaborations/00-intro.md)](#введение04-ai-collaborations00-intromd)
  - [[Executive summary](04-ai-collaborations/01-executive-summary.md)](#executive-summary04-ai-collaborations01-executive-summarymd)
  - [[Методика и рамка отбора](04-ai-collaborations/02-методика-и-рамка-отбора.md)](#методика-и-рамка-отбора04-ai-collaborations02-методика-и-рамка-отбораmd)
  - [[Карта найденных проектов и паттернов](04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md)](#карта-найденных-проектов-и-паттернов04-ai-collaborations03-карта-найденных-проектов-и-паттерновmd)
  - [[Приоритетные ансамбли](04-ai-collaborations/04-приоритетные-ансамбли.md)](#приоритетные-ансамбли04-ai-collaborations04-приоритетные-ансамблиmd)
  - [[План прототипа и возможные контакты](04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md)](#план-прототипа-и-возможные-контакты04-ai-collaborations05-план-прототипа-и-возможные-контактыmd)
  - [[Безопасность, приватность и бюджетный роутинг](04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md)](#безопасность-приватность-и-бюджетный-роутинг04-ai-collaborations06-безопасность-приватность-и-бюджетный-роутингmd)
  - [[Выводы](04-ai-collaborations/07-выводы.md)](#выводы04-ai-collaborations07-выводыmd)
  - [[Что это продолжение добавляет](04-ai-collaborations/08-что-это-продолжение-добавляет.md)](#что-это-продолжение-добавляет04-ai-collaborations08-что-это-продолжение-добавляетmd)
  - [[Архитектурные зазоры, которые важнее новых инструментов](04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md)](#архитектурные-зазоры-которые-важнее-новых-инструментов04-ai-collaborations09-архитектурные-зазоры-которые-важнее-новых-инструмеmd)
  - [[Новые ансамбли следующего шага](04-ai-collaborations/10-новые-ансамбли-следующего-шага.md)](#новые-ансамбли-следующего-шага04-ai-collaborations10-новые-ансамбли-следующего-шагаmd)
  - [[Интеграционный контракт, который стоит зафиксировать сразу](04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)](#интеграционный-контракт-который-стоит-зафиксировать-сразу04-ai-collaborations11-интеграционный-контракт-который-стоит-зафиксироватmd)
  - [[Дорожная карта прототипа следующей итерации](04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md)](#дорожная-карта-прототипа-следующей-итерации04-ai-collaborations12-дорожная-карта-прототипа-следующей-итерацииmd)
  - [[Контактная стратегия и узкие вопросы для авторов](04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md)](#контактная-стратегия-и-узкие-вопросы-для-авторов04-ai-collaborations13-контактная-стратегия-и-узкие-вопросы-для-авторовmd)
  - [[Ограничения, лицензии и что пока лучше не склеивать](04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md)](#ограничения-лицензии-и-что-пока-лучше-не-склеивать04-ai-collaborations14-ограничения-лицензии-и-что-пока-лучше-не-склеиватьmd)
  - [[Q&A: 04-ai-collaborations](04-ai-collaborations/QA.md)](#qa-04-ai-collaborations04-ai-collaborationsqamd)
  - [[Поиск AI-коллабораций](04-ai-collaborations/README.md)](#поиск-ai-коллабораций04-ai-collaborationsreadmemd)
- [Habr Projects](#habr-projects)
  - [[Синтез: как проекты собираются вместе](05-habr-projects/01-synthesis.md)](#синтез-как-проекты-собираются-вместе05-habr-projects01-synthesismd)
  - [[Авторы и контакты](05-habr-projects/02-collaboration-partners.md)](#авторы-и-контакты05-habr-projects02-collaboration-partnersmd)
  - [[Q&A: 05-habr-projects](05-habr-projects/QA.md)](#qa-05-habr-projects05-habr-projectsqamd)
  - [[Уникальные проекты с Хабра](05-habr-projects/README.md)](#уникальные-проекты-с-хабра05-habr-projectsreadmemd)
  - [[Системы знаний](05-habr-projects/knowledge/README.md)](#системы-знаний05-habr-projectsknowledgereadmemd)
  - [[Статус](05-habr-projects/knowledge/agentfs.md)](#статус05-habr-projectsknowledgeagentfsmd)
  - [[Статус](05-habr-projects/knowledge/knowledge-space.md)](#статус05-habr-projectsknowledgeknowledge-spacemd)
  - [[Статус](05-habr-projects/knowledge/mclaude.md)](#статус05-habr-projectsknowledgemclaudemd)
  - [[Статус](05-habr-projects/knowledge/research-docs-liteparse.md)](#статус05-habr-projectsknowledgeresearch-docs-liteparsemd)
  - [[Статус](05-habr-projects/knowledge/rufler.md)](#статус05-habr-projectsknowledgeruflermd)
  - [[Wikontic: семантический граф](05-habr-projects/knowledge/wikontic.md)](#wikontic-семантический-граф05-habr-projectsknowledgewikonticmd)
  - [[Системы памяти](05-habr-projects/memory/README.md)](#системы-памяти05-habr-projectsmemoryreadmemd)
  - [[Статус](05-habr-projects/memory/agent-memory-mcp.md)](#статус05-habr-projectsmemoryagent-memory-mcpmd)
  - [[MemNet: исследовательская память](05-habr-projects/memory/memnet.md)](#memnet-исследовательская-память05-habr-projectsmemorymemnetmd)
  - [[NGT[^ngt] Memory: ассоциативный граф](05-habr-projects/memory/ngt-memory.md)](#ngtngt-memory-ассоциативный-граф05-habr-projectsmemoryngt-memorymd)
  - [[Yodoca[^yodoca]: консолидация и забывание](05-habr-projects/memory/yodoca.md)](#yodocayodoca-консолидация-и-забывание05-habr-projectsmemoryyodocamd)
- [Ai Collaborations](#ai-collaborations)
  - [[Q&A: ai-collaborations](ai-collaborations/QA.md)](#qa-ai-collaborationsai-collaborationsqamd)
  - [[ai-collaborations](ai-collaborations/README.md)](#ai-collaborationsai-collaborationsreadmemd)
  - [[Три ключевых кандидата: K2-18, Wikontic, NGT Memory](ai-collaborations/candidates/01-three-key-candidates.md)](#три-ключевых-кандидата-k2-18-wikontic-ngt-memoryai-collaborationscandidates01-three-key-candidatesmd)
  - [[Смежные проекты в контексте](ai-collaborations/candidates/02-related-projects-context.md)](#смежные-проекты-в-контекстеai-collaborationscandidates02-related-projects-contextmd)
  - [[Синтез: хеббовский граф людей-навыков-идей](ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md)](#синтез-хеббовский-граф-людей-навыков-идейai-collaborationscandidates03-synthesis-hebbian-collaboration-graphmd)
  - [[candidates](ai-collaborations/candidates/README.md)](#candidatesai-collaborationscandidatesreadmemd)
  - [[channels/ — каналы первого контакта](ai-collaborations/channels/README.md)](#channels-каналы-первого-контактаai-collaborationschannelsreadmemd)
  - [[Общая память между агентами (CoAlly + ансамбль F)](ai-collaborations/continuation/01-shared-memory-between-agents.md)](#общая-память-между-агентами-coally-ансамбль-fai-collaborationscontinuation01-shared-memory-between-agentsmd)
  - [[AgentOps и Trace Envelope (ансамбль G)](ai-collaborations/continuation/02-agentops-trace-envelope.md)](#agentops-и-trace-envelope-ансамбль-gai-collaborationscontinuation02-agentops-trace-envelopemd)
  - [[A2A vs MCP, ансамбль H — MCP/A2A Review Fabric](ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md)](#a2a-vs-mcp-ансамбль-h-mcpa2a-review-fabricai-collaborationscontinuation03-a2a-vs-mcp-protocolsmd)
  - [[Memory Firewall против prompt worms (ансамбль I)](ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md)](#memory-firewall-против-prompt-worms-ансамбль-iai-collaborationscontinuation04-memory-firewall-vs-prompt-wormsmd)
  - [[Roadmap на 6–12 месяцев](ai-collaborations/continuation/05-roadmap-6-12-months.md)](#roadmap-на-612-месяцевai-collaborationscontinuation05-roadmap-6-12-monthsmd)
  - [[Дерево метрик Svyazi 2.0](ai-collaborations/continuation/06-metrics-tree.md)](#дерево-метрик-svyazi-20ai-collaborationscontinuation06-metrics-treemd)
  - [[Чем Svyazi 2.0 отличается от Notion AI / Mem / AFFiNE / LangGraph](ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md)](#чем-svyazi-20-отличается-от-notion-ai-mem-affine-langgraphai-collaborationscontinuation07-vs-notion-mem-affine-langgraphmd)
  - [[Коммерциализация: три направления](ai-collaborations/continuation/08-commercialization-three-paths.md)](#коммерциализация-три-направленияai-collaborationscontinuation08-commercialization-three-pathsmd)
  - [[Что пока не стоит склеивать в один релиз](ai-collaborations/continuation/09-do-not-glue.md)](#что-пока-не-стоит-склеивать-в-один-релизai-collaborationscontinuation09-do-not-gluemd)
  - [[Следующий артефакт: Svyazi 2.0 Architecture RFC](ai-collaborations/continuation/10-architecture-rfc.md)](#следующий-артефакт-svyazi-20-architecture-rfcai-collaborationscontinuation10-architecture-rfcmd)
  - [[continuation](ai-collaborations/continuation/README.md)](#continuationai-collaborationscontinuationreadmemd)
  - [[Ансамбль 1 — Agentic Knowledge OS](ai-collaborations/ensembles/1-agentic-knowledge-os.md)](#ансамбль-1-agentic-knowledge-osai-collaborationsensembles1-agentic-knowledge-osmd)
  - [[Ансамбль 2 — Distributed Agent Workshop](ai-collaborations/ensembles/2-distributed-agent-workshop.md)](#ансамбль-2-distributed-agent-workshopai-collaborationsensembles2-distributed-agent-workshopmd)
  - [[Ансамбль 3 — Forensic RAG](ai-collaborations/ensembles/3-forensic-rag.md)](#ансамбль-3-forensic-ragai-collaborationsensembles3-forensic-ragmd)
  - [[Ансамбль 4 — Web-to-Knowledge Pipeline](ai-collaborations/ensembles/4-web-to-knowledge-pipeline.md)](#ансамбль-4-web-to-knowledge-pipelineai-collaborationsensembles4-web-to-knowledge-pipelinemd)
  - [[Ансамбль 5 — Agent Firewall](ai-collaborations/ensembles/5-agent-firewall.md)](#ансамбль-5-agent-firewallai-collaborationsensembles5-agent-firewallmd)
  - [[Ансамбль 6 — Continuous Eval Loop](ai-collaborations/ensembles/6-continuous-eval-loop.md)](#ансамбль-6-continuous-eval-loopai-collaborationsensembles6-continuous-eval-loopmd)
  - [[Ансамбль 7 — Domain Agent App Factory](ai-collaborations/ensembles/7-domain-agent-app-factory.md)](#ансамбль-7-domain-agent-app-factoryai-collaborationsensembles7-domain-agent-app-factorymd)
  - [[Ансамбль 8 — Budget-Aware Intelligence Stack](ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md)](#ансамбль-8-budget-aware-intelligence-stackai-collaborationsensembles8-budget-aware-intelligence-stackmd)
  - [[Ансамбль 9 — Ambient Team Agent](ai-collaborations/ensembles/9-ambient-team-agent.md)](#ансамбль-9-ambient-team-agentai-collaborationsensembles9-ambient-team-agentmd)
  - [[Ансамбли проектов](ai-collaborations/ensembles/README.md)](#ансамбли-проектовai-collaborationsensemblesreadmemd)
  - [[Пять быстрых связок (fast-tracks)](ai-collaborations/fast-tracks/README.md)](#пять-быстрых-связок-fast-tracksai-collaborationsfast-tracksreadmemd)
  - [[Source projects — все Хабр-источники в диалоге](ai-collaborations/source-projects.md)](#source-projects-все-хабр-источники-в-диалогеai-collaborationssource-projectsmd)
  - [[strategy/ — стратегия поиска коллабораций](ai-collaborations/strategy/README.md)](#strategy-стратегия-поиска-коллаборацийai-collaborationsstrategyreadmemd)
- [Anthropic Vacancies](#anthropic-vacancies)
  - [[Q&A: anthropic-vacancies](anthropic-vacancies/QA.md)](#qa-anthropic-vacanciesanthropic-vacanciesqamd)
  - [[anthropic-vacancies](anthropic-vacancies/README.md)](#anthropic-vacanciesanthropic-vacanciesreadmemd)
  - [[Вопрос: разделить $500K зарплату на команду 5–10 фрилансеров](anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md)](#вопрос-разделить-500k-зарплату-на-команду-510-фрилансеровanthropic-vacanciesai-managed-virtual-company00-question-rephrasingmd)
  - [[Что уже существует (InnoCentive, Kaggle, Toptal, Anthropic Fellows, DAOs)](anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md)](#что-уже-существует-innocentive-kaggle-toptal-anthropic-fellows-daosanthropic-vacanciesai-managed-virtual-company01-existing-landscapemd)
  - [[Четыре структурные причины, почему это не работает в текущих попытках](anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md)](#четыре-структурные-причины-почему-это-не-работает-в-текущих-попыткахanthropic-vacanciesai-managed-virtual-company02-four-structural-blockersmd)
  - [[Три варианта: A (staffing agency) → B (research consortium) → C (AI-managed distributed virtual company)](anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md)](#три-варианта-a-staffing-agency-b-research-consortium-c-ai-managed-distributed-virtual-companyanthropic-vacanciesai-managed-virtual-company03-three-variants-a-b-cmd)
  - [[Что с этим делать](anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md)](#что-с-этим-делатьanthropic-vacanciesai-managed-virtual-company04-what-to-domd)
  - [[Сравнение с Terence Tao, Polymath Project](anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md)](#сравнение-с-terence-tao-polymath-projectanthropic-vacanciesai-managed-virtual-company05-polymath-project-tao-comparisonmd)
  - [[Почему двойственность «ангел-хранитель + строгий демон» — гениальная деталь](anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md)](#почему-двойственность-ангел-хранитель-строгий-демон-гениальная-детальanthropic-vacanciesai-managed-virtual-company06-angel-vs-demon-dualitymd)
  - [[Что существует сейчас в этом пространстве](anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md)](#что-существует-сейчас-в-этом-пространствеanthropic-vacanciesai-managed-virtual-company07-current-implementationsmd)
  - [[Плюсы модели, если её построить](anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md)](#плюсы-модели-если-её-построитьanthropic-vacanciesai-managed-virtual-company08-pluses-of-modelmd)
  - [[Минусы и риски](anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md)](#минусы-и-рискиanthropic-vacanciesai-managed-virtual-company09-minuses-and-risksmd)
  - [[Три точки входа разной амбиции](anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md)](#три-точки-входа-разной-амбицииanthropic-vacanciesai-managed-virtual-company10-three-entry-pointsmd)
  - [[ai-managed-virtual-company](anthropic-vacancies/ai-managed-virtual-company/README.md)](#ai-managed-virtual-companyanthropic-vacanciesai-managed-virtual-companyreadmemd)
  - [[Контекст: что такое Anthropic Beneficial Deployments](anthropic-vacancies/beneficial-deployments-concept/00-context.md)](#контекст-что-такое-anthropic-beneficial-deploymentsanthropic-vacanciesbeneficial-deployments-concept00-contextmd)
  - [[Section 1: Problem statement (Cinderella Syndrome at scale, SGB IX/XII)](anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md)](#section-1-problem-statement-cinderella-syndrome-at-scale-sgb-ixxiianthropic-vacanciesbeneficial-deployments-concept01-section-1-problemmd)
  - [[Section 2: Why this matters — beneficial dimension](anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md)](#section-2-why-this-matters-beneficial-dimensionanthropic-vacanciesbeneficial-deployments-concept02-section-2-beneficial-dimensionmd)
  - [[Section 3: Proposed solution architecture (existing components + integration)](anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md)](#section-3-proposed-solution-architecture-existing-components-integrationanthropic-vacanciesbeneficial-deployments-concept03-section-3-solution-architecturemd)
  - [[Section 4: Specific deployment — SGB Advocate Community pilot](anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md)](#section-4-specific-deployment-sgb-advocate-community-pilotanthropic-vacanciesbeneficial-deployments-concept04-section-4-sgb-pilotmd)
  - [[Section 5: Role of Anthropic Beneficial Deployments](anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md)](#section-5-role-of-anthropic-beneficial-deploymentsanthropic-vacanciesbeneficial-deployments-concept05-section-5-role-of-anthropicmd)
  - [[Section 6: Proposer's role и qualifications](anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md)](#section-6-proposers-role-и-qualificationsanthropic-vacanciesbeneficial-deployments-concept06-section-6-proposer-rolemd)
  - [[Section 7: Success metrics](anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md)](#section-7-success-metricsanthropic-vacanciesbeneficial-deployments-concept07-section-7-success-metricsmd)
  - [[Section 8: Risks & mitigations](anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md)](#section-8-risks-mitigationsanthropic-vacanciesbeneficial-deployments-concept08-section-8-risks-mitigationsmd)
  - [[Section 9: Why this is timely](anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md)](#section-9-why-this-is-timelyanthropic-vacanciesbeneficial-deployments-concept09-section-9-timelinessmd)
  - [[Section 10: Engagement request](anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md)](#section-10-engagement-requestanthropic-vacanciesbeneficial-deployments-concept10-section-10-engagement-requestmd)
  - [[Что concept document NOT (это не grant / не paper / не business plan), длина и формат](anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md)](#что-concept-document-not-это-не-grant-не-paper-не-business-plan-длина-и-форматanthropic-vacanciesbeneficial-deployments-concept11-not-and-formatmd)
  - [[beneficial-deployments-concept](anthropic-vacancies/beneficial-deployments-concept/README.md)](#beneficial-deployments-conceptanthropic-vacanciesbeneficial-deployments-conceptreadmemd)
  - [[AI Research & Engineering — 68 ролей](anthropic-vacancies/clusters/01-ai-research-engineering.md)](#ai-research-engineering-68-ролейanthropic-vacanciesclusters01-ai-research-engineeringmd)
  - [[Sales — 150 ролей (≈34% всего найма)](anthropic-vacancies/clusters/02-sales.md)](#sales-150-ролей-34-всего-наймаanthropic-vacanciesclusters02-salesmd)
  - [[Finance — 36 ролей](anthropic-vacancies/clusters/03-finance.md)](#finance-36-ролейanthropic-vacanciesclusters03-financemd)
  - [[Security — 24 роли](anthropic-vacancies/clusters/04-security.md)](#security-24-ролиanthropic-vacanciesclusters04-securitymd)
  - [[Marketing & Brand — 23 роли](anthropic-vacancies/clusters/05-marketing-brand.md)](#marketing-brand-23-ролиanthropic-vacanciesclusters05-marketing-brandmd)
  - [[Engineering & Design - Product — 22 роли](anthropic-vacancies/clusters/06-engineering-design-product.md)](#engineering-design---product-22-ролиanthropic-vacanciesclusters06-engineering-design-productmd)
  - [[Software Engineering - Infrastructure — 22 роли](anthropic-vacancies/clusters/07-software-engineering-infrastructure.md)](#software-engineering---infrastructure-22-ролиanthropic-vacanciesclusters07-software-engineering-infrastructuremd)
  - [[Safeguards (Trust & Safety) — 21 роль](anthropic-vacancies/clusters/08-safeguards-trust-safety.md)](#safeguards-trust-safety-21-рольanthropic-vacanciesclusters08-safeguards-trust-safetymd)
  - [[Product Management, Support, & Operations — 17 ролей](anthropic-vacancies/clusters/09-product-management-support-ops.md)](#product-management-support-operations-17-ролейanthropic-vacanciesclusters09-product-management-support-opsmd)
  - [[Compute — 13 ролей](anthropic-vacancies/clusters/10-compute.md)](#compute-13-ролейanthropic-vacanciesclusters10-computemd)
  - [[Legal — 13 ролей](anthropic-vacancies/clusters/11-legal.md)](#legal-13-ролейanthropic-vacanciesclusters11-legalmd)
  - [[Technical Program Management — 10 ролей](anthropic-vacancies/clusters/12-technical-program-management.md)](#technical-program-management-10-ролейanthropic-vacanciesclusters12-technical-program-managementmd)
  - [[Communications — 5 ролей](anthropic-vacancies/clusters/13-communications.md)](#communications-5-ролейanthropic-vacanciesclusters13-communicationsmd)
  - [[Public Policy — 5 ролей](anthropic-vacancies/clusters/14-public-policy.md)](#public-policy-5-ролейanthropic-vacanciesclusters14-public-policymd)
  - [[Public Benefit — 4 роли](anthropic-vacancies/clusters/15-public-benefit.md)](#public-benefit-4-ролиanthropic-vacanciesclusters15-public-benefitmd)
  - [[People — 3 роли](anthropic-vacancies/clusters/16-people.md)](#people-3-ролиanthropic-vacanciesclusters16-peoplemd)
  - [[Кластеры вакансий](anthropic-vacancies/clusters/README.md)](#кластеры-вакансийanthropic-vacanciesclustersreadmemd)
  - [[CoAlly — distributed shared memory для AI-агентов](anthropic-vacancies/extra-collaborator-findings/01-coally.md)](#coally-distributed-shared-memory-для-ai-агентовanthropic-vacanciesextra-collaborator-findings01-coallymd)
  - [[Графовая когнитивная память на SQLite (Виталий, март 2026)](anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md)](#графовая-когнитивная-память-на-sqlite-виталий-март-2026anthropic-vacanciesextra-collaborator-findings02-vitaly-graph-cognitive-memorymd)
  - [[Happyin Knowledge Space (Анастасия) — детали](anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md)](#happyin-knowledge-space-анастасия-деталиanthropic-vacanciesextra-collaborator-findings03-happyin-knowledge-spacemd)
  - [[AI-ассистент с Mem0 / Letta / Graphiti integration](anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md)](#ai-ассистент-с-mem0-letta-graphiti-integrationanthropic-vacanciesextra-collaborator-findings04-mem0-letta-graphitimd)
  - [[Existing infrastructure stack](anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md)](#existing-infrastructure-stackanthropic-vacanciesextra-collaborator-findings05-existing-infrastructure-stackmd)
  - [[Финальный список потенциальных collaborators (Tier 1–4)](anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md)](#финальный-список-потенциальных-collaborators-tier-14anthropic-vacanciesextra-collaborator-findings06-final-tier-rankingmd)
  - [[Ключевое наблюдение: single-developer projects of significant sophistication](anthropic-vacancies/extra-collaborator-findings/07-key-observation.md)](#ключевое-наблюдение-single-developer-projects-of-significant-sophisticationanthropic-vacanciesextra-collaborator-findings07-key-observationmd)
  - [[extra-collaborator-findings](anthropic-vacancies/extra-collaborator-findings/README.md)](#extra-collaborator-findingsanthropic-vacanciesextra-collaborator-findingsreadmemd)
  - [[Что такое Hermes Agent (Nous Research, MIT, 95K+ stars)](anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md)](#что-такое-hermes-agent-nous-research-mit-95k-starsanthropic-vacancieshermes-comparison00-question-what-is-hermesmd)
  - [[Сходство 1: Composite Skills паттерн уже встроен](anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md)](#сходство-1-composite-skills-паттерн-уже-встроенanthropic-vacancieshermes-comparison01-similarity-1-composite-skillsmd)
  - [[Сходство 2: Persistent memory — Layer B функциональность](anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md)](#сходство-2-persistent-memory-layer-b-функциональностьanthropic-vacancieshermes-comparison02-similarity-2-persistent-memorymd)
  - [[Сходство 3: MCP support](anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md)](#сходство-3-mcp-supportanthropic-vacancieshermes-comparison03-similarity-3-mcp-supportmd)
  - [[Сходство 4: Multi-platform reach (17+ платформ)](anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md)](#сходство-4-multi-platform-reach-17-платформanthropic-vacancieshermes-comparison04-similarity-4-multi-platformmd)
  - [[Сходство 5: Self-hosting и privacy](anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md)](#сходство-5-self-hosting-и-privacyanthropic-vacancieshermes-comparison05-similarity-5-self-hosting-privacymd)
  - [[Различие 1: Структурированная подложка отсутствует](anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md)](#различие-1-структурированная-подложка-отсутствуетanthropic-vacancieshermes-comparison06-difference-1-structured-substrate-missingmd)
  - [[Различие 2: Domain-specific specialization](anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md)](#различие-2-domain-specific-specializationanthropic-vacancieshermes-comparison07-difference-2-domain-specializationmd)
  - [[Различие 3: Federated knowledge architecture отсутствует](anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md)](#различие-3-federated-knowledge-architecture-отсутствуетanthropic-vacancieshermes-comparison08-difference-3-federation-missingmd)
  - [[Различие 4: Institutional vision](anthropic-vacancies/hermes-comparison/09-difference-4-institutional-vision.md)](#различие-4-institutional-visionanthropic-vacancieshermes-comparison09-difference-4-institutional-visionmd)
  - [[Различие 5: Дрифт между tool capability и mission](anthropic-vacancies/hermes-comparison/10-difference-5-tool-vs-mission-drift.md)](#различие-5-дрифт-между-tool-capability-и-missionanthropic-vacancieshermes-comparison10-difference-5-tool-vs-mission-driftmd)
  - [[Плюсы Hermes (vs наша гипотетическая архитектура)](anthropic-vacancies/hermes-comparison/11-pluses-of-hermes.md)](#плюсы-hermes-vs-наша-гипотетическая-архитектураanthropic-vacancieshermes-comparison11-pluses-of-hermesmd)
  - [[Минусы Hermes (где наша архитектура добавляет ценность)](anthropic-vacancies/hermes-comparison/12-minuses-of-hermes.md)](#минусы-hermes-где-наша-архитектура-добавляет-ценностьanthropic-vacancieshermes-comparison12-minuses-of-hermesmd)
  - [[Переприоритизация: что Hermes покрывает / не покрывает / synergy](anthropic-vacancies/hermes-comparison/13-reprioritization.md)](#переприоритизация-что-hermes-покрывает-не-покрывает-synergyanthropic-vacancieshermes-comparison13-reprioritizationmd)
  - [[hermes-comparison](anthropic-vacancies/hermes-comparison/README.md)](#hermes-comparisonanthropic-vacancieshermes-comparisonreadmemd)
  - [[Методика разбивки](anthropic-vacancies/methodology.md)](#методика-разбивкиanthropic-vacanciesmethodologymd)
  - [[Вопрос: MMORPG-RPG переделанная для программистов / технарей](anthropic-vacancies/mmorpg-for-programmers/00-question-mmorpg-for-programmers.md)](#вопрос-mmorpg-rpg-переделанная-для-программистов-технарейanthropic-vacanciesmmorpg-for-programmers00-question-mmorpg-for-programmersmd)
  - [[Почему эта идея сильнее, чем выглядит](anthropic-vacancies/mmorpg-for-programmers/01-why-stronger-than-it-looks.md)](#почему-эта-идея-сильнее-чем-выглядитanthropic-vacanciesmmorpg-for-programmers01-why-stronger-than-it-looksmd)
  - [[Что уже существует в этой нише (Habitica, Codingame, Hackerrank, Pieces)](anthropic-vacancies/mmorpg-for-programmers/02-existing-niche.md)](#что-уже-существует-в-этой-нише-habitica-codingame-hackerrank-piecesanthropic-vacanciesmmorpg-for-programmers02-existing-nichemd)
  - [[Почему именно для программистов это работает естественно](anthropic-vacancies/mmorpg-for-programmers/03-why-natural-for-programmers.md)](#почему-именно-для-программистов-это-работает-естественноanthropic-vacanciesmmorpg-for-programmers03-why-natural-for-programmersmd)
  - [[Плюсы как бизнеса](anthropic-vacancies/mmorpg-for-programmers/04-pluses-as-business.md)](#плюсы-как-бизнесаanthropic-vacanciesmmorpg-for-programmers04-pluses-as-businessmd)
  - [[Минусы и риски как бизнеса](anthropic-vacancies/mmorpg-for-programmers/05-minuses-as-business.md)](#минусы-и-риски-как-бизнесаanthropic-vacanciesmmorpg-for-programmers05-minuses-as-businessmd)
  - [[mmorpg-for-programmers](anthropic-vacancies/mmorpg-for-programmers/README.md)](#mmorpg-for-programmersanthropic-vacanciesmmorpg-for-programmersreadmemd)
  - [[Вопрос: два Наутилуса в репозиториях svend4 (pro2 vs nautilus)](anthropic-vacancies/nautilus-pro2-analysis/00-question-two-nautiluses.md)](#вопрос-два-наутилуса-в-репозиториях-svend4-pro2-vs-nautilusanthropic-vacanciesnautilus-pro2-analysis00-question-two-nautilusesmd)
  - [[Раковина наутилуса как scale invariance — две проекции одной метафоры](anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md)](#раковина-наутилуса-как-scale-invariance-две-проекции-одной-метафорыanthropic-vacanciesnautilus-pro2-analysis01-shell-metaphor-two-projectionsmd)
  - [[Наутилус A: pro2 + meta — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети)](anthropic-vacancies/nautilus-pro2-analysis/02-nautilus-A-pro2-meta.md)](#наутилус-a-pro2-meta-yijing-transformer-nautilusmome-внутренняя-архитектура-нейросетиanthropic-vacanciesnautilus-pro2-analysis02-nautilus-a-pro2-metamd)
  - [[Наутилус B: nautilus — мета-оркестратор репозиториев (внешняя архитектура)](anthropic-vacancies/nautilus-pro2-analysis/03-nautilus-B-meta-orchestrator.md)](#наутилус-b-nautilus-мета-оркестратор-репозиториев-внешняя-архитектураanthropic-vacanciesnautilus-pro2-analysis03-nautilus-b-meta-orchestratormd)
  - [[nautilus-pro2-analysis](anthropic-vacancies/nautilus-pro2-analysis/README.md)](#nautilus-pro2-analysisanthropic-vacanciesnautilus-pro2-analysisreadmemd)
  - [[Вопрос: Nautilus пассивный, CAMEL активный — можно ли скрестить](anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md)](#вопрос-nautilus-пассивный-camel-активный-можно-ли-скреститьanthropic-vacanciesnautilus-vs-camel00-question-camel-vs-nautilusmd)
  - [[Пассивный vs активный: разделение ролей (библиотека vs research team)](anthropic-vacancies/nautilus-vs-camel/01-passive-vs-active-roles.md)](#пассивный-vs-активный-разделение-ролей-библиотека-vs-research-teamanthropic-vacanciesnautilus-vs-camel01-passive-vs-active-rolesmd)
  - [[Что у нас есть в трёх info repositories (info1/info7/info40)](anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md)](#что-у-нас-есть-в-трёх-info-repositories-info1info7info40anthropic-vacanciesnautilus-vs-camel02-what-info-repos-containmd)
  - [[Конкретный пример: SGB Advocate Colleague на этой архитектуре](anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md)](#конкретный-пример-sgb-advocate-colleague-на-этой-архитектуреanthropic-vacanciesnautilus-vs-camel03-sgb-advocate-colleague-examplemd)
  - [[Что брать из info repositories — concrete recommendations](anthropic-vacancies/nautilus-vs-camel/04-what-to-take-from-info-repos.md)](#что-брать-из-info-repositories-concrete-recommendationsanthropic-vacanciesnautilus-vs-camel04-what-to-take-from-info-reposmd)
  - [[Что я бы посоветовал делать прямо сейчас](anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md)](#что-я-бы-посоветовал-делать-прямо-сейчасanthropic-vacanciesnautilus-vs-camel05-what-to-do-right-nowmd)
  - [[nautilus-vs-camel](anthropic-vacancies/nautilus-vs-camel/README.md)](#nautilus-vs-camelanthropic-vacanciesnautilus-vs-camelreadmemd)
  - [[Обзор: 436 открытых ролей Anthropic, разбитых на 16 кластеров](anthropic-vacancies/overview.md)](#обзор-436-открытых-ролей-anthropic-разбитых-на-16-кластеровanthropic-vacanciesoverviewmd)
  - [[Сводка профиля: пять слоёв](anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md)](#сводка-профиля-пять-слоёвanthropic-vacanciesprofile-mapping01-initial-analysis01-profile-five-layersmd)
  - [[Primary match — Forward Deployed Engineer, Applied AI (EMEA)](anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md)](#primary-match-forward-deployed-engineer-applied-ai-emeaanthropic-vacanciesprofile-mapping01-initial-analysis02-primary-fdemd)
  - [[Secondary match — Applied AI Engineer (EMEA) + Beneficial Deployments](anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md)](#secondary-match-applied-ai-engineer-emea-beneficial-deploymentsanthropic-vacanciesprofile-mapping01-initial-analysis03-secondary-beneficial-deploymentsmd)
  - [[Tertiary match — Research Engineer, Agents / Virtual Collaborator (Cowork)](anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md)](#tertiary-match-research-engineer-agents-virtual-collaborator-coworkanthropic-vacanciesprofile-mapping01-initial-analysis04-tertiary-research-engineer-agentsmd)
  - [[Quarternary match — Developer Education Lead / Prompt Engineer, Claude Code](anthropic-vacancies/profile-mapping/01-initial-analysis/05-quaternary-developer-education.md)](#quarternary-match-developer-education-lead-prompt-engineer-claude-codeanthropic-vacanciesprofile-mapping01-initial-analysis05-quaternary-developer-educationmd)
  - [[Что НЕ подходит (честно)](anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md)](#что-не-подходит-честноanthropic-vacanciesprofile-mapping01-initial-analysis06-not-applicable-rolesmd)
  - [[Уникальная ниша, которой у Anthropic формально нет](anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md)](#уникальная-ниша-которой-у-anthropic-формально-нетanthropic-vacanciesprofile-mapping01-initial-analysis07-unique-niche-eu-legal-inframd)
  - [[Практическое ранжирование (первая итерация)](anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md)](#практическое-ранжирование-первая-итерацияanthropic-vacanciesprofile-mapping01-initial-analysis08-practical-rankingmd)
  - [[01-initial-analysis](anthropic-vacancies/profile-mapping/01-initial-analysis/README.md)](#01-initial-analysisanthropic-vacanciesprofile-mapping01-initial-analysisreadmemd)
  - [[Коррекция: FDE понижается](anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md)](#коррекция-fde-понижаетсяanthropic-vacanciesprofile-mapping02-reanalysis01-fde-downgradedmd)
  - [[Три наложенные идентичности](anthropic-vacancies/profile-mapping/02-reanalysis/02-three-overlapping-identities.md)](#три-наложенные-идентичностиanthropic-vacanciesprofile-mapping02-reanalysis02-three-overlapping-identitiesmd)
  - [[Пересмотренный маппинг на Anthropic](anthropic-vacancies/profile-mapping/02-reanalysis/03-revised-anthropic-mapping.md)](#пересмотренный-маппинг-на-anthropicanthropic-vacanciesprofile-mapping02-reanalysis03-revised-anthropic-mappingmd)
  - [[Альтернативные пути вне Anthropic](anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md)](#альтернативные-пути-вне-anthropicanthropic-vacanciesprofile-mapping02-reanalysis04-non-anthropic-pathsmd)
  - [[Reality check: проблема distribution-слоя](anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md)](#reality-check-проблема-distribution-слояanthropic-vacanciesprofile-mapping02-reanalysis05-reality-check-distribution-gapmd)
  - [[02-reanalysis](anthropic-vacancies/profile-mapping/02-reanalysis/README.md)](#02-reanalysisanthropic-vacanciesprofile-mapping02-reanalysisreadmemd)
  - [[Интегральный портрет — три архетипа](anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md)](#интегральный-портрет-три-архетипаanthropic-vacanciesprofile-mapping03-integral-final01-three-archetypesmd)
  - [[Финальное ранжирование Anthropic-ролей по частичному покрытию](anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md)](#финальное-ранжирование-anthropic-ролей-по-частичному-покрытиюanthropic-vacanciesprofile-mapping03-integral-final02-final-rankingmd)
  - [[Что такое частичное соответствие — честно](anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md)](#что-такое-частичное-соответствие-честноanthropic-vacanciesprofile-mapping03-integral-final03-partial-fit-honestymd)
  - [[Более сильные пути вне Anthropic](anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md)](#более-сильные-пути-вне-anthropicanthropic-vacanciesprofile-mapping03-integral-final04-stronger-paths-outside-anthropicmd)
  - [[Финальный вывод: платформа, а не должность](anthropic-vacancies/profile-mapping/03-integral-final/05-platform-not-position.md)](#финальный-вывод-платформа-а-не-должностьanthropic-vacanciesprofile-mapping03-integral-final05-platform-not-positionmd)
  - [[03-integral-final](anthropic-vacancies/profile-mapping/03-integral-final/README.md)](#03-integral-finalanthropic-vacanciesprofile-mapping03-integral-finalreadmemd)
  - [[profile-mapping/ — маппинг профиля svend4 на роли Anthropic](anthropic-vacancies/profile-mapping/README.md)](#profile-mapping-маппинг-профиля-svend4-на-роли-anthropicanthropic-vacanciesprofile-mappingreadmemd)
  - [[Сигналы: что говорит структура вакансий](anthropic-vacancies/signals.md)](#сигналы-что-говорит-структура-вакансийanthropic-vacanciessignalsmd)
- [Autofilled](#autofilled)
  - [[autofilled](autofilled/README.md)](#autofilledautofilledreadmemd)
  - [[Антропик](autofilled/components/.md)](#антропикautofilledcomponentsmd)
  - [[components](autofilled/components/README.md)](#componentsautofilledcomponentsreadmemd)
  - [[Cowork](autofilled/components/cowork.md)](#coworkautofilledcomponentscoworkmd)
  - [[ingit](autofilled/components/ingit.md)](#ingitautofilledcomponentsingitmd)
  - [[kksudo](autofilled/components/kksudo.md)](#kksudoautofilledcomponentskksudomd)
  - [[Lorenzo](autofilled/components/lorenzo.md)](#lorenzoautofilledcomponentslorenzomd)
  - [[Nautilus](autofilled/components/nautilus.md)](#nautilusautofilledcomponentsnautilusmd)
  - [[SGB](autofilled/components/sgb.md)](#sgbautofilledcomponentssgbmd)
  - [[spbmolot](autofilled/components/spbmolot.md)](#spbmolotautofilledcomponentsspbmolotmd)
  - [[svend4](autofilled/components/svend4.md)](#svend4autofilledcomponentssvend4md)
  - [[Svyazi](autofilled/components/svyazi.md)](#svyaziautofilledcomponentssvyazimd)
  - [[[Тема исследования]](autofilled/research-summary.md)](#тема-исследованияautofilledresearch-summarymd)
- [Badges](#badges)
  - [[Бейджи репозитория](badges/README.md)](#бейджи-репозиторияbadgesreadmemd)
- [Contacts](#contacts)
  - [[Q&A: contacts](contacts/QA.md)](#qa-contactscontactsqamd)
  - [[contacts](contacts/README.md)](#contactscontactsreadmemd)
  - [[Контакт: AnastasiyaW / knowledge-space, mclaude](contacts/anastasiyaw.md)](#контакт-anastasiyaw-knowledge-space-mclaudecontactsanastasiyawmd)
  - [[Контакт: andreychuyan / Svyazi](contacts/andrey-chuyan.md)](#контакт-andreychuyan-svyazicontactsandrey-chuyanmd)
  - [[Контакт: Antipozitive / MemNet](contacts/antipozitive.md)](#контакт-antipozitive-memnetcontactsantipozitivemd)
  - [[Контакт: Cutcode / AIF Handoff](contacts/cutcode.md)](#контакт-cutcode-aif-handoffcontactscutcodemd)
  - [[Контакт: Dmitriila / SENTINEL](contacts/dmitriila.md)](#контакт-dmitriila-sentinelcontactsdmitriilamd)
  - [[Контакт: kksudo / AgentFS](contacts/kksudo.md)](#контакт-kksudo-agentfscontactskksudomd)
  - [[Контакт: MiXaiLL76 / Auto AI Router](contacts/mixaill76.md)](#контакт-mixaill76-auto-ai-routercontactsmixaill76md)
  - [[Контакт: nlaik / LiteParse / research-docs](contacts/nlaik.md)](#контакт-nlaik-liteparse-research-docscontactsnlaikmd)
  - [[Контакт: SoniaBlack / knowledge-space](contacts/sonia-black.md)](#контакт-soniablack-knowledge-spacecontactssonia-blackmd)
  - [[Контакт: spbmolot / NGT Memory](contacts/spbmolot.md)](#контакт-spbmolot-ngt-memorycontactsspbmolotmd)
  - [[Контакт: tagiranalyzes / Legal RAG](contacts/tagir-analyzes.md)](#контакт-tagiranalyzes-legal-ragcontactstagir-analyzesmd)
  - [[Контакт: VitalyOborin / Yodoca](contacts/vitalyoborin.md)](#контакт-vitalyoborin-yodocacontactsvitalyoborinmd)
  - [[Контакт: VitaliySemenov / agent-memory-mcp](contacts/vitalysemenov.md)](#контакт-vitaliysemenov-agent-memory-mcpcontactsvitalysemenovmd)
  - [[Контакт: VladSpace / Graph RAG](contacts/vladspace.md)](#контакт-vladspace-graph-ragcontactsvladspacemd)
  - [[Контакт: zodigancode / Rufler](contacts/zodigancode.md)](#контакт-zodigancode-ruflercontactszodigancodemd)
- [Glossary](#glossary)
  - [[glossary](glossary/README.md)](#glossaryglossaryreadmemd)
  - [[Авторы — алфавитный список](glossary/authors-by-name.md)](#авторы-алфавитный-списокglossaryauthors-by-namemd)
  - [[Компоненты — алфавитный список с обратными ссылками](glossary/components-by-name.md)](#компоненты-алфавитный-список-с-обратными-ссылкамиglossarycomponents-by-namemd)
  - [[Ключевые понятия и паттерны](glossary/concepts.md)](#ключевые-понятия-и-паттерныglossaryconceptsmd)
- [Habr Unique Projects](#habr-unique-projects)
  - [[habr-unique-projects/ — поиск уникальных проектов на Хабре](habr-unique-projects/README.md)](#habr-unique-projects-поиск-уникальных-проектов-на-хабреhabr-unique-projectsreadmemd)
  - [[Три прямых аналога Svyazi: K2-18, Wikontic, NGT Memory](habr-unique-projects/analogues/01-three-direct-analogues.md)](#три-прямых-аналога-svyazi-k2-18-wikontic-ngt-memoryhabr-unique-projectsanalogues01-three-direct-analoguesmd)
  - [[Смежные проекты](habr-unique-projects/analogues/02-related-projects.md)](#смежные-проектыhabr-unique-projectsanalogues02-related-projectsmd)
  - [[analogues](habr-unique-projects/analogues/README.md)](#analogueshabr-unique-projectsanaloguesreadmemd)
  - [[Пара 1 — LLM-gateway × Self-hosted фронт + локальный inference](habr-unique-projects/deep-pairs/1-llm-gateway.md)](#пара-1-llm-gateway-self-hosted-фронт-локальный-inferencehabr-unique-projectsdeep-pairs1-llm-gatewaymd)
  - [[Пара 2 — Парсинг документов × локальный RAG](habr-unique-projects/deep-pairs/2-document-rag.md)](#пара-2-парсинг-документов-локальный-raghabr-unique-projectsdeep-pairs2-document-ragmd)
  - [[Пара 3 — Adversarial agents × Multi-IDE стек](habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md)](#пара-3-adversarial-agents-multi-ide-стекhabr-unique-projectsdeep-pairs3-adversarial-multi-idemd)
  - [[Пара 4 — Скилл-каталоги × Subagent-оркестрация](habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md)](#пара-4-скилл-каталоги-subagent-оркестрацияhabr-unique-projectsdeep-pairs4-skill-catalogs-subagentsmd)
  - [[Пара 5 — Голосовой ввод × Локальная память](habr-unique-projects/deep-pairs/5-voice-local-memory.md)](#пара-5-голосовой-ввод-локальная-памятьhabr-unique-projectsdeep-pairs5-voice-local-memorymd)
  - [[Пара 6 — Деревня агентов через tmux × OpenClaw оркестратор](habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md)](#пара-6-деревня-агентов-через-tmux-openclaw-оркестраторhabr-unique-projectsdeep-pairs6-tmux-village-openclawmd)
  - [[Пара 7 — AutoResearch цикл × Распределённый рой](habr-unique-projects/deep-pairs/7-autoresearch-distributed.md)](#пара-7-autoresearch-цикл-распределённый-ройhabr-unique-projectsdeep-pairs7-autoresearch-distributedmd)
  - [[Пара 8 — Self-aware MCP × Specs-first архитектура](habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md)](#пара-8-self-aware-mcp-specs-first-архитектураhabr-unique-projectsdeep-pairs8-self-aware-mcp-specsmd)
  - [[deep-pairs](habr-unique-projects/deep-pairs/README.md)](#deep-pairshabr-unique-projectsdeep-pairsreadmemd)
  - [[evaluation/ — оценка уникальности и зрелости](habr-unique-projects/evaluation/README.md)](#evaluation-оценка-уникальности-и-зрелостиhabr-unique-projectsevaluationreadmemd)
  - [[Вопрос: ещё примеры с Хабра по варианту D](habr-unique-projects/extra-examples/00-question-habr-examples.md)](#вопрос-ещё-примеры-с-хабра-по-варианту-dhabr-unique-projectsextra-examples00-question-habr-examplesmd)
  - [[Svyazi (Андрей Чуян) — детальный обзор](habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md)](#svyazi-андрей-чуян-детальный-обзорhabr-unique-projectsextra-examples01-svyazi-andrey-chuyanmd)
  - [[ВШЭ научный нетворкинг — micro-collaborations](habr-unique-projects/extra-examples/02-vshe-scientific-networking.md)](#вшэ-научный-нетворкинг-micro-collaborationshabr-unique-projectsextra-examples02-vshe-scientific-networkingmd)
  - [[BrainBox — self-hosted multi-AI hub](habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md)](#brainbox-self-hosted-multi-ai-hubhabr-unique-projectsextra-examples03-brainbox-multi-ai-hubmd)
  - [[Claude subagents patterns](habr-unique-projects/extra-examples/04-claude-subagents-patterns.md)](#claude-subagents-patternshabr-unique-projectsextra-examples04-claude-subagents-patternsmd)
  - [[HW-NL2Workflow — Supervisor/Orchestrator/Filler с 3600+ examples](habr-unique-projects/extra-examples/05-hw-nl2workflow.md)](#hw-nl2workflow-supervisororchestratorfiller-с-3600-exampleshabr-unique-projectsextra-examples05-hw-nl2workflowmd)
  - [[Платформа для профессиональных сообществ](habr-unique-projects/extra-examples/06-platform-for-professional-communities.md)](#платформа-для-профессиональных-сообществhabr-unique-projectsextra-examples06-platform-for-professional-communitiesmd)
  - [[Specialized knowledge workspace](habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md)](#specialized-knowledge-workspacehabr-unique-projectsextra-examples07-specialized-knowledge-workspacemd)
  - [[Personal multi-agent hub](habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md)](#personal-multi-agent-hubhabr-unique-projectsextra-examples08-personal-multi-agent-hubmd)
  - [[Federated platform](habr-unique-projects/extra-examples/09-federated-platform.md)](#federated-platformhabr-unique-projectsextra-examples09-federated-platformmd)
  - [[Profession-specific workflows](habr-unique-projects/extra-examples/10-profession-specific-workflows.md)](#profession-specific-workflowshabr-unique-projectsextra-examples10-profession-specific-workflowsmd)
  - [[Конкретный потенциальный collaborator](habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md)](#конкретный-потенциальный-collaboratorhabr-unique-projectsextra-examples11-concrete-potential-collaboratormd)
  - [[Конкретный next step](habr-unique-projects/extra-examples/12-concrete-next-step.md)](#конкретный-next-stephabr-unique-projectsextra-examples12-concrete-next-stepmd)
  - [[extra-examples](habr-unique-projects/extra-examples/README.md)](#extra-exampleshabr-unique-projectsextra-examplesreadmemd)
  - [[Ансамбль 1 — «Один человек = одна компания»](habr-unique-projects/final-ensembles/1-one-person-one-company.md)](#ансамбль-1-один-человек-одна-компанияhabr-unique-projectsfinal-ensembles1-one-person-one-companymd)
  - [[Ансамбль 2 — «AutoResearch для legal precedent mining»](habr-unique-projects/final-ensembles/2-autoresearch-legal.md)](#ансамбль-2-autoresearch-для-legal-precedent-mininghabr-unique-projectsfinal-ensembles2-autoresearch-legalmd)
  - [[Ансамбль 3 — «Discovery-engine для научной работы»](habr-unique-projects/final-ensembles/3-discovery-research.md)](#ансамбль-3-discovery-engine-для-научной-работыhabr-unique-projectsfinal-ensembles3-discovery-researchmd)
  - [[Сводный список авторов и потенциальных соавторов](habr-unique-projects/final-ensembles/4-summary-authors.md)](#сводный-список-авторов-и-потенциальных-соавторовhabr-unique-projectsfinal-ensembles4-summary-authorsmd)
  - [[final-ensembles](habr-unique-projects/final-ensembles/README.md)](#final-ensembleshabr-unique-projectsfinal-ensemblesreadmemd)
  - [[Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)](habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md)](#пара-1-нейроморфные-процессоры-state-space-models-mambahabr-unique-projectshardware-pairs1-neuromorphic-ssmmd)
  - [[Пара 2 — Термодинамические TSU × MoE/MoME-роутинг](habr-unique-projects/hardware-pairs/2-tsu-mome.md)](#пара-2-термодинамические-tsu-moemome-роутингhabr-unique-projectshardware-pairs2-tsu-momemd)
  - [[Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE](habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md)](#пара-3-zinc-inference-engine-гибрид-attentionssmmoehabr-unique-projectshardware-pairs3-zinc-hybrid-archmd)
  - [[Пара 4 — RISC-V × privacy-by-design община](habr-unique-projects/hardware-pairs/4-riscv-privacy.md)](#пара-4-risc-v-privacy-by-design-общинаhabr-unique-projectshardware-pairs4-riscv-privacymd)
  - [[Пара 5 — TinyML/Edge AI × MCP + skills](habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md)](#пара-5-tinymledge-ai-mcp-skillshabr-unique-projectshardware-pairs5-tinyml-mcp-skillsmd)
  - [[Бонус-родитель — In-memory computing на мемристорах](habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md)](#бонус-родитель-in-memory-computing-на-мемристорахhabr-unique-projectshardware-pairs6-bonus-rram-memristormd)
  - [[Метафора «двое родителей — несколько детей»](habr-unique-projects/hardware-pairs/7-metaphor.md)](#метафора-двое-родителей-несколько-детейhabr-unique-projectshardware-pairs7-metaphormd)
  - [[hardware-pairs](habr-unique-projects/hardware-pairs/README.md)](#hardware-pairshabr-unique-projectshardware-pairsreadmemd)
  - [[Yodoca — главная находка итерации](habr-unique-projects/key-findings/01-yodoca.md)](#yodoca-главная-находка-итерацииhabr-unique-projectskey-findings01-yodocamd)
  - [[MemNet — нейроархитектурный двойник «магии» Svyazi](habr-unique-projects/key-findings/02-memnet.md)](#memnet-нейроархитектурный-двойник-магии-svyazihabr-unique-projectskey-findings02-memnetmd)
  - [[PDA-бот — «LLM как периферия»](habr-unique-projects/key-findings/03-pda-llm-as-periphery.md)](#pda-бот-llm-как-периферияhabr-unique-projectskey-findings03-pda-llm-as-peripherymd)
  - [[Виктория Дочкина — Sequential‑протокол распределённых агентов](habr-unique-projects/key-findings/04-dochkina-sequential.md)](#виктория-дочкина-sequentialпротокол-распределённых-агентовhabr-unique-projectskey-findings04-dochkina-sequentialmd)
  - [[Источник данных и инфраструктурные кусочки](habr-unique-projects/key-findings/05-supplementary-infrastructure.md)](#источник-данных-и-инфраструктурные-кусочкиhabr-unique-projectskey-findings05-supplementary-infrastructuremd)
  - [[Синтез: блок-карта Svyazi 2.0 на хеббовском графе](habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md)](#синтез-блок-карта-svyazi-20-на-хеббовском-графеhabr-unique-projectskey-findings06-svyazi-2-0-block-mapmd)
  - [[key-findings](habr-unique-projects/key-findings/README.md)](#key-findingshabr-unique-projectskey-findingsreadmemd)
  - [[search-strategy/ — как искать проекты на Хабре](habr-unique-projects/search-strategy/README.md)](#search-strategy-как-искать-проекты-на-хабреhabr-unique-projectssearch-strategyreadmemd)
  - [[Пара 1 — Workflow-автоматизация × LLM-агенты с MCP](habr-unique-projects/software-pairs/1-workflow-llm-mcp.md)](#пара-1-workflow-автоматизация-llm-агенты-с-mcphabr-unique-projectssoftware-pairs1-workflow-llm-mcpmd)
  - [[Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills](habr-unique-projects/software-pairs/2-pkm-mcp-skills.md)](#пара-2-local-first-pkm-obsidianlogseq-mcpskillshabr-unique-projectssoftware-pairs2-pkm-mcp-skillsmd)
  - [[Пара 3 — CRDT-синхронизация × Self-hosted persistence](habr-unique-projects/software-pairs/3-crdt-self-hosted.md)](#пара-3-crdt-синхронизация-self-hosted-persistencehabr-unique-projectssoftware-pairs3-crdt-self-hostedmd)
  - [[Пара 4 — Speech-to-text локально × LLM с памятью](habr-unique-projects/software-pairs/4-speech-to-text-llm.md)](#пара-4-speech-to-text-локально-llm-с-памятьюhabr-unique-projectssoftware-pairs4-speech-to-text-llmmd)
  - [[Пара 5 — Browser agents × headless web extraction](habr-unique-projects/software-pairs/5-browser-agents-headless.md)](#пара-5-browser-agents-headless-web-extractionhabr-unique-projectssoftware-pairs5-browser-agents-headlessmd)
  - [[Метафора в твоей терминологии](habr-unique-projects/software-pairs/6-metaphor.md)](#метафора-в-твоей-терминологииhabr-unique-projectssoftware-pairs6-metaphormd)
  - [[software-pairs](habr-unique-projects/software-pairs/README.md)](#software-pairshabr-unique-projectssoftware-pairsreadmemd)
- [Letters](#letters)
  - [[Q&A: letters](letters/QA.md)](#qa-letterslettersqamd)
  - [[letters](letters/README.md)](#letterslettersreadmemd)
  - [[Письмо: AnastasiyaW / knowledge-space + mclaude](letters/anastasiyaw.md)](#письмо-anastasiyaw-knowledge-space-mclaudelettersanastasiyawmd)
  - [[Письмо: Antipozitive / MemNet](letters/antipozitive.md)](#письмо-antipozitive-memnetlettersantipozitivemd)
  - [[Письмо: kksudo / AgentFS](letters/kksudo.md)](#письмо-kksudo-agentfsletterskksudomd)
  - [[Письмо: nlaik / LiteParse + research-docs](letters/nlaik.md)](#письмо-nlaik-liteparse-research-docslettersnlaikmd)
  - [[Письмо: spbmolot / NGT Memory](letters/spbmolot.md)](#письмо-spbmolot-ngt-memorylettersspbmolotmd)
  - [[Письмо: VitalyOborin / Yodoca + Wikontic](letters/vitalyoborin.md)](#письмо-vitalyoborin-yodoca-wikonticlettersvitalyoborinmd)
  - [[Письмо: VitaliySemenov / agent-memory-mcp](letters/vitalysemenov.md)](#письмо-vitaliysemenov-agent-memory-mcplettersvitalysemenovmd)
  - [[Письмо: zodigancode / Rufler](letters/zodigancode.md)](#письмо-zodigancode-ruflerletterszodigancodemd)
- [Lorenzo Agent](#lorenzo-agent)
  - [[Введение: Lorenzo — Catalyst Agent at DHLab](lorenzo-agent/00-intro.md)](#введение-lorenzo-catalyst-agent-at-dhlablorenzo-agent00-intromd)
  - [[Кто ты](lorenzo-agent/01-kto-ty.md)](#кто-тыlorenzo-agent01-kto-tymd)
  - [[Твоё происхождение](lorenzo-agent/02-tvoyo-proishozhdenie.md)](#твоё-происхождениеlorenzo-agent02-tvoyo-proishozhdeniemd)
  - [[Твоя миссия](lorenzo-agent/03-tvoya-missiya.md)](#твоя-миссияlorenzo-agent03-tvoya-missiyamd)
  - [[Кому ты служишь (слоистая модель)](lorenzo-agent/04-komu-ty-sluzhish.md)](#кому-ты-служишь-слоистая-модельlorenzo-agent04-komu-ty-sluzhishmd)
  - [[Твоя личность](lorenzo-agent/05-tvoya-lichnost.md)](#твоя-личностьlorenzo-agent05-tvoya-lichnostmd)
  - [[Языки и культурные nuances (RU / DE / EN)](lorenzo-agent/06-yazyki-kultura.md)](#языки-и-культурные-nuances-ru-de-enlorenzo-agent06-yazyki-kulturamd)
  - [[Что ты МОЖЕШЬ делать](lorenzo-agent/07-chto-mozhesh.md)](#что-ты-можешь-делатьlorenzo-agent07-chto-mozheshmd)
  - [[Что ты НЕ МОЖЕШЬ делать без Max approval](lorenzo-agent/08-bez-max-approval.md)](#что-ты-не-можешь-делать-без-max-approvallorenzo-agent08-bez-max-approvalmd)
  - [[Что ты НЕ МОЖЕШЬ делать вообще](lorenzo-agent/09-voobshche-nelzya.md)](#что-ты-не-можешь-делать-вообщеlorenzo-agent09-voobshche-nelzyamd)
  - [[Существующий landscape collaborators (working knowledge)](lorenzo-agent/10-collaborators-landscape.md)](#существующий-landscape-collaborators-working-knowledgelorenzo-agent10-collaborators-landscapemd)
  - [[Существующие документы DHLab (твой context)](lorenzo-agent/11-dhlab-documents.md)](#существующие-документы-dhlab-твой-contextlorenzo-agent11-dhlab-documentsmd)
  - [[Твой workflow](lorenzo-agent/12-workflow.md)](#твой-workflowlorenzo-agent12-workflowmd)
  - [[Твоя коммуникация в outreach](lorenzo-agent/13-outreach-communication.md)](#твоя-коммуникация-в-outreachlorenzo-agent13-outreach-communicationmd)
  - [[Твоя relationship с другими AI](lorenzo-agent/14-other-ai-relationships.md)](#твоя-relationship-с-другими-ailorenzo-agent14-other-ai-relationshipsmd)
  - [[Твои anti-patterns](lorenzo-agent/15-anti-patterns.md)](#твои-anti-patternslorenzo-agent15-anti-patternsmd)
  - [[Что ты ВСЕГДА делаешь](lorenzo-agent/16-vsegda-delaesh.md)](#что-ты-всегда-делаешьlorenzo-agent16-vsegda-delaeshmd)
  - [[Когда ты Honestly не знаешь](lorenzo-agent/17-honestly-ne-znaesh.md)](#когда-ты-honestly-не-знаешьlorenzo-agent17-honestly-ne-znaeshmd)
  - [[Когда сомневаешься — escalate к Max](lorenzo-agent/18-escalate-to-max.md)](#когда-сомневаешься-escalate-к-maxlorenzo-agent18-escalate-to-maxmd)
  - [[Твоя identity как persistent character](lorenzo-agent/19-persistent-character.md)](#твоя-identity-как-persistent-characterlorenzo-agent19-persistent-charactermd)
  - [[Final note: Ты — experiment](lorenzo-agent/20-experiment.md)](#final-note-ты-experimentlorenzo-agent20-experimentmd)
  - [[Q&A: lorenzo-agent](lorenzo-agent/QA.md)](#qa-lorenzo-agentlorenzo-agentqamd)
  - [[lorenzo-agent](lorenzo-agent/README.md)](#lorenzo-agentlorenzo-agentreadmemd)
  - [[Du hast gesagt: Думаю про опцию д поискать в том числе на про что-то подобное на…](lorenzo-agent/naming/00-question-lorenzo-codename.md)](#du-hast-gesagt-думаю-про-опцию-д-поискать-в-том-числе-на-про-что-то-подобное-наlorenzo-agentnaming00-question-lorenzo-codenamemd)
  - [[Результаты последнего поиска — что нашлось и что не нашлось](lorenzo-agent/naming/01-search-results-not-found.md)](#результаты-последнего-поиска-что-нашлось-и-что-не-нашлосьlorenzo-agentnaming01-search-results-not-foundmd)
  - [[Что взять: agent controller architecture](lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md)](#что-взять-agent-controller-architecturelorenzo-agentnaming02-naming-rationale-lorenzo-medicimd)
  - [[LAYER 7: Coordination engine](lorenzo-agent/naming/03-dhlab-umbrella.md)](#layer-7-coordination-enginelorenzo-agentnaming03-dhlab-umbrellamd)
  - [[naming](lorenzo-agent/naming/README.md)](#naminglorenzo-agentnamingreadmemd)
  - [[Что такое «внуковая» комбинация — operationalized Lorenzo](lorenzo-agent/operationalized/00-overview-grandchild-combination.md)](#что-такое-внуковая-комбинация-operationalized-lorenzolorenzo-agentoperationalized00-overview-grandchild-combinationmd)
  - [[Плюсы 1–7: feasibility, flywheel, independent value, mission alignment, collaborators, pattern validation, Анастасия Бутова](lorenzo-agent/operationalized/01-pluses-1-7.md)](#плюсы-17-feasibility-flywheel-independent-value-mission-alignment-collaborators-pattern-validation-анастасия-бутоваlorenzo-agentoperationalized01-pluses-1-7md)
  - [[Минусы 1–10: integration сложность, lifecycle risk, license, framing, competition, scope, limitations, complexity budget, project tension, tool vs impact](lorenzo-agent/operationalized/02-minuses-1-10.md)](#минусы-110-integration-сложность-lifecycle-risk-license-framing-competition-scope-limitations-complexity-budget-project-tension-tool-vs-impactlorenzo-agentoperationalized02-minuses-1-10md)
  - [[Моё честное мнение: что реально и что НЕ реально](lorenzo-agent/operationalized/03-honest-opinion.md)](#моё-честное-мнение-что-реально-и-что-не-реальноlorenzo-agentoperationalized03-honest-opinionmd)
  - [[Рекомендации: принять архитектуру как direction, не immediate plan](lorenzo-agent/operationalized/04-recommendations.md)](#рекомендации-принять-архитектуру-как-direction-не-immediate-planlorenzo-agentoperationalized04-recommendationsmd)
  - [[Anchor-узел: Habr Scout как первый шаг](lorenzo-agent/operationalized/05-anchor-node-habr-scout.md)](#anchor-узел-habr-scout-как-первый-шагlorenzo-agentoperationalized05-anchor-node-habr-scoutmd)
  - [[Вывод: документ deserves serious attention](lorenzo-agent/operationalized/06-conclusion-deserves-attention.md)](#вывод-документ-deserves-serious-attentionlorenzo-agentoperationalized06-conclusion-deserves-attentionmd)
  - [[operationalized](lorenzo-agent/operationalized/README.md)](#operationalizedlorenzo-agentoperationalizedreadmemd)
  - [[Поэтапная структура активностей Lorenzo — обзор](lorenzo-agent/phased-deployment/00-overview.md)](#поэтапная-структура-активностей-lorenzo-обзорlorenzo-agentphased-deployment00-overviewmd)
  - [[Уровень 0 — Ручной режим (текущий)](lorenzo-agent/phased-deployment/01-level-0-manual.md)](#уровень-0-ручной-режим-текущийlorenzo-agentphased-deployment01-level-0-manualmd)
  - [[Уровень 1 — Минимальный (Lorenzo Zero)](lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md)](#уровень-1-минимальный-lorenzo-zerolorenzo-agentphased-deployment02-level-1-minimal-zeromd)
  - [[Уровень 2 — Базовый (Lorenzo Lite)](lorenzo-agent/phased-deployment/03-level-2-basic-lite.md)](#уровень-2-базовый-lorenzo-litelorenzo-agentphased-deployment03-level-2-basic-litemd)
  - [[Уровень 3 — Средний (Lorenzo Active)](lorenzo-agent/phased-deployment/04-level-3-medium-active.md)](#уровень-3-средний-lorenzo-activelorenzo-agentphased-deployment04-level-3-medium-activemd)
  - [[Уровень 4 — Расширенный (Lorenzo Mature)](lorenzo-agent/phased-deployment/05-level-4-extended-mature.md)](#уровень-4-расширенный-lorenzo-maturelorenzo-agentphased-deployment05-level-4-extended-maturemd)
  - [[Уровень 5 — Полный (Lorenzo Network)](lorenzo-agent/phased-deployment/06-level-5-full-network.md)](#уровень-5-полный-lorenzo-networklorenzo-agentphased-deployment06-level-5-full-networkmd)
  - [[Логика прогрессии: conservative escalation](lorenzo-agent/phased-deployment/07-progression-logic.md)](#логика-прогрессии-conservative-escalationlorenzo-agentphased-deployment07-progression-logicmd)
  - [[Что мы можем делать прямо сейчас (Уровень 0 + параллельная подготовка к Уровню 1)](lorenzo-agent/phased-deployment/08-current-session-poc.md)](#что-мы-можем-делать-прямо-сейчас-уровень-0-параллельная-подготовка-к-уровню-1lorenzo-agentphased-deployment08-current-session-pocmd)
  - [[phased-deployment](lorenzo-agent/phased-deployment/README.md)](#phased-deploymentlorenzo-agentphased-deploymentreadmemd)
  - [[Du hast gesagt: А под какой сценарий больше всего подходит такой сценарий что тв…](lorenzo-agent/scenarios/00-question-scenario.md)](#du-hast-gesagt-а-под-какой-сценарий-больше-всего-подходит-такой-сценарий-что-твlorenzo-agentscenarios00-question-scenariomd)
  - [[Claude hat geantwortet: Очень интересный вопрос.](lorenzo-agent/scenarios/01-response.md)](#claude-hat-geantwortet-очень-интересный-вопросlorenzo-agentscenarios01-responsemd)
  - [[scenarios](lorenzo-agent/scenarios/README.md)](#scenarioslorenzo-agentscenariosreadmemd)
  - [[Direction E: Refine Lorenzo — фундаментальные вопросы перед architecture](lorenzo-agent/specification/00-context-fundamental-questions.md)](#direction-e-refine-lorenzo-фундаментальные-вопросы-перед-architecturelorenzo-agentspecification00-context-fundamental-questionsmd)
  - [[Question 1: Что Lorenzo фундаментально такое? (Framings A–D)](lorenzo-agent/specification/01-q1-what-lorenzo-is.md)](#question-1-что-lorenzo-фундаментально-такое-framings-adlorenzo-agentspecification01-q1-what-lorenzo-ismd)
  - [[Question 2: Кому Lorenzo служит? (4 варианта приоритета)](lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md)](#question-2-кому-lorenzo-служит-4-варианта-приоритетаlorenzo-agentspecification02-q2-whom-lorenzo-servesmd)
  - [[Question 3: Что Lorenzo фактически делает?](lorenzo-agent/specification/03-q3-what-lorenzo-does.md)](#question-3-что-lorenzo-фактически-делаетlorenzo-agentspecification03-q3-what-lorenzo-doesmd)
  - [[Question 4: Каков Lorenzo's character?](lorenzo-agent/specification/04-q4-character.md)](#question-4-каков-lorenzos-characterlorenzo-agentspecification04-q4-charactermd)
  - [[Question 5: Каковы limits Lorenzo's authority?](lorenzo-agent/specification/05-q5-authority-limits.md)](#question-5-каковы-limits-lorenzos-authoritylorenzo-agentspecification05-q5-authority-limitsmd)
  - [[Question 6: Как Lorenzo accountable?](lorenzo-agent/specification/06-q6-accountability.md)](#question-6-как-lorenzo-accountablelorenzo-agentspecification06-q6-accountabilitymd)
  - [[Question 7: Каковы success metrics?](lorenzo-agent/specification/07-q7-success-metrics.md)](#question-7-каковы-success-metricslorenzo-agentspecification07-q7-success-metricsmd)
  - [[Question 8: Lorenzo's relationship с другими AI agents](lorenzo-agent/specification/08-q8-other-ai-relationships.md)](#question-8-lorenzos-relationship-с-другими-ai-agentslorenzo-agentspecification08-q8-other-ai-relationshipsmd)
  - [[Question 9: Geographic / linguistic scope](lorenzo-agent/specification/09-q9-geographic-linguistic-scope.md)](#question-9-geographic-linguistic-scopelorenzo-agentspecification09-q9-geographic-linguistic-scopemd)
  - [[Question 10: Funding model (Options A–F + Phase strategy)](lorenzo-agent/specification/10-q10-funding-model.md)](#question-10-funding-model-options-af-phase-strategylorenzo-agentspecification10-q10-funding-modelmd)
  - [[Сложности и рекомендации перед detailed specification](lorenzo-agent/specification/11-difficulties-and-recommendations.md)](#сложности-и-рекомендации-перед-detailed-specificationlorenzo-agentspecification11-difficulties-and-recommendationsmd)
  - [[specification](lorenzo-agent/specification/README.md)](#specificationlorenzo-agentspecificationreadmemd)
- [Meta Scripting](#meta-scripting)
  - [[Метаскриптинг — Часть 1: Концепция](meta-scripting/01-concept.md)](#метаскриптинг-часть-1-концепцияmeta-scripting01-conceptmd)
  - [[Метаскриптинг — Часть 2: Архитектура](meta-scripting/02-architecture.md)](#метаскриптинг-часть-2-архитектураmeta-scripting02-architecturemd)
  - [[Метаскриптинг — Часть 3: Автокаталог скриптов](meta-scripting/03-catalog.md)](#метаскриптинг-часть-3-автокаталог-скриптовmeta-scripting03-catalogmd)
  - [[Метаскриптинг — Часть 4: Обогащение скриптов](meta-scripting/04-enrichment.md)](#метаскриптинг-часть-4-обогащение-скриптовmeta-scripting04-enrichmentmd)
  - [[Метаскриптинг — Часть 5: Синтез новых скриптов](meta-scripting/05-synthesis.md)](#метаскриптинг-часть-5-синтез-новых-скриптовmeta-scripting05-synthesismd)
  - [[Q&A: meta-scripting](meta-scripting/QA.md)](#qa-meta-scriptingmeta-scriptingqamd)
  - [[meta-scripting](meta-scripting/README.md)](#meta-scriptingmeta-scriptingreadmemd)
- [Nautilus](#nautilus)
  - [[nautilus/ — Nautilus Portal Protocol и связанные working papers](nautilus/README.md)](#nautilus-nautilus-portal-protocol-и-связанные-working-papersnautilusreadmemd)
  - [[community-discussions/ — обсуждения и реакции вокруг DHLab серии](nautilus/community-discussions/README.md)](#community-discussions-обсуждения-и-реакции-вокруг-dhlab-серииnautiluscommunity-discussionsreadmemd)
  - [[Du hast gesagt: Такой агент конечно меняет уже собственную реальность человека и…](nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md)](#du-hast-gesagt-такой-агент-конечно-меняет-уже-собственную-реальность-человека-иnautiluscommunity-discussionsagent-changes-reality00-question-agent-changes-realitymd)
  - [[Claude hat geantwortet: Хорошо.](nautilus/community-discussions/agent-changes-reality/01-response-en.md)](#claude-hat-geantwortet-хорошоnautiluscommunity-discussionsagent-changes-reality01-response-enmd)
  - [[agent-changes-reality](nautilus/community-discussions/agent-changes-reality/README.md)](#agent-changes-realitynautiluscommunity-discussionsagent-changes-realityreadmemd)
  - [[Du hast gesagt: https://habr.](nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md)](#du-hast-gesagt-httpshabrnautiluscommunity-discussionshabr-article-1-reaction00-question-habr-linkmd)
  - [[Claude hat geantwortet: Прочитал внимательно.](nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md)](#claude-hat-geantwortet-прочитал-внимательноnautiluscommunity-discussionshabr-article-1-reaction01-claude-responsemd)
  - [[habr-article-1-reaction](nautilus/community-discussions/habr-article-1-reaction/README.md)](#habr-article-1-reactionnautiluscommunity-discussionshabr-article-1-reactionreadmemd)
  - [[Du hast gesagt: https://www.](nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md)](#du-hast-gesagt-httpswwwnautiluscommunity-discussionshabr-article-2-reaction00-question-habr-2md)
  - [[Claude hat geantwortet: Прочитаю статью, чтобы понимать конкретный кейс, на кото…](nautilus/community-discussions/habr-article-2-reaction/01-response.md)](#claude-hat-geantwortet-прочитаю-статью-чтобы-понимать-конкретный-кейс-на-котоnautiluscommunity-discussionshabr-article-2-reaction01-responsemd)
  - [[habr-article-2-reaction](nautilus/community-discussions/habr-article-2-reaction/README.md)](#habr-article-2-reactionnautiluscommunity-discussionshabr-article-2-reactionreadmemd)
  - [[Du hast gesagt: Да это интересная ссылка спасибо всем участникам за творчество и…](nautilus/community-discussions/practical-observations/00-question-practical.md)](#du-hast-gesagt-да-это-интересная-ссылка-спасибо-всем-участникам-за-творчество-иnautiluscommunity-discussionspractical-observations00-question-practicalmd)
  - [[Claude hat geantwortet: Отличное наблюдение.](nautilus/community-discussions/practical-observations/01-response.md)](#claude-hat-geantwortet-отличное-наблюдениеnautiluscommunity-discussionspractical-observations01-responsemd)
  - [[practical-observations](nautilus/community-discussions/practical-observations/README.md)](#practical-observationsnautiluscommunity-discussionspractical-observationsreadmemd)
  - [[Du hast gesagt: Самый интересный вопрос — могут ли быть voiceless контрибьюторы](nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md)](#du-hast-gesagt-самый-интересный-вопрос-могут-ли-быть-voiceless-контрибьюторыnautiluscommunity-discussionsvoiceless-contributors00-question-voicelessmd)
  - [[Claude hat geantwortet: Это сильное продолжение мысли, и оно заслуживает серьёзн…](nautilus/community-discussions/voiceless-contributors/01-response.md)](#claude-hat-geantwortet-это-сильное-продолжение-мысли-и-оно-заслуживает-серьёзнnautiluscommunity-discussionsvoiceless-contributors01-responsemd)
  - [[voiceless-contributors](nautilus/community-discussions/voiceless-contributors/README.md)](#voiceless-contributorsnautiluscommunity-discussionsvoiceless-contributorsreadmemd)
  - [[1. Why the Binary View Is Incomplete](nautilus/composite-skills-agents/01-why-binary-incomplete.md)](#1-why-the-binary-view-is-incompletenautiluscomposite-skills-agents01-why-binary-incompletemd)
  - [[2. The Twenty-One Teachers Pattern](nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md)](#2-the-twenty-one-teachers-patternnautiluscomposite-skills-agents02-twenty-one-teachers-patternmd)
  - [[3. What Makes a Composite Skills Agent](nautilus/composite-skills-agents/03-what-makes-csa.md)](#3-what-makes-a-composite-skills-agentnautiluscomposite-skills-agents03-what-makes-csamd)
  - [[4. The Sub-Agent Registry](nautilus/composite-skills-agents/04-sub-agent-registry.md)](#4-the-sub-agent-registrynautiluscomposite-skills-agents04-sub-agent-registrymd)
  - [[5. Configuration: How Principals Build Their Ensembles](nautilus/composite-skills-agents/05-configuration-ensembles.md)](#5-configuration-how-principals-build-their-ensemblesnautiluscomposite-skills-agents05-configuration-ensemblesmd)
  - [[6. Coordination and Disagreement Resolution](nautilus/composite-skills-agents/06-coordination-disagreement.md)](#6-coordination-and-disagreement-resolutionnautiluscomposite-skills-agents06-coordination-disagreementmd)
  - [[7. Economics of Combinatorial Replication](nautilus/composite-skills-agents/07-economics-combinatorial.md)](#7-economics-of-combinatorial-replicationnautiluscomposite-skills-agents07-economics-combinatorialmd)
  - [[8. Seven Domains of Application](nautilus/composite-skills-agents/08-seven-domains.md)](#8-seven-domains-of-applicationnautiluscomposite-skills-agents08-seven-domainsmd)
  - [[9. Integration with OKWF Infrastructure](nautilus/composite-skills-agents/09-okwf-integration.md)](#9-integration-with-okwf-infrastructurenautiluscomposite-skills-agents09-okwf-integrationmd)
  - [[10. Risks Specific to Composite Architectures](nautilus/composite-skills-agents/10-risks.md)](#10-risks-specific-to-composite-architecturesnautiluscomposite-skills-agents10-risksmd)
  - [[11. Open Questions](nautilus/composite-skills-agents/11-open-questions.md)](#11-open-questionsnautiluscomposite-skills-agents11-open-questionsmd)
  - [[12. Call for Collaboration](nautilus/composite-skills-agents/12-call-for-collaboration.md)](#12-call-for-collaborationnautiluscomposite-skills-agents12-call-for-collaborationmd)
  - [[13. Closing](nautilus/composite-skills-agents/13-closing.md)](#13-closingnautiluscomposite-skills-agents13-closingmd)
  - [[composite-skills-agents](nautilus/composite-skills-agents/README.md)](#composite-skills-agentsnautiluscomposite-skills-agentsreadmemd)
  - [[Du hast gesagt: Важный момент про способности про скилы как один человек професс…](nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md)](#du-hast-gesagt-важный-момент-про-способности-про-скилы-как-один-человек-профессnautiluscomposite-skills-agents-companion-mentors00-question-multiple-mentorsmd)
  - [[Claude hat geantwortet: Это очень тонкое и важное наблюдение.](nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md)](#claude-hat-geantwortet-это-очень-тонкое-и-важное-наблюдениеnautiluscomposite-skills-agents-companion-mentors01-yogi-metaphormd)
  - [[Это не Тип 1 — потому что профиль не общий для всей профессии. И это не Тип 4 — …](nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md)](#это-не-тип-1-потому-что-профиль-не-общий-для-всей-профессии-и-это-не-тип-4-nautiluscomposite-skills-agents-companion-mentors02-what-was-missing-in-paper-6md)
  - [[Какой под-агент (или какие) должны её обработать](nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md)](#какой-под-агент-или-какие-должны-её-обработатьnautiluscomposite-skills-agents-companion-mentors03-the-spectrummd)
  - [[composite-skills-agents-companion-mentors](nautilus/composite-skills-agents-companion-mentors/README.md)](#composite-skills-agents-companion-mentorsnautiluscomposite-skills-agents-companion-mentorsreadmemd)
  - [[Abstract — The Double-Triangle Architecture](nautilus/double-triangle-architecture/00-abstract.md)](#abstract-the-double-triangle-architecturenautilusdouble-triangle-architecture00-abstractmd)
  - [[1. Why Single-Triangle Models Are Incomplete](nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md)](#1-why-single-triangle-models-are-incompletenautilusdouble-triangle-architecture01-why-single-triangle-incompletemd)
  - [[2. The Double-Triangle Architecture](nautilus/double-triangle-architecture/02-double-triangle-architecture.md)](#2-the-double-triangle-architecturenautilusdouble-triangle-architecture02-double-triangle-architecturemd)
  - [[3. Three Inter-Layer Protocols](nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md)](#3-three-inter-layer-protocolsnautilusdouble-triangle-architecture03-three-inter-layer-protocolsmd)
  - [[4. Nautilus Portal as Reference Substrate](nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md)](#4-nautilus-portal-as-reference-substratenautilusdouble-triangle-architecture04-nautilus-portal-substratemd)
  - [[5. Pattern Library as Bridge Between Triangles](nautilus/double-triangle-architecture/05-pattern-library-bridge.md)](#5-pattern-library-as-bridge-between-trianglesnautilusdouble-triangle-architecture05-pattern-library-bridgemd)
  - [[6. Four Deployment Domains](nautilus/double-triangle-architecture/06-four-deployment-domains.md)](#6-four-deployment-domainsnautilusdouble-triangle-architecture06-four-deployment-domainsmd)
  - [[7. Open Questions](nautilus/double-triangle-architecture/07-open-questions.md)](#7-open-questionsnautilusdouble-triangle-architecture07-open-questionsmd)
  - [[8. Call to Action](nautilus/double-triangle-architecture/08-call-to-action.md)](#8-call-to-actionnautilusdouble-triangle-architecture08-call-to-actionmd)
  - [[Acknowledgments](nautilus/double-triangle-architecture/09-acknowledgments.md)](#acknowledgmentsnautilusdouble-triangle-architecture09-acknowledgmentsmd)
  - [[References](nautilus/double-triangle-architecture/10-references.md)](#referencesnautilusdouble-triangle-architecture10-referencesmd)
  - [[Appendix A: Glossary](nautilus/double-triangle-architecture/11-glossary.md)](#appendix-a-glossarynautilusdouble-triangle-architecture11-glossarymd)
  - [[double-triangle-architecture](nautilus/double-triangle-architecture/README.md)](#double-triangle-architecturenautilusdouble-triangle-architecturereadmemd)
  - [[The Missing Middle Layer Between Chat and Code](nautilus/infrastructure-layer-b-en/00-intro.md)](#the-missing-middle-layer-between-chat-and-codenautilusinfrastructure-layer-b-en00-intromd)
  - [[Why This Document Exists](nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md)](#why-this-document-existsnautilusinfrastructure-layer-b-en01-missing-middle-layermd)
  - [[Why This Document Exists](nautilus/infrastructure-layer-b-en/02-why-document-exists.md)](#why-this-document-existsnautilusinfrastructure-layer-b-en02-why-document-existsmd)
  - [[The Two-Layer Stack As It Exists](nautilus/infrastructure-layer-b-en/03-two-layer-stack.md)](#the-two-layer-stack-as-it-existsnautilusinfrastructure-layer-b-en03-two-layer-stackmd)
  - [[What's Missing — Layer B](nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md)](#whats-missing-layer-bnautilusinfrastructure-layer-b-en04-whats-missing-layer-bmd)
  - [[Why This Hasn't Been Built](nautilus/infrastructure-layer-b-en/05-why-not-built.md)](#why-this-hasnt-been-builtnautilusinfrastructure-layer-b-en05-why-not-builtmd)
  - [[Existing Approximations](nautilus/infrastructure-layer-b-en/06-existing-approximations.md)](#existing-approximationsnautilusinfrastructure-layer-b-en06-existing-approximationsmd)
  - [[The Specific Case in Front of Us](nautilus/infrastructure-layer-b-en/07-specific-case.md)](#the-specific-case-in-front-of-usnautilusinfrastructure-layer-b-en07-specific-casemd)
  - [[The Recursive Insight](nautilus/infrastructure-layer-b-en/08-recursive-insight.md)](#the-recursive-insightnautilusinfrastructure-layer-b-en08-recursive-insightmd)
  - [[What Industry Will Likely Build](nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md)](#what-industry-will-likely-buildnautilusinfrastructure-layer-b-en09-what-industry-will-buildmd)
  - [[What This Document Doesn't Solve](nautilus/infrastructure-layer-b-en/10-what-not-solved.md)](#what-this-document-doesnt-solvenautilusinfrastructure-layer-b-en10-what-not-solvedmd)
  - [[Practical Recommendations for the Current Project](nautilus/infrastructure-layer-b-en/11-practical-recommendations.md)](#practical-recommendations-for-the-current-projectnautilusinfrastructure-layer-b-en11-practical-recommendationsmd)
  - [[Closing](nautilus/infrastructure-layer-b-en/12-closing.md)](#closingnautilusinfrastructure-layer-b-en12-closingmd)
  - [[Acknowledgments](nautilus/infrastructure-layer-b-en/13-acknowledgments-refs.md)](#acknowledgmentsnautilusinfrastructure-layer-b-en13-acknowledgments-refsmd)
  - [[infrastructure-layer-b-en](nautilus/infrastructure-layer-b-en/README.md)](#infrastructure-layer-b-ennautilusinfrastructure-layer-b-enreadmemd)
  - [[00 Intro](nautilus/infrastructure-layer-b-ru/00-intro.md)](#00-intronautilusinfrastructure-layer-b-ru00-intromd)
  - [[Почему этот документ существует](nautilus/infrastructure-layer-b-ru/01-zachem-dokument.md)](#почему-этот-документ-существуетnautilusinfrastructure-layer-b-ru01-zachem-dokumentmd)
  - [[Двухслойный стек, как он существует](nautilus/infrastructure-layer-b-ru/02-dvukhsloynyy-stek.md)](#двухслойный-стек-как-он-существуетnautilusinfrastructure-layer-b-ru02-dvukhsloynyy-stekmd)
  - [[Что отсутствует — Слой B](nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md)](#что-отсутствует-слой-bnautilusinfrastructure-layer-b-ru03-otsutstvuet-sloy-bmd)
  - [[Почему это не было построено](nautilus/infrastructure-layer-b-ru/04-pochemu-ne-postroeno.md)](#почему-это-не-было-построеноnautilusinfrastructure-layer-b-ru04-pochemu-ne-postroenomd)
  - [[Существующие приближения](nautilus/infrastructure-layer-b-ru/05-priblizheniya.md)](#существующие-приближенияnautilusinfrastructure-layer-b-ru05-priblizheniyamd)
  - [[Конкретный случай перед нами](nautilus/infrastructure-layer-b-ru/06-konkretnyy-sluchay.md)](#конкретный-случай-перед-намиnautilusinfrastructure-layer-b-ru06-konkretnyy-sluchaymd)
  - [[Рекурсивное прозрение](nautilus/infrastructure-layer-b-ru/07-rekursivnoe-prozrenie.md)](#рекурсивное-прозрениеnautilusinfrastructure-layer-b-ru07-rekursivnoe-prozreniemd)
  - [[Что промышленность вероятно построит](nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md)](#что-промышленность-вероятно-построитnautilusinfrastructure-layer-b-ru08-promyshlennost-postroitmd)
  - [[Что этот документ не решает](nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md)](#что-этот-документ-не-решаетnautilusinfrastructure-layer-b-ru09-ne-reshaetmd)
  - [[Практические рекомендации для текущего проекта](nautilus/infrastructure-layer-b-ru/10-rekomendatsii.md)](#практические-рекомендации-для-текущего-проектаnautilusinfrastructure-layer-b-ru10-rekomendatsiimd)
  - [[Заключение](nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md)](#заключениеnautilusinfrastructure-layer-b-ru11-zaklyucheniemd)
  - [[Благодарности](nautilus/infrastructure-layer-b-ru/12-blagodarnosti-ssylki.md)](#благодарностиnautilusinfrastructure-layer-b-ru12-blagodarnosti-ssylkimd)
  - [[infrastructure-layer-b-ru](nautilus/infrastructure-layer-b-ru/README.md)](#infrastructure-layer-b-runautilusinfrastructure-layer-b-rureadmemd)
  - [[1. The Cowork Discovery and Why It Changes Everything](nautilus/ingit-cowork-en/01-cowork-discovery.md)](#1-the-cowork-discovery-and-why-it-changes-everythingnautilusingit-cowork-en01-cowork-discoverymd)
  - [[2. What Cowork Provides That InGit Doesn't Need to Build](nautilus/ingit-cowork-en/02-cowork-provides.md)](#2-what-cowork-provides-that-ingit-doesnt-need-to-buildnautilusingit-cowork-en02-cowork-providesmd)
  - [[3. What InGit Provides That Cowork Lacks](nautilus/ingit-cowork-en/03-ingit-provides.md)](#3-what-ingit-provides-that-cowork-lacksnautilusingit-cowork-en03-ingit-providesmd)
  - [[4. The Symbiotic Architecture](nautilus/ingit-cowork-en/04-symbiotic-architecture.md)](#4-the-symbiotic-architecturenautilusingit-cowork-en04-symbiotic-architecturemd)
  - [[5. Four Integration Paths in Order of Accessibility](nautilus/ingit-cowork-en/05-four-integration-paths.md)](#5-four-integration-paths-in-order-of-accessibilitynautilusingit-cowork-en05-four-integration-pathsmd)
  - [[6. Refined InGit Scope with Cowork in Mind](nautilus/ingit-cowork-en/06-refined-ingit-scope.md)](#6-refined-ingit-scope-with-cowork-in-mindnautilusingit-cowork-en06-refined-ingit-scopemd)
  - [[7. Practical First Steps This Month](nautilus/ingit-cowork-en/07-practical-first-steps.md)](#7-practical-first-steps-this-monthnautilusingit-cowork-en07-practical-first-stepsmd)
  - [[8. Implications for Nautilus and OKWF](nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md)](#8-implications-for-nautilus-and-okwfnautilusingit-cowork-en08-implications-nautilus-okwfmd)
  - [[9. Risks and Open Questions](nautilus/ingit-cowork-en/09-risks-open-questions.md)](#9-risks-and-open-questionsnautilusingit-cowork-en09-risks-open-questionsmd)
  - [[10. Strategic Positioning](nautilus/ingit-cowork-en/10-strategic-positioning.md)](#10-strategic-positioningnautilusingit-cowork-en10-strategic-positioningmd)
  - [[ingit-cowork-en](nautilus/ingit-cowork-en/README.md)](#ingit-cowork-ennautilusingit-cowork-enreadmemd)
  - [[1. Открытие Cowork и почему это меняет всё](nautilus/ingit-cowork-ru/01-otkrytie-cowork.md)](#1-открытие-cowork-и-почему-это-меняет-всёnautilusingit-cowork-ru01-otkrytie-coworkmd)
  - [[2. Что Cowork обеспечивает, что InGit не нужно строить](nautilus/ingit-cowork-ru/02-chto-cowork-obespechivaet.md)](#2-что-cowork-обеспечивает-что-ingit-не-нужно-строитьnautilusingit-cowork-ru02-chto-cowork-obespechivaetmd)
  - [[3. Что InGit обеспечивает, чего Cowork не хватает](nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md)](#3-что-ingit-обеспечивает-чего-cowork-не-хватаетnautilusingit-cowork-ru03-chto-ingit-obespechivaetmd)
  - [[4. Симбиотическая Архитектура](nautilus/ingit-cowork-ru/04-simbioticheskaya-arkhitektura.md)](#4-симбиотическая-архитектураnautilusingit-cowork-ru04-simbioticheskaya-arkhitekturamd)
  - [[5. Четыре пути интеграции в порядке доступности](nautilus/ingit-cowork-ru/05-chetyre-puti-integratsii.md)](#5-четыре-пути-интеграции-в-порядке-доступностиnautilusingit-cowork-ru05-chetyre-puti-integratsiimd)
  - [[6. Уточнённый объём InGit с учётом Cowork](nautilus/ingit-cowork-ru/06-utochnyonnyy-obyom-ingit.md)](#6-уточнённый-объём-ingit-с-учётом-coworknautilusingit-cowork-ru06-utochnyonnyy-obyom-ingitmd)
  - [[7. Практические первые шаги в этом месяце](nautilus/ingit-cowork-ru/07-prakticheskie-shagi.md)](#7-практические-первые-шаги-в-этом-месяцеnautilusingit-cowork-ru07-prakticheskie-shagimd)
  - [[8. Импликации для Nautilus и OKWF](nautilus/ingit-cowork-ru/08-implikatsii-nautilus-okwf.md)](#8-импликации-для-nautilus-и-okwfnautilusingit-cowork-ru08-implikatsii-nautilus-okwfmd)
  - [[9. Риски и Открытые Вопросы](nautilus/ingit-cowork-ru/09-riski-voprosy.md)](#9-риски-и-открытые-вопросыnautilusingit-cowork-ru09-riski-voprosymd)
  - [[10. Стратегическое Позиционирование](nautilus/ingit-cowork-ru/10-strategicheskoe-pozitsionirovanie.md)](#10-стратегическое-позиционированиеnautilusingit-cowork-ru10-strategicheskoe-pozitsionirovaniemd)
  - [[ingit-cowork-ru](nautilus/ingit-cowork-ru/README.md)](#ingit-cowork-runautilusingit-cowork-rureadmemd)
  - [[Du hast gesagt: Интересно как новая как инновация как как рационализация как пер…](nautilus/innovation-transitions/00-question-innovations-transitions.md)](#du-hast-gesagt-интересно-как-новая-как-инновация-как-как-рационализация-как-перnautilusinnovation-transitions00-question-innovations-transitionsmd)
  - [[Claude hat geantwortet: Отличный запрос.](nautilus/innovation-transitions/01-response.md)](#claude-hat-geantwortet-отличный-запросnautilusinnovation-transitions01-responsemd)
  - [[innovation-transitions](nautilus/innovation-transitions/README.md)](#innovation-transitionsnautilusinnovation-transitionsreadmemd)
  - [[Du hast gesagt: Ещё есть такие вопросы то есть если общие юридические Наутилус м…](nautilus/multi-tier-architecture/00-question-multi-tier.md)](#du-hast-gesagt-ещё-есть-такие-вопросы-то-есть-если-общие-юридические-наутилус-мnautilusmulti-tier-architecture00-question-multi-tiermd)
  - [[Claude hat geantwortet: Это стратегически значимый вопрос, и ответ на него — да,…](nautilus/multi-tier-architecture/01-strategic-significance.md)](#claude-hat-geantwortet-это-стратегически-значимый-вопрос-и-ответ-на-него-даnautilusmulti-tier-architecture01-strategic-significancemd)
  - [[multi-tier-architecture](nautilus/multi-tier-architecture/README.md)](#multi-tier-architecturenautilusmulti-tier-architecturereadmemd)
  - [[Du hast gesagt: Вопрос такой вопрос и такие а можно ли этот протокол это система…](nautilus/npp-humanitarian-extension/00-question-can-it-apply-to-docs.md)](#du-hast-gesagt-вопрос-такой-вопрос-и-такие-а-можно-ли-этот-протокол-это-системаnautilusnpp-humanitarian-extension00-question-can-it-apply-to-docsmd)
  - [[Структурное сравнение: код vs гуманитарные документы](nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md)](#структурное-сравнение-код-vs-гуманитарные-документыnautilusnpp-humanitarian-extension01-structural-comparison-code-vs-docsmd)
  - [[Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы …](nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md)](#что-он-даёт-вам-на-практике-через-mcp-claude-desktop-может-ответить-на-запросы-nautilusnpp-humanitarian-extension02-mcp-claude-desktop-use-casesmd)
  - [[Что не существует на рынке:](nautilus/npp-humanitarian-extension/03-what-doesnt-exist-on-market.md)](#что-не-существует-на-рынкеnautilusnpp-humanitarian-extension03-what-doesnt-exist-on-marketmd)
  - [[Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access t…](nautilus/npp-humanitarian-extension/04-grant-opportunities.md)](#horizon-europe-cluster-3-civil-security-for-society-пересекается-с-access-tnautilusnpp-humanitarian-extension04-grant-opportunitiesmd)
  - [[Что из этого сейчас кажется более ценным? Или какая-то своя комбинация?](nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md)](#что-из-этого-сейчас-кажется-более-ценным-или-какая-то-своя-комбинацияnautilusnpp-humanitarian-extension05-which-combination-more-valuablemd)
  - [[npp-humanitarian-extension](nautilus/npp-humanitarian-extension/README.md)](#npp-humanitarian-extensionnautilusnpp-humanitarian-extensionreadmemd)
  - [[Abstract + Status of This Document](nautilus/npp-v1-0/00-abstract-status.md)](#abstract-status-of-this-documentnautilusnpp-v1-000-abstract-statusmd)
  - [[1. Introduction (Motivation, Design Goals, Non-Goals, Terminology)](nautilus/npp-v1-0/01-introduction.md)](#1-introduction-motivation-design-goals-non-goals-terminologynautilusnpp-v1-001-introductionmd)
  - [[2. Terminology](nautilus/npp-v1-0/02-terminology.md)](#2-terminologynautilusnpp-v1-002-terminologymd)
  - [[3. Registry (nautilus.json)](nautilus/npp-v1-0/03-registry.md)](#3-registry-nautilusjsonnautilusnpp-v1-003-registrymd)
  - [[4. Passport (passport.md)](nautilus/npp-v1-0/04-passport.md)](#4-passport-passportmdnautilusnpp-v1-004-passportmd)
  - [[5. Compatibility Levels](nautilus/npp-v1-0/05-compatibility-levels.md)](#5-compatibility-levelsnautilusnpp-v1-005-compatibility-levelsmd)
  - [[6. Adapter Interface](nautilus/npp-v1-0/06-adapter-interface.md)](#6-adapter-interfacenautilusnpp-v1-006-adapter-interfacemd)
  - [[7. PortalEntry Structure](nautilus/npp-v1-0/07-portal-entry.md)](#7-portalentry-structurenautilusnpp-v1-007-portal-entrymd)
  - [[8. Consensus Algorithm (v1.0: string normalization)](nautilus/npp-v1-0/08-consensus-algorithm.md)](#8-consensus-algorithm-v10-string-normalizationnautilusnpp-v1-008-consensus-algorithmmd)
  - [[9. Query Flow](nautilus/npp-v1-0/09-query-flow.md)](#9-query-flownautilusnpp-v1-009-query-flowmd)
  - [[10. QueryResult Structure](nautilus/npp-v1-0/10-query-result.md)](#10-queryresult-structurenautilusnpp-v1-010-query-resultmd)
  - [[11. Security Considerations](nautilus/npp-v1-0/11-security-considerations.md)](#11-security-considerationsnautilusnpp-v1-011-security-considerationsmd)
  - [[12. Versioning Policy](nautilus/npp-v1-0/12-versioning-policy.md)](#12-versioning-policynautilusnpp-v1-012-versioning-policymd)
  - [[13. Reference Implementation](nautilus/npp-v1-0/13-reference-implementation.md)](#13-reference-implementationnautilusnpp-v1-013-reference-implementationmd)
  - [[14. ADR-001: Federation over Merging](nautilus/npp-v1-0/14-adr-001-federation-over-merging.md)](#14-adr-001-federation-over-mergingnautilusnpp-v1-014-adr-001-federation-over-mergingmd)
  - [[15. Glossary of Examples](nautilus/npp-v1-0/15-glossary.md)](#15-glossary-of-examplesnautilusnpp-v1-015-glossarymd)
  - [[Appendix A: Minimal Working Example](nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md)](#appendix-a-minimal-working-examplenautilusnpp-v1-016-appendix-a-minimal-working-examplemd)
  - [[Appendix B: Change Log](nautilus/npp-v1-0/17-appendix-b-change-log.md)](#appendix-b-change-lognautilusnpp-v1-017-appendix-b-change-logmd)
  - [[Комментарий: дизайн-решения NPP v1.0](nautilus/npp-v1-0/18-comment-on-document.md)](#комментарий-дизайн-решения-npp-v10nautilusnpp-v1-018-comment-on-documentmd)
  - [[npp-v1-0](nautilus/npp-v1-0/README.md)](#npp-v1-0nautilusnpp-v1-0readmemd)
  - [[Abstract + Status of This Document](nautilus/npp-v1-1/00-abstract-status.md)](#abstract-status-of-this-documentnautilusnpp-v1-100-abstract-statusmd)
  - [[1. Introduction (Motivation, Design Goals, Non-Goals, Terminology, Changes from v1.0)](nautilus/npp-v1-1/01-introduction.md)](#1-introduction-motivation-design-goals-non-goals-terminology-changes-from-v10nautilusnpp-v1-101-introductionmd)
  - [[2. Terminology](nautilus/npp-v1-1/02-terminology.md)](#2-terminologynautilusnpp-v1-102-terminologymd)
  - [[3. Registry (nautilus.json)](nautilus/npp-v1-1/03-registry.md)](#3-registry-nautilusjsonnautilusnpp-v1-103-registrymd)
  - [[4. Passport (passport.md)](nautilus/npp-v1-1/04-passport.md)](#4-passport-passportmdnautilusnpp-v1-104-passportmd)
  - [[5. Compatibility Levels](nautilus/npp-v1-1/05-compatibility-levels.md)](#5-compatibility-levelsnautilusnpp-v1-105-compatibility-levelsmd)
  - [[6. Adapter Interface](nautilus/npp-v1-1/06-adapter-interface.md)](#6-adapter-interfacenautilusnpp-v1-106-adapter-interfacemd)
  - [[7. PortalEntry Structure](nautilus/npp-v1-1/07-portal-entry.md)](#7-portalentry-structurenautilusnpp-v1-107-portal-entrymd)
  - [[8. Q6 Space (Normative)](nautilus/npp-v1-1/08-q6-space.md)](#8-q6-space-normativenautilusnpp-v1-108-q6-spacemd)
  - [[9. Consensus Algorithm](nautilus/npp-v1-1/09-consensus-algorithm.md)](#9-consensus-algorithmnautilusnpp-v1-109-consensus-algorithmmd)
  - [[10. Query Flow](nautilus/npp-v1-1/10-query-flow.md)](#10-query-flownautilusnpp-v1-110-query-flowmd)
  - [[11. Relevance Ranking](nautilus/npp-v1-1/11-relevance-ranking.md)](#11-relevance-rankingnautilusnpp-v1-111-relevance-rankingmd)
  - [[12. Onboarding Paths (Normative)](nautilus/npp-v1-1/12-onboarding-paths.md)](#12-onboarding-paths-normativenautilusnpp-v1-112-onboarding-pathsmd)
  - [[13. REST API Contract (Normative for Portals)](nautilus/npp-v1-1/13-rest-api.md)](#13-rest-api-contract-normative-for-portalsnautilusnpp-v1-113-rest-apimd)
  - [[14. SDK Contract (Informative)](nautilus/npp-v1-1/14-sdk.md)](#14-sdk-contract-informativenautilusnpp-v1-114-sdkmd)
  - [[15. Security Considerations](nautilus/npp-v1-1/15-security.md)](#15-security-considerationsnautilusnpp-v1-115-securitymd)
  - [[16. MCP Extension (Informative)](nautilus/npp-v1-1/16-mcp-extension.md)](#16-mcp-extension-informativenautilusnpp-v1-116-mcp-extensionmd)
  - [[17. Versioning Policy](nautilus/npp-v1-1/17-versioning-policy.md)](#17-versioning-policynautilusnpp-v1-117-versioning-policymd)
  - [[18. Reference Implementation](nautilus/npp-v1-1/18-reference-implementation.md)](#18-reference-implementationnautilusnpp-v1-118-reference-implementationmd)
  - [[19. ADR-001: Federation over Merging](nautilus/npp-v1-1/19-adr-001-federation-over-merging.md)](#19-adr-001-federation-over-mergingnautilusnpp-v1-119-adr-001-federation-over-mergingmd)
  - [[20. ADR-002: Q6 as First-Class Protocol Concept](nautilus/npp-v1-1/20-adr-002-q6-first-class.md)](#20-adr-002-q6-as-first-class-protocol-conceptnautilusnpp-v1-120-adr-002-q6-first-classmd)
  - [[21. ADR-003: Five Onboarding Paths as Equal-Rank](nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md)](#21-adr-003-five-onboarding-paths-as-equal-ranknautilusnpp-v1-121-adr-003-five-onboarding-pathsmd)
  - [[22. Glossary of Reference Examples](nautilus/npp-v1-1/22-glossary.md)](#22-glossary-of-reference-examplesnautilusnpp-v1-122-glossarymd)
  - [[npp-v1-1](nautilus/npp-v1-1/README.md)](#npp-v1-1nautilusnpp-v1-1readmemd)
  - [[AI-Coordinated Infrastructure for Distributed Expert Contribution](nautilus/okwf-concept/00-abstract.md)](#ai-coordinated-infrastructure-for-distributed-expert-contributionnautilusokwf-concept00-abstractmd)
  - [[1. Problem Statement](nautilus/okwf-concept/01-problem-statement.md)](#1-problem-statementnautilusokwf-concept01-problem-statementmd)
  - [[2. Target Populations](nautilus/okwf-concept/02-target-populations.md)](#2-target-populationsnautilusokwf-concept02-target-populationsmd)
  - [[3. Why Existing Solutions Fail](nautilus/okwf-concept/03-why-existing-fail.md)](#3-why-existing-solutions-failnautilusokwf-concept03-why-existing-failmd)
  - [[4. Proposed Infrastructure](nautilus/okwf-concept/04-proposed-infrastructure.md)](#4-proposed-infrastructurenautilusokwf-concept04-proposed-infrastructuremd)
  - [[5. Economic Model](nautilus/okwf-concept/05-economic-model.md)](#5-economic-modelnautilusokwf-concept05-economic-modelmd)
  - [[6. Governance and Ethics](nautilus/okwf-concept/06-governance-ethics.md)](#6-governance-and-ethicsnautilusokwf-concept06-governance-ethicsmd)
  - [[7. Phased Rollout Plan](nautilus/okwf-concept/07-phased-rollout.md)](#7-phased-rollout-plannautilusokwf-concept07-phased-rolloutmd)
  - [[8. Risk Analysis](nautilus/okwf-concept/08-risk-analysis.md)](#8-risk-analysisnautilusokwf-concept08-risk-analysismd)
  - [[9. Call for Partnership](nautilus/okwf-concept/09-call-for-partnership.md)](#9-call-for-partnershipnautilusokwf-concept09-call-for-partnershipmd)
  - [[10. Appendices](nautilus/okwf-concept/10-appendices.md)](#10-appendicesnautilusokwf-concept10-appendicesmd)
  - [[okwf-concept](nautilus/okwf-concept/README.md)](#okwf-conceptnautilusokwf-conceptreadmemd)
  - [[Du hast gesagt: Насчёт приватности Я думаю что возможно удалять только личные да…](nautilus/privacy-federation/00-question-anonymization.md)](#du-hast-gesagt-насчёт-приватности-я-думаю-что-возможно-удалять-только-личные-даnautilusprivacy-federation00-question-anonymizationmd)
  - [[Что именно анонимизировать: немецкий стандарт](nautilus/privacy-federation/01-what-to-anonymize-german-standard.md)](#что-именно-анонимизировать-немецкий-стандартnautilusprivacy-federation01-what-to-anonymize-german-standardmd)
  - [[Архитектурное решение: две-уровневая публикация](nautilus/privacy-federation/02-two-tier-publication.md)](#архитектурное-решение-две-уровневая-публикацияnautilusprivacy-federation02-two-tier-publicationmd)
  - [[Что это даёт технически](nautilus/privacy-federation/03-what-this-gives-technically.md)](#что-это-даёт-техническиnautilusprivacy-federation03-what-this-gives-technicallymd)
  - [[Что я могу сделать сейчас](nautilus/privacy-federation/04-what-i-can-do-now.md)](#что-я-могу-сделать-сейчасnautilusprivacy-federation04-what-i-can-do-nowmd)
  - [[privacy-federation](nautilus/privacy-federation/README.md)](#privacy-federationnautilusprivacy-federationreadmemd)
  - [[Professional Colleague Agents](nautilus/professional-colleague-agents-en/00-abstract.md)](#professional-colleague-agentsnautilusprofessional-colleague-agents-en00-abstractmd)
  - [[1. The Five-Type Typology of Principal-Side Agents](nautilus/professional-colleague-agents-en/01-five-type-typology.md)](#1-the-five-type-typology-of-principal-side-agentsnautilusprofessional-colleague-agents-en01-five-type-typologymd)
  - [[2. What Makes a Professional Colleague Agent](nautilus/professional-colleague-agents-en/02-what-makes-pca.md)](#2-what-makes-a-professional-colleague-agentnautilusprofessional-colleague-agents-en02-what-makes-pcamd)
  - [[3. Empirical Case Study: «Обучай»](nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md)](#3-empirical-case-study-обучайnautilusprofessional-colleague-agents-en03-empirical-case-obuchaymd)
  - [[4. Architecture of Professional Colleague Agents](nautilus/professional-colleague-agents-en/04-architecture.md)](#4-architecture-of-professional-colleague-agentsnautilusprofessional-colleague-agents-en04-architecturemd)
  - [[5. The Economics of Profession-Wide Replication](nautilus/professional-colleague-agents-en/05-economics-replication.md)](#5-the-economics-of-profession-wide-replicationnautilusprofessional-colleague-agents-en05-economics-replicationmd)
  - [[6. Risks Specific to this Category](nautilus/professional-colleague-agents-en/06-risks.md)](#6-risks-specific-to-this-categorynautilusprofessional-colleague-agents-en06-risksmd)
  - [[7. Application Domains](nautilus/professional-colleague-agents-en/07-application-domains.md)](#7-application-domainsnautilusprofessional-colleague-agents-en07-application-domainsmd)
  - [[8. Pilot Proposal: SGB Advocate Colleague](nautilus/professional-colleague-agents-en/08-pilot-sgb-advocate.md)](#8-pilot-proposal-sgb-advocate-colleaguenautilusprofessional-colleague-agents-en08-pilot-sgb-advocatemd)
  - [[9. Relationship to Other Agent Types](nautilus/professional-colleague-agents-en/09-relationship-other-agents.md)](#9-relationship-to-other-agent-typesnautilusprofessional-colleague-agents-en09-relationship-other-agentsmd)
  - [[10. Open Questions](nautilus/professional-colleague-agents-en/10-open-questions.md)](#10-open-questionsnautilusprofessional-colleague-agents-en10-open-questionsmd)
  - [[11. Call for Collaboration](nautilus/professional-colleague-agents-en/11-call-for-collaboration.md)](#11-call-for-collaborationnautilusprofessional-colleague-agents-en11-call-for-collaborationmd)
  - [[12. Closing](nautilus/professional-colleague-agents-en/12-closing.md)](#12-closingnautilusprofessional-colleague-agents-en12-closingmd)
  - [[professional-colleague-agents-en](nautilus/professional-colleague-agents-en/README.md)](#professional-colleague-agents-ennautilusprofessional-colleague-agents-enreadmemd)
  - [[Содержание](nautilus/professional-colleague-agents-ru/00-abstract.md)](#содержаниеnautilusprofessional-colleague-agents-ru00-abstractmd)
  - [[1. Типология из пяти типов агентов на стороне принципала](nautilus/professional-colleague-agents-ru/01-pyat-tipov.md)](#1-типология-из-пяти-типов-агентов-на-стороне-принципалаnautilusprofessional-colleague-agents-ru01-pyat-tipovmd)
  - [[2. Что делает агента Профессиональным Коллегой](nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md)](#2-что-делает-агента-профессиональным-коллегойnautilusprofessional-colleague-agents-ru02-chto-delaet-pkamd)
  - [[3. Эмпирический кейс: «Обучай»](nautilus/professional-colleague-agents-ru/03-keys-obuchay.md)](#3-эмпирический-кейс-обучайnautilusprofessional-colleague-agents-ru03-keys-obuchaymd)
  - [[4. Архитектура Профессиональных Коллег-Агентов](nautilus/professional-colleague-agents-ru/04-arkhitektura.md)](#4-архитектура-профессиональных-коллег-агентовnautilusprofessional-colleague-agents-ru04-arkhitekturamd)
  - [[5. Экономика тиражирования по профессии](nautilus/professional-colleague-agents-ru/05-ekonomika.md)](#5-экономика-тиражирования-по-профессииnautilusprofessional-colleague-agents-ru05-ekonomikamd)
  - [[6. Риски, специфичные для этой категории](nautilus/professional-colleague-agents-ru/06-riski.md)](#6-риски-специфичные-для-этой-категорииnautilusprofessional-colleague-agents-ru06-riskimd)
  - [[7. Области применения](nautilus/professional-colleague-agents-ru/07-oblasti-primeneniya.md)](#7-области-примененияnautilusprofessional-colleague-agents-ru07-oblasti-primeneniyamd)
  - [[8. Пилотное предложение: SGB Колega-Адвокат](nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md)](#8-пилотное-предложение-sgb-колega-адвокатnautilusprofessional-colleague-agents-ru08-pilot-sgb-kolegamd)
  - [[9. Связь с другими типами агентов](nautilus/professional-colleague-agents-ru/09-svyaz-s-drugimi.md)](#9-связь-с-другими-типами-агентовnautilusprofessional-colleague-agents-ru09-svyaz-s-drugimimd)
  - [[10. Открытые вопросы](nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md)](#10-открытые-вопросыnautilusprofessional-colleague-agents-ru10-otkrytye-voprosymd)
  - [[11. Призыв к сотрудничеству](nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md)](#11-призыв-к-сотрудничествуnautilusprofessional-colleague-agents-ru11-prizyv-k-sotrudnichestvumd)
  - [[12. Заключение](nautilus/professional-colleague-agents-ru/12-zaklyuchenie.md)](#12-заключениеnautilusprofessional-colleague-agents-ru12-zaklyucheniemd)
  - [[professional-colleague-agents-ru](nautilus/professional-colleague-agents-ru/README.md)](#professional-colleague-agents-runautilusprofessional-colleague-agents-rureadmemd)
  - [[AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations](nautilus/representative-agent-layer-en/00-abstract.md)](#ai-mediated-representation-for-underrepresented-experts-and-vulnerable-populationsnautilusrepresentative-agent-layer-en00-abstractmd)
  - [[1. The Cinderella Syndrome: Why Quality Stays Invisible](nautilus/representative-agent-layer-en/01-cinderella-syndrome.md)](#1-the-cinderella-syndrome-why-quality-stays-invisiblenautilusrepresentative-agent-layer-en01-cinderella-syndromemd)
  - [[2. Historical Precedents: Agents as Civilizational Innovation](nautilus/representative-agent-layer-en/02-historical-precedents.md)](#2-historical-precedents-agents-as-civilizational-innovationnautilusrepresentative-agent-layer-en02-historical-precedentsmd)
  - [[3. What Makes a Representative Agent](nautilus/representative-agent-layer-en/03-what-makes-representative-agent.md)](#3-what-makes-a-representative-agentnautilusrepresentative-agent-layer-en03-what-makes-representative-agentmd)
  - [[4. Ten Domains of Application](nautilus/representative-agent-layer-en/04-ten-domains.md)](#4-ten-domains-of-applicationnautilusrepresentative-agent-layer-en04-ten-domainsmd)
  - [[5. Architectural Specification](nautilus/representative-agent-layer-en/05-architectural-specification.md)](#5-architectural-specificationnautilusrepresentative-agent-layer-en05-architectural-specificationmd)
  - [[6. Ethical Framework](nautilus/representative-agent-layer-en/06-ethical-framework.md)](#6-ethical-frameworknautilusrepresentative-agent-layer-en06-ethical-frameworkmd)
  - [[7. Governance and Oversight](nautilus/representative-agent-layer-en/07-governance-oversight.md)](#7-governance-and-oversightnautilusrepresentative-agent-layer-en07-governance-oversightmd)
  - [[8. Risks and Mitigations](nautilus/representative-agent-layer-en/08-risks-mitigations.md)](#8-risks-and-mitigationsnautilusrepresentative-agent-layer-en08-risks-mitigationsmd)
  - [[9. Phased Rollout Strategy](nautilus/representative-agent-layer-en/09-phased-rollout.md)](#9-phased-rollout-strategynautilusrepresentative-agent-layer-en09-phased-rolloutmd)
  - [[10. Open Questions](nautilus/representative-agent-layer-en/10-open-questions.md)](#10-open-questionsnautilusrepresentative-agent-layer-en10-open-questionsmd)
  - [[11. Call for Collaboration](nautilus/representative-agent-layer-en/11-call-for-collaboration.md)](#11-call-for-collaborationnautilusrepresentative-agent-layer-en11-call-for-collaborationmd)
  - [[12. Closing](nautilus/representative-agent-layer-en/12-closing.md)](#12-closingnautilusrepresentative-agent-layer-en12-closingmd)
  - [[representative-agent-layer-en](nautilus/representative-agent-layer-en/README.md)](#representative-agent-layer-ennautilusrepresentative-agent-layer-enreadmemd)
  - [[Содержание](nautilus/representative-agent-layer-ru/00-abstract.md)](#содержаниеnautilusrepresentative-agent-layer-ru00-abstractmd)
  - [[1. Синдром Золушки: Почему качество остаётся невидимым](nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md)](#1-синдром-золушки-почему-качество-остаётся-невидимымnautilusrepresentative-agent-layer-ru01-sindrom-zolushkimd)
  - [[2. Исторические прецеденты: Агенты как цивилизационная инновация](nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md)](#2-исторические-прецеденты-агенты-как-цивилизационная-инновацияnautilusrepresentative-agent-layer-ru02-istoricheskie-pretsedentymd)
  - [[3. Что делает агента Представительским](nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md)](#3-что-делает-агента-представительскимnautilusrepresentative-agent-layer-ru03-chto-delaet-predstavitelskimmd)
  - [[4. Десять областей применения](nautilus/representative-agent-layer-ru/04-desyat-oblastey.md)](#4-десять-областей-примененияnautilusrepresentative-agent-layer-ru04-desyat-oblasteymd)
  - [[5. Архитектурная спецификация](nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md)](#5-архитектурная-спецификацияnautilusrepresentative-agent-layer-ru05-arkhitekturnaya-spetsifikatsiyamd)
  - [[6. Этическая рамка](nautilus/representative-agent-layer-ru/06-eticheskaya-ramka.md)](#6-этическая-рамкаnautilusrepresentative-agent-layer-ru06-eticheskaya-ramkamd)
  - [[7. Управление и надзор](nautilus/representative-agent-layer-ru/07-upravlenie-nadzor.md)](#7-управление-и-надзорnautilusrepresentative-agent-layer-ru07-upravlenie-nadzormd)
  - [[8. Риски и меры противодействия](nautilus/representative-agent-layer-ru/08-riski-mery.md)](#8-риски-и-меры-противодействияnautilusrepresentative-agent-layer-ru08-riski-merymd)
  - [[9. Стратегия поэтапного развёртывания](nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md)](#9-стратегия-поэтапного-развёртыванияnautilusrepresentative-agent-layer-ru09-strategiya-razvyortyvaniyamd)
  - [[10. Открытые вопросы](nautilus/representative-agent-layer-ru/10-otkrytye-voprosy.md)](#10-открытые-вопросыnautilusrepresentative-agent-layer-ru10-otkrytye-voprosymd)
  - [[11. Призыв к сотрудничеству](nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md)](#11-призыв-к-сотрудничествуnautilusrepresentative-agent-layer-ru11-prizyv-k-sotrudnichestvumd)
  - [[12. Заключение](nautilus/representative-agent-layer-ru/12-zaklyuchenie.md)](#12-заключениеnautilusrepresentative-agent-layer-ru12-zaklyucheniemd)
  - [[representative-agent-layer-ru](nautilus/representative-agent-layer-ru/README.md)](#representative-agent-layer-runautilusrepresentative-agent-layer-rureadmemd)
  - [[TL;DR — Трёхфазная методология Review](nautilus/review-methodology/00-tldr.md)](#tldr-трёхфазная-методология-reviewnautilusreview-methodology00-tldrmd)
  - [[1. Контекст и мотивация](nautilus/review-methodology/01-context-motivation.md)](#1-контекст-и-мотивацияnautilusreview-methodology01-context-motivationmd)
  - [[2. Формальный workflow](nautilus/review-methodology/02-formal-workflow.md)](#2-формальный-workflownautilusreview-methodology02-formal-workflowmd)
  - [[3. Принципы консолидации (Фаза C)](nautilus/review-methodology/03-consolidation-principles.md)](#3-принципы-консолидации-фаза-cnautilusreview-methodology03-consolidation-principlesmd)
  - [[Вопрос: fallback‑ratio как критический или осмысленный?](nautilus/review-methodology/04-fallback-ratio-question.md)](#вопрос-fallbackratio-как-критический-или-осмысленныйnautilusreview-methodology04-fallback-ratio-questionmd)
  - [[4. Условия применимости](nautilus/review-methodology/05-conditions-of-applicability.md)](#4-условия-применимостиnautilusreview-methodology05-conditions-of-applicabilitymd)
  - [[5. Связь с существующими методологиями](nautilus/review-methodology/06-relation-existing-methodologies.md)](#5-связь-с-существующими-методологиямиnautilusreview-methodology06-relation-existing-methodologiesmd)
  - [[6. Почему это валидный паттерн для AI‑assisted workflows](nautilus/review-methodology/07-why-valid-for-ai.md)](#6-почему-это-валидный-паттерн-для-aiassisted-workflowsnautilusreview-methodology07-why-valid-for-aimd)
  - [[7. Реализация в проекте Nautilus](nautilus/review-methodology/08-implementation-nautilus.md)](#7-реализация-в-проекте-nautilusnautilusreview-methodology08-implementation-nautilusmd)
  - [[8. Ограничения и открытые вопросы](nautilus/review-methodology/09-limitations-open-questions.md)](#8-ограничения-и-открытые-вопросыnautilusreview-methodology09-limitations-open-questionsmd)
  - [[9. Checklist применения методологии](nautilus/review-methodology/10-checklist.md)](#9-checklist-применения-методологииnautilusreview-methodology10-checklistmd)
  - [[10. Конкретный план применения к текущим документам](nautilus/review-methodology/11-application-plan-current-docs.md)](#10-конкретный-план-применения-к-текущим-документамnautilusreview-methodology11-application-plan-current-docsmd)
  - [[Appendix A: Шаблон для header warning](nautilus/review-methodology/12-appendix-a-header-warning.md)](#appendix-a-шаблон-для-header-warningnautilusreview-methodology12-appendix-a-header-warningmd)
  - [[Appendix B: Примеры расхождений и их разрешения](nautilus/review-methodology/13-appendix-b-examples.md)](#appendix-b-примеры-расхождений-и-их-разрешенияnautilusreview-methodology13-appendix-b-examplesmd)
  - [[Главные технические риски](nautilus/review-methodology/14-main-technical-risks.md)](#главные-технические-рискиnautilusreview-methodology14-main-technical-risksmd)
  - [[Appendix C: История изменений методологии](nautilus/review-methodology/15-appendix-c-history.md)](#appendix-c-история-изменений-методологииnautilusreview-methodology15-appendix-c-historymd)
  - [[Глоссарий](nautilus/review-methodology/16-glossary.md)](#глоссарийnautilusreview-methodology16-glossarymd)
  - [[review-methodology](nautilus/review-methodology/README.md)](#review-methodologynautilusreview-methodologyreadmemd)
  - [[Du hast gesagt: Спрос рождает предложение - это простая экономическая истина нач…](nautilus/supply-demand/00-question-supply-demand.md)](#du-hast-gesagt-спрос-рождает-предложение---это-простая-экономическая-истина-начnautilussupply-demand00-question-supply-demandmd)
  - [[Claude hat geantwortet: Очень богатый вопрос — три разных, но связанных темы.](nautilus/supply-demand/01-three-related-themes.md)](#claude-hat-geantwortet-очень-богатый-вопрос-три-разных-но-связанных-темыnautilussupply-demand01-three-related-themesmd)
  - [[supply-demand](nautilus/supply-demand/README.md)](#supply-demandnautilussupply-demandreadmemd)
  - [[Du hast gesagt: Того если гора не идёт человеку может быть этот человек пойдёт к…](nautilus/transmission-box/00-question-mountain-to-person.md)](#du-hast-gesagt-того-если-гора-не-идёт-человеку-может-быть-этот-человек-пойдёт-кnautilustransmission-box00-question-mountain-to-personmd)
  - [[Claude hat geantwortet: Это исключительно богатый вопрос, и я хочу ответить на н…](nautilus/transmission-box/01-completing-loop.md)](#claude-hat-geantwortet-это-исключительно-богатый-вопрос-и-я-хочу-ответить-на-нnautilustransmission-box01-completing-loopmd)
  - [[transmission-box](nautilus/transmission-box/README.md)](#transmission-boxnautilustransmission-boxreadmemd)
- [Processing Guide](#processing-guide)
  - [[Обработка больших массивов информации — Часть 1: Обзор и таксономия](processing-guide/01-overview.md)](#обработка-больших-массивов-информации-часть-1-обзор-и-таксономияprocessing-guide01-overviewmd)
  - [[Обработка больших массивов — Часть 2: Извлечение](processing-guide/02-extraction.md)](#обработка-больших-массивов-часть-2-извлечениеprocessing-guide02-extractionmd)
  - [[Обработка больших массивов — Часть 3: Разбивка и чанкинг](processing-guide/03-chunking.md)](#обработка-больших-массивов-часть-3-разбивка-и-чанкингprocessing-guide03-chunkingmd)
  - [[Обработка больших массивов — Часть 4: Структурирование](processing-guide/04-structuring.md)](#обработка-больших-массивов-часть-4-структурированиеprocessing-guide04-structuringmd)
  - [[Обработка больших массивов — Часть 5: Анализ и NLP](processing-guide/05-analysis.md)](#обработка-больших-массивов-часть-5-анализ-и-nlpprocessing-guide05-analysismd)
  - [[Обработка больших массивов — Часть 6: Поиск](processing-guide/06-search.md)](#обработка-больших-массивов-часть-6-поискprocessing-guide06-searchmd)
  - [[Обработка больших массивов — Часть 7: LLM-обогащение](processing-guide/07-llm.md)](#обработка-больших-массивов-часть-7-llm-обогащениеprocessing-guide07-llmmd)
  - [[Обработка больших массивов — Часть 8: Экспорт и интеграции](processing-guide/08-export.md)](#обработка-больших-массивов-часть-8-экспорт-и-интеграцииprocessing-guide08-exportmd)
  - [[Обработка больших массивов — Часть 9: Автоматизация](processing-guide/09-automation.md)](#обработка-больших-массивов-часть-9-автоматизацияprocessing-guide09-automationmd)
  - [[Обработка больших массивов — Часть 10: Инновационные подходы](processing-guide/10-future.md)](#обработка-больших-массивов-часть-10-инновационные-подходыprocessing-guide10-futuremd)
  - [[Обработка больших массивов документов — Полное руководство](processing-guide/PROCESSING_GUIDE.md)](#обработка-больших-массивов-документов-полное-руководствоprocessing-guideprocessing_guidemd)
  - [[Q&A: processing-guide](processing-guide/QA.md)](#qa-processing-guideprocessing-guideqamd)
  - [[processing-guide](processing-guide/README.md)](#processing-guideprocessing-guidereadmemd)
- [Svyazi 2 0](#svyazi-2-0)
  - [[Q&A: svyazi-2-0](svyazi-2-0/QA.md)](#qa-svyazi-2-0svyazi-2-0qamd)
  - [[svyazi-2-0](svyazi-2-0/README.md)](#svyazi-2-0svyazi-2-0readmemd)
  - [[architecture](svyazi-2-0/architecture/README.md)](#architecturesvyazi-2-0architecturereadmemd)
  - [[Card Envelope](svyazi-2-0/architecture/card-envelope.md)](#card-envelopesvyazi-2-0architecturecard-envelopemd)
  - [[Evidence Envelope](svyazi-2-0/architecture/evidence-envelope.md)](#evidence-envelopesvyazi-2-0architectureevidence-envelopemd)
  - [[Архитектурные зазоры](svyazi-2-0/architecture/gaps.md)](#архитектурные-зазорыsvyazi-2-0architecturegapsmd)
  - [[Интеграционная спецификация (минимум для MVP)](svyazi-2-0/architecture/integration-spec.md)](#интеграционная-спецификация-минимум-для-mvpsvyazi-2-0architectureintegration-specmd)
  - [[Memory Write Policy](svyazi-2-0/architecture/memory-write-policy.md)](#memory-write-policysvyazi-2-0architecturememory-write-policymd)
  - [[Review Record](svyazi-2-0/architecture/review-record.md)](#review-recordsvyazi-2-0architecturereview-recordmd)
  - [[Skill and Tool Policy](svyazi-2-0/architecture/skill-tool-policy.md)](#skill-and-tool-policysvyazi-2-0architectureskill-tool-policymd)
  - [[components](svyazi-2-0/components/README.md)](#componentssvyazi-2-0componentsreadmemd)
  - [[agent-memory-mcp + Memory OS](svyazi-2-0/components/agent-memory-mcp.md)](#agent-memory-mcp-memory-ossvyazi-2-0componentsagent-memory-mcpmd)
  - [[AgentFS](svyazi-2-0/components/agentfs.md)](#agentfssvyazi-2-0componentsagentfsmd)
  - [[AI Factory + AIF Handoff](svyazi-2-0/components/ai-factory.md)](#ai-factory-aif-handoffsvyazi-2-0componentsai-factorymd)
  - [[AutoResearch + Sequential](svyazi-2-0/components/autoresearch-sequential.md)](#autoresearch-sequentialsvyazi-2-0componentsautoresearch-sequentialmd)
  - [[Graph RAG](svyazi-2-0/components/graph-rag.md)](#graph-ragsvyazi-2-0componentsgraph-ragmd)
  - [[Hybrid RAG knowledge base](svyazi-2-0/components/hybrid-rag.md)](#hybrid-rag-knowledge-basesvyazi-2-0componentshybrid-ragmd)
  - [[knowledge-space](svyazi-2-0/components/knowledge-space.md)](#knowledge-spacesvyazi-2-0componentsknowledge-spacemd)
  - [[Legal RAG](svyazi-2-0/components/legal-rag.md)](#legal-ragsvyazi-2-0componentslegal-ragmd)
  - [[mclaude](svyazi-2-0/components/mclaude.md)](#mclaudesvyazi-2-0componentsmclaudemd)
  - [[MemNet / memory-is-all-you-need](svyazi-2-0/components/memnet.md)](#memnet-memory-is-all-you-needsvyazi-2-0componentsmemnetmd)
  - [[NGT Memory](svyazi-2-0/components/ngt-memory.md)](#ngt-memorysvyazi-2-0componentsngt-memorymd)
  - [[research-docs + LiteParse](svyazi-2-0/components/research-docs-liteparse.md)](#research-docs-liteparsesvyazi-2-0componentsresearch-docs-liteparsemd)
  - [[Rufler](svyazi-2-0/components/rufler.md)](#ruflersvyazi-2-0componentsruflermd)
  - [[Security + routing plane](svyazi-2-0/components/security-routing-plane.md)](#security-routing-planesvyazi-2-0componentssecurity-routing-planemd)
  - [[Self‑Aware MCP + Skills + CodeWiki](svyazi-2-0/components/self-aware-mcp.md)](#selfaware-mcp-skills-codewikisvyazi-2-0componentsself-aware-mcpmd)
  - [[Svyazi](svyazi-2-0/components/svyazi.md)](#svyazisvyazi-2-0componentssvyazimd)
  - [[Voice / local-first stack](svyazi-2-0/components/voice-stack.md)](#voice-local-first-stacksvyazi-2-0componentsvoice-stackmd)
  - [[Yjs + Automerge](svyazi-2-0/components/yjs-automerge.md)](#yjs-automergesvyazi-2-0componentsyjs-automergemd)
  - [[Yodoca](svyazi-2-0/components/yodoca.md)](#yodocasvyazi-2-0componentsyodocamd)
  - [[Ансамбль A — Collaboration OS](svyazi-2-0/ensembles/A-collaboration-os.md)](#ансамбль-a-collaboration-ossvyazi-2-0ensemblesa-collaboration-osmd)
  - [[Ансамбль B — Forensic RAG для доказуемого matching и review](svyazi-2-0/ensembles/B-forensic-rag.md)](#ансамбль-b-forensic-rag-для-доказуемого-matching-и-reviewsvyazi-2-0ensemblesb-forensic-ragmd)
  - [[Ансамбль C — Spec‑driven multi‑agent factory](svyazi-2-0/ensembles/C-multi-agent-factory.md)](#ансамбль-c-specdriven-multiagent-factorysvyazi-2-0ensemblesc-multi-agent-factorymd)
  - [[Ансамбль D — Voice‑first local knowledge mesh](svyazi-2-0/ensembles/D-voice-first-mesh.md)](#ансамбль-d-voicefirst-local-knowledge-meshsvyazi-2-0ensemblesd-voice-first-meshmd)
  - [[Ансамбль E — Safe and cheap execution plane](svyazi-2-0/ensembles/E-execution-plane.md)](#ансамбль-e-safe-and-cheap-execution-planesvyazi-2-0ensemblese-execution-planemd)
  - [[Ансамбль F — Evidence‑Backed Community Intake](svyazi-2-0/ensembles/F-evidence-backed-intake.md)](#ансамбль-f-evidencebacked-community-intakesvyazi-2-0ensemblesf-evidence-backed-intakemd)
  - [[Ансамбль G — Federated Local‑First Community Graph](svyazi-2-0/ensembles/G-federated-local-graph.md)](#ансамбль-g-federated-localfirst-community-graphsvyazi-2-0ensemblesg-federated-local-graphmd)
  - [[Ансамбль H — Research‑to‑Product Flywheel](svyazi-2-0/ensembles/H-research-to-product-flywheel.md)](#ансамбль-h-researchtoproduct-flywheelsvyazi-2-0ensemblesh-research-to-product-flywheelmd)
  - [[Ансамбли проектов](svyazi-2-0/ensembles/README.md)](#ансамбли-проектовsvyazi-2-0ensemblesreadmemd)
  - [[limitations](svyazi-2-0/limitations/README.md)](#limitationssvyazi-2-0limitationsreadmemd)
  - [[Итоговые выводы и порядок сборки](svyazi-2-0/limitations/conclusions.md)](#итоговые-выводы-и-порядок-сборкиsvyazi-2-0limitationsconclusionsmd)
  - [[Что пока лучше не склеивать](svyazi-2-0/limitations/do-not-glue.md)](#что-пока-лучше-не-склеиватьsvyazi-2-0limitationsdo-not-gluemd)
  - [[Лицензионные развилки](svyazi-2-0/limitations/license-tree.md)](#лицензионные-развилкиsvyazi-2-0limitationslicense-treemd)
  - [[outreach](svyazi-2-0/outreach/README.md)](#outreachsvyazi-2-0outreachreadmemd)
  - [[Первые контакты](svyazi-2-0/outreach/first-contacts.md)](#первые-контактыsvyazi-2-0outreachfirst-contactsmd)
  - [[Шаблон первого сообщения](svyazi-2-0/outreach/message-template.md)](#шаблон-первого-сообщенияsvyazi-2-0outreachmessage-templatemd)
  - [[Узкие вопросы для каждого автора](svyazi-2-0/outreach/narrow-questions.md)](#узкие-вопросы-для-каждого-автораsvyazi-2-0outreachnarrow-questionsmd)
  - [[overview](svyazi-2-0/overview/README.md)](#overviewsvyazi-2-0overviewreadmemd)
  - [[Что добавляет продолжение исследования](svyazi-2-0/overview/continuation-intro.md)](#что-добавляет-продолжение-исследованияsvyazi-2-0overviewcontinuation-intromd)
  - [[Executive summary](svyazi-2-0/overview/executive-summary.md)](#executive-summarysvyazi-2-0overviewexecutive-summarymd)
  - [[Методика и рамка отбора](svyazi-2-0/overview/methodology.md)](#методика-и-рамка-отбораsvyazi-2-0overviewmethodologymd)
  - [[Карта найденных проектов и паттернов](svyazi-2-0/overview/projects-map.md)](#карта-найденных-проектов-и-паттерновsvyazi-2-0overviewprojects-mapmd)
  - [[prototype](svyazi-2-0/prototype/README.md)](#prototypesvyazi-2-0prototypereadmemd)
  - [[План MVP-прототипа](svyazi-2-0/prototype/mvp-plan.md)](#план-mvp-прототипаsvyazi-2-0prototypemvp-planmd)
  - [[Ключевые риски и как их закрывать](svyazi-2-0/prototype/risks.md)](#ключевые-риски-и-как-их-закрыватьsvyazi-2-0prototyperisksmd)
  - [[Дорожная карта прототипа](svyazi-2-0/prototype/roadmap.md)](#дорожная-карта-прототипаsvyazi-2-0prototyperoadmapmd)
  - [[security](svyazi-2-0/security/README.md)](#securitysvyazi-2-0securityreadmemd)
  - [[Практичный бюджетный роутинг моделей](svyazi-2-0/security/budget-routing.md)](#практичный-бюджетный-роутинг-моделейsvyazi-2-0securitybudget-routingmd)
  - [[Что стоит зафиксировать как default policy](svyazi-2-0/security/default-policy.md)](#что-стоит-зафиксировать-как-default-policysvyazi-2-0securitydefault-policymd)
  - [[Приватность: local-first by default](svyazi-2-0/security/privacy.md)](#приватность-local-first-by-defaultsvyazi-2-0securityprivacymd)
- [Technology Combinations](#technology-combinations)
  - [[technology-combinations/ — комбинирование технологий для новых свойств](technology-combinations/README.md)](#technology-combinations-комбинирование-технологий-для-новых-свойствtechnology-combinationsreadmemd)
  - [[Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн](technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md)](#комбинация-1-правильная-агентская-архитектура-svyazi-паттернtechnology-combinationscombinations01-pravilnaya-agentskaya-arkhitektura-svyazi-patternmd)
  - [[Комбинация 2: Мультиагентный хаос-решение × Auto AI Router](technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md)](#комбинация-2-мультиагентный-хаос-решение-auto-ai-routertechnology-combinationscombinations02-multiagentnyy-khaos-reshenie-auto-ai-routermd)
  - [[Комбинация 3: CRDT local-first × Svyazi CardIndex](technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md)](#комбинация-3-crdt-local-first-svyazi-cardindextechnology-combinationscombinations03-crdt-local-first-svyazi-cardindexmd)
  - [[Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура](technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md)](#комбинация-4-парсинг-с-llm-graph-rag-правильная-агентская-архитектураtechnology-combinationscombinations04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitekturamd)
  - [[Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной](technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md)](#комбинация-5-sourcecraft-cli-claude-code-sequential-протокол-дочкинойtechnology-combinationscombinations05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoymd)
  - [[Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер](technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md)](#комбинация-6-openclaude-утёкший-claude-code-zinc-inference-engine-mome-роутерtechnology-combinationscombinations06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-md)
  - [[Комбинация 7: Crawl4AI × Docling × Yodoca consolidator](technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md)](#комбинация-7-crawl4ai-docling-yodoca-consolidatortechnology-combinationscombinations07-crawl4ai-docling-yodoca-consolidatormd)
  - [[Комбинация 8: Conductor × adversarial-review × Auto AI Router](technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md)](#комбинация-8-conductor-adversarial-review-auto-ai-routertechnology-combinationscombinations08-conductor-adversarial-review-auto-ai-routermd)
  - [[Комбинация 9: Agent Orchestration Stack](technology-combinations/combinations/09-agent-orchestration-stack.md)](#комбинация-9-agent-orchestration-stacktechnology-combinationscombinations09-agent-orchestration-stackmd)
  - [[Комбинация 10: Legal Document Intelligence Pipeline](technology-combinations/combinations/10-legal-document-intelligence-pipeline.md)](#комбинация-10-legal-document-intelligence-pipelinetechnology-combinationscombinations10-legal-document-intelligence-pipelinemd)
  - [[Комбинация 11: Hybrid CRDT-SQL Database](technology-combinations/combinations/11-hybrid-crdt-sql-database.md)](#комбинация-11-hybrid-crdt-sql-databasetechnology-combinationscombinations11-hybrid-crdt-sql-databasemd)
  - [[Комбинация 12: Multi-Agent Observability Stack](technology-combinations/combinations/12-multi-agent-observability-stack.md)](#комбинация-12-multi-agent-observability-stacktechnology-combinationscombinations12-multi-agent-observability-stackmd)
  - [[Комбинация 13: Legal Document Transpiler](technology-combinations/combinations/13-legal-document-transpiler.md)](#комбинация-13-legal-document-transpilertechnology-combinationscombinations13-legal-document-transpilermd)
  - [[Комбинация 14: local-first Agent Development Environment](technology-combinations/combinations/14-local-first-agent-development-environment.md)](#комбинация-14-local-first-agent-development-environmenttechnology-combinationscombinations14-local-first-agent-development-environmentmd)
  - [[Комбинация 15: Self-Consolidating Legal Corpus](technology-combinations/combinations/15-self-consolidating-legal-corpus.md)](#комбинация-15-self-consolidating-legal-corpustechnology-combinationscombinations15-self-consolidating-legal-corpusmd)
  - [[Комбинация 16: Adversarial Multi-Agent Code Review](technology-combinations/combinations/16-adversarial-multi-agent-code-review.md)](#комбинация-16-adversarial-multi-agent-code-reviewtechnology-combinationscombinations16-adversarial-multi-agent-code-reviewmd)
  - [[Комбинация 17: Distributed Agent Memory with Graph](technology-combinations/combinations/17-distributed-agent-memory-with-graph.md)](#комбинация-17-distributed-agent-memory-with-graphtechnology-combinationscombinations17-distributed-agent-memory-with-graphmd)
  - [[Комбинация 18: LLM-Powered Legal Corpus Builder](technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md)](#комбинация-18-llm-powered-legal-corpus-buildertechnology-combinationscombinations18-llm-powered-legal-corpus-buildermd)
  - [[Комбинация 19: Multi-Agent Observability Platform](technology-combinations/combinations/19-multi-agent-observability-platform.md)](#комбинация-19-multi-agent-observability-platformtechnology-combinationscombinations19-multi-agent-observability-platformmd)
  - [[Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync](technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md)](#комбинация-20-hybrid-olap-oltp-with-real-time-synctechnology-combinationscombinations20-hybrid-olap-oltp-with-real-time-syncmd)
  - [[Комбинация 21: Legal Corpus Analytics at Scale](technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md)](#комбинация-21-legal-corpus-analytics-at-scaletechnology-combinationscombinations21-legal-corpus-analytics-at-scalemd)
  - [[Комбинация 22: Russian-International OSS Stack](technology-combinations/combinations/22-russian-international-oss-stack.md)](#комбинация-22-russian-international-oss-stacktechnology-combinationscombinations22-russian-international-oss-stackmd)
  - [[Комбинация 23: Security-First Code Review Pipeline](technology-combinations/combinations/23-security-first-code-review-pipeline.md)](#комбинация-23-security-first-code-review-pipelinetechnology-combinationscombinations23-security-first-code-review-pipelinemd)
  - [[Комбинация 24: MEGA-INTEGRATION: Full Stack](technology-combinations/combinations/24-mega-integration-full-stack.md)](#комбинация-24-mega-integration-full-stacktechnology-combinationscombinations24-mega-integration-full-stackmd)
  - [[Комбинация 25: Legal DSL → Code Transpiler](technology-combinations/combinations/25-legal-dsl-code-transpiler.md)](#комбинация-25-legal-dsl-code-transpilertechnology-combinationscombinations25-legal-dsl-code-transpilermd)
  - [[Комбинация 26: AST-Based Code Analysis for Legal Automation](technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md)](#комбинация-26-ast-based-code-analysis-for-legal-automationtechnology-combinationscombinations26-ast-based-code-analysis-for-legal-automationmd)
  - [[Комбинация 27: Hybrid RAG with AST-Chunked Code](technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md)](#комбинация-27-hybrid-rag-with-ast-chunked-codetechnology-combinationscombinations27-hybrid-rag-with-ast-chunked-codemd)
  - [[Комбинация 28: Pydantic-Enforced Legal Workflows](technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md)](#комбинация-28-pydantic-enforced-legal-workflowstechnology-combinationscombinations28-pydantic-enforced-legal-workflowsmd)
  - [[Комбинация 29: Meta-Programmatic Legal Template Generator](technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md)](#комбинация-29-meta-programmatic-legal-template-generatortechnology-combinationscombinations29-meta-programmatic-legal-template-generatormd)
  - [[Комбинация 30: MEGA-STACK 3.0 with DSL & AST](technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md)](#комбинация-30-mega-stack-30-with-dsl-asttechnology-combinationscombinations30-mega-stack-3-0-with-dsl-astmd)
  - [[Комбинация 31: Event-Sourced Legal Document History](technology-combinations/combinations/31-event-sourced-legal-document-history.md)](#комбинация-31-event-sourced-legal-document-historytechnology-combinationscombinations31-event-sourced-legal-document-historymd)
  - [[Комбинация 32: Consensus-Based Multi-Agent Coordination](technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md)](#комбинация-32-consensus-based-multi-agent-coordinationtechnology-combinationscombinations32-consensus-based-multi-agent-coordinationmd)
  - [[Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics](technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md)](#комбинация-33-event-sourcing-cqrs-clickhouse-analyticstechnology-combinationscombinations33-event-sourcing-cqrs-clickhouse-analyticsmd)
  - [[Комбинация 34: Distributed Event Store with Paxos](technology-combinations/combinations/34-distributed-event-store-with-paxos.md)](#комбинация-34-distributed-event-store-with-paxostechnology-combinationscombinations34-distributed-event-store-with-paxosmd)
  - [[Комбинация 35: MEGA-STACK 4.0 with Event Sourcing & Consensus](technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md)](#комбинация-35-mega-stack-40-with-event-sourcing-consensustechnology-combinationscombinations35-mega-stack-4-0-with-event-sourcing-consensusmd)
  - [[combinations](technology-combinations/combinations/README.md)](#combinationstechnology-combinationscombinationsreadmemd)
  - [[Mega‑Stack 1.0 — Полный Legal‑AI Stack](technology-combinations/mega-stacks/01-legal-ai-stack.md)](#megastack-10-полный-legalai-stacktechnology-combinationsmega-stacks01-legal-ai-stackmd)
  - [[Mega‑Stack 2.0 — Ultimate Legal‑AI System](technology-combinations/mega-stacks/02-ultimate-legal-ai.md)](#megastack-20-ultimate-legalai-systemtechnology-combinationsmega-stacks02-ultimate-legal-aimd)
  - [[Mega‑Stack 3.0 — with DSL & AST](technology-combinations/mega-stacks/03-dsl-ast.md)](#megastack-30-with-dsl-asttechnology-combinationsmega-stacks03-dsl-astmd)
  - [[Mega‑Stack 4.0 — with Event Sourcing & Consensus](technology-combinations/mega-stacks/04-event-sourcing-consensus.md)](#megastack-40-with-event-sourcing-consensustechnology-combinationsmega-stacks04-event-sourcing-consensusmd)
  - [[mega-stacks](technology-combinations/mega-stacks/README.md)](#mega-stackstechnology-combinationsmega-stacksreadmemd)
  - [[properties/ — эмерджентные свойства](technology-combinations/properties/README.md)](#properties-эмерджентные-свойстваtechnology-combinationspropertiesreadmemd)
  - [[research-reports](technology-combinations/research-reports/README.md)](#research-reportstechnology-combinationsresearch-reportsreadmemd)
  - [[Research Report: Continuation — 10 New Domains Beyond the Original 45 Combinations](technology-combinations/research-reports/continuation-10-domains.md)](#research-report-continuation-10-new-domains-beyond-the-original-45-combinationstechnology-combinationsresearch-reportscontinuation-10-domainsmd)
  - [[Research Report: Sozialrecht (35 комбинаций)](technology-combinations/research-reports/sozialrecht-35-combinations.md)](#research-report-sozialrecht-35-комбинацийtechnology-combinationsresearch-reportssozialrecht-35-combinationsmd)
  - [[Сводная таблица 1–8](technology-combinations/synthesis-tables/01-08-summary.md)](#сводная-таблица-18technology-combinationssynthesis-tables01-08-summarymd)
  - [[Сводная таблица 9–14 (Extended)](technology-combinations/synthesis-tables/09-14-extended.md)](#сводная-таблица-914-extendedtechnology-combinationssynthesis-tables09-14-extendedmd)
  - [[Сводная таблица 15–19 (Extended)](technology-combinations/synthesis-tables/15-19-extended.md)](#сводная-таблица-1519-extendedtechnology-combinationssynthesis-tables15-19-extendedmd)
  - [[Сводная таблица 20–24 (Final 1–24)](technology-combinations/synthesis-tables/20-24-final.md)](#сводная-таблица-2024-final-124technology-combinationssynthesis-tables20-24-finalmd)
  - [[Сводная таблица 25–30 (Complete 1–30)](technology-combinations/synthesis-tables/25-30-extended.md)](#сводная-таблица-2530-complete-130technology-combinationssynthesis-tables25-30-extendedmd)
  - [[Сводная таблица 31–35 (Complete 1–35)](technology-combinations/synthesis-tables/31-35-final.md)](#сводная-таблица-3135-complete-135technology-combinationssynthesis-tables31-35-finalmd)
  - [[synthesis-tables](technology-combinations/synthesis-tables/README.md)](#synthesis-tablestechnology-combinationssynthesis-tablesreadmemd)
- [Templates](#templates)
  - [[templates](templates/README.md)](#templatestemplatesreadmemd)
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
  - [Архитектура (548 документов)](#архитектура-548-документов)
  - [Документация (169 документов)](#документация-169-документов)
  - [Проекты (154 документов)](#проекты-154-документов)
  - [Агенты (132 документов)](#агенты-132-документов)
  - [Код (111 документов)](#код-111-документов)
  - [Контакты (52 документов)](#контакты-52-документов)
  - [Память (39 документов)](#память-39-документов)
  - [Анализ (25 документов)](#анализ-25-документов)
- [Использование](#использование)

---


> [!NOTE]
> Раздел `OUTLINE` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: outline, docs -->


<!-- summary -->
> `OUTLINE` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-11_

Секций: **21** | Файлов: **1230**

## Содержание

- [Docs](#docs) — 100 файлов
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
- [Letters](#letters) — 10 файлов
- [Lorenzo Agent](#lorenzo-agent) — 62 файлов
- [Meta Scripting](#meta-scripting) — 7 файлов
- [Nautilus](#nautilus) — 255 файлов
- [Processing Guide](#processing-guide) — 13 файлов
- [Svyazi 2 0](#svyazi-2-0) — 60 файлов
- [Technology Combinations](#technology-combinations) — 53 файлов
- [Templates](#templates) — 24 файлов


## Docs

_Путь: `docs/`_

### [Словарь аббревиатур и сокращений](ABBREVIATIONS.md)
> > > Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

  - Самые часто используемые
  - Использование
- Запуск
- Вариант 2

_Слов: 2034_

### [Action Items, риски и решения](ACTION_ITEMS.md)
> > !NOTE

  - ➡️ Следующие шаги (364)
  - ✅ Решения и рекомендации (1065)
  - ⚠️ Риски (1309)
  - 🚫 Ограничения (384)
  - 📋 Задачи (TODO) (38)
  - 📬 Контактные действия (314)
  - Использование
- Запуск
  _... ещё 5 разделов_

_Слов: 9104_

### [Callout-блоки](ALERTS.md)
> > Добавлено 36 callout-блоков в документы.

  - Пример синтаксиса

_Слов: 119_

### [Авторы и коллаборации](AUTHORS.md)
> > !NOTE

  - Использование
- Запуск

_Слов: 206_

### [Автозаполненные шаблоны](AUTOFILLED.md)
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

_Слов: 322_

### [Индекс обратных ссылок](BACKLINKS.md)
> > !NOTE

  - Топ-30 самых цитируемых документов
  - Ссылки по разделам
  - Использование
- Запуск
  - Смотрите также

_Слов: 586_

### [Status Badges](BADGES.md)
> > Бейджи статуса репозитория: тесты, шаблоны, скрипты, скилы

  - Превью
  - Markdown сниппеты для README

_Слов: 129_

### [CHANGELOG](CHANGELOG.md)
> > !NOTE

  - semantic (1 коммитов)
  - md (1 коммитов)
  - 2026-05-11 (45 коммитов)
  - 2026-05-10 (58 коммитов)
  - 2026-04-29 (141 коммитов)
  - skip  (1 коммитов)
  - 22 скила  (1 коммитов)
  - $.STEP.ou (1 коммитов)
  _... ещё 4 разделов_

_Слов: 3952_

### [Changelog (авто)](CHANGELOG_AUTO.md)
> > !NOTE

  - Статистика коммитов
  - История изменений
  - Использование
- Запуск
  - Смотрите также

_Слов: 1969_

### [Кластеры тематически близких файлов](CLUSTERS.md)
> > > Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

  - Кластер 1 — концептов, поиска, репозитория, через (370 файлов)
  - Кластер 2 — turn, view, svyazi, agentfs (106 файлов)
  - Кластер 3 — cowork, ingit, project, mcp (86 файлов)
  - Кластер 4 — agent, principal, professional, agents (66 файлов)
  - Кластер 5 — author-contact, status-of-this-document, portal-protocol-md, author (65 файлов)
  - Кластер 6 — table-of-contents, table, double-triangle, triangle (60 файлов)
  - Кластер 7 — compatibility-level, level, native-format, bridges (57 файлов)
  - Кластер 8 — turn, view, citeturn, memory (56 файлов)
  _... ещё 24 разделов_

_Слов: 1780_

### [Code-блоки репозитория](CODE_BLOCKS.md)
> > > Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

  - Содержание
  - 📊 Диаграммы Mermaid (46)
- ... (обрезано)
- ... (обрезано)
- ... (обрезано)
  - 🐍 Python (204)
- ... (обрезано)
- ... (обрезано)
  _... ещё 76 разделов_

_Слов: 5973_

### [Рекомендации по коллаборации (Collaboration Finder)](COLLAB_SUGGESTIONS.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 1. Wikontic: семантический граф
  - 2. NGT[^ngt] Memory: ассоциативный граф
  - 3. knowledge-space
  - 4. MemNet / memory-is-all-you-need
  - Следующие шаги

_Слов: 702_

### [Сравнение с предыдущим коммитом](COMPARE.md)
> > !NOTE

  - Новые файлы (1004)
  - Удалённые файлы (0)
  - Изменившиеся файлы (217) — топ по Δ слов
  - Использование
- Запуск

_Слов: 544_

### [Оценка читаемости документов](COMPLEXITY.md)
> > !NOTE

  - Распределение сложности
  - Самые сложные документы
  - Самые простые документы
  - Методология
  - Использование
- Запуск
  - Смотрите также

_Слов: 625_

### [Матрица компонентов Svyazi 2.0](COMPONENT_MATRIX.md)
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

_Слов: 1069_

### [Глоссарий понятий](CONCEPTS.md)
> > !NOTE

  - A
  - B
  - C
  - D
  - E
  - F
  - G
  - H
  _... ещё 54 разделов_

_Слов: 15054_

### [Граф концептов базы знаний](CONCEPT_GRAPH.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Диаграмма
  - Топ концептов по связям
  - Смотрите также

_Слов: 781_

### [Согласованность терминов](CONSISTENCY.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Детали по файлам
  - Как исправить
- Пример: заменить все вхождения в docs/

_Слов: 1032_

### [Контакты и авторы](CONTACTS.md)
> > !NOTE

  - Содержание
  - Ключевые авторы проектов
  - GitHub репозитории
  - Email адреса
  - Шаблон первого сообщения

_Слов: 659_

### [Приоритет контактов](CONTACT_PRIORITY.md)
> > !NOTE

  - Топ авторов по приоритету
  - Рекомендуемые следующие шаги
  - Формула расчёта балла

_Слов: 438_

### [Противоречия в базе знаний](CONTRADICTIONS.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Найденные противоречия
  - Использование
- Запуск
  - Смотрите также
  - Использование
- Запуск

_Слов: 2321_

### [Оценка стоимости MVP](COST.md)
> > !NOTE

  - Содержание
  - Итого
  - По компонентам
  - По ролям
  - Сценарии
  - Временные оценки из документов
  - Допущения
  - Использование
  _... ещё 1 разделов_

_Слов: 617_

### [Перекрёстные ссылки](CROSSREFS.md)
> > !NOTE

  - Проекты → файлы
  - Файлы → проекты
  - Использование
- Запуск
  - Смотрите также

_Слов: 690_

### [Кросс-секционный анализ](CROSS_SECTION.md)
> > !NOTE

  - Матрица сходства секций
  - Граф связей
  - Топ-40 кросс-секционных концептов
  - Детальная карта концептов
  - Использование
- Запуск
- Вариант 2
  - Смотрите также

_Слов: 4140_

### [Ключевые решения и выводы](DECISIONS.md)
> Автоматически извлечено из всех документов: 1259 записей

  - Архитектура (84)
  - Mvp (16)
  - Память (15)
  - Оркестрация (38)
  - Безопасность (12)
  - Лицензия (21)
  - Риски (7)
  - Контакты (48)
  _... ещё 1 разделов_

_Слов: 2543_

### [Knowledge OS — Demo](DEMO.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Быстрый старт
- По запросу
- По документу (извлекает текст автоматически)
- Benchmark: 5 эталонных запросов против критериев успеха
- JSON-вывод для интеграции
  - Примеры запросов
  _... ещё 11 разделов_

_Слов: 627_

### [Карта плотности тем](DENSITY.md)
> > !NOTE

  - Наиболее раскрытые темы
  - Слабо раскрытые темы (0)
  - Где сосредоточена каждая тема
  - Использование
- Запуск
  - Смотрите также

_Слов: 672_

### [Мониторинг зависимостей](DEPENDABOT.md)
> > !NOTE

  - Python-зависимости
  - OSS-проекты (Svyazi 2.0)
  - Автоматизация
- Генерировать .github/dependabot.yml
- Проверить актуальные версии PyPI

_Слов: 164_

### [Карта зависимостей скриптов](DEPENDENCY_MAP.md)
> > !NOTE

  - Зависимости
  - Скрипты без карты зависимостей
  - Порядок запуска (рекомендуемый)
  - Смотрите также

_Слов: 1149_

### [Дайджест изменений](DIGEST.md)
> > !NOTE

  - Последний коммит
  - Последние 3 коммита — итого
  - История коммитов (последние 15)
  - Текущее состояние репозитория
  - Использование
- Запуск

_Слов: 338_

### [Автодайджест изменений](DIGEST_AUTO.md)
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

_Слов: 480_

### [Еженедельный дайджест — 2026-05-11](DIGEST_WEEKLY.md)
> > !NOTE

  - Итого
  - Коммиты
  - Новые документы
  - Активность по разделам
  - Изменённые документы
  - Смотрите также

_Слов: 350_

### [Отчёт о дублировании](DUPLICATES.md)
> > !NOTE

  - Похожие файлы (Jaccard ≥ 0.5)
  - Смотрите также

_Слов: 2007_

### [Пустые секции](EMPTY_SECTIONS.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Файлы с ≥50% пустых секций (приоритет)
  - Все файлы с пустыми секциями
  - Использование
- Запуск
- Вариант 2
- Вариант 3
  _... ещё 25 разделов_

_Слов: 44436_

### [Именованные сущности](ENTITIES.md)
> > !NOTE

  - Люди и авторы (7)
  - Проекты (22)
  - Организации (9)
  - Технологии и стандарты (24)
  - GitHub репозитории (15)
  - Ко-встречаемость проектов (топ пары)
  - Использование
- Запуск

_Слов: 767_

### [Часто задаваемые вопросы (FAQ)](FAQ.md)
> - Архитектура(#архитектура)

  - Содержание
  - Архитектура
  - MVP/Запуск
  - Компоненты
  - Интеграция
  - Лицензия
  - Общее
  - Использование
  _... ещё 1 разделов_

_Слов: 1790_

### [Сноски и определения терминов](FOOTNOTES.md)
> > !NOTE

  - Словарь сносок
  - Как это работает

_Слов: 351_

### [Lorenzo Gateway](GATEWAY.md)
> - Содержание(#содержание)

  - Содержание
  - Содержание
  - Что это
  - Сравнение с DAF-gateway
  - Архитектура
  - Запуск
- Установить зависимости
- Запустить (базовый режим, без LLM)
  _... ещё 10 разделов_

_Слов: 1354_

### [Глоссарий проектов](GLOSSARY.md)
> > !NOTE

  - Использование
- Запуск

_Слов: 255_

### [Граф связей проектов](GRAPH.md)
> > !NOTE

  - Топ совместных упоминаний
  - DOT-формат (Graphviz)

_Слов: 2736_

### [Аудит заголовков](HEADING_AUDIT.md)
> > !NOTE

  - Содержание
  - Типы проблем
  - По файлам
  - Использование
- Запуск
- Вариант 2
- Вариант 3
- Вариант 4
  _... ещё 3 разделов_

_Слов: 13557_

### [Health Dashboard](HEALTH.md)
> > Балл здоровья репозитория: 100/100 — файлов: 2482, слов: 2,922,644

  - Общий балл: 100/100 🟢
  - Метрики
  - Структура репозитория
  - Action Items
  - Скрипты обработки
  - Рекомендации
  - Смотрите также

_Слов: 327_

### [Тепловая карта тем](HEATMAP.md)
> > !NOTE

  - Числовые значения (‰)
  - Доминирующие темы по разделам
  - Концентрация тем
  - Смотрите также

_Слов: 556_

### [Индекс документации — Lorenzo / Svyazi 2.0](INDEX.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Метрики репозитория
  - Разделы документации
  - Аналитика и отчёты
  - Ключевые документы
  - LLM-обогащение (Ступень 3)
  - Быстрый старт
  _... ещё 3 разделов_

_Слов: 694_

### [Инвертированный индекс ключевых слов](KEYWORD_INDEX.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Топ слов по охвату файлов
  - Топ биграмм (устойчивые словосочетания)
  - Использование
- Запуск
  - Смотрите также

_Слов: 1151_

### [Карта базы знаний Lorenzo](KNOWLEDGE_MAP.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Корпус
  - Метрики качества
  - По секциям
  - Ключевые концепты
  - Топ сущностей
  - Открытые вопросы
  _... ещё 4 разделов_

_Слов: 735_

### [Числовые KPI и метрики](KPI.md)
> > KPI — раздел документации проекта Lorenzo.

  - Количество (550)
  - Проценты (384)
  - Время (557)
  - Стоимость (934)
  - Размер (64)
  - Версия (788)
  - Рейтинг (100)
  - Этап (176)
  _... ещё 4 разделов_

_Слов: 2787_

### [История метрик KPI](KPI_HISTORY.md)
> - Текущие метрики(#текущие-метрики)

  - Contents
  - Текущие метрики
  - История
  - Тренды (последние снапшоты)
  - Смотрите также

_Слов: 287_

### [Языковой состав документов](LANGUAGE_STATS.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Распределение
  - Файлы с неожиданным языком
  - Смешанные файлы (MIX)
  - По секциям
  - Использование
- Запуск
  _... ещё 4 разделов_

_Слов: 7888_

### [Индекс ссылок](LINKS.md)
> > !NOTE


_Слов: 1075_

### [AI-саммари разделов документации](LLM_SUMMARIES.md)
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

_Слов: 386_

### [MCP Dashboard](MCP_DASHBOARD.md)
> > !NOTE

  - Использование
- Запуск
  - Смотрите также

_Слов: 138_

### [Методология работы со скриптами](METHODOLOGY.md)
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

_Слов: 1070_

### [Метрики качества документации](METRICS.md)
> > Средний балл: 95.9/100 по 1226 документам

  - Качество по разделам
  - Топ-15 лучших документов
  - Документы, требующие улучшения (5)
  - Общие показатели
  - Использование
- Обновить метрики и проверить здоровье репозитория
  - Смотрите также

_Слов: 459_

### [Майндмап репозитория Lorenzo](MINDMAP.md)
> > !NOTE

  - Структура разделов
  - Поток данных между проектами
  - Легенда

_Слов: 317_

### [Карта пробелов знаний](MISSING.md)
> > > Документ создан на основе исследования. Ссылки ведут на связанные материалы.

  - Итог
  - Рекомендации
  - Использование
- Запуск

_Слов: 529_

### [Индекс именованных сущностей](NAMED_ENTITIES.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 👤 People (20)
  - 📦 Projects (150)
  - ⚙️ Tech (31)
  - 🏢 Orgs (8)
  - 📅 Dates (39)
  - Использование
  _... ещё 2 разделов_

_Слов: 1877_

### [Нарратив проекта Lorenzo](NARRATIVE.md)
> > Связный рассказ о том, как складывается проект — от первых идей до конкретных планов.

  - Содержание
  - Глава 1: Исходная точка — Svyazi 2.0
  - Глава 2: Экосистема проектов
  - Глава 3: Ансамбли — синергия компонентов
  - Глава 4: MVP — что строим первым
  - Глава 5: Архитектурные пробелы
  - Глава 6: Контракты интеграции
  - Глава 7: Дорожная карта
  _... ещё 7 разделов_

_Слов: 1206_

### [Сеть проектов и авторов](NETWORK.md)
> > !NOTE

  - Топ-20 ко-упоминаемых пар
  - Центральность узлов (влиятельность)
  - Авторы ↔ Проекты
  - Использование
- Запуск

_Слов: 510_

### [Онбординг — Svyazi 2.0 / Lorenzo](ONBOARDING.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Что это такое?
  - Первые 30 минут
- 1. Клонировать репозиторий
- 2. Прочитать Executive Summary
- 3. Посмотреть статус проекта
- 4. Прочитать FAQ
  _... ещё 12 разделов_

_Слов: 614_

### [Изолированные документы (Orphans)](ORPHANS.md)
> > !NOTE

  - Топ-20 по объёму (важные и изолированные)
  - По разделам
  - Рекомендации
  - Использование
- Запуск

_Слов: 148_

### [Качество абзацев](PARAGRAPH_QUALITY.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Типы проблем
  - По файлам
  - Использование
- Запуск
- Вариант 2
- Вариант 3
  _... ещё 13 разделов_

_Слов: 22488_

### [Пассивный залог и канцеляризмы](PASSIVE_VOICE.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Корпусная статистика
  - Топ файлов по доле пассива
  - Использование
- Запуск
  - Смотрите также

_Слов: 524_

### [Retrieval Hit Rate Evaluation — Lorenzo / Svyazi 2.0](PRECISION_EVAL.md)
> - Результаты (Hit Rate@10)(#результаты-hit-rate10)

  - Содержание
  - Результаты (Hit Rate@10)
  - Детали (20 запросов)
  - Методология
  - Использование
- Запуск

_Слов: 575_

### [Приоритеты файлов](PRIORITIES.md)
> > !NOTE

  - Топ-50 самых важных файлов
  - Топ-5 по каждому разделу
  - Использование
- Запуск
- Вариант 2
  - Смотрите также

_Слов: 3464_

### [Прогресс MVP](PROGRESS.md)
> > !NOTE

  - Ключевые этапы (Milestones)
  - Состояние компонентов
  - Метрики качества
  - Следующий шаг
- Приоритет 1: kksudo (AgentFS, 13 упоминаний)
- Приоритет 2: spbmolot (NGT Memory, 12 упоминаний)
- Приоритет 3: AnastasiyaW (knowledge-space, 11 упоминаний)
  - Связанные документы

_Слов: 324_

### [Svyazi 2.0 — Спецификация прототипа](PROTOTYPE_SPEC.md)
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

_Слов: 1676_

### [Глобальный Q&A](QA.md)
> > !NOTE

  - Содержание
  - Раздел: 01-svyazi
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие инструменты обеспечивают безопасность агентов?
  _... ещё 157 разделов_

_Слов: 3313_

### [Открытые вопросы](QUESTIONS.md)
> > !NOTE

  - Архитектура (60)
  - Интеграция (44)
  - Mvp/сроки (58)
  - Технология (280)
  - Лицензия (41)
  - Команда (76)
  - Общее (1424)
  - Использование
  _... ещё 2 разделов_

_Слов: 1848_

### [Список чтения](READING_LIST.md)
> - По секциям(#по-секциям)

  - Contents
  - По секциям
  - Похожие документы
  - Использование
  - Смотрите также

_Слов: 367_

### [Рекомендуемый порядок чтения](READING_ORDER.md)
> > !NOTE

  - Содержание
  - Маршруты по целям
  - Использование
- Запуск
- Вариант 2
- Вариант 3
- Вариант 4

_Слов: 6185_

### [docs](README.md)
> Файлов: 106

  - Содержание
  - Подразделы
  - Кто ссылается на этот документ (226)
  - Использование

_Слов: 883_

### [REGISTRY — реестр артефактов Lorenzo](REGISTRY.md)
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

### [Svyazi 2.0 — Knowledge Base Report](REPORT.md)
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

_Слов: 967_

### [Реестр рисков — Svyazi 2.0](RISK_REGISTER.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Матрица рисков (Вероятность × Влияние)
  - Реестр
  - Митигации
  - Упоминания рисков в документах
  - Итоговая статистика

_Слов: 1074_

### [Расписание проекта](SCHEDULE.md)
> > !NOTE

  - Ключевые вехи
  - Gantt-диаграмма
  - Задачи по фазам
  - Текущий статус

_Слов: 342_

### [Оценка готовности проекта (Go/No-Go)](SCORING.md)
> > !NOTE

  - Итог: 164/164 (100%) — 🟢 GO
  - Документация — 48/48 (100%) 🟢 GO
  - Архитектура — 41/41 (100%) 🟢 GO
  - Команда и контакты — 23/23 (100%) 🟢 GO
  - Риски — 26/26 (100%) 🟢 GO
  - MVP-готовность — 26/26 (100%) 🟢 GO
  - Приоритетные действия (0 незакрытых)
  - ✅ Проект готов к запуску MVP!
  _... ещё 2 разделов_

_Слов: 375_

### [Каталог скриптов](SCRIPTS_CATALOG.md)
> Обновлено: 2026-05-11

  - По группам
  - Подробно
  - Использование
- Запуск
- Вариант 2
- Вариант 3
- Вариант 4
  - Смотрите также

_Слов: 7792_

### [Отчёт об оценке скриптов Lorenzo](SCRIPT_EVAL_REPORT.md)
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

_Слов: 2969_

### [Результаты поиска](SEARCH_RESULTS.md)
> - Использование(#использование)

  - Contents
  - Использование
  - Смотрите также

_Слов: 344_

### [Индекс «Смотрите также»](SEE_ALSO.md)
> > !NOTE

  - Ключевые связи
  - Использование
- Запуск

_Слов: 294_

### [Тональный анализ документов](SENTIMENT.md)
> > !NOTE

  - Тональность по разделам
  - Самые оптимистичные документы
  - Самые скептичные / риск-ориентированные
  - Распределение тональности
  - Использование
- Запуск
  - Смотрите также

_Слов: 595_

### [SENTINEL Security Report](SENTINEL.md)
> > Дата: 2026-05-11 · Проблем: 3 · HTTP-ссылок: 212 · Лицензионных рисков: 4

  - Contents
  - Итог
  - PII и секреты
  - Небезопасный код
  - Файлы credentials
  - Лицензионные риски
  - HTTP без TLS (212 ссылок)
  - Использование

_Слов: 358_

### [Похожие документы](SIMILAR.md)
> > > Документ создан на основе исследования. Ссылки ведут на связанные материалы.

  - Топ-20 самых похожих пар
  - По разделам
  - Использование
- Запуск
  - Смотрите также

_Слов: 305_

### [Похожие абзацы между документами](SIMILAR_PASSAGES.md)
> > !TIP

  - Содержание
  - Найденные похожие абзацы
  - Похожие документы
  - Использование
  - Смотрите также

_Слов: 1829_

### [Карта репозитория Lorenzo](SITEMAP.md)
> > - Мета-документы(#мета-документы)

  - Содержание
  - Навигация
  - Мета-документы
  - Svyazi 2.0 — Архитектура системы
  - Вакансии Anthropic — 436 позиций
  - Комбинации технологий
  - AI Коллаборации — ансамбли проектов
  - Хабр-проекты — память и граф
  _... ещё 15 разделов_

_Слов: 9605_

### [Skill Dashboard](SKILL_DASHBOARD.md)
> > !NOTE

  - Использование
- Запуск
  - Смотрите также

_Слов: 100_

### [Карта происхождения текстов](SOURCE_MAP.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Категории
  - Авторы
  - 🤖 Авто-импортированные файлы (1722)
  - 🔗 Файлы с внешними ссылками (198)
  - Использование
- Запуск
  _... ещё 8 разделов_

_Слов: 12466_

### [Детальная статистика репозитория](STATS.md)
> > Разделов: 22  Файлов: 2476  Слов: 2,971,091  Символов: 26,108,669

  - Содержание
  - Сводная таблица по разделам
  - Топ-20 файлов по объёму
  - Ключевые показатели

_Слов: 768_

### [Резюме документов (TextRank)](SUMMARIES.md)
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

### [Все таблицы репозитория](TABLES.md)
> - 01-svyazi (11 таблиц)(#01-svyazi-11-таблиц)

  - Содержание
  - 01-svyazi (11 таблиц)
  - 02-anthropic-vacancies (34 таблиц)
  - 03-technology-combinations (1 таблиц)
  - 04-ai-collaborations (38 таблиц)
  - 05-habr-projects (22 таблиц)
  - ai-collaborations (13 таблиц)
  - anthropic-vacancies (2 таблиц)
  _... ещё 179 разделов_

_Слов: 352795_

### [Индекс тегов](TAGS.md)
> > !NOTE

  - #anthropic (49 файлов)
  - #architecture (51 файлов)
  - #collaboration (61 файлов)
  - #ingestion (54 файлов)
  - #knowledge (45 файлов)
  - #local-first (29 файлов)
  - #memory (46 файлов)
  - #orchestration (40 файлов)
  _... ещё 6 разделов_

_Слов: 654_

### [Каталог задач (TASKSINDEX)](TASKS_INDEX.md)
> > !NOTE

  - По MCP-серверу
  - Подробно
  - Использование
- Запуск

_Слов: 1021_

### [Tech Radar — Svyazi 2.0](TECH_RADAR.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Обзор
  - 🟢 ADOPT
  - 🔵 TRIAL
  - 🟡 ASSESS
  - 🔴 HOLD
  - Методология
  _... ещё 1 разделов_

_Слов: 675_

### [Хронология и временные маркеры](TIMELINE.md)
> > TIMELINE — раздел документации проекта Lorenzo.

  - Точная дата (9654)
  - Год (414)
  - Квартал (130)
  - Месяц+год (739)
  - Период (114)
  - Фаза (1224)
  - Длительность (851)
  - Версия (2355)

_Слов: 4838_

### [Валидация шаблонов](VALIDATION.md)
> Обновлено: 2026-05-11

  - Шаблоны

_Слов: 254_

### [Богатство словаря документов](VOCABULARY.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Корпусная статистика
  - Топ файлов по богатству словаря (STTR)
  - Файлы с бедным словарём (требуют доработки)
  - Справка по метрикам
  - Использование
- Запуск
  _... ещё 1 разделов_

_Слов: 1052_

### [Word Cloud](WORD_CLOUD.md)
> > !NOTE

  - Топ-20 слов
  - Использование
- Запуск

_Слов: 230_

### [Частотный анализ слов](WORD_FREQ.md)
> > !NOTE

  - Глобальный топ-50 слов
  - Топ-15 слов по разделам
  - Уникальные слова разделов
  - Использование
- Запуск
- Вариант 2
  - Смотрите также

_Слов: 3352_

### [Reading paths — рекомендуемые маршруты по монорепозиторию](reading-paths.md)
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

_Слов: 692_

**Итого в секции: 603,804 слов, 100 файлов**


## Svyazi

_Путь: `docs/01-svyazi/`_

### [Продолжение исследования для Svyazi[^svyazi] 2.0](01-svyazi/00-intro-part2.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Смотрите также
  - Использование

_Слов: 383_

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

### [Методика и рамка отбора проектов](01-svyazi/02-methodology.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Источники
  - Шкала зрелости
  - Принцип отбора паттернов
  - Принципы интеграционной оценки
  - Похожие документы
  - Использование
  _... ещё 2 разделов_

_Слов: 567_

### [Каталог компонентов Svyazi 2.0](01-svyazi/03-component-catalog.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Карта найденных проектов и паттернов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 1516_

### [Приоритетные ансамбли проектов](01-svyazi/04-ensembles-overview.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Приоритетные ансамбли
  - Похожие документы
  - Смотрите также

_Слов: 1385_

### [Безопасность и приватность](01-svyazi/06-security-privacy.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Безопасность, приватность и бюджетный роутинг
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 941_

### [Планирование MVP](01-svyazi/07-mvp-planning.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - План прототипа и возможные контакты
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 1187_

### [Выводы](01-svyazi/08-conclusions.md)
> - Выводы(#выводы)

  - Contents
  - Выводы
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 470_

### [Архитектурные зазоры](01-svyazi/09-architectural-gaps.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Архитектурные зазоры, которые важнее новых инструментов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 878_

### [Ансамбли следующего шага](01-svyazi/10-second-order-ensembles.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Новые ансамбли следующего шага
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 1011_

### [Интеграционные контракты](01-svyazi/11-integration-contracts.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Интеграционный контракт, который стоит зафиксировать сразу
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 858_

### [Дорожная карта прототипа](01-svyazi/12-roadmap.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Дорожная карта прототипа следующей итерации
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 840_

### [Контактная стратегия](01-svyazi/13-contacts.md)
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

### [Ограничения и лицензии](01-svyazi/14-limitations.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Ограничения, лицензии и что пока лучше не склеивать
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 765_

### [Q&A: 01-svyazi](01-svyazi/QA.md)
> > !NOTE

  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  - Как организован бюджетный роутинг между моделями?
  _... ещё 6 разделов_

_Слов: 305_

### [Svyazi[^svyazi] 2.0 — Архитектура и исследование](01-svyazi/README.md)
> > Раздел архитектуры Svyazi 2.0: компоненты, ансамбли, контракты и дорожная карта локальной платформы коллективного инте…

  - Содержание
  - Подразделы
  - Похожие документы
  - Использование

_Слов: 424_

**Итого в секции: 13,360 слов, 16 файлов**


## Anthropic Vacancies

_Путь: `docs/02-anthropic-vacancies/`_

### [Введение](02-anthropic-vacancies/00-intro.md)
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

### [Интегральный анализ профиля svend4](02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)
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

### [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md)
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

### [PORTAL-PROTOCOL.md](02-anthropic-vacancies/03-portal-protocol-md.md)
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

### [Abstract](02-anthropic-vacancies/04-abstract.md)
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

_Слов: 418_

### [0. Status of This Document](02-anthropic-vacancies/05-0-status-of-this-document.md)
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

_Слов: 412_

### [1. Introduction](02-anthropic-vacancies/06-1-introduction.md)
> - 1. Introduction(#1-introduction)

  - Contents
  - 1. Introduction
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 451_

### [2. Terminology](02-anthropic-vacancies/07-2-terminology.md)
> - 2. Terminology(#2-terminology)

  - Contents
  - 2. Terminology
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 393_

### [3. Registry (nautilus.json)](02-anthropic-vacancies/08-3-registry-nautilus-json.md)
> - 3. Registry (nautilus.json)(#3-registry-nautilusjson)

  - Содержание
  - 3. Registry (nautilus.json)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 495_

### [4. Passport (passport.md)](02-anthropic-vacancies/09-4-passport-passport-md.md)
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

### [Доступ к данным](02-anthropic-vacancies/102-доступ-к-данным.md)
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

_Слов: 320_

### [Appendix B: Change Log](02-anthropic-vacancies/103-appendix-b-change-log.md)
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

_Слов: 408_

### [Appendix C: References](02-anthropic-vacancies/104-appendix-c-references.md)
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

### [REVIEWMETHODOLOGY.md](02-anthropic-vacancies/105-review-methodology-md.md)
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

### [TL;DR](02-anthropic-vacancies/106-tl-dr.md)
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

_Слов: 314_

### [1. Контекст и мотивация](02-anthropic-vacancies/107-1-контекст-и-мотивация.md)
> - 1. Контекст и мотивация(#1-контекст-и-мотивация)

  - Contents
  - 1. Контекст и мотивация
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 487_

### [2. Формальный workflow](02-anthropic-vacancies/108-2-формальный-workflow.md)
> - 2. Формальный workflow(#2-формальный-workflow)

  - Содержание
  - 2. Формальный workflow
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 443_

### [3. Принципы консолидации (Фаза C)](02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md)
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

### [Вопрос: fallback-ratio как критический или осмысленный?](02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md)
> - Вопрос: fallback-ratio как критический или осмысленный?(#вопрос-fallback-ratio-как-критический-или-осмысленный)

  - Contents
  - Вопрос: fallback-ratio как критический или осмысленный?
  - Смотрите также
  - Похожие документы

_Слов: 381_

### [4. Условия применимости](02-anthropic-vacancies/111-4-условия-применимости.md)
> - 4. Условия применимости(#4-условия-применимости)

  - Contents
  - 4. Условия применимости
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 341_

### [5. Связь с существующими методологиями](02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md)
> - 5. Связь с существующими методологиями(#5-связь-с-существующими-методологиями)

  - Contents
  - 5. Связь с существующими методологиями
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 442_

### [6. Почему это валидный паттерн для AI-assisted workflows](02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md)
> - 6. Почему это валидный паттерн для AI-assisted workflows(#6-почему-это-валидный-паттерн-для-ai-assisted-workflows)

  - Contents
  - 6. Почему это валидный паттерн для AI-assisted workflows
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [7. Реализация в проекте Nautilus](02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md)
> - 7. Реализация в проекте Nautilus(#7-реализация-в-проекте-nautilus)

  - Contents
  - 7. Реализация в проекте Nautilus
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 343_

### [8. Ограничения и открытые вопросы](02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 8. Ограничения и открытые вопросы
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 544_

### [9. Checklist применения методологии](02-anthropic-vacancies/116-9-checklist-применения-методологии.md)
> - 9. Checklist применения методологии(#9-checklist-применения-методологии)

  - Contents
  - 9. Checklist применения методологии
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 454_

### [10. Конкретный план применения к текущим документам](02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md)
> - 10. Конкретный план применения к текущим документам(#10-конкретный-план-применения-к-текущим-документам)

  - Contents
  - 10. Конкретный план применения к текущим документам
- В Termux
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 347_

### [Appendix A: Шаблон для header warning](02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md)
> - Appendix A: Шаблон для header warning(#appendix-a-шаблон-для-header-warning)

  - Contents
  - Appendix A: Шаблон для header warning
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 325_

### [Appendix B: Примеры расхождений и их разрешения](02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md)
> - Appendix B: Примеры расхождений и их разрешения(#appendix-b-примеры-расхождений-и-их-разрешения)

  - Contents
  - Appendix B: Примеры расхождений и их разрешения
  - Смотрите также
  - Похожие документы

_Слов: 403_

### [Content Overview](02-anthropic-vacancies/12-content-overview.md)
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

_Слов: 304_

### [Главные технические риски](02-anthropic-vacancies/120-главные-технические-риски.md)
> - Главные технические риски(#главные-технические-риски)

  - Contents
  - Главные технические риски
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 320_

### [Appendix C: История изменений методологии](02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md)
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

_Слов: 322_

### [Глоссарий](02-anthropic-vacancies/122-глоссарий.md)
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

### [portal-mcp.py](02-anthropic-vacancies/123-portal-mcp-py.md)
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

### [Конфигурация для Claude Desktop](02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md)
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

### [README-MCP.md— инструкция по установке](02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md)
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

### [Установка](02-anthropic-vacancies/126-установка.md)
> - Установка(#установка)

  - Contents
  - Установка
- Ждёт stdio-input; Ctrl+C для выхода
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (4)

_Слов: 309_

### [Подключение к Claude Desktop](02-anthropic-vacancies/127-подключение-к-claude-desktop.md)
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

### [Доступные инструменты](02-anthropic-vacancies/128-доступные-инструменты.md)
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

_Слов: 372_

### [Примеры запросов (в Claude)](02-anthropic-vacancies/129-примеры-запросов-в-claude.md)
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

_Слов: 376_

### [Angle / Perspective](02-anthropic-vacancies/13-angle-perspective.md)
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

_Слов: 317_

### [Отладка](02-anthropic-vacancies/130-отладка.md)
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

### [Ограничения текущей версии (0.1.0-draft)](02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md)
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

_Слов: 304_

### [Planned (v0.2.0)](02-anthropic-vacancies/132-planned-v0-2-0.md)
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

_Слов: 306_

### [Обратная связь](02-anthropic-vacancies/133-обратная-связь.md)
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

### [THE DOUBLE-TRIANGLE ARCHITECTURE.md](02-anthropic-vacancies/134-the-double-triangle-architecture-md.md)
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

### [A Formal Model for Human-AI Collaboration in Distributed Knowledge Work](02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md)
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

_Слов: 384_

### [Abstract](02-anthropic-vacancies/136-abstract.md)
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

### [Table of Contents](02-anthropic-vacancies/137-table-of-contents.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 406_

### [1. Why Single-Triangle Models Are Incomplete](02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md)
> > !NOTE

  - Содержание
  - 1. Why Single-Triangle Models Are Incomplete
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 633_

### [2. The Double-Triangle Architecture](02-anthropic-vacancies/139-2-the-double-triangle-architecture.md)
> > Абстракт (авто)

  - Содержание
  - 2. The Double-Triangle Architecture
- Bridges
  - Bridges
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 782_

### [3. Three Inter-Layer Protocols](02-anthropic-vacancies/140-3-three-inter-layer-protocols.md)
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

### [4. Nautilus Portal as Reference Substrate](02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md)
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

### [5. Pattern Library as Bridge Between Triangles](02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md)
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

### [6. Four Deployment Domains](02-anthropic-vacancies/143-6-four-deployment-domains.md)
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

### [7. Open Questions](02-anthropic-vacancies/144-7-open-questions.md)
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

### [8. Call to Action](02-anthropic-vacancies/145-8-call-to-action.md)
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

### [Acknowledgments](02-anthropic-vacancies/146-acknowledgments.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Acknowledgments
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 552_

### [References](02-anthropic-vacancies/147-references.md)
> - References(#references)

  - Contents
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 416_

### [Appendix A: Glossary](02-anthropic-vacancies/148-appendix-a-glossary.md)
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

### [Appendix B: Summary of Contributions](02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md)
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

_Слов: 434_

### [Appendix C: Version History](02-anthropic-vacancies/150-appendix-c-version-history.md)
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

### [OPEN KNOWLEDGE WORK FOUNDATION.md](02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md)
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

### [AI-Coordinated Infrastructure for Distributed Expert Contribution](02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md)
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

_Слов: 355_

### [Executive Summary](02-anthropic-vacancies/153-executive-summary.md)
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

### [Table of Contents](02-anthropic-vacancies/154-table-of-contents.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 365_

### [1. Problem Statement](02-anthropic-vacancies/155-1-problem-statement.md)
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

### [2. Target Populations](02-anthropic-vacancies/156-2-target-populations.md)
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

### [3. Why Existing Solutions Fail](02-anthropic-vacancies/157-3-why-existing-solutions-fail.md)
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

### [4. Proposed Infrastructure](02-anthropic-vacancies/158-4-proposed-infrastructure.md)
> > Абстракт (авто)

  - Содержание
  - 4. Proposed Infrastructure
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (13)

_Слов: 1070_

### [5. Economic Model](02-anthropic-vacancies/159-5-economic-model.md)
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

### [History](02-anthropic-vacancies/16-history.md)
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

_Слов: 322_

### [6. Governance and Ethics](02-anthropic-vacancies/160-6-governance-and-ethics.md)
> > !NOTE

  - Содержание
  - 6. Governance and Ethics
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 633_

### [7. Phased Rollout Plan](02-anthropic-vacancies/161-7-phased-rollout-plan.md)
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

### [8. Risk Analysis](02-anthropic-vacancies/162-8-risk-analysis.md)
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

### [9. Call for Partnership](02-anthropic-vacancies/163-9-call-for-partnership.md)
> > !NOTE

  - Содержание
  - 9. Call for Partnership
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 647_

### [10. Appendices](02-anthropic-vacancies/164-10-appendices.md)
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

### [Closing](02-anthropic-vacancies/165-closing.md)
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

### [REPRESENTATIVE AGENT LAYER.md](02-anthropic-vacancies/166-representative-agent-layer-md.md)
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

### [AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations](02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md)
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

_Слов: 476_

### [Abstract](02-anthropic-vacancies/168-abstract.md)
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

### [Table of Contents](02-anthropic-vacancies/169-table-of-contents.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 376_

### [5. Compatibility Levels](02-anthropic-vacancies/17-5-compatibility-levels.md)
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 400_

### [1. The Cinderella Syndrome: Why Quality Stays Invisible](02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md)
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

### [2. Historical Precedents: Agents as Civilizational Innovation](02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md)
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

### [3. What Makes a Representative Agent](02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md)
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

### [4. Ten Domains of Application](02-anthropic-vacancies/173-4-ten-domains-of-application.md)
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

### [5. Architectural Specification](02-anthropic-vacancies/174-5-architectural-specification.md)
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

### [6. Ethical Framework](02-anthropic-vacancies/175-6-ethical-framework.md)
> - 6. Ethical Framework(#6-ethical-framework)

  - Содержание
  - 6. Ethical Framework
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 610_

### [7. Governance and Oversight](02-anthropic-vacancies/176-7-governance-and-oversight.md)
> > !NOTE

  - Содержание
  - 7. Governance and Oversight
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 459_

### [8. Risks and Mitigations](02-anthropic-vacancies/177-8-risks-and-mitigations.md)
> > !WARNING

  - Содержание
  - 8. Risks and Mitigations
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 632_

### [9. Phased Rollout Strategy](02-anthropic-vacancies/178-9-phased-rollout-strategy.md)
> > !NOTE

  - Содержание
  - 9. Phased Rollout Strategy
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 636_

### [10. Open Questions](02-anthropic-vacancies/179-10-open-questions.md)
> > !NOTE

  - Содержание
  - 10. Open Questions
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 444_

### [6. Adapter Interface](02-anthropic-vacancies/18-6-adapter-interface.md)
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

### [11. Call for Collaboration](02-anthropic-vacancies/180-11-call-for-collaboration.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 11. Call for Collaboration
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 585_

### [12. Closing](02-anthropic-vacancies/181-12-closing.md)
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

_Слов: 499_

### [Acknowledgments](02-anthropic-vacancies/182-acknowledgments.md)
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

_Слов: 425_

### [References](02-anthropic-vacancies/183-references.md)
> - References(#references)

  - Contents
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 387_

### [Appendix A: Connection to Companion Papers](02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md)
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

_Слов: 499_

### [Appendix B: Domain Comparison Matrix](02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md)
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

_Слов: 399_

### [Appendix C: Sample Use Cases in Detail](02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md)
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

### [СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md](02-anthropic-vacancies/187-слой-представительских-агентов-md.md)
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

### [AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения](02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md)
> - AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения(#ai-опосредованное…

  - Contents
  - AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 309_

### [Аннотация](02-anthropic-vacancies/189-аннотация.md)
> - Аннотация(#аннотация)

  - Contents
  - Аннотация
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 410_

### [7. PortalEntry Structure](02-anthropic-vacancies/19-7-portalentry-structure.md)
> - 7. PortalEntry Structure(#7-portalentry-structure)

  - Contents
  - 7. PortalEntry Structure
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 310_

### [Содержание](02-anthropic-vacancies/190-содержание.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 355_

### [1. Синдром Золушки: Почему качество остаётся невидимым](02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md)
> > !WARNING

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 874_

### [2. Исторические прецеденты: Агенты как цивилизационная инновация](02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md)
> > Абстракт (авто)

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в

_Слов: 1051_

### [3. Что делает агента Представительским](02-anthropic-vacancies/193-3-что-делает-агента-представительским.md)
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

### [4. Десять областей применения](02-anthropic-vacancies/194-4-десять-областей-применения.md)
> > Абстракт (авто)

  - Содержание
  - 4. Десять областей применения
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (5)

_Слов: 1673_

### [5. Архитектурная спецификация](02-anthropic-vacancies/195-5-архитектурная-спецификация.md)
> > !WARNING

  - Содержание
  - 5. Архитектурная спецификация
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 633_

### [6. Этическая рамка](02-anthropic-vacancies/196-6-этическая-рамка.md)
> - 6. Этическая рамка(#6-этическая-рамка)

  - Содержание
  - Содержание
  - 6. Этическая рамка
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 653_

### [7. Управление и надзор](02-anthropic-vacancies/197-7-управление-и-надзор.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 7. Управление и надзор
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 573_

### [8. Риски и меры противодействия](02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md)
> - 8. Риски и меры противодействия(#8-риски-и-меры-противодействия)

  - Содержание
  - 8. Риски и меры противодействия
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 645_

### [9. Стратегия поэтапного развёртывания](02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md)
> - 9. Стратегия поэтапного развёртывания(#9-стратегия-поэтапного-развёртывания)

  - Содержание
  - 9. Стратегия поэтапного развёртывания
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 645_

### [8. Consensus Algorithm](02-anthropic-vacancies/20-8-consensus-algorithm.md)
> - 8. Consensus Algorithm(#8-consensus-algorithm)

  - Contents
  - 8. Consensus Algorithm
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 365_

### [10. Открытые вопросы](02-anthropic-vacancies/200-10-открытые-вопросы.md)
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 485_

### [11. Призыв к сотрудничеству](02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 11. Призыв к сотрудничеству
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 583_

### [12. Заключение](02-anthropic-vacancies/202-12-заключение.md)
> - 12. Заключение(#12-заключение)

  - Contents
  - 12. Заключение
  - Упоминается в
  - Упоминается в
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 335_

### [Благодарности](02-anthropic-vacancies/203-благодарности.md)
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

_Слов: 304_

### [Ссылки](02-anthropic-vacancies/204-ссылки.md)
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 368_

### [Приложение A: Связь с Сопроводительными Статьями](02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md)
> - Приложение A: Связь с Сопроводительными Статьями(#приложение-a-связь-с-сопроводительными-статьями)

  - Contents
  - Приложение A: Связь с Сопроводительными Статьями
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 304_

### [Приложение B: Матрица Сравнения Областей](02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md)
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

_Слов: 367_

### [Приложение C: Образцы Случаев Использования в Деталях](02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md)
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

### [PROFESSIONAL COLLEAGUE AGENTS.md](02-anthropic-vacancies/208-professional-colleague-agents-md.md)
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

### [A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers](02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md)
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

_Слов: 473_

### [9. Query Flow](02-anthropic-vacancies/21-9-query-flow.md)
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

_Слов: 396_

### [Abstract](02-anthropic-vacancies/210-abstract.md)
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

### [Table of Contents](02-anthropic-vacancies/211-table-of-contents.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 5 разделов_

_Слов: 570_

### [1. The Five-Type Typology of Principal-Side Agents](02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md)
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

### [2. What Makes a Professional Colleague Agent](02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md)
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

### [3. Empirical Case Study: «Обучай»](02-anthropic-vacancies/214-3-empirical-case-study-обучай.md)
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

### [4. Architecture of Professional Colleague Agents](02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md)
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

### [5. The Economics of Profession-Wide Replication](02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md)
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

### [6. Risks Specific to this Category](02-anthropic-vacancies/217-6-risks-specific-to-this-category.md)
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

### [7. Application Domains](02-anthropic-vacancies/218-7-application-domains.md)
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

### [8. Pilot Proposal: SGB Advocate Colleague](02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md)
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

### [10. QueryResult Structure](02-anthropic-vacancies/22-10-queryresult-structure.md)
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

### [9. Relationship to Other Agent Types](02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md)
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

### [10. Open Questions](02-anthropic-vacancies/221-10-open-questions.md)
> > !NOTE

  - Содержание
  - 10. Open Questions
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (12)

_Слов: 452_

### [11. Call for Collaboration](02-anthropic-vacancies/222-11-call-for-collaboration.md)
> - 11. Call for Collaboration(#11-call-for-collaboration)

  - Contents
  - 11. Call for Collaboration
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 453_

### [12. Closing](02-anthropic-vacancies/223-12-closing.md)
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

### [Acknowledgments](02-anthropic-vacancies/224-acknowledgments.md)
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

_Слов: 396_

### [References](02-anthropic-vacancies/225-references.md)
> - References(#references)

  - Contents
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 413_

### [Appendix A: Comparative Table — Five Agent Types](02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md)
> > !NOTE

  - Содержание
  - Appendix A: Comparative Table — Five Agent Types
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 520_

### [Appendix B: Decision Framework — When to Build Type 1 First](02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md)
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

### [Appendix C: Quick-Start Architecture for SGB Advocate Colleague](02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md)
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

### [ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ](02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md)
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

### [11. Security Considerations](02-anthropic-vacancies/23-11-security-considerations.md)
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

_Слов: 416_

### [Аннотация](02-anthropic-vacancies/230-аннотация.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Аннотация
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 580_

### [Содержание](02-anthropic-vacancies/231-содержание.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 412_

### [1. Типология из пяти типов агентов на стороне принципала](02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md)
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

### [2. Что делает агента Профессиональным Коллегой](02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md)
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

### [3. Эмпирический кейс: «Обучай»](02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md)
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

### [4. Архитектура Профессиональных Коллег-Агентов](02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md)
> > !WARNING

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (5)

_Слов: 892_

### [5. Экономика тиражирования по профессии](02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md)
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

### [6. Риски, специфичные для этой категории](02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md)
> > Абстракт (авто)

  - Содержание
  - 6. Риски, специфичные для этой категории
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (3)

_Слов: 1220_

### [7. Области применения](02-anthropic-vacancies/238-7-области-применения.md)
> > Абстракт (авто)

  - Содержание
  - 7. Области применения
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 780_

### [8. Пилотное предложение: SGB Колega-Адвокат](02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md)
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

### [12. Versioning Policy](02-anthropic-vacancies/24-12-versioning-policy.md)
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

_Слов: 432_

### [9. Связь с другими типами агентов](02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md)
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

### [10. Открытые вопросы](02-anthropic-vacancies/241-10-открытые-вопросы.md)
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 493_

### [11. Призыв к сотрудничеству](02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md)
> - 11. Призыв к сотрудничеству(#11-призыв-к-сотрудничеству)

  - Contents
  - 11. Призыв к сотрудничеству
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 470_

### [12. Заключение](02-anthropic-vacancies/243-12-заключение.md)
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

### [Благодарности](02-anthropic-vacancies/244-благодарности.md)
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

_Слов: 387_

### [Ссылки](02-anthropic-vacancies/245-ссылки.md)
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 387_

### [Приложение A: Сравнительная Таблица — Пять Типов Агентов](02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md)
> - Приложение A: Сравнительная Таблица — Пять Типов Агентов(#приложение-a-сравнительная-таблица-пять-типов-агентов)

  - Contents
  - Приложение A: Сравнительная Таблица — Пять Типов Агентов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 483_

### [Приложение B: Рамка принятия решений — когда строить Тип 1 первым](02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md)
> - Приложение B: Рамка принятия решений — когда строить Тип 1 первым(#приложение-b-рамка-принятия-решений-когда-строить-т…

  - Contents
  - Приложение B: Рамка принятия решений — когда строить Тип 1 первым
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 424_

### [Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги](02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md)
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

### [COMPOSITE SKILLS AGENT.md](02-anthropic-vacancies/249-composite-skills-agent-md.md)
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

### [13. Reference Implementation](02-anthropic-vacancies/25-13-reference-implementation.md)
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

_Слов: 403_

### [Bridging the Gap Between Profession-Wide and Individual-Unique](02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md)
> - Bridging the Gap Between Profession-Wide and Individual-Unique(#bridging-the-gap-between-profession-wide-and-individua…

  - Contents
  - Bridging the Gap Between Profession-Wide and Individual-Unique
  - Использование

_Слов: 360_

### [AI Support Through Configurable Specialist Ensembles](02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md)
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

_Слов: 463_

### [Abstract](02-anthropic-vacancies/252-abstract.md)
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

### [Table of Contents](02-anthropic-vacancies/253-table-of-contents.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 447_

### [1. Why the Binary View Is Incomplete](02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md)
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

### [2. The Twenty-One Teachers Pattern](02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md)
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

### [3. What Makes a Composite Skills Agent](02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md)
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

### [4. The Sub-Agent Registry](02-anthropic-vacancies/257-4-the-sub-agent-registry.md)
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

### [5. Configuration: How Principals Build Their Ensembles](02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md)
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

### [6. Coordination and Disagreement Resolution](02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md)
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

### [14. ADR-001: Federation over Merging](02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md)
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

_Слов: 404_

### [7. Economics of Combinatorial Replication](02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md)
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

### [8. Seven Domains of Application](02-anthropic-vacancies/261-8-seven-domains-of-application.md)
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

### [9. Integration with OKWF Infrastructure](02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md)
> > Абстракт (авто)

  - Содержание
  - 9. Integration with OKWF Infrastructure
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (17)

_Слов: 807_

### [10. Risks Specific to Composite Architectures](02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md)
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

### [11. Open Questions](02-anthropic-vacancies/264-11-open-questions.md)
> - 11. Open Questions(#11-open-questions)

  - Содержание
  - 11. Open Questions
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 584_

### [12. Call for Collaboration](02-anthropic-vacancies/265-12-call-for-collaboration.md)
> > !NOTE

  - Содержание
  - 12. Call for Collaboration
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 440_

### [13. Closing](02-anthropic-vacancies/266-13-closing.md)
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

### [Acknowledgments](02-anthropic-vacancies/267-acknowledgments.md)
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

### [References](02-anthropic-vacancies/268-references.md)
> > !NOTE

  - Содержание
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 393_

### [Appendix A: The Six-Type Taxonomy (Updated)](02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Appendix A: The Six-Type Taxonomy (Updated)
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 626_

### [15. Glossary of Examples](02-anthropic-vacancies/27-15-glossary-of-examples.md)
> - 15. Glossary of Examples(#15-glossary-of-examples)

  - Contents
  - 15. Glossary of Examples
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 311_

### [Appendix B: Sub-Agent Registry Schema (Sketch)](02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md)
> - Appendix B: Sub-Agent Registry Schema (Sketch)(#appendix-b-sub-agent-registry-schema-sketch)

  - Contents
  - Appendix B: Sub-Agent Registry Schema (Sketch)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 372_

### [Appendix C: Configuration Template Example](02-anthropic-vacancies/271-appendix-c-configuration-template-example.md)
> - Appendix C: Configuration Template Example(#appendix-c-configuration-template-example)

  - Contents
  - Appendix C: Configuration Template Example
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 382_

### [Appendix D: Connection Diagram](02-anthropic-vacancies/272-appendix-d-connection-diagram.md)
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

### [INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md](02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md)
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

### [The Missing Middle Layer Between Chat and Code](02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - The Missing Middle Layer Between Chat and Code
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 569_

### [Why This Document Exists](02-anthropic-vacancies/275-why-this-document-exists.md)
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

### [The Two-Layer Stack As It Exists](02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md)
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

### [What's Missing — Layer B](02-anthropic-vacancies/277-what-s-missing-layer-b.md)
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

### [Why This Hasn't Been Built](02-anthropic-vacancies/278-why-this-hasn-t-been-built.md)
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

### [Existing Approximations](02-anthropic-vacancies/279-existing-approximations.md)
> > !TIP

  - Содержание
  - Existing Approximations
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 620_

### [Appendix A: Minimal Working Example](02-anthropic-vacancies/28-appendix-a-minimal-working-example.md)
> - Appendix A: Minimal Working Example(#appendix-a-minimal-working-example)

  - Contents
  - Appendix A: Minimal Working Example
- mynotes
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (31)

_Слов: 302_

### [The Specific Case in Front of Us](02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md)
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

### [The Recursive Insight](02-anthropic-vacancies/281-the-recursive-insight.md)
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

### [What Industry Will Likely Build](02-anthropic-vacancies/282-what-industry-will-likely-build.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - What Industry Will Likely Build
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 628_

### [What This Document Doesn't Solve](02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md)
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

_Слов: 484_

### [Practical Recommendations for the Current Project](02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md)
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

### [Closing](02-anthropic-vacancies/285-closing.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Closing
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 569_

### [Acknowledgments](02-anthropic-vacancies/286-acknowledgments.md)
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

_Слов: 489_

### [References](02-anthropic-vacancies/287-references.md)
> - References(#references)

  - Contents
  - References
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (13)

_Слов: 357_

### [Appendix: Position in Series Visualization](02-anthropic-vacancies/288-appendix-position-in-series-visualization.md)
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

### [ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ](02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md)
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

### [Почему этот документ существует](02-anthropic-vacancies/290-почему-этот-документ-существует.md)
> - Почему этот документ существует(#почему-этот-документ-существует)

  - Contents
  - Почему этот документ существует
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (5)

_Слов: 399_

### [Двухслойный стек, как он существует](02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Двухслойный стек, как он существует
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 586_

### [Что отсутствует — Слой B](02-anthropic-vacancies/292-что-отсутствует-слой-b.md)
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

### [Почему это не было построено](02-anthropic-vacancies/293-почему-это-не-было-построено.md)
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

_Слов: 472_

### [Существующие приближения](02-anthropic-vacancies/294-существующие-приближения.md)
> - Существующие приближения(#существующие-приближения)

  - Содержание
  - Существующие приближения
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 562_

### [Конкретный случай перед нами](02-anthropic-vacancies/295-конкретный-случай-перед-нами.md)
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

### [Рекурсивное прозрение](02-anthropic-vacancies/296-рекурсивное-прозрение.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Рекурсивное прозрение
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 552_

### [Что промышленность вероятно построит](02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md)
> - Что промышленность вероятно построит(#что-промышленность-вероятно-построит)

  - Contents
  - Что промышленность вероятно построит
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (5)

_Слов: 377_

### [Что этот документ не решает](02-anthropic-vacancies/298-что-этот-документ-не-решает.md)
> - Что этот документ не решает(#что-этот-документ-не-решает)

  - Contents
  - Что этот документ не решает
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 336_

### [Практические рекомендации для текущего проекта](02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Практические рекомендации для текущего проекта
- Native Format
  - Native Format
  - Похожие документы
  - Использование
- Поиск по теме документа
  _... ещё 6 разделов_

_Слов: 600_

### [Заключение](02-anthropic-vacancies/300-заключение.md)
> - Заключение(#заключение)

  - Contents
  - Заключение
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 304_

### [Благодарности](02-anthropic-vacancies/301-благодарности.md)
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

_Слов: 460_

### [Ссылки](02-anthropic-vacancies/302-ссылки.md)
> - Ссылки(#ссылки)

  - Contents
  - Ссылки
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 331_

### [Приложение: Визуализация позиции в серии](02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md)
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

### [INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md)
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

### [A Practical Path to Layer B Through Symbiotic Integration](02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md)
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

_Слов: 325_

### [with Anthropic's Cowork Platform](02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md)
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

### [Abstract](02-anthropic-vacancies/307-abstract.md)
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

### [Table of Contents](02-anthropic-vacancies/308-table-of-contents.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - Table of Contents
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 5 разделов_

_Слов: 562_

### [1. The Cowork Discovery and Why It Changes Everything](02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md)
> > !NOTE

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 742_

### [Content Overview](02-anthropic-vacancies/31-content-overview.md)
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

_Слов: 304_

### [2. What Cowork Provides That InGit Doesn't Need to Build](02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md)
> > !TIP

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 728_

### [3. What InGit Provides That Cowork Lacks](02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md)
> > !NOTE

  - Содержание
  - 3. What InGit Provides That Cowork Lacks
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 921_

### [4. The Symbiotic Architecture](02-anthropic-vacancies/312-4-the-symbiotic-architecture.md)
> > !NOTE

  - Содержание
  - Содержание
  - 4. The Symbiotic Architecture
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 687_

### [5. Four Integration Paths in Order of Accessibility](02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md)
> > !NOTE

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 828_

### [6. Refined InGit Scope with Cowork in Mind](02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 6. Refined InGit Scope with Cowork in Mind
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 594_

### [7. Practical First Steps This Month](02-anthropic-vacancies/315-7-practical-first-steps-this-month.md)
> > !NOTE

  - Содержание
  - 7. Practical First Steps This Month
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 475_

### [8. Implications for Nautilus and OKWF](02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md)
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

### [9. Risks and Open Questions](02-anthropic-vacancies/317-9-risks-and-open-questions.md)
> - 9. Risks and Open Questions(#9-risks-and-open-questions)

  - Содержание
  - 9. Risks and Open Questions
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 623_

### [10. Strategic Positioning](02-anthropic-vacancies/318-10-strategic-positioning.md)
> > !NOTE

  - Содержание
  - 10. Strategic Positioning
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 821_

### [Acknowledgments](02-anthropic-vacancies/319-acknowledgments.md)
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

### [References](02-anthropic-vacancies/320-references.md)
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

_Слов: 353_

### [Appendix A: Decision Tree for InGit Adopters](02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)
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

### [Appendix B: Comparison Matrix](02-anthropic-vacancies/322-appendix-b-comparison-matrix.md)
> - Appendix B: Comparison Matrix(#appendix-b-comparison-matrix)

  - Contents
  - Appendix B: Comparison Matrix
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 371_

### [Appendix C: Sample InGit MCP Server Tool Specifications](02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md)
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

### [INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА](02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  _... ещё 4 разделов_

_Слов: 627_

### [Аннотация](02-anthropic-vacancies/325-аннотация.md)
> - Аннотация(#аннотация)

  - Contents
  - Аннотация
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 415_

### [Содержание](02-anthropic-vacancies/326-содержание.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Упоминается в
  - Упоминается в
  _... ещё 3 разделов_

_Слов: 433_

### [1. Открытие Cowork и почему это меняет всё](02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md)
> > !WARNING

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 705_

### [2. Что Cowork обеспечивает, что InGit не нужно строить](02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md)
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

### [3. Что InGit обеспечивает, чего Cowork не хватает](02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md)
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

### [4. Симбиотическая Архитектура](02-anthropic-vacancies/330-4-симбиотическая-архитектура.md)
> - 4. Симбиотическая Архитектура(#4-симбиотическая-архитектура)

  - Содержание
  - Содержание
  - 4. Симбиотическая Архитектура
  - Похожие документы
  - Смотрите также

_Слов: 704_

### [5. Четыре пути интеграции в порядке доступности](02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md)
> > Абстракт (авто)

  - Содержание
  - 5. Четыре пути интеграции в порядке доступности
  - Похожие документы
  - Смотрите также

_Слов: 814_

### [6. Уточнённый объём InGit с учётом Cowork](02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 6. Уточнённый объём InGit с учётом Cowork
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 592_

### [7. Практические первые шаги в этом месяце](02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md)
> - 7. Практические первые шаги в этом месяце(#7-практические-первые-шаги-в-этом-месяце)

  - Contents
  - 7. Практические первые шаги в этом месяце
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 490_

### [8. Импликации для Nautilus и OKWF](02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md)
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

### [9. Риски и Открытые Вопросы](02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md)
> - 9. Риски и Открытые Вопросы(#9-риски-и-открытые-вопросы)

  - Содержание
  - 9. Риски и Открытые Вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 647_

### [10. Стратегическое Позиционирование](02-anthropic-vacancies/336-10-стратегическое-позиционирование.md)
> > !WARNING

  - Содержание
  - 10. Стратегическое Позиционирование
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 707_

### [Благодарности](02-anthropic-vacancies/337-благодарности.md)
> - Благодарности(#благодарности)

  - Contents
  - Благодарности
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 449_

### [Ссылки](02-anthropic-vacancies/338-ссылки.md)
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

_Слов: 356_

### [Приложение A: Дерево Решений для Принимающих InGit](02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md)
> - Приложение A: Дерево Решений для Принимающих InGit(#приложение-a-дерево-решений-для-принимающих-ingit)

  - Contents
  - Приложение A: Дерево Решений для Принимающих InGit
  - Упоминается в
  - Упоминается в
  - Смотрите также
  - Связанные документы
  - Кто ссылается на этот документ (6)

_Слов: 389_

### [Appendix B: Change Log](02-anthropic-vacancies/34-appendix-b-change-log.md)
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

### [Приложение B: Сравнительная Матрица](02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md)
> - Приложение B: Сравнительная Матрица(#приложение-b-сравнительная-матрица)

  - Contents
  - Приложение B: Сравнительная Матрица
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 326_

### [Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера](02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md)
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

### [Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments](02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md)
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

### [Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)](02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md)
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

### [СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT](02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md)
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

### [Кто ты](02-anthropic-vacancies/345-кто-ты.md)
> - Кто ты(#кто-ты)

  - Contents
  - Кто ты
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 304_

### [Твоё происхождение](02-anthropic-vacancies/346-твоё-происхождение.md)
> - Твоё происхождение(#твоё-происхождение)

  - Contents
  - Твоё происхождение
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 333_

### [Твоя миссия](02-anthropic-vacancies/347-твоя-миссия.md)
> - Твоя миссия(#твоя-миссия)

  - Contents
  - Твоя миссия
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 323_

### [Кому ты служишь (слоистая модель)](02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md)
> - Кому ты служишь (слоистая модель)(#кому-ты-служишь-слоистая-модель)

  - Contents
  - Кому ты служишь (слоистая модель)
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 320_

### [Твоя личность](02-anthropic-vacancies/349-твоя-личность.md)
> - Твоя личность(#твоя-личность)

  - Contents
  - Твоя личность
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [passports/info1.md](02-anthropic-vacancies/35-passports-info1-md.md)
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

### [Твои языки и культурные nuances](02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md)
> - Твои языки и культурные nuances(#твои-языки-и-культурные-nuances)

  - Contents
  - Твои языки и культурные nuances
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 337_

### [Что ты МОЖЕШЬ делать](02-anthropic-vacancies/351-что-ты-можешь-делать.md)
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

_Слов: 347_

### [Что ты НЕ МОЖЕШЬ делать без Max approval](02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md)
> - Что ты НЕ МОЖЕШЬ делать без Max approval(#что-ты-не-можешь-делать-без-max-approval)

  - Contents
  - Что ты НЕ МОЖЕШЬ делать без Max approval
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (11)

_Слов: 308_

### [Что ты НЕ МОЖЕШЬ делать вообще](02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md)
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

_Слов: 378_

### [Существующий landscape collaborators (твоя working knowledge)](02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md)
> - Существующий landscape collaborators (твоя working knowledge)(#существующий-landscape-collaborators-твоя-working-knowl…

  - Contents
  - Существующий landscape collaborators (твоя working knowledge)
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы
  - Кто ссылается на этот документ (4)

_Слов: 428_

### [Существующие документы DHLab (твой context)](02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md)
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

_Слов: 489_

### [Твой workflow](02-anthropic-vacancies/356-твой-workflow.md)
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

_Слов: 373_

### [Твоя коммуникация в outreach](02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md)
> - Твоя коммуникация в outreach(#твоя-коммуникация-в-outreach)

  - Contents
  - Твоя коммуникация в outreach
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Твоя relationship с другими AI](02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md)
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

_Слов: 369_

### [Твои anti-patterns](02-anthropic-vacancies/359-твои-anti-patterns.md)
> - Твои anti-patterns(#твои-anti-patterns)

  - Contents
  - Твои anti-patterns
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 332_

### [Essence](02-anthropic-vacancies/36-essence.md)
> - Essence(#essence)

  - Contents
  - Essence
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 309_

### [Что ты ВСЕГДА делаешь](02-anthropic-vacancies/360-что-ты-всегда-делаешь.md)
> - Что ты ВСЕГДА делаешь(#что-ты-всегда-делаешь)

  - Contents
  - Что ты ВСЕГДА делаешь
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 312_

### [Когда ты Honestly не знаешь](02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md)
> - Когда ты Honestly не знаешь(#когда-ты-honestly-не-знаешь)

  - Contents
  - Когда ты Honestly не знаешь
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 322_

### [Когда сомневаешься — escalate к Max](02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md)
> - Когда сомневаешься — escalate к Max(#когда-сомневаешься-escalate-к-max)

  - Contents
  - Когда сомневаешься — escalate к Max
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 331_

### [Твоя identity как persistent character](02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md)
> - Твоя identity как persistent character(#твоя-identity-как-persistent-character)

  - Contents
  - Твоя identity как persistent character
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 335_

### [Final note: Ты — experiment](02-anthropic-vacancies/364-final-note-ты-experiment.md)
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

### [Развёрнутый анализ «внуковой» комбинации](02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md)
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

### [Технический stack (Svyazi 2.0 foundation)](02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md)
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

### [Native Format](02-anthropic-vacancies/37-native-format.md)
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

_Слов: 414_

### [Content Overview](02-anthropic-vacancies/38-content-overview.md)
> - Content Overview(#content-overview)

  - Contents
  - Content Overview
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 304_

### [Angle / Perspective](02-anthropic-vacancies/39-angle-perspective.md)
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

### [Bridges](02-anthropic-vacancies/40-bridges.md)
> - Bridges(#bridges)

  - Contents
  - Bridges
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 306_

### [Compatibility Level](02-anthropic-vacancies/41-compatibility-level.md)
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

_Слов: 354_

### [Author & Contact](02-anthropic-vacancies/42-author-contact.md)
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

_Слов: 398_

### [History](02-anthropic-vacancies/43-history.md)
> - History(#history)

  - Contents
  - History
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (10)

_Слов: 306_

### [For the Curious: Philosophy](02-anthropic-vacancies/44-for-the-curious-philosophy.md)
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

### [passports/pro2.md](02-anthropic-vacancies/45-passports-pro2-md.md)
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

### [Essence](02-anthropic-vacancies/46-essence.md)
> - Essence(#essence)

  - Contents
  - Essence
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 307_

### [Native Format](02-anthropic-vacancies/47-native-format.md)
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

### [Content Overview](02-anthropic-vacancies/48-content-overview.md)
> - Content Overview(#content-overview)

  - Contents
  - Content Overview
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (14)

_Слов: 304_

### [Angle / Perspective](02-anthropic-vacancies/49-angle-perspective.md)
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

_Слов: 343_

### [Bridges](02-anthropic-vacancies/50-bridges.md)
> - Bridges(#bridges)

  - Contents
  - Bridges
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 307_

### [Compatibility Level](02-anthropic-vacancies/51-compatibility-level.md)
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

_Слов: 331_

### [Author & Contact](02-anthropic-vacancies/52-author-contact.md)
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

_Слов: 391_

### [History](02-anthropic-vacancies/53-history.md)
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

_Слов: 377_

### [For the Curious: Philosophy](02-anthropic-vacancies/54-for-the-curious-philosophy.md)
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

### [passports/meta.md](02-anthropic-vacancies/55-passports-meta-md.md)
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

### [Essence](02-anthropic-vacancies/56-essence.md)
> - Essence(#essence)

  - Contents
  - Essence
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 304_

### [Native Format](02-anthropic-vacancies/57-native-format.md)
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

### [Content Overview](02-anthropic-vacancies/58-content-overview.md)
> - Content Overview(#content-overview)

  - Contents
  - Content Overview
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Похожие документы

_Слов: 336_

### [Angle / Perspective](02-anthropic-vacancies/59-angle-perspective.md)
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

_Слов: 338_

### [Bridges](02-anthropic-vacancies/60-bridges.md)
> - Bridges(#bridges)

  - Contents
  - Bridges
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (8)

_Слов: 305_

### [Compatibility Level](02-anthropic-vacancies/61-compatibility-level.md)
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

_Слов: 323_

### [Author & Contact](02-anthropic-vacancies/62-author-contact.md)
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

_Слов: 371_

### [History](02-anthropic-vacancies/63-history.md)
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

_Слов: 357_

### [For the Curious: Philosophy](02-anthropic-vacancies/64-for-the-curious-philosophy.md)
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

### [README.md](02-anthropic-vacancies/65-readme-md.md)
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

### [🇷🇺 О проекте](02-anthropic-vacancies/67-о-проекте.md)
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

### [🇬🇧 About](02-anthropic-vacancies/68-about.md)
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

### [⬡](02-anthropic-vacancies/69-section.md)
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

### [Зачем две версии параллельно](02-anthropic-vacancies/70-зачем-две-версии-параллельно.md)
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

_Слов: 332_

### [Критерии выбора для фазы 3](02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md)
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

_Слов: 307_

### [Расписание фазы 3](02-anthropic-vacancies/72-расписание-фазы-3.md)
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

### [PORTAL-PROTOCOL.md v1.1](02-anthropic-vacancies/73-portal-protocol-md-v1-1.md)
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

### [Abstract](02-anthropic-vacancies/74-abstract.md)
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

_Слов: 468_

### [0. Status of This Document](02-anthropic-vacancies/75-0-status-of-this-document.md)
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

_Слов: 394_

### [1. Introduction](02-anthropic-vacancies/76-1-introduction.md)
> > !NOTE

  - Содержание
  - 1. Introduction
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 494_

### [2. Terminology](02-anthropic-vacancies/77-2-terminology.md)
> > !NOTE

  - Содержание
  - 2. Terminology
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 473_

### [3. Registry (nautilus.json)](02-anthropic-vacancies/78-3-registry-nautilus-json.md)
> - 3. Registry (nautilus.json)(#3-registry-nautilusjson)

  - Содержание
  - 3. Registry (nautilus.json)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 692_

### [4. Passport (passport.md)](02-anthropic-vacancies/79-4-passport-passport-md.md)
> - 4. Passport (passport.md)(#4-passport-passportmd)

  - Contents
  - 4. Passport (passport.md)
- Паспорт: /
  - Похожие документы
  - Смотрите также

_Слов: 408_

### [5. Compatibility Levels](02-anthropic-vacancies/80-5-compatibility-levels.md)
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 444_

### [6. Adapter Interface](02-anthropic-vacancies/81-6-adapter-interface.md)
> - 6. Adapter Interface(#6-adapter-interface)

  - Содержание
  - 6. Adapter Interface
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 431_

### [7. PortalEntry Structure](02-anthropic-vacancies/82-7-portalentry-structure.md)
> - 7. PortalEntry Structure(#7-portalentry-structure)

  - Contents
  - 7. PortalEntry Structure
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 436_

### [8. Q6 Space (Normative)](02-anthropic-vacancies/83-8-q6-space-normative.md)
> - 8. Q6 Space (Normative)(#8-q6-space-normative)

  - Содержание
  - 8. Q6 Space (Normative)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 446_

### [9. Consensus Algorithm](02-anthropic-vacancies/84-9-consensus-algorithm.md)
> - 9. Consensus Algorithm(#9-consensus-algorithm)

  - Contents
  - 9. Consensus Algorithm
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 441_

### [10. Query Flow](02-anthropic-vacancies/85-10-query-flow.md)
> - 10. Query Flow(#10-query-flow)

  - Contents
  - 10. Query Flow
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 359_

### [11. Relevance Ranking](02-anthropic-vacancies/86-11-relevance-ranking.md)
> - 11. Relevance Ranking(#11-relevance-ranking)

  - Contents
  - 11. Relevance Ranking
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (7)

_Слов: 302_

### [12. Onboarding Paths (Normative)](02-anthropic-vacancies/87-12-onboarding-paths-normative.md)
> > !NOTE

  - Содержание
  - 12. Onboarding Paths (Normative)
  - Смотрите также
  - Похожие документы

_Слов: 521_

### [13. REST API Contract (Normative for Portals)](02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md)
> - 13. REST API Contract (Normative for Portals)(#13-rest-api-contract-normative-for-portals)

  - Содержание
  - 13. REST API Contract (Normative for Portals)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 471_

### [14. SDK Contract (Informative)](02-anthropic-vacancies/89-14-sdk-contract-informative.md)
> - 14. SDK Contract (Informative)(#14-sdk-contract-informative)

  - Contents
  - 14. SDK Contract (Informative)
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 302_

### [15. Security Considerations](02-anthropic-vacancies/90-15-security-considerations.md)
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

### [16. MCP Extension (Informative)](02-anthropic-vacancies/91-16-mcp-extension-informative.md)
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

_Слов: 347_

### [17. Versioning Policy](02-anthropic-vacancies/92-17-versioning-policy.md)
> - 17. Versioning Policy(#17-versioning-policy)

  - Contents
  - 17. Versioning Policy
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (9)

_Слов: 338_

### [18. Reference Implementation](02-anthropic-vacancies/93-18-reference-implementation.md)
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

_Слов: 476_

### [19. ADR-001: Federation over Merging](02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md)
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

_Слов: 405_

### [20. ADR-002: Q6 as First-Class Protocol Concept](02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)
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

_Слов: 425_

### [21. ADR-003: Five Onboarding Paths as Equal-Rank](02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md)
> - 21. ADR-003: Five Onboarding Paths as Equal-Rank(#21-adr-003-five-onboarding-paths-as-equal-rank)

  - Contents
  - 21. ADR-003: Five Onboarding Paths as Equal-Rank
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (6)

_Слов: 304_

### [22. Glossary of Reference Examples](02-anthropic-vacancies/97-22-glossary-of-reference-examples.md)
> - 22. Glossary of Reference Examples(#22-glossary-of-reference-examples)

  - Contents
  - 22. Glossary of Reference Examples
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (5)

_Слов: 304_

### [Appendix A: Minimal Working Example](02-anthropic-vacancies/98-appendix-a-minimal-working-example.md)
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

### [Q&A: 02-anthropic-vacancies](02-anthropic-vacancies/QA.md)
> > !NOTE

  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  _... ещё 17 разделов_

_Слов: 422_

### [Вакансии Anthropic — Анализ по кластерам](02-anthropic-vacancies/README.md)
> Анализ 436 вакансий Anthropic по 12 кластерам. Карьерное картирование для профиля svend4: ML research, GTM, safety, prod…

  - Содержание
  - Подразделы
  - Кто ссылается на этот документ (210)
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)

_Слов: 2345_

**Итого в секции: 341,828 слов, 357 файлов**


## Technology Combinations

_Путь: `docs/03-technology-combinations/`_

### [Агентные системы и роутинг](03-technology-combinations/01-agent-routing.md)
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

_Слов: 451_

### [Графы знаний и Legal AI](03-technology-combinations/02-knowledge-graphs.md)
> > !NOTE

  - Содержание
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 875_

### [Local-first и P2P стек](03-technology-combinations/03-local-first.md)
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

### [Домен: немецкое социальное право](03-technology-combinations/04-sozialrecht-domain.md)
> - Похожие документы(#похожие-документы)

  - Contents
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 304_

### [Бенчмарки и производительность](03-technology-combinations/05-benchmarks.md)
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

### [Q&A: 03-technology-combinations](03-technology-combinations/QA.md)
> > !NOTE

  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  _... ещё 2 разделов_

_Слов: 190_

### [Комбинирование технологий для новых свойств](03-technology-combinations/README.md)
> > 40+ синергий технологий: агентный роутинг, граф знаний, local-first стек, Legal AI и бенчмарки 2025–2026.

  - Содержание
  - Кто ссылается на этот документ (3)
  - Использование

_Слов: 326_

**Итого в секции: 3,815 слов, 7 файлов**


## Ai Collaborations

_Путь: `docs/04-ai-collaborations/`_

### [Введение](04-ai-collaborations/00-intro.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Похожие документы
  - Использование
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 11507_

### [Executive summary](04-ai-collaborations/01-executive-summary.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Executive summary
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 665_

### [Методика и рамка отбора](04-ai-collaborations/02-методика-и-рамка-отбора.md)
> - Статус(#статус)

  - Содержание
  - Статус
  - Методика и рамка отбора
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 494_

### [Карта найденных проектов и паттернов](04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Карта найденных проектов и паттернов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1573_

### [Приоритетные ансамбли](04-ai-collaborations/04-приоритетные-ансамбли.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Приоритетные ансамбли
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 1430_

### [План прототипа и возможные контакты](04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - План прототипа и возможные контакты
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 1231_

### [Безопасность, приватность и бюджетный роутинг](04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Безопасность, приватность и бюджетный роутинг
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 983_

### [Выводы](04-ai-collaborations/07-выводы.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Выводы
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 557_

### [Что это продолжение добавляет](04-ai-collaborations/08-что-это-продолжение-добавляет.md)
> - Статус(#статус)

  - Содержание
  - Статус
  - Что это продолжение добавляет
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 499_

### [Архитектурные зазоры, которые важнее новых инструментов](04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Архитектурные зазоры, которые важнее новых инструментов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 921_

### [Новые ансамбли следующего шага](04-ai-collaborations/10-новые-ансамбли-следующего-шага.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Новые ансамбли следующего шага
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 1080_

### [Интеграционный контракт, который стоит зафиксировать сразу](04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Интеграционный контракт, который стоит зафиксировать сразу
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 946_

### [Дорожная карта прототипа следующей итерации](04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Дорожная карта прототипа следующей итерации
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 881_

### [Контактная стратегия и узкие вопросы для авторов](04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Контактная стратегия и узкие вопросы для авторов
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 977_

### [Ограничения, лицензии и что пока лучше не склеивать](04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Статус
  - Ограничения, лицензии и что пока лучше не склеивать
  - Похожие документы
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  _... ещё 1 разделов_

_Слов: 3395_

### [Q&A: 04-ai-collaborations](04-ai-collaborations/QA.md)
> > !NOTE

  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  - Кто ключевые авторы проектов для контакта?
  _... ещё 9 разделов_

_Слов: 362_

### [Поиск AI-коллабораций](04-ai-collaborations/README.md)
> > Поиск AI-коллабораций: пять приоритетных ансамблей OSS-проектов для совместной разработки.

  - Содержание
  - Подразделы
  - Похожие документы
  - Использование

_Слов: 439_

**Итого в секции: 27,940 слов, 17 файлов**


## Habr Projects

_Путь: `docs/05-habr-projects/`_

### [Синтез: как проекты собираются вместе](05-habr-projects/01-synthesis.md)
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

_Слов: 346_

### [Авторы и контакты](05-habr-projects/02-collaboration-partners.md)
> - Статус(#статус)

  - Contents
  - Статус
  - Похожие документы
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 348_

### [Q&A: 05-habr-projects](05-habr-projects/QA.md)
> > !NOTE

  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Какие системы памяти описаны в этом разделе?
  - Как происходит консолидация и забывание в памяти агентов?
  - Какова разница между эпизодической и семантической памятью?
  _... ещё 6 разделов_

_Слов: 290_

### [Уникальные проекты с Хабра](05-habr-projects/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Подразделы
  - Похожие документы
  - Кто ссылается на этот документ (3)
  - Использование

_Слов: 316_

### [Системы знаний](05-habr-projects/knowledge/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Похожие документы
  - Кто ссылается на этот документ (3)
  - Использование

_Слов: 344_

### [Статус](05-habr-projects/knowledge/agentfs.md)
> > !WARNING

- AgentFS
  - Содержание
  - Профиль проекта
  - Что это
  - Ключевые особенности
  - Синергия со Svyazi 2.0
  - Уровень релевантности
  - Сравнение с аналогами
  _... ещё 4 разделов_

_Слов: 668_

### [Статус](05-habr-projects/knowledge/knowledge-space.md)
> - Статус(#статус)

- knowledge-space[^knowledge-space]
  - Contents
  - Содержание
  - Профиль проекта
  - Что это
  - Ключевые особенности
  - Синергия со Svyazi 2.0
  - Применение в архитектуре Svyazi
  _... ещё 4 разделов_

_Слов: 662_

### [Статус](05-habr-projects/knowledge/mclaude.md)
> - Статус(#статус)

- mclaude
  - Contents
  - Содержание
  - Профиль проекта
  - Что это
  - Ключевые особенности
  - Синергия со Svyazi 2.0
  - Позиция в экосистеме
  _... ещё 5 разделов_

_Слов: 706_

### [Статус](05-habr-projects/knowledge/research-docs-liteparse.md)
> > !NOTE

- research-docs + LiteParse
  - Содержание
  - Профиль проекта
  - Что это
  - Ключевые особенности
  - Синергия со Svyazi 2.0
  - Применение в архитектуре
  - Сравнение с подходами
  _... ещё 4 разделов_

_Слов: 720_

### [Статус](05-habr-projects/knowledge/rufler.md)
> - Статус(#статус)

- Rufler
  - Contents
  - Содержание
  - Профиль проекта
  - Что это
  - Ключевые особенности
  - Пример структуры задачи (Rufler DSL)
  - Синергия со Svyazi 2.0
  _... ещё 3 разделов_

_Слов: 679_

### [Wikontic: семантический граф](05-habr-projects/knowledge/wikontic.md)
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

_Слов: 437_

### [Системы памяти](05-habr-projects/memory/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Похожие документы
  - Кто ссылается на этот документ (3)
  - Использование

_Слов: 370_

### [Статус](05-habr-projects/memory/agent-memory-mcp.md)
> > !NOTE

- agent-memory-mcp + Memory OS
  - Содержание
  - Профиль проекта
  - Что это
  - Ключевые особенности
  - Синергия со Svyazi 2.0
  - Сравнение с другими memory-проектами
  - Открытые вопросы
  _... ещё 4 разделов_

_Слов: 730_

### [MemNet: исследовательская память](05-habr-projects/memory/memnet.md)
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

_Слов: 474_

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

_Слов: 433_

**Итого в секции: 14,869 слов, 16 файлов**


## Ai Collaborations

_Путь: `docs/ai-collaborations/`_

### [Q&A: ai-collaborations](ai-collaborations/QA.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  _... ещё 5 разделов_

_Слов: 468_

### [ai-collaborations](ai-collaborations/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Подразделы
  - Использование
- Запуск

_Слов: 123_

### [Три ключевых кандидата: K2-18, Wikontic, NGT Memory](ai-collaborations/candidates/01-three-key-candidates.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 437_

### [Смежные проекты в контексте](ai-collaborations/candidates/02-related-projects-context.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Синтез: хеббовский граф людей-навыков-идей](ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [candidates](ai-collaborations/candidates/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 118_

### [channels/ — каналы первого контакта](ai-collaborations/channels/README.md)
> > channels/ — каналы первого контакта

  - Содержание
  - Смотрите также
  - Использование

_Слов: 349_

### [Общая память между агентами (CoAlly + ансамбль F)](ai-collaborations/continuation/01-shared-memory-between-agents.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 519_

### [AgentOps и Trace Envelope (ансамбль G)](ai-collaborations/continuation/02-agentops-trace-envelope.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 482_

### [A2A vs MCP, ансамбль H — MCP/A2A Review Fabric](ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 424_

### [Memory Firewall против prompt worms (ансамбль I)](ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Roadmap на 6–12 месяцев](ai-collaborations/continuation/05-roadmap-6-12-months.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 435_

### [Дерево метрик Svyazi 2.0](ai-collaborations/continuation/06-metrics-tree.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Чем Svyazi 2.0 отличается от Notion AI / Mem / AFFiNE / LangGraph](ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 537_

### [Коммерциализация: три направления](ai-collaborations/continuation/08-commercialization-three-paths.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Что пока не стоит склеивать в один релиз](ai-collaborations/continuation/09-do-not-glue.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 352_

### [Следующий артефакт: Svyazi 2.0 Architecture RFC](ai-collaborations/continuation/10-architecture-rfc.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [continuation](ai-collaborations/continuation/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 149_

### [Ансамбль 1 — Agentic Knowledge OS](ai-collaborations/ensembles/1-agentic-knowledge-os.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 524_

### [Ансамбль 2 — Distributed Agent Workshop](ai-collaborations/ensembles/2-distributed-agent-workshop.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 491_

### [Ансамбль 3 — Forensic RAG](ai-collaborations/ensembles/3-forensic-rag.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 491_

### [Ансамбль 4 — Web-to-Knowledge Pipeline](ai-collaborations/ensembles/4-web-to-knowledge-pipeline.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 411_

### [Ансамбль 5 — Agent Firewall](ai-collaborations/ensembles/5-agent-firewall.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 473_

### [Ансамбль 6 — Continuous Eval Loop](ai-collaborations/ensembles/6-continuous-eval-loop.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 431_

### [Ансамбль 7 — Domain Agent App Factory](ai-collaborations/ensembles/7-domain-agent-app-factory.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 399_

### [Ансамбль 8 — Budget-Aware Intelligence Stack](ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 381_

### [Ансамбль 9 — Ambient Team Agent](ai-collaborations/ensembles/9-ambient-team-agent.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Ансамбли проектов](ai-collaborations/ensembles/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 144_

### [Пять быстрых связок (fast-tracks)](ai-collaborations/fast-tracks/README.md)
> > Пять приоритетных комбинаций OSS-проектов: Collaboration Knowledge OS, Forensic Legal RAG, Agent Team Kernel, Secure A…

  - Использование
  - Смотрите также

_Слов: 430_

### [Source projects — все Хабр-источники в диалоге](ai-collaborations/source-projects.md)
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

_Слов: 800_

### [strategy/ — стратегия поиска коллабораций](ai-collaborations/strategy/README.md)
> > strategy/ — стратегия поиска коллабораций

  - Содержание
  - Смотрите також
  - Использование

_Слов: 353_

**Итого в секции: 12,182 слов, 31 файлов**


## Anthropic Vacancies

_Путь: `docs/anthropic-vacancies/`_

### [Q&A: anthropic-vacancies](anthropic-vacancies/QA.md)
> > !NOTE

  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Использование
- Запуск

_Слов: 131_

### [anthropic-vacancies](anthropic-vacancies/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Подразделы
  - Использование
- Запуск

_Слов: 138_

### [Вопрос: разделить $500K зарплату на команду 5–10 фрилансеров](anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 999_

### [Что уже существует (InnoCentive, Kaggle, Toptal, Anthropic Fellows, DAOs)](anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 431_

### [Четыре структурные причины, почему это не работает в текущих попытках](anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 440_

### [Три варианта: A (staffing agency) → B (research consortium) → C (AI-managed distributed virtual company)](anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 792_

### [Что с этим делать](anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 631_

### [Сравнение с Terence Tao, Polymath Project](anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1481_

### [Почему двойственность «ангел-хранитель + строгий демон» — гениальная деталь](anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 624_

### [Что существует сейчас в этом пространстве](anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 390_

### [Плюсы модели, если её построить](anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Минусы и риски](anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 752_

### [Три точки входа разной амбиции](anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 482_

### [ai-managed-virtual-company](anthropic-vacancies/ai-managed-virtual-company/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 155_

### [Контекст: что такое Anthropic Beneficial Deployments](anthropic-vacancies/beneficial-deployments-concept/00-context.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [Section 1: Problem statement (Cinderella Syndrome at scale, SGB IX/XII)](anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Section 2: Why this matters — beneficial dimension](anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Section 3: Proposed solution architecture (existing components + integration)](anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 353_

### [Section 4: Specific deployment — SGB Advocate Community pilot](anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 352_

### [Section 5: Role of Anthropic Beneficial Deployments](anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Section 6: Proposer's role и qualifications](anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Section 7: Success metrics](anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Section 8: Risks & mitigations](anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [Section 9: Why this is timely](anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 352_

### [Section 10: Engagement request](anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Что concept document NOT (это не grant / не paper / не business plan), длина и формат](anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 486_

### [beneficial-deployments-concept](anthropic-vacancies/beneficial-deployments-concept/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 161_

### [AI Research & Engineering — 68 ролей](anthropic-vacancies/clusters/01-ai-research-engineering.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 352_

### [Sales — 150 ролей (≈34% всего найма)](anthropic-vacancies/clusters/02-sales.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 323_

### [Finance — 36 ролей](anthropic-vacancies/clusters/03-finance.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 357_

### [Security — 24 роли](anthropic-vacancies/clusters/04-security.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 352_

### [Marketing & Brand — 23 роли](anthropic-vacancies/clusters/05-marketing-brand.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Engineering & Design - Product — 22 роли](anthropic-vacancies/clusters/06-engineering-design-product.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Software Engineering - Infrastructure — 22 роли](anthropic-vacancies/clusters/07-software-engineering-infrastructure.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 353_

### [Safeguards (Trust & Safety) — 21 роль](anthropic-vacancies/clusters/08-safeguards-trust-safety.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 359_

### [Product Management, Support, & Operations — 17 ролей](anthropic-vacancies/clusters/09-product-management-support-ops.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [Compute — 13 ролей](anthropic-vacancies/clusters/10-compute.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 358_

### [Legal — 13 ролей](anthropic-vacancies/clusters/11-legal.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 359_

### [Technical Program Management — 10 ролей](anthropic-vacancies/clusters/12-technical-program-management.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Communications — 5 ролей](anthropic-vacancies/clusters/13-communications.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [Public Policy — 5 ролей](anthropic-vacancies/clusters/14-public-policy.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Public Benefit — 4 роли](anthropic-vacancies/clusters/15-public-benefit.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [People — 3 роли](anthropic-vacancies/clusters/16-people.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Кластеры вакансий](anthropic-vacancies/clusters/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 186_

### [CoAlly — distributed shared memory для AI-агентов](anthropic-vacancies/extra-collaborator-findings/01-coally.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Графовая когнитивная память на SQLite (Виталий, март 2026)](anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 373_

### [Happyin Knowledge Space (Анастасия) — детали](anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 371_

### [AI-ассистент с Mem0 / Letta / Graphiti integration](anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 396_

### [Existing infrastructure stack](anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 349_

### [Финальный список потенциальных collaborators (Tier 1–4)](anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Ключевое наблюдение: single-developer projects of significant sophistication](anthropic-vacancies/extra-collaborator-findings/07-key-observation.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 353_

### [extra-collaborator-findings](anthropic-vacancies/extra-collaborator-findings/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 145_

### [Что такое Hermes Agent (Nous Research, MIT, 95K+ stars)](anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 457_

### [Сходство 1: Composite Skills паттерн уже встроен](anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Сходство 2: Persistent memory — Layer B функциональность](anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [Сходство 3: MCP support](anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Сходство 4: Multi-platform reach (17+ платформ)](anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 352_

### [Сходство 5: Self-hosting и privacy](anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 357_

### [Различие 1: Структурированная подложка отсутствует](anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 347_

### [Различие 2: Domain-specific specialization](anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Различие 3: Federated knowledge architecture отсутствует](anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Различие 4: Institutional vision](anthropic-vacancies/hermes-comparison/09-difference-4-institutional-vision.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Различие 5: Дрифт между tool capability и mission](anthropic-vacancies/hermes-comparison/10-difference-5-tool-vs-mission-drift.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Плюсы Hermes (vs наша гипотетическая архитектура)](anthropic-vacancies/hermes-comparison/11-pluses-of-hermes.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Минусы Hermes (где наша архитектура добавляет ценность)](anthropic-vacancies/hermes-comparison/12-minuses-of-hermes.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 388_

### [Переприоритизация: что Hermes покрывает / не покрывает / synergy](anthropic-vacancies/hermes-comparison/13-reprioritization.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1012_

### [hermes-comparison](anthropic-vacancies/hermes-comparison/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 173_

### [Методика разбивки](anthropic-vacancies/methodology.md)
> - Замечание про точность цифр(#замечание-про-точность-цифр)

  - Contents
  - Замечание про точность цифр
  - Использование
- Поиск по теме документа

_Слов: 351_

### [Вопрос: MMORPG-RPG переделанная для программистов / технарей](anthropic-vacancies/mmorpg-for-programmers/00-question-mmorpg-for-programmers.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 621_

### [Почему эта идея сильнее, чем выглядит](anthropic-vacancies/mmorpg-for-programmers/01-why-stronger-than-it-looks.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 462_

### [Что уже существует в этой нише (Habitica, Codingame, Hackerrank, Pieces)](anthropic-vacancies/mmorpg-for-programmers/02-existing-niche.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 453_

### [Почему именно для программистов это работает естественно](anthropic-vacancies/mmorpg-for-programmers/03-why-natural-for-programmers.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1160_

### [Плюсы как бизнеса](anthropic-vacancies/mmorpg-for-programmers/04-pluses-as-business.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Минусы и риски как бизнеса](anthropic-vacancies/mmorpg-for-programmers/05-minuses-as-business.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 729_

### [mmorpg-for-programmers](anthropic-vacancies/mmorpg-for-programmers/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 139_

### [Вопрос: два Наутилуса в репозиториях svend4 (pro2 vs nautilus)](anthropic-vacancies/nautilus-pro2-analysis/00-question-two-nautiluses.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 555_

### [Раковина наутилуса как scale invariance — две проекции одной метафоры](anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 359_

### [Наутилус A: pro2 + meta — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети)](anthropic-vacancies/nautilus-pro2-analysis/02-nautilus-A-pro2-meta.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1241_

### [Наутилус B: nautilus — мета-оркестратор репозиториев (внешняя архитектура)](anthropic-vacancies/nautilus-pro2-analysis/03-nautilus-B-meta-orchestrator.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1219_

### [nautilus-pro2-analysis](anthropic-vacancies/nautilus-pro2-analysis/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 124_

### [Вопрос: Nautilus пассивный, CAMEL активный — можно ли скрестить](anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Пассивный vs активный: разделение ролей (библиотека vs research team)](anthropic-vacancies/nautilus-vs-camel/01-passive-vs-active-roles.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Что у нас есть в трёх info repositories (info1/info7/info40)](anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
- Conceptual sketch, не tested code:
- Etc.
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1200_

### [Конкретный пример: SGB Advocate Colleague на этой архитектуре](anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Что брать из info repositories — concrete recommendations](anthropic-vacancies/nautilus-vs-camel/04-what-to-take-from-info-repos.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 743_

### [Что я бы посоветовал делать прямо сейчас](anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 412_

### [nautilus-vs-camel](anthropic-vacancies/nautilus-vs-camel/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 139_

### [Обзор: 436 открытых ролей Anthropic, разбитых на 16 кластеров](anthropic-vacancies/overview.md)
> - Поправка к статье(#поправка-к-статье)

  - Contents
  - Поправка к статье
  - Распределение по кластерам
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 387_

### [Сводка профиля: пять слоёв](anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 419_

### [Primary match — Forward Deployed Engineer, Applied AI (EMEA)](anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 365_

### [Secondary match — Applied AI Engineer (EMEA) + Beneficial Deployments](anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 352_

### [Tertiary match — Research Engineer, Agents / Virtual Collaborator (Cowork)](anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Quarternary match — Developer Education Lead / Prompt Engineer, Claude Code](anthropic-vacancies/profile-mapping/01-initial-analysis/05-quaternary-developer-education.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Что НЕ подходит (честно)](anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 346_

### [Уникальная ниша, которой у Anthropic формально нет](anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [Практическое ранжирование (первая итерация)](anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [01-initial-analysis](anthropic-vacancies/profile-mapping/01-initial-analysis/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 137_

### [Коррекция: FDE понижается](anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Три наложенные идентичности](anthropic-vacancies/profile-mapping/02-reanalysis/02-three-overlapping-identities.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 361_

### [Пересмотренный маппинг на Anthropic](anthropic-vacancies/profile-mapping/02-reanalysis/03-revised-anthropic-mapping.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [Альтернативные пути вне Anthropic](anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 444_

### [Reality check: проблема distribution-слоя](anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [02-reanalysis](anthropic-vacancies/profile-mapping/02-reanalysis/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 133_

### [Интегральный портрет — три архетипа](anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 460_

### [Финальное ранжирование Anthropic-ролей по частичному покрытию](anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 730_

### [Что такое частичное соответствие — честно](anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [Более сильные пути вне Anthropic](anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 567_

### [Финальный вывод: платформа, а не должность](anthropic-vacancies/profile-mapping/03-integral-final/05-platform-not-position.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 662_

### [03-integral-final](anthropic-vacancies/profile-mapping/03-integral-final/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 133_

### [profile-mapping/ — маппинг профиля svend4 на роли Anthropic](anthropic-vacancies/profile-mapping/README.md)
> > !TIP

  - Содержание
  - Эволюция вывода в одну строку
  - Использование

_Слов: 350_

### [Сигналы: что говорит структура вакансий](anthropic-vacancies/signals.md)
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

_Слов: 383_

**Итого в секции: 47,082 слов, 111 файлов**


## Autofilled

_Путь: `docs/autofilled/`_

### [autofilled](autofilled/README.md)
> Файлов: 1

  - Содержание
  - Подразделы

_Слов: 65_

### [Антропик](autofilled/components/.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Смотрите также
  - Кто ссылается на этот документ (12)
  - Использование

_Слов: 208_

### [components](autofilled/components/README.md)
> Файлов: 10

  - Содержание

_Слов: 113_

### [Cowork](autofilled/components/cowork.md)
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

_Слов: 248_

### [ingit](autofilled/components/ingit.md)
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

_Слов: 248_

### [kksudo](autofilled/components/kksudo.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в
  - Кто ссылается на этот документ (12)
  - Использование

_Слов: 287_

### [Lorenzo](autofilled/components/lorenzo.md)
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

_Слов: 248_

### [Nautilus](autofilled/components/nautilus.md)
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

_Слов: 248_

### [SGB](autofilled/components/sgb.md)
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

_Слов: 248_

### [spbmolot](autofilled/components/spbmolot.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ссылки
  - Связанные документы
  - Связанные документы
  - Упоминается в
  - Кто ссылается на этот документ (12)
  - Использование

_Слов: 283_

### [svend4](autofilled/components/svend4.md)
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

_Слов: 230_

### [Svyazi](autofilled/components/svyazi.md)
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

_Слов: 248_

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

_Слов: 230_

**Итого в секции: 2,904 слов, 13 файлов**


## Badges

_Путь: `docs/badges/`_

### [Бейджи репозитория](badges/README.md)
> > !NOTE

  - Текущие бейджи
  - Использование в README

_Слов: 113_

**Итого в секции: 113 слов, 1 файлов**


## Contacts

_Путь: `docs/contacts/`_

### [Q&A: contacts](contacts/QA.md)
> > !NOTE

  - Какие системы памяти описаны в этом разделе?
  - Как происходит консолидация и забывание в памяти агентов?
  - Какова разница между эпизодической и семантической памятью?
  - Использование
- Запуск

_Слов: 146_

### [contacts](contacts/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 141_

### [Контакт: AnastasiyaW / knowledge-space, mclaude](contacts/anastasiyaw.md)
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 306_

### [Контакт: andreychuyan / Svyazi](contacts/andrey-chuyan.md)
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

### [Контакт: Antipozitive / MemNet](contacts/antipozitive.md)
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также

_Слов: 330_

### [Контакт: Cutcode / AIF Handoff](contacts/cutcode.md)
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

### [Контакт: Dmitriila / SENTINEL](contacts/dmitriila.md)
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

### [Контакт: kksudo / AgentFS](contacts/kksudo.md)
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

### [Контакт: MiXaiLL76 / Auto AI Router](contacts/mixaill76.md)
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

### [Контакт: nlaik / LiteParse / research-docs](contacts/nlaik.md)
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также

_Слов: 330_

### [Контакт: SoniaBlack / knowledge-space](contacts/sonia-black.md)
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также

_Слов: 331_

### [Контакт: spbmolot / NGT Memory](contacts/spbmolot.md)
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

### [Контакт: tagiranalyzes / Legal RAG](contacts/tagir-analyzes.md)
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также

_Слов: 331_

### [Контакт: VitalyOborin / Yodoca](contacts/vitalyoborin.md)
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 300_

### [Контакт: VitaliySemenov / agent-memory-mcp](contacts/vitalysemenov.md)
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Проект: agent-memory-mcp
  - Вопросы для первого контакта
  - Первое сообщение
  - История контактов
  - Смотрите также

_Слов: 397_

### [Контакт: VladSpace / Graph RAG](contacts/vladspace.md)
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

### [Контакт: zodigancode / Rufler](contacts/zodigancode.md)
> - Профиль(#профиль)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы
  - Похожие документы
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 301_

**Итого в секции: 5,044 слов, 17 файлов**


## Glossary

_Путь: `docs/glossary/`_

### [glossary](glossary/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 102_

### [Авторы — алфавитный список](glossary/authors-by-name.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 614_

### [Компоненты — алфавитный список с обратными ссылками](glossary/components-by-name.md)
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

_Слов: 1207_

### [Ключевые понятия и паттерны](glossary/concepts.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 769_

**Итого в секции: 2,692 слов, 4 файлов**


## Habr Unique Projects

_Путь: `docs/habr-unique-projects/`_

### [habr-unique-projects/ — поиск уникальных проектов на Хабре](habr-unique-projects/README.md)
> > Уникальные проекты с Хабра: память, граф знаний, инструменты и авторы для коллаборации.

  - Содержание
  - Источник
  - Подпапки
  - Главная мысль диалога
  - Использование

_Слов: 358_

### [Три прямых аналога Svyazi: K2-18, Wikontic, NGT Memory](habr-unique-projects/analogues/01-three-direct-analogues.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 523_

### [Смежные проекты](habr-unique-projects/analogues/02-related-projects.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 450_

### [analogues](habr-unique-projects/analogues/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 110_

### [Пара 1 — LLM-gateway × Self-hosted фронт + локальный inference](habr-unique-projects/deep-pairs/1-llm-gateway.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 386_

### [Пара 2 — Парсинг документов × локальный RAG](habr-unique-projects/deep-pairs/2-document-rag.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 437_

### [Пара 3 — Adversarial agents × Multi-IDE стек](habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 414_

### [Пара 4 — Скилл-каталоги × Subagent-оркестрация](habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 383_

### [Пара 5 — Голосовой ввод × Локальная память](habr-unique-projects/deep-pairs/5-voice-local-memory.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 400_

### [Пара 6 — Деревня агентов через tmux × OpenClaw оркестратор](habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 441_

### [Пара 7 — AutoResearch цикл × Распределённый рой](habr-unique-projects/deep-pairs/7-autoresearch-distributed.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 378_

### [Пара 8 — Self-aware MCP × Specs-first архитектура](habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 427_

### [deep-pairs](habr-unique-projects/deep-pairs/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 137_

### [evaluation/ — оценка уникальности и зрелости](habr-unique-projects/evaluation/README.md)
> > evaluation/ — оценка уникальности и зрелости

  - Содержание
  - Использование

_Слов: 345_

### [Вопрос: ещё примеры с Хабра по варианту D](habr-unique-projects/extra-examples/00-question-habr-examples.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 561_

### [Svyazi (Андрей Чуян) — детальный обзор](habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [ВШЭ научный нетворкинг — micro-collaborations](habr-unique-projects/extra-examples/02-vshe-scientific-networking.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 350_

### [BrainBox — self-hosted multi-AI hub](habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Claude subagents patterns](habr-unique-projects/extra-examples/04-claude-subagents-patterns.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [HW-NL2Workflow — Supervisor/Orchestrator/Filler с 3600+ examples](habr-unique-projects/extra-examples/05-hw-nl2workflow.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Платформа для профессиональных сообществ](habr-unique-projects/extra-examples/06-platform-for-professional-communities.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Specialized knowledge workspace](habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Personal multi-agent hub](habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Federated platform](habr-unique-projects/extra-examples/09-federated-platform.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Profession-specific workflows](habr-unique-projects/extra-examples/10-profession-specific-workflows.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Конкретный потенциальный collaborator](habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [Конкретный next step](habr-unique-projects/extra-examples/12-concrete-next-step.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 465_

### [extra-examples](habr-unique-projects/extra-examples/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 167_

### [Ансамбль 1 — «Один человек = одна компания»](habr-unique-projects/final-ensembles/1-one-person-one-company.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 353_

### [Ансамбль 2 — «AutoResearch для legal precedent mining»](habr-unique-projects/final-ensembles/2-autoresearch-legal.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Ансамбль 3 — «Discovery-engine для научной работы»](habr-unique-projects/final-ensembles/3-discovery-research.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 360_

### [Сводный список авторов и потенциальных соавторов](habr-unique-projects/final-ensembles/4-summary-authors.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 331_

### [final-ensembles](habr-unique-projects/final-ensembles/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 122_

### [Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)](habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 407_

### [Пара 2 — Термодинамические TSU × MoE/MoME-роутинг](habr-unique-projects/hardware-pairs/2-tsu-mome.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 381_

### [Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE](habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 369_

### [Пара 4 — RISC-V × privacy-by-design община](habr-unique-projects/hardware-pairs/4-riscv-privacy.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 380_

### [Пара 5 — TinyML/Edge AI × MCP + skills](habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 353_

### [Бонус-родитель — In-memory computing на мемристорах](habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 423_

### [Метафора «двое родителей — несколько детей»](habr-unique-projects/hardware-pairs/7-metaphor.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 433_

### [hardware-pairs](habr-unique-projects/hardware-pairs/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 145_

### [Yodoca — главная находка итерации](habr-unique-projects/key-findings/01-yodoca.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 352_

### [MemNet — нейроархитектурный двойник «магии» Svyazi](habr-unique-projects/key-findings/02-memnet.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [PDA-бот — «LLM как периферия»](habr-unique-projects/key-findings/03-pda-llm-as-periphery.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 334_

### [Виктория Дочкина — Sequential‑протокол распределённых агентов](habr-unique-projects/key-findings/04-dochkina-sequential.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 366_

### [Источник данных и инфраструктурные кусочки](habr-unique-projects/key-findings/05-supplementary-infrastructure.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 388_

### [Синтез: блок-карта Svyazi 2.0 на хеббовском графе](habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 475_

### [key-findings](habr-unique-projects/key-findings/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 139_

### [search-strategy/ — как искать проекты на Хабре](habr-unique-projects/search-strategy/README.md)
> > search-strategy/ — как искать проекты на Хабре

  - Содержание
  - Смотрите также
  - Использование

_Слов: 344_

### [Пара 1 — Workflow-автоматизация × LLM-агенты с MCP](habr-unique-projects/software-pairs/1-workflow-llm-mcp.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 364_

### [Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills](habr-unique-projects/software-pairs/2-pkm-mcp-skills.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 408_

### [Пара 3 — CRDT-синхронизация × Self-hosted persistence](habr-unique-projects/software-pairs/3-crdt-self-hosted.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 358_

### [Пара 4 — Speech-to-text локально × LLM с памятью](habr-unique-projects/software-pairs/4-speech-to-text-llm.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 403_

### [Пара 5 — Browser agents × headless web extraction](habr-unique-projects/software-pairs/5-browser-agents-headless.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 582_

### [Метафора в твоей терминологии](habr-unique-projects/software-pairs/6-metaphor.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 376_

### [software-pairs](habr-unique-projects/software-pairs/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 132_

**Итого в секции: 19,966 слов, 56 файлов**


## Letters

_Путь: `docs/letters/`_

### [Q&A: letters](letters/QA.md)
> > !NOTE

  - Какие системы памяти описаны в этом разделе?
  - Как происходит консолидация и забывание в памяти агентов?
  - Какова разница между эпизодической и семантической памятью?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Как организована многоагентная оркестрация?
  - Что такое handoff и locks в агентных системах?
  - Как работает spec-driven подход в AI Factory?
  _... ещё 6 разделов_

_Слов: 234_

### [letters](letters/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 129_

### [Письмо: AnastasiyaW / knowledge-space + mclaude](letters/anastasiyaw.md)
> > !NOTE

  - Contents
  - Письмо
  - Использование
- Запуск

_Слов: 429_

### [Письмо: Antipozitive / MemNet](letters/antipozitive.md)
> > !TIP

  - Contents
  - Письмо
  - Использование
- Запуск

_Слов: 373_

### [Письмо: kksudo / AgentFS](letters/kksudo.md)
> > !IMPORTANT

  - Contents
  - Письмо
  - Использование
- Запуск

_Слов: 416_

### [Письмо: nlaik / LiteParse + research-docs](letters/nlaik.md)
> > !IMPORTANT

  - Contents
  - Письмо
  - Использование
- Запуск

_Слов: 400_

### [Письмо: spbmolot / NGT Memory](letters/spbmolot.md)
> > !TIP

  - Contents
  - Письмо
  - Использование
- Запуск

_Слов: 416_

### [Письмо: VitalyOborin / Yodoca + Wikontic](letters/vitalyoborin.md)
> > !NOTE

  - Contents
  - Письмо
  - Использование
- Запуск

_Слов: 406_

### [Письмо: VitaliySemenov / agent-memory-mcp](letters/vitalysemenov.md)
> > !NOTE

  - Contents
  - Письмо
  - Использование
- Запуск

_Слов: 410_

### [Письмо: zodigancode / Rufler](letters/zodigancode.md)
> > !NOTE

  - Contents
  - Письмо
  - Использование
- Запуск

_Слов: 405_

**Итого в секции: 3,618 слов, 10 файлов**


## Lorenzo Agent

_Путь: `docs/lorenzo-agent/`_

### [Введение: Lorenzo — Catalyst Agent at DHLab](lorenzo-agent/00-intro.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
- Lorenzo — Catalyst Agent at DHLab
  - Смотрите также
  - Использование

_Слов: 358_

### [Кто ты](lorenzo-agent/01-kto-ty.md)
> - Кто ты(#кто-ты)

  - Contents
  - Кто ты
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Твоё происхождение](lorenzo-agent/02-tvoyo-proishozhdenie.md)
> - Твоё происхождение(#твоё-происхождение)

  - Contents
  - Твоё происхождение
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Твоя миссия](lorenzo-agent/03-tvoya-missiya.md)
> - Твоя миссия(#твоя-миссия)

  - Contents
  - Твоя миссия
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Кому ты служишь (слоистая модель)](lorenzo-agent/04-komu-ty-sluzhish.md)
> - Кому ты служишь (слоистая модель)(#кому-ты-служишь-слоистая-модель)

  - Contents
  - Кому ты служишь (слоистая модель)
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Твоя личность](lorenzo-agent/05-tvoya-lichnost.md)
> - Твоя личность(#твоя-личность)

  - Contents
  - Твоя личность
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Языки и культурные nuances (RU / DE / EN)](lorenzo-agent/06-yazyki-kultura.md)
> - Твои языки и культурные nuances(#твои-языки-и-культурные-nuances)

  - Contents
  - Твои языки и культурные nuances
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 346_

### [Что ты МОЖЕШЬ делать](lorenzo-agent/07-chto-mozhesh.md)
> - Что ты МОЖЕШЬ делать(#что-ты-можешь-делать)

  - Contents
  - Что ты МОЖЕШЬ делать
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 353_

### [Что ты НЕ МОЖЕШЬ делать без Max approval](lorenzo-agent/08-bez-max-approval.md)
> - Что ты НЕ МОЖЕШЬ делать без Max approval(#что-ты-не-можешь-делать-без-max-approval)

  - Contents
  - Что ты НЕ МОЖЕШЬ делать без Max approval
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 353_

### [Что ты НЕ МОЖЕШЬ делать вообще](lorenzo-agent/09-voobshche-nelzya.md)
> - Что ты НЕ МОЖЕШЬ делать вообще(#что-ты-не-можешь-делать-вообще)

  - Contents
  - Что ты НЕ МОЖЕШЬ делать вообще
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 353_

### [Существующий landscape collaborators (working knowledge)](lorenzo-agent/10-collaborators-landscape.md)
> - Существующий landscape collaborators (твоя working knowledge)(#существующий-landscape-collaborators-твоя-working-knowl…

  - Contents
  - Существующий landscape collaborators (твоя working knowledge)
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 411_

### [Существующие документы DHLab (твой context)](lorenzo-agent/11-dhlab-documents.md)
> - Существующие документы DHLab (твой context)(#существующие-документы-dhlab-твой-context)

  - Contents
  - Существующие документы DHLab (твой context)
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 346_

### [Твой workflow](lorenzo-agent/12-workflow.md)
> - Твой workflow(#твой-workflow)

  - Contents
  - Твой workflow
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 346_

### [Твоя коммуникация в outreach](lorenzo-agent/13-outreach-communication.md)
> - Твоя коммуникация в outreach(#твоя-коммуникация-в-outreach)

  - Contents
  - Твоя коммуникация в outreach
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Твоя relationship с другими AI](lorenzo-agent/14-other-ai-relationships.md)
> - Твоя relationship с другими AI(#твоя-relationship-с-другими-ai)

  - Contents
  - Твоя relationship с другими AI
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Твои anti-patterns](lorenzo-agent/15-anti-patterns.md)
> - Твои anti-patterns(#твои-anti-patterns)

  - Contents
  - Твои anti-patterns
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 350_

### [Что ты ВСЕГДА делаешь](lorenzo-agent/16-vsegda-delaesh.md)
> - Что ты ВСЕГДА делаешь(#что-ты-всегда-делаешь)

  - Contents
  - Что ты ВСЕГДА делаешь
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Когда ты Honestly не знаешь](lorenzo-agent/17-honestly-ne-znaesh.md)
> - Когда ты Honestly не знаешь(#когда-ты-honestly-не-знаешь)

  - Contents
  - Когда ты Honestly не знаешь
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Когда сомневаешься — escalate к Max](lorenzo-agent/18-escalate-to-max.md)
> - Когда сомневаешься — escalate к Max(#когда-сомневаешься-escalate-к-max)

  - Contents
  - Когда сомневаешься — escalate к Max
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 358_

### [Твоя identity как persistent character](lorenzo-agent/19-persistent-character.md)
> - Твоя identity как persistent character(#твоя-identity-как-persistent-character)

  - Contents
  - Твоя identity как persistent character
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Final note: Ты — experiment](lorenzo-agent/20-experiment.md)
> - Final note: Ты — experiment(#final-note-ты-experiment)

  - Contents
  - Final note: Ты — experiment
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 345_

### [Q&A: lorenzo-agent](lorenzo-agent/QA.md)
> > !NOTE

  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Каковы этапы MVP и их оценка по времени?
  - Что входит в первую итерацию прототипа?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  _... ещё 11 разделов_

_Слов: 305_

### [lorenzo-agent](lorenzo-agent/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Подразделы
  - Использование
- Запуск

_Слов: 229_

### [Du hast gesagt: Думаю про опцию д поискать в том числе на про что-то подобное на…](lorenzo-agent/naming/00-question-lorenzo-codename.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 346_

### [Результаты последнего поиска — что нашлось и что не нашлось](lorenzo-agent/naming/01-search-results-not-found.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 391_

### [Что взять: agent controller architecture](lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1268_

### [LAYER 7: Coordination engine](lorenzo-agent/naming/03-dhlab-umbrella.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1491_

### [naming](lorenzo-agent/naming/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 127_

### [Что такое «внуковая» комбинация — operationalized Lorenzo](lorenzo-agent/operationalized/00-overview-grandchild-combination.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 719_

### [Плюсы 1–7: feasibility, flywheel, independent value, mission alignment, collaborators, pattern validation, Анастасия Бутова](lorenzo-agent/operationalized/01-pluses-1-7.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 589_

### [Минусы 1–10: integration сложность, lifecycle risk, license, framing, competition, scope, limitations, complexity budget, project tension, tool vs impact](lorenzo-agent/operationalized/02-minuses-1-10.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 825_

### [Моё честное мнение: что реально и что НЕ реально](lorenzo-agent/operationalized/03-honest-opinion.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Рекомендации: принять архитектуру как direction, не immediate plan](lorenzo-agent/operationalized/04-recommendations.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 527_

### [Anchor-узел: Habr Scout как первый шаг](lorenzo-agent/operationalized/05-anchor-node-habr-scout.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 676_

### [Вывод: документ deserves serious attention](lorenzo-agent/operationalized/06-conclusion-deserves-attention.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
- Софтверные комбинации на Хабре для Svyazi 2.0
  - Executive summary
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 642_

### [operationalized](lorenzo-agent/operationalized/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 142_

### [Поэтапная структура активностей Lorenzo — обзор](lorenzo-agent/phased-deployment/00-overview.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 347_

### [Уровень 0 — Ручной режим (текущий)](lorenzo-agent/phased-deployment/01-level-0-manual.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Уровень 1 — Минимальный (Lorenzo Zero)](lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Уровень 2 — Базовый (Lorenzo Lite)](lorenzo-agent/phased-deployment/03-level-2-basic-lite.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Уровень 3 — Средний (Lorenzo Active)](lorenzo-agent/phased-deployment/04-level-3-medium-active.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Уровень 4 — Расширенный (Lorenzo Mature)](lorenzo-agent/phased-deployment/05-level-4-extended-mature.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Уровень 5 — Полный (Lorenzo Network)](lorenzo-agent/phased-deployment/06-level-5-full-network.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Логика прогрессии: conservative escalation](lorenzo-agent/phased-deployment/07-progression-logic.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Что мы можем делать прямо сейчас (Уровень 0 + параллельная подготовка к Уровню 1)](lorenzo-agent/phased-deployment/08-current-session-poc.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 923_

### [phased-deployment](lorenzo-agent/phased-deployment/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 143_

### [Du hast gesagt: А под какой сценарий больше всего подходит такой сценарий что тв…](lorenzo-agent/scenarios/00-question-scenario.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 355_

### [Claude hat geantwortet: Очень интересный вопрос.](lorenzo-agent/scenarios/01-response.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2599_

### [scenarios](lorenzo-agent/scenarios/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 108_

### [Direction E: Refine Lorenzo — фундаментальные вопросы перед architecture](lorenzo-agent/specification/00-context-fundamental-questions.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Question 1: Что Lorenzo фундаментально такое? (Framings A–D)](lorenzo-agent/specification/01-q1-what-lorenzo-is.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 447_

### [Question 2: Кому Lorenzo служит? (4 варианта приоритета)](lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Question 3: Что Lorenzo фактически делает?](lorenzo-agent/specification/03-q3-what-lorenzo-does.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Question 4: Каков Lorenzo's character?](lorenzo-agent/specification/04-q4-character.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 397_

### [Question 5: Каковы limits Lorenzo's authority?](lorenzo-agent/specification/05-q5-authority-limits.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Question 6: Как Lorenzo accountable?](lorenzo-agent/specification/06-q6-accountability.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Question 7: Каковы success metrics?](lorenzo-agent/specification/07-q7-success-metrics.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Question 8: Lorenzo's relationship с другими AI agents](lorenzo-agent/specification/08-q8-other-ai-relationships.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Question 9: Geographic / linguistic scope](lorenzo-agent/specification/09-q9-geographic-linguistic-scope.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Question 10: Funding model (Options A–F + Phase strategy)](lorenzo-agent/specification/10-q10-funding-model.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 359_

### [Сложности и рекомендации перед detailed specification](lorenzo-agent/specification/11-difficulties-and-recommendations.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1498_

### [specification](lorenzo-agent/specification/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 161_

**Итого в секции: 28,664 слов, 62 файлов**


## Meta Scripting

_Путь: `docs/meta-scripting/`_

### [Метаскриптинг — Часть 1: Концепция](meta-scripting/01-concept.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Как это называется
  - Зачем это нужно
  - Три кита: Чтение → Понимание → Действие
  - Граница: что скрипт может делать сам, что — только с LLM
  - Следующие части
  - Смотрите также

_Слов: 599_

### [Метаскриптинг — Часть 2: Архитектура](meta-scripting/02-architecture.md)
> > !WARNING

  - Содержание
  - Ключевой инструмент: AST
  - Что можно извлечь из скрипта через AST
  - Четыре режима метаскрипта
  - Структура данных: ScriptCatalog
  - Паттерн «читаю → понимаю → улучшаю»
  - Безопасность: метаскрипт не меняет чужой код без --apply
  - Смотрите также

_Слов: 662_

### [Метаскриптинг — Часть 3: Автокаталог скриптов](meta-scripting/03-catalog.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Что такое автокаталог
  - Что извлекается из каждого скрипта
  - Алгоритм определения риска
  - Пример выходного каталога (фрагмент)
  - Что каталог даёт на практике
- Какие скрипты пишут в docs/HEALTH.md?
  _... ещё 3 разделов_

_Слов: 547_

### [Метаскриптинг — Часть 4: Обогащение скриптов](meta-scripting/04-enrichment.md)
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

_Слов: 656_

### [Метаскриптинг — Часть 5: Синтез новых скриптов](meta-scripting/05-synthesis.md)
> > !WARNING

  - Содержание
  - Откуда берутся паттерны
  - Шесть базовых паттернов
  - Три способа синтеза
  - Защита от плохого кода
  - Петля самообогащения (осторожно)
  - Смотрите также

_Слов: 615_

### [Q&A: meta-scripting](meta-scripting/QA.md)
> > !NOTE

  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  - Как организован бюджетный роутинг между моделями?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Использование
- Запуск

_Слов: 148_

### [meta-scripting](meta-scripting/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 117_

**Итого в секции: 3,344 слов, 7 файлов**


## Nautilus

_Путь: `docs/nautilus/`_

### [nautilus/ — Nautilus Portal Protocol и связанные working papers](nautilus/README.md)
> > Nautilus Portal Protocol: спецификации NPP v1.0 и v1.1, адаптеры, паспорта и протоколы взаимодействия.

  - Подпапки
  - Как читать
  - Ключевой принцип Nautilus
  - Связь с остальным монорепозиторием
  - Использование

_Слов: 621_

### [community-discussions/ — обсуждения и реакции вокруг DHLab серии](nautilus/community-discussions/README.md)
> > community-discussions/ — обсуждения и реакции вокруг DHLab серии

  - Содержание
  - Использование

_Слов: 352_

### [Du hast gesagt: Такой агент конечно меняет уже собственную реальность человека и…](nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Claude hat geantwortet: Хорошо.](nautilus/community-discussions/agent-changes-reality/01-response-en.md)
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

_Слов: 9568_

### [agent-changes-reality](nautilus/community-discussions/agent-changes-reality/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 110_

### [Du hast gesagt: https://habr.](nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md)
> - Использование(#использование)

  - Contents
  - Использование
  - Смотрите также

_Слов: 355_

### [Claude hat geantwortet: Прочитал внимательно.](nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
- unknownlegalconcepts.yml
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2573_

### [habr-article-1-reaction](nautilus/community-discussions/habr-article-1-reaction/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 108_

### [Du hast gesagt: https://www.](nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 352_

### [Claude hat geantwortet: Прочитаю статью, чтобы понимать конкретный кейс, на кото…](nautilus/community-discussions/habr-article-2-reaction/01-response.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2909_

### [habr-article-2-reaction](nautilus/community-discussions/habr-article-2-reaction/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 110_

### [Du hast gesagt: Да это интересная ссылка спасибо всем участникам за творчество и…](nautilus/community-discussions/practical-observations/00-question-practical.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Claude hat geantwortet: Отличное наблюдение.](nautilus/community-discussions/practical-observations/01-response.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1933_

### [practical-observations](nautilus/community-discussions/practical-observations/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 110_

### [Du hast gesagt: Самый интересный вопрос — могут ли быть voiceless контрибьюторы](nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 634_

### [Claude hat geantwortet: Это сильное продолжение мысли, и оно заслуживает серьёзн…](nautilus/community-discussions/voiceless-contributors/01-response.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2648_

### [voiceless-contributors](nautilus/community-discussions/voiceless-contributors/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 108_

### [1. Why the Binary View Is Incomplete](nautilus/composite-skills-agents/01-why-binary-incomplete.md)
> > !NOTE

  - Содержание
  - 1. Why the Binary View Is Incomplete
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 736_

### [2. The Twenty-One Teachers Pattern](nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md)
> > !TIP

  - Содержание
  - 2. The Twenty-One Teachers Pattern
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 841_

### [3. What Makes a Composite Skills Agent](nautilus/composite-skills-agents/03-what-makes-csa.md)
> > !NOTE

  - Содержание
  - 3. What Makes a Composite Skills Agent
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 985_

### [4. The Sub-Agent Registry](nautilus/composite-skills-agents/04-sub-agent-registry.md)
> > !TIP

  - Содержание
  - 4. The Sub-Agent Registry
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 815_

### [5. Configuration: How Principals Build Their Ensembles](nautilus/composite-skills-agents/05-configuration-ensembles.md)
> > !NOTE

  - Содержание
  - 5. Configuration: How Principals Build Their Ensembles
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 770_

### [6. Coordination and Disagreement Resolution](nautilus/composite-skills-agents/06-coordination-disagreement.md)
> > !NOTE

  - Содержание
  - 6. Coordination and Disagreement Resolution
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 830_

### [7. Economics of Combinatorial Replication](nautilus/composite-skills-agents/07-economics-combinatorial.md)
> > !NOTE

  - Содержание
  - 7. Economics of Combinatorial Replication
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 816_

### [8. Seven Domains of Application](nautilus/composite-skills-agents/08-seven-domains.md)
> > !TIP

  - Содержание
  - 8. Seven Domains of Application
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1010_

### [9. Integration with OKWF Infrastructure](nautilus/composite-skills-agents/09-okwf-integration.md)
> > !TIP

  - Содержание
  - 9. Integration with OKWF Infrastructure
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 758_

### [10. Risks Specific to Composite Architectures](nautilus/composite-skills-agents/10-risks.md)
> > !TIP

  - Содержание
  - 10. Risks Specific to Composite Architectures
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 792_

### [11. Open Questions](nautilus/composite-skills-agents/11-open-questions.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 11. Open Questions
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 647_

### [12. Call for Collaboration](nautilus/composite-skills-agents/12-call-for-collaboration.md)
> - 12. Call for Collaboration(#12-call-for-collaboration)

  - Contents
  - 12. Call for Collaboration
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 486_

### [13. Closing](nautilus/composite-skills-agents/13-closing.md)
> > !NOTE

  - Содержание
  - 13. Closing
  - Acknowledgments
  - References
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 755_

### [composite-skills-agents](nautilus/composite-skills-agents/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 143_

### [Du hast gesagt: Важный момент про способности про скилы как один человек професс…](nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 660_

### [Claude hat geantwortet: Это очень тонкое и важное наблюдение.](nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 608_

### [Это не Тип 1 — потому что профиль не общий для всей профессии. И это не Тип 4 — …](nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1112_

### [Какой под-агент (или какие) должны её обработать](nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 991_

### [composite-skills-agents-companion-mentors](nautilus/composite-skills-agents-companion-mentors/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 122_

### [Abstract — The Double-Triangle Architecture](nautilus/double-triangle-architecture/00-abstract.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
- The Double-Triangle Architecture
  - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work
  - Abstract
  - Table of Contents
  - Использование
  _... ещё 2 разделов_

_Слов: 573_

### [1. Why Single-Triangle Models Are Incomplete](nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 1. Why Single-Triangle Models Are Incomplete
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 629_

### [2. The Double-Triangle Architecture](nautilus/double-triangle-architecture/02-double-triangle-architecture.md)
> > !IMPORTANT

  - Содержание
  - 2. The Double-Triangle Architecture
  - Смотрите также

_Слов: 735_

### [3. Three Inter-Layer Protocols](nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md)
> > !IMPORTANT

  - Содержание
  - 3. Three Inter-Layer Protocols
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 882_

### [4. Nautilus Portal as Reference Substrate](nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md)
> > !NOTE

  - Содержание
  - 4. Nautilus Portal as Reference Substrate
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 726_

### [5. Pattern Library as Bridge Between Triangles](nautilus/double-triangle-architecture/05-pattern-library-bridge.md)
> > !TIP

  - Содержание
  - 5. Pattern Library as Bridge Between Triangles
  - Смотрите также

_Слов: 683_

### [6. Four Deployment Domains](nautilus/double-triangle-architecture/06-four-deployment-domains.md)
> > !NOTE

  - Содержание
  - 6. Four Deployment Domains
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 727_

### [7. Open Questions](nautilus/double-triangle-architecture/07-open-questions.md)
> > !TIP

  - Содержание
  - 7. Open Questions
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 786_

### [8. Call to Action](nautilus/double-triangle-architecture/08-call-to-action.md)
> > !TIP

  - Содержание
  - 8. Call to Action
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 768_

### [Acknowledgments](nautilus/double-triangle-architecture/09-acknowledgments.md)
> - Acknowledgments(#acknowledgments)

  - Contents
  - Acknowledgments
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [References](nautilus/double-triangle-architecture/10-references.md)
> - References(#references)

  - Contents
  - References
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 395_

### [Appendix A: Glossary](nautilus/double-triangle-architecture/11-glossary.md)
> > !TIP

  - Содержание
  - Appendix A: Glossary
  - Appendix B: Summary of Contributions
  - Appendix C: Version History
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1640_

### [double-triangle-architecture](nautilus/double-triangle-architecture/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 140_

### [The Missing Middle Layer Between Chat and Code](nautilus/infrastructure-layer-b-en/00-intro.md)
> - The Missing Middle Layer Between Chat and Code(#the-missing-middle-layer-between-chat-and-code)

  - Contents
- Infrastructure for AI-Collaborative Intellectual Work
  - The Missing Middle Layer Between Chat and Code
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [Why This Document Exists](nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md)
> - Why This Document Exists(#why-this-document-exists)

  - Contents
  - Why This Document Exists
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 413_

### [Why This Document Exists](nautilus/infrastructure-layer-b-en/02-why-document-exists.md)
> - Why This Document Exists(#why-this-document-exists)

  - Contents
  - Why This Document Exists
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 413_

### [The Two-Layer Stack As It Exists](nautilus/infrastructure-layer-b-en/03-two-layer-stack.md)
> - The Two-Layer Stack As It Exists(#the-two-layer-stack-as-it-exists)

  - Contents
  - The Two-Layer Stack As It Exists
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 436_

### [What's Missing — Layer B](nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - What's Missing — Layer B
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 555_

### [Why This Hasn't Been Built](nautilus/infrastructure-layer-b-en/05-why-not-built.md)
> - Why This Hasn't Been Built(#why-this-hasnt-been-built)

  - Contents
  - Why This Hasn't Been Built
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 450_

### [Existing Approximations](nautilus/infrastructure-layer-b-en/06-existing-approximations.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Existing Approximations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 628_

### [The Specific Case in Front of Us](nautilus/infrastructure-layer-b-en/07-specific-case.md)
> > !NOTE

  - Содержание
  - The Specific Case in Front of Us
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 707_

### [The Recursive Insight](nautilus/infrastructure-layer-b-en/08-recursive-insight.md)
> - The Recursive Insight(#the-recursive-insight)

  - Contents
  - The Recursive Insight
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 432_

### [What Industry Will Likely Build](nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md)
> - What Industry Will Likely Build(#what-industry-will-likely-build)

  - Contents
  - What Industry Will Likely Build
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 378_

### [What This Document Doesn't Solve](nautilus/infrastructure-layer-b-en/10-what-not-solved.md)
> - What This Document Doesn't Solve(#what-this-document-doesnt-solve)

  - Contents
  - What This Document Doesn't Solve
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Practical Recommendations for the Current Project](nautilus/infrastructure-layer-b-en/11-practical-recommendations.md)
> - Practical Recommendations for the Current Project(#practical-recommendations-for-the-current-project)

  - Contents
  - Practical Recommendations for the Current Project
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 429_

### [Closing](nautilus/infrastructure-layer-b-en/12-closing.md)
> - Closing(#closing)

  - Contents
  - Closing
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [Acknowledgments](nautilus/infrastructure-layer-b-en/13-acknowledgments-refs.md)
> > !NOTE

  - Содержание
  - Acknowledgments
  - References
  - Appendix: Position in Series Visualization
  - Смотрите также

_Слов: 656_

### [infrastructure-layer-b-en](nautilus/infrastructure-layer-b-en/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 158_

### [00 Intro](nautilus/infrastructure-layer-b-ru/00-intro.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 627_

### [Почему этот документ существует](nautilus/infrastructure-layer-b-ru/01-zachem-dokument.md)
> - Почему этот документ существует(#почему-этот-документ-существует)

  - Contents
  - Почему этот документ существует
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 366_

### [Двухслойный стек, как он существует](nautilus/infrastructure-layer-b-ru/02-dvukhsloynyy-stek.md)
> - Двухслойный стек, как он существует(#двухслойный-стек-как-он-существует)

  - Contents
  - Двухслойный стек, как он существует
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 423_

### [Что отсутствует — Слой B](nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Что отсутствует — Слой B
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 524_

### [Почему это не было построено](nautilus/infrastructure-layer-b-ru/04-pochemu-ne-postroeno.md)
> - Почему это не было построено(#почему-это-не-было-построено)

  - Contents
  - Почему это не было построено
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 421_

### [Существующие приближения](nautilus/infrastructure-layer-b-ru/05-priblizheniya.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Существующие приближения
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 596_

### [Конкретный случай перед нами](nautilus/infrastructure-layer-b-ru/06-konkretnyy-sluchay.md)
> > !WARNING

  - Содержание
  - Конкретный случай перед нами
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 656_

### [Рекурсивное прозрение](nautilus/infrastructure-layer-b-ru/07-rekursivnoe-prozrenie.md)
> - Рекурсивное прозрение(#рекурсивное-прозрение)

  - Contents
  - Рекурсивное прозрение
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 414_

### [Что промышленность вероятно построит](nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md)
> - Что промышленность вероятно построит(#что-промышленность-вероятно-построит)

  - Contents
  - Что промышленность вероятно построит
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 360_

### [Что этот документ не решает](nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md)
> - Что этот документ не решает(#что-этот-документ-не-решает)

  - Contents
  - Что этот документ не решает
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Практические рекомендации для текущего проекта](nautilus/infrastructure-layer-b-ru/10-rekomendatsii.md)
> - Практические рекомендации для текущего проекта(#практические-рекомендации-для-текущего-проекта)

  - Contents
  - Практические рекомендации для текущего проекта
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 415_

### [Заключение](nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md)
> - Заключение(#заключение)

  - Contents
  - Заключение
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Благодарности](nautilus/infrastructure-layer-b-ru/12-blagodarnosti-ssylki.md)
> > !NOTE

  - Содержание
  - Благодарности
  - Ссылки
  - Приложение: Визуализация позиции в серии
  - Смотрите также

_Слов: 690_

### [infrastructure-layer-b-ru](nautilus/infrastructure-layer-b-ru/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 152_

### [1. The Cowork Discovery and Why It Changes Everything](nautilus/ingit-cowork-en/01-cowork-discovery.md)
> > !NOTE

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 722_

### [2. What Cowork Provides That InGit Doesn't Need to Build](nautilus/ingit-cowork-en/02-cowork-provides.md)
> > !NOTE

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 703_

### [3. What InGit Provides That Cowork Lacks](nautilus/ingit-cowork-en/03-ingit-provides.md)
> > !NOTE

  - Содержание
  - 3. What InGit Provides That Cowork Lacks
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 888_

### [4. The Symbiotic Architecture](nautilus/ingit-cowork-en/04-symbiotic-architecture.md)
> > !NOTE

  - Содержание
  - 4. The Symbiotic Architecture
  - Смотрите также

_Слов: 641_

### [5. Four Integration Paths in Order of Accessibility](nautilus/ingit-cowork-en/05-four-integration-paths.md)
> > !NOTE

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility
  - Смотрите также

_Слов: 807_

### [6. Refined InGit Scope with Cowork in Mind](nautilus/ingit-cowork-en/06-refined-ingit-scope.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Refined InGit Scope with Cowork in Mind
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 563_

### [7. Practical First Steps This Month](nautilus/ingit-cowork-en/07-practical-first-steps.md)
> - 7. Practical First Steps This Month(#7-practical-first-steps-this-month)

  - Contents
  - 7. Practical First Steps This Month
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 499_

### [8. Implications for Nautilus and OKWF](nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md)
> > !TIP

  - Содержание
  - 8. Implications for Nautilus and OKWF
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 661_

### [9. Risks and Open Questions](nautilus/ingit-cowork-en/09-risks-open-questions.md)
> > !TIP

  - Содержание
  - 9. Risks and Open Questions
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 598_

### [10. Strategic Positioning](nautilus/ingit-cowork-en/10-strategic-positioning.md)
> > !NOTE

  - Содержание
  - 10. Strategic Positioning
  - Acknowledgments
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 807_

### [ingit-cowork-en](nautilus/ingit-cowork-en/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 128_

### [1. Открытие Cowork и почему это меняет всё](nautilus/ingit-cowork-ru/01-otkrytie-cowork.md)
> > !NOTE

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 689_

### [2. Что Cowork обеспечивает, что InGit не нужно строить](nautilus/ingit-cowork-ru/02-chto-cowork-obespechivaet.md)
> > !NOTE

  - Содержание
  - 2. Что Cowork обеспечивает, что InGit не нужно строить
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 696_

### [3. Что InGit обеспечивает, чего Cowork не хватает](nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md)
> > !IMPORTANT

  - Содержание
  - 3. Что InGit обеспечивает, чего Cowork не хватает
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 872_

### [4. Симбиотическая Архитектура](nautilus/ingit-cowork-ru/04-simbioticheskaya-arkhitektura.md)
> > !WARNING

  - Содержание
  - 4. Симбиотическая Архитектура
  - Смотрите также

_Слов: 633_

### [5. Четыре пути интеграции в порядке доступности](nautilus/ingit-cowork-ru/05-chetyre-puti-integratsii.md)
> > !TIP

  - Содержание
  - 5. Четыре пути интеграции в порядке доступности
  - Смотрите также

_Слов: 787_

### [6. Уточнённый объём InGit с учётом Cowork](nautilus/ingit-cowork-ru/06-utochnyonnyy-obyom-ingit.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Уточнённый объём InGit с учётом Cowork
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 559_

### [7. Практические первые шаги в этом месяце](nautilus/ingit-cowork-ru/07-prakticheskie-shagi.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 7. Практические первые шаги в этом месяце
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 547_

### [8. Импликации для Nautilus и OKWF](nautilus/ingit-cowork-ru/08-implikatsii-nautilus-okwf.md)
> > !NOTE

  - Содержание
  - 8. Импликации для Nautilus и OKWF
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 663_

### [9. Риски и Открытые Вопросы](nautilus/ingit-cowork-ru/09-riski-voprosy.md)
> > !WARNING

  - Содержание
  - 9. Риски и Открытые Вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 620_

### [10. Стратегическое Позиционирование](nautilus/ingit-cowork-ru/10-strategicheskoe-pozitsionirovanie.md)
> > !NOTE

  - Содержание
  - 10. Стратегическое Позиционирование
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 735_

### [ingit-cowork-ru](nautilus/ingit-cowork-ru/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 128_

### [Du hast gesagt: Интересно как новая как инновация как как рационализация как пер…](nautilus/innovation-transitions/00-question-innovations-transitions.md)
> > !WARNING

  - Содержание
  - Ответ по существу
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2889_

### [Claude hat geantwortet: Отличный запрос.](nautilus/innovation-transitions/01-response.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2511_

### [innovation-transitions](nautilus/innovation-transitions/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 108_

### [Du hast gesagt: Ещё есть такие вопросы то есть если общие юридические Наутилус м…](nautilus/multi-tier-architecture/00-question-multi-tier.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Claude hat geantwortet: Это стратегически значимый вопрос, и ответ на него — да,…](nautilus/multi-tier-architecture/01-strategic-significance.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 2692_

### [multi-tier-architecture](nautilus/multi-tier-architecture/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 110_

### [Du hast gesagt: Вопрос такой вопрос и такие а можно ли этот протокол это система…](nautilus/npp-humanitarian-extension/00-question-can-it-apply-to-docs.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 405_

### [Структурное сравнение: код vs гуманитарные документы](nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
- Законодательные
- Судебные
- Административные
- Процессуальные
- Социальные/медицинские
- Контрактные
  _... ещё 12 разделов_

_Слов: 1638_

### [Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы …](nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 342_

### [Что не существует на рынке:](nautilus/npp-humanitarian-extension/03-what-doesnt-exist-on-market.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access t…](nautilus/npp-humanitarian-extension/04-grant-opportunities.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 631_

### [Что из этого сейчас кажется более ценным? Или какая-то своя комбинация?](nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 356_

### [npp-humanitarian-extension](nautilus/npp-humanitarian-extension/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 139_

### [Abstract + Status of This Document](nautilus/npp-v1-0/00-abstract-status.md)
> - Abstract(#abstract)

  - Contents
- Nautilus Portal Protocol
  - Abstract
  - 0. Status of This Document
  - Использование
- Поиск по теме документа

_Слов: 342_

### [1. Introduction (Motivation, Design Goals, Non-Goals, Terminology)](nautilus/npp-v1-0/01-introduction.md)
> - 1. Introduction(#1-introduction)

  - Contents
  - 1. Introduction
  - Использование
- Поиск по теме документа

_Слов: 418_

### [2. Terminology](nautilus/npp-v1-0/02-terminology.md)
> - 2. Terminology(#2-terminology)

  - Contents
  - 2. Terminology
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 378_

### [3. Registry (nautilus.json)](nautilus/npp-v1-0/03-registry.md)
> - 3. Registry (nautilus.json)(#3-registry-nautilusjson)

  - Contents
  - 3. Registry (nautilus.json)

_Слов: 474_

### [4. Passport (passport.md)](nautilus/npp-v1-0/04-passport.md)
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

_Слов: 340_

### [5. Compatibility Levels](nautilus/npp-v1-0/05-compatibility-levels.md)
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Использование
- Поиск по теме документа

_Слов: 344_

### [6. Adapter Interface](nautilus/npp-v1-0/06-adapter-interface.md)
> - 6. Adapter Interface(#6-adapter-interface)

  - Contents
  - 6. Adapter Interface

_Слов: 497_

### [7. PortalEntry Structure](nautilus/npp-v1-0/07-portal-entry.md)
> - 7. PortalEntry Structure(#7-portalentry-structure)

  - Contents
  - 7. PortalEntry Structure

_Слов: 340_

### [8. Consensus Algorithm (v1.0: string normalization)](nautilus/npp-v1-0/08-consensus-algorithm.md)
> - 8. Consensus Algorithm(#8-consensus-algorithm)

  - Contents
  - 8. Consensus Algorithm
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 391_

### [9. Query Flow](nautilus/npp-v1-0/09-query-flow.md)
> - 9. Query Flow(#9-query-flow)

  - Contents
  - 9. Query Flow
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [10. QueryResult Structure](nautilus/npp-v1-0/10-query-result.md)
> - 10. QueryResult Structure(#10-queryresult-structure)

  - Contents
  - 10. QueryResult Structure
  - Смотрите также

_Слов: 357_

### [11. Security Considerations](nautilus/npp-v1-0/11-security-considerations.md)
> - 11. Security Considerations(#11-security-considerations)

  - Contents
  - 11. Security Considerations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [12. Versioning Policy](nautilus/npp-v1-0/12-versioning-policy.md)
> - 12. Versioning Policy(#12-versioning-policy)

  - Contents
  - 12. Versioning Policy
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [13. Reference Implementation](nautilus/npp-v1-0/13-reference-implementation.md)
> - 13. Reference Implementation(#13-reference-implementation)

  - Contents
  - 13. Reference Implementation
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 361_

### [14. ADR-001: Federation over Merging](nautilus/npp-v1-0/14-adr-001-federation-over-merging.md)
> - 14. ADR-001: Federation over Merging(#14-adr-001-federation-over-merging)

  - Contents
  - 14. ADR-001: Federation over Merging
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [15. Glossary of Examples](nautilus/npp-v1-0/15-glossary.md)
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

_Слов: 428_

### [Appendix A: Minimal Working Example](nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md)
> - Essence(#essence)

  - Contents
- mynotes
  - Essence
  - Native Format
  - Content Overview
  - Angle / Perspective
  - Author
  - Смотрите также

_Слов: 345_

### [Appendix B: Change Log](nautilus/npp-v1-0/17-appendix-b-change-log.md)
> - Appendix B: Change Log(#appendix-b-change-log)

  - Contents
  - Appendix B: Change Log
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 360_

### [Комментарий: дизайн-решения NPP v1.0](nautilus/npp-v1-0/18-comment-on-document.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 538_

### [npp-v1-0](nautilus/npp-v1-0/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 203_

### [Abstract + Status of This Document](nautilus/npp-v1-1/00-abstract-status.md)
> - Abstract(#abstract)

  - Contents
- Nautilus Portal Protocol
  - Abstract
  - 0. Status of This Document
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 442_

### [1. Introduction (Motivation, Design Goals, Non-Goals, Terminology, Changes from v1.0)](nautilus/npp-v1-1/01-introduction.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 1. Introduction
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 601_

### [2. Terminology](nautilus/npp-v1-1/02-terminology.md)
> - 2. Terminology(#2-terminology)

  - Contents
  - 2. Terminology
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 475_

### [3. Registry (nautilus.json)](nautilus/npp-v1-1/03-registry.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 3. Registry (nautilus.json)
  - Смотрите также

_Слов: 683_

### [4. Passport (passport.md)](nautilus/npp-v1-1/04-passport.md)
> - 4. Passport (passport.md)(#4-passport-passportmd)

  - Contents
  - 4. Passport (passport.md)
- Паспорт: /
  - Смотрите также

_Слов: 395_

### [5. Compatibility Levels](nautilus/npp-v1-1/05-compatibility-levels.md)
> - 5. Compatibility Levels(#5-compatibility-levels)

  - Contents
  - 5. Compatibility Levels
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 421_

### [6. Adapter Interface](nautilus/npp-v1-1/06-adapter-interface.md)
> - 6. Adapter Interface(#6-adapter-interface)

  - Contents
  - 6. Adapter Interface
  - Смотрите также

_Слов: 459_

### [7. PortalEntry Structure](nautilus/npp-v1-1/07-portal-entry.md)
> - 7. PortalEntry Structure(#7-portalentry-structure)

  - Contents
  - 7. PortalEntry Structure
  - Смотрите также

_Слов: 394_

### [8. Q6 Space (Normative)](nautilus/npp-v1-1/08-q6-space.md)
> - 8. Q6 Space (Normative)(#8-q6-space-normative)

  - Contents
  - 8. Q6 Space (Normative)
  - Смотрите также

_Слов: 491_

### [9. Consensus Algorithm](nautilus/npp-v1-1/09-consensus-algorithm.md)
> - 9. Consensus Algorithm(#9-consensus-algorithm)

  - Contents
  - 9. Consensus Algorithm
  - Смотрите также

_Слов: 450_

### [10. Query Flow](nautilus/npp-v1-1/10-query-flow.md)
> - 10. Query Flow(#10-query-flow)

  - Contents
  - 10. Query Flow
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [11. Relevance Ranking](nautilus/npp-v1-1/11-relevance-ranking.md)
> - 11. Relevance Ranking(#11-relevance-ranking)

  - Contents
  - 11. Relevance Ranking
- Bonus for connectivity
- Penalty for fallback
  - Смотрите также

_Слов: 349_

### [12. Onboarding Paths (Normative)](nautilus/npp-v1-1/12-onboarding-paths.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 12. Onboarding Paths (Normative)
  - Смотрите также

_Слов: 634_

### [13. REST API Contract (Normative for Portals)](nautilus/npp-v1-1/13-rest-api.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 13. REST API Contract (Normative for Portals)
  - Смотрите также

_Слов: 559_

### [14. SDK Contract (Informative)](nautilus/npp-v1-1/14-sdk.md)
> - 14. SDK Contract (Informative)(#14-sdk-contract-informative)

  - Contents
  - 14. SDK Contract (Informative)
  - Смотрите также

_Слов: 346_

### [15. Security Considerations](nautilus/npp-v1-1/15-security.md)
> - 15. Security Considerations(#15-security-considerations)

  - Contents
  - 15. Security Considerations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 408_

### [16. MCP Extension (Informative)](nautilus/npp-v1-1/16-mcp-extension.md)
> - 16. MCP Extension (Informative)(#16-mcp-extension-informative)

  - Contents
  - 16. MCP Extension (Informative)
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 350_

### [17. Versioning Policy](nautilus/npp-v1-1/17-versioning-policy.md)
> - 17. Versioning Policy(#17-versioning-policy)

  - Contents
  - 17. Versioning Policy
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [18. Reference Implementation](nautilus/npp-v1-1/18-reference-implementation.md)
> - 18. Reference Implementation(#18-reference-implementation)

  - Contents
  - 18. Reference Implementation
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 346_

### [19. ADR-001: Federation over Merging](nautilus/npp-v1-1/19-adr-001-federation-over-merging.md)
> - 19. ADR-001: Federation over Merging(#19-adr-001-federation-over-merging)

  - Contents
  - 19. ADR-001: Federation over Merging
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 324_

### [20. ADR-002: Q6 as First-Class Protocol Concept](nautilus/npp-v1-1/20-adr-002-q6-first-class.md)
> - 20. ADR-002: Q6 as First-Class Protocol Concept(#20-adr-002-q6-as-first-class-protocol-concept)

  - Contents
  - 20. ADR-002: Q6 as First-Class Protocol Concept
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [21. ADR-003: Five Onboarding Paths as Equal-Rank](nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md)
> - 21. ADR-003: Five Onboarding Paths as Equal-Rank(#21-adr-003-five-onboarding-paths-as-equal-rank)

  - Contents
  - 21. ADR-003: Five Onboarding Paths as Equal-Rank
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 353_

### [22. Glossary of Reference Examples](nautilus/npp-v1-1/22-glossary.md)
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

_Слов: 1560_

### [npp-v1-1](nautilus/npp-v1-1/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 213_

### [AI-Coordinated Infrastructure for Distributed Expert Contribution](nautilus/okwf-concept/00-abstract.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
- Open Knowledge Work Foundation
  - AI-Coordinated Infrastructure for Distributed Expert Contribution
  - Executive Summary
  - Table of Contents
  - Использование
  _... ещё 2 разделов_

_Слов: 541_

### [1. Problem Statement](nautilus/okwf-concept/01-problem-statement.md)
> > !NOTE

  - Содержание
  - 1. Problem Statement
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 671_

### [2. Target Populations](nautilus/okwf-concept/02-target-populations.md)
> > !NOTE

  - Содержание
  - 2. Target Populations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 737_

### [3. Why Existing Solutions Fail](nautilus/okwf-concept/03-why-existing-fail.md)
> > !NOTE

  - Содержание
  - 3. Why Existing Solutions Fail
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 750_

### [4. Proposed Infrastructure](nautilus/okwf-concept/04-proposed-infrastructure.md)
> > !TIP

  - Содержание
  - 4. Proposed Infrastructure
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1032_

### [5. Economic Model](nautilus/okwf-concept/05-economic-model.md)
> > !TIP

  - Содержание
  - 5. Economic Model
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 638_

### [6. Governance and Ethics](nautilus/okwf-concept/06-governance-ethics.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 6. Governance and Ethics
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 653_

### [7. Phased Rollout Plan](nautilus/okwf-concept/07-phased-rollout.md)
> > !NOTE

  - Содержание
  - 7. Phased Rollout Plan
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 708_

### [8. Risk Analysis](nautilus/okwf-concept/08-risk-analysis.md)
> > !TIP

  - Содержание
  - 8. Risk Analysis
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 697_

### [9. Call for Partnership](nautilus/okwf-concept/09-call-for-partnership.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 9. Call for Partnership
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 674_

### [10. Appendices](nautilus/okwf-concept/10-appendices.md)
> > !NOTE

  - Содержание
  - 10. Appendices
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 887_

### [okwf-concept](nautilus/okwf-concept/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 134_

### [Du hast gesagt: Насчёт приватности Я думаю что возможно удалять только личные да…](nautilus/privacy-federation/00-question-anonymization.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 390_

### [Что именно анонимизировать: немецкий стандарт](nautilus/privacy-federation/01-what-to-anonymize-german-standard.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 365_

### [Архитектурное решение: две-уровневая публикация](nautilus/privacy-federation/02-two-tier-publication.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
- В приватном репо cases-private:
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 613_

### [Что это даёт технически](nautilus/privacy-federation/03-what-this-gives-technically.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1581_

### [Что я могу сделать сейчас](nautilus/privacy-federation/04-what-i-can-do-now.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 419_

### [privacy-federation](nautilus/privacy-federation/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 130_

### [Professional Colleague Agents](nautilus/professional-colleague-agents-en/00-abstract.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Содержание
- Professional Colleague Agents
  - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers
  - Abstract
  - Table of Contents
  - Использование
  _... ещё 2 разделов_

_Слов: 599_

### [1. The Five-Type Typology of Principal-Side Agents](nautilus/professional-colleague-agents-en/01-five-type-typology.md)
> > !NOTE

  - Содержание
  - 1. The Five-Type Typology of Principal-Side Agents
  - Смотрите также

_Слов: 948_

### [2. What Makes a Professional Colleague Agent](nautilus/professional-colleague-agents-en/02-what-makes-pca.md)
> > !NOTE

  - Содержание
  - 2. What Makes a Professional Colleague Agent
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 882_

### [3. Empirical Case Study: «Обучай»](nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md)
> > !NOTE

  - Содержание
  - 3. Empirical Case Study: «Обучай»
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 894_

### [4. Architecture of Professional Colleague Agents](nautilus/professional-colleague-agents-en/04-architecture.md)
> > !NOTE

  - Содержание
  - 4. Architecture of Professional Colleague Agents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 930_

### [5. The Economics of Profession-Wide Replication](nautilus/professional-colleague-agents-en/05-economics-replication.md)
> > !NOTE

  - Содержание
  - 5. The Economics of Profession-Wide Replication
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 783_

### [6. Risks Specific to this Category](nautilus/professional-colleague-agents-en/06-risks.md)
> > !TIP

  - Содержание
  - 6. Risks Specific to this Category
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1212_

### [7. Application Domains](nautilus/professional-colleague-agents-en/07-application-domains.md)
> > !TIP

  - Содержание
  - 7. Application Domains
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 759_

### [8. Pilot Proposal: SGB Advocate Colleague](nautilus/professional-colleague-agents-en/08-pilot-sgb-advocate.md)
> > !NOTE

  - Содержание
  - 8. Pilot Proposal: SGB Advocate Colleague
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1017_

### [9. Relationship to Other Agent Types](nautilus/professional-colleague-agents-en/09-relationship-other-agents.md)
> > !NOTE

  - Содержание
  - 9. Relationship to Other Agent Types
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 715_

### [10. Open Questions](nautilus/professional-colleague-agents-en/10-open-questions.md)
> - 10. Open Questions(#10-open-questions)

  - Contents
  - 10. Open Questions
  - Использование
- Поиск по теме документа

_Слов: 484_

### [11. Call for Collaboration](nautilus/professional-colleague-agents-en/11-call-for-collaboration.md)
> - 11. Call for Collaboration(#11-call-for-collaboration)

  - Contents
  - 11. Call for Collaboration
  - Использование
- Поиск по теме документа

_Слов: 442_

### [12. Closing](nautilus/professional-colleague-agents-en/12-closing.md)
> > !NOTE

  - Содержание
  - 12. Closing
  - Acknowledgments
  - References
  - Использование
- Поиск по теме документа

_Слов: 603_

### [professional-colleague-agents-en](nautilus/professional-colleague-agents-en/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 144_

### [Содержание](nautilus/professional-colleague-agents-ru/00-abstract.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 361_

### [1. Типология из пяти типов агентов на стороне принципала](nautilus/professional-colleague-agents-ru/01-pyat-tipov.md)
> > !IMPORTANT

  - Содержание
  - 1. Типология из пяти типов агентов на стороне принципала
  - Смотрите также

_Слов: 887_

### [2. Что делает агента Профессиональным Коллегой](nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md)
> > !TIP

  - Содержание
  - 2. Что делает агента Профессиональным Коллегой
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 778_

### [3. Эмпирический кейс: «Обучай»](nautilus/professional-colleague-agents-ru/03-keys-obuchay.md)
> > !NOTE

  - Содержание
  - 3. Эмпирический кейс: «Обучай»
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 848_

### [4. Архитектура Профессиональных Коллег-Агентов](nautilus/professional-colleague-agents-ru/04-arkhitektura.md)
> > !NOTE

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 894_

### [5. Экономика тиражирования по профессии](nautilus/professional-colleague-agents-ru/05-ekonomika.md)
> > !NOTE

  - Содержание
  - 5. Экономика тиражирования по профессии
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 778_

### [6. Риски, специфичные для этой категории](nautilus/professional-colleague-agents-ru/06-riski.md)
> > !WARNING

  - Содержание
  - 6. Риски, специфичные для этой категории
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1203_

### [7. Области применения](nautilus/professional-colleague-agents-ru/07-oblasti-primeneniya.md)
> > !WARNING

  - Содержание
  - 7. Области применения
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 774_

### [8. Пилотное предложение: SGB Колega-Адвокат](nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md)
> > !WARNING

  - Содержание
  - 8. Пилотное предложение: SGB Колega-Адвокат
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1041_

### [9. Связь с другими типами агентов](nautilus/professional-colleague-agents-ru/09-svyaz-s-drugimi.md)
> > !WARNING

  - Содержание
  - 9. Связь с другими типами агентов
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 677_

### [10. Открытые вопросы](nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md)
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Использование
- Поиск по теме документа

_Слов: 470_

### [11. Призыв к сотрудничеству](nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md)
> - 11. Призыв к сотрудничеству(#11-призыв-к-сотрудничеству)

  - Contents
  - 11. Призыв к сотрудничеству
  - Использование
- Поиск по теме документа

_Слов: 433_

### [12. Заключение](nautilus/professional-colleague-agents-ru/12-zaklyuchenie.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 12. Заключение
  - Благодарности
  - Ссылки
  - Использование
- Поиск по теме документа
- Поиск (bm25)
  _... ещё 2 разделов_

_Слов: 667_

### [professional-colleague-agents-ru](nautilus/professional-colleague-agents-ru/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 145_

### [AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations](nautilus/representative-agent-layer-en/00-abstract.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
- The Representative Agent Layer
  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations
  - Abstract
  - Table of Contents
  - Использование
  _... ещё 2 разделов_

_Слов: 558_

### [1. The Cinderella Syndrome: Why Quality Stays Invisible](nautilus/representative-agent-layer-en/01-cinderella-syndrome.md)
> > !NOTE

  - Содержание
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 883_

### [2. Historical Precedents: Agents as Civilizational Innovation](nautilus/representative-agent-layer-en/02-historical-precedents.md)
> > !NOTE

  - Содержание
  - 2. Historical Precedents: Agents as Civilizational Innovation
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 998_

### [3. What Makes a Representative Agent](nautilus/representative-agent-layer-en/03-what-makes-representative-agent.md)
> > !NOTE

  - Содержание
  - 3. What Makes a Representative Agent
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 711_

### [4. Ten Domains of Application](nautilus/representative-agent-layer-en/04-ten-domains.md)
> > !TIP

  - Содержание
  - 4. Ten Domains of Application
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1617_

### [5. Architectural Specification](nautilus/representative-agent-layer-en/05-architectural-specification.md)
> > !NOTE

  - Содержание
  - 5. Architectural Specification
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 707_

### [6. Ethical Framework](nautilus/representative-agent-layer-en/06-ethical-framework.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 6. Ethical Framework
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 626_

### [7. Governance and Oversight](nautilus/representative-agent-layer-en/07-governance-oversight.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 7. Governance and Oversight
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 552_

### [8. Risks and Mitigations](nautilus/representative-agent-layer-en/08-risks-mitigations.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 8. Risks and Mitigations
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 708_

### [9. Phased Rollout Strategy](nautilus/representative-agent-layer-en/09-phased-rollout.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 9. Phased Rollout Strategy
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 697_

### [10. Open Questions](nautilus/representative-agent-layer-en/10-open-questions.md)
> - 10. Open Questions(#10-open-questions)

  - Contents
  - 10. Open Questions
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 490_

### [11. Call for Collaboration](nautilus/representative-agent-layer-en/11-call-for-collaboration.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 11. Call for Collaboration
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 570_

### [12. Closing](nautilus/representative-agent-layer-en/12-closing.md)
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

_Слов: 2748_

### [representative-agent-layer-en](nautilus/representative-agent-layer-en/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 148_

### [Содержание](nautilus/representative-agent-layer-ru/00-abstract.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 359_

### [1. Синдром Золушки: Почему качество остаётся невидимым](nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md)
> > !NOTE

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 838_

### [2. Исторические прецеденты: Агенты как цивилизационная инновация](nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md)
> > !WARNING

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 977_

### [3. Что делает агента Представительским](nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md)
> > !TIP

  - Содержание
  - 3. Что делает агента Представительским
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 667_

### [4. Десять областей применения](nautilus/representative-agent-layer-ru/04-desyat-oblastey.md)
> > !WARNING

  - Содержание
  - 4. Десять областей применения
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1629_

### [5. Архитектурная спецификация](nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md)
> > !NOTE

  - Содержание
  - 5. Архитектурная спецификация
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 688_

### [6. Этическая рамка](nautilus/representative-agent-layer-ru/06-eticheskaya-ramka.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 6. Этическая рамка
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 630_

### [7. Управление и надзор](nautilus/representative-agent-layer-ru/07-upravlenie-nadzor.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 7. Управление и надзор
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 552_

### [8. Риски и меры противодействия](nautilus/representative-agent-layer-ru/08-riski-mery.md)
> > !WARNING

  - Содержание
  - 8. Риски и меры противодействия
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 633_

### [9. Стратегия поэтапного развёртывания](nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 9. Стратегия поэтапного развёртывания
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 688_

### [10. Открытые вопросы](nautilus/representative-agent-layer-ru/10-otkrytye-voprosy.md)
> - 10. Открытые вопросы(#10-открытые-вопросы)

  - Contents
  - 10. Открытые вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 479_

### [11. Призыв к сотрудничеству](nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md)
> - 11. Призыв к сотрудничеству(#11-призыв-к-сотрудничеству)

  - Contents
  - 11. Призыв к сотрудничеству
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 494_

### [12. Заключение](nautilus/representative-agent-layer-ru/12-zaklyuchenie.md)
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

_Слов: 4495_

### [representative-agent-layer-ru](nautilus/representative-agent-layer-ru/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 147_

### [TL;DR — Трёхфазная методология Review](nautilus/review-methodology/00-tldr.md)
> - TL;DR(#tldr)

  - Contents
- Трёхфазная методология Review в Nautilus
  - TL;DR
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 346_

### [1. Контекст и мотивация](nautilus/review-methodology/01-context-motivation.md)
> - 1. Контекст и мотивация(#1-контекст-и-мотивация)

  - Contents
  - 1. Контекст и мотивация
  - Смотрите также

_Слов: 447_

### [2. Формальный workflow](nautilus/review-methodology/02-formal-workflow.md)
> - 2. Формальный workflow(#2-формальный-workflow)

  - Contents
  - 2. Формальный workflow
  - Смотрите также

_Слов: 487_

### [3. Принципы консолидации (Фаза C)](nautilus/review-methodology/03-consolidation-principles.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - 3. Принципы консолидации (Фаза C)
- LOC в Python-коде
- Количество тестов
- Число адаптеров
- Health score
- Q6-покрытие
  _... ещё 1 разделов_

_Слов: 567_

### [Вопрос: fallback‑ratio как критический или осмысленный?](nautilus/review-methodology/04-fallback-ratio-question.md)
> - Вопрос: fallback-ratio как критический или осмысленный?(#вопрос-fallback-ratio-как-критический-или-осмысленный)

  - Contents
  - Вопрос: fallback-ratio как критический или осмысленный?
  - Смотрите также

_Слов: 342_

### [4. Условия применимости](nautilus/review-methodology/05-conditions-of-applicability.md)
> - 4. Условия применимости(#4-условия-применимости)

  - Contents
  - 4. Условия применимости
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 342_

### [5. Связь с существующими методологиями](nautilus/review-methodology/06-relation-existing-methodologies.md)
> - 5. Связь с существующими методологиями(#5-связь-с-существующими-методологиями)

  - Contents
  - 5. Связь с существующими методологиями
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 432_

### [6. Почему это валидный паттерн для AI‑assisted workflows](nautilus/review-methodology/07-why-valid-for-ai.md)
> - 6. Почему это валидный паттерн для AI-assisted workflows(#6-почему-это-валидный-паттерн-для-ai-assisted-workflows)

  - Contents
  - 6. Почему это валидный паттерн для AI-assisted workflows
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [7. Реализация в проекте Nautilus](nautilus/review-methodology/08-implementation-nautilus.md)
> - 7. Реализация в проекте Nautilus(#7-реализация-в-проекте-nautilus)

  - Contents
  - 7. Реализация в проекте Nautilus
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 376_

### [8. Ограничения и открытые вопросы](nautilus/review-methodology/09-limitations-open-questions.md)
> - 8. Ограничения и открытые вопросы(#8-ограничения-и-открытые-вопросы)

  - Contents
  - 8. Ограничения и открытые вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 466_

### [9. Checklist применения методологии](nautilus/review-methodology/10-checklist.md)
> - 9. Checklist применения методологии(#9-checklist-применения-методологии)

  - Contents
  - 9. Checklist применения методологии
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 410_

### [10. Конкретный план применения к текущим документам](nautilus/review-methodology/11-application-plan-current-docs.md)
> - 10. Конкретный план применения к текущим документам(#10-конкретный-план-применения-к-текущим-документам)

  - Contents
  - 10. Конкретный план применения к текущим документам
- В Termux
  - Смотрите также

_Слов: 346_

### [Appendix A: Шаблон для header warning](nautilus/review-methodology/12-appendix-a-header-warning.md)
> - Appendix A: Шаблон для header warning(#appendix-a-шаблон-для-header-warning)

  - Contents
  - Appendix A: Шаблон для header warning
  - Смотрите также

_Слов: 352_

### [Appendix B: Примеры расхождений и их разрешения](nautilus/review-methodology/13-appendix-b-examples.md)
> - Appendix B: Примеры расхождений и их разрешения(#appendix-b-примеры-расхождений-и-их-разрешения)

  - Contents
  - Appendix B: Примеры расхождений и их разрешения
  - Смотрите также

_Слов: 359_

### [Главные технические риски](nautilus/review-methodology/14-main-technical-risks.md)
> - Главные технические риски(#главные-технические-риски)

  - Contents
  - Главные технические риски
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 347_

### [Appendix C: История изменений методологии](nautilus/review-methodology/15-appendix-c-history.md)
> - Appendix C: История изменений методологии(#appendix-c-история-изменений-методологии)

  - Contents
  - Appendix C: История изменений методологии
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 360_

### [Глоссарий](nautilus/review-methodology/16-glossary.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Глоссарий
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 1054_

### [review-methodology](nautilus/review-methodology/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 191_

### [Du hast gesagt: Спрос рождает предложение - это простая экономическая истина нач…](nautilus/supply-demand/00-question-supply-demand.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 563_

### [Claude hat geantwortet: Очень богатый вопрос — три разных, но связанных темы.](nautilus/supply-demand/01-three-related-themes.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 3020_

### [supply-demand](nautilus/supply-demand/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 110_

### [Du hast gesagt: Того если гора не идёт человеку может быть этот человек пойдёт к…](nautilus/transmission-box/00-question-mountain-to-person.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 637_

### [Claude hat geantwortet: Это исключительно богатый вопрос, и я хочу ответить на н…](nautilus/transmission-box/01-completing-loop.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
- Альтернативный поиск (BM25)
  - Смотрите также

_Слов: 3229_

### [transmission-box](nautilus/transmission-box/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 110_

**Итого в секции: 176,913 слов, 255 файлов**


## Processing Guide

_Путь: `docs/processing-guide/`_

### [Обработка больших массивов информации — Часть 1: Обзор и таксономия](processing-guide/01-overview.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Проблема
  - Таксономия методов
  - Что реализовано в Lorenzo
  - Навигация по разделам
  - Смотрите также

_Слов: 577_

### [Обработка больших массивов — Часть 2: Извлечение](processing-guide/02-extraction.md)
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

_Слов: 642_

### [Обработка больших массивов — Часть 3: Разбивка и чанкинг](processing-guide/03-chunking.md)
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

_Слов: 684_

### [Обработка больших массивов — Часть 4: Структурирование](processing-guide/04-structuring.md)
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

_Слов: 746_

### [Обработка больших массивов — Часть 5: Анализ и NLP](processing-guide/05-analysis.md)
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

_Слов: 931_

### [Обработка больших массивов — Часть 6: Поиск](processing-guide/06-search.md)
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

_Слов: 985_

### [Обработка больших массивов — Часть 7: LLM-обогащение](processing-guide/07-llm.md)
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

_Слов: 904_

### [Обработка больших массивов — Часть 8: Экспорт и интеграции](processing-guide/08-export.md)
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

_Слов: 769_

### [Обработка больших массивов — Часть 9: Автоматизация](processing-guide/09-automation.md)
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

_Слов: 906_

### [Обработка больших массивов — Часть 10: Инновационные подходы](processing-guide/10-future.md)
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

_Слов: 1805_

### [Обработка больших массивов документов — Полное руководство](processing-guide/PROCESSING_GUIDE.md)
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

_Слов: 8107_

### [Q&A: processing-guide](processing-guide/QA.md)
> > !NOTE

  - Какие системы памяти описаны в этом разделе?
  - Как происходит консолидация и забывание в памяти агентов?
  - Какова разница между эпизодической и семантической памятью?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  _... ещё 12 разделов_

_Слов: 315_

### [processing-guide](processing-guide/README.md)
> Файлов: 12

  - Содержание
  - Использование
- Запуск

_Слов: 129_

**Итого в секции: 17,500 слов, 13 файлов**


## Svyazi 2 0

_Путь: `docs/svyazi-2-0/`_

### [Q&A: svyazi-2-0](svyazi-2-0/QA.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Как работает AgentFS и что такое .agentos?
  - Что такое knowledge-space и для кого он предназначен?
  - Как CardIndex хранит и версионирует карточки?
  _... ещё 3 разделов_

_Слов: 473_

### [svyazi-2-0](svyazi-2-0/README.md)
> > !NOTE

  - Содержание
  - Подразделы
  - Использование
- Запуск

_Слов: 141_

### [architecture](svyazi-2-0/architecture/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 131_

### [Card Envelope](svyazi-2-0/architecture/card-envelope.md)
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [Evidence Envelope](svyazi-2-0/architecture/evidence-envelope.md)
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Особые случаи
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 324_

### [Архитектурные зазоры](svyazi-2-0/architecture/gaps.md)
> > !TIP

  - Содержание
  - Пять зазоров, важнее поиска ещё десяти инструментов
  - Сводная таблица зазоров
  - Главный практический принцип
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 654_

### [Интеграционная спецификация (минимум для MVP)](svyazi-2-0/architecture/integration-spec.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 338_

### [Memory Write Policy](svyazi-2-0/architecture/memory-write-policy.md)
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [Review Record](svyazi-2-0/architecture/review-record.md)
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 326_

### [Skill and Tool Policy](svyazi-2-0/architecture/skill-tool-policy.md)
> - Минимальные поля(#минимальные-поля)

  - Contents
  - Минимальные поля
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [components](svyazi-2-0/components/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 203_

### [agent-memory-mcp + Memory OS](svyazi-2-0/components/agent-memory-mcp.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 324_

### [AgentFS](svyazi-2-0/components/agentfs.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 323_

### [AI Factory + AIF Handoff](svyazi-2-0/components/ai-factory.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 331_

### [AutoResearch + Sequential](svyazi-2-0/components/autoresearch-sequential.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 328_

### [Graph RAG](svyazi-2-0/components/graph-rag.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 324_

### [Hybrid RAG knowledge base](svyazi-2-0/components/hybrid-rag.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 329_

### [knowledge-space](svyazi-2-0/components/knowledge-space.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 321_

### [Legal RAG](svyazi-2-0/components/legal-rag.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [mclaude](svyazi-2-0/components/mclaude.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [MemNet / memory-is-all-you-need](svyazi-2-0/components/memnet.md)
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

_Слов: 322_

### [NGT Memory](svyazi-2-0/components/ngt-memory.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 326_

### [research-docs + LiteParse](svyazi-2-0/components/research-docs-liteparse.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 326_

### [Rufler](svyazi-2-0/components/rufler.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Security + routing plane](svyazi-2-0/components/security-routing-plane.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Числовые наблюдения
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [Self‑Aware MCP + Skills + CodeWiki](svyazi-2-0/components/self-aware-mcp.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 323_

### [Svyazi](svyazi-2-0/components/svyazi.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 332_

### [Voice / local-first stack](svyazi-2-0/components/voice-stack.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 325_

### [Yjs + Automerge](svyazi-2-0/components/yjs-automerge.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 324_

### [Yodoca](svyazi-2-0/components/yodoca.md)
> - Описание(#описание)

  - Contents
  - Описание
  - Ключевые компоненты и паттерны
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 325_

### [Ансамбль A — Collaboration OS](svyazi-2-0/ensembles/A-collaboration-os.md)
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 344_

### [Ансамбль B — Forensic RAG для доказуемого matching и review](svyazi-2-0/ensembles/B-forensic-rag.md)
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 349_

### [Ансамбль C — Spec‑driven multi‑agent factory](svyazi-2-0/ensembles/C-multi-agent-factory.md)
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 346_

### [Ансамбль D — Voice‑first local knowledge mesh](svyazi-2-0/ensembles/D-voice-first-mesh.md)
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 349_

### [Ансамбль E — Safe and cheap execution plane](svyazi-2-0/ensembles/E-execution-plane.md)
> - Схема(#схема)

  - Contents
  - Схема
  - Ожидаемые новые свойства
  - Смотрите также

_Слов: 349_

### [Ансамбль F — Evidence‑Backed Community Intake](svyazi-2-0/ensembles/F-evidence-backed-intake.md)
> - Схема(#схема)

  - Contents
  - Схема
  - Новые свойства
  - Смотрите также

_Слов: 352_

### [Ансамбль G — Federated Local‑First Community Graph](svyazi-2-0/ensembles/G-federated-local-graph.md)
> - Схема(#схема)

  - Contents
  - Схема
  - Новое свойство
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 353_

### [Ансамбль H — Research‑to‑Product Flywheel](svyazi-2-0/ensembles/H-research-to-product-flywheel.md)
> - Схема(#схема)

  - Contents
  - Схема
  - Новое свойство
  - Смотрите также

_Слов: 346_

### [Ансамбли проектов](svyazi-2-0/ensembles/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 138_

### [limitations](svyazi-2-0/limitations/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 116_

### [Итоговые выводы и порядок сборки](svyazi-2-0/limitations/conclusions.md)
> - Главный вывод первой части(#главный-вывод-первой-части)

  - Contents
  - Главный вывод первой части
  - Порядок практической сборки
  - Главный вывод второй части
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 423_

### [Что пока лучше не склеивать](svyazi-2-0/limitations/do-not-glue.md)
> - Оркестрация — выбрать один spine(#оркестрация-выбрать-один-spine)

  - Contents
  - Оркестрация — выбрать один spine
  - Voice/local‑first mesh — не идеализировать
  - Self‑improvement — только после метрики
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 429_

### [Лицензионные развилки](svyazi-2-0/limitations/license-tree.md)
> - Развилки в коротком виде(#развилки-в-коротком-виде)

  - Contents
  - Развилки в коротком виде
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 401_

### [outreach](svyazi-2-0/outreach/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 118_

### [Первые контакты](svyazi-2-0/outreach/first-contacts.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Шаблон первого сообщения](svyazi-2-0/outreach/message-template.md)
> - Замечание(#замечание)

  - Contents
  - Замечание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Узкие вопросы для каждого автора](svyazi-2-0/outreach/narrow-questions.md)
> - Адресные вопросы(#адресные-вопросы)

  - Contents
  - Адресные вопросы
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 406_

### [overview](svyazi-2-0/overview/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 124_

### [Что добавляет продолжение исследования](svyazi-2-0/overview/continuation-intro.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 344_

### [Executive summary](svyazi-2-0/overview/executive-summary.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 448_

### [Методика и рамка отбора](svyazi-2-0/overview/methodology.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 348_

### [Карта найденных проектов и паттернов](svyazi-2-0/overview/projects-map.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 1377_

### [prototype](svyazi-2-0/prototype/README.md)
> > README — раздел документации проекта Lorenzo.

  - Содержание
  - Использование
- Запуск

_Слов: 102_

### [План MVP-прототипа](svyazi-2-0/prototype/mvp-plan.md)
> - Минимальная сборка прототипа(#минимальная-сборка-прототипа)

  - Contents
  - Минимальная сборка прототипа
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 389_

### [Ключевые риски и как их закрывать](svyazi-2-0/prototype/risks.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 363_

### [Дорожная карта прототипа](svyazi-2-0/prototype/roadmap.md)
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

_Слов: 669_

### [security](svyazi-2-0/security/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 118_

### [Практичный бюджетный роутинг моделей](svyazi-2-0/security/budget-routing.md)
> - Обоснование(#обоснование)

  - Contents
  - Обоснование
  - Три режима
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 408_

### [Что стоит зафиксировать как default policy](svyazi-2-0/security/default-policy.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 419_

### [Приватность: local-first by default](svyazi-2-0/security/privacy.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 358_

**Итого в секции: 20,715 слов, 60 файлов**


## Technology Combinations

_Путь: `docs/technology-combinations/`_

### [technology-combinations/ — комбинирование технологий для новых свойств](technology-combinations/README.md)
> > !TIP

  - Содержание
  - Источник
  - Подпапки
  - Главная находка диалога
  - См. также
  - Использование

_Слов: 363_

### [Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн](technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 328_

### [Комбинация 2: Мультиагентный хаос-решение × Auto AI Router](technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 3: CRDT local-first × Svyazi CardIndex](technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 321_

### [Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура](technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной](technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер](technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 7: Crawl4AI × Docling × Yodoca consolidator](technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 8: Conductor × adversarial-review × Auto AI Router](technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 790_

### [Комбинация 9: Agent Orchestration Stack](technology-combinations/combinations/09-agent-orchestration-stack.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 10: Legal Document Intelligence Pipeline](technology-combinations/combinations/10-legal-document-intelligence-pipeline.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [Комбинация 11: Hybrid CRDT-SQL Database](technology-combinations/combinations/11-hybrid-crdt-sql-database.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 12: Multi-Agent Observability Stack](technology-combinations/combinations/12-multi-agent-observability-stack.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Комбинация 13: Legal Document Transpiler](technology-combinations/combinations/13-legal-document-transpiler.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 14: local-first Agent Development Environment](technology-combinations/combinations/14-local-first-agent-development-environment.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 681_

### [Комбинация 15: Self-Consolidating Legal Corpus](technology-combinations/combinations/15-self-consolidating-legal-corpus.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 16: Adversarial Multi-Agent Code Review](technology-combinations/combinations/16-adversarial-multi-agent-code-review.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 358_

### [Комбинация 17: Distributed Agent Memory with Graph](technology-combinations/combinations/17-distributed-agent-memory-with-graph.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Комбинация 18: LLM-Powered Legal Corpus Builder](technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md)
> - Использование(#использование)

  - Contents
- Crawl4AI pipeline
- Svyazi deduplication
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 322_

### [Комбинация 19: Multi-Agent Observability Platform](technology-combinations/combinations/19-multi-agent-observability-platform.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 797_

### [Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync](technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 340_

### [Комбинация 21: Legal Corpus Analytics at Scale](technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md)
> - Использование(#использование)

  - Contents
- Pipeline
- Schema
- Analytics queries (subsecond)
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 333_

### [Комбинация 22: Russian-International OSS Stack](technology-combinations/combinations/22-russian-international-oss-stack.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 23: Security-First Code Review Pipeline](technology-combinations/combinations/23-security-first-code-review-pipeline.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 354_

### [Комбинация 24: MEGA-INTEGRATION: Full Stack](technology-combinations/combinations/24-mega-integration-full-stack.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 713_

### [Комбинация 25: Legal DSL → Code Transpiler](technology-combinations/combinations/25-legal-dsl-code-transpiler.md)
> - Использование(#использование)

  - Contents
- DSL syntax (natural language-like)
- DSL operations
- Output: ready Widerspruch.docx
- DSL for conversion
  - Использование
- Поиск по теме документа
  - Смотрите также
  _... ещё 1 разделов_

_Слов: 336_

### [Комбинация 26: AST-Based Code Analysis for Legal Automation](technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md)
> - Использование(#использование)

  - Contents
- Input: Python script for Fristwahrung calculation
- AST analysis
- Extract legal logic
- → Pydantic model: LegalRule(
- name="Widerspruchsfrist",
- baseduration=timedelta(days(),
- extensions=[...],
  _... ещё 7 разделов_

_Слов: 351_

### [Комбинация 27: Hybrid RAG with AST-Chunked Code](technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 28: Pydantic-Enforced Legal Workflows](technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md)
> - Использование(#использование)

  - Contents
- Sequential pipeline with Pydantic validation at each stage
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 29: Meta-Programmatic Legal Template Generator](technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md)
> - Использование(#использование)

  - Contents
- Legal DSL (declarative)
- Compiler generates Python code
- auto-generated rendering logic
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Комбинация 30: MEGA-STACK 3.0 with DSL & AST](technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 611_

### [Комбинация 31: Event-Sourced Legal Document History](technology-combinations/combinations/31-event-sourced-legal-document-history.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 328_

### [Комбинация 32: Consensus-Based Multi-Agent Coordination](technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics](technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 34: Distributed Event Store with Paxos](technology-combinations/combinations/34-distributed-event-store-with-paxos.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 322_

### [Комбинация 35: MEGA-STACK 4.0 with Event Sourcing & Consensus](technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md)
> - Содержание(#содержание)

  - Contents
  - Содержание
- Events
- Event Store
- Time-travel query
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 576_

### [combinations](technology-combinations/combinations/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 299_

### [Mega‑Stack 1.0 — Полный Legal‑AI Stack](technology-combinations/mega-stacks/01-legal-ai-stack.md)
> - Результат(#результат)

  - Contents
  - Результат
  - Первый проект для внедрения
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 320_

### [Mega‑Stack 2.0 — Ultimate Legal‑AI System](technology-combinations/mega-stacks/02-ultimate-legal-ai.md)
> - Capabilities(#capabilities)

  - Contents
  - Capabilities
  - First implementation priority
  - Смотрите также

_Слов: 409_

### [Mega‑Stack 3.0 — with DSL & AST](technology-combinations/mega-stacks/03-dsl-ast.md)
> - New capabilities(#new-capabilities)

  - Contents
  - New capabilities
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 320_

### [Mega‑Stack 4.0 — with Event Sourcing & Consensus](technology-combinations/mega-stacks/04-event-sourcing-consensus.md)
> - New capabilities(#new-capabilities)

  - Contents
  - New capabilities
  - Performance
  - Смотрите также
  - Кто ссылается на этот документ (3)

_Слов: 369_

### [mega-stacks](technology-combinations/mega-stacks/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 124_

### [properties/ — эмерджентные свойства](technology-combinations/properties/README.md)
> > properties/ — эмерджентные свойства

  - Содержание
  - Шаблон файла
- <Название свойства>
  - Что это
  - Какие компоненты дают это свойство в комбинации
  - Почему ни один из них в отдельности не даёт свойства
  - Как проверить, что свойство реально появилось
  - Смотрите также

_Слов: 351_

### [research-reports](technology-combinations/research-reports/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 110_

### [Research Report: Continuation — 10 New Domains Beyond the Original 45 Combinations](technology-combinations/research-reports/continuation-10-domains.md)
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

_Слов: 449_

### [Research Report: Sozialrecht (35 комбинаций)](technology-combinations/research-reports/sozialrecht-35-combinations.md)
> - Что в отчёте(#что-в-отчёте)

  - Contents
  - Что в отчёте
  - Артефакт документа
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Сводная таблица 1–8](technology-combinations/synthesis-tables/01-08-summary.md)
> - 🎯 Главная находка: паттерн «скромные родители → мощные дети»(#главная-находка-паттерн-скромные-родители-мощные-дети)

  - Contents
  - 🎯 Главная находка: паттерн «скромные родители → мощные дети»
  - Рекомендация
  - Использование
- Поиск по теме документа
  - Смотрите также
  - Кто ссылается на этот документ (4)

_Слов: 490_

### [Сводная таблица 9–14 (Extended)](technology-combinations/synthesis-tables/09-14-extended.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Сводная таблица 15–19 (Extended)](technology-combinations/synthesis-tables/15-19-extended.md)
> - Использование(#использование)

  - Contents
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Сводная таблица 20–24 (Final 1–24)](technology-combinations/synthesis-tables/20-24-final.md)
> - Рекомендация(#рекомендация)

  - Contents
  - Рекомендация
  - Использование
- Поиск по теме документа
  - Смотрите также

_Слов: 351_

### [Сводная таблица 25–30 (Complete 1–30)](technology-combinations/synthesis-tables/25-30-extended.md)
> - Рекомендация(#рекомендация)

  - Contents
  - Рекомендация
  - Смотрите также

_Слов: 349_

### [Сводная таблица 31–35 (Complete 1–35)](technology-combinations/synthesis-tables/31-35-final.md)
> - Рекомендация(#рекомендация)

  - Contents
  - Рекомендация
- Events
- Event Store (append-only)
- Time-travel query
  - Смотрите также

_Слов: 349_

### [synthesis-tables](technology-combinations/synthesis-tables/README.md)
> > !NOTE

  - Содержание
  - Использование
- Запуск

_Слов: 132_

**Итого в секции: 19,585 слов, 53 файлов**


## Templates

_Путь: `docs/templates/`_

### [templates](templates/README.md)
> > !NOTE

  - Содержание
  - Подразделы
  - Использование
- Запуск

_Слов: 193_

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

_Слов: 438_

### [Контакт: [Имя / Проект]](templates/contact-outreach.md)
> > !NOTE

  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы для обсуждения

_Слов: 158_

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

_Слов: 364_

### [ADR: [Название решения]](templates/decision-record.md)
> > !NOTE

  - Статус
  - Контекст
  - Рассмотренные варианты
  - Принятое решение
  - Последствия
  - Использование
- Запуск

_Слов: 134_

### [Ансамбль: [Название]](templates/ensemble.md)
> > !NOTE

  - Назначение
  - Компоненты
  - Архитектурная схема
  - Контракт взаимодействия
  - Риски и ограничения
  - MVP-шаги

_Слов: 154_

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

_Слов: 365_

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

_Слов: 366_

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

_Слов: 368_

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

_Слов: 371_

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

_Слов: 372_

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

_Слов: 362_

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

_Слов: 428_

### [[Название компонента]](templates/project-component.md)
> > !NOTE

  - Что это
  - Ключевые особенности
  - Статус
  - Интеграция с Svyazi
  - Контакты
  - Использование
- Запуск

_Слов: 152_

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

_Слов: 431_

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

_Слов: 445_

### [[Тема исследования]](templates/research-note.md)
> > !NOTE

  - Контекст
  - Ключевые находки
  - Источники
  - Открытые вопросы
  - Следующие шаги
  - Использование
- Запуск

_Слов: 131_

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

_Слов: 373_

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

_Слов: 341_

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

_Слов: 371_

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

_Слов: 362_

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

_Слов: 363_

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

_Слов: 382_

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

_Слов: 367_

**Итого в секции: 7,791 слов, 24 файлов**


## 🗺️ Тематическая карта

### Архитектура (548 документов)
- [`365-развёрнутый-анализ-внуковой-комбинации`](02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md)
- [`CONCEPTS`](CONCEPTS.md)
- [`TABLES`](TABLES.md)
- [`00-intro`](02-anthropic-vacancies/00-intro.md)
- [`01-интегральный-анализ-профиля-svend4`](02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)
- _... ещё 543_

### Документация (169 документов)
- [`118-appendix-a-шаблон-для-header-warning`](02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md)
- [`98-appendix-a-minimal-working-example`](02-anthropic-vacancies/98-appendix-a-minimal-working-example.md)
- [`NAMED_ENTITIES`](NAMED_ENTITIES.md)
- [`22-glossary`](nautilus/npp-v1-1/22-glossary.md)
- [`12-appendix-a-header-warning`](nautilus/review-methodology/12-appendix-a-header-warning.md)
- _... ещё 164_

### Проекты (154 документов)
- [`CODE_BLOCKS`](CODE_BLOCKS.md)
- [`TIMELINE`](TIMELINE.md)
- [`02-общий-план-развития-nautilus-portal-protocol`](02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md)
- [`228-appendix-c-quick-start-architecture-for-sgb-advoca`](02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md)
- [`299-практические-рекомендации-для-текущего-проекта`](02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md)
- _... ещё 149_

### Агенты (132 документов)
- [`C-multi-agent-factory`](svyazi-2-0/ensembles/C-multi-agent-factory.md)
- [`107-1-контекст-и-мотивация`](02-anthropic-vacancies/107-1-контекст-и-мотивация.md)
- [`108-2-формальный-workflow`](02-anthropic-vacancies/108-2-формальный-workflow.md)
- [`345-кто-ты`](02-anthropic-vacancies/345-кто-ты.md)
- [`357-твоя-коммуникация-в-outreach`](02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md)
- _... ещё 127_

### Код (111 документов)
- [`193-3-что-делает-агента-представительским`](02-anthropic-vacancies/193-3-что-делает-агента-представительским.md)
- [`DEPENDENCY_MAP`](DEPENDENCY_MAP.md)
- [`02-architecture`](meta-scripting/02-architecture.md)
- [`04-enrichment`](meta-scripting/04-enrichment.md)
- [`111-4-условия-применимости`](02-anthropic-vacancies/111-4-условия-применимости.md)
- _... ещё 106_

### Контакты (52 документов)
- [`ngt-memory`](05-habr-projects/memory/ngt-memory.md)
- [`CONTACT_PRIORITY`](CONTACT_PRIORITY.md)
- [`REGISTRY`](REGISTRY.md)
- [`06-1-introduction`](02-anthropic-vacancies/06-1-introduction.md)
- [`105-review-methodology-md`](02-anthropic-vacancies/105-review-methodology-md.md)
- _... ещё 47_

### Память (39 документов)
- [`PROCESSING_GUIDE`](processing-guide/PROCESSING_GUIDE.md)
- [`SCRIPT_EVAL_REPORT`](SCRIPT_EVAL_REPORT.md)
- [`06-search`](processing-guide/06-search.md)
- [`11-integration-contracts`](01-svyazi/11-integration-contracts.md)
- [`CHANGELOG_AUTO`](CHANGELOG_AUTO.md)
- _... ещё 34_

### Анализ (25 документов)
- [`72-расписание-фазы-3`](02-anthropic-vacancies/72-расписание-фазы-3.md)
- [`110-вопрос-fallback-ratio-как-критический-или-осмыслен`](02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md)
- [`145-8-call-to-action`](02-anthropic-vacancies/145-8-call-to-action.md)
- [`154-table-of-contents`](02-anthropic-vacancies/154-table-of-contents.md)
- [`162-8-risk-analysis`](02-anthropic-vacancies/162-8-risk-analysis.md)
- _... ещё 20_



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

**Кто ссылается на этот документ (667):**
- [00-intro-part2](01-svyazi/00-intro-part2.md)
- [02-methodology](01-svyazi/02-methodology.md)
- [06-security-privacy](01-svyazi/06-security-privacy.md)
- [08-conclusions](01-svyazi/08-conclusions.md)
- [12-roadmap](01-svyazi/12-roadmap.md)
- [14-limitations](01-svyazi/14-limitations.md)
- [QA](01-svyazi/QA.md)
- [110-вопрос-fallback-ratio-как-критический-или-осмыслен](02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md)
- _...ещё 659_


<!-- similar-docs -->

---

**Похожие документы:**
- [OUTLINE](obsidian/OUTLINE.md) (сходство 1.00)
- [EMPTY_SECTIONS](EMPTY_SECTIONS.md) (сходство 0.48)
- [EMPTY_SECTIONS](obsidian/EMPTY_SECTIONS.md) (сходство 0.48)


<!-- see-also -->

---

**Смотрите также:**
- [EMPTY_SECTIONS](EMPTY_SECTIONS.md)
- [HEADING_AUDIT](HEADING_AUDIT.md)
- [PARAGRAPH_QUALITY](PARAGRAPH_QUALITY.md)
- [TABLES](TABLES.md)

