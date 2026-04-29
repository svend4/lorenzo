# 4. Passport (`passport.md`)

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

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
| Уровень совместимости | <0-3> — |
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

<!-- see-also -->

---

**Смотрите также:**
- [79-4-passport-passport-md](docs/02-anthropic-vacancies/79-4-passport-passport-md.md)
- [09-4-passport-passport-md](docs/02-anthropic-vacancies/09-4-passport-passport-md.md)
- [03-registry](docs/nautilus/npp-v1-1/03-registry.md)
- [16-mcp-extension](docs/nautilus/npp-v1-1/16-mcp-extension.md)

