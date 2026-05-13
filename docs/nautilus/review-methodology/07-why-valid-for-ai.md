---
state: normalized
---

# 6. Почему это валидный паттерн для AI‑assisted workflows

<!-- toc-auto -->
## Contents

- [6. Почему это валидный паттерн для AI-assisted workflows](#6-почему-это-валидный-паттерн-для-ai-assisted-workflows)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

---
<!-- tags: anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

## 6. Почему это валидный паттерн для AI-assisted workflows

Традиционная software engineering оптимизировалась против 
дублирования кода и документации — это разумно, когда каждая 
работа стоит человеческих часов.

С AI-агентами ситуация **меняется количественно**. Каждый запуск 
Claude Code — минуты работы, не часы. Создание параллельной версии 
документа — дешевле, чем потеря единственного insight.

**ROI меняется в другую сторону**: избыточность больше не люкс, а 
страховка.

Это пример **adaptation of engineering practice к новой реальности 
AI-assisted development**. Старые правила («избегай дублирования») 
требуют переосмысления, когда unit cost меняется в 10-100 раз.

Аналогичные переосмысления происходят в других областях:

- **Code generation**: меньше DRY-полicy, больше regenerate-on-demand
- **Testing**: меньше handcraft, больше auto-generated property tests
- **Documentation**: меньше "write once", больше "iterate with AI"

Трёхфазная методология — часть этого shift.

---

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "6 Почему это валидный паттерн для AI"
```

## Смотрите также
- [113-6-почему-это-валидный-паттерн-для-ai-assisted-work](../../02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md)
- [15-appendix-c-history](15-appendix-c-history.md)
- [12-appendix-a-header-warning](12-appendix-a-header-warning.md)
- [14-main-technical-risks](14-main-technical-risks.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в базе репозитория Lorenzo и доступен для семантического поиска._ _Доступен семантический поиск._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [113-6-почему-это-валидный-паттерн-для-ai-assisted-work](../../02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [07-why-valid-for-ai](../../obsidian/nautilus/review-methodology/07-why-valid-for-ai.md) (сходство 0.98)
- [113-6-почему-это-валидный-паттерн-для-ai-assisted-work](../../02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) (сходство 0.78)
- [113-6-почему-это-валидный-паттерн-для-ai-assisted-work](../../obsidian/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md) (сходство 0.77)

