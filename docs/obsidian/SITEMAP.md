---
title: "Карта репозитория Lorenzo"
tags:
  - general
date: 2026-05-10
---

# Карта репозитория Lorenzo

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> - [Мета-документы](#мета-документы)
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, Rufler, LiteParse

---

<!-- toc -->
## Содержание

- [Навигация](#навигация)
- [Мета-документы](#мета-документы)
- [Svyazi 2.0 — Архитектура системы](#svyazi-20-архитектура-системы)
- [Вакансии Anthropic — 436 позиций](#вакансии-anthropic-436-позиций)
- [Комбинации технологий](#комбинации-технологий)
- [AI Коллаборации — ансамбли проектов](#ai-коллаборации-ансамбли-проектов)
- [Хабр-проекты — память и граф](#хабр-проекты-память-и-граф)
- [ai-collaborations](#ai-collaborations)
- [anthropic-vacancies](#anthropic-vacancies)
- [autofilled](#autofilled)
- [contacts](#contacts)
- [glossary](#glossary)
- [habr-unique-projects](#habr-unique-projects)
- [lorenzo-agent](#lorenzo-agent)
- [meta-scripting](#meta-scripting)
- [nautilus](#nautilus)
- [obsidian](#obsidian)
- [processing-guide](#processing-guide)
- [svyazi-2-0](#svyazi-2-0)
- [technology-combinations](#technology-combinations)
- [templates](#templates)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->




_Обновлено: 2026-05-10_

**Всего файлов:** 1739

## Навигация

- [Мета-документы](#мета-документы)
- [Svyazi 2.0 — Архитектура системы](#svyazi-20-архитектура-системы)
- [Вакансии Anthropic — 436 позиций](#вакансии-anthropic-436-позиций)
- [Комбинации технологий](#комбинации-технологий)
- [AI Коллаборации — ансамбли проектов](#ai-коллаборации-ансамбли-проектов)
- [Хабр-проекты — память и граф](#хабр-проекты-память-и-граф)
- [ai-collaborations](#ai-collaborations)
- [anthropic-vacancies](#anthropic-vacancies)
- [autofilled](#autofilled)
- [contacts](#contacts)
- [glossary](#glossary)
- [habr-unique-projects](#habr-unique-projects)
- [lorenzo-agent](#lorenzo-agent)
- [meta-scripting](#meta-scripting)
- [nautilus](#nautilus)
- [obsidian](#obsidian)
- [processing-guide](#processing-guide)
- [svyazi-2-0](#svyazi-2-0)
- [technology-combinations](#technology-combinations)
- [templates](#templates)

---

## Мета-документы

| Документ | Описание | Слов |
|----------|----------|------|
| [[ABBREVIATIONS|ABBREVIATIONS.md]] | — | 1697 |
| [[ACTION_ITEMS|ACTION_ITEMS.md]] | Задачи и риски (490) | 9180 |
| [[ACTION_ITEMS|ACTION_ITEMS.md]] | Задачи и риски (490) | 8127 |
| [[ALERTS|ALERTS.md]] | — | 79 |
| [[AUTHORS|AUTHORS.md]] | Авторы и контакты | 158 |
| [[AUTHORS|AUTHORS.md]] | Авторы и контакты | 169 |
| [[AUTOFILLED|AUTOFILLED.md]] | — | 187 |
| [[BACKLINKS|BACKLINKS.md]] | — | 527 |
| [[BADGES|BADGES.md]] | — | 42 |
| [[BROKEN_LINKS|BROKEN_LINKS.md]] | Сломанные ссылки (26) | 746 |
| [[CHANGELOG|CHANGELOG.md]] | История изменений | 2285 |
| [[CHANGELOG|CHANGELOG.md]] | История изменений | 1560 |
| [[CHANGELOG_AUTO|CHANGELOG_AUTO.md]] | — | 681 |
| [[CITATION_INDEX|CITATION_INDEX.md]] | — | 1045 |
| [[CLUSTERS|CLUSTERS.md]] | Кластеры (384 → 120 групп) | 1409 |
| [[CLUSTERS|CLUSTERS.md]] | Кластеры (384 → 120 групп) | 1408 |
| [[CODE_BLOCKS|CODE_BLOCKS.md]] | — | 5259 |
| [[CODE_BLOCKS|CODE_BLOCKS.md]] | — | 5313 |
| [[COMPARE|COMPARE.md]] | Сравнение с предыдущим коммитом | 477 |
| [[COMPARE|COMPARE.md]] | Сравнение с предыдущим коммитом | 498 |
| [[COMPLEXITY|COMPLEXITY.md]] | Оценка читаемости | 605 |
| [[COMPLEXITY|COMPLEXITY.md]] | Оценка читаемости | 642 |
| [[COMPONENT_MATRIX|COMPONENT_MATRIX.md]] | — | 1051 |
| [[CONCEPTS|CONCEPTS.md]] | Глоссарий понятий (888) | 13914 |
| [[CONCEPTS|CONCEPTS.md]] | Глоссарий понятий (888) | 13271 |
| [[CONCEPT_GRAPH|CONCEPT_GRAPH.md]] | — | 697 |
| [[CONSISTENCY|CONSISTENCY.md]] | — | 495 |
| [[CONSISTENCY|CONSISTENCY.md]] | — | 397 |
| [[CONTACTS|CONTACTS.md]] | Контакты (15 авторов) | 552 |
| [[CONTACTS|CONTACTS.md]] | Контакты (15 авторов) | 593 |
| [[CONTACT_PRIORITY|CONTACT_PRIORITY.md]] | — | 412 |
| [[CONTENT_GAPS|CONTENT_GAPS.md]] | — | 886 |
| [[CONTRADICTIONS|CONTRADICTIONS.md]] | — | 2071 |
| [[COST|COST.md]] | — | 600 |
| [[COVERAGE|COVERAGE.md]] | — | 310 |
| [[CROSSREFS|CROSSREFS.md]] | Перекрёстные ссылки проектов | 653 |
| [[CROSSREFS|CROSSREFS.md]] | Перекрёстные ссылки проектов | 665 |
| [[CROSS_SECTION|CROSS_SECTION.md]] | — | 1256 |
| [[DECISIONS|DECISIONS.md]] | Ключевые решения (150) | 2567 |
| [[DECISIONS|DECISIONS.md]] | Ключевые решения (150) | 2493 |
| [[DENSITY|DENSITY.md]] | Карта плотности тем | 650 |
| [[DENSITY|DENSITY.md]] | Карта плотности тем | 694 |
| [[DEPENDABOT|DEPENDABOT.md]] | — | 173 |
| [[DEPENDENCY_MAP|DEPENDENCY_MAP.md]] | — | 1157 |
| [[DIGEST|DIGEST.md]] | — | 360 |
| [[DIGEST_AUTO|DIGEST_AUTO.md]] | — | 315 |
| [[DIGEST_WEEKLY|DIGEST_WEEKLY.md]] | — | 232 |
| [[DUPLICATES|DUPLICATES.md]] | — | 2324 |
| [[DUPLICATES|DUPLICATES.md]] | — | 2936 |
| [[EMPTY_SECTIONS|EMPTY_SECTIONS.md]] | — | 15794 |
| [[ENTITIES|ENTITIES.md]] | Именованные сущности | 742 |
| [[ENTITIES|ENTITIES.md]] | Именованные сущности | 815 |
| [[FAQ|FAQ.md]] | — | 892 |
| [[FOOTNOTES|FOOTNOTES.md]] | — | 275 |
| [[GITHUB_ISSUES|GITHUB_ISSUES.md]] | — | 1754 |
| [[GLOSSARY|GLOSSARY.md]] | Глоссарий проектов (33 записи) | 222 |
| [[GLOSSARY|GLOSSARY.md]] | Глоссарий проектов (33 записи) | 214 |
| [[GRAPH|GRAPH.md]] | Граф связей проектов | 2655 |
| [[GRAPH|GRAPH.md]] | Граф связей проектов | 2679 |
| [[HEADING_AUDIT|HEADING_AUDIT.md]] | — | 9317 |
| [[HEALTH|HEALTH.md]] | Дашборд здоровья (75/100) | 236 |
| [[HEALTH|HEALTH.md]] | Дашборд здоровья (75/100) | 230 |
| [[HEATMAP|HEATMAP.md]] | — | 537 |
| [[INDEX|INDEX.md]] | — | 694 |
| [[KEYWORD_INDEX|KEYWORD_INDEX.md]] | — | 1162 |
| [[KNOWLEDGE_MAP|KNOWLEDGE_MAP.md]] | — | 616 |
| [[KPI|KPI.md]] | Числовые KPI (737 показателей) | 2736 |
| [[KPI|KPI.md]] | Числовые KPI (737 показателей) | 2596 |
| [[KPI_HISTORY|KPI_HISTORY.md]] | — | 128 |
| [[LANGUAGE_STATS|LANGUAGE_STATS.md]] | — | 6783 |
| [[LINKS|LINKS.md]] | Внешние ссылки | 1060 |
| [[LINKS|LINKS.md]] | Внешние ссылки | 1039 |
| [[LLM_SUMMARIES|LLM_SUMMARIES.md]] | — | 300 |
| [[MCP_DASHBOARD|MCP_DASHBOARD.md]] | — | 327 |
| [[METHODOLOGY|METHODOLOGY.md]] | — | 998 |
| [[METRICS|METRICS.md]] | — | 475 |
| [[MINDMAP|MINDMAP.md]] | Майндмап в Mermaid | 242 |
| [[MINDMAP|MINDMAP.md]] | Майндмап в Mermaid | 267 |
| [[MISSING|MISSING.md]] | Пробелы знаний | 434 |
| [[MISSING|MISSING.md]] | Пробелы знаний | 457 |
| [[NAMED_ENTITIES|NAMED_ENTITIES.md]] | — | 1640 |
| [[NARRATIVE|NARRATIVE.md]] | — | 1055 |
| [[NETWORK|NETWORK.md]] | — | 414 |
| [[ONBOARDING|ONBOARDING.md]] | — | 576 |
| [[ORPHANS|ORPHANS.md]] | — | 302 |
| [[OUTLINE|OUTLINE.md]] | — | 20073 |
| [[PARAGRAPH_QUALITY|PARAGRAPH_QUALITY.md]] | — | 10093 |
| [[PASSIVE_VOICE|PASSIVE_VOICE.md]] | — | 408 |
| [[PRIORITIES|PRIORITIES.md]] | Приоритеты (TF-IDF) | 3158 |
| [[PRIORITIES|PRIORITIES.md]] | Приоритеты (TF-IDF) | 3224 |
| [[PROGRESS|PROGRESS.md]] | — | 332 |
| [[PROTOTYPE_SPEC|PROTOTYPE_SPEC.md]] | — | 1377 |
| [[QA|QA.md]] | Вопросы и ответы | 224 |
| [[QA|QA.md]] | Вопросы и ответы | 323 |
| [[QA|QA.md]] | Вопросы и ответы | 133 |
| [[QA|QA.md]] | Вопросы и ответы | 250 |
| [[QA|QA.md]] | Вопросы и ответы | 138 |
| [[QA|QA.md]] | Вопросы и ответы | 1975 |
| [[QA|QA.md]] | Вопросы и ответы | 115 |
| [[QA|QA.md]] | Вопросы и ответы | 206 |
| [[QA|QA.md]] | Вопросы и ответы | 71 |
| [[QA|QA.md]] | Вопросы и ответы | 244 |
| [[QA|QA.md]] | Вопросы и ответы | 803 |
| [[QA|QA.md]] | Вопросы и ответы | 209 |
| [[QA|QA.md]] | Вопросы и ответы | 246 |
| [[QA|QA.md]] | Вопросы и ответы | 352 |
| [[QA|QA.md]] | Вопросы и ответы | 336 |
| [[QA|QA.md]] | Вопросы и ответы | 219 |
| [[QUESTIONS|QUESTIONS.md]] | Открытые вопросы (484) | 1852 |
| [[QUESTIONS|QUESTIONS.md]] | Открытые вопросы (484) | 23070 |
| [[READABILITY|READABILITY.md]] | — | 26181 |
| [[READING_LIST|READING_LIST.md]] | — | 232 |
| [[READING_ORDER|READING_ORDER.md]] | Рекомендуемый порядок чтения | 5947 |
| [[READING_ORDER|READING_ORDER.md]] | Рекомендуемый порядок чтения | 5997 |
| [[READING_TIME|READING_TIME.md]] | — | 11356 |
| [[README|README.md]] | Главная страница и навигация | 342 |
| [[README|README.md]] | Главная страница и навигация | 2242 |
| [[README|README.md]] | Главная страница и навигация | 65 |
| [[README|README.md]] | Главная страница и навигация | 366 |
| [[README|README.md]] | Главная страница и навигация | 96 |
| [[README|README.md]] | Главная страница и навигация | 55 |
| [[README|README.md]] | Главная страница и навигация | 94 |
| [[README|README.md]] | Главная страница и навигация | 847 |
| [[README|README.md]] | Главная страница и навигация | 39 |
| [[README|README.md]] | Главная страница и навигация | 23 |
| [[README|README.md]] | Главная страница и навигация | 25 |
| [[README|README.md]] | Главная страница и навигация | 61 |
| [[README|README.md]] | Главная страница и навигация | 60 |
| [[README|README.md]] | Главная страница и навигация | 311 |
| [[README|README.md]] | Главная страница и навигация | 32 |
| [[README|README.md]] | Главная страница и навигация | 72 |
| [[README|README.md]] | Главная страница и навигация | 69 |
| [[README|README.md]] | Главная страница и навигация | 77 |
| [[README|README.md]] | Главная страница и навигация | 103 |
| [[README|README.md]] | Главная страница и навигация | 46 |
| [[README|README.md]] | Главная страница и навигация | 88 |
| [[README|README.md]] | Главная страница и навигация | 41 |
| [[README|README.md]] | Главная страница и навигация | 30 |
| [[README|README.md]] | Главная страница и навигация | 40 |
| [[README|README.md]] | Главная страница и навигация | 53 |
| [[README|README.md]] | Главная страница и навигация | 35 |
| [[README|README.md]] | Главная страница и навигация | 35 |
| [[README|README.md]] | Главная страница и навигация | 159 |
| [[README|README.md]] | Главная страница и навигация | 47 |
| [[README|README.md]] | Главная страница и навигация | 95 |
| [[README|README.md]] | Главная страница и навигация | 44 |
| [[README|README.md]] | Главная страница и навигация | 62 |
| [[README|README.md]] | Главная страница и навигация | 24 |
| [[README|README.md]] | Главная страница и навигация | 234 |
| [[README|README.md]] | Главная страница и навигация | 18 |
| [[README|README.md]] | Главная страница и навигация | 54 |
| [[README|README.md]] | Главная страница и навигация | 28 |
| [[README|README.md]] | Главная страница и навигация | 82 |
| [[README|README.md]] | Главная страница и навигация | 30 |
| [[README|README.md]] | Главная страница и навигация | 48 |
| [[README|README.md]] | Главная страница и навигация | 42 |
| [[README|README.md]] | Главная страница и навигация | 25 |
| [[README|README.md]] | Главная страница и навигация | 42 |
| [[README|README.md]] | Главная страница и навигация | 163 |
| [[README|README.md]] | Главная страница и навигация | 28 |
| [[README|README.md]] | Главная страница и навигация | 45 |
| [[README|README.md]] | Главная страница и навигация | 59 |
| [[README|README.md]] | Главная страница и навигация | 18 |
| [[README|README.md]] | Главная страница и навигация | 77 |
| [[README|README.md]] | Главная страница и навигация | 45 |
| [[README|README.md]] | Главная страница и навигация | 524 |
| [[README|README.md]] | Главная страница и навигация | 90 |
| [[README|README.md]] | Главная страница и навигация | 17 |
| [[README|README.md]] | Главная страница и навигация | 17 |
| [[README|README.md]] | Главная страница и навигация | 17 |
| [[README|README.md]] | Главная страница и навигация | 17 |
| [[README|README.md]] | Главная страница и навигация | 17 |
| [[README|README.md]] | Главная страница и навигация | 78 |
| [[README|README.md]] | Главная страница и навигация | 27 |
| [[README|README.md]] | Главная страница и навигация | 71 |
| [[README|README.md]] | Главная страница и навигация | 89 |
| [[README|README.md]] | Главная страница и навигация | 80 |
| [[README|README.md]] | Главная страница и навигация | 64 |
| [[README|README.md]] | Главная страница и навигация | 62 |
| [[README|README.md]] | Главная страница и навигация | 16 |
| [[README|README.md]] | Главная страница и навигация | 17 |
| [[README|README.md]] | Главная страница и навигация | 41 |
| [[README|README.md]] | Главная страница и навигация | 116 |
| [[README|README.md]] | Главная страница и навигация | 138 |
| [[README|README.md]] | Главная страница и навигация | 69 |
| [[README|README.md]] | Главная страница и навигация | 35 |
| [[README|README.md]] | Главная страница и навигация | 82 |
| [[README|README.md]] | Главная страница и навигация | 78 |
| [[README|README.md]] | Главная страница и навигация | 81 |
| [[README|README.md]] | Главная страница и навигация | 77 |
| [[README|README.md]] | Главная страница и навигация | 97 |
| [[README|README.md]] | Главная страница и навигация | 17 |
| [[README|README.md]] | Главная страница и навигация | 16 |
| [[README|README.md]] | Главная страница и навигация | 124 |
| [[README|README.md]] | Главная страница и навигация | 2220 |
| [[README|README.md]] | Главная страница и навигация | 62 |
| [[README|README.md]] | Главная страница и навигация | 113 |
| [[README|README.md]] | Главная страница и навигация | 54 |
| [[README|README.md]] | Главная страница и навигация | 49 |
| [[README|README.md]] | Главная страница и навигация | 83 |
| [[README|README.md]] | Главная страница и навигация | 391 |
| [[README|README.md]] | Главная страница и навигация | 16 |
| [[README|README.md]] | Главная страница и навигация | 46 |
| [[README|README.md]] | Главная страница и навигация | 69 |
| [[README|README.md]] | Главная страница и навигация | 62 |
| [[README|README.md]] | Главная страница и навигация | 26 |
| [[README|README.md]] | Главная страница и навигация | 103 |
| [[README|README.md]] | Главная страница и навигация | 158 |
| [[README|README.md]] | Главная страница и навигация | 46 |
| [[README|README.md]] | Главная страница и навигация | 120 |
| [[README|README.md]] | Главная страница и навигация | 54 |
| [[README|README.md]] | Главная страница и навигация | 22 |
| [[README|README.md]] | Главная страница и навигация | 22 |
| [[README|README.md]] | Главная страница и навигация | 27 |
| [[README|README.md]] | Главная страница и навигация | 21 |
| [[README|README.md]] | Главная страница и навигация | 21 |
| [[README|README.md]] | Главная страница и навигация | 155 |
| [[README|README.md]] | Главная страница и навигация | 214 |
| [[README|README.md]] | Главная страница и навигация | 29 |
| [[README|README.md]] | Главная страница и навигация | 68 |
| [[README|README.md]] | Главная страница и навигация | 18 |
| [[README|README.md]] | Главная страница и навигация | 42 |
| [[README|README.md]] | Главная страница и навигация | 82 |
| [[REGISTRY|REGISTRY.md]] | — | 1347 |
| [[REPORT|REPORT.md]] | — | 965 |
| [[RISK_REGISTER|RISK_REGISTER.md]] | — | 1088 |
| [[SCHEDULE|SCHEDULE.md]] | — | 348 |
| [[SCORING|SCORING.md]] | — | 405 |
| [[SCRIPTS_CATALOG|SCRIPTS_CATALOG.md]] | — | 7281 |
| [[SEARCH|SEARCH.md]] | Поисковый индекс | 9457 |
| [[SEARCH_RESULTS|SEARCH_RESULTS.md]] | — | 73 |
| [[SEE_ALSO|SEE_ALSO.md]] | — | 220 |
| [[SENTIMENT|SENTIMENT.md]] | — | 561 |
| [[SIMILAR|SIMILAR.md]] | Похожие документы (937 пар) | 341 |
| [[SIMILAR|SIMILAR.md]] | Похожие документы (937 пар) | 363 |
| [[SIMILAR_PASSAGES|SIMILAR_PASSAGES.md]] | — | 1931 |
| [[SKILL_DASHBOARD|SKILL_DASHBOARD.md]] | — | 35 |
| [[SOURCE_MAP|SOURCE_MAP.md]] | — | 5728 |
| [[SPELLCHECK|SPELLCHECK.md]] | — | 346 |
| [[STALENESS|STALENESS.md]] | — | 448 |
| [[STATS|STATS.md]] | Детальная статистика | 681 |
| [[STATS|STATS.md]] | Детальная статистика | 667 |
| [[SUMMARIES|SUMMARIES.md]] | — | 3910 |
| [[TABLES|TABLES.md]] | — | 192814 |
| [[TABLES|TABLES.md]] | — | 119650 |
| [[TAGS|TAGS.md]] | Теги (316 файлов, 12 тем) | 600 |
| [[TAGS|TAGS.md]] | Теги (316 файлов, 12 тем) | 610 |
| [[TASKS_INDEX|TASKS_INDEX.md]] | — | 1012 |
| [[TECH_RADAR|TECH_RADAR.md]] | — | 684 |
| [[TIMELINE|TIMELINE.md]] | Временная шкала (800 маркеров) | 4470 |
| [[TIMELINE|TIMELINE.md]] | Временная шкала (800 маркеров) | 2185 |
| [[TOPIC_MODEL|TOPIC_MODEL.md]] | — | 1051 |
| [[VALIDATION|VALIDATION.md]] | — | 619 |
| [[VERSION_DIFF|VERSION_DIFF.md]] | — | 6259 |
| [[VOCABULARY|VOCABULARY.md]] | — | 946 |
| [[WORD_CLOUD|WORD_CLOUD.md]] | — | 234 |
| [[WORD_FREQ|WORD_FREQ.md]] | Частотный анализ слов | 3193 |
| [[WORD_FREQ|WORD_FREQ.md]] | Частотный анализ слов | 2898 |
| [[reading-paths|reading-paths.md]] | — | 627 |

## Svyazi 2.0 — Архитектура системы

_`docs/01-svyazi/` — 14 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-intro-part2|Продолжение исследования для Svyazi 2.0]] | 6 |
| 2 | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 726 |
| 3 | [[02-methodology|Методика и рамка отбора проектов]] | 480 |
| 4 | [[03-component-catalog]] | 1405 |
| 5 | [[04-ensembles-overview]] | 1288 |
| 6 | [[06-security-privacy]] | 823 |
| 7 | [[07-mvp-planning]] | 1083 |
| 8 | [[08-conclusions]] | 380 |
| 9 | [[09-architectural-gaps]] | 774 |
| 10 | [[10-second-order-ensembles]] | 924 |
| 11 | [[11-integration-contracts]] | 753 |
| 12 | [[12-roadmap]] | 722 |
| 13 | [[13-contacts]] | 1010 |
| 14 | [[14-limitations]] | 638 |

## Вакансии Anthropic — 436 позиций

_`docs/02-anthropic-vacancies/` — 355 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-intro|Введение]] | 9000 |
| 2 | [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]] | 19237 |
| 3 | [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]] | 3326 |
| 4 | [[03-portal-protocol-md|PORTAL-PROTOCOL.md]] | 347 |
| 5 | [[04-abstract|Abstract]] | 339 |
| 6 | [[05-0-status-of-this-document|0. Status of This Document]] | 325 |
| 7 | [[06-1-introduction|1. Introduction]] | 403 |
| 8 | [[07-2-terminology|2. Terminology]] | 324 |
| 9 | [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] | 427 |
| 10 | [[09-4-passport-passport-md|4. Passport (`passport.md`)]] | 324 |
| 11 | [[102-доступ-к-данным|Доступ к данным]] | 256 |
| 12 | [[103-appendix-b-change-log|Appendix B: Change Log]] | 333 |
| 13 | [[104-appendix-c-references|Appendix C: References]] | 1191 |
| 14 | [[105-review-methodology-md|REVIEW_METHODOLOGY.md]] | 300 |
| 15 | [[106-tl-dr|TL;DR]] | 236 |
| 16 | [[107-1-контекст-и-мотивация|1. Контекст и мотивация]] | 471 |
| 17 | [[108-2-формальный-workflow|2. Формальный workflow]] | 483 |
| 18 | [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]] | 697 |
| 19 | [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или осмысле]] | 338 |
| 20 | [[111-4-условия-применимости|4. Условия применимости]] | 292 |
| 21 | [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]] | 389 |
| 22 | [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assisted wor]] | 172 |
| 23 | [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]] | 308 |
| 24 | [[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]] | 447 |
| 25 | [[116-9-checklist-применения-методологии|9. Checklist применения методологии]] | 399 |
| 26 | [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим документа]] | 331 |
| 27 | [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]] | 215 |
| 28 | [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешения]] | 372 |
| 29 | [[12-content-overview|Content Overview]] | 211 |
| 30 | [[120-главные-технические-риски|Главные технические риски]] | 100 |
| 31 | [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]] | 250 |
| 32 | [[122-глоссарий|Глоссарий]] | 1539 |
| 33 | [[123-portal-mcp-py|portal-mcp.py]] | 2524 |
| 34 | [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]] | 263 |
| 35 | [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]] | 290 |
| 36 | [[126-установка|Установка]] | 163 |
| 37 | [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]] | 276 |
| 38 | [[128-доступные-инструменты|Доступные инструменты]] | 320 |
| 39 | [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]] | 320 |
| 40 | [[13-angle-perspective|Angle / Perspective]] | 238 |
| 41 | [[130-отладка|Отладка]] | 261 |
| 42 | [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]] | 197 |
| 43 | [[132-planned-v0-2-0|Planned (v0.2.0)]] | 252 |
| 44 | [[133-обратная-связь|Обратная связь]] | 17099 |
| 45 | [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]] | 310 |
| 46 | [[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in Distr]] | 291 |
| 47 | [[136-abstract|Abstract]] | 631 |
| 48 | [[137-table-of-contents|Table of Contents]] | 316 |
| 49 | [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]] | 613 |
| 50 | [[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]] | 779 |
| ... | _ещё 305 файлов_ | |

## Комбинации технологий

_`docs/03-technology-combinations/` — 5 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[01-agent-routing|Агентные системы и роутинг]] | 374 |
| 2 | [[02-knowledge-graphs|Графы знаний и Legal AI]] | 838 |
| 3 | [[03-local-first|Local-first и P2P стек]] | 560 |
| 4 | [[04-sozialrecht-domain|Домен: немецкое социальное право]] | 176 |
| 5 | [[05-benchmarks|Бенчмарки и производительность]] | 1013 |

## AI Коллаборации — ансамбли проектов

_`docs/04-ai-collaborations/` — 15 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-intro|Введение]] | 11407 |
| 2 | [[01-executive-summary|Executive summary]] | 593 |
| 3 | [[02-методика-и-рамка-отбора|Методика и рамка отбора]] | 459 |
| 4 | [[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]] | 1478 |
| 5 | [[04-приоритетные-ансамбли|Приоритетные ансамбли]] | 1358 |
| 6 | [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]] | 1150 |
| 7 | [[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]] | 903 |
| 8 | [[07-выводы|Выводы]] | 488 |
| 9 | [[08-что-это-продолжение-добавляет|Что это продолжение добавляет]] | 464 |
| 10 | [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых инструм]] | 839 |
| 11 | [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]] | 1002 |
| 12 | [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафиксирова]] | 864 |
| 13 | [[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]] | 787 |
| 14 | [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авторов]] | 892 |
| 15 | [[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|Ограничения, лицензии и что пока лучше не склеиват]] | 3274 |

## Хабр-проекты — память и граф

_`docs/05-habr-projects/` — 6 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[01-synthesis|Синтез: как проекты собираются вместе]] | 263 |
| 2 | [[02-collaboration-partners|Авторы и контакты]] | 279 |
| 3 | [[wikontic|Wikontic: семантический граф]] | 385 |
| 4 | [[memnet|MemNet: исследовательская память]] | 7264 |
| 5 | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 382 |
| 6 | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 379 |

## ai-collaborations

_`docs/ai-collaborations/` — 23 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[01-three-key-candidates|Три ключевых кандидата: K2-18, Wikontic, NGT Memor]] | 353 |
| 2 | [[02-related-projects-context|Смежные проекты в контексте]] | 194 |
| 3 | [[03-synthesis-hebbian-collaboration-graph|Синтез: хеббовский граф людей-навыков-идей]] | 264 |
| 4 | [[01-shared-memory-between-agents|Общая память между агентами (CoAlly + ансамбль F)]] | 431 |
| 5 | [[02-agentops-trace-envelope|AgentOps и Trace Envelope (ансамбль G)]] | 398 |
| 6 | [[03-a2a-vs-mcp-protocols|A2A vs MCP, ансамбль H — MCP/A2A Review Fabric]] | 346 |
| 7 | [[04-memory-firewall-vs-prompt-worms|Memory Firewall против prompt worms (ансамбль I)]] | 266 |
| 8 | [[05-roadmap-6-12-months|Roadmap на 6–12 месяцев]] | 360 |
| 9 | [[06-metrics-tree|Дерево метрик Svyazi 2.0]] | 205 |
| 10 | [[07-vs-notion-mem-affine-langgraph|Чем Svyazi 2.0 отличается от Notion AI / Mem / AFF]] | 444 |
| 11 | [[08-commercialization-three-paths|Коммерциализация: три направления]] | 252 |
| 12 | [[09-do-not-glue|Что пока не стоит склеивать в один релиз]] | 250 |
| 13 | [[10-architecture-rfc|Следующий артефакт: Svyazi 2.0 Architecture RFC]] | 172 |
| 14 | [[1-agentic-knowledge-os|Ансамбль 1 — Agentic Knowledge OS]] | 407 |
| 15 | [[2-distributed-agent-workshop|Ансамбль 2 — Distributed Agent Workshop]] | 387 |
| 16 | [[3-forensic-rag|Ансамбль 3 — Forensic RAG]] | 409 |
| 17 | [[4-web-to-knowledge-pipeline|Ансамбль 4 — Web-to-Knowledge Pipeline]] | 309 |
| 18 | [[5-agent-firewall|Ансамбль 5 — Agent Firewall]] | 402 |
| 19 | [[6-continuous-eval-loop|Ансамбль 6 — Continuous Eval Loop]] | 330 |
| 20 | [[7-domain-agent-app-factory|Ансамбль 7 — Domain Agent App Factory]] | 294 |
| 21 | [[8-budget-aware-intelligence-stack|Ансамбль 8 — Budget-Aware Intelligence Stack]] | 277 |
| 22 | [[9-ambient-team-agent|Ансамбль 9 — Ambient Team Agent]] | 251 |
| 23 | [[source-projects|Source projects — все Хабр-источники в диалоге]] | 705 |

## anthropic-vacancies

_`docs/anthropic-vacancies/` — 97 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-question-rephrasing|Вопрос: разделить $500K зарплату на команду 5–10 ф]] | 909 |
| 2 | [[01-existing-landscape|Что уже существует (InnoCentive, Kaggle, Toptal, A]] | 327 |
| 3 | [[02-four-structural-blockers|Четыре структурные причины, почему это не работает]] | 339 |
| 4 | [[03-three-variants-A-B-C|Три варианта: A (staffing agency) → B (research co]] | 672 |
| 5 | [[04-what-to-do|Что с этим делать]] | 516 |
| 6 | [[05-polymath-project-tao-comparison|Сравнение с Terence Tao, Polymath Project]] | 1390 |
| 7 | [[06-angel-vs-demon-duality|Почему двойственность «ангел-хранитель + строгий д]] | 511 |
| 8 | [[07-current-implementations|Что существует сейчас в этом пространстве]] | 286 |
| 9 | [[08-pluses-of-model|Плюсы модели, если её построить]] | 244 |
| 10 | [[09-minuses-and-risks|Минусы и риски]] | 664 |
| 11 | [[10-three-entry-points|Три точки входа разной амбиции]] | 378 |
| 12 | [[00-context|Контекст: что такое Anthropic Beneficial Deploymen]] | 252 |
| 13 | [[01-section-1-problem|Section 1: Problem statement (Cinderella Syndrome ]] | 179 |
| 14 | [[02-section-2-beneficial-dimension|Section 2: Why this matters — beneficial dimension]] | 158 |
| 15 | [[03-section-3-solution-architecture|Section 3: Proposed solution architecture (existin]] | 172 |
| 16 | [[04-section-4-sgb-pilot|Section 4: Specific deployment — SGB Advocate Comm]] | 173 |
| 17 | [[05-section-5-role-of-anthropic|Section 5: Role of Anthropic Beneficial Deployment]] | 221 |
| 18 | [[06-section-6-proposer-role|Section 6: Proposer's role и qualifications]] | 169 |
| 19 | [[07-section-7-success-metrics|Section 7: Success metrics]] | 151 |
| 20 | [[08-section-8-risks-mitigations|Section 8: Risks & mitigations]] | 163 |
| 21 | [[09-section-9-timeliness|Section 9: Why this is timely]] | 162 |
| 22 | [[10-section-10-engagement-request|Section 10: Engagement request]] | 213 |
| 23 | [[11-not-and-format|Что concept document NOT (это не grant / не paper ]] | 383 |
| 24 | [[01-ai-research-engineering|AI Research & Engineering — 68 ролей]] | 126 |
| 25 | [[02-sales|Sales — 150 ролей (≈34% всего найма)]] | 164 |
| 26 | [[03-finance|Finance — 36 ролей]] | 113 |
| 27 | [[04-security|Security — 24 роли]] | 96 |
| 28 | [[05-marketing-brand|Marketing & Brand — 23 роли]] | 107 |
| 29 | [[06-engineering-design-product|Engineering & Design - Product — 22 роли]] | 109 |
| 30 | [[07-software-engineering-infrastructure|Software Engineering - Infrastructure — 22 роли]] | 108 |
| 31 | [[08-safeguards-trust-safety|Safeguards (Trust & Safety) — 21 роль]] | 111 |
| 32 | [[09-product-management-support-ops|Product Management, Support, & Operations — 17 рол]] | 96 |
| 33 | [[10-compute|Compute — 13 ролей]] | 101 |
| 34 | [[11-legal|Legal — 13 ролей]] | 100 |
| 35 | [[12-technical-program-management|Technical Program Management — 10 ролей]] | 90 |
| 36 | [[13-communications|Communications — 5 ролей]] | 81 |
| 37 | [[14-public-policy|Public Policy — 5 ролей]] | 88 |
| 38 | [[15-public-benefit|Public Benefit — 4 роли]] | 88 |
| 39 | [[16-people|People — 3 роли]] | 79 |
| 40 | [[01-coally|CoAlly — distributed shared memory для AI-агентов]] | 275 |
| 41 | [[02-vitaly-graph-cognitive-memory|Графовая когнитивная память на SQLite (Виталий, ма]] | 301 |
| 42 | [[03-happyin-knowledge-space|Happyin Knowledge Space (Анастасия) — детали]] | 274 |
| 43 | [[04-mem0-letta-graphiti|AI-ассистент с Mem0 / Letta / Graphiti integration]] | 291 |
| 44 | [[05-existing-infrastructure-stack|Existing infrastructure stack]] | 151 |
| 45 | [[06-final-tier-ranking|Финальный список потенциальных collaborators (Tier]] | 242 |
| 46 | [[07-key-observation|Ключевое наблюдение: single-developer projects of ]] | 172 |
| 47 | [[00-question-what-is-hermes|Что такое Hermes Agent (Nous Research, MIT, 95K+ s]] | 357 |
| 48 | [[01-similarity-1-composite-skills|Сходство 1: Composite Skills паттерн уже встроен]] | 212 |
| 49 | [[02-similarity-2-persistent-memory|Сходство 2: Persistent memory — Layer B функционал]] | 150 |
| 50 | [[03-similarity-3-mcp-support|Сходство 3: MCP support]] | 139 |
| ... | _ещё 47 файлов_ | |

## autofilled

_`docs/autofilled/` — 11 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[.md|Антропик]] | 137 |
| 2 | [[cowork]] | 174 |
| 3 | [[ingit]] | 174 |
| 4 | [[kksudo]] | 217 |
| 5 | [[lorenzo]] | 174 |
| 6 | [[nautilus]] | 174 |
| 7 | [[sgb]] | 174 |
| 8 | [[spbmolot]] | 213 |
| 9 | [[svend4]] | 156 |
| 10 | [[svyazi]] | 174 |
| 11 | [[Тема исследования]](docs/autofilled/research-summary.md) | 149 |

## contacts

_`docs/contacts/` — 14 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[anastasiyaw|Контакт: AnastasiyaW / knowledge-space, mclaude]] | 291 |
| 2 | [[andrey-chuyan|Контакт: andrey_chuyan / Svyazi]] | 278 |
| 3 | [[antipozitive|Контакт: Antipozitive / MemNet]] | 239 |
| 4 | [[cutcode|Контакт: Cutcode / AIF Handoff]] | 258 |
| 5 | [[dmitriila|Контакт: Dmitriila / SENTINEL]] | 255 |
| 6 | [[kksudo|Контакт: kksudo / AgentFS]] | 270 |
| 7 | [[mixaill76|Контакт: MiXaiLL76 / Auto AI Router]] | 269 |
| 8 | [[nlaik|Контакт: nlaik / LiteParse / research-docs]] | 249 |
| 9 | [[sonia-black|Контакт: Sonia_Black / knowledge-space]] | 239 |
| 10 | [[spbmolot|Контакт: spbmolot / NGT Memory]] | 290 |
| 11 | [[tagir-analyzes|Контакт: tagir_analyzes / Legal RAG]] | 246 |
| 12 | [[vitalyoborin|Контакт: VitalyOborin / Yodoca]] | 284 |
| 13 | [[vladspace|Контакт: VladSpace / Graph RAG]] | 262 |
| 14 | [[zodigancode|Контакт: zodigancode / Rufler]] | 255 |

## glossary

_`docs/glossary/` — 3 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[authors-by-name|Авторы — алфавитный список]] | 497 |
| 2 | [[components-by-name|Компоненты — алфавитный список с обратными ссылкам]] | 1114 |
| 3 | [[concepts|Ключевые понятия и паттерны]] | 665 |

## habr-unique-projects

_`docs/habr-unique-projects/` — 46 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[01-three-direct-analogues|Три прямых аналога Svyazi: K2-18, Wikontic, NGT Me]] | 419 |
| 2 | [[02-related-projects|Смежные проекты]] | 370 |
| 3 | [[1-llm-gateway|Пара 1 — LLM-gateway × Self-hosted фронт + локальн]] | 280 |
| 4 | [[2-document-rag|Пара 2 — Парсинг документов × локальный RAG]] | 332 |
| 5 | [[3-adversarial-multi-ide|Пара 3 — Adversarial agents × Multi-IDE стек]] | 329 |
| 6 | [[4-skill-catalogs-subagents|Пара 4 — Скилл-каталоги × Subagent-оркестрация]] | 300 |
| 7 | [[5-voice-local-memory|Пара 5 — Голосовой ввод × Локальная память]] | 295 |
| 8 | [[6-tmux-village-openclaw|Пара 6 — Деревня агентов через tmux × OpenClaw орк]] | 336 |
| 9 | [[7-autoresearch-distributed|Пара 7 — AutoResearch цикл × Распределённый рой]] | 277 |
| 10 | [[8-self-aware-mcp-specs|Пара 8 — Self-aware MCP × Specs-first архитектура]] | 345 |
| 11 | [[00-question-habr-examples|Вопрос: ещё примеры с Хабра по варианту D]] | 444 |
| 12 | [[01-svyazi-andrey-chuyan|Svyazi (Андрей Чуян) — детальный обзор]] | 200 |
| 13 | [[02-vshe-scientific-networking|ВШЭ научный нетворкинг — micro-collaborations]] | 165 |
| 14 | [[03-brainbox-multi-ai-hub|BrainBox — self-hosted multi-AI hub]] | 241 |
| 15 | [[04-claude-subagents-patterns|Claude subagents patterns]] | 142 |
| 16 | [[05-hw-nl2workflow|HW-NL2Workflow — Supervisor/Orchestrator/Filler с ]] | 227 |
| 17 | [[06-platform-for-professional-communities|Платформа для профессиональных сообществ]] | 205 |
| 18 | [[07-specialized-knowledge-workspace|Specialized knowledge workspace]] | 200 |
| 19 | [[08-personal-multi-agent-hub|Personal multi-agent hub]] | 193 |
| 20 | [[09-federated-platform|Federated platform]] | 192 |
| 21 | [[10-profession-specific-workflows|Profession-specific workflows]] | 282 |
| 22 | [[11-concrete-potential-collaborator|Конкретный потенциальный collaborator]] | 247 |
| 23 | [[12-concrete-next-step|Конкретный next step]] | 395 |
| 24 | [[1-one-person-one-company|Ансамбль 1 — «Один человек = одна компания»]] | 180 |
| 25 | [[2-autoresearch-legal|Ансамбль 2 — «AutoResearch для legal precedent min]] | 189 |
| 26 | [[3-discovery-research|Ансамбль 3 — «Discovery-engine для научной работы»]] | 133 |
| 27 | [[4-summary-authors|Сводный список авторов и потенциальных соавторов]] | 253 |
| 28 | [[1-neuromorphic-ssm|Пара 1 — Нейроморфные процессоры × State Space Mod]] | 324 |
| 29 | [[2-tsu-mome|Пара 2 — Термодинамические TSU × MoE/MoME-роутинг]] | 297 |
| 30 | [[3-zinc-hybrid-arch|Пара 3 — ZINC inference engine × гибрид Attention+]] | 285 |
| 31 | [[4-riscv-privacy|Пара 4 — RISC-V × privacy-by-design община]] | 294 |
| 32 | [[5-tinyml-mcp-skills|Пара 5 — TinyML/Edge AI × MCP + skills]] | 268 |
| 33 | [[6-bonus-rram-memristor|Бонус-родитель — In-memory computing на мемристора]] | 318 |
| 34 | [[7-metaphor|Метафора «двое родителей — несколько детей»]] | 329 |
| 35 | [[01-yodoca|Yodoca — главная находка итерации]] | 270 |
| 36 | [[02-memnet|MemNet — нейроархитектурный двойник «магии» Svyazi]] | 227 |
| 37 | [[03-pda-llm-as-periphery|PDA-бот — «LLM как периферия»]] | 251 |
| 38 | [[04-dochkina-sequential|Виктория Дочкина — Sequential‑протокол распределён]] | 284 |
| 39 | [[05-supplementary-infrastructure|Источник данных и инфраструктурные кусочки]] | 306 |
| 40 | [[06-svyazi-2-0-block-map|Синтез: блок-карта Svyazi 2.0 на хеббовском графе]] | 369 |
| 41 | [[1-workflow-llm-mcp|Пара 1 — Workflow-автоматизация × LLM-агенты с MCP]] | 260 |
| 42 | [[2-pkm-mcp-skills|Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/S]] | 302 |
| 43 | [[3-crdt-self-hosted|Пара 3 — CRDT-синхронизация × Self-hosted persiste]] | 253 |
| 44 | [[4-speech-to-text-llm|Пара 4 — Speech-to-text локально × LLM с памятью]] | 296 |
| 45 | [[5-browser-agents-headless|Пара 5 — Browser agents × headless web extraction]] | 465 |
| 46 | [[6-metaphor|Метафора в твоей терминологии]] | 273 |

## lorenzo-agent

_`docs/lorenzo-agent/` — 55 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-intro|Введение: Lorenzo — Catalyst Agent at DHLab]] | 78 |
| 2 | [[01-kto-ty|Кто ты]] | 156 |
| 3 | [[02-tvoyo-proishozhdenie|Твоё происхождение]] | 177 |
| 4 | [[03-tvoya-missiya|Твоя миссия]] | 160 |
| 5 | [[04-komu-ty-sluzhish|Кому ты служишь (слоистая модель)]] | 150 |
| 6 | [[05-tvoya-lichnost|Твоя личность]] | 253 |
| 7 | [[06-yazyki-kultura|Языки и культурные nuances (RU / DE / EN)]] | 206 |
| 8 | [[07-chto-mozhesh|Что ты МОЖЕШЬ делать]] | 163 |
| 9 | [[08-bez-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]] | 156 |
| 10 | [[09-voobshche-nelzya|Что ты НЕ МОЖЕШЬ делать вообще]] | 150 |
| 11 | [[10-collaborators-landscape|Существующий landscape collaborators (working know]] | 305 |
| 12 | [[11-dhlab-documents|Существующие документы DHLab (твой context)]] | 192 |
| 13 | [[12-workflow|Твой workflow]] | 218 |
| 14 | [[13-outreach-communication|Твоя коммуникация в outreach]] | 226 |
| 15 | [[14-other-ai-relationships|Твоя relationship с другими AI]] | 186 |
| 16 | [[15-anti-patterns|Твои anti-patterns]] | 175 |
| 17 | [[16-vsegda-delaesh|Что ты ВСЕГДА делаешь]] | 131 |
| 18 | [[17-honestly-ne-znaesh|Когда ты Honestly не знаешь]] | 133 |
| 19 | [[18-escalate-to-max|Когда сомневаешься — escalate к Max]] | 135 |
| 20 | [[19-persistent-character|Твоя identity как persistent character]] | 168 |
| 21 | [[20-experiment|Final note: Ты — experiment]] | 158 |
| 22 | [[00-question-lorenzo-codename|Du hast gesagt: Думаю про опцию д поискать в том ч]] | 238 |
| 23 | [[01-search-results-not-found|Результаты последнего поиска — что нашлось и что н]] | 295 |
| 24 | [[02-naming-rationale-lorenzo-medici|Что взять: agent controller architecture]] | 1183 |
| 25 | [[03-dhlab-umbrella|LAYER 7: Coordination engine]] | 1402 |
| 26 | [[00-overview-grandchild-combination|Что такое «внуковая» комбинация — operationalized ]] | 603 |
| 27 | [[01-pluses-1-7|Плюсы 1–7: feasibility, flywheel, independent valu]] | 470 |
| 28 | [[02-minuses-1-10|Минусы 1–10: integration сложность, lifecycle risk]] | 738 |
| 29 | [[03-honest-opinion|Моё честное мнение: что реально и что НЕ реально]] | 180 |
| 30 | [[04-recommendations|Рекомендации: принять архитектуру как direction, н]] | 440 |
| 31 | [[05-anchor-node-habr-scout|Anchor-узел: Habr Scout как первый шаг]] | 584 |
| 32 | [[06-conclusion-deserves-attention|Вывод: документ deserves serious attention]] | 518 |
| 33 | [[00-overview|Поэтапная структура активностей Lorenzo — обзор]] | 169 |
| 34 | [[01-level-0-manual|Уровень 0 — Ручной режим (текущий)]] | 179 |
| 35 | [[02-level-1-minimal-zero|Уровень 1 — Минимальный (Lorenzo Zero)]] | 241 |
| 36 | [[03-level-2-basic-lite|Уровень 2 — Базовый (Lorenzo Lite)]] | 207 |
| 37 | [[04-level-3-medium-active|Уровень 3 — Средний (Lorenzo Active)]] | 222 |
| 38 | [[05-level-4-extended-mature|Уровень 4 — Расширенный (Lorenzo Mature)]] | 183 |
| 39 | [[06-level-5-full-network|Уровень 5 — Полный (Lorenzo Network)]] | 146 |
| 40 | [[07-progression-logic|Логика прогрессии: conservative escalation]] | 185 |
| 41 | [[08-current-session-poc|Что мы можем делать прямо сейчас (Уровень 0 + пара]] | 839 |
| 42 | [[00-question-scenario|Du hast gesagt: А под какой сценарий больше всего ]] | 177 |
| 43 | [[01-response|Claude hat geantwortet: Очень интересный вопрос.]] | 2453 |
| 44 | [[00-context-fundamental-questions|Direction E: Refine Lorenzo — фундаментальные вопр]] | 205 |
| 45 | [[01-q1-what-lorenzo-is|Question 1: Что Lorenzo фундаментально такое? (Fra]] | 348 |
| 46 | [[02-q2-whom-lorenzo-serves|Question 2: Кому Lorenzo служит? (4 варианта приор]] | 238 |
| 47 | [[03-q3-what-lorenzo-does|Question 3: Что Lorenzo фактически делает?]] | 228 |
| 48 | [[04-q4-character|Question 4: Каков Lorenzo's character?]] | 292 |
| 49 | [[05-q5-authority-limits|Question 5: Каковы limits Lorenzo's authority?]] | 228 |
| 50 | [[06-q6-accountability|Question 6: Как Lorenzo accountable?]] | 214 |
| ... | _ещё 5 файлов_ | |

## meta-scripting

_`docs/meta-scripting/` — 5 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[01-concept|Метаскриптинг — Часть 1: Концепция]] | 439 |
| 2 | [[02-architecture|Метаскриптинг — Часть 2: Архитектура]] | 614 |
| 3 | [[03-catalog|Метаскриптинг — Часть 3: Автокаталог скриптов]] | 412 |
| 4 | [[04-enrichment|Метаскриптинг — Часть 4: Обогащение скриптов]] | 582 |
| 5 | [[05-synthesis|Метаскриптинг — Часть 5: Синтез новых скриптов]] | 503 |

## nautilus

_`docs/nautilus/` — 227 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-question-agent-changes-reality|Du hast gesagt: Такой агент конечно меняет уже соб]] | 216 |
| 2 | [[01-response-en|Claude hat geantwortet: Хорошо.]] | 9468 |
| 3 | [[00-question-habr-link|Du hast gesagt: https://habr.]] | 72 |
| 4 | [[01-claude-response|Claude hat geantwortet: Прочитал внимательно.]] | 2467 |
| 5 | [[00-question-habr-2|Du hast gesagt: https://www.]] | 157 |
| 6 | [[01-response|Claude hat geantwortet: Прочитаю статью, чтобы пон]] | 2792 |
| 7 | [[00-question-practical|Du hast gesagt: Да это интересная ссылка спасибо в]] | 227 |
| 8 | [[01-response|Claude hat geantwortet: Отличное наблюдение.]] | 1837 |
| 9 | [[00-question-voiceless|Du hast gesagt: Самый интересный вопрос — могут ли]] | 514 |
| 10 | [[01-response|Claude hat geantwortet: Это сильное продолжение мы]] | 2533 |
| 11 | [[01-why-binary-incomplete|1. Why the Binary View Is Incomplete]] | 640 |
| 12 | [[02-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]] | 780 |
| 13 | [[03-what-makes-csa|3. What Makes a Composite Skills Agent]] | 889 |
| 14 | [[04-sub-agent-registry|4. The Sub-Agent Registry]] | 750 |
| 15 | [[05-configuration-ensembles|5. Configuration: How Principals Build Their Ensem]] | 681 |
| 16 | [[06-coordination-disagreement|6. Coordination and Disagreement Resolution]] | 742 |
| 17 | [[07-economics-combinatorial|7. Economics of Combinatorial Replication]] | 722 |
| 18 | [[08-seven-domains|8. Seven Domains of Application]] | 948 |
| 19 | [[09-okwf-integration|9. Integration with OKWF Infrastructure]] | 693 |
| 20 | [[10-risks|10. Risks Specific to Composite Architectures]] | 732 |
| 21 | [[11-open-questions|11. Open Questions]] | 467 |
| 22 | [[12-call-for-collaboration|12. Call for Collaboration]] | 350 |
| 23 | [[13-closing|13. Closing]] | 664 |
| 24 | [[00-question-multiple-mentors|Du hast gesagt: Важный момент про способности про ]] | 540 |
| 25 | [[01-yogi-metaphor|Claude hat geantwortet: Это очень тонкое и важное ]] | 517 |
| 26 | [[02-what-was-missing-in-paper-6|Это не Тип 1 — потому что профиль не общий для все]] | 1019 |
| 27 | [[03-the-spectrum|Какой под-агент (или какие) должны её обработать]] | 902 |
| 28 | [[00-abstract|Abstract — The Double-Triangle Architecture]] | 407 |
| 29 | [[01-why-single-triangle-incomplete|1. Why Single-Triangle Models Are Incomplete]] | 466 |
| 30 | [[02-double-triangle-architecture|2. The Double-Triangle Architecture]] | 687 |
| 31 | [[03-three-inter-layer-protocols|3. Three Inter-Layer Protocols]] | 820 |
| 32 | [[04-nautilus-portal-substrate|4. Nautilus Portal as Reference Substrate]] | 631 |
| 33 | [[05-pattern-library-bridge|5. Pattern Library as Bridge Between Triangles]] | 642 |
| 34 | [[06-four-deployment-domains|6. Four Deployment Domains]] | 634 |
| 35 | [[07-open-questions|7. Open Questions]] | 726 |
| 36 | [[08-call-to-action|8. Call to Action]] | 704 |
| 37 | [[09-acknowledgments|Acknowledgments]] | 208 |
| 38 | [[10-references|References]] | 278 |
| 39 | [[11-glossary|Appendix A: Glossary]] | 1582 |
| 40 | [[00-intro|The Missing Middle Layer Between Chat and Code]] | 191 |
| 41 | [[01-missing-middle-layer|Why This Document Exists]] | 305 |
| 42 | [[02-why-document-exists|Why This Document Exists]] | 305 |
| 43 | [[03-two-layer-stack|The Two-Layer Stack As It Exists]] | 352 |
| 44 | [[04-whats-missing-layer-b|What's Missing — Layer B]] | 424 |
| 45 | [[05-why-not-built|Why This Hasn't Been Built]] | 344 |
| 46 | [[06-existing-approximations|Existing Approximations]] | 466 |
| 47 | [[07-specific-case|The Specific Case in Front of Us]] | 614 |
| 48 | [[08-recursive-insight|The Recursive Insight]] | 326 |
| 49 | [[09-what-industry-will-build|What Industry Will Likely Build]] | 273 |
| 50 | [[10-what-not-solved|What This Document Doesn't Solve]] | 204 |
| ... | _ещё 177 файлов_ | |

## obsidian

_`docs/obsidian/` — 473 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[00-intro-part2|Продолжение исследования для Svyazi 2.0]] | 36 |
| 2 | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/obsidian/01-svyazi/01-executive-summary.md) | 739 |
| 3 | [[02-methodology|Методика и рамка отбора проектов]] | 526 |
| 4 | [[03-component-catalog]] | 1394 |
| 5 | [[04-ensembles-overview]] | 1299 |
| 6 | [[06-security-privacy]] | 834 |
| 7 | [[07-mvp-planning]] | 1074 |
| 8 | [[08-conclusions]] | 390 |
| 9 | [[09-architectural-gaps]] | 769 |
| 10 | [[10-second-order-ensembles]] | 920 |
| 11 | [[11-integration-contracts]] | 748 |
| 12 | [[12-roadmap]] | 732 |
| 13 | [[13-contacts]] | 1020 |
| 14 | [[14-limitations]] | 648 |
| 15 | [[00-intro|Введение]] | 8993 |
| 16 | [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]] | 19229 |
| 17 | [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]] | 3332 |
| 18 | [[03-portal-protocol-md|PORTAL-PROTOCOL.md]] | 329 |
| 19 | [[04-abstract|Abstract]] | 321 |
| 20 | [[05-0-status-of-this-document|0. Status of This Document]] | 311 |
| 21 | [[06-1-introduction|1. Introduction]] | 395 |
| 22 | [[07-2-terminology|2. Terminology]] | 316 |
| 23 | [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] | 416 |
| 24 | [[09-4-passport-passport-md|4. Passport (`passport.md`)]] | 311 |
| 25 | [[102-доступ-к-данным|Доступ к данным]] | 227 |
| 26 | [[103-appendix-b-change-log|Appendix B: Change Log]] | 325 |
| 27 | [[104-appendix-c-references|Appendix C: References]] | 1187 |
| 28 | [[105-review-methodology-md|REVIEW_METHODOLOGY.md]] | 282 |
| 29 | [[106-tl-dr|TL;DR]] | 227 |
| 30 | [[107-1-контекст-и-мотивация|1. Контекст и мотивация]] | 473 |
| 31 | [[108-2-формальный-workflow|2. Формальный workflow]] | 480 |
| 32 | [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]] | 696 |
| 33 | [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или осмысле]] | 358 |
| 34 | [[111-4-условия-применимости|4. Условия применимости]] | 289 |
| 35 | [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]] | 406 |
| 36 | [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assisted wor]] | 170 |
| 37 | [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]] | 328 |
| 38 | [[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]] | 464 |
| 39 | [[116-9-checklist-применения-методологии|9. Checklist применения методологии]] | 413 |
| 40 | [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим документа]] | 334 |
| 41 | [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]] | 191 |
| 42 | [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешения]] | 391 |
| 43 | [[12-content-overview|Content Overview]] | 194 |
| 44 | [[120-главные-технические-риски|Главные технические риски]] | 95 |
| 45 | [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]] | 225 |
| 46 | [[122-глоссарий|Глоссарий]] | 1527 |
| 47 | [[123-portal-mcp-py|portal-mcp.py]] | 2512 |
| 48 | [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]] | 255 |
| 49 | [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]] | 275 |
| 50 | [[126-установка|Установка]] | 156 |
| ... | _ещё 423 файлов_ | |

## processing-guide

_`docs/processing-guide/` — 11 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[01-overview|Обработка больших массивов информации — Часть 1: О]] | 462 |
| 2 | [[02-extraction|Обработка больших массивов — Часть 2: Извлечение]] | 622 |
| 3 | [[03-chunking|Обработка больших массивов — Часть 3: Разбивка и ч]] | 664 |
| 4 | [[04-structuring|Обработка больших массивов — Часть 4: Структуриров]] | 716 |
| 5 | [[05-analysis|Обработка больших массивов — Часть 5: Анализ и NLP]] | 882 |
| 6 | [[06-search|Обработка больших массивов — Часть 6: Поиск]] | 965 |
| 7 | [[07-llm|Обработка больших массивов — Часть 7: LLM-обогащен]] | 855 |
| 8 | [[08-export|Обработка больших массивов — Часть 8: Экспорт и ин]] | 720 |
| 9 | [[09-automation|Обработка больших массивов — Часть 9: Автоматизаци]] | 886 |
| 10 | [[10-future|Обработка больших массивов — Часть 10: Инновационн]] | 1756 |
| 11 | [[PROCESSING_GUIDE|Обработка больших массивов документов — Полное рук]] | 8049 |

## svyazi-2-0

_`docs/svyazi-2-0/` — 50 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[card-envelope|Card Envelope]] | 200 |
| 2 | [[evidence-envelope|Evidence Envelope]] | 238 |
| 3 | [[gaps|Архитектурные зазоры]] | 597 |
| 4 | [[integration-spec|Интеграционная спецификация (минимум для MVP)]] | 285 |
| 5 | [[memory-write-policy|Memory Write Policy]] | 186 |
| 6 | [[review-record|Review Record]] | 121 |
| 7 | [[skill-tool-policy|Skill and Tool Policy]] | 183 |
| 8 | [[agent-memory-mcp|agent-memory-mcp + Memory OS]] | 166 |
| 9 | [[agentfs]] | 125 |
| 10 | [[ai-factory|AI Factory + AIF Handoff]] | 130 |
| 11 | [[autoresearch-sequential|AutoResearch + Sequential]] | 140 |
| 12 | [[graph-rag|Graph RAG]] | 125 |
| 13 | [[hybrid-rag|Hybrid RAG knowledge base]] | 118 |
| 14 | [[knowledge-space]] | 123 |
| 15 | [[legal-rag|Legal RAG]] | 123 |
| 16 | [[mclaude]] | 114 |
| 17 | [[memnet|MemNet / memory-is-all-you-need]] | 117 |
| 18 | [[ngt-memory|NGT Memory]] | 138 |
| 19 | [[research-docs-liteparse|research-docs + LiteParse]] | 137 |
| 20 | [[rufler]] | 114 |
| 21 | [[security-routing-plane|Security + routing plane]] | 210 |
| 22 | [[self-aware-mcp|Self‑Aware MCP + Skills + CodeWiki]] | 148 |
| 23 | [[svyazi]] | 134 |
| 24 | [[voice-stack|Voice / local-first stack]] | 152 |
| 25 | [[yjs-automerge|Yjs + Automerge]] | 125 |
| 26 | [[yodoca]] | 127 |
| 27 | [[A-collaboration-os|Ансамбль A — Collaboration OS]] | 248 |
| 28 | [[B-forensic-rag|Ансамбль B — Forensic RAG для доказуемого matching]] | 252 |
| 29 | [[C-multi-agent-factory|Ансамбль C — Spec‑driven multi‑agent factory]] | 249 |
| 30 | [[D-voice-first-mesh|Ансамбль D — Voice‑first local knowledge mesh]] | 265 |
| 31 | [[E-execution-plane|Ансамбль E — Safe and cheap execution plane]] | 253 |
| 32 | [[F-evidence-backed-intake|Ансамбль F — Evidence‑Backed Community Intake]] | 262 |
| 33 | [[G-federated-local-graph|Ансамбль G — Federated Local‑First Community Graph]] | 284 |
| 34 | [[H-research-to-product-flywheel|Ансамбль H — Research‑to‑Product Flywheel]] | 234 |
| 35 | [[conclusions|Итоговые выводы и порядок сборки]] | 318 |
| 36 | [[do-not-glue|Что пока лучше не склеивать]] | 343 |
| 37 | [[license-tree|Лицензионные развилки]] | 324 |
| 38 | [[first-contacts|Первые контакты]] | 259 |
| 39 | [[message-template|Шаблон первого сообщения]] | 248 |
| 40 | [[narrow-questions|Узкие вопросы для каждого автора]] | 306 |
| 41 | [[continuation-intro|Что добавляет продолжение исследования]] | 242 |
| 42 | [[executive-summary|Executive summary]] | 376 |
| 43 | [[methodology|Методика и рамка отбора]] | 268 |
| 44 | [[projects-map|Карта найденных проектов и паттернов]] | 1301 |
| 45 | [[mvp-plan|План MVP-прототипа]] | 312 |
| 46 | [[risks|Ключевые риски и как их закрывать]] | 287 |
| 47 | [[roadmap|Дорожная карта прототипа]] | 609 |
| 48 | [[budget-routing|Практичный бюджетный роутинг моделей]] | 329 |
| 49 | [[default-policy|Что стоит зафиксировать как default policy]] | 365 |
| 50 | [[privacy|Приватность: local-first by default]] | 124 |

## technology-combinations

_`docs/technology-combinations/` — 47 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [[01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern|Комбинация 1: Правильная агентская архитектура × S]] | 246 |
| 2 | [[02-multiagentnyy-khaos-reshenie-auto-ai-router|Комбинация 2: Мультиагентный хаос-решение × Auto A]] | 187 |
| 3 | [[03-crdt-local-first-svyazi-cardindex|Комбинация 3: CRDT local-first × Svyazi CardIndex]] | 199 |
| 4 | [[04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura|Комбинация 4: Парсинг с LLM × Graph-RAG × Правильн]] | 218 |
| 5 | [[05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy|Комбинация 5: SourceCraft CLI × Claude Code × Sequ]] | 212 |
| 6 | [[06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-|Комбинация 6: OpenClaude (утёкший Claude Code) × Z]] | 218 |
| 7 | [[07-crawl4ai-docling-yodoca-consolidator|Комбинация 7: Crawl4AI × Docling × Yodoca consolid]] | 199 |
| 8 | [[08-conductor-adversarial-review-auto-ai-router|Комбинация 8: Conductor × adversarial-review × Aut]] | 686 |
| 9 | [[09-agent-orchestration-stack|Комбинация 9: Agent Orchestration Stack]] | 196 |
| 10 | [[10-legal-document-intelligence-pipeline|Комбинация 10: Legal Document Intelligence Pipelin]] | 200 |
| 11 | [[11-hybrid-crdt-sql-database|Комбинация 11: Hybrid CRDT-SQL Database]] | 189 |
| 12 | [[12-multi-agent-observability-stack|Комбинация 12: Multi-Agent Observability Stack]] | 165 |
| 13 | [[13-legal-document-transpiler|Комбинация 13: Legal Document Transpiler]] | 180 |
| 14 | [[14-local-first-agent-development-environment|Комбинация 14: local-first Agent Development Envir]] | 577 |
| 15 | [[15-self-consolidating-legal-corpus|Комбинация 15: Self-Consolidating Legal Corpus]] | 226 |
| 16 | [[16-adversarial-multi-agent-code-review|Комбинация 16: Adversarial Multi-Agent Code Review]] | 254 |
| 17 | [[17-distributed-agent-memory-with-graph|Комбинация 17: Distributed Agent Memory with Graph]] | 209 |
| 18 | [[18-llm-powered-legal-corpus-builder|Комбинация 18: LLM-Powered Legal Corpus Builder]] | 228 |
| 19 | [[19-multi-agent-observability-platform|Комбинация 19: Multi-Agent Observability Platform]] | 678 |
| 20 | [[20-hybrid-olap-oltp-with-real-time-sync|Комбинация 20: Hybrid OLAP-OLTP with Real-Time Syn]] | 256 |
| 21 | [[21-legal-corpus-analytics-at-scale|Комбинация 21: Legal Corpus Analytics at Scale]] | 249 |
| 22 | [[22-russian-international-oss-stack|Комбинация 22: Russian-International OSS Stack]] | 213 |
| 23 | [[23-security-first-code-review-pipeline|Комбинация 23: Security-First Code Review Pipeline]] | 183 |
| 24 | [[24-mega-integration-full-stack|Комбинация 24: MEGA-INTEGRATION: Full Stack]] | 594 |
| 25 | [[25-legal-dsl-code-transpiler|Комбинация 25: Legal DSL → Code Transpiler]] | 252 |
| 26 | [[26-ast-based-code-analysis-for-legal-automation|Комбинация 26: AST-Based Code Analysis for Legal A]] | 206 |
| 27 | [[27-hybrid-rag-with-ast-chunked-code|Комбинация 27: Hybrid RAG with AST-Chunked Code]] | 220 |
| 28 | [[28-pydantic-enforced-legal-workflows|Комбинация 28: Pydantic-Enforced Legal Workflows]] | 225 |
| 29 | [[29-meta-programmatic-legal-template-generator|Комбинация 29: Meta-Programmatic Legal Template Ge]] | 198 |
| 30 | [[30-mega-stack-3-0-with-dsl-ast|Комбинация 30: MEGA-STACK 3.0 with DSL & AST]] | 489 |
| 31 | [[31-event-sourced-legal-document-history|Комбинация 31: Event-Sourced Legal Document Histor]] | 245 |
| 32 | [[32-consensus-based-multi-agent-coordination|Комбинация 32: Consensus-Based Multi-Agent Coordin]] | 260 |
| 33 | [[33-event-sourcing-cqrs-clickhouse-analytics|Комбинация 33: Event Sourcing + CQRS + ClickHouse ]] | 221 |
| 34 | [[34-distributed-event-store-with-paxos|Комбинация 34: Distributed Event Store with Paxos]] | 193 |
| 35 | [[35-mega-stack-4-0-with-event-sourcing-consensus|Комбинация 35: MEGA-STACK 4.0 with Event Sourcing ]] | 483 |
| 36 | [[01-legal-ai-stack|Mega‑Stack 1.0 — Полный Legal‑AI Stack]] | 227 |
| 37 | [[02-ultimate-legal-ai|Mega‑Stack 2.0 — Ultimate Legal‑AI System]] | 318 |
| 38 | [[03-dsl-ast|Mega‑Stack 3.0 — with DSL & AST]] | 242 |
| 39 | [[04-event-sourcing-consensus|Mega‑Stack 4.0 — with Event Sourcing & Consensus]] | 329 |
| 40 | [[continuation-10-domains|Research Report: Continuation — 10 New Domains Bey]] | 316 |
| 41 | [[sozialrecht-35-combinations|Research Report: Sozialrecht (35 комбинаций)]] | 222 |
| 42 | [[01-08-summary|Сводная таблица 1–8]] | 401 |
| 43 | [[09-14-extended|Сводная таблица 9–14 (Extended)]] | 195 |
| 44 | [[15-19-extended|Сводная таблица 15–19 (Extended)]] | 162 |
| 45 | [[20-24-final|Сводная таблица 20–24 (Final 1–24)]] | 212 |
| 46 | [[25-30-extended|Сводная таблица 25–30 (Complete 1–30)]] | 228 |
| 47 | [[31-35-final|Сводная таблица 31–35 (Complete 1–35)]] | 249 |

## templates

_`docs/templates/` — 23 файлов_

| # | Документ | Слов |
|---|----------|------|
| 1 | [Спецификация агента: [Название]](docs/templates/agent-spec.md) | 356 |
| 2 | [Контакт: [Имя / Проект]](docs/templates/contact-outreach.md) | 119 |
| 3 | [Противоречие: [Название]](docs/templates/contradiction-record.md) | 174 |
| 4 | [ADR: [Название решения]](docs/templates/decision-record.md) | 84 |
| 5 | [Ансамбль: [Название]](docs/templates/ensemble.md) | 112 |
| 6 | [Эксперимент: [Название]](docs/templates/experiment-log.md) | 185 |
| 7 | [FAQ: [Вопрос]](docs/templates/faq-entry.md) | 132 |
| 8 | [[Термин]](docs/templates/glossary-entry.md) | 117 |
| 9 | [KPI Snapshot: [дата]](docs/templates/kpi-snapshot.md) | 220 |
| 10 | [Юридический кейс: [Aktenzeichen]](docs/templates/legal-case.md) | 275 |
| 11 | [Встреча: [Тема]](docs/templates/meeting-notes.md) | 151 |
| 12 | [Mega-stack: [Название]](docs/templates/mega-stack.md) | 339 |
| 13 | [[Название компонента]](docs/templates/project-component.md) | 102 |
| 14 | [[Название протокола]](docs/templates/protocol-spec.md) | 361 |
| 15 | [MVP: [Название]](docs/templates/prototype-mvp.md) | 384 |
| 16 | [[Тема исследования]](docs/templates/research-note.md) | 66 |
| 17 | [Ретроспектива: [период]](docs/templates/retrospective.md) | 160 |
| 18 | [RFC NNNN: [Название]](docs/templates/rfc.md) | 241 |
| 19 | [Риск: [Название]](docs/templates/risk-entry.md) | 221 |
| 20 | [Tech Pair: [A] × [B]](docs/templates/tech-pair.md) | 273 |
| 21 | [Tech Radar: [Название]](docs/templates/tech-radar-entry.md) | 224 |
| 22 | [[имя нового шаблона]](docs/templates/template-of-templates.md) | 319 |
| 23 | [Еженедельный дайджест: [период]](docs/templates/weekly-digest.md) | 193 |

<!-- see-also -->

---

## Использование

```bash
python scripts/improve_sitemap.py
```

```bash
# Только навигационная карта раздела
python scripts/improve_sitemap.py --section 05-habr-projects
```

```bash
# Формат с включением файлов-заготовок
python scripts/improve_sitemap.py --include-stubs
```

```bash
# Обновить и проверить сразу
python scripts/improve_sitemap.py && python scripts/improve_broken_links.py
```

```bash
# Подробный вывод путей
python scripts/improve_sitemap.py --verbose
```

## Смотрите также
- [[READABILITY]]
- [[READING_TIME]]
- [[LANGUAGE_STATS]]
- [[SOURCE_MAP]]

