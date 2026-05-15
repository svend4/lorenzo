---
date: 2026-05-15
tags: [memory, rag, security, knowledge, ingestion]
state: normalized
---

# MWS Vision Bench: первый русскоязычный бенчмарк для бизнес-OCR с VLM

<!-- toc-auto -->
<!-- tags: mts-ai-mws-vision-bench-business-ocr-vlm, docs -->


<!-- summary -->
> `mts-ai-mws-vision-bench-business-ocr-vlm` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** eCaesar (Георгий Гайков, MTS AI)  
**Хабр:** https://habr.com/ru/companies/mts_ai/articles/953292/  
**GitHub:** есть (инструменты оценки + HuggingFace датасет)  
**Слой:** analytics  
**Дата:** октябрь 2025  
**Уникальность:** Первый русскоязычный production-бенчмарк для бизнес-OCR с Vision-Language Models: 800 изображений документов, 2580 QA-пар, 5 типов задач (full-page OCR, image-to-markdown, text grounding, KIE, VQA) с разными метриками на каждую. Ключевые находки: задачи грандинга (локализация координат текста) остаются сложнейшими для всех VLM; летние модели 2025 года показали регресс vision-качества несмотря на рост LM-части — vision encoder завис на ~500M параметров.

## Проблема: нет русскоязычного OCR-бенчмарка для бизнес-документов

```
Текущее состояние VLM-OCR оценки:
  → DocVQA, ChartQA, InfoVQA: англоязычные
  → Русскоязычные документы: специфика кириллицы + деловой формат
  → Производственные документы: сканы, таблицы, схемы, рукопись
  → Нет benchmark для сравнения GPT-4 vs Gemini vs Qwen на RU-бизнес-документах

Что нужно:
  → Структурированный воспроизводимый бенчмарк
  → Несколько задач: OCR, структурирование, локализация, извлечение данных
  → Разные типы документов: офисные, рукописи, смешанные
  → Публичный датасет + закрытый тест (без leakage)
```

## Архитектура бенчмарка

```python
# MTS AI: MWS Vision Bench
# habr.com/ru/companies/mts_ai/articles/953292

from dataclasses import dataclass
from typing import Literal
from pathlib import Path

@dataclass
class BenchmarkDocument:
    """Один документ в бенчмарке MWS Vision Bench."""
    image_path: Path
    doc_type: Literal[
        "scanned_office",     # отсканированные офисные документы
        "diagram",            # схемы и диаграммы
        "table",              # таблицы (финансовые, отчёты)
        "schematic",          # технические чертежи
        "handwritten",        # рукописные заметки
        "mixed"               # смешанный тип
    ]
    language: str = "ru"      # преимущественно русский


BENCHMARK_STATS = {
    "total_images": 800,
    "qa_pairs": 2580,
    "split": {
        "validation": 1302,   # публичная часть
        "test": 1278          # закрытая (нет leakage)
    },
    "doc_types": [
        "scanned_office", "diagrams", "tables",
        "schematics", "handwritten", "mixed"
    ]
}


class MWSVisionBench:
    """
    5 типов задач с разными метриками.
    Каждый тип задачи требует разной способности модели.
    """

    TASK_TYPES = {
        "full_page_ocr": {
            "description": "Распознать весь текст на странице",
            "metric": "CER (Character Error Rate)",
            "difficulty": "medium",
            "current_best": "Gemini-2.5-Pro",
            "current_best_score": 0.682
        },

        "image_to_markdown": {
            "description": "Конвертировать документ в структурированный Markdown",
            "metric": "TEDS (Tree Edit Distance-based Similarity)",
            "difficulty": "hard",
            "challenge": "Таблицы: сохранить структуру строк/столбцов"
        },

        "text_grounding": {
            "description": "Локализовать текст: вернуть bounding box координаты",
            "metric": "IoU (Intersection over Union)",
            "difficulty": "very_hard",
            "key_finding": "Большинство моделей < IoU 25%; Anthropic-модели — выбросы вверх"
        },

        "key_information_extraction": {
            "description": "Извлечь структурированные данные → JSON по схеме",
            "metric": "Precision / Recall / F1 на JSON-полях",
            "difficulty": "hard",
            "use_case": "Накладные, договоры, акты — автоматическое заполнение форм"
        },

        "vqa": {
            "description": "Визуальные вопросы о содержании документа",
            "metric": "Exact match / partial match",
            "difficulty": "medium"
        }
    }

    def evaluate_model(self, model_name: str,
                        doc: BenchmarkDocument,
                        task: str) -> dict:
        """
        Запустить модель на документе по заданной задаче.
        Универсальный интерфейс для всех 5 типов задач.
        """
        prompt = self._build_task_prompt(task, doc)
        response = self._call_model(model_name, doc.image_path, prompt)
        score = self._compute_metric(task, response, self._get_gt(doc, task))

        return {
            "model": model_name,
            "task": task,
            "doc_type": doc.doc_type,
            "score": score,
            "response": response
        }
```

## Результаты бенчмарка (октябрь 2025)

```python
LEADERBOARD = {
    "метрика": "Средний балл по всем 5 задачам (нормализованный 0-1)",
    "дата": "Октябрь 2025",

    "результаты": [
        {"model": "Gemini-2.5-Pro",       "score": 0.682, "tier": "S"},
        {"model": "Gemini-2.5-Flash",     "score": 0.644, "tier": "A"},
        {"model": "GPT-4.1-mini",         "score": 0.643, "tier": "A"},
        {"model": "Claude-4.5-Sonnet",    "score": 0.639, "tier": "A"},
        {"model": "Cotype VL 32B",        "score": 0.639, "tier": "A"},
        {"model": "Qwen2.5-VL-7B",        "score": 0.601, "tier": "B"},
        {"model": "Qwen2.5-VL-72B",       "score": 0.618, "tier": "B"},
    ],

    "ключевые_выводы": {
        "grounding_провал": (
            "Задача text_grounding: большинство моделей < IoU 0.25. "
            "Модели не умеют точно указывать координаты текста на документе."
        ),
        "anthropic_выброс": (
            "Claude-семейство показывает аномально высокий IoU на grounding "
            "по сравнению со средним по рынку."
        ),
        "vision_регресс_2025": (
            "Модели лето 2025: рост LM-параметров, но регресс vision-качества. "
            "Vision encoder завис на ~500M параметров — узкое место архитектуры."
        ),
        "таблицы_сложнее_текста": (
            "image-to-markdown TEDS на таблицах << OCR на сплошном тексте. "
            "Структура строк/столбцов — сложнейшее для всех VLM."
        )
    }
}


VISION_STAGNATION_ANALYSIS = {
    "факт": "Летние 2025 VLM модели показали снижение vision-качества",
    "причина_гипотеза": (
        "LM-часть масштабируется (Qwen 7B → 72B), "
        "но vision encoder остаётся ~500M параметров (ViT-Large/H). "
        "Bottleneck — не LM, а vision encoder."
    ),
    "следствие": (
        "Больше параметров в LM не улучшает OCR/grounding. "
        "Нужно масштабировать vision encoder отдельно."
    ),
    "рекомендация": (
        "Для бизнес-OCR: выбирать по vision-специфичным метрикам, "
        "не по общим LLM бенчмаркам (MMLU, HumanEval)."
    )
}
```

## Техническая инфраструктура бенчмарка

```python
BENCHMARK_INFRASTRUCTURE = {
    "датасет": {
        "публичная_часть": "HuggingFace Dataset (validation 1302 пар)",
        "закрытая_часть": "Private test (1278 пар) — доступ по email",
        "формат": "image + question + answer + task_type"
    },

    "инструменты": {
        "evaluation_code": "GitHub (MTS AI)",
        "метрики_реализация": [
            "CER (difflib + editdistance)",
            "TEDS (tree edit distance для HTML-таблиц)",
            "IoU (polygon intersection для grounding)",
            "F1 для JSON extraction (field-level)"
        ]
    },

    "промпт_стратегии": {
        "zero_shot": "Базовая оценка без примеров",
        "few_shot": "3-5 примеров в промпте",
        "json_schema": "Явная схема для KIE задач"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: MWS Vision Bench паттерн для оценки docs/ извлечения

class LorenzoDocumentExtractionBench:
    """
    MWS паттерн для Lorenzo:
    Вместо бизнес-документов → оценка качества извлечения из docs/.
    5 типов задач → 5 метрик качества для RAG-системы Lorenzo.
    """

    LORENZO_TASK_MAPPING = {
        "full_page_ocr": "Полное считывание markdown-файла (baseline)",
        "image_to_markdown": "Конвертация PDF-проектных материалов",
        "text_grounding": "Точная локализация цитаты в источнике",
        "key_information_extraction": "Извлечение карточки проекта из статьи",
        "vqa": "Q&A по базе знаний (improve_llm_qa.py)"
    }

    def benchmark_retrieval_quality(self, query: str) -> dict:
        """
        Оценить качество поиска по аналогии с MWS Vision Bench:
        не один агрегированный скор, а профиль по задачам.
        """
        return {
            "precision_at_5": self._eval_kie(query),      # точность карточек
            "recall_at_5": self._eval_ocr(query),          # полнота текста
            "grounding_score": self._eval_grounding(query) # точность цитат
        }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **MWS Vision Bench + LoRA Embeddings (R44)** | LoRA-дообученные vision embeddings → специализация на RU бизнес-документах |
| **MWS Vision Bench + RAG чанкинг (R43)** | Hybrid chunking для мультимодальных документов + TEDS метрика оценки |
| **MWS Vision Bench + Yandex LLM Eval (R44)** | Style-bias-free оценка VLM: явные рубрики для OCR/KIE вместо общего скора |
| **MWS Vision Bench + Privacy Gateway (R41)** | OCR из документов + PII-фильтр перед отправкой в облачный VLM |
| **MWS Vision Bench + LangGraph (R44)** | Multi-step документный pipeline с чекпоинтами: OCR → KIE → валидация |

## Контакт

- Статья: https://habr.com/ru/companies/mts_ai/articles/953292/ (октябрь 2025)
- Автор: eCaesar (Георгий Гайков, MTS AI)
- MTS AI: mts.ai
- HuggingFace датасет: huggingface.co/MTS-AI (MWS Vision Bench)
- Смежная (VLM vs IDP бенчмарк ContentAI, R30): docs/06-discovery/round-30/
- Смежная (Авито VLM, R32): docs/06-discovery/round-32/
- Смежная (Docling мультимодальный RAG, R19): docs/06-discovery/round-19/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
