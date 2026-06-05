# ИИ против болезней: BioBERT на MIMIC-III и Ambient AI Scribing в реальных клиниках

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** full_moon (Magnus Tech)  
**Хабр:** https://habr.com/ru/companies/magnus-tech/articles/878456/  
**GitHub:** нет (обзорная статья с производственными кейсами)  
**Слой:** analytics / knowledge  
**Дата:** апрель 2025  
**Уникальность:** Производственно-валидированные ML-системы в реальных клиниках: Ambient AI scribing (3 442 врача, 303 000 консультаций), BioBERT на MIMIC-III (F1=0.876), Cleerly кардио-диагностика (AUC=0.91), Deep 6 AI отбор пациентов для клинических испытаний (120+ онтологий). Переход "от исследований к клинической практике" как центральная проблема медицинского AI: почему 89% пилотов не попадают в прод.

## Проблема: разрыв между research и clinical deployment

```
Медицинский AI сегодня:
  → 89% пилотов ML в медицине не доходят до продакшна
  → Причины: regulatory approval, clinical validation, liability
  → Академические результаты → не воспроизводятся на реальных пациентах
  → Distribution shift: датасет MIMIC-III (40K+ записей) ≠ данные реальной клиники

Четыре рабочих кейса в статье (уже в продакшне):
  1. BioBERT: NLP по ЭМК → извлечение диагнозов, лекарств, процедур
  2. Cleerly ISCHEMIA: кардио-диагностика по КТА → замена инвазивного FFR
  3. Ambient AI Scribing: авто-транскрипция приёма → структурированные ЭМК
  4. Deep 6 AI: RAG по EMR → поиск пациентов для клинических испытаний
```

## BioBERT: NLP по медицинским записям

```python
# full_moon (Magnus Tech): BioBERT на MIMIC-III
# habr.com/ru/companies/magnus-tech/articles/878456/

from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class ClinicalEntity:
    """Медицинская сущность, извлечённая из ЭМК."""
    text: str
    entity_type: str   # "diagnosis" | "medication" | "procedure" | "symptom"
    icd_code: Optional[str]   # ICD-10 код (если диагноз)
    confidence: float
    span_start: int
    span_end: int


class BioBERTClinicalNLP:
    """
    BioBERT fine-tuned на MIMIC-III для извлечения клинических сущностей.

    MIMIC-III: 40,000+ деидентифицированных записей интенсивной терапии
    (Beth Israel Deaconess Medical Center, 2001–2012).

    Производительность:
    - Accuracy: 89.8%
    - F1-score: 87.6%
    - Задача: NER (Named Entity Recognition) по клиническим заметкам

    Ключевое отличие от general BERT:
    - BioBERT предобучен на PubMed (4.5B слов) + PMC (13.5B слов)
    - Медицинская терминология: "myocardial infarction" != "heart attack"
      в general BERT → в BioBERT → одна концепция
    """

    ENTITY_TYPES = [
        "diagnosis",    # МКБ-10 диагнозы
        "medication",   # названия препаратов + дозировка
        "procedure",    # медицинские процедуры (операции, исследования)
        "symptom",      # симптомы и жалобы
        "lab_value",    # лабораторные показатели + значения
        "anatomy"       # анатомические термины
    ]

    def extract_entities(self, clinical_note: str) -> list[ClinicalEntity]:
        """
        NER-извлечение клинических сущностей из текста приёма.

        Входные данные: неструктурированная врачебная заметка
        Выход: список типизированных сущностей с ICD-кодами

        Пример:
        "Пациент с АГ 2 степени, принимает Лизиноприл 10мг, ЧСС 72 уд/мин"
        → diagnosis(АГ 2 степени, ICD: I10)
        → medication(Лизиноприл, dose: 10мг)
        → lab_value(ЧСС, value: 72 уд/мин)
        """
        # ... BioBERT inference → NER tags → entity extraction
        pass

    def map_to_icd10(self, diagnosis_text: str) -> Optional[str]:
        """
        Маппинг свободного текста диагноза → ICD-10 код.
        Используется SNOMED CT + ICD-10 онтология.
        """
        # Нормализация: "сердечная недостаточность" → "I50" (ICD-10)
        pass


BENCHMARK_RESULTS = {
    "модель": "BioBERT (fine-tuned на MIMIC-III)",
    "датасет": "MIMIC-III: 40,000+ клинических записей ICU",
    "метрики": {
        "accuracy": 0.898,
        "f1_score": 0.876,
        "задача": "Named Entity Recognition (NER) по клиническим заметкам"
    },
    "сравнение": {
        "general_BERT": {"F1": 0.812, "проблема": "не знает медтерминологию"},
        "BioBERT": {"F1": 0.876, "преимущество": "PubMed + PMC pretraining"}
    }
}
```

## Ambient AI Scribing: авто-транскрипция врачебного приёма

```python
class AmbientAIScribing:
    """
    Ambient AI Scribing: автоматическое заполнение ЭМК по аудио приёма.

    Производственные цифры (реальное внедрение):
    - 3,442 врача используют систему
    - 303,000 консультаций обработано
    - Экономия: врач тратит на заполнение ЭМК 2-3 часа в день → <30 мин

    Pipeline:
    1. ASR: аудио приёма → черновой текст (врач + пациент)
    2. Speaker Diarization: разделение голосов врач/пациент
    3. Clinical NLP: извлечение структурированных данных (диагноз, план, Rx)
    4. SOAP-форматирование: Subjective / Objective / Assessment / Plan
    5. ЭМК-интеграция: запись в EMR через FHIR API

    Ключевой барьер (до Ambient AI):
    Doctors spend 37% of their time on EHR documentation
    → Burnout → ошибки → снижение контакта с пациентом
    """

    SOAP_TEMPLATE = {
        "Subjective": "Жалобы пациента, анамнез (из речи пациента)",
        "Objective": "Результаты осмотра, витальные показатели, лаб. данные",
        "Assessment": "Диагноз, дифференциальный диагноз",
        "Plan": "Лечение, направления, follow-up"
    }

    def process_consultation(self,
                              audio_stream: bytes,
                              patient_context: dict) -> dict:
        """
        Real-time обработка приёма: аудио → структурированная ЭМК.

        Конфиденциальность: on-premise deployment, аудио не покидает клинику.
        HIPAA-compliant: де-идентификация перед хранением.
        """
        # Шаг 1: ASR (speech-to-text)
        transcript = self._asr_transcribe(audio_stream)

        # Шаг 2: Speaker diarization
        turns = self._diarize_speakers(transcript)

        # Шаг 3: Извлечь клинические данные
        entities = self._extract_clinical_entities(turns)

        # Шаг 4: Сгенерировать SOAP-заметку
        soap_note = self._generate_soap(entities, patient_context)

        # Шаг 5: Отправить в ЭМК (FHIR)
        return self._write_to_emr(soap_note)
```

## Кардио-диагностика: Cleerly ISCHEMIA

```python
CLEERLY_SYSTEM = {
    "задача": "Неинвазивная оценка ишемической болезни сердца по CCTA",
    "вход": "КТ-ангиография коронарных артерий (CCTA)",
    "выход": "37 параметров состояния сердца + предсказание FFR",

    "метрики": {
        "AUC": 0.91,
        "задача": "Предсказание гемодинамической значимости стенозов"
    },

    "клиническое_значение": (
        "До Cleerly: инвазивный FFR-тест (катетер → риски + дорого) "
        "После: CCTA + AI → те же данные, неинвазивно, без радиационной нагрузки"
    ),

    "принцип": (
        "Quantitative CT (QCT): сегментация бляшек → объём, состав, риск разрыва "
        "FFRCT (Fractional Flow Reserve from CT): симуляция кровотока → ишемия"
    )
}

DEEP6_AI_SYSTEM = {
    "задача": "Отбор пациентов для клинических испытаний по ЭМК",
    "архитектура": "RAG поверх корпуса EMR + 120+ медицинских онтологий",
    "проблема": (
        "80% клинических испытаний не достигают нужного набора пациентов в срок "
        "→ 11 месяцев средняя задержка → $8M потери на испытание"
    ),
    "решение": (
        "Поиск по ЭМК на естественном языке: "
        "'пациенты с HbA1c > 7.5%, возраст 40-65, без почечной недостаточности' "
        "→ система понимает клинические критерии без SQL-запросов"
    ),
    "онтологии": ["SNOMED CT", "ICD-10", "RxNorm", "LOINC", "CPT", "...+115"]
}
```

## Почему 89% пилотов не выходят в прод

```python
CLINICAL_AI_DEPLOYMENT_FAILURES = {
    "регуляторика": {
        "США": "FDA 510(k) clearance → 3-12 месяцев на алгоритм",
        "EU": "CE-маркировка по MDR → клиническая валидация обязательна",
        "РФ": "Росздравнадзор: регистрация как медицинское изделие класса 2а/2б"
    },

    "distribution_shift": {
        "проблема": "MIMIC-III (ICU, Boston, 2001-2012) ≠ текущая клиника",
        "пример": "Модель обучена на текстах на английском → плохо работает на RU",
        "решение": "Domain adaptation + continual learning на локальных данных"
    },

    "интеграция_с_ЭМК": {
        "проблема": "100+ несовместимых EMR-систем (Epic, Cerner, 1С-Медицина...)",
        "стандарт": "FHIR R4 — решает, но внедрение дорого и медленно"
    },

    "liability": {
        "проблема": "Кто отвечает за ошибочный ИИ-диагноз?",
        "модель": "AI = инструмент поддержки решений (DSS), врач — ответственен"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: медицинский AI паттерн для knowledge enrichment

class LorenzoMedicalKnowledge:
    """
    full_moon паттерн для Lorenzo:
    BioBERT NER для извлечения технических сущностей из docs/.
    Ambient AI Scribing идея → авто-протоколирование встреч по аудио.

    "SOAP для проектных обсуждений":
    S (Subjective) — что хотим сделать
    O (Objective) — что уже есть в базе знаний
    A (Assessment) — анализ ситуации
    P (Plan) — конкретные шаги
    """

    def apply_soap_to_project_discussion(self,
                                          meeting_transcript: str) -> dict:
        """
        Структурировать проектное обсуждение по SOAP-паттерну.
        Аналог Ambient AI Scribing — но для tech-meetings Lorenzo.
        """
        return {
            "Subjective": "Что хочет сделать команда (из transcript)",
            "Objective": "Данные из базы знаний (BM25-поиск)",
            "Assessment": "Анализ gap между желаемым и имеющимся",
            "Plan": "Список ACTION_ITEMS"
        }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Ambient Scribing + LangGraph (R44)** | LangGraph граф: ASR → diarize → NER → SOAP → review → write — с HITL перед записью в ЭМК |
| **BioBERT NER + Temporal KG (R47)** | Извлечённые диагнозы + темпоральный граф → история болезни со временными метками |
| **BioBERT + LLM Observability (R45)** | Трейсинг каждого NER-вызова: где модель галлюцинирует в медтерминологии |
| **Deep 6 AI + Lorenzo Search** | RAG по базе знаний с онтологиями: поиск не по ключевым словам, а по смыслу критериев |
| **Ambient AI + SENTINEL (R47)** | Защита медицинского ASR от prompt injection через транскрипт |

## Контакт

- Статья: https://habr.com/ru/companies/magnus-tech/articles/878456/ (апрель 2025)
- Автор: full_moon (Magnus Tech)
- BioBERT: huggingface.co/dmis-lab/biobert-base-cased-v1.2
- MIMIC-III: physionet.org/content/mimiciii/
- Cleerly: cleerly.com (ISCHEMIA система)
- Deep 6 AI: d6ai.com
- FHIR: hl7.org/fhir
- Смежная (DBRM медицина v1, R31): docs/06-discovery/round-31/
- Смежная (LLM медицина v2, R38): docs/06-discovery/round-38/
- Смежная (Temporal KG, R47): docs/06-discovery/round-47/projects/ekaterina-ya-temporal-knowledge-graph-legal-rag.md
