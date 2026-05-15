# Self-hosted LLM на 4× RTX 4090 с водяным охлаждением: реплицированный vs tensor parallelism

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Автор:** Dmitrii-Chashchin (Дмитрий Чащин, компания BVM)  
**Хабр:** https://habr.com/ru/articles/1032698/  
**GitHub:** нет (production кейс для клиента)  
**Слой:** orchestration  
**Дата:** май 2026  
**Уникальность:** Детальный enterprise hardware кейс: on-premise LLM-сервер на 4× RTX 4090 (96 GB VRAM суммарно) с водяным охлаждением под нагрузку 10 000+ звонков/месяц. Ключевой вывод: на PCIe 4.0 без NvLink режим replicated×4 в 9.6× быстрее tensor parallelism (TP=4). Llama 3.1 8B replicated = 18 564 t/s; Qwen3.5 122B TP=4 = 440 t/s при TTFT 110ms. Энергопотребление пик 2 200-2 500W; рекомендуют лимитировать карты на 10-20% для production.

## Проблема: облако дорого, а железо нужно правильно собрать

```
Задача клиента:
  → Анализ звонков колл-центра: 10 000+ звонков в месяц
  → Транскрипция + суммаризация + извлечение метаданных
  → Данные конфиденциальны → облако исключено
  → Нужен on-premise сервер с достаточной производительностью

Почему не облако:
  → AWS/Azure LLM inference: $0.01-0.10 за 1K токенов
  → 10K звонков × 5K токенов = $500-5000/мес → $6K-60K/год
  → Стоимость сервера: ~$30K → окупается за 1-2 года
  → Полный контроль данных (GDPR, 152-ФЗ)

Выбор GPU:
  → A100 80GB: $30K+/штука → бюджет не позволяет
  → RTX 4090 24GB: $2K/штука → 4 карты = $8K в VRAM
  → NvLink: только у A/H-серии → карты общаются через PCIe
  → Ключевой вопрос: как эффективно распределить нагрузку?
```

## Архитектура сервера и водяное охлаждение

```python
# Dmitrii-Chashchin (BVM): production self-hosted LLM на 4× RTX 4090
# habr.com/ru/articles/1032698/

from dataclasses import dataclass

@dataclass
class ServerSpec:
    """Спецификация production LLM-сервера."""
    # CPU
    cpu: str = "AMD Ryzen Threadripper PRO 5975WX"
    cpu_cores: int = 32
    ram_gb: int = 256
    ram_type: str = "DDR4 ECC"

    # GPU
    gpu_model: str = "NVIDIA RTX 4090"
    gpu_count: int = 4
    gpu_vram_each_gb: int = 24
    gpu_vram_total_gb: int = 96  # 4 × 24

    # Охлаждение
    cooling: str = "водяное"
    cooling_components: list = None  # 2 помпы, 2 радиатора
    gpu_temp_under_load_c: tuple = (29, 38)  # диапазон под нагрузкой

    # Питание
    psu_w: int = 3000
    peak_consumption_w: tuple = (2200, 2500)
    typical_load_w: int = 1693

    # Хранилище
    nvme_tb: int = 4


SERVER = ServerSpec()

COOLING_NOTES = {
    "проблема_воздушного": (
        "4× RTX 4090 в closed case → воздушное охлаждение не справляется "
        "при длительной нагрузке. GPU 83-90°C → throttling → деградация производительности."
    ),
    "водяное_решение": (
        "EK Water Blocks для каждой карты + 2 помпы + 2 радиатора 360mm. "
        "Результат: GPU 29-38°C под полной нагрузкой (vs 83-90°C воздух). "
        "Никакого throttling."
    ),
    "рекомендация_продакшн": (
        "Для 24/7 нагрузки: Power Limit на 10-20% ниже TDP. "
        "RTX 4090 TDP = 450W → лимит 360-400W. "
        "Потеря производительности: ~5-10%. Выигрыш: стабильность + срок службы."
    )
}
```

## Replicated vs Tensor Parallelism: ключевой вывод

```python
class VLLMDeploymentModes:
    """
    Два режима распределения нагрузки на 4× GPU без NvLink.

    Режим 1: Replicated (4 копии модели, каждая на 1 GPU)
    Режим 2: Tensor Parallelism TP=4 (модель разрезана на 4 GPU)

    Контринтуитивный результат:
    На PCIe 4.0 (без NvLink) replicated БЫСТРЕЕ TP в 9.6 раза
    для малых и средних моделей.

    Почему: NvLink = 600 GB/s между GPU
            PCIe 4.0 x16 = 64 GB/s между GPU (в 9.4 раза медленнее)
    TP требует постоянной синхронизации между GPU при каждом attention layer →
    на медленном PCIe это доминирующий bottleneck.
    """

    BENCHMARK_RESULTS = {
        "hardware": "4× RTX 4090, PCIe 4.0 (без NvLink)",
        "software": "Ubuntu 24.04.1 + vLLM",

        "models": {
            "Llama_3.1_8B": {
                "replicated_x4": {
                    "throughput_tps": 18564,
                    "mode": "4 копии модели, каждая на 1 GPU",
                    "fits_in_vram": True  # 8B ≈ 16GB fp16 → влезает в 24GB
                },
                "tp_4": {
                    "throughput_tps": 1930,  # примерно, из сравнения
                    "mode": "модель разрезана на 4 GPU",
                    "overhead": "PCIe bottleneck"
                },
                "speedup_replicated_vs_tp": 9.6
            },

            "Gemma_4_E4B": {
                "replicated_x4": {
                    "throughput_tps": 21429,
                    "note": "MoE модель: активированы только E4B параметры из 27B"
                }
            },

            "Qwen3_122B": {
                "tp_4": {
                    "throughput_tps": 440,
                    "ttft_ms": 110,
                    "mode": "единственный вариант — не влезает в 24GB × 1"
                },
                "note": "122B модель ТРЕБУЕТ TP — не влезает ни на одну GPU"
            }
        },

        "вывод": (
            "Правило выбора режима:\n"
            "Модель влезает в 1 GPU VRAM → replicated (копии на каждой GPU)\n"
            "Модель НЕ влезает в 1 GPU → tensor parallelism (разрезать на N GPU)\n"
            "На PCIe без NvLink: replicated даёт 9.6× больше throughput"
        )
    }

    def choose_deployment_mode(self,
                                model_size_gb: float,
                                gpu_vram_gb: int = 24,
                                gpu_count: int = 4) -> dict:
        """
        Выбрать оптимальный режим развёртывания.
        """
        fits_in_one_gpu = model_size_gb <= gpu_vram_gb * 0.85  # 15% overhead

        if fits_in_one_gpu:
            return {
                "mode": "replicated",
                "replicas": gpu_count,
                "config": {
                    "tensor_parallel_size": 1,
                    "pipeline_parallel_size": 1,
                    "num_replicas": gpu_count
                },
                "reason": f"Модель {model_size_gb:.1f}GB влезает в {gpu_vram_gb}GB VRAM"
            }
        else:
            # Минимальное число GPU для TP
            min_gpus = -(-int(model_size_gb / (gpu_vram_gb * 0.85)) // 1)
            tp_size = min(min_gpus, gpu_count)
            return {
                "mode": "tensor_parallel",
                "tensor_parallel_size": tp_size,
                "config": {
                    "tensor_parallel_size": tp_size,
                    "pipeline_parallel_size": 1
                },
                "reason": f"Модель {model_size_gb:.1f}GB не влезает в {gpu_vram_gb}GB"
            }
```

## vLLM Production Конфигурация

```python
VLLM_PRODUCTION_CONFIG = """
# Запуск vLLM для production на 4× RTX 4090

# Режим replicated (для моделей ≤20GB): максимальный throughput
python -m vllm.entrypoints.openai.api_server \\
    --model Llama-3.1-8B-Instruct \\
    --tensor-parallel-size 1 \\
    --gpu-memory-utilization 0.90 \\
    --max-model-len 8192 \\
    --served-model-name llama-3.1-8b

# Запустить 4 копии на портах 8000-8003, балансировать через nginx

# Режим TP=4 (для моделей >60GB): максимальный размер модели  
python -m vllm.entrypoints.openai.api_server \\
    --model Qwen3-122B-Instruct \\
    --tensor-parallel-size 4 \\
    --gpu-memory-utilization 0.95 \\
    --max-model-len 4096 \\
    --served-model-name qwen3-122b
"""

POWER_MANAGEMENT = {
    "проблема": "2200-2500W пик → дорогое электричество + нагрев помещения",
    "решение": "nvidia-smi -pl <power_limit> для каждой карты",
    "рекомендация": {
        "rtx_4090_tdp_w": 450,
        "production_limit_w": 370,  # 82% от TDP
        "потеря_производительности_%": 8,
        "команда": "nvidia-smi -i 0,1,2,3 -pl 370"
    },
    "годовое_электричество": {
        "без_лимита_kwh_год": 15768,   # 1800W * 8760h
        "с_лимитом_kwh_год": 12994,    # 1483W * 8760h
        "экономия_kwh_год": 2774,
        "экономия_рублей": "~16K руб/год (при 6 руб/kWh)"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: self-hosted рекомендация для development

class LorenzoSelfHostedRecommendation:
    """
    Dmitrii-Chashchin паттерн для Lorenzo:
    При рекомендации self-hosted LLM для Svyazi 2.0 — учитывать
    режим развёртывания в зависимости от целевой модели.

    Для мелких задач Lorenzo (improve_*.py, gateway.py):
    1× RTX 3090/4090 24GB → Llama 3.1 8B → replicated не нужен

    Для production Svyazi RAG:
    4× RTX 4090 replicated → 18K t/s → обслуживает тысячи запросов/день
    """

    def recommend_for_use_case(self, use_case: str) -> dict:
        """Рекомендовать конфигурацию под задачу."""
        configs = {
            "development": {"gpu": "1× RTX 4090", "model": "Llama 3.1 8B"},
            "production_rag": {"gpu": "4× RTX 4090 replicated", "model": "Llama 3.1 8B"},
            "large_context": {"gpu": "4× RTX 4090 TP=4", "model": "Qwen3 122B"}
        }
        return configs.get(use_case, configs["development"])
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Self-hosted 4090 + vLLM inference (R32)** | 4×RTX 4090 + vLLM оптимизации: PagedAttention + continuous batching → максимальная утилизация 96GB |
| **Self-hosted 4090 + SENTINEL (R47)** | On-premise SENTINEL перед on-premise LLM = полностью изолированный security stack |
| **Self-hosted 4090 + Telecom Classifier (R46)** | Qwen2.5-0.5B классификатор + 18K t/s throughput = on-premise обработка тысяч запросов в секунду |
| **Self-hosted 4090 + LLM Code Review (R47)** | 4×RTX 4090 replicated → параллельные Codeqwen ревью для нескольких MR одновременно |
| **Self-hosted 4090 + AQLM.rs (R46)** | 2-bit quantization AQLM → Llama 3.1 8B 16GB→2.5GB → на 1 карте помещается 9 реплик |

## Контакт

- Статья: https://habr.com/ru/articles/1032698/ (май 2026)
- Автор: Dmitrii-Chashchin (Дмитрий Чащин, BVM)
- vLLM: docs.vllm.ai
- EK Water Blocks: ekwb.com (водяное охлаждение GPU)
- nvidia-smi power limit: nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-documentation/nvidia-smi-guide.pdf
- Смежная (vLLM inference opt, R32): docs/06-discovery/round-32/
- Смежная (Private LLM стек, R24): docs/06-discovery/round-24/
- Смежная (AQLM.rs браузер, R46): docs/06-discovery/round-46/projects/yandex-aqlm-rs-llm-browser-wasm-2bit.md
