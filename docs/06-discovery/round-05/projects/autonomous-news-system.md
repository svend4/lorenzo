---
date: 2026-05-15
tags: [rag, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# Autonomous AI News System

<!-- toc-auto -->
<!-- tags: autonomous-news-system, docs -->


<!-- summary -->
> Особенно ценно: паттерн «5 агентов в пайплайне» — каждый отвечает за свой слой обработки.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** неизвестен (статья апрель 2026 — уточнить профиль)  
**Хабр:** https://habr.com/ru/articles/1023446/  
**GitHub:** не найден явно  
**Слой:** ingestion / orchestration / multi-agent  
**Дата:** апрель 2026  
**Уникальность:** Полностью автономная новостная система: 160 источников (RSS + API: Arxiv, TechCrunch, Habr, VC.ru, GitHub...), 5 AI-агентов, 11 воркеров, локальный LLM на домашнем мини-ПК, управление через Telegram. Автор переписал 7 n8n-воркфлоу в единый Python-pipeline за 1.5 месяца. 7 127 записей в БД.

## Что делает

- Сбор новостей каждые 15 минут из 160 источников
- 5 AI-агентов: классификация → резюмирование → дедупликация → ранжирование → публикация
- 11 воркеров параллельно
- Локальная LLM (домашний мини-ПК, без облака)
- Оркестратор принимает команды через Telegram
- Хранит всё в БД (PostgreSQL предположительно)

## Почему интересно для Svyazi

Это **работающий эталон** того, что Svyazi хочет стать: автономная система с несколькими агентами, локальным LLM и Telegram как интерфейсом. Особенно ценно: паттерн «5 агентов в пайплайне» — каждый отвечает за свой слой обработки.

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **News System паттерн + Lorenzo** | 5-агентный пайплайн поверх Lorenzo: Habr → ingestion → classify → summarize → карточка |
| **News System + LiteParse (nlaik)** | LiteParse как агент извлечения evidence из новостей |
| **News System + knowledge-space** | Новости автоматически попадают в граф знаний |
| **News System + Coreness Flow (R02)** | Coreness как event-runtime (каждые 15 мин), News System как бизнес-логика |
| **News System + OpenClaw (R04)** | OpenClaw как Telegram-интерфейс к новостной системе |
| **News System + improve_digest_auto** | Дайджест Lorenzo обогащается свежими внешними новостями |

## Контакт

- Статья: https://habr.com/ru/articles/1023446/ (апрель 2026)
- ⚠️ Нужно найти GitHub через профиль автора


## Использование
```bash
# Запуск
python scripts/improve_autonomous_news_system.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
