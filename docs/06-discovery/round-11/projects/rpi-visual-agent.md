---
date: 2026-06-05
tags: [orchestration, ingestion, local-first, architecture, collaboration]
state: normalized
---

# Raspberry Pi Visual Agent (Edge AI, Qwen3 1.7b)

<!-- toc-auto -->
<!-- tags: rpi-visual-agent, docs -->


<!-- summary -->
> Автор: Simone Marculli (GitHub подтверждён) Хабр: https://habr.com/ru/companies/bothub/news/974604/
Хабр: https://habr.com/ru/companies/bothub/news/974604/  
GitHub: профиль Simone Marculli — уточнить точный URL репозитория  
Слой: edge-AI / IoT / local-inference  
Дата: 2025–2026  
Уникальность: Полнос


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Simone Marculli (GitHub подтверждён)  
**Хабр:** https://habr.com/ru/companies/bothub/news/974604/  
**GitHub:** профиль Simone Marculli — уточнить точный URL репозитория  
**Слой:** edge-AI / IoT / local-inference  
**Дата:** 2025–2026  
**Уникальность:** Полностью локальный визуальный AI-ассистент на **Raspberry Pi 5**: Vosk (ключевые слова) + faster-whisper (STT) + Ollama (Qwen3 1.7b + Gemma3 1b). Ничего не покидает устройство. 1B–2B модели — оптимальный баланс скорость/выразительность на RPi. Полная документация: список деталей, установка, конфигурация.

## Железо

| Компонент | Модель |
|-----------|--------|
| Компьютер | Raspberry Pi 5 (8 или 16 ГБ) |
| Микрофон | USB-микрофон |
| Корпус | GeeekPi kit (экран + кулер) |

## Стек (всё локально)

```
Vosk API → ключевые слова / wake word
        ↓
faster-whisper → STT (быстро и точно)
        ↓
Ollama → LLM (Qwen3 1.7b или Gemma3 1b)
        ↓
Ответ на устройстве (TTS или экран)
```

- **Ruby 3.3.0 + Node 22 + Python 3** — runtime
- **Ollama** — инференс локальных моделей
- **AGPL-3.0** — лицензия

## Ключевой принцип

Модели 1B–2B параметров = разумный баланс скорость/качество на RPi.  
Никакой облачной зависимости. Весь pipeline работает офлайн.

## Почему важно для Svyazi

Lorenzo работает на локальной машине. Edge AI на RPi — следующий уровень:  
агент Svyazi, работающий на RPi без отдельного сервера.  
Паттерн «Vosk (wake word) + faster-whisper (STT) + Ollama» применим к любому устройству.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **RPi Agent + Ирина (R02)** | Ирина (русский TTS) + этот стек STT = полный русский voice pipeline |
| **RPi Agent + Ботинок (R06)** | Ботинок = SSH/серверный CLI, RPi Agent = voice edge UI |
| **RPi Agent + openLight (R07)** | RPi управляет инфраструктурой голосом + локально |
| **RPi Agent + Vera** | Vera (десктоп) + RPi (edge) — полная оффлайн экосистема |

## Контакт

- GitHub: Simone Marculli — уточнить точный URL
- Хабр (новость): https://habr.com/ru/companies/bothub/news/974604/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
