# Классификатор тикетов для телеком-поддержки на Qwen2.5-0.5B за $10/месяц

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** ractangle  
**Хабр:** https://habr.com/ru/articles/988916/  
**GitHub:** нет (архитектура описана детально в статье)  
**Слой:** orchestration / analytics  
**Дата:** январь 2026  
**Уникальность:** Полный воспроизводимый pipeline телеком-специфичной классификации обращений: Qwen2.5-0.5B-Instruct fine-tuned на ~4000 синтетических примерах, GGUF Q4_K_M (350 MB), FastAPI + llama-cpp-python, $10/мес VPS (2 vCPU / 4 GB RAM), CPU inference 3-5 сек, intent accuracy 92%. On-premise: никаких данных в облако. Единственная RU статья с конкретным cost benchmark для телеком-классификации.

## Проблема: операторы тратят 60% времени на разбор обращений

```
Типичная телеком-поддержка без автоматизации:
  → Оператор читает тикет → вручную определяет тип обращения
  → 60% времени смены: разбор и маршрутизация, не решение проблем
  → Ошибки маршрутизации: срочные вопросы (отключение) → очередь биллинга
  → Пиковые часы: очередь нарастает быстрее чем операторы справляются

Решение:
  → Автоматическая классификация на входе: intent + urgency + sentiment
  → Авто-маршрутизация в нужный отдел без участия оператора
  → Срочные обращения выносятся в приоритет автоматически
  → Всё локально: телеком-данные не уходят в облако (compliance)
```

## Fine-tuning Qwen2.5-0.5B на телеком-домене

```python
# ractangle: телеком-классификатор на Qwen2.5-0.5B
# habr.com/ru/articles/988916

from dataclasses import dataclass
from typing import Literal

# Структурированный выход классификатора
@dataclass
class TicketClassification:
    intent: Literal[
        "technical_fault",    # технические неисправности
        "billing_question",   # вопросы по биллингу
        "churn_risk",         # угроза оттока (абонент хочет уйти)
        "general_inquiry"     # общие вопросы
    ]
    category: str            # детальная подкатегория (интернет/голос/ТВ/мобильный)
    urgency: Literal["low", "medium", "high", "critical"]
    sentiment: Literal["positive", "neutral", "negative", "angry"]
    routing_destination: str  # куда направить тикет


# Синтетические обучающие данные: 4000 примеров
SYNTHETIC_DATA_EXAMPLES = [
    {
        "text": "У меня не работает интернет уже 3 часа. Жду ответа.",
        "label": TicketClassification(
            intent="technical_fault",
            category="internet",
            urgency="high",
            sentiment="negative",
            routing_destination="tech_support_internet"
        )
    },
    {
        "text": "Мне выставили счёт на 500 рублей больше обычного. Объясните.",
        "label": TicketClassification(
            intent="billing_question",
            category="billing_discrepancy",
            urgency="medium",
            sentiment="negative",
            routing_destination="billing_department"
        )
    },
    {
        "text": "Хочу расторгнуть договор. Надоело платить за плохой сигнал.",
        "label": TicketClassification(
            intent="churn_risk",
            category="service_quality",
            urgency="critical",
            sentiment="angry",
            routing_destination="retention_team"
        )
    }
]


class TelecomDataGenerator:
    """
    Генерация синтетических обучающих данных.
    Телеком-специфика: реальный словарь жалоб, терминология оператора.
    """

    TELECOM_INTENTS = {
        "technical_fault": {
            "templates": [
                "Не работает {service} уже {duration}",
                "Пропал сигнал на {location}",
                "Скорость интернета упала до {speed} Мбит/с"
            ],
            "services": ["интернет", "телефон", "ТВ", "мобильный интернет"],
            "durations": ["час", "3 часа", "весь день", "с утра"]
        },
        "billing_question": {
            "templates": [
                "Почему списали {amount} рублей {period}?",
                "Хочу понять за что начислено {service}",
                "В счёте ошибка: {discrepancy}"
            ]
        },
        "churn_risk": {
            "triggers": [
                "хочу расторгнуть договор",
                "перехожу к другому оператору",
                "отключите меня",
                "надоело платить за плохое качество"
            ],
            "urgency": "critical"  # всегда критический → retention team
        }
    }

    def generate_dataset(self, n_examples: int = 4000,
                          llm_assisted: bool = True) -> list[dict]:
        """
        Генерация датасета для fine-tuning.
        llm_assisted=True: LLM генерирует вариации → разнообразнее
        llm_assisted=False: шаблоны без LLM → быстрее

        Ractangle использовал LLM-assisted: ChatGPT для генерации вариаций.
        """
        dataset = []
        per_intent = n_examples // len(self.TELECOM_INTENTS)

        for intent, config in self.TELECOM_INTENTS.items():
            if llm_assisted:
                examples = self._llm_generate_variations(intent, config, per_intent)
            else:
                examples = self._template_generate(intent, config, per_intent)
            dataset.extend(examples)

        return dataset
```

## Архитектура production-системы

```python
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import json

app = FastAPI(title="Telecom Ticket Classifier")

class TicketRequest(BaseModel):
    text: str
    ticket_id: str

class ClassificationResponse(BaseModel):
    ticket_id: str
    intent: str
    category: str
    urgency: str
    sentiment: str
    routing: str
    confidence: float
    processing_time_ms: float


class QwenTelecomClassifier:
    """
    Qwen2.5-0.5B-Instruct fine-tuned + GGUF Q4_K_M.
    Backend: llama-cpp-python (CPU inference на дешёвом VPS).
    """

    MODEL_PROFILE = {
        "base_model": "Qwen2.5-0.5B-Instruct",
        "fine_tuned_on": "~4000 телеком-специфичных примеров",
        "quantization": "GGUF Q4_K_M",
        "model_size": "350 MB",
        "training": {
            "method": "Full fine-tuning (не LoRA — модель маленькая)",
            "hardware": "Google Colab T4 GPU",
            "time": "40 минут",
            "epochs": 3
        }
    }

    INFERENCE_PROFILE = {
        "backend": "llama-cpp-python",
        "cpu_vps_latency": "3-5 сек",
        "mac_m4_latency": "150-300 мс",
        "ram_usage": "~700 MB",
        "infra_cost": "$10/месяц (2 vCPU / 4 GB RAM VPS + nginx + SSL)"
    }

    def __init__(self, model_path: str):
        from llama_cpp import Llama
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=2,      # 2 vCPU на VPS
            verbose=False
        )
        self.heuristic_filter = HeuristicPreFilter()

    def classify(self, ticket_text: str) -> TicketClassification:
        """
        Классификация с двухступенчатым pipeline:
        1. Heuristic pre-filter: быстрая проверка по ключевым словам
        2. LLM классификация: structured JSON output
        """
        # Быстрая эвристика (< 1мс): определить очевидные случаи
        pre_result = self.heuristic_filter.check(ticket_text)
        if pre_result.is_confident:
            return pre_result.classification

        # LLM классификация с structured output
        prompt = self._build_prompt(ticket_text)
        response = self.llm(
            prompt,
            max_tokens=256,
            temperature=0.1,  # низкая температура → стабильный JSON
            stop=["###"]
        )

        return self._parse_json_response(response["choices"][0]["text"])

    def _build_prompt(self, text: str) -> str:
        return f"""### Задача: классифицировать обращение клиента телеком-оператора.

Обращение: {text}

Верни JSON с полями: intent, category, urgency, sentiment, routing_destination.
Допустимые значения intent: technical_fault, billing_question, churn_risk, general_inquiry.
Urgency: low, medium, high, critical.

### Ответ:
```json"""


class HeuristicPreFilter:
    """
    Быстрая проверка до LLM: очевидные случаи без нейросети.
    Экономия инференса для простых тикетов.
    """

    CHURN_KEYWORDS = ["расторгнуть", "отключите", "уходим", "к другому оператору"]
    CRITICAL_TECH_KEYWORDS = ["нет связи вообще", "полное отключение", "аварийная ситуация"]

    def check(self, text: str) -> "PreFilterResult":
        text_lower = text.lower()

        if any(kw in text_lower for kw in self.CHURN_KEYWORDS):
            return PreFilterResult(
                is_confident=True,
                classification=TicketClassification(
                    intent="churn_risk",
                    category="service_cancellation",
                    urgency="critical",
                    sentiment="negative",
                    routing_destination="retention_team"
                )
            )

        return PreFilterResult(is_confident=False, classification=None)


BENCHMARK_RESULTS = {
    "тест_сет": "500 реальных обезличенных тикетов телеком-оператора",
    "метрики": {
        "intent_accuracy": 0.92,      # 92% точность определения намерения
        "category_accuracy": 0.89,    # 89% точность подкатегории
        "urgency_precision": 0.87,    # точность определения срочности
        "sentiment_accuracy": 0.91
    },
    "инфраструктура": {
        "vps": "2 vCPU / 4 GB RAM",
        "os": "Ubuntu 22.04",
        "stack": "FastAPI + llama-cpp-python + nginx + SSL",
        "logging": "SQLite (локальный audit log)",
        "monthly_cost": "$10"
    },
    "privacy": "On-premise: данные клиентов не покидают инфраструктуру оператора"
}
```

## Применение к Lorenzo

```python
# Lorenzo: telecom-паттерн для классификации входящих запросов

class LorenzoQueryClassifier:
    """
    ractangle паттерн для Lorenzo:
    Классифицировать входящие запросы к /api/ask перед retrieval.
    intent → выбор стратегии поиска.
    urgency → приоритизация в Review Queue.
    """

    LORENZO_INTENTS = {
        "project_search": "Найти проект по теме",
        "author_contact": "Найти контакты автора",
        "combination_ideas": "Какие проекты можно объединить?",
        "technical_detail": "Технические детали реализации"
    }

    def classify_query(self, query: str) -> dict:
        """
        Определить intent запроса → настроить поиск.
        project_search → BM25 + TF-IDF по docs/05-habr-projects/
        author_contact → поиск по docs/contacts/
        combination_ideas → collab_finder
        """
        # Лёгкая эвристика (без LLM) для Lorenzo:
        if any(w in query.lower() for w in ["контакт", "автор", "написать"]):
            return {"intent": "author_contact", "search_section": "contacts"}
        if any(w in query.lower() for w in ["комбинация", "объединить", "синергия"]):
            return {"intent": "combination_ideas", "tool": "collab_finder"}
        return {"intent": "project_search", "search_section": "all"}
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Telecom Classifier + Robovoice (R41)** | Robovoice routing + Qwen-классификатор: текстовые тикеты + голосовые обращения в единую систему |
| **Telecom Classifier + Privacy Gateway (R41)** | On-premise классификация (уже есть) + PII-анонимизация перед escalation в облако |
| **Telecom Classifier + LangGraph (R44)** | Классификатор как стартовый узел LangGraph: intent → ветка графа |
| **Telecom Classifier + LLM Observability (R45)** | Semantic span typing: трассировать каждое решение классификатора, детектировать drift |
| **Telecom Classifier + LoRA Embeddings (R44)** | LoRA на эмбеддингах телеком-домена + fine-tuned classifier = двойная доменная адаптация |

## Контакт

- Статья: https://habr.com/ru/articles/988916/ (январь 2026)
- Автор: ractangle (независимый разработчик, Хабр)
- Base model: Qwen2.5-0.5B-Instruct (Alibaba, HuggingFace)
- Stack: FastAPI + llama-cpp-python + GGUF
- Смежная (LLM телеком общий, R35): docs/06-discovery/round-35/
- Смежная (Robovoice поддержка, R41): docs/06-discovery/round-41/projects/robovoice-llm-rag-omnichannel-customer-support.md
