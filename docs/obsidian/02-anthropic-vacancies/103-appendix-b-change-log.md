---
title: "Appendix B: Change Log"
tags:
  - rag
  - architecture
  - anthropic-vacancies
date: 2026-05-14
---

# Appendix B: Change Log

<!-- toc-auto -->
## Contents

- [Appendix B: Change Log](#appendix-b-change-log)
  - [v1.1.0-draft (2026-04-19)](#v110-draft-2026-04-19)
  - [v1.0.0-draft (2026-04 earlier)](#v100-draft-2026-04-earlier)
- [Похожие документы](#похожие-документы)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в-1)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы-1)
- [Кто ссылается на этот документ (7)](#кто-ссылается-на-этот-документ-7)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы. New: Q6 as normative concept (section 8, ADR-002) New: Q6 as normative concept (section 8, ADR-002)
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> - **New**: Q6 as normative concept (section 8, ADR-002)

---
<!-- tags: rag, architecture -->




## Appendix B: Change Log

### v1.1.0-draft (2026-04-19)

- **New**: Q6 as normative concept (section 8, ADR-002)
- **New**: Five onboarding paths formalized (section 12, ADR-003)
- **New**: REST API contract mandatory (section 13)
- **New**: SDK contract informative (section 14)
- **New**: MCP extension informative (section 16)
- **Changed**: `is_fallback` field added to [[01-интегральный-анализ-профиля-svend4|PortalEntry]] (normative)
- **Changed**: Consensus structure extended with `coverage_with_fallback`
- **Changed**: Passport schema formalized via `passport_schema.json`
- **Clarified**: Naming conventions (passport by format, not by repo)
- **Clarified**: Timeout RECOMMENDED 5 seconds (was 10)

### v1.0.0-draft (2026-04 earlier)

- Initial draft published

---

<!-- similar-docs -->

---

## Похожие документы
- 91-16-[[91-16-mcp-extension-informative|mcp-extension-informative]] (сходство 0.13)
- [[82-7-portalentry-structure]] (сходство 0.11)
- [[93-18-reference-implementation]] (сходство 0.10)


<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Appendix B Change Log"
```

## Смотрите также
- 91-16-[[91-16-mcp-extension-informative|mcp-extension-informative]]
- [[22-10-queryresult-structure]]
- [[28-appendix-a-minimal-working-example]]
- [[93-18-reference-implementation]]

<!-- backlinks-auto -->
## Упоминается в

- 10. [[22-10-queryresult-structure|QueryResult Structure]]
- [[86-11-relevance-ranking|11. Relevance Ranking]]
- [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]]
- [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]]
- [[81-6-adapter-interface|6. Adapter Interface]]
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]]
- [[104-appendix-c-references|Appendix C: References]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
- [[128-доступные-инструменты|Доступные инструменты]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]] _29%_
- [[128-доступные-инструменты|Доступные инструменты]] _21%_
- 10. [[22-10-queryresult-structure|QueryResult Structure]] _21%_
- [[81-6-adapter-interface|6. Adapter Interface]] _21%_
- [[93-18-reference-implementation|18. Reference Implementation]] _21%_
- [[104-appendix-c-references|Appendix C: References]] _17%_
## Связанные документы

- [[104-appendix-c-references|Appendix C: References]] _25%_
- 10. [[22-10-queryresult-structure|QueryResult Structure]] _25%_
- [[89-14-sdk-contract-informative|14. SDK Contract (Informative)]] _25%_
- [[91-16-mcp-extension-informative|16. MCP Extension (Informative)]] _25%_
- [[128-доступные-инструменты|Доступные инструменты]] _21%_
- [[34-appendix-b-change-log|Appendix B: Change Log]] _21%_
- [[81-6-adapter-interface|6. Adapter Interface]] _21%_
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]] _21%_

<!-- backlinks -->

---

## Кто ссылается на этот документ (7)
- [[104-appendix-c-references]]
- [[128-доступные-инструменты]]
- [[22-10-queryresult-structure]]
- [[34-appendix-b-change-log]]
- 91-16-[[91-16-mcp-extension-informative|mcp-extension-informative]]
- [[93-18-reference-implementation]]
- [[README]]

