---
date: 2026-05-29
tags: [rag, orchestration, architecture, collaboration]
state: normalized
---

# OCR Guide — 6 open-source моделей для сложных документов

<!-- toc-auto -->
<!-- tags: ocr-6-models-guide, docs -->


<!-- summary -->
> Автор: независимый инженер (Хабр) Хабр: https://habr.com/ru/articles/966846/ GitHub: модели: PaddleOCR, Surya, EasyOCR, Tesseract, DocTR, Qwen3 VL
Хабр: https://habr.com/ru/articles/966846/  
GitHub: модели: PaddleOCR, Surya, EasyOCR, Tesseract, DocTR, Qwen3 VL  
Слой: ingestion / document-AI / ocr  
Дата: ноябрь 2025  
Уникальность: Честное сравнение 6 open-


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый инженер (Хабр)  
**Хабр:** https://habr.com/ru/articles/966846/  
**GitHub:** модели: PaddleOCR, Surya, EasyOCR, Tesseract, DocTR, Qwen3 VL  
**Слой:** ingestion / document-AI / ocr  
**Дата:** ноябрь 2025  
**Уникальность:** Честное сравнение 6 open-source OCR на «кошмаре инженера» — документ со сложной вёрсткой, таблицами, рукописным текстом. Включает современные VLM-модели (Qwen3 VL 30B). Вывод: VLM побеждают на сложных случаях, классические OCR — на скорости.

## Сравнение 6 моделей

| Модель | Тип | Сложные таблицы | Рукопись | Скорость | Лицензия |
|--------|-----|-----------------|----------|----------|---------|
| **Qwen3 VL 30B A3B** | VLM | ★★★★★ | ★★★★★ | медленно | Apache 2.0 |
| **PaddleOCR VL** | VLM-OCR | ★★★★ | ★★★ | средне | Apache 2.0 |
| **Surya** | neural OCR | ★★★★ | ★★ | средне | GPL-3.0 |
| **EasyOCR** | neural OCR | ★★★ | ★★ | быстро | Apache 2.0 |
| **DocTR** | neural OCR | ★★★ | ★★ | быстро | Apache 2.0 |
| **Tesseract** | классика | ★★ | ★ | очень быстро | Apache 2.0 |

### Рекомендации из статьи

- **Для качества** (сложные таблицы, рукопись): **Qwen3 VL** — лучший на всех тестах
- **Для скорости** (простые печатные документы): **LightOnOCR / PaddleOCR VL**
- **Для батч-обработки**: классический pipeline (Tesseract/DocTR) + VLM на проверке

## Архитектура гибридного pipeline

```
Документ (PDF / скан)
        ↓
Классический OCR (быстро, дёшево) → черновик
        ↓
VLM-верификатор (только для сложных случаев)
        ↓
Финальный структурированный текст (Markdown / HTML)
```

Этот гибрид использует и ContentAI (R12 нашла похожий подход).

## Связь с Lorenzo

Lorenzo использует:
- `improve_llm_enrich.py` — LLM-обогащение документов (текст уже готов)
- `improve_chunk_semantic.py` — чанки для RAG (из Markdown)
- **Нет OCR** — Lorenzo работает с готовым текстом

Где нужен OCR: ingestion внешних PDF-статей с Хабра (скачать → распознать → добавить в corpus).  
Паттерн: Surya (быстро) → если таблицы → Qwen3 VL → Markdown → `improve_index_update.py`.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **OCR + research-docs (R01)** | LiteParse (R01) + OCR = ingestion PDF → structured text → Lorenzo corpus |
| **OCR + Paper2Agent (R08)** | Paper2Agent конвертирует PDF статей через OCR → 22 MCP инструмента |
| **OCR + improve_chunk_semantic** | OCR → чанки → RAG pipeline для внешних документов |
| **Qwen3 VL + Vector DB (R12)** | VLM-распознавание → векторизация → Qdrant = мультимодальный поиск |

## Контакт

- Статья: https://habr.com/ru/articles/966846/ (ноябрь 2025)
- PaddleOCR GitHub: https://github.com/PaddlePaddle/PaddleOCR
- Surya GitHub: https://github.com/VikParuchuri/surya
- Qwen3 VL: через HuggingFace (Qwen/Qwen3-VL-30B-A3B)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
