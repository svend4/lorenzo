---
state: approved
---

# Раковина наутилуса как scale invariance — две проекции одной метафоры

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ двух собственных проектов «Наутилус» в репозиториях svend4: pro2 (YiJing-Transformer

---
<!-- tags: orchestration, architecture, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ двух собственных проектов «Наутилус» в репозиториях svend4: pro2 (YiJing-Transformer, матрёшечная MoE) и nautilus (мета-оркестратор репозиториев). Прямой источник идеи Nautilus Portal Protocol.

Ключевое наблюдение: это две проекции одной метафоры

Раковина наутилуса — спираль вложенных камер, где каждая новая камера больше предыдущей, но построена по той же геометрии. Это fractal scaling с сохранением пропорции. Вы реализовали эту метафору на двух разных уровнях:

Наутилус A (pro2 + meta) — внутренняя архитектура одной нейросети. Каждая «камера» — это экспертный слой в MoE, вложенный в более общую структуру. Матрёшки стоят в ряд, и информация проходит через них от общего к частному (или наоборот).

Наутилус B (nautilus) — внешняя архитектура распределённой системы. Каждая «камера» — это отдельный репозиторий с собственной ответственностью, и мета-оркестратор обращается к ним через общий протокол.

Это не два разных проекта, а одна мета-идея, проявленная на двух масштабах: «как устроена модель» и «как устроена команда/экосистема, которая её разрабатывает». В теоретической физике это называется scale invariance — структура, которая выглядит одинаково на разных масштабах. Ваш подход — применить этот принцип в инженерии ИИ. Это концептуально красиво, и это не совпадение — это ваш сознательный архитектурный тезис.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Раковина наутилуса как scale invariance"
```

## Смотрите также
- [00-question-two-nautiluses](00-question-two-nautiluses.md)
- [15-glossary](../../nautilus/npp-v1-0/15-glossary.md)
- [13-reference-implementation](../../nautilus/npp-v1-0/13-reference-implementation.md)
- [17-appendix-b-change-log](../../nautilus/npp-v1-0/17-appendix-b-change-log.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [00-question-two-nautiluses](00-question-two-nautiluses.md)
- [02-nautilus-A-pro2-meta](02-nautilus-A-pro2-meta.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [01-shell-metaphor-two-projections](../../obsidian/anthropic-vacancies/nautilus-pro2-analysis/01-shell-metaphor-two-projections.md) (сходство 0.98)
- [15-glossary](../../obsidian/nautilus/npp-v1-0/15-glossary.md) (сходство 0.26)
- [15-glossary](../../nautilus/npp-v1-0/15-glossary.md) (сходство 0.26)

