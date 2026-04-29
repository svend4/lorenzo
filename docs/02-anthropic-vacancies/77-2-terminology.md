# 2. Terminology

<!-- summary -->
> **Ecosystem** — набор репозиториев, участвующих в одной федерации.

---
<!-- tags: rag, architecture, collaboration -->




## 2. Terminology

**Ecosystem** — набор репозиториев, участвующих в одной федерации. 
Имеет уникальное имя (например, `svend4`).

**Repository-participant** (далее — **Repo**) — Git-репозиторий, 
содержащий минимум `nautilus.json` в корне и/или зарегистрированный 
в registry портала.

**Native format** — исходный формат данных в Repo, определяемый автором. 
Может быть любым: Markdown, JSON, YAML, plain text, бинарный формат. 
NPP не ограничивает native format.

**Portal** — implementation NPP, которая загружает registry, 
инстанцирует адаптеры и выполняет query-операции. Reference 
implementation: `github.com/svend4/nautilus`, но альтернативные 
порталы совместимы через соответствие этому протоколу.

**Registry** — файл `nautilus.json` в корне Portal-репо, перечисляющий 
все Repos экосистемы с их метаданными.

**Adapter** — Python-модуль (или эквивалент на другом языке), 
реализующий `BaseAdapter` interface и переводящий native format Repo 
в унифицированный `PortalEntry`.

**Passport** — `passport.md` файл, human-readable описание Repo, 
располагается в `passports/<format>.md` в Portal-репо. Валидируется 
по `passport_schema.json`.

**PortalEntry** — унифицированная структура данных, в которую 
адаптеры конвертируют native-записи при fetch.

**Bridge** — декларативное описание моста между концепциями разных 
Repos. Описан в `nautilus.json` в поле `bridges` и в passport 
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
`PortalEntry.is_fallback = True`.

**Protocol Version** — semver-версия NPP, объявляемая в 
`nautilus.json` поле `protocol_version` (или `nautilus_version` 
для v1.x из-за исторических причин).

**Onboarding Path** — один из пяти стандартных способов подключения 
Repo к экосистеме (A–E, см. раздел 12).

---

<!-- similar-docs -->

---

**Похожие документы:**
- [07-2-terminology](docs/02-anthropic-vacancies/07-2-terminology.md) (сходство 0.63)
- [78-3-registry-nautilus-json](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md) (сходство 0.16)
- [08-3-registry-nautilus-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [07-2-terminology](docs/02-anthropic-vacancies/07-2-terminology.md)
- [78-3-registry-nautilus-json](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md)
- [08-3-registry-nautilus-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md)
- [67-о-проекте](docs/02-anthropic-vacancies/67-о-проекте.md)

