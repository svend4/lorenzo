---
title: "Personal multi-agent hub"
tags:
  - architecture
  - anthropic
  - collaboration
  - habr-unique-projects
date: 2026-05-13
---

# Personal multi-agent hub

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — расширенные примеры с Хабра по варианту D (поиск ещё уникальных проектов).

---
<!-- tags: architecture, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — расширенные примеры с Хабра по варианту D (поиск ещё уникальных проектов).

Что получается: Personal multi-agent hub:

Local AI infrastructure (BrainBox-style hosting)

Files-as-config для agent roles (.ai/agents/ pattern)

Decomposition patterns (WorkTeam supervisor → orchestrator → filler)

CAMEL для actual coordination

Применение: Personal SGB Advocate с specialized sub-agents:

agents/01_legal_research.md — для поиска precedent

agents/02_drafting.md — для составления документов

agents/03_citation_checker.md — для проверки ссылок

agents/04_strategic_advisor.md — для общей стратегии

Все work через CAMEL coordination, hosted locally в style BrainBox.

Это очень близко к Document 7 (Composite Skills Agent), но с конкретными templates и patterns из real Хабр-работающих проектов.

Синтез D: «Federated knowledge marketplace для уязвимых групп»

Совмещение: Свяжи (collaboration matching) + info40 (marketplace concept) + Document 5 (Representative Agent Layer) + Nautilus Portal Protocol (Document 1).

<!-- see-also -->

---

**Смотрите также:**
- [[07-specialized-knowledge-workspace]]
- [[06-platform-for-professional-communities]]
- [[09-federated-platform]]
- [[04-claude-subagents-patterns]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[07-specialized-knowledge-workspace]] (сходство 0.34)
- [[06-platform-for-professional-communities]] (сходство 0.32)
- [[09-federated-platform]] (сходство 0.31)


<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [READABILITY](../../../READABILITY.md)
- [READING_TIME](../../../READING_TIME.md)
- [SEARCH](../../../SEARCH.md)
- [TABLES](../../../TABLES.md)
- [03-sgb-advocate-colleague-example](../../../anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md)
- [05-hw-nl2workflow](../../../habr-unique-projects/extra-examples/05-hw-nl2workflow.md)
- [07-specialized-knowledge-workspace](../../../habr-unique-projects/extra-examples/07-specialized-knowledge-workspace.md)
- [08-personal-multi-agent-hub](../../../habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md)

