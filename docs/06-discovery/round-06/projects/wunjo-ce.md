---
date: 2026-06-05
tags: [knowledge, ingestion, local-first, architecture, collaboration]
state: normalized
---

# Wunjo CE (Video Generation, полностью свободный)
<!-- tags: wunjo-ce, docs -->


<!-- summary -->
> Wunjo CE = multimodal layer для будущего Lorenzo: обогащение карточек видео-превью,  
автоматическая генерация демо-роликов из текстовых описаний проектов.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @wladradchenko (Vladislav Radchenko)  
**Хабр:** https://habr.com/ru/users/wladradchenko/  
**GitHub:** https://github.com/wladradchenko/wunjo.wladradchenko.ru  
**Слой:** media / video-generation / multimodal  
**Зрелость:** активный, 2024–2026  
**Уникальность:** Единственный полностью открытый (CE = Community Edition) инструмент для генерации видео «всё в одном»: text-to-video, image-to-video, face swap, lip sync, клонирование голоса, удаление объектов — **без облачных API, без подписок**. Минимум: 8 ГБ VRAM.

## Что умеет

| Функция | Описание |
|---------|---------|
| Text-to-video | Генерация видео из текстового описания |
| Image-to-video | Анимация изображения |
| Face swap | Замена лица в видео |
| Lip sync | Синхронизация губ с новой аудиодорожкой |
| Voice cloning | Клонирование голоса |
| Object removal | Удаление объектов из видео inpainting |

## Архитектура

- Python + PyTorch + локальные модели (никаких облачных API)
- Веб-интерфейс через FastAPI + Vue.js
- Поддержка CUDA, частично CPU
- Все модели скачиваются автоматически при первом запуске

## Почему интересно для Svyazi

Svyazi работает с документами, но в R06 тема — изображения/видео.  
Wunjo CE = multimodal layer для будущего Lorenzo: обогащение карточек видео-превью,  
автоматическая генерация демо-роликов из текстовых описаний проектов.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Wunjo CE + Lorenzo карточки** | Видео-превью для проектных файлов из текстового описания |
| **Wunjo CE + Natasha (R05)** | NLP извлекает факты → Wunjo генерирует визуализацию |
| **Wunjo CE + News System (R05)** | Автоматическое видео по новостям (text-to-video pipeline) |
| **Wunjo CE + AI Web Tester (R05)** | Скриншот/видео теста → автоматический bug report |

## Контакт

- GitHub: https://github.com/wladradchenko/wunjo.wladradchenko.ru
- Хабр автора: https://habr.com/ru/users/wladradchenko/


## Использование
```bash
# Запуск
python scripts/improve_wunjo_ce.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
