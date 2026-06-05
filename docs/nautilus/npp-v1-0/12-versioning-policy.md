---
state: approved
---

# 12. Versioning Policy

<!-- toc-auto -->
## Contents

- [12. Versioning Policy](#12-versioning-policy)
  - [12.1. Semver](#121-semver)
  - [12.2. Version in Registry](#122-version-in-registry)
  - [12.3. Breaking Changes Process](#123-breaking-changes-process)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы. Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория).
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "12 Versioning Policy"
```

## Смотрите также
- [24-12-versioning-policy](../../02-anthropic-vacancies/24-12-versioning-policy.md)
- [17-versioning-policy](../npp-v1-1/17-versioning-policy.md)
- [92-17-versioning-policy](../../02-anthropic-vacancies/92-17-versioning-policy.md)
- [17-appendix-b-change-log](17-appendix-b-change-log.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал доступен для поиска в базе знаний репозитория._ _Для поиска доступен._

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)
- [17-versioning-policy](../npp-v1-1/17-versioning-policy.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [12-versioning-policy](../../obsidian/nautilus/npp-v1-0/12-versioning-policy.md) (сходство 0.97)
- [24-12-versioning-policy](../../02-anthropic-vacancies/24-12-versioning-policy.md) (сходство 0.60)
- [24-12-versioning-policy](../../obsidian/02-anthropic-vacancies/24-12-versioning-policy.md) (сходство 0.60)

