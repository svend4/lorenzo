# Abstract + Status of This Document

<!-- toc-auto -->
## Contents

- [Abstract](#abstract)
- [0. Status of This Document](#0-status-of-this-document)
- [Использование](#использование)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

# Nautilus Portal Protocol

**Version:** 1.0.0-draft 
**Status:** Draft (Working Document) 
**Author:** svend4 
**License:** CC BY 4.0 (documentation) / MIT (reference implementation) 
**Date:** 2026-04 

---

## Abstract

The Nautilus Portal Protocol (далее — NPP) определяет способ федерации 
независимых Git-репозиториев, содержащих знания в разных native-форматах, 
без их принудительного слияния в единую схему. Протокол специфицирует: 
(1) минимальный манифест, который репозиторий размещает для объявления 
своего участия в федерации; (2) интерфейс адаптера, который переводит 
native-формат репозитория в унифицированное представление; (3) алгоритм 
вычисления консенсуса между репозиториями; (4) уровни совместимости для 
постепенного подключения.

Ключевой принцип: **федерация, а не слияние**. Native-форматы сохраняются 
как есть. Унификация происходит только в момент обращения, через адаптер.

---

## 0. Status of This Document

Этот документ — рабочий черновик Nautilus Portal Protocol v1.0. Он может 
изменяться до объявления stable v1.0.0. Breaking changes после stable 
потребуют bump до v2.0 с migration guide.

Комментарии и предложения — через Issues в репозитории github.com/svend4/nautilus.

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Abstract Status of This Document"
```

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал индексирован и доступен для поиска, BM25 и навигации через граф концептов._ _Документ доступен для семантического поиска._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [00-abstract-status](../../obsidian/nautilus/npp-v1-0/00-abstract-status.md) (сходство 0.99)
- [04-abstract](../../obsidian/02-anthropic-vacancies/04-abstract.md) (сходство 0.49)
- [04-abstract](../../02-anthropic-vacancies/04-abstract.md) (сходство 0.49)

