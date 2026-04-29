---
title: "14. ADR-001: Federation over Merging"
tags:
  - architecture
  - anthropic
  - collaboration
  - nautilus
date: 2026-04-29
---

# 14. ADR-001: Federation over Merging

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: architecture, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 14. ADR-001: Federation over Merging

**Status:** Accepted

**Context:** При построении системы knowledge management встаёт 
выбор: заставить все данные мигрировать в единую схему (merge), 
либо сохранить разные native-форматы и переводить по необходимости 
(federation).

**Decision:** Выбрана federation.

**Consequences:**

**Positive:**
- Low barrier to entry: существующие Repos подключаются без 
рефакторинга
- Authorship preserved: каждый автор работает в своей модели
- Multi-angle views: один концепт может существовать в трёх Repos 
с тремя разными углами одновременно

**Negative:**
- Cross-repo queries дороже: требуется вызов всех адаптеров
- Consensus нетривиален: string matching — аппроксимация, не 
formal mapping
- Bridges — текстовые описания, не machine-executable

**Alternatives rejected:**
- Unified RDF/OWL ontology: слишком высокий barrier to entry
- Centralized database: нарушает принцип local autonomy
- Schema-less dump: теряется семантика angles

---

<!-- see-also -->

---

**Смотрите также:**
- [[19-adr-001-federation-over-merging]]
- [[26-14-adr-001-federation-over-merging]]
- [[94-19-adr-001-federation-over-merging]]
- [[20-adr-002-q6-first-class]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[19-adr-001-federation-over-merging]] (сходство 0.85)
- [[26-14-adr-001-federation-over-merging]] (сходство 0.75)
- [[26-14-adr-001-federation-over-merging]] (сходство 0.74)

