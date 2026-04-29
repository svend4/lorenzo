# Вопрос: fallback‑ratio как критический или осмысленный?

> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

---
<!-- tags: memory, rag, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

## Вопрос: fallback-ratio как критический или осмысленный?

Два независимых анализа пришли к разным выводам:

- **Позиция A**: 88% fallback критично, требует срочных живых 
адаптеров для info1/pro2/meta/data2
- **Позиция B**: 88% fallback — осмысленное решение для 
early-stage проекта, приоритет средний

**Текущее решение автора**: [ваше решение + обоснование]
```

Это превращает конфликт в документированный decision point.

### 3.2. Последовательность консолидации

```
1. Прочитать A и B целиком, сформировать ментальную карту общих 
и уникальных разделов
2. Создать outline финальной версии (список секций)
3. Для каждой секции применить правила 1-5
4. Написать черновик финальной версии
5. Проверить, что все уникальные insights из A и B включены
6. Удалить transitional header
7. Добавить changelog-запись: «v3.0 consolidated from A (branch X) 
and B (branch Y) on YYYY-MM-DD»
```

### 3.3. Какие числа проверять в первую очередь

Для Nautilus конкретно, приоритет верификации:

1. **Python LOC** — базовая метрика масштаба проекта
2. **Test count** — indicator качества
3. **Q6 coverage** — ключевая метрика конкретного проекта
4. **Health score** — agregate metric
5. **Adapter count** — structural metric
6. **Commit count** — временная метрика

Всё остальное (даты, версии, названия веток) — проверяется при 
встрече, но не в приоритете.

---

<!-- see-also -->

---

**Смотрите также:**
- [110-вопрос-fallback-ratio-как-критический-или-осмыслен](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md)
- [10-checklist](docs/nautilus/review-methodology/10-checklist.md)
- [07-portal-entry](docs/nautilus/npp-v1-1/07-portal-entry.md)
- [12-appendix-a-header-warning](docs/nautilus/review-methodology/12-appendix-a-header-warning.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [110-вопрос-fallback-ratio-как-критический-или-осмыслен](docs/obsidian/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) (сходство 0.80)
- [110-вопрос-fallback-ratio-как-критический-или-осмыслен](docs/02-anthropic-vacancies/110-вопрос-fallback-ratio-как-критический-или-осмыслен.md) (сходство 0.74)
- [14-main-technical-risks](docs/nautilus/review-methodology/14-main-technical-risks.md) (сходство 0.19)

