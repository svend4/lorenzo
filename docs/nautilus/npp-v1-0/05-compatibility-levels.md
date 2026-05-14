---
state: approved
---

# 5. Compatibility Levels

<!-- toc-auto -->
## Contents

- [5. Compatibility Levels](#5-compatibility-levels)
  - [Level 0 — Discoverable](#level-0-discoverable)
  - [Level 1 — Readable](#level-1-readable)
  - [Level 2 — Queryable](#level-2-queryable)
  - [Level 3 — Interactive / Bridged](#level-3-interactive-bridged)
- [Использование](#использование)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы. Источник: MHTML‑снимок Вакансии в Anthropic по кластерам - Claude (корень репозитория).
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: anthropic, rag -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 5. Compatibility Levels

NPP определяет 4 уровня совместимости Repo с экосистемой. Это 
позволяет постепенное подключение: существующий Repo может начать 
на уровне 0 и расти к уровню 3 без переделки.

### Level 0 — Discoverable

Repo объявлен в `nautilus.json` с полями `name`, `url`, `format`. 
Адаптера ещё нет. Portal знает о существовании Repo, но не может 
его запрашивать.

**Use case**: анонс намерения подключить Repo до написания кода.

### Level 1 — Readable

Repo имеет `passport.md` в корне. Адаптер реализует только 
`describe()` метод. Portal может показать метаданные, но не может 
выполнять query.

**Use case**: статические Repos (архивы, reference docs), которые 
не нужно искать.

### Level 2 — Queryable

Адаптер реализует `describe()` + `fetch(query)`. Portal может 
выполнять полноценный поиск в Repo.

**Use case**: большинство активных Repos.

### Level 3 — Interactive / Bridged

Адаптер реализует `describe()` + `fetch(query)` + `translate_to(entry, target_repo)`. 
Portal может переводить концепты между Repos через bridges.

**Use case**: Repos, глубоко связанные с другими в экосистеме, где 
важны cross-repo queries.

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "5 Compatibility Levels"
```

_Документ доступен для семантического поиска._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [02-terminology](02-terminology.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [05-compatibility-levels](../../obsidian/nautilus/npp-v1-0/05-compatibility-levels.md) (сходство 0.98)
- [17-5-compatibility-levels](../../obsidian/02-anthropic-vacancies/17-5-compatibility-levels.md) (сходство 0.67)
- [17-5-compatibility-levels](../../02-anthropic-vacancies/17-5-compatibility-levels.md) (сходство 0.67)

