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
- [02-knowledge-graphs](docs/03-technology-combinations/02-knowledge-graphs.md)
- [04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura](docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md)
- [15-self-consolidating-legal-corpus](docs/technology-combinations/combinations/15-self-consolidating-legal-corpus.md)
- [10-legal-document-intelligence-pipeline](docs/technology-combinations/combinations/10-legal-document-intelligence-pipeline.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [02-knowledge-graphs](docs/03-technology-combinations/02-knowledge-graphs.md) (сходство 0.27)
- [04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura](docs/technology-combinations/combinations/04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md) (сходство 0.27)
- [02-knowledge-graphs](docs/obsidian/03-technology-combinations/02-knowledge-graphs.md) (сходство 0.27)

