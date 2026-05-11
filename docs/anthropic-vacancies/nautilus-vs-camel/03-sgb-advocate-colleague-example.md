# Конкретный пример: SGB Advocate Colleague на этой архитектуре

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

---
<!-- tags: architecture, anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Конкретный пример SGB Advocate"
```

## Смотрите также
- [08-personal-multi-agent-hub](../../habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md)
- [04-what-to-take-from-info-repos](04-what-to-take-from-info-repos.md)
- [09-federated-platform](../../habr-unique-projects/extra-examples/09-federated-platform.md)
- [01-passive-vs-active-roles](01-passive-vs-active-roles.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [01-passive-vs-active-roles](01-passive-vs-active-roles.md)
- [02-what-info-repos-contain](02-what-info-repos-contain.md)
- [04-what-to-take-from-info-repos](04-what-to-take-from-info-repos.md)
- [05-what-to-do-right-now](05-what-to-do-right-now.md)
- _...ещё 1_

