---
date: 2026-05-28
tags: [memory, rag, ingestion, local-first, architecture]
state: normalized
---

# Self-hosted AI Platform (Open WebUI + Qdrant + Whisper)

<!-- toc-auto -->
<!-- tags: self-hosted-ai-platform, docs -->


<!-- summary -->
> Автор: неизвестен (статья декабрь 2025) Хабр: https://habr.com/ru/articles/973456/
Хабр: https://habr.com/ru/articles/973456/  
GitHub: не найден явно  
Слой: infrastructure / self-hosted / RAG  
Дата: декабрь 2025  
Уникальность: Полный self-hosted AI стек с бенчмарками и ROI-расчётом: Lla


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** неизвестен (статья декабрь 2025)  
**Хабр:** https://habr.com/ru/articles/973456/  
**GitHub:** не найден явно  
**Слой:** infrastructure / self-hosted / RAG  
**Дата:** декабрь 2025  
**Уникальность:** Полный self-hosted AI стек с **бенчмарками и ROI-расчётом**: Llama 3.3 70B даёт 91% RAG-точности (GPT-4 = 96%). Самоокупаемость через **2–3 месяца** при 1000+ запросов в сутки. Включает STT (Whisper), векторную БД (Qdrant/Rust), ChatGPT-подобный UI и обратный прокси с автоматическим HTTPS.

## Стек

| Компонент | Роль | Технология |
|-----------|------|------------|
| **Open WebUI** | ChatGPT-интерфейс + встроенный RAG + история | Python |
| **Qdrant** | Векторная БД, HNSW, оптимизирована под нагрузку | **Rust** |
| **Whisper** (faster-whisper-server) | STT с OpenAI-совместимым API | Python |
| **Redis** | Кеш + очереди для N8N | — |
| **Caddy** | Reverse proxy, авто-HTTPS, zero-config Let's Encrypt | Go |

## Ключевые метрики (из статьи)

| Показатель | Значение |
|------------|---------|
| RAG-точность Llama 3.3 70B | **91%** |
| RAG-точность GPT-4 | 96% |
| Окупаемость | 2–3 месяца при 1000+ запросов/сутки |

## Почему важно для Svyazi

Lorenzo уже имеет `gateway.py` (OpenAI-compatible API на порту 8083).  
Этот стек — production-ready обёртка вокруг него: добавить Open WebUI + Qdrant + Caddy →  
получить полноценную приватную AI-платформу с интерфейсом, HTTPS и мониторингом.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Self-hosted + Lorenzo gateway** | Open WebUI поверх gateway.py → UI для Lorenzo |
| **Self-hosted + n8n AI Stack (R10)** | Оба стека дополняют друг друга (разные компоненты) |
| **Self-hosted + SocratiCode (R08)** | Qdrant уже в стеке → SocratiCode подключается без доп. установки |
| **Self-hosted + Memory MCP v2 (R06)** | Qdrant как backend для engineering memory |

## Контакт

- Статья: https://habr.com/ru/articles/973456/ (декабрь 2025)
- ⚠️ Нужно найти GitHub через профиль автора


## Использование
```bash
# Запуск
python scripts/improve_self_hosted_ai_platform.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
