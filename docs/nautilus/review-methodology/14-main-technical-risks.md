# Главные технические риски

<!-- toc-auto -->
## Contents

- [Главные технические риски](#главные-технические-риски)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

---
<!-- tags: anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

## Главные технические риски

Два независимых анализа выделили разные приоритеты:

1. **Отсутствие persistent DB** 
(выделено Вариантом A) — критично для production use case
2. **88% fallback записей в адаптерах** 
(выделено Вариантом B) — критично для демонстрации концепции

Текущая приоритезация автора: **#2 выше** — проект currently в 
proof-of-concept стадии, demonstration value > production 
readiness.
```

---

<!-- see-also -->

---

## Смотрите также
- [120-главные-технические-риски](../../02-anthropic-vacancies/120-главные-технические-риски.md)
- [12-appendix-a-header-warning](12-appendix-a-header-warning.md)
- [15-appendix-c-history](15-appendix-c-history.md)
- [00-question-habr-link](../community-discussions/habr-article-1-reaction/00-question-habr-link.md)

