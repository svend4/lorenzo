---
title: "12. Versioning Policy"
tags:
  - architecture
  - anthropic-vacancies
date: 2026-04-29
---

# 12. Versioning Policy

<!-- toc-auto -->
## Contents

- [12. Versioning Policy](#12-versioning-policy)
  - [12.1. Semver](#121-semver)
  - [12.2. Version in Registry](#122-version-in-registry)
  - [12.3. Breaking Changes Process](#123-breaking-changes-process)


<!-- summary -->
> - **Major** (v1 → v2): breaking changes в interfaces или schemas

---
<!-- tags: architecture -->




## 12. Versioning Policy

### 12.1. Semver

NPP следует semver:

- **Major** (v1 → v2): breaking changes в interfaces или schemas
- **Minor** (v1.0 → v1.1): новая функциональность, backward-compatible
- **Patch** (v1.0.0 → v1.0.1): clarifications, typo fixes

### 12.2. Version in Registry

Каждый registry MUST объявлять `protocol_version`. Portal 
implementation MUST поддерживать **минимум текущую major version**.

### 12.3. Breaking Changes Process

Для major version bump требуется:

1. RFC в Issues репо Portal с обоснованием
2. Минимум 30 дней обсуждения
3. Migration guide для существующих адаптеров
4. Опубликованная compatibility shim в Portal для переходного 
   периода (минимум 6 месяцев)

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[92-17-versioning-policy]] (сходство 0.63)
- [[05-0-status-of-this-document]] (сходство 0.14)
- [[75-0-status-of-this-document]] (сходство 0.13)


<!-- see-also -->

---

**Смотрите также:**
- [[92-17-versioning-policy]]
- [[05-0-status-of-this-document]]
- [[75-0-status-of-this-document]]
- [[03-portal-protocol-md]]

<!-- backlinks-auto -->
## Упоминается в

- [[05-0-status-of-this-document|0. Status of This Document]]
- [[75-0-status-of-this-document|0. Status of This Document]]
- [[92-17-versioning-policy|17. Versioning Policy]]
- [[114-7-реализация-в-проекте-nautilus|7. Реализация в проекте Nautilus]]
- [[42-author-contact|Author & Contact]]
- [[62-author-contact|Author & Contact]]
- [[03-portal-protocol-md|PORTAL-PROTOCOL.md]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
- [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[92-17-versioning-policy|17. Versioning Policy]] _81%_
- [[62-author-contact|Author & Contact]] _37%_
- [[42-author-contact|Author & Contact]] _33%_
- [[75-0-status-of-this-document|0. Status of This Document]] _33%_
- [[05-0-status-of-this-document|0. Status of This Document]] _29%_
- [[25-13-reference-implementation|13. Reference Implementation]] _29%_
- [[93-18-reference-implementation|18. Reference Implementation]] _29%_
- [[03-portal-protocol-md|PORTAL-PROTOCOL.md]] _21%_
## Связанные документы

- [[92-17-versioning-policy|17. Versioning Policy]] _81%_
- [[05-0-status-of-this-document|0. Status of This Document]] _29%_
- [[42-author-contact|Author & Contact]] _29%_
- [[62-author-contact|Author & Contact]] _29%_
- [[75-0-status-of-this-document|0. Status of This Document]] _29%_
- [[03-portal-protocol-md|PORTAL-PROTOCOL.md]] _25%_
- [[TIMELINE|Хронологическая лента событий]] _25%_
- [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]] _21%_
