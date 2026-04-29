---
title: "13. REST API Contract (Normative for Portals)"
tags:
  - rag
  - architecture
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

# 13. REST API Contract (Normative for Portals)

<!-- toc -->
## Содержание

- [Contents](#contents)
- [13. REST API Contract (Normative for Portals)](#13-rest-api-contract-normative-for-portals)
  - [13.1. Required Endpoints](#131-required-endpoints)
  - [13.2. Recommended Endpoints](#132-recommended-endpoints)
  - [13.3. Response Schemas](#133-response-schemas)
  - [13.4. CORS](#134-cors)
  - [13.5. OpenAPI Specification](#135-openapi-specification)
  - [13.6. Error Responses](#136-error-responses)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)

---


<!-- toc-auto -->
## Contents

- [13. REST API Contract (Normative for Portals)](#13-rest-api-contract-normative-for-portals)
  - [13.1. Required Endpoints](#131-required-endpoints)
  - [13.2. Recommended Endpoints](#132-recommended-endpoints)
  - [13.3. Response Schemas](#133-response-schemas)
  - [13.4. CORS](#134-cors)
  - [13.5. OpenAPI Specification](#135-openapi-specification)
  - [13.6. Error Responses](#136-error-responses)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> v1.1 делает REST API mandatory частью протокола. Это обеспечивает

---
<!-- tags: rag, architecture, collaboration -->




## 13. REST API Contract (Normative for Portals)

v1.1 делает REST API mandatory частью протокола. Это обеспечивает 
interoperability между порталами и внешними клиентами (SDK, web UI, 
MCP wrappers).

### 13.1. Required Endpoints

Compatible portal MUST предоставлять:

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/query?q=<text>&ranked=<0\|1>` | Поиск концептов |
| GET | `/api/describe` | Описание всех адаптеров |
| GET | `/api/health` | Состояние экосистемы (score 0–100) |

### 13.2. Recommended Endpoints

Portal SHOULD предоставлять:

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/links` | Валидация кросс-ссылок |
| GET | `/api/neighbors?q6=<bits>&dist=<N>` | Q6-соседи |
| GET | `/metrics` | Prometheus-метрики (text/plain) |
| GET | `/` | Root endpoint со списком endpoints |

### 13.3. Response Schemas

Все ответы MUST быть JSON (кроме `/metrics` — text/plain).

**`/api/query` response**:

```json
{
  "query": "string",
  "entries": [
    {
      "id": "string",
      "title": "string",
      "source": "owner/repo",
      "format_type": "string",
      "content": "string",
      "metadata": { "q6": "010100", ... },
      "links": ["pro2:q6:010100", ...],
      "is_fallback": false,
      "relevance_score": 0.85
    }
  ],
  "consensus": {
    "present_in": ["info1", "pro2"],
    "present_in_fallback": ["meta"],
    "missing_in": ["data2"],
    "coverage": 0.5,
    "coverage_with_fallback": 0.75,
    "agreed": false
  },
  "cross_links": [...],
  "errors": {}
}
```

**`/api/describe` response**:

```json
{
  "adapters": {
    "info1": { "repo": "svend4/info1", "format": "info1", ... },
    "pro2": { "repo": "svend4/pro2", "format": "pro2", ... }
  }
}
```

**`/api/health` response**:

```json
{
  "score": 82,
  "adapters_count": 7,
  "real_entries": 8,
  "fallback_entries": 68,
  "issues": ["info1: 0 real entries", "pro2: 0 real entries"]
}
```

### 13.4. CORS

Portal MUST включать CORS headers для `/api/*` endpoints:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, OPTIONS
```

(Для production с auth — SHOULD whitelist specific origins.)

### 13.5. OpenAPI Specification

Portal MUST предоставлять `openapi.yaml` в корне репо, совместимый 
с OpenAPI 3.1.0.

### 13.6. Error Responses

Все errors MUST возвращаться как JSON с HTTP status code:

```json
{
  "error": "string (machine-readable code)",
  "message": "string (human-readable)",
  "details": { ... }
}
```

Стандартные коды:
- `400 invalid_query` — malformed request
- `404 repo_not_found` — repo не в registry
- `500 internal_error` — unexpected error
- `503 adapter_timeout` — все adapters timed out

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[128-доступные-инструменты]] (сходство 0.12)
- [[90-15-security-considerations]] (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [[90-15-security-considerations]]
- [[23-11-security-considerations]]
- [[128-доступные-инструменты]]
- [[82-7-portalentry-structure]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[128-доступные-инструменты|Доступные инструменты]] _29%_
- [[90-15-security-considerations|15. Security Considerations]] _29%_
- [[23-11-security-considerations|11. Security Considerations]] _21%_
- [[18-6-adapter-interface|6. Adapter Interface]] _17%_
- [[78-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] _17%_
- [[81-6-adapter-interface|6. Adapter Interface]] _17%_
