# Skill and Tool Policy

<!-- toc-auto -->
## Contents

- [Минимальные поля](#минимальные-поля)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (4)](#кто-ссылается-на-этот-документ-4)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».
**Проекты:** SENTINEL, LiteLLM, Auto AI Router, Tool Search

---
<!-- tags: security, architecture -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Skill and Tool Policy"
```

## Смотрите также
- [11-integration-contracts](../../01-svyazi/11-integration-contracts.md)
- [11-интеграционный-контракт-который-стоит-зафиксироват](../../04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)
- [integration-spec](integration-spec.md)
- [review-record](review-record.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (4)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)
- [integration-spec](integration-spec.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал индексирован и доступен для поиска, BM25 и навигации через граф концептов._ _Документ доступен для семантического поиска._ _Индексировано._

<!-- similar-docs -->

---

**Похожие документы:**
- [skill-tool-policy](../../obsidian/svyazi-2-0/architecture/skill-tool-policy.md) (сходство 0.97)
- [memory-write-policy](memory-write-policy.md) (сходство 0.34)
- [memory-write-policy](../../obsidian/svyazi-2-0/architecture/memory-write-policy.md) (сходство 0.33)

