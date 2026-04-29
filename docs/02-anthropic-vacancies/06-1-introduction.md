# 1. Introduction

<!-- toc-auto -->
## Contents

- [1. Introduction](#1-introduction)
  - [1.1. Motivation](#11-motivation)
  - [1.2. Design Goals](#12-design-goals)
  - [1.3. Non-Goals](#13-non-goals)
  - [1.4. Terminology](#14-terminology)


<!-- summary -->
> Современные системы управления знаниями (Notion, Obsidian, Roam, Logseq,

---
<!-- tags: collaboration -->




## 1. Introduction

### 1.1. Motivation

Современные системы управления знаниями (Notion, Obsidian, Roam, Logseq, 
Coda, Confluence) требуют от пользователя миграции в их единый формат. 
Это создаёт три проблемы:

1. **Lock-in**: данные становятся заложниками платформы. Экспорт теряет 
   семантику.
2. **Homogenization**: разные типы знаний (методология, семантика, символизм) 
   принудительно приводятся к одной структуре, что уменьшает выразительность.
3. **Loss of authorship**: каждый автор вынужден работать в чужой модели, 
   вместо того чтобы развивать свою.

Альтернатива, предлагаемая NPP: **федеративная модель**, где каждый 
репозиторий сохраняет свой native формат, а переводы между форматами 
происходят через адаптеры по запросу.

### 1.2. Design Goals

Протокол спроектирован так, чтобы одновременно достичь:

- **Low barrier to entry**: подключение существующего репо к федерации 
  требует не больше 5 минут работы (два файла в корень).
- **Local autonomy**: каждый репо остаётся полностью функциональным без 
  портала.
- **Progressive enhancement**: репо может быть подключён на уровне 0 
  (просто обнаруживаем), затем повышен до уровня 3 (интерактивный) 
  постепенно.
- **Implementation independence**: спецификация достаточна для написания 
  альтернативных движков и клиентов.
- **Forward compatibility**: новые версии протокола совместимы со старыми 
  адаптерами через shim-логику движка.

### 1.3. Non-Goals

NPP **не** пытается:

- Заменить существующие системы знаний (Notion, Obsidian — они 
  дополняются, не заменяются)
- Обеспечить real-time sync между репо (федерация асинхронна по дизайну)
- Формализовать онтологии (bridges между репо — свободные текстовые 
  описания, не OWL/RDF)
- Обеспечить write-operations в федерируемые репо (read-only в v1.0)

### 1.4. Terminology

Ключевые термины определены в разделе 2. Для ключевых слов 
**MUST**, **MUST NOT**, **SHOULD**, **MAY**, **REQUIRED**, **RECOMMENDED** 
применяется трактовка из RFC 2119.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [76-1-introduction](76-1-introduction.md) (сходство 0.53)
- [67-о-проекте](67-о-проекте.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [76-1-introduction](76-1-introduction.md)
- [67-о-проекте](67-о-проекте.md)
- [26-14-adr-001-federation-over-merging](26-14-adr-001-federation-over-merging.md)
- [94-19-adr-001-federation-over-merging](94-19-adr-001-federation-over-merging.md)

<!-- backlinks-auto -->
## Упоминается в

- [1. Introduction](76-1-introduction.md)
- [14. ADR-001: Federation over Merging](26-14-adr-001-federation-over-merging.md)
- [19. ADR-001: Federation over Merging](94-19-adr-001-federation-over-merging.md)
- [20. ADR-002: Q6 as First-Class Protocol Concept](95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [21. ADR-003: Five Onboarding Paths as Equal-Rank](96-21-adr-003-five-onboarding-paths-as-equal-rank.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [1. Introduction](76-1-introduction.md) _42%_
## Связанные документы

- [1. Introduction](76-1-introduction.md) _53%_
- [14. ADR-001: Federation over Merging](26-14-adr-001-federation-over-merging.md) _21%_
- [🇷🇺 О проекте](67-о-проекте.md) _17%_
- [2. Terminology](77-2-terminology.md) _17%_
- [19. ADR-001: Federation over Merging](94-19-adr-001-federation-over-merging.md) _17%_
- [20. ADR-002: Q6 as First-Class Protocol Concept](95-20-adr-002-q6-as-first-class-protocol-concept.md) _17%_
- [21. ADR-003: Five Onboarding Paths as Equal-Rank](96-21-adr-003-five-onboarding-paths-as-equal-rank.md) _17%_
