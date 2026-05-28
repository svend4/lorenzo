---
date: 2026-05-28
tags: [rag, orchestration, knowledge, architecture, roadmap]
state: normalized
---

# Reasoning-LLM — архитектура думающих моделей и практика применения

<!-- toc-auto -->
<!-- tags: reasoning-llm-architecture, docs -->


<!-- summary -->
> Три модели — три подхода DeepSeek R1 (открытые веса) Claude 3.7 Sonnet (hybrid) Когда использовать reasoning-модель
OpenAI o1 / o3
 
DeepSeek R1 (открытые веса)
 
Claude 3.7 Sonnet (hybrid)
 
Когда использовать reasoning-модель
 
Reasoning overhead: когда окупается
 
Дистилляция reasoning-моделей (R1 паттерн)
 
Применение к Lorenzo
Lorenzo


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** команда Selectel (облачный провайдер, образовательные статьи)  
**Хабр:** https://habr.com/ru/companies/selectel/articles/892600/  
**GitHub:** не указан (обзорная статья с кодом и архитектурными схемами)  
**Слой:** orchestration / knowledge / analytics  
**Дата:** март 2025  
**Уникальность:** Первый детальный русскоязычный разбор архитектуры thinking-моделей (OpenAI o1, DeepSeek R1, Claude 3.7 Sonnet) с практическими рекомендациями когда их применять — а когда они избыточны. Ключевой инсайт: reasoning overhead 5-30 секунд оправдан только при P(ошибки) × стоимость_ошибки > стоимость_reasoning.

## Что такое reasoning-LLM

```
Обычная LLM:
  Запрос → [один forward pass] → Ответ
  Время: ~1-3 секунды
  Точность: на сложных задачах ~70-80%

Reasoning-LLM (thinking model):
  Запрос → [thinking tokens: рассуждение] → Ответ
  Время: ~10-60 секунд (зависит от сложности)
  Точность: на сложных задачах ~90-95%
        ↓
Thinking tokens = внутренний монолог модели (не виден пользователю)
  «Давайте подумаем. Задача X. Первый подход... нет, это неверно.
   Второй подход... вот уравнение... проверим... ответ Y.»
```

## Архитектура: как работает thinking

```
Input Tokens
  ↓
<think> токен — начало рассуждения
  → Self-attention внутри thinking block
  → LLM генерирует chain-of-thought свободно
  → Exploring, backtracking, self-correction
</think> токен — конец рассуждения
  ↓
Output generation: финальный ответ
  (используется весь контекст thinking как prefix)
```

**Ключевое**: thinking tokens не показываются пользователю (o1) или показываются (R1, Claude).  
DeepSeek R1 с открытыми thinking tokens дал академическому сообществу беспрецедентный датасет для изучения reasoning.

## Три модели — три подхода

### OpenAI o1 / o3
```
Thinking: скрыто полностью (closed thinking)
  → Пользователь видит только ответ
  → Anthropic/DeepSeek могут видеть = конкурентное преимущество
Управление: budget токенов (low/medium/high reasoning effort)
Специализация: математика, код, логика
```

### DeepSeek R1 (открытые веса)
```
Thinking: полностью открыто → RL без supervision
Обучение: GRPO (Group Relative Policy Optimization)
  → модель сама учится, когда думать и как
  → не нужны размеченные CoT-примеры (дорого)
Открытые веса: можно дистиллировать в меньшую модель
  → DeepSeek R1 Distill 7B = 90% качества R1 при 5% размера
```

### Claude 3.7 Sonnet (hybrid)
```
Первая "гибридная" reasoning-модель:
  → Один вызов API, два режима: think / no-think
  → thinking_budget: max_tokens для reasoning
  → Опциональный streaming thinking tokens
```

## Когда использовать reasoning-модель

```
ИСПОЛЬЗУЙ THINKING если:
  ✅ Математические доказательства, конкурсные задачи
  ✅ Генерация кода с нетривиальной логикой
  ✅ Анализ сложных документов (legal, medical)
  ✅ Задачи, где одна ошибка стоит дорого
  ✅ Задачи, где ответ верифицируем

НЕ ИСПОЛЬЗУЙ THINKING если:
  ❌ Простые вопросы с фактическим ответом
  ❌ Обогащение/форматирование текста (improve_llm_enrich)
  ❌ Классификация/тегирование
  ❌ Latency критична (real-time чат)
  ❌ Batch обработка тысяч документов
```

## Reasoning overhead: когда окупается

```
Стоимость reasoning = 5-60 секунд + N×10 токенов/запрос

Формула окупаемости:
  P(ошибка без thinking) × стоимость_ошибки > стоимость_reasoning

Пример 1: Генерация SQL-запроса
  P(ошибки) = 15%, стоимость = $0 (легко проверить)
  → thinking НЕ нужен

Пример 2: Медицинский диагноз из симптомов
  P(ошибки) = 20%, стоимость = здоровье пациента
  → thinking НУЖЕН

Пример 3: improve_llm_enrich.py (обогащение карточек)
  P(ошибки) = 10%, стоимость = плохая карточка (легко исправить)
  → thinking НЕ нужен
```

## Дистилляция reasoning-моделей (R1 паттерн)

```
Большая reasoning-модель (R1 671B):
  генерирует thinking traces для 800K задач
        ↓
Дистилляция (паттерн R16 + здесь):
  маленькая модель (7B) обучается на этих traces
  → DeepSeek R1 Distill 7B
  → 90% качества при 1% стоимости
        ↓
Итого: reasoning без затрат large model
```

## Применение к Lorenzo

Lorenzo сейчас использует `claude-sonnet-4-6` для всех LLM-задач.  
Reasoning-стратегия для оптимизации:

```python
# improve_llm_router.py (паттерн):
def choose_model(task_type: str) -> str:
    if task_type in ["enrich", "tag", "format"]:
        return "claude-haiku-4-5"      # быстро, дёшево
    if task_type in ["qa", "analysis"]:
        return "claude-sonnet-4-6"     # баланс
    if task_type in ["complex_qa", "contradiction_check"]:
        return "claude-opus-4-7"       # thinking, редко
    if task_type in ["bulk_batch"]:
        return "deepseek-v3"           # дёшево, OpenAI-совместимо
```

Экономия: не использовать Sonnet там, где хватает Haiku.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Reasoning + CoT Illusion (R17)** | R17: CoT вредит простым задачам → Reasoning только для сложных |
| **Reasoning + DSPy (R14)** | DSPy оптимизирует: когда thinking on, когда off |
| **Reasoning + LLM Tests (R20)** | Reasoning-модель генерирует более точные edge cases |
| **Reasoning + DeepSeek (R20)** | DeepSeek V3.2 hybrid = reasoning on demand без смены модели |
| **Reasoning + Incident RAG (R18)** | Reasoning для диагностики: думать перед планом исправления |

## Контакт

- Статья: https://habr.com/ru/companies/selectel/articles/892600/ (март 2025)
- Смежная (Как устроены LLM-агенты): https://habr.com/ru/companies/selectel/articles/916798/
- DeepSeek R1 paper: arxiv.org/abs/2501.12948
- OpenAI o1 system card: openai.com/index/openai-o1-system-card/
- Thinking models: думающие модели: https://habr.com/ru/companies/raft/articles/873372/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
