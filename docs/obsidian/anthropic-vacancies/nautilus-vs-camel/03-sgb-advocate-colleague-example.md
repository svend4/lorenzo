---
title: "Конкретный пример: SGB Advocate Colleague на этой архитектуре"
tags:
  - architecture
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# Конкретный пример: SGB Advocate Colleague на этой архитектуре

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

Конкретный example: SGB Advocate Colleague на этой архитектуре

Как это могло бы work для concrete case:

Layer 1 — CAMEL substrate:

One CAMEL deployment per practitioner (or per organization)

Workforce coordinator coordinates specialized sub-agents

Sub-agents: SGB statute interpreter, KSV Sachsen pattern specialist, court procedure advisor, medical assessment integrator

Layer 2 — Domain MCP servers:

mcp-sgb-ix — SGB IX statute knowledge

mcp-sgb-xii — SGB XII statute knowledge

mcp-sozialgericht-procedures — court procedural patterns

mcp-ksv-sachsen-history — patterns from KSV Sachsen disputes

These MCP servers portable — usable от других agent frameworks too.

Layer 3 — Nautilus federation:

Practitioners' deployments expose Portal Protocol

New patterns (successful arguments, useful templates) shared через federation

Nautilus provides discovery: «who has handled cases like this?»

Layer 4 — Marketplace economy (longer term):

Volunteer pool: free access для disabled persons advocacy work

Commercial tier: paid services for legal firms

Hybrid: foundations subsidize volunteer pool через commercial revenues

This synthesizes:

info7's Professional Agent specialization

info40's marketplace economy

CAMEL's working multi-agent infrastructure

Nautilus federation

MCP interoperability

Каждый component legitimate, working architecture, не speculation.

<!-- see-also -->

---

**Смотрите также:**
- [[08-personal-multi-agent-hub]]
- [[04-what-to-take-from-info-repos]]
- [[09-federated-platform]]
- [[01-passive-vs-active-roles]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[08-personal-multi-agent-hub]] (сходство 0.24)
- [[09-federated-platform]] (сходство 0.23)
- [[04-what-to-take-from-info-repos]] (сходство 0.20)

