# 5. Связь с существующими методологиями

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

**Смотрите также:**
- [112-5-связь-с-существующими-методологиями](docs/02-anthropic-vacancies/112-5-связь-с-существующими-методологиями.md)
- [10-checklist](docs/nautilus/review-methodology/10-checklist.md)
- [12-appendix-a-header-warning](docs/nautilus/review-methodology/12-appendix-a-header-warning.md)
- [09-limitations-open-questions](docs/nautilus/review-methodology/09-limitations-open-questions.md)

