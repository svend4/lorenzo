---
title: "Abstract"
tags:
  - architecture
  - anthropic-vacancies
date: 2026-04-29
---

# Abstract

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Abstract Nautilus Portal Protocol (далее — NPP) определяет способ федерации --- Abstract Nautilus Portal Protocol (далее — NPP) определяет способ федерации независимых Git-репозито
> 🔧 **Подход:** Алгоритм вычисления консенсуса между репозиториями 6.
> 🏷️ **Ключевые слова:** `anthropic`, `vacancies`, `abstract`, `introduction`, `terminology`, `nautilus`, `федерации`, `сходство`
>


<!-- summary -->
> Nautilus Portal Protocol (далее — **NPP**) определяет способ федерации

---
<!-- tags: architecture -->




## Abstract

Nautilus Portal Protocol (далее — **NPP**) определяет способ федерации 
независимых Git-репозиториев, содержащих знания в разных native-форматах, 
без их принудительного слияния в единую схему. Протокол специфицирует:

1. Минимальный манифест, объявляющий репозиторий участником федерации 
   (`[[memnet|nautilus]].json`)
2. Формат человекочитаемого описания репозитория (`passport.md`)
3. Обязательный интерфейс адаптера (`[[01-интегральный-анализ-профиля-svend4|BaseAdapter]]`)
4. Унифицированную структуру данных (`[[01-интегральный-анализ-профиля-svend4|PortalEntry]]`)
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
`is_fallback` в [[01-интегральный-анализ-профиля-svend4|PortalEntry]], расширенная модель консенсуса с учётом 
fallback-статуса.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[04-abstract]] (сходство 0.43)
- [[76-1-introduction]] (сходство 0.13)
- [[77-2-terminology]] (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [[04-abstract]]
- [[76-1-introduction]]
- [[07-2-terminology]]
- [[98-appendix-a-minimal-working-example]]

<!-- backlinks-auto -->
## Упоминается в

- [[76-1-introduction|1. Introduction]]
- [[07-2-terminology|2. Terminology]]
- [[77-2-terminology|2. Terminology]]
- [[109-3-принципы-консолидации-фаза-c|3. Принципы консолидации (Фаза C)]]
- [[19-7-portalentry-structure|7. PortalEntry Structure]]
- [[04-abstract|Abstract]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[04-abstract|Abstract]] _33%_
- [[07-2-terminology|2. Terminology]] _25%_
- [[77-2-terminology|2. Terminology]] _25%_
- [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] _21%_
## Связанные документы

- [[04-abstract|Abstract]] _42%_
- [[77-2-terminology|2. Terminology]] _29%_
- [[07-2-terminology|2. Terminology]] _25%_
- [[05-0-status-of-this-document|0. Status of This Document]] _21%_
- [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] _21%_
- [[105-review-methodology-md|REVIEW_METHODOLOGY.md]] _21%_
- [[125-readme-mcp-md-инструкция-по-установке|README-MCP.md— инструкция по установке]] _21%_
- [[19-7-portalentry-structure|7. PortalEntry Structure]] _21%_
