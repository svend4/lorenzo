# 2. Terminology

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Terminology Ecosystem — набор репозиториев, участвующих в одной федерации.
> ✅ **Результат:** Fallback — адаптер вернул статические (заранее заготовленные) данные, а не результат реального поиска.
> 🏷️ **Ключевые слова:** `nautilus`, `registry`, `anthropic`, `vacancies`, `terminology`, `native`, `format`, `passport`
>


<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> **Ecosystem** — набор репозиториев, участвующих в одной федерации.

---

<!-- toc -->
## Содержание

- [2. Terminology](#2-terminology)

---

<!-- tags: rag, architecture, collaboration -->




## 2. Terminology

**Ecosystem** — набор репозиториев, участвующих в одной федерации. 
Имеет уникальное имя (например, `svend4`).

**Repository-participant** (далее — **Repo**) — Git-репозиторий, 
содержащий минимум `[nautilus](../05-habr-projects/memory/memnet.md).json` в корне и/или зарегистрированный 
в registry портала.

**Native format** — исходный формат данных в Repo, определяемый автором. 
Может быть любым: Markdown, JSON, YAML, plain text, бинарный формат. 
NPP не ограничивает native format.

**Portal** — implementation NPP, которая загружает registry, 
инстанцирует адаптеры и выполняет query-операции. Reference 
implementation: `github.com/svend4/nautilus`, но альтернативные 
порталы совместимы через соответствие этому протоколу.

**Registry** — файл `[nautilus](../05-habr-projects/memory/memnet.md).json` в корне Portal-репо, перечисляющий 
все Repos экосистемы с их метаданными.

**Adapter** — Python-модуль (или эквивалент на другом языке), 
реализующий `[BaseAdapter](01-интегральный-анализ-профиля-svend4.md)` interface и переводящий native format Repo 
в унифицированный `[PortalEntry](01-интегральный-анализ-профиля-svend4.md)`.

**Passport** — `passport.md` файл, human-readable описание Repo, 
располагается в `passports/<format>.md` в Portal-репо. Валидируется 
по `passport_schema.json`.

**[PortalEntry](01-интегральный-анализ-профиля-svend4.md)** — унифицированная структура данных, в которую 
адаптеры конвертируют native-записи при fetch.

**Bridge** — декларативное описание моста между концепциями разных 
Repos. Описан в `[nautilus](../05-habr-projects/memory/memnet.md).json` в поле `bridges` и в passport 
соответствующего репо.

**Consensus** — результат сопоставления найденных концептов между 
несколькими Repos. Может быть full (coverage == 1.0), partial 
(coverage < 1.0), absent (coverage == 0).

**Compatibility Level** — целое число от 0 до 3, характеризующее 
степень интеграции Repo с экосистемой. Определение в разделе 5.

**Q6-координата** — 6-битная строка (строка символов «0» и «1» 
длиной 6), обозначающая позицию концепта в 6-мерном бинарном 
гиперкубе {0,1}⁶ (64 вершины).

**Q6-соседство** — отношение между Q6-координатами с расстоянием 
Хэмминга ≤ N. По умолчанию N = 1 (соседи, отличающиеся в одном бите).

**Fallback** — адаптер вернул статические (заранее заготовленные) 
данные, а не результат реального поиска. Обозначается 
`[PortalEntry](01-интегральный-анализ-профиля-svend4.md).is_fallback = True`.

**Protocol Version** — semver-версия NPP, объявляемая в 
`[nautilus](../05-habr-projects/memory/memnet.md).json` поле `protocol_version` (или `nautilus_version` 
для v1.x из-за исторических причин).

**Onboarding Path** — один из пяти стандартных способов подключения 
Repo к экосистеме (A–E, см. раздел 12).

---

<!-- similar-docs -->

---

**Похожие документы:**
- [07-2-terminology](07-2-terminology.md) (сходство 0.63)
- [78-3-registry-[nautilus](../05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md) (сходство 0.16)
- [08-3-registry-[nautilus](../05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [07-2-terminology](07-2-terminology.md)
- [78-3-registry-[nautilus](../05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md)
- [08-3-registry-[nautilus](../05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md)
- [67-о-проекте](67-о-проекте.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [109-3-принципы-консолидации-фаза-c](109-3-принципы-консолидации-фаза-c.md)
- 124-конфигурация-для-[claude-desktop](124-конфигурация-для-claude-desktop.md)
- [67-о-проекте](67-о-проекте.md)
- [74-abstract](74-abstract.md)
- 91-16-[mcp-extension-informative](91-16-mcp-extension-informative.md)
- [README](README.md)

