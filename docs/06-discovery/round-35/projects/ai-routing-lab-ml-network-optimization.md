---
date: 2026-05-29
tags: [orchestration, ingestion, architecture, self-improve, collaboration]
state: normalized
---

# AI Routing Lab: ML для оптимизации сетевых маршрутов

<!-- toc-auto -->
<!-- tags: ai-routing-lab-ml-network-optimization, docs -->


<!-- summary -->
> AI Routing Lab: ML для оптимизации сетевых маршрутов — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** maxorik (Максим Ланиес), CloudBridge Research  
**Хабр:** https://habr.com/ru/articles/970630/  
**GitHub:** https://github.com/cloudbridge-research/ai-routing-lab  
**Слой:** analytics / orchestration  
**Дата:** ноябрь 2025  
**Уникальность:** Редкий open-source NetOps ML стек на Хабре с реальным GitHub: Random Forest для прогнозирования RTT/jitter за 5-10 минут (MAE 3.2 мс, R²=0.94) + Q-Learning + Multi-Armed Bandit (UCB) + Isolation Forest для аномалий + GPT-4o как AI агент. Интеграция с Prometheus телеметрией. 196 unit-тестов, 71.73% покрытие.

## Проблема: BGP не видит будущего

```
BGP (Border Gateway Protocol) — стандарт маршрутизации интернета:
  → Метрики: hop count, AS path, local preference
  → НЕ знает: текущую задержку, джиттер, потери пакетов
  → Реакция на деградацию: ПОСЛЕ того как она случилась

Симптом в production:
  Видеозвонок / биржевая транзакция / стриминг
  → Путь A: 40 мс (нормально) → внезапно 150 мс (конгестия)
  → BGP не переключается → деградация 2-5 минут до реакции

Решение AI Routing Lab:
  → ML предсказывает деградацию за 5-10 минут
  → Превентивное переключение до начала проблемы
  → R²=0.94 → предсказание с точностью MAE 3.2 мс
```

## Архитектура: несколько ML подходов в одном стеке

```python
# AI Routing Lab: github.com/cloudbridge-research/ai-routing-lab
# Несколько алгоритмов для разных аспектов маршрутизации

from ai_routing_lab import (
    LatencyPredictor,
    JitterPredictor,
    QLearningRouter,
    MultiArmedBanditRouter,
    AnomalyDetector
)

class AIRoutingStack:
    """
    Слой 1: Prediction (Random Forest)
      → предсказание RTT и jitter за 5-10 мин вперёд

    Слой 2: Decision (Q-Learning / MAB)
      → выбор оптимального пути на основе прогноза

    Слой 3: Anomaly Detection (Isolation Forest)
      → выявление аномальных паттернов трафика

    Слой 4: AI Agent (GPT-4o via CAI Framework)
      → объяснение решений, лабораторные задания
    """

    def __init__(self):
        self.latency_predictor = LatencyPredictor()
        self.jitter_predictor = JitterPredictor()
        self.router = QLearningRouter(n_paths=4)
        self.bandit = MultiArmedBanditRouter(algorithm="ucb")
        self.anomaly_detector = AnomalyDetector()

    def predict_and_route(self, current_metrics: dict) -> dict:
        # Предсказать метрики через 5-10 минут
        predicted_latency = self.latency_predictor.predict(
            current_metrics, horizon=5  # минут
        )
        predicted_jitter = self.jitter_predictor.predict(
            current_metrics, horizon=5
        )

        # Выбрать путь на основе прогноза
        path = self.router.select_path(
            predicted_latency=predicted_latency,
            predicted_jitter=predicted_jitter,
            available_paths=current_metrics["paths"]
        )

        # Детектировать аномалии
        is_anomaly = self.anomaly_detector.predict(current_metrics)

        return {
            "selected_path": path,
            "predicted_latency_ms": predicted_latency,
            "predicted_jitter_ms": predicted_jitter,
            "anomaly_detected": is_anomaly
        }
```

## Random Forest для предсказания задержки

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

class LatencyPredictor:
    """
    Фичи: временные паттерны сетевых метрик.
    Цель: предсказать RTT через N минут.
    MAE: 3.2 мс | R²: 0.94 (из статьи)
    """

    FEATURES = [
        # Текущие метрики
        "current_rtt_ms",
        "current_packet_loss_pct",
        "current_bandwidth_mbps",
        "current_jitter_ms",

        # Скользящие средние (temporal features)
        "rtt_ma_5min",      # среднее за 5 минут
        "rtt_ma_15min",     # среднее за 15 минут
        "rtt_std_5min",     # стандартное отклонение (волатильность)

        # Паттерны конгестии
        "congestion_indicator",  # 0/1
        "path_utilization_pct",  # загрузка канала

        # Временные фичи (time-of-day patterns)
        "hour_of_day",
        "day_of_week",
        "is_business_hours"
    ]

    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )

    def train(self, df: pd.DataFrame):
        X = df[self.FEATURES]
        y = df["rtt_ms_in_5min"]  # целевая переменная
        self.model.fit(X, y)

    def predict(self, current_metrics: dict, horizon: int = 5) -> float:
        features = self._extract_features(current_metrics)
        return float(self.model.predict([features])[0])

    def evaluate(self, X_test, y_test) -> dict:
        y_pred = self.model.predict(X_test)
        return {
            "mae_ms": mean_absolute_error(y_test, y_pred),  # ~3.2 ms
            "r2": r2_score(y_test, y_pred),                 # ~0.94
            "feature_importance": dict(zip(
                self.FEATURES,
                self.model.feature_importances_
            ))
        }
```

## Q-Learning для выбора маршрута

```python
import numpy as np

class QLearningRouter:
    """
    Q-Learning для адаптивного выбора пути.
    State: (predicted_latency_bucket, predicted_jitter_bucket)
    Action: выбор пути (0..N-1)
    Reward: -latency -jitter + bandwidth_bonus
    """

    def __init__(self, n_paths: int = 4, n_states: int = 10):
        # Q-table: states × actions
        self.q_table = np.zeros((n_states, n_states, n_paths))
        self.n_paths = n_paths
        self.alpha = 0.1   # learning rate
        self.gamma = 0.95  # discount factor
        self.epsilon = 0.1  # exploration rate

    def select_path(self, predicted_latency: float,
                    predicted_jitter: float,
                    available_paths: list) -> int:
        state = self._discretize_state(predicted_latency, predicted_jitter)

        # ε-greedy exploration
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_paths)
        else:
            return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        # Bellman equation
        current_q = self.q_table[state][action]
        next_max_q = np.max(self.q_table[next_state])
        new_q = current_q + self.alpha * (
            reward + self.gamma * next_max_q - current_q
        )
        self.q_table[state][action] = new_q

    def _compute_reward(self, actual_latency: float,
                        actual_jitter: float,
                        bandwidth: float) -> float:
        return -actual_latency * 0.5 - actual_jitter * 0.3 + bandwidth * 0.2


class MultiArmedBanditRouter:
    """
    UCB (Upper Confidence Bound) для быстрой адаптации.
    Альтернатива Q-Learning для менее стационарных сред.
    """

    def __init__(self, algorithm: str = "ucb", n_arms: int = 4):
        self.counts = np.zeros(n_arms)   # сколько раз выбран путь
        self.rewards = np.zeros(n_arms)  # суммарная награда

    def select_path(self, t: int) -> int:
        # UCB: выбрать путь с наибольшим upper confidence bound
        ucb_values = (self.rewards / (self.counts + 1e-5) +
                      np.sqrt(2 * np.log(t + 1) / (self.counts + 1e-5)))
        return int(np.argmax(ucb_values))
```

## Интеграция с Prometheus телеметрией

```python
from prometheus_client import start_http_server, Gauge
import requests

class NetworkTelemetryCollector:
    """
    Сбор метрик из CloudBridge Relay инфраструктуры.
    Экспорт в Prometheus для мониторинга и обучения ML.
    """

    # Prometheus метрики
    rtt_gauge = Gauge("network_rtt_ms", "RTT по путям", ["path_id"])
    jitter_gauge = Gauge("network_jitter_ms", "Jitter по путям", ["path_id"])
    loss_gauge = Gauge("network_packet_loss_pct", "Потери пакетов", ["path_id"])

    def collect_from_quic_test(self, paths: list) -> dict:
        """
        quic-test: проверка качества путей через QUIC протокол.
        Запускается каждые 30 сек для каждого пути.
        """
        metrics = {}
        for path in paths:
            result = self._run_quic_test(path.endpoint)
            metrics[path.id] = {
                "rtt_ms": result["rtt"],
                "jitter_ms": result["jitter"],
                "packet_loss_pct": result["loss"],
                "bandwidth_mbps": result["bandwidth"]
            }

            # Обновить Prometheus метрики
            self.rtt_gauge.labels(path_id=path.id).set(result["rtt"])
            self.jitter_gauge.labels(path_id=path.id).set(result["jitter"])

        return metrics
```

## GPT-4o как AI агент (CAI Framework)

```python
# CAI Framework: AI агент для объяснения решений и обучения

CAI_AGENT_SYSTEM_PROMPT = """
Ты — сетевой эксперт. Анализируй метрики маршрутизации
и объясняй решения ML системы на понятном языке.

Доступные инструменты:
- get_current_metrics() → текущие RTT/jitter по путям
- get_prediction() → прогноз на 5 минут вперёд
- get_routing_decision() → текущее решение и причины
- explain_anomaly(path_id) → объяснение аномалии
"""

# Использование для образовательных лабораторных работ:
class RoutingLabAgent:
    """
    Студент: "Почему система выбрала путь 2?"
    GPT-4o: "Путь 2 выбран потому что:
             - Текущий RTT пути 1: 45мс → прогноз через 5 мин: 120мс
             - Пути 2 прогноз: 38мс (стабильный)
             - Isolation Forest обнаружил начало конгестии на пути 1"
    """
    pass
```

## Применение к Lorenzo

```python
# Паттерн: ML для предсказания деградации пайплайна Lorenzo

class LorenzoPipelinePredictor:
    """
    Lorenzo запускает 159 скриптов.
    AI Routing Lab паттерн: предсказывать медленные скрипты
    ДО запуска improve_run_all.py
    """

    def predict_slow_scripts(self, history: list) -> list:
        features = self._extract_script_features(history)
        predicted_times = self.rf_model.predict(features)
        slow = [s for s, t in zip(history, predicted_times) if t > 60]
        return slow  # пропустить в --fast режиме
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **AI Routing + Meta-Monitor (R29)** | Meta-Monitor детектирует аномалии → AI Routing переключает трафик |
| **AI Routing + YADRO (R33)** | ML маршрутизация между inference нодами YADRO кластера |
| **AI Routing + Volga Streaming (R28)** | ML предсказание деградации для streaming ML пайплайна |
| **AI Routing + Edge Pi (R34)** | Federated edge: Pi ноды как measurement points для ML routing |
| **AI Routing + Federated Edge (R28)** | Distributed routing decisions at edge nodes |

## Контакт

- Статья: https://habr.com/ru/articles/970630/ (ноябрь 2025)
- GitHub: https://github.com/cloudbridge-research/ai-routing-lab (v0.2.1, MIT)
- Prometheus: prometheus.io
- Смежная (Ростелеком B2B AI): https://habr.com/ru/companies/rostelecom/articles/913828/
- BGP спецификация: RFC 4271

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
