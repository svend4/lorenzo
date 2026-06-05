---
date: 2026-06-05
tags: [memory, rag, orchestration, knowledge, architecture]
state: normalized
---

# Sberbank AIOps: ML/AI в системе мониторинга — предотвращение инцидентов

<!-- toc-auto -->
<!-- tags: sberbank-aiops-incident-prevention, docs -->


<!-- summary -->
> Автор: Павел Стёпуро, исполнительный директор ДИТ Сбербанка Хабр: https://habr.com/ru/companies/sberbank/articles/1015336/
Хабр: https://habr.com/ru/companies/sberbank/articles/1015336/  
GitHub: не опубликован (production Sberbank внутренняя система)  
Слой: orchestration / analytics / memory  
Дата: март 202


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Павел Стёпуро, исполнительный директор ДИТ Сбербанка  
**Хабр:** https://habr.com/ru/companies/sberbank/articles/1015336/  
**GitHub:** не опубликован (production Sberbank внутренняя система)  
**Слой:** orchestration / analytics / memory  
**Дата:** март 2026  
**Уникальность:** Production-кейс AIOps от Сбербанка: переход от реактивного реагирования на инциденты к **проактивному предотвращению**. ML-модели предсказывают сбои до их возникновения, анализируют паттерны из десятков тысяч алертов, автоматически коррелируют события. Масштаб: ~50 млн пользователей мобильного приложения.

## Эволюция от реактивного к проактивному мониторингу

```
Поколение 1 (Reactive):
  Инцидент → алерт → дежурный → расследование → исправление
  Проблема: пользователи уже пострадали, время восстановления 30-120 мин

Поколение 2 (Predictive — AIOps):
  Аномалия в метриках → ML предсказывает инцидент → превентивные действия
  Цель: пользователь вообще не замечает проблему

Масштаб Сбербанка:
  10,000+ метрик → ~500K алертов/день → 3% = реальные инциденты
  Проблема: инженер физически не может обработать 500K алертов
```

## Три слоя ML в системе мониторинга

```python
# Слой 1: Anomaly Detection (несупервайзированный)
#   Базовая линия по историческим данным → отклонение = аномалия
#   Алгоритмы: Isolation Forest, LSTM AutoEncoder, Prophet (для seasonal)

class AnomalyDetector:
    def detect(self, metric_stream: TimeSeries) -> list[Anomaly]:
        baseline = self.prophet_model.predict(metric_stream)
        z_score = (metric_stream - baseline.yhat) / baseline.uncertainty

        return [
            Anomaly(timestamp=t, metric=m, severity=abs(z))
            for t, m, z in zip(timestamps, values, z_score)
            if abs(z) > THRESHOLD  # > 3σ = аномалия
        ]

# Слой 2: Incident Prediction (супервайзированный)
#   Обучен на исторических инцидентах: какие паттерны предшествовали?
#   За N минут до инцидента → классификатор говорит "высокий риск"

class IncidentPredictor:
    def predict_risk(self, anomalies: list[Anomaly], timewindow=30) -> float:
        features = self.extract_features(anomalies, timewindow)
        # features: количество аномалий, тип, коррелирующие сервисы, время суток
        return self.xgboost_model.predict_proba(features)[1]  # P(incident)

# Слой 3: Alert Correlation (граф)
#   Десятки тысяч алертов → группировать по причине
#   Root cause analysis: найти один источник за множеством симптомов
class AlertCorrelator:
    def correlate(self, alerts: list[Alert]) -> list[IncidentGroup]:
        # Построить граф: алерт → зависимые сервисы
        # Community detection (Louvain) → группы по общей причине
        graph = self.build_dependency_graph(alerts)
        communities = nx.community.louvain_communities(graph)
        return [IncidentGroup(root_cause=self.find_root(c)) for c in communities]
```

## LLM-слой: объяснение и рекомендации

```python
# ML находит аномалию → LLM объясняет инженеру + предлагает действия

INCIDENT_EXPLAIN_PROMPT = """
Ты — SRE-инженер Сбербанка. Проанализируй ситуацию:

Обнаруженная аномалия:
  Метрика: {metric_name}
  Отклонение: {deviation_pct}% от нормы
  Время: {timestamp}
  Затронутые сервисы: {affected_services}

Похожие прошлые инциденты:
  {similar_incidents_from_kb}  ← RAG из базы знаний инцидентов

Предоставь:
1. Вероятная причина (1-2 предложения)
2. Немедленные действия (конкретные команды)
3. Оценка критичности (P1/P2/P3)
"""

# База знаний: все прошлые инциденты + их RCA → векторная БД
# При новом инциденте: embedding → найти похожие → передать LLM
```

## Auto-Remediation: автоматическое исправление

```
Категории действий по уровню риска:

AUTO (без участия человека):
  → Перезапустить зависший сервис (если P(incident) > 0.95 + retry_count > 3)
  → Масштабировать pod (если CPU > 85% + trend → 100%)
  → Очистить кэш (если cache hit rate < 20%)
  → Переключить трафик на backup node

SUGGEST (предлагает инженеру):
  → Откатить деплой (если аномалия началась N минут после деплоя)
  → Увеличить лимиты БД (если connection pool исчерпан)

ESCALATE (немедленно будит дежурного):
  → P(incident) > 0.99 + затронуто более 3 критических сервисов
  → Паттерн незнаком (нет похожих в KB)
```

## Метрики системы Сбербанка

```
До AIOps:
  MTTR (Mean Time To Resolve): 45 минут среднее
  False Positive Alert Rate: 97% (3% = реальные инциденты из 500K)
  Ночные пробуждения дежурных: 12-15 раз/месяц

После AIOps:
  MTTR: 12 минут (-73%)
  Alert Noise Reduction: -85% (фильтрация ML)
  Предотвращённые инциденты: 35% инцидентов не дошло до пользователей
  Ночные пробуждения: 3-4 раза/месяц (-75%)
```

## Архитектура данных

```
Источники:
  Prometheus metrics → TimeSeries (CPU, RAM, RPS, error rate, latency)
  ELK/Loki logs → события и ошибки
  Jaeger traces → цепочки вызовов
  APM (Application Performance Monitor) → бизнес-метрики

Хранение:
  ClickHouse: метрики (columnar, fast aggregation)
  Elasticsearch: логи + полнотекстовый поиск
  VectorDB (pgvector): embeddings инцидентов для RAG

Pipeline:
  Kafka → [ML Anomaly Detection] → [Incident Predictor] → [LLM Explain] → Alertmanager
```

## Применение к Lorenzo

Lorenzo запускает 159+ скриптов и имеет `audit.db` для всех событий.  
AIOps паттерн = **Scripts Health Monitoring**:

```python
# improve_aiops.py (паттерн):
class LorenzoAIOps:
    def monitor_scripts(self, audit_db: AuditDB) -> list[Anomaly]:
        """Анализировать тренды выполнения скриптов"""
        # Метрики: время выполнения, статус, частота ошибок
        for script in audit_db.get_scripts():
            baseline = audit_db.get_baseline(script, days=30)
            current = audit_db.get_recent(script, hours=24)

            if current.avg_time > baseline.avg_time * 1.5:
                yield Anomaly(f"{script} стал в 1.5× медленнее")
            if current.error_rate > 0.1:  # >10% ошибок
                yield Anomaly(f"{script} падает слишком часто")

    def suggest_fix(self, anomaly: Anomaly) -> str:
        """LLM объясняет и предлагает действия"""
        return llm.explain(anomaly, similar_past=kb.search(anomaly))
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **AIOps + DevOps LLM (R24)** | Custom DevOps-агент + ML-предсказание = исправляет предсказанный инцидент |
| **AIOps + Langfuse (R13)** | Langfuse трейсит LLM-объяснения инцидентов → обратная связь по качеству |
| **AIOps + ADD (R13)** | ADD feedback loop + AIOps: агент оценивает свои предсказания → self-correction |
| **AIOps + RAG Incident (R18)** | Sberbank KB + Agentic RAG: агент сам выбирает стратегию поиска по инцидентам |
| **AIOps + Reasoning LLM (R20)** | Reasoning-модель для сложных корреляций (thinking перед root cause analysis) |

## Контакт

- Статья: https://habr.com/ru/companies/sberbank/articles/1015336/ (март 2026)
- Смежная (Мониторинг ML-систем: 6 лет назад vs сегодня): https://habr.com/ru/articles/692462/
- Prometheus: github.com/prometheus/prometheus (Apache 2.0)
- Grafana: github.com/grafana/grafana (AGPL)
- Kafka: github.com/apache/kafka (Apache 2.0)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
