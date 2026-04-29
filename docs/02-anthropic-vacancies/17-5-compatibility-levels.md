# 5. Compatibility Levels
<!-- tags: anthropic -->


<!-- toc-auto -->
## Contents

- [5. Compatibility Levels](#5-compatibility-levels)
  - [Level 0 — Discoverable](#level-0-discoverable)
  - [Level 1 — Readable](#level-1-readable)
  - [Level 2 — Queryable](#level-2-queryable)
  - [Level 3 — Interactive / Bridged](#level-3-interactive-bridged)


<!-- summary -->
> NPP определяет 4 уровня совместимости Repo с экосистемой. Это

---
<!-- tags: anthropic -->




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

<!-- similar-docs -->

---

**Похожие документы:**
- [80-5-compatibility-levels](80-5-compatibility-levels.md) (сходство 0.32)
- [41-compatibility-level](41-compatibility-level.md) (сходство 0.17)
- [51-compatibility-level](51-compatibility-level.md) (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [80-5-compatibility-levels](80-5-compatibility-levels.md)
- [41-compatibility-level](41-compatibility-level.md)
- [51-compatibility-level](51-compatibility-level.md)
- [61-compatibility-level](61-compatibility-level.md)

<!-- backlinks-auto -->
## Упоминается в

- [10. Query Flow](85-10-query-flow.md)
- [5. Compatibility Levels](80-5-compatibility-levels.md)
- [6. Adapter Interface](18-6-adapter-interface.md)
- [9. Consensus Algorithm](84-9-consensus-algorithm.md)
- [9. Query Flow](21-9-query-flow.md)
- [Compatibility Level](41-compatibility-level.md)
- [Compatibility Level](61-compatibility-level.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [5. Compatibility Levels](80-5-compatibility-levels.md) _42%_
- [Compatibility Level](41-compatibility-level.md) _25%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _21%_
- [Compatibility Level](61-compatibility-level.md) _21%_
- [6. Adapter Interface](18-6-adapter-interface.md) _17%_
- [Compatibility Level](51-compatibility-level.md) _17%_
- [9. Consensus Algorithm](84-9-consensus-algorithm.md) _17%_
## Связанные документы

- [5. Compatibility Levels](80-5-compatibility-levels.md) _48%_
- [Compatibility Level](41-compatibility-level.md) _25%_
- [6. Adapter Interface](18-6-adapter-interface.md) _21%_
- [Compatibility Level](51-compatibility-level.md) _21%_
- [Compatibility Level](61-compatibility-level.md) _21%_
- [🇬🇧 About](68-about.md) _21%_
- [10. Query Flow](85-10-query-flow.md) _21%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _17%_
