# 1. Introduction

<!-- summary -->
> Современные системы управления знаниями (Notion, Obsidian, Roam Research,

---
<!-- tags: rag, architecture, collaboration -->




## 1. Introduction

### 1.1. Motivation

Современные системы управления знаниями (Notion, Obsidian, Roam Research, 
Logseq, Coda, Confluence) требуют от пользователя миграции данных в 
единый формат платформы. Это создаёт три проблемы:

1. **Vendor lock-in**: данные становятся заложниками платформы, экспорт 
   теряет семантику
2. **Homogenization**: разные типы знаний (методология, семантика, 
   символизм) принудительно приводятся к одной структуре
3. **Loss of authorship**: каждый автор вынужден работать в чужой модели

NPP предлагает альтернативу: **федеративную модель**, где каждый 
репозиторий сохраняет свой native формат, а переводы между форматами 
происходят через адаптеры по запросу.

### 1.2. Design Goals

Протокол спроектирован так, чтобы одновременно достичь:

- **Low barrier to entry**: подключение существующего репо к федерации 
  занимает не более 5 минут (один файл `nautilus.json` в корне + 
  опциональный passport)
- **Five onboarding paths**: от ручного адаптера до полностью 
  автоматической регистрации через GitHub Actions webhook
- **Local autonomy**: каждый репо остаётся функциональным без портала
- **Progressive enhancement**: репо может подключиться на Level 0 и 
  дорастать до Level 3 без переделки
- **Implementation independence**: спецификация достаточна для написания 
  альтернативных порталов и SDK
- **Forward compatibility**: v1.0 адаптеры совместимы с v1.1 порталами 
  через shim-логику
- **Zero external dependencies**: reference implementation не зависит 
  от внешних Python-пакетов (только stdlib), что делает протокол 
  легко реализуемым в любой среде

### 1.3. Non-Goals

NPP **не** пытается:

- Заменить существующие системы знаний (Notion, Obsidian — они 
  федерируются, не заменяются)
- Обеспечить real-time sync между репо (федерация асинхронна по дизайну)
- Формализовать онтологии (bridges — свободные описания, не OWL/RDF)
- Обеспечить write-operations в федерируемые репо (read-only в v1.x)
- Решить все вопросы аутентификации и RBAC (это — ответственность 
  конкретной implementation, не протокола)

### 1.4. Terminology

Ключевые термины определены в разделе 2. Для ключевых слов 
**MUST**, **MUST NOT**, **SHOULD**, **MAY**, **REQUIRED**, **RECOMMENDED** 
применяется трактовка из RFC 2119.

### 1.5. Changes from v1.0

- **Q6-пространство** перенесено из "reference implementation detail" в 
  нормативный концепт протокола (раздел 8)
- **Пять путей онбординга** (A–E) формализованы как равнорангованные 
  стратегии (раздел 12)
- **REST API контракт** сделан mandatory для совместимых порталов 
  (раздел 13)
- **`is_fallback`** поле добавлено в PortalEntry как нормативное
- **Консенсус-модель** расширена: различаются `coverage` (только real) 
  и `coverage_with_fallback` (раздел 9)
- **Passport schema** формализована в `passport_schema.json` (раздел 4)
- **SDK контракт** добавлен как часть протокола (раздел 14)

---

<!-- similar-docs -->

---

**Похожие документы:**
- [06-1-introduction](docs/02-anthropic-vacancies/06-1-introduction.md) (сходство 0.53)
- [67-о-проекте](docs/02-anthropic-vacancies/67-о-проекте.md) (сходство 0.14)
- [74-abstract](docs/02-anthropic-vacancies/74-abstract.md) (сходство 0.13)


<!-- see-also -->

---

**Смотрите также:**
- [06-1-introduction](docs/02-anthropic-vacancies/06-1-introduction.md)
- [74-abstract](docs/02-anthropic-vacancies/74-abstract.md)
- [67-о-проекте](docs/02-anthropic-vacancies/67-о-проекте.md)
- [77-2-terminology](docs/02-anthropic-vacancies/77-2-terminology.md)

