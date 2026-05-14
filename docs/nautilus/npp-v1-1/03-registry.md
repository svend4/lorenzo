---
state: approved
---

# 3. Registry (`nautilus.json`)

<!-- toc-auto -->
## Contents

- [Содержание](#содержание)
- [3. Registry (nautilus.json)](#3-registry-nautilusjson)
  - [3.1. Purpose](#31-purpose)
  - [3.2. Schema](#32-schema)
  - [3.3. Required Fields](#33-required-fields)
  - [3.4. Optional Fields](#34-optional-fields)
  - [3.5. Validation Rules](#35-validation-rules)
  - [3.6. AutoAdapter Special Case](#36-autoadapter-special-case)
- [Смотрите также](#смотрите-также)


<!-- toc -->
## Содержание

- [Contents](#contents)
- [3. Registry (`nautilus.json`)](#3-registry-nautilusjson)
  - [3.1. Purpose](#31-purpose)
  - [3.2. Schema](#32-schema)
  - [3.3. Required Fields](#33-required-fields)
  - [3.4. Optional Fields](#34-optional-fields)
  - [3.5. Validation Rules](#35-validation-rules)
  - [3.6. AutoAdapter Special Case](#36-autoadapter-special-case)
- [Смотрите также](#смотрите-также)

---


- 3. Registry (nautilus.[json)](#3-registry-nautilusjson)
  - [3.1. Purpose](#31-purpose)
  - [3.2. Schema](#32-schema)
  - [3.3. Required Fields](#33-required-fields)
  - [3.4. Optional Fields](#34-optional-fields)
  - [3.5. Validation Rules](#35-validation-rules)
  - 3.6. [AutoAdapter Special Case](#36-autoadapter-special-case)
- 3. Registry (nautilus.[json)](#3-registry-nautilusjson)
  - [3.1. Purpose](#31-purpose)
  - [3.2. Schema](#32-schema)
  - [3.3. Required Fields](#33-required-fields)
  - [3.4. Optional Fields](#34-optional-fields)
  - [3.5. Validation Rules](#35-validation-rules)
  - 3.6. [AutoAdapter Special Case](#36-autoadapter-special-case)
- 3. Registry (nautilus.[json)](#3-registry-nautilusjson)
  - [3.1. Purpose](#31-purpose)
  - [3.2. Schema](#32-schema)
  - [3.3. Required Fields](#33-required-fields)
  - [3.4. Optional Fields](#34-optional-fields)
  - [3.5. Validation Rules](#35-validation-rules)
  - 3.6. [AutoAdapter Special Case](#36-autoadapter-special-case)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: architecture, anthropic -->


> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

## 3. Registry (`nautilus.json`)

### 3.1. Purpose

Registry — central source of truth о том, какие Repos входят в 
экосистему и как их интерпретировать. Располагается в корне 
Portal-репо.

### 3.2. Schema

Registry MUST быть валидным JSON со следующей структурой:

```json
{
"protocol_version": "1.1",
"ecosystem_name": "string",
"registry": [
{
"name": "string",
"repo": "string (owner/repo-name)",
"url": "string (git URL, optional)",
"format": "string (e.g. 'info1', 'pro2')",
"native_unit": "string (human description)",
"adapter": "string (module name, e.g. 'info1' or 'auto')",
"passport": "string (path, e.g. 'passports/info1.md')",
"angle": "string (e.g. 'methodological', 'semantic', 'symbolic')",
"compatibility": 0 | 1 | 2 | 3,
"q6_key": "string (rule for mapping to Q6)",
"bridges": {
"other_repo_name": "string (bridge description)"
}
}
]
}
```

### 3.3. Required Fields

- `protocol_version` — строка в формате semver (`"1.0"`, `"1.1"`). 
Портал MUST отклонять registry с `protocol_version`, не 
поддерживаемым этим порталом
- `ecosystem_name` — короткое уникальное имя (latin, без пробелов)
- `registry` — массив. MUST содержать минимум один элемент

Каждый элемент `registry` MUST содержать:

- `name` — уникальное в пределах экосистемы
- `format` — идентификатор native-формата (используется для 
именования адаптера и passport)
- `adapter` — имя адаптера: либо имя Python-модуля в `adapters/`, 
либо `"auto"` для использования AutoAdapter (см. раздел 12.3)
- `compatibility` — целое 0..3

### 3.4. Optional Fields

- `repo`, `url` — если опущены, Repo существует только локально
- `native_unit` — human-readable описание единицы данных
- `passport` — путь к файлу в формате `passports/<format>.md`. Если 
опущен, адаптер MUST всё равно быть functional
- `angle` — semantic/methodological/symbolic/other — указывает 
"угол зрения" Repo на общие концепты
- `q6_key` — правило проекции native-сущностей в Q6 (например, 
`"hex_id - 1 → bin(6)"` для meta)
- `bridges` — объект: ключи — имена других Repos, значения — 
текстовые описания семантических мостов

### 3.5. Validation Rules

Portal MUST отклонять registry, если:

- JSON невалиден
- Missing required fields в любом элементе `registry`
- `compatibility` вне диапазона 0..3
- Дубликаты `name` в пределах одной экосистемы
- `protocol_version` не поддерживается порталом

Portal SHOULD выдавать warning (но не отклонять), если:

- `repo` или `url` указаны, но недоступны
- `adapter` указан, но модуль не найден
- `bridges` ссылаются на `name`, которых нет в registry
- `passport` указан, но файл не найден

### 3.6. AutoAdapter Special Case

Если `adapter: "auto"`, portal MUST использовать AutoAdapter (см. 
раздел 12.3), который загружает `nautilus.json` из корня 
target-репо вместо локального модуля-адаптера. Это enables 
Onboarding Path C (self-declaring repo).

---

<!-- see-also -->

---

## Смотрите также
- [78-3-registry-nautilus-json](../../02-anthropic-vacancies/78-3-registry-nautilus-json.md)
- [08-3-registry-nautilus-json](../../02-anthropic-vacancies/08-3-registry-nautilus-json.md)
- [07-portal-entry](07-portal-entry.md)
- [02-terminology](02-terminology.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (10):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [18-comment-on-document](../npp-v1-0/18-comment-on-document.md)
- [02-terminology](02-terminology.md)
- [04-passport](04-passport.md)
- [12-onboarding-paths](12-onboarding-paths.md)
- _...ещё 2_


<!-- similar-docs -->

---

**Похожие документы:**
- [03-registry](../../obsidian/nautilus/npp-v1-1/03-registry.md) (сходство 0.98)
- [78-3-registry-nautilus-json](../../obsidian/02-anthropic-vacancies/78-3-registry-nautilus-json.md) (сходство 0.79)
- [78-3-registry-nautilus-json](../../02-anthropic-vacancies/78-3-registry-nautilus-json.md) (сходство 0.79)

