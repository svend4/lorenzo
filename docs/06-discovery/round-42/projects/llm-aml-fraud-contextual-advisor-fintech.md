---
date: 2026-05-28
tags: [rag, orchestration, security, ingestion, architecture]
state: normalized
---

# LLM против мошенников: контекстный советник в AML/AF pipeline

<!-- toc-auto -->
<!-- tags: llm-aml-fraud-contextual-advisor-fintech, docs -->


<!-- summary -->
> `llm-aml-fraud-contextual-advisor-fintech` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** daniilmaibe  
**Хабр:** https://habr.com/ru/articles/908424/  
**GitHub:** нет (архитектурная статья)  
**Слой:** analytics / orchestration  
**Дата:** май 2025  
**Уникальность:** Конкретная production-архитектура LLM как второго уровня в AML/AF пайплайне: не замена правилам и ML, а контекстный советник-объяснитель для аналитиков. Два режима: batch (еженедельные JSON-нарративы на клиента, ~$0.02/клиент) и hybrid (LLM как second-stage scorer + объяснение для оператора). Детальная модель стоимости: $20K/неделю на 1M клиентов через GPT-4-turbo. Паттерн: LLM читает многофакторный профиль клиента → генерирует natural-language объяснение почему транзакция подозрительна.

## Проблема: ML-скор без объяснения — это проблема для регулятора

```
Текущий ML-пайплайн в банке:
  → Правила: device_change AND geo_anomaly AND large_tx → flag
  → ML-модель: gradient boosting score = 0.87
  → Аналитик видит: "Клиент: подозрителен (0.87)"
  → Аналитик думает: "Почему? Что именно смотреть?"

Проблемы:
  → Регулятор (ЦБ РФ/ФАТФ): "Объясните решение о блокировке"
  → Аналитик тратит 10-15 мин на ручное изучение профиля
  → False positives: хороший клиент заблокирован → жалоба
  → ML-модель не может объяснить на русском языке

LLM как контекстный советник:
  → ML-пайплайн работает как прежде (правила + скоринг)
  → LLM читает полный профиль клиента → строит нарратив
  → Аналитик видит: "Клиент сменил устройство в 03:00, находится
    в Екатеринбурге хотя обычно в Москве, перевод 850K руб.
    нетипичному получателю. Комбинация признаков соответствует
    паттерну компрометации учётной записи."
  → Аналитик принимает решение за 2-3 мин вместо 15
```

## Два режима работы

```python
# daniilmaibe: LLM как second-stage в AML/AF pipeline
# habr.com/ru/articles/908424

from dataclasses import dataclass
from typing import Optional

@dataclass
class ClientRiskProfile:
    """
    Мультифакторный профиль клиента для LLM-нарратива.
    Все данные уже собраны ML-пайплайном — LLM только читает.
    """
    client_id: str
    ml_fraud_score: float          # 0.0 - 1.0 от ML-модели
    rule_triggers: list[str]       # сработавшие AML-правила

    # Поведенческие аномалии
    device_change: bool            # смена устройства
    geo_anomaly: bool              # нетипичная геолокация
    time_anomaly: bool             # нетипичное время суток
    velocity_anomaly: bool         # необычная частота операций

    # Транзакционные данные
    transaction_amount: float
    recipient_profile: str         # "новый получатель"/"контрагент под санкциями"
    transaction_type: str

    # Исторический контекст
    avg_monthly_amount: float      # обычный паттерн клиента
    similar_incidents: list[str]   # похожие случаи из истории


class AMLLLMAdvisor:
    """
    LLM-советник: читает профиль риска → генерирует объяснение.
    НЕ принимает решения — только объясняет для аналитика.
    """

    # Режим 1: Batch (офлайн, еженедельно)
    BATCH_PROMPT = """Ты — аналитик финансовой безопасности.
Проанализируй профиль клиента и объясни подозрения на русском языке.

Профиль клиента:
{profile_json}

Требования к ответу:
1. 3-5 предложений, конкретно и по делу
2. Укажи конкретные комбинации признаков (не перечисляй все)
3. Сопоставь с типичным паттерном клиента
4. Если подозрения слабые — скажи честно
5. НЕ выноси решение о блокировке

Формат: краткий нарратив для аналитика."""

    # Режим 2: Hybrid (онлайн, real-time)
    HYBRID_PROMPT = """Транзакция под проверкой.

Клиент {client_id}: ML-скор {ml_score:.2f}
Сработавшие правила: {rules}
Детали операции: {tx_details}
Исторический профиль: {history}

Оцени: насколько обоснованы подозрения?
Дай рекомендацию: ИССЛЕДОВАТЬ / ЗАПРОСИТЬ_ДОКУМЕНТЫ / ПРОПУСТИТЬ
Объясни в 2-3 предложениях."""

    def batch_narrative(self, profile: ClientRiskProfile,
                         model: str = "gpt-4-turbo") -> str:
        """
        Режим 1 (Batch): еженедельный анализ подозрительных клиентов.
        Стоимость: ~1.5K input + 0.5K output = ~2K токенов = ~$0.02/клиент.
        """
        import json
        prompt = self.BATCH_PROMPT.format(
            profile_json=json.dumps(self._profile_to_dict(profile),
                                     ensure_ascii=False, indent=2)
        )
        return self.llm.complete(prompt, model=model)

    def hybrid_score(self, profile: ClientRiskProfile,
                      model: str = "gpt-4-turbo") -> dict:
        """
        Режим 2 (Hybrid): онлайн second-stage после ML-скора.
        LLM вызывается только если ML-скор > threshold (экономия).
        """
        if profile.ml_fraud_score < 0.7:
            return {"recommendation": "ПРОПУСТИТЬ", "narrative": None}

        prompt = self.HYBRID_PROMPT.format(
            client_id=profile.client_id,
            ml_score=profile.ml_fraud_score,
            rules=", ".join(profile.rule_triggers),
            tx_details=f"{profile.transaction_amount:,.0f} руб. → {profile.recipient_profile}",
            history=f"Обычный объём: {profile.avg_monthly_amount:,.0f} руб./мес"
        )

        narrative = self.llm.complete(prompt, model=model)
        recommendation = self._extract_recommendation(narrative)

        return {
            "recommendation": recommendation,
            "narrative": narrative,
            "tokens_used": len(prompt.split()) + len(narrative.split())
        }
```

## Модель стоимости

```python
COST_MODEL = {
    "режим": "Batch (GPT-4-turbo, май 2025)",

    "токены_на_клиента": {
        "input": 1500,   # профиль клиента + правила + история
        "output": 500,   # нарратив объяснения
        "total": 2000
    },

    "стоимость": {
        "за_клиента": "$0.02",
        "1000_клиентов": "$20",
        "100K_клиентов": "$2,000",
        "1M_клиентов": "$20,000 в неделю"
    },

    "оптимизации": {
        "threshold_filtering": "LLM только для ML-скор > 0.7 → 70% экономии",
        "caching": "Одинаковые профили → кэш нарративов",
        "smaller_model": "GPT-4o-mini: $0.002/клиент vs $0.02 (10x дешевле)",
        "self_hosted": "Qwen 7B локально: ~$0.0002/клиент (100x дешевле)"
    },

    "ROI": {
        "экономия_времени": "10-15 мин → 2-3 мин на кейс",
        "аналитиков": "Те же аналитики закрывают в 4-5x больше кейсов",
        "false_positive_rate": "Снижение за счёт лучшего контекста"
    }
}

# Реальный пример нарратива (из статьи)
EXAMPLE_NARRATIVE = """
Клиент сменил устройство в нетипичное время (03:47), 
одновременно с изменением геолокации на Екатеринбург при обычной 
Москве. Перевод 850 000 руб. новому получателю превышает 
среднемесячный оборот клиента в 8 раз. Комбинация трёх аномалий 
(device + geo + velocity) соответствует классическому паттерну 
компрометации учётной записи. Рекомендую: запросить подтверждение 
через альтернативный канал перед исполнением.
"""
```

## Архитектура пайплайна

```python
class AFAMLPipeline:
    """
    Полный пайплайн: Rules → ML → LLM → Analyst.
    LLM — третий уровень, не первый.
    """

    def process_transaction(self, tx: dict) -> dict:
        # Уровень 1: Детерминированные правила (мгновенно)
        rule_result = self.rule_engine.check(tx)
        if rule_result.is_clear:
            return {"action": "PASS", "reason": "rules_clear"}

        # Уровень 2: ML-скоринг (< 100ms)
        ml_score = self.ml_model.score(tx)
        if ml_score < 0.5:
            return {"action": "PASS", "reason": "low_ml_score"}

        # Уровень 3: LLM-нарратив (только для высокорисковых)
        profile = self.profile_builder.build(tx, rule_result, ml_score)
        llm_output = self.llm_advisor.hybrid_score(profile)

        # Уровень 4: Аналитик видит полную картину
        return {
            "action": "REVIEW",
            "ml_score": ml_score,
            "rule_triggers": rule_result.triggered_rules,
            "llm_narrative": llm_output["narrative"],
            "llm_recommendation": llm_output["recommendation"]
        }
```

## Применение к Lorenzo

```python
# Lorenzo: LLM как объяснитель результатов поиска

class LorenzoExplainedSearch:
    """
    daniilmaibe паттерн для Lorenzo:
    После BM25/TF-IDF поиска — LLM объясняет ПОЧЕМУ результат релевантен.
    Аналог: ML-скор + LLM-нарратив для аналитика.
    """

    def search_with_explanation(self, query: str) -> list[dict]:
        results = self.bm25.search(query, top_k=5)

        for result in results:
            if result["score"] > 0.5:  # только для релевантных
                result["explanation"] = self.llm.explain(
                    f"Почему документ '{result['title']}' релевантен "
                    f"запросу '{query}'? Кратко, 1-2 предложения."
                )
        return results
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **AML LLM + Privacy Gateway (R41)** | PII-прокси перед LLM-анализом транзакций: клиентские данные не покидают контур |
| **AML LLM + Kaspersky MCP (R40)** | Codegen анализ паттернов мошенничества в больших объёмах транзакций |
| **AML LLM + LangFuse (R38)** | Трейсинг каждого LLM-объяснения: стоимость, токены, accuracy по обратной связи |
| **AML LLM + Sequential (R38)** | Панель LLM-аналитиков обсуждает сложный кейс мошенничества без координатора |
| **AML LLM + Structured Output (R40)** | Instructor + Pydantic: гарантированный JSON с recommendation + narrative + confidence |

## Контакт

- Статья: https://habr.com/ru/articles/908424/ (май 2025)
- Смежная (VTB SHAP для AML/скоринга): https://habr.com/ru/companies/vtb/articles/938988/
- Смежная (Finam FinBench LLM финансы): https://habr.com/ru/companies/finam_broker/articles/989842/
- FATF рекомендации: fatf-gafi.org

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
