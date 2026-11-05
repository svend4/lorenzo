---
state: normalized
---

# MarkItDown — универсальный конвертер документов в Markdown для LLM

<!-- toc-auto -->
<!-- tags: markitdown, docs -->


<!-- summary -->
> Автор: Microsoft (open source) Хабр: https://habr.com/ru/articles/890774/ (упомянут в карте OSS-инструментов для AI-агентов)
Хабр: https://habr.com/ru/articles/890774/ (упомянут в карте OSS-инструментов для AI-агентов)  
GitHub: https://github.com/microsoft/markitdown (MIT, 91k+ stars)  
Слой: ingestion / document-AI / preprocessing  
Дата:


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Microsoft (open source)  
**Хабр:** https://habr.com/ru/articles/890774/ (упомянут в карте OSS-инструментов для AI-агентов)  
**GitHub:** https://github.com/microsoft/markitdown (MIT, 91k+ stars)  
**Слой:** ingestion / document-AI / preprocessing  
**Дата:** конец 2024 → 2025–2026 (активная разработка)  
**Уникальность:** MIT-лицензия + 91k stars = де-факто стандарт конвертации документов для RAG. Принимает **любой формат** (PDF, DOCX, PPTX, XLSX, HTML, изображения, ZIP) → Markdown с сохранением заголовков, таблиц, списков. Нативная интеграция с Microsoft AutoGen и Azure.

## Поддерживаемые форматы

| Формат | Что сохраняется |
|--------|----------------|
| PDF | текст, заголовки (эвристика) |
| DOCX / PPTX | заголовки, таблицы, списки, изображения (alt-text через LLM) |
| XLSX | таблицы → Markdown-таблицы |
| HTML | структура, ссылки |
| Изображения (PNG/JPG) | описание через LLaVA / любой VLM |
| ZIP | рекурсивная обработка вложений |

## Архитектура pipeline

```
Документ любого формата
        ↓
MarkItDown (Python, pip install markitdown)
        ↓
Чистый Markdown (заголовки + таблицы + списки)
        ↓
improve_chunk_semantic.py → all_chunks.jsonl
        ↓
Vector DB (Qdrant / pgvector) → RAG
```

## Ключевые преимущества

- **MIT лицензия** — полная свобода использования
- **Без зависимостей** от облака (можно офлайн)
- **Сохраняет структуру** — таблицы в Markdown, заголовки, списки
- **LLM-friendly** — output сразу готов для chunking / embedding
- **AutoGen integration** — нативный инструмент в Microsoft multi-agent stack

## Почему важно для Lorenzo

Lorenzo сейчас обрабатывает только **уже готовые Markdown файлы**.  
MarkItDown открывает **ingestion pipeline для внешних документов**:

```bash
# Новый сценарий с MarkItDown:
markitdown habr_article.pdf -o docs/05-habr-projects/new_project.md
python scripts/improve_index_update.py --incremental
python scripts/improve_card_index.py --build --incremental
# → PDF статья с Хабра стала карточкой в Lorenzo corpus
```

## Сравнение с текущим стеком Lorenzo

| Задача | Сейчас | С MarkItDown |
|--------|--------|--------------|
| Добавить PDF | вручную копировать | markitdown doc.pdf → .md → corpus |
| Обработать DOCX | не поддерживается | автоматически |
| Изображения в doc | игнорируются | alt-text через VLM |
| Таблицы из Excel | вручную | XLSX → Markdown-таблица |

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **MarkItDown + OCR Guide (R13)** | MarkItDown (структура) + Qwen3 VL (распознавание сложных элементов) = полный doc pipeline |
| **MarkItDown + research-docs LiteParse (R01)** | LiteParse структурирует → MarkItDown конвертирует = двойной ingestion layer |
| **MarkItDown + Paper2Agent (R08)** | PDF научной статьи → MarkItDown → Paper2Agent → 22 MCP инструмента |
| **MarkItDown + improve_chunk_semantic** | Стандартный RAG pipeline: PDF → Markdown → chunks → Qdrant |

## Контакт

- GitHub: https://github.com/microsoft/markitdown (MIT)
- pip install markitdown
- Habr упоминание: https://habr.com/ru/articles/890774/
- Ollama + LLaVA + MarkItDown гайд: Medium (Giacomo Carfì)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
