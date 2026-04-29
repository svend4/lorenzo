# 12. Versioning Policy

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

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

<!-- see-also -->

---

**Смотрите также:**
- [24-12-versioning-policy](docs/02-anthropic-vacancies/24-12-versioning-policy.md)
- [17-versioning-policy](docs/nautilus/npp-v1-1/17-versioning-policy.md)
- [92-17-versioning-policy](docs/02-anthropic-vacancies/92-17-versioning-policy.md)
- [17-appendix-b-change-log](docs/nautilus/npp-v1-0/17-appendix-b-change-log.md)

