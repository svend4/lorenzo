# 11. Security Considerations

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Security Considerations(11-security-considerations) - 11.1.
> 🔧 **Подход:** MCP Exposure(113-mcp-exposure) !IMPORTANT Ключевой документ для понимания архитектуры.
> ✅ **Результат:** Implementation MUST различать public и private registries и не смешивать результаты без явного запроса.
> 🏷️ **Ключевые слова:** `security`, `considerations`, `portal`, `adapters`, `private`, `untrusted`, `anthropic`, `vacancies`
>


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
`private-[nautilus](../docs/05-habr-projects/memory/memnet.md).json` с явным opt-in.

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
- [90-15-security-considerations](docs/02-anthropic-vacancies/90-15-security-considerations.md) (сходство 0.55)


<!-- see-also -->

---

**Смотрите также:**
- [90-15-security-considerations](docs/02-anthropic-vacancies/90-15-security-considerations.md)
- [123-portal-mcp-py](docs/02-anthropic-vacancies/123-portal-mcp-py.md)
- [88-13-rest-api-contract-normative-for-portals](docs/02-anthropic-vacancies/88-13-rest-api-contract-normative-for-portals.md)
- [19-7-portalentry-structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md)

