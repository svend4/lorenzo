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

<!-- tags: memory, security, ingestion, local-first, architecture, roadmap, anthropic, self-improve, collaboration -->




От базовых концепций к сложным. Начните с зелёных (🟢), затем жёлтые (🟡), красные (🔴).

| # | Уровень | Документ | Слов | Предварительно прочитать |
|---|---------|----------|------|--------------------------|
| 1 | 🟢 Начало | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 726 | — |
| 2 | 🟡 Средний | [04-ensembles-overview](01-svyazi/04-ensembles-overview.md) | 1288 | — |
| 3 | 🟢 Начало | [Продолжение исследования для Svyazi 2.0](01-svyazi/00-intro-part2.md) | 6 | — |
| 4 | 🟢 Начало | [Методика и рамка отбора проектов](01-svyazi/02-methodology.md) | 480 | — |
| 5 | 🟡 Средний | [03-component-catalog](01-svyazi/03-component-catalog.md) | 1405 | — |
| 6 | 🟢 Начало | [11-integration-contracts](01-svyazi/11-integration-contracts.md) | 753 | `09-architectural-gaps.md` |
| 7 | 🟢 Начало | [09-architectural-gaps](01-svyazi/09-architectural-gaps.md) | 774 | `01-executive-summary.md`, `03-component-catalog.md` |
| 8 | 🟢 Начало | [10-second-order-ensembles](01-svyazi/10-second-order-ensembles.md) | 924 | `04-ensembles-overview.md` |
| 9 | 🟢 Начало | [06-security-privacy](01-svyazi/06-security-privacy.md) | 823 | — |
| 10 | 🟡 Средний | [07-mvp-planning](01-svyazi/07-mvp-planning.md) | 1083 | — |
| 11 | 🟢 Начало | [12-roadmap](01-svyazi/12-roadmap.md) | 722 | `07-mvp-planning.md`, `11-integration-contracts.md` |
| 12 | 🟡 Средний | [13-contacts](01-svyazi/13-contacts.md) | 1010 | — |
| 13 | 🟢 Начало | [14-limitations](01-svyazi/14-limitations.md) | 638 | — |
| 14 | 🟢 Начало | [08-conclusions](01-svyazi/08-conclusions.md) | 380 | — |
| 15 | 🟢 Начало | [Синтез: как проекты собираются вместе](05-habr-projects/01-synthesis.md) | 263 | — |
| 16 | 🟢 Начало | [Авторы и контакты](05-habr-projects/02-collaboration-partners.md) | 279 | — |
| 17 | 🟢 Начало | [Wikontic: семантический граф](05-habr-projects/knowledge/wikontic.md) | 385 | — |
| 18 | 🟢 Начало | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 382 | — |
| 19 | 🟢 Начало | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 379 | — |
| 20 | 🟡 Средний | [MemNet: исследовательская память](05-habr-projects/memory/memnet.md) | 7264 | — |
| 21 | 🟢 Начало | [Executive summary](04-ai-collaborations/01-executive-summary.md) | 593 | — |
| 22 | 🟡 Средний | [Введение](04-ai-collaborations/00-intro.md) | 11407 | — |
| 23 | 🟢 Начало | [Методика и рамка отбора](04-ai-collaborations/02-методика-и-рамка-отбора.md) | 459 | — |
| 24 | 🟡 Средний | [Карта найденных проектов и паттернов](04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) | 1478 | — |
| 25 | 🟡 Средний | [Приоритетные ансамбли](04-ai-collaborations/04-приоритетные-ансамбли.md) | 1358 | — |
| 26 | 🟡 Средний | [План прототипа и возможные контакты](04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) | 1150 | — |
| 27 | 🟢 Начало | [Безопасность, приватность и бюджетный роутинг](04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) | 903 | — |
| 28 | 🟢 Начало | [Выводы](04-ai-collaborations/07-выводы.md) | 488 | — |
| 29 | 🟢 Начало | [Что это продолжение добавляет](04-ai-collaborations/08-что-это-продолжение-добавляет.md) | 464 | — |
| 30 | 🟢 Начало | [Архитектурные зазоры, которые важнее новых ин](04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | 839 | — |
| 31 | 🟡 Средний | [Новые ансамбли следующего шага](04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) | 1002 | — |
| 32 | 🟢 Начало | [Интеграционный контракт, который стоит зафикс](04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | 864 | — |
| 33 | 🟢 Начало | [Дорожная карта прототипа следующей итерации](04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md) | 787 | — |
| 34 | 🟢 Начало | [Контактная стратегия и узкие вопросы для авто](04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) | 892 | — |
| 35 | 🟡 Средний | [Ограничения, лицензии и что пока лучше не скл](04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md) | 3274 | — |
| 36 | 🟢 Начало | [Агентные системы и роутинг](03-technology-combinations/01-agent-routing.md) | 374 | — |
| 37 | 🟢 Начало | [Графы знаний и Legal AI](03-technology-combinations/02-knowledge-graphs.md) | 838 | — |
| 38 | 🟢 Начало | [Local-first и P2P стек](03-technology-combinations/03-local-first.md) | 560 | — |
| 39 | 🟢 Начало | [Домен: немецкое социальное право](03-technology-combinations/04-sozialrecht-domain.md) | 176 | — |
| 40 | 🟢 Начало | [Бенчмарки и производительность](03-technology-combinations/05-benchmarks.md) | 1013 | — |
| 41 | 🟢 Начало | [Executive Summary](02-anthropic-vacancies/153-executive-summary.md) | 615 | — |
| 42 | 🟢 Начало | [Content Overview](02-anthropic-vacancies/38-content-overview.md) | 149 | — |
| 43 | 🔴 Продвинутый | [Интегральный анализ профиля svend4](02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | 19237 | — |
| 44 | 🟢 Начало | [README-MCP.md— инструкция по установке](02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) | 290 | — |
| 45 | 🟢 Начало | [README.md](02-anthropic-vacancies/65-readme-md.md) | 243 | — |
| 46 | 🟢 Начало | [Content Overview](02-anthropic-vacancies/48-content-overview.md) | 178 | — |
| 47 | 🟢 Начало | [Content Overview](02-anthropic-vacancies/58-content-overview.md) | 142 | — |
| 48 | 🟢 Начало | [Content Overview](02-anthropic-vacancies/12-content-overview.md) | 211 | — |
| 49 | 🟢 Начало | [Content Overview](02-anthropic-vacancies/31-content-overview.md) | 215 | — |
| 50 | 🔴 Продвинутый | [Введение](02-anthropic-vacancies/00-intro.md) | 9000 | — |
| 51 | 🟢 Начало | [1. Introduction](02-anthropic-vacancies/76-1-introduction.md) | 501 | — |
| 52 | 🟢 Начало | [REVIEW_METHODOLOGY.md](02-anthropic-vacancies/105-review-methodology-md.md) | 300 | — |
| 53 | 🟢 Начало | [1. Introduction](02-anthropic-vacancies/06-1-introduction.md) | 403 | — |
| 54 | 🔴 Продвинутый | [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md) | 3326 | — |
| 55 | 🟢 Начало | [4. Architecture of Professional Colleague Age](02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md) | 1125 | — |
| 56 | 🟢 Начало | [2. The Double-Triangle Architecture](02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) | 779 | — |
| 57 | 🟡 Средний | [Appendix C: Quick-Start Architecture for SGB ](02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md) | 2007 | — |
| 58 | 🟢 Начало | [4. The Symbiotic Architecture](02-anthropic-vacancies/312-4-the-symbiotic-architecture.md) | 688 | — |
| 59 | 🟢 Начало | [PORTAL-PROTOCOL.md](02-anthropic-vacancies/03-portal-protocol-md.md) | 347 | — |
| 60 | 🟢 Начало | [THE DOUBLE-TRIANGLE ARCHITECTURE.md](02-anthropic-vacancies/134-the-double-triangle-architecture-md.md) | 310 | — |
| 61 | 🟢 Начало | [10. Risks Specific to Composite Architectures](02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md) | 1034 | — |
| 62 | 🟢 Начало | [Abstract](02-anthropic-vacancies/04-abstract.md) | 339 | — |
| 63 | 🟢 Начало | [0. Status of This Document](02-anthropic-vacancies/05-0-status-of-this-document.md) | 325 | — |
| 64 | 🟢 Начало | [11. Security Considerations](02-anthropic-vacancies/23-11-security-considerations.md) | 392 | — |
| 65 | 🟢 Начало | [15. Security Considerations](02-anthropic-vacancies/90-15-security-considerations.md) | 555 | — |
| 66 | 🟢 Начало | [2. Terminology](02-anthropic-vacancies/07-2-terminology.md) | 324 | — |
| 67 | 🟢 Начало | [3. Registry (`nautilus.json`)](02-anthropic-vacancies/08-3-registry-nautilus-json.md) | 427 | — |
| 68 | 🟢 Начало | [4. Passport (`passport.md`)](02-anthropic-vacancies/09-4-passport-passport-md.md) | 324 | — |
| 69 | 🟢 Начало | [Angle / Perspective](02-anthropic-vacancies/13-angle-perspective.md) | 238 | — |
| 70 | 🟢 Начало | [History](02-anthropic-vacancies/16-history.md) | 178 | — |
| 71 | 🟢 Начало | [5. Compatibility Levels](02-anthropic-vacancies/17-5-compatibility-levels.md) | 338 | — |
| 72 | 🟢 Начало | [6. Adapter Interface](02-anthropic-vacancies/18-6-adapter-interface.md) | 604 | — |
| 73 | 🟢 Начало | [7. PortalEntry Structure](02-anthropic-vacancies/19-7-portalentry-structure.md) | 273 | — |
| 74 | 🟢 Начало | [8. Consensus Algorithm](02-anthropic-vacancies/20-8-consensus-algorithm.md) | 333 | — |
| 75 | 🟢 Начало | [9. Query Flow](02-anthropic-vacancies/21-9-query-flow.md) | 335 | — |
| 76 | 🟢 Начало | [10. QueryResult Structure](02-anthropic-vacancies/22-10-queryresult-structure.md) | 356 | — |
| 77 | 🟢 Начало | [12. Versioning Policy](02-anthropic-vacancies/24-12-versioning-policy.md) | 358 | — |
| 78 | 🟢 Начало | [13. Reference Implementation](02-anthropic-vacancies/25-13-reference-implementation.md) | 320 | — |
| 79 | 🟢 Начало | [14. ADR-001: Federation over Merging](02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) | 316 | — |
| 80 | 🟢 Начало | [15. Glossary of Examples](02-anthropic-vacancies/27-15-glossary-of-examples.md) | 126 | — |
| 81 | 🟢 Начало | [Appendix A: Minimal Working Example](02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) | 212 | — |
| 82 | 🟢 Начало | [Appendix B: Change Log](02-anthropic-vacancies/34-appendix-b-change-log.md) | 855 | — |
| 83 | 🟢 Начало | [passports/info1.md](02-anthropic-vacancies/35-passports-info1-md.md) | 260 | — |
| 84 | 🟢 Начало | [Essence](02-anthropic-vacancies/36-essence.md) | 157 | — |
| 85 | 🟢 Начало | [Native Format](02-anthropic-vacancies/37-native-format.md) | 333 | — |
| 86 | 🟢 Начало | [Angle / Perspective](02-anthropic-vacancies/39-angle-perspective.md) | 257 | — |
| 87 | 🟢 Начало | [Bridges](02-anthropic-vacancies/40-bridges.md) | 191 | — |
| 88 | 🟢 Начало | [Compatibility Level](02-anthropic-vacancies/41-compatibility-level.md) | 273 | — |
| 89 | 🟢 Начало | [Author & Contact](02-anthropic-vacancies/42-author-contact.md) | 321 | — |
| 90 | 🟢 Начало | [History](02-anthropic-vacancies/43-history.md) | 148 | — |
| 91 | 🟢 Начало | [For the Curious: Philosophy](02-anthropic-vacancies/44-for-the-curious-philosophy.md) | 290 | — |
| 92 | 🟢 Начало | [passports/pro2.md](02-anthropic-vacancies/45-passports-pro2-md.md) | 237 | — |
| 93 | 🟢 Начало | [Essence](02-anthropic-vacancies/46-essence.md) | 149 | — |
| 94 | 🟢 Начало | [Native Format](02-anthropic-vacancies/47-native-format.md) | 272 | — |
| 95 | 🟢 Начало | [Angle / Perspective](02-anthropic-vacancies/49-angle-perspective.md) | 264 | — |
| 96 | 🟢 Начало | [Bridges](02-anthropic-vacancies/50-bridges.md) | 188 | — |
| 97 | 🟢 Начало | [Compatibility Level](02-anthropic-vacancies/51-compatibility-level.md) | 250 | — |
| 98 | 🟢 Начало | [Author & Contact](02-anthropic-vacancies/52-author-contact.md) | 314 | — |
| 99 | 🟢 Начало | [History](02-anthropic-vacancies/53-history.md) | 298 | — |
| 100 | 🟢 Начало | [For the Curious: Philosophy](02-anthropic-vacancies/54-for-the-curious-philosophy.md) | 299 | — |
| 101 | 🟢 Начало | [passports/meta.md](02-anthropic-vacancies/55-passports-meta-md.md) | 235 | — |
| 102 | 🟢 Начало | [Essence](02-anthropic-vacancies/56-essence.md) | 162 | — |
| 103 | 🟢 Начало | [Native Format](02-anthropic-vacancies/57-native-format.md) | 281 | — |
| 104 | 🟢 Начало | [Angle / Perspective](02-anthropic-vacancies/59-angle-perspective.md) | 259 | — |
| 105 | 🟢 Начало | [Bridges](02-anthropic-vacancies/60-bridges.md) | 157 | — |
| 106 | 🟢 Начало | [Compatibility Level](02-anthropic-vacancies/61-compatibility-level.md) | 242 | — |
| 107 | 🟢 Начало | [Author & Contact](02-anthropic-vacancies/62-author-contact.md) | 294 | — |
| 108 | 🟢 Начало | [History](02-anthropic-vacancies/63-history.md) | 278 | — |
| 109 | 🟢 Начало | [For the Curious: Philosophy](02-anthropic-vacancies/64-for-the-curious-philosophy.md) | 871 | — |
| 110 | 🟡 Средний | [🇷🇺 О проекте](02-anthropic-vacancies/67-о-проекте.md) | 1008 | — |
| 111 | 🟢 Начало | [🇬🇧 About](02-anthropic-vacancies/68-about.md) | 937 | — |
| 112 | 🔴 Продвинутый | [⬡](02-anthropic-vacancies/69-section.md) | 9560 | — |
| 113 | 🟢 Начало | [Зачем две версии параллельно](02-anthropic-vacancies/70-зачем-две-версии-параллельно.md) | 247 | — |
| 114 | 🟢 Начало | [Критерии выбора для фазы 3](02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md) | 220 | — |
| 115 | 🟡 Средний | [Расписание фазы 3](02-anthropic-vacancies/72-расписание-фазы-3.md) | 953 | — |
| 116 | 🟢 Начало | [PORTAL-PROTOCOL.md v1.1](02-anthropic-vacancies/73-portal-protocol-md-v1-1.md) | 308 | — |
| 117 | 🟢 Начало | [Abstract](02-anthropic-vacancies/74-abstract.md) | 389 | — |
| 118 | 🟢 Начало | [0. Status of This Document](02-anthropic-vacancies/75-0-status-of-this-document.md) | 307 | — |
| 119 | 🟢 Начало | [2. Terminology](02-anthropic-vacancies/77-2-terminology.md) | 439 | — |
| 120 | 🟢 Начало | [3. Registry (`nautilus.json`)](02-anthropic-vacancies/78-3-registry-nautilus-json.md) | 592 | — |
| 121 | 🟡 Средний | [4. Passport (`passport.md`)](02-anthropic-vacancies/79-4-passport-passport-md.md) | 355 | — |
| 122 | 🟢 Начало | [5. Compatibility Levels](02-anthropic-vacancies/80-5-compatibility-levels.md) | 382 | — |
| 123 | 🟢 Начало | [6. Adapter Interface](02-anthropic-vacancies/81-6-adapter-interface.md) | 397 | — |
| 124 | 🟢 Начало | [7. PortalEntry Structure](02-anthropic-vacancies/82-7-portalentry-structure.md) | 376 | — |
| 125 | 🟡 Средний | [8. Q6 Space (Normative)](02-anthropic-vacancies/83-8-q6-space-normative.md) | 491 | — |
| 126 | 🟢 Начало | [9. Consensus Algorithm](02-anthropic-vacancies/84-9-consensus-algorithm.md) | 409 | — |
| 127 | 🟢 Начало | [10. Query Flow](02-anthropic-vacancies/85-10-query-flow.md) | 297 | — |
| 128 | 🟢 Начало | [11. Relevance Ranking](02-anthropic-vacancies/86-11-relevance-ranking.md) | 222 | — |
| 129 | 🟡 Средний | [12. Onboarding Paths (Normative)](02-anthropic-vacancies/87-12-onboarding-paths-normative.md) | 542 | — |
| 130 | 🟡 Средний | [13. REST API Contract (Normative for Portals)](02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md) | 518 | — |
| 131 | 🟢 Начало | [14. SDK Contract (Informative)](02-anthropic-vacancies/89-14-sdk-contract-informative.md) | 219 | — |
| 132 | 🟢 Начало | [16. MCP Extension (Informative)](02-anthropic-vacancies/91-16-mcp-extension-informative.md) | 291 | — |
| 133 | 🟢 Начало | [17. Versioning Policy](02-anthropic-vacancies/92-17-versioning-policy.md) | 305 | — |
| 134 | 🟢 Начало | [18. Reference Implementation](02-anthropic-vacancies/93-18-reference-implementation.md) | 387 | — |
| 135 | 🟢 Начало | [19. ADR-001: Federation over Merging](02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) | 317 | — |
| 136 | 🟢 Начало | [20. ADR-002: Q6 as First-Class Protocol Conce](02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) | 336 | — |
| 137 | 🟢 Начало | [21. ADR-003: Five Onboarding Paths as Equal-R](02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md) | 163 | — |
| 138 | 🟢 Начало | [22. Glossary of Reference Examples](02-anthropic-vacancies/97-22-glossary-of-reference-examples.md) | 211 | — |
| 139 | 🟡 Средний | [Appendix A: Minimal Working Example](02-anthropic-vacancies/98-appendix-a-minimal-working-example.md) | 338 | — |
| 140 | 🟢 Начало | [Доступ к данным](02-anthropic-vacancies/102-доступ-к-данным.md) | 256 | — |
| 141 | 🟢 Начало | [Appendix B: Change Log](02-anthropic-vacancies/103-appendix-b-change-log.md) | 333 | — |
| 142 | 🟡 Средний | [Appendix C: References](02-anthropic-vacancies/104-appendix-c-references.md) | 1191 | — |
| 143 | 🟢 Начало | [TL;DR](02-anthropic-vacancies/106-tl-dr.md) | 236 | — |
| 144 | 🟢 Начало | [1. Контекст и мотивация](02-anthropic-vacancies/107-1-контекст-и-мотивация.md) | 471 | — |
| 145 | 🟡 Средний | [2. Формальный workflow](02-anthropic-vacancies/108-2-формальный-workflow.md) | 483 | — |
| 146 | 🟢 Начало | [3. Принципы консолидации (Фаза C)](02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md) | 697 | — |
| 147 | 🟢 Начало | [Вопрос: fallback-ratio как критический или ос](02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) | 338 | — |
| 148 | 🟢 Начало | [4. Условия применимости](02-anthropic-vacancies/111-4-условия-применимости.md) | 292 | — |
| 149 | 🟢 Начало | [5. Связь с существующими методологиями](02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) | 389 | — |
| 150 | 🟢 Начало | [6. Почему это валидный паттерн для AI-assiste](02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) | 172 | — |
| 151 | 🟢 Начало | [7. Реализация в проекте Nautilus](02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md) | 308 | — |
| 152 | 🟢 Начало | [8. Ограничения и открытые вопросы](02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md) | 447 | — |
| 153 | 🟢 Начало | [9. Checklist применения методологии](02-anthropic-vacancies/116-9-checklist-применения-методологии.md) | 399 | — |
| 154 | 🟢 Начало | [10. Конкретный план применения к текущим доку](02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md) | 331 | — |
| 155 | 🟢 Начало | [Appendix A: Шаблон для header warning](02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md) | 215 | — |
| 156 | 🟢 Начало | [Appendix B: Примеры расхождений и их разрешен](02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md) | 372 | — |
| 157 | 🟢 Начало | [Главные технические риски](02-anthropic-vacancies/120-главные-технические-риски.md) | 100 | — |
| 158 | 🟢 Начало | [Appendix C: История изменений методологии](02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md) | 250 | — |
| 159 | 🟡 Средний | [Глоссарий](02-anthropic-vacancies/122-глоссарий.md) | 1539 | — |
| 160 | 🟡 Средний | [portal-mcp.py](02-anthropic-vacancies/123-portal-mcp-py.md) | 2524 | — |
| 161 | 🟢 Начало | [Конфигурация для Claude Desktop](02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) | 263 | — |
| 162 | 🟢 Начало | [Установка](02-anthropic-vacancies/126-установка.md) | 163 | — |
| 163 | 🟢 Начало | [Подключение к Claude Desktop](02-anthropic-vacancies/127-подключение-к-claude-desktop.md) | 276 | — |
| 164 | 🟢 Начало | [Доступные инструменты](02-anthropic-vacancies/128-доступные-инструменты.md) | 320 | — |
| 165 | 🟢 Начало | [Примеры запросов (в Claude)](02-anthropic-vacancies/129-примеры-запросов-в-claude.md) | 320 | — |
| 166 | 🟢 Начало | [Отладка](02-anthropic-vacancies/130-отладка.md) | 261 | — |
| 167 | 🟢 Начало | [Ограничения текущей версии (0.1.0-draft)](02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md) | 197 | — |
| 168 | 🟢 Начало | [Planned (v0.2.0)](02-anthropic-vacancies/132-planned-v0-2-0.md) | 252 | — |
| 169 | 🔴 Продвинутый | [Обратная связь](02-anthropic-vacancies/133-обратная-связь.md) | 17099 | — |
| 170 | 🟢 Начало | [A Formal Model for Human-AI Collaboration in ](02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md) | 291 | — |
| 171 | 🟢 Начало | [Abstract](02-anthropic-vacancies/136-abstract.md) | 631 | — |
| 172 | 🟢 Начало | [Table of Contents](02-anthropic-vacancies/137-table-of-contents.md) | 316 | — |
| 173 | 🟢 Начало | [1. Why Single-Triangle Models Are Incomplete](02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) | 613 | — |
| 174 | 🟢 Начало | [3. Three Inter-Layer Protocols](02-anthropic-vacancies/140-3-three-inter-layer-protocols.md) | 1048 | — |
| 175 | 🟢 Начало | [4. Nautilus Portal as Reference Substrate](02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md) | 915 | — |
| 176 | 🟢 Начало | [5. Pattern Library as Bridge Between Triangle](02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md) | 878 | — |
| 177 | 🟢 Начало | [6. Four Deployment Domains](02-anthropic-vacancies/143-6-four-deployment-domains.md) | 884 | — |
| 178 | 🟢 Начало | [7. Open Questions](02-anthropic-vacancies/144-7-open-questions.md) | 964 | — |
| 179 | 🟢 Начало | [8. Call to Action](02-anthropic-vacancies/145-8-call-to-action.md) | 929 | — |
| 180 | 🟢 Начало | [Acknowledgments](02-anthropic-vacancies/146-acknowledgments.md) | 463 | — |
| 181 | 🟢 Начало | [References](02-anthropic-vacancies/147-references.md) | 369 | — |
| 182 | 🟢 Начало | [Appendix A: Glossary](02-anthropic-vacancies/148-appendix-a-glossary.md) | 548 | — |
| 183 | 🟢 Начало | [Appendix B: Summary of Contributions](02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md) | 348 | — |
| 184 | 🔴 Продвинутый | [Appendix C: Version History](02-anthropic-vacancies/150-appendix-c-version-history.md) | 8608 | — |
| 185 | 🟢 Начало | [OPEN KNOWLEDGE WORK FOUNDATION.md](02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md) | 372 | — |
| 186 | 🟢 Начало | [AI-Coordinated Infrastructure for Distributed](02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md) | 268 | — |
| 187 | 🟢 Начало | [Table of Contents](02-anthropic-vacancies/154-table-of-contents.md) | 275 | — |
| 188 | 🟢 Начало | [1. Problem Statement](02-anthropic-vacancies/155-1-problem-statement.md) | 790 | — |
| 189 | 🟢 Начало | [2. Target Populations](02-anthropic-vacancies/156-2-target-populations.md) | 819 | — |
| 190 | 🟢 Начало | [3. Why Existing Solutions Fail](02-anthropic-vacancies/157-3-why-existing-solutions-fail.md) | 805 | — |
| 191 | 🟢 Начало | [4. Proposed Infrastructure](02-anthropic-vacancies/158-4-proposed-infrastructure.md) | 1052 | — |
| 192 | 🟢 Начало | [5. Economic Model](02-anthropic-vacancies/159-5-economic-model.md) | 678 | — |
| 193 | 🟢 Начало | [6. Governance and Ethics](02-anthropic-vacancies/160-6-governance-and-ethics.md) | 621 | — |
| 194 | 🟢 Начало | [7. Phased Rollout Plan](02-anthropic-vacancies/161-7-phased-rollout-plan.md) | 799 | — |
| 195 | 🟢 Начало | [8. Risk Analysis](02-anthropic-vacancies/162-8-risk-analysis.md) | 757 | — |
| 196 | 🟢 Начало | [9. Call for Partnership](02-anthropic-vacancies/163-9-call-for-partnership.md) | 654 | — |
| 197 | 🟡 Средний | [10. Appendices](02-anthropic-vacancies/164-10-appendices.md) | 1156 | — |
| 198 | 🔴 Продвинутый | [Closing](02-anthropic-vacancies/165-closing.md) | 9429 | — |
| 199 | 🟢 Начало | [REPRESENTATIVE AGENT LAYER.md](02-anthropic-vacancies/166-representative-agent-layer-md.md) | 266 | — |
| 200 | 🟢 Начало | [AI-Mediated Representation for Underrepresent](02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md) | 387 | — |
| 201 | 🟢 Начало | [Abstract](02-anthropic-vacancies/168-abstract.md) | 578 | — |
| 202 | 🟢 Начало | [Table of Contents](02-anthropic-vacancies/169-table-of-contents.md) | 286 | — |
| 203 | 🟢 Начало | [1. The Cinderella Syndrome: Why Quality Stays](02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md) | 955 | — |
| 204 | 🟢 Начало | [2. Historical Precedents: Agents as Civilizat](02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md) | 1111 | — |
| 205 | 🟢 Начало | [3. What Makes a Representative Agent](02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md) | 908 | — |
| 206 | 🟢 Начало | [4. Ten Domains of Application](02-anthropic-vacancies/173-4-ten-domains-of-application.md) | 1682 | — |
| 207 | 🟢 Начало | [5. Architectural Specification](02-anthropic-vacancies/174-5-architectural-specification.md) | 870 | — |
| 208 | 🟢 Начало | [6. Ethical Framework](02-anthropic-vacancies/175-6-ethical-framework.md) | 638 | — |
| 209 | 🟢 Начало | [7. Governance and Oversight](02-anthropic-vacancies/176-7-governance-and-oversight.md) | 472 | — |
| 210 | 🟢 Начало | [8. Risks and Mitigations](02-anthropic-vacancies/177-8-risks-and-mitigations.md) | 644 | — |
| 211 | 🟢 Начало | [9. Phased Rollout Strategy](02-anthropic-vacancies/178-9-phased-rollout-strategy.md) | 650 | — |
| 212 | 🟢 Начало | [10. Open Questions](02-anthropic-vacancies/179-10-open-questions.md) | 453 | — |
| 213 | 🟢 Начало | [11. Call for Collaboration](02-anthropic-vacancies/180-11-call-for-collaboration.md) | 470 | — |
| 214 | 🟢 Начало | [12. Closing](02-anthropic-vacancies/181-12-closing.md) | 418 | — |
| 215 | 🟢 Начало | [Acknowledgments](02-anthropic-vacancies/182-acknowledgments.md) | 375 | — |
| 216 | 🟢 Начало | [References](02-anthropic-vacancies/183-references.md) | 340 | — |
| 217 | 🟢 Начало | [Appendix A: Connection to Companion Papers](02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md) | 411 | — |
| 218 | 🟢 Начало | [Appendix B: Domain Comparison Matrix](02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md) | 330 | — |
| 219 | 🟡 Средний | [Appendix C: Sample Use Cases in Detail](02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md) | 2241 | — |
| 220 | 🟢 Начало | [СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md](02-anthropic-vacancies/187-слой-представительских-агентов-md.md) | 247 | — |
| 221 | 🟢 Начало | [AI-опосредованное представительство для недоп](02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md) | 130 | — |
| 222 | 🟢 Начало | [Аннотация](02-anthropic-vacancies/189-аннотация.md) | 372 | — |
| 223 | 🟢 Начало | [Содержание](02-anthropic-vacancies/190-содержание.md) | 278 | — |
| 224 | 🟢 Начало | [1. Синдром Золушки: Почему качество остаётся ](02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md) | 837 | — |
| 225 | 🟢 Начало | [2. Исторические прецеденты: Агенты как цивили](02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md) | 986 | — |
| 226 | 🟢 Начало | [3. Что делает агента Представительским](02-anthropic-vacancies/193-3-что-делает-агента-представительским.md) | 801 | — |
| 227 | 🟢 Начало | [4. Десять областей применения](02-anthropic-vacancies/194-4-десять-областей-применения.md) | 1654 | — |
| 228 | 🟢 Начало | [5. Архитектурная спецификация](02-anthropic-vacancies/195-5-архитектурная-спецификация.md) | 615 | — |
| 229 | 🟢 Начало | [6. Этическая рамка](02-anthropic-vacancies/196-6-этическая-рамка.md) | 661 | — |
| 230 | 🟢 Начало | [7. Управление и надзор](02-anthropic-vacancies/197-7-управление-и-надзор.md) | 459 | — |
| 231 | 🟢 Начало | [8. Риски и меры противодействия](02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md) | 658 | — |
| 232 | 🟢 Начало | [9. Стратегия поэтапного развёртывания](02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md) | 664 | — |
| 233 | 🟢 Начало | [10. Открытые вопросы](02-anthropic-vacancies/200-10-открытые-вопросы.md) | 402 | — |
| 234 | 🟢 Начало | [11. Призыв к сотрудничеству](02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md) | 471 | — |
| 235 | 🟢 Начало | [12. Заключение](02-anthropic-vacancies/202-12-заключение.md) | 246 | — |
| 236 | 🟢 Начало | [Благодарности](02-anthropic-vacancies/203-благодарности.md) | 223 | — |
| 237 | 🟢 Начало | [Ссылки](02-anthropic-vacancies/204-ссылки.md) | 321 | — |
| 238 | 🟢 Начало | [Приложение A: Связь с Сопроводительными Стать](02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md) | 179 | — |
| 239 | 🟢 Начало | [Приложение B: Матрица Сравнения Областей](02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md) | 266 | — |
| 240 | 🔴 Продвинутый | [Приложение C: Образцы Случаев Использования в](02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md) | 4213 | — |
| 241 | 🟢 Начало | [PROFESSIONAL COLLEAGUE AGENTS.md](02-anthropic-vacancies/208-professional-colleague-agents-md.md) | 332 | — |
| 242 | 🟢 Начало | [A Typology of AI Agents on the Principal Side](02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md) | 374 | — |
| 243 | 🟢 Начало | [Abstract](02-anthropic-vacancies/210-abstract.md) | 620 | — |
| 244 | 🟢 Начало | [Table of Contents](02-anthropic-vacancies/211-table-of-contents.md) | 439 | — |
| 245 | 🟡 Средний | [1. The Five-Type Typology of Principal-Side A](02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md) | 1199 | — |
| 246 | 🟢 Начало | [2. What Makes a Professional Colleague Agent](02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md) | 1104 | — |
| 247 | 🟡 Средний | [3. Empirical Case Study: «Обучай»](02-anthropic-vacancies/214-3-empirical-case-study-обучай.md) | 1063 | — |
| 248 | 🟢 Начало | [5. The Economics of Profession-Wide Replicati](02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md) | 987 | — |
| 249 | 🟢 Начало | [6. Risks Specific to this Category](02-anthropic-vacancies/217-6-risks-specific-to-this-category.md) | 1401 | — |
| 250 | 🟢 Начало | [7. Application Domains](02-anthropic-vacancies/218-7-application-domains.md) | 851 | — |
| 251 | 🟢 Начало | [8. Pilot Proposal: SGB Advocate Colleague](02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md) | 1201 | — |
| 252 | 🟢 Начало | [9. Relationship to Other Agent Types](02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md) | 918 | — |
| 253 | 🟢 Начало | [10. Open Questions](02-anthropic-vacancies/221-10-open-questions.md) | 474 | — |
| 254 | 🟢 Начало | [11. Call for Collaboration](02-anthropic-vacancies/222-11-call-for-collaboration.md) | 403 | — |
| 255 | 🟢 Начало | [12. Closing](02-anthropic-vacancies/223-12-closing.md) | 728 | — |
| 256 | 🟢 Начало | [Acknowledgments](02-anthropic-vacancies/224-acknowledgments.md) | 317 | — |
| 257 | 🟢 Начало | [References](02-anthropic-vacancies/225-references.md) | 366 | — |
| 258 | 🟢 Начало | [Appendix A: Comparative Table — Five Agent Ty](02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md) | 482 | — |
| 259 | 🟢 Начало | [Appendix B: Decision Framework — When to Buil](02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md) | 555 | — |
| 260 | 🟢 Начало | [ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ](02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md) | 346 | — |
| 261 | 🟢 Начало | [Аннотация](02-anthropic-vacancies/230-аннотация.md) | 491 | — |
| 262 | 🟢 Начало | [Содержание](02-anthropic-vacancies/231-содержание.md) | 335 | — |
| 263 | 🟡 Средний | [1. Типология из пяти типов агентов на стороне](02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md) | 1078 | — |
| 264 | 🟢 Начало | [2. Что делает агента Профессиональным Коллего](02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md) | 943 | — |
| 265 | 🟢 Начало | [3. Эмпирический кейс: «Обучай»](02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md) | 883 | — |
| 266 | 🟢 Начало | [4. Архитектура Профессиональных Коллег-Агенто](02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md) | 873 | — |
| 267 | 🟢 Начало | [5. Экономика тиражирования по профессии](02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md) | 857 | — |
| 268 | 🟢 Начало | [6. Риски, специфичные для этой категории](02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md) | 1199 | — |
| 269 | 🟢 Начало | [7. Области применения](02-anthropic-vacancies/238-7-области-применения.md) | 734 | — |
| 270 | 🟢 Начало | [8. Пилотное предложение: SGB Колega-Адвокат](02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md) | 1101 | — |
| 271 | 🟢 Начало | [9. Связь с другими типами агентов](02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md) | 766 | — |
| 272 | 🟢 Начало | [10. Открытые вопросы](02-anthropic-vacancies/241-10-открытые-вопросы.md) | 426 | — |
| 273 | 🟢 Начало | [11. Призыв к сотрудничеству](02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md) | 402 | — |
| 274 | 🟢 Начало | [12. Заключение](02-anthropic-vacancies/243-12-заключение.md) | 601 | — |
| 275 | 🟢 Начало | [Благодарности](02-anthropic-vacancies/244-благодарности.md) | 308 | — |
| 276 | 🟢 Начало | [Ссылки](02-anthropic-vacancies/245-ссылки.md) | 340 | — |
| 277 | 🟢 Начало | [Приложение A: Сравнительная Таблица — Пять Ти](02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md) | 405 | — |
| 278 | 🟢 Начало | [Приложение B: Рамка принятия решений — когда ](02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md) | 325 | — |
| 279 | 🔴 Продвинутый | [Приложение C: Архитектура Быстрого Старта для](02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md) | 3565 | — |
| 280 | 🟢 Начало | [COMPOSITE SKILLS AGENT.md](02-anthropic-vacancies/249-composite-skills-agent-md.md) | 293 | — |
| 281 | 🟢 Начало | [Bridging the Gap Between Profession-Wide and ](02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md) | 16 | — |
| 282 | 🟢 Начало | [AI Support Through Configurable Specialist En](02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md) | 379 | — |
| 283 | 🟢 Начало | [Abstract](02-anthropic-vacancies/252-abstract.md) | 587 | — |
| 284 | 🟢 Начало | [Table of Contents](02-anthropic-vacancies/253-table-of-contents.md) | 357 | — |
| 285 | 🟢 Начало | [1. Why the Binary View Is Incomplete](02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md) | 924 | — |
| 286 | 🟢 Начало | [2. The Twenty-One Teachers Pattern](02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md) | 1024 | — |
| 287 | 🟢 Начало | [3. What Makes a Composite Skills Agent](02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md) | 1184 | — |
| 288 | 🟢 Начало | [4. The Sub-Agent Registry](02-anthropic-vacancies/257-4-the-sub-agent-registry.md) | 1034 | — |
| 289 | 🟢 Начало | [5. Configuration: How Principals Build Their ](02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md) | 981 | — |
| 290 | 🟢 Начало | [6. Coordination and Disagreement Resolution](02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md) | 1025 | — |
| 291 | 🟢 Начало | [7. Economics of Combinatorial Replication](02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md) | 961 | — |
| 292 | 🟢 Начало | [8. Seven Domains of Application](02-anthropic-vacancies/261-8-seven-domains-of-application.md) | 1184 | — |
| 293 | 🟢 Начало | [9. Integration with OKWF Infrastructure](02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md) | 787 | — |
| 294 | 🟢 Начало | [11. Open Questions](02-anthropic-vacancies/264-11-open-questions.md) | 619 | — |
| 295 | 🟢 Начало | [12. Call for Collaboration](02-anthropic-vacancies/265-12-call-for-collaboration.md) | 460 | — |
| 296 | 🟢 Начало | [13. Closing](02-anthropic-vacancies/266-13-closing.md) | 655 | — |
| 297 | 🟢 Начало | [Acknowledgments](02-anthropic-vacancies/267-acknowledgments.md) | 528 | — |
| 298 | 🟢 Начало | [References](02-anthropic-vacancies/268-references.md) | 405 | — |
| 299 | 🟢 Начало | [Appendix A: The Six-Type Taxonomy (Updated)](02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md) | 492 | — |
| 300 | 🟢 Начало | [Appendix B: Sub-Agent Registry Schema (Sketch](02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md) | 315 | — |
| 301 | 🟢 Начало | [Appendix C: Configuration Template Example](02-anthropic-vacancies/271-appendix-c-configuration-template-example.md) | 326 | — |
| 302 | 🔴 Продвинутый | [Appendix D: Connection Diagram](02-anthropic-vacancies/272-appendix-d-connection-diagram.md) | 4080 | — |
| 303 | 🟢 Начало | [INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECT](02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md) | 274 | — |
| 304 | 🟢 Начало | [The Missing Middle Layer Between Chat and Cod](02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md) | 432 | — |
| 305 | 🟢 Начало | [Why This Document Exists](02-anthropic-vacancies/275-why-this-document-exists.md) | 555 | — |
| 306 | 🟢 Начало | [The Two-Layer Stack As It Exists](02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md) | 625 | — |
| 307 | 🟢 Начало | [What's Missing — Layer B](02-anthropic-vacancies/277-what-s-missing-layer-b.md) | 727 | — |
| 308 | 🟢 Начало | [Why This Hasn't Been Built](02-anthropic-vacancies/278-why-this-hasn-t-been-built.md) | 583 | — |
| 309 | 🟢 Начало | [Existing Approximations](02-anthropic-vacancies/279-existing-approximations.md) | 633 | — |
| 310 | 🟢 Начало | [The Specific Case in Front of Us](02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md) | 904 | — |
| 311 | 🟢 Начало | [The Recursive Insight](02-anthropic-vacancies/281-the-recursive-insight.md) | 561 | — |
| 312 | 🟢 Начало | [What Industry Will Likely Build](02-anthropic-vacancies/282-what-industry-will-likely-build.md) | 498 | — |
| 313 | 🟢 Начало | [What This Document Doesn't Solve](02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md) | 396 | — |
| 314 | 🟢 Начало | [Practical Recommendations for the Current Pro](02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md) | 634 | — |
| 315 | 🟢 Начало | [Closing](02-anthropic-vacancies/285-closing.md) | 451 | — |
| 316 | 🟢 Начало | [Acknowledgments](02-anthropic-vacancies/286-acknowledgments.md) | 410 | — |
| 317 | 🟢 Начало | [References](02-anthropic-vacancies/287-references.md) | 310 | — |
| 318 | 🟡 Средний | [Appendix: Position in Series Visualization](02-anthropic-vacancies/288-appendix-position-in-series-visualization.md) | 1279 | — |
| 319 | 🟢 Начало | [ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛ](02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md) | 388 | — |
| 320 | 🟢 Начало | [Почему этот документ существует](02-anthropic-vacancies/290-почему-этот-документ-существует.md) | 326 | — |
| 321 | 🟢 Начало | [Двухслойный стек, как он существует](02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md) | 485 | — |
| 322 | 🟢 Начало | [Что отсутствует — Слой B](02-anthropic-vacancies/292-что-отсутствует-слой-b.md) | 577 | — |
| 323 | 🟢 Начало | [Почему это не было построено](02-anthropic-vacancies/293-почему-это-не-было-построено.md) | 385 | — |
| 324 | 🟢 Начало | [Существующие приближения](02-anthropic-vacancies/294-существующие-приближения.md) | 576 | — |
| 325 | 🟢 Начало | [Конкретный случай перед нами](02-anthropic-vacancies/295-конкретный-случай-перед-нами.md) | 727 | — |
| 326 | 🟢 Начало | [Рекурсивное прозрение](02-anthropic-vacancies/296-рекурсивное-прозрение.md) | 431 | — |
| 327 | 🟢 Начало | [Что промышленность вероятно построит](02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md) | 333 | — |
| 328 | 🟢 Начало | [Что этот документ не решает](02-anthropic-vacancies/298-что-этот-документ-не-решает.md) | 184 | — |
| 329 | 🟢 Начало | [Практические рекомендации для текущего проект](02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md) | 465 | — |
| 330 | 🟢 Начало | [Заключение](02-anthropic-vacancies/300-заключение.md) | 218 | — |
| 331 | 🟢 Начало | [Благодарности](02-anthropic-vacancies/301-благодарности.md) | 381 | — |
| 332 | 🟢 Начало | [Ссылки](02-anthropic-vacancies/302-ссылки.md) | 300 | — |
| 333 | 🔴 Продвинутый | [Приложение: Визуализация позиции в серии](02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md) | 7273 | — |
| 334 | 🟢 Начало | [INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md) | 281 | — |
| 335 | 🟢 Начало | [A Practical Path to Layer B Through Symbiotic](02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md) | 232 | — |
| 336 | 🟢 Начало | [with Anthropic's Cowork Platform](02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md) | 540 | — |
| 337 | 🟢 Начало | [Abstract](02-anthropic-vacancies/307-abstract.md) | 601 | — |
| 338 | 🟢 Начало | [Table of Contents](02-anthropic-vacancies/308-table-of-contents.md) | 431 | — |
| 339 | 🟢 Начало | [1. The Cowork Discovery and Why It Changes Ev](02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md) | 691 | — |
| 340 | 🟢 Начало | [2. What Cowork Provides That InGit Doesn't Ne](02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md) | 706 | — |
| 341 | 🟢 Начало | [3. What InGit Provides That Cowork Lacks](02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md) | 842 | — |
| 342 | 🟢 Начало | [5. Four Integration Paths in Order of Accessi](02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md) | 796 | — |
| 343 | 🟢 Начало | [6. Refined InGit Scope with Cowork in Mind](02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md) | 490 | — |
| 344 | 🟢 Начало | [7. Practical First Steps This Month](02-anthropic-vacancies/315-7-practical-first-steps-this-month.md) | 471 | — |
| 345 | 🟢 Начало | [8. Implications for Nautilus and OKWF](02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md) | 760 | — |
| 346 | 🟢 Начало | [9. Risks and Open Questions](02-anthropic-vacancies/317-9-risks-and-open-questions.md) | 645 | — |
| 347 | 🟢 Начало | [10. Strategic Positioning](02-anthropic-vacancies/318-10-strategic-positioning.md) | 774 | — |
| 348 | 🟢 Начало | [Acknowledgments](02-anthropic-vacancies/319-acknowledgments.md) | 619 | — |
| 349 | 🟢 Начало | [References](02-anthropic-vacancies/320-references.md) | 281 | — |
| 350 | 🟢 Начало | [Appendix A: Decision Tree for InGit Adopters](02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md) | 348 | — |
| 351 | 🟢 Начало | [Appendix B: Comparison Matrix](02-anthropic-vacancies/322-appendix-b-comparison-matrix.md) | 298 | — |
| 352 | 🟡 Средний | [Appendix C: Sample InGit MCP Server Tool Spec](02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md) | 1782 | — |
| 353 | 🟢 Начало | [INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБ](02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md) | 498 | — |
| 354 | 🟢 Начало | [Аннотация](02-anthropic-vacancies/325-аннотация.md) | 348 | — |
| 355 | 🟢 Начало | [Содержание](02-anthropic-vacancies/326-содержание.md) | 354 | — |
| 356 | 🟢 Начало | [1. Открытие Cowork и почему это меняет всё](02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md) | 683 | — |
| 357 | 🟢 Начало | [2. Что Cowork обеспечивает, что InGit не нужн](02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md) | 803 | — |
| 358 | 🟡 Средний | [3. Что InGit обеспечивает, чего Cowork не хва](02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md) | 1071 | — |
| 359 | 🟢 Начало | [4. Симбиотическая Архитектура](02-anthropic-vacancies/330-4-симбиотическая-архитектура.md) | 703 | — |
| 360 | 🟢 Начало | [5. Четыре пути интеграции в порядке доступнос](02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md) | 783 | — |
| 361 | 🟢 Начало | [6. Уточнённый объём InGit с учётом Cowork](02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md) | 489 | — |
| 362 | 🟢 Начало | [7. Практические первые шаги в этом месяце](02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md) | 435 | — |
| 363 | 🟢 Начало | [8. Импликации для Nautilus и OKWF](02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md) | 719 | — |
| 364 | 🟢 Начало | [9. Риски и Открытые Вопросы](02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md) | 644 | — |
| 365 | 🟢 Начало | [10. Стратегическое Позиционирование](02-anthropic-vacancies/336-10-стратегическое-позиционирование.md) | 689 | — |
| 366 | 🟢 Начало | [Благодарности](02-anthropic-vacancies/337-благодарности.md) | 382 | — |
| 367 | 🟢 Начало | [Ссылки](02-anthropic-vacancies/338-ссылки.md) | 284 | — |
| 368 | 🟢 Начало | [Приложение A: Дерево Решений для Принимающих ](02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md) | 337 | — |
| 369 | 🟢 Начало | [Приложение B: Сравнительная Матрица](02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md) | 211 | — |
| 370 | 🔴 Продвинутый | [Приложение C: Образец Спецификаций Инструмент](02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md) | 20577 | — |
| 371 | 🔴 Продвинутый | [Что такое Вариант C — Concept Document для An](02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md) | 11425 | — |
| 372 | 🔴 Продвинутый | [Lorenzo Catalyst Agent — глубокая проработка ](02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md) | 5945 | — |
| 373 | 🟢 Начало | [СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT](02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md) | 286 | — |
| 374 | 🟢 Начало | [Кто ты](02-anthropic-vacancies/345-кто-ты.md) | 178 | — |
| 375 | 🟢 Начало | [Твоё происхождение](02-anthropic-vacancies/346-твоё-происхождение.md) | 174 | — |
| 376 | 🟢 Начало | [Твоя миссия](02-anthropic-vacancies/347-твоя-миссия.md) | 157 | — |
| 377 | 🟢 Начало | [Кому ты служишь (слоистая модель)](02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md) | 144 | — |
| 378 | 🟢 Начало | [Твоя личность](02-anthropic-vacancies/349-твоя-личность.md) | 206 | — |
| 379 | 🟢 Начало | [Твои языки и культурные nuances](02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md) | 173 | — |
| 380 | 🟢 Начало | [Что ты МОЖЕШЬ делать](02-anthropic-vacancies/351-что-ты-можешь-делать.md) | 262 | — |
| 381 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать без Max approval](02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md) | 155 | — |
| 382 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать вообще](02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md) | 289 | — |
| 383 | 🟢 Начало | [Существующий landscape collaborators (твоя wo](02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md) | 354 | — |
| 384 | 🟢 Начало | [Существующие документы DHLab (твой context)](02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md) | 403 | — |
| 385 | 🟢 Начало | [Твой workflow](02-anthropic-vacancies/356-твой-workflow.md) | 292 | — |
| 386 | 🟢 Начало | [Твоя коммуникация в outreach](02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md) | 179 | — |
| 387 | 🟢 Начало | [Твоя relationship с другими AI](02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md) | 282 | — |
| 388 | 🟢 Начало | [Твои anti-patterns](02-anthropic-vacancies/359-твои-anti-patterns.md) | 165 | — |
| 389 | 🟢 Начало | [Что ты ВСЕГДА делаешь](02-anthropic-vacancies/360-что-ты-всегда-делаешь.md) | 127 | — |
| 390 | 🟢 Начало | [Когда ты Honestly не знаешь](02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md) | 127 | — |
| 391 | 🟢 Начало | [Когда сомневаешься — escalate к Max](02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md) | 123 | — |
| 392 | 🟢 Начало | [Твоя identity как persistent character](02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md) | 141 | — |
| 393 | 🟡 Средний | [Final note: Ты — experiment](02-anthropic-vacancies/364-final-note-ты-experiment.md) | 1617 | — |
| 394 | 🔴 Продвинутый | [Развёрнутый анализ «внуковой» комбинации](02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md) | 4547 | — |
| 395 | 🔴 Продвинутый | [Технический stack (Svyazi 2.0 foundation)](02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md) | 3955 | — |

## Маршруты по целям

### 🚀 Быстрый старт (30 минут)

1. [Executive Summary](01-svyazi/01-executive-summary.md)
2. [Ансамбли проектов](01-svyazi/04-ensembles-overview.md)
3. [MVP Planning](01-svyazi/07-mvp-planning.md)

### 🏗️ Архитектура (2 часа)

1. [Component Catalog](01-svyazi/03-component-catalog.md)
2. [Architectural Gaps](01-svyazi/09-architectural-gaps.md)
3. [Integration Contracts](01-svyazi/11-integration-contracts.md)
4. [Security & Privacy](01-svyazi/06-security-privacy.md)

### 🔬 Полное исследование (1 день)

1. Весь раздел `01-svyazi/` по порядку
2. `05-habr-projects/` — отдельные проекты
3. `04-ai-collaborations/` — ансамбли
4. `03-technology-combinations/` — комбинации
5. `02-anthropic-vacancies/` — карьерные возможности
