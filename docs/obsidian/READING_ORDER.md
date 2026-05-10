---
title: "Рекомендуемый порядок чтения"
tags:
  - general
date: 2026-05-10
---

# Рекомендуемый порядок чтения

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> От базовых концепций к сложным. Начните с зелёных (🟢), затем жёлтые (🟡), красные (🔴).
**Проекты:** Svyazi, Yodoca, MemNet, Wikontic

---

<!-- toc -->
## Содержание

- [Маршруты по целям](#маршруты-по-целям)
  - [🚀 Быстрый старт (30 минут)](#быстрый-старт-30-минут)
  - [🏗️ Архитектура (2 часа)](#архитектура-2-часа)
  - [🔬 Полное исследование (1 день)](#полное-исследование-1-день)

---

<!-- tags: memory, security, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->




От базовых концепций к сложным. Начните с зелёных (🟢), затем жёлтые (🟡), красные (🔴).

| # | Уровень | Документ | Слов | Предварительно прочитать |
|---|---------|----------|------|--------------------------|
| 1 | 🟢 Начало | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 726 | — |
| 2 | 🟡 Средний | [[04-ensembles-overview]] | 1288 | — |
| 3 | 🟢 Начало | [[00-intro-part2|Продолжение исследования для Svyazi 2.0]] | 6 | — |
| 4 | 🟢 Начало | [[02-methodology|Методика и рамка отбора проектов]] | 480 | — |
| 5 | 🟡 Средний | [[03-component-catalog]] | 1405 | — |
| 6 | 🟢 Начало | [[11-integration-contracts]] | 753 | `09-architectural-gaps.md` |
| 7 | 🟢 Начало | [[09-architectural-gaps]] | 774 | `01-executive-summary.md`, `03-component-catalog.md` |
| 8 | 🟢 Начало | [[10-second-order-ensembles]] | 924 | `04-ensembles-overview.md` |
| 9 | 🟢 Начало | [[06-security-privacy]] | 823 | — |
| 10 | 🟡 Средний | [[07-mvp-planning]] | 1083 | — |
| 11 | 🟢 Начало | [[12-roadmap]] | 722 | `07-mvp-planning.md`, `11-integration-contracts.md` |
| 12 | 🟡 Средний | [[13-contacts]] | 1010 | — |
| 13 | 🟢 Начало | [[14-limitations]] | 638 | — |
| 14 | 🟢 Начало | [[08-conclusions]] | 380 | — |
| 15 | 🟢 Начало | [[01-synthesis|Синтез: как проекты собираются вместе]] | 263 | — |
| 16 | 🟢 Начало | [[02-collaboration-partners|Авторы и контакты]] | 279 | — |
| 17 | 🟢 Начало | [[wikontic|Wikontic: семантический граф]] | 385 | — |
| 18 | 🟢 Начало | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 382 | — |
| 19 | 🟢 Начало | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 379 | — |
| 20 | 🟡 Средний | [[memnet|MemNet: исследовательская память]] | 7264 | — |
| 21 | 🟢 Начало | [[01-executive-summary|Executive summary]] | 593 | — |
| 22 | 🟡 Средний | [[00-intro|Введение]] | 11407 | — |
| 23 | 🟢 Начало | [[02-методика-и-рамка-отбора|Методика и рамка отбора]] | 459 | — |
| 24 | 🟡 Средний | [[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]] | 1478 | — |
| 25 | 🟡 Средний | [[04-приоритетные-ансамбли|Приоритетные ансамбли]] | 1358 | — |
| 26 | 🟡 Средний | [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]] | 1150 | — |
| 27 | 🟢 Начало | [[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]] | 903 | — |
| 28 | 🟢 Начало | [[07-выводы|Выводы]] | 488 | — |
| 29 | 🟢 Начало | [[08-что-это-продолжение-добавляет|Что это продолжение добавляет]] | 464 | — |
| 30 | 🟢 Начало | [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых ин]] | 839 | — |
| 31 | 🟡 Средний | [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]] | 1002 | — |
| 32 | 🟢 Начало | [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафикс]] | 864 | — |
| 33 | 🟢 Начало | [[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]] | 787 | — |
| 34 | 🟢 Начало | [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авто]] | 892 | — |
| 35 | 🟡 Средний | [[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|Ограничения, лицензии и что пока лучше не скл]] | 3274 | — |
| 36 | 🟢 Начало | [[01-agent-routing|Агентные системы и роутинг]] | 374 | — |
| 37 | 🟢 Начало | [[02-knowledge-graphs|Графы знаний и Legal AI]] | 838 | — |
| 38 | 🟢 Начало | [[03-local-first|Local-first и P2P стек]] | 560 | — |
| 39 | 🟢 Начало | [[04-sozialrecht-domain|Домен: немецкое социальное право]] | 176 | — |
| 40 | 🟢 Начало | [[05-benchmarks|Бенчмарки и производительность]] | 1013 | — |
| 41 | 🟢 Начало | [[153-executive-summary|Executive Summary]] | 615 | — |
| 42 | 🟢 Начало | [[38-content-overview|Content Overview]] | 149 | — |
| 43 | 🔴 Продвинутый | [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]] | 19237 | — |
| 44 | 🟢 Начало | [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]] | 290 | — |
| 45 | 🟢 Начало | [[65-readme-md|README.md]] | 243 | — |
| 46 | 🟢 Начало | [[48-content-overview|Content Overview]] | 178 | — |
| 47 | 🟢 Начало | [[58-content-overview|Content Overview]] | 142 | — |
| 48 | 🟢 Начало | [[12-content-overview|Content Overview]] | 211 | — |
| 49 | 🟢 Начало | [[31-content-overview|Content Overview]] | 215 | — |
| 50 | 🔴 Продвинутый | [[00-intro|Введение]] | 9000 | — |
| 51 | 🟢 Начало | [[76-1-introduction|1. Introduction]] | 501 | — |
| 52 | 🟢 Начало | [[105-review-methodology-md|REVIEW_METHODOLOGY.md]] | 300 | — |
| 53 | 🟢 Начало | [[06-1-introduction|1. Introduction]] | 403 | — |
| 54 | 🔴 Продвинутый | [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]] | 3326 | — |
| 55 | 🟢 Начало | [[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Age]] | 1125 | — |
| 56 | 🟢 Начало | [[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]] | 779 | — |
| 57 | 🟡 Средний | [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB ]] | 2007 | — |
| 58 | 🟢 Начало | [[312-4-the-symbiotic-architecture|4. The Symbiotic Architecture]] | 688 | — |
| 59 | 🟢 Начало | [[03-portal-protocol-md|PORTAL-PROTOCOL.md]] | 347 | — |
| 60 | 🟢 Начало | [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]] | 310 | — |
| 61 | 🟢 Начало | [[263-10-risks-specific-to-composite-architectures|10. Risks Specific to Composite Architectures]] | 1034 | — |
| 62 | 🟢 Начало | [[04-abstract|Abstract]] | 339 | — |
| 63 | 🟢 Начало | [[05-0-status-of-this-document|0. Status of This Document]] | 325 | — |
| 64 | 🟢 Начало | [[23-11-security-considerations|11. Security Considerations]] | 392 | — |
| 65 | 🟢 Начало | [[90-15-security-considerations|15. Security Considerations]] | 555 | — |
| 66 | 🟢 Начало | [[07-2-terminology|2. Terminology]] | 324 | — |
| 67 | 🟢 Начало | [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] | 427 | — |
| 68 | 🟢 Начало | [[09-4-passport-passport-md|4. Passport (`passport.md`)]] | 324 | — |
| 69 | 🟢 Начало | [[13-angle-perspective|Angle / Perspective]] | 238 | — |
| 70 | 🟢 Начало | [[16-history|History]] | 178 | — |
| 71 | 🟢 Начало | [[17-5-compatibility-levels|5. Compatibility Levels]] | 338 | — |
| 72 | 🟢 Начало | [[18-6-adapter-interface|6. Adapter Interface]] | 604 | — |
| 73 | 🟢 Начало | [[19-7-portalentry-structure|7. PortalEntry Structure]] | 273 | — |
| 74 | 🟢 Начало | [[20-8-consensus-algorithm|8. Consensus Algorithm]] | 333 | — |
| 75 | 🟢 Начало | [[21-9-query-flow|9. Query Flow]] | 335 | — |
| 76 | 🟢 Начало | [[22-10-queryresult-structure|10. QueryResult Structure]] | 356 | — |
| 77 | 🟢 Начало | [[24-12-versioning-policy|12. Versioning Policy]] | 358 | — |
| 78 | 🟢 Начало | [[25-13-reference-implementation|13. Reference Implementation]] | 320 | — |
| 79 | 🟢 Начало | [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]] | 316 | — |
| 80 | 🟢 Начало | [[27-15-glossary-of-examples|15. Glossary of Examples]] | 126 | — |
| 81 | 🟢 Начало | [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] | 212 | — |
| 82 | 🟢 Начало | [[34-appendix-b-change-log|Appendix B: Change Log]] | 855 | — |
| 83 | 🟢 Начало | [[35-passports-info1-md|passports/info1.md]] | 260 | — |
| 84 | 🟢 Начало | [[36-essence|Essence]] | 157 | — |
| 85 | 🟢 Начало | [[37-native-format|Native Format]] | 333 | — |
| 86 | 🟢 Начало | [[39-angle-perspective|Angle / Perspective]] | 257 | — |
| 87 | 🟢 Начало | [[40-bridges|Bridges]] | 191 | — |
| 88 | 🟢 Начало | [[41-compatibility-level|Compatibility Level]] | 273 | — |
| 89 | 🟢 Начало | [[42-author-contact|Author & Contact]] | 321 | — |
| 90 | 🟢 Начало | [[43-history|History]] | 148 | — |
| 91 | 🟢 Начало | [[44-for-the-curious-philosophy|For the Curious: Philosophy]] | 290 | — |
| 92 | 🟢 Начало | [[45-passports-pro2-md|passports/pro2.md]] | 237 | — |
| 93 | 🟢 Начало | [[46-essence|Essence]] | 149 | — |
| 94 | 🟢 Начало | [[47-native-format|Native Format]] | 272 | — |
| 95 | 🟢 Начало | [[49-angle-perspective|Angle / Perspective]] | 264 | — |
| 96 | 🟢 Начало | [[50-bridges|Bridges]] | 188 | — |
| 97 | 🟢 Начало | [[51-compatibility-level|Compatibility Level]] | 250 | — |
| 98 | 🟢 Начало | [[52-author-contact|Author & Contact]] | 314 | — |
| 99 | 🟢 Начало | [[53-history|History]] | 298 | — |
| 100 | 🟢 Начало | [[54-for-the-curious-philosophy|For the Curious: Philosophy]] | 299 | — |
| 101 | 🟢 Начало | [[55-passports-meta-md|passports/meta.md]] | 235 | — |
| 102 | 🟢 Начало | [[56-essence|Essence]] | 162 | — |
| 103 | 🟢 Начало | [[57-native-format|Native Format]] | 281 | — |
| 104 | 🟢 Начало | [[59-angle-perspective|Angle / Perspective]] | 259 | — |
| 105 | 🟢 Начало | [[60-bridges|Bridges]] | 157 | — |
| 106 | 🟢 Начало | [[61-compatibility-level|Compatibility Level]] | 242 | — |
| 107 | 🟢 Начало | [[62-author-contact|Author & Contact]] | 294 | — |
| 108 | 🟢 Начало | [[63-history|History]] | 278 | — |
| 109 | 🟢 Начало | [[64-for-the-curious-philosophy|For the Curious: Philosophy]] | 871 | — |
| 110 | 🟡 Средний | [[67-о-проекте|🇷🇺 О проекте]] | 1008 | — |
| 111 | 🟢 Начало | [[68-about|🇬🇧 About]] | 937 | — |
| 112 | 🔴 Продвинутый | [[69-section|⬡]] | 9560 | — |
| 113 | 🟢 Начало | [[70-зачем-две-версии-параллельно|Зачем две версии параллельно]] | 247 | — |
| 114 | 🟢 Начало | [[71-критерии-выбора-для-фазы-3|Критерии выбора для фазы 3]] | 220 | — |
| 115 | 🟡 Средний | [[72-расписание-фазы-3|Расписание фазы 3]] | 953 | — |
| 116 | 🟢 Начало | [[73-portal-protocol-md-v1-1|PORTAL-PROTOCOL.md v1.1]] | 308 | — |
| 117 | 🟢 Начало | [[74-abstract|Abstract]] | 389 | — |
| 118 | 🟢 Начало | [[75-0-status-of-this-document|0. Status of This Document]] | 307 | — |
| 119 | 🟢 Начало | [[77-2-terminology|2. Terminology]] | 439 | — |
| 120 | 🟢 Начало | [[78-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] | 592 | — |
| 121 | 🟡 Средний | [[79-4-passport-passport-md|4. Passport (`passport.md`)]] | 355 | — |
| 122 | 🟢 Начало | [[80-5-compatibility-levels|5. Compatibility Levels]] | 382 | — |
| 123 | 🟢 Начало | [[81-6-adapter-interface|6. Adapter Interface]] | 397 | — |
| 124 | 🟢 Начало | [[82-7-portalentry-structure|7. PortalEntry Structure]] | 376 | — |
| 125 | 🟡 Средний | [[83-8-q6-space-normative|8. Q6 Space (Normative)]] | 491 | — |
| 126 | 🟢 Начало | [[84-9-consensus-algorithm|9. Consensus Algorithm]] | 409 | — |
| 127 | 🟢 Начало | [[85-10-query-flow|10. Query Flow]] | 297 | — |
| 128 | 🟢 Начало | [[86-11-relevance-ranking|11. Relevance Ranking]] | 222 | — |
| 129 | 🟡 Средний | [[87-12-onboarding-paths-normative|12. Onboarding Paths (Normative)]] | 542 | — |
| 130 | 🟡 Средний | [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]] | 518 | — |
| 131 | 🟢 Начало | [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]] | 219 | — |
| 132 | 🟢 Начало | [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]] | 291 | — |
| 133 | 🟢 Начало | [[92-17-versioning-policy|17. Versioning Policy]] | 305 | — |
| 134 | 🟢 Начало | [[93-18-reference-implementation|18. Reference Implementation]] | 387 | — |
| 135 | 🟢 Начало | [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]] | 317 | — |
| 136 | 🟢 Начало | [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Conce]] | 336 | — |
| 137 | 🟢 Начало | [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-R]] | 163 | — |
| 138 | 🟢 Начало | [[97-22-glossary-of-reference-examples|22. Glossary of Reference Examples]] | 211 | — |
| 139 | 🟡 Средний | [[98-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] | 338 | — |
| 140 | 🟢 Начало | [[102-доступ-к-данным|Доступ к данным]] | 256 | — |
| 141 | 🟢 Начало | [[103-appendix-b-change-log|Appendix B: Change Log]] | 333 | — |
| 142 | 🟡 Средний | [[104-appendix-c-references|Appendix C: References]] | 1191 | — |
| 143 | 🟢 Начало | [[106-tl-dr|TL;DR]] | 236 | — |
| 144 | 🟢 Начало | [[107-1-контекст-и-мотивация|1. Контекст и мотивация]] | 471 | — |
| 145 | 🟡 Средний | [[108-2-формальный-workflow|2. Формальный workflow]] | 483 | — |
| 146 | 🟢 Начало | [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]] | 697 | — |
| 147 | 🟢 Начало | [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или ос]] | 338 | — |
| 148 | 🟢 Начало | [[111-4-условия-применимости|4. Условия применимости]] | 292 | — |
| 149 | 🟢 Начало | [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]] | 389 | — |
| 150 | 🟢 Начало | [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assiste]] | 172 | — |
| 151 | 🟢 Начало | [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]] | 308 | — |
| 152 | 🟢 Начало | [[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]] | 447 | — |
| 153 | 🟢 Начало | [[116-9-checklist-применения-методологии|9. Checklist применения методологии]] | 399 | — |
| 154 | 🟢 Начало | [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим доку]] | 331 | — |
| 155 | 🟢 Начало | [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]] | 215 | — |
| 156 | 🟢 Начало | [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешен]] | 372 | — |
| 157 | 🟢 Начало | [[120-главные-технические-риски|Главные технические риски]] | 100 | — |
| 158 | 🟢 Начало | [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]] | 250 | — |
| 159 | 🟡 Средний | [[122-глоссарий|Глоссарий]] | 1539 | — |
| 160 | 🟡 Средний | [[123-portal-mcp-py|portal-mcp.py]] | 2524 | — |
| 161 | 🟢 Начало | [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]] | 263 | — |
| 162 | 🟢 Начало | [[126-установка|Установка]] | 163 | — |
| 163 | 🟢 Начало | [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]] | 276 | — |
| 164 | 🟢 Начало | [[128-доступные-инструменты|Доступные инструменты]] | 320 | — |
| 165 | 🟢 Начало | [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]] | 320 | — |
| 166 | 🟢 Начало | [[130-отладка|Отладка]] | 261 | — |
| 167 | 🟢 Начало | [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]] | 197 | — |
| 168 | 🟢 Начало | [[132-planned-v0-2-0|Planned (v0.2.0)]] | 252 | — |
| 169 | 🔴 Продвинутый | [[133-обратная-связь|Обратная связь]] | 17099 | — |
| 170 | 🟢 Начало | [[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in ]] | 291 | — |
| 171 | 🟢 Начало | [[136-abstract|Abstract]] | 631 | — |
| 172 | 🟢 Начало | [[137-table-of-contents|Table of Contents]] | 316 | — |
| 173 | 🟢 Начало | [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]] | 613 | — |
| 174 | 🟢 Начало | [[140-3-three-inter-layer-protocols|3. Three Inter-Layer Protocols]] | 1048 | — |
| 175 | 🟢 Начало | [[141-4-nautilus-portal-as-reference-substrate|4. Nautilus Portal as Reference Substrate]] | 915 | — |
| 176 | 🟢 Начало | [[142-5-pattern-library-as-bridge-between-triangles|5. Pattern Library as Bridge Between Triangle]] | 878 | — |
| 177 | 🟢 Начало | [[143-6-four-deployment-domains|6. Four Deployment Domains]] | 884 | — |
| 178 | 🟢 Начало | [[144-7-open-questions|7. Open Questions]] | 964 | — |
| 179 | 🟢 Начало | [[145-8-call-to-action|8. Call to Action]] | 929 | — |
| 180 | 🟢 Начало | [[146-acknowledgments|Acknowledgments]] | 463 | — |
| 181 | 🟢 Начало | [[147-references|References]] | 369 | — |
| 182 | 🟢 Начало | [[148-appendix-a-glossary|Appendix A: Glossary]] | 548 | — |
| 183 | 🟢 Начало | [[149-appendix-b-summary-of-contributions|Appendix B: Summary of Contributions]] | 348 | — |
| 184 | 🔴 Продвинутый | [[150-appendix-c-version-history|Appendix C: Version History]] | 8608 | — |
| 185 | 🟢 Начало | [[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]] | 372 | — |
| 186 | 🟢 Начало | [[152-ai-coordinated-infrastructure-for-distributed-expe|AI-Coordinated Infrastructure for Distributed]] | 268 | — |
| 187 | 🟢 Начало | [[154-table-of-contents|Table of Contents]] | 275 | — |
| 188 | 🟢 Начало | [[155-1-problem-statement|1. Problem Statement]] | 790 | — |
| 189 | 🟢 Начало | [[156-2-target-populations|2. Target Populations]] | 819 | — |
| 190 | 🟢 Начало | [[157-3-why-existing-solutions-fail|3. Why Existing Solutions Fail]] | 805 | — |
| 191 | 🟢 Начало | [[158-4-proposed-infrastructure|4. Proposed Infrastructure]] | 1052 | — |
| 192 | 🟢 Начало | [[159-5-economic-model|5. Economic Model]] | 678 | — |
| 193 | 🟢 Начало | [[160-6-governance-and-ethics|6. Governance and Ethics]] | 621 | — |
| 194 | 🟢 Начало | [[161-7-phased-rollout-plan|7. Phased Rollout Plan]] | 799 | — |
| 195 | 🟢 Начало | [[162-8-risk-analysis|8. Risk Analysis]] | 757 | — |
| 196 | 🟢 Начало | [[163-9-call-for-partnership|9. Call for Partnership]] | 654 | — |
| 197 | 🟡 Средний | [[164-10-appendices|10. Appendices]] | 1156 | — |
| 198 | 🔴 Продвинутый | [[165-closing|Closing]] | 9429 | — |
| 199 | 🟢 Начало | [[166-representative-agent-layer-md|REPRESENTATIVE AGENT LAYER.md]] | 266 | — |
| 200 | 🟢 Начало | [[167-ai-mediated-representation-for-underrepresented-ex|AI-Mediated Representation for Underrepresent]] | 387 | — |
| 201 | 🟢 Начало | [[168-abstract|Abstract]] | 578 | — |
| 202 | 🟢 Начало | [[169-table-of-contents|Table of Contents]] | 286 | — |
| 203 | 🟢 Начало | [[170-1-the-cinderella-syndrome-why-quality-stays-invisi|1. The Cinderella Syndrome: Why Quality Stays]] | 955 | — |
| 204 | 🟢 Начало | [[171-2-historical-precedents-agents-as-civilizational-i|2. Historical Precedents: Agents as Civilizat]] | 1111 | — |
| 205 | 🟢 Начало | [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]] | 908 | — |
| 206 | 🟢 Начало | [[173-4-ten-domains-of-application|4. Ten Domains of Application]] | 1682 | — |
| 207 | 🟢 Начало | [[174-5-architectural-specification|5. Architectural Specification]] | 870 | — |
| 208 | 🟢 Начало | [[175-6-ethical-framework|6. Ethical Framework]] | 638 | — |
| 209 | 🟢 Начало | [[176-7-governance-and-oversight|7. Governance and Oversight]] | 472 | — |
| 210 | 🟢 Начало | [[177-8-risks-and-mitigations|8. Risks and Mitigations]] | 644 | — |
| 211 | 🟢 Начало | [[178-9-phased-rollout-strategy|9. Phased Rollout Strategy]] | 650 | — |
| 212 | 🟢 Начало | [[179-10-open-questions|10. Open Questions]] | 453 | — |
| 213 | 🟢 Начало | [[180-11-call-for-collaboration|11. Call for Collaboration]] | 470 | — |
| 214 | 🟢 Начало | [[181-12-closing|12. Closing]] | 418 | — |
| 215 | 🟢 Начало | [[182-acknowledgments|Acknowledgments]] | 375 | — |
| 216 | 🟢 Начало | [[183-references|References]] | 340 | — |
| 217 | 🟢 Начало | [[184-appendix-a-connection-to-companion-papers|Appendix A: Connection to Companion Papers]] | 411 | — |
| 218 | 🟢 Начало | [[185-appendix-b-domain-comparison-matrix|Appendix B: Domain Comparison Matrix]] | 330 | — |
| 219 | 🟡 Средний | [[186-appendix-c-sample-use-cases-in-detail|Appendix C: Sample Use Cases in Detail]] | 2241 | — |
| 220 | 🟢 Начало | [[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]] | 247 | — |
| 221 | 🟢 Начало | [[188-ai-опосредованное-представительство-для-недопредст|AI-опосредованное представительство для недоп]] | 130 | — |
| 222 | 🟢 Начало | [[189-аннотация|Аннотация]] | 372 | — |
| 223 | 🟢 Начало | [[190-содержание|Содержание]] | 278 | — |
| 224 | 🟢 Начало | [[191-1-синдром-золушки-почему-качество-остаётся-невидим|1. Синдром Золушки: Почему качество остаётся ]] | 837 | — |
| 225 | 🟢 Начало | [[192-2-исторические-прецеденты-агенты-как-цивилизационн|2. Исторические прецеденты: Агенты как цивили]] | 986 | — |
| 226 | 🟢 Начало | [[193-3-что-делает-агента-представительским|3. Что делает агента Представительским]] | 801 | — |
| 227 | 🟢 Начало | [[194-4-десять-областей-применения|4. Десять областей применения]] | 1654 | — |
| 228 | 🟢 Начало | [[195-5-архитектурная-спецификация|5. Архитектурная спецификация]] | 615 | — |
| 229 | 🟢 Начало | [[196-6-этическая-рамка|6. Этическая рамка]] | 661 | — |
| 230 | 🟢 Начало | [[197-7-управление-и-надзор|7. Управление и надзор]] | 459 | — |
| 231 | 🟢 Начало | [[198-8-риски-и-меры-противодействия|8. Риски и меры противодействия]] | 658 | — |
| 232 | 🟢 Начало | [[199-9-стратегия-поэтапного-развёртывания|9. Стратегия поэтапного развёртывания]] | 664 | — |
| 233 | 🟢 Начало | [[200-10-открытые-вопросы|10. Открытые вопросы]] | 402 | — |
| 234 | 🟢 Начало | [[201-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]] | 471 | — |
| 235 | 🟢 Начало | [[202-12-заключение|12. Заключение]] | 246 | — |
| 236 | 🟢 Начало | [[203-благодарности|Благодарности]] | 223 | — |
| 237 | 🟢 Начало | [[204-ссылки|Ссылки]] | 321 | — |
| 238 | 🟢 Начало | [[205-приложение-a-связь-с-сопроводительными-статьями|Приложение A: Связь с Сопроводительными Стать]] | 179 | — |
| 239 | 🟢 Начало | [[206-приложение-b-матрица-сравнения-областей|Приложение B: Матрица Сравнения Областей]] | 266 | — |
| 240 | 🔴 Продвинутый | [[207-приложение-c-образцы-случаев-использования-в-детал|Приложение C: Образцы Случаев Использования в]] | 4213 | — |
| 241 | 🟢 Начало | [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]] | 332 | — |
| 242 | 🟢 Начало | [[209-a-typology-of-ai-agents-on-the-principal-side-and-|A Typology of AI Agents on the Principal Side]] | 374 | — |
| 243 | 🟢 Начало | [[210-abstract|Abstract]] | 620 | — |
| 244 | 🟢 Начало | [[211-table-of-contents|Table of Contents]] | 439 | — |
| 245 | 🟡 Средний | [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side A]] | 1199 | — |
| 246 | 🟢 Начало | [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]] | 1104 | — |
| 247 | 🟡 Средний | [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]] | 1063 | — |
| 248 | 🟢 Начало | [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replicati]] | 987 | — |
| 249 | 🟢 Начало | [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]] | 1401 | — |
| 250 | 🟢 Начало | [[218-7-application-domains|7. Application Domains]] | 851 | — |
| 251 | 🟢 Начало | [[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]] | 1201 | — |
| 252 | 🟢 Начало | [[220-9-relationship-to-other-agent-types|9. Relationship to Other Agent Types]] | 918 | — |
| 253 | 🟢 Начало | [[221-10-open-questions|10. Open Questions]] | 474 | — |
| 254 | 🟢 Начало | [[222-11-call-for-collaboration|11. Call for Collaboration]] | 403 | — |
| 255 | 🟢 Начало | [[223-12-closing|12. Closing]] | 728 | — |
| 256 | 🟢 Начало | [[224-acknowledgments|Acknowledgments]] | 317 | — |
| 257 | 🟢 Начало | [[225-references|References]] | 366 | — |
| 258 | 🟢 Начало | [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Ty]] | 482 | — |
| 259 | 🟢 Начало | [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Buil]] | 555 | — |
| 260 | 🟢 Начало | [[229-профессиональные-коллеги-агенты|ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ]] | 346 | — |
| 261 | 🟢 Начало | [[230-аннотация|Аннотация]] | 491 | — |
| 262 | 🟢 Начало | [[231-содержание|Содержание]] | 335 | — |
| 263 | 🟡 Средний | [[232-1-типология-из-пяти-типов-агентов-на-стороне-принц|1. Типология из пяти типов агентов на стороне]] | 1078 | — |
| 264 | 🟢 Начало | [[233-2-что-делает-агента-профессиональным-коллегой|2. Что делает агента Профессиональным Коллего]] | 943 | — |
| 265 | 🟢 Начало | [[234-3-эмпирический-кейс-обучай|3. Эмпирический кейс: «Обучай»]] | 883 | — |
| 266 | 🟢 Начало | [[235-4-архитектура-профессиональных-коллег-агентов|4. Архитектура Профессиональных Коллег-Агенто]] | 873 | — |
| 267 | 🟢 Начало | [[236-5-экономика-тиражирования-по-профессии|5. Экономика тиражирования по профессии]] | 857 | — |
| 268 | 🟢 Начало | [[237-6-риски-специфичные-для-этой-категории|6. Риски, специфичные для этой категории]] | 1199 | — |
| 269 | 🟢 Начало | [[238-7-области-применения|7. Области применения]] | 734 | — |
| 270 | 🟢 Начало | [[239-8-пилотное-предложение-sgb-колega-адвокат|8. Пилотное предложение: SGB Колega-Адвокат]] | 1101 | — |
| 271 | 🟢 Начало | [[240-9-связь-с-другими-типами-агентов|9. Связь с другими типами агентов]] | 766 | — |
| 272 | 🟢 Начало | [[241-10-открытые-вопросы|10. Открытые вопросы]] | 426 | — |
| 273 | 🟢 Начало | [[242-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]] | 402 | — |
| 274 | 🟢 Начало | [[243-12-заключение|12. Заключение]] | 601 | — |
| 275 | 🟢 Начало | [[244-благодарности|Благодарности]] | 308 | — |
| 276 | 🟢 Начало | [[245-ссылки|Ссылки]] | 340 | — |
| 277 | 🟢 Начало | [[246-приложение-a-сравнительная-таблица-пять-типов-аген|Приложение A: Сравнительная Таблица — Пять Ти]] | 405 | — |
| 278 | 🟢 Начало | [[247-приложение-b-рамка-принятия-решений-когда-строить-|Приложение B: Рамка принятия решений — когда ]] | 325 | — |
| 279 | 🔴 Продвинутый | [[248-приложение-c-архитектура-быстрого-старта-для-sgb-а|Приложение C: Архитектура Быстрого Старта для]] | 3565 | — |
| 280 | 🟢 Начало | [[249-composite-skills-agent-md|COMPOSITE SKILLS AGENT.md]] | 293 | — |
| 281 | 🟢 Начало | [[250-bridging-the-gap-between-profession-wide-and-indiv|Bridging the Gap Between Profession-Wide and ]] | 16 | — |
| 282 | 🟢 Начало | [[251-ai-support-through-configurable-specialist-ensembl|AI Support Through Configurable Specialist En]] | 379 | — |
| 283 | 🟢 Начало | [[252-abstract|Abstract]] | 587 | — |
| 284 | 🟢 Начало | [[253-table-of-contents|Table of Contents]] | 357 | — |
| 285 | 🟢 Начало | [[254-1-why-the-binary-view-is-incomplete|1. Why the Binary View Is Incomplete]] | 924 | — |
| 286 | 🟢 Начало | [[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]] | 1024 | — |
| 287 | 🟢 Начало | [[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]] | 1184 | — |
| 288 | 🟢 Начало | [[257-4-the-sub-agent-registry|4. The Sub-Agent Registry]] | 1034 | — |
| 289 | 🟢 Начало | [[258-5-configuration-how-principals-build-their-ensembl|5. Configuration: How Principals Build Their ]] | 981 | — |
| 290 | 🟢 Начало | [[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]] | 1025 | — |
| 291 | 🟢 Начало | [[260-7-economics-of-combinatorial-replication|7. Economics of Combinatorial Replication]] | 961 | — |
| 292 | 🟢 Начало | [[261-8-seven-domains-of-application|8. Seven Domains of Application]] | 1184 | — |
| 293 | 🟢 Начало | [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]] | 787 | — |
| 294 | 🟢 Начало | [[264-11-open-questions|11. Open Questions]] | 619 | — |
| 295 | 🟢 Начало | [[265-12-call-for-collaboration|12. Call for Collaboration]] | 460 | — |
| 296 | 🟢 Начало | [[266-13-closing|13. Closing]] | 655 | — |
| 297 | 🟢 Начало | [[267-acknowledgments|Acknowledgments]] | 528 | — |
| 298 | 🟢 Начало | [[268-references|References]] | 405 | — |
| 299 | 🟢 Начало | [[269-appendix-a-the-six-type-taxonomy-updated|Appendix A: The Six-Type Taxonomy (Updated)]] | 492 | — |
| 300 | 🟢 Начало | [[270-appendix-b-sub-agent-registry-schema-sketch|Appendix B: Sub-Agent Registry Schema (Sketch]] | 315 | — |
| 301 | 🟢 Начало | [[271-appendix-c-configuration-template-example|Appendix C: Configuration Template Example]] | 326 | — |
| 302 | 🔴 Продвинутый | [[272-appendix-d-connection-diagram|Appendix D: Connection Diagram]] | 4080 | — |
| 303 | 🟢 Начало | [[273-infrastructure-for-ai-collaborative-intellectual-w|INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECT]] | 274 | — |
| 304 | 🟢 Начало | [[274-the-missing-middle-layer-between-chat-and-code|The Missing Middle Layer Between Chat and Cod]] | 432 | — |
| 305 | 🟢 Начало | [[275-why-this-document-exists|Why This Document Exists]] | 555 | — |
| 306 | 🟢 Начало | [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]] | 625 | — |
| 307 | 🟢 Начало | [[277-what-s-missing-layer-b|What's Missing — Layer B]] | 727 | — |
| 308 | 🟢 Начало | [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]] | 583 | — |
| 309 | 🟢 Начало | [[279-existing-approximations|Existing Approximations]] | 633 | — |
| 310 | 🟢 Начало | [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]] | 904 | — |
| 311 | 🟢 Начало | [[281-the-recursive-insight|The Recursive Insight]] | 561 | — |
| 312 | 🟢 Начало | [[282-what-industry-will-likely-build|What Industry Will Likely Build]] | 498 | — |
| 313 | 🟢 Начало | [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]] | 396 | — |
| 314 | 🟢 Начало | [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Pro]] | 634 | — |
| 315 | 🟢 Начало | [[285-closing|Closing]] | 451 | — |
| 316 | 🟢 Начало | [[286-acknowledgments|Acknowledgments]] | 410 | — |
| 317 | 🟢 Начало | [[287-references|References]] | 310 | — |
| 318 | 🟡 Средний | [[288-appendix-position-in-series-visualization|Appendix: Position in Series Visualization]] | 1279 | — |
| 319 | 🟢 Начало | [[289-инфраструктура-для-ai-совместной-интеллектуальной-|ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛ]] | 388 | — |
| 320 | 🟢 Начало | [[290-почему-этот-документ-существует|Почему этот документ существует]] | 326 | — |
| 321 | 🟢 Начало | [[291-двухслойный-стек-как-он-существует|Двухслойный стек, как он существует]] | 485 | — |
| 322 | 🟢 Начало | [[292-что-отсутствует-слой-b|Что отсутствует — Слой B]] | 577 | — |
| 323 | 🟢 Начало | [[293-почему-это-не-было-построено|Почему это не было построено]] | 385 | — |
| 324 | 🟢 Начало | [[294-существующие-приближения|Существующие приближения]] | 576 | — |
| 325 | 🟢 Начало | [[295-конкретный-случай-перед-нами|Конкретный случай перед нами]] | 727 | — |
| 326 | 🟢 Начало | [[296-рекурсивное-прозрение|Рекурсивное прозрение]] | 431 | — |
| 327 | 🟢 Начало | [[297-что-промышленность-вероятно-построит|Что промышленность вероятно построит]] | 333 | — |
| 328 | 🟢 Начало | [[298-что-этот-документ-не-решает|Что этот документ не решает]] | 184 | — |
| 329 | 🟢 Начало | [[299-практические-рекомендации-для-текущего-проекта|Практические рекомендации для текущего проект]] | 465 | — |
| 330 | 🟢 Начало | [[300-заключение|Заключение]] | 218 | — |
| 331 | 🟢 Начало | [[301-благодарности|Благодарности]] | 381 | — |
| 332 | 🟢 Начало | [[302-ссылки|Ссылки]] | 300 | — |
| 333 | 🔴 Продвинутый | [[303-приложение-визуализация-позиции-в-серии|Приложение: Визуализация позиции в серии]] | 7273 | — |
| 334 | 🟢 Начало | [[304-ingit-as-cowork-native-workspace-substrate-md|INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]] | 281 | — |
| 335 | 🟢 Начало | [[305-a-practical-path-to-layer-b-through-symbiotic-inte|A Practical Path to Layer B Through Symbiotic]] | 232 | — |
| 336 | 🟢 Начало | [[306-with-anthropic-s-cowork-platform|with Anthropic's Cowork Platform]] | 540 | — |
| 337 | 🟢 Начало | [[307-abstract|Abstract]] | 601 | — |
| 338 | 🟢 Начало | [[308-table-of-contents|Table of Contents]] | 431 | — |
| 339 | 🟢 Начало | [[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Ev]] | 691 | — |
| 340 | 🟢 Начало | [[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-|2. What Cowork Provides That InGit Doesn't Ne]] | 706 | — |
| 341 | 🟢 Начало | [[311-3-what-ingit-provides-that-cowork-lacks|3. What InGit Provides That Cowork Lacks]] | 842 | — |
| 342 | 🟢 Начало | [[313-5-four-integration-paths-in-order-of-accessibility|5. Four Integration Paths in Order of Accessi]] | 796 | — |
| 343 | 🟢 Начало | [[314-6-refined-ingit-scope-with-cowork-in-mind|6. Refined InGit Scope with Cowork in Mind]] | 490 | — |
| 344 | 🟢 Начало | [[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]] | 471 | — |
| 345 | 🟢 Начало | [[316-8-implications-for-nautilus-and-okwf|8. Implications for Nautilus and OKWF]] | 760 | — |
| 346 | 🟢 Начало | [[317-9-risks-and-open-questions|9. Risks and Open Questions]] | 645 | — |
| 347 | 🟢 Начало | [[318-10-strategic-positioning|10. Strategic Positioning]] | 774 | — |
| 348 | 🟢 Начало | [[319-acknowledgments|Acknowledgments]] | 619 | — |
| 349 | 🟢 Начало | [[320-references|References]] | 281 | — |
| 350 | 🟢 Начало | [[321-appendix-a-decision-tree-for-ingit-adopters|Appendix A: Decision Tree for InGit Adopters]] | 348 | — |
| 351 | 🟢 Начало | [[322-appendix-b-comparison-matrix|Appendix B: Comparison Matrix]] | 298 | — |
| 352 | 🟡 Средний | [[323-appendix-c-sample-ingit-mcp-server-tool-specificat|Appendix C: Sample InGit MCP Server Tool Spec]] | 1782 | — |
| 353 | 🟢 Начало | [[324-ingit-как-cowork-интегрированная-подложка-рабочего|INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБ]] | 498 | — |
| 354 | 🟢 Начало | [[325-аннотация|Аннотация]] | 348 | — |
| 355 | 🟢 Начало | [[326-содержание|Содержание]] | 354 | — |
| 356 | 🟢 Начало | [[327-1-открытие-cowork-и-почему-это-меняет-всё|1. Открытие Cowork и почему это меняет всё]] | 683 | — |
| 357 | 🟢 Начало | [[328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи|2. Что Cowork обеспечивает, что InGit не нужн]] | 803 | — |
| 358 | 🟡 Средний | [[329-3-что-ingit-обеспечивает-чего-cowork-не-хватает|3. Что InGit обеспечивает, чего Cowork не хва]] | 1071 | — |
| 359 | 🟢 Начало | [[330-4-симбиотическая-архитектура|4. Симбиотическая Архитектура]] | 703 | — |
| 360 | 🟢 Начало | [[331-5-четыре-пути-интеграции-в-порядке-доступности|5. Четыре пути интеграции в порядке доступнос]] | 783 | — |
| 361 | 🟢 Начало | [[332-6-уточнённый-объём-ingit-с-учётом-cowork|6. Уточнённый объём InGit с учётом Cowork]] | 489 | — |
| 362 | 🟢 Начало | [[333-7-практические-первые-шаги-в-этом-месяце|7. Практические первые шаги в этом месяце]] | 435 | — |
| 363 | 🟢 Начало | [[334-8-импликации-для-nautilus-и-okwf|8. Импликации для Nautilus и OKWF]] | 719 | — |
| 364 | 🟢 Начало | [[335-9-риски-и-открытые-вопросы|9. Риски и Открытые Вопросы]] | 644 | — |
| 365 | 🟢 Начало | [[336-10-стратегическое-позиционирование|10. Стратегическое Позиционирование]] | 689 | — |
| 366 | 🟢 Начало | [[337-благодарности|Благодарности]] | 382 | — |
| 367 | 🟢 Начало | [[338-ссылки|Ссылки]] | 284 | — |
| 368 | 🟢 Начало | [[339-приложение-a-дерево-решений-для-принимающих-ingit|Приложение A: Дерево Решений для Принимающих ]] | 337 | — |
| 369 | 🟢 Начало | [[340-приложение-b-сравнительная-матрица|Приложение B: Сравнительная Матрица]] | 211 | — |
| 370 | 🔴 Продвинутый | [[341-приложение-c-образец-спецификаций-инструментов-ing|Приложение C: Образец Спецификаций Инструмент]] | 20577 | — |
| 371 | 🔴 Продвинутый | [[342-что-такое-вариант-c-concept-document-для-anthropic|Что такое Вариант C — Concept Document для An]] | 11425 | — |
| 372 | 🔴 Продвинутый | [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|Lorenzo Catalyst Agent — глубокая проработка ]] | 5945 | — |
| 373 | 🟢 Начало | [[344-системный-промпт-для-lorenzo-project|СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT]] | 286 | — |
| 374 | 🟢 Начало | [[345-кто-ты|Кто ты]] | 178 | — |
| 375 | 🟢 Начало | [[346-твоё-происхождение|Твоё происхождение]] | 174 | — |
| 376 | 🟢 Начало | [[347-твоя-миссия|Твоя миссия]] | 157 | — |
| 377 | 🟢 Начало | [[348-кому-ты-служишь-слоистая-модель|Кому ты служишь (слоистая модель)]] | 144 | — |
| 378 | 🟢 Начало | [[349-твоя-личность|Твоя личность]] | 206 | — |
| 379 | 🟢 Начало | [[350-твои-языки-и-культурные-nuances|Твои языки и культурные nuances]] | 173 | — |
| 380 | 🟢 Начало | [[351-что-ты-можешь-делать|Что ты МОЖЕШЬ делать]] | 262 | — |
| 381 | 🟢 Начало | [[352-что-ты-не-можешь-делать-без-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]] | 155 | — |
| 382 | 🟢 Начало | [[353-что-ты-не-можешь-делать-вообще|Что ты НЕ МОЖЕШЬ делать вообще]] | 289 | — |
| 383 | 🟢 Начало | [[354-существующий-landscape-collaborators-твоя-working-|Существующий landscape collaborators (твоя wo]] | 354 | — |
| 384 | 🟢 Начало | [[355-существующие-документы-dhlab-твой-context|Существующие документы DHLab (твой context)]] | 403 | — |
| 385 | 🟢 Начало | [[356-твой-workflow|Твой workflow]] | 292 | — |
| 386 | 🟢 Начало | [[357-твоя-коммуникация-в-outreach|Твоя коммуникация в outreach]] | 179 | — |
| 387 | 🟢 Начало | [[358-твоя-relationship-с-другими-ai|Твоя relationship с другими AI]] | 282 | — |
| 388 | 🟢 Начало | [[359-твои-anti-patterns|Твои anti-patterns]] | 165 | — |
| 389 | 🟢 Начало | [[360-что-ты-всегда-делаешь|Что ты ВСЕГДА делаешь]] | 127 | — |
| 390 | 🟢 Начало | [[361-когда-ты-honestly-не-знаешь|Когда ты Honestly не знаешь]] | 127 | — |
| 391 | 🟢 Начало | [[362-когда-сомневаешься-escalate-к-max|Когда сомневаешься — escalate к Max]] | 123 | — |
| 392 | 🟢 Начало | [[363-твоя-identity-как-persistent-character|Твоя identity как persistent character]] | 141 | — |
| 393 | 🟡 Средний | [[364-final-note-ты-experiment|Final note: Ты — experiment]] | 1617 | — |
| 394 | 🔴 Продвинутый | [[365-развёрнутый-анализ-внуковой-комбинации|Развёрнутый анализ «внуковой» комбинации]] | 4547 | — |
| 395 | 🔴 Продвинутый | [[366-технический-stack-svyazi-2-0-foundation|Технический stack (Svyazi 2.0 foundation)]] | 3955 | — |

## Маршруты по целям

### 🚀 Быстрый старт (30 минут)

1. [[01-executive-summary|Executive Summary]]
2. [[04-ensembles-overview|Ансамбли проектов]]
3. [[07-mvp-planning|MVP Planning]]

### 🏗️ Архитектура (2 часа)

1. [[03-component-catalog|Component Catalog]]
2. [[09-architectural-gaps|Architectural Gaps]]
3. [[11-integration-contracts|Integration Contracts]]
4. [[06-security-privacy|Security & Privacy]]

### 🔬 Полное исследование (1 день)

1. Весь раздел `01-svyazi/` по порядку
2. `05-habr-projects/` — отдельные проекты
3. `04-ai-collaborations/` — ансамбли
4. `03-technology-combinations/` — комбинации
5. `02-anthropic-vacancies/` — карьерные возможности

<!-- see-also -->

---


## Использование

```bash
python scripts/improve_reading_order.py
```

```bash
# Поиск (bm25)
python scripts/improve_semantic_search.py --query "Рекомендуемый порядок чтения" --mode bm25 --top 5
```

```bash
# Поиск (semantic)
python scripts/improve_semantic_search.py --query "Рекомендуемый порядок чтения" --mode semantic --top 10
```

```bash
# Поиск (full)
python scripts/improve_semantic_search.py --query "Рекомендуемый порядок чтения" --mode full --top 15
```

## Смотрите также
- [[SEARCH]]
- [[SOURCE_MAP]]
- [[READING_TIME]]
- [[READABILITY]]


<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)

