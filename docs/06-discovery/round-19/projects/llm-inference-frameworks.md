---
date: 2026-05-29
tags: [memory, rag, ingestion, local-first, architecture]
state: normalized
---

# LLM-инференс фреймворки — сравнение Ollama, vLLM, Triton, llama.cpp, SGLang

<!-- toc-auto -->
<!-- tags: llm-inference-frameworks, docs -->


<!-- summary -->
> Автор: независимый исследователь (Хабр, 2025) Хабр: https://habr.com/ru/articles/948934/
Хабр: https://habr.com/ru/articles/948934/  
GitHub: несколько: llama.cpp (MIT), vLLM (Apache 2.0), Ollama (MIT), SGLang (Apache 2.0)  
Слой: orchestration / memory / ingestion  
Дата: 2025  
Уникальнос


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Автор:** независимый исследователь (Хабр, 2025)  
**Хабр:** https://habr.com/ru/articles/948934/  
**GitHub:** несколько: llama.cpp (MIT), vLLM (Apache 2.0), Ollama (MIT), SGLang (Apache 2.0)  
**Слой:** orchestration / memory / ingestion  
**Дата:** 2025  
**Уникальность:** Единственный русскоязычный сравнительный гайд всех 6 major LLM inference frameworks с рекомендациями по сценариям. Включает: Ollama (devex), vLLM (throughput), Triton (enterprise GPU), LM Studio (GUI), llama.cpp (CPU/edge), SGLang (structured output). Критический вывод: llama.cpp в 2.8–3.2× быстрее Ollama при равных ресурсах.

## Карта 6 фреймворков

```
┌─────────────────────────────────────────────────────┐
│              LLM Inference Landscape                │
├──────────────┬──────────────────────────────────────┤
│ Ollama       │ DX > все. Docker-like CLI, GGUF, REST│
│ llama.cpp    │ Скорость > всех. CPU + GPU, MIT      │
│ vLLM         │ Throughput > всех. PagedAttention     │
│ Triton       │ NVIDIA production. TensorRT FP8       │
│ LM Studio    │ GUI для Mac/Windows. Ollama внутри    │
│ SGLang       │ Structured output. RadixAttention     │
└──────────────┴──────────────────────────────────────┘
```

## Сравнительная таблица

| Фреймворк | Tokens/s | Сложность | GPU нужен | Когда использовать |
|-----------|---------|-----------|-----------|-------------------|
| **Ollama** | базовый | ★☆☆ | нет (но лучше) | разработка, прототипы |
| **llama.cpp** | ×2.8–3.2 Ollama | ★★☆ | нет (CPU!) | edge, ресурсы важны |
| **vLLM** | очень высокий | ★★★ | да (A100+) | много параллельных запросов |
| **Triton** | максимум | ★★★★ | да (NVIDIA) | production enterprise |
| **LM Studio** | Ollama | ★☆☆ | нет | UI для не-разработчиков |
| **SGLang** | высокий | ★★★ | да | structured output, JSON |

## Детали: Ollama

```bash
# Установка + запуск за 2 минуты
curl -fsSL https://ollama.ai/install.sh | sh
ollama run qwen2.5:7b
ollama serve  # REST API: http://localhost:11434

# REST API
curl http://localhost:11434/api/generate \
  -d '{"model": "qwen2.5:7b", "prompt": "Привет!"}'
```

**Ограничения**: в 2.8–3.2× медленнее llama.cpp. Ollama — это удобная обёртка над llama.cpp, но с overhead.

## Детали: llama.cpp (быстрейший для CPU)

```bash
cmake -B build && cmake --build build --config Release -j8
./build/bin/llama-server \
  --model qwen2.5-7b-instruct.Q4_K_M.gguf \
  --port 8080 \
  --n-gpu-layers 0  # чистый CPU

# Количественные оценки (quantization)
# Q4_K_M:  лучший balance quality/speed
# Q4_K_XL: выше качество при том же размере (новый формат 2025)
```

**Вывод из статьи**: `UD_Q4_K_XL` лучше `Q4_K_M` при том же весе файла.

## Детали: vLLM (максимальный throughput)

```python
from vllm import LLM, SamplingParams

llm = LLM(model="Qwen/Qwen2.5-7B-Instruct", gpu_memory_utilization=0.9)
params = SamplingParams(temperature=0.7, max_tokens=512)

# Batch processing: обрабатывает N запросов параллельно
outputs = llm.generate(prompts_list, params)
```

**PagedAttention**: не резервирует KV-cache заранее → обслуживает 10–20× больше параллельных запросов vs наивный инференс.

## Детали: SGLang (structured output)

```python
import sglang as sgl

@sgl.function
def extract_project_info(s, doc_text):
    s += sgl.system("Extract structured info from document")
    s += sgl.user(doc_text)
    with s.json_schema(ProjectInfo):  # Pydantic схема
        s += sgl.assistant(sgl.gen("info", max_tokens=500))

# RadixAttention: кэширует prefix → быстро при похожих промптах
result = extract_project_info.run(doc_text=text)
```

**SGLang** = лучший выбор если нужен надёжный JSON-вывод (без retry на плохой JSON).

## Рекомендуемый стек для Lorenzo/Svyazi

```
Разработка:     Ollama + qwen2.5:7b (простота)
  ↓
Тесты скорости: llama.cpp (Q4_K_XL квантизация)
  ↓
Production:     vLLM (если GPU) / llama.cpp (если CPU-only)
  ↓
Structured output: SGLang для improve_llm_enrich.py
  (надёжный JSON без retry-логики)
```

## Применение к Lorenzo

Lorenzo вызывает Claude API (`improve_llm_*.py`).  
Для локального режима (без API-ключа):

```python
# improve_llm_qa.py — переключение на локальный инференс
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.anthropic.com")
# При OLLAMA: export LLM_BASE_URL=http://localhost:11434/v1
# При llama.cpp: export LLM_BASE_URL=http://localhost:8080/v1
```

SGLang + `improve_llm_enrich.py` = структурированное обогащение без галлюцинаций формата.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **llama.cpp + Lorenzo offline** | Полностью локальный Lorenzo без API-ключа |
| **vLLM + Synthetic Data (R18)** | Distilabel через vLLM = batch синтетика на 1 GPU |
| **SGLang + improve_llm_enrich** | Надёжный JSON из LLM без retry-логики |
| **Ollama + GigaAM (R16)** | Голос (GigaAM) → текст → Ollama → ответ (полностью локально) |
| **llama.cpp + FRIDA (R18)** | FRIDA embeddings + llama.cpp generation = локальный RAG |
| **vLLM + RAG Eval (R16)** | RAGAS прогоняет 1000 тестов через vLLM батчами |

## Контакт

- Статья: https://habr.com/ru/articles/948934/ (2025)
- Ollama: https://github.com/ollama/ollama (MIT)
- llama.cpp: https://github.com/ggerganov/llama.cpp (MIT)
- vLLM: https://github.com/vllm-project/vllm (Apache 2.0)
- SGLang: https://github.com/sgl-project/sglang (Apache 2.0)
- Смежная (Ollama от А до Я): https://habr.com/en/articles/990260/
- Смежная (Выжать больше из Ollama): https://habr.com/ru/articles/1025132/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
