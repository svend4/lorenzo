---
title: "Качество абзацев"
tags:
  - general
date: 2026-04-29
---

# Качество абзацев

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> _абзац: 700, Оборванный: 534, начала: 205, Дубль: 4_
**Проекты:** Svyazi, Yodoca, MemNet, Wikontic

---

<!-- toc -->
## Содержание

- [Типы проблем](#типы-проблем)
- [По файлам](#по-файлам)
  - [`docs/CONCEPTS.md` (1443 проблем)](#docsconceptsmd-1443-проблем)
  - [`docs/TABLES.md` (553 проблем)](#docstablesmd-553-проблем)
  - [`docs/CODE_BLOCKS.md` (170 проблем)](#docscode_blocksmd-170-проблем)
  - [`docs/QUESTIONS.md` (138 проблем)](#docsquestionsmd-138-проблем)
  - [`docs/QA.md` (127 проблем)](#docsqamd-127-проблем)
  - [`docs/CONTRADICTIONS.md` (126 проблем)](#docscontradictionsmd-126-проблем)
  - [`docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` (92 проблем)](#docs02-anthropic-vacancies342-что-такое-вариант-c-concept-document-для-anthropicmd-92-проблем)
  - [`docs/CLUSTERS.md` (76 проблем)](#docsclustersmd-76-проблем)
  - [`docs/DECISIONS.md` (71 проблем)](#docsdecisionsmd-71-проблем)
  - [`docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` (67 проблем)](#docs02-anthropic-vacancies341-приложение-c-образец-спецификаций-инструментов-ingmd-67-проблем)
  - [`docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` (65 проблем)](#docs02-anthropic-vacancies343-lorenzo-catalyst-agent-глубокая-проработка-специфиmd-65-проблем)
  - [`docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` (55 проблем)](#docs02-anthropic-vacancies01-интегральный-анализ-профиля-svend4md-55-проблем)
  - [`docs/GITHUB_ISSUES.md` (55 проблем)](#docsgithub_issuesmd-55-проблем)
  - [`docs/02-anthropic-vacancies/QA.md` (47 проблем)](#docs02-anthropic-vacanciesqamd-47-проблем)
  - [`docs/04-ai-collaborations/00-intro.md` (46 проблем)](#docs04-ai-collaborations00-intromd-46-проблем)
  - [`docs/CONTENT_GAPS.md` (46 проблем)](#docscontent_gapsmd-46-проблем)
  - [`docs/02-anthropic-vacancies/218-7-application-domains.md` (44 проблем)](#docs02-anthropic-vacancies218-7-application-domainsmd-44-проблем)
  - [`docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` (44 проблем)](#docs02-anthropic-vacancies219-8-pilot-proposal-sgb-advocate-colleaguemd-44-проблем)
  - [`docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` (43 проблем)](#docs02-anthropic-vacancies217-6-risks-specific-to-this-categorymd-43-проблем)
  - [`docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` (42 проблем)](#docs02-anthropic-vacancies237-6-риски-специфичные-для-этой-категорииmd-42-проблем)
  - [`docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` (40 проблем)](#docs02-anthropic-vacancies212-1-the-five-type-typology-of-principal-side-agentsmd-40-проблем)
  - [`docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` (40 проблем)](#docs02-anthropic-vacancies239-8-пилотное-предложение-sgb-колega-адвокатmd-40-проблем)
  - [`docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` (38 проблем)](#docs02-anthropic-vacancies157-3-why-existing-solutions-failmd-38-проблем)
  - [`docs/02-anthropic-vacancies/165-closing.md` (38 проблем)](#docs02-anthropic-vacancies165-closingmd-38-проблем)
  - [`docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` (37 проблем)](#docs02-anthropic-vacancies173-4-ten-domains-of-applicationmd-37-проблем)
  - [`docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` (37 проблем)](#docs02-anthropic-vacancies232-1-типология-из-пяти-типов-агентов-на-стороне-принцmd-37-проблем)
  - [`docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` (36 проблем)](#docs02-anthropic-vacancies158-4-proposed-infrastructuremd-36-проблем)
  - [`docs/02-anthropic-vacancies/238-7-области-применения.md` (36 проблем)](#docs02-anthropic-vacancies238-7-области-примененияmd-36-проблем)
  - [`docs/05-habr-projects/memory/memnet.md` (36 проблем)](#docs05-habr-projectsmemorymemnetmd-36-проблем)
  - [`docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` (35 проблем)](#docs02-anthropic-vacancies194-4-десять-областей-примененияmd-35-проблем)
  - [`docs/02-anthropic-vacancies/69-section.md` (34 проблем)](#docs02-anthropic-vacancies69-sectionmd-34-проблем)
  - [`docs/01-svyazi/04-ensembles-overview.md` (33 проблем)](#docs01-svyazi04-ensembles-overviewmd-33-проблем)
  - [`docs/01-svyazi/QA.md` (32 проблем)](#docs01-svyaziqamd-32-проблем)
  - [`docs/04-ai-collaborations/QA.md` (32 проблем)](#docs04-ai-collaborationsqamd-32-проблем)
  - [`docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` (31 проблем)](#docs02-anthropic-vacancies186-appendix-c-sample-use-cases-in-detailmd-31-проблем)
  - [`docs/SPELLCHECK.md` (31 проблем)](#docsspellcheckmd-31-проблем)
  - [`docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` (30 проблем)](#docs02-anthropic-vacancies256-3-what-makes-a-composite-skills-agentmd-30-проблем)
  - [`docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` (30 проблем)](#docs02-anthropic-vacancies365-развёрнутый-анализ-внуковой-комбинацииmd-30-проблем)
  - [`docs/02-anthropic-vacancies/68-about.md` (30 проблем)](#docs02-anthropic-vacancies68-aboutmd-30-проблем)
  - [`docs/04-ai-collaborations/04-приоритетные-ансамбли.md` (29 проблем)](#docs04-ai-collaborations04-приоритетные-ансамблиmd-29-проблем)
  - [`docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` (29 проблем)](#docs04-ai-collaborations11-интеграционный-контракт-который-стоит-зафиксироватmd-29-проблем)
  - [`docs/02-anthropic-vacancies/150-appendix-c-version-history.md` (28 проблем)](#docs02-anthropic-vacancies150-appendix-c-version-historymd-28-проблем)
  - [`docs/02-anthropic-vacancies/163-9-call-for-partnership.md` (28 проблем)](#docs02-anthropic-vacancies163-9-call-for-partnershipmd-28-проблем)
  - [`docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` (28 проблем)](#docs02-anthropic-vacancies207-приложение-c-образцы-случаев-использования-в-деталmd-28-проблем)
  - [`docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` (28 проблем)](#docs02-anthropic-vacancies312-4-the-symbiotic-architecturemd-28-проблем)
  - [`docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` (28 проблем)](#docs02-anthropic-vacancies331-5-четыре-пути-интеграции-в-порядке-доступностиmd-28-проблем)
  - [`docs/02-anthropic-vacancies/67-о-проекте.md` (28 проблем)](#docs02-anthropic-vacancies67-о-проектеmd-28-проблем)
  - [`docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` (28 проблем)](#docs04-ai-collaborations14-ограничения-лицензии-и-что-пока-лучше-не-склеиватьmd-28-проблем)
  - [`docs/RISK_REGISTER.md` (28 проблем)](#docsrisk_registermd-28-проблем)
  - [`docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` (27 проблем)](#docs02-anthropic-vacancies313-5-four-integration-paths-in-order-of-accessibilitymd-27-проблем)
  - [`docs/02-anthropic-vacancies/133-обратная-связь.md` (26 проблем)](#docs02-anthropic-vacancies133-обратная-связьmd-26-проблем)
  - [`docs/02-anthropic-vacancies/159-5-economic-model.md` (26 проблем)](#docs02-anthropic-vacancies159-5-economic-modelmd-26-проблем)
  - [`docs/02-anthropic-vacancies/162-8-risk-analysis.md` (26 проблем)](#docs02-anthropic-vacancies162-8-risk-analysismd-26-проблем)
  - [`docs/02-anthropic-vacancies/164-10-appendices.md` (26 проблем)](#docs02-anthropic-vacancies164-10-appendicesmd-26-проблем)
  - [`docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` (26 проблем)](#docs02-anthropic-vacancies248-приложение-c-архитектура-быстрого-старта-для-sgb-аmd-26-проблем)
  - [`docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` (26 проблем)](#docs04-ai-collaborations05-план-прототипа-и-возможные-контактыmd-26-проблем)
  - [`docs/TAGS.md` (26 проблем)](#docstagsmd-26-проблем)
  - [`docs/02-anthropic-vacancies/00-intro.md` (25 проблем)](#docs02-anthropic-vacancies00-intromd-25-проблем)
  - [`docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` (25 проблем)](#docs02-anthropic-vacancies160-6-governance-and-ethicsmd-25-проблем)
  - [`docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` (25 проблем)](#docs02-anthropic-vacancies213-2-what-makes-a-professional-colleague-agentmd-25-проблем)
  - [`docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` (25 проблем)](#docs02-anthropic-vacancies366-технический-stack-svyazi-2-0-foundationmd-25-проблем)
  - [`docs/01-svyazi/07-mvp-planning.md` (24 проблем)](#docs01-svyazi07-mvp-planningmd-24-проблем)
  - [`docs/02-anthropic-vacancies/148-appendix-a-glossary.md` (24 проблем)](#docs02-anthropic-vacancies148-appendix-a-glossarymd-24-проблем)
  - [`docs/02-anthropic-vacancies/174-5-architectural-specification.md` (24 проблем)](#docs02-anthropic-vacancies174-5-architectural-specificationmd-24-проблем)
  - [`docs/02-anthropic-vacancies/179-10-open-questions.md` (24 проблем)](#docs02-anthropic-vacancies179-10-open-questionsmd-24-проблем)
  - [`docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` (24 проблем)](#docs02-anthropic-vacancies216-5-the-economics-of-profession-wide-replicationmd-24-проблем)
  - [`docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` (24 проблем)](#docs02-anthropic-vacancies236-5-экономика-тиражирования-по-профессииmd-24-проблем)
  - [`docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` (24 проблем)](#docs02-anthropic-vacancies315-7-practical-first-steps-this-monthmd-24-проблем)
  - [`docs/01-svyazi/01-executive-summary.md` (23 проблем)](#docs01-svyazi01-executive-summarymd-23-проблем)
  - [`docs/02-anthropic-vacancies/156-2-target-populations.md` (23 проблем)](#docs02-anthropic-vacancies156-2-target-populationsmd-23-проблем)
  - [`docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` (23 проблем)](#docs02-anthropic-vacancies177-8-risks-and-mitigationsmd-23-проблем)
  - [`docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` (23 проблем)](#docs02-anthropic-vacancies195-5-архитектурная-спецификацияmd-23-проблем)
  - [`docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` (23 проблем)](#docs02-anthropic-vacancies364-final-note-ты-experimentmd-23-проблем)
  - [`docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` (23 проблем)](#docs02-anthropic-vacancies78-3-registry-nautilus-jsonmd-23-проблем)
  - [`docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` (23 проблем)](#docs04-ai-collaborations03-карта-найденных-проектов-и-паттерновmd-23-проблем)
  - [`docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` (23 проблем)](#docs04-ai-collaborations10-новые-ансамбли-следующего-шагаmd-23-проблем)
  - [`docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` (23 проблем)](#docs04-ai-collaborations13-контактная-стратегия-и-узкие-вопросы-для-авторовmd-23-проблем)
  - [`docs/TOPIC_MODEL.md` (23 проблем)](#docstopic_modelmd-23-проблем)
  - [`docs/01-svyazi/10-second-order-ensembles.md` (22 проблем)](#docs01-svyazi10-second-order-ensemblesmd-22-проблем)
  - [`docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` (22 проблем)](#docs02-anthropic-vacancies02-общий-план-развития-nautilus-portal-protocolmd-22-проблем)
  - [`docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` (22 проблем)](#docs02-anthropic-vacancies178-9-phased-rollout-strategymd-22-проблем)
  - [`docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` (22 проблем)](#docs02-anthropic-vacancies200-10-открытые-вопросыmd-22-проблем)
  - [`docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` (22 проблем)](#docs02-anthropic-vacancies228-appendix-c-quick-start-architecture-for-sgb-advocamd-22-проблем)
  - [`docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` (22 проблем)](#docs02-anthropic-vacancies257-4-the-sub-agent-registrymd-22-проблем)
  - [`docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` (22 проблем)](#docs02-anthropic-vacancies259-6-coordination-and-disagreement-resolutionmd-22-проблем)
  - [`docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` (22 проблем)](#docs02-anthropic-vacancies272-appendix-d-connection-diagrammd-22-проблем)
  - [`docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` (22 проблем)](#docs02-anthropic-vacancies330-4-симбиотическая-архитектураmd-22-проблем)
  - [`docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` (22 проблем)](#docs04-ai-collaborations06-безопасность-приватность-и-бюджетный-роутингmd-22-проблем)
  - [`docs/01-svyazi/13-contacts.md` (21 проблем)](#docs01-svyazi13-contactsmd-21-проблем)
  - [`docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` (21 проблем)](#docs02-anthropic-vacancies08-3-registry-nautilus-jsonmd-21-проблем)
  - [`docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` (21 проблем)](#docs02-anthropic-vacancies139-2-the-double-triangle-architecturemd-21-проблем)
  - [`docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` (21 проблем)](#docs02-anthropic-vacancies233-2-что-делает-агента-профессиональным-коллегойmd-21-проблем)
  - [`docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` (21 проблем)](#docs02-anthropic-vacancies255-2-the-twenty-one-teachers-patternmd-21-проблем)
  - [`docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` (21 проблем)](#docs02-anthropic-vacancies262-9-integration-with-okwf-infrastructuremd-21-проблем)
  - [`docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` (21 проблем)](#docs02-anthropic-vacancies323-appendix-c-sample-ingit-mcp-server-tool-specificatmd-21-проблем)
  - [`docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` (21 проблем)](#docs02-anthropic-vacancies329-3-что-ingit-обеспечивает-чего-cowork-не-хватаетmd-21-проблем)
  - [`docs/04-ai-collaborations/01-executive-summary.md` (21 проблем)](#docs04-ai-collaborations01-executive-summarymd-21-проблем)
  - [`docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` (21 проблем)](#docs04-ai-collaborations09-архитектурные-зазоры-которые-важнее-новых-инструмеmd-21-проблем)
  - [`docs/CITATION_INDEX.md` (21 проблем)](#docscitation_indexmd-21-проблем)
  - [`docs/01-svyazi/09-architectural-gaps.md` (20 проблем)](#docs01-svyazi09-architectural-gapsmd-20-проблем)
  - [`docs/01-svyazi/11-integration-contracts.md` (20 проблем)](#docs01-svyazi11-integration-contractsmd-20-проблем)
  - [`docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` (20 проблем)](#docs02-anthropic-vacancies171-2-historical-precedents-agents-as-civilizational-imd-20-проблем)
  - [`docs/02-anthropic-vacancies/175-6-ethical-framework.md` (20 проблем)](#docs02-anthropic-vacancies175-6-ethical-frameworkmd-20-проблем)
  - [`docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` (20 проблем)](#docs02-anthropic-vacancies176-7-governance-and-oversightmd-20-проблем)
  - [`docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` (20 проблем)](#docs02-anthropic-vacancies198-8-риски-и-меры-противодействияmd-20-проблем)
  - [`docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` (20 проблем)](#docs02-anthropic-vacancies199-9-стратегия-поэтапного-развёртыванияmd-20-проблем)
  - [`docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` (20 проблем)](#docs02-anthropic-vacancies240-9-связь-с-другими-типами-агентовmd-20-проблем)
  - [`docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` (20 проблем)](#docs02-anthropic-vacancies303-приложение-визуализация-позиции-в-серииmd-20-проблем)
  - [`docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` (20 проблем)](#docs02-anthropic-vacancies314-6-refined-ingit-scope-with-cowork-in-mindmd-20-проблем)
  - [`docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` (20 проблем)](#docs02-anthropic-vacancies332-6-уточнённый-объём-ingit-с-учётом-coworkmd-20-проблем)
  - [`docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` (20 проблем)](#docs02-anthropic-vacancies333-7-практические-первые-шаги-в-этом-месяцеmd-20-проблем)
  - [`docs/02-anthropic-vacancies/90-15-security-considerations.md` (20 проблем)](#docs02-anthropic-vacancies90-15-security-considerationsmd-20-проблем)
  - [`docs/01-svyazi/06-security-privacy.md` (19 проблем)](#docs01-svyazi06-security-privacymd-19-проблем)
  - [`docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` (19 проблем)](#docs02-anthropic-vacancies143-6-four-deployment-domainsmd-19-проблем)
  - [`docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` (19 проблем)](#docs02-anthropic-vacancies172-3-what-makes-a-representative-agentmd-19-проблем)
  - [`docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` (19 проблем)](#docs02-anthropic-vacancies193-3-что-делает-агента-представительскимmd-19-проблем)
  - [`docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` (19 проблем)](#docs02-anthropic-vacancies215-4-architecture-of-professional-colleague-agentsmd-19-проблем)
  - [`docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` (19 проблем)](#docs02-anthropic-vacancies311-3-what-ingit-provides-that-cowork-lacksmd-19-проблем)
  - [`docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` (19 проблем)](#docs02-anthropic-vacancies317-9-risks-and-open-questionsmd-19-проблем)
  - [`docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` (19 проблем)](#docs02-anthropic-vacancies336-10-стратегическое-позиционированиеmd-19-проблем)
  - [`docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` (19 проблем)](#docs02-anthropic-vacancies87-12-onboarding-paths-normativemd-19-проблем)
  - [`docs/04-ai-collaborations/07-выводы.md` (19 проблем)](#docs04-ai-collaborations07-выводыmd-19-проблем)
  - [`docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` (19 проблем)](#docs04-ai-collaborations12-дорожная-карта-прототипа-следующей-итерацииmd-19-проблем)
  - [`docs/INDEX.md` (19 проблем)](#docsindexmd-19-проблем)
  - [`docs/01-svyazi/12-roadmap.md` (18 проблем)](#docs01-svyazi12-roadmapmd-18-проблем)
  - [`docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` (18 проблем)](#docs02-anthropic-vacancies140-3-three-inter-layer-protocolsmd-18-проблем)
  - [`docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` (18 проблем)](#docs02-anthropic-vacancies161-7-phased-rollout-planmd-18-проблем)
  - [`docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` (18 проблем)](#docs02-anthropic-vacancies170-1-the-cinderella-syndrome-why-quality-stays-invisimd-18-проблем)
  - [`docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` (18 проблем)](#docs02-anthropic-vacancies220-9-relationship-to-other-agent-typesmd-18-проблем)
  - [`docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` (18 проблем)](#docs02-anthropic-vacancies227-appendix-b-decision-framework-when-to-build-type-1md-18-проблем)
  - [`docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` (18 проблем)](#docs02-anthropic-vacancies260-7-economics-of-combinatorial-replicationmd-18-проблем)
  - [`docs/02-anthropic-vacancies/279-existing-approximations.md` (18 проблем)](#docs02-anthropic-vacancies279-existing-approximationsmd-18-проблем)
  - [`docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` (18 проблем)](#docs02-anthropic-vacancies316-8-implications-for-nautilus-and-okwfmd-18-проблем)
  - [`docs/02-anthropic-vacancies/318-10-strategic-positioning.md` (18 проблем)](#docs02-anthropic-vacancies318-10-strategic-positioningmd-18-проблем)
  - [`docs/02-anthropic-vacancies/80-5-compatibility-levels.md` (18 проблем)](#docs02-anthropic-vacancies80-5-compatibility-levelsmd-18-проблем)
  - [`docs/CONSISTENCY.md` (18 проблем)](#docsconsistencymd-18-проблем)
  - [`docs/NARRATIVE.md` (18 проблем)](#docsnarrativemd-18-проблем)
  - [`docs/ONBOARDING.md` (18 проблем)](#docsonboardingmd-18-проблем)
  - [`docs/01-svyazi/14-limitations.md` (17 проблем)](#docs01-svyazi14-limitationsmd-17-проблем)
  - [`docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` (17 проблем)](#docs02-anthropic-vacancies197-7-управление-и-надзорmd-17-проблем)
  - [`docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` (17 проблем)](#docs02-anthropic-vacancies214-3-empirical-case-study-обучайmd-17-проблем)
  - [`docs/02-anthropic-vacancies/294-существующие-приближения.md` (17 проблем)](#docs02-anthropic-vacancies294-существующие-приближенияmd-17-проблем)
  - [`docs/02-anthropic-vacancies/79-4-passport-passport-md.md` (17 проблем)](#docs02-anthropic-vacancies79-4-passport-passport-mdmd-17-проблем)
  - [`docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` (17 проблем)](#docs02-anthropic-vacancies88-13-rest-api-contract-normative-for-portalsmd-17-проблем)
  - [`docs/SITEMAP.md` (17 проблем)](#docssitemapmd-17-проблем)
  - [`docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` (16 проблем)](#docs02-anthropic-vacancies142-5-pattern-library-as-bridge-between-trianglesmd-16-проблем)
  - [`docs/02-anthropic-vacancies/144-7-open-questions.md` (16 проблем)](#docs02-anthropic-vacancies144-7-open-questionsmd-16-проблем)
  - [`docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` (16 проблем)](#docs02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd-16-проблем)
  - [`docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` (16 проблем)](#docs02-anthropic-vacancies235-4-архитектура-профессиональных-коллег-агентовmd-16-проблем)
  - [`docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` (16 проблем)](#docs02-anthropic-vacancies247-приложение-b-рамка-принятия-решений-когда-строить-md-16-проблем)
  - [`docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` (16 проблем)](#docs02-anthropic-vacancies258-5-configuration-how-principals-build-their-ensemblmd-16-проблем)
  - [`docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` (16 проблем)](#docs02-anthropic-vacancies263-10-risks-specific-to-composite-architecturesmd-16-проблем)
  - [`docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` (16 проблем)](#docs02-anthropic-vacancies280-the-specific-case-in-front-of-usmd-16-проблем)
  - [`docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` (16 проблем)](#docs02-anthropic-vacancies328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строиmd-16-проблем)
  - [`docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` (16 проблем)](#docs02-anthropic-vacancies334-8-импликации-для-nautilus-и-okwfmd-16-проблем)
  - [`docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` (16 проблем)](#docs02-anthropic-vacancies335-9-риски-и-открытые-вопросыmd-16-проблем)
  - [`docs/CHANGELOG_AUTO.md` (16 проблем)](#docschangelog_automd-16-проблем)
  - [`docs/LLM_SUMMARIES.md` (16 проблем)](#docsllm_summariesmd-16-проблем)
  - [`docs/01-svyazi/03-component-catalog.md` (15 проблем)](#docs01-svyazi03-component-catalogmd-15-проблем)
  - [`docs/01-svyazi/08-conclusions.md` (15 проблем)](#docs01-svyazi08-conclusionsmd-15-проблем)
  - [`docs/02-anthropic-vacancies/09-4-passport-passport-md.md` (15 проблем)](#docs02-anthropic-vacancies09-4-passport-passport-mdmd-15-проблем)
  - [`docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` (15 проблем)](#docs02-anthropic-vacancies234-3-эмпирический-кейс-обучайmd-15-проблем)
  - [`docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` (15 проблем)](#docs02-anthropic-vacancies284-practical-recommendations-for-the-current-projectmd-15-проблем)
  - [`docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` (15 проблем)](#docs02-anthropic-vacancies288-appendix-position-in-series-visualizationmd-15-проблем)
  - [`docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` (15 проблем)](#docs02-anthropic-vacancies299-практические-рекомендации-для-текущего-проектаmd-15-проблем)
  - [`docs/02-anthropic-vacancies/356-твой-workflow.md` (15 проблем)](#docs02-anthropic-vacancies356-твой-workflowmd-15-проблем)
  - [`docs/02-anthropic-vacancies/92-17-versioning-policy.md` (15 проблем)](#docs02-anthropic-vacancies92-17-versioning-policymd-15-проблем)
  - [`docs/03-technology-combinations/02-knowledge-graphs.md` (15 проблем)](#docs03-technology-combinations02-knowledge-graphsmd-15-проблем)
  - [`docs/01-svyazi/02-methodology.md` (14 проблем)](#docs01-svyazi02-methodologymd-14-проблем)
  - [`docs/02-anthropic-vacancies/104-appendix-c-references.md` (14 проблем)](#docs02-anthropic-vacancies104-appendix-c-referencesmd-14-проблем)
  - [`docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` (14 проблем)](#docs02-anthropic-vacancies109-3-принципы-консолидации-фаза-cmd-14-проблем)
  - [`docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` (14 проблем)](#docs02-anthropic-vacancies114-7-реализация-в-проекте-nautilusmd-14-проблем)
  - [`docs/02-anthropic-vacancies/122-глоссарий.md` (14 проблем)](#docs02-anthropic-vacancies122-глоссарийmd-14-проблем)
  - [`docs/02-anthropic-vacancies/155-1-problem-statement.md` (14 проблем)](#docs02-anthropic-vacancies155-1-problem-statementmd-14-проблем)
  - [`docs/02-anthropic-vacancies/196-6-этическая-рамка.md` (14 проблем)](#docs02-anthropic-vacancies196-6-этическая-рамкаmd-14-проблем)
  - [`docs/02-anthropic-vacancies/264-11-open-questions.md` (14 проблем)](#docs02-anthropic-vacancies264-11-open-questionsmd-14-проблем)
  - [`docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` (14 проблем)](#docs02-anthropic-vacancies295-конкретный-случай-перед-намиmd-14-проблем)
  - [`docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` (14 проблем)](#docs02-anthropic-vacancies309-1-the-cowork-discovery-and-why-it-changes-everythimd-14-проблем)
  - [`docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` (14 проблем)](#docs02-anthropic-vacancies310-2-what-cowork-provides-that-ingit-doesn-t-need-to-md-14-проблем)
  - [`docs/02-anthropic-vacancies/320-references.md` (14 проблем)](#docs02-anthropic-vacancies320-referencesmd-14-проблем)
  - [`docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` (14 проблем)](#docs02-anthropic-vacancies327-1-открытие-cowork-и-почему-это-меняет-всёmd-14-проблем)
  - [`docs/02-anthropic-vacancies/338-ссылки.md` (14 проблем)](#docs02-anthropic-vacancies338-ссылкиmd-14-проблем)
  - [`docs/02-anthropic-vacancies/81-6-adapter-interface.md` (14 проблем)](#docs02-anthropic-vacancies81-6-adapter-interfacemd-14-проблем)
  - [`docs/02-anthropic-vacancies/85-10-query-flow.md` (14 проблем)](#docs02-anthropic-vacancies85-10-query-flowmd-14-проблем)
  - [`docs/TECH_RADAR.md` (14 проблем)](#docstech_radarmd-14-проблем)
  - [`docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` (13 проблем)](#docs02-anthropic-vacancies117-10-конкретный-план-применения-к-текущим-документамmd-13-проблем)
  - [`docs/02-anthropic-vacancies/130-отладка.md` (13 проблем)](#docs02-anthropic-vacancies130-отладкаmd-13-проблем)
  - [`docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` (13 проблем)](#docs02-anthropic-vacancies141-4-nautilus-portal-as-reference-substratemd-13-проблем)
  - [`docs/02-anthropic-vacancies/18-6-adapter-interface.md` (13 проблем)](#docs02-anthropic-vacancies18-6-adapter-interfacemd-13-проблем)
  - [`docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` (13 проблем)](#docs02-anthropic-vacancies191-1-синдром-золушки-почему-качество-остаётся-невидимmd-13-проблем)
  - [`docs/02-anthropic-vacancies/21-9-query-flow.md` (13 проблем)](#docs02-anthropic-vacancies21-9-query-flowmd-13-проблем)
  - [`docs/02-anthropic-vacancies/23-11-security-considerations.md` (13 проблем)](#docs02-anthropic-vacancies23-11-security-considerationsmd-13-проблем)
  - [`docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` (13 проблем)](#docs02-anthropic-vacancies265-12-call-for-collaborationmd-13-проблем)
  - [`docs/02-anthropic-vacancies/302-ссылки.md` (13 проблем)](#docs02-anthropic-vacancies302-ссылкиmd-13-проблем)
  - [`docs/02-anthropic-vacancies/40-bridges.md` (13 проблем)](#docs02-anthropic-vacancies40-bridgesmd-13-проблем)
  - [`docs/02-anthropic-vacancies/48-content-overview.md` (13 проблем)](#docs02-anthropic-vacancies48-content-overviewmd-13-проблем)
  - [`docs/02-anthropic-vacancies/57-native-format.md` (13 проблем)](#docs02-anthropic-vacancies57-native-formatmd-13-проблем)
  - [`docs/02-anthropic-vacancies/83-8-q6-space-normative.md` (13 проблем)](#docs02-anthropic-vacancies83-8-q6-space-normativemd-13-проблем)
  - [`docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` (13 проблем)](#docs04-ai-collaborations08-что-это-продолжение-добавляетmd-13-проблем)
  - [`docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` (12 проблем)](#docs02-anthropic-vacancies107-1-контекст-и-мотивацияmd-12-проблем)
  - [`docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` (12 проблем)](#docs02-anthropic-vacancies138-1-why-single-triangle-models-are-incompletemd-12-проблем)
  - [`docs/02-anthropic-vacancies/17-5-compatibility-levels.md` (12 проблем)](#docs02-anthropic-vacancies17-5-compatibility-levelsmd-12-проблем)
  - [`docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` (12 проблем)](#docs02-anthropic-vacancies20-8-consensus-algorithmmd-12-проблем)
  - [`docs/02-anthropic-vacancies/24-12-versioning-policy.md` (12 проблем)](#docs02-anthropic-vacancies24-12-versioning-policymd-12-проблем)
  - [`docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` (12 проблем)](#docs02-anthropic-vacancies254-1-why-the-binary-view-is-incompletemd-12-проблем)
  - [`docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` (12 проблем)](#docs02-anthropic-vacancies276-the-two-layer-stack-as-it-existsmd-12-проблем)
  - [`docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` (12 проблем)](#docs02-anthropic-vacancies278-why-this-hasn-t-been-builtmd-12-проблем)
  - [`docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` (12 проблем)](#docs02-anthropic-vacancies306-with-anthropic-s-cowork-platformmd-12-проблем)
  - [`docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` (12 проблем)](#docs02-anthropic-vacancies324-ingit-как-cowork-интегрированная-подложка-рабочегоmd-12-проблем)
  - [`docs/02-anthropic-vacancies/76-1-introduction.md` (12 проблем)](#docs02-anthropic-vacancies76-1-introductionmd-12-проблем)
  - [`docs/02-anthropic-vacancies/07-2-terminology.md` (11 проблем)](#docs02-anthropic-vacancies07-2-terminologymd-11-проблем)
  - [`docs/02-anthropic-vacancies/108-2-формальный-workflow.md` (11 проблем)](#docs02-anthropic-vacancies108-2-формальный-workflowmd-11-проблем)
  - [`docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` (11 проблем)](#docs02-anthropic-vacancies110-вопрос-fallback-ratio-как-критический-или-осмысленmd-11-проблем)
  - [`docs/02-anthropic-vacancies/111-4-условия-применимости.md` (11 проблем)](#docs02-anthropic-vacancies111-4-условия-применимостиmd-11-проблем)
  - [`docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` (11 проблем)](#docs02-anthropic-vacancies112-5-связь-с-существующими-методологиямиmd-11-проблем)
  - [`docs/02-anthropic-vacancies/25-13-reference-implementation.md` (11 проблем)](#docs02-anthropic-vacancies25-13-reference-implementationmd-11-проблем)
  - [`docs/02-anthropic-vacancies/266-13-closing.md` (11 проблем)](#docs02-anthropic-vacancies266-13-closingmd-11-проблем)
  - [`docs/02-anthropic-vacancies/267-acknowledgments.md` (11 проблем)](#docs02-anthropic-vacancies267-acknowledgmentsmd-11-проблем)
  - [`docs/02-anthropic-vacancies/268-references.md` (11 проблем)](#docs02-anthropic-vacancies268-referencesmd-11-проблем)
  - [`docs/02-anthropic-vacancies/319-acknowledgments.md` (11 проблем)](#docs02-anthropic-vacancies319-acknowledgmentsmd-11-проблем)
  - [`docs/02-anthropic-vacancies/34-appendix-b-change-log.md` (11 проблем)](#docs02-anthropic-vacancies34-appendix-b-change-logmd-11-проблем)
  - [`docs/02-anthropic-vacancies/37-native-format.md` (11 проблем)](#docs02-anthropic-vacancies37-native-formatmd-11-проблем)
  - [`docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` (11 проблем)](#docs02-anthropic-vacancies64-for-the-curious-philosophymd-11-проблем)
  - [`docs/02-anthropic-vacancies/82-7-portalentry-structure.md` (11 проблем)](#docs02-anthropic-vacancies82-7-portalentry-structuremd-11-проблем)
  - [`docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` (11 проблем)](#docs02-anthropic-vacancies84-9-consensus-algorithmmd-11-проблем)
  - [`docs/03-technology-combinations/05-benchmarks.md` (11 проблем)](#docs03-technology-combinations05-benchmarksmd-11-проблем)
  - [`docs/03-technology-combinations/QA.md` (11 проблем)](#docs03-technology-combinationsqamd-11-проблем)
  - [`docs/05-habr-projects/02-collaboration-partners.md` (11 проблем)](#docs05-habr-projects02-collaboration-partnersmd-11-проблем)
  - [`docs/DIGEST.md` (11 проблем)](#docsdigestmd-11-проблем)
  - [`docs/SIMILAR.md` (11 проблем)](#docssimilarmd-11-проблем)
  - [`docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` (10 проблем)](#docs02-anthropic-vacancies119-appendix-b-примеры-расхождений-и-их-разрешенияmd-10-проблем)
  - [`docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` (10 проблем)](#docs02-anthropic-vacancies127-подключение-к-claude-desktopmd-10-проблем)
  - [`docs/02-anthropic-vacancies/145-8-call-to-action.md` (10 проблем)](#docs02-anthropic-vacancies145-8-call-to-actionmd-10-проблем)
  - [`docs/02-anthropic-vacancies/146-acknowledgments.md` (10 проблем)](#docs02-anthropic-vacancies146-acknowledgmentsmd-10-проблем)
  - [`docs/02-anthropic-vacancies/245-ссылки.md` (10 проблем)](#docs02-anthropic-vacancies245-ссылкиmd-10-проблем)
  - [`docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` (10 проблем)](#docs02-anthropic-vacancies277-what-s-missing-layer-bmd-10-проблем)
  - [`docs/02-anthropic-vacancies/287-references.md` (10 проблем)](#docs02-anthropic-vacancies287-referencesmd-10-проблем)
  - [`docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` (10 проблем)](#docs02-anthropic-vacancies289-инфраструктура-для-ai-совместной-интеллектуальной-md-10-проблем)
  - [`docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` (10 проблем)](#docs02-anthropic-vacancies291-двухслойный-стек-как-он-существуетmd-10-проблем)
  - [`docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` (10 проблем)](#docs02-anthropic-vacancies292-что-отсутствует-слой-bmd-10-проблем)
  - [`docs/02-anthropic-vacancies/349-твоя-личность.md` (10 проблем)](#docs02-anthropic-vacancies349-твоя-личностьmd-10-проблем)
  - [`docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` (10 проблем)](#docs02-anthropic-vacancies351-что-ты-можешь-делатьmd-10-проблем)
  - [`docs/02-anthropic-vacancies/42-author-contact.md` (10 проблем)](#docs02-anthropic-vacancies42-author-contactmd-10-проблем)
  - [`docs/02-anthropic-vacancies/43-history.md` (10 проблем)](#docs02-anthropic-vacancies43-historymd-10-проблем)
  - [`docs/02-anthropic-vacancies/56-essence.md` (10 проблем)](#docs02-anthropic-vacancies56-essencemd-10-проблем)
  - [`docs/02-anthropic-vacancies/72-расписание-фазы-3.md` (10 проблем)](#docs02-anthropic-vacancies72-расписание-фазы-3md-10-проблем)
  - [`docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` (10 проблем)](#docs02-anthropic-vacancies94-19-adr-001-federation-over-mergingmd-10-проблем)
  - [`docs/03-technology-combinations/03-local-first.md` (10 проблем)](#docs03-technology-combinations03-local-firstmd-10-проблем)
  - [`docs/05-habr-projects/memory/yodoca.md` (10 проблем)](#docs05-habr-projectsmemoryyodocamd-10-проблем)
  - [`docs/COMPONENT_MATRIX.md` (10 проблем)](#docscomponent_matrixmd-10-проблем)
  - [`docs/DEPENDENCY_MAP.md` (10 проблем)](#docsdependency_mapmd-10-проблем)
  - [`docs/autofilled/research-summary.md` (10 проблем)](#docsautofilledresearch-summarymd-10-проблем)
  - [`docs/02-anthropic-vacancies/103-appendix-b-change-log.md` (9 проблем)](#docs02-anthropic-vacancies103-appendix-b-change-logmd-9-проблем)
  - [`docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` (9 проблем)](#docs02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd-9-проблем)
  - [`docs/02-anthropic-vacancies/123-portal-mcp-py.md` (9 проблем)](#docs02-anthropic-vacancies123-portal-mcp-pymd-9-проблем)
  - [`docs/02-anthropic-vacancies/22-10-queryresult-structure.md` (9 проблем)](#docs02-anthropic-vacancies22-10-queryresult-structuremd-9-проблем)
  - [`docs/02-anthropic-vacancies/221-10-open-questions.md` (9 проблем)](#docs02-anthropic-vacancies221-10-open-questionsmd-9-проблем)
  - [`docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` (9 проблем)](#docs02-anthropic-vacancies222-11-call-for-collaborationmd-9-проблем)
  - [`docs/02-anthropic-vacancies/225-references.md` (9 проблем)](#docs02-anthropic-vacancies225-referencesmd-9-проблем)
  - [`docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` (9 проблем)](#docs02-anthropic-vacancies26-14-adr-001-federation-over-mergingmd-9-проблем)
  - [`docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` (9 проблем)](#docs02-anthropic-vacancies261-8-seven-domains-of-applicationmd-9-проблем)
  - [`docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` (9 проблем)](#docs02-anthropic-vacancies27-15-glossary-of-examplesmd-9-проблем)
  - [`docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` (9 проблем)](#docs02-anthropic-vacancies274-the-missing-middle-layer-between-chat-and-codemd-9-проблем)
  - [`docs/02-anthropic-vacancies/275-why-this-document-exists.md` (9 проблем)](#docs02-anthropic-vacancies275-why-this-document-existsmd-9-проблем)
  - [`docs/02-anthropic-vacancies/281-the-recursive-insight.md` (9 проблем)](#docs02-anthropic-vacancies281-the-recursive-insightmd-9-проблем)
  - [`docs/02-anthropic-vacancies/285-closing.md` (9 проблем)](#docs02-anthropic-vacancies285-closingmd-9-проблем)
  - [`docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` (9 проблем)](#docs02-anthropic-vacancies293-почему-это-не-было-построеноmd-9-проблем)
  - [`docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` (9 проблем)](#docs02-anthropic-vacancies354-существующий-landscape-collaborators-твоя-working-md-9-проблем)
  - [`docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` (9 проблем)](#docs02-anthropic-vacancies355-существующие-документы-dhlab-твой-contextmd-9-проблем)
  - [`docs/02-anthropic-vacancies/50-bridges.md` (9 проблем)](#docs02-anthropic-vacancies50-bridgesmd-9-проблем)
  - [`docs/02-anthropic-vacancies/52-author-contact.md` (9 проблем)](#docs02-anthropic-vacancies52-author-contactmd-9-проблем)
  - [`docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` (9 проблем)](#docs02-anthropic-vacancies54-for-the-curious-philosophymd-9-проблем)
  - [`docs/02-anthropic-vacancies/65-readme-md.md` (9 проблем)](#docs02-anthropic-vacancies65-readme-mdmd-9-проблем)
  - [`docs/02-anthropic-vacancies/77-2-terminology.md` (9 проблем)](#docs02-anthropic-vacancies77-2-terminologymd-9-проблем)
  - [`docs/02-anthropic-vacancies/86-11-relevance-ranking.md` (9 проблем)](#docs02-anthropic-vacancies86-11-relevance-rankingmd-9-проблем)
  - [`docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` (9 проблем)](#docs02-anthropic-vacancies91-16-mcp-extension-informativemd-9-проблем)
  - [`docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` (9 проблем)](#docs02-anthropic-vacancies96-21-adr-003-five-onboarding-paths-as-equal-rankmd-9-проблем)
  - [`docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` (9 проблем)](#docs02-anthropic-vacancies97-22-glossary-of-reference-examplesmd-9-проблем)
  - [`docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` (9 проблем)](#docs04-ai-collaborations02-методика-и-рамка-отбораmd-9-проблем)
  - [`docs/05-habr-projects/memory/ngt-memory.md` (9 проблем)](#docs05-habr-projectsmemoryngt-memorymd-9-проблем)
  - [`docs/02-anthropic-vacancies/05-0-status-of-this-document.md` (8 проблем)](#docs02-anthropic-vacancies05-0-status-of-this-documentmd-8-проблем)
  - [`docs/02-anthropic-vacancies/06-1-introduction.md` (8 проблем)](#docs02-anthropic-vacancies06-1-introductionmd-8-проблем)
  - [`docs/ACTION_ITEMS.md` (8 проблем)](#docsaction_itemsmd-8-проблем)
  - [`docs/DEPENDENCY_MAP.md` (8 проблем)](#docsdependency_mapmd-8-проблем)
  - [`docs/02-anthropic-vacancies/105-review-methodology-md.md` (8 проблем)](#docs02-anthropic-vacancies105-review-methodology-mdmd-8-проблем)
  - [`docs/02-anthropic-vacancies/106-tl-dr.md` (8 проблем)](#docs02-anthropic-vacancies106-tl-drmd-8-проблем)
  - [`docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` (8 проблем)](#docs02-anthropic-vacancies116-9-checklist-применения-методологииmd-8-проблем)
  - [`docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` (8 проблем)](#docs02-anthropic-vacancies125-readme-mcp-md-инструкция-по-установкеmd-8-проблем)
  - [`docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` (8 проблем)](#docs02-anthropic-vacancies129-примеры-запросов-в-claudemd-8-проблем)
  - [`docs/02-anthropic-vacancies/136-abstract.md` (8 проблем)](#docs02-anthropic-vacancies136-abstractmd-8-проблем)
  - [`docs/02-anthropic-vacancies/147-references.md` (8 проблем)](#docs02-anthropic-vacancies147-referencesmd-8-проблем)
  - [`docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` (8 проблем)](#docs02-anthropic-vacancies149-appendix-b-summary-of-contributionsmd-8-проблем)
  - [`docs/02-anthropic-vacancies/153-executive-summary.md` (8 проблем)](#docs02-anthropic-vacancies153-executive-summarymd-8-проблем)
  - [`docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` (8 проблем)](#docs02-anthropic-vacancies167-ai-mediated-representation-for-underrepresented-exmd-8-проблем)
  - [`docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` (8 проблем)](#docs02-anthropic-vacancies188-ai-опосредованное-представительство-для-недопредстmd-8-проблем)
  - [`docs/02-anthropic-vacancies/19-7-portalentry-structure.md` (8 проблем)](#docs02-anthropic-vacancies19-7-portalentry-structuremd-8-проблем)
  - [`docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` (8 проблем)](#docs02-anthropic-vacancies209-a-typology-of-ai-agents-on-the-principal-side-and-md-8-проблем)
  - [`docs/02-anthropic-vacancies/210-abstract.md` (8 проблем)](#docs02-anthropic-vacancies210-abstractmd-8-проблем)
  - [`docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` (8 проблем)](#docs02-anthropic-vacancies229-профессиональные-коллеги-агентыmd-8-проблем)
  - [`docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` (8 проблем)](#docs02-anthropic-vacancies251-ai-support-through-configurable-specialist-ensemblmd-8-проблем)
  - [`docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` (8 проблем)](#docs02-anthropic-vacancies283-what-this-document-doesn-t-solvemd-8-проблем)
  - [`docs/02-anthropic-vacancies/38-content-overview.md` (8 проблем)](#docs02-anthropic-vacancies38-content-overviewmd-8-проблем)
  - [`docs/02-anthropic-vacancies/41-compatibility-level.md` (8 проблем)](#docs02-anthropic-vacancies41-compatibility-levelmd-8-проблем)
  - [`docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` (8 проблем)](#docs02-anthropic-vacancies44-for-the-curious-philosophymd-8-проблем)
  - [`docs/02-anthropic-vacancies/51-compatibility-level.md` (8 проблем)](#docs02-anthropic-vacancies51-compatibility-levelmd-8-проблем)
  - [`docs/02-anthropic-vacancies/53-history.md` (8 проблем)](#docs02-anthropic-vacancies53-historymd-8-проблем)
  - [`docs/02-anthropic-vacancies/60-bridges.md` (8 проблем)](#docs02-anthropic-vacancies60-bridgesmd-8-проблем)
  - [`docs/02-anthropic-vacancies/61-compatibility-level.md` (8 проблем)](#docs02-anthropic-vacancies61-compatibility-levelmd-8-проблем)
  - [`docs/02-anthropic-vacancies/62-author-contact.md` (8 проблем)](#docs02-anthropic-vacancies62-author-contactmd-8-проблем)
  - [`docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` (8 проблем)](#docs02-anthropic-vacancies71-критерии-выбора-для-фазы-3md-8-проблем)
  - [`docs/02-anthropic-vacancies/75-0-status-of-this-document.md` (8 проблем)](#docs02-anthropic-vacancies75-0-status-of-this-documentmd-8-проблем)
  - [`docs/02-anthropic-vacancies/93-18-reference-implementation.md` (8 проблем)](#docs02-anthropic-vacancies93-18-reference-implementationmd-8-проблем)
  - [`docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` (8 проблем)](#docs02-anthropic-vacancies95-20-adr-002-q6-as-first-class-protocol-conceptmd-8-проблем)
  - [`docs/03-technology-combinations/01-agent-routing.md` (8 проблем)](#docs03-technology-combinations01-agent-routingmd-8-проблем)
  - [`docs/ACTION_ITEMS.md` (8 проблем)](#docsaction_itemsmd-8-проблем)
  - [`docs/AUTOFILLED.md` (8 проблем)](#docsautofilledmd-8-проблем)
  - [`docs/KEYWORD_INDEX.md` (8 проблем)](#docskeyword_indexmd-8-проблем)
  - [`docs/contacts/antipozitive.md` (8 проблем)](#docscontactsantipozitivemd-8-проблем)
  - [`docs/02-anthropic-vacancies/03-portal-protocol-md.md` (7 проблем)](#docs02-anthropic-vacancies03-portal-protocol-mdmd-7-проблем)
  - [`docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` (7 проблем)](#docs02-anthropic-vacancies124-конфигурация-для-claude-desktopmd-7-проблем)
  - [`docs/02-anthropic-vacancies/128-доступные-инструменты.md` (7 проблем)](#docs02-anthropic-vacancies128-доступные-инструментыmd-7-проблем)
  - [`docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` (7 проблем)](#docs02-anthropic-vacancies131-ограничения-текущей-версии-0-1-0-draftmd-7-проблем)
  - [`docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` (7 проблем)](#docs02-anthropic-vacancies135-a-formal-model-for-human-ai-collaboration-in-distrmd-7-проблем)
  - [`docs/02-anthropic-vacancies/137-table-of-contents.md` (7 проблем)](#docs02-anthropic-vacancies137-table-of-contentsmd-7-проблем)
  - [`docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` (7 проблем)](#docs02-anthropic-vacancies152-ai-coordinated-infrastructure-for-distributed-expemd-7-проблем)
  - [`docs/02-anthropic-vacancies/169-table-of-contents.md` (7 проблем)](#docs02-anthropic-vacancies169-table-of-contentsmd-7-проблем)
  - [`docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` (7 проблем)](#docs02-anthropic-vacancies180-11-call-for-collaborationmd-7-проблем)
  - [`docs/02-anthropic-vacancies/181-12-closing.md` (7 проблем)](#docs02-anthropic-vacancies181-12-closingmd-7-проблем)
  - [`docs/02-anthropic-vacancies/182-acknowledgments.md` (7 проблем)](#docs02-anthropic-vacancies182-acknowledgmentsmd-7-проблем)
  - [`docs/02-anthropic-vacancies/183-references.md` (7 проблем)](#docs02-anthropic-vacancies183-referencesmd-7-проблем)
  - [`docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` (7 проблем)](#docs02-anthropic-vacancies184-appendix-a-connection-to-companion-papersmd-7-проблем)
  - [`docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` (7 проблем)](#docs02-anthropic-vacancies205-приложение-a-связь-с-сопроводительными-статьямиmd-7-проблем)
  - [`docs/02-anthropic-vacancies/211-table-of-contents.md` (7 проблем)](#docs02-anthropic-vacancies211-table-of-contentsmd-7-проблем)
  - [`docs/02-anthropic-vacancies/224-acknowledgments.md` (7 проблем)](#docs02-anthropic-vacancies224-acknowledgmentsmd-7-проблем)
  - [`docs/02-anthropic-vacancies/230-аннотация.md` (7 проблем)](#docs02-anthropic-vacancies230-аннотацияmd-7-проблем)
  - [`docs/02-anthropic-vacancies/231-содержание.md` (7 проблем)](#docs02-anthropic-vacancies231-содержаниеmd-7-проблем)
  - [`docs/02-anthropic-vacancies/253-table-of-contents.md` (7 проблем)](#docs02-anthropic-vacancies253-table-of-contentsmd-7-проблем)
  - [`docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` (7 проблем)](#docs02-anthropic-vacancies282-what-industry-will-likely-buildmd-7-проблем)
  - [`docs/02-anthropic-vacancies/286-acknowledgments.md` (7 проблем)](#docs02-anthropic-vacancies286-acknowledgmentsmd-7-проблем)
  - [`docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` (7 проблем)](#docs02-anthropic-vacancies290-почему-этот-документ-существуетmd-7-проблем)
  - [`docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` (7 проблем)](#docs02-anthropic-vacancies296-рекурсивное-прозрениеmd-7-проблем)
  - [`docs/02-anthropic-vacancies/308-table-of-contents.md` (7 проблем)](#docs02-anthropic-vacancies308-table-of-contentsmd-7-проблем)
  - [`docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` (7 проблем)](#docs02-anthropic-vacancies321-appendix-a-decision-tree-for-ingit-adoptersmd-7-проблем)
  - [`docs/02-anthropic-vacancies/337-благодарности.md` (7 проблем)](#docs02-anthropic-vacancies337-благодарностиmd-7-проблем)
  - [`docs/02-anthropic-vacancies/347-твоя-миссия.md` (7 проблем)](#docs02-anthropic-vacancies347-твоя-миссияmd-7-проблем)
  - [`docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` (7 проблем)](#docs02-anthropic-vacancies353-что-ты-не-можешь-делать-вообщеmd-7-проблем)
  - [`docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` (7 проблем)](#docs02-anthropic-vacancies357-твоя-коммуникация-в-outreachmd-7-проблем)
  - [`docs/02-anthropic-vacancies/63-history.md` (7 проблем)](#docs02-anthropic-vacancies63-historymd-7-проблем)
  - [`docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` (7 проблем)](#docs02-anthropic-vacancies70-зачем-две-версии-параллельноmd-7-проблем)
  - [`docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` (7 проблем)](#docs02-anthropic-vacancies73-portal-protocol-md-v1-1md-7-проблем)
  - [`docs/02-anthropic-vacancies/74-abstract.md` (7 проблем)](#docs02-anthropic-vacancies74-abstractmd-7-проблем)
  - [`docs/05-habr-projects/QA.md` (7 проблем)](#docs05-habr-projectsqamd-7-проблем)
  - [`docs/CHANGELOG.md` (7 проблем)](#docschangelogmd-7-проблем)
  - [`docs/VALIDATION.md` (7 проблем)](#docsvalidationmd-7-проблем)
  - [`docs/contacts/anastasiyaw.md` (7 проблем)](#docscontactsanastasiyawmd-7-проблем)
  - [`docs/contacts/andrey-chuyan.md` (7 проблем)](#docscontactsandrey-chuyanmd-7-проблем)
  - [`docs/contacts/cutcode.md` (7 проблем)](#docscontactscutcodemd-7-проблем)
  - [`docs/contacts/dmitriila.md` (7 проблем)](#docscontactsdmitriilamd-7-проблем)
  - [`docs/contacts/kksudo.md` (7 проблем)](#docscontactskksudomd-7-проблем)
  - [`docs/contacts/mixaill76.md` (7 проблем)](#docscontactsmixaill76md-7-проблем)
  - [`docs/contacts/nlaik.md` (7 проблем)](#docscontactsnlaikmd-7-проблем)
  - [`docs/contacts/sonia-black.md` (7 проблем)](#docscontactssonia-blackmd-7-проблем)
  - [`docs/contacts/spbmolot.md` (7 проблем)](#docscontactsspbmolotmd-7-проблем)
  - [`docs/contacts/tagir-analyzes.md` (7 проблем)](#docscontactstagir-analyzesmd-7-проблем)
  - [`docs/contacts/vitalyoborin.md` (7 проблем)](#docscontactsvitalyoborinmd-7-проблем)
  - [`docs/contacts/vladspace.md` (7 проблем)](#docscontactsvladspacemd-7-проблем)
  - [`docs/contacts/zodigancode.md` (7 проблем)](#docscontactszodigancodemd-7-проблем)
  - [`docs/02-anthropic-vacancies/04-abstract.md` (6 проблем)](#docs02-anthropic-vacancies04-abstractmd-6-проблем)
  - [`docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` (6 проблем)](#docs02-anthropic-vacancies113-6-почему-это-валидный-паттерн-для-ai-assisted-workmd-6-проблем)
  - [`docs/02-anthropic-vacancies/12-content-overview.md` (6 проблем)](#docs02-anthropic-vacancies12-content-overviewmd-6-проблем)
  - [`docs/02-anthropic-vacancies/120-главные-технические-риски.md` (6 проблем)](#docs02-anthropic-vacancies120-главные-технические-рискиmd-6-проблем)
  - [`docs/02-anthropic-vacancies/126-установка.md` (6 проблем)](#docs02-anthropic-vacancies126-установкаmd-6-проблем)
  - [`docs/02-anthropic-vacancies/132-planned-v0-2-0.md` (6 проблем)](#docs02-anthropic-vacancies132-planned-v0-2-0md-6-проблем)
  - [`docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` (6 проблем)](#docs02-anthropic-vacancies134-the-double-triangle-architecture-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` (6 проблем)](#docs02-anthropic-vacancies151-open-knowledge-work-foundation-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/154-table-of-contents.md` (6 проблем)](#docs02-anthropic-vacancies154-table-of-contentsmd-6-проблем)
  - [`docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` (6 проблем)](#docs02-anthropic-vacancies166-representative-agent-layer-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/168-abstract.md` (6 проблем)](#docs02-anthropic-vacancies168-abstractmd-6-проблем)
  - [`docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` (6 проблем)](#docs02-anthropic-vacancies187-слой-представительских-агентов-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/190-содержание.md` (6 проблем)](#docs02-anthropic-vacancies190-содержаниеmd-6-проблем)
  - [`docs/02-anthropic-vacancies/204-ссылки.md` (6 проблем)](#docs02-anthropic-vacancies204-ссылкиmd-6-проблем)
  - [`docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` (6 проблем)](#docs02-anthropic-vacancies208-professional-colleague-agents-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/223-12-closing.md` (6 проблем)](#docs02-anthropic-vacancies223-12-closingmd-6-проблем)
  - [`docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` (6 проблем)](#docs02-anthropic-vacancies226-appendix-a-comparative-table-five-agent-typesmd-6-проблем)
  - [`docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` (6 проблем)](#docs02-anthropic-vacancies241-10-открытые-вопросыmd-6-проблем)
  - [`docs/02-anthropic-vacancies/244-благодарности.md` (6 проблем)](#docs02-anthropic-vacancies244-благодарностиmd-6-проблем)
  - [`docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` (6 проблем)](#docs02-anthropic-vacancies246-приложение-a-сравнительная-таблица-пять-типов-агенmd-6-проблем)
  - [`docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` (6 проблем)](#docs02-anthropic-vacancies249-composite-skills-agent-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/252-abstract.md` (6 проблем)](#docs02-anthropic-vacancies252-abstractmd-6-проблем)
  - [`docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` (6 проблем)](#docs02-anthropic-vacancies269-appendix-a-the-six-type-taxonomy-updatedmd-6-проблем)
  - [`docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` (6 проблем)](#docs02-anthropic-vacancies270-appendix-b-sub-agent-registry-schema-sketchmd-6-проблем)
  - [`docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` (6 проблем)](#docs02-anthropic-vacancies271-appendix-c-configuration-template-examplemd-6-проблем)
  - [`docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` (6 проблем)](#docs02-anthropic-vacancies273-infrastructure-for-ai-collaborative-intellectual-wmd-6-проблем)
  - [`docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` (6 проблем)](#docs02-anthropic-vacancies28-appendix-a-minimal-working-examplemd-6-проблем)
  - [`docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` (6 проблем)](#docs02-anthropic-vacancies298-что-этот-документ-не-решаетmd-6-проблем)
  - [`docs/02-anthropic-vacancies/300-заключение.md` (6 проблем)](#docs02-anthropic-vacancies300-заключениеmd-6-проблем)
  - [`docs/02-anthropic-vacancies/301-благодарности.md` (6 проблем)](#docs02-anthropic-vacancies301-благодарностиmd-6-проблем)
  - [`docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` (6 проблем)](#docs02-anthropic-vacancies304-ingit-as-cowork-native-workspace-substrate-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` (6 проблем)](#docs02-anthropic-vacancies305-a-practical-path-to-layer-b-through-symbiotic-intemd-6-проблем)
  - [`docs/02-anthropic-vacancies/307-abstract.md` (6 проблем)](#docs02-anthropic-vacancies307-abstractmd-6-проблем)
  - [`docs/02-anthropic-vacancies/31-content-overview.md` (6 проблем)](#docs02-anthropic-vacancies31-content-overviewmd-6-проблем)
  - [`docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` (6 проблем)](#docs02-anthropic-vacancies322-appendix-b-comparison-matrixmd-6-проблем)
  - [`docs/02-anthropic-vacancies/325-аннотация.md` (6 проблем)](#docs02-anthropic-vacancies325-аннотацияmd-6-проблем)
  - [`docs/02-anthropic-vacancies/326-содержание.md` (6 проблем)](#docs02-anthropic-vacancies326-содержаниеmd-6-проблем)
  - [`docs/02-anthropic-vacancies/35-passports-info1-md.md` (6 проблем)](#docs02-anthropic-vacancies35-passports-info1-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` (6 проблем)](#docs02-anthropic-vacancies358-твоя-relationship-с-другими-aimd-6-проблем)
  - [`docs/02-anthropic-vacancies/36-essence.md` (6 проблем)](#docs02-anthropic-vacancies36-essencemd-6-проблем)
  - [`docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` (6 проблем)](#docs02-anthropic-vacancies360-что-ты-всегда-делаешьmd-6-проблем)
  - [`docs/02-anthropic-vacancies/39-angle-perspective.md` (6 проблем)](#docs02-anthropic-vacancies39-angle-perspectivemd-6-проблем)
  - [`docs/02-anthropic-vacancies/45-passports-pro2-md.md` (6 проблем)](#docs02-anthropic-vacancies45-passports-pro2-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/46-essence.md` (6 проблем)](#docs02-anthropic-vacancies46-essencemd-6-проблем)
  - [`docs/02-anthropic-vacancies/47-native-format.md` (6 проблем)](#docs02-anthropic-vacancies47-native-formatmd-6-проблем)
  - [`docs/02-anthropic-vacancies/49-angle-perspective.md` (6 проблем)](#docs02-anthropic-vacancies49-angle-perspectivemd-6-проблем)
  - [`docs/02-anthropic-vacancies/55-passports-meta-md.md` (6 проблем)](#docs02-anthropic-vacancies55-passports-meta-mdmd-6-проблем)
  - [`docs/02-anthropic-vacancies/58-content-overview.md` (6 проблем)](#docs02-anthropic-vacancies58-content-overviewmd-6-проблем)
  - [`docs/02-anthropic-vacancies/59-angle-perspective.md` (6 проблем)](#docs02-anthropic-vacancies59-angle-perspectivemd-6-проблем)
  - [`docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` (6 проблем)](#docs02-anthropic-vacancies89-14-sdk-contract-informativemd-6-проблем)
  - [`docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` (6 проблем)](#docs02-anthropic-vacancies98-appendix-a-minimal-working-examplemd-6-проблем)
  - [`docs/CONCEPT_GRAPH.md` (6 проблем)](#docsconcept_graphmd-6-проблем)
  - [`docs/DUPLICATES.md` (6 проблем)](#docsduplicatesmd-6-проблем)
  - [`docs/HEATMAP.md` (6 проблем)](#docsheatmapmd-6-проблем)
  - [`docs/VOCABULARY.md` (6 проблем)](#docsvocabularymd-6-проблем)
  - [`docs/templates/project-component.md` (6 проблем)](#docstemplatesproject-componentmd-6-проблем)
  - [`docs/templates/research-note.md` (6 проблем)](#docstemplatesresearch-notemd-6-проблем)
  - [`docs/02-anthropic-vacancies/102-доступ-к-данным.md` (5 проблем)](#docs02-anthropic-vacancies102-доступ-к-даннымmd-5-проблем)
  - [`docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` (5 проблем)](#docs02-anthropic-vacancies118-appendix-a-шаблон-для-header-warningmd-5-проблем)
  - [`docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` (5 проблем)](#docs02-anthropic-vacancies121-appendix-c-история-изменений-методологииmd-5-проблем)
  - [`docs/02-anthropic-vacancies/13-angle-perspective.md` (5 проблем)](#docs02-anthropic-vacancies13-angle-perspectivemd-5-проблем)
  - [`docs/02-anthropic-vacancies/16-history.md` (5 проблем)](#docs02-anthropic-vacancies16-historymd-5-проблем)
  - [`docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` (5 проблем)](#docs02-anthropic-vacancies242-11-призыв-к-сотрудничествуmd-5-проблем)
  - [`docs/02-anthropic-vacancies/243-12-заключение.md` (5 проблем)](#docs02-anthropic-vacancies243-12-заключениеmd-5-проблем)
  - [`docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` (5 проблем)](#docs02-anthropic-vacancies339-приложение-a-дерево-решений-для-принимающих-ingitmd-5-проблем)
  - [`docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` (5 проблем)](#docs02-anthropic-vacancies344-системный-промпт-для-lorenzo-projectmd-5-проблем)
  - [`docs/02-anthropic-vacancies/345-кто-ты.md` (5 проблем)](#docs02-anthropic-vacancies345-кто-тыmd-5-проблем)
  - [`docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` (5 проблем)](#docs02-anthropic-vacancies350-твои-языки-и-культурные-nuancesmd-5-проблем)
  - [`docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` (5 проблем)](#docs02-anthropic-vacancies352-что-ты-не-можешь-делать-без-max-approvalmd-5-проблем)
  - [`docs/02-anthropic-vacancies/359-твои-anti-patterns.md` (5 проблем)](#docs02-anthropic-vacancies359-твои-anti-patternsmd-5-проблем)
  - [`docs/03-technology-combinations/04-sozialrecht-domain.md` (5 проблем)](#docs03-technology-combinations04-sozialrecht-domainmd-5-проблем)
  - [`docs/05-habr-projects/01-synthesis.md` (5 проблем)](#docs05-habr-projects01-synthesismd-5-проблем)
  - [`docs/05-habr-projects/knowledge/wikontic.md` (5 проблем)](#docs05-habr-projectsknowledgewikonticmd-5-проблем)
  - [`docs/BROKEN_LINKS.md` (5 проблем)](#docsbroken_linksmd-5-проблем)
  - [`docs/FAQ.md` (5 проблем)](#docsfaqmd-5-проблем)
  - [`docs/HEALTH.md` (5 проблем)](#docshealthmd-5-проблем)
  - [`docs/MISSING.md` (5 проблем)](#docsmissingmd-5-проблем)
  - [`docs/NETWORK.md` (5 проблем)](#docsnetworkmd-5-проблем)
  - [`docs/READING_ORDER.md` (5 проблем)](#docsreading_ordermd-5-проблем)
  - [`docs/READING_TIME.md` (5 проблем)](#docsreading_timemd-5-проблем)
  - [`docs/REPORT.md` (5 проблем)](#docsreportmd-5-проблем)
  - [`docs/WORD_FREQ.md` (5 проблем)](#docsword_freqmd-5-проблем)
  - [`docs/autofilled/components/.md` (5 проблем)](#docsautofilledcomponentsmd-5-проблем)
  - [`docs/autofilled/components/cowork.md` (5 проблем)](#docsautofilledcomponentscoworkmd-5-проблем)
  - [`docs/autofilled/components/ingit.md` (5 проблем)](#docsautofilledcomponentsingitmd-5-проблем)
  - [`docs/autofilled/components/lorenzo.md` (5 проблем)](#docsautofilledcomponentslorenzomd-5-проблем)
  - [`docs/autofilled/components/nautilus.md` (5 проблем)](#docsautofilledcomponentsnautilusmd-5-проблем)
  - [`docs/autofilled/components/sgb.md` (5 проблем)](#docsautofilledcomponentssgbmd-5-проблем)
  - [`docs/autofilled/components/svend4.md` (5 проблем)](#docsautofilledcomponentssvend4md-5-проблем)
  - [`docs/autofilled/components/svyazi.md` (5 проблем)](#docsautofilledcomponentssvyazimd-5-проблем)
  - [`docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` (4 проблем)](#docs02-anthropic-vacancies201-11-призыв-к-сотрудничествуmd-4-проблем)
  - [`docs/02-anthropic-vacancies/202-12-заключение.md` (4 проблем)](#docs02-anthropic-vacancies202-12-заключениеmd-4-проблем)
  - [`docs/02-anthropic-vacancies/203-благодарности.md` (4 проблем)](#docs02-anthropic-vacancies203-благодарностиmd-4-проблем)
  - [`docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` (4 проблем)](#docs02-anthropic-vacancies206-приложение-b-матрица-сравнения-областейmd-4-проблем)
  - [`docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` (4 проблем)](#docs02-anthropic-vacancies297-что-промышленность-вероятно-построитmd-4-проблем)
  - [`docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` (4 проблем)](#docs02-anthropic-vacancies362-когда-сомневаешься-escalate-к-maxmd-4-проблем)
  - [`docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` (4 проблем)](#docs02-anthropic-vacancies363-твоя-identity-как-persistent-charactermd-4-проблем)
  - [`docs/DENSITY.md` (4 проблем)](#docsdensitymd-4-проблем)
  - [`docs/KPI_HISTORY.md` (4 проблем)](#docskpi_historymd-4-проблем)
  - [`docs/ORPHANS.md` (4 проблем)](#docsorphansmd-4-проблем)
  - [`docs/PROGRESS.md` (4 проблем)](#docsprogressmd-4-проблем)
  - [`docs/VERSION_DIFF.md` (4 проблем)](#docsversion_diffmd-4-проблем)
  - [`docs/WORD_CLOUD.md` (4 проблем)](#docsword_cloudmd-4-проблем)
  - [`docs/autofilled/components/kksudo.md` (4 проблем)](#docsautofilledcomponentskksudomd-4-проблем)
  - [`docs/autofilled/components/spbmolot.md` (4 проблем)](#docsautofilledcomponentsspbmolotmd-4-проблем)
  - [`docs/templates/decision-record.md` (4 проблем)](#docstemplatesdecision-recordmd-4-проблем)
  - [`docs/templates/ensemble.md` (4 проблем)](#docstemplatesensemblemd-4-проблем)
  - [`docs/01-svyazi/README.md` (3 проблем)](#docs01-svyazireadmemd-3-проблем)
  - [`docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` (3 проблем)](#docs02-anthropic-vacancies185-appendix-b-domain-comparison-matrixmd-3-проблем)
  - [`docs/02-anthropic-vacancies/189-аннотация.md` (3 проблем)](#docs02-anthropic-vacancies189-аннотацияmd-3-проблем)
  - [`docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` (3 проблем)](#docs02-anthropic-vacancies348-кому-ты-служишь-слоистая-модельmd-3-проблем)
  - [`docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` (3 проблем)](#docs02-anthropic-vacancies361-когда-ты-honestly-не-знаешьmd-3-проблем)
  - [`docs/05-habr-projects/README.md` (3 проблем)](#docs05-habr-projectsreadmemd-3-проблем)
  - [`docs/ABBREVIATIONS.md` (3 проблем)](#docsabbreviationsmd-3-проблем)
  - [`docs/COMPARE.md` (3 проблем)](#docscomparemd-3-проблем)
  - [`docs/COST.md` (3 проблем)](#docscostmd-3-проблем)
  - [`docs/CROSSREFS.md` (3 проблем)](#docscrossrefsmd-3-проблем)
  - [`docs/DIGEST_WEEKLY.md` (3 проблем)](#docsdigest_weeklymd-3-проблем)
  - [`docs/KPI.md` (3 проблем)](#docskpimd-3-проблем)
  - [`docs/METRICS.md` (3 проблем)](#docsmetricsmd-3-проблем)
  - [`docs/PRIORITIES.md` (3 проблем)](#docsprioritiesmd-3-проблем)
  - [`docs/PRIORITIES.md` (3 проблем)](#docsprioritiesmd-3-проблем)
  - [`docs/SCHEDULE.md` (3 проблем)](#docsschedulemd-3-проблем)
  - [`docs/SEE_ALSO.md` (3 проблем)](#docssee_alsomd-3-проблем)
  - [`docs/templates/contact-outreach.md` (3 проблем)](#docstemplatescontact-outreachmd-3-проблем)
  - [`docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` (2 проблем)](#docs02-anthropic-vacancies340-приложение-b-сравнительная-матрицаmd-2-проблем)
  - [`docs/02-anthropic-vacancies/346-твоё-происхождение.md` (2 проблем)](#docs02-anthropic-vacancies346-твоё-происхождениеmd-2-проблем)
  - [`docs/02-anthropic-vacancies/README.md` (2 проблем)](#docs02-anthropic-vacanciesreadmemd-2-проблем)
  - [`docs/04-ai-collaborations/README.md` (2 проблем)](#docs04-ai-collaborationsreadmemd-2-проблем)
  - [`docs/ALERTS.md` (2 проблем)](#docsalertsmd-2-проблем)
  - [`docs/AUTHORS.md` (2 проблем)](#docsauthorsmd-2-проблем)
  - [`docs/COMPLEXITY.md` (2 проблем)](#docscomplexitymd-2-проблем)
  - [`docs/CONTACT_PRIORITY.md` (2 проблем)](#docscontact_prioritymd-2-проблем)
  - [`docs/FOOTNOTES.md` (2 проблем)](#docsfootnotesmd-2-проблем)
  - [`docs/FOOTNOTES.md` (2 проблем)](#docsfootnotesmd-2-проблем)
  - [`docs/GLOSSARY.md` (2 проблем)](#docsglossarymd-2-проблем)
  - [`docs/GRAPH.md` (2 проблем)](#docsgraphmd-2-проблем)
  - [`docs/LINKS.md` (2 проблем)](#docslinksmd-2-проблем)
  - [`docs/README.md` (2 проблем)](#docsreadmemd-2-проблем)
  - [`docs/SCORING.md` (2 проблем)](#docsscoringmd-2-проблем)
  - [`docs/SOURCE_MAP.md` (2 проблем)](#docssource_mapmd-2-проблем)
  - [`docs/STALENESS.md` (2 проблем)](#docsstalenessmd-2-проблем)
  - [`docs/STATS.md` (2 проблем)](#docsstatsmd-2-проблем)
  - [`docs/badges/README.md` (2 проблем)](#docsbadgesreadmemd-2-проблем)
  - [`docs/03-technology-combinations/README.md` (1 проблем)](#docs03-technology-combinationsreadmemd-1-проблем)
  - [`docs/05-habr-projects/memory/README.md` (1 проблем)](#docs05-habr-projectsmemoryreadmemd-1-проблем)
  - [`docs/02-anthropic-vacancies/README.md` (1 проблем)](#docs02-anthropic-vacanciesreadmemd-1-проблем)
  - [`docs/03-technology-combinations/README.md` (1 проблем)](#docs03-technology-combinationsreadmemd-1-проблем)
  - [`docs/04-ai-collaborations/README.md` (1 проблем)](#docs04-ai-collaborationsreadmemd-1-проблем)
  - [`docs/05-habr-projects/memory/README.md` (1 проблем)](#docs05-habr-projectsmemoryreadmemd-1-проблем)
  - [`docs/BACKLINKS.md` (1 проблем)](#docsbacklinksmd-1-проблем)
  - [`docs/DEPENDABOT.md` (1 проблем)](#docsdependabotmd-1-проблем)
  - [`docs/ENTITIES.md` (1 проблем)](#docsentitiesmd-1-проблем)
  - [`docs/MINDMAP.md` (1 проблем)](#docsmindmapmd-1-проблем)
  - [`docs/SENTIMENT.md` (1 проблем)](#docssentimentmd-1-проблем)
  - [`docs/autofilled/components/README.md` (1 проблем)](#docsautofilledcomponentsreadmemd-1-проблем)
  - [`docs/contacts/README.md` (1 проблем)](#docscontactsreadmemd-1-проблем)
  - [`docs/templates/README.md` (1 проблем)](#docstemplatesreadmemd-1-проблем)

---

<!-- tags: memory, orchestration, security, ingestion, local-first, architecture, roadmap, anthropic, self-improvement, collaboration -->




_Обновлено: 2026-04-29_

Файлов с проблемами: **518**

## Типы проблем

| Тип | Кол-во |
|-----|--------|
| ⚪ Короткий абзац | 4792 |
| ✂️  Оборванный | 2856 |
| 📏 Длинное предложение | 178 |
| 🔁 Повтор начала | 1248 |
| ♊ Дубль | 138 |

## По файлам

### `docs/CONCEPTS.md` (1443 проблем)

_абзац: 700, Оборванный: 534, начала: 205, Дубль: 4_


### `docs/TABLES.md` (553 проблем)

_абзац: 264, начала: 257, Дубль: 28, Оборванный: 4_


### `docs/CODE_BLOCKS.md` (170 проблем)

_абзац: 86, начала: 81, Дубль: 3_


### `docs/QUESTIONS.md` (138 проблем)

_абзац: 58, Оборванный: 65, Дубль: 9, начала: 6_


### `docs/QA.md` (127 проблем)

_абзац: 66, начала: 57, Оборванный: 3, Дубль: 1_


### `docs/CONTRADICTIONS.md` (126 проблем)

_абзац: 68, Оборванный: 36, Дубль: 22_


### `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` (92 проблем)

_абзац: 15, Оборванный: 40, предложение: 37_


### `docs/CLUSTERS.md` (76 проблем)

_абзац: 11, Оборванный: 34, предложение: 1, начала: 30_


### `docs/DECISIONS.md` (71 проблем)

_абзац: 5, Оборванный: 59, начала: 7_


### `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` (67 проблем)

_абзац: 17, Оборванный: 30, предложение: 7, начала: 13_


### `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` (65 проблем)

_Оборванный: 28, предложение: 21, абзац: 10, начала: 6_


### `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` (55 проблем)

_абзац: 17, Оборванный: 20, предложение: 18_


### `docs/GITHUB_ISSUES.md` (55 проблем)

_абзац: 6, Оборванный: 21, предложение: 1, начала: 13, Дубль: 14_


### `docs/02-anthropic-vacancies/QA.md` (47 проблем)

_абзац: 23, начала: 23, Оборванный: 1_


### `docs/04-ai-collaborations/00-intro.md` (46 проблем)

_абзац: 30, Оборванный: 11, предложение: 5_


### `docs/CONTENT_GAPS.md` (46 проблем)

_абзац: 23, Оборванный: 20, Дубль: 3_


### `docs/02-anthropic-vacancies/218-7-application-domains.md` (44 проблем)

_абзац: 40, Оборванный: 4_


### `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` (44 проблем)

_абзац: 16, Оборванный: 19, начала: 9_


### `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` (43 проблем)

_абзац: 12, Оборванный: 3, начала: 28_


### `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` (42 проблем)

_абзац: 13, Оборванный: 1, начала: 28_


### `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` (40 проблем)

_абзац: 33, Оборванный: 4, начала: 3_


### `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` (40 проблем)

_абзац: 15, Оборванный: 16, начала: 9_


### `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` (38 проблем)

_абзац: 27, Оборванный: 11_


### `docs/02-anthropic-vacancies/165-closing.md` (38 проблем)

_абзац: 10, Оборванный: 9, предложение: 8, начала: 11_


### `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` (37 проблем)

_абзац: 33, Оборванный: 4_


### `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` (37 проблем)

_абзац: 34, Оборванный: 3_


### `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` (36 проблем)

_абзац: 13, Оборванный: 23_


### `docs/02-anthropic-vacancies/238-7-области-применения.md` (36 проблем)

_абзац: 34, Оборванный: 2_


### `docs/05-habr-projects/memory/memnet.md` (36 проблем)

_Оборванный: 7, абзац: 13, предложение: 6, начала: 10_


### `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` (35 проблем)

_Оборванный: 4, абзац: 31_


### `docs/02-anthropic-vacancies/69-section.md` (34 проблем)

_абзац: 20, Оборванный: 13, предложение: 1_


### `docs/01-svyazi/04-ensembles-overview.md` (33 проблем)

_абзац: 20, Оборванный: 13_


### `docs/01-svyazi/QA.md` (32 проблем)

_абзац: 16, начала: 15, Оборванный: 1_


### `docs/04-ai-collaborations/QA.md` (32 проблем)

_абзац: 16, начала: 15, Оборванный: 1_


### `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` (31 проблем)

_абзац: 15, Оборванный: 10, предложение: 3, начала: 3_


### `docs/SPELLCHECK.md` (31 проблем)

_абзац: 17, начала: 14_


### `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` (30 проблем)

_абзац: 9, Оборванный: 4, начала: 17_


### `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` (30 проблем)

_абзац: 6, Оборванный: 18, предложение: 6_


### `docs/02-anthropic-vacancies/68-about.md` (30 проблем)

_абзац: 19, Оборванный: 11_


### `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` (29 проблем)

_абзац: 20, Оборванный: 9_


### `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` (29 проблем)

_абзац: 18, Оборванный: 11_


### `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` (28 проблем)

_абзац: 6, Оборванный: 12, предложение: 10_


### `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` (28 проблем)

_Оборванный: 15, Дубль: 1, абзац: 4, начала: 8_


### `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` (28 проблем)

_абзац: 14, Оборванный: 9, Дубль: 1, предложение: 4_


### `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` (28 проблем)

_Оборванный: 10, Дубль: 1, начала: 3, абзац: 14_


### `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` (28 проблем)

_абзац: 18, Оборванный: 10_


### `docs/02-anthropic-vacancies/67-о-проекте.md` (28 проблем)

_абзац: 18, Оборванный: 10_


### `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` (28 проблем)

_абзац: 17, Оборванный: 10, предложение: 1_


### `docs/RISK_REGISTER.md` (28 проблем)

_абзац: 24, Оборванный: 3, Дубль: 1_


### `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` (27 проблем)

_абзац: 16, Оборванный: 11_


### `docs/02-anthropic-vacancies/133-обратная-связь.md` (26 проблем)

_абзац: 10, Дубль: 1, Оборванный: 9, предложение: 6_


### `docs/02-anthropic-vacancies/159-5-economic-model.md` (26 проблем)

_Оборванный: 11, абзац: 7, начала: 8_


### `docs/02-anthropic-vacancies/162-8-risk-analysis.md` (26 проблем)

_абзац: 11, Оборванный: 15_


### `docs/02-anthropic-vacancies/164-10-appendices.md` (26 проблем)

_абзац: 11, Оборванный: 10, начала: 5_


### `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` (26 проблем)

_абзац: 15, Оборванный: 8, предложение: 3_


### `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` (26 проблем)

_абзац: 19, Оборванный: 7_


### `docs/TAGS.md` (26 проблем)

_абзац: 2, Оборванный: 12, начала: 12_


### `docs/02-anthropic-vacancies/00-intro.md` (25 проблем)

_абзац: 8, Оборванный: 12, Дубль: 1, предложение: 4_


### `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` (25 проблем)

_Оборванный: 9, Дубль: 1, абзац: 8, начала: 7_


### `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` (25 проблем)

_абзац: 7, Оборванный: 3, начала: 15_


### `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` (25 проблем)

_абзац: 15, Оборванный: 8, предложение: 2_


### `docs/01-svyazi/07-mvp-planning.md` (24 проблем)

_абзац: 19, Оборванный: 5_


### `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` (24 проблем)

_абзац: 19, начала: 3, Оборванный: 2_


### `docs/02-anthropic-vacancies/174-5-architectural-specification.md` (24 проблем)

_абзац: 7, Оборванный: 4, начала: 13_


### `docs/02-anthropic-vacancies/179-10-open-questions.md` (24 проблем)

_Оборванный: 3, абзац: 21_


### `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` (24 проблем)

_абзац: 9, Оборванный: 6, начала: 9_


### `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` (24 проблем)

_абзац: 9, Оборванный: 5, начала: 9, Дубль: 1_


### `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` (24 проблем)

_Оборванный: 5, абзац: 10, начала: 9_


### `docs/01-svyazi/01-executive-summary.md` (23 проблем)

_Оборванный: 8, Дубль: 1, абзац: 14_


### `docs/02-anthropic-vacancies/156-2-target-populations.md` (23 проблем)

_абзац: 8, Оборванный: 15_


### `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` (23 проблем)

_Оборванный: 12, Дубль: 1, абзац: 10_


### `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` (23 проблем)

_абзац: 7, Оборванный: 3, начала: 13_


### `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` (23 проблем)

_абзац: 6, Оборванный: 13, Дубль: 1, предложение: 3_


### `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` (23 проблем)

_Оборванный: 10, Дубль: 1, абзац: 9, начала: 3_


### `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` (23 проблем)

_абзац: 14, Оборванный: 9_


### `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` (23 проблем)

_абзац: 13, Оборванный: 7, предложение: 3_


### `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` (23 проблем)

_абзац: 11, Оборванный: 12_


### `docs/TOPIC_MODEL.md` (23 проблем)

_абзац: 10, Оборванный: 13_


### `docs/01-svyazi/10-second-order-ensembles.md` (22 проблем)

_абзац: 13, Оборванный: 9_


### `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` (22 проблем)

_абзац: 6, Оборванный: 10, предложение: 1, начала: 5_


### `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` (22 проблем)

_Оборванный: 15, Дубль: 1, абзац: 6_


### `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` (22 проблем)

_Оборванный: 1, абзац: 20, Дубль: 1_


### `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` (22 проблем)

_абзац: 12, Оборванный: 9, предложение: 1_


### `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` (22 проблем)

_абзац: 10, начала: 7, Оборванный: 5_


### `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` (22 проблем)

_абзац: 9, Оборванный: 5, начала: 8_


### `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` (22 проблем)

_абзац: 8, Оборванный: 10, предложение: 4_


### `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` (22 проблем)

_Оборванный: 9, абзац: 13_


### `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` (22 проблем)

_абзац: 12, Оборванный: 10_


### `docs/01-svyazi/13-contacts.md` (21 проблем)

_абзац: 11, Оборванный: 10_


### `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` (21 проблем)

_Оборванный: 8, абзац: 10, начала: 3_


### `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` (21 проблем)

_абзац: 10, Оборванный: 5, начала: 6_


### `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` (21 проблем)

_абзац: 7, Оборванный: 3, начала: 11_


### `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` (21 проблем)

_абзац: 8, Оборванный: 5, начала: 8_


### `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` (21 проблем)

_абзац: 10, Оборванный: 6, начала: 5_


### `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` (21 проблем)

_абзац: 11, Оборванный: 7, начала: 3_


### `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` (21 проблем)

_абзац: 11, Оборванный: 10_


### `docs/04-ai-collaborations/01-executive-summary.md` (21 проблем)

_абзац: 14, Оборванный: 7_


### `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` (21 проблем)

_абзац: 13, Оборванный: 8_


### `docs/CITATION_INDEX.md` (21 проблем)

_абзац: 21_


### `docs/01-svyazi/09-architectural-gaps.md` (20 проблем)

_абзац: 14, Оборванный: 6_


### `docs/01-svyazi/11-integration-contracts.md` (20 проблем)

_абзац: 13, Оборванный: 7_


### `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` (20 проблем)

_абзац: 13, Оборванный: 7_


### `docs/02-anthropic-vacancies/175-6-ethical-framework.md` (20 проблем)

_Оборванный: 9, Дубль: 1, абзац: 10_


### `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` (20 проблем)

_Оборванный: 6, абзац: 14_


### `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` (20 проблем)

_Оборванный: 10, Дубль: 1, абзац: 9_


### `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` (20 проблем)

_Оборванный: 13, Дубль: 1, абзац: 6_


### `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` (20 проблем)

_Оборванный: 4, Дубль: 1, абзац: 10, начала: 5_


### `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` (20 проблем)

_абзац: 10, Оборванный: 6, предложение: 4_


### `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` (20 проблем)

_абзац: 12, Оборванный: 8_


### `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` (20 проблем)

_абзац: 12, Оборванный: 8_


### `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` (20 проблем)

_Оборванный: 3, абзац: 8, начала: 9_


### `docs/02-anthropic-vacancies/90-15-security-considerations.md` (20 проблем)

_Оборванный: 7, абзац: 12, Дубль: 1_


### `docs/01-svyazi/06-security-privacy.md` (19 проблем)

_абзац: 12, Оборванный: 7_


### `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` (19 проблем)

_абзац: 10, Оборванный: 9_


### `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` (19 проблем)

_абзац: 8, Оборванный: 3, начала: 8_


### `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` (19 проблем)

_абзац: 8, Оборванный: 2, начала: 8, Дубль: 1_


### `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` (19 проблем)

_абзац: 8, Оборванный: 3, начала: 8_


### `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` (19 проблем)

_абзац: 9, Оборванный: 10_


### `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` (19 проблем)

_Оборванный: 4, Дубль: 1, абзац: 11, начала: 3_


### `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` (19 проблем)

_абзац: 12, Оборванный: 7_


### `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` (19 проблем)

_Оборванный: 6, абзац: 12, Дубль: 1_


### `docs/04-ai-collaborations/07-выводы.md` (19 проблем)

_абзац: 13, Оборванный: 6_


### `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` (19 проблем)

_абзац: 10, Оборванный: 9_


### `docs/INDEX.md` (19 проблем)

_абзац: 15, Оборванный: 3, Дубль: 1_


### `docs/01-svyazi/12-roadmap.md` (18 проблем)

_абзац: 10, Оборванный: 8_


### `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` (18 проблем)

_абзац: 12, Оборванный: 6_


### `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` (18 проблем)

_абзац: 4, Оборванный: 14_


### `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` (18 проблем)

_абзац: 7, Оборванный: 5, начала: 5, предложение: 1_


### `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` (18 проблем)

_абзац: 10, Оборванный: 3, начала: 5_


### `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` (18 проблем)

_абзац: 6, Оборванный: 7, начала: 5_


### `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` (18 проблем)

_абзац: 8, Оборванный: 6, начала: 4_


### `docs/02-anthropic-vacancies/279-existing-approximations.md` (18 проблем)

_Оборванный: 10, Дубль: 1, абзац: 7_


### `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` (18 проблем)

_Оборванный: 7, Дубль: 1, абзац: 10_


### `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` (18 проблем)

_абзац: 10, Оборванный: 8_


### `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` (18 проблем)

_Оборванный: 7, абзац: 11_


### `docs/CONSISTENCY.md` (18 проблем)

_абзац: 8, начала: 10_


### `docs/NARRATIVE.md` (18 проблем)

_абзац: 4, Оборванный: 12, предложение: 2_


### `docs/ONBOARDING.md` (18 проблем)

_абзац: 10, Оборванный: 7, Дубль: 1_


### `docs/01-svyazi/14-limitations.md` (17 проблем)

_абзац: 8, Оборванный: 9_


### `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` (17 проблем)

_Оборванный: 4, абзац: 13_


### `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` (17 проблем)

_абзац: 8, Оборванный: 6, начала: 3_


### `docs/02-anthropic-vacancies/294-существующие-приближения.md` (17 проблем)

_Оборванный: 9, Дубль: 1, абзац: 7_


### `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` (17 проблем)

_Оборванный: 5, начала: 6, абзац: 6_


### `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` (17 проблем)

_Оборванный: 3, абзац: 11, начала: 3_


### `docs/SITEMAP.md` (17 проблем)

_Оборванный: 1, абзац: 8, начала: 8_


### `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` (16 проблем)

_абзац: 9, Оборванный: 7_


### `docs/02-anthropic-vacancies/144-7-open-questions.md` (16 проблем)

_абзац: 11, Оборванный: 5_


### `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` (16 проблем)

_Дубль: 1, Оборванный: 5, абзац: 10_


### `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` (16 проблем)

_абзац: 6, Оборванный: 2, начала: 8_


### `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` (16 проблем)

_абзац: 6, Оборванный: 5, начала: 5_


### `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` (16 проблем)

_абзац: 8, Оборванный: 8_


### `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` (16 проблем)

_абзац: 5, Оборванный: 11_


### `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` (16 проблем)

_абзац: 5, начала: 8, Оборванный: 3_


### `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` (16 проблем)

_Оборванный: 7, Дубль: 2, абзац: 7_


### `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` (16 проблем)

_Оборванный: 6, Дубль: 1, абзац: 9_


### `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` (16 проблем)

_Оборванный: 2, Дубль: 1, абзац: 10, начала: 3_


### `docs/CHANGELOG_AUTO.md` (16 проблем)

_абзац: 8, Дубль: 1, Оборванный: 5, предложение: 2_


### `docs/LLM_SUMMARIES.md` (16 проблем)

_абзац: 15, Оборванный: 1_


### `docs/01-svyazi/03-component-catalog.md` (15 проблем)

_абзац: 12, Оборванный: 3_


### `docs/01-svyazi/08-conclusions.md` (15 проблем)

_Оборванный: 5, абзац: 10_


### `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` (15 проблем)

_абзац: 9, начала: 5, Оборванный: 1_


### `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` (15 проблем)

_абзац: 10, Оборванный: 5_


### `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` (15 проблем)

_абзац: 5, начала: 8, Оборванный: 2_


### `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` (15 проблем)

_абзац: 10, Оборванный: 5_


### `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` (15 проблем)

_абзац: 6, начала: 8, Оборванный: 1_


### `docs/02-anthropic-vacancies/356-твой-workflow.md` (15 проблем)

_абзац: 8, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/92-17-versioning-policy.md` (15 проблем)

_Оборванный: 7, абзац: 8_


### `docs/03-technology-combinations/02-knowledge-graphs.md` (15 проблем)

_абзац: 4, Оборванный: 7, начала: 4_


### `docs/01-svyazi/02-methodology.md` (14 проблем)

_абзац: 11, Оборванный: 3_


### `docs/02-anthropic-vacancies/104-appendix-c-references.md` (14 проблем)

_Оборванный: 7, абзац: 7_


### `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` (14 проблем)

_абзац: 11, Оборванный: 3_


### `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` (14 проблем)

_Оборванный: 6, абзац: 8_


### `docs/02-anthropic-vacancies/122-глоссарий.md` (14 проблем)

_абзац: 7, Оборванный: 4, начала: 3_


### `docs/02-anthropic-vacancies/155-1-problem-statement.md` (14 проблем)

_абзац: 6, Оборванный: 8_


### `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` (14 проблем)

_абзац: 7, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/264-11-open-questions.md` (14 проблем)

_Оборванный: 4, Дубль: 1, абзац: 9_


### `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` (14 проблем)

_Оборванный: 4, Дубль: 1, абзац: 5, начала: 4_


### `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` (14 проблем)

_абзац: 5, Оборванный: 5, начала: 4_


### `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` (14 проблем)

_абзац: 7, Оборванный: 6, Дубль: 1_


### `docs/02-anthropic-vacancies/320-references.md` (14 проблем)

_Оборванный: 4, абзац: 7, начала: 3_


### `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` (14 проблем)

_абзац: 6, Оборванный: 4, начала: 4_


### `docs/02-anthropic-vacancies/338-ссылки.md` (14 проблем)

_Оборванный: 4, абзац: 7, начала: 3_


### `docs/02-anthropic-vacancies/81-6-adapter-interface.md` (14 проблем)

_Оборванный: 5, абзац: 9_


### `docs/02-anthropic-vacancies/85-10-query-flow.md` (14 проблем)

_Оборванный: 6, абзац: 8_


### `docs/TECH_RADAR.md` (14 проблем)

_Оборванный: 4, абзац: 9, Дубль: 1_


### `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` (13 проблем)

_абзац: 10, Оборванный: 3_


### `docs/02-anthropic-vacancies/130-отладка.md` (13 проблем)

_Оборванный: 3, абзац: 10_


### `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` (13 проблем)

_абзац: 5, Оборванный: 5, начала: 3_


### `docs/02-anthropic-vacancies/18-6-adapter-interface.md` (13 проблем)

_Оборванный: 5, абзац: 8_


### `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` (13 проблем)

_Оборванный: 3, абзац: 4, начала: 5, предложение: 1_


### `docs/02-anthropic-vacancies/21-9-query-flow.md` (13 проблем)

_абзац: 8, Оборванный: 5_


### `docs/02-anthropic-vacancies/23-11-security-considerations.md` (13 проблем)

_Оборванный: 4, абзац: 9_


### `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` (13 проблем)

_Оборванный: 6, абзац: 7_


### `docs/02-anthropic-vacancies/302-ссылки.md` (13 проблем)

_Оборванный: 4, начала: 3, абзац: 6_


### `docs/02-anthropic-vacancies/40-bridges.md` (13 проблем)

_абзац: 5, Оборванный: 5, начала: 3_


### `docs/02-anthropic-vacancies/48-content-overview.md` (13 проблем)

_абзац: 7, Оборванный: 6_


### `docs/02-anthropic-vacancies/57-native-format.md` (13 проблем)

_абзац: 8, начала: 3, Оборванный: 2_


### `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` (13 проблем)

_Оборванный: 3, абзац: 10_


### `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` (13 проблем)

_абзац: 7, Оборванный: 6_


### `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` (12 проблем)

_Оборванный: 4, абзац: 8_


### `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` (12 проблем)

_Оборванный: 7, Дубль: 1, абзац: 4_


### `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` (12 проблем)

_Оборванный: 3, абзац: 9_


### `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` (12 проблем)

_Оборванный: 3, абзац: 9_


### `docs/02-anthropic-vacancies/24-12-versioning-policy.md` (12 проблем)

_Оборванный: 6, абзац: 6_


### `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` (12 проблем)

_абзац: 8, Оборванный: 4_


### `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` (12 проблем)

_абзац: 7, Оборванный: 4, предложение: 1_


### `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` (12 проблем)

_абзац: 5, начала: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` (12 проблем)

_абзац: 5, Оборванный: 7_


### `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` (12 проблем)

_абзац: 5, Оборванный: 7_


### `docs/02-anthropic-vacancies/76-1-introduction.md` (12 проблем)

_Оборванный: 6, абзац: 6_


### `docs/02-anthropic-vacancies/07-2-terminology.md` (11 проблем)

_абзац: 9, Оборванный: 2_


### `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` (11 проблем)

_Оборванный: 4, абзац: 7_


### `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` (11 проблем)

_абзац: 8, Оборванный: 3_


### `docs/02-anthropic-vacancies/111-4-условия-применимости.md` (11 проблем)

_Оборванный: 5, абзац: 6_


### `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` (11 проблем)

_Оборванный: 6, абзац: 5_


### `docs/02-anthropic-vacancies/25-13-reference-implementation.md` (11 проблем)

_абзац: 5, начала: 3, Оборванный: 3_


### `docs/02-anthropic-vacancies/266-13-closing.md` (11 проблем)

_абзац: 7, Оборванный: 4_


### `docs/02-anthropic-vacancies/267-acknowledgments.md` (11 проблем)

_абзац: 4, начала: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/268-references.md` (11 проблем)

_Оборванный: 7, абзац: 4_


### `docs/02-anthropic-vacancies/319-acknowledgments.md` (11 проблем)

_абзац: 5, начала: 3, Оборванный: 3_


### `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` (11 проблем)

_абзац: 7, Оборванный: 4_


### `docs/02-anthropic-vacancies/37-native-format.md` (11 проблем)

_абзац: 5, Оборванный: 6_


### `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` (11 проблем)

_абзац: 7, Оборванный: 4_


### `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` (11 проблем)

_абзац: 7, Оборванный: 4_


### `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` (11 проблем)

_Оборванный: 4, абзац: 7_


### `docs/03-technology-combinations/05-benchmarks.md` (11 проблем)

_Оборванный: 7, предложение: 1, абзац: 3_


### `docs/03-technology-combinations/QA.md` (11 проблем)

_абзац: 8, начала: 3_


### `docs/05-habr-projects/02-collaboration-partners.md` (11 проблем)

_Оборванный: 5, Дубль: 1, абзац: 5_


### `docs/DIGEST.md` (11 проблем)

_абзац: 7, Дубль: 1, Оборванный: 3_


### `docs/SIMILAR.md` (11 проблем)

_абзац: 5, Оборванный: 6_


### `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` (10 проблем)

_Оборванный: 1, абзац: 9_


### `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` (10 проблем)

_абзац: 5, Оборванный: 2, начала: 3_


### `docs/02-anthropic-vacancies/145-8-call-to-action.md` (10 проблем)

_абзац: 7, Оборванный: 3_


### `docs/02-anthropic-vacancies/146-acknowledgments.md` (10 проблем)

_абзац: 5, начала: 3, Оборванный: 2_


### `docs/02-anthropic-vacancies/245-ссылки.md` (10 проблем)

_Оборванный: 4, абзац: 6_


### `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` (10 проблем)

_абзац: 7, Оборванный: 3_


### `docs/02-anthropic-vacancies/287-references.md` (10 проблем)

_Оборванный: 6, абзац: 4_


### `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` (10 проблем)

_абзац: 6, Оборванный: 3, Дубль: 1_


### `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` (10 проблем)

_абзац: 8, Дубль: 1, Оборванный: 1_


### `docs/02-anthropic-vacancies/349-твоя-личность.md` (10 проблем)

_абзац: 9, Оборванный: 1_


### `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` (10 проблем)

_абзац: 5, Оборванный: 3, Дубль: 1, предложение: 1_


### `docs/02-anthropic-vacancies/42-author-contact.md` (10 проблем)

_абзац: 7, Оборванный: 3_


### `docs/02-anthropic-vacancies/43-history.md` (10 проблем)

_абзац: 5, Оборванный: 5_


### `docs/02-anthropic-vacancies/56-essence.md` (10 проблем)

_абзац: 6, Оборванный: 4_


### `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` (10 проблем)

_абзац: 6, Оборванный: 4_


### `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` (10 проблем)

_абзац: 5, Оборванный: 4, Дубль: 1_


### `docs/03-technology-combinations/03-local-first.md` (10 проблем)

_абзац: 4, Оборванный: 6_


### `docs/05-habr-projects/memory/yodoca.md` (10 проблем)

_Оборванный: 4, абзац: 6_


### `docs/COMPONENT_MATRIX.md` (10 проблем)

_абзац: 7, Оборванный: 3_


### `docs/DEPENDENCY_MAP.md` (10 проблем)

_абзац: 8, Дубль: 1, Оборванный: 1_


### `docs/autofilled/research-summary.md` (10 проблем)

_абзац: 8, Оборванный: 2_


### `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` (9 проблем)

_абзац: 5, Оборванный: 4_


### `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` (9 проблем)

_Оборванный: 3, абзац: 6_


### `docs/02-anthropic-vacancies/123-portal-mcp-py.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/221-10-open-questions.md` (9 проблем)

_Оборванный: 3, абзац: 6_


### `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` (9 проблем)

_Оборванный: 4, абзац: 5_


### `docs/02-anthropic-vacancies/225-references.md` (9 проблем)

_Оборванный: 4, абзац: 5_


### `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` (9 проблем)

_абзац: 4, Оборванный: 4, Дубль: 1_


### `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` (9 проблем)

_абзац: 5, Оборванный: 4_


### `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` (9 проблем)

_абзац: 4, Оборванный: 5_


### `docs/02-anthropic-vacancies/275-why-this-document-exists.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/281-the-recursive-insight.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/285-closing.md` (9 проблем)

_абзац: 4, начала: 3, Оборванный: 2_


### `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` (9 проблем)

_абзац: 4, начала: 5_


### `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` (9 проблем)

_Оборванный: 3, абзац: 3, начала: 3_


### `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/50-bridges.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/52-author-contact.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/65-readme-md.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/77-2-terminology.md` (9 проблем)

_абзац: 7, Оборванный: 2_


### `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` (9 проблем)

_абзац: 7, Оборванный: 2_


### `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` (9 проблем)

_абзац: 6, Оборванный: 3_


### `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` (9 проблем)

_Оборванный: 4, абзац: 5_


### `docs/05-habr-projects/memory/ngt-memory.md` (9 проблем)

_Оборванный: 3, абзац: 6_


### `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/06-1-introduction.md` (8 проблем)

_абзац: 6, Оборванный: 2_


### `docs/ACTION_ITEMS.md` (8 проблем)

_абзац: 3, Оборванный: 3, предложение: 2_


### `docs/DEPENDENCY_MAP.md` (8 проблем)

_абзац: 7, Оборванный: 1_


### `docs/02-anthropic-vacancies/105-review-methodology-md.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/106-tl-dr.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` (8 проблем)

_Оборванный: 4, абзац: 4_


### `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` (8 проблем)

_абзац: 5, Дубль: 1, Оборванный: 2_


### `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/136-abstract.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/147-references.md` (8 проблем)

_Оборванный: 4, абзац: 4_


### `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/153-executive-summary.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` (8 проблем)

_абзац: 6, Оборванный: 2_


### `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/210-abstract.md` (8 проблем)

_абзац: 4, предложение: 2, Оборванный: 2_


### `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/38-content-overview.md` (8 проблем)

_абзац: 6, Оборванный: 2_


### `docs/02-anthropic-vacancies/41-compatibility-level.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` (8 проблем)

_абзац: 6, Оборванный: 2_


### `docs/02-anthropic-vacancies/51-compatibility-level.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/53-history.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/60-bridges.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/61-compatibility-level.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/62-author-contact.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` (8 проблем)

_абзац: 6, Оборванный: 2_


### `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/93-18-reference-implementation.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/03-technology-combinations/01-agent-routing.md` (8 проблем)

_абзац: 4, Оборванный: 4_


### `docs/ACTION_ITEMS.md` (8 проблем)

_абзац: 3, Оборванный: 3, предложение: 2_


### `docs/AUTOFILLED.md` (8 проблем)

_абзац: 6, Оборванный: 2_


### `docs/KEYWORD_INDEX.md` (8 проблем)

_абзац: 5, Оборванный: 3_


### `docs/contacts/antipozitive.md` (8 проблем)

_Оборванный: 3, абзац: 5_


### `docs/02-anthropic-vacancies/03-portal-protocol-md.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/02-anthropic-vacancies/128-доступные-инструменты.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/137-table-of-contents.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/169-table-of-contents.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/02-anthropic-vacancies/181-12-closing.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/182-acknowledgments.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/183-references.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/211-table-of-contents.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/224-acknowledgments.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/230-аннотация.md` (7 проблем)

_абзац: 4, предложение: 1, Оборванный: 2_


### `docs/02-anthropic-vacancies/231-содержание.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/253-table-of-contents.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/286-acknowledgments.md` (7 проблем)

_абзац: 4, Оборванный: 2, Дубль: 1_


### `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` (7 проблем)

_абзац: 6, Оборванный: 1_


### `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` (7 проблем)

_абзац: 7_


### `docs/02-anthropic-vacancies/308-table-of-contents.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` (7 проблем)

_абзац: 6, Оборванный: 1_


### `docs/02-anthropic-vacancies/337-благодарности.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/347-твоя-миссия.md` (7 проблем)

_абзац: 5, Дубль: 1, Оборванный: 1_


### `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` (7 проблем)

_абзац: 4, начала: 3_


### `docs/02-anthropic-vacancies/63-history.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` (7 проблем)

_абзац: 5, Оборванный: 2_


### `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/02-anthropic-vacancies/74-abstract.md` (7 проблем)

_абзац: 4, Оборванный: 3_


### `docs/05-habr-projects/QA.md` (7 проблем)

_абзац: 7_


### `docs/CHANGELOG.md` (7 проблем)

_Оборванный: 6, предложение: 1_


### `docs/VALIDATION.md` (7 проблем)

_абзац: 3, Оборванный: 4_


### `docs/contacts/anastasiyaw.md` (7 проблем)

_Оборванный: 4, абзац: 3_


### `docs/contacts/andrey-chuyan.md` (7 проблем)

_Оборванный: 4, абзац: 3_


### `docs/contacts/cutcode.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/contacts/dmitriila.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/contacts/kksudo.md` (7 проблем)

_Оборванный: 4, абзац: 3_


### `docs/contacts/mixaill76.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/contacts/nlaik.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/contacts/sonia-black.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/contacts/spbmolot.md` (7 проблем)

_Оборванный: 4, абзац: 3_


### `docs/contacts/tagir-analyzes.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/contacts/vitalyoborin.md` (7 проблем)

_Оборванный: 4, абзац: 3_


### `docs/contacts/vladspace.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/contacts/zodigancode.md` (7 проблем)

_Оборванный: 3, абзац: 4_


### `docs/02-anthropic-vacancies/04-abstract.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` (6 проблем)

_абзац: 6_


### `docs/02-anthropic-vacancies/12-content-overview.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/02-anthropic-vacancies/120-главные-технические-риски.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/126-установка.md` (6 проблем)

_Оборванный: 2, абзац: 4_


### `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/154-table-of-contents.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/168-abstract.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/190-содержание.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/204-ссылки.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/223-12-closing.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` (6 проблем)

_Оборванный: 1, абзац: 5_


### `docs/02-anthropic-vacancies/244-благодарности.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` (6 проблем)

_абзац: 4, Дубль: 1, Оборванный: 1_


### `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/252-abstract.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/02-anthropic-vacancies/300-заключение.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/301-благодарности.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/307-abstract.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/31-content-overview.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/325-аннотация.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/326-содержание.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/35-passports-info1-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/02-anthropic-vacancies/36-essence.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/39-angle-perspective.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/45-passports-pro2-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/46-essence.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/47-native-format.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/02-anthropic-vacancies/49-angle-perspective.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/55-passports-meta-md.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/58-content-overview.md` (6 проблем)

_абзац: 3, Оборванный: 3_


### `docs/02-anthropic-vacancies/59-angle-perspective.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` (6 проблем)

_Оборванный: 2, абзац: 4_


### `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` (6 проблем)

_Оборванный: 3, абзац: 3_


### `docs/CONCEPT_GRAPH.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/DUPLICATES.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/HEATMAP.md` (6 проблем)

_абзац: 4, Оборванный: 2_


### `docs/VOCABULARY.md` (6 проблем)

_абзац: 3, Оборванный: 2, Дубль: 1_


### `docs/templates/project-component.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/templates/research-note.md` (6 проблем)

_абзац: 5, Оборванный: 1_


### `docs/02-anthropic-vacancies/102-доступ-к-данным.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` (5 проблем)

_абзац: 5_


### `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` (5 проблем)

_абзац: 5_


### `docs/02-anthropic-vacancies/13-angle-perspective.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/02-anthropic-vacancies/16-history.md` (5 проблем)

_абзац: 5_


### `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` (5 проблем)

_Оборванный: 2, абзац: 3_


### `docs/02-anthropic-vacancies/243-12-заключение.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` (5 проблем)

_абзац: 5_


### `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/02-anthropic-vacancies/345-кто-ты.md` (5 проблем)

_Оборванный: 2, абзац: 3_


### `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` (5 проблем)

_Оборванный: 4, абзац: 1_


### `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` (5 проблем)

_абзац: 3, Оборванный: 1, предложение: 1_


### `docs/03-technology-combinations/04-sozialrecht-domain.md` (5 проблем)

_Оборванный: 2, абзац: 3_


### `docs/05-habr-projects/01-synthesis.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/05-habr-projects/knowledge/wikontic.md` (5 проблем)

_Оборванный: 3, абзац: 2_


### `docs/BROKEN_LINKS.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/FAQ.md` (5 проблем)

_абзац: 4, Оборванный: 1_


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


### `docs/REPORT.md` (5 проблем)

_абзац: 3, Оборванный: 2_


### `docs/WORD_FREQ.md` (5 проблем)

_абзац: 3, Оборванный: 1, предложение: 1_


### `docs/autofilled/components/.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/autofilled/components/cowork.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/autofilled/components/ingit.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/autofilled/components/lorenzo.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/autofilled/components/nautilus.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/autofilled/components/sgb.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/autofilled/components/svend4.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/autofilled/components/svyazi.md` (5 проблем)

_абзац: 4, Оборванный: 1_


### `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` (4 проблем)

_Оборванный: 1, Дубль: 1, абзац: 2_


### `docs/02-anthropic-vacancies/202-12-заключение.md` (4 проблем)

_Оборванный: 1, абзац: 3_


### `docs/02-anthropic-vacancies/203-благодарности.md` (4 проблем)

_Оборванный: 1, абзац: 3_


### `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` (4 проблем)

_абзац: 4_


### `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` (4 проблем)

_абзац: 3, Оборванный: 1_


### `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` (4 проблем)

_абзац: 3, Оборванный: 1_


### `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` (4 проблем)

_абзац: 2, Оборванный: 2_


### `docs/DENSITY.md` (4 проблем)

_абзац: 4_


### `docs/KPI_HISTORY.md` (4 проблем)

_абзац: 4_


### `docs/ORPHANS.md` (4 проблем)

_абзац: 3, Оборванный: 1_


### `docs/PROGRESS.md` (4 проблем)

_Оборванный: 1, абзац: 3_


### `docs/VERSION_DIFF.md` (4 проблем)

_абзац: 2, Оборванный: 2_


### `docs/WORD_CLOUD.md` (4 проблем)

_абзац: 3, Оборванный: 1_


### `docs/autofilled/components/kksudo.md` (4 проблем)

_абзац: 3, Оборванный: 1_


### `docs/autofilled/components/spbmolot.md` (4 проблем)

_абзац: 3, Оборванный: 1_


### `docs/templates/decision-record.md` (4 проблем)

_абзац: 4_


### `docs/templates/ensemble.md` (4 проблем)

_абзац: 4_


### `docs/01-svyazi/README.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` (3 проблем)

_абзац: 3_


### `docs/02-anthropic-vacancies/189-аннотация.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` (3 проблем)

_абзац: 3_


### `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` (3 проблем)

_абзац: 3_


### `docs/05-habr-projects/README.md` (3 проблем)

_абзац: 2, Оборванный: 1_


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


### `docs/METRICS.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/PRIORITIES.md` (3 проблем)

_абзац: 3_


### `docs/PRIORITIES.md` (3 проблем)

_абзац: 3_


### `docs/SCHEDULE.md` (3 проблем)

_абзац: 2, Оборванный: 1_


### `docs/SEE_ALSO.md` (3 проблем)

_абзац: 1, Оборванный: 1, предложение: 1_


### `docs/templates/contact-outreach.md` (3 проблем)

_Оборванный: 1, абзац: 2_


### `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` (2 проблем)

_абзац: 2_


### `docs/02-anthropic-vacancies/346-твоё-происхождение.md` (2 проблем)

_Оборванный: 1, абзац: 1_


### `docs/02-anthropic-vacancies/README.md` (2 проблем)

_Оборванный: 1, абзац: 1_


### `docs/04-ai-collaborations/README.md` (2 проблем)

_абзац: 2_


### `docs/ALERTS.md` (2 проблем)

_абзац: 2_


### `docs/AUTHORS.md` (2 проблем)

_абзац: 2_


### `docs/COMPLEXITY.md` (2 проблем)

_Оборванный: 1, абзац: 1_


### `docs/CONTACT_PRIORITY.md` (2 проблем)

_Оборванный: 1, абзац: 1_


### `docs/FOOTNOTES.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/FOOTNOTES.md` (2 проблем)

_абзац: 2_


### `docs/GLOSSARY.md` (2 проблем)

_абзац: 2_


### `docs/GRAPH.md` (2 проблем)

_абзац: 2_


### `docs/LINKS.md` (2 проблем)

_абзац: 2_


### `docs/README.md` (2 проблем)

_Оборванный: 2_


### `docs/SCORING.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/SOURCE_MAP.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/STALENESS.md` (2 проблем)

_абзац: 2_


### `docs/STATS.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/badges/README.md` (2 проблем)

_абзац: 1, Оборванный: 1_


### `docs/03-technology-combinations/README.md` (1 проблем)

_Оборванный: 1_


### `docs/05-habr-projects/memory/README.md` (1 проблем)

_абзац: 1_


### `docs/02-anthropic-vacancies/README.md` (1 проблем)

_Оборванный: 1_


### `docs/03-technology-combinations/README.md` (1 проблем)

_Оборванный: 1_


### `docs/04-ai-collaborations/README.md` (1 проблем)

_Оборванный: 1_


### `docs/05-habr-projects/memory/README.md` (1 проблем)

_абзац: 1_


### `docs/BACKLINKS.md` (1 проблем)

_абзац: 1_


### `docs/DEPENDABOT.md` (1 проблем)

_абзац: 1_


### `docs/ENTITIES.md` (1 проблем)

_абзац: 1_


### `docs/MINDMAP.md` (1 проблем)

_абзац: 1_


### `docs/SENTIMENT.md` (1 проблем)

_абзац: 1_


### `docs/autofilled/components/README.md` (1 проблем)

_Оборванный: 1_


### `docs/contacts/README.md` (1 проблем)

_Оборванный: 1_


### `docs/templates/README.md` (1 проблем)

_абзац: 1_



<!-- see-also -->

---

**Смотрите также:**
- [[READING_TIME]]
- [[READABILITY]]
- [[SEARCH]]
- [[SOURCE_MAP]]


<!-- similar-docs -->

---

**Похожие документы:**
- [HEADING_AUDIT](docs/HEADING_AUDIT.md) (сходство 0.67)
- [READING_TIME](docs/obsidian/READING_TIME.md) (сходство 0.63)
- [SOURCE_MAP](docs/obsidian/SOURCE_MAP.md) (сходство 0.55)

