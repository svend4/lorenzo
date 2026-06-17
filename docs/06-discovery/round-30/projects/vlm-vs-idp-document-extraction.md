---
date: 2026-06-05
tags: [rag, ingestion, local-first, architecture, self-improve]
state: normalized
---

# VLM vs IDP: кто выигрывает в извлечении данных из российских финансовых документов

<!-- toc-auto -->
<!-- tags: vlm-vs-idp-document-extraction, docs -->


<!-- summary -->
> Автор: ContentAI Team (Хабр, октябрь 2025) Хабр: https://habr.com/ru/companies/contentai/articles/958768/
Хабр: https://habr.com/ru/companies/contentai/articles/958768/  
GitHub: не опубликован (внутренние бенчмарки ContentAI)  
Слой: ingestion / analytics  
Дата: октябрь 2025  
Уникальность: Честный бенчмарк


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** ContentAI Team (Хабр, октябрь 2025)  
**Хабр:** https://habr.com/ru/companies/contentai/articles/958768/  
**GitHub:** не опубликован (внутренние бенчмарки ContentAI)  
**Слой:** ingestion / analytics  
**Дата:** октябрь 2025  
**Уникальность:** Честный бенчмарк VLM vs классической IDP-платформы ContentCapture на 764 синтетических российских финансовых документах (счета, УПД, накладные, 6 типов). Метрики: PassThroughRate, FieldF1, CharF1. Вывод: гибрид IDP+VLM — не замена, а дополнение. Быстрое структурное извлечение OCR + контекстная LLM-постобработка.

## Контекст: почему это важно для России

```
Российский финансовый документооборот:
  → Счёт-фактура (НДС)
  → Универсальный передаточный документ (УПД)
  → ТОРГ-12 (накладная)
  → Акт выполненных работ
  → КС-2, КС-3 (строительство)
  
Особенности RU документов:
  → ФИО в разных падежах
  → ОГРН/ИНН/КПП — специфические поля
  → Рукописные подписи и печати
  → Сканы плохого качества (70-80% реальных документов)
  → Нестандартные шаблоны у каждой компании

Масштаб:
  → Крупные компании: 10K+ документов в день
  → Требование: <3 сек/документ, >95% точность полей
```

## Методология бенчмарка

```python
BENCHMARK_CONFIG = {
    "dataset": {
        "total_documents": 764,
        "synthetic": True,  # сгенерированы для воспроизводимости
        "document_types": {
            "invoice":          127,  # счёт-фактура
            "upd":              148,  # УПД
            "torg12":           121,  # накладная
            "act":              118,  # акт
            "ks2":              124,  # КС-2
            "payment_order":    126   # платёжное поручение
        },
        "quality_distribution": {
            "clean_scan": 0.35,
            "medium_quality": 0.40,
            "low_quality": 0.25   # имитация плохих сканов
        }
    },

    "metrics": {
        "PassThroughRate": "% документов успешно обработанных без ошибок",
        "FieldF1": "F1-мера по каждому полю (точность + полнота)",
        "CharF1": "F1-мера на уровне символов (критично для ИНН/ОГРН)"
    },

    "systems_compared": [
        "ContentCapture IDP",      # классическая IDP-платформа
        "GPT-4o (vision)",         # VLM облако
        "Claude Sonnet 4.5 (vision)", # VLM облако
        "Qwen2.5-VL-72B",         # open-source VLM
        "IDP + GPT-4o hybrid"     # гибридный подход
    ]
}
```

## Результаты бенчмарка

```python
BENCHMARK_RESULTS = {
    "ContentCapture IDP": {
        "PassThroughRate": 0.92,
        "FieldF1": {
            "avg": 0.94,
            "structured_fields": 0.97,  # ИНН, ОГРН, суммы
            "free_text": 0.87           # наименования товаров
        },
        "CharF1": 0.96,
        "speed_sec_per_doc": 0.8,
        "cost_per_1000_docs": "$2.40",  # on-premise
        "weakness": "Плохо с нестандартными шаблонами (-15% FieldF1)"
    },

    "GPT-4o (vision)": {
        "PassThroughRate": 0.78,
        "FieldF1": {
            "avg": 0.81,
            "structured_fields": 0.76,  # путает ИНН/ОГРН/КПП
            "free_text": 0.89           # хорошо понимает контекст
        },
        "CharF1": 0.73,  # галлюцинации в числах!
        "speed_sec_per_doc": 3.2,
        "cost_per_1000_docs": "$45",
        "weakness": "Галлюцинирует цифры (ИНН, суммы, даты)"
    },

    "Qwen2.5-VL-72B": {
        "PassThroughRate": 0.83,
        "FieldF1": {"avg": 0.85, "structured_fields": 0.82},
        "CharF1": 0.79,
        "speed_sec_per_doc": 4.1,  # self-hosted
        "cost_per_1000_docs": "$8",  # GPU сервер
        "note": "Лучший open-source VLM для RU документов"
    },

    "IDP + GPT-4o hybrid": {  # ПОБЕДИТЕЛЬ
        "PassThroughRate": 0.96,
        "FieldF1": {
            "avg": 0.95,
            "structured_fields": 0.97,  # IDP извлекает
            "free_text": 0.94           # GPT-4o постобрабатывает
        },
        "CharF1": 0.97,
        "speed_sec_per_doc": 1.4,
        "cost_per_1000_docs": "$8.50",
        "strength": "Лучшее из двух миров"
    }
}
```

## Гибридная архитектура: IDP + VLM

```python
# Ключевой вывод: не заменять, а комбинировать

class HybridDocumentProcessor:
    """
    Stage 1: IDP для структурного извлечения (быстро, точно для шаблонных полей)
    Stage 2: VLM для контекстного обогащения (понимает нестандартное)
    """

    def process(self, document: Document) -> ExtractedData:
        # Шаг 1: OCR + структурное извлечение через IDP
        idp_result = self.idp.extract(document)
        # → Быстро (0.5-1 сек)
        # → Высокая точность для стандартных полей (ИНН, суммы, даты)
        # → Ошибается на нестандартных шаблонах

        # Шаг 2: Определить "трудные" поля
        uncertain_fields = [
            field for field in idp_result.fields
            if field.confidence < 0.85 or field.is_ambiguous
        ]

        if not uncertain_fields:
            return idp_result  # IDP справился сам

        # Шаг 3: VLM для неуверенных полей
        # Отправляем только изображение + перечень проблемных мест
        vlm_result = self.vlm.clarify(
            image=document.image,
            prompt=self.build_clarification_prompt(uncertain_fields),
            focus_regions=self.get_bounding_boxes(uncertain_fields)
        )

        # Шаг 4: Смерджить
        return self.merge(
            idp_result=idp_result,
            vlm_corrections=vlm_result,
            strategy="vlm_wins_on_uncertainty"
        )

    def build_clarification_prompt(self, fields: list[Field]) -> str:
        return f"""
        IDP система не уверена в следующих полях:
        {[f"{f.name}: '{f.value}' (уверенность {f.confidence:.0%})" for f in fields]}
        
        Пожалуйста, найди правильные значения на изображении.
        Для числовых полей (ИНН, суммы): возвращай ТОЛЬКО цифры.
        Формат ответа: {{"field_name": "correct_value", ...}}
        """
```

## Когда использовать что

```python
DECISION_MATRIX = {
    "IDP only": {
        "когда": [
            "Стандартные шаблоны документов (>90% вашего потока)",
            "Требование < 1 сек/документ",
            "Большой объём (>10K/день)",
            "Строгие требования к данным (ИНН/ОГРН/суммы)"
        ],
        "не когда": [
            "Документы произвольного формата",
            "Нужно понять контекст (не только поля)"
        ]
    },
    "VLM only": {
        "когда": [
            "Нестандартные документы",
            "Малый объём (<500/день)",
            "Нужно 'понять' документ, не только извлечь"
        ],
        "не когда": [
            "Числовые поля критичны (галлюцинирует!)",
            "Нужна скорость < 3 сек/документ"
        ]
    },
    "Hybrid IDP+VLM": {
        "когда": [
            "Смешанный поток: 70% стандартные + 30% нестандартные",
            "Высокие требования по точности И скорости",
            "Приемлемая стоимость $5-15/1000 документов"
        ],
        "рекомендация": "Оптимум для большинства enterprise задач"
    }
}
```

## Применение к Lorenzo

Lorenzo обрабатывает документы (discovery files, Habr articles). IDP+VLM паттерн:

```python
# improve_doc_extractor.py (паттерн):

class LorenzoDocExtractor:
    """
    Гибридное извлечение структуры из неструктурированных файлов Хабра
    Stage 1: regex/BM25 → структурные поля (автор, дата, теги)
    Stage 2: LLM → для неясных/отсутствующих полей
    """

    def extract_project_metadata(self, habr_article: str) -> ProjectMetadata:
        # Stage 1: структурное (быстро, без LLM)
        structured = self.regex_extractor.extract({
            "github_url": r'github\.com/[\w-]+/[\w-]+',
            "habr_id": r'habr\.com/ru/\w+/articles/(\d+)',
            "date": r'(\d{1,2}\s+\w+\s+\d{4})',
            "author": r'\*\*Автор:\*\*\s+(.+?)(?:\n|$)'
        }, habr_article)

        # Определить что не нашли
        missing = [k for k, v in structured.items() if not v]

        # Stage 2: LLM только для пропущенных (экономим токены)
        if missing:
            llm_result = self.llm.extract(
                text=habr_article[:2000],
                fields=missing
            )
            structured.update(llm_result)

        return ProjectMetadata(**structured)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **IDP+VLM + Multimodal (R28)** | Multimodal VLM как Stage 2: видит документ как изображение |
| **IDP+VLM + Normcontrol (R25)** | IDP извлекает → нормоконтроль проверяет структуру |
| **IDP+VLM + Legal RAG (R25)** | Извлечь данные из договора → поиск по реестру норм |
| **IDP+VLM + CAVM (R26)** | CAVM пайплайн: документы → IDP+VLM → анализ → отчёт |
| **IDP+VLM + LLM Judge (R28)** | LLM Judge верифицирует извлечённые данные (нет галлюцинаций?) |

## Контакт

- Статья: https://habr.com/ru/companies/contentai/articles/958768/ (октябрь 2025)
- ContentAI: contentai.ru (IDP платформа ContentCapture)
- Смежная (МТС умная маршрутизация): https://habr.com/ru/companies/ru_mts/articles/1028974/
- Смежная (АСКОН NLP для ГОСТ): https://habr.com/ru/companies/ascon/articles/1031940/
- Qwen2.5-VL: github.com/QwenLM/Qwen2.5-VL (Apache 2.0)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
