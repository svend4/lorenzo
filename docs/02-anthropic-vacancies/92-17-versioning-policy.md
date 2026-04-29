# 17. Versioning Policy

<!-- toc-auto -->
## Contents

- [17. Versioning Policy](#17-versioning-policy)
  - [17.1. Semver](#171-semver)
  - [17.2. Version in Registry](#172-version-in-registry)
  - [17.3. Breaking Changes Process](#173-breaking-changes-process)
  - [17.4. Deprecation Policy](#174-deprecation-policy)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> - **Major** (v1 → v2): breaking changes в interfaces или schemas

---
<!-- tags: architecture -->




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

**Похожие документы:**
- [24-12-versioning-policy](24-12-versioning-policy.md) (сходство 0.63)
- [75-0-status-of-this-document](75-0-status-of-this-document.md) (сходство 0.15)
- [05-0-status-of-this-document](05-0-status-of-this-document.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [24-12-versioning-policy](24-12-versioning-policy.md)
- [123-portal-mcp-py](123-portal-mcp-py.md)
- [75-0-status-of-this-document](75-0-status-of-this-document.md)
- [05-0-status-of-this-document](05-0-status-of-this-document.md)

<!-- backlinks-auto -->
## Упоминается в

- [12. Versioning Policy](24-12-versioning-policy.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [12. Versioning Policy](24-12-versioning-policy.md) _81%_
- [Author & Contact](62-author-contact.md) _33%_
- [Author & Contact](42-author-contact.md) _29%_
- [0. Status of This Document](75-0-status-of-this-document.md) _29%_
- [0. Status of This Document](05-0-status-of-this-document.md) _25%_
- [13. Reference Implementation](25-13-reference-implementation.md) _25%_
- [18. Reference Implementation](93-18-reference-implementation.md) _25%_
- [PORTAL-PROTOCOL.md](03-portal-protocol-md.md) _17%_
## Связанные документы

- [12. Versioning Policy](24-12-versioning-policy.md) _81%_
- [0. Status of This Document](05-0-status-of-this-document.md) _25%_
- [Author & Contact](42-author-contact.md) _25%_
- [Author & Contact](62-author-contact.md) _25%_
- [0. Status of This Document](75-0-status-of-this-document.md) _25%_
- [PORTAL-PROTOCOL.md](03-portal-protocol-md.md) _21%_
- [Примеры запросов (в Claude)](129-примеры-запросов-в-claude.md) _21%_
- [2. Terminology](77-2-terminology.md) _21%_
