---
state: normalized
---

# Paper2Agent (научные статьи → AI-агенты)

<!-- toc-auto -->
<!-- tags: paper2agent, docs -->


<!-- summary -->
> Автор: @jmiao24 (Stanford) Хабр: https://habr.com/ru/articles/945582/ GitHub: https://github.com/jmiao24/Paper2Agent
Хабр: https://habr.com/ru/articles/945582/  
GitHub: https://github.com/jmiao24/Paper2Agent  
Слой: ingestion / scientific / MCP  
Зрелость: research release, активный  
Уникальность: Конвертирует PDF-статьи в интерактивн


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @jmiao24 (Stanford)  
**Хабр:** https://habr.com/ru/articles/945582/  
**GitHub:** https://github.com/jmiao24/Paper2Agent  
**Слой:** ingestion / scientific / MCP  
**Зрелость:** research release, активный  
**Уникальность:** Конвертирует PDF-статьи в интерактивных AI-агентов через MCP: **Paper2MCP** анализирует статью + код → создаёт MCP-сервер с готовыми инструментами. Пример: AlphaGenome → 22 инструмента за 3 часа на ноутбуке, 100% точность на тестовых запросах.

## Как работает

```
PDF статья + GitHub repo
      ↓ Paper2MCP
  MCP-сервер (инструменты из методов статьи)
      ↓
  Claude Code / ChatGPT
      ↓
  «Запусти метод X с параметрами Y» → результат
```

1. **Extraction** — извлекает код, автоматически настраивает среду для воспроизводимости
2. **Tool generation** — ключевые аналитические функции → MCP-инструменты, итеративно тестируются
3. **Deploy** — MCP-сервер деплоится на Hugging Face Spaces или локально

## Ключевые результаты

- **AlphaGenome**: 22 инструмента (variant scoring, sequence predictions, tissue ontologies, visualizations)
- **100% точность** на 15 запросах из оригинального туториала
- **15 новых запросов** — снова без ошибок vs ручного запуска кода

## Почему важно для Svyazi

Lorenzo работает с Хабр-статьями как источниками знаний.  
Paper2Agent — следующий уровень: статья становится не документом, а **рабочим инструментом**.  
Применимо к `improve_llm_enrich.py`: вместо суммаризации → извлечение методов → MCP-инструменты.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Paper2Agent + Lorenzo ingestion** | Хабр-статья → MCP-инструменты, не просто карточка |
| **Paper2Agent + SocratiCode** | Код из статьи + понимание зависимостей → полный контекст |
| **Paper2Agent + Memory MCP v2 (R06)** | Методы статьи → артефакты в engineering memory backbone |
| **Paper2Agent + improve_llm_enrich** | Stage 3: не суммарки, а работающие инструменты из источников |

## Контакт

- GitHub: https://github.com/jmiao24/Paper2Agent
- Deploy: Hugging Face Spaces (встроенная поддержка)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
