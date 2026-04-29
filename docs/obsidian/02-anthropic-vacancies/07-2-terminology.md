---
title: "2. Terminology"
tags:
  - architecture
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

# 2. Terminology

<!-- summary -->
> **Ecosystem** — набор репозиториев, участвующих в одной федерации.

---
<!-- tags: architecture, collaboration -->




## 2. Terminology

**Ecosystem** — набор репозиториев, участвующих в одной федерации. 
Имеет уникальное имя (например, `svend4`).

**Repository-participant** (далее — **Repo**) — Git-репозиторий, 
содержащий минимум `nautilus.json` и `passport.md` в корне.

**Native format** — исходный формат данных в Repo, определяемый автором. 
Может быть любым: Markdown, JSON, YAML, plain text, бинарный формат, 
и так далее. NPP не ограничивает native format.

**Portal** — implementation NPP, которая загружает registry, инстанцирует 
адаптеры и выполняет query-операции. Reference implementation: 
`github.com/svend4/nautilus`, но возможны альтернативные.

**Registry** — файл `nautilus.json` в корне Portal-репо, перечисляющий 
все Repos экосистемы с их метаданными.

**Adapter** — Python-модуль (или эквивалент на другом языке), 
реализующий `BaseAdapter` interface и переводящий native format Repo 
в унифицированный `PortalEntry`.

**Passport** — `passport.md` файл в корне каждого Repo, 
human-readable описание: что хранит, какая философия, кто автор, 
как работать.

**PortalEntry** — унифицированная структура данных, в которую 
адаптеры конвертируют native-записи при fetch.

**Bridge** — декларативное описание моста между концепциями 
разных Repos. Описан в `nautilus.json` в поле `bridges`.

**Consensus** — результат сопоставления найденных концептов между 
несколькими Repos. Может быть full (во всех Repos), partial (в 
некоторых), singular (только в одном).

**Compatibility Level** — целое число от 0 до 3, характеризующее 
степень интеграции Repo с экосистемой. Определение в разделе 5.

**Protocol Version** — semver-версия NPP, объявляемая в 
`nautilus.json` поле `protocol_version`.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[77-2-terminology]] (сходство 0.63)
- [[08-3-registry-nautilus-json]] (сходство 0.16)
- [[67-о-проекте]] (сходство 0.16)


<!-- see-also -->

---

**Смотрите также:**
- [[77-2-terminology]]
- [[08-3-registry-nautilus-json]]
- [[67-о-проекте]]
- [[78-3-registry-nautilus-json]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[77-2-terminology|2. Terminology]] _53%_
- [[79-4-passport-passport-md|4. Passport (`passport.md`)]] _29%_
- [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] _25%_
- [[68-about|🇬🇧 About]] _25%_
- [[74-abstract|Abstract]] _25%_
- [[78-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] _25%_
- [[82-7-portalentry-structure|7. PortalEntry Structure]] _25%_
- [[19-7-portalentry-structure|7. PortalEntry Structure]] _21%_
