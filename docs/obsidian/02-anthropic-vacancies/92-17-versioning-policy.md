---
title: "17. Versioning Policy"
tags:
  - architecture
  - rag
  - anthropic-vacancies
date: 2026-05-14
---

# 17. Versioning Policy

<!-- toc-auto -->
## Contents

- [17. Versioning Policy](#17-versioning-policy)
  - [17.1. Semver](#171-semver)
  - [17.2. Version in Registry](#172-version-in-registry)
  - [17.3. Breaking Changes Process](#173-breaking-changes-process)
  - [17.4. Deprecation Policy](#174-deprecation-policy)
- [Похожие документы](#похожие-документы)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (9)](#кто-ссылается-на-этот-документ-9)


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Breaking Changes Process Для major version bump требуется: 1.
> 🔧 **Подход:** Deprecation Policy(174-deprecation-policy) !IMPORTANT Ключевой документ для понимания архитектуры.
> 🏷️ **Ключевые слова:** `policy`, `versioning`, `status`, `document`, `version`, `anthropic`, `vacancies`, `major`
>


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> * Breaking Changes Process Для major version bump требуется: 1. * Deprecation Policy !IMPORTANT Ключевой документ для понимания архитектуры 🎯 Проблема: Breaking Changes Process Для major version bump требуется: 1.
NPP следует semver:
 Major (v1 → v2): breaking changes в interfaces или schemas
 Minor (v1.0 → v1.1): новая функциональность, backward-compatible
 Patch (v1.0.0 → v1.0.1): clarifications, typo fixes
17.2.

---
<!-- tags: architecture, rag -->




## 17. Versioning Policy

### 17.1. Semver

NPP следует semver:

- **Major** (v1 → v2): breaking changes в interfaces или schemas
- **Minor** (v1.0 → v1.1): новая функциональность, backward-compatible
- **Patch** (v1.0.0 → v1.0.1): clarifications, typo fixes

### 17.2. Version in Registry

Каждый registry MUST объявлять `protocol_version`. Portal MUST 
поддерживать минимум текущую major version.

v1.1 porталы MUST поддерживать v1.0 адаптеры через shim-логику 
(default values для новых полей типа `is_fallback`).

### 17.3. Breaking Changes Process

Для major version bump требуется:

1. RFC в Issues репо Portal с обоснованием
2. Минимум 30 дней обсуждения
3. Migration guide для существующих адаптеров
4. Compatibility shim в Portal минимум на 6 месяцев

### 17.4. Deprecation Policy

Когда поле/метод помечается deprecated:

- Remains functional в текущей major version
- Warning log при использовании
- Удаляется только в следующем major bump

---

<!-- similar-docs -->

---

## Похожие документы
- [[24-12-versioning-policy]] (сходство 0.63)
- [[75-0-status-of-this-document]] (сходство 0.15)
- [[05-0-status-of-this-document]] (сходство 0.12)


<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "17 Versioning Policy"
```

## Смотрите также
- [[24-12-versioning-policy]]
- 123-portal-[[123-portal-mcp-py|mcp-py]]
- [[75-0-status-of-this-document]]
- [[05-0-status-of-this-document]]


<!-- backlinks -->

---

## Кто ссылается на этот документ (9)
- [[03-portal-protocol-md]]
- [[05-0-status-of-this-document]]
- 123-portal-[[123-portal-mcp-py|mcp-py]]
- [[129-примеры-запросов-в-claude]]
- [[24-12-versioning-policy]]
- [[42-author-contact]]
- [[62-author-contact]]
- [[75-0-status-of-this-document]]
- _...ещё 1_

