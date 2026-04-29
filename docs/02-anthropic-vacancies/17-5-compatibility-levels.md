# 5. Compatibility Levels

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Use case: статические Repos (архивы, reference docs), которые не нужно искать.
> 🔧 **Подход:** Адаптер реализует только describe() метод.
> ✅ **Результат:** Это позволяет постепенное подключение: существующий Repo может начать на уровне 0 и расти к уровню 3 без переделки.
> 🏷️ **Ключевые слова:** `level`, `compatibility`, `levels`, `anthropic`, `vacancies`, `может`, `portal`, `repos`
>


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
- [80-5-compatibility-levels](docs/02-anthropic-vacancies/80-5-compatibility-levels.md) (сходство 0.32)
- [41-compatibility-level](docs/02-anthropic-vacancies/41-compatibility-level.md) (сходство 0.17)
- [51-compatibility-level](docs/02-anthropic-vacancies/51-compatibility-level.md) (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [80-5-compatibility-levels](docs/02-anthropic-vacancies/80-5-compatibility-levels.md)
- [41-compatibility-level](docs/02-anthropic-vacancies/41-compatibility-level.md)
- [51-compatibility-level](docs/02-anthropic-vacancies/51-compatibility-level.md)
- [61-compatibility-level](docs/02-anthropic-vacancies/61-compatibility-level.md)

