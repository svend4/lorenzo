# 2. Terminology

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Terminology Ecosystem — набор репозиториев, участвующих в одной федерации.
> ✅ **Результат:** Consensus — результат сопоставления найденных концептов между несколькими Repos.
> 🏷️ **Ключевые слова:** `nautilus`, `registry`, `anthropic`, `vacancies`, `terminology`, `native`, `repos`, `проекте`
>


<!-- summary -->
> **Ecosystem** — набор репозиториев, участвующих в одной федерации.

---
<!-- tags: architecture, collaboration -->




## 2. Terminology

**Ecosystem** — набор репозиториев, участвующих в одной федерации. 
Имеет уникальное имя (например, `svend4`).

**Repository-participant** (далее — **Repo**) — Git-репозиторий, 
содержащий минимум `[nautilus](../docs/05-habr-projects/memory/memnet.md).json` и `passport.md` в корне.

**Native format** — исходный формат данных в Repo, определяемый автором. 
Может быть любым: Markdown, JSON, YAML, plain text, бинарный формат, 
и так далее. NPP не ограничивает native format.

**Portal** — implementation NPP, которая загружает registry, инстанцирует 
адаптеры и выполняет query-операции. Reference implementation: 
`github.com/svend4/nautilus`, но возможны альтернативные.

**Registry** — файл `[nautilus](../docs/05-habr-projects/memory/memnet.md).json` в корне Portal-репо, перечисляющий 
все Repos экосистемы с их метаданными.

**Adapter** — Python-модуль (или эквивалент на другом языке), 
реализующий `[BaseAdapter](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)` interface и переводящий native format Repo 
в унифицированный `[PortalEntry](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)`.

**Passport** — `passport.md` файл в корне каждого Repo, 
human-readable описание: что хранит, какая философия, кто автор, 
как работать.

**[PortalEntry](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)** — унифицированная структура данных, в которую 
адаптеры конвертируют native-записи при fetch.

**Bridge** — декларативное описание моста между концепциями 
разных Repos. Описан в `[nautilus](../docs/05-habr-projects/memory/memnet.md).json` в поле `bridges`.

**Consensus** — результат сопоставления найденных концептов между 
несколькими Repos. Может быть full (во всех Repos), partial (в 
некоторых), singular (только в одном).

**Compatibility Level** — целое число от 0 до 3, характеризующее 
степень интеграции Repo с экосистемой. Определение в разделе 5.

**Protocol Version** — semver-версия NPP, объявляемая в 
`[nautilus](../docs/05-habr-projects/memory/memnet.md).json` поле `protocol_version`.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [77-2-terminology](docs/02-anthropic-vacancies/77-2-terminology.md) (сходство 0.63)
- [08-3-registry-[nautilus](../docs/05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) (сходство 0.16)
- [67-о-проекте](docs/02-anthropic-vacancies/67-о-проекте.md) (сходство 0.16)


<!-- see-also -->

---

**Смотрите также:**
- [77-2-terminology](docs/02-anthropic-vacancies/77-2-terminology.md)
- [08-3-registry-[nautilus](../docs/05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md)
- [67-о-проекте](docs/02-anthropic-vacancies/67-о-проекте.md)
- [78-3-registry-[nautilus](../docs/05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md)

