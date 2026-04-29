# 15. Security Considerations

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
