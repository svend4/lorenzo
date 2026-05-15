---
date: 2026-05-15
tags: [memory, orchestration, knowledge, ingestion, local-first]
state: normalized
---

# XAI Agent (SadSabrina)
<!-- tags: xai-agent, docs -->


<!-- summary -->
> Хабр: https://habr.com/ru/articles/1033184/ GitHub: https://github.com/SadSabrina/XAI-open_materials
Хабр: https://habr.com/ru/articles/1033184/  
GitHub: https://github.com/SadSabrina/XAI-open_materials  
Слой: observability / explainability  
Дата: апрель–май 2026  
Уникальность: Агент для генерации XAI (Explainable AI) отчёто


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @SadSabrina  
**Хабр:** https://habr.com/ru/articles/1033184/  
**GitHub:** https://github.com/SadSabrina/XAI-open_materials  
**Слой:** observability / explainability  
**Дата:** апрель–май 2026  
**Уникальность:** Агент для генерации XAI (Explainable AI) отчётов — объясняет решения ML-моделей автоматически. Единственный на Хабре проект, который соединяет Agent Loop с интерпретируемостью моделей (SHAP, feature importance, локальные объяснения).

## Что делает

- Агентский pipeline: получает задачу → вызывает инструменты XAI (SHAP, LIME) → строит отчёт
- Полностью offline (не требует облака)
- Инструменты: метрики качества, feature importance, SHAP, локальные объяснения
- Автор ведёт Telegram-канал с обучающими материалами по data science

## Почему интересно для Svyazi

Svyazi накапливает знания — но не объясняет *почему* те или иные проекты получили высокие оценки. XAI Agent + Collaboration Finder = объяснимые рекомендации коллабораций («вот почему AgentFS + knowledge-space — сильная пара»).

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **XAI Agent + improve_collab_finder** | Объяснимый Collaboration Finder: не просто топ-5, а «почему эти проекты совместимы» |
| **XAI Agent + improve_scoring.py** | Go/No-Go скоринг с объяснением каждого балла |
| **XAI Agent + NGT Memory** | Векторная память с объяснениями почему тот или иной результат релевантен |

## Контакт

- GitHub: https://github.com/SadSabrina
- Telegram: https://t.me/jdata_blog


## Использование
```bash
# Запуск
python scripts/improve_xai_agent.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
