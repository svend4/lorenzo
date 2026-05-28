---
date: 2026-05-28
tags: [memory, rag, security, ingestion, architecture]
state: normalized
---

# Федеративное обучение на Edge-устройствах с ограниченной памятью

<!-- toc-auto -->
<!-- tags: federated-learning-edge-devices, docs -->


<!-- summary -->
> Реальная экспериментальная платформа: Flower (федеративный координатор) + TensorFlow Federated (цифровые двойники) + LiteRT (TF Lite C++ API для on-device inference).


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Александр Лошкарёв (Eltex Enterprise), Oleg Bunin blog, апрель–май 2026  
**Хабр:** https://habr.com/ru/companies/oleg-bunin/articles/1009670/ (часть 1), https://habr.com/ru/companies/oleg-bunin/articles/1009674/ (часть 2)  
**GitHub:** не опубликован (исследовательская платформа Eltex)  
**Слой:** orchestration / memory  
**Дата:** апрель–май 2026  
**Уникальность:** Практическая серия о федеративном обучении в условиях жёсткого ограничения памяти (< 256 МБ RAM). Реальная экспериментальная платформа: Flower (федеративный координатор) + TensorFlow Federated (цифровые двойники) + LiteRT (TF Lite C++ API для on-device inference). ~60% экономия памяти через специфические паттерны обучения. Автор — инженер производителя сетевого оборудования.

## Почему федеративное обучение и почему на edge

```
Классический ML (централизованный):
  Устройство → передать данные → облако → обучить модель → отдать веса

Проблемы:
  ❌ Приватные данные покидают устройство
  ❌ Требует постоянный интернет
  ❌ ФЗ-152: персональные данные не должны покидать Россию
  ❌ Медицина, банки: данные под регуляторными ограничениями

Кейс Eltex (сетевое оборудование):
  Роутер собирает сетевые паттерны → аномалии → угрозы безопасности
  НО: логи сети клиента = конфиденциальные данные
  РЕШЕНИЕ: обучать модель прямо на роутере, передавать только веса

Федеративное обучение:
  Устройство → обучить локально → передать ТОЛЬКО веса → сервер агрегирует
  → Данные НИКОГДА не покидают устройство
```

## Архитектура: Flower + TF Federated + LiteRT

```python
# Flower: координатор федеративного обучения

import flwr as fl

class EdgeDeviceClient(fl.client.NumPyClient):
    """Запускается на каждом edge-устройстве (роутере/камере/сенсоре)"""

    def __init__(self, device_id: str, local_data_path: str):
        self.model = load_model("anomaly_detector.tflite")
        self.data = load_local_data(local_data_path)
        # Данные НИКОГДА не уходят с устройства

    def get_parameters(self, config):
        """Отдать текущие веса серверу"""
        return self.model.get_weights()

    def fit(self, parameters, config):
        """Обучить на локальных данных с весами от сервера"""
        self.model.set_weights(parameters)

        # Локальное обучение (только локальные данные!)
        history = self.model.fit(
            self.data.X,
            self.data.y,
            epochs=config.get("local_epochs", 3),
            batch_size=config.get("batch_size", 16),
            verbose=0
        )

        return self.model.get_weights(), len(self.data), {
            "loss": history.history["loss"][-1]
        }
        # Возвращаем: обновлённые веса + кол-во примеров + метрика
        # НЕ ДАННЫЕ! Только веса.

    def evaluate(self, parameters, config):
        """Оценить глобальную модель на локальных данных"""
        self.model.set_weights(parameters)
        loss, accuracy = self.model.evaluate(self.data.X_val, self.data.y_val)
        return loss, len(self.data.X_val), {"accuracy": accuracy}


# Сервер: агрегирует веса от всех устройств
class FederatedServer:
    def start(self, min_clients: int = 10):
        strategy = fl.server.strategy.FedAvg(
            min_fit_clients=min_clients,
            min_available_clients=min_clients,
            # Взвешенное среднее: устройства с больше данных = больше вес
            fit_metrics_aggregation_fn=weighted_average
        )
        fl.server.start_server(
            server_address="0.0.0.0:8080",
            config=fl.server.ServerConfig(num_rounds=10),
            strategy=strategy
        )
```

## Проблема памяти: < 256 МБ RAM

```python
# Edge устройство (роутер Eltex): 256 МБ total RAM
# ОС + сервисы: ~180 МБ
# Доступно для ML: ~76 МБ

# LiteRT (TF Lite C++ API): минимальный runtime
import tflite_runtime.interpreter as tflite

class EdgeMLRuntime:
    def __init__(self, model_path: str, memory_limit_mb: int = 50):
        self.interpreter = tflite.Interpreter(
            model_path=model_path,
            experimental_preserve_all_tensors=False,  # экономия памяти
        )
        self.interpreter.allocate_tensors()
        # LiteRT: ~5-15 МБ runtime vs TensorFlow ~500 МБ

    def infer(self, input_data: np.ndarray) -> np.ndarray:
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        self.interpreter.set_tensor(input_details[0]['index'], input_data)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(output_details[0]['index'])


# Паттерны экономии памяти при обучении:

MEMORY_OPTIMIZATION_PATTERNS = {
    "gradient_checkpointing": {
        "описание": "Пересчитывать активации при backprop вместо хранения",
        "экономия": "~50% памяти активаций",
        "компромисс": "+30% вычислений"
    },
    "micro_batching": {
        "описание": "batch_size=1-4 вместо 32-128",
        "экономия": "линейно: batch/4 → память/4",
        "компромисс": "медленнее сходимость"
    },
    "quantization_aware_training": {
        "описание": "Обучать в int8 вместо float32",
        "экономия": "4× меньше памяти весов",
        "компромисс": "-0.5-2% точность (обычно приемлемо)"
    },
    "layer_freezing": {
        "описание": "Обновлять только последние N слоёв",
        "экономия": "пропорционально замороженным слоям",
        "компромисс": "медленнее адаптация к новым паттернам"
    }
}

# Результат Eltex: комбинация всех 4 паттернов → ~60% экономия памяти
```

## Secure Aggregation: приватность при передаче весов

```python
# Проблема: веса тоже могут содержать информацию об обучающих данных
# (атаки model inversion, membership inference)

class SecureAggregation:
    """
    Веса суммируются на сервере не в открытом виде
    Сервер видит только агрегат, не индивидуальные веса
    """

    def aggregate_with_noise(self,
                              client_updates: list[np.ndarray]) -> np.ndarray:
        # Дифференциальная приватность: добавить шум Гаусса
        aggregated = np.mean(client_updates, axis=0)

        # Шум пропорционален чувствительности и бюджету приватности
        noise = np.random.normal(
            0,
            scale=self.sensitivity / self.epsilon,
            size=aggregated.shape
        )
        return aggregated + noise

        # epsilon (ε): чем меньше → больше приватность, меньше точность
        # Типичные значения: ε = 1-10 для ML задач
```

## Цифровые двойники через TF Federated

```python
# TF Federated: симуляция федеративного обучения без реальных устройств

import tensorflow_federated as tff

# Создать "цифровые двойники" реальных устройств для тестирования

def create_digital_twins(n_devices: int = 100):
    """
    Каждый цифровой двойник = симуляция edge-устройства
    с реалистичными данными и ограничениями памяти
    """
    return [
        tff.simulation.datasets.ClientData.from_clients_and_fn(
            client_ids=[f"device_{i}"],
            create_tf_dataset_for_client_fn=lambda id: generate_device_data(id)
        )
        for i in range(n_devices)
    ]

# Преимущество: отлаживать федеративный пайплайн без 100 физических роутеров
# → затем деплоить на реальные устройства (LiteRT API совместим с TF Federated)
```

## Применение к Lorenzo

Федеративный паттерн → **Распределённое Lorenzo без централизации**:

```python
# improve_federated_index.py (паттерн):
# Если Lorenzo — community platform, каждый участник = edge node

class FederatedLorenzoNode:
    """
    Каждый участник Svyazi = node с локальными данными
    Глобальный индекс строится федеративно
    """

    def compute_local_embeddings(self) -> LocalUpdate:
        """
        Участник обрабатывает свои документы локально
        Отдаёт только агрегированные TF-IDF веса, не тексты
        """
        local_docs = self.load_private_docs()
        local_tfidf = self.fit_tfidf(local_docs)

        # Передаём не тексты, только веса модели
        return LocalUpdate(
            tfidf_weights=local_tfidf.get_feature_weights(),
            n_docs=len(local_docs)
        )

    def federated_merge(self, updates: list[LocalUpdate]) -> GlobalIndex:
        """FedAvg: взвешенное среднее весов всех участников"""
        return weighted_average(updates, weight_fn=lambda u: u.n_docs)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Federated + LLM Privacy (R24)** | Полный privacy stack: FL на edge + Privacy Gateway для cloud запросов |
| **Federated + Jay Guard (R21)** | Анонимизация ДО отправки весов серверу = двойная защита |
| **Federated + AIOps (R24)** | Каждый сервер обучает аномалии локально → FedAvg → глобальная модель |
| **Federated + Fine-tuning (R24)** | LoRA адаптеры на каждом edge → федеративный merge адаптеров |
| **Federated + Self-hosted (R22)** | Self-hosted координатор Flower + on-premise edge = полный суверенитет |

## Контакт

- Статья (ч.1): https://habr.com/ru/companies/oleg-bunin/articles/1009670/ (апрель 2026)
- Статья (ч.2): https://habr.com/ru/companies/oleg-bunin/articles/1009674/ (май 2026)
- Flower (федеративный фреймворк): flower.ai, github.com/adap/flower (Apache 2.0)
- TensorFlow Federated: tensorflow.org/federated
- LiteRT (TF Lite): ai.google.dev/edge/litert
- Eltex Enterprise: eltex-co.ru

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
