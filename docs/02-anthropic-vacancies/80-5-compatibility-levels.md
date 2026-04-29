# 5. Compatibility Levels
<!-- tags: anthropic -->


<!-- toc-auto -->
## Contents

- [5. Compatibility Levels](#5-compatibility-levels)
  - [Level 0 — Discoverable](#level-0-discoverable)
  - [Level 1 — Readable](#level-1-readable)
  - [Level 2 — Linked](#level-2-linked)
  - [Level 3 — Interactive](#level-3-interactive)


<!-- summary -->
> NPP определяет 4 уровня совместимости Repo с экосистемой. Это

---
<!-- tags: anthropic -->




## 5. Compatibility Levels

NPP определяет 4 уровня совместимости Repo с экосистемой. Это 
позволяет постепенное подключение.

### Level 0 — Discoverable

Repo объявлен в `nautilus.json`. Адаптера нет. Portal знает о 
существовании Repo, но не может запрашивать.

**Use case**: анонс намерения подключить Repo до написания кода.

**Требования**:
- Только запись в `nautilus.json` (минимально `name` + `format` + `repo`)

### Level 1 — Readable

Repo имеет passport + адаптер со статическими записями. 
Portal возвращает static entries.

**Use case**: архивы, reference docs, стабильные репо.

**Требования**:
- Всё из Level 0
- `passport.md` в `passports/`
- Адаптер реализует `fetch()` + `describe()` (см. раздел 6)
- Fallback-entries в адаптере (≥3 записи)

### Level 2 — Linked

Адаптер производит записи с заполненными Q6-координатами в 
`metadata.q6` и `links` на другие Repos. Portal может вычислять 
кросс-ссылки и визуализировать граф.

**Use case**: активные Repos с семантическими связями.

**Требования**:
- Всё из Level 1
- Каждый PortalEntry MUST иметь `metadata.q6` (если Q6-маппинг 
  определён для этого Repo)
- Каждый PortalEntry SHOULD иметь ≥1 link на другой Repo

### Level 3 — Interactive

Адаптер выполняет live-fetch через GitHub API или эквивалент, 
возвращая реальные данные из Repo (не только fallback).

**Use case**: Repos, глубоко интегрированные с экосистемой.

**Требования**:
- Всё из Level 2
- `fetch()` делает real network call (с timeout ≤ 5 сек)
- Graceful fallback: при ошибке сети/API возвращает static entries 
  с `is_fallback=True`
- `PortalEntry.is_fallback` явно помечается

---

<!-- similar-docs -->

---

**Похожие документы:**
- [17-5-compatibility-levels](17-5-compatibility-levels.md) (сходство 0.32)
- [77-2-terminology](77-2-terminology.md) (сходство 0.12)
- [82-7-portalentry-structure](82-7-portalentry-structure.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [17-5-compatibility-levels](17-5-compatibility-levels.md)
- [82-7-portalentry-structure](82-7-portalentry-structure.md)
- [41-compatibility-level](41-compatibility-level.md)
- [77-2-terminology](77-2-terminology.md)

<!-- backlinks-auto -->
## Упоминается в

- [5. Compatibility Levels](17-5-compatibility-levels.md)
- [9. Consensus Algorithm](84-9-consensus-algorithm.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [5. Compatibility Levels](17-5-compatibility-levels.md) _42%_
- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md) _29%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _25%_
- [4. Passport (`passport.md`)](79-4-passport-passport-md.md) _25%_
- [2. Terminology](07-2-terminology.md) _21%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _21%_
- [7. PortalEntry Structure](19-7-portalentry-structure.md) _21%_
- [Compatibility Level](41-compatibility-level.md) _21%_
## Связанные документы

- [5. Compatibility Levels](17-5-compatibility-levels.md) _48%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _21%_
- [6. Adapter Interface](18-6-adapter-interface.md) _21%_
- [7. PortalEntry Structure](19-7-portalentry-structure.md) _21%_
- [Compatibility Level](41-compatibility-level.md) _21%_
- [2. Terminology](77-2-terminology.md) _21%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _17%_
- [Compatibility Level](51-compatibility-level.md) _17%_
