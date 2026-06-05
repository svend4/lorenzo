---
title: "Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура"
tags:
  - rag
  - architecture
  - collaboration
  - technology-combinations
date: 2026-05-13
---

# Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: rag, architecture, collaboration -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Парсинг с LLM (habr.com/ru/articles/892954/) — Structured Outputs, Pydantic, автоматическое извлечение структуры

Graph-RAG (habr.com/ru/articles/871700/) — Microsoft Research, графы знаний вместо плоского RAG

Durable state агенты (habr.com/ru/articles/1028290/)

Дети:

4.1 Self-building legal knowledge graph

Агент читает новые решения Sozialgericht:

Парсер LLM: извлекает сущности (судья, § закона, истец, ответчик, решение)

Graph builder: строит граф знаний (BSG B 8 SO 9/19 R → § 78 Abs. 6 SGB IX → Antragsteller)

Durable state: граф персистентен между запусками, растёт автоматически

Query: вопросы типа "найди дела где § 78 + retroactive budget + BSG" идут через Graph-RAG, не через векторный поиск

Качество: находит многошаговые связи, которые обычный RAG пропускает.

4.2 Progressive knowledge refinement

Первый проход — LLM парсит грубо, добавляет узлы в граф с confidence=low. Агент периодически переобрабатывает low-confidence узлы через более сильную модель, повышает точность. Граф становится точнее со временем без переобработки всего корпуса.

<!-- see-also -->

---

**Смотрите также:**
- [[03-local-first]]
- [[07-crawl4ai-docling-yodoca-consolidator]]
- [[02-knowledge-graphs]]
- [[01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[03-local-first]] (сходство 0.27)
- [[07-crawl4ai-docling-yodoca-consolidator]] (сходство 0.27)
- [[03-local-first]] (сходство 0.26)


<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [READABILITY](../../../READABILITY.md)
- [READING_TIME](../../../READING_TIME.md)
- [SEARCH](../../../SEARCH.md)
- [TABLES](../../../TABLES.md)
- [04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura](../../../technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md)
- [07-crawl4ai-docling-yodoca-consolidator](../../../technology-combinations/combinations/07-crawl4ai-docling-yodoca-consolidator.md)

