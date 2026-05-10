# Комбинация 7: Crawl4AI × Docling × Yodoca consolidator

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Yodoca

---
<!-- tags: memory, rag, knowledge, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 7 Crawl4AI Docling Yodoca"
```

## Смотрите также
- [02-knowledge-graphs](../../03-technology-combinations/02-knowledge-graphs.md)
- 04-parsing-s-llm-graph-[rag-pravilnaya-agentskaya-arkhitektura](04-parsing-s-llm-graph-rag-pravilnaya-agentskaya-arkhitektura.md)
- [15-self-consolidating-legal-corpus](15-self-consolidating-legal-corpus.md)
- [10-legal-document-intelligence-pipeline](10-legal-document-intelligence-pipeline.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [01-08-summary](../synthesis-tables/01-08-summary.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал доступен для семантического поиска, BM25 и навигации через граф концептов._ _Материал доступен для поиска._ _Индексировано._
