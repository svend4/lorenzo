---
date: 2026-05-29
tags: [rag, knowledge, ingestion, architecture, self-improve]
state: normalized
---

# LLM Compute Economics 2026 — когда и какую модель использовать

<!-- toc-auto -->
<!-- tags: llm-compute-economics-2026, docs -->


<!-- summary -->
> LLM Compute Economics 2026 — когда и какую модель использовать — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый аналитик (Хабр, 2026)  
**Хабр:** https://habr.com/ru/articles/1024850/  
**GitHub:** не указан (аналитическая статья с расчётами и фреймворком решений)  
**Слой:** orchestration / knowledge / analytics  
**Дата:** 2026  
**Уникальность:** Первый русскоязычный экономический фреймворк для LLM-решений в 2026: «compute crunch» (дефицит GPU) меняет экономику — reasoning-модели стали в 5-10× дороже в вычислениях. Практические таблицы: стоимость запроса × точность × latency для 15+ сценариев. Ответ на вопрос: «когда платить за GPT-5, когда хватит Haiku, когда запустить локально».

## Compute Crunch 2026

```
2023: GPU = дефицитный ресурс, мало у кого
2024: NVIDIA H100 расширились, цены снизились
2025: Reasoning-модели (o1, R1, V3) создали новый спрос
2026: «Compute crunch» — reasoning inference в 10-50× тяжелее

Почему thinking дороже:
  Обычный запрос: ~500 output tokens
  Thinking запрос: ~5000-50000 tokens (reasoning) + ~500 финальный ответ
  → В 10-100× больше GPU-времени
  → В 10-100× дороже при reasoning API

Результат: тщательный выбор модели под задачу = основная экономия 2026
```

## Матрица выбора модели

| Задача | Рекомендация | Почему | Примерная цена/1M tokens |
|--------|-------------|--------|--------------------------|
| Тегирование, форматирование | **Haiku / Qwen-0.6B** | не нужна точность, нужна скорость | $0.25 |
| Суммаризация текстов | **Sonnet / DeepSeek V3** | баланс качества и цены | $3-5 |
| Сложный Q&A, анализ | **Sonnet** | достаточно точен | $3 |
| Математика, логика | **o3 / R1** (reasoning) | точность > скорость | $15-60 |
| Bulk обработка (>10K) | **локальный LLM** (llama.cpp) | нет per-token cost | ~$0 (электричество) |
| Критичные решения | **Opus / o3** | максимальная точность | $15-75 |
| Генерация синтетики | **DeepSeek V3 API** | дёшево, OpenAI-совм. | $0.27 |

## Экономика Lorenzo: расчёт

```
Текущий Lorenzo: claude-sonnet-4-6 для всего

Задачи и объёмы:
  improve_llm_enrich.py: 2483 карточки × 500 tokens = 1.24M tokens
    → Sonnet: 1.24M × $3/M = $3.72
    → Haiku:  1.24M × $0.25/M = $0.31  (экономия $3.41 = -92%)

  improve_llm_qa.py: 50 запросов/день × 2000 tokens = 100K tokens/день
    → Sonnet: 100K × $3/M = $0.30/день = $9/месяц
    → Haiku:  OK для 80% запросов → экономия $7.2/месяц

  improve_llm_summary.py: 50 файлов × 1000 tokens = 50K tokens
    → Достаточно Haiku: $0.013 вместо $0.15

Итого экономия: ~85% при правильном routing
```

## Decision Tree: выбор модели

```
Задача поступает в improve_llm_router():
        ↓
Нужна точность >95%?
  ДА → сложная задача?
    ДА → Opus / o3 (reasoning)
    НЕТ → Sonnet
  НЕТ → нужен русский язык?
    ДА → Sonnet (Claude лучший в RU, по R17 CoT)
    НЕТ → Haiku / DeepSeek (дёшево)
        ↓
Bulk (>1000 документов)?
  ДА → локальный LLM (llama.cpp Q4_K_XL из R19)
  НЕТ → API
```

## Reasoning overhead: конкретные числа (2026)

```
claude-opus-4-7 с thinking (extended):
  Запрос на анализ кода: ~15,000 thinking tokens + 500 ответ
  Стоимость: ~$1.13 за запрос
  Latency: ~45 секунд

claude-haiku-4-5 без thinking:
  Тот же запрос: ~500 tokens ответ
  Стоимость: ~$0.00013 за запрос (в 8700× дешевле!)
  Latency: ~2 секунды

Вывод: reasoning оправдан если один правильный ответ
  заменяет 1000 неправильных × стоимость исправления
```

## Тренд: «Маленькие умные модели» 2026

```
2024: «нужна большая модель для умного ответа»
2026: «маленькая модель + правильный промпт + RAG = большая модель»

Qwen 2.5 7B (QLoRA fine-tuned на Lorenzo corpus):
  Знает Lorenzo corpus наизусть
  Отвечает на вопросы о Svyazi без RAG
  Cost: $0 за инференс (локально)

vs

Claude Sonnet (general):
  Не знает Lorenzo
  RAG нужен + стоит $3/M токенов
```

## Паттерн: Model Routing в Lorenzo

```python
# Предложенный improve_llm_router.py:
class LLMRouter:
    def route(self, task: str, doc_len: int) -> str:
        if doc_len > 10_000:  # bulk
            return "local://qwen2.5:7b"
        if task in FORMATTING_TASKS:
            return "claude-haiku-4-5-20251001"
        if task in ANALYSIS_TASKS and doc_len < 2000:
            return "claude-sonnet-4-6"
        if task in COMPLEX_TASKS:
            return "claude-opus-4-7"  # с thinking
        return "deepseek-v3"  # default: cheap + capable
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Economics + Reasoning (R20)** | Роутинг: когда reasoning окупается, когда нет |
| **Economics + DeepSeek (R20)** | DeepSeek как cheap tier в 3-уровневом роутинге |
| **Economics + Synthetic Data (R18)** | DeepSeek V3 API для bulk синтетики (10× дешевле GPT) |
| **Economics + llama.cpp (R19)** | Локальный инференс = нулевая стоимость для bulk |
| **Economics + Fine-tuning (R15)** | QLoRA fine-tune → specialised модель → дешевле RAG |
| **Economics + RAG Eval (R16)** | RAGAS измеряет: стоит ли дорогая модель своих денег |

## Контакт

- Статья: https://habr.com/ru/articles/1024850/ (2026)
- LLM pricing tracker: artificialanalysis.ai
- Смежная (Итоги LLM 2025): https://habr.com/ru/articles/982496/
- Смежная (как считать экономику AI): openai.com/pricing
- Token counter: platform.openai.com/tokenizer

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
