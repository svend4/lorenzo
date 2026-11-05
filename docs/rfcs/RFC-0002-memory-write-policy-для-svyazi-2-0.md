---
state: approved
rfc: "0002"
title: "Memory Write Policy для Svyazi 2.0"
status: Accepted
author: "svend4"
date: 2026-05-13
supersedes: ""
superseded_by: ""
tags: [architecture, rfc, memory, write-policy, mcp]
---

# RFC-0002: Memory Write Policy для Svyazi 2.0

<!-- toc-auto -->
<!-- tags: rfc-0002-memory-write-policy-для-svyazi-2-0, docs -->


<!-- summary -->
> title: "Memory Write Policy для Svyazi 2.0"
**Проекты:** Svyazi

---



> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

## Summary

Memory Write Policy определяет четыре типа записи в базу знаний Svyazi 2.0
(`episode`, `fact`, `proposal`, `decay_event`) и правила их применения,
обеспечивая атомарность, идемпотентность и трассируемость всех изменений.

## Motivation

После реализации Card Envelope (RFC-0001) и write-back инструментов в MCP и Gateway
возник вопрос: какие типы операций записи являются первоклассными гражданами системы?
Без политики записи возникает хаос: агенты пишут произвольные карточки, нет различия
между наблюдением (episode), выводом (fact), предложением (proposal) и устареванием (decay).
Это затрудняет аудит, replay и доверие к базе знаний.

## Design

### Четыре типа записи

| Тип | Семантика | card_type | Начальный state |
|-----|-----------|-----------|-----------------|
| `episode` | Наблюдение из взаимодействия (разговор, поиск) | `note` | `raw` |
| `fact` | Извлечённый факт с источником | `fact` | `raw` |
| `proposal` | Предложение интеграции двух проектов | `proposal` | `raw` |
| `decay_event` | Пометка устаревания существующей карточки | любой | `decayed` |

### Контракт Memory Write

```json
{
  "write_type": "episode | fact | proposal | decay_event",
  "card_type":  "note | fact | proposal | ...",
  "payload": {
    "title":   "...",
    "summary": "...(300 символов)...",
    "body":    "...(текст)...",
    "tags":    ["tag1"],
    "source_url": "https://..."
  },
  "edges": [{"to": "card_id", "rel": "references | extends | contradicts"}],
  "decay_target": "card_id (только для decay_event)"
}
```

### Правила применения

1. **episode** — пишется агентом немедленно, без ревью. `state: raw`.
2. **fact** — требует `source_url` или `edges` с источником. `state: raw` → promote по критериям RFC-0001.
3. **proposal** — создаётся `improve_proposal_gen.py` или MCP `propose_integration`. Всегда содержит `project_a`, `project_b`, `hypothesis`. `state: raw`.
4. **decay_event** — устанавливает `state: decayed` на целевую карточку. Атомарная операция. Нельзя отменить без явного `restore_event`.

### Идемпотентность

Перед записью `episode` и `fact` выполняется проверка дубликата (cosine ≥ 0.85 по title+body).
Если дубликат найден — запись пропускается, возвращается `{duplicate: true, existing_id: "..."}`.

### Аудит-след

Каждая операция записи добавляет в frontmatter карточки:
```yaml
write_type: episode
written_by: mcp | gateway | cli
written_at: 2026-05-13T10:00:00
```

## Alternatives Considered

| Альтернатива | Причина отклонения |
|-------------|-------------------|
| Единый тип write без семантики | Нет трассируемости, сложно строить аудит |
| Event-sourcing с отдельным журналом | Избыточная сложность для нашего масштаба |
| Версионирование карточек | Дорого по дисковому месту, не нужно для MVP |

## Drawbacks

- Агенты должны знать о типах записи (дополнительная ответственность).
- `decay_event` необратим без явного восстановления — риск потери данных при ошибке.

## Implementation

- [x] `gateway.py` — write-back с dedup и `state: raw` (реализовано)
- [x] `mcp_server.py` — `add_card`, `update_card_state`, `propose_integration` (реализовано)
- [x] `improve_card_promote.py` — promote lifecycle raw→normalized→approved (реализовано)
- [ ] Добавить поле `write_type` в frontmatter при записи через Gateway и MCP
- [ ] Реализовать `decay_event` как отдельный MCP-инструмент `decay_card`
- [ ] Добавить `restore_event` для отмены decay

## References

- [RFC-0001: Card Envelope](RFC-0001-card-envelope-contract.md)
- [PROTOTYPE_SPEC §3.3](../PROTOTYPE_SPEC.md)
- [11-integration-contracts](../01-svyazi/11-integration-contracts.md)

<!-- see-also -->

---

**Смотрите также:**
- [RFC-0003-mcp-write-back-protocol-для-svyazi-2-0](RFC-0003-mcp-write-back-protocol-для-svyazi-2-0.md)
- [RFC-0001-card-envelope-contract](RFC-0001-card-envelope-contract.md)
- [template](template.md)
- [card-envelope](../svyazi-2-0/architecture/card-envelope.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [READING_TIME](../READING_TIME.md)
- [README](README.md)
- [RFC-0001-card-envelope-contract](RFC-0001-card-envelope-contract.md)
- [RFC-0003-mcp-write-back-protocol-для-svyazi-2-0](RFC-0003-mcp-write-back-protocol-для-svyazi-2-0.md)
- [template](template.md)

