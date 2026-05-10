# 9. Checklist применения методологии

<!-- toc-auto -->
## Contents

- [9. Checklist применения методологии](#9-checklist-применения-методологии)
  - [9.1. Перед началом (Pre-Phase A)](#91-перед-началом-pre-phase-a)
  - [9.2. Во время Фазы A и B](#92-во-время-фазы-a-и-b)
  - [9.3. После merge to main (Transitional State)](#93-после-merge-to-main-transitional-state)
  - [9.4. Фаза C — Consolidation](#94-фаза-c-consolidation)
- [Смотрите также](#смотрите-также)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

---
<!-- tags: roadmap, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

## 9. Checklist применения методологии

### 9.1. Перед началом (Pre-Phase A)

- [ ] Документ действительно критически важен (см. §4.1)?
- [ ] Есть время на Фазу C в течение 2 недель?
- [ ] Две ветки будут работать на **полностью независимых** 
prompts (не «продолжи вариант A»)?

### 9.2. Во время Фазы A и B

- [ ] Агенты работают в **разных ветках** (не в одной)
- [ ] Prompt'ы для A и B **идентичны** (иначе это не 
независимое воспроизведение)
- [ ] Каждый агент не видит результат другого

### 9.3. После merge to main (Transitional State)

- [ ] Header warning добавлен (см. §2.4)
- [ ] Документ скомпозирован с дубликатами, а не с одним 
выбранным вариантом
- [ ] Ветки A и B не удалены (audit trail)
- [ ] Установлен deadline Фазы C (ISO дата или sprint marker)

### 9.4. Фаза C — Consolidation

- [ ] Прочитаны A и B целиком
- [ ] Outline финальной версии создан
- [ ] Применены правила 1-5 ко всем расхождениям
- [ ] Числа верифицированы (команды из §3.1 Правило 2)
- [ ] Уникальные секции из A и B сохранены
- [ ] Header warning удалён
- [ ] Changelog запись добавлена
- [ ] Исходные ветки могут быть удалены или archived

---

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "9 Checklist применения методологии"
```

## Смотрите также
- [116-9-checklist-применения-методологии](../../02-anthropic-vacancies/116-9-checklist-применения-методологии.md)
- [GITHUB_ISSUES](../../GITHUB_ISSUES.md)
- [13-appendix-b-examples](13-appendix-b-examples.md)
- [02-formal-workflow](02-formal-workflow.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (13):**
- [GITHUB_ISSUES](../../GITHUB_ISSUES.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [01-context-motivation](01-context-motivation.md)
- [02-formal-workflow](02-formal-workflow.md)
- [03-consolidation-principles](03-consolidation-principles.md)
- _...ещё 5_

