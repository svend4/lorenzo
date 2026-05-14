---
state: approved
---

# Abstract + Status of This Document

<!-- toc-auto -->
## Contents

- [Abstract](#abstract)
- [0. Status of This Document](#0-status-of-this-document)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: architecture, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

# Nautilus Portal Protocol

**Version:** 1.1.0-draft 
**Status:** Draft — пересмотрен под текущую реализацию v1.1 
**Author:** svend4 
**Editorial review:** Claude (ассистирующий анализ, 2026-04-19) 
**Previous version:** [PORTAL-PROTOCOL.md v1.0](https://github.com/svend4/nautilus/blob/main/docs/PORTAL-PROTOCOL-v1.0.md) 
**License:** CC BY 4.0 (документация) / MIT (reference implementation) 
**Date:** 2026-04 

---

## Abstract

Nautilus Portal Protocol (далее — **NPP**) определяет способ федерации 
независимых Git-репозиториев, содержащих знания в разных native-форматах, 
без их принудительного слияния в единую схему. Протокол специфицирует:

1. Минимальный манифест, объявляющий репозиторий участником федерации 
(`nautilus.json`)
2. Формат человекочитаемого описания репозитория (`passport.md`)
3. Обязательный интерфейс адаптера (`BaseAdapter`)
4. Унифицированную структуру данных (`PortalEntry`)
5. Алгоритм вычисления консенсуса между репозиториями
6. Пространство координат Q6 для семантической близости
7. Четыре уровня совместимости для поэтапного подключения
8. Пять стандартных путей онбординга новых репозиториев
9. REST API контракт для внешних потребителей
10. SDK контракт для программных клиентов

Ключевой принцип: **федерация, а не слияние**. Native-форматы сохраняются 
как есть. Унификация происходит только в момент обращения, через адаптер.

**v1.1 отличается от v1.0 тем, что нормализует практики, возникшие в 
ходе разработки reference implementation**: Q6-пространство как первоклассный 
концепт протокола, пять путей онбординга как equivalent-рангованные 
стратегии, REST API как mandatory для совместимых порталов, поле 
`is_fallback` в PortalEntry, расширенная модель консенсуса с учётом 
fallback-статуса.

---

## 0. Status of This Document

Этот документ — рабочий черновик Nautilus Portal Protocol v1.1. До 
объявления stable v1.1.0 возможны изменения. Breaking changes после 
stable требуют bump до v2.0 с migration guide.

**Обратная совместимость с v1.0**: все v1.0-адаптеры продолжают работать. 
Новые поля (`is_fallback`, Q6-координаты в metadata) — опциональные. 
Порталы v1.1 поддерживают оба протокола через shim-логику.

Комментарии и предложения — через Issues в репозитории 
[github.com/svend4/nautilus](https://github.com/svend4/nautilus).

---

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Abstract Status of This Document"
```

## Смотрите также
- [74-abstract](../../02-anthropic-vacancies/74-abstract.md)
- [04-abstract](../../02-anthropic-vacancies/04-abstract.md)
- [75-0-status-of-this-document](../../02-anthropic-vacancies/75-0-status-of-this-document.md)
- [01-introduction](01-introduction.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [01-introduction](01-introduction.md)
- [README](README.md)
- [reading-paths](../../reading-paths.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [00-abstract-status](../../obsidian/nautilus/npp-v1-1/00-abstract-status.md) (сходство 0.97)
- [74-abstract](../../obsidian/02-anthropic-vacancies/74-abstract.md) (сходство 0.60)
- [74-abstract](../../02-anthropic-vacancies/74-abstract.md) (сходство 0.59)

