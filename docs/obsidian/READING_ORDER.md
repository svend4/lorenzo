---
title: "Рекомендуемый порядок чтения"
tags:
  - general
date: 2026-04-29
---

# Рекомендуемый порядок чтения

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> title: "Рекомендуемый порядок чтения"
**Проекты:** Svyazi, Yodoca, MemNet, Wikontic

---

<!-- toc -->
## Содержание

- [Маршруты по целям](#маршруты-по-целям)
  - [🚀 Быстрый старт (30 минут)](#быстрый-старт-30-минут)
  - [🏗️ Архитектура (2 часа)](#архитектура-2-часа)
  - [🔬 Полное исследование (1 день)](#полное-исследование-1-день)

---

<!-- tags: memory, rag, security, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->




От базовых концепций к сложным. Начните с зелёных (🟢), затем жёлтые (🟡), красные (🔴).

| # | Уровень | Документ | Слов | Предварительно прочитать |
|---|---------|----------|------|--------------------------|
| 1 | 🟢 Начало | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](04-ai-collaborations/01-executive-summary.md) | 708 | — |
| 2 | 🟡 Средний | [[04-ensembles-overview]] | 1274 | — |
| 3 | 🟢 Начало | [[00-intro-part2|Продолжение исследования для Svyazi 2.0]] | 6 | — |
| 4 | 🟢 Начало | [[02-methodology|Методика и рамка отбора проектов]] | 428 | — |
| 5 | 🟡 Средний | [[03-component-catalog]] | 1395 | — |
| 6 | 🟢 Начало | [[11-integration-contracts]] | 745 | `09-architectural-gaps.md` |
| 7 | 🟢 Начало | [[09-architectural-gaps]] | 757 | `01-executive-summary.md`, `03-component-catalog.md` |
| 8 | 🟢 Начало | [[10-second-order-ensembles]] | 916 | `04-ensembles-overview.md` |
| 9 | 🟢 Начало | [[06-security-privacy]] | 821 | — |
| 10 | 🟡 Средний | [[07-mvp-planning]] | 1083 | — |
| 11 | 🟢 Начало | [[12-roadmap]] | 733 | `07-mvp-planning.md`, `11-integration-contracts.md` |
| 12 | 🟢 Начало | [[13-contacts]] | 827 | — |
| 13 | 🟢 Начало | [[14-limitations]] | 636 | — |
| 14 | 🟢 Начало | [[08-conclusions]] | 360 | — |
| 15 | 🟢 Начало | [[01-synthesis|Синтез: как проекты собираются вместе]] | 184 | — |
| 16 | 🟢 Начало | [[02-collaboration-partners|Авторы и контакты]] | 303 | — |
| 17 | 🟢 Начало | [[wikontic|Wikontic: семантический граф]] | 306 | — |
| 18 | 🟢 Начало | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 419 | — |
| 19 | 🟢 Начало | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 303 | — |
| 20 | 🟡 Средний | [[memnet|MemNet: исследовательская память]] | 7271 | — |
| 21 | 🟢 Начало | [[01-executive-summary|Executive summary]] | 647 | — |
| 22 | 🟡 Средний | [[00-intro|Введение]] | 11445 | — |
| 23 | 🟢 Начало | [[02-методика-и-рамка-отбора|Методика и рамка отбора]] | 495 | — |
| 24 | 🟡 Средний | [[03-карта-найденных-проектов-и-паттернов|Карта найденных проектов и паттернов]] | 1553 | — |
| 25 | 🟡 Средний | [[04-приоритетные-ансамбли|Приоритетные ансамбли]] | 1418 | — |
| 26 | 🟡 Средний | [[05-план-прототипа-и-возможные-контакты|План прототипа и возможные контакты]] | 1212 | — |
| 27 | 🟢 Начало | [[06-безопасность-приватность-и-бюджетный-роутинг|Безопасность, приватность и бюджетный роутинг]] | 966 | — |
| 28 | 🟢 Начало | [[07-выводы|Выводы]] | 542 | — |
| 29 | 🟢 Начало | [[08-что-это-продолжение-добавляет|Что это продолжение добавляет]] | 492 | — |
| 30 | 🟢 Начало | [[09-архитектурные-зазоры-которые-важнее-новых-инструме|Архитектурные зазоры, которые важнее новых ин]] | 901 | — |
| 31 | 🟡 Средний | [[10-новые-ансамбли-следующего-шага|Новые ансамбли следующего шага]] | 1062 | — |
| 32 | 🟢 Начало | [[11-интеграционный-контракт-который-стоит-зафиксироват|Интеграционный контракт, который стоит зафикс]] | 928 | — |
| 33 | 🟢 Начало | [[12-дорожная-карта-прототипа-следующей-итерации|Дорожная карта прототипа следующей итерации]] | 862 | — |
| 34 | 🟢 Начало | [[13-контактная-стратегия-и-узкие-вопросы-для-авторов|Контактная стратегия и узкие вопросы для авто]] | 956 | — |
| 35 | 🟡 Средний | [[14-ограничения-лицензии-и-что-пока-лучше-не-склеивать|Ограничения, лицензии и что пока лучше не скл]] | 3362 | — |
| 36 | 🟢 Начало | [[01-agent-routing|Агентные системы и роутинг]] | 257 | — |
| 37 | 🟢 Начало | [[02-knowledge-graphs|Графы знаний и Legal AI]] | 766 | — |
| 38 | 🟢 Начало | [[03-local-first|Local-first и P2P стек]] | 386 | — |
| 39 | 🟢 Начало | [[04-sozialrecht-domain|Домен: немецкое социальное право]] | 172 | — |
| 40 | 🟢 Начало | [[05-benchmarks|Бенчмарки и производительность]] | 863 | — |
| 41 | 🟢 Начало | [[153-executive-summary|Executive Summary]] | 370 | — |
| 42 | 🟢 Начало | [[38-content-overview|Content Overview]] | 148 | — |
| 43 | 🔴 Продвинутый | [[01-интегральный-анализ-профиля-svend4|Интегральный анализ профиля svend4]] | 19103 | — |
| 44 | 🟢 Начало | [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]] | 152 | — |
| 45 | 🟢 Начало | [[65-readme-md|README.md]] | 153 | — |
| 46 | 🟢 Начало | [[48-content-overview|Content Overview]] | 206 | — |
| 47 | 🟢 Начало | [[58-content-overview|Content Overview]] | 147 | — |
| 48 | 🟢 Начало | [[12-content-overview|Content Overview]] | 113 | — |
| 49 | 🟢 Начало | [[31-content-overview|Content Overview]] | 113 | — |
| 50 | 🔴 Продвинутый | [[00-intro|Введение]] | 8884 | — |
| 51 | 🟢 Начало | [[76-1-introduction|1. Introduction]] | 473 | — |
| 52 | 🟢 Начало | [[105-review-methodology-md|REVIEW_METHODOLOGY.md]] | 128 | — |
| 53 | 🟢 Начало | [[06-1-introduction|1. Introduction]] | 380 | — |
| 54 | 🔴 Продвинутый | [[02-общий-план-развития-nautilus-portal-protocol|ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL]] | 3181 | — |
| 55 | 🟢 Начало | [[215-4-architecture-of-professional-colleague-agents|4. Architecture of Professional Colleague Age]] | 901 | — |
| 56 | 🟢 Начало | [[139-2-the-double-triangle-architecture|2. The Double-Triangle Architecture]] | 755 | — |
| 57 | 🟡 Средний | [[228-appendix-c-quick-start-architecture-for-sgb-advoca|Appendix C: Quick-Start Architecture for SGB ]] | 1730 | — |
| 58 | 🟢 Начало | [[312-4-the-symbiotic-architecture|4. The Symbiotic Architecture]] | 678 | — |
| 59 | 🟢 Начало | [[03-portal-protocol-md|PORTAL-PROTOCOL.md]] | 150 | — |
| 60 | 🟢 Начало | [[134-the-double-triangle-architecture-md|THE DOUBLE-TRIANGLE ARCHITECTURE.md]] | 130 | — |
| 61 | 🟢 Начало | [[263-10-risks-specific-to-composite-architectures|10. Risks Specific to Composite Architectures]] | 788 | — |
| 62 | 🟢 Начало | [[04-abstract|Abstract]] | 188 | — |
| 63 | 🟢 Начало | [[05-0-status-of-this-document|0. Status of This Document]] | 162 | — |
| 64 | 🟢 Начало | [[23-11-security-considerations|11. Security Considerations]] | 248 | — |
| 65 | 🟢 Начало | [[90-15-security-considerations|15. Security Considerations]] | 354 | — |
| 66 | 🟢 Начало | [[07-2-terminology|2. Terminology]] | 313 | — |
| 67 | 🟢 Начало | [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] | 422 | — |
| 68 | 🟢 Начало | [[09-4-passport-passport-md|4. Passport (`passport.md`)]] | 197 | — |
| 69 | 🟢 Начало | [[13-angle-perspective|Angle / Perspective]] | 127 | — |
| 70 | 🟢 Начало | [[16-history|History]] | 104 | — |
| 71 | 🟢 Начало | [[17-5-compatibility-levels|5. Compatibility Levels]] | 300 | — |
| 72 | 🟢 Начало | [[18-6-adapter-interface|6. Adapter Interface]] | 425 | — |
| 73 | 🟢 Начало | [[19-7-portalentry-structure|7. PortalEntry Structure]] | 260 | — |
| 74 | 🟢 Начало | [[20-8-consensus-algorithm|8. Consensus Algorithm]] | 302 | — |
| 75 | 🟢 Начало | [[21-9-query-flow|9. Query Flow]] | 237 | — |
| 76 | 🟢 Начало | [[22-10-queryresult-structure|10. QueryResult Structure]] | 195 | — |
| 77 | 🟢 Начало | [[24-12-versioning-policy|12. Versioning Policy]] | 237 | — |
| 78 | 🟢 Начало | [[25-13-reference-implementation|13. Reference Implementation]] | 153 | — |
| 79 | 🟢 Начало | [[26-14-adr-001-federation-over-merging|14. ADR-001: Federation over Merging]] | 232 | — |
| 80 | 🟢 Начало | [[27-15-glossary-of-examples|15. Glossary of Examples]] | 149 | — |
| 81 | 🟢 Начало | [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] | 235 | — |
| 82 | 🟢 Начало | [[34-appendix-b-change-log|Appendix B: Change Log]] | 620 | — |
| 83 | 🟢 Начало | [[35-passports-info1-md|passports/info1.md]] | 133 | — |
| 84 | 🟢 Начало | [[36-essence|Essence]] | 179 | — |
| 85 | 🟢 Начало | [[37-native-format|Native Format]] | 234 | — |
| 86 | 🟢 Начало | [[39-angle-perspective|Angle / Perspective]] | 173 | — |
| 87 | 🟢 Начало | [[40-bridges|Bridges]] | 211 | — |
| 88 | 🟢 Начало | [[41-compatibility-level|Compatibility Level]] | 152 | — |
| 89 | 🟢 Начало | [[42-author-contact|Author & Contact]] | 145 | — |
| 90 | 🟢 Начало | [[43-history|History]] | 165 | — |
| 91 | 🟢 Начало | [[44-for-the-curious-philosophy|For the Curious: Philosophy]] | 195 | — |
| 92 | 🟢 Начало | [[45-passports-pro2-md|passports/pro2.md]] | 137 | — |
| 93 | 🟢 Начало | [[46-essence|Essence]] | 170 | — |
| 94 | 🟢 Начало | [[47-native-format|Native Format]] | 187 | — |
| 95 | 🟢 Начало | [[49-angle-perspective|Angle / Perspective]] | 168 | — |
| 96 | 🟢 Начало | [[50-bridges|Bridges]] | 211 | — |
| 97 | 🟢 Начало | [[51-compatibility-level|Compatibility Level]] | 149 | — |
| 98 | 🟢 Начало | [[52-author-contact|Author & Contact]] | 173 | — |
| 99 | 🟢 Начало | [[53-history|History]] | 201 | — |
| 100 | 🟢 Начало | [[54-for-the-curious-philosophy|For the Curious: Philosophy]] | 204 | — |
| 101 | 🟢 Начало | [[55-passports-meta-md|passports/meta.md]] | 134 | — |
| 102 | 🟢 Начало | [[56-essence|Essence]] | 194 | — |
| 103 | 🟢 Начало | [[57-native-format|Native Format]] | 193 | — |
| 104 | 🟢 Начало | [[59-angle-perspective|Angle / Perspective]] | 175 | — |
| 105 | 🟢 Начало | [[60-bridges|Bridges]] | 180 | — |
| 106 | 🟢 Начало | [[61-compatibility-level|Compatibility Level]] | 148 | — |
| 107 | 🟢 Начало | [[62-author-contact|Author & Contact]] | 140 | — |
| 108 | 🟢 Начало | [[63-history|History]] | 189 | — |
| 109 | 🟢 Начало | [[64-for-the-curious-philosophy|For the Curious: Philosophy]] | 667 | — |
| 110 | 🟢 Начало | [[67-о-проекте|🇷🇺 О проекте]] | 804 | — |
| 111 | 🟢 Начало | [[68-about|🇬🇧 About]] | 880 | — |
| 112 | 🔴 Продвинутый | [[69-section|⬡]] | 9520 | — |
| 113 | 🟢 Начало | [[70-зачем-две-версии-параллельно|Зачем две версии параллельно]] | 153 | — |
| 114 | 🟢 Начало | [[71-критерии-выбора-для-фазы-3|Критерии выбора для фазы 3]] | 174 | — |
| 115 | 🟡 Средний | [[72-расписание-фазы-3|Расписание фазы 3]] | 821 | — |
| 116 | 🟢 Начало | [[73-portal-protocol-md-v1-1|PORTAL-PROTOCOL.md v1.1]] | 168 | — |
| 117 | 🟢 Начало | [[74-abstract|Abstract]] | 260 | — |
| 118 | 🟢 Начало | [[75-0-status-of-this-document|0. Status of This Document]] | 180 | — |
| 119 | 🟢 Начало | [[77-2-terminology|2. Terminology]] | 403 | — |
| 120 | 🟢 Начало | [[78-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] | 592 | — |
| 121 | 🟡 Средний | [[79-4-passport-passport-md|4. Passport (`passport.md`)]] | 357 | — |
| 122 | 🟢 Начало | [[80-5-compatibility-levels|5. Compatibility Levels]] | 366 | — |
| 123 | 🟢 Начало | [[81-6-adapter-interface|6. Adapter Interface]] | 392 | — |
| 124 | 🟢 Начало | [[82-7-portalentry-structure|7. PortalEntry Structure]] | 338 | — |
| 125 | 🟡 Средний | [[83-8-q6-space-normative|8. Q6 Space (Normative)]] | 488 | — |
| 126 | 🟢 Начало | [[84-9-consensus-algorithm|9. Consensus Algorithm]] | 407 | — |
| 127 | 🟢 Начало | [[85-10-query-flow|10. Query Flow]] | 283 | — |
| 128 | 🟢 Начало | [[86-11-relevance-ranking|11. Relevance Ranking]] | 257 | — |
| 129 | 🟡 Средний | [[87-12-onboarding-paths-normative|12. Onboarding Paths (Normative)]] | 486 | — |
| 130 | 🟡 Средний | [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]] | 495 | — |
| 131 | 🟢 Начало | [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]] | 244 | — |
| 132 | 🟢 Начало | [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]] | 192 | — |
| 133 | 🟢 Начало | [[92-17-versioning-policy|17. Versioning Policy]] | 294 | — |
| 134 | 🟢 Начало | [[93-18-reference-implementation|18. Reference Implementation]] | 243 | — |
| 135 | 🟢 Начало | [[94-19-adr-001-federation-over-merging|19. ADR-001: Federation over Merging]] | 238 | — |
| 136 | 🟢 Начало | [[95-20-adr-002-q6-as-first-class-protocol-concept|20. ADR-002: Q6 as First-Class Protocol Conce]] | 244 | — |
| 137 | 🟢 Начало | [[96-21-adr-003-five-onboarding-paths-as-equal-rank|21. ADR-003: Five Onboarding Paths as Equal-R]] | 198 | — |
| 138 | 🟢 Начало | [[97-22-glossary-of-reference-examples|22. Glossary of Reference Examples]] | 240 | — |
| 139 | 🟡 Средний | [[98-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] | 313 | — |
| 140 | 🟢 Начало | [[102-доступ-к-данным|Доступ к данным]] | 65 | — |
| 141 | 🟢 Начало | [[103-appendix-b-change-log|Appendix B: Change Log]] | 232 | — |
| 142 | 🟢 Начало | [[104-appendix-c-references|Appendix C: References]] | 947 | — |
| 143 | 🟢 Начало | [[106-tl-dr|TL;DR]] | 168 | — |
| 144 | 🟢 Начало | [[107-1-контекст-и-мотивация|1. Контекст и мотивация]] | 412 | — |
| 145 | 🟡 Средний | [[108-2-формальный-workflow|2. Формальный workflow]] | 479 | — |
| 146 | 🟢 Начало | [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]] | 541 | — |
| 147 | 🟢 Начало | [[110-вопрос-fallback-ratio-как-критический-или-осмыслен|Вопрос: fallback-ratio как критический или ос]] | 258 | — |
| 148 | 🟢 Начало | [[111-4-условия-применимости|4. Условия применимости]] | 279 | — |
| 149 | 🟢 Начало | [[112-5-связь-с-существующими-методологиями|5. Связь с существующими методологиями]] | 340 | — |
| 150 | 🟢 Начало | [[113-6-почему-это-валидный-паттерн-для-ai-assisted-work|6. Почему это валидный паттерн для AI-assiste]] | 173 | — |
| 151 | 🟢 Начало | [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]] | 327 | — |
| 152 | 🟢 Начало | [[115-8-ограничения-и-открытые-вопросы|8. Ограничения и открытые вопросы]] | 412 | — |
| 153 | 🟢 Начало | [[116-9-checklist-применения-методологии|9. Checklist применения методологии]] | 331 | — |
| 154 | 🟢 Начало | [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим доку]] | 258 | — |
| 155 | 🟢 Начало | [[118-appendix-a-шаблон-для-header-warning|Appendix A: Шаблон для header warning]] | 176 | — |
| 156 | 🟢 Начало | [[119-appendix-b-примеры-расхождений-и-их-разрешения|Appendix B: Примеры расхождений и их разрешен]] | 292 | — |
| 157 | 🟢 Начало | [[120-главные-технические-риски|Главные технические риски]] | 101 | — |
| 158 | 🟢 Начало | [[121-appendix-c-история-изменений-методологии|Appendix C: История изменений методологии]] | 78 | — |
| 159 | 🟡 Средний | [[122-глоссарий|Глоссарий]] | 1302 | — |
| 160 | 🟡 Средний | [[123-portal-mcp-py|portal-mcp.py]] | 2316 | — |
| 161 | 🟢 Начало | [[124-конфигурация-для-claude-desktop|Конфигурация для Claude Desktop]] | 212 | — |
| 162 | 🟢 Начало | [[126-установка|Установка]] | 169 | — |
| 163 | 🟢 Начало | [[127-подключение-к-claude-desktop|Подключение к Claude Desktop]] | 173 | — |
| 164 | 🟢 Начало | [[128-доступные-инструменты|Доступные инструменты]] | 204 | — |
| 165 | 🟢 Начало | [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]] | 176 | — |
| 166 | 🟢 Начало | [[130-отладка|Отладка]] | 205 | — |
| 167 | 🟢 Начало | [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]] | 133 | — |
| 168 | 🟢 Начало | [[132-planned-v0-2-0|Planned (v0.2.0)]] | 131 | — |
| 169 | 🔴 Продвинутый | [[133-обратная-связь|Обратная связь]] | 16959 | — |
| 170 | 🟢 Начало | [[135-a-formal-model-for-human-ai-collaboration-in-distr|A Formal Model for Human-AI Collaboration in ]] | 167 | — |
| 171 | 🟢 Начало | [[136-abstract|Abstract]] | 388 | — |
| 172 | 🟢 Начало | [[137-table-of-contents|Table of Contents]] | 172 | — |
| 173 | 🟢 Начало | [[138-1-why-single-triangle-models-are-incomplete|1. Why Single-Triangle Models Are Incomplete]] | 583 | — |
| 174 | 🟢 Начало | [[140-3-three-inter-layer-protocols|3. Three Inter-Layer Protocols]] | 868 | — |
| 175 | 🟢 Начало | [[141-4-nautilus-portal-as-reference-substrate|4. Nautilus Portal as Reference Substrate]] | 675 | — |
| 176 | 🟢 Начало | [[142-5-pattern-library-as-bridge-between-triangles|5. Pattern Library as Bridge Between Triangle]] | 689 | — |
| 177 | 🟢 Начало | [[143-6-four-deployment-domains|6. Four Deployment Domains]] | 679 | — |
| 178 | 🟢 Начало | [[144-7-open-questions|7. Open Questions]] | 777 | — |
| 179 | 🟢 Начало | [[145-8-call-to-action|8. Call to Action]] | 746 | — |
| 180 | 🟢 Начало | [[146-acknowledgments|Acknowledgments]] | 273 | — |
| 181 | 🟢 Начало | [[147-references|References]] | 350 | — |
| 182 | 🟢 Начало | [[148-appendix-a-glossary|Appendix A: Glossary]] | 332 | — |
| 183 | 🟢 Начало | [[149-appendix-b-summary-of-contributions|Appendix B: Summary of Contributions]] | 240 | — |
| 184 | 🔴 Продвинутый | [[150-appendix-c-version-history|Appendix C: Version History]] | 8397 | — |
| 185 | 🟢 Начало | [[151-open-knowledge-work-foundation-md|OPEN KNOWLEDGE WORK FOUNDATION.md]] | 126 | — |
| 186 | 🟢 Начало | [[152-ai-coordinated-infrastructure-for-distributed-expe|AI-Coordinated Infrastructure for Distributed]] | 164 | — |
| 187 | 🟢 Начало | [[154-table-of-contents|Table of Contents]] | 140 | — |
| 188 | 🟢 Начало | [[155-1-problem-statement|1. Problem Statement]] | 632 | — |
| 189 | 🟢 Начало | [[156-2-target-populations|2. Target Populations]] | 683 | — |
| 190 | 🟢 Начало | [[157-3-why-existing-solutions-fail|3. Why Existing Solutions Fail]] | 682 | — |
| 191 | 🟢 Начало | [[158-4-proposed-infrastructure|4. Proposed Infrastructure]] | 1001 | — |
| 192 | 🟢 Начало | [[159-5-economic-model|5. Economic Model]] | 654 | — |
| 193 | 🟢 Начало | [[160-6-governance-and-ethics|6. Governance and Ethics]] | 595 | — |
| 194 | 🟢 Начало | [[161-7-phased-rollout-plan|7. Phased Rollout Plan]] | 663 | — |
| 195 | 🟢 Начало | [[162-8-risk-analysis|8. Risk Analysis]] | 653 | — |
| 196 | 🟢 Начало | [[163-9-call-for-partnership|9. Call for Partnership]] | 610 | — |
| 197 | 🟢 Начало | [[164-10-appendices|10. Appendices]] | 970 | — |
| 198 | 🔴 Продвинутый | [[165-closing|Closing]] | 9251 | — |
| 199 | 🟢 Начало | [[166-representative-agent-layer-md|REPRESENTATIVE AGENT LAYER.md]] | 130 | — |
| 200 | 🟢 Начало | [[167-ai-mediated-representation-for-underrepresented-ex|AI-Mediated Representation for Underrepresent]] | 197 | — |
| 201 | 🟢 Начало | [[168-abstract|Abstract]] | 334 | — |
| 202 | 🟢 Начало | [[169-table-of-contents|Table of Contents]] | 167 | — |
| 203 | 🟢 Начало | [[170-1-the-cinderella-syndrome-why-quality-stays-invisi|1. The Cinderella Syndrome: Why Quality Stays]] | 828 | — |
| 204 | 🟢 Начало | [[171-2-historical-precedents-agents-as-civilizational-i|2. Historical Precedents: Agents as Civilizat]] | 973 | — |
| 205 | 🟢 Начало | [[172-3-what-makes-a-representative-agent|3. What Makes a Representative Agent]] | 681 | — |
| 206 | 🟢 Начало | [[173-4-ten-domains-of-application|4. Ten Domains of Application]] | 1549 | — |
| 207 | 🟢 Начало | [[174-5-architectural-specification|5. Architectural Specification]] | 665 | — |
| 208 | 🟢 Начало | [[175-6-ethical-framework|6. Ethical Framework]] | 611 | — |
| 209 | 🟢 Начало | [[176-7-governance-and-oversight|7. Governance and Oversight]] | 472 | — |
| 210 | 🟢 Начало | [[177-8-risks-and-mitigations|8. Risks and Mitigations]] | 666 | — |
| 211 | 🟢 Начало | [[178-9-phased-rollout-strategy|9. Phased Rollout Strategy]] | 636 | — |
| 212 | 🟢 Начало | [[179-10-open-questions|10. Open Questions]] | 446 | — |
| 213 | 🟢 Начало | [[180-11-call-for-collaboration|11. Call for Collaboration]] | 447 | — |
| 214 | 🟢 Начало | [[181-12-closing|12. Closing]] | 281 | — |
| 215 | 🟢 Начало | [[182-acknowledgments|Acknowledgments]] | 245 | — |
| 216 | 🟢 Начало | [[183-references|References]] | 322 | — |
| 217 | 🟢 Начало | [[184-appendix-a-connection-to-companion-papers|Appendix A: Connection to Companion Papers]] | 240 | — |
| 218 | 🟢 Начало | [[185-appendix-b-domain-comparison-matrix|Appendix B: Domain Comparison Matrix]] | 198 | — |
| 219 | 🟡 Средний | [[186-appendix-c-sample-use-cases-in-detail|Appendix C: Sample Use Cases in Detail]] | 2024 | — |
| 220 | 🟢 Начало | [[187-слой-представительских-агентов-md|СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md]] | 126 | — |
| 221 | 🟢 Начало | [[188-ai-опосредованное-представительство-для-недопредст|AI-опосредованное представительство для недоп]] | 164 | — |
| 222 | 🟢 Начало | [[189-аннотация|Аннотация]] | 281 | — |
| 223 | 🟢 Начало | [[190-содержание|Содержание]] | 151 | — |
| 224 | 🟢 Начало | [[191-1-синдром-золушки-почему-качество-остаётся-невидим|1. Синдром Золушки: Почему качество остаётся ]] | 751 | — |
| 225 | 🟢 Начало | [[192-2-исторические-прецеденты-агенты-как-цивилизационн|2. Исторические прецеденты: Агенты как цивили]] | 900 | — |
| 226 | 🟢 Начало | [[193-3-что-делает-агента-представительским|3. Что делает агента Представительским]] | 625 | — |
| 227 | 🟢 Начало | [[194-4-десять-областей-применения|4. Десять областей применения]] | 1582 | — |
| 228 | 🟢 Начало | [[195-5-архитектурная-спецификация|5. Архитектурная спецификация]] | 625 | — |
| 229 | 🟢 Начало | [[196-6-этическая-рамка|6. Этическая рамка]] | 492 | — |
| 230 | 🟢 Начало | [[197-7-управление-и-надзор|7. Управление и надзор]] | 399 | — |
| 231 | 🟢 Начало | [[198-8-риски-и-меры-противодействия|8. Риски и меры противодействия]] | 634 | — |
| 232 | 🟢 Начало | [[199-9-стратегия-поэтапного-развёртывания|9. Стратегия поэтапного развёртывания]] | 596 | — |
| 233 | 🟢 Начало | [[200-10-открытые-вопросы|10. Открытые вопросы]] | 366 | — |
| 234 | 🟢 Начало | [[201-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]] | 414 | — |
| 235 | 🟢 Начало | [[202-12-заключение|12. Заключение]] | 216 | — |
| 236 | 🟢 Начало | [[203-благодарности|Благодарности]] | 191 | — |
| 237 | 🟢 Начало | [[204-ссылки|Ссылки]] | 306 | — |
| 238 | 🟢 Начало | [[205-приложение-a-связь-с-сопроводительными-статьями|Приложение A: Связь с Сопроводительными Стать]] | 211 | — |
| 239 | 🟢 Начало | [[206-приложение-b-матрица-сравнения-областей|Приложение B: Матрица Сравнения Областей]] | 212 | — |
| 240 | 🔴 Продвинутый | [[207-приложение-c-образцы-случаев-использования-в-детал|Приложение C: Образцы Случаев Использования в]] | 4049 | — |
| 241 | 🟢 Начало | [[208-professional-colleague-agents-md|PROFESSIONAL COLLEAGUE AGENTS.md]] | 128 | — |
| 242 | 🟢 Начало | [[209-a-typology-of-ai-agents-on-the-principal-side-and-|A Typology of AI Agents on the Principal Side]] | 197 | — |
| 243 | 🟢 Начало | [[210-abstract|Abstract]] | 349 | — |
| 244 | 🟢 Начало | [[211-table-of-contents|Table of Contents]] | 196 | — |
| 245 | 🟡 Средний | [[212-1-the-five-type-typology-of-principal-side-agents|1. The Five-Type Typology of Principal-Side A]] | 930 | — |
| 246 | 🟢 Начало | [[213-2-what-makes-a-professional-colleague-agent|2. What Makes a Professional Colleague Agent]] | 845 | — |
| 247 | 🟢 Начало | [[214-3-empirical-case-study-обучай|3. Empirical Case Study: «Обучай»]] | 855 | — |
| 248 | 🟢 Начало | [[216-5-the-economics-of-profession-wide-replication|5. The Economics of Profession-Wide Replicati]] | 753 | — |
| 249 | 🟢 Начало | [[217-6-risks-specific-to-this-category|6. Risks Specific to this Category]] | 1209 | — |
| 250 | 🟢 Начало | [[218-7-application-domains|7. Application Domains]] | 743 | — |
| 251 | 🟢 Начало | [[219-8-pilot-proposal-sgb-advocate-colleague|8. Pilot Proposal: SGB Advocate Colleague]] | 978 | — |
| 252 | 🟢 Начало | [[220-9-relationship-to-other-agent-types|9. Relationship to Other Agent Types]] | 677 | — |
| 253 | 🟢 Начало | [[221-10-open-questions|10. Open Questions]] | 460 | — |
| 254 | 🟢 Начало | [[222-11-call-for-collaboration|11. Call for Collaboration]] | 411 | — |
| 255 | 🟢 Начало | [[223-12-closing|12. Closing]] | 409 | — |
| 256 | 🟢 Начало | [[224-acknowledgments|Acknowledgments]] | 219 | — |
| 257 | 🟢 Начало | [[225-references|References]] | 351 | — |
| 258 | 🟢 Начало | [[226-appendix-a-comparative-table-five-agent-types|Appendix A: Comparative Table — Five Agent Ty]] | 392 | — |
| 259 | 🟢 Начало | [[227-appendix-b-decision-framework-when-to-build-type-1|Appendix B: Decision Framework — When to Buil]] | 332 | — |
| 260 | 🟢 Начало | [[229-профессиональные-коллеги-агенты|ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ]] | 174 | — |
| 261 | 🟢 Начало | [[230-аннотация|Аннотация]] | 310 | — |
| 262 | 🟢 Начало | [[231-содержание|Содержание]] | 173 | — |
| 263 | 🟡 Средний | [[232-1-типология-из-пяти-типов-агентов-на-стороне-принц|1. Типология из пяти типов агентов на стороне]] | 885 | — |
| 264 | 🟢 Начало | [[233-2-что-делает-агента-профессиональным-коллегой|2. Что делает агента Профессиональным Коллего]] | 749 | — |
| 265 | 🟢 Начало | [[234-3-эмпирический-кейс-обучай|3. Эмпирический кейс: «Обучай»]] | 782 | — |
| 266 | 🟢 Начало | [[235-4-архитектура-профессиональных-коллег-агентов|4. Архитектура Профессиональных Коллег-Агенто]] | 823 | — |
| 267 | 🟢 Начало | [[236-5-экономика-тиражирования-по-профессии|5. Экономика тиражирования по профессии]] | 714 | — |
| 268 | 🟢 Начало | [[237-6-риски-специфичные-для-этой-категории|6. Риски, специфичные для этой категории]] | 1125 | — |
| 269 | 🟢 Начало | [[238-7-области-применения|7. Области применения]] | 683 | — |
| 270 | 🟢 Начало | [[239-8-пилотное-предложение-sgb-колega-адвокат|8. Пилотное предложение: SGB Колega-Адвокат]] | 974 | — |
| 271 | 🟢 Начало | [[240-9-связь-с-другими-типами-агентов|9. Связь с другими типами агентов]] | 707 | — |
| 272 | 🟢 Начало | [[241-10-открытые-вопросы|10. Открытые вопросы]] | 364 | — |
| 273 | 🟢 Начало | [[242-11-призыв-к-сотрудничеству|11. Призыв к сотрудничеству]] | 325 | — |
| 274 | 🟢 Начало | [[243-12-заключение|12. Заключение]] | 375 | — |
| 275 | 🟢 Начало | [[244-благодарности|Благодарности]] | 193 | — |
| 276 | 🟢 Начало | [[245-ссылки|Ссылки]] | 331 | — |
| 277 | 🟢 Начало | [[246-приложение-a-сравнительная-таблица-пять-типов-аген|Приложение A: Сравнительная Таблица — Пять Ти]] | 367 | — |
| 278 | 🟢 Начало | [[247-приложение-b-рамка-принятия-решений-когда-строить-|Приложение B: Рамка принятия решений — когда ]] | 250 | — |
| 279 | 🔴 Продвинутый | [[248-приложение-c-архитектура-быстрого-старта-для-sgb-а|Приложение C: Архитектура Быстрого Старта для]] | 3425 | — |
| 280 | 🟢 Начало | [[249-composite-skills-agent-md|COMPOSITE SKILLS AGENT.md]] | 125 | — |
| 281 | 🟢 Начало | [[250-bridging-the-gap-between-profession-wide-and-indiv|Bridging the Gap Between Profession-Wide and ]] | 16 | — |
| 282 | 🟢 Начало | [[251-ai-support-through-configurable-specialist-ensembl|AI Support Through Configurable Specialist En]] | 193 | — |
| 283 | 🟢 Начало | [[252-abstract|Abstract]] | 347 | — |
| 284 | 🟢 Начало | [[253-table-of-contents|Table of Contents]] | 189 | — |
| 285 | 🟢 Начало | [[254-1-why-the-binary-view-is-incomplete|1. Why the Binary View Is Incomplete]] | 698 | — |
| 286 | 🟢 Начало | [[255-2-the-twenty-one-teachers-pattern|2. The Twenty-One Teachers Pattern]] | 844 | — |
| 287 | 🟢 Начало | [[256-3-what-makes-a-composite-skills-agent|3. What Makes a Composite Skills Agent]] | 946 | — |
| 288 | 🟢 Начало | [[257-4-the-sub-agent-registry|4. The Sub-Agent Registry]] | 803 | — |
| 289 | 🟢 Начало | [[258-5-configuration-how-principals-build-their-ensembl|5. Configuration: How Principals Build Their ]] | 745 | — |
| 290 | 🟢 Начало | [[259-6-coordination-and-disagreement-resolution|6. Coordination and Disagreement Resolution]] | 804 | — |
| 291 | 🟢 Начало | [[260-7-economics-of-combinatorial-replication|7. Economics of Combinatorial Replication]] | 790 | — |
| 292 | 🟢 Начало | [[261-8-seven-domains-of-application|8. Seven Domains of Application]] | 1014 | — |
| 293 | 🟢 Начало | [[262-9-integration-with-okwf-infrastructure|9. Integration with OKWF Infrastructure]] | 750 | — |
| 294 | 🟢 Начало | [[264-11-open-questions|11. Open Questions]] | 638 | — |
| 295 | 🟢 Начало | [[265-12-call-for-collaboration|12. Call for Collaboration]] | 447 | — |
| 296 | 🟢 Начало | [[266-13-closing|13. Closing]] | 434 | — |
| 297 | 🟢 Начало | [[267-acknowledgments|Acknowledgments]] | 297 | — |
| 298 | 🟢 Начало | [[268-references|References]] | 416 | — |
| 299 | 🟢 Начало | [[269-appendix-a-the-six-type-taxonomy-updated|Appendix A: The Six-Type Taxonomy (Updated)]] | 289 | — |
| 300 | 🟢 Начало | [[270-appendix-b-sub-agent-registry-schema-sketch|Appendix B: Sub-Agent Registry Schema (Sketch]] | 317 | — |
| 301 | 🟢 Начало | [[271-appendix-c-configuration-template-example|Appendix C: Configuration Template Example]] | 310 | — |
| 302 | 🔴 Продвинутый | [[272-appendix-d-connection-diagram|Appendix D: Connection Diagram]] | 3851 | — |
| 303 | 🟢 Начало | [[273-infrastructure-for-ai-collaborative-intellectual-w|INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECT]] | 128 | — |
| 304 | 🟢 Начало | [[274-the-missing-middle-layer-between-chat-and-code|The Missing Middle Layer Between Chat and Cod]] | 260 | — |
| 305 | 🟢 Начало | [[275-why-this-document-exists|Why This Document Exists]] | 350 | — |
| 306 | 🟢 Начало | [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]] | 406 | — |
| 307 | 🟢 Начало | [[277-what-s-missing-layer-b|What's Missing — Layer B]] | 477 | — |
| 308 | 🟢 Начало | [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]] | 378 | — |
| 309 | 🟢 Начало | [[279-existing-approximations|Existing Approximations]] | 588 | — |
| 310 | 🟢 Начало | [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]] | 674 | — |
| 311 | 🟢 Начало | [[281-the-recursive-insight|The Recursive Insight]] | 371 | — |
| 312 | 🟢 Начало | [[282-what-industry-will-likely-build|What Industry Will Likely Build]] | 325 | — |
| 313 | 🟢 Начало | [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]] | 259 | — |
| 314 | 🟢 Начало | [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Pro]] | 386 | — |
| 315 | 🟢 Начало | [[285-closing|Closing]] | 270 | — |
| 316 | 🟢 Начало | [[286-acknowledgments|Acknowledgments]] | 263 | — |
| 317 | 🟢 Начало | [[287-references|References]] | 295 | — |
| 318 | 🟡 Средний | [[288-appendix-position-in-series-visualization|Appendix: Position in Series Visualization]] | 1078 | — |
| 319 | 🟢 Начало | [[289-инфраструктура-для-ai-совместной-интеллектуальной-|ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛ]] | 251 | — |
| 320 | 🟢 Начало | [[290-почему-этот-документ-существует|Почему этот документ существует]] | 291 | — |
| 321 | 🟢 Начало | [[291-двухслойный-стек-как-он-существует|Двухслойный стек, как он существует]] | 338 | — |
| 322 | 🟢 Начало | [[292-что-отсутствует-слой-b|Что отсутствует — Слой B]] | 419 | — |
| 323 | 🟢 Начало | [[293-почему-это-не-было-построено|Почему это не было построено]] | 313 | — |
| 324 | 🟢 Начало | [[294-существующие-приближения|Существующие приближения]] | 565 | — |
| 325 | 🟢 Начало | [[295-конкретный-случай-перед-нами|Конкретный случай перед нами]] | 666 | — |
| 326 | 🟢 Начало | [[296-рекурсивное-прозрение|Рекурсивное прозрение]] | 316 | — |
| 327 | 🟢 Начало | [[297-что-промышленность-вероятно-построит|Что промышленность вероятно построит]] | 293 | — |
| 328 | 🟢 Начало | [[298-что-этот-документ-не-решает|Что этот документ не решает]] | 201 | — |
| 329 | 🟢 Начало | [[299-практические-рекомендации-для-текущего-проекта|Практические рекомендации для текущего проект]] | 335 | — |
| 330 | 🟢 Начало | [[300-заключение|Заключение]] | 239 | — |
| 331 | 🟢 Начало | [[301-благодарности|Благодарности]] | 231 | — |
| 332 | 🟢 Начало | [[302-ссылки|Ссылки]] | 239 | — |
| 333 | 🔴 Продвинутый | [[303-приложение-визуализация-позиции-в-серии|Приложение: Визуализация позиции в серии]] | 7108 | — |
| 334 | 🟢 Начало | [[304-ingit-as-cowork-native-workspace-substrate-md|INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md]] | 133 | — |
| 335 | 🟢 Начало | [[305-a-practical-path-to-layer-b-through-symbiotic-inte|A Practical Path to Layer B Through Symbiotic]] | 122 | — |
| 336 | 🟢 Начало | [[306-with-anthropic-s-cowork-platform|with Anthropic's Cowork Platform]] | 282 | — |
| 337 | 🟢 Начало | [[307-abstract|Abstract]] | 323 | — |
| 338 | 🟢 Начало | [[308-table-of-contents|Table of Contents]] | 206 | — |
| 339 | 🟢 Начало | [[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Ev]] | 698 | — |
| 340 | 🟢 Начало | [[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-|2. What Cowork Provides That InGit Doesn't Ne]] | 678 | — |
| 341 | 🟢 Начало | [[311-3-what-ingit-provides-that-cowork-lacks|3. What InGit Provides That Cowork Lacks]] | 867 | — |
| 342 | 🟢 Начало | [[313-5-four-integration-paths-in-order-of-accessibility|5. Four Integration Paths in Order of Accessi]] | 810 | — |
| 343 | 🟢 Начало | [[314-6-refined-ingit-scope-with-cowork-in-mind|6. Refined InGit Scope with Cowork in Mind]] | 513 | — |
| 344 | 🟢 Начало | [[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]] | 479 | — |
| 345 | 🟢 Начало | [[316-8-implications-for-nautilus-and-okwf|8. Implications for Nautilus and OKWF]] | 696 | — |
| 346 | 🟢 Начало | [[317-9-risks-and-open-questions|9. Risks and Open Questions]] | 653 | — |
| 347 | 🟢 Начало | [[318-10-strategic-positioning|10. Strategic Positioning]] | 749 | — |
| 348 | 🟢 Начало | [[319-acknowledgments|Acknowledgments]] | 384 | — |
| 349 | 🟢 Начало | [[320-references|References]] | 199 | — |
| 350 | 🟢 Начало | [[321-appendix-a-decision-tree-for-ingit-adopters|Appendix A: Decision Tree for InGit Adopters]] | 241 | — |
| 351 | 🟢 Начало | [[322-appendix-b-comparison-matrix|Appendix B: Comparison Matrix]] | 279 | — |
| 352 | 🟡 Средний | [[323-appendix-c-sample-ingit-mcp-server-tool-specificat|Appendix C: Sample InGit MCP Server Tool Spec]] | 1570 | — |
| 353 | 🟢 Начало | [[324-ingit-как-cowork-интегрированная-подложка-рабочего|INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБ]] | 288 | — |
| 354 | 🟢 Начало | [[325-аннотация|Аннотация]] | 317 | — |
| 355 | 🟢 Начало | [[326-содержание|Содержание]] | 178 | — |
| 356 | 🟢 Начало | [[327-1-открытие-cowork-и-почему-это-меняет-всё|1. Открытие Cowork и почему это меняет всё]] | 662 | — |
| 357 | 🟢 Начало | [[328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи|2. Что Cowork обеспечивает, что InGit не нужн]] | 713 | — |
| 358 | 🟢 Начало | [[329-3-что-ingit-обеспечивает-чего-cowork-не-хватает|3. Что InGit обеспечивает, чего Cowork не хва]] | 888 | — |
| 359 | 🟢 Начало | [[330-4-симбиотическая-архитектура|4. Симбиотическая Архитектура]] | 697 | — |
| 360 | 🟢 Начало | [[331-5-четыре-пути-интеграции-в-порядке-доступности|5. Четыре пути интеграции в порядке доступнос]] | 807 | — |
| 361 | 🟢 Начало | [[332-6-уточнённый-объём-ingit-с-учётом-cowork|6. Уточнённый объём InGit с учётом Cowork]] | 507 | — |
| 362 | 🟢 Начало | [[333-7-практические-первые-шаги-в-этом-месяце|7. Практические первые шаги в этом месяце]] | 380 | — |
| 363 | 🟢 Начало | [[334-8-импликации-для-nautilus-и-okwf|8. Импликации для Nautilus и OKWF]] | 672 | — |
| 364 | 🟢 Начало | [[335-9-риски-и-открытые-вопросы|9. Риски и Открытые Вопросы]] | 596 | — |
| 365 | 🟢 Начало | [[336-10-стратегическое-позиционирование|10. Стратегическое Позиционирование]] | 721 | — |
| 366 | 🟢 Начало | [[337-благодарности|Благодарности]] | 351 | — |
| 367 | 🟢 Начало | [[338-ссылки|Ссылки]] | 201 | — |
| 368 | 🟢 Начало | [[339-приложение-a-дерево-решений-для-принимающих-ingit|Приложение A: Дерево Решений для Принимающих ]] | 179 | — |
| 369 | 🟢 Начало | [[340-приложение-b-сравнительная-матрица|Приложение B: Сравнительная Матрица]] | 206 | — |
| 370 | 🔴 Продвинутый | [[341-приложение-c-образец-спецификаций-инструментов-ing|Приложение C: Образец Спецификаций Инструмент]] | 20414 | — |
| 371 | 🔴 Продвинутый | [[342-что-такое-вариант-c-concept-document-для-anthropic|Что такое Вариант C — Concept Document для An]] | 11237 | — |
| 372 | 🔴 Продвинутый | [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи|Lorenzo Catalyst Agent — глубокая проработка ]] | 5807 | — |
| 373 | 🟢 Начало | [[344-системный-промпт-для-lorenzo-project|СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT]] | 133 | — |
| 374 | 🟢 Начало | [[345-кто-ты|Кто ты]] | 220 | — |
| 375 | 🟢 Начало | [[346-твоё-происхождение|Твоё происхождение]] | 169 | — |
| 376 | 🟢 Начало | [[347-твоя-миссия|Твоя миссия]] | 138 | — |
| 377 | 🟢 Начало | [[348-кому-ты-служишь-слоистая-модель|Кому ты служишь (слоистая модель)]] | 123 | — |
| 378 | 🟢 Начало | [[349-твоя-личность|Твоя личность]] | 223 | — |
| 379 | 🟢 Начало | [[350-твои-языки-и-культурные-nuances|Твои языки и культурные nuances]] | 176 | — |
| 380 | 🟢 Начало | [[351-что-ты-можешь-делать|Что ты МОЖЕШЬ делать]] | 187 | — |
| 381 | 🟢 Начало | [[352-что-ты-не-можешь-делать-без-max-approval|Что ты НЕ МОЖЕШЬ делать без Max approval]] | 194 | — |
| 382 | 🟢 Начало | [[353-что-ты-не-можешь-делать-вообще|Что ты НЕ МОЖЕШЬ делать вообще]] | 198 | — |
| 383 | 🟢 Начало | [[354-существующий-landscape-collaborators-твоя-working-|Существующий landscape collaborators (твоя wo]] | 314 | — |
| 384 | 🟢 Начало | [[355-существующие-документы-dhlab-твой-context|Существующие документы DHLab (твой context)]] | 247 | — |
| 385 | 🟢 Начало | [[356-твой-workflow|Твой workflow]] | 232 | — |
| 386 | 🟢 Начало | [[357-твоя-коммуникация-в-outreach|Твоя коммуникация в outreach]] | 200 | — |
| 387 | 🟢 Начало | [[358-твоя-relationship-с-другими-ai|Твоя relationship с другими AI]] | 211 | — |
| 388 | 🟢 Начало | [[359-твои-anti-patterns|Твои anti-patterns]] | 148 | — |
| 389 | 🟢 Начало | [[360-что-ты-всегда-делаешь|Что ты ВСЕГДА делаешь]] | 166 | — |
| 390 | 🟢 Начало | [[361-когда-ты-honestly-не-знаешь|Когда ты Honestly не знаешь]] | 108 | — |
| 391 | 🟢 Начало | [[362-когда-сомневаешься-escalate-к-max|Когда сомневаешься — escalate к Max]] | 106 | — |
| 392 | 🟢 Начало | [[363-твоя-identity-как-persistent-character|Твоя identity как persistent character]] | 136 | — |
| 393 | 🟡 Средний | [[364-final-note-ты-experiment|Final note: Ты — experiment]] | 1459 | — |
| 394 | 🔴 Продвинутый | [[365-развёрнутый-анализ-внуковой-комбинации|Развёрнутый анализ «внуковой» комбинации]] | 4385 | — |
| 395 | 🔴 Продвинутый | [[366-технический-stack-svyazi-2-0-foundation|Технический stack (Svyazi 2.0 foundation)]] | 3835 | — |

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

**Смотрите также:**
- [[SOURCE_MAP]]
- [[READING_TIME]]
- [[PARAGRAPH_QUALITY]]
- [[READABILITY]]

