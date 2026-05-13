# 2. Terminology

<!-- toc-auto -->
## Contents

- [2. Terminology](#2-terminology)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: rag, architecture, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

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
несколькими Repos. Может быть full (coverage = 1.0), partial 
(coverage < 1.0), absent (coverage = 0).

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

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "2 Terminology"
```

## Смотрите также
- [77-2-terminology](../../02-anthropic-vacancies/77-2-terminology.md)
- [07-2-terminology](../../02-anthropic-vacancies/07-2-terminology.md)
- [03-registry](03-registry.md)
- [05-compatibility-levels](05-compatibility-levels.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [01-introduction](01-introduction.md)
- [03-registry](03-registry.md)
- [12-onboarding-paths](12-onboarding-paths.md)
- [README](README.md)
- _...ещё 1_


<!-- similar-docs -->

---

**Похожие документы:**
- [02-terminology](../../obsidian/nautilus/npp-v1-1/02-terminology.md) (сходство 0.99)
- [77-2-terminology](../../obsidian/02-anthropic-vacancies/77-2-terminology.md) (сходство 0.81)
- [77-2-terminology](../../02-anthropic-vacancies/77-2-terminology.md) (сходство 0.81)

