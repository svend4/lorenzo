---
state: approved
---

# 4. Условия применимости

<!-- toc-auto -->
## Contents

- [4. Условия применимости](#4-условия-применимости)
  - [4.1. Когда применять](#41-когда-применять)
  - [4.2. Когда НЕ применять](#42-когда-не-применять)
  - [4.3. Когда оппонирует](#43-когда-оппонирует)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

---
<!-- tags: memory, architecture, roadmap, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

## 4. Условия применимости

Методология не универсальна. Она **уместна при следующих условиях**:

### 4.1. Когда применять

- Документ критичен для архитектуры или публичного positioning
- Время на pause между Фазами B и C есть (минимум несколько часов)
- Работа ведётся итеративно с AI-агентами (Claude Code, Cursor, 
Copilot Workspace, similar)
- Потеря одной наблюдения может повлиять на downstream-решения
- Документ длиннее 5-7 страниц (для коротких документов overhead 
превышает пользу)

### 4.2. Когда НЕ применять

- Рутинный README или changelog (single-pass достаточно)
- Code (для кода merge-conflicts — ошибки, не insights; там 
применяются стандартные git-практики)
- Документация с formal schema (OpenAPI, JSON Schema — там 
правильность не субъективна)
- Временно-чувствительные документы, где пауза на консолидацию не 
допустима

### 4.3. Когда оппонирует

Этот подход **не подходит** если:

- Работает команда людей вместо "solo + AI" — human reviewers 
могут координироваться напрямую, не нуждаются в параллельных 
версиях
- Проект follows strict GitFlow с required code review на каждый 
PR
- Вы работаете с критической инфраструктурой (финансы, медицина), 
где transitional states недопустимы

---

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "4 Условия применимости"
```

## Смотрите также
- [111-4-условия-применимости](../../02-anthropic-vacancies/111-4-условия-применимости.md)
- [02-formal-workflow](02-formal-workflow.md)
- [12-appendix-a-header-warning](12-appendix-a-header-warning.md)
- [11-application-plan-current-docs](11-application-plan-current-docs.md)

_Для поиска доступен._

<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [05-conditions-of-applicability](../../obsidian/nautilus/review-methodology/05-conditions-of-applicability.md) (сходство 0.98)
- [111-4-условия-применимости](../../02-anthropic-vacancies/111-4-условия-применимости.md) (сходство 0.67)
- [111-4-условия-применимости](../../obsidian/02-anthropic-vacancies/111-4-условия-применимости.md) (сходство 0.67)

