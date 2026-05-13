# Happyin Knowledge Space (Анастасия) — детали

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Вариант D: продолжение поиска уникальных проектов и финальное ранжирование.
**Проекты:** knowledge-space

---
<!-- tags: knowledge, ingestion, architecture, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Вариант D: продолжение поиска уникальных проектов и финальное ранжирование.

3. Happyin Knowledge Space (Анастасия)

Проект: «785 статей. 26 доменов. Для агентов, не людей»

URL: https://habr.com/ru/articles/1026666/

Live: https://happyin.space/

Repo: https://github.com/AnastasiyaW/knowledge-space (MIT)

Что делает: Knowledge Space построенный специально для AI-агентов, не для людей. 785 статей в 26 доменах. Когда агент открывает проект, он сразу попадает в контекст «так делают здесь», не пересобирает с нуля.

Уникальные свойства:

Knowledge written for agents, not humans — fundamentally different design

Domain-specific freshness thresholds: алгоритмы стабильны (обновлять не нужно), diffusion training меняется каждые месяцы

Two-layer pipeline:

Layer 1: сырой research в inbox

Layer 2: separate session разбирает inbox, выделяет факты, переупаковывает в карточки, dedups, проверяет wiki-links

Build automation: одна сессия даёт 20-40 новых или обогащённых карточек за несколько часов

MIT license — open для использования и адаптации

Почему важно для нас: Это first-of-its-kind knowledge base built for AI consumption. Большинство knowledge bases (Obsidian vaults, wiki, etc.) написаны для человека, AI читает их «по совместительству». Анастасия flipped это: знания форматируются для AI primarily, человек secondary.

Для SGB Advocate Colleague это критически важно. SGB knowledge базы (статуты, прецеденты, шаблоны) могут быть форматированы для AI-агентов первично. Practitioner-readable as side-effect.

Также: Repository under MIT license, можно изучать архитектуру и адаптировать.

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Happyin Knowledge Space Анастасия детали"
```

## Смотрите также
- [04-mem0-letta-graphiti](04-mem0-letta-graphiti.md)
- [06-final-tier-ranking](06-final-tier-ranking.md)
- [01-coally](01-coally.md)
- [07-key-observation](07-key-observation.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [03-happyin-knowledge-space](../../obsidian/anthropic-vacancies/extra-collaborator-findings/03-happyin-knowledge-space.md) (сходство 0.98)
- [04-mem0-letta-graphiti](../../obsidian/anthropic-vacancies/extra-collaborator-findings/04-mem0-letta-graphiti.md) (сходство 0.25)
- [04-mem0-letta-graphiti](04-mem0-letta-graphiti.md) (сходство 0.25)

