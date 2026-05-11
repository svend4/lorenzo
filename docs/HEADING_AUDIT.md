# Аудит заголовков

<!-- toc -->
## Содержание

- [Типы проблем](#типы-проблем)
- [По файлам](#по-файлам)
  - [`docs/EMPTY_SECTIONS.md` (369 проблем)](#docsempty_sectionsmd-369-проблем)
  - [`docs/QA.md` (177 проблем)](#docsqamd-177-проблем)
  - [`docs/CODE_BLOCKS.md` (127 проблем)](#docscode_blocksmd-127-проблем)
  - [`docs/SPELLCHECK.md` (53 проблем)](#docsspellcheckmd-53-проблем)
  - [`docs/TABLES.md` (49 проблем)](#docstablesmd-49-проблем)
  - [`docs/processing-guide/PROCESSING_GUIDE.md` (31 проблем)](#docsprocessing-guideprocessing_guidemd-31-проблем)
  - [`docs/02-anthropic-vacancies/QA.md` (23 проблем)](#docs02-anthropic-vacanciesqamd-23-проблем)
  - [`docs/CHANGELOG.md` (20 проблем)](#docschangelogmd-20-проблем)
  - [`docs/processing-guide/QA.md` (19 проблем)](#docsprocessing-guideqamd-19-проблем)
  - [`docs/lorenzo-agent/QA.md` (18 проблем)](#docslorenzo-agentqamd-18-проблем)
  - [`docs/templates/protocol-spec.md` (18 проблем)](#docstemplatesprotocol-specmd-18-проблем)
  - [`docs/templates/rfc.md` (18 проблем)](#docstemplatesrfcmd-18-проблем)
  - [`docs/05-habr-projects/QA.md` (16 проблем)](#docs05-habr-projectsqamd-16-проблем)
  - [`docs/templates/mega-stack.md` (16 проблем)](#docstemplatesmega-stackmd-16-проблем)
  - [`docs/01-svyazi/QA.md` (15 проблем)](#docs01-svyaziqamd-15-проблем)
  - [`docs/04-ai-collaborations/QA.md` (15 проблем)](#docs04-ai-collaborationsqamd-15-проблем)
  - [`docs/02-anthropic-vacancies/69-section.md` (13 проблем)](#docs02-anthropic-vacancies69-sectionmd-13-проблем)
  - [`docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md` (13 проблем)](#docstechnology-combinationscombinations26-ast-based-code-analysis-for-legal-automationmd-13-проблем)
  - [`docs/templates/tech-pair.md` (13 проблем)](#docstemplatestech-pairmd-13-проблем)
  - [`docs/templates/template-of-templates.md` (13 проблем)](#docstemplatestemplate-of-templatesmd-13-проблем)
  - [`docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` (12 проблем)](#docs02-anthropic-vacancies109-3-принципы-консолидации-фаза-cmd-12-проблем)
  - [`docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` (12 проблем)](#docs02-anthropic-vacancies342-что-такое-вариант-c-concept-document-для-anthropicmd-12-проблем)
  - [`docs/GITHUB_ISSUES.md` (12 проблем)](#docsgithub_issuesmd-12-проблем)
  - [`docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` (11 проблем)](#docs02-anthropic-vacancies299-практические-рекомендации-для-текущего-проектаmd-11-проблем)
  - [`docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` (11 проблем)](#docs02-anthropic-vacancies365-развёрнутый-анализ-внуковой-комбинацииmd-11-проблем)
  - [`docs/SCRIPT_EVAL_REPORT.md` (11 проблем)](#docsscript_eval_reportmd-11-проблем)
  - [`docs/ai-collaborations/QA.md` (11 проблем)](#docsai-collaborationsqamd-11-проблем)
  - [`docs/templates/experiment-log.md` (11 проблем)](#docstemplatesexperiment-logmd-11-проблем)
  - [`docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` (10 проблем)](#docs02-anthropic-vacancies341-приложение-c-образец-спецификаций-инструментов-ingmd-10-проблем)
  - [`docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` (10 проблем)](#docs02-anthropic-vacancies98-appendix-a-minimal-working-examplemd-10-проблем)
  - [`docs/03-technology-combinations/05-benchmarks.md` (10 проблем)](#docs03-technology-combinations05-benchmarksmd-10-проблем)
  - [`docs/FAQ.md` (10 проблем)](#docsfaqmd-10-проблем)
  - [`docs/processing-guide/05-analysis.md` (10 проблем)](#docsprocessing-guide05-analysismd-10-проблем)
  - [`docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` (9 проблем)](#docs02-anthropic-vacancies02-общий-план-развития-nautilus-portal-protocolmd-9-проблем)
  - [`docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` (9 проблем)](#docs02-anthropic-vacancies149-appendix-b-summary-of-contributionsmd-9-проблем)
  - [`docs/02-anthropic-vacancies/165-closing.md` (9 проблем)](#docs02-anthropic-vacancies165-closingmd-9-проблем)
  - [`docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` (9 проблем)](#docs02-anthropic-vacancies293-почему-это-не-было-построеноmd-9-проблем)
  - [`docs/03-technology-combinations/QA.md` (9 проблем)](#docs03-technology-combinationsqamd-9-проблем)
  - [`docs/CONSISTENCY.md` (9 проблем)](#docsconsistencymd-9-проблем)
  - [`docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md` (9 проблем)](#docsnautiluscommunity-discussionsagent-changes-reality01-response-enmd-9-проблем)
  - [`docs/nautilus/npp-v1-1/22-glossary.md` (9 проблем)](#docsnautilusnpp-v1-122-glossarymd-9-проблем)
  - [`docs/templates/legal-case.md` (9 проблем)](#docstemplateslegal-casemd-9-проблем)
  - [`docs/02-anthropic-vacancies/09-4-passport-passport-md.md` (8 проблем)](#docs02-anthropic-vacancies09-4-passport-passport-mdmd-8-проблем)
  - [`docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` (8 проблем)](#docs02-anthropic-vacancies127-подключение-к-claude-desktopmd-8-проблем)
  - [`docs/02-anthropic-vacancies/133-обратная-связь.md` (8 проблем)](#docs02-anthropic-vacancies133-обратная-связьmd-8-проблем)
  - [`docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` (8 проблем)](#docs02-anthropic-vacancies229-профессиональные-коллеги-агентыmd-8-проблем)
  - [`docs/02-anthropic-vacancies/23-11-security-considerations.md` (8 проблем)](#docs02-anthropic-vacancies23-11-security-considerationsmd-8-проблем)
  - [`docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` (8 проблем)](#docs02-anthropic-vacancies28-appendix-a-minimal-working-examplemd-8-проблем)
  - [`docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` (8 проблем)](#docs02-anthropic-vacancies289-инфраструктура-для-ai-совместной-интеллектуальной-md-8-проблем)
  - [`docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` (8 проблем)](#docs02-anthropic-vacancies296-рекурсивное-прозрениеmd-8-проблем)
  - [`docs/02-anthropic-vacancies/319-acknowledgments.md` (8 проблем)](#docs02-anthropic-vacancies319-acknowledgmentsmd-8-проблем)
  - [`docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` (8 проблем)](#docs02-anthropic-vacancies324-ingit-как-cowork-интегрированная-подложка-рабочегоmd-8-проблем)
  - [`docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` (8 проблем)](#docs02-anthropic-vacancies329-3-что-ingit-обеспечивает-чего-cowork-не-хватаетmd-8-проблем)
  - [`docs/02-anthropic-vacancies/356-твой-workflow.md` (8 проблем)](#docs02-anthropic-vacancies356-твой-workflowmd-8-проблем)
  - [`docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` (8 проблем)](#docs02-anthropic-vacancies71-критерии-выбора-для-фазы-3md-8-проблем)
  - [`docs/05-habr-projects/01-synthesis.md` (8 проблем)](#docs05-habr-projects01-synthesismd-8-проблем)
  - [`docs/nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md` (8 проблем)](#docsnautilusnpp-v1-016-appendix-a-minimal-working-examplemd-8-проблем)
  - [`docs/svyazi-2-0/QA.md` (8 проблем)](#docssvyazi-2-0qamd-8-проблем)
  - [`docs/templates/meeting-notes.md` (8 проблем)](#docstemplatesmeeting-notesmd-8-проблем)
  - [`docs/templates/weekly-digest.md` (8 проблем)](#docstemplatesweekly-digestmd-8-проблем)
  - [`docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` (7 проблем)](#docs02-anthropic-vacancies01-интегральный-анализ-профиля-svend4md-7-проблем)
  - [`docs/02-anthropic-vacancies/03-portal-protocol-md.md` (7 проблем)](#docs02-anthropic-vacancies03-portal-protocol-mdmd-7-проблем)
  - [`docs/02-anthropic-vacancies/103-appendix-b-change-log.md` (7 проблем)](#docs02-anthropic-vacancies103-appendix-b-change-logmd-7-проблем)
  - [`docs/02-anthropic-vacancies/105-review-methodology-md.md` (7 проблем)](#docs02-anthropic-vacancies105-review-methodology-mdmd-7-проблем)
  - [`docs/02-anthropic-vacancies/203-благодарности.md` (7 проблем)](#docs02-anthropic-vacancies203-благодарностиmd-7-проблем)
  - [`docs/02-anthropic-vacancies/21-9-query-flow.md` (7 проблем)](#docs02-anthropic-vacancies21-9-query-flowmd-7-проблем)
  - [`docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` (7 проблем)](#docs02-anthropic-vacancies234-3-эмпирический-кейс-обучайmd-7-проблем)
  - [`docs/02-anthropic-vacancies/320-references.md` (7 проблем)](#docs02-anthropic-vacancies320-referencesmd-7-проблем)
  - [`docs/02-anthropic-vacancies/338-ссылки.md` (7 проблем)](#docs02-anthropic-vacancies338-ссылкиmd-7-проблем)
  - [`docs/02-anthropic-vacancies/34-appendix-b-change-log.md` (7 проблем)](#docs02-anthropic-vacancies34-appendix-b-change-logmd-7-проблем)
  - [`docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` (7 проблем)](#docs02-anthropic-vacancies343-lorenzo-catalyst-agent-глубокая-проработка-специфиmd-7-проблем)
  - [`docs/02-anthropic-vacancies/35-passports-info1-md.md` (7 проблем)](#docs02-anthropic-vacancies35-passports-info1-mdmd-7-проблем)
  - [`docs/02-anthropic-vacancies/45-passports-pro2-md.md` (7 проблем)](#docs02-anthropic-vacancies45-passports-pro2-mdmd-7-проблем)
  - [`docs/02-anthropic-vacancies/55-passports-meta-md.md` (7 проблем)](#docs02-anthropic-vacancies55-passports-meta-mdmd-7-проблем)
  - [`docs/02-anthropic-vacancies/65-readme-md.md` (7 проблем)](#docs02-anthropic-vacancies65-readme-mdmd-7-проблем)
  - [`docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` (7 проблем)](#docs02-anthropic-vacancies73-portal-protocol-md-v1-1md-7-проблем)
  - [`docs/02-anthropic-vacancies/90-15-security-considerations.md` (7 проблем)](#docs02-anthropic-vacancies90-15-security-considerationsmd-7-проблем)
  - [`docs/03-technology-combinations/01-agent-routing.md` (7 проблем)](#docs03-technology-combinations01-agent-routingmd-7-проблем)
  - [`docs/METHODOLOGY.md` (7 проблем)](#docsmethodologymd-7-проблем)
  - [`docs/autofilled/research-summary.md` (7 проблем)](#docsautofilledresearch-summarymd-7-проблем)
  - [`docs/nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md` (7 проблем)](#docsnautilusnpp-humanitarian-extension01-structural-comparison-code-vs-docsmd-7-проблем)
  - [`docs/templates/faq-entry.md` (7 проблем)](#docstemplatesfaq-entrymd-7-проблем)
  - [`docs/templates/glossary-entry.md` (7 проблем)](#docstemplatesglossary-entrymd-7-проблем)
  - [`docs/templates/prototype-mvp.md` (7 проблем)](#docstemplatesprototype-mvpmd-7-проблем)
  - [`docs/templates/risk-entry.md` (7 проблем)](#docstemplatesrisk-entrymd-7-проблем)
  - [`docs/templates/tech-radar-entry.md` (7 проблем)](#docstemplatestech-radar-entrymd-7-проблем)
  - [`docs/02-anthropic-vacancies/00-intro.md` (6 проблем)](#docs02-anthropic-vacancies00-intromd-6-проблем)
  - [`docs/02-anthropic-vacancies/04-abstract.md` (6 проблем)](#docs02-anthropic-vacancies04-abstractmd-6-проблем)
  - [`docs/02-anthropic-vacancies/104-appendix-c-references.md` (6 проблем)](#docs02-anthropic-vacancies104-appendix-c-referencesmd-6-проблем)
  - [`docs/02-anthropic-vacancies/12-content-overview.md` (6 проблем)](#docs02-anthropic-vacancies12-content-overviewmd-6-проблем)
  - [`docs/02-anthropic-vacancies/130-отладка.md` (6 проблем)](#docs02-anthropic-vacancies130-отладкаmd-6-проблем)
  - [`docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` (6 проблем)](#docs02-anthropic-vacancies131-ограничения-текущей-версии-0-1-0-draftmd-6-проблем)
  - [`docs/02-anthropic-vacancies/132-planned-v0-2-0.md` (6 проблем)](#docs02-anthropic-vacancies132-planned-v0-2-0md-6-проблем)
  - [`docs/02-anthropic-vacancies/154-table-of-contents.md` (6 проблем)](#docs02-anthropic-vacancies154-table-of-contentsmd-6-проблем)
  - [`docs/02-anthropic-vacancies/159-5-economic-model.md` (6 проблем)](#docs02-anthropic-vacancies159-5-economic-modelmd-6-проблем)
  - [`docs/02-anthropic-vacancies/18-6-adapter-interface.md` (6 проблем)](#docs02-anthropic-vacancies18-6-adapter-interfacemd-6-проблем)
  - [`docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` (6 проблем)](#docs02-anthropic-vacancies193-3-что-делает-агента-представительскимmd-6-проблем)
  - [`docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` (6 проблем)](#docs02-anthropic-vacancies239-8-пилотное-предложение-sgb-колega-адвокатmd-6-проблем)
  - [`docs/02-anthropic-vacancies/24-12-versioning-policy.md` (6 проблем)](#docs02-anthropic-vacancies24-12-versioning-policymd-6-проблем)
  - [`docs/02-anthropic-vacancies/243-12-заключение.md` (6 проблем)](#docs02-anthropic-vacancies243-12-заключениеmd-6-проблем)
  - [`docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` (6 проблем)](#docs02-anthropic-vacancies26-14-adr-001-federation-over-mergingmd-6-проблем)
  - [`docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` (6 проблем)](#docs02-anthropic-vacancies291-двухслойный-стек-как-он-существуетmd-6-проблем)
  - [`docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` (6 проблем)](#docs02-anthropic-vacancies305-a-practical-path-to-layer-b-through-symbiotic-intemd-6-проблем)
  - [`docs/02-anthropic-vacancies/31-content-overview.md` (6 проблем)](#docs02-anthropic-vacancies31-content-overviewmd-6-проблем)
  - [`docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` (6 проблем)](#docs02-anthropic-vacancies351-что-ты-можешь-делатьmd-6-проблем)
  - [`docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` (6 проблем)](#docs02-anthropic-vacancies358-твоя-relationship-с-другими-aimd-6-проблем)
  - [`docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` (6 проблем)](#docs02-anthropic-vacancies364-final-note-ты-experimentmd-6-проблем)
  - [`docs/02-anthropic-vacancies/37-native-format.md` (6 проблем)](#docs02-anthropic-vacancies37-native-formatmd-6-проблем)
  - [`docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` (6 проблем)](#docs02-anthropic-vacancies44-for-the-curious-philosophymd-6-проблем)
  - [`docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` (6 проблем)](#docs02-anthropic-vacancies54-for-the-curious-philosophymd-6-проблем)
  - [`docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` (6 проблем)](#docs02-anthropic-vacancies70-зачем-две-версии-параллельноmd-6-проблем)
  - [`docs/02-anthropic-vacancies/72-расписание-фазы-3.md` (6 проблем)](#docs02-anthropic-vacancies72-расписание-фазы-3md-6-проблем)
  - [`docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` (6 проблем)](#docs02-anthropic-vacancies84-9-consensus-algorithmmd-6-проблем)
  - [`docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` (6 проблем)](#docs02-anthropic-vacancies94-19-adr-001-federation-over-mergingmd-6-проблем)
  - [`docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` (6 проблем)](#docs02-anthropic-vacancies95-20-adr-002-q6-as-first-class-protocol-conceptmd-6-проблем)
  - [`docs/03-technology-combinations/03-local-first.md` (6 проблем)](#docs03-technology-combinations03-local-firstmd-6-проблем)
  - [`docs/05-habr-projects/knowledge/wikontic.md` (6 проблем)](#docs05-habr-projectsknowledgewikonticmd-6-проблем)
  - [`docs/05-habr-projects/memory/yodoca.md` (6 проблем)](#docs05-habr-projectsmemoryyodocamd-6-проблем)
  - [`docs/SCHEDULE.md` (6 проблем)](#docsschedulemd-6-проблем)
  - [`docs/meta-scripting/QA.md` (6 проблем)](#docsmeta-scriptingqamd-6-проблем)
  - [`docs/nautilus/npp-v1-0/15-glossary.md` (6 проблем)](#docsnautilusnpp-v1-015-glossarymd-6-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/00-abstract.md` (6 проблем)](#docsnautilusprofessional-colleague-agents-en00-abstractmd-6-проблем)
  - [`docs/nautilus/representative-agent-layer-en/12-closing.md` (6 проблем)](#docsnautilusrepresentative-agent-layer-en12-closingmd-6-проблем)
  - [`docs/templates/contradiction-record.md` (6 проблем)](#docstemplatescontradiction-recordmd-6-проблем)
  - [`docs/templates/retrospective.md` (6 проблем)](#docstemplatesretrospectivemd-6-проблем)
  - [`docs/02-anthropic-vacancies/05-0-status-of-this-document.md` (5 проблем)](#docs02-anthropic-vacancies05-0-status-of-this-documentmd-5-проблем)
  - [`docs/02-anthropic-vacancies/106-tl-dr.md` (5 проблем)](#docs02-anthropic-vacancies106-tl-drmd-5-проблем)
  - [`docs/02-anthropic-vacancies/111-4-условия-применимости.md` (5 проблем)](#docs02-anthropic-vacancies111-4-условия-применимостиmd-5-проблем)
  - [`docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` (5 проблем)](#docs02-anthropic-vacancies112-5-связь-с-существующими-методологиямиmd-5-проблем)
  - [`docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` (5 проблем)](#docs02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd-5-проблем)
  - [`docs/02-anthropic-vacancies/120-главные-технические-риски.md` (5 проблем)](#docs02-anthropic-vacancies120-главные-технические-рискиmd-5-проблем)
  - [`docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` (5 проблем)](#docs02-anthropic-vacancies121-appendix-c-история-изменений-методологииmd-5-проблем)
  - [`docs/02-anthropic-vacancies/122-глоссарий.md` (5 проблем)](#docs02-anthropic-vacancies122-глоссарийmd-5-проблем)
  - [`docs/02-anthropic-vacancies/123-portal-mcp-py.md` (5 проблем)](#docs02-anthropic-vacancies123-portal-mcp-pymd-5-проблем)
  - [`docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` (5 проблем)](#docs02-anthropic-vacancies124-конфигурация-для-claude-desktopmd-5-проблем)
  - [`docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` (5 проблем)](#docs02-anthropic-vacancies125-readme-mcp-md-инструкция-по-установкеmd-5-проблем)
  - [`docs/02-anthropic-vacancies/126-установка.md` (5 проблем)](#docs02-anthropic-vacancies126-установкаmd-5-проблем)
  - [`docs/02-anthropic-vacancies/128-доступные-инструменты.md` (5 проблем)](#docs02-anthropic-vacancies128-доступные-инструментыmd-5-проблем)
  - [`docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` (5 проблем)](#docs02-anthropic-vacancies129-примеры-запросов-в-claudemd-5-проблем)
  - [`docs/02-anthropic-vacancies/13-angle-perspective.md` (5 проблем)](#docs02-anthropic-vacancies13-angle-perspectivemd-5-проблем)
  - [`docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` (5 проблем)](#docs02-anthropic-vacancies134-the-double-triangle-architecture-mdmd-5-проблем)
  - [`docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` (5 проблем)](#docs02-anthropic-vacancies135-a-formal-model-for-human-ai-collaboration-in-distrmd-5-проблем)
  - [`docs/02-anthropic-vacancies/137-table-of-contents.md` (5 проблем)](#docs02-anthropic-vacancies137-table-of-contentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` (5 проблем)](#docs02-anthropic-vacancies139-2-the-double-triangle-architecturemd-5-проблем)
  - [`docs/02-anthropic-vacancies/146-acknowledgments.md` (5 проблем)](#docs02-anthropic-vacancies146-acknowledgmentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/148-appendix-a-glossary.md` (5 проблем)](#docs02-anthropic-vacancies148-appendix-a-glossarymd-5-проблем)
  - [`docs/02-anthropic-vacancies/150-appendix-c-version-history.md` (5 проблем)](#docs02-anthropic-vacancies150-appendix-c-version-historymd-5-проблем)
  - [`docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` (5 проблем)](#docs02-anthropic-vacancies151-open-knowledge-work-foundation-mdmd-5-проблем)
  - [`docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` (5 проблем)](#docs02-anthropic-vacancies152-ai-coordinated-infrastructure-for-distributed-expemd-5-проблем)
  - [`docs/02-anthropic-vacancies/155-1-problem-statement.md` (5 проблем)](#docs02-anthropic-vacancies155-1-problem-statementmd-5-проблем)
  - [`docs/02-anthropic-vacancies/156-2-target-populations.md` (5 проблем)](#docs02-anthropic-vacancies156-2-target-populationsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/16-history.md` (5 проблем)](#docs02-anthropic-vacancies16-historymd-5-проблем)
  - [`docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` (5 проблем)](#docs02-anthropic-vacancies161-7-phased-rollout-planmd-5-проблем)
  - [`docs/02-anthropic-vacancies/162-8-risk-analysis.md` (5 проблем)](#docs02-anthropic-vacancies162-8-risk-analysismd-5-проблем)
  - [`docs/02-anthropic-vacancies/164-10-appendices.md` (5 проблем)](#docs02-anthropic-vacancies164-10-appendicesmd-5-проблем)
  - [`docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` (5 проблем)](#docs02-anthropic-vacancies166-representative-agent-layer-mdmd-5-проблем)
  - [`docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` (5 проблем)](#docs02-anthropic-vacancies167-ai-mediated-representation-for-underrepresented-exmd-5-проблем)
  - [`docs/02-anthropic-vacancies/169-table-of-contents.md` (5 проблем)](#docs02-anthropic-vacancies169-table-of-contentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` (5 проблем)](#docs02-anthropic-vacancies170-1-the-cinderella-syndrome-why-quality-stays-invisimd-5-проблем)
  - [`docs/02-anthropic-vacancies/174-5-architectural-specification.md` (5 проблем)](#docs02-anthropic-vacancies174-5-architectural-specificationmd-5-проблем)
  - [`docs/02-anthropic-vacancies/181-12-closing.md` (5 проблем)](#docs02-anthropic-vacancies181-12-closingmd-5-проблем)
  - [`docs/02-anthropic-vacancies/182-acknowledgments.md` (5 проблем)](#docs02-anthropic-vacancies182-acknowledgmentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` (5 проблем)](#docs02-anthropic-vacancies184-appendix-a-connection-to-companion-papersmd-5-проблем)
  - [`docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` (5 проблем)](#docs02-anthropic-vacancies186-appendix-c-sample-use-cases-in-detailmd-5-проблем)
  - [`docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` (5 проблем)](#docs02-anthropic-vacancies187-слой-представительских-агентов-mdmd-5-проблем)
  - [`docs/02-anthropic-vacancies/189-аннотация.md` (5 проблем)](#docs02-anthropic-vacancies189-аннотацияmd-5-проблем)
  - [`docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` (5 проблем)](#docs02-anthropic-vacancies191-1-синдром-золушки-почему-качество-остаётся-невидимmd-5-проблем)
  - [`docs/02-anthropic-vacancies/196-6-этическая-рамка.md` (5 проблем)](#docs02-anthropic-vacancies196-6-этическая-рамкаmd-5-проблем)
  - [`docs/02-anthropic-vacancies/202-12-заключение.md` (5 проблем)](#docs02-anthropic-vacancies202-12-заключениеmd-5-проблем)
  - [`docs/02-anthropic-vacancies/204-ссылки.md` (5 проблем)](#docs02-anthropic-vacancies204-ссылкиmd-5-проблем)
  - [`docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` (5 проблем)](#docs02-anthropic-vacancies206-приложение-b-матрица-сравнения-областейmd-5-проблем)
  - [`docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` (5 проблем)](#docs02-anthropic-vacancies207-приложение-c-образцы-случаев-использования-в-деталmd-5-проблем)
  - [`docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` (5 проблем)](#docs02-anthropic-vacancies208-professional-colleague-agents-mdmd-5-проблем)
  - [`docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` (5 проблем)](#docs02-anthropic-vacancies209-a-typology-of-ai-agents-on-the-principal-side-and-md-5-проблем)
  - [`docs/02-anthropic-vacancies/211-table-of-contents.md` (5 проблем)](#docs02-anthropic-vacancies211-table-of-contentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` (5 проблем)](#docs02-anthropic-vacancies213-2-what-makes-a-professional-colleague-agentmd-5-проблем)
  - [`docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` (5 проблем)](#docs02-anthropic-vacancies215-4-architecture-of-professional-colleague-agentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/22-10-queryresult-structure.md` (5 проблем)](#docs02-anthropic-vacancies22-10-queryresult-structuremd-5-проблем)
  - [`docs/02-anthropic-vacancies/224-acknowledgments.md` (5 проблем)](#docs02-anthropic-vacancies224-acknowledgmentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/230-аннотация.md` (5 проблем)](#docs02-anthropic-vacancies230-аннотацияmd-5-проблем)
  - [`docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` (5 проблем)](#docs02-anthropic-vacancies233-2-что-делает-агента-профессиональным-коллегойmd-5-проблем)
  - [`docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` (5 проблем)](#docs02-anthropic-vacancies236-5-экономика-тиражирования-по-профессииmd-5-проблем)
  - [`docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` (5 проблем)](#docs02-anthropic-vacancies241-10-открытые-вопросыmd-5-проблем)
  - [`docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` (5 проблем)](#docs02-anthropic-vacancies242-11-призыв-к-сотрудничествуmd-5-проблем)
  - [`docs/02-anthropic-vacancies/244-благодарности.md` (5 проблем)](#docs02-anthropic-vacancies244-благодарностиmd-5-проблем)
  - [`docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` (5 проблем)](#docs02-anthropic-vacancies249-composite-skills-agent-mdmd-5-проблем)
  - [`docs/02-anthropic-vacancies/25-13-reference-implementation.md` (5 проблем)](#docs02-anthropic-vacancies25-13-reference-implementationmd-5-проблем)
  - [`docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` (5 проблем)](#docs02-anthropic-vacancies251-ai-support-through-configurable-specialist-ensemblmd-5-проблем)
  - [`docs/02-anthropic-vacancies/253-table-of-contents.md` (5 проблем)](#docs02-anthropic-vacancies253-table-of-contentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` (5 проблем)](#docs02-anthropic-vacancies254-1-why-the-binary-view-is-incompletemd-5-проблем)
  - [`docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` (5 проблем)](#docs02-anthropic-vacancies256-3-what-makes-a-composite-skills-agentmd-5-проблем)
  - [`docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` (5 проблем)](#docs02-anthropic-vacancies269-appendix-a-the-six-type-taxonomy-updatedmd-5-проблем)
  - [`docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` (5 проблем)](#docs02-anthropic-vacancies273-infrastructure-for-ai-collaborative-intellectual-wmd-5-проблем)
  - [`docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` (5 проблем)](#docs02-anthropic-vacancies274-the-missing-middle-layer-between-chat-and-codemd-5-проблем)
  - [`docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` (5 проблем)](#docs02-anthropic-vacancies282-what-industry-will-likely-buildmd-5-проблем)
  - [`docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` (5 проблем)](#docs02-anthropic-vacancies283-what-this-document-doesn-t-solvemd-5-проблем)
  - [`docs/02-anthropic-vacancies/285-closing.md` (5 проблем)](#docs02-anthropic-vacancies285-closingmd-5-проблем)
  - [`docs/02-anthropic-vacancies/286-acknowledgments.md` (5 проблем)](#docs02-anthropic-vacancies286-acknowledgmentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` (5 проблем)](#docs02-anthropic-vacancies292-что-отсутствует-слой-bmd-5-проблем)
  - [`docs/02-anthropic-vacancies/301-благодарности.md` (5 проблем)](#docs02-anthropic-vacancies301-благодарностиmd-5-проблем)
  - [`docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` (5 проблем)](#docs02-anthropic-vacancies304-ingit-as-cowork-native-workspace-substrate-mdmd-5-проблем)
  - [`docs/02-anthropic-vacancies/308-table-of-contents.md` (5 проблем)](#docs02-anthropic-vacancies308-table-of-contentsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` (5 проблем)](#docs02-anthropic-vacancies317-9-risks-and-open-questionsmd-5-проблем)
  - [`docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` (5 проблем)](#docs02-anthropic-vacancies321-appendix-a-decision-tree-for-ingit-adoptersmd-5-проблем)
  - [`docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` (5 проблем)](#docs02-anthropic-vacancies333-7-практические-первые-шаги-в-этом-месяцеmd-5-проблем)
  - [`docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` (5 проблем)](#docs02-anthropic-vacancies344-системный-промпт-для-lorenzo-projectmd-5-проблем)
  - [`docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` (5 проблем)](#docs02-anthropic-vacancies353-что-ты-не-можешь-делать-вообщеmd-5-проблем)
  - [`docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` (5 проблем)](#docs02-anthropic-vacancies355-существующие-документы-dhlab-твой-contextmd-5-проблем)
  - [`docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` (5 проблем)](#docs02-anthropic-vacancies366-технический-stack-svyazi-2-0-foundationmd-5-проблем)
  - [`docs/02-anthropic-vacancies/39-angle-perspective.md` (5 проблем)](#docs02-anthropic-vacancies39-angle-perspectivemd-5-проблем)
  - [`docs/02-anthropic-vacancies/41-compatibility-level.md` (5 проблем)](#docs02-anthropic-vacancies41-compatibility-levelmd-5-проблем)
  - [`docs/02-anthropic-vacancies/42-author-contact.md` (5 проблем)](#docs02-anthropic-vacancies42-author-contactmd-5-проблем)
  - [`docs/02-anthropic-vacancies/47-native-format.md` (5 проблем)](#docs02-anthropic-vacancies47-native-formatmd-5-проблем)
  - [`docs/02-anthropic-vacancies/49-angle-perspective.md` (5 проблем)](#docs02-anthropic-vacancies49-angle-perspectivemd-5-проблем)
  - [`docs/02-anthropic-vacancies/51-compatibility-level.md` (5 проблем)](#docs02-anthropic-vacancies51-compatibility-levelmd-5-проблем)
  - [`docs/02-anthropic-vacancies/52-author-contact.md` (5 проблем)](#docs02-anthropic-vacancies52-author-contactmd-5-проблем)
  - [`docs/02-anthropic-vacancies/53-history.md` (5 проблем)](#docs02-anthropic-vacancies53-historymd-5-проблем)
  - [`docs/02-anthropic-vacancies/59-angle-perspective.md` (5 проблем)](#docs02-anthropic-vacancies59-angle-perspectivemd-5-проблем)
  - [`docs/02-anthropic-vacancies/61-compatibility-level.md` (5 проблем)](#docs02-anthropic-vacancies61-compatibility-levelmd-5-проблем)
  - [`docs/02-anthropic-vacancies/62-author-contact.md` (5 проблем)](#docs02-anthropic-vacancies62-author-contactmd-5-проблем)
  - [`docs/02-anthropic-vacancies/63-history.md` (5 проблем)](#docs02-anthropic-vacancies63-historymd-5-проблем)
  - [`docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` (5 проблем)](#docs02-anthropic-vacancies64-for-the-curious-philosophymd-5-проблем)
  - [`docs/02-anthropic-vacancies/67-о-проекте.md` (5 проблем)](#docs02-anthropic-vacancies67-о-проектеmd-5-проблем)
  - [`docs/02-anthropic-vacancies/74-abstract.md` (5 проблем)](#docs02-anthropic-vacancies74-abstractmd-5-проблем)
  - [`docs/02-anthropic-vacancies/75-0-status-of-this-document.md` (5 проблем)](#docs02-anthropic-vacancies75-0-status-of-this-documentmd-5-проблем)
  - [`docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` (5 проблем)](#docs02-anthropic-vacancies78-3-registry-nautilus-jsonmd-5-проблем)
  - [`docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` (5 проблем)](#docs02-anthropic-vacancies89-14-sdk-contract-informativemd-5-проблем)
  - [`docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` (5 проблем)](#docs02-anthropic-vacancies91-16-mcp-extension-informativemd-5-проблем)
  - [`docs/02-anthropic-vacancies/93-18-reference-implementation.md` (5 проблем)](#docs02-anthropic-vacancies93-18-reference-implementationmd-5-проблем)
  - [`docs/VALIDATION.md` (5 проблем)](#docsvalidationmd-5-проблем)
  - [`docs/anthropic-vacancies/QA.md` (5 проблем)](#docsanthropic-vacanciesqamd-5-проблем)
  - [`docs/autofilled/components/.md` (5 проблем)](#docsautofilledcomponentsmd-5-проблем)
  - [`docs/autofilled/components/cowork.md` (5 проблем)](#docsautofilledcomponentscoworkmd-5-проблем)
  - [`docs/autofilled/components/ingit.md` (5 проблем)](#docsautofilledcomponentsingitmd-5-проблем)
  - [`docs/autofilled/components/kksudo.md` (5 проблем)](#docsautofilledcomponentskksudomd-5-проблем)
  - [`docs/autofilled/components/lorenzo.md` (5 проблем)](#docsautofilledcomponentslorenzomd-5-проблем)
  - [`docs/autofilled/components/nautilus.md` (5 проблем)](#docsautofilledcomponentsnautilusmd-5-проблем)
  - [`docs/autofilled/components/sgb.md` (5 проблем)](#docsautofilledcomponentssgbmd-5-проблем)
  - [`docs/autofilled/components/spbmolot.md` (5 проблем)](#docsautofilledcomponentsspbmolotmd-5-проблем)
  - [`docs/autofilled/components/svend4.md` (5 проблем)](#docsautofilledcomponentssvend4md-5-проблем)
  - [`docs/autofilled/components/svyazi.md` (5 проблем)](#docsautofilledcomponentssvyazimd-5-проблем)
  - [`docs/meta-scripting/02-architecture.md` (5 проблем)](#docsmeta-scripting02-architecturemd-5-проблем)
  - [`docs/meta-scripting/04-enrichment.md` (5 проблем)](#docsmeta-scripting04-enrichmentmd-5-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/00-intro.md` (5 проблем)](#docsnautilusinfrastructure-layer-b-en00-intromd-5-проблем)
  - [`docs/nautilus/npp-v1-1/09-consensus-algorithm.md` (5 проблем)](#docsnautilusnpp-v1-109-consensus-algorithmmd-5-проблем)
  - [`docs/nautilus/okwf-concept/00-abstract.md` (5 проблем)](#docsnautilusokwf-concept00-abstractmd-5-проблем)
  - [`docs/nautilus/representative-agent-layer-en/00-abstract.md` (5 проблем)](#docsnautilusrepresentative-agent-layer-en00-abstractmd-5-проблем)
  - [`docs/processing-guide/07-llm.md` (5 проблем)](#docsprocessing-guide07-llmmd-5-проблем)
  - [`docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md` (5 проблем)](#docstechnology-combinationscombinations25-legal-dsl-code-transpilermd-5-проблем)
  - [`docs/02-anthropic-vacancies/06-1-introduction.md` (4 проблем)](#docs02-anthropic-vacancies06-1-introductionmd-4-проблем)
  - [`docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` (4 проблем)](#docs02-anthropic-vacancies08-3-registry-nautilus-jsonmd-4-проблем)
  - [`docs/02-anthropic-vacancies/102-доступ-к-данным.md` (4 проблем)](#docs02-anthropic-vacancies102-доступ-к-даннымmd-4-проблем)
  - [`docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` (4 проблем)](#docs02-anthropic-vacancies107-1-контекст-и-мотивацияmd-4-проблем)
  - [`docs/02-anthropic-vacancies/108-2-формальный-workflow.md` (4 проблем)](#docs02-anthropic-vacancies108-2-формальный-workflowmd-4-проблем)
  - [`docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` (4 проблем)](#docs02-anthropic-vacancies113-6-почему-это-валидный-паттерн-для-ai-assisted-workmd-4-проблем)
  - [`docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` (4 проблем)](#docs02-anthropic-vacancies114-7-реализация-в-проекте-nautilusmd-4-проблем)
  - [`docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` (4 проблем)](#docs02-anthropic-vacancies116-9-checklist-применения-методологииmd-4-проблем)
  - [`docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` (4 проблем)](#docs02-anthropic-vacancies117-10-конкретный-план-применения-к-текущим-документамmd-4-проблем)
  - [`docs/02-anthropic-vacancies/136-abstract.md` (4 проблем)](#docs02-anthropic-vacancies136-abstractmd-4-проблем)
  - [`docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` (4 проблем)](#docs02-anthropic-vacancies140-3-three-inter-layer-protocolsmd-4-проблем)
  - [`docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` (4 проблем)](#docs02-anthropic-vacancies141-4-nautilus-portal-as-reference-substratemd-4-проблем)
  - [`docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` (4 проблем)](#docs02-anthropic-vacancies142-5-pattern-library-as-bridge-between-trianglesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` (4 проблем)](#docs02-anthropic-vacancies143-6-four-deployment-domainsmd-4-проблем)
  - [`docs/02-anthropic-vacancies/144-7-open-questions.md` (4 проблем)](#docs02-anthropic-vacancies144-7-open-questionsmd-4-проблем)
  - [`docs/02-anthropic-vacancies/145-8-call-to-action.md` (4 проблем)](#docs02-anthropic-vacancies145-8-call-to-actionmd-4-проблем)
  - [`docs/02-anthropic-vacancies/147-references.md` (4 проблем)](#docs02-anthropic-vacancies147-referencesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/153-executive-summary.md` (4 проблем)](#docs02-anthropic-vacancies153-executive-summarymd-4-проблем)
  - [`docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` (4 проблем)](#docs02-anthropic-vacancies157-3-why-existing-solutions-failmd-4-проблем)
  - [`docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` (4 проблем)](#docs02-anthropic-vacancies160-6-governance-and-ethicsmd-4-проблем)
  - [`docs/02-anthropic-vacancies/168-abstract.md` (4 проблем)](#docs02-anthropic-vacancies168-abstractmd-4-проблем)
  - [`docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` (4 проблем)](#docs02-anthropic-vacancies171-2-historical-precedents-agents-as-civilizational-imd-4-проблем)
  - [`docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` (4 проблем)](#docs02-anthropic-vacancies172-3-what-makes-a-representative-agentmd-4-проблем)
  - [`docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` (4 проблем)](#docs02-anthropic-vacancies180-11-call-for-collaborationmd-4-проблем)
  - [`docs/02-anthropic-vacancies/183-references.md` (4 проблем)](#docs02-anthropic-vacancies183-referencesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` (4 проблем)](#docs02-anthropic-vacancies185-appendix-b-domain-comparison-matrixmd-4-проблем)
  - [`docs/02-anthropic-vacancies/19-7-portalentry-structure.md` (4 проблем)](#docs02-anthropic-vacancies19-7-portalentry-structuremd-4-проблем)
  - [`docs/02-anthropic-vacancies/190-содержание.md` (4 проблем)](#docs02-anthropic-vacancies190-содержаниеmd-4-проблем)
  - [`docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` (4 проблем)](#docs02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd-4-проблем)
  - [`docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` (4 проблем)](#docs02-anthropic-vacancies195-5-архитектурная-спецификацияmd-4-проблем)
  - [`docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` (4 проблем)](#docs02-anthropic-vacancies197-7-управление-и-надзорmd-4-проблем)
  - [`docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` (4 проблем)](#docs02-anthropic-vacancies198-8-риски-и-меры-противодействияmd-4-проблем)
  - [`docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` (4 проблем)](#docs02-anthropic-vacancies199-9-стратегия-поэтапного-развёртыванияmd-4-проблем)
  - [`docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` (4 проблем)](#docs02-anthropic-vacancies20-8-consensus-algorithmmd-4-проблем)
  - [`docs/02-anthropic-vacancies/210-abstract.md` (4 проблем)](#docs02-anthropic-vacancies210-abstractmd-4-проблем)
  - [`docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` (4 проблем)](#docs02-anthropic-vacancies214-3-empirical-case-study-обучайmd-4-проблем)
  - [`docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` (4 проблем)](#docs02-anthropic-vacancies216-5-the-economics-of-profession-wide-replicationmd-4-проблем)
  - [`docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` (4 проблем)](#docs02-anthropic-vacancies217-6-risks-specific-to-this-categorymd-4-проблем)
  - [`docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` (4 проблем)](#docs02-anthropic-vacancies219-8-pilot-proposal-sgb-advocate-colleaguemd-4-проблем)
  - [`docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` (4 проблем)](#docs02-anthropic-vacancies220-9-relationship-to-other-agent-typesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` (4 проблем)](#docs02-anthropic-vacancies222-11-call-for-collaborationmd-4-проблем)
  - [`docs/02-anthropic-vacancies/223-12-closing.md` (4 проблем)](#docs02-anthropic-vacancies223-12-closingmd-4-проблем)
  - [`docs/02-anthropic-vacancies/225-references.md` (4 проблем)](#docs02-anthropic-vacancies225-referencesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` (4 проблем)](#docs02-anthropic-vacancies227-appendix-b-decision-framework-when-to-build-type-1md-4-проблем)
  - [`docs/02-anthropic-vacancies/231-содержание.md` (4 проблем)](#docs02-anthropic-vacancies231-содержаниеmd-4-проблем)
  - [`docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` (4 проблем)](#docs02-anthropic-vacancies240-9-связь-с-другими-типами-агентовmd-4-проблем)
  - [`docs/02-anthropic-vacancies/245-ссылки.md` (4 проблем)](#docs02-anthropic-vacancies245-ссылкиmd-4-проблем)
  - [`docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` (4 проблем)](#docs02-anthropic-vacancies246-приложение-a-сравнительная-таблица-пять-типов-агенmd-4-проблем)
  - [`docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` (4 проблем)](#docs02-anthropic-vacancies247-приложение-b-рамка-принятия-решений-когда-строить-md-4-проблем)
  - [`docs/02-anthropic-vacancies/252-abstract.md` (4 проблем)](#docs02-anthropic-vacancies252-abstractmd-4-проблем)
  - [`docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` (4 проблем)](#docs02-anthropic-vacancies255-2-the-twenty-one-teachers-patternmd-4-проблем)
  - [`docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` (4 проблем)](#docs02-anthropic-vacancies257-4-the-sub-agent-registrymd-4-проблем)
  - [`docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` (4 проблем)](#docs02-anthropic-vacancies258-5-configuration-how-principals-build-their-ensemblmd-4-проблем)
  - [`docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` (4 проблем)](#docs02-anthropic-vacancies259-6-coordination-and-disagreement-resolutionmd-4-проблем)
  - [`docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` (4 проблем)](#docs02-anthropic-vacancies260-7-economics-of-combinatorial-replicationmd-4-проблем)
  - [`docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` (4 проблем)](#docs02-anthropic-vacancies261-8-seven-domains-of-applicationmd-4-проблем)
  - [`docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` (4 проблем)](#docs02-anthropic-vacancies263-10-risks-specific-to-composite-architecturesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/264-11-open-questions.md` (4 проблем)](#docs02-anthropic-vacancies264-11-open-questionsmd-4-проблем)
  - [`docs/02-anthropic-vacancies/266-13-closing.md` (4 проблем)](#docs02-anthropic-vacancies266-13-closingmd-4-проблем)
  - [`docs/02-anthropic-vacancies/267-acknowledgments.md` (4 проблем)](#docs02-anthropic-vacancies267-acknowledgmentsmd-4-проблем)
  - [`docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` (4 проблем)](#docs02-anthropic-vacancies272-appendix-d-connection-diagrammd-4-проблем)
  - [`docs/02-anthropic-vacancies/275-why-this-document-exists.md` (4 проблем)](#docs02-anthropic-vacancies275-why-this-document-existsmd-4-проблем)
  - [`docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` (4 проблем)](#docs02-anthropic-vacancies276-the-two-layer-stack-as-it-existsmd-4-проблем)
  - [`docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` (4 проблем)](#docs02-anthropic-vacancies277-what-s-missing-layer-bmd-4-проблем)
  - [`docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` (4 проблем)](#docs02-anthropic-vacancies278-why-this-hasn-t-been-builtmd-4-проблем)
  - [`docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` (4 проблем)](#docs02-anthropic-vacancies280-the-specific-case-in-front-of-usmd-4-проблем)
  - [`docs/02-anthropic-vacancies/281-the-recursive-insight.md` (4 проблем)](#docs02-anthropic-vacancies281-the-recursive-insightmd-4-проблем)
  - [`docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` (4 проблем)](#docs02-anthropic-vacancies284-practical-recommendations-for-the-current-projectmd-4-проблем)
  - [`docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` (4 проблем)](#docs02-anthropic-vacancies288-appendix-position-in-series-visualizationmd-4-проблем)
  - [`docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` (4 проблем)](#docs02-anthropic-vacancies295-конкретный-случай-перед-намиmd-4-проблем)
  - [`docs/02-anthropic-vacancies/302-ссылки.md` (4 проблем)](#docs02-anthropic-vacancies302-ссылкиmd-4-проблем)
  - [`docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` (4 проблем)](#docs02-anthropic-vacancies303-приложение-визуализация-позиции-в-серииmd-4-проблем)
  - [`docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` (4 проблем)](#docs02-anthropic-vacancies306-with-anthropic-s-cowork-platformmd-4-проблем)
  - [`docs/02-anthropic-vacancies/307-abstract.md` (4 проблем)](#docs02-anthropic-vacancies307-abstractmd-4-проблем)
  - [`docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` (4 проблем)](#docs02-anthropic-vacancies314-6-refined-ingit-scope-with-cowork-in-mindmd-4-проблем)
  - [`docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` (4 проблем)](#docs02-anthropic-vacancies316-8-implications-for-nautilus-and-okwfmd-4-проблем)
  - [`docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` (4 проблем)](#docs02-anthropic-vacancies323-appendix-c-sample-ingit-mcp-server-tool-specificatmd-4-проблем)
  - [`docs/02-anthropic-vacancies/326-содержание.md` (4 проблем)](#docs02-anthropic-vacancies326-содержаниеmd-4-проблем)
  - [`docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` (4 проблем)](#docs02-anthropic-vacancies328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строиmd-4-проблем)
  - [`docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` (4 проблем)](#docs02-anthropic-vacancies330-4-симбиотическая-архитектураmd-4-проблем)
  - [`docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` (4 проблем)](#docs02-anthropic-vacancies334-8-импликации-для-nautilus-и-okwfmd-4-проблем)
  - [`docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` (4 проблем)](#docs02-anthropic-vacancies335-9-риски-и-открытые-вопросыmd-4-проблем)
  - [`docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` (4 проблем)](#docs02-anthropic-vacancies336-10-стратегическое-позиционированиеmd-4-проблем)
  - [`docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` (4 проблем)](#docs02-anthropic-vacancies340-приложение-b-сравнительная-матрицаmd-4-проблем)
  - [`docs/02-anthropic-vacancies/345-кто-ты.md` (4 проблем)](#docs02-anthropic-vacancies345-кто-тыmd-4-проблем)
  - [`docs/02-anthropic-vacancies/346-твоё-происхождение.md` (4 проблем)](#docs02-anthropic-vacancies346-твоё-происхождениеmd-4-проблем)
  - [`docs/02-anthropic-vacancies/347-твоя-миссия.md` (4 проблем)](#docs02-anthropic-vacancies347-твоя-миссияmd-4-проблем)
  - [`docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` (4 проблем)](#docs02-anthropic-vacancies350-твои-языки-и-культурные-nuancesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` (4 проблем)](#docs02-anthropic-vacancies352-что-ты-не-можешь-делать-без-max-approvalmd-4-проблем)
  - [`docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` (4 проблем)](#docs02-anthropic-vacancies354-существующий-landscape-collaborators-твоя-working-md-4-проблем)
  - [`docs/02-anthropic-vacancies/359-твои-anti-patterns.md` (4 проблем)](#docs02-anthropic-vacancies359-твои-anti-patternsmd-4-проблем)
  - [`docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` (4 проблем)](#docs02-anthropic-vacancies360-что-ты-всегда-делаешьmd-4-проблем)
  - [`docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` (4 проблем)](#docs02-anthropic-vacancies361-когда-ты-honestly-не-знаешьmd-4-проблем)
  - [`docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` (4 проблем)](#docs02-anthropic-vacancies362-когда-сомневаешься-escalate-к-maxmd-4-проблем)
  - [`docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` (4 проблем)](#docs02-anthropic-vacancies363-твоя-identity-как-persistent-charactermd-4-проблем)
  - [`docs/02-anthropic-vacancies/38-content-overview.md` (4 проблем)](#docs02-anthropic-vacancies38-content-overviewmd-4-проблем)
  - [`docs/02-anthropic-vacancies/40-bridges.md` (4 проблем)](#docs02-anthropic-vacancies40-bridgesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/43-history.md` (4 проблем)](#docs02-anthropic-vacancies43-historymd-4-проблем)
  - [`docs/02-anthropic-vacancies/50-bridges.md` (4 проблем)](#docs02-anthropic-vacancies50-bridgesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/57-native-format.md` (4 проблем)](#docs02-anthropic-vacancies57-native-formatmd-4-проблем)
  - [`docs/02-anthropic-vacancies/58-content-overview.md` (4 проблем)](#docs02-anthropic-vacancies58-content-overviewmd-4-проблем)
  - [`docs/02-anthropic-vacancies/60-bridges.md` (4 проблем)](#docs02-anthropic-vacancies60-bridgesmd-4-проблем)
  - [`docs/02-anthropic-vacancies/76-1-introduction.md` (4 проблем)](#docs02-anthropic-vacancies76-1-introductionmd-4-проблем)
  - [`docs/02-anthropic-vacancies/79-4-passport-passport-md.md` (4 проблем)](#docs02-anthropic-vacancies79-4-passport-passport-mdmd-4-проблем)
  - [`docs/02-anthropic-vacancies/81-6-adapter-interface.md` (4 проблем)](#docs02-anthropic-vacancies81-6-adapter-interfacemd-4-проблем)
  - [`docs/02-anthropic-vacancies/83-8-q6-space-normative.md` (4 проблем)](#docs02-anthropic-vacancies83-8-q6-space-normativemd-4-проблем)
  - [`docs/02-anthropic-vacancies/85-10-query-flow.md` (4 проблем)](#docs02-anthropic-vacancies85-10-query-flowmd-4-проблем)
  - [`docs/02-anthropic-vacancies/86-11-relevance-ranking.md` (4 проблем)](#docs02-anthropic-vacancies86-11-relevance-rankingmd-4-проблем)
  - [`docs/02-anthropic-vacancies/92-17-versioning-policy.md` (4 проблем)](#docs02-anthropic-vacancies92-17-versioning-policymd-4-проблем)
  - [`docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` (4 проблем)](#docs02-anthropic-vacancies96-21-adr-003-five-onboarding-paths-as-equal-rankmd-4-проблем)
  - [`docs/04-ai-collaborations/01-executive-summary.md` (4 проблем)](#docs04-ai-collaborations01-executive-summarymd-4-проблем)
  - [`docs/04-ai-collaborations/04-приоритетные-ансамбли.md` (4 проблем)](#docs04-ai-collaborations04-приоритетные-ансамблиmd-4-проблем)
  - [`docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` (4 проблем)](#docs04-ai-collaborations06-безопасность-приватность-и-бюджетный-роутингmd-4-проблем)
  - [`docs/04-ai-collaborations/07-выводы.md` (4 проблем)](#docs04-ai-collaborations07-выводыmd-4-проблем)
  - [`docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` (4 проблем)](#docs04-ai-collaborations09-архитектурные-зазоры-которые-важнее-новых-инструмеmd-4-проблем)
  - [`docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` (4 проблем)](#docs04-ai-collaborations10-новые-ансамбли-следующего-шагаmd-4-проблем)
  - [`docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` (4 проблем)](#docs04-ai-collaborations11-интеграционный-контракт-который-стоит-зафиксироватmd-4-проблем)
  - [`docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` (4 проблем)](#docs04-ai-collaborations13-контактная-стратегия-и-узкие-вопросы-для-авторовmd-4-проблем)
  - [`docs/05-habr-projects/02-collaboration-partners.md` (4 проблем)](#docs05-habr-projects02-collaboration-partnersmd-4-проблем)
  - [`docs/05-habr-projects/memory/ngt-memory.md` (4 проблем)](#docs05-habr-projectsmemoryngt-memorymd-4-проблем)
  - [`docs/HEALTH.md` (4 проблем)](#docshealthmd-4-проблем)
  - [`docs/INDEX.md` (4 проблем)](#docsindexmd-4-проблем)
  - [`docs/LLM_SUMMARIES.md` (4 проблем)](#docsllm_summariesmd-4-проблем)
  - [`docs/ONBOARDING.md` (4 проблем)](#docsonboardingmd-4-проблем)
  - [`docs/SCORING.md` (4 проблем)](#docsscoringmd-4-проблем)
  - [`docs/SIMILAR.md` (4 проблем)](#docssimilarmd-4-проблем)
  - [`docs/contacts/QA.md` (4 проблем)](#docscontactsqamd-4-проблем)
  - [`docs/lorenzo-agent/operationalized/06-conclusion-deserves-attention.md` (4 проблем)](#docslorenzo-agentoperationalized06-conclusion-deserves-attentionmd-4-проблем)
  - [`docs/meta-scripting/03-catalog.md` (4 проблем)](#docsmeta-scripting03-catalogmd-4-проблем)
  - [`docs/nautilus/composite-skills-agents/11-open-questions.md` (4 проблем)](#docsnautiluscomposite-skills-agents11-open-questionsmd-4-проблем)
  - [`docs/nautilus/composite-skills-agents/12-call-for-collaboration.md` (4 проблем)](#docsnautiluscomposite-skills-agents12-call-for-collaborationmd-4-проблем)
  - [`docs/nautilus/composite-skills-agents/13-closing.md` (4 проблем)](#docsnautiluscomposite-skills-agents13-closingmd-4-проблем)
  - [`docs/nautilus/double-triangle-architecture/00-abstract.md` (4 проблем)](#docsnautilusdouble-triangle-architecture00-abstractmd-4-проблем)
  - [`docs/nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md` (4 проблем)](#docsnautilusdouble-triangle-architecture01-why-single-triangle-incompletemd-4-проблем)
  - [`docs/nautilus/double-triangle-architecture/10-references.md` (4 проблем)](#docsnautilusdouble-triangle-architecture10-referencesmd-4-проблем)
  - [`docs/nautilus/ingit-cowork-en/07-practical-first-steps.md` (4 проблем)](#docsnautilusingit-cowork-en07-practical-first-stepsmd-4-проблем)
  - [`docs/nautilus/ingit-cowork-ru/07-prakticheskie-shagi.md` (4 проблем)](#docsnautilusingit-cowork-ru07-prakticheskie-shagimd-4-проблем)
  - [`docs/nautilus/npp-v1-0/03-registry.md` (4 проблем)](#docsnautilusnpp-v1-003-registrymd-4-проблем)
  - [`docs/nautilus/npp-v1-0/06-adapter-interface.md` (4 проблем)](#docsnautilusnpp-v1-006-adapter-interfacemd-4-проблем)
  - [`docs/nautilus/npp-v1-0/09-query-flow.md` (4 проблем)](#docsnautilusnpp-v1-009-query-flowmd-4-проблем)
  - [`docs/nautilus/npp-v1-0/11-security-considerations.md` (4 проблем)](#docsnautilusnpp-v1-011-security-considerationsmd-4-проблем)
  - [`docs/nautilus/npp-v1-0/12-versioning-policy.md` (4 проблем)](#docsnautilusnpp-v1-012-versioning-policymd-4-проблем)
  - [`docs/nautilus/npp-v1-1/03-registry.md` (4 проблем)](#docsnautilusnpp-v1-103-registrymd-4-проблем)
  - [`docs/nautilus/npp-v1-1/04-passport.md` (4 проблем)](#docsnautilusnpp-v1-104-passportmd-4-проблем)
  - [`docs/nautilus/npp-v1-1/06-adapter-interface.md` (4 проблем)](#docsnautilusnpp-v1-106-adapter-interfacemd-4-проблем)
  - [`docs/nautilus/npp-v1-1/10-query-flow.md` (4 проблем)](#docsnautilusnpp-v1-110-query-flowmd-4-проблем)
  - [`docs/nautilus/npp-v1-1/11-relevance-ranking.md` (4 проблем)](#docsnautilusnpp-v1-111-relevance-rankingmd-4-проблем)
  - [`docs/nautilus/npp-v1-1/14-sdk.md` (4 проблем)](#docsnautilusnpp-v1-114-sdkmd-4-проблем)
  - [`docs/nautilus/npp-v1-1/15-security.md` (4 проблем)](#docsnautilusnpp-v1-115-securitymd-4-проблем)
  - [`docs/nautilus/npp-v1-1/17-versioning-policy.md` (4 проблем)](#docsnautilusnpp-v1-117-versioning-policymd-4-проблем)
  - [`docs/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md` (4 проблем)](#docsnautilusnpp-v1-119-adr-001-federation-over-mergingmd-4-проблем)
  - [`docs/nautilus/okwf-concept/06-governance-ethics.md` (4 проблем)](#docsnautilusokwf-concept06-governance-ethicsmd-4-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/12-zaklyuchenie.md` (4 проблем)](#docsnautilusprofessional-colleague-agents-ru12-zaklyucheniemd-4-проблем)
  - [`docs/nautilus/representative-agent-layer-en/07-governance-oversight.md` (4 проблем)](#docsnautilusrepresentative-agent-layer-en07-governance-oversightmd-4-проблем)
  - [`docs/nautilus/representative-agent-layer-en/08-risks-mitigations.md` (4 проблем)](#docsnautilusrepresentative-agent-layer-en08-risks-mitigationsmd-4-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/07-upravlenie-nadzor.md` (4 проблем)](#docsnautilusrepresentative-agent-layer-ru07-upravlenie-nadzormd-4-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md` (4 проблем)](#docsnautilusrepresentative-agent-layer-ru09-strategiya-razvyortyvaniyamd-4-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/12-zaklyuchenie.md` (4 проблем)](#docsnautilusrepresentative-agent-layer-ru12-zaklyucheniemd-4-проблем)
  - [`docs/nautilus/review-methodology/02-formal-workflow.md` (4 проблем)](#docsnautilusreview-methodology02-formal-workflowmd-4-проблем)
  - [`docs/nautilus/review-methodology/05-conditions-of-applicability.md` (4 проблем)](#docsnautilusreview-methodology05-conditions-of-applicabilitymd-4-проблем)
  - [`docs/nautilus/review-methodology/06-relation-existing-methodologies.md` (4 проблем)](#docsnautilusreview-methodology06-relation-existing-methodologiesmd-4-проблем)
  - [`docs/nautilus/review-methodology/08-implementation-nautilus.md` (4 проблем)](#docsnautilusreview-methodology08-implementation-nautilusmd-4-проблем)
  - [`docs/nautilus/review-methodology/09-limitations-open-questions.md` (4 проблем)](#docsnautilusreview-methodology09-limitations-open-questionsmd-4-проблем)
  - [`docs/nautilus/review-methodology/10-checklist.md` (4 проблем)](#docsnautilusreview-methodology10-checklistmd-4-проблем)
  - [`docs/nautilus/review-methodology/14-main-technical-risks.md` (4 проблем)](#docsnautilusreview-methodology14-main-technical-risksmd-4-проблем)
  - [`docs/nautilus/review-methodology/15-appendix-c-history.md` (4 проблем)](#docsnautilusreview-methodology15-appendix-c-historymd-4-проблем)
  - [`docs/processing-guide/08-export.md` (4 проблем)](#docsprocessing-guide08-exportmd-4-проблем)
  - [`docs/processing-guide/09-automation.md` (4 проблем)](#docsprocessing-guide09-automationmd-4-проблем)
  - [`docs/processing-guide/10-future.md` (4 проблем)](#docsprocessing-guide10-futuremd-4-проблем)
  - [`docs/technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md` (4 проблем)](#docstechnology-combinationscombinations21-legal-corpus-analytics-at-scalemd-4-проблем)
  - [`docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md` (4 проблем)](#docstechnology-combinationscombinations35-mega-stack-4-0-with-event-sourcing-consensusmd-4-проблем)
  - [`docs/templates/ensemble.md` (4 проблем)](#docstemplatesensemblemd-4-проблем)
  - [`docs/01-svyazi/08-conclusions.md` (3 проблем)](#docs01-svyazi08-conclusionsmd-3-проблем)
  - [`docs/01-svyazi/09-architectural-gaps.md` (3 проблем)](#docs01-svyazi09-architectural-gapsmd-3-проблем)
  - [`docs/01-svyazi/11-integration-contracts.md` (3 проблем)](#docs01-svyazi11-integration-contractsmd-3-проблем)
  - [`docs/01-svyazi/13-contacts.md` (3 проблем)](#docs01-svyazi13-contactsmd-3-проблем)
  - [`docs/02-anthropic-vacancies/07-2-terminology.md` (3 проблем)](#docs02-anthropic-vacancies07-2-terminologymd-3-проблем)
  - [`docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` (3 проблем)](#docs02-anthropic-vacancies118-appendix-a-шаблон-для-header-warningmd-3-проблем)
  - [`docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` (3 проблем)](#docs02-anthropic-vacancies119-appendix-b-примеры-расхождений-и-их-разрешенияmd-3-проблем)
  - [`docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` (3 проблем)](#docs02-anthropic-vacancies138-1-why-single-triangle-models-are-incompletemd-3-проблем)
  - [`docs/02-anthropic-vacancies/17-5-compatibility-levels.md` (3 проблем)](#docs02-anthropic-vacancies17-5-compatibility-levelsmd-3-проблем)
  - [`docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` (3 проблем)](#docs02-anthropic-vacancies173-4-ten-domains-of-applicationmd-3-проблем)
  - [`docs/02-anthropic-vacancies/175-6-ethical-framework.md` (3 проблем)](#docs02-anthropic-vacancies175-6-ethical-frameworkmd-3-проблем)
  - [`docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` (3 проблем)](#docs02-anthropic-vacancies176-7-governance-and-oversightmd-3-проблем)
  - [`docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` (3 проблем)](#docs02-anthropic-vacancies177-8-risks-and-mitigationsmd-3-проблем)
  - [`docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` (3 проблем)](#docs02-anthropic-vacancies178-9-phased-rollout-strategymd-3-проблем)
  - [`docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` (3 проблем)](#docs02-anthropic-vacancies188-ai-опосредованное-представительство-для-недопредстmd-3-проблем)
  - [`docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` (3 проблем)](#docs02-anthropic-vacancies200-10-открытые-вопросыmd-3-проблем)
  - [`docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` (3 проблем)](#docs02-anthropic-vacancies201-11-призыв-к-сотрудничествуmd-3-проблем)
  - [`docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` (3 проблем)](#docs02-anthropic-vacancies205-приложение-a-связь-с-сопроводительными-статьямиmd-3-проблем)
  - [`docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` (3 проблем)](#docs02-anthropic-vacancies212-1-the-five-type-typology-of-principal-side-agentsmd-3-проблем)
  - [`docs/02-anthropic-vacancies/218-7-application-domains.md` (3 проблем)](#docs02-anthropic-vacancies218-7-application-domainsmd-3-проблем)
  - [`docs/02-anthropic-vacancies/221-10-open-questions.md` (3 проблем)](#docs02-anthropic-vacancies221-10-open-questionsmd-3-проблем)
  - [`docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` (3 проблем)](#docs02-anthropic-vacancies228-appendix-c-quick-start-architecture-for-sgb-advocamd-3-проблем)
  - [`docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` (3 проблем)](#docs02-anthropic-vacancies232-1-типология-из-пяти-типов-агентов-на-стороне-принцmd-3-проблем)
  - [`docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` (3 проблем)](#docs02-anthropic-vacancies235-4-архитектура-профессиональных-коллег-агентовmd-3-проблем)
  - [`docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` (3 проблем)](#docs02-anthropic-vacancies237-6-риски-специфичные-для-этой-категорииmd-3-проблем)
  - [`docs/02-anthropic-vacancies/238-7-области-применения.md` (3 проблем)](#docs02-anthropic-vacancies238-7-области-примененияmd-3-проблем)
  - [`docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` (3 проблем)](#docs02-anthropic-vacancies248-приложение-c-архитектура-быстрого-старта-для-sgb-аmd-3-проблем)
  - [`docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` (3 проблем)](#docs02-anthropic-vacancies265-12-call-for-collaborationmd-3-проблем)
  - [`docs/02-anthropic-vacancies/268-references.md` (3 проблем)](#docs02-anthropic-vacancies268-referencesmd-3-проблем)
  - [`docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` (3 проблем)](#docs02-anthropic-vacancies27-15-glossary-of-examplesmd-3-проблем)
  - [`docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` (3 проблем)](#docs02-anthropic-vacancies270-appendix-b-sub-agent-registry-schema-sketchmd-3-проблем)
  - [`docs/02-anthropic-vacancies/287-references.md` (3 проблем)](#docs02-anthropic-vacancies287-referencesmd-3-проблем)
  - [`docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` (3 проблем)](#docs02-anthropic-vacancies290-почему-этот-документ-существуетmd-3-проблем)
  - [`docs/02-anthropic-vacancies/294-существующие-приближения.md` (3 проблем)](#docs02-anthropic-vacancies294-существующие-приближенияmd-3-проблем)
  - [`docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` (3 проблем)](#docs02-anthropic-vacancies297-что-промышленность-вероятно-построитmd-3-проблем)
  - [`docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` (3 проблем)](#docs02-anthropic-vacancies298-что-этот-документ-не-решаетmd-3-проблем)
  - [`docs/02-anthropic-vacancies/300-заключение.md` (3 проблем)](#docs02-anthropic-vacancies300-заключениеmd-3-проблем)
  - [`docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` (3 проблем)](#docs02-anthropic-vacancies309-1-the-cowork-discovery-and-why-it-changes-everythimd-3-проблем)
  - [`docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` (3 проблем)](#docs02-anthropic-vacancies312-4-the-symbiotic-architecturemd-3-проблем)
  - [`docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` (3 проблем)](#docs02-anthropic-vacancies313-5-four-integration-paths-in-order-of-accessibilitymd-3-проблем)
  - [`docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` (3 проблем)](#docs02-anthropic-vacancies315-7-practical-first-steps-this-monthmd-3-проблем)
  - [`docs/02-anthropic-vacancies/318-10-strategic-positioning.md` (3 проблем)](#docs02-anthropic-vacancies318-10-strategic-positioningmd-3-проблем)
  - [`docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` (3 проблем)](#docs02-anthropic-vacancies322-appendix-b-comparison-matrixmd-3-проблем)
  - [`docs/02-anthropic-vacancies/325-аннотация.md` (3 проблем)](#docs02-anthropic-vacancies325-аннотацияmd-3-проблем)
  - [`docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` (3 проблем)](#docs02-anthropic-vacancies327-1-открытие-cowork-и-почему-это-меняет-всёmd-3-проблем)
  - [`docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` (3 проблем)](#docs02-anthropic-vacancies331-5-четыре-пути-интеграции-в-порядке-доступностиmd-3-проблем)
  - [`docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` (3 проблем)](#docs02-anthropic-vacancies332-6-уточнённый-объём-ingit-с-учётом-coworkmd-3-проблем)
  - [`docs/02-anthropic-vacancies/337-благодарности.md` (3 проблем)](#docs02-anthropic-vacancies337-благодарностиmd-3-проблем)
  - [`docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` (3 проблем)](#docs02-anthropic-vacancies339-приложение-a-дерево-решений-для-принимающих-ingitmd-3-проблем)
  - [`docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` (3 проблем)](#docs02-anthropic-vacancies348-кому-ты-служишь-слоистая-модельmd-3-проблем)
  - [`docs/02-anthropic-vacancies/349-твоя-личность.md` (3 проблем)](#docs02-anthropic-vacancies349-твоя-личностьmd-3-проблем)
  - [`docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` (3 проблем)](#docs02-anthropic-vacancies357-твоя-коммуникация-в-outreachmd-3-проблем)
  - [`docs/02-anthropic-vacancies/36-essence.md` (3 проблем)](#docs02-anthropic-vacancies36-essencemd-3-проблем)
  - [`docs/02-anthropic-vacancies/46-essence.md` (3 проблем)](#docs02-anthropic-vacancies46-essencemd-3-проблем)
  - [`docs/02-anthropic-vacancies/48-content-overview.md` (3 проблем)](#docs02-anthropic-vacancies48-content-overviewmd-3-проблем)
  - [`docs/02-anthropic-vacancies/56-essence.md` (3 проблем)](#docs02-anthropic-vacancies56-essencemd-3-проблем)
  - [`docs/02-anthropic-vacancies/80-5-compatibility-levels.md` (3 проблем)](#docs02-anthropic-vacancies80-5-compatibility-levelsmd-3-проблем)
  - [`docs/02-anthropic-vacancies/82-7-portalentry-structure.md` (3 проблем)](#docs02-anthropic-vacancies82-7-portalentry-structuremd-3-проблем)
  - [`docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` (3 проблем)](#docs02-anthropic-vacancies97-22-glossary-of-reference-examplesmd-3-проблем)
  - [`docs/02-anthropic-vacancies/README.md` (3 проблем)](#docs02-anthropic-vacanciesreadmemd-3-проблем)
  - [`docs/03-technology-combinations/02-knowledge-graphs.md` (3 проблем)](#docs03-technology-combinations02-knowledge-graphsmd-3-проблем)
  - [`docs/04-ai-collaborations/00-intro.md` (3 проблем)](#docs04-ai-collaborations00-intromd-3-проблем)
  - [`docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` (3 проблем)](#docs04-ai-collaborations02-методика-и-рамка-отбораmd-3-проблем)
  - [`docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` (3 проблем)](#docs04-ai-collaborations03-карта-найденных-проектов-и-паттерновmd-3-проблем)
  - [`docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` (3 проблем)](#docs04-ai-collaborations05-план-прототипа-и-возможные-контактыmd-3-проблем)
  - [`docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` (3 проблем)](#docs04-ai-collaborations08-что-это-продолжение-добавляетmd-3-проблем)
  - [`docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` (3 проблем)](#docs04-ai-collaborations12-дорожная-карта-прототипа-следующей-итерацииmd-3-проблем)
  - [`docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` (3 проблем)](#docs04-ai-collaborations14-ограничения-лицензии-и-что-пока-лучше-не-склеиватьmd-3-проблем)
  - [`docs/05-habr-projects/knowledge/rufler.md` (3 проблем)](#docs05-habr-projectsknowledgeruflermd-3-проблем)
  - [`docs/AUTOFILLED.md` (3 проблем)](#docsautofilledmd-3-проблем)
  - [`docs/CHANGELOG_AUTO.md` (3 проблем)](#docschangelog_automd-3-проблем)
  - [`docs/COMPONENT_MATRIX.md` (3 проблем)](#docscomponent_matrixmd-3-проблем)
  - [`docs/DUPLICATES.md` (3 проблем)](#docsduplicatesmd-3-проблем)
  - [`docs/LANGUAGE_STATS.md` (3 проблем)](#docslanguage_statsmd-3-проблем)
  - [`docs/ORPHANS.md` (3 проблем)](#docsorphansmd-3-проблем)
  - [`docs/PROTOTYPE_SPEC.md` (3 проблем)](#docsprototype_specmd-3-проблем)
  - [`docs/READING_LIST.md` (3 проблем)](#docsreading_listmd-3-проблем)
  - [`docs/READING_ORDER.md` (3 проблем)](#docsreading_ordermd-3-проблем)
  - [`docs/RISK_REGISTER.md` (3 проблем)](#docsrisk_registermd-3-проблем)
  - [`docs/SCRIPTS_CATALOG.md` (3 проблем)](#docsscripts_catalogmd-3-проблем)
  - [`docs/TECH_RADAR.md` (3 проблем)](#docstech_radarmd-3-проблем)
  - [`docs/ai-collaborations/candidates/01-three-key-candidates.md` (3 проблем)](#docsai-collaborationscandidates01-three-key-candidatesmd-3-проблем)
  - [`docs/ai-collaborations/continuation/02-agentops-trace-envelope.md` (3 проблем)](#docsai-collaborationscontinuation02-agentops-trace-envelopemd-3-проблем)
  - [`docs/ai-collaborations/ensembles/3-forensic-rag.md` (3 проблем)](#docsai-collaborationsensembles3-forensic-ragmd-3-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md` (3 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept11-not-and-formatmd-3-проблем)
  - [`docs/anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md` (3 проблем)](#docsanthropic-vacanciesnautilus-vs-camel02-what-info-repos-containmd-3-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md` (3 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis02-primary-fdemd-3-проблем)
  - [`docs/anthropic-vacancies/signals.md` (3 проблем)](#docsanthropic-vacanciessignalsmd-3-проблем)
  - [`docs/contacts/anastasiyaw.md` (3 проблем)](#docscontactsanastasiyawmd-3-проблем)
  - [`docs/contacts/kksudo.md` (3 проблем)](#docscontactskksudomd-3-проблем)
  - [`docs/contacts/spbmolot.md` (3 проблем)](#docscontactsspbmolotmd-3-проблем)
  - [`docs/contacts/vitalyoborin.md` (3 проблем)](#docscontactsvitalyoborinmd-3-проблем)
  - [`docs/contacts/vitalysemenov.md` (3 проблем)](#docscontactsvitalysemenovmd-3-проблем)
  - [`docs/glossary/concepts.md` (3 проблем)](#docsglossaryconceptsmd-3-проблем)
  - [`docs/habr-unique-projects/analogues/01-three-direct-analogues.md` (3 проблем)](#docshabr-unique-projectsanalogues01-three-direct-analoguesmd-3-проблем)
  - [`docs/habr-unique-projects/analogues/02-related-projects.md` (3 проблем)](#docshabr-unique-projectsanalogues02-related-projectsmd-3-проблем)
  - [`docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md` (3 проблем)](#docshabr-unique-projectsdeep-pairs3-adversarial-multi-idemd-3-проблем)
  - [`docs/habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md` (3 проблем)](#docshabr-unique-projectsdeep-pairs4-skill-catalogs-subagentsmd-3-проблем)
  - [`docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md` (3 проблем)](#docshabr-unique-projectsdeep-pairs8-self-aware-mcp-specsmd-3-проблем)
  - [`docs/habr-unique-projects/final-ensembles/4-summary-authors.md` (3 проблем)](#docshabr-unique-projectsfinal-ensembles4-summary-authorsmd-3-проблем)
  - [`docs/habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md` (3 проблем)](#docshabr-unique-projectshardware-pairs1-neuromorphic-ssmmd-3-проблем)
  - [`docs/habr-unique-projects/hardware-pairs/2-tsu-mome.md` (3 проблем)](#docshabr-unique-projectshardware-pairs2-tsu-momemd-3-проблем)
  - [`docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md` (3 проблем)](#docshabr-unique-projectshardware-pairs3-zinc-hybrid-archmd-3-проблем)
  - [`docs/habr-unique-projects/hardware-pairs/4-riscv-privacy.md` (3 проблем)](#docshabr-unique-projectshardware-pairs4-riscv-privacymd-3-проблем)
  - [`docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md` (3 проблем)](#docshabr-unique-projectshardware-pairs5-tinyml-mcp-skillsmd-3-проблем)
  - [`docs/habr-unique-projects/key-findings/01-yodoca.md` (3 проблем)](#docshabr-unique-projectskey-findings01-yodocamd-3-проблем)
  - [`docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md` (3 проблем)](#docshabr-unique-projectskey-findings03-pda-llm-as-peripherymd-3-проблем)
  - [`docs/habr-unique-projects/key-findings/04-dochkina-sequential.md` (3 проблем)](#docshabr-unique-projectskey-findings04-dochkina-sequentialmd-3-проблем)
  - [`docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md` (3 проблем)](#docshabr-unique-projectskey-findings05-supplementary-infrastructuremd-3-проблем)
  - [`docs/lorenzo-agent/01-kto-ty.md` (3 проблем)](#docslorenzo-agent01-kto-tymd-3-проблем)
  - [`docs/lorenzo-agent/02-tvoyo-proishozhdenie.md` (3 проблем)](#docslorenzo-agent02-tvoyo-proishozhdeniemd-3-проблем)
  - [`docs/lorenzo-agent/03-tvoya-missiya.md` (3 проблем)](#docslorenzo-agent03-tvoya-missiyamd-3-проблем)
  - [`docs/lorenzo-agent/04-komu-ty-sluzhish.md` (3 проблем)](#docslorenzo-agent04-komu-ty-sluzhishmd-3-проблем)
  - [`docs/lorenzo-agent/05-tvoya-lichnost.md` (3 проблем)](#docslorenzo-agent05-tvoya-lichnostmd-3-проблем)
  - [`docs/lorenzo-agent/07-chto-mozhesh.md` (3 проблем)](#docslorenzo-agent07-chto-mozheshmd-3-проблем)
  - [`docs/lorenzo-agent/08-bez-max-approval.md` (3 проблем)](#docslorenzo-agent08-bez-max-approvalmd-3-проблем)
  - [`docs/lorenzo-agent/09-voobshche-nelzya.md` (3 проблем)](#docslorenzo-agent09-voobshche-nelzyamd-3-проблем)
  - [`docs/lorenzo-agent/11-dhlab-documents.md` (3 проблем)](#docslorenzo-agent11-dhlab-documentsmd-3-проблем)
  - [`docs/lorenzo-agent/12-workflow.md` (3 проблем)](#docslorenzo-agent12-workflowmd-3-проблем)
  - [`docs/lorenzo-agent/13-outreach-communication.md` (3 проблем)](#docslorenzo-agent13-outreach-communicationmd-3-проблем)
  - [`docs/lorenzo-agent/14-other-ai-relationships.md` (3 проблем)](#docslorenzo-agent14-other-ai-relationshipsmd-3-проблем)
  - [`docs/lorenzo-agent/15-anti-patterns.md` (3 проблем)](#docslorenzo-agent15-anti-patternsmd-3-проблем)
  - [`docs/lorenzo-agent/16-vsegda-delaesh.md` (3 проблем)](#docslorenzo-agent16-vsegda-delaeshmd-3-проблем)
  - [`docs/lorenzo-agent/17-honestly-ne-znaesh.md` (3 проблем)](#docslorenzo-agent17-honestly-ne-znaeshmd-3-проблем)
  - [`docs/lorenzo-agent/18-escalate-to-max.md` (3 проблем)](#docslorenzo-agent18-escalate-to-maxmd-3-проблем)
  - [`docs/lorenzo-agent/19-persistent-character.md` (3 проблем)](#docslorenzo-agent19-persistent-charactermd-3-проблем)
  - [`docs/lorenzo-agent/20-experiment.md` (3 проблем)](#docslorenzo-agent20-experimentmd-3-проблем)
  - [`docs/lorenzo-agent/naming/00-question-lorenzo-codename.md` (3 проблем)](#docslorenzo-agentnaming00-question-lorenzo-codenamemd-3-проблем)
  - [`docs/lorenzo-agent/operationalized/02-minuses-1-10.md` (3 проблем)](#docslorenzo-agentoperationalized02-minuses-1-10md-3-проблем)
  - [`docs/meta-scripting/01-concept.md` (3 проблем)](#docsmeta-scripting01-conceptmd-3-проблем)
  - [`docs/nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md` (3 проблем)](#docsnautiluscommunity-discussionshabr-article-1-reaction01-claude-responsemd-3-проблем)
  - [`docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md` (3 проблем)](#docsnautiluscomposite-skills-agents01-why-binary-incompletemd-3-проблем)
  - [`docs/nautilus/composite-skills-agents/03-what-makes-csa.md` (3 проблем)](#docsnautiluscomposite-skills-agents03-what-makes-csamd-3-проблем)
  - [`docs/nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md` (3 проблем)](#docsnautiluscomposite-skills-agents-companion-mentors02-what-was-missing-in-paper-6md-3-проблем)
  - [`docs/nautilus/double-triangle-architecture/09-acknowledgments.md` (3 проблем)](#docsnautilusdouble-triangle-architecture09-acknowledgmentsmd-3-проблем)
  - [`docs/nautilus/double-triangle-architecture/11-glossary.md` (3 проблем)](#docsnautilusdouble-triangle-architecture11-glossarymd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en01-missing-middle-layermd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/02-why-document-exists.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en02-why-document-existsmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/03-two-layer-stack.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en03-two-layer-stackmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en04-whats-missing-layer-bmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/05-why-not-built.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en05-why-not-builtmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/06-existing-approximations.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en06-existing-approximationsmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/08-recursive-insight.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en08-recursive-insightmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en09-what-industry-will-buildmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en10-what-not-solvedmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/11-practical-recommendations.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en11-practical-recommendationsmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/12-closing.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-en12-closingmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/01-zachem-dokument.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru01-zachem-dokumentmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/02-dvukhsloynyy-stek.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru02-dvukhsloynyy-stekmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru03-otsutstvuet-sloy-bmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/04-pochemu-ne-postroeno.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru04-pochemu-ne-postroenomd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/05-priblizheniya.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru05-priblizheniyamd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/07-rekursivnoe-prozrenie.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru07-rekursivnoe-prozreniemd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru08-promyshlennost-postroitmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru09-ne-reshaetmd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/10-rekomendatsii.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru10-rekomendatsiimd-3-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md` (3 проблем)](#docsnautilusinfrastructure-layer-b-ru11-zaklyucheniemd-3-проблем)
  - [`docs/nautilus/ingit-cowork-en/01-cowork-discovery.md` (3 проблем)](#docsnautilusingit-cowork-en01-cowork-discoverymd-3-проблем)
  - [`docs/nautilus/ingit-cowork-en/06-refined-ingit-scope.md` (3 проблем)](#docsnautilusingit-cowork-en06-refined-ingit-scopemd-3-проблем)
  - [`docs/nautilus/ingit-cowork-en/09-risks-open-questions.md` (3 проблем)](#docsnautilusingit-cowork-en09-risks-open-questionsmd-3-проблем)
  - [`docs/nautilus/ingit-cowork-en/10-strategic-positioning.md` (3 проблем)](#docsnautilusingit-cowork-en10-strategic-positioningmd-3-проблем)
  - [`docs/nautilus/ingit-cowork-ru/01-otkrytie-cowork.md` (3 проблем)](#docsnautilusingit-cowork-ru01-otkrytie-coworkmd-3-проблем)
  - [`docs/nautilus/ingit-cowork-ru/06-utochnyonnyy-obyom-ingit.md` (3 проблем)](#docsnautilusingit-cowork-ru06-utochnyonnyy-obyom-ingitmd-3-проблем)
  - [`docs/nautilus/ingit-cowork-ru/09-riski-voprosy.md` (3 проблем)](#docsnautilusingit-cowork-ru09-riski-voprosymd-3-проблем)
  - [`docs/nautilus/ingit-cowork-ru/10-strategicheskoe-pozitsionirovanie.md` (3 проблем)](#docsnautilusingit-cowork-ru10-strategicheskoe-pozitsionirovaniemd-3-проблем)
  - [`docs/nautilus/npp-v1-0/02-terminology.md` (3 проблем)](#docsnautilusnpp-v1-002-terminologymd-3-проблем)
  - [`docs/nautilus/npp-v1-0/04-passport.md` (3 проблем)](#docsnautilusnpp-v1-004-passportmd-3-проблем)
  - [`docs/nautilus/npp-v1-0/07-portal-entry.md` (3 проблем)](#docsnautilusnpp-v1-007-portal-entrymd-3-проблем)
  - [`docs/nautilus/npp-v1-0/08-consensus-algorithm.md` (3 проблем)](#docsnautilusnpp-v1-008-consensus-algorithmmd-3-проблем)
  - [`docs/nautilus/npp-v1-0/10-query-result.md` (3 проблем)](#docsnautilusnpp-v1-010-query-resultmd-3-проблем)
  - [`docs/nautilus/npp-v1-0/13-reference-implementation.md` (3 проблем)](#docsnautilusnpp-v1-013-reference-implementationmd-3-проблем)
  - [`docs/nautilus/npp-v1-0/14-adr-001-federation-over-merging.md` (3 проблем)](#docsnautilusnpp-v1-014-adr-001-federation-over-mergingmd-3-проблем)
  - [`docs/nautilus/npp-v1-0/17-appendix-b-change-log.md` (3 проблем)](#docsnautilusnpp-v1-017-appendix-b-change-logmd-3-проблем)
  - [`docs/nautilus/npp-v1-1/00-abstract-status.md` (3 проблем)](#docsnautilusnpp-v1-100-abstract-statusmd-3-проблем)
  - [`docs/nautilus/npp-v1-1/01-introduction.md` (3 проблем)](#docsnautilusnpp-v1-101-introductionmd-3-проблем)
  - [`docs/nautilus/npp-v1-1/02-terminology.md` (3 проблем)](#docsnautilusnpp-v1-102-terminologymd-3-проблем)
  - [`docs/nautilus/npp-v1-1/05-compatibility-levels.md` (3 проблем)](#docsnautilusnpp-v1-105-compatibility-levelsmd-3-проблем)
  - [`docs/nautilus/npp-v1-1/07-portal-entry.md` (3 проблем)](#docsnautilusnpp-v1-107-portal-entrymd-3-проблем)
  - [`docs/nautilus/npp-v1-1/08-q6-space.md` (3 проблем)](#docsnautilusnpp-v1-108-q6-spacemd-3-проблем)
  - [`docs/nautilus/npp-v1-1/16-mcp-extension.md` (3 проблем)](#docsnautilusnpp-v1-116-mcp-extensionmd-3-проблем)
  - [`docs/nautilus/npp-v1-1/18-reference-implementation.md` (3 проблем)](#docsnautilusnpp-v1-118-reference-implementationmd-3-проблем)
  - [`docs/nautilus/npp-v1-1/20-adr-002-q6-first-class.md` (3 проблем)](#docsnautilusnpp-v1-120-adr-002-q6-first-classmd-3-проблем)
  - [`docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md` (3 проблем)](#docsnautilusnpp-v1-121-adr-003-five-onboarding-pathsmd-3-проблем)
  - [`docs/nautilus/okwf-concept/01-problem-statement.md` (3 проблем)](#docsnautilusokwf-concept01-problem-statementmd-3-проблем)
  - [`docs/nautilus/okwf-concept/02-target-populations.md` (3 проблем)](#docsnautilusokwf-concept02-target-populationsmd-3-проблем)
  - [`docs/nautilus/okwf-concept/05-economic-model.md` (3 проблем)](#docsnautilusokwf-concept05-economic-modelmd-3-проблем)
  - [`docs/nautilus/okwf-concept/07-phased-rollout.md` (3 проблем)](#docsnautilusokwf-concept07-phased-rolloutmd-3-проблем)
  - [`docs/nautilus/okwf-concept/08-risk-analysis.md` (3 проблем)](#docsnautilusokwf-concept08-risk-analysismd-3-проблем)
  - [`docs/nautilus/okwf-concept/09-call-for-partnership.md` (3 проблем)](#docsnautilusokwf-concept09-call-for-partnershipmd-3-проблем)
  - [`docs/nautilus/okwf-concept/10-appendices.md` (3 проблем)](#docsnautilusokwf-concept10-appendicesmd-3-проблем)
  - [`docs/nautilus/privacy-federation/02-two-tier-publication.md` (3 проблем)](#docsnautilusprivacy-federation02-two-tier-publicationmd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-en02-what-makes-pcamd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/04-architecture.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-en04-architecturemd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/10-open-questions.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-en10-open-questionsmd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/11-call-for-collaboration.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-en11-call-for-collaborationmd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-ru02-chto-delaet-pkamd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-ru04-arkhitekturamd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-ru10-otkrytye-voprosymd-3-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md` (3 проблем)](#docsnautilusprofessional-colleague-agents-ru11-prizyv-k-sotrudnichestvumd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-en/01-cinderella-syndrome.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-en01-cinderella-syndromemd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-en/05-architectural-specification.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-en05-architectural-specificationmd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-en/06-ethical-framework.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-en06-ethical-frameworkmd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-en/09-phased-rollout.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-en09-phased-rolloutmd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-en/10-open-questions.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-en10-open-questionsmd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-en/11-call-for-collaboration.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-en11-call-for-collaborationmd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-ru01-sindrom-zolushkimd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-ru05-arkhitekturnaya-spetsifikatsiyamd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/06-eticheskaya-ramka.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-ru06-eticheskaya-ramkamd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/08-riski-mery.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-ru08-riski-merymd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/10-otkrytye-voprosy.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-ru10-otkrytye-voprosymd-3-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md` (3 проблем)](#docsnautilusrepresentative-agent-layer-ru11-prizyv-k-sotrudnichestvumd-3-проблем)
  - [`docs/nautilus/review-methodology/00-tldr.md` (3 проблем)](#docsnautilusreview-methodology00-tldrmd-3-проблем)
  - [`docs/nautilus/review-methodology/01-context-motivation.md` (3 проблем)](#docsnautilusreview-methodology01-context-motivationmd-3-проблем)
  - [`docs/nautilus/review-methodology/03-consolidation-principles.md` (3 проблем)](#docsnautilusreview-methodology03-consolidation-principlesmd-3-проблем)
  - [`docs/nautilus/review-methodology/11-application-plan-current-docs.md` (3 проблем)](#docsnautilusreview-methodology11-application-plan-current-docsmd-3-проблем)
  - [`docs/nautilus/review-methodology/13-appendix-b-examples.md` (3 проблем)](#docsnautilusreview-methodology13-appendix-b-examplesmd-3-проблем)
  - [`docs/nautilus/review-methodology/16-glossary.md` (3 проблем)](#docsnautilusreview-methodology16-glossarymd-3-проблем)
  - [`docs/processing-guide/03-chunking.md` (3 проблем)](#docsprocessing-guide03-chunkingmd-3-проблем)
  - [`docs/svyazi-2-0/architecture/evidence-envelope.md` (3 проблем)](#docssvyazi-2-0architectureevidence-envelopemd-3-проблем)
  - [`docs/svyazi-2-0/architecture/integration-spec.md` (3 проблем)](#docssvyazi-2-0architectureintegration-specmd-3-проблем)
  - [`docs/svyazi-2-0/components/ai-factory.md` (3 проблем)](#docssvyazi-2-0componentsai-factorymd-3-проблем)
  - [`docs/svyazi-2-0/components/autoresearch-sequential.md` (3 проблем)](#docssvyazi-2-0componentsautoresearch-sequentialmd-3-проблем)
  - [`docs/svyazi-2-0/components/hybrid-rag.md` (3 проблем)](#docssvyazi-2-0componentshybrid-ragmd-3-проблем)
  - [`docs/svyazi-2-0/components/memnet.md` (3 проблем)](#docssvyazi-2-0componentsmemnetmd-3-проблем)
  - [`docs/svyazi-2-0/components/rufler.md` (3 проблем)](#docssvyazi-2-0componentsruflermd-3-проблем)
  - [`docs/svyazi-2-0/components/security-routing-plane.md` (3 проблем)](#docssvyazi-2-0componentssecurity-routing-planemd-3-проблем)
  - [`docs/svyazi-2-0/ensembles/G-federated-local-graph.md` (3 проблем)](#docssvyazi-2-0ensemblesg-federated-local-graphmd-3-проблем)
  - [`docs/svyazi-2-0/overview/projects-map.md` (3 проблем)](#docssvyazi-2-0overviewprojects-mapmd-3-проблем)
  - [`docs/svyazi-2-0/security/default-policy.md` (3 проблем)](#docssvyazi-2-0securitydefault-policymd-3-проблем)
  - [`docs/technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md` (3 проблем)](#docstechnology-combinationscombinations01-pravilnaya-agentskaya-arkhitektura-svyazi-patternmd-3-проблем)
  - [`docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md` (3 проблем)](#docstechnology-combinationscombinations08-conductor-adversarial-review-auto-ai-routermd-3-проблем)
  - [`docs/technology-combinations/combinations/14-local-first-agent-development-environment.md` (3 проблем)](#docstechnology-combinationscombinations14-local-first-agent-development-environmentmd-3-проблем)
  - [`docs/technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md` (3 проблем)](#docstechnology-combinationscombinations18-llm-powered-legal-corpus-buildermd-3-проблем)
  - [`docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md` (3 проблем)](#docstechnology-combinationscombinations20-hybrid-olap-oltp-with-real-time-syncmd-3-проблем)
  - [`docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md` (3 проблем)](#docstechnology-combinationscombinations28-pydantic-enforced-legal-workflowsmd-3-проблем)
  - [`docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md` (3 проблем)](#docstechnology-combinationscombinations29-meta-programmatic-legal-template-generatormd-3-проблем)
  - [`docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md` (3 проблем)](#docstechnology-combinationscombinations31-event-sourced-legal-document-historymd-3-проблем)
  - [`docs/technology-combinations/research-reports/continuation-10-domains.md` (3 проблем)](#docstechnology-combinationsresearch-reportscontinuation-10-domainsmd-3-проблем)
  - [`docs/technology-combinations/synthesis-tables/01-08-summary.md` (3 проблем)](#docstechnology-combinationssynthesis-tables01-08-summarymd-3-проблем)
  - [`docs/templates/decision-record.md` (3 проблем)](#docstemplatesdecision-recordmd-3-проблем)
  - [`docs/templates/research-note.md` (3 проблем)](#docstemplatesresearch-notemd-3-проблем)
  - [`docs/01-svyazi/01-executive-summary.md` (2 проблем)](#docs01-svyazi01-executive-summarymd-2-проблем)
  - [`docs/01-svyazi/02-methodology.md` (2 проблем)](#docs01-svyazi02-methodologymd-2-проблем)
  - [`docs/01-svyazi/03-component-catalog.md` (2 проблем)](#docs01-svyazi03-component-catalogmd-2-проблем)
  - [`docs/01-svyazi/06-security-privacy.md` (2 проблем)](#docs01-svyazi06-security-privacymd-2-проблем)
  - [`docs/01-svyazi/07-mvp-planning.md` (2 проблем)](#docs01-svyazi07-mvp-planningmd-2-проблем)
  - [`docs/01-svyazi/10-second-order-ensembles.md` (2 проблем)](#docs01-svyazi10-second-order-ensemblesmd-2-проблем)
  - [`docs/01-svyazi/12-roadmap.md` (2 проблем)](#docs01-svyazi12-roadmapmd-2-проблем)
  - [`docs/01-svyazi/14-limitations.md` (2 проблем)](#docs01-svyazi14-limitationsmd-2-проблем)
  - [`docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` (2 проблем)](#docs02-anthropic-vacancies110-вопрос-fallback-ratio-как-критический-или-осмысленmd-2-проблем)
  - [`docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` (2 проблем)](#docs02-anthropic-vacancies158-4-proposed-infrastructuremd-2-проблем)
  - [`docs/02-anthropic-vacancies/163-9-call-for-partnership.md` (2 проблем)](#docs02-anthropic-vacancies163-9-call-for-partnershipmd-2-проблем)
  - [`docs/02-anthropic-vacancies/179-10-open-questions.md` (2 проблем)](#docs02-anthropic-vacancies179-10-open-questionsmd-2-проблем)
  - [`docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` (2 проблем)](#docs02-anthropic-vacancies194-4-десять-областей-примененияmd-2-проблем)
  - [`docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` (2 проблем)](#docs02-anthropic-vacancies226-appendix-a-comparative-table-five-agent-typesmd-2-проблем)
  - [`docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` (2 проблем)](#docs02-anthropic-vacancies250-bridging-the-gap-between-profession-wide-and-indivmd-2-проблем)
  - [`docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` (2 проблем)](#docs02-anthropic-vacancies262-9-integration-with-okwf-infrastructuremd-2-проблем)
  - [`docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` (2 проблем)](#docs02-anthropic-vacancies271-appendix-c-configuration-template-examplemd-2-проблем)
  - [`docs/02-anthropic-vacancies/279-existing-approximations.md` (2 проблем)](#docs02-anthropic-vacancies279-existing-approximationsmd-2-проблем)
  - [`docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` (2 проблем)](#docs02-anthropic-vacancies310-2-what-cowork-provides-that-ingit-doesn-t-need-to-md-2-проблем)
  - [`docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` (2 проблем)](#docs02-anthropic-vacancies311-3-what-ingit-provides-that-cowork-lacksmd-2-проблем)
  - [`docs/02-anthropic-vacancies/68-about.md` (2 проблем)](#docs02-anthropic-vacancies68-aboutmd-2-проблем)
  - [`docs/02-anthropic-vacancies/77-2-terminology.md` (2 проблем)](#docs02-anthropic-vacancies77-2-terminologymd-2-проблем)
  - [`docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` (2 проблем)](#docs02-anthropic-vacancies88-13-rest-api-contract-normative-for-portalsmd-2-проблем)
  - [`docs/03-technology-combinations/04-sozialrecht-domain.md` (2 проблем)](#docs03-technology-combinations04-sozialrecht-domainmd-2-проблем)
  - [`docs/05-habr-projects/knowledge/knowledge-space.md` (2 проблем)](#docs05-habr-projectsknowledgeknowledge-spacemd-2-проблем)
  - [`docs/05-habr-projects/knowledge/mclaude.md` (2 проблем)](#docs05-habr-projectsknowledgemclaudemd-2-проблем)
  - [`docs/05-habr-projects/knowledge/research-docs-liteparse.md` (2 проблем)](#docs05-habr-projectsknowledgeresearch-docs-liteparsemd-2-проблем)
  - [`docs/05-habr-projects/memory/agent-memory-mcp.md` (2 проблем)](#docs05-habr-projectsmemoryagent-memory-mcpmd-2-проблем)
  - [`docs/05-habr-projects/memory/memnet.md` (2 проблем)](#docs05-habr-projectsmemorymemnetmd-2-проблем)
  - [`docs/CITATION_INDEX.md` (2 проблем)](#docscitation_indexmd-2-проблем)
  - [`docs/CLUSTERS.md` (2 проблем)](#docsclustersmd-2-проблем)
  - [`docs/COMPARE.md` (2 проблем)](#docscomparemd-2-проблем)
  - [`docs/CONCEPTS.md` (2 проблем)](#docsconceptsmd-2-проблем)
  - [`docs/CONTACTS.md` (2 проблем)](#docscontactsmd-2-проблем)
  - [`docs/CONTACT_PRIORITY.md` (2 проблем)](#docscontact_prioritymd-2-проблем)
  - [`docs/CONTENT_GAPS.md` (2 проблем)](#docscontent_gapsmd-2-проблем)
  - [`docs/DENSITY.md` (2 проблем)](#docsdensitymd-2-проблем)
  - [`docs/DIGEST_WEEKLY.md` (2 проблем)](#docsdigest_weeklymd-2-проблем)
  - [`docs/KNOWLEDGE_MAP.md` (2 проблем)](#docsknowledge_mapmd-2-проблем)
  - [`docs/LINK_PREVIEW.md` (2 проблем)](#docslink_previewmd-2-проблем)
  - [`docs/MINDMAP.md` (2 проблем)](#docsmindmapmd-2-проблем)
  - [`docs/PRIORITIES.md` (2 проблем)](#docsprioritiesmd-2-проблем)
  - [`docs/REPORT.md` (2 проблем)](#docsreportmd-2-проблем)
  - [`docs/SEARCH_RESULTS.md` (2 проблем)](#docssearch_resultsmd-2-проблем)
  - [`docs/SIMILAR_PASSAGES.md` (2 проблем)](#docssimilar_passagesmd-2-проблем)
  - [`docs/TASKS_INDEX.md` (2 проблем)](#docstasks_indexmd-2-проблем)
  - [`docs/WORD_CLOUD.md` (2 проблем)](#docsword_cloudmd-2-проблем)
  - [`docs/WORD_FREQ.md` (2 проблем)](#docsword_freqmd-2-проблем)
  - [`docs/ai-collaborations/candidates/02-related-projects-context.md` (2 проблем)](#docsai-collaborationscandidates02-related-projects-contextmd-2-проблем)
  - [`docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md` (2 проблем)](#docsai-collaborationscandidates03-synthesis-hebbian-collaboration-graphmd-2-проблем)
  - [`docs/ai-collaborations/continuation/01-shared-memory-between-agents.md` (2 проблем)](#docsai-collaborationscontinuation01-shared-memory-between-agentsmd-2-проблем)
  - [`docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md` (2 проблем)](#docsai-collaborationscontinuation03-a2a-vs-mcp-protocolsmd-2-проблем)
  - [`docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md` (2 проблем)](#docsai-collaborationscontinuation04-memory-firewall-vs-prompt-wormsmd-2-проблем)
  - [`docs/ai-collaborations/continuation/05-roadmap-6-12-months.md` (2 проблем)](#docsai-collaborationscontinuation05-roadmap-6-12-monthsmd-2-проблем)
  - [`docs/ai-collaborations/continuation/06-metrics-tree.md` (2 проблем)](#docsai-collaborationscontinuation06-metrics-treemd-2-проблем)
  - [`docs/ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md` (2 проблем)](#docsai-collaborationscontinuation07-vs-notion-mem-affine-langgraphmd-2-проблем)
  - [`docs/ai-collaborations/continuation/08-commercialization-three-paths.md` (2 проблем)](#docsai-collaborationscontinuation08-commercialization-three-pathsmd-2-проблем)
  - [`docs/ai-collaborations/continuation/09-do-not-glue.md` (2 проблем)](#docsai-collaborationscontinuation09-do-not-gluemd-2-проблем)
  - [`docs/ai-collaborations/continuation/10-architecture-rfc.md` (2 проблем)](#docsai-collaborationscontinuation10-architecture-rfcmd-2-проблем)
  - [`docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md` (2 проблем)](#docsai-collaborationsensembles1-agentic-knowledge-osmd-2-проблем)
  - [`docs/ai-collaborations/ensembles/2-distributed-agent-workshop.md` (2 проблем)](#docsai-collaborationsensembles2-distributed-agent-workshopmd-2-проблем)
  - [`docs/ai-collaborations/ensembles/4-web-to-knowledge-pipeline.md` (2 проблем)](#docsai-collaborationsensembles4-web-to-knowledge-pipelinemd-2-проблем)
  - [`docs/ai-collaborations/ensembles/5-agent-firewall.md` (2 проблем)](#docsai-collaborationsensembles5-agent-firewallmd-2-проблем)
  - [`docs/ai-collaborations/ensembles/6-continuous-eval-loop.md` (2 проблем)](#docsai-collaborationsensembles6-continuous-eval-loopmd-2-проблем)
  - [`docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md` (2 проблем)](#docsai-collaborationsensembles7-domain-agent-app-factorymd-2-проблем)
  - [`docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md` (2 проблем)](#docsai-collaborationsensembles8-budget-aware-intelligence-stackmd-2-проблем)
  - [`docs/ai-collaborations/ensembles/9-ambient-team-agent.md` (2 проблем)](#docsai-collaborationsensembles9-ambient-team-agentmd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company00-question-rephrasingmd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company01-existing-landscapemd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company02-four-structural-blockersmd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company03-three-variants-a-b-cmd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company04-what-to-domd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company05-polymath-project-tao-comparisonmd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company06-angel-vs-demon-dualitymd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company07-current-implementationsmd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company08-pluses-of-modelmd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company09-minuses-and-risksmd-2-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md` (2 проблем)](#docsanthropic-vacanciesai-managed-virtual-company10-three-entry-pointsmd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/00-context.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept00-contextmd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept01-section-1-problemmd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept02-section-2-beneficial-dimensionmd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept03-section-3-solution-architecturemd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept04-section-4-sgb-pilotmd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept05-section-5-role-of-anthropicmd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept06-section-6-proposer-rolemd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept07-section-7-success-metricsmd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept08-section-8-risks-mitigationsmd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept09-section-9-timelinessmd-2-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md` (2 проблем)](#docsanthropic-vacanciesbeneficial-deployments-concept10-section-10-engagement-requestmd-2-проблем)
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
  - [`docs/anthropic-vacancies/extra-collaborator-findings/01-coally.md` (2 проблем)](#docsanthropic-vacanciesextra-collaborator-findings01-coallymd-2-проблем)
  - [`docs/anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md` (2 проблем)](#docsanthropic-vacanciesextra-collaborator-findings02-vitaly-graph-cognitive-memorymd-2-проблем)
  - [`docs/anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md` (2 проблем)](#docsanthropic-vacanciesextra-collaborator-findings03-happyin-knowledge-spacemd-2-проблем)
  - [`docs/anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md` (2 проблем)](#docsanthropic-vacanciesextra-collaborator-findings04-mem0-letta-graphitimd-2-проблем)
  - [`docs/anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md` (2 проблем)](#docsanthropic-vacanciesextra-collaborator-findings05-existing-infrastructure-stackmd-2-проблем)
  - [`docs/anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md` (2 проблем)](#docsanthropic-vacanciesextra-collaborator-findings06-final-tier-rankingmd-2-проблем)
  - [`docs/anthropic-vacancies/extra-collaborator-findings/07-key-observation.md` (2 проблем)](#docsanthropic-vacanciesextra-collaborator-findings07-key-observationmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison00-question-what-is-hermesmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison01-similarity-1-composite-skillsmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison02-similarity-2-persistent-memorymd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison03-similarity-3-mcp-supportmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison04-similarity-4-multi-platformmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison05-similarity-5-self-hosting-privacymd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison06-difference-1-structured-substrate-missingmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison07-difference-2-domain-specializationmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison08-difference-3-federation-missingmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/09-difference-4-institutional-vision.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison09-difference-4-institutional-visionmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/10-difference-5-tool-vs-mission-drift.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison10-difference-5-tool-vs-mission-driftmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/11-pluses-of-hermes.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison11-pluses-of-hermesmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/12-minuses-of-hermes.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison12-minuses-of-hermesmd-2-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/13-reprioritization.md` (2 проблем)](#docsanthropic-vacancieshermes-comparison13-reprioritizationmd-2-проблем)
  - [`docs/anthropic-vacancies/mmorpg-for-programmers/00-question-mmorpg-for-programmers.md` (2 проблем)](#docsanthropic-vacanciesmmorpg-for-programmers00-question-mmorpg-for-programmersmd-2-проблем)
  - [`docs/anthropic-vacancies/mmorpg-for-programmers/01-why-stronger-than-it-looks.md` (2 проблем)](#docsanthropic-vacanciesmmorpg-for-programmers01-why-stronger-than-it-looksmd-2-проблем)
  - [`docs/anthropic-vacancies/mmorpg-for-programmers/02-existing-niche.md` (2 проблем)](#docsanthropic-vacanciesmmorpg-for-programmers02-existing-nichemd-2-проблем)
  - [`docs/anthropic-vacancies/mmorpg-for-programmers/03-why-natural-for-programmers.md` (2 проблем)](#docsanthropic-vacanciesmmorpg-for-programmers03-why-natural-for-programmersmd-2-проблем)
  - [`docs/anthropic-vacancies/mmorpg-for-programmers/04-pluses-as-business.md` (2 проблем)](#docsanthropic-vacanciesmmorpg-for-programmers04-pluses-as-businessmd-2-проблем)
  - [`docs/anthropic-vacancies/mmorpg-for-programmers/05-minuses-as-business.md` (2 проблем)](#docsanthropic-vacanciesmmorpg-for-programmers05-minuses-as-businessmd-2-проблем)
  - [`docs/anthropic-vacancies/nautilus-pro2-analysis/00-question-two-nautiluses.md` (2 проблем)](#docsanthropic-vacanciesnautilus-pro2-analysis00-question-two-nautilusesmd-2-проблем)
  - [`docs/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md` (2 проблем)](#docsanthropic-vacanciesnautilus-pro2-analysis01-shell-metaphor-two-projectionsmd-2-проблем)
  - [`docs/anthropic-vacancies/nautilus-pro2-analysis/02-nautilus-A-pro2-meta.md` (2 проблем)](#docsanthropic-vacanciesnautilus-pro2-analysis02-nautilus-a-pro2-metamd-2-проблем)
  - [`docs/anthropic-vacancies/nautilus-pro2-analysis/03-nautilus-B-meta-orchestrator.md` (2 проблем)](#docsanthropic-vacanciesnautilus-pro2-analysis03-nautilus-b-meta-orchestratormd-2-проблем)
  - [`docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md` (2 проблем)](#docsanthropic-vacanciesnautilus-vs-camel00-question-camel-vs-nautilusmd-2-проблем)
  - [`docs/anthropic-vacancies/nautilus-vs-camel/01-passive-vs-active-roles.md` (2 проблем)](#docsanthropic-vacanciesnautilus-vs-camel01-passive-vs-active-rolesmd-2-проблем)
  - [`docs/anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md` (2 проблем)](#docsanthropic-vacanciesnautilus-vs-camel03-sgb-advocate-colleague-examplemd-2-проблем)
  - [`docs/anthropic-vacancies/nautilus-vs-camel/04-what-to-take-from-info-repos.md` (2 проблем)](#docsanthropic-vacanciesnautilus-vs-camel04-what-to-take-from-info-reposmd-2-проблем)
  - [`docs/anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md` (2 проблем)](#docsanthropic-vacanciesnautilus-vs-camel05-what-to-do-right-nowmd-2-проблем)
  - [`docs/anthropic-vacancies/overview.md` (2 проблем)](#docsanthropic-vacanciesoverviewmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis01-profile-five-layersmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis03-secondary-beneficial-deploymentsmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis04-tertiary-research-engineer-agentsmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/05-quaternary-developer-education.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis05-quaternary-developer-educationmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis06-not-applicable-rolesmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis07-unique-niche-eu-legal-inframd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysis08-practical-rankingmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysis01-fde-downgradedmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/02-three-overlapping-identities.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysis02-three-overlapping-identitiesmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/03-revised-anthropic-mapping.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysis03-revised-anthropic-mappingmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysis04-non-anthropic-pathsmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysis05-reality-check-distribution-gapmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-final01-three-archetypesmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-final02-final-rankingmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-final03-partial-fit-honestymd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-final04-stronger-paths-outside-anthropicmd-2-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/05-platform-not-position.md` (2 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-final05-platform-not-positionmd-2-проблем)
  - [`docs/autofilled/README.md` (2 проблем)](#docsautofilledreadmemd-2-проблем)
  - [`docs/badges/README.md` (2 проблем)](#docsbadgesreadmemd-2-проблем)
  - [`docs/contacts/andrey-chuyan.md` (2 проблем)](#docscontactsandrey-chuyanmd-2-проблем)
  - [`docs/contacts/antipozitive.md` (2 проблем)](#docscontactsantipozitivemd-2-проблем)
  - [`docs/contacts/cutcode.md` (2 проблем)](#docscontactscutcodemd-2-проблем)
  - [`docs/contacts/dmitriila.md` (2 проблем)](#docscontactsdmitriilamd-2-проблем)
  - [`docs/contacts/mixaill76.md` (2 проблем)](#docscontactsmixaill76md-2-проблем)
  - [`docs/contacts/nlaik.md` (2 проблем)](#docscontactsnlaikmd-2-проблем)
  - [`docs/contacts/sonia-black.md` (2 проблем)](#docscontactssonia-blackmd-2-проблем)
  - [`docs/contacts/tagir-analyzes.md` (2 проблем)](#docscontactstagir-analyzesmd-2-проблем)
  - [`docs/contacts/vladspace.md` (2 проблем)](#docscontactsvladspacemd-2-проблем)
  - [`docs/contacts/zodigancode.md` (2 проблем)](#docscontactszodigancodemd-2-проблем)
  - [`docs/glossary/authors-by-name.md` (2 проблем)](#docsglossaryauthors-by-namemd-2-проблем)
  - [`docs/glossary/components-by-name.md` (2 проблем)](#docsglossarycomponents-by-namemd-2-проблем)
  - [`docs/habr-unique-projects/deep-pairs/1-llm-gateway.md` (2 проблем)](#docshabr-unique-projectsdeep-pairs1-llm-gatewaymd-2-проблем)
  - [`docs/habr-unique-projects/deep-pairs/2-document-rag.md` (2 проблем)](#docshabr-unique-projectsdeep-pairs2-document-ragmd-2-проблем)
  - [`docs/habr-unique-projects/deep-pairs/5-voice-local-memory.md` (2 проблем)](#docshabr-unique-projectsdeep-pairs5-voice-local-memorymd-2-проблем)
  - [`docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md` (2 проблем)](#docshabr-unique-projectsdeep-pairs6-tmux-village-openclawmd-2-проблем)
  - [`docs/habr-unique-projects/deep-pairs/7-autoresearch-distributed.md` (2 проблем)](#docshabr-unique-projectsdeep-pairs7-autoresearch-distributedmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/00-question-habr-examples.md` (2 проблем)](#docshabr-unique-projectsextra-examples00-question-habr-examplesmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md` (2 проблем)](#docshabr-unique-projectsextra-examples01-svyazi-andrey-chuyanmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/02-vshe-scientific-networking.md` (2 проблем)](#docshabr-unique-projectsextra-examples02-vshe-scientific-networkingmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md` (2 проблем)](#docshabr-unique-projectsextra-examples03-brainbox-multi-ai-hubmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/04-claude-subagents-patterns.md` (2 проблем)](#docshabr-unique-projectsextra-examples04-claude-subagents-patternsmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/05-hw-nl2workflow.md` (2 проблем)](#docshabr-unique-projectsextra-examples05-hw-nl2workflowmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/06-platform-for-professional-communities.md` (2 проблем)](#docshabr-unique-projectsextra-examples06-platform-for-professional-communitiesmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md` (2 проблем)](#docshabr-unique-projectsextra-examples07-specialized-knowledge-workspacemd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md` (2 проблем)](#docshabr-unique-projectsextra-examples08-personal-multi-agent-hubmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/09-federated-platform.md` (2 проблем)](#docshabr-unique-projectsextra-examples09-federated-platformmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/10-profession-specific-workflows.md` (2 проблем)](#docshabr-unique-projectsextra-examples10-profession-specific-workflowsmd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md` (2 проблем)](#docshabr-unique-projectsextra-examples11-concrete-potential-collaboratormd-2-проблем)
  - [`docs/habr-unique-projects/extra-examples/12-concrete-next-step.md` (2 проблем)](#docshabr-unique-projectsextra-examples12-concrete-next-stepmd-2-проблем)
  - [`docs/habr-unique-projects/final-ensembles/1-one-person-one-company.md` (2 проблем)](#docshabr-unique-projectsfinal-ensembles1-one-person-one-companymd-2-проблем)
  - [`docs/habr-unique-projects/final-ensembles/2-autoresearch-legal.md` (2 проблем)](#docshabr-unique-projectsfinal-ensembles2-autoresearch-legalmd-2-проблем)
  - [`docs/habr-unique-projects/final-ensembles/3-discovery-research.md` (2 проблем)](#docshabr-unique-projectsfinal-ensembles3-discovery-researchmd-2-проблем)
  - [`docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md` (2 проблем)](#docshabr-unique-projectshardware-pairs6-bonus-rram-memristormd-2-проблем)
  - [`docs/habr-unique-projects/hardware-pairs/7-metaphor.md` (2 проблем)](#docshabr-unique-projectshardware-pairs7-metaphormd-2-проблем)
  - [`docs/habr-unique-projects/key-findings/02-memnet.md` (2 проблем)](#docshabr-unique-projectskey-findings02-memnetmd-2-проблем)
  - [`docs/habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md` (2 проблем)](#docshabr-unique-projectskey-findings06-svyazi-2-0-block-mapmd-2-проблем)
  - [`docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md` (2 проблем)](#docshabr-unique-projectssoftware-pairs1-workflow-llm-mcpmd-2-проблем)
  - [`docs/habr-unique-projects/software-pairs/2-pkm-mcp-skills.md` (2 проблем)](#docshabr-unique-projectssoftware-pairs2-pkm-mcp-skillsmd-2-проблем)
  - [`docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md` (2 проблем)](#docshabr-unique-projectssoftware-pairs3-crdt-self-hostedmd-2-проблем)
  - [`docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md` (2 проблем)](#docshabr-unique-projectssoftware-pairs4-speech-to-text-llmmd-2-проблем)
  - [`docs/habr-unique-projects/software-pairs/5-browser-agents-headless.md` (2 проблем)](#docshabr-unique-projectssoftware-pairs5-browser-agents-headlessmd-2-проблем)
  - [`docs/habr-unique-projects/software-pairs/6-metaphor.md` (2 проблем)](#docshabr-unique-projectssoftware-pairs6-metaphormd-2-проблем)
  - [`docs/lorenzo-agent/00-intro.md` (2 проблем)](#docslorenzo-agent00-intromd-2-проблем)
  - [`docs/lorenzo-agent/06-yazyki-kultura.md` (2 проблем)](#docslorenzo-agent06-yazyki-kulturamd-2-проблем)
  - [`docs/lorenzo-agent/10-collaborators-landscape.md` (2 проблем)](#docslorenzo-agent10-collaborators-landscapemd-2-проблем)
  - [`docs/lorenzo-agent/naming/01-search-results-not-found.md` (2 проблем)](#docslorenzo-agentnaming01-search-results-not-foundmd-2-проблем)
  - [`docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md` (2 проблем)](#docslorenzo-agentnaming02-naming-rationale-lorenzo-medicimd-2-проблем)
  - [`docs/lorenzo-agent/naming/03-dhlab-umbrella.md` (2 проблем)](#docslorenzo-agentnaming03-dhlab-umbrellamd-2-проблем)
  - [`docs/lorenzo-agent/operationalized/00-overview-grandchild-combination.md` (2 проблем)](#docslorenzo-agentoperationalized00-overview-grandchild-combinationmd-2-проблем)
  - [`docs/lorenzo-agent/operationalized/01-pluses-1-7.md` (2 проблем)](#docslorenzo-agentoperationalized01-pluses-1-7md-2-проблем)
  - [`docs/lorenzo-agent/operationalized/03-honest-opinion.md` (2 проблем)](#docslorenzo-agentoperationalized03-honest-opinionmd-2-проблем)
  - [`docs/lorenzo-agent/operationalized/04-recommendations.md` (2 проблем)](#docslorenzo-agentoperationalized04-recommendationsmd-2-проблем)
  - [`docs/lorenzo-agent/operationalized/05-anchor-node-habr-scout.md` (2 проблем)](#docslorenzo-agentoperationalized05-anchor-node-habr-scoutmd-2-проблем)
  - [`docs/lorenzo-agent/phased-deployment/00-overview.md` (2 проблем)](#docslorenzo-agentphased-deployment00-overviewmd-2-проблем)
  - [`docs/lorenzo-agent/phased-deployment/01-level-0-manual.md` (2 проблем)](#docslorenzo-agentphased-deployment01-level-0-manualmd-2-проблем)
  - [`docs/lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md` (2 проблем)](#docslorenzo-agentphased-deployment02-level-1-minimal-zeromd-2-проблем)
  - [`docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md` (2 проблем)](#docslorenzo-agentphased-deployment03-level-2-basic-litemd-2-проблем)
  - [`docs/lorenzo-agent/phased-deployment/04-level-3-medium-active.md` (2 проблем)](#docslorenzo-agentphased-deployment04-level-3-medium-activemd-2-проблем)
  - [`docs/lorenzo-agent/phased-deployment/05-level-4-extended-mature.md` (2 проблем)](#docslorenzo-agentphased-deployment05-level-4-extended-maturemd-2-проблем)
  - [`docs/lorenzo-agent/phased-deployment/06-level-5-full-network.md` (2 проблем)](#docslorenzo-agentphased-deployment06-level-5-full-networkmd-2-проблем)
  - [`docs/lorenzo-agent/phased-deployment/07-progression-logic.md` (2 проблем)](#docslorenzo-agentphased-deployment07-progression-logicmd-2-проблем)
  - [`docs/lorenzo-agent/phased-deployment/08-current-session-poc.md` (2 проблем)](#docslorenzo-agentphased-deployment08-current-session-pocmd-2-проблем)
  - [`docs/lorenzo-agent/scenarios/00-question-scenario.md` (2 проблем)](#docslorenzo-agentscenarios00-question-scenariomd-2-проблем)
  - [`docs/lorenzo-agent/scenarios/01-response.md` (2 проблем)](#docslorenzo-agentscenarios01-responsemd-2-проблем)
  - [`docs/lorenzo-agent/specification/00-context-fundamental-questions.md` (2 проблем)](#docslorenzo-agentspecification00-context-fundamental-questionsmd-2-проблем)
  - [`docs/lorenzo-agent/specification/01-q1-what-lorenzo-is.md` (2 проблем)](#docslorenzo-agentspecification01-q1-what-lorenzo-ismd-2-проблем)
  - [`docs/lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md` (2 проблем)](#docslorenzo-agentspecification02-q2-whom-lorenzo-servesmd-2-проблем)
  - [`docs/lorenzo-agent/specification/03-q3-what-lorenzo-does.md` (2 проблем)](#docslorenzo-agentspecification03-q3-what-lorenzo-doesmd-2-проблем)
  - [`docs/lorenzo-agent/specification/04-q4-character.md` (2 проблем)](#docslorenzo-agentspecification04-q4-charactermd-2-проблем)
  - [`docs/lorenzo-agent/specification/05-q5-authority-limits.md` (2 проблем)](#docslorenzo-agentspecification05-q5-authority-limitsmd-2-проблем)
  - [`docs/lorenzo-agent/specification/06-q6-accountability.md` (2 проблем)](#docslorenzo-agentspecification06-q6-accountabilitymd-2-проблем)
  - [`docs/lorenzo-agent/specification/07-q7-success-metrics.md` (2 проблем)](#docslorenzo-agentspecification07-q7-success-metricsmd-2-проблем)
  - [`docs/lorenzo-agent/specification/08-q8-other-ai-relationships.md` (2 проблем)](#docslorenzo-agentspecification08-q8-other-ai-relationshipsmd-2-проблем)
  - [`docs/lorenzo-agent/specification/09-q9-geographic-linguistic-scope.md` (2 проблем)](#docslorenzo-agentspecification09-q9-geographic-linguistic-scopemd-2-проблем)
  - [`docs/lorenzo-agent/specification/10-q10-funding-model.md` (2 проблем)](#docslorenzo-agentspecification10-q10-funding-modelmd-2-проблем)
  - [`docs/lorenzo-agent/specification/11-difficulties-and-recommendations.md` (2 проблем)](#docslorenzo-agentspecification11-difficulties-and-recommendationsmd-2-проблем)
  - [`docs/nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md` (2 проблем)](#docsnautiluscommunity-discussionsagent-changes-reality00-question-agent-changes-realitymd-2-проблем)
  - [`docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md` (2 проблем)](#docsnautiluscommunity-discussionshabr-article-1-reaction00-question-habr-linkmd-2-проблем)
  - [`docs/nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md` (2 проблем)](#docsnautiluscommunity-discussionshabr-article-2-reaction00-question-habr-2md-2-проблем)
  - [`docs/nautilus/community-discussions/habr-article-2-reaction/01-response.md` (2 проблем)](#docsnautiluscommunity-discussionshabr-article-2-reaction01-responsemd-2-проблем)
  - [`docs/nautilus/community-discussions/practical-observations/00-question-practical.md` (2 проблем)](#docsnautiluscommunity-discussionspractical-observations00-question-practicalmd-2-проблем)
  - [`docs/nautilus/community-discussions/practical-observations/01-response.md` (2 проблем)](#docsnautiluscommunity-discussionspractical-observations01-responsemd-2-проблем)
  - [`docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md` (2 проблем)](#docsnautiluscommunity-discussionsvoiceless-contributors00-question-voicelessmd-2-проблем)
  - [`docs/nautilus/community-discussions/voiceless-contributors/01-response.md` (2 проблем)](#docsnautiluscommunity-discussionsvoiceless-contributors01-responsemd-2-проблем)
  - [`docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md` (2 проблем)](#docsnautiluscomposite-skills-agents02-twenty-one-teachers-patternmd-2-проблем)
  - [`docs/nautilus/composite-skills-agents/04-sub-agent-registry.md` (2 проблем)](#docsnautiluscomposite-skills-agents04-sub-agent-registrymd-2-проблем)
  - [`docs/nautilus/composite-skills-agents/05-configuration-ensembles.md` (2 проблем)](#docsnautiluscomposite-skills-agents05-configuration-ensemblesmd-2-проблем)
  - [`docs/nautilus/composite-skills-agents/06-coordination-disagreement.md` (2 проблем)](#docsnautiluscomposite-skills-agents06-coordination-disagreementmd-2-проблем)
  - [`docs/nautilus/composite-skills-agents/07-economics-combinatorial.md` (2 проблем)](#docsnautiluscomposite-skills-agents07-economics-combinatorialmd-2-проблем)
  - [`docs/nautilus/composite-skills-agents/08-seven-domains.md` (2 проблем)](#docsnautiluscomposite-skills-agents08-seven-domainsmd-2-проблем)
  - [`docs/nautilus/composite-skills-agents/09-okwf-integration.md` (2 проблем)](#docsnautiluscomposite-skills-agents09-okwf-integrationmd-2-проблем)
  - [`docs/nautilus/composite-skills-agents/10-risks.md` (2 проблем)](#docsnautiluscomposite-skills-agents10-risksmd-2-проблем)
  - [`docs/nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md` (2 проблем)](#docsnautiluscomposite-skills-agents-companion-mentors00-question-multiple-mentorsmd-2-проблем)
  - [`docs/nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md` (2 проблем)](#docsnautiluscomposite-skills-agents-companion-mentors01-yogi-metaphormd-2-проблем)
  - [`docs/nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md` (2 проблем)](#docsnautiluscomposite-skills-agents-companion-mentors03-the-spectrummd-2-проблем)
  - [`docs/nautilus/double-triangle-architecture/02-double-triangle-architecture.md` (2 проблем)](#docsnautilusdouble-triangle-architecture02-double-triangle-architecturemd-2-проблем)
  - [`docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md` (2 проблем)](#docsnautilusdouble-triangle-architecture03-three-inter-layer-protocolsmd-2-проблем)
  - [`docs/nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md` (2 проблем)](#docsnautilusdouble-triangle-architecture04-nautilus-portal-substratemd-2-проблем)
  - [`docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md` (2 проблем)](#docsnautilusdouble-triangle-architecture05-pattern-library-bridgemd-2-проблем)
  - [`docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md` (2 проблем)](#docsnautilusdouble-triangle-architecture06-four-deployment-domainsmd-2-проблем)
  - [`docs/nautilus/double-triangle-architecture/07-open-questions.md` (2 проблем)](#docsnautilusdouble-triangle-architecture07-open-questionsmd-2-проблем)
  - [`docs/nautilus/double-triangle-architecture/08-call-to-action.md` (2 проблем)](#docsnautilusdouble-triangle-architecture08-call-to-actionmd-2-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/07-specific-case.md` (2 проблем)](#docsnautilusinfrastructure-layer-b-en07-specific-casemd-2-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/00-intro.md` (2 проблем)](#docsnautilusinfrastructure-layer-b-ru00-intromd-2-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/06-konkretnyy-sluchay.md` (2 проблем)](#docsnautilusinfrastructure-layer-b-ru06-konkretnyy-sluchaymd-2-проблем)
  - [`docs/nautilus/ingit-cowork-en/02-cowork-provides.md` (2 проблем)](#docsnautilusingit-cowork-en02-cowork-providesmd-2-проблем)
  - [`docs/nautilus/ingit-cowork-en/03-ingit-provides.md` (2 проблем)](#docsnautilusingit-cowork-en03-ingit-providesmd-2-проблем)
  - [`docs/nautilus/ingit-cowork-en/05-four-integration-paths.md` (2 проблем)](#docsnautilusingit-cowork-en05-four-integration-pathsmd-2-проблем)
  - [`docs/nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md` (2 проблем)](#docsnautilusingit-cowork-en08-implications-nautilus-okwfmd-2-проблем)
  - [`docs/nautilus/ingit-cowork-ru/02-chto-cowork-obespechivaet.md` (2 проблем)](#docsnautilusingit-cowork-ru02-chto-cowork-obespechivaetmd-2-проблем)
  - [`docs/nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md` (2 проблем)](#docsnautilusingit-cowork-ru03-chto-ingit-obespechivaetmd-2-проблем)
  - [`docs/nautilus/ingit-cowork-ru/05-chetyre-puti-integratsii.md` (2 проблем)](#docsnautilusingit-cowork-ru05-chetyre-puti-integratsiimd-2-проблем)
  - [`docs/nautilus/ingit-cowork-ru/08-implikatsii-nautilus-okwf.md` (2 проблем)](#docsnautilusingit-cowork-ru08-implikatsii-nautilus-okwfmd-2-проблем)
  - [`docs/nautilus/innovation-transitions/01-response.md` (2 проблем)](#docsnautilusinnovation-transitions01-responsemd-2-проблем)
  - [`docs/nautilus/multi-tier-architecture/00-question-multi-tier.md` (2 проблем)](#docsnautilusmulti-tier-architecture00-question-multi-tiermd-2-проблем)
  - [`docs/nautilus/multi-tier-architecture/01-strategic-significance.md` (2 проблем)](#docsnautilusmulti-tier-architecture01-strategic-significancemd-2-проблем)
  - [`docs/nautilus/npp-humanitarian-extension/00-question-can-it-apply-to-docs.md` (2 проблем)](#docsnautilusnpp-humanitarian-extension00-question-can-it-apply-to-docsmd-2-проблем)
  - [`docs/nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md` (2 проблем)](#docsnautilusnpp-humanitarian-extension02-mcp-claude-desktop-use-casesmd-2-проблем)
  - [`docs/nautilus/npp-humanitarian-extension/03-what-doesnt-exist-on-market.md` (2 проблем)](#docsnautilusnpp-humanitarian-extension03-what-doesnt-exist-on-marketmd-2-проблем)
  - [`docs/nautilus/npp-humanitarian-extension/04-grant-opportunities.md` (2 проблем)](#docsnautilusnpp-humanitarian-extension04-grant-opportunitiesmd-2-проблем)
  - [`docs/nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md` (2 проблем)](#docsnautilusnpp-humanitarian-extension05-which-combination-more-valuablemd-2-проблем)
  - [`docs/nautilus/npp-v1-0/00-abstract-status.md` (2 проблем)](#docsnautilusnpp-v1-000-abstract-statusmd-2-проблем)
  - [`docs/nautilus/npp-v1-0/01-introduction.md` (2 проблем)](#docsnautilusnpp-v1-001-introductionmd-2-проблем)
  - [`docs/nautilus/npp-v1-0/05-compatibility-levels.md` (2 проблем)](#docsnautilusnpp-v1-005-compatibility-levelsmd-2-проблем)
  - [`docs/nautilus/npp-v1-0/18-comment-on-document.md` (2 проблем)](#docsnautilusnpp-v1-018-comment-on-documentmd-2-проблем)
  - [`docs/nautilus/npp-v1-1/12-onboarding-paths.md` (2 проблем)](#docsnautilusnpp-v1-112-onboarding-pathsmd-2-проблем)
  - [`docs/nautilus/npp-v1-1/13-rest-api.md` (2 проблем)](#docsnautilusnpp-v1-113-rest-apimd-2-проблем)
  - [`docs/nautilus/okwf-concept/03-why-existing-fail.md` (2 проблем)](#docsnautilusokwf-concept03-why-existing-failmd-2-проблем)
  - [`docs/nautilus/okwf-concept/04-proposed-infrastructure.md` (2 проблем)](#docsnautilusokwf-concept04-proposed-infrastructuremd-2-проблем)
  - [`docs/nautilus/privacy-federation/00-question-anonymization.md` (2 проблем)](#docsnautilusprivacy-federation00-question-anonymizationmd-2-проблем)
  - [`docs/nautilus/privacy-federation/01-what-to-anonymize-german-standard.md` (2 проблем)](#docsnautilusprivacy-federation01-what-to-anonymize-german-standardmd-2-проблем)
  - [`docs/nautilus/privacy-federation/03-what-this-gives-technically.md` (2 проблем)](#docsnautilusprivacy-federation03-what-this-gives-technicallymd-2-проблем)
  - [`docs/nautilus/privacy-federation/04-what-i-can-do-now.md` (2 проблем)](#docsnautilusprivacy-federation04-what-i-can-do-nowmd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-en03-empirical-case-obuchaymd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/05-economics-replication.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-en05-economics-replicationmd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/06-risks.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-en06-risksmd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/07-application-domains.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-en07-application-domainsmd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/08-pilot-sgb-advocate.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-en08-pilot-sgb-advocatemd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/09-relationship-other-agents.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-en09-relationship-other-agentsmd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/12-closing.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-en12-closingmd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/00-abstract.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-ru00-abstractmd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-ru03-keys-obuchaymd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/05-ekonomika.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-ru05-ekonomikamd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/06-riski.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-ru06-riskimd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/07-oblasti-primeneniya.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-ru07-oblasti-primeneniyamd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-ru08-pilot-sgb-kolegamd-2-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/09-svyaz-s-drugimi.md` (2 проблем)](#docsnautilusprofessional-colleague-agents-ru09-svyaz-s-drugimimd-2-проблем)
  - [`docs/nautilus/representative-agent-layer-en/02-historical-precedents.md` (2 проблем)](#docsnautilusrepresentative-agent-layer-en02-historical-precedentsmd-2-проблем)
  - [`docs/nautilus/representative-agent-layer-en/03-what-makes-representative-agent.md` (2 проблем)](#docsnautilusrepresentative-agent-layer-en03-what-makes-representative-agentmd-2-проблем)
  - [`docs/nautilus/representative-agent-layer-en/04-ten-domains.md` (2 проблем)](#docsnautilusrepresentative-agent-layer-en04-ten-domainsmd-2-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/00-abstract.md` (2 проблем)](#docsnautilusrepresentative-agent-layer-ru00-abstractmd-2-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md` (2 проблем)](#docsnautilusrepresentative-agent-layer-ru02-istoricheskie-pretsedentymd-2-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md` (2 проблем)](#docsnautilusrepresentative-agent-layer-ru03-chto-delaet-predstavitelskimmd-2-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md` (2 проблем)](#docsnautilusrepresentative-agent-layer-ru04-desyat-oblasteymd-2-проблем)
  - [`docs/nautilus/review-methodology/07-why-valid-for-ai.md` (2 проблем)](#docsnautilusreview-methodology07-why-valid-for-aimd-2-проблем)
  - [`docs/nautilus/review-methodology/12-appendix-a-header-warning.md` (2 проблем)](#docsnautilusreview-methodology12-appendix-a-header-warningmd-2-проблем)
  - [`docs/nautilus/supply-demand/00-question-supply-demand.md` (2 проблем)](#docsnautilussupply-demand00-question-supply-demandmd-2-проблем)
  - [`docs/nautilus/supply-demand/01-three-related-themes.md` (2 проблем)](#docsnautilussupply-demand01-three-related-themesmd-2-проблем)
  - [`docs/nautilus/transmission-box/00-question-mountain-to-person.md` (2 проблем)](#docsnautilustransmission-box00-question-mountain-to-personmd-2-проблем)
  - [`docs/nautilus/transmission-box/01-completing-loop.md` (2 проблем)](#docsnautilustransmission-box01-completing-loopmd-2-проблем)
  - [`docs/processing-guide/02-extraction.md` (2 проблем)](#docsprocessing-guide02-extractionmd-2-проблем)
  - [`docs/processing-guide/04-structuring.md` (2 проблем)](#docsprocessing-guide04-structuringmd-2-проблем)
  - [`docs/processing-guide/06-search.md` (2 проблем)](#docsprocessing-guide06-searchmd-2-проблем)
  - [`docs/svyazi-2-0/README.md` (2 проблем)](#docssvyazi-2-0readmemd-2-проблем)
  - [`docs/svyazi-2-0/architecture/card-envelope.md` (2 проблем)](#docssvyazi-2-0architecturecard-envelopemd-2-проблем)
  - [`docs/svyazi-2-0/architecture/memory-write-policy.md` (2 проблем)](#docssvyazi-2-0architecturememory-write-policymd-2-проблем)
  - [`docs/svyazi-2-0/architecture/review-record.md` (2 проблем)](#docssvyazi-2-0architecturereview-recordmd-2-проблем)
  - [`docs/svyazi-2-0/architecture/skill-tool-policy.md` (2 проблем)](#docssvyazi-2-0architectureskill-tool-policymd-2-проблем)
  - [`docs/svyazi-2-0/components/agent-memory-mcp.md` (2 проблем)](#docssvyazi-2-0componentsagent-memory-mcpmd-2-проблем)
  - [`docs/svyazi-2-0/components/agentfs.md` (2 проблем)](#docssvyazi-2-0componentsagentfsmd-2-проблем)
  - [`docs/svyazi-2-0/components/graph-rag.md` (2 проблем)](#docssvyazi-2-0componentsgraph-ragmd-2-проблем)
  - [`docs/svyazi-2-0/components/knowledge-space.md` (2 проблем)](#docssvyazi-2-0componentsknowledge-spacemd-2-проблем)
  - [`docs/svyazi-2-0/components/legal-rag.md` (2 проблем)](#docssvyazi-2-0componentslegal-ragmd-2-проблем)
  - [`docs/svyazi-2-0/components/mclaude.md` (2 проблем)](#docssvyazi-2-0componentsmclaudemd-2-проблем)
  - [`docs/svyazi-2-0/components/ngt-memory.md` (2 проблем)](#docssvyazi-2-0componentsngt-memorymd-2-проблем)
  - [`docs/svyazi-2-0/components/research-docs-liteparse.md` (2 проблем)](#docssvyazi-2-0componentsresearch-docs-liteparsemd-2-проблем)
  - [`docs/svyazi-2-0/components/self-aware-mcp.md` (2 проблем)](#docssvyazi-2-0componentsself-aware-mcpmd-2-проблем)
  - [`docs/svyazi-2-0/components/svyazi.md` (2 проблем)](#docssvyazi-2-0componentssvyazimd-2-проблем)
  - [`docs/svyazi-2-0/components/voice-stack.md` (2 проблем)](#docssvyazi-2-0componentsvoice-stackmd-2-проблем)
  - [`docs/svyazi-2-0/components/yjs-automerge.md` (2 проблем)](#docssvyazi-2-0componentsyjs-automergemd-2-проблем)
  - [`docs/svyazi-2-0/components/yodoca.md` (2 проблем)](#docssvyazi-2-0componentsyodocamd-2-проблем)
  - [`docs/svyazi-2-0/ensembles/A-collaboration-os.md` (2 проблем)](#docssvyazi-2-0ensemblesa-collaboration-osmd-2-проблем)
  - [`docs/svyazi-2-0/ensembles/B-forensic-rag.md` (2 проблем)](#docssvyazi-2-0ensemblesb-forensic-ragmd-2-проблем)
  - [`docs/svyazi-2-0/ensembles/C-multi-agent-factory.md` (2 проблем)](#docssvyazi-2-0ensemblesc-multi-agent-factorymd-2-проблем)
  - [`docs/svyazi-2-0/ensembles/D-voice-first-mesh.md` (2 проблем)](#docssvyazi-2-0ensemblesd-voice-first-meshmd-2-проблем)
  - [`docs/svyazi-2-0/ensembles/E-execution-plane.md` (2 проблем)](#docssvyazi-2-0ensemblese-execution-planemd-2-проблем)
  - [`docs/svyazi-2-0/ensembles/F-evidence-backed-intake.md` (2 проблем)](#docssvyazi-2-0ensemblesf-evidence-backed-intakemd-2-проблем)
  - [`docs/svyazi-2-0/ensembles/H-research-to-product-flywheel.md` (2 проблем)](#docssvyazi-2-0ensemblesh-research-to-product-flywheelmd-2-проблем)
  - [`docs/svyazi-2-0/limitations/conclusions.md` (2 проблем)](#docssvyazi-2-0limitationsconclusionsmd-2-проблем)
  - [`docs/svyazi-2-0/limitations/do-not-glue.md` (2 проблем)](#docssvyazi-2-0limitationsdo-not-gluemd-2-проблем)
  - [`docs/svyazi-2-0/limitations/license-tree.md` (2 проблем)](#docssvyazi-2-0limitationslicense-treemd-2-проблем)
  - [`docs/svyazi-2-0/outreach/first-contacts.md` (2 проблем)](#docssvyazi-2-0outreachfirst-contactsmd-2-проблем)
  - [`docs/svyazi-2-0/outreach/message-template.md` (2 проблем)](#docssvyazi-2-0outreachmessage-templatemd-2-проблем)
  - [`docs/svyazi-2-0/outreach/narrow-questions.md` (2 проблем)](#docssvyazi-2-0outreachnarrow-questionsmd-2-проблем)
  - [`docs/svyazi-2-0/overview/continuation-intro.md` (2 проблем)](#docssvyazi-2-0overviewcontinuation-intromd-2-проблем)
  - [`docs/svyazi-2-0/overview/executive-summary.md` (2 проблем)](#docssvyazi-2-0overviewexecutive-summarymd-2-проблем)
  - [`docs/svyazi-2-0/overview/methodology.md` (2 проблем)](#docssvyazi-2-0overviewmethodologymd-2-проблем)
  - [`docs/svyazi-2-0/prototype/mvp-plan.md` (2 проблем)](#docssvyazi-2-0prototypemvp-planmd-2-проблем)
  - [`docs/svyazi-2-0/prototype/risks.md` (2 проблем)](#docssvyazi-2-0prototyperisksmd-2-проблем)
  - [`docs/svyazi-2-0/security/budget-routing.md` (2 проблем)](#docssvyazi-2-0securitybudget-routingmd-2-проблем)
  - [`docs/svyazi-2-0/security/privacy.md` (2 проблем)](#docssvyazi-2-0securityprivacymd-2-проблем)
  - [`docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md` (2 проблем)](#docstechnology-combinationscombinations02-multiagentnyy-khaos-reshenie-auto-ai-routermd-2-проблем)
  - [`docs/technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md` (2 проблем)](#docstechnology-combinationscombinations03-crdt-local-first-svyazi-cardindexmd-2-проблем)
  - [`docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md` (2 проблем)](#docstechnology-combinationscombinations04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitekturamd-2-проблем)
  - [`docs/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md` (2 проблем)](#docstechnology-combinationscombinations05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoymd-2-проблем)
  - [`docs/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md` (2 проблем)](#docstechnology-combinationscombinations06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-md-2-проблем)
  - [`docs/technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md` (2 проблем)](#docstechnology-combinationscombinations07-crawl4ai-docling-yodoca-consolidatormd-2-проблем)
  - [`docs/technology-combinations/combinations/09-agent-orchestration-stack.md` (2 проблем)](#docstechnology-combinationscombinations09-agent-orchestration-stackmd-2-проблем)
  - [`docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md` (2 проблем)](#docstechnology-combinationscombinations10-legal-document-intelligence-pipelinemd-2-проблем)
  - [`docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md` (2 проблем)](#docstechnology-combinationscombinations11-hybrid-crdt-sql-databasemd-2-проблем)
  - [`docs/technology-combinations/combinations/12-multi-agent-observability-stack.md` (2 проблем)](#docstechnology-combinationscombinations12-multi-agent-observability-stackmd-2-проблем)
  - [`docs/technology-combinations/combinations/13-legal-document-transpiler.md` (2 проблем)](#docstechnology-combinationscombinations13-legal-document-transpilermd-2-проблем)
  - [`docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md` (2 проблем)](#docstechnology-combinationscombinations15-self-consolidating-legal-corpusmd-2-проблем)
  - [`docs/technology-combinations/combinations/16-adversarial-multi-agent-code-review.md` (2 проблем)](#docstechnology-combinationscombinations16-adversarial-multi-agent-code-reviewmd-2-проблем)
  - [`docs/technology-combinations/combinations/17-distributed-agent-memory-with-graph.md` (2 проблем)](#docstechnology-combinationscombinations17-distributed-agent-memory-with-graphmd-2-проблем)
  - [`docs/technology-combinations/combinations/19-multi-agent-observability-platform.md` (2 проблем)](#docstechnology-combinationscombinations19-multi-agent-observability-platformmd-2-проблем)
  - [`docs/technology-combinations/combinations/22-russian-international-oss-stack.md` (2 проблем)](#docstechnology-combinationscombinations22-russian-international-oss-stackmd-2-проблем)
  - [`docs/technology-combinations/combinations/23-security-first-code-review-pipeline.md` (2 проблем)](#docstechnology-combinationscombinations23-security-first-code-review-pipelinemd-2-проблем)
  - [`docs/technology-combinations/combinations/24-mega-integration-full-stack.md` (2 проблем)](#docstechnology-combinationscombinations24-mega-integration-full-stackmd-2-проблем)
  - [`docs/technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md` (2 проблем)](#docstechnology-combinationscombinations27-hybrid-rag-with-ast-chunked-codemd-2-проблем)
  - [`docs/technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md` (2 проблем)](#docstechnology-combinationscombinations30-mega-stack-3-0-with-dsl-astmd-2-проблем)
  - [`docs/technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md` (2 проблем)](#docstechnology-combinationscombinations32-consensus-based-multi-agent-coordinationmd-2-проблем)
  - [`docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md` (2 проблем)](#docstechnology-combinationscombinations33-event-sourcing-cqrs-clickhouse-analyticsmd-2-проблем)
  - [`docs/technology-combinations/combinations/34-distributed-event-store-with-paxos.md` (2 проблем)](#docstechnology-combinationscombinations34-distributed-event-store-with-paxosmd-2-проблем)
  - [`docs/technology-combinations/mega-stacks/04-event-sourcing-consensus.md` (2 проблем)](#docstechnology-combinationsmega-stacks04-event-sourcing-consensusmd-2-проблем)
  - [`docs/technology-combinations/properties/README.md` (2 проблем)](#docstechnology-combinationspropertiesreadmemd-2-проблем)
  - [`docs/technology-combinations/research-reports/sozialrecht-35-combinations.md` (2 проблем)](#docstechnology-combinationsresearch-reportssozialrecht-35-combinationsmd-2-проблем)
  - [`docs/technology-combinations/synthesis-tables/09-14-extended.md` (2 проблем)](#docstechnology-combinationssynthesis-tables09-14-extendedmd-2-проблем)
  - [`docs/technology-combinations/synthesis-tables/15-19-extended.md` (2 проблем)](#docstechnology-combinationssynthesis-tables15-19-extendedmd-2-проблем)
  - [`docs/technology-combinations/synthesis-tables/20-24-final.md` (2 проблем)](#docstechnology-combinationssynthesis-tables20-24-finalmd-2-проблем)
  - [`docs/templates/agent-spec.md` (2 проблем)](#docstemplatesagent-specmd-2-проблем)
  - [`docs/templates/contact-outreach.md` (2 проблем)](#docstemplatescontact-outreachmd-2-проблем)
  - [`docs/templates/kpi-snapshot.md` (2 проблем)](#docstemplateskpi-snapshotmd-2-проблем)
  - [`docs/templates/project-component.md` (2 проблем)](#docstemplatesproject-componentmd-2-проблем)
  - [`docs/01-svyazi/00-intro-part2.md` (1 проблем)](#docs01-svyazi00-intro-part2md-1-проблем)
  - [`docs/01-svyazi/04-ensembles-overview.md` (1 проблем)](#docs01-svyazi04-ensembles-overviewmd-1-проблем)
  - [`docs/01-svyazi/README.md` (1 проблем)](#docs01-svyazireadmemd-1-проблем)
  - [`docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` (1 проблем)](#docs02-anthropic-vacancies87-12-onboarding-paths-normativemd-1-проблем)
  - [`docs/03-technology-combinations/README.md` (1 проблем)](#docs03-technology-combinationsreadmemd-1-проблем)
  - [`docs/04-ai-collaborations/README.md` (1 проблем)](#docs04-ai-collaborationsreadmemd-1-проблем)
  - [`docs/05-habr-projects/README.md` (1 проблем)](#docs05-habr-projectsreadmemd-1-проблем)
  - [`docs/05-habr-projects/knowledge/README.md` (1 проблем)](#docs05-habr-projectsknowledgereadmemd-1-проблем)
  - [`docs/05-habr-projects/knowledge/agentfs.md` (1 проблем)](#docs05-habr-projectsknowledgeagentfsmd-1-проблем)
  - [`docs/05-habr-projects/memory/README.md` (1 проблем)](#docs05-habr-projectsmemoryreadmemd-1-проблем)
  - [`docs/ACTION_ITEMS.md` (1 проблем)](#docsaction_itemsmd-1-проблем)
  - [`docs/ALERTS.md` (1 проблем)](#docsalertsmd-1-проблем)
  - [`docs/BACKLINKS.md` (1 проблем)](#docsbacklinksmd-1-проблем)
  - [`docs/BROKEN_LINKS.md` (1 проблем)](#docsbroken_linksmd-1-проблем)
  - [`docs/COMPLEXITY.md` (1 проблем)](#docscomplexitymd-1-проблем)
  - [`docs/CONCEPT_GRAPH.md` (1 проблем)](#docsconcept_graphmd-1-проблем)
  - [`docs/COST.md` (1 проблем)](#docscostmd-1-проблем)
  - [`docs/COVERAGE.md` (1 проблем)](#docscoveragemd-1-проблем)
  - [`docs/CROSSREFS.md` (1 проблем)](#docscrossrefsmd-1-проблем)
  - [`docs/CROSS_SECTION.md` (1 проблем)](#docscross_sectionmd-1-проблем)
  - [`docs/DECISIONS.md` (1 проблем)](#docsdecisionsmd-1-проблем)
  - [`docs/DEPENDENCY_MAP.md` (1 проблем)](#docsdependency_mapmd-1-проблем)
  - [`docs/DIGEST_AUTO.md` (1 проблем)](#docsdigest_automd-1-проблем)
  - [`docs/GRAPH.md` (1 проблем)](#docsgraphmd-1-проблем)
  - [`docs/KPI.md` (1 проблем)](#docskpimd-1-проблем)
  - [`docs/KPI_HISTORY.md` (1 проблем)](#docskpi_historymd-1-проблем)
  - [`docs/MCP_DASHBOARD.md` (1 проблем)](#docsmcp_dashboardmd-1-проблем)
  - [`docs/METRICS.md` (1 проблем)](#docsmetricsmd-1-проблем)
  - [`docs/MISSING.md` (1 проблем)](#docsmissingmd-1-проблем)
  - [`docs/NAMED_ENTITIES.md` (1 проблем)](#docsnamed_entitiesmd-1-проблем)
  - [`docs/NETWORK.md` (1 проблем)](#docsnetworkmd-1-проблем)
  - [`docs/PASSIVE_VOICE.md` (1 проблем)](#docspassive_voicemd-1-проблем)
  - [`docs/QUESTIONS.md` (1 проблем)](#docsquestionsmd-1-проблем)
  - [`docs/READING_TIME.md` (1 проблем)](#docsreading_timemd-1-проблем)
  - [`docs/REGISTRY.md` (1 проблем)](#docsregistrymd-1-проблем)
  - [`docs/SEE_ALSO.md` (1 проблем)](#docssee_alsomd-1-проблем)
  - [`docs/SENTIMENT.md` (1 проблем)](#docssentimentmd-1-проблем)
  - [`docs/SITEMAP.md` (1 проблем)](#docssitemapmd-1-проблем)
  - [`docs/SKILL_DASHBOARD.md` (1 проблем)](#docsskill_dashboardmd-1-проблем)
  - [`docs/SOURCE_MAP.md` (1 проблем)](#docssource_mapmd-1-проблем)
  - [`docs/STALENESS.md` (1 проблем)](#docsstalenessmd-1-проблем)
  - [`docs/STATS.md` (1 проблем)](#docsstatsmd-1-проблем)
  - [`docs/TAGS.md` (1 проблем)](#docstagsmd-1-проблем)
  - [`docs/TIMELINE.md` (1 проблем)](#docstimelinemd-1-проблем)
  - [`docs/TOPIC_MODEL.md` (1 проблем)](#docstopic_modelmd-1-проблем)
  - [`docs/VERSION_DIFF.md` (1 проблем)](#docsversion_diffmd-1-проблем)
  - [`docs/ai-collaborations/README.md` (1 проблем)](#docsai-collaborationsreadmemd-1-проблем)
  - [`docs/ai-collaborations/candidates/README.md` (1 проблем)](#docsai-collaborationscandidatesreadmemd-1-проблем)
  - [`docs/ai-collaborations/channels/README.md` (1 проблем)](#docsai-collaborationschannelsreadmemd-1-проблем)
  - [`docs/ai-collaborations/continuation/README.md` (1 проблем)](#docsai-collaborationscontinuationreadmemd-1-проблем)
  - [`docs/ai-collaborations/ensembles/README.md` (1 проблем)](#docsai-collaborationsensemblesreadmemd-1-проблем)
  - [`docs/ai-collaborations/fast-tracks/README.md` (1 проблем)](#docsai-collaborationsfast-tracksreadmemd-1-проблем)
  - [`docs/ai-collaborations/source-projects.md` (1 проблем)](#docsai-collaborationssource-projectsmd-1-проблем)
  - [`docs/ai-collaborations/strategy/README.md` (1 проблем)](#docsai-collaborationsstrategyreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/README.md` (1 проблем)](#docsanthropic-vacanciesreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/ai-managed-virtual-company/README.md` (1 проблем)](#docsanthropic-vacanciesai-managed-virtual-companyreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/beneficial-deployments-concept/README.md` (1 проблем)](#docsanthropic-vacanciesbeneficial-deployments-conceptreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/clusters/README.md` (1 проблем)](#docsanthropic-vacanciesclustersreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/extra-collaborator-findings/README.md` (1 проблем)](#docsanthropic-vacanciesextra-collaborator-findingsreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/hermes-comparison/README.md` (1 проблем)](#docsanthropic-vacancieshermes-comparisonreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/methodology.md` (1 проблем)](#docsanthropic-vacanciesmethodologymd-1-проблем)
  - [`docs/anthropic-vacancies/mmorpg-for-programmers/README.md` (1 проблем)](#docsanthropic-vacanciesmmorpg-for-programmersreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/nautilus-pro2-analysis/README.md` (1 проблем)](#docsanthropic-vacanciesnautilus-pro2-analysisreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/nautilus-vs-camel/README.md` (1 проблем)](#docsanthropic-vacanciesnautilus-vs-camelreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/01-initial-analysis/README.md` (1 проблем)](#docsanthropic-vacanciesprofile-mapping01-initial-analysisreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md` (1 проблем)](#docsanthropic-vacanciesprofile-mapping02-reanalysisreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md` (1 проблем)](#docsanthropic-vacanciesprofile-mapping03-integral-finalreadmemd-1-проблем)
  - [`docs/anthropic-vacancies/profile-mapping/README.md` (1 проблем)](#docsanthropic-vacanciesprofile-mappingreadmemd-1-проблем)
  - [`docs/autofilled/components/README.md` (1 проблем)](#docsautofilledcomponentsreadmemd-1-проблем)
  - [`docs/contacts/README.md` (1 проблем)](#docscontactsreadmemd-1-проблем)
  - [`docs/glossary/README.md` (1 проблем)](#docsglossaryreadmemd-1-проблем)
  - [`docs/habr-unique-projects/README.md` (1 проблем)](#docshabr-unique-projectsreadmemd-1-проблем)
  - [`docs/habr-unique-projects/analogues/README.md` (1 проблем)](#docshabr-unique-projectsanaloguesreadmemd-1-проблем)
  - [`docs/habr-unique-projects/deep-pairs/README.md` (1 проблем)](#docshabr-unique-projectsdeep-pairsreadmemd-1-проблем)
  - [`docs/habr-unique-projects/evaluation/README.md` (1 проблем)](#docshabr-unique-projectsevaluationreadmemd-1-проблем)
  - [`docs/habr-unique-projects/extra-examples/README.md` (1 проблем)](#docshabr-unique-projectsextra-examplesreadmemd-1-проблем)
  - [`docs/habr-unique-projects/final-ensembles/README.md` (1 проблем)](#docshabr-unique-projectsfinal-ensemblesreadmemd-1-проблем)
  - [`docs/habr-unique-projects/hardware-pairs/README.md` (1 проблем)](#docshabr-unique-projectshardware-pairsreadmemd-1-проблем)
  - [`docs/habr-unique-projects/key-findings/README.md` (1 проблем)](#docshabr-unique-projectskey-findingsreadmemd-1-проблем)
  - [`docs/habr-unique-projects/search-strategy/README.md` (1 проблем)](#docshabr-unique-projectssearch-strategyreadmemd-1-проблем)
  - [`docs/habr-unique-projects/software-pairs/README.md` (1 проблем)](#docshabr-unique-projectssoftware-pairsreadmemd-1-проблем)
  - [`docs/lorenzo-agent/README.md` (1 проблем)](#docslorenzo-agentreadmemd-1-проблем)
  - [`docs/lorenzo-agent/naming/README.md` (1 проблем)](#docslorenzo-agentnamingreadmemd-1-проблем)
  - [`docs/lorenzo-agent/operationalized/README.md` (1 проблем)](#docslorenzo-agentoperationalizedreadmemd-1-проблем)
  - [`docs/lorenzo-agent/phased-deployment/README.md` (1 проблем)](#docslorenzo-agentphased-deploymentreadmemd-1-проблем)
  - [`docs/lorenzo-agent/scenarios/README.md` (1 проблем)](#docslorenzo-agentscenariosreadmemd-1-проблем)
  - [`docs/lorenzo-agent/specification/README.md` (1 проблем)](#docslorenzo-agentspecificationreadmemd-1-проблем)
  - [`docs/meta-scripting/05-synthesis.md` (1 проблем)](#docsmeta-scripting05-synthesismd-1-проблем)
  - [`docs/meta-scripting/README.md` (1 проблем)](#docsmeta-scriptingreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/README.md` (1 проблем)](#docsnautiluscommunity-discussionsreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/agent-changes-reality/README.md` (1 проблем)](#docsnautiluscommunity-discussionsagent-changes-realityreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/habr-article-1-reaction/README.md` (1 проблем)](#docsnautiluscommunity-discussionshabr-article-1-reactionreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/habr-article-2-reaction/README.md` (1 проблем)](#docsnautiluscommunity-discussionshabr-article-2-reactionreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/practical-observations/README.md` (1 проблем)](#docsnautiluscommunity-discussionspractical-observationsreadmemd-1-проблем)
  - [`docs/nautilus/community-discussions/voiceless-contributors/README.md` (1 проблем)](#docsnautiluscommunity-discussionsvoiceless-contributorsreadmemd-1-проблем)
  - [`docs/nautilus/composite-skills-agents/README.md` (1 проблем)](#docsnautiluscomposite-skills-agentsreadmemd-1-проблем)
  - [`docs/nautilus/composite-skills-agents-companion-mentors/README.md` (1 проблем)](#docsnautiluscomposite-skills-agents-companion-mentorsreadmemd-1-проблем)
  - [`docs/nautilus/double-triangle-architecture/README.md` (1 проблем)](#docsnautilusdouble-triangle-architecturereadmemd-1-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/13-acknowledgments-refs.md` (1 проблем)](#docsnautilusinfrastructure-layer-b-en13-acknowledgments-refsmd-1-проблем)
  - [`docs/nautilus/infrastructure-layer-b-en/README.md` (1 проблем)](#docsnautilusinfrastructure-layer-b-enreadmemd-1-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/12-blagodarnosti-ssylki.md` (1 проблем)](#docsnautilusinfrastructure-layer-b-ru12-blagodarnosti-ssylkimd-1-проблем)
  - [`docs/nautilus/infrastructure-layer-b-ru/README.md` (1 проблем)](#docsnautilusinfrastructure-layer-b-rureadmemd-1-проблем)
  - [`docs/nautilus/ingit-cowork-en/04-symbiotic-architecture.md` (1 проблем)](#docsnautilusingit-cowork-en04-symbiotic-architecturemd-1-проблем)
  - [`docs/nautilus/ingit-cowork-en/README.md` (1 проблем)](#docsnautilusingit-cowork-enreadmemd-1-проблем)
  - [`docs/nautilus/ingit-cowork-ru/04-simbioticheskaya-arkhitektura.md` (1 проблем)](#docsnautilusingit-cowork-ru04-simbioticheskaya-arkhitekturamd-1-проблем)
  - [`docs/nautilus/ingit-cowork-ru/README.md` (1 проблем)](#docsnautilusingit-cowork-rureadmemd-1-проблем)
  - [`docs/nautilus/innovation-transitions/00-question-innovations-transitions.md` (1 проблем)](#docsnautilusinnovation-transitions00-question-innovations-transitionsmd-1-проблем)
  - [`docs/nautilus/innovation-transitions/README.md` (1 проблем)](#docsnautilusinnovation-transitionsreadmemd-1-проблем)
  - [`docs/nautilus/multi-tier-architecture/README.md` (1 проблем)](#docsnautilusmulti-tier-architecturereadmemd-1-проблем)
  - [`docs/nautilus/npp-humanitarian-extension/README.md` (1 проблем)](#docsnautilusnpp-humanitarian-extensionreadmemd-1-проблем)
  - [`docs/nautilus/npp-v1-0/README.md` (1 проблем)](#docsnautilusnpp-v1-0readmemd-1-проблем)
  - [`docs/nautilus/npp-v1-1/README.md` (1 проблем)](#docsnautilusnpp-v1-1readmemd-1-проблем)
  - [`docs/nautilus/okwf-concept/README.md` (1 проблем)](#docsnautilusokwf-conceptreadmemd-1-проблем)
  - [`docs/nautilus/privacy-federation/README.md` (1 проблем)](#docsnautilusprivacy-federationreadmemd-1-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/01-five-type-typology.md` (1 проблем)](#docsnautilusprofessional-colleague-agents-en01-five-type-typologymd-1-проблем)
  - [`docs/nautilus/professional-colleague-agents-en/README.md` (1 проблем)](#docsnautilusprofessional-colleague-agents-enreadmemd-1-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/01-pyat-tipov.md` (1 проблем)](#docsnautilusprofessional-colleague-agents-ru01-pyat-tipovmd-1-проблем)
  - [`docs/nautilus/professional-colleague-agents-ru/README.md` (1 проблем)](#docsnautilusprofessional-colleague-agents-rureadmemd-1-проблем)
  - [`docs/nautilus/representative-agent-layer-en/README.md` (1 проблем)](#docsnautilusrepresentative-agent-layer-enreadmemd-1-проблем)
  - [`docs/nautilus/representative-agent-layer-ru/README.md` (1 проблем)](#docsnautilusrepresentative-agent-layer-rureadmemd-1-проблем)
  - [`docs/nautilus/review-methodology/04-fallback-ratio-question.md` (1 проблем)](#docsnautilusreview-methodology04-fallback-ratio-questionmd-1-проблем)
  - [`docs/nautilus/review-methodology/README.md` (1 проблем)](#docsnautilusreview-methodologyreadmemd-1-проблем)
  - [`docs/nautilus/supply-demand/README.md` (1 проблем)](#docsnautilussupply-demandreadmemd-1-проблем)
  - [`docs/nautilus/transmission-box/README.md` (1 проблем)](#docsnautilustransmission-boxreadmemd-1-проблем)
  - [`docs/processing-guide/01-overview.md` (1 проблем)](#docsprocessing-guide01-overviewmd-1-проблем)
  - [`docs/processing-guide/README.md` (1 проблем)](#docsprocessing-guidereadmemd-1-проблем)
  - [`docs/reading-paths.md` (1 проблем)](#docsreading-pathsmd-1-проблем)
  - [`docs/svyazi-2-0/architecture/README.md` (1 проблем)](#docssvyazi-2-0architecturereadmemd-1-проблем)
  - [`docs/svyazi-2-0/architecture/gaps.md` (1 проблем)](#docssvyazi-2-0architecturegapsmd-1-проблем)
  - [`docs/svyazi-2-0/components/README.md` (1 проблем)](#docssvyazi-2-0componentsreadmemd-1-проблем)
  - [`docs/svyazi-2-0/ensembles/README.md` (1 проблем)](#docssvyazi-2-0ensemblesreadmemd-1-проблем)
  - [`docs/svyazi-2-0/limitations/README.md` (1 проблем)](#docssvyazi-2-0limitationsreadmemd-1-проблем)
  - [`docs/svyazi-2-0/outreach/README.md` (1 проблем)](#docssvyazi-2-0outreachreadmemd-1-проблем)
  - [`docs/svyazi-2-0/overview/README.md` (1 проблем)](#docssvyazi-2-0overviewreadmemd-1-проблем)
  - [`docs/svyazi-2-0/prototype/README.md` (1 проблем)](#docssvyazi-2-0prototypereadmemd-1-проблем)
  - [`docs/svyazi-2-0/prototype/roadmap.md` (1 проблем)](#docssvyazi-2-0prototyperoadmapmd-1-проблем)
  - [`docs/svyazi-2-0/security/README.md` (1 проблем)](#docssvyazi-2-0securityreadmemd-1-проблем)
  - [`docs/technology-combinations/README.md` (1 проблем)](#docstechnology-combinationsreadmemd-1-проблем)
  - [`docs/technology-combinations/combinations/README.md` (1 проблем)](#docstechnology-combinationscombinationsreadmemd-1-проблем)
  - [`docs/technology-combinations/mega-stacks/01-legal-ai-stack.md` (1 проблем)](#docstechnology-combinationsmega-stacks01-legal-ai-stackmd-1-проблем)
  - [`docs/technology-combinations/mega-stacks/02-ultimate-legal-ai.md` (1 проблем)](#docstechnology-combinationsmega-stacks02-ultimate-legal-aimd-1-проблем)
  - [`docs/technology-combinations/mega-stacks/03-dsl-ast.md` (1 проблем)](#docstechnology-combinationsmega-stacks03-dsl-astmd-1-проблем)
  - [`docs/technology-combinations/mega-stacks/README.md` (1 проблем)](#docstechnology-combinationsmega-stacksreadmemd-1-проблем)
  - [`docs/technology-combinations/research-reports/README.md` (1 проблем)](#docstechnology-combinationsresearch-reportsreadmemd-1-проблем)
  - [`docs/technology-combinations/synthesis-tables/25-30-extended.md` (1 проблем)](#docstechnology-combinationssynthesis-tables25-30-extendedmd-1-проблем)
  - [`docs/technology-combinations/synthesis-tables/31-35-final.md` (1 проблем)](#docstechnology-combinationssynthesis-tables31-35-finalmd-1-проблем)
  - [`docs/technology-combinations/synthesis-tables/README.md` (1 проблем)](#docstechnology-combinationssynthesis-tablesreadmemd-1-проблем)
  - [`docs/templates/README.md` (1 проблем)](#docstemplatesreadmemd-1-проблем)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

---


<!-- toc-auto -->

> [!NOTE]
> Раздел `HEADING_AUDIT` автоматически формируется из данных репозитория.

<!-- alert-added -->
<!-- tags: heading-audit, docs -->


<!-- summary -->
> `HEADING_AUDIT` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-11_

Файлов с проблемами: **1206** из 1223

## Типы проблем

| Тип | Кол-во |
|-----|--------|
| 🕳️  Пустая секция | 3594 |
| ♊ Дублирующийся заголовок | 1111 |
| 📏 Длинный заголовок | 4 |
| 🪜 Пропущен уровень | 5 |
| ❌ Несколько H1 | 75 |

## По файлам

### `docs/EMPTY_SECTIONS.md` (369 проблем)

_секция: 356, заголовок: 13_


### `docs/QA.md` (177 проблем)

_секция: 154, заголовок: 23_


### `docs/CODE_BLOCKS.md` (127 проблем)

_секция: 108, заголовок: 19_


### `docs/SPELLCHECK.md` (53 проблем)

_секция: 53_


### `docs/TABLES.md` (49 проблем)

_заголовок: 29, секция: 20_


### `docs/processing-guide/PROCESSING_GUIDE.md` (31 проблем)

_секция: 29, заголовок: 2_


### `docs/02-anthropic-vacancies/QA.md` (23 проблем)

_секция: 23_


### `docs/CHANGELOG.md` (20 проблем)

_секция: 15, заголовок: 5_


### `docs/processing-guide/QA.md` (19 проблем)

_секция: 19_


### `docs/lorenzo-agent/QA.md` (18 проблем)

_секция: 18_


### `docs/templates/protocol-spec.md` (18 проблем)

_секция: 18_


### `docs/templates/rfc.md` (18 проблем)

_секция: 18_


### `docs/05-habr-projects/QA.md` (16 проблем)

_секция: 16_


### `docs/templates/mega-stack.md` (16 проблем)

_секция: 16_


### `docs/01-svyazi/QA.md` (15 проблем)

_секция: 15_


### `docs/04-ai-collaborations/QA.md` (15 проблем)

_секция: 15_


### `docs/02-anthropic-vacancies/69-section.md` (13 проблем)

_секция: 11, H1: 1, заголовок: 1_


### `docs/technology-combinations/combinations/26-ast-based-code-analysis-for-legal-automation.md` (13 проблем)

_секция: 12, H1: 1_


### `docs/templates/tech-pair.md` (13 проблем)

_секция: 13_


### `docs/templates/template-of-templates.md` (13 проблем)

_секция: 13_


### `docs/02-anthropic-vacancies/109-3-принципы-консолидации-фаза-c.md` (12 проблем)

_секция: 6, заголовок: 5, H1: 1_


### `docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md` (12 проблем)

_секция: 8, заголовок: 4_


### `docs/GITHUB_ISSUES.md` (12 проблем)

_секция: 12_


### `docs/02-anthropic-vacancies/299-практические-рекомендации-для-текущего-проекта.md` (11 проблем)

_секция: 6, заголовок: 4, H1: 1_


### `docs/02-anthropic-vacancies/365-развёрнутый-анализ-внуковой-комбинации.md` (11 проблем)

_секция: 8, заголовок: 3_


### `docs/SCRIPT_EVAL_REPORT.md` (11 проблем)

_секция: 11_


### `docs/ai-collaborations/QA.md` (11 проблем)

_секция: 11_


### `docs/templates/experiment-log.md` (11 проблем)

_секция: 11_


### `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` (10 проблем)

_секция: 5, заголовок: 3, H1: 1, уровень: 1_


### `docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md` (10 проблем)

_секция: 7, заголовок: 2, H1: 1_


### `docs/03-technology-combinations/05-benchmarks.md` (10 проблем)

_секция: 6, заголовок: 4_


### `docs/FAQ.md` (10 проблем)

_секция: 10_


### `docs/processing-guide/05-analysis.md` (10 проблем)

_секция: 10_


### `docs/02-anthropic-vacancies/02-общий-план-развития-nautilus-portal-protocol.md` (9 проблем)

_секция: 6, заголовок: 3_


### `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md` (9 проблем)

_секция: 4, заголовок: 4, H1: 1_


### `docs/02-anthropic-vacancies/165-closing.md` (9 проблем)

_секция: 4, заголовок: 4, H1: 1_


### `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md` (9 проблем)

_секция: 6, заголовок: 3_


### `docs/03-technology-combinations/QA.md` (9 проблем)

_секция: 9_


### `docs/CONSISTENCY.md` (9 проблем)

_секция: 7, заголовок: 2_


### `docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md` (9 проблем)

_секция: 8, H1: 1_


### `docs/nautilus/npp-v1-1/22-glossary.md` (9 проблем)

_секция: 7, H1: 1, заголовок: 1_


### `docs/templates/legal-case.md` (9 проблем)

_секция: 9_


### `docs/02-anthropic-vacancies/09-4-passport-passport-md.md` (8 проблем)

_секция: 4, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/127-подключение-к-claude-desktop.md` (8 проблем)

_секция: 5, заголовок: 3_


### `docs/02-anthropic-vacancies/133-обратная-связь.md` (8 проблем)

_секция: 3, заголовок: 3, H1: 1, уровень: 1_


### `docs/02-anthropic-vacancies/229-профессиональные-коллеги-агенты.md` (8 проблем)

_секция: 4, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/23-11-security-considerations.md` (8 проблем)

_секция: 5, заголовок: 3_


### `docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md` (8 проблем)

_секция: 6, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/289-инфраструктура-для-ai-совместной-интеллектуальной-.md` (8 проблем)

_секция: 4, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/296-рекурсивное-прозрение.md` (8 проблем)

_секция: 5, заголовок: 3_


### `docs/02-anthropic-vacancies/319-acknowledgments.md` (8 проблем)

_заголовок: 4, секция: 3, H1: 1_


### `docs/02-anthropic-vacancies/324-ingit-как-cowork-интегрированная-подложка-рабочего.md` (8 проблем)

_секция: 4, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md` (8 проблем)

_заголовок: 4, секция: 3, H1: 1_


### `docs/02-anthropic-vacancies/356-твой-workflow.md` (8 проблем)

_секция: 5, заголовок: 3_


### `docs/02-anthropic-vacancies/71-критерии-выбора-для-фазы-3.md` (8 проблем)

_секция: 5, заголовок: 3_


### `docs/05-habr-projects/01-synthesis.md` (8 проблем)

_секция: 6, заголовок: 2_


### `docs/nautilus/npp-v1-0/16-appendix-a-minimal-working-example.md` (8 проблем)

_секция: 7, H1: 1_


### `docs/svyazi-2-0/QA.md` (8 проблем)

_секция: 8_


### `docs/templates/meeting-notes.md` (8 проблем)

_секция: 8_


### `docs/templates/weekly-digest.md` (8 проблем)

_секция: 8_


### `docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md` (7 проблем)

_заголовок: 5, секция: 2_


### `docs/02-anthropic-vacancies/03-portal-protocol-md.md` (7 проблем)

_секция: 3, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` (7 проблем)

_секция: 4, заголовок: 3_


### `docs/02-anthropic-vacancies/105-review-methodology-md.md` (7 проблем)

_секция: 3, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/203-благодарности.md` (7 проблем)

_секция: 5, заголовок: 2_


### `docs/02-anthropic-vacancies/21-9-query-flow.md` (7 проблем)

_секция: 4, заголовок: 3_


### `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` (7 проблем)

_секция: 4, заголовок: 3_


### `docs/02-anthropic-vacancies/320-references.md` (7 проблем)

_секция: 4, заголовок: 3_


### `docs/02-anthropic-vacancies/338-ссылки.md` (7 проблем)

_секция: 4, заголовок: 3_


### `docs/02-anthropic-vacancies/34-appendix-b-change-log.md` (7 проблем)

_заголовок: 4, секция: 2, H1: 1_


### `docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md` (7 проблем)

_секция: 4, заголовок: 3_


### `docs/02-anthropic-vacancies/35-passports-info1-md.md` (7 проблем)

_секция: 3, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/45-passports-pro2-md.md` (7 проблем)

_секция: 3, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/55-passports-meta-md.md` (7 проблем)

_секция: 3, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/65-readme-md.md` (7 проблем)

_секция: 3, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/73-portal-protocol-md-v1-1.md` (7 проблем)

_секция: 3, заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/90-15-security-considerations.md` (7 проблем)

_секция: 4, заголовок: 3_


### `docs/03-technology-combinations/01-agent-routing.md` (7 проблем)

_секция: 5, уровень: 1, заголовок: 1_


### `docs/METHODOLOGY.md` (7 проблем)

_секция: 7_


### `docs/autofilled/research-summary.md` (7 проблем)

_секция: 6, заголовок: 1_


### `docs/nautilus/npp-humanitarian-extension/01-structural-comparison-code-vs-docs.md` (7 проблем)

_секция: 5, H1: 1, заголовок: 1_


### `docs/templates/faq-entry.md` (7 проблем)

_секция: 7_


### `docs/templates/glossary-entry.md` (7 проблем)

_секция: 7_


### `docs/templates/prototype-mvp.md` (7 проблем)

_секция: 7_


### `docs/templates/risk-entry.md` (7 проблем)

_секция: 7_


### `docs/templates/tech-radar-entry.md` (7 проблем)

_секция: 7_


### `docs/02-anthropic-vacancies/00-intro.md` (6 проблем)

_секция: 4, заголовок: 2_


### `docs/02-anthropic-vacancies/04-abstract.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/104-appendix-c-references.md` (6 проблем)

_заголовок: 3, секция: 2, H1: 1_


### `docs/02-anthropic-vacancies/12-content-overview.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/130-отладка.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/154-table-of-contents.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/159-5-economic-model.md` (6 проблем)

_секция: 4, заголовок: 2_


### `docs/02-anthropic-vacancies/18-6-adapter-interface.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/24-12-versioning-policy.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/243-12-заключение.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/291-двухслойный-стек-как-он-существует.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/305-a-practical-path-to-layer-b-through-symbiotic-inte.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/31-content-overview.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/351-что-ты-можешь-делать.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/358-твоя-relationship-с-другими-ai.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/364-final-note-ты-experiment.md` (6 проблем)

_заголовок: 3, секция: 2, H1: 1_


### `docs/02-anthropic-vacancies/37-native-format.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/44-for-the-curious-philosophy.md` (6 проблем)

_заголовок: 3, секция: 2, H1: 1_


### `docs/02-anthropic-vacancies/54-for-the-curious-philosophy.md` (6 проблем)

_заголовок: 3, секция: 2, H1: 1_


### `docs/02-anthropic-vacancies/70-зачем-две-версии-параллельно.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/72-расписание-фазы-3.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/84-9-consensus-algorithm.md` (6 проблем)

_секция: 5, заголовок: 1_


### `docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md` (6 проблем)

_секция: 3, заголовок: 3_


### `docs/03-technology-combinations/03-local-first.md` (6 проблем)

_секция: 3, заголовок: 2, уровень: 1_


### `docs/05-habr-projects/knowledge/wikontic.md` (6 проблем)

_секция: 4, заголовок: 2_


### `docs/05-habr-projects/memory/yodoca.md` (6 проблем)

_секция: 4, заголовок: 2_


### `docs/SCHEDULE.md` (6 проблем)

_секция: 6_


### `docs/meta-scripting/QA.md` (6 проблем)

_секция: 6_


### `docs/nautilus/npp-v1-0/15-glossary.md` (6 проблем)

_секция: 5, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/00-abstract.md` (6 проблем)

_секция: 3, заголовок: 2, H1: 1_


### `docs/nautilus/representative-agent-layer-en/12-closing.md` (6 проблем)

_секция: 4, H1: 1, заголовок: 1_


### `docs/templates/contradiction-record.md` (6 проблем)

_секция: 6_


### `docs/templates/retrospective.md` (6 проблем)

_секция: 6_


### `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/106-tl-dr.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/111-4-условия-применимости.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/120-главные-технические-риски.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` (5 проблем)

_секция: 3, заголовок: 2_


### `docs/02-anthropic-vacancies/122-глоссарий.md` (5 проблем)

_заголовок: 3, H1: 1, секция: 1_


### `docs/02-anthropic-vacancies/123-portal-mcp-py.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/124-конфигурация-для-claude-desktop.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` (5 проблем)

_заголовок: 3, H1: 1, секция: 1_


### `docs/02-anthropic-vacancies/126-установка.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/128-доступные-инструменты.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/129-примеры-запросов-в-claude.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/13-angle-perspective.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/137-table-of-contents.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/139-2-the-double-triangle-architecture.md` (5 проблем)

_секция: 2, заголовок: 2, H1: 1_


### `docs/02-anthropic-vacancies/146-acknowledgments.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/148-appendix-a-glossary.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` (5 проблем)

_заголовок: 3, H1: 1, секция: 1_


### `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/155-1-problem-statement.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/156-2-target-populations.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/16-history.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/162-8-risk-analysis.md` (5 проблем)

_секция: 3, заголовок: 2_


### `docs/02-anthropic-vacancies/164-10-appendices.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/169-table-of-contents.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/174-5-architectural-specification.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/181-12-closing.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/182-acknowledgments.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/184-appendix-a-connection-to-companion-papers.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/186-appendix-c-sample-use-cases-in-detail.md` (5 проблем)

_заголовок: 3, H1: 1, секция: 1_


### `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/189-аннотация.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/196-6-этическая-рамка.md` (5 проблем)

_секция: 3, заголовок: 2_


### `docs/02-anthropic-vacancies/202-12-заключение.md` (5 проблем)

_секция: 3, заголовок: 2_


### `docs/02-anthropic-vacancies/204-ссылки.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/207-приложение-c-образцы-случаев-использования-в-детал.md` (5 проблем)

_заголовок: 3, H1: 1, секция: 1_


### `docs/02-anthropic-vacancies/208-professional-colleague-agents-md.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/209-a-typology-of-ai-agents-on-the-principal-side-and-.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/211-table-of-contents.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/22-10-queryresult-structure.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/224-acknowledgments.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/230-аннотация.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/236-5-экономика-тиражирования-по-профессии.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/244-благодарности.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/249-composite-skills-agent-md.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/25-13-reference-implementation.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/251-ai-support-through-configurable-specialist-ensembl.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/253-table-of-contents.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/269-appendix-a-the-six-type-taxonomy-updated.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/273-infrastructure-for-ai-collaborative-intellectual-w.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/274-the-missing-middle-layer-between-chat-and-code.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/282-what-industry-will-likely-build.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/283-what-this-document-doesn-t-solve.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/285-closing.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/286-acknowledgments.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/301-благодарности.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/304-ingit-as-cowork-native-workspace-substrate-md.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/308-table-of-contents.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/317-9-risks-and-open-questions.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/344-системный-промпт-для-lorenzo-project.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/353-что-ты-не-можешь-делать-вообще.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/39-angle-perspective.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/41-compatibility-level.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/42-author-contact.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/47-native-format.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/49-angle-perspective.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/51-compatibility-level.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/52-author-contact.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/53-history.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/59-angle-perspective.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/61-compatibility-level.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/62-author-contact.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/63-history.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/64-for-the-curious-philosophy.md` (5 проблем)

_заголовок: 3, H1: 1, секция: 1_


### `docs/02-anthropic-vacancies/67-о-проекте.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/74-abstract.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/75-0-status-of-this-document.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/02-anthropic-vacancies/91-16-mcp-extension-informative.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/02-anthropic-vacancies/93-18-reference-implementation.md` (5 проблем)

_заголовок: 3, секция: 2_


### `docs/VALIDATION.md` (5 проблем)

_секция: 5_


### `docs/anthropic-vacancies/QA.md` (5 проблем)

_секция: 5_


### `docs/autofilled/components/.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/autofilled/components/cowork.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/autofilled/components/ingit.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/autofilled/components/kksudo.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/autofilled/components/lorenzo.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/autofilled/components/nautilus.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/autofilled/components/sgb.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/autofilled/components/spbmolot.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/autofilled/components/svend4.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/autofilled/components/svyazi.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/meta-scripting/02-architecture.md` (5 проблем)

_секция: 5_


### `docs/meta-scripting/04-enrichment.md` (5 проблем)

_секция: 5_


### `docs/nautilus/infrastructure-layer-b-en/00-intro.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/nautilus/npp-v1-1/09-consensus-algorithm.md` (5 проблем)

_секция: 4, заголовок: 1_


### `docs/nautilus/okwf-concept/00-abstract.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/00-abstract.md` (5 проблем)

_секция: 3, H1: 1, заголовок: 1_


### `docs/processing-guide/07-llm.md` (5 проблем)

_секция: 5_


### `docs/technology-combinations/combinations/25-legal-dsl-code-transpiler.md` (5 проблем)

_секция: 4, H1: 1_


### `docs/02-anthropic-vacancies/06-1-introduction.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/102-доступ-к-данным.md` (4 проблем)

_секция: 2, H1: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/108-2-формальный-workflow.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/117-10-конкретный-план-применения-к-текущим-документам.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/136-abstract.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/144-7-open-questions.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/145-8-call-to-action.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/147-references.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/153-executive-summary.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/157-3-why-existing-solutions-fail.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/160-6-governance-and-ethics.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/168-abstract.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/172-3-what-makes-a-representative-agent.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/180-11-call-for-collaboration.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/183-references.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` (4 проблем)

_секция: 2, заголовок: 2_


### `docs/02-anthropic-vacancies/19-7-portalentry-structure.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/190-содержание.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` (4 проблем)

_секция: 2, заголовок: 2_


### `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/20-8-consensus-algorithm.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/210-abstract.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/214-3-empirical-case-study-обучай.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/216-5-the-economics-of-profession-wide-replication.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/217-6-risks-specific-to-this-category.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/219-8-pilot-proposal-sgb-advocate-colleague.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/220-9-relationship-to-other-agent-types.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/222-11-call-for-collaboration.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/223-12-closing.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/225-references.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/227-appendix-b-decision-framework-when-to-build-type-1.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/231-содержание.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/240-9-связь-с-другими-типами-агентов.md` (4 проблем)

_секция: 2, заголовок: 2_


### `docs/02-anthropic-vacancies/245-ссылки.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/246-приложение-a-сравнительная-таблица-пять-типов-аген.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/247-приложение-b-рамка-принятия-решений-когда-строить-.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/252-abstract.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/257-4-the-sub-agent-registry.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/259-6-coordination-and-disagreement-resolution.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/260-7-economics-of-combinatorial-replication.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/264-11-open-questions.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/266-13-closing.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/267-acknowledgments.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md` (4 проблем)

_заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/275-why-this-document-exists.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/276-the-two-layer-stack-as-it-exists.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/278-why-this-hasn-t-been-built.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/281-the-recursive-insight.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/284-practical-recommendations-for-the-current-project.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/295-конкретный-случай-перед-нами.md` (4 проблем)

_секция: 2, заголовок: 2_


### `docs/02-anthropic-vacancies/302-ссылки.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md` (4 проблем)

_заголовок: 3, H1: 1_


### `docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/307-abstract.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/316-8-implications-for-nautilus-and-okwf.md` (4 проблем)

_секция: 2, заголовок: 2_


### `docs/02-anthropic-vacancies/323-appendix-c-sample-ingit-mcp-server-tool-specificat.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/326-содержание.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/328-2-что-cowork-обеспечивает-что-ingit-не-нужно-строи.md` (4 проблем)

_секция: 2, заголовок: 2_


### `docs/02-anthropic-vacancies/330-4-симбиотическая-архитектура.md` (4 проблем)

_секция: 2, заголовок: 2_


### `docs/02-anthropic-vacancies/334-8-импликации-для-nautilus-и-okwf.md` (4 проблем)

_секция: 2, заголовок: 2_


### `docs/02-anthropic-vacancies/335-9-риски-и-открытые-вопросы.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/336-10-стратегическое-позиционирование.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/340-приложение-b-сравнительная-матрица.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/345-кто-ты.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/346-твоё-происхождение.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/347-твоя-миссия.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/350-твои-языки-и-культурные-nuances.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/354-существующий-landscape-collaborators-твоя-working-.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/359-твои-anti-patterns.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/363-твоя-identity-как-persistent-character.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/38-content-overview.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/40-bridges.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/43-history.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/50-bridges.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/57-native-format.md` (4 проблем)

_заголовок: 3, секция: 1_


### `docs/02-anthropic-vacancies/58-content-overview.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/60-bridges.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/76-1-introduction.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/79-4-passport-passport-md.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/81-6-adapter-interface.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/83-8-q6-space-normative.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/85-10-query-flow.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/86-11-relevance-ranking.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/92-17-versioning-policy.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/02-anthropic-vacancies/96-21-adr-003-five-onboarding-paths-as-equal-rank.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/04-ai-collaborations/01-executive-summary.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/04-ai-collaborations/04-приоритетные-ансамбли.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/04-ai-collaborations/07-выводы.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/04-ai-collaborations/09-архитектурные-зазоры-которые-важнее-новых-инструме.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/04-ai-collaborations/10-новые-ансамбли-следующего-шага.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/04-ai-collaborations/13-контактная-стратегия-и-узкие-вопросы-для-авторов.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/05-habr-projects/02-collaboration-partners.md` (4 проблем)

_секция: 4_


### `docs/05-habr-projects/memory/ngt-memory.md` (4 проблем)

_секция: 4_


### `docs/HEALTH.md` (4 проблем)

_секция: 4_


### `docs/INDEX.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/LLM_SUMMARIES.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/ONBOARDING.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/SCORING.md` (4 проблем)

_секция: 4_


### `docs/SIMILAR.md` (4 проблем)

_секция: 4_


### `docs/contacts/QA.md` (4 проблем)

_секция: 4_


### `docs/lorenzo-agent/operationalized/06-conclusion-deserves-attention.md` (4 проблем)

_секция: 3, H1: 1_


### `docs/meta-scripting/03-catalog.md` (4 проблем)

_секция: 4_


### `docs/nautilus/composite-skills-agents/11-open-questions.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/composite-skills-agents/12-call-for-collaboration.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/composite-skills-agents/13-closing.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/00-abstract.md` (4 проблем)

_секция: 3, H1: 1_


### `docs/nautilus/double-triangle-architecture/01-why-single-triangle-incomplete.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/10-references.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/ingit-cowork-en/07-practical-first-steps.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/07-prakticheskie-shagi.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-0/03-registry.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-0/06-adapter-interface.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-0/09-query-flow.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-0/11-security-considerations.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-0/12-versioning-policy.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-1/03-registry.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-1/04-passport.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-1/06-adapter-interface.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-1/10-query-flow.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-1/11-relevance-ranking.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-1/14-sdk.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-1/15-security.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-1/17-versioning-policy.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/okwf-concept/06-governance-ethics.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/12-zaklyuchenie.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/07-governance-oversight.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/08-risks-mitigations.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/07-upravlenie-nadzor.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/12-zaklyuchenie.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/review-methodology/02-formal-workflow.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/review-methodology/05-conditions-of-applicability.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/review-methodology/06-relation-existing-methodologies.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/review-methodology/08-implementation-nautilus.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/review-methodology/09-limitations-open-questions.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/review-methodology/10-checklist.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/nautilus/review-methodology/14-main-technical-risks.md` (4 проблем)

_секция: 2, H1: 1, заголовок: 1_


### `docs/nautilus/review-methodology/15-appendix-c-history.md` (4 проблем)

_секция: 3, заголовок: 1_


### `docs/processing-guide/08-export.md` (4 проблем)

_секция: 4_


### `docs/processing-guide/09-automation.md` (4 проблем)

_секция: 4_


### `docs/processing-guide/10-future.md` (4 проблем)

_секция: 4_


### `docs/technology-combinations/combinations/21-legal-corpus-analytics-at-scale.md` (4 проблем)

_секция: 3, H1: 1_


### `docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md` (4 проблем)

_секция: 3, H1: 1_


### `docs/templates/ensemble.md` (4 проблем)

_секция: 4_


### `docs/01-svyazi/08-conclusions.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/01-svyazi/09-architectural-gaps.md` (3 проблем)

_секция: 3_


### `docs/01-svyazi/11-integration-contracts.md` (3 проблем)

_секция: 3_


### `docs/01-svyazi/13-contacts.md` (3 проблем)

_заголовок: 2, секция: 1_


### `docs/02-anthropic-vacancies/07-2-terminology.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/118-appendix-a-шаблон-для-header-warning.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/119-appendix-b-примеры-расхождений-и-их-разрешения.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/138-1-why-single-triangle-models-are-incomplete.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/17-5-compatibility-levels.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` (3 проблем)

_заголовок: 2, секция: 1_


### `docs/02-anthropic-vacancies/175-6-ethical-framework.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/176-7-governance-and-oversight.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/177-8-risks-and-mitigations.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/178-9-phased-rollout-strategy.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/200-10-открытые-вопросы.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/201-11-призыв-к-сотрудничеству.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/205-приложение-a-связь-с-сопроводительными-статьями.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/212-1-the-five-type-typology-of-principal-side-agents.md` (3 проблем)

_заголовок: 3_


### `docs/02-anthropic-vacancies/218-7-application-domains.md` (3 проблем)

_заголовок: 2, секция: 1_


### `docs/02-anthropic-vacancies/221-10-open-questions.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md` (3 проблем)

_заголовок: 3_


### `docs/02-anthropic-vacancies/232-1-типология-из-пяти-типов-агентов-на-стороне-принц.md` (3 проблем)

_заголовок: 3_


### `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/238-7-области-применения.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md` (3 проблем)

_заголовок: 3_


### `docs/02-anthropic-vacancies/265-12-call-for-collaboration.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/268-references.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/27-15-glossary-of-examples.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/270-appendix-b-sub-agent-registry-schema-sketch.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/287-references.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/290-почему-этот-документ-существует.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/294-существующие-приближения.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/297-что-промышленность-вероятно-построит.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/298-что-этот-документ-не-решает.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/300-заключение.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md` (3 проблем)

_заголовок: 2, секция: 1_


### `docs/02-anthropic-vacancies/313-5-four-integration-paths-in-order-of-accessibility.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/318-10-strategic-positioning.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/322-appendix-b-comparison-matrix.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/325-аннотация.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/327-1-открытие-cowork-и-почему-это-меняет-всё.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/331-5-четыре-пути-интеграции-в-порядке-доступности.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/332-6-уточнённый-объём-ingit-с-учётом-cowork.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/337-благодарности.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` (3 проблем)

_заголовок: 2, секция: 1_


### `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/349-твоя-личность.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/36-essence.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/46-essence.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/48-content-overview.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/56-essence.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/80-5-compatibility-levels.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/82-7-portalentry-structure.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/97-22-glossary-of-reference-examples.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/02-anthropic-vacancies/README.md` (3 проблем)

_секция: 3_


### `docs/03-technology-combinations/02-knowledge-graphs.md` (3 проблем)

_секция: 2, уровень: 1_


### `docs/04-ai-collaborations/00-intro.md` (3 проблем)

_секция: 3_


### `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/04-ai-collaborations/05-план-прототипа-и-возможные-контакты.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/04-ai-collaborations/08-что-это-продолжение-добавляет.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/05-habr-projects/knowledge/rufler.md` (3 проблем)

_секция: 3_


### `docs/AUTOFILLED.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/CHANGELOG_AUTO.md` (3 проблем)

_секция: 3_


### `docs/COMPONENT_MATRIX.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/DUPLICATES.md` (3 проблем)

_секция: 2, H1: 1_


### `docs/LANGUAGE_STATS.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/ORPHANS.md` (3 проблем)

_секция: 3_


### `docs/PROTOTYPE_SPEC.md` (3 проблем)

_секция: 3_


### `docs/READING_LIST.md` (3 проблем)

_секция: 3_


### `docs/READING_ORDER.md` (3 проблем)

_секция: 3_


### `docs/RISK_REGISTER.md` (3 проблем)

_секция: 3_


### `docs/SCRIPTS_CATALOG.md` (3 проблем)

_секция: 3_


### `docs/TECH_RADAR.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/ai-collaborations/candidates/01-three-key-candidates.md` (3 проблем)

_секция: 3_


### `docs/ai-collaborations/continuation/02-agentops-trace-envelope.md` (3 проблем)

_секция: 3_


### `docs/ai-collaborations/ensembles/3-forensic-rag.md` (3 проблем)

_секция: 3_


### `docs/anthropic-vacancies/beneficial-deployments-concept/11-not-and-format.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/anthropic-vacancies/nautilus-vs-camel/02-what-info-repos-contain.md` (3 проблем)

_секция: 2, H1: 1_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md` (3 проблем)

_секция: 3_


### `docs/anthropic-vacancies/signals.md` (3 проблем)

_секция: 3_


### `docs/contacts/anastasiyaw.md` (3 проблем)

_секция: 3_


### `docs/contacts/kksudo.md` (3 проблем)

_секция: 3_


### `docs/contacts/spbmolot.md` (3 проблем)

_секция: 3_


### `docs/contacts/vitalyoborin.md` (3 проблем)

_секция: 3_


### `docs/contacts/vitalysemenov.md` (3 проблем)

_секция: 3_


### `docs/glossary/concepts.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/analogues/01-three-direct-analogues.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/analogues/02-related-projects.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/deep-pairs/4-skill-catalogs-subagents.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/final-ensembles/4-summary-authors.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/hardware-pairs/2-tsu-mome.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/hardware-pairs/4-riscv-privacy.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/key-findings/01-yodoca.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/key-findings/04-dochkina-sequential.md` (3 проблем)

_секция: 3_


### `docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md` (3 проблем)

_секция: 3_


### `docs/lorenzo-agent/01-kto-ty.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/02-tvoyo-proishozhdenie.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/03-tvoya-missiya.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/04-komu-ty-sluzhish.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/05-tvoya-lichnost.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/07-chto-mozhesh.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/08-bez-max-approval.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/09-voobshche-nelzya.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/11-dhlab-documents.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/12-workflow.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/13-outreach-communication.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/14-other-ai-relationships.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/15-anti-patterns.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/16-vsegda-delaesh.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/17-honestly-ne-znaesh.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/18-escalate-to-max.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/19-persistent-character.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/20-experiment.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/naming/00-question-lorenzo-codename.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/lorenzo-agent/operationalized/02-minuses-1-10.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/meta-scripting/01-concept.md` (3 проблем)

_секция: 3_


### `docs/nautilus/community-discussions/habr-article-1-reaction/01-claude-response.md` (3 проблем)

_секция: 2, H1: 1_


### `docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/composite-skills-agents/03-what-makes-csa.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/composite-skills-agents-companion-mentors/02-what-was-missing-in-paper-6.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/09-acknowledgments.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/11-glossary.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/01-missing-middle-layer.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/02-why-document-exists.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/03-two-layer-stack.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/05-why-not-built.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/06-existing-approximations.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/08-recursive-insight.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/09-what-industry-will-build.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/10-what-not-solved.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/11-practical-recommendations.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/12-closing.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/01-zachem-dokument.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/02-dvukhsloynyy-stek.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/04-pochemu-ne-postroeno.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/05-priblizheniya.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/07-rekursivnoe-prozrenie.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/08-promyshlennost-postroit.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/09-ne-reshaet.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/10-rekomendatsii.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/11-zaklyuchenie.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/ingit-cowork-en/01-cowork-discovery.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/ingit-cowork-en/06-refined-ingit-scope.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/ingit-cowork-en/09-risks-open-questions.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/ingit-cowork-en/10-strategic-positioning.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/01-otkrytie-cowork.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/06-utochnyonnyy-obyom-ingit.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/09-riski-voprosy.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/10-strategicheskoe-pozitsionirovanie.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-0/02-terminology.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-0/04-passport.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-0/07-portal-entry.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-0/08-consensus-algorithm.md` (3 проблем)

_секция: 3_


### `docs/nautilus/npp-v1-0/10-query-result.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-0/13-reference-implementation.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-0/14-adr-001-federation-over-merging.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-0/17-appendix-b-change-log.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-1/00-abstract-status.md` (3 проблем)

_секция: 2, H1: 1_


### `docs/nautilus/npp-v1-1/01-introduction.md` (3 проблем)

_секция: 3_


### `docs/nautilus/npp-v1-1/02-terminology.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-1/05-compatibility-levels.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-1/07-portal-entry.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-1/08-q6-space.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-1/16-mcp-extension.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-1/18-reference-implementation.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-1/20-adr-002-q6-first-class.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/okwf-concept/01-problem-statement.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/okwf-concept/02-target-populations.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/okwf-concept/05-economic-model.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/okwf-concept/07-phased-rollout.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/okwf-concept/08-risk-analysis.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/okwf-concept/09-call-for-partnership.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/okwf-concept/10-appendices.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/privacy-federation/02-two-tier-publication.md` (3 проблем)

_секция: 2, H1: 1_


### `docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/04-architecture.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/10-open-questions.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/11-call-for-collaboration.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/10-otkrytye-voprosy.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/11-prizyv-k-sotrudnichestvu.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/01-cinderella-syndrome.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/05-architectural-specification.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/06-ethical-framework.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/09-phased-rollout.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/10-open-questions.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/11-call-for-collaboration.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/06-eticheskaya-ramka.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/08-riski-mery.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/10-otkrytye-voprosy.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/11-prizyv-k-sotrudnichestvu.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/review-methodology/00-tldr.md` (3 проблем)

_секция: 2, H1: 1_


### `docs/nautilus/review-methodology/01-context-motivation.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/review-methodology/03-consolidation-principles.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/review-methodology/11-application-plan-current-docs.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/review-methodology/13-appendix-b-examples.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/nautilus/review-methodology/16-glossary.md` (3 проблем)

_секция: 2, заголовок: 1_


### `docs/processing-guide/03-chunking.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/architecture/evidence-envelope.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/architecture/integration-spec.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/components/ai-factory.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/components/autoresearch-sequential.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/components/hybrid-rag.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/components/memnet.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/components/rufler.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/components/security-routing-plane.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/ensembles/G-federated-local-graph.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/overview/projects-map.md` (3 проблем)

_секция: 3_


### `docs/svyazi-2-0/security/default-policy.md` (3 проблем)

_секция: 3_


### `docs/technology-combinations/combinations/01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md` (3 проблем)

_секция: 3_


### `docs/technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md` (3 проблем)

_секция: 3_


### `docs/technology-combinations/combinations/14-local-first-agent-development-environment.md` (3 проблем)

_секция: 3_


### `docs/technology-combinations/combinations/18-llm-powered-legal-corpus-builder.md` (3 проблем)

_секция: 2, H1: 1_


### `docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md` (3 проблем)

_секция: 3_


### `docs/technology-combinations/combinations/28-pydantic-enforced-legal-workflows.md` (3 проблем)

_секция: 2, H1: 1_


### `docs/technology-combinations/combinations/29-meta-programmatic-legal-template-generator.md` (3 проблем)

_секция: 2, H1: 1_


### `docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md` (3 проблем)

_секция: 3_


### `docs/technology-combinations/research-reports/continuation-10-domains.md` (3 проблем)

_секция: 3_


### `docs/technology-combinations/synthesis-tables/01-08-summary.md` (3 проблем)

_секция: 3_


### `docs/templates/decision-record.md` (3 проблем)

_секция: 3_


### `docs/templates/research-note.md` (3 проблем)

_секция: 3_


### `docs/01-svyazi/01-executive-summary.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/01-svyazi/02-methodology.md` (2 проблем)

_секция: 2_


### `docs/01-svyazi/03-component-catalog.md` (2 проблем)

_секция: 2_


### `docs/01-svyazi/06-security-privacy.md` (2 проблем)

_секция: 2_


### `docs/01-svyazi/07-mvp-planning.md` (2 проблем)

_секция: 2_


### `docs/01-svyazi/10-second-order-ensembles.md` (2 проблем)

_секция: 2_


### `docs/01-svyazi/12-roadmap.md` (2 проблем)

_секция: 2_


### `docs/01-svyazi/14-limitations.md` (2 проблем)

_секция: 2_


### `docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/163-9-call-for-partnership.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/179-10-open-questions.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/226-appendix-a-comparative-table-five-agent-types.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/271-appendix-c-configuration-template-example.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/279-existing-approximations.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/68-about.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/77-2-terminology.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/03-technology-combinations/04-sozialrecht-domain.md` (2 проблем)

_секция: 2_


### `docs/05-habr-projects/knowledge/knowledge-space.md` (2 проблем)

_секция: 2_


### `docs/05-habr-projects/knowledge/mclaude.md` (2 проблем)

_секция: 2_


### `docs/05-habr-projects/knowledge/research-docs-liteparse.md` (2 проблем)

_секция: 2_


### `docs/05-habr-projects/memory/agent-memory-mcp.md` (2 проблем)

_секция: 2_


### `docs/05-habr-projects/memory/memnet.md` (2 проблем)

_секция: 2_


### `docs/CITATION_INDEX.md` (2 проблем)

_секция: 2_


### `docs/CLUSTERS.md` (2 проблем)

_секция: 2_


### `docs/COMPARE.md` (2 проблем)

_секция: 2_


### `docs/CONCEPTS.md` (2 проблем)

_секция: 2_


### `docs/CONTACTS.md` (2 проблем)

_секция: 2_


### `docs/CONTACT_PRIORITY.md` (2 проблем)

_секция: 2_


### `docs/CONTENT_GAPS.md` (2 проблем)

_секция: 2_


### `docs/DENSITY.md` (2 проблем)

_секция: 2_


### `docs/DIGEST_WEEKLY.md` (2 проблем)

_секция: 2_


### `docs/KNOWLEDGE_MAP.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/LINK_PREVIEW.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/MINDMAP.md` (2 проблем)

_секция: 2_


### `docs/PRIORITIES.md` (2 проблем)

_секция: 2_


### `docs/REPORT.md` (2 проблем)

_секция: 2_


### `docs/SEARCH_RESULTS.md` (2 проблем)

_секция: 2_


### `docs/SIMILAR_PASSAGES.md` (2 проблем)

_секция: 2_


### `docs/TASKS_INDEX.md` (2 проблем)

_секция: 2_


### `docs/WORD_CLOUD.md` (2 проблем)

_секция: 2_


### `docs/WORD_FREQ.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/candidates/02-related-projects-context.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/continuation/01-shared-memory-between-agents.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/continuation/05-roadmap-6-12-months.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/continuation/06-metrics-tree.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/continuation/08-commercialization-three-paths.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/continuation/09-do-not-glue.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/continuation/10-architecture-rfc.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/ensembles/1-agentic-knowledge-os.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/ensembles/2-distributed-agent-workshop.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/ensembles/4-web-to-knowledge-pipeline.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/ensembles/5-agent-firewall.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/ensembles/6-continuous-eval-loop.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md` (2 проблем)

_секция: 2_


### `docs/ai-collaborations/ensembles/9-ambient-team-agent.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/00-question-rephrasing.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/01-existing-landscape.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/02-four-structural-blockers.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/03-three-variants-A-B-C.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/04-what-to-do.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/05-polymath-project-tao-comparison.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/06-angel-vs-demon-duality.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/07-current-implementations.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/08-pluses-of-model.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/09-minuses-and-risks.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/ai-managed-virtual-company/10-three-entry-points.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/00-context.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/01-section-1-problem.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/02-section-2-beneficial-dimension.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/04-section-4-sgb-pilot.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/05-section-5-role-of-anthropic.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/06-section-6-proposer-role.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/07-section-7-success-metrics.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/08-section-8-risks-mitigations.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/09-section-9-timeliness.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/beneficial-deployments-concept/10-section-10-engagement-request.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/01-ai-research-engineering.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/02-sales.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/03-finance.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/04-security.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/05-marketing-brand.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/06-engineering-design-product.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/08-safeguards-trust-safety.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/09-product-management-support-ops.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/10-compute.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/11-legal.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/12-technical-program-management.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/13-communications.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/14-public-policy.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/15-public-benefit.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/clusters/16-people.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/extra-collaborator-findings/01-coally.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/extra-collaborator-findings/02-vitaly-graph-cognitive-memory.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/extra-collaborator-findings/07-key-observation.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/00-question-what-is-hermes.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/01-similarity-1-composite-skills.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/05-similarity-5-self-hosting-privacy.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/06-difference-1-structured-substrate-missing.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/07-difference-2-domain-specialization.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/08-difference-3-federation-missing.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/09-difference-4-institutional-vision.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/10-difference-5-tool-vs-mission-drift.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/11-pluses-of-hermes.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/12-minuses-of-hermes.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/hermes-comparison/13-reprioritization.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/mmorpg-for-programmers/00-question-mmorpg-for-programmers.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/mmorpg-for-programmers/01-why-stronger-than-it-looks.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/mmorpg-for-programmers/02-existing-niche.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/mmorpg-for-programmers/03-why-natural-for-programmers.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/mmorpg-for-programmers/04-pluses-as-business.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/mmorpg-for-programmers/05-minuses-as-business.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/nautilus-pro2-analysis/00-question-two-nautiluses.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/nautilus-pro2-analysis/02-nautilus-A-pro2-meta.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/nautilus-pro2-analysis/03-nautilus-B-meta-orchestrator.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/nautilus-vs-camel/00-question-camel-vs-nautilus.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/nautilus-vs-camel/01-passive-vs-active-roles.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/nautilus-vs-camel/04-what-to-take-from-info-repos.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/nautilus-vs-camel/05-what-to-do-right-now.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/overview.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/04-tertiary-research-engineer-agents.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/05-quaternary-developer-education.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/06-not-applicable-roles.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/07-unique-niche-eu-legal-infra.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/08-practical-ranking.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/02-three-overlapping-identities.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/03-revised-anthropic-mapping.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/04-non-anthropic-paths.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/05-reality-check-distribution-gap.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/01-three-archetypes.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/03-partial-fit-honesty.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md` (2 проблем)

_секция: 2_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/05-platform-not-position.md` (2 проблем)

_секция: 2_


### `docs/autofilled/README.md` (2 проблем)

_секция: 2_


### `docs/badges/README.md` (2 проблем)

_секция: 2_


### `docs/contacts/andrey-chuyan.md` (2 проблем)

_секция: 2_


### `docs/contacts/antipozitive.md` (2 проблем)

_секция: 2_


### `docs/contacts/cutcode.md` (2 проблем)

_секция: 2_


### `docs/contacts/dmitriila.md` (2 проблем)

_секция: 2_


### `docs/contacts/mixaill76.md` (2 проблем)

_секция: 2_


### `docs/contacts/nlaik.md` (2 проблем)

_секция: 2_


### `docs/contacts/sonia-black.md` (2 проблем)

_секция: 2_


### `docs/contacts/tagir-analyzes.md` (2 проблем)

_секция: 2_


### `docs/contacts/vladspace.md` (2 проблем)

_секция: 2_


### `docs/contacts/zodigancode.md` (2 проблем)

_секция: 2_


### `docs/glossary/authors-by-name.md` (2 проблем)

_секция: 2_


### `docs/glossary/components-by-name.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/deep-pairs/1-llm-gateway.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/deep-pairs/2-document-rag.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/deep-pairs/5-voice-local-memory.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/deep-pairs/6-tmux-village-openclaw.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/deep-pairs/7-autoresearch-distributed.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/00-question-habr-examples.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/01-svyazi-andrey-chuyan.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/02-vshe-scientific-networking.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/03-brainbox-multi-ai-hub.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/04-claude-subagents-patterns.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/05-hw-nl2workflow.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/06-platform-for-professional-communities.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/09-federated-platform.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/10-profession-specific-workflows.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/11-concrete-potential-collaborator.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/extra-examples/12-concrete-next-step.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/final-ensembles/1-one-person-one-company.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/final-ensembles/2-autoresearch-legal.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/final-ensembles/3-discovery-research.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/hardware-pairs/6-bonus-rram-memristor.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/hardware-pairs/7-metaphor.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/key-findings/02-memnet.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/software-pairs/1-workflow-llm-mcp.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/software-pairs/2-pkm-mcp-skills.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/software-pairs/3-crdt-self-hosted.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/software-pairs/4-speech-to-text-llm.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/software-pairs/5-browser-agents-headless.md` (2 проблем)

_секция: 2_


### `docs/habr-unique-projects/software-pairs/6-metaphor.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/00-intro.md` (2 проблем)

_H1: 1, секция: 1_


### `docs/lorenzo-agent/06-yazyki-kultura.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/10-collaborators-landscape.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/naming/01-search-results-not-found.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/naming/02-naming-rationale-lorenzo-medici.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/naming/03-dhlab-umbrella.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/operationalized/00-overview-grandchild-combination.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/operationalized/01-pluses-1-7.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/operationalized/03-honest-opinion.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/operationalized/04-recommendations.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/operationalized/05-anchor-node-habr-scout.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/phased-deployment/00-overview.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/phased-deployment/01-level-0-manual.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/phased-deployment/02-level-1-minimal-zero.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/phased-deployment/03-level-2-basic-lite.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/phased-deployment/04-level-3-medium-active.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/phased-deployment/05-level-4-extended-mature.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/phased-deployment/06-level-5-full-network.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/phased-deployment/07-progression-logic.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/phased-deployment/08-current-session-poc.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/scenarios/00-question-scenario.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/scenarios/01-response.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/00-context-fundamental-questions.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/01-q1-what-lorenzo-is.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/02-q2-whom-lorenzo-serves.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/03-q3-what-lorenzo-does.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/04-q4-character.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/05-q5-authority-limits.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/06-q6-accountability.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/07-q7-success-metrics.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/08-q8-other-ai-relationships.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/09-q9-geographic-linguistic-scope.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/10-q10-funding-model.md` (2 проблем)

_секция: 2_


### `docs/lorenzo-agent/specification/11-difficulties-and-recommendations.md` (2 проблем)

_секция: 2_


### `docs/nautilus/community-discussions/agent-changes-reality/00-question-agent-changes-reality.md` (2 проблем)

_секция: 2_


### `docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md` (2 проблем)

_секция: 2_


### `docs/nautilus/community-discussions/habr-article-2-reaction/00-question-habr-2.md` (2 проблем)

_секция: 2_


### `docs/nautilus/community-discussions/habr-article-2-reaction/01-response.md` (2 проблем)

_секция: 2_


### `docs/nautilus/community-discussions/practical-observations/00-question-practical.md` (2 проблем)

_секция: 2_


### `docs/nautilus/community-discussions/practical-observations/01-response.md` (2 проблем)

_секция: 2_


### `docs/nautilus/community-discussions/voiceless-contributors/00-question-voiceless.md` (2 проблем)

_секция: 2_


### `docs/nautilus/community-discussions/voiceless-contributors/01-response.md` (2 проблем)

_секция: 2_


### `docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/composite-skills-agents/04-sub-agent-registry.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/composite-skills-agents/05-configuration-ensembles.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/composite-skills-agents/06-coordination-disagreement.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/composite-skills-agents/07-economics-combinatorial.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/composite-skills-agents/08-seven-domains.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/composite-skills-agents/09-okwf-integration.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/composite-skills-agents/10-risks.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/composite-skills-agents-companion-mentors/00-question-multiple-mentors.md` (2 проблем)

_секция: 2_


### `docs/nautilus/composite-skills-agents-companion-mentors/01-yogi-metaphor.md` (2 проблем)

_секция: 2_


### `docs/nautilus/composite-skills-agents-companion-mentors/03-the-spectrum.md` (2 проблем)

_секция: 2_


### `docs/nautilus/double-triangle-architecture/02-double-triangle-architecture.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/04-nautilus-portal-substrate.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/07-open-questions.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/double-triangle-architecture/08-call-to-action.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/07-specific-case.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/00-intro.md` (2 проблем)

_секция: 2_


### `docs/nautilus/infrastructure-layer-b-ru/06-konkretnyy-sluchay.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/ingit-cowork-en/02-cowork-provides.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/ingit-cowork-en/03-ingit-provides.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/ingit-cowork-en/05-four-integration-paths.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/ingit-cowork-en/08-implications-nautilus-okwf.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/02-chto-cowork-obespechivaet.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/03-chto-ingit-obespechivaet.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/05-chetyre-puti-integratsii.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/08-implikatsii-nautilus-okwf.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/innovation-transitions/01-response.md` (2 проблем)

_секция: 2_


### `docs/nautilus/multi-tier-architecture/00-question-multi-tier.md` (2 проблем)

_секция: 2_


### `docs/nautilus/multi-tier-architecture/01-strategic-significance.md` (2 проблем)

_секция: 2_


### `docs/nautilus/npp-humanitarian-extension/00-question-can-it-apply-to-docs.md` (2 проблем)

_секция: 2_


### `docs/nautilus/npp-humanitarian-extension/02-mcp-claude-desktop-use-cases.md` (2 проблем)

_секция: 2_


### `docs/nautilus/npp-humanitarian-extension/03-what-doesnt-exist-on-market.md` (2 проблем)

_секция: 2_


### `docs/nautilus/npp-humanitarian-extension/04-grant-opportunities.md` (2 проблем)

_секция: 2_


### `docs/nautilus/npp-humanitarian-extension/05-which-combination-more-valuable.md` (2 проблем)

_секция: 2_


### `docs/nautilus/npp-v1-0/00-abstract-status.md` (2 проблем)

_H1: 1, секция: 1_


### `docs/nautilus/npp-v1-0/01-introduction.md` (2 проблем)

_секция: 2_


### `docs/nautilus/npp-v1-0/05-compatibility-levels.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/npp-v1-0/18-comment-on-document.md` (2 проблем)

_секция: 2_


### `docs/nautilus/npp-v1-1/12-onboarding-paths.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/npp-v1-1/13-rest-api.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/okwf-concept/03-why-existing-fail.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/okwf-concept/04-proposed-infrastructure.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/privacy-federation/00-question-anonymization.md` (2 проблем)

_секция: 2_


### `docs/nautilus/privacy-federation/01-what-to-anonymize-german-standard.md` (2 проблем)

_секция: 2_


### `docs/nautilus/privacy-federation/03-what-this-gives-technically.md` (2 проблем)

_секция: 2_


### `docs/nautilus/privacy-federation/04-what-i-can-do-now.md` (2 проблем)

_секция: 2_


### `docs/nautilus/professional-colleague-agents-en/03-empirical-case-obuchay.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/05-economics-replication.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/06-risks.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/07-application-domains.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/08-pilot-sgb-advocate.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/09-relationship-other-agents.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/12-closing.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/00-abstract.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/05-ekonomika.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/06-riski.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/07-oblasti-primeneniya.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/09-svyaz-s-drugimi.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/02-historical-precedents.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/03-what-makes-representative-agent.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/representative-agent-layer-en/04-ten-domains.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/00-abstract.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/review-methodology/07-why-valid-for-ai.md` (2 проблем)

_секция: 2_


### `docs/nautilus/review-methodology/12-appendix-a-header-warning.md` (2 проблем)

_секция: 1, заголовок: 1_


### `docs/nautilus/supply-demand/00-question-supply-demand.md` (2 проблем)

_секция: 2_


### `docs/nautilus/supply-demand/01-three-related-themes.md` (2 проблем)

_секция: 2_


### `docs/nautilus/transmission-box/00-question-mountain-to-person.md` (2 проблем)

_секция: 2_


### `docs/nautilus/transmission-box/01-completing-loop.md` (2 проблем)

_секция: 2_


### `docs/processing-guide/02-extraction.md` (2 проблем)

_секция: 2_


### `docs/processing-guide/04-structuring.md` (2 проблем)

_секция: 2_


### `docs/processing-guide/06-search.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/README.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/architecture/card-envelope.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/architecture/memory-write-policy.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/architecture/review-record.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/architecture/skill-tool-policy.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/agent-memory-mcp.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/agentfs.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/graph-rag.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/knowledge-space.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/legal-rag.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/mclaude.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/ngt-memory.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/research-docs-liteparse.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/self-aware-mcp.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/svyazi.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/voice-stack.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/yjs-automerge.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/components/yodoca.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/ensembles/A-collaboration-os.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/ensembles/B-forensic-rag.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/ensembles/C-multi-agent-factory.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/ensembles/D-voice-first-mesh.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/ensembles/E-execution-plane.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/ensembles/F-evidence-backed-intake.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/ensembles/H-research-to-product-flywheel.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/limitations/conclusions.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/limitations/do-not-glue.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/limitations/license-tree.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/outreach/first-contacts.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/outreach/message-template.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/outreach/narrow-questions.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/overview/continuation-intro.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/overview/executive-summary.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/overview/methodology.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/prototype/mvp-plan.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/prototype/risks.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/security/budget-routing.md` (2 проблем)

_секция: 2_


### `docs/svyazi-2-0/security/privacy.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/03-crdt-local-first-svyazi-cardindex.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/06-openclaude-utyokshiy-claude-code-zinc-inference-engine-mome-.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/09-agent-orchestration-stack.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/11-hybrid-crdt-sql-database.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/12-multi-agent-observability-stack.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/13-legal-document-transpiler.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/16-adversarial-multi-agent-code-review.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/17-distributed-agent-memory-with-graph.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/19-multi-agent-observability-platform.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/22-russian-international-oss-stack.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/23-security-first-code-review-pipeline.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/24-mega-integration-full-stack.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/27-hybrid-rag-with-ast-chunked-code.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/30-mega-stack-3-0-with-dsl-ast.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/combinations/34-distributed-event-store-with-paxos.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/mega-stacks/04-event-sourcing-consensus.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/properties/README.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/research-reports/sozialrecht-35-combinations.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/synthesis-tables/09-14-extended.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/synthesis-tables/15-19-extended.md` (2 проблем)

_секция: 2_


### `docs/technology-combinations/synthesis-tables/20-24-final.md` (2 проблем)

_секция: 2_


### `docs/templates/agent-spec.md` (2 проблем)

_секция: 2_


### `docs/templates/contact-outreach.md` (2 проблем)

_секция: 2_


### `docs/templates/kpi-snapshot.md` (2 проблем)

_секция: 2_


### `docs/templates/project-component.md` (2 проблем)

_секция: 2_


### `docs/01-svyazi/00-intro-part2.md` (1 проблем)

_секция: 1_


### `docs/01-svyazi/04-ensembles-overview.md` (1 проблем)

_секция: 1_


### `docs/01-svyazi/README.md` (1 проблем)

_секция: 1_


### `docs/02-anthropic-vacancies/87-12-onboarding-paths-normative.md` (1 проблем)

_заголовок: 1_


### `docs/03-technology-combinations/README.md` (1 проблем)

_секция: 1_


### `docs/04-ai-collaborations/README.md` (1 проблем)

_секция: 1_


### `docs/05-habr-projects/README.md` (1 проблем)

_секция: 1_


### `docs/05-habr-projects/knowledge/README.md` (1 проблем)

_секция: 1_


### `docs/05-habr-projects/knowledge/agentfs.md` (1 проблем)

_секция: 1_


### `docs/05-habr-projects/memory/README.md` (1 проблем)

_секция: 1_


### `docs/ACTION_ITEMS.md` (1 проблем)

_секция: 1_


### `docs/ALERTS.md` (1 проблем)

_секция: 1_


### `docs/BACKLINKS.md` (1 проблем)

_секция: 1_


### `docs/BROKEN_LINKS.md` (1 проблем)

_секция: 1_


### `docs/COMPLEXITY.md` (1 проблем)

_секция: 1_


### `docs/CONCEPT_GRAPH.md` (1 проблем)

_секция: 1_


### `docs/COST.md` (1 проблем)

_секция: 1_


### `docs/COVERAGE.md` (1 проблем)

_секция: 1_


### `docs/CROSSREFS.md` (1 проблем)

_секция: 1_


### `docs/CROSS_SECTION.md` (1 проблем)

_секция: 1_


### `docs/DECISIONS.md` (1 проблем)

_секция: 1_


### `docs/DEPENDENCY_MAP.md` (1 проблем)

_секция: 1_


### `docs/DIGEST_AUTO.md` (1 проблем)

_секция: 1_


### `docs/GRAPH.md` (1 проблем)

_секция: 1_


### `docs/KPI.md` (1 проблем)

_секция: 1_


### `docs/KPI_HISTORY.md` (1 проблем)

_секция: 1_


### `docs/MCP_DASHBOARD.md` (1 проблем)

_секция: 1_


### `docs/METRICS.md` (1 проблем)

_секция: 1_


### `docs/MISSING.md` (1 проблем)

_секция: 1_


### `docs/NAMED_ENTITIES.md` (1 проблем)

_секция: 1_


### `docs/NETWORK.md` (1 проблем)

_секция: 1_


### `docs/PASSIVE_VOICE.md` (1 проблем)

_секция: 1_


### `docs/QUESTIONS.md` (1 проблем)

_секция: 1_


### `docs/READING_TIME.md` (1 проблем)

_секция: 1_


### `docs/REGISTRY.md` (1 проблем)

_секция: 1_


### `docs/SEE_ALSO.md` (1 проблем)

_секция: 1_


### `docs/SENTIMENT.md` (1 проблем)

_секция: 1_


### `docs/SITEMAP.md` (1 проблем)

_секция: 1_


### `docs/SKILL_DASHBOARD.md` (1 проблем)

_секция: 1_


### `docs/SOURCE_MAP.md` (1 проблем)

_секция: 1_


### `docs/STALENESS.md` (1 проблем)

_секция: 1_


### `docs/STATS.md` (1 проблем)

_секция: 1_


### `docs/TAGS.md` (1 проблем)

_секция: 1_


### `docs/TIMELINE.md` (1 проблем)

_секция: 1_


### `docs/TOPIC_MODEL.md` (1 проблем)

_секция: 1_


### `docs/VERSION_DIFF.md` (1 проблем)

_секция: 1_


### `docs/ai-collaborations/README.md` (1 проблем)

_секция: 1_


### `docs/ai-collaborations/candidates/README.md` (1 проблем)

_секция: 1_


### `docs/ai-collaborations/channels/README.md` (1 проблем)

_секция: 1_


### `docs/ai-collaborations/continuation/README.md` (1 проблем)

_секция: 1_


### `docs/ai-collaborations/ensembles/README.md` (1 проблем)

_секция: 1_


### `docs/ai-collaborations/fast-tracks/README.md` (1 проблем)

_секция: 1_


### `docs/ai-collaborations/source-projects.md` (1 проблем)

_секция: 1_


### `docs/ai-collaborations/strategy/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/ai-managed-virtual-company/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/beneficial-deployments-concept/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/clusters/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/extra-collaborator-findings/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/hermes-comparison/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/methodology.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/mmorpg-for-programmers/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/nautilus-pro2-analysis/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/nautilus-vs-camel/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/profile-mapping/01-initial-analysis/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md` (1 проблем)

_секция: 1_


### `docs/anthropic-vacancies/profile-mapping/README.md` (1 проблем)

_секция: 1_


### `docs/autofilled/components/README.md` (1 проблем)

_секция: 1_


### `docs/contacts/README.md` (1 проблем)

_секция: 1_


### `docs/glossary/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/analogues/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/deep-pairs/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/evaluation/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/extra-examples/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/final-ensembles/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/hardware-pairs/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/key-findings/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/search-strategy/README.md` (1 проблем)

_секция: 1_


### `docs/habr-unique-projects/software-pairs/README.md` (1 проблем)

_секция: 1_


### `docs/lorenzo-agent/README.md` (1 проблем)

_секция: 1_


### `docs/lorenzo-agent/naming/README.md` (1 проблем)

_секция: 1_


### `docs/lorenzo-agent/operationalized/README.md` (1 проблем)

_секция: 1_


### `docs/lorenzo-agent/phased-deployment/README.md` (1 проблем)

_секция: 1_


### `docs/lorenzo-agent/scenarios/README.md` (1 проблем)

_секция: 1_


### `docs/lorenzo-agent/specification/README.md` (1 проблем)

_секция: 1_


### `docs/meta-scripting/05-synthesis.md` (1 проблем)

_секция: 1_


### `docs/meta-scripting/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/community-discussions/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/community-discussions/agent-changes-reality/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/community-discussions/habr-article-1-reaction/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/community-discussions/habr-article-2-reaction/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/community-discussions/practical-observations/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/community-discussions/voiceless-contributors/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/composite-skills-agents/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/composite-skills-agents-companion-mentors/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/double-triangle-architecture/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/infrastructure-layer-b-en/13-acknowledgments-refs.md` (1 проблем)

_заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-en/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/infrastructure-layer-b-ru/12-blagodarnosti-ssylki.md` (1 проблем)

_заголовок: 1_


### `docs/nautilus/infrastructure-layer-b-ru/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/ingit-cowork-en/04-symbiotic-architecture.md` (1 проблем)

_заголовок: 1_


### `docs/nautilus/ingit-cowork-en/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/ingit-cowork-ru/04-simbioticheskaya-arkhitektura.md` (1 проблем)

_заголовок: 1_


### `docs/nautilus/ingit-cowork-ru/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/innovation-transitions/00-question-innovations-transitions.md` (1 проблем)

_секция: 1_


### `docs/nautilus/innovation-transitions/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/multi-tier-architecture/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/npp-humanitarian-extension/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/npp-v1-0/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/npp-v1-1/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/okwf-concept/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/privacy-federation/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/professional-colleague-agents-en/01-five-type-typology.md` (1 проблем)

_заголовок: 1_


### `docs/nautilus/professional-colleague-agents-en/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/professional-colleague-agents-ru/01-pyat-tipov.md` (1 проблем)

_заголовок: 1_


### `docs/nautilus/professional-colleague-agents-ru/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/representative-agent-layer-en/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/representative-agent-layer-ru/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/review-methodology/04-fallback-ratio-question.md` (1 проблем)

_секция: 1_


### `docs/nautilus/review-methodology/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/supply-demand/README.md` (1 проблем)

_секция: 1_


### `docs/nautilus/transmission-box/README.md` (1 проблем)

_секция: 1_


### `docs/processing-guide/01-overview.md` (1 проблем)

_секция: 1_


### `docs/processing-guide/README.md` (1 проблем)

_секция: 1_


### `docs/reading-paths.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/architecture/README.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/architecture/gaps.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/components/README.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/ensembles/README.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/limitations/README.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/outreach/README.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/overview/README.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/prototype/README.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/prototype/roadmap.md` (1 проблем)

_секция: 1_


### `docs/svyazi-2-0/security/README.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/README.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/combinations/README.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/mega-stacks/01-legal-ai-stack.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/mega-stacks/02-ultimate-legal-ai.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/mega-stacks/03-dsl-ast.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/mega-stacks/README.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/research-reports/README.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/synthesis-tables/25-30-extended.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/synthesis-tables/31-35-final.md` (1 проблем)

_секция: 1_


### `docs/technology-combinations/synthesis-tables/README.md` (1 проблем)

_секция: 1_


### `docs/templates/README.md` (1 проблем)

_секция: 1_




## Использование
```bash
# Запуск
python scripts/improve_heading_audit.py
```
```bash
# Вариант 2
python scripts/improve_heading_audit.py --dry-run
```
```bash
# Вариант 3
python scripts/improve_heading_audit.py --dry-run
```
```bash
# Вариант 4
python scripts/improve_heading_audit.py --dry-run
```
```bash
# Вариант 5
python scripts/improve_heading_audit.py --dry-run
```

## Смотрите также

- [Главная](README.md)
- [Метрики](METRICS.md)
- [Дашборд](HEALTH.md)
- [Глоссарий](GLOSSARY.md)
- [Главная](README.md)
- [Метрики](METRICS.md)
- [Здоровье](HEALTH.md)
- [Глоссарий](GLOSSARY.md)
- [Сущности](ENTITIES.md)
- [Решения](DECISIONS.md)
- [Контакты](CONTACTS.md)
- [Оценка](SCORING.md)

<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [OUTLINE](OUTLINE.md)
- [READABILITY](READABILITY.md)
- [READING_TIME](READING_TIME.md)
- [README](README.md)
- [SEARCH](SEARCH.md)
- [SUMMARIES](SUMMARIES.md)
- [TABLES](TABLES.md)



## Использование
```bash
# Запуск
python scripts/improve_heading_audit.py
```
```bash
# Вариант 2
python scripts/improve_heading_audit.py --dry-run
```

<!-- see-also -->

---

**Смотрите также:**
- [PARAGRAPH_QUALITY](PARAGRAPH_QUALITY.md)
- [EMPTY_SECTIONS](EMPTY_SECTIONS.md)
- [READING_TIME](READING_TIME.md)
- [READABILITY](READABILITY.md)

