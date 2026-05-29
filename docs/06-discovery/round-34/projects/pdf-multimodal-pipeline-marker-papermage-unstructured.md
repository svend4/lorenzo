---
date: 2026-05-29
tags: [memory, rag, knowledge, ingestion, architecture]
state: normalized
---

# Демистифицируем парсинг PDF: конвейерная обработка с LayoutLMv3, Table Transformer, YOLOX

<!-- toc-auto -->
<!-- tags: pdf-multimodal-pipeline-marker-papermage-unstructured, docs -->


<!-- summary -->
> `pdf-multimodal-pipeline-marker-papermage-unstructured` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** MaxRokatansky (OTUS)  
**Хабр:** https://habr.com/ru/companies/otus/articles/835930/  
**GitHub:** https://github.com/VikParuchuri/marker (Marker), https://github.com/allenai/papermage (PaperMage), https://github.com/Unstructured-IO/unstructured (Unstructured)  
**Слой:** ingestion  
**Дата:** август 2024  
**Уникальность:** Единственная русскоязычная статья с практическим сравнением трёх production PDF pipeline с разными моделями: Marker (LayoutLMv3 + Texify для формул), Unstructured (Table Transformer DETR на PubTables-1M), PaperMage (YOLOX + IVILA token classification). Прямое сравнение CNN/transformer подходов на смешанных документах (колонки, таблицы без границ, формулы).

## Три архитектуры парсинга: разные модели под одну задачу

```
Задача: структурированное извлечение из PDF
  → текст (включая многоколончатый)
  → таблицы (с границами и без)
  → математические формулы (LaTeX)
  → порядок чтения (reading order)

Pipeline 1: Marker (VikParuchuri)
  → LayoutLMv3 fine-tuned → блоки (текст/таблица/формула/заголовок)
  → Texify (Donut-архитектура) → формулы → LaTeX
  → Output: Markdown с LaTeX-блоками

Pipeline 2: Unstructured (unstructured.io)
  → Table Transformer (DETR + ResNet) → структура таблицы
  → Обучен на PubTables-1M (900K таблиц из научных статей)
  → Output: HTML таблицы + chunk элементы

Pipeline 3: PaperMage (AllenAI)
  → YOLOX → bounding boxes блоков
  → IVILA token classification → логическая структура (section/caption/ref)
  → Output: layered Document объект
```

## Marker: LayoutLMv3 + Texify

```python
# Marker: github.com/VikParuchuri/marker
# Ключевое: два специализированных трансформера для разных элементов

from marker.convert import convert_single_pdf
from marker.models import load_all_models

# Загрузить все модели (LayoutLMv3 + Texify + OCR)
models = load_all_models()

def extract_with_marker(pdf_path: str) -> dict:
    """
    Marker внутри:
    1. Nougat/Surya OCR → текст с позициями
    2. LayoutLMv3 (fine-tuned на DocLayNet) → классификация блоков:
       Text | Title | List | Table | Figure | Caption | Formula
    3. Texify (Donut seq2seq) → формулы → LaTeX
    4. Heuristics → порядок чтения в многоколончатом документе
    """
    full_text, images, out_meta = convert_single_pdf(
        pdf_path,
        models,
        max_pages=None,
        langs=["ru", "en"],   # поддержка русского языка
        batch_multiplier=2    # GPU batch size
    )

    return {
        "text": full_text,       # Markdown с LaTeX для формул
        "meta": out_meta,        # статистика блоков
        "images": images         # извлечённые изображения
    }

# Пример output для документа с формулой:
# "## Теорема Байеса\n\nP(A|B) = $$\\frac{P(B|A) \\cdot P(A)}{P(B)}$$\n\n"

# LayoutLMv3 architecture:
class LayoutLMv3ForBlockClassification:
    """
    Input: токены текста + bounding box координаты + patch изображения
    Output: класс каждого блока (Text/Table/Formula/...)

    Ключевое: multimodal — объединяет text tokens + visual patches
    Fine-tuned на DocLayNet (80K страниц, 11 классов)
    """
    def forward(self, input_ids, bbox, pixel_values):
        # text embeddings + 2D positional (x1,y1,x2,y2) + visual patches
        text_embeds = self.roberta(input_ids)
        layout_embeds = self.layout_embed(bbox)
        visual_embeds = self.patch_embed(pixel_values)
        # Fusion → transformer layers → per-token classification
        return self.classifier(text_embeds + layout_embeds + visual_embeds)
```

## Unstructured: Table Transformer (DETR)

```python
# Unstructured: github.com/Unstructured-IO/unstructured
# Ключевое: Table Transformer специализирован на структуре таблиц

from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Table, Text, Title

def extract_with_unstructured(pdf_path: str) -> dict:
    """
    Unstructured Table Transformer внутри:
    1. PDFMiner → layout объекты
    2. DETR + ResNet (Table Transformer) → table detection + cell recognition
       Обучен на PubTables-1M: 900K таблиц из научных статей
    3. OCR (tesseract/paddle) → текст ячеек
    4. Chunking по смысловым блокам
    """
    elements = partition_pdf(
        filename=pdf_path,
        extract_images_in_pdf=True,
        infer_table_structure=True,    # Table Transformer включён
        strategy="hi_res",             # используем detection модели
        languages=["rus", "eng"]
    )

    tables = []
    texts = []

    for el in elements:
        if isinstance(el, Table):
            tables.append({
                "html": el.metadata.text_as_html,   # структурированная таблица
                "text": el.text,
                "page": el.metadata.page_number
            })
        elif isinstance(el, (Text, Title)):
            texts.append({"text": el.text, "type": type(el).__name__})

    return {"tables": tables, "texts": texts}

# Table Transformer DETR architecture:
class TableTransformerDETR:
    """
    Detection TRansformer (DETR) для таблиц:
    1. ResNet backbone → feature map
    2. Transformer encoder-decoder
    3. Object queries → N предсказаний (table cells/rows/columns)
    4. Hungarian matching → финальные bounding boxes

    Две модели:
    - microsoft/table-transformer-detection → найти таблицу в документе
    - microsoft/table-transformer-structure-recognition → структура ячеек

    PubTables-1M: 900K таблиц из PubMed статей
    GriTS score: 0.966 (structure recognition)
    """
```

## PaperMage: YOLOX + IVILA

```python
# PaperMage: github.com/allenai/papermage
# Ключевое: layered document model с YOLOX детектором

from papermage import Document
from papermage.recipes import CoreRecipe

recipe = CoreRecipe()

def extract_with_papermage(pdf_path: str) -> dict:
    """
    PaperMage архитектура:
    1. pdfplumber → текст + позиции символов
    2. YOLOX (anchor-free detector) → figure/table/equation bounding boxes
       Pretrained COCO → fine-tuned на DocLayNet
    3. IVILA (Inter-sentence VIsual LAyout) → token classification:
       section/paragraph/caption/reference/footnote
    4. Sentence segmentation → reading order
    """
    doc = recipe.from_path(pdf_path)

    # Layered доступ к документу
    result = {
        "sections": [s.text for s in doc.sections],
        "paragraphs": [p.text for p in doc.paragraphs],
        "figures": [
            {
                "caption": fig.caption.text if fig.caption else None,
                "bbox": fig.boxes[0].coordinates
            }
            for fig in doc.figures
        ],
        "tables": [
            {
                "caption": tbl.caption.text if tbl.caption else None,
                "cells": [[cell.text for cell in row] for row in tbl.rows]
            }
            for tbl in doc.tables
        ],
        "equations": [eq.text for eq in doc.equations]
    }
    return result
```

## Сравнение pipeline: скорость vs качество

```python
PIPELINE_COMPARISON = {
    "задача": "100-страничный PDF с текстом, 20 таблицами, 15 формулами",

    "Marker": {
        "время": "~45 сек (GPU) / ~3 мин (CPU)",
        "таблицы": "конвертирует в Markdown таблицы (теряет сложную структуру)",
        "формулы": "★★★★★ — Texify даёт точный LaTeX",
        "многоколончатый": "★★★★ — LayoutLMv3 справляется хорошо",
        "русский": "★★★ — нужен tesseract с rus+eng",
        "output": "Markdown (удобно для RAG)",
        "лучше_для": "научные статьи, документы с формулами"
    },
    "Unstructured": {
        "время": "~2 мин (CPU, hi_res)",
        "таблицы": "★★★★★ — Table Transformer лучший для структуры",
        "формулы": "★★ — нет специальной модели, берёт как текст",
        "многоколончатый": "★★★ — хуже чем Marker",
        "русский": "★★★★ — хорошая поддержка",
        "output": "List[Element] (гибко)",
        "лучше_для": "корпоративные документы с таблицами"
    },
    "PaperMage": {
        "время": "~1 мин (GPU)",
        "таблицы": "★★★ — структура базовая",
        "формулы": "★★★ — извлекает как текст",
        "многоколончатый": "★★★★ — IVILA хорошо с логической структурой",
        "русский": "★★ — обучен на английских статьях",
        "output": "Document объект (удобно для структурного анализа)",
        "лучше_для": "научные статьи с complex layout"
    }
}

# Выводы статьи:
# → Нет универсального победителя
# → Marker: лучший Markdown output для RAG
# → Unstructured: лучший для таблиц в enterprise docs
# → PaperMage: лучший для structure-aware pipeline
```

## Применение к Lorenzo

```python
# improve_pdf_multimodal.py (паттерн):

class LorenzoPDFIngestion:
    """
    Lorenzo собирает документы с Хабр.
    Паттерн Marker/Unstructured для ingestion PDF-отчётов
    (технические статьи, корпоративные доки) в базу знаний.
    """

    def ingest_pdf(self, pdf_path: str,
                   doc_type: str = "article") -> list[dict]:
        if doc_type == "scientific":
            # Научная статья: Marker для точных формул и ссылок
            return self._ingest_with_marker(pdf_path)
        elif doc_type == "corporate":
            # Корпоративный отчёт: Unstructured для таблиц
            return self._ingest_with_unstructured(pdf_path)
        else:
            # Общий случай: Marker (лучший Markdown)
            return self._ingest_with_marker(pdf_path)

    def _chunk_for_rag(self, text: str, source: str) -> list[dict]:
        """Разбить Markdown на чанки для RAG."""
        # Разбивка по заголовкам → чанки ~500 токенов
        sections = text.split("\n## ")
        return [
            {"text": s[:2000], "source": source, "section": s[:80]}
            for s in sections if len(s) > 100
        ]
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **PDF Multimodal + FinPDF pipeline (R32)** | Marker/Unstructured вместо fitz для финансовых отчётов — точные таблицы в LLM анализе |
| **PDF Multimodal + Enterprise RAG (R32)** | Table Transformer → структурированные таблицы в корпоративном RAG МТС |
| **PDF Multimodal + DQ LLM (R33)** | Извлечённые таблицы → автоматическая генерация DQ правил для данных |
| **PDF Multimodal + Avito VLM (R32)** | VLM pipeline вместо LayoutLMv3 для документов с изображениями |
| **PDF Multimodal + Cognitive Memory (R31)** | Формулы и таблицы → semantic memory nodes с типом PROCEDURAL |

## Контакт

- Статья: https://habr.com/ru/companies/otus/articles/835930/ (август 2024)
- OTUS: otus.ru (образовательная платформа)
- Marker (Vik Paruchuri): github.com/VikParuchuri/marker
- PaperMage (AllenAI): github.com/allenai/papermage
- Unstructured: github.com/Unstructured-IO/unstructured
- Table Transformer: huggingface.co/microsoft/table-transformer-detection
- Смежная (OCR до ADE, LayoutLM + LandingAI): https://habr.com/ru/articles/1008610/
- DocLayNet dataset: github.com/DS4SD/DocLayNet

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
