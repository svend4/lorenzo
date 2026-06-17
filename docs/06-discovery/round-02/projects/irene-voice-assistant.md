---
date: 2026-06-05
tags: [memory, orchestration, knowledge, ingestion, local-first]
state: normalized
---

# Ирина (Irene Voice Assistant)
<!-- tags: irene-voice-assistant, docs -->


<!-- summary -->
> Хабр: https://habr.com/ru/articles/595855/ GitHub: https://github.com/janvarev/Irene-Voice-Assistant
Хабр: https://habr.com/ru/articles/595855/  
GitHub: https://github.com/janvarev/Irene-Voice-Assistant  
Слой: voice-interface / orchestration  
Дата: активно обновляется (последняя статья + GPT-3 интеграция: 2023, проект живой)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @janvarev  
**Хабр:** https://habr.com/ru/articles/595855/  
**GitHub:** https://github.com/janvarev/Irene-Voice-Assistant  
**Слой:** voice-interface / orchestration  
**Дата:** активно обновляется (последняя статья + GPT-3 интеграция: 2023, проект живой)  
**Уникальность:** Полностью offline русскоязычный голосовой ассистент с системой плагинов (скиллов). Единственный зрелый open-source голосовой проект на Хабре с русскоязычным TTS/STT без облака.

## Что делает

- STT: Vosk (offline, русский)
- TTS: Silero v3 (лучший offline RU голос)
- Архитектура плагинов — скиллы добавляются как Python-модули
- Remote-Irene: клиент-серверная версия (несколько устройств)
- Уже умеет: таймер, погода, медиа, расписание, и ~30 плагинов от комьюнити

## Почему интересно для Svyazi

Svyazi сейчас полностью текстовый. Ирина + knowledge-space = голосовой интерфейс к базе знаний без облака. Архитектура скиллов совпадает с архитектурой Svyazi (скрипт → шаблон → скилл → плагин).

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **Ирина + agent-memory-mcp** | Голосовые запросы сохраняются в MCP-памяти → ассистент помнит контекст разговора |
| **Ирина + knowledge-space** | «Найди мне информацию про AgentFS» → голосом → ответ из базы знаний Svyazi |
| **Ирина + mclaude** | Голосовой front-end для mclaude orchestrator |
| **Ирина + Yodoca** | Голосовые команды → граф знаний (Wikontic-style) обновляется в реальном времени |

## Контакт

- GitHub: https://github.com/janvarev
- Habr профиль автора: https://habr.com/ru/users/janvarev/


## Использование
```bash
# Запуск
python scripts/improve_irene_voice_assistant.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
