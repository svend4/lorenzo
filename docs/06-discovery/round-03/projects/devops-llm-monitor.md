---
date: 2026-05-29
tags: [memory, rag, knowledge, ingestion, local-first]
state: normalized
---

# DevOps LLM Monitor
<!-- tags: devops-llm-monitor, docs -->


<!-- summary -->
> Это единственный на Хабре case «свой домен-специфичный LLM как решение реальной задачи мониторинга».


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @oni_devops_lab (Telegram/Habr)  
**Хабр:** https://habr.com/ru/articles/1033128/ (часть 1), https://habr.com/ru/articles/1033426/ (часть 2 — обучение)  
**GitHub:** не найден (нужно уточнить через Telegram @oni_devops_lab или @oni_devops_bot)  
**Слой:** observability / domain-specific-LLM / devops  
**Дата:** апрель–май 2026 (живая серия)  
**Уникальность:** Разработчик не взял готовый LLM — он **дообучил Qwen3 с LoRA** специально под DevOps-мониторинг своих проектов, чтобы уйти в отпуск без тревоги. Использует дистилляцию: gemma4 как учитель, Qwen3 как ученик. RTX 3090 24GB. Это единственный на Хабре case «свой домен-специфичный LLM как решение реальной задачи мониторинга».

## Что делает

- Fine-tuned Qwen3 (QLoRA) на DevOps-кейсах: анализ логов, ошибок, алертов
- Дистилляция: крупная модель (gemma4) генерирует датасет, маленькая обучается
- Incremental delta-LoRA: v1 → тест → delta на новых примерах → v2
- Telegram-бот @oni_devops_bot (планируется публичное демо)
- Мониторит проекты автономно, пока автор в отпуске

## Почему интересно для Svyazi

Паттерн «дообучи маленькую модель под свою задачу» — это следующий шаг для Svyazi после RAG. Вместо поиска по 2483 документам — своя модель, которая уже знает базу. Плюс: сам процесс дистилляции (учитель→ученик) применим к любому корпусу Lorenzo.

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **DevOps LLM паттерн + Lorenzo corpus** | Дистиллировать знания Svyazi в маленькую локальную модель (offline Knowledge OS) |
| **DevOps LLM + improve_llm_enrich** | LLM-обогащение через дообученную модель вместо API (бесплатно, offline) |
| **DevOps LLM + NGT Memory** | Дообученная модель + ассоциативный граф = персонализированный Knowledge OS |

## Контакт

- Telegram: https://t.me/oni_devops_lab
- Telegram-бот: @oni_devops_bot (демо)


## Использование
```bash
# Запуск
python scripts/improve_devops_llm_monitor.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
