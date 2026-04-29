# Обработка больших массивов документов — Руководство

> Полное руководство по обработке, анализу и управлению большими коллекциями документов.
> Основано на реальной практике проекта Lorenzo: 9 MHTML/Markdown файлов → 483 структурированных документа.

---

## Содержание

| # | Тема | Описание |
|---|------|---------|
| [01](01-overview.md) | Обзор и таксономия | 8 уровней обработки от extraction до automation |
| [02](02-extraction.md) | Извлечение | MHTML → Markdown, форматы, качество |
| [03](03-chunking.md) | Чанкинг | 6 стратегий разбивки: фиксированный, по заголовкам, семантический |
| [04](04-structuring.md) | Структурирование | TOC, теги, шаблоны, перекрёстные ссылки |
| [05](05-analysis.md) | Анализ и NLP | TF-IDF, TextRank, граф концептов, противоречия |
| [06](06-search.md) | Поиск | grep → BM25 → фасеты → пассажи → LLM Q&A |
| [07](07-llm.md) | LLM-обогащение | 5 скриптов, 3 стратегии, ~$0.10 на весь проект |
| [08](08-export.md) | Экспорт | Obsidian, EPUB, RSS, JSON, JSONL, MCP |
| [09](09-automation.md) | Автоматизация | Оркестратор, watcher, CI/CD, MCP |
| [10](10-future.md) | Инновационные подходы | Векторный поиск, граф знаний, мультиагент |

---

## Быстрый старт

```bash
# Запустить всё разом (умный режим)
python scripts/improve_run_all.py --smart

# Только быстрые скрипты
python scripts/improve_run_all.py --fast

# Конкретная группа
python scripts/improve_run_all.py --group quality
python scripts/improve_run_all.py --group deeptext
```

---

## Единый документ

→ [PROCESSING_GUIDE.md](PROCESSING_GUIDE.md) — все 10 частей в одном файле
