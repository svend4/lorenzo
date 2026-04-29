---
title: "4. Passport (`passport.md`)"
tags:
  - anthropic
  - collaboration
  - nautilus
date: 2026-04-29
---

# 4. Passport (`passport.md`)

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 4. Passport (`passport.md`)

### 4.1. Purpose

Passport — human-readable описание Repo, расположенное в корне 
КАЖДОГО Repo-participant (не в Portal).

Passport предназначен для людей, читающих Repo впервые, и для 
адаптеров, которые могут его парсить для discovery.

### 4.2. Recommended Structure

Passport SHOULD содержать следующие разделы:

```markdown
# 

## Essence
Один абзац: что это, для кого, почему существует.

## Native Format
Формат хранения: `.ext`, структура, примеры.

## Content Overview
Что внутри: типы данных, приблизительный объём, основные темы.

## Angle / Perspective
С какого угла Repo смотрит на общие концепты 
(methodological / semantic / symbolic / other).

## Bridges
Как концепты Repo соотносятся с концепциями других Repos в экосистеме.

## Author & Contact
Кто поддерживает, как связаться.

## History
Когда создан, ключевые версии, направление развития.
```

Passport MAY содержать дополнительные разделы. Passport SHOULD быть 
не длиннее 2 страниц.

### 4.3. Multilingual Support

Passports MAY быть на любом языке. Для международной видимости 
RECOMMENDED иметь минимум две секции: primary language автора + 
English. Рекомендуется формат с параллельными разделами, а не 
отдельные файлы `passport.ru.md` / `passport.en.md` 
(чтобы избежать рассинхрона).

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[16-history]] (сходство 0.37)
- [[16-history]] (сходство 0.33)
- [[09-4-passport-passport-md]] (сходство 0.28)

