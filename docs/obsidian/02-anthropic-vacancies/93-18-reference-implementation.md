---
title: "18. Reference Implementation"
tags:
  - rag
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

# 18. Reference Implementation

<!-- summary -->
> [`github.com/svend4/nautilus`](https://github.com/svend4/nautilus).

---
<!-- tags: rag, collaboration -->




## 18. Reference Implementation

Reference implementation: 
[`github.com/svend4/nautilus`](https://github.com/svend4/nautilus).

Reference НЕ является нормативной. Альтернативные implementations 
NPP-compatible, если они:

- Корректно парсят `nautilus.json` per раздел 3
- Реализуют BaseAdapter interface per раздел 6
- Производят PortalEntry структуры per раздел 7
- Обеспечивают Q6 для Level 2+ per раздел 8
- Вычисляют consensus per раздел 9
- Предоставляют required REST endpoints per раздел 13

### 18.1. Current Reference Implementation Metrics

(Informative snapshot, v1.1.0-draft, 2026-04-19)

| Метрика | Значение |
|---------|----------|
| Python LOC | 6 782 |
| Адаптеров | 13 (7 реестровых + 6 расширенных) |
| Тестов | 60 / 60 passing |
| mypy errors | 0 |
| Внешних зависимостей | 0 (stdlib only) |
| Health Score | 82 / 100 |
| Q6 coverage (real) | 21.9% (14 / 64 vertices) |

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[25-13-reference-implementation]] (сходство 0.36)
- [[73-portal-protocol-md-v1-1]] (сходство 0.13)
- [[89-14-sdk-contract-informative]] (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [[25-13-reference-implementation]]
- [[42-author-contact]]
- [[73-portal-protocol-md-v1-1]]
- [[03-portal-protocol-md]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[25-13-reference-implementation|13. Reference Implementation]] _81%_
- [[42-author-contact|Author & Contact]] _60%_
- [[62-author-contact|Author & Contact]] _48%_
- [[05-0-status-of-this-document|0. Status of This Document]] _37%_
- [[75-0-status-of-this-document|0. Status of This Document]] _37%_
- [[104-appendix-c-references|Appendix C: References]] _33%_
- [[35-passports-info1-md|passports/info1.md]] _33%_
- [[52-author-contact|Author & Contact]] _33%_
