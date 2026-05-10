# Voice / local-first stack

<!-- toc-auto -->
## Contents

- [Описание](#описание)
- [Ключевые компоненты и паттерны](#ключевые-компоненты-и-паттерны)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> - **Авторы:** atatchin / askid / обзоры Handy / OpenWhispr
**Проекты:** Svyazi, Whisper, Yttri

---
<!-- tags: memory, ingestion, local-first, collaboration -->




- **Авторы:** atatchin / askid / обзоры Handy / OpenWhispr
- **Источник:** Хабр citeturn21view10turn21view11turn21view12turn35search0
- **Лицензия:** смешанная картина; для Yttri лицензия в просмотренных источниках не уточнена. citeturn35search0turn21view11
- **Maturity:** от usable scripts до beta‑продукта. citeturn21view10turn35search0
- **Релевантность к Svyazi‑2.0:** средне‑высокая — лучший входной канал для «raw episodes» в память.

## Описание

Локальный speech→text→LLM transform и более широкий local‑first knowledge workspace с recording / transcription.

## Ключевые компоненты и паттерны

- Whisper локально
- Ollama post‑processing
- Handy / OpenWhispr / GigaAM
- Live transcription
- Diarization
- Semantic links
- SQLite

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Voice local-first stack"
```

## Смотрите также
- [memnet](memnet.md)
- [knowledge-space](knowledge-space.md)
- [yodoca](yodoca.md)
- [rufler](rufler.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [authors-by-name](../../glossary/authors-by-name.md)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all.
