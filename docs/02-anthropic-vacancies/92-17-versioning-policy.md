# 17. Versioning Policy

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Breaking Changes Process Для major version bump требуется: 1.
> 🔧 **Подход:** Deprecation Policy(174-deprecation-policy) !IMPORTANT Ключевой документ для понимания архитектуры.
> 🏷️ **Ключевые слова:** `policy`, `versioning`, `status`, `document`, `version`, `anthropic`, `vacancies`, `major`
>


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
- [24-12-versioning-policy](docs/02-anthropic-vacancies/24-12-versioning-policy.md) (сходство 0.63)
- [75-0-status-of-this-document](docs/02-anthropic-vacancies/75-0-status-of-this-document.md) (сходство 0.15)
- [05-0-status-of-this-document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [24-12-versioning-policy](docs/02-anthropic-vacancies/24-12-versioning-policy.md)
- [123-portal-mcp-py](docs/02-anthropic-vacancies/123-portal-mcp-py.md)
- [75-0-status-of-this-document](docs/02-anthropic-vacancies/75-0-status-of-this-document.md)
- [05-0-status-of-this-document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md)

