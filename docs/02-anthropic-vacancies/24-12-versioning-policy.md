# 12. Versioning Policy

<!-- summary -->
> - **Major** (v1 → v2): breaking changes в interfaces или schemas

---
<!-- tags: architecture -->




## 12. Versioning Policy

### 12.1. Semver

NPP следует semver:

- **Major** (v1 → v2): breaking changes в interfaces или schemas
- **Minor** (v1.0 → v1.1): новая функциональность, backward-compatible
- **Patch** (v1.0.0 → v1.0.1): clarifications, typo fixes

### 12.2. Version in Registry

Каждый registry MUST объявлять `protocol_version`. Portal 
implementation MUST поддерживать **минимум текущую major version**.

### 12.3. Breaking Changes Process

Для major version bump требуется:

1. RFC в Issues репо Portal с обоснованием
2. Минимум 30 дней обсуждения
3. Migration guide для существующих адаптеров
4. Опубликованная compatibility shim в Portal для переходного 
   периода (минимум 6 месяцев)

---

<!-- similar-docs -->

---

**Похожие документы:**
- [92-17-versioning-policy](docs/02-anthropic-vacancies/92-17-versioning-policy.md) (сходство 0.63)
- [05-0-status-of-this-document](docs/02-anthropic-vacancies/05-0-status-of-this-document.md) (сходство 0.14)
- [75-0-status-of-this-document](docs/02-anthropic-vacancies/75-0-status-of-this-document.md) (сходство 0.13)

