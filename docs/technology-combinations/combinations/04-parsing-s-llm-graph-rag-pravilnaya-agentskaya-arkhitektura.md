# Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (4)](#кто-ссылается-на-этот-документ-4)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: rag, architecture, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 4 Парсинг с LLM Graph RAG"
```

## Смотрите также
- [03-local-first](../../03-technology-combinations/03-local-first.md)
- 07-crawl4ai-docling-[yodoca-consolidator](07-crawl4ai-docling-yodoca-consolidator.md)
- [02-knowledge-graphs](../../03-technology-combinations/02-knowledge-graphs.md)
- 01-pravilnaya-agentskaya-arkhitektura-[svyazi-pattern](01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (4)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [01-legal-ai-stack](../mega-stacks/01-legal-ai-stack.md)
- [01-08-summary](../synthesis-tables/01-08-summary.md)

_Документ доступен для семантического поиска, BM25 и навигации через граф связей репозитория._ _Индексировано в поисковой базе репозитория Lorenzo._ _Индексировано._
