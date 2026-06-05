# Quantization Deep Dive: LLM.Int8 → SmoothQuant → GPTQ → SPQR → QLoRA

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** re9ulus (Яндекс)  
**Хабр:** https://habr.com/ru/companies/yandex/articles/800945/  
**GitHub:** ссылки на GPTQ, SmoothQuant, SPQR, QLoRA в статье  
**Слой:** knowledge / ingestion  
**Дата:** март 2024  
**Уникальность:** Единственная на Хабре систематическая таксономия 6 современных методов квантования LLM с объяснением корневой причины проблемы (outlier activations в больших моделях) и механизмами каждого решения. GPTQ: 3.25× speedup на A100 через Hessian-оптимизацию. QLoRA: файн-тюнинг 65B на одном 48GB GPU через NF4. Не просто "как запустить" — "почему наивный INT8 ломает LLM и как каждый метод это исправляет".

## Проблема: почему наивный INT8 ломает большие языковые модели

```
Наивное квантование (до ~7B параметров работает):
  FP16 → INT8: поделить на max_value, округлить
  → Сохраняет 50% памяти
  → Работает для маленьких моделей

Проблема outlier activations (масштабируется с размером модели):
  В моделях 6.7B+ появляются "выбросы":
  99% активаций: диапазон [-1, 1]
  1% активаций: диапазон [-500, 500]  ← outliers

  Если квантовать всё вместе:
    INT8 шаг = 500/127 ≈ 3.9
    → 99% обычных значений: округлены до 0!
    → Информация потеряна, модель деградирует

  Масштабирование: чем больше модель, тем сильнее outliers.
  BLOOM-176B: выбросы в 25% каналов всех слоёв.

  Каждый из 6 методов — разное решение этой проблемы.
```

## 6 методов квантования: механизмы и компромиссы

```python
# re9ulus (Yandex): Quantization Deep Dive
# habr.com/ru/companies/yandex/articles/800945/

from dataclasses import dataclass
from typing import Literal
import numpy as np

QuantMethod = Literal[
    "naive_int8",
    "llm_int8",
    "smoothquant",
    "gptq",
    "spqr",
    "qlora"
]

@dataclass
class QuantBenchmark:
    """Результаты метода квантования."""
    method: QuantMethod
    bits: int
    memory_reduction: float      # × относительно FP16
    latency_vs_fp16: float       # <1.0 = быстрее, >1.0 = медленнее
    quality_loss_ppl: float      # perplexity degradation (меньше = лучше)
    key_innovation: str


# ===== МЕТОД 1: LLM.int8() (Dettmers et al., 2022) =====

class LLMInt8:
    """
    Решение: изолировать outlier-каналы и обработать отдельно.

    Идея: не пытаться квантовать outliers в INT8 — оставить их в FP16.
    99% "обычных" каналов → INT8 (быстро, дёшево)
    1% outlier-каналов → FP16 (точно, но дорого)

    Результат: векторизованная смешанная точность.
    Память: -50% (большая часть в INT8)
    Скорость: +15-23% накладных расходов (смешанные операции)

    Почему медленнее несмотря на меньше памяти:
    Scatter/gather для разделения outlier-каналов → дополнительные операции
    Overhead растёт с числом outlier-каналов (BLOOM-176B: 25% слоёв!)
    """

    def quantize_matmul(self,
                         W: np.ndarray,
                         X: np.ndarray) -> np.ndarray:
        """
        Смешанная точность: INT8 для обычных + FP16 для outliers.
        """
        # Найти outlier-столбцы в активациях (threshold=6.0 стандартный)
        outlier_cols = np.where(np.abs(X).max(axis=0) > 6.0)[0]
        normal_cols = np.setdiff1d(np.arange(X.shape[1]), outlier_cols)

        # INT8 часть (большинство каналов)
        X_normal = X[:, normal_cols].astype(np.int8)
        W_normal = W[:, normal_cols].astype(np.int8)
        result_int8 = (X_normal @ W_normal.T).astype(np.float32)

        # FP16 часть (outlier-каналы)
        X_outlier = X[:, outlier_cols].astype(np.float16)
        W_outlier = W[:, outlier_cols].astype(np.float16)
        result_fp16 = (X_outlier @ W_outlier.T).astype(np.float32)

        return result_int8 + result_fp16

    BENCHMARK = QuantBenchmark(
        method="llm_int8", bits=8,
        memory_reduction=2.0,          # -50% памяти
        latency_vs_fp16=1.20,          # +15-23% медленнее BLOOM-176B
        quality_loss_ppl=0.1,          # минимальная деградация
        key_innovation="Смешанная точность: INT8 + FP16 для outliers"
    )


# ===== МЕТОД 2: SmoothQuant (Xiao et al., 2022) =====

class SmoothQuant:
    """
    Решение: перенести проблему outliers из активаций в веса OFFLINE.

    Математика:
    Y = X · W = (X / s) · (s · W) = X_smooth · W_smooth

    s = per-channel smoothing factor (вычисляется один раз offline)
    После деления X на s: outliers исчезают → INT8 без потерь
    После умножения W на s: веса компенсируют, качество сохраняется

    Ключевое: s вычисляется OFFLINE (один раз при подготовке модели).
    При инференсе — чистый INT8, нет накладных расходов!
    → 0 overhead vs FP16 при инференсе.
    """

    def compute_smoothing_factors(self,
                                   weights: np.ndarray,
                                   calibration_activations: np.ndarray,
                                   alpha: float = 0.5) -> np.ndarray:
        """
        Вычислить s offline по калибровочным данным.
        alpha: баланс между активациями и весами (0.5 = равный).
        """
        # Максимальные значения по каналам
        max_act = np.abs(calibration_activations).max(axis=0) ** alpha
        max_wt = np.abs(weights).max(axis=1) ** (1 - alpha)

        # Smoothing factor: перенести "сложность" в веса
        s = max_act / max_wt
        return s

    BENCHMARK = QuantBenchmark(
        method="smoothquant", bits=8,
        memory_reduction=2.0,
        latency_vs_fp16=0.95,       # чуть быстрее FP16 (чистый INT8)
        quality_loss_ppl=0.15,
        key_innovation="Offline перенос outliers: нулевой overhead при инференсе"
    )


# ===== МЕТОД 3: GPTQ (Frantar et al., 2022) =====

class GPTQ:
    """
    Решение: оптимальные веса для квантования через Hessian (2-й порядок).

    Проблема наивного округления: ошибки накапливаются по слоям.
    GPTQ: для каждого столбца весов найти оптимальное INT4 значение,
    компенсируя ошибку в соседних столбцах.

    Алгоритм (упрощённо):
    1. Вычислить Hessian = X^T X (чувствительность loss к весам)
    2. Квантовать столбец 1 → ошибка δ
    3. Скорректировать оставшиеся столбцы: W -= δ × H_inv[j, j+1:]
    4. Повторить для каждого столбца (lazy batch optimization)

    Результат: 3.25× speedup на A100, 4.5× на A6000 при 3-4 бит
    """

    def quantize_layer_gptq(self,
                              W: np.ndarray,
                              H: np.ndarray,  # Hessian = X^T X
                              bits: int = 4) -> np.ndarray:
        """
        GPTQ per-column quantization с коррекцией ошибок через Hessian.
        """
        W_q = W.copy().astype(np.float32)
        H_inv = np.linalg.inv(H + 0.01 * np.eye(H.shape[0]))  # regularized

        for j in range(W.shape[1]):
            # Квантовать столбец j
            w_j = W_q[:, j]
            w_j_quantized = self._quantize_vector(w_j, bits)

            # Ошибка квантования
            delta = w_j_quantized - w_j

            # Компенсировать ошибку в оставшихся столбцах
            if j + 1 < W.shape[1]:
                correction = np.outer(delta, H_inv[j, j+1:] / H_inv[j, j])
                W_q[:, j+1:] -= correction

            W_q[:, j] = w_j_quantized

        return W_q

    BENCHMARK = QuantBenchmark(
        method="gptq", bits=4,
        memory_reduction=4.0,           # FP16 → INT4
        latency_vs_fp16=0.31,           # 3.25× быстрее на A100
        quality_loss_ppl=0.5,           # небольшая деградация на 4 бит
        key_innovation="Hessian-оптимальное квантование: 3.25× на A100, 4.5× на A6000"
    )


# ===== МЕТОД 4: QLoRA (Dettmers et al., 2023) =====

class QLoRA:
    """
    Решение: файн-тюнинг через LoRA адаптеры поверх NF4-квантованной модели.

    NF4 (NormalFloat4): 4-битный формат, оптимальный для нормально
    распределённых весов трансформеров.

    Два уровня квантования:
    1. NF4 для весов: 4 бит (FP16 → NF4 → double quant → ещё меньше)
    2. BF16 для адаптеров LoRA: высокая точность обновлений

    Gradient checkpointing: не хранить активации → -70% памяти при обучении.

    Результат: LLaMA 65B на одном 48GB GPU (A6000/A100)
    Раньше требовал 8× A100 80GB = 640GB VRAM!
    """

    DOUBLE_QUANTIZATION = {
        "идея": "Квантовать константы квантования (scale factors)",
        "экономия": "0.37 бит/параметр (дополнительно к NF4)",
        "итого": "NF4 + double quant ≈ 4.5 бит/параметр"
    }

    BENCHMARK = QuantBenchmark(
        method="qlora", bits=4,
        memory_reduction=8.0,           # 65B: 130GB → ~18GB
        latency_vs_fp16=1.0,            # обучение медленнее, инференс = GPTQ
        quality_loss_ppl=0.3,           # файн-тюн компенсирует деградацию
        key_innovation="65B fine-tuning на 1×48GB GPU через NF4 + BF16 LoRA адаптеры"
    )


COMPARISON_TABLE = {
    "LLM.int8": {
        "bits": 8, "speedup_A100": "0.80×", "memory": "2×",
        "use_case": "Inference без деградации качества"
    },
    "SmoothQuant": {
        "bits": 8, "speedup_A100": "1.05×", "memory": "2×",
        "use_case": "Быстрый INT8 inference без overhead"
    },
    "GPTQ": {
        "bits": 4, "speedup_A100": "3.25×", "memory": "4×",
        "use_case": "Максимальная скорость inference"
    },
    "SPQR": {
        "bits": "3-4", "speedup_A100": "3×", "memory": "4×",
        "use_case": "GPTQ + outlier blocks для лучшего качества"
    },
    "QLoRA": {
        "bits": 4, "speedup_A100": "N/A (training)", "memory": "8×",
        "use_case": "Файн-тюнинг 65B на одном GPU"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: квантование для локального inference в gateway.py

class LorenzoQuantizedInference:
    """
    re9ulus паттерн для Lorenzo:
    Выбор метода квантования под доступное железо.

    A100 80GB + production throughput → GPTQ INT4 (3.25× speedup)
    A6000 48GB + fine-tuning → QLoRA NF4 (65B на 1 GPU)
    Consumer GPU (16-24GB) → QLoRA 7B-13B без деградации
    CPU inference + память → LLM.int8 (меньше speedup, надёжно)

    Для Lorenzo gateway.py:
    model = AutoModelForCausalLM.from_pretrained(
        "model_name",
        load_in_4bit=True,         # QLoRA
        bnb_4bit_quant_type="nf4", # NormalFloat4
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Quantization + Self-hosted 4×4090 (R49)** | Выбор метода квантования для 4×RTX 4090: GPTQ INT4 vs QLoRA NF4 vs LLM.int8 на 96GB VRAM |
| **Quantization + RAG Embedder Fine-Tuning (R50)** | QLoRA для fine-tuning deepvk/USER-bge-m3: 4-бит базовая модель + BF16 LoRA адаптеры |
| **Quantization + GBNF Constrained Decoding (R49)** | GPTQ INT4 inference + XGrammar grammar constraints: максимальная скорость + структурированный вывод |
| **Quantization + LLM Observability (R45)** | Трейсинг: perplexity деградация при квантовании на реальных запросах Lorenzo corpus |
| **Quantization + Agent Evaluation (R48)** | Golden Set для измерения деградации качества агентского поведения при INT4 vs FP16 |

## Контакт

- Статья: https://habr.com/ru/companies/yandex/articles/800945/ (март 2024)
- Автор: re9ulus (Яндекс)
- GPTQ: github.com/IST-DASLab/gptq
- SmoothQuant: github.com/mit-han-lab/smoothquant
- QLoRA: github.com/artidoro/qlora
- bitsandbytes: github.com/TimDettmers/bitsandbytes (LLM.int8 + QLoRA)
- Смежная (AQLM.rs браузер, R46): docs/06-discovery/round-46/
- Смежная (Self-hosted 4×4090, R49): docs/06-discovery/round-49/projects/dmitrii-chashchin-self-hosted-4x4090-vllm-parallelism.md
- Смежная (vLLM inference opt, R32): docs/06-discovery/round-32/
