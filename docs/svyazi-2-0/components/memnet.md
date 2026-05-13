---
state: normalized
---

# MemNet / memory-is-all-you-need

<!-- toc-auto -->
## Contents

- [Описание](#описание)
- [Ключевые компоненты и паттерны](#ключевые-компоненты-и-паттерны)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (4)](#кто-ссылается-на-этот-документ-4)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> - **Источник:** Хабр + GitHub citeturn21view4turn17search0turn18search2
**Проекты:** Svyazi, MemNet

---
<!-- tags: memory, ingestion, architecture, roadmap, collaboration -->




- **Автор:** Antipozitive
- **Источник:** Хабр + GitHub citeturn21view4turn17search0turn18search2
- **Лицензия:** **MIT**. citeturn17search0turn18search2
- **Maturity:** экспериментальный research codebase. citeturn17search0
- **Релевантность к Svyazi‑2.0:** средне‑высокая — не MVP‑слой, но сильная идея для future memory engine.

## Описание

Исследовательская активная память для трансформеров.

## Ключевые компоненты и паттерны

- Hebbian graph memory
- STDP
- Spreading activation
- «Dreaming»
- Anti‑forgetting

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "MemNet memory is all you need"
```

```bash
# Поиск (bm25)
python scripts/improve_semantic_search.py --query "MemNet memory is all you need" --mode bm25 --top 5
```

```bash
# Поиск (semantic)
python scripts/improve_semantic_search.py --query "MemNet memory is all you need" --mode semantic --top 10
```

```bash
# Поиск (full)
python scripts/improve_semantic_search.py --query "MemNet memory is all you need" --mode full --top 15
```

```bash
# Поиск (bm25)
python scripts/improve_semantic_search.py --query "MemNet memory is all you need" --mode bm25 --top 5
```

## Смотрите также
- [ngt-memory](ngt-memory.md)
- [yodoca](yodoca.md)
- [rufler](rufler.md)
- [knowledge-space](knowledge-space.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (4)
- [authors-by-name](../../glossary/authors-by-name.md)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал индексирован и доступен для поиска, BM25 и навигации через граф концептов._ _Документ доступен для семантического поиска._ _Индексировано._

<!-- similar-docs -->

---

**Похожие документы:**
- [memnet](../../obsidian/svyazi-2-0/components/memnet.md) (сходство 0.97)
- [ngt-memory](ngt-memory.md) (сходство 0.45)
- [rufler](rufler.md) (сходство 0.44)

