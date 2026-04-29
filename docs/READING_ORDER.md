# Рекомендуемый порядок чтения

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
| 1 | 🟡 Средний | [04-ensembles-overview](docs/01-svyazi/04-ensembles-overview.md) | 1288 | — |
| 2 | 🟢 Начало | [Svyazi[^svyazi] 2.0 — Исполнительное резюме](docs/01-svyazi/01-executive-summary.md) | 726 | — |
| 3 | 🟢 Начало | [Методика и рамка отбора проектов](docs/01-svyazi/02-methodology.md) | 480 | — |
| 4 | 🟢 Начало | [Продолжение исследования для Svyazi 2.0](docs/01-svyazi/00-intro-part2.md) | 6 | — |
| 5 | 🟡 Средний | [03-component-catalog](docs/01-svyazi/03-component-catalog.md) | 1383 | — |
| 6 | 🟢 Начало | [09-architectural-gaps](docs/01-svyazi/09-architectural-gaps.md) | 758 | `01-executive-summary.md`, `03-component-catalog.md` |
| 7 | 🟢 Начало | [11-integration-contracts](docs/01-svyazi/11-integration-contracts.md) | 737 | `09-architectural-gaps.md` |
| 8 | 🟢 Начало | [10-second-order-ensembles](docs/01-svyazi/10-second-order-ensembles.md) | 908 | `04-ensembles-overview.md` |
| 9 | 🟢 Начало | [06-security-privacy](docs/01-svyazi/06-security-privacy.md) | 823 | — |
| 10 | 🟡 Средний | [07-mvp-planning](docs/01-svyazi/07-mvp-planning.md) | 1063 | — |
| 11 | 🟢 Начало | [12-roadmap](docs/01-svyazi/12-roadmap.md) | 722 | `07-mvp-planning.md`, `11-integration-contracts.md` |
| 12 | 🟡 Средний | [13-contacts](docs/01-svyazi/13-contacts.md) | 1010 | — |
| 13 | 🟢 Начало | [14-limitations](docs/01-svyazi/14-limitations.md) | 638 | — |
| 14 | 🟢 Начало | [08-conclusions](docs/01-svyazi/08-conclusions.md) | 380 | — |
| 15 | 🟢 Начало | [Синтез: как проекты собираются вместе](docs/05-habr-projects/01-synthesis.md) | 245 | — |
| 16 | 🟢 Начало | [Авторы и контакты](docs/05-habr-projects/02-collaboration-partners.md) | 261 | — |
| 17 | 🟢 Начало | [Wikontic: семантический граф](docs/05-habr-projects/knowledge/wikontic.md) | 369 | — |
| 18 | 🟢 Начало | [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) | 359 | — |
| 19 | 🟡 Средний | [MemNet: исследовательская память](docs/05-habr-projects/memory/memnet.md) | 7246 | — |
| 20 | 🟢 Начало | [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) | 364 | — |
| 21 | 🟢 Начало | [Executive summary](docs/04-ai-collaborations/01-executive-summary.md) | 575 | — |
| 22 | 🟡 Средний | [Введение](docs/04-ai-collaborations/00-intro.md) | 11389 | — |
| 23 | 🟢 Начало | [Методика и рамка отбора](docs/04-ai-collaborations/02-методика-и-рамка-отбора.md) | 434 | — |
| 24 | 🟡 Средний | [Карта найденных проектов и паттернов](docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md) | 1478 | — |
| 25 | 🟡 Средний | [Приоритетные ансамбли](docs/04-ai-collaborations/04-приоритетные-ансамбли.md) | 1340 | — |
| 26 | 🟡 Средний | [План прототипа и возможные контакты](docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md) | 1130 | — |
| 27 | 🟢 Начало | [Безопасность, приватность и бюджетный роутинг](docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md) | 887 | — |
| 28 | 🟢 Начало | [Выводы](docs/04-ai-collaborations/07-выводы.md) | 470 | — |
| 29 | 🟢 Начало | [Что это продолжение добавляет](docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md) | 439 | — |
| 30 | 🟢 Начало | [Архитектурные зазоры, которые важнее новых ин](docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md) | 821 | — |
| 31 | 🟢 Начало | [Новые ансамбли следующего шага](docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md) | 984 | — |
| 32 | 🟢 Начало | [Интеграционный контракт, который стоит зафикс](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md) | 846 | — |
| 33 | 🟢 Начало | [Дорожная карта прототипа следующей итерации](docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md) | 787 | — |
| 34 | 🟢 Начало | [Контактная стратегия и узкие вопросы для авто](docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md) | 874 | — |
| 35 | 🟡 Средний | [Ограничения, лицензии и что пока лучше не скл](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md) | 3274 | — |
| 36 | 🟢 Начало | [Агентные системы и роутинг](docs/03-technology-combinations/01-agent-routing.md) | 358 | — |
| 37 | 🟢 Начало | [Графы знаний и Legal AI](docs/03-technology-combinations/02-knowledge-graphs.md) | 802 | — |
| 38 | 🟢 Начало | [Local-first и P2P стек](docs/03-technology-combinations/03-local-first.md) | 526 | — |
| 39 | 🟢 Начало | [Домен: немецкое социальное право](docs/03-technology-combinations/04-sozialrecht-domain.md) | 160 | — |
| 40 | 🟢 Начало | [Бенчмарки и производительность](docs/03-technology-combinations/05-benchmarks.md) | 997 | — |
| 41 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/58-content-overview.md) | 142 | — |
| 42 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/31-content-overview.md) | 186 | — |
| 43 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/38-content-overview.md) | 131 | — |
| 44 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/12-content-overview.md) | 182 | — |
| 45 | 🟢 Начало | [README.md](docs/02-anthropic-vacancies/65-readme-md.md) | 214 | — |
| 46 | 🔴 Продвинутый | [Интегральный анализ профиля svend4](docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) | 19217 | — |
| 47 | 🟢 Начало | [README-MCP.md— инструкция по установке](docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md) | 261 | — |
| 48 | 🟢 Начало | [Executive Summary](docs/02-anthropic-vacancies/153-executive-summary.md) | 565 | — |
| 49 | 🟢 Начало | [Content Overview](docs/02-anthropic-vacancies/48-content-overview.md) | 149 | — |
| 50 | 🟢 Начало | [REVIEW_METHODOLOGY.md](docs/02-anthropic-vacancies/105-review-methodology-md.md) | 271 | — |
| 51 | 🟢 Начало | [1. Introduction](docs/02-anthropic-vacancies/76-1-introduction.md) | 494 | — |
| 52 | 🔴 Продвинутый | [Введение](docs/02-anthropic-vacancies/00-intro.md) | 8984 | — |
| 53 | 🔴 Продвинутый | [ОБЩИЙ ПЛАН РАЗВИТИЯ NAUTILUS PORTAL PROTOCOL](docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md) | 3300 | — |
| 54 | 🟢 Начало | [1. Introduction](docs/02-anthropic-vacancies/06-1-introduction.md) | 383 | — |
| 55 | 🟢 Начало | [4. The Symbiotic Architecture](docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md) | 670 | — |
| 56 | 🟢 Начало | [4. Architecture of Professional Colleague Age](docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md) | 1096 | — |
| 57 | 🟢 Начало | [PORTAL-PROTOCOL.md](docs/02-anthropic-vacancies/03-portal-protocol-md.md) | 318 | — |
| 58 | 🟢 Начало | [THE DOUBLE-TRIANGLE ARCHITECTURE.md](docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md) | 281 | — |
| 59 | 🟢 Начало | [2. The Double-Triangle Architecture](docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md) | 753 | — |
| 60 | 🟡 Средний | [Appendix C: Quick-Start Architecture for SGB ](docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md) | 1978 | — |
| 61 | 🟢 Начало | [10. Risks Specific to Composite Architectures](docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md) | 1005 | — |
| 62 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/04-abstract.md) | 310 | — |
| 63 | 🟢 Начало | [0. Status of This Document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md) | 296 | — |
| 64 | 🟢 Начало | [15. Security Considerations](docs/02-anthropic-vacancies/90-15-security-considerations.md) | 491 | — |
| 65 | 🟢 Начало | [11. Security Considerations](docs/02-anthropic-vacancies/23-11-security-considerations.md) | 374 | — |
| 66 | 🟢 Начало | [2. Terminology](docs/02-anthropic-vacancies/07-2-terminology.md) | 302 | — |
| 67 | 🟢 Начало | [3. Registry (`nautilus.json`)](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) | 403 | — |
| 68 | 🟢 Начало | [4. Passport (`passport.md`)](docs/02-anthropic-vacancies/09-4-passport-passport-md.md) | 298 | — |
| 69 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/13-angle-perspective.md) | 209 | — |
| 70 | 🟢 Начало | [History](docs/02-anthropic-vacancies/16-history.md) | 160 | — |
| 71 | 🟢 Начало | [5. Compatibility Levels](docs/02-anthropic-vacancies/17-5-compatibility-levels.md) | 314 | — |
| 72 | 🟢 Начало | [6. Adapter Interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md) | 643 | — |
| 73 | 🟢 Начало | [7. PortalEntry Structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md) | 251 | — |
| 74 | 🟢 Начало | [8. Consensus Algorithm](docs/02-anthropic-vacancies/20-8-consensus-algorithm.md) | 317 | — |
| 75 | 🟢 Начало | [9. Query Flow](docs/02-anthropic-vacancies/21-9-query-flow.md) | 317 | — |
| 76 | 🟢 Начало | [10. QueryResult Structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md) | 327 | — |
| 77 | 🟢 Начало | [12. Versioning Policy](docs/02-anthropic-vacancies/24-12-versioning-policy.md) | 329 | — |
| 78 | 🟢 Начало | [13. Reference Implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md) | 291 | — |
| 79 | 🟢 Начало | [14. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) | 300 | — |
| 80 | 🟢 Начало | [15. Glossary of Examples](docs/02-anthropic-vacancies/27-15-glossary-of-examples.md) | 100 | — |
| 81 | 🟢 Начало | [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) | 183 | — |
| 82 | 🟢 Начало | [Appendix B: Change Log](docs/02-anthropic-vacancies/34-appendix-b-change-log.md) | 826 | — |
| 83 | 🟢 Начало | [passports/info1.md](docs/02-anthropic-vacancies/35-passports-info1-md.md) | 231 | — |
| 84 | 🟢 Начало | [Essence](docs/02-anthropic-vacancies/36-essence.md) | 128 | — |
| 85 | 🟢 Начало | [Native Format](docs/02-anthropic-vacancies/37-native-format.md) | 304 | — |
| 86 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/39-angle-perspective.md) | 233 | — |
| 87 | 🟢 Начало | [Bridges](docs/02-anthropic-vacancies/40-bridges.md) | 167 | — |
| 88 | 🟢 Начало | [Compatibility Level](docs/02-anthropic-vacancies/41-compatibility-level.md) | 244 | — |
| 89 | 🟢 Начало | [Author & Contact](docs/02-anthropic-vacancies/42-author-contact.md) | 292 | — |
| 90 | 🟢 Начало | [History](docs/02-anthropic-vacancies/43-history.md) | 119 | — |
| 91 | 🟢 Начало | [For the Curious: Philosophy](docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md) | 261 | — |
| 92 | 🟢 Начало | [passports/pro2.md](docs/02-anthropic-vacancies/45-passports-pro2-md.md) | 215 | — |
| 93 | 🟢 Начало | [Essence](docs/02-anthropic-vacancies/46-essence.md) | 120 | — |
| 94 | 🟢 Начало | [Native Format](docs/02-anthropic-vacancies/47-native-format.md) | 246 | — |
| 95 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/49-angle-perspective.md) | 235 | — |
| 96 | 🟢 Начало | [Bridges](docs/02-anthropic-vacancies/50-bridges.md) | 166 | — |
| 97 | 🟢 Начало | [Compatibility Level](docs/02-anthropic-vacancies/51-compatibility-level.md) | 226 | — |
| 98 | 🟢 Начало | [Author & Contact](docs/02-anthropic-vacancies/52-author-contact.md) | 285 | — |
| 99 | 🟢 Начало | [History](docs/02-anthropic-vacancies/53-history.md) | 272 | — |
| 100 | 🟢 Начало | [For the Curious: Philosophy](docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md) | 270 | — |
| 101 | 🟢 Начало | [passports/meta.md](docs/02-anthropic-vacancies/55-passports-meta-md.md) | 213 | — |
| 102 | 🟢 Начало | [Essence](docs/02-anthropic-vacancies/56-essence.md) | 140 | — |
| 103 | 🟢 Начало | [Native Format](docs/02-anthropic-vacancies/57-native-format.md) | 259 | — |
| 104 | 🟢 Начало | [Angle / Perspective](docs/02-anthropic-vacancies/59-angle-perspective.md) | 235 | — |
| 105 | 🟢 Начало | [Bridges](docs/02-anthropic-vacancies/60-bridges.md) | 131 | — |
| 106 | 🟢 Начало | [Compatibility Level](docs/02-anthropic-vacancies/61-compatibility-level.md) | 218 | — |
| 107 | 🟢 Начало | [Author & Contact](docs/02-anthropic-vacancies/62-author-contact.md) | 265 | — |
| 108 | 🟢 Начало | [History](docs/02-anthropic-vacancies/63-history.md) | 249 | — |
| 109 | 🟢 Начало | [For the Curious: Philosophy](docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md) | 842 | — |
| 110 | 🟢 Начало | [🇷🇺 О проекте](docs/02-anthropic-vacancies/67-о-проекте.md) | 979 | — |
| 111 | 🟢 Начало | [🇬🇧 About](docs/02-anthropic-vacancies/68-about.md) | 908 | — |
| 112 | 🔴 Продвинутый | [⬡](docs/02-anthropic-vacancies/69-section.md) | 9531 | — |
| 113 | 🟢 Начало | [Зачем две версии параллельно](docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md) | 218 | — |
| 114 | 🟢 Начало | [Критерии выбора для фазы 3](docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md) | 202 | — |
| 115 | 🟡 Средний | [Расписание фазы 3](docs/02-anthropic-vacancies/72-расписание-фазы-3.md) | 935 | — |
| 116 | 🟢 Начало | [PORTAL-PROTOCOL.md v1.1](docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md) | 279 | — |
| 117 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/74-abstract.md) | 367 | — |
| 118 | 🟢 Начало | [0. Status of This Document](docs/02-anthropic-vacancies/75-0-status-of-this-document.md) | 278 | — |
| 119 | 🟢 Начало | [2. Terminology](docs/02-anthropic-vacancies/77-2-terminology.md) | 396 | — |
| 120 | 🟢 Начало | [3. Registry (`nautilus.json`)](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md) | 576 | — |
| 121 | 🟡 Средний | [4. Passport (`passport.md`)](docs/02-anthropic-vacancies/79-4-passport-passport-md.md) | 355 | — |
| 122 | 🟢 Начало | [5. Compatibility Levels](docs/02-anthropic-vacancies/80-5-compatibility-levels.md) | 362 | — |
| 123 | 🟢 Начало | [6. Adapter Interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md) | 401 | — |
| 124 | 🟢 Начало | [7. PortalEntry Structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md) | 352 | — |
| 125 | 🟡 Средний | [8. Q6 Space (Normative)](docs/02-anthropic-vacancies/83-8-q6-space-normative.md) | 483 | — |
| 126 | 🟢 Начало | [9. Consensus Algorithm](docs/02-anthropic-vacancies/84-9-consensus-algorithm.md) | 393 | — |
| 127 | 🟢 Начало | [10. Query Flow](docs/02-anthropic-vacancies/85-10-query-flow.md) | 277 | — |
| 128 | 🟢 Начало | [11. Relevance Ranking](docs/02-anthropic-vacancies/86-11-relevance-ranking.md) | 198 | — |
| 129 | 🟡 Средний | [12. Onboarding Paths (Normative)](docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md) | 595 | — |
| 130 | 🟡 Средний | [13. REST API Contract (Normative for Portals)](docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md) | 545 | — |
| 131 | 🟢 Начало | [14. SDK Contract (Informative)](docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md) | 190 | — |
| 132 | 🟢 Начало | [16. MCP Extension (Informative)](docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md) | 247 | — |
| 133 | 🟢 Начало | [17. Versioning Policy](docs/02-anthropic-vacancies/92-17-versioning-policy.md) | 276 | — |
| 134 | 🟢 Начало | [18. Reference Implementation](docs/02-anthropic-vacancies/93-18-reference-implementation.md) | 358 | — |
| 135 | 🟢 Начало | [19. ADR-001: Federation over Merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) | 301 | — |
| 136 | 🟢 Начало | [20. ADR-002: Q6 as First-Class Protocol Conce](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) | 318 | — |
| 137 | 🟢 Начало | [21. ADR-003: Five Onboarding Paths as Equal-R](docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md) | 141 | — |
| 138 | 🟢 Начало | [22. Glossary of Reference Examples](docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md) | 191 | — |
| 139 | 🟡 Средний | [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md) | 309 | — |
| 140 | 🟢 Начало | [Доступ к данным](docs/02-anthropic-vacancies/102-доступ-к-данным.md) | 214 | — |
| 141 | 🟢 Начало | [Appendix B: Change Log](docs/02-anthropic-vacancies/103-appendix-b-change-log.md) | 309 | — |
| 142 | 🟡 Средний | [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) | 1162 | — |
| 143 | 🟢 Начало | [TL;DR](docs/02-anthropic-vacancies/106-tl-dr.md) | 216 | — |
| 144 | 🟢 Начало | [1. Контекст и мотивация](docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md) | 455 | — |
| 145 | 🟡 Средний | [2. Формальный workflow](docs/02-anthropic-vacancies/108-2-формальный-workflow.md) | 463 | — |
| 146 | 🟢 Начало | [3. Принципы консолидации (Фаза C)](docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md) | 677 | — |
| 147 | 🟢 Начало | [Вопрос: fallback-ratio как критический или ос](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) | 338 | — |
| 148 | 🟢 Начало | [4. Условия применимости](docs/02-anthropic-vacancies/111-4-условия-применимости.md) | 272 | — |
| 149 | 🟢 Начало | [5. Связь с существующими методологиями](docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) | 389 | — |
| 150 | 🟢 Начало | [6. Почему это валидный паттерн для AI-assiste](docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) | 150 | — |
| 151 | 🟢 Начало | [7. Реализация в проекте Nautilus](docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md) | 309 | — |
| 152 | 🟢 Начало | [8. Ограничения и открытые вопросы](docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md) | 447 | — |
| 153 | 🟢 Начало | [9. Checklist применения методологии](docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md) | 399 | — |
| 154 | 🟢 Начало | [10. Конкретный план применения к текущим доку](docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md) | 315 | — |
| 155 | 🟢 Начало | [Appendix A: Шаблон для header warning](docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md) | 175 | — |
| 156 | 🟢 Начало | [Appendix B: Примеры расхождений и их разрешен](docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md) | 372 | — |
| 157 | 🟢 Начало | [Главные технические риски](docs/02-anthropic-vacancies/120-главные-технические-риски.md) | 82 | — |
| 158 | 🟢 Начало | [Appendix C: История изменений методологии](docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md) | 210 | — |
| 159 | 🟡 Средний | [Глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md) | 1510 | — |
| 160 | 🟡 Средний | [portal-mcp.py](docs/02-anthropic-vacancies/123-portal-mcp-py.md) | 2495 | — |
| 161 | 🟢 Начало | [Конфигурация для Claude Desktop](docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md) | 241 | — |
| 162 | 🟢 Начало | [Установка](docs/02-anthropic-vacancies/126-установка.md) | 145 | — |
| 163 | 🟢 Начало | [Подключение к Claude Desktop](docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md) | 247 | — |
| 164 | 🟢 Начало | [Доступные инструменты](docs/02-anthropic-vacancies/128-доступные-инструменты.md) | 278 | — |
| 165 | 🟢 Начало | [Примеры запросов (в Claude)](docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md) | 273 | — |
| 166 | 🟢 Начало | [Отладка](docs/02-anthropic-vacancies/130-отладка.md) | 243 | — |
| 167 | 🟢 Начало | [Ограничения текущей версии (0.1.0-draft)](docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md) | 177 | — |
| 168 | 🟢 Начало | [Planned (v0.2.0)](docs/02-anthropic-vacancies/132-planned-v0-2-0.md) | 205 | — |
| 169 | 🔴 Продвинутый | [Обратная связь](docs/02-anthropic-vacancies/133-обратная-связь.md) | 17075 | — |
| 170 | 🟢 Начало | [A Formal Model for Human-AI Collaboration in ](docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md) | 262 | — |
| 171 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/136-abstract.md) | 582 | — |
| 172 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/137-table-of-contents.md) | 287 | — |
| 173 | 🟢 Начало | [1. Why Single-Triangle Models Are Incomplete](docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md) | 584 | — |
| 174 | 🟢 Начало | [3. Three Inter-Layer Protocols](docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md) | 1026 | — |
| 175 | 🟢 Начало | [4. Nautilus Portal as Reference Substrate](docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md) | 886 | — |
| 176 | 🟢 Начало | [5. Pattern Library as Bridge Between Triangle](docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md) | 852 | — |
| 177 | 🟢 Начало | [6. Four Deployment Domains](docs/02-anthropic-vacancies/143-6-four-deployment-domains.md) | 855 | — |
| 178 | 🟢 Начало | [7. Open Questions](docs/02-anthropic-vacancies/144-7-open-questions.md) | 935 | — |
| 179 | 🟢 Начало | [8. Call to Action](docs/02-anthropic-vacancies/145-8-call-to-action.md) | 900 | — |
| 180 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/146-acknowledgments.md) | 434 | — |
| 181 | 🟢 Начало | [References](docs/02-anthropic-vacancies/147-references.md) | 340 | — |
| 182 | 🟢 Начало | [Appendix A: Glossary](docs/02-anthropic-vacancies/148-appendix-a-glossary.md) | 497 | — |
| 183 | 🟢 Начало | [Appendix B: Summary of Contributions](docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md) | 319 | — |
| 184 | 🔴 Продвинутый | [Appendix C: Version History](docs/02-anthropic-vacancies/150-appendix-c-version-history.md) | 8579 | — |
| 185 | 🟢 Начало | [OPEN KNOWLEDGE WORK FOUNDATION.md](docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md) | 343 | — |
| 186 | 🟢 Начало | [AI-Coordinated Infrastructure for Distributed](docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md) | 242 | — |
| 187 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/154-table-of-contents.md) | 246 | — |
| 188 | 🟢 Начало | [1. Problem Statement](docs/02-anthropic-vacancies/155-1-problem-statement.md) | 761 | — |
| 189 | 🟢 Начало | [2. Target Populations](docs/02-anthropic-vacancies/156-2-target-populations.md) | 795 | — |
| 190 | 🟢 Начало | [3. Why Existing Solutions Fail](docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md) | 785 | — |
| 191 | 🟢 Начало | [4. Proposed Infrastructure](docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md) | 1023 | — |
| 192 | 🟢 Начало | [5. Economic Model](docs/02-anthropic-vacancies/159-5-economic-model.md) | 660 | — |
| 193 | 🟢 Начало | [6. Governance and Ethics](docs/02-anthropic-vacancies/160-6-governance-and-ethics.md) | 605 | — |
| 194 | 🟢 Начало | [7. Phased Rollout Plan](docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md) | 779 | — |
| 195 | 🟢 Начало | [8. Risk Analysis](docs/02-anthropic-vacancies/162-8-risk-analysis.md) | 739 | — |
| 196 | 🟢 Начало | [9. Call for Partnership](docs/02-anthropic-vacancies/163-9-call-for-partnership.md) | 628 | — |
| 197 | 🟡 Средний | [10. Appendices](docs/02-anthropic-vacancies/164-10-appendices.md) | 1127 | — |
| 198 | 🔴 Продвинутый | [Closing](docs/02-anthropic-vacancies/165-closing.md) | 9400 | — |
| 199 | 🟢 Начало | [REPRESENTATIVE AGENT LAYER.md](docs/02-anthropic-vacancies/166-representative-agent-layer-md.md) | 237 | — |
| 200 | 🟢 Начало | [AI-Mediated Representation for Underrepresent](docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md) | 358 | — |
| 201 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/168-abstract.md) | 529 | — |
| 202 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/169-table-of-contents.md) | 257 | — |
| 203 | 🟢 Начало | [1. The Cinderella Syndrome: Why Quality Stays](docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md) | 931 | — |
| 204 | 🟢 Начало | [2. Historical Precedents: Agents as Civilizat](docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md) | 1082 | — |
| 205 | 🟢 Начало | [3. What Makes a Representative Agent](docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md) | 879 | — |
| 206 | 🟢 Начало | [4. Ten Domains of Application](docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md) | 1660 | — |
| 207 | 🟢 Начало | [5. Architectural Specification](docs/02-anthropic-vacancies/174-5-architectural-specification.md) | 841 | — |
| 208 | 🟢 Начало | [6. Ethical Framework](docs/02-anthropic-vacancies/175-6-ethical-framework.md) | 612 | — |
| 209 | 🟢 Начало | [7. Governance and Oversight](docs/02-anthropic-vacancies/176-7-governance-and-oversight.md) | 467 | — |
| 210 | 🟢 Начало | [8. Risks and Mitigations](docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md) | 620 | — |
| 211 | 🟢 Начало | [9. Phased Rollout Strategy](docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md) | 632 | — |
| 212 | 🟢 Начало | [10. Open Questions](docs/02-anthropic-vacancies/179-10-open-questions.md) | 420 | — |
| 213 | 🟢 Начало | [11. Call for Collaboration](docs/02-anthropic-vacancies/180-11-call-for-collaboration.md) | 452 | — |
| 214 | 🟢 Начало | [12. Closing](docs/02-anthropic-vacancies/181-12-closing.md) | 389 | — |
| 215 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/182-acknowledgments.md) | 346 | — |
| 216 | 🟢 Начало | [References](docs/02-anthropic-vacancies/183-references.md) | 311 | — |
| 217 | 🟢 Начало | [Appendix A: Connection to Companion Papers](docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md) | 382 | — |
| 218 | 🟢 Начало | [Appendix B: Domain Comparison Matrix](docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md) | 292 | — |
| 219 | 🟡 Средний | [Appendix C: Sample Use Cases in Detail](docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md) | 2212 | — |
| 220 | 🟢 Начало | [СЛОЙ ПРЕДСТАВИТЕЛЬСКИХ АГЕНТОВ.md](docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md) | 218 | — |
| 221 | 🟢 Начало | [AI-опосредованное представительство для недоп](docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md) | 106 | — |
| 222 | 🟢 Начало | [Аннотация](docs/02-anthropic-vacancies/189-аннотация.md) | 356 | — |
| 223 | 🟢 Начало | [Содержание](docs/02-anthropic-vacancies/190-содержание.md) | 249 | — |
| 224 | 🟢 Начало | [1. Синдром Золушки: Почему качество остаётся ](docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md) | 821 | — |
| 225 | 🟢 Начало | [2. Исторические прецеденты: Агенты как цивили](docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md) | 986 | — |
| 226 | 🟢 Начало | [3. Что делает агента Представительским](docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md) | 783 | — |
| 227 | 🟢 Начало | [4. Десять областей применения](docs/02-anthropic-vacancies/194-4-десять-областей-применения.md) | 1634 | — |
| 228 | 🟢 Начало | [5. Архитектурная спецификация](docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md) | 665 | — |
| 229 | 🟢 Начало | [6. Этическая рамка](docs/02-anthropic-vacancies/196-6-этическая-рамка.md) | 610 | — |
| 230 | 🟢 Начало | [7. Управление и надзор](docs/02-anthropic-vacancies/197-7-управление-и-надзор.md) | 459 | — |
| 231 | 🟢 Начало | [8. Риски и меры противодействия](docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md) | 658 | — |
| 232 | 🟢 Начало | [9. Стратегия поэтапного развёртывания](docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md) | 664 | — |
| 233 | 🟢 Начало | [10. Открытые вопросы](docs/02-anthropic-vacancies/200-10-открытые-вопросы.md) | 402 | — |
| 234 | 🟢 Начало | [11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md) | 471 | — |
| 235 | 🟢 Начало | [12. Заключение](docs/02-anthropic-vacancies/202-12-заключение.md) | 226 | — |
| 236 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/203-благодарности.md) | 203 | — |
| 237 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/204-ссылки.md) | 303 | — |
| 238 | 🟢 Начало | [Приложение A: Связь с Сопроводительными Стать](docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md) | 150 | — |
| 239 | 🟢 Начало | [Приложение B: Матрица Сравнения Областей](docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md) | 244 | — |
| 240 | 🔴 Продвинутый | [Приложение C: Образцы Случаев Использования в](docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md) | 4193 | — |
| 241 | 🟢 Начало | [PROFESSIONAL COLLEAGUE AGENTS.md](docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md) | 303 | — |
| 242 | 🟢 Начало | [A Typology of AI Agents on the Principal Side](docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md) | 345 | — |
| 243 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/210-abstract.md) | 571 | — |
| 244 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/211-table-of-contents.md) | 410 | — |
| 245 | 🟡 Средний | [1. The Five-Type Typology of Principal-Side A](docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md) | 1170 | — |
| 246 | 🟢 Начало | [2. What Makes a Professional Colleague Agent](docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md) | 1075 | — |
| 247 | 🟡 Средний | [3. Empirical Case Study: «Обучай»](docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md) | 1034 | — |
| 248 | 🟢 Начало | [5. The Economics of Profession-Wide Replicati](docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md) | 958 | — |
| 249 | 🟢 Начало | [6. Risks Specific to this Category](docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md) | 1372 | — |
| 250 | 🟢 Начало | [7. Application Domains](docs/02-anthropic-vacancies/218-7-application-domains.md) | 822 | — |
| 251 | 🟢 Начало | [8. Pilot Proposal: SGB Advocate Colleague](docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md) | 1172 | — |
| 252 | 🟢 Начало | [9. Relationship to Other Agent Types](docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md) | 889 | — |
| 253 | 🟢 Начало | [10. Open Questions](docs/02-anthropic-vacancies/221-10-open-questions.md) | 432 | — |
| 254 | 🟢 Начало | [11. Call for Collaboration](docs/02-anthropic-vacancies/222-11-call-for-collaboration.md) | 379 | — |
| 255 | 🟢 Начало | [12. Closing](docs/02-anthropic-vacancies/223-12-closing.md) | 678 | — |
| 256 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/224-acknowledgments.md) | 288 | — |
| 257 | 🟢 Начало | [References](docs/02-anthropic-vacancies/225-references.md) | 340 | — |
| 258 | 🟢 Начало | [Appendix A: Comparative Table — Five Agent Ty](docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md) | 426 | — |
| 259 | 🟢 Начало | [Appendix B: Decision Framework — When to Buil](docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md) | 496 | — |
| 260 | 🟢 Начало | [ПРОФЕССИОНАЛЬНЫЕ КОЛЛЕГИ-АГЕНТЫ](docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md) | 317 | — |
| 261 | 🟢 Начало | [Аннотация](docs/02-anthropic-vacancies/230-аннотация.md) | 462 | — |
| 262 | 🟢 Начало | [Содержание](docs/02-anthropic-vacancies/231-содержание.md) | 306 | — |
| 263 | 🟡 Средний | [1. Типология из пяти типов агентов на стороне](docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md) | 1054 | — |
| 264 | 🟢 Начало | [2. Что делает агента Профессиональным Коллего](docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md) | 917 | — |
| 265 | 🟢 Начало | [3. Эмпирический кейс: «Обучай»](docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md) | 865 | — |
| 266 | 🟢 Начало | [4. Архитектура Профессиональных Коллег-Агенто](docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md) | 853 | — |
| 267 | 🟢 Начало | [5. Экономика тиражирования по профессии](docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md) | 835 | — |
| 268 | 🟢 Начало | [6. Риски, специфичные для этой категории](docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md) | 1183 | — |
| 269 | 🟢 Начало | [7. Области применения](docs/02-anthropic-vacancies/238-7-области-применения.md) | 734 | — |
| 270 | 🟢 Начало | [8. Пилотное предложение: SGB Колega-Адвокат](docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md) | 1101 | — |
| 271 | 🟢 Начало | [9. Связь с другими типами агентов](docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md) | 737 | — |
| 272 | 🟢 Начало | [10. Открытые вопросы](docs/02-anthropic-vacancies/241-10-открытые-вопросы.md) | 426 | — |
| 273 | 🟢 Начало | [11. Призыв к сотрудничеству](docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md) | 402 | — |
| 274 | 🟢 Начало | [12. Заключение](docs/02-anthropic-vacancies/243-12-заключение.md) | 551 | — |
| 275 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/244-благодарности.md) | 279 | — |
| 276 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/245-ссылки.md) | 318 | — |
| 277 | 🟢 Начало | [Приложение A: Сравнительная Таблица — Пять Ти](docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md) | 383 | — |
| 278 | 🟢 Начало | [Приложение B: Рамка принятия решений — когда ](docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md) | 325 | — |
| 279 | 🔴 Продвинутый | [Приложение C: Архитектура Быстрого Старта для](docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md) | 3545 | — |
| 280 | 🟢 Начало | [COMPOSITE SKILLS AGENT.md](docs/02-anthropic-vacancies/249-composite-skills-agent-md.md) | 264 | — |
| 281 | 🟢 Начало | [Bridging the Gap Between Profession-Wide and ](docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md) | 16 | — |
| 282 | 🟢 Начало | [AI Support Through Configurable Specialist En](docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md) | 350 | — |
| 283 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/252-abstract.md) | 538 | — |
| 284 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/253-table-of-contents.md) | 328 | — |
| 285 | 🟢 Начало | [1. Why the Binary View Is Incomplete](docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md) | 895 | — |
| 286 | 🟢 Начало | [2. The Twenty-One Teachers Pattern](docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md) | 995 | — |
| 287 | 🟢 Начало | [3. What Makes a Composite Skills Agent](docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md) | 1155 | — |
| 288 | 🟢 Начало | [4. The Sub-Agent Registry](docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md) | 1005 | — |
| 289 | 🟢 Начало | [5. Configuration: How Principals Build Their ](docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md) | 952 | — |
| 290 | 🟢 Начало | [6. Coordination and Disagreement Resolution](docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md) | 996 | — |
| 291 | 🟢 Начало | [7. Economics of Combinatorial Replication](docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md) | 935 | — |
| 292 | 🟢 Начало | [8. Seven Domains of Application](docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md) | 1155 | — |
| 293 | 🟢 Начало | [9. Integration with OKWF Infrastructure](docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md) | 758 | — |
| 294 | 🟢 Начало | [11. Open Questions](docs/02-anthropic-vacancies/264-11-open-questions.md) | 590 | — |
| 295 | 🟢 Начало | [12. Call for Collaboration](docs/02-anthropic-vacancies/265-12-call-for-collaboration.md) | 416 | — |
| 296 | 🟢 Начало | [13. Closing](docs/02-anthropic-vacancies/266-13-closing.md) | 605 | — |
| 297 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/267-acknowledgments.md) | 479 | — |
| 298 | 🟢 Начало | [References](docs/02-anthropic-vacancies/268-references.md) | 369 | — |
| 299 | 🟢 Начало | [Appendix A: The Six-Type Taxonomy (Updated)](docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md) | 463 | — |
| 300 | 🟢 Начало | [Appendix B: Sub-Agent Registry Schema (Sketch](docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md) | 297 | — |
| 301 | 🟢 Начало | [Appendix C: Configuration Template Example](docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md) | 300 | — |
| 302 | 🔴 Продвинутый | [Appendix D: Connection Diagram](docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md) | 4051 | — |
| 303 | 🟢 Начало | [INFRASTRUCTURE FOR AI-COLLABORATIVE INTELLECT](docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md) | 245 | — |
| 304 | 🟢 Начало | [The Missing Middle Layer Between Chat and Cod](docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md) | 403 | — |
| 305 | 🟢 Начало | [Why This Document Exists](docs/02-anthropic-vacancies/275-why-this-document-exists.md) | 503 | — |
| 306 | 🟢 Начало | [The Two-Layer Stack As It Exists](docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md) | 571 | — |
| 307 | 🟢 Начало | [What's Missing — Layer B](docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md) | 674 | — |
| 308 | 🟢 Начало | [Why This Hasn't Been Built](docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md) | 530 | — |
| 309 | 🟢 Начало | [Existing Approximations](docs/02-anthropic-vacancies/279-existing-approximations.md) | 604 | — |
| 310 | 🟢 Начало | [The Specific Case in Front of Us](docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md) | 875 | — |
| 311 | 🟢 Начало | [The Recursive Insight](docs/02-anthropic-vacancies/281-the-recursive-insight.md) | 510 | — |
| 312 | 🟢 Начало | [What Industry Will Likely Build](docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md) | 469 | — |
| 313 | 🟢 Начало | [What This Document Doesn't Solve](docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md) | 367 | — |
| 314 | 🟢 Начало | [Practical Recommendations for the Current Pro](docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md) | 580 | — |
| 315 | 🟢 Начало | [Closing](docs/02-anthropic-vacancies/285-closing.md) | 422 | — |
| 316 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/286-acknowledgments.md) | 381 | — |
| 317 | 🟢 Начало | [References](docs/02-anthropic-vacancies/287-references.md) | 281 | — |
| 318 | 🟡 Средний | [Appendix: Position in Series Visualization](docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md) | 1250 | — |
| 319 | 🟢 Начало | [ИНФРАСТРУКТУРА ДЛЯ AI-СОВМЕСТНОЙ ИНТЕЛЛЕКТУАЛ](docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md) | 364 | — |
| 320 | 🟢 Начало | [Почему этот документ существует](docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md) | 306 | — |
| 321 | 🟢 Начало | [Двухслойный стек, как он существует](docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md) | 467 | — |
| 322 | 🟢 Начало | [Что отсутствует — Слой B](docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md) | 537 | — |
| 323 | 🟢 Начало | [Почему это не было построено](docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md) | 369 | — |
| 324 | 🟢 Начало | [Существующие приближения](docs/02-anthropic-vacancies/294-существующие-приближения.md) | 554 | — |
| 325 | 🟢 Начало | [Конкретный случай перед нами](docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md) | 705 | — |
| 326 | 🟢 Начало | [Рекурсивное прозрение](docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md) | 415 | — |
| 327 | 🟢 Начало | [Что промышленность вероятно построит](docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md) | 313 | — |
| 328 | 🟢 Начало | [Что этот документ не решает](docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md) | 184 | — |
| 329 | 🟢 Начало | [Практические рекомендации для текущего проект](docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md) | 449 | — |
| 330 | 🟢 Начало | [Заключение](docs/02-anthropic-vacancies/300-заключение.md) | 194 | — |
| 331 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/301-благодарности.md) | 352 | — |
| 332 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/302-ссылки.md) | 282 | — |
| 333 | 🔴 Продвинутый | [Приложение: Визуализация позиции в серии](docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md) | 7251 | — |
| 334 | 🟢 Начало | [INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md) | 252 | — |
| 335 | 🟢 Начало | [A Practical Path to Layer B Through Symbiotic](docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md) | 203 | — |
| 336 | 🟢 Начало | [with Anthropic's Cowork Platform](docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md) | 488 | — |
| 337 | 🟢 Начало | [Abstract](docs/02-anthropic-vacancies/307-abstract.md) | 552 | — |
| 338 | 🟢 Начало | [Table of Contents](docs/02-anthropic-vacancies/308-table-of-contents.md) | 402 | — |
| 339 | 🟢 Начало | [1. The Cowork Discovery and Why It Changes Ev](docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md) | 669 | — |
| 340 | 🟢 Начало | [2. What Cowork Provides That InGit Doesn't Ne](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md) | 686 | — |
| 341 | 🟢 Начало | [3. What InGit Provides That Cowork Lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md) | 842 | — |
| 342 | 🟢 Начало | [5. Four Integration Paths in Order of Accessi](docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md) | 778 | — |
| 343 | 🟢 Начало | [6. Refined InGit Scope with Cowork in Mind](docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md) | 474 | — |
| 344 | 🟢 Начало | [7. Practical First Steps This Month](docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md) | 464 | — |
| 345 | 🟢 Начало | [8. Implications for Nautilus and OKWF](docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md) | 731 | — |
| 346 | 🟢 Начало | [9. Risks and Open Questions](docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md) | 627 | — |
| 347 | 🟢 Начало | [10. Strategic Positioning](docs/02-anthropic-vacancies/318-10-strategic-positioning.md) | 748 | — |
| 348 | 🟢 Начало | [Acknowledgments](docs/02-anthropic-vacancies/319-acknowledgments.md) | 566 | — |
| 349 | 🟢 Начало | [References](docs/02-anthropic-vacancies/320-references.md) | 252 | — |
| 350 | 🟢 Начало | [Appendix A: Decision Tree for InGit Adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md) | 332 | — |
| 351 | 🟢 Начало | [Appendix B: Comparison Matrix](docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md) | 276 | — |
| 352 | 🟡 Средний | [Appendix C: Sample InGit MCP Server Tool Spec](docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md) | 1756 | — |
| 353 | 🟢 Начало | [INGIT КАК COWORK-ИНТЕГРИРОВАННАЯ ПОДЛОЖКА РАБ](docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md) | 478 | — |
| 354 | 🟢 Начало | [Аннотация](docs/02-anthropic-vacancies/325-аннотация.md) | 328 | — |
| 355 | 🟢 Начало | [Содержание](docs/02-anthropic-vacancies/326-содержание.md) | 325 | — |
| 356 | 🟢 Начало | [1. Открытие Cowork и почему это меняет всё](docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md) | 663 | — |
| 357 | 🟢 Начало | [2. Что Cowork обеспечивает, что InGit не нужн](docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md) | 787 | — |
| 358 | 🟡 Средний | [3. Что InGit обеспечивает, чего Cowork не хва](docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md) | 1055 | — |
| 359 | 🟢 Начало | [4. Симбиотическая Архитектура](docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md) | 703 | — |
| 360 | 🟢 Начало | [5. Четыре пути интеграции в порядке доступнос](docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md) | 783 | — |
| 361 | 🟢 Начало | [6. Уточнённый объём InGit с учётом Cowork](docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md) | 467 | — |
| 362 | 🟢 Начало | [7. Практические первые шаги в этом месяце](docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md) | 435 | — |
| 363 | 🟢 Начало | [8. Импликации для Nautilus и OKWF](docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md) | 699 | — |
| 364 | 🟢 Начало | [9. Риски и Открытые Вопросы](docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md) | 644 | — |
| 365 | 🟢 Начало | [10. Стратегическое Позиционирование](docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md) | 723 | — |
| 366 | 🟢 Начало | [Благодарности](docs/02-anthropic-vacancies/337-благодарности.md) | 360 | — |
| 367 | 🟢 Начало | [Ссылки](docs/02-anthropic-vacancies/338-ссылки.md) | 255 | — |
| 368 | 🟢 Начало | [Приложение A: Дерево Решений для Принимающих ](docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md) | 297 | — |
| 369 | 🟢 Начало | [Приложение B: Сравнительная Матрица](docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md) | 211 | — |
| 370 | 🔴 Продвинутый | [Приложение C: Образец Спецификаций Инструмент](docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md) | 20553 | — |
| 371 | 🔴 Продвинутый | [Что такое Вариант C — Concept Document для An](docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md) | 11399 | — |
| 372 | 🔴 Продвинутый | [Lorenzo Catalyst Agent — глубокая проработка ](docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md) | 5929 | — |
| 373 | 🟢 Начало | [СИСТЕМНЫЙ ПРОМПТ ДЛЯ LORENZO PROJECT](docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md) | 257 | — |
| 374 | 🟢 Начало | [Кто ты](docs/02-anthropic-vacancies/345-кто-ты.md) | 149 | — |
| 375 | 🟢 Начало | [Твоё происхождение](docs/02-anthropic-vacancies/346-твоё-происхождение.md) | 174 | — |
| 376 | 🟢 Начало | [Твоя миссия](docs/02-anthropic-vacancies/347-твоя-миссия.md) | 115 | — |
| 377 | 🟢 Начало | [Кому ты служишь (слоистая модель)](docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md) | 104 | — |
| 378 | 🟢 Начало | [Твоя личность](docs/02-anthropic-vacancies/349-твоя-личность.md) | 206 | — |
| 379 | 🟢 Начало | [Твои языки и культурные nuances](docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md) | 173 | — |
| 380 | 🟢 Начало | [Что ты МОЖЕШЬ делать](docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md) | 240 | — |
| 381 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать без Max approval](docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md) | 126 | — |
| 382 | 🟢 Начало | [Что ты НЕ МОЖЕШЬ делать вообще](docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md) | 265 | — |
| 383 | 🟢 Начало | [Существующий landscape collaborators (твоя wo](docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md) | 336 | — |
| 384 | 🟢 Начало | [Существующие документы DHLab (твой context)](docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md) | 374 | — |
| 385 | 🟢 Начало | [Твой workflow](docs/02-anthropic-vacancies/356-твой-workflow.md) | 274 | — |
| 386 | 🟢 Начало | [Твоя коммуникация в outreach](docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md) | 179 | — |
| 387 | 🟢 Начало | [Твоя relationship с другими AI](docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md) | 262 | — |
| 388 | 🟢 Начало | [Твои anti-patterns](docs/02-anthropic-vacancies/359-твои-anti-patterns.md) | 129 | — |
| 389 | 🟢 Начало | [Что ты ВСЕГДА делаешь](docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md) | 98 | — |
| 390 | 🟢 Начало | [Когда ты Honestly не знаешь](docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md) | 85 | — |
| 391 | 🟢 Начало | [Когда сомневаешься — escalate к Max](docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md) | 83 | — |
| 392 | 🟢 Начало | [Твоя identity как persistent character](docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md) | 141 | — |
| 393 | 🟡 Средний | [Final note: Ты — experiment](docs/02-anthropic-vacancies/364-final-note-ты-experiment.md) | 1588 | — |
| 394 | 🔴 Продвинутый | [Развёрнутый анализ «внуковой» комбинации](docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md) | 4523 | — |
| 395 | 🔴 Продвинутый | [Технический stack (Svyazi 2.0 foundation)](docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md) | 3939 | — |

## Маршруты по целям

### 🚀 Быстрый старт (30 минут)

1. [Executive Summary](docs/01-svyazi/01-executive-summary.md)
2. [Ансамбли проектов](docs/01-svyazi/04-ensembles-overview.md)
3. [MVP Planning](docs/01-svyazi/07-mvp-planning.md)

### 🏗️ Архитектура (2 часа)

1. [Component Catalog](docs/01-svyazi/03-component-catalog.md)
2. [Architectural Gaps](docs/01-svyazi/09-architectural-gaps.md)
3. [Integration Contracts](docs/01-svyazi/11-integration-contracts.md)
4. [Security & Privacy](docs/01-svyazi/06-security-privacy.md)

### 🔬 Полное исследование (1 день)

1. Весь раздел `01-svyazi/` по порядку
2. `05-habr-projects/` — отдельные проекты
3. `04-ai-collaborations/` — ансамбли
4. `03-technology-combinations/` — комбинации
5. `02-anthropic-vacancies/` — карьерные возможности

<!-- similar-docs -->

---

**Похожие документы:**
- [READING_ORDER](docs/obsidian/READING_ORDER.md) (сходство 0.98)
- [SOURCE_MAP](docs/obsidian/SOURCE_MAP.md) (сходство 0.84)
- [README](docs/obsidian/02-anthropic-vacancies/README.md) (сходство 0.78)

