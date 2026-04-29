# 17. Versioning Policy

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
