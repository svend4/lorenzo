# Комбинация 7: Crawl4AI × Docling × Yodoca consolidator

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
