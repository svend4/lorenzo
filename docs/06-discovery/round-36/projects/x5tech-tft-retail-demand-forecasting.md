---
date: 2026-05-28
tags: [ingestion, architecture, roadmap, anthropic, collaboration]
state: normalized
---

# Temporal Fusion Transformer для прогнозирования спроса в ритейле

<!-- toc-auto -->
<!-- tags: x5tech-tft-retail-demand-forecasting, docs -->


<!-- summary -->
> Автор: mayo889 (Дмитрий Поляков), X5 Tech Хабр: https://habr.com/ru/companies/X5Tech/articles/869750/
Хабр: https://habr.com/ru/companies/X5Tech/articles/869750/  
GitHub: нет (внутренняя разработка Пятёрочка/Перекрёсток)  
Слой: analytics  
Дата: декабрь 2024  
Уникальность: Production TFT для прогнозирова


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** mayo889 (Дмитрий Поляков), X5 Tech  
**Хабр:** https://habr.com/ru/companies/X5Tech/articles/869750/  
**GitHub:** нет (внутренняя разработка Пятёрочка/Перекрёсток)  
**Слой:** analytics  
**Дата:** декабрь 2024  
**Уникальность:** Production TFT для прогнозирования спроса на уровне product-store с 7% улучшением MAPE/WAPE на реальных данных сетей X5 за 6 месяцев. Технически уникален data-leakage-free метод инжекции предсказаний как future covariates через truncated normal distribution. Quantile regression по 17 квантилям. Darts + PyTorch Lightning стек.

## Проблема: классические модели не видят будущих событий

```
Задача: прогноз спроса на product-store уровне
  → Сколько единиц товара X продастся в магазине Y через неделю?
  → Нужно для: заказ поставщикам, управление запасами, минимизация излишков

Проблема классических моделей (SARIMA, Prophet):
  → Нет механизма attention — не видят паттерны далеко в прошлом
  → Scalar output — один прогноз без uncertainty quantification
  → Не используют known future: праздники, акции, расписание поставок

Проблема использования предсказаний как future covariates:
  → Хотим подать: "прогноз базовой модели" как дополнительный признак TFT
  → Но: исторические значения этого признака = предсказания прошлых запусков
  → Проблема: будущие предсказания (target) утекают в features (data leakage!)

Решение:
  → Генерация синтетических исторических значений через truncated normal
  → distribution, имитирующую распределение ошибок базовой модели
```

## Temporal Fusion Transformer: архитектура

```python
# Temporal Fusion Transformer (Lim et al., NeurIPS 2020)
# Реализация через Darts + PyTorch Lightning

from darts import TimeSeries
from darts.models import TFTModel
from darts.dataprocessing.transformers import Scaler
import pytorch_lightning as pl

class RetailTFTModel:
    """
    TFT компоненты (все одновременно):
    1. Variable Selection Networks → выбирают важные признаки
    2. LSTM Encoder-Decoder → sequence encoding
    3. Temporal Self-Attention (multi-head) → долгосрочные паттерны
    4. Gating Mechanisms → пропускать неважные компоненты
    5. Quantile outputs → probabilistic forecasting
    """

    def build_model(self) -> TFTModel:
        return TFTModel(
            input_chunk_length=90,      # история: 90 дней
            output_chunk_length=14,     # горизонт: 2 недели
            hidden_size=128,
            lstm_layers=2,              # dual LSTM
            num_attention_heads=4,      # multi-head attention
            dropout=0.1,
            batch_size=64,
            n_epochs=100,

            # Probabilistic: 17 квантилей
            likelihood=QuantileRegression(
                quantiles=[0.05, 0.1, 0.2, 0.25, 0.3,
                           0.4, 0.5,                    # медиана
                           0.6, 0.7, 0.75, 0.8,
                           0.85, 0.9, 0.95, 0.975,
                           0.99, 0.999]
            ),

            # Признаки
            add_relative_index=True,   # позиция в окне

            optimizer_kwargs={"lr": 1e-3},
            pl_trainer_kwargs={
                "accelerator": "gpu",
                "devices": 1,
                "gradient_clip_val": 0.1
            }
        )
```

## Ключевой паттерн: data-leakage-free future covariates

```python
import numpy as np
from scipy.stats import truncnorm

class FutureCovariateInjector:
    """
    Проблема: подать прогноз базовой модели как future covariate TFT.
    Нужны исторические значения этого признака (для обучения TFT).
    Наивный подход: взять реальные прошлые прогнозы → DATA LEAKAGE!

    Почему leakage:
    В момент t прогноз на t+7 коррелирует с реальным спросом t+7.
    Если дать TFT "прогноз на t+7" как признак при обучении на t+7 →
    TFT видит "прямой ответ" в признаках → переобучение.

    Решение автора:
    Генерировать синтетические исторические прогнозы через truncated
    normal, параметризованную историческими ошибками базовой модели.
    → TFT видит "как бы выглядел прогноз" без утечки реальных значений.
    """

    def generate_synthetic_historical_forecasts(
        self,
        actual_demand: np.ndarray,
        baseline_model_mae: float,
        baseline_model_bias: float = 0.0
    ) -> np.ndarray:
        """
        Симулировать исторические прогнозы базовой модели.

        Параметры truncated normal:
        - mean = actual_demand + bias (базовая модель немного смещена)
        - std = MAE (ошибка равномерно распределена)
        - bounds = [0, ∞] (спрос не может быть отрицательным)
        """
        n = len(actual_demand)
        synthetic_forecasts = np.zeros(n)

        for i in range(n):
            mean = actual_demand[i] + baseline_model_bias
            std = baseline_model_mae

            # Truncated normal: нет отрицательных значений
            a = -mean / std  # нижняя граница в стандартных единицах
            synthetic_forecasts[i] = truncnorm.rvs(
                a=a,
                b=np.inf,
                loc=mean,
                scale=std
            )

        return synthetic_forecasts

    def prepare_covariates(self, ts: TimeSeries,
                           base_model) -> TimeSeries:
        """
        Полный pipeline подготовки future covariates:
        1. Посчитать MAE базовой модели (cross-validation)
        2. Сгенерировать синтетические исторические прогнозы
        3. Для будущих периодов: использовать реальный прогноз модели
        """
        # Исторические ошибки базовой модели
        cv_errors = self._cross_validate(base_model, ts)
        historical_mae = np.mean(np.abs(cv_errors))
        historical_bias = np.mean(cv_errors)

        # Синтетические исторические значения
        synthetic_hist = self.generate_synthetic_historical_forecasts(
            actual_demand=ts.values().flatten(),
            baseline_model_mae=historical_mae,
            baseline_model_bias=historical_bias
        )

        # Future: реальный прогноз модели (нет leakage, это будущее)
        future_forecast = base_model.predict(len(ts), ts)

        # Склеить исторические (синтетические) + будущие (реальные)
        full_covariate = np.concatenate([
            synthetic_hist,
            future_forecast.values().flatten()
        ])

        return TimeSeries.from_values(full_covariate)
```

## Результаты: 7% улучшение MAPE на production данных

```python
# Из статьи: 6 месяцев on Pyaterochka/Perekrestok данных

PRODUCTION_RESULTS = {
    "данные": {
        "сети": "Пятёрочка + Перекрёсток (X5 Group)",
        "период_теста": "6 месяцев",
        "уровень": "product-store (каждый SKU × каждый магазин)",
        "SKU_count": "топ-5000 SKU по обороту"
    },

    "метрики_улучшения_vs_baseline": {
        "MAPE":  "-7.1% (mean absolute percentage error)",
        "WAPE":  "-6.8% (weighted absolute percentage error)",
        "RTO":   "-11.34% (key metric for ordering decisions)",
        # RTO = Retail Trade Optimization — внутренняя метрика X5
    },

    "где_TFT_лучше_всего": {
        "сезонные_товары": "внимание видит прошлогодние паттерны",
        "акционные_товары": "future covariates: плановые акции",
        "новые_магазины": "transfer learning из похожих магазинов"
    },

    "где_TFT_проигрывает": {
        "товары_с_малой_историей": "< 30 дней данных",
        "нерегулярный_спрос": "случайные единичные заказы"
    }
}
```

## Explainability: что влияет на прогноз

```python
from darts.explainability import TFTExplainer

class DemandExplainer:
    """
    TFT имеет встроенную интерпретируемость через attention weights.
    Можно ответить: "Почему модель предсказала рост спроса?"
    """

    def explain_forecast(self, model: TFTModel,
                         series: TimeSeries,
                         horizon: int = 7) -> dict:
        explainer = TFTExplainer(model)
        explanation = explainer.explain(
            foreground_series=series,
            horizons=[horizon]
        )

        return {
            # Какие исторические моменты важны (attention scores)
            "temporal_attention": explanation.get_attention(horizon),

            # Какие признаки важны для прогноза
            "feature_importance": explanation.get_feature_importance(horizon),

            # Пример вывода для менеджера:
            # "Прогноз роста на 23% основан на:
            #  - Аналогичный период прошлого года (+40% вес)
            #  - Плановая акция следующей недели (+35% вес)
            #  - Сезонный паттерн конец месяца (+25% вес)"
        }
```

## Применение к Lorenzo

```python
# Lorenzo отслеживает активность проектов во времени.
# TFT паттерн: предсказывать интерес к темам (temporal patterns)

class LorenzoTopicForecaster:
    """
    Lorenzo накопил 36 раундов × 4 проекта = 144 проекта.
    TFT паттерн: какие темы будут интересны в следующих раундах?
    """

    def forecast_topic_relevance(self, topic: str,
                                 horizon_rounds: int = 5) -> dict:
        # Time series: популярность темы по раундам (упоминания)
        ts = self._build_topic_timeseries(topic)

        # Future covariates: плановые конференции, тренды Хабра
        future_cov = self._get_conference_calendar()

        return self.tft.predict(horizon_rounds, ts, future_covariates=future_cov)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **X5 TFT + Volga Streaming (R28)** | Streaming ML: TFT inference на потоке транзакций в реальном времени |
| **X5 TFT + Meta-Monitor (R29)** | Мониторинг дрейфа распределения спроса → автоматический retraining триггер |
| **X5 TFT + AI Routing (R35)** | TFT предсказывает нагрузку на inference cluster → проактивная маршрутизация |
| **X5 TFT + Synthetic Data (R18)** | Синтетические исторические данные (truncated normal паттерн) для аугментации |
| **X5 TFT + LLM Judge (R28)** | LLM объясняет прогноз TFT менеджеру на естественном языке |

## Контакт

- Статья: https://habr.com/ru/companies/X5Tech/articles/869750/ (декабрь 2024)
- X5 Tech: x5.tech (технологии X5 Group — Пятёрочка, Перекрёсток, Чижик)
- Temporal Fusion Transformer (оригинальная статья): arxiv.org/abs/1912.09363
- Darts: github.com/unit8co/darts
- Смежная (LLM для временных рядов, Raft): https://habr.com/ru/companies/raft/articles/887486/
- Смежная (X5 оптимизация маршрутов E-CUP): https://habr.com/ru/companies/X5Tech/articles/989466/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
