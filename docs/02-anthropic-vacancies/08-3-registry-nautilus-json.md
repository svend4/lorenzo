# 3. Registry (`nautilus.json`)

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Registry (nautilus.json)(3-registry-nautilusjson) - 3.1.
> 🔧 **Подход:** Validation Rules(35-validation-rules) !IMPORTANT Ключевой документ для понимания архитектуры.
> 🏷️ **Ключевые слова:** `registry`, `nautilus`, `fields`, `anthropic`, `vacancies`, `terminology`, `required`, `optional`
>


<!-- toc-auto -->
## Contents

- [3. Registry (nautilus.json)](#3-registry-nautilusjson)
  - [3.1. Purpose](#31-purpose)
  - [3.2. Schema](#32-schema)
  - [3.3. Required Fields](#33-required-fields)
  - [3.4. Optional Fields](#34-optional-fields)
  - [3.5. Validation Rules](#35-validation-rules)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Registry — central source of truth о том, какие Repos входят в

---
<!-- tags: architecture -->




## 3. Registry (`nautilus.json`)

### 3.1. Purpose

Registry — central source of truth о том, какие Repos входят в 
экосистему и как их интерпретировать. Располагается в корне 
Portal-репо.

### 3.2. Schema

Registry MUST быть валидным JSON со следующей структурой:

```json
{
  "protocol_version": "1.0",
  "ecosystem_name": "string",
  "repositories": [
    {
      "name": "string",
      "url": "string (git URL)",
      "format": "string (e.g. '.info1')",
      "native_unit": "string (human description)",
      "adapter": "string (relative path to adapter file)",
      "passport": "string (relative path to passport file)",
      "angle": "methodological | semantic | symbolic | other",
      "compatibility_level": 0 | 1 | 2 | 3,
      "bridges": {
        "other_repo_name": "string (description of bridge)"
      }
    }
  ]
}
```

### 3.3. Required Fields

- `protocol_version` — строка в формате semver. v1.0 совместимо с 
  минорными обновлениями.
- `ecosystem_name` — короткое уникальное имя (latin, без пробелов).
- `repositories` — массив. MUST содержать минимум один элемент.

Каждый элемент `repositories` MUST содержать:

- `name` — уникальное в пределах экосистемы
- `format` — идентификатор native-формата
- `adapter` — путь к файлу адаптера
- `compatibility_level` — целое 0..3

### 3.4. Optional Fields

Все остальные поля OPTIONAL, но SHOULD быть заполнены для хорошей 
discoverability:

- `url` — если опущен, Repo существует только локально
- `native_unit`, `passport`, `angle` — human-readable metadata
- `bridges` — пустой объект допустим, если мостов нет

### 3.5. Validation Rules

Implementation MUST отклонять registry, если:

- JSON невалиден
- Missing required fields
- `compatibility_level` вне диапазона 0..3
- Дубликаты `name` в пределах одной экосистемы

Implementation SHOULD выдавать warning (но не отклонять), если:

- `url` указан, но недоступен
- `adapter` указан, но файл не найден
- `bridges` ссылаются на `name`, которых нет в registry

---

<!-- similar-docs -->

---

**Похожие документы:**
- [78-3-registry-[nautilus](../docs/05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md) (сходство 0.52)
- [07-2-terminology](docs/02-anthropic-vacancies/07-2-terminology.md) (сходство 0.16)
- [77-2-terminology](docs/02-anthropic-vacancies/77-2-terminology.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [78-3-registry-[nautilus](../docs/05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md)
- [82-7-portalentry-structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md)
- [19-7-portalentry-structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md)
- [07-2-terminology](docs/02-anthropic-vacancies/07-2-terminology.md)

