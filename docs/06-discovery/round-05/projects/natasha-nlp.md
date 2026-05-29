---
date: 2026-05-29
tags: [rag, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# Natasha (Russian NLP)

<!-- toc-auto -->
<!-- tags: natasha-nlp, docs -->


<!-- summary -->
> Автор: @natasha org (Alexander Kukushkin и команда) Хабр: https://habr.com/ru/articles/516098/
Хабр: https://habr.com/ru/articles/516098/  
GitHub: https://github.com/natasha/natasha  
Слой: NLP / text-processing / russian-language  
Зрелость: production, активный с 2019, обновляется  
Уник


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @natasha org (Alexander Kukushkin и команда)  
**Хабр:** https://habr.com/ru/articles/516098/  
**GitHub:** https://github.com/natasha/natasha  
**Слой:** NLP / text-processing / russian-language  
**Зрелость:** production, активный с 2019, обновляется  
**Уникальность:** Лучший открытый NLP-toolkit для русского языка: 9 репозиториев в одном API. В 2020 году — модель в 75× меньше BERT (27 MB), в 30× меньше памяти, в 2× быстрее на CPU. Полный стек: токенизация → морфология → синтаксис → NER → извлечение фактов (даты, деньги, адреса).

## Экосистема (9 репозиториев)

| Компонент | Что делает |
|-----------|------------|
| natasha | Основной API, NER, факты |
| slovnet | Deep Learning NLP моделирование |
| navec | Компактные эмбеддинги для русского |
| razdel | Токенизатор + сегментатор предложений |
| corus | Коллекция русских NLP-датасетов |
| nerus | Большой синтетический датасет |
| naeval | Бенчмарк NLP-систем для русского |

## Почему интересно для Svyazi

Lorenzo работает с русскоязычными документами — 2483 карточки, большинство на русском. Сейчас NER — через `improve_named_entity_index.py` (regex-based). Natasha = замена на production-grade NLP: правильные леммы, синтаксис, NER с высокой точностью.

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **Natasha + improve_named_entity_index** | Замена regex-NER на ML-NER: точные сущности (люди, проекты, даты) |
| **Natasha + improve_keyword_index** | Леммы вместо словоформ → лучший поиск (агент = агента = агентов) |
| **Natasha + knowledge-space** | Автоматическое извлечение фактов (даты, имена, суммы) из документов |
| **Natasha + LiteParse (nlaik)** | Natasha извлекает структуру, LiteParse — доказательства |
| **Natasha + improve_embedding_index** | Navec-эмбеддинги вместо TF-IDF → семантический поиск на русском |

## Контакт

- GitHub org: https://github.com/natasha
- Site: https://natasha.github.io/


## Использование
```bash
# Запуск
python scripts/improve_natasha_nlp.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
