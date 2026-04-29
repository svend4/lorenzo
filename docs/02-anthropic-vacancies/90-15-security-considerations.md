# 15. Security Considerations
<!-- tags: ingestion, architecture, anthropic -->


<!-- toc-auto -->
## Contents

- [15. Security Considerations](#15-security-considerations)
  - [15.1. Untrusted Adapters](#151-untrusted-adapters)
  - [15.2. Private Repositories](#152-private-repositories)
  - [15.3. MCP Exposure](#153-mcp-exposure)
  - [15.4. Rate Limiting](#154-rate-limiting)
  - [15.5. Supply Chain](#155-supply-chain)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Adapters выполняются внутри Portal-процесса. Portal MUST

---



## 15. Security Considerations

### 15.1. Untrusted Adapters

Adapters выполняются внутри Portal-процесса. Portal MUST 
обрабатывать adapters как untrusted code:

- Timeout на каждый adapter call (RECOMMENDED 5 секунд)
- Exception handling вокруг каждого call
- XSS protection (`_html.escape`) во всех user-facing rendered полях

Portal SHOULD НЕ выполнять adapters из untrusted sources без review.

### 15.2. Private Repositories

Repos, содержащие чувствительные данные (legal, medical, personal), 
SHOULD НЕ включаться в публичную registry.

Для приватных Repos RECOMMENDED:

- Отдельный `private-nautilus.json` с explicit opt-in
- Отдельный portal instance, не доступный публично
- Authentication на REST API (JWT / API keys)
- Нет MCP exposure без whitelist

Implementation MUST различать public и private registries и не 
смешивать результаты без явного запроса.

### 15.3. MCP Exposure

При экспонировании Portal через MCP (см. раздел 16), implementation 
SHOULD:

- Требовать явный whitelist Repos, доступных через MCP
- Логировать queries отдельно, с возможностью очистки
- Не включать private Repos в MCP responses по умолчанию

### 15.4. Rate Limiting

Public-facing portals SHOULD реализовать rate limiting:

- RECOMMENDED: 60 requests per minute per IP для `/api/query`
- RECOMMENDED: 120 requests per minute per IP для `/api/describe` и 
  `/api/health`

### 15.5. Supply Chain

Reference implementation использует только Python stdlib (zero 
external dependencies). Это RECOMMENDED для альтернативных 
implementations. Каждая external dependency — потенциальный 
supply-chain риск.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [23-11-security-considerations](23-11-security-considerations.md) (сходство 0.55)
- [88-13-rest-api-contract-normative-for-portals](88-13-rest-api-contract-normative-for-portals.md) (сходство 0.11)
- [85-10-query-flow](85-10-query-flow.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [23-11-security-considerations](23-11-security-considerations.md)
- [88-13-rest-api-contract-normative-for-portals](88-13-rest-api-contract-normative-for-portals.md)
- [81-6-adapter-interface](81-6-adapter-interface.md)
- [18-6-adapter-interface](18-6-adapter-interface.md)

<!-- backlinks-auto -->
## Упоминается в

- [11. Security Considerations](23-11-security-considerations.md)
- [13. REST API Contract (Normative for Portals)](88-13-rest-api-contract-normative-for-portals.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [11. Security Considerations](23-11-security-considerations.md) _48%_
- [13. REST API Contract (Normative for Portals)](88-13-rest-api-contract-normative-for-portals.md) _25%_
## Связанные документы

- [11. Security Considerations](23-11-security-considerations.md) _42%_
- [13. REST API Contract (Normative for Portals)](88-13-rest-api-contract-normative-for-portals.md) _29%_
- [9. Query Flow](21-9-query-flow.md) _17%_
- [10. Query Flow](85-10-query-flow.md) _17%_
