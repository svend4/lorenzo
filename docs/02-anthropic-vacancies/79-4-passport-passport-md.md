# 4. Passport (`passport.md`)

<!-- toc-auto -->
## Contents

- [4. Passport (passport.md)](#4-passport-passportmd)
  - [4.1. Purpose](#41-purpose)
  - [4.2. Required Structure](#42-required-structure)
  - [4.3. Recommended Sections](#43-recommended-sections)
  - [4.4. Schema Validation](#44-schema-validation)
  - [4.5. Naming Convention](#45-naming-convention)


<!-- summary -->
> Passport — human-readable описание Repo, расположенное в

---
<!-- tags: architecture -->




## 4. Passport (`passport.md`)

### 4.1. Purpose

Passport — human-readable описание Repo, расположенное в 
`passports/<format>.md` **в Portal-репо** (в отличие от v1.0, где 
Passport жил в самом Repo).

Passport предназначен для людей, читающих Repo впервые, для 
адаптеров, которые могут его парсить для discovery, и для 
автоматических систем валидации (через JSON-Schema).

### 4.2. Required Structure

Passport MUST содержать в начале metadata-таблицу с обязательными полями:

```markdown
# Паспорт: /

| Поле | Значение |
|------|----------|
| Репозиторий | / |
| Формат | `.` — краткое описание |
| Единица | что является одной записью |
| Адаптер | `adapters/.py` |
| Уровень совместимости | <0-3> —  |
```

### 4.3. Recommended Sections

Passport SHOULD содержать разделы:

- **Описание** — 2-3 предложения о содержании Repo
- **Объём** — количество единиц, связей
- **Q6-отображение** — правило проекции на 6-битный гиперкуб
- **Мосты** — таблица bridges к другим Repos
- **Примеры запросов** — 3-5 query-string, дающих хорошие результаты
- **Доступ к данным** — `static | github_api | http_api | local_files` + 
  требования к токенам

### 4.4. Schema Validation

Passports MUST проходить валидацию по `passport_schema.json`. 
Portal SHOULD предоставлять команду валидации: 
`python generate_passport.py --validate passports/<format>.md`.

### 4.5. Naming Convention

- Passport-файлы именуются `passports/<format>.md`, не 
  `passports/<repo-name>.md`
- Причина: один format может обслуживаться несколькими репо 
  (например, domain-sub-adapters в рамках pro2), но passport — 
  один на format

---

<!-- similar-docs -->

---

**Похожие документы:**
- [09-4-passport-passport-md](09-4-passport-passport-md.md) (сходство 0.24)
- [78-3-registry-nautilus-json](78-3-registry-nautilus-json.md) (сходство 0.13)
- [08-3-registry-nautilus-json](08-3-registry-nautilus-json.md) (сходство 0.13)


<!-- see-also -->

---

**Смотрите также:**
- [09-4-passport-passport-md](09-4-passport-passport-md.md)
- [08-3-registry-nautilus-json](08-3-registry-nautilus-json.md)
- [78-3-registry-nautilus-json](78-3-registry-nautilus-json.md)
- [82-7-portalentry-structure](82-7-portalentry-structure.md)

<!-- backlinks-auto -->
## Упоминается в

- [2. Terminology](07-2-terminology.md)
- [2. Terminology](77-2-terminology.md)
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md)
- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md)
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md)
- [7. PortalEntry Structure](82-7-portalentry-structure.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md) _48%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _42%_
- [2. Terminology](07-2-terminology.md) _29%_
- [2. Terminology](77-2-terminology.md) _29%_
- [7. PortalEntry Structure](82-7-portalentry-structure.md) _29%_
- [5. Compatibility Levels](80-5-compatibility-levels.md) _25%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _21%_
- [7. PortalEntry Structure](19-7-portalentry-structure.md) _21%_
## Связанные документы

- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _37%_
- [3. Registry (`nautilus.json`)](78-3-registry-nautilus-json.md) _37%_
- [2. Terminology](07-2-terminology.md) _29%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _29%_
- [2. Terminology](77-2-terminology.md) _29%_
- [7. PortalEntry Structure](82-7-portalentry-structure.md) _25%_
- [Appendix A: Minimal Working Example](98-appendix-a-minimal-working-example.md) _25%_
- [7. PortalEntry Structure](19-7-portalentry-structure.md) _21%_
