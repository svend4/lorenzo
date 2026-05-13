# 17. Versioning Policy

<!-- toc-auto -->
## Contents

- [17. Versioning Policy](#17-versioning-policy)
  - [17.1. Semver](#171-semver)
  - [17.2. Version in Registry](#172-version-in-registry)
  - [17.3. Breaking Changes Process](#173-breaking-changes-process)
  - [17.4. Deprecation Policy](#174-deprecation-policy)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

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

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "17 Versioning Policy"
```

## Смотрите также
- [92-17-versioning-policy](../../02-anthropic-vacancies/92-17-versioning-policy.md)
- [12-versioning-policy](../npp-v1-0/12-versioning-policy.md)
- [24-12-versioning-policy](../../02-anthropic-vacancies/24-12-versioning-policy.md)
- [07-portal-entry](07-portal-entry.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал индексирован и доступен для поиска, BM25 и навигации через граф концептов._ _Документ доступен для семантического поиска._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [12-versioning-policy](../npp-v1-0/12-versioning-policy.md)
- [07-portal-entry](07-portal-entry.md)
- [13-rest-api](13-rest-api.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [17-versioning-policy](../../obsidian/nautilus/npp-v1-1/17-versioning-policy.md) (сходство 0.98)
- [92-17-versioning-policy](../../02-anthropic-vacancies/92-17-versioning-policy.md) (сходство 0.64)
- [92-17-versioning-policy](../../obsidian/02-anthropic-vacancies/92-17-versioning-policy.md) (сходство 0.63)

