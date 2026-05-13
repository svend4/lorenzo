---
state: approved
---

# 11. Security Considerations

<!-- toc-auto -->
## Contents

- [11. Security Considerations](#11-security-considerations)
  - [11.1. Untrusted Adapters](#111-untrusted-adapters)
  - [11.2. Private Repositories](#112-private-repositories)
  - [11.3. MCP Exposure](#113-mcp-exposure)
- [Похожие документы](#похожие-документы)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в-1)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы-1)
- [Кто ссылается на этот документ (4)](#кто-ссылается-на-этот-документ-4)


<!-- tags: memory, ingestion, architecture, anthropic, collaboration -->


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Security Considerations(11-security-considerations) - 11.1.
> 🔧 **Подход:** MCP Exposure(113-mcp-exposure) !IMPORTANT Ключевой документ для понимания архитектуры.
> ✅ **Результат:** Implementation MUST различать public и private registries и не смешивать результаты без явного запроса.
> 🏷️ **Ключевые слова:** `security`, `considerations`, `portal`, `adapters`, `private`, `untrusted`, `anthropic`, `vacancies`
>


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> * Security Considerations - 11.1. * MCP Exposure !IMPORTANT Ключевой документ для понимания архитектуры 🎯 Проблема: Security Considerations - 11.1. 🔧 Подход: MCP Exposure !IMPORTANT Ключевой документ для понимания архитектуры.
 Похожие документы
 Использование
 Смотрите также
 Упоминается в
 Упоминается в
 Связанные документы
 Связанные документы
 Кто ссылается на этот документ (4)
 
 
> Абстракт (авто)
>
> 🎯 Проблема: Security Considerations(11-security-consi

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
`private-[nautilus](../05-habr-projects/memory/memnet.md).json` с явным opt-in.

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

## Похожие документы
- [90-15-security-considerations](90-15-security-considerations.md) (сходство 0.55)


<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "11 Security Considerations"
```

## Смотрите также
- [90-15-security-considerations](90-15-security-considerations.md)
- 123-portal-[mcp-py](123-portal-mcp-py.md)
- 88-13-[rest-api-contract-normative-for-portals](88-13-rest-api-contract-normative-for-portals.md)
- [19-7-portalentry-structure](19-7-portalentry-structure.md)

<!-- backlinks-auto -->
## Упоминается в

- [13. REST API Contract (Normative for Portals)](88-13-rest-api-contract-normative-for-portals.md)
- [15. Security Considerations](90-15-security-considerations.md)
- [6. Adapter Interface](18-6-adapter-interface.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [15. Security Considerations](90-15-security-considerations.md) _48%_
- [13. REST API Contract (Normative for Portals)](88-13-rest-api-contract-normative-for-portals.md) _33%_
- [6. Adapter Interface](81-6-adapter-interface.md) _17%_
## Связанные документы

- [15. Security Considerations](90-15-security-considerations.md) _42%_
- [13. REST API Contract (Normative for Portals)](88-13-rest-api-contract-normative-for-portals.md) _21%_
- [🇬🇧 About](68-about.md) _17%_
- [6. Adapter Interface](81-6-adapter-interface.md) _17%_

<!-- backlinks -->

---

## Кто ссылается на этот документ (4)
- 123-portal-[mcp-py](123-portal-mcp-py.md)
- [18-6-adapter-interface](18-6-adapter-interface.md)
- [90-15-security-considerations](90-15-security-considerations.md)
- [README](README.md)

