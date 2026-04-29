# Abstract

<!-- summary -->
> Nautilus Portal Protocol (далее — **NPP**) определяет способ федерации

---
<!-- tags: architecture -->




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

<!-- similar-docs -->

---

**Похожие документы:**
- [04-abstract](04-abstract.md) (сходство 0.43)
- [76-1-introduction](76-1-introduction.md) (сходство 0.13)
- [77-2-terminology](77-2-terminology.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [04-abstract](04-abstract.md)
- [76-1-introduction](76-1-introduction.md)
- [07-2-terminology](07-2-terminology.md)
- [98-appendix-a-minimal-working-example](98-appendix-a-minimal-working-example.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [Abstract](04-abstract.md) _42%_
- [2. Terminology](77-2-terminology.md) _29%_
- [2. Terminology](07-2-terminology.md) _25%_
- [0. Status of This Document](05-0-status-of-this-document.md) _21%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _21%_
- [REVIEW_METHODOLOGY.md](105-review-methodology-md.md) _21%_
- [README-MCP.md— инструкция по установке](125-readme-mcp-md-инструкция-по-установке.md) _21%_
- [7. PortalEntry Structure](19-7-portalentry-structure.md) _21%_
