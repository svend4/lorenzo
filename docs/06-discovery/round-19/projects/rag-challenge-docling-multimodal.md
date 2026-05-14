# RAG Challenge победитель — Docling + multimodal pipeline для PDF с таблицами

**Автор:** независимый разработчик (Хабр, март 2025)  
**Хабр:** https://habr.com/ru/articles/893356/  
**GitHub:** не опубликован (конкурсный проект, но все техники описаны)  
**Слой:** ingestion / knowledge / orchestration  
**Дата:** март 2025  
**Уникальность:** Победа в двух категориях RAG-конкурса на реальной задаче: 100 корпоративных annual reports (PDF, до 1000 страниц) → вопрос-ответ. Ключевое открытие: **Docling для таблиц** — конвертирует PDF-таблицы в Markdown/HTML с сохранением структуры. Простые техники (если правильно настроены) бьют сложные.

## Задача конкурса

```
Дано: 100 annual reports (PDF, до 1000 страниц каждый)
Время на подготовку: 2.5 часа
Задача: ответить на 100 вопросов по данным из отчётов
  Пример: "Какой ROE у компании X за 2023 год?"
  Ответ должен быть точным числом из таблицы в PDF
```

Сложность: таблицы с финансовыми данными, многостраничные, вложенные, в скане.

## Основные техники победителя

### 1. Docling для извлечения таблиц

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("annual_report.pdf")

# Docling понимает таблицы и конвертирует в структурированный Markdown
for table in result.document.tables:
    md_table = table.export_to_markdown()
    # Результат: | Показатель | 2023 | 2022 |
    #            |------------|------|------|
    #            | ROE        | 18%  | 15%  |
```

**Результат**: LLM корректно читает таблицы из Markdown — без галлюцинаций цифр.

### 2. JSON-метаданные для контекста

```python
# Модифицированный метод Docling для генерации JSON с метаданными
doc_json = {
    "source": "annual_report_2023.pdf",
    "page": 45,
    "section": "Financial Highlights",
    "content_type": "table",
    "markdown": md_table,
    "html": html_table  # альтернативное представление
}
```

Dual-format (MD + HTML) позволяет LLM выбрать удобное представление.

### 3. Прецизионный чанкинг

```
Наивный чанкинг: режем по N символов → разрезаем таблицу пополам
        ↓
Семантический чанкинг по секциям:
  → каждый раздел отчёта = отдельный чанк
  → таблица никогда не разрезается
  → заголовок раздела дублируется в каждый чанк (контекст)
```

### 4. Ensemble retrieval

```python
# Не один ретривер, а ансамбль
results_bm25 = bm25.search(query, top_k=10)
results_dense = dense.search(query, top_k=10)
results_hybrid = rrf_merge(results_bm25, results_dense)  # RRF fusion
# RRF = Reciprocal Rank Fusion: 1/(k + rank_i) суммируется
```

## Архитектура pipeline

```
PDF (100 отчётов, 1000 стр каждый)
        ↓
Docling: layout analysis + table extraction
  → Markdown с таблицами + JSON с метаданными
        ↓
Semantic chunking по секциям (без разрезания таблиц)
        ↓
Dual index: BM25 + dense embeddings
        ↓
Ensemble retrieval (RRF fusion)
        ↓
LLM: извлечение точного числа из таблицы
        ↓
Проверка формата ответа (число / процент / валюта)
```

## Почему Docling лучше PyMuPDF / pdfminer

| Инструмент | Таблицы | Разметка | Скорость | Когда |
|-----------|---------|---------|----------|-------|
| PyMuPDF | потеря структуры | нет | быстрый | простые тексты |
| pdfminer | плохо | нет | медленный | legacy |
| **Docling** | **сохраняет структуру** | **MD + HTML** | средний | **RAG с таблицами** |
| LlamaParse | хорошо | MD | медленный (API) | cloud |

Docling — Apache 2.0, работает локально, IBM open source.

## Ключевой вывод

> «Магия RAG скрыта в деталях: чем лучше понимаешь задачу, тем точнее настраиваешь каждую часть пайплайна — и даже простые техники дают SoTA.»

Не сложность → точность. Правильная декомпозиция → точность.

## Применение к Lorenzo

Lorenzo парсит документы через `improve_chunk_semantic.py` (текст).  
Docling даёт следующий уровень:
- PDF с таблицами (отчёты, спецификации) → правильный Markdown
- Структурированные чанки с метаданными страниц
- Связь с MarkItDown (R14): MarkItDown = общий конвертер, Docling = специалист по таблицам

Для `improve_llm_qa.py`: если документ-источник — PDF с таблицами → Docling preprocessor.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Docling + MarkItDown (R14)** | MarkItDown = общий конвертер, Docling = специалист по PDF-таблицам |
| **Docling + Agentic RAG (R18)** | Агент решает: нужен ли Docling для этого документа (PDF vs TXT) |
| **Docling + FRIDA (R18)** | FRIDA embeddings для Docling-чанков с таблицами на русском |
| **Docling + Vector DB (R19)** | Docling-чанки → Qdrant с payload filter по content_type=table |
| **Docling + LLM DBA (R17)** | Schema Extractor + Docling = RAG по PDF с описаниями схем БД |

## Контакт

- Статья: https://habr.com/ru/articles/893356/ (март 2025)
- Docling GitHub: https://github.com/DS4SD/docling (Apache 2.0, IBM)
- Docling PyPI: pip install docling
- Смежная (PDF hardcore): https://habr.com/ru/articles/996144/
- Смежная (Hybrid RAG + Docling + Qwen2.5-VL): https://habr.com/ru/articles/1024696/
