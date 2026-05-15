# LLM Extraction из бухгалтерских документов: Qwen3-30B, F1=95.9% на счетах-фактурах

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Рег.облако + Raft (runity blog)  
**Хабр:** https://habr.com/ru/companies/runity/articles/987424/  
**GitHub:** нет (production эксперимент)  
**Слой:** ingestion / knowledge  
**Дата:** январь 2025  
**Уникальность:** Единственная на Хабре статья с production-метриками LLM extraction из реальных бухгалтерских документов (счета-фактуры, акты, договоры, допсоглашения): 200+ документов строительной отрасли, F1=95.9% vs 63% baseline, до 30 полей на документ. Qwen3-30B-A3B выбран над Qwen3-235B и Qwen3-32B после сравнения quality/speed/GPU tradeoffs. 5-этапный пайплайн с confidence scoring (70% threshold) + schema validation. Не RAFT/RAG — extraction пайплайн для прямого импорта в ERP/DWH.

## Проблема: извлечение полей из неструктурированных бухгалтерских документов

```
Строительная компания: тысячи документов месяц
  → Счета-фактуры от подрядчиков (разные форматы)
  → Акты выполненных работ (свободная форма)
  → Договоры (50-200 страниц)
  → Дополнительные соглашения (изменения к договорам)

Проблема ручного ввода:
  → Бухгалтер вручную вносит: дата, сумма, НДС, контрагент, реквизиты
  → 30+ полей на документ × тысячи документов = дни работы
  → Ошибки ручного ввода → проблемы с налоговой

Традиционный OCR + regex:
  → Regex хрупкий: каждый подрядчик форматирует по-своему
  → OCR теряет структуру таблиц
  → Baseline F1: 63%

LLM extraction:
  → Понимает контекст: "НДС 20%" = "tax_rate=0.20"
  → Работает со свободным текстом без шаблона
  → F1: 95.9% (Qwen3-30B-A3B-Instruct)
```

## 5-этапный пайплайн extraction

```python
# Рег.облако + Raft: LLM extraction из бухгалтерских документов
# habr.com/ru/companies/runity/articles/987424/

from dataclasses import dataclass, field
from typing import Literal, Optional, Any
from enum import Enum

DocumentType = Literal[
    "invoice",          # счёт-фактура
    "act",              # акт выполненных работ
    "contract",         # договор
    "supplement",       # дополнительное соглашение
    "payment_order"     # платёжное поручение
]

@dataclass
class ExtractedField:
    """Одно извлечённое поле из документа."""
    field_name: str
    value: Any
    confidence: float     # 0.0-1.0 (LLM self-reported)
    source_text: str      # фрагмент откуда извлечено (для проверки)
    validated: bool = False


@dataclass
class DocumentExtractionResult:
    """Результат обработки одного документа."""
    doc_type: DocumentType
    fields: list[ExtractedField]
    overall_confidence: float
    ready_for_erp: bool    # True если все обязательные поля извлечены


# Схемы полей по типу документа
INVOICE_SCHEMA = {
    "required": [
        "invoice_number",     # номер счёта-фактуры
        "invoice_date",       # дата
        "seller_inn",         # ИНН продавца
        "seller_name",        # название организации
        "buyer_inn",          # ИНН покупателя
        "total_amount",       # итоговая сумма
        "vat_amount",         # сумма НДС
        "vat_rate",           # ставка НДС
    ],
    "optional": [
        "line_items",         # позиции (список)
        "payment_terms",      # условия оплаты
        "contract_ref",       # ссылка на договор
        "kpp",                # КПП
        "bank_account",       # банковский счёт
    ]
}

ACT_SCHEMA = {
    "required": [
        "act_number",
        "act_date",
        "contractor_inn",
        "work_description",
        "total_amount",
        "period_from", "period_to"   # период выполнения работ
    ]
}


class DocumentClassifier:
    """
    Этап 1: Классификация типа документа.

    До LLM: определить тип документа по заголовку/структуре.
    Позволяет выбрать правильную схему для extraction.

    Методы:
    1. Keyword detection (быстро): "СЧЁТ-ФАКТУРА" → invoice
    2. LLM classification (для нестандартных форматов)
    """

    KEYWORDS = {
        "invoice": ["счёт-фактура", "с/ф", "ндс"],
        "act": ["акт выполненных работ", "акт приёмки", "акт оказанных услуг"],
        "contract": ["договор", "соглашение"],
        "supplement": ["дополнительное соглашение", "доп. соглашение", "допсоглашение"]
    }

    def classify(self, text: str) -> tuple[DocumentType, float]:
        """Классифицировать тип документа + уверенность."""
        text_lower = text[:500].lower()

        for doc_type, keywords in self.KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return doc_type, 0.95

        # Если keyword не нашёл → LLM classification
        return self._llm_classify(text[:1000])


class LLMExtractor:
    """
    Этап 3-4: LLM extraction с confidence scoring.

    Модель: Qwen3-30B-A3B-Instruct (выбрана из 4 кандидатов)

    Почему Qwen3-30B-A3B победил:
    Qwen3-235B: лучшее качество, но слишком дорого/медленно на A100 80GB
    Qwen3-32B: хорошее качество, но dense модель (больше VRAM)
    Qwen3-30B-A3B: Mixture-of-Experts (A3B = Active 3B params из 30B total)
      → Быстрее dense 32B (только 3B активных параметров)
      → Качество ≈ dense 30B
      → Помещается на A100 80GB
    Qwen3-7B: не хватало точности на сложных форматах

    Пайплайн запроса:
    Context (тип документа + схема) → chunk → extraction → confidence
    """

    MODEL = "Qwen3-30B-A3B-Instruct"  # MoE: 30B total, 3B active
    CONFIDENCE_THRESHOLD = 0.70       # ниже → требует человеческой проверки

    async def extract_fields(self,
                              text: str,
                              doc_type: DocumentType,
                              schema: dict) -> list[ExtractedField]:
        """
        Извлечь поля из документа по схеме с confidence scoring.
        """
        required_fields = schema["required"]
        optional_fields = schema.get("optional", [])

        prompt = f"""Извлеки следующие поля из бухгалтерского документа.
Тип документа: {doc_type}

Обязательные поля (извлечь обязательно): {required_fields}
Опциональные поля (извлечь если есть): {optional_fields}

Для каждого поля укажи:
1. Значение (точно как в документе)
2. Уверенность 0.0-1.0 (0.9+ = найдено явно, 0.5-0.9 = вывел из контекста, <0.5 = неточно)
3. Фрагмент текста источника

Документ:
{text}

Ответ в JSON:"""

        response = await self.llm.generate(
            prompt,
            response_format={"type": "json_object"},
            temperature=0.0  # детерминированность для extraction
        )

        return self._parse_extraction_response(response)

    def flag_low_confidence(self,
                             fields: list[ExtractedField]) -> list[ExtractedField]:
        """Пометить поля с confidence < threshold для проверки."""
        for field in fields:
            if field.confidence < self.CONFIDENCE_THRESHOLD:
                field.validated = False  # требует human review
        return fields


class SchemaValidator:
    """
    Этап 5: Валидация + дедупликация перед выгрузкой в ERP.

    После LLM extraction:
    1. Проверить форматы (ИНН = 10 или 12 цифр, дата = DD.MM.YYYY)
    2. Проверить суммы: total = sum(line_items) ± 1 коп
    3. Проверить логику: vat_amount = total * vat_rate
    4. Дедупликация: не загружать дважды один документ (по номеру+дате)
    """

    def validate_invoice(self, fields: dict) -> tuple[bool, list[str]]:
        """Валидация счёта-фактуры. Возвращает (valid, errors)."""
        errors = []

        # ИНН
        inn = fields.get("seller_inn", "")
        if not (len(inn) == 10 or len(inn) == 12) or not inn.isdigit():
            errors.append(f"Некорректный ИНН: {inn}")

        # Суммовой контроль
        total = float(fields.get("total_amount", 0))
        vat = float(fields.get("vat_amount", 0))
        vat_rate = float(fields.get("vat_rate", 0.2))
        expected_vat = total * vat_rate / (1 + vat_rate)

        if abs(vat - expected_vat) > 0.01:
            errors.append(f"Расхождение НДС: {vat} vs ожидаемое {expected_vat:.2f}")

        return len(errors) == 0, errors


class AsyncExtractionPipeline:
    """
    Полный 5-этапный асинхронный пайплайн.

    Асинхронность важна: 200+ документов × API calls = параллельно.
    """

    PIPELINE_STAGES = [
        "1. document_loading",    # загрузка + OCR если нужно
        "2. text_extraction",     # извлечь plain text из PDF/DOCX
        "3. type_classification", # определить тип документа
        "4. llm_extraction",      # Qwen3-30B → поля + confidence
        "5. validation_dedup"     # схема + суммы + дедупликация
    ]

    async def process_document(self, doc_path: str) -> DocumentExtractionResult:
        """Обработать один документ через весь пайплайн."""
        # Stage 1-2: загрузка и text extraction
        text = await self._load_and_extract_text(doc_path)

        # Stage 3: classification
        doc_type, type_confidence = self.classifier.classify(text)
        schema = self._get_schema(doc_type)

        # Stage 4: LLM extraction
        fields = await self.extractor.extract_fields(text, doc_type, schema)
        fields = self.extractor.flag_low_confidence(fields)

        # Stage 5: validation
        valid, errors = self.validator.validate(doc_type, fields)
        ready_for_erp = valid and all(f.confidence >= 0.70 for f in fields
                                        if f.field_name in schema["required"])

        return DocumentExtractionResult(
            doc_type=doc_type,
            fields=fields,
            overall_confidence=sum(f.confidence for f in fields) / len(fields),
            ready_for_erp=ready_for_erp
        )


BENCHMARK_RESULTS = {
    "датасет": "200+ реальных документов строительной отрасли",
    "типы": ["счета-фактуры", "акты", "договоры", "допсоглашения"],
    "поля": "до 30 полей на документ",
    "модели_сравнение": {
        "Qwen3-235B": "лучшее качество, но медленно/дорого на A100",
        "Qwen3-30B-A3B": "ВЫБРАН: MoE 3B активных, качество ≈ dense 30B",
        "Qwen3-32B": "dense модель, хорошо, но Qwen3-30B-A3B быстрее",
        "Qwen3-7B": "не хватает точности на сложных форматах"
    },
    "метрики": {
        "F1": "95.9% (vs 63% baseline regex+OCR)",
        "Precision": "99.7%",
        "Recall": "93.1%"
    },
    "инфраструктура": "A100 80GB, горизонтальное масштабирование",
    "confidence_threshold": 0.70,
    "erp_integration": "прямой импорт без ручной правки"
}
```

## Применение к Lorenzo

```python
# Lorenzo: extraction пайплайн для ingestion карточек

class LorenzoDocumentIngestion:
    """
    Рег.облако паттерн для Lorenzo:
    5-этапный пайплайн для ingestion новых документов в базу знаний.

    Применение: автоматическое извлечение метаданных из новых
    Хабр-статей для создания карточек Lorenzo.

    Схема extraction:
    required: [author, title, date, habr_url, layer]
    optional: [github_url, metrics, tech_stack, unique_aspect]

    Qwen3 → extraction → schema validation → card creation → CardStore
    Confidence threshold 0.80 для автоматического добавления в индекс.
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Accounting Docs + Finance RAG 4-head (R49)** | Извлечённые поля из счетов-фактур → Finance RAG для аналитических запросов по транзакциям |
| **Accounting Docs + GBNF Decoding (R49)** | GBNF грамматика для extraction: JSON schema как грамматика → 100% валидный JSON от LLM |
| **Accounting Docs + RAG Chunking (R43)** | Семантическая разбивка договоров (50-200 стр.) перед extraction → лучший контекст для LLM |
| **Accounting Docs + LLM Observability (R45)** | Трейсинг: какие поля чаще получают confidence < 0.7 → точечные улучшения промптов |
| **Accounting Docs + Review Queue (Lorenzo)** | Документы с confidence < threshold → Review Queue Streamlit для ручной проверки полей |

## Контакт

- Статья: https://habr.com/ru/companies/runity/articles/987424/ (январь 2025)
- Авторы: Рег.облако (runity) + Raft consulting
- Qwen3-30B-A3B-Instruct: huggingface.co/Qwen/Qwen3-30B-A3B-Instruct (MoE)
- Смежная (SAP ERP Text2SQL, R49): docs/06-discovery/round-49/projects/gennadybanin-text2sql-sap-erp-schema-explorer.md
- Смежная (Finance RAG 4-head, R49): docs/06-discovery/round-49/projects/runoi-finance-rag-four-head-hybrid-retriever.md
- Смежная (FinPDF pipeline, R32): docs/06-discovery/round-32/
