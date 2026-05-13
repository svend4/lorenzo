---
state: approved
rfc: "0003"
title: "MCP Write-back Protocol для Svyazi 2.0"
status: Accepted
author: "svend4"
date: 2026-05-13
supersedes: ""
superseded_by: ""
tags: [architecture, rfc, mcp, write-back, protocol]
---

# RFC-0003: MCP Write-back Protocol для Svyazi 2.0

## Summary

MCP Write-back Protocol определяет 4 новых инструмента MCP-сервера
(`add_card`, `update_card_state`, `propose_integration`, `list_cards`),
их входные/выходные контракты и правила безопасного взаимодействия
Claude Desktop с базой знаний Svyazi 2.0.

## Motivation

MCP-сервер Svyazi 2.0 изначально был read-only: 11 инструментов для поиска
и чтения, ноль инструментов для записи. Claude Desktop не мог сохранять
артефакты разговора в базу знаний. Это разрывало петлю обратной связи:
агент находил знание, но не мог его обогатить или зафиксировать вывод.

## Design

### Новые MCP-инструменты

#### `add_card`

Добавляет новую карточку знания.

**Input:**
```json
{
  "title":      "string (required)",
  "content":    "string (required, min 50 chars)",
  "section":    "string (default: 04-ai-collaborations)",
  "tags":       "string (comma-separated)",
  "source_url": "string (optional)"
}
```

**Output:**
```json
{
  "path":      "docs/...",
  "card_id":   "sha256:...",
  "duplicate": false,
  "message":   "Card added successfully"
}
```

**Dedup:** перед записью выполняется cosine similarity ≥ 0.85 по top-200 TF-IDF.
Если дубликат — возвращает `{duplicate: true, existing_path: "..."}` без записи.

#### `update_card_state`

Изменяет state карточки по жизненному циклу RFC-0001.

**Input:**
```json
{
  "path":      "docs/... (required)",
  "new_state": "raw | normalized | approved | rejected | decayed",
  "reason":    "string (optional)"
}
```

**Правила:** только вперёд по графу состояний (raw→normalized→approved).
Разрешён переход в `rejected` и `decayed` из любого состояния.

#### `propose_integration`

Создаёт карточку-предложение интеграции двух проектов.

**Input:**
```json
{
  "project_a":  "string (required)",
  "project_b":  "string (required)",
  "hypothesis": "string (required)",
  "rationale":  "string (optional)"
}
```

**Output:** путь созданной карточки `docs/04-ai-collaborations/proposals/`.

#### `list_cards`

Список карточек с фильтрами.

**Input:**
```json
{
  "state":   "raw | normalized | approved | all (default: all)",
  "section": "string (optional)",
  "limit":   "integer (default: 20, max: 100)"
}
```

### Транспорт и безопасность

- Транспорт: **stdio** (Claude Desktop совместимый).
- Аутентификация: не требуется (локальный процесс).
- Rate limit: нет на стороне сервера, но `add_card` блокируется на 100ms между вызовами
  для предотвращения flood-записи.
- Файловая система: все пути санируются через `Path(ROOT / path).resolve()`,
  выход за пределы `ROOT` запрещён.

### Инварианты

1. `add_card` никогда не перезаписывает существующий файл — использует UUID-суффикс.
2. `update_card_state` не понижает state (нет approved→normalized).
3. После каждой записи обновляется `passages.json` (инкрементально).
4. Все операции логируются в `audit.db` (если доступен `improve_audit_db.py`).

## Alternatives Considered

| Альтернатива | Причина отклонения |
|-------------|-------------------|
| HTTP REST вместо stdio | Требует отдельного процесса, сложнее для Claude Desktop |
| GraphQL mutation | Избыточно для 4 инструментов |
| Прямой доступ к файлам без MCP | Нет контроля, нет audit trail |

## Drawbacks

- stdio транспорт не поддерживает параллельные запросы (один клиент за раз).
- После `add_card` нужно вручную запустить `improve_card_promote.py` для промоушена.

## Implementation

- [x] `mcp_server.py` — все 4 инструмента реализованы
- [x] `gateway.py` — аналогичный write-back через HTTP
- [x] Dedup через `_find_dup()` (cosine ≥ 0.85)
- [x] Passages sync через `_sync_passages_mcp()`
- [ ] Rate limiting (100ms задержка)
- [ ] Интеграция с `audit.db` для полного audit trail
- [ ] Понижение state только через явный `decay_card` (RFC-0002)

## References

- [RFC-0001: Card Envelope](RFC-0001-card-envelope-contract.md)
- [RFC-0002: Memory Write Policy](RFC-0002-memory-write-policy-для-svyazi-2-0.md)
- [PROTOTYPE_SPEC §3.3](../PROTOTYPE_SPEC.md)
- [MCP сервер](../../scripts/mcp_server.py)
