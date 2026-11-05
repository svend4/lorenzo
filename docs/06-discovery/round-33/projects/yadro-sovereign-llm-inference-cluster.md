---
date: 2026-06-05
tags: [memory, rag, security, knowledge, architecture]
state: normalized
---

# Где живут LLM: суверенный инференс-кластер YADRO

<!-- toc-auto -->
<!-- tags: yadro-sovereign-llm-inference-cluster, docs -->


<!-- summary -->
> Провальная миграция с Triton на vLLM → затем с LiteLLM на vLLM Production Stack (экспоненциальный overhead при нагрузке).


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** jet-47 (Владислав Виноградов), YADRO (Хабр, июль 2025)  
**Хабр:** https://habr.com/ru/companies/yadro/articles/930304/  
**GitHub:** не опубликован (ссылки на vllm-project/vllm, philschmid/mt-bench)  
**Слой:** orchestration  
**Дата:** июль 2025  
**Уникальность:** Честный production-отчёт от российского производителя IT-оборудования: vLLM на RTX 4090 + H100 в собственном кластере (данные не покидают контур). Провальная миграция с Triton на vLLM → затем с LiteLLM на vLLM Production Stack (экспоненциальный overhead при нагрузке). T-pro-it-1.0 vs глобальные модели на русском языке. FP8 + tensor parallelism.

## Зачем YADRO нужен суверенный LLM inference

```
YADRO — российский производитель серверов и СХД.
Запросы сотрудников содержат:
  → Техническую документацию (конкурентные секреты)
  → Контракты и финансовую информацию
  → Данные клиентов (персональные данные по 152-ФЗ)

OpenAI/Anthropic API → данные уходят за рубеж → НЕТ.
Решение: собственный inference кластер внутри периметра.

Дополнительный мотив: у YADRO есть свои GPU серверы.
Цель: показать клиентам что на своём железе это работает.
```

## Hardware: RTX 4090 vs H100 в production

```python
HARDWARE_COMPARISON = {
    "RTX 4090": {
        "VRAM": "24 GB GDDR6X",
        "назначение": "некритичные модели (7B-13B)",
        "autoscaling": "горизонтальное (GPU load based)",
        "стоимость": "~$1600 за карту (потребительская)",
        "ограничения": [
            "NVLink нет (GPU isolated)",
            "ECC нет → потенциальные ошибки памяти в production",
            "Одна карта = одна модель (нет tensor parallelism между картами)"
        ],
        "подходит_для": "вспомогательные задачи, малые модели"
    },
    "H100": {
        "VRAM": "80 GB HBM3",
        "назначение": "latency-sensitive критичные модели (70B+)",
        "autoscaling": "статичные инстансы (нельзя быстро стартовать)",
        "стоимость": "~$30K за карту",
        "преимущества": [
            "NVLink: tensor parallelism между картами",
            "ECC: надёжность в production",
            "FP8: аппаратное ускорение"
        ],
        "подходит_для": "production-grade 70B+ модели"
    }
}

# Архитектурное решение:
# RTX 4090 → Kubernetes + HPA (horizontal pod autoscaler по GPU load)
# H100 → статичный deployment (минимум 2 реплики для availability)
```

## Эволюция стека: три итерации

```python
STACK_EVOLUTION = {
    "Итерация 1: Triton Inference Server": {
        "период": "2024 Q1-Q2",
        "плюсы": ["NVIDIA native", "низкая latency для батчей"],
        "проблемы": [
            "Сложная настройка (model repository, config.pbtxt)",
            "Плохая поддержка LLM-специфических оптимизаций",
            "Нет prefix caching из коробки",
            "Много ручной работы для каждой модели"
        ],
        "итог": "❌ Отказались"
    },

    "Итерация 2: vLLM + LiteLLM Proxy": {
        "период": "2024 Q3 - 2025 Q1",
        "плюсы": [
            "OpenAI-совместимый API",
            "Простой routing между моделями",
            "Access control через LiteLLM"
        ],
        "проблемы": [
            "LiteLLM: экспоненциальный overhead при concurrent нагрузке",
            "50+ concurrent users → LiteLLM становится bottleneck",
            "Внутренний state LiteLLM = проблемы при рестарте"
        ],
        "итог": "⚠️ Работало, но не масштабировалось"
    },

    "Итерация 3: vLLM Production Stack": {
        "период": "2025 Q2+",
        "плюсы": [
            "Kubernetes-native (Helm chart)",
            "Нативный load balancing без LiteLLM overhead",
            "Встроенный router с prefix caching",
            "Горизонтальное масштабирование",
        ],
        "итог": "✅ Текущее решение"
    }
}
```

## vLLM Production Stack: конфигурация

```yaml
# Kubernetes Helm values для YADRO inference cluster

# vllm-production-stack/values.yaml
servingEngineSpec:
  modelSpec:
    - name: "t-pro-it-1.0"         # Российская модель
      repository: "yadro-registry/t-pro-it"
      tag: "1.0"
      replicaCount: 2
      resources:
        limits:
          nvidia.com/gpu: 1        # RTX 4090, одна карта
      vllmConfig:
        maxModelLen: 32768
        enablePrefixCaching: true
        kvCacheDtype: "fp8"        # экономия VRAM

    - name: "qwen2.5-72b"          # Мощная открытая модель
      repository: "yadro-registry/qwen"
      replicaCount: 1              # статичный (H100)
      resources:
        limits:
          nvidia.com/gpu: 2        # 2× H100, tensor parallel
      vllmConfig:
        tensorParallelSize: 2
        maxModelLen: 131072
        enablePrefixCaching: true
        quantization: "fp8"

routerSpec:
  # Маршрутизация по модели + prefix caching на уровне router
  prefixCacheEnabled: true
  loadBalancing: "session_affinity"  # sticky routing для prefix cache
```

## FP8 + Tensor Parallelism для H100

```python
# FP8 dynamic quantization + tensor parallelism

INFERENCE_OPTIMIZATIONS = {
    "FP8_dynamic": {
        "что": "weights + KV-cache в FP8 (8-bit floating point)",
        "как": "vLLM: --quantization fp8 --kv-cache-dtype fp8",
        "результат_VRAM": "70B модель: 140GB BF16 → 70GB FP8 (~2x)",
        "результат_quality": "-1-3% на бенчмарках (приемлемо)",
        "нужно": "H100 (аппаратная поддержка FP8)"
    },

    "tensor_parallelism": {
        "что": "модель разделена между GPU через NVLink",
        "как": "--tensor-parallel-size 2 (для 2× H100)",
        "результат": "70B модель на 2× H100 (80GB) vs 1× H100 (80GB) невозможно",
        "overhead": "NVLink коммуникации ~5-10% от compute"
    },

    "prefix_caching": {
        "что": "KV-cache для общих system prompt",
        "эффект_в_YADRO": "корпоративный system prompt = один для всех",
        "TTFT_speedup": "~60-70% для повторяющихся промптов"
    }
}
```

## T-pro-it-1.0: российская модель в production

```python
# Benchmarking: T-pro-it-1.0 vs глобальные модели на RU задачах

RUSSIAN_MODEL_BENCHMARK = {
    "benchmark": "MT-Bench адаптированный для RU (philschmid/mt-bench)",
    "задачи": ["рассуждение", "знание", "кодирование", "математика"],

    "результаты": {
        "T-pro-it-1.0 (13B)": {
            "ru_reasoning": 7.2,
            "ru_knowledge": 7.8,  # ← преимущество на RU-специфичных вопросах
            "coding": 6.1,
            "math": 6.5
        },
        "Llama-3.1-8B-Instruct": {
            "ru_reasoning": 6.8,
            "ru_knowledge": 6.2,  # ← слабее на RU-специфике
            "coding": 6.9,
            "math": 7.1
        },
        "Qwen2.5-14B": {
            "ru_reasoning": 7.5,
            "ru_knowledge": 7.3,
            "coding": 8.0,  # ← лучше в коде
            "math": 8.2
        }
    },

    "вывод": (
        "T-pro-it-1.0 выигрывает на RU-специфичных задачах "
        "(законодательство, история РФ, российские реалии). "
        "Qwen2.5 лучше в коде и математике."
    ),

    "производственный_выбор": {
        "корпоративный_ассистент": "T-pro-it-1.0 (RU задачи)",
        "code_assistant": "Qwen2.5-72B",
        "математика": "Qwen2.5-72B"
    }
}
```

## Lessons Learned: честный производственный опыт

```python
YADRO_LESSONS = [
    {
        "урок": "LiteLLM не масштабируется при concurrent нагрузке",
        "симптом": "50+ concurrent req → latency растёт экспоненциально",
        "решение": "vLLM Production Stack (нативный K8s router)"
    },
    {
        "урок": "RTX 4090 → не для production-критичных LLM",
        "симптом": "нет ECC, нет NVLink → memory errors под нагрузкой",
        "решение": "RTX 4090 только для некритичных/dev задач"
    },
    {
        "урок": "FP8 на H100 = обязателен для 70B+ моделей",
        "симптом": "без FP8: 70B не влезает на 2×80GB (нужно 4×80GB)",
        "решение": "fp8 quantization → помещается на 2×80GB"
    },
    {
        "урок": "Российские модели лучше на RU-специфике",
        "симптом": "GPT-4 путается в российском законодательстве",
        "решение": "T-pro-it-1.0 для бизнес-задач, Qwen для кода"
    }
]
```

## Применение к Lorenzo

```python
# Если Lorenzo нужен локальный LLM endpoint:

LORENZO_SOVEREIGN_CONFIG = {
    "модель": "T-pro-it-1.0 или Qwen2.5-7B-Instruct",
    "runtime": "vLLM Production Stack",
    "endpoint": "http://localhost:8000/v1",
    "совместимость": "OpenAI API (все improve_llm_*.py без изменений)",
    "приватность": "данные не покидают машину"
}
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **YADRO + vLLM R32** | YADRO = production case для vLLM Production Stack (R32 статья) |
| **YADRO + Enterprise RAG (R32)** | Суверенный RAG: BGE-m3 + T-pro-it-1.0 в одном корпоративном контуре |
| **YADRO + DBRM medical (R31)** | Медицинский AI в закрытом контуре: все данные пациентов локально |
| **YADRO + Federated Edge (R28)** | Cluster-edge гибрид: YADRO cluster + edge LiteRT устройства |
| **YADRO + Meta-Monitor (R29)** | Мониторинг GPU утилизации + LLM аномалий в суверенном стеке |

## Контакт

- Статья: https://habr.com/ru/companies/yadro/articles/930304/ (июль 2025)
- YADRO Tech: habr.com/ru/companies/yadro/
- Смежная (Self-hosted AI платформа, GitHub): https://habr.com/ru/articles/973456/
- Смежная (Ollama vs vLLM vs llama.cpp сравнение): https://habr.com/ru/articles/948934/
- vLLM Production Stack: github.com/vllm-project/production-stack
- MT-Bench: github.com/philschmid/mt-bench

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
