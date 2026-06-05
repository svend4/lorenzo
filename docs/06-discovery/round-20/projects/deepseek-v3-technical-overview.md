# DeepSeek V3→V3.2 — технический обзор эволюции открытых LLM

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый ML-исследователь (Хабр, апрель 2026)  
**Хабр:** https://habr.com/ru/articles/973954/  
**GitHub:** https://github.com/deepseek-ai/DeepSeek-V3 (MIT)  
**Слой:** knowledge / orchestration / memory  
**Дата:** апрель 2026  
**Уникальность:** Единственный русскоязычный глубокий технический разбор эволюции DeepSeek от V3 до V3.2: MLA (Multi-head Latent Attention), MoE архитектура, FP8 training, DSA (DeepSeek Sparse Attention) для длинного контекста. V3.2 достигает уровня GPT-5 при открытых весах (MIT). Практический взгляд: когда DeepSeek лучше Claude для конкретных задач.

## Эволюция архитектур

```
DeepSeek V2 (2024)
  → MLA: Multi-head Latent Attention
    KV-cache через latent vectors → в 5-13× меньше KV-cache памяти
  → MoE: 236B параметров, активны только 21B за инференс
        ↓
DeepSeek V3 (декабрь 2024)
  → 671B total, 37B active (MoE)
  → FP8 training: первый раз в production на этом масштабе
  → DualPipe: overlap computation+communication при distributed training
  → context: 128K токенов
        ↓
DeepSeek V3.1 (февраль 2025)
  → Hybrid model: instruction + reasoning в одной модели
  → /no_think токен: выключает reasoning-режим
  → Улучшенный math и code
        ↓
DeepSeek V3.2 (апрель 2026)
  → DSA: DeepSeek Sparse Attention
    - разреженное внимание для длинных контекстов
    - значительное ускорение при >32K токенов
  → Производительность на уровне GPT-5 (бенчмарки)
  → Открытые веса (MIT)
```

## MLA — ключевая инновация

```
Стандартный Multi-head Attention:
  KV-cache = O(seq_len × n_heads × head_dim)
  При 128K контексте = ~20GB только KV-cache на 70B модели

MLA (Multi-head Latent Attention):
  KV-cache = O(seq_len × latent_dim)  где latent_dim << n_heads × head_dim
  → В 5-13× меньше памяти
  → Длинные контексты без OOM

Идея: сжать KV в latent vector → восстановить при вычислении attention
```

## MoE — эффективность при масштабе

```
Dense модель 37B:
  37B параметров активны при каждом токене
  = дорого, но предсказуемо

DeepSeek V3 MoE (671B total, 37B active):
  671B параметров хранятся
  Каждый токен активирует только ~5.5% параметров (37B)
  = скорость/стоимость как у 37B
  = качество как у 671B
  → GPU memory: нужно хранить 671B, но вычислять 37B
```

## DSA (V3.2) — длинный контекст

```
Full Attention: O(n²) по длине последовательности
  При n=128K: 128K² = 16B операций внимания
  → медленно, дорого

DeepSeek Sparse Attention:
  Каждый токен смотрит только на часть контекста:
  - локальное окно: последние K токенов (полностью)
  - глобальные якоря: специальные токены с полным вниманием
  - стридовое: каждый s-й токен
  → O(n × K) вместо O(n²)
  → V3.2 значительно быстрее на длинных контекстах
```

## Практическое сравнение (бенчмарки апрель 2026)

| Задача | DeepSeek V3.2 | GPT-5 | Claude 4 Opus | Выводы |
|--------|---------------|-------|--------------|--------|
| Код (HumanEval) | ≈GPT-5 | baseline | ≈GPT-5 | паритет |
| Математика (MATH) | чуть лучше | baseline | ≈ | DS побеждает |
| Русский язык | хуже | хуже | лучше | Claude выигрывает |
| Long context | очень хорошо (DSA) | хорошо | хорошо | DS выигрывает |
| Цена инференса | очень дёшево | дорого | дорого | DS выигрывает |

## Открытые веса — практические последствия

```
MIT лицензия = можно:
  ✅ fine-tune под свои данные
  ✅ distill в меньшую модель (паттерн R16)
  ✅ запустить локально (vLLM, llama.cpp из R19)
  ✅ использовать в коммерческих продуктах без royalty
  ✅ встроить в Lorenzo как альтернатива Claude API
```

**Объём**: V3.2 требует ~400GB VRAM для full inference (Multi-GPU).  
Квантованные версии (Q4): ~200GB → 3× A100 80GB или 5× RTX 4090.

## /no_think токен (V3.1+)

```python
# Стандартный режим (thinking включён):
response = client.chat("Реши это уравнение: x² + 5x + 6 = 0")
# → DeepSeek думает 30 секунд → точный ответ

# Режим без thinking (быстрый ответ):
response = client.chat("/no_think Реши это уравнение: x² + 5x + 6 = 0")
# → DeepSeek отвечает сразу → 90% точность при 5× скорости
```

Для Lorenzo: `/no_think` для `improve_llm_enrich.py` (не нужно думать для форматирования).  
Полный reasoning — только для `improve_llm_qa.py` (сложные вопросы по базе знаний).

## Применение к Lorenzo

```python
# Переключение с Claude на DeepSeek в improve_llm_*.py:
import anthropic  # сейчас
# → заменить на:
from openai import OpenAI
client = OpenAI(
    api_key="deepseek-api-key",
    base_url="https://api.deepseek.com"
)
# DeepSeek API совместим с OpenAI API формат
# Цена: ~10-20× дешевле Claude для bulk операций
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **DeepSeek + llama.cpp (R19)** | V3.2 GGUF квантизация → полностью локальный large LLM |
| **DeepSeek /no_think + improve_llm_enrich** | Быстрое обогащение карточек без CoT overhead |
| **DeepSeek + Fine-tuning (R15)** | MIT веса → QLoRA fine-tune на Lorenzo-специфичных данных |
| **DeepSeek + Synthetic Data (R18)** | Cheap bulk синтетика через DeepSeek API (10× дешевле GPT) |
| **DeepSeek + Reasoning LLM (R20)** | V3.2 hybrid: выбирать thinking on/off по сложности задачи |

## Контакт

- Статья: https://habr.com/ru/articles/973954/ (апрель 2026)
- DeepSeek GitHub: https://github.com/deepseek-ai/DeepSeek-V3 (MIT)
- DeepSeek API: api.deepseek.com (OpenAI-compatible)
- Технический отчёт: arxiv.org/abs/2412.19437 (V3), /2501.12948 (V3.1)
- Смежная (YADRO тест DeepSeek R1 + Qwen3): https://habr.com/ru/companies/yadro/articles/938172/
