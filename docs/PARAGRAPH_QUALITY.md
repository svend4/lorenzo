# Качество абзацев

<!-- summary -->
> _абзац: 698, Оборванный: 537, начала: 205, Дубль: 4_
**Проекты:** Svyazi, LiteParse, Yodoca, MemNet, agent-memory-mcp, Wikontic, Yjs, Automerge

---

<!-- toc -->
## Содержание

- [Типы проблем](#типы-проблем)
- [По файлам](#по-файлам)
  - [`docs/CONCEPTS.md` (1444 проблем)](#docsconceptsmd-1444-проблем)
  - [`docs/TABLES.md` (1109 проблем)](#docstablesmd-1109-проблем)
  - [`docs/TABLES.md` (910 проблем)](#docstablesmd-910-проблем)
  - [`docs/QA.md` (186 проблем)](#docsqamd-186-проблем)
  - [`docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md` (218 проблем)](#docsnautiluscommunity-discussionsagent-changes-reality01-response-enmd-218-проблем)
  - [`docs/nautilus/transmission-box/01-completing-loop.md` (183 проблем)](#docsnautilustransmission-box01-completing-loopmd-183-проблем)
  - [`docs/lorenzo-agent/naming/03-dhlab-umbrella.md` (167 проблем)](#docslorenzo-agentnaming03-dhlab-umbrellamd-167-проблем)
  - [`docs/QA.md` (165 проблем)](#docsqamd-165-проблем)
  - [`docs/lorenzo-agent/scenarios/01-response.md` (164 проблем)](#docslorenzo-agentscenarios01-responsemd-164-проблем)
  - [`docs/QUESTIONS.md` (160 проблем)](#docsquestionsmd-160-проблем)
  - [`docs/lorenzo-agent/specification/11-difficulties-and-recommendations.md` (160 проблем)](#docslorenzo-agentspecification11-difficulties-and-recommendationsmd-160-проблем)
  - [`docs/nautilus/multi-tier-architecture/01-strategic-significance.md` (144 проблем)](#docsnautilusmulti-tier-architecture01-strategic-significancemd-144-проблем)
  - [`docs/SIMILAR_PASSAGES.md` (128 проблем)](#docssimilar_passagesmd-128-проблем)
  - [`docs/DUPLICATES.md` (127 проблем)](#docsduplicatesmd-127-проблем)
  - [`docs/CONTRADICTIONS.md` (117 проблем)](#docscontradictionsmd-117-проблем)
  - [`docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md` (123 проблем)](#docslorenzo-agentnaming02-naming-rationale-lorenzo-medicimd-123-проблем)
  - [`docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` (94 проблем)](#docs02-anthropic-vacancies342-что-такое-вариант-c-concept-document-для-anthropicmd-94-проблем)
  - [`docs/DUPLICATES.md` (92 проблем)](#docsduplicatesmd-92-проблем)
  - [`docs/CLUSTERS.md` (79 проблем)](#docsclustersmd-79-проблем)
  - [`docs/DECISIONS.md` (75 проблем)](#docsdecisionsmd-75-проблем)
  - [`docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` (69 проблем)](#docs02-anthropic-vacancies341-приложение-c-образец-спецификаций-инструментов-ingmd-69-проблем)
  - [`docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` (69 проблем)](#docs02-anthropic-vacancies343-lorenzo-catalyst-agent-глубокая-проработка-специфиmd-69-проблем)
  - [`docs/SPELLCHECK.md` (63 проблем)](#docsspellcheckmd-63-проблем)
  - [`docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` (58 проблем)](#docs02-anthropic-vacancies01-интегральный-анализ-профиля-svend4md-58-проблем)
  - [`docs/04-ai-collaborations/00-intro.md` (49 проблем)](#docs04-ai-collaborations00-intromd-49-проблем)
  - [`docs/02-anthropic-vacancies/QA.md` (47 проблем)](#docs02-anthropic-vacanciesqamd-47-проблем)
  - [`docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` (46 проблем)](#docs02-anthropic-vacancies219-8-pilot-proposal-sgb-advocate-colleaguemd-46-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/13-reprioritization.md` (44 проблем)](#docsanthropic-vacancieshermes-comparison13-reprioritizationmd-44-проблем)
  - [`docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` (45 проблем)](#docs02-anthropic-vacancies217-6-risks-specific-to-this-categorymd-45-проблем)
  - [`docs/02-anthropic-vacancies/218-7-application-domains.md` (45 проблем)](#docs02-anthropic-vacancies218-7-application-domainsmd-45-проблем)
  - [`docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` (44 проблем)](#docs02-anthropic-vacancies237-6-риски-специфичные-для-этой-категорииmd-44-проблем)
  - [`docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` (43 проблем)](#docs02-anthropic-vacancies212-1-the-five-type-typology-of-principal-side-agentsmd-43-проблем)
  - [`docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` (42 проблем)](#docs02-anthropic-vacancies239-8-пилотное-предложение-sgb-колega-адвокатmd-42-проблем)
  - [`docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` (41 проблем)](#docs02-anthropic-vacancies157-3-why-existing-solutions-failmd-41-проблем)
  - [`docs/02-anthropic-vacancies/165-closing.md` (41 проблем)](#docs02-anthropic-vacancies165-closingmd-41-проблем)
  - [`docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` (40 проблем)](#docs02-anthropic-vacancies232-1-типология-из-пяти-типов-агентов-на-стороне-принцmd-40-проблем)
  - [`docs/05-habr-projects/memory/memnet.md` (40 проблем)](#docs05-habr-projectsmemorymemnetmd-40-проблем)
  - [`docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` (38 проблем)](#docs02-anthropic-vacancies158-4-proposed-infrastructuremd-38-проблем)
  - [`docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` (38 проблем)](#docs02-anthropic-vacancies173-4-ten-domains-of-applicationmd-38-проблем)
  - [`docs/02-anthropic-vacancies/238-7-области-применения.md` (37 проблем)](#docs02-anthropic-vacancies238-7-области-примененияmd-37-проблем)
  - [`docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` (36 проблем)](#docs02-anthropic-vacancies194-4-десять-областей-примененияmd-36-проблем)
  - [`docs/02-anthropic-vacancies/69-section.md` (36 проблем)](#docs02-anthropic-vacancies69-sectionmd-36-проблем)
  - [`docs/01-svyazi/04-ensembles-overview.md` (35 проблем)](#docs01-svyazi04-ensembles-overviewmd-35-проблем)
  - [`docs/04-ai-collaborations/QA.md` (35 проблем)](#docs04-ai-collaborationsqamd-35-проблем)
  - [`docs/01-svyazi/QA.md` (34 проблем)](#docs01-svyaziqamd-34-проблем)
  - [`docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` (34 проблем)](#docs02-anthropic-vacancies312-4-the-symbiotic-architecturemd-34-проблем)
  - [`docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` (33 проблем)](#docs02-anthropic-vacancies186-appendix-c-sample-use-cases-in-detailmd-33-проблем)
  - [`docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` (33 проблем)](#docs02-anthropic-vacancies256-3-what-makes-a-composite-skills-agentmd-33-проблем)
  - [`docs/02-anthropic-vacancies/68-about.md` (33 проблем)](#docs02-anthropic-vacancies68-aboutmd-33-проблем)
  - [`docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` (32 проблем)](#docs02-anthropic-vacancies365-развёрнутый-анализ-внуковой-комбинацииmd-32-проблем)
  - [`docs/01-svyazi/01-executive-summary.md` (31 проблем)](#docs01-svyazi01-executive-summarymd-31-проблем)
  - [`docs/04-ai-collaborations/04-приоритетные-ансамбли.md` (31 проблем)](#docs04-ai-collaborations04-приоритетные-ансамблиmd-31-проблем)
  - [`docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` (31 проблем)](#docs04-ai-collaborations11-интеграционный-контракт-который-стоит-зафиксироватmd-31-проблем)
  - [`docs/02-anthropic-vacancies/150-appendix-c-version-history.md` (30 проблем)](#docs02-anthropic-vacancies150-appendix-c-version-historymd-30-проблем)
  - [`docs/02-anthropic-vacancies/159-5-economic-model.md` (30 проблем)](#docs02-anthropic-vacancies159-5-economic-modelmd-30-проблем)
  - [`docs/02-anthropic-vacancies/163-9-call-for-partnership.md` (30 проблем)](#docs02-anthropic-vacancies163-9-call-for-partnershipmd-30-проблем)
  - [`docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` (30 проблем)](#docs02-anthropic-vacancies207-приложение-c-образцы-случаев-использования-в-деталmd-30-проблем)
  - [`docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` (30 проблем)](#docs02-anthropic-vacancies313-5-four-integration-paths-in-order-of-accessibilitymd-30-проблем)
  - [`docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` (30 проблем)](#docs02-anthropic-vacancies331-5-четыре-пути-интеграции-в-порядке-доступностиmd-30-проблем)
  - [`docs/02-anthropic-vacancies/67-о-проекте.md` (30 проблем)](#docs02-anthropic-vacancies67-о-проектеmd-30-проблем)
  - [`docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` (30 проблем)](#docs04-ai-collaborations14-ограничения-лицензии-и-что-пока-лучше-не-склеиватьmd-30-проблем)
  - [`docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` (29 проблем)](#docs02-anthropic-vacancies248-приложение-c-архитектура-быстрого-старта-для-sgb-аmd-29-проблем)
  - [`docs/RISK_REGISTER.md` (29 проблем)](#docsrisk_registermd-29-проблем)
  - [`docs/02-anthropic-vacancies/133-обратная-связь.md` (28 проблем)](#docs02-anthropic-vacancies133-обратная-связьmd-28-проблем)
  - [`docs/02-anthropic-vacancies/164-10-appendices.md` (28 проблем)](#docs02-anthropic-vacancies164-10-appendicesmd-28-проблем)
  - [`docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` (28 проблем)](#docs02-anthropic-vacancies213-2-what-makes-a-professional-colleague-agentmd-28-проблем)
  - [`docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` (28 проблем)](#docs02-anthropic-vacancies315-7-practical-first-steps-this-monthmd-28-проблем)
  - [`docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` (28 проблем)](#docs04-ai-collaborations05-план-прототипа-и-возможные-контактыmd-28-проблем)
  - [`docs/02-anthropic-vacancies/00-intro.md` (27 проблем)](#docs02-anthropic-vacancies00-intromd-27-проблем)
  - [`docs/02-anthropic-vacancies/162-8-risk-analysis.md` (27 проблем)](#docs02-anthropic-vacancies162-8-risk-analysismd-27-проблем)
  - [`docs/02-anthropic-vacancies/179-10-open-questions.md` (27 проблем)](#docs02-anthropic-vacancies179-10-open-questionsmd-27-проблем)
  - [`docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` (27 проблем)](#docs02-anthropic-vacancies236-5-экономика-тиражирования-по-профессииmd-27-проблем)
  - [`docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` (27 проблем)](#docs02-anthropic-vacancies366-технический-stack-svyazi-2-0-foundationmd-27-проблем)
  - [`docs/01-svyazi/07-mvp-planning.md` (26 проблем)](#docs01-svyazi07-mvp-planningmd-26-проблем)
  - [`docs/02-anthropic-vacancies/148-appendix-a-glossary.md` (26 проблем)](#docs02-anthropic-vacancies148-appendix-a-glossarymd-26-проблем)
  - [`docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` (26 проблем)](#docs02-anthropic-vacancies160-6-governance-and-ethicsmd-26-проблем)
  - [`docs/02-anthropic-vacancies/174-5-architectural-specification.md` (26 проблем)](#docs02-anthropic-vacancies174-5-architectural-specificationmd-26-проблем)
  - [`docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` (26 проблем)](#docs02-anthropic-vacancies216-5-the-economics-of-profession-wide-replicationmd-26-проблем)
  - [`docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` (26 проблем)](#docs02-anthropic-vacancies330-4-симбиотическая-архитектураmd-26-проблем)
  - [`docs/TAGS.md` (26 проблем)](#docstagsmd-26-проблем)
  - [`docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` (25 проблем)](#docs02-anthropic-vacancies08-3-registry-nautilus-jsonmd-25-проблем)
  - [`docs/02-anthropic-vacancies/156-2-target-populations.md` (25 проблем)](#docs02-anthropic-vacancies156-2-target-populationsmd-25-проблем)
  - [`docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` (25 проблем)](#docs02-anthropic-vacancies176-7-governance-and-oversightmd-25-проблем)
  - [`docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` (25 проблем)](#docs02-anthropic-vacancies177-8-risks-and-mitigationsmd-25-проблем)
  - [`docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` (25 проблем)](#docs02-anthropic-vacancies195-5-архитектурная-спецификацияmd-25-проблем)
  - [`docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` (25 проблем)](#docs02-anthropic-vacancies314-6-refined-ingit-scope-with-cowork-in-mindmd-25-проблем)
  - [`docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` (25 проблем)](#docs02-anthropic-vacancies364-final-note-ты-experimentmd-25-проблем)
  - [`docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` (25 проблем)](#docs02-anthropic-vacancies78-3-registry-nautilus-jsonmd-25-проблем)
  - [`docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` (25 проблем)](#docs04-ai-collaborations03-карта-найденных-проектов-и-паттерновmd-25-проблем)
  - [`docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` (25 проблем)](#docs04-ai-collaborations10-новые-ансамбли-следующего-шагаmd-25-проблем)
  - [`docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` (25 проблем)](#docs04-ai-collaborations13-контактная-стратегия-и-узкие-вопросы-для-авторовmd-25-проблем)
  - [`docs/01-svyazi/10-second-order-ensembles.md` (24 проблем)](#docs01-svyazi10-second-order-ensemblesmd-24-проблем)
  - [`docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` (24 проблем)](#docs02-anthropic-vacancies02-общий-план-развития-nautilus-portal-protocolmd-24-проблем)
  - [`docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` (24 проблем)](#docs02-anthropic-vacancies139-2-the-double-triangle-architecturemd-24-проблем)
  - [`docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` (24 проблем)](#docs02-anthropic-vacancies178-9-phased-rollout-strategymd-24-проблем)
  - [`docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` (24 проблем)](#docs02-anthropic-vacancies228-appendix-c-quick-start-architecture-for-sgb-advocamd-24-проблем)
  - [`docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` (24 проблем)](#docs02-anthropic-vacancies233-2-что-делает-агента-профессиональным-коллегойmd-24-проблем)
  - [`docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` (24 проблем)](#docs02-anthropic-vacancies240-9-связь-с-другими-типами-агентовmd-24-проблем)
  - [`docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` (24 проблем)](#docs02-anthropic-vacancies257-4-the-sub-agent-registrymd-24-проблем)
  - [`docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` (24 проблем)](#docs02-anthropic-vacancies259-6-coordination-and-disagreement-resolutionmd-24-проблем)
  - [`docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` (24 проблем)](#docs02-anthropic-vacancies272-appendix-d-connection-diagrammd-24-проблем)
  - [`docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` (24 проблем)](#docs02-anthropic-vacancies332-6-уточнённый-объём-ingit-с-учётом-coworkmd-24-проблем)
  - [`docs/02-anthropic-vacancies/90-15-security-considerations.md` (24 проблем)](#docs02-anthropic-vacancies90-15-security-considerationsmd-24-проблем)
  - [`docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` (24 проблем)](#docs04-ai-collaborations06-безопасность-приватность-и-бюджетный-роутингmd-24-проблем)
  - [`docs/01-svyazi/11-integration-contracts.md` (23 проблем)](#docs01-svyazi11-integration-contractsmd-23-проблем)
  - [`docs/01-svyazi/13-contacts.md` (23 проблем)](#docs01-svyazi13-contactsmd-23-проблем)
  - [`docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` (23 проблем)](#docs02-anthropic-vacancies198-8-риски-и-меры-противодействияmd-23-проблем)
  - [`docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` (23 проблем)](#docs02-anthropic-vacancies200-10-открытые-вопросыmd-23-проблем)
  - [`docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` (23 проблем)](#docs02-anthropic-vacancies255-2-the-twenty-one-teachers-patternmd-23-проблем)
  - [`docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` (23 проблем)](#docs02-anthropic-vacancies262-9-integration-with-okwf-infrastructuremd-23-проблем)
  - [`docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` (23 проблем)](#docs02-anthropic-vacancies323-appendix-c-sample-ingit-mcp-server-tool-specificatmd-23-проблем)
  - [`docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` (23 проблем)](#docs02-anthropic-vacancies329-3-что-ingit-обеспечивает-чего-cowork-не-хватаетmd-23-проблем)
  - [`docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` (23 проблем)](#docs02-anthropic-vacancies88-13-rest-api-contract-normative-for-portalsmd-23-проблем)
  - [`docs/04-ai-collaborations/01-executive-summary.md` (23 проблем)](#docs04-ai-collaborations01-executive-summarymd-23-проблем)
  - [`docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` (23 проблем)](#docs04-ai-collaborations09-архитектурные-зазоры-которые-важнее-новых-инструмеmd-23-проблем)
  - [`docs/02-anthropic-vacancies/179-10-open-questions.md` (23 проблем)](#docs02-anthropic-vacancies179-10-open-questionsmd-23-проблем)
  - [`docs/01-svyazi/09-architectural-gaps.md` (22 проблем)](#docs01-svyazi09-architectural-gapsmd-22-проблем)
  - [`docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` (22 проблем)](#docs02-anthropic-vacancies171-2-historical-precedents-agents-as-civilizational-imd-22-проблем)
  - [`docs/02-anthropic-vacancies/175-6-ethical-framework.md` (22 проблем)](#docs02-anthropic-vacancies175-6-ethical-frameworkmd-22-проблем)
  - [`docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` (22 проблем)](#docs02-anthropic-vacancies303-приложение-визуализация-позиции-в-серииmd-22-проблем)
  - [`docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` (22 проблем)](#docs02-anthropic-vacancies311-3-what-ingit-provides-that-cowork-lacksmd-22-проблем)
  - [`docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` (22 проблем)](#docs02-anthropic-vacancies316-8-implications-for-nautilus-and-okwfmd-22-проблем)
  - [`docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` (22 проблем)](#docs02-anthropic-vacancies336-10-стратегическое-позиционированиеmd-22-проблем)
  - [`docs/02-anthropic-vacancies/80-5-compatibility-levels.md` (22 проблем)](#docs02-anthropic-vacancies80-5-compatibility-levelsmd-22-проблем)
  - [`docs/NARRATIVE.md` (22 проблем)](#docsnarrativemd-22-проблем)
  - [`docs/01-svyazi/06-security-privacy.md` (21 проблем)](#docs01-svyazi06-security-privacymd-21-проблем)
  - [`docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` (21 проблем)](#docs02-anthropic-vacancies140-3-three-inter-layer-protocolsmd-21-проблем)
  - [`docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` (21 проблем)](#docs02-anthropic-vacancies143-6-four-deployment-domainsmd-21-проблем)
  - [`docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` (21 проблем)](#docs02-anthropic-vacancies161-7-phased-rollout-planmd-21-проблем)
  - [`docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` (21 проблем)](#docs02-anthropic-vacancies170-1-the-cinderella-syndrome-why-quality-stays-invisimd-21-проблем)
  - [`docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` (21 проблем)](#docs02-anthropic-vacancies172-3-what-makes-a-representative-agentmd-21-проблем)
  - [`docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` (21 проблем)](#docs02-anthropic-vacancies193-3-что-делает-агента-представительскимmd-21-проблем)
  - [`docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` (21 проблем)](#docs02-anthropic-vacancies199-9-стратегия-поэтапного-развёртыванияmd-21-проблем)
  - [`docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` (21 проблем)](#docs02-anthropic-vacancies215-4-architecture-of-professional-colleague-agentsmd-21-проблем)
  - [`docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` (21 проблем)](#docs02-anthropic-vacancies220-9-relationship-to-other-agent-typesmd-21-проблем)
  - [`docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` (21 проблем)](#docs02-anthropic-vacancies227-appendix-b-decision-framework-when-to-build-type-1md-21-проблем)
  - [`docs/02-anthropic-vacancies/279-existing-approximations.md` (21 проблем)](#docs02-anthropic-vacancies279-existing-approximationsmd-21-проблем)
  - [`docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` (21 проблем)](#docs02-anthropic-vacancies317-9-risks-and-open-questionsmd-21-проблем)
  - [`docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` (21 проблем)](#docs02-anthropic-vacancies333-7-практические-первые-шаги-в-этом-месяцеmd-21-проблем)
  - [`docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` (21 проблем)](#docs02-anthropic-vacancies87-12-onboarding-paths-normativemd-21-проблем)
  - [`docs/04-ai-collaborations/07-выводы.md` (21 проблем)](#docs04-ai-collaborations07-выводыmd-21-проблем)
  - [`docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` (21 проблем)](#docs04-ai-collaborations12-дорожная-карта-прототипа-следующей-итерацииmd-21-проблем)
  - [`docs/CITATION_INDEX.md` (21 проблем)](#docscitation_indexmd-21-проблем)
  - [`docs/01-svyazi/02-methodology.md` (20 проблем)](#docs01-svyazi02-methodologymd-20-проблем)
  - [`docs/01-svyazi/12-roadmap.md` (20 проблем)](#docs01-svyazi12-roadmapmd-20-проблем)
  - [`docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` (20 проблем)](#docs02-anthropic-vacancies260-7-economics-of-combinatorial-replicationmd-20-проблем)
  - [`docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` (20 проблем)](#docs02-anthropic-vacancies284-practical-recommendations-for-the-current-projectmd-20-проблем)
  - [`docs/02-anthropic-vacancies/294-существующие-приближения.md` (20 проблем)](#docs02-anthropic-vacancies294-существующие-приближенияmd-20-проблем)
  - [`docs/02-anthropic-vacancies/318-10-strategic-positioning.md` (20 проблем)](#docs02-anthropic-vacancies318-10-strategic-positioningmd-20-проблем)
  - [`docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` (20 проблем)](#docs02-anthropic-vacancies334-8-импликации-для-nautilus-и-okwfmd-20-проблем)
  - [`docs/CONSISTENCY.md` (20 проблем)](#docsconsistencymd-20-проблем)
  - [`docs/ONBOARDING.md` (20 проблем)](#docsonboardingmd-20-проблем)
  - [`docs/01-svyazi/14-limitations.md` (19 проблем)](#docs01-svyazi14-limitationsmd-19-проблем)
  - [`docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` (19 проблем)](#docs02-anthropic-vacancies142-5-pattern-library-as-bridge-between-trianglesmd-19-проблем)
  - [`docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` (19 проблем)](#docs02-anthropic-vacancies214-3-empirical-case-study-обучайmd-19-проблем)
  - [`docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` (19 проблем)](#docs02-anthropic-vacancies247-приложение-b-рамка-принятия-решений-когда-строить-md-19-проблем)
  - [`docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` (19 проблем)](#docs02-anthropic-vacancies263-10-risks-specific-to-composite-architecturesmd-19-проблем)
  - [`docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` (19 проблем)](#docs02-anthropic-vacancies280-the-specific-case-in-front-of-usmd-19-проблем)
  - [`docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` (19 проблем)](#docs02-anthropic-vacancies295-конкретный-случай-перед-намиmd-19-проблем)
  - [`docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` (19 проблем)](#docs02-anthropic-vacancies328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строиmd-19-проблем)
  - [`docs/02-anthropic-vacancies/79-4-passport-passport-md.md` (19 проблем)](#docs02-anthropic-vacancies79-4-passport-passport-mdmd-19-проблем)
  - [`docs/CHANGELOG_AUTO.md` (19 проблем)](#docschangelog_automd-19-проблем)
  - [`docs/INDEX.md` (19 проблем)](#docsindexmd-19-проблем)
  - [`docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md` (19 проблем)](#docslorenzo-agentphased-deployment03-level-2-basic-litemd-19-проблем)
  - [`docs/02-anthropic-vacancies/144-7-open-questions.md` (18 проблем)](#docs02-anthropic-vacancies144-7-open-questionsmd-18-проблем)
  - [`docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` (18 проблем)](#docs02-anthropic-vacancies197-7-управление-и-надзорmd-18-проблем)
  - [`docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` (18 проблем)](#docs02-anthropic-vacancies234-3-эмпирический-кейс-обучайmd-18-проблем)
  - [`docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` (18 проблем)](#docs02-anthropic-vacancies235-4-архитектура-профессиональных-коллег-агентовmd-18-проблем)
  - [`docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` (18 проблем)](#docs02-anthropic-vacancies258-5-configuration-how-principals-build-their-ensemblmd-18-проблем)
  - [`docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` (18 проблем)](#docs02-anthropic-vacancies299-практические-рекомендации-для-текущего-проектаmd-18-проблем)
  - [`docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` (18 проблем)](#docs02-anthropic-vacancies335-9-риски-и-открытые-вопросыmd-18-проблем)
  - [`docs/03-technology-combinations/02-knowledge-graphs.md` (18 проблем)](#docs03-technology-combinations02-knowledge-graphsmd-18-проблем)
  - [`docs/LLM_SUMMARIES.md` (18 проблем)](#docsllm_summariesmd-18-проблем)
  - [`docs/01-svyazi/03-component-catalog.md` (17 проблем)](#docs01-svyazi03-component-catalogmd-17-проблем)
  - [`docs/01-svyazi/08-conclusions.md` (17 проблем)](#docs01-svyazi08-conclusionsmd-17-проблем)
  - [`docs/02-anthropic-vacancies/09-4-passport-passport-md.md` (17 проблем)](#docs02-anthropic-vacancies09-4-passport-passport-mdmd-17-проблем)
  - [`docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` (17 проблем)](#docs02-anthropic-vacancies109-3-принципы-консолидации-фаза-cmd-17-проблем)
  - [`docs/02-anthropic-vacancies/130-отладка.md` (17 проблем)](#docs02-anthropic-vacancies130-отладкаmd-17-проблем)
  - [`docs/02-anthropic-vacancies/18-6-adapter-interface.md` (17 проблем)](#docs02-anthropic-vacancies18-6-adapter-interfacemd-17-проблем)
  - [`docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` (17 проблем)](#docs02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd-17-проблем)
  - [`docs/02-anthropic-vacancies/196-6-этическая-рамка.md` (17 проблем)](#docs02-anthropic-vacancies196-6-этическая-рамкаmd-17-проблем)
  - [`docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` (17 проблем)](#docs02-anthropic-vacancies265-12-call-for-collaborationmd-17-проблем)
  - [`docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` (17 проблем)](#docs02-anthropic-vacancies276-the-two-layer-stack-as-it-existsmd-17-проблем)
  - [`docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` (17 проблем)](#docs02-anthropic-vacancies288-appendix-position-in-series-visualizationmd-17-проблем)
  - [`docs/02-anthropic-vacancies/320-references.md` (17 проблем)](#docs02-anthropic-vacancies320-referencesmd-17-проблем)
  - [`docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` (17 проблем)](#docs02-anthropic-vacancies327-1-открытие-cowork-и-почему-это-меняет-всёmd-17-проблем)
  - [`docs/02-anthropic-vacancies/338-ссылки.md` (17 проблем)](#docs02-anthropic-vacancies338-ссылкиmd-17-проблем)
  - [`docs/02-anthropic-vacancies/356-твой-workflow.md` (17 проблем)](#docs02-anthropic-vacancies356-твой-workflowmd-17-проблем)
  - [`docs/02-anthropic-vacancies/81-6-adapter-interface.md` (17 проблем)](#docs02-anthropic-vacancies81-6-adapter-interfacemd-17-проблем)
  - [`docs/02-anthropic-vacancies/83-8-q6-space-normative.md` (17 проблем)](#docs02-anthropic-vacancies83-8-q6-space-normativemd-17-проблем)
  - [`docs/02-anthropic-vacancies/92-17-versioning-policy.md` (17 проблем)](#docs02-anthropic-vacancies92-17-versioning-policymd-17-проблем)
  - [`docs/03-technology-combinations/QA.md` (17 проблем)](#docs03-technology-combinationsqamd-17-проблем)
  - [`docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` (17 проблем)](#docs04-ai-collaborations08-что-это-продолжение-добавляетmd-17-проблем)
  - [`docs/02-anthropic-vacancies/104-appendix-c-references.md` (16 проблем)](#docs02-anthropic-vacancies104-appendix-c-referencesmd-16-проблем)
  - [`docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` (16 проблем)](#docs02-anthropic-vacancies114-7-реализация-в-проекте-nautilusmd-16-проблем)
  - [`docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` (16 проблем)](#docs02-anthropic-vacancies117-10-конкретный-план-применения-к-текущим-документамmd-16-проблем)
  - [`docs/nautilus/composite-skills-agents/09-okwf-integration.md` (17 проблем)](#docsnautiluscomposite-skills-agents09-okwf-integrationmd-17-проблем)
  - [`docs/nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md` (17 проблем)](#docsnautilusingit-cowork-ru03-chto-ingit-obespechivaetmd-17-проблем)
  - [`docs/technology-combinations/combinations/12-multi-agent-observability-stack.md` (17 проблем)](#docstechnology-combinationscombinations12-multi-agent-observability-stackmd-17-проблем)
  - [`docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md` (17 проблем)](#docstechnology-combinationscombinations26-ast-based-code-analysis-for-legal-automationmd-17-проблем)
  - [`docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md` (17 проблем)](#docstechnology-combinationscombinations29-meta-programmatic-legal-template-generatormd-17-проблем)
  - [`docs/01-svyazi/12-roadmap.md` (16 проблем)](#docs01-svyazi12-roadmapmd-16-проблем)
  - [`docs/02-anthropic-vacancies/122-глоссарий.md` (16 проблем)](#docs02-anthropic-vacancies122-глоссарийmd-16-проблем)
  - [`docs/02-anthropic-vacancies/155-1-problem-statement.md` (16 проблем)](#docs02-anthropic-vacancies155-1-problem-statementmd-16-проблем)
  - [`docs/02-anthropic-vacancies/23-11-security-considerations.md` (16 проблем)](#docs02-anthropic-vacancies23-11-security-considerationsmd-16-проблем)
  - [`docs/02-anthropic-vacancies/264-11-open-questions.md` (16 проблем)](#docs02-anthropic-vacancies264-11-open-questionsmd-16-проблем)
  - [`docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` (16 проблем)](#docs02-anthropic-vacancies309-1-the-cowork-discovery-and-why-it-changes-everythimd-16-проблем)
  - [`docs/02-anthropic-vacancies/48-content-overview.md` (16 проблем)](#docs02-anthropic-vacancies48-content-overviewmd-16-проблем)
  - [`docs/02-anthropic-vacancies/57-native-format.md` (16 проблем)](#docs02-anthropic-vacancies57-native-formatmd-16-проблем)
  - [`docs/02-anthropic-vacancies/85-10-query-flow.md` (16 проблем)](#docs02-anthropic-vacancies85-10-query-flowmd-16-проблем)
  - [`docs/02-anthropic-vacancies/108-2-формальный-workflow.md` (15 проблем)](#docs02-anthropic-vacancies108-2-формальный-workflowmd-15-проблем)
  - [`docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` (15 проблем)](#docs02-anthropic-vacancies141-4-nautilus-portal-as-reference-substratemd-15-проблем)
  - [`docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` (15 проблем)](#docs02-anthropic-vacancies20-8-consensus-algorithmmd-15-проблем)
  - [`docs/02-anthropic-vacancies/21-9-query-flow.md` (15 проблем)](#docs02-anthropic-vacancies21-9-query-flowmd-15-проблем)
  - [`docs/02-anthropic-vacancies/266-13-closing.md` (15 проблем)](#docs02-anthropic-vacancies266-13-closingmd-15-проблем)
  - [`docs/02-anthropic-vacancies/268-references.md` (15 проблем)](#docs02-anthropic-vacancies268-referencesmd-15-проблем)
  - [`docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` (15 проблем)](#docs02-anthropic-vacancies277-what-s-missing-layer-bmd-15-проблем)
  - [`docs/02-anthropic-vacancies/302-ссылки.md` (15 проблем)](#docs02-anthropic-vacancies302-ссылкиmd-15-проблем)
  - [`docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` (15 проблем)](#docs02-anthropic-vacancies306-with-anthropic-s-cowork-platformmd-15-проблем)
  - [`docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` (15 проблем)](#docs02-anthropic-vacancies310-2-what-cowork-provides-that-ingit-doesn-t-need-to-md-15-проблем)
  - [`docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` (15 проблем)](#docs02-anthropic-vacancies324-ingit-как-cowork-интегрированная-подложка-рабочегоmd-15-проблем)
  - [`docs/02-anthropic-vacancies/40-bridges.md` (15 проблем)](#docs02-anthropic-vacancies40-bridgesmd-15-проблем)
  - [`docs/TECH_RADAR.md` (15 проблем)](#docstech_radarmd-15-проблем)
  - [`docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` (14 проблем)](#docs02-anthropic-vacancies107-1-контекст-и-мотивацияmd-14-проблем)
  - [`docs/02-anthropic-vacancies/111-4-условия-применимости.md` (14 проблем)](#docs02-anthropic-vacancies111-4-условия-применимостиmd-14-проблем)
  - [`docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` (14 проблем)](#docs02-anthropic-vacancies138-1-why-single-triangle-models-are-incompletemd-14-проблем)
  - [`docs/02-anthropic-vacancies/17-5-compatibility-levels.md` (14 проблем)](#docs02-anthropic-vacancies17-5-compatibility-levelsmd-14-проблем)
  - [`docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` (14 проблем)](#docs02-anthropic-vacancies191-1-синдром-золушки-почему-качество-остаётся-невидимmd-14-проблем)
  - [`docs/02-anthropic-vacancies/24-12-versioning-policy.md` (14 проблем)](#docs02-anthropic-vacancies24-12-versioning-policymd-14-проблем)
  - [`docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` (14 проблем)](#docs02-anthropic-vacancies254-1-why-the-binary-view-is-incompletemd-14-проблем)
  - [`docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` (14 проблем)](#docs02-anthropic-vacancies278-why-this-hasn-t-been-builtmd-14-проблем)
  - [`docs/02-anthropic-vacancies/319-acknowledgments.md` (14 проблем)](#docs02-anthropic-vacancies319-acknowledgmentsmd-14-проблем)
  - [`docs/02-anthropic-vacancies/76-1-introduction.md` (14 проблем)](#docs02-anthropic-vacancies76-1-introductionmd-14-проблем)
  - [`docs/03-technology-combinations/05-benchmarks.md` (14 проблем)](#docs03-technology-combinations05-benchmarksmd-14-проблем)
  - [`docs/BROKEN_LINKS.md` (14 проблем)](#docsbroken_linksmd-14-проблем)
  - [`docs/autofilled/research-summary.md` (14 проблем)](#docsautofilledresearch-summarymd-14-проблем)
  - [`docs/02-anthropic-vacancies/07-2-terminology.md` (13 проблем)](#docs02-anthropic-vacancies07-2-terminologymd-13-проблем)
  - [`docs/02-anthropic-vacancies/145-8-call-to-action.md` (13 проблем)](#docs02-anthropic-vacancies145-8-call-to-actionmd-13-проблем)
  - [`docs/02-anthropic-vacancies/146-acknowledgments.md` (13 проблем)](#docs02-anthropic-vacancies146-acknowledgmentsmd-13-проблем)
  - [`docs/02-anthropic-vacancies/221-10-open-questions.md` (13 проблем)](#docs02-anthropic-vacancies221-10-open-questionsmd-13-проблем)
  - [`docs/02-anthropic-vacancies/25-13-reference-implementation.md` (13 проблем)](#docs02-anthropic-vacancies25-13-reference-implementationmd-13-проблем)
  - [`docs/02-anthropic-vacancies/267-acknowledgments.md` (13 проблем)](#docs02-anthropic-vacancies267-acknowledgmentsmd-13-проблем)
  - [`docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` (13 проблем)](#docs02-anthropic-vacancies274-the-missing-middle-layer-between-chat-and-codemd-13-проблем)
  - [`docs/02-anthropic-vacancies/287-references.md` (13 проблем)](#docs02-anthropic-vacancies287-referencesmd-13-проблем)
  - [`docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` (13 проблем)](#docs02-anthropic-vacancies289-инфраструктура-для-ai-совместной-интеллектуальной-md-13-проблем)
  - [`docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` (13 проблем)](#docs02-anthropic-vacancies291-двухслойный-стек-как-он-существуетmd-13-проблем)
  - [`docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` (13 проблем)](#docs02-anthropic-vacancies292-что-отсутствует-слой-bmd-13-проблем)
  - [`docs/02-anthropic-vacancies/34-appendix-b-change-log.md` (13 проблем)](#docs02-anthropic-vacancies34-appendix-b-change-logmd-13-проблем)
  - [`docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` (13 проблем)](#docs02-anthropic-vacancies351-что-ты-можешь-делатьmd-13-проблем)
  - [`docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` (13 проблем)](#docs02-anthropic-vacancies355-существующие-документы-dhlab-твой-contextmd-13-проблем)
  - [`docs/02-anthropic-vacancies/37-native-format.md` (13 проблем)](#docs02-anthropic-vacancies37-native-formatmd-13-проблем)
  - [`docs/02-anthropic-vacancies/43-history.md` (13 проблем)](#docs02-anthropic-vacancies43-historymd-13-проблем)
  - [`docs/02-anthropic-vacancies/56-essence.md` (13 проблем)](#docs02-anthropic-vacancies56-essencemd-13-проблем)
  - [`docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` (13 проблем)](#docs02-anthropic-vacancies64-for-the-curious-philosophymd-13-проблем)
  - [`docs/02-anthropic-vacancies/82-7-portalentry-structure.md` (13 проблем)](#docs02-anthropic-vacancies82-7-portalentry-structuremd-13-проблем)
  - [`docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` (13 проблем)](#docs02-anthropic-vacancies84-9-consensus-algorithmmd-13-проблем)
  - [`docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` (13 проблем)](#docs02-anthropic-vacancies94-19-adr-001-federation-over-mergingmd-13-проблем)
  - [`docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` (13 проблем)](#docs04-ai-collaborations02-методика-и-рамка-отбораmd-13-проблем)
  - [`docs/05-habr-projects/02-collaboration-partners.md` (13 проблем)](#docs05-habr-projects02-collaboration-partnersmd-13-проблем)
  - [`docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` (13 проблем)](#docs02-anthropic-vacancies327-1-открытие-cowork-и-почему-это-меняет-всёmd-13-проблем)
  - [`docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` (12 проблем)](#docs02-anthropic-vacancies110-вопрос-fallback-ratio-как-критический-или-осмысленmd-12-проблем)
  - [`docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` (12 проблем)](#docs02-anthropic-vacancies112-5-связь-с-существующими-методологиямиmd-12-проблем)
  - [`docs/02-anthropic-vacancies/123-portal-mcp-py.md` (12 проблем)](#docs02-anthropic-vacancies123-portal-mcp-pymd-12-проблем)
  - [`docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` (12 проблем)](#docs02-anthropic-vacancies127-подключение-к-claude-desktopmd-12-проблем)
  - [`docs/02-anthropic-vacancies/22-10-queryresult-structure.md` (12 проблем)](#docs02-anthropic-vacancies22-10-queryresult-structuremd-12-проблем)
  - [`docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` (12 проблем)](#docs02-anthropic-vacancies222-11-call-for-collaborationmd-12-проблем)
  - [`docs/02-anthropic-vacancies/245-ссылки.md` (12 проблем)](#docs02-anthropic-vacancies245-ссылкиmd-12-проблем)
  - [`docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` (12 проблем)](#docs02-anthropic-vacancies26-14-adr-001-federation-over-mergingmd-12-проблем)
  - [`docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` (12 проблем)](#docs02-anthropic-vacancies261-8-seven-domains-of-applicationmd-12-проблем)
  - [`docs/02-anthropic-vacancies/275-why-this-document-exists.md` (12 проблем)](#docs02-anthropic-vacancies275-why-this-document-existsmd-12-проблем)
  - [`docs/02-anthropic-vacancies/285-closing.md` (12 проблем)](#docs02-anthropic-vacancies285-closingmd-12-проблем)
  - [`docs/02-anthropic-vacancies/42-author-contact.md` (12 проблем)](#docs02-anthropic-vacancies42-author-contactmd-12-проблем)
  - [`docs/02-anthropic-vacancies/52-author-contact.md` (12 проблем)](#docs02-anthropic-vacancies52-author-contactmd-12-проблем)
  - [`docs/02-anthropic-vacancies/65-readme-md.md` (12 проблем)](#docs02-anthropic-vacancies65-readme-mdmd-12-проблем)
  - [`docs/02-anthropic-vacancies/72-расписание-фазы-3.md` (12 проблем)](#docs02-anthropic-vacancies72-расписание-фазы-3md-12-проблем)
  - [`docs/02-anthropic-vacancies/77-2-terminology.md` (12 проблем)](#docs02-anthropic-vacancies77-2-terminologymd-12-проблем)
  - [`docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` (12 проблем)](#docs02-anthropic-vacancies97-22-glossary-of-reference-examplesmd-12-проблем)
  - [`docs/03-technology-combinations/03-local-first.md` (12 проблем)](#docs03-technology-combinations03-local-firstmd-12-проблем)
  - [`docs/05-habr-projects/memory/yodoca.md` (12 проблем)](#docs05-habr-projectsmemoryyodocamd-12-проблем)
  - [`docs/COMPONENT_MATRIX.md` (12 проблем)](#docscomponent_matrixmd-12-проблем)
  - [`docs/SIMILAR.md` (12 проблем)](#docssimilarmd-12-проблем)
  - [`docs/02-anthropic-vacancies/103-appendix-b-change-log.md` (11 проблем)](#docs02-anthropic-vacancies103-appendix-b-change-logmd-11-проблем)
  - [`docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` (11 проблем)](#docs02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd-11-проблем)
  - [`docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` (11 проблем)](#docs02-anthropic-vacancies119-appendix-b-примеры-расхождений-и-их-разрешенияmd-11-проблем)
  - [`docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` (11 проблем)](#docs02-anthropic-vacancies125-readme-mcp-md-инструкция-по-установкеmd-11-проблем)
  - [`docs/02-anthropic-vacancies/128-доступные-инструменты.md` (11 проблем)](#docs02-anthropic-vacancies128-доступные-инструментыmd-11-проблем)
  - [`docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` (11 проблем)](#docs02-anthropic-vacancies131-ограничения-текущей-версии-0-1-0-draftmd-11-проблем)
  - [`docs/02-anthropic-vacancies/136-abstract.md` (11 проблем)](#docs02-anthropic-vacancies136-abstractmd-11-проблем)
  - [`docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` (11 проблем)](#docs02-anthropic-vacancies184-appendix-a-connection-to-companion-papersmd-11-проблем)
  - [`docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` (11 проблем)](#docs02-anthropic-vacancies188-ai-опосредованное-представительство-для-недопредстmd-11-проблем)
  - [`docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` (11 проблем)](#docs02-anthropic-vacancies209-a-typology-of-ai-agents-on-the-principal-side-and-md-11-проблем)
  - [`docs/02-anthropic-vacancies/225-references.md` (11 проблем)](#docs02-anthropic-vacancies225-referencesmd-11-проблем)
  - [`docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` (11 проблем)](#docs02-anthropic-vacancies229-профессиональные-коллеги-агентыmd-11-проблем)
  - [`docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` (11 проблем)](#docs02-anthropic-vacancies251-ai-support-through-configurable-specialist-ensemblmd-11-проблем)
  - [`docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` (11 проблем)](#docs02-anthropic-vacancies27-15-glossary-of-examplesmd-11-проблем)
  - [`docs/02-anthropic-vacancies/281-the-recursive-insight.md` (11 проблем)](#docs02-anthropic-vacancies281-the-recursive-insightmd-11-проблем)
  - [`docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` (11 проблем)](#docs02-anthropic-vacancies283-what-this-document-doesn-t-solvemd-11-проблем)
  - [`docs/02-anthropic-vacancies/349-твоя-личность.md` (11 проблем)](#docs02-anthropic-vacancies349-твоя-личностьmd-11-проблем)
  - [`docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` (11 проблем)](#docs02-anthropic-vacancies354-существующий-landscape-collaborators-твоя-working-md-11-проблем)
  - [`docs/02-anthropic-vacancies/50-bridges.md` (11 проблем)](#docs02-anthropic-vacancies50-bridgesmd-11-проблем)
  - [`docs/02-anthropic-vacancies/51-compatibility-level.md` (11 проблем)](#docs02-anthropic-vacancies51-compatibility-levelmd-11-проблем)
  - [`docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` (11 проблем)](#docs02-anthropic-vacancies54-for-the-curious-philosophymd-11-проблем)
  - [`docs/02-anthropic-vacancies/62-author-contact.md` (11 проблем)](#docs02-anthropic-vacancies62-author-contactmd-11-проблем)
  - [`docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` (11 проблем)](#docs02-anthropic-vacancies71-критерии-выбора-для-фазы-3md-11-проблем)
  - [`docs/02-anthropic-vacancies/75-0-status-of-this-document.md` (11 проблем)](#docs02-anthropic-vacancies75-0-status-of-this-documentmd-11-проблем)
  - [`docs/02-anthropic-vacancies/86-11-relevance-ranking.md` (11 проблем)](#docs02-anthropic-vacancies86-11-relevance-rankingmd-11-проблем)
  - [`docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` (11 проблем)](#docs02-anthropic-vacancies91-16-mcp-extension-informativemd-11-проблем)
  - [`docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` (11 проблем)](#docs02-anthropic-vacancies95-20-adr-002-q6-as-first-class-protocol-conceptmd-11-проблем)
  - [`docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` (11 проблем)](#docs02-anthropic-vacancies96-21-adr-003-five-onboarding-paths-as-equal-rankmd-11-проблем)
  - [`docs/05-habr-projects/memory/ngt-memory.md` (11 проблем)](#docs05-habr-projectsmemoryngt-memorymd-11-проблем)
  - [`docs/DIGEST.md` (11 проблем)](#docsdigestmd-11-проблем)
  - [`docs/contacts/anastasiyaw.md` (11 проблем)](#docscontactsanastasiyawmd-11-проблем)
  - [`docs/contacts/antipozitive.md` (11 проблем)](#docscontactsantipozitivemd-11-проблем)
  - [`docs/02-anthropic-vacancies/03-portal-protocol-md.md` (10 проблем)](#docs02-anthropic-vacancies03-portal-protocol-mdmd-10-проблем)
  - [`docs/02-anthropic-vacancies/05-0-status-of-this-document.md` (10 проблем)](#docs02-anthropic-vacancies05-0-status-of-this-documentmd-10-проблем)
  - [`docs/02-anthropic-vacancies/105-review-methodology-md.md` (10 проблем)](#docs02-anthropic-vacancies105-review-methodology-mdmd-10-проблем)
  - [`docs/02-anthropic-vacancies/106-tl-dr.md` (10 проблем)](#docs02-anthropic-vacancies106-tl-drmd-10-проблем)
  - [`docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` (10 проблем)](#docs02-anthropic-vacancies116-9-checklist-применения-методологииmd-10-проблем)
  - [`docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` (10 проблем)](#docs02-anthropic-vacancies124-конфигурация-для-claude-desktopmd-10-проблем)
  - [`docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` (10 проблем)](#docs02-anthropic-vacancies129-примеры-запросов-в-claudemd-10-проблем)
  - [`docs/02-anthropic-vacancies/147-references.md` (10 проблем)](#docs02-anthropic-vacancies147-referencesmd-10-проблем)
  - [`docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` (10 проблем)](#docs02-anthropic-vacancies149-appendix-b-summary-of-contributionsmd-10-проблем)
  - [`docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` (10 проблем)](#docs02-anthropic-vacancies152-ai-coordinated-infrastructure-for-distributed-expemd-10-проблем)
  - [`docs/02-anthropic-vacancies/153-executive-summary.md` (10 проблем)](#docs02-anthropic-vacancies153-executive-summarymd-10-проблем)
  - [`docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` (10 проблем)](#docs02-anthropic-vacancies167-ai-mediated-representation-for-underrepresented-exmd-10-проблем)
  - [`docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` (10 проблем)](#docs02-anthropic-vacancies180-11-call-for-collaborationmd-10-проблем)
  - [`docs/02-anthropic-vacancies/181-12-closing.md` (10 проблем)](#docs02-anthropic-vacancies181-12-closingmd-10-проблем)
  - [`docs/02-anthropic-vacancies/19-7-portalentry-structure.md` (10 проблем)](#docs02-anthropic-vacancies19-7-portalentry-structuremd-10-проблем)
  - [`docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` (10 проблем)](#docs02-anthropic-vacancies205-приложение-a-связь-с-сопроводительными-статьямиmd-10-проблем)
  - [`docs/02-anthropic-vacancies/210-abstract.md` (10 проблем)](#docs02-anthropic-vacancies210-abstractmd-10-проблем)
  - [`docs/02-anthropic-vacancies/224-acknowledgments.md` (10 проблем)](#docs02-anthropic-vacancies224-acknowledgmentsmd-10-проблем)
  - [`docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` (10 проблем)](#docs02-anthropic-vacancies282-what-industry-will-likely-buildmd-10-проблем)
  - [`docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` (10 проблем)](#docs02-anthropic-vacancies293-почему-это-не-было-построеноmd-10-проблем)
  - [`docs/02-anthropic-vacancies/337-благодарности.md` (10 проблем)](#docs02-anthropic-vacancies337-благодарностиmd-10-проблем)
  - [`docs/02-anthropic-vacancies/38-content-overview.md` (10 проблем)](#docs02-anthropic-vacancies38-content-overviewmd-10-проблем)
  - [`docs/02-anthropic-vacancies/41-compatibility-level.md` (10 проблем)](#docs02-anthropic-vacancies41-compatibility-levelmd-10-проблем)
  - [`docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` (10 проблем)](#docs02-anthropic-vacancies44-for-the-curious-philosophymd-10-проблем)
  - [`docs/02-anthropic-vacancies/53-history.md` (10 проблем)](#docs02-anthropic-vacancies53-historymd-10-проблем)
  - [`docs/02-anthropic-vacancies/60-bridges.md` (10 проблем)](#docs02-anthropic-vacancies60-bridgesmd-10-проблем)
  - [`docs/02-anthropic-vacancies/61-compatibility-level.md` (10 проблем)](#docs02-anthropic-vacancies61-compatibility-levelmd-10-проблем)
  - [`docs/02-anthropic-vacancies/63-history.md` (10 проблем)](#docs02-anthropic-vacancies63-historymd-10-проблем)
  - [`docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` (10 проблем)](#docs02-anthropic-vacancies73-portal-protocol-md-v1-1md-10-проблем)
  - [`docs/02-anthropic-vacancies/74-abstract.md` (10 проблем)](#docs02-anthropic-vacancies74-abstractmd-10-проблем)
  - [`docs/02-anthropic-vacancies/93-18-reference-implementation.md` (10 проблем)](#docs02-anthropic-vacancies93-18-reference-implementationmd-10-проблем)
  - [`docs/AUTOFILLED.md` (10 проблем)](#docsautofilledmd-10-проблем)
  - [`docs/BACKLINKS.md` (10 проблем)](#docsbacklinksmd-10-проблем)
  - [`docs/KEYWORD_INDEX.md` (10 проблем)](#docskeyword_indexmd-10-проблем)
  - [`docs/contacts/cutcode.md` (10 проблем)](#docscontactscutcodemd-10-проблем)
  - [`docs/contacts/dmitriila.md` (10 проблем)](#docscontactsdmitriilamd-10-проблем)
  - [`docs/contacts/mixaill76.md` (10 проблем)](#docscontactsmixaill76md-10-проблем)
  - [`docs/contacts/nlaik.md` (10 проблем)](#docscontactsnlaikmd-10-проблем)
  - [`docs/contacts/sonia-black.md` (10 проблем)](#docscontactssonia-blackmd-10-проблем)
  - [`docs/contacts/tagir-analyzes.md` (10 проблем)](#docscontactstagir-analyzesmd-10-проблем)
  - [`docs/contacts/vitalyoborin.md` (10 проблем)](#docscontactsvitalyoborinmd-10-проблем)
  - [`docs/contacts/vladspace.md` (10 проблем)](#docscontactsvladspacemd-10-проблем)
  - [`docs/contacts/zodigancode.md` (10 проблем)](#docscontactszodigancodemd-10-проблем)
  - [`docs/02-anthropic-vacancies/06-1-introduction.md` (9 проблем)](#docs02-anthropic-vacancies06-1-introductionmd-9-проблем)
  - [`docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` (9 проблем)](#docs02-anthropic-vacancies134-the-double-triangle-architecture-mdmd-9-проблем)
  - [`docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` (9 проблем)](#docs02-anthropic-vacancies135-a-formal-model-for-human-ai-collaboration-in-distrmd-9-проблем)
  - [`docs/02-anthropic-vacancies/137-table-of-contents.md` (9 проблем)](#docs02-anthropic-vacancies137-table-of-contentsmd-9-проблем)
  - [`docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` (9 проблем)](#docs02-anthropic-vacancies166-representative-agent-layer-mdmd-9-проблем)
  - [`docs/02-anthropic-vacancies/169-table-of-contents.md` (9 проблем)](#docs02-anthropic-vacancies169-table-of-contentsmd-9-проблем)
  - [`docs/02-anthropic-vacancies/182-acknowledgments.md` (9 проблем)](#docs02-anthropic-vacancies182-acknowledgmentsmd-9-проблем)
  - [`docs/02-anthropic-vacancies/183-references.md` (9 проблем)](#docs02-anthropic-vacancies183-referencesmd-9-проблем)
  - [`docs/02-anthropic-vacancies/190-содержание.md` (9 проблем)](#docs02-anthropic-vacancies190-содержаниеmd-9-проблем)
  - [`docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` (9 проблем)](#docs02-anthropic-vacancies208-professional-colleague-agents-mdmd-9-проблем)
  - [`docs/02-anthropic-vacancies/211-table-of-contents.md` (9 проблем)](#docs02-anthropic-vacancies211-table-of-contentsmd-9-проблем)
  - [`docs/02-anthropic-vacancies/223-12-closing.md` (9 проблем)](#docs02-anthropic-vacancies223-12-closingmd-9-проблем)
  - [`docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` (9 проблем)](#docs02-anthropic-vacancies226-appendix-a-comparative-table-five-agent-typesmd-9-проблем)
  - [`docs/02-anthropic-vacancies/230-аннотация.md` (9 проблем)](#docs02-anthropic-vacancies230-аннотацияmd-9-проблем)
  - [`docs/02-anthropic-vacancies/231-содержание.md` (9 проблем)](#docs02-anthropic-vacancies231-содержаниеmd-9-проблем)
  - [`docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` (9 проблем)](#docs02-anthropic-vacancies246-приложение-a-сравнительная-таблица-пять-типов-агенmd-9-проблем)
  - [`docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` (9 проблем)](#docs02-anthropic-vacancies249-composite-skills-agent-mdmd-9-проблем)
  - [`docs/02-anthropic-vacancies/253-table-of-contents.md` (9 проблем)](#docs02-anthropic-vacancies253-table-of-contentsmd-9-проблем)
  - [`docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` (9 проблем)](#docs02-anthropic-vacancies269-appendix-a-the-six-type-taxonomy-updatedmd-9-проблем)
  - [`docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` (9 проблем)](#docs02-anthropic-vacancies290-почему-этот-документ-существуетmd-9-проблем)
  - [`docs/02-anthropic-vacancies/300-заключение.md` (9 проблем)](#docs02-anthropic-vacancies300-заключениеmd-9-проблем)
  - [`docs/02-anthropic-vacancies/301-благодарности.md` (9 проблем)](#docs02-anthropic-vacancies301-благодарностиmd-9-проблем)
  - [`docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` (9 проблем)](#docs02-anthropic-vacancies305-a-practical-path-to-layer-b-through-symbiotic-intemd-9-проблем)
  - [`docs/02-anthropic-vacancies/308-table-of-contents.md` (9 проблем)](#docs02-anthropic-vacancies308-table-of-contentsmd-9-проблем)
  - [`docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` (9 проблем)](#docs02-anthropic-vacancies321-appendix-a-decision-tree-for-ingit-adoptersmd-9-проблем)
  - [`docs/02-anthropic-vacancies/325-аннотация.md` (9 проблем)](#docs02-anthropic-vacancies325-аннотацияmd-9-проблем)
  - [`docs/02-anthropic-vacancies/347-твоя-миссия.md` (9 проблем)](#docs02-anthropic-vacancies347-твоя-миссияmd-9-проблем)
  - [`docs/02-anthropic-vacancies/35-passports-info1-md.md` (9 проблем)](#docs02-anthropic-vacancies35-passports-info1-mdmd-9-проблем)
  - [`docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` (9 проблем)](#docs02-anthropic-vacancies353-что-ты-не-можешь-делать-вообщеmd-9-проблем)
  - [`docs/02-anthropic-vacancies/36-essence.md` (9 проблем)](#docs02-anthropic-vacancies36-essencemd-9-проблем)
  - [`docs/02-anthropic-vacancies/39-angle-perspective.md` (9 проблем)](#docs02-anthropic-vacancies39-angle-perspectivemd-9-проблем)
  - [`docs/02-anthropic-vacancies/45-passports-pro2-md.md` (9 проблем)](#docs02-anthropic-vacancies45-passports-pro2-mdmd-9-проблем)
  - [`docs/02-anthropic-vacancies/46-essence.md` (9 проблем)](#docs02-anthropic-vacancies46-essencemd-9-проблем)
  - [`docs/02-anthropic-vacancies/55-passports-meta-md.md` (9 проблем)](#docs02-anthropic-vacancies55-passports-meta-mdmd-9-проблем)
  - [`docs/02-anthropic-vacancies/59-angle-perspective.md` (9 проблем)](#docs02-anthropic-vacancies59-angle-perspectivemd-9-проблем)
  - [`docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` (9 проблем)](#docs02-anthropic-vacancies70-зачем-две-версии-параллельноmd-9-проблем)
  - [`docs/03-technology-combinations/01-agent-routing.md` (9 проблем)](#docs03-technology-combinations01-agent-routingmd-9-проблем)
  - [`docs/contacts/andrey-chuyan.md` (9 проблем)](#docscontactsandrey-chuyanmd-9-проблем)
  - [`docs/contacts/spbmolot.md` (9 проблем)](#docscontactsspbmolotmd-9-проблем)
  - [`docs/02-anthropic-vacancies/04-abstract.md` (8 проблем)](#docs02-anthropic-vacancies04-abstractmd-8-проблем)
  - [`docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` (8 проблем)](#docs02-anthropic-vacancies118-appendix-a-шаблон-для-header-warningmd-8-проблем)
  - [`docs/02-anthropic-vacancies/12-content-overview.md` (8 проблем)](#docs02-anthropic-vacancies12-content-overviewmd-8-проблем)
  - [`docs/02-anthropic-vacancies/120-главные-технические-риски.md` (8 проблем)](#docs02-anthropic-vacancies120-главные-технические-рискиmd-8-проблем)
  - [`docs/02-anthropic-vacancies/126-установка.md` (8 проблем)](#docs02-anthropic-vacancies126-установкаmd-8-проблем)
  - [`docs/02-anthropic-vacancies/132-planned-v0-2-0.md` (8 проблем)](#docs02-anthropic-vacancies132-planned-v0-2-0md-8-проблем)
  - [`docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` (8 проблем)](#docs02-anthropic-vacancies151-open-knowledge-work-foundation-mdmd-8-проблем)
  - [`docs/02-anthropic-vacancies/154-table-of-contents.md` (8 проблем)](#docs02-anthropic-vacancies154-table-of-contentsmd-8-проблем)
  - [`docs/02-anthropic-vacancies/168-abstract.md` (8 проблем)](#docs02-anthropic-vacancies168-abstractmd-8-проблем)
  - [`docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` (8 проблем)](#docs02-anthropic-vacancies187-слой-представительских-агентов-mdmd-8-проблем)
  - [`docs/02-anthropic-vacancies/204-ссылки.md` (8 проблем)](#docs02-anthropic-vacancies204-ссылкиmd-8-проблем)
  - [`docs/02-anthropic-vacancies/244-благодарности.md` (8 проблем)](#docs02-anthropic-vacancies244-благодарностиmd-8-проблем)
  - [`docs/02-anthropic-vacancies/252-abstract.md` (8 проблем)](#docs02-anthropic-vacancies252-abstractmd-8-проблем)
  - [`docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` (8 проблем)](#docs02-anthropic-vacancies270-appendix-b-sub-agent-registry-schema-sketchmd-8-проблем)
  - [`docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` (8 проблем)](#docs02-anthropic-vacancies271-appendix-c-configuration-template-examplemd-8-проблем)
  - [`docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` (8 проблем)](#docs02-anthropic-vacancies273-infrastructure-for-ai-collaborative-intellectual-wmd-8-проблем)
  - [`docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` (8 проблем)](#docs02-anthropic-vacancies28-appendix-a-minimal-working-examplemd-8-проблем)
  - [`docs/02-anthropic-vacancies/286-acknowledgments.md` (8 проблем)](#docs02-anthropic-vacancies286-acknowledgmentsmd-8-проблем)
  - [`docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` (8 проблем)](#docs02-anthropic-vacancies296-рекурсивное-прозрениеmd-8-проблем)
  - [`docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` (8 проблем)](#docs02-anthropic-vacancies298-что-этот-документ-не-решаетmd-8-проблем)
  - [`docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` (8 проблем)](#docs02-anthropic-vacancies304-ingit-as-cowork-native-workspace-substrate-mdmd-8-проблем)
  - [`docs/02-anthropic-vacancies/307-abstract.md` (8 проблем)](#docs02-anthropic-vacancies307-abstractmd-8-проблем)
  - [`docs/02-anthropic-vacancies/31-content-overview.md` (8 проблем)](#docs02-anthropic-vacancies31-content-overviewmd-8-проблем)
  - [`docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` (8 проблем)](#docs02-anthropic-vacancies322-appendix-b-comparison-matrixmd-8-проблем)
  - [`docs/02-anthropic-vacancies/326-содержание.md` (8 проблем)](#docs02-anthropic-vacancies326-содержаниеmd-8-проблем)
  - [`docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` (8 проблем)](#docs02-anthropic-vacancies357-твоя-коммуникация-в-outreachmd-8-проблем)
  - [`docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` (8 проблем)](#docs02-anthropic-vacancies358-твоя-relationship-с-другими-aimd-8-проблем)
  - [`docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` (8 проблем)](#docs02-anthropic-vacancies360-что-ты-всегда-делаешьmd-8-проблем)
  - [`docs/02-anthropic-vacancies/47-native-format.md` (8 проблем)](#docs02-anthropic-vacancies47-native-formatmd-8-проблем)
  - [`docs/02-anthropic-vacancies/49-angle-perspective.md` (8 проблем)](#docs02-anthropic-vacancies49-angle-perspectivemd-8-проблем)
  - [`docs/02-anthropic-vacancies/58-content-overview.md` (8 проблем)](#docs02-anthropic-vacancies58-content-overviewmd-8-проблем)
  - [`docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` (8 проблем)](#docs02-anthropic-vacancies89-14-sdk-contract-informativemd-8-проблем)
  - [`docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` (8 проблем)](#docs02-anthropic-vacancies98-appendix-a-minimal-working-examplemd-8-проблем)
  - [`docs/05-habr-projects/01-synthesis.md` (8 проблем)](#docs05-habr-projects01-synthesismd-8-проблем)
  - [`docs/05-habr-projects/knowledge/wikontic.md` (8 проблем)](#docs05-habr-projectsknowledgewikonticmd-8-проблем)
  - [`docs/autofilled/components/cowork.md` (8 проблем)](#docsautofilledcomponentscoworkmd-8-проблем)
  - [`docs/autofilled/components/ingit.md` (8 проблем)](#docsautofilledcomponentsingitmd-8-проблем)
  - [`docs/autofilled/components/lorenzo.md` (8 проблем)](#docsautofilledcomponentslorenzomd-8-проблем)
  - [`docs/autofilled/components/nautilus.md` (8 проблем)](#docsautofilledcomponentsnautilusmd-8-проблем)
  - [`docs/autofilled/components/sgb.md` (8 проблем)](#docsautofilledcomponentssgbmd-8-проблем)
  - [`docs/autofilled/components/svend4.md` (8 проблем)](#docsautofilledcomponentssvend4md-8-проблем)
  - [`docs/autofilled/components/svyazi.md` (8 проблем)](#docsautofilledcomponentssvyazimd-8-проблем)
  - [`docs/contacts/kksudo.md` (8 проблем)](#docscontactskksudomd-8-проблем)
  - [`docs/02-anthropic-vacancies/102-доступ-к-данным.md` (7 проблем)](#docs02-anthropic-vacancies102-доступ-к-даннымmd-7-проблем)
  - [`docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` (7 проблем)](#docs02-anthropic-vacancies113-6-почему-это-валидный-паттерн-для-ai-assisted-workmd-7-проблем)
  - [`docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` (7 проблем)](#docs02-anthropic-vacancies121-appendix-c-история-изменений-методологииmd-7-проблем)
  - [`docs/02-anthropic-vacancies/13-angle-perspective.md` (7 проблем)](#docs02-anthropic-vacancies13-angle-perspectivemd-7-проблем)
  - [`docs/02-anthropic-vacancies/16-history.md` (7 проблем)](#docs02-anthropic-vacancies16-historymd-7-проблем)
  - [`docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` (7 проблем)](#docs02-anthropic-vacancies206-приложение-b-матрица-сравнения-областейmd-7-проблем)
  - [`docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` (7 проблем)](#docs02-anthropic-vacancies241-10-открытые-вопросыmd-7-проблем)
  - [`docs/02-anthropic-vacancies/243-12-заключение.md` (7 проблем)](#docs02-anthropic-vacancies243-12-заключениеmd-7-проблем)
  - [`docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` (7 проблем)](#docs02-anthropic-vacancies339-приложение-a-дерево-решений-для-принимающих-ingitmd-7-проблем)
  - [`docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` (7 проблем)](#docs02-anthropic-vacancies340-приложение-b-сравнительная-матрицаmd-7-проблем)
  - [`docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` (7 проблем)](#docs02-anthropic-vacancies344-системный-промпт-для-lorenzo-projectmd-7-проблем)
  - [`docs/02-anthropic-vacancies/345-кто-ты.md` (7 проблем)](#docs02-anthropic-vacancies345-кто-тыmd-7-проблем)
  - [`docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` (7 проблем)](#docs02-anthropic-vacancies352-что-ты-не-можешь-делать-без-max-approvalmd-7-проблем)
  - [`docs/02-anthropic-vacancies/359-твои-anti-patterns.md` (7 проблем)](#docs02-anthropic-vacancies359-твои-anti-patternsmd-7-проблем)
  - [`docs/05-habr-projects/QA.md` (7 проблем)](#docs05-habr-projectsqamd-7-проблем)
  - [`docs/CHANGELOG.md` (7 проблем)](#docschangelogmd-7-проблем)
  - [`docs/DEPENDENCY_MAP.md` (7 проблем)](#docsdependency_mapmd-7-проблем)
  - [`docs/autofilled/components/.md` (7 проблем)](#docsautofilledcomponentsmd-7-проблем)
  - [`docs/autofilled/components/kksudo.md` (7 проблем)](#docsautofilledcomponentskksudomd-7-проблем)
  - [`docs/autofilled/components/spbmolot.md` (7 проблем)](#docsautofilledcomponentsspbmolotmd-7-проблем)
  - [`docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` (6 проблем)](#docs02-anthropic-vacancies242-11-призыв-к-сотрудничествуmd-6-проблем)
  - [`docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` (6 проблем)](#docs02-anthropic-vacancies297-что-промышленность-вероятно-построитmd-6-проблем)
  - [`docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` (6 проблем)](#docs02-anthropic-vacancies350-твои-языки-и-культурные-nuancesmd-6-проблем)
  - [`docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` (6 проблем)](#docs02-anthropic-vacancies362-когда-сомневаешься-escalate-к-maxmd-6-проблем)
  - [`docs/03-technology-combinations/04-sozialrecht-domain.md` (6 проблем)](#docs03-technology-combinations04-sozialrecht-domainmd-6-проблем)
  - [`docs/VALIDATION.md` (6 проблем)](#docsvalidationmd-6-проблем)
  - [`docs/02-anthropic-vacancies/183-references.md` (6 проблем)](#docs02-anthropic-vacancies183-referencesmd-6-проблем)
  - [`docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` (6 проблем)](#docs02-anthropic-vacancies188-ai-опосредованное-представительство-для-недопредстmd-6-проблем)
  - [`docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` (6 проблем)](#docs02-anthropic-vacancies201-11-призыв-к-сотрудничествуmd-6-проблем)
  - [`docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` (6 проблем)](#docs02-anthropic-vacancies209-a-typology-of-ai-agents-on-the-principal-side-and-md-6-проблем)
  - [`docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` (6 проблем)](#docs02-anthropic-vacancies226-appendix-a-comparative-table-five-agent-typesmd-6-проблем)
  - [`docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` (6 проблем)](#docs02-anthropic-vacancies229-профессиональные-коллеги-агентыmd-6-проблем)
  - [`docs/02-anthropic-vacancies/230-аннотация.md` (6 проблем)](#docs02-anthropic-vacancies230-аннотацияmd-6-проблем)
  - [`docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` (6 проблем)](#docs02-anthropic-vacancies251-ai-support-through-configurable-specialist-ensemblmd-6-проблем)
  - [`docs/02-anthropic-vacancies/252-abstract.md` (6 проблем)](#docs02-anthropic-vacancies252-abstractmd-6-проблем)
  - [`docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` (6 проблем)](#docs02-anthropic-vacancies26-14-adr-001-federation-over-mergingmd-6-проблем)
  - [`docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` (6 проблем)](#docs02-anthropic-vacancies282-what-industry-will-likely-buildmd-6-проблем)
  - [`docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` (6 проблем)](#docs02-anthropic-vacancies283-what-this-document-doesn-t-solvemd-6-проблем)
  - [`docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` (6 проблем)](#docs02-anthropic-vacancies296-рекурсивное-прозрениеmd-6-проблем)
  - [`docs/02-anthropic-vacancies/337-благодарности.md` (6 проблем)](#docs02-anthropic-vacancies337-благодарностиmd-6-проблем)
  - [`docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` (6 проблем)](#docs02-anthropic-vacancies351-что-ты-можешь-делатьmd-6-проблем)
  - [`docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` (6 проблем)](#docs02-anthropic-vacancies357-твоя-коммуникация-в-outreachmd-6-проблем)
  - [`docs/02-anthropic-vacancies/41-compatibility-level.md` (6 проблем)](#docs02-anthropic-vacancies41-compatibility-levelmd-6-проблем)
  - [`docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` (6 проблем)](#docs02-anthropic-vacancies44-for-the-curious-philosophymd-6-проблем)
  - [`docs/02-anthropic-vacancies/51-compatibility-level.md` (6 проблем)](#docs02-anthropic-vacancies51-compatibility-levelmd-6-проблем)
  - [`docs/02-anthropic-vacancies/53-history.md` (6 проблем)](#docs02-anthropic-vacancies53-historymd-6-проблем)
  - [`docs/02-anthropic-vacancies/60-bridges.md` (6 проблем)](#docs02-anthropic-vacancies60-bridgesmd-6-проблем)
  - [`docs/02-anthropic-vacancies/61-compatibility-level.md` (6 проблем)](#docs02-anthropic-vacancies61-compatibility-levelmd-6-проблем)
  - [`docs/02-anthropic-vacancies/62-author-contact.md` (6 проблем)](#docs02-anthropic-vacancies62-author-contactmd-6-проблем)
  - [`docs/02-anthropic-vacancies/74-abstract.md` (6 проблем)](#docs02-anthropic-vacancies74-abstractmd-6-проблем)
  - [`docs/02-anthropic-vacancies/75-0-status-of-this-document.md` (6 проблем)](#docs02-anthropic-vacancies75-0-status-of-this-documentmd-6-проблем)
  - [`docs/02-anthropic-vacancies/93-18-reference-implementation.md` (6 проблем)](#docs02-anthropic-vacancies93-18-reference-implementationmd-6-проблем)
  - [`docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` (6 проблем)](#docs02-anthropic-vacancies95-20-adr-002-q6-as-first-class-protocol-conceptmd-6-проблем)
  - [`docs/HEATMAP.md` (6 проблем)](#docsheatmapmd-6-проблем)
  - [`docs/KNOWLEDGE_MAP.md` (6 проблем)](#docsknowledge_mapmd-6-проблем)
  - [`docs/VALIDATION.md` (6 проблем)](#docsvalidationmd-6-проблем)
  - [`docs/ai-collaborations/candidates/02-related-projects-context.md` (6 проблем)](#docsai-collaborationscandidates02-related-projects-contextmd-6-проблем)
  - [`docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md` (6 проблем)](#docsai-collaborationscandidates03-synthesis-hebbian-collaboration-graphmd-6-проблем)
  - [`docs/ai-collaborations/continuation/05-roadmap-6-12-months.md` (6 проблем)](#docsai-collaborationscontinuation05-roadmap-6-12-monthsmd-6-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md` (6 проблем)](#docsanthropic-vacanciesai-managed-virtual-company04-what-to-domd-6-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md` (6 проблем)](#docsanthropic-vacanciesai-managed-virtual-company06-angel-vs-demon-dualitymd-6-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md` (6 проблем)](#docsanthropic-vacanciesai-managed-virtual-company09-minuses-and-risksmd-6-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md` (6 проблем)](#docsanthropic-vacancieshermes-comparison05-similarity-5-self-hosting-privacymd-6-проблем)
  - [`docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md` (6 проблем)](#docsanthropic-vacanciesnautilus-vs-camel00-question-camel-vs-nautilusmd-6-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md` (6 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis06-not-applicable-rolesmd-6-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md` (6 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-final02-final-rankingmd-6-проблем)
  - [`docs/autofilled/research-summary.md` (6 проблем)](#docsautofilledresearch-summarymd-6-проблем)
  - [`docs/habr-unique-projects/final-ensembles/1-one-person-one-company.md` (6 проблем)](#docshabr-unique-projectsfinal-ensembles1-one-person-one-companymd-6-проблем)
  - [`docs/lorenzo-agent/07-chto-mozhesh.md` (6 проблем)](#docslorenzo-agent07-chto-mozheshmd-6-проблем)
  - [`docs/lorenzo-agent/13-outreach-communication.md` (6 проблем)](#docslorenzo-agent13-outreach-communicationmd-6-проблем)
  - [`docs/lorenzo-agent/naming/00-question-lorenzo-codename.md` (6 проблем)](#docslorenzo-agentnaming00-question-lorenzo-codenamemd-6-проблем)
  - [`docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md` (6 проблем)](#docsnautiluscommunity-discussionsvoiceless-contributors00-question-voicelessmd-6-проблем)
  - [`docs/nautilus/double-triangle-architecture/08-call-to-action.md` (6 проблем)](#docsnautilusdouble-triangle-architecture08-call-to-actionmd-6-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md` (6 проблем)](#docsnautilusinfrastructure-layer-b-ru03-otsutstvuet-sloy-bmd-6-проблем)
  - [`docs/nautilus/npp-v1-0/02-terminology.md` (6 проблем)](#docsnautilusnpp-v1-002-terminologymd-6-проблем)
  - [`docs/nautilus/npp-v1-0/05-compatibility-levels.md` (6 проблем)](#docsnautilusnpp-v1-005-compatibility-levelsmd-6-проблем)
  - [`docs/nautilus/npp-v1-0/12-versioning-policy.md` (6 проблем)](#docsnautilusnpp-v1-012-versioning-policymd-6-проблем)
  - [`docs/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md` (6 проблем)](#docsnautilusnpp-v1-119-adr-001-federation-over-mergingmd-6-проблем)
  - [`docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md` (6 проблем)](#docsnautilusnpp-v1-121-adr-003-five-onboarding-pathsmd-6-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/00-abstract.md` (6 проблем)](#docsnautilusprofessional-colleague-agents-en00-abstractmd-6-проблем)
  - [`docs/nautilus/review-methodology/00-tldr.md` (6 проблем)](#docsnautilusreview-methodology00-tldrmd-6-проблем)
  - [`docs/nautilus/review-methodology/02-formal-workflow.md` (6 проблем)](#docsnautilusreview-methodology02-formal-workflowmd-6-проблем)
  - [`docs/nautilus/transmission-box/00-question-mountain-to-person.md` (6 проблем)](#docsnautilustransmission-box00-question-mountain-to-personmd-6-проблем)
  - [`docs/svyazi-2-0/architecture/card-envelope.md` (6 проблем)](#docssvyazi-2-0architecturecard-envelopemd-6-проблем)
  - [`docs/svyazi-2-0/architecture/integration-spec.md` (6 проблем)](#docssvyazi-2-0architectureintegration-specmd-6-проблем)
  - [`docs/svyazi-2-0/architecture/review-record.md` (6 проблем)](#docssvyazi-2-0architecturereview-recordmd-6-проблем)
  - [`docs/svyazi-2-0/components/ai-factory.md` (6 проблем)](#docssvyazi-2-0componentsai-factorymd-6-проблем)
  - [`docs/svyazi-2-0/components/research-docs-liteparse.md` (6 проблем)](#docssvyazi-2-0componentsresearch-docs-liteparsemd-6-проблем)
  - [`docs/svyazi-2-0/components/yjs-automerge.md` (6 проблем)](#docssvyazi-2-0componentsyjs-automergemd-6-проблем)
  - [`docs/svyazi-2-0/ensembles/A-collaboration-os.md` (6 проблем)](#docssvyazi-2-0ensemblesa-collaboration-osmd-6-проблем)
  - [`docs/svyazi-2-0/ensembles/B-forensic-rag.md` (6 проблем)](#docssvyazi-2-0ensemblesb-forensic-ragmd-6-проблем)
  - [`docs/svyazi-2-0/ensembles/C-multi-agent-factory.md` (6 проблем)](#docssvyazi-2-0ensemblesc-multi-agent-factorymd-6-проблем)
  - [`docs/svyazi-2-0/ensembles/E-execution-plane.md` (6 проблем)](#docssvyazi-2-0ensemblese-execution-planemd-6-проблем)
  - [`docs/svyazi-2-0/ensembles/G-federated-local-graph.md` (6 проблем)](#docssvyazi-2-0ensemblesg-federated-local-graphmd-6-проблем)
  - [`docs/svyazi-2-0/ensembles/H-research-to-product-flywheel.md` (6 проблем)](#docssvyazi-2-0ensemblesh-research-to-product-flywheelmd-6-проблем)
  - [`docs/svyazi-2-0/limitations/conclusions.md` (6 проблем)](#docssvyazi-2-0limitationsconclusionsmd-6-проблем)
  - [`docs/svyazi-2-0/limitations/do-not-glue.md` (6 проблем)](#docssvyazi-2-0limitationsdo-not-gluemd-6-проблем)
  - [`docs/svyazi-2-0/overview/continuation-intro.md` (6 проблем)](#docssvyazi-2-0overviewcontinuation-intromd-6-проблем)
  - [`docs/svyazi-2-0/security/privacy.md` (6 проблем)](#docssvyazi-2-0securityprivacymd-6-проблем)
  - [`docs/technology-combinations/research-reports/continuation-10-domains.md` (6 проблем)](#docstechnology-combinationsresearch-reportscontinuation-10-domainsmd-6-проблем)
  - [`docs/WORD_CLOUD.md` (6 проблем)](#docsword_cloudmd-6-проблем)
  - [`docs/templates/project-component.md` (6 проблем)](#docstemplatesproject-componentmd-6-проблем)
  - [`docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` (5 проблем)](#docs02-anthropic-vacancies185-appendix-b-domain-comparison-matrixmd-5-проблем)
  - [`docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` (5 проблем)](#docs02-anthropic-vacancies201-11-призыв-к-сотрудничествуmd-5-проблем)
  - [`docs/02-anthropic-vacancies/202-12-заключение.md` (5 проблем)](#docs02-anthropic-vacancies202-12-заключениеmd-5-проблем)
  - [`docs/02-anthropic-vacancies/203-благодарности.md` (5 проблем)](#docs02-anthropic-vacancies203-благодарностиmd-5-проблем)
  - [`docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` (5 проблем)](#docs02-anthropic-vacancies348-кому-ты-служишь-слоистая-модельmd-5-проблем)
  - [`docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` (5 проблем)](#docs02-anthropic-vacancies361-когда-ты-honestly-не-знаешьmd-5-проблем)
  - [`docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` (5 проблем)](#docs02-anthropic-vacancies363-твоя-identity-как-persistent-charactermd-5-проблем)
  - [`docs/CONCEPT_GRAPH.md` (5 проблем)](#docsconcept_graphmd-5-проблем)
  - [`docs/COMPONENT_MATRIX.md` (5 проблем)](#docscomponent_matrixmd-5-проблем)
  - [`docs/DIGEST_AUTO.md` (5 проблем)](#docsdigest_automd-5-проблем)
  - [`docs/HEALTH.md` (5 проблем)](#docshealthmd-5-проблем)
  - [`docs/MISSING.md` (5 проблем)](#docsmissingmd-5-проблем)
  - [`docs/NETWORK.md` (5 проблем)](#docsnetworkmd-5-проблем)
  - [`docs/READING_ORDER.md` (5 проблем)](#docsreading_ordermd-5-проблем)
  - [`docs/READING_TIME.md` (5 проблем)](#docsreading_timemd-5-проблем)
  - [`docs/WORD_CLOUD.md` (5 проблем)](#docsword_cloudmd-5-проблем)
  - [`docs/WORD_FREQ.md` (5 проблем)](#docsword_freqmd-5-проблем)
  - [`docs/02-anthropic-vacancies/189-аннотация.md` (4 проблем)](#docs02-anthropic-vacancies189-аннотацияmd-4-проблем)
  - [`docs/DIGEST_WEEKLY.md` (4 проблем)](#docsdigest_weeklymd-4-проблем)
  - [`docs/KPI_HISTORY.md` (4 проблем)](#docskpi_historymd-4-проблем)
  - [`docs/PASSIVE_VOICE.md` (4 проблем)](#docspassive_voicemd-4-проблем)
  - [`docs/PROGRESS.md` (4 проблем)](#docsprogressmd-4-проблем)
  - [`docs/VERSION_DIFF.md` (4 проблем)](#docsversion_diffmd-4-проблем)
  - [`docs/templates/mega-stack.md` (4 проблем)](#docstemplatesmega-stackmd-4-проблем)
  - [`docs/01-svyazi/README.md` (3 проблем)](#docs01-svyazireadmemd-3-проблем)
  - [`docs/02-anthropic-vacancies/346-твоё-происхождение.md` (3 проблем)](#docs02-anthropic-vacancies346-твоё-происхождениеmd-3-проблем)
  - [`docs/02-anthropic-vacancies/13-angle-perspective.md` (3 проблем)](#docs02-anthropic-vacancies13-angle-perspectivemd-3-проблем)
  - [`docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` (3 проблем)](#docs02-anthropic-vacancies134-the-double-triangle-architecture-mdmd-3-проблем)
  - [`docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` (3 проблем)](#docs02-anthropic-vacancies151-open-knowledge-work-foundation-mdmd-3-проблем)
  - [`docs/02-anthropic-vacancies/16-history.md` (3 проблем)](#docs02-anthropic-vacancies16-historymd-3-проблем)
  - [`docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` (3 проблем)](#docs02-anthropic-vacancies166-representative-agent-layer-mdmd-3-проблем)
  - [`docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` (3 проблем)](#docs02-anthropic-vacancies187-слой-представительских-агентов-mdmd-3-проблем)
  - [`docs/02-anthropic-vacancies/203-благодарности.md` (3 проблем)](#docs02-anthropic-vacancies203-благодарностиmd-3-проблем)
  - [`docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` (3 проблем)](#docs02-anthropic-vacancies208-professional-colleague-agents-mdmd-3-проблем)
  - [`docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` (3 проблем)](#docs02-anthropic-vacancies249-composite-skills-agent-mdmd-3-проблем)
  - [`docs/02-anthropic-vacancies/31-content-overview.md` (3 проблем)](#docs02-anthropic-vacancies31-content-overviewmd-3-проблем)
  - [`docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` (3 проблем)](#docs02-anthropic-vacancies339-приложение-a-дерево-решений-для-принимающих-ingitmd-3-проблем)
  - [`docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` (3 проблем)](#docs02-anthropic-vacancies340-приложение-b-сравнительная-матрицаmd-3-проблем)
  - [`docs/02-anthropic-vacancies/345-кто-ты.md` (3 проблем)](#docs02-anthropic-vacancies345-кто-тыmd-3-проблем)
  - [`docs/02-anthropic-vacancies/346-твоё-происхождение.md` (3 проблем)](#docs02-anthropic-vacancies346-твоё-происхождениеmd-3-проблем)
  - [`docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` (3 проблем)](#docs02-anthropic-vacancies352-что-ты-не-можешь-делать-без-max-approvalmd-3-проблем)
  - [`docs/02-anthropic-vacancies/359-твои-anti-patterns.md` (3 проблем)](#docs02-anthropic-vacancies359-твои-anti-patternsmd-3-проблем)
  - [`docs/05-habr-projects/01-synthesis.md` (3 проблем)](#docs05-habr-projects01-synthesismd-3-проблем)
  - [`docs/05-habr-projects/README.md` (3 проблем)](#docs05-habr-projectsreadmemd-3-проблем)
  - [`docs/05-habr-projects/knowledge/wikontic.md` (3 проблем)](#docs05-habr-projectsknowledgewikonticmd-3-проблем)
  - [`docs/ABBREVIATIONS.md` (3 проблем)](#docsabbreviationsmd-3-проблем)
  - [`docs/COMPARE.md` (3 проблем)](#docscomparemd-3-проблем)
  - [`docs/COST.md` (3 проблем)](#docscostmd-3-проблем)
  - [`docs/CROSSREFS.md` (3 проблем)](#docscrossrefsmd-3-проблем)
  - [`docs/DIGEST_WEEKLY.md` (3 проблем)](#docsdigest_weeklymd-3-проблем)
  - [`docs/KPI.md` (3 проблем)](#docskpimd-3-проблем)
  - [`docs/LANGUAGE_STATS.md` (3 проблем)](#docslanguage_statsmd-3-проблем)
  - [`docs/METRICS.md` (3 проблем)](#docsmetricsmd-3-проблем)
  - [`docs/ORPHANS.md` (3 проблем)](#docsorphansmd-3-проблем)
  - [`docs/PRIORITIES.md` (3 проблем)](#docsprioritiesmd-3-проблем)
  - [`docs/README.md` (3 проблем)](#docsreadmemd-3-проблем)
  - [`docs/SCHEDULE.md` (3 проблем)](#docsschedulemd-3-проблем)
  - [`docs/SEE_ALSO.md` (3 проблем)](#docssee_alsomd-3-проблем)
  - [`docs/VERSION_DIFF.md` (3 проблем)](#docsversion_diffmd-3-проблем)
  - [`docs/ai-collaborations/source-projects.md` (3 проблем)](#docsai-collaborationssource-projectsmd-3-проблем)
  - [`docs/anthropic-vacancies/README.md` (3 проблем)](#docsanthropic-vacanciesreadmemd-3-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md` (3 проблем)](#docsanthropic-vacanciesai-managed-virtual-company10-three-entry-pointsmd-3-проблем)
  - [`docs/anthropic-vacancies/methodology.md` (3 проблем)](#docsanthropic-vacanciesmethodologymd-3-проблем)
  - [`docs/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md` (3 проблем)](#docsanthropic-vacanciesnautilus-pro2-analysis01-shell-metaphor-two-projectionsmd-3-проблем)
  - [`docs/anthropic-vacancies/overview.md` (3 проблем)](#docsanthropic-vacanciesoverviewmd-3-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md` (3 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis03-secondary-beneficial-deploymentsmd-3-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md` (3 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis04-tertiary-research-engineer-agentsmd-3-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md` (3 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysis04-non-anthropic-pathsmd-3-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md` (3 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysis05-reality-check-distribution-gapmd-3-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md` (3 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-final01-three-archetypesmd-3-проблем)
  - [`docs/autofilled/components/.md` (3 проблем)](#docsautofilledcomponentsmd-3-проблем)
  - [`docs/autofilled/components/cowork.md` (3 проблем)](#docsautofilledcomponentscoworkmd-3-проблем)
  - [`docs/autofilled/components/ingit.md` (3 проблем)](#docsautofilledcomponentsingitmd-3-проблем)
  - [`docs/autofilled/components/kksudo.md` (3 проблем)](#docsautofilledcomponentskksudomd-3-проблем)
  - [`docs/autofilled/components/lorenzo.md` (3 проблем)](#docsautofilledcomponentslorenzomd-3-проблем)
  - [`docs/autofilled/components/nautilus.md` (3 проблем)](#docsautofilledcomponentsnautilusmd-3-проблем)
  - [`docs/autofilled/components/sgb.md` (3 проблем)](#docsautofilledcomponentssgbmd-3-проблем)
  - [`docs/autofilled/components/spbmolot.md` (3 проблем)](#docsautofilledcomponentsspbmolotmd-3-проблем)
  - [`docs/autofilled/components/svend4.md` (3 проблем)](#docsautofilledcomponentssvend4md-3-проблем)
  - [`docs/autofilled/components/svyazi.md` (3 проблем)](#docsautofilledcomponentssvyazimd-3-проблем)
  - [`docs/glossary/concepts.md` (3 проблем)](#docsglossaryconceptsmd-3-проблем)
  - [`docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md` (3 проблем)](#docshabr-unique-projectsdeep-pairs3-adversarial-multi-idemd-3-проблем)
  - [`docs/habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md` (3 проблем)](#docshabr-unique-projectsdeep-pairs4-skill-catalogs-subagentsmd-3-проблем)
  - [`docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md` (3 проблем)](#docshabr-unique-projectsdeep-pairs6-tmux-village-openclawmd-3-проблем)
  - [`docs/habr-unique-projects/final-ensembles/4-summary-authors.md` (3 проблем)](#docshabr-unique-projectsfinal-ensembles4-summary-authorsmd-3-проблем)
  - [`docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md` (3 проблем)](#docshabr-unique-projectskey-findings03-pda-llm-as-peripherymd-3-проблем)
  - [`docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md` (3 проблем)](#docshabr-unique-projectskey-findings05-supplementary-infrastructuremd-3-проблем)
  - [`docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md` (3 проблем)](#docshabr-unique-projectssoftware-pairs1-workflow-llm-mcpmd-3-проблем)
  - [`docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md` (3 проблем)](#docshabr-unique-projectssoftware-pairs3-crdt-self-hostedmd-3-проблем)
  - [`docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md` (3 проблем)](#docshabr-unique-projectssoftware-pairs4-speech-to-text-llmmd-3-проблем)
  - [`docs/lorenzo-agent/04-komu-ty-sluzhish.md` (3 проблем)](#docslorenzo-agent04-komu-ty-sluzhishmd-3-проблем)
  - [`docs/lorenzo-agent/09-voobshche-nelzya.md` (3 проблем)](#docslorenzo-agent09-voobshche-nelzyamd-3-проблем)
  - [`docs/lorenzo-agent/16-vsegda-delaesh.md` (3 проблем)](#docslorenzo-agent16-vsegda-delaeshmd-3-проблем)
  - [`docs/lorenzo-agent/18-escalate-to-max.md` (3 проблем)](#docslorenzo-agent18-escalate-to-maxmd-3-проблем)
  - [`docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md` (3 проблем)](#docsnautiluscommunity-discussionshabr-article-1-reaction00-question-habr-linkmd-3-проблем)
  - [`docs/nautilus/double-triangle-architecture/09-acknowledgments.md` (3 проблем)](#docsnautilusdouble-triangle-architecture09-acknowledgmentsmd-3-проблем)
  - [`docs/nautilus/double-triangle-architecture/10-references.md` (3 проблем)](#docsnautilusdouble-triangle-architecture10-referencesmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en10-what-not-solvedmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru09-ne-reshaetmd-3-проблем)
  - [`docs/nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md` (3 проблем)](#docsnautilusnpp-humanitarian-extension05-which-combination-more-valuablemd-3-проблем)
  - [`docs/nautilus/npp-v1-0/00-abstract-status.md` (3 проблем)](#docsnautilusnpp-v1-000-abstract-statusmd-3-проблем)
  - [`docs/nautilus/npp-v1-0/01-introduction.md` (3 проблем)](#docsnautilusnpp-v1-001-introductionmd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/10-open-questions.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-en10-open-questionsmd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/11-call-for-collaboration.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-en11-call-for-collaborationmd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/00-abstract.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-ru00-abstractmd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-ru10-otkrytye-voprosymd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-ru11-prizyv-k-sotrudnichestvumd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/00-abstract.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-ru00-abstractmd-3-проблем)
  - [`docs/svyazi-2-0/components/agent-memory-mcp.md` (3 проблем)](#docssvyazi-2-0componentsagent-memory-mcpmd-3-проблем)
  - [`docs/svyazi-2-0/components/svyazi.md` (3 проблем)](#docssvyazi-2-0componentssvyazimd-3-проблем)
  - [`docs/templates/decision-record.md` (3 проблем)](#docstemplatesdecision-recordmd-3-проблем)
  - [`docs/templates/ensemble.md` (3 проблем)](#docstemplatesensemblemd-3-проблем)
  - [`docs/01-svyazi/README.md` (2 проблем)](#docs01-svyazireadmemd-2-проблем)
  - [`docs/02-anthropic-vacancies/README.md` (2 проблем)](#docs02-anthropic-vacanciesreadmemd-2-проблем)
  - [`docs/05-habr-projects/README.md` (2 проблем)](#docs05-habr-projectsreadmemd-2-проблем)
  - [`docs/ALERTS.md` (2 проблем)](#docsalertsmd-2-проблем)
  - [`docs/CONTACT_PRIORITY.md` (2 проблем)](#docscontact_prioritymd-2-проблем)
  - [`docs/COVERAGE.md` (2 проблем)](#docscoveragemd-2-проблем)
  - [`docs/KPI.md` (2 проблем)](#docskpimd-2-проблем)
  - [`docs/LINKS.md` (2 проблем)](#docslinksmd-2-проблем)
  - [`docs/GRAPH.md` (2 проблем)](#docsgraphmd-2-проблем)
  - [`docs/LINKS.md` (2 проблем)](#docslinksmd-2-проблем)
  - [`docs/REGISTRY.md` (2 проблем)](#docsregistrymd-2-проблем)
  - [`docs/SCORING.md` (2 проблем)](#docsscoringmd-2-проблем)
  - [`docs/SOURCE_MAP.md` (2 проблем)](#docssource_mapmd-2-проблем)
  - [`docs/STALENESS.md` (2 проблем)](#docsstalenessmd-2-проблем)
  - [`docs/STATS.md` (2 проблем)](#docsstatsmd-2-проблем)
  - [`docs/ai-collaborations/strategy/README.md` (2 проблем)](#docsai-collaborationsstrategyreadmemd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/01-ai-research-engineering.md` (2 проблем)](#docsanthropic-vacanciesclusters01-ai-research-engineeringmd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/02-sales.md` (2 проблем)](#docsanthropic-vacanciesclusters02-salesmd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/03-finance.md` (2 проблем)](#docsanthropic-vacanciesclusters03-financemd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/04-security.md` (2 проблем)](#docsanthropic-vacanciesclusters04-securitymd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/05-marketing-brand.md` (2 проблем)](#docsanthropic-vacanciesclusters05-marketing-brandmd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/06-engineering-design-product.md` (2 проблем)](#docsanthropic-vacanciesclusters06-engineering-design-productmd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md` (2 проблем)](#docsanthropic-vacanciesclusters07-software-engineering-infrastructuremd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/08-safeguards-trust-safety.md` (2 проблем)](#docsanthropic-vacanciesclusters08-safeguards-trust-safetymd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/09-product-management-support-ops.md` (2 проблем)](#docsanthropic-vacanciesclusters09-product-management-support-opsmd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/10-compute.md` (2 проблем)](#docsanthropic-vacanciesclusters10-computemd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/11-legal.md` (2 проблем)](#docsanthropic-vacanciesclusters11-legalmd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/12-technical-program-management.md` (2 проблем)](#docsanthropic-vacanciesclusters12-technical-program-managementmd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/13-communications.md` (2 проблем)](#docsanthropic-vacanciesclusters13-communicationsmd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/14-public-policy.md` (2 проблем)](#docsanthropic-vacanciesclusters14-public-policymd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/15-public-benefit.md` (2 проблем)](#docsanthropic-vacanciesclusters15-public-benefitmd-2-проблем)
  - [`docs/anthropic-vacancies/clusters/16-people.md` (2 проблем)](#docsanthropic-vacanciesclusters16-peoplemd-2-проблем)
  - [`docs/anthropic-vacancies/mmorpg-for-programmers/README.md` (2 проблем)](#docsanthropic-vacanciesmmorpg-for-programmersreadmemd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis01-profile-five-layersmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis07-unique-niche-eu-legal-inframd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis08-practical-rankingmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysis01-fde-downgradedmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysisreadmemd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-final04-stronger-paths-outside-anthropicmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-finalreadmemd-2-проблем)
  - [`docs/badges/README.md` (2 проблем)](#docsbadgesreadmemd-2-проблем)
  - [`docs/glossary/authors-by-name.md` (2 проблем)](#docsglossaryauthors-by-namemd-2-проблем)
  - [`docs/habr-unique-projects/README.md` (2 проблем)](#docshabr-unique-projectsreadmemd-2-проблем)
  - [`docs/habr-unique-projects/hardware-pairs/README.md` (2 проблем)](#docshabr-unique-projectshardware-pairsreadmemd-2-проблем)
  - [`docs/habr-unique-projects/key-findings/README.md` (2 проблем)](#docshabr-unique-projectskey-findingsreadmemd-2-проблем)
  - [`docs/habr-unique-projects/software-pairs/README.md` (2 проблем)](#docshabr-unique-projectssoftware-pairsreadmemd-2-проблем)
  - [`docs/lorenzo-agent/00-intro.md` (2 проблем)](#docslorenzo-agent00-intromd-2-проблем)
  - [`docs/lorenzo-agent/01-kto-ty.md` (2 проблем)](#docslorenzo-agent01-kto-tymd-2-проблем)
  - [`docs/lorenzo-agent/02-tvoyo-proishozhdenie.md` (2 проблем)](#docslorenzo-agent02-tvoyo-proishozhdeniemd-2-проблем)
  - [`docs/lorenzo-agent/08-bez-max-approval.md` (2 проблем)](#docslorenzo-agent08-bez-max-approvalmd-2-проблем)
  - [`docs/lorenzo-agent/17-honestly-ne-znaesh.md` (2 проблем)](#docslorenzo-agent17-honestly-ne-znaeshmd-2-проблем)
  - [`docs/lorenzo-agent/README.md` (2 проблем)](#docslorenzo-agentreadmemd-2-проблем)
  - [`docs/lorenzo-agent/naming/README.md` (2 проблем)](#docslorenzo-agentnamingreadmemd-2-проблем)
  - [`docs/nautilus/composite-skills-agents-companion-mentors/README.md` (2 проблем)](#docsnautiluscomposite-skills-agents-companion-mentorsreadmemd-2-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md` (2 проблем)](#docsnautilusinfrastructure-layer-b-en09-what-industry-will-buildmd-2-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md` (2 проблем)](#docsnautilusinfrastructure-layer-b-ru08-promyshlennost-postroitmd-2-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md` (2 проблем)](#docsnautilusinfrastructure-layer-b-ru11-zaklyucheniemd-2-проблем)
  - [`docs/nautilus/npp-humanitarian-extension/README.md` (2 проблем)](#docsnautilusnpp-humanitarian-extensionreadmemd-2-проблем)
  - [`docs/nautilus/npp-v1-1/14-sdk.md` (2 проблем)](#docsnautilusnpp-v1-114-sdkmd-2-проблем)
  - [`docs/nautilus/privacy-federation/README.md` (2 проблем)](#docsnautilusprivacy-federationreadmemd-2-проблем)
  - [`docs/nautilus/representative-agent-layer-en/11-call-for-collaboration.md` (2 проблем)](#docsnautilusrepresentative-agent-layer-en11-call-for-collaborationmd-2-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md` (2 проблем)](#docsnautilusrepresentative-agent-layer-ru11-prizyv-k-sotrudnichestvumd-2-проблем)
  - [`docs/svyazi-2-0/overview/README.md` (2 проблем)](#docssvyazi-2-0overviewreadmemd-2-проблем)
  - [`docs/svyazi-2-0/prototype/README.md` (2 проблем)](#docssvyazi-2-0prototypereadmemd-2-проблем)
  - [`docs/svyazi-2-0/security/README.md` (2 проблем)](#docssvyazi-2-0securityreadmemd-2-проблем)
  - [`docs/technology-combinations/research-reports/sozialrecht-35-combinations.md` (2 проблем)](#docstechnology-combinationsresearch-reportssozialrecht-35-combinationsmd-2-проблем)
  - [`docs/technology-combinations/synthesis-tables/README.md` (2 проблем)](#docstechnology-combinationssynthesis-tablesreadmemd-2-проблем)
  - [`docs/templates/contact-outreach.md` (2 проблем)](#docstemplatescontact-outreachmd-2-проблем)
  - [`docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` (1 проблем)](#docs02-anthropic-vacancies348-кому-ты-служишь-слоистая-модельmd-1-проблем)
  - [`docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` (1 проблем)](#docs02-anthropic-vacancies361-когда-ты-honestly-не-знаешьmd-1-проблем)
  - [`docs/02-anthropic-vacancies/README.md` (1 проблем)](#docs02-anthropic-vacanciesreadmemd-1-проблем)
  - [`docs/03-technology-combinations/README.md` (1 проблем)](#docs03-technology-combinationsreadmemd-1-проблем)
  - [`docs/04-ai-collaborations/README.md` (1 проблем)](#docs04-ai-collaborationsreadmemd-1-проблем)
  - [`docs/05-habr-projects/memory/README.md` (1 проблем)](#docs05-habr-projectsmemoryreadmemd-1-проблем)
  - [`docs/BADGES.md` (1 проблем)](#docsbadgesmd-1-проблем)
  - [`docs/COVERAGE.md` (1 проблем)](#docscoveragemd-1-проблем)
  - [`docs/DEPENDABOT.md` (1 проблем)](#docsdependabotmd-1-проблем)
  - [`docs/ENTITIES.md` (1 проблем)](#docsentitiesmd-1-проблем)
  - [`docs/MCP_DASHBOARD.md` (1 проблем)](#docsmcp_dashboardmd-1-проблем)
  - [`docs/MINDMAP.md` (1 проблем)](#docsmindmapmd-1-проблем)
  - [`docs/SEARCH_RESULTS.md` (1 проблем)](#docssearch_resultsmd-1-проблем)
  - [`docs/autofilled/components/README.md` (1 проблем)](#docsautofilledcomponentsreadmemd-1-проблем)
  - [`docs/contacts/README.md` (1 проблем)](#docscontactsreadmemd-1-проблем)
  - [`docs/glossary/README.md` (1 проблем)](#docsglossaryreadmemd-1-проблем)
  - [`docs/habr-unique-projects/analogues/README.md` (1 проблем)](#docshabr-unique-projectsanaloguesreadmemd-1-проблем)
  - [`docs/habr-unique-projects/deep-pairs/README.md` (1 проблем)](#docshabr-unique-projectsdeep-pairsreadmemd-1-проблем)
  - [`docs/habr-unique-projects/extra-examples/README.md` (1 проблем)](#docshabr-unique-projectsextra-examplesreadmemd-1-проблем)
  - [`docs/habr-unique-projects/final-ensembles/README.md` (1 проблем)](#docshabr-unique-projectsfinal-ensemblesreadmemd-1-проблем)
  - [`docs/lorenzo-agent/operationalized/README.md` (1 проблем)](#docslorenzo-agentoperationalizedreadmemd-1-проблем)
  - [`docs/lorenzo-agent/phased-deployment/README.md` (1 проблем)](#docslorenzo-agentphased-deploymentreadmemd-1-проблем)
  - [`docs/lorenzo-agent/scenarios/README.md` (1 проблем)](#docslorenzo-agentscenariosreadmemd-1-проблем)
  - [`docs/lorenzo-agent/specification/README.md` (1 проблем)](#docslorenzo-agentspecificationreadmemd-1-проблем)
  - [`docs/nautilus/README.md` (1 проблем)](#docsnautilusreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/agent-changes-reality/README.md` (1 проблем)](#docsnautiluscommunity-discussionsagent-changes-realityreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/habr-article-1-reaction/README.md` (1 проблем)](#docsnautiluscommunity-discussionshabr-article-1-reactionreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/habr-article-2-reaction/README.md` (1 проблем)](#docsnautiluscommunity-discussionshabr-article-2-reactionreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/practical-observations/README.md` (1 проблем)](#docsnautiluscommunity-discussionspractical-observationsreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/voiceless-contributors/README.md` (1 проблем)](#docsnautiluscommunity-discussionsvoiceless-contributorsreadmemd-1-проблем)
  - [`docs/nautilus/composite-skills-agents/README.md` (1 проблем)](#docsnautiluscomposite-skills-agentsreadmemd-1-проблем)
  - [`docs/nautilus/double-triangle-architecture/README.md` (1 проблем)](#docsnautilusdouble-triangle-architecturereadmemd-1-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/12-closing.md` (1 проблем)](#docsnautilusinfrastructure-layer-b-en12-closingmd-1-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/README.md` (1 проблем)](#docsnautilusinfrastructure-layer-b-enreadmemd-1-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/README.md` (1 проблем)](#docsnautilusinfrastructure-layer-b-rureadmemd-1-проблем)
  - [`docs/nautilus/ingit-cowork-en/README.md` (1 проблем)](#docsnautilusingit-cowork-enreadmemd-1-проблем)
  - [`docs/nautilus/ingit-cowork-ru/README.md` (1 проблем)](#docsnautilusingit-cowork-rureadmemd-1-проблем)
  - [`docs/nautilus/innovation-transitions/README.md` (1 проблем)](#docsnautilusinnovation-transitionsreadmemd-1-проблем)
  - [`docs/nautilus/multi-tier-architecture/README.md` (1 проблем)](#docsnautilusmulti-tier-architecturereadmemd-1-проблем)
  - [`docs/nautilus/npp-v1-0/README.md` (1 проблем)](#docsnautilusnpp-v1-0readmemd-1-проблем)
  - [`docs/nautilus/npp-v1-1/README.md` (1 проблем)](#docsnautilusnpp-v1-1readmemd-1-проблем)
  - [`docs/nautilus/okwf-concept/README.md` (1 проблем)](#docsnautilusokwf-conceptreadmemd-1-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/README.md` (1 проблем)](#docsnautilusprofessional-colleague-agents-enreadmemd-1-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/README.md` (1 проблем)](#docsnautilusprofessional-colleague-agents-rureadmemd-1-проблем)
  - [`docs/nautilus/representative-agent-layer-en/README.md` (1 проблем)](#docsnautilusrepresentative-agent-layer-enreadmemd-1-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/README.md` (1 проблем)](#docsnautilusrepresentative-agent-layer-rureadmemd-1-проблем)
  - [`docs/nautilus/review-methodology/README.md` (1 проблем)](#docsnautilusreview-methodologyreadmemd-1-проблем)
  - [`docs/nautilus/supply-demand/README.md` (1 проблем)](#docsnautilussupply-demandreadmemd-1-проблем)
  - [`docs/nautilus/transmission-box/README.md` (1 проблем)](#docsnautilustransmission-boxreadmemd-1-проблем)
  - [`docs/svyazi-2-0/README.md` (1 проблем)](#docssvyazi-2-0readmemd-1-проблем)
  - [`docs/svyazi-2-0/architecture/README.md` (1 проблем)](#docssvyazi-2-0architecturereadmemd-1-проблем)
  - [`docs/svyazi-2-0/components/README.md` (1 проблем)](#docssvyazi-2-0componentsreadmemd-1-проблем)
  - [`docs/svyazi-2-0/ensembles/README.md` (1 проблем)](#docssvyazi-2-0ensemblesreadmemd-1-проблем)
  - [`docs/svyazi-2-0/limitations/README.md` (1 проблем)](#docssvyazi-2-0limitationsreadmemd-1-проблем)
  - [`docs/svyazi-2-0/outreach/README.md` (1 проблем)](#docssvyazi-2-0outreachreadmemd-1-проблем)
  - [`docs/technology-combinations/README.md` (1 проблем)](#docstechnology-combinationsreadmemd-1-проблем)
  - [`docs/technology-combinations/combinations/README.md` (1 проблем)](#docstechnology-combinationscombinationsreadmemd-1-проблем)
  - [`docs/technology-combinations/mega-stacks/README.md` (1 проблем)](#docstechnology-combinationsmega-stacksreadmemd-1-проблем)
  - [`docs/technology-combinations/properties/README.md` (1 проблем)](#docstechnology-combinationspropertiesreadmemd-1-проблем)
  - [`docs/technology-combinations/research-reports/README.md` (1 проблем)](#docstechnology-combinationsresearch-reportsreadmemd-1-проблем)
  - [`docs/templates/README.md` (1 проблем)](#docstemplatesreadmemd-1-проблем)

---

<!-- tags: memory, rag, security, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->




_Обновлено: 2026-04-29_

Файлов с проблемами: **1176**

## Типы проблем

| Тип | Кол-во |
|-----|--------|
| ⚪ Короткий абзац | 5311 |
| ✂️  Оборванный | 3697 |
| 📏 Длинное предложение | 182 |
| 🔁 Повтор начала | 1606 |
| ♊ Дубль | 318 |

## По файлам

### `docs/CONCEPTS.md` (1444 проблем)

_абзац: 698, Оборванный: 537, начала: 205, Дубль: 4_


### `docs/TABLES.md` (1109 проблем)

_абзац: 531, начала: 512, Дубль: 57, Оборванный: 9_


### `docs/TABLES.md` (910 проблем)

_абзац: 433, начала: 420, Дубль: 34, Оборванный: 14, предложение: 9_


### `docs/QA.md` (186 проблем)

_абзац: 94, начала: 87, Оборванный: 4, Дубль: 1_


### `docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md` (218 проблем)

_абзац: 138, Дубль: 1, Оборванный: 44, предложение: 5, начала: 30_


### `docs/nautilus/transmission-box/01-completing-loop.md` (183 проблем)

_абзац: 146, Дубль: 1, Оборванный: 27, начала: 9_


### `docs/lorenzo-agent/naming/03-dhlab-umbrella.md` (167 проблем)

_абзац: 143, Оборванный: 16, Дубль: 1, начала: 7_


### `docs/QA.md` (165 проблем)

_абзац: 81, начала: 80, Оборванный: 3, Дубль: 1_


### `docs/lorenzo-agent/scenarios/01-response.md` (164 проблем)

_Оборванный: 23, Дубль: 1, абзац: 124, начала: 16_


### `docs/QUESTIONS.md` (160 проблем)

_абзац: 68, Оборванный: 73, Дубль: 10, начала: 9_


### `docs/lorenzo-agent/specification/11-difficulties-and-recommendations.md` (160 проблем)

_абзац: 117, Оборванный: 17, Дубль: 1, начала: 25_


### `docs/nautilus/multi-tier-architecture/01-strategic-significance.md` (144 проблем)

_Дубль: 1, абзац: 110, Оборванный: 9, начала: 24_


### `docs/SIMILAR_PASSAGES.md` (128 проблем)

_абзац: 5, Оборванный: 55, Дубль: 18, начала: 50_


### `docs/DUPLICATES.md` (127 проблем)

_абзац: 34, Оборванный: 88, начала: 3_


### `docs/CONTRADICTIONS.md` (117 проблем)

_абзац: 88, Оборванный: 12, Дубль: 14, начала: 3_


### `docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md` (123 проблем)

_абзац: 93, Оборванный: 14, Дубль: 1, предложение: 1, начала: 14_


### `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` (94 проблем)

_абзац: 16, Оборванный: 41, предложение: 37_


### `docs/DUPLICATES.md` (92 проблем)

_абзац: 32, Оборванный: 57, начала: 3_


### `docs/CLUSTERS.md` (79 проблем)

_абзац: 11, Оборванный: 36, предложение: 1, начала: 30, Дубль: 1_


### `docs/DECISIONS.md` (75 проблем)

_абзац: 7, Оборванный: 60, Дубль: 1, начала: 7_


### `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` (69 проблем)

_абзац: 18, Оборванный: 31, предложение: 7, начала: 13_


### `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` (69 проблем)

_Оборванный: 30, предложение: 21, абзац: 11, начала: 6, Дубль: 1_


### `docs/SPELLCHECK.md` (63 проблем)

_абзац: 33, начала: 30_


### `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` (58 проблем)

_абзац: 19, Оборванный: 21, предложение: 18_


### `docs/04-ai-collaborations/00-intro.md` (49 проблем)

_абзац: 30, Оборванный: 13, предложение: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/QA.md` (47 проблем)

_абзац: 23, начала: 23, Оборванный: 1_


### `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` (46 проблем)

_абзац: 16, Оборванный: 21, начала: 9_


### `docs/anthropic-vacancies/hermes-comparison/13-reprioritization.md` (44 проблем)

_абзац: 31, Оборванный: 1, Дубль: 1, начала: 11_


### `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` (45 проблем)

_абзац: 12, Оборванный: 5, начала: 28_


### `docs/02-anthropic-vacancies/218-7-application-domains.md` (45 проблем)

_абзац: 40, Оборванный: 5_


### `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` (44 проблем)

_абзац: 14, Оборванный: 2, начала: 28_


### `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` (43 проблем)

_абзац: 33, Оборванный: 6, начала: 3, Дубль: 1_


### `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` (42 проблем)

_абзац: 16, Оборванный: 17, начала: 9_


### `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` (41 проблем)

_абзац: 27, Оборванный: 13, Дубль: 1_


### `docs/02-anthropic-vacancies/165-closing.md` (41 проблем)

_абзац: 11, Оборванный: 10, предложение: 8, начала: 11, Дубль: 1_


### `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` (40 проблем)

_абзац: 34, Оборванный: 5, Дубль: 1_


### `docs/05-habr-projects/memory/memnet.md` (40 проблем)

_Оборванный: 7, абзац: 15, предложение: 6, начала: 10, Дубль: 2_


### `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` (38 проблем)

_абзац: 13, Оборванный: 25_


### `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` (38 проблем)

_абзац: 33, Оборванный: 5_


### `docs/02-anthropic-vacancies/238-7-области-применения.md` (37 проблем)

_Оборванный: 4, Дубль: 1, абзац: 32_


### `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` (36 проблем)

_Оборванный: 5, абзац: 31_


### `docs/02-anthropic-vacancies/69-section.md` (36 проблем)

_абзац: 20, Оборванный: 15, предложение: 1_


### `docs/01-svyazi/04-ensembles-overview.md` (35 проблем)

_абзац: 20, Оборванный: 15_


### `docs/04-ai-collaborations/QA.md` (35 проблем)

_абзац: 18, начала: 16, Оборванный: 1_


### `docs/01-svyazi/QA.md` (34 проблем)

_абзац: 17, начала: 16, Оборванный: 1_


### `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` (34 проблем)

_Оборванный: 13, Дубль: 3, начала: 4, абзац: 14_


### `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` (33 проблем)

_абзац: 15, Оборванный: 12, предложение: 3, начала: 3_


### `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` (33 проблем)

_абзац: 9, Оборванный: 6, начала: 17, Дубль: 1_


### `docs/02-anthropic-vacancies/68-about.md` (33 проблем)

_абзац: 19, Оборванный: 13, Дубль: 1_


### `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` (32 проблем)

_абзац: 7, Оборванный: 19, предложение: 6_


### `docs/01-svyazi/01-executive-summary.md` (31 проблем)

_Оборванный: 10, Дубль: 2, абзац: 16, начала: 3_


### `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` (31 проблем)

_абзац: 20, Оборванный: 11_


### `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` (31 проблем)

_абзац: 18, Оборванный: 13_


### `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` (30 проблем)

_абзац: 6, Оборванный: 14, предложение: 10_


### `docs/02-anthropic-vacancies/159-5-economic-model.md` (30 проблем)

_Оборванный: 14, Дубль: 1, абзац: 7, начала: 8_


### `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` (30 проблем)

_Оборванный: 16, Дубль: 1, абзац: 5, начала: 8_


### `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` (30 проблем)

_абзац: 14, Оборванный: 11, Дубль: 1, предложение: 4_


### `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` (30 проблем)

_абзац: 16, Оборванный: 13, Дубль: 1_


### `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` (30 проблем)

_абзац: 18, Оборванный: 12_


### `docs/02-anthropic-vacancies/67-о-проекте.md` (30 проблем)

_абзац: 18, Оборванный: 12_


### `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` (30 проблем)

_абзац: 17, Оборванный: 12, предложение: 1_


### `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` (29 проблем)

_абзац: 16, Оборванный: 10, предложение: 3_


### `docs/RISK_REGISTER.md` (29 проблем)

_абзац: 24, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/133-обратная-связь.md` (28 проблем)

_абзац: 11, Дубль: 1, Оборванный: 10, предложение: 6_


### `docs/02-anthropic-vacancies/164-10-appendices.md` (28 проблем)

_абзац: 11, Оборванный: 12, начала: 5_


### `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` (28 проблем)

_абзац: 7, Оборванный: 5, начала: 15, Дубль: 1_


### `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` (28 проблем)

_Оборванный: 8, Дубль: 1, абзац: 10, начала: 9_


### `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` (28 проблем)

_абзац: 19, Оборванный: 9_


### `docs/02-anthropic-vacancies/00-intro.md` (27 проблем)

_абзац: 10, Оборванный: 12, Дубль: 1, предложение: 4_


### `docs/02-anthropic-vacancies/162-8-risk-analysis.md` (27 проблем)

_абзац: 11, Оборванный: 16_


### `docs/02-anthropic-vacancies/179-10-open-questions.md` (27 проблем)

_Оборванный: 6, абзац: 21_


### `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` (27 проблем)

_абзац: 10, Оборванный: 7, начала: 9, Дубль: 1_


### `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` (27 проблем)

_абзац: 16, Оборванный: 9, предложение: 2_


### `docs/01-svyazi/07-mvp-planning.md` (26 проблем)

_Оборванный: 6, Дубль: 1, абзац: 19_


### `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` (26 проблем)

_абзац: 19, начала: 3, Оборванный: 4_


### `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` (26 проблем)

_Оборванный: 10, Дубль: 1, абзац: 8, начала: 7_


### `docs/02-anthropic-vacancies/174-5-architectural-specification.md` (26 проблем)

_абзац: 7, Оборванный: 6, начала: 13_


### `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` (26 проблем)

_абзац: 9, Оборванный: 8, начала: 9_


### `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` (26 проблем)

_Оборванный: 12, Дубль: 1, абзац: 13_


### `docs/TAGS.md` (26 проблем)

_абзац: 1, Оборванный: 12, начала: 12, Дубль: 1_


### `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` (25 проблем)

_Оборванный: 11, абзац: 10, начала: 3, Дубль: 1_


### `docs/02-anthropic-vacancies/156-2-target-populations.md` (25 проблем)

_абзац: 8, Оборванный: 17_


### `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` (25 проблем)

_Оборванный: 8, Дубль: 1, абзац: 16_


### `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` (25 проблем)

_Оборванный: 14, Дубль: 1, абзац: 10_


### `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` (25 проблем)

_абзац: 8, Оборванный: 4, начала: 13_


### `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` (25 проблем)

_Оборванный: 11, Дубль: 2, абзац: 12_


### `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` (25 проблем)

_абзац: 7, Оборванный: 14, Дубль: 1, предложение: 3_


### `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` (25 проблем)

_Оборванный: 12, Дубль: 1, абзац: 9, начала: 3_


### `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` (25 проблем)

_абзац: 14, Оборванный: 11_


### `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` (25 проблем)

_абзац: 13, Оборванный: 9, предложение: 3_


### `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` (25 проблем)

_абзац: 11, Оборванный: 14_


### `docs/01-svyazi/10-second-order-ensembles.md` (24 проблем)

_абзац: 13, Оборванный: 11_


### `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` (24 проблем)

_абзац: 7, Оборванный: 11, предложение: 1, начала: 5_


### `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` (24 проблем)

_абзац: 10, Оборванный: 7, начала: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` (24 проблем)

_Оборванный: 17, Дубль: 1, абзац: 6_


### `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` (24 проблем)

_абзац: 12, Оборванный: 11, предложение: 1_


### `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` (24 проблем)

_абзац: 7, Оборванный: 5, начала: 11, Дубль: 1_


### `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` (24 проблем)

_Оборванный: 7, Дубль: 2, абзац: 10, начала: 5_


### `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` (24 проблем)

_абзац: 10, начала: 7, Оборванный: 7_


### `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` (24 проблем)

_абзац: 9, Оборванный: 7, начала: 8_


### `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` (24 проблем)

_абзац: 8, Оборванный: 12, предложение: 4_


### `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` (24 проблем)

_Оборванный: 11, Дубль: 1, абзац: 12_


### `docs/02-anthropic-vacancies/90-15-security-considerations.md` (24 проблем)

_Оборванный: 9, абзац: 13, Дубль: 2_


### `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` (24 проблем)

_абзац: 12, Оборванный: 12_


### `docs/01-svyazi/11-integration-contracts.md` (23 проблем)

_абзац: 13, Оборванный: 9, Дубль: 1_


### `docs/01-svyazi/13-contacts.md` (23 проблем)

_абзац: 11, Оборванный: 12_


### `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` (23 проблем)

_Оборванный: 11, Дубль: 2, абзац: 10_


### `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` (23 проблем)

_Оборванный: 2, абзац: 20, Дубль: 1_


### `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` (23 проблем)

_абзац: 8, Оборванный: 7, начала: 8_


### `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` (23 проблем)

_абзац: 10, Оборванный: 8, начала: 5_


### `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` (23 проблем)

_абзац: 11, Оборванный: 9, начала: 3_


### `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` (23 проблем)

_абзац: 11, Оборванный: 12_


### `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` (23 проблем)

_Оборванный: 6, Дубль: 2, абзац: 12, начала: 3_


### `docs/04-ai-collaborations/01-executive-summary.md` (23 проблем)

_Оборванный: 3, Дубль: 1, абзац: 20_


### `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` (23 проблем)

_абзац: 13, Оборванный: 10_


### `docs/02-anthropic-vacancies/179-10-open-questions.md` (23 проблем)

_Оборванный: 3, абзац: 20_


### `docs/01-svyazi/09-architectural-gaps.md` (22 проблем)

_абзац: 14, Оборванный: 8_


### `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` (22 проблем)

_абзац: 14, Оборванный: 8_


### `docs/02-anthropic-vacancies/175-6-ethical-framework.md` (22 проблем)

_Оборванный: 11, Дубль: 1, абзац: 10_


### `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` (22 проблем)

_абзац: 10, Оборванный: 8, предложение: 4_


### `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` (22 проблем)

_абзац: 9, Оборванный: 12, Дубль: 1_


### `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` (22 проблем)

_Оборванный: 10, Дубль: 2, абзац: 10_


### `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` (22 проблем)

_Оборванный: 6, абзац: 8, начала: 9_


### `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` (22 проблем)

_Оборванный: 9, абзац: 12, Дубль: 1_


### `docs/NARRATIVE.md` (22 проблем)

_абзац: 7, Оборванный: 12, предложение: 2, Дубль: 1_


### `docs/01-svyazi/06-security-privacy.md` (21 проблем)

_абзац: 12, Оборванный: 9_


### `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` (21 проблем)

_абзац: 12, Оборванный: 8, Дубль: 1_


### `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` (21 проблем)

_абзац: 10, Оборванный: 11_


### `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` (21 проблем)

_абзац: 5, Оборванный: 16_


### `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` (21 проблем)

_абзац: 8, Оборванный: 7, начала: 5, предложение: 1_


### `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` (21 проблем)

_Оборванный: 5, предложение: 1, абзац: 7, начала: 8_


### `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` (21 проблем)

_абзац: 8, Оборванный: 4, начала: 8, Дубль: 1_


### `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` (21 проблем)

_Оборванный: 14, Дубль: 1, абзац: 6_


### `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` (21 проблем)

_абзац: 8, Оборванный: 5, начала: 8_


### `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` (21 проблем)

_абзац: 10, Оборванный: 5, начала: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` (21 проблем)

_абзац: 6, Оборванный: 9, начала: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/279-existing-approximations.md` (21 проблем)

_Оборванный: 12, Дубль: 2, абзац: 7_


### `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` (21 проблем)

_Оборванный: 6, Дубль: 1, абзац: 11, начала: 3_


### `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` (21 проблем)

_Оборванный: 3, абзац: 9, начала: 9_


### `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` (21 проблем)

_Оборванный: 8, абзац: 13_


### `docs/04-ai-collaborations/07-выводы.md` (21 проблем)

_Оборванный: 8, абзац: 13_


### `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` (21 проблем)

_абзац: 10, Оборванный: 11_


### `docs/CITATION_INDEX.md` (21 проблем)

_Оборванный: 6, абзац: 12, предложение: 3_


### `docs/01-svyazi/02-methodology.md` (20 проблем)

_абзац: 13, Оборванный: 4, начала: 3_


### `docs/01-svyazi/12-roadmap.md` (20 проблем)

_абзац: 10, Оборванный: 10_


### `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` (20 проблем)

_абзац: 8, Оборванный: 8, начала: 4_


### `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` (20 проблем)

_абзац: 6, Оборванный: 5, начала: 8, Дубль: 1_


### `docs/02-anthropic-vacancies/294-существующие-приближения.md` (20 проблем)

_Оборванный: 11, Дубль: 2, абзац: 7_


### `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` (20 проблем)

_абзац: 10, Оборванный: 10_


### `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` (20 проблем)

_абзац: 16, Дубль: 1, Оборванный: 4_


### `docs/CONSISTENCY.md` (20 проблем)

_Оборванный: 10, абзац: 5, начала: 5_


### `docs/ONBOARDING.md` (20 проблем)

_абзац: 11, Оборванный: 8, Дубль: 1_


### `docs/01-svyazi/14-limitations.md` (19 проблем)

_абзац: 8, Оборванный: 11_


### `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` (19 проблем)

_абзац: 9, Оборванный: 9, Дубль: 1_


### `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` (19 проблем)

_абзац: 8, Оборванный: 8, начала: 3_


### `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` (19 проблем)

_абзац: 7, Оборванный: 7, начала: 5_


### `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` (19 проблем)

_абзац: 5, Оборванный: 13, Дубль: 1_


### `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` (19 проблем)

_абзац: 5, начала: 8, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` (19 проблем)

_Оборванный: 7, Дубль: 3, абзац: 5, начала: 4_


### `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` (19 проблем)

_Оборванный: 9, Дубль: 3, абзац: 7_


### `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` (19 проблем)

_Оборванный: 7, начала: 6, абзац: 6_


### `docs/CHANGELOG_AUTO.md` (19 проблем)

_абзац: 10, Дубль: 1, Оборванный: 6, предложение: 2_


### `docs/INDEX.md` (19 проблем)

_абзац: 15, Оборванный: 4_


### `docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md` (19 проблем)

_Дубль: 1, абзац: 17, Оборванный: 1_


### `docs/02-anthropic-vacancies/144-7-open-questions.md` (18 проблем)

_абзац: 11, Оборванный: 7_


### `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` (18 проблем)

_Оборванный: 4, абзац: 14_


### `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` (18 проблем)

_Дубль: 1, Оборванный: 7, абзац: 11_


### `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` (18 проблем)

_абзац: 6, Оборванный: 4, начала: 8_


### `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` (18 проблем)

_абзац: 8, Оборванный: 10_


### `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` (18 проблем)

_абзац: 6, начала: 8, Оборванный: 3, Дубль: 1_


### `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` (18 проблем)

_Оборванный: 3, Дубль: 1, абзац: 11, начала: 3_


### `docs/03-technology-combinations/02-knowledge-graphs.md` (18 проблем)

_абзац: 5, Оборванный: 9, начала: 4_


### `docs/LLM_SUMMARIES.md` (18 проблем)

_абзац: 15, Оборванный: 3_


### `docs/01-svyazi/03-component-catalog.md` (17 проблем)

_абзац: 12, Оборванный: 5_


### `docs/01-svyazi/08-conclusions.md` (17 проблем)

_Оборванный: 7, абзац: 10_


### `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` (17 проблем)

_абзац: 9, начала: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` (17 проблем)

_абзац: 13, Оборванный: 4_


### `docs/02-anthropic-vacancies/130-отладка.md` (17 проблем)

_Оборванный: 5, абзац: 12_


### `docs/02-anthropic-vacancies/18-6-adapter-interface.md` (17 проблем)

_Оборванный: 8, абзац: 8, Дубль: 1_


### `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` (17 проблем)

_Дубль: 1, Оборванный: 6, абзац: 10_


### `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` (17 проблем)

_Оборванный: 8, Дубль: 2, абзац: 7_


### `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` (17 проблем)

_Оборванный: 7, абзац: 5, начала: 5_


### `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` (17 проблем)

_абзац: 8, Оборванный: 7, предложение: 1, Дубль: 1_


### `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` (17 проблем)

_абзац: 10, Оборванный: 7_


### `docs/02-anthropic-vacancies/320-references.md` (17 проблем)

_Оборванный: 6, абзац: 8, начала: 3_


### `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` (17 проблем)

_абзац: 7, Оборванный: 6, начала: 4_


### `docs/02-anthropic-vacancies/338-ссылки.md` (17 проблем)

_Оборванный: 6, абзац: 8, начала: 3_


### `docs/02-anthropic-vacancies/356-твой-workflow.md` (17 проблем)

_абзац: 9, Оборванный: 7, Дубль: 1_


### `docs/02-anthropic-vacancies/81-6-adapter-interface.md` (17 проблем)

_Оборванный: 8, абзац: 9_


### `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` (17 проблем)

_Оборванный: 6, Дубль: 1, абзац: 10_


### `docs/02-anthropic-vacancies/92-17-versioning-policy.md` (17 проблем)

_Оборванный: 8, абзац: 9_


### `docs/03-technology-combinations/QA.md` (17 проблем)

_абзац: 10, начала: 7_


### `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` (17 проблем)

_абзац: 8, Оборванный: 9_


### `docs/02-anthropic-vacancies/104-appendix-c-references.md` (16 проблем)

_Оборванный: 9, абзац: 7_


### `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` (16 проблем)

_Оборванный: 8, абзац: 8_


### `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` (16 проблем)

_Дубль: 1, абзац: 16_


### `docs/nautilus/composite-skills-agents/09-okwf-integration.md` (17 проблем)

_абзац: 7, Дубль: 1, Оборванный: 4, начала: 5_


### `docs/nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md` (17 проблем)

_абзац: 8, Дубль: 1, Оборванный: 8_


### `docs/technology-combinations/combinations/12-multi-agent-observability-stack.md` (17 проблем)

_абзац: 16, Дубль: 1_


### `docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md` (17 проблем)

_абзац: 16, Дубль: 1_


### `docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md` (17 проблем)

_абзац: 14, Дубль: 1, Оборванный: 2_


### `docs/01-svyazi/12-roadmap.md` (16 проблем)

_Оборванный: 8, абзац: 8_


### `docs/02-anthropic-vacancies/122-глоссарий.md` (16 проблем)

_абзац: 7, Оборванный: 6, начала: 3_


### `docs/02-anthropic-vacancies/155-1-problem-statement.md` (16 проблем)

_абзац: 6, Оборванный: 10_


### `docs/02-anthropic-vacancies/23-11-security-considerations.md` (16 проблем)

_Оборванный: 6, абзац: 9, Дубль: 1_


### `docs/02-anthropic-vacancies/264-11-open-questions.md` (16 проблем)

_Оборванный: 6, Дубль: 1, абзац: 9_


### `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` (16 проблем)

_абзац: 5, Оборванный: 7, начала: 4_


### `docs/02-anthropic-vacancies/48-content-overview.md` (16 проблем)

_абзац: 7, Оборванный: 8, Дубль: 1_


### `docs/02-anthropic-vacancies/57-native-format.md` (16 проблем)

_абзац: 8, начала: 3, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/85-10-query-flow.md` (16 проблем)

_Оборванный: 8, абзац: 8_


### `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` (15 проблем)

_Оборванный: 7, Дубль: 1, абзац: 7_


### `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` (15 проблем)

_абзац: 5, Оборванный: 7, начала: 3_


### `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` (15 проблем)

_Оборванный: 4, абзац: 11_


### `docs/02-anthropic-vacancies/21-9-query-flow.md` (15 проблем)

_абзац: 8, Оборванный: 7_


### `docs/02-anthropic-vacancies/266-13-closing.md` (15 проблем)

_абзац: 8, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/268-references.md` (15 проблем)

_Оборванный: 10, Дубль: 1, абзац: 4_


### `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` (15 проблем)

_абзац: 8, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/302-ссылки.md` (15 проблем)

_Оборванный: 5, начала: 3, абзац: 7_


### `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` (15 проблем)

_абзац: 5, Оборванный: 9, Дубль: 1_


### `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` (15 проблем)

_абзац: 7, Оборванный: 8_


### `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` (15 проблем)

_абзац: 5, Оборванный: 9, Дубль: 1_


### `docs/02-anthropic-vacancies/40-bridges.md` (15 проблем)

_абзац: 5, Оборванный: 7, начала: 3_


### `docs/TECH_RADAR.md` (15 проблем)

_Оборванный: 5, абзац: 9, Дубль: 1_


### `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` (14 проблем)

_Оборванный: 4, абзац: 10_


### `docs/02-anthropic-vacancies/111-4-условия-применимости.md` (14 проблем)

_Оборванный: 6, абзац: 7, Дубль: 1_


### `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` (14 проблем)

_Оборванный: 9, Дубль: 1, абзац: 4_


### `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` (14 проблем)

_Оборванный: 5, абзац: 9_


### `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` (14 проблем)

_Оборванный: 3, абзац: 5, начала: 5, предложение: 1_


### `docs/02-anthropic-vacancies/24-12-versioning-policy.md` (14 проблем)

_Оборванный: 8, абзац: 6_


### `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` (14 проблем)

_абзац: 8, Оборванный: 6_


### `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` (14 проблем)

_абзац: 5, начала: 5, Оборванный: 4_


### `docs/02-anthropic-vacancies/319-acknowledgments.md` (14 проблем)

_абзац: 5, начала: 3, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/76-1-introduction.md` (14 проблем)

_Оборванный: 8, абзац: 6_


### `docs/03-technology-combinations/05-benchmarks.md` (14 проблем)

_Оборванный: 9, предложение: 1, абзац: 4_


### `docs/BROKEN_LINKS.md` (14 проблем)

_абзац: 12, Оборванный: 1, Дубль: 1_


### `docs/autofilled/research-summary.md` (14 проблем)

_абзац: 9, Оборванный: 2, начала: 3_


### `docs/02-anthropic-vacancies/07-2-terminology.md` (13 проблем)

_абзац: 9, Оборванный: 4_


### `docs/02-anthropic-vacancies/145-8-call-to-action.md` (13 проблем)

_абзац: 7, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/146-acknowledgments.md` (13 проблем)

_абзац: 5, начала: 3, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/221-10-open-questions.md` (13 проблем)

_Оборванный: 6, Дубль: 1, абзац: 6_


### `docs/02-anthropic-vacancies/25-13-reference-implementation.md` (13 проблем)

_абзац: 5, начала: 3, Оборванный: 5_


### `docs/02-anthropic-vacancies/267-acknowledgments.md` (13 проблем)

_абзац: 4, начала: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` (13 проблем)

_абзац: 4, Оборванный: 7, Дубль: 2_


### `docs/02-anthropic-vacancies/287-references.md` (13 проблем)

_Оборванный: 8, абзац: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` (13 проблем)

_абзац: 5, Оборванный: 7, Дубль: 1_


### `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` (13 проблем)

_абзац: 6, Оборванный: 5, Дубль: 2_


### `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` (13 проблем)

_абзац: 8, Дубль: 2, Оборванный: 3_


### `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` (13 проблем)

_абзац: 7, Оборванный: 6_


### `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` (13 проблем)

_абзац: 5, Оборванный: 5, Дубль: 2, предложение: 1_


### `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` (13 проблем)

_абзац: 6, Оборванный: 5, Дубль: 2_


### `docs/02-anthropic-vacancies/37-native-format.md` (13 проблем)

_абзац: 5, Оборванный: 8_


### `docs/02-anthropic-vacancies/43-history.md` (13 проблем)

_абзац: 6, Оборванный: 7_


### `docs/02-anthropic-vacancies/56-essence.md` (13 проблем)

_абзац: 6, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` (13 проблем)

_абзац: 7, Оборванный: 6_


### `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` (13 проблем)

_абзац: 7, Оборванный: 6_


### `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` (13 проблем)

_Оборванный: 6, абзац: 7_


### `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` (13 проблем)

_абзац: 5, Оборванный: 6, Дубль: 2_


### `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` (13 проблем)

_абзац: 6, Оборванный: 7_


### `docs/05-habr-projects/02-collaboration-partners.md` (13 проблем)

_Оборванный: 7, Дубль: 1, абзац: 5_


### `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` (13 проблем)

_Оборванный: 4, абзац: 5, начала: 4_


### `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` (12 проблем)

_абзац: 9, Оборванный: 3_


### `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` (12 проблем)

_Оборванный: 6, абзац: 6_


### `docs/02-anthropic-vacancies/123-portal-mcp-py.md` (12 проблем)

_абзац: 6, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` (12 проблем)

_абзац: 5, Оборванный: 4, начала: 3_


### `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` (12 проблем)

_абзац: 6, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` (12 проблем)

_Оборванный: 6, абзац: 6_


### `docs/02-anthropic-vacancies/245-ссылки.md` (12 проблем)

_Оборванный: 4, абзац: 8_


### `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` (12 проблем)

_абзац: 4, Оборванный: 6, Дубль: 2_


### `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` (12 проблем)

_абзац: 6, Оборванный: 6_


### `docs/02-anthropic-vacancies/275-why-this-document-exists.md` (12 проблем)

_абзац: 6, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/285-closing.md` (12 проблем)

_абзац: 4, начала: 3, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/42-author-contact.md` (12 проблем)

_абзац: 7, Оборванный: 5_


### `docs/02-anthropic-vacancies/52-author-contact.md` (12 проблем)

_абзац: 6, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/65-readme-md.md` (12 проблем)

_абзац: 7, Оборванный: 5_


### `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` (12 проблем)

_абзац: 8, Оборванный: 4_


### `docs/02-anthropic-vacancies/77-2-terminology.md` (12 проблем)

_абзац: 8, Оборванный: 4_


### `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` (12 проблем)

_абзац: 7, Оборванный: 5_


### `docs/03-technology-combinations/03-local-first.md` (12 проблем)

_абзац: 4, Оборванный: 8_


### `docs/05-habr-projects/memory/yodoca.md` (12 проблем)

_Оборванный: 3, абзац: 6, начала: 3_


### `docs/COMPONENT_MATRIX.md` (12 проблем)

_абзац: 7, Оборванный: 5_


### `docs/SIMILAR.md` (12 проблем)

_абзац: 5, Оборванный: 7_


### `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` (11 проблем)

_абзац: 5, Оборванный: 6_


### `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` (11 проблем)

_Оборванный: 3, абзац: 9_


### `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` (11 проблем)

_Оборванный: 2, абзац: 9_


### `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` (11 проблем)

_абзац: 5, Дубль: 2, Оборванный: 4_


### `docs/02-anthropic-vacancies/128-доступные-инструменты.md` (11 проблем)

_абзац: 5, Оборванный: 4, Дубль: 2_


### `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` (11 проблем)

_абзац: 6, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/136-abstract.md` (11 проблем)

_абзац: 6, Оборванный: 5_


### `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` (11 проблем)

_абзац: 5, Оборванный: 4, Дубль: 2_


### `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` (11 проблем)

_абзац: 4, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` (11 проблем)

_абзац: 4, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/225-references.md` (11 проблем)

_Оборванный: 3, абзац: 8_


### `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` (11 проблем)

_абзац: 4, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` (11 проблем)

_абзац: 4, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` (11 проблем)

_абзац: 6, Оборванный: 5_


### `docs/02-anthropic-vacancies/281-the-recursive-insight.md` (11 проблем)

_абзац: 6, Оборванный: 5_


### `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` (11 проблем)

_абзац: 5, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/349-твоя-личность.md` (11 проблем)

_абзац: 10, Оборванный: 1_


### `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` (11 проблем)

_Оборванный: 4, абзац: 4, начала: 3_


### `docs/02-anthropic-vacancies/50-bridges.md` (11 проблем)

_абзац: 6, Оборванный: 5_


### `docs/02-anthropic-vacancies/51-compatibility-level.md` (11 проблем)

_абзац: 5, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` (11 проблем)

_абзац: 6, Оборванный: 5_


### `docs/02-anthropic-vacancies/62-author-contact.md` (11 проблем)

_абзац: 5, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` (11 проблем)

_абзац: 8, Оборванный: 3_


### `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` (11 проблем)

_абзац: 5, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` (11 проблем)

_Оборванный: 7, Дубль: 1, абзац: 3_


### `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` (11 проблем)

_абзац: 6, Оборванный: 5_


### `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` (11 проблем)

_абзац: 5, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` (11 проблем)

_абзац: 6, Оборванный: 5_


### `docs/05-habr-projects/memory/ngt-memory.md` (11 проблем)

_Оборванный: 4, абзац: 7_


### `docs/DIGEST.md` (11 проблем)

_абзац: 6, Оборванный: 4, Дубль: 1_


### `docs/contacts/anastasiyaw.md` (11 проблем)

_абзац: 5, Оборванный: 6_


### `docs/contacts/antipozitive.md` (11 проблем)

_Оборванный: 5, абзац: 6_


### `docs/02-anthropic-vacancies/03-portal-protocol-md.md` (10 проблем)

_абзац: 4, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/105-review-methodology-md.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/106-tl-dr.md` (10 проблем)

_абзац: 6, Оборванный: 4_


### `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` (10 проблем)

_Оборванный: 5, абзац: 5_


### `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` (10 проблем)

_Оборванный: 4, абзац: 6_


### `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/147-references.md` (10 проблем)

_Оборванный: 3, абзац: 4, начала: 3_


### `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` (10 проблем)

_Оборванный: 4, абзац: 3, начала: 3_


### `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` (10 проблем)

_абзац: 4, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/153-executive-summary.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` (10 проблем)

_абзац: 4, Оборванный: 6_


### `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` (10 проблем)

_Оборванный: 4, абзац: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/181-12-closing.md` (10 проблем)

_абзац: 6, Оборванный: 4_


### `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` (10 проблем)

_абзац: 6, Оборванный: 4_


### `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/210-abstract.md` (10 проблем)

_абзац: 4, предложение: 2, Оборванный: 4_


### `docs/02-anthropic-vacancies/224-acknowledgments.md` (10 проблем)

_абзац: 6, Оборванный: 3, Дубль: 1_


### `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` (10 проблем)

_абзац: 4, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` (10 проблем)

_абзац: 5, начала: 5_


### `docs/02-anthropic-vacancies/337-благодарности.md` (10 проблем)

_абзац: 4, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/38-content-overview.md` (10 проблем)

_абзац: 7, Оборванный: 3_


### `docs/02-anthropic-vacancies/41-compatibility-level.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` (10 проблем)

_абзац: 6, Оборванный: 4_


### `docs/02-anthropic-vacancies/53-history.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/60-bridges.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/61-compatibility-level.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/63-history.md` (10 проблем)

_абзац: 6, Оборванный: 4_


### `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` (10 проблем)

_абзац: 4, Оборванный: 5, Дубль: 1_


### `docs/02-anthropic-vacancies/74-abstract.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/93-18-reference-implementation.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/AUTOFILLED.md` (10 проблем)

_абзац: 7, Оборванный: 3_


### `docs/BACKLINKS.md` (10 проблем)

_абзац: 5, Оборванный: 4, Дубль: 1_


### `docs/KEYWORD_INDEX.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/contacts/cutcode.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/contacts/dmitriila.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/contacts/mixaill76.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/contacts/nlaik.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/contacts/sonia-black.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/contacts/tagir-analyzes.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/contacts/vitalyoborin.md` (10 проблем)

_Оборванный: 6, абзац: 3, Дубль: 1_


### `docs/contacts/vladspace.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/contacts/zodigancode.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/06-1-introduction.md` (9 проблем)

_Оборванный: 4, абзац: 5_


### `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/137-table-of-contents.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/169-table-of-contents.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/182-acknowledgments.md` (9 проблем)

_абзац: 5, Оборванный: 4_


### `docs/02-anthropic-vacancies/183-references.md` (9 проблем)

_Оборванный: 5, абзац: 4_


### `docs/02-anthropic-vacancies/190-содержание.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/211-table-of-contents.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/223-12-closing.md` (9 проблем)

_абзац: 5, Оборванный: 4_


### `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/230-аннотация.md` (9 проблем)

_абзац: 5, предложение: 1, Оборванный: 3_


### `docs/02-anthropic-vacancies/231-содержание.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` (9 проблем)

_абзац: 4, Дубль: 2, Оборванный: 3_


### `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/253-table-of-contents.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` (9 проблем)

_абзац: 7, Оборванный: 2_


### `docs/02-anthropic-vacancies/300-заключение.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/301-благодарности.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/308-table-of-contents.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` (9 проблем)

_Оборванный: 3, абзац: 5, предложение: 1_


### `docs/02-anthropic-vacancies/325-аннотация.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/347-твоя-миссия.md` (9 проблем)

_абзац: 6, Дубль: 1, Оборванный: 2_


### `docs/02-anthropic-vacancies/35-passports-info1-md.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/36-essence.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/39-angle-perspective.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/45-passports-pro2-md.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/46-essence.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/55-passports-meta-md.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/59-angle-perspective.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` (9 проблем)

_абзац: 5, Оборванный: 4_


### `docs/03-technology-combinations/01-agent-routing.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/contacts/andrey-chuyan.md` (9 проблем)

_Оборванный: 6, абзац: 3_


### `docs/contacts/spbmolot.md` (9 проблем)

_Оборванный: 5, абзац: 3, Дубль: 1_


### `docs/02-anthropic-vacancies/04-abstract.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` (8 проблем)

_абзац: 5, Оборванный: 2, Дубль: 1_


### `docs/02-anthropic-vacancies/12-content-overview.md` (8 проблем)

_Оборванный: 5, абзац: 4_


### `docs/02-anthropic-vacancies/120-главные-технические-риски.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/126-установка.md` (8 проблем)

_Оборванный: 3, абзац: 5_


### `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/154-table-of-contents.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/168-abstract.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/204-ссылки.md` (8 проблем)

_Оборванный: 4, абзац: 4_


### `docs/02-anthropic-vacancies/244-благодарности.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/252-abstract.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` (8 проблем)

_Оборванный: 5, абзац: 3_


### `docs/02-anthropic-vacancies/286-acknowledgments.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` (8 проблем)

_абзац: 7, Оборванный: 1_


### `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` (8 проблем)

_абзац: 6, Оборванный: 2_


### `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/307-abstract.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/31-content-overview.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/326-содержание.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` (8 проблем)

_абзац: 5, начала: 3_


### `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` (8 проблем)

_Оборванный: 5, абзац: 3_


### `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/47-native-format.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/49-angle-perspective.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/58-content-overview.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` (8 проблем)

_Оборванный: 4, абзац: 4_


### `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` (8 проблем)

_Оборванный: 5, абзац: 3_


### `docs/05-habr-projects/01-synthesis.md` (8 проблем)

_абзац: 4, Оборванный: 3, Дубль: 1_


### `docs/05-habr-projects/knowledge/wikontic.md` (8 проблем)

_Оборванный: 5, абзац: 2, Дубль: 1_


### `docs/autofilled/components/cowork.md` (8 проблем)

_абзац: 4, Оборванный: 3, Дубль: 1_


### `docs/autofilled/components/ingit.md` (8 проблем)

_абзац: 4, Оборванный: 3, Дубль: 1_


### `docs/autofilled/components/lorenzo.md` (8 проблем)

_абзац: 4, Оборванный: 3, Дубль: 1_


### `docs/autofilled/components/nautilus.md` (8 проблем)

_абзац: 4, Оборванный: 3, Дубль: 1_


### `docs/autofilled/components/sgb.md` (8 проблем)

_абзац: 4, Оборванный: 3, Дубль: 1_


### `docs/autofilled/components/svend4.md` (8 проблем)

_абзац: 5, Оборванный: 2, Дубль: 1_


### `docs/autofilled/components/svyazi.md` (8 проблем)

_абзац: 4, Оборванный: 3, Дубль: 1_


### `docs/contacts/kksudo.md` (8 проблем)

_Оборванный: 5, абзац: 3_


### `docs/02-anthropic-vacancies/102-доступ-к-данным.md` (7 проблем)

_абзац: 6, Оборванный: 2_


### `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/13-angle-perspective.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/16-history.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` (7 проблем)

_абзац: 6, Оборванный: 1_


### `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` (7 проблем)

_Оборванный: 1, абзац: 6_


### `docs/02-anthropic-vacancies/243-12-заключение.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` (7 проблем)

_абзац: 4, начала: 3_


### `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/345-кто-ты.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` (7 проблем)

_абзац: 3, Оборванный: 4_


### `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` (7 проблем)

_абзац: 4, Оборванный: 2, предложение: 1_


### `docs/05-habr-projects/QA.md` (7 проблем)

_Оборванный: 3, Дубль: 1, абзац: 3_


### `docs/CHANGELOG.md` (7 проблем)

_Оборванный: 6, предложение: 1_


### `docs/DEPENDENCY_MAP.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/autofilled/components/.md` (7 проблем)

_абзац: 4, Оборванный: 2, Дубль: 1_


### `docs/autofilled/components/kksudo.md` (7 проблем)

_абзац: 3, Оборванный: 3, Дубль: 1_


### `docs/autofilled/components/spbmolot.md` (7 проблем)

_абзац: 3, Оборванный: 3, Дубль: 1_


### `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` (6 проблем)

_Оборванный: 2, абзац: 4_


### `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` (6 проблем)

_Оборванный: 4, абзац: 2_


### `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/03-technology-combinations/04-sozialrecht-domain.md` (6 проблем)

_Оборванный: 2, абзац: 4_


### `docs/VALIDATION.md` (6 проблем)

_Оборванный: 2, абзац: 4_


### `docs/02-anthropic-vacancies/183-references.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` (6 проблем)

_Оборванный: 3, Дубль: 1, абзац: 2_


### `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` (6 проблем)

_Оборванный: 3, предложение: 1, абзац: 2_


### `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/02-anthropic-vacancies/230-аннотация.md` (6 проблем)

_Оборванный: 2, абзац: 3, предложение: 1_


### `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/02-anthropic-vacancies/252-abstract.md` (6 проблем)

_Оборванный: 2, предложение: 1, абзац: 3_


### `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` (6 проблем)

_Оборванный: 1, абзац: 5_


### `docs/02-anthropic-vacancies/337-благодарности.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` (6 проблем)

_абзац: 3, начала: 3_


### `docs/02-anthropic-vacancies/41-compatibility-level.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/02-anthropic-vacancies/51-compatibility-level.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/53-history.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/60-bridges.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/61-compatibility-level.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/62-author-contact.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/74-abstract.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/93-18-reference-implementation.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/HEATMAP.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/KNOWLEDGE_MAP.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/VALIDATION.md` (6 проблем)

_абзац: 2, Оборванный: 4_


### `docs/ai-collaborations/candidates/02-related-projects-context.md` (6 проблем)

_абзац: 4, Оборванный: 1, Дубль: 1_


### `docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/ai-collaborations/continuation/05-roadmap-6-12-months.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md` (6 проблем)

_Оборванный: 1, Дубль: 1, абзац: 4_


### `docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md` (6 проблем)

_Оборванный: 1, Дубль: 1, абзац: 4_


### `docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md` (6 проблем)

_Оборванный: 1, Дубль: 1, абзац: 4_


### `docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md` (6 проблем)

_Оборванный: 1, Дубль: 1, абзац: 4_


### `docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md` (6 проблем)

_Дубль: 1, Оборванный: 2, предложение: 1, абзац: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md` (6 проблем)

_Дубль: 1, абзац: 5_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md` (6 проблем)

_абзац: 5, Дубль: 1_


### `docs/autofilled/research-summary.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/habr-unique-projects/final-ensembles/1-one-person-one-company.md` (6 проблем)

_Оборванный: 1, Дубль: 1, абзац: 4_


### `docs/lorenzo-agent/07-chto-mozhesh.md` (6 проблем)

_Оборванный: 2, Дубль: 1, абзац: 2, предложение: 1_


### `docs/lorenzo-agent/13-outreach-communication.md` (6 проблем)

_Дубль: 1, абзац: 2, начала: 3_


### `docs/lorenzo-agent/naming/00-question-lorenzo-codename.md` (6 проблем)

_Дубль: 1, Оборванный: 2, абзац: 3_


### `docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md` (6 проблем)

_Дубль: 1, абзац: 2, Оборванный: 2, предложение: 1_


### `docs/nautilus/double-triangle-architecture/08-call-to-action.md` (6 проблем)

_абзац: 4, Дубль: 1, Оборванный: 1_


### `docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md` (6 проблем)

_Дубль: 1, абзац: 5_


### `docs/nautilus/npp-v1-0/02-terminology.md` (6 проблем)

_Дубль: 1, абзац: 5_


### `docs/nautilus/npp-v1-0/05-compatibility-levels.md` (6 проблем)

_Дубль: 1, абзац: 5_


### `docs/nautilus/npp-v1-0/12-versioning-policy.md` (6 проблем)

_Дубль: 1, Оборванный: 2, абзац: 3_


### `docs/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md` (6 проблем)

_Дубль: 1, абзац: 2, Оборванный: 3_


### `docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md` (6 проблем)

_Дубль: 1, абзац: 3, Оборванный: 2_


### `docs/nautilus/professional-colleague-agents-en/00-abstract.md` (6 проблем)

_Дубль: 1, Оборванный: 3, предложение: 2_


### `docs/nautilus/review-methodology/00-tldr.md` (6 проблем)

_Дубль: 1, абзац: 3, Оборванный: 2_


### `docs/nautilus/review-methodology/02-formal-workflow.md` (6 проблем)

_Дубль: 1, абзац: 4, Оборванный: 1_


### `docs/nautilus/transmission-box/00-question-mountain-to-person.md` (6 проблем)

_абзац: 2, Дубль: 1, Оборванный: 2, предложение: 1_


### `docs/svyazi-2-0/architecture/card-envelope.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/svyazi-2-0/architecture/integration-spec.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/svyazi-2-0/architecture/review-record.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/svyazi-2-0/components/ai-factory.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/svyazi-2-0/components/research-docs-liteparse.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/svyazi-2-0/components/yjs-automerge.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/svyazi-2-0/ensembles/A-collaboration-os.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/svyazi-2-0/ensembles/B-forensic-rag.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/svyazi-2-0/ensembles/C-multi-agent-factory.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/svyazi-2-0/ensembles/E-execution-plane.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/svyazi-2-0/ensembles/G-federated-local-graph.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/svyazi-2-0/ensembles/H-research-to-product-flywheel.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/svyazi-2-0/limitations/conclusions.md` (6 проблем)

_Оборванный: 4, абзац: 2_


### `docs/svyazi-2-0/limitations/do-not-glue.md` (6 проблем)

_Оборванный: 4, абзац: 2_


### `docs/svyazi-2-0/overview/continuation-intro.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/svyazi-2-0/security/privacy.md` (6 проблем)

_абзац: 3, Оборванный: 2, Дубль: 1_


### `docs/technology-combinations/research-reports/continuation-10-domains.md` (6 проблем)

_Дубль: 1, абзац: 5_


### `docs/WORD_CLOUD.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/templates/project-component.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` (5 проблем)

_абзац: 3, Оборванный: 2_


### `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` (5 проблем)

_Оборванный: 2, Дубль: 1, абзац: 2_


### `docs/02-anthropic-vacancies/202-12-заключение.md` (5 проблем)

_Оборванный: 1, абзац: 4_


### `docs/02-anthropic-vacancies/203-благодарности.md` (5 проблем)

_Оборванный: 1, абзац: 4_


### `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` (5 проблем)

_абзац: 3, Оборванный: 2_


### `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` (5 проблем)

_абзац: 3, Оборванный: 2_


### `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` (5 проблем)

_абзац: 3, Оборванный: 2_


### `docs/CONCEPT_GRAPH.md` (5 проблем)

_абзац: 3, Оборванный: 2_


### `docs/COMPONENT_MATRIX.md` (5 проблем)

_Оборванный: 1, абзац: 4_


### `docs/DIGEST_AUTO.md` (5 проблем)

_абзац: 2, Оборванный: 2, предложение: 1_


### `docs/HEALTH.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/MISSING.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/NETWORK.md` (5 проблем)

_абзац: 2, Оборванный: 3_


### `docs/READING_ORDER.md` (5 проблем)

_абзац: 3, Оборванный: 2_


### `docs/READING_TIME.md` (5 проблем)

_абзац: 2, Оборванный: 3_


### `docs/WORD_CLOUD.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/WORD_FREQ.md` (5 проблем)

_абзац: 3, Оборванный: 1, предложение: 1_


### `docs/02-anthropic-vacancies/189-аннотация.md` (4 проблем)

_Оборванный: 3, абзац: 2_


### `docs/DIGEST_WEEKLY.md` (4 проблем)

_абзац: 3, Оборванный: 1_


### `docs/KPI_HISTORY.md` (4 проблем)

_абзац: 4_


### `docs/PASSIVE_VOICE.md` (4 проблем)

_абзац: 3, Оборванный: 1_


### `docs/PROGRESS.md` (4 проблем)

_Оборванный: 1, абзац: 3_


### `docs/VERSION_DIFF.md` (4 проблем)

_абзац: 2, Оборванный: 2_


### `docs/templates/mega-stack.md` (4 проблем)

_Оборванный: 2, абзац: 2_


### `docs/01-svyazi/README.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/02-anthropic-vacancies/346-твоё-происхождение.md` (3 проблем)

_Оборванный: 2, абзац: 1_


### `docs/02-anthropic-vacancies/13-angle-perspective.md` (3 проблем)

_абзац: 3_


### `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/02-anthropic-vacancies/16-history.md` (3 проблем)

_абзац: 3_


### `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/02-anthropic-vacancies/203-благодарности.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/02-anthropic-vacancies/31-content-overview.md` (3 проблем)

_абзац: 3_


### `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` (3 проблем)

_абзац: 3_


### `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/02-anthropic-vacancies/345-кто-ты.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/02-anthropic-vacancies/346-твоё-происхождение.md` (3 проблем)

_Оборванный: 2, абзац: 1_


### `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` (3 проблем)

_абзац: 3_


### `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` (3 проблем)

_абзац: 1, Оборванный: 1, предложение: 1_


### `docs/05-habr-projects/01-synthesis.md` (3 проблем)

_абзац: 3_


### `docs/05-habr-projects/README.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/05-habr-projects/knowledge/wikontic.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/ABBREVIATIONS.md` (3 проблем)

_абзац: 3_


### `docs/COMPARE.md` (3 проблем)

_абзац: 1, Оборванный: 2_


### `docs/COST.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/CROSSREFS.md` (3 проблем)

_абзац: 3_


### `docs/DIGEST_WEEKLY.md` (3 проблем)

_абзац: 3_


### `docs/KPI.md` (3 проблем)

_абзац: 3_


### `docs/LANGUAGE_STATS.md` (3 проблем)

_абзац: 3_


### `docs/METRICS.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/ORPHANS.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/PRIORITIES.md` (3 проблем)

_абзац: 3_


### `docs/README.md` (3 проблем)

_Оборванный: 2, предложение: 1_


### `docs/SCHEDULE.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/SEE_ALSO.md` (3 проблем)

_абзац: 1, Оборванный: 1, предложение: 1_


### `docs/VERSION_DIFF.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/ai-collaborations/source-projects.md` (3 проблем)

_Оборванный: 2, абзац: 1_


### `docs/anthropic-vacancies/README.md` (3 проблем)

_абзац: 1, Оборванный: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md` (3 проблем)

_Оборванный: 1, Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/methodology.md` (3 проблем)

_абзац: 2, Дубль: 1_


### `docs/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/anthropic-vacancies/overview.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md` (3 проблем)

_абзац: 2, Дубль: 1_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/autofilled/components/.md` (3 проблем)

_абзац: 3_


### `docs/autofilled/components/cowork.md` (3 проблем)

_абзац: 3_


### `docs/autofilled/components/ingit.md` (3 проблем)

_абзац: 3_


### `docs/autofilled/components/kksudo.md` (3 проблем)

_абзац: 3_


### `docs/autofilled/components/lorenzo.md` (3 проблем)

_абзац: 3_


### `docs/autofilled/components/nautilus.md` (3 проблем)

_абзац: 3_


### `docs/autofilled/components/sgb.md` (3 проблем)

_абзац: 3_


### `docs/autofilled/components/spbmolot.md` (3 проблем)

_абзац: 3_


### `docs/autofilled/components/svend4.md` (3 проблем)

_абзац: 3_


### `docs/autofilled/components/svyazi.md` (3 проблем)

_абзац: 3_


### `docs/glossary/concepts.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/habr-unique-projects/final-ensembles/4-summary-authors.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md` (3 проблем)

_Оборванный: 1, предложение: 1, абзац: 1_


### `docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/lorenzo-agent/04-komu-ty-sluzhish.md` (3 проблем)

_Дубль: 1, Оборванный: 1, абзац: 1_


### `docs/lorenzo-agent/09-voobshche-nelzya.md` (3 проблем)

_Дубль: 1, Оборванный: 1, абзац: 1_


### `docs/lorenzo-agent/16-vsegda-delaesh.md` (3 проблем)

_Дубль: 1, Оборванный: 1, абзац: 1_


### `docs/lorenzo-agent/18-escalate-to-max.md` (3 проблем)

_Дубль: 1, Оборванный: 1, абзац: 1_


### `docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/nautilus/double-triangle-architecture/09-acknowledgments.md` (3 проблем)

_абзац: 2, Дубль: 1_


### `docs/nautilus/double-triangle-architecture/10-references.md` (3 проблем)

_Дубль: 1, Оборванный: 1, абзац: 1_


### `docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/nautilus/npp-v1-0/00-abstract-status.md` (3 проблем)

_Дубль: 1, Оборванный: 1, абзац: 1_


### `docs/nautilus/npp-v1-0/01-introduction.md` (3 проблем)

_Дубль: 1, абзац: 1, Оборванный: 1_


### `docs/nautilus/professional-colleague-agents-en/10-open-questions.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/nautilus/professional-colleague-agents-en/11-call-for-collaboration.md` (3 проблем)

_Дубль: 1, абзац: 1, Оборванный: 1_


### `docs/nautilus/professional-colleague-agents-ru/00-abstract.md` (3 проблем)

_Дубль: 1, абзац: 1, Оборванный: 1_


### `docs/nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md` (3 проблем)

_Дубль: 1, абзац: 2_


### `docs/nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md` (3 проблем)

_Дубль: 1, абзац: 1, Оборванный: 1_


### `docs/nautilus/representative-agent-layer-ru/00-abstract.md` (3 проблем)

_Дубль: 1, Оборванный: 1, абзац: 1_


### `docs/svyazi-2-0/components/agent-memory-mcp.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/svyazi-2-0/components/svyazi.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/templates/decision-record.md` (3 проблем)

_абзац: 3_


### `docs/templates/ensemble.md` (3 проблем)

_абзац: 3_


### `docs/01-svyazi/README.md` (2 проблем)

_Оборванный: 1, абзац: 1_


### `docs/02-anthropic-vacancies/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/05-habr-projects/README.md` (2 проблем)

_абзац: 2_


### `docs/ALERTS.md` (2 проблем)

_абзац: 2_


### `docs/CONTACT_PRIORITY.md` (2 проблем)

_Оборванный: 1, абзац: 1_


### `docs/COVERAGE.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/KPI.md` (2 проблем)

_абзац: 2_


### `docs/LINKS.md` (2 проблем)

_абзац: 2_


### `docs/GRAPH.md` (2 проблем)

_абзац: 2_


### `docs/LINKS.md` (2 проблем)

_абзац: 2_


### `docs/REGISTRY.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/SCORING.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/SOURCE_MAP.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/STALENESS.md` (2 проблем)

_абзац: 2_


### `docs/STATS.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/ai-collaborations/strategy/README.md` (2 проблем)

_абзац: 2_


### `docs/anthropic-vacancies/clusters/01-ai-research-engineering.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/02-sales.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/03-finance.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/04-security.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/05-marketing-brand.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/06-engineering-design-product.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/08-safeguards-trust-safety.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/09-product-management-support-ops.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/10-compute.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/11-legal.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/12-technical-program-management.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/13-communications.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/14-public-policy.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/15-public-benefit.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/clusters/16-people.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/mmorpg-for-programmers/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/badges/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/glossary/authors-by-name.md` (2 проблем)

_Оборванный: 1, абзац: 1_


### `docs/habr-unique-projects/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/habr-unique-projects/hardware-pairs/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/habr-unique-projects/key-findings/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/habr-unique-projects/software-pairs/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/lorenzo-agent/00-intro.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/lorenzo-agent/01-kto-ty.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/lorenzo-agent/02-tvoyo-proishozhdenie.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/lorenzo-agent/08-bez-max-approval.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/lorenzo-agent/17-honestly-ne-znaesh.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/lorenzo-agent/README.md` (2 проблем)

_Оборванный: 2_


### `docs/lorenzo-agent/naming/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/nautilus/composite-skills-agents-companion-mentors/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/nautilus/npp-humanitarian-extension/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/nautilus/npp-v1-1/14-sdk.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/nautilus/privacy-federation/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/nautilus/representative-agent-layer-en/11-call-for-collaboration.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/svyazi-2-0/overview/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/svyazi-2-0/prototype/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/svyazi-2-0/security/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/technology-combinations/research-reports/sozialrecht-35-combinations.md` (2 проблем)

_Дубль: 1, абзац: 1_


### `docs/technology-combinations/synthesis-tables/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/templates/contact-outreach.md` (2 проблем)

_Оборванный: 1, абзац: 1_


### `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` (1 проблем)

_абзац: 1_


### `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` (1 проблем)

_абзац: 1_


### `docs/02-anthropic-vacancies/README.md` (1 проблем)

_Оборванный: 1_


### `docs/03-technology-combinations/README.md` (1 проблем)

_Оборванный: 1_


### `docs/04-ai-collaborations/README.md` (1 проблем)

_Оборванный: 1_


### `docs/05-habr-projects/memory/README.md` (1 проблем)

_абзац: 1_


### `docs/BADGES.md` (1 проблем)

_Оборванный: 1_


### `docs/COVERAGE.md` (1 проблем)

_абзац: 1_


### `docs/DEPENDABOT.md` (1 проблем)

_абзац: 1_


### `docs/ENTITIES.md` (1 проблем)

_абзац: 1_


### `docs/MCP_DASHBOARD.md` (1 проблем)

_абзац: 1_


### `docs/MINDMAP.md` (1 проблем)

_абзац: 1_


### `docs/SEARCH_RESULTS.md` (1 проблем)

_абзац: 1_


### `docs/autofilled/components/README.md` (1 проблем)

_Оборванный: 1_


### `docs/contacts/README.md` (1 проблем)

_Оборванный: 1_


### `docs/glossary/README.md` (1 проблем)

_абзац: 1_


### `docs/habr-unique-projects/analogues/README.md` (1 проблем)

_абзац: 1_


### `docs/habr-unique-projects/deep-pairs/README.md` (1 проблем)

_Оборванный: 1_


### `docs/habr-unique-projects/extra-examples/README.md` (1 проблем)

_Оборванный: 1_


### `docs/habr-unique-projects/final-ensembles/README.md` (1 проблем)

_абзац: 1_


### `docs/lorenzo-agent/operationalized/README.md` (1 проблем)

_Оборванный: 1_


### `docs/lorenzo-agent/phased-deployment/README.md` (1 проблем)

_Оборванный: 1_


### `docs/lorenzo-agent/scenarios/README.md` (1 проблем)

_абзац: 1_


### `docs/lorenzo-agent/specification/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/README.md` (1 проблем)

_абзац: 1_


### `docs/nautilus/community-discussions/agent-changes-reality/README.md` (1 проблем)

_абзац: 1_


### `docs/nautilus/community-discussions/habr-article-1-reaction/README.md` (1 проблем)

_абзац: 1_


### `docs/nautilus/community-discussions/habr-article-2-reaction/README.md` (1 проблем)

_абзац: 1_


### `docs/nautilus/community-discussions/practical-observations/README.md` (1 проблем)

_абзац: 1_


### `docs/nautilus/community-discussions/voiceless-contributors/README.md` (1 проблем)

_абзац: 1_


### `docs/nautilus/composite-skills-agents/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/double-triangle-architecture/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/infrastructure-layer-b-en/12-closing.md` (1 проблем)

_Дубль: 1_


### `docs/nautilus/infrastructure-layer-b-en/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/infrastructure-layer-b-ru/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/ingit-cowork-en/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/ingit-cowork-ru/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/innovation-transitions/README.md` (1 проблем)

_абзац: 1_


### `docs/nautilus/multi-tier-architecture/README.md` (1 проблем)

_абзац: 1_


### `docs/nautilus/npp-v1-0/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/npp-v1-1/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/okwf-concept/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/professional-colleague-agents-en/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/professional-colleague-agents-ru/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/representative-agent-layer-en/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/representative-agent-layer-ru/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/review-methodology/README.md` (1 проблем)

_Оборванный: 1_


### `docs/nautilus/supply-demand/README.md` (1 проблем)

_абзац: 1_


### `docs/nautilus/transmission-box/README.md` (1 проблем)

_абзац: 1_


### `docs/svyazi-2-0/README.md` (1 проблем)

_абзац: 1_


### `docs/svyazi-2-0/architecture/README.md` (1 проблем)

_Оборванный: 1_


### `docs/svyazi-2-0/components/README.md` (1 проблем)

_Оборванный: 1_


### `docs/svyazi-2-0/ensembles/README.md` (1 проблем)

_Оборванный: 1_


### `docs/svyazi-2-0/limitations/README.md` (1 проблем)

_абзац: 1_


### `docs/svyazi-2-0/outreach/README.md` (1 проблем)

_абзац: 1_


### `docs/technology-combinations/README.md` (1 проблем)

_абзац: 1_


### `docs/technology-combinations/combinations/README.md` (1 проблем)

_Оборванный: 1_


### `docs/technology-combinations/mega-stacks/README.md` (1 проблем)

_абзац: 1_


### `docs/technology-combinations/properties/README.md` (1 проблем)

_абзац: 1_


### `docs/technology-combinations/research-reports/README.md` (1 проблем)

_абзац: 1_


### `docs/templates/README.md` (1 проблем)

_абзац: 1_



<!-- backlinks -->

---

**Кто ссылается на этот документ (3):**
- [321-appendix-a-decision-tree-for-ingit-adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)
- [README](docs/README.md)
- [TABLES](docs/TABLES.md)

