---
date: 2026-05-29
tags: [memory, rag, security, knowledge, ingestion]
state: normalized
---

# Нейросети в промышленности: правда о провалах ML на производстве и паттерн «модель-консультант»

<!-- toc-auto -->
<!-- tags: kamil-gr-ml-industry-predictive-maintenance-failures, docs -->


<!-- summary -->
> `kamil-gr-ml-industry-predictive-maintenance-failures` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Kamil_GR (Камиль Гадеев, Timeweb Cloud)  
**Хабр:** https://habr.com/ru/companies/timeweb/articles/995012/  
**GitHub:** нет (кейсы с реального производства)  
**Слой:** analytics  
**Дата:** март 2025  
**Уникальность:** Честный разбор провалов ML в реальной промышленности — почему F1=0.77 на синтетике оказался бесполезным в эксплуатации. Конкретные архитектуры (GRU hidden=64-128, 1D-CNN kernel=3-7, XGBoost n_estimators=200-500) с production-ограничениями. Кейс электродуговой печи: дисбаланс классов 50:1, дрейф сенсоров (+30-80°C за 6 мес.), "тихий саботаж" инженеров. Вводит паттерн "модель-консультант" вместо бинарного решения и параметр порядка Курамото для фазовой синхронизации сенсоров.

## Проблема: ML-модели проходят пилот, но не выживают в эксплуатации

```
Типичная история провала ML на производстве:

  Пилот (лаб. условия):
  → Синтетические данные + реальные (соотношение 1:1)
  → F1 = 0.77 → "отлично, внедряем!"
  → ROC AUC = 0.83 → "модель работает"

  Первые месяцы в эксплуатации:
  → Дисбаланс классов: неисправность 1 раз / 50 нормальных = 50:1
  → Модель научилась говорить "всё хорошо" в 98% случаев → F1 → 0.15
  → Сенсоры дрейфуют: +30-80°C за 6 месяцев → distribution shift
  → Инженеры игнорируют предупреждения ("волк, волк") → "тихий саботаж"

  Корень проблемы:
  → Академический ML оптимизирует метрику на датасете
  → Production ML должен решать реальную задачу (предотвращать поломку)
  → Это принципиально разные вещи
```

## Кейс: электродуговая печь

```python
# Kamil_GR: ML для промышленного предиктивного обслуживания
# habr.com/ru/companies/timeweb/articles/995012/

import numpy as np
from dataclasses import dataclass
from typing import Optional

@dataclass
class SensorReading:
    """Показания промышленного датчика."""
    sensor_id: str
    timestamp: float
    value: float
    unit: str
    calibration_date: float  # unix timestamp последней калибровки


@dataclass
class MaintenanceEvent:
    """Событие технического обслуживания / поломки."""
    equipment_id: str
    event_type: str     # "failure" | "maintenance" | "warning"
    timestamp: float
    description: str
    downtime_hours: float


class ElectricArcFurnaceMonitor:
    """
    Предиктивное обслуживание электродуговой печи (ЭДП).

    Реальные условия кейса:
    - Оборудование: ЭДП для производства стали
    - Данные: 18 сенсоров (ток, напряжение, температура, вибрация)
    - Частота: 1 Гц (1 запись/сек)
    - Период обучения: 2 года исторических данных
    - Дисбаланс: 1 поломка на ~50 нормальных часов работы

    Ключевые проблемы, обнаруженные в production:
    1. Дрейф сенсоров температуры: +30-80°C за 6 месяцев → ложные тревоги
    2. Дисбаланс классов 50:1 → модель "всё норм" выигрывает по accuracy
    3. Коваривное смещение: летние данные ≠ зимним (охлаждение меняется)
    4. "Тихий саботаж": инженеры отключают алерты после 10+ ложных тревог
    """

    def detect_sensor_drift(self,
                             readings: list[SensorReading],
                             window_days: int = 30) -> dict:
        """
        Обнаружить дрейф сенсора за последние N дней.

        Метод: скользящее среднее + CUSUM (CUmulative SUM).
        Если среднее значение сместилось > threshold → сенсор нужно калибровать.

        Это критично: дрейф сенсора выглядит как "аномалия" для ML-модели,
        хотя на самом деле просто прибор "плывёт".
        """
        values = [r.value for r in readings]
        baseline = np.mean(values[:window_days * 24 * 3600])
        recent = np.mean(values[-7 * 24 * 3600:])
        drift = abs(recent - baseline)

        return {
            "sensor_id": readings[0].sensor_id,
            "drift_magnitude": drift,
            "needs_calibration": drift > self._drift_threshold(readings[0].unit),
            "calibration_urgency": "high" if drift > 50 else "medium"
        }
```

## Правильные архитектуры для временных рядов

```python
class IndustrialMLArchitectures:
    """
    Три проверенных архитектуры для промышленных временных рядов.
    Все с конкретными гиперпараметрами из реальных внедрений.
    """

    # Архитектура 1: GRU (лучший баланс точность/скорость)
    GRU_CONFIG = {
        "hidden_size": 64,        # 64-128 — больше → переобучение
        "num_layers": 2,
        "dropout": 0.3,
        "sequence_length": 128,   # ~2 минуты при 1 Гц
        "features": 18,           # число сенсоров
        "training_note": (
            "Важно: нормализация per-sensor, не global. "
            "Иначе температура (400°C) доминирует над током (0.8 А)"
        )
    }

    # Архитектура 2: 1D-CNN (быстрый, хорошо на edge-оборудовании)
    CNN_1D_CONFIG = {
        "filters": [32, 64, 128],
        "kernel_size": 5,         # 3-7 — нечётный для симметрии
        "pooling": "global_average",
        "deployment_note": (
            "Экспортируется в ONNX → работает на промышленном ПЛК "
            "без Python. Inference 2мс → real-time на 1 Гц данных."
        )
    }

    # Архитектура 3: XGBoost на ручных фичах (интерпретируемость для инженеров)
    XGBOOST_CONFIG = {
        "n_estimators": 300,      # 200-500
        "max_depth": 6,
        "learning_rate": 0.05,
        "feature_engineering": [
            "rolling_mean_5min",
            "rolling_std_5min",
            "peak_to_peak_amplitude",
            "zero_crossing_rate",    # для вибро-сигналов
            "spectral_entropy"       # быстрое преобразование Фурье
        ],
        "advantage": (
            "SHAP values → объяснить инженеру ПОЧЕМУ модель дала алерт. "
            "'Вибрация подшипника выросла на 40% за 3 часа' — понятно. "
            "Нейросеть: 'confidence 0.73' — непонятно."
        )
    }

    def handle_class_imbalance(self, X_train, y_train):
        """
        50:1 дисбаланс: 1 поломка на 50 нормальных событий.

        Неправильно: просто обучить → модель говорит "норм" всегда → 98% acc.
        Правильно: комбинация подходов.
        """
        from imblearn.combine import SMOTETomek
        from sklearn.utils.class_weight import compute_sample_weight

        # Вариант 1: SMOTE + Tomek (но: синтетика ≠ реальные поломки)
        sampler = SMOTETomek(sampling_strategy=0.1)  # не 1:1 — перебор!
        X_res, y_res = sampler.fit_resample(X_train, y_train)

        # Вариант 2: class_weight (предпочтительнее для временных рядов)
        weights = compute_sample_weight("balanced", y_train)

        # Вариант 3: threshold tuning (критически важно для производства)
        # Лучше: пропустить поломку редко, чем ложная тревога каждый час
        # optimal_threshold = 0.3 вместо 0.5 → больше recall, меньше precision
        return X_res, y_res, weights
```

## Параметр порядка Курамото: синхронизация сенсоров

```python
import numpy as np

def kuramoto_order_parameter(phases: np.ndarray) -> float:
    """
    Параметр порядка Курамото — мера синхронности осцилляторов.
    r = |1/N * Σ exp(i * θ_k)| ∈ [0, 1]

    r ≈ 1: все осцилляторы синхронизированы (нормальная работа)
    r ≈ 0: хаос, рассинхронизация (предвестник поломки)

    Применение: 18 сенсоров ЭДП — у каждого своя "фаза" колебаний.
    При начале разрушения подшипника сенсоры начинают рассинхронизироваться
    → r падает с 0.85 до 0.4 за несколько часов → алерт.

    Это физически интерпретируемая фича — инженеры понимают смысл.
    """
    N = len(phases)
    order_param = np.abs(np.sum(np.exp(1j * phases))) / N
    return float(order_param)


def extract_sensor_phases(readings: np.ndarray,
                           sampling_rate: float = 1.0) -> np.ndarray:
    """
    Извлечь фазы колебаний сенсоров через Гильберт-преобразование.
    """
    from scipy.signal import hilbert
    phases = np.angle(hilbert(readings, axis=0))
    return phases
```

## Паттерн «Модель-Консультант»: главный вывод статьи

```python
class ModelConsultantPattern:
    """
    Главный архитектурный вывод:
    НЕ "модель принимает решение о техобслуживании"
    А "модель советует инженеру что проверить"

    Проблема бинарного решения:
    → "Модель сказала поломка" → остановка линии → 2 часа простоя
    → Модель ошиблась → инженер злится → "тихий саботаж"
    → После 10 ложных тревог инженер отключает систему навсегда

    Паттерн Консультанта:
    → Модель не "решает", а "рекомендует с объяснением"
    → "Рекомендую проверить подшипник #3: вибрация выросла на 40%,
       исторически 73% таких ситуаций заканчивались поломкой через 8-24 часа"
    → Инженер сам решает — и чувствует контроль
    → Доверие к системе растёт
    """

    def generate_recommendation(self,
                                  equipment_id: str,
                                  sensor_data: dict,
                                  shap_values: np.ndarray,
                                  historical_context: dict) -> dict:
        """
        Рекомендация с объяснением вместо бинарного решения.
        SHAP → объяснение. История → calibrated probability.
        """
        # Топ-3 фактора по SHAP
        top_factors = self._get_top_shap_factors(shap_values)

        return {
            "recommendation": "check_bearing_3",
            "urgency": "within_8_hours",  # не "CRITICAL" — нет паники
            "probability": 0.73,
            "explanation": f"Вибрация вала +40% за 3 часа ({top_factors[0]}). "
                           f"Из {historical_context['similar_cases']} похожих "
                           f"ситуаций {historical_context['failure_rate']*100:.0f}% "
                           f"завершались поломкой в течение 8-24 часов.",
            "suggested_action": "Осмотреть подшипник #3, смазка или замена",
            "confidence_interval": (0.58, 0.84)  # не точечная оценка
        }


PRODUCTION_LESSONS = {
    "главные_провалы": [
        "F1=0.77 на синтетике → 0.15 в проде (дисбаланс 50:1)",
        "Drift сенсоров +30-80°C за 6 мес → ложные тревоги → саботаж",
        "Distribution shift: летние данные ≠ зимним",
        "GigaChat/GPT4 для анализа вибраций → не работает (нет специализации)"
    ],
    "что_работает": [
        "GRU(hidden=64-128) + XGBoost(SHAP) ансамбль",
        "Параметр порядка Курамото как early warning",
        "Threshold tuning (0.3 вместо 0.5) под конкретный cost-benefit",
        "Паттерн Консультанта вместо бинарного алерта",
        "ONNX export → inference на ПЛК без Python"
    ]
}
```

## Применение к Lorenzo

```python
# Lorenzo: паттерн Консультанта для quality scoring скриптов

class LorenzoScriptQualityConsultant:
    """
    Kamil_GR паттерн для Lorenzo:
    Improve_*.py скрипты не "решают" проблему качества,
    а "рекомендуют" что улучшить — с объяснением.

    Аналог дисбаланса 50:1:
    В docs/ большинство файлов ОК → качественная проверка
    должна редко ложно тревожить авторов.

    Аналог дрейфа сенсоров:
    Базовые метрики (читаемость, длина) дрейфуют при росте corpus →
    нужна периодическая рекалибровка порогов.
    """

    def recommend_improvements(self, doc_metrics: dict) -> dict:
        """
        Консультант для docs/: не "файл плохой", а "рекомендую исправить X".
        """
        return {
            "recommendation": "add_code_examples",
            "explanation": "Файл содержит описание, но нет кода. "
                           "По базе знаний, файлы с кодом получают "
                           "на 40% больше обращений в поиске.",
            "urgency": "low",
            "effort_estimate_minutes": 15
        }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Промышленность ML + LLM Observability (R45)** | Трейсинг семантических спанов модели-консультанта: где и почему возникают ложные тревоги |
| **Промышленность ML + SENTINEL (R47)** | SENTINEL защита API предиктивного обслуживания от adversarial входов (манипуляция предсказаниями) |
| **Промышленность ML + Temporal KG (R47)** | История технических событий как темпоральный граф: "что было с подшипником #3 в прошлом году?" |
| **Промышленность ML + LangGraph (R44)** | LangGraph граф: sensor_anomaly → consult_model → explain_shap → notify_engineer → schedule_maintenance |
| **Промышленность ML + SherlockOps (R42)** | SherlockOps для ИТ + Kamil_GR для производства = единый консультант по инцидентам |

## Контакт

- Статья: https://habr.com/ru/companies/timeweb/articles/995012/ (март 2025)
- Автор: Kamil_GR (Камиль Гадеев, Timeweb Cloud)
- SMOTE-Tomek: imbalanced-learn.org
- ONNX Runtime: onnxruntime.ai
- Параметр Курамото: en.wikipedia.org/wiki/Kuramoto_model
- Смежная (Kaspersky MLAD ICS, R43): docs/06-discovery/round-43/projects/kaspersky-mlad-ics-anomaly-digital-twin.md
- Смежная (LLM IoT промышленность, R37): docs/06-discovery/round-37/
- Смежная (SherlockOps SRE, R42): docs/06-discovery/round-42/projects/sherlockops-llm-alert-investigation-devops.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
