---
template: project-component
version: "1.0"
author: "AnastasiyaW"
author_handle: "@Sonia_Black"
component: knowledge-space
projects: [knowledge-space]
layer: knowledge
license: MIT
maturity: beta
priority: 2
tags: [knowledge-space, reference, cards, agent-first, wiki, domains, research]
---
<!-- autofill-status -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Статус

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 998 |
| Слой | knowledge/orchestration |
| Контакт | [@AnastasiyaW](../../contacts/anastasiyaw.md) |
| Статус связи | не писали |

_Обновлено: 2026-05-10_

# knowledge-space[^knowledge-space]

<!-- toc-auto -->
## Contents

- [Статус](#статус)
- [Содержание](#содержание)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Синергия со Svyazi 2.0](#синергия-со-svyazi-20)
- [Применение в архитектуре Svyazi](#применение-в-архитектуре-svyazi)
- [Контакт](#контакт)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


<!-- toc -->
## Содержание

- [Статус](#статус)
- [Contents](#contents)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Синергия со Svyazi[^svyazi] 2.0](#синергия-со-svyazi-20)
- [Применение в архитектуре Svyazi](#применение-в-архитектуре-svyazi)
- [Контакт](#контакт)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

---


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> tags: [knowledge-space, reference, cards, agent-first, wiki, domains, research]
**Проекты:** Svyazi, AgentFS[^agentfs], knowledge-space, mclaude, LiteParse, Wikontic

---



<!-- summary: Agent-first референсная база знаний: 785+ карточек по 26 доменам, растущая из реальных research-сессий -->
<!-- tags: knowledge-space, agent, reference, cards, wiki-links, domains, research, inbox -->

## Профиль проекта

| Параметр | Значение |
|----------|---------|
| Автор | Sonia_Black / AnastasiyaW |
| GitHub | @Sonia_Black |
| Источник | Хабр + GitHub |
| Лицензия | **MIT** |
| Maturity | Активный OSS, база растёт почти ежедневно |
| Слой в Svyazi | knowledge |

## Что это

knowledge-space — это agent-first референсная база знаний: 785+ плотных карточек по 26 доменам, выращенная из реальных research-сессий автора. Ключевой принцип: карточки написаны «для агентов, не людей» — каждая содержит максимум структурированной информации в минимуме текста, gotchas (подводные камни) и wiki-links на связанные концепты.

База включает `research/inbox/` — поток необработанных исследовательских заметок, которые постепенно превращаются в нормализованные карточки знаний. Это реализует принцип episodic → semantic conversion из PROTOTYPE_SPEC.

## Ключевые особенности

- **Dense reference cards** — плотные карточки: минимум воды, максимум фактов
- **Gotchas** — явно помеченные подводные камни и типичные ошибки
- **Wiki-links** — [[двойные скобки]] для связей между концептами
- **`research/inbox/`** — необработанные исследовательские заметки (episodic)
- **26 доменов** — широкий охват: от ML до права и системного дизайна
- **785+ карточек** — реально накопленная, не синтетическая база
- **Agent-first дизайн** — структура оптимизирована для LLM[^llm]-чтения, не для людей

## Синергия со Svyazi 2.0

- **Внешний knowledge layer**: knowledge-space как upstream источник карточек для CardStore
- **research/inbox/** = episodic memory → CardEnvelope(state="raw") → normalizer → CardEnvelope(state="normalized")
- **Dense cards** — идеальный формат для TF-IDF[^tf_idf] векторизации: высокая информационная плотность
- **Gotchas как факты**: CardEnvelope(type="fact") для явных ограничений и предупреждений
- **Wiki-links** могут стать CardEdge(rel="references") при ingestion
- **MIT лицензия** — прямое использование без ограничений

## Применение в архитектуре Svyazi

knowledge-space закрывает слой "нормализованного знания" между raw research notes и структурированным GraphRAG. В то время как AgentFS управляет файловым layout, knowledge-space предоставляет уже структурированный корпус для начальной загрузки CardStore.

## Контакт

- Контактный файл: [docs/contacts/sonia-black.md](../../contacts/sonia-black.md)
- Упомянут в документах: 11 раз

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "knowledge-space"
```

## Смотрите также

- [AgentFS](agentfs.md) — файловое ядро, поверх которого knowledge-space размещается
- [mclaude](mclaude.md) — координация агентов, читающих knowledge-space параллельно
- [research-docs-liteparse](research-docs-liteparse.md) — ingestion pipeline для пополнения knowledge-space
- [Wikontic: семантический граф](wikontic.md) — граф-дополнение к reference-картам knowledge-space

---
_Создано: 2026-05-10_

<!-- backlinks -->

---

**Кто ссылается на этот документ (10):**
- [README](README.md)
- [agentfs](agentfs.md)
- [mclaude](mclaude.md)
- [research-docs-liteparse](research-docs-liteparse.md)
- [rufler](rufler.md)
- [memnet](../memory/memnet.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- _...ещё 2_



<!-- footnotes-added -->

---

[^llm]: Large Language Model — большая языковая модель

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^svyazi]: Главный проект: экосистема AI-компонентов

[^knowledge-space]: OSS-проект: база знаний 785+ карточек (MIT)

[^tf_idf]: Term Frequency–Inverse Document Frequency — метрика важности термина

<!-- similar-docs -->

---

**Похожие документы:**
- [knowledge-space](../../svyazi-2-0/components/knowledge-space.md) (сходство 0.95)
- [agentfs](agentfs.md) (сходство 0.28)
- [mclaude](mclaude.md) (сходство 0.28)

