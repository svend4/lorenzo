---
state: approved
---

# 5. Связь с существующими методологиями

<!-- toc-auto -->
## Contents

- [5. Связь с существующими методологиями](#5-связь-с-существующими-методологиями)
  - [5.1. N-Version Programming](#51-n-version-programming)
  - [5.2. Paired Reviews (Academia)](#52-paired-reviews-academia)
  - [5.3. Consensus ML Ensembles](#53-consensus-ml-ensembles)
  - [5.4. Red Team / Blue Team](#54-red-team-blue-team)
  - [5.5. Новое в данной методологии](#55-новое-в-данной-методологии)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

---
<!-- tags: memory, rag, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

## 5. Связь с существующими методологиями

### 5.1. N-Version Programming

Теоретическим прародителем является **N-version programming** 
(Chen & Avizienis, 1977–78) — написание нескольких независимых 
имплементаций одной спецификации для повышения reliability. 
Использовалось в safety-critical systems (Boeing, NASA).

Отличия:

- N-version programming: про код, цель — fault-tolerance
- Трёхфазная методология: про документацию, цель — completeness 
of insights

### 5.2. Paired Reviews (Academia)

В академической рецензии две независимые peer reviews могут 
**противоречить друг другу**. Meta-reviewer (editor) должен 
разрешить противоречие. Структура похожая: two independent → 
consolidation.

Отличия:

- Academic review: A и B — оценки (accept / reject / major revision)
- Наша методология: A и B — конструктивные версии документа

### 5.3. Consensus ML Ensembles

В ML используется **ensemble methods**: несколько моделей → voting 
или averaging. Это разрешение через числовой механизм.

Отличия:

- ML ensembles: разрешение автоматическое, по правилу
- Наша методология: разрешение ручное, через правила 1-5

### 5.4. Red Team / Blue Team

В security и public policy используется структура **red vs blue**: 
один агент критикует, другой защищает. Meta-reviewer interpretates.

Отличия:

- Red/Blue: agents имеют разные роли (adversarial)
- Наша методология: agents имеют одну роль, независимость 
исполнения (convergent)

### 5.5. Новое в данной методологии

Комбинация следующих свойств **не описана** в известной 
литературе:

1. Применение к AI-assisted documentation (а не к человеческой 
работе)
2. Сохранение параллельных версий в main (а не в отдельных ветках)
3. Явный transitional state с документированным header warning
4. Decision tree для ручной консолидации (правила 1-5)

Это делает методологию **потенциально публикационной**.

---

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "5 Связь с существующими методологиями"
```

## Смотрите также
- [112-5-связь-с-существующими-методологиями](../../02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md)
- [10-checklist](10-checklist.md)
- [12-appendix-a-header-warning](12-appendix-a-header-warning.md)
- [09-limitations-open-questions](09-limitations-open-questions.md)


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
- [06-relation-existing-methodologies](../../obsidian/nautilus/review-methodology/06-relation-existing-methodologies.md) (сходство 0.98)
- [112-5-связь-с-существующими-методологиями](../../obsidian/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) (сходство 0.80)
- [112-5-связь-с-существующими-методологиями](../../02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md) (сходство 0.80)

