---
date: 2026-05-28
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# ИИ-ассистент врача: GigaAM ASR + Mistral NLP → авто-заполнение ЭМК

<!-- toc-auto -->
<!-- tags: ai-talent-hub-medical-asr-nlp-emr-autofill, docs -->


<!-- summary -->
> `ai-talent-hub-medical-asr-nlp-emr-autofill` — раздел документации проекта Lorenzo.


> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

**Авторы:** Максим Иоган, Артур Мусаев, Денис Кустов, Алина Миллер (AI Talent Hub)  
**Хабр:** https://habr.com/ru/articles/915330/  
**GitHub:** нет (MVP-стадия)  
**Слой:** orchestration / analytics  
**Дата:** июнь 2025  
**Уникальность:** End-to-end pipeline от аудио приёма пациента до структурированной ЭМК: GigaAM (Сбер, open-source) для распознавания речи в реальном времени + Diart/Pyannote/NeMo для диаризации спикеров → Mistral NLP-модуль для NER из медицинской речи и авто-заполнения полей медкарты. Синтетические тренировочные данные из фармацевтических терминологических датасетов и симулированных записей консультаций — обход ограничений приватности реальных пациентов. Клинические рекомендации генерируются LLM параллельно с заполнением карты.

## Проблема: врач тратит 30-40% времени на документирование

```
Типичный приём пациента (20 минут):
  → 12-15 мин: диалог с пациентом
  → 5-8 мин: документирование в ЭМК вручную
  → Врач печатает, не слушает, упускает детали

Проблема ЭМК в России:
  → ЕГИСЗ: тысячи полей для заполнения
  → Жалобы, анамнез, осмотр, диагноз, назначения
  → Шаблоны не адаптированы к разговорной речи врача
  → Медицинская терминология: нераспознаётся в общих ASR

Синтетические данные вместо реальных:
  → Записи пациентов — персональные данные (152-ФЗ)
  → Реальные записи приёмов: невозможно получить для обучения
  → Решение: фармацевтические термины + симуляция диалогов
```

## Pipeline: от речи к структурированной ЭМК

```python
# AI Talent Hub: Medical AI Assistant
# habr.com/ru/articles/915330

from dataclasses import dataclass, field
from typing import Optional
import asyncio

@dataclass
class MedicalSession:
    """Одна консультационная сессия: аудио → структурированная ЭМК."""
    session_id: str
    audio_stream: bytes         # входящий аудио-поток
    doctor_id: str
    patient_id: str

    # Промежуточные результаты
    transcript: list[dict] = field(default_factory=list)    # [speaker, text, time]
    entities: dict = field(default_factory=dict)             # NER результаты
    emr_fields: dict = field(default_factory=dict)           # поля ЭМК
    clinical_recs: list[str] = field(default_factory=list)  # рекомендации LLM


class MedicalASRPipeline:
    """
    Шаг 1: Распознавание речи + диаризация спикеров.

    GigaAM: открытая ASR модель Сбера.
    Оптимизирована для русского языка, медицинская терминология в словаре.
    Diart: онлайн-диаризация в реальном времени (кто говорит когда).
    """

    def __init__(self):
        # GigaAM (Sber open-source ASR)
        import gigaam
        self.asr = gigaam.load_model("v2_rnnt")  # CTC + RNN-T

        # Diart: онлайн-диаризация
        from diart import SpeakerDiarization
        from diart.sources import MicrophoneAudioSource
        self.diarizer = SpeakerDiarization()

        # Pyannote: сегментация + NeMo для сложных случаев
        from pyannote.audio import Pipeline
        self.pyannote = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1"
        )

    async def process_stream(self, audio_stream,
                              session: MedicalSession) -> list[dict]:
        """
        Асинхронная обработка аудио-потока в реальном времени.
        Диаризация: автоматическое определение "врач" vs "пациент".
        """
        transcript = []
        async for audio_chunk in audio_stream:
            # Диаризация: определить спикера
            speaker_segment = await self.diarizer.process(audio_chunk)

            # ASR: распознать речь
            text = self.asr.transcribe(audio_chunk)

            # Определить роль: врач (задаёт вопросы) vs пациент
            role = self._classify_speaker(text, speaker_segment)

            transcript.append({
                "speaker": role,      # "doctor" / "patient"
                "text": text,
                "timestamp": speaker_segment.start
            })

        session.transcript = transcript
        return transcript

    def _classify_speaker(self, text: str, segment: dict) -> str:
        """
        Эвристика: врач спрашивает, пациент отвечает.
        Медицинские термины → вероятнее врач.
        Жалобы ("болит", "беспокоит") → вероятнее пациент.
        """
        doctor_indicators = ["расскажите", "жалобы", "давление", "назначаю"]
        patient_indicators = ["болит", "беспокоит", "чувствую", "уже неделю"]

        doc_score = sum(1 for kw in doctor_indicators if kw in text.lower())
        pat_score = sum(1 for kw in patient_indicators if kw in text.lower())

        return "doctor" if doc_score >= pat_score else "patient"


class MedicalNLPModule:
    """
    Шаг 2: NER + авто-заполнение ЭМК.

    Mistral-based модель, дообученная на медицинских терминах.
    Синтетические данные: фармацевтические термины + симуляция диалогов.
    """

    # Поля ЭМК для авто-заполнения
    EMR_SCHEMA = {
        "complaints": "Жалобы пациента",
        "anamnesis_disease": "Анамнез заболевания",
        "anamnesis_life": "Анамнез жизни",
        "objective_status": "Объективный статус",
        "diagnosis": "Диагноз (МКБ-10)",
        "treatment_plan": "План лечения",
        "prescriptions": "Назначения",
        "followup": "Явка на повторный приём"
    }

    NER_ENTITIES = {
        "symptom": ["боль", "температура", "тошнота", "одышка"],
        "medication": ["амоксициллин", "ибупрофен", "метформин"],
        "diagnosis": ["ОРВИ", "гипертония", "диабет 2 типа"],
        "body_part": ["голова", "грудь", "живот", "спина"],
        "duration": ["неделю", "три дня", "с прошлого года"],
        "measurement": ["38.5°C", "140/90 мм рт.ст.", "10 мг"]
    }

    def extract_entities(self, transcript: list[dict]) -> dict:
        """
        NER из транскрипта консультации.
        Медицинская NER: Mistral + специализированный словарь.
        """
        full_text = " ".join([t["text"] for t in transcript])

        # LLM-based NER
        prompt = f"""Извлеки медицинские сущности из транскрипта консультации.

Транскрипт:
{full_text}

Извлеки JSON со следующими полями:
- symptoms: список симптомов
- medications_mentioned: упомянутые препараты
- diagnosis_hypothesis: гипотезы диагноза
- measurements: числовые показатели (температура, давление и т.д.)
- duration: длительность симптомов
- body_parts: упомянутые части тела

Верни только JSON."""

        entities_raw = self.llm.complete(prompt)
        return self._parse_entities(entities_raw)

    def fill_emr(self, transcript: list[dict],
                  entities: dict) -> dict:
        """
        Авто-заполнение полей ЭМК из транскрипта + NER.
        Каждое поле = отдельный LLM-запрос с контекстом.
        """
        emr = {}

        # Жалобы: из слов пациента
        patient_text = " ".join([
            t["text"] for t in transcript
            if t["speaker"] == "patient"
        ])
        emr["complaints"] = self._fill_field(
            "complaints", patient_text, entities
        )

        # Назначения: из слов врача
        doctor_text = " ".join([
            t["text"] for t in transcript
            if t["speaker"] == "doctor"
        ])
        emr["prescriptions"] = self._fill_field(
            "prescriptions", doctor_text, entities
        )

        # Диагноз: синтез + МКБ-10 код
        emr["diagnosis"] = self._map_to_icd10(entities.get("diagnosis_hypothesis", []))

        return emr

    def _map_to_icd10(self, diagnoses: list[str]) -> dict:
        """
        Маппинг диагноза → код МКБ-10.
        Используется lookup-таблица + LLM для неоднозначных случаев.
        """
        ICD10_COMMON = {
            "ОРВИ": "J06.9",
            "гипертония": "I10",
            "диабет 2 типа": "E11",
            "бронхит": "J40"
        }
        result = {}
        for diagnosis in diagnoses:
            code = ICD10_COMMON.get(diagnosis)
            if not code:
                code = self.llm.complete(
                    f"МКБ-10 код для '{diagnosis}'? Только код."
                )
            result[diagnosis] = code
        return result


class SyntheticMedicalDataGenerator:
    """
    Синтетические данные вместо реальных записей пациентов (152-ФЗ).
    """

    def generate_consultation(self,
                               disease_type: str) -> list[dict]:
        """
        Симуляция диалога врач-пациент.
        Источники: фармакологические справочники + стандарты лечения МЗ РФ.
        """
        prompt = f"""Сгенерируй реалистичный диалог приёма у врача.
Диагноз: {disease_type}
Формат: [Врач]: ... [Пациент]: ...
Используй медицинскую терминологию.
Длина: 15-20 реплик."""
        return self.llm.complete(prompt)
```

## Технический стек и статус

```python
SYSTEM_PROFILE = {
    "авторы": "AI Talent Hub (Иоган, Мусаев, Кустов, Миллер)",
    "статус": "MVP, реальное время ещё оптимизируется",

    "стек": {
        "asr": "GigaAM v2 (Сбер, open-source, RNNT архитектура)",
        "diarization": ["Diart (онлайн)", "Pyannote 3.1", "NVIDIA NeMo"],
        "nlp": "Mistral-based (дообученный на медицинских данных)",
        "синтетика": "Фармацевтические датасеты + симуляция диалогов"
    },

    "целевые_поля_ЭМК": [
        "Жалобы", "Анамнез заболевания", "Анамнез жизни",
        "Объективный статус", "Диагноз (МКБ-10)",
        "План лечения", "Назначения", "Явка"
    ],

    "проблемы_решённые": [
        "Приватность: синтетика вместо реальных записей",
        "Диаризация: разделение врач/пациент в реальном времени",
        "Медицинский словарь: GigaAM лучше общих ASR"
    ],

    "ограничения": [
        "Задержка real-time не оптимизирована (MVP)",
        "Точность NER на редких диагнозах не измерена",
        "Нет интеграции с реальными ЕГИСЗ-системами"
    ]
}
```

## Применение к Lorenzo

```python
# Lorenzo: Medical NLP паттерн для структурированного извлечения

class LorenzoStructuredExtractor:
    """
    AI Talent Hub паттерн для Lorenzo:
    Вместо EMR — структурированное извлечение из discovery-статей.
    NER → поля карточки проекта.
    """

    PROJECT_SCHEMA = {
        "author": "Автор (Habr username)",
        "technologies": "Используемые технологии",
        "metrics": "Численные результаты",
        "github": "GitHub репозиторий",
        "problem": "Решаемая проблема",
        "innovation": "Ключевая инновация"
    }

    def extract_project_card(self, article_text: str) -> dict:
        """NER из статьи → автозаполнение карточки проекта."""
        return self.nlp.extract_entities(article_text, self.PROJECT_SCHEMA)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **AI EMR + MAESTRO (R38)** | CARL DAG для пошаговой клинической логики поверх авто-заполненной ЭМК |
| **AI EMR + Structured Output (R40)** | Instructor + Pydantic: гарантированный JSON для полей ЭМК |
| **AI EMR + Privacy Gateway (R41)** | PII-прокси: анонимизация перед отправкой транскрипта в облачный LLM |
| **AI EMR + LangFuse (R38)** | Трейсинг каждого поля ЭМК: какой промпт дал лучшее заполнение |
| **AI EMR + Cognitive Memory (R31)** | SQLite память: история пациента между приёмами без повторного сбора анамнеза |

## Контакт

- Статья: https://habr.com/ru/articles/915330/ (июнь 2025)
- AI Talent Hub: aitalenthub.ru
- GigaAM: github.com/salute-developers/GigaAM
- Смежная (медицинский Graph RAG, Sandboxer): https://habr.com/ru/companies/sandboxer/articles/1032704/
- Смежная (DBRM медицинские агенты, R31): https://habr.com/ru/companies/raft/articles/960388/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
