# Fine-tuning LLM 2026 — дообучение локальных моделей для одного разработчика

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

**Автор:** команда OTUS (образовательная платформа)  
**Хабр:** https://habr.com/ru/companies/otus/articles/1026700/  
**GitHub:** инструменты: Unsloth, TRL, LLaMA-Factory (все open source)  
**Слой:** orchestration / quality / knowledge  
**Дата:** апрель–май 2026  
**Уникальность:** Первая в 2026 году практическая статья, констатирующая: дообучение 7–8B LLM стало **реальной опцией для одного разработчика** — не корпоративной задачей. Сниженные требования к VRAM (QLoRA на 16 ГБ), зрелые инструменты, открытые базовые модели.

## Почему 2026 — переломный год для fine-tuning

| Год | Требования | Доступность |
|-----|-----------|-------------|
| 2023 | 80 ГБ+ (A100) | только корпорации |
| 2024 | 40 ГБ (RTX 3090) | энтузиасты |
| 2025 | 24 ГБ (QLoRA) | продвинутые разработчики |
| 2026 | **16 ГБ (QLoRA + Unsloth)** | **один разработчик** |

## Практический стек (из статьи)

### Базовые модели (рекомендованные)

| Модель | Параметры | Особенность |
|--------|-----------|-------------|
| **Llama 3.1 8B** | 8B | лучший English/Code |
| **Mistral 7B** | 7B | баланс качество/скорость |
| **Qwen 2.5 7B** | 7B | лучший для Russian + Code |

### Инструменты

| Инструмент | Назначение | GitHub |
|-----------|-----------|--------|
| **Unsloth** | 2x быстрее обучение, меньше VRAM | github.com/unslothai/unsloth |
| **TRL (HuggingFace)** | SFT, RLHF, DPO | github.com/huggingface/trl |
| **LLaMA-Factory** | UI + конфиги для любых моделей | github.com/hiyouga/LLaMA-Factory |

### Минимальный датасет

> 500–10 000 примеров в формате `{instruction, input, output}`.  
> Качество важнее количества: 500 чистых примеров > 5000 шумных.

## Методы (PEFT)

```
Full Fine-tuning (все веса):  слишком дорого
        vs
LoRA (Low-Rank Adaptation):   обучается 1–10% параметров
        ↓
QLoRA (4-bit квантизация):    VRAM ÷ 4, скорость ÷ 1.3
        ↓
Unsloth + QLoRA:              ещё 2× быстрее
```

## Применение к Lorenzo

Lorenzo использует Anthropic API (облачная модель).  
Fine-tuned local model открывает **полностью офлайн Svyazi-агент**:

```
Датасет: docs/06-discovery/round-*/projects/*.md (60+ проектов)
         + docs/05-habr-projects/**/*.md
         → 500+ примеров {запрос → ответ о проектах}

Qwen 2.5 7B + QLoRA (16 ГБ VRAM)
         → локальная модель, знающая всю базу Svyazi
```

Это следующий шаг после RAG: не поиск + LLM, а **LLM, которая помнит**.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Fine-tuning + 60 проектов Lorenzo** | Дообучение Qwen 2.5 7B на базе знаний = локальный Svyazi-советник |
| **Fine-tuning + DSPy (R14)** | DSPy генерирует обучающие примеры для fine-tuning автоматически |
| **Fine-tuning + Vera (R11)** | Vera (GGUF десктоп) + дообученная модель = персональный офлайн ассистент |
| **Fine-tuning + Орrин RK3588 (R11)** | Дообученная 7B на RK3588 = специализированный edge AI агент |

## Контакт

- Статья: https://habr.com/ru/companies/otus/articles/1026700/
- Unsloth: https://github.com/unslothai/unsloth (Apache 2.0)
- LLaMA-Factory: https://github.com/hiyouga/LLaMA-Factory (Apache 2.0)
- TRL: https://github.com/huggingface/trl (Apache 2.0)
