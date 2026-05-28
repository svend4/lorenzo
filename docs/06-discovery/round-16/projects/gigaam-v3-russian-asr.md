---
date: 2026-05-28
tags: [orchestration, ingestion, local-first, architecture, collaboration]
state: normalized
---

# GigaAM-v3 — SOTA русский ASR от SberDevices

<!-- toc-auto -->
<!-- tags: gigaam-v3-russian-asr, docs -->


<!-- summary -->
> Автор: SberDevices (команда AI-sage / salute-developers) Хабр: https://habr.com/ru/companies/sberdevices/articles/973160/
Хабр: https://habr.com/ru/companies/sberdevices/articles/973160/  
GitHub: https://github.com/salute-developers/GigaAM (MIT)  
Слой: voice / edge-AI / ingestion / local  
Дата: ноябрь 2025


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** SberDevices (команда AI-sage / salute-developers)  
**Хабр:** https://habr.com/ru/companies/sberdevices/articles/973160/  
**GitHub:** https://github.com/salute-developers/GigaAM (MIT)  
**Слой:** voice / edge-AI / ingestion / local  
**Дата:** ноябрь 2025  
**Уникальность:** Лучшая открытая русскоязычная ASR-модель: **Conformer, 220–240M параметров**, обучена на **700 000 часов** русской речи. Бьёт Whisper в среднем 70:30. MIT-лицензия. Прямой выход: пунктуированный нормализованный текст без постобработки. Домены: колл-центры, музыка, голосовые сообщения, атипичная речь.

## Характеристики

| Параметр | Значение |
|----------|---------|
| Архитектура | Conformer (CTC + RNNT) |
| Параметры | 220–240M |
| Обучение | 700 000 часов русской речи |
| Вывод | Пунктуированный + нормализованный текст |
| Лицензия | MIT |
| Установка | pip install gigaam |

## Модели в семействе

| Модель | Режим | Особенность |
|--------|-------|-------------|
| `e2e_ctc` | streaming/batch | быстрый, CTC-декодинг |
| `e2e_rnnt` | batch | точнее, RNNT-декодинг |
| `v2_ctc` | legacy | совместимость с GigaAM-v2 |

## Сравнение с конкурентами

```
WER на русских бенчмарках (меньше = лучше):
GigaAM-v3 e2e_ctc  ████████░░  лучший в категории
GigaAM-v3 e2e_rnnt ██████████  SOTA
Whisper large-v3   ██████░░░░  в 1.4× хуже
Vosk russian       ████░░░░░░  в 2.5× хуже
```

*GigaAM бьёт Whisper в соотношении 70:30 на русских данных*

## Новые домены в v3 (vs v2)

- **Колл-центры** — телефонные разговоры (фоновый шум, сжатие)
- **Музыка** — речь на музыкальном фоне
- **Голосовые сообщения** — неформальная речь, сленг
- **Атипичная речь** — акценты, дизартрия, заикание
- **Результат**: +30% на новых доменах при той же точности на старых

## Pipeline Lorenzo + GigaAM-v3

```bash
# Полный офлайн voice pipeline:
pip install gigaam

import gigaam
model = gigaam.load_model('e2e_ctc')  # или e2e_rnnt

# Транскрипция
transcript = model.transcribe('audio.wav')
# → "Покажи мне статус последних проектов Svyazi."

# Следующий шаг: LLM → действие
```

## Связь с voice pipeline раундов

| Компонент | Источник |
|-----------|---------|
| Wake word (Vosk) | RPi Agent (R11) |
| **STT (GigaAM-v3)** | **R16 — SOTA русский** |
| LLM | Vera (R11) / Qwen (R11) |
| TTS | Ирина (R02) |

GigaAM-v3 **заменяет** Vosk и faster-whisper в русском voice pipeline — лучшее качество.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **GigaAM-v3 + Ирина (R02)** | GigaAM-v3 (STT) + Ирина (TTS) = полный русский offline voice pipeline SOTA |
| **GigaAM-v3 + RPi Agent (R11)** | Заменить faster-whisper на GigaAM-v3 → лучший WER на русском |
| **GigaAM-v3 + Orrin RK3588 (R11)** | GigaAM-v3 на ARM NPU = production edge ASR без облака |
| **GigaAM-v3 + MarkItDown (R14)** | Аудио → GigaAM-v3 → текст → MarkItDown → corpus |

## Контакт

- GitHub: https://github.com/salute-developers/GigaAM (MIT)
- PyPI: pip install gigaam
- HuggingFace: https://huggingface.co/ai-sage/GigaAM-v3
- arXiv: https://arxiv.org/abs/2506.01192
- Статья Хабр: https://habr.com/ru/companies/sberdevices/articles/973160/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
