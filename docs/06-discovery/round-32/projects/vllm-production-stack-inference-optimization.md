# vLLM Production Stack: KV-cache, FP8, Speculative Decoding в production

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Mikhail Androsov (@Bambarbrandenburg, Хабр, март 2025)  
**Хабр:** https://habr.com/ru/articles/1016062/  
**GitHub:** https://github.com/vllm-project/vllm + https://github.com/vllm-project/production-stack  
**Слой:** orchestration / ingestion  
**Дата:** март 2025  
**Уникальность:** Практическое руководство по развёртыванию vLLM в production: Kubernetes YAML манифесты, реальные GuideLLM бенчмарки BF16 vs FP8 (~3x снижение памяти KV-cache), LMCache для cross-request reuse. Единственная RU статья 2025 покрывающая весь стек: prefix caching → tensor parallelism → quantization → speculative decoding в связке.

## Проблема: inference в production ≠ inference в ноутбуке

```
Dev-режим (один запрос):
  → latency 2-5 сек → нормально
  → GPU memory: вся под одну сессию

Production (1000+ req/sec):
  → latency должна быть < 500ms (P95)
  → GPU memory: нужно обслуживать 100+ concurrent пользователей
  → Контексты пересекаются: system prompts одинаковые у 90% запросов

Ключевые проблемы:
  → KV-cache = главный потребитель VRAM (до 60% при длинных контекстах)
  → Prefill фаза: медленная для длинных prompts (у всех один system prompt)
  → Decode фаза: медленная при авторегрессии (bottleneck = memory bandwidth)
```

## KV-Cache: prefix caching + chunked prefill

```python
# vLLM настройка для production

from vllm import AsyncLLMEngine, AsyncEngineArgs

engine_args = AsyncEngineArgs(
    model="Qwen/Qwen2.5-72B-Instruct",
    tensor_parallel_size=4,        # 4 GPU, tensor parallelism

    # KV-Cache оптимизации
    enable_prefix_caching=True,    # ← ключевое: кэшировать общие префиксы
    max_num_batched_tokens=32768,  # chunked prefill batch size
    max_num_seqs=256,              # concurrent sequences

    # Квантизация KV-cache
    kv_cache_dtype="fp8",          # ~3x экономия VRAM vs fp16
    # Attention weights остаются BF16 для качества

    # Speculative decoding
    speculative_model="Qwen/Qwen2.5-7B-Instruct",  # draft model
    num_speculative_tokens=5,      # draft 5 токенов → verify 1 раз

    # Производительность
    gpu_memory_utilization=0.90,
    enforce_eager=False,           # использовать CUDA graphs
)

engine = AsyncLLMEngine.from_engine_args(engine_args)
```

## Prefix Caching: как работает на практике

```python
# Сценарий: 1000 пользователей с одним system prompt

SYSTEM_PROMPT = """Ты — корпоративный AI-ассистент компании МТС.
Отвечай точно и по делу. Используй только проверенную информацию.
Формат ответов: структурированный Markdown."""

# БЕЗ prefix caching:
# Каждый запрос → prefill полного system prompt (1000 токенов)
# → 1000 req × 1000 токенов = 1M токенов prefill compute

# С prefix caching:
# Первый запрос → вычислить KV для system prompt → кэшировать в VRAM
# Следующие 999 → использовать кэш → только user_message prefill
# → Экономия: ~90% compute на prefill фазе для repeated prefixes

class PrefixCacheStats:
    """Мониторинг эффективности prefix cache."""

    def report(self, engine_metrics: dict) -> str:
        hit_rate = engine_metrics["prefix_cache_hit_rate"]
        ttft_with = engine_metrics["ttft_with_cache_ms"]
        ttft_without = engine_metrics["ttft_without_cache_ms"]

        return (
            f"Prefix cache hit rate: {hit_rate:.1%}\n"
            f"TTFT с кэшем: {ttft_with}ms vs без: {ttft_without}ms\n"
            f"Speedup: {ttft_without/ttft_with:.1f}x"
        )
```

## FP8 квантизация: бенчмарки из статьи

```python
# GuideLLM бенчмарки из статьи (Qwen2.5-32B, 1 GPU A100-80GB)

BENCHMARK_RESULTS = {
    "BF16 (baseline)": {
        "kv_cache_size_gb": 24.0,
        "max_concurrent_seqs": 32,
        "throughput_tok_per_sec": 850,
        "output_quality": "baseline"
    },

    "FP8 weights + BF16 KV": {
        "kv_cache_size_gb": 24.0,  # KV не сжат
        "max_concurrent_seqs": 32,
        "throughput_tok_per_sec": 1100,  # +30% throughput (меньше data movement)
        "output_quality": "-0.5% MMLU"  # почти без потерь
    },

    "FP8 weights + FP8 KV": {  # ПОБЕДИТЕЛЬ по memory
        "kv_cache_size_gb": 8.0,   # ~3x меньше!
        "max_concurrent_seqs": 96,  # 3x больше concurrent users
        "throughput_tok_per_sec": 2200,
        "output_quality": "-2.1% MMLU",  # приемлемо для большинства задач
        "recommendation": "Оптимум cost/quality для production"
    }
}

# Как применить FP8 в vLLM:
# engine_args.quantization = "fp8"
# engine_args.kv_cache_dtype = "fp8"
```

## Speculative Decoding: draft → verify

```python
# Принцип: маленькая модель (draft) генерирует N токенов быстро
# Большая модель (target) проверяет их за 1 forward pass

class SpeculativeDecodingExplained:
    """
    Без SD:
        Target (72B): token1 → token2 → token3 → ... (sequential)
        → 3 forward passes, 3× latency

    С SD (N=5):
        Draft (7B):  token1, token2, token3, token4, token5  (быстро)
        Target (72B): verify all 5 in ONE forward pass
        → Если все приняты: 5 токенов за цену 1 forward pass
        → Acceptance rate обычно 70-80% → ~2x speedup на decode фазе
    """

    # vLLM конфиг:
    # speculative_model = "smaller-draft-model"
    # num_speculative_tokens = 5

    # Когда SD особенно выгоден:
    # - Длинные generative ответы (>100 токенов)
    # - Draft и target модели из одного семейства (Qwen-7B + Qwen-72B)

    # Когда SD не помогает:
    # - Короткие ответы (< 20 токенов)
    # - Очень разные модели (draft acceptance rate < 50%)
```

## LMCache: cross-request KV реuse

```python
# LMCache: персистентный KV-cache между запросами (даже после eviction)
# github.com/LMCache/LMCache

LMCACHE_CONFIG = {
    "storage": "redis",              # персистентное хранение KV
    "max_cache_size_gb": 50,         # больше чем VRAM
    "eviction_policy": "LRU",

    # Сценарий использования:
    # Запрос 1: system_prompt + "Расскажи про тариф А" → KV вычислен → кэш
    # Запрос 2: system_prompt + "Расскажи про тариф Б" →
    #    → prefix (system_prompt) уже в LMCache → TTFT -70%

    # Выгода vs в-памяти prefix cache:
    # → Переживает GPU eviction (KV offloaded to Redis)
    # → Shared между несколькими vLLM инстансами
    # → Полезно при масштабировании (N GPU nodes)
}
```

## Kubernetes: production deployment

```yaml
# Из статьи: реальный Kubernetes манифест для vLLM production stack

apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-server
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        args:
          - --model=Qwen/Qwen2.5-32B-Instruct
          - --tensor-parallel-size=4
          - --enable-prefix-caching
          - --kv-cache-dtype=fp8
          - --speculative-model=Qwen/Qwen2.5-7B-Instruct
          - --num-speculative-tokens=5
          - --max-num-seqs=128
          - --gpu-memory-utilization=0.90
        resources:
          limits:
            nvidia.com/gpu: 4
        env:
          - name: VLLM_WORKER_MULTIPROC_METHOD
            value: "spawn"

---
# GuideLLM для бенчмарка:
# guidellm benchmark --target http://vllm-service:8000
#   --backend openai --model Qwen2.5-32B
#   --rate-type constant --rate 50 --max-seconds 120
```

## Применение к Lorenzo

```python
# Если Lorenzo использует LLM API — vLLM можно поднять локально

LORENZO_VLLM_CONFIG = {
    "модель": "Qwen2.5-7B-Instruct",  # для скриптов improve_llm_*.py
    "endpoint": "http://localhost:8000/v1",
    "совместимость": "OpenAI API (drop-in замена)",

    "оптимизации_для_Lorenzo": {
        "prefix_caching": True,   # CLAUDE.md повторяется в каждом запросе
        "kv_cache_dtype": "fp8",  # GPU с 24GB VRAM (одна карта)
        "max_num_seqs": 16,       # Lorenzo не production-scale
    }
}
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **vLLM + Enterprise RAG (R32)** | RAG pipeline с высокой нагрузкой: батчинг embedding + vLLM inference |
| **vLLM + LLM Judge (R28)** | Судья на базе vLLM: batch evaluate N ответов параллельно |
| **vLLM + DBRM medical (R31)** | Медицинские LLM-судьи через vLLM: высокая пропускная способность |
| **vLLM + Federated Edge (R28)** | LiteRT для edge устройств + vLLM для server-side; маршрутизация по сложности |
| **vLLM + Meta-Monitor (R29)** | Meta-Monitor следит за GPU utilization vLLM → авто-скейлинг |

## Контакт

- Статья: https://habr.com/ru/articles/1016062/ (март 2025)
- Хабр-аккаунт: habr.com/ru/users/Bambarbrandenburg/
- vLLM: github.com/vllm-project/vllm (Apache 2.0)
- vLLM Production Stack: github.com/vllm-project/production-stack
- LMCache: github.com/LMCache/LMCache
- Смежная (оптимизация inference, Yandex): https://habr.com/ru/companies/yandex/articles/878230/
- Смежная (ZINC inference engine, 35B на $500 GPU): https://habr.com/ru/articles/1020702/
- Смежная (VK batch inference): https://habr.com/ru/companies/vk/articles/900762/
