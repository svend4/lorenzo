---
date: 2026-06-05
tags: [memory, rag, orchestration, ingestion, architecture]
state: normalized
---

# Kaspersky MLAD: цифровой двойник ICS + LLM как компрессор данных

<!-- toc-auto -->
<!-- tags: kaspersky-mlad-digital-twin-ics-llm-compression, docs -->


<!-- summary -->
> `kaspersky-mlad-digital-twin-ics-llm-compression` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Friflex_dev (Вадим Кондаратцев, Friflex)  
**Хабр:** https://habr.com/ru/amp/publications/1014940/  
**GitHub:** нет (материал конференции CrossConf 2025)  
**Слой:** analytics / orchestration  
**Дата:** март 2026  
**Уникальность:** Расширенная публикация доклада CrossConf 2025 по синтетическим данным для промышленного ML. Центральный кейс: Kaspersky MLAD — цифровой двойник АСУ ТП в Dymola/MATLAB Simulink моделирует физику (теплообмен, гидродинамика, химкинетика) и генерирует физически точные временны́е ряды (температура, давление, расход с ПЛК) для обучения детекторов аномалий без реальных данных атак. Второй паттерн: LLM как универсальный компрессор — дообученные LLM достигают 4000x сжатия бинарных сенсорных данных для edge-развёртывания.

## Проблема: в промышленных системах нет данных об атаках

```
Задача: обнаружение аномалий в ICS/АСУ ТП
  → Нужно обучить ML-модель на примерах атак и сбоев
  → Проблема: в нормальной работе атак нет (это хорошо!)
  → Реальные атаки: Stuxnet, Industroyer — единичны, непубличны
  → Ручная разметка "нормально/аномалия" на гигабайтах ПЛК-данных:
    дорого, требует экспертов, субъективно

Kaspersky MLAD решение:
  → Цифровой двойник в Dymola + MATLAB Simulink
  → Модель физики: теплообменник, насосы, реакторы
  → Генерация сценариев: нормальная работа + инъекция атак
  → 100% размеченные синтетические данные без реальных инцидентов
  → Выявляет: целевые кибератаки + человеческие ошибки (открытый вентиль)
```

## Цифровой двойник АСУ ТП: генерация синтетики

```python
# Kaspersky MLAD: digital twin для ICS anomaly detection
# Friflex (CrossConf 2025 extended write-up)

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class PhysicalProcess:
    """Физический процесс в модели цифрового двойника."""
    name: str           # "heat_exchanger", "pump_system", "chemical_reactor"
    equations: str      # Dymola/Modelica уравнения (физика)
    variables: list[str]  # температура, давление, расход, уровень
    plc_signals: list[str]  # сигналы с ПЛК (имитация реальных датчиков)


class KasperskyMLADDigitalTwin:
    """
    Цифровой двойник промышленной системы.
    Инструменты: Dymola (симуляция) + MATLAB Simulink (управление).

    Физические модели:
    - Теплообмен: уравнение теплопроводности, конвекция
    - Гидродинамика: уравнение Бернулли, потери давления
    - Химическая кинетика: реакционные уравнения
    """

    SIMULATED_PROCESSES = [
        PhysicalProcess(
            name="heat_exchanger",
            equations="dT/dt = (Q_in - Q_out) / (m * Cp)",
            variables=["temperature_in", "temperature_out",
                       "flow_rate", "heat_transfer_coeff"],
            plc_signals=["TT101", "TT102", "FT201", "PT301"]
        ),
        PhysicalProcess(
            name="centrifugal_pump",
            equations="H = f(Q, n)  # насосная характеристика",
            variables=["pressure_in", "pressure_out",
                       "flow_rate", "rpm", "power"],
            plc_signals=["PT401", "PT402", "FT501", "ST601"]
        )
    ]

    def generate_normal_operation(self, duration_hours: int = 720) -> dict:
        """
        Симуляция нормальной работы (30 дней).
        Результат: временны́е ряды значений датчиков без аномалий.
        """
        timestamps = np.arange(0, duration_hours * 3600, 1)  # каждую секунду
        data = {}

        for process in self.SIMULATED_PROCESSES:
            for signal in process.plc_signals:
                # Физически точное значение + шум датчика
                nominal = self._compute_nominal(signal, timestamps)
                noise = np.random.normal(0, self._sensor_noise(signal),
                                          len(timestamps))
                data[signal] = nominal + noise

        return {"timestamps": timestamps, "signals": data, "label": "NORMAL"}

    def inject_attack_scenario(self,
                                normal_data: dict,
                                attack_type: str,
                                start_time: int) -> dict:
        """
        Инъекция атаки в синтетические данные.
        attack_type: "sensor_spoofing" | "valve_manipulation" | "dos"
        """
        attacked_data = normal_data.copy()

        if attack_type == "sensor_spoofing":
            # Attacker подделывает показания температуры
            target_signal = "TT101"
            attacked_data["signals"][target_signal][start_time:] = \
                normal_data["signals"][target_signal][start_time] * 0.9  # стабильный ложный сигнал

        elif attack_type == "valve_manipulation":
            # Открытый вентиль → скачок расхода
            target_signal = "FT201"
            attacked_data["signals"][target_signal][start_time:start_time + 300] *= 3.5

        attacked_data["label"] = f"ATTACK_{attack_type}"
        attacked_data["attack_start"] = start_time
        return attacked_data

    def generate_training_dataset(self,
                                   n_normal: int = 1000,
                                   n_attacks: int = 500) -> list[dict]:
        """
        Генерация размеченного датасета без единого реального инцидента.
        100% recall на классах атак т.к. сами генерируем метки.
        """
        dataset = []

        # Нормальные сценарии
        for _ in range(n_normal):
            dataset.append(self.generate_normal_operation(duration_hours=24))

        # Атаки (разные типы и моменты начала)
        attack_types = ["sensor_spoofing", "valve_manipulation", "dos"]
        for _ in range(n_attacks):
            normal = self.generate_normal_operation(duration_hours=24)
            attack_type = np.random.choice(attack_types)
            start = np.random.randint(3600, 20 * 3600)
            dataset.append(self.inject_attack_scenario(normal, attack_type, start))

        return dataset
```

## LLM как универсальный компрессор сенсорных данных

```python
class LLMDataCompressor:
    """
    Паттерн: LLM as compressor (DeepMind 2023: "Language Modeling Is Compression").

    Идея: дообученный LLM = модель распределения данных.
    Arithmetric coding с LLM как prior → сжатие лучше gzip/bzip2.

    Применение в промышленности:
    - Edge-устройства: хранить дни данных датчиков в малой памяти
    - Передача: 4000x меньше трафика с завода в облако
    - Dual-use: та же LLM = аномалия-детектор (high perplexity = аномалия)
    """

    COMPRESSION_BENCHMARK = {
        "dataset": "Бинарные данные ПЛК-сигналов (температура, давление)",
        "baseline_gzip": "10x сжатие",
        "baseline_bzip2": "15x сжатие",
        "llm_compressor": "4000x сжатие (fine-tuned LLM)",
        "source": "DeepMind 'Language Modeling Is Compression', Delétang et al. 2023"
    }

    def compress_sensor_stream(self, sensor_values: list[float],
                                llm_model) -> bytes:
        """
        Arithmetic coding с LLM как prior:
        1. LLM предсказывает следующее значение → распределение вероятностей
        2. Arithmetic coder кодирует реальное значение через это распределение
        3. Чем лучше LLM предсказывает → меньше битов нужно

        Формально: compressed_length ≈ -log2(P_LLM(actual_value))
        """
        compressed_bits = []
        for i, value in enumerate(sensor_values):
            # LLM предсказывает распределение следующего значения
            context = sensor_values[max(0, i-100):i]
            prob_distribution = llm_model.predict_next(context)

            # Arithmetic coding
            bits = self._arithmetic_encode(value, prob_distribution)
            compressed_bits.extend(bits)

        return bytes(compressed_bits)

    def detect_anomaly_via_perplexity(self, sensor_window: list[float],
                                       llm_model,
                                       threshold: float = 100.0) -> bool:
        """
        Dual-use: тот же LLM для детекции аномалий.
        Высокая perplexity = LLM не ожидал этих значений = аномалия.

        Threshold: настраивается по нормальным данным (95 перцентиль).
        """
        perplexity = llm_model.compute_perplexity(sensor_window)
        return perplexity > threshold


MLAD_PROFILE = {
    "продукт": "Kaspersky MLAD (Machine Learning for Anomaly Detection)",
    "назначение": "Обнаружение аномалий в промышленных системах (ICS/АСУ ТП)",

    "технология_двойника": {
        "инструменты": ["Dymola", "MATLAB Simulink"],
        "физические_модели": ["теплообмен", "гидродинамика", "химкинетика"],
        "выход": "размеченные временны́е ряды сигналов ПЛК"
    },

    "обнаруживает": [
        "Целевые кибератаки (подмена сигналов, манипуляция клапанами)",
        "Человеческие ошибки (открытый вентиль, загрязнённые датчики)",
        "Оборудованные сбои (деградация насоса, утечка теплоносителя)"
    ],

    "llm_как_компрессор": {
        "degree": "4000x",
        "применение": "Edge-развёртывание с малой памятью",
        "dual_use": "Та же модель = детектор аномалий через perplexity"
    },

    "статус": "Коммерческий продукт Kaspersky (не open-source)"
}
```

## Применение к Lorenzo

```python
# Lorenzo: цифровой двойник паттерн для тестирования скриптов

class LorenzoDigitalTwinTesting:
    """
    Kaspersky MLAD паттерн для Lorenzo:
    Вместо реальных production данных — синтетический корпус
    для тестирования improve_*.py скриптов.

    Аналог: synthetic данные атак → synthetic деградировавшие docs/
    для тестирования quality скриптов.
    """

    def generate_degraded_corpus(self,
                                  degradation_type: str) -> list[dict]:
        """
        Синтетическая "деградация" документов для тестирования.
        degradation_type: "broken_links" | "missing_sections" | "duplicate_content"
        """
        normal_docs = self.read_docs("/home/user/lorenzo/docs")
        degraded = []

        for doc in normal_docs:
            if degradation_type == "broken_links":
                degraded.append(self._inject_broken_links(doc))
            elif degradation_type == "missing_sections":
                degraded.append(self._remove_random_section(doc))
            elif degradation_type == "duplicate_content":
                degraded.append(self._duplicate_paragraph(doc))

        return degraded

    def validate_script(self, script_name: str,
                         degradation_type: str) -> dict:
        """
        Запустить скрипт на синтетически деградированном корпусе.
        Убедиться что скрипт находит проблему.
        """
        degraded = self.generate_degraded_corpus(degradation_type)
        result = self.run_script(script_name, degraded)
        return {
            "detected": result["issues_found"] > 0,
            "precision": result["true_positives"] / result["total_found"],
            "recall": result["true_positives"] / len(degraded)
        }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **MLAD + Kaspersky MCP (R40)** | Цифровой двойник генерирует данные → MCP-агент анализирует через codegen |
| **MLAD + LangFuse (R38)** | Трейсинг perplexity-детекции: когда LLM-компрессор видит аномалию |
| **MLAD + Agent Distillation (R39)** | Дистилляция трасс MLAD-агента в компактную edge-модель |
| **MLAD + Stryker Testing (R39)** | Mutation testing для детектора аномалий: что если инъекция невидима? |
| **MLAD + SherlockOps (R42)** | SherlockOps расследует аномалию обнаруженную MLAD → RCA в Slack |

## Контакт

- Статья: https://habr.com/ru/amp/publications/1014940/ (март 2026)
- Kaspersky MLAD: kaspersky.ru/enterprise-security/industrial
- CrossConf 2025: crossconf.ru
- DeepMind "Language Modeling Is Compression": arxiv.org/abs/2309.10668
- Dymola: 3ds.com/products/catia/dymola
- Смежная (цифровые двойники гибридные, Zhurakhovskii): https://habr.com/ru/articles/1030824/
- Смежная (предиктивное обслуживание ML, Jet Infosystems R41): https://habr.com/ru/companies/jetinfosystems/articles/761984/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
