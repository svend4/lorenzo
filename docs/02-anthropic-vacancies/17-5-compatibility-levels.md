# 5. Compatibility Levels

<!-- summary -->
> NPP определяет 4 уровня совместимости Repo с экосистемой. Это

---



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
