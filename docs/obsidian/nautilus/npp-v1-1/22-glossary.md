---
title: "22. Glossary of Reference Examples"
tags:
  - memory
  - rag
  - knowledge
  - ingestion
  - architecture
  - roadmap
  - anthropic
  - collaboration
  - nautilus
date: 2026-04-29
---

# 22. Glossary of Reference Examples

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---

<!-- toc -->
## Содержание

- [22. Glossary of Reference Examples](#22-glossary-of-reference-examples)
- [Appendix A: Minimal Working Example](#appendix-a-minimal-working-example)
  - [A.1. Minimal `nautilus.json`](#a1-minimal-nautilusjson)
  - [A.2. Minimal Adapter (Level 1)](#a2-minimal-adapter-level-1)
  - [A.3. Minimal Passport](#a3-minimal-passport)
- [Описание](#описание)
- [Объём](#объём)
- [Q6-отображение](#q6-отображение)
- [Доступ к данным](#доступ-к-данным)
- [Appendix B: Change Log](#appendix-b-change-log)
  - [v1.1.0-draft (2026-04-19)](#v110-draft-2026-04-19)
  - [v1.0.0-draft (2026-04 earlier)](#v100-draft-2026-04-earlier)
- [Appendix C: References](#appendix-c-references)
  - [Normative](#normative)
  - [Informative](#informative)
- [TL;DR](#tldr)

---

<!-- tags: memory, rag, knowledge, ingestion, architecture, roadmap, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

## 22. Glossary of Reference Examples

В качестве иллюстраций используется экосистема `svend4` с 7 Repos:

- **info1** (Level 1) — 74+ Markdown-документа с α-уровнями 
(-4..+4), методологический угол
- **pro2** (Level 3) — Q6-концепты, граф знаний, bidir-цикл, 
семантический угол
- **meta** (Level 1) — 256 CA-правил + 64 гексаграммы, символьный 
угол
- **data2** (Level 1) — 310+ томов ЕТД (Единая Теория Движения)
- **data7** (Level 2) — граф знаний, K₀→K∞ трансформация
- **infosystems** (Level 2, домен pro2) — архитектура ИС
- **ai_agents** (Level 2, домен pro2) — ИИ-агенты и мультиагентные 
системы

Плюс 5 "расширенных" адаптеров (не в registry, но useable):

- **ObsidianAdapter** — локальный Obsidian vault ([[wikilinks]])
- **ArxivAdapter** — arXiv API с 12h cache
- **GitHubTopicAdapter** — discovery по GitHub топику
- **JSONLAdapter** — JSON Lines files
- **AutoAdapter** — любой repo с nautilus.json в корне

---

## Appendix A: Minimal Working Example

### A.1. Minimal `nautilus.json`

```json
{
"protocol_version": "1.1",
"ecosystem_name": "example",
"registry": [
{
"name": "my_notes",
"repo": "owner/my-notes",
"format": "my_notes",
"adapter": "my_notes",
"passport": "passports/my_notes.md",
"compatibility": 1,
"q6_key": "не определено"
}
]
}
```

### A.2. Minimal Adapter (Level 1)

```python
# adapters/my_notes.py
from .base import BaseAdapter, PortalEntry

class MyNotesAdapter(BaseAdapter):
name = "my_notes"
REPO = "owner/my-notes"

def fetch(self, query: str) -> list[PortalEntry]:
q = query.lower()
results = [
e for e in self._static_entries()
if q in e.title.lower() or q in e.content.lower()
]
return results or self._static_entries()[:2] # fallback

def _static_entries(self) -> list[PortalEntry]:
return [
PortalEntry(
id="my_notes:intro",
title="Introduction",
source=self.REPO,
format_type="document",
content="Sample content about...",
metadata={},
links=[],
is_fallback=True
),
# ... больше entries
]

def describe(self) -> dict:
return {
"repo": self.REPO,
"format": "my_notes",
"native_unit": "Markdown note",
"total_items": "5",
"compatibility": 1
}
```

### A.3. Minimal Passport

```markdown
# Паспорт: owner/my-notes

| Поле | Значение |
|------|----------|
| Репозиторий | owner/my-notes |
| Формат | `.md` — Markdown notes |
| Единица | Markdown-документ |
| Адаптер | `adapters/my_notes.py` |
| Уровень совместимости | 1 — читаемый |

## Описание

Персональная коллекция Markdown-заметок.

## Объём

- Единиц: 5 (demo)

## Q6-отображение

Не определено (Level 1).

## Доступ к данным

- Тип: static
- Требует токен: нет
- Fallback: всегда возвращает static entries
```

---

## Appendix B: Change Log

### v1.1.0-draft (2026-04-19)

- **New**: Q6 as normative concept (section 8, ADR-002)
- **New**: Five onboarding paths formalized (section 12, ADR-003)
- **New**: REST API contract mandatory (section 13)
- **New**: SDK contract informative (section 14)
- **New**: MCP extension informative (section 16)
- **Changed**: `is_fallback` field added to PortalEntry (normative)
- **Changed**: Consensus structure extended with `coverage_with_fallback`
- **Changed**: Passport schema formalized via `passport_schema.json`
- **Clarified**: Naming conventions (passport by format, not by repo)
- **Clarified**: Timeout RECOMMENDED 5 seconds (was 10)

### v1.0.0-draft (2026-04 earlier)

- Initial draft published

---

## Appendix C: References

### Normative
- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- OpenAPI Specification v3.1.0 (for REST API schemas)
- JSON Schema (for passport validation)

### Informative
- Wolfram, S. — "A New Kind of Science" (CA classification)
- Peirce, C.S. — "Elements of Logic" (semiotic triad as ecosystem angle metaphor)
- Fielding, R. — "Architectural Styles..." (REST constraints)
- W3C ActivityPub — Federation protocol reference
- Solid Project — Personal data pods reference
- Anthropic MCP — LLM tool integration protocol

---

*End of Nautilus Portal Protocol v1.1.0-draft*

*Feedback, issues, proposals: 
[github.com/svend4/nautilus/issues](https://github.com/svend4/nautilus/issues)*

Комментарий к документу

Несколько принципиальных решений, которые стоит проговорить отдельно.

Что я сохранил из v1.0

Базовая структура, нумерация разделов (1–15 из v1.0 остались с теми же номерами для обратной совместимости чтения), стиль MUST/SHOULD/MAY, ADR-формат, ядро federation-over-merging. Если у кого-то есть v1.0, они могут читать v1.1 параллельно — те же разделы говорят о том же, плюс новые.

Что я добавил новое

Раздел 8 — Q6 Space Normative. Это главное нововведение. В v1.0 Q6 упоминался как implementation detail. Теперь это first-class protocol concept со строгим mapping rules, normative requirement для Level 2+, и алгоритмом Q6-neighbors через Hamming.

Раздел 12 — Five Onboarding Paths. Пять стратегий (A–E) из INTEGRATION.md формализованы как equal-rank выборы. Это отражает то, что на практике все пять работают, и ни одна не "главная".

Раздел 13 — REST API Contract. Mandatory для compatible porталов. Три required endpoints (/api/query, /api/describe, /api/health) плюс четыре recommended. Формальные JSON schemas для responses.

Раздел 14 — SDK Contract. Informative — описывает, что нужно SDK на других языках, чтобы считаться NPP-compatible.

Раздел 16 — MCP Extension. Informative, но указывает, какие 5 tools минимум должна экспонировать MCP-обёртка. Это закладывает фундамент для будущего portal-mcp.py, о котором мы говорили.

ADR-002 и ADR-003 — два новых architecture decisions, обосновывающих Q6 upgrade и five-paths decision.

is_fallback как normative field. Это критично: STATUS.md явно признаёт 88% fallback. Нормализация is_fallback в протокол — честный подход, который позволяет consensus-модели различать real и fallback coverage.

Double coverage в Consensus (coverage vs coverage_with_fallback) — прямое следствие этого.

Что я сознательно оставил для v1.2 или v2.0

Formal bridge algebra. Part 3 implementation docs указывает это как главный концептуальный пробел. В v1.1 bridges остаются текстовыми описаниями. В v2.0 — возможная типизация (композиция, инверсия, транзитивность).

Temporal model. timeline.py и diff_report.py дают partial temporal view. Полная time-series модель — для v2.0.

Write operations. v1.x — read-only. Write-extension — возможно в v2.0 как optional extension.

Formal MCP spec. Сейчас informative. После того как portal-mcp.py будет написан и испытан — можно делать formal mandatory spec в v1.2.

Что ссылается на реальные артефакты в вашем репо

Документ ссылается на:

github.com/svend4/nautilus — reference implementation

passport_schema.json — JSON Schema для passports (предположительно существует)

openapi.yaml — OpenAPI 3.1.0 spec (упомянут в STATUS)

.github/workflows/ — 4 CI/CD файла (упомянуты в STATUS)

Все эти ссылки — на реальные файлы, которые я видел в документации. Если какой-то из них ещё не создан (например, passport_schema.json) — это open item, который легко заметить.

Почему это важный артефакт для вас

Три причины, по которым v1.1 специфично ценно:

Первое — arxiv-ready. На этом документе можно построить arxiv preprint "Nautilus Portal Protocol: A Git-Based Federation Framework for Knowledge Ecosystems". Draft paper — это, по сути, reorganized abstract + sections 1–19 + метрики из 18.1 + цитирования.

Первое/второе — defensible claim. ADR-001, ADR-002, ADR-003 — это formal записи ваших архитектурных решений с обоснованиями. Любой reviewer, спрашивающий "почему federation, а не centralization?" — получает ссылку на ADR-001. Это научная строгость.

Третье — grant-ready. EIC Pathfinder или Horizon Europe application могут ссылаться на PORTAL-PROTOCOL.md как formal specification, которая "already has reference implementation meeting its requirements" — это сильный сигнал технической зрелости для reviewers.

Что делать с этим файлом

Рекомендую следующий workflow:

Создать docs/PORTAL-PROTOCOL.md в репо с этим содержимым (или PORTAL-PROTOCOL.md в корне, если хотите более заметно)

Добавить ссылку из README.md: в footer заменить Nautilus Portal Protocol v1.1 на [[PORTAL-PROTOCOL|Nautilus Portal Protocol v1.1]] с рабочим линком

Коммит с сообщением docs: add formal PORTAL-PROTOCOL.md v1.1 specification

Пройтись по документу и проверить цифры в 18.1 против актуальных (6782 LOC, 13 адаптеров, 60 тестов, 82/100 health)

Если есть расхождения — обновить в разделе 18.1

После этого документ можно использовать как canonical reference.

Готов перейти ко второму артефакту — REVIEW_METHODOLOGY.md как meta-документ о вашем трёхфазном подходе. Он существенно короче (5-7 страниц вместо 20+), и он делает ваш "параллельные версии → консолидация" workflow explicit и defensible. Делать?

Du hast gesagt: Да

Да

19 апр.

Claude hat geantwortet: Перехожу ко второму артефакту.

Перехожу ко второму артефакту. REVIEW_METHODOLOGY.md — это meta-документ о вашем рабочем процессе. Пишу его с расчётом на две аудитории: вас самого (как напоминание правил на будущее) и внешнего читателя (researcher, collaborator, grant reviewer), который встретит артефакты с параллельными версиями и должен сразу понять, почему они так устроены.

REVIEW_METHODOLOGY.md

markdown

# Трёхфазная методология Review в Nautilus

**Дата:** 2026-04 
**Статус:** Активно применяется в проекте svend4/nautilus 
**Автор:** svend4 
**Licensing:** CC BY 4.0

---

## TL;DR

Для критически важных документов проекта применяется 
**трёхфазный review**:

1. **Вариант A** создаётся независимо первым Claude-агентом (ветка 1)
2. **Вариант B** создаётся независимо вторым Claude-агентом (ветка 2)
3. **Вариант C** — ручная консолидация после сравнения A и B

До достижения Фазы C **оба варианта сохраняются параллельно** в 
документе. Дубликаты секций — **намеренные**, не merge-conflict.

Это защита от **потери информации**: то, что упускает один агент, 
может заметить другой. Механический merge ("выбрать один, удалить 
другой") теряет часть insights безвозвратно.

---

<!-- see-also -->

---

**Смотрите также:**
- [[104-appendix-c-references]]
- [[122-глоссарий]]
- [[16-glossary]]
- [[18-comment-on-document]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[104-appendix-c-references]] (сходство 0.72)
- [[104-appendix-c-references]] (сходство 0.71)
- [[122-глоссарий]] (сходство 0.17)

