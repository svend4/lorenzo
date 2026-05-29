---
date: 2026-05-29
tags: [memory, rag, orchestration, ingestion, local-first]
state: normalized
---

# YandexGPT Acceleration: DMC KV-cache 3.5×, SpinQuant W4A4 2.7×, EAGLE Speculative Decoding

<!-- toc-auto -->
<!-- tags: roman-gorb-yandex-llm-acceleration-speculative-dmc-kvcache, docs -->


<!-- summary -->
> `roman-gorb-yandex-llm-acceleration-speculative-dmc-kvcache` — раздел документации проекта Lorenzo.


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Автор:** roman-gorb (Яндекс, команда YandexGPT inference)  
**Хабр:** https://habr.com/ru/companies/yandex/articles/878230/  
**GitHub:** ссылки на arXiv paper'ы в статье  
**Слой:** knowledge / ingestion  
**Дата:** февраль 2025  
**Уникальность:** Production-опыт команды YandexGPT: 5 категорий ускорения inference с реальными цифрами. DMC (Dynamic Memory Compression) — runtime сжатие KV-cache 4× → 3.5× throughput без изменения весов. SpinQuant W4A4 через rotation matrices — 2.7× speedup. EAGLE tree-based speculative decoding. Ragged tensor batching для multi-turn +10%. Не квантование весов для размера (R52 re9ulus) — throughput engineering при инференсе.

## 5 категорий ускорения LLM Inference

```
Проблема: LLM inference bottlenecks при production scale

Два режима inference:
  Prefill: обработать prompt (parallel, compute-bound)
  Decode:  генерировать токены (sequential, memory-bound)

Decode — главное узкое место:
  → Каждый токен = один forward pass
  → KV-cache растёт с длиной контекста
  → Memory bandwidth становится bottleneck

YandexGPT опыт: 5 направлений оптимизации
  1. Knowledge Distillation (качество меньшей модели)
  2. Weight Quantization (размер → скорость)
  3. KV-cache Compression (DMC → runtime throughput)
  4. Speculative Decoding (EAGLE → decode speedup)
  5. Batching Optimization (ragged tensors → efficiency)
```

## Детали 5 методов ускорения

```python
# roman-gorb (Yandex): LLM Acceleration Production Methods
# habr.com/ru/companies/yandex/articles/878230/

from dataclasses import dataclass
import numpy as np

@dataclass
class InferenceBenchmark:
    """Результаты метода ускорения."""
    method: str
    throughput_multiplier: float  # × vs FP16 baseline
    latency_multiplier: float     # <1.0 = быстрее
    memory_reduction: float       # × vs baseline
    quality_impact: str


# ===== МЕТОД 1: Knowledge Distillation =====

class SpeculativeKnowledgeDistillation:
    """
    On-Policy Distillation — обучать student на ответах teacher при инференсе.

    Обычная дистилляция (offline):
      Teacher генерирует датасет → student обучается на нём
      Проблема: distribution shift (student видит другие токены чем teacher)

    On-Policy дистилляция:
      Student генерирует токены → teacher оценивает → KL divergence loss
      → Student обучается на своём распределении, не teacher's
      → Лучше качество, меньше hallucinations

    Speculative Knowledge Distillation:
      Student используется как draft model для teacher (speculative decoding)
      → Обучение и ускорение inference объединены
    """

    DISTILLATION_VARIANTS = [
        "Hard-label (стандартная): student учится предсказывать argmax(teacher)",
        "Soft-label (SLIM): student учится распределению вероятностей teacher",
        "On-Policy: student генерирует, teacher корректирует",
        "Speculative KD: student = draft model в speculative decoding"
    ]


# ===== МЕТОД 2: Weight Quantization (новые форматы) =====

class FP8Quantization:
    """
    FP8 (E4M3): 8-битный floating point с 4 битами экспоненты.

    Vs INT8:
    INT8: [0, 255] равномерно → плохо для малых значений
    FP8 E4M3: сохраняет floating point динамический диапазон
    → Лучше для активаций, меньше деградация качества

    Поддержка: H100/H800 (hardware FP8), A100 (эмуляция)
    Throughput: ×1.4 vs FP16 на A100
    """
    BENCHMARK = InferenceBenchmark(
        method="FP8 E4M3", throughput_multiplier=1.4,
        latency_multiplier=0.7, memory_reduction=2.0,
        quality_impact="минимальная (FP8 сохраняет динамический диапазон)"
    )


class SpinQuantW4A4:
    """
    SpinQuant W4A4: квантование весов И активаций до 4 бит через rotation matrices.

    Проблема W4A4 (vs W4A16 GPTQ):
    Квантовать активации до 4 бит → outliers разрушают качество
    (та же проблема что LLM.Int8, но хуже при 4 битах)

    SpinQuant решение: rotation matrices R
    X_rotated = X @ R  → распределение стабилизируется
    Outliers исчезают в rotated пространстве → 4 бит OK

    R = случайные orthogonal матрицы (Hadamard family)
    R вычисляются OFFLINE → нет overhead при инференсе
    Квантование в rotated space → dequantize перед computations

    Результат: W4A4KV4 (веса+активации+KV-cache в 4 бит) → 2.7× speedup
    """

    BENCHMARK = InferenceBenchmark(
        method="SpinQuant W4A4KV4", throughput_multiplier=2.7,
        latency_multiplier=0.37, memory_reduction=4.0,
        quality_impact="умеренная (rotation компенсирует outlier проблему)"
    )

    def apply_rotation(self,
                        activations: np.ndarray,
                        R: np.ndarray) -> np.ndarray:
        """
        Применить rotation matrix для стабилизации активаций.
        R — orthogonal matrix (R^T R = I)
        """
        return activations @ R  # rotate → quantize → dequantize → rotate back


# ===== МЕТОД 3: DMC — Dynamic Memory Compression =====

class DynamicMemoryCompression:
    """
    DMC: runtime сжатие KV-cache без изменения весов модели.

    Ключевое отличие от weight quantization (R52):
    Weight quantization: изменить веса модели (offline, один раз)
    DMC: сжимать KV-cache во ВРЕМЯ декодирования (online, каждый токен)

    Идея:
    Не все токены в KV-cache одинаково важны для будущих предсказаний.
    Older tokens → можно объединить (merge) в более компактное представление.
    → KV-cache растёт медленнее с длиной контекста

    DMC алгоритм:
    При каждом decode шаге:
    1. Выбрать "mergeable" token pairs (низкая attention entropy)
    2. Объединить их KV представления (weighted average)
    3. Освободить слоты → cache остаётся компактным

    Нет изменений весов модели! Fine-tune только merge policy.
    """

    def merge_kv_cache(self,
                        keys: np.ndarray,
                        values: np.ndarray,
                        attention_scores: np.ndarray,
                        compression_ratio: float = 2.0) -> tuple:
        """
        DMC: объединить наименее важные KV пары.

        compression_ratio: 2.0 = вдвое меньше KV entries
        """
        seq_len = keys.shape[1]
        target_len = int(seq_len / compression_ratio)

        # Найти токены с низкой attention важностью → кандидаты для merge
        importance = attention_scores.mean(axis=0)  # mean across heads
        merge_candidates = np.argsort(importance)[:seq_len - target_len]

        # Объединить соседние merge candidates
        new_keys = self._merge_pairs(keys, merge_candidates)
        new_values = self._merge_pairs(values, merge_candidates)

        return new_keys, new_values

    BENCHMARK_2X = InferenceBenchmark(
        method="DMC 2× compression", throughput_multiplier=2.0,
        latency_multiplier=0.5, memory_reduction=2.0,
        quality_impact="небольшая (merge низкоэнтропийных токенов)"
    )
    BENCHMARK_4X = InferenceBenchmark(
        method="DMC 4× compression", throughput_multiplier=3.5,
        latency_multiplier=0.29, memory_reduction=4.0,
        quality_impact="умеренная (aggressive compression)"
    )


# ===== МЕТОД 4: EAGLE Speculative Decoding =====

class EAGLESpeculativeDecoding:
    """
    EAGLE (Extrapolation Algorithm for Greater Language-model Efficiency):
    Tree-based speculative decoding для ускорения decode фазы.

    Обычный speculative decoding:
      Draft model → k токенов → Target model верифицирует все k
      → Параллельная верификация: k+1 токенов за ~1 forward pass target
      Проблема: если draft неточен → reject → 1 токен за pass (хуже baseline)

    EAGLE tree-based:
      Draft model → ДЕРЕВО возможных токенов (не цепочку)
      → Target верифицирует дерево параллельно
      → При rejection: другая ветка дерева часто принимается
      → Более высокий acceptance rate → больше speedup

    Драфт-модель EAGLE:
    Маленький autoregressive head поверх hidden states target модели
    → Predicts next token distribution from target's hidden state
    → Очень точный draft → высокий acceptance rate
    """

    def draft_tree(self,
                    hidden_states: np.ndarray,
                    beam_width: int = 4,
                    depth: int = 3) -> dict:
        """
        Построить дерево кандидатов из hidden states target модели.

        beam_width: ширина дерева (токенов на уровень)
        depth: глубина (сколько токенов заглядываем вперёд)
        Итого: beam_width^depth кандидатных путей
        """
        tree = {"root": hidden_states, "children": []}

        for d in range(depth):
            candidates = self.eagle_head.predict_top_k(
                hidden_states, k=beam_width
            )
            tree["children"].extend(candidates)

        return tree


# ===== МЕТОД 5: Ragged Tensor Batching =====

class RaggedTensorBatching:
    """
    Ragged tensors для эффективного multi-turn батчинга.

    Проблема padding в multi-turn диалогах:
    Запрос 1: 50 токенов history + 10 новых = 60 токенов
    Запрос 2: 200 токенов history + 15 новых = 215 токенов
    → Padding запроса 1 до 215 → 73% вычислений на padding!

    Ragged tensors:
    → Батч из запросов разной длины БЕЗ padding
    → GPU kernel поддерживает irregular shapes
    → ~10% throughput improvement для multi-turn workloads

    Реализация в FlashAttention 2+ и cuBLAS sparse
    """

    BENCHMARK = InferenceBenchmark(
        method="Ragged Tensor Batching", throughput_multiplier=1.10,
        latency_multiplier=0.91, memory_reduction=1.2,
        quality_impact="нет (только batching optimization)"
    )


COMBINED_RESULTS = {
    "FP8_quantization": "×1.4 throughput",
    "SpinQuant_W4A4KV4": "×2.7 generation speedup",
    "DMC_2x_compression": "×2.0 throughput",
    "DMC_4x_compression": "×3.5 throughput",
    "ragged_batching": "+~10% multi-turn",
    "base_platform": "YandexGPT production, LLaMA-family architectures",
    "hardware": "A100 80GB (основной бенчмарк)"
}
```

## Применение к Lorenzo

```python
# Lorenzo: выбор метода ускорения для gateway.py inference

class LorenzoInferenceOptimizer:
    """
    roman-gorb паттерн для Lorenzo:
    Выбор метода ускорения под конкретные задачи Lorenzo.

    Задача "быстрые short ответы" (improve_llm_qa.py):
    → SpinQuant W4A4 или GPTQ INT4 → максимальная скорость

    Задача "длинные документы" (improve_llm_summary.py):
    → DMC 4× compression → KV-cache не переполняется на 100K+ токенах

    Задача "multi-turn" (gateway.py /api/ask):
    → Ragged tensor batching → -73% overhead от padding

    Задача "fine-tuning embedder" (R50 huraligne):
    → QLoRA NF4 → файн-тюн на 1 GPU

    Decision tree Lorenzo inference:
    context_len > 50K → DMC
    latency_critical → SpinQuant W4A4
    finetuning_needed → QLoRA
    default → FP8 + Ragged
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **YandexGPT Accel + Quantization Deep Dive (R52)** | re9ulus: теория квантования (GPTQ/QLoRA); roman-gorb: production практика (SpinQuant + DMC) — теория + практика |
| **YandexGPT Accel + Self-hosted 4×4090 (R49)** | Выбор метода ускорения под 4×RTX 4090: DMC для длинных контекстов + SpinQuant для throughput |
| **YandexGPT Accel + RAG Embedder Fine-Tuning (R50)** | On-Policy Distillation для embedder + DMC при retrieval inference |
| **YandexGPT Accel + GBNF Constrained Decoding (R49)** | EAGLE speculative + XGrammar grammar: ускоренная генерация с гарантированной структурой |
| **YandexGPT Accel + LLM Observability (R45)** | Трейсинг: latency breakdown по фазам (prefill/decode/KV-compression) в production |

## Контакт

- Статья: https://habr.com/ru/companies/yandex/articles/878230/ (февраль 2025)
- Автор: roman-gorb (Яндекс, команда YandexGPT inference)
- DMC: arxiv.org/abs/2405.00524
- EAGLE: arxiv.org/abs/2401.15077
- SpinQuant: arxiv.org/abs/2405.16406
- FlashAttention: github.com/Dao-AILab/flash-attention
- Смежная (Quantization Deep Dive, R52): docs/06-discovery/round-52/projects/re9ulus-yandex-llm-quantization-deep-dive-gptq-qlora.md
- Смежная (Self-hosted 4×4090, R49): docs/06-discovery/round-49/projects/dmitrii-chashchin-self-hosted-4x4090-vllm-parallelism.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
