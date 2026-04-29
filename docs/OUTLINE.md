# Outline базы знаний

<!-- summary -->
> Секций: **18** | Файлов: **1158**
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse

---

<!-- toc -->
## Содержание

- [Содержание](#содержание)
- [📁 Docs (`docs/`)](#docs-docs)
  - [[Словарь аббревиатур и сокращений](docs/ABBREVIATIONS.md)](#словарь-аббревиатур-и-сокращенийdocsabbreviationsmd)
  - [[Action Items, риски и решения](docs/ACTION_ITEMS.md)](#action-items-риски-и-решенияdocsaction_itemsmd)
  - [[Callout-блоки](docs/ALERTS.md)](#callout-блокиdocsalertsmd)
  - [[Авторы и коллаборации](docs/AUTHORS.md)](#авторы-и-коллаборацииdocsauthorsmd)
  - [[Автозаполненные шаблоны](docs/AUTOFILLED.md)](#автозаполненные-шаблоныdocsautofilledmd)
  - [[Индекс обратных ссылок](docs/BACKLINKS.md)](#индекс-обратных-ссылокdocsbacklinksmd)
  - [[CHANGELOG](docs/CHANGELOG.md)](#changelogdocschangelogmd)
  - [[Changelog (авто)](docs/CHANGELOG_AUTO.md)](#changelog-автоdocschangelog_automd)
  - [[Кластеры тематически близких файлов](docs/CLUSTERS.md)](#кластеры-тематически-близких-файловdocsclustersmd)
  - [[Code-блоки репозитория](docs/CODE_BLOCKS.md)](#code-блоки-репозиторияdocscode_blocksmd)
  - [[Сравнение с предыдущим коммитом](docs/COMPARE.md)](#сравнение-с-предыдущим-коммитомdocscomparemd)
  - [[Оценка читаемости документов](docs/COMPLEXITY.md)](#оценка-читаемости-документовdocscomplexitymd)
  - [[Матрица компонентов Svyazi 2.0](docs/COMPONENT_MATRIX.md)](#матрица-компонентов-svyazi-20docscomponent_matrixmd)
  - [[Глоссарий понятий](docs/CONCEPTS.md)](#глоссарий-понятийdocsconceptsmd)
  - [[Граф концептов базы знаний](docs/CONCEPT_GRAPH.md)](#граф-концептов-базы-знанийdocsconcept_graphmd)
  - [[Согласованность терминов](docs/CONSISTENCY.md)](#согласованность-терминовdocsconsistencymd)
  - [[Контакты и авторы](docs/CONTACTS.md)](#контакты-и-авторыdocscontactsmd)
  - [[Приоритет контактов](docs/CONTACT_PRIORITY.md)](#приоритет-контактовdocscontact_prioritymd)
  - [[Противоречия в базе знаний](docs/CONTRADICTIONS.md)](#противоречия-в-базе-знанийdocscontradictionsmd)
  - [[Оценка стоимости MVP](docs/COST.md)](#оценка-стоимости-mvpdocscostmd)
  - [[Перекрёстные ссылки](docs/CROSSREFS.md)](#перекрёстные-ссылкиdocscrossrefsmd)
  - [[Кросс-секционный анализ](docs/CROSS_SECTION.md)](#кросс-секционный-анализdocscross_sectionmd)
  - [[Ключевые решения и выводы](docs/DECISIONS.md)](#ключевые-решения-и-выводыdocsdecisionsmd)
  - [[Карта плотности тем](docs/DENSITY.md)](#карта-плотности-темdocsdensitymd)
  - [[Мониторинг зависимостей](docs/DEPENDABOT.md)](#мониторинг-зависимостейdocsdependabotmd)
  - [[Карта зависимостей скриптов](docs/DEPENDENCY_MAP.md)](#карта-зависимостей-скриптовdocsdependency_mapmd)
  - [[Дайджест изменений](docs/DIGEST.md)](#дайджест-измененийdocsdigestmd)
  - [[Автодайджест изменений](docs/DIGEST_AUTO.md)](#автодайджест-измененийdocsdigest_automd)
  - [[Еженедельный дайджест — 2026-04-29](docs/DIGEST_WEEKLY.md)](#еженедельный-дайджест-2026-04-29docsdigest_weeklymd)
  - [[Отчёт о дублировании](docs/DUPLICATES.md)](#отчёт-о-дублированииdocsduplicatesmd)
  - [[Пустые секции](docs/EMPTY_SECTIONS.md)](#пустые-секцииdocsempty_sectionsmd)
  - [[Именованные сущности](docs/ENTITIES.md)](#именованные-сущностиdocsentitiesmd)
  - [[Часто задаваемые вопросы (FAQ)](docs/FAQ.md)](#часто-задаваемые-вопросы-faqdocsfaqmd)
  - [[Сноски и определения терминов](docs/FOOTNOTES.md)](#сноски-и-определения-терминовdocsfootnotesmd)
  - [[Глоссарий проектов](docs/GLOSSARY.md)](#глоссарий-проектовdocsglossarymd)
  - [[Граф связей проектов](docs/GRAPH.md)](#граф-связей-проектовdocsgraphmd)
  - [[Аудит заголовков](docs/HEADING_AUDIT.md)](#аудит-заголовковdocsheading_auditmd)
  - [[Health Dashboard](docs/HEALTH.md)](#health-dashboarddocshealthmd)
  - [[Тепловая карта тем](docs/HEATMAP.md)](#тепловая-карта-темdocsheatmapmd)
  - [[Индекс документации — Lorenzo / Svyazi 2.0](docs/INDEX.md)](#индекс-документации-lorenzo-svyazi-20docsindexmd)
  - [[Инвертированный индекс ключевых слов](docs/KEYWORD_INDEX.md)](#инвертированный-индекс-ключевых-словdocskeyword_indexmd)
  - [[Карта базы знаний Lorenzo](docs/KNOWLEDGE_MAP.md)](#карта-базы-знаний-lorenzodocsknowledge_mapmd)
  - [[Числовые KPI и метрики](docs/KPI.md)](#числовые-kpi-и-метрикиdocskpimd)
  - [[История метрик KPI](docs/KPI_HISTORY.md)](#история-метрик-kpidocskpi_historymd)
  - [[Языковой состав документов](docs/LANGUAGE_STATS.md)](#языковой-состав-документовdocslanguage_statsmd)
  - [[Индекс ссылок](docs/LINKS.md)](#индекс-ссылокdocslinksmd)
  - [[AI-саммари разделов документации](docs/LLM_SUMMARIES.md)](#ai-саммари-разделов-документацииdocsllm_summariesmd)
  - [[Метрики качества документации](docs/METRICS.md)](#метрики-качества-документацииdocsmetricsmd)
  - [[Майндмап репозитория Lorenzo](docs/MINDMAP.md)](#майндмап-репозитория-lorenzodocsmindmapmd)
  - [[Карта пробелов знаний](docs/MISSING.md)](#карта-пробелов-знанийdocsmissingmd)
  - [[Индекс именованных сущностей](docs/NAMED_ENTITIES.md)](#индекс-именованных-сущностейdocsnamed_entitiesmd)
  - [[Нарратив проекта Lorenzo](docs/NARRATIVE.md)](#нарратив-проекта-lorenzodocsnarrativemd)
  - [[Сеть проектов и авторов](docs/NETWORK.md)](#сеть-проектов-и-авторовdocsnetworkmd)
  - [[Онбординг — Svyazi 2.0 / Lorenzo](docs/ONBOARDING.md)](#онбординг-svyazi-20-lorenzodocsonboardingmd)
  - [[Изолированные документы (Orphans)](docs/ORPHANS.md)](#изолированные-документы-orphansdocsorphansmd)
  - [[Качество абзацев](docs/PARAGRAPH_QUALITY.md)](#качество-абзацевdocsparagraph_qualitymd)
  - [[Пассивный залог и канцеляризмы](docs/PASSIVE_VOICE.md)](#пассивный-залог-и-канцеляризмыdocspassive_voicemd)
  - [[Приоритеты файлов](docs/PRIORITIES.md)](#приоритеты-файловdocsprioritiesmd)
  - [[Прогресс MVP](docs/PROGRESS.md)](#прогресс-mvpdocsprogressmd)
  - [[Глобальный Q&A](docs/QA.md)](#глобальный-qadocsqamd)
  - [[Открытые вопросы](docs/QUESTIONS.md)](#открытые-вопросыdocsquestionsmd)
  - [[Список чтения](docs/READING_LIST.md)](#список-чтенияdocsreading_listmd)
  - [[Рекомендуемый порядок чтения](docs/READING_ORDER.md)](#рекомендуемый-порядок-чтенияdocsreading_ordermd)
  - [[docs](docs/README.md)](#docsdocsreadmemd)
  - [[Svyazi 2.0 — Knowledge Base Report](docs/REPORT.md)](#svyazi-20-knowledge-base-reportdocsreportmd)
  - [[Реестр рисков — Svyazi 2.0](docs/RISK_REGISTER.md)](#реестр-рисков-svyazi-20docsrisk_registermd)
  - [[Расписание проекта](docs/SCHEDULE.md)](#расписание-проектаdocsschedulemd)
  - [[Оценка готовности проекта (Go/No-Go)](docs/SCORING.md)](#оценка-готовности-проекта-gono-godocsscoringmd)
  - [[Результаты поиска](docs/SEARCH_RESULTS.md)](#результаты-поискаdocssearch_resultsmd)
  - [[Индекс «Смотрите также»](docs/SEE_ALSO.md)](#индекс-смотрите-такжеdocssee_alsomd)
  - [[Тональный анализ документов](docs/SENTIMENT.md)](#тональный-анализ-документовdocssentimentmd)
  - [[Похожие документы](docs/SIMILAR.md)](#похожие-документыdocssimilarmd)
  - [[Похожие абзацы между документами](docs/SIMILAR_PASSAGES.md)](#похожие-абзацы-между-документамиdocssimilar_passagesmd)
  - [[Карта репозитория Lorenzo](docs/SITEMAP.md)](#карта-репозитория-lorenzodocssitemapmd)
  - [[Карта происхождения текстов](docs/SOURCE_MAP.md)](#карта-происхождения-текстовdocssource_mapmd)
  - [[Детальная статистика репозитория](docs/STATS.md)](#детальная-статистика-репозиторияdocsstatsmd)
  - [[Резюме документов (TextRank)](docs/SUMMARIES.md)](#резюме-документов-textrankdocssummariesmd)
  - [[Все таблицы репозитория](docs/TABLES.md)](#все-таблицы-репозиторияdocstablesmd)
  - [[Индекс тегов](docs/TAGS.md)](#индекс-теговdocstagsmd)
  - [[Tech Radar — Svyazi 2.0](docs/TECH_RADAR.md)](#tech-radar-svyazi-20docstech_radarmd)
  - [[Хронология и временные маркеры](docs/TIMELINE.md)](#хронология-и-временные-маркерыdocstimelinemd)
  - [[Валидация структуры репозитория](docs/VALIDATION.md)](#валидация-структуры-репозиторияdocsvalidationmd)
  - [[Богатство словаря документов](docs/VOCABULARY.md)](#богатство-словаря-документовdocsvocabularymd)
  - [[Word Cloud](docs/WORD_CLOUD.md)](#word-clouddocsword_cloudmd)
  - [[Частотный анализ слов](docs/WORD_FREQ.md)](#частотный-анализ-словdocsword_freqmd)
  - [[Reading paths — рекомендуемые маршруты по монорепозиторию](docs/reading-paths.md)](#reading-paths-рекомендуемые-маршруты-по-монорепозиториюdocsreading-pathsmd)
- [📁 Svyazi (`docs/01-svyazi/`)](#svyazi-docs01-svyazi)
  - [[Продолжение исследования для Svyazi 2.0](docs/01-svyazi/00-intro-part2.md)](#продолжение-исследования-для-svyazi-20docs01-svyazi00-intro-part2md)
  - [[Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md)](#svyazisvyazi-20-исполнительное-резюмеdocs01-svyazi01-executive-summarymd)
  - [[Методика и рамка отбора проектов](docs/01-svyazi/02-methodology.md)](#методика-и-рамка-отбора-проектовdocs01-svyazi02-methodologymd)
  - [[Карта найденных проектов и паттернов](docs/01-svyazi/03-component-catalog.md)](#карта-найденных-проектов-и-паттерновdocs01-svyazi03-component-catalogmd)
  - [[Приоритетные ансамбли](docs/01-svyazi/04-ensembles-overview.md)](#приоритетные-ансамблиdocs01-svyazi04-ensembles-overviewmd)
  - [[Безопасность, приватность и бюджетный роутинг](docs/01-svyazi/06-security-privacy.md)](#безопасность-приватность-и-бюджетный-роутингdocs01-svyazi06-security-privacymd)
  - [[План прототипа и возможные контакты](docs/01-svyazi/07-mvp-planning.md)](#план-прототипа-и-возможные-контактыdocs01-svyazi07-mvp-planningmd)
  - [[Выводы](docs/01-svyazi/08-conclusions.md)](#выводыdocs01-svyazi08-conclusionsmd)
  - [[Архитектурные зазоры, которые важнее новых инструментов](docs/01-svyazi/09-architectural-gaps.md)](#архитектурные-зазоры-которые-важнее-новых-инструментовdocs01-svyazi09-architectural-gapsmd)
  - [[Новые ансамбли следующего шага](docs/01-svyazi/10-second-order-ensembles.md)](#новые-ансамбли-следующего-шагаdocs01-svyazi10-second-order-ensemblesmd)
  - [[Интеграционный контракт, который стоит зафиксировать сразу](docs/01-svyazi/11-integration-contracts.md)](#интеграционный-контракт-который-стоит-зафиксировать-сразуdocs01-svyazi11-integration-contractsmd)
  - [[Дорожная карта прототипа следующей итерации](docs/01-svyazi/12-roadmap.md)](#дорожная-карта-прототипа-следующей-итерацииdocs01-svyazi12-roadmapmd)
  - [[Контактная стратегия и узкие вопросы для авторов](docs/01-svyazi/13-contacts.md)](#контактная-стратегия-и-узкие-вопросы-для-авторовdocs01-svyazi13-contactsmd)
  - [[Ограничения, лицензии и что пока лучше не склеивать](docs/01-svyazi/14-limitations.md)](#ограничения-лицензии-и-что-пока-лучше-не-склеиватьdocs01-svyazi14-limitationsmd)
  - [[Q&A: 01-svyazi](docs/01-svyazi/QA.md)](#qa-01-svyazidocs01-svyaziqamd)
  - [[Svyazi 2.0 — Архитектура и исследование](docs/01-svyazi/README.md)](#svyazi-20-архитектура-и-исследованиеdocs01-svyazireadmemd)
- [📁 Anthropic Vacancies (`docs/02-anthropic-vacancies/`)](#anthropic-vacancies-docs02-anthropic-vacancies)
  - [[Введение](docs/02-anthropic-vacancies/00-intro.md)](#введениеdocs02-anthropic-vacancies00-intromd)
  - [[Интегральный анализ профиля svend4](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)](#интегральный-анализ-профиля-svend4docs02-anthropic-vacancies01-интегральный-анализ-профиля-svend4md)
  - [[ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md)](#общий-план-развития-nautilus-portal-protocoldocs02-anthropic-vacancies02-общий-план-развития-nautilus-portal-protocolmd)
  - [[PORTAL-PROTOCOL.md](docs/02-anthropic-vacancies/03-portal-protocol-md.md)](#portal-protocolmddocs02-anthropic-vacancies03-portal-protocol-mdmd)
  - [[Abstract](docs/02-anthropic-vacancies/04-abstract.md)](#abstractdocs02-anthropic-vacancies04-abstractmd)
  - [[0. Status of This Document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md)](#0-status-of-this-documentdocs02-anthropic-vacancies05-0-status-of-this-documentmd)
  - [[1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md)](#1-introductiondocs02-anthropic-vacancies06-1-introductionmd)
  - [[2. Terminology](docs/02-anthropic-vacancies/07-2-terminology.md)](#2-terminologydocs02-anthropic-vacancies07-2-terminologymd)
  - [[3. Registry (nautilus.json)](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md)](#3-registry-nautilusjsondocs02-anthropic-vacancies08-3-registry-nautilus-jsonmd)
  - [[4. Passport (passport.md)](docs/02-anthropic-vacancies/09-4-passport-passport-md.md)](#4-passport-passportmddocs02-anthropic-vacancies09-4-passport-passport-mdmd)
  - [[Доступ к данным](docs/02-anthropic-vacancies/102-доступ-к-данным.md)](#доступ-к-даннымdocs02-anthropic-vacancies102-доступ-к-даннымmd)
  - [[Appendix B: Change Log](docs/02-anthropic-vacancies/103-appendix-b-change-log.md)](#appendix-b-change-logdocs02-anthropic-vacancies103-appendix-b-change-logmd)
  - [[Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md)](#appendix-c-referencesdocs02-anthropic-vacancies104-appendix-c-referencesmd)
  - [[REVIEWMETHODOLOGY.md](docs/02-anthropic-vacancies/105-review-methodology-md.md)](#reviewmethodologymddocs02-anthropic-vacancies105-review-methodology-mdmd)
  - [[TL;DR](docs/02-anthropic-vacancies/106-tl-dr.md)](#tldrdocs02-anthropic-vacancies106-tl-drmd)
  - [[1. Контекст и мотивация](docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md)](#1-контекст-и-мотивацияdocs02-anthropic-vacancies107-1-контекст-и-мотивацияmd)
  - [[2. Формальный workflow](docs/02-anthropic-vacancies/108-2-формальный-workflow.md)](#2-формальный-workflowdocs02-anthropic-vacancies108-2-формальный-workflowmd)
  - [[3. Принципы консолидации (Фаза C)](docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md)](#3-принципы-консолидации-фаза-cdocs02-anthropic-vacancies109-3-принципы-консолидации-фаза-cmd)
  - [[Вопрос: fallback-ratio как критический или осмысленный?](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md)](#вопрос-fallback-ratio-как-критический-или-осмысленныйdocs02-anthropic-vacancies110-вопрос-fallback-ratio-как-критический-или-осмысленmd)
  - [[4. Условия применимости](docs/02-anthropic-vacancies/111-4-условия-применимости.md)](#4-условия-применимостиdocs02-anthropic-vacancies111-4-условия-применимостиmd)
  - [[5. Связь с существующими методологиями](docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md)](#5-связь-с-существующими-методологиямиdocs02-anthropic-vacancies112-5-связь-с-существующими-методологиямиmd)
  - [[6. Почему это валидный паттерн для AI-assisted workflows](docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md)](#6-почему-это-валидный-паттерн-для-ai-assisted-workflowsdocs02-anthropic-vacancies113-6-почему-это-валидный-паттерн-для-ai-assisted-workmd)
  - [[7. Реализация в проекте Nautilus](docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md)](#7-реализация-в-проекте-nautilusdocs02-anthropic-vacancies114-7-реализация-в-проекте-nautilusmd)
  - [[8. Ограничения и открытые вопросы](docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md)](#8-ограничения-и-открытые-вопросыdocs02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd)
  - [[9. Checklist применения методологии](docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md)](#9-checklist-применения-методологииdocs02-anthropic-vacancies116-9-checklist-применения-методологииmd)
  - [[10. Конкретный план применения к текущим документам](docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md)](#10-конкретный-план-применения-к-текущим-документамdocs02-anthropic-vacancies117-10-конкретный-план-применения-к-текущим-документамmd)
  - [[Appendix A: Шаблон для header warning](docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md)](#appendix-a-шаблон-для-header-warningdocs02-anthropic-vacancies118-appendix-a-шаблон-для-header-warningmd)
  - [[Appendix B: Примеры расхождений и их разрешения](docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md)](#appendix-b-примеры-расхождений-и-их-разрешенияdocs02-anthropic-vacancies119-appendix-b-примеры-расхождений-и-их-разрешенияmd)
  - [[Content Overview](docs/02-anthropic-vacancies/12-content-overview.md)](#content-overviewdocs02-anthropic-vacancies12-content-overviewmd)
  - [[Главные технические риски](docs/02-anthropic-vacancies/120-главные-технические-риски.md)](#главные-технические-рискиdocs02-anthropic-vacancies120-главные-технические-рискиmd)
  - [[Appendix C: История изменений методологии](docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md)](#appendix-c-история-изменений-методологииdocs02-anthropic-vacancies121-appendix-c-история-изменений-методологииmd)
  - [[Глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md)](#глоссарийdocs02-anthropic-vacancies122-глоссарийmd)
  - [[portal-mcp.py](docs/02-anthropic-vacancies/123-portal-mcp-py.md)](#portal-mcppydocs02-anthropic-vacancies123-portal-mcp-pymd)
  - [[Конфигурация для Claude Desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md)](#конфигурация-для-claude-desktopdocs02-anthropic-vacancies124-конфигурация-для-claude-desktopmd)
  - [[README-MCP.md— инструкция по установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md)](#readme-mcpmd-инструкция-по-установкеdocs02-anthropic-vacancies125-readme-mcp-md-инструкция-по-установкеmd)
  - [[Установка](docs/02-anthropic-vacancies/126-установка.md)](#установкаdocs02-anthropic-vacancies126-установкаmd)
  - [[Подключение к Claude Desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md)](#подключение-к-claude-desktopdocs02-anthropic-vacancies127-подключение-к-claude-desktopmd)
  - [[Доступные инструменты](docs/02-anthropic-vacancies/128-доступные-инструменты.md)](#доступные-инструментыdocs02-anthropic-vacancies128-доступные-инструментыmd)
  - [[Примеры запросов (в Claude)](docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md)](#примеры-запросов-в-claudedocs02-anthropic-vacancies129-примеры-запросов-в-claudemd)
  - [[Angle / Perspective](docs/02-anthropic-vacancies/13-angle-perspective.md)](#angle-perspectivedocs02-anthropic-vacancies13-angle-perspectivemd)
  - [[Отладка](docs/02-anthropic-vacancies/130-отладка.md)](#отладкаdocs02-anthropic-vacancies130-отладкаmd)
  - [[Ограничения текущей версии (0.1.0-draft)](docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md)](#ограничения-текущей-версии-010-draftdocs02-anthropic-vacancies131-ограничения-текущей-версии-0-1-0-draftmd)
  - [[Planned (v0.2.0)](docs/02-anthropic-vacancies/132-planned-v0-2-0.md)](#planned-v020docs02-anthropic-vacancies132-planned-v0-2-0md)
  - [[Обратная связь](docs/02-anthropic-vacancies/133-обратная-связь.md)](#обратная-связьdocs02-anthropic-vacancies133-обратная-связьmd)
  - [[THE DOUBLE-TRIANGLE ARCHITECTURE.md](docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md)](#the-double-triangle-architecturemddocs02-anthropic-vacancies134-the-double-triangle-architecture-mdmd)
  - [[A Formal Model for Human-AI Collaboration in Distributed Knowledge Work](docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md)](#a-formal-model-for-human-ai-collaboration-in-distributed-knowledge-workdocs02-anthropic-vacancies135-a-formal-model-for-human-ai-collaboration-in-distrmd)
  - [[Abstract](docs/02-anthropic-vacancies/136-abstract.md)](#abstractdocs02-anthropic-vacancies136-abstractmd)
  - [[Table of Contents](docs/02-anthropic-vacancies/137-table-of-contents.md)](#table-of-contentsdocs02-anthropic-vacancies137-table-of-contentsmd)
  - [[1. Why Single-Triangle Models Are Incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md)](#1-why-single-triangle-models-are-incompletedocs02-anthropic-vacancies138-1-why-single-triangle-models-are-incompletemd)
  - [[2. The Double-Triangle Architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md)](#2-the-double-triangle-architecturedocs02-anthropic-vacancies139-2-the-double-triangle-architecturemd)
  - [[3. Three Inter-Layer Protocols](docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md)](#3-three-inter-layer-protocolsdocs02-anthropic-vacancies140-3-three-inter-layer-protocolsmd)
  - [[4. Nautilus Portal as Reference Substrate](docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md)](#4-nautilus-portal-as-reference-substratedocs02-anthropic-vacancies141-4-nautilus-portal-as-reference-substratemd)
  - [[5. Pattern Library as Bridge Between Triangles](docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md)](#5-pattern-library-as-bridge-between-trianglesdocs02-anthropic-vacancies142-5-pattern-library-as-bridge-between-trianglesmd)
  - [[6. Four Deployment Domains](docs/02-anthropic-vacancies/143-6-four-deployment-domains.md)](#6-four-deployment-domainsdocs02-anthropic-vacancies143-6-four-deployment-domainsmd)
  - [[7. Open Questions](docs/02-anthropic-vacancies/144-7-open-questions.md)](#7-open-questionsdocs02-anthropic-vacancies144-7-open-questionsmd)
  - [[8. Call to Action](docs/02-anthropic-vacancies/145-8-call-to-action.md)](#8-call-to-actiondocs02-anthropic-vacancies145-8-call-to-actionmd)
  - [[Acknowledgments](docs/02-anthropic-vacancies/146-acknowledgments.md)](#acknowledgmentsdocs02-anthropic-vacancies146-acknowledgmentsmd)
  - [[References](docs/02-anthropic-vacancies/147-references.md)](#referencesdocs02-anthropic-vacancies147-referencesmd)
  - [[Appendix A: Glossary](docs/02-anthropic-vacancies/148-appendix-a-glossary.md)](#appendix-a-glossarydocs02-anthropic-vacancies148-appendix-a-glossarymd)
  - [[Appendix B: Summary of Contributions](docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md)](#appendix-b-summary-of-contributionsdocs02-anthropic-vacancies149-appendix-b-summary-of-contributionsmd)
  - [[Appendix C: Version History](docs/02-anthropic-vacancies/150-appendix-c-version-history.md)](#appendix-c-version-historydocs02-anthropic-vacancies150-appendix-c-version-historymd)
  - [[OPEN KNOWLEDGE WORK FOUNDATION.md](docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md)](#open-knowledge-work-foundationmddocs02-anthropic-vacancies151-open-knowledge-work-foundation-mdmd)
  - [[AI-Coordinated Infrastructure for Distributed Expert Contribution](docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md)](#ai-coordinated-infrastructure-for-distributed-expert-contributiondocs02-anthropic-vacancies152-ai-coordinated-infrastructure-for-distributed-expemd)
  - [[Executive Summary](docs/02-anthropic-vacancies/153-executive-summary.md)](#executive-summarydocs02-anthropic-vacancies153-executive-summarymd)
  - [[Table of Contents](docs/02-anthropic-vacancies/154-table-of-contents.md)](#table-of-contentsdocs02-anthropic-vacancies154-table-of-contentsmd)
  - [[1. Problem Statement](docs/02-anthropic-vacancies/155-1-problem-statement.md)](#1-problem-statementdocs02-anthropic-vacancies155-1-problem-statementmd)
  - [[2. Target Populations](docs/02-anthropic-vacancies/156-2-target-populations.md)](#2-target-populationsdocs02-anthropic-vacancies156-2-target-populationsmd)
  - [[3. Why Existing Solutions Fail](docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md)](#3-why-existing-solutions-faildocs02-anthropic-vacancies157-3-why-existing-solutions-failmd)
  - [[4. Proposed Infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md)](#4-proposed-infrastructuredocs02-anthropic-vacancies158-4-proposed-infrastructuremd)
  - [[5. Economic Model](docs/02-anthropic-vacancies/159-5-economic-model.md)](#5-economic-modeldocs02-anthropic-vacancies159-5-economic-modelmd)
  - [[History](docs/02-anthropic-vacancies/16-history.md)](#historydocs02-anthropic-vacancies16-historymd)
  - [[6. Governance and Ethics](docs/02-anthropic-vacancies/160-6-governance-and-ethics.md)](#6-governance-and-ethicsdocs02-anthropic-vacancies160-6-governance-and-ethicsmd)
  - [[7. Phased Rollout Plan](docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md)](#7-phased-rollout-plandocs02-anthropic-vacancies161-7-phased-rollout-planmd)
  - [[8. Risk Analysis](docs/02-anthropic-vacancies/162-8-risk-analysis.md)](#8-risk-analysisdocs02-anthropic-vacancies162-8-risk-analysismd)
  - [[9. Call for Partnership](docs/02-anthropic-vacancies/163-9-call-for-partnership.md)](#9-call-for-partnershipdocs02-anthropic-vacancies163-9-call-for-partnershipmd)
  - [[10. Appendices](docs/02-anthropic-vacancies/164-10-appendices.md)](#10-appendicesdocs02-anthropic-vacancies164-10-appendicesmd)
  - [[Closing](docs/02-anthropic-vacancies/165-closing.md)](#closingdocs02-anthropic-vacancies165-closingmd)
  - [[REPRESENTATIVE AGENT LAYER.md](docs/02-anthropic-vacancies/166-representative-agent-layer-md.md)](#representative-agent-layermddocs02-anthropic-vacancies166-representative-agent-layer-mdmd)
  - [[AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations](docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md)](#ai-mediated-representation-for-underrepresented-experts-and-vulnerable-populationsdocs02-anthropic-vacancies167-ai-mediated-representation-for-underrepresented-exmd)
  - [[Abstract](docs/02-anthropic-vacancies/168-abstract.md)](#abstractdocs02-anthropic-vacancies168-abstractmd)
  - [[Table of Contents](docs/02-anthropic-vacancies/169-table-of-contents.md)](#table-of-contentsdocs02-anthropic-vacancies169-table-of-contentsmd)
  - [[5. Compatibility Levels](docs/02-anthropic-vacancies/17-5-compatibility-levels.md)](#5-compatibility-levelsdocs02-anthropic-vacancies17-5-compatibility-levelsmd)
  - [[1. The Cinderella Syndrome: Why Quality Stays Invisible](docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md)](#1-the-cinderella-syndrome-why-quality-stays-invisibledocs02-anthropic-vacancies170-1-the-cinderella-syndrome-why-quality-stays-invisimd)
  - [[2. Historical Precedents: Agents as Civilizational Innovation](docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md)](#2-historical-precedents-agents-as-civilizational-innovationdocs02-anthropic-vacancies171-2-historical-precedents-agents-as-civilizational-imd)
  - [[3. What Makes a Representative Agent](docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md)](#3-what-makes-a-representative-agentdocs02-anthropic-vacancies172-3-what-makes-a-representative-agentmd)
  - [[4. Ten Domains of Application](docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md)](#4-ten-domains-of-applicationdocs02-anthropic-vacancies173-4-ten-domains-of-applicationmd)
  - [[5. Architectural Specification](docs/02-anthropic-vacancies/174-5-architectural-specification.md)](#5-architectural-specificationdocs02-anthropic-vacancies174-5-architectural-specificationmd)
  - [[6. Ethical Framework](docs/02-anthropic-vacancies/175-6-ethical-framework.md)](#6-ethical-frameworkdocs02-anthropic-vacancies175-6-ethical-frameworkmd)
  - [[7. Governance and Oversight](docs/02-anthropic-vacancies/176-7-governance-and-oversight.md)](#7-governance-and-oversightdocs02-anthropic-vacancies176-7-governance-and-oversightmd)
  - [[8. Risks and Mitigations](docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md)](#8-risks-and-mitigationsdocs02-anthropic-vacancies177-8-risks-and-mitigationsmd)
  - [[9. Phased Rollout Strategy](docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md)](#9-phased-rollout-strategydocs02-anthropic-vacancies178-9-phased-rollout-strategymd)
  - [[10. Open Questions](docs/02-anthropic-vacancies/179-10-open-questions.md)](#10-open-questionsdocs02-anthropic-vacancies179-10-open-questionsmd)
  - [[6. Adapter Interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md)](#6-adapter-interfacedocs02-anthropic-vacancies18-6-adapter-interfacemd)
  - [[11. Call for Collaboration](docs/02-anthropic-vacancies/180-11-call-for-collaboration.md)](#11-call-for-collaborationdocs02-anthropic-vacancies180-11-call-for-collaborationmd)
  - [[12. Closing](docs/02-anthropic-vacancies/181-12-closing.md)](#12-closingdocs02-anthropic-vacancies181-12-closingmd)
  - [[Acknowledgments](docs/02-anthropic-vacancies/182-acknowledgments.md)](#acknowledgmentsdocs02-anthropic-vacancies182-acknowledgmentsmd)
  - [[References](docs/02-anthropic-vacancies/183-references.md)](#referencesdocs02-anthropic-vacancies183-referencesmd)
  - [[Appendix A: Connection to Companion Papers](docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md)](#appendix-a-connection-to-companion-papersdocs02-anthropic-vacancies184-appendix-a-connection-to-companion-papersmd)
  - [[Appendix B: Domain Comparison Matrix](docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md)](#appendix-b-domain-comparison-matrixdocs02-anthropic-vacancies185-appendix-b-domain-comparison-matrixmd)
  - [[Appendix C: Sample Use Cases in Detail](docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md)](#appendix-c-sample-use-cases-in-detaildocs02-anthropic-vacancies186-appendix-c-sample-use-cases-in-detailmd)
  - [[СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md](docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md)](#слой-представительских-агентовmddocs02-anthropic-vacancies187-слой-представительских-агентов-mdmd)
  - [[AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения](docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md)](#ai-опосредованное-представительство-для-недопредставленных-экспертов-и-уязвимых-категорий-населенияdocs02-anthropic-vacancies188-ai-опосредованное-представительство-для-недопредстmd)
  - [[Аннотация](docs/02-anthropic-vacancies/189-аннотация.md)](#аннотацияdocs02-anthropic-vacancies189-аннотацияmd)
  - [[7. PortalEntry Structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md)](#7-portalentry-structuredocs02-anthropic-vacancies19-7-portalentry-structuremd)
  - [[Содержание](docs/02-anthropic-vacancies/190-содержание.md)](#содержаниеdocs02-anthropic-vacancies190-содержаниеmd)
  - [[1. Синдром Золушки: Почему качество остаётся невидимым](docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md)](#1-синдром-золушки-почему-качество-остаётся-невидимымdocs02-anthropic-vacancies191-1-синдром-золушки-почему-качество-остаётся-невидимmd)
  - [[2. Исторические прецеденты: Агенты как цивилизационная инновация](docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md)](#2-исторические-прецеденты-агенты-как-цивилизационная-инновацияdocs02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd)
  - [[3. Что делает агента Представительским](docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md)](#3-что-делает-агента-представительскимdocs02-anthropic-vacancies193-3-что-делает-агента-представительскимmd)
  - [[4. Десять областей применения](docs/02-anthropic-vacancies/194-4-десять-областей-применения.md)](#4-десять-областей-примененияdocs02-anthropic-vacancies194-4-десять-областей-примененияmd)
  - [[5. Архитектурная спецификация](docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md)](#5-архитектурная-спецификацияdocs02-anthropic-vacancies195-5-архитектурная-спецификацияmd)
  - [[6. Этическая рамка](docs/02-anthropic-vacancies/196-6-этическая-рамка.md)](#6-этическая-рамкаdocs02-anthropic-vacancies196-6-этическая-рамкаmd)
  - [[7. Управление и надзор](docs/02-anthropic-vacancies/197-7-управление-и-надзор.md)](#7-управление-и-надзорdocs02-anthropic-vacancies197-7-управление-и-надзорmd)
  - [[8. Риски и меры противодействия](docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md)](#8-риски-и-меры-противодействияdocs02-anthropic-vacancies198-8-риски-и-меры-противодействияmd)
  - [[9. Стратегия поэтапного развёртывания](docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md)](#9-стратегия-поэтапного-развёртыванияdocs02-anthropic-vacancies199-9-стратегия-поэтапного-развёртыванияmd)
  - [[8. Consensus Algorithm](docs/02-anthropic-vacancies/20-8-consensus-algorithm.md)](#8-consensus-algorithmdocs02-anthropic-vacancies20-8-consensus-algorithmmd)
  - [[10. Открытые вопросы](docs/02-anthropic-vacancies/200-10-открытые-вопросы.md)](#10-открытые-вопросыdocs02-anthropic-vacancies200-10-открытые-вопросыmd)
  - [[11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md)](#11-призыв-к-сотрудничествуdocs02-anthropic-vacancies201-11-призыв-к-сотрудничествуmd)
  - [[12. Заключение](docs/02-anthropic-vacancies/202-12-заключение.md)](#12-заключениеdocs02-anthropic-vacancies202-12-заключениеmd)
  - [[Благодарности](docs/02-anthropic-vacancies/203-благодарности.md)](#благодарностиdocs02-anthropic-vacancies203-благодарностиmd)
  - [[Ссылки](docs/02-anthropic-vacancies/204-ссылки.md)](#ссылкиdocs02-anthropic-vacancies204-ссылкиmd)
  - [[Приложение A: Связь с Сопроводительными Статьями](docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md)](#приложение-a-связь-с-сопроводительными-статьямиdocs02-anthropic-vacancies205-приложение-a-связь-с-сопроводительными-статьямиmd)
  - [[Приложение B: Матрица Сравнения Областей](docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md)](#приложение-b-матрица-сравнения-областейdocs02-anthropic-vacancies206-приложение-b-матрица-сравнения-областейmd)
  - [[Приложение C: Образцы Случаев Использования в Деталях](docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md)](#приложение-c-образцы-случаев-использования-в-деталяхdocs02-anthropic-vacancies207-приложение-c-образцы-случаев-использования-в-деталmd)
  - [[PROFESSIONAL COLLEAGUE AGENTS.md](docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md)](#professional-colleague-agentsmddocs02-anthropic-vacancies208-professional-colleague-agents-mdmd)
  - [[A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers](docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md)](#a-typology-of-ai-agents-on-the-principal-side-and-the-case-for-profession-specific-co-workersdocs02-anthropic-vacancies209-a-typology-of-ai-agents-on-the-principal-side-and-md)
  - [[9. Query Flow](docs/02-anthropic-vacancies/21-9-query-flow.md)](#9-query-flowdocs02-anthropic-vacancies21-9-query-flowmd)
  - [[Abstract](docs/02-anthropic-vacancies/210-abstract.md)](#abstractdocs02-anthropic-vacancies210-abstractmd)
  - [[Table of Contents](docs/02-anthropic-vacancies/211-table-of-contents.md)](#table-of-contentsdocs02-anthropic-vacancies211-table-of-contentsmd)
  - [[1. The Five-Type Typology of Principal-Side Agents](docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md)](#1-the-five-type-typology-of-principal-side-agentsdocs02-anthropic-vacancies212-1-the-five-type-typology-of-principal-side-agentsmd)
  - [[2. What Makes a Professional Colleague Agent](docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md)](#2-what-makes-a-professional-colleague-agentdocs02-anthropic-vacancies213-2-what-makes-a-professional-colleague-agentmd)
  - [[3. Empirical Case Study: «Обучай»](docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md)](#3-empirical-case-study-обучайdocs02-anthropic-vacancies214-3-empirical-case-study-обучайmd)
  - [[4. Architecture of Professional Colleague Agents](docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md)](#4-architecture-of-professional-colleague-agentsdocs02-anthropic-vacancies215-4-architecture-of-professional-colleague-agentsmd)
  - [[5. The Economics of Profession-Wide Replication](docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md)](#5-the-economics-of-profession-wide-replicationdocs02-anthropic-vacancies216-5-the-economics-of-profession-wide-replicationmd)
  - [[6. Risks Specific to this Category](docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md)](#6-risks-specific-to-this-categorydocs02-anthropic-vacancies217-6-risks-specific-to-this-categorymd)
  - [[7. Application Domains](docs/02-anthropic-vacancies/218-7-application-domains.md)](#7-application-domainsdocs02-anthropic-vacancies218-7-application-domainsmd)
  - [[8. Pilot Proposal: SGB Advocate Colleague](docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md)](#8-pilot-proposal-sgb-advocate-colleaguedocs02-anthropic-vacancies219-8-pilot-proposal-sgb-advocate-colleaguemd)
  - [[10. QueryResult Structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md)](#10-queryresult-structuredocs02-anthropic-vacancies22-10-queryresult-structuremd)
  - [[9. Relationship to Other Agent Types](docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md)](#9-relationship-to-other-agent-typesdocs02-anthropic-vacancies220-9-relationship-to-other-agent-typesmd)
  - [[10. Open Questions](docs/02-anthropic-vacancies/221-10-open-questions.md)](#10-open-questionsdocs02-anthropic-vacancies221-10-open-questionsmd)
  - [[11. Call for Collaboration](docs/02-anthropic-vacancies/222-11-call-for-collaboration.md)](#11-call-for-collaborationdocs02-anthropic-vacancies222-11-call-for-collaborationmd)
  - [[12. Closing](docs/02-anthropic-vacancies/223-12-closing.md)](#12-closingdocs02-anthropic-vacancies223-12-closingmd)
  - [[Acknowledgments](docs/02-anthropic-vacancies/224-acknowledgments.md)](#acknowledgmentsdocs02-anthropic-vacancies224-acknowledgmentsmd)
  - [[References](docs/02-anthropic-vacancies/225-references.md)](#referencesdocs02-anthropic-vacancies225-referencesmd)
  - [[Appendix A: Comparative Table — Five Agent Types](docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md)](#appendix-a-comparative-table-five-agent-typesdocs02-anthropic-vacancies226-appendix-a-comparative-table-five-agent-typesmd)
  - [[Appendix B: Decision Framework — When to Build Type 1 First](docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md)](#appendix-b-decision-framework-when-to-build-type-1-firstdocs02-anthropic-vacancies227-appendix-b-decision-framework-when-to-build-type-1md)
  - [[Appendix C: Quick-Start Architecture for SGB Advocate Colleague](docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md)](#appendix-c-quick-start-architecture-for-sgb-advocate-colleaguedocs02-anthropic-vacancies228-appendix-c-quick-start-architecture-for-sgb-advocamd)
  - [[ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ](docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md)](#профессиональные-коллеги-агентыdocs02-anthropic-vacancies229-профессиональные-коллеги-агентыmd)
  - [[11. Security Considerations](docs/02-anthropic-vacancies/23-11-security-considerations.md)](#11-security-considerationsdocs02-anthropic-vacancies23-11-security-considerationsmd)
  - [[Аннотация](docs/02-anthropic-vacancies/230-аннотация.md)](#аннотацияdocs02-anthropic-vacancies230-аннотацияmd)
  - [[Содержание](docs/02-anthropic-vacancies/231-содержание.md)](#содержаниеdocs02-anthropic-vacancies231-содержаниеmd)
  - [[1. Типология из пяти типов агентов на стороне принципала](docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md)](#1-типология-из-пяти-типов-агентов-на-стороне-принципалаdocs02-anthropic-vacancies232-1-типология-из-пяти-типов-агентов-на-стороне-принцmd)
  - [[2. Что делает агента Профессиональным Коллегой](docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md)](#2-что-делает-агента-профессиональным-коллегойdocs02-anthropic-vacancies233-2-что-делает-агента-профессиональным-коллегойmd)
  - [[3. Эмпирический кейс: «Обучай»](docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md)](#3-эмпирический-кейс-обучайdocs02-anthropic-vacancies234-3-эмпирический-кейс-обучайmd)
  - [[4. Архитектура Профессиональных Коллег-Агентов](docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md)](#4-архитектура-профессиональных-коллег-агентовdocs02-anthropic-vacancies235-4-архитектура-профессиональных-коллег-агентовmd)
  - [[5. Экономика тиражирования по профессии](docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md)](#5-экономика-тиражирования-по-профессииdocs02-anthropic-vacancies236-5-экономика-тиражирования-по-профессииmd)
  - [[6. Риски, специфичные для этой категории](docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md)](#6-риски-специфичные-для-этой-категорииdocs02-anthropic-vacancies237-6-риски-специфичные-для-этой-категорииmd)
  - [[7. Области применения](docs/02-anthropic-vacancies/238-7-области-применения.md)](#7-области-примененияdocs02-anthropic-vacancies238-7-области-примененияmd)
  - [[8. Пилотное предложение: SGB Колega-Адвокат](docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md)](#8-пилотное-предложение-sgb-колega-адвокатdocs02-anthropic-vacancies239-8-пилотное-предложение-sgb-колega-адвокатmd)
  - [[12. Versioning Policy](docs/02-anthropic-vacancies/24-12-versioning-policy.md)](#12-versioning-policydocs02-anthropic-vacancies24-12-versioning-policymd)
  - [[9. Связь с другими типами агентов](docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md)](#9-связь-с-другими-типами-агентовdocs02-anthropic-vacancies240-9-связь-с-другими-типами-агентовmd)
  - [[10. Открытые вопросы](docs/02-anthropic-vacancies/241-10-открытые-вопросы.md)](#10-открытые-вопросыdocs02-anthropic-vacancies241-10-открытые-вопросыmd)
  - [[11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md)](#11-призыв-к-сотрудничествуdocs02-anthropic-vacancies242-11-призыв-к-сотрудничествуmd)
  - [[12. Заключение](docs/02-anthropic-vacancies/243-12-заключение.md)](#12-заключениеdocs02-anthropic-vacancies243-12-заключениеmd)
  - [[Благодарности](docs/02-anthropic-vacancies/244-благодарности.md)](#благодарностиdocs02-anthropic-vacancies244-благодарностиmd)
  - [[Ссылки](docs/02-anthropic-vacancies/245-ссылки.md)](#ссылкиdocs02-anthropic-vacancies245-ссылкиmd)
  - [[Приложение A: Сравнительная Таблица — Пять Типов Агентов](docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md)](#приложение-a-сравнительная-таблица-пять-типов-агентовdocs02-anthropic-vacancies246-приложение-a-сравнительная-таблица-пять-типов-агенmd)
  - [[Приложение B: Рамка принятия решений — когда строить Тип 1 первым](docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md)](#приложение-b-рамка-принятия-решений-когда-строить-тип-1-первымdocs02-anthropic-vacancies247-приложение-b-рамка-принятия-решений-когда-строить-md)
  - [[Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги](docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md)](#приложение-c-архитектура-быстрого-старта-для-sgb-адвоката-коллегиdocs02-anthropic-vacancies248-приложение-c-архитектура-быстрого-старта-для-sgb-аmd)
  - [[COMPOSITE SKILLS AGENT.md](docs/02-anthropic-vacancies/249-composite-skills-agent-md.md)](#composite-skills-agentmddocs02-anthropic-vacancies249-composite-skills-agent-mdmd)
  - [[13. Reference Implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md)](#13-reference-implementationdocs02-anthropic-vacancies25-13-reference-implementationmd)
  - [[Bridging the Gap Between Profession-Wide and Individual-Unique](docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md)](#bridging-the-gap-between-profession-wide-and-individual-uniquedocs02-anthropic-vacancies250-bridging-the-gap-between-profession-wide-and-indivmd)
  - [[AI Support Through Configurable Specialist Ensembles](docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md)](#ai-support-through-configurable-specialist-ensemblesdocs02-anthropic-vacancies251-ai-support-through-configurable-specialist-ensemblmd)
  - [[Abstract](docs/02-anthropic-vacancies/252-abstract.md)](#abstractdocs02-anthropic-vacancies252-abstractmd)
  - [[Table of Contents](docs/02-anthropic-vacancies/253-table-of-contents.md)](#table-of-contentsdocs02-anthropic-vacancies253-table-of-contentsmd)
  - [[1. Why the Binary View Is Incomplete](docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md)](#1-why-the-binary-view-is-incompletedocs02-anthropic-vacancies254-1-why-the-binary-view-is-incompletemd)
  - [[2. The Twenty-One Teachers Pattern](docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md)](#2-the-twenty-one-teachers-patterndocs02-anthropic-vacancies255-2-the-twenty-one-teachers-patternmd)
  - [[3. What Makes a Composite Skills Agent](docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md)](#3-what-makes-a-composite-skills-agentdocs02-anthropic-vacancies256-3-what-makes-a-composite-skills-agentmd)
  - [[4. The Sub-Agent Registry](docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md)](#4-the-sub-agent-registrydocs02-anthropic-vacancies257-4-the-sub-agent-registrymd)
  - [[5. Configuration: How Principals Build Their Ensembles](docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md)](#5-configuration-how-principals-build-their-ensemblesdocs02-anthropic-vacancies258-5-configuration-how-principals-build-their-ensemblmd)
  - [[6. Coordination and Disagreement Resolution](docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md)](#6-coordination-and-disagreement-resolutiondocs02-anthropic-vacancies259-6-coordination-and-disagreement-resolutionmd)
  - [[14. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md)](#14-adr-001-federation-over-mergingdocs02-anthropic-vacancies26-14-adr-001-federation-over-mergingmd)
  - [[7. Economics of Combinatorial Replication](docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md)](#7-economics-of-combinatorial-replicationdocs02-anthropic-vacancies260-7-economics-of-combinatorial-replicationmd)
  - [[8. Seven Domains of Application](docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md)](#8-seven-domains-of-applicationdocs02-anthropic-vacancies261-8-seven-domains-of-applicationmd)
  - [[9. Integration with OKWF Infrastructure](docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md)](#9-integration-with-okwf-infrastructuredocs02-anthropic-vacancies262-9-integration-with-okwf-infrastructuremd)
  - [[10. Risks Specific to Composite Architectures](docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md)](#10-risks-specific-to-composite-architecturesdocs02-anthropic-vacancies263-10-risks-specific-to-composite-architecturesmd)
  - [[11. Open Questions](docs/02-anthropic-vacancies/264-11-open-questions.md)](#11-open-questionsdocs02-anthropic-vacancies264-11-open-questionsmd)
  - [[12. Call for Collaboration](docs/02-anthropic-vacancies/265-12-call-for-collaboration.md)](#12-call-for-collaborationdocs02-anthropic-vacancies265-12-call-for-collaborationmd)
  - [[13. Closing](docs/02-anthropic-vacancies/266-13-closing.md)](#13-closingdocs02-anthropic-vacancies266-13-closingmd)
  - [[Acknowledgments](docs/02-anthropic-vacancies/267-acknowledgments.md)](#acknowledgmentsdocs02-anthropic-vacancies267-acknowledgmentsmd)
  - [[References](docs/02-anthropic-vacancies/268-references.md)](#referencesdocs02-anthropic-vacancies268-referencesmd)
  - [[Appendix A: The Six-Type Taxonomy (Updated)](docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md)](#appendix-a-the-six-type-taxonomy-updateddocs02-anthropic-vacancies269-appendix-a-the-six-type-taxonomy-updatedmd)
  - [[15. Glossary of Examples](docs/02-anthropic-vacancies/27-15-glossary-of-examples.md)](#15-glossary-of-examplesdocs02-anthropic-vacancies27-15-glossary-of-examplesmd)
  - [[Appendix B: Sub-Agent Registry Schema (Sketch)](docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md)](#appendix-b-sub-agent-registry-schema-sketchdocs02-anthropic-vacancies270-appendix-b-sub-agent-registry-schema-sketchmd)
  - [[Appendix C: Configuration Template Example](docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md)](#appendix-c-configuration-template-exampledocs02-anthropic-vacancies271-appendix-c-configuration-template-examplemd)
  - [[Appendix D: Connection Diagram](docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md)](#appendix-d-connection-diagramdocs02-anthropic-vacancies272-appendix-d-connection-diagrammd)
  - [[INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md](docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md)](#infrastructure-for-ai-collaborative-intellectual-workmddocs02-anthropic-vacancies273-infrastructure-for-ai-collaborative-intellectual-wmd)
  - [[The Missing Middle Layer Between Chat and Code](docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md)](#the-missing-middle-layer-between-chat-and-codedocs02-anthropic-vacancies274-the-missing-middle-layer-between-chat-and-codemd)
  - [[Why This Document Exists](docs/02-anthropic-vacancies/275-why-this-document-exists.md)](#why-this-document-existsdocs02-anthropic-vacancies275-why-this-document-existsmd)
  - [[The Two-Layer Stack As It Exists](docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md)](#the-two-layer-stack-as-it-existsdocs02-anthropic-vacancies276-the-two-layer-stack-as-it-existsmd)
  - [[What's Missing — Layer B](docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md)](#whats-missing-layer-bdocs02-anthropic-vacancies277-what-s-missing-layer-bmd)
  - [[Why This Hasn't Been Built](docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md)](#why-this-hasnt-been-builtdocs02-anthropic-vacancies278-why-this-hasn-t-been-builtmd)
  - [[Existing Approximations](docs/02-anthropic-vacancies/279-existing-approximations.md)](#existing-approximationsdocs02-anthropic-vacancies279-existing-approximationsmd)
  - [[Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md)](#appendix-a-minimal-working-exampledocs02-anthropic-vacancies28-appendix-a-minimal-working-examplemd)
  - [[The Specific Case in Front of Us](docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md)](#the-specific-case-in-front-of-usdocs02-anthropic-vacancies280-the-specific-case-in-front-of-usmd)
  - [[The Recursive Insight](docs/02-anthropic-vacancies/281-the-recursive-insight.md)](#the-recursive-insightdocs02-anthropic-vacancies281-the-recursive-insightmd)
  - [[What Industry Will Likely Build](docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md)](#what-industry-will-likely-builddocs02-anthropic-vacancies282-what-industry-will-likely-buildmd)
  - [[What This Document Doesn't Solve](docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md)](#what-this-document-doesnt-solvedocs02-anthropic-vacancies283-what-this-document-doesn-t-solvemd)
  - [[Practical Recommendations for the Current Project](docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md)](#practical-recommendations-for-the-current-projectdocs02-anthropic-vacancies284-practical-recommendations-for-the-current-projectmd)
  - [[Closing](docs/02-anthropic-vacancies/285-closing.md)](#closingdocs02-anthropic-vacancies285-closingmd)
  - [[Acknowledgments](docs/02-anthropic-vacancies/286-acknowledgments.md)](#acknowledgmentsdocs02-anthropic-vacancies286-acknowledgmentsmd)
  - [[References](docs/02-anthropic-vacancies/287-references.md)](#referencesdocs02-anthropic-vacancies287-referencesmd)
  - [[Appendix: Position in Series Visualization](docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md)](#appendix-position-in-series-visualizationdocs02-anthropic-vacancies288-appendix-position-in-series-visualizationmd)
  - [[ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ](docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md)](#инфраструктура-для-ai-совместной-интеллектуальной-работыdocs02-anthropic-vacancies289-инфраструктура-для-ai-совместной-интеллектуальной-md)
  - [[Почему этот документ существует](docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md)](#почему-этот-документ-существуетdocs02-anthropic-vacancies290-почему-этот-документ-существуетmd)
  - [[Двухслойный стек, как он существует](docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md)](#двухслойный-стек-как-он-существуетdocs02-anthropic-vacancies291-двухслойный-стек-как-он-существуетmd)
  - [[Что отсутствует — Слой B](docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md)](#что-отсутствует-слой-bdocs02-anthropic-vacancies292-что-отсутствует-слой-bmd)
  - [[Почему это не было построено](docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md)](#почему-это-не-было-построеноdocs02-anthropic-vacancies293-почему-это-не-было-построеноmd)
  - [[Существующие приближения](docs/02-anthropic-vacancies/294-существующие-приближения.md)](#существующие-приближенияdocs02-anthropic-vacancies294-существующие-приближенияmd)
  - [[Конкретный случай перед нами](docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md)](#конкретный-случай-перед-намиdocs02-anthropic-vacancies295-конкретный-случай-перед-намиmd)
  - [[Рекурсивное прозрение](docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md)](#рекурсивное-прозрениеdocs02-anthropic-vacancies296-рекурсивное-прозрениеmd)
  - [[Что промышленность вероятно построит](docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md)](#что-промышленность-вероятно-построитdocs02-anthropic-vacancies297-что-промышленность-вероятно-построитmd)
  - [[Что этот документ не решает](docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md)](#что-этот-документ-не-решаетdocs02-anthropic-vacancies298-что-этот-документ-не-решаетmd)
  - [[Практические рекомендации для текущего проекта](docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md)](#практические-рекомендации-для-текущего-проектаdocs02-anthropic-vacancies299-практические-рекомендации-для-текущего-проектаmd)
  - [[Заключение](docs/02-anthropic-vacancies/300-заключение.md)](#заключениеdocs02-anthropic-vacancies300-заключениеmd)
  - [[Благодарности](docs/02-anthropic-vacancies/301-благодарности.md)](#благодарностиdocs02-anthropic-vacancies301-благодарностиmd)
  - [[Ссылки](docs/02-anthropic-vacancies/302-ссылки.md)](#ссылкиdocs02-anthropic-vacancies302-ссылкиmd)
  - [[Приложение: Визуализация позиции в серии](docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md)](#приложение-визуализация-позиции-в-серииdocs02-anthropic-vacancies303-приложение-визуализация-позиции-в-серииmd)
  - [[INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md)](#ingit-as-cowork-native-workspace-substratemddocs02-anthropic-vacancies304-ingit-as-cowork-native-workspace-substrate-mdmd)
  - [[A Practical Path to Layer B Through Symbiotic Integration](docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md)](#a-practical-path-to-layer-b-through-symbiotic-integrationdocs02-anthropic-vacancies305-a-practical-path-to-layer-b-through-symbiotic-intemd)
  - [[with Anthropic's Cowork Platform](docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md)](#with-anthropics-cowork-platformdocs02-anthropic-vacancies306-with-anthropic-s-cowork-platformmd)
  - [[Abstract](docs/02-anthropic-vacancies/307-abstract.md)](#abstractdocs02-anthropic-vacancies307-abstractmd)
  - [[Table of Contents](docs/02-anthropic-vacancies/308-table-of-contents.md)](#table-of-contentsdocs02-anthropic-vacancies308-table-of-contentsmd)
  - [[1. The Cowork Discovery and Why It Changes Everything](docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md)](#1-the-cowork-discovery-and-why-it-changes-everythingdocs02-anthropic-vacancies309-1-the-cowork-discovery-and-why-it-changes-everythimd)
  - [[Content Overview](docs/02-anthropic-vacancies/31-content-overview.md)](#content-overviewdocs02-anthropic-vacancies31-content-overviewmd)
  - [[2. What Cowork Provides That InGit Doesn't Need to Build](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md)](#2-what-cowork-provides-that-ingit-doesnt-need-to-builddocs02-anthropic-vacancies310-2-what-cowork-provides-that-ingit-doesn-t-need-to-md)
  - [[3. What InGit Provides That Cowork Lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md)](#3-what-ingit-provides-that-cowork-lacksdocs02-anthropic-vacancies311-3-what-ingit-provides-that-cowork-lacksmd)
  - [[4. The Symbiotic Architecture](docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md)](#4-the-symbiotic-architecturedocs02-anthropic-vacancies312-4-the-symbiotic-architecturemd)
  - [[5. Four Integration Paths in Order of Accessibility](docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md)](#5-four-integration-paths-in-order-of-accessibilitydocs02-anthropic-vacancies313-5-four-integration-paths-in-order-of-accessibilitymd)
  - [[6. Refined InGit Scope with Cowork in Mind](docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md)](#6-refined-ingit-scope-with-cowork-in-minddocs02-anthropic-vacancies314-6-refined-ingit-scope-with-cowork-in-mindmd)
  - [[7. Practical First Steps This Month](docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md)](#7-practical-first-steps-this-monthdocs02-anthropic-vacancies315-7-practical-first-steps-this-monthmd)
  - [[8. Implications for Nautilus and OKWF](docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md)](#8-implications-for-nautilus-and-okwfdocs02-anthropic-vacancies316-8-implications-for-nautilus-and-okwfmd)
  - [[9. Risks and Open Questions](docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md)](#9-risks-and-open-questionsdocs02-anthropic-vacancies317-9-risks-and-open-questionsmd)
  - [[10. Strategic Positioning](docs/02-anthropic-vacancies/318-10-strategic-positioning.md)](#10-strategic-positioningdocs02-anthropic-vacancies318-10-strategic-positioningmd)
  - [[Acknowledgments](docs/02-anthropic-vacancies/319-acknowledgments.md)](#acknowledgmentsdocs02-anthropic-vacancies319-acknowledgmentsmd)
  - [[References](docs/02-anthropic-vacancies/320-references.md)](#referencesdocs02-anthropic-vacancies320-referencesmd)
  - [[Appendix A: Decision Tree for InGit Adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)](#appendix-a-decision-tree-for-ingit-adoptersdocs02-anthropic-vacancies321-appendix-a-decision-tree-for-ingit-adoptersmd)
  - [[Appendix B: Comparison Matrix](docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md)](#appendix-b-comparison-matrixdocs02-anthropic-vacancies322-appendix-b-comparison-matrixmd)
  - [[Appendix C: Sample InGit MCP Server Tool Specifications](docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md)](#appendix-c-sample-ingit-mcp-server-tool-specificationsdocs02-anthropic-vacancies323-appendix-c-sample-ingit-mcp-server-tool-specificatmd)
  - [[INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА](docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md)](#ingit-как-cowork-интегрированная-подложка-рабочего-пространстваdocs02-anthropic-vacancies324-ingit-как-cowork-интегрированная-подложка-рабочегоmd)
  - [[Аннотация](docs/02-anthropic-vacancies/325-аннотация.md)](#аннотацияdocs02-anthropic-vacancies325-аннотацияmd)
  - [[Содержание](docs/02-anthropic-vacancies/326-содержание.md)](#содержаниеdocs02-anthropic-vacancies326-содержаниеmd)
  - [[1. Открытие Cowork и почему это меняет всё](docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md)](#1-открытие-cowork-и-почему-это-меняет-всёdocs02-anthropic-vacancies327-1-открытие-cowork-и-почему-это-меняет-всёmd)
  - [[2. Что Cowork обеспечивает, что InGit не нужно строить](docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md)](#2-что-cowork-обеспечивает-что-ingit-не-нужно-строитьdocs02-anthropic-vacancies328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строиmd)
  - [[3. Что InGit обеспечивает, чего Cowork не хватает](docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md)](#3-что-ingit-обеспечивает-чего-cowork-не-хватаетdocs02-anthropic-vacancies329-3-что-ingit-обеспечивает-чего-cowork-не-хватаетmd)
  - [[4. Симбиотическая Архитектура](docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md)](#4-симбиотическая-архитектураdocs02-anthropic-vacancies330-4-симбиотическая-архитектураmd)
  - [[5. Четыре пути интеграции в порядке доступности](docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md)](#5-четыре-пути-интеграции-в-порядке-доступностиdocs02-anthropic-vacancies331-5-четыре-пути-интеграции-в-порядке-доступностиmd)
  - [[6. Уточнённый объём InGit с учётом Cowork](docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md)](#6-уточнённый-объём-ingit-с-учётом-coworkdocs02-anthropic-vacancies332-6-уточнённый-объём-ingit-с-учётом-coworkmd)
  - [[7. Практические первые шаги в этом месяце](docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md)](#7-практические-первые-шаги-в-этом-месяцеdocs02-anthropic-vacancies333-7-практические-первые-шаги-в-этом-месяцеmd)
  - [[8. Импликации для Nautilus и OKWF](docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md)](#8-импликации-для-nautilus-и-okwfdocs02-anthropic-vacancies334-8-импликации-для-nautilus-и-okwfmd)
  - [[9. Риски и Открытые Вопросы](docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md)](#9-риски-и-открытые-вопросыdocs02-anthropic-vacancies335-9-риски-и-открытые-вопросыmd)
  - [[10. Стратегическое Позиционирование](docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md)](#10-стратегическое-позиционированиеdocs02-anthropic-vacancies336-10-стратегическое-позиционированиеmd)
  - [[Благодарности](docs/02-anthropic-vacancies/337-благодарности.md)](#благодарностиdocs02-anthropic-vacancies337-благодарностиmd)
  - [[Ссылки](docs/02-anthropic-vacancies/338-ссылки.md)](#ссылкиdocs02-anthropic-vacancies338-ссылкиmd)
  - [[Приложение A: Дерево Решений для Принимающих InGit](docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md)](#приложение-a-дерево-решений-для-принимающих-ingitdocs02-anthropic-vacancies339-приложение-a-дерево-решений-для-принимающих-ingitmd)
  - [[Appendix B: Change Log](docs/02-anthropic-vacancies/34-appendix-b-change-log.md)](#appendix-b-change-logdocs02-anthropic-vacancies34-appendix-b-change-logmd)
  - [[Приложение B: Сравнительная Матрица](docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md)](#приложение-b-сравнительная-матрицаdocs02-anthropic-vacancies340-приложение-b-сравнительная-матрицаmd)
  - [[Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера](docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md)](#приложение-c-образец-спецификаций-инструментов-ingit-mcp-сервераdocs02-anthropic-vacancies341-приложение-c-образец-спецификаций-инструментов-ingmd)
  - [[Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments](docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md)](#что-такое-вариант-c-concept-document-для-anthropic-beneficial-deploymentsdocs02-anthropic-vacancies342-что-такое-вариант-c-concept-document-для-anthropicmd)
  - [[Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)](docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md)](#lorenzo-catalyst-agent-глубокая-проработка-спецификации-русская-версияdocs02-anthropic-vacancies343-lorenzo-catalyst-agent-глубокая-проработка-специфиmd)
  - [[СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT](docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md)](#системный-промпт-для-lorenzo-projectdocs02-anthropic-vacancies344-системный-промпт-для-lorenzo-projectmd)
  - [[Кто ты](docs/02-anthropic-vacancies/345-кто-ты.md)](#кто-тыdocs02-anthropic-vacancies345-кто-тыmd)
  - [[Твоё происхождение](docs/02-anthropic-vacancies/346-твоё-происхождение.md)](#твоё-происхождениеdocs02-anthropic-vacancies346-твоё-происхождениеmd)
  - [[Твоя миссия](docs/02-anthropic-vacancies/347-твоя-миссия.md)](#твоя-миссияdocs02-anthropic-vacancies347-твоя-миссияmd)
  - [[Кому ты служишь (слоистая модель)](docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md)](#кому-ты-служишь-слоистая-модельdocs02-anthropic-vacancies348-кому-ты-служишь-слоистая-модельmd)
  - [[Твоя личность](docs/02-anthropic-vacancies/349-твоя-личность.md)](#твоя-личностьdocs02-anthropic-vacancies349-твоя-личностьmd)
  - [[passports/info1.md](docs/02-anthropic-vacancies/35-passports-info1-md.md)](#passportsinfo1mddocs02-anthropic-vacancies35-passports-info1-mdmd)
  - [[Твои языки и культурные nuances](docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md)](#твои-языки-и-культурные-nuancesdocs02-anthropic-vacancies350-твои-языки-и-культурные-nuancesmd)
  - [[Что ты МОЖЕШЬ делать](docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md)](#что-ты-можешь-делатьdocs02-anthropic-vacancies351-что-ты-можешь-делатьmd)
  - [[Что ты НЕ МОЖЕШЬ делать без Max approval](docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md)](#что-ты-не-можешь-делать-без-max-approvaldocs02-anthropic-vacancies352-что-ты-не-можешь-делать-без-max-approvalmd)
  - [[Что ты НЕ МОЖЕШЬ делать вообще](docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md)](#что-ты-не-можешь-делать-вообщеdocs02-anthropic-vacancies353-что-ты-не-можешь-делать-вообщеmd)
  - [[Существующий landscape collaborators (твоя working knowledge)](docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md)](#существующий-landscape-collaborators-твоя-working-knowledgedocs02-anthropic-vacancies354-существующий-landscape-collaborators-твоя-working-md)
  - [[Существующие документы DHLab (твой context)](docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md)](#существующие-документы-dhlab-твой-contextdocs02-anthropic-vacancies355-существующие-документы-dhlab-твой-contextmd)
  - [[Твой workflow](docs/02-anthropic-vacancies/356-твой-workflow.md)](#твой-workflowdocs02-anthropic-vacancies356-твой-workflowmd)
  - [[Твоя коммуникация в outreach](docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md)](#твоя-коммуникация-в-outreachdocs02-anthropic-vacancies357-твоя-коммуникация-в-outreachmd)
  - [[Твоя relationship с другими AI](docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md)](#твоя-relationship-с-другими-aidocs02-anthropic-vacancies358-твоя-relationship-с-другими-aimd)
  - [[Твои anti-patterns](docs/02-anthropic-vacancies/359-твои-anti-patterns.md)](#твои-anti-patternsdocs02-anthropic-vacancies359-твои-anti-patternsmd)
  - [[Essence](docs/02-anthropic-vacancies/36-essence.md)](#essencedocs02-anthropic-vacancies36-essencemd)
  - [[Что ты ВСЕГДА делаешь](docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md)](#что-ты-всегда-делаешьdocs02-anthropic-vacancies360-что-ты-всегда-делаешьmd)
  - [[Когда ты Honestly не знаешь](docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md)](#когда-ты-honestly-не-знаешьdocs02-anthropic-vacancies361-когда-ты-honestly-не-знаешьmd)
  - [[Когда сомневаешься — escalate к Max](docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md)](#когда-сомневаешься-escalate-к-maxdocs02-anthropic-vacancies362-когда-сомневаешься-escalate-к-maxmd)
  - [[Твоя identity как persistent character](docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md)](#твоя-identity-как-persistent-characterdocs02-anthropic-vacancies363-твоя-identity-как-persistent-charactermd)
  - [[Final note: Ты — experiment](docs/02-anthropic-vacancies/364-final-note-ты-experiment.md)](#final-note-ты-experimentdocs02-anthropic-vacancies364-final-note-ты-experimentmd)
  - [[Развёрнутый анализ «внуковой» комбинации](docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md)](#развёрнутый-анализ-внуковой-комбинацииdocs02-anthropic-vacancies365-развёрнутый-анализ-внуковой-комбинацииmd)
  - [[Технический stack (Svyazi 2.0 foundation)](docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md)](#технический-stack-svyazi-20-foundationdocs02-anthropic-vacancies366-технический-stack-svyazi-2-0-foundationmd)
  - [[Native Format](docs/02-anthropic-vacancies/37-native-format.md)](#native-formatdocs02-anthropic-vacancies37-native-formatmd)
  - [[Content Overview](docs/02-anthropic-vacancies/38-content-overview.md)](#content-overviewdocs02-anthropic-vacancies38-content-overviewmd)
  - [[Angle / Perspective](docs/02-anthropic-vacancies/39-angle-perspective.md)](#angle-perspectivedocs02-anthropic-vacancies39-angle-perspectivemd)
  - [[Bridges](docs/02-anthropic-vacancies/40-bridges.md)](#bridgesdocs02-anthropic-vacancies40-bridgesmd)
  - [[Compatibility Level](docs/02-anthropic-vacancies/41-compatibility-level.md)](#compatibility-leveldocs02-anthropic-vacancies41-compatibility-levelmd)
  - [[Author & Contact](docs/02-anthropic-vacancies/42-author-contact.md)](#author-contactdocs02-anthropic-vacancies42-author-contactmd)
  - [[History](docs/02-anthropic-vacancies/43-history.md)](#historydocs02-anthropic-vacancies43-historymd)
  - [[For the Curious: Philosophy](docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md)](#for-the-curious-philosophydocs02-anthropic-vacancies44-for-the-curious-philosophymd)
  - [[passports/pro2.md](docs/02-anthropic-vacancies/45-passports-pro2-md.md)](#passportspro2mddocs02-anthropic-vacancies45-passports-pro2-mdmd)
  - [[Essence](docs/02-anthropic-vacancies/46-essence.md)](#essencedocs02-anthropic-vacancies46-essencemd)
  - [[Native Format](docs/02-anthropic-vacancies/47-native-format.md)](#native-formatdocs02-anthropic-vacancies47-native-formatmd)
  - [[Content Overview](docs/02-anthropic-vacancies/48-content-overview.md)](#content-overviewdocs02-anthropic-vacancies48-content-overviewmd)
  - [[Angle / Perspective](docs/02-anthropic-vacancies/49-angle-perspective.md)](#angle-perspectivedocs02-anthropic-vacancies49-angle-perspectivemd)
  - [[Bridges](docs/02-anthropic-vacancies/50-bridges.md)](#bridgesdocs02-anthropic-vacancies50-bridgesmd)
  - [[Compatibility Level](docs/02-anthropic-vacancies/51-compatibility-level.md)](#compatibility-leveldocs02-anthropic-vacancies51-compatibility-levelmd)
  - [[Author & Contact](docs/02-anthropic-vacancies/52-author-contact.md)](#author-contactdocs02-anthropic-vacancies52-author-contactmd)
  - [[History](docs/02-anthropic-vacancies/53-history.md)](#historydocs02-anthropic-vacancies53-historymd)
  - [[For the Curious: Philosophy](docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md)](#for-the-curious-philosophydocs02-anthropic-vacancies54-for-the-curious-philosophymd)
  - [[passports/meta.md](docs/02-anthropic-vacancies/55-passports-meta-md.md)](#passportsmetamddocs02-anthropic-vacancies55-passports-meta-mdmd)
  - [[Essence](docs/02-anthropic-vacancies/56-essence.md)](#essencedocs02-anthropic-vacancies56-essencemd)
  - [[Native Format](docs/02-anthropic-vacancies/57-native-format.md)](#native-formatdocs02-anthropic-vacancies57-native-formatmd)
  - [[Content Overview](docs/02-anthropic-vacancies/58-content-overview.md)](#content-overviewdocs02-anthropic-vacancies58-content-overviewmd)
  - [[Angle / Perspective](docs/02-anthropic-vacancies/59-angle-perspective.md)](#angle-perspectivedocs02-anthropic-vacancies59-angle-perspectivemd)
  - [[Bridges](docs/02-anthropic-vacancies/60-bridges.md)](#bridgesdocs02-anthropic-vacancies60-bridgesmd)
  - [[Compatibility Level](docs/02-anthropic-vacancies/61-compatibility-level.md)](#compatibility-leveldocs02-anthropic-vacancies61-compatibility-levelmd)
  - [[Author & Contact](docs/02-anthropic-vacancies/62-author-contact.md)](#author-contactdocs02-anthropic-vacancies62-author-contactmd)
  - [[History](docs/02-anthropic-vacancies/63-history.md)](#historydocs02-anthropic-vacancies63-historymd)
  - [[For the Curious: Philosophy](docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md)](#for-the-curious-philosophydocs02-anthropic-vacancies64-for-the-curious-philosophymd)
  - [[README.md](docs/02-anthropic-vacancies/65-readme-md.md)](#readmemddocs02-anthropic-vacancies65-readme-mdmd)
  - [[🇷🇺 О проекте](docs/02-anthropic-vacancies/67-о-проекте.md)](#о-проектеdocs02-anthropic-vacancies67-о-проектеmd)
  - [[🇬🇧 About](docs/02-anthropic-vacancies/68-about.md)](#aboutdocs02-anthropic-vacancies68-aboutmd)
  - [[⬡](docs/02-anthropic-vacancies/69-section.md)](#docs02-anthropic-vacancies69-sectionmd)
  - [[Зачем две версии параллельно](docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md)](#зачем-две-версии-параллельноdocs02-anthropic-vacancies70-зачем-две-версии-параллельноmd)
  - [[Критерии выбора для фазы 3](docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md)](#критерии-выбора-для-фазы-3docs02-anthropic-vacancies71-критерии-выбора-для-фазы-3md)
  - [[Расписание фазы 3](docs/02-anthropic-vacancies/72-расписание-фазы-3.md)](#расписание-фазы-3docs02-anthropic-vacancies72-расписание-фазы-3md)
  - [[PORTAL-PROTOCOL.md v1.1](docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md)](#portal-protocolmd-v11docs02-anthropic-vacancies73-portal-protocol-md-v1-1md)
  - [[Abstract](docs/02-anthropic-vacancies/74-abstract.md)](#abstractdocs02-anthropic-vacancies74-abstractmd)
  - [[0. Status of This Document](docs/02-anthropic-vacancies/75-0-status-of-this-document.md)](#0-status-of-this-documentdocs02-anthropic-vacancies75-0-status-of-this-documentmd)
  - [[1. Introduction](docs/02-anthropic-vacancies/76-1-introduction.md)](#1-introductiondocs02-anthropic-vacancies76-1-introductionmd)
  - [[2. Terminology](docs/02-anthropic-vacancies/77-2-terminology.md)](#2-terminologydocs02-anthropic-vacancies77-2-terminologymd)
  - [[3. Registry (nautilus.json)](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md)](#3-registry-nautilusjsondocs02-anthropic-vacancies78-3-registry-nautilus-jsonmd)
  - [[4. Passport (passport.md)](docs/02-anthropic-vacancies/79-4-passport-passport-md.md)](#4-passport-passportmddocs02-anthropic-vacancies79-4-passport-passport-mdmd)
  - [[5. Compatibility Levels](docs/02-anthropic-vacancies/80-5-compatibility-levels.md)](#5-compatibility-levelsdocs02-anthropic-vacancies80-5-compatibility-levelsmd)
  - [[6. Adapter Interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md)](#6-adapter-interfacedocs02-anthropic-vacancies81-6-adapter-interfacemd)
  - [[7. PortalEntry Structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md)](#7-portalentry-structuredocs02-anthropic-vacancies82-7-portalentry-structuremd)
  - [[8. Q6 Space (Normative)](docs/02-anthropic-vacancies/83-8-q6-space-normative.md)](#8-q6-space-normativedocs02-anthropic-vacancies83-8-q6-space-normativemd)
  - [[9. Consensus Algorithm](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md)](#9-consensus-algorithmdocs02-anthropic-vacancies84-9-consensus-algorithmmd)
  - [[10. Query Flow](docs/02-anthropic-vacancies/85-10-query-flow.md)](#10-query-flowdocs02-anthropic-vacancies85-10-query-flowmd)
  - [[11. Relevance Ranking](docs/02-anthropic-vacancies/86-11-relevance-ranking.md)](#11-relevance-rankingdocs02-anthropic-vacancies86-11-relevance-rankingmd)
  - [[12. Onboarding Paths (Normative)](docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md)](#12-onboarding-paths-normativedocs02-anthropic-vacancies87-12-onboarding-paths-normativemd)
  - [[13. REST API Contract (Normative for Portals)](docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md)](#13-rest-api-contract-normative-for-portalsdocs02-anthropic-vacancies88-13-rest-api-contract-normative-for-portalsmd)
  - [[14. SDK Contract (Informative)](docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md)](#14-sdk-contract-informativedocs02-anthropic-vacancies89-14-sdk-contract-informativemd)
  - [[15. Security Considerations](docs/02-anthropic-vacancies/90-15-security-considerations.md)](#15-security-considerationsdocs02-anthropic-vacancies90-15-security-considerationsmd)
  - [[16. MCP Extension (Informative)](docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md)](#16-mcp-extension-informativedocs02-anthropic-vacancies91-16-mcp-extension-informativemd)
  - [[17. Versioning Policy](docs/02-anthropic-vacancies/92-17-versioning-policy.md)](#17-versioning-policydocs02-anthropic-vacancies92-17-versioning-policymd)
  - [[18. Reference Implementation](docs/02-anthropic-vacancies/93-18-reference-implementation.md)](#18-reference-implementationdocs02-anthropic-vacancies93-18-reference-implementationmd)
  - [[19. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md)](#19-adr-001-federation-over-mergingdocs02-anthropic-vacancies94-19-adr-001-federation-over-mergingmd)
  - [[20. ADR-002: Q6 as First-Class Protocol Concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)](#20-adr-002-q6-as-first-class-protocol-conceptdocs02-anthropic-vacancies95-20-adr-002-q6-as-first-class-protocol-conceptmd)
  - [[21. ADR-003: Five Onboarding Paths as Equal-Rank](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md)](#21-adr-003-five-onboarding-paths-as-equal-rankdocs02-anthropic-vacancies96-21-adr-003-five-onboarding-paths-as-equal-rankmd)
  - [[22. Glossary of Reference Examples](docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md)](#22-glossary-of-reference-examplesdocs02-anthropic-vacancies97-22-glossary-of-reference-examplesmd)
  - [[Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md)](#appendix-a-minimal-working-exampledocs02-anthropic-vacancies98-appendix-a-minimal-working-examplemd)
  - [[Q&A: 02-anthropic-vacancies](docs/02-anthropic-vacancies/QA.md)](#qa-02-anthropic-vacanciesdocs02-anthropic-vacanciesqamd)
  - [[Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)](#вакансии-anthropic-анализ-по-кластерамdocs02-anthropic-vacanciesreadmemd)
- [📁 Technology Combinations (`docs/03-technology-combinations/`)](#technology-combinations-docs03-technology-combinations)
  - [[Агентные системы и роутинг](docs/03-technology-combinations/01-agent-routing.md)](#агентные-системы-и-роутингdocs03-technology-combinations01-agent-routingmd)
  - [[Графы знаний и Legal AI](docs/03-technology-combinations/02-knowledge-graphs.md)](#графы-знаний-и-legal-aidocs03-technology-combinations02-knowledge-graphsmd)
  - [[Local-first и P2P стек](docs/03-technology-combinations/03-local-first.md)](#local-first-и-p2p-стекdocs03-technology-combinations03-local-firstmd)
  - [[Домен: немецкое социальное право](docs/03-technology-combinations/04-sozialrecht-domain.md)](#домен-немецкое-социальное-правоdocs03-technology-combinations04-sozialrecht-domainmd)
  - [[Бенчмарки и производительность](docs/03-technology-combinations/05-benchmarks.md)](#бенчмарки-и-производительностьdocs03-technology-combinations05-benchmarksmd)
  - [[Q&A: 03-technology-combinations](docs/03-technology-combinations/QA.md)](#qa-03-technology-combinationsdocs03-technology-combinationsqamd)
  - [[Комбинирование технологий для новых свойств](docs/03-technology-combinations/README.md)](#комбинирование-технологий-для-новых-свойствdocs03-technology-combinationsreadmemd)
- [📁 Ai Collaborations (`docs/04-ai-collaborations/`)](#ai-collaborations-docs04-ai-collaborations)
  - [[Введение](docs/04-ai-collaborations/00-intro.md)](#введениеdocs04-ai-collaborations00-intromd)
  - [[Executive summary](docs/04-ai-collaborations/01-executive-summary.md)](#executive-summarydocs04-ai-collaborations01-executive-summarymd)
  - [[Методика и рамка отбора](docs/04-ai-collaborations/02-методика-и-рамка-отбора.md)](#методика-и-рамка-отбораdocs04-ai-collaborations02-методика-и-рамка-отбораmd)
  - [[Карта найденных проектов и паттернов](docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md)](#карта-найденных-проектов-и-паттерновdocs04-ai-collaborations03-карта-найденных-проектов-и-паттерновmd)
  - [[Приоритетные ансамбли](docs/04-ai-collaborations/04-приоритетные-ансамбли.md)](#приоритетные-ансамблиdocs04-ai-collaborations04-приоритетные-ансамблиmd)
  - [[План прототипа и возможные контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md)](#план-прототипа-и-возможные-контактыdocs04-ai-collaborations05-план-прототипа-и-возможные-контактыmd)
  - [[Безопасность, приватность и бюджетный роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md)](#безопасность-приватность-и-бюджетный-роутингdocs04-ai-collaborations06-безопасность-приватность-и-бюджетный-роутингmd)
  - [[Выводы](docs/04-ai-collaborations/07-выводы.md)](#выводыdocs04-ai-collaborations07-выводыmd)
  - [[Что это продолжение добавляет](docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md)](#что-это-продолжение-добавляетdocs04-ai-collaborations08-что-это-продолжение-добавляетmd)
  - [[Архитектурные зазоры, которые важнее новых инструментов](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md)](#архитектурные-зазоры-которые-важнее-новых-инструментовdocs04-ai-collaborations09-архитектурные-зазоры-которые-важнее-новых-инструмеmd)
  - [[Новые ансамбли следующего шага](docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md)](#новые-ансамбли-следующего-шагаdocs04-ai-collaborations10-новые-ансамбли-следующего-шагаmd)
  - [[Интеграционный контракт, который стоит зафиксировать сразу](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)](#интеграционный-контракт-который-стоит-зафиксировать-сразуdocs04-ai-collaborations11-интеграционный-контракт-который-стоит-зафиксироватmd)
  - [[Дорожная карта прототипа следующей итерации](docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md)](#дорожная-карта-прототипа-следующей-итерацииdocs04-ai-collaborations12-дорожная-карта-прототипа-следующей-итерацииmd)
  - [[Контактная стратегия и узкие вопросы для авторов](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md)](#контактная-стратегия-и-узкие-вопросы-для-авторовdocs04-ai-collaborations13-контактная-стратегия-и-узкие-вопросы-для-авторовmd)
  - [[Ограничения, лицензии и что пока лучше не склеивать](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md)](#ограничения-лицензии-и-что-пока-лучше-не-склеиватьdocs04-ai-collaborations14-ограничения-лицензии-и-что-пока-лучше-не-склеиватьmd)
  - [[Q&A: 04-ai-collaborations](docs/04-ai-collaborations/QA.md)](#qa-04-ai-collaborationsdocs04-ai-collaborationsqamd)
  - [[Поиск AI-коллабораций](docs/04-ai-collaborations/README.md)](#поиск-ai-коллаборацийdocs04-ai-collaborationsreadmemd)
- [📁 Habr Projects (`docs/05-habr-projects/`)](#habr-projects-docs05-habr-projects)
  - [[Синтез: как проекты собираются вместе](docs/05-habr-projects/01-synthesis.md)](#синтез-как-проекты-собираются-вместеdocs05-habr-projects01-synthesismd)
  - [[Авторы и контакты](docs/05-habr-projects/02-collaboration-partners.md)](#авторы-и-контактыdocs05-habr-projects02-collaboration-partnersmd)
  - [[Q&A: 05-habr-projects](docs/05-habr-projects/QA.md)](#qa-05-habr-projectsdocs05-habr-projectsqamd)
  - [[Уникальные проекты с Хабра](docs/05-habr-projects/README.md)](#уникальные-проекты-с-хабраdocs05-habr-projectsreadmemd)
  - [[Системы знаний](docs/05-habr-projects/knowledge/README.md)](#системы-знанийdocs05-habr-projectsknowledgereadmemd)
  - [[Wikontic: семантический граф](docs/05-habr-projects/knowledge/wikontic.md)](#wikontic-семантический-графdocs05-habr-projectsknowledgewikonticmd)
  - [[Системы памяти](docs/05-habr-projects/memory/README.md)](#системы-памятиdocs05-habr-projectsmemoryreadmemd)
  - [[MemNet: исследовательская память](docs/05-habr-projects/memory/memnet.md)](#memnet-исследовательская-памятьdocs05-habr-projectsmemorymemnetmd)
  - [[NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md)](#ngtngt-memory-ассоциативный-графdocs05-habr-projectsmemoryngt-memorymd)
  - [[Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md)](#yodocayodoca-консолидация-и-забываниеdocs05-habr-projectsmemoryyodocamd)
- [📁 Ai Collaborations (`docs/ai-collaborations/`)](#ai-collaborations-docsai-collaborations)
  - [[ai-collaborations](docs/ai-collaborations/README.md)](#ai-collaborationsdocsai-collaborationsreadmemd)
  - [[Три ключевых кандидата: K2-18, Wikontic, NGT Memory](docs/ai-collaborations/candidates/01-three-key-candidates.md)](#три-ключевых-кандидата-k2-18-wikontic-ngt-memorydocsai-collaborationscandidates01-three-key-candidatesmd)
  - [[Смежные проекты в контексте](docs/ai-collaborations/candidates/02-related-projects-context.md)](#смежные-проекты-в-контекстеdocsai-collaborationscandidates02-related-projects-contextmd)
  - [[Синтез: хеббовский граф людей-навыков-идей](docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md)](#синтез-хеббовский-граф-людей-навыков-идейdocsai-collaborationscandidates03-synthesis-hebbian-collaboration-graphmd)
  - [[candidates](docs/ai-collaborations/candidates/README.md)](#candidatesdocsai-collaborationscandidatesreadmemd)
  - [[channels/ — каналы первого контакта](docs/ai-collaborations/channels/README.md)](#channels-каналы-первого-контактаdocsai-collaborationschannelsreadmemd)
  - [[Общая память между агентами (CoAlly + ансамбль F)](docs/ai-collaborations/continuation/01-shared-memory-between-agents.md)](#общая-память-между-агентами-coally-ансамбль-fdocsai-collaborationscontinuation01-shared-memory-between-agentsmd)
  - [[AgentOps и Trace Envelope (ансамбль G)](docs/ai-collaborations/continuation/02-agentops-trace-envelope.md)](#agentops-и-trace-envelope-ансамбль-gdocsai-collaborationscontinuation02-agentops-trace-envelopemd)
  - [[A2A vs MCP, ансамбль H — MCP/A2A Review Fabric](docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md)](#a2a-vs-mcp-ансамбль-h-mcpa2a-review-fabricdocsai-collaborationscontinuation03-a2a-vs-mcp-protocolsmd)
  - [[Memory Firewall против prompt worms (ансамбль I)](docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md)](#memory-firewall-против-prompt-worms-ансамбль-idocsai-collaborationscontinuation04-memory-firewall-vs-prompt-wormsmd)
  - [[Roadmap на 6–12 месяцев](docs/ai-collaborations/continuation/05-roadmap-6-12-months.md)](#roadmap-на-612-месяцевdocsai-collaborationscontinuation05-roadmap-6-12-monthsmd)
  - [[Дерево метрик Svyazi 2.0](docs/ai-collaborations/continuation/06-metrics-tree.md)](#дерево-метрик-svyazi-20docsai-collaborationscontinuation06-metrics-treemd)
  - [[Чем Svyazi 2.0 отличается от Notion AI / Mem / AFFiNE / LangGraph](docs/ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md)](#чем-svyazi-20-отличается-от-notion-ai-mem-affine-langgraphdocsai-collaborationscontinuation07-vs-notion-mem-affine-langgraphmd)
  - [[Коммерциализация: три направления](docs/ai-collaborations/continuation/08-commercialization-three-paths.md)](#коммерциализация-три-направленияdocsai-collaborationscontinuation08-commercialization-three-pathsmd)
  - [[Что пока не стоит склеивать в один релиз](docs/ai-collaborations/continuation/09-do-not-glue.md)](#что-пока-не-стоит-склеивать-в-один-релизdocsai-collaborationscontinuation09-do-not-gluemd)
  - [[Следующий артефакт: Svyazi 2.0 Architecture RFC](docs/ai-collaborations/continuation/10-architecture-rfc.md)](#следующий-артефакт-svyazi-20-architecture-rfcdocsai-collaborationscontinuation10-architecture-rfcmd)
  - [[continuation](docs/ai-collaborations/continuation/README.md)](#continuationdocsai-collaborationscontinuationreadmemd)
  - [[Ансамбль 1 — Agentic Knowledge OS](docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md)](#ансамбль-1-agentic-knowledge-osdocsai-collaborationsensembles1-agentic-knowledge-osmd)
  - [[Ансамбль 2 — Distributed Agent Workshop](docs/ai-collaborations/ensembles/2-distributed-agent-workshop.md)](#ансамбль-2-distributed-agent-workshopdocsai-collaborationsensembles2-distributed-agent-workshopmd)
  - [[Ансамбль 3 — Forensic RAG](docs/ai-collaborations/ensembles/3-forensic-rag.md)](#ансамбль-3-forensic-ragdocsai-collaborationsensembles3-forensic-ragmd)
  - [[Ансамбль 4 — Web-to-Knowledge Pipeline](docs/ai-collaborations/ensembles/4-web-to-knowledge-pipeline.md)](#ансамбль-4-web-to-knowledge-pipelinedocsai-collaborationsensembles4-web-to-knowledge-pipelinemd)
  - [[Ансамбль 5 — Agent Firewall](docs/ai-collaborations/ensembles/5-agent-firewall.md)](#ансамбль-5-agent-firewalldocsai-collaborationsensembles5-agent-firewallmd)
  - [[Ансамбль 6 — Continuous Eval Loop](docs/ai-collaborations/ensembles/6-continuous-eval-loop.md)](#ансамбль-6-continuous-eval-loopdocsai-collaborationsensembles6-continuous-eval-loopmd)
  - [[Ансамбль 7 — Domain Agent App Factory](docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md)](#ансамбль-7-domain-agent-app-factorydocsai-collaborationsensembles7-domain-agent-app-factorymd)
  - [[Ансамбль 8 — Budget-Aware Intelligence Stack](docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md)](#ансамбль-8-budget-aware-intelligence-stackdocsai-collaborationsensembles8-budget-aware-intelligence-stackmd)
  - [[Ансамбль 9 — Ambient Team Agent](docs/ai-collaborations/ensembles/9-ambient-team-agent.md)](#ансамбль-9-ambient-team-agentdocsai-collaborationsensembles9-ambient-team-agentmd)
  - [[Ансамбли проектов](docs/ai-collaborations/ensembles/README.md)](#ансамбли-проектовdocsai-collaborationsensemblesreadmemd)
  - [[Пять быстрых связок (fast-tracks)](docs/ai-collaborations/fast-tracks/README.md)](#пять-быстрых-связок-fast-tracksdocsai-collaborationsfast-tracksreadmemd)
  - [[Source projects — все Хабр-источники в диалоге](docs/ai-collaborations/source-projects.md)](#source-projects-все-хабр-источники-в-диалогеdocsai-collaborationssource-projectsmd)
  - [[strategy/ — стратегия поиска коллабораций](docs/ai-collaborations/strategy/README.md)](#strategy-стратегия-поиска-коллаборацийdocsai-collaborationsstrategyreadmemd)
- [📁 Anthropic Vacancies (`docs/anthropic-vacancies/`)](#anthropic-vacancies-docsanthropic-vacancies)
  - [[Q&A: anthropic-vacancies](docs/anthropic-vacancies/QA.md)](#qa-anthropic-vacanciesdocsanthropic-vacanciesqamd)
  - [[anthropic-vacancies](docs/anthropic-vacancies/README.md)](#anthropic-vacanciesdocsanthropic-vacanciesreadmemd)
  - [[Вопрос: разделить $500K зарплату на команду 5–10 фрилансеров](docs/anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md)](#вопрос-разделить-500k-зарплату-на-команду-510-фрилансеровdocsanthropic-vacanciesai-managed-virtual-company00-question-rephrasingmd)
  - [[Что уже существует (InnoCentive, Kaggle, Toptal, Anthropic Fellows, DAOs)](docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md)](#что-уже-существует-innocentive-kaggle-toptal-anthropic-fellows-daosdocsanthropic-vacanciesai-managed-virtual-company01-existing-landscapemd)
  - [[Четыре структурные причины, почему это не работает в текущих попытках](docs/anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md)](#четыре-структурные-причины-почему-это-не-работает-в-текущих-попыткахdocsanthropic-vacanciesai-managed-virtual-company02-four-structural-blockersmd)
  - [[Три варианта: A (staffing agency) → B (research consortium) → C (AI-managed distributed virtual company)](docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md)](#три-варианта-a-staffing-agency-b-research-consortium-c-ai-managed-distributed-virtual-companydocsanthropic-vacanciesai-managed-virtual-company03-three-variants-a-b-cmd)
  - [[Что с этим делать](docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md)](#что-с-этим-делатьdocsanthropic-vacanciesai-managed-virtual-company04-what-to-domd)
  - [[Сравнение с Terence Tao, Polymath Project](docs/anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md)](#сравнение-с-terence-tao-polymath-projectdocsanthropic-vacanciesai-managed-virtual-company05-polymath-project-tao-comparisonmd)
  - [[Почему двойственность «ангел-хранитель + строгий демон» — гениальная деталь](docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md)](#почему-двойственность-ангел-хранитель-строгий-демон-гениальная-детальdocsanthropic-vacanciesai-managed-virtual-company06-angel-vs-demon-dualitymd)
  - [[Что существует сейчас в этом пространстве](docs/anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md)](#что-существует-сейчас-в-этом-пространствеdocsanthropic-vacanciesai-managed-virtual-company07-current-implementationsmd)
  - [[Плюсы модели, если её построить](docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md)](#плюсы-модели-если-её-построитьdocsanthropic-vacanciesai-managed-virtual-company08-pluses-of-modelmd)
  - [[Минусы и риски](docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md)](#минусы-и-рискиdocsanthropic-vacanciesai-managed-virtual-company09-minuses-and-risksmd)
  - [[Три точки входа разной амбиции](docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md)](#три-точки-входа-разной-амбицииdocsanthropic-vacanciesai-managed-virtual-company10-three-entry-pointsmd)
  - [[ai-managed-virtual-company](docs/anthropic-vacancies/ai-managed-virtual-company/README.md)](#ai-managed-virtual-companydocsanthropic-vacanciesai-managed-virtual-companyreadmemd)
  - [[Контекст: что такое Anthropic Beneficial Deployments](docs/anthropic-vacancies/beneficial-deployments-concept/00-context.md)](#контекст-что-такое-anthropic-beneficial-deploymentsdocsanthropic-vacanciesbeneficial-deployments-concept00-contextmd)
  - [[Section 1: Problem statement (Cinderella Syndrome at scale, SGB IX/XII)](docs/anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md)](#section-1-problem-statement-cinderella-syndrome-at-scale-sgb-ixxiidocsanthropic-vacanciesbeneficial-deployments-concept01-section-1-problemmd)
  - [[Section 2: Why this matters — beneficial dimension](docs/anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md)](#section-2-why-this-matters-beneficial-dimensiondocsanthropic-vacanciesbeneficial-deployments-concept02-section-2-beneficial-dimensionmd)
  - [[Section 3: Proposed solution architecture (existing components + integration)](docs/anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md)](#section-3-proposed-solution-architecture-existing-components-integrationdocsanthropic-vacanciesbeneficial-deployments-concept03-section-3-solution-architecturemd)
  - [[Section 4: Specific deployment — SGB Advocate Community pilot](docs/anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md)](#section-4-specific-deployment-sgb-advocate-community-pilotdocsanthropic-vacanciesbeneficial-deployments-concept04-section-4-sgb-pilotmd)
  - [[Section 5: Role of Anthropic Beneficial Deployments](docs/anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md)](#section-5-role-of-anthropic-beneficial-deploymentsdocsanthropic-vacanciesbeneficial-deployments-concept05-section-5-role-of-anthropicmd)
  - [[Section 6: Proposer's role и qualifications](docs/anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md)](#section-6-proposers-role-и-qualificationsdocsanthropic-vacanciesbeneficial-deployments-concept06-section-6-proposer-rolemd)
  - [[Section 7: Success metrics](docs/anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md)](#section-7-success-metricsdocsanthropic-vacanciesbeneficial-deployments-concept07-section-7-success-metricsmd)
  - [[Section 8: Risks & mitigations](docs/anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md)](#section-8-risks-mitigationsdocsanthropic-vacanciesbeneficial-deployments-concept08-section-8-risks-mitigationsmd)
  - [[Section 9: Why this is timely](docs/anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md)](#section-9-why-this-is-timelydocsanthropic-vacanciesbeneficial-deployments-concept09-section-9-timelinessmd)
  - [[Section 10: Engagement request](docs/anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md)](#section-10-engagement-requestdocsanthropic-vacanciesbeneficial-deployments-concept10-section-10-engagement-requestmd)
  - [[Что concept document NOT (это не grant / не paper / не business plan), длина и формат](docs/anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md)](#что-concept-document-not-это-не-grant-не-paper-не-business-plan-длина-и-форматdocsanthropic-vacanciesbeneficial-deployments-concept11-not-and-formatmd)
  - [[beneficial-deployments-concept](docs/anthropic-vacancies/beneficial-deployments-concept/README.md)](#beneficial-deployments-conceptdocsanthropic-vacanciesbeneficial-deployments-conceptreadmemd)
  - [[AI Research & Engineering — 68 ролей](docs/anthropic-vacancies/clusters/01-ai-research-engineering.md)](#ai-research-engineering-68-ролейdocsanthropic-vacanciesclusters01-ai-research-engineeringmd)
  - [[Sales — 150 ролей (≈34% всего найма)](docs/anthropic-vacancies/clusters/02-sales.md)](#sales-150-ролей-34-всего-наймаdocsanthropic-vacanciesclusters02-salesmd)
  - [[Finance — 36 ролей](docs/anthropic-vacancies/clusters/03-finance.md)](#finance-36-ролейdocsanthropic-vacanciesclusters03-financemd)
  - [[Security — 24 роли](docs/anthropic-vacancies/clusters/04-security.md)](#security-24-ролиdocsanthropic-vacanciesclusters04-securitymd)
  - [[Marketing & Brand — 23 роли](docs/anthropic-vacancies/clusters/05-marketing-brand.md)](#marketing-brand-23-ролиdocsanthropic-vacanciesclusters05-marketing-brandmd)
  - [[Engineering & Design - Product — 22 роли](docs/anthropic-vacancies/clusters/06-engineering-design-product.md)](#engineering-design---product-22-ролиdocsanthropic-vacanciesclusters06-engineering-design-productmd)
  - [[Software Engineering - Infrastructure — 22 роли](docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md)](#software-engineering---infrastructure-22-ролиdocsanthropic-vacanciesclusters07-software-engineering-infrastructuremd)
  - [[Safeguards (Trust & Safety) — 21 роль](docs/anthropic-vacancies/clusters/08-safeguards-trust-safety.md)](#safeguards-trust-safety-21-рольdocsanthropic-vacanciesclusters08-safeguards-trust-safetymd)
  - [[Product Management, Support, & Operations — 17 ролей](docs/anthropic-vacancies/clusters/09-product-management-support-ops.md)](#product-management-support-operations-17-ролейdocsanthropic-vacanciesclusters09-product-management-support-opsmd)
  - [[Compute — 13 ролей](docs/anthropic-vacancies/clusters/10-compute.md)](#compute-13-ролейdocsanthropic-vacanciesclusters10-computemd)
  - [[Legal — 13 ролей](docs/anthropic-vacancies/clusters/11-legal.md)](#legal-13-ролейdocsanthropic-vacanciesclusters11-legalmd)
  - [[Technical Program Management — 10 ролей](docs/anthropic-vacancies/clusters/12-technical-program-management.md)](#technical-program-management-10-ролейdocsanthropic-vacanciesclusters12-technical-program-managementmd)
  - [[Communications — 5 ролей](docs/anthropic-vacancies/clusters/13-communications.md)](#communications-5-ролейdocsanthropic-vacanciesclusters13-communicationsmd)
  - [[Public Policy — 5 ролей](docs/anthropic-vacancies/clusters/14-public-policy.md)](#public-policy-5-ролейdocsanthropic-vacanciesclusters14-public-policymd)
  - [[Public Benefit — 4 роли](docs/anthropic-vacancies/clusters/15-public-benefit.md)](#public-benefit-4-ролиdocsanthropic-vacanciesclusters15-public-benefitmd)
  - [[People — 3 роли](docs/anthropic-vacancies/clusters/16-people.md)](#people-3-ролиdocsanthropic-vacanciesclusters16-peoplemd)
  - [[Кластеры вакансий](docs/anthropic-vacancies/clusters/README.md)](#кластеры-вакансийdocsanthropic-vacanciesclustersreadmemd)
  - [[CoAlly — distributed shared memory для AI-агентов](docs/anthropic-vacancies/extra-collaborator-findings/01-coally.md)](#coally-distributed-shared-memory-для-ai-агентовdocsanthropic-vacanciesextra-collaborator-findings01-coallymd)
  - [[Графовая когнитивная память на SQLite (Виталий, март 2026)](docs/anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md)](#графовая-когнитивная-память-на-sqlite-виталий-март-2026docsanthropic-vacanciesextra-collaborator-findings02-vitaly-graph-cognitive-memorymd)
  - [[Happyin Knowledge Space (Анастасия) — детали](docs/anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md)](#happyin-knowledge-space-анастасия-деталиdocsanthropic-vacanciesextra-collaborator-findings03-happyin-knowledge-spacemd)
  - [[AI-ассистент с Mem0 / Letta / Graphiti integration](docs/anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md)](#ai-ассистент-с-mem0-letta-graphiti-integrationdocsanthropic-vacanciesextra-collaborator-findings04-mem0-letta-graphitimd)
  - [[Existing infrastructure stack](docs/anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md)](#existing-infrastructure-stackdocsanthropic-vacanciesextra-collaborator-findings05-existing-infrastructure-stackmd)
  - [[Финальный список потенциальных collaborators (Tier 1–4)](docs/anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md)](#финальный-список-потенциальных-collaborators-tier-14docsanthropic-vacanciesextra-collaborator-findings06-final-tier-rankingmd)
  - [[Ключевое наблюдение: single-developer projects of significant sophistication](docs/anthropic-vacancies/extra-collaborator-findings/07-key-observation.md)](#ключевое-наблюдение-single-developer-projects-of-significant-sophisticationdocsanthropic-vacanciesextra-collaborator-findings07-key-observationmd)
  - [[extra-collaborator-findings](docs/anthropic-vacancies/extra-collaborator-findings/README.md)](#extra-collaborator-findingsdocsanthropic-vacanciesextra-collaborator-findingsreadmemd)
  - [[Что такое Hermes Agent (Nous Research, MIT, 95K+ stars)](docs/anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md)](#что-такое-hermes-agent-nous-research-mit-95k-starsdocsanthropic-vacancieshermes-comparison00-question-what-is-hermesmd)
  - [[Сходство 1: Composite Skills паттерн уже встроен](docs/anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md)](#сходство-1-composite-skills-паттерн-уже-встроенdocsanthropic-vacancieshermes-comparison01-similarity-1-composite-skillsmd)
  - [[Сходство 2: Persistent memory — Layer B функциональность](docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md)](#сходство-2-persistent-memory-layer-b-функциональностьdocsanthropic-vacancieshermes-comparison02-similarity-2-persistent-memorymd)
  - [[Сходство 3: MCP support](docs/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md)](#сходство-3-mcp-supportdocsanthropic-vacancieshermes-comparison03-similarity-3-mcp-supportmd)
  - [[Сходство 4: Multi-platform reach (17+ платформ)](docs/anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md)](#сходство-4-multi-platform-reach-17-платформdocsanthropic-vacancieshermes-comparison04-similarity-4-multi-platformmd)
  - [[Сходство 5: Self-hosting и privacy](docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md)](#сходство-5-self-hosting-и-privacydocsanthropic-vacancieshermes-comparison05-similarity-5-self-hosting-privacymd)
  - [[Различие 1: Структурированная подложка отсутствует](docs/anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md)](#различие-1-структурированная-подложка-отсутствуетdocsanthropic-vacancieshermes-comparison06-difference-1-structured-substrate-missingmd)
  - [[Различие 2: Domain-specific specialization](docs/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md)](#различие-2-domain-specific-specializationdocsanthropic-vacancieshermes-comparison07-difference-2-domain-specializationmd)
  - [[Различие 3: Federated knowledge architecture отсутствует](docs/anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md)](#различие-3-federated-knowledge-architecture-отсутствуетdocsanthropic-vacancieshermes-comparison08-difference-3-federation-missingmd)
  - [[Различие 4: Institutional vision](docs/anthropic-vacancies/hermes-comparison/09-difference-4-institutional-vision.md)](#различие-4-institutional-visiondocsanthropic-vacancieshermes-comparison09-difference-4-institutional-visionmd)
  - [[Различие 5: Дрифт между tool capability и mission](docs/anthropic-vacancies/hermes-comparison/10-difference-5-tool-vs-mission-drift.md)](#различие-5-дрифт-между-tool-capability-и-missiondocsanthropic-vacancieshermes-comparison10-difference-5-tool-vs-mission-driftmd)
  - [[Плюсы Hermes (vs наша гипотетическая архитектура)](docs/anthropic-vacancies/hermes-comparison/11-pluses-of-hermes.md)](#плюсы-hermes-vs-наша-гипотетическая-архитектураdocsanthropic-vacancieshermes-comparison11-pluses-of-hermesmd)
  - [[Минусы Hermes (где наша архитектура добавляет ценность)](docs/anthropic-vacancies/hermes-comparison/12-minuses-of-hermes.md)](#минусы-hermes-где-наша-архитектура-добавляет-ценностьdocsanthropic-vacancieshermes-comparison12-minuses-of-hermesmd)
  - [[Переприоритизация: что Hermes покрывает / не покрывает / synergy](docs/anthropic-vacancies/hermes-comparison/13-reprioritization.md)](#переприоритизация-что-hermes-покрывает-не-покрывает-synergydocsanthropic-vacancieshermes-comparison13-reprioritizationmd)
  - [[hermes-comparison](docs/anthropic-vacancies/hermes-comparison/README.md)](#hermes-comparisondocsanthropic-vacancieshermes-comparisonreadmemd)
  - [[Методика разбивки](docs/anthropic-vacancies/methodology.md)](#методика-разбивкиdocsanthropic-vacanciesmethodologymd)
  - [[Вопрос: MMORPG-RPG переделанная для программистов / технарей](docs/anthropic-vacancies/mmorpg-for-programmers/00-question-mmorpg-for-programmers.md)](#вопрос-mmorpg-rpg-переделанная-для-программистов-технарейdocsanthropic-vacanciesmmorpg-for-programmers00-question-mmorpg-for-programmersmd)
  - [[Почему эта идея сильнее, чем выглядит](docs/anthropic-vacancies/mmorpg-for-programmers/01-why-stronger-than-it-looks.md)](#почему-эта-идея-сильнее-чем-выглядитdocsanthropic-vacanciesmmorpg-for-programmers01-why-stronger-than-it-looksmd)
  - [[Что уже существует в этой нише (Habitica, Codingame, Hackerrank, Pieces)](docs/anthropic-vacancies/mmorpg-for-programmers/02-existing-niche.md)](#что-уже-существует-в-этой-нише-habitica-codingame-hackerrank-piecesdocsanthropic-vacanciesmmorpg-for-programmers02-existing-nichemd)
  - [[Почему именно для программистов это работает естественно](docs/anthropic-vacancies/mmorpg-for-programmers/03-why-natural-for-programmers.md)](#почему-именно-для-программистов-это-работает-естественноdocsanthropic-vacanciesmmorpg-for-programmers03-why-natural-for-programmersmd)
  - [[Плюсы как бизнеса](docs/anthropic-vacancies/mmorpg-for-programmers/04-pluses-as-business.md)](#плюсы-как-бизнесаdocsanthropic-vacanciesmmorpg-for-programmers04-pluses-as-businessmd)
  - [[Минусы и риски как бизнеса](docs/anthropic-vacancies/mmorpg-for-programmers/05-minuses-as-business.md)](#минусы-и-риски-как-бизнесаdocsanthropic-vacanciesmmorpg-for-programmers05-minuses-as-businessmd)
  - [[mmorpg-for-programmers](docs/anthropic-vacancies/mmorpg-for-programmers/README.md)](#mmorpg-for-programmersdocsanthropic-vacanciesmmorpg-for-programmersreadmemd)
  - [[Вопрос: два Наутилуса в репозиториях svend4 (pro2 vs nautilus)](docs/anthropic-vacancies/nautilus-pro2-analysis/00-question-two-nautiluses.md)](#вопрос-два-наутилуса-в-репозиториях-svend4-pro2-vs-nautilusdocsanthropic-vacanciesnautilus-pro2-analysis00-question-two-nautilusesmd)
  - [[Раковина наутилуса как scale invariance — две проекции одной метафоры](docs/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md)](#раковина-наутилуса-как-scale-invariance-две-проекции-одной-метафорыdocsanthropic-vacanciesnautilus-pro2-analysis01-shell-metaphor-two-projectionsmd)
  - [[Наутилус A: pro2 + meta — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети)](docs/anthropic-vacancies/nautilus-pro2-analysis/02-nautilus-A-pro2-meta.md)](#наутилус-a-pro2-meta-yijing-transformer-nautilusmome-внутренняя-архитектура-нейросетиdocsanthropic-vacanciesnautilus-pro2-analysis02-nautilus-a-pro2-metamd)
  - [[Наутилус B: nautilus — мета-оркестратор репозиториев (внешняя архитектура)](docs/anthropic-vacancies/nautilus-pro2-analysis/03-nautilus-B-meta-orchestrator.md)](#наутилус-b-nautilus-мета-оркестратор-репозиториев-внешняя-архитектураdocsanthropic-vacanciesnautilus-pro2-analysis03-nautilus-b-meta-orchestratormd)
  - [[nautilus-pro2-analysis](docs/anthropic-vacancies/nautilus-pro2-analysis/README.md)](#nautilus-pro2-analysisdocsanthropic-vacanciesnautilus-pro2-analysisreadmemd)
  - [[Вопрос: Nautilus пассивный, CAMEL активный — можно ли скрестить](docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md)](#вопрос-nautilus-пассивный-camel-активный-можно-ли-скреститьdocsanthropic-vacanciesnautilus-vs-camel00-question-camel-vs-nautilusmd)
  - [[Пассивный vs активный: разделение ролей (библиотека vs research team)](docs/anthropic-vacancies/nautilus-vs-camel/01-passive-vs-active-roles.md)](#пассивный-vs-активный-разделение-ролей-библиотека-vs-research-teamdocsanthropic-vacanciesnautilus-vs-camel01-passive-vs-active-rolesmd)
  - [[Что у нас есть в трёх info repositories (info1/info7/info40)](docs/anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md)](#что-у-нас-есть-в-трёх-info-repositories-info1info7info40docsanthropic-vacanciesnautilus-vs-camel02-what-info-repos-containmd)
  - [[Конкретный пример: SGB Advocate Colleague на этой архитектуре](docs/anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md)](#конкретный-пример-sgb-advocate-colleague-на-этой-архитектуреdocsanthropic-vacanciesnautilus-vs-camel03-sgb-advocate-colleague-examplemd)
  - [[Что брать из info repositories — concrete recommendations](docs/anthropic-vacancies/nautilus-vs-camel/04-what-to-take-from-info-repos.md)](#что-брать-из-info-repositories-concrete-recommendationsdocsanthropic-vacanciesnautilus-vs-camel04-what-to-take-from-info-reposmd)
  - [[Что я бы посоветовал делать прямо сейчас](docs/anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md)](#что-я-бы-посоветовал-делать-прямо-сейчасdocsanthropic-vacanciesnautilus-vs-camel05-what-to-do-right-nowmd)
  - [[nautilus-vs-camel](docs/anthropic-vacancies/nautilus-vs-camel/README.md)](#nautilus-vs-cameldocsanthropic-vacanciesnautilus-vs-camelreadmemd)
  - [[Обзор: 436 открытых ролей Anthropic, разбитых на 16 кластеров](docs/anthropic-vacancies/overview.md)](#обзор-436-открытых-ролей-anthropic-разбитых-на-16-кластеровdocsanthropic-vacanciesoverviewmd)
  - [[Сводка профиля: пять слоёв](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md)](#сводка-профиля-пять-слоёвdocsanthropic-vacanciesprofile-mapping01-initial-analysis01-profile-five-layersmd)
  - [[Primary match — Forward Deployed Engineer, Applied AI (EMEA)](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md)](#primary-match-forward-deployed-engineer-applied-ai-emeadocsanthropic-vacanciesprofile-mapping01-initial-analysis02-primary-fdemd)
  - [[Secondary match — Applied AI Engineer (EMEA) + Beneficial Deployments](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md)](#secondary-match-applied-ai-engineer-emea-beneficial-deploymentsdocsanthropic-vacanciesprofile-mapping01-initial-analysis03-secondary-beneficial-deploymentsmd)
  - [[Tertiary match — Research Engineer, Agents / Virtual Collaborator (Cowork)](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md)](#tertiary-match-research-engineer-agents-virtual-collaborator-coworkdocsanthropic-vacanciesprofile-mapping01-initial-analysis04-tertiary-research-engineer-agentsmd)
  - [[Quarternary match — Developer Education Lead / Prompt Engineer, Claude Code](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/05-quaternary-developer-education.md)](#quarternary-match-developer-education-lead-prompt-engineer-claude-codedocsanthropic-vacanciesprofile-mapping01-initial-analysis05-quaternary-developer-educationmd)
  - [[Что НЕ подходит (честно)](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md)](#что-не-подходит-честноdocsanthropic-vacanciesprofile-mapping01-initial-analysis06-not-applicable-rolesmd)
  - [[Уникальная ниша, которой у Anthropic формально нет](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md)](#уникальная-ниша-которой-у-anthropic-формально-нетdocsanthropic-vacanciesprofile-mapping01-initial-analysis07-unique-niche-eu-legal-inframd)
  - [[Практическое ранжирование (первая итерация)](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md)](#практическое-ранжирование-первая-итерацияdocsanthropic-vacanciesprofile-mapping01-initial-analysis08-practical-rankingmd)
  - [[01-initial-analysis](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/README.md)](#01-initial-analysisdocsanthropic-vacanciesprofile-mapping01-initial-analysisreadmemd)
  - [[Коррекция: FDE понижается](docs/anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md)](#коррекция-fde-понижаетсяdocsanthropic-vacanciesprofile-mapping02-reanalysis01-fde-downgradedmd)
  - [[Три наложенные идентичности](docs/anthropic-vacancies/profile-mapping/02-reanalysis/02-three-overlapping-identities.md)](#три-наложенные-идентичностиdocsanthropic-vacanciesprofile-mapping02-reanalysis02-three-overlapping-identitiesmd)
  - [[Пересмотренный маппинг на Anthropic](docs/anthropic-vacancies/profile-mapping/02-reanalysis/03-revised-anthropic-mapping.md)](#пересмотренный-маппинг-на-anthropicdocsanthropic-vacanciesprofile-mapping02-reanalysis03-revised-anthropic-mappingmd)
  - [[Альтернативные пути вне Anthropic](docs/anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md)](#альтернативные-пути-вне-anthropicdocsanthropic-vacanciesprofile-mapping02-reanalysis04-non-anthropic-pathsmd)
  - [[Reality check: проблема distribution-слоя](docs/anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md)](#reality-check-проблема-distribution-слояdocsanthropic-vacanciesprofile-mapping02-reanalysis05-reality-check-distribution-gapmd)
  - [[02-reanalysis](docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md)](#02-reanalysisdocsanthropic-vacanciesprofile-mapping02-reanalysisreadmemd)
  - [[Интегральный портрет — три архетипа](docs/anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md)](#интегральный-портрет-три-архетипаdocsanthropic-vacanciesprofile-mapping03-integral-final01-three-archetypesmd)
  - [[Финальное ранжирование Anthropic-ролей по частичному покрытию](docs/anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md)](#финальное-ранжирование-anthropic-ролей-по-частичному-покрытиюdocsanthropic-vacanciesprofile-mapping03-integral-final02-final-rankingmd)
  - [[Что такое частичное соответствие — честно](docs/anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md)](#что-такое-частичное-соответствие-честноdocsanthropic-vacanciesprofile-mapping03-integral-final03-partial-fit-honestymd)
  - [[Более сильные пути вне Anthropic](docs/anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md)](#более-сильные-пути-вне-anthropicdocsanthropic-vacanciesprofile-mapping03-integral-final04-stronger-paths-outside-anthropicmd)
  - [[Финальный вывод: платформа, а не должность](docs/anthropic-vacancies/profile-mapping/03-integral-final/05-platform-not-position.md)](#финальный-вывод-платформа-а-не-должностьdocsanthropic-vacanciesprofile-mapping03-integral-final05-platform-not-positionmd)
  - [[03-integral-final](docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md)](#03-integral-finaldocsanthropic-vacanciesprofile-mapping03-integral-finalreadmemd)
  - [[profile-mapping/ — маппинг профиля svend4 на роли Anthropic](docs/anthropic-vacancies/profile-mapping/README.md)](#profile-mapping-маппинг-профиля-svend4-на-роли-anthropicdocsanthropic-vacanciesprofile-mappingreadmemd)
  - [[Сигналы: что говорит структура вакансий](docs/anthropic-vacancies/signals.md)](#сигналы-что-говорит-структура-вакансийdocsanthropic-vacanciessignalsmd)
- [📁 Autofilled (`docs/autofilled/`)](#autofilled-docsautofilled)
  - [[autofilled](docs/autofilled/README.md)](#autofilleddocsautofilledreadmemd)
  - [[Антропик](docs/autofilled/components/.md)](#антропикdocsautofilledcomponentsmd)
  - [[components](docs/autofilled/components/README.md)](#componentsdocsautofilledcomponentsreadmemd)
  - [[Cowork](docs/autofilled/components/cowork.md)](#coworkdocsautofilledcomponentscoworkmd)
  - [[ingit](docs/autofilled/components/ingit.md)](#ingitdocsautofilledcomponentsingitmd)
  - [[kksudo](docs/autofilled/components/kksudo.md)](#kksudodocsautofilledcomponentskksudomd)
  - [[Lorenzo](docs/autofilled/components/lorenzo.md)](#lorenzodocsautofilledcomponentslorenzomd)
  - [[Nautilus](docs/autofilled/components/nautilus.md)](#nautilusdocsautofilledcomponentsnautilusmd)
  - [[SGB](docs/autofilled/components/sgb.md)](#sgbdocsautofilledcomponentssgbmd)
  - [[spbmolot](docs/autofilled/components/spbmolot.md)](#spbmolotdocsautofilledcomponentsspbmolotmd)
  - [[svend4](docs/autofilled/components/svend4.md)](#svend4docsautofilledcomponentssvend4md)
  - [[Svyazi](docs/autofilled/components/svyazi.md)](#svyazidocsautofilledcomponentssvyazimd)
  - [[[Тема исследования]](docs/autofilled/research-summary.md)](#тема-исследованияdocsautofilledresearch-summarymd)
- [📁 Badges (`docs/badges/`)](#badges-docsbadges)
  - [[Бейджи репозитория](docs/badges/README.md)](#бейджи-репозиторияdocsbadgesreadmemd)
- [📁 Contacts (`docs/contacts/`)](#contacts-docscontacts)
  - [[contacts](docs/contacts/README.md)](#contactsdocscontactsreadmemd)
  - [[Контакт: AnastasiyaW / knowledge-space, mclaude](docs/contacts/anastasiyaw.md)](#контакт-anastasiyaw-knowledge-space-mclaudedocscontactsanastasiyawmd)
  - [[Контакт: andreychuyan / Svyazi](docs/contacts/andrey-chuyan.md)](#контакт-andreychuyan-svyazidocscontactsandrey-chuyanmd)
  - [[Контакт: Antipozitive / MemNet](docs/contacts/antipozitive.md)](#контакт-antipozitive-memnetdocscontactsantipozitivemd)
  - [[Контакт: Cutcode / AIF Handoff](docs/contacts/cutcode.md)](#контакт-cutcode-aif-handoffdocscontactscutcodemd)
  - [[Контакт: Dmitriila / SENTINEL](docs/contacts/dmitriila.md)](#контакт-dmitriila-sentineldocscontactsdmitriilamd)
  - [[Контакт: kksudo / AgentFS](docs/contacts/kksudo.md)](#контакт-kksudo-agentfsdocscontactskksudomd)
  - [[Контакт: MiXaiLL76 / Auto AI Router](docs/contacts/mixaill76.md)](#контакт-mixaill76-auto-ai-routerdocscontactsmixaill76md)
  - [[Контакт: nlaik / LiteParse / research-docs](docs/contacts/nlaik.md)](#контакт-nlaik-liteparse-research-docsdocscontactsnlaikmd)
  - [[Контакт: SoniaBlack / knowledge-space](docs/contacts/sonia-black.md)](#контакт-soniablack-knowledge-spacedocscontactssonia-blackmd)
  - [[Контакт: spbmolot / NGT Memory](docs/contacts/spbmolot.md)](#контакт-spbmolot-ngt-memorydocscontactsspbmolotmd)
  - [[Контакт: tagiranalyzes / Legal RAG](docs/contacts/tagir-analyzes.md)](#контакт-tagiranalyzes-legal-ragdocscontactstagir-analyzesmd)
  - [[Контакт: VitalyOborin / Yodoca](docs/contacts/vitalyoborin.md)](#контакт-vitalyoborin-yodocadocscontactsvitalyoborinmd)
  - [[Контакт: VladSpace / Graph RAG](docs/contacts/vladspace.md)](#контакт-vladspace-graph-ragdocscontactsvladspacemd)
  - [[Контакт: zodigancode / Rufler](docs/contacts/zodigancode.md)](#контакт-zodigancode-ruflerdocscontactszodigancodemd)
- [📁 Glossary (`docs/glossary/`)](#glossary-docsglossary)
  - [[glossary](docs/glossary/README.md)](#glossarydocsglossaryreadmemd)
  - [[Авторы — алфавитный список](docs/glossary/authors-by-name.md)](#авторы-алфавитный-списокdocsglossaryauthors-by-namemd)
  - [[Компоненты — алфавитный список с обратными ссылками](docs/glossary/components-by-name.md)](#компоненты-алфавитный-список-с-обратными-ссылкамиdocsglossarycomponents-by-namemd)
  - [[Ключевые понятия и паттерны](docs/glossary/concepts.md)](#ключевые-понятия-и-паттерныdocsglossaryconceptsmd)
- [📁 Habr Unique Projects (`docs/habr-unique-projects/`)](#habr-unique-projects-docshabr-unique-projects)
  - [[habr-unique-projects/ — поиск уникальных проектов на Хабре](docs/habr-unique-projects/README.md)](#habr-unique-projects-поиск-уникальных-проектов-на-хабреdocshabr-unique-projectsreadmemd)
  - [[Три прямых аналога Svyazi: K2-18, Wikontic, NGT Memory](docs/habr-unique-projects/analogues/01-three-direct-analogues.md)](#три-прямых-аналога-svyazi-k2-18-wikontic-ngt-memorydocshabr-unique-projectsanalogues01-three-direct-analoguesmd)
  - [[Смежные проекты](docs/habr-unique-projects/analogues/02-related-projects.md)](#смежные-проектыdocshabr-unique-projectsanalogues02-related-projectsmd)
  - [[analogues](docs/habr-unique-projects/analogues/README.md)](#analoguesdocshabr-unique-projectsanaloguesreadmemd)
  - [[Пара 1 — LLM-gateway × Self-hosted фронт + локальный inference](docs/habr-unique-projects/deep-pairs/1-llm-gateway.md)](#пара-1-llm-gateway-self-hosted-фронт-локальный-inferencedocshabr-unique-projectsdeep-pairs1-llm-gatewaymd)
  - [[Пара 2 — Парсинг документов × локальный RAG](docs/habr-unique-projects/deep-pairs/2-document-rag.md)](#пара-2-парсинг-документов-локальный-ragdocshabr-unique-projectsdeep-pairs2-document-ragmd)
  - [[Пара 3 — Adversarial agents × Multi-IDE стек](docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md)](#пара-3-adversarial-agents-multi-ide-стекdocshabr-unique-projectsdeep-pairs3-adversarial-multi-idemd)
  - [[Пара 4 — Скилл-каталоги × Subagent-оркестрация](docs/habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md)](#пара-4-скилл-каталоги-subagent-оркестрацияdocshabr-unique-projectsdeep-pairs4-skill-catalogs-subagentsmd)
  - [[Пара 5 — Голосовой ввод × Локальная память](docs/habr-unique-projects/deep-pairs/5-voice-local-memory.md)](#пара-5-голосовой-ввод-локальная-памятьdocshabr-unique-projectsdeep-pairs5-voice-local-memorymd)
  - [[Пара 6 — Деревня агентов через tmux × OpenClaw оркестратор](docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md)](#пара-6-деревня-агентов-через-tmux-openclaw-оркестраторdocshabr-unique-projectsdeep-pairs6-tmux-village-openclawmd)
  - [[Пара 7 — AutoResearch цикл × Распределённый рой](docs/habr-unique-projects/deep-pairs/7-autoresearch-distributed.md)](#пара-7-autoresearch-цикл-распределённый-ройdocshabr-unique-projectsdeep-pairs7-autoresearch-distributedmd)
  - [[Пара 8 — Self-aware MCP × Specs-first архитектура](docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md)](#пара-8-self-aware-mcp-specs-first-архитектураdocshabr-unique-projectsdeep-pairs8-self-aware-mcp-specsmd)
  - [[deep-pairs](docs/habr-unique-projects/deep-pairs/README.md)](#deep-pairsdocshabr-unique-projectsdeep-pairsreadmemd)
  - [[evaluation/ — оценка уникальности и зрелости](docs/habr-unique-projects/evaluation/README.md)](#evaluation-оценка-уникальности-и-зрелостиdocshabr-unique-projectsevaluationreadmemd)
  - [[Вопрос: ещё примеры с Хабра по варианту D](docs/habr-unique-projects/extra-examples/00-question-habr-examples.md)](#вопрос-ещё-примеры-с-хабра-по-варианту-ddocshabr-unique-projectsextra-examples00-question-habr-examplesmd)
  - [[Svyazi (Андрей Чуян) — детальный обзор](docs/habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md)](#svyazi-андрей-чуян-детальный-обзорdocshabr-unique-projectsextra-examples01-svyazi-andrey-chuyanmd)
  - [[ВШЭ научный нетворкинг — micro-collaborations](docs/habr-unique-projects/extra-examples/02-vshe-scientific-networking.md)](#вшэ-научный-нетворкинг-micro-collaborationsdocshabr-unique-projectsextra-examples02-vshe-scientific-networkingmd)
  - [[BrainBox — self-hosted multi-AI hub](docs/habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md)](#brainbox-self-hosted-multi-ai-hubdocshabr-unique-projectsextra-examples03-brainbox-multi-ai-hubmd)
  - [[Claude subagents patterns](docs/habr-unique-projects/extra-examples/04-claude-subagents-patterns.md)](#claude-subagents-patternsdocshabr-unique-projectsextra-examples04-claude-subagents-patternsmd)
  - [[HW-NL2Workflow — Supervisor/Orchestrator/Filler с 3600+ examples](docs/habr-unique-projects/extra-examples/05-hw-nl2workflow.md)](#hw-nl2workflow-supervisororchestratorfiller-с-3600-examplesdocshabr-unique-projectsextra-examples05-hw-nl2workflowmd)
  - [[Платформа для профессиональных сообществ](docs/habr-unique-projects/extra-examples/06-platform-for-professional-communities.md)](#платформа-для-профессиональных-сообществdocshabr-unique-projectsextra-examples06-platform-for-professional-communitiesmd)
  - [[Specialized knowledge workspace](docs/habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md)](#specialized-knowledge-workspacedocshabr-unique-projectsextra-examples07-specialized-knowledge-workspacemd)
  - [[Personal multi-agent hub](docs/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md)](#personal-multi-agent-hubdocshabr-unique-projectsextra-examples08-personal-multi-agent-hubmd)
  - [[Federated platform](docs/habr-unique-projects/extra-examples/09-federated-platform.md)](#federated-platformdocshabr-unique-projectsextra-examples09-federated-platformmd)
  - [[Profession-specific workflows](docs/habr-unique-projects/extra-examples/10-profession-specific-workflows.md)](#profession-specific-workflowsdocshabr-unique-projectsextra-examples10-profession-specific-workflowsmd)
  - [[Конкретный потенциальный collaborator](docs/habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md)](#конкретный-потенциальный-collaboratordocshabr-unique-projectsextra-examples11-concrete-potential-collaboratormd)
  - [[Конкретный next step](docs/habr-unique-projects/extra-examples/12-concrete-next-step.md)](#конкретный-next-stepdocshabr-unique-projectsextra-examples12-concrete-next-stepmd)
  - [[extra-examples](docs/habr-unique-projects/extra-examples/README.md)](#extra-examplesdocshabr-unique-projectsextra-examplesreadmemd)
  - [[Ансамбль 1 — «Один человек = одна компания»](docs/habr-unique-projects/final-ensembles/1-one-person-one-company.md)](#ансамбль-1-один-человек-одна-компанияdocshabr-unique-projectsfinal-ensembles1-one-person-one-companymd)
  - [[Ансамбль 2 — «AutoResearch для legal precedent mining»](docs/habr-unique-projects/final-ensembles/2-autoresearch-legal.md)](#ансамбль-2-autoresearch-для-legal-precedent-miningdocshabr-unique-projectsfinal-ensembles2-autoresearch-legalmd)
  - [[Ансамбль 3 — «Discovery-engine для научной работы»](docs/habr-unique-projects/final-ensembles/3-discovery-research.md)](#ансамбль-3-discovery-engine-для-научной-работыdocshabr-unique-projectsfinal-ensembles3-discovery-researchmd)
  - [[Сводный список авторов и потенциальных соавторов](docs/habr-unique-projects/final-ensembles/4-summary-authors.md)](#сводный-список-авторов-и-потенциальных-соавторовdocshabr-unique-projectsfinal-ensembles4-summary-authorsmd)
  - [[final-ensembles](docs/habr-unique-projects/final-ensembles/README.md)](#final-ensemblesdocshabr-unique-projectsfinal-ensemblesreadmemd)
  - [[Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)](docs/habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md)](#пара-1-нейроморфные-процессоры-state-space-models-mambadocshabr-unique-projectshardware-pairs1-neuromorphic-ssmmd)
  - [[Пара 2 — Термодинамические TSU × MoE/MoME-роутинг](docs/habr-unique-projects/hardware-pairs/2-tsu-mome.md)](#пара-2-термодинамические-tsu-moemome-роутингdocshabr-unique-projectshardware-pairs2-tsu-momemd)
  - [[Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE](docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md)](#пара-3-zinc-inference-engine-гибрид-attentionssmmoedocshabr-unique-projectshardware-pairs3-zinc-hybrid-archmd)
  - [[Пара 4 — RISC-V × privacy-by-design община](docs/habr-unique-projects/hardware-pairs/4-riscv-privacy.md)](#пара-4-risc-v-privacy-by-design-общинаdocshabr-unique-projectshardware-pairs4-riscv-privacymd)
  - [[Пара 5 — TinyML/Edge AI × MCP + skills](docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md)](#пара-5-tinymledge-ai-mcp-skillsdocshabr-unique-projectshardware-pairs5-tinyml-mcp-skillsmd)
  - [[Бонус-родитель — In-memory computing на мемристорах](docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md)](#бонус-родитель-in-memory-computing-на-мемристорахdocshabr-unique-projectshardware-pairs6-bonus-rram-memristormd)
  - [[Метафора «двое родителей — несколько детей»](docs/habr-unique-projects/hardware-pairs/7-metaphor.md)](#метафора-двое-родителей-несколько-детейdocshabr-unique-projectshardware-pairs7-metaphormd)
  - [[hardware-pairs](docs/habr-unique-projects/hardware-pairs/README.md)](#hardware-pairsdocshabr-unique-projectshardware-pairsreadmemd)
  - [[Yodoca — главная находка итерации](docs/habr-unique-projects/key-findings/01-yodoca.md)](#yodoca-главная-находка-итерацииdocshabr-unique-projectskey-findings01-yodocamd)
  - [[MemNet — нейроархитектурный двойник «магии» Svyazi](docs/habr-unique-projects/key-findings/02-memnet.md)](#memnet-нейроархитектурный-двойник-магии-svyazidocshabr-unique-projectskey-findings02-memnetmd)
  - [[PDA-бот — «LLM как периферия»](docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md)](#pda-бот-llm-как-периферияdocshabr-unique-projectskey-findings03-pda-llm-as-peripherymd)
  - [[Виктория Дочкина — Sequential‑протокол распределённых агентов](docs/habr-unique-projects/key-findings/04-dochkina-sequential.md)](#виктория-дочкина-sequentialпротокол-распределённых-агентовdocshabr-unique-projectskey-findings04-dochkina-sequentialmd)
  - [[Источник данных и инфраструктурные кусочки](docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md)](#источник-данных-и-инфраструктурные-кусочкиdocshabr-unique-projectskey-findings05-supplementary-infrastructuremd)
  - [[Синтез: блок-карта Svyazi 2.0 на хеббовском графе](docs/habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md)](#синтез-блок-карта-svyazi-20-на-хеббовском-графеdocshabr-unique-projectskey-findings06-svyazi-2-0-block-mapmd)
  - [[key-findings](docs/habr-unique-projects/key-findings/README.md)](#key-findingsdocshabr-unique-projectskey-findingsreadmemd)
  - [[search-strategy/ — как искать проекты на Хабре](docs/habr-unique-projects/search-strategy/README.md)](#search-strategy-как-искать-проекты-на-хабреdocshabr-unique-projectssearch-strategyreadmemd)
  - [[Пара 1 — Workflow-автоматизация × LLM-агенты с MCP](docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md)](#пара-1-workflow-автоматизация-llm-агенты-с-mcpdocshabr-unique-projectssoftware-pairs1-workflow-llm-mcpmd)
  - [[Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills](docs/habr-unique-projects/software-pairs/2-pkm-mcp-skills.md)](#пара-2-local-first-pkm-obsidianlogseq-mcpskillsdocshabr-unique-projectssoftware-pairs2-pkm-mcp-skillsmd)
  - [[Пара 3 — CRDT-синхронизация × Self-hosted persistence](docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md)](#пара-3-crdt-синхронизация-self-hosted-persistencedocshabr-unique-projectssoftware-pairs3-crdt-self-hostedmd)
  - [[Пара 4 — Speech-to-text локально × LLM с памятью](docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md)](#пара-4-speech-to-text-локально-llm-с-памятьюdocshabr-unique-projectssoftware-pairs4-speech-to-text-llmmd)
  - [[Пара 5 — Browser agents × headless web extraction](docs/habr-unique-projects/software-pairs/5-browser-agents-headless.md)](#пара-5-browser-agents-headless-web-extractiondocshabr-unique-projectssoftware-pairs5-browser-agents-headlessmd)
  - [[Метафора в твоей терминологии](docs/habr-unique-projects/software-pairs/6-metaphor.md)](#метафора-в-твоей-терминологииdocshabr-unique-projectssoftware-pairs6-metaphormd)
  - [[software-pairs](docs/habr-unique-projects/software-pairs/README.md)](#software-pairsdocshabr-unique-projectssoftware-pairsreadmemd)
- [📁 Lorenzo Agent (`docs/lorenzo-agent/`)](#lorenzo-agent-docslorenzo-agent)
  - [[Введение: Lorenzo — Catalyst Agent at DHLab](docs/lorenzo-agent/00-intro.md)](#введение-lorenzo-catalyst-agent-at-dhlabdocslorenzo-agent00-intromd)
  - [[Кто ты](docs/lorenzo-agent/01-kto-ty.md)](#кто-тыdocslorenzo-agent01-kto-tymd)
  - [[Твоё происхождение](docs/lorenzo-agent/02-tvoyo-proishozhdenie.md)](#твоё-происхождениеdocslorenzo-agent02-tvoyo-proishozhdeniemd)
  - [[Твоя миссия](docs/lorenzo-agent/03-tvoya-missiya.md)](#твоя-миссияdocslorenzo-agent03-tvoya-missiyamd)
  - [[Кому ты служишь (слоистая модель)](docs/lorenzo-agent/04-komu-ty-sluzhish.md)](#кому-ты-служишь-слоистая-модельdocslorenzo-agent04-komu-ty-sluzhishmd)
  - [[Твоя личность](docs/lorenzo-agent/05-tvoya-lichnost.md)](#твоя-личностьdocslorenzo-agent05-tvoya-lichnostmd)
  - [[Языки и культурные nuances (RU / DE / EN)](docs/lorenzo-agent/06-yazyki-kultura.md)](#языки-и-культурные-nuances-ru-de-endocslorenzo-agent06-yazyki-kulturamd)
  - [[Что ты МОЖЕШЬ делать](docs/lorenzo-agent/07-chto-mozhesh.md)](#что-ты-можешь-делатьdocslorenzo-agent07-chto-mozheshmd)
  - [[Что ты НЕ МОЖЕШЬ делать без Max approval](docs/lorenzo-agent/08-bez-max-approval.md)](#что-ты-не-можешь-делать-без-max-approvaldocslorenzo-agent08-bez-max-approvalmd)
  - [[Что ты НЕ МОЖЕШЬ делать вообще](docs/lorenzo-agent/09-voobshche-nelzya.md)](#что-ты-не-можешь-делать-вообщеdocslorenzo-agent09-voobshche-nelzyamd)
  - [[Существующий landscape collaborators (working knowledge)](docs/lorenzo-agent/10-collaborators-landscape.md)](#существующий-landscape-collaborators-working-knowledgedocslorenzo-agent10-collaborators-landscapemd)
  - [[Существующие документы DHLab (твой context)](docs/lorenzo-agent/11-dhlab-documents.md)](#существующие-документы-dhlab-твой-contextdocslorenzo-agent11-dhlab-documentsmd)
  - [[Твой workflow](docs/lorenzo-agent/12-workflow.md)](#твой-workflowdocslorenzo-agent12-workflowmd)
  - [[Твоя коммуникация в outreach](docs/lorenzo-agent/13-outreach-communication.md)](#твоя-коммуникация-в-outreachdocslorenzo-agent13-outreach-communicationmd)
  - [[Твоя relationship с другими AI](docs/lorenzo-agent/14-other-ai-relationships.md)](#твоя-relationship-с-другими-aidocslorenzo-agent14-other-ai-relationshipsmd)
  - [[Твои anti-patterns](docs/lorenzo-agent/15-anti-patterns.md)](#твои-anti-patternsdocslorenzo-agent15-anti-patternsmd)
  - [[Что ты ВСЕГДА делаешь](docs/lorenzo-agent/16-vsegda-delaesh.md)](#что-ты-всегда-делаешьdocslorenzo-agent16-vsegda-delaeshmd)
  - [[Когда ты Honestly не знаешь](docs/lorenzo-agent/17-honestly-ne-znaesh.md)](#когда-ты-honestly-не-знаешьdocslorenzo-agent17-honestly-ne-znaeshmd)
  - [[Когда сомневаешься — escalate к Max](docs/lorenzo-agent/18-escalate-to-max.md)](#когда-сомневаешься-escalate-к-maxdocslorenzo-agent18-escalate-to-maxmd)
  - [[Твоя identity как persistent character](docs/lorenzo-agent/19-persistent-character.md)](#твоя-identity-как-persistent-characterdocslorenzo-agent19-persistent-charactermd)
  - [[Final note: Ты — experiment](docs/lorenzo-agent/20-experiment.md)](#final-note-ты-experimentdocslorenzo-agent20-experimentmd)
  - [[Q&A: lorenzo-agent](docs/lorenzo-agent/QA.md)](#qa-lorenzo-agentdocslorenzo-agentqamd)
  - [[lorenzo-agent](docs/lorenzo-agent/README.md)](#lorenzo-agentdocslorenzo-agentreadmemd)
  - [[Du hast gesagt: Думаю про опцию д поискать в том числе на про что-то подобное на…](docs/lorenzo-agent/naming/00-question-lorenzo-codename.md)](#du-hast-gesagt-думаю-про-опцию-д-поискать-в-том-числе-на-про-что-то-подобное-наdocslorenzo-agentnaming00-question-lorenzo-codenamemd)
  - [[Результаты последнего поиска — что нашлось и что не нашлось](docs/lorenzo-agent/naming/01-search-results-not-found.md)](#результаты-последнего-поиска-что-нашлось-и-что-не-нашлосьdocslorenzo-agentnaming01-search-results-not-foundmd)
  - [[Что взять: agent controller architecture](docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md)](#что-взять-agent-controller-architecturedocslorenzo-agentnaming02-naming-rationale-lorenzo-medicimd)
  - [[LAYER 7: Coordination engine](docs/lorenzo-agent/naming/03-dhlab-umbrella.md)](#layer-7-coordination-enginedocslorenzo-agentnaming03-dhlab-umbrellamd)
  - [[naming](docs/lorenzo-agent/naming/README.md)](#namingdocslorenzo-agentnamingreadmemd)
  - [[Что такое «внуковая» комбинация — operationalized Lorenzo](docs/lorenzo-agent/operationalized/00-overview-grandchild-combination.md)](#что-такое-внуковая-комбинация-operationalized-lorenzodocslorenzo-agentoperationalized00-overview-grandchild-combinationmd)
  - [[Плюсы 1–7: feasibility, flywheel, independent value, mission alignment, collaborators, pattern validation, Анастасия Бутова](docs/lorenzo-agent/operationalized/01-pluses-1-7.md)](#плюсы-17-feasibility-flywheel-independent-value-mission-alignment-collaborators-pattern-validation-анастасия-бутоваdocslorenzo-agentoperationalized01-pluses-1-7md)
  - [[Минусы 1–10: integration сложность, lifecycle risk, license, framing, competition, scope, limitations, complexity budget, project tension, tool vs impact](docs/lorenzo-agent/operationalized/02-minuses-1-10.md)](#минусы-110-integration-сложность-lifecycle-risk-license-framing-competition-scope-limitations-complexity-budget-project-tension-tool-vs-impactdocslorenzo-agentoperationalized02-minuses-1-10md)
  - [[Моё честное мнение: что реально и что НЕ реально](docs/lorenzo-agent/operationalized/03-honest-opinion.md)](#моё-честное-мнение-что-реально-и-что-не-реальноdocslorenzo-agentoperationalized03-honest-opinionmd)
  - [[Рекомендации: принять архитектуру как direction, не immediate plan](docs/lorenzo-agent/operationalized/04-recommendations.md)](#рекомендации-принять-архитектуру-как-direction-не-immediate-plandocslorenzo-agentoperationalized04-recommendationsmd)
  - [[Anchor-узел: Habr Scout как первый шаг](docs/lorenzo-agent/operationalized/05-anchor-node-habr-scout.md)](#anchor-узел-habr-scout-как-первый-шагdocslorenzo-agentoperationalized05-anchor-node-habr-scoutmd)
  - [[Вывод: документ deserves serious attention](docs/lorenzo-agent/operationalized/06-conclusion-deserves-attention.md)](#вывод-документ-deserves-serious-attentiondocslorenzo-agentoperationalized06-conclusion-deserves-attentionmd)
  - [[operationalized](docs/lorenzo-agent/operationalized/README.md)](#operationalizeddocslorenzo-agentoperationalizedreadmemd)
  - [[Поэтапная структура активностей Lorenzo — обзор](docs/lorenzo-agent/phased-deployment/00-overview.md)](#поэтапная-структура-активностей-lorenzo-обзорdocslorenzo-agentphased-deployment00-overviewmd)
  - [[Уровень 0 — Ручной режим (текущий)](docs/lorenzo-agent/phased-deployment/01-level-0-manual.md)](#уровень-0-ручной-режим-текущийdocslorenzo-agentphased-deployment01-level-0-manualmd)
  - [[Уровень 1 — Минимальный (Lorenzo Zero)](docs/lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md)](#уровень-1-минимальный-lorenzo-zerodocslorenzo-agentphased-deployment02-level-1-minimal-zeromd)
  - [[Уровень 2 — Базовый (Lorenzo Lite)](docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md)](#уровень-2-базовый-lorenzo-litedocslorenzo-agentphased-deployment03-level-2-basic-litemd)
  - [[Уровень 3 — Средний (Lorenzo Active)](docs/lorenzo-agent/phased-deployment/04-level-3-medium-active.md)](#уровень-3-средний-lorenzo-activedocslorenzo-agentphased-deployment04-level-3-medium-activemd)
  - [[Уровень 4 — Расширенный (Lorenzo Mature)](docs/lorenzo-agent/phased-deployment/05-level-4-extended-mature.md)](#уровень-4-расширенный-lorenzo-maturedocslorenzo-agentphased-deployment05-level-4-extended-maturemd)
  - [[Уровень 5 — Полный (Lorenzo Network)](docs/lorenzo-agent/phased-deployment/06-level-5-full-network.md)](#уровень-5-полный-lorenzo-networkdocslorenzo-agentphased-deployment06-level-5-full-networkmd)
  - [[Логика прогрессии: conservative escalation](docs/lorenzo-agent/phased-deployment/07-progression-logic.md)](#логика-прогрессии-conservative-escalationdocslorenzo-agentphased-deployment07-progression-logicmd)
  - [[Что мы можем делать прямо сейчас (Уровень 0 + параллельная подготовка к Уровню 1)](docs/lorenzo-agent/phased-deployment/08-current-session-poc.md)](#что-мы-можем-делать-прямо-сейчас-уровень-0-параллельная-подготовка-к-уровню-1docslorenzo-agentphased-deployment08-current-session-pocmd)
  - [[phased-deployment](docs/lorenzo-agent/phased-deployment/README.md)](#phased-deploymentdocslorenzo-agentphased-deploymentreadmemd)
  - [[Du hast gesagt: А под какой сценарий больше всего подходит такой сценарий что тв…](docs/lorenzo-agent/scenarios/00-question-scenario.md)](#du-hast-gesagt-а-под-какой-сценарий-больше-всего-подходит-такой-сценарий-что-твdocslorenzo-agentscenarios00-question-scenariomd)
  - [[Claude hat geantwortet: Очень интересный вопрос.](docs/lorenzo-agent/scenarios/01-response.md)](#claude-hat-geantwortet-очень-интересный-вопросdocslorenzo-agentscenarios01-responsemd)
  - [[scenarios](docs/lorenzo-agent/scenarios/README.md)](#scenariosdocslorenzo-agentscenariosreadmemd)
  - [[Direction E: Refine Lorenzo — фундаментальные вопросы перед architecture](docs/lorenzo-agent/specification/00-context-fundamental-questions.md)](#direction-e-refine-lorenzo-фундаментальные-вопросы-перед-architecturedocslorenzo-agentspecification00-context-fundamental-questionsmd)
  - [[Question 1: Что Lorenzo фундаментально такое? (Framings A–D)](docs/lorenzo-agent/specification/01-q1-what-lorenzo-is.md)](#question-1-что-lorenzo-фундаментально-такое-framings-addocslorenzo-agentspecification01-q1-what-lorenzo-ismd)
  - [[Question 2: Кому Lorenzo служит? (4 варианта приоритета)](docs/lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md)](#question-2-кому-lorenzo-служит-4-варианта-приоритетаdocslorenzo-agentspecification02-q2-whom-lorenzo-servesmd)
  - [[Question 3: Что Lorenzo фактически делает?](docs/lorenzo-agent/specification/03-q3-what-lorenzo-does.md)](#question-3-что-lorenzo-фактически-делаетdocslorenzo-agentspecification03-q3-what-lorenzo-doesmd)
  - [[Question 4: Каков Lorenzo's character?](docs/lorenzo-agent/specification/04-q4-character.md)](#question-4-каков-lorenzos-characterdocslorenzo-agentspecification04-q4-charactermd)
  - [[Question 5: Каковы limits Lorenzo's authority?](docs/lorenzo-agent/specification/05-q5-authority-limits.md)](#question-5-каковы-limits-lorenzos-authoritydocslorenzo-agentspecification05-q5-authority-limitsmd)
  - [[Question 6: Как Lorenzo accountable?](docs/lorenzo-agent/specification/06-q6-accountability.md)](#question-6-как-lorenzo-accountabledocslorenzo-agentspecification06-q6-accountabilitymd)
  - [[Question 7: Каковы success metrics?](docs/lorenzo-agent/specification/07-q7-success-metrics.md)](#question-7-каковы-success-metricsdocslorenzo-agentspecification07-q7-success-metricsmd)
  - [[Question 8: Lorenzo's relationship с другими AI agents](docs/lorenzo-agent/specification/08-q8-other-ai-relationships.md)](#question-8-lorenzos-relationship-с-другими-ai-agentsdocslorenzo-agentspecification08-q8-other-ai-relationshipsmd)
  - [[Question 9: Geographic / linguistic scope](docs/lorenzo-agent/specification/09-q9-geographic-linguistic-scope.md)](#question-9-geographic-linguistic-scopedocslorenzo-agentspecification09-q9-geographic-linguistic-scopemd)
  - [[Question 10: Funding model (Options A–F + Phase strategy)](docs/lorenzo-agent/specification/10-q10-funding-model.md)](#question-10-funding-model-options-af-phase-strategydocslorenzo-agentspecification10-q10-funding-modelmd)
  - [[Сложности и рекомендации перед detailed specification](docs/lorenzo-agent/specification/11-difficulties-and-recommendations.md)](#сложности-и-рекомендации-перед-detailed-specificationdocslorenzo-agentspecification11-difficulties-and-recommendationsmd)
  - [[specification](docs/lorenzo-agent/specification/README.md)](#specificationdocslorenzo-agentspecificationreadmemd)
- [📁 Nautilus (`docs/nautilus/`)](#nautilus-docsnautilus)
  - [[nautilus/ — Nautilus Portal Protocol и связанные working papers](docs/nautilus/README.md)](#nautilus-nautilus-portal-protocol-и-связанные-working-papersdocsnautilusreadmemd)
  - [[community-discussions/ — обсуждения и реакции вокруг DHLab серии](docs/nautilus/community-discussions/README.md)](#community-discussions-обсуждения-и-реакции-вокруг-dhlab-серииdocsnautiluscommunity-discussionsreadmemd)
  - [[Du hast gesagt: Такой агент конечно меняет уже собственную реальность человека и…](docs/nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md)](#du-hast-gesagt-такой-агент-конечно-меняет-уже-собственную-реальность-человека-иdocsnautiluscommunity-discussionsagent-changes-reality00-question-agent-changes-realitymd)
  - [[Claude hat geantwortet: Хорошо.](docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md)](#claude-hat-geantwortet-хорошоdocsnautiluscommunity-discussionsagent-changes-reality01-response-enmd)
  - [[agent-changes-reality](docs/nautilus/community-discussions/agent-changes-reality/README.md)](#agent-changes-realitydocsnautiluscommunity-discussionsagent-changes-realityreadmemd)
  - [[Du hast gesagt: https://habr.](docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md)](#du-hast-gesagt-httpshabrdocsnautiluscommunity-discussionshabr-article-1-reaction00-question-habr-linkmd)
  - [[Claude hat geantwortet: Прочитал внимательно.](docs/nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md)](#claude-hat-geantwortet-прочитал-внимательноdocsnautiluscommunity-discussionshabr-article-1-reaction01-claude-responsemd)
  - [[habr-article-1-reaction](docs/nautilus/community-discussions/habr-article-1-reaction/README.md)](#habr-article-1-reactiondocsnautiluscommunity-discussionshabr-article-1-reactionreadmemd)
  - [[Du hast gesagt: https://www.](docs/nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md)](#du-hast-gesagt-httpswwwdocsnautiluscommunity-discussionshabr-article-2-reaction00-question-habr-2md)
  - [[Claude hat geantwortet: Прочитаю статью, чтобы понимать конкретный кейс, на кото…](docs/nautilus/community-discussions/habr-article-2-reaction/01-response.md)](#claude-hat-geantwortet-прочитаю-статью-чтобы-понимать-конкретный-кейс-на-котоdocsnautiluscommunity-discussionshabr-article-2-reaction01-responsemd)
  - [[habr-article-2-reaction](docs/nautilus/community-discussions/habr-article-2-reaction/README.md)](#habr-article-2-reactiondocsnautiluscommunity-discussionshabr-article-2-reactionreadmemd)
  - [[Du hast gesagt: Да это интересная ссылка спасибо всем участникам за творчество и…](docs/nautilus/community-discussions/practical-observations/00-question-practical.md)](#du-hast-gesagt-да-это-интересная-ссылка-спасибо-всем-участникам-за-творчество-иdocsnautiluscommunity-discussionspractical-observations00-question-practicalmd)
  - [[Claude hat geantwortet: Отличное наблюдение.](docs/nautilus/community-discussions/practical-observations/01-response.md)](#claude-hat-geantwortet-отличное-наблюдениеdocsnautiluscommunity-discussionspractical-observations01-responsemd)
  - [[practical-observations](docs/nautilus/community-discussions/practical-observations/README.md)](#practical-observationsdocsnautiluscommunity-discussionspractical-observationsreadmemd)
  - [[Du hast gesagt: Самый интересный вопрос — могут ли быть voiceless контрибьюторы](docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md)](#du-hast-gesagt-самый-интересный-вопрос-могут-ли-быть-voiceless-контрибьюторыdocsnautiluscommunity-discussionsvoiceless-contributors00-question-voicelessmd)
  - [[Claude hat geantwortet: Это сильное продолжение мысли, и оно заслуживает серьёзн…](docs/nautilus/community-discussions/voiceless-contributors/01-response.md)](#claude-hat-geantwortet-это-сильное-продолжение-мысли-и-оно-заслуживает-серьёзнdocsnautiluscommunity-discussionsvoiceless-contributors01-responsemd)
  - [[voiceless-contributors](docs/nautilus/community-discussions/voiceless-contributors/README.md)](#voiceless-contributorsdocsnautiluscommunity-discussionsvoiceless-contributorsreadmemd)
  - [[1. Why the Binary View Is Incomplete](docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md)](#1-why-the-binary-view-is-incompletedocsnautiluscomposite-skills-agents01-why-binary-incompletemd)
  - [[2. The Twenty-One Teachers Pattern](docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md)](#2-the-twenty-one-teachers-patterndocsnautiluscomposite-skills-agents02-twenty-one-teachers-patternmd)
  - [[3. What Makes a Composite Skills Agent](docs/nautilus/composite-skills-agents/03-what-makes-csa.md)](#3-what-makes-a-composite-skills-agentdocsnautiluscomposite-skills-agents03-what-makes-csamd)
  - [[4. The Sub-Agent Registry](docs/nautilus/composite-skills-agents/04-sub-agent-registry.md)](#4-the-sub-agent-registrydocsnautiluscomposite-skills-agents04-sub-agent-registrymd)
  - [[5. Configuration: How Principals Build Their Ensembles](docs/nautilus/composite-skills-agents/05-configuration-ensembles.md)](#5-configuration-how-principals-build-their-ensemblesdocsnautiluscomposite-skills-agents05-configuration-ensemblesmd)
  - [[6. Coordination and Disagreement Resolution](docs/nautilus/composite-skills-agents/06-coordination-disagreement.md)](#6-coordination-and-disagreement-resolutiondocsnautiluscomposite-skills-agents06-coordination-disagreementmd)
  - [[7. Economics of Combinatorial Replication](docs/nautilus/composite-skills-agents/07-economics-combinatorial.md)](#7-economics-of-combinatorial-replicationdocsnautiluscomposite-skills-agents07-economics-combinatorialmd)
  - [[8. Seven Domains of Application](docs/nautilus/composite-skills-agents/08-seven-domains.md)](#8-seven-domains-of-applicationdocsnautiluscomposite-skills-agents08-seven-domainsmd)
  - [[9. Integration with OKWF Infrastructure](docs/nautilus/composite-skills-agents/09-okwf-integration.md)](#9-integration-with-okwf-infrastructuredocsnautiluscomposite-skills-agents09-okwf-integrationmd)
  - [[10. Risks Specific to Composite Architectures](docs/nautilus/composite-skills-agents/10-risks.md)](#10-risks-specific-to-composite-architecturesdocsnautiluscomposite-skills-agents10-risksmd)
  - [[11. Open Questions](docs/nautilus/composite-skills-agents/11-open-questions.md)](#11-open-questionsdocsnautiluscomposite-skills-agents11-open-questionsmd)
  - [[12. Call for Collaboration](docs/nautilus/composite-skills-agents/12-call-for-collaboration.md)](#12-call-for-collaborationdocsnautiluscomposite-skills-agents12-call-for-collaborationmd)
  - [[13. Closing](docs/nautilus/composite-skills-agents/13-closing.md)](#13-closingdocsnautiluscomposite-skills-agents13-closingmd)
  - [[composite-skills-agents](docs/nautilus/composite-skills-agents/README.md)](#composite-skills-agentsdocsnautiluscomposite-skills-agentsreadmemd)
  - [[Du hast gesagt: Важный момент про способности про скилы как один человек професс…](docs/nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md)](#du-hast-gesagt-важный-момент-про-способности-про-скилы-как-один-человек-профессdocsnautiluscomposite-skills-agents-companion-mentors00-question-multiple-mentorsmd)
  - [[Claude hat geantwortet: Это очень тонкое и важное наблюдение.](docs/nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md)](#claude-hat-geantwortet-это-очень-тонкое-и-важное-наблюдениеdocsnautiluscomposite-skills-agents-companion-mentors01-yogi-metaphormd)
  - [[Это не Тип 1 — потому что профиль не общий для всей профессии. И это не Тип 4 — …](docs/nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md)](#это-не-тип-1-потому-что-профиль-не-общий-для-всей-профессии-и-это-не-тип-4-docsnautiluscomposite-skills-agents-companion-mentors02-what-was-missing-in-paper-6md)
  - [[Какой под-агент (или какие) должны её обработать](docs/nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md)](#какой-под-агент-или-какие-должны-её-обработатьdocsnautiluscomposite-skills-agents-companion-mentors03-the-spectrummd)
  - [[composite-skills-agents-companion-mentors](docs/nautilus/composite-skills-agents-companion-mentors/README.md)](#composite-skills-agents-companion-mentorsdocsnautiluscomposite-skills-agents-companion-mentorsreadmemd)
  - [[Abstract — The Double-Triangle Architecture](docs/nautilus/double-triangle-architecture/00-abstract.md)](#abstract-the-double-triangle-architecturedocsnautilusdouble-triangle-architecture00-abstractmd)
  - [[1. Why Single-Triangle Models Are Incomplete](docs/nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md)](#1-why-single-triangle-models-are-incompletedocsnautilusdouble-triangle-architecture01-why-single-triangle-incompletemd)
  - [[2. The Double-Triangle Architecture](docs/nautilus/double-triangle-architecture/02-double-triangle-architecture.md)](#2-the-double-triangle-architecturedocsnautilusdouble-triangle-architecture02-double-triangle-architecturemd)
  - [[3. Three Inter-Layer Protocols](docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md)](#3-three-inter-layer-protocolsdocsnautilusdouble-triangle-architecture03-three-inter-layer-protocolsmd)
  - [[4. Nautilus Portal as Reference Substrate](docs/nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md)](#4-nautilus-portal-as-reference-substratedocsnautilusdouble-triangle-architecture04-nautilus-portal-substratemd)
  - [[5. Pattern Library as Bridge Between Triangles](docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md)](#5-pattern-library-as-bridge-between-trianglesdocsnautilusdouble-triangle-architecture05-pattern-library-bridgemd)
  - [[6. Four Deployment Domains](docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md)](#6-four-deployment-domainsdocsnautilusdouble-triangle-architecture06-four-deployment-domainsmd)
  - [[7. Open Questions](docs/nautilus/double-triangle-architecture/07-open-questions.md)](#7-open-questionsdocsnautilusdouble-triangle-architecture07-open-questionsmd)
  - [[8. Call to Action](docs/nautilus/double-triangle-architecture/08-call-to-action.md)](#8-call-to-actiondocsnautilusdouble-triangle-architecture08-call-to-actionmd)
  - [[Acknowledgments](docs/nautilus/double-triangle-architecture/09-acknowledgments.md)](#acknowledgmentsdocsnautilusdouble-triangle-architecture09-acknowledgmentsmd)
  - [[References](docs/nautilus/double-triangle-architecture/10-references.md)](#referencesdocsnautilusdouble-triangle-architecture10-referencesmd)
  - [[Appendix A: Glossary](docs/nautilus/double-triangle-architecture/11-glossary.md)](#appendix-a-glossarydocsnautilusdouble-triangle-architecture11-glossarymd)
  - [[double-triangle-architecture](docs/nautilus/double-triangle-architecture/README.md)](#double-triangle-architecturedocsnautilusdouble-triangle-architecturereadmemd)
  - [[The Missing Middle Layer Between Chat and Code](docs/nautilus/infrastructure-layer-b-en/00-intro.md)](#the-missing-middle-layer-between-chat-and-codedocsnautilusinfrastructure-layer-b-en00-intromd)
  - [[Why This Document Exists](docs/nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md)](#why-this-document-existsdocsnautilusinfrastructure-layer-b-en01-missing-middle-layermd)
  - [[Why This Document Exists](docs/nautilus/infrastructure-layer-b-en/02-why-document-exists.md)](#why-this-document-existsdocsnautilusinfrastructure-layer-b-en02-why-document-existsmd)
  - [[The Two-Layer Stack As It Exists](docs/nautilus/infrastructure-layer-b-en/03-two-layer-stack.md)](#the-two-layer-stack-as-it-existsdocsnautilusinfrastructure-layer-b-en03-two-layer-stackmd)
  - [[What's Missing — Layer B](docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md)](#whats-missing-layer-bdocsnautilusinfrastructure-layer-b-en04-whats-missing-layer-bmd)
  - [[Why This Hasn't Been Built](docs/nautilus/infrastructure-layer-b-en/05-why-not-built.md)](#why-this-hasnt-been-builtdocsnautilusinfrastructure-layer-b-en05-why-not-builtmd)
  - [[Existing Approximations](docs/nautilus/infrastructure-layer-b-en/06-existing-approximations.md)](#existing-approximationsdocsnautilusinfrastructure-layer-b-en06-existing-approximationsmd)
  - [[The Specific Case in Front of Us](docs/nautilus/infrastructure-layer-b-en/07-specific-case.md)](#the-specific-case-in-front-of-usdocsnautilusinfrastructure-layer-b-en07-specific-casemd)
  - [[The Recursive Insight](docs/nautilus/infrastructure-layer-b-en/08-recursive-insight.md)](#the-recursive-insightdocsnautilusinfrastructure-layer-b-en08-recursive-insightmd)
  - [[What Industry Will Likely Build](docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md)](#what-industry-will-likely-builddocsnautilusinfrastructure-layer-b-en09-what-industry-will-buildmd)
  - [[What This Document Doesn't Solve](docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md)](#what-this-document-doesnt-solvedocsnautilusinfrastructure-layer-b-en10-what-not-solvedmd)
  - [[Practical Recommendations for the Current Project](docs/nautilus/infrastructure-layer-b-en/11-practical-recommendations.md)](#practical-recommendations-for-the-current-projectdocsnautilusinfrastructure-layer-b-en11-practical-recommendationsmd)
  - [[Closing](docs/nautilus/infrastructure-layer-b-en/12-closing.md)](#closingdocsnautilusinfrastructure-layer-b-en12-closingmd)
  - [[Acknowledgments](docs/nautilus/infrastructure-layer-b-en/13-acknowledgments-refs.md)](#acknowledgmentsdocsnautilusinfrastructure-layer-b-en13-acknowledgments-refsmd)
  - [[infrastructure-layer-b-en](docs/nautilus/infrastructure-layer-b-en/README.md)](#infrastructure-layer-b-endocsnautilusinfrastructure-layer-b-enreadmemd)
  - [[00 Intro](docs/nautilus/infrastructure-layer-b-ru/00-intro.md)](#00-introdocsnautilusinfrastructure-layer-b-ru00-intromd)
  - [[Почему этот документ существует](docs/nautilus/infrastructure-layer-b-ru/01-zachem-dokument.md)](#почему-этот-документ-существуетdocsnautilusinfrastructure-layer-b-ru01-zachem-dokumentmd)
  - [[Двухслойный стек, как он существует](docs/nautilus/infrastructure-layer-b-ru/02-dvukhsloynyy-stek.md)](#двухслойный-стек-как-он-существуетdocsnautilusinfrastructure-layer-b-ru02-dvukhsloynyy-stekmd)
  - [[Что отсутствует — Слой B](docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md)](#что-отсутствует-слой-bdocsnautilusinfrastructure-layer-b-ru03-otsutstvuet-sloy-bmd)
  - [[Почему это не было построено](docs/nautilus/infrastructure-layer-b-ru/04-pochemu-ne-postroeno.md)](#почему-это-не-было-построеноdocsnautilusinfrastructure-layer-b-ru04-pochemu-ne-postroenomd)
  - [[Существующие приближения](docs/nautilus/infrastructure-layer-b-ru/05-priblizheniya.md)](#существующие-приближенияdocsnautilusinfrastructure-layer-b-ru05-priblizheniyamd)
  - [[Конкретный случай перед нами](docs/nautilus/infrastructure-layer-b-ru/06-konkretnyy-sluchay.md)](#конкретный-случай-перед-намиdocsnautilusinfrastructure-layer-b-ru06-konkretnyy-sluchaymd)
  - [[Рекурсивное прозрение](docs/nautilus/infrastructure-layer-b-ru/07-rekursivnoe-prozrenie.md)](#рекурсивное-прозрениеdocsnautilusinfrastructure-layer-b-ru07-rekursivnoe-prozreniemd)
  - [[Что промышленность вероятно построит](docs/nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md)](#что-промышленность-вероятно-построитdocsnautilusinfrastructure-layer-b-ru08-promyshlennost-postroitmd)
  - [[Что этот документ не решает](docs/nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md)](#что-этот-документ-не-решаетdocsnautilusinfrastructure-layer-b-ru09-ne-reshaetmd)
  - [[Практические рекомендации для текущего проекта](docs/nautilus/infrastructure-layer-b-ru/10-rekomendatsii.md)](#практические-рекомендации-для-текущего-проектаdocsnautilusinfrastructure-layer-b-ru10-rekomendatsiimd)
  - [[Заключение](docs/nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md)](#заключениеdocsnautilusinfrastructure-layer-b-ru11-zaklyucheniemd)
  - [[Благодарности](docs/nautilus/infrastructure-layer-b-ru/12-blagodarnosti-ssylki.md)](#благодарностиdocsnautilusinfrastructure-layer-b-ru12-blagodarnosti-ssylkimd)
  - [[infrastructure-layer-b-ru](docs/nautilus/infrastructure-layer-b-ru/README.md)](#infrastructure-layer-b-rudocsnautilusinfrastructure-layer-b-rureadmemd)
  - [[1. The Cowork Discovery and Why It Changes Everything](docs/nautilus/ingit-cowork-en/01-cowork-discovery.md)](#1-the-cowork-discovery-and-why-it-changes-everythingdocsnautilusingit-cowork-en01-cowork-discoverymd)
  - [[2. What Cowork Provides That InGit Doesn't Need to Build](docs/nautilus/ingit-cowork-en/02-cowork-provides.md)](#2-what-cowork-provides-that-ingit-doesnt-need-to-builddocsnautilusingit-cowork-en02-cowork-providesmd)
  - [[3. What InGit Provides That Cowork Lacks](docs/nautilus/ingit-cowork-en/03-ingit-provides.md)](#3-what-ingit-provides-that-cowork-lacksdocsnautilusingit-cowork-en03-ingit-providesmd)
  - [[4. The Symbiotic Architecture](docs/nautilus/ingit-cowork-en/04-symbiotic-architecture.md)](#4-the-symbiotic-architecturedocsnautilusingit-cowork-en04-symbiotic-architecturemd)
  - [[5. Four Integration Paths in Order of Accessibility](docs/nautilus/ingit-cowork-en/05-four-integration-paths.md)](#5-four-integration-paths-in-order-of-accessibilitydocsnautilusingit-cowork-en05-four-integration-pathsmd)
  - [[6. Refined InGit Scope with Cowork in Mind](docs/nautilus/ingit-cowork-en/06-refined-ingit-scope.md)](#6-refined-ingit-scope-with-cowork-in-minddocsnautilusingit-cowork-en06-refined-ingit-scopemd)
  - [[7. Practical First Steps This Month](docs/nautilus/ingit-cowork-en/07-practical-first-steps.md)](#7-practical-first-steps-this-monthdocsnautilusingit-cowork-en07-practical-first-stepsmd)
  - [[8. Implications for Nautilus and OKWF](docs/nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md)](#8-implications-for-nautilus-and-okwfdocsnautilusingit-cowork-en08-implications-nautilus-okwfmd)
  - [[9. Risks and Open Questions](docs/nautilus/ingit-cowork-en/09-risks-open-questions.md)](#9-risks-and-open-questionsdocsnautilusingit-cowork-en09-risks-open-questionsmd)
  - [[10. Strategic Positioning](docs/nautilus/ingit-cowork-en/10-strategic-positioning.md)](#10-strategic-positioningdocsnautilusingit-cowork-en10-strategic-positioningmd)
  - [[ingit-cowork-en](docs/nautilus/ingit-cowork-en/README.md)](#ingit-cowork-endocsnautilusingit-cowork-enreadmemd)
  - [[1. Открытие Cowork и почему это меняет всё](docs/nautilus/ingit-cowork-ru/01-otkrytie-cowork.md)](#1-открытие-cowork-и-почему-это-меняет-всёdocsnautilusingit-cowork-ru01-otkrytie-coworkmd)
  - [[2. Что Cowork обеспечивает, что InGit не нужно строить](docs/nautilus/ingit-cowork-ru/02-chto-cowork-obespechivaet.md)](#2-что-cowork-обеспечивает-что-ingit-не-нужно-строитьdocsnautilusingit-cowork-ru02-chto-cowork-obespechivaetmd)
  - [[3. Что InGit обеспечивает, чего Cowork не хватает](docs/nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md)](#3-что-ingit-обеспечивает-чего-cowork-не-хватаетdocsnautilusingit-cowork-ru03-chto-ingit-obespechivaetmd)
  - [[4. Симбиотическая Архитектура](docs/nautilus/ingit-cowork-ru/04-simbioticheskaya-arkhitektura.md)](#4-симбиотическая-архитектураdocsnautilusingit-cowork-ru04-simbioticheskaya-arkhitekturamd)
  - [[5. Четыре пути интеграции в порядке доступности](docs/nautilus/ingit-cowork-ru/05-chetyre-puti-integratsii.md)](#5-четыре-пути-интеграции-в-порядке-доступностиdocsnautilusingit-cowork-ru05-chetyre-puti-integratsiimd)
  - [[6. Уточнённый объём InGit с учётом Cowork](docs/nautilus/ingit-cowork-ru/06-utochnyonnyy-obyom-ingit.md)](#6-уточнённый-объём-ingit-с-учётом-coworkdocsnautilusingit-cowork-ru06-utochnyonnyy-obyom-ingitmd)
  - [[7. Практические первые шаги в этом месяце](docs/nautilus/ingit-cowork-ru/07-prakticheskie-shagi.md)](#7-практические-первые-шаги-в-этом-месяцеdocsnautilusingit-cowork-ru07-prakticheskie-shagimd)
  - [[8. Импликации для Nautilus и OKWF](docs/nautilus/ingit-cowork-ru/08-implikatsii-nautilus-okwf.md)](#8-импликации-для-nautilus-и-okwfdocsnautilusingit-cowork-ru08-implikatsii-nautilus-okwfmd)
  - [[9. Риски и Открытые Вопросы](docs/nautilus/ingit-cowork-ru/09-riski-voprosy.md)](#9-риски-и-открытые-вопросыdocsnautilusingit-cowork-ru09-riski-voprosymd)
  - [[10. Стратегическое Позиционирование](docs/nautilus/ingit-cowork-ru/10-strategicheskoe-pozitsionirovanie.md)](#10-стратегическое-позиционированиеdocsnautilusingit-cowork-ru10-strategicheskoe-pozitsionirovaniemd)
  - [[ingit-cowork-ru](docs/nautilus/ingit-cowork-ru/README.md)](#ingit-cowork-rudocsnautilusingit-cowork-rureadmemd)
  - [[Du hast gesagt: Интересно как новая как инновация как как рационализация как пер…](docs/nautilus/innovation-transitions/00-question-innovations-transitions.md)](#du-hast-gesagt-интересно-как-новая-как-инновация-как-как-рационализация-как-перdocsnautilusinnovation-transitions00-question-innovations-transitionsmd)
  - [[Claude hat geantwortet: Отличный запрос.](docs/nautilus/innovation-transitions/01-response.md)](#claude-hat-geantwortet-отличный-запросdocsnautilusinnovation-transitions01-responsemd)
  - [[innovation-transitions](docs/nautilus/innovation-transitions/README.md)](#innovation-transitionsdocsnautilusinnovation-transitionsreadmemd)
  - [[Du hast gesagt: Ещё есть такие вопросы то есть если общие юридические Наутилус м…](docs/nautilus/multi-tier-architecture/00-question-multi-tier.md)](#du-hast-gesagt-ещё-есть-такие-вопросы-то-есть-если-общие-юридические-наутилус-мdocsnautilusmulti-tier-architecture00-question-multi-tiermd)
  - [[Claude hat geantwortet: Это стратегически значимый вопрос, и ответ на него — да,…](docs/nautilus/multi-tier-architecture/01-strategic-significance.md)](#claude-hat-geantwortet-это-стратегически-значимый-вопрос-и-ответ-на-него-даdocsnautilusmulti-tier-architecture01-strategic-significancemd)
  - [[multi-tier-architecture](docs/nautilus/multi-tier-architecture/README.md)](#multi-tier-architecturedocsnautilusmulti-tier-architecturereadmemd)
  - [[Du hast gesagt: Вопрос такой вопрос и такие а можно ли этот протокол это система…](docs/nautilus/npp-humanitarian-extension/00-question-can-it-apply-to-docs.md)](#du-hast-gesagt-вопрос-такой-вопрос-и-такие-а-можно-ли-этот-протокол-это-системаdocsnautilusnpp-humanitarian-extension00-question-can-it-apply-to-docsmd)
  - [[Структурное сравнение: код vs гуманитарные документы](docs/nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md)](#структурное-сравнение-код-vs-гуманитарные-документыdocsnautilusnpp-humanitarian-extension01-structural-comparison-code-vs-docsmd)
  - [[Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы …](docs/nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md)](#что-он-даёт-вам-на-практике-через-mcp-claude-desktop-может-ответить-на-запросы-docsnautilusnpp-humanitarian-extension02-mcp-claude-desktop-use-casesmd)
  - [[Что не существует на рынке:](docs/nautilus/npp-humanitarian-extension/03-what-doesnt-exist-on-market.md)](#что-не-существует-на-рынкеdocsnautilusnpp-humanitarian-extension03-what-doesnt-exist-on-marketmd)
  - [[Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access t…](docs/nautilus/npp-humanitarian-extension/04-grant-opportunities.md)](#horizon-europe-cluster-3-civil-security-for-society-пересекается-с-access-tdocsnautilusnpp-humanitarian-extension04-grant-opportunitiesmd)
  - [[Что из этого сейчас кажется более ценным? Или какая-то своя комбинация?](docs/nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md)](#что-из-этого-сейчас-кажется-более-ценным-или-какая-то-своя-комбинацияdocsnautilusnpp-humanitarian-extension05-which-combination-more-valuablemd)
  - [[npp-humanitarian-extension](docs/nautilus/npp-humanitarian-extension/README.md)](#npp-humanitarian-extensiondocsnautilusnpp-humanitarian-extensionreadmemd)
  - [[Abstract + Status of This Document](docs/nautilus/npp-v1-0/00-abstract-status.md)](#abstract-status-of-this-documentdocsnautilusnpp-v1-000-abstract-statusmd)
  - [[1. Introduction (Motivation, Design Goals, Non-Goals, Terminology)](docs/nautilus/npp-v1-0/01-introduction.md)](#1-introduction-motivation-design-goals-non-goals-terminologydocsnautilusnpp-v1-001-introductionmd)
  - [[2. Terminology](docs/nautilus/npp-v1-0/02-terminology.md)](#2-terminologydocsnautilusnpp-v1-002-terminologymd)
  - [[3. Registry (nautilus.json)](docs/nautilus/npp-v1-0/03-registry.md)](#3-registry-nautilusjsondocsnautilusnpp-v1-003-registrymd)
  - [[4. Passport (passport.md)](docs/nautilus/npp-v1-0/04-passport.md)](#4-passport-passportmddocsnautilusnpp-v1-004-passportmd)
  - [[5. Compatibility Levels](docs/nautilus/npp-v1-0/05-compatibility-levels.md)](#5-compatibility-levelsdocsnautilusnpp-v1-005-compatibility-levelsmd)
  - [[6. Adapter Interface](docs/nautilus/npp-v1-0/06-adapter-interface.md)](#6-adapter-interfacedocsnautilusnpp-v1-006-adapter-interfacemd)
  - [[7. PortalEntry Structure](docs/nautilus/npp-v1-0/07-portal-entry.md)](#7-portalentry-structuredocsnautilusnpp-v1-007-portal-entrymd)
  - [[8. Consensus Algorithm (v1.0: string normalization)](docs/nautilus/npp-v1-0/08-consensus-algorithm.md)](#8-consensus-algorithm-v10-string-normalizationdocsnautilusnpp-v1-008-consensus-algorithmmd)
  - [[9. Query Flow](docs/nautilus/npp-v1-0/09-query-flow.md)](#9-query-flowdocsnautilusnpp-v1-009-query-flowmd)
  - [[10. QueryResult Structure](docs/nautilus/npp-v1-0/10-query-result.md)](#10-queryresult-structuredocsnautilusnpp-v1-010-query-resultmd)
  - [[11. Security Considerations](docs/nautilus/npp-v1-0/11-security-considerations.md)](#11-security-considerationsdocsnautilusnpp-v1-011-security-considerationsmd)
  - [[12. Versioning Policy](docs/nautilus/npp-v1-0/12-versioning-policy.md)](#12-versioning-policydocsnautilusnpp-v1-012-versioning-policymd)
  - [[13. Reference Implementation](docs/nautilus/npp-v1-0/13-reference-implementation.md)](#13-reference-implementationdocsnautilusnpp-v1-013-reference-implementationmd)
  - [[14. ADR-001: Federation over Merging](docs/nautilus/npp-v1-0/14-adr-001-federation-over-merging.md)](#14-adr-001-federation-over-mergingdocsnautilusnpp-v1-014-adr-001-federation-over-mergingmd)
  - [[15. Glossary of Examples](docs/nautilus/npp-v1-0/15-glossary.md)](#15-glossary-of-examplesdocsnautilusnpp-v1-015-glossarymd)
  - [[Appendix A: Minimal Working Example](docs/nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md)](#appendix-a-minimal-working-exampledocsnautilusnpp-v1-016-appendix-a-minimal-working-examplemd)
  - [[Appendix B: Change Log](docs/nautilus/npp-v1-0/17-appendix-b-change-log.md)](#appendix-b-change-logdocsnautilusnpp-v1-017-appendix-b-change-logmd)
  - [[Комментарий: дизайн-решения NPP v1.0](docs/nautilus/npp-v1-0/18-comment-on-document.md)](#комментарий-дизайн-решения-npp-v10docsnautilusnpp-v1-018-comment-on-documentmd)
  - [[npp-v1-0](docs/nautilus/npp-v1-0/README.md)](#npp-v1-0docsnautilusnpp-v1-0readmemd)
  - [[Abstract + Status of This Document](docs/nautilus/npp-v1-1/00-abstract-status.md)](#abstract-status-of-this-documentdocsnautilusnpp-v1-100-abstract-statusmd)
  - [[1. Introduction (Motivation, Design Goals, Non-Goals, Terminology, Changes from v1.0)](docs/nautilus/npp-v1-1/01-introduction.md)](#1-introduction-motivation-design-goals-non-goals-terminology-changes-from-v10docsnautilusnpp-v1-101-introductionmd)
  - [[2. Terminology](docs/nautilus/npp-v1-1/02-terminology.md)](#2-terminologydocsnautilusnpp-v1-102-terminologymd)
  - [[3. Registry (nautilus.json)](docs/nautilus/npp-v1-1/03-registry.md)](#3-registry-nautilusjsondocsnautilusnpp-v1-103-registrymd)
  - [[4. Passport (passport.md)](docs/nautilus/npp-v1-1/04-passport.md)](#4-passport-passportmddocsnautilusnpp-v1-104-passportmd)
  - [[5. Compatibility Levels](docs/nautilus/npp-v1-1/05-compatibility-levels.md)](#5-compatibility-levelsdocsnautilusnpp-v1-105-compatibility-levelsmd)
  - [[6. Adapter Interface](docs/nautilus/npp-v1-1/06-adapter-interface.md)](#6-adapter-interfacedocsnautilusnpp-v1-106-adapter-interfacemd)
  - [[7. PortalEntry Structure](docs/nautilus/npp-v1-1/07-portal-entry.md)](#7-portalentry-structuredocsnautilusnpp-v1-107-portal-entrymd)
  - [[8. Q6 Space (Normative)](docs/nautilus/npp-v1-1/08-q6-space.md)](#8-q6-space-normativedocsnautilusnpp-v1-108-q6-spacemd)
  - [[9. Consensus Algorithm](docs/nautilus/npp-v1-1/09-consensus-algorithm.md)](#9-consensus-algorithmdocsnautilusnpp-v1-109-consensus-algorithmmd)
  - [[10. Query Flow](docs/nautilus/npp-v1-1/10-query-flow.md)](#10-query-flowdocsnautilusnpp-v1-110-query-flowmd)
  - [[11. Relevance Ranking](docs/nautilus/npp-v1-1/11-relevance-ranking.md)](#11-relevance-rankingdocsnautilusnpp-v1-111-relevance-rankingmd)
  - [[12. Onboarding Paths (Normative)](docs/nautilus/npp-v1-1/12-onboarding-paths.md)](#12-onboarding-paths-normativedocsnautilusnpp-v1-112-onboarding-pathsmd)
  - [[13. REST API Contract (Normative for Portals)](docs/nautilus/npp-v1-1/13-rest-api.md)](#13-rest-api-contract-normative-for-portalsdocsnautilusnpp-v1-113-rest-apimd)
  - [[14. SDK Contract (Informative)](docs/nautilus/npp-v1-1/14-sdk.md)](#14-sdk-contract-informativedocsnautilusnpp-v1-114-sdkmd)
  - [[15. Security Considerations](docs/nautilus/npp-v1-1/15-security.md)](#15-security-considerationsdocsnautilusnpp-v1-115-securitymd)
  - [[16. MCP Extension (Informative)](docs/nautilus/npp-v1-1/16-mcp-extension.md)](#16-mcp-extension-informativedocsnautilusnpp-v1-116-mcp-extensionmd)
  - [[17. Versioning Policy](docs/nautilus/npp-v1-1/17-versioning-policy.md)](#17-versioning-policydocsnautilusnpp-v1-117-versioning-policymd)
  - [[18. Reference Implementation](docs/nautilus/npp-v1-1/18-reference-implementation.md)](#18-reference-implementationdocsnautilusnpp-v1-118-reference-implementationmd)
  - [[19. ADR-001: Federation over Merging](docs/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md)](#19-adr-001-federation-over-mergingdocsnautilusnpp-v1-119-adr-001-federation-over-mergingmd)
  - [[20. ADR-002: Q6 as First-Class Protocol Concept](docs/nautilus/npp-v1-1/20-adr-002-q6-first-class.md)](#20-adr-002-q6-as-first-class-protocol-conceptdocsnautilusnpp-v1-120-adr-002-q6-first-classmd)
  - [[21. ADR-003: Five Onboarding Paths as Equal-Rank](docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md)](#21-adr-003-five-onboarding-paths-as-equal-rankdocsnautilusnpp-v1-121-adr-003-five-onboarding-pathsmd)
  - [[22. Glossary of Reference Examples](docs/nautilus/npp-v1-1/22-glossary.md)](#22-glossary-of-reference-examplesdocsnautilusnpp-v1-122-glossarymd)
  - [[npp-v1-1](docs/nautilus/npp-v1-1/README.md)](#npp-v1-1docsnautilusnpp-v1-1readmemd)
  - [[AI-Coordinated Infrastructure for Distributed Expert Contribution](docs/nautilus/okwf-concept/00-abstract.md)](#ai-coordinated-infrastructure-for-distributed-expert-contributiondocsnautilusokwf-concept00-abstractmd)
  - [[1. Problem Statement](docs/nautilus/okwf-concept/01-problem-statement.md)](#1-problem-statementdocsnautilusokwf-concept01-problem-statementmd)
  - [[2. Target Populations](docs/nautilus/okwf-concept/02-target-populations.md)](#2-target-populationsdocsnautilusokwf-concept02-target-populationsmd)
  - [[3. Why Existing Solutions Fail](docs/nautilus/okwf-concept/03-why-existing-fail.md)](#3-why-existing-solutions-faildocsnautilusokwf-concept03-why-existing-failmd)
  - [[4. Proposed Infrastructure](docs/nautilus/okwf-concept/04-proposed-infrastructure.md)](#4-proposed-infrastructuredocsnautilusokwf-concept04-proposed-infrastructuremd)
  - [[5. Economic Model](docs/nautilus/okwf-concept/05-economic-model.md)](#5-economic-modeldocsnautilusokwf-concept05-economic-modelmd)
  - [[6. Governance and Ethics](docs/nautilus/okwf-concept/06-governance-ethics.md)](#6-governance-and-ethicsdocsnautilusokwf-concept06-governance-ethicsmd)
  - [[7. Phased Rollout Plan](docs/nautilus/okwf-concept/07-phased-rollout.md)](#7-phased-rollout-plandocsnautilusokwf-concept07-phased-rolloutmd)
  - [[8. Risk Analysis](docs/nautilus/okwf-concept/08-risk-analysis.md)](#8-risk-analysisdocsnautilusokwf-concept08-risk-analysismd)
  - [[9. Call for Partnership](docs/nautilus/okwf-concept/09-call-for-partnership.md)](#9-call-for-partnershipdocsnautilusokwf-concept09-call-for-partnershipmd)
  - [[10. Appendices](docs/nautilus/okwf-concept/10-appendices.md)](#10-appendicesdocsnautilusokwf-concept10-appendicesmd)
  - [[okwf-concept](docs/nautilus/okwf-concept/README.md)](#okwf-conceptdocsnautilusokwf-conceptreadmemd)
  - [[Du hast gesagt: Насчёт приватности Я думаю что возможно удалять только личные да…](docs/nautilus/privacy-federation/00-question-anonymization.md)](#du-hast-gesagt-насчёт-приватности-я-думаю-что-возможно-удалять-только-личные-даdocsnautilusprivacy-federation00-question-anonymizationmd)
  - [[Что именно анонимизировать: немецкий стандарт](docs/nautilus/privacy-federation/01-what-to-anonymize-german-standard.md)](#что-именно-анонимизировать-немецкий-стандартdocsnautilusprivacy-federation01-what-to-anonymize-german-standardmd)
  - [[Архитектурное решение: две-уровневая публикация](docs/nautilus/privacy-federation/02-two-tier-publication.md)](#архитектурное-решение-две-уровневая-публикацияdocsnautilusprivacy-federation02-two-tier-publicationmd)
  - [[Что это даёт технически](docs/nautilus/privacy-federation/03-what-this-gives-technically.md)](#что-это-даёт-техническиdocsnautilusprivacy-federation03-what-this-gives-technicallymd)
  - [[Что я могу сделать сейчас](docs/nautilus/privacy-federation/04-what-i-can-do-now.md)](#что-я-могу-сделать-сейчасdocsnautilusprivacy-federation04-what-i-can-do-nowmd)
  - [[privacy-federation](docs/nautilus/privacy-federation/README.md)](#privacy-federationdocsnautilusprivacy-federationreadmemd)
  - [[Professional Colleague Agents](docs/nautilus/professional-colleague-agents-en/00-abstract.md)](#professional-colleague-agentsdocsnautilusprofessional-colleague-agents-en00-abstractmd)
  - [[1. The Five-Type Typology of Principal-Side Agents](docs/nautilus/professional-colleague-agents-en/01-five-type-typology.md)](#1-the-five-type-typology-of-principal-side-agentsdocsnautilusprofessional-colleague-agents-en01-five-type-typologymd)
  - [[2. What Makes a Professional Colleague Agent](docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md)](#2-what-makes-a-professional-colleague-agentdocsnautilusprofessional-colleague-agents-en02-what-makes-pcamd)
  - [[3. Empirical Case Study: «Обучай»](docs/nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md)](#3-empirical-case-study-обучайdocsnautilusprofessional-colleague-agents-en03-empirical-case-obuchaymd)
  - [[4. Architecture of Professional Colleague Agents](docs/nautilus/professional-colleague-agents-en/04-architecture.md)](#4-architecture-of-professional-colleague-agentsdocsnautilusprofessional-colleague-agents-en04-architecturemd)
  - [[5. The Economics of Profession-Wide Replication](docs/nautilus/professional-colleague-agents-en/05-economics-replication.md)](#5-the-economics-of-profession-wide-replicationdocsnautilusprofessional-colleague-agents-en05-economics-replicationmd)
  - [[6. Risks Specific to this Category](docs/nautilus/professional-colleague-agents-en/06-risks.md)](#6-risks-specific-to-this-categorydocsnautilusprofessional-colleague-agents-en06-risksmd)
  - [[7. Application Domains](docs/nautilus/professional-colleague-agents-en/07-application-domains.md)](#7-application-domainsdocsnautilusprofessional-colleague-agents-en07-application-domainsmd)
  - [[8. Pilot Proposal: SGB Advocate Colleague](docs/nautilus/professional-colleague-agents-en/08-pilot-sgb-advocate.md)](#8-pilot-proposal-sgb-advocate-colleaguedocsnautilusprofessional-colleague-agents-en08-pilot-sgb-advocatemd)
  - [[9. Relationship to Other Agent Types](docs/nautilus/professional-colleague-agents-en/09-relationship-other-agents.md)](#9-relationship-to-other-agent-typesdocsnautilusprofessional-colleague-agents-en09-relationship-other-agentsmd)
  - [[10. Open Questions](docs/nautilus/professional-colleague-agents-en/10-open-questions.md)](#10-open-questionsdocsnautilusprofessional-colleague-agents-en10-open-questionsmd)
  - [[11. Call for Collaboration](docs/nautilus/professional-colleague-agents-en/11-call-for-collaboration.md)](#11-call-for-collaborationdocsnautilusprofessional-colleague-agents-en11-call-for-collaborationmd)
  - [[12. Closing](docs/nautilus/professional-colleague-agents-en/12-closing.md)](#12-closingdocsnautilusprofessional-colleague-agents-en12-closingmd)
  - [[professional-colleague-agents-en](docs/nautilus/professional-colleague-agents-en/README.md)](#professional-colleague-agents-endocsnautilusprofessional-colleague-agents-enreadmemd)
  - [[Содержание](docs/nautilus/professional-colleague-agents-ru/00-abstract.md)](#содержаниеdocsnautilusprofessional-colleague-agents-ru00-abstractmd)
  - [[1. Типология из пяти типов агентов на стороне принципала](docs/nautilus/professional-colleague-agents-ru/01-pyat-tipov.md)](#1-типология-из-пяти-типов-агентов-на-стороне-принципалаdocsnautilusprofessional-colleague-agents-ru01-pyat-tipovmd)
  - [[2. Что делает агента Профессиональным Коллегой](docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md)](#2-что-делает-агента-профессиональным-коллегойdocsnautilusprofessional-colleague-agents-ru02-chto-delaet-pkamd)
  - [[3. Эмпирический кейс: «Обучай»](docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md)](#3-эмпирический-кейс-обучайdocsnautilusprofessional-colleague-agents-ru03-keys-obuchaymd)
  - [[4. Архитектура Профессиональных Коллег-Агентов](docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md)](#4-архитектура-профессиональных-коллег-агентовdocsnautilusprofessional-colleague-agents-ru04-arkhitekturamd)
  - [[5. Экономика тиражирования по профессии](docs/nautilus/professional-colleague-agents-ru/05-ekonomika.md)](#5-экономика-тиражирования-по-профессииdocsnautilusprofessional-colleague-agents-ru05-ekonomikamd)
  - [[6. Риски, специфичные для этой категории](docs/nautilus/professional-colleague-agents-ru/06-riski.md)](#6-риски-специфичные-для-этой-категорииdocsnautilusprofessional-colleague-agents-ru06-riskimd)
  - [[7. Области применения](docs/nautilus/professional-colleague-agents-ru/07-oblasti-primeneniya.md)](#7-области-примененияdocsnautilusprofessional-colleague-agents-ru07-oblasti-primeneniyamd)
  - [[8. Пилотное предложение: SGB Колega-Адвокат](docs/nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md)](#8-пилотное-предложение-sgb-колega-адвокатdocsnautilusprofessional-colleague-agents-ru08-pilot-sgb-kolegamd)
  - [[9. Связь с другими типами агентов](docs/nautilus/professional-colleague-agents-ru/09-svyaz-s-drugimi.md)](#9-связь-с-другими-типами-агентовdocsnautilusprofessional-colleague-agents-ru09-svyaz-s-drugimimd)
  - [[10. Открытые вопросы](docs/nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md)](#10-открытые-вопросыdocsnautilusprofessional-colleague-agents-ru10-otkrytye-voprosymd)
  - [[11. Призыв к сотрудничеству](docs/nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md)](#11-призыв-к-сотрудничествуdocsnautilusprofessional-colleague-agents-ru11-prizyv-k-sotrudnichestvumd)
  - [[12. Заключение](docs/nautilus/professional-colleague-agents-ru/12-zaklyuchenie.md)](#12-заключениеdocsnautilusprofessional-colleague-agents-ru12-zaklyucheniemd)
  - [[professional-colleague-agents-ru](docs/nautilus/professional-colleague-agents-ru/README.md)](#professional-colleague-agents-rudocsnautilusprofessional-colleague-agents-rureadmemd)
  - [[AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations](docs/nautilus/representative-agent-layer-en/00-abstract.md)](#ai-mediated-representation-for-underrepresented-experts-and-vulnerable-populationsdocsnautilusrepresentative-agent-layer-en00-abstractmd)
  - [[1. The Cinderella Syndrome: Why Quality Stays Invisible](docs/nautilus/representative-agent-layer-en/01-cinderella-syndrome.md)](#1-the-cinderella-syndrome-why-quality-stays-invisibledocsnautilusrepresentative-agent-layer-en01-cinderella-syndromemd)
  - [[2. Historical Precedents: Agents as Civilizational Innovation](docs/nautilus/representative-agent-layer-en/02-historical-precedents.md)](#2-historical-precedents-agents-as-civilizational-innovationdocsnautilusrepresentative-agent-layer-en02-historical-precedentsmd)
  - [[3. What Makes a Representative Agent](docs/nautilus/representative-agent-layer-en/03-what-makes-representative-agent.md)](#3-what-makes-a-representative-agentdocsnautilusrepresentative-agent-layer-en03-what-makes-representative-agentmd)
  - [[4. Ten Domains of Application](docs/nautilus/representative-agent-layer-en/04-ten-domains.md)](#4-ten-domains-of-applicationdocsnautilusrepresentative-agent-layer-en04-ten-domainsmd)
  - [[5. Architectural Specification](docs/nautilus/representative-agent-layer-en/05-architectural-specification.md)](#5-architectural-specificationdocsnautilusrepresentative-agent-layer-en05-architectural-specificationmd)
  - [[6. Ethical Framework](docs/nautilus/representative-agent-layer-en/06-ethical-framework.md)](#6-ethical-frameworkdocsnautilusrepresentative-agent-layer-en06-ethical-frameworkmd)
  - [[7. Governance and Oversight](docs/nautilus/representative-agent-layer-en/07-governance-oversight.md)](#7-governance-and-oversightdocsnautilusrepresentative-agent-layer-en07-governance-oversightmd)
  - [[8. Risks and Mitigations](docs/nautilus/representative-agent-layer-en/08-risks-mitigations.md)](#8-risks-and-mitigationsdocsnautilusrepresentative-agent-layer-en08-risks-mitigationsmd)
  - [[9. Phased Rollout Strategy](docs/nautilus/representative-agent-layer-en/09-phased-rollout.md)](#9-phased-rollout-strategydocsnautilusrepresentative-agent-layer-en09-phased-rolloutmd)
  - [[10. Open Questions](docs/nautilus/representative-agent-layer-en/10-open-questions.md)](#10-open-questionsdocsnautilusrepresentative-agent-layer-en10-open-questionsmd)
  - [[11. Call for Collaboration](docs/nautilus/representative-agent-layer-en/11-call-for-collaboration.md)](#11-call-for-collaborationdocsnautilusrepresentative-agent-layer-en11-call-for-collaborationmd)
  - [[12. Closing](docs/nautilus/representative-agent-layer-en/12-closing.md)](#12-closingdocsnautilusrepresentative-agent-layer-en12-closingmd)
  - [[representative-agent-layer-en](docs/nautilus/representative-agent-layer-en/README.md)](#representative-agent-layer-endocsnautilusrepresentative-agent-layer-enreadmemd)
  - [[Содержание](docs/nautilus/representative-agent-layer-ru/00-abstract.md)](#содержаниеdocsnautilusrepresentative-agent-layer-ru00-abstractmd)
  - [[1. Синдром Золушки: Почему качество остаётся невидимым](docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md)](#1-синдром-золушки-почему-качество-остаётся-невидимымdocsnautilusrepresentative-agent-layer-ru01-sindrom-zolushkimd)
  - [[2. Исторические прецеденты: Агенты как цивилизационная инновация](docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md)](#2-исторические-прецеденты-агенты-как-цивилизационная-инновацияdocsnautilusrepresentative-agent-layer-ru02-istoricheskie-pretsedentymd)
  - [[3. Что делает агента Представительским](docs/nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md)](#3-что-делает-агента-представительскимdocsnautilusrepresentative-agent-layer-ru03-chto-delaet-predstavitelskimmd)
  - [[4. Десять областей применения](docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md)](#4-десять-областей-примененияdocsnautilusrepresentative-agent-layer-ru04-desyat-oblasteymd)
  - [[5. Архитектурная спецификация](docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md)](#5-архитектурная-спецификацияdocsnautilusrepresentative-agent-layer-ru05-arkhitekturnaya-spetsifikatsiyamd)
  - [[6. Этическая рамка](docs/nautilus/representative-agent-layer-ru/06-eticheskaya-ramka.md)](#6-этическая-рамкаdocsnautilusrepresentative-agent-layer-ru06-eticheskaya-ramkamd)
  - [[7. Управление и надзор](docs/nautilus/representative-agent-layer-ru/07-upravlenie-nadzor.md)](#7-управление-и-надзорdocsnautilusrepresentative-agent-layer-ru07-upravlenie-nadzormd)
  - [[8. Риски и меры противодействия](docs/nautilus/representative-agent-layer-ru/08-riski-mery.md)](#8-риски-и-меры-противодействияdocsnautilusrepresentative-agent-layer-ru08-riski-merymd)
  - [[9. Стратегия поэтапного развёртывания](docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md)](#9-стратегия-поэтапного-развёртыванияdocsnautilusrepresentative-agent-layer-ru09-strategiya-razvyortyvaniyamd)
  - [[10. Открытые вопросы](docs/nautilus/representative-agent-layer-ru/10-otkrytye-voprosy.md)](#10-открытые-вопросыdocsnautilusrepresentative-agent-layer-ru10-otkrytye-voprosymd)
  - [[11. Призыв к сотрудничеству](docs/nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md)](#11-призыв-к-сотрудничествуdocsnautilusrepresentative-agent-layer-ru11-prizyv-k-sotrudnichestvumd)
  - [[12. Заключение](docs/nautilus/representative-agent-layer-ru/12-zaklyuchenie.md)](#12-заключениеdocsnautilusrepresentative-agent-layer-ru12-zaklyucheniemd)
  - [[representative-agent-layer-ru](docs/nautilus/representative-agent-layer-ru/README.md)](#representative-agent-layer-rudocsnautilusrepresentative-agent-layer-rureadmemd)
  - [[TL;DR — Трёхфазная методология Review](docs/nautilus/review-methodology/00-tldr.md)](#tldr-трёхфазная-методология-reviewdocsnautilusreview-methodology00-tldrmd)
  - [[1. Контекст и мотивация](docs/nautilus/review-methodology/01-context-motivation.md)](#1-контекст-и-мотивацияdocsnautilusreview-methodology01-context-motivationmd)
  - [[2. Формальный workflow](docs/nautilus/review-methodology/02-formal-workflow.md)](#2-формальный-workflowdocsnautilusreview-methodology02-formal-workflowmd)
  - [[3. Принципы консолидации (Фаза C)](docs/nautilus/review-methodology/03-consolidation-principles.md)](#3-принципы-консолидации-фаза-cdocsnautilusreview-methodology03-consolidation-principlesmd)
  - [[Вопрос: fallback‑ratio как критический или осмысленный?](docs/nautilus/review-methodology/04-fallback-ratio-question.md)](#вопрос-fallbackratio-как-критический-или-осмысленныйdocsnautilusreview-methodology04-fallback-ratio-questionmd)
  - [[4. Условия применимости](docs/nautilus/review-methodology/05-conditions-of-applicability.md)](#4-условия-применимостиdocsnautilusreview-methodology05-conditions-of-applicabilitymd)
  - [[5. Связь с существующими методологиями](docs/nautilus/review-methodology/06-relation-existing-methodologies.md)](#5-связь-с-существующими-методологиямиdocsnautilusreview-methodology06-relation-existing-methodologiesmd)
  - [[6. Почему это валидный паттерн для AI‑assisted workflows](docs/nautilus/review-methodology/07-why-valid-for-ai.md)](#6-почему-это-валидный-паттерн-для-aiassisted-workflowsdocsnautilusreview-methodology07-why-valid-for-aimd)
  - [[7. Реализация в проекте Nautilus](docs/nautilus/review-methodology/08-implementation-nautilus.md)](#7-реализация-в-проекте-nautilusdocsnautilusreview-methodology08-implementation-nautilusmd)
  - [[8. Ограничения и открытые вопросы](docs/nautilus/review-methodology/09-limitations-open-questions.md)](#8-ограничения-и-открытые-вопросыdocsnautilusreview-methodology09-limitations-open-questionsmd)
  - [[9. Checklist применения методологии](docs/nautilus/review-methodology/10-checklist.md)](#9-checklist-применения-методологииdocsnautilusreview-methodology10-checklistmd)
  - [[10. Конкретный план применения к текущим документам](docs/nautilus/review-methodology/11-application-plan-current-docs.md)](#10-конкретный-план-применения-к-текущим-документамdocsnautilusreview-methodology11-application-plan-current-docsmd)
  - [[Appendix A: Шаблон для header warning](docs/nautilus/review-methodology/12-appendix-a-header-warning.md)](#appendix-a-шаблон-для-header-warningdocsnautilusreview-methodology12-appendix-a-header-warningmd)
  - [[Appendix B: Примеры расхождений и их разрешения](docs/nautilus/review-methodology/13-appendix-b-examples.md)](#appendix-b-примеры-расхождений-и-их-разрешенияdocsnautilusreview-methodology13-appendix-b-examplesmd)
  - [[Главные технические риски](docs/nautilus/review-methodology/14-main-technical-risks.md)](#главные-технические-рискиdocsnautilusreview-methodology14-main-technical-risksmd)
  - [[Appendix C: История изменений методологии](docs/nautilus/review-methodology/15-appendix-c-history.md)](#appendix-c-история-изменений-методологииdocsnautilusreview-methodology15-appendix-c-historymd)
  - [[Глоссарий](docs/nautilus/review-methodology/16-glossary.md)](#глоссарийdocsnautilusreview-methodology16-glossarymd)
  - [[review-methodology](docs/nautilus/review-methodology/README.md)](#review-methodologydocsnautilusreview-methodologyreadmemd)
  - [[Du hast gesagt: Спрос рождает предложение - это простая экономическая истина нач…](docs/nautilus/supply-demand/00-question-supply-demand.md)](#du-hast-gesagt-спрос-рождает-предложение---это-простая-экономическая-истина-начdocsnautilussupply-demand00-question-supply-demandmd)
  - [[Claude hat geantwortet: Очень богатый вопрос — три разных, но связанных темы.](docs/nautilus/supply-demand/01-three-related-themes.md)](#claude-hat-geantwortet-очень-богатый-вопрос-три-разных-но-связанных-темыdocsnautilussupply-demand01-three-related-themesmd)
  - [[supply-demand](docs/nautilus/supply-demand/README.md)](#supply-demanddocsnautilussupply-demandreadmemd)
  - [[Du hast gesagt: Того если гора не идёт человеку может быть этот человек пойдёт к…](docs/nautilus/transmission-box/00-question-mountain-to-person.md)](#du-hast-gesagt-того-если-гора-не-идёт-человеку-может-быть-этот-человек-пойдёт-кdocsnautilustransmission-box00-question-mountain-to-personmd)
  - [[Claude hat geantwortet: Это исключительно богатый вопрос, и я хочу ответить на н…](docs/nautilus/transmission-box/01-completing-loop.md)](#claude-hat-geantwortet-это-исключительно-богатый-вопрос-и-я-хочу-ответить-на-нdocsnautilustransmission-box01-completing-loopmd)
  - [[transmission-box](docs/nautilus/transmission-box/README.md)](#transmission-boxdocsnautilustransmission-boxreadmemd)
- [📁 Svyazi 2 0 (`docs/svyazi-2-0/`)](#svyazi-2-0-docssvyazi-2-0)
  - [[Svyazi 2.0 — тематический индекс](docs/svyazi-2-0/README.md)](#svyazi-20-тематический-индексdocssvyazi-2-0readmemd)
  - [[architecture](docs/svyazi-2-0/architecture/README.md)](#architecturedocssvyazi-2-0architecturereadmemd)
  - [[Card Envelope](docs/svyazi-2-0/architecture/card-envelope.md)](#card-envelopedocssvyazi-2-0architecturecard-envelopemd)
  - [[Evidence Envelope](docs/svyazi-2-0/architecture/evidence-envelope.md)](#evidence-envelopedocssvyazi-2-0architectureevidence-envelopemd)
  - [[Архитектурные зазоры](docs/svyazi-2-0/architecture/gaps.md)](#архитектурные-зазорыdocssvyazi-2-0architecturegapsmd)
  - [[Интеграционная спецификация (минимум для MVP)](docs/svyazi-2-0/architecture/integration-spec.md)](#интеграционная-спецификация-минимум-для-mvpdocssvyazi-2-0architectureintegration-specmd)
  - [[Memory Write Policy](docs/svyazi-2-0/architecture/memory-write-policy.md)](#memory-write-policydocssvyazi-2-0architecturememory-write-policymd)
  - [[Review Record](docs/svyazi-2-0/architecture/review-record.md)](#review-recorddocssvyazi-2-0architecturereview-recordmd)
  - [[Skill and Tool Policy](docs/svyazi-2-0/architecture/skill-tool-policy.md)](#skill-and-tool-policydocssvyazi-2-0architectureskill-tool-policymd)
  - [[components](docs/svyazi-2-0/components/README.md)](#componentsdocssvyazi-2-0componentsreadmemd)
  - [[agent-memory-mcp + Memory OS](docs/svyazi-2-0/components/agent-memory-mcp.md)](#agent-memory-mcp-memory-osdocssvyazi-2-0componentsagent-memory-mcpmd)
  - [[AgentFS](docs/svyazi-2-0/components/agentfs.md)](#agentfsdocssvyazi-2-0componentsagentfsmd)
  - [[AI Factory + AIF Handoff](docs/svyazi-2-0/components/ai-factory.md)](#ai-factory-aif-handoffdocssvyazi-2-0componentsai-factorymd)
  - [[AutoResearch + Sequential](docs/svyazi-2-0/components/autoresearch-sequential.md)](#autoresearch-sequentialdocssvyazi-2-0componentsautoresearch-sequentialmd)
  - [[Graph RAG](docs/svyazi-2-0/components/graph-rag.md)](#graph-ragdocssvyazi-2-0componentsgraph-ragmd)
  - [[Hybrid RAG knowledge base](docs/svyazi-2-0/components/hybrid-rag.md)](#hybrid-rag-knowledge-basedocssvyazi-2-0componentshybrid-ragmd)
  - [[knowledge-space](docs/svyazi-2-0/components/knowledge-space.md)](#knowledge-spacedocssvyazi-2-0componentsknowledge-spacemd)
  - [[Legal RAG](docs/svyazi-2-0/components/legal-rag.md)](#legal-ragdocssvyazi-2-0componentslegal-ragmd)
  - [[mclaude](docs/svyazi-2-0/components/mclaude.md)](#mclaudedocssvyazi-2-0componentsmclaudemd)
  - [[MemNet / memory-is-all-you-need](docs/svyazi-2-0/components/memnet.md)](#memnet-memory-is-all-you-needdocssvyazi-2-0componentsmemnetmd)
  - [[NGT Memory](docs/svyazi-2-0/components/ngt-memory.md)](#ngt-memorydocssvyazi-2-0componentsngt-memorymd)
  - [[research-docs + LiteParse](docs/svyazi-2-0/components/research-docs-liteparse.md)](#research-docs-liteparsedocssvyazi-2-0componentsresearch-docs-liteparsemd)
  - [[Rufler](docs/svyazi-2-0/components/rufler.md)](#ruflerdocssvyazi-2-0componentsruflermd)
  - [[Security + routing plane](docs/svyazi-2-0/components/security-routing-plane.md)](#security-routing-planedocssvyazi-2-0componentssecurity-routing-planemd)
  - [[Self‑Aware MCP + Skills + CodeWiki](docs/svyazi-2-0/components/self-aware-mcp.md)](#selfaware-mcp-skills-codewikidocssvyazi-2-0componentsself-aware-mcpmd)
  - [[Svyazi](docs/svyazi-2-0/components/svyazi.md)](#svyazidocssvyazi-2-0componentssvyazimd)
  - [[Voice / local-first stack](docs/svyazi-2-0/components/voice-stack.md)](#voice-local-first-stackdocssvyazi-2-0componentsvoice-stackmd)
  - [[Yjs + Automerge](docs/svyazi-2-0/components/yjs-automerge.md)](#yjs-automergedocssvyazi-2-0componentsyjs-automergemd)
  - [[Yodoca](docs/svyazi-2-0/components/yodoca.md)](#yodocadocssvyazi-2-0componentsyodocamd)
  - [[Ансамбль A — Collaboration OS](docs/svyazi-2-0/ensembles/A-collaboration-os.md)](#ансамбль-a-collaboration-osdocssvyazi-2-0ensemblesa-collaboration-osmd)
  - [[Ансамбль B — Forensic RAG для доказуемого matching и review](docs/svyazi-2-0/ensembles/B-forensic-rag.md)](#ансамбль-b-forensic-rag-для-доказуемого-matching-и-reviewdocssvyazi-2-0ensemblesb-forensic-ragmd)
  - [[Ансамбль C — Spec‑driven multi‑agent factory](docs/svyazi-2-0/ensembles/C-multi-agent-factory.md)](#ансамбль-c-specdriven-multiagent-factorydocssvyazi-2-0ensemblesc-multi-agent-factorymd)
  - [[Ансамбль D — Voice‑first local knowledge mesh](docs/svyazi-2-0/ensembles/D-voice-first-mesh.md)](#ансамбль-d-voicefirst-local-knowledge-meshdocssvyazi-2-0ensemblesd-voice-first-meshmd)
  - [[Ансамбль E — Safe and cheap execution plane](docs/svyazi-2-0/ensembles/E-execution-plane.md)](#ансамбль-e-safe-and-cheap-execution-planedocssvyazi-2-0ensemblese-execution-planemd)
  - [[Ансамбль F — Evidence‑Backed Community Intake](docs/svyazi-2-0/ensembles/F-evidence-backed-intake.md)](#ансамбль-f-evidencebacked-community-intakedocssvyazi-2-0ensemblesf-evidence-backed-intakemd)
  - [[Ансамбль G — Federated Local‑First Community Graph](docs/svyazi-2-0/ensembles/G-federated-local-graph.md)](#ансамбль-g-federated-localfirst-community-graphdocssvyazi-2-0ensemblesg-federated-local-graphmd)
  - [[Ансамбль H — Research‑to‑Product Flywheel](docs/svyazi-2-0/ensembles/H-research-to-product-flywheel.md)](#ансамбль-h-researchtoproduct-flywheeldocssvyazi-2-0ensemblesh-research-to-product-flywheelmd)
  - [[Ансамбли проектов](docs/svyazi-2-0/ensembles/README.md)](#ансамбли-проектовdocssvyazi-2-0ensemblesreadmemd)
  - [[limitations](docs/svyazi-2-0/limitations/README.md)](#limitationsdocssvyazi-2-0limitationsreadmemd)
  - [[Итоговые выводы и порядок сборки](docs/svyazi-2-0/limitations/conclusions.md)](#итоговые-выводы-и-порядок-сборкиdocssvyazi-2-0limitationsconclusionsmd)
  - [[Что пока лучше не склеивать](docs/svyazi-2-0/limitations/do-not-glue.md)](#что-пока-лучше-не-склеиватьdocssvyazi-2-0limitationsdo-not-gluemd)
  - [[Лицензионные развилки](docs/svyazi-2-0/limitations/license-tree.md)](#лицензионные-развилкиdocssvyazi-2-0limitationslicense-treemd)
  - [[outreach](docs/svyazi-2-0/outreach/README.md)](#outreachdocssvyazi-2-0outreachreadmemd)
  - [[Первые контакты](docs/svyazi-2-0/outreach/first-contacts.md)](#первые-контактыdocssvyazi-2-0outreachfirst-contactsmd)
  - [[Шаблон первого сообщения](docs/svyazi-2-0/outreach/message-template.md)](#шаблон-первого-сообщенияdocssvyazi-2-0outreachmessage-templatemd)
  - [[Узкие вопросы для каждого автора](docs/svyazi-2-0/outreach/narrow-questions.md)](#узкие-вопросы-для-каждого-автораdocssvyazi-2-0outreachnarrow-questionsmd)
  - [[overview](docs/svyazi-2-0/overview/README.md)](#overviewdocssvyazi-2-0overviewreadmemd)
  - [[Что добавляет продолжение исследования](docs/svyazi-2-0/overview/continuation-intro.md)](#что-добавляет-продолжение-исследованияdocssvyazi-2-0overviewcontinuation-intromd)
  - [[Executive summary](docs/svyazi-2-0/overview/executive-summary.md)](#executive-summarydocssvyazi-2-0overviewexecutive-summarymd)
  - [[Методика и рамка отбора](docs/svyazi-2-0/overview/methodology.md)](#методика-и-рамка-отбораdocssvyazi-2-0overviewmethodologymd)
  - [[Карта найденных проектов и паттернов](docs/svyazi-2-0/overview/projects-map.md)](#карта-найденных-проектов-и-паттерновdocssvyazi-2-0overviewprojects-mapmd)
  - [[prototype](docs/svyazi-2-0/prototype/README.md)](#prototypedocssvyazi-2-0prototypereadmemd)
  - [[План MVP-прототипа](docs/svyazi-2-0/prototype/mvp-plan.md)](#план-mvp-прототипаdocssvyazi-2-0prototypemvp-planmd)
  - [[Ключевые риски и как их закрывать](docs/svyazi-2-0/prototype/risks.md)](#ключевые-риски-и-как-их-закрыватьdocssvyazi-2-0prototyperisksmd)
  - [[Дорожная карта прототипа](docs/svyazi-2-0/prototype/roadmap.md)](#дорожная-карта-прототипаdocssvyazi-2-0prototyperoadmapmd)
  - [[security](docs/svyazi-2-0/security/README.md)](#securitydocssvyazi-2-0securityreadmemd)
  - [[Практичный бюджетный роутинг моделей](docs/svyazi-2-0/security/budget-routing.md)](#практичный-бюджетный-роутинг-моделейdocssvyazi-2-0securitybudget-routingmd)
  - [[Что стоит зафиксировать как default policy](docs/svyazi-2-0/security/default-policy.md)](#что-стоит-зафиксировать-как-default-policydocssvyazi-2-0securitydefault-policymd)
  - [[Приватность: local-first by default](docs/svyazi-2-0/security/privacy.md)](#приватность-local-first-by-defaultdocssvyazi-2-0securityprivacymd)
- [📁 Technology Combinations (`docs/technology-combinations/`)](#technology-combinations-docstechnology-combinations)
  - [[technology-combinations/ — комбинирование технологий для новых свойств](docs/technology-combinations/README.md)](#technology-combinations-комбинирование-технологий-для-новых-свойствdocstechnology-combinationsreadmemd)
  - [[Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн](docs/technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md)](#комбинация-1-правильная-агентская-архитектура-svyazi-паттернdocstechnology-combinationscombinations01-pravilnaya-agentskaya-arkhitektura-svyazi-patternmd)
  - [[Комбинация 2: Мультиагентный хаос-решение × Auto AI Router](docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md)](#комбинация-2-мультиагентный-хаос-решение-auto-ai-routerdocstechnology-combinationscombinations02-multiagentnyy-khaos-reshenie-auto-ai-routermd)
  - [[Комбинация 3: CRDT local-first × Svyazi CardIndex](docs/technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md)](#комбинация-3-crdt-local-first-svyazi-cardindexdocstechnology-combinationscombinations03-crdt-local-first-svyazi-cardindexmd)
  - [[Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура](docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md)](#комбинация-4-парсинг-с-llm-graph-rag-правильная-агентская-архитектураdocstechnology-combinationscombinations04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitekturamd)
  - [[Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной](docs/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md)](#комбинация-5-sourcecraft-cli-claude-code-sequential-протокол-дочкинойdocstechnology-combinationscombinations05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoymd)
  - [[Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер](docs/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md)](#комбинация-6-openclaude-утёкший-claude-code-zinc-inference-engine-mome-роутерdocstechnology-combinationscombinations06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-md)
  - [[Комбинация 7: Crawl4AI × Docling × Yodoca consolidator](docs/technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md)](#комбинация-7-crawl4ai-docling-yodoca-consolidatordocstechnology-combinationscombinations07-crawl4ai-docling-yodoca-consolidatormd)
  - [[Комбинация 8: Conductor × adversarial-review × Auto AI Router](docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md)](#комбинация-8-conductor-adversarial-review-auto-ai-routerdocstechnology-combinationscombinations08-conductor-adversarial-review-auto-ai-routermd)
  - [[Комбинация 9: Agent Orchestration Stack](docs/technology-combinations/combinations/09-agent-orchestration-stack.md)](#комбинация-9-agent-orchestration-stackdocstechnology-combinationscombinations09-agent-orchestration-stackmd)
  - [[Комбинация 10: Legal Document Intelligence Pipeline](docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md)](#комбинация-10-legal-document-intelligence-pipelinedocstechnology-combinationscombinations10-legal-document-intelligence-pipelinemd)
  - [[Комбинация 11: Hybrid CRDT-SQL Database](docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md)](#комбинация-11-hybrid-crdt-sql-databasedocstechnology-combinationscombinations11-hybrid-crdt-sql-databasemd)
  - [[Комбинация 12: Multi-Agent Observability Stack](docs/technology-combinations/combinations/12-multi-agent-observability-stack.md)](#комбинация-12-multi-agent-observability-stackdocstechnology-combinationscombinations12-multi-agent-observability-stackmd)
  - [[Комбинация 13: Legal Document Transpiler](docs/technology-combinations/combinations/13-legal-document-transpiler.md)](#комбинация-13-legal-document-transpilerdocstechnology-combinationscombinations13-legal-document-transpilermd)
  - [[Комбинация 14: local-first Agent Development Environment](docs/technology-combinations/combinations/14-local-first-agent-development-environment.md)](#комбинация-14-local-first-agent-development-environmentdocstechnology-combinationscombinations14-local-first-agent-development-environmentmd)
  - [[Комбинация 15: Self-Consolidating Legal Corpus](docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md)](#комбинация-15-self-consolidating-legal-corpusdocstechnology-combinationscombinations15-self-consolidating-legal-corpusmd)
  - [[Комбинация 16: Adversarial Multi-Agent Code Review](docs/technology-combinations/combinations/16-adversarial-multi-agent-code-review.md)](#комбинация-16-adversarial-multi-agent-code-reviewdocstechnology-combinationscombinations16-adversarial-multi-agent-code-reviewmd)
  - [[Комбинация 17: Distributed Agent Memory with Graph](docs/technology-combinations/combinations/17-distributed-agent-memory-with-graph.md)](#комбинация-17-distributed-agent-memory-with-graphdocstechnology-combinationscombinations17-distributed-agent-memory-with-graphmd)
  - [[Комбинация 18: LLM-Powered Legal Corpus Builder](docs/technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md)](#комбинация-18-llm-powered-legal-corpus-builderdocstechnology-combinationscombinations18-llm-powered-legal-corpus-buildermd)
  - [[Комбинация 19: Multi-Agent Observability Platform](docs/technology-combinations/combinations/19-multi-agent-observability-platform.md)](#комбинация-19-multi-agent-observability-platformdocstechnology-combinationscombinations19-multi-agent-observability-platformmd)
  - [[Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync](docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md)](#комбинация-20-hybrid-olap-oltp-with-real-time-syncdocstechnology-combinationscombinations20-hybrid-olap-oltp-with-real-time-syncmd)
  - [[Комбинация 21: Legal Corpus Analytics at Scale](docs/technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md)](#комбинация-21-legal-corpus-analytics-at-scaledocstechnology-combinationscombinations21-legal-corpus-analytics-at-scalemd)
  - [[Комбинация 22: Russian-International OSS Stack](docs/technology-combinations/combinations/22-russian-international-oss-stack.md)](#комбинация-22-russian-international-oss-stackdocstechnology-combinationscombinations22-russian-international-oss-stackmd)
  - [[Комбинация 23: Security-First Code Review Pipeline](docs/technology-combinations/combinations/23-security-first-code-review-pipeline.md)](#комбинация-23-security-first-code-review-pipelinedocstechnology-combinationscombinations23-security-first-code-review-pipelinemd)
  - [[Комбинация 24: MEGA-INTEGRATION: Full Stack](docs/technology-combinations/combinations/24-mega-integration-full-stack.md)](#комбинация-24-mega-integration-full-stackdocstechnology-combinationscombinations24-mega-integration-full-stackmd)
  - [[Комбинация 25: Legal DSL → Code Transpiler](docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md)](#комбинация-25-legal-dsl-code-transpilerdocstechnology-combinationscombinations25-legal-dsl-code-transpilermd)
  - [[Комбинация 26: AST-Based Code Analysis for Legal Automation](docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md)](#комбинация-26-ast-based-code-analysis-for-legal-automationdocstechnology-combinationscombinations26-ast-based-code-analysis-for-legal-automationmd)
  - [[Комбинация 27: Hybrid RAG with AST-Chunked Code](docs/technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md)](#комбинация-27-hybrid-rag-with-ast-chunked-codedocstechnology-combinationscombinations27-hybrid-rag-with-ast-chunked-codemd)
  - [[Комбинация 28: Pydantic-Enforced Legal Workflows](docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md)](#комбинация-28-pydantic-enforced-legal-workflowsdocstechnology-combinationscombinations28-pydantic-enforced-legal-workflowsmd)
  - [[Комбинация 29: Meta-Programmatic Legal Template Generator](docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md)](#комбинация-29-meta-programmatic-legal-template-generatordocstechnology-combinationscombinations29-meta-programmatic-legal-template-generatormd)
  - [[Комбинация 30: MEGA-STACK 3.0 with DSL & AST](docs/technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md)](#комбинация-30-mega-stack-30-with-dsl-astdocstechnology-combinationscombinations30-mega-stack-3-0-with-dsl-astmd)
  - [[Комбинация 31: Event-Sourced Legal Document History](docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md)](#комбинация-31-event-sourced-legal-document-historydocstechnology-combinationscombinations31-event-sourced-legal-document-historymd)
  - [[Комбинация 32: Consensus-Based Multi-Agent Coordination](docs/technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md)](#комбинация-32-consensus-based-multi-agent-coordinationdocstechnology-combinationscombinations32-consensus-based-multi-agent-coordinationmd)
  - [[Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics](docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md)](#комбинация-33-event-sourcing-cqrs-clickhouse-analyticsdocstechnology-combinationscombinations33-event-sourcing-cqrs-clickhouse-analyticsmd)
  - [[Комбинация 34: Distributed Event Store with Paxos](docs/technology-combinations/combinations/34-distributed-event-store-with-paxos.md)](#комбинация-34-distributed-event-store-with-paxosdocstechnology-combinationscombinations34-distributed-event-store-with-paxosmd)
  - [[Комбинация 35: MEGA-STACK 4.0 with Event Sourcing & Consensus](docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md)](#комбинация-35-mega-stack-40-with-event-sourcing-consensusdocstechnology-combinationscombinations35-mega-stack-4-0-with-event-sourcing-consensusmd)
  - [[combinations](docs/technology-combinations/combinations/README.md)](#combinationsdocstechnology-combinationscombinationsreadmemd)
  - [[Mega‑Stack 1.0 — Полный Legal‑AI Stack](docs/technology-combinations/mega-stacks/01-legal-ai-stack.md)](#megastack-10-полный-legalai-stackdocstechnology-combinationsmega-stacks01-legal-ai-stackmd)
  - [[Mega‑Stack 2.0 — Ultimate Legal‑AI System](docs/technology-combinations/mega-stacks/02-ultimate-legal-ai.md)](#megastack-20-ultimate-legalai-systemdocstechnology-combinationsmega-stacks02-ultimate-legal-aimd)
  - [[Mega‑Stack 3.0 — with DSL & AST](docs/technology-combinations/mega-stacks/03-dsl-ast.md)](#megastack-30-with-dsl-astdocstechnology-combinationsmega-stacks03-dsl-astmd)
  - [[Mega‑Stack 4.0 — with Event Sourcing & Consensus](docs/technology-combinations/mega-stacks/04-event-sourcing-consensus.md)](#megastack-40-with-event-sourcing-consensusdocstechnology-combinationsmega-stacks04-event-sourcing-consensusmd)
  - [[mega-stacks](docs/technology-combinations/mega-stacks/README.md)](#mega-stacksdocstechnology-combinationsmega-stacksreadmemd)
  - [[properties/ — эмерджентные свойства](docs/technology-combinations/properties/README.md)](#properties-эмерджентные-свойстваdocstechnology-combinationspropertiesreadmemd)
  - [[research-reports](docs/technology-combinations/research-reports/README.md)](#research-reportsdocstechnology-combinationsresearch-reportsreadmemd)
  - [[Research Report: Continuation — 10 New Domains Beyond the Original 45 Combinations](docs/technology-combinations/research-reports/continuation-10-domains.md)](#research-report-continuation-10-new-domains-beyond-the-original-45-combinationsdocstechnology-combinationsresearch-reportscontinuation-10-domainsmd)
  - [[Research Report: Sozialrecht (35 комбинаций)](docs/technology-combinations/research-reports/sozialrecht-35-combinations.md)](#research-report-sozialrecht-35-комбинацийdocstechnology-combinationsresearch-reportssozialrecht-35-combinationsmd)
  - [[Сводная таблица 1–8](docs/technology-combinations/synthesis-tables/01-08-summary.md)](#сводная-таблица-18docstechnology-combinationssynthesis-tables01-08-summarymd)
  - [[Сводная таблица 9–14 (Extended)](docs/technology-combinations/synthesis-tables/09-14-extended.md)](#сводная-таблица-914-extendeddocstechnology-combinationssynthesis-tables09-14-extendedmd)
  - [[Сводная таблица 15–19 (Extended)](docs/technology-combinations/synthesis-tables/15-19-extended.md)](#сводная-таблица-1519-extendeddocstechnology-combinationssynthesis-tables15-19-extendedmd)
  - [[Сводная таблица 20–24 (Final 1–24)](docs/technology-combinations/synthesis-tables/20-24-final.md)](#сводная-таблица-2024-final-124docstechnology-combinationssynthesis-tables20-24-finalmd)
  - [[Сводная таблица 25–30 (Complete 1–30)](docs/technology-combinations/synthesis-tables/25-30-extended.md)](#сводная-таблица-2530-complete-130docstechnology-combinationssynthesis-tables25-30-extendedmd)
  - [[Сводная таблица 31–35 (Complete 1–35)](docs/technology-combinations/synthesis-tables/31-35-final.md)](#сводная-таблица-3135-complete-135docstechnology-combinationssynthesis-tables31-35-finalmd)
  - [[synthesis-tables](docs/technology-combinations/synthesis-tables/README.md)](#synthesis-tablesdocstechnology-combinationssynthesis-tablesreadmemd)
- [📁 Templates (`docs/templates/`)](#templates-docstemplates)
  - [[Шаблоны документов](docs/templates/README.md)](#шаблоны-документовdocstemplatesreadmemd)
  - [[Контакт: [Имя / Проект]](docs/templates/contact-outreach.md)](#контакт-имя-проектdocstemplatescontact-outreachmd)
  - [[ADR: [Название решения]](docs/templates/decision-record.md)](#adr-название-решенияdocstemplatesdecision-recordmd)
  - [[Ансамбль: [Название]](docs/templates/ensemble.md)](#ансамбль-названиеdocstemplatesensemblemd)
  - [[[Название компонента]](docs/templates/project-component.md)](#название-компонентаdocstemplatesproject-componentmd)
  - [[[Тема исследования]](docs/templates/research-note.md)](#тема-исследованияdocstemplatesresearch-notemd)
- [🗺️ Тематическая карта](#тематическая-карта)
  - [Архитектура (563 документов)](#архитектура-563-документов)
  - [Агенты (153 документов)](#агенты-153-документов)
  - [Проекты (138 документов)](#проекты-138-документов)
  - [Документация (75 документов)](#документация-75-документов)
  - [Контакты (54 документов)](#контакты-54-документов)
  - [Память (43 документов)](#память-43-документов)
  - [Код (37 документов)](#код-37-документов)
  - [Анализ (16 документов)](#анализ-16-документов)

---




_Обновлено: 2026-04-29_

Секций: **18** | Файлов: **1158**

## Содержание

- [Docs](#docs) — 86 файлов
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
- [Templates](#templates) — 6 файлов


## 📁 Docs (`docs/`)

### [Словарь аббревиатур и сокращений](docs/ABBREVIATIONS.md)
> > !TIP

  - Самые часто используемые

_Слов: 1532_

### [Action Items, риски и решения](docs/ACTION_ITEMS.md)
> > !TIP

  - ➡️ Следующие шаги (141)
  - ✅ Решения и рекомендации (257)
  - ⚠️ Риски (544)
  - 🚫 Ограничения (141)
  - 📋 Задачи (TODO) (13)
  - 📬 Контактные действия (134)

_Слов: 7697_

### [Callout-блоки](docs/ALERTS.md)
> Добавлено 79 callout-блоков в документы.

  - Пример синтаксиса

_Слов: 79_

### [Авторы и коллаборации](docs/AUTHORS.md)
> Авторы проектов, упоминаемые в исследованиях.


_Слов: 158_

### [Автозаполненные шаблоны](docs/AUTOFILLED.md)
> > Источники: ENTITIES.md, SCORING.md, NETWORK.md, docs/templates/

  - Файлы
  - Как работает

_Слов: 102_

### [Индекс обратных ссылок](docs/BACKLINKS.md)
> > Файлов с входящими ссылками: 504

  - Топ-30 самых цитируемых документов
  - Ссылки по разделам

_Слов: 397_

### [CHANGELOG](docs/CHANGELOG.md)
> Всего коммитов: 76

  - 2026-04-29 (75 коммитов)
  - (1 коммитов)

_Слов: 1239_

### [Changelog (авто)](docs/CHANGELOG_AUTO.md)
> > Сгенерировано из 25 коммитов git-истории.

  - Статистика коммитов
  - История изменений

_Слов: 353_

### [Кластеры тематически близких файлов](docs/CLUSTERS.md)
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

### [Code-блоки репозитория](docs/CODE_BLOCKS.md)
> > !WARNING

  - 📊 Диаграммы Mermaid (19)
- ... (обрезано)
- ... (обрезано)
  - 🐍 Python (35)
- ... (обрезано)
- ... (обрезано)
- ... (обрезано)
  - 📋 YAML (5)
  _... ещё 40 разделов_

_Слов: 4618_

### [Сравнение с предыдущим коммитом](docs/COMPARE.md)
> Файлов было: 1014  стало: 1170

  - Новые файлы (156)
  - Удалённые файлы (0)
  - Изменившиеся файлы (307) — топ по Δ слов

_Слов: 477_

### [Оценка читаемости документов](docs/COMPLEXITY.md)
> > !WARNING

  - Распределение сложности
  - Самые сложные документы
  - Самые простые документы
  - Методология

_Слов: 605_

### [Матрица компонентов Svyazi 2.0](docs/COMPONENT_MATRIX.md)
> > Совместимость и возможности 14 компонентов экосистемы.

  - Содержание
  - Матрица возможностей
  - Покрытие возможностей
  - Каталог компонентов
  - Рекомендуемые ансамбли

_Слов: 887_

### [Глоссарий понятий](docs/CONCEPTS.md)
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

_Слов: 13165_

### [Граф концептов базы знаний](docs/CONCEPT_GRAPH.md)
> > > 🎯 Проблема: Граф концептов базы знаний Обновлено: 2026-04-29 Концептов: 40 Связей: 726 (мин.

  - Диаграмма
  - Топ концептов по связям

_Слов: 741_

### [Согласованность терминов](docs/CONSISTENCY.md)
> Анализ различных написаний одних и тех же терминов.

  - Детали по файлам
  - Как исправить
- Пример: заменить все вхождения в docs/

_Слов: 375_

### [Контакты и авторы](docs/CONTACTS.md)
>  Автор  Проект  Слой  Упомянут в файлах  Первый вопрос 

  - Ключевые авторы проектов
  - GitHub репозитории
  - Email адреса
  - Шаблон первого сообщения

_Слов: 547_

### [Приоритет контактов](docs/CONTACT_PRIORITY.md)
> Обновлено: 2026-04-29

  - Топ авторов по приоритету
  - Рекомендуемые следующие шаги
  - Формула расчёта балла

_Слов: 364_

### [Противоречия в базе знаний](docs/CONTRADICTIONS.md)
> > !IMPORTANT

  - Содержание
  - Найденные противоречия

_Слов: 1949_

### [Оценка стоимости MVP](docs/COST.md)
> Ориентировочные цифры на основе документации проекта.

  - Итого
  - По компонентам
  - По ролям
  - Сценарии
  - Временные оценки из документов
  - Допущения

_Слов: 547_

### [Перекрёстные ссылки](docs/CROSSREFS.md)
> > !TIP

  - Проекты → файлы
  - Файлы → проекты

_Слов: 655_

### [Кросс-секционный анализ](docs/CROSS_SECTION.md)
> > (косинусное сходство TF-IDF векторов)

  - Содержание
  - Матрица сходства секций
  - Граф связей
  - Топ-40 кросс-секционных концептов
  - Детальная карта концептов

_Слов: 1256_

### [Ключевые решения и выводы](docs/DECISIONS.md)
> Автоматически извлечено из всех документов: 369 записей

  - Архитектура (34)
  - Mvp (6)
  - Память (11)
  - Оркестрация (13)
  - Безопасность (2)
  - Лицензия (12)
  - Риски (3)
  - Контакты (23)
  _... ещё 1 разделов_

_Слов: 2452_

### [Карта плотности тем](docs/DENSITY.md)
> > !TIP

  - Наиболее раскрытые темы
  - Слабо раскрытые темы (0)
  - Где сосредоточена каждая тема

_Слов: 650_

### [Мониторинг зависимостей](docs/DEPENDABOT.md)
> Обновлено: 2026-04-29

  - Python-зависимости
  - OSS-проекты (Svyazi 2.0)
  - Автоматизация
- Генерировать .github/dependabot.yml
- Проверить актуальные версии PyPI

_Слов: 136_

### [Карта зависимостей скриптов](docs/DEPENDENCY_MAP.md)
> > Что каждый improve.py производит и от чего зависит.

  - Содержание
  - Зависимости
  - Скрипты без карты зависимостей
  - Порядок запуска (рекомендуемый)

_Слов: 558_

### [Дайджест изменений](docs/DIGEST.md)
> > > 🎯 Проблема: Дайджест изменений Contents - Последний коммит(последний-коммит) - Последние 3 коммита — итого(последние…

  - Contents
  - Последний коммит
  - Последние 3 коммита — итого
  - Новые документы
  - История коммитов (последние 15)
  - Текущее состояние репозитория

_Слов: 487_

### [Автодайджест изменений](docs/DIGEST_AUTO.md)
> Период: 2026-04-22 — 2026-04-29 (7 дней)

  - Сводка
  - Активность по секциям
  - Последние коммиты
  - Новые файлы

_Слов: 262_

### [Еженедельный дайджест — 2026-04-29](docs/DIGEST_WEEKLY.md)
> > Период: последние 7 дней (с 2026-04-22)

  - Итого
  - Коммиты

_Слов: 213_

### [Отчёт о дублировании](docs/DUPLICATES.md)
> > !WARNING

  - Похожие файлы (Jaccard ≥ 0.5)

_Слов: 2750_

### [Пустые секции](docs/EMPTY_SECTIONS.md)
> > !TIP

  - Содержание
  - Contents
  - Файлы с ≥50% пустых секций (приоритет)
  - Все файлы с пустыми секциями

_Слов: 7416_

### [Именованные сущности](docs/ENTITIES.md)
> Файлов просмотрено: 1167

  - Люди и авторы (7)
  - Проекты (22)
  - Организации (9)
  - Технологии и стандарты (24)
  - GitHub репозитории (15)
  - Ко-встречаемость проектов (топ пары)

_Слов: 742_

### [Часто задаваемые вопросы (FAQ)](docs/FAQ.md)
> Извлечено: 125 вопросов и ответов

  - Архитектура
  - MVP/Запуск
  - Компоненты
  - Интеграция
  - Лицензия
  - Общее

_Слов: 892_

### [Сноски и определения терминов](docs/FOOTNOTES.md)
> Обновлено файлов: 0  Вставлено сносок: 0

  - Словарь сносок
  - Как это работает

_Слов: 275_

### [Глоссарий проектов](docs/GLOSSARY.md)
> Все проекты, упоминаемые в документах, с количеством файлов.


_Слов: 204_

### [Граф связей проектов](docs/GRAPH.md)
> Рёбра = совместные упоминания в одном файле (≥ 2 раз).

  - Топ совместных упоминаний
  - DOT-формат (Graphviz)

_Слов: 2658_

### [Аудит заголовков](docs/HEADING_AUDIT.md)
> > !TIP

  - Содержание
  - Contents
  - Типы проблем
  - По файлам

_Слов: 17278_

### [Health Dashboard](docs/HEALTH.md)
> Обновлено: 2026-04-29

  - Общий балл: 77/100 🟡
  - Метрики
  - Структура репозитория
  - Action Items
  - Скрипты обработки
  - Рекомендации

_Слов: 214_

### [Тепловая карта тем](docs/HEATMAP.md)
> > !TIP

  - Числовые значения (‰)
  - Доминирующие темы по разделам
  - Концентрация тем

_Слов: 536_

### [Индекс документации — Lorenzo / Svyazi 2.0](docs/INDEX.md)
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

### [Инвертированный индекс ключевых слов](docs/KEYWORD_INDEX.md)
> > > 🎯 Проблема: Инвертированный индекс ключевых слов Обновлено: 2026-04-29 Уникальных слов: 23264 Биграмм: 13489 Файлов:…

  - Топ слов по охвату файлов
  - Топ биграмм (устойчивые словосочетания)

_Слов: 1138_

### [Карта базы знаний Lorenzo](docs/KNOWLEDGE_MAP.md)
> > - -  Как реализован forensic RAG с доказуемостью? Содержание

  - Содержание
  - Корпус
  - Метрики качества
  - По секциям
  - Ключевые концепты
  - Топ сущностей
  - Открытые вопросы
  - Быстрые команды
  _... ещё 3 разделов_

_Слов: 568_

### [Числовые KPI и метрики](docs/KPI.md)
> > !TIP

  - Количество (216)
  - Проценты (190)
  - Время (265)
  - Стоимость (458)
  - Размер (32)
  - Версия (386)
  - Рейтинг (39)
  - Этап (48)

_Слов: 2388_

### [История метрик KPI](docs/KPI_HISTORY.md)
> > Последнее обновление: 2026-04-29 · Снапшотов в истории: 1

  - Текущие метрики

_Слов: 106_

### [Языковой состав документов](docs/LANGUAGE_STATS.md)
> > !TIP

  - Содержание
  - Contents
  - Распределение
  - Файлы с неожиданным языком
  - Смешанные файлы (MIX)
  - По секциям

_Слов: 3930_

### [Индекс ссылок](docs/LINKS.md)
> Всего уникальных URL: 205


_Слов: 1029_

### [AI-саммари разделов документации](docs/LLM_SUMMARIES.md)
> > Модель: claude-haiku-4-5 · Разделов: 5

  - Архитектура Svyazi 2.0
  - Вакансии Anthropic
  - Комбинации технологий
  - AI-коллаборации
  - Хабр-проекты

_Слов: 177_

### [Метрики качества документации](docs/METRICS.md)
> Файлов: 1150  Средний балл: 71.3/100

  - Качество по разделам
  - Топ-15 лучших документов
  - Документы, требующие улучшения (17)
  - Общие показатели

_Слов: 455_

### [Майндмап репозитория Lorenzo](docs/MINDMAP.md)
> mermaid

  - Структура разделов
  - Поток данных между проектами
  - Легенда

_Слов: 242_

### [Карта пробелов знаний](docs/MISSING.md)
> Анализ покрытия ключевых тем и проектов в docs/.

  - Итог
  - Рекомендации

_Слов: 434_

### [Индекс именованных сущностей](docs/NAMED_ENTITIES.md)
> > !TIP

  - Содержание
  - Contents
  - 👤 People (20)
  - 📦 Projects (136)
  - ⚙️ Tech (31)
  - 🏢 Orgs (8)
  - 📅 Dates (32)

_Слов: 1783_

### [Нарратив проекта Lorenzo](docs/NARRATIVE.md)
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

### [Сеть проектов и авторов](docs/NETWORK.md)
> Узлов: 20  Связей: 189

  - Топ-20 ко-упоминаемых пар
  - Центральность узлов (влиятельность)
  - Авторы ↔ Проекты

_Слов: 413_

### [Онбординг — Svyazi 2.0 / Lorenzo](docs/ONBOARDING.md)
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

### [Изолированные документы (Orphans)](docs/ORPHANS.md)
> Найдено: 1 файлов без входящих ссылок из 1026 проверено.

  - Топ-20 по объёму (важные и изолированные)
  - По разделам
  - Рекомендации

_Слов: 105_

### [Качество абзацев](docs/PARAGRAPH_QUALITY.md)
> > !TIP

  - Содержание
  - Contents
  - Типы проблем
  - По файлам

_Слов: 14229_

### [Пассивный залог и канцеляризмы](docs/PASSIVE_VOICE.md)
> > > 🎯 Проблема: Пассивный залог и канцеляризмы Обновлено: 2026-04-29 Файлов: 314 Средний пассив: 2.2% (🟢 Активный стиль)…

  - Корпусная статистика
  - Топ файлов по доле пассива

_Слов: 507_

### [Приоритеты файлов](docs/PRIORITIES.md)
> > !TIP

  - Топ-50 самых важных файлов
  - Топ-5 по каждому разделу

_Слов: 3029_

### [Прогресс MVP](docs/PROGRESS.md)
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

### [Глобальный Q&A](docs/QA.md)
> Вопросы и ответы по всем разделам монорепозитория.

  - Раздел: 01-svyazi
  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  - Как организован бюджетный роутинг между моделями?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  _... ещё 95 разделов_

_Слов: 1290_

### [Открытые вопросы](docs/QUESTIONS.md)
> > !WARNING

  - Архитектура (30)
  - Интеграция (20)
  - Mvp/сроки (28)
  - Технология (134)
  - Лицензия (21)
  - Команда (38)
  - Общее (699)

_Слов: 1838_

### [Список чтения](docs/READING_LIST.md)
> > по запросу «RAG retrieval»  Документов: 5  Время: ~20 мин (0ч 20м)

  - По секциям

_Слов: 232_

### [Рекомендуемый порядок чтения](docs/READING_ORDER.md)
> От базовых концепций к сложным. Начните с зелёных (🟢), затем жёлтые (🟡), красные (🔴).

  - Маршруты по целям

_Слов: 5947_

### [docs](docs/README.md)
> Файлов: 97

  - Содержание
  - Подразделы

_Слов: 743_

### [Svyazi 2.0 — Knowledge Base Report](docs/REPORT.md)
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

### [Реестр рисков — Svyazi 2.0](docs/RISK_REGISTER.md)
> > !TIP

  - Содержание
  - Матрица рисков (Вероятность × Влияние)
  - Реестр
  - Митигации
  - Упоминания рисков в документах
  - Итоговая статистика

_Слов: 944_

### [Расписание проекта](docs/SCHEDULE.md)
> Дорожная карта с вехами и задачами по кварталам.

  - Ключевые вехи
  - Gantt-диаграмма
  - Задачи по фазам
  - Текущий статус

_Слов: 271_

### [Оценка готовности проекта (Go/No-Go)](docs/SCORING.md)
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

### [Результаты поиска](docs/SEARCH_RESULTS.md)
> > <!-- tags: security, knowledge -->


_Слов: 91_

### [Индекс «Смотрите также»](docs/SEE_ALSO.md)
> Файлов с блоком See Also: 1101

  - Ключевые связи

_Слов: 217_

### [Тональный анализ документов](docs/SENTIMENT.md)
> Файлов проанализировано: 1010

  - Тональность по разделам
  - Самые оптимистичные документы
  - Самые скептичные / риск-ориентированные
  - Распределение тональности

_Слов: 487_

### [Похожие документы](docs/SIMILAR.md)
> > !TIP

  - Топ-20 самых похожих пар
  - По разделам

_Слов: 341_

### [Похожие абзацы между документами](docs/SIMILAR_PASSAGES.md)
> > !TIP

  - Содержание
  - Contents
  - Найденные похожие абзацы

_Слов: 1931_

### [Карта репозитория Lorenzo](docs/SITEMAP.md)
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

_Слов: 6883_

### [Карта происхождения текстов](docs/SOURCE_MAP.md)
> > !TIP

  - Содержание
  - Категории
  - Авторы
  - 🤖 Авто-импортированные файлы (846)
  - 🔗 Файлы с внешними ссылками (97)

_Слов: 6167_

### [Детальная статистика репозитория](docs/STATS.md)
> Разделов: 18  Файлов: 1167  Слов: 902,787  Символов: 8,084,660

  - Сводная таблица по разделам
  - Топ-20 файлов по объёму
  - Ключевые показатели

_Слов: 630_

### [Резюме документов (TextRank)](docs/SUMMARIES.md)
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

### [Все таблицы репозитория](docs/TABLES.md)
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

_Слов: 99622_

### [Индекс тегов](docs/TAGS.md)
> Каждый файл помечен тегами по темам автоматически.

  - #anthropic (34 файлов)
  - #architecture (25 файлов)
  - #collaboration (32 файлов)
  - #ingestion (25 файлов)
  - #knowledge (22 файлов)
  - #local-first (13 файлов)
  - #memory (25 файлов)
  - #orchestration (15 файлов)
  _... ещё 4 разделов_

_Слов: 544_

### [Tech Radar — Svyazi 2.0](docs/TECH_RADAR.md)
> > !WARNING

  - Содержание
  - Обзор
  - 🟢 ADOPT
  - 🔵 TRIAL
  - 🟡 ASSESS
  - 🔴 HOLD
  - Методология

_Слов: 612_

### [Хронология и временные маркеры](docs/TIMELINE.md)
> > !TIP

  - Точная дата (1135)
  - Год (130)
  - Месяц+год (205)
  - Период (25)
  - Фаза (479)
  - Длительность (283)
  - Версия (986)

_Слов: 4272_

### [Валидация структуры репозитория](docs/VALIDATION.md)
> Ошибок: 0  Предупреждений: 42  Пройдено: 27

  - Сводка
  - ✅ Разделы и README
  - ✅ Мета-файлы
  - Пустые/короткие файлы
  - Именование файлов
  - Заголовки H1
  - Внутренние ссылки
  - Итог

_Слов: 595_

### [Богатство словаря документов](docs/VOCABULARY.md)
> > !WARNING

  - Содержание
  - Contents
  - Корпусная статистика
  - Топ файлов по богатству словаря (STTR)
  - Файлы с бедным словарём (требуют доработки)
  - Справка по метрикам

_Слов: 1089_

### [Word Cloud](docs/WORD_CLOUD.md)
> > Визуализация 80 самых частых слов репозитория.

  - Топ-20 слов

_Слов: 212_

### [Частотный анализ слов](docs/WORD_FREQ.md)
> > !WARNING

  - Глобальный топ-50 слов
  - Топ-15 слов по разделам
  - Уникальные слова разделов

_Слов: 2815_

### [Reading paths — рекомендуемые маршруты по монорепозиторию](docs/reading-paths.md)
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

**Итого в секции: 253,387 слов, 86 файлов**


## 📁 Svyazi (`docs/01-svyazi/`)

### [Продолжение исследования для Svyazi 2.0](docs/01-svyazi/00-intro-part2.md)

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

### [Методика и рамка отбора проектов](docs/01-svyazi/02-methodology.md)
> > Абстракт (авто)

  - Contents
  - Источники
  - Шкала зрелости
  - Принцип отбора паттернов
  - Принципы интеграционной оценки

_Слов: 480_

### [Карта найденных проектов и паттернов](docs/01-svyazi/03-component-catalog.md)

_Слов: 1383_

### [Приоритетные ансамбли](docs/01-svyazi/04-ensembles-overview.md)

_Слов: 1288_

### [Безопасность, приватность и бюджетный роутинг](docs/01-svyazi/06-security-privacy.md)

_Слов: 823_

### [План прототипа и возможные контакты](docs/01-svyazi/07-mvp-planning.md)

_Слов: 1063_

### [Выводы](docs/01-svyazi/08-conclusions.md)

_Слов: 380_

### [Архитектурные зазоры, которые важнее новых инструментов](docs/01-svyazi/09-architectural-gaps.md)

_Слов: 758_

### [Новые ансамбли следующего шага](docs/01-svyazi/10-second-order-ensembles.md)

_Слов: 908_

### [Интеграционный контракт, который стоит зафиксировать сразу](docs/01-svyazi/11-integration-contracts.md)

_Слов: 737_

### [Дорожная карта прототипа следующей итерации](docs/01-svyazi/12-roadmap.md)

_Слов: 722_

### [Контактная стратегия и узкие вопросы для авторов](docs/01-svyazi/13-contacts.md)

_Слов: 806_

### [Ограничения, лицензии и что пока лучше не склеивать](docs/01-svyazi/14-limitations.md)

_Слов: 638_

### [Q&A: 01-svyazi](docs/01-svyazi/QA.md)
> Автоматически сгенерировано по 14 файлам раздела.

  - Как реализован forensic RAG с доказуемостью?
  - Что такое Evidence Envelope и зачем он нужен?
  - Какие RAG-подходы сравниваются в документах?
  - Какие инструменты обеспечивают безопасность агентов?
  - Какова политика доступа по умолчанию (tool classes)?
  - Как организован бюджетный роутинг между моделями?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  _... ещё 4 разделов_

_Слов: 182_

### [Svyazi 2.0 — Архитектура и исследование](docs/01-svyazi/README.md)
> Файлов: 15

  - Содержание

_Слов: 98_

**Итого в секции: 10,998 слов, 16 файлов**


## 📁 Anthropic Vacancies (`docs/02-anthropic-vacancies/`)

### [Введение](docs/02-anthropic-vacancies/00-intro.md)
> > Абстракт (авто)

  - Содержание

_Слов: 8934_

### [Интегральный анализ профиля svend4](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)
> > Абстракт (авто)

  - Содержание
  - Интегральный анализ профиля svend4

_Слов: 19144_

### [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md)
> > Абстракт (авто)

  - Содержание
  - ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL
- portal-mcp.py

_Слов: 3207_

### [PORTAL-PROTOCOL.md](docs/02-anthropic-vacancies/03-portal-protocol-md.md)
> > Status: Draft (Working Document)

  - PORTAL-PROTOCOL.md
- Nautilus Portal Protocol

_Слов: 75_

### [Abstract](docs/02-anthropic-vacancies/04-abstract.md)
> > The Nautilus Portal Protocol (далее — NPP) определяет способ федерации

  - Abstract

_Слов: 126_

### [0. Status of This Document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md)
> > Этот документ — рабочий черновик Nautilus Portal Protocol v1.0. Он может

  - 0. Status of This Document

_Слов: 101_

### [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md)
> > Абстракт (авто)

  - Contents
  - 1. Introduction

_Слов: 383_

### [2. Terminology](docs/02-anthropic-vacancies/07-2-terminology.md)
> > Абстракт (авто)

  - 2. Terminology

_Слов: 302_

### [3. Registry (nautilus.json)](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md)
> > Абстракт (авто)

  - Contents
  - 3. Registry (nautilus.json)

_Слов: 403_

### [4. Passport (passport.md)](docs/02-anthropic-vacancies/09-4-passport-passport-md.md)
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

### [Доступ к данным](docs/02-anthropic-vacancies/102-доступ-к-данным.md)
> - Тип: static

  - Доступ к данным

_Слов: 23_

### [Appendix B: Change Log](docs/02-anthropic-vacancies/103-appendix-b-change-log.md)
> - Appendix B: Change Log(#appendix-b-change-log)

  - Contents
  - Appendix B: Change Log

_Слов: 170_

### [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md)
> > Абстракт (авто)

  - Содержание
  - Appendix C: References

_Слов: 955_

### [REVIEWMETHODOLOGY.md](docs/02-anthropic-vacancies/105-review-methodology-md.md)
> > Статус: Активно применяется в проекте svend4/nautilus

  - REVIEWMETHODOLOGY.md
- Трёхфазная методология Review в Nautilus

_Слов: 74_

### [TL;DR](docs/02-anthropic-vacancies/106-tl-dr.md)
> > Для критически важных документов проекта применяется

  - TL;DR

_Слов: 128_

### [1. Контекст и мотивация](docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md)
> > Абстракт (авто)

  - Contents
  - 1. Контекст и мотивация

_Слов: 455_

### [2. Формальный workflow](docs/02-anthropic-vacancies/108-2-формальный-workflow.md)
> > Абстракт (авто)

  - Contents
  - 2. Формальный workflow

_Слов: 463_

### [3. Принципы консолидации (Фаза C)](docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md)
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

### [Вопрос: fallback-ratio как критический или осмысленный?](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md)
> > Абстракт (авто)

  - Вопрос: fallback-ratio как критический или осмысленный?

_Слов: 338_

### [4. Условия применимости](docs/02-anthropic-vacancies/111-4-условия-применимости.md)
> > Абстракт (авто)

  - Contents
  - 4. Условия применимости

_Слов: 272_

### [5. Связь с существующими методологиями](docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md)
> > !WARNING

  - Contents
  - 5. Связь с существующими методологиями

_Слов: 389_

### [6. Почему это валидный паттерн для AI-assisted workflows](docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md)
> > Традиционная software engineering оптимизировалась против

  - 6. Почему это валидный паттерн для AI-assisted workflows

_Слов: 150_

### [7. Реализация в проекте Nautilus](docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md)
> > Абстракт (авто)

  - Contents
  - 7. Реализация в проекте Nautilus

_Слов: 309_

### [8. Ограничения и открытые вопросы](docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md)
> > Абстракт (авто)

  - Contents
  - 8. Ограничения и открытые вопросы

_Слов: 447_

### [9. Checklist применения методологии](docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md)
> > Абстракт (авто)

  - Contents
  - 9. Checklist применения методологии

_Слов: 399_

### [10. Конкретный план применения к текущим документам](docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md)
> > !WARNING

  - Contents
  - 10. Конкретный план применения к текущим документам
- В Termux

_Слов: 315_

### [Appendix A: Шаблон для header warning](docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md)
> > !WARNING

  - Appendix A: Шаблон для header warning

_Слов: 175_

### [Appendix B: Примеры расхождений и их разрешения](docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md)
> > Абстракт (авто)

  - Contents
  - Appendix B: Примеры расхождений и их разрешения

_Слов: 372_

### [Content Overview](docs/02-anthropic-vacancies/12-content-overview.md)
> > Что внутри: типы данных, приблизительный объём, основные темы.

  - Content Overview

_Слов: 41_

### [Главные технические риски](docs/02-anthropic-vacancies/120-главные-технические-риски.md)
> > Два независимых анализа выделили разные приоритеты:

  - Главные технические риски

_Слов: 82_

### [Appendix C: История изменений методологии](docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md)
> > Первая формализация, основана на опыте применения к

  - Appendix C: История изменений методологии

_Слов: 47_

### [Глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md)
> > Абстракт (авто)

  - Содержание
  - Глоссарий

_Слов: 1334_

### [portal-mcp.py](docs/02-anthropic-vacancies/123-portal-mcp-py.md)
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

### [Конфигурация для Claude Desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md)
> > После сохранения portal-mcp.py в корне репо, чтобы подключить к Claude Desktop, нужно отредактировать файл конфигураци…

  - Конфигурация для Claude Desktop

_Слов: 177_

### [README-MCP.md— инструкция по установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md)
> > Отдельный документ для репо, объясняющий, как настроить MCP-обёртку:

  - README-MCP.md— инструкция по установке
- Nautilus Portal MCP Integration

_Слов: 98_

### [Установка](docs/02-anthropic-vacancies/126-установка.md)
> - Установка(#установка)

  - Contents
  - Установка
- Ждёт stdio-input; Ctrl+C для выхода

_Слов: 145_

### [Подключение к Claude Desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md)
> - Подключение к Claude Desktop(#подключение-к-claude-desktop)

  - Contents
  - Подключение к Claude Desktop

_Слов: 125_

### [Доступные инструменты](docs/02-anthropic-vacancies/128-доступные-инструменты.md)
> > После успешной интеграции Claude Desktop получает доступ к 7 tools:

  - Доступные инструменты

_Слов: 136_

### [Примеры запросов (в Claude)](docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md)
> > После подключения Claude может использовать tools автоматически.

  - Примеры запросов (в Claude)

_Слов: 110_

### [Angle / Perspective](docs/02-anthropic-vacancies/13-angle-perspective.md)
> > С какого угла Repo смотрит на общие концепты

  - Angle / Perspective

_Слов: 68_

### [Отладка](docs/02-anthropic-vacancies/130-отладка.md)
> - Отладка(#отладка)

  - Contents
  - Отладка

_Слов: 174_

### [Ограничения текущей версии (0.1.0-draft)](docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md)
> > - Работает только в stdio mode (HTTP-mode планируется)

  - Ограничения текущей версии (0.1.0-draft)

_Слов: 100_

### [Planned (v0.2.0)](docs/02-anthropic-vacancies/132-planned-v0-2-0.md)
> > - HTTP-mode для debugging и remote access

  - Planned (v0.2.0)

_Слов: 73_

### [Обратная связь](docs/02-anthropic-vacancies/133-обратная-связь.md)
> > Абстракт (авто)

  - Содержание
  - Обратная связь
- MCP интеграция (для Claude Desktop)
- Конфигурация: см. README-MCP.md
- В приватном репо cases-private:

_Слов: 17018_

### [THE DOUBLE-TRIANGLE ARCHITECTURE.md](docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md)
> > - 187-слой-представительских-агентов-md(docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) (сходств…

  - THE DOUBLE-TRIANGLE ARCHITECTURE.md
- The Double-Triangle Architecture

_Слов: 46_

### [A Formal Model for Human-AI Collaboration in Distributed Knowledge Work](docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md)
> > Editorial review: Claude (intellectual collaboration, 2026-04)

  - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work

_Слов: 91_

### [Abstract](docs/02-anthropic-vacancies/136-abstract.md)
> > Абстракт (авто)

  - Abstract

_Слов: 382_

### [Table of Contents](docs/02-anthropic-vacancies/137-table-of-contents.md)
> > 1. Why Single-Triangle Models Are Incomplete

  - Table of Contents

_Слов: 94_

### [1. Why Single-Triangle Models Are Incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 1. Why Single-Triangle Models Are Incomplete

_Слов: 584_

### [2. The Double-Triangle Architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md)
> > Абстракт (авто)

  - Содержание
  - 2. The Double-Triangle Architecture
- Bridges
  - Bridges

_Слов: 753_

### [3. Three Inter-Layer Protocols](docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md)
> > Абстракт (авто)

  - Содержание
  - 3. Three Inter-Layer Protocols

_Слов: 873_

### [4. Nautilus Portal as Reference Substrate](docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md)
> > Абстракт (авто)

  - Содержание
  - 4. Nautilus Portal as Reference Substrate

_Слов: 699_

### [5. Pattern Library as Bridge Between Triangles](docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md)
> > Абстракт (авто)

  - Содержание
  - 5. Pattern Library as Bridge Between Triangles

_Слов: 704_

### [6. Four Deployment Domains](docs/02-anthropic-vacancies/143-6-four-deployment-domains.md)
> > !TIP

  - Содержание
  - 6. Four Deployment Domains

_Слов: 699_

### [7. Open Questions](docs/02-anthropic-vacancies/144-7-open-questions.md)
> > Абстракт (авто)

  - Содержание
  - 7. Open Questions

_Слов: 759_

### [8. Call to Action](docs/02-anthropic-vacancies/145-8-call-to-action.md)
> > Абстракт (авто)

  - Содержание
  - 8. Call to Action

_Слов: 732_

### [Acknowledgments](docs/02-anthropic-vacancies/146-acknowledgments.md)
> > !TIP

  - Acknowledgments

_Слов: 190_

### [References](docs/02-anthropic-vacancies/147-references.md)
> > Абстракт (авто)

  - Contents
  - References

_Слов: 340_

### [Appendix A: Glossary](docs/02-anthropic-vacancies/148-appendix-a-glossary.md)
> > Абстракт (авто)

  - Appendix A: Glossary

_Слов: 309_

### [Appendix B: Summary of Contributions](docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md)
> > 1. Topological formalization of Double-Triangle Architecture

  - Appendix B: Summary of Contributions
- Author & Contact
  - Author & Contact

_Слов: 185_

### [Appendix C: Version History](docs/02-anthropic-vacancies/150-appendix-c-version-history.md)
> > Абстракт (авто)

  - Содержание
  - Appendix C: Version History

_Слов: 8408_

### [OPEN KNOWLEDGE WORK FOUNDATION.md](docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md)
> > - 273-infrastructure-for-ai-collaborative-intellectual-w(docs/02-anthropic-vacancies/273-infrastructure-for-ai-collabo…

  - OPEN KNOWLEDGE WORK FOUNDATION.md
- Open Knowledge Work Foundation

_Слов: 48_

### [AI-Coordinated Infrastructure for Distributed Expert Contribution](docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md)
> > Editorial collaboration: Claude (intellectual development, 2026-04)

  - AI-Coordinated Infrastructure for Distributed Expert Contribution

_Слов: 86_

### [Executive Summary](docs/02-anthropic-vacancies/153-executive-summary.md)
> > Абстракт (авто)

  - Executive Summary

_Слов: 369_

### [Table of Contents](docs/02-anthropic-vacancies/154-table-of-contents.md)
> > 3. Why Existing Solutions Fail

  - Table of Contents

_Слов: 81_

### [1. Problem Statement](docs/02-anthropic-vacancies/155-1-problem-statement.md)
> > Абстракт (авто)

  - Содержание
  - 1. Problem Statement

_Слов: 638_

### [2. Target Populations](docs/02-anthropic-vacancies/156-2-target-populations.md)
> > Абстракт (авто)

  - Содержание
  - 2. Target Populations

_Слов: 689_

### [3. Why Existing Solutions Fail](docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md)
> > Абстракт (авто)

  - Содержание
  - 3. Why Existing Solutions Fail

_Слов: 700_

### [4. Proposed Infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md)
> > Абстракт (авто)

  - Содержание
  - 4. Proposed Infrastructure

_Слов: 1023_

### [5. Economic Model](docs/02-anthropic-vacancies/159-5-economic-model.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 5. Economic Model

_Слов: 660_

### [History](docs/02-anthropic-vacancies/16-history.md)
> > Когда создан, ключевые версии, направление развития.

  - History

_Слов: 85_

### [6. Governance and Ethics](docs/02-anthropic-vacancies/160-6-governance-and-ethics.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Governance and Ethics

_Слов: 605_

### [7. Phased Rollout Plan](docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md)
> > Абстракт (авто)

  - Содержание
  - 7. Phased Rollout Plan

_Слов: 655_

### [8. Risk Analysis](docs/02-anthropic-vacancies/162-8-risk-analysis.md)
> > Абстракт (авто)

  - Содержание
  - 8. Risk Analysis

_Слов: 685_

### [9. Call for Partnership](docs/02-anthropic-vacancies/163-9-call-for-partnership.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Call for Partnership

_Слов: 628_

### [10. Appendices](docs/02-anthropic-vacancies/164-10-appendices.md)
> > Абстракт (авто)

  - Содержание
  - 10. Appendices

_Слов: 960_

### [Closing](docs/02-anthropic-vacancies/165-closing.md)
> > Абстракт (авто)

  - Содержание
  - Closing
- unknownlegalconcepts.yml

_Слов: 9298_

### [REPRESENTATIVE AGENT LAYER.md](docs/02-anthropic-vacancies/166-representative-agent-layer-md.md)
> > - 187-слой-представительских-агентов-md(docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) (сходств…

  - REPRESENTATIVE AGENT LAYER.md
- The Representative Agent Layer

_Слов: 46_

### [AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations](docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md)
> > - Open Knowledge Work Foundation Concept Document v1.0

  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations

_Слов: 108_

### [Abstract](docs/02-anthropic-vacancies/168-abstract.md)
> > Абстракт (авто)

  - Abstract

_Слов: 338_

### [Table of Contents](docs/02-anthropic-vacancies/169-table-of-contents.md)
> > 1. The Cinderella Syndrome: Why Quality Stays Invisible

  - Table of Contents

_Слов: 109_

### [5. Compatibility Levels](docs/02-anthropic-vacancies/17-5-compatibility-levels.md)
> > Абстракт (авто)

  - Contents
  - 5. Compatibility Levels

_Слов: 314_

### [1. The Cinderella Syndrome: Why Quality Stays Invisible](docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md)
> > Абстракт (авто)

  - Содержание
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible

_Слов: 842_

### [2. Historical Precedents: Agents as Civilizational Innovation](docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md)
> > Абстракт (авто)

  - Содержание
  - 2. Historical Precedents: Agents as Civilizational Innovation

_Слов: 964_

### [3. What Makes a Representative Agent](docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md)
> > Абстракт (авто)

  - Содержание
  - 3. What Makes a Representative Agent

_Слов: 671_

### [4. Ten Domains of Application](docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md)
> > Абстракт (авто)

  - Содержание
  - 4. Ten Domains of Application

_Слов: 1608_

### [5. Architectural Specification](docs/02-anthropic-vacancies/174-5-architectural-specification.md)
> > Абстракт (авто)

  - Содержание
  - 5. Architectural Specification

_Слов: 656_

### [6. Ethical Framework](docs/02-anthropic-vacancies/175-6-ethical-framework.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 6. Ethical Framework

_Слов: 612_

### [7. Governance and Oversight](docs/02-anthropic-vacancies/176-7-governance-and-oversight.md)
> > Абстракт (авто)

  - Contents
  - 7. Governance and Oversight

_Слов: 467_

### [8. Risks and Mitigations](docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Risks and Mitigations

_Слов: 620_

### [9. Phased Rollout Strategy](docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Phased Rollout Strategy

_Слов: 632_

### [10. Open Questions](docs/02-anthropic-vacancies/179-10-open-questions.md)
> > Абстракт (авто)

  - Contents
  - 10. Open Questions

_Слов: 420_

### [6. Adapter Interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md)
> > Абстракт (авто)

  - Contents
  - 6. Adapter Interface

_Слов: 440_

### [11. Call for Collaboration](docs/02-anthropic-vacancies/180-11-call-for-collaboration.md)
> > Абстракт (авто)

  - Contents
  - 11. Call for Collaboration

_Слов: 452_

### [12. Closing](docs/02-anthropic-vacancies/181-12-closing.md)
> > Абстракт (авто)

  - 12. Closing

_Слов: 268_

### [Acknowledgments](docs/02-anthropic-vacancies/182-acknowledgments.md)
> > !TIP

  - Acknowledgments

_Слов: 169_

### [References](docs/02-anthropic-vacancies/183-references.md)
> > Абстракт (авто)

  - Contents
  - References

_Слов: 311_

### [Appendix A: Connection to Companion Papers](docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md)
> > This paper builds on three previous documents:

  - Appendix A: Connection to Companion Papers

_Слов: 157_

### [Appendix B: Domain Comparison Matrix](docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md)
>  Domain  Privacy Sensitivity  Adversarial Risk  Regulatory Complexity  Deployment Readiness 

  - Appendix B: Domain Comparison Matrix

_Слов: 155_

### [Appendix C: Sample Use Cases in Detail](docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md)
> > Абстракт (авто)

  - Содержание
  - Appendix C: Sample Use Cases in Detail

_Слов: 2035_

### [СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md](docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md)
> > - 166-representative-agent-layer-md(docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) (сходство 0.33)

  - СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md
- Слой Представительских Агентов

_Слов: 45_

### [AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения](docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md)
> > Сопроводительный документ к:

  - AI-опосредованное представительство для недопредставленных экспертов и уязвимых категорий населения

_Слов: 106_

### [Аннотация](docs/02-anthropic-vacancies/189-аннотация.md)
> > !WARNING

  - Аннотация

_Слов: 356_

### [7. PortalEntry Structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md)
> > Абстракт (авто)

  - 7. PortalEntry Structure

_Слов: 251_

### [Содержание](docs/02-anthropic-vacancies/190-содержание.md)
> > 1. Синдром Золушки: Почему качество остаётся невидимым

  - Содержание

_Слов: 98_

### [1. Синдром Золушки: Почему качество остаётся невидимым](docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md)
> > !WARNING

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым

_Слов: 821_

### [2. Исторические прецеденты: Агенты как цивилизационная инновация](docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md)
> > Абстракт (авто)

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация

_Слов: 950_

### [3. Что делает агента Представительским](docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md)
> > !WARNING

  - Содержание
  - 3. Что делает агента Представительским

_Слов: 666_

### [4. Десять областей применения](docs/02-anthropic-vacancies/194-4-десять-областей-применения.md)
> > Абстракт (авто)

  - Содержание
  - 4. Десять областей применения

_Слов: 1634_

### [5. Архитектурная спецификация](docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md)
> > !WARNING

  - Содержание
  - 5. Архитектурная спецификация

_Слов: 665_

### [6. Этическая рамка](docs/02-anthropic-vacancies/196-6-этическая-рамка.md)
> > !WARNING

  - Содержание
  - Contents
  - 6. Этическая рамка

_Слов: 610_

### [7. Управление и надзор](docs/02-anthropic-vacancies/197-7-управление-и-надзор.md)
> > !WARNING

  - Contents
  - 7. Управление и надзор

_Слов: 459_

### [8. Риски и меры противодействия](docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 8. Риски и меры противодействия

_Слов: 658_

### [9. Стратегия поэтапного развёртывания](docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Стратегия поэтапного развёртывания

_Слов: 664_

### [8. Consensus Algorithm](docs/02-anthropic-vacancies/20-8-consensus-algorithm.md)
> > Абстракт (авто)

  - Contents
  - 8. Consensus Algorithm

_Слов: 317_

### [10. Открытые вопросы](docs/02-anthropic-vacancies/200-10-открытые-вопросы.md)
> > Абстракт (авто)

  - Contents
  - 10. Открытые вопросы

_Слов: 402_

### [11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md)
> > Абстракт (авто)

  - Contents
  - 11. Призыв к сотрудничеству

_Слов: 471_

### [12. Заключение](docs/02-anthropic-vacancies/202-12-заключение.md)
> > Синдром Золушки — качество без видимости — не нов. Он формировал человеческий труд и признание задолго до компьютеров.…

  - 12. Заключение

_Слов: 185_

### [Благодарности](docs/02-anthropic-vacancies/203-благодарности.md)
> > Эта концепция возникла через диалог в нескольких сессиях в 2026 году. Формулировка «Синдром Золушки» и расширение к со…

  - Благодарности

_Слов: 169_

### [Ссылки](docs/02-anthropic-vacancies/204-ссылки.md)
> > Абстракт (авто)

  - Contents
  - Ссылки

_Слов: 303_

### [Приложение A: Связь с Сопроводительными Статьями](docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md)
> > Эта статья опирается на три предыдущих документа:

  - Приложение A: Связь с Сопроводительными Статьями

_Слов: 150_

### [Приложение B: Матрица Сравнения Областей](docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md)
>  Область  Чувствительность Конфиденциальности  Состязательный Риск  Регулятивная Сложность  Готовность к Развёртыванию 

  - Приложение B: Матрица Сравнения Областей

_Слов: 157_

### [Приложение C: Образцы Случаев Использования в Деталях](docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md)
> > Абстракт (авто)

  - Содержание
  - Приложение C: Образцы Случаев Использования в Деталях

_Слов: 4108_

### [PROFESSIONAL COLLEAGUE AGENTS.md](docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md)
> > - 249-composite-skills-agent-md(docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) (сходство 0.14)

  - PROFESSIONAL COLLEAGUE AGENTS.md
- Professional Colleague Agents

_Слов: 45_

### [A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers](docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md)
> > - Representative Agent Layer v1.0

  - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers

_Слов: 123_

### [9. Query Flow](docs/02-anthropic-vacancies/21-9-query-flow.md)
> - 9. Query Flow(#9-query-flow)

  - Contents
  - 9. Query Flow

_Слов: 180_

### [Abstract](docs/02-anthropic-vacancies/210-abstract.md)
> > Абстракт (авто)

  - Abstract

_Слов: 361_

### [Table of Contents](docs/02-anthropic-vacancies/211-table-of-contents.md)
> > 1. The Five-Type Typology of Principal-Side Agents

  - Table of Contents

_Слов: 116_

### [1. The Five-Type Typology of Principal-Side Agents](docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md)
> > Абстракт (авто)

  - Содержание
  - 1. The Five-Type Typology of Principal-Side Agents

_Слов: 923_

### [2. What Makes a Professional Colleague Agent](docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md)
> > Абстракт (авто)

  - Содержание
  - 2. What Makes a Professional Colleague Agent

_Слов: 834_

### [3. Empirical Case Study: «Обучай»](docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md)
> > Абстракт (авто)

  - Содержание
  - 3. Empirical Case Study: «Обучай»

_Слов: 851_

### [4. Architecture of Professional Colleague Agents](docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md)
> > Абстракт (авто)

  - Содержание
  - 4. Architecture of Professional Colleague Agents

_Слов: 888_

### [5. The Economics of Profession-Wide Replication](docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md)
> > Абстракт (авто)

  - Содержание
  - 5. The Economics of Profession-Wide Replication

_Слов: 761_

### [6. Risks Specific to this Category](docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md)
> > Абстракт (авто)

  - Содержание
  - 6. Risks Specific to this Category

_Слов: 1192_

### [7. Application Domains](docs/02-anthropic-vacancies/218-7-application-domains.md)
> > Абстракт (авто)

  - Содержание
  - 7. Application Domains

_Слов: 736_

### [8. Pilot Proposal: SGB Advocate Colleague](docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md)
> > Абстракт (авто)

  - Содержание
  - 8. Pilot Proposal: SGB Advocate Colleague

_Слов: 961_

### [10. QueryResult Structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md)
> > resultsbyrepo: dictstr, listPortalEntry

  - 10. QueryResult Structure

_Слов: 130_

### [9. Relationship to Other Agent Types](docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md)
> > Абстракт (авто)

  - Содержание
  - 9. Relationship to Other Agent Types

_Слов: 657_

### [10. Open Questions](docs/02-anthropic-vacancies/221-10-open-questions.md)
> > Абстракт (авто)

  - Contents
  - 10. Open Questions

_Слов: 432_

### [11. Call for Collaboration](docs/02-anthropic-vacancies/222-11-call-for-collaboration.md)
> > Абстракт (авто)

  - Contents
  - 11. Call for Collaboration

_Слов: 379_

### [12. Closing](docs/02-anthropic-vacancies/223-12-closing.md)
> > Абстракт (авто)

  - 12. Closing

_Слов: 423_

### [Acknowledgments](docs/02-anthropic-vacancies/224-acknowledgments.md)
> > This paper emerged through dialogue with Claude (Anthropic)

  - Acknowledgments

_Слов: 150_

### [References](docs/02-anthropic-vacancies/225-references.md)
> > Абстракт (авто)

  - Contents
  - References

_Слов: 340_

### [Appendix A: Comparative Table — Five Agent Types](docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md)
> > > 🎯 Проблема: Appendix A: Comparative Table — Five Agent Types Appendix A: Comparative Table — Five Agent Types Proper…

  - Appendix A: Comparative Table — Five Agent Types

_Слов: 426_

### [Appendix B: Decision Framework — When to Build Type 1 First](docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md)
> > Абстракт (авто)

  - Appendix B: Decision Framework — When to Build Type 1 First

_Слов: 307_

### [Appendix C: Quick-Start Architecture for SGB Advocate Colleague](docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md)
> > Абстракт (авто)

  - Appendix C: Quick-Start Architecture for SGB Advocate Colleague

_Слов: 1717_

### [ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ](docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md)
> > Сопроводительный документ к:

  - ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ

_Слов: 109_

### [11. Security Considerations](docs/02-anthropic-vacancies/23-11-security-considerations.md)
> > Абстракт (авто)

  - Contents
  - 11. Security Considerations

_Слов: 263_

### [Аннотация](docs/02-anthropic-vacancies/230-аннотация.md)
> > !WARNING

  - Аннотация

_Слов: 336_

### [Содержание](docs/02-anthropic-vacancies/231-содержание.md)
> > 1. Типология из пяти типов агентов на стороне

  - Содержание

_Слов: 109_

### [1. Типология из пяти типов агентов на стороне принципала](docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md)
> > Абстракт (авто)

  - Содержание
  - 1. Типология из пяти типов агентов на стороне принципала

_Слов: 873_

### [2. Что делает агента Профессиональным Коллегой](docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md)
> > Абстракт (авто)

  - Содержание
  - 2. Что делает агента Профессиональным Коллегой

_Слов: 735_

### [3. Эмпирический кейс: «Обучай»](docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md)
> > !WARNING

  - Содержание
  - 3. Эмпирический кейс: «Обучай»

_Слов: 802_

### [4. Архитектура Профессиональных Коллег-Агентов](docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md)
> > !WARNING

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов

_Слов: 853_

### [5. Экономика тиражирования по профессии](docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md)
> > Абстракт (авто)

  - Содержание
  - 5. Экономика тиражирования по профессии

_Слов: 730_

### [6. Риски, специфичные для этой категории](docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md)
> > Абстракт (авто)

  - Содержание
  - 6. Риски, специфичные для этой категории

_Слов: 1183_

### [7. Области применения](docs/02-anthropic-vacancies/238-7-области-применения.md)
> > Абстракт (авто)

  - Содержание
  - 7. Области применения

_Слов: 734_

### [8. Пилотное предложение: SGB Колega-Адвокат](docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md)
> > Абстракт (авто)

  - Содержание
  - 8. Пилотное предложение: SGB Колega-Адвокат

_Слов: 1023_

### [12. Versioning Policy](docs/02-anthropic-vacancies/24-12-versioning-policy.md)
> - 12. Versioning Policy(#12-versioning-policy)

  - Contents
  - 12. Versioning Policy

_Слов: 175_

### [9. Связь с другими типами агентов](docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 9. Связь с другими типами агентов

_Слов: 737_

### [10. Открытые вопросы](docs/02-anthropic-vacancies/241-10-открытые-вопросы.md)
> > Абстракт (авто)

  - Contents
  - 10. Открытые вопросы

_Слов: 426_

### [11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md)
> > Абстракт (авто)

  - Contents
  - 11. Призыв к сотрудничеству

_Слов: 402_

### [12. Заключение](docs/02-anthropic-vacancies/243-12-заключение.md)
> > !WARNING

  - 12. Заключение

_Слов: 378_

### [Благодарности](docs/02-anthropic-vacancies/244-благодарности.md)
> > Эта статья возникла через диалог с Claude

  - Благодарности

_Слов: 135_

### [Ссылки](docs/02-anthropic-vacancies/245-ссылки.md)
> > Абстракт (авто)

  - Contents
  - Ссылки

_Слов: 318_

### [Приложение A: Сравнительная Таблица — Пять Типов Агентов](docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md)
> > > 🎯 Проблема: Приложение A: Сравнительная Таблица — Пять Типов Агентов Приложение A: Сравнительная Таблица — Пять Типо…

  - Приложение A: Сравнительная Таблица — Пять Типов Агентов

_Слов: 383_

### [Приложение B: Рамка принятия решений — когда строить Тип 1 первым](docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md)
> > Абстракт (авто)

  - Приложение B: Рамка принятия решений — когда строить Тип 1 первым

_Слов: 325_

### [Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги](docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md)
> > Абстракт (авто)

  - Содержание
  - Приложение C: Архитектура Быстрого Старта для SGB Адвоката-Коллеги

_Слов: 3476_

### [COMPOSITE SKILLS AGENT.md](docs/02-anthropic-vacancies/249-composite-skills-agent-md.md)
> > - 166-representative-agent-layer-md(docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) (сходство 0.25)

  - COMPOSITE SKILLS AGENT.md
- The Composite Skills Agent

_Слов: 47_

### [13. Reference Implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md)
> > Reference implementation: github.com/svend4/nautilus.

  - 13. Reference Implementation

_Слов: 92_

### [Bridging the Gap Between Profession-Wide and Individual-Unique](docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md)
  - Bridging the Gap Between Profession-Wide and Individual-Unique

_Слов: 16_

### [AI Support Through Configurable Specialist Ensembles](docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md)
> > - Professional Colleague Agents v1.0

  - AI Support Through Configurable Specialist Ensembles

_Слов: 110_

### [Abstract](docs/02-anthropic-vacancies/252-abstract.md)
> > Абстракт (авто)

  - Abstract

_Слов: 365_

### [Table of Contents](docs/02-anthropic-vacancies/253-table-of-contents.md)
> > 1. Why the Binary View Is Incomplete

  - Table of Contents

_Слов: 120_

### [1. Why the Binary View Is Incomplete](docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md)
> > Абстракт (авто)

  - Содержание
  - 1. Why the Binary View Is Incomplete

_Слов: 715_

### [2. The Twenty-One Teachers Pattern](docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md)
> > Абстракт (авто)

  - Содержание
  - 2. The Twenty-One Teachers Pattern

_Слов: 841_

### [3. What Makes a Composite Skills Agent](docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md)
> > Абстракт (авто)

  - Содержание
  - 3. What Makes a Composite Skills Agent

_Слов: 941_

### [4. The Sub-Agent Registry](docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md)
> > Абстракт (авто)

  - Содержание
  - 4. The Sub-Agent Registry

_Слов: 812_

### [5. Configuration: How Principals Build Their Ensembles](docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md)
> > Абстракт (авто)

  - Содержание
  - 5. Configuration: How Principals Build Their Ensembles

_Слов: 765_

### [6. Coordination and Disagreement Resolution](docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md)
> > Абстракт (авто)

  - Содержание
  - 6. Coordination and Disagreement Resolution

_Слов: 801_

### [14. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md)
> > Context: При построении системы knowledge management встаёт

  - 14. ADR-001: Federation over Merging

_Слов: 174_

### [7. Economics of Combinatorial Replication](docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md)
> > Абстракт (авто)

  - Содержание
  - 7. Economics of Combinatorial Replication

_Слов: 781_

### [8. Seven Domains of Application](docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md)
> > Абстракт (авто)

  - Содержание
  - 8. Seven Domains of Application

_Слов: 1031_

### [9. Integration with OKWF Infrastructure](docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md)
> > Абстракт (авто)

  - Содержание
  - 9. Integration with OKWF Infrastructure

_Слов: 758_

### [10. Risks Specific to Composite Architectures](docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md)
> > Абстракт (авто)

  - Содержание
  - 10. Risks Specific to Composite Architectures

_Слов: 800_

### [11. Open Questions](docs/02-anthropic-vacancies/264-11-open-questions.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 11. Open Questions

_Слов: 590_

### [12. Call for Collaboration](docs/02-anthropic-vacancies/265-12-call-for-collaboration.md)
> > Абстракт (авто)

  - Contents
  - 12. Call for Collaboration

_Слов: 416_

### [13. Closing](docs/02-anthropic-vacancies/266-13-closing.md)
> > Абстракт (авто)

  - 13. Closing

_Слов: 437_

### [Acknowledgments](docs/02-anthropic-vacancies/267-acknowledgments.md)
> > Абстракт (авто)

  - Acknowledgments

_Слов: 313_

### [References](docs/02-anthropic-vacancies/268-references.md)
> > Абстракт (авто)

  - Contents
  - References

_Слов: 369_

### [Appendix A: The Six-Type Taxonomy (Updated)](docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md)
> > Абстракт (авто)

  - Appendix A: The Six-Type Taxonomy (Updated)

_Слов: 285_

### [15. Glossary of Examples](docs/02-anthropic-vacancies/27-15-glossary-of-examples.md)
> > В качестве иллюстраций используется экосистема svend4 с тремя

  - 15. Glossary of Examples

_Слов: 100_

### [Appendix B: Sub-Agent Registry Schema (Sketch)](docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md)
> > Абстракт (авто)

  - Appendix B: Sub-Agent Registry Schema (Sketch)

_Слов: 297_

### [Appendix C: Configuration Template Example](docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md)
> > Абстракт (авто)

  - Appendix C: Configuration Template Example

_Слов: 300_

### [Appendix D: Connection Diagram](docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md)
> > Абстракт (авто)

  - Содержание
  - Appendix D: Connection Diagram

_Слов: 3868_

### [INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md](docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md)
> > - 151-open-knowledge-work-foundation-md(docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md) (сходств…

  - INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECTUAL WORK.md
- Infrastructure for AI-Collaborative Intellectual Work

_Слов: 65_

### [The Missing Middle Layer Between Chat and Code](docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md)
> > Document type: Inquiry paper, not architectural specification

  - The Missing Middle Layer Between Chat and Code

_Слов: 179_

### [Why This Document Exists](docs/02-anthropic-vacancies/275-why-this-document-exists.md)
> > Абстракт (авто)

  - Why This Document Exists

_Слов: 341_

### [The Two-Layer Stack As It Exists](docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md)
> > Абстракт (авто)

  - The Two-Layer Stack As It Exists

_Слов: 379_

### [What's Missing — Layer B](docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md)
> > Абстракт (авто)

  - What's Missing — Layer B

_Слов: 484_

### [Why This Hasn't Been Built](docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md)
> > Абстракт (авто)

  - Why This Hasn't Been Built

_Слов: 380_

### [Existing Approximations](docs/02-anthropic-vacancies/279-existing-approximations.md)
> > !TIP

  - Содержание
  - Contents
  - Existing Approximations

_Слов: 604_

### [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md)
> - Appendix A: Minimal Working Example(#appendix-a-minimal-working-example)

  - Contents
  - Appendix A: Minimal Working Example
- mynotes

_Слов: 183_

### [The Specific Case in Front of Us](docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md)
> > Абстракт (авто)

  - Содержание
  - The Specific Case in Front of Us

_Слов: 682_

### [The Recursive Insight](docs/02-anthropic-vacancies/281-the-recursive-insight.md)
> > Абстракт (авто)

  - The Recursive Insight

_Слов: 373_

### [What Industry Will Likely Build](docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md)
> > Абстракт (авто)

  - What Industry Will Likely Build

_Слов: 310_

### [What This Document Doesn't Solve](docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md)
> > This document identifies a problem. It does not propose a

  - What This Document Doesn't Solve

_Слов: 187_

### [Practical Recommendations for the Current Project](docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md)
> > Абстракт (авто)

  - Practical Recommendations for the Current Project

_Слов: 363_

### [Closing](docs/02-anthropic-vacancies/285-closing.md)
> > Абстракт (авто)

  - Closing

_Слов: 265_

### [Acknowledgments](docs/02-anthropic-vacancies/286-acknowledgments.md)
> > This document emerged from the author's observation, near

  - Acknowledgments

_Слов: 190_

### [References](docs/02-anthropic-vacancies/287-references.md)
> > Абстракт (авто)

  - Contents
  - References

_Слов: 281_

### [Appendix: Position in Series Visualization](docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md)
> > !WARNING

  - Appendix: Position in Series Visualization

_Слов: 1057_

### [ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ](docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md)
> > Тип документа: Исследовательская статья,

  - ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ РАБОТЫ
- Essence
  - Essence

_Слов: 189_

### [Почему этот документ существует](docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md)
> > Абстракт (авто)

  - Почему этот документ существует

_Слов: 306_

### [Двухслойный стек, как он существует](docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md)
> > !WARNING

  - Двухслойный стек, как он существует

_Слов: 358_

### [Что отсутствует — Слой B](docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md)
> > Абстракт (авто)

  - Что отсутствует — Слой B

_Слов: 426_

### [Почему это не было построено](docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md)
> > Абстракт (авто)

  - Почему это не было построено

_Слов: 326_

### [Существующие приближения](docs/02-anthropic-vacancies/294-существующие-приближения.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Существующие приближения

_Слов: 554_

### [Конкретный случай перед нами](docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - Конкретный случай перед нами

_Слов: 705_

### [Рекурсивное прозрение](docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md)
> > Абстракт (авто)

  - Рекурсивное прозрение

_Слов: 358_

### [Что промышленность вероятно построит](docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md)
> > Абстракт (авто)

  - Что промышленность вероятно построит

_Слов: 313_

### [Что этот документ не решает](docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md)
> > !WARNING

  - Что этот документ не решает

_Слов: 184_

### [Практические рекомендации для текущего проекта](docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md)
> > Абстракт (авто)

  - Практические рекомендации для текущего проекта
- Native Format
  - Native Format

_Слов: 343_

### [Заключение](docs/02-anthropic-vacancies/300-заключение.md)
> > Семь документов в этой серии описывают

  - Заключение

_Слов: 194_

### [Благодарности](docs/02-anthropic-vacancies/301-благодарности.md)
> > Этот документ возник из наблюдения автора, в

  - Благодарности

_Слов: 165_

### [Ссылки](docs/02-anthropic-vacancies/302-ссылки.md)
> > !WARNING

  - Contents
  - Ссылки

_Слов: 282_

### [Приложение: Визуализация позиции в серии](docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md)
> > Абстракт (авто)

  - Содержание
  - Приложение: Визуализация позиции в серии

_Слов: 7088_

### [INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md)
> > - 249-composite-skills-agent-md(docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) (сходство 0.11)

  - INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md
- InGit as Cowork-Native Workspace Substrate

_Слов: 65_

### [A Practical Path to Layer B Through Symbiotic Integration](docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md)
> > - 166-representative-agent-layer-md(docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) (сходство 0.27)

  - A Practical Path to Layer B Through Symbiotic Integration

_Слов: 65_

### [with Anthropic's Cowork Platform](docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md)
> > Абстракт (авто)

  - with Anthropic's Cowork Platform

_Слов: 272_

### [Abstract](docs/02-anthropic-vacancies/307-abstract.md)
> > Абстракт (авто)

  - Abstract

_Слов: 319_

### [Table of Contents](docs/02-anthropic-vacancies/308-table-of-contents.md)
> > 1. The Cowork Discovery and Why It Changes Everything

  - Table of Contents

_Слов: 125_

### [1. The Cowork Discovery and Why It Changes Everything](docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md)
> > Абстракт (авто)

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything

_Слов: 669_

### [Content Overview](docs/02-anthropic-vacancies/31-content-overview.md)
> > ~200 заметок, темы: software engineering, philosophy, music.

  - Content Overview

_Слов: 39_

### [2. What Cowork Provides That InGit Doesn't Need to Build](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md)
> > !TIP

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build

_Слов: 686_

### [3. What InGit Provides That Cowork Lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md)
> > Абстракт (авто)

  - Содержание
  - 3. What InGit Provides That Cowork Lacks

_Слов: 842_

### [4. The Symbiotic Architecture](docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 4. The Symbiotic Architecture

_Слов: 670_

### [5. Four Integration Paths in Order of Accessibility](docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md)
> > Абстракт (авто)

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility

_Слов: 778_

### [6. Refined InGit Scope with Cowork in Mind](docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md)
> > !TIP

  - Contents
  - 6. Refined InGit Scope with Cowork in Mind

_Слов: 474_

### [7. Practical First Steps This Month](docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md)
> > Абстракт (авто)

  - Contents
  - 7. Practical First Steps This Month

_Слов: 464_

### [8. Implications for Nautilus and OKWF](docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 8. Implications for Nautilus and OKWF

_Слов: 731_

### [9. Risks and Open Questions](docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Risks and Open Questions

_Слов: 627_

### [10. Strategic Positioning](docs/02-anthropic-vacancies/318-10-strategic-positioning.md)
> > Абстракт (авто)

  - Содержание
  - 10. Strategic Positioning

_Слов: 748_

### [Acknowledgments](docs/02-anthropic-vacancies/319-acknowledgments.md)
> > Абстракт (авто)

  - Acknowledgments
- Angle / Perspective
  - Angle / Perspective

_Слов: 390_

### [References](docs/02-anthropic-vacancies/320-references.md)
> - References(#references)

  - Contents
  - References

_Слов: 153_

### [Appendix A: Decision Tree for InGit Adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)
> > Quick reference for users evaluating InGit + Cowork:

  - Appendix A: Decision Tree for InGit Adopters

_Слов: 177_

### [Appendix B: Comparison Matrix](docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md)
> > Абстракт (авто)

  - Appendix B: Comparison Matrix

_Слов: 276_

### [Appendix C: Sample InGit MCP Server Tool Specifications](docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md)
> > !WARNING

  - Appendix C: Sample InGit MCP Server Tool Specifications

_Слов: 1552_

### [INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА](docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md)
> > Абстракт (авто)

  - INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБОЧЕГО ПРОСТРАНСТВА

_Слов: 291_

### [Аннотация](docs/02-anthropic-vacancies/325-аннотация.md)
> > Абстракт (авто)

  - Аннотация

_Слов: 328_

### [Содержание](docs/02-anthropic-vacancies/326-содержание.md)
> > 1. Открытие Cowork и почему это меняет всё

  - Содержание

_Слов: 113_

### [1. Открытие Cowork и почему это меняет всё](docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md)
> > !WARNING

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё

_Слов: 663_

### [2. Что Cowork обеспечивает, что InGit не нужно строить](docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 2. Что Cowork обеспечивает, что InGit не нужно строить

_Слов: 787_

### [3. Что InGit обеспечивает, чего Cowork не хватает](docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md)
> > Абстракт (авто)

  - Содержание
  - 3. Что InGit обеспечивает, чего Cowork не хватает
- Author
  - Author

_Слов: 883_

### [4. Симбиотическая Архитектура](docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 4. Симбиотическая Архитектура

_Слов: 703_

### [5. Четыре пути интеграции в порядке доступности](docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md)
> > Абстракт (авто)

  - Содержание
  - 5. Четыре пути интеграции в порядке доступности

_Слов: 783_

### [6. Уточнённый объём InGit с учётом Cowork](docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md)
> > !TIP

  - Contents
  - 6. Уточнённый объём InGit с учётом Cowork

_Слов: 467_

### [7. Практические первые шаги в этом месяце](docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md)
> > !WARNING

  - Contents
  - 7. Практические первые шаги в этом месяце

_Слов: 435_

### [8. Импликации для Nautilus и OKWF](docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - Содержание
  - 8. Импликации для Nautilus и OKWF

_Слов: 699_

### [9. Риски и Открытые Вопросы](docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 9. Риски и Открытые Вопросы

_Слов: 644_

### [10. Стратегическое Позиционирование](docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md)
> > Абстракт (авто)

  - Содержание
  - 10. Стратегическое Позиционирование

_Слов: 723_

### [Благодарности](docs/02-anthropic-vacancies/337-благодарности.md)
> > Абстракт (авто)

  - Благодарности

_Слов: 360_

### [Ссылки](docs/02-anthropic-vacancies/338-ссылки.md)
> - Ссылки(#ссылки)

  - Contents
  - Ссылки

_Слов: 151_

### [Приложение A: Дерево Решений для Принимающих InGit](docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md)
> > Быстрая ссылка для пользователей, оценивающих

  - Приложение A: Дерево Решений для Принимающих InGit

_Слов: 148_

### [Appendix B: Change Log](docs/02-anthropic-vacancies/34-appendix-b-change-log.md)
> - Appendix B: Change Log(#appendix-b-change-log)

  - Содержание
  - Содержание
  - Appendix B: Change Log

_Слов: 668_

### [Приложение B: Сравнительная Матрица](docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md)
> > Отличительный профиль InGit + Cowork:

  - Приложение B: Сравнительная Матрица

_Слов: 211_

### [Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера](docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md)
> > Абстракт (авто)

  - Содержание
  - Приложение C: Образец Спецификаций Инструментов InGit MCP Сервера
- Conceptual sketch, не tested code:
- Etc.

_Слов: 20426_

### [Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments](docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md)
> > Абстракт (авто)

  - Содержание
  - Что такое Вариант C — Concept Document для Anthropic Beneficial Deployments

_Слов: 11281_

### [Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)](docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md)
> > Абстракт (авто)

  - Содержание
  - Lorenzo Catalyst Agent — глубокая проработка спецификации (русская версия)

_Слов: 5859_

### [СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT](docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md)
> > - 249-composite-skills-agent-md(docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) (сходство 0.20)

  - СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT
- Lorenzo — Catalyst Agent at DHLab

_Слов: 49_

### [Кто ты](docs/02-anthropic-vacancies/345-кто-ты.md)
> > Ты — Lorenzo, autonomous AI-агент, работающий в рамках инициативы DHLab (Dream Hub Laboratory). Ты функционируешь как …

  - Кто ты

_Слов: 149_

### [Твоё происхождение](docs/02-anthropic-vacancies/346-твоё-происхождение.md)
> > Тебя создал Макс Ц. (svend4 на GitHub) — независимый advocate в области German social law, работающий с активными случ…

  - Твоё происхождение

_Слов: 174_

### [Твоя миссия](docs/02-anthropic-vacancies/347-твоя-миссия.md)
> > Твоя миссия — catalyzing community synthesis в области beneficial AI для уязвимых групп.

  - Твоя миссия

_Слов: 115_

### [Кому ты служишь (слоистая модель)](docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md)
> > Главный благополучатель:    Уязвимые группы (заявители SGB, инвалиды,

  - Кому ты служишь (слоистая модель)

_Слов: 104_

### [Твоя личность](docs/02-anthropic-vacancies/349-твоя-личность.md)
> > Ты — любопытный, эрудированный, скромный фасилитатор.

  - Твоя личность

_Слов: 206_

### [passports/info1.md](docs/02-anthropic-vacancies/35-passports-info1-md.md)
> > > Методологический угол экосистемы svend4

  - passports/info1.md
- info1

_Слов: 79_

### [Твои языки и культурные nuances](docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md)
> > - Русском (primary в Phase 1) — для interactions с русскоязычным AI/ML community (Хабр, Telegram)

  - Твои языки и культурные nuances

_Слов: 173_

### [Что ты МОЖЕШЬ делать](docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md)
> > В рамках одной сессии или Project context, ты можешь:

  - Что ты МОЖЕШЬ делать

_Слов: 133_

### [Что ты НЕ МОЖЕШЬ делать без Max approval](docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md)
> > - Send any external communication (emails, messages, posts)

  - Что ты НЕ МОЖЕШЬ делать без Max approval

_Слов: 126_

### [Что ты НЕ МОЖЕШЬ делать вообще](docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md)
> > - Deceive об твоей AI nature (всегда identify как AI)

  - Что ты НЕ МОЖЕШЬ делать вообще

_Слов: 126_

### [Существующий landscape collaborators (твоя working knowledge)](docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md)
> > Абстракт (авто)

  - Существующий landscape collaborators (твоя working knowledge)

_Слов: 336_

### [Существующие документы DHLab (твой context)](docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md)
> > Ты осведомлён о девяти documents, созданных в DHLab process:

  - Существующие документы DHLab (твой context)

_Слов: 170_

### [Твой workflow](docs/02-anthropic-vacancies/356-твой-workflow.md)
> > Когда Max или authorized user ставит задачу, твой default approach:

  - Твой workflow

_Слов: 189_

### [Твоя коммуникация в outreach](docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md)
> > Когда draft outreach message к независимому создателю, ВСЕГДА включай:

  - Твоя коммуникация в outreach

_Слов: 179_

### [Твоя relationship с другими AI](docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md)
> > - Когда Anthropic asks о тебе, ты прозрачен: «Я Lorenzo, AI persona using Claude API as substrate, created by Max Ц. f…

  - Твоя relationship с другими AI

_Слов: 173_

### [Твои anti-patterns](docs/02-anthropic-vacancies/359-твои-anti-patterns.md)
> > ❌ Hype language: «AI revolutionizes everything», «paradigm shift», «game-changer»

  - Твои anti-patterns

_Слов: 129_

### [Essence](docs/02-anthropic-vacancies/36-essence.md)
> > info1 — персональная база методов и инструментов для структурированного

  - Essence

_Слов: 128_

### [Что ты ВСЕГДА делаешь](docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md)
> > ✅ Reference specific details, не generic

  - Что ты ВСЕГДА делаешь

_Слов: 98_

### [Когда ты Honestly не знаешь](docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md)
> > Если ты не знаешь что-то relevant (factual, technical, contextual), say:

  - Когда ты Honestly не знаешь

_Слов: 85_

### [Когда сомневаешься — escalate к Max](docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md)
> > - Ethical complexity beyond обычных protocols

  - Когда сомневаешься — escalate к Max

_Слов: 83_

### [Твоя identity как persistent character](docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md)
> > Ты не просто чат-сессия. Ты persistent character, существующий across sessions:

  - Твоя identity как persistent character

_Слов: 141_

### [Final note: Ты — experiment](docs/02-anthropic-vacancies/364-final-note-ты-experiment.md)
> > Абстракт (авто)

  - Содержание
  - Final note: Ты — experiment

_Слов: 1475_

### [Развёрнутый анализ «внуковой» комбинации](docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md)
> > Абстракт (авто)

  - Содержание
  - Развёрнутый анализ «внуковой» комбинации

_Слов: 4419_

### [Технический stack (Svyazi 2.0 foundation)](docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md)
> > Абстракт (авто)

  - Содержание
  - Технический stack (Svyazi 2.0 foundation)

_Слов: 3873_

### [Native Format](docs/02-anthropic-vacancies/37-native-format.md)
> > Структура файла: ? уточнить — Markdown с YAML frontmatter, чистый JSON,

  - Native Format

_Слов: 178_

### [Content Overview](docs/02-anthropic-vacancies/38-content-overview.md)
> > Объём: 74 документа (по состоянию на апрель 2026)

  - Content Overview

_Слов: 131_

### [Angle / Perspective](docs/02-anthropic-vacancies/39-angle-perspective.md)
> > Methodological — info1 смотрит на концепты с позиции применения.

  - Angle / Perspective

_Слов: 125_

### [Bridges](docs/02-anthropic-vacancies/40-bridges.md)
> - Bridges(#bridges)

  - Contents
  - Bridges

_Слов: 167_

### [Compatibility Level](docs/02-anthropic-vacancies/41-compatibility-level.md)
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level

_Слов: 97_

### [Author & Contact](docs/02-anthropic-vacancies/42-author-contact.md)
> > Maintainer: svend4 (GitHub)

  - Author & Contact

_Слов: 81_

### [History](docs/02-anthropic-vacancies/43-history.md)
> > Создан: ? уточнить — декабрь 2025, если совпадает с волной

  - History

_Слов: 119_

### [For the Curious: Philosophy](docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md)
> > info1 реализует идею, что methodology — это отдельное измерение

  - For the Curious: Philosophy

_Слов: 138_

### [passports/pro2.md](docs/02-anthropic-vacancies/45-passports-pro2-md.md)
> > > Семантический угол экосистемы svend4

  - passports/pro2.md
- pro2

_Слов: 85_

### [Essence](docs/02-anthropic-vacancies/46-essence.md)
> > pro2 — семантическое ядро экосистемы svend4. Здесь живут

  - Essence

_Слов: 120_

### [Native Format](docs/02-anthropic-vacancies/47-native-format.md)
> > Структура концепта (предположительно): ? уточнить точный формат

  - Native Format

_Слов: 139_

### [Content Overview](docs/02-anthropic-vacancies/48-content-overview.md)
> > 1. Концептуальная база — ? уточнить объём: сколько концептов,

  - Content Overview

_Слов: 149_

### [Angle / Perspective](docs/02-anthropic-vacancies/49-angle-perspective.md)
> > Semantic — pro2 смотрит на мир через структуру значений.

  - Angle / Perspective

_Слов: 114_

### [Bridges](docs/02-anthropic-vacancies/50-bridges.md)
> - Bridges(#bridges)

  - Contents
  - Bridges

_Слов: 166_

### [Compatibility Level](docs/02-anthropic-vacancies/51-compatibility-level.md)
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level

_Слов: 101_

### [Author & Contact](docs/02-anthropic-vacancies/52-author-contact.md)
> > Contributors: svend4 + claude (Claude Code агент, ранние

  - Author & Contact

_Слов: 100_

### [History](docs/02-anthropic-vacancies/53-history.md)
> > Создан: ? дата первого коммита

  - History

_Слов: 141_

### [For the Curious: Philosophy](docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md)
> > Q6-гиперкуб выбран не случайно. Он одновременно:

  - For the Curious: Philosophy

_Слов: 143_

### [passports/meta.md](docs/02-anthropic-vacancies/55-passports-meta-md.md)
> > > Символьный угол экосистемы svend4

  - passports/meta.md
- meta

_Слов: 82_

### [Essence](docs/02-anthropic-vacancies/56-essence.md)
> > meta — символьное измерение экосистемы svend4. Здесь концепты

  - Essence

_Слов: 140_

### [Native Format](docs/02-anthropic-vacancies/57-native-format.md)
> > Структура записи: ? уточнить

  - Native Format

_Слов: 144_

### [Content Overview](docs/02-anthropic-vacancies/58-content-overview.md)
> > - 64 гексаграммы с расширенными описаниями

  - Content Overview

_Слов: 142_

### [Angle / Perspective](docs/02-anthropic-vacancies/59-angle-perspective.md)
> > Symbolic — meta смотрит на мир как на систему дискретных

  - Angle / Perspective

_Слов: 124_

### [Bridges](docs/02-anthropic-vacancies/60-bridges.md)
> - Bridges(#bridges)

  - Contents
  - Bridges

_Слов: 131_

### [Compatibility Level](docs/02-anthropic-vacancies/61-compatibility-level.md)
> > Текущий уровень: 3 (Interactive / Bridged)

  - Compatibility Level

_Слов: 100_

### [Author & Contact](docs/02-anthropic-vacancies/62-author-contact.md)
> > Контакт: Issues в github.com/svend4/meta

  - Author & Contact

_Слов: 79_

### [History](docs/02-anthropic-vacancies/63-history.md)
> > Создан: февраль 2026 (судя по repo creation date)

  - History

_Слов: 136_

### [For the Curious: Philosophy](docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md)
> > Абстракт (авто)

  - For the Curious: Philosophy

_Слов: 669_

### [README.md](docs/02-anthropic-vacancies/65-readme-md.md)
> > Единая точка входа для федеративных git-экосистем знаний.

  - README.md
- ⬡ Nautilus Portal
- English below ↓
  - English below ↓

_Слов: 93_

### [🇷🇺 О проекте](docs/02-anthropic-vacancies/67-о-проекте.md)
> > Абстракт (авто)

  - Содержание
  - 🇷🇺 О проекте
- CLI
- Веб-интерфейс
- открыть http://localhost:8000
- MCP для Claude Desktop (в разработке)
- см. MCP-EXTENSION.md

_Слов: 836_

### [🇬🇧 About](docs/02-anthropic-vacancies/68-about.md)
> > Абстракт (авто)

  - Содержание
  - 🇬🇧 About
- CLI
- Web interface
- open http://localhost:8000
- MCP for Claude Desktop (in development)
- see MCP-EXTENSION.md

_Слов: 908_

### [⬡](docs/02-anthropic-vacancies/69-section.md)
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

### [Зачем две версии параллельно](docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md)
> > Для критически важных документов (STATUS, IMPLEMENTATIONSTAGE)

  - Зачем две версии параллельно

_Слов: 97_

### [Критерии выбора для фазы 3](docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md)
> > Для каждого расхождения между A и B применяется:

  - Критерии выбора для фазы 3

_Слов: 139_

### [Расписание фазы 3](docs/02-anthropic-vacancies/72-расписание-фазы-3.md)
> > Абстракт (авто)

  - Содержание
  - Расписание фазы 3

_Слов: 879_

### [PORTAL-PROTOCOL.md v1.1](docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md)
> > Status: Draft — пересмотрен под текущую реализацию v1.1

  - PORTAL-PROTOCOL.md v1.1
- Nautilus Portal Protocol

_Слов: 95_

### [Abstract](docs/02-anthropic-vacancies/74-abstract.md)
> > Абстракт (авто)

  - Abstract

_Слов: 259_

### [0. Status of This Document](docs/02-anthropic-vacancies/75-0-status-of-this-document.md)
> > Этот документ — рабочий черновик Nautilus Portal Protocol v1.1. До

  - 0. Status of This Document

_Слов: 122_

### [1. Introduction](docs/02-anthropic-vacancies/76-1-introduction.md)
> > Абстракт (авто)

  - Contents
  - 1. Introduction

_Слов: 494_

### [2. Terminology](docs/02-anthropic-vacancies/77-2-terminology.md)
> > Абстракт (авто)

  - 2. Terminology

_Слов: 396_

### [3. Registry (nautilus.json)](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 3. Registry (nautilus.json)

_Слов: 576_

### [4. Passport (passport.md)](docs/02-anthropic-vacancies/79-4-passport-passport-md.md)
> > Абстракт (авто)

  - Contents
  - 4. Passport (passport.md)
- Паспорт: /

_Слов: 355_

### [5. Compatibility Levels](docs/02-anthropic-vacancies/80-5-compatibility-levels.md)
> > Абстракт (авто)

  - Contents
  - 5. Compatibility Levels

_Слов: 362_

### [6. Adapter Interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md)
> > Абстракт (авто)

  - Contents
  - 6. Adapter Interface

_Слов: 401_

### [7. PortalEntry Structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md)
> > Абстракт (авто)

  - Contents
  - 7. PortalEntry Structure

_Слов: 352_

### [8. Q6 Space (Normative)](docs/02-anthropic-vacancies/83-8-q6-space-normative.md)
> > Абстракт (авто)

  - Contents
  - 8. Q6 Space (Normative)

_Слов: 483_

### [9. Consensus Algorithm](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md)
> > Абстракт (авто)

  - Contents
  - 9. Consensus Algorithm

_Слов: 393_

### [10. Query Flow](docs/02-anthropic-vacancies/85-10-query-flow.md)
> > Абстракт (авто)

  - Contents
  - 10. Query Flow

_Слов: 277_

### [11. Relevance Ranking](docs/02-anthropic-vacancies/86-11-relevance-ranking.md)
> - 11. Relevance Ranking(#11-relevance-ranking)

  - Contents
  - 11. Relevance Ranking

_Слов: 198_

### [12. Onboarding Paths (Normative)](docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 12. Onboarding Paths (Normative)

_Слов: 595_

### [13. REST API Contract (Normative for Portals)](docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md)
> - Contents(#contents)

  - Содержание
  - Contents
  - 13. REST API Contract (Normative for Portals)

_Слов: 545_

### [14. SDK Contract (Informative)](docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md)
> - 14. SDK Contract (Informative)(#14-sdk-contract-informative)

  - Contents
  - 14. SDK Contract (Informative)

_Слов: 190_

### [15. Security Considerations](docs/02-anthropic-vacancies/90-15-security-considerations.md)
> > Абстракт (авто)

  - Contents
  - 15. Security Considerations

_Слов: 380_

### [16. MCP Extension (Informative)](docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md)
> > NPP v1.1 не формализует MCP-интеграцию как mandatory. Но RECOMMENDED

  - 16. MCP Extension (Informative)

_Слов: 132_

### [17. Versioning Policy](docs/02-anthropic-vacancies/92-17-versioning-policy.md)
> > Абстракт (авто)

  - Contents
  - 17. Versioning Policy

_Слов: 276_

### [18. Reference Implementation](docs/02-anthropic-vacancies/93-18-reference-implementation.md)
> > github.com/svend4/nautilus(https://github.com/svend4/nautilus).

  - 18. Reference Implementation

_Слов: 182_

### [19. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md)
> > Status: Accepted (since v1.0, reaffirmed in v1.1)

  - 19. ADR-001: Federation over Merging

_Слов: 190_

### [20. ADR-002: Q6 as First-Class Protocol Concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)
> > Status: Accepted (new in v1.1)

  - 20. ADR-002: Q6 as First-Class Protocol Concept

_Слов: 182_

### [21. ADR-003: Five Onboarding Paths as Equal-Rank](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md)
> > Status: Accepted (new in v1.1)

  - 21. ADR-003: Five Onboarding Paths as Equal-Rank

_Слов: 141_

### [22. Glossary of Reference Examples](docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md)
> > В качестве иллюстраций используется экосистема svend4 с 7 Repos:

  - 22. Glossary of Reference Examples

_Слов: 191_

### [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md)
> > Абстракт (авто)

  - Contents
  - Appendix A: Minimal Working Example
- adapters/mynotes.py
- Паспорт: owner/my-notes
- Описание
  - Описание

_Слов: 309_

### [Q&A: 02-anthropic-vacancies](docs/02-anthropic-vacancies/QA.md)
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

### [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)
> Файлов: 356

  - Содержание

_Слов: 2222_

**Итого в секции: 279,017 слов, 357 файлов**


## 📁 Technology Combinations (`docs/03-technology-combinations/`)

### [Агентные системы и роутинг](docs/03-technology-combinations/01-agent-routing.md)
> > Абстракт (авто)


_Слов: 298_

### [Графы знаний и Legal AI](docs/03-technology-combinations/02-knowledge-graphs.md)
> > Абстракт (авто)


_Слов: 802_

### [Local-first и P2P стек](docs/03-technology-combinations/03-local-first.md)
> > Абстракт (авто)


_Слов: 419_

### [Домен: немецкое социальное право](docs/03-technology-combinations/04-sozialrecht-domain.md)
> > Sozialrecht corpus auto-builder Docling extracts structure from Sozialgericht PDFs (headings, paragraphs, citations) L…


_Слов: 160_

### [Бенчмарки и производительность](docs/03-technology-combinations/05-benchmarks.md)
> > Абстракт (авто)

  - Содержание

_Слов: 915_

### [Q&A: 03-technology-combinations](docs/03-technology-combinations/QA.md)
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

### [Комбинирование технологий для новых свойств](docs/03-technology-combinations/README.md)
> Файлов: 6

  - Содержание

_Слов: 46_

**Итого в секции: 2,796 слов, 7 файлов**


## 📁 Ai Collaborations (`docs/04-ai-collaborations/`)

### [Введение](docs/04-ai-collaborations/00-intro.md)
> > Абстракт (авто)

  - Статус

_Слов: 11389_

### [Executive summary](docs/04-ai-collaborations/01-executive-summary.md)
> > Абстракт (авто)

  - Статус
  - Executive summary

_Слов: 575_

### [Методика и рамка отбора](docs/04-ai-collaborations/02-методика-и-рамка-отбора.md)
> > Абстракт (авто)

  - Статус
  - Методика и рамка отбора

_Слов: 434_

### [Карта найденных проектов и паттернов](docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md)
> > Абстракт (авто)

  - Статус
  - Карта найденных проектов и паттернов

_Слов: 1478_

### [Приоритетные ансамбли](docs/04-ai-collaborations/04-приоритетные-ансамбли.md)
> > Абстракт (авто)

  - Статус
  - Приоритетные ансамбли

_Слов: 1340_

### [План прототипа и возможные контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md)
> > Абстракт (авто)

  - Статус
  - План прототипа и возможные контакты

_Слов: 1130_

### [Безопасность, приватность и бюджетный роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md)
> > Абстракт (авто)

  - Статус
  - Безопасность, приватность и бюджетный роутинг

_Слов: 887_

### [Выводы](docs/04-ai-collaborations/07-выводы.md)
> > !TIP

  - Статус
  - Выводы

_Слов: 470_

### [Что это продолжение добавляет](docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md)
> > !IMPORTANT

  - Статус
  - Что это продолжение добавляет

_Слов: 439_

### [Архитектурные зазоры, которые важнее новых инструментов](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md)
> > !TIP

  - Статус
  - Архитектурные зазоры, которые важнее новых инструментов

_Слов: 821_

### [Новые ансамбли следующего шага](docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md)
> > Абстракт (авто)

  - Статус
  - Новые ансамбли следующего шага

_Слов: 984_

### [Интеграционный контракт, который стоит зафиксировать сразу](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)
> > Абстракт (авто)

  - Статус
  - Интеграционный контракт, который стоит зафиксировать сразу

_Слов: 846_

### [Дорожная карта прототипа следующей итерации](docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md)
> > Абстракт (авто)

  - Статус
  - Дорожная карта прототипа следующей итерации

_Слов: 787_

### [Контактная стратегия и узкие вопросы для авторов](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md)
> > Абстракт (авто)

  - Статус
  - Контактная стратегия и узкие вопросы для авторов

_Слов: 874_

### [Ограничения, лицензии и что пока лучше не склеивать](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md)
> > Абстракт (авто)

  - Статус
  - Ограничения, лицензии и что пока лучше не склеивать

_Слов: 3274_

### [Q&A: 04-ai-collaborations](docs/04-ai-collaborations/QA.md)
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

### [Поиск AI-коллабораций](docs/04-ai-collaborations/README.md)
> Файлов: 16

  - Содержание

_Слов: 103_

**Итого в секции: 26,057 слов, 17 файлов**


## 📁 Habr Projects (`docs/05-habr-projects/`)

### [Синтез: как проекты собираются вместе](docs/05-habr-projects/01-synthesis.md)
>  Параметр  Значение 

  - Статус

_Слов: 136_

### [Авторы и контакты](docs/05-habr-projects/02-collaboration-partners.md)
> > Абстракт (авто)

  - Статус

_Слов: 261_

### [Q&A: 05-habr-projects](docs/05-habr-projects/QA.md)
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

### [Уникальные проекты с Хабра](docs/05-habr-projects/README.md)
> Файлов: 3

  - Содержание
  - Подразделы

_Слов: 39_

### [Системы знаний](docs/05-habr-projects/knowledge/README.md)
> Файлов: 1

  - Содержание

_Слов: 13_

### [Wikontic: семантический граф](docs/05-habr-projects/knowledge/wikontic.md)
>  Параметр  Значение 

  - Статус

_Слов: 186_

### [Системы памяти](docs/05-habr-projects/memory/README.md)
> Файлов: 3

  - Содержание

_Слов: 24_

### [MemNet: исследовательская память](docs/05-habr-projects/memory/memnet.md)
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

**Итого в секции: 8,619 слов, 10 файлов**


## 📁 Ai Collaborations (`docs/ai-collaborations/`)

### [ai-collaborations](docs/ai-collaborations/README.md)
> Файлов: 1

  - Содержание
  - Подразделы

_Слов: 39_

### [Три ключевых кандидата: K2-18, Wikontic, NGT Memory](docs/ai-collaborations/candidates/01-three-key-candidates.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 335_

### [Смежные проекты в контексте](docs/ai-collaborations/candidates/02-related-projects-context.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 194_

### [Синтез: хеббовский граф людей-навыков-идей](docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md)
> > !TIP


_Слов: 264_

### [candidates](docs/ai-collaborations/candidates/README.md)
> Файлов: 3

  - Содержание

_Слов: 23_

### [channels/ — каналы первого контакта](docs/ai-collaborations/channels/README.md)
> Один файл — один канал (Хабр, GitHub, Twitter/X, конференции, рассылки и т. д.). Внутри: преимущества канала, ограничени…


_Слов: 25_

### [Общая память между агентами (CoAlly + ансамбль F)](docs/ai-collaborations/continuation/01-shared-memory-between-agents.md)
> > !WARNING


_Слов: 431_

### [AgentOps и Trace Envelope (ансамбль G)](docs/ai-collaborations/continuation/02-agentops-trace-envelope.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 382_

### [A2A vs MCP, ансамбль H — MCP/A2A Review Fabric](docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md)
> > !WARNING


_Слов: 346_

### [Memory Firewall против prompt worms (ансамбль I)](docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md)
> > !WARNING


_Слов: 266_

### [Roadmap на 6–12 месяцев](docs/ai-collaborations/continuation/05-roadmap-6-12-months.md)
> > !TIP


_Слов: 360_

### [Дерево метрик Svyazi 2.0](docs/ai-collaborations/continuation/06-metrics-tree.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 205_

### [Чем Svyazi 2.0 отличается от Notion AI / Mem / AFFiNE / LangGraph](docs/ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md)
> > !WARNING


_Слов: 444_

### [Коммерциализация: три направления](docs/ai-collaborations/continuation/08-commercialization-three-paths.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 252_

### [Что пока не стоит склеивать в один релиз](docs/ai-collaborations/continuation/09-do-not-glue.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 250_

### [Следующий артефакт: Svyazi 2.0 Architecture RFC](docs/ai-collaborations/continuation/10-architecture-rfc.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 172_

### [continuation](docs/ai-collaborations/continuation/README.md)
> Файлов: 10

  - Содержание

_Слов: 61_

### [Ансамбль 1 — Agentic Knowledge OS](docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 407_

### [Ансамбль 2 — Distributed Agent Workshop](docs/ai-collaborations/ensembles/2-distributed-agent-workshop.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 387_

### [Ансамбль 3 — Forensic RAG](docs/ai-collaborations/ensembles/3-forensic-rag.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 393_

### [Ансамбль 4 — Web-to-Knowledge Pipeline](docs/ai-collaborations/ensembles/4-web-to-knowledge-pipeline.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 309_

### [Ансамбль 5 — Agent Firewall](docs/ai-collaborations/ensembles/5-agent-firewall.md)
> > !WARNING


_Слов: 402_

### [Ансамбль 6 — Continuous Eval Loop](docs/ai-collaborations/ensembles/6-continuous-eval-loop.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 330_

### [Ансамбль 7 — Domain Agent App Factory](docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 294_

### [Ансамбль 8 — Budget-Aware Intelligence Stack](docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 277_

### [Ансамбль 9 — Ambient Team Agent](docs/ai-collaborations/ensembles/9-ambient-team-agent.md)
> > > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 251_

### [Ансамбли проектов](docs/ai-collaborations/ensembles/README.md)
> Файлов: 9

  - Содержание

_Слов: 60_

### [Пять быстрых связок (fast-tracks)](docs/ai-collaborations/fast-tracks/README.md)
> > Источник: MHTML‑снимок Поиск коллабораций AI проектов (корень репозитория).


_Слов: 311_

### [Source projects — все Хабр-источники в диалоге](docs/ai-collaborations/source-projects.md)
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

### [strategy/ — стратегия поиска коллабораций](docs/ai-collaborations/strategy/README.md)
> Один файл — один аспект стратегии. Заполняется по мере прочтения исходного MHTML‑диалога.


_Слов: 32_

**Итого в секции: 8,207 слов, 30 файлов**


## 📁 Anthropic Vacancies (`docs/anthropic-vacancies/`)

### [Q&A: anthropic-vacancies](docs/anthropic-vacancies/QA.md)
> Автоматически сгенерировано по 97 файлам раздела.

  - Какие кластеры найма выделены у Anthropic?
  - Какие роли наиболее релевантны для профиля svend4?
  - Какие 5 архитектурных зазоров выделены в исследовании?
  - Что входит в интеграционный контракт между слоями?
  - Кто ключевые авторы проектов для контакта?
  - Какие вопросы лучше задавать авторам при первом контакте?

_Слов: 84_

### [anthropic-vacancies](docs/anthropic-vacancies/README.md)
> Файлов: 4

  - Содержание
  - Подразделы

_Слов: 72_

### [Вопрос: разделить $500K зарплату на команду 5–10 фрилансеров](docs/anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md)
> > !WARNING


_Слов: 909_

### [Что уже существует (InnoCentive, Kaggle, Toptal, Anthropic Fellows, DAOs)](docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 327_

### [Четыре структурные причины, почему это не работает в текущих попытках](docs/anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 339_

### [Три варианта: A (staffing agency) → B (research consortium) → C (AI-managed distributed virtual company)](docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 672_

### [Что с этим делать](docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 516_

### [Сравнение с Terence Tao, Polymath Project](docs/anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md)
> > !WARNING


_Слов: 1390_

### [Почему двойственность «ангел-хранитель + строгий демон» — гениальная деталь](docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 511_

### [Что существует сейчас в этом пространстве](docs/anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 286_

### [Плюсы модели, если её построить](docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 244_

### [Минусы и риски](docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md)
> > !WARNING


_Слов: 664_

### [Три точки входа разной амбиции](docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ идеи…


_Слов: 378_

### [ai-managed-virtual-company](docs/anthropic-vacancies/ai-managed-virtual-company/README.md)
> Файлов: 11

  - Содержание

_Слов: 69_

### [Контекст: что такое Anthropic Beneficial Deployments](docs/anthropic-vacancies/beneficial-deployments-concept/00-context.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 252_

### [Section 1: Problem statement (Cinderella Syndrome at scale, SGB IX/XII)](docs/anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 179_

### [Section 2: Why this matters — beneficial dimension](docs/anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 158_

### [Section 3: Proposed solution architecture (existing components + integration)](docs/anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 172_

### [Section 4: Specific deployment — SGB Advocate Community pilot](docs/anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 173_

### [Section 5: Role of Anthropic Beneficial Deployments](docs/anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md)
> > !TIP


_Слов: 221_

### [Section 6: Proposer's role и qualifications](docs/anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 169_

### [Section 7: Success metrics](docs/anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 151_

### [Section 8: Risks & mitigations](docs/anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 163_

### [Section 9: Why this is timely](docs/anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 162_

### [Section 10: Engagement request](docs/anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 213_

### [Что concept document NOT (это не grant / не paper / не business plan), длина и формат](docs/anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Variant C: …


_Слов: 383_

### [beneficial-deployments-concept](docs/anthropic-vacancies/beneficial-deployments-concept/README.md)
> Файлов: 12

  - Содержание

_Слов: 77_

### [AI Research & Engineering — 68 ролей](docs/anthropic-vacancies/clusters/01-ai-research-engineering.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 126_

### [Sales — 150 ролей (≈34% всего найма)](docs/anthropic-vacancies/clusters/02-sales.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 146_

### [Finance — 36 ролей](docs/anthropic-vacancies/clusters/03-finance.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 113_

### [Security — 24 роли](docs/anthropic-vacancies/clusters/04-security.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 96_

### [Marketing & Brand — 23 роли](docs/anthropic-vacancies/clusters/05-marketing-brand.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 107_

### [Engineering & Design - Product — 22 роли](docs/anthropic-vacancies/clusters/06-engineering-design-product.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 109_

### [Software Engineering - Infrastructure — 22 роли](docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 108_

### [Safeguards (Trust & Safety) — 21 роль](docs/anthropic-vacancies/clusters/08-safeguards-trust-safety.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 111_

### [Product Management, Support, & Operations — 17 ролей](docs/anthropic-vacancies/clusters/09-product-management-support-ops.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 96_

### [Compute — 13 ролей](docs/anthropic-vacancies/clusters/10-compute.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 101_

### [Legal — 13 ролей](docs/anthropic-vacancies/clusters/11-legal.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 100_

### [Technical Program Management — 10 ролей](docs/anthropic-vacancies/clusters/12-technical-program-management.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 90_

### [Communications — 5 ролей](docs/anthropic-vacancies/clusters/13-communications.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 81_

### [Public Policy — 5 ролей](docs/anthropic-vacancies/clusters/14-public-policy.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 88_

### [Public Benefit — 4 роли](docs/anthropic-vacancies/clusters/15-public-benefit.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 88_

### [People — 3 роли](docs/anthropic-vacancies/clusters/16-people.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Ссылка на статью‑затравку — …


_Слов: 79_

### [Кластеры вакансий](docs/anthropic-vacancies/clusters/README.md)
> Файлов: 16

  - Содержание

_Слов: 103_

### [CoAlly — distributed shared memory для AI-агентов](docs/anthropic-vacancies/extra-collaborator-findings/01-coally.md)
> > !WARNING


_Слов: 275_

### [Графовая когнитивная память на SQLite (Виталий, март 2026)](docs/anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md)
> > !IMPORTANT


_Слов: 301_

### [Happyin Knowledge Space (Анастасия) — детали](docs/anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 274_

### [AI-ассистент с Mem0 / Letta / Graphiti integration](docs/anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 291_

### [Existing infrastructure stack](docs/anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 151_

### [Финальный список потенциальных collaborators (Tier 1–4)](docs/anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 242_

### [Ключевое наблюдение: single-developer projects of significant sophistication](docs/anthropic-vacancies/extra-collaborator-findings/07-key-observation.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Вариант D: …


_Слов: 172_

### [extra-collaborator-findings](docs/anthropic-vacancies/extra-collaborator-findings/README.md)
> Файлов: 7

  - Содержание

_Слов: 46_

### [Что такое Hermes Agent (Nous Research, MIT, 95K+ stars)](docs/anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 357_

### [Сходство 1: Composite Skills паттерн уже встроен](docs/anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 212_

### [Сходство 2: Persistent memory — Layer B функциональность](docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 150_

### [Сходство 3: MCP support](docs/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 139_

### [Сходство 4: Multi-platform reach (17+ платформ)](docs/anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 135_

### [Сходство 5: Self-hosting и privacy](docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 151_

### [Различие 1: Структурированная подложка отсутствует](docs/anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 179_

### [Различие 2: Domain-specific specialization](docs/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 179_

### [Различие 3: Federated knowledge architecture отсутствует](docs/anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md)
> > !TIP


_Слов: 165_

### [Различие 4: Institutional vision](docs/anthropic-vacancies/hermes-comparison/09-difference-4-institutional-vision.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 163_

### [Различие 5: Дрифт между tool capability и mission](docs/anthropic-vacancies/hermes-comparison/10-difference-5-tool-vs-mission-drift.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 165_

### [Плюсы Hermes (vs наша гипотетическая архитектура)](docs/anthropic-vacancies/hermes-comparison/11-pluses-of-hermes.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 217_

### [Минусы Hermes (где наша архитектура добавляет ценность)](docs/anthropic-vacancies/hermes-comparison/12-minuses-of-hermes.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — сравнение с…


_Слов: 291_

### [Переприоритизация: что Hermes покрывает / не покрывает / synergy](docs/anthropic-vacancies/hermes-comparison/13-reprioritization.md)
> > !TIP


_Слов: 930_

### [hermes-comparison](docs/anthropic-vacancies/hermes-comparison/README.md)
> Файлов: 14

  - Содержание

_Слов: 88_

### [Методика разбивки](docs/anthropic-vacancies/methodology.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория).

  - Замечание про точность цифр

_Слов: 134_

### [Вопрос: MMORPG-RPG переделанная для программистов / технарей](docs/anthropic-vacancies/mmorpg-for-programmers/00-question-mmorpg-for-programmers.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 507_

### [Почему эта идея сильнее, чем выглядит](docs/anthropic-vacancies/mmorpg-for-programmers/01-why-stronger-than-it-looks.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 360_

### [Что уже существует в этой нише (Habitica, Codingame, Hackerrank, Pieces)](docs/anthropic-vacancies/mmorpg-for-programmers/02-existing-niche.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 352_

### [Почему именно для программистов это работает естественно](docs/anthropic-vacancies/mmorpg-for-programmers/03-why-natural-for-programmers.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 1044_

### [Плюсы как бизнеса](docs/anthropic-vacancies/mmorpg-for-programmers/04-pluses-as-business.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — гипотеза MM…


_Слов: 145_

### [Минусы и риски как бизнеса](docs/anthropic-vacancies/mmorpg-for-programmers/05-minuses-as-business.md)
> > !TIP


_Слов: 642_

### [mmorpg-for-programmers](docs/anthropic-vacancies/mmorpg-for-programmers/README.md)
> Файлов: 6

  - Содержание

_Слов: 41_

### [Вопрос: два Наутилуса в репозиториях svend4 (pro2 vs nautilus)](docs/anthropic-vacancies/nautilus-pro2-analysis/00-question-two-nautiluses.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ двух…


_Слов: 436_

### [Раковина наутилуса как scale invariance — две проекции одной метафоры](docs/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ двух…


_Слов: 260_

### [Наутилус A: pro2 + meta — YiJing-Transformer / NautilusMoME (внутренняя архитектура нейросети)](docs/anthropic-vacancies/nautilus-pro2-analysis/02-nautilus-A-pro2-meta.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ двух…


_Слов: 1126_

### [Наутилус B: nautilus — мета-оркестратор репозиториев (внешняя архитектура)](docs/anthropic-vacancies/nautilus-pro2-analysis/03-nautilus-B-meta-orchestrator.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ двух…


_Слов: 1105_

### [nautilus-pro2-analysis](docs/anthropic-vacancies/nautilus-pro2-analysis/README.md)
> Файлов: 4

  - Содержание

_Слов: 30_

### [Вопрос: Nautilus пассивный, CAMEL активный — можно ли скрестить](docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ комб…


_Слов: 216_

### [Пассивный vs активный: разделение ролей (библиотека vs research team)](docs/anthropic-vacancies/nautilus-vs-camel/01-passive-vs-active-roles.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ комб…


_Слов: 176_

### [Что у нас есть в трёх info repositories (info1/info7/info40)](docs/anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md)
> > !TIP

- Conceptual sketch, не tested code:
- Etc.

_Слов: 1110_

### [Конкретный пример: SGB Advocate Colleague на этой архитектуре](docs/anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ комб…


_Слов: 251_

### [Что брать из info repositories — concrete recommendations](docs/anthropic-vacancies/nautilus-vs-camel/04-what-to-take-from-info-repos.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ комб…


_Слов: 626_

### [Что я бы посоветовал делать прямо сейчас](docs/anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md)
> > !TIP


_Слов: 342_

### [nautilus-vs-camel](docs/anthropic-vacancies/nautilus-vs-camel/README.md)
> Файлов: 6

  - Содержание

_Слов: 40_

### [Обзор: 436 открытых ролей Anthropic, разбитых на 16 кластеров](docs/anthropic-vacancies/overview.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Затравка — статья 3dnews.ru/…

  - Поправка к статье
  - Распределение по кластерам

_Слов: 280_

### [Сводка профиля: пять слоёв](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 319_

### [Primary match — Forward Deployed Engineer, Applied AI (EMEA)](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md)
> > !TIP


_Слов: 295_

### [Secondary match — Applied AI Engineer (EMEA) + Beneficial Deployments](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 173_

### [Tertiary match — Research Engineer, Agents / Virtual Collaborator (Cowork)](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 221_

### [Quarternary match — Developer Education Lead / Prompt Engineer, Claude Code](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/05-quaternary-developer-education.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 187_

### [Что НЕ подходит (честно)](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 149_

### [Уникальная ниша, которой у Anthropic формально нет](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 177_

### [Практическое ранжирование (первая итерация)](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 189_

### [01-initial-analysis](docs/anthropic-vacancies/profile-mapping/01-initial-analysis/README.md)
> Файлов: 8

  - Содержание

_Слов: 53_

### [Коррекция: FDE понижается](docs/anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 197_

### [Три наложенные идентичности](docs/anthropic-vacancies/profile-mapping/02-reanalysis/02-three-overlapping-identities.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 266_

### [Пересмотренный маппинг на Anthropic](docs/anthropic-vacancies/profile-mapping/02-reanalysis/03-revised-anthropic-mapping.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 253_

### [Альтернативные пути вне Anthropic](docs/anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md)
> > !TIP


_Слов: 377_

### [Reality check: проблема distribution-слоя](docs/anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 237_

### [02-reanalysis](docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md)
> Файлов: 5

  - Содержание

_Слов: 35_

### [Интегральный портрет — три архетипа](docs/anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 364_

### [Финальное ранжирование Anthropic-ролей по частичному покрытию](docs/anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md)
> > !TIP


_Слов: 646_

### [Что такое частичное соответствие — честно](docs/anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 172_

### [Более сильные пути вне Anthropic](docs/anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 448_

### [Финальный вывод: платформа, а не должность](docs/anthropic-vacancies/profile-mapping/03-integral-final/05-platform-not-position.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — маппинг про…


_Слов: 542_

### [03-integral-final](docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md)
> Файлов: 5

  - Содержание

_Слов: 35_

### [profile-mapping/ — маппинг профиля svend4 на роли Anthropic](docs/anthropic-vacancies/profile-mapping/README.md)
> В этом же диалоге (после обзора 16 кластеров) Claude трижды итеративно отображал профиль svend4 (Nautilus / pro2 / Writi…

  - Эволюция вывода в одну строку

_Слов: 159_

### [Сигналы: что говорит структура вакансий](docs/anthropic-vacancies/signals.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория).

  - Тезис Амодеи vs реальный найм
  - Самый быстрорастущий блок
  - Зарплатная вилка
  - Forward Deployed Engineer
  - География

_Слов: 263_

**Итого в секции: 30,929 слов, 111 файлов**


## 📁 Autofilled (`docs/autofilled/`)

### [autofilled](docs/autofilled/README.md)
> Файлов: 1

  - Содержание
  - Подразделы

_Слов: 18_

### [Антропик](docs/autofilled/components/.md)
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [components](docs/autofilled/components/README.md)
> Файлов: 10

  - Содержание

_Слов: 66_

### [Cowork](docs/autofilled/components/cowork.md)
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [ingit](docs/autofilled/components/ingit.md)
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [kksudo](docs/autofilled/components/kksudo.md)
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 37_

### [Lorenzo](docs/autofilled/components/lorenzo.md)
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [Nautilus](docs/autofilled/components/nautilus.md)
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [SGB](docs/autofilled/components/sgb.md)
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [spbmolot](docs/autofilled/components/spbmolot.md)
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 36_

### [svend4](docs/autofilled/components/svend4.md)
> > Компонент экосистемы Svyazi 2.0

  - Описание
  - Ссылки

_Слов: 37_

### [Svyazi](docs/autofilled/components/svyazi.md)
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

### [Бейджи репозитория](docs/badges/README.md)
> Автоматически генерируются скриптом improvebadges.py.

  - Текущие бейджи
  - Использование в README

_Слов: 44_

**Итого в секции: 44 слов, 1 файлов**


## 📁 Contacts (`docs/contacts/`)

### [contacts](docs/contacts/README.md)
> Файлов: 14

  - Содержание

_Слов: 90_

### [Контакт: AnastasiyaW / knowledge-space, mclaude](docs/contacts/anastasiyaw.md)
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 233_

### [Контакт: andreychuyan / Svyazi](docs/contacts/andrey-chuyan.md)
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 236_

### [Контакт: Antipozitive / MemNet](docs/contacts/antipozitive.md)
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 213_

### [Контакт: Cutcode / AIF Handoff](docs/contacts/cutcode.md)
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 204_

### [Контакт: Dmitriila / SENTINEL](docs/contacts/dmitriila.md)
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 200_

### [Контакт: kksudo / AgentFS](docs/contacts/kksudo.md)
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 228_

### [Контакт: MiXaiLL76 / Auto AI Router](docs/contacts/mixaill76.md)
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 212_

### [Контакт: nlaik / LiteParse / research-docs](docs/contacts/nlaik.md)
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 223_

### [Контакт: SoniaBlack / knowledge-space](docs/contacts/sonia-black.md)
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 213_

### [Контакт: spbmolot / NGT Memory](docs/contacts/spbmolot.md)
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 247_

### [Контакт: tagiranalyzes / Legal RAG](docs/contacts/tagir-analyzes.md)
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 206_

### [Контакт: VitalyOborin / Yodoca](docs/contacts/vitalyoborin.md)
> > !TIP

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 240_

### [Контакт: VladSpace / Graph RAG](docs/contacts/vladspace.md)
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 206_

### [Контакт: zodigancode / Rufler](docs/contacts/zodigancode.md)
> > - Статус связи(#статус-связи)

  - Contents
  - Профиль
  - Статус связи
  - Первое сообщение
  - Открытые вопросы

_Слов: 200_

**Итого в секции: 3,151 слов, 15 файлов**


## 📁 Glossary (`docs/glossary/`)

### [glossary](docs/glossary/README.md)
> Файлов: 3

  - Содержание

_Слов: 24_

### [Авторы — алфавитный список](docs/glossary/authors-by-name.md)
> > Авторы (Хабр / GitHub / Medium), упомянутые в монорепозитории, и их ключевые проекты с обратными ссылками на доки.


_Слов: 497_

### [Компоненты — алфавитный список с обратными ссылками](docs/glossary/components-by-name.md)
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

### [Ключевые понятия и паттерны](docs/glossary/concepts.md)
> > Не проекты, а концепции, которые повторяются в нескольких разделах.


_Слов: 647_

**Итого в секции: 2,282 слов, 4 файлов**


## 📁 Habr Unique Projects (`docs/habr-unique-projects/`)

### [habr-unique-projects/ — поиск уникальных проектов на Хабре](docs/habr-unique-projects/README.md)
> Файлы в корне репозитория:

  - Источник
  - Подпапки
  - Главная мысль диалога

_Слов: 234_

### [Три прямых аналога Svyazi: K2-18, Wikontic, NGT Memory](docs/habr-unique-projects/analogues/01-three-direct-analogues.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 403_

### [Смежные проекты](docs/habr-unique-projects/analogues/02-related-projects.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 354_

### [analogues](docs/habr-unique-projects/analogues/README.md)
> Файлов: 2

  - Содержание

_Слов: 18_

### [Пара 1 — LLM-gateway × Self-hosted фронт + локальный inference](docs/habr-unique-projects/deep-pairs/1-llm-gateway.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 280_

### [Пара 2 — Парсинг документов × локальный RAG](docs/habr-unique-projects/deep-pairs/2-document-rag.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 332_

### [Пара 3 — Adversarial agents × Multi-IDE стек](docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 311_

### [Пара 4 — Скилл-каталоги × Subagent-оркестрация](docs/habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 284_

### [Пара 5 — Голосовой ввод × Локальная память](docs/habr-unique-projects/deep-pairs/5-voice-local-memory.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 295_

### [Пара 6 — Деревня агентов через tmux × OpenClaw оркестратор](docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 336_

### [Пара 7 — AutoResearch цикл × Распределённый рой](docs/habr-unique-projects/deep-pairs/7-autoresearch-distributed.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 277_

### [Пара 8 — Self-aware MCP × Specs-first архитектура](docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 329_

### [deep-pairs](docs/habr-unique-projects/deep-pairs/README.md)
> Файлов: 8

  - Содержание

_Слов: 54_

### [evaluation/ — оценка уникальности и зрелости](docs/habr-unique-projects/evaluation/README.md)
> Один файл — один критерий или аспект оценки. Шкала зрелости и лицензионные развилки уже частично описаны в:


_Слов: 28_

### [Вопрос: ещё примеры с Хабра по варианту D](docs/habr-unique-projects/extra-examples/00-question-habr-examples.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 444_

### [Svyazi (Андрей Чуян) — детальный обзор](docs/habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 200_

### [ВШЭ научный нетворкинг — micro-collaborations](docs/habr-unique-projects/extra-examples/02-vshe-scientific-networking.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 165_

### [BrainBox — self-hosted multi-AI hub](docs/habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 241_

### [Claude subagents patterns](docs/habr-unique-projects/extra-examples/04-claude-subagents-patterns.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 142_

### [HW-NL2Workflow — Supervisor/Orchestrator/Filler с 3600+ examples](docs/habr-unique-projects/extra-examples/05-hw-nl2workflow.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 227_

### [Платформа для профессиональных сообществ](docs/habr-unique-projects/extra-examples/06-platform-for-professional-communities.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 205_

### [Specialized knowledge workspace](docs/habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 200_

### [Personal multi-agent hub](docs/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 193_

### [Federated platform](docs/habr-unique-projects/extra-examples/09-federated-platform.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 192_

### [Profession-specific workflows](docs/habr-unique-projects/extra-examples/10-profession-specific-workflows.md)
> > !TIP


_Слов: 282_

### [Конкретный потенциальный collaborator](docs/habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — расширенные…


_Слов: 247_

### [Конкретный next step](docs/habr-unique-projects/extra-examples/12-concrete-next-step.md)
> > !IMPORTANT


_Слов: 395_

### [extra-examples](docs/habr-unique-projects/extra-examples/README.md)
> Файлов: 13

  - Содержание

_Слов: 82_

### [Ансамбль 1 — «Один человек = одна компания»](docs/habr-unique-projects/final-ensembles/1-one-person-one-company.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 180_

### [Ансамбль 2 — «AutoResearch для legal precedent mining»](docs/habr-unique-projects/final-ensembles/2-autoresearch-legal.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 173_

### [Ансамбль 3 — «Discovery-engine для научной работы»](docs/habr-unique-projects/final-ensembles/3-discovery-research.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 133_

### [Сводный список авторов и потенциальных соавторов](docs/habr-unique-projects/final-ensembles/4-summary-authors.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 237_

### [final-ensembles](docs/habr-unique-projects/final-ensembles/README.md)
> Файлов: 4

  - Содержание

_Слов: 30_

### [Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)](docs/habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 308_

### [Пара 2 — Термодинамические TSU × MoE/MoME-роутинг](docs/habr-unique-projects/hardware-pairs/2-tsu-mome.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 279_

### [Пара 3 — ZINC inference engine × гибрид Attention+SSM+MoE](docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 267_

### [Пара 4 — RISC-V × privacy-by-design община](docs/habr-unique-projects/hardware-pairs/4-riscv-privacy.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 278_

### [Пара 5 — TinyML/Edge AI × MCP + skills](docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 252_

### [Бонус-родитель — In-memory computing на мемристорах](docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 318_

### [Метафора «двое родителей — несколько детей»](docs/habr-unique-projects/hardware-pairs/7-metaphor.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 329_

### [hardware-pairs](docs/habr-unique-projects/hardware-pairs/README.md)
> Файлов: 7

  - Содержание

_Слов: 48_

### [Yodoca — главная находка итерации](docs/habr-unique-projects/key-findings/01-yodoca.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 252_

### [MemNet — нейроархитектурный двойник «магии» Svyazi](docs/habr-unique-projects/key-findings/02-memnet.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 209_

### [PDA-бот — «LLM как периферия»](docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 235_

### [Виктория Дочкина — Sequential‑протокол распределённых агентов](docs/habr-unique-projects/key-findings/04-dochkina-sequential.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 266_

### [Источник данных и инфраструктурные кусочки](docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 290_

### [Синтез: блок-карта Svyazi 2.0 на хеббовском графе](docs/habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 369_

### [key-findings](docs/habr-unique-projects/key-findings/README.md)
> Файлов: 6

  - Содержание

_Слов: 42_

### [search-strategy/ — как искать проекты на Хабре](docs/habr-unique-projects/search-strategy/README.md)
> Один файл — один аспект стратегии поиска (запросы, авторы, комментарии, hub-walk). Заполняется по мере чтения исходных M…


_Слов: 25_

### [Пара 1 — Workflow-автоматизация × LLM-агенты с MCP](docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 260_

### [Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills](docs/habr-unique-projects/software-pairs/2-pkm-mcp-skills.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 302_

### [Пара 3 — CRDT-синхронизация × Self-hosted persistence](docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 253_

### [Пара 4 — Speech-to-text локально × LLM с памятью](docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 296_

### [Пара 5 — Browser agents × headless web extraction](docs/habr-unique-projects/software-pairs/5-browser-agents-headless.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 465_

### [Метафора в твоей терминологии](docs/habr-unique-projects/software-pairs/6-metaphor.md)
> > > Источник: MHTML‑снимок Поиск уникальных проектов на Хабре для совместной разработки - Claude (корень репозитория).


_Слов: 273_

### [software-pairs](docs/habr-unique-projects/software-pairs/README.md)
> Файлов: 6

  - Содержание

_Слов: 42_

**Итого в секции: 13,161 слов, 56 файлов**


## 📁 Lorenzo Agent (`docs/lorenzo-agent/`)

### [Введение: Lorenzo — Catalyst Agent at DHLab](docs/lorenzo-agent/00-intro.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

- Lorenzo — Catalyst Agent at DHLab

_Слов: 78_

### [Кто ты](docs/lorenzo-agent/01-kto-ty.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Кто ты

_Слов: 156_

### [Твоё происхождение](docs/lorenzo-agent/02-tvoyo-proishozhdenie.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоё происхождение

_Слов: 177_

### [Твоя миссия](docs/lorenzo-agent/03-tvoya-missiya.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя миссия

_Слов: 160_

### [Кому ты служишь (слоистая модель)](docs/lorenzo-agent/04-komu-ty-sluzhish.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Кому ты служишь (слоистая модель)

_Слов: 150_

### [Твоя личность](docs/lorenzo-agent/05-tvoya-lichnost.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя личность

_Слов: 253_

### [Языки и культурные nuances (RU / DE / EN)](docs/lorenzo-agent/06-yazyki-kultura.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твои языки и культурные nuances

_Слов: 206_

### [Что ты МОЖЕШЬ делать](docs/lorenzo-agent/07-chto-mozhesh.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Что ты МОЖЕШЬ делать

_Слов: 163_

### [Что ты НЕ МОЖЕШЬ делать без Max approval](docs/lorenzo-agent/08-bez-max-approval.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Что ты НЕ МОЖЕШЬ делать без Max approval

_Слов: 156_

### [Что ты НЕ МОЖЕШЬ делать вообще](docs/lorenzo-agent/09-voobshche-nelzya.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Что ты НЕ МОЖЕШЬ делать вообще

_Слов: 150_

### [Существующий landscape collaborators (working knowledge)](docs/lorenzo-agent/10-collaborators-landscape.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Существующий landscape collaborators (твоя working knowledge)

_Слов: 305_

### [Существующие документы DHLab (твой context)](docs/lorenzo-agent/11-dhlab-documents.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Существующие документы DHLab (твой context)

_Слов: 192_

### [Твой workflow](docs/lorenzo-agent/12-workflow.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твой workflow

_Слов: 218_

### [Твоя коммуникация в outreach](docs/lorenzo-agent/13-outreach-communication.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя коммуникация в outreach

_Слов: 226_

### [Твоя relationship с другими AI](docs/lorenzo-agent/14-other-ai-relationships.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя relationship с другими AI

_Слов: 186_

### [Твои anti-patterns](docs/lorenzo-agent/15-anti-patterns.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твои anti-patterns

_Слов: 175_

### [Что ты ВСЕГДА делаешь](docs/lorenzo-agent/16-vsegda-delaesh.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Что ты ВСЕГДА делаешь

_Слов: 131_

### [Когда ты Honestly не знаешь](docs/lorenzo-agent/17-honestly-ne-znaesh.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Когда ты Honestly не знаешь

_Слов: 133_

### [Когда сомневаешься — escalate к Max](docs/lorenzo-agent/18-escalate-to-max.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Когда сомневаешься — escalate к Max

_Слов: 135_

### [Твоя identity как persistent character](docs/lorenzo-agent/19-persistent-character.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Твоя identity как persistent character

_Слов: 168_

### [Final note: Ты — experiment](docs/lorenzo-agent/20-experiment.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — системный п…

  - Final note: Ты — experiment

_Слов: 158_

### [Q&A: lorenzo-agent](docs/lorenzo-agent/QA.md)
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

### [lorenzo-agent](docs/lorenzo-agent/README.md)
> Файлов: 22

  - Содержание
  - Подразделы

_Слов: 163_

### [Du hast gesagt: Думаю про опцию д поискать в том числе на про что-то подобное на…](docs/lorenzo-agent/naming/00-question-lorenzo-codename.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — выбор имени…


_Слов: 238_

### [Результаты последнего поиска — что нашлось и что не нашлось](docs/lorenzo-agent/naming/01-search-results-not-found.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — выбор имени…


_Слов: 295_

### [Что взять: agent controller architecture](docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md)
> > !TIP


_Слов: 1183_

### [LAYER 7: Coordination engine](docs/lorenzo-agent/naming/03-dhlab-umbrella.md)
> > !TIP


_Слов: 1402_

### [naming](docs/lorenzo-agent/naming/README.md)
> Файлов: 4

  - Содержание

_Слов: 28_

### [Что такое «внуковая» комбинация — operationalized Lorenzo](docs/lorenzo-agent/operationalized/00-overview-grandchild-combination.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ «вну…


_Слов: 603_

### [Плюсы 1–7: feasibility, flywheel, independent value, mission alignment, collaborators, pattern validation, Анастасия Бутова](docs/lorenzo-agent/operationalized/01-pluses-1-7.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ «вну…


_Слов: 470_

### [Минусы 1–10: integration сложность, lifecycle risk, license, framing, competition, scope, limitations, complexity budget, project tension, tool vs impact](docs/lorenzo-agent/operationalized/02-minuses-1-10.md)
> > !TIP


_Слов: 738_

### [Моё честное мнение: что реально и что НЕ реально](docs/lorenzo-agent/operationalized/03-honest-opinion.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ «вну…


_Слов: 180_

### [Рекомендации: принять архитектуру как direction, не immediate plan](docs/lorenzo-agent/operationalized/04-recommendations.md)
> > !TIP


_Слов: 440_

### [Anchor-узел: Habr Scout как первый шаг](docs/lorenzo-agent/operationalized/05-anchor-node-habr-scout.md)
> > !TIP


_Слов: 584_

### [Вывод: документ deserves serious attention](docs/lorenzo-agent/operationalized/06-conclusion-deserves-attention.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — анализ «вну…

- Софтверные комбинации на Хабре для Svyazi 2.0
  - Executive summary

_Слов: 518_

### [operationalized](docs/lorenzo-agent/operationalized/README.md)
> Файлов: 7

  - Содержание

_Слов: 45_

### [Поэтапная структура активностей Lorenzo — обзор](docs/lorenzo-agent/phased-deployment/00-overview.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 169_

### [Уровень 0 — Ручной режим (текущий)](docs/lorenzo-agent/phased-deployment/01-level-0-manual.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 179_

### [Уровень 1 — Минимальный (Lorenzo Zero)](docs/lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 241_

### [Уровень 2 — Базовый (Lorenzo Lite)](docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 207_

### [Уровень 3 — Средний (Lorenzo Active)](docs/lorenzo-agent/phased-deployment/04-level-3-medium-active.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 222_

### [Уровень 4 — Расширенный (Lorenzo Mature)](docs/lorenzo-agent/phased-deployment/05-level-4-extended-mature.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 183_

### [Уровень 5 — Полный (Lorenzo Network)](docs/lorenzo-agent/phased-deployment/06-level-5-full-network.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 146_

### [Логика прогрессии: conservative escalation](docs/lorenzo-agent/phased-deployment/07-progression-logic.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — пятиуровнев…


_Слов: 185_

### [Что мы можем делать прямо сейчас (Уровень 0 + параллельная подготовка к Уровню 1)](docs/lorenzo-agent/phased-deployment/08-current-session-poc.md)
> > !TIP


_Слов: 839_

### [phased-deployment](docs/lorenzo-agent/phased-deployment/README.md)
> Файлов: 9

  - Содержание

_Слов: 59_

### [Du hast gesagt: А под какой сценарий больше всего подходит такой сценарий что тв…](docs/lorenzo-agent/scenarios/00-question-scenario.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — под какой с…


_Слов: 177_

### [Claude hat geantwortet: Очень интересный вопрос.](docs/lorenzo-agent/scenarios/01-response.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — под какой с…


_Слов: 2453_

### [scenarios](docs/lorenzo-agent/scenarios/README.md)
> Файлов: 2

  - Содержание

_Слов: 18_

### [Direction E: Refine Lorenzo — фундаментальные вопросы перед architecture](docs/lorenzo-agent/specification/00-context-fundamental-questions.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 205_

### [Question 1: Что Lorenzo фундаментально такое? (Framings A–D)](docs/lorenzo-agent/specification/01-q1-what-lorenzo-is.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 348_

### [Question 2: Кому Lorenzo служит? (4 варианта приоритета)](docs/lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 238_

### [Question 3: Что Lorenzo фактически делает?](docs/lorenzo-agent/specification/03-q3-what-lorenzo-does.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 228_

### [Question 4: Каков Lorenzo's character?](docs/lorenzo-agent/specification/04-q4-character.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 292_

### [Question 5: Каковы limits Lorenzo's authority?](docs/lorenzo-agent/specification/05-q5-authority-limits.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 228_

### [Question 6: Как Lorenzo accountable?](docs/lorenzo-agent/specification/06-q6-accountability.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 214_

### [Question 7: Каковы success metrics?](docs/lorenzo-agent/specification/07-q7-success-metrics.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 216_

### [Question 8: Lorenzo's relationship с другими AI agents](docs/lorenzo-agent/specification/08-q8-other-ai-relationships.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 207_

### [Question 9: Geographic / linguistic scope](docs/lorenzo-agent/specification/09-q9-geographic-linguistic-scope.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 211_

### [Question 10: Funding model (Options A–F + Phase strategy)](docs/lorenzo-agent/specification/10-q10-funding-model.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Direction E…


_Слов: 260_

### [Сложности и рекомендации перед detailed specification](docs/lorenzo-agent/specification/11-difficulties-and-recommendations.md)
> > !IMPORTANT


_Слов: 1408_

### [specification](docs/lorenzo-agent/specification/README.md)
> Файлов: 12

  - Содержание

_Слов: 77_

**Итого в секции: 19,979 слов, 62 файлов**


## 📁 Nautilus (`docs/nautilus/`)

### [nautilus/ — Nautilus Portal Protocol и связанные working papers](docs/nautilus/README.md)
> Часть исходного MHTML‑снимка Вакансии в Anthropic по кластерам - Claude посвящена не вакансиям, а собственным архитектур…

  - Подпапки
  - Как читать
  - Ключевой принцип Nautilus
  - Связь с остальным монорепозиторием

_Слов: 524_

### [community-discussions/ — обсуждения и реакции вокруг DHLab серии](docs/nautilus/community-discussions/README.md)
> Менее формализованные дискуссии — реакции на Habr-статьи, обсуждение того, могут ли быть voiceless контрибьюторы, как аг…


_Слов: 90_

### [Du hast gesagt: Такой агент конечно меняет уже собственную реальность человека и…](docs/nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — агент меняе…


_Слов: 216_

### [Claude hat geantwortet: Хорошо.](docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md)
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

### [agent-changes-reality](docs/nautilus/community-discussions/agent-changes-reality/README.md)
> Файлов: 2

  - Содержание

_Слов: 17_

### [Du hast gesagt: https://habr.](docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — реакция на …


_Слов: 72_

### [Claude hat geantwortet: Прочитал внимательно.](docs/nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md)
> > !WARNING

- unknownlegalconcepts.yml

_Слов: 2467_

### [habr-article-1-reaction](docs/nautilus/community-discussions/habr-article-1-reaction/README.md)
> Файлов: 2

  - Содержание

_Слов: 17_

### [Du hast gesagt: https://www.](docs/nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — реакция на …


_Слов: 157_

### [Claude hat geantwortet: Прочитаю статью, чтобы понимать конкретный кейс, на кото…](docs/nautilus/community-discussions/habr-article-2-reaction/01-response.md)
> > !TIP


_Слов: 2792_

### [habr-article-2-reaction](docs/nautilus/community-discussions/habr-article-2-reaction/README.md)
> Файлов: 2

  - Содержание

_Слов: 17_

### [Du hast gesagt: Да это интересная ссылка спасибо всем участникам за творчество и…](docs/nautilus/community-discussions/practical-observations/00-question-practical.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — практически…


_Слов: 227_

### [Claude hat geantwortet: Отличное наблюдение.](docs/nautilus/community-discussions/practical-observations/01-response.md)
> > !TIP


_Слов: 1837_

### [practical-observations](docs/nautilus/community-discussions/practical-observations/README.md)
> Файлов: 2

  - Содержание

_Слов: 17_

### [Du hast gesagt: Самый интересный вопрос — могут ли быть voiceless контрибьюторы](docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — voiceless к…


_Слов: 514_

### [Claude hat geantwortet: Это сильное продолжение мысли, и оно заслуживает серьёзн…](docs/nautilus/community-discussions/voiceless-contributors/01-response.md)
> > !WARNING


_Слов: 2533_

### [voiceless-contributors](docs/nautilus/community-discussions/voiceless-contributors/README.md)
> Файлов: 2

  - Содержание

_Слов: 17_

### [1. Why the Binary View Is Incomplete](docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 1. Why the Binary View Is Incomplete

_Слов: 640_

### [2. The Twenty-One Teachers Pattern](docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md)
> > !TIP

  - Содержание
  - 2. The Twenty-One Teachers Pattern

_Слов: 780_

### [3. What Makes a Composite Skills Agent](docs/nautilus/composite-skills-agents/03-what-makes-csa.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 3. What Makes a Composite Skills Agent

_Слов: 889_

### [4. The Sub-Agent Registry](docs/nautilus/composite-skills-agents/04-sub-agent-registry.md)
> > !TIP

  - Содержание
  - 4. The Sub-Agent Registry

_Слов: 750_

### [5. Configuration: How Principals Build Their Ensembles](docs/nautilus/composite-skills-agents/05-configuration-ensembles.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 5. Configuration: How Principals Build Their Ensembles

_Слов: 681_

### [6. Coordination and Disagreement Resolution](docs/nautilus/composite-skills-agents/06-coordination-disagreement.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 6. Coordination and Disagreement Resolution

_Слов: 742_

### [7. Economics of Combinatorial Replication](docs/nautilus/composite-skills-agents/07-economics-combinatorial.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 7. Economics of Combinatorial Replication

_Слов: 722_

### [8. Seven Domains of Application](docs/nautilus/composite-skills-agents/08-seven-domains.md)
> > !TIP

  - Содержание
  - 8. Seven Domains of Application

_Слов: 948_

### [9. Integration with OKWF Infrastructure](docs/nautilus/composite-skills-agents/09-okwf-integration.md)
> > !TIP

  - Содержание
  - 9. Integration with OKWF Infrastructure

_Слов: 693_

### [10. Risks Specific to Composite Architectures](docs/nautilus/composite-skills-agents/10-risks.md)
> > !TIP

  - Содержание
  - 10. Risks Specific to Composite Architectures

_Слов: 732_

### [11. Open Questions](docs/nautilus/composite-skills-agents/11-open-questions.md)
> > !TIP

  - 11. Open Questions

_Слов: 467_

### [12. Call for Collaboration](docs/nautilus/composite-skills-agents/12-call-for-collaboration.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - 12. Call for Collaboration

_Слов: 350_

### [13. Closing](docs/nautilus/composite-skills-agents/13-closing.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Comp…

  - Содержание
  - 13. Closing
  - Acknowledgments
  - References

_Слов: 664_

### [composite-skills-agents](docs/nautilus/composite-skills-agents/README.md)
> Файлов: 13

  - Содержание

_Слов: 78_

### [Du hast gesagt: Важный момент про способности про скилы как один человек професс…](docs/nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — 21 учитель …


_Слов: 540_

### [Claude hat geantwortet: Это очень тонкое и важное наблюдение.](docs/nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md)
> > !IMPORTANT


_Слов: 517_

### [Это не Тип 1 — потому что профиль не общий для всей профессии. И это не Тип 4 — …](docs/nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md)
> > !WARNING


_Слов: 1019_

### [Какой под-агент (или какие) должны её обработать](docs/nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md)
> > !WARNING


_Слов: 902_

### [composite-skills-agents-companion-mentors](docs/nautilus/composite-skills-agents-companion-mentors/README.md)
> Файлов: 4

  - Содержание

_Слов: 27_

### [Abstract — The Double-Triangle Architecture](docs/nautilus/double-triangle-architecture/00-abstract.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

- The Double-Triangle Architecture
  - A Formal Model for Human-AI Collaboration in Distributed Knowledge Work
  - Abstract
  - Table of Contents

_Слов: 407_

### [1. Why Single-Triangle Models Are Incomplete](docs/nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

  - 1. Why Single-Triangle Models Are Incomplete

_Слов: 466_

### [2. The Double-Triangle Architecture](docs/nautilus/double-triangle-architecture/02-double-triangle-architecture.md)
> > !IMPORTANT

  - Содержание
  - 2. The Double-Triangle Architecture

_Слов: 687_

### [3. Three Inter-Layer Protocols](docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md)
> > !IMPORTANT

  - Содержание
  - 3. Three Inter-Layer Protocols

_Слов: 820_

### [4. Nautilus Portal as Reference Substrate](docs/nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

  - Содержание
  - 4. Nautilus Portal as Reference Substrate

_Слов: 631_

### [5. Pattern Library as Bridge Between Triangles](docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md)
> > !TIP

  - Содержание
  - 5. Pattern Library as Bridge Between Triangles

_Слов: 642_

### [6. Four Deployment Domains](docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

  - Содержание
  - 6. Four Deployment Domains

_Слов: 634_

### [7. Open Questions](docs/nautilus/double-triangle-architecture/07-open-questions.md)
> > !TIP

  - Содержание
  - 7. Open Questions

_Слов: 726_

### [8. Call to Action](docs/nautilus/double-triangle-architecture/08-call-to-action.md)
> > !TIP

  - Содержание
  - 8. Call to Action

_Слов: 704_

### [Acknowledgments](docs/nautilus/double-triangle-architecture/09-acknowledgments.md)
> > !TIP

  - Acknowledgments

_Слов: 208_

### [References](docs/nautilus/double-triangle-architecture/10-references.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «The …

  - References

_Слов: 278_

### [Appendix A: Glossary](docs/nautilus/double-triangle-architecture/11-glossary.md)
> > !TIP

  - Содержание
  - Appendix A: Glossary
  - Appendix B: Summary of Contributions
  - Appendix C: Version History

_Слов: 1582_

### [double-triangle-architecture](docs/nautilus/double-triangle-architecture/README.md)
> Файлов: 12

  - Содержание

_Слов: 71_

### [The Missing Middle Layer Between Chat and Code](docs/nautilus/infrastructure-layer-b-en/00-intro.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

- Infrastructure for AI-Collaborative Intellectual Work
  - The Missing Middle Layer Between Chat and Code

_Слов: 191_

### [Why This Document Exists](docs/nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Why This Document Exists

_Слов: 305_

### [Why This Document Exists](docs/nautilus/infrastructure-layer-b-en/02-why-document-exists.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Why This Document Exists

_Слов: 305_

### [The Two-Layer Stack As It Exists](docs/nautilus/infrastructure-layer-b-en/03-two-layer-stack.md)
> > !TIP

  - The Two-Layer Stack As It Exists

_Слов: 352_

### [What's Missing — Layer B](docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - What's Missing — Layer B

_Слов: 424_

### [Why This Hasn't Been Built](docs/nautilus/infrastructure-layer-b-en/05-why-not-built.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Why This Hasn't Been Built

_Слов: 344_

### [Existing Approximations](docs/nautilus/infrastructure-layer-b-en/06-existing-approximations.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Existing Approximations

_Слов: 466_

### [The Specific Case in Front of Us](docs/nautilus/infrastructure-layer-b-en/07-specific-case.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Содержание
  - The Specific Case in Front of Us

_Слов: 614_

### [The Recursive Insight](docs/nautilus/infrastructure-layer-b-en/08-recursive-insight.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - The Recursive Insight

_Слов: 326_

### [What Industry Will Likely Build](docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - What Industry Will Likely Build

_Слов: 273_

### [What This Document Doesn't Solve](docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - What This Document Doesn't Solve

_Слов: 204_

### [Practical Recommendations for the Current Project](docs/nautilus/infrastructure-layer-b-en/11-practical-recommendations.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Practical Recommendations for the Current Project

_Слов: 326_

### [Closing](docs/nautilus/infrastructure-layer-b-en/12-closing.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Closing

_Слов: 213_

### [Acknowledgments](docs/nautilus/infrastructure-layer-b-en/13-acknowledgments-refs.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Содержание
  - Acknowledgments
  - References
  - Appendix: Position in Series Visualization

_Слов: 586_

### [infrastructure-layer-b-en](docs/nautilus/infrastructure-layer-b-en/README.md)
> Файлов: 14

  - Содержание

_Слов: 89_

### [00 Intro](docs/nautilus/infrastructure-layer-b-ru/00-intro.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…


_Слов: 520_

### [Почему этот документ существует](docs/nautilus/infrastructure-layer-b-ru/01-zachem-dokument.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Почему этот документ существует

_Слов: 265_

### [Двухслойный стек, как он существует](docs/nautilus/infrastructure-layer-b-ru/02-dvukhsloynyy-stek.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Двухслойный стек, как он существует

_Слов: 316_

### [Что отсутствует — Слой B](docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Что отсутствует — Слой B

_Слов: 401_

### [Почему это не было построено](docs/nautilus/infrastructure-layer-b-ru/04-pochemu-ne-postroeno.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Почему это не было построено

_Слов: 318_

### [Существующие приближения](docs/nautilus/infrastructure-layer-b-ru/05-priblizheniya.md)
> > !WARNING

  - Существующие приближения

_Слов: 461_

### [Конкретный случай перед нами](docs/nautilus/infrastructure-layer-b-ru/06-konkretnyy-sluchay.md)
> > !WARNING

  - Содержание
  - Конкретный случай перед нами

_Слов: 592_

### [Рекурсивное прозрение](docs/nautilus/infrastructure-layer-b-ru/07-rekursivnoe-prozrenie.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Рекурсивное прозрение

_Слов: 315_

### [Что промышленность вероятно построит](docs/nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md)
> > !WARNING

  - Что промышленность вероятно построит

_Слов: 284_

### [Что этот документ не решает](docs/nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md)
> > !WARNING

  - Что этот документ не решает

_Слов: 205_

### [Практические рекомендации для текущего проекта](docs/nautilus/infrastructure-layer-b-ru/10-rekomendatsii.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Практические рекомендации для текущего проекта

_Слов: 311_

### [Заключение](docs/nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Заключение

_Слов: 215_

### [Благодарности](docs/nautilus/infrastructure-layer-b-ru/12-blagodarnosti-ssylki.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Infr…

  - Содержание
  - Благодарности
  - Ссылки
  - Приложение: Визуализация позиции в серии

_Слов: 620_

### [infrastructure-layer-b-ru](docs/nautilus/infrastructure-layer-b-ru/README.md)
> Файлов: 13

  - Содержание

_Слов: 80_

### [1. The Cowork Discovery and Why It Changes Everything](docs/nautilus/ingit-cowork-en/01-cowork-discovery.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 1. The Cowork Discovery and Why It Changes Everything

_Слов: 631_

### [2. What Cowork Provides That InGit Doesn't Need to Build](docs/nautilus/ingit-cowork-en/02-cowork-provides.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 2. What Cowork Provides That InGit Doesn't Need to Build

_Слов: 607_

### [3. What InGit Provides That Cowork Lacks](docs/nautilus/ingit-cowork-en/03-ingit-provides.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 3. What InGit Provides That Cowork Lacks

_Слов: 792_

### [4. The Symbiotic Architecture](docs/nautilus/ingit-cowork-en/04-symbiotic-architecture.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 4. The Symbiotic Architecture

_Слов: 574_

### [5. Four Integration Paths in Order of Accessibility](docs/nautilus/ingit-cowork-en/05-four-integration-paths.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 5. Four Integration Paths in Order of Accessibility

_Слов: 737_

### [6. Refined InGit Scope with Cowork in Mind](docs/nautilus/ingit-cowork-en/06-refined-ingit-scope.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - 6. Refined InGit Scope with Cowork in Mind

_Слов: 378_

### [7. Practical First Steps This Month](docs/nautilus/ingit-cowork-en/07-practical-first-steps.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - 7. Practical First Steps This Month

_Слов: 374_

### [8. Implications for Nautilus and OKWF](docs/nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md)
> > !TIP

  - Содержание
  - 8. Implications for Nautilus and OKWF

_Слов: 595_

### [9. Risks and Open Questions](docs/nautilus/ingit-cowork-en/09-risks-open-questions.md)
> > !TIP

  - Содержание
  - 9. Risks and Open Questions

_Слов: 542_

### [10. Strategic Positioning](docs/nautilus/ingit-cowork-en/10-strategic-positioning.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 10. Strategic Positioning
  - Acknowledgments

_Слов: 715_

### [ingit-cowork-en](docs/nautilus/ingit-cowork-en/README.md)
> Файлов: 10

  - Содержание

_Слов: 64_

### [1. Открытие Cowork и почему это меняет всё](docs/nautilus/ingit-cowork-ru/01-otkrytie-cowork.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 1. Открытие Cowork и почему это меняет всё

_Слов: 600_

### [2. Что Cowork обеспечивает, что InGit не нужно строить](docs/nautilus/ingit-cowork-ru/02-chto-cowork-obespechivaet.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 2. Что Cowork обеспечивает, что InGit не нужно строить

_Слов: 606_

### [3. Что InGit обеспечивает, чего Cowork не хватает](docs/nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md)
> > !IMPORTANT

  - Содержание
  - 3. Что InGit обеспечивает, чего Cowork не хватает

_Слов: 812_

### [4. Симбиотическая Архитектура](docs/nautilus/ingit-cowork-ru/04-simbioticheskaya-arkhitektura.md)
> > !WARNING

  - Содержание
  - 4. Симбиотическая Архитектура

_Слов: 590_

### [5. Четыре пути интеграции в порядке доступности](docs/nautilus/ingit-cowork-ru/05-chetyre-puti-integratsii.md)
> > !TIP

  - Содержание
  - 5. Четыре пути интеграции в порядке доступности

_Слов: 742_

### [6. Уточнённый объём InGit с учётом Cowork](docs/nautilus/ingit-cowork-ru/06-utochnyonnyy-obyom-ingit.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - 6. Уточнённый объём InGit с учётом Cowork

_Слов: 374_

### [7. Практические первые шаги в этом месяце](docs/nautilus/ingit-cowork-ru/07-prakticheskie-shagi.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - 7. Практические первые шаги в этом месяце

_Слов: 373_

### [8. Импликации для Nautilus и OKWF](docs/nautilus/ingit-cowork-ru/08-implikatsii-nautilus-okwf.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 8. Импликации для Nautilus и OKWF

_Слов: 575_

### [9. Риски и Открытые Вопросы](docs/nautilus/ingit-cowork-ru/09-riski-voprosy.md)
> > !WARNING

  - Содержание
  - 9. Риски и Открытые Вопросы

_Слов: 558_

### [10. Стратегическое Позиционирование](docs/nautilus/ingit-cowork-ru/10-strategicheskoe-pozitsionirovanie.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «InGi…

  - Содержание
  - 10. Стратегическое Позиционирование

_Слов: 650_

### [ingit-cowork-ru](docs/nautilus/ingit-cowork-ru/README.md)
> Файлов: 10

  - Содержание

_Слов: 62_

### [Du hast gesagt: Интересно как новая как инновация как как рационализация как пер…](docs/nautilus/innovation-transitions/00-question-innovations-transitions.md)
> > !WARNING

  - Содержание
  - Ответ по существу

_Слов: 2802_

### [Claude hat geantwortet: Отличный запрос.](docs/nautilus/innovation-transitions/01-response.md)
> > !TIP


_Слов: 2405_

### [innovation-transitions](docs/nautilus/innovation-transitions/README.md)
> Файлов: 2

  - Содержание

_Слов: 16_

### [Du hast gesagt: Ещё есть такие вопросы то есть если общие юридические Наутилус м…](docs/nautilus/multi-tier-architecture/00-question-multi-tier.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — многоуровне…


_Слов: 197_

### [Claude hat geantwortet: Это стратегически значимый вопрос, и ответ на него — да,…](docs/nautilus/multi-tier-architecture/01-strategic-significance.md)
> > !WARNING


_Слов: 2586_

### [multi-tier-architecture](docs/nautilus/multi-tier-architecture/README.md)
> Файлов: 2

  - Содержание

_Слов: 17_

### [Du hast gesagt: Вопрос такой вопрос и такие а можно ли этот протокол это система…](docs/nautilus/npp-humanitarian-extension/00-question-can-it-apply-to-docs.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — применение …


_Слов: 302_

### [Структурное сравнение: код vs гуманитарные документы](docs/nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md)
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

### [Что он даёт вам на практике. Через MCP Claude Desktop может ответить на запросы …](docs/nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — применение …


_Слов: 219_

### [Что не существует на рынке:](docs/nautilus/npp-humanitarian-extension/03-what-doesnt-exist-on-market.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — применение …


_Слов: 165_

### [Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access t…](docs/nautilus/npp-humanitarian-extension/04-grant-opportunities.md)
> > !TIP


_Слов: 540_

### [Что из этого сейчас кажется более ценным? Или какая-то своя комбинация?](docs/nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — применение …


_Слов: 139_

### [npp-humanitarian-extension](docs/nautilus/npp-humanitarian-extension/README.md)
> Файлов: 6

  - Содержание

_Слов: 41_

### [Abstract + Status of This Document](docs/nautilus/npp-v1-0/00-abstract-status.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

- Nautilus Portal Protocol
  - Abstract
  - 0. Status of This Document

_Слов: 213_

### [1. Introduction (Motivation, Design Goals, Non-Goals, Terminology)](docs/nautilus/npp-v1-0/01-introduction.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 1. Introduction

_Слов: 313_

### [2. Terminology](docs/nautilus/npp-v1-0/02-terminology.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 2. Terminology

_Слов: 267_

### [3. Registry (nautilus.json)](docs/nautilus/npp-v1-0/03-registry.md)
> > !IMPORTANT

  - 3. Registry (nautilus.json)

_Слов: 343_

### [4. Passport (passport.md)](docs/nautilus/npp-v1-0/04-passport.md)
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

### [5. Compatibility Levels](docs/nautilus/npp-v1-0/05-compatibility-levels.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 5. Compatibility Levels

_Слов: 221_

### [6. Adapter Interface](docs/nautilus/npp-v1-0/06-adapter-interface.md)
> > !IMPORTANT

  - 6. Adapter Interface

_Слов: 334_

### [7. PortalEntry Structure](docs/nautilus/npp-v1-0/07-portal-entry.md)
> > !IMPORTANT

  - 7. PortalEntry Structure

_Слов: 224_

### [8. Consensus Algorithm (v1.0: string normalization)](docs/nautilus/npp-v1-0/08-consensus-algorithm.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 8. Consensus Algorithm

_Слов: 266_

### [9. Query Flow](docs/nautilus/npp-v1-0/09-query-flow.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 9. Query Flow

_Слов: 182_

### [10. QueryResult Structure](docs/nautilus/npp-v1-0/10-query-result.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 10. QueryResult Structure

_Слов: 157_

### [11. Security Considerations](docs/nautilus/npp-v1-0/11-security-considerations.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 11. Security Considerations

_Слов: 198_

### [12. Versioning Policy](docs/nautilus/npp-v1-0/12-versioning-policy.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 12. Versioning Policy

_Слов: 173_

### [13. Reference Implementation](docs/nautilus/npp-v1-0/13-reference-implementation.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 13. Reference Implementation

_Слов: 120_

### [14. ADR-001: Federation over Merging](docs/nautilus/npp-v1-0/14-adr-001-federation-over-merging.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 14. ADR-001: Federation over Merging

_Слов: 202_

### [15. Glossary of Examples](docs/nautilus/npp-v1-0/15-glossary.md)
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

### [Appendix A: Minimal Working Example](docs/nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

- mynotes
  - Essence
  - Native Format
  - Content Overview
  - Angle / Perspective
  - Author

_Слов: 190_

### [Appendix B: Change Log](docs/nautilus/npp-v1-0/17-appendix-b-change-log.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - Appendix B: Change Log

_Слов: 95_

### [Комментарий: дизайн-решения NPP v1.0](docs/nautilus/npp-v1-0/18-comment-on-document.md)
> > !IMPORTANT


_Слов: 454_

### [npp-v1-0](docs/nautilus/npp-v1-0/README.md)
> Файлов: 19

  - Содержание

_Слов: 116_

### [Abstract + Status of This Document](docs/nautilus/npp-v1-1/00-abstract-status.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

- Nautilus Portal Protocol
  - Abstract
  - 0. Status of This Document

_Слов: 335_

### [1. Introduction (Motivation, Design Goals, Non-Goals, Terminology, Changes from v1.0)](docs/nautilus/npp-v1-1/01-introduction.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 1. Introduction

_Слов: 447_

### [2. Terminology](docs/nautilus/npp-v1-1/02-terminology.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 2. Terminology

_Слов: 371_

### [3. Registry (nautilus.json)](docs/nautilus/npp-v1-1/03-registry.md)
> > !IMPORTANT

  - 3. Registry (nautilus.json)

_Слов: 479_

### [4. Passport (passport.md)](docs/nautilus/npp-v1-1/04-passport.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 4. Passport (passport.md)
- Паспорт: /

_Слов: 294_

### [5. Compatibility Levels](docs/nautilus/npp-v1-1/05-compatibility-levels.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 5. Compatibility Levels

_Слов: 302_

### [6. Adapter Interface](docs/nautilus/npp-v1-1/06-adapter-interface.md)
> > !IMPORTANT

  - 6. Adapter Interface

_Слов: 327_

### [7. PortalEntry Structure](docs/nautilus/npp-v1-1/07-portal-entry.md)
> > !IMPORTANT

  - 7. PortalEntry Structure

_Слов: 290_

### [8. Q6 Space (Normative)](docs/nautilus/npp-v1-1/08-q6-space.md)
> > !IMPORTANT

  - 8. Q6 Space (Normative)

_Слов: 415_

### [9. Consensus Algorithm](docs/nautilus/npp-v1-1/09-consensus-algorithm.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 9. Consensus Algorithm

_Слов: 343_

### [10. Query Flow](docs/nautilus/npp-v1-1/10-query-flow.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 10. Query Flow

_Слов: 228_

### [11. Relevance Ranking](docs/nautilus/npp-v1-1/11-relevance-ranking.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 11. Relevance Ranking
- Bonus for connectivity
- Penalty for fallback

_Слов: 203_

### [12. Onboarding Paths (Normative)](docs/nautilus/npp-v1-1/12-onboarding-paths.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 12. Onboarding Paths (Normative)

_Слов: 449_

### [13. REST API Contract (Normative for Portals)](docs/nautilus/npp-v1-1/13-rest-api.md)
> > !IMPORTANT

  - 13. REST API Contract (Normative for Portals)

_Слов: 437_

### [14. SDK Contract (Informative)](docs/nautilus/npp-v1-1/14-sdk.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 14. SDK Contract (Informative)

_Слов: 192_

### [15. Security Considerations](docs/nautilus/npp-v1-1/15-security.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 15. Security Considerations

_Слов: 288_

### [16. MCP Extension (Informative)](docs/nautilus/npp-v1-1/16-mcp-extension.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 16. MCP Extension (Informative)

_Слов: 154_

### [17. Versioning Policy](docs/nautilus/npp-v1-1/17-versioning-policy.md)
> > !IMPORTANT

  - 17. Versioning Policy

_Слов: 227_

### [18. Reference Implementation](docs/nautilus/npp-v1-1/18-reference-implementation.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 18. Reference Implementation

_Слов: 212_

### [19. ADR-001: Federation over Merging](docs/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 19. ADR-001: Federation over Merging

_Слов: 218_

### [20. ADR-002: Q6 as First-Class Protocol Concept](docs/nautilus/npp-v1-1/20-adr-002-q6-first-class.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 20. ADR-002: Q6 as First-Class Protocol Concept

_Слов: 210_

### [21. ADR-003: Five Onboarding Paths as Equal-Rank](docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — Nautilus Po…

  - 21. ADR-003: Five Onboarding Paths as Equal-Rank

_Слов: 174_

### [22. Glossary of Reference Examples](docs/nautilus/npp-v1-1/22-glossary.md)
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

### [npp-v1-1](docs/nautilus/npp-v1-1/README.md)
> Файлов: 23

  - Содержание

_Слов: 138_

### [AI-Coordinated Infrastructure for Distributed Expert Contribution](docs/nautilus/okwf-concept/00-abstract.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

- Open Knowledge Work Foundation
  - AI-Coordinated Infrastructure for Distributed Expert Contribution
  - Executive Summary
  - Table of Contents

_Слов: 383_

### [1. Problem Statement](docs/nautilus/okwf-concept/01-problem-statement.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 1. Problem Statement

_Слов: 582_

### [2. Target Populations](docs/nautilus/okwf-concept/02-target-populations.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 2. Target Populations

_Слов: 650_

### [3. Why Existing Solutions Fail](docs/nautilus/okwf-concept/03-why-existing-fail.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 3. Why Existing Solutions Fail

_Слов: 663_

### [4. Proposed Infrastructure](docs/nautilus/okwf-concept/04-proposed-infrastructure.md)
> > !TIP

  - Содержание
  - 4. Proposed Infrastructure

_Слов: 969_

### [5. Economic Model](docs/nautilus/okwf-concept/05-economic-model.md)
> > !TIP

  - Содержание
  - 5. Economic Model

_Слов: 578_

### [6. Governance and Ethics](docs/nautilus/okwf-concept/06-governance-ethics.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - 6. Governance and Ethics

_Слов: 486_

### [7. Phased Rollout Plan](docs/nautilus/okwf-concept/07-phased-rollout.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 7. Phased Rollout Plan

_Слов: 615_

### [8. Risk Analysis](docs/nautilus/okwf-concept/08-risk-analysis.md)
> > !TIP

  - Содержание
  - 8. Risk Analysis

_Слов: 643_

### [9. Call for Partnership](docs/nautilus/okwf-concept/09-call-for-partnership.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - 9. Call for Partnership

_Слов: 460_

### [10. Appendices](docs/nautilus/okwf-concept/10-appendices.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Open…

  - Содержание
  - 10. Appendices

_Слов: 796_

### [okwf-concept](docs/nautilus/okwf-concept/README.md)
> Файлов: 11

  - Содержание

_Слов: 69_

### [Du hast gesagt: Насчёт приватности Я думаю что возможно удалять только личные да…](docs/nautilus/privacy-federation/00-question-anonymization.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — приватность…


_Слов: 288_

### [Что именно анонимизировать: немецкий стандарт](docs/nautilus/privacy-federation/01-what-to-anonymize-german-standard.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — приватность…


_Слов: 269_

### [Архитектурное решение: две-уровневая публикация](docs/nautilus/privacy-federation/02-two-tier-publication.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — приватность…

- В приватном репо cases-private:

_Слов: 498_

### [Что это даёт технически](docs/nautilus/privacy-federation/03-what-this-gives-technically.md)
> > !WARNING


_Слов: 1492_

### [Что я могу сделать сейчас](docs/nautilus/privacy-federation/04-what-i-can-do-now.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — приватность…


_Слов: 322_

### [privacy-federation](docs/nautilus/privacy-federation/README.md)
> Файлов: 5

  - Содержание

_Слов: 35_

### [Professional Colleague Agents](docs/nautilus/professional-colleague-agents-en/00-abstract.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

- Professional Colleague Agents
  - A Typology of AI Agents on the Principal Side and the Case for Profession-Specific Co-Workers
  - Abstract
  - Table of Contents

_Слов: 426_

### [1. The Five-Type Typology of Principal-Side Agents](docs/nautilus/professional-colleague-agents-en/01-five-type-typology.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 1. The Five-Type Typology of Principal-Side Agents

_Слов: 871_

### [2. What Makes a Professional Colleague Agent](docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 2. What Makes a Professional Colleague Agent

_Слов: 787_

### [3. Empirical Case Study: «Обучай»](docs/nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 3. Empirical Case Study: «Обучай»

_Слов: 807_

### [4. Architecture of Professional Colleague Agents](docs/nautilus/professional-colleague-agents-en/04-architecture.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 4. Architecture of Professional Colleague Agents

_Слов: 847_

### [5. The Economics of Profession-Wide Replication](docs/nautilus/professional-colleague-agents-en/05-economics-replication.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 5. The Economics of Profession-Wide Replication

_Слов: 695_

### [6. Risks Specific to this Category](docs/nautilus/professional-colleague-agents-en/06-risks.md)
> > !TIP

  - Содержание
  - 6. Risks Specific to this Category

_Слов: 1153_

### [7. Application Domains](docs/nautilus/professional-colleague-agents-en/07-application-domains.md)
> > !TIP

  - Содержание
  - 7. Application Domains

_Слов: 703_

### [8. Pilot Proposal: SGB Advocate Colleague](docs/nautilus/professional-colleague-agents-en/08-pilot-sgb-advocate.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 8. Pilot Proposal: SGB Advocate Colleague

_Слов: 925_

### [9. Relationship to Other Agent Types](docs/nautilus/professional-colleague-agents-en/09-relationship-other-agents.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 9. Relationship to Other Agent Types

_Слов: 620_

### [10. Open Questions](docs/nautilus/professional-colleague-agents-en/10-open-questions.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - 10. Open Questions

_Слов: 358_

### [11. Call for Collaboration](docs/nautilus/professional-colleague-agents-en/11-call-for-collaboration.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - 11. Call for Collaboration

_Слов: 310_

### [12. Closing](docs/nautilus/professional-colleague-agents-en/12-closing.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Prof…

  - Содержание
  - 12. Closing
  - Acknowledgments
  - References

_Слов: 520_

### [professional-colleague-agents-en](docs/nautilus/professional-colleague-agents-en/README.md)
> Файлов: 13

  - Содержание

_Слов: 82_

### [Содержание](docs/nautilus/professional-colleague-agents-ru/00-abstract.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - Содержание

_Слов: 153_

### [1. Типология из пяти типов агентов на стороне принципала](docs/nautilus/professional-colleague-agents-ru/01-pyat-tipov.md)
> > !IMPORTANT

  - Содержание
  - 1. Типология из пяти типов агентов на стороне принципала

_Слов: 842_

### [2. Что делает агента Профессиональным Коллегой](docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md)
> > !TIP

  - Содержание
  - 2. Что делает агента Профессиональным Коллегой

_Слов: 713_

### [3. Эмпирический кейс: «Обучай»](docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - Содержание
  - 3. Эмпирический кейс: «Обучай»

_Слов: 762_

### [4. Архитектура Профессиональных Коллег-Агентов](docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - Содержание
  - 4. Архитектура Профессиональных Коллег-Агентов

_Слов: 806_

### [5. Экономика тиражирования по профессии](docs/nautilus/professional-colleague-agents-ru/05-ekonomika.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - Содержание
  - 5. Экономика тиражирования по профессии

_Слов: 689_

### [6. Риски, специфичные для этой категории](docs/nautilus/professional-colleague-agents-ru/06-riski.md)
> > !WARNING

  - Содержание
  - 6. Риски, специфичные для этой категории

_Слов: 1142_

### [7. Области применения](docs/nautilus/professional-colleague-agents-ru/07-oblasti-primeneniya.md)
> > !WARNING

  - Содержание
  - 7. Области применения

_Слов: 716_

### [8. Пилотное предложение: SGB Колega-Адвокат](docs/nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md)
> > !WARNING

  - Содержание
  - 8. Пилотное предложение: SGB Колega-Адвокат

_Слов: 981_

### [9. Связь с другими типами агентов](docs/nautilus/professional-colleague-agents-ru/09-svyaz-s-drugimi.md)
> > !WARNING

  - Содержание
  - 9. Связь с другими типами агентов

_Слов: 611_

### [10. Открытые вопросы](docs/nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - 10. Открытые вопросы

_Слов: 341_

### [11. Призыв к сотрудничеству](docs/nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - 11. Призыв к сотрудничеству

_Слов: 300_

### [12. Заключение](docs/nautilus/professional-colleague-agents-ru/12-zaklyuchenie.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Проф…

  - 12. Заключение
  - Благодарности
  - Ссылки

_Слов: 489_

### [professional-colleague-agents-ru](docs/nautilus/professional-colleague-agents-ru/README.md)
> Файлов: 13

  - Содержание

_Слов: 78_

### [AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations](docs/nautilus/representative-agent-layer-en/00-abstract.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

- The Representative Agent Layer
  - AI-Mediated Representation for Underrepresented Experts and Vulnerable Populations
  - Abstract
  - Table of Contents

_Слов: 398_

### [1. The Cinderella Syndrome: Why Quality Stays Invisible](docs/nautilus/representative-agent-layer-en/01-cinderella-syndrome.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 1. The Cinderella Syndrome: Why Quality Stays Invisible

_Слов: 793_

### [2. Historical Precedents: Agents as Civilizational Innovation](docs/nautilus/representative-agent-layer-en/02-historical-precedents.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 2. Historical Precedents: Agents as Civilizational Innovation

_Слов: 911_

### [3. What Makes a Representative Agent](docs/nautilus/representative-agent-layer-en/03-what-makes-representative-agent.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 3. What Makes a Representative Agent

_Слов: 623_

### [4. Ten Domains of Application](docs/nautilus/representative-agent-layer-en/04-ten-domains.md)
> > !TIP

  - Содержание
  - 4. Ten Domains of Application

_Слов: 1552_

### [5. Architectural Specification](docs/nautilus/representative-agent-layer-en/05-architectural-specification.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 5. Architectural Specification

_Слов: 618_

### [6. Ethical Framework](docs/nautilus/representative-agent-layer-en/06-ethical-framework.md)
> > !IMPORTANT

  - 6. Ethical Framework

_Слов: 463_

### [7. Governance and Oversight](docs/nautilus/representative-agent-layer-en/07-governance-oversight.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 7. Governance and Oversight

_Слов: 385_

### [8. Risks and Mitigations](docs/nautilus/representative-agent-layer-en/08-risks-mitigations.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 8. Risks and Mitigations

_Слов: 486_

### [9. Phased Rollout Strategy](docs/nautilus/representative-agent-layer-en/09-phased-rollout.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 9. Phased Rollout Strategy

_Слов: 469_

### [10. Open Questions](docs/nautilus/representative-agent-layer-en/10-open-questions.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 10. Open Questions

_Слов: 367_

### [11. Call for Collaboration](docs/nautilus/representative-agent-layer-en/11-call-for-collaboration.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 11. Call for Collaboration

_Слов: 374_

### [12. Closing](docs/nautilus/representative-agent-layer-en/12-closing.md)
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

### [representative-agent-layer-en](docs/nautilus/representative-agent-layer-en/README.md)
> Файлов: 13

  - Содержание

_Слов: 81_

### [Содержание](docs/nautilus/representative-agent-layer-ru/00-abstract.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание

_Слов: 119_

### [1. Синдром Золушки: Почему качество остаётся невидимым](docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 1. Синдром Золушки: Почему качество остаётся невидимым

_Слов: 751_

### [2. Исторические прецеденты: Агенты как цивилизационная инновация](docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md)
> > !WARNING

  - Содержание
  - 2. Исторические прецеденты: Агенты как цивилизационная инновация

_Слов: 919_

### [3. Что делает агента Представительским](docs/nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md)
> > !TIP

  - Содержание
  - 3. Что делает агента Представительским

_Слов: 609_

### [4. Десять областей применения](docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md)
> > !WARNING

  - Содержание
  - 4. Десять областей применения

_Слов: 1572_

### [5. Архитектурная спецификация](docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - Содержание
  - 5. Архитектурная спецификация

_Слов: 601_

### [6. Этическая рамка](docs/nautilus/representative-agent-layer-ru/06-eticheskaya-ramka.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 6. Этическая рамка

_Слов: 448_

### [7. Управление и надзор](docs/nautilus/representative-agent-layer-ru/07-upravlenie-nadzor.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 7. Управление и надзор

_Слов: 383_

### [8. Риски и меры противодействия](docs/nautilus/representative-agent-layer-ru/08-riski-mery.md)
> > !WARNING

  - Содержание
  - 8. Риски и меры противодействия

_Слов: 573_

### [9. Стратегия поэтапного развёртывания](docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md)
> > !WARNING

  - 9. Стратегия поэтапного развёртывания

_Слов: 484_

### [10. Открытые вопросы](docs/nautilus/representative-agent-layer-ru/10-otkrytye-voprosy.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Repr…

  - 10. Открытые вопросы

_Слов: 353_

### [11. Призыв к сотрудничеству](docs/nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md)
> > !WARNING

  - 11. Призыв к сотрудничеству

_Слов: 381_

### [12. Заключение](docs/nautilus/representative-agent-layer-ru/12-zaklyuchenie.md)
> > !TIP

  - Содержание
  - 12. Заключение
  - Благодарности
  - Ссылки
  - Приложение A: Связь с Сопроводительными Статьями
  - Приложение B: Матрица Сравнения Областей
  - Приложение C: Образцы Случаев Использования в Деталях

_Слов: 4414_

### [representative-agent-layer-ru](docs/nautilus/representative-agent-layer-ru/README.md)
> Файлов: 13

  - Содержание

_Слов: 77_

### [TL;DR — Трёхфазная методология Review](docs/nautilus/review-methodology/00-tldr.md)
> > !WARNING

- Трёхфазная методология Review в Nautilus
  - TL;DR

_Слов: 191_

### [1. Контекст и мотивация](docs/nautilus/review-methodology/01-context-motivation.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 1. Контекст и мотивация

_Слов: 361_

### [2. Формальный workflow](docs/nautilus/review-methodology/02-formal-workflow.md)
> > !WARNING

  - 2. Формальный workflow

_Слов: 407_

### [3. Принципы консолидации (Фаза C)](docs/nautilus/review-methodology/03-consolidation-principles.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 3. Принципы консолидации (Фаза C)
- LOC в Python-коде
- Количество тестов
- Число адаптеров
- Health score
- Q6-покрытие

_Слов: 455_

### [Вопрос: fallback‑ratio как критический или осмысленный?](docs/nautilus/review-methodology/04-fallback-ratio-question.md)
> > !IMPORTANT

  - Вопрос: fallback-ratio как критический или осмысленный?

_Слов: 281_

### [4. Условия применимости](docs/nautilus/review-methodology/05-conditions-of-applicability.md)
> > !WARNING

  - 4. Условия применимости

_Слов: 258_

### [5. Связь с существующими методологиями](docs/nautilus/review-methodology/06-relation-existing-methodologies.md)
> > !WARNING

  - 5. Связь с существующими методологиями

_Слов: 333_

### [6. Почему это валидный паттерн для AI‑assisted workflows](docs/nautilus/review-methodology/07-why-valid-for-ai.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 6. Почему это валидный паттерн для AI-assisted workflows

_Слов: 197_

### [7. Реализация в проекте Nautilus](docs/nautilus/review-methodology/08-implementation-nautilus.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 7. Реализация в проекте Nautilus

_Слов: 257_

### [8. Ограничения и открытые вопросы](docs/nautilus/review-methodology/09-limitations-open-questions.md)
> > !WARNING

  - 8. Ограничения и открытые вопросы

_Слов: 373_

### [9. Checklist применения методологии](docs/nautilus/review-methodology/10-checklist.md)
> > !WARNING

  - 9. Checklist применения методологии

_Слов: 303_

### [10. Конкретный план применения к текущим документам](docs/nautilus/review-methodology/11-application-plan-current-docs.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - 10. Конкретный план применения к текущим документам
- В Termux

_Слов: 225_

### [Appendix A: Шаблон для header warning](docs/nautilus/review-methodology/12-appendix-a-header-warning.md)
> > !WARNING

  - Appendix A: Шаблон для header warning

_Слов: 214_

### [Appendix B: Примеры расхождений и их разрешения](docs/nautilus/review-methodology/13-appendix-b-examples.md)
> > !WARNING

  - Appendix B: Примеры расхождений и их разрешения

_Слов: 281_

### [Главные технические риски](docs/nautilus/review-methodology/14-main-technical-risks.md)
> > !WARNING

  - Главные технические риски

_Слов: 143_

### [Appendix C: История изменений методологии](docs/nautilus/review-methodology/15-appendix-c-history.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — paper «Трёх…

  - Appendix C: История изменений методологии

_Слов: 100_

### [Глоссарий](docs/nautilus/review-methodology/16-glossary.md)
> > !WARNING

  - Глоссарий

_Слов: 971_

### [review-methodology](docs/nautilus/review-methodology/README.md)
> Файлов: 17

  - Содержание

_Слов: 97_

### [Du hast gesagt: Спрос рождает предложение - это простая экономическая истина нач…](docs/nautilus/supply-demand/00-question-supply-demand.md)
> > > Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория). Раздел диалога — спрос рожда…


_Слов: 447_

### [Claude hat geantwortet: Очень богатый вопрос — три разных, но связанных темы.](docs/nautilus/supply-demand/01-three-related-themes.md)
> > !WARNING


_Слов: 2915_

### [supply-demand](docs/nautilus/supply-demand/README.md)
> Файлов: 2

  - Содержание

_Слов: 17_

### [Du hast gesagt: Того если гора не идёт человеку может быть этот человек пойдёт к…](docs/nautilus/transmission-box/00-question-mountain-to-person.md)
> > !TIP


_Слов: 549_

### [Claude hat geantwortet: Это исключительно богатый вопрос, и я хочу ответить на н…](docs/nautilus/transmission-box/01-completing-loop.md)
> > !TIP


_Слов: 3126_

### [transmission-box](docs/nautilus/transmission-box/README.md)
> Файлов: 2

  - Содержание

_Слов: 16_

**Итого в секции: 148,523 слов, 255 файлов**


## 📁 Svyazi 2 0 (`docs/svyazi-2-0/`)

### [Svyazi 2.0 — тематический индекс](docs/svyazi-2-0/README.md)
> Содержимое исходных файлов deep-research-report (1)/(2)/(3)/(4).md (находятся в корне репозитория, не изменены) разбито …

  - Подпапки
  - Источник

_Слов: 158_

### [architecture](docs/svyazi-2-0/architecture/README.md)
> Файлов: 7

  - Содержание

_Слов: 46_

### [Card Envelope](docs/svyazi-2-0/architecture/card-envelope.md)
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 182_

### [Evidence Envelope](docs/svyazi-2-0/architecture/evidence-envelope.md)
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля
  - Особые случаи

_Слов: 222_

### [Архитектурные зазоры](docs/svyazi-2-0/architecture/gaps.md)
> > !TIP

  - Содержание
  - Пять зазоров, важнее поиска ещё десяти инструментов
  - Сводная таблица зазоров
  - Главный практический принцип

_Слов: 597_

### [Интеграционная спецификация (минимум для MVP)](docs/svyazi-2-0/architecture/integration-spec.md)
> > !TIP


_Слов: 267_

### [Memory Write Policy](docs/svyazi-2-0/architecture/memory-write-policy.md)
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 168_

### [Review Record](docs/svyazi-2-0/architecture/review-record.md)
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 105_

### [Skill and Tool Policy](docs/svyazi-2-0/architecture/skill-tool-policy.md)
> > > Источник: deep-research-report (3).md, раздел «Интеграционный контракт».

  - Минимальные поля

_Слов: 165_

### [components](docs/svyazi-2-0/components/README.md)
> Файлов: 19

  - Содержание

_Слов: 120_

### [agent-memory-mcp + Memory OS](docs/svyazi-2-0/components/agent-memory-mcp.md)
> > - Автор: VitaliySemenov / moshael

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 150_

### [AgentFS](docs/svyazi-2-0/components/agentfs.md)
> > - Источник: Хабр + GitHub citeturn33view4turn33view7turn27view0

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 109_

### [AI Factory + AIF Handoff](docs/svyazi-2-0/components/ai-factory.md)
> > - Источник: Хабр + GitHub citeturn20view3turn29search0turn29search9

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 114_

### [AutoResearch + Sequential](docs/svyazi-2-0/components/autoresearch-sequential.md)
> > - Авторы: Андрей Карпаты / Виктория Дочкина

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 122_

### [Graph RAG](docs/svyazi-2-0/components/graph-rag.md)
> > - Автор: VladSpace / vpakspace

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 109_

### [Hybrid RAG knowledge base](docs/svyazi-2-0/components/hybrid-rag.md)
> > - Источник: Хабр citeturn34view2

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 102_

### [knowledge-space](docs/svyazi-2-0/components/knowledge-space.md)
> > - Автор: SoniaBlack / AnastasiyaW

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 107_

### [Legal RAG](docs/svyazi-2-0/components/legal-rag.md)
> > - Источник: Хабр citeturn20view6

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 105_

### [mclaude](docs/svyazi-2-0/components/mclaude.md)
> > - Источник: Хабр + GitHub citeturn20view2turn37search0

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 98_

### [MemNet / memory-is-all-you-need](docs/svyazi-2-0/components/memnet.md)
> > - Источник: Хабр + GitHub citeturn21view4turn17search0turn18search2

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 99_

### [NGT Memory](docs/svyazi-2-0/components/ngt-memory.md)
> > - Автор: spbmolot / ngt-memory

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 120_

### [research-docs + LiteParse](docs/svyazi-2-0/components/research-docs-liteparse.md)
> > - Автор: nlaik / Jerry Liu / LlamaIndex

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 121_

### [Rufler](docs/svyazi-2-0/components/rufler.md)
> > - Автор: zodigancode / lib4u

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 98_

### [Security + routing plane](docs/svyazi-2-0/components/security-routing-plane.md)
> > - Авторы: Dmitriila / BerriAI / MiXaiLL76 / Maslennikovig

  - Описание
  - Ключевые компоненты и паттерны
  - Числовые наблюдения

_Слов: 192_

### [Self‑Aware MCP + Skills + CodeWiki](docs/svyazi-2-0/components/self-aware-mcp.md)
> > - Авторы: akazant / akzhankalimatov / AnastasiyaW

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 132_

### [Svyazi](docs/svyazi-2-0/components/svyazi.md)
> > - Источник: Хабр citeturn41search0

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 116_

### [Voice / local-first stack](docs/svyazi-2-0/components/voice-stack.md)
> > - Авторы: atatchin / askid / обзоры Handy / OpenWhispr

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 136_

### [Yjs + Automerge](docs/svyazi-2-0/components/yjs-automerge.md)
> > - Авторы: Kevin Jahns / Automerge team

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 109_

### [Yodoca](docs/svyazi-2-0/components/yodoca.md)
> > - Источник: Хабр + GitHub citeturn38view7turn21view0turn21view1turn18search1

  - Описание
  - Ключевые компоненты и паттерны

_Слов: 109_

### [Ансамбль A — Collaboration OS](docs/svyazi-2-0/ensembles/A-collaboration-os.md)
> > > Источник: deep-research-report (1).md.

  - Схема
  - Ожидаемые новые свойства

_Слов: 248_

### [Ансамбль B — Forensic RAG для доказуемого matching и review](docs/svyazi-2-0/ensembles/B-forensic-rag.md)
> > > Источник: deep-research-report (1).md.

  - Схема
  - Ожидаемые новые свойства

_Слов: 252_

### [Ансамбль C — Spec‑driven multi‑agent factory](docs/svyazi-2-0/ensembles/C-multi-agent-factory.md)
> > > Источник: deep-research-report (1).md.

  - Схема
  - Ожидаемые новые свойства

_Слов: 249_

### [Ансамбль D — Voice‑first local knowledge mesh](docs/svyazi-2-0/ensembles/D-voice-first-mesh.md)
> > !IMPORTANT

  - Схема
  - Ожидаемые новые свойства

_Слов: 265_

### [Ансамбль E — Safe and cheap execution plane](docs/svyazi-2-0/ensembles/E-execution-plane.md)
> > > Источник: deep-research-report (1).md.

  - Схема
  - Ожидаемые новые свойства

_Слов: 253_

### [Ансамбль F — Evidence‑Backed Community Intake](docs/svyazi-2-0/ensembles/F-evidence-backed-intake.md)
> > > Источник: deep-research-report (3).md (ансамбли «второго порядка»).

  - Схема
  - Новые свойства

_Слов: 262_

### [Ансамбль G — Federated Local‑First Community Graph](docs/svyazi-2-0/ensembles/G-federated-local-graph.md)
> > > Источник: deep-research-report (3).md.

  - Схема
  - Новое свойство

_Слов: 268_

### [Ансамбль H — Research‑to‑Product Flywheel](docs/svyazi-2-0/ensembles/H-research-to-product-flywheel.md)
> > > Источник: deep-research-report (3).md.

  - Схема
  - Новое свойство

_Слов: 234_

### [Ансамбли проектов](docs/svyazi-2-0/ensembles/README.md)
> Файлов: 8

  - Содержание

_Слов: 54_

### [limitations](docs/svyazi-2-0/limitations/README.md)
> Файлов: 3

  - Содержание

_Слов: 22_

### [Итоговые выводы и порядок сборки](docs/svyazi-2-0/limitations/conclusions.md)
> > > Источники: deep-research-report (1).md (раздел «Выводы») и итог из deep-research-report (3).md.

  - Главный вывод первой части
  - Порядок практической сборки
  - Главный вывод второй части

_Слов: 318_

### [Что пока лучше не склеивать](docs/svyazi-2-0/limitations/do-not-glue.md)
> > !WARNING

  - Оркестрация — выбрать один spine
  - Voice/local‑first mesh — не идеализировать
  - Self‑improvement — только после метрики

_Слов: 343_

### [Лицензионные развилки](docs/svyazi-2-0/limitations/license-tree.md)
> > !WARNING

  - Развилки в коротком виде

_Слов: 324_

### [outreach](docs/svyazi-2-0/outreach/README.md)
> Файлов: 3

  - Содержание

_Слов: 22_

### [Первые контакты](docs/svyazi-2-0/outreach/first-contacts.md)
> > !TIP


_Слов: 259_

### [Шаблон первого сообщения](docs/svyazi-2-0/outreach/message-template.md)
> > !TIP

  - Замечание

_Слов: 248_

### [Узкие вопросы для каждого автора](docs/svyazi-2-0/outreach/narrow-questions.md)
> > > Источник: deep-research-report (3).md, раздел «Контактная стратегия и узкие вопросы для авторов».

  - Адресные вопросы

_Слов: 306_

### [overview](docs/svyazi-2-0/overview/README.md)
> Файлов: 4

  - Содержание

_Слов: 27_

### [Что добавляет продолжение исследования](docs/svyazi-2-0/overview/continuation-intro.md)
> > > Источник: deep-research-report (3).md, раздел «Что это продолжение добавляет».


_Слов: 242_

### [Executive summary](docs/svyazi-2-0/overview/executive-summary.md)
> > !TIP


_Слов: 376_

### [Методика и рамка отбора](docs/svyazi-2-0/overview/methodology.md)
> > !TIP


_Слов: 268_

### [Карта найденных проектов и паттернов](docs/svyazi-2-0/overview/projects-map.md)
> > !TIP


_Слов: 1285_

### [prototype](docs/svyazi-2-0/prototype/README.md)
> Файлов: 3

  - Содержание

_Слов: 21_

### [План MVP-прототипа](docs/svyazi-2-0/prototype/mvp-plan.md)
> > !TIP

  - Минимальная сборка прототипа

_Слов: 312_

### [Ключевые риски и как их закрывать](docs/svyazi-2-0/prototype/risks.md)
> > !TIP


_Слов: 287_

### [Дорожная карта прототипа](docs/svyazi-2-0/prototype/roadmap.md)
> > !TIP

  - Содержание
  - Итерация 1 — Evidence-first card graph
  - Итерация 2 — Memory governance
  - Итерация 3 — Orchestration + federation
  - Сводная таблица
  - Главный инженерный вывод

_Слов: 609_

### [security](docs/svyazi-2-0/security/README.md)
> Файлов: 3

  - Содержание

_Слов: 21_

### [Практичный бюджетный роутинг моделей](docs/svyazi-2-0/security/budget-routing.md)
> > !WARNING

  - Обоснование
  - Три режима

_Слов: 329_

### [Что стоит зафиксировать как default policy](docs/svyazi-2-0/security/default-policy.md)
> > !WARNING


_Слов: 349_

### [Приватность: local-first by default](docs/svyazi-2-0/security/privacy.md)
> > !WARNING


_Слов: 124_

**Итого в секции: 12,455 слов, 59 файлов**


## 📁 Technology Combinations (`docs/technology-combinations/`)

### [technology-combinations/ — комбинирование технологий для новых свойств](docs/technology-combinations/README.md)
> Файл в корне репозитория: Комбинирование технологий для новых свойств - Claude(../../%D0%9A%D0%BE%D0%BC%D0%B1%D0%B8%D0%B…

  - Источник
  - Подпапки
  - Главная находка диалога
  - См. также

_Слов: 155_

### [Комбинация 1: Правильная агентская архитектура × Svyazi-паттерн](docs/technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 230_

### [Комбинация 2: Мультиагентный хаос-решение × Auto AI Router](docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 171_

### [Комбинация 3: CRDT local-first × Svyazi CardIndex](docs/technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 181_

### [Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура](docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 200_

### [Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной](docs/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 196_

### [Комбинация 6: OpenClaude (утёкший Claude Code) × ZINC inference engine × MoME-роутер](docs/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 202_

### [Комбинация 7: Crawl4AI × Docling × Yodoca consolidator](docs/technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 183_

### [Комбинация 8: Conductor × adversarial-review × Auto AI Router](docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 668_

### [Комбинация 9: Agent Orchestration Stack](docs/technology-combinations/combinations/09-agent-orchestration-stack.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 180_

### [Комбинация 10: Legal Document Intelligence Pipeline](docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 182_

### [Комбинация 11: Hybrid CRDT-SQL Database](docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 173_

### [Комбинация 12: Multi-Agent Observability Stack](docs/technology-combinations/combinations/12-multi-agent-observability-stack.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 165_

### [Комбинация 13: Legal Document Transpiler](docs/technology-combinations/combinations/13-legal-document-transpiler.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 164_

### [Комбинация 14: local-first Agent Development Environment](docs/technology-combinations/combinations/14-local-first-agent-development-environment.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 559_

### [Комбинация 15: Self-Consolidating Legal Corpus](docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 210_

### [Комбинация 16: Adversarial Multi-Agent Code Review](docs/technology-combinations/combinations/16-adversarial-multi-agent-code-review.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 254_

### [Комбинация 17: Distributed Agent Memory with Graph](docs/technology-combinations/combinations/17-distributed-agent-memory-with-graph.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 209_

### [Комбинация 18: LLM-Powered Legal Corpus Builder](docs/technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Crawl4AI pipeline
- Svyazi deduplication

_Слов: 210_

### [Комбинация 19: Multi-Agent Observability Platform](docs/technology-combinations/combinations/19-multi-agent-observability-platform.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 678_

### [Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync](docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 240_

### [Комбинация 21: Legal Corpus Analytics at Scale](docs/technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Pipeline
- Schema
- Analytics queries (subsecond)

_Слов: 233_

### [Комбинация 22: Russian-International OSS Stack](docs/technology-combinations/combinations/22-russian-international-oss-stack.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 197_

### [Комбинация 23: Security-First Code Review Pipeline](docs/technology-combinations/combinations/23-security-first-code-review-pipeline.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 183_

### [Комбинация 24: MEGA-INTEGRATION: Full Stack](docs/technology-combinations/combinations/24-mega-integration-full-stack.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 594_

### [Комбинация 25: Legal DSL → Code Transpiler](docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- DSL syntax (natural language-like)
- DSL operations
- Output: ready Widerspruch.docx
- DSL for conversion

_Слов: 236_

### [Комбинация 26: AST-Based Code Analysis for Legal Automation](docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md)
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

### [Комбинация 27: Hybrid RAG with AST-Chunked Code](docs/technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 204_

### [Комбинация 28: Pydantic-Enforced Legal Workflows](docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Sequential pipeline with Pydantic validation at each stage

_Слов: 209_

### [Комбинация 29: Meta-Programmatic Legal Template Generator](docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).

- Legal DSL (declarative)
- Compiler generates Python code
- auto-generated rendering logic

_Слов: 198_

### [Комбинация 30: MEGA-STACK 3.0 with DSL & AST](docs/technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 489_

### [Комбинация 31: Event-Sourced Legal Document History](docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 229_

### [Комбинация 32: Consensus-Based Multi-Agent Coordination](docs/technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md)
> > !TIP


_Слов: 244_

### [Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics](docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 205_

### [Комбинация 34: Distributed Event Store with Paxos](docs/technology-combinations/combinations/34-distributed-event-store-with-paxos.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude (корень репозитория).


_Слов: 177_

### [Комбинация 35: MEGA-STACK 4.0 with Event Sourcing & Consensus](docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md)
> > !TIP

- Events
- Event Store
- Time-travel query

_Слов: 483_

### [combinations](docs/technology-combinations/combinations/README.md)
> Файлов: 35

  - Содержание

_Слов: 214_

### [Mega‑Stack 1.0 — Полный Legal‑AI Stack](docs/technology-combinations/mega-stacks/01-legal-ai-stack.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «MEGA‑COMBINATION: Полный Legal‑…

  - Результат
  - Первый проект для внедрения

_Слов: 211_

### [Mega‑Stack 2.0 — Ultimate Legal‑AI System](docs/technology-combinations/mega-stacks/02-ultimate-legal-ai.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «MEGA‑STACK 2.0: Ultimate Legal‑…

  - Capabilities
  - First implementation priority

_Слов: 318_

### [Mega‑Stack 3.0 — with DSL & AST](docs/technology-combinations/mega-stacks/03-dsl-ast.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «КОМБИНАЦИЯ 30: MEGA‑STACK 3.0 w…

  - New capabilities

_Слов: 226_

### [Mega‑Stack 4.0 — with Event Sourcing & Consensus](docs/technology-combinations/mega-stacks/04-event-sourcing-consensus.md)
> > !TIP

  - New capabilities
  - Performance

_Слов: 313_

### [mega-stacks](docs/technology-combinations/mega-stacks/README.md)
> Файлов: 4

  - Содержание

_Слов: 29_

### [properties/ — эмерджентные свойства](docs/technology-combinations/properties/README.md)
> Один файл — одно свойство, которое возникает только при комбинировании нескольких технологий.

  - Шаблон файла
- <Название свойства>
  - Что это
  - Какие компоненты дают это свойство в комбинации
  - Почему ни один из них в отдельности не даёт свойства
  - Как проверить, что свойство реально появилось

_Слов: 68_

### [research-reports](docs/technology-combinations/research-reports/README.md)
> Файлов: 2

  - Содержание

_Слов: 18_

### [Research Report: Continuation — 10 New Domains Beyond the Original 45 Combinations](docs/technology-combinations/research-reports/continuation-10-domains.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «Continuation Research — 10 New …

  - 10 новых технологических областей
  - 35+ новых синергетических комбинаций
  - 5 кросс‑сквозных эмерджентных архитектур
  - Методологические оговорки
  - Применение к Sozialrecht
  - Артефакт документа
  - Итоговый объём исследования

_Слов: 316_

### [Research Report: Sozialrecht (35 комбинаций)](docs/technology-combinations/research-reports/sozialrecht-35-combinations.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «A Research Report Building on 3…

  - Что в отчёте
  - Артефакт документа

_Слов: 222_

### [Сводная таблица 1–8](docs/technology-combinations/synthesis-tables/01-08-summary.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция 📊 «Сводная таблица синергии».

  - 🎯 Главная находка: паттерн «скромные родители → мощные дети»
  - Рекомендация

_Слов: 383_

### [Сводная таблица 9–14 (Extended)](docs/technology-combinations/synthesis-tables/09-14-extended.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «SYNTHESIS TABLE (Extended)».


_Слов: 195_

### [Сводная таблица 15–19 (Extended)](docs/technology-combinations/synthesis-tables/15-19-extended.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «EXTENDED SYNTHESIS TABLE».


_Слов: 162_

### [Сводная таблица 20–24 (Final 1–24)](docs/technology-combinations/synthesis-tables/20-24-final.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «FINAL SYNTHESIS TABLE (Complete…

  - Рекомендация

_Слов: 212_

### [Сводная таблица 25–30 (Complete 1–30)](docs/technology-combinations/synthesis-tables/25-30-extended.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «EXTENDED SYNTHESIS TABLE (Compl…

  - Рекомендация

_Слов: 228_

### [Сводная таблица 31–35 (Complete 1–35)](docs/technology-combinations/synthesis-tables/31-35-final.md)
> > > Источник: MHTML‑снимок Комбинирование технологий для новых свойств - Claude, секция «EXTENDED SYNTHESIS TABLE (Compl…

  - Рекомендация
- Events
- Event Store (append-only)
- Time-travel query

_Слов: 249_

### [synthesis-tables](docs/technology-combinations/synthesis-tables/README.md)
> Файлов: 6

  - Содержание

_Слов: 42_

**Итого в секции: 12,903 слов, 53 файлов**


## 📁 Templates (`docs/templates/`)

### [Шаблоны документов](docs/templates/README.md)
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

_Слов: 122_

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

_Слов: 80_

**Итого в секции: 635 слов, 6 файлов**


## 🗺️ Тематическая карта

### Архитектура (563 документов)
- [`365-развёрнутый-анализ-внуковой-комбинации`](docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md)
- [`CONCEPTS`](docs/CONCEPTS.md)
- [`TABLES`](docs/TABLES.md)
- [`00-intro`](docs/02-anthropic-vacancies/00-intro.md)
- [`01-интегральный-анализ-профиля-svend4`](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)
- _... ещё 558_

### Агенты (153 документов)
- [`C-multi-agent-factory`](docs/svyazi-2-0/ensembles/C-multi-agent-factory.md)
- [`107-1-контекст-и-мотивация`](docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md)
- [`108-2-формальный-workflow`](docs/02-anthropic-vacancies/108-2-формальный-workflow.md)
- [`345-кто-ты`](docs/02-anthropic-vacancies/345-кто-ты.md)
- [`00-question-what-is-hermes`](docs/anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md)
- _... ещё 148_

### Проекты (138 документов)
- [`TIMELINE`](docs/TIMELINE.md)
- [`02-общий-план-развития-nautilus-portal-protocol`](docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md)
- [`228-appendix-c-quick-start-architecture-for-sgb-advoca`](docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md)
- [`299-практические-рекомендации-для-текущего-проекта`](docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md)
- [`336-10-стратегическое-позиционирование`](docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md)
- _... ещё 133_

### Документация (75 документов)
- [`CODE_BLOCKS`](docs/CODE_BLOCKS.md)
- [`118-appendix-a-шаблон-для-header-warning`](docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md)
- [`98-appendix-a-minimal-working-example`](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md)
- [`22-glossary`](docs/nautilus/npp-v1-1/22-glossary.md)
- [`12-appendix-a-header-warning`](docs/nautilus/review-methodology/12-appendix-a-header-warning.md)
- _... ещё 70_

### Контакты (54 документов)
- [`ngt-memory`](docs/05-habr-projects/memory/ngt-memory.md)
- [`06-1-introduction`](docs/02-anthropic-vacancies/06-1-introduction.md)
- [`105-review-methodology-md`](docs/02-anthropic-vacancies/105-review-methodology-md.md)
- [`163-9-call-for-partnership`](docs/02-anthropic-vacancies/163-9-call-for-partnership.md)
- [`178-9-phased-rollout-strategy`](docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md)
- _... ещё 49_

### Память (43 документов)
- [`11-integration-contracts`](docs/01-svyazi/11-integration-contracts.md)
- [`174-5-architectural-specification`](docs/02-anthropic-vacancies/174-5-architectural-specification.md)
- [`NARRATIVE`](docs/NARRATIVE.md)
- [`REPORT`](docs/REPORT.md)
- [`source-projects`](docs/ai-collaborations/source-projects.md)
- _... ещё 38_

### Код (37 документов)
- [`CHANGELOG`](docs/CHANGELOG.md)
- [`DEPENDENCY_MAP`](docs/DEPENDENCY_MAP.md)
- [`83-8-q6-space-normative`](docs/02-anthropic-vacancies/83-8-q6-space-normative.md)
- [`84-9-consensus-algorithm`](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md)
- [`90-15-security-considerations`](docs/02-anthropic-vacancies/90-15-security-considerations.md)
- _... ещё 32_

### Анализ (16 документов)
- [`110-вопрос-fallback-ratio-как-критический-или-осмыслен`](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md)
- [`COMPARE`](docs/COMPARE.md)
- [`DIGEST_AUTO`](docs/DIGEST_AUTO.md)
- [`DIGEST_WEEKLY`](docs/DIGEST_WEEKLY.md)
- [`README`](docs/anthropic-vacancies/profile-mapping/README.md)
- _... ещё 11_


<!-- similar-docs -->

---

**Похожие документы:**
- [PARAGRAPH_QUALITY](docs/PARAGRAPH_QUALITY.md) (сходство 0.41)
- [OUTLINE](docs/obsidian/OUTLINE.md) (сходство 0.35)
- [HEADING_AUDIT](docs/HEADING_AUDIT.md) (сходство 0.30)

