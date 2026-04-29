# docs-toolkit

Universal toolkit для markdown documentation monorepos.

[![tests](https://img.shields.io/badge/tests-245-brightgreen)]()
[![python](https://img.shields.io/badge/python-3.10+-blue)]()
[![license](https://img.shields.io/badge/license-MIT-green)]()

## Что это

`docs-toolkit` превращает любой markdown-репозиторий в типизированную knowledge platform с:

- **Шаблоны** — JSON-Schema валидация документов
- **Ингестия** — PDF / EPUB / HTML / DOCX / Jupyter / MHTML / web
- **Embeddings** — TF-IDF + sentence-transformers с persistent SQLite cache
- **RAG** — retrieve → assemble → answer (Anthropic / OpenAI / Gemini / Ollama)
- **Knowledge graph** — NER + co-occurrence, экспорт в JSON / DOT / Mermaid
- **Background jobs** — async queue для долгих операций
- **Web dashboard** — встроенный HTTP сервер
- **Plugin system** — PEP 621 entry_points для third-party расширений

## Quickstart

```bash
pip install docs-toolkit
cd my-docs-repo
docstoolkit init
docstoolkit doctor
docstoolkit doc list-templates
docstoolkit search "my topic"
docstoolkit serve
```

## Содержание

- [Установка и конфигурация](installation.md)
- [Шаблоны и валидация](templates.md)
- [Ингестия документов](ingest.md)
- [Поиск и embeddings](search.md)
- [RAG: вопрос-ответ](rag.md)
- [Knowledge graph](graph.md)
- [Background jobs](jobs.md)
- [Web dashboard](serve.md)
- [Plugin development](plugins.md)
- [API Reference](api/)
- [CHANGELOG](../CHANGELOG.md)
- [SECURITY](../SECURITY.md)
- [CONTRIBUTING](../CONTRIBUTING.md)

## Архитектура

```
Ingest → Embed → Search → RAG → Graph
    ↓        ↓
 Cache   Background jobs
```

Все слои опциональны. Core (markdown ingest, TF-IDF embeddings, jobs queue, graph)
работает на чистом stdlib без зависимостей.
