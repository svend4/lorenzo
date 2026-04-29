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
- [11-integration-contracts](docs/01-svyazi/11-integration-contracts.md)
- [11-интеграционный-контракт-который-стоит-зафиксироват](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)
- [integration-spec](docs/svyazi-2-0/architecture/integration-spec.md)
- [review-record](docs/svyazi-2-0/architecture/review-record.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [11-integration-contracts](docs/01-svyazi/11-integration-contracts.md) (сходство 0.21)
- [integration-spec](docs/svyazi-2-0/architecture/integration-spec.md) (сходство 0.21)
- [11-integration-contracts](docs/obsidian/01-svyazi/11-integration-contracts.md) (сходство 0.20)

