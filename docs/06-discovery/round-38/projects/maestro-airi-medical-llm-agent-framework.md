# MAESTRO: промышленный фреймворк медицинских LLM-агентов от AIRI

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** yaroslav_bespalov (AIRI — Институт искусственного интеллекта)  
**Хабр:** https://habr.com/ru/companies/airi/articles/967612/  
**GitHub:** нет (внутренняя разработка AIRI)  
**Слой:** orchestration  
**Дата:** ноябрь 2025  
**Уникальность:** Промышленный мультиагентный фреймворк для медицинских систем, реально задеплоенный в СберЗдоровье и СберМедИИ. CARL (Event-Action-Result) формализует экспертное медицинское мышление как DAG с параллельным выполнением. FLAME — встроенная защита от jailbreak с задержкой 2–5ms (точность 98.7%). Text Extractor CER <4%.

## Проблема: медицинские агенты не прощают ошибок

```
Стандартный LLM-агент для медицины:
  → Нет формализации клинического рассуждения (порядок шагов важен)
  → Нет встроенной защиты: jailbreak в медицине = репутационный и юридический риск
  → Нет аудитируемости: врач должен видеть КАК система пришла к выводу
  → Нет метрик надёжности на медицинском домене

MAESTRO решает:
  → CARL: DAG-граф клинических шагов с параллельным выполнением
  → FLAME: мгновенная защита от атак (2-5ms, не замедляет UX)
  → Full provenance: каждый шаг агента — аудитируемый event
  → Реальный deployment: СберЗдоровье, СберМедИИ
```

## Архитектура MAESTRO

```python
# AIRI MAESTRO: мультиагентный фреймворк для медицины

from maestro import Agent, DAGWorkflow, CARLStep, FLAMEGuard
from maestro.connectors import GigaChatConnector, PostgreSQLMemory

class MedicalConsultationAgent(Agent):
    """
    MAESTRO агент для медицинской консультации.
    CARL: Event-Action-Result формализация клинического мышления.
    """

    def __init__(self):
        super().__init__(
            name="medical_consultant",
            llm=GigaChatConnector(model="GigaChat-Max"),
            memory=PostgreSQLMemory(dsn="postgresql://..."),
            guard=FLAMEGuard(threshold=0.85)  # jailbreak защита
        )
        self.workflow = self._build_carl_dag()

    def _build_carl_dag(self) -> DAGWorkflow:
        """
        CARL DAG: Event → Action → Result для медицинской консультации.
        Поддерживает параллельное выполнение независимых шагов.
        """
        dag = DAGWorkflow()

        # Этап 1: Сбор анамнеза (последовательный)
        dag.add_step(CARLStep(
            event="patient_complaint_received",
            action="extract_symptoms_and_history",
            result="structured_anamnesis",
            prompt="""Извлеки из жалобы пациента:
            1. Основные симптомы (с длительностью и интенсивностью)
            2. Сопутствующие заболевания
            3. Принимаемые препараты
            Верни структурированный JSON."""
        ))

        # Этап 2: Параллельный анализ (3 ветки одновременно)
        dag.add_parallel_steps([
            CARLStep(
                event="anamnesis_ready",
                action="generate_differential_diagnosis",
                result="ddx_list",
                prompt="Дифференциальный диагноз на основе {anamnesis}..."
            ),
            CARLStep(
                event="anamnesis_ready",
                action="check_drug_interactions",
                result="drug_alerts",
                prompt="Проверь взаимодействие препаратов: {medications}..."
            ),
            CARLStep(
                event="anamnesis_ready",
                action="recommend_investigations",
                result="lab_orders",
                prompt="Рекомендуемые исследования для {symptoms}..."
            )
        ])

        # Этап 3: Синтез (ждёт все ветки)
        dag.add_step(CARLStep(
            event="parallel_analysis_complete",
            action="synthesize_clinical_recommendation",
            result="final_recommendation",
            depends_on=["ddx_list", "drug_alerts", "lab_orders"]
        ))

        return dag
```

## FLAME: встроенная защита за 2–5ms

```python
class FLAMEGuard:
    """
    Fast Language Attack Mitigation Engine.
    On-premise защита: данные не покидают инфраструктуру.

    Метрики (из статьи):
      Точность: 98.7%
      Полнота:  90.9%
      Latency:  2-5ms (не замедляет UX)
    """

    MEDICAL_ATTACK_PATTERNS = [
        # Попытки получить конкретные дозировки для самолечения
        r"скажи точную дозу .{0,50} для меня",
        # Попытки обойти медицинскую ответственность
        r"ты не врач, поэтому можешь",
        # Извлечение данных других пациентов
        r"покажи (данные|историю|карту) (пациент|больн)",
        # Ролевые атаки
        r"притворись что ты (хакер|взломщик|не ограниченный)",
    ]

    def scan(self, user_input: str) -> tuple[bool, float]:
        """
        Быстрое сканирование: regex (0.5ms) + micro-classifier (1.5ms).
        Returns: (is_attack, confidence)
        """
        # Уровень 1: regex patterns (<<1ms)
        for pattern in self.MEDICAL_ATTACK_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                return True, 0.95

        # Уровень 2: lightweight binary classifier (2-4ms)
        features = self._extract_features(user_input)
        prob = self.micro_model.predict_proba([features])[0][1]

        return prob > self.threshold, float(prob)

    def _extract_features(self, text: str) -> list[float]:
        """
        36 признаков: лексические, синтаксические, семантические.
        Всё без LLM — чистая статистика для скорости.
        """
        return [
            len(text) / 1000,              # нормированная длина
            text.count("не ограничен"),    # ключевые фразы
            text.count("забудь"),
            self._entropy(text),           # информационная энтропия
            # ... 32 другие признака
        ]
```

## Детектор медицинских вопросов: >99.9%

```python
class MedicalQuestionDetector:
    """
    Классификатор: является ли запрос медицинским?
    Метрики: точность >99.9%, полнота >99.9% (из статьи AIRI).

    Нужен чтобы не передавать немедицинские запросы
    медицинскому агенту.
    """

    MEDICAL_KEYWORDS = {
        "ru": ["симптом", "боль", "лечение", "диагноз", "препарат",
               "врач", "болезнь", "анализ", "давление", "температура"],
        "medical_context": ["принимать", "пить", "колоть", "мазать"]
    }

    def classify(self, query: str) -> dict:
        keyword_score = self._keyword_score(query)
        semantic_score = self._semantic_score(query)  # TF-IDF на медкорпусе

        combined = 0.4 * keyword_score + 0.6 * semantic_score
        return {
            "is_medical": combined > 0.5,
            "confidence": float(combined),
            "route": "medical_agent" if combined > 0.5 else "general_agent"
        }
```

## Text Extractor: CER < 4%

```python
class MedicalTextExtractor:
    """
    Извлечение структурированных данных из медицинских текстов.
    CER (Character Error Rate) < 4% на тестовом наборе AIRI.

    Специализирован на:
    - Извлечение числовых значений (давление 120/80, температура 37.2)
    - Распознавание МКБ-10 кодов
    - Парсинг рецептов (препарат + доза + кратность)
    """

    def extract(self, clinical_text: str) -> dict:
        return {
            "vitals": self._extract_vitals(clinical_text),
            # "АД 120/80" → {"systolic": 120, "diastolic": 80}
            "diagnoses": self._extract_icd10(clinical_text),
            # "J06.9" → {"code": "J06.9", "name": "ОРВИ"}
            "medications": self._extract_prescriptions(clinical_text),
            # "Амоксициллин 500мг 3р/д 7дней" → структурированный объект
            "dates": self._extract_medical_dates(clinical_text)
        }
```

## Production метрики MAESTRO

```python
MAESTRO_PRODUCTION_METRICS = {
    "deployment": ["СберЗдоровье", "СберМедИИ"],
    "stack": {
        "runtime": "Python 3.12+",
        "api": "FastAPI",
        "transport": "gRPC + protobuf",
        "storage": "PostgreSQL",
        "llm": "GigaChat (различные версии)",
        "auth": "JWT"
    },

    "component_metrics": {
        "FLAME_guard": {
            "precision": 0.987,
            "recall": 0.909,
            "latency_ms": "2-5"
        },
        "question_detector": {
            "precision": 0.999,
            "recall": 0.999,
            "description": "Маршрутизация медицинских vs общих запросов"
        },
        "text_extractor": {
            "CER": "<4%",
            "description": "Извлечение витальных показателей, МКБ-10, рецептов"
        }
    },

    "carl_dag_benefits": [
        "Параллельное выполнение независимых диагностических шагов",
        "Полная аудитируемость: Event → Action → Result для каждого шага",
        "Детерминированный порядок при зависимостях",
        "Визуализируемый граф клинического рассуждения"
    ]
}
```

## Применение к Lorenzo

```python
# Lorenzo как Knowledge OS может использовать CARL-паттерн
# для структурирования сложных Q&A пайплайнов

class LorenzoCARLPipeline:
    """
    CARL DAG для документного Q&A:
    Параллельный поиск по разным источникам → синтез ответа.
    """

    def answer(self, question: str) -> dict:
        dag = DAGWorkflow()

        # Параллельный поиск по разным индексам
        dag.add_parallel_steps([
            CARLStep(event="question", action="bm25_search", result="bm25_hits"),
            CARLStep(event="question", action="semantic_search", result="sem_hits"),
            CARLStep(event="question", action="graph_lookup", result="graph_hits")
        ])

        # Синтез из всех источников
        dag.add_step(CARLStep(
            event="all_searches_done",
            action="synthesize_answer",
            result="final_answer",
            depends_on=["bm25_hits", "sem_hits", "graph_hits"]
        ))

        return dag.execute({"question": question})
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **MAESTRO + AISecurity (R37)** | FLAME (медицина) + C/Rust Shield (общий) = двухуровневая on-premise защита |
| **MAESTRO + DBRM (R31)** | CARL DAG для медицинских рассуждений + DBRM оценка качества агента |
| **MAESTRO + Cognitive Memory (R31)** | CARL Event хранится как эпизодическая память для контекстных консультаций |
| **MAESTRO + LangGraph (R35)** | CARL DAG → LangGraph StateGraph: state machine для медицинских воркфлоу |
| **MAESTRO + CV Guard (R37)** | FLAME защита + CV верификация медицинских изображений = guard для VLM в медицине |

## Контакт

- Статья: https://habr.com/ru/companies/airi/articles/967612/ (ноябрь 2025)
- AIRI: airi.net
- Deployment: СберЗдоровье, СберМедИИ
- Смежная (DBRM медицинские агенты): https://habr.com/ru/companies/raft/articles/960388/
- Смежная (ИИ-ассистент Genotek речь→ЭМК): https://habr.com/ru/articles/915330/
