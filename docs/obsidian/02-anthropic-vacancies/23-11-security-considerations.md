---
title: "11. Security Considerations"
tags:
  - ingestion
  - architecture
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# 11. Security Considerations
<!-- tags: ingestion, architecture, anthropic -->


<!-- toc-auto -->
## Contents

- [11. Security Considerations](#11-security-considerations)
  - [11.1. Untrusted Adapters](#111-untrusted-adapters)
  - [11.2. Private Repositories](#112-private-repositories)
  - [11.3. MCP Exposure](#113-mcp-exposure)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Adapters выполняются внутри Portal-процесса. Portal MUST обрабатывать

---



## 11. Security Considerations

### 11.1. Untrusted Adapters

Adapters выполняются внутри Portal-процесса. Portal MUST обрабатывать 
adapters как untrusted code:

- Timeout на каждый adapter call
- Exception handling вокруг каждого call
- Resource limits (memory, CPU), если implementation позволяет

Portal SHOULD НЕ выполнять adapters из untrusted sources без review.

### 11.2. Private Repositories

Repos, содержащие чувствительные данные, SHOULD НЕ включаться в 
публичную registry. Для приватных Repos RECOMMENDED отдельный 
`private-nautilus.json` с явным opt-in.

Implementation MUST различать public и private registries и не 
смешивать результаты без явного запроса.

### 11.3. MCP Exposure

При экспонировании Portal через MCP, implementation SHOULD:

- Требовать явный whitelist Repos, доступных через MCP
- Логировать queries отдельно, с возможностью очистки
- Не включать private Repos в MCP responses по умолчанию

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[90-15-security-considerations]] (сходство 0.55)


<!-- see-also -->

---

**Смотрите также:**
- [[90-15-security-considerations]]
- [[123-portal-mcp-py]]
- [[88-13-rest-api-contract-normative-for-portals]]
- [[19-7-portalentry-structure]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[90-15-security-considerations|15. Security Considerations]] _42%_
- [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]] _21%_
- [[68-about|🇬🇧 About]] _17%_
- [[81-6-adapter-interface|6. Adapter Interface]] _17%_
