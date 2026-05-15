---
date: 2026-05-15
tags: [rag, security, ingestion, local-first, architecture]
state: normalized
---

# AQLM.rs: 8B LLM в браузере через WebAssembly и 2-битную квантизацию

<!-- toc-auto -->
<!-- tags: yandex-aqlm-rs-llm-browser-wasm-2bit, docs -->


<!-- summary -->
> Принципиально отличается от WebGPU/WebLLM (R41): здесь CPU + WASM, а не GPU; и от GGUF/llama.cpp: аддитивное векторное квантование вместо скалярного.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** galqiwi (Владимир Малиновский, Yandex Research)  
**Хабр:** https://habr.com/ru/companies/yandex/articles/864296/  
**GitHub:** https://github.com/galqiwi/demo-aqlm-rs  
**Слой:** analytics  
**Дата:** декабрь 2024  
**Уникальность:** Llama 3.1 8B запущена в браузере на CPU без GPU через Rust + WebAssembly + 2-битную аддитивную квантизацию AQLM (Additive Quantization for Language Models): 8x сжатие (16 GB → 2.5 GB). Автор — создатель самого алгоритма AQLM и PV-Tuning. Принципиально отличается от WebGPU/WebLLM (R41): здесь CPU + WASM, а не GPU; и от GGUF/llama.cpp: аддитивное векторное квантование вместо скалярного.

## Проблема: LLM требует дорогого железа и интернета

```
Стандартный инференс LLM:
  → Llama 3.1 8B в bf16: 16 GB VRAM → нужна видеокарта
  → GGUF Q4_K_M: 4-5 GB → нужен мощный CPU / GPU
  → Облако: данные уходят на сервер → privacy проблема
  → Нет интернета → нет LLM

Цель: браузер на обычном ноутбуке без GPU
  → Максимальное сжатие (< 3 GB для 8B модели)
  → CPU inference (нет WebGPU dependency)
  → Zero install: открыл страницу → модель работает
  → Полная приватность: данные не покидают браузер
```

## AQLM: аддитивное векторное квантование

```python
# galqiwi / Yandex Research: AQLM.rs
# habr.com/ru/companies/yandex/articles/864296
# github.com/galqiwi/demo-aqlm-rs

import torch
import numpy as np
from dataclasses import dataclass

@dataclass
class AQLMConfig:
    """
    AQLM (Additive Quantization for Language Models) конфигурация.
    Принципиально отличается от GPTQ/AWQ/GGUF:
    - GPTQ/AWQ/GGUF: скалярное квантование (каждый вес → N бит)
    - AQLM: аддитивное ВЕКТОРНОЕ квантование (группа весов → сумма кодовых слов)
    """
    codebook_size: int = 256    # размер словаря кодовых слов
    num_codebooks: int = 2      # количество кодовых книг (аддитивность)
    group_size: int = 8         # число весов на вектор

    # Итоговая битность: log2(256^2) / 8 ≈ 2 бит/вес
    # 8B параметров × 2 бит = 2 GB (без учёта head и embeddings)


class AQLMQuantizer:
    """
    AQLM квантизация веса матриц.

    Идея: вместо "каждый вес = N-битное целое число"
    → "группа из k весов = W1[i1] + W2[i2]"
    где W1, W2 — обучаемые кодовые книги (codebooks),
    i1, i2 — индексы (хранятся как log2(256) = 8 бит каждый).

    Аддитивность: сумма двух кодовых слов лучше покрывает
    пространство весов чем одно слово → качество выше при той же битности.
    """

    def __init__(self, config: AQLMConfig):
        self.config = config
        # Кодовые книги: обучаются совместно с моделью
        self.codebooks = [
            torch.randn(config.codebook_size, config.group_size)
            for _ in range(config.num_codebooks)
        ]

    def quantize_weight_matrix(self,
                                 W: torch.Tensor) -> "QuantizedMatrix":
        """
        Квантизовать матрицу весов.

        Для каждой группы из group_size весов:
        1. Найти лучшие индексы i1, i2 в кодовых книгах
           (минимизировать ||W_group - (CB1[i1] + CB2[i2])||^2)
        2. Сохранить только индексы (8+8=16 бит на group_size весов)
           Вместо group_size × 16 бит (bf16) → 16 бит → сжатие в group_size раз

        Для group_size=8: сжатие в 8x → 2 бит/вес эффективно.
        """
        n_groups = W.numel() // self.config.group_size
        indices = []

        W_reshaped = W.reshape(n_groups, self.config.group_size)
        for group in W_reshaped:
            best_i1, best_i2 = self._find_best_codes(group)
            indices.append((best_i1, best_i2))

        return QuantizedMatrix(
            indices=indices,
            codebooks=self.codebooks,
            original_shape=W.shape
        )

    def _find_best_codes(self,
                          group: torch.Tensor) -> tuple[int, int]:
        """
        Beam search по кодовым книгам для минимизации ошибки квантизации.
        Сложность: O(codebook_size^2) → O(codebook_size × beam_width) с beam.
        """
        best_error = float("inf")
        best_i1, best_i2 = 0, 0

        for i1, cw1 in enumerate(self.codebooks[0]):
            residual = group - cw1
            # Найти лучшее слово для residual в CB2
            errors = torch.norm(
                residual.unsqueeze(0) - self.codebooks[1], dim=1
            )
            i2 = errors.argmin().item()
            error = errors[i2].item()

            if error < best_error:
                best_error = error
                best_i1, best_i2 = i1, i2

        return best_i1, best_i2


QUANTIZATION_COMPARISON = {
    "model": "Llama 3.1 8B",
    "methods": {
        "bf16": {
            "size": "16 GB",
            "quality": "baseline (PPL = X)",
            "hardware": "80GB A100 / H100"
        },
        "GGUF_Q4_K_M": {
            "size": "4.7 GB",
            "quality": "-1.5% quality",
            "hardware": "GPU / мощный CPU"
        },
        "AQLM_2bit": {
            "size": "~2.5 GB",
            "quality": "-3% quality (лучше чем GGUF при той же битности)",
            "hardware": "CPU (в браузере через WASM!)",
            "compression": "8x от bf16"
        }
    },
    "aqlm_advantage": (
        "При 2 бит/вес AQLM теряет меньше качества чем скалярное квантование "
        "потому что аддитивные векторные коды лучше покрывают пространство весов."
    )
}
```

## PV-Tuning: доводка качества квантизации

```python
class PVTuning:
    """
    PV-Tuning (Proximal-Variance Tuning) — улучшение AQLM качества.
    Опубликовано той же группой авторов (май 2024).

    Проблема AQLM без PV-Tuning:
    - Квантизация layer-by-layer: каждый слой независимо
    - Ошибки квантизации накапливаются через слои

    PV-Tuning решение:
    - Fine-tuning кодовых книг после квантизации
    - Минимизировать ошибку на downstream задаче, не только MSE весов
    - На небольшом calibration датасете (< 1000 примеров)
    """

    def tune_codebooks(self,
                        model: "QuantizedModel",
                        calibration_data: list[str],
                        n_steps: int = 1000) -> "QuantizedModel":
        """
        Донастройка кодовых книг на calibration данных.
        Кодовые книги обучаемы; индексы заморожены.
        """
        optimizer = torch.optim.AdamW(
            [cb for layer in model.layers for cb in layer.codebooks],
            lr=1e-4
        )

        for step, batch in enumerate(calibration_data[:n_steps]):
            loss = model.compute_loss(batch)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        return model
```

## Rust + WebAssembly: браузерный inference engine

```rust
// AQLM.rs: inference engine на Rust, компилируется в WASM
// github.com/galqiwi/demo-aqlm-rs

use wasm_bindgen::prelude::*;

/// Дескватизация одной группы весов из кодовых книг
#[wasm_bindgen]
pub fn dequantize_group(
    codebook1: &[f32],
    codebook2: &[f32],
    index1: u8,
    index2: u8,
    group_size: usize,
) -> Vec<f32> {
    let offset1 = index1 as usize * group_size;
    let offset2 = index2 as usize * group_size;

    (0..group_size)
        .map(|i| codebook1[offset1 + i] + codebook2[offset2 + i])
        .collect()
}

/// Web Workers: параллельный inference через разделение матриц
/// Каждый Worker обрабатывает свой сегмент матрицы умножения
/// Результат: ~2x ускорение на 4-core CPU
```

```python
# Python сторона: архитектурные решения

WASM_ARCHITECTURE = {
    "язык": "Rust → WebAssembly (WASM)",
    "причина_выбора_rust": [
        "Zero-cost abstractions: нет GC пауз в inference",
        "Безопасная многопоточность через Web Workers",
        "Компилируется в WASM без managed runtime"
    ],
    "многопоточность": {
        "механизм": "Web Workers + SharedArrayBuffer",
        "подход": "Model-parallel: матрица делится между Workers",
        "speedup": "~2x на 4-ядерном CPU",
        "без_webgpu": "CPU-только, не требует GPU в браузере"
    },
    "custom_rpc": {
        "задача": "Rust (WASM) ↔ JavaScript interop",
        "проблема": "wasm-bindgen не поддерживает async cross-thread calls",
        "решение": "Собственный RPC стек для передачи тензоров между потоками"
    }
}

BROWSER_DEPLOYMENT = {
    "model_loading": {
        "source": "HuggingFace Hub (streaming загрузка)",
        "format": "AQLM safetensors + кодовые книги",
        "size": "~2.5 GB (Llama 3.1 8B, 2-bit body + 4/8-bit head)"
    },
    "quantization_layers": {
        "model_body": "2-bit AQLM (основные transformer слои)",
        "head_layers": "4-bit (выходной слой)",
        "embeddings": "8-bit (embedding таблица)"
    },
    "privacy": "100% браузер: токены и запросы не покидают устройство",
    "install_required": "Нет: открыть URL → работает"
}

BENCHMARK = {
    "модель": "Llama 3.1 8B (AQLM 2-bit)",
    "hardware": "Обычный ноутбук CPU (no GPU)",
    "RAM": "~2.5 GB",
    "quality_drop": "~3% vs bf16 baseline (измерено через perplexity)",
    "demo": "Живой демо на GitHub Pages (galqiwi/demo-aqlm-rs)"
}
```

## Применение к Lorenzo

```python
# Lorenzo: AQLM паттерн для локального on-device inference

class LorenzoOnDeviceInference:
    """
    galqiwi паттерн для Lorenzo:
    AQLM-квантизованная модель для локального инференса в improve_llm_*.py.
    Вместо Anthropic API (с оплатой) → браузер/WASM модель для дешёвых задач.

    Гибрид: простые задачи (тегирование, классификация) → локальная AQLM
            сложные задачи (суммаризация, Q&A) → Anthropic API
    """

    TASK_ROUTING = {
        "simple_classification": {
            "model": "AQLM-quantized Qwen 0.5B (local)",
            "cost": "$0",
            "latency": "< 5 сек в браузере"
        },
        "complex_reasoning": {
            "model": "claude-sonnet-4-6 (API)",
            "cost": "~$0.003/запрос",
            "latency": "< 2 сек"
        }
    }

    def decide_model(self, task_complexity: float) -> str:
        if task_complexity < 0.4:
            return "local_aqlm"
        return "anthropic_api"
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **AQLM.rs + Privacy Gateway (R41)** | Максимальная приватность: AQLM в браузере = нет сервера = нет данных в облако |
| **AQLM.rs + Avito CPT (R45)** | CPT создаёт RU-модель → AQLM квантизует для браузера → offline RU LLM |
| **AQLM.rs + Telecom Classifier (R46)** | AQLM-квантизованный классификатор на edge-устройствах оператора |
| **AQLM.rs + MWS Vision Bench (R45)** | Можно ли запустить Vision Encoder в браузере? AQLM для мультимодальных edge |
| **AQLM.rs + LLM Observability (R45)** | Tracing browser-based inference: измерить latency/quality WASM vs API |

## Контакт

- Статья: https://habr.com/ru/companies/yandex/articles/864296/ (декабрь 2024)
- GitHub: https://github.com/galqiwi/demo-aqlm-rs
- Автор: galqiwi (Владимир Малиновский, Yandex Research)
- AQLM paper: arxiv.org/abs/2401.06118
- PV-Tuning paper: arxiv.org/abs/2405.14852 (май 2024)
- Смежная (Privacy LLM in-browser WebGPU, R41): docs/06-discovery/round-41/projects/privacy-llm-pii-gateway-ondevice-rag.md
- Смежная (Edge AI v1, R34): docs/06-discovery/round-34/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
