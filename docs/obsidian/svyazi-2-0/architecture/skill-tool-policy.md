---
title: "Skill and Tool Policy"
tags:
  - security
  - architecture
  - svyazi-2-0
date: 2026-05-13
---

# Skill and Tool Policy

<!-- summary -->
> > Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».
**Проекты:** SENTINEL, LiteLLM, Auto AI Router, Tool Search

---
<!-- tags: security, architecture -->




> Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».

Каждый skill или MCP‑инструмент должен иметь класс доступа, класс среды, условия вызова и postcondition. Простейшее разбиение: `read`, `annotate`, `plan`, `mutate`, `publish`, `external_send`. Это дополняет Tool Search, который экономит контекст, но сам по себе не задаёт governance; LiteLLM и Auto AI Router, которые управляют провайдерами, но не правами; и SENTINEL, который контролирует угрозы, но выигрывает от того, что политика уже структурирована, а не размазана по промптам. citeturn39view1turn11search2turn39view0turn20view10

## Минимальные поля

- `tool_class` — `read` | `annotate` | `plan` | `mutate` | `publish` | `external_send`
- `approval_mode` — авто / требует подтверждения
- `path_scope` — какие пути на диске разрешены
- `network_scope` — какие домены/endpoint'ы разрешены
- `output_target` — куда уходит результат (memory? user UI? external?)

<!-- see-also -->

---

**Смотрите также:**
- [[11-integration-contracts]]
- [[11-интеграционный-контракт-который-стоит-зафиксироват]]
- [[integration-spec]]
- [[review-record]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[11-integration-contracts]] (сходство 0.21)
- [[integration-spec]] (сходство 0.21)
- [[11-integration-contracts]] (сходство 0.20)


<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [READABILITY](../../../READABILITY.md)
- [READING_TIME](../../../READING_TIME.md)
- [SEARCH](../../../SEARCH.md)
- [TABLES](../../../TABLES.md)
- [skill-tool-policy](../../../svyazi-2-0/architecture/skill-tool-policy.md)

