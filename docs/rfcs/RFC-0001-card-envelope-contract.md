---
state: normalized
rfc: "0001"
title: "Card Envelope как единый контракт данных Svyazi 2.0"
status: Accepted
author: "svend4"
date: 2026-05-13
supersedes: ""
superseded_by: ""
tags: [architecture, rfc, card-envelope, core]
---

# RFC-0001: Card Envelope как единый контракт данных Svyazi 2.0


<!-- summary -->
> Card Envelope — единый формат хранения любого знания в системе Svyazi 2.0. Все компоненты (AgentFS, Yodoca, MCP, Gateway) обмениваются только через Card Envelope.
Summary
Card Envelope — единый формат хранения любого знания в системе Svyazi 2.0.

## Summary

Card Envelope — единый формат хранения любого знания в системе Svyazi 2.0.
Все компоненты (AgentFS, Yodoca, MCP, Gateway) обмениваются только через Card Envelope.

## Motivation

Без общего формата каждый компонент создаёт своё представление данных.
AgentFS хранит файлы, Yodoca хранит episodes, CardIndex хранит JSON —
три несовместимых формата для одного понятия «карточка знания».

## Design

```json
{
  "card_id":      "sha256:...",
  "card_type":    "doc | note | fact | person | project | event | proposal",
  "state":        "raw | normalized | approved | rejected | decayed",
  "sources":      ["url", "file_path"],
  "edges":        [{"to": "card_id", "rel": "references | contradicts | extends"}],
  "created_at":   "ISO-8601",
  "updated_at":   "ISO-8601",
  "payload_hash": "sha256:...",
  "payload":      {
    "title":   "...",
    "summary": "...(300 символов)...",
    "body":    "...(800 слов)...",
    "tags":    ["tag1", "tag2"]
  }
}
```

### Инварианты

1. `card_id` — иммутабельный, SHA256 от начального контента
2. `state` — монотонно растёт: raw → normalized → approved (нельзя откатиться без явного decay)
3. `edges` — направленные, типизированные рёбра к другим card_id
4. `payload` — расширяемый, но `title` + `summary` обязательны для normalized

## Alternatives Considered

| Альтернатива | Причина отклонения |
|-------------|-------------------|
| Yodoca-native format | BSL 1.1 лицензия, зависимость от внешнего API |
| JSON-LD / RDF | Избыточная сложность для нашего масштаба |
| Flat файлы без metadata | Нет жизненного цикла и графа |

## Implementation

- [x] `utils_card_envelope.py` — базовая реализация
- [x] `improve_card_index.py` — CardStore
- [x] `gateway.py` — write-back через Card Envelope
- [x] `mcp_server.py` — add_card, update_card_state
- [x] `improve_card_promote.py` — промоушен состояний

## References

- [PROTOTYPE_SPEC §3.1](../PROTOTYPE_SPEC.md)
- [11-integration-contracts](../01-svyazi/11-integration-contracts.md)
