---
date: 2026-05-28
tags: [rag, orchestration, knowledge, architecture, anthropic]
state: normalized
---

# DSPy — программирование языковых моделей вместо промптинга

<!-- toc-auto -->
<!-- tags: dspy-prompt-optimizer, docs -->


<!-- summary -->
> Компонент | Назначение | Signature | Описание: что принимает модуль, что возвращает |
 
Компоненты DSPy
 Компонент | Назначение |
 -----------|-----------|
 Signature | Описание: что принимает модуль, что возвращает |
 Module | ChainOfThought, ReAct, Retrieve и др.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Stanford NLP Group (Omar Khattab и команда)  
**Хабр:** https://habr.com/ru/articles/882864/  
**GitHub:** https://github.com/stanfordnlp/dspy (MIT, 22k+ stars)  
**Слой:** orchestration / optimization / quality  
**Дата:** 2022 (DSP) → 2023 (DSPy) → 2025–2026 (stable)  
**Уникальность:** Единственный open-source фреймворк для **алгоритмической** оптимизации промптов: не «угадай правильный промпт вручную», а компилятор подбирает best-in-class инструкции и few-shot примеры автоматически. Модель рассматривается как **параметр**, который оптимизируется — как веса нейросети.

## Ключевая идея

```
Традиционный подход:
  Разработчик → угадывает промпт → тестирует → улучшает → ...

DSPy:
  Разработчик → пишет сигнатуры (input/output) → задаёт метрику
       ↓
  DSPy Compiler → прогоняет оптимизатор (MIPROv2, BootstrapFewShot)
       ↓
  Оптимальные инструкции + few-shot примеры → производительный пайплайн
```

## Компоненты DSPy

| Компонент | Назначение |
|-----------|-----------|
| **Signature** | Описание: что принимает модуль, что возвращает |
| **Module** | ChainOfThought, ReAct, Retrieve и др. |
| **Optimizer** | MIPROv2, BootstrapFewShotWithRandomSearch, OPRO |
| **Metric** | Функция оценки качества (F1, exact_match, custom) |
| **Teleprompter** | Оркестратор оптимизации |

## Результаты (из Stanford)

- Автоматически превосходит ручные few-shot промпты для **GPT-3.5** и **Llama2-13b**
- Интеграция с **Qdrant** (векторный поиск в RAG-пайплайнах DSPy)
- Поддержка любой LLM через API (Anthropic, OpenAI, Ollama, локальные)

## Применение к Lorenzo

Lorenzo использует `improve_llm_enrich.py` с фиксированными промптами.  
С DSPy: **промпт для обогащения карточек оптимизируется автоматически**  
по метрике (полнота секций, качество summary, релевантность тегов).  
`improve_llm_qa.py` → DSPy-пайплайн = лучшие ответы при тех же токенах.

```python
# DSPy-паттерн для Lorenzo:
class CardEnrichment(dspy.Signature):
    """Обогащение карточки проекта."""
    card_text: str = dspy.InputField()
    summary: str = dspy.OutputField(desc="300-символьный summary")
    tags: list[str] = dspy.OutputField(desc="теги проекта")

enrich = dspy.ChainOfThought(CardEnrichment)
# Оптимизатор подбирает лучшие инструкции автоматически
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **DSPy + improve_llm_enrich** | Автооптимизация промптов обогащения карточек Lorenzo |
| **DSPy + Context Engineering (R14)** | DSPy оптимизирует слой промптов внутри правильного контекста |
| **DSPy + SocratiCode (R08)** | Qwen компилятор (SocratiCode) + DSPy оптимизация = меньше токенов + лучше |
| **DSPy + Qdrant (Vector DB R12)** | DSPy + Qdrant = production RAG пайплайн с автооптимизацией |

## Контакт

- GitHub: https://github.com/stanfordnlp/dspy (MIT)
- Статья Хабр: https://habr.com/ru/articles/882864/
- Документация: https://dspy.ai/
- Интеграция с Qdrant: https://qdrant.tech/documentation/frameworks/dspy/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
