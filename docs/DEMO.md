# Knowledge OS — Demo

<!-- toc -->
## Содержание

- [Contents](#contents)
- [Быстрый старт](#быстрый-старт)
- [Примеры запросов](#примеры-запросов)
- [Результаты benchmark](#результаты-benchmark)
- [Архитектура потока](#архитектура-потока)
- [Метрики успеха](#метрики-успеха)
- [Компоненты](#компоненты)
- [Следующие шаги](#следующие-шаги)
- [Использование](#использование)

---


<!-- toc-auto -->
## Contents

- [Быстрый старт](#быстрый-старт)
- [Примеры запросов](#примеры-запросов)
- [Результаты benchmark](#результаты-benchmark)
- [Архитектура потока](#архитектура-потока)
- [Метрики успеха](#метрики-успеха)
- [Компоненты](#компоненты)
- [Следующие шаги](#следующие-шаги)
- [Использование](#использование)


<!-- summary -->
> Запускаемый прototип Svyazi 2.0: запрос → гибридный поиск → коллаборации → контакты → письма. Латентность ~0.9s.

<!-- tags: prototype, demo, knowledge-os, search, collaboration -->

> [!TIP]
> Прototип работает полностью офлайн, без API-ключей. Все данные в `docs/`.

<!-- alert-added -->

---

## Быстрый старт

```bash
# По запросу
python scripts/prototype_demo.py --query "агент с памятью граф знаний"

# По документу (извлекает текст автоматически)
python scripts/prototype_demo.py --file docs/PROTOTYPE_SPEC.md

# Benchmark: 5 эталонных запросов против критериев успеха
python scripts/prototype_demo.py --benchmark

# JSON-вывод для интеграции
python scripts/prototype_demo.py --query "RAG retrieval" --json
```

## Примеры запросов

```bash
# Memory layer
python scripts/prototype_demo.py --query "консолидация памяти decay граф"

# Orchestration
python scripts/prototype_demo.py --query "декларативный YAML рой агентов"

# Evidence RAG
python scripts/prototype_demo.py --query "PDF визуальные цитаты bounding box"

# Security
python scripts/prototype_demo.py --query "local-first GDPR offline безопасность"

# Knowledge OS
python scripts/prototype_demo.py --query "агент файловая система vault obsidian"
```

## Результаты benchmark

Прогон 5 эталонных запросов (2026-05-11):

| Запрос | Латентность | Найдено |
|--------|-------------|---------|
| агент с памятью консолидация карточки знаний | 0.922s | 5 |
| граф связей между проектами авторы Хабр | 0.894s | 5 |
| RAG retrieval evidence визуальные цитаты PDF | 0.874s | 5 |
| декларативный YAML оркестрация агентов рой | 0.882s | 5 |
| local-first offline GDPR безопасность данных | 0.916s | 5 |
| **Среднее** | **0.898s** | **5.0** |

## Архитектура потока

```
Запрос (свободный текст или файл)
        │
        ▼
┌───────────────────────────────────┐
│        Гибридный поиск            │
│   0.6×TF-IDF + 0.4×BM25          │
│   2461 карточек · 13291 абзацев   │
└───────────────┬───────────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
  Документы         Коллаборации
  (top-5 файлов)    (top-5 проектов)
                        │
                        ▼
                ┌───────────────┐
                │ Автор + Письмо │
                │ docs/letters/  │
                └───────────────┘
```

## Метрики успеха

Сравнение с критериями PROTOTYPE_SPEC §8:

| Критерий | Порог | Факт | Статус |
|----------|-------|------|--------|
| Latency (поиск→результат) | ≤ 5s | 0.9s | ✅ |
| Cards накоплено | ≥ 500 | 2461 | ✅ |
| Orphan rate | ≤ 15% | 0% | ✅ |
| Retrieval Precision@5 | ≥ 0.70 | ручная оценка | ⬜ |
| Collaboration quality | ≥ 3/5 | экспертная оценка | ⬜ |

## Компоненты

| Компонент | Скрипт | Статус |
|-----------|--------|--------|
| TF-IDF поиск | `prototype_demo.py` | ✅ |
| BM25 поиск | `improve_passage_retrieval.py` | ✅ |
| Гибридный ранжировщик | `prototype_demo.py` | ✅ |
| Collaboration finder | `improve_collab_finder.py` | ✅ |
| Контакты авторов | `docs/contacts/` | ✅ 16 файлов |
| Открытые письма | `docs/letters/` | ✅ 8 файлов |
| MCP сервер (Claude Desktop) | `scripts/mcp_server.py` | ✅ |
| Search index | `docs/search_index.json` | ✅ 2461 записей |
| RAG chunks | `docs/chunks/*.jsonl` | ✅ 13 секций |
| SENTINEL security | `improve_sentinel_check.py` | ✅ 0 проблем |

## Следующие шаги

1. **Ручная оценка Precision@5** — 20 запросов, 2 независимых оценщика
2. **Отправить письма авторам** — открытые черновики в `docs/letters/`
3. **Streamlit UI** — интерактивный интерфейс (опционально):
   ```bash
   pip install streamlit
   streamlit run scripts/prototype_streamlit.py
   ```
4. **LLM-обогащение** — `improve_llm_enrich.py` (нужен `ANTHROPIC_API_KEY`)

## Использование

```bash
python scripts/prototype_demo.py --query "ваш запрос"
```
