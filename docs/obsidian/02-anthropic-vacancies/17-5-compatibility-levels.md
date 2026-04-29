---
title: "5. Compatibility Levels"
tags:
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

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
- [[80-5-compatibility-levels]] (сходство 0.32)
- [[41-compatibility-level]] (сходство 0.17)
- [[51-compatibility-level]] (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [[80-5-compatibility-levels]]
- [[41-compatibility-level]]
- [[51-compatibility-level]]
- [[61-compatibility-level]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[80-5-compatibility-levels|5. Compatibility Levels]] _48%_
- [[41-compatibility-level|Compatibility Level]] _25%_
- [[18-6-adapter-interface|6. Adapter Interface]] _21%_
- [[51-compatibility-level|Compatibility Level]] _21%_
- [[61-compatibility-level|Compatibility Level]] _21%_
- [[68-about|🇬🇧 About]] _21%_
- [[85-10-query-flow|10. Query Flow]] _21%_
- [[09-4-passport-passport-md|4. Passport (`passport.md`)]] _17%_
