---
date: 2026-05-28
tags: [rag, ingestion, architecture, collaboration]
state: normalized
---

# Анализ договорных рисков: Schema Guided Reasoning + CoT

<!-- toc-auto -->
<!-- tags: contract-risk-analysis-schema-guided-reasoning, docs -->


<!-- summary -->
> `contract-risk-analysis-schema-guided-reasoning` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** favioes  
**Хабр:** https://habr.com/ru/articles/1005144/  
**GitHub:** нет (production система)  
**Слой:** analytics / orchestration  
**Дата:** март 2025  
**Уникальность:** Chain-of-Thought с типизированными JSON-схемами как механизм детерминированного вывода (Schema Guided Reasoning): LLM обязана заполнить `clause_number`, `confidence` (0–1), `reason_short` — превращает свободный текст в структурированный аудит. Preprocessing восстанавливает визуальную нумерацию пунктов из `numbering.xml` Word-документов через abstract numbering maps — решение для корпоративных договоров с Track Changes. 1000+ договоров/год.

## Проблема: LLM выдаёт мнение, юрист хочет структуру

```
Наивный подход: "Найди риски в этом договоре"
  → LLM: "Пункт 5 выглядит рискованным потому что..."
  → Нет: номера пунктов, confidence, структуры для Excel

Реальный договор:
  → Track Changes: нумерация пунктов смещается при удалении
  → Word docx: визуальный "5.2.1" в XML → абстрактная нумерация
  → Нужно: пункт 5.2.1 = риск "ответственность" = confidence 0.87

Schema Guided Reasoning решает:
  → JSON-схема ОБЯЗЫВАЕТ LLM структурировать вывод
  → reasoning_effort=medium: CoT "думает" перед заполнением схемы
  → Единственный гиперпараметр: порог confidence для фильтрации
```

## Schema Guided Reasoning: принудительная структура

```python
# Анализ договорных рисков: production пайплайн

from openai import OpenAI
from pydantic import BaseModel, Field
import json

client = OpenAI()

class ClauseRisk(BaseModel):
    """
    Типизированная схема риска: LLM ОБЯЗАНА заполнить все поля.
    Schema Guided Reasoning = CoT + structured output.
    """
    clause_number: str = Field(
        description="Номер пункта договора (например '5.2.1')"
    )
    risk_category: str = Field(
        description="Категория: ответственность|штрафы|расторжение|конфиденциальность|IP"
    )
    risk_description: str = Field(
        description="Описание риска (1-2 предложения)"
    )
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Уверенность LLM в наличии риска (0.0-1.0)"
    )
    reason_short: str = Field(
        description="Краткое обоснование confidence (<100 символов)"
    )
    mitigation: str = Field(
        description="Рекомендация по снижению риска"
    )

class ContractAnalysis(BaseModel):
    """Результат анализа всего договора."""
    contract_title: str
    total_clauses_analyzed: int
    risks: list[ClauseRisk]
    overall_risk_level: str = Field(
        description="low|medium|high|critical"
    )


def analyze_contract_risks(contract_text: str,
                             confidence_threshold: float = 0.7) -> dict:
    """
    Schema Guided Reasoning: CoT reasoning_effort=medium + typed JSON schema.

    reasoning_effort=medium: модель "думает" перед структурированием.
    Единственный настраиваемый параметр: порог confidence.
    """
    response = client.responses.parse(
        model="gpt-4o",
        input=[{
            "role": "user",
            "content": f"""Проанализируй договор и найди все правовые риски.

Договор:
{contract_text}

Для каждого риска укажи точный номер пункта, категорию, описание
и степень уверенности от 0 до 1. Будь консервативным в оценках."""
        }],
        text_format=ContractAnalysis,
        reasoning={"effort": "medium"}  # CoT перед заполнением схемы
    )

    analysis = response.output_parsed

    # Фильтрация по порогу — единственный гиперпараметр
    filtered_risks = [
        r for r in analysis.risks
        if r.confidence >= confidence_threshold
    ]

    return {
        "contract_title": analysis.contract_title,
        "total_risks_found": len(analysis.risks),
        "high_confidence_risks": len(filtered_risks),
        "risks": [r.model_dump() for r in filtered_risks],
        "overall_risk_level": analysis.overall_risk_level,
        "threshold_used": confidence_threshold
    }
```

## Preprocessing: восстановление нумерации Word docx

```python
from docx import Document
from lxml import etree
from rapidfuzz import fuzz, process

class WordContractPreprocessor:
    """
    Ключевое: корпоративные договоры с Track Changes имеют
    смещённую нумерацию пунктов в XML.
    Восстановление визуальной нумерации через abstract numbering maps.
    """

    def extract_with_numbering(self, docx_path: str) -> list[dict]:
        """
        Извлечь параграфы с правильными номерами пунктов.
        """
        doc = Document(docx_path)
        numbering_map = self._build_abstract_numbering_map(doc)

        clauses = []
        counters = {}  # уровень → текущий счётчик

        for para in doc.paragraphs:
            if not para.text.strip():
                continue

            # Получить уровень нумерации из XML
            num_id, ilvl = self._get_numbering_info(para._element)
            if num_id is None:
                clauses.append({"number": None, "text": para.text})
                continue

            # Восстановить визуальный номер из abstract numbering
            visual_number = self._compute_visual_number(
                num_id, ilvl, numbering_map, counters
            )
            clauses.append({
                "number": visual_number,  # "5.2.1" а не XML-ID
                "text": para.text,
                "level": ilvl
            })

        return clauses

    def _build_abstract_numbering_map(self, doc: Document) -> dict:
        """
        Парсинг numbering.xml: abstractNumId → формат нумерации.
        Нужен для правильной генерации "5.2.1" из XML-счётчиков.
        """
        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            return {}

        root = etree.fromstring(numbering_part._blob)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

        abstract_nums = {}
        for abstract_num in root.findall("w:abstractNum", ns):
            abstract_id = abstract_num.get(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}abstractNumId"
            )
            levels = {}
            for lvl in abstract_num.findall("w:lvl", ns):
                ilvl = int(lvl.get(
                    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ilvl"
                ))
                num_fmt = lvl.find("w:numFmt/[@w:val]", ns)
                lvl_text = lvl.find("w:lvlText/[@w:val]", ns)
                levels[ilvl] = {
                    "format": num_fmt.get("{...}val") if num_fmt is not None else "decimal",
                    "text": lvl_text.get("{...}val") if lvl_text is not None else "%1"
                }
            abstract_nums[abstract_id] = levels

        return abstract_nums

    def fuzzy_match_clause(self, clause_number: str,
                            clauses: list[dict],
                            threshold: int = 85) -> dict | None:
        """
        RapidFuzz: поиск пункта по нечёткому совпадению.
        Нужен когда LLM указывает "5.2" вместо "5.2.1".
        """
        numbers = [c["number"] for c in clauses if c["number"]]
        match = process.extractOne(
            clause_number, numbers,
            scorer=fuzz.ratio,
            score_cutoff=threshold
        )
        if match:
            matched_number = match[0]
            return next(c for c in clauses if c["number"] == matched_number)
        return None
```

## Dual-mode анализ: структурированный + неструктурированный

```python
class DualModeAnalyzer:
    """
    Два режима для разных типов договоров.
    Structured: типовые договоры с предсказуемой структурой.
    Unstructured: свободная форма, иностранные документы.
    """

    def analyze(self, contract_path: str, mode: str = "auto") -> dict:
        clauses = self.preprocessor.extract_with_numbering(contract_path)

        if mode == "auto":
            # Определить режим по наличию нумерации
            has_numbering = any(c["number"] for c in clauses)
            mode = "structured" if has_numbering else "unstructured"

        if mode == "structured":
            return self._structured_analysis(clauses)
        else:
            return self._unstructured_analysis(contract_path)

    def _structured_analysis(self, clauses: list[dict]) -> dict:
        """
        Анализ по пунктам: каждый пункт → отдельный SGR запрос.
        Параллельно через Celery для 1000+ договоров/год.
        """
        # Батчи по 10 пунктов для оптимизации токенов
        batches = [clauses[i:i+10] for i in range(0, len(clauses), 10)]
        results = []
        for batch in batches:
            batch_text = "\n".join(
                f"{c['number']}. {c['text']}"
                for c in batch if c["number"]
            )
            risks = analyze_contract_risks(batch_text)
            results.extend(risks["risks"])

        return {"mode": "structured", "risks": results}


PRODUCTION_METRICS = {
    "volume": "1000+ договоров/год",
    "stack": {
        "api": "FastAPI",
        "queue": "Celery + Redis",
        "db": "SQLAlchemy",
        "export": "pandas + xlsxwriter",
        "parsing": "lxml, python-docx",
        "fuzzy_match": "RapidFuzz",
        "llm": "OpenAI Responses API (reasoning_effort=medium)"
    },
    "speed": "минуты вместо ~2 часов на договор",
    "hyperparameters": "только 1: порог confidence (default=0.7)",
    "split_strategy": "dev/val/test по договорам, не по строкам"
}
```

## Применение к Lorenzo

```python
# Lorenzo анализирует документы.
# SGR паттерн: структурированное извлечение фактов с confidence

class LorenzoSGRExtractor:
    """
    Schema Guided Reasoning для документного Q&A:
    Вместо свободного текста → типизированный вывод с confidence.
    """

    class ExtractedFact(BaseModel):
        fact: str
        source_section: str
        confidence: float
        supporting_quote: str

    def extract_facts(self, question: str,
                       document: str) -> list[dict]:
        response = client.responses.parse(
            model="gpt-4o-mini",
            input=[{"role": "user", "content":
                f"Вопрос: {question}\n\nДокумент:\n{document}"}],
            text_format=list[self.ExtractedFact],
            reasoning={"effort": "low"}
        )
        return [f.model_dump() for f in response.output_parsed
                if f.confidence >= 0.7]
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **SGR + CV Guard (R37)** | SGR для юридических фактов + CV Guard паттерн верификации = двойная проверка |
| **SGR + LLM Judge (R28)** | SGR вывод → LLM-судья проверяет confidence калибровку |
| **SGR + Enterprise RAG (R32)** | RAG находит пункты → SGR структурирует риски по каждому |
| **SGR + AISecurity (R37)** | FLAME guard перед SGR: фильтр опасных запросов к юридическим документам |
| **SGR + Lorenzo Gateway** | /api/ask → SGR: структурированные ответы с confidence вместо свободного текста |

## Контакт

- Статья: https://habr.com/ru/articles/1005144/ (март 2025)
- Автор: favioes (Хабр)
- OpenAI Responses API: platform.openai.com/docs/api-reference/responses
- RapidFuzz: github.com/maxbachmann/RapidFuzz
- Смежная (нормоконтроль Directum): https://habr.com/ru/companies/directum/articles/980140/
- Смежная (LLM юридические документы ContentAI): https://habr.com/ru/companies/contentai/articles/932894/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
