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
   (`[nautilus](../docs/05-habr-projects/memory/memnet.md).json`)
2. Формат человекочитаемого описания репозитория (`passport.md`)
3. Обязательный интерфейс адаптера (`[BaseAdapter](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)`)
4. Унифицированную структуру данных (`[PortalEntry](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)`)
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
`is_fallback` в [PortalEntry](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md), расширенная модель консенсуса с учётом 
fallback-статуса.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [04-abstract](docs/02-anthropic-vacancies/04-abstract.md) (сходство 0.43)
- [76-1-introduction](docs/02-anthropic-vacancies/76-1-introduction.md) (сходство 0.13)
- [77-2-terminology](docs/02-anthropic-vacancies/77-2-terminology.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [04-abstract](docs/02-anthropic-vacancies/04-abstract.md)
- [76-1-introduction](docs/02-anthropic-vacancies/76-1-introduction.md)
- [07-2-terminology](docs/02-anthropic-vacancies/07-2-terminology.md)
- [98-appendix-a-minimal-working-example](docs/02-anthropic-vacancies/98-appendix-a-minimal-working-example.md)

