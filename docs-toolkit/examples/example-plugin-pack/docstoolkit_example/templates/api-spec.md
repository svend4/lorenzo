---
template: api-spec
version: "1.0"
api_name: "[Название API]"
api_version: "0.1.0"
auth_type: "[bearer|oauth2|api-key|none]"
base_url: "[https://api.example.com]"
created: 2026-04-29
tags: [api, спецификация]
---

# API: [Название]

<!-- summary: REST API спецификация -->
<!-- tags: api, спецификация -->

## Базовый URL

`[https://api.example.com/v1]`

## Аутентификация

`[bearer | oauth2 | api-key | none]`

## Endpoints

### GET /resource

[Описание]

**Параметры:**
- `param1` (required) — описание

**Ответ:**
```json
{
  "field": "value"
}
```

## Коды ошибок

| Код | Описание |
|-----|----------|
| 400 | Bad request |
| 401 | Unauthorized |
| 404 | Not found |

---
_Создано: 2026-04-29_
