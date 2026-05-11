# PDA-бот — «LLM как периферия»

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

---
<!-- tags: orchestration, architecture, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

AI-бот для самопознания
https://habr.com/ru/articles/1027210/
Автор строит систему, где LLM не ядро, а узел. Архитектура — Possibility-Driven Architecture (PDA): каждый ответ пользователя — неизменяемое событие (event sourcing), профиль — read model поверх event log, есть Stability Engine, Dialog Engine, Aeon Engine. Stability Engine отвечает за класс решений, которые LLM принимать не должен никогда. Это та же интуиция, что у Чуяна («гибрид LLM + детерминированный код, потому что LLM творец, а алгоритмами жёстко приводим в рамки»), но доведённая до предела: код целиком отвечает за стабильность, LLM — только генератор гипотез. Серия из четырёх статей у автора, видно, что это его главный проект.

Параллель к MoME-роутингу

Долой иерархию и роли — диссертация Виктории Дочкиной (Сбер, МФТИ)
https://habr.com/ru/articles/1017200/
Эксперимент: 8–16 LLM-агентов решают задачи по четырём протоколам коммуникации. Sequential-протокол (распределённая сеть, агенты видят только реальные завершённые результаты предшественников) выигрывает у Coordinator (центральный хаб) на 44% (Cohen's d = 1.86). Дочкина пишет диссертацию по автономным AI-системам, активно публикует. Это твой человек по теме «распределённое лучше центрального» — тот же тезис, что у тебя в Q6/MoME.

Источник данных и инфраструктурные кусочки

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "PDA бот LLM как периферия"
```

## Смотрите также
- 8-self-aware-[mcp-specs](../deep-pairs/8-self-aware-mcp-specs.md)
- [02-memnet](02-memnet.md)
- [3-zinc-hybrid-arch](../hardware-pairs/3-zinc-hybrid-arch.md)
- [05-supplementary-infrastructure](05-supplementary-infrastructure.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [03-pda-llm-as-periphery](../../obsidian/habr-unique-projects/key-findings/03-pda-llm-as-periphery.md) (сходство 0.95)
- [8-self-aware-mcp-specs](../deep-pairs/8-self-aware-mcp-specs.md) (сходство 0.24)
- [8-self-aware-mcp-specs](../../obsidian/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md) (сходство 0.23)

