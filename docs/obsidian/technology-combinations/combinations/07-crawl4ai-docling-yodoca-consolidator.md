---
title: "Комбинация 7: Crawl4AI × Docling × Yodoca consolidator"
tags:
  - memory
  - rag
  - knowledge
  - collaboration
  - technology-combinations
date: 2026-04-29
---

# Комбинация 7: Crawl4AI × Docling × Yodoca consolidator

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Yodoca

---
<!-- tags: memory, rag, knowledge, collaboration -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Crawl4AI (habr.com/ru/articles/875088/) — open-source веб-скрейпинг для LLM, оптимизация для обучения моделей

Docling (от IBM Research) — структурированный DoclingDocument, таблицы/параграфы как объекты

Yodoca (habr.com/ru/articles/1006622/) — агент-консолидатор, ночные cron-задачи, Ebbinghaus decay

Дети:

7.1 Self-consolidating legal corpus

Crawl4AI собирает новые решения Sozialgericht и BSG с сайтов. Docling парсит в структуру. Yodoca-консолидатор ночью:

Извлекает durable knowledge (прецеденты, применённые статьи, аргументы)

Старые неиспользуемые дела затухают по Эббингаузу

Часто используемые — укрепляются

Результат: корпус сам поддерживает актуальность, не нужно вручную чистить старые дела.

7.2 Wikipedia-style legal knowledge base

Crawl4AI + Docling + Yodoca + LLM Wiki (Obsidian плагин):

Каждое новое решение → markdown-страница в Obsidian vault

Консолидатор извлекает wikilinks между делами

Graph view показывает связи между прецедентами

Поиск через гибридный RAG (векторный + BM25 + graph traversal)

<!-- see-also -->

---

**Смотрите также:**
- [[02-knowledge-graphs]]
- [[04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura]]
- [[15-self-consolidating-legal-corpus]]
- [[10-legal-document-intelligence-pipeline]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[02-knowledge-graphs]] (сходство 0.27)
- [[04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura]] (сходство 0.27)
- [[02-knowledge-graphs]] (сходство 0.27)

