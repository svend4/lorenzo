---
title: "15. Security Considerations"
tags:
  - memory
  - ingestion
  - architecture
  - anthropic
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

# 15. Security Considerations
<!-- tags: memory, ingestion, architecture, anthropic, collaboration -->


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Security Considerations(15-security-considerations) - 15.1.
> 🔧 **Подход:** Supply Chain(155-supply-chain) !IMPORTANT Ключевой документ для понимания архитектуры.
> ✅ **Результат:** Для приватных Repos RECOMMENDED: - Отдельный private-nautilus.json с explicit opt-in - Отдельный portal instance, не доступный публично - Authentication на REST API (JWT / API keys
> 🏷️ **Ключевые слова:** `security`, `considerations`, `adapters`, `portal`, `anthropic`, `vacancies`, `private`, `untrusted`
>


<!-- toc-auto -->
## Contents

- [15. Security Considerations](#15-security-considerations)
  - [15.1. Untrusted Adapters](#151-untrusted-adapters)
  - [15.2. Private Repositories](#152-private-repositories)
  - [15.3. MCP Exposure](#153-mcp-exposure)
  - [15.4. Rate Limiting](#154-rate-limiting)
  - [15.5. Supply Chain](#155-supply-chain)


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

- Отдельный `private-[[memnet|nautilus]].json` с explicit opt-in
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
- [[23-11-security-considerations]] (сходство 0.55)
- [[88-13-rest-api-contract-normative-for-portals]] (сходство 0.11)
- [[85-10-query-flow]] (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [[23-11-security-considerations]]
- [[88-13-rest-api-contract-normative-for-portals]]
- [[81-6-adapter-interface]]
- [[18-6-adapter-interface]]

<!-- backlinks-auto -->
## Упоминается в

- [[23-11-security-considerations|11. Security Considerations]]
- [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[23-11-security-considerations|11. Security Considerations]] _48%_
- [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]] _25%_
## Связанные документы

- [[23-11-security-considerations|11. Security Considerations]] _42%_
- [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]] _29%_
- [[21-9-query-flow|9. Query Flow]] _17%_
- [[85-10-query-flow|10. Query Flow]] _17%_
