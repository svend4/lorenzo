# Различие 2: Domain-specific specialization

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Resear

---
<!-- tags: architecture, anthropic -->

> [!IMPORTANT]
> Нормативный документ. Описывает контракты и архитектурные решения.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Различие 2: Domain-specific specialization

Skills в Hermes общие. Functional capabilities. 118 skills covering web search, code execution, file management, communication, etc.

Наши семь документов focus на domain-specific specialization — Composite Skills Agent для немецкого социального права, Professional Colleague Agents для специфических профессий, Representative Agents для уязвимых граждан.

Hermes не имеет этого domain layer. Чтобы превратить Hermes в SGB Advocate Colleague, нужно создать domain-specific skills — что именно то, что наш Document 6 и 7 предлагают.

То есть Hermes — это реализованная инфраструктура, наши documents — specifications для domain-specific applications на этой инфраструктуре.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Различие 2 Domain specific"
```

## Смотрите также
- [01-similarity-1-composite-skills](01-similarity-1-composite-skills.md)
- [09-difference-4-institutional-vision](09-difference-4-institutional-vision.md)
- [10-difference-5-tool-vs-mission-drift](10-difference-5-tool-vs-mission-drift.md)
- [02-similarity-2-persistent-memory](02-similarity-2-persistent-memory.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25.

<!-- backlinks -->

---

**Кто ссылается на этот документ (13):**
- [CONCEPTS](../../CONCEPTS.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [01-similarity-1-composite-skills](01-similarity-1-composite-skills.md)
- [02-similarity-2-persistent-memory](02-similarity-2-persistent-memory.md)
- [09-difference-4-institutional-vision](09-difference-4-institutional-vision.md)
- _...ещё 5_

