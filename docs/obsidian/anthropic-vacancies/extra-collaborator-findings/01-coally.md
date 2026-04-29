---
title: "CoAlly — distributed shared memory для AI-агентов"
tags:
  - rag
  - security
  - architecture
  - anthropic
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

# CoAlly — distributed shared memory для AI-агентов

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Вариант D: продолжение поиска уникальных проектов и финальное ранжирование.

---
<!-- tags: rag, security, architecture, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Вариант D: продолжение поиска уникальных проектов и финальное ранжирование.

Итоги расширенного поиска — три новых критически важных проекта

1. CoAlly — distributed shared memory для AI-агентов

Проект: «Контекстная амнезия: три агента, три IDE, ноль общей памяти»

URL: https://habr.com/ru/articles/1021622/

Что делает: Решает проблему «контекстной амнезии», когда несколько AI-агентов работают над одним проектом, но не имеют общей памяти. Roy агентов: один проектирует, другой реализует, третий ревьюит, четвёртый тестирует, пятый деплоит — и каждому нужен доступ к общей persistent memory о том, что было решено и почему.

Ключевые особенности:

Shared memory layer между разными AI-tools

Автоматический knowledge scan — система ищет ADR, .memorybank, docs

Эмбеддинг и контекстуализация артефактов репозитория

Архитектура безопасности с изоляцией данных

Интеграция с A2A (Agent-to-Agent protocol) от Google

Personalized PageRank по графу знаний (HippoRAG, Stanford/OSU)

Граф связей: баг ↔ модуль ↔ архитектурное решение ↔ бизнес-требование

Процедурное знание (stand: в этом проекте всегда пишем тесты ≥80%)

Почему важно для нас: CoAlly directly implements концепцию shared memory layer для multi-agent collaboration. Это точно тот компонент, которого не хватало в нашей стек поверх HMP. Если HMP — federation protocol, то CoAlly — practical shared memory implementation.

<!-- see-also -->

---

**Смотрите также:**
- [[13-appendix-b-examples]]
- [[04-mem0-letta-graphiti]]
- [[02-vitaly-graph-cognitive-memory]]
- [[02-formal-workflow]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[00-tldr]] (сходство 0.20)
- [[14-main-technical-risks]] (сходство 0.19)
- [[07-key-observation]] (сходство 0.19)

